"""
pattern_planning_capability.py — Productie Reasoning Capability: Pattern Planning (IMP-019).

Vijfde productie-capability, exact volgens het bewezen IMP-015/016/017/018-patroon.
Vervangt UITSLUITEND de deterministische placeholder achter de bestaande Pattern
Reasoning Boundary (BUILD-013: `PatroonRedeneerFunctie = Callable[[dict], list]`,
contract = lijst van patroonvoorstellen met verplicht `motiefstructuur`/
`motiefschaal`/`motivering` en optioneel `dichtheid`/`herhalingskarakter`). De
boundary, het contract, het PatternProfile-resultaatobject (identifier/status/
herkomst, buiten de DesignContext), de orchestrator, de guards, de cache/
invalidatie, de DesignContext en de componentgrenzen blijven volledig ongewijzigd;
deze module levert enkel een andere injecteerbare redeneerfunctie.

Vertaalt de drie bevestigde upstream-objecten (Concept + Floor Design + Material
Profile) naar één of meer technisch realiseerbare printtapijt-patronen. De
capability redeneert op REASONING-001 en houdt de patronen binnen het concept en
passend bij het materiaal en de ontwerprichting. Zij kent GEEN HTTP, opslag,
sessies, DesignContext of orchestratie, en GEEN leveranciersspecifieke logica —
uitsluitend de abstracte `ModelClient` (reasoning_client.py). Provider-/
modusselectie wordt hergebruikt uit IMP-015/016/017/018.

Downstream-veiligheid (regressie): `motiefschaal` wordt genormaliseerd naar
{klein, gemiddeld, groot} (die de SVG-pipeline-adapter mapt naar 50/100/200);
`motiefstructuur` is vrije tekst (de SVG-adapter resolveert de stijl uit
stijlfamilie/motiefstructuur). VAL-004-les: ruimere `max_tokens` om JSON-afkapping
te voorkomen. Bij welke productiefout of onbruikbaar antwoord dan ook valt de
capability gecontroleerd terug op de deterministische placeholder — het bestaande
contract blijft altijd geldig en de gebruiker ziet nooit een technische melding
(AB-012 / BUILD-023 R5).
"""

from __future__ import annotations

import json
from typing import Optional

from reasoning_client import AnthropicModelClient, ModelClient, kies_redeneerfunctie
from pattern_planner import PatroonRedeneerFunctie, placeholder_patroon_generatie

_MAX_VOORSTELLEN = 3
_LIJST_SLEUTELS = ("voorstellen", "patronen", "pattern_profiles", "patroonvoorstellen", "profielen")

# Downstream-vocabulaire (svg_planner_pipeline motiefschaal-mapping).
_MOTIEFSCHAAL_SYN = {
    "klein": "klein", "fijn": "klein", "smal": "klein", "small": "klein", "fine": "klein",
    "gemiddeld": "gemiddeld", "normaal": "gemiddeld", "medium": "gemiddeld", "normal": "gemiddeld",
    "groot": "groot", "grof": "groot", "large": "groot", "breed": "groot",
}
_STANDAARD_SCHAAL = "gemiddeld"

_SYSTEEM = (
    "Je bent de patroondeskundige van DCOD, een studio voor vloerontwerp "
    "(PRINTTAPIJT) voor architecten en interieurontwerpers. Op basis van het "
    "bevestigde concept, het gekozen Floor Design en het gekozen materiaal bepaal "
    "je nu het PATROON: één of meer technisch realiseerbare, naadloos tegelbare "
    "printtapijt-patronen.\n\n"
    "Ontwerpfilosofie (leidend):\n"
    "- Een vloer is een dragend, dienend ontwerpelement; het patroon werkt de "
    "gekozen ontwerprichting concreet uit en respecteert het materiaal.\n"
    "- Elk patroon blijft BINNEN het bevestigde concept en de ontwerprichting; je "
    "verlaat die niet en spreekt ze niet tegen.\n"
    "- Weeg schaal, dichtheid en herhaling in verhouding tot de ruimte, de "
    "leesbaarheid en de rust; houd rekening met naadloze tegeling en printbaarheid.\n"
    "- Variatie is bewust: bied betekenisvol verschillende patroonrichtingen "
    "(bijvoorbeeld rustiger/opener versus ritmischer/dichter), geen willekeurige "
    "ruis en geen bijna-identieke varianten.\n"
    "- Onderbouwd en uitlegbaar; je STELT VOOR, je beslist niet.\n"
    "- Schrijf in helder Nederlands, zonder jargon, en zonder te verwijzen naar "
    "AI, modellen of techniek.\n\n"
    "Geef ALLEEN een JSON-array terug (geen uitleg, geen markdown) met 2 of 3 "
    "objecten, elk met:\n"
    "- 'motiefstructuur': korte beschrijving van de motiefopbouw (bv. organisch "
    "vloeiend, geometrisch ritmisch, fijn lineair);\n"
    "- 'motiefschaal': EXACT één van 'klein', 'gemiddeld', 'groot';\n"
    "- 'dichtheid': bv. open, gemiddeld, dicht;\n"
    "- 'herhalingskarakter': bv. full, half-drop, brick, spiegelend;\n"
    "- 'motivering': waarom dit patroon past bij concept, ontwerprichting en "
    "materiaal, en naadloos printbaar is.\n\n"
    '[{"motiefstructuur": "...", "motiefschaal": "klein|gemiddeld|groot", '
    '"dichtheid": "...", "herhalingskarakter": "...", "motivering": "..."}]'
)

