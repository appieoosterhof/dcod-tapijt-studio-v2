# BUILD-018 — Integratie SVG Planner ↔ bestaande generatiepipeline: technisch integratieontwerp

**Status:** technisch integratieontwerp, ter review. Geen programmacode, geen implementatie. Beschrijft uitsluitend **hoe** de placeholder-renderboundary van de SVG Planner wordt vervangen door de bestaande productiepipeline, **zonder architectuurwijziging**. Realiseert exact het slot dat AB-005/TD-004 al hadden voorzien ("de standaard omhult de bestaande pipeline … hier een deterministische placeholder voor test").

**Normatief:** AB-005 (SVG Planner = de bestaande pipeline), BUILD-014 + TD-004 (SVG Planner, injecteerbare `SVGRenderFunctie`), BUILD-015 + TD-005 (FVE — buiten scope, zie §1), en de bestaande live pipeline (`app.py`/`modules_extra.py`).

---

## 1. Inventarisatie (feitelijk, geverifieerd)

- **`STYLE_GENERATORS`** (`app.py:432`): dict met **29 stijl-sleutels** → generator-functies; enkele aliassen (`persian`, `classic` → `generate_medallion_svg`), dus ± **27 distinct** pure generators in `modules_extra.py`. Consistent met AB-005 F5.
- **`build_tile_svg(analysis, tile_size=400, motief_schaal=100, kleurpalet_override=None)`** (`app.py:465`): bouwt **één 400px-basistegel**. Kiest de stijl via `analysis["style"]` + keyword-routing op `analysis["_prompt"]`; leest `analysis["palette"]`, `["complexity"]`, `["shapes"]`, `["_tile_cm"]`; past motiefschaal toe via n×n-tegeling (n deler van 400); roept `STYLE_GENERATORS[style](palette, g, complexity)` aan. `kleurpalet_override` (BUILD-002) laat `DesignContext.concept.kleurpalet` de leidende palette zijn.
- **`build_repeat_svg(tile_svg, analysis, tile_cm, repeat_type, dpi, cols, rows, repeat_type_override=None)`** (`app.py:623`): stelt de tegel samen tot een **all-over repeat** (print/productie). Gebruikt `clipPath` (`id="canvas"`). `repeat_type_override` (BUILD-003) laat `productierealisatie.repeat_type` leiden.
- **Generatoren** (`modules_extra.py`): puur `generator(palette, tile_size, complexity[, …]) → SVG-string`. **Determinisme is gemengd:** sommige gebruiken een **vaste** seed (`random.Random(42)`, `random.Random(7)` → deterministisch), meerdere gebruiken **`seed=None`** → niet-deterministisch ("verrassing per klik": o.a. terrazzo, urban_plaid, aardlagen, vrije_vormen).
- **`svg_to_png()`** (`app.py:696`): STUB (retourneert het pad) — hoort bij de latere Productie Engine, buiten deze scope.
- **Koppelingen vanuit `app.py`:** `app = Flask(__name__)` op moduleniveau (`app.py:35`); de server start uitsluitend onder `if __name__ == "__main__"` (`app.py:1112`). De `api_key` wordt per request gelezen, **niet** bij import. De live route `/api/generate` gebruikt `analyse_prompt` → `build_tile_svg`/`build_repeat_svg`; deze flow blijft volledig ongemoeid.

**Scope-afbakening (FVE, BUILD-015/TD-005):** de FVE-placeholder (`placeholder_visualisatie`) omhult de **browser-JS-projectie** (`matrix3d`/`ROOM_MOCKUPS` in `static/js/app.js`) en is **niet** vervangbaar door deze Python-pipeline. De FVE blijft in deze fase ongewijzigd; dit ontwerp raakt uitsluitend de SVG Planner-renderboundary.

## 2. Welke placeholder wordt vervangen, door welke productiecode

