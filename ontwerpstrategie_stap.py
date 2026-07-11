"""
BUILD-009 -- Ontwerpstrategie-stap.

Implementeert de reeds bekrachtigde component uit T7 (AB-008): de
Ontwerpstrategie-stap die voorgestelde inhoud voor DesignContext-laag 3
(Ontwerpstrategie) produceert. Zij STELT VOOR, bevestigt nooit.

De component is intern gesplitst in drie verantwoordelijkheden
(BUILD-009 technisch ontwerp):

  1. validatie        -- preconditie- en overwrite-guard-controles;
  2. reasoning boundary -- de redeneerstap, AI-model-onafhankelijk;
  3. registratie      -- wegschrijven van het voorstel + Ontwerpredenering.

De reasoning boundary kent DesignContext niet en kent de registratie niet:
zij ontvangt uitsluitend een platte dict met de noodzakelijke invoer en
retourneert uitsluitend een voorstel (dict met "aanpak" en "onderbouwing").
Dit bestand bevat GEEN LLM-aanroepen en GEEN promptteksten; de meegeleverde
`placeholder_redenering` dient uitsluitend om de architectuur te kunnen
testen. Een echte, model-specifieke redenering kan later worden geinjecteerd
zonder deze component te wijzigen.

Volledig additief en losstaand: geen wijziging aan design_context.py, app.py,
de generatie-pipeline of de frontend. Niets in de bestaande Dessinator roept
deze module aan.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

from design_context import DesignContext, OntwerpStrategie


# ─── Reasoning boundary (AI-model-onafhankelijk) ────────────────────────────
#
# Contract: een functie die een platte invoer-dict ontvangt en een voorstel-
# dict teruggeeft met de sleutels "aanpak" en "onderbouwing". Zij kent
# DesignContext noch registratie -- puur voorstel in, voorstel uit.

RedeneerFunctie = Callable[[dict], dict]


def placeholder_redenering(invoer: dict) -> dict:
    """Deterministische placeholder voor de reasoning boundary.

    Bevat geen LLM-aanroep en geen promptteksten. Stelt op basis van de
    meegegeven visie-/contextvelden een eenvoudige aanpak + onderbouwing samen,
    zodat de keten validatie -> boundary -> registratie testbaar is zonder AI.
    """
    sfeer = invoer.get("sfeer") or "de gevraagde beleving"
    context = invoer.get("ruimtetype") or invoer.get("projecttype") or "de opgegeven context"
    aanpak = f"Aanpak afgestemd op {sfeer} binnen {context}."
    onderbouwing = (
        "Afgeleid uit de bevestigde Ontwerpvisie en de vastgelegde "
        "Project-/Ruimtecontext (placeholder-redenering)."
    )
    return {"aanpak": aanpak, "onderbouwing": onderbouwing}


@dataclass
class StrategieResultaat:
    """Technische returnvorm (geen architectuurobject): een voorgestelde
    OntwerpStrategie, of uitsluitend signaleringen wanneer de stap niet mag
    of kan starten."""

    strategie: Optional[OntwerpStrategie] = None
    signaleringen: list[str] = field(default_factory=list)

    @property
    def geslaagd(self) -> bool:
        return self.strategie is not None


class OntwerpStrategieStap:
    """Publieke component van BUILD-009.

    Roep `stel_voor(dc)` aan met een DesignContext. Bij geldige input wordt een
    OntwerpStrategie (status "in ontwikkeling") in laag 3 gezet en een reden in
    de Ontwerpredenering geregistreerd; laag 1 en 2 worden nooit gemuteerd.
    Bij onvoldoende of niet-bevestigde context, of bij een reeds vastgestelde
    strategie (overwrite-guard), wordt uitsluitend een signalering teruggegeven.
    """

    STATUS_IN_ONTWIKKELING = "in ontwikkeling"
    STATUS_VASTGESTELD = "vastgesteld"
    _VERPLICHTE_VOORSTEL_VELDEN = ("aanpak", "onderbouwing")

    def __init__(self, redeneer: RedeneerFunctie = placeholder_redenering) -> None:
        # De reasoning boundary is injecteerbaar; standaard de placeholder.
        self._redeneer = redeneer

    def stel_voor(self, dc: DesignContext) -> StrategieResultaat:
        """Voert de drie interne stappen uit: validatie, boundary, registratie."""
        # 1. Validatie (inclusief overwrite-guard)
        signaleringen = self._valideer(dc)
        if signaleringen:
            return StrategieResultaat(signaleringen=signaleringen)

        # 2. Reasoning boundary -- uitsluitend de noodzakelijke invoer.
        #    Een technische fout in de (injecteerbare) redenering mag nooit
        #    een partiele Ontwerpstrategie wegschrijven.
        try:
            voorstel = self._redeneer(self._verzamel_invoer(dc))
        except Exception as fout:  # boundary is injecteerbaar en onbekend
            return StrategieResultaat(
                signaleringen=[f"Technische fout in de reasoning boundary: {fout}"]
            )

        # 2b. Validatie van de boundary-output vóór registratie: een onvolledig
        #     voorstel wordt niet geregistreerd.
        voorstel_signaleringen = self._valideer_voorstel(voorstel)
        if voorstel_signaleringen:
            return StrategieResultaat(signaleringen=voorstel_signaleringen)

        # 3. Registratie -- voorstel wegschrijven, nooit bevestigen
        strategie = OntwerpStrategie(
            aanpak=voorstel.get("aanpak"),
            onderbouwing=voorstel.get("onderbouwing"),
            status=self.STATUS_IN_ONTWIKKELING,
        )
        dc.ontwerpstrategie = strategie
        dc.ontwerpredenering.voeg_beslissing_toe(
            laag="ontwerpstrategie",
            reden=strategie.onderbouwing or "voorgestelde ontwerpstrategie",
            vervangt=None,
        )
        return StrategieResultaat(strategie=strategie)

    # ── Validatie ───────────────────────────────────────────────────────────
    def _valideer(self, dc: DesignContext) -> list[str]:
        signaleringen: list[str] = []

        ov = dc.ontwerpvisie
        if not ov.bevestigd_door_architect:
            signaleringen.append("Ontwerpvisie is nog niet bevestigd.")
        if not (ov.vrije_tekst or ov.voorgestelde_interpretatie or ov.sfeer):
            signaleringen.append("Ontwerpvisie bevat onvoldoende inhoud.")

        pc = dc.projectcontext
        if not (pc.projecttype or pc.ruimtetype or pc.gebruikscontext):
            signaleringen.append("Project-/Ruimtecontext is onvoldoende vastgelegd.")

        # Overwrite-guard: een reeds vastgestelde laag 3 wordt niet overschreven.
        if dc.ontwerpstrategie.status == self.STATUS_VASTGESTELD:
            signaleringen.append(
                "Ontwerpstrategie is reeds vastgesteld en wordt niet overschreven."
            )

        return signaleringen

    # ── Validatie van de boundary-output ──────────────────────────────────────
    @classmethod
    def _valideer_voorstel(cls, voorstel: dict) -> list[str]:
        """Controleert dat de reasoning boundary een volledig voorstel gaf.

        Ontbrekende of lege verplichte velden leiden tot een signalering; er
        wordt dan geen (onvolledige) Ontwerpstrategie geregistreerd.
        """
        if not isinstance(voorstel, dict):
            return ["Reasoning boundary gaf geen geldig voorstel terug."]
        signaleringen: list[str] = []
        for veld in cls._VERPLICHTE_VOORSTEL_VELDEN:
            waarde = voorstel.get(veld)
            if waarde is None or (isinstance(waarde, str) and not waarde.strip()):
                signaleringen.append(f"Voorstel mist verplicht veld: {veld}.")
        return signaleringen

    # ── Invoer voor de reasoning boundary ─────────────────────────────────────
    @staticmethod
    def _verzamel_invoer(dc: DesignContext) -> dict:
        """Verzamelt uitsluitend de velden die de boundary nodig heeft.

        Geeft platte waarden door -- geen DesignContext, geen dataclasses --
        zodat de boundary volledig ontkoppeld blijft.
        """
        ov = dc.ontwerpvisie
        pc = dc.projectcontext
        return {
            "vrije_tekst": ov.vrije_tekst,
            "sfeer": ov.sfeer,
            "gewenste_identiteit": ov.gewenste_identiteit,
            "ontwerpambitie": ov.ontwerpambitie,
            "projecttype": pc.projecttype,
            "ruimtetype": pc.ruimtetype,
            "doelgroep": pc.doelgroep,
            "gebruikscontext": pc.gebruikscontext,
        }
