# AR-002 — Harmonisatie DESIGN_BRAIN_ARCHITECTUURVISIE.md: analyse en voorstel

**Status:** analyse en voorstel, ter beoordeling. **Geen enkel bestaand document is in dit document gewijzigd.** Geen nieuwe BUILD, geen architectuurbesluit — uitsluitend een inventarisatie en een lijst met punten die zelf een expliciet Architectuurbesluit vereisen voordat er iets wordt herschreven. Vervolg op AR-001, bevinding 2.1 ("twee onverzoende architectuurketens").

---

## 0. Werkwijze

Elk architectuurbegrip uit `DESIGN_BRAIN_ARCHITECTUURVISIE.md` is nagelopen tegen de inmiddels vastgestelde architectuur (SPEC-000, DESIGN_CONTEXT_MODEL.md, BUILD-001 t/m BUILD-007, VISION-001) en in precies één van vijf categorieën geplaatst:

- **Gelijk gebleven** — begrip en betekenis onveranderd terug te vinden.
- **Hernoemd** — zelfde betekenis, andere, inmiddels gangbare naam.
- **Opgesplitst** — één begrip is in de gerealiseerde architectuur meerdere, elk eigen-verantwoordelijkheid-dragende begrippen geworden.
- **Vervallen** — het begrip zelf bestaat niet meer als zelfstandig architectuurobject, hetzij omdat het gedrag is geworden in plaats van een component, hetzij omdat het overbodig is gebleken.
- **Nog niet gerealiseerd** — het begrip is nog geldig, maar er is nog geen BUILD die het daadwerkelijk heeft gebouwd of technisch gepositioneerd.

Waar de categorisering zelf een architectuurbesluit vereist (bijvoorbeeld: welke van twee mogelijke lezingen is de juiste), is dat expliciet zo benoemd in hoofdstuk 6 — dit document beslist dat niet zelf.

## 1. Volledige inventarisatie

| Begrip (Architectuurvisie) | Categorie | Huidige tegenhanger | Toelichting |
|---|---|---|---|
| Projectcontext | Hernoemd (in de praktijk al toegepast) | Project-/Ruimtecontext (DesignContext Model, laag 2) | De koppeling stond al voorgeschreven in Regel 1 van het brondocument zelf; BUILD-004 gebruikt al de DesignContext Model-naam. De formele afronding van Regel 1 heeft alleen nooit plaatsgevonden. |
| Ontwerpintentie | Hernoemd (in de praktijk al toegepast) | Ontwerpvisie (DesignContext Model, laag 1) | Idem — al voorgeschreven in Regel 1, al toegepast in BUILD-004, nooit formeel afgesloten. |
| Ontwerpsignatuur | Gelijk gebleven, nog niet gerealiseerd | SPEC-000 §17 (begrippenlijst, ongewijzigde definitie) | Begrip en definitie bestaan nog onveranderd. Heeft geen plek in de BUILD-007-keten (Project → Ontwerpvraag → ... ) — geen vervallen begrip, wel een onbeantwoorde vraag wáár in de keten het wordt vastgelegd. |
| DCOD Design Brain | Gelijk gebleven | SPEC-000 §17, BUILD-005 Technisch Ontwerp §5 | Definitie letterlijk herhaald en bevestigd, geen wijziging. |
| "Context" (interne Design Brain-stap in het oorspronkelijke ontwerpketen-diagram) | Hernoemd/verduidelijkt (al toegepast) | Context Interpreter (BUILD-004) | Regel 2 van het brondocument benoemt deze stap zelf al als "Context Interpreter"; zo gebouwd. |
| "Strategie" (interne Design Brain-stap) | Nog niet gerealiseerd | Ontwerpstrategie (DesignContext Model, laag 3) | Regel 2 schreef hiervoor een eigen, afzonderlijke bouwstap voor ("Ontwerpstrategie (eigen stap)"), tussen Context Interpreter en Reasoning Engine. Die BUILD bestaat nog niet, en ontbreekt ook als aparte naam in de BUILD-007-keten. Zie hoofdstuk 3. |
| Reasoning Engine | Nog niet gerealiseerd, relatie tot Floor Design nog niet bevestigd | — | Zie hoofdstuk 3. |
| Material Planner | Nog niet gerealiseerd, relatie tot Material Profile nog niet bevestigd | — | Zie hoofdstuk 4. |
| Pattern Planner | Nog niet gerealiseerd, relatie tot Reasoning Engine/Floor Design nog niet bevestigd | — | Zie hoofdstuk 3. |
| SVG Planner | Gelijk gebleven, al gerealiseerd (nooit formeel als zodanig erkend) | Bestaande SVG-generatiepipeline (`build_tile_svg()`, `build_repeat_svg()`, de 28 generator-functies in `modules_extra.py`) | Deze rol bestaat al, van vóór de DesignContext-architectuur (SPEC-000 §6: "de SVG-generator is uitsluitend een uitvoerende component"). Nooit als "SVG Planner" benoemd, wel functioneel identiek. |
| Mock-up | Opgesplitst | Scene (BUILD-006) + Floor Visualization Engine (VISION-001/BUILD-007) + Visualisatie (BUILD-007) | Eén ongedifferentieerde eindstap is drie afzonderlijke architectuurobjecten geworden, elk met een eigen, in BUILD-007 vastgelegde verantwoordelijkheid. |
| Iteratieve verfijning | Vervallen als zelfstandig begrip, blijft bestaan als gedrag | BUILD-007 Functioneel Ontwerp, fase 8 (Visualisatie): "vanaf hier kan het gesprek weer terug... zonder dat eerdere stappen overnieuw hoeven" | Niet langer een aparte stap in het diagram, wel een expliciet beschreven eigenschap van de keten. Niet te verwarren met de Conversation Planner-lus — zie hoofdstuk 5. |
| Design Reasoning | Gelijk gebleven onder canonieke naam | Ontwerpredenering (DesignContext Model, doorlopende laag) | Regel 1 schreef deze koppeling zelf al voor; "Design Reasoning" is nooit zelfstandig gebouwd. Let op: naamsovereenkomst met "Reasoning Engine" — dit zijn twéé verschillende begrippen in het brondocument. Zie hoofdstuk 5. |
| Conversation Planner | Gelijk gebleven, gerealiseerd (ontworpen, nog niet geïmplementeerd) | BUILD-005 | Geen wijziging. |
| De vijf Uitgangspunten (Conversatie is de ontwerpmotor / Projectcontext is leidend / Snelheid is een harde ontwerpregel / SVG-generator is uitvoerend / Collecties zijn optioneel) | Gelijk gebleven | SPEC-000 §6, letterlijk overgenomen | Al volledig geharmoniseerd, geen actie nodig. |

