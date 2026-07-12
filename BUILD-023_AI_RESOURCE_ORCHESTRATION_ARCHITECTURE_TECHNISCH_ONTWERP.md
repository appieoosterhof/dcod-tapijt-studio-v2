# BUILD-023 — AI Resource & Orchestration Architecture: technisch ontwerp

**Status:** technisch ontwerp, ter review (TR). Geen implementatie, geen code. Beschrijft uitsluitend **waar** de in BUILD-023 (functioneel) vastgelegde orkestratieregels landen en **hoe** ze worden afgedwongen — niet de regels zelf (die liggen vast in het functionele ontwerp). Geen nieuwe component, geen wijziging aan BUILD-007, aan de componentgrenzen of aan de reasoning-boundaries.

**Normatief:** BUILD-023 functioneel (AP-001; R1–R6), de bestaande `is_stale`-methoden en herkomst-referenties, de persistente `Gesprekstoestand` (BUILD-019/TD-008), de gates (BUILD-008), en AB-012 (AI-infra verborgen).

**Architectuurprincipe (technisch geborgd):** de orkestratie is een **beleids-/guardlaag in de integratielaag** (`design_brain_api.py`). Zij **beslist of** een boundary wordt aangeroepen; zij **wijzigt geen enkele boundary, component of laag**. De `Gesprekstoestand` is de cache; de bestaande herkomst + `is_stale` zijn de geldigheidstoets.

---

## 1. Plaats van de orchestrator

- **In de integratielaag, nergens anders.** De guards worden een dunne schil **rond de bestaande endpoint-bodies** in `design_brain_api.py`. De Design Brain-componenten (Reasoning Engine, planners, SVG Planner, FVE, DTP, Context Interpreter) blijven exact zoals ze zijn — zij worden aangeroepen óf overgeslagen, nooit aangepast.
- **Vorm:** één hulpfunctie die per stap bepaalt of er al een **geldig (niet-stale) resultaat** in de `Gesprekstoestand` staat. Zo ja → dat resultaat teruggeven (hergebruik); zo nee → de bestaande stap (gate + boundary) draaien en het resultaat opslaan. Geen nieuw domeinobject, geen nieuwe store.
- **Reikwijdte:** uitsluitend de reasoning-producerende endpoints (`/ontwerpstrategie`, `/concept`, `/floor-designs`, `/material-profiles`, `/pattern-profiles`, `/dialoog`) en de deterministische stappen (`/svg`, `/visualisatie`, `/transfer-package`). Bevestig-/navigatie-/leesendpoints raken nooit een boundary (R2) en behoeven geen guard.

## 2. Volgorde van de guards (R1–R6) per aanroep

Elke stap-endpoint doorloopt dezelfde vaste guard-volgorde:

1. **Geldig-resultaat-check (R1 + R6 idempotentie):** bestaat er in de `Gesprekstoestand` al een resultaat voor deze stap waarvan de **herkomst matcht** met de huidige bevestigde upstream (en dat niet *stale* is)? → **hergebruik**, retourneer het bestaande resultaat, **geen boundary-call**.
2. **Preconditie/gate (bestaand):** zo niet, toets de bestaande gate (bevestigde upstream). Niet voldaan → de bestaande, mensvriendelijke gate-uitkomst (R2: zicht/navigatie start niets).
3. **Nieuwe ontwerpwaarde (R1):** upstream bevestigd én geen geldig resultaat aanwezig → dít is een echte nieuwe/gewijzigde ontwerpbeslissing → roep de bestaande boundary aan en **cache** het resultaat in de `Gesprekstoestand`.
4. **Deterministisch werk (R3):** voor `/svg` en `/visualisatie` geldt hetzelfde patroon, maar de "boundary" is deterministisch; hergebruik het bewaarde artefact zolang de invoer ongewijzigd is (via `is_stale`), draai alleen bij wijziging.
5. **Gerichte invalidatie (R4):** een gewijzigde/opnieuw bevestigde upstream maakt via de herkomst-mismatch uitsluitend het geraakte downstream *stale*; niet-geraakte resultaten blijven geldig en worden hergebruikt.
6. **Falen (R5):** faalt een noodzakelijke nieuwe reasoning-aanroep, dan geldt de BUILD-023-R5-grens: is er een geldig resultaat → onzichtbaar hergebruiken; anders de neutrale AB-012-melding. Nooit een zichtbare limiet/teller.

