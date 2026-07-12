# BUILD-019 — Integratie Design Brain in de bestaande Flask-app: functioneel ontwerp

> **Geamendeerd door BUILD-020**: de workflow omvat vóór het Concept ook de **laag-2-projectie** (Project-/Ruimtecontext, via de Context Interpreter) en de **Ontwerpstrategie-stap** (laag 3, BUILD-009) — beide reeds bestaande componenten, uitsluitend georkestreerd. Zie `BUILD-020_TD-008_AMENDEMENT_LAAG2_ONTWERPSTRATEGIE.md`.

**Status:** functioneel ontwerp, gereed voor architectuurreview (VR). Beschrijft uitsluitend **wat** de integratie doet, niet **hoe**. Geen nieuwe architectuurcomponent — een **dunne, additieve ontsluitingslaag** (HTTP-endpoints) die de reeds bestaande Design Brain-componenten aanstuurt. Verankerd in BUILD-007 (de toekomstige workflow), BUILD-017 (Conversation Planner) en BUILD-018 (SVG Planner ↔ productiepipeline).

**Uitgangspunt:** de volledige Design Brain-keten (Conversation Planner → Context Interpreter → Reasoning Engine → Material Planner → Pattern Planner → SVG Planner (productiepipeline) → Floor Visualization Engine → Design Transfer Package) bestaat, is gereviewd en losstaand geborgd, maar is **nog niet ontsloten** in de app. BUILD-019 ontsluit die keten als een **tweede, additieve ingang** ("Ontwerp zelf met AI", `CLAUDE.md`), **náást** de ongewijzigde bestaande `/api/generate`-Dessinator.

---

## Inventarisatie van de huidige workflow (feitelijk)

- **Bestaande routes** (`app.py`): `/`, `/inspiratie`, `/scene-builder`; `/api/scenes` (GET/POST), `/api/scenes/<id>` (GET), `/api/scenes/<id>/calibratie` (POST); `/api/generate` (POST); `/api/refine` (POST); `/api/export/svg`, `/api/export/png` (POST); `/api/bestelling` (POST).
- **`/api/generate`-flow:** request (prompt, api_key, tile_cm, repeat_type, dpi, direct-modus, aangepast_palet) → `analyse_prompt` (AI) óf direct-modus → keyword-routing op `analysis["style"]` → een **lichtgewicht DesignContext** (`design_context.bouw_context_uit_request` + `vergelijk_met_analysis`, BUILD-001/002/003) levert `kleurpalet_override` (concept.kleurpalet) en `repeat_type_override` → `build_tile_svg` → `build_repeat_svg` → base64 → JSON. De DesignContext-stap is in `try/except` gehuld zodat een fout de Dessinator **nooit** breekt (terugval op `None`).
- **Bestaande chat-/generate-workflow:** één request = één volledige generatie; **stateless** per request (de DesignContext wordt per request opgebouwd, niet vastgehouden).
- **Bestaande Scene Builder** (BUILD-006): `/api/scenes`-routes leveren `Scene`-objecten met gekalibreerd vloerpolygon.
- **Bestaande SVG-productiepipeline:** `build_tile_svg`/`build_repeat_svg` + `STYLE_GENERATORS`; de SVG Planner-component omhult `build_tile_svg` via de BUILD-018-adapter.
- **Constatering:** de huidige app gebruikt reeds een *lichtgewicht* DesignContext (uitsluitend voor twee overrides); de *volledige* Design Brain-keten (RE/MP/PP/SVG-component/FVE/DTP) wordt nog nergens aangeroepen.

## 1. Plaats van de integratie

Een **dunne ontsluitingslaag** binnen de bestaande Flask-app: nieuwe, additieve HTTP-endpoints die de bestaande Design Brain-componenten in volgorde aanroepen. Positie: **náást** `/api/generate`, niet erin. `/api/generate` blijft de snelle, bestaande ingang; de Design Brain wordt de tweede, rijkere ingang die de volledige BUILD-007-workflow doorloopt.

## 2. Verantwoordelijkheid

