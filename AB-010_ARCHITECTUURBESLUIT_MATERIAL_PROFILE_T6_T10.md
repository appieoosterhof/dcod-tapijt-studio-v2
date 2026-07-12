# AB-010 — Concept-Architectuurbesluit: Material Profile (T6) en Material Planner ↔ Material Profile (T10)

**Status:** VASTGESTELD — architectuurbesluit; **geamendeerd via AB-010A** (K10-A invoer-preconditie: "beschikbare Floor Designs" → "het bevestigde Floor Design", na TR-003). De agendapunten **T6** (identiteit Material Profile) en **T10** (relatie Material Planner ↔ Material Profile) zijn hiermee formeel afgesloten. Geen technische implementatie. Verankerd in BUILD-007, AB-002, AB-006, AB-009, DESIGN_CONTEXT_MODEL, DESIGN_BRAIN en BUILD-012.

**Kern:** Material Profile wordt vastgesteld naar hetzelfde, reeds bekrachtigde model als Floor Design (AB-006/AB-009). Er wordt **geen nieuwe component** geïntroduceerd — Material Planner en Material Profile bestaan al als begrip.

---

## 1. Vaststaande feiten

- **F1.** Material Profile = de visuele en materiële eigenschappen (uitstraling, structuur, pooltype) van de gekozen vloerafwerking. Bron: BUILD-007 Functioneel r. 16; Technisch r. 45.
- **F2.** Material Profile is een **resultaat-object** ("materiaaleigenschappen"), status "Nieuw, nog niet technisch uitgewerkt". Bron: BUILD-007 Technisch, statustabel r. 28.
- **F3.** Material Profile is **geen synoniem** voor Materialisatie (DesignContext-laag 5); laag 5 blijft een eigenschap ván een ontwerp binnen de ontwerpfase. Bron: BUILD-007 Functioneel r. 16; Technisch r. 45.
- **F4.** Material Profile wordt bepaald **in samenhang met het al vastgestelde Floor Design — nooit andersom**. Bron: BUILD-007 Technisch r. 62.
- **F5.** Downstream-consumenten: Floor Visualization Engine (Floor Design + Material Profile + Scene) en Design Transfer Package. Bron: BUILD-007 Technisch r. 64, 66.
- **F6.** Een statusmechanisme voorgesteld/bevestigd is voor Material Profile verondersteld. Bron: BUILD-007 Technisch r. 144.
- **F7.** Precedent Floor Design: eigenaar van de bevestiging = de architect, status Voorgesteld → Bevestigd, de Design Brain heeft uitsluitend een producerende rol (AB-006); Floor Design is een resultaat-object **buiten** de DesignContext (AB-009).
- **F8.** De Material Planner bestaat als begrip (DESIGN_BRAIN: één van de planners ná de Reasoning Engine) en is in BUILD-012 beschreven als producent van materiaalvoorstellen.
- **Grondslag:** zoals AB-002 voor Floor Design vaststelde, zijn eigenaarschap, producent en statusmechanisme *constitutief* (te kiezen, niet uit bewijs af te leiden). De onderstaande keuzes worden voorgesteld op basis van F1–F8 en het bekrachtigde Floor Design-precedent, ter vaststelling.

## 2. T6 — Identiteit van het Material Profile

- **K6-A — Wat het is.** Het Material Profile is het resultaat-object dat de visuele en materiële eigenschappen (uitstraling, structuur, pooltype) van de gekozen vloerafwerking vastlegt (F1).
- **K6-B — Zelfstandig resultaat-object.** Het is een **zelfstandig resultaat-object**, geen onderdeel van een andere component en geen DesignContext-laag; het is nadrukkelijk geen synoniem voor Materialisatie (laag 5) (F2/F3).
- **K6-C — Buiten de DesignContext.** Het Material Profile bestaat **buiten** de DesignContext — analoog aan Floor Design (AB-009). De DesignContext wordt gelezen, niet gemuteerd.
- **K6-D — Producent.** De **Material Planner** produceert het Material Profile (F8), naar hetzelfde patroon als de Reasoning Engine (Fase 2) het Floor Design produceert.
- **K6-E — Eigenaar van de bevestiging.** De **architect** bevestigt het Material Profile (F7; het bevroren principe "de architect blijft eigenaar van alle bevestigingen"; laag 5 is gedeeld: DCOD brengt materiaalkennis in, de architect stuurt en bevestigt).
- **K6-F — Statusovergangen.** **Voorgesteld → Bevestigd** (F6). De Material Planner schrijft uitsluitend "Voorgesteld"; uitsluitend de architect kent "Bevestigd" toe.

