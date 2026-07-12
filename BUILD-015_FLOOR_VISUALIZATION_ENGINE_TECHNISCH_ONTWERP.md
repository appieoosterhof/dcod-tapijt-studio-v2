# BUILD-015 — Floor Visualization Engine: technisch ontwerp

**Status:** technisch ontwerp, ter review. Geen programmacode. Beschrijft uitsluitend **hoe** de Floor Visualization Engine (FVE) wordt gerealiseerd; het **wat** ligt vast in BUILD-015 en mag niet wijzigen. Geen nieuwe architectuurcomponent — de FVE is de reeds bestaande visualisatiecomponent (BUILD-007/VISION-001; de bestaande mockup-/floorvisualizer-engine) en uitsluitend uitvoerend.

**Normatief:** BUILD-007, AB-005, AR-003/004/005 (leidend), BUILD-014, TD-004 (leidend), BUILD-015, en het bewezen implementatiepatroon uit de eerdere planners.

**Architectuurprincipe (technisch geborgd):** de FVE is een **uitvoerende compositiecomponent**, geen ontwerpcomponent. Zij voegt geen ontwerpkeuze toe: zij projecteert het reeds gerenderde `SVGResultaat` deterministisch op de Scene en voegt Floor Design en Material Profile samen tot één Visualisatie. De compositie-stap loopt via een **injecteerbare Visualization Boundary** die de **bestaande mockup-/projectie-engine omhult** (de `matrix3d`-projectie op het vloerpolygon, `ROOM_MOCKUPS`/floorvisualizer in `static/js/app.js`, AB-005). De boundary bevat geen ontwerplogica. Volledig additief en losstaand.

---

## 1. Architectuur

- **Eén module, één publieke component** (bijv. `floor_visualization_engine.py` / `FloorVisualizationEngine`), naast de bestaande bestanden — niet erin.
- **Interne modulegrenzen** (drie, zoals bij de eerdere componenten):
  - **Orkestratie** — stuurt de compositie-keten aan en geeft het resultaat terug.
  - **Visualization Boundary** — injecteerbaar; ontvangt een platte compositie-invoer (het `SVGResultaat`-artefact + de Scene-projectiegegevens + Floor Design/Material Profile-context) en retourneert een Visualisatie-artefact. **Bevat geen ontwerplogica**; de standaard-implementatie **omhult de bestaande projectie-engine** (mockup/floorvisualizer, AB-005), de test-implementatie is een deterministische placeholder. Geen wijziging aan bestaande render-/projectiecode.
  - **Validatie & kwaliteitsborging** — controles vóór en ná de compositie; muteren niets.
- **Uitvoerende compositiecomponent, geen ontwerpautoriteit:** de FVE leest uitsluitend, componeert, en beslist/bevestigt niets (BUILD-007, AR-004/AR-005; uitgangspunt 4).
- **Afhankelijkheden (read-only):** het `SVGResultaat` (uit `svg_planner`), het bevestigde `FloorDesign` (uit `reasoning_engine`), het bevestigde `MaterialProfile` (uit `material_planner`) en de `Scene` (uit `scene_builder`, BUILD-006). Het **Visualisatie-resultaat leeft buiten de DesignContext**, in deze module. Geen wijziging aan `design_context.py`, de planner-modules of de bestaande projectiecode.

## 2. Verwerkingsketen

