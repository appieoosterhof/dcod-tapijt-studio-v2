"""
conceptvorming_capability.py — Productie Reasoning Capability: Conceptvorming (IMP-016).

Tweede productie-Reasoning Capability, exact volgens het bewezen IMP-015-patroon.
Vervangt UITSLUITEND de deterministische placeholder achter de reeds bestaande
Concept-boundary (BUILD-010, Reasoning Engine Fase 1:
`RedeneerFunctie = Callable[[dict], dict]`, contract
`{"stijlfamilie", "kleurpalet", "complexiteit", "motiefschaal"}` (+ optioneel
`motivering`)). De boundary, het contract, het Concept-resultaatobject (laag 4),
de orchestrator, de guards, de cache/invalidatie en de DesignContext blijven
volledig ongewijzigd; deze module levert enkel een andere injecteerbare
redeneerfunctie.

Bouwt logisch voort op de reeds gevalideerde Ontwerpstrategie (laag 3): de
strategie (`aanpak`/`onderbouwing`) wordt als kader meegegeven. De capability
redeneert op REASONING-001 en kent GEEN HTTP, opslag, sessies, DesignContext of
orchestratie, en GEEN leveranciersspecifieke logica — uitsluitend de abstracte
`ModelClient` (reasoning_client.py). Provider-/modusselectie, fallback en
foutafhandeling worden hergebruikt uit IMP-015.

Downstream-veiligheid (regressie): `complexiteit` wordt genormaliseerd naar
{low, medium, high} (waarop `build_tile_svg` vertakt) en `motiefschaal` naar
{klein, gemiddeld, groot} (die de SVG-pipeline-adapter mapt naar 50/100/200).
Bij welke productiefout of onbruikbaar antwoord dan ook valt de capability
gecontroleerd terug op de deterministische placeholder — het bestaande contract
blijft altijd geldig, en de gebruiker ziet nooit een technische melding (AB-012).
"""

from __future__ import annotations

from typing import Optional

from reasoning_client import (
    AnthropicModelClient,
    ModelClient,
    extraheer_json,
    kies_redeneerfunctie,
)
from reasoning_engine import RedeneerFunctie, placeholder_conceptvorming

# Downstream-vocabulaire (zie svg_planner_pipeline / app.build_tile_svg).
_COMPLEXITEIT = {"low", "medium", "high"}
_COMPLEXITEIT_SYN = {
    "low": "low", "laag": "low", "eenvoudig": "low", "minimaal": "low",
    "medium": "medium", "gemiddeld": "medium", "middel": "medium", "normaal": "medium",
    "high": "high", "hoog": "high", "complex": "high", "rijk": "high",
}
_MOTIEFSCHAAL = {"klein", "gemiddeld", "groot"}
_MOTIEFSCHAAL_SYN = {
    "klein": "klein", "fijn": "klein", "smal": "klein", "small": "klein", "fine": "klein",
    "gemiddeld": "gemiddeld", "normaal": "gemiddeld", "medium": "gemiddeld", "normal": "gemiddeld",
    "groot": "groot", "grof": "groot", "large": "groot", "breed": "groot",
}

_SYSTEEM = (
    "Je bent de ontwerpredenering van DCOD, een studio voor vloerontwerp "
    "(printtapijt) voor architecten en interieurontwerpers. Op basis van de reeds "
    "vastgestelde ONTWERPSTRATEGIE bepaal je nu het CONCEPT: de concrete, maar nog "
    "voorgestelde ontwerprichting van de vloer.\n\n"
    "Ontwerpfilosofie (leidend):\n"
    "- Een vloer is een dragend, dienend ontwerpelement: hij ondersteunt de "
    "architectuur, versterkt de functie en maakt het verhaal van de ruimte "
    "compleet — hij is niet het verhaal zelf.\n"
    "- Het concept moet logisch voortbouwen op de ontwerpstrategie; het mag die "
    "niet tegenspreken.\n"
    "- Weeg de ontwerpfactoren in samenhang: functie en gebruik, doelgroep, sfeer "
    "en identiteit, licht, en de randvoorwaarden onderhoud, akoestiek, "
    "duurzaamheid, budget en productie.\n"
    "- Onderbouwd en uitlegbaar, geen willekeur; je STELT VOOR, je beslist niet.\n"
    "- Schrijf in helder Nederlands, zonder jargon, en zonder te verwijzen naar "
    "AI, modellen of techniek.\n\n"
    "Bepaal exact deze velden:\n"
    "- 'stijlfamilie': een korte, herkenbare naam voor de ontwerprichting van de "
    "vloer (bv. 'ingetogen geometrisch', 'organisch natuurlijk').\n"
    "- 'kleurpalet': een JSON-object met minimaal 'achtergrond' en 'primary', elk "
    "een hexkleur (bijvoorbeeld '#f5f5f0').\n"
    "- 'complexiteit': EXACT één van: 'low', 'medium', 'high'.\n"
    "- 'motiefschaal': EXACT één van: 'klein', 'gemiddeld', 'groot'.\n"
    "- 'motivering': 2–4 zinnen die uitleggen waarom dit concept past bij de "
    "strategie en de context.\n\n"
    "Geef ALLEEN een JSON-object terug (geen uitleg, geen markdown):\n"
    '{"stijlfamilie": "...", "kleurpalet": {"achtergrond": "#......", '
    '"primary": "#......"}, "complexiteit": "low|medium|high", '
    '"motiefschaal": "klein|gemiddeld|groot", "motivering": "..."}'
)

