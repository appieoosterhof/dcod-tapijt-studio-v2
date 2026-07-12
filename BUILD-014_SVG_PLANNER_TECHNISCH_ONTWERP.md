# BUILD-014 — SVG Planner: technisch ontwerp

**Status:** technisch ontwerp, ter review. Geen programmacode. Beschrijft uitsluitend **hoe** de SVG Planner wordt gerealiseerd; het **wat** ligt vast in BUILD-014 en mag niet wijzigen. Geen nieuwe architectuurcomponent — de SVG Planner is de reeds erkende bestaande pipeline (AB-005), uitsluitend uitvoerend (AR-004/AR-005).

**Normatief:** AB-005, AR-003, AR-004, AR-005 (leidend), BUILD-014 (leidend), BUILD-007, AB-011, en het bewezen implementatiepatroon uit de eerdere planners.

**Architectuurprincipe (technisch geborgd):** de SVG Planner is een **uitvoerende renderer**, geen ontwerpcomponent. Hij voegt geen ontwerpkeuze toe: hij rendert een reeds bevestigd patroon deterministisch tot een SVG. De rendering-stap loopt via een **injecteerbare SVG Rendering Boundary** (die kan de bestaande pipeline `build_tile_svg()`/`build_repeat_svg()` uit AB-005 omhullen, of een placeholder voor test); de boundary bevat geen ontwerplogica. Volledig additief en losstaand.

---

## 1. Technische architectuur

- **Eén module, één publieke component** (bijv. `svg_planner.py` / `SVGPlanner`), naast de bestaande bestanden — niet erin.
- **Interne modulegrenzen** (drie, zoals bij de eerdere planners):
  - **Orkestratie** — stuurt de verwerkingsketen aan en geeft het resultaat terug.
  - **SVG Rendering Boundary** — injecteerbaar; ontvangt een platte render-invoer (projectie van de bevestigde objecten) en retourneert een SVG-artefact. **Bevat geen ontwerplogica**; de standaard-implementatie omhult de bestaande generatiepipeline (AB-005), de test-implementatie is een deterministische placeholder. Geen LLM, geen promptteksten.
  - **Validatie & kwaliteitsborging** — controles vóór en ná de rendering; muteren niets.
- **Uitvoerende renderer, geen ontwerpcomponent:** de SVG Planner leest uitsluitend, beslist niets en draagt geen ontwerpautoriteit (AR-004/AR-005; uitgangspunt 4).
- **Afhankelijkheden:** leest het bevestigde `Concept` (laag 4) via de BUILD-008-dataclasses, het bevestigde `FloorDesign`, `MaterialProfile` en `PatternProfile` (buiten de DesignContext) — alle read-only. Het **SVG-resultaat leeft buiten de DesignContext**, in deze module. Geen wijziging aan `design_context.py`, `reasoning_engine.py`, `material_planner.py`, `pattern_planner.py` of de bestaande pipeline (`app.py`/`modules_extra.py`).

## 2. Verwerkingsketen

- **Invoer:** de `DesignContext` (voor het bevestigde Concept), en de bevestigde `FloorDesign`-, `MaterialProfile`- en `PatternProfile`-objecten (read-only).
- **Verwerking:** deterministische gate → projectie van de bevestigde objecten naar de render-invoer → SVG Rendering Boundary (render-invoer → SVG-artefact) → kwaliteitsborging → verpakken als `SVGResultaat` (met herkomst).
- **Deterministische gate:** `Concept.status == "bevestigd"` **én** `FloorDesign.status == "Bevestigd"` **én** `MaterialProfile.status == "Bevestigd"` **én** `PatternProfile.status == "Bevestigd"`; ontbreekt of is er één niet bevestigd, dan rendert de SVG Planner niet (signalering).
- **Uitvoer:** één `SVGResultaat` (het SVG-artefact + herkomst) buiten de DesignContext + resultaatwikkel.
- **Foutafhandeling:** falende gate of renderfout → signalering/foutresultaat; **geen partieel SVG-resultaat**; DesignContext en de bevestigde objecten blijven ongewijzigd.

## 3. Gegevensmodellen (technische representatie)

- **`SVGResultaat`** — resultaat-object **buiten** de DesignContext: identifier; het **SVG-artefact** (de SVG-string/tegel); een **weergave-motivering** (uitsluitend hoe het bevestigde patroon getrouw is gerenderd — geen ontwerprechtvaardiging); herkomst-referenties; kwaliteitsinformatie.
- **Motivatie** — de weergave-onderbouwing, in het object.
- **Kwaliteitsinformatie** — bijv. render-status (geldig/ongeldig), naadloosheid/tegeling, pogingen.
- **Traceerbaarheid/herkomst** — zie §7.

### VR-026 bevinding 2 — besluit: **géén eigen bevestigingsstatus**
Het `SVGResultaat` draagt **geen eigen Voorgesteld/Bevestigd-status**. Het is een **deterministische rendering** van het reeds bevestigde Pattern Profile.
**Architectonische onderbouwing:** het bevestigings­model (Voorgesteld → Bevestigd) hoort bij *ontwerpbeslissingen* die eigendom zijn van de architect (AB-006/AB-009/AB-010/AB-011). De SVG Planner voegt géén ontwerpbeslissing toe (AR-004/AR-005; uitgangspunt 4) — de beslissing ís het bevestigde Pattern Profile. Een eigen bevestiging zou de SVG Planner ten onrechte tot beslissings­dragende component maken en de bevestiging circulair maken. Daarom leidt de **geldigheid** van het SVG-resultaat zich volledig af uit het bevestigde Pattern Profile waarnaar het verwijst; wijzigt dat Pattern Profile, dan is een bestaand SVG-resultaat *stale* en wordt het opnieuw gerenderd (§5).

