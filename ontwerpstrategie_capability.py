"""
ontwerpstrategie_capability.py — Productie Reasoning Capability: Ontwerpstrategie (IMP-015).

Vervangt UITSLUITEND de deterministische placeholder achter de reeds bestaande
Ontwerpstrategie-boundary (BUILD-009: `RedeneerFunctie = Callable[[dict], dict]`,
contract `{"aanpak", "onderbouwing"}`). De boundary, het contract, het
resultaatobject (OntwerpStrategie / laag 3), de orchestrator, de guards, de
cache/invalidatie en de DesignContext blijven volledig ongewijzigd; deze module
levert enkel een andere injecteerbare redeneerfunctie.

De capability redeneert op REASONING-001 (ontwerpfilosofie): onderbouwd,
uitlegbaar, dienend — een vloer ondersteunt de architectuur en versterkt de
functie. Zij kent GEEN HTTP, opslag, sessies, DesignContext of orchestratie, en
GEEN leveranciersspecifieke logica: uitsluitend de abstracte `ModelClient`
(reasoning_client.py). De concrete client wordt via CONFIGURATIE gekozen
(env `DCOD_REASONING_MODUS`), op één plek — nergens hardcoded of verspreid.

Fallback (AB-012 / BUILD-023 R5): bij welke productiefout dan ook (netwerk,
timeout, authenticatie, rate limiting, provider onbeschikbaar, ongeldig
antwoord) valt de capability GECONTROLEERD terug op de deterministische
placeholder, zodat de gebruiker altijd een geldig contract-resultaat ontvangt en
nooit een technische foutmelding ziet.
"""

from __future__ import annotations

import os
from typing import Optional

from ontwerpstrategie_stap import RedeneerFunctie, placeholder_redenering
from reasoning_client import AnthropicModelClient, ModelClient, extraheer_json

MODUS_PLACEHOLDER = "placeholder"
MODUS_PRODUCTIE = "productie"
_CONFIG_ENV = "DCOD_REASONING_MODUS"

_VERPLICHT = ("aanpak", "onderbouwing")

# REASONING-001 als systeeminstructie: de inhoudelijke ontwerpfilosofie waarop de
# capability redeneert. Geen model-/leveranciersnaam, geen techniek (AB-012).
_SYSTEEM = (
    "Je bent de ontwerpredenering van DCOD, een studio voor vloerontwerp "
    "(printtapijt) voor architecten en interieurontwerpers. Je bepaalt de "
    "ONTWERPSTRATEGIE: de overkoepelende aanpak waarmee een passend vloerconcept "
    "wordt ontwikkeld, nog vóór concrete kleur-, materiaal- of patroonkeuzes.\n\n"
    "Ontwerpfilosofie (leidend):\n"
    "- Een vloer is een dragend, dienend ontwerpelement: hij ondersteunt de "
    "architectuur, versterkt de functie en maakt het verhaal van de ruimte "
    "compleet — hij is niet het verhaal zelf.\n"
    "- Redeneer vanuit de driehoek architectuur — functie — vloer, nooit vanuit "
    "een los esthetisch idee.\n"
    "- Weeg de ontwerpfactoren in samenhang: ruimtefunctie en gebruik, doelgroep, "
    "sfeer en identiteit, licht, en de randvoorwaarden onderhoud, akoestiek, "
    "duurzaamheid, budget en productie.\n"
    "- Ruimtefunctie, maakbaarheid en budget zijn harde ondergrenzen; sfeer, "
    "identiteit en beleving krijgen hun gewicht uit de opdracht.\n\n"
    "Eisen aan je antwoord:\n"
    "- Onderbouwd en uitlegbaar: elke keuze is herleidbaar naar de context; geen "
    "willekeur, geen 'omdat het mooi is'.\n"
    "- Je STELT VOOR, je beslist niet: formuleer een aanpak, geen definitief "
    "eindproduct.\n"
    "- Schrijf in helder Nederlands, zonder jargon, en zonder te verwijzen naar "
    "AI, modellen of techniek.\n\n"
    "Geef ALLEEN een JSON-object terug (geen uitleg, geen markdown):\n"
    '{"aanpak": "1–2 zinnen: de overkoepelende ontwerpstrategie", '
    '"onderbouwing": "2–4 zinnen: waarom deze strategie past bij de context"}'
)

