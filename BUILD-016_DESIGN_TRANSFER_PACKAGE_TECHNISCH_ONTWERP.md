# BUILD-016 — Design Transfer Package: technisch ontwerp (TD-006)

**Status:** technisch ontwerp, ter review. Geen programmacode. Beschrijft uitsluitend **hoe** de Design Transfer Package Builder wordt gerealiseerd; het **wat** ligt vast in BUILD-016 en mag niet wijzigen. Geen nieuwe architectuurcomponent — het Design Transfer Package (DTP) is de reeds vastgestelde **laatste ketenstap** van BUILD-007 (ketenstap 11) en uitsluitend uitvoerend.

**Normatief:** BUILD-007 (leidend), BUILD-014, TD-004 (leidend), BUILD-015, TD-005 (leidend), BUILD-016, VR-028, en het bewezen implementatiepatroon uit de eerdere uitvoerende componenten.

**Architectuurprincipe (technisch geborgd):** de DTP Builder is een **uitsluitend uitvoerende bundelcomponent**, geen ontwerpcomponent. Zij voegt geen ontwerpkeuze toe: zij verzamelt de reeds bevestigde inhoud en serialiseert die deterministisch tot één overdrachtsartefact voor DCOD. De export-stap loopt via een **injecteerbare Transfer Boundary** die later verschillende exportformaten kan ondersteunen; de boundary bevat geen ontwerplogica en legt in dit ontwerp geen concreet productie-/exportformaat vast. Volledig additief en losstaand.

---

## Voorafgaand: twee besluiten uit VR-028 (hier beslecht)

### TD-006 — besluit 1: **bundelomvang**

Het pakket bundelt **expliciet**:
- de **bevestigde Ontwerpvisie** (DesignContext, laag 1 — "de visie");
- het **bevestigde Floor Design**;
- het **bevestigde Material Profile**;
- de **Visualisatie**;
- het **`SVGResultaat`**.

Het **Pattern Profile** en het **Concept** worden **transitief** meegenomen — als **herkomst-referentie**, niet als apart bundelonderdeel.

**Onderbouwing.** BUILD-007 benoemt als kern-bundel: visie + Floor Design + Material Profile + Visualisatie. Het `SVGResultaat` is echter het **concrete, overdraagbare vloerpatroon-artefact** dat DCOD's technische specialisten "direct kunnen oppakken" (BUILD-007). Het transitief bereiken ervan via de herkomst van de Visualisatie zou DCOD dwingen "door het beeld heen te reiken" om bij het feitelijke artefact te komen; dat past niet bij een overdrachtspakket. Daarom wordt het `SVGResultaat` **expliciet** opgenomen. Het **Pattern Profile** daarentegen is een **tussenliggend ontwerpobject** waarvan het resultaat **volledig in het `SVGResultaat` is vastgelegd**; het toevoegen als apart bundelonderdeel voegt geen overdraagbare inhoud toe. Het wordt daarom uitsluitend als herkomst meegenomen (traceerbaar, §7), net als het Concept. Dit blijft binnen het overdrachtskarakter (geen ontwerpkeuze) en verruimt de BUILD-007-kern uitsluitend met het reeds bestaande, concrete resultaat-artefact.

### TD-006 — besluit 2: **géén eigen status**

Het Design Transfer Package draagt **geen eigen Voorgesteld/Bevestigd-status**. Het is een **zuivere, deterministische bundeling** van reeds bevestigde bronnen.

**Onderbouwing.** Dit is exact hetzelfde besluit als voor het `SVGResultaat` (TD-004) en de Visualisatie (TD-005). Het bevestigings­model (Voorgesteld → Bevestigd) hoort bij *ontwerpbeslissingen* die eigendom zijn van de architect; de DTP Builder voegt géén ontwerpbeslissing toe (BUILD-007; AR-004/AR-005; BUILD-016 uitgangspunt). De **geldigheid** van het pakket leidt zich volledig af uit zijn bronnen: alle gebundelde objecten zijn bevestigd/geldig, en wijzigt één ervan, dan is het pakket *stale* en wordt het opnieuw gebundeld (§5). Het samenstellen gebeurt op het moment dat **de architect tevreden is** (BUILD-016); die tevredenheid is een handeling van de architect, geen status óp het pakket. Een eigen bevestiging zou de Builder ten onrechte beslissings­dragend maken. Dit verheldert en vervangt de eerdere, voorlopige veronderstelling in BUILD-007 (waarin een statusmechanisme voor het pakket nog open werd gelaten).

