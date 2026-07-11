# AR-006 — Historisch architectuuronderzoek: de intentie achter de externalisatie in BUILD-002 en BUILD-003

**Status:** historisch onderzoek, ter kennisname. **Geen Architectuurbesluit.** Geen bestaand document gewijzigd, geen nieuw architectuurbegrip geïntroduceerd. Gebaseerd uitsluitend op: BUILD-001, BUILD-002 (voorstel), BUILD-003 (voorstel + advies), `RELEASE_0.2_DESIGNCONTEXT_FOUNDATION.md`, `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, `SPEC-000`, en de historische implementatie (`app.py`).

**Onderzoeksvraag:** *"Was BUILD-002 en BUILD-003 aantoonbaar bedoeld als tussenstap naar volledige externalisatie van ontwerpbeslissingen, of was het expliciet de bedoeling dat bepaalde ontwerpbeslissingen permanent in de generator zouden blijven?"*

Bewijsniveaus: **aantoonbaar feit** / **architectuurinterpretatie** / **onbewezen aanname**.

---

## 1. Welke ontwerpbeslissingen zijn in BUILD-002 en BUILD-003 daadwerkelijk geëxternaliseerd?

- **[Feit]** BUILD-002 externaliseerde het **kleurpalet**: `build_tile_svg()` leest het palet uit `DesignContext.concept.kleurpalet`, met `analysis["palette"]` als fallback. Bron: `BUILD-002_VOORSTEL` (Doel, Definition of Done); `RELEASE_0.2` regels 41–43.
- **[Feit]** BUILD-003 externaliseerde het **repeat-type**: `build_repeat_svg()` leest het uit `DesignContext.productierealisatie.repeat_type`, met parameter-fallback. Bron: `BUILD-003_VOORSTEL`; `RELEASE_0.2` regels 47–51.
- **[Feit]** In beide gevallen verschoof uitsluitend de **bron** van de waarde; de generator-code bleef intact. Bron: `BUILD-001` regel 58 ("Hun interne werking verandert niet — alleen waar ze hun input vandaan halen"); `BUILD-002` rollback ("één functie, één regel").

## 2. Welke ontwerpbeslissingen bleven in de generator / niet-gemigreerd?

- **[Feit]** **Stijl** bleef ongemigreerd en wordt op twee plekken bepaald (`api_generate()` én `build_tile_svg()`); expliciet "bewust buiten scope (Fase 5)". Bron: `BUILD-003_ADVIES` §1-tabel; `RELEASE_0.2` regels 78, 81.
- **[Feit]** **Complexiteit, motief-schaal, tegelmaat, resolutie, vormen** zijn als kandidaten geïnventariseerd maar "bewust niet meegenomen". Bron: `RELEASE_0.2` regel 80; `BUILD-003_ADVIES` §2–§4.
- **[Feit]** BUILD-003_ADVIES classificeert daarbij expliciet: tegelmaat/resolutie zijn "puur dimensionale doorgifte, geen ontwerpbeslissing"; motief-schaal is "definitorisch twijfelachtig ... eerder een technisch renderparameter". Bron: `BUILD-003_ADVIES` §2, §4-C.
- **[Interpretatie]** "Bleef in de generator" geldt strikt alleen voor wat fysiek in `build_tile_svg()` zit: de stijl-routing (deel van R3) en de motief-schaal-berekening. Complexiteit en vormen leven in de `analysis`-laag (vóór de generator), niet in de generator zelf.

## 3. Is er expliciet beschreven dat de migratie later zou worden voortgezet?

- **[Feit]** Ja, voor specifieke beslissingen:
  - `BUILD-002_VOORSTEL`: stijl "blijft bewust bij Fase 5 van BUILD-001 horen" — een benoemde toekomstige fase.
  - `BUILD-001` §8 ("Gefaseerde implementatie", Fase 1–5): een expliciet gefaseerd integratieplan; Fase 4 = generatorfuncties lezen uit DesignContext.
  - `BUILD-003_ADVIES`: stijl "bewust buiten scope (Fase 5)"; motief-schaal "wel als goede kandidaat voor een latere BUILD bewaren".
  - `RELEASE_0.2` regel 78: over stijl — "pas daarna is het verantwoord om een beslissing te migreren die twee ... bronnen moet vervangen door één".
  - `RELEASE_0.2` regel 89: de uitgangspunten "blijven leidend voor toekomstig werk op DesignContext".
- **[Interpretatie]** Voortzetting van de migratie is dus **expliciet voorzien** — maar telkens voor *benoemde, afzonderlijke* beslissingen (met name stijl), niet als een toezegging om àlles te externaliseren.

## 4. Is er expliciet beschreven dat resterende ontwerpbeslissingen bewust in de generator moesten blijven?

- **[Feit]** **Nee.** Geen van de bronnen bevat een uitspraak dat enige ontwerpbeslissing *permanent* of *definitief* in de generator moet blijven. De niet-gemigreerde beslissingen worden telkens omschreven als *uitgesteld* ("Fase 5", "latere BUILD", "bewust niet meegenomen"), niet als *permanent behouden*.
- **[Feit]** Het bevroren einddoel-principe wijst juist de andere kant op: `DESIGN_BRAIN_ARCHITECTUURVISIE.md` uitgangspunt 4 en `SPEC-000` regel 48 — "de SVG-generator is uitsluitend een uitvoerende component — alle ontwerpintelligentie bevindt zich vóór de generator."
- **[Interpretatie]** De optie "bepaalde ontwerpbeslissingen blijven permanent in de generator" wordt door geen enkel document ondersteund en staat op gespannen voet met uitgangspunt 4. Deze pool van de onderzoeksvraag is dus **niet aantoonbaar** en wordt door het einddoel-principe eerder tegengesproken.

## 5. Welke feiten ondersteunen welke conclusie?

- **Voortzetting voorzien (tussenstap-richting):** `BUILD-002` (Fase 5), `BUILD-001` §8, `BUILD-003_ADVIES` (Fase 5 / latere BUILD), `RELEASE_0.2` r. 78/89. **Aantoonbaar.**
- **Einddoel = intelligentie vóór de generator:** uitgangspunt 4 / `SPEC-000` r. 48. **Aantoonbaar als principe** (visie), niet als migratieprogramma.
- **Geen permanente retentie:** afwezigheid van enige retentie-uitspraak + uitgangspunt 4. **Aantoonbaar (als afwezigheid van tegenbewijs).**

## 6. Falsificatie van de hypothese "gefaseerde migratie naar volledige externalisatie"

**Actief gezocht tegenbewijs — en gevonden:**

1. **[Feit]** `RELEASE_0.2` regel 80: de niet-gemigreerde velden zijn "bewust niet meegenomen — elke migratie in deze release had een eigen, specifiek architectonisch doel, **geen kwantitatieve voortgang** ('zoveel mogelijk velden migreren')." Dit verwerpt expliciet de lezing dat de migraties bedoeld waren om richting *volledige* externalisatie te tellen.
2. **[Feit]** `RELEASE_0.2` regel 21: DesignContext nam autoriteit over "stap voor stap ... **nooit meer dan wat op dat moment kon worden aangetoond als veilig**." De drijfveer was bewijsbaarheid/veiligheid per stap, niet een einddoel van volledigheid.
3. **[Feit]** BUILD-002 en BUILD-003 rechtvaardigen elke migratie door een *specifiek architectonisch punt* te bewijzen (BUILD-002: veiligste single-source; BUILD-003: gedeelde autoriteit over twee functies), niet door de generator leeg te maken. Bron: `BUILD-002_VOORSTEL` (Waarom veiligste eerste migratie); `BUILD-003_VOORSTEL` (Doel), `BUILD-003_ADVIES` §5.
4. **[Feit]** BUILD-003_ADVIES classificeert sommige resterende parameters expliciet als *géén ontwerpbeslissing* (tegelmaat/resolutie: "puur dimensionale doorgifte"; motief-schaal: "eerder een technisch renderparameter"). "Volledige externalisatie van ontwerpbeslissingen" zou deze dus sowieso niet betreffen.

**[Interpretatie — uitkomst van de falsificatie]** De hypothese wordt **niet in haar sterke vorm bevestigd.** Wat aantoonbaar is: de migratie was **bedoeld om te worden voortgezet** voor benoemde beslissingen (met name stijl). Wat **niet** aantoonbaar is: dat BUILD-002/003 waren opgezet als fasen van een toegezegd programma richting *volledige* externalisatie — die framing wordt door `RELEASE_0.2` r. 80 juist afgewezen. En de tegenpool (permanente retentie) is evenmin aantoonbaar (hoofdstuk 4).

## 7. Welke conclusies mogen niet worden getrokken?

- **[Mag niet]** "BUILD-002/003 waren fasen van een plan naar volledige externalisatie van alle ontwerpbeslissingen." — niet aantoonbaar; `RELEASE_0.2` r. 80 verwerpt de kwantitatieve lezing.
- **[Mag niet]** "Het was expliciet de bedoeling dat bepaalde ontwerpbeslissingen permanent in de generator zouden blijven." — geen enkel document zegt dit; uitgangspunt 4 spreekt het tegen.
- **[Mag niet]** "Stijl blijft definitief in de generator." — het tegendeel is expliciet: stijl is *uitgesteld* naar Fase 5, niet behouden.
- **[Mag niet]** "Motief-schaal/tegelmaat/resolutie zijn ontwerpbeslissingen die nog geëxternaliseerd moeten worden." — deels tegengesproken: BUILD-003_ADVIES classificeert ze (deels) als technische renderparameters, geen ontwerpbeslissingen.

## 8. Antwoord op de onderzoeksvraag (geen besluit)

- **[Aantoonbaar feit]** BUILD-002 en BUILD-003 externaliseerden kleurpalet en repeat-type, telkens door bron-verschuiving met behoud van de generator-code.
- **[Aantoonbaar feit]** Voortzetting van de migratie voor specifieke, benoemde beslissingen (met name stijl, Fase 5) is expliciet voorzien.
- **[Aantoonbaar feit]** Nergens staat dat een ontwerpbeslissing *permanent* in de generator moest blijven; het bevroren einddoel-principe (uitgangspunt 4) wijst het tegenovergestelde aan als richting.
- **[Architectuurinterpretatie]** De juiste lezing ligt tússen de twee polen van de onderzoeksvraag: geen toegezegd programma naar *volledige* externalisatie én geen bedoelde *permanente* retentie, maar een **doel-gedreven, veiligheid-eerst, open-einde migratie** waarin elke stap een eigen architectonisch punt bewees, met voortzetting voorzien voor benoemde beslissingen en een visie-principe dat naar externalisatie van *intelligentie* (niet per se elke parameter) neigt.
- **[Onbewezen aanname, expliciet]** Dat "volledige externalisatie" ooit als concreet, afgebakend einddoel is vastgesteld. Het bestaat alleen als richtinggevend principe (uitgangspunt 4), niet als vastgelegd programma — en mag daarom niet als voldongen intentie worden aangenomen.

Dit onderzoek levert uitsluitend deze constateringen; het neemt geen besluit, introduceert geen begrip en doet geen wijzigingsvoorstel.