_GEBRUIKER_SJABLOON = (
    "Context voor deze ontwerpopdracht:\n"
    "- Vrije omschrijving: {vrije_tekst}\n"
    "- Gewenste sfeer/beleving: {sfeer}\n"
    "- Gewenste identiteit: {gewenste_identiteit}\n"
    "- Ontwerpambitie: {ontwerpambitie}\n"
    "- Projecttype: {projecttype}\n"
    "- Ruimtetype: {ruimtetype}\n"
    "- Doelgroep: {doelgroep}\n"
    "- Gebruikscontext: {gebruikscontext}\n\n"
    "Bepaal op basis hiervan de ontwerpstrategie."
)

_INVOERVELDEN = (
    "vrije_tekst", "sfeer", "gewenste_identiteit", "ontwerpambitie",
    "projecttype", "ruimtetype", "doelgroep", "gebruikscontext",
)


def _geldig_voorstel(voorstel: dict) -> bool:
    """Zelfde contract-eis als OntwerpStrategieStap._valideer_voorstel: beide
    verplichte velden aanwezig en niet-leeg."""
    return isinstance(voorstel, dict) and all(
        isinstance(voorstel.get(v), str) and voorstel.get(v).strip() for v in _VERPLICHT
    )


def _gebruikerprompt(invoer: dict) -> str:
    velden = {v: (str(invoer.get(v)).strip() if invoer.get(v) else "(niet opgegeven)")
              for v in _INVOERVELDEN}
    return _GEBRUIKER_SJABLOON.format(**velden)


class ProductieStrategieReasoner:
    """Productie-implementatie van de reasoning boundary.

    Bouwt een op REASONING-001 gebaseerde opdracht, laat het model redeneren via
    de abstracte `ModelClient`, en levert `{"aanpak", "onderbouwing"}`. Bij ELKE
    fout — netwerk, timeout, authenticatie, rate limiting, provider onbeschikbaar,
    of een onvolledig/ongeldig antwoord — valt zij GECONTROLEERD terug op de
    deterministische placeholder. De terugval is bewust exception-type-agnostisch
    (vangt alles af), zodat een productie-reasoning nooit tot een technische fout
    of een leeg resultaat voor de gebruiker leidt (AB-012 / BUILD-023 R5).
    """

    def __init__(self, model_client: ModelClient) -> None:
        self._model = model_client

    def redeneer(self, invoer: dict) -> dict:
        try:
            ruw = self._model.genereer(_SYSTEEM, _gebruikerprompt(invoer))
            data = extraheer_json(ruw)
            voorstel = {
                "aanpak": (data.get("aanpak") or "").strip(),
                "onderbouwing": (data.get("onderbouwing") or "").strip(),
            }
            if not _geldig_voorstel(voorstel):
                return placeholder_redenering(invoer)
            return voorstel
        except Exception:
            # Gecontroleerde, onzichtbare terugval op de deterministische
            # placeholder — nooit een technische fout naar de gebruiker (AB-012).
            return placeholder_redenering(invoer)


def maak_ontwerpstrategie_redeneerfunctie(
    api_sleutel: str = "", modus: Optional[str] = None
) -> RedeneerFunctie:
    """Configuratie-gestuurde keuze van de reasoning-client (één plek).

    - `modus` None → gelezen uit env `DCOD_REASONING_MODUS` (default 'placeholder');
    - 'productie' mét geldige serversleutel → `ProductieStrategieReasoner`
      bovenop de Anthropic-adapter;
    - in alle overige gevallen (incl. 'productie' zónder sleutel) → de bestaande
      deterministische placeholder.

    Retourneert een `RedeneerFunctie` (Callable[[dict], dict]) die onveranderd in
    de bestaande `OntwerpStrategieStap` wordt geïnjecteerd. De sleutel komt van de
    aanroeper (integratielaag, `_ai_sleutel()` — AB-012: uitsluitend
    serverconfiguratie); deze module leest zelf nooit de request of de sleutel.
    """
    if modus is None:
        modus = (os.environ.get(_CONFIG_ENV) or MODUS_PLACEHOLDER).strip().lower()
    if modus == MODUS_PRODUCTIE and (api_sleutel or "").strip():
        return ProductieStrategieReasoner(AnthropicModelClient(api_sleutel.strip())).redeneer
    return placeholder_redenering
