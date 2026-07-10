"""
Context Interpreter (BUILD-004).

Interpreteert vrije tekst en eventuele basisprojectgegevens naar
voorgestelde interpretaties voor de lagen Ontwerpvisie en ProjectContext
van het DesignContext Model. Levert uitsluitend interpretaties -- nooit
bevestigde waarden, en stelt zelf geen vragen aan de architect (dat is
de verantwoordelijkheid van de toekomstige Conversation Planner, zie
DESIGN_BRAIN_ARCHITECTUURVISIE.md).

Architectuurprincipe (zie BUILD-004_CONTEXT_INTERPRETER_TECHNISCH_ONTWERP.md,
hoofdstuk 0): iedere AI-component binnen de Dessinator produceert
interpretaties, nooit waarheden. Onzekerheid is daarom een eigenschap
van elke afzonderlijke Interpretatie (het "zekerheid"-veld), niet van de
DesignContext-velden zelf.

Volledig losstaand: dit bestand wordt door niets in de bestaande
Dessinator (app.py, modules_extra.py, de /api/generate-flow) aangeroepen
en roept op zijn beurt ook niets uit die bestanden aan. Rollback:
dit bestand verwijderen volstaat.
"""

from __future__ import annotations

import json
from typing import Any, Optional

import anthropic

from design_context import DesignContext, Interpretatie

# Functionele veldnamen (BUILD-004-vocabulaire) -> attribuutnaam op de
# DesignContext-dataclass. "gewenste_beleving" bestond al als "sfeer"
# (BUILD-001A); hier alleen een naam-mapping, geen wijziging van dat veld.
_VELD_NAAR_ATTRIBUUT: dict[str, str] = {
    "projecttype": "projecttype",
    "ruimtetype": "ruimtetype",
    "doelgroep": "doelgroep",
    "functionele_eisen": "functionele_eisen",
    "bijzondere_randvoorwaarden": "bijzondere_randvoorwaarden",
    "gewenste_beleving": "sfeer",
    "gewenste_identiteit": "gewenste_identiteit",
    "ontwerpambitie": "ontwerpambitie",
}

_VELDEN_PROJECTCONTEXT = [
    "projecttype", "ruimtetype", "doelgroep",
    "functionele_eisen", "bijzondere_randvoorwaarden",
]
_VELDEN_ONTWERPVISIE = ["gewenste_beleving", "gewenste_identiteit", "ontwerpambitie"]

_SYSTEM_PROMPT = """Je analyseert vrije tekst van een architect om twee soorten informatie te herkennen:
(1) feiten over het project/de ruimte, en (2) de ontwerpvisie/beleving die de architect nastreeft.

Geef ALLEEN een JSON-object terug (geen uitleg, geen markdown) met onderstaande velden.
Vul een veld alleen in wanneer de tekst daar daadwerkelijk een basis voor geeft -- verzin niets.
Laat een veld volledig weg uit de JSON wanneer de tekst er geen aanwijzing voor bevat.

Voor elk ingevuld veld: "waarde" is een korte, feitelijke samenvatting in het Nederlands,
en "zekerheid" is "hoog", "middel" of "laag" -- hoe zeker je bent dat deze lezing correct is.

{
  "projecttype": {"waarde": "...", "zekerheid": "hoog|middel|laag"},
  "ruimtetype": {"waarde": "...", "zekerheid": "..."},
  "doelgroep": {"waarde": "...", "zekerheid": "..."},
  "functionele_eisen": {"waarde": "...", "zekerheid": "..."},
  "bijzondere_randvoorwaarden": {"waarde": "...", "zekerheid": "..."},
  "gewenste_beleving": {"waarde": "...", "zekerheid": "..."},
  "gewenste_identiteit": {"waarde": "...", "zekerheid": "..."},
  "ontwerpambitie": {"waarde": "...", "zekerheid": "..."}
}

Tekst van de architect: "{tekst}"
"""