---

## 1. Architectuur

- **Eén module, één publieke component** (bijv. `design_transfer_package.py` / `DesignTransferPackageBuilder`), naast de bestaande bestanden — niet erin.
- **Interne modulegrenzen** (drie, zoals bij de eerdere componenten):
  - **Orkestratie** — stuurt de bundel-keten aan en geeft het resultaat terug.
  - **Transfer Boundary** — injecteerbaar; ontvangt een platte bundelinhoud (de read-only snapshots van de gebundelde objecten) en retourneert een **export-representatie** (het overdrachtsartefact volgens het geïnjecteerde formaat). **Bevat geen ontwerplogica**; de standaard-implementatie is een **deterministische placeholder**, en het is **format-agnostisch** zodat later verschillende exportformaten kunnen worden geïnjecteerd **zonder** de component te wijzigen. Dit ontwerp legt geen concreet productie-/exportformaat vast.
  - **Validatie & kwaliteitsborging** — controles vóór en ná de bundeling; muteren niets.
- **Uitvoerende bundelcomponent, geen ontwerpautoriteit:** de Builder leest uitsluitend, bundelt, en beslist/bevestigt niets (BUILD-007, AR-004/AR-005; BUILD-016).
- **Afhankelijkheden (read-only):** de **bevestigde Ontwerpvisie** (uit `design_context.py`, laag 1), het bevestigde `FloorDesign` (uit `reasoning_engine`), het bevestigde `MaterialProfile` (uit `material_planner`), de `Visualisatie` (uit `floor_visualization_engine`) en het `SVGResultaat` (uit `svg_planner`). Het **Pattern Profile** en het **Concept** worden niet als directe invoer gelezen — uitsluitend hun herkomst-identifiers (transitief). Het **DTP-resultaat leeft buiten de DesignContext**, in deze module. Geen wijziging aan `design_context.py`, de planner-modules, de FVE of de bestaande render-/projectiecode.

## 2. Verwerkingsketen

- **Invoer:** de bevestigde Ontwerpvisie (read-only uit de DesignContext), het bevestigde `FloorDesign`, het bevestigde `MaterialProfile`, de `Visualisatie` en het `SVGResultaat` (alle read-only).
- **Verwerking:** gate → verzamelen van de bundelinhoud (read-only snapshots van de vijf expliciete onderdelen + de transitieve herkomst van Pattern Profile en Concept) → **Transfer Boundary** (serialiseert de bundel tot de export-representatie volgens het geïnjecteerde formaat) → kwaliteitsborging → verpakken als `DesignTransferPackage` (met herkomst).
- **Gate:** `FloorDesign.status == "Bevestigd"` **én** `MaterialProfile.status == "Bevestigd"` **én** een **geldig** `SVGResultaat` (niet-leeg, identifier aanwezig) **én** een **niet-*stale* `Visualisatie`** (haar `SVGResultaat`-herkomst komt overeen met het aangeleverde `SVGResultaat`) **én** een **bevestigde, volledige Ontwerpvisie** (laag 1: `OntwerpVisie.bevestigd_door_architect is True` én ten minste één inhoudelijk visie-veld gevuld) **én** **interne herkomst-coherentie** (§4); anders geen bundeling (signalering).
- **Grens van de *stale*-controle (consistent met besluit 1):** de content-*staleness* van het `SVGResultaat` t.o.v. zijn Pattern Profile wordt door de DTP **niet zelfstandig herbeoordeeld** — de Builder ontvangt het Pattern Profile-object niet (uitsluitend transitief via de herkomst-identifier). Die *staleness* is reeds door de **upstream-poorten** (SVG Planner → FVE) geborgd: een `Visualisatie` kon uitsluitend ontstaan uit een niet-*stale* `SVGResultaat`. De DTP borgt daarbovenop uitsluitend dat de aangeleverde `Visualisatie` en het `SVGResultaat` **hetzelfde** object betreffen (identifier-gelijkheid) en dat de keten coherent is (§4).
- **Uitvoer:** één `DesignTransferPackage` (het overdrachtsartefact + herkomst) buiten de DesignContext + resultaatwikkel.
- **Foutafhandeling:** falende gate of export-fout → signalering/foutresultaat; **geen partieel pakket**; DesignContext en alle invoer blijven ongewijzigd.

## 3. Gegevensmodellen (technische representatie)

