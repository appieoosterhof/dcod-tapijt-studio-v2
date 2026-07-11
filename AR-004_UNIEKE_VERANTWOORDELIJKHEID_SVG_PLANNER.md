# AR-004 — Architectuuronderzoek: de unieke architectuurverantwoordelijkheid van de SVG Planner

**Status:** onderzoek, ter kennisname. **Geen Architectuurbesluit.** Geen bestaand document gewijzigd, geen nieuw architectuurbegrip geïntroduceerd, geen wijzigingsvoorstel gedaan. Gebaseerd uitsluitend op: `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, `SPEC-000_PROJECT_CHARTER.md`, BUILD-001 t/m BUILD-007, AR-001 t/m AR-003, AB-001 t/m AB-005, en de geverifieerde implementatie (`app.py`, `modules_extra.py`).

**Onderzoeksvraag:** *"Welke unieke architectuurverantwoordelijkheid heeft de SVG Planner?"*

Elk hoofdstuk scheidt: **[Feit]** (letterlijk/ondubbelzinnig in bron of code), **[Interpretatie]** (redenering uit meerdere feiten), **[Onbewezen aanname]** (in geen enkele bron aantoonbaar).

---

## 0. Bewijsbasis

- **F1.** `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, uitgangspunt 4 (regel 26): "De SVG-generator is uitsluitend een uitvoerende component. Alle ontwerpintelligentie bevindt zich vóór de generator." (bevroren principe, letterlijk herhaald in `SPEC-000`, regel 48).
- **F2.** `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, interne opbouw (regel 61): "Reasoning Engine → Material Planner / Pattern Planner / SVG Planner." SVG Planner is één van drie samen genoemde planners.
- **F3.** `SPEC-000`, §16 (regel 136): SVG Planner wordt letterlijk opgesomd als een van de Design Brain-componenten die "elk als eigen, gecontroleerde BUILD" worden uitgewerkt.
- **F4.** `SPEC-000`, hoofdstuk 2 (regel 17): "Vóór de introductie van het DesignContext Model was de Dessinator in essentie een SVG-generator: een functie die tekst omzette in een patroon." De visie plaatst nieuwe intelligentie vóór die bestaande pipeline (regel 48).
- **F5.** `AR-002`, harmonisatietabel (regel 32): SVG Planner = "Gelijk gebleven, al gerealiseerd (nooit formeel als zodanig erkend)"; de rol "bestaat al, van vóór de DesignContext-architectuur." Aanbeveling 5 (regel 86): "een naamserkenning, geen codewijziging." (Formeel erkend in AB-005.)
- **F6.** `BUILD-001`, regel 15: de generators in `modules_extra.py` zijn "pure SVG-generator-functies, input → SVG-string, zonder enige kennis van 'waarom' een kleur of stijl is gekozen."
- **F7.** Geverifieerde code: de patroon-/stijlbeslissing valt in `analyse_prompt()` (`app.py`, regel 43; het veld `"style"`, regel 55) en in de routing-guards van `api_generate()` (`app.py`, regels 833–843). `build_tile_svg()` leest die beslissing (`style = analysis.get("style", ...)`, regel 473) en voert haar uit via `STYLE_GENERATORS` → een generator. De beslissing valt dus vóór, de uitvoering ín de SVG-pipeline.
- **F8.** `AR-003` (dit traject): de SVG Planner komt uitsluitend voor in Diagram A (Design Brain-opbouw) en ontbreekt volledig in de BUILD-007-keten (Diagram B). Geen architectuurobject is als zijn in- of uitvoer vastgelegd; zijn enige aantoonbare contract is het code-niveau `analysis`-dict → SVG-string.
- **F9.** Geen enkel document definieert de afzonderlijke verantwoordelijkheid van Material Planner, Pattern Planner en SVG Planner ten opzichte van elkaar; zij worden uitsluitend samen genoemd als "drie specialistische planners" (`AR-002`, regel 48). AB-001/AB-002 behandelen Reasoning Engine/Pattern Planner als kandidaat-vullers van DesignContext-lagen 3/4, maar geven de SVG Planner nergens een eigen, onderscheiden taakomschrijving.

## 1. Waarom is de SVG Planner oorspronkelijk in de Architectuurvisie opgenomen?

- **[Feit]** De Dessinator wás vóór DesignContext in essentie een SVG-generator (F4). De visie herpositioneert die generator als uitvoerende sluitpost, met alle nieuwe intelligentie ervóór (F1), en noemt "SVG Planner" als één van drie planners onder de Reasoning Engine (F2), tevens in de componentenlijst van SPEC-000 §16 (F3).
- **[Interpretatie]** De SVG Planner is opgenomen om de reeds bestaande SVG-generator een benoemde, begrensde en ondergeschikte plaats in de nieuwe architectuur te geven — niet om een nieuwe capaciteit toe te voegen. De opname dient om de verantwoordelijkheid van de generator te *begrenzen* ("uitsluitend uitvoerend"), zodat er ruimte vóór hem ontstaat voor de nieuwe intelligentie. Dit sluit aan op F5 ("gelijk gebleven, al gerealiseerd").
- **[Onbewezen aanname]** Dat de SVG Planner bedoeld was als volwaardige, zelfstandige architectuurcomponent naast Material/Pattern Planner, mét eigen beslisdomein. De bronnen dragen dit niet: zij noemen hem als component (F2/F3) maar karakteriseren hem tegelijk als intelligentievrij (F1/F6), zonder die twee te verzoenen.

## 2. Welke verantwoordelijkheid heeft de SVG Planner die niet al door een andere component wordt uitgevoerd?

- **[Feit]** Geen andere component in beide diagrammen produceert een SVG-string: Context Interpreter produceert DesignContext-velden, Conversation Planner een procesuitkomst, Floor Visualization Engine een (samengesteld) Visualisatie-beeld (BUILD-007 Technisch, regels 42/43/47/48). De SVG-string zelf wordt uitsluitend door `build_tile_svg()`/`build_repeat_svg()` voortgebracht (F7).
- **[Interpretatie]** De enige verantwoordelijkheid die nergens anders wordt uitgevoerd, is het *technisch renderen*: een reeds bepaalde stijl + parameters omzetten in een concrete SVG. Die specifieke handeling is uniek voor de SVG Planner.
- **[Feit]** De *beslissing* welk patroon/stijl wordt gebruikt, is niet van de SVG Planner: die valt upstream in `analyse_prompt()` en de routing-guards (F7). De SVG Planner voert uit, beslist niet.

## 3. Is die verantwoordelijkheid architectonisch of uitsluitend technisch?

- **[Feit]** F1 definieert de rol expliciet als "uitsluitend een uitvoerende component"; F6 bevestigt "zonder enige kennis van 'waarom'"; F7 toont dat de beslissing upstream valt.
- **[Interpretatie]** De verantwoordelijkheid is **uitsluitend technisch** (rendering). Architectonisch draagt de SVG Planner geen eigenaarschap, geen ontwerpbeslissing en geen interpretatie — de architectuur definieert hem juist als het punt wáár de intelligentie ophoudt. Zijn enige "architecturale" betekenis is het markeren van de uitvoeringsgrens; dat is een principe/grens (F1), geen zelfstandig gedragen verantwoordelijkheid.
- **[Onbewezen aanname]** Dat de rendering-stap een eigen architecturaal beslisdomein bevat (bijvoorbeeld patroon-compositie als ontwerpkeuze). De code weerspreekt dit eerder dan dat ze het steunt (F7: dispatch op een reeds gekozen `style`).

## 4. Is de SVG Planner een zelfstandige architectuurcomponent of een implementatieservice?

- **[Feit]** SPEC-000 §16 (F3) en de Architectuurvisie (F2) benoemen hem als "component." Tegelijk heeft hij geen architectuurobject-contract (F8) en is hij een pure functie input → SVG (F6).
- **[Interpretatie]** In gedrag is de SVG Planner een **implementatieservice**: staatloos, input→output, zonder eigenaarschap, beslissing of interpretatie — anders dan de overige Design Brain-componenten, die elk wél eigenaarschap of interpretatie dragen (Context Interpreter: interpretaties; Conversation Planner: procesregie; Reasoning Engine/Planners: beoogde inhoudsproductie). De benaming "component" (F3) en de karakterisering "intelligentievrije uitvoering" (F1) staan op gespannen voet; geen document verzoent die spanning.
- **[Onbewezen aanname]** Dat de SVG Planner op één architecturaal niveau staat met de andere planners. Dit is een naamgevingssuggestie (samen opgesomd, F2/F9), geen aantoonbaar vastgelegde gelijkwaardigheid.

## 5. Welke architectuurobjecten consumeert en produceert de SVG Planner aantoonbaar?

- **[Feit]** **Geen.** Aantoonbaar consumeert hij een code-niveau `analysis`-dict (F7, `app.py` regel 473) en produceert hij een SVG-string (F7, `build_repeat_svg`). Geen van beide is een gedefinieerd architectuurobject; er is geen architectuurobject als zijn in- of uitvoer vastgelegd (F8).
- **[Interpretatie]** Op architectuurniveau consumeert en produceert de SVG Planner dus *niets aantoonbaars*. Zijn contract leeft volledig op code-niveau.

## 6. Zijn deze contracten expliciet vastgelegd of alleen afleidbaar uit de code?

- **[Feit]** Alleen afleidbaar uit de code. Het contract `analysis`-dict → SVG-string staat in `app.py`/`modules_extra.py` (F7), niet in enig architectuurdocument. Geen document benoemt de in-/uitvoer van de SVG Planner als architectuurobjecten (F8).
- **[Interpretatie]** Er is een expliciet *code*-contract en geen enkel *architectuur*-contract. Dat is exact het patroon van een implementatieservice, niet van een contract-dragende architectuurcomponent.

## 7. Heeft de SVG Planner een unieke architectuurverantwoordelijkheid? — onderbouwing met bewijs

- **[Interpretatie, gedragen door F1–F9]** De SVG Planner heeft een unieke **technische** verantwoordelijkheid (het renderen van de SVG), maar **geen unieke architectuurverantwoordelijkheid.** Onderbouwing, uitsluitend uit bewijs:
  1. Hij is per definitie intelligentievrij en uitvoerend (F1, F6).
  2. De beslissing die hij uitvoert, valt aantoonbaar upstream (F7).
  3. Hij draagt geen architectuurobject-contract; in-/uitvoer zijn uitsluitend code-artefacten (F8, hoofdstukken 5–6).
  4. Hij ontbreekt volledig in de vastgestelde BUILD-007-keten en bestaat alleen in het oudere, niet-verzoende Diagram A (F8).
  5. Geen document onderscheidt zijn architectuurverantwoordelijkheid van die van de Pattern Planner; ze worden alleen samen genoemd (F9).
- **[Interpretatie]** Wat resteert als "architecturaal" aan de SVG Planner is niet een verantwoordelijkheid maar een *grens*: hij markeert waar ontwerpintelligentie eindigt en pure uitvoering begint (F1). Een grens/principe is geen zelfstandig gedragen verantwoordelijkheid.
- **[Onbewezen aanname, expliciet als zodanig gemarkeerd]** Dat aan de SVG Planner tóch een eigen architectuurverantwoordelijkheid toekomt (bijvoorbeeld patroon-compositie of een eigen contract richting de Floor Visualization Engine). Voor deze lezing is in geen enkele bron bewijs; ze wordt hier niet aangenomen en niet weerlegd — alleen als onbewezen benoemd.

## 8. Antwoord op de onderzoeksvraag (geen besluit)

- **Aantoonbaar:** de SVG Planner heeft één unieke *technische* verantwoordelijkheid — het produceren van de SVG-string uit een reeds bepaalde stijl/parameters (F6/F7). Deze handeling wordt nergens anders uitgevoerd.
- **Aantoonbaar:** de SVG Planner heeft **geen** aantoonbare unieke *architectuur*verantwoordelijkheid: hij is gedefinieerd als intelligentievrije uitvoering (F1), draagt geen eigenaarschap of beslissing (F7), heeft geen architectuurobject-contract (F8), en is van de vastgestelde keten afwezig (F8).
- **Interpretatie:** de SVG Planner gedraagt zich als een **implementatieservice** met een expliciet code-contract en geen architectuur-contract; architectonisch fungeert hij als de *uitvoeringsgrens* van de Design Brain, niet als een beslissing-dragende component.
- **Onbewezen (open in de bronnen):** de spanning tussen "component" (SPEC-000 §16) en "intelligentievrije uitvoering" (uitgangspunt 4), en de ontbrekende afbakening ten opzichte van de Pattern Planner, blijven onopgelost — maar het oplossen daarvan is een besluit, niet een constatering, en valt buiten dit onderzoek.

Dit onderzoek levert uitsluitend deze constateringen; het neemt geen besluit, introduceert geen begrip en doet geen wijzigingsvoorstel.
