# BUILD-030 — Studio Architecture Index & Freeze

**Status:** centraal architectuurregister / officiële inhoudsopgave van de DCOD Studio-architectuur en de vaste ingang voor alle toekomstige ontwikkeling. **Document-only. Geen code, geen implementatie, geen contractwijziging, geen nieuwe architectuur.** Bundelt en structureert uitsluitend reeds goedgekeurde documenten. **Bij enig verschil prevaleert altijd het oorspronkelijke brondocument.**

---

## 1. Architectuuroverzicht

De DCOD Studio is één samenhangend platform, opgebouwd in vier lagen (zie de hoofdkaart BUILD-029): **Experience Layer** (merk/kanaal/modaliteit/UX/gesprek) → **API-/integratielaag** (endpoints, `Gesprekstoestand`, orkestratie-guards, server-side sleutel) → **Design Brain** (domein/redenering, ongewijzigd) → **productie/downstream** (SVG, visualisatie, transfer package). Dwars daarover: platformvisie, ontwerpfilosofie, contracten, governance en security. De Design Brain redeneert; de Experience Layer verzorgt beleving en modaliteit; de contracten en de workflow verbinden beide, additief en stabiel.

## 2. & 3. Architectuurregister met status

**Blanket-regel:** geen enkel document in dit register **vervangt** een ander; de architectuur is additief (BUILD-024-geest). Dit register is enkel een index.

### Fundament

| Doc | Doel | Status | Afhankelijk van | Gebruikt door |
|---|---|---|---|---|
| **PLATFORM-001** | Studio Platform-visie: één platform, Experience Layers, capabilities, merk-/kanaalonafhankelijkheid | Vastgesteld | — | alle latere platform-/experience-docs |
| **PLATFORM-002** | Conversation Experience / Design Dialogue-visie | Vastgesteld | PLATFORM-001 | BUILD-025/026/027/028 |

### Governance

| Doc | Doel | Status | Afhankelijk van | Gebruikt door |
|---|---|---|---|---|
| **SEC-001** | Security & Intellectual Property-strategie | Vastgesteld | PLATFORM-001/002, BUILD-023/024, REASONING-001 | LEGAL-001, alle IMP/RELEASE |
| **LEGAL-001** | Vertrouwelijke juridische vastlegging (auteurschap/IE) — **buiten de repository** | Vastgesteld (concept, ter juridische toetsing) | SEC-001 | — |

### Design Brain

| Doc | Doel | Status | Afhankelijk van | Gebruikt door |
|---|---|---|---|---|
| **REASONING-001** | Ontwerpfilosofie & reasoning-principes (bron van waarheid voor reasoning) | Vastgesteld | PLATFORM-001 | alle IMP/VAL, BUILD-025..028 |
| **BUILD-023** | AI Resource & Orchestration Architecture (AP-001; R1–R6) | Vastgesteld | BUILD-007/008/019, IMP-014 | alle IMP/VAL, orkestratielaag |
| **BUILD-024** | Contract Hardening (formele, additief-only boundary-contracten) | Vastgesteld | BUILD-023, AB-006/009/012 | alle IMP/VAL, modaliteiten |

### Studio Experience

| Doc | Doel | Status | Afhankelijk van | Gebruikt door |
|---|---|---|---|---|
| **BUILD-025** | Conversation Experience & Voice Architecture (TD) | Architectonisch afgerond | PLATFORM-002, REASONING-001 | BUILD-026/027/028/029 |
| **BUILD-025-A** | Afsluitend architectuurbesluit bij BUILD-025 (canonieke 8-fasenstroom; keuzes → IMP-020) | Vastgesteld | BUILD-025/026/027/028 | IMP-020 |
| **BUILD-026** | Conversation State Architecture (afgeleide toestand op `Gesprekstoestand`) | Vastgesteld | BUILD-019/025, AB-006 | BUILD-028/029, IMP-020 |
| **BUILD-027** | Multimodal Experience Architecture (modaliteiten = adapters → contract-invoer) | Vastgesteld | BUILD-004/024/025 | BUILD-028/029, IMP-020 |
| **BUILD-028** | Studio UX Architecture (Dessinator als ontwerpcollega; gebruikersreis) | Vastgesteld | BUILD-021/022/025/026/027 | BUILD-029, IMP-020 |
| **BUILD-029** | Studio Platform Blueprint (hoofdkaart, synthese) | Vastgesteld | alle bovenstaande | BUILD-030 |

### Implementaties (productie-Reasoning Capabilities)

| Doc | Doel | Status | Afhankelijk van | Gebruikt door |
|---|---|---|---|---|
| **IMP-015** | Productie Ontwerpstrategie | IMPLEMENTATIEGEREED, live-gevalideerd | BUILD-023/024, REASONING-001 | VAL-001, downstream |
| **IMP-016** | Productie Conceptvorming | IMPLEMENTATIEGEREED, live-gevalideerd | IMP-015-infra | VAL-002, Floor Design |
| **IMP-017** | Productie Floor Design | IMPLEMENTATIEGEREED, live-gevalideerd | IMP-016 | VAL-003, Material |
| **IMP-018** | Productie Material Planning | IMPLEMENTATIEGEREED, live-gevalideerd | IMP-017 | VAL-004, Pattern |
| **IMP-019** | Productie Pattern Planning | IMPLEMENTATIEGEREED, live-gevalideerd | IMP-018 | VAL-005, SVG |

