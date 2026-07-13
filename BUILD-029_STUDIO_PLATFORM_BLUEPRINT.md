# BUILD-029 — Studio Platform Blueprint

**Status:** overkoepelend architectuuroverzicht / hoofdkaart. **Geen nieuwe architectuur, geen implementatie, geen contractwijziging, geen code.** Brengt uitsluitend de reeds goedgekeurde architectuurdocumenten samen tot één samenhangend beeld van het volledige Studio Platform. Bij enig verschil prevaleert steeds het onderliggende, specifieke document.

**Samengebracht (bindend):** AB-006, AB-009, AB-012, BUILD-004, BUILD-007, BUILD-008, BUILD-017, BUILD-018, BUILD-019, BUILD-023, IMP-014, BUILD-024, IMP-015 t/m IMP-019, PLATFORM-001, PLATFORM-002, REASONING-001, SEC-001, LEGAL-001 (vertrouwelijk, buiten repo), BUILD-025 (+025-A)/026/027/028.

---

## 1. Compleet Studio-overzicht (lagen)

```
┌───────────────────────────────────────────────────────────────────────────┐
│  EXPERIENCE LAYER   (merk · kanaal · modaliteit · UX · gesprek)             │
│   Studio UX (BUILD-028) · Conversation Experience/Voice (BUILD-025/025-A)   │
│   Conversation State (BUILD-026) · Multimodal adapters (BUILD-027)          │
│   belevingslaag /ontwerp (BUILD-021/022, IMP-013) · Design Dialogue (PF-002)│
└───────────────▲───────────────────────────────────────────────────────────┘
                │  platte tekst / platte parameters (nooit audio/beeld ruw)
┌───────────────┴───────────────────────────────────────────────────────────┐
│  API / INTEGRATIE LAYER   (design_brain_api.py)                             │
│   endpoints /api/design-brain · Gesprekstoestand-cache (BUILD-019)          │
│   orchestratie-guards R1–R6 (BUILD-023/IMP-014) · AI-sleutel server-side    │
│   (AB-012) · gates/bevestiging (BUILD-008/AB-006)                           │
└───────────────▲───────────────────────────────────────────────────────────┘
                │  gecontracteerde platte dicts (BUILD-024)
┌───────────────┴───────────────────────────────────────────────────────────┐
│  DESIGN BRAIN   (domein · redeneert · ongewijzigd)                          │
│   Conversation Planner (BUILD-017) · Context Interpreter (BUILD-004)        │
│   DesignContext-model (6 lagen + redenering + interpretaties)               │
│   Reasoning Capabilities → zie §6                                           │
└───────────────▲───────────────────────────────────────────────────────────┘
                │  bevestigde resultaat-objecten (buiten DesignContext)
┌───────────────┴───────────────────────────────────────────────────────────┐
│  PRODUCTIE / DOWNSTREAM   (deterministisch)                                 │
│   SVG Planner-pipeline (AB-005/BUILD-018) · Floor Visualization Engine      │
│   Design Transfer Package                                                   │
└───────────────────────────────────────────────────────────────────────────┘
   Dwars over alles:  Governance & Security (SEC-001/LEGAL-001) · Platformvisie
   (PLATFORM-001) · Ontwerpfilosofie (REASONING-001) · Contracten (BUILD-024)
```

## 2. Design Brain

De domeinkern die **ontwerpbeslissingen** neemt en nergens anders van weet. Bevat het **DesignContext-model** (OntwerpVisie → ProjectContext → OntwerpStrategie → Concept → Materialisatie → ProductieRealisatie, + Ontwerpredenering + interpretaties) en de redeneercomponenten. Redeneert uitsluitend via **injecteerbare boundaries** (platte dict in, platte dict/lijst uit) en is model-, HTTP-, opslag- en orchestratie-blind (BUILD-024 §5). Bindend: BUILD-007 (ketenvolgorde), AB-009 (Floor Design = Fase 2 in de Reasoning Engine).

## 3. Studio Experience

De **beleving** bovenop de Design Brain: de Dessinator als ontwerpcollega (BUILD-028), een canonieke 8-fasen gespreksstroom (BUILD-025-A), een afgeleide gesprekstoestand (BUILD-026) en modaliteit-adapters (BUILD-027), voortbouwend op de belevingslaag (BUILD-021/022, IMP-013) en de Design Dialogue-visie (PLATFORM-002). Toont nooit techniek/model/fout (AB-012).

## 4. Experience Layer

De uitwisselbare **presentatie-/ervaringslaag** (PLATFORM-001 §2): branding, terminologie, rechten, navigatie, gebruikersreis, modaliteit. Bevat geen ontwerp- of AI-logica. Meerdere instanties naast elkaar: Professional/Consumer/Dealer/White-label; merken DCOD, Dutch Carpets, e.a. Het huidige `/ontwerp`-atelier is de eerste instantie.

## 5. API Layer

De **integratielaag** (`design_brain_api.py`): de HTTP-endpoints, de persistente `Gesprekstoestand` (per `gesprek_id`, BUILD-019), de orkestratie-guards (BUILD-023/IMP-014: hergebruik + gerichte invalidatie via herkomst/`is_stale`), de gates/bevestiging (BUILD-008/AB-006) en het **server-side sleutelbeheer** (AB-012). De Experience Layer praat uitsluitend met deze laag; de Design Brain wordt hier aangeroepen óf overgeslagen, nooit gewijzigd.

## 6. Reasoning Capabilities

Vijf productie-capabilities achter de bestaande boundaries, elk via de gedeelde `reasoning_client.py` (vendor-agnostische `ModelClient`-poort + Anthropic-adapter + config-factory `DCOD_REASONING_MODUS` + gecontroleerde placeholder-fallback):