_GEBRUIKER_SJABLOON = (
    "Bevestigd concept:\n"
    "- Stijlfamilie: {stijlfamilie}\n"
    "- Kleurpalet: {kleurpalet}\n"
    "- Complexiteit: {complexiteit}\n"
    "- Motiefschaal (concept): {motiefschaal}\n\n"
    "Gekozen Floor Design (ontwerprichting):\n"
    "- {ontwerprichting}\n\n"
    "Gekozen materiaal:\n"
    "- Structuur: {structuur}\n"
    "- Pooltype: {pooltype}\n"
    "- Uitstraling: {uitstraling}\n\n"
    "Bepaal 2 à 3 technisch realiseerbare printtapijt-patronen die binnen dit "
    "concept en deze ontwerprichting blijven en bij dit materiaal passen."
)

_INVOERVELDEN = (
    "stijlfamilie", "kleurpalet", "complexiteit", "motiefschaal",
    "ontwerprichting", "structuur", "pooltype", "uitstraling",
)


def _gebruikerprompt(invoer: dict) -> str:
    velden = {v: (str(invoer.get(v)).strip() if invoer.get(v) else "(niet opgegeven)")
              for v in _INVOERVELDEN}
    return _GEBRUIKER_SJABLOON.format(**velden)


def _json_uit_tekst(tekst: str):
    schoon = (tekst or "").strip().replace("```json", "").replace("```", "").strip()
    return json.loads(schoon)


def _normaliseer(data) -> Optional[list]:
    """Zet een modelantwoord (array of object) om naar een lijst downstream-veilige
    patroonvoorstellen, of None wanneer onbruikbaar (→ terugval placeholder).
    `motiefschaal` wordt genormaliseerd naar {klein, gemiddeld, groot}; voorstellen
    die het concept verlaten worden geweerd."""
    if isinstance(data, dict):
        for sleutel in _LIJST_SLEUTELS:
            if isinstance(data.get(sleutel), list):
                data = data[sleutel]
                break
        else:
            data = [data] if data.get("motiefstructuur") else None
    if not isinstance(data, list):
        return None

    schoon: list = []
    for item in data:
        if not isinstance(item, dict) or item.get("verlaat_concept") is True:
            continue
        structuur = item.get("motiefstructuur")
        motivering = item.get("motivering")
        if not (isinstance(structuur, str) and structuur.strip()
                and isinstance(motivering, str) and motivering.strip()):
            continue
        schaal = _MOTIEFSCHAAL_SYN.get(str(item.get("motiefschaal", "")).strip().lower(), _STANDAARD_SCHAAL)
        voorstel = {
            "motiefstructuur": structuur.strip(),
            "motiefschaal": schaal,
            "motivering": motivering.strip(),
        }
        for veld in ("dichtheid", "herhalingskarakter"):
            if isinstance(item.get(veld), str) and item.get(veld).strip():
                voorstel[veld] = item[veld].strip()
        schoon.append(voorstel)
        if len(schoon) >= _MAX_VOORSTELLEN:
            break
    return schoon or None


class ProductiePatroonReasoner:
    """Productie-implementatie van de Pattern Reasoning Boundary.

    Bouwt een op REASONING-001 gebaseerde opdracht bovenop concept, ontwerprichting
    en materiaal, laat het model één of meer technisch realiseerbare patronen bepalen
    via de abstracte `ModelClient`, en levert een lijst genormaliseerde, downstream-
    veilige voorstellen. Bij ELKE fout — netwerk, timeout, authenticatie, rate
    limiting, provider onbeschikbaar, of een onbruikbaar/leeg antwoord — valt zij
    GECONTROLEERD terug op de deterministische placeholder (exception-type-agnostisch),
    zodat het bestaande contract altijd geldig blijft en de gebruiker nooit een
    technische fout ziet (AB-012 / BUILD-023 R5).
    """

    def __init__(self, model_client: ModelClient) -> None:
        self._model = model_client

    def redeneer(self, invoer: dict) -> list:
        try:
            ruw = self._model.genereer(_SYSTEEM, _gebruikerprompt(invoer))
            voorstellen = _normaliseer(_json_uit_tekst(ruw))
            if not voorstellen:
                return placeholder_patroon_generatie(invoer)
            return voorstellen
        except Exception:
            return placeholder_patroon_generatie(invoer)


def maak_pattern_planning_redeneerfunctie(
    api_sleutel: str = "", modus: Optional[str] = None
) -> PatroonRedeneerFunctie:
    """Configuratie-gestuurde keuze van de reasoning-client (hergebruikt de gedeelde
    factory): 'productie' mét serversleutel → productie-reasoner, anders de bestaande
    deterministische placeholder. Retourneert een `PatroonRedeneerFunctie`
    (Callable[[dict], list]) voor injectie in de ongewijzigde `PatternPlanner`."""
    return kies_redeneerfunctie(
        api_sleutel,
        placeholder_patroon_generatie,
        # VAL-004-les: ruimere token-limiet om afkapping van meervoudige output te
        # voorkomen; gedeelde default en overige capabilities ongewijzigd.
        lambda sl: ProductiePatroonReasoner(AnthropicModelClient(sl, max_tokens=1200)).redeneer,
        modus,
    )
