# BUILD-020 — Amendement op TD-008: laag 2 + Ontwerpstrategie-stap vóór het Concept

**Status:** architectuur-/ontwerpamendement, ter review (TR). **Geen implementatie.** Lost de tijdens CR-009 (IMP-010) gevonden ontwerp-gap op: de HTTP-keten *Conversation Planner → Reasoning Engine* is vanuit een leeg gesprek niet uitvoerbaar. Wijkt nergens van de bestaande architectuur af; introduceert geen component en verplaatst geen componentgrens.

**Normatief/gelezen:** BUILD-004, BUILD-007, BUILD-008, BUILD-009, BUILD-017, BUILD-019, TD-007, TD-008, en de code (`reasoning_engine.py`, `conversation_planner.py`, `context_interpreter.py`, `ontwerpstrategie_stap.py`, `design_context.py`, `design_brain_api.py`).

---

## 1. De gap (feitelijk)

`ReasoningEngine.vorm_concept()` (Fase 1) heeft als preconditie (geverifieerd, `reasoning_engine.py:231–242`): **bevestigde OntwerpVisie (laag 1)** + **Project-/Ruimtecontext (laag 2)** + **Ontwerpstrategie (laag 3, `aanpak`)**. TD-008 orkestreert echter uitsluitend laag 1 (via de Conversation Planner, die per BUILD-017/TD-007 bewust alléén laag 1 projecteert) en noemt de Ontwerpstrategie-stap (BUILD-009) niet. Gevolg: `vorm_concept` signaleert *"Project-/Ruimtecontext onvoldoende vastgelegd"* + *"Ontwerpstrategie ontbreekt"* (CR-009, T6).

## 2. Beslechting van de acht punten

### 1. Hoe ontstaat laag 2?
De **Context Interpreter (BUILD-004)** produceert bij het interpreteren van de vrije tekst **zowel** laag-1- als laag-2-interpretaties in **één** `interpreteer_context`-aanroep (`context_interpreter.py`: `_VELDEN_PROJECTCONTEXT` → `laag="projectcontext"`). De laag-2-waarden worden geprojecteerd met de **bestaande** functie `pas_interpretaties_toe(dc, <laag-2-subset>)` — exact het mechanisme dat de live app al gebruikt. Dit is een **verbatim projectie**, geen (nieuwe) interpretatie.

### 2. Wanneer wordt BUILD-009 (Ontwerpstrategie) uitgevoerd?
**Ná** het bevestigen van de visie en met een gevulde laag 2 — precies de preconditie van `OntwerpStrategieStap.stel_voor()` (bevestigde visie + laag 2). De stap produceert laag 3 (`aanpak`, status "in ontwikkeling"); een **gezamenlijke vaststelling** (architect + DCOD, laag 3 is GEZAMENLIJK — BUILD-008) zet de status op "vastgesteld". Daarná is `vorm_concept` uitvoerbaar. Dit herstelt exact de BUILD-007-volgorde *Context Interpreter → Ontwerpstrategie (eigen stap) → Reasoning Engine*.

### 3. Welke component is verantwoordelijk?
- **Laag 2:** de **Context Interpreter (BUILD-004)** — interpreteert én projecteert (via `pas_interpretaties_toe`).
- **Laag 3:** de **Ontwerpstrategie-stap (BUILD-009)** — reeds bestaand, met eigen reasoning-boundary.
- De **integratielaag** (BUILD-019/TD-008) doet uitsluitend de **orkestratie** (aanroepen in de juiste volgorde) — geen eigen ontwerplogica.

### 4. Hoe past dit binnen BUILD-007?
Naadloos: BUILD-007 schrijft de keten *Context Interpreter → Ontwerpstrategie → Reasoning Engine* al voor. TD-008 had die twee tussenstappen weggelaten; dit amendement **voegt geen nieuwe stap toe aan de architectuur**, maar orkestreert de reeds vastgestelde BUILD-007-stappen die TD-008 miste.

### 5. Zonder nieuwe component
Alle drie de betrokken elementen bestaan al: `interpreteer_context` + `pas_interpretaties_toe` (BUILD-004) en `OntwerpStrategieStap` (BUILD-009). De integratielaag krijgt uitsluitend extra **orkestratie** (endpoints), geen nieuwe component of verantwoordelijkheid.

### 6. Zonder dubbele interpretatie
Per dialoogbeurt wordt **één** `interpreteer_context`-aanroep gedaan; het resultaat (beide lagen) voedt zowel de laag-1-projectie (Conversation Planner) als de laag-2-projectie (`pas_interpretaties_toe`). Dat wordt bereikt door de reeds geïnterpreteerde lijst te **delen**: de integratie injecteert die lijst in de injecteerbare interpretatie-boundary van de Conversation Planner (die daardoor niet opnieuw interpreteert) en projecteert de laag-2-subset apart. De Ontwerpstrategie-stap interpreteert géén vrije tekst (zij redeneert over de reeds gevulde laag 1/2 via haar eigen boundary) — dus ook daar geen tweede interpretatie.

