# BUILD-012 — Material Planner: functioneel ontwerp

**Status:** functioneel ontwerp, gereed voor architectuurreview (VR). Beschrijft uitsluitend **wat** de Material Planner functioneel doet, niet **hoe**. Geen nieuwe architectuurcomponent, geen nieuwe functionele verantwoordelijkheid buiten de bestaande architectuur. Verankerd in DESIGN_BRAIN, DESIGN_CONTEXT_MODEL (laag 5, Materialisatie), BUILD-007, AB-006 en AB-009.

**Uitgangspunt:** de Material Planner is de eerste downstream-component ná de volledig geïmplementeerde Reasoning Engine. Hij **vormt uitsluitend materiaalvoorstellen** op basis van beschikbare Floor Designs, **bevestigt nooit**, wijzigt Concept noch Floor Designs, en motiveert elk voorstel.

---

## 1. Plaats binnen de architectuur

De Material Planner is één van de planners die in de interne opbouw van de Design Brain ná de Reasoning Engine staan (DESIGN_BRAIN: Reasoning Engine → Material Planner / Pattern Planner / SVG Planner). Hij is **downstream** van de Reasoning Engine en werkt met de door Fase 2 geproduceerde Floor Designs (BUILD-007: "Floor Design → Material Profile: bepaald in samenhang met het al vastgestelde Floor Design — nooit andersom").

## 2. Functionele verantwoordelijkheid

De Material Planner **stelt materiaal voor, bevestigt nooit**. Hij vormt materiaalvoorstellen — de visuele en materiële eigenschappen van de vloerafwerking (uitstraling, structuur, pooltype; DESIGN_CONTEXT_MODEL laag 5, Materialisatie; BUILD-007) — in samenhang met een beschikbaar Floor Design en het bevestigde Concept, en **motiveert** elk voorstel. Passend bij het gedeelde eigenaarschap van laag 5 (DCOD brengt materiaalkennis in, de architect stuurt op tactiliteit en uitstraling).

## 3. Input

- **Startvoorwaarde:** uitsluitend starten **nadat er Floor Designs beschikbaar zijn** (uit de Reasoning Engine, Fase 2).
- De **beschikbare Floor Designs** (read-only).
- Het **bevestigde Concept** (laag 4) en de onderliggende visie/context als onderbouwing (read-only).

## 4. Output

**Eén of meer materiaalvoorstellen**, elk met de status **"Voorgesteld"** en elk **voorzien van een motivering**. De Material Planner produceert uitsluitend materiaalvoorstellen — geen andere artefacten. De architect (of de gezamenlijke dialoog) bevestigt; de Material Planner niet.

## 5. Gebruikte gegevens uit het bevestigde Concept

Uitsluitend lezend, voor zover relevant voor de materiaalkeuze: **stijlfamilie**, **kleurpalet**, **complexiteit** en **motiefschaal** (laag 4). Deze geven het esthetische kader waarbinnen het materiaal past; de Material Planner wijzigt ze nooit.

## 6. Gebruikte gegevens uit de Floor Designs

Uitsluitend lezend: de **ontwerprichting** van elk Floor Design en de **herkomst-referentie** naar het bevestigde Concept. Het materiaalvoorstel wordt in samenhang met de gekozen ontwerprichting gevormd; de Floor Designs zelf worden nooit gewijzigd.

## 7. Welke beslissingen wel en niet

**Wel:** materiaalvoorstellen vormen (materiaalsoort, structuur, pooltype, tactiliteit, uitstraling — laag 5) en die onderbouwen.

**Niet:**
- **Niets bevestigen** — bevestiging van materiaal ligt bij de architect/gezamenlijke dialoog (laag 5, gedeeld eigenaarschap).
- **Het bevestigde Concept niet wijzigen** en **Floor Designs niet wijzigen**.
- **Geen Floor Designs genereren** (dat is de Reasoning Engine, Fase 2).
- **Geen patroon** (Pattern Planner), **geen SVG** (SVG Planner), **geen visualisatie** (Floor Visualization Engine).

## 8. Relatie met de overige architectuurcomponenten

- **Upstream — Reasoning Engine:** levert de Floor Designs en (via de DesignContext) het bevestigde Concept. De scheiding blijft intact: de Material Planner produceert of wijzigt geen Floor Designs, de Reasoning Engine kent geen materiaal.
- **Architect:** bevestigt het materiaal (laag 5 gedeeld); de Material Planner stelt uitsluitend voor.
- **Downstream — Floor Visualization Engine:** gebruikt het bevestigde materiaal samen met Floor Design en Scene (BUILD-007). De Material Planner kent de werking van de FVE niet.

## 9. Grenzen van de verantwoordelijkheid

- Read-only op het Concept en de Floor Designs; geen enkele mutatie daarvan.
- Uitsluitend voorstellen met status "Voorgesteld"; nooit bevestigen.
- Geen patroon-, SVG-, visualisatie-, export- of persistentietaken.

## 10. Architectuurbasis (T6/T10 besloten via AB-010)

De identiteit van het Material Profile (T6) en de relatie Material Planner ↔ Material Profile (T10) zijn formeel vastgesteld in **AB-010**. Conform dat besluit geldt: een materiaalvoorstel is een **Material Profile met status "Voorgesteld"**; de Material Planner produceert uitsluitend voorgestelde Material Profiles (buiten de DesignContext) en bevestigt nooit; uitsluitend de architect bevestigt (status "Bevestigd"). Dit functioneel ontwerp is daarmee volledig gedekt door het vastgestelde architectuurbesluit.

---

**Reviewgereed:** dit document legt uitsluitend de verantwoordelijkheid, in-/output, gebruikte gegevens, beslissingen en grenzen van de Material Planner vast; de architectuurbasis (T6/T10) is vastgesteld in AB-010 (zie §10). Na een positieve VR kan het als basis dienen voor het technisch ontwerp.
