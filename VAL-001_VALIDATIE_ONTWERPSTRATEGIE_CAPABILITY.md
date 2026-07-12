# VAL-001 — Validatie Productie Reasoning Capability: Ontwerpstrategie

**Status:** validatiedocument / kwaliteitsrapport. Valideert de **inhoudelijke kwaliteit** van de productie-Ontwerpstrategie-capability (IMP-015) tegen de ontwerpfilosofie (REASONING-001) — niet de techniek en niet de werking van de AI-provider. **Geen architectuur-, contract-, boundary- of orchestratiewijziging.** Naar aanleiding van deze validatie zijn **geen** code-/capabilitycorrecties doorgevoerd (zie §Correctieronde).

**Bindend / respecteert:** AB-006, AB-009, AB-012, BUILD-007, BUILD-023, IMP-014, BUILD-024, PLATFORM-001, REASONING-001, IMP-015.

---

## Methode

- **Uitvoering:** live, via de productie-reasoner *as built* (`ProductieStrategieReasoner` + `AnthropicModelClient`, serversleutel via `_ai_sleutel()`, AB-012). Géén boundary-, contract- of promptwijziging tijdens de meting.
- **Validatieset:** **34 hoofdcases** verdeeld over de twaalf gevraagde sectoren — Hospitality, Hotel, Restaurant, Kantoor, Onderwijs, Bibliotheek, Zorg, Retail, Museum, Gemeente/Overheid, Leisure, Wonen — inclusief twee **consistentie-tweelingen** (H02b ≈ H02, K01b ≈ K01) met bewust bijna-identieke invoer.
- **Reproduceerbaarheid:** 5 cases (H02, K01, Z01, M01, G01) een tweede ronde gedraaid.
- **Grensgevallen:** 6 (X1 minimaal, X2 conflicterende wensen, X3 onvolledige context, X4 uitzonderlijk projecttype [uitvaart], X5 onbekende/tegenstrijdige stijl, X6 vrijwel leeg).
- **Totaal:** **45 live-aanroepen.** Per case volledig vastgelegd: invoer (8 boundary-velden), gegenereerde `aanpak` + `onderbouwing`, en automatische controles op (a) terugval op de placeholder, (b) contractvorm, (c) technische/AI-lekkage.

## Kwantitatieve resultaten

| Meting | Resultaat |
|---|---|
| Live-aanroepen | 45 |
| Terugval op placeholder (provider-/sleutelfout) | **0** |
| Contractafwijkingen (`{aanpak, onderbouwing}`, niet-leeg) | **0** |
| Technische/AI-lekkage (model, provider, "AI", "prompt", "token", "API", …) | **0** |

Elke case leverde een echte, volledige, contractconforme reasoning zonder enige technische verwijzing.

## Beoordeling per criterium

**1. Ontwerpkwaliteit — sterk.** De strategieën zijn logisch, professioneel, bruikbaar en geloofwaardig. Zij vertrekken consequent vanuit functie en randvoorwaarden vóór esthetiek (bv. H02 "luxe door soberheid en craft, onopvallende duurzaamheid onder 24/7-doorloop"; H03 spa "anti-slip, waterbestendig, thermisch aangenaam" eerst).

**2. Consistentie — sterk.** Bijna-identieke invoer geeft sterk convergerende strategie (H02≈H02b: "stille welstand / ondergeschikt aan de architectuur, luxe zonder opvallendheid"; K01≈K01b: "discreet-neutrale, duurzame basis die concentratie en corporate identiteit draagt"). Afwijkende context geeft gemotiveerde verschillen (H02 vs Z02: representatieve stille luxe vs dementie-veilige oriëntatie met valpreventie). Geen willekeurige variatie.

**3. Onderbouwing — sterk.** Onderbouwingen zijn inhoudelijk juist, controleerbaar en herleidbaar naar de context; geen technische of AI-uitleg; geen hallucinerende claims. Elke keuze wordt teruggekoppeld naar functie, doelgroep en randvoorwaarden.