De integratielaag **ontsluit en orkestreert, meer niet**: zij ontvangt HTTP-verzoeken, roept de bestaande componenten aan (Conversation Planner, Reasoning Engine, Material/Pattern Planner, SVG Planner via de BUILD-018-adapter, Floor Visualization Engine, Design Transfer Package), houdt per gesprek de gedeelde DesignContext-toestand vast, en serialiseert de resultaten naar JSON. Zij **beslist, interpreteert en bevestigt niets zelf** en **dupliceert geen ontwerplogica**.

## 3. Input

- **Gebruikersinvoer** (dialoog/vrije tekst) voor de Conversation Planner.
- **Architect-bevestiging:** een expliciete actie van de gebruiker-als-architect die de OntwerpVisie bevestigt (zet `bevestigd_door_architect`).
- **Scene-referentie:** een `Scene` uit de bestaande Scene Builder (voor de Floor Visualization Engine).
- **Standaard request-gegevens:** o.a. de `api_key` (zoals `/api/generate` die al ontvangt) waarmee de Context Interpreter achter de Conversation Planner wordt aangedreven.

## 4. Output

- **De conversationele vervolgstap** van de Conversation Planner (vraag of samenvatting ter bevestiging).
- **De opgebouwde/bevestigde OntwerpVisie** (laag 1).
- **De resultaat-objecten van de keten** — Floor Design, Material Profile, Pattern Profile, `SVGResultaat`, Visualisatie en het Design Transfer Package — geserialiseerd als JSON voor de frontend.

Uitsluitend de **bestaande** resultaat-objecten; er ontstaat geen nieuw resultaat-object.

## 5. Gebruikte gegevens

- De **DesignContext** als gedeelde toestand per gesprek (dezelfde datastructuur, `design_context.py`).
- De **Scene** uit de Scene Builder (read-only).
- De **SVG-productiepipeline** via de SVG Planner-adapter (BUILD-018) — read-only hergebruik, geen duplicatie.
- De bestaande componenten en hun resultaat-objecten.

De integratielaag schrijft **zelf** niets in de DesignContext; alle schrijfacties verlopen via de componenten binnen hun eigen grenzen (uitsluitend de Conversation Planner schrijft de onbevestigde laag 1; de Reasoning Engine Fase 1 schrijft laag 4 + Ontwerpredenering).

## 6. Wel / niet verantwoordelijk

**Wel:**
- de Design Brain-componenten via HTTP **ontsluiten**;
- per gesprek de **DesignContext-toestand vasthouden**;
- de componenten in de **juiste ketenvolgorde** aanroepen;
- de resultaten **serialiseren** naar JSON.

**Niet:**
- **geen ontwerpbeslissing, interpretatie of bevestiging** zelf;
- **geen herimplementatie/duplicatie** van chain-logica;
- **geen wijziging** aan `/api/generate` of aan enige bestaande route/flow;
- **geen bypass** van de keten (geen directe `build_tile_svg`-shortcut binnen de Design Brain-ingang);
- **geen nieuw resultaat-object** en **geen nieuw productie-/exportformaat** (DTP/Productie Engine blijven zoals ze zijn);
- **geen automatische bestelling/productie** (het Design Transfer Package levert aan DCOD als mens).

## 7. Relaties met bestaande componenten

- **Conversation Planner (BUILD-017):** voert de dialoog en bouwt laag 1; de integratielaag geeft gebruikersinvoer door en injecteert de Context Interpreter met de `api_key`.
- **Reasoning Engine / Material Planner / Pattern Planner:** de ontwerpketen, aangeroepen op bevestigde upstream-inhoud.
- **SVG Planner + BUILD-018-adapter:** rendert via de bestaande `build_tile_svg`-pipeline; **geen** aparte/dubbele render.
- **Scene Builder (BUILD-006):** levert de `Scene` voor de Floor Visualization Engine (read-only).
- **Floor Visualization Engine (BUILD-015):** produceert de Visualisatie.
- **Design Transfer Package (BUILD-016):** bundelt de bevestigde inhoud voor DCOD.
- **Bestaande routes** (`/api/generate`, `/api/refine`, `/api/export/*`, `/api/scenes`, `/api/bestelling`): blijven **ongewijzigd** naast de nieuwe ingang; de lichtgewicht-DesignContext van `/api/generate` (BUILD-001/002/003) wordt niet aangeraakt of samengevoegd.