- **`DesignTransferPackage`** — resultaat-artefact **buiten** de DesignContext: identifier; de **gebundelde inhoud** (read-only snapshots van: bevestigde visie, Floor Design, Material Profile, Visualisatie, `SVGResultaat`); de **export-representatie** (het door de Transfer Boundary geproduceerde overdrachtsartefact); een **overdrachts-motivering** (uitsluitend hoe de bevestigde inhoud getrouw is gebundeld — geen ontwerprechtvaardiging); herkomst-referenties (incl. transitief Pattern Profile + Concept); kwaliteitsinformatie. **Geen eigen status** (besluit 2).
- **Overdrachts-motivering** — de bundel-onderbouwing, in het object.
- **Kwaliteitsinformatie** — bijv. bundel-status (volledig/incompleet), resultaat van de coherentie-controle, het gebruikte exportformaat (welk formaat de boundary leverde), pogingen.
- **Traceerbaarheid/herkomst** — zie §7.

## 4. Validatie

- **Uitsluitend bevestigde/geldige invoer:** de gate (§2) toetst de bevestigde statussen van Floor Design en Material Profile, een geldig `SVGResultaat`, een niet-*stale* `Visualisatie`, en een bevestigde, volledige Ontwerpvisie. Laag 1 (`OntwerpVisie`) draagt **geen string-status** (Voorgesteld/Bevestigd zit op het Concept, laag 4), maar wél een expliciete bevestigingsvlag **`bevestigd_door_architect: bool`**; de Builder toetst daarom die vlag (`is True`) **plus volledigheid** (ten minste één inhoudelijk visie-veld gevuld) — read-only, zonder de vlag ooit te zetten. Dit is hetzelfde poort-criterium dat de Ontwerpstrategie-stap (BUILD-009 technisch, §"bevestigde, niet-lege Ontwerpvisie") al hanteert; de correctie is een alignering met dat gevestigde precedent en met het datamodel, geen nieuwe keuze.
- **Interne herkomst-coherentie:** de aangeleverde objecten moeten **één samenhangende ontwerpketen** vormen. De Builder controleert dat de herkomst-identifiers kloppen: de `Visualisatie` verwijst naar exact het aangeleverde `SVGResultaat`, en het `SVGResultaat` verwijst naar exact het aangeleverde Floor Design en Material Profile (en, transitief, naar het bijbehorende Pattern Profile en Concept). Dit voorkomt dat objecten uit verschillende ontwerptrajecten per ongeluk worden samengebundeld.
- **Volledigheid:** alle vijf expliciete bundelonderdelen aanwezig en niet-leeg; ontbreekt er één, dan is de bundel *incompleet* → afgewezen.
- **Consistentie bundel ↔ bronnen:** de bundeling is een deterministische functie van de invoer. De kwaliteitsborging toetst **formaat-onafhankelijk** dat de export-representatie bruikbaar is — dat wil zeggen: de Transfer Boundary heeft succesvol en zonder fout een niet-lege representatie geretourneerd — en dat de herkomst naar de gebruikte objecten klopt. Elke **formaat-specifieke** validatie (schema, bestandsstructuur) hoort in de geïnjecteerde boundary, niet in deze laag, zodat de component format-agnostisch blijft. Een incomplete bundel of een uitgebleven/lege boundary-retour wordt niet als geldig teruggegeven en niet verpakt.

## 5. Regeneratie / herstel

- **Wanneer:** bij een technische export-fout, óf wanneer een bron is gewijzigd waardoor het bestaande pakket *stale* is (de `Visualisatie` of het `SVGResultaat` is *stale* geworden, of een eerder bevestigd object is opnieuw "Voorgesteld").
- **Welke stap opnieuw:** uitsluitend de bundeling + export (Transfer Boundary + kwaliteitsborging) opnieuw; de bevestigde bronnen blijven ongewijzigd behouden — er is **geen ontwerpstap** in deze component. Is een bron zelf *stale*, dan wordt eerst **upstream** herbouwd (nieuw `SVGResultaat` via de SVG Planner en/of een nieuwe `Visualisatie` via de FVE), waarna de Builder opnieuw bundelt.
- **`is_stale`:** het pakket is *stale* zodra een gebundelde bron-identifier niet meer overeenkomt — in het bijzonder wanneer de herkomst-identifier van de gebruikte `Visualisatie` of het `SVGResultaat` afwijkt van het actuele object.
- **Geen oneindige lus:** omdat de bundeling *deterministisch* is, levert een herhaling met ongewijzigde invoer hetzelfde resultaat; een technische regeneratielimiet voorkomt eindeloos herhalen bij een blijvende export-fout → signalering.