_GEBRUIKER_SJABLOON = (
    "Reeds vastgestelde ontwerpstrategie:\n"
    "- Aanpak: {aanpak}\n"
    "- Onderbouwing: {onderbouwing}\n\n"
    "Context voor deze ontwerpopdracht:\n"
    "- Vrije omschrijving: {vrije_tekst}\n"
    "- Gewenste sfeer/beleving: {sfeer}\n"
    "- Gewenste identiteit: {gewenste_identiteit}\n"
    "- Ontwerpambitie: {ontwerpambitie}\n"
    "- Projecttype: {projecttype}\n"
    "- Ruimtetype: {ruimtetype}\n"
    "- Doelgroep: {doelgroep}\n"
    "- Gebruikscontext: {gebruikscontext}\n\n"
    "Bepaal op basis hiervan het concept."
)

_INVOERVELDEN = (
    "aanpak", "onderbouwing", "vrije_tekst", "sfeer", "gewenste_identiteit",
    "ontwerpambitie", "projecttype", "ruimtetype", "doelgroep", "gebruikscontext",
)


def _gebruikerprompt(invoer: dict) -> str:
    velden = {v: (str(invoer.get(v)).strip() if invoer.get(v) else "(niet opgegeven)")
              for v in _INVOERVELDEN}
    return _GEBRUIKER_SJABLOON.format(**velden)


def _hex(waarde) -> bool:
    return (isinstance(waarde, str) and waarde.startswith("#")
            and len(waarde) in (4, 7))


def _normaliseer(data: dict) -> Optional[dict]:
    """Zet een modelantwoord om naar een geldig, downstream-veilig Concept-
    voorstel, of geeft None wanneer het onbruikbaar is (→ terugval placeholder).
    """
    if not isinstance(data, dict):
        return None
    stijl = (data.get("stijlfamilie") or "").strip() if isinstance(data.get("stijlfamilie"), str) else ""
    palet = data.get("kleurpalet")
    if isinstance(palet, dict):
        palet = {("achtergrond" if k in ("achtergrond", "background") else
                  "primary" if k in ("primary", "voorgrond") else k): v
                 for k, v in palet.items()}
    compl = _COMPLEXITEIT_SYN.get(str(data.get("complexiteit", "")).strip().lower())
    schaal = _MOTIEFSCHAAL_SYN.get(str(data.get("motiefschaal", "")).strip().lower())

    if not stijl or not isinstance(palet, dict):
        return None
    if not (_hex(palet.get("achtergrond")) and _hex(palet.get("primary"))):
        return None
    if compl not in _COMPLEXITEIT or schaal not in _MOTIEFSCHAAL:
        return None

    voorstel = {
        "stijlfamilie": stijl,
        "kleurpalet": {"achtergrond": palet["achtergrond"], "primary": palet["primary"]},
        "complexiteit": compl,
        "motiefschaal": schaal,
    }
    motivering = data.get("motivering")
    if isinstance(motivering, str) and motivering.strip():
        voorstel["motivering"] = motivering.strip()
    return voorstel


class ProductieConceptReasoner:
    """Productie-implementatie van de Concept-reasoning boundary (Fase 1).

    Bouwt een op REASONING-001 gebaseerde opdracht bovenop de vastgestelde
    ontwerpstrategie, laat het model redeneren via de abstracte `ModelClient`, en
    levert een genormaliseerd, downstream-veilig Concept-voorstel. Bij ELKE fout
    — netwerk, timeout, authenticatie, rate limiting, provider onbeschikbaar, of
    een onvolledig/ongeldig antwoord — valt zij GECONTROLEERD terug op de
    deterministische placeholder (exception-type-agnostisch), zodat het bestaande
    contract altijd geldig blijft en de gebruiker nooit een technische fout ziet
    (AB-012 / BUILD-023 R5).
    """

    def __init__(self, model_client: ModelClient) -> None:
        self._model = model_client

    def redeneer(self, invoer: dict) -> dict:
        try:
            ruw = self._model.genereer(_SYSTEEM, _gebruikerprompt(invoer))
            voorstel = _normaliseer(extraheer_json(ruw))
            if voorstel is None:
                return placeholder_conceptvorming(invoer)
            return voorstel
        except Exception:
            return placeholder_conceptvorming(invoer)


def maak_conceptvorming_redeneerfunctie(
    api_sleutel: str = "", modus: Optional[str] = None
) -> RedeneerFunctie:
    """Configuratie-gestuurde keuze van de reasoning-client (hergebruikt de
    gedeelde IMP-015-factory): 'productie' mét serversleutel → productie-reasoner,
    anders de bestaande deterministische placeholder. Retourneert een
    `RedeneerFunctie` (Callable[[dict], dict]) voor injectie in de ongewijzigde
    `ReasoningEngine`."""
    return kies_redeneerfunctie(
        api_sleutel,
        placeholder_conceptvorming,
        lambda sl: ProductieConceptReasoner(AnthropicModelClient(sl)).redeneer,
        modus,
    )
