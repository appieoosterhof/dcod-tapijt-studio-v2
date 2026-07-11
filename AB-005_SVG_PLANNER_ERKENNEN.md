# AB-005 — Concept-Architectuurbesluit: SVG Planner erkennen als de bestaande SVG-generatiepipeline

**Status:** concept, ter beoordeling. Geen enkel bestaand document en geen enkele regel code is gewijzigd. Uitwerking van agendapunt **T3** uit `ARCHITECTUUR_BESLUITVORMINGSAGENDA_FASE_2.md` (roadmap Sprint 1 — Opruiming; §5 markeert T3 als Architectuurbesluit + visiewijziging). Aanleiding: `AR-002_DESIGN_BRAIN_HARMONISATIE_ANALYSE.md`, aanbeveling 5.

**Vraagstelling:** moet de bestaande SVG-generatiepipeline architectonisch worden erkend als de component "SVG Planner" uit de interne opbouw van de Design Brain — dat wil zeggen: is SVG Planner geen nog te bouwen component, maar een reeds gerealiseerde die nooit formeel als zodanig is benoemd?

**Scope:** uitsluitend de naamserkenning van de bestaande SVG-pipeline als SVG Planner. Geen nieuwe functionaliteit, geen codewijziging, en geen uitspraak over de andere planners (Material Planner, Pattern Planner) of over hun aansturing.

---

## 1. Vastgestelde feiten

Uitsluitend letterlijke/ondubbelzinnige inhoud uit bestaande documenten, plus geverifieerde eigenschappen van de bestaande code:

- **F1.** `SPEC-000_PROJECT_CHARTER.md`, regel 48 (uitgangspunt), en `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, uitgangspunt 4 (regel 26): "de SVG-generator is uitsluitend een uitvoerende component — alle ontwerpintelligentie bevindt zich vóór de generator." Dit is een bevroren principe.
- **F2.** `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, interne opbouw van de Design Brain (regel 61): "Reasoning Engine → Material Planner / Pattern Planner / SVG Planner." SVG Planner is daar één van drie specialistische planners.
- **F3.** `SPEC-000_PROJECT_CHARTER.md`, §16 (regel 136) noemt SVG Planner letterlijk in de opsomming van componenten die "daarna wordt de Design Brain uitgewerkt als verzameling afzonderlijke componenten ... elk als eigen, gecontroleerde BUILD" — dus als (nog) te bouwen component. Bevestigd in `AB-001`, F8.
- **F4.** `AR-002_DESIGN_BRAIN_HARMONISATIE_ANALYSE.md`, harmonisatietabel (regel 32): "SVG Planner | Gelijk gebleven, al gerealiseerd (nooit formeel als zodanig erkend) | Bestaande SVG-generatiepipeline (`build_tile_svg()`, `build_repeat_svg()`, de ... generator-functies in `modules_extra.py`) | Deze rol bestaat al, van vóór de DesignContext-architectuur." Aanbeveling 5 (regel 86): "Formeel erkennen dat SVG Planner al bestaat ... een naamserkenning, geen codewijziging."
- **F5.** Geverifieerd in de bestaande implementatie:
  - `build_tile_svg()` (`app.py`, regel 465) en `build_repeat_svg()` (`app.py`, regel 623) vormen de pipeline die een tegel bouwt en tot een naadloos herhaald patroon samenstelt.
  - `STYLE_GENERATORS` (`app.py`, regel 432) koppelt stijl-sleutels aan generator-functies; de generator-functies zelf staan in `modules_extra.py`.
  - **Aantalsnuance:** `STYLE_GENERATORS` bevat 29 stijl-sleutels, waarvan enkele aliassen zijn (bijv. `persian` en `classic` verwijzen beide naar `generate_medallion_svg`), wat neerkomt op circa 27 distinct generator-functies. Het in de documenten genoemde getal "28" (F4, en `BUILD-001` regel 15) is daarmee een benadering, geen exact geverifieerd aantal — de strekking (een vaste set pure generators achter één pipeline) klopt wel.
- **F6.** `BUILD-001_DESIGNCONTEXT_INTEGRATIE.md`, regel 15, karakteriseert de generators in `modules_extra.py` als "pure SVG-generator-functies, input → SVG-string, zonder enige kennis van 'waarom' een kleur of stijl is gekozen." Dit bevestigt feitelijk de uitvoerende, niet-intelligente aard uit F1.
- **F7.** `svg_to_png()` (`app.py`, regel 696) bestaat, maar is volgens `CLAUDE.md` een STUB en behoort tot de Productie Engine (SVG → printklaar bestand), niet tot de SVG-generatie. Deze functie valt buiten de SVG Planner-rol.

## 2. Architectuurinterpretaties

Redeneringen die de feiten verbinden — zelf geen feit, wel direct herleidbaar:

