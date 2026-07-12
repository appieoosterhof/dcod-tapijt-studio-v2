"""
BUILD-017 -- Conversation Planner.

Implementeert de Conversation Planner conform de goedgekeurde ontwerpbaseline
(BUILD-017 functioneel + technisch/TD-007). De Conversation Planner is de
conversationele voorkant van de Design Brain: hij bouwt samen met de gebruiker
de OntwerpVisie (DesignContext laag 1) op tot de architect haar kan bevestigen.
Hij ORKESTREERT uitsluitend -- hij interpreteert niet zelf en bevestigt nooit.

Kernprincipes (technisch geborgd, conform TD-007):
  * uitsluitend op laag 1 schrijvende orchestrator; interpreteert niet zelf en
    voegt geen ontwerpintelligentie toe;
  * de eigen beslislogica (welke vervolgstap) is DETERMINISTISCH gegeven de
    DesignContext-stand; het AI-model zit uitsluitend achter de injecteerbare
    interpretatie-grens (de bestaande Context Interpreter, BUILD-004);
  * schrijft `OntwerpVisie.vrije_tekst` verbatim uit de ruwe gebruikersinvoer
    (geen interpretatie) en projecteert uitsluitend de laag-1-interpretaties via
    de bestaande `pas_interpretaties_toe` (ongewijzigd hergebruikt);
  * zet NOOIT `bevestigd_door_architect` (exclusief de architect);
  * wordt volledig READ-ONLY zodra de OntwerpVisie is bevestigd (write-gate);
  * start GEEN downstream-component; levert uitsluitend de bevestigde
    OntwerpVisie op.

Volledig additief en losstaand: GEEN wijziging aan design_context.py,
context_interpreter.py, de downstream-componenten of de bestaande pipeline. De
component is AI-model-onafhankelijk: hij importeert zelf geen AI-model; de
interpretatie-grens wordt geinjecteerd (in productie de Context Interpreter,
hier een deterministische placeholder).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

from design_context import DesignContext, Interpretatie
from context_interpreter import pas_interpretaties_toe


# ─── Interpretatie-grens (injecteerbaar, AI-model-onafhankelijk) ──────────────
#
# Contract: een functie die ruwe gebruikersinvoer (str) ontvangt en een lijst
# `Interpretatie` retourneert. Bevat GEEN projectie-/beslislogica -- puur tekst
# in, interpretaties uit. In productie wordt de bestaande Context Interpreter
# geinjecteerd (bijv. `lambda t: interpreteer_context(t, api_key=...)`,
# BUILD-004); hier een deterministische placeholder die NIETS interpreteert.

InterpreteerFunctie = Callable[[str], list[Interpretatie]]


def placeholder_interpretatie(vrije_tekst: str) -> list[Interpretatie]:
    """Deterministische placeholder voor de interpretatie-grens.

    Interpreteert bewust NIETS (geen LLM, geen betekenisafleiding): retourneert
    een lege lijst. De echte interpretatie hoort in de geinjecteerde Context
    Interpreter (BUILD-004). Zo blijft de Conversation Planner zelf
    AI-model-onafhankelijk en deterministisch.
    """
    return []


@dataclass
class Vervolgstap:
    """De door de planner gekozen conversationele vervolgstap -- een structuur
    BINNEN de Conversation Planner-module (BUILD-005 §8), geen DesignContext-laag
    en zonder eigen status."""

    type: str      # ConversationPlanner.TYPE_VRAAG | TYPE_SAMENVATTING
    inhoud: str


@dataclass
class ConversationPlannerResultaat:
    """Technische returnvorm: de (in-place bijgewerkte) DesignContext plus de
    gekozen vervolgstap, of uitsluitend signaleringen bij een fout."""

    design_context: Optional[DesignContext] = None
    vervolgstap: Optional[Vervolgstap] = None
    signaleringen: list[str] = field(default_factory=list)
    kwaliteitsinformatie: dict = field(default_factory=dict)

    @property
    def geslaagd(self) -> bool:
        return not self.signaleringen


class ConversationPlanner:
    """Publieke component (BUILD-017) -- uitsluitend orchestrerende voorkant.

    `verwerk(dc, gebruikersinvoer, ...)` bouwt, zolang de OntwerpVisie onbevestigd
    is, laag 1 op (verbatim `vrije_tekst` + projectie van de laag-1-interpretaties)
    en kiest deterministisch precies één vervolgstap. Leest alle overige stand
    uitsluitend; schrijft nooit een andere laag, bevestigt nooit, en start geen
    downstream. Na bevestiging is laag 1 read-only.
    """

    TYPE_VRAAG = "vraag"
    TYPE_SAMENVATTING = "samenvatting_ter_bevestiging"
    LAAG_ONTWERPVISIE = "ontwerpvisie"
    _VISIE_INHOUD_VELDEN = ("sfeer", "gewenste_identiteit", "ontwerpambitie")
    MAX_INTERPRETATIE_POGINGEN = 3

    def __init__(self, interpreteer: InterpreteerFunctie = placeholder_interpretatie) -> None:
        # De interpretatie-grens is injecteerbaar; standaard de placeholder.
        self._interpreteer = interpreteer

    # ── Orkestratie ───────────────────────────────────────────────────────────
    def verwerk(
        self,
        dc: DesignContext,
        gebruikersinvoer: str = "",
        gespreksgeschiedenis: Optional[list] = None,
        projectfase: Optional[str] = None,
    ) -> ConversationPlannerResultaat:
        """Orkestreert één gespreksbeurt: write-gate -> ruwe wens -> interpretatie
        (gedelegeerd) -> projectie (laag 1) -> vervolgstapkeuze. Leest alle overige
        stand uitsluitend."""
        # 1. Write-gate: read-only zodra de architect heeft bevestigd. Geen enkele
        #    schrijfactie; de bevestigde OntwerpVisie is dan de levering.
        if dc.ontwerpvisie.bevestigd_door_architect:
            return ConversationPlannerResultaat(
                design_context=dc,
                vervolgstap=None,
                kwaliteitsinformatie={
                    "bevestigd": True,
                    "read_only": True,
                    "levering": "bevestigde OntwerpVisie",
                },
            )

        # 2. Ruwe wens verbatim vastleggen (laag 1, geen interpretatie).
        if gebruikersinvoer and gebruikersinvoer.strip():
            dc.ontwerpvisie.vrije_tekst = gebruikersinvoer

            # 3. Interpretatie (gedelegeerd, injecteerbaar, met gelimiteerde herhaling).
            interpretaties, signaleringen = self._interpreteer_met_herhaling(gebruikersinvoer)
            if signaleringen:
                # Geen partiële projectie; laag 1 behoudt de reeds verbatim
                # vastgelegde wens, verder ongewijzigd.
                return ConversationPlannerResultaat(
                    design_context=dc,
                    signaleringen=signaleringen,
                    kwaliteitsinformatie={"pogingen": self.MAX_INTERPRETATIE_POGINGEN},
                )

            # 4. Projectie: uitsluitend de laag-1-interpretaties (velden + record).
            laag1 = [
                i for i in interpretaties
                if getattr(i, "laag", None) == self.LAAG_ONTWERPVISIE
            ]
            pas_interpretaties_toe(dc, laag1)

        # 5. Vervolgstapkeuze (deterministisch).
        vervolgstap = self._kies_vervolgstap(dc)
        return ConversationPlannerResultaat(
            design_context=dc,
            vervolgstap=vervolgstap,
            kwaliteitsinformatie={"bevestigd": False, "read_only": False},
        )

    # ── Interpretatie-grens met gelimiteerde herhaling + foutafhandeling ──────
    def _interpreteer_met_herhaling(self, tekst: str) -> tuple[Optional[list], list[str]]:
        laatste_fout: Optional[Exception] = None
        for _ in range(1, self.MAX_INTERPRETATIE_POGINGEN + 1):
            try:
                interpretaties = self._interpreteer(tekst)
            except Exception as fout:  # boundary is injecteerbaar en onbekend
                laatste_fout = fout
                continue
            if not isinstance(interpretaties, list):
                return None, ["Interpretatie-grens leverde geen geldige lijst interpretaties."]
            return interpretaties, []
        return None, [
            f"Interpretatie mislukt na {self.MAX_INTERPRETATIE_POGINGEN} pogingen: {laatste_fout}"
        ]

    # ── Deterministische vervolgstapkeuze (BUILD-005 vaste beslisvolgorde) ────
    def _kies_vervolgstap(self, dc: DesignContext) -> Vervolgstap:
        ov = dc.ontwerpvisie
        # Stap 1: is de context voldoende? Zo niet -> gerichte vraag.
        if not self._context_voldoende(ov):
            return Vervolgstap(self.TYPE_VRAAG, self._gerichte_vraag(ov))
        # Stap 2: voldoende context -> samenvatting ter bevestiging (uitsluitend
        # bij een niet-lege visie; door stap 1 gegarandeerd).
        return Vervolgstap(self.TYPE_SAMENVATTING, self._samenvatting(ov))

    def _context_voldoende(self, ov) -> bool:
        heeft_wens = bool(ov.vrije_tekst and ov.vrije_tekst.strip())
        heeft_inhoud = any(
            isinstance(getattr(ov, veld, None), str) and getattr(ov, veld).strip()
            for veld in self._VISIE_INHOUD_VELDEN
        )
        return heeft_wens and heeft_inhoud

    _VRAAG_LABELS = {
        "sfeer": "de gewenste sfeer of beleving",
        "gewenste_identiteit": "de identiteit die de ruimte moet uitstralen",
        "ontwerpambitie": "de ontwerpambitie",
    }

    def _gerichte_vraag(self, ov) -> str:
        if not (ov.vrije_tekst and ov.vrije_tekst.strip()):
            return "Kunt u in eigen woorden vertellen wat u met deze ruimte voor ogen heeft?"
        for veld in self._VISIE_INHOUD_VELDEN:
            waarde = getattr(ov, veld, None)
            if not (isinstance(waarde, str) and waarde.strip()):
                return f"Kunt u iets vertellen over {self._VRAAG_LABELS[veld]}?"
        # Defensief: context zou hier voldoende zijn; val terug op een open vraag.
        return "Wilt u de visie op een punt nog aanvullen of verduidelijken?"

    def _samenvatting(self, ov) -> str:
        onderdelen = [f"wens: {ov.vrije_tekst}"]
        for veld in self._VISIE_INHOUD_VELDEN:
            waarde = getattr(ov, veld, None)
            if isinstance(waarde, str) and waarde.strip():
                onderdelen.append(f"{veld}: {waarde}")
        return (
            "Samenvatting van de ontwerpvisie ter bevestiging — "
            + "; ".join(onderdelen)
            + ". Klopt dit beeld?"
        )
