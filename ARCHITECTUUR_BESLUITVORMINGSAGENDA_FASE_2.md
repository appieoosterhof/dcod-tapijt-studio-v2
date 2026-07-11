# Architectuur Besluitvormingsagenda — Fase 2

**Status:** besluitvormingsagenda, ter beoordeling. Dit document neemt zelf geen architectuurbesluiten, introduceert geen nieuwe architectuurbegrippen, en wijzigt geen bestaande documenten. Uitsluitend gebaseerd op AR-001, AR-002, AB-001, AB-002, `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, `SPEC-000_PROJECT_CHARTER.md`, `OPEN_ARCHITECTUURVRAGEN.md` en BUILD-001 t/m BUILD-007.

**Doel:** een compleet overzicht van alle resterende architectuurkeuzes die expliciete besluitvorming door de architect vereisen, vóórdat de ontwikkeling van het platform wordt voortgezet.

---

## 1. Inventarisatie van alle nog open architectuurkeuzes

**Groep A — Terminologie en naamgeving (laag risico, geen inhoudelijke afhankelijkheden)**
- T1. Canonieke naamswijzigingen: Projectcontext → Project-/Ruimtecontext, Ontwerpintentie → Ontwerpvisie
- T2. Mock-up laten vervallen ten gunste van Scene / Floor Visualization Engine / Visualisatie
- T3. SVG Planner formeel erkennen als de bestaande SVG-generatiepipeline
- T4. Naamscollisie Reasoning Engine ↔ Design Reasoning oplossen

**Groep B — Fundamentele identiteitsvragen**
- T5. Eigenaarschap, statusmechanisme en relatie tot Ontwerpstudie van Floor Design (vervolg op AB-002)
- T6. Eigenaarschap, statusmechanisme en identiteit van Material Profile (analoog onderzoek, nog niet gestart)
- T7. Positie van Ontwerpstrategie-stap en Reasoning Engine als producenten van DesignContext-lagen 3/4 (AB-001, Deel A)
- T8. Positionering van Ontwerpsignatuur binnen de BUILD-007-keten

**Groep C — Relatieonderzoek (afhankelijk van Groep B)**
- T9. Relatie tussen Reasoning Engine/Pattern Planner en Floor Design
- T10. Relatie tussen Material Planner en Material Profile
- T11. Asymmetrische toegang tot DesignContext (Floor Visualization Engine versus Design Transfer Package)

**Groep D — Consolidatie en governance**
- T12. BUILD-007-keten als gezaghebbend ontwerpketen-diagram erkennen; positie van `DESIGN_BRAIN_ARCHITECTUURVISIE.md`
- T13. Positionering van de Conversation Planner: Project Brain of Design Brain (AV-001, bestaand, ongewijzigd open)
- T14. Opname van het AI-interpretatieprincipe in SPEC-000 v1.1 (AV-002, bestaand, ongewijzigd open)
- T15. SPEC-000 Documenthiërarchie en §9 (adviesdocument-regel) bijwerken; AV-001 Impact-veld actualiseren

## 2. Uitwerking per keuze

### T1 — Canonieke naamswijzigingen (Projectcontext/Ontwerpintentie)

- **Aanleiding:** Regel 1 van `DESIGN_BRAIN_ARCHITECTUURVISIE.md` schreef deze koppeling zelf voor, maar heeft dit nooit als afgerond artefact opgeleverd.
- **Betrokken documenten:** `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, `DESIGN_CONTEXT_MODEL.md`, BUILD-004.
- **Wat vaststaat:** BUILD-004 gebruikt al consequent Project-/Ruimtecontext en Ontwerpvisie; er is geen enkele plek meer waar Projectcontext/Ontwerpintentie als operationele term wordt gebruikt.
- **Wat onbekend is:** niets inhoudelijks — dit is een formalisering van bestaande praktijk.
- **Historisch bewijs nog mogelijk?** Ja — de koppeling is al bewezen: Regel 1 van de Architectuurvisie schreef de hernoeming voor en BUILD-004 past Project-/Ruimtecontext en Ontwerpvisie consequent toe.
- **Expliciet Architectuurbesluit nodig?** Ja — een formele bekrachtiging dat de hernoeming definitief is (§5: Architectuurbesluit + visiewijziging), ook al is de inhoudelijke consequentie nihil.
- **Te maken keuze:** bevestigen dat deze twee hernoemingen definitief zijn.
- **Mogelijke consequenties:** geen — betreft uitsluitend documentatie, geen enkele code of BUILD wijzigt.

