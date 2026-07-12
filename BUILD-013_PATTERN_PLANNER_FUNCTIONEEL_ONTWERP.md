# BUILD-013 — Pattern Planner: functioneel ontwerp

**Status:** functioneel ontwerp, gereed voor architectuurreview (VR). Beschrijft uitsluitend **wat** de Pattern Planner functioneel doet, niet **hoe**. Geen nieuwe architectuurcomponent, geen nieuwe functionele verantwoordelijkheid buiten de bestaande architectuur. Verankerd in DESIGN_BRAIN, BUILD-007, AB-005, AB-009, AB-010, BUILD-011 en BUILD-012.

**Uitgangspunt:** de Pattern Planner is de volgende downstream-component ná de Material Planner. Hij **vormt uitsluitend patroonvoorstellen** op basis van de **bevestigde** upstream-objecten (Concept, Floor Design, Material Profile), motiveert elk voorstel, en **bevestigt nooit**.

---

## 1. Plaats in de architectuur

De Pattern Planner is één van de planners in de interne opbouw van de Design Brain (DESIGN_BRAIN: Reasoning Engine → Material Planner / Pattern Planner / SVG Planner). In de keten staat hij **ná de Material Planner**:
- **Reasoning Engine** — levert (Fase 1) het Concept en (Fase 2) de Floor Designs; de architect bevestigt er één.
- **Material Planner** — levert de Material Profiles; de architect bevestigt er één (AB-010).
- **Material Profile** — het bevestigde materiaalresultaat dat de Pattern Planner leest.
- **Downstream** — na bevestiging van een patroonvoorstel volgt de **SVG Planner** (rendering; AB-005/AR-004) en verderop de Floor Visualization Engine en de Design Transfer Package (BUILD-007).

## 2. Verantwoordelijkheid

De Pattern Planner **stelt patronen voor, bevestigt nooit**. Hij vormt **patroonvoorstellen** die passen bij het bevestigde ontwerp (Concept + Floor Design) en het bevestigde materiaal (Material Profile), **motiveert** elk voorstel, en produceert **uitsluitend voorstellen**. De architect bevestigt; de Pattern Planner niet.

## 3. Input

De Pattern Planner **leest** — uitsluitend **read-only** — de bevestigde upstream-objecten:
- het **bevestigde Concept** (laag 4, `status == "bevestigd"`);
- het **bevestigde Floor Design** (`status == "Bevestigd"`);
- het **bevestigde Material Profile** (`status == "Bevestigd"`, AB-010).

Startvoorwaarde: uitsluitend starten wanneer alle drie de upstream-objecten bevestigd zijn (consistent met het gate-patroon: elke stap start op bevestigde upstream-objecten). De Pattern Planner muteert geen van deze objecten.

## 4. Output

De Pattern Planner produceert één of meer **patroonvoorstellen** (het voorgestelde patroonresultaat):
- **Status:** "Voorgesteld" — nooit bevestigd door de Pattern Planner.
- **Motivatie:** elk patroonvoorstel draagt zijn **motivering in het object zelf**.
- **Traceerbaarheid:** elk patroonvoorstel draagt een **herkomst-referentie** naar het bevestigde Concept, het bevestigde Floor Design en het bevestigde Material Profile.
- **Relatie met downstream:** na bevestiging door de architect vormt het patroon de invoer voor de **SVG Planner** (rendering) en, via de gerenderde vloerafwerking, voor de Floor Visualization Engine.

## 5. Gebruikte gegevens

Uitsluitend lezend, voor zover relevant voor het patroon:
- **Concept:** stijlfamilie, complexiteit, motiefschaal, kleurpalet — het esthetische kader.
- **Floor Design:** de ontwerprichting — de bevestigde richting waarbinnen het patroon past.
- **Material Profile:** structuur, pooltype en uitstraling — de materiaal-eigenschappen die bepalen welk patroon technisch en visueel passend is.

## 6. Wel / niet verantwoordelijk

**Wel:**
- **patroonvoorstellen vormen** die passen bij Concept, Floor Design en Material Profile;
- **motiveren** — de onderbouwing in het patroonvoorstel;
- **signaleren** wanneer de bevestigde invoer onvoldoende is om een onderbouwd patroon te vormen (ontbrekende informatie wordt nooit zelf ingevuld).

**Niet:**
- het **Concept niet wijzigen**, het **Floor Design niet wijzigen**, het **Material Profile niet wijzigen**;
- **geen patroon bevestigen** (dat doet de architect);
- **geen SVG genereren** (SVG Planner);
- **niet visualiseren** (Floor Visualization Engine);
- **niet exporteren**.

## 7. Relatie met de overige architectuur

- **DesignContext:** read-only — de Pattern Planner leest het bevestigde Concept (laag 4) via de DesignContext en muteert haar niet.
- **Resultaat-objecten:** leest het bevestigde Floor Design en het bevestigde Material Profile (beide buiten de DesignContext); de patroonvoorstellen zijn eveneens resultaat-objecten buiten de DesignContext.
- **Architect:** bevestigt één patroonvoorstel (Voorgesteld → Bevestigd); de Pattern Planner leest die status alleen.
- **SVG Planner:** downstream — rendert (ná bevestiging) het patroon naar een SVG; de SVG Planner is uitsluitend uitvoerend (AB-005/AR-004). De Pattern Planner beslist het patroon, de SVG Planner voert de weergave uit.
- **Overige downstream:** de Floor Visualization Engine en de Design Transfer Package werken met het (gerenderde) patroon conform de bestaande architectuur (BUILD-007).

## 8. Grenzen

- De Pattern Planner werkt **uitsluitend met bevestigde upstream-objecten** (Concept, Floor Design, Material Profile).
- Hij produceert **uitsluitend voorgestelde patroonresultaten** (status "Voorgesteld"); hij bevestigt nooit.
- Hij **wijzigt geen bestaande objecten** (read-only op alle invoer).
- Hij **introduceert geen nieuwe architectuur** — Pattern Planner bestaat al als begrip (DESIGN_BRAIN).

## 9. Architectuurbasis (identiteit Pattern Profile besloten via AB-011)

De identiteit en het eigenaarschap van het patroonresultaat zijn formeel vastgesteld in **AB-011**. Conform dat besluit geldt: het patroonresultaat is het **Pattern Profile**, een zelfstandig resultaat-object **buiten de DesignContext** (geen DesignContext-laag, geen relatie met laag 5 Materialisatie); een patroonvoorstel is een Pattern Profile met status "Voorgesteld"; de Pattern Planner produceert uitsluitend voorgestelde Pattern Profiles en bevestigt nooit; uitsluitend de architect bevestigt (status "Bevestigd"). Dit functioneel ontwerp is daarmee volledig gedekt door het vastgestelde architectuurbesluit.

---

**Reviewgereed:** dit document legt uitsluitend de verantwoordelijkheid, plaats, in-/output, gebruikte gegevens, beslissingen en grenzen van de Pattern Planner vast; de architectuurbasis (identiteit Pattern Profile) is vastgesteld in AB-011 (zie §9). Na een positieve VR kan het als basis dienen voor het technisch ontwerp.