## 2. Vier architectuurregels van het brondocument — status

- **Regel 1 (canonieke woordenschat):** gedeeltelijk uitgevoerd in de praktijk (zie Projectcontext/Ontwerpintentie/Context/Design Reasoning hierboven), maar nooit als het voorgeschreven, zelfstandige artefact opgeleverd. Dit document is in feite de achterstallige, formele uitvoering van die eigen precondition.
- **Regel 2 (Ontwerpstrategie als eigen stap):** niet uitgevoerd. Zie hoofdstuk 3.
- **Regel 3 (eigenaarschap propageert omlaag):** consequent gevolgd (bevestigd in AR-001, sterke punten).
- **Regel 4 (gecontroleerde migratie, één component per keer):** consequent gevolgd (BUILD-004 → BUILD-005 → BUILD-006-patroon).

## 3. Verdieping: Ontwerpstrategie-stap, Reasoning Engine, Pattern Planner en Floor Design

Het oorspronkelijke ontwerpketen-diagram plaatst, ná Context Interpreter, twee stappen vóórdat er iets concreets ontstaat: eerst **Ontwerpstrategie (eigen stap)**, dan **Reasoning Engine**, die op zijn beurt drie specialistische planners aanstuurt: **Material Planner / Pattern Planner / SVG Planner**.

BUILD-007 Technisch Ontwerp (hoofdstuk 8) benoemt zelf al een open vraag: *"Precieze afleiding van Floor Design uit DesignContext... nog niet vastgelegd."* De twee documenten spreken elkaar hier niet tegen — ze passen juist op elkaar: de Ontwerpstrategie-stap en de Reasoning Engine uit `DESIGN_BRAIN_ARCHITECTUURVISIE.md` zijn sterke kandidaten om precies dát gat te vullen. Concreet, als hypothese die bevestiging behoeft:

- **Ontwerpstrategie (eigen stap)** en **Reasoning Engine** zijn de nog te bouwen verwerkende componenten die tussen Conversation Planner en Floor Design zitten in de BUILD-007-keten, maar daar nog geen eigen naam hebben gekregen.
- **Pattern Planner** is vermoedelijk de specifieke, nog te bouwen component die Floor Design als resultaat oplevert (het "Patroon"-deel van de oorspronkelijke Materiaal/Patroon/SVG-groepering).
- Onbeslist is of **Reasoning Engine** en **Pattern Planner** twee opeenvolgende componenten zijn (Reasoning Engine bepaalt de algemene richting, Pattern Planner werkt die uit tot Floor Design), of dat het twee namen zijn voor dezelfde, nog niet geconsolideerde verantwoordelijkheid.

Dit is nadrukkelijk een voorstel ter beoordeling, geen vaststaand feit — zie besluitpunt 2 en 3 in hoofdstuk 6.

## 4. Verdieping: Material Planner versus Material Profile (expliciet gevraagd)

Dit zijn twee begrippen van een verschillende aard, geen twee namen voor hetzelfde:

- **Material Planner** (`DESIGN_BRAIN_ARCHITECTUURVISIE.md`, ook genoemd in SPEC-000 §16) is een **verwerkende component** — onderdeel van de nog te bouwen Design Brain.
- **Material Profile** (BUILD-007) is expliciet geclassificeerd als een **resultaat-object**, geen verwerkende component (BUILD-007 Technisch Ontwerp, hoofdstuk 1): "de visuele en materiële eigenschappen... van de gekozen vloerafwerking."

