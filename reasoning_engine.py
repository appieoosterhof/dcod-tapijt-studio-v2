"""
BUILD-010 -- Reasoning Engine (Fase 1: Conceptvorming; Fase 2: Floor Design-generatie).

Implementeert de Reasoning Engine conform de goedgekeurde ontwerpbaseline
(BUILD-010 functioneel + technisch/TD-001, en BUILD-011 voor Fase 2). Deze
module realiseert:

  * de interne module-structuur van de Reasoning Engine;
  * Fase 1 -- Conceptvorming (IMP-001);
  * Fase 2 -- Floor Design-generatie (IMP-002, conform BUILD-011).

De planners (Material/Pattern/SVG), materiaal-/patroonkeuze, SVG-generatie,
visualisatie, export en persistentie zijn hier NIET geimplementeerd (zie de
downstream-componenten).

Kernprincipes (technisch geborgd, conform AB-008/AB-001/DESIGN_BRAIN):
  * de component STELT VOOR, bevestigt nooit;
  * AI-model-onafhankelijk: de redeneerstap loopt via een injecteerbare
    boundary (BUILD-009-patroon) die DesignContext noch registratie kent en
    uitsluitend een voorstel retourneert; geen LLM-aanroep, geen promptteksten;
  * volledig additief en losstaand: GEEN wijziging aan design_context.py, geen
    koppeling aan de live pipeline.

Fase-gate (TD-001, deterministisch):
  * na Fase 1 schrijft deze component uitsluitend Concept.status = "voorgesteld";
  * de waarde "bevestigd" wordt uitsluitend door de architect toegekend --
    deze component leest die status alleen en bevestigt nooit;
  * Fase 2 mag uitsluitend starten wanneer Concept.status == "bevestigd".
"""

from __future__ import annotations

import copy
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

from design_context import Concept, DesignContext


# ─── Reasoning boundary (AI-model-onafhankelijk) ────────────────────────────
#
# Contract: een functie die een platte invoer-dict ontvangt en een voorstel-
# dict teruggeeft. Zij kent DesignContext noch registratie -- puur voorstel in,
# voorstel uit. Verplichte sleutels in de output: de laag-4-velden; optioneel
# "motivering" (het "waarom", dat -- conform TD-001 -- uitsluitend in de
# Ontwerpredenering wordt vastgelegd, nooit in het Concept-datamodel).

RedeneerFunctie = Callable[[dict], dict]


def placeholder_conceptvorming(invoer: dict) -> dict:
    """Deterministische placeholder voor de Fase 1-reasoning boundary.

    Bevat geen LLM-aanroep en geen promptteksten. Stelt op basis van de
    meegegeven visie-/context-/strategievelden een volledig Concept-voorstel
    samen, zodat de keten validatie -> boundary -> kwaliteitsborging ->
    registratie testbaar is zonder AI. Een echte, model-specifieke redenering
    kan later worden geinjecteerd zonder deze component te wijzigen.
    """
    sfeer = invoer.get("sfeer") or "neutraal"
    aanpak = invoer.get("aanpak") or "de vastgelegde ontwerpstrategie"
    return {
        "stijlfamilie": f"stijl afgeleid van {sfeer}",
        "kleurpalet": {"achtergrond": "#f5f5f0", "primary": "#8a8a7a"},
        "complexiteit": "medium",
        "motiefschaal": "medium",
        "motivering": (
            f"Concept voorgesteld binnen {aanpak}, afgestemd op de beleving "
            f"'{sfeer}' (placeholder-redenering)."
        ),
    }


@dataclass
class ConceptResultaat:
    """Technische returnvorm (geen architectuurobject): een voorgesteld Concept,
    of uitsluitend signaleringen wanneer Fase 1 niet mag of kan slagen.
    `kwaliteitsinformatie` bevat de technische kwaliteitsindicatoren."""

    concept: Optional[Concept] = None
    signaleringen: list[str] = field(default_factory=list)
    kwaliteitsinformatie: dict = field(default_factory=dict)

    @property
    def geslaagd(self) -> bool:
        return self.concept is not None


