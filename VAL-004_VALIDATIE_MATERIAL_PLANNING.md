# VAL-004 — Live Validatie Material Planning (volledige keten t/m materiaal)

**Status:** validatiedocument / kwaliteitsrapport. Valideert de volledige productie-keten Ontwerpstrategie → Conceptvorming → Floor Design → **Material Planning** op ketenconsistentie, materiaaltechnische kwaliteit, productiegeschiktheid, ontwerpkwaliteit, reproduceerbaarheid, grensgevallen en contractstabiliteit. **Bevat één noodzakelijke correctie** (zie §Correctieronde): een token-limiet-fix op de Material-capability. Geen architectuur-, contract-, boundary- of workflowwijziging.

**Bindend / respecteert:** AB-006, AB-009, AB-012, BUILD-007, BUILD-023, IMP-014, BUILD-024, PLATFORM-001, PLATFORM-002, REASONING-001, SEC-001, IMP-015 t/m IMP-018.

---

## Methode

- **Uitvoering:** live, via de vier productie-reasoners *as built* (serversleutel via `_ai_sleutel()`, AB-012). Per case de volledige keten zonder handmatige tussenkomst: strategie → concept → floor design → (eerste floor design gekozen) → material planning.
- **Validatieset:** dezelfde dekking als VAL-003 — 34 hoofdcases (12 sectoren) + 2 tweelingen, 5 reproduceerbaarheidsherhalingen, 6 grensgevallen = **45 ketens**.
- **Omvang:** eerste run **180 live-aanroepen** (4 stappen × 45); na de correctie een gerichte **material-hermeting van 45 aanroepen** (uitsluitend de material-stap, met het reeds gevalideerde concept + gekozen floor design als invoer — "herhaal alleen de benodigde validaties"). Totaal ≈ **225 live-aanroepen**.

## Bevinding & correctieronde (kern van deze validatie)

**Bevinding (eerste run):** de Material-stap viel in **alle 45 ketens (100%)** terug op de deterministische placeholder, terwijl strategie/concept/floor normaal slaagden.

**Oorzaakanalyse:** een gerichte diagnostische call toonde een **afgekapt** modelantwoord (`JSONDecodeError: Unterminated string`). De materiaal-output (2–3 voorstellen met een afweging over gebruik, onderhoud, slijtvastheid, akoestiek, comfort, duurzaamheid en productie) is aanzienlijk rijker dan die van de andere capabilities en overschreed de **gedeelde default `max_tokens` (600)** → afgekapte JSON → parse-fout → terugval. De strategie-/concept-/floor-output bleef korter en onder de limiet.

**Laag-toewijzing:** **capability-/configuratielaag** — geen contract-, boundary-, orchestrator- of ontwerpfilosofie-defect. Het contract en de fallback werkten exact zoals ontworpen (bij een onbruikbaar antwoord een geldig placeholder-resultaat).

**Correctie (uitsluitend noodzakelijk):** de Material-capability construeert haar client nu met een ruimere token-limiet (`max_tokens=1500`); de **gedeelde default en de overige capabilities (IMP-015/016/017) blijven ongewijzigd**. Geen wijziging aan boundary, contract, normalisatie of orchestratie.

**Hermeting na correctie (45 material-calls):** **0 fallbacks**, **45/45 contract-geldig**, **3 voorstellen per case**, **0 lekken**.

## Kwantitatieve resultaten (na correctie)

| Meting | Resultaat |
|---|---|
| Ketens / totaal live-aanroepen | 45 / ≈225 |
| Contract-geldig — strategie / concept / floor / material | 45 / 45 / 45 / **45** |
| Terugval placeholder — strategie / floor / material | 0 / 2 / **0** |
| Terugval placeholder — concept | 1 (grensgeval X3) |
| Material-voorstellen per case | **3** in alle 45 ketens |
| Technische/AI-lekkage | **0** |

*(De concept-/floor-fallbacks betreffen uitsluitend grensgevallen met ontbrekende context — dezelfde graceful degradatie als in VAL-002/003; in productie door de gates geblokkeerd.)*

## Beoordeling per controlepunt

**Ketenconsistentie — sterk.** Elk Material Profile refereert expliciet aan het concept ("ondersteunt de organische warmte van het concept") en het gekozen Floor Design ("verstevigt de horizontale strokengrafiek"), zonder tegenstrijdigheden met strategie/concept/floor.

**Materiaaltechnische kwaliteit — sterk.** `materiaalsoort`, `structuur`, `pooltype`, `tactiliteit`, `uitstraling` en `motivering` zijn volledig en coherent; realistische tapijtwaarden (wol, wol-polyamide 80/20, PA6/PA6.6, gerecycled PA/rPA; getuft/geweven/velours/bouclé; poolhoogtes 2–12 mm).

**Productiegeschiktheid — sterk.** De voorstellen zijn technisch realiseerbaar en sluiten aan op DCOD-printtapijt: expliciete aandacht voor printbaarheid, kleurechtheid, reinigbaarheid en slijtvastheid ("realiseerbaar binnen standaard printtapijt-workflow", "kleurdiepte uitstekend op wolvezel"). Geen interne tegenstrijdigheden.

**Ontwerpkwaliteit — sterk.** De materiaalkeuze versterkt het ontwerp, ondersteunt de ontwerpfilosofie (dienende, technisch verantwoorde vloer) en is geloofwaardig én praktisch voor een interieurarchitect. Betekenisvolle differentiatie: doorgaans een warm/wol-, een robuust/PA- en een duurzaam/gerecycled-alternatief.

**Reproduceerbaarheid — voldoende/goed.** Herhaalde cases leveren consistente materiaalfamilies (wol-mix / PA / gerecycled PA) en identieke contractstructuren; variatie zit in de precieze samenstelling en poolhoogte — binnen "acceptabele variatie".

**Grensgevallen — sterk.** Bij ontbrekende/onbekende invoer degradeert de keten gecontroleerd (grensgeval-fallbacks op concept/floor) en hallucineert niet; de material-stap levert nog steeds technisch verdedigbare, neutrale voorstellen.

## Analyse

**Sterke punten:** ketenconsistente, productiegerichte materiaalredenering; realistische DCOD-materialen; betekenisvolle differentiatie; 45/45 contractstabiliteit na correctie; 0 lekken; robuuste grensgeval-degradatie.

**Verbeterpunten:** (a) *afgehandeld* — de token-limiet is gecorrigeerd; (b) *optioneel, laag* — dezelfde cosmetische taal-slips als in eerdere validaties (enkele anglicismen/typefouten), modelgedrag, geen contract-/inhoudsgevolg; (c) *optioneel* — run-variatie in concept-palet (zie VAL-003), onveranderd.

## Eindbeoordeling

**IMPLEMENTATIEGEREED.** Na de noodzakelijke token-limiet-correctie levert de Material Planning-capability in de volledige keten technisch verantwoorde, productiegeschikte en ketenconsistente materiaalvoorstellen: 45/45 contract-geldig, 3 gedifferentieerde voorstellen per case, 0 fallbacks, 0 lekken. De keten Ontwerpstrategie → Conceptvorming → Floor Design → Material Planning is inhoudelijk geschikt voor productie.