### T2 — Mock-up vervalt

- **Aanleiding:** AR-002, inventarisatie.
- **Betrokken documenten:** `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, BUILD-006, VISION-001, BUILD-007.
- **Wat vaststaat:** Scene (BUILD-006), Floor Visualization Engine en Visualisatie (BUILD-007) dekken samen, met eigen, elk afzonderlijk vastgelegde verantwoordelijkheid, wat Mock-up ooit als één begrip was.
- **Wat onbekend is:** niets inhoudelijks.
- **Historisch bewijs nog mogelijk?** Ja — Scene (BUILD-006), Floor Visualization Engine en Visualisatie (BUILD-007) zijn elk al afzonderlijk vastgelegd en dekken samen wat Mock-up ooit als één begrip was.
- **Expliciet Architectuurbesluit nodig?** Ja — bevestigen dat Mock-up als zelfstandig begrip vervalt (§5: Architectuurbesluit + visiewijziging).
- **Te maken keuze:** bevestigen dat Mock-up als zelfstandig begrip vervalt.
- **Mogelijke consequenties:** geen.

### T3 — SVG Planner erkennen

- **Aanleiding:** AR-002, inventarisatie.
- **Betrokken documenten:** `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, SPEC-000 §6, `app.py`/`modules_extra.py` (bestaande, ongewijzigde code).
- **Wat vaststaat:** de bestaande SVG-generatiepipeline (`build_tile_svg()`, `build_repeat_svg()`, 28 generator-functies) vervult deze rol al, van vóór de DesignContext-architectuur.
- **Wat onbekend is:** niets — dit is een naamserkenning, geen codewijziging.
- **Historisch bewijs nog mogelijk?** Ja — de bestaande code (`build_tile_svg()`, `build_repeat_svg()`, 28 generator-functies) bewijst dat deze pipeline de rol al vervult, van vóór de DesignContext-architectuur.
- **Expliciet Architectuurbesluit nodig?** Ja — een naamserkenning vastleggen (§5: Architectuurbesluit + visiewijziging); geen codewijziging.
- **Te maken keuze:** bevestigen dat SVG Planner = de bestaande SVG-generatiepipeline.
- **Mogelijke consequenties:** geen wijziging aan code; uitsluitend documentatie.

### T4 — Naamscollisie Reasoning Engine ↔ Design Reasoning

