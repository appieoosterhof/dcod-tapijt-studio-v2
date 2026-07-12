# BUILD-013 — Pattern Planner: technisch ontwerp

**Status:** technisch ontwerp, ter review. Geen programmacode. Beschrijft uitsluitend **hoe** de Pattern Planner wordt gerealiseerd; het **wat** ligt vast in BUILD-013 en AB-011 en mag niet wijzigen. Geen nieuwe architectuurcomponent, geen nieuwe functionele verantwoordelijkheid.

**Normatief:** AB-011 (leidend), BUILD-013 (leidend), AB-010A, BUILD-007, BUILD-010/BUILD-011/BUILD-012 (consistent te houden), BUILD-008 (fundament), en het bewezen implementatiepatroon uit `reasoning_engine.py` en `material_planner.py`.

**Architectuurprincipe (technisch geborgd):** de Pattern Planner **stelt voor, bevestigt nooit** (AB-011) en is **AI-model-onafhankelijk** — de redeneerstap loopt via een injecteerbare boundary die DesignContext noch registratie kent. Het **Pattern Profile is een zelfstandig resultaat-object buiten de DesignContext** (AB-011); de DesignContext en de drie bevestigde upstream-objecten worden uitsluitend gelezen. Volledig additief en losstaand.

---

## 1. Technische architectuur

- **Eén module, één publieke component** (bijv. `pattern_planner.py` / `PatternPlanner`), naast `design_context.py`, `reasoning_engine.py` en `material_planner.py` — niet erin.
- **Interne modulegrenzen** (drie, zoals bij de eerdere planners):
  - **Orkestratie** — stuurt de verwerkingsketen aan en geeft het resultaat terug.
  - **Pattern Reasoning Boundary** — injecteerbaar; kent DesignContext noch registratie; ontvangt een platte invoer (projectie van de drie bevestigde objecten) en retourneert een lijst patroonvoorstellen. Deterministische placeholder voor test; geen LLM, geen promptteksten.
  - **Validatie & kwaliteitsborging** — controles vóór en ná de boundary; muteren niets.
- **Afhankelijkheden:** leest het bevestigde `Concept` (laag 4) via de BUILD-008-dataclasses, het bevestigde `FloorDesign` (uit `reasoning_engine`) en het bevestigde `MaterialProfile` (uit `material_planner`) — alle read-only, buiten of via de DesignContext. Het **`PatternProfile`-datamodel leeft buiten de DesignContext**, in deze module. Geen wijziging aan `design_context.py`, `reasoning_engine.py` of `material_planner.py`.

## 2. Verwerkingsketen

- **Invoer:** de `DesignContext` (voor het bevestigde Concept, laag 4), het bevestigde `FloorDesign`-object en het bevestigde `MaterialProfile`-object (read-only).
- **Verwerking:** preconditie-validatie → Pattern Reasoning Boundary (projectie van de drie objecten → lijst patroonvoorstellen) → kwaliteitsborging → verpakken als `PatternProfile`-objecten (status "Voorgesteld", met motivering en drie herkomst-referenties).
- **Validatie:** Concept bevestigd en volledig; Floor Design bevestigd; Material Profile bevestigd; elk patroonvoorstel structureel volledig en aansluitend op de drie bevestigde objecten.
- **Uitvoer:** één of meer `PatternProfile`-objecten (status "Voorgesteld") buiten de DesignContext + resultaatwikkel.
- **Foutafhandeling:** falende preconditie of boundary → signalering/foutresultaat; **geen partieel Pattern Profile**; DesignContext, Floor Design en Material Profile blijven ongewijzigd.

## 3. Gegevensmodellen (technische representatie, functionele betekenis ongewijzigd)

- **`PatternProfile`** — zelfstandig resultaat-object **buiten** de DesignContext (AB-011): identifier; de patroonbeschrijving (bijv. motiefstructuur, motiefschaal, dichtheid, herhalingskarakter); de **motivering** (in het object zelf); status "Voorgesteld"; **drie enkelvoudige herkomst-referenties** — naar het bevestigde Concept, het bevestigde Floor Design en het bevestigde Material Profile; kwaliteitsinformatie.
- **Patroonvoorstellen** — conform AB-011 K2-B is een patroonvoorstel exact een `PatternProfile` met status "Voorgesteld"; er is dus één datamodel, niet twee.
- **Motivaties** — `PatternProfile.motivering`, uitsluitend in het object (niet in de DesignContext).
- **Kwaliteitsinformatie** — per resultaat: binnen-Concept, aansluiting-Floor-Design, aansluiting-Material-Profile, aantal, afgekeurd, pogingen.
- **Traceerbaarheid** — via de drie herkomst-referenties (Concept-snapshot + Floor Design-identifier + Material Profile-identifier); zie §7.

## 4. Validatie en kwaliteitsborging