## 3. Relatie met `is_stale`

De bestaande `is_stale`-methoden **zijn** de geldigheidstoets voor de deterministische downstream-resultaten; de guard hergebruikt ze onveranderd:
- `SVGResultaat` geldig ⇔ `not SVGPlanner.is_stale(svg, pattern_profile)`;
- `Visualisatie` geldig ⇔ `not FloorVisualizationEngine.is_stale(vis, svg)`;
- `DesignTransferPackage` geldig ⇔ `not DesignTransferPackageBuilder.is_stale(pkg, svg, vis)`.

Voor de **reasoning-resultaat-objecten buiten de DesignContext** (Floor Designs, Material/Pattern Profiles) — die geen eigen `is_stale`-methode hebben — geldt exact hetzelfde principe via een **herkomst-identifier-vergelijking**: het opgeslagen resultaat is geldig zolang zijn herkomst-identifier(s) overeenkomen met de actueel bevestigde upstream (§4).

**Nuance — laag-3/4 dragen géén upstream-herkomst.** De Ontwerpstrategie (laag 3) en het Concept (laag 4) leven *in* de DesignContext en bevatten geen herkomst-referentie naar hun upstream. Hun geldigheid is daarom **aanwezigheids-/statusgebaseerd**: is er al een voorgesteld/bevestigd resultaat, dan wordt dat hergebruikt en draait de reasoning niet opnieuw (dit sluit aan op de bestaande overwrite-guards in `OntwerpStrategieStap`/`ReasoningEngine`). De **herkomst-precieze** invalidatie (R4) geldt dus voor de resultaat-objecten buiten de DesignContext; voor laag 3/4 is de toets grover (presence/status). Dat is voldoende omdat laag 1 na bevestiging read-only is (BUILD-017) en strategie/concept vóór voortgang worden bevestigd — een fijnmaziger herkomst voor laag 3/4 zou een domeinmodel-uitbreiding zijn en valt buiten dit TD.

De integratielaag vat dit samen in één `_geldig(stap, toestand)`-toets die per stap óf de bestaande `is_stale` (result-objecten), óf de herkomst-vergelijking (Floor/Material/Pattern), óf de presence/status-toets (strategie/concept) gebruikt — géén nieuwe stale-logica in de componenten.

## 4. Relatie met herkomst / traceerbaarheid

De keten draagt de cache-sleutel **al**: elk resultaat bevat herkomst-referenties naar zijn bevestigde upstream. De guard vergelijkt die met de huidige bevestigde objecten:
- **Floor Designs** geldig ⇔ afgeleid van het huidige bevestigde Concept (`concept_herkomst` matcht);
- **Material Profile(s)** geldig ⇔ `floor_design_herkomst.identifier == toestand.floor_design.identifier` (en concept-herkomst matcht);
- **Pattern Profile(s)** geldig ⇔ `material_profile_herkomst.identifier == toestand.material_profile.identifier`;
- **SVG/Visualisatie/DTP** ⇔ via hun `is_stale` (§3).

Er wordt **geen nieuwe herkomst** geïntroduceerd; de bestaande traceerbaarheid is de invalidatiegrond.

## 5. Relatie met `Gesprekstoestand`

De persistente `Gesprekstoestand` (per `gesprek_id`, BUILD-019) **is de cache**: zij bewaart al `floor_designs/floor_design/material_profiles/material_profile/pattern_profiles/pattern_profile/svg_resultaat/visualisatie/pakket`. De guard **leest** deze om reuse-vs-recompute te bepalen en **schrijft** een nieuw resultaat terug op dezelfde plek. Geen extra store, geen extra serialisatie — het bestaande laden→muteren→opslaan (atomair) blijft ongewijzigd.

