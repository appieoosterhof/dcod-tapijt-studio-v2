# AR-005 — Historisch architectuuronderzoek: de evolutie van de oorspronkelijke SVG Planner

**Status:** historisch onderzoek, ter kennisname. **Geen Architectuurbesluit.** Geen bestaand document gewijzigd, geen nieuw architectuurbegrip geïntroduceerd. Gebaseerd uitsluitend op: `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, `SPEC-000`, BUILD-001 t/m BUILD-007, AR-001 t/m AR-004, AB-001 t/m AB-005, `RELEASE_0.2_DESIGNCONTEXT_FOUNDATION.md`, en de huidige implementatie (`app.py`, `modules_extra.py`).

**Onderzoeksvraag:** *"Welke verantwoordelijkheden had de oorspronkelijke SVG Planner, en hoe hebben die verantwoordelijkheden zich ontwikkeld tot de huidige architectuur?"*

Bewijsniveaus: **expliciet** / **impliciet** / **niet aantoonbaar**.

---

## 0. Terminologische scheiding vooraf (bepalend voor het hele onderzoek)

Twee begrippen worden makkelijk verward; ze scheiden is noodzakelijk om de vraag eerlijk te beantwoorden:

- **[Feit]** De **oorspronkelijke SVG-generator** — de eerste Dessinator vóór DesignContext. `SPEC-000` regel 17: "Vóór de introductie van het DesignContext Model was de Dessinator in essentie een SVG-generator: een functie die tekst omzette in een patroon." `RELEASE_0.2` regel 17 beschrijft die pipeline concreet: "een prompt ging naar Claude, Claude gaf een JSON-analyse terug, keyword-matching bepaalde een stijl, en een generator-functie tekende een SVG." Dit is een brede pipeline (analyse + rendering).
- **[Feit]** De **"SVG Planner"** — een naam die pas in `DESIGN_BRAIN_ARCHITECTUURVISIE.md` is gemunt en dáár meteen is begrensd tot "uitsluitend een uitvoerende component" (uitgangspunt 4, regel 26). `AR-002` regel 32: de rol is "nooit formeel als zodanig erkend" onder die naam.

**[Interpretatie]** "De oorspronkelijke SVG Planner" bestaat strikt genomen niet: op het moment dat de eerste Dessinator draaide, bestond de náám SVG Planner nog niet. Wat bestond, was de brede SVG-generator. De naam "SVG Planner" is later toegekend aan uitsluitend het rendering-deel daarvan. Dit onderscheid is de kern van de falsificatie in hoofdstuk 4.

## 1. Verantwoordelijkheden van de oorspronkelijke SVG-generator (de eerste Dessinator)

Alle verantwoordelijkheden van de "rechte lijn" tekst→patroon, met bron en bewijsniveau:

- **R1 — Prompt-interpretatie / stijlanalyse.** `analyse_prompt()` (`app.py` regels 43–80) laat Claude een JSON teruggeven met o.a. `style`, `complexity`, `motif_size`, `shapes`. Bron: `app.py`; `RELEASE_0.2` regel 17. **Expliciet.**
- **R2 — Kleurpalet bepalen.** `analyse_prompt()` produceert het `palette`-object (achtergrond/primary/secondary/accenten). Bron: `app.py` regels 55–61; `BUILD-002_VOORSTEL`. **Expliciet.**
- **R3 — Stijl-routing (keuze welke generator/patroon).** Keyword-matching in `api_generate()` (`app.py` regels 833–843) én, apart, opnieuw in `build_tile_svg()` (regel 473). Bron: `app.py`; `RELEASE_0.2` regels 39, 78; `BUILD-002_VOORSTEL`. **Expliciet** (inclusief de vastgestelde dubbele routering).
- **R4 — Repeat-type bepalen (herhaalpatroon: full/half-drop/brick/mirror).** Geconsumeerd door `build_repeat_svg()`. Bron: `BUILD-003_VOORSTEL`. Let op: repeat-type "heeft nooit in `analysis` gezeten" — het kwam als request-parameter (`data.get("repeat_type","full")`), niet uit de AI-analyse. **Expliciet.**
- **R5 — SVG renderen (tegel bouwen + naadloos herhalen).** `build_tile_svg()` + `build_repeat_svg()` roepen de generator-functies in `modules_extra.py` aan. Bron: `app.py`; `BUILD-001` regel 15; `AB-005` F5. **Expliciet.**

**[Onbewezen aanname]** Dat de oorspronkelijke generator méér verantwoordelijkheden droeg dan R1–R5 (bijvoorbeeld materiaal- of ruimtelijke beslissingen). Geen bron toont dit; materiaal/ruimte kwamen pas met latere begrippen (Material Profile, Scene) en zaten niet in de eerste pipeline.

## 2. Ontwerp- versus technische verantwoordelijkheden

- **[Feit/Interpretatie] Ontwerpverantwoordelijkheden (beslissingen):** R1 (stijl/complexiteit/vormen), R2 (kleurpalet), R3 (patroonkeuze), R4 (repeat-type). Dit zijn keuzes over hóe het dessin eruitziet. Grondslag: `RELEASE_0.2` noemt kleurpalet en repeat-type expliciet "ontwerpbeslissingen" (regels 43, 49, 103).
- **[Feit/Interpretatie] Technische uitvoeringsverantwoordelijkheid:** uitsluitend R5 (rendering). `BUILD-001` regel 15 karakteriseert de generators als "input → SVG-string, zonder enige kennis van 'waarom'."

**[Interpretatie]** De oorspronkelijke generator verenigde dus ontwerpbeslissingen (R1–R4) én technische uitvoering (R5) in één pipeline — dat is de feitelijke basis onder elke "monoliet"-lezing (zie hoofdstuk 4).

## 3. Evolutie per verantwoordelijkheid

Classificatie: *overgenomen* (door welke component) / *nog SVG Planner* / *vervallen* / *niet aantoonbaar*.

| # | Verantwoordelijkheid | Aard | Huidige architectuurpositie | Bron | Bewijs | Classificatie |
|---|---|---|---|---|---|---|
| R1 | Prompt-interpretatie / stijl-, complexiteit-, vormanalyse | Ontwerp | **Niet gemigreerd.** Blijft in `analyse_prompt()`/`analysis`. Naast de generator is met BUILD-004 een aparte Context Interpreter gebouwd die visie/context interpreteert — een *nieuwe* interpretatie, geen overname van R1. | `RELEASE_0.2` r. 80–81; BUILD-004 Technisch r. 41–48 | Expliciet | Deels **nog bij de oorspronkelijke pipeline**; niet door SVG Planner en niet door Context Interpreter overgenomen |
| R2 | Kleurpalet bepalen | Ontwerp | **Overgenomen** door DesignContext (`Concept.kleurpalet`), met `analysis` als fallback. Generator-code onveranderd; alleen de *bron* verschoof. | `BUILD-002_VOORSTEL`; `RELEASE_0.2` r. 41–43 | Expliciet | **Overgenomen door DesignContext (Concept-laag)** |
| R3 | Stijl-routing (patroonkeuze) | Ontwerp | **Niet gemigreerd.** Nog steeds op twee plekken (`api_generate()` + `build_tile_svg()`); bewust niet gemigreerd wegens dubbele, mogelijk tegenstrijdige bron. | `RELEASE_0.2` r. 78, 81; `BUILD-002_VOORSTEL` | Expliciet | **Nog bij de oorspronkelijke pipeline** (deels binnen `build_tile_svg()`) |
| R4 | Repeat-type bepalen | Ontwerp | **Overgenomen** door DesignContext (`Productierealisatie.repeat_type`), geconsumeerd door `build_repeat_svg()`, met parameter-fallback. | `BUILD-003_VOORSTEL`; `RELEASE_0.2` r. 47–51 | Expliciet | **Overgenomen door DesignContext (Productierealisatie-laag)** |
| R5 | SVG renderen | Technisch | **Nog volledig SVG Planner.** `build_tile_svg()`/`build_repeat_svg()` + generators; ongewijzigd. | `AB-005` F5; `BUILD-001` r. 15 | Expliciet | **Nog steeds de SVG Planner** |

- **[Feit]** Complexiteit, motief-schaal, tegelmaat en resolutie zijn als migratiekandidaten benoemd maar **bewust niet gemigreerd** (`RELEASE_0.2` regel 80). Deze vallen onder R1 en blijven `analysis`-gestuurd.
- **[Feit]** De generator-functies zelf zijn nooit herbouwd of opgesplitst: "De bestaande generator-functies (28 stuks, in `modules_extra.py`) zijn stabiel ... niet opnieuw te bouwen" (`RELEASE_0.2` regel 21); BUILD-001 regel 5: "de SVG-generatoren ... blijven volledig intact."

## 4. Falsificatie: was de oorspronkelijke SVG Planner een monoliet die later is opgesplitst?

**Poging tot bevestiging én weerlegging, uitsluitend op bewijs.**

Bewijs dat de hypothese lijkt te steunen:
- De oorspronkelijke generator verenigde ontwerpbeslissingen (R1–R4) en uitvoering (R5) in één pipeline (hoofdstuk 2). Twee ontwerpbeslissingen (R2, R4) zijn daarna naar DesignContext-componenten verhuisd (hoofdstuk 3).

Bewijs dat de hypothese, zoals geformuleerd, **weerlegt:**
1. **[Feit]** De naam "SVG Planner" verwees nooit naar een monoliet. Op het moment dat de naam werd gemunt (Architectuurvisie), was hij al begrensd tot "uitsluitend uitvoerend" (uitgangspunt 4). Onder de naam *SVG Planner* was de component dus nooit breed. Wat breed was, heette "SVG-generator" (hoofdstuk 0).
2. **[Feit]** Het mechanisme was geen *opsplitsing van een component*, maar een *autoriteitsoverdracht van bronnen*: alleen de bron van R2/R4 verschoof naar DesignContext; de generator-code bleef intact en werd nooit gecarveld (`BUILD-001` r. 5; `BUILD-002` rollback "één functie, één regel"; `RELEASE_0.2` r. 21). Nieuwe intelligentie is vóór een ongewijzigde generator geplaatst, niet uit de generator gesneden.
3. **[Feit]** De overdracht is bovendien onvolledig: R1 en R3 (stijl, complexiteit, vormen) zijn nooit gemigreerd (`RELEASE_0.2` r. 80–81). Een "voltooide opsplitsing" is er dus sowieso niet.

**[Interpretatie — conclusie van de falsificatie]** De hypothese wordt **niet bevestigd zoals geformuleerd.** Correcter is: de oorspronkelijke *SVG-generator* (niet de "SVG Planner") verenigde beslissing en uitvoering; van die beslissingen zijn er twee (kleurpalet, repeat-type) naar DesignContext-lagen overgedragen via bron-verschuiving, terwijl de rendering-code intact bleef. De "SVG Planner" is de naam voor het overgebleven, altijd al tot uitvoering begrensde deel — geen monoliet die is opgeknipt, maar het residu na gedeeltelijke externalisatie.

## 5. Antwoord op de deelvragen (geen besluit)

1. **Welke verantwoordelijkheden vervulde de oorspronkelijke SVG Planner?** Strikt: de oorspronkelijke *SVG-generator* vervulde R1–R5 (hoofdstuk 1). De component *onder de naam SVG Planner* vervulde vanaf zijn benoeming uitsluitend R5.
2. **Ontwerpverantwoordelijkheden:** R1, R2, R3, R4 (hoofdstuk 2) — **expliciet**.
3. **Technische uitvoeringsverantwoordelijkheden:** uitsluitend R5 — **expliciet**.
4. **Later overgenomen door andere componenten:** R2 → DesignContext (Concept-laag, BUILD-002); R4 → DesignContext (Productierealisatie-laag, BUILD-003). R1/R3 zijn **niet** overgenomen en resteren in de `analysis`-pipeline. **Expliciet.**
5. **Vandaag aantoonbaar nog over bij de SVG Planner:** uitsluitend R5, de rendering — plus, feitelijk maar niet-architectonisch, een deel van R3 (stijl-routing zit nog fysiek in `build_tile_svg()`). **Expliciet.**
6. **Kleiner geworden dan de oorspronkelijke architectuurrol, of altijd al beperkt?** [Interpretatie] De *architectuurrol "SVG Planner"* was **altijd al beperkt** (execution-only vanaf de benaming). De *implementatie* is niet aantoonbaar kleiner geworden: de generator-code bleef intact; alleen twee invoerbronnen (R2, R4) verhuisden upstream. Wat kromp was niet de SVG Planner maar de reikwijdte van de bredere oorspronkelijke *SVG-generator*, doordat beslissingen eruit werden geëxternaliseerd. De lezing "de implementatie is kleiner dan haar architectuurrol" wordt dus **niet** ondersteund; eerder het omgekeerde — de implementatie draagt vandaag nog steeds iets (R3-routing) dat de architectuurrol (execution-only) haar niet toekent.

**[Onbewezen aanname, expliciet]** Dat de resterende stijl-routing (R3) in `build_tile_svg()` bewust tot de SVG Planner-rol behoort. Geen bron bevestigt dit; `RELEASE_0.2` (r. 78) merkt het juist aan als een bekende, nog niet geconsolideerde inconsistentie.

Dit onderzoek levert uitsluitend deze constateringen; het neemt geen besluit, introduceert geen begrip en doet geen wijzigingsvoorstel.