- **Deterministische drievoudige gate:** `Concept.status == "bevestigd"` (laag 4) **én** `FloorDesign.status == "Bevestigd"` **én** `MaterialProfile.status == "Bevestigd"`; ontbreekt of is er één niet bevestigd, dan start de component niet (signalering). Het Concept moet bovendien volledig zijn (verplichte laag-4-velden).
- **Aansluiting op de drie bevestigde objecten:** elk patroonvoorstel draagt de drie herkomst-referenties én wordt structureel getoetst; een voorstel dat het Concept verlaat of een van de bronnen niet correct referentieert, wordt afgewezen. De semantische toets "aantoonbaar aansluitend" wordt (conform de lijn van de eerdere planners) door de model-specifieke boundary geleverd; deze laag borgt de structurele geldigheid en de expliciete grens.
- **Ongeldige voorstellen afwijzen:** structureel onvolledige of grens-overschrijdende voorstellen worden niet als geldig teruggegeven en niet verpakt.

## 5. Regeneratie

- **Wanneer:** bij een afgekeurd resultaat (geen geldig patroonvoorstel) of op verzoek van de architect (varianten).
- **Welke fase opnieuw:** uitsluitend de Pattern Planner-verwerking (boundary + validatie) opnieuw; de drie bevestigde upstream-objecten blijven ongewijzigd behouden — er is geen upstream-fase binnen deze component.
- **Geen oneindige lus:** een technische regeneratielimiet (analoog aan de eerdere planners); bij overschrijding → signalering, geen verdere retry. De component vult nooit zelf aan.

## 6. Interfaces

- **Reasoning Engine + architect → Pattern Planner:** leveren (via de DesignContext) het bevestigde Concept en het bevestigde Floor Design.
- **Material Planner + architect → Pattern Planner:** levert het bevestigde Material Profile.
- **Pattern Planner → Pattern Profile:** produceert `PatternProfile`-objecten (buiten de DesignContext), teruggegeven via de resultaatwikkel — niet in de DesignContext geschreven.
- **Architect → Pattern Profile:** bevestigt één voorgesteld Pattern Profile (Voorgesteld → Bevestigd); de Pattern Planner **leest** die status alleen en bevestigt nooit.
- **Pattern Planner → SVG Planner:** **geen directe aanroep.** Het bevestigde Pattern Profile is (ná bevestiging) invoer voor de SVG Planner, die het patroon rendert (uitsluitend uitvoerend; AB-005/AR-004).
- **SVG Planner → Floor Visualization Engine / Design Transfer Package:** conform de bestaande architectuur (BUILD-007). De precieze technische koppeling SVG ↔ visualisatie (AR-003, C4) valt buiten deze component en wordt niet heropend.

## 7. Traceerbaarheid

- Elk `PatternProfile` draagt: een **Concept-herkomst** (snapshot van het bevestigde Concept), een **Floor Design-herkomst** (identifier/verwijzing naar het bevestigde Floor Design), een **Material Profile-herkomst** (identifier/verwijzing naar het bevestigde Material Profile) en de **motivering**. Daarmee is elk Pattern Profile herleidbaar naar de drie bevestigde bronobjecten en de onderbouwing van het voorstel.
- Er wordt **niets in de DesignContext geregistreerd** (buiten de DesignContext; motivering in het object) — analoog aan Floor Design en Material Profile.

## 8. Robuustheid

- **Fouttolerantie:** elke boundary-aanroep in een `try/except`; een technische fout → gestructureerd foutresultaat, **nooit** een partieel of verzonnen Pattern Profile; DesignContext, Floor Design en Material Profile ongewijzigd.
- **Herstelgedrag:** gelimiteerde regeneratie (§5); de drie bevestigde upstream-objecten blijven behouden.
- **Uitbreidbaarheid:** het patroon validatie → boundary → kwaliteitsborging → resultaatwikkel is de herbruikbare blauwdruk; een echte, model-specifieke redenering wordt later geïnjecteerd **zonder** de component te wijzigen.
- **AI-model-onafhankelijk:** geen model of prompt vastgelegd; de boundary is de enige plek waar redenering plaatsvindt.
- **Additief:** nieuw bestand; geen wijziging aan `design_context.py`, `reasoning_engine.py` of `material_planner.py`; geen koppeling aan de live pipeline tot er bewust wordt aangesloten.

---

**Acceptatie:** met een bevestigd, volledig Concept, een bevestigd Floor Design en een bevestigd Material Profile levert de Pattern Planner één of meer `PatternProfile`-objecten (status "Voorgesteld", met motivering en drie enkelvoudige herkomst-referenties) buiten de DesignContext; onvoldoende input, een afgekeurd resultaat of een technische fout leiden tot een signalering/foutresultaat en, waar van toepassing, gelimiteerde regeneratie — zonder mutatie van de DesignContext of de bevestigde upstream-objecten, zonder bevestiging en zonder zelf aan te vullen.