- **Aanleiding:** AR-002, hoofdstuk 5 (bijvangst) — twee verschillende begrippen delen het woord "Reasoning" binnen hetzelfde brondocument.
- **Betrokken documenten:** `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, `DESIGN_CONTEXT_MODEL.md` (Ontwerpredenering).
- **Wat vaststaat:** Design Reasoning is al gekoppeld aan Ontwerpredenering (Regel 1); Reasoning Engine is een afzonderlijk, nog te bouwen verwerkend component.
- **Wat onbekend is:** hoe de dubbelzinnigheid wordt weggenomen — bijvoorbeeld door "Design Reasoning" als term te laten vervallen ten gunste van uitsluitend "Ontwerpredenering."
- **Historisch bewijs nog mogelijk?** Gedeeltelijk — de koppeling Design Reasoning ↔ Ontwerpredenering is bewezen (Regel 1), maar hóe de dubbelzinnigheid wordt opgelost is een keuze, niet iets wat uit bewijs volgt.
- **Expliciet Architectuurbesluit nodig?** Ja — bevestigen dat "Design Reasoning" als term vervalt (§5: Architectuurbesluit + visiewijziging), vóór Reasoning Engine verder als term wordt gebruikt.
- **Te maken keuze:** bevestigen dat "Design Reasoning" vervalt als term (Ontwerpredenering blijft de enige canonieke naam), Reasoning Engine blijft ongemoeid.
- **Mogelijke consequenties:** geen inhoudelijke wijziging, uitsluitend eenduidigere naamgeving vóórdat Reasoning Engine (T7/T9) als component wordt vastgesteld.

### T5 — Eigenaarschap, statusmechanisme en relatie tot Ontwerpstudie van Floor Design

**Status: afgerond** (AB-006): K-A/K-B vastgesteld; K-C gedelegeerd naar T9, K-D naar T13, K-E optioneel.

- **Aanleiding:** AB-002, Deel B (nog niet te onderbouwen bevonden).
- **Betrokken documenten:** AB-002, BUILD-007 (functioneel + technisch), SPEC-000 §7 (Governance), SPEC-000 §14 (Ontwerpstudie).
- **Wat vaststaat:** Floor Design is een resultaat-object, ontstaat op het moment dat de Conversation Planner een andere uitkomst dan "vraag" kiest, en heeft drie benoemde downstream-consumenten (Material Profile, Floor Visualization Engine, Design Transfer Package).
- **Wat onbekend is:** wie eigenaar is, of er een voorgesteld/bevestigd-statusmechanisme is, en of Floor Design hetzelfde begrip is als, een specialisatie is van, of onafhankelijk is van "Ontwerpstudie" (SPEC-000 §14).
- **Historisch bewijs nog mogelijk?** Nee — AB-002 (Deel B) heeft juist vastgesteld dat eigenaarschap en statusmechanisme niet uit historisch bewijs te onderbouwen zijn; dit vergt een constitutief (nieuw) besluit, geen afleiding.
- **Expliciet Architectuurbesluit nodig?** Ja — het meest fundamentele, blokkerende besluit van deze agenda (§5: Architectuurbesluit, mogelijk SPEC-000 §7-achtig).
- **Te maken keuze:** de architect stelt eigenaarschap en statusmechanisme vast, en beslist over de relatie met Ontwerpstudie.
- **Mogelijke consequenties:** bepaalt rechtstreeks of, en hoe, T9 (relatie Reasoning Engine/Pattern Planner ↔ Floor Design) en T11 (DesignContext-toegang) later kunnen worden besloten — dit is het meest fundamentele, blokkerende punt in de hele agenda.

### T6 — Eigenaarschap, statusmechanisme en identiteit van Material Profile

- **Aanleiding:** AR-001, bevinding 2.3 — dezelfde open vraag als bij Floor Design bestaat structureel ook voor Material Profile, maar is nooit apart onderzocht.
- **Betrokken documenten:** BUILD-007 (functioneel + technisch), DesignContext Model laag 5 (Materialisatie).
- **Wat vaststaat:** Material Profile is expliciet geen synoniem voor Materialisatie (DesignContext laag 5); het wordt "bepaald in samenhang met het al vastgestelde Floor Design."
- **Wat onbekend is:** exact dezelfde categorieën als bij T5 (eigenaarschap, statusmechanisme, precieze afleiding, creërend component) — hier nog niet eens in kaart gebracht met een AB-002-achtig onderzoek.
- **Historisch bewijs nog mogelijk?** Gedeeltelijk (nog te bepalen) — er is nog geen AB-002-achtig onderzoek uitgevoerd; naar analogie met T5 is de kern (eigenaarschap) waarschijnlijk niet af te leiden, maar dat moet het onderzoek zelf uitwijzen.
- **Expliciet Architectuurbesluit nodig?** Ja — zowel over het al dan niet uitvoeren van het onderzoek als over de uitkomst (§5: Architectuurbesluit, mogelijk SPEC-000 §7-achtig).
- **Te maken keuze:** of dit onderzoek op dezelfde manier wordt uitgevoerd als bij Floor Design (AB-002), en met welke uitkomst.
- **Mogelijke consequenties:** bepaalt T10 (relatie Material Planner ↔ Material Profile).

### T7 — Ontwerpstrategie-stap en Reasoning Engine als producenten van DesignContext-lagen 3/4

**Status: afgerond** (AB-008): AB-001 Deel A bekrachtigd.

- **Aanleiding:** AB-001, Deel A — het enige gedeelte van AB-001 dat al concreet ter goedkeuring is voorgesteld.
- **Betrokken documenten:** AB-001, `DESIGN_BRAIN_ARCHITECTUURVISIE.md` Regel 2, DesignContext Model lagen 3 en 4.
- **Wat vaststaat:** dit voorstel is volledig consistent met alle negen in AB-001 vastgestelde feiten en wijzigt niets aan BUILD-007.
- **Wat onbekend is:** niets voor dit specifieke deelbesluit — het staat klaar voor bevestiging of afwijzing.
- **Historisch bewijs nog mogelijk?** Ja — AB-001 heeft negen feiten uit bewijs vastgesteld; Deel A is daarmee volledig consistent en wijzigt niets aan BUILD-007.
- **Expliciet Architectuurbesluit nodig?** Ja — AB-001 Deel A bekrachtigen of afwijzen (§5: Architectuurbesluit); ligt al klaar ter goedkeuring.
- **Te maken keuze:** AB-001 Deel A bekrachtigen (of afwijzen).
- **Mogelijke consequenties:** bij bevestiging ontstaan twee kandidaat-BUILD's (Ontwerpstrategie-stap, Reasoning Engine) volgens het bestaande BUILD-patroon; is een randvoorwaarde voor T9.

### T8 — Positionering van Ontwerpsignatuur

- **Aanleiding:** AR-002, inventarisatie — begrip en definitie bestaan nog (SPEC-000 §17), maar ontbreken in de BUILD-007-keten.
- **Betrokken documenten:** `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, SPEC-000 §17, BUILD-007.
- **Wat vaststaat:** de v1-scope was al vastgesteld als sessiegebonden.
- **Wat onbekend is:** of, en zo ja waar, Ontwerpsignatuur een plek krijgt in de huidige keten (bijvoorbeeld als onderdeel van fase 2, Ontwerpvraag), of dat het bewust buiten scope blijft tot een latere fase.
- **Historisch bewijs nog mogelijk?** Gedeeltelijk — de definitie (SPEC-000 §17) en de sessiegebonden v1-scope bestaan als bewijs, maar de positie in de BUILD-007-keten is een nieuwe keuze, geen afleiding.
- **Expliciet Architectuurbesluit nodig?** Ja — positioneren of expliciet uitstellen (§5: Architectuurbesluit; mogelijk BUILD-007-wijziging, mogelijk geen actie).
- **Te maken keuze:** positioneren, of expliciet uitstellen.
- **Mogelijke consequenties:** raakt mogelijk BUILD-007 Functioneel Ontwerp, fase 2 — geen andere afhankelijkheden.