## 3. T10 — Relatie Material Planner ↔ Material Profile

- **K10-A — Verantwoordelijkheid Material Planner.** De Material Planner vormt materiaalvoorstellen op basis van **het bevestigde Floor Design** en het bevestigde Concept, motiveert elk voorstel, en bevestigt nooit (BUILD-012). *(Amendement AB-010A, na TR-003:)* de Material Planner start **uitsluitend nadat één Floor Design door de architect is bevestigd**, en werkt **uitsluitend met dát bevestigde Floor Design**; hierdoor blijft de sequentiële architectuur volledig consistent met het gate-patroon (elke stap start op een bevestigd upstream-object; BUILD-007).
- **K10-B — Voorstel = voorgesteld Material Profile.** Een **materiaalvoorstel is een Material Profile met status "Voorgesteld".** Hiermee zijn de twee begrippen verzoend: "materiaalvoorstel" (BUILD-012) en "Material Profile" (BUILD-007) beschrijven hetzelfde resultaat-object in respectievelijk de status Voorgesteld en (na bevestiging) Bevestigd.
- **K10-C — Verhouding component ↔ resultaat.** De **Material Planner is de component** (producent); het **Material Profile is het resultaat-object**. Dit is dezelfde component-↔-resultaat-verhouding als Reasoning Engine ↔ Floor Design (AB-009).
- **K10-D — Einde van de verantwoordelijkheid.** De verantwoordelijkheid van de Material Planner eindigt bij het opleveren van één of meer voorgestelde Material Profiles (buiten de DesignContext, met motivering). Hij bevestigt niet en voert geen downstream-verwerking uit.
- **K10-E — Bevestiging door de architect.** De architect kiest en bevestigt één voorgesteld Material Profile; daarmee gaat de status naar "Bevestigd" (K6-E/K6-F).
- **K10-F — Downstream.** Het bevestigde Material Profile wordt geconsumeerd door de **Floor Visualization Engine** (samen met Floor Design en Scene) en de **Design Transfer Package** (F5).

## 4. Overwogen alternatieven

- **Alternatief 1 — Material Profile gelijkstellen aan Materialisatie (laag 5).** *Afgewezen*: BUILD-007 (F3) stelt expliciet dat het geen synoniem is; laag 5 blijft ontwerpfase-eigenschap.
- **Alternatief 2 — Material Profile binnen de DesignContext plaatsen.** *Afgewezen*: strijdig met F3 en met het Floor Design-precedent (resultaat-object ná de ontwerpfase, buiten de DesignContext).
- **Alternatief 3 — De Material Planner laten bevestigen.** *Afgewezen*: strijdig met "de architect blijft eigenaar van alle bevestigingen" en met "voorstellen, nooit bevestigen".
- **Alternatief 4 (voorgesteld) — Material Profile als zelfstandig resultaat-object buiten de DesignContext, geproduceerd door de Material Planner (status Voorgesteld), bevestigd door de architect.** Zie hoofdstuk 2 en 3 — de enige lezing die consistent is met F1–F8 en het bekrachtigde Floor Design-precedent.

## 5. Consequenties

- **BUILD-012 wordt reviewbaar.** De open punten in BUILD-012 §10 (T6/T10) zijn hiermee besloten: de "materiaalvoorstellen" van de Material Planner zijn voorgestelde Material Profiles; de begrippen zijn verzoend.
- **Consistentie:** volledig in lijn met AB-006/AB-009 (Floor Design-precedent), BUILD-007 en het milestone-principe (architect eigenaar van bevestigingen). Geen nieuwe component.
- **Downstream vastgelegd:** het bevestigde Material Profile voedt de Floor Visualization Engine en de Design Transfer Package (F5).
- **Laag 5 Materialisatie blijft ongewijzigd** en losstaand van het Material Profile.
- De precieze objectvorm en het technische statusmechanisme blijven voor het technisch ontwerp (hier niet uitgewerkt).

## 6. Scope-afbakening (wat dit besluit niet doet)

- Geen technische implementatie of objectdefinitie op veldniveau.
- Geen uitspraak over de interne werking van de Floor Visualization Engine, de Design Transfer Package of de Pattern/SVG Planner.
- Geen wijziging aan het bevroren DesignContext Model of aan laag 5 (Materialisatie).

---

De architect heeft K6-A t/m K6-F en K10-A t/m K10-F vastgesteld; T6 en T10 zijn hiermee formeel besloten en de onafhankelijke review van BUILD-012 kan worden uitgevoerd.