# ─── Fase 2: Floor Design-generatie (BUILD-011) ─────────────────────────────
#
# Floor Designs staan volledig BUITEN de DesignContext. De Floor Design
# reasoning boundary kent DesignContext noch registratie; zij ontvangt een
# platte invoer (het bevestigde Concept + onderbouwende context) en retourneert
# een lijst voorstel-dicts, elk met "ontwerprichting" en "motivering".

FloorDesignRedeneerFunctie = Callable[[dict], list]


def placeholder_floor_design_generatie(invoer: dict) -> list:
    """Deterministische placeholder voor de Fase 2-reasoning boundary.

    Geen LLM-aanroep, geen promptteksten. Leidt uit het bevestigde Concept een
    of meer ontwerprichtingen af, zodat de keten preconditie -> boundary ->
    binnen-Concept-validatie -> regeneratie testbaar is zonder AI.
    """
    stijl = invoer.get("stijlfamilie") or "de gekozen stijl"
    complexiteit = invoer.get("complexiteit") or "medium"
    return [
        {
            "ontwerprichting": f"{stijl}, ingetogen uitgewerkt ({complexiteit})",
            "motivering": f"Directe, rustige uitwerking van het bevestigde Concept ({stijl}).",
        },
        {
            "ontwerprichting": f"{stijl}, expressief uitgewerkt ({complexiteit})",
            "motivering": f"Zelfde Concept ({stijl}), met meer contrast als alternatieve richting.",
        },
    ]


@dataclass
class FloorDesign:
    """Technisch datamodel van een voorgesteld Floor Design -- BUITEN de
    DesignContext (BUILD-011/AB-006). Draagt de motivering in het object zelf en
    een herkomst-referentie naar het bevestigde Concept (traceerbaarheid)."""

    identifier: str
    ontwerprichting: str
    concept_herkomst: dict
    motivering: str
    status: str = "Voorgesteld"
    kwaliteitsinformatie: dict = field(default_factory=dict)


@dataclass
class FloorDesignResultaat:
    """Technische returnvorm: één of meer Floor Designs, of uitsluitend
    signaleringen wanneer Fase 2 niet mag of kan slagen."""

    floor_designs: list = field(default_factory=list)
    signaleringen: list[str] = field(default_factory=list)
    kwaliteitsinformatie: dict = field(default_factory=dict)

    @property
    def geslaagd(self) -> bool:
        return len(self.floor_designs) > 0


