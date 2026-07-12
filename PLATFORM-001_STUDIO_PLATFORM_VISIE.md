# PLATFORM-001 — Studio Platform Visie

**Status:** visiedocument / strategische platformarchitectuur. **Geen technisch ontwerp, geen implementatie, geen code, geen architectuurwijziging.** Legt de langetermijnvisie vast waarbinnen alle toekomstige BUILD- en IMP-trajecten vallen.

**Aard:** dit document is **richtinggevend, niet normatief**. De bestaande, bekrachtigde architectuur (AB-006, AB-009, AB-012, BUILD-007, BUILD-023, IMP-014, BUILD-024) blijft **volledig leidend**. Waar deze visie en een bestaand architectuurbesluit ooit zouden lijken te botsen, wint het bestaande besluit; PLATFORM-001 introduceert geen afwijkende architectuur en verplicht tot geen enkele herstructurering.

**Funderingsfase afgerond:** BUILD-023 (orchestrator TD), IMP-014 (orchestrator-guardlaag) en BUILD-024 (contract hardening) zijn technisch beoordeeld, IMPLEMENTATIEGEREED en lokaal gecommit (nog niet gepusht). Op die fundering rust deze visie.

---

## Doel

Vastleggen van de strategische platformarchitectuur waar alle toekomstige BUILD- en IMP-trajecten onder vallen. Uitsluitend de langetermijnvisie van het Studio Platform; nadrukkelijk géén technisch ontwerp.

---

## Uitgangspunten

### 1. Eén Studio Platform

Er bestaat **één generiek Studio Platform** — niet "DCOD Studio", "Dutch Carpets Studio" of "Dealer Studio", maar één platform waarop meerdere ervaringen kunnen draaien. Merk- en doelgroepnamen zijn ervaringen ván het platform, niet aparte platformen.

### 2. Experience Layer

Het platform ondersteunt meerdere **Experience Layers** (bv. Professional, Consumer, Dealer, Partner, Internal, White-label). Een Experience Layer bepaalt **uitsluitend**: branding, terminologie, rechten, navigatie, gebruikersreis en beschikbare functionaliteit. Een Experience Layer bevat **geen ontwerp- of AI-logica**.

### 3. Eén Design Workflow

Alle Experience Layers gebruiken **dezelfde Design Workflow**. De workflow kent geen doelgroep — uitsluitend ontwerpstappen. Er ontstaan **geen** afzonderlijke workflows voor architecten, consumenten of dealers. (Dit is de bestaande BUILD-007-keten; PLATFORM-001 hernoemt of herstructureert die niet.)

### 4. Capabilities

De Design Workflow maakt gebruik van afzonderlijke **capabilities** (bv. Reasoning, Trend, Material, Mockup, SVG, Product, Visualisatie, DTP). Capabilities zijn **zelfstandig uitbreidbaar**: een nieuwe capability wordt additief toegevoegd zonder bestaande capabilities te raken.

### 5. AI is een capability

AI vormt **geen kern** van het platform; AI is uitsluitend een **implementatie van een capability**. Een capability kan daardoor in de toekomst worden gerealiseerd met een ander AI-model, meerdere AI-modellen, regelsystemen of hybride oplossingen — **zonder** wijziging van de workflow, de orchestrator, de contracten of de objectmodellen. Dit is exact het reeds vastgelegde boundary-principe (BUILD-023/BUILD-024): een capability implementeert enkel het contract.

### 6. Merken

Het platform ondersteunt **meerdere merken** (bv. DCOD, Dutch Carpets, toekomstige merken, white-label partners). De merkidentiteit bevindt zich **uitsluitend in de Experience Layer** — nooit in de workflow of de capabilities.

### 7. Kanaalonafhankelijkheid

Het platform ondersteunt meerdere distributiekanalen (eigen website, dealerportaal, architectenportaal, verkoopportal, mobiele applicatie, API-koppelingen). **Kanaalkeuze heeft geen invloed op de Design Workflow.**

### 8. Architectuurprincipes

De bestaande architectuur blijft **volledig leidend**. Ongewijzigd gerespecteerd: **AB-006, AB-009, AB-012, BUILD-007, BUILD-023, IMP-014, BUILD-024**. PLATFORM-001 introduceert **geen** afwijkende architectuur.

### 9. Uitbreidbaarheid

Nieuwe capabilities moeten **additief** kunnen worden toegevoegd. Zij mogen **niet** leiden tot wijzigingen aan: bestaande workflow, orchestratie, contracten, resultaatobjecten of bestaande capabilities. Dit is de directe voortzetting van de additief-only versieregel uit BUILD-024.

