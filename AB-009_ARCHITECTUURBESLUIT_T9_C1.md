# AB-009 — Architectuurbesluit T9 (C1): oorsprong van Floor Design

**Status:** T9 afgerond. C1 vastgesteld (lezing a); C2/C3 volgen uit C1; C4 opgelost door AB-005 + AB-009. Resterend: uitsluitend een technisch interfacecontract (BUILD). Geen nieuw onderzoek, geen nieuwe architectuur.

**Volledige bewijsbasis:** zie **AB-001 Deel B** (de drie lezingen en hun niet-onderscheidbaarheid worden daar vastgesteld; hier niet integraal herhaald).

**Randvoorwaarde:** T7 is bekrachtigd (AB-008) — Reasoning Engine als producent van laag 4 (Concept).

---

## 1. Vaststaande feiten

- **F1.** Floor Design is een resultaat-object ná de ontwerpfase: "een andere fase, een andere reikwijdte". Bron: BUILD-007 Func. r. 15.
- **F2.** Floor Design kent twee statussen (Voorgesteld/Bevestigd); de architect is eigenaar en bevestigt, de Design Brain heeft uitsluitend een producerende rol en is nooit eigenaar. Bron: AB-006 §5.
- **F3.** De Reasoning Engine produceert voorgestelde inhoud voor laag 4 (Concept), de Ontwerpstrategie-stap voor laag 3; beide "voorstellen, nooit bevestigen". Bron: AB-008.
- **F4.** Floor Design wordt afgeleid uit "op dat moment vastgelegde inhoud van DesignContext"; de precieze afleiding is een open punt. Bron: BUILD-007 h. 3/h. 8.
- **F5.** C1 is constitutief: de drie lezingen zijn met de bestaande documenten niet van elkaar te onderscheiden. Bron: AB-001 Deel B; AB-007 §3/§4 (C1).

## 2. De drie bestaande lezingen

- **(a)** Floor Design ontstaat uit de bevestigde ontwerpcontext (Concept).
- **(b)** Floor Design ontstaat uit de Ontwerpstudie.
- **(c)** Floor Design ontstaat autonoom.

## 3. Gevolgen per lezing voor de architectuur

- **(a) Uit bevestigd Concept:**
  - Producent = de Concept-producent, i.e. de Reasoning Engine (AB-008).
  - De planners (Diagram A) staan vóór Floor Design; de twee diagrammen verbinden via Concept → Floor Design.
  - Een bevestigd Concept is voorwaarde vóórdat Floor Design ontstaat.
- **(b) Uit Ontwerpstudie:**
  - De oorsprong ligt bij het Ontwerpstudie-begrip; dit koppelt C1 aan K-D (relatie tot Ontwerpstudie), reeds gedelegeerd naar T13 (AB-006).
  - De afleiding valt buiten de in BUILD-007 beschreven Concept-keten en vereist een eigen koppeling die daar nog niet is uitgewerkt.
- **(c) Autonoom:**
  - Floor Design ontstaat zonder afleiding uit Concept; de in AB-008 bekrachtigde rol (Reasoning Engine → Concept) staat dan los van Floor Design.
  - De planners (Diagram A) staan niet vóór Floor Design; Floor Design krijgt een eigen, nog te bepalen ontstaan.

*In alle drie de lezingen blijven de statussen (Voorgesteld/Bevestigd) en het eigenaarschap (architect) uit AB-006 ongewijzigd; de Design Brain behoudt uitsluitend een producerende rol.*

## 4. Vast te stellen door de architect

> **Gekozen lezing (a / b / c):** **(a)**
>
> Floor Design ontstaat uit de bevestigde ontwerpcontext, zoals vastgelegd in het bevestigde Concept. De Design Brain werkt deze ontwerpcontext creatief uit tot één of meer voorgestelde Floor Designs. De architect beoordeelt, wijzigt en bevestigt het gekozen Floor Design.

**Administratieve status (T9 afgerond):**
- **C1 — vastgesteld:** lezing (a).
- **C2 (producent) en C3 (diagramverhouding) volgen uit C1** (AB-007 §4; AB-008).
- **C4 (uitvoeringsgrens) opgelost** door AB-005 (SVG Planner uitsluitend uitvoerend) + AB-009 (Floor Design zelfstandig ontwerpobject); resterend uitsluitend een technisch interfacecontract (BUILD).