**4. Ontwerpfilosofie & factoren — sterk.** Expliciete, terugkerende aansluiting op identiteit, functionaliteit, sfeer, routing, materiaal, onderhoud, akoestiek, duurzaamheid en productie; de driehoek *architectuur–functie–vloer* en de "dienende, dragende vloer" komen consequent terug (o.a. B01 akoestiek/leesrust, Z03 looptraining/rolstoel, L02 zweet/hygiëne, D03 zeer hoge omloop/karren).

**5. Reproduceerbaarheid — voldoende/goed.** Herhaalde cases behouden dezelfde kernredenering en identieke contractstructuur, met acceptabele bewoordingsvariatie (Z01 en M01 vrijwel identiek van strekking; H02/K01/G01 consistent van kern). De variatie is die van formulering, niet van richting.

**6. Grensgevallen — sterk.** X2 (conflict) lost de spanning "knus vs klinisch" beargumenteerd op; X4 (uitvaart) redeneert waardig en passend. X1/X3/X5/X6 (minimaal/onvolledig/onbekend/leeg) **weigeren te gissen** en vragen om de essentiële context — exact conform REASONING-001 §6 (geen willekeur, stelt voor, geen hallucinatie). In de productieflow worden zulke onvolledige invoeren bovendien al door de **gate** (`OntwerpStrategieStap._valideer`) geblokkeerd vóór de boundary; de nette weigering is dus aanvullende robuustheid.

## Analyse

**Sterke punten:** consequente functie-vóór-esthetiek-redenering; correcte, expliciete weging van harde randvoorwaarden; geloofwaardige, sectorspecifieke onderbouwing; volledige afwezigheid van technische/AI-lekkage; robuuste, eerlijke omgang met ontbrekende/tegenstrijdige input; 100% contractnaleving en 0% ongewenste terugval.

**Terugkerende zwakke punten:** uitsluitend cosmetische **modeltaal-slips** — incidentele anglicismen ("neutral", "subtle", "teachers") en spelfouten ("kleurpallet", "versterkken", "stillte"). Laagfrequent en zonder gevolg voor de ontwerpinhoud of het contract.

**Patronen:** de capability neigt (terecht) naar ingetogen, dienende vloeren; bij schaarse input schakelt zij naar "eerst context ophalen" in plaats van te fantaseren.

**Onderscheid naar type:**
- **Promptverbetering (optioneel, laag):** een instructie toevoegen die strikt correct Nederlands afdwingt en anglicismen vermijdt, zou de cosmetische slips wegnemen.
- **Capabilityverbetering:** geen nodig — boundary, contract, fallback en isolatie functioneren zoals ontworpen.
- **Ontwerpfilosofie:** geen tekort geconstateerd; REASONING-001 wordt inhoudelijk gevolgd.
- **Modelgedrag:** de spelling-/taalslips zijn modeleigen; de terugval-/contractgaranties van de capability vangen alle overige modelrisico's al af.

## Correctieronde

De enige geconstateerde afwijkingen zijn cosmetische modeltaal-slips; deze vormen **geen afwijking van de ontwerpfilosofie** en geen contract-/capabilitydefect. Conform de VAL-001-regel ("codewijzigingen uitsluitend indien zij direct voortkomen uit geconstateerde kwaliteitsafwijkingen") is **geen** code-/prompt-/capabilitywijziging doorgevoerd. De anglicismen/spelling zijn vastgelegd als **optionele, laag-prioritaire promptverbetering** voor een toekomstige iteratie, buiten de scope van deze validatie.

## Eindbeoordeling

**IMPLEMENTATIEGEREED.** De eerste productie-Reasoning Capability (Ontwerpstrategie) voldoet inhoudelijk aan de ontwerpfilosofie van DCOD (REASONING-001): onderbouwd, consistent, reproduceerbaar, filosofie-getrouw en robuust bij grensgevallen, met volledige contractnaleving en zonder enige technische of AI-lekkage.
