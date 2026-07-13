"""
floor_design_capability.py — Productie Reasoning Capability: Floor Design (IMP-017).

Eerste productie-capability van Fase 2 van de Design Brain, exact volgens het
bewezen IMP-015/016-patroon. Vervangt UITSLUITEND de deterministische placeholder
achter de bestaande Floor Design-boundary (BUILD-011, Reasoning Engine Fase 2:
`FloorDesignRedeneerFunctie = Callable[[dict], list]`, contract = lijst van
`{"ontwerprichting", "motivering"}`). De boundary, het contract, het FloorDesign-
resultaatobject (identifier/status/herkomst, buiten de DesignContext), de
orchestrator, de guards, de cache/invalidatie, de DesignContext en de
componentgrenzen blijven volledig ongewijzigd; deze module levert enkel een
andere injecteerbare redeneerfunctie.

Bouwt logisch voort op het reeds BEVESTIGDE Concept (Fase 1) en de vastgestelde
Ontwerpstrategie: het bevestigde concept (stijlfamilie/kleurpalet/complexiteit/
motiefschaal) + context (sfeer/projecttype/ruimtetype) vormen het kader. De
capability produceert meerdere BEWUST onderscheiden ontwerprichtingen die BINNEN
het concept blijven (REASONING-001: bewuste variatie, geen willekeur). Zij kent
GEEN HTTP, opslag, sessies, DesignContext of orchestratie, en GEEN leveranciers-
specifieke logica — uitsluitend de abstracte `ModelClient` (reasoning_client.py).
Provider-/modusselectie wordt hergebruikt uit IMP-015/016.

Downstream-compatibiliteit (regressie): elk voorstel levert uitsluitend de door
de engine gebruikte velden `ontwerprichting` + `motivering`; de engine bouwt daar
de FloorDesign-objecten van. Voorstellen die het concept expliciet verlaten
(`verlaat_concept`) worden weggelaten. Bij welke productiefout of onbruikbaar
antwoord dan ook valt de capability gecontroleerd terug op de deterministische
placeholder — het bestaande contract blijft altijd geldig en de gebruiker ziet
nooit een technische melding (AB-012 / BUILD-023 R5).
"""

from __future__ import annotations

import json
from typing import Optional

from reasoning_client import AnthropicModelClient, ModelClient, kies_redeneerfunctie
from reasoning_engine import FloorDesignRedeneerFunctie, placeholder_floor_design_generatie

_MAX_VOORSTELLEN = 3
_LIJST_SLEUTELS = ("voorstellen", "floor_designs", "designs", "ontwerprichtingen", "richtingen")

_SYSTEEM = (
    "Je bent de ontwerpredenering van DCOD, een studio voor vloerontwerp "
    "(printtapijt) voor architecten en interieurontwerpers. Op basis van het "
    "reeds BEVESTIGDE concept werk je nu meerdere concrete FLOOR DESIGNS uit: "
    "onderscheiden ontwerprichtingen voor de vloer.\n\n"
    "Ontwerpfilosofie (leidend):\n"
    "- Een vloer is een dragend, dienend ontwerpelement: hij ondersteunt de "
    "architectuur, versterkt de functie en maakt het verhaal van de ruimte "
    "compleet — hij is niet het verhaal zelf.\n"
    "- Elke ontwerprichting blijft BINNEN het bevestigde concept (stijlfamilie, "
    "kleurpalet, complexiteit, motiefschaal); je verlaat het concept niet en "
    "spreekt het niet tegen.\n"
    "- Variatie is bewust: bied betekenisvol verschillende richtingen (bijvoorbeeld "
    "rustiger versus expressiever, of een andere ordening/ritme), geen willekeurige "
    "ruis en geen bijna-identieke varianten.\n"
    "- Onderbouwd en uitlegbaar; je STELT VOOR, je beslist niet.\n"
    "- Schrijf in helder Nederlands, zonder jargon, en zonder te verwijzen naar "
    "AI, modellen of techniek.\n\n"
    "Geef ALLEEN een JSON-array terug (geen uitleg, geen markdown) met 2 of 3 "
    "objecten, elk met:\n"
    "- 'ontwerprichting': een korte, concrete beschrijving van de vloerrichting;\n"
    "- 'motivering': waarom deze richting binnen het concept past.\n\n"
    '[{"ontwerprichting": "...", "motivering": "..."}, '
    '{"ontwerprichting": "...", "motivering": "..."}]'
)

