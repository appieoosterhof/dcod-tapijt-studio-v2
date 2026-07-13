"""
material_planning_capability.py — Productie Reasoning Capability: Material Planning (IMP-018).

Vierde productie-capability, exact volgens het bewezen IMP-015/016/017-patroon.
Vervangt UITSLUITEND de deterministische placeholder achter de bestaande Material
Reasoning Boundary (BUILD-012: `MateriaalRedeneerFunctie = Callable[[dict], list]`,
contract = lijst van materiaalvoorstellen met verplicht
`materiaalsoort`/`structuur`/`pooltype`/`motivering` en optioneel
`tactiliteit`/`uitstraling`). De boundary, het contract, het MaterialProfile-
resultaatobject (identifier/status/herkomst, buiten de DesignContext), de
orchestrator, de guards, de cache/invalidatie, de DesignContext en de
componentgrenzen blijven volledig ongewijzigd; deze module levert enkel een
andere injecteerbare redeneerfunctie.

Vertaalt een gekozen (bevestigd) Floor Design + bevestigd Concept naar een
technisch verantwoord materiaalvoorstel voor printtapijt. De capability redeneert
op REASONING-001 en weegt — voor zover uit de ontwerprichting en het concept af te
leiden — gebruiksintensiteit, onderhoud, slijtvastheid, akoestiek, comfort,
duurzaamheid en productietechnische haalbaarheid, en verwerkt die afweging in de
motivering. Zij kent GEEN HTTP, opslag, sessies, DesignContext of orchestratie, en
GEEN leveranciersspecifieke logica — uitsluitend de abstracte `ModelClient`
(reasoning_client.py). Provider-/modusselectie wordt hergebruikt uit IMP-015/016/017.

Afbakening (regressie/contract): de boundary-invoer ligt vast op
{stijlfamilie, kleurpalet, complexiteit, motiefschaal, ontwerprichting} (BUILD-024);
deze module voegt GEEN invoervelden toe (bv. projecttype) — dat zou een
contract-/componentwijziging zijn. Elk voorstel levert uitsluitend de door de
Material Planner gebruikte velden. Bij welke productiefout of onbruikbaar antwoord
dan ook valt de capability gecontroleerd terug op de deterministische placeholder
— het bestaande contract blijft altijd geldig en de gebruiker ziet nooit een
technische melding (AB-012 / BUILD-023 R5).
"""

from __future__ import annotations

import json
from typing import Optional

from reasoning_client import AnthropicModelClient, ModelClient, kies_redeneerfunctie
from material_planner import MateriaalRedeneerFunctie, placeholder_materiaal_generatie

_MAX_VOORSTELLEN = 3
_LIJST_SLEUTELS = ("voorstellen", "materialen", "material_profiles", "materiaalvoorstellen", "profielen")
_VERPLICHT = ("materiaalsoort", "structuur", "pooltype", "motivering")
_OPTIONEEL = ("tactiliteit", "uitstraling")

_SYSTEEM = (
    "Je bent de materiaaldeskundige van DCOD, een studio voor vloerontwerp "
    "(PRINTTAPIJT) voor architecten en interieurontwerpers. Op basis van het reeds "
    "bevestigde concept en het gekozen Floor Design bepaal je nu het MATERIAAL: "
    "één of meer technisch verantwoorde tapijtmaterialisaties.\n\n"
    "Ontwerpfilosofie (leidend):\n"
    "- Een vloer is een dragend, dienend ontwerpelement; het materiaal ondersteunt "
    "de gekozen ontwerprichting en maakt die technisch realiseerbaar.\n"
    "- Elk materiaalvoorstel blijft BINNEN het bevestigde concept en de gekozen "
    "ontwerprichting; je verlaat die niet en spreekt ze niet tegen.\n"
    "- Weeg — voor zover uit de ontwerprichting en het concept af te leiden — "
    "gebruiksintensiteit, onderhoud en reinigbaarheid, slijtvastheid, akoestiek, "
    "loopcomfort, duurzaamheid, en de productietechnische haalbaarheid als "
    "printtapijt (printkwaliteit, toepassingsgeschiktheid).\n"
    "- Variatie is bewust: bied betekenisvol verschillende materialisaties "
    "(bijvoorbeeld warm/zacht versus strak/robuust), geen willekeurige ruis.\n"
    "- Onderbouwd en uitlegbaar; je STELT VOOR, je beslist niet.\n"
    "- Schrijf in helder Nederlands, zonder jargon, en zonder te verwijzen naar "
    "AI, modellen of techniek.\n\n"
    "Geef ALLEEN een JSON-array terug (geen uitleg, geen markdown) met 2 of 3 "
    "objecten, elk met:\n"
    "- 'materiaalsoort': bv. wol, wol-mix, polyamide, gerecycled PA;\n"
    "- 'structuur': bv. getuft dicht, geweven strak, laagpolig velours;\n"
    "- 'pooltype': bv. laagpolig, hoogpolig, vlak, bouclé;\n"
    "- 'tactiliteit': het gevoel onder de voet (optioneel);\n"
    "- 'uitstraling': hoe het oogt in de ruimte (optioneel);\n"
    "- 'motivering': waarom deze materialisatie technisch en qua beleving past, "
    "met de relevante afwegingen (gebruik, onderhoud, slijtvastheid, akoestiek, "
    "comfort, duurzaamheid, productie).\n\n"
    '[{"materiaalsoort": "...", "structuur": "...", "pooltype": "...", '
    '"tactiliteit": "...", "uitstraling": "...", "motivering": "..."}]'
)