- **Vervangen:** `placeholder_svg_rendering(invoer: dict) -> str` in `svg_planner.py` — de **default** van de injecteerbare `SVGRenderFunctie`.
- **Door:** een **productie-boundary** die de bestaande **`build_tile_svg(...)`** (+ `STYLE_GENERATORS` + de generators in `modules_extra.py`) omhult. Dit is een **boundary-implementatie**, geen nieuwe component en geen nieuwe verantwoordelijkheid (zie §4).
- **Niet in scope:** `build_repeat_svg` (all-over repeat = print/productie, latere Productie Engine) en `svg_to_png` (stub). De SVG Planner rendert de **tegel**; het herhaal-/printstuk blijft een aparte, latere stap.

## 3. Exacte parameterkoppeling

De SVG Planner levert de renderboundary een platte `invoer`-dict (`svg_planner._verzamel_render_invoer`). De productie-boundary mapt die naar de argumenten van `build_tile_svg`:

| `build_tile_svg`-parameter | Bron uit SVG Planner-`invoer` | Opmerking |
|---|---|---|
| `kleurpalet_override` | `invoer["kleurpalet"]` (Concept-kleurpalet) | **genormaliseerd** naar de vereiste keys (§5, R2) |
| `motief_schaal` (int %) | `invoer["motiefschaal"]` | label → % via een **vaste mapping** (§5, R4) |
| `analysis["style"]` | afgeleid uit `invoer["stijlfamilie"]`/`["motiefstructuur"]` | **vaste mapping** naar een `STYLE_GENERATORS`-sleutel; fallback `geometric` (§5, R3) |
| `analysis["complexity"]` | `invoer["complexiteit"]` | direct |
| `analysis["_prompt"]` | **leeg** (`""`) | bewust leeg om keyword-routing/­botsingen te vermijden (§5, R7); de stijl wordt expliciet via `style` gezet |
| `analysis["palette"]` | genormaliseerd Concept-kleurpalet (fallback) | dient als fallback naast `kleurpalet_override` |
| `analysis["shapes"]` | `[]` | geen shape-sturing vanuit de Design Brain |
| `tile_size` | `400` (default) | naadloze-tegeling-conventie |

De boundary retourneert de `build_tile_svg`-string ongewijzigd; de SVG Planner valideert die met zijn bestaande `_valideer_svg` (`<svg …>…</svg>`).

## 4. Eigenaarschap

- **Eigenaar blijft de SVG Planner** (uitvoerende renderer, AB-005/AR-004/AR-005). De bestaande pipeline **ís** de SVG Planner-implementatie die AB-005 formeel erkent; hem injecteren als boundary bevestigt dat eigenaarschap, het verplaatst het niet.
- De **productie-boundary is een boundary-implementatie**, geen component: zij heeft geen eigen toestand, neemt geen beslissing en draagt geen ontwerpautoriteit — zij mapt parameters en delegeert aan `build_tile_svg`. Exact het injectiepunt dat TD-004 §8 al beschreef.
- Ontwerpautoriteit blijft volledig vóór de SVG Planner (Reasoning Engine/Material/Pattern Planner).

## 5. Risico's

- **R1 — Determinisme-conflict (primair).** TD-004 borgt dat de SVG Planner-rendering deterministisch is. Meerdere productie-generatoren zijn echter bewust **niet-deterministisch** (`seed=None`, "verrassing per klik"), en `build_tile_svg` geeft geen seed door. Zónder wijziging aan `build_tile_svg`/`app.py` (buiten scope) is volledige determinisme voor die stijlen niet af te dwingen.
  - **Implementeerbare basislijn (vastgelegd):** de **eerste integratie omvat uitsluitend de deterministische (vaste-seed) stijlen** — daarvoor blijft TD-004's determinisme volledig gelden en is geen beslissing nodig. De productie-boundary weigert (valt terug op de placeholder of signaleert) voor stijlen die niet in de deterministische basislijn zitten.
  - **Uitbreiding — gegate't op architect-akkoord:** de niet-deterministische (`seed=None`) stijlen kunnen pas worden meegenomen na een **expliciet architect-akkoord** dat de bewust-variabele pipeline-uitvoer ("verrassing per klik") als productgedrag aanvaardt. Dat relaxeert TD-004's determinisme uitsluitend voor de productie-boundary (de SVG Planner-logica + placeholder blijven deterministisch) en vraagt geen architectuurwijziging. Ik stel dit niet zelf vast (§9).
