# BUILD-016 — Design Transfer Package: functioneel ontwerp

**Status:** functioneel ontwerp, gereed voor architectuurreview (VR). Beschrijft uitsluitend **wat** het Design Transfer Package (DTP) is, niet **hoe**. Geen nieuwe architectuurcomponent — het DTP is de reeds vastgestelde **laatste ketenstap** van BUILD-007 (ketenstap 11). Verankerd in BUILD-007, AB-005, BUILD-014 en BUILD-015.

**Uitgangspunt:** het DTP is **uitsluitend een overdrachtsartefact**. Het bundelt, zodra de architect tevreden is, de reeds bevestigde inhoud tot één geheel dat DCOD's technische specialisten direct kunnen oppakken. Het **maakt geen ontwerpkeuzes**, wijzigt geen enkel bron-object, schrijft niets naar de DesignContext, en bevestigt nooit.

---

## 1. Plaats in de architectuur

Het DTP is de **laatste stap** in de keten van BUILD-007 (Project → … → Floor Visualization Engine → Visualisatie → **Design Transfer Package** → DCOD). Het komt ná de Floor Visualization Engine en levert aan **DCOD** (de ontvangende partij; een mens/technische specialisten — geen technische interface, het eindpunt van de keten).

## 2. Verantwoordelijkheid

Het DTP **bundelt, overhandigt niet meer dan dat**. Zijn enige verantwoordelijkheid is het samenvoegen van de op dat moment **bevestigde** inhoud — de visie, het Floor Design, het Material Profile en de Visualisatie — tot één overdrachtsgeheel voor DCOD (BUILD-007). Het beslist niets, voegt geen ontwerpintelligentie toe, en bevestigt nooit. Het is **nadrukkelijk niet** de opvolger van de offerte-/bestelfunctionaliteit — die blijft een apart bedrijfsproces (BUILD-007).

## 3. Input

Het DTP wordt samengesteld wanneer de **architect tevreden is** (de afronding van het ontwerpgesprek) en alle bronnen bevestigd/afgerond zijn. Het leest — uitsluitend **read-only**:
- de **bevestigde Ontwerpvisie** (DesignContext, laag 1 — "de visie");
- het **bevestigde Floor Design**;
- het **bevestigde Material Profile**;
- de **Visualisatie** (het getoonde eindbeeld uit de FVE).

Het DTP muteert geen van deze bronnen en leest niets anders uit de DesignContext dan de bevestigde visie.

## 4. Output

- **Design Transfer Package:** één overdrachtsartefact dat de bevestigde inhoud bundelt — de visie, het Floor Design, het Material Profile en de Visualisatie — zodat DCOD het direct kan oppakken (BUILD-007).
- **Traceerbaarheid:** het pakket draagt herkomst-referenties naar de gebundelde bronnen (en, via de Visualisatie, transitief naar het `SVGResultaat`, het Pattern Profile, en de onderliggende bevestigde objecten).

*(Dit ontwerp beschrijft uitsluitend **welke** informatie wordt overgedragen; productie-, export- of bestandsformaat-specificaties vallen buiten dit functioneel ontwerp.)*

## 5. Gebruikte gegevens

Uitsluitend lezend (read-only):
- **DesignContext (visie):** de bevestigde Ontwerpvisie (laag 1) — de beleving en bedoeling die de architect heeft vastgesteld.
- **Floor Design:** het bevestigde ontwerpresultaat (de gekozen ontwerprichting).
- **Material Profile:** het bevestigde materiaal (uitstraling, structuur, pooltype).
- **Visualisatie:** het getoonde eindbeeld; hierin zijn — via de herkomst — het `SVGResultaat` en het Pattern Profile reeds vertegenwoordigd.

## 6. Wel / niet verantwoordelijk

**Wel:**
- de **bevestigde inhoud bundelen** (visie, Floor Design, Material Profile, Visualisatie) tot één overdrachtsartefact;
- **traceerbaarheid** meegeven (herkomst naar de gebundelde bronnen);
- **signaleren** wanneer een bron ontbreekt of niet bevestigd/afgerond is.

**Niet:**
- **geen enkel bron-object wijzigen** (Concept, Floor Design, Material Profile, Pattern Profile, `SVGResultaat`, Visualisatie);
- **niets naar de DesignContext schrijven**;
- **niet bevestigen** en **geen ontwerpkeuze maken**;
- **geen productie- of exportspecificaties** vormen;
- **geen offerte-/bestelproces** uitvoeren (apart bedrijfsproces, BUILD-007).

## 7. Relaties met upstream en downstream

- **Upstream — Floor Visualization Engine + planners + architect:** de Visualisatie (FVE), het bevestigde Floor Design en Material Profile (Reasoning Engine/Material Planner + architect) en de bevestigde visie (DesignContext) vormen de bronnen; de **architect** geeft — door tevreden te zijn — het moment aan waarop het pakket wordt samengesteld.
- **Downstream — DCOD:** het pakket wordt aan DCOD's technische specialisten overhandigd. Dit is een levering aan een mens, geen technische interface; het is het eindpunt van de keten.

## 8. Grenzen

- Het DTP is **uitsluitend een overdrachtsartefact** (bundeling); het draagt **geen ontwerpautoriteit** en voegt geen ontwerpintelligentie toe.
- Het werkt **read-only** op alle bronnen en **schrijft niets naar de DesignContext**.
- Het bevat **geen productie-/exportspecificaties** — uitsluitend welke informatie wordt overgedragen.
- Het is **nadrukkelijk niet** de offerte-/bestelfunctionaliteit (apart bedrijfsproces, BUILD-007).
- Er ontstaat **geen nieuwe architectuurcomponent** — het DTP is ketenstap 11 uit BUILD-007.

## 9. Architectuurbewaking (ter attentie van de VR)

1. **Overdrachtsartefact, geen ontwerpautoriteit.** Het DTP voegt geen ontwerpkeuze toe aan de reeds bevestigde bovenstroomse objecten; het bundelt uitsluitend (BUILD-007; AR-004/AR-005-lijn).
2. **Bundelomvang.** BUILD-007 (ketenstap 11) benoemt de bundel als visie + Floor Design + Material Profile + Visualisatie. Het Pattern Profile en het `SVGResultaat` zijn — via de herkomst van de Visualisatie — reeds traceerbaar in het pakket. Of zij daarnaast **expliciet** in het pakket horen (bijvoorbeeld het `SVGResultaat` als printbaar artefact voor DCOD's specialisten), is een punt om bij de VR/TD te bevestigen; dit functioneel ontwerp volgt vooralsnog de BUILD-007-bundel en loopt daar niet op vooruit.
3. **Status van het pakket — te beslissen bij het technisch ontwerp.** Analoog aan het `SVGResultaat` (TD-004) en de Visualisatie (TD-005, beide zonder eigen status) is het DTP een bundel van reeds bevestigde inhoud. Of het pakket een eigen Voorgesteld/Bevestigd-status krijgt dan wel een zuivere, deterministische bundeling is (zonder eigen status, samengesteld op het moment dat de architect tevreden is), wordt bewust **niet** in dit functioneel ontwerp beslist — het is een punt voor het technisch ontwerp, consistent met de eerdere uitvoerende artefacten.

---

**Reviewgereed:** dit document legt uitsluitend de verantwoordelijkheid, plaats, in-/output, gebruikte gegevens, beslissingen en grenzen van het Design Transfer Package vast, met een expliciete markering van zijn overdrachtskarakter en de twee nog te bevestigen punten (bundelomvang, status — §9). Na een positieve VR kan het als basis dienen voor het technisch ontwerp.