### 7. Zonder ontwerpautoriteit toe te voegen
De laag-2-projectie is een verbatim waarde-kopie (geen betekenisafleiding). De Ontwerpstrategie-stap **stelt voor** (status "in ontwikkeling") en bevestigt nooit; de vaststelling ("vastgesteld") is een **expliciete gezamenlijke actie** (architect + DCOD), door de integratie toegepast namens die actie — nooit door een component zelf. Consistent met AB-008/AR-007.

### 8. Zonder bestaande componentgrenzen te wijzigen
- De **Conversation Planner** blijft **uitsluitend laag 1** schrijven (BUILD-017/TD-007 ongewijzigd) — de laag-2-projectie loopt bewust **buiten** de CP.
- De **Context Interpreter** blijft de enige interpreter (BUILD-004 ongewijzigd).
- De **Ontwerpstrategie-stap** blijft laag 3 (BUILD-009 ongewijzigd); zij muteert nooit laag 1/2.
- De **Reasoning Engine** blijft laag 4 (ongewijzigd).
Geen enkele grens verschuift; er komt uitsluitend orkestratie bij.

## 3. Geamendeerde orkestratie-keten (vervangt de betreffende TD-008-passage)

1. **Dialoog-beurt:** één interpretatie → laag 1 (Conversation Planner) **én** laag 2 (`pas_interpretaties_toe`, laag-2-subset), gedeeld uit dezelfde interpretatie.
2. **Visie bevestigen** (architect).
3. **Ontwerpstrategie-stap** (BUILD-009) → laag 3 ("in ontwikkeling").
4. **Strategie vaststellen** (gezamenlijk) → laag 3 "vastgesteld".
5. **Concept** (Reasoning Engine Fase 1) — nu uitvoerbaar.
6. **Floor Designs → Material Profile → Pattern Profile → SVGResultaat → Visualisatie → Design Transfer Package** — ongewijzigd t.o.v. TD-008.

## 4. Documentimpact (welke documenten aangepast moeten worden)

| Document | Aanpassing nodig? | Toelichting |
|---|---|---|
| **TD-008** | **Ja** | Orkestratie-keten (§2) en importlijst (Besluit B) missen de laag-2-projectie en de Ontwerpstrategie-stap. Wordt geamendeerd door dit BUILD-020 (pointer toegevoegd). |
| **BUILD-019** | **Ja (klein)** | Functionele workflow/§gebruikte gegevens moet laag-2-projectie + Ontwerpstrategie-stap noemen. Pointer toegevoegd. |
| **BUILD-004** | Nee | Context Interpreter interpreteert beide lagen en projecteert al; ongewijzigd hergebruikt. |
| **BUILD-007** | Nee | Dit amendement **herstelt** de reeds vastgelegde BUILD-007-volgorde. |
| **BUILD-008** | Nee | Eigenaarschap (laag 2 = architect-feiten/DCOD structureert; laag 3 = gezamenlijk) blijft gerespecteerd. |
| **BUILD-009** | Nee | Ontwerpstrategie-stap ongewijzigd hergebruikt. |
| **BUILD-017 / TD-007** | Nee | De Conversation Planner blijft uitsluitend laag 1 schrijven; de laag-2-projectie loopt buiten de CP. |

## 5. Vereiste vervolgimplementatie (IMP, niet in dit amendement)

`design_brain_api.py` wordt in een latere IMP additief uitgebreid met: (a) de laag-2-projectie in de dialoog-endpoint (één gedeelde interpretatie), (b) een `ontwerpstrategie`-endpoint (BUILD-009) en (c) een `bevestig-strategie`-endpoint (vaststelling), ingevoegd vóór het `concept`-endpoint. Geen wijziging aan de componenten, de pipeline of de bestaande routes.

Twee punten voor die IMP (uit TR-012):
- **Timing laag 2:** de laag-2-projectie hoort bij de **dialoog-/pré-strategiefase** (consistent met laag 1). Laag 2 kent geen bevestigingsvlag; de IMP legt vast dat laag 2 na de strategie-/Concept-fase niet ongemerkt wordt herschreven (bijv. door de projectie alleen in de dialoog-endpoint te doen).
- **Vaststelling-gate:** `vorm_concept` toetst uitsluitend `aanpak`, niet status "vastgesteld". De IMP beslist of het `concept`-endpoint aanvullend op laag-3-status "vastgesteld" gate't (workflow-correctheid, consistent met de gelaagde bevestiging) — zonder een componentgrens te wijzigen.

---

**Reviewgereed:** dit amendement beslecht de acht gevraagde punten op ontwerpniveau, wijst uitsluitend TD-008 (en klein BUILD-019) als aan te passen aan, herstelt de BUILD-007-volgorde, en doet dit zonder nieuwe component, zonder dubbele interpretatie, zonder ontwerpautoriteit en zonder verschuiving van componentgrenzen.
