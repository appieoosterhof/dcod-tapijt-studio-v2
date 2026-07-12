"""
BUILD-012 -- Material Planner.

Implementeert de Material Planner conform de goedgekeurde ontwerpbaseline
(BUILD-012 functioneel + technisch/TD-002 en het amendement AB-010A). De
Material Planner is de eerste downstream-component ná de Reasoning Engine: hij
vormt uitsluitend materiaalvoorstellen (= Material Profiles met status
"Voorgesteld") op basis van het BEVESTIGDE Floor Design en het bevestigde
Concept. Hij STELT VOOR, bevestigt nooit.

Kernprincipes (technisch geborgd, conform AB-010/AB-010A):
  * de component stelt voor, bevestigt nooit;
  * AI-model-onafhankelijk: de redeneerstap loopt via een injecteerbare
    boundary die DesignContext noch registratie kent; geen LLM, geen prompt;
  * het Material Profile is een zelfstandig resultaat-object BUITEN de
    DesignContext; de DesignContext en het Floor Design worden uitsluitend
    gelezen;
  * deterministische preconditie: start uitsluitend bij een bevestigd Floor
    Design (FloorDesign.status == "Bevestigd") en een bevestigd Concept
    (Concept.status == "bevestigd").

Volledig additief en losstaand: GEEN wijziging aan design_context.py of
reasoning_engine.py; geen koppeling aan de live pipeline. Nog NIET
geimplementeerd: Floor Visualization Engine, Design Transfer Package, de
overige planners en persistentie.
"""

from __future__ import annotations

import copy
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

from design_context import Concept, DesignContext
from reasoning_engine import FloorDesign


# ─── Material Reasoning Boundary (AI-model-onafhankelijk) ────────────────────
#
# Contract: een functie die een platte invoer-dict ontvangt (bevestigd Concept
# + projectie van het bevestigde Floor Design) en een lijst materiaalvoorstellen
# retourneert, elk met de materiaaleigenschappen en een "motivering". Zij kent
# DesignContext noch registratie -- puur voorstel in, voorstel uit.

MateriaalRedeneerFunctie = Callable[[dict], list]


def placeholder_materiaal_generatie(invoer: dict) -> list:
    """Deterministische placeholder voor de Material Reasoning Boundary.

    Geen LLM-aanroep, geen promptteksten. Leidt uit het bevestigde Concept en
    de ontwerprichting van het bevestigde Floor Design een of meer
    materiaalvoorstellen af, zodat de keten preconditie -> boundary ->
    validatie -> regeneratie testbaar is zonder AI.
    """
    stijl = invoer.get("stijlfamilie") or "de gekozen stijl"
    richting = invoer.get("ontwerprichting") or "de gekozen ontwerprichting"
    return [
        {
            "materiaalsoort": "wol",
            "structuur": "getuft, dicht",
            "pooltype": "laagpolig",
            "tactiliteit": "zacht, warm",
            "uitstraling": f"ingetogen, passend bij {stijl}",
            "motivering": f"Warme, rustige materialisatie voor {richting} ({stijl}).",
        },
        {
            "materiaalsoort": "wol-mix",
            "structuur": "geweven, strak",
            "pooltype": "vlak",
            "tactiliteit": "stevig",
            "uitstraling": f"contrastrijker alternatief bij {stijl}",
            "motivering": f"Strakker alternatief voor {richting}, zelfde Concept.",
        },
    ]


@dataclass
class MaterialProfile:
    """Technisch datamodel van een voorgesteld Material Profile -- BUITEN de
    DesignContext (AB-010). Draagt de motivering in het object zelf en een
    enkelvoudige herkomst-referentie naar het bevestigde Concept en het
    bevestigde Floor Design (traceerbaarheid)."""

    identifier: str
    materiaalsoort: Optional[str]
    structuur: Optional[str]
    pooltype: Optional[str]
    tactiliteit: Optional[str]
    uitstraling: Optional[str]
    motivering: str
    concept_herkomst: dict
    floor_design_herkomst: dict
    status: str = "Voorgesteld"
    kwaliteitsinformatie: dict = field(default_factory=dict)


@dataclass
class MaterialProfileResultaat:
    """Technische returnvorm: één of meer voorgestelde Material Profiles, of
    uitsluitend signaleringen wanneer de Material Planner niet mag of kan
    slagen."""

    material_profiles: list = field(default_factory=list)
    signaleringen: list[str] = field(default_factory=list)
    kwaliteitsinformatie: dict = field(default_factory=dict)

    @property
    def geslaagd(self) -> bool:
        return len(self.material_profiles) > 0