- **Invoer:** het `SVGResultaat`, het bevestigde `FloorDesign`, het bevestigde `MaterialProfile` en een `Scene` (read-only).
- **Verwerking:** gate → verzamelen van de compositie-invoer (SVG-artefact + Scene-projectiegegevens + Floor Design/Material Profile-context) → Visualization Boundary (projecteert de SVG op het vloerpolygon van de Scene → Visualisatie-artefact) → kwaliteitsborging → verpakken als `Visualisatie` (met herkomst).
- **Gate:** een geldig, **niet-*stale*** `SVGResultaat` (het bronpatroon is nog bevestigd) **én** `FloorDesign.status == "Bevestigd"` **én** `MaterialProfile.status == "Bevestigd"` **én** een geldige `Scene` (achtergrond + vloerpolygon); anders geen compositie (signalering).
- **Uitvoer:** één `Visualisatie` (het samengestelde beeld-artefact + herkomst) buiten de DesignContext + resultaatwikkel.
- **Foutafhandeling:** falende gate of compositiefout → signalering/foutresultaat; **geen partiële Visualisatie**; DesignContext en alle invoer blijven ongewijzigd.

## 3. Gegevensmodellen (technische representatie)

- **`Visualisatie`** — resultaat-artefact **buiten** de DesignContext: identifier; het **beeld-artefact** (het samengestelde resultaat — bijv. de op het vloerpolygon geprojecteerde SVG met de bijbehorende projectiegegevens); een **weergave-motivering** (uitsluitend hoe de bevestigde inhoud getrouw is samengesteld — geen ontwerprechtvaardiging); herkomst-referenties; kwaliteitsinformatie.
- **Motivatie** — de weergave-onderbouwing, in het object.
- **Kwaliteitsinformatie** — bijv. compositie-status (geldig/ongeldig), of de projectie welgevormd is, pogingen.
- **Traceerbaarheid/herkomst** — zie §7.

### VR-027 — besluit: **géén eigen status**
De `Visualisatie` draagt **geen eigen Voorgesteld/Bevestigd-status**. Zij is een **zuivere, deterministische compositie** van reeds bevestigde bronnen (`SVGResultaat` + bevestigd Floor Design + bevestigd Material Profile + Scene).
**Architectonische onderbouwing:** BUILD-007 bepaalt dat de Visualisatie "geen eigen verwerkingslogica" heeft en het getoonde eindbeeld is. Het bevestigings­model (Voorgesteld → Bevestigd) hoort bij *ontwerpbeslissingen* die eigendom zijn van de architect; de FVE voegt géén ontwerpbeslissing toe (AR-004/AR-005; uitgangspunt 4). Dit is exact hetzelfde besluit als voor het `SVGResultaat` (TD-004): de **geldigheid** van de Visualisatie leidt zich volledig af uit haar bronnen — met name uit het `SVGResultaat` (dat op zijn beurt *stale* is zodra zijn Pattern Profile wijzigt). Wijzigt een bron, dan is de Visualisatie *stale* en wordt zij opnieuw samengesteld (§5). Een eigen bevestiging zou de FVE ten onrechte beslissings­dragend maken en circulair zijn.

## 4. Validatie

- **Uitsluitend bevestigde/geldige invoer:** de gate (§2) toetst een niet-*stale* `SVGResultaat`, de bevestigde statussen van Floor Design en Material Profile, en een geldige Scene; anders geen compositie.
- **Uitsluitend het bevestigde `SVGResultaat` projecteren:** de compositie-invoer wordt uitsluitend uit het `SVGResultaat` + de Scene (+ Floor Design/Material Profile-context) geprojecteerd.
- **Consistentie compositie ↔ bronnen:** de compositie is een deterministische functie van de invoer; de kwaliteitsborging controleert dat het Visualisatie-artefact geldig is (welgevormde projectie op het vloerpolygon) en dat de herkomst naar het gebruikte `SVGResultaat` en de Scene klopt. Een semantische "getrouwheids"-toets ligt bij de Visualization Boundary; deze laag borgt structurele geldigheid.
- **Ongeldige composities afwijzen:** een lege/onwelgevormde Visualisatie wordt niet als geldig teruggegeven en niet verpakt.

## 5. Regeneratie / herstel