### T9 — Relatie Reasoning Engine/Pattern Planner ↔ Floor Design

**Status: afgerond** (AB-009): C1 vastgesteld (lezing a); C2/C3 volgen; C4 opgelost door AB-005 + AB-009; resterend een technisch interfacecontract (BUILD).

- **Aanleiding:** AB-001, Deel B — expliciet niet besloten, wacht op T5 (Floor Design-identiteit) en T7 (Reasoning Engine bevestigd als component).
- **Betrokken documenten:** AB-001, AB-002, `DESIGN_BRAIN_ARCHITECTUURVISIE.md`.
- **Wat vaststaat:** de oorspronkelijke AR-002-hypothese (Reasoning Engine/Pattern Planner produceren Floor Design rechtstreeks) staat op gespannen voet met Floor Design's vastgestelde omschrijving ("andere fase, andere reikwijdte").
- **Wat onbekend is:** het volledige afleidingsmechanisme.
- **Historisch bewijs nog mogelijk?** Nee — AB-001 (Deel B) heeft dit expliciet niet besloten; het afleidingsmechanisme is niet uit bewijs af te leiden en hangt af van de uitkomst van T5 en T7.
- **Expliciet Architectuurbesluit nodig?** Ja — maar pas zinvol ná T5 en T7 (§5: Architectuurbesluit; later mogelijk een nieuw BUILD).
- **Te maken keuze:** kan pas zinvol worden gemaakt ná T5 en T7.
- **Mogelijke consequenties:** bepaalt of er een nieuw BUILD-document komt voor de daadwerkelijke Floor Design-generatie.

