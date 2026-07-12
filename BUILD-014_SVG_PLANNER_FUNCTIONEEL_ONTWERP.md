# BUILD-014 — SVG Planner: functioneel ontwerp

**Status:** functioneel ontwerp, gereed voor architectuurreview (VR). Beschrijft uitsluitend **wat** de SVG Planner doet, niet **hoe**. Geen nieuwe architectuurcomponent — de SVG Planner is de **reeds erkende, bestaande** SVG-generatiepipeline (AB-005) en **uitsluitend uitvoerend** (AR-004/AR-005; DESIGN_BRAIN uitgangspunt 4). Verankerd in AB-005, AR-003, AR-004, BUILD-007, AB-011, BUILD-013 en TD-003.

**Uitgangspunt:** de SVG Planner verzorgt uitsluitend een **uitvoerende vertaalslag** — hij rendert een bevestigd patroon tot een SVG. Hij **maakt nooit ontwerpkeuzes**, wijzigt nooit Pattern Profiles, en bevestigt nooit.

---

## 1. Plaats in de architectuur

De SVG Planner staat in de interne opbouw van de Design Brain als de uitvoerende sluitpost (DESIGN_BRAIN: Reasoning Engine → Material Planner / Pattern Planner / **SVG Planner**), en in de keten **ná de Pattern Planner**:
- **Pattern Profile** — het bevestigde patroon dat de SVG Planner rendert; alle ontwerpintelligentie ligt vóór de SVG Planner (uitgangspunt 4).
- **Floor Visualization Engine** — gebruikt (downstream) het gerenderde resultaat samen met Floor Design, Material Profile en Scene (BUILD-007). De precieze koppeling SVG ↔ visualisatie blijft een open technische interface (AR-003, C4) en wordt hier niet vastgelegd.
- **Design Transfer Package** — bundelt (verderop) de bevestigde inhoud voor DCOD (BUILD-007).

## 2. Verantwoordelijkheid

De SVG Planner **rendert, beslist niet**. Zijn enige verantwoordelijkheid is het vormen van een **SVG-voorstel** — de getrouwe visuele weergave van het bevestigde patroon. Expliciet:
- hij vormt **uitsluitend SVG-voorstellen** (uitvoerende weergaven);
- hij **maakt nooit ontwerpkeuzes** (die liggen vast in Concept, Floor Design, Material Profile en Pattern Profile);
- hij **wijzigt nooit Pattern Profiles** (noch enig ander upstream-object);
- hij **bevestigt nooit**.

## 3. Input

De SVG Planner start uitsluitend wanneer alle upstream-objecten bevestigd zijn — hetzelfde deterministische gate-patroon als de eerdere planners:
- het **bevestigde Concept** (laag 4, `status == "bevestigd"`);
- het **bevestigde Floor Design** (`status == "Bevestigd"`);
- het **bevestigde Material Profile** (`status == "Bevestigd"`);
- het **bevestigde Pattern Profile** (`status == "Bevestigd"`).

Ontbreekt of is er één niet bevestigd, dan start de SVG Planner niet. Alle invoer wordt uitsluitend **read-only** gebruikt.

## 4. Output

- **SVG-resultaat:** een SVG — de getrouwe uitvoerende weergave van het bevestigde patroon op de vloerafwerking. Eventuele meervoudigheid (bijv. tegeling/resolutie) is **technisch**, nooit een ontwerpvariant.
- **Status:** het SVG-resultaat heeft **geen eigen bevestigingsstatus** (TD-004): het is een **deterministische rendering** van het bevestigde Pattern Profile en bevat **geen ontwerpkeuze**. Zijn geldigheid volgt volledig uit het bevestigde Pattern Profile waarnaar het verwijst; wijziging verloopt uitsluitend via een upstream-object, niet via het SVG-resultaat. De SVG Planner bevestigt nooit.
- **Motivatie:** de onderbouwing bij het SVG-resultaat is uitsluitend een **weergave-onderbouwing** (hoe het bevestigde patroon getrouw is gerenderd) — geen ontwerprechtvaardiging.
- **Herkomst:** het SVG-resultaat draagt een herkomst-referentie naar het bevestigde Pattern Profile (en, via diens herkomst, naar Concept, Floor Design en Material Profile).