- **Wanneer:** bij een technische compositiefout, óf wanneer een bron is gewijzigd waardoor de bestaande Visualisatie *stale* is (het `SVGResultaat` is *stale* geworden, of de Scene is gewijzigd).
- **Welke stap opnieuw:** uitsluitend de compositie (Visualization Boundary + kwaliteitsborging) opnieuw; de bevestigde bronnen blijven ongewijzigd behouden — er is geen ontwerpstap in deze component. Is het `SVGResultaat` zelf *stale*, dan wordt eerst upstream een nieuw `SVGResultaat` gerenderd (SVG Planner), waarna de FVE opnieuw componeert.
- **Geen oneindige lus:** omdat de compositie *deterministisch* is, levert een herhaling met ongewijzigde invoer hetzelfde resultaat; een technische regeneratielimiet voorkomt eindeloos herhalen bij een blijvende compositiefout → signalering.

## 6. Interfaces (C4 ongewijzigd overgenomen uit TD-004)

- **SVG Planner → FVE:** de FVE consumeert het `SVGResultaat` als **data-input** — exact de in TD-004 vastgestelde C4-interface. Deze wordt hier **niet heropend**; de SVG Planner roept de FVE niet aan.
- **Planners + architect → FVE:** leveren het bevestigde Floor Design en Material Profile; read-only.
- **Scene Builder → FVE:** levert de `Scene` (BUILD-006, onafhankelijk aangeleverd); read-only.
- **FVE → Visualisatie:** produceert het `Visualisatie`-artefact (buiten de DesignContext), teruggegeven via de resultaatwikkel — niet in de DesignContext geschreven; geen eigen bevestiging (§3).
- **FVE → Design Transfer Package:** **geen directe aanroep.** De `Visualisatie` is een data-input die de Design Transfer Package (verderop) opneemt, conform de bestaande architectuur (BUILD-007). De FVE kent haar werking niet.

## 7. Traceerbaarheid

- Elke `Visualisatie` draagt een **herkomst-referentie naar het `SVGResultaat`** (identifier) en naar de gebruikte **Scene** (identifier); via de herkomst van het `SVGResultaat` is zij verder herleidbaar naar het bevestigde Concept, Floor Design, Material Profile en Pattern Profile.
- Er wordt **niets in de DesignContext geregistreerd** (buiten de DesignContext) — analoog aan het `SVGResultaat` en de eerdere resultaat-objecten.

## 8. Robuustheid

- **Fouttolerantie:** de compositie-boundary-aanroep in een `try/except`; een technische fout → gestructureerd foutresultaat, **nooit** een partiële of ongeldige Visualisatie; DesignContext en bronnen ongewijzigd.
- **Herstelgedrag:** her-compositie bij een gewijzigde/stale bron of een technische fout, met regeneratielimiet (§5).
- **Uitbreidbaarheid:** de Visualization Boundary is injecteerbaar — de standaard omhult de bestaande projectie-engine (AB-005), maar een andere projectie/renderer kan worden geïnjecteerd **zonder** de component te wijzigen.
- **AI-model-onafhankelijk / deterministisch:** de compositie is deterministisch; geen model, geen prompt.
- **Additief:** nieuw bestand; geen wijziging aan `design_context.py`, de planner-modules of de bestaande render-/projectiecode; geen koppeling aan de live pipeline tot er bewust wordt aangesloten.

---

**Acceptatie:** met een geldig, niet-*stale* `SVGResultaat`, een bevestigd Floor Design en Material Profile en een geldige Scene levert de FVE één `Visualisatie` (het samengestelde beeld-artefact + herkomst naar `SVGResultaat` en Scene, met weergave-motivering) buiten de DesignContext, **zonder eigen bevestigingsstatus**; een ontbrekende/niet-bevestigde bron, een *stale* `SVGResultaat` of een technische compositiefout leiden tot een signalering/foutresultaat en, waar van toepassing, gelimiteerde her-compositie — zonder mutatie van de DesignContext of de bronnen, zonder ontwerpkeuze en zonder bevestiging.