## 4. Validatie en kwaliteitsborging

- **Uitsluitend bevestigde upstream-objecten:** de deterministische gate (§2) toetst alle vier de statussen; anders geen rendering.
- **Uitsluitend het bevestigde Pattern Profile renderen:** de render-invoer wordt uitsluitend uit het bevestigde Pattern Profile (+ Concept/kleurpalet, Material Profile, Floor Design) geprojecteerd; het Pattern Profile is de primaire renderbron.
- **Consistentie render ↔ Pattern Profile:** de rendering is een deterministische functie van de bevestigde invoer; de kwaliteitsborging controleert dat het SVG-artefact geldig (niet leeg, welgevormd, naadloos tegelbaar) is en dat de herkomst naar het gerenderde Pattern Profile klopt. Een semantische "getrouwheids"-toets ligt bij de rendering-boundary; deze laag borgt structurele geldigheid.
- **Ongeldige renderresultaten afwijzen:** een leeg/onwelgevormd SVG-artefact wordt niet als geldig teruggegeven en niet verpakt.

## 5. Regeneratie

- **Wanneer:** bij een technische renderfout, óf wanneer een upstream-object is gewijzigd waardoor het bestaande SVG-resultaat *stale* is (de herkomst-identifier van het Pattern Profile komt niet meer overeen).
- **Welke stap opnieuw:** uitsluitend de rendering (boundary + kwaliteitsborging) opnieuw; de bevestigde upstream-objecten blijven ongewijzigd behouden — er is geen ontwerpstap in deze component.
- **Geen oneindige lus:** omdat de rendering *deterministisch* is, levert een herhaling met ongewijzigde invoer hetzelfde resultaat; een technische regeneratielimiet voorkomt eindeloos herhalen bij een blijvende renderfout → signalering.

## 6. Interfaces (inclusief het beslechten van C4)

- **Pattern Planner + architect → SVG Planner:** leveren — na bevestiging — het Pattern Profile dat de SVG Planner rendert; read-only.
- **SVG Planner → SVG-resultaat:** produceert het `SVGResultaat` (buiten de DesignContext), teruggegeven via de resultaatwikkel — niet in de DesignContext geschreven; geen eigen bevestiging (§3).
- **SVG Planner → Floor Visualization Engine — C4 beslecht als technische data-koppeling:** de SVG Planner roept de FVE **niet** aan. Het `SVGResultaat` (SVG-artefact + herkomst) is een **data-input** die de Floor Visualization Engine consumeert: de FVE projecteert het SVG-artefact als de concrete vloerafwerking op de Scene, samen met Floor Design en Material Profile (BUILD-007). Dit is exact hetzelfde technische mechanisme als de bestaande mockup-engine, die een SVG al op een vloerpolygon projecteert (`ROOM_MOCKUPS`, AB-005). Hiermee is de open koppeling uit AR-003 (C4) als **technische interface** ingevuld, **zonder architectuurwijziging**: het SVG-artefact is de concrete render die de FVE nodig heeft; er ontstaat geen nieuwe verantwoordelijkheid en de DesignContext blijft ongemoeid.
- **Design Transfer Package:** neemt (verderop) het bevestigde geheel conform de bestaande architectuur op (BUILD-007); de SVG Planner kent zijn werking niet.

## 7. Traceerbaarheid

- Elk `SVGResultaat` draagt een **herkomst-referentie naar het bevestigde Pattern Profile** (identifier) en — via de herkomst van dat Pattern Profile — naar het bevestigde Concept, Floor Design en Material Profile. Daarmee is elk SVG-resultaat herleidbaar naar alle vier de bevestigde bronobjecten en naar de weergave-motivering.
- Er wordt **niets in de DesignContext geregistreerd** (buiten de DesignContext) — analoog aan de eerdere resultaat-objecten.

## 8. Robuustheid

- **Fouttolerantie:** de rendering-boundary-aanroep in een `try/except`; een technische fout → gestructureerd foutresultaat, **nooit** een partieel of ongeldig SVG-resultaat; DesignContext en bevestigde objecten ongewijzigd.
- **Herstelgedrag:** re-render bij een gewijzigd (stale) upstream-object of een technische fout, met regeneratielimiet (§5).
- **Uitbreidbaarheid:** de rendering-boundary is injecteerbaar — de standaard omhult de bestaande pipeline (AB-005), maar een andere renderer kan worden geïnjecteerd **zonder** de component te wijzigen.
- **AI-model-onafhankelijk:** de rendering is deterministisch; geen model, geen prompt.
- **Additief:** nieuw bestand; geen wijziging aan `design_context.py`, `reasoning_engine.py`, `material_planner.py`, `pattern_planner.py` of de bestaande pipeline; geen koppeling aan de live pipeline tot er bewust wordt aangesloten.

---

**Acceptatie:** met een bevestigd, volledig Concept en een bevestigd Floor Design, Material Profile en Pattern Profile levert de SVG Planner één `SVGResultaat` (het SVG-artefact + herkomst naar de vier bronobjecten, met weergave-motivering) buiten de DesignContext, **zonder eigen bevestigingsstatus**; onvoldoende/niet-bevestigde input of een technische renderfout leiden tot een signalering/foutresultaat en, waar van toepassing, gelimiteerde regeneratie — zonder mutatie van de DesignContext of de bevestigde objecten, zonder ontwerpkeuze en zonder bevestiging.