- **R2 — Palette-keys.** Diverse generatoren en `build_tile_svg` (`palette['background']`) spreken keys **hard** aan (`background/primary/secondary/accent1/accent2`); een Concept-kleurpalet zonder die keys → `KeyError`. **Mitigatie:** de boundary **normaliseert** het Concept-kleurpalet naar de vereiste keys (ontbrekende uit de bestaande default aanvullen) vóór aanroep.
- **R3 — Stijl-mapping.** `stijlfamilie`/`motiefstructuur` (Design Brain-vocabulaire) is **niet 1:1** met de 29 `STYLE_GENERATORS`-sleutels. **Mitigatie:** een expliciete, vaste mapping met `geometric` als veilige fallback; onbekende families → fallback (getest, R-tests).
- **R4 — Motiefschaal.** `pattern_profile.motiefschaal` kan een label zijn ("groot/fijn"); `build_tile_svg` verwacht een int-percentage. **Mitigatie:** vaste label→%-mapping.
- **R5 — Import-neveneffect.** Het importeren van `build_tile_svg` uit `app.py` instantieert de Flask-app (`app.py:35`). De server start niet (guarded). **Mitigatie:** `build_tile_svg` **lui** importeren *binnen* de boundary-functie (niet op moduleniveau), zodat `app.py` pas bij de eerste render wordt geladen en het importeren van de adapter zelf geen Flask-instantiatie veroorzaakt. Geen refactor van `app.py` (buiten scope).
- **R6 — `clipPath` in de tegel.** De CLAUDE.md-valkuil: `clipPath` breekt in een base64-`<img>` (de FVE laadt de SVG zo). `build_repeat_svg` gebruikt `clipPath` — die is buiten scope; maar een enkele **generator** kan intern `clipPath` in de tegel zetten. **Mitigatie:** R-test die per stijl controleert dat de tegel geen `clipPath` bevat (of dat de FVE-projectie die stijl verdraagt).
- **R7 — Keyword-routing-botsing.** `build_tile_svg` routeert mede op `analysis["_prompt"]`; een gevulde `_prompt` kan de expliciete stijl overschrijven (bekende valkuil). **Mitigatie:** `_prompt` leeg laten en de stijl uitsluitend via `analysis["style"]` zetten.

## 6. Welke bestanden gewijzigd moeten worden / expliciet ongewijzigd blijven

**Te wijzigen:** in principe **geen bestaand bestand**. De integratie is een **injectie**: `SVGPlanner(render=<productie-boundary>)`. De boundary zelf komt in **één nieuw, dun bestand** (bijv. `svg_planner_pipeline.py`) dat `build_tile_svg` importeert en de mapping/normalisatie uit §3/§5 uitvoert. Er is nog **geen** live aanroepsite van de SVG Planner (de keten is bewust losstaand), dus er hoeft geen bestaande call-site te worden aangepast.

**Expliciet ongewijzigd:**
- `svg_planner.py` (de boundary is al injecteerbaar — geen wijziging nodig);
- `app.py` en `modules_extra.py` (`build_tile_svg`/`build_repeat_svg`/generatoren read-only hergebruikt);
- `design_context.py`, de planners, `floor_visualization_engine.py`, `design_transfer_package.py`, `conversation_planner.py`;
- de live route `/api/generate` en de bestaande render-/mockup-flow.

## 7. Noodzakelijke regressietesten

