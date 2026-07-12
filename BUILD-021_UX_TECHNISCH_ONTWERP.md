# BUILD-021 — Technisch UX-/Frontendontwerp: de Design Brain-frontend

**Status:** technisch ontwerp, ter review (TR). Geen implementatie, geen code. Beschrijft uitsluitend **hoe** de frontend die de bestaande Design Brain ontsluit wordt gebouwd; het **wat** ligt vast in BUILD-021 (UX-functioneel). Geen nieuwe backend-component, geen wijziging aan bestaande componenten. Realiseert de "Ontwerp zelf met AI"-ingang bovenop de bestaande `/api/design-brain`-endpoints (BUILD-019/020).

**Bestaande stack (feitelijk):** vanilla JS (`static/js/app.js`), Flask-templates (`index.html`, `inspiratie.html`, `scene_builder.html`), geen framework; JS geladen met cache-stamp `?v=YYYYMMDD_HHMMSS`; datacommunicatie via `fetch(..., {method, headers:{'Content-Type':'application/json'}, body: JSON.stringify(...)})` → `await response.json()`. Aparte pagina per route (`/`, `/inspiratie`, `/scene-builder`).

**Kernbeslissing:** de Design Brain-frontend is een **aparte, volledig additieve pagina** (eigen route + eigen template + eigen JS-bestand), náást de ongewijzigde Dessinator (`/` + `app.js` + `/api/generate`). Geen enkele bestaande template, JS-functie, route of pipeline wordt gewijzigd.

---

## 1. Frontend-architectuur

- **Nieuwe pagina, additief:** één nieuwe Flask-route (bijv. `GET /ontwerp` → `render_template("ontwerp.html")`) — dezelfde additieve vorm als `/scene-builder`. Eén nieuw template `templates/ontwerp.html` en één nieuw JS-bestand `static/js/ontwerp.js` (met eigen `?v=`-cache-stamp). `app.py` wordt uitsluitend uitgebreid met deze ene route (naast de reeds bestaande `register_blueprint`). De bestaande `index.html`/`app.js` blijven ongemoeid; een optionele **één-regels-navigatielink** vanaf de landingspagina is de enige denkbare aanraking van een bestaand template en verandert geen enkele flow.
- **Schermindeling (twee panelen):**
  - **Links — gespreks-/beslispaneel:** chatvenster + bevestigingskaarten + voortgangsbalk + (inklapbaar) samenvattingspaneel.
  - **Rechts — visualisatiepaneel:** het meest actuele beeld (sfeerbeeld → dessin-staal → dessin-in-de-ruimte).
  - **Responsief:** onder een breekpunt gestapeld (beeld boven, gesprek onder); relatieve eenheden, `max-width:100%` op beeld.
- **Componentstructuur (vanilla JS, geen framework):** één client-controller (`OntwerpController`) die de client-state houdt en na elke server-respons de betreffende DOM-secties opnieuw rendert. "Componenten" = pure render-functies per sectie (chat, kaart, viz, voortgang, samenvatting, eindscherm) die in hun eigen container schrijven. Unidirectioneel: **actie → API-call → state bijwerken → re-render**.
- **State-management:** één in-memory client-state-object, bijv. `{ gesprek_id, fase, visie, projectcontext, strategie, concept, floor_design, materiaal, patroon, svg, mockup, dtp, bezig }`. De **backend is de bron van waarheid**; de client houdt uitsluitend een spiegel voor weergave en leidt de `fase` af uit welke artefacten bevestigd zijn. `gesprek_id` wordt in `localStorage` bewaard voor herstel (§3).
- **Koppeling met Flask:** de nieuwe route serveert alleen het statische template; alle dynamiek loopt via `fetch` naar `/api/design-brain/*` (en `/api/scenes` voor de ruimte). Geen server-side rendering van ontwerpinhoud — exact het patroon van de bestaande app.

## 2. API-koppelingen