def _interpreteer_vrije_tekst(vrije_tekst: str, api_key: str) -> list[Interpretatie]:
    """Roept Claude aan om vrije tekst te interpreteren naar Interpretatie-objecten.

    Volgt hetzelfde aanroepmechaniek als analyse_prompt() in app.py (zelfde
    model, zelfde manier van JSON-afdwingen), maar is een eigen, aparte
    functie -- analyse_prompt() zelf wordt niet aangeraakt of hergebruikt.
    """
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=800,
        messages=[{
            "role": "user",
            "content": _SYSTEM_PROMPT.replace("{tekst}", vrije_tekst),
        }],
    )
    tekst = message.content[0].text.strip()
    tekst = tekst.replace("```json", "").replace("```", "").strip()
    ruw = json.loads(tekst)

    interpretaties = []
    for functioneel_veld in _VELDEN_PROJECTCONTEXT + _VELDEN_ONTWERPVISIE:
        item = ruw.get(functioneel_veld)
        if not item or not item.get("waarde"):
            continue
        laag = "ontwerpvisie" if functioneel_veld in _VELDEN_ONTWERPVISIE else "projectcontext"
        interpretaties.append(Interpretatie(
            laag=laag,
            veld=functioneel_veld,
            waarde=item["waarde"],
            zekerheid=item.get("zekerheid"),
        ))
    return interpretaties


def interpreteer_context(
    vrije_tekst: str,
    basisgegevens: Optional[dict[str, Any]] = None,
    api_key: Optional[str] = None,
) -> list[Interpretatie]:
    """Interpreteert vrije tekst en eventuele basisprojectgegevens.

    Args:
        vrije_tekst: de beschrijving van het project in eigen woorden
            van de architect.
        basisgegevens: reeds bekende gegevens (bv. uit de inspiratie-flow),
            als dict met functionele veldnamen als sleutel. Deze worden
            als interpretatie met zekerheid "hoog" opgenomen, niet
            rechtstreeks als bevestigde waarde -- ook basisgegevens zijn
            een interpretatie totdat de architect ze bevestigt.
        api_key: de Anthropic API-sleutel, op dezelfde manier aangeleverd
            als elders in de Dessinator (geen nieuw sleutelbeheer).

    Returns:
        Een lijst van Interpretatie-objecten. Kan leeg zijn als er noch
        in de vrije tekst, noch in de basisgegevens voldoende basis was.
    """
    interpretaties: list[Interpretatie] = []

    if basisgegevens:
        for functioneel_veld, waarde in basisgegevens.items():
            if functioneel_veld not in _VELD_NAAR_ATTRIBUUT or not waarde:
                continue
            laag = "ontwerpvisie" if functioneel_veld in _VELDEN_ONTWERPVISIE else "projectcontext"
            interpretaties.append(Interpretatie(
                laag=laag,
                veld=functioneel_veld,
                waarde=str(waarde),
                zekerheid="hoog",
            ))

    if vrije_tekst and vrije_tekst.strip():
        if not api_key:
            raise ValueError("api_key is vereist om vrije tekst te interpreteren.")
        interpretaties.extend(_interpreteer_vrije_tekst(vrije_tekst, api_key))

    return interpretaties


def pas_interpretaties_toe(dc: DesignContext, interpretaties: list[Interpretatie]) -> DesignContext:
    """Verwerkt interpretaties in de juiste DesignContext-lagen.

    Legt elke interpretatie vast in dc.interpretaties (het record met
    zekerheid) en zet daarnaast de bijbehorende waarde in het betreffende
    veld van ontwerpvisie/projectcontext. Bevestigt niets: OntwerpVisie's
    `bevestigd_door_architect` blijft ongewijzigd (False, tenzij de
    architect die zelf al had gezet) -- dat blijft uitsluitend een
    handeling van de architect.

    Args:
        dc: de DesignContext waarin de interpretaties worden verwerkt.
        interpretaties: de te verwerken interpretaties.

    Returns:
        Dezelfde DesignContext, met dc.interpretaties uitgebreid en de
        betreffende ontwerpvisie-/projectcontext-velden gevuld.
    """
    for interpretatie in interpretaties:
        dc.interpretaties.append(interpretatie)
        attribuut = _VELD_NAAR_ATTRIBUUT.get(interpretatie.veld)
        if attribuut is None:
            continue
        doel = dc.ontwerpvisie if interpretatie.laag == "ontwerpvisie" else dc.projectcontext
        setattr(doel, attribuut, interpretatie.waarde)
    return dc