1. **SVG Planner-contract intact:** met de productie-boundary geïnjecteerd blijven gate, `_valideer_svg`, stale-detectie en de resultaatwikkel werken; elke ondersteunde stijl levert een welgevormde `<svg…>…</svg>`-tegel.
2. **Palette-normalisatie:** een Concept-kleurpalet zónder `background/…` leidt **niet** tot `KeyError` (R2).
3. **Stijl-mapping:** bekende families mappen naar de juiste generator; onbekende → `geometric` (R3).
4. **Motiefschaal-mapping:** labels → geldige int-% en een naadloze tegel (R4).
5. **Determinisme (basislijn):** de vaste-seed-stijlen leveren bij gelijke invoer een **identieke** SVG (TD-004-contract). Stijlen buiten de deterministische basislijn worden door de boundary geweigerd/teruggevallen (R1) totdat het architect-akkoord er is.
6. **Geen `clipPath` in de tegel** per ondersteunde stijl (R6).
7. **Live pipeline onaangetast:** `/api/generate` en `build_tile_svg`/`build_repeat_svg` gedragen zich ongewijzigd (geen bestand gewijzigd).
8. **FVE/DTP/keten-regressie:** de bestaande end-to-end ketentest (OntwerpVisie → DTP) blijft slagen met de productie-boundary.

## 8. Consistentietoets

- **AB-005:** ✔ dit realiseert de erkenning — de bestaande pipeline wordt de feitelijke SVG Planner-renderboundary; geen naams-/rolwijziging.
- **BUILD-014 / TD-004:** ✔ gebruikt exact het injectieslot (`SVGRenderFunctie`) dat TD-004 §8 beschreef; **`svg_planner.py` wordt niet gewijzigd**. Op de deterministische basislijn blijft TD-004's determinisme volledig gelden; alleen de uitbreiding naar variabele stijlen vraagt de architect-beslissing (R1/§9).
- **BUILD-015 / TD-005:** ✔ de FVE blijft ongewijzigd en buiten scope (browser-JS-projectie).
- **Live pipeline:** ✔ geen wijziging aan `app.py`/`modules_extra.py`/routes; `build_tile_svg`/`build_repeat_svg` read-only hergebruikt.
- **Geen nieuwe architectuur/component/verantwoordelijkheid:** ✔ uitsluitend een boundary-implementatie in de reeds bestaande injectieslot.

## 9. Architectuurbewaking (ter attentie van de TR/architect)

1. **Determinisme (R1) — basislijn vastgelegd, uitbreiding vraagt beslissing.** De implementeerbare basislijn is vastgelegd op de **deterministische (vaste-seed) stijlen** (geen beslissing nodig; TD-004-determinisme blijft gelden). Het **uitbreiden** naar de bewust-variabele stijlen ("verrassing per klik") vraagt een expliciet architect-akkoord dat dat productgedrag aanvaardt — geen architectuurwijziging, maar een bewuste keuze die ik niet zelf vaststel.
2. **Boundary-implementatie, geen component.** De adapter mapt/normaliseert en delegeert; geen toestand, geen ontwerpautoriteit. Blijft binnen het injectiemodel van TD-004.
3. **Import-afhankelijkheid (R5).** De boundary importeert uit `app.py` (Flask-instantiatie als neveneffect). Aanvaard als integratiedetail; geen refactor van `app.py` in deze scope.

---

**Reviewgereed:** dit ontwerp beschrijft uitsluitend de vervanging van de SVG Planner-placeholder door de bestaande productiepipeline via de reeds bestaande injecteerbare boundary, met exacte parameterkoppeling, ongewijzigd eigenaarschap, de te (on)wijzigen bestanden, de risico's (met determinisme als hoofdpunt) en de noodzakelijke regressietesten — zonder architectuurwijziging, nieuwe component of nieuwe verantwoordelijkheid, en zonder implementatie.
