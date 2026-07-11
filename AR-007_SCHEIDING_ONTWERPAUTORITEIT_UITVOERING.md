# AR-007 — Architectuuronderzoek: scheiding tussen ontwerpautoriteit en uitvoeringsverantwoordelijkheid

**Status:** onderzoek, ter kennisname. **Geen Architectuurbesluit.** Geen bestaand document gewijzigd, geen nieuw architectuurbegrip geïntroduceerd. Gebaseerd uitsluitend op: `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, `SPEC-000`, `DESIGN_CONTEXT_MODEL.md`, BUILD-001 t/m BUILD-007, AR-001 t/m AR-006, AB-001 t/m AB-005, en de huidige implementatie (uitsluitend ter verificatie, nooit als norm).

**Onderzoeksvraag:** *"Bestaat er in de huidige architectuur een expliciete scheiding tussen ontwerpautoriteit en uitvoeringsverantwoordelijkheid?"*

Bewijsniveaus: **aantoonbaar feit** / **architectuurinterpretatie** / **onbewezen aanname**.

---

## 0. Wat de bronnen onder de twee begrippen verstaan (geen nieuwe begrippen)

- **[Feit] Ontwerpautoriteit** — het recht om een ontwerpbeslissing *definitief te bevestigen*. Het DesignContext Model kent dit per laag toe: Ontwerpvisie = architect (onaantastbaar na bevestiging), Ontwerpstrategie = gezamenlijk (DCOD + architect), Concept en Materialisatie = gedeeld (DCOD stelt voor, architect stuurt bij), Productierealisatie = DCOD. Bron: `DESIGN_CONTEXT_MODEL.md` regel 174 (kernuitspraak) en de laaghoofdstukken.
- **[Feit] Uitvoeringsverantwoordelijkheid** — het omzetten van reeds genomen beslissingen in een resultaat, zonder eigen beslissing. Bron: `DESIGN_BRAIN_ARCHITECTUURVISIE.md` uitgangspunt 4 ("de SVG-generator is uitsluitend een uitvoerende component — alle ontwerpintelligentie bevindt zich vóór de generator"); `SPEC-000` regel 48.

## 1. Componenten die aantoonbaar ontwerpbeslissingen nemen (of bevestigen)

- **[Feit] De architect (mens)** bevestigt definitief; alleen de architect maakt een interpretatie tot vastgestelde ontwerpbeslissing. Bron: `BUILD-004` Technisch hoofdstuk 0; `DESIGN_BRAIN_ARCHITECTUURVISIE.md` Regel 3 (regels 66–70). **Expliciet.** — Dit is echter geen softwarecomponent.
- **[Feit] Geen enkele softwarecomponent** mag zelfstandig een ontwerpbeslissing definitief bevestigen die volgens het model eigendom is van de architect of van de gezamenlijke dialoog. Bron: `DESIGN_BRAIN_ARCHITECTUURVISIE.md` Regel 3. **Expliciet.**
- **[Feit] AI-componenten (Context Interpreter; toekomstig Reasoning Engine, Material/Pattern Planner)** produceren *interpretaties/voorstellen*, nooit bevestigde waarheden. Bron: `BUILD-004` Technisch hoofdstuk 0; Context Interpreter-output heeft status uitsluitend "voorgesteld" (BUILD-004 Technisch regel 46). **Expliciet.**
- **[Interpretatie]** Er is dus geen softwarecomponent die *ontwerpautoriteit* draagt. Componenten *stellen voor*; de autoriteit ligt bij de mens/gezamenlijke dialoog.

## 2. Componenten die uitsluitend eerder genomen beslissingen uitvoeren

- **[Feit] SVG Planner** — uitsluitend uitvoerend (rendering), geen beslissing. Bron: uitgangspunt 4; `AB-005`; `AR-004`. **Expliciet** (met één inconsistentie, zie §4).
- **[Feit] Floor Visualization Engine** — voegt Floor Design + Material Profile + Scene samen tot een beeld; resultaat-artefact Visualisatie heeft "geen eigen verwerkingslogica". Bron: `BUILD-007` Technisch regels 47–48. **Expliciet.**
- **[Feit] Scene Builder** — standaardiseert ruimte-invoer tot één Scene; geen ontwerpbeslissing over de vloer. Bron: `BUILD-006`; `BUILD-007` Technisch regel 46. **Expliciet.**
- **[Feit] Design Transfer Package** — bundelt reeds bevestigde inhoud; geen eigen beslissing. Bron: `BUILD-007` Technisch regel 49. **Expliciet.**

## 3. Autoriteit versus uitvoering per component

| Component | Ontwerpautoriteit | Uitvoeringsverantwoordelijkheid | Bron | Bewijs |
|---|---|---|---|---|
| Architect (mens) | Definitief bevestigen (m.n. Ontwerpvisie) | — | `DESIGN_CONTEXT_MODEL` r. 174; Regel 3 | Expliciet |
| DesignContext | Geen — *registreert* eigenaarschap/autoriteit per laag, beslist zelf niet | — (container) | `BUILD-007` Technisch r. 41; `DESIGN_CONTEXT_MODEL` | Expliciet |
| Context Interpreter | Geen — produceert voorstellen (status "voorgesteld") | Interpreteren/structureren van vrije tekst | `BUILD-004` Technisch h. 0, r. 46 | Expliciet |
| Conversation Planner | Geen — schrijft geen ontwerpinhoud weg | Procesregie (één vervolgstap kiezen) | `BUILD-005`; `AB-001` F6; `DESIGN_BRAIN` r. 64 | Expliciet |
| Reasoning Engine / Material Planner / Pattern Planner | Geen (voorstellend) — bedoeld als vullers van lagen 3/4, "interpretaties, nooit waarheden" | Nog niet gebouwd | `AB-001` deel A; `BUILD-004` h. 0 | Impliciet (nog niet gerealiseerd) |
| SVG Planner | Geen | Uitsluitend renderen (SVG) | uitgangspunt 4; `AB-005`; `AR-004` | Expliciet |
| Scene Builder / Scene | Geen | Ruimte-invoer standaardiseren | `BUILD-006`; `BUILD-007` Technisch r. 46 | Expliciet |
| Floor Visualization Engine | Geen | Drie objecten samenvoegen tot beeld | `BUILD-007` Technisch r. 47 | Expliciet |
| Design Transfer Package | Geen | Bevestigde inhoud bundelen | `BUILD-007` Technisch r. 49 | Expliciet |

- **[Interpretatie]** De tabel toont geen tweedeling maar een *drie*deling: (a) autoriteit = architect/gezamenlijke dialoog (mens); (b) voorstellen/interpreteren = de AI-componenten; (c) uitvoeren = SVG Planner, Scene Builder, FVE, Design Transfer Package. De scheiding "autoriteit ↔ uitvoering" bestaat, maar met een tussenlaag ertussen en met de autoriteit buiten de software.

## 4. Is er een consistent patroon van stapsgewijze verwijdering van ontwerpautoriteit uit uitvoerende componenten?

- **[Feit]** BUILD-002 en BUILD-003 verplaatsten de *bron* van twee ontwerpbeslissingen (kleurpalet, repeat-type) uit de generator-invoer naar DesignContext. Bron: `BUILD-002`, `BUILD-003`, `RELEASE_0.2` r. 41–51; `AR-005`, `AR-006`.
- **[Interpretatie]** Dit is consistent mét uitgangspunt 4 (intelligentie vóór de generator) en vormt een zichtbaar patroon van *bron-externalisatie*.
- **[Feit — tegenbewijs, actief gezocht]:**
  1. De **stijl-routing** (een ontwerpbeslissing) zit nog fysiek in de uitvoerende functie `build_tile_svg()` en is nooit verwijderd — een bekende, niet-geconsolideerde inconsistentie. Bron: `RELEASE_0.2` r. 78; `AR-004`, `AR-005`.
  2. `RELEASE_0.2` r. 81: "DesignContext is geen volledige autoriteit ... de bestaande `analysis`-dictionary blijft voor het overgrote deel van de beslissingen (stijl, complexiteit, vormen) de bron van waarheid."
  3. `RELEASE_0.2` r. 80 en `AR-006`: er is geen toegezegd programma naar volledige externalisatie; "geen kwantitatieve voortgang".
  4. Wat verplaatst is, is de *bron/afhankelijkheid* van een beslissing — niet "autoriteit die de generator ooit bezat". De generator bezat nooit *autoriteit* (het bevestigde niets); hij bezat *invoerafhankelijkheid*. Bron: `AR-005` (falsificatie), `AR-004`.
- **[Interpretatie — uitkomst]** Het patroon is **reëel maar onvolledig en niet als programma vastgelegd.** Bovendien is de nauwkeurige formulering niet "autoriteit uit uitvoerende componenten verwijderd", maar "beslissingsbronnen naar DesignContext verplaatst"; de uitvoerende component hield hoe dan ook geen autoriteit.

## 5. Waar het bewijs ophoudt en interpretatie begint

- **Bewezen (expliciet):**
  - Een expliciet *principe* van scheiding bestaat: uitgangspunt 4 (uitvoering intelligentievrij) + Regel 3 (componenten bevestigen niet) + het interpretaties-principe (BUILD-004 h. 0).
  - Ontwerpautoriteit is *per laag* expliciet toegekend in het bevroren DesignContext Model, met de architect/gezamenlijke dialoog als houder.
  - De uitvoerende componenten (SVG Planner, Scene Builder, FVE, Design Transfer Package) zijn expliciet uitvoerend.
- **Interpretatie (begint hier):**
  - Dat deze losse feiten samen één *consistent, doorgevoerd* scheidingspatroon vormen. Het principe is expliciet; de volledige *realisatie* ervan niet (stijl-routing in de generator; DesignContext "geen volledige autoriteit").
  - Dat de scheiding een tweedeling is. De bronnen ondersteunen eerder een driedeling (autoriteit/voorstellen/uitvoering), met autoriteit buiten de software.
- **Niet aantoonbaar (mag niet geconcludeerd):**
  - Dat de scheiding *volledig* is doorgevoerd in de architectuur of implementatie.
  - Dat elke uitvoerende component vandaag aantoonbaar vrij is van ontwerpbeslissingen (de stijl-routing weerlegt dit voor de SVG Planner).

## 6. Antwoord op de onderzoeksvraag (geen besluit)

- **[Aantoonbaar feit]** Ja, er bestaat een **expliciete scheiding op principe- en eigenaarschapsniveau**: het beginsel dat uitvoerende componenten intelligentievrij zijn (uitgangspunt 4) en dat geen component definitief bevestigt (Regel 3), plus de expliciete toekenning van ontwerpautoriteit per laag in het bevroren DesignContext Model.
- **[Aantoonbaar feit]** Die scheiding is **niet volledig gerealiseerd**: een ontwerpbeslissing (stijl-routing) zit nog in een uitvoerende component, en DesignContext is expliciet "geen volledige autoriteit".
- **[Architectuurinterpretatie]** De architectuur scheidt in de praktijk *drie* rollen, niet twee: autoriteit (mens/gezamenlijke dialoog), voorstellen (AI-componenten) en uitvoering (renderende/samenvoegende componenten). "Ontwerpautoriteit versus uitvoering" is dus expliciet als *principe*, maar de twee worden gescheiden dóór een voorstellende tussenlaag, en geen component draagt zelf ontwerpautoriteit.
- **[Onbewezen aanname, expliciet]** Dat deze scheiding als een afgerond, consistent doorgevoerd architectuurpatroon geldt. Het is een expliciet *principe* met een *gedeeltelijke* realisatie; het als voltooid patroon aannemen gaat verder dan het bewijs.

Dit onderzoek levert uitsluitend deze constateringen; het neemt geen besluit, introduceert geen begrip en doet geen wijzigingsvoorstel.