| Frontendonderdeel / actie | Endpoint | Wanneer | Payload | Verwachte respons |
|---|---|---|---|---|
| Pagina-init / "Begin" | `POST /api/design-brain/gesprek` | bij start zonder opgeslagen id | — | `{gesprek_id}` (201) |
| Herstel bij herladen | `GET /api/design-brain/<gid>` | bij load met opgeslagen id | — | `{toestand}` of 404 |
| Chat verzenden | `POST /<gid>/dialoog` | gebruiker stuurt bericht | `{invoer, api_key}` | `{vervolgstap, ontwerpvisie, projectcontext}` of `{signaleringen}` |
| Visie bevestigen | `POST /<gid>/bevestig-visie` | op bevestigingskaart | — | `{bevestigd_door_architect}` |
| Richting voorstellen | `POST /<gid>/ontwerpstrategie` | na visie-bevestiging | — | `{ontwerpstrategie}` of `{signaleringen}` |
| Richting bevestigen | `POST /<gid>/bevestig-strategie` | op kaart | — | `{ontwerpstrategie_status}` |
| Concept ophalen | `POST /<gid>/concept` | na strategie-vaststelling | — | `{concept}` of `{signaleringen}` |
| Concept bevestigen | `POST /<gid>/bevestig-concept` | op kaart | — | `{concept_status}` |
| Ontwerprichtingen | `POST /<gid>/floor-designs` | na concept-bevestiging | — | `{floor_designs[]}` |
| Ontwerp kiezen | `POST /<gid>/bevestig-floor-design` | keuzekaart | `{index}` | `{floor_design}` |
| Materiaal | `POST /<gid>/material-profiles` → `.../bevestig-material-profile` | na floor-design | `{index}` bij bevestigen | `{material_profiles[]}` / `{material_profile}` |
| Patroon | `POST /<gid>/pattern-profiles` → `.../bevestig-pattern-profile` | na materiaal | `{index}` bij bevestigen | `{pattern_profiles[]}` / `{pattern_profile}` |
| Dessin renderen | `POST /<gid>/svg` | na patroon-bevestiging | — | `{svg_resultaat}` |
| Ruimte kiezen | `GET /api/scenes` (+ bestaande `/scene-builder`) | vóór het ruimtebeeld | — | lijst scenes |
| Beeld in de ruimte | `POST /<gid>/visualisatie` | na SVG + gekozen ruimte | `{scene_id}` | `{visualisatie}` |
| Overdrachtspakket | `POST /<gid>/transfer-package` | bij "tevreden" | — | `{design_transfer_package}` |

`api_key` wordt door de gebruiker aangeleverd zoals in de bestaande app (invoerveld); de frontend stuurt hem uitsluitend mee bij `/dialoog` (de enige stap die de Context Interpreter aandrijft). De `api_key` wordt **uitsluitend in-memory** gehouden en **nooit in `localStorage`** bewaard (consistent met de bestaande app; uitsluitend `gesprek_id` wordt gepersisteerd — §3).

## 3. Gesprekstoestand (client)

- **`gesprek_id`-beheer:** aangemaakt bij de eerste start, bewaard in `localStorage` (bijv. `db_gesprek_id`). Alle vervolgcalls gebruiken dit id in het pad.
- **Herstel van gesprekken:** bij pagina-load met een opgeslagen id doet de client `GET /<gid>` en **rehydrateert** de UI uit `toestand` (fase afgeleid uit aanwezige/bevestigde artefacten). Zonder opgeslagen id → nieuw gesprek.
- **Verversen van de UI:** na elke geslaagde actie wordt de client-state uit de respons bijgewerkt en worden alleen de geraakte secties opnieuw gerenderd (chat, kaart, viz, voortgang, samenvatting).
- **Foutafhandeling/synchronisatie:** de **backend is leidend**. De client neemt nooit een toestand aan die de backend niet bevestigde. Bij twijfel/inconsistentie haalt de client `GET /<gid>` op en rendert daaruit. Een 404 op een opgeslagen id (verlopen/afwezig, bv. na herstart van de ephemeral store) → `localStorage` wissen en een nieuw gesprek aanbieden (§6).

