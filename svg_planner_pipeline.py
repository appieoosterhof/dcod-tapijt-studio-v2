"""
BUILD-018 -- Integratie SVG Planner <-> bestaande generatiepipeline.

Dunne BOUNDARY-IMPLEMENTATIE (geen component, geen ontwerpautoriteit) die de
placeholder-renderboundary van de SVG Planner vervangt door de bestaande
productiepipeline `build_tile_svg` (+ STYLE_GENERATORS + de generators in
modules_extra.py, AB-005). Realiseert exact het injecteerbare `SVGRenderFunctie`-
slot dat TD-004 §8 al beschreef; `svg_planner.py`, `app.py` en `modules_extra.py`
blijven ONGEWIJZIGD.

Conform BUILD-018 (IMP-009, deterministische basislijn):
  * uitsluitend de DETERMINISTISCHE (empirisch geverifieerde) stijlen; niet-
    deterministische stijlen (seed=None: aardlagen, japandi, lijnenspel,
    prism_overlay, vrije_vormen) vallen buiten de basislijn en worden vervangen
    door de deterministische fallback (geometric) -- de uitbreiding daarnaar is
    in BUILD-018 §9 gegate't op een expliciet architect-akkoord;
  * gebruikt `build_tile_svg` (de TEGEL); GEEN `build_repeat_svg`, GEEN
    `svg_to_png` (Productie Engine, buiten scope);
  * `build_tile_svg` wordt LUI (lazy) geimporteerd binnen de boundary, zodat het
    importeren van deze adapter geen Flask-instantiatie veroorzaakt (R5);
  * palette-normalisatie (R2), stijl-mapping (R3), motiefschaal-mapping (R4) en
    een leeg `_prompt` om keyword-routing-botsingen te vermijden (R7).

De boundary is deterministisch en AI-model-onafhankelijk: gelijke invoer levert
exact dezelfde SVG.
"""

from __future__ import annotations

from typing import Optional

from svg_planner import SVGPlanner, SVGRenderFunctie


# ─── Deterministische basislijn (BUILD-018 R1, empirisch geverifieerd) ────────
# Stabiel bevonden over meerdere paletten/schalen/herhalingen.
DETERMINISTISCHE_STIJLEN: frozenset[str] = frozenset({
    "art_deco", "art_deco_hex", "art_deco_waaier", "bamboe", "bauhaus",
    "botanical", "chevron", "chevron_bold", "classic", "diamant", "dots",
    "floral", "geometric", "hexagon", "hoogtelijnen", "houndstooth", "knitwerk",
    "medallion", "mozaiek", "ogee", "persian", "strepen", "terrazzo",
    "urban_plaid",
})

# Bekende, bewust NIET-deterministische stijlen ("verrassing per klik",
# seed=None). Buiten de basislijn: de boundary SIGNALEERT hiervoor (BUILD-018 R1)
# i.p.v. stil te renderen -- uitbreiding hierheen is gegate't op architect-akkoord.
NIET_DETERMINISTISCHE_STIJLEN: frozenset[str] = frozenset({
    "aardlagen", "japandi", "lijnenspel", "prism_overlay", "vrije_vormen",
})

_ALLE_BEKENDE_STIJLEN: frozenset[str] = DETERMINISTISCHE_STIJLEN | NIET_DETERMINISTISCHE_STIJLEN

# Veilige deterministische fallback voor ECHT ONBEKENDE families (BUILD-018 R3).
FALLBACK_STIJL = "geometric"


# ─── Stijl-mapping: Design Brain-stijlfamilie -> STYLE_GENERATORS-sleutel (R3) ─
_STIJL_SYNONIEMEN: dict[str, str] = {
    "geometrisch": "geometric", "geometric": "geometric",
    "art deco": "art_deco", "artdeco": "art_deco", "art_deco": "art_deco",
    "bauhaus": "bauhaus",
    "bloemen": "floral", "floraal": "floral", "floral": "floral", "bloemrijk": "floral",
    "botanisch": "botanical", "botanical": "botanical", "planten": "botanical",
    "perzisch": "persian", "persian": "persian", "oosters": "persian",
    "klassiek": "classic", "classic": "classic",
    "medaillon": "medallion", "medallion": "medallion",
    "chevron": "chevron", "zigzag": "chevron", "visgraat": "chevron",
    "chevron_bold": "chevron_bold",
    "strepen": "strepen", "gestreept": "strepen",
    "mozaiek": "mozaiek", "mozaïek": "mozaiek",
    "hexagon": "hexagon", "zeshoek": "hexagon", "honingraat": "hexagon",
    "houndstooth": "houndstooth", "pied-de-poule": "houndstooth", "hanenpoot": "houndstooth",
    "ogee": "ogee",
    "diamant": "diamant", "ruit": "diamant", "ruiten": "diamant",
    "terrazzo": "terrazzo",
    "dots": "dots", "stippen": "dots",
    "hoogtelijnen": "hoogtelijnen", "topografie": "hoogtelijnen", "contour": "hoogtelijnen",
    "knitwerk": "knitwerk", "gebreid": "knitwerk", "nordic": "knitwerk", "scandinavisch": "knitwerk",
    "bamboe": "bamboe",
    "urban plaid": "urban_plaid", "urban_plaid": "urban_plaid", "plaid": "urban_plaid",
    "tartan": "urban_plaid", "ruitpatroon": "urban_plaid",
    "art_deco_hex": "art_deco_hex", "art_deco_waaier": "art_deco_waaier",
}