class ReasoningEngine:
    """Publieke component (BUILD-010).

    Fase 1 -- `vorm_concept(dc)` -- leidt uit de bevestigde Ontwerpvisie (laag 1),
    de vastgelegde Project-/Ruimtecontext (laag 2) en de Ontwerpstrategie
    (laag 3) een voorgesteld Concept (laag 4) af, schrijft dit met status
    "voorgesteld" weg en registreert het "waarom" in de Ontwerpredenering.
    De component bevestigt nooit en muteert laag 1-3 niet.

    Fase 2 -- `genereer_floor_designs(dc)` -- genereert, uitsluitend bij een
    bevestigd Concept, één of meer Floor Designs BUITEN de DesignContext
    (BUILD-011); het Concept wordt gelezen, nooit gewijzigd of bevestigd.
    """

    STATUS_VOORGESTELD = "voorgesteld"
    STATUS_BEVESTIGD = "bevestigd"
    _VERPLICHTE_CONCEPT_VELDEN = ("stijlfamilie", "kleurpalet", "complexiteit", "motiefschaal")
    MAX_REGENERATIE_POGINGEN = 3

    def __init__(
        self,
        conceptvorming: RedeneerFunctie = placeholder_conceptvorming,
        floor_design_generatie: FloorDesignRedeneerFunctie = placeholder_floor_design_generatie,
    ) -> None:
        # Beide reasoning boundaries zijn injecteerbaar; standaard de placeholders.
        self._conceptvorming = conceptvorming
        self._floor_design_generatie = floor_design_generatie

    # ── Fase 1: Conceptvorming (orkestratie) ──────────────────────────────────
    def vorm_concept(self, dc: DesignContext) -> ConceptResultaat:
        """Orkestreert Fase 1: validatie -> boundary -> kwaliteitsborging ->
        registratie. Muteert laag 1-3 nooit; bevestigt nooit."""
        # 1. Preconditie-validatie (incl. overwrite-guard op een bevestigd Concept)
        signaleringen = self._valideer_input(dc)
        if signaleringen:
            return ConceptResultaat(signaleringen=signaleringen)

        # 2. Reasoning boundary -- uitsluitend de noodzakelijke invoer.
        #    Een technische fout mag nooit een partieel Concept wegschrijven.
        try:
            voorstel = self._conceptvorming(self._verzamel_invoer(dc))
        except Exception as fout:  # boundary is injecteerbaar en onbekend
            return ConceptResultaat(
                signaleringen=[f"Technische fout in de reasoning boundary: {fout}"]
            )

        # 2b. Validatie van de boundary-output vóór registratie.
        voorstel_signaleringen = self._valideer_voorstel(voorstel)
        if voorstel_signaleringen:
            return ConceptResultaat(signaleringen=voorstel_signaleringen)

        # 3. Kwaliteitsborging (o.a. binnen de strategie-bandbreedte).
        kwaliteits_signaleringen, kwaliteitsinformatie = self._kwaliteitsborging(dc, voorstel)
        if kwaliteits_signaleringen:
            return ConceptResultaat(
                signaleringen=kwaliteits_signaleringen,
                kwaliteitsinformatie=kwaliteitsinformatie,
            )

        # 4. Registratie -- voorgesteld Concept wegschrijven, nooit bevestigen.
        vorig_bestond = bool(dc.concept.stijlfamilie or dc.concept.status)
        concept = Concept(
            stijlfamilie=voorstel.get("stijlfamilie"),
            kleurpalet=voorstel.get("kleurpalet"),
            complexiteit=voorstel.get("complexiteit"),
            motiefschaal=voorstel.get("motiefschaal"),
            status=self.STATUS_VOORGESTELD,
        )
        dc.concept = concept
        # Traceerbaarheid: het "waarom" van het Concept uitsluitend in de
        # Ontwerpredenering (Concept-datamodel blijft ongewijzigd).
        dc.ontwerpredenering.voeg_beslissing_toe(
            laag="concept",
            reden=voorstel.get("motivering") or "voorgesteld Concept",
            vervangt="vorig voorgesteld Concept" if vorig_bestond else None,
        )
        return ConceptResultaat(concept=concept, kwaliteitsinformatie=kwaliteitsinformatie)

    # ── Preconditie-validatie ─────────────────────────────────────────────────
    def _valideer_input(self, dc: DesignContext) -> list[str]:
        signaleringen: list[str] = []

        ov = dc.ontwerpvisie
        if not ov.bevestigd_door_architect:
            signaleringen.append("Ontwerpvisie is nog niet bevestigd.")
        if not (ov.vrije_tekst or ov.voorgestelde_interpretatie or ov.sfeer):
            signaleringen.append("Ontwerpvisie bevat onvoldoende inhoud.")

        pc = dc.projectcontext
        if not (pc.projecttype or pc.ruimtetype or pc.gebruikscontext):
            signaleringen.append("Project-/Ruimtecontext is onvoldoende vastgelegd.")

        if not dc.ontwerpstrategie.aanpak:
            signaleringen.append("Ontwerpstrategie ontbreekt.")

        # Overwrite-guard: een reeds bevestigd Concept wordt niet overschreven.
        if dc.concept.status == self.STATUS_BEVESTIGD:
            signaleringen.append(
                "Concept is reeds bevestigd en wordt niet opnieuw voorgesteld."
            )

        return signaleringen

    # ── Invoer voor de reasoning boundary ─────────────────────────────────────
    @staticmethod
    def _verzamel_invoer(dc: DesignContext) -> dict:
        """Verzamelt uitsluitend de velden die de boundary nodig heeft: visie
        (laag 1), context (laag 2) en strategie (laag 3). Platte waarden -- geen
        DesignContext, geen dataclasses -- zodat de boundary ontkoppeld blijft."""
        ov = dc.ontwerpvisie
        pc = dc.projectcontext
        st = dc.ontwerpstrategie
        return {
            "vrije_tekst": ov.vrije_tekst,
            "sfeer": ov.sfeer,
            "gewenste_identiteit": ov.gewenste_identiteit,
            "ontwerpambitie": ov.ontwerpambitie,
            "projecttype": pc.projecttype,
            "ruimtetype": pc.ruimtetype,
            "doelgroep": pc.doelgroep,
            "gebruikscontext": pc.gebruikscontext,
            "aanpak": st.aanpak,
            "onderbouwing": st.onderbouwing,
        }

    # ── Validatie van de boundary-output ──────────────────────────────────────
    @classmethod
    def _valideer_voorstel(cls, voorstel: dict) -> list[str]:
        """Controleert dat de boundary een volledig Concept-voorstel gaf."""
        if not isinstance(voorstel, dict):
            return ["Reasoning boundary gaf geen geldig voorstel terug."]
        signaleringen: list[str] = []
        for veld in cls._VERPLICHTE_CONCEPT_VELDEN:
            waarde = voorstel.get(veld)
            if waarde is None or (isinstance(waarde, str) and not waarde.strip()):
                signaleringen.append(f"Concept-voorstel mist verplicht veld: {veld}.")
        return signaleringen

    # ── Kwaliteitsborging ─────────────────────────────────────────────────────
    def _kwaliteitsborging(self, dc: DesignContext, voorstel: dict) -> tuple[list[str], dict]:
        """Technische kwaliteitscontrole van het Concept-voorstel.

        Op infrastructuurniveau (zonder AI) wordt structureel geborgd dat het
        voorstel volledig is en dat een ontwerpstrategie als kader aanwezig is;
        de kwaliteitsinformatie wordt teruggegeven. De semantische toets
        "aantoonbaar binnen de strategie-bandbreedte" (TD-001 §4) vereist de
        model-specifieke boundary en wordt daaraan overgelaten -- deze laag
        levert er de haak voor, zonder zelf inhoudelijk te oordelen.
        """
        strategie_aanwezig = bool(dc.ontwerpstrategie.aanpak)
        kwaliteitsinformatie = {
            "volledig": True,  # reeds gevalideerd in _valideer_voorstel
            "strategie_aanwezig": strategie_aanwezig,
            "binnen_strategie": strategie_aanwezig,
        }
        signaleringen: list[str] = []
        if not strategie_aanwezig:
            signaleringen.append(
                "Geen ontwerpstrategie aanwezig om het Concept aan te toetsen."
            )
        return signaleringen, kwaliteitsinformatie

    # ── Fase 2: Floor Design-generatie (orkestratie, BUILD-011) ───────────────
    def genereer_floor_designs(self, dc: DesignContext) -> FloorDesignResultaat:
        """Orkestreert Fase 2: preconditie -> boundary -> binnen-Concept-validatie
        -> (gelimiteerde) regeneratie -> verpakken.

        Leest de DesignContext uitsluitend; Floor Designs staan BUITEN de
        DesignContext. Wijzigt het Concept nooit en bevestigt nooit.
        """
        # 1. Preconditie: uitsluitend starten bij een bevestigd, volledig Concept.
        signaleringen = self._valideer_concept_bevestigd(dc)
        if signaleringen:
            return FloorDesignResultaat(signaleringen=signaleringen)

        invoer = self._verzamel_concept_invoer(dc)
        herkomst = self._concept_snapshot(dc.concept)
        laatste_afkeur: list[str] = []

        # 2-4. Boundary + binnen-Concept-validatie, met gelimiteerde regeneratie
        #      (TD-001 §5: afgekeurde Floor Designs -> uitsluitend Fase 2 opnieuw;
        #      het bevestigde Concept blijft ongewijzigd behouden).
        for poging in range(1, self.MAX_REGENERATIE_POGINGEN + 1):
            try:
                voorstellen = self._floor_design_generatie(invoer)
            except Exception as fout:  # boundary is injecteerbaar en onbekend
                return FloorDesignResultaat(
                    signaleringen=[f"Technische fout in de reasoning boundary: {fout}"]
                )

            geldig, laatste_afkeur = self._filter_binnen_concept(voorstellen)
            if geldig:
                floor_designs = [
                    self._bouw_floor_design(v, herkomst, poging) for v in geldig
                ]
                return FloorDesignResultaat(
                    floor_designs=floor_designs,
                    kwaliteitsinformatie={
                        "pogingen": poging,
                        "aantal": len(floor_designs),
                        "afgekeurd": len(laatste_afkeur),
                    },
                )

        # 5. Regeneratielimiet bereikt -> geen geldig resultaat, geen mutatie.
        return FloorDesignResultaat(
            signaleringen=(
                [
                    f"Geen Floor Design bleef binnen het bevestigde Concept na "
                    f"{self.MAX_REGENERATIE_POGINGEN} pogingen."
                ]
                + laatste_afkeur
            ),
            kwaliteitsinformatie={"pogingen": self.MAX_REGENERATIE_POGINGEN},
        )

    # ── Fase 2: preconditie (deterministische statusgate) ─────────────────────
    def _valideer_concept_bevestigd(self, dc: DesignContext) -> list[str]:
        signaleringen: list[str] = []
        if dc.concept.status != self.STATUS_BEVESTIGD:
            signaleringen.append(
                'Concept is niet bevestigd; Fase 2 start niet '
                '(vereist Concept.status == "bevestigd").'
            )
            return signaleringen  # zonder bevestigd Concept geen verdere controles
        for veld in self._VERPLICHTE_CONCEPT_VELDEN:
            waarde = getattr(dc.concept, veld)
            if waarde is None or (isinstance(waarde, str) and not waarde.strip()):
                signaleringen.append(f"Bevestigd Concept mist verplicht veld: {veld}.")
        return signaleringen

    # ── Fase 2: invoer voor de boundary ───────────────────────────────────────
    @staticmethod
    def _verzamel_concept_invoer(dc: DesignContext) -> dict:
        c = dc.concept
        ov = dc.ontwerpvisie
        pc = dc.projectcontext
        return {
            "stijlfamilie": c.stijlfamilie,
            "kleurpalet": c.kleurpalet,
            "complexiteit": c.complexiteit,
            "motiefschaal": c.motiefschaal,
            "sfeer": ov.sfeer,
            "projecttype": pc.projecttype,
            "ruimtetype": pc.ruimtetype,
        }

    # ── Fase 2: herkomst-referentie (traceerbaarheid Concept -> Floor Design) ──
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

    # ── Fase 2: binnen-Concept-validatie ──────────────────────────────────────
    @staticmethod
    def _filter_binnen_concept(voorstellen) -> tuple[list, list[str]]:
        """Scheidt geldige voorstellen van afgekeurde. Een voorstel is geldig
        wanneer het structureel volledig is (ontwerprichting + motivering) en
        niet expliciet aangeeft het Concept te verlaten (`verlaat_concept`). De
        semantische toets "aantoonbaar binnen" wordt door de model-specifieke
        boundary geleverd; deze laag borgt de structurele geldigheid en de
        expliciete grens, en wijst ongeldige voorstellen af."""
        geldig: list = []
        afgekeurd: list[str] = []
        if not isinstance(voorstellen, list):
            return [], ["Reasoning boundary gaf geen lijst voorstellen terug."]
        for i, v in enumerate(voorstellen):
            if not isinstance(v, dict):
                afgekeurd.append(f"Voorstel {i} is geen geldig object.")
                continue
            ontwerprichting = v.get("ontwerprichting")
            motivering = v.get("motivering")
            if not (isinstance(ontwerprichting, str) and ontwerprichting.strip()):
                afgekeurd.append(f"Voorstel {i} mist een ontwerprichting.")
                continue
            if not (isinstance(motivering, str) and motivering.strip()):
                afgekeurd.append(f"Voorstel {i} mist een motivering.")
                continue
            if v.get("verlaat_concept") is True:
                afgekeurd.append(f"Voorstel {i} verlaat het bevestigde Concept.")
                continue
            geldig.append(v)
        return geldig, afgekeurd

    # ── Fase 2: Floor Design-object bouwen (buiten de DesignContext) ──────────
    @staticmethod
    def _bouw_floor_design(voorstel: dict, herkomst: dict, poging: int) -> FloorDesign:
        return FloorDesign(
            identifier=str(uuid.uuid4()),
            ontwerprichting=voorstel["ontwerprichting"],
            concept_herkomst=herkomst,
            motivering=voorstel["motivering"],
            status="Voorgesteld",
            kwaliteitsinformatie={"binnen_concept": True, "poging": poging},
        )
