# AR-003 — Architectuuronderzoek: contractuele in- en uitvoer per component in de ontwerpketen

**Status:** onderzoek, ter kennisname. **Geen Architectuurbesluit.** Geen enkel bestaand document is gewijzigd, geen nieuw architectuurobject geïntroduceerd. Uitsluitend gebaseerd op bestaande documenten: `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, `SPEC-000_PROJECT_CHARTER.md`, BUILD-001 t/m BUILD-007, AR-001, AR-002, AB-001 t/m AB-004 (en, waar het over reeds erkende code gaat, AB-005 en de geverifieerde implementatie).

**Onderzoeksvraag:** *"Welk architectuurobject vormt de contractuele invoer en uitvoer van iedere component in de ontwerpketen?"*

**Bewijsniveaus:** *expliciet* = letterlijk in een document benoemde interface; *impliciet* = alleen via redenering uit meerdere plaatsen af te leiden, niet letterlijk benoemd; *niet aantoonbaar* = geen enkel document legt dit vast.

---

## 1. Vooraf: er zijn twee niet-verzoende ketendiagrammen

Elke uitspraak over "de ontwerpketen" hangt af van wélk diagram men bedoelt. Er bestaan er twee, en ze zijn nooit met elkaar verzoend (dit is agendapunt T12):

- **Diagram A — Design Brain-opbouw** (`DESIGN_BRAIN_ARCHITECTUURVISIE.md`, regels 16–19 en 60–61):
  `... → DCOD Design Brain (Context Interpreter → Ontwerpstrategie → Reasoning Engine → Material Planner / Pattern Planner / SVG Planner) → Mock-up → Iteratieve verfijning`
- **Diagram B — BUILD-007-keten** (`BUILD-007 ... FUNCTIONEEL`, regel 9; `... TECHNISCH`, hoofdstuk 1–4):
  `Project → Ontwerpvraag → DesignContext → Context Interpreter → Conversation Planner → Floor Design → Material Profile → Scene → Floor Visualization Engine → Visualisatie → Design Transfer Package → DCOD`

**Aantoonbaar feit:** de enige componenten die in béíde diagrammen voorkomen zijn **DesignContext, Context Interpreter en Conversation Planner**. De begrippen **Ontwerpstrategie-stap, Reasoning Engine, Material Planner, Pattern Planner en SVG Planner** komen uitsluitend in Diagram A voor; **Floor Design, Material Profile, Scene, Floor Visualization Engine, Visualisatie en Design Transfer Package** uitsluitend in Diagram B. Dit is bepalend voor de falsificatie in hoofdstuk 3.

## 2. Contract per component

Per component: geconsumeerd object → geproduceerd object, met bron en bewijsniveau. Uitsluitend bestaande objecten; geen nieuwe geïntroduceerd.

### DesignContext (domeinmodel / container — beide diagrammen)
- **Geconsumeerd:** n.v.t. — DesignContext is geen verwerkende component maar de gedeelde container die wordt gelezen/geschreven. Wordt beschreven door Ontwerpvraag (vrije tekst toegevoegd) en Context Interpreter (interpretaties). Bron: BUILD-007 Technisch, regels 41, 57–58. **Expliciet.**
- **Geproduceerd:** zichzelf als toestand; leverend object voor Conversation Planner, Floor Design-afleiding en Design Transfer Package. Bron: BUILD-007 Technisch, regels 59, 61, 66. **Expliciet.**

### Context Interpreter (verwerkende component — beide diagrammen)
- **Geconsumeerd:** vrije tekst (Ontwerpvraag) + optionele basisprojectgegevens + bestaande DesignContext-inhoud. Bron: BUILD-004 Technisch, hoofdstuk 3 (regel 45), BUILD-007 Technisch, regel 58. **Expliciet.**
- **Geproduceerd:** een deel van een `DesignContext`-object — de velden `ontwerpvisie` en `projectcontext`, status uitsluitend "voorgesteld", elke interpretatie met een eigen mate van zekerheid. Bron: BUILD-004 Technisch, hoofdstuk 3 (regel 46). **Expliciet.**

### Conversation Planner (verwerkende component — beide diagrammen)
- **Geconsumeerd:** uitsluitend `DesignContext.interpretaties`. Bron: BUILD-007 Technisch, regel 59; BUILD-005. **Expliciet.**
- **Geproduceerd:** **geen architectuurobject.** Levert precies één procesuitkomst (vraag / samenvatting ter bevestiging / voldoende vastgesteld) en schrijft nadrukkelijk geen ontwerpinhoud weg. Bron: BUILD-007 Technisch, regel 43; `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, regel 64; AB-001, F6. **Expliciet (dat het géén object produceert).**
- **Aandachtspunt:** Diagram B tekent "Conversation Planner → Floor Design", maar dit is een *vertakking/trigger*, geen productie-relatie (BUILD-007 Technisch, regel 60: "gaat de keten door naar Floor Design"). De Conversation Planner produceert Floor Design dus niet.

