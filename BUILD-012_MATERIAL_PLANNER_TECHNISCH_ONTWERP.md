# BUILD-012 — Material Planner: technisch ontwerp

**Status:** technisch ontwerp, ter review. Geen programmacode. Beschrijft uitsluitend **hoe** de Material Planner wordt gerealiseerd; het **wat** ligt vast in BUILD-012 en AB-010 en mag niet wijzigen. Geen nieuwe architectuurcomponent, geen nieuwe functionele verantwoordelijkheid.

**Normatief:** AB-010 (leidend), BUILD-012 (leidend), BUILD-007, BUILD-010/BUILD-011 (consistent te houden), BUILD-008 (fundament), en het bewezen implementatiepatroon uit `reasoning_engine.py` (Fase 2).

**Architectuurprincipe (technisch geborgd):** de Material Planner **stelt voor, bevestigt nooit** (AB-010) en is **AI-model-onafhankelijk** — de redeneerstap loopt via een injecteerbare boundary die DesignContext noch registratie kent. Het **Material Profile is een zelfstandig resultaat-object buiten de DesignContext** (AB-010); de DesignContext en het **bevestigde Floor Design** worden uitsluitend gelezen. De component start uitsluitend bij een bevestigd Floor Design (AB-010A). Volledig additief en losstaand.

---

## 1. Technische architectuur

- **Eén module, één publieke component** (bijv. `material_planner.py` / `MaterialPlanner`), naast `design_context.py` en `reasoning_engine.py` — niet erin.
- **Interne modulegrenzen** (drie, zoals bij de Reasoning Engine):
  - **Orkestratie** — stuurt de verwerkingsketen aan en geeft het resultaat terug.
  - **Material Reasoning Boundary** — injecteerbaar; kent DesignContext noch registratie; ontvangt een platte invoer (bevestigd Concept + Floor Design-projectie) en retourneert een lijst materiaalvoorstellen. Deterministische placeholder voor test; geen LLM, geen promptteksten.
  - **Validatie & kwaliteitsborging** — controles vóór en ná de boundary; muteren niets.
- **Afhankelijkheden:** leest de bevestigde `Concept` (laag 4) via de BUILD-008-dataclasses en de `FloorDesign`-objecten (buiten de DesignContext, uit `reasoning_engine`). Het **`MaterialProfile`-datamodel leeft buiten de DesignContext**, in deze module. Geen wijziging aan `design_context.py` of `reasoning_engine.py`.

## 2. Verwerkingsketen

- **Invoer:** de `DesignContext` (voor het bevestigde Concept, laag 4) en het **bevestigde `FloorDesign`-object** (`status == "Bevestigd"`, read-only).
- **Verwerking:** preconditie-validatie → Material Reasoning Boundary (Concept + Floor Design-projectie → lijst materiaalvoorstellen) → kwaliteitsborging → verpakken als `MaterialProfile`-objecten (status "Voorgesteld", met motivering en herkomst).
- **Validatie:** Concept bevestigd en volledig; **het Floor Design bevestigd** (`FloorDesign.status == "Bevestigd"`); elk materiaalvoorstel structureel volledig en aansluitend op Concept + het bevestigde Floor Design.
- **Uitvoer:** één of meer `MaterialProfile`-objecten (status "Voorgesteld") buiten de DesignContext + resultaatwikkel.
- **Foutafhandeling:** falende preconditie of boundary → signalering/foutresultaat; **geen partieel Material Profile**; DesignContext én het bevestigde Floor Design blijven ongewijzigd.

## 3. Gegevensmodellen (technische representatie, functionele betekenis ongewijzigd)

- **`MaterialProfile`** — zelfstandig resultaat-object **buiten** de DesignContext (AB-010): identifier; de materiële eigenschappen (materiaalsoort, structuur, pooltype, tactiliteit, uitstraling — BUILD-007); de **motivering** (in het object zelf); status "Voorgesteld"; een **enkelvoudige herkomst-referentie** naar het bevestigde Concept én naar het bevestigde Floor Design; kwaliteitsinformatie.
- **Materiaalvoorstellen** — conform AB-010 K10-B is een materiaalvoorstel exact een `MaterialProfile` met status "Voorgesteld"; er is dus één datamodel, niet twee.
- **Motivaties** — `MaterialProfile.motivering`, uitsluitend in het object (niet in de DesignContext).
- **Kwaliteitsinformatie** — per resultaat: binnen-Concept, aansluiting-Floor-Design, aantal, afgekeurd, pogingen.
- **Traceerbaarheid** — via de herkomst-referenties (Concept-snapshot + Floor Design-identifier(s)); zie §7.

## 4. Validatie en kwaliteitsborging

