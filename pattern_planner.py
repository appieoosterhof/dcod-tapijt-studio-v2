"""
BUILD-013 -- Pattern Planner.

Implementeert de Pattern Planner conform de goedgekeurde ontwerpbaseline
(AB-011, BUILD-013 functioneel + technisch/TD-003). De Pattern Planner is de
downstream-component ná de Material Planner: hij vormt uitsluitend
patroonvoorstellen (= Pattern Profiles met status "Voorgesteld") op basis van
de DRIE bevestigde upstream-objecten -- het bevestigde Concept, het bevestigde
Floor Design en het bevestigde Material Profile. Hij STELT VOOR, bevestigt nooit.

Kernprincipes (technisch geborgd, conform AB-011):
  * de component stelt voor, bevestigt nooit;
  * AI-model-onafhankelijk: de redeneerstap loopt via een injecteerbare
    boundary die DesignContext noch registratie kent; geen LLM, geen prompt;
  * het Pattern Profile is een zelfstandig resultaat-object BUITEN de
    DesignContext; de DesignContext en de bevestigde upstream-objecten worden
    uitsluitend gelezen;
  * drievoudige deterministische preconditie: start uitsluitend bij een
    bevestigd Concept (Concept.status == "bevestigd"), een bevestigd Floor
    Design (FloorDesign.status == "Bevestigd") en een bevestigd Material
    Profile (MaterialProfile.status == "Bevestigd").

Volledig additief en losstaand: GEEN wijziging aan design_context.py,
reasoning_engine.py of material_planner.py; geen koppeling aan de live pipeline.
Nog NIET geimplementeerd: SVG Planner, Floor Visualization Engine, Design
Transfer Package, de overige downstream-componenten en persistentie.
"""

from __future__ import annotations

import copy
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

from design_context import Concept, DesignContext
from reasoning_engine import FloorDesign
from material_planner import MaterialProfile


# ─── Pattern Reasoning Boundary (AI-model-onafhankelijk) ─────────────────────
#
# Contract: een functie die een platte invoer-dict ontvangt (projectie van de
# drie bevestigde objecten) en een lijst patroonvoorstellen retourneert, elk
# met de patroonbeschrijving en een "motivering". Zij kent DesignContext noch
# registratie -- puur voorstel in, voorstel uit.

PatroonRedeneerFunctie = Callable[[dict], list]


def placeholder_patroon_generatie(invoer: dict) -> list:
    """Deterministische placeholder voor de Pattern Reasoning Boundary.

    Geen LLM-aanroep, geen promptteksten. Leidt uit het bevestigde Concept, de
    ontwerprichting van het bevestigde Floor Design en de materiaal-structuur
    van het bevestigde Material Profile een of meer patroonvoorstellen af, zodat
    de keten preconditie -> boundary -> validatie -> regeneratie testbaar is
    zonder AI.
    """
    stijl = invoer.get("stijlfamilie") or "de gekozen stijl"
    richting = invoer.get("ontwerprichting") or "de gekozen ontwerprichting"
    structuur = invoer.get("structuur") or "het gekozen materiaal"
    return [
        {
            "motiefstructuur": f"organisch, vloeiend ({stijl})",
            "motiefschaal": "medium",
            "dichtheid": "open",
            "herhalingskarakter": "half-drop",
            "motivering": f"Rustig, vloeiend patroon voor {richting}, passend bij {structuur}.",
        },
        {
            "motiefstructuur": f"geometrisch, ritmisch ({stijl})",
            "motiefschaal": "medium",
            "dichtheid": "dicht",
            "herhalingskarakter": "full",
            "motivering": f"Ritmisch alternatief voor {richting}, zelfde Concept.",
        },
    ]


@dataclass
class PatternProfile:
    """Technisch datamodel van een voorgesteld Pattern Profile -- BUITEN de
    DesignContext (AB-011). Draagt de motivering in het object zelf en drie
    enkelvoudige herkomst-referenties naar het bevestigde Concept, Floor Design
    en Material Profile (traceerbaarheid)."""

    identifier: str
    motiefstructuur: Optional[str]
    motiefschaal: Optional[str]
    dichtheid: Optional[str]
    herhalingskarakter: Optional[str]
    motivering: str
    concept_herkomst: dict
    floor_design_herkomst: dict
    material_profile_herkomst: dict
    status: str = "Voorgesteld"
    kwaliteitsinformatie: dict = field(default_factory=dict)


@dataclass
class PatternProfileResultaat:
    """Technische returnvorm: één of meer voorgestelde Pattern Profiles, of
    uitsluitend signaleringen wanneer de Pattern Planner niet mag of kan
    slagen."""

    pattern_profiles: list = field(default_factory=list)
    signaleringen: list[str] = field(default_factory=list)
    kwaliteitsinformatie: dict = field(default_factory=dict)

    @property
    def geslaagd(self) -> bool:
        return len(self.pattern_profiles) > 0


