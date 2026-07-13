# VAL-002 — Live Validatie Productie Reasoning Keten: Ontwerpstrategie → Conceptvorming

**Status:** validatiedocument / kwaliteitsrapport. Valideert de eerste volledige **productie-reasoningketen** (Ontwerpstrategie → Conceptvorming) op inhoudelijke kwaliteit, onderlinge consistentie, reproduceerbaarheid, ontwerpfilosofie en contractstabiliteit — niet de AI-provider. **Geen architectuur-, boundary- of contractwijziging.** Naar aanleiding van deze validatie zijn **geen** code-/capabilitycorrecties doorgevoerd (zie §Correctieronde).

**Bindend / respecteert:** AB-006, AB-009, AB-012, BUILD-007, BUILD-023, IMP-014, BUILD-024, PLATFORM-001, REASONING-001, IMP-015, VAL-001, IMP-016.

---

## Methode

- **Uitvoering:** live, via de productie-reasoners *as built* (`ProductieStrategieReasoner` en `ProductieConceptReasoner` op de `AnthropicModelClient`, serversleutel via `_ai_sleutel()`, AB-012). Per case werd de **keten** zonder handmatige tussenkomst gedraaid: (1) Ontwerpstrategie → (2) Conceptvorming, waarbij `aanpak`/`onderbouwing` uit stap 1 als kader in stap 2 werden gevoerd. Géén boundary-, contract- of promptwijziging tijdens de meting.
- **Validatieset:** dezelfde dekking als VAL-001 — **34 hoofdcases** over de twaalf sectoren (Hospitality, Hotel, Restaurant, Kantoor, Onderwijs, Bibliotheek, Zorg, Retail, Museum, Gemeente/Overheid, Leisure, Wonen), inclusief twee consistentie-tweelingen (H02b≈H02, K01b≈K01), **5 reproduceerbaarheidsherhalingen** (H02, K01, Z01, M01, G01) en **6 grensgevallen** (minimaal, conflict, onvolledig, uitzonderlijk [uitvaart], onbekende stijl, leeg).
- **Omvang:** **45 ketens = 90 live-aanroepen** (2 per keten). Per keten volledig vastgelegd: invoer, strategie (`aanpak`/`onderbouwing`), concept (`stijlfamilie`/`kleurpalet`/`complexiteit`/`motiefschaal`/`motivering`), en automatische controles op terugval (per stap), contractvorm (per stap), downstream-veilige conceptvocabulaire en technische/AI-lekkage.

## Kwantitatieve resultaten

| Meting | Resultaat |
|---|---|
| Ketens / live-aanroepen | 45 / **90** |
| Terugval op placeholder — Ontwerpstrategie | **0** |
| Terugval op placeholder — Conceptvorming | **0** |
| Contractafwijkingen — strategie (`{aanpak, onderbouwing}`) | **0** |
| Contractafwijkingen — concept (4 verplichte velden) | **0** |
| Concept buiten downstream-veilige vocab (complexiteit/motiefschaal) | **0** |
| Technische/AI-lekkage | **0** |

## Beoordeling per criterium

**1. Strategie → Concept (ketencoherentie) — sterk.** Elk concept verwijst expliciet naar en bouwt voort op de strategie ("ondersteunt de strategie…", "voldoet aan alle strategiebouwstenen", "volgt de strategie exact"), zonder tegenstrijdigheden met `aanpak`, `onderbouwing` of de ontwerpvisie. Voorbeeld H02: strategie "subtiele materiaaldifferentiatie, stille gids, zones zonder afleidend patroon" → concept "verfijnd minimaal, monochromatisch, zone-oriëntatie zonder patroongedrama".

**2. Stijlconsistentie mét differentiatie — sterk.** `stijlfamilie`, `kleurpalet`, `complexiteit` en `motiefschaal` ondersteunen consequent de gekozen strategie. De ingetogen sectoren clusteren terecht op warm-neutrale, low-complexe paletten, maar de keten **differentieert betekenisvol** waar de context daarom vraagt: Retail-flagship (D01) donker `#2a2a2a` met goud `#d4af37` (medium), Science center (M03) licht met blauw `#0066cc` rastergrid (medium), sportvloer (L02) met teal richtingslijnen, basisschool (O01) terracotta zones. De output is dus niet uniform.