### Floor Design (resultaat-object — alleen Diagram B)
- **Geconsumeerd / afgeleid uit:** de op dat moment vastgelegde inhoud van DesignContext — maar "de precieze afleiding is een open punt, geen vastgesteld mechanisme". Bron: BUILD-007 Technisch, regels 44, 61 (hoofdstuk 8); AB-001, hoofdstuk 7. **Invoercontract: niet aantoonbaar** (expliciet als open verklaard).
- **Producerende component:** geen. "Geen enkel document noemt een component die Floor Design creëert." Bron: AB-002, regel 55. **Niet aantoonbaar.**
- **Geproduceerd / geleverd aan:** Material Profile, Floor Visualization Engine, Design Transfer Package. Bron: BUILD-007 Technisch, regels 62, 64, 66; AB-002, regels 24, 49–50. **Expliciet (uitvoerzijde).**
- **Interne objectvorm:** "Nieuw, nog niet technisch uitgewerkt". Bron: BUILD-007 Technisch, regel 27. **Niet aantoonbaar.**

### Material Profile (resultaat-object — alleen Diagram B)
- **Geconsumeerd / afgeleid uit:** "bepaald in samenhang met het al vastgestelde Floor Design — nooit andersom". Bron: BUILD-007 Technisch, regel 62. **Expliciet (relatie tot Floor Design); mechanisme/producent impliciet-tot-niet-aantoonbaar** (analoog aan Floor Design; agendapunt T6).
- **Geproduceerd / geleverd aan:** Floor Visualization Engine, Design Transfer Package. Bron: BUILD-007 Technisch, regels 64, 66. **Expliciet.**
- **Interne objectvorm:** "Nieuw, nog niet technisch uitgewerkt". Bron: BUILD-007 Technisch, regel 28. **Niet aantoonbaar.**

### SVG Planner (verwerkende component — alleen Diagram A; erkend in AB-005)
- **Geconsumeerd:** in de geverifieerde code een `analysis`-dict (stijl/palet/parameters), via `STYLE_GENERATORS` naar een generator-functie. Bron: `app.py` (`build_tile_svg`, regel 465; `STYLE_GENERATORS`, regel 432); AB-005, F5. **Code-contract expliciet; architectuur-contract (wélk architectuurobject de invoer vormt) niet aantoonbaar** — geen document benoemt een architectuurobject als invoer van de SVG Planner.
- **Geproduceerd:** een SVG-string (tegel/naadloos patroon via `build_repeat_svg`). Bron: `app.py`, regel 623; AB-005, F5. **Code-contract expliciet.**
- **Downstream-bestemming in de architectuur:** in Diagram A voedde de Design Brain (incl. SVG Planner) → Mock-up. Mock-up is echter opgeheven (AB-004) en in Diagram B vervangen door Scene/FVE/Visualisatie zónder SVG Planner. De architecturale bestemming van de SVG Planner-uitvoer is daardoor nergens meer gedefinieerd. **Niet aantoonbaar.**