### Validaties

| Doc | Doel | Status | Afhankelijk van | Gebruikt door |
|---|---|---|---|---|
| **VAL-001** | Live validatie Ontwerpstrategie | IMPLEMENTATIEGEREED | IMP-015 | RELEASE-001 |
| **VAL-002** | Live validatie keten strategie→concept | IMPLEMENTATIEGEREED | IMP-016 | RELEASE-001 |
| **VAL-003** | Live validatie keten t/m Floor Design | IMPLEMENTATIEGEREED | IMP-017 | RELEASE-002 |
| **VAL-004** | Live validatie t/m Material Planning (+ token-fix) | IMPLEMENTATIEGEREED | IMP-018 | RELEASE-003 |
| **VAL-005** | Live validatie t/m Pattern Planning | Live-validatie afgerond; eindoordeel in VAL-005-rapport | IMP-019 | RELEASE-004 (voorstel) |

**Onderliggende fundering (eerder bekrachtigd, blijft bindend):** AB-005 (SVG-pipeline), AB-006 (statusvocabulaire), AB-009 (Floor Design = Fase 2), AB-012 (verborgen AI); BUILD-004 (Context Interpreter), BUILD-007 (workflow/ketenvolgorde), BUILD-008 (gates), BUILD-009/010/011/012/013 (strategie/concept/floor/material/pattern-boundaries), BUILD-016 (Design Transfer Package), BUILD-017 (Conversation Planner), BUILD-018 (SVG-pipeline-integratie), BUILD-019 (Flask/`Gesprekstoestand`), IMP-014 (orchestrator-guardlaag). Deze documenten worden door bovenstaande register-documenten gebruikt en blijven leidend.

## 4. Architectuur Freeze

De **fundamentele Studio-architectuur wordt hiermee als stabiel beschouwd (bevroren).**

- Nieuwe **BUILD-**, **PLATFORM-** of **REASONING-**documenten worden vanaf dit punt **uitsluitend** toegevoegd wanneer sprake is van een **fundamentele architectuurwijziging**.
- Nieuwe functionaliteit wordt vanaf hier normaal ontwikkeld via **IMP → VAL → RELEASE**.
- Architectuurdocumentatie groeit vanaf nu alleen nog mee wanneer de architectuur werkelijk verandert.

## 5. Rangorde (permanent leidend)

```
Architectuur → Technisch ontwerp → Implementatie → Validatie → Release
```

Deze volgorde blijft permanent leidend: geen implementatie zonder architectuur/ontwerp, geen release zonder validatie.

## 6. Bron van waarheid

BUILD-030 dient **uitsluitend als architectuurindex**. De inhoud vervangt nooit de oorspronkelijke documenten; bij verschillen prevaleert **altijd** het oorspronkelijke bronbestand. Dit register wordt bijgewerkt wanneer een nieuw architectuurdocument wordt bekrachtigd of een status wijzigt — niet als vervanging, maar als wegwijzer.

---

## Technical Review — consistentietoets

- **Volledigheid:** alle door de opdracht benoemde documenten zijn opgenomen; de eerder bekrachtigde fundering is als aparte, bindende sectie toegevoegd zodat het register de kern-workflow (BUILD-007), de verborgen AI (AB-012) en de gates (BUILD-008) niet weglaat.
- **Documentstructuur & verwijzingen:** logische groepering (Fundament / Governance / Design Brain / Studio Experience / Implementaties / Validaties) met per document doel, status, afhankelijkheden en "gebruikt door"; geen circulaire of ontbrekende verwijzingen geconstateerd.
- **Consistentie & backward compatibility:** geen document wordt vervangen of gewijzigd; het register is puur additief en verandert geen enkel besluit (BUILD-024-geest).
- **Rangorde & freeze:** de hiërarchie en de freeze-regel zijn expliciet vastgelegd en consistent met de bestaande werkwijze (VR/TR/CR; push op autorisatie).
- **Prevalentie:** expliciet vastgelegd dat het bronbestand altijd prevaleert.

**TR-oordeel: IMPLEMENTATIEGEREED.**

---

**Reviewgereed:** dit document is het centrale architectuurregister en de architectuur-freeze van de DCOD Studio — een gegroepeerde, gestatuste index van alle goedgekeurde documenten (plus de bindende onderliggende fundering), met de permanente rangorde (Architectuur → TO → Implementatie → Validatie → Release), de vaststelling dat de fundamentele architectuur stabiel/bevroren is, en de regel dat het oorspronkelijke bronbestand altijd prevaleert — zonder enige nieuwe architectuur, contractwijziging of code.