class MaterialPlanner:
    """Publieke component (BUILD-012).

    `stel_material_profiles_voor(dc, floor_design)` leidt uit het bevestigde
    Concept (laag 4) en het bevestigde Floor Design één of meer voorgestelde
    Material Profiles af (buiten de DesignContext, met motivering en enkelvoudige
    herkomst). De component leest de DesignContext en het Floor Design
    uitsluitend; hij wijzigt niets en bevestigt nooit.
    """

    STATUS_CONCEPT_BEVESTIGD = "bevestigd"      # laag 4 (Concept)
    STATUS_FLOOR_DESIGN_BEVESTIGD = "Bevestigd"  # Floor Design (AB-006)
    STATUS_VOORGESTELD = "Voorgesteld"           # Material Profile
    _VERPLICHTE_CONCEPT_VELDEN = ("stijlfamilie", "kleurpalet", "complexiteit", "motiefschaal")
    _VERPLICHTE_MATERIAAL_VELDEN = ("materiaalsoort", "structuur", "pooltype")
    MAX_REGENERATIE_POGINGEN = 3

    def __init__(self, materiaal_generatie: MateriaalRedeneerFunctie = placeholder_materiaal_generatie) -> None:
        # De Material Reasoning Boundary is injecteerbaar; standaard de placeholder.
        self._materiaal_generatie = materiaal_generatie

    # ── Orkestratie ───────────────────────────────────────────────────────────
    def stel_material_profiles_voor(
        self, dc: DesignContext, floor_design: FloorDesign
    ) -> MaterialProfileResultaat:
        """Orkestreert de verwerkingsketen: preconditie -> boundary ->
        validatie -> (gelimiteerde) regeneratie -> verpakken. Leest de
        DesignContext en het Floor Design uitsluitend."""
        # 1. Deterministische preconditie (bevestigd Concept + bevestigd Floor Design).
        signaleringen = self._valideer_preconditie(dc, floor_design)
        if signaleringen:
            return MaterialProfileResultaat(signaleringen=signaleringen)

        invoer = self._verzamel_invoer(dc, floor_design)
        concept_herkomst = self._concept_snapshot(dc.concept)
        fd_herkomst = self._floor_design_snapshot(floor_design)
        laatste_afkeur: list[str] = []

        # 2-4. Boundary + validatie, met gelimiteerde regeneratie.
        for poging in range(1, self.MAX_REGENERATIE_POGINGEN + 1):
            try:
                voorstellen = self._materiaal_generatie(invoer)
            except Exception as fout:  # boundary is injecteerbaar en onbekend
                return MaterialProfileResultaat(
                    signaleringen=[f"Technische fout in de reasoning boundary: {fout}"]
                )

            geldig, laatste_afkeur = self._filter_geldig(voorstellen)
            if geldig:
                profielen = [
                    self._bouw_material_profile(v, concept_herkomst, fd_herkomst, poging)
                    for v in geldig
                ]
                return MaterialProfileResultaat(
                    material_profiles=profielen,
                    kwaliteitsinformatie={
                        "pogingen": poging,
                        "aantal": len(profielen),
                        "afgekeurd": len(laatste_afkeur),
                    },
                )

        # 5. Regeneratielimiet bereikt -> geen geldig resultaat, geen mutatie.
        return MaterialProfileResultaat(
            signaleringen=(
                [
                    f"Geen geldig materiaalvoorstel na "
                    f"{self.MAX_REGENERATIE_POGINGEN} pogingen."
                ]
                + laatste_afkeur
            ),
            kwaliteitsinformatie={"pogingen": self.MAX_REGENERATIE_POGINGEN},
        )

    # ── Preconditie (deterministische gate) ───────────────────────────────────
    def _valideer_preconditie(self, dc: DesignContext, floor_design: FloorDesign) -> list[str]:
        signaleringen: list[str] = []

        if dc.concept.status != self.STATUS_CONCEPT_BEVESTIGD:
            signaleringen.append(
                'Concept is niet bevestigd; Material Planner start niet '
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
                'Floor Design is niet bevestigd; Material Planner start niet '
                '(vereist FloorDesign.status == "Bevestigd").'
            )
        elif not (floor_design.ontwerprichting and floor_design.identifier):
            signaleringen.append("Bevestigd Floor Design is niet identificeerbaar.")

        return signaleringen

    # ── Invoer voor de boundary ───────────────────────────────────────────────
    @staticmethod
    def _verzamel_invoer(dc: DesignContext, floor_design: FloorDesign) -> dict:
        c = dc.concept
        return {
            "stijlfamilie": c.stijlfamilie,
            "kleurpalet": c.kleurpalet,
            "complexiteit": c.complexiteit,
            "motiefschaal": c.motiefschaal,
            "ontwerprichting": floor_design.ontwerprichting,
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

    # ── Validatie van de boundary-output ──────────────────────────────────────
    @classmethod
    def _filter_geldig(cls, voorstellen) -> tuple[list, list[str]]:
        """Scheidt geldige materiaalvoorstellen van afgekeurde. Een voorstel is
        geldig wanneer het structureel volledig is (verplichte materiaalvelden +
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
                veld for veld in cls._VERPLICHTE_MATERIAAL_VELDEN
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

    # ── Material Profile-object bouwen (buiten de DesignContext) ──────────────
    @staticmethod
    def _bouw_material_profile(
        voorstel: dict, concept_herkomst: dict, fd_herkomst: dict, poging: int
    ) -> MaterialProfile:
        return MaterialProfile(
            identifier=str(uuid.uuid4()),
            materiaalsoort=voorstel.get("materiaalsoort"),
            structuur=voorstel.get("structuur"),
            pooltype=voorstel.get("pooltype"),
            tactiliteit=voorstel.get("tactiliteit"),
            uitstraling=voorstel.get("uitstraling"),
            motivering=voorstel["motivering"],
            concept_herkomst=concept_herkomst,
            floor_design_herkomst=fd_herkomst,
            status="Voorgesteld",
            kwaliteitsinformatie={"binnen_concept": True, "poging": poging},
        )