### Scene Builder → Scene (verwerkende component → resultaat-object — alleen Diagram B)
- **Scene Builder geconsumeerd:** ruwe ruimte-invoer — een geüploade achtergrondafbeelding + vier handmatig vastgelegde vloerhoeken. Bron: BUILD-006, regels 11–13, 22–23. **Expliciet.**
- **Scene Builder geproduceerd:** een `Scene`-object (één achtergrond + één vloerpolygon `[TL,TR,BL,BR]`), opgeslagen als `scene.json`. Bron: BUILD-006, regels 14, 21, 26, 30. **Expliciet.**
- **Scene (object) geleverd aan:** Floor Visualization Engine; onafhankelijk aangeleverd, geen afhankelijkheid van Floor Design of Material Profile. Bron: BUILD-007 Technisch, regels 63–64. **Expliciet.**

### Floor Visualization Engine (verwerkende component — alleen Diagram B)
- **Geconsumeerd:** Floor Design + Material Profile + Scene — uitsluitend deze drie gestandaardiseerde objecten, "nooit rechtstreeks met DesignContext of met de ruwe scene-brongegevens". Bron: BUILD-007 Technisch, regels 47, 64, 117; AR-001, regel 48; VISION-001, regel 19. **Expliciet.**
- **Geproduceerd:** Visualisatie (resultaat-artefact, geen eigen verwerkingslogica). Bron: BUILD-007 Technisch, regels 48, 65. **Expliciet.**
- **Aandachtspunt:** hóe de FVE uit "Floor Design" een gerenderd beeld maakt — en of daarvoor de SVG-uitvoer van de SVG Planner nodig is — wordt nergens vastgelegd. **Niet aantoonbaar** (zie hoofdstuk 4, gat 4).

### Design Transfer Package (resultaat-object/bundeling — alleen Diagram B)
- **Geconsumeerd:** DesignContext (visie) + Floor Design + Material Profile + Visualisatie. Bron: BUILD-007 Technisch, regels 49, 66. **Expliciet.**
- **Geproduceerd:** één gebundeld geheel, geleverd aan DCOD (mens; geen technische interface). Bron: BUILD-007 Technisch, regels 49, 67. **Expliciet.**
- **Aandachtspunt (asymmetrie, T11/AR-001 2.2):** Design Transfer Package leest DesignContext (visie) wél rechtstreeks, terwijl de FVE dat expliciet niet mag. Beide consumeren Floor Design. Bron: BUILD-007 Technisch, regels 47, 49. **Expliciet (de asymmetrie zelf).**

## 3. Falsificatie: is Floor Design het contractobject van de SVG Planner?

**Poging tot bevestiging.** Gezocht is naar één document dat Floor Design benoemt als invoer óf uitvoer van de SVG Planner.

**Bevinding — de bewering is niet aantoonbaar en wordt gefalsifieerd:**

1. SVG Planner komt uitsluitend in Diagram A voor; Floor Design uitsluitend in Diagram B (hoofdstuk 1). Geen enkel document plaatst beide in dezelfde keten.
2. De expliciet benoemde consumenten van Floor Design zijn Material Profile, Floor Visualization Engine en Design Transfer Package (BUILD-007 Technisch, regels 62/64/66; AB-002 regel 24) — **de SVG Planner staat daar niet tussen.**
3. Het enige aantoonbare invoer-contract van de SVG Planner is het code-niveau `analysis`-dict → SVG-string (AB-005, F5). Dat is geen Floor Design; Floor Design is bovendien "nog niet technisch uitgewerkt" (BUILD-007 Technisch, regel 27) en kan dus onmogelijk aantoonbaar het invoerformaat van een bestaande functie zijn.
4. De enige (indirecte) koppeling die ooit bestond, liep via Diagram A: Design Brain → **Mock-up**. Dat begrip is opgeheven (AB-004) en in Diagram B vervangen zonder SVG Planner. De koppeling is daarmee vervallen, niet vervangen.