- **I1.** F1 + F2 + F4 + F6 samen: de rol die "SVG Planner" in de Design Brain-opbouw invult — een uitvoerende component die een reeds bepaalde stijl/parameters omzet in een concrete SVG, zonder zelf te ontwerpen — is functioneel exact wat de bestaande pipeline (F5) al doet. De rol is niet nieuw; alleen de naam "SVG Planner" is er nooit aan gekoppeld.
- **I2.** F3 en F4 staan op gespannen voet: SPEC-000 §16 rekent SVG Planner tot de "nog te bouwen" componenten, terwijl AR-002 vaststelt dat hij al gerealiseerd is. Deze spanning is de kern van T3. Erkenning van de bestaande pipeline als SVG Planner beslecht die spanning ten gunste van "al gerealiseerd" — zonder SPEC-000 te wijzigen (SPEC-000 is bevroren; zie hoofdstuk 5).
- **I3.** SVG Planner is niet hetzelfde als Pattern Planner: F2 noemt beide als afzonderlijke planners. Erkennen dat de bestaande pipeline de SVG Planner ís, zegt niets over Pattern Planner, die een apart, nog niet gerealiseerd begrip blijft (hoort bij T9-gebied). Dit besluit vermengt de twee nadrukkelijk niet.

## 3. Architectuurkeuze

**K1.** De bestaande SVG-generatiepipeline — `build_tile_svg()` + `build_repeat_svg()` (`app.py`) plus de via `STYLE_GENERATORS` geregistreerde generator-functies (`modules_extra.py`) — wordt formeel erkend als de component **"SVG Planner"** uit de interne opbouw van de Design Brain (F2). SVG Planner is dus **geen nog te bouwen component, maar reeds gerealiseerd**.

**K2.** Deze erkenning bevestigt de rol van SVG Planner als **uitsluitend uitvoerende component** (F1/F6): hij vertaalt een reeds bepaalde stijl en parameters naar een concrete SVG en neemt zelf geen ontwerpbeslissingen.

**K3.** Dit is een **zuivere naamserkenning**: geen codewijziging, geen nieuwe functionaliteit, geen wijziging van gedrag van de pipeline.

## 4. Overwogen alternatieven

- **Alternatief 1 — SVG Planner als een alsnog nieuw te bouwen component beschouwen (SPEC-000 §16 letterlijk volgen).** *Afgewezen*: zou naast de bestaande, bewezen pipeline een tweede component met dezelfde uitvoerende rol introduceren — een tweede vocabulaire/implementatie voor dezelfde werkelijkheid, in strijd met AR-002 en met de opruimings-insteek van Sprint 1.
- **Alternatief 2 — SVG Planner erkennen én de bestaande pipeline meteen herstructureren/hernoemen in code.** *Afgewezen als onderdeel van dit besluit*: T3 is expliciet een naamserkenning zonder codewijziging (F4); herstructurering is geen onderdeel van deze keuze en zou de randvoorwaarde "introduceer geen nieuwe functionaliteit" schenden.
- **Alternatief 3 (voorgesteld) — Uitsluitend erkennen dat de bestaande pipeline de SVG Planner-rol al vervult, zonder code te raken en zonder uitspraak over de andere planners of hun aansturing.** Zie hoofdstuk 3. De enige lezing die consistent is met alle feiten (F1–F7).

## 5. Consequenties van het besluit

- SVG Planner geldt voortaan als een reeds gerealiseerde component. De vermeldingen in `SPEC-000` §16 (regel 136) en in de componentlijst van `DESIGN_BRAIN_ARCHITECTUURVISIE.md` (F2/F3), die SVG Planner nog als "nog te bouwen" presenteren, worden daarmee op dit punt achterhaald — maar worden **door dit besluit niet gewijzigd**. Correctie loopt mee in de latere SPEC-000-revisieronde (**T14/T15**) respectievelijk de herschrijving van de Architectuurvisie (**T12**).
- **Geen enkele codewijziging.** De pipeline blijft functioneel identiek; de bekende STUB `svg_to_png()` (Productie Engine, F7) valt buiten dit besluit en verandert niet.
- De **aansturing** van de SVG Planner (hoe een toekomstige Reasoning Engine/Pattern Planner de pipeline voedt) blijft open en hoort bij T4/T7/T9. Dit besluit legt uitsluitend vast wélke bestaande code de SVG Planner-rol vervult, niet hoe die wordt aangedreven.
- Het bevroren principe "SVG-generator is uitsluitend uitvoerend" (F1) wordt door dit besluit bevestigd, niet gewijzigd.

## 6. Scope-afbakening (wat dit besluit uitdrukkelijk niet doet)

- Het beslist **niet** over Pattern Planner, Material Planner of Reasoning Engine, noch over hun onderlinge bedrading (T4/T7/T9/T10).
- Het wijzigt **geen** code en introduceert **geen** functionaliteit; ook de `svg_to_png()`-stub (Productie Engine) blijft ongemoeid.
- Het herschrijft of corrigeert `SPEC-000` en de Architectuurvisie **niet** (T12/T14/T15).
- Het doet **geen** uitspraak over een eventuele toekomstige migratie van generators naar de Geometry Engine (bindende architectuurregel uit `CLAUDE.md`) — dat is een aparte, bestaande lijn.

## 7. Conclusie

Een **volledig** Architectuurbesluit is hier mogelijk: de rol bestaat aantoonbaar al in geverifieerde code (F5/F6), vervult exact de uitvoerende SVG Planner-functie uit de Design Brain-opbouw (F1/F2/I1), en de enige tegenspraak (SPEC-000 §16 "nog te bouwen", F3/I2) wordt beslecht zonder enig bevroren document of enige code te wijzigen. Het voorstel (hoofdstuk 3, K1–K3) wordt in zijn geheel ter goedkeuring voorgelegd.