### 10. Toekomstvisie

Het Studio Platform moet geschikt blijven voor uitbreiding naar nieuwe producten, merken, markten, AI-technologieën, Experience Layers en distributiekanalen — **zonder fundamentele herstructurering** van de architectuur.

---

## Verankering in de bestaande architectuur

Deze visie is geen nieuwe laag bovenop het systeem; zij is een **naamgevende, strategische duiding** van wat er architectonisch al staat. De platformbegrippen mappen één-op-één op bestaande onderdelen:

| Platformbegrip (PLATFORM-001) | Bestaand onderdeel | Bindend document |
|---|---|---|
| **Design Workflow** | de Design Brain-keten (Conversation Planner → Context Interpreter → Ontwerpstrategie → Reasoning Engine → Material/Pattern Planner → SVG Planner → Floor Visualization Engine → DTP) | BUILD-007 |
| **Capability** | een component/boundary in de keten (`RedeneerFunctie`/`*RedeneerFunctie`/`SVGRenderFunctie`/`VisualisatieBoundary`/`TransferFunctie`) | BUILD-023, BUILD-024 |
| **AI-implementatie van een capability** | een productie-reasoning-boundary achter het bestaande, model-onafhankelijke contract | BUILD-024 §5, AB-012 |
| **Orchestratie** | de guardlaag in de integratielaag (hergebruik/invalidatie via herkomst + `is_stale`) | BUILD-023, IMP-014 |
| **Contracten / resultaatobjecten** | de formele, additief-uitbreidbare boundary-contracten | BUILD-024 |
| **Experience Layer** | de presentatie-/ervaringslaag; het huidige `/ontwerp`-atelier is de **eerste** Experience Layer-instantie (Professional-gericht) | BUILD-021, BUILD-022 |
| **Merk** | branding binnen de Experience Layer; **DCOD** is de eerste merk-instantie | AB-012, BUILD-022 |

**Belangrijke afbakening:** het woord *"capability"* is een **conceptueel koepelbegrip** voor de reeds bestaande componenten/boundaries — geen nieuwe architectuurlaag en geen aanleiding tot hernoemen of herbouwen van code. Evenzo is *"Experience Layer"* de bestaande frontend-/ervaringslaag; er wordt met PLATFORM-001 geen tweede frontend, geen merk-rename en geen kanaal-splitsing gebouwd. Die stappen zijn latere, optionele en additieve BUILD-trajecten die pas op expliciete opdracht ontstaan.

---

## Consistentietoets

- **AB-006 / AB-009:** statusvocabulaire en de Floor Design-positionering (Fase 2 binnen de Reasoning Engine) blijven ongemoeid; PLATFORM-001 raakt geen resultaatobject of status.
- **AB-012:** "AI is een capability" en de merk-/ervaringsscheiding sluiten naadloos aan op de verborgen AI-infrastructuur; niets in deze visie maakt AI, model of sleutel zichtbaar.
- **BUILD-007:** één Design Workflow = de bestaande keten; geen doelgroep-specifieke workflows, geen wijziging aan volgorde of bevestigingsmomenten.
- **BUILD-023 / IMP-014:** de orchestratie blijft de dunne guardlaag in de integratielaag; capabilities worden aangeroepen of overgeslagen, nooit aangepast.
- **BUILD-024:** "capabilities zijn zelfstandig/additief uitbreidbaar" ís de additief-only contractregel; boundary-onafhankelijkheid maakt het inwisselen van AI-implementaties mogelijk zonder contractwijziging.
- **Platform-/kanaalonafhankelijkheid:** doordat Experience Layer, merk en kanaal buiten de workflow en de capabilities staan, kan het platform naar nieuwe ervaringen, merken en kanalen groeien zonder de architectuur te herstructureren.

---

**Reviewgereed:** dit visiedocument legt de strategische platformarchitectuur van het Studio Platform vast — één platform, meerdere Experience Layers, één Design Workflow, capabilities (waaronder AI als inwisselbare capability-implementatie), merk- en kanaalonafhankelijkheid, additieve uitbreidbaarheid en toekomstvastheid — als richtinggevende duiding bovenop de bestaande, leidende architectuur (AB-006/009/012, BUILD-007/023/024, IMP-014), zonder enige code-, contract- of architectuurwijziging. Hiermee is de funderings- én visieperiode afgesloten en kan de eerste productie-reasoning-capability (Ontwerpstrategie) binnen dit kader worden aangesloten.