| # | Capability | Boundary-contract | Doc |
|---|---|---|---|
| 1 | Ontwerpstrategie | `dict → {aanpak, onderbouwing}` | IMP-015 (VAL-001) |
| 2 | Conceptvorming | `dict → {stijlfamilie, kleurpalet, complexiteit, motiefschaal}` | IMP-016 (VAL-002) |
| 3 | Floor Design | `dict → list[{ontwerprichting, motivering}]` | IMP-017 (VAL-003) |
| 4 | Material Planning | `dict → list[{materiaalsoort, structuur, pooltype, motivering}]` | IMP-018 (VAL-004) |
| 5 | Pattern Planning | `dict → list[{motiefstructuur, motiefschaal, motivering}]` | IMP-019 (VAL-005) |

Alle vijf redeneren op REASONING-001, produceren voorstellen (nooit bevestigingen), en vallen bij elke fout gecontroleerd terug op hun deterministische placeholder. Productie staat pas "aan" met `DCOD_REASONING_MODUS=productie` + serversleutel; anders draait alles op placeholders.

## 7. Workflow

De vaste ketenvolgorde (BUILD-007), met een expliciet bevestigingsmoment per stap (AB-006/BUILD-008):

```
Gesprek → visie (bevestig) → Ontwerpstrategie (vaststel) → Concept (bevestig)
       → Floor Design (bevestig) → Material (bevestig) → Pattern (bevestig)
       → SVG → Visualisatie → Design Transfer Package
```

Reasoning draait uitsluitend bij **nieuwe ontwerpwaarde** (AP-001/BUILD-023); gewijzigde bevestigde upstream invalideert gericht downstream (R4).

## 8. Governance

Repository-governance, releasebeleid (push uitsluitend op expliciete autorisatie; `main` = live via Render, `preview` = integratie), VR/TR/CR-werkwijze, en de projectroadmap (PLATFORM-001/002). Auteurschap/IP: SEC-001 §2 (openbaar, zonder persoonsgegevens) + LEGAL-001 (vertrouwelijk, buiten de repo).

## 9. Security

Security by architecture (SEC-001): server-side reasoning en geheimen (AB-012), capability-/boundary-isolatie, contractgebaseerde communicatie, provider-onafhankelijkheid, onzichtbare degradatie. Geheimenbeheer, kennisbescherming, continuïteit/bus-factor en een releasegefaseerde beveiligingsroadmap. Gevoelige toekomstige data (spraak/beeld) valt onder hetzelfde beleid; provider-/privacykeuzes zijn expliciete IMP-beslissingen.

## 10. Uitbreidbaarheid

Additief op elk niveau, zonder wijziging aan de Design Brain: nieuwe **Reasoning Capabilities** (zelfde patroon/infra), nieuwe **modaliteiten** (adapter → platte contract-invoer, BUILD-027), nieuwe **Experience Layers**/merken/kanalen (PLATFORM-001), nieuwe **AI-modellen** (nieuwe `ModelClient`-adapter, BUILD-024 §5). Contracten zijn **additief-only**: nooit hernoemen/verwijderen, uitbreiden mag.

## 11. Permanente architectuur (bindend, verandert niet)

- de ketenvolgorde en bevestigingsmomenten (BUILD-007, BUILD-008/AB-006);
- de boundary-contracten en hun additief-only regel (BUILD-024);
- de orkestratie-/reuse-/invalidatieregels (BUILD-023/IMP-014, AP-001);
- de scheidingen: **Voice≠Reasoning · Conversation≠Workflow · Experience≠Design Brain · Modaliteit≠Contract**;
- verborgen AI-infrastructuur (AB-012); Floor Design als Fase 2 (AB-009); statusvocabulaire (AB-006);
- de ontwerpfilosofie (REASONING-001) als bron van waarheid voor reasoning;
- het DesignContext-model en de componentgrenzen.

## 12. Variabele onderdelen (uitwisselbaar/additief)

- de **AI-provider/het model** (of regelsysteem/hybride) achter elke boundary;
- de **capability-implementatie** (placeholder ↔ productie; per-capability config zoals `max_tokens`);
- de **Experience Layer** (branding, terminologie, navigatie, rechten) en het **merk/kanaal**;
- de **modaliteit-adapters** (STT/TTS/beeld/scan) en hun providers;
- deployment-/configuratieparameters (`DCOD_REASONING_MODUS`, sleutelbron).

---

## Consistentietoets

- **Uitsluitend synthese:** elk onderdeel verwijst naar een bestaand, goedgekeurd document; er wordt geen nieuwe architectuur, geen contract en geen code geïntroduceerd.
- **Grenzen intact:** de blueprint bevestigt (en overschrijdt nooit) de vastgelegde scheidingen tussen Experience Layer, API Layer, Design Brain en productie.
- **Permanente vs variabele onderdelen:** de indeling (§11/§12) volgt exact BUILD-024 (additief-only), BUILD-023 (orkestratie), PLATFORM-001/002 (Experience Layer) en AB-012 (verborgen AI); niets erin wijzigt een besluit.
- **Prevalentie:** bij enig verschil tussen deze hoofdkaart en een specifiek document, prevaleert het specifieke document.

---

**Reviewgereed:** dit blueprint brengt het volledige Studio Platform samen als één hoofdkaart — de lagen (Experience → API → Design Brain → productie), de vijf Reasoning Capabilities, de workflow, de governance en security, de uitbreidbaarheid, en het onderscheid tussen permanente (bindende) en variabele (uitwisselbare) onderdelen — uitsluitend als synthese van reeds goedgekeurde architectuur, zonder enige nieuwe architectuur, contractwijziging of code.