De meest voor de hand liggende, coherente lezing — dezelfde structuur als Reasoning Engine/Pattern Planner ten opzichte van Floor Design (hoofdstuk 3) — is dat **Material Planner de nog te bouwen component is die Material Profile als resultaat oplevert.** Dit sluit rechtstreeks aan bij een gat dat AR-001 al signaleerde (bevinding 2.3: BUILD-007 hoofdstuk 8 mist de vraag naar de afleiding van Material Profile, terwijl die vraag voor Floor Design wel is gesteld) — Material Planner is een sterke kandidaat om exact die ontbrekende vraag te beantwoorden.

Dit is, net als bij Reasoning Engine/Pattern Planner, een voorstel ter bevestiging — zie besluitpunt 4.

## 5. Bijvangst: een naamscollisie binnen het brondocument zelf

Twee verschillende begrippen in `DESIGN_BRAIN_ARCHITECTUURVISIE.md` delen het woord "Reasoning", zonder dat het document zelf dat onderscheidt:

- **Reasoning Engine** — een verwerkende component in de ontwerpketen (Context → Strategie → **Reasoning** → Materiaal/Patroon/SVG).
- **Design Reasoning** — de term die in Regel 1 expliciet aan **Ontwerpredenering** wordt gekoppeld: de doorlopende laag die niet beslist, maar bewaakt waarom iets is besloten (DesignContext Model, hoofdstuk 7).

Dit is geen gevolg van BUILD-007 — deze dubbelzinnigheid bestond al in het brondocument zelf, vóórdat BUILD-004 t/m BUILD-007 werden geschreven. Ze is tot nu toe onopgemerkt gebleven omdat "Design Reasoning" verder nergens als zelfstandig gebouwd component is opgedoken. Wordt Reasoning Engine ooit gebouwd, dan is een eigen, onderscheidende naam nodig om verwarring met Ontwerpredenering/Design Reasoning te voorkomen — zie besluitpunt 7.

## 6. Punten die een expliciet Architectuurbesluit vereisen

Onderstaande punten worden hier **niet** besloten. Elk vereist een aparte, expliciete goedkeuring voordat `DESIGN_BRAIN_ARCHITECTUURVISIE.md` (of enig ander document) wordt aangepast:

1. **Projectcontext → Project-/Ruimtecontext en Ontwerpintentie → Ontwerpvisie** formeel vastleggen als afgeronde hernoemingen (grotendeels al staande praktijk, laag risico).
2. Bevestigen of **Ontwerpstrategie (eigen stap)** en **Reasoning Engine** de nog-onbeantwoorde "hoe wordt Floor Design afgeleid uit DesignContext"-vraag uit BUILD-007 hoofdstuk 8 mogen invullen, en zo ja: één gecombineerde toekomstige BUILD, of twee aparte.
3. Bevestigen of **Pattern Planner** een zelfstandig component is naast Reasoning Engine, of dat beide dezelfde verantwoordelijkheid beschrijven en tot één naam moeten worden geconsolideerd.
4. Bevestigen dat **Material Planner** de nog te bouwen component is die **Material Profile** als resultaat oplevert — inclusief het expliciet aanvullen van de in AR-001 (bevinding 2.3) gesignaleerde ontbrekende open vraag in BUILD-007 hoofdstuk 8.
5. Formeel erkennen dat **SVG Planner** al bestaat (de huidige `build_tile_svg()`/`build_repeat_svg()`-pipeline) — een naamserkenning, geen codewijziging.
6. Bevestigen dat **Mock-up** als verouderd, opgesplitst begrip vervalt ten gunste van Scene / Floor Visualization Engine / Visualisatie.
7. Besluiten hoe wordt omgegaan met de naamscollisie **Reasoning Engine ↔ Design Reasoning** (bijvoorbeeld: "Design Reasoning" als term laten vervallen ten gunste van uitsluitend "Ontwerpredenering", Reasoning Engine ongemoeid laten).
8. Besluiten of **Ontwerpsignatuur** alsnog een plek krijgt in de BUILD-007-keten, en zo ja waar, of bewust buiten scope blijft tot een latere fase.
9. Besluiten of de **BUILD-007-keten** voortaan geldt als de actuele, gezaghebbende ontwerpketen — zodat het diagram in `DESIGN_BRAIN_ARCHITECTUURVISIE.md` wordt vervangen in plaats van dat er twee diagrammen naast elkaar blijven bestaan.

## 7. Voorstel voor het vervolg (proces, geen inhoud)

Zodra de bovenstaande negen punten zijn beoordeeld, kan `DESIGN_BRAIN_ARCHITECTUURVISIE.md` worden herschreven tot één geharmoniseerd document — of vervangen door een nieuw, bijgewerkt architectuurdocument dat de BUILD-007-keten als uitgangspunt neemt. Welke van beide vorm krijgt, is zelf ook geen keuze die dit document maakt; dat volgt pas ná de Architectuurbesluiten hierboven.

Geen enkel bestaand document — inclusief `DESIGN_BRAIN_ARCHITECTUURVISIE.md` zelf — is in dit proces gewijzigd.