### T10 — Relatie Material Planner ↔ Material Profile

- **Aanleiding:** AR-002, hoofdstuk 4 — hypothese (component/resultaat-relatie, analoog aan T9), nooit bevestigd.
- **Betrokken documenten:** AR-002, `DESIGN_BRAIN_ARCHITECTUURVISIE.md`.
- **Wat vaststaat:** Material Planner en Material Profile zijn begrippen van een verschillende aard (component versus resultaat), geen synoniemen.
- **Wat onbekend is:** het volledige afleidingsmechanisme.
- **Historisch bewijs nog mogelijk?** Nee — de component/resultaat-relatie is nooit bevestigd; het afleidingsmechanisme volgt niet uit bewijs en hangt af van de uitkomst van T6.
- **Expliciet Architectuurbesluit nodig?** Ja — maar pas zinvol ná T6 (§5: Architectuurbesluit; later mogelijk een nieuw BUILD).
- **Te maken keuze:** kan pas zinvol worden gemaakt ná T6 (en, voor de component-naam, T7-achtig, al is Material Planner in AB-001 niet behandeld).
- **Mogelijke consequenties:** bepaalt of er een nieuw BUILD-document komt voor de daadwerkelijke Material Profile-generatie.

### T11 — Asymmetrische toegang tot DesignContext