## 8. Grenzen

- **Volledig additief:** uitsluitend nieuwe endpoints; geen wijziging aan bestaande routes, flows of de productiepipeline.
- **Geen bypass:** de Design Brain-ingang doorloopt de volledige keten via de componenten.
- **Geen nieuwe architectuurcomponent/verantwoordelijkheid:** de laag is uitsluitend ontsluiting/orkestratie (vergelijkbaar met de BUILD-018-boundary-implementatie).
- **Determinisme-basislijn (BUILD-018):** geldt voor de SVG-stap; niet-deterministische stijlen blijven gegate't (R1).
- **De bestaande Dessinator blijft de snelle ingang;** de Design Brain is de tweede ingang, geen vervanging.

## 9. Architectuurbewaking (ter attentie van de VR)

1. **Geen nieuwe component.** De ontsluitingslaag draagt geen ontwerpautoriteit en geen nieuwe verantwoordelijkheid; zij orkestreert bestaande componenten (analoog aan BUILD-018).
2. **Geen wijziging aan BUILD-007/017/018** en geen duplicatie: de style-mapping en rendering lopen via de BUILD-018-adapter, niet via de `/api/generate`-keyword-routing.
3. **Sessie-/toestandsbeheer — nieuw aspect voor de app (voor de TD).** De bestaande app is stateless per request, terwijl de Conversation Planner de OntwerpVisie over meerdere beurten opbouwt. Het vasthouden van de DesignContext per gesprek is een **functionele behoefte** die het technisch ontwerp moet oplossen **zonder** een nieuwe architectuurcomponent en **zonder** toestand in het DesignContext-model zelf te introduceren (de DesignContext ís de toestand; de bewaarplaats is infrastructuur). Ter bevestiging door de VR.
4. **Architect-bevestiging via HTTP.** Functioneel is dit een expliciete gebruikersactie die `bevestigd_door_architect` zet; de exacte mechaniek (welke actie, welke autorisatie) is een "hoe" voor het TD. De integratielaag zet de vlag nooit uit zichzelf.
5. **Regressiegrens.** Omdat de integratie strikt additief is (nieuwe endpoints), mag geen bestaande route in gedrag wijzigen; dit is een expliciete acceptatie-eis voor het TD/implementatie.
6. **Import-plaatsing / circulaire afhankelijkheid (voor de TD).** De SVG Planner-adapter (BUILD-018) importeert `app` **lui** (binnen de boundary) juist om een cyclus te vermijden. De integratielaag leeft in of naast `app.py`; het technisch ontwerp moet de plaatsing zó kiezen dat er **geen import-cyclus bij module-load** ontstaat (de lui-import van BUILD-018 blijft daarvoor leidend). Ter bevestiging door de VR.
7. **Concurrency-isolatie van de gesprekstoestand (voor de TD).** "Per gesprek de DesignContext vasthouden" betekent functioneel dat **gelijktijdige gesprekken elk een geïsoleerde DesignContext** hebben; toestand mag niet via gedeelde module-globals lopen (zoals `/api/generate`'s `_ETALAGE_DIRECT_PAL`), om kruisbesmetting tussen gebruikers te voorkomen. Dit is een functionele eis; de bewaarmechaniek is een "hoe" voor het TD.

---

**Reviewgereed:** dit document legt uitsluitend de verantwoordelijkheid, plaats, in-/output, gebruikte gegevens, relaties en grenzen van de Design Brain-integratie vast op functioneel niveau, met een expliciete inventarisatie van de bestaande workflow en drie/­vijf bewust gemarkeerde aandachtspunten (§9). Na een positieve VR kan het als basis dienen voor het technisch ontwerp — dat hier bewust nog niet is uitgewerkt.