## 4. Visualisaties

- **Sfeerbeeld:** client-side gerenderd uit de `concept`-respons (kleurpalet als stalen + stijlkarakter) — **geen** extra call.
- **SVG (dessin-staal):** opgehaald met `POST /<gid>/svg`; de client rendert de teruggegeven SVG-string inline of als `data:`-URI (basislijn is `clipPath`-vrij, Safari-veilig — BUILD-018).
- **Mockup (in de ruimte):** ná `POST /<gid>/visualisatie`; de respons `visualisatie.beeld` bevat achtergrond, vloerpolygon en de SVG. De client rendert dit in het visualisatiepaneel **zonder de bestaande mockup-engine (`app.js`) aan te raken of te dupliceren** — het eerste niveau is een **zelfstandige, lichte** weergave uit de `beeld`-payload (achtergrond + projectie op het vloerpolygon), nadrukkelijk **geen kopie van de `matrix3d`-code** uit `app.js`. De **hoogwaardige `matrix3d`-projectie** (de bestaande floorvisualizer) is een bewust **uitgestelde P1-integratiekeuze** (delen via een later te extraheren gedeelde helper vs. injecteren als productie-boundary in de FVE); dit TD legt die keuze niet vast om geen duplicatie of wijziging van de mockup-engine te forceren.
- **Andere ruimte kiezen:** de gebruiker kiest een andere Scene → `POST /<gid>/visualisatie {nieuw scene_id}` → mockup ververst (zelfde dessin, nieuwe ruimte).
- **Stale-resultaten verdwijnen:** wijzigt een bovenstroomse keuze (materiaal of patroon), dan **verwijdert de client onmiddellijk** het oude dessin/mockup uit de state en haalt de downstream opnieuw op (`/svg`, daarna `/visualisatie`) — de client spiegelt zo de backend-stale-detectie; er wordt nooit een beeld getoond dat niet meer bij de keuzes hoort.
- **Design Transfer Package:** komt beschikbaar zodra `POST /<gid>/transfer-package` slaagt; dan toont het eindscherm (§5) de bundel-samenvatting.

## 5. UX-componenten (technisch)

- **Chatvenster:** scrollbare berichtenlijst (gebruiker + Dessinator) + invoerveld; rendert `vervolgstap.inhoud` als bericht; stuurt naar `/dialoog`. Toont een "aan het meedenken…"-indicator tijdens de call.
- **Bevestigingskaarten:** een kaart met een korte samenvatting + acties **"Bevestig"** / **"Pas aan"**, gekoppeld aan het bijbehorende bevestig-endpoint. Voor lijsten (ontwerprichtingen, materialen, patronen) een **keuzekaartenset**: kies er één → `bevestig-…-{index}`.
- **Visualisatiepaneel:** toont het meest actuele beeld uit de client-state (sfeerbeeld/dessin/mockup) met laad- en lege toestanden; nooit een verouderd beeld (§4).
- **Voortgangsbalk:** zeven mijlpalen (visie → strategie → concept → ontwerp → materiaal → patroon → eindontwerp), afgeleid uit de client-state. Vooruitspringen kan niet (alleen via bevestigingen); reeds bevestigde stappen zijn herbezoekbaar.
- **Samenvattingspaneel:** een meegroeiend overzicht van bevestigde keuzes in gewone taal, bijgewerkt na elke bevestiging.
- **Eindscherm:** groot eindbeeld + leesbare samenvatting + bevestiging van het overdrachtspakket + afsluitende CTA ("DCOD ontvangt uw ontwerp"). Geen bestelling/prijs (BUILD-007/021).

## 6. Foutafhandeling