**3. Ontwerpfilosofie — sterk.** Beide capabilities blijven binnen REASONING-001: de vloer als dragend/dienend element, functie- en randvoorwaarde-gedreven, onderbouwd en uitlegbaar, voorstellend (nooit beslissend). Geen van beide verlaat de filosofie.

**4. Reproduceerbaarheid — voldoende/goed.** Herhaalde ketens behouden dezelfde kernstrategie én kernconcept en identieke contractstructuren; de variatie beperkt zich tot formulering en incidenteel de grove `motiefschaal`-as (H02: klein↔groot) — binnen de toegestane "acceptabele variatie". Z01/M01/K01/G01 zijn zeer stabiel.

**5. Grensgevallen — sterk.** Bij minimale/onvolledige/onbekende/lege invoer weigert de **volledige keten** professioneel te gissen: de strategie vraagt om context en het concept propageert die weigering eerlijk (stijlfamilie "niet bepaalbaar zonder kerngegevens" / "niet determineerbaar" / "Contextloos", met een motivering die om de kerngegevens vraagt). De keten fabriceert nooit een schijnontwerp. In de productieflow worden zulke invoeren bovendien al door de **gate** (bevestigde visie + context + vastgestelde strategie) geblokkeerd vóór de boundaries; de nette weigering is aanvullende, out-of-gate robuustheid.

## Analyse (met correcte laag-toewijzing)

**Sterke punten:** volledige ketencoherentie; betekenisvolle contextafhankelijke differentiatie; 100% contract- en vocab-stabiliteit; 0% ongewenste terugval; 0 technische/AI-lekkage; eerlijke, niet-hallucinerende omgang met ontbrekende/tegenstrijdige input door de hele keten.

**Enige terugkerende zwakte:** cosmetische **modeltaal-slips** — incidentele anglicismen en een enkel niet-Nederlands woord ("ablenkende", "desenvolgend", "orient", "resistent"). Laagfrequent, zonder gevolg voor ontwerpinhoud of contract.

**Laag-toewijzing (expliciet, om verkeerde attributie te voorkomen):**
- **Ontwerpfilosofie:** geen tekort — REASONING-001 wordt door beide stappen gevolgd.
- **Capability:** geen tekort — boundary-isolatie, fallback, normalisatie en contract functioneren zoals ontworpen; de keten (aanpak/onderbouwing → concept) verloopt correct.
- **Prompt (optioneel, laag):** de taal-slips zijn met een strikt-Nederlands-instructie te verminderen — een optionele, latere promptverbetering (geldt voor beide capabilities).
- **Modelgedrag:** de taal-slips zijn modeleigen; de terugval-/normalisatie-/contractgaranties vangen alle overige modelrisico's al af.
- **Contract:** stabiel — 90/90 aanroepen contractconform; de out-of-gate weigering (concept met refusal-tekst in `stijlfamilie`) is technisch contract-geldig en in productie onbereikbaar (gate), dus geen defect.
- **Architectuur:** ongewijzigd en consistent; geen bevinding.

## Correctieronde

De enige geconstateerde afwijkingen zijn cosmetische modeltaal-slips (laag: prompt/modelgedrag), reeds in VAL-001 vastgelegd als optionele latere promptverbetering. Zij vormen **geen** afwijking van de ontwerpfilosofie, de keten, het contract of de architectuur. Conform de VAL-002-regel ("uitsluitend noodzakelijke correcties") is **geen** code-/prompt-/capabilitywijziging doorgevoerd.

## Eindbeoordeling

**IMPLEMENTATIEGEREED.** Ontwerpstrategie en Conceptvorming vormen aantoonbaar één consistente Design Brain: het concept bouwt logisch en zonder tegenstrijdigheid voort op de strategie, de stijlkeuzes ondersteunen de strategie en differentiëren betekenisvol per context, beide capabilities blijven binnen REASONING-001, de keten is reproduceerbaar met acceptabele variatie en contractstabiel, en blijft ook bij grensgevallen professioneel — zonder enige technische of AI-lekkage.