## 6. Idempotentie van requests

- **Herhaalde identieke acties** (dubbelklik, opnieuw bevestigen, opnieuw ophalen, opnieuw tonen) vallen in guard-stap 1 → hergebruik, **geen** boundary-call.
- **`/dialoog`:** alleen nieuwe/gewijzigde invoer start de Context Interpreter (R1); lege invoer draait sowieso geen interpretatie (bestaand gedrag). Snelle dubbele verzending van identieke tekst wordt al afgevangen door de bestaande **frontend in-flight-lock + debounce**; strikte backend-de-duplicatie van identieke opeenvolgende tekst is een optionele verfijning, geen vereiste van dit TD.
- **Concurrency:** het bestaande per-`gesprek_id`-slot (BUILD-019) serialiseert samenvallende verzoeken al; twee snelle identieke klikken produceren nooit twee aanroepen.

## 7. Cache-sleutels

De cache-sleutel per resultaat is **de herkomst zelf** — geen nieuw construct:

| Resultaat | Geldig zolang (cache-sleutel) |
|---|---|
| Ontwerpstrategie / Concept | **presence/status** (laag 3/4 dragen geen herkomst — §3): hergebruik zolang een voorgesteld/bevestigd resultaat bestaat |
| Floor Designs | `concept_herkomst` = huidig bevestigd Concept |
| Material Profile(s) | `floor_design_herkomst.identifier` = bevestigd Floor Design (+ concept) |
| Pattern Profile(s) | `material_profile_herkomst.identifier` = bevestigd Material Profile |
| SVGResultaat | `pattern_profile_herkomst.identifier` = bevestigd Pattern Profile (`is_stale`) |
| Visualisatie | `svgresultaat_herkomst.identifier` = huidig SVGResultaat **+ gekozen `scene_id`** |
| Design Transfer Package | SVGResultaat- én Visualisatie-identifier (`is_stale`) |

De Visualisatie-sleutel omvat expliciet de **`scene_id`**: een andere ruimte is een gewijzigde invoer (R3) en vraagt een nieuwe projectie, terwijl hetzelfde dessin wordt hergebruikt.

## 8. Architectuurgrenzen

- **Geen wijziging aan BUILD-007:** dezelfde ketenvolgorde en bevestigingsmomenten; de guards bepalen alleen *of* een stap rekent of hergebruikt.
- **Geen wijziging van componentgrenzen:** de guardlaag zit uitsluitend in `design_brain_api.py`; CP=laag 1, Context Interpreter=interpretatie, planners/RE/SVG/FVE/DTP=hun verantwoordelijkheid — allemaal onaangeroerd.
- **Geen wijziging van de reasoning-boundaries:** boundaries worden aangeroepen of overgeslagen; hun contract/gedrag blijft identiek. Toekomstige productie-boundaries erven de orkestratie automatisch.
- **AB-012:** de gehele guard-/cachelaag is en blijft onzichtbaar; geen "cache/call/budget" in beeld.
- **Additief:** de guards zijn een dunne toevoeging aan de bestaande endpoints; geen nieuw bestand nodig (mag als hulpfunctie in `design_brain_api.py`).

---

**Acceptatie:** de orkestratieregels R1–R6 worden afgedwongen als een dunne guardlaag in de integratielaag die, vóór elke stap, met de bestaande `is_stale`/herkomst-toets tegen de persistente `Gesprekstoestand` bepaalt of er een geldig resultaat is (hergebruik) dan wel een echte nieuwe ontwerpbeslissing nodig is (boundary-call + cache) — met de herkomst als cache-sleutel en het per-`gesprek_id`-slot voor idempotentie, zonder enige wijziging aan BUILD-007, de componentgrenzen of de reasoning-boundaries, en volledig onzichtbaar voor de gebruiker (AB-012).