- **Netwerkfouten:** een `fetch`-afwijzing/timeout → vriendelijke melding met "opnieuw proberen"; de laatst bekende UI blijft staan; geen dataverlies (backend is leidend).
- **Backend-signaleringen** (`{success:false, signaleringen}`): vertaald naar in-context, mensvriendelijke tekst (bijv. de Dessinator die om de ontbrekende informatie vraagt), **nooit** een ruwe foutcode. Bekende signaleringen krijgen begeleidende copy.
- **Ontbrekende informatie:** bij een dialoog-signalering (bv. interpretatie mislukt / geen `api_key`) vraagt de UI gericht om dat ene ontbrekende gegeven.
- **Verlopen gesprek:** 404 op een opgeslagen `gesprek_id` → `localStorage` wissen, "we beginnen opnieuw" tonen, nieuw gesprek aanbieden.
- **Herstellen van de interface:** bij load of inconsistentie rehydrateert de client uit `GET /<gid>`; bij twijfel wint altijd de backend-`toestand`.

## 7. Performance

- **Lazy loading:** de scene-lijst en scene-afbeeldingen worden pas geladen bij de ruimtekeuze; de SVG/mockup pas bij hun stap; het eigen JS-bestand pas op de nieuwe pagina.
- **Caching:** de scene-lijst en het laatst opgehaalde dessin/mockup worden in de client-state gecachet om onnodige refetches te vermijden; `GET /<gid>` uitsluitend bij load/herstel.
- **Debounce:** chatverzending en snelle klikken worden gedebounced; knoppen zijn uitgeschakeld tijdens een lopende call.
- **Asynchrone requests:** alle calls `async/await`; niet-blokkerende UI met laadindicatoren.
- **Voorkomen van dubbele requests:** een **in-flight-vergrendeling** per actie (de knop wordt uitgeschakeld tot de respons binnen is). Bevestig-acties zijn bovendien idempotent op de backend (ze zetten een status/vlag), zodat een onbedoelde herhaling geen schade doet.

## 8. Integratie & consistentietoets

- **Geen wijziging van `/api/generate`:** de nieuwe pagina raakt die route niet.
- **Geen wijziging van de bestaande Dessinator-flow:** `index.html`/`app.js` blijven ongemoeid (hooguit één additieve navigatielink).
- **Geen wijziging van de SVG-pipeline:** rendering loopt via de bestaande `/svg`-endpoint (SVG Planner + BUILD-018-adapter).
- **Geen wijziging van de mockup-engine:** de nieuwe pagina rendert uit de FVE-`beeld`-payload en raakt `app.js`' mockup-engine niet; de hoogwaardige projectie-integratie is bewust uitgesteld (§4).
- **Uitsluitend additieve frontend:** nieuwe route + nieuw template + nieuw JS-bestand (+ optionele navigatielink).
- **BUILD-007:** de schermflow volgt exact de keten (visie → strategie → concept → floor design → materiaal → patroon → visualisatie → overdracht).
- **BUILD-019:** elke UI-actie map t 1-op-1 op een bestaand endpoint (§2).
- **BUILD-020:** de frontend respecteert de volgorde laag 2 (in de dialoog) → strategie → vaststellen → concept.
- **BUILD-021:** realiseert de UX-reis, dialoogtoon, visualisatie-timing, bevestigingsmomenten, foutbegeleiding en het eindscherm.

---

**Acceptatie:** de frontend is een aparte, additieve pagina (route + template + JS) die uitsluitend via `fetch` de bestaande `/api/design-brain`-endpoints en `/api/scenes` aanroept, met de backend als bron van waarheid, `gesprek_id` in `localStorage` voor herstel, unidirectionele state→render, stale-veilige visualisatie, mensvriendelijke foutbegeleiding en in-flight-bescherming — zonder enige wijziging aan `/api/generate`, de bestaande Dessinator-flow, de SVG-pipeline of de mockup-engine, en volledig consistent met BUILD-007/019/020/021.