## 5. Gebruikte gegevens

Uitsluitend lezend (read-only):
- **Concept:** kleurpalet en, waar relevant voor de weergave, stijl/complexiteit/motiefschaal.
- **Floor Design:** de ontwerprichting (de bevestigde richting die wordt weergegeven).
- **Material Profile:** structuur, pooltype en uitstraling (voor een materiaalgetrouwe weergave).
- **Pattern Profile:** de patroonbeschrijving (motiefstructuur, motiefschaal, dichtheid, herhalingskarakter) — de primaire bron voor de rendering.

## 6. Wel / niet verantwoordelijk

**Wel:**
- **SVG-voorstellen vormen** (de uitvoerende weergave van het bevestigde patroon);
- **motiveren** (weergave-onderbouwing in het resultaat);
- **signaleren** wanneer de bevestigde invoer onvoldoende is om te renderen.

**Niet:**
- **niet ontwerpen**, **geen materialen kiezen**, **geen patronen vormen** (dat zijn de Reasoning Engine, Material Planner en Pattern Planner);
- **niet visualiseren** (Floor Visualization Engine);
- **niet exporteren**;
- **niet bevestigen**.

## 7. Relaties

- **Pattern Planner (upstream):** levert — na bevestiging door de architect — het Pattern Profile dat de SVG Planner rendert. De SVG Planner wijzigt het Pattern Profile niet en beslist niets.
- **Floor Visualization Engine (downstream):** gebruikt het gerenderde resultaat samen met Floor Design, Material Profile en Scene tot één beeld (BUILD-007). De SVG Planner kent de werking van de FVE niet; de koppeling SVG ↔ visualisatie blijft een open technische interface (AR-003, C4).
- **Design Transfer Package (downstream):** verwerkt de bevestigde inhoud conform de bestaande architectuur (BUILD-007).

## 8. Grenzen

- Alle **upstream-objecten moeten bevestigd** zijn (Concept, Floor Design, Material Profile, Pattern Profile) voordat de SVG Planner start.
- De SVG Planner verzorgt **uitsluitend een uitvoerende vertaalslag** (rendering); alle ontwerpintelligentie ligt ervóór (uitgangspunt 4).
- Er wordt **geen DesignContext gewijzigd** (read-only op alle invoer).
- Er ontstaat **geen nieuwe architectuurcomponent** — de SVG Planner bestaat al (AB-005).

## 9. Architecturale positie (ter attentie van de VR)

Twee punten, ter borging van consistentie met de reeds vastgestelde architectuur:
1. **Uitvoerend, geen ontwerpautoriteit.** De SVG Planner is uitsluitend uitvoerend en draagt geen ontwerpautoriteit (AR-004/AR-005). Het SVG-resultaat is een aangeboden, deterministische rendering **zonder eigen bevestigingsstatus** (TD-004), niet een ontwerpbeslissing; de SVG Planner voegt geen enkele ontwerpkeuze toe aan de reeds bevestigde bovenstroomse objecten.
2. **Reeds bestaand + open koppeling.** De SVG Planner is de reeds erkende bestaande SVG-generatiepipeline (AB-005). De precieze technische koppeling tussen zijn output en de Floor Visualization Engine/visualisatie is een open technische interface (AR-003, C4) en wordt door dit functioneel ontwerp niet besloten.

---

**Reviewgereed:** dit document legt uitsluitend de verantwoordelijkheid, plaats, in-/output, gebruikte gegevens, beslissingen en grenzen van de SVG Planner vast, met een expliciete markering van zijn uitvoerende positie en de open technische koppeling (§9). Na een positieve VR kan het als basis dienen voor het technisch ontwerp — waarbij de bestaande pipeline (AB-005) en de open koppeling (C4) leidend zijn.