class PatternPlanner:
    """Publieke component (BUILD-013).

    `stel_pattern_profiles_voor(dc, floor_design, material_profile)` leidt uit de
    drie bevestigde upstream-objecten één of meer voorgestelde Pattern Profiles
    af (buiten de DesignContext, met motivering en drie herkomst-referenties).
    De component leest de DesignContext, het Floor Design en het Material Profile
    uitsluitend; hij wijzigt niets en bevestigt nooit.
    """

    STATUS_CONCEPT_BEVESTIGD = "bevestigd"        # laag 4 (Concept)
    STATUS_FLOOR_DESIGN_BEVESTIGD = "Bevestigd"   # Floor Design (AB-006)
    STATUS_MATERIAL_PROFILE_BEVESTIGD = "Bevestigd"  # Material Profile (AB-010)
    STATUS_VOORGESTELD = "Voorgesteld"            # Pattern Profile
    _VERPLICHTE_CONCEPT_VELDEN = ("stijlfamilie", "kleurpalet", "complexiteit", "motiefschaal")
    _VERPLICHTE_PATROON_VELDEN = ("motiefstructuur", "motiefschaal")
    MAX_REGENERATIE_POGINGEN = 3

    def __init__(self, patroon_generatie: PatroonRedeneerFunctie = placeholder_patroon_generatie) -> None:
        # De Pattern Reasoning Boundary is injecteerbaar; standaard de placeholder.
        self._patroon_generatie = patroon_generatie

    # ── Orkestratie ───────────────────────────────────────────────────────────
    def stel_pattern_profiles_voor(
        self, dc: DesignContext, floor_design: FloorDesign, material_profile: MaterialProfile
    ) -> PatternProfileResultaat:
        """Orkestreert de verwerkingsketen: preconditie -> boundary ->
        validatie -> (gelimiteerde) regeneratie -> verpakken. Leest de
        DesignContext, het Floor Design en het Material Profile uitsluitend."""
        # 1. Drievoudige deterministische preconditie.
        signaleringen = self._valideer_preconditie(dc, floor_design, material_profile)
        if signaleringen:
            return PatternProfileResultaat(signaleringen=signaleringen)

        invoer = self._verzamel_invoer(dc, floor_design, material_profile)
        concept_herkomst = self._concept_snapshot(dc.concept)
        fd_herkomst = self._floor_design_snapshot(floor_design)
        mp_herkomst = self._material_profile_snapshot(material_profile)
        laatste_afkeur: list[str] = []

        # 2-4. Boundary + validatie, met gelimiteerde regeneratie.
        for poging in range(1, self.MAX_REGENERATIE_POGINGEN + 1):
            try:
                voorstellen = self._patroon_generatie(invoer)
            except Exception as fout:  # boundary is injecteerbaar en onbekend
                return PatternProfileResultaat(
                    signaleringen=[f"Technische fout in de reasoning boundary: {fout}"]
                )

            geldig, laatste_afkeur = self._filter_geldig(voorstellen)
            if geldig:
                profielen = [
                    self._bouw_pattern_profile(v, concept_herkomst, fd_herkomst, mp_herkomst, poging)
                    for v in geldig
                ]
                return PatternProfileResultaat(
                    pattern_profiles=profielen,
                    kwaliteitsinformatie={
                        "pogingen": poging,
                        "aantal": len(profielen),
                        "afgekeurd": len(laatste_afkeur),
                    },
                )

        # 5. Regeneratielimiet bereikt -> geen geldig resultaat, geen mutatie.
        return PatternProfileResultaat(
            signaleringen=(
                [
                    f"Geen geldig patroonvoorstel na "
                    f"{self.MAX_REGENERATIE_POGINGEN} pogingen."
                ]
                + laatste_afkeur
            ),
            kwaliteitsinformatie={"pogingen": self.MAX_REGENERATIE_POGINGEN},
        )

    # ── Preconditie (drievoudige deterministische gate) ───────────────────────
    def _valideer_preconditie(
        self, dc: DesignContext, floor_design: FloorDesign, material_profile: MaterialProfile
    ) -> list[str]:
        signaleringen: list[str] = []

        if dc.concept.status != self.STATUS_CONCEPT_BEVESTIGD:
            signaleringen.append(
                'Concept is niet bevestigd; Pattern Planner start niet '
                '(vereist Concept.status == "bevestigd").'
            )
        else:
            for veld in self._VERPLICHTE_CONCEPT_VELDEN:
                waarde = getattr(dc.concept, veld)
                if waarde is None or (isinstance(waarde, str) and not waarde.strip()):
                    signaleringen.append(f"Bevestigd Concept mist verplicht veld: {veld}.")

        if floor_design is None:
            signaleringen.append("Geen Floor Design meegegeven.")
        elif floor_design.status != self.STATUS_FLOOR_DESIGN_BEVESTIGD:
            signaleringen.append(
                'Floor Design is niet bevestigd; Pattern Planner start niet '
                '(vereist FloorDesign.status == "Bevestigd").'
            )
        elif not (floor_design.ontwerprichting and floor_design.identifier):
            signaleringen.append("Bevestigd Floor Design is niet identificeerbaar.")

        if material_profile is None:
            signaleringen.append("Geen Material Profile meegegeven.")
        elif material_profile.status != self.STATUS_MATERIAL_PROFILE_BEVESTIGD:
            signaleringen.append(
                'Material Profile is niet bevestigd; Pattern Planner start niet '
                '(vereist MaterialProfile.status == "Bevestigd").'
            )
        elif not material_profile.identifier:
            signaleringen.append("Bevestigd Material Profile is niet identificeerbaar.")

        return signaleringen

    # ── Invoer voor de boundary ───────────────────────────────────────────────
    @staticmethod
    def _verzamel_invoer(
        dc: DesignContext, floor_design: FloorDesign, material_profile: MaterialProfile
    ) -> dict:
        c = dc.concept
        return {
            "stijlfamilie": c.stijlfamilie,
            "kleurpalet": c.kleurpalet,
            "complexiteit": c.complexiteit,
            "motiefschaal": c.motiefschaal,
            "ontwerprichting": floor_design.ontwerprichting,
            "structuur": material_profile.structuur,
            "pooltype": material_profile.pooltype,
            "uitstraling": material_profile.uitstraling,
        }

    # ── Herkomst-referenties (traceerbaarheid) ────────────────────────────────
    @staticmethod
    def _concept_snapshot(concept: Concept) -> dict:
        return {
            "stijlfamilie": concept.stijlfamilie,
            # Defensieve kopie: kleurpalet is een mutabele dict; een snapshot moet
            # bevroren blijven ook als het bron-Concept later zou wijzigen.
            "kleurpalet": copy.deepcopy(concept.kleurpalet),
            "complexiteit": concept.complexiteit,
            "motiefschaal": concept.motiefschaal,
            "status": concept.status,
        }

    @staticmethod
    def _floor_design_snapshot(floor_design: FloorDesign) -> dict:
        return {
            "identifier": floor_design.identifier,
            "ontwerprichting": floor_design.ontwerprichting,
            "status": floor_design.status,
        }

    @staticmethod
    def _material_profile_snapshot(material_profile: MaterialProfile) -> dict:
        return {
            "identifier": material_profile.identifier,
            "materiaalsoort": material_profile.materiaalsoort,
            "structuur": material_profile.structuur,
            "status": material_profile.status,
        }

    # ── Validatie van de boundary-output ──────────────────────────────────────
    @classmethod
    def _filter_geldig(cls, voorstellen) -> tuple[list, list[str]]:
        """Scheidt geldige patroonvoorstellen van afgekeurde. Een voorstel is
        geldig wanneer het structureel volledig is (verplichte patroonvelden +
        motivering) en niet expliciet aangeeft het Concept te verlaten. De
        semantische toets "aantoonbaar aansluitend" ligt bij de model-specifieke
        boundary; deze laag borgt de structurele geldigheid en de expliciete
        grens, en wijst ongeldige voorstellen af."""
        geldig: list = []
        afgekeurd: list[str] = []
        if not isinstance(voorstellen, list):
            return [], ["Reasoning boundary gaf geen lijst voorstellen terug."]
        for i, v in enumerate(voorstellen):
            if not isinstance(v, dict):
                afgekeurd.append(f"Voorstel {i} is geen geldig object.")
                continue
            ontbreekt = [
                veld for veld in cls._VERPLICHTE_PATROON_VELDEN
                if not (isinstance(v.get(veld), str) and v.get(veld).strip())
            ]
            if ontbreekt:
                afgekeurd.append(f"Voorstel {i} mist verplichte velden: {', '.join(ontbreekt)}.")
                continue
            motivering = v.get("motivering")
            if not (isinstance(motivering, str) and motivering.strip()):
                afgekeurd.append(f"Voorstel {i} mist een motivering.")
                continue
            if v.get("verlaat_concept") is True:
                afgekeurd.append(f"Voorstel {i} verlaat het bevestigde Concept.")
                continue
            geldig.append(v)
        return geldig, afgekeurd

    # ── Pattern Profile-object bouwen (buiten de DesignContext) ───────────────
    @staticmethod
    def _bouw_pattern_profile(
        voorstel: dict, concept_herkomst: dict, fd_herkomst: dict, mp_herkomst: dict, poging: int
    ) -> PatternProfile:
        return PatternProfile(
            identifier=str(uuid.uuid4()),
            motiefstructuur=voorstel.get("motiefstructuur"),
            motiefschaal=voorstel.get("motiefschaal"),
            dichtheid=voorstel.get("dichtheid"),
            herhalingskarakter=voorstel.get("herhalingskarakter"),
            motivering=voorstel["motivering"],
            concept_herkomst=concept_herkomst,
            floor_design_herkomst=fd_herkomst,
            material_profile_herkomst=mp_herkomst,
            status="Voorgesteld",
            kwaliteitsinformatie={"binnen_concept": True, "poging": poging},
        )
