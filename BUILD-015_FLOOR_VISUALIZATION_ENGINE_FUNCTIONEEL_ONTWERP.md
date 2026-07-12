# BUILD-015 — Floor Visualization Engine: functioneel ontwerp

**Status:** functioneel ontwerp, gereed voor architectuurreview (VR). Beschrijft uitsluitend **wat** de Floor Visualization Engine (FVE) doet, niet **hoe**. Geen nieuwe architectuurcomponent — de FVE is de **reeds bestaande** visualisatiecomponent (BUILD-007 ketenstap 9; VISION-001; de bestaande mockup-/floorvisualizer-engine) en **uitsluitend uitvoerend**. Verankerd in BUILD-007, VISION-001, AB-005, AR-003/004/005 en BUILD-014.

**Uitgangspunt:** de FVE **projecteert** — zij voegt het gerenderde `SVGResultaat`, het bevestigde Floor Design, het bevestigde Material Profile en de Scene samen tot één beeld (de Visualisatie). Zij **maakt nooit ontwerpkeuzes**, wijzigt geen upstream-object, schrijft niets naar de DesignContext, en bevestigt nooit.

---

## 1. Plaats in de architectuur

De FVE staat in de keten **ná de SVG Planner** (BUILD-007: Floor Design + Material Profile + Scene → Floor Visualization Engine → Visualisatie). Zij is de uitvoerende visualisatiecomponent die het gerenderde patroon (het `SVGResultaat`) op de ruimte toont. Zij is reeds vastgesteld in naam/rol (VISION-001) en herkenbaar als de bestaande mockup-engine. Downstream volgt de Design Transfer Package (BUILD-007).

## 2. Verantwoordelijkheid

De FVE **componeert, beslist niet**. Haar enige verantwoordelijkheid is het samenvoegen van:
- het **`SVGResultaat`** (de gerenderde vloerafwerking — de concrete weergave van het bevestigde patroon),
- het **bevestigde Floor Design**, het **bevestigde Material Profile** en de **Scene**,

tot één **Visualisatie** — het beeld waarin de vloerafwerking op de ruimte wordt getoond. Zij projecteert het `SVGResultaat` op het vloerpolygon van de Scene. Expliciet: zij maakt **geen ontwerpkeuzes**, voegt geen ontwerpintelligentie toe (alle intelligentie ligt vóór de FVE), en bevestigt nooit.

## 3. Input

De FVE start uitsluitend wanneer alle benodigde bronnen aanwezig en bevestigd zijn (hetzelfde deterministische gate-patroon):
- een geldig, niet-*stale* **`SVGResultaat`** (waarvan het bronpatroon bevestigd is);
- het **bevestigde Floor Design** (`status == "Bevestigd"`);
- het **bevestigde Material Profile** (`status == "Bevestigd"`);
- een beschikbare **Scene** (gestandaardiseerd: één achtergrond + één vloerpolygon, BUILD-006).

Alle invoer wordt uitsluitend **read-only** gebruikt. De FVE leest nooit rechtstreeks de DesignContext of ruwe scene-brongegevens (BUILD-007).

## 4. Output

- **Visualisatie:** het resultaat-artefact — het samengestelde beeld waarin het `SVGResultaat` op de Scene is geprojecteerd, in samenhang met Floor Design en Material Profile. De Visualisatie heeft **geen eigen verwerkingslogica** (BUILD-007); zij is het getoonde eindbeeld.
- **Motivatie:** de onderbouwing bij de Visualisatie is uitsluitend een **weergave-onderbouwing** (hoe de bevestigde inhoud getrouw is samengesteld) — geen ontwerprechtvaardiging.
- **Herkomst:** de Visualisatie draagt een herkomst-referentie naar het `SVGResultaat` (en, via diens herkomst, naar Concept, Floor Design, Material Profile en Pattern Profile) en naar de gebruikte Scene.

## 5. Gebruikte gegevens

Uitsluitend lezend (read-only):
- **`SVGResultaat`:** het SVG-artefact — de primaire visuele bron die op de Scene wordt geprojecteerd.
- **Floor Design:** de ontwerprichting (de bevestigde richting die wordt getoond).
- **Material Profile:** de materiaaleigenschappen (uitstraling, structuur, pooltype) voor een materiaalgetrouwe weergave.
- **Scene:** de achtergrond en het vloerpolygon waarop het `SVGResultaat` wordt geprojecteerd.