def _resolveer_stijl(stijlfamilie, motiefstructuur) -> Optional[str]:
    """Mapt de Design Brain-stijlfamilie (met motiefstructuur als tweede hint)
    naar een BEKENDE STYLE_GENERATORS-sleutel (deterministisch óf niet), of `None`
    wanneer niets herkend wordt. De classificatie/fallback gebeurt in de boundary
    (R1 vs R3)."""
    for bron in (stijlfamilie, motiefstructuur):
        if not isinstance(bron, str) or not bron.strip():
            continue
        sleutel = bron.strip().lower()
        if sleutel in _ALLE_BEKENDE_STIJLEN:
            return sleutel
        kandidaat = _STIJL_SYNONIEMEN.get(sleutel)
        if kandidaat:
            return kandidaat
    return None


# ─── Palette-normalisatie (R2) ────────────────────────────────────────────────
_DEFAULT_PALETTE: dict[str, str] = {
    "background": "#F5E6D3", "primary": "#C4753A", "secondary": "#8B4513",
    "accent1": "#D4A055", "accent2": "#F0C080",
}
_PALETTE_SYNONIEMEN: dict[str, str] = {"achtergrond": "background", "voorgrond": "primary"}


def _normaliseer_palette(kleurpalet) -> dict[str, str]:
    """Zorgt dat de vereiste keys (background/primary/secondary/accent1/accent2)
    aanwezig zijn -- ontbrekende worden aangevuld uit de bestaande default --
    zodat generatoren die keys hard aanspreken geen KeyError geven (R2)."""
    genormaliseerd = dict(_DEFAULT_PALETTE)
    if isinstance(kleurpalet, dict):
        for k, v in kleurpalet.items():
            sleutel = _PALETTE_SYNONIEMEN.get(k, k)
            if sleutel in _DEFAULT_PALETTE and v:
                genormaliseerd[sleutel] = v
    return genormaliseerd


# ─── Motiefschaal-mapping: label -> int-percentage (R4) ───────────────────────
_MOTIEFSCHAAL_MAPPING: dict[str, int] = {
    "fijn": 50, "klein": 50, "fine": 50, "smal": 50,
    "normaal": 100, "gemiddeld": 100, "medium": 100, "normal": 100,
    "groot": 200, "grof": 200, "large": 200, "breed": 200,
}


def _bepaal_motiefschaal(motiefschaal) -> int:
    """Mapt een motiefschaal-label of getal naar een int-percentage voor
    `build_tile_svg`; default 100 (R4)."""
    if isinstance(motiefschaal, bool):
        return 100
    if isinstance(motiefschaal, (int, float)):
        return max(int(motiefschaal), 10)
    if isinstance(motiefschaal, str):
        s = motiefschaal.strip().lower()
        if s in _MOTIEFSCHAAL_MAPPING:
            return _MOTIEFSCHAAL_MAPPING[s]
        if s.isdigit():
            return max(int(s), 10)
    return 100


# ─── Productie-boundary (vervangt placeholder_svg_rendering) ──────────────────
def pipeline_svg_rendering(invoer: dict) -> str:
    """Deterministische productie-implementatie van de `SVGRenderFunctie`.

    Mapt de platte SVG Planner-invoer naar de argumenten van `build_tile_svg`
    (de bestaande pipeline, AB-005) en retourneert de gerenderde 400px-TEGEL.
    Geen ontwerpkeuze, geen toestand: puur mappen/normaliseren en delegeren.
    """
    # Lui importeren: pas hier wordt app.py (Flask) geladen (R5).
    from app import build_tile_svg

    kandidaat = _resolveer_stijl(invoer.get("stijlfamilie"), invoer.get("motiefstructuur"))
    if kandidaat in NIET_DETERMINISTISCHE_STIJLEN:
        # Bekende maar bewust niet-deterministische stijl: signaleer i.p.v.
        # renderen (BUILD-018 R1; placeholder is uit het actieve pad). De
        # SVG Planner vangt dit op als foutresultaat.
        raise ValueError(
            f"Stijl '{kandidaat}' valt buiten de deterministische basislijn "
            "(BUILD-018 R1); uitbreiding vereist een expliciet architect-akkoord."
        )
    # Bekende deterministische stijl gebruiken; echt onbekende family -> geometric (R3).
    stijl = kandidaat if kandidaat in DETERMINISTISCHE_STIJLEN else FALLBACK_STIJL
    palette = _normaliseer_palette(invoer.get("kleurpalet"))
    motief_schaal = _bepaal_motiefschaal(invoer.get("motiefschaal"))
    complexity = invoer.get("complexiteit") or "medium"

    analysis = {
        "style": stijl,
        "_prompt": "",          # leeg: vermijdt keyword-routing-botsingen (R7)
        "palette": dict(palette),
        "complexity": complexity,
        "shapes": [],
    }
    # kleurpalet_override laat het (genormaliseerde) Concept-kleurpalet leiden.
    return build_tile_svg(analysis, tile_size=400, motief_schaal=motief_schaal,
                          kleurpalet_override=dict(palette))


def maak_svg_planner(render: SVGRenderFunctie = pipeline_svg_rendering) -> SVGPlanner:
    """Fabrieksfunctie die de SVG Planner met de PRODUCTIE-boundary bedraadt.

    Hiermee is de placeholder-rendering volledig uit het actieve pad: het actieve
    pad construeert de SVG Planner via deze fabriek, die standaard de
    `pipeline_svg_rendering`-boundary injecteert. De injecteerbare
    `SVGRenderFunctie` (en de placeholder als test-default in svg_planner.py)
    blijven ongewijzigd behouden.
    """
    return SVGPlanner(render=render)