- **Aanleiding:** AR-001, bevinding 2.2.
- **Betrokken documenten:** BUILD-007 Technisch Ontwerp, hoofdstuk 2 en 3.
- **Wat vaststaat:** Floor Visualization Engine mag DesignContext expliciet niet rechtstreeks lezen; Design Transfer Package leest wel rechtstreeks "DesignContext (visie)."
- **Wat onbekend is:** of dit een bewuste, onderbouwde uitzondering is, of een inconsistentie die hersteld moet worden.
- **Historisch bewijs nog mogelijk?** Gedeeltelijk — BUILD-007 Technisch Ontwerp bewijst dát de asymmetrie bestaat, maar niet óf die bewust en onderbouwd is; die motivering ontbreekt in het bewijs.
- **Expliciet Architectuurbesluit nodig?** Ja — de regel expliciet motiveren of gelijktrekken (§5: Architectuurbesluit; raakt BUILD-007 Technisch Ontwerp hfst. 3).
- **Te maken keuze:** de regel expliciet motiveren, óf gelijktrekken zodat beide componenten dezelfde beperking krijgen.
- **Mogelijke consequenties:** raakt BUILD-007 Technisch Ontwerp, hoofdstuk 3; hangt inhoudelijk samen met T5 (zodra Floor Design's eigen status/eigenaarschap vaststaat, is preciezer te bepalen wat "rechtstreeks bij DesignContext" behoort te betekenen).

### T12 — BUILD-007-keten als gezaghebbend diagram; positie van DESIGN_BRAIN_ARCHITECTUURVISIE.md

- **Aanleiding:** AR-002, besluitpunt 9.
- **Betrokken documenten:** `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, BUILD-007.
- **Wat vaststaat:** er bestaan op dit moment twee, nooit verzoende ontwerpketen-diagrammen.
- **Wat onbekend is:** of `DESIGN_BRAIN_ARCHITECTUURVISIE.md` wordt herschreven, vervangen, of gearchiveerd zodra T1 t/m T10 zijn besloten.
- **Historisch bewijs nog mogelijk?** Ja — beide, nooit verzoende ontwerpketen-diagrammen bestaan als bewijs; dit is een consolidatiekeuze, geen ontbrekend feit.
- **Expliciet Architectuurbesluit nodig?** Nee — dit is een wijziging van de Architectuurvisie (§5: geen zelfstandig Architectuurbesluit), zinvol pas nadat T1 t/m T10 zijn besloten.
- **Te maken keuze:** vorm van de uiteindelijke, geharmoniseerde Architectuurvisie.
- **Mogelijke consequenties:** dit is de samenvattende, laatste stap — pas zinvol te maken nadat T1 t/m T10 zijn besloten, anders wordt het document mogelijk twee keer herschreven.

### T13 — AV-001: Conversation Planner, Project Brain of Design Brain?

- **Aanleiding:** bestaand, `OPEN_ARCHITECTUURVRAGEN.md`, ontstaan in BUILD-005 Technisch Ontwerp. Door dit traject niet gewijzigd, maar wel relevanter geworden: T5 (Floor Design-eigenaarschap) roept een vergelijkbare Project Brain/Design Brain-vraag op.
- **Betrokken documenten:** `OPEN_ARCHITECTUURVRAGEN.md`, BUILD-005 (drie documenten), `DESIGN_BRAIN_ARCHITECTUURVISIE.md`.
- **Wat vaststaat:** de canonieke definities van Project Brain en Design Brain (BUILD-005 Technisch Ontwerp, hoofdstuk 5).
- **Wat onbekend is:** exact zoals in het register vastgelegd — onveranderd.
- **Historisch bewijs nog mogelijk?** Gedeeltelijk — de canonieke Project Brain/Design Brain-definities (BUILD-005 Technisch Ontwerp, hfst. 5) bestaan als bewijs, maar de positionering van de Conversation Planner volgt daar niet dwingend uit; daarom staat de vraag in het register.
- **Expliciet Architectuurbesluit nodig?** Ja — ongewijzigd t.o.v. het register (§5: Architectuurbesluit, mogelijk visiewijziging); aan te bevelen gelijktijdig met T5 te behandelen.
- **Te maken keuze:** ongewijzigd ten opzichte van het register; wel aan te bevelen dit gelijktijdig met T5 te bespreken, gezien de inhoudelijke overlap.
- **Mogelijke consequenties:** raakt BUILD-005 Technisch Ontwerp en mogelijk de eigenaarschapskeuze bij T5.

### T14 — AV-002: opname AI-interpretatieprincipe in SPEC-000 v1.1

- **Aanleiding:** bestaand, `OPEN_ARCHITECTUURVRAGEN.md`, ontstaan in BUILD-004 Technisch Ontwerp.
- **Betrokken documenten:** `OPEN_ARCHITECTUURVRAGEN.md`, SPEC-000 §6/§7.
- **Wat vaststaat:** het principe wordt al toegepast (BUILD-004, BUILD-005, BUILD-007); alleen de formele opname in SPEC-000 staat nog open.
- **Wat onbekend is:** ongewijzigd ten opzichte van het register.
- **Historisch bewijs nog mogelijk?** Ja — het principe wordt al toegepast in BUILD-004, BUILD-005 en BUILD-007; die praktijk is het bewijs. Alleen de formele opname in SPEC-000 staat nog open.
- **Expliciet Architectuurbesluit nodig?** Nee — dit is een SPEC-000-revisie (§5: wijziging SPEC-000 §6/§7), geen zelfstandig Architectuurbesluit; te bundelen met T15.
- **Te maken keuze:** ongewijzigd; kandidaat voor dezelfde SPEC-000-revisieronde als T15.
- **Mogelijke consequenties:** wijziging SPEC-000 §6/§7.

### T15 — SPEC-000 Documenthiërarchie, §9 en AV-001 Impact-veld

- **Aanleiding:** AR-001, bevindingen 2.4, 2.5, 2.6.
- **Betrokken documenten:** SPEC-000 §8, §9; `OPEN_ARCHITECTUURVRAGEN.md`.
- **Wat vaststaat:** de Documenthiërarchie (§8) eindigt bij BUILD-003 en mist VISION-001/BUILD-004 t/m 007/`OPEN_ARCHITECTUURVRAGEN.md`; §9's adviesdocument-regel dekt de sinds BUILD-004 gegroeide praktijk (migratie versus nieuwe capaciteit) niet meer letterlijk; AV-001's Impact-veld noemt BUILD-007 niet.
- **Wat onbekend is:** niets inhoudelijks — dit is bijwerken van bestaande, achterhaald geraakte documentatie.
- **Historisch bewijs nog mogelijk?** Ja — de bestaande documenten (SPEC-000 §8/§9, AV-001 Impact-veld) zijn zelf het bewijs van de achterstand die moet worden bijgewerkt.
- **Expliciet Architectuurbesluit nodig?** Nee — dit is bijwerken van achterhaalde documentatie in één SPEC-000-revisieronde (§5: wijziging SPEC-000), geen zelfstandig Architectuurbesluit.
- **Te maken keuze:** bevestigen dat dit in één, gecontroleerde SPEC-000-revisieronde wordt meegenomen, samen met T14.
- **Mogelijke consequenties:** wijziging SPEC-000 (§8, §9) en `OPEN_ARCHITECTUURVRAGEN.md` (AV-001 Impact-veld) — bij voorkeur pas ná T1 t/m T12, zodat de hiërarchie in één keer volledig wordt bijgewerkt in plaats van herhaaldelijk.

## 3. Afhankelijkheden tussen keuzes

```
T4 ──▶ T7 ──▶ T9 ──▶ T12
              │       ▲
T5 ───────────┴───────┤
  │                   │
  ├──▶ T11 ───────────┤
  │                   │
  └──▶ T13 (parallel, inhoudelijke overlap, geen harde afhankelijkheid)

T6 ──▶ T10 ──▶ T12

T1, T2, T3, T8  (geen afhankelijkheden, kunnen op elk moment)

T14, T15  (na T1 t/m T12, één gecombineerde SPEC-000-revisieronde)
```

- **T5 is het meest fundamentele, blokkerende punt**: T9 en T11 kunnen zonder T5 niet zinvol worden besloten.
- **T6 volgt hetzelfde patroon als T5**, maar dan voor Material Profile — logisch pas te starten nadat de aanpak bij T5 is doorlopen, zodat dezelfde onderzoeksmethode kan worden hergebruikt.
- **T7 is onafhankelijk uitvoerbaar**, maar T4 (naamscollisie) lost men bij voorkeur eerst op, om te voorkomen dat "Reasoning Engine" tweemaal een naamswijziging doormaakt.
- **T12 is een consoliderende stap** en kan pas na T1, T2, T3, T7, T8, T9, T10 zinvol worden gemaakt.
- **T14 en T15 raken alleen SPEC-000** en worden bij voorkeur gebundeld tot één revisieronde, ná de inhoudelijke besluiten (T1–T12), zodat SPEC-000 niet meerdere keren hoeft te worden herzien.
- **T13 heeft geen harde afhankelijkheid**, maar inhoudelijke overlap met T5 (eigenaarschap/Brain-positionering) maakt gelijktijdige behandeling efficiënter.

## 4. Geadviseerde volgorde van besluitvorming

1. **T1, T2, T3** — snelle, risicoloze formaliseringen (kunnen desgewenst in één keer worden afgehandeld).
2. **T4** — naamscollisie oplossen, vóór Reasoning Engine als term verder wordt gebruikt.
3. **T7** — Ontwerpstrategie-stap/Reasoning Engine als DesignContext-laag 3/4-producenten (AB-001 Deel A ligt al klaar).
4. **T5, samen met T13** — Floor Design-identiteit en de gerelateerde Project Brain/Design Brain-vraag; het meest fundamentele besluit van deze agenda.
5. **T6** — Material Profile-identiteit, met dezelfde aanpak als T5.
6. **T8** — Ontwerpsignatuur-positionering (kan ook eerder, geen afhankelijkheden; hier geplaatst omdat het geen prioriteit heeft).
7. **T9, T10, T11** — relatieonderzoek, nu voor het eerst zinvol mogelijk.
8. **T12** — BUILD-007-keten als gezaghebbend diagram; `DESIGN_BRAIN_ARCHITECTUURVISIE.md` herschrijven of vervangen.
9. **T14, T15** — gecombineerde SPEC-000-revisieronde, als afsluiting.

## 5. Resultaattype per keuze

| Keuze | Architectuurbesluit | Wijziging Architectuurvisie | Wijziging SPEC-000 | Nieuw BUILD-document | Geen actie |
|---|---|---|---|---|---|
| T1 | ✓ | ✓ | | | |
| T2 | ✓ | ✓ | | | |
| T3 | ✓ | ✓ | | | |
| T4 | ✓ | ✓ | | | |
| T5 | ✓ | | mogelijk (§7-achtig) | | |
| T6 | ✓ | | mogelijk (§7-achtig) | | |
| T7 | ✓ | | | later, bij bouw | |
| T8 | ✓ | | | mogelijk (BUILD-007-wijziging) | mogelijk |
| T9 | ✓ | | | later, bij bouw | |
| T10 | ✓ | | | later, bij bouw | |
| T11 | ✓ | | | mogelijk (BUILD-007-wijziging) | |
| T12 | | ✓ | | | |
| T13 | ✓ | mogelijk | | | mogelijk |
| T14 | | | ✓ | | |
| T15 | | | ✓ | | |

## 6. Voorgestelde roadmap Architectuurfase 2

- **Sprint 1 — Opruiming:** T1, T2, T3, T4. Laag risico, geen onderlinge afhankelijkheden, verkleint de agenda snel.
- **Sprint 2 — Fundament:** T7, gevolgd door T5 en T13 gezamenlijk. Dit is het zwaartepunt van Architectuurfase 2 — zonder deze besluiten blijft het grootste deel van de resterende agenda geblokkeerd.
- **Sprint 3 — Analoog onderzoek:** T6, T8.
- **Sprint 4 — Relaties:** T9, T10, T11 — nu voor het eerst met voldoende fundament om te besluiten.
- **Sprint 5 — Consolidatie:** T12 (Architectuurvisie herschrijven/vervangen), afgesloten met T14/T15 (één SPEC-000-revisieronde).

Deze roadmap is een volgorde-advies, geen tijdsplanning — de architect bepaalt het tempo. Elke sprint levert uitsluitend Architectuurbesluiten en/of documentwijzigingen op; geen enkele sprint in deze roadmap bevat BUILD-implementatie. Nieuwe BUILD-documenten (voor Ontwerpstrategie-stap, Reasoning Engine, Material Planner, Pattern Planner, of de daadwerkelijke Floor Design/Material Profile-generatie) volgen pas ná Architectuurfase 2, als eigen, aparte stap.