## 6. Interfaces

- **FVE → DTP Builder:** de `Visualisatie` is **data-input** — exact de in BUILD-015/TD-005 §6 vastgelegde richting (de FVE roept de DTP Builder **niet** aan). Deze wordt hier niet heropend.
- **SVG Planner → DTP Builder:** het `SVGResultaat` is **data-input** (read-only), consistent met de in TD-004 vastgestelde data-interface; de SVG Planner roept de Builder niet aan.
- **Planners + architect → DTP Builder:** leveren het bevestigde Floor Design en Material Profile; read-only.
- **DesignContext → DTP Builder:** de Builder **leest** uitsluitend de bevestigde Ontwerpvisie (laag 1); zij **schrijft niets** naar de DesignContext.
- **DTP Builder → DesignTransferPackage:** produceert het `DesignTransferPackage` (buiten de DesignContext), teruggegeven via de resultaatwikkel — niet in de DesignContext geschreven; geen eigen bevestiging (besluit 2).
- **DTP Builder → DCOD:** het pakket wordt aan DCOD's technische specialisten overhandigd. Dit is een levering aan een mens, **geen technische interface**; het is het eindpunt van de keten. De Builder kent geen productie-/bestelproces (BUILD-007/BUILD-016).
- **Transfer Boundary:** injecteerbaar; ontvangt de platte bundelinhoud en retourneert de export-representatie; **format-agnostisch**; standaard = deterministische placeholder; bevat geen ontwerplogica en legt geen concreet productie-/exportformaat vast (dat kan later worden geïnjecteerd).

## 7. Traceerbaarheid

- Elk `DesignTransferPackage` draagt een **herkomst-referentie naar elk expliciet gebundeld object** (identifiers van de bevestigde visie, het Floor Design, het Material Profile, de `Visualisatie` en het `SVGResultaat`) en — **transitief** — naar het **Pattern Profile** en het **Concept** (via de herkomst van het `SVGResultaat`).
- Er wordt **niets in de DesignContext geregistreerd** (buiten de DesignContext) — analoog aan het `SVGResultaat`, de Visualisatie en de eerdere resultaat-objecten.

## 8. Robuustheid

- **Fouttolerantie:** de Transfer-Boundary-aanroep in een `try/except`; een technische fout → gestructureerd foutresultaat, **nooit** een partieel of onwelgevormd pakket; DesignContext en bronnen ongewijzigd.
- **Herstelgedrag:** her-bundeling bij een gewijzigde/*stale* bron of een technische fout, met regeneratielimiet (§5).
- **Read-only snapshots:** de bundelinhoud wordt als read-only snapshot verzameld; de Builder muteert geen enkel bron-object. (Een projectbrede defensieve-kopie-afweging blijft, net als bij de eerdere componenten, een latere uniforme kwaliteitsronde.)
- **Uitbreidbaarheid:** de Transfer Boundary is injecteerbaar — de standaard is een deterministische placeholder, maar een concreet exportformaat kan worden geïnjecteerd **zonder** de component te wijzigen.
- **AI-model-onafhankelijk / deterministisch:** de bundeling is deterministisch; geen model, geen prompt.
- **Additief:** nieuw bestand; geen wijziging aan `design_context.py`, de planner-modules, de FVE of de bestaande render-/projectiecode; geen koppeling aan de live pipeline tot er bewust wordt aangesloten.

---

**Acceptatie:** met een bevestigd Floor Design en Material Profile, een geldig `SVGResultaat`, een niet-*stale* `Visualisatie`, een aanwezige, volledige Ontwerpvisie en een coherente onderlinge herkomst levert de DTP Builder één `DesignTransferPackage` (de vijf expliciet gebundelde onderdelen + de export-representatie + herkomst naar alle onderdelen en, transitief, naar Pattern Profile en Concept, met overdrachts-motivering) buiten de DesignContext, **zonder eigen status**; een ontbrekende/niet-bevestigde bron, een *stale* `Visualisatie`, een incoherente herkomst of een technische export-fout leiden tot een signalering/foutresultaat en, waar van toepassing, gelimiteerde her-bundeling — zonder mutatie van de DesignContext of de bronnen, zonder ontwerpkeuze en zonder bevestiging.