**Conclusie van de falsificatie:** Floor Design is **niet** aantoonbaar het contractobject van de SVG Planner. Er is geen enkele bronverwijzing die de twee als in- of uitvoer van elkaar vastlegt.

## 4. Waar de architectuur een contract of objectdefinitie mist

Uitsluitend geconstateerd, niet opgelost (dat zou een besluit zijn):

1. **Producent van Floor Design ontbreekt.** Geen component is aangewezen die Floor Design creëert (AB-002, regel 55). Diagram B suggereert de Conversation Planner via plaatsing, maar die produceert geen ontwerpinhoud (hoofdstuk 2). → agendapunten T5/T9.
2. **Afleidingscontract DesignContext → Floor Design ontbreekt.** Expliciet open verklaard (BUILD-007 Technisch, hoofdstuk 8; AB-001, hoofdstuk 7). → T5/T7/T9.
3. **Architectuur-invoercontract van de SVG Planner ontbreekt.** Er bestaat een code-contract (`analysis` → SVG), maar geen architectuurobject is als invoer gedefinieerd. Het is niet Floor Design (hoofdstuk 3); wat het wél is (Concept? een nog te definiëren patroon-specificatie? DesignContext-inhoud?) is nergens vastgelegd. → hangt samen met T4/T7/T9/T12.
4. **Koppeling SVG-uitvoer ↔ visualisatieketen ontbreekt.** De FVE consumeert Floor Design + Material Profile + Scene en produceert een beeld, maar nergens staat of, en hoe, de door de SVG Planner geproduceerde SVG daarin terechtkomt (bevat Floor Design een SVG? roept de FVE de SVG Planner aan? is de SVG een eigenschap van Material Profile?). → T9/T11/T12.
5. **Afleiding/producent van Material Profile ontbreekt.** Alleen de relatie "in samenhang met Floor Design" is benoemd; het mechanisme en de producerende component niet (BUILD-007 Technisch, regel 62). → T6/T10.
6. **Interne objectvorm van Floor Design, Material Profile en Visualisatie ontbreekt.** Alle drie "nog niet technisch uitgewerkt" (BUILD-007 Technisch, regels 27, 28, 31). Zonder objectdefinitie is een sluitend contract per definitie niet vast te stellen.

## 5. Antwoord op de onderzoeksvraag (geen besluit)

- Voor het **reeds geïmplementeerde deel van de keten** (DesignContext, Context Interpreter, Conversation Planner, Scene Builder/Scene) zijn de contractobjecten **expliciet** vastgelegd: DesignContext is het gedeelde container-object; Context Interpreter consumeert vrije tekst en produceert DesignContext-velden; Conversation Planner consumeert `DesignContext.interpretaties` en produceert géén object maar een procesuitkomst; Scene Builder consumeert ruwe ruimte-invoer en produceert een Scene.
- Voor het **nog niet gebouwde deel** (Floor Design, Material Profile, Floor Visualization Engine, Visualisatie, Design Transfer Package) is de **uitvoerzijde** grotendeels expliciet (wie wat consumeert), maar de **invoer-/afleidings- en producentzijde** van Floor Design en Material Profile is **niet aantoonbaar**.
- **Er bestaat geen enkel architectuurobject dat aantoonbaar de contractuele invoer én uitvoer van de SVG Planner vormt binnen de vastgestelde keten.** In het bijzonder is Floor Design dat niet (hoofdstuk 3). De SVG Planner heeft een geverifieerd *code*-contract, maar geen *architectuur*-contract — dat is de belangrijkste ontbrekende schakel (hoofdstuk 4, gat 3 en 4).

Dit onderzoek levert uitsluitend deze constateringen; het neemt geen besluit en beveelt geen wijziging aan.