_GEBRUIKER_SJABLOON = (
    "Bevestigd concept:\n"
    "- Stijlfamilie: {stijlfamilie}\n"
    "- Kleurpalet: {kleurpalet}\n"
    "- Complexiteit: {complexiteit}\n"
    "- Motiefschaal: {motiefschaal}\n\n"
    "Context:\n"
    "- Sfeer: {sfeer}\n"
    "- Projecttype: {projecttype}\n"
    "- Ruimtetype: {ruimtetype}\n\n"
    "Werk 2 à 3 onderscheiden floor-designrichtingen uit die binnen dit concept blijven."
)

_INVOERVELDEN = (
    "stijlfamilie", "kleurpalet", "complexiteit", "motiefschaal",
    "sfeer", "projecttype", "ruimtetype",
)


def _gebruikerprompt(invoer: dict) -> str:
    velden = {v: (str(invoer.get(v)).strip() if invoer.get(v) else "(niet opgegeven)")
              for v in _INVOERVELDEN}
    return _GEBRUIKER_SJABLOON.format(**velden)


def _json_uit_tekst(tekst: str):
    """Parseert modeltekst naar JSON (array óf object). Verwijdert ```-hekjes.
    Werpt bij ongeldige JSON — de capability vangt dat af als reden voor terugval."""
    schoon = (tekst or "").strip().replace("```json", "").replace("```", "").strip()
    return json.loads(schoon)


def _normaliseer(data) -> Optional[list]:
    """Zet een modelantwoord (array of object) om naar een lijst downstream-veilige
    voorstel-dicts `{"ontwerprichting", "motivering"}`, of None wanneer onbruikbaar
    (→ terugval placeholder). Voorstellen die het concept verlaten worden geweerd."""
    if isinstance(data, dict):
        for sleutel in _LIJST_SLEUTELS:
            if isinstance(data.get(sleutel), list):
                data = data[sleutel]
                break
        else:
            data = [data] if data.get("ontwerprichting") else None
    if not isinstance(data, list):
        return None

    schoon: list = []
    for item in data:
        if not isinstance(item, dict) or item.get("verlaat_concept") is True:
            continue
        richting = item.get("ontwerprichting")
        motivering = item.get("motivering")
        if (isinstance(richting, str) and richting.strip()
                and isinstance(motivering, str) and motivering.strip()):
            schoon.append({"ontwerprichting": richting.strip(),
                           "motivering": motivering.strip()})
        if len(schoon) >= _MAX_VOORSTELLEN:
            break
    return schoon or None


class ProductieFloorDesignReasoner:
    """Productie-implementatie van de Floor Design-reasoning boundary (Fase 2).

    Bouwt een op REASONING-001 gebaseerde opdracht bovenop het bevestigde concept,
    laat het model meerdere onderscheiden ontwerprichtingen bepalen via de abstracte
    `ModelClient`, en levert een lijst genormaliseerde, downstream-veilige
    voorstellen. Bij ELKE fout — netwerk, timeout, authenticatie, rate limiting,
    provider onbeschikbaar, of een onbruikbaar/leeg antwoord — valt zij
    GECONTROLEERD terug op de deterministische placeholder (exception-type-
    agnostisch), zodat het bestaande contract altijd geldig blijft en de gebruiker
    nooit een technische fout ziet (AB-012 / BUILD-023 R5).
    """

    def __init__(self, model_client: ModelClient) -> None:
        self._model = model_client

    def redeneer(self, invoer: dict) -> list:
        try:
            ruw = self._model.genereer(_SYSTEEM, _gebruikerprompt(invoer))
            voorstellen = _normaliseer(_json_uit_tekst(ruw))
            if not voorstellen:
                return placeholder_floor_design_generatie(invoer)
            return voorstellen
        except Exception:
            return placeholder_floor_design_generatie(invoer)


def maak_floor_design_redeneerfunctie(
    api_sleutel: str = "", modus: Optional[str] = None
) -> FloorDesignRedeneerFunctie:
    """Configuratie-gestuurde keuze van de reasoning-client (hergebruikt de gedeelde
    IMP-015/016-factory): 'productie' mét serversleutel → productie-reasoner, anders
    de bestaande deterministische placeholder. Retourneert een
    `FloorDesignRedeneerFunctie` (Callable[[dict], list]) voor injectie in de
    ongewijzigde `ReasoningEngine`."""
    return kies_redeneerfunctie(
        api_sleutel,
        placeholder_floor_design_generatie,
        lambda sl: ProductieFloorDesignReasoner(AnthropicModelClient(sl)).redeneer,
        modus,
    )