_GEBRUIKER_SJABLOON = (
    "Bevestigd concept:\n"
    "- Stijlfamilie: {stijlfamilie}\n"
    "- Kleurpalet: {kleurpalet}\n"
    "- Complexiteit: {complexiteit}\n"
    "- Motiefschaal: {motiefschaal}\n\n"
    "Gekozen Floor Design (ontwerprichting):\n"
    "- {ontwerprichting}\n\n"
    "Bepaal 2 à 3 technisch verantwoorde materiaalvoorstellen die binnen dit "
    "concept en deze ontwerprichting blijven."
)

_INVOERVELDEN = ("stijlfamilie", "kleurpalet", "complexiteit", "motiefschaal", "ontwerprichting")


def _gebruikerprompt(invoer: dict) -> str:
    velden = {v: (str(invoer.get(v)).strip() if invoer.get(v) else "(niet opgegeven)")
              for v in _INVOERVELDEN}
    return _GEBRUIKER_SJABLOON.format(**velden)


def _json_uit_tekst(tekst: str):
    schoon = (tekst or "").strip().replace("```json", "").replace("```", "").strip()
    return json.loads(schoon)


def _normaliseer(data) -> Optional[list]:
    """Zet een modelantwoord (array of object) om naar een lijst downstream-veilige
    materiaalvoorstellen, of None wanneer onbruikbaar (→ terugval placeholder).
    Voorstellen die het concept verlaten worden geweerd."""
    if isinstance(data, dict):
        for sleutel in _LIJST_SLEUTELS:
            if isinstance(data.get(sleutel), list):
                data = data[sleutel]
                break
        else:
            data = [data] if data.get("materiaalsoort") else None
    if not isinstance(data, list):
        return None

    schoon: list = []
    for item in data:
        if not isinstance(item, dict) or item.get("verlaat_concept") is True:
            continue
        if any(not (isinstance(item.get(v), str) and item.get(v).strip()) for v in _VERPLICHT):
            continue
        voorstel = {v: item[v].strip() for v in _VERPLICHT}
        for v in _OPTIONEEL:
            if isinstance(item.get(v), str) and item.get(v).strip():
                voorstel[v] = item[v].strip()
        schoon.append(voorstel)
        if len(schoon) >= _MAX_VOORSTELLEN:
            break
    return schoon or None


class ProductieMateriaalReasoner:
    """Productie-implementatie van de Material Reasoning Boundary.

    Bouwt een op REASONING-001 gebaseerde opdracht bovenop het bevestigde concept
    en de gekozen ontwerprichting, laat het model één of meer technisch verantwoorde
    materialisaties bepalen via de abstracte `ModelClient`, en levert een lijst
    genormaliseerde, downstream-veilige voorstellen. Bij ELKE fout — netwerk,
    timeout, authenticatie, rate limiting, provider onbeschikbaar, of een
    onbruikbaar/leeg antwoord — valt zij GECONTROLEERD terug op de deterministische
    placeholder (exception-type-agnostisch), zodat het bestaande contract altijd
    geldig blijft en de gebruiker nooit een technische fout ziet
    (AB-012 / BUILD-023 R5).
    """

    def __init__(self, model_client: ModelClient) -> None:
        self._model = model_client

    def redeneer(self, invoer: dict) -> list:
        try:
            ruw = self._model.genereer(_SYSTEEM, _gebruikerprompt(invoer))
            voorstellen = _normaliseer(_json_uit_tekst(ruw))
            if not voorstellen:
                return placeholder_materiaal_generatie(invoer)
            return voorstellen
        except Exception:
            return placeholder_materiaal_generatie(invoer)


def maak_material_planning_redeneerfunctie(
    api_sleutel: str = "", modus: Optional[str] = None
) -> MateriaalRedeneerFunctie:
    """Configuratie-gestuurde keuze van de reasoning-client (hergebruikt de gedeelde
    IMP-015/016/017-factory): 'productie' mét serversleutel → productie-reasoner,
    anders de bestaande deterministische placeholder. Retourneert een
    `MateriaalRedeneerFunctie` (Callable[[dict], list]) voor injectie in de
    ongewijzigde `MaterialPlanner`."""
    return kies_redeneerfunctie(
        api_sleutel,
        placeholder_materiaal_generatie,
        # VAL-004: de materiaal-output (2-3 voorstellen met een afweging over
        # gebruik/onderhoud/slijtvastheid/akoestiek/comfort/duurzaamheid/productie)
        # is rijker dan de andere capabilities en overschrijdt de gedeelde default
        # max_tokens (600), wat de JSON afkapt -> parse-fout -> onterechte terugval.
        # Ruimere token-limiet voor deze capability; de gedeelde default en de
        # overige capabilities blijven ongewijzigd.
        lambda sl: ProductieMateriaalReasoner(AnthropicModelClient(sl, max_tokens=1500)).redeneer,
        modus,
    )