- **Uitsluitend een bevestigd Concept:** preconditie `Concept.status == "bevestigd"` (deterministische gate, zoals bij de Reasoning Engine) + verplichte laag-4-velden aanwezig.
- **Uitsluitend een bevestigd Floor Design:** preconditie — `FloorDesign.status == "Bevestigd"`; het bevestigde Floor Design moet identificeerbaar zijn (enkelvoudig).
- **Aansluiting op Concept en het bevestigde Floor Design:** elk materiaalvoorstel draagt de herkomst-referenties én wordt structureel getoetst; een voorstel dat het Concept verlaat of het bevestigde Floor Design niet correct referentieert, wordt afgewezen. De semantische toets "aantoonbaar aansluitend" wordt (conform de lijn van de Reasoning Engine) door de model-specifieke boundary geleverd; deze laag borgt de structurele geldigheid en de expliciete grens.
- **Ongeldige voorstellen afwijzen:** structureel onvolledige of grens-overschrijdende voorstellen worden niet als geldig teruggegeven en niet verpakt.

## 5. Regeneratie

- **Wanneer:** bij een afgekeurd resultaat (geen geldig materiaalvoorstel) of op verzoek van de architect (varianten).
- **Welke fase opnieuw:** uitsluitend de Material Planner-verwerking (boundary + validatie) opnieuw; het bevestigde Concept en het bevestigde Floor Design blijven ongewijzigd behouden — er is geen upstream-fase binnen deze component.
- **Geen oneindige lus:** een technische regeneratielimiet (analoog aan de Reasoning Engine); bij overschrijding → signalering, geen verdere retry. De component vult nooit zelf aan.

## 6. Interfaces

- **Reasoning Engine + architect → Material Planner:** de Reasoning Engine produceert Floor Designs; ná bevestiging door de architect ontvangt de Material Planner het **bevestigde `FloorDesign`-object** (buiten de DesignContext) en, via de DesignContext, het bevestigde Concept. Read-only; de Material Planner produceert of wijzigt geen Floor Designs.
- **Material Planner → Material Profile:** produceert `MaterialProfile`-objecten (buiten de DesignContext), teruggegeven via de resultaatwikkel — niet in de DesignContext geschreven.
- **Architect → Material Profile:** de architect bevestigt één voorgesteld Material Profile (Voorgesteld → Bevestigd); de Material Planner **leest** die status alleen en bevestigt nooit.
- **Material Planner → Floor Visualization Engine / Design Transfer Package:** **geen directe aanroep.** Het bevestigde Material Profile is (samen met Floor Design + Scene) invoer voor de FVE en onderdeel van de Design Transfer Package (BUILD-007). De Material Planner kent hun werking niet.

## 7. Traceerbaarheid

- Elk `MaterialProfile` draagt: een **Concept-herkomst** (snapshot van het bevestigde Concept), een **enkelvoudige Floor Design-herkomst** (identifier/verwijzing naar het bevestigde Floor Design) en de **motivering**. Daarmee is elk Material Profile herleidbaar naar het bevestigde Concept, het bevestigde Floor Design en de onderbouwing van het voorstel.
- Er wordt **niets in de DesignContext geregistreerd** (buiten de DesignContext; motivering in het object) — analoog aan het Floor Design (Fase 2).

## 8. Robuustheid

- **Fouttolerantie:** elke boundary-aanroep in een `try/except`; een technische fout → gestructureerd foutresultaat, **nooit** een partieel of verzonnen Material Profile; DesignContext en het bevestigde Floor Design ongewijzigd.
- **Herstelgedrag:** gelimiteerde regeneratie (§5); Concept en het bevestigde Floor Design blijven behouden.
- **Uitbreidbaarheid:** het patroon validatie → boundary → kwaliteitsborging → resultaatwikkel is de herbruikbare blauwdruk; een echte, model-specifieke redenering wordt later geïnjecteerd **zonder** de component te wijzigen.
- **AI-model-onafhankelijk:** geen model of prompt vastgelegd; de boundary is de enige plek waar redenering plaatsvindt.
- **Additief:** nieuw bestand; geen wijziging aan `design_context.py` of `reasoning_engine.py`; geen koppeling aan de live pipeline tot er bewust wordt aangesloten.

---

## Besloten preconditie (TR-003 → AB-010A)

Het eerder openstaande punt is besloten: de Material Planner start **uitsluitend bij een bevestigd Floor Design** (`FloorDesign.status == "Bevestigd"`), conform BUILD-007 (r. 62, "het al vastgestelde Floor Design") en het consistente gate-patroon (elke stap start op een bevestigd upstream-object). Dit is vastgelegd in het amendement **AB-010A** en verwerkt in BUILD-012 en dit technisch ontwerp; de herkomst-referentie naar het Floor Design is daarmee enkelvoudig.

**Acceptatie:** met een bevestigd, volledig Concept en een **bevestigd Floor Design** levert de Material Planner één of meer `MaterialProfile`-objecten (status "Voorgesteld", met motivering en enkelvoudige herkomst) buiten de DesignContext; onvoldoende input, een afgekeurd resultaat of een technische fout leiden tot een signalering/foutresultaat en, waar van toepassing, gelimiteerde regeneratie — zonder mutatie van de DesignContext of het bevestigde Floor Design, zonder bevestiging en zonder zelf aan te vullen.