(Concept en Pattern Profile zijn al in het `SVGResultaat` verwerkt; de FVE leest ze niet apart.)

## 6. Wel / niet verantwoordelijk

**Wel:**
- het **`SVGResultaat` op de Scene projecteren** en samenvoegen met Floor Design en Material Profile tot één Visualisatie;
- **motiveren** (weergave-onderbouwing in het resultaat);
- **signaleren** wanneer een bron ontbreekt, niet bevestigd of *stale* is.

**Niet:**
- **niet ontwerpen**, **geen materiaal/patroon kiezen**, **geen SVG genereren** (dat zijn de Reasoning Engine, Material Planner, Pattern Planner en SVG Planner);
- **geen Concept, Floor Design, Material Profile of Pattern Profile wijzigen**;
- **niets naar de DesignContext schrijven**;
- **niet bevestigen**;
- **niet exporteren** (Design Transfer Package).

## 7. Relaties met upstream en downstream

- **Upstream — SVG Planner:** levert het `SVGResultaat` (het gerenderde patroon). De FVE consumeert dit als data-input (de in TD-004 beslechte C4-koppeling) en projecteert het.
- **Upstream — planners + architect:** het Floor Design en Material Profile zijn door de architect bevestigd; de Scene komt van de Scene Builder (BUILD-006, onafhankelijk aangeleverd).
- **Downstream — Design Transfer Package:** neemt de Visualisatie samen met de bevestigde inhoud op tot één geheel voor DCOD (BUILD-007). De FVE kent de werking van de Design Transfer Package niet.

## 8. Grenzen

- De FVE is **uitsluitend uitvoerend** (compositie/projectie); alle ontwerpintelligentie ligt ervóór (uitgangspunt 4). Zij draagt **geen ontwerpautoriteit**.
- Zij werkt uitsluitend met de gestandaardiseerde objecten (`SVGResultaat`, Floor Design, Material Profile, Scene); **nooit rechtstreeks** met ruwe scene-brongegevens of de DesignContext (BUILD-007).
- Zij **wijzigt geen enkel upstream-object** en **schrijft niets naar de DesignContext**.
- Er ontstaat **geen nieuwe architectuurcomponent** — de FVE bestaat al (VISION-001; de bestaande mockup-engine).

## 9. Architectuurbewaking (ter attentie van de VR)

1. **Uitvoerend, geen ontwerpautoriteit.** De FVE voegt geen ontwerpkeuze toe aan de reeds bevestigde bovenstroomse objecten; zij toont uitsluitend (BUILD-007, AR-004/AR-005, uitgangspunt 4).
2. **C4 reeds beslecht.** De koppeling SVG Planner → FVE is in TD-004 vastgelegd als technische data-interface (de FVE consumeert het `SVGResultaat`); dit functioneel ontwerp bevestigt die richting en opent haar niet opnieuw.
3. **Status van de Visualisatie — te beslissen bij het technisch ontwerp.** Analoog aan het `SVGResultaat` (dat conform TD-004 géén eigen bevestigingsstatus draagt) is de Visualisatie een resultaat-artefact "zonder eigen verwerkingslogica" (BUILD-007). Of de Visualisatie een eigen Voorgesteld/Bevestigd-status krijgt dan wel een zuivere, deterministische compositie van bevestigde inputs is (zonder eigen status), wordt bewust **niet** in dit functioneel ontwerp beslist — het is een punt voor het technisch ontwerp, consistent met hoe dit voor de SVG Planner is afgehandeld.

---

**Reviewgereed:** dit document legt uitsluitend de verantwoordelijkheid, plaats, in-/output, gebruikte gegevens, beslissingen en grenzen van de Floor Visualization Engine vast, met een expliciete markering van haar uitvoerende positie, de reeds beslechte C4-koppeling en het nog te beslissen status-punt (§9). Na een positieve VR kan het als basis dienen voor het technisch ontwerp — waarbij de bestaande mockup-/floorvisualizer-engine leidend is.
