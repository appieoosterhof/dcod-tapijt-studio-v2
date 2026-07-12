# BUILD-024 — Contract Hardening DesignContext & Boundary-Contracten: technisch ontwerp

**Status:** technisch ontwerp / contractarchitectuur, ter TR. **Geen implementatie, geen code.** Legt de formele, stabiele contracten vast tussen **DesignContext → Orchestrator → Reasoning Boundaries**, zodat elke boundary uitsluitend een contract ontvangt/retourneert en geen kennis heeft van elkaars interne implementatie.

**Bindend / respecteert:** AB-006, AB-009, AB-012, BUILD-007, BUILD-023, IMP-014. **Geen wijziging** aan componentgrenzen, Design Brain, orchestratorlogica, reasoning-flow, caching/invalidatie, prompts of API-flow — dit document beschrijft uitsluitend de contractarchitectuur.

**Kernprincipe:** een boundary is een pure functie `Callable[[platte dict], platte dict | list | str]`. De **component** projecteert de invoer (`_verzamel_invoer`) en registreert het resultaat (herkomst/status); de **boundary** kent uitsluitend het contract. Zo blijft de boundary AI-model-onafhankelijk en volledig ontkoppeld.

---

## 1. Inputprojecties (per boundary)

Legenda: **V** verplicht (contractueel gegarandeerd aanwezig doordat de **gate** de bron borgt — geen crash-conditie: de deterministische placeholders verdragen afwezigheid via defaults, maar het contract garandeert de bron voor betekenisvolle redenering) · **O** optioneel (mag aanwezig zijn; uitbreidbaar; boundary behandelt afwezigheid gracieus) · **A** afgeleid (door de projectie/adapter berekend, als platte waarde aangeboden) · **U** uitgesloten (nooit aanwezig).

**Universeel uitgesloten (U) voor élke boundary:** het `DesignContext`-object, dataclass-instanties, herkomst-**identifiers**, de orchestrator/`Gesprekstoestand`/opslagstructuur, de API-request, en de **AI-sleutel/provider/model** (AB-012). Boundaries ontvangen uitsluitend platte waarden.

| Boundary | Signatuur | V (verplicht) | O (optioneel, uitbreidbaar) | A (afgeleid) |
|---|---|---|---|---|
| **Ontwerpstrategie** (BUILD-009) | `dict → dict` | `sfeer` óf `vrije_tekst`; `projecttype` óf `ruimtetype` | `gewenste_identiteit`, `ontwerpambitie`, `doelgroep`, `gebruikscontext` | — |
| **Concept** (RE Fase 1) | `dict → dict` | `sfeer`, `projecttype` óf `ruimtetype` | de huidige concept-velden `stijlfamilie`/`kleurpalet`/`complexiteit`/`motiefschaal` (bij eerste vorming leeg — het Concept wórdt hier geproduceerd), uitbreidbaar: `doelgroep`, `functionele_eisen`, `bijzondere_randvoorwaarden` | — |
| **Floor Design** (RE Fase 2, AB-009) | `dict → list` | `stijlfamilie`, `complexiteit` (uit bevestigd Concept) | `kleurpalet`, `motiefschaal`, `vrije_tekst`, `sfeer`, `gewenste_identiteit`, `ontwerpambitie`, `projecttype`, `ruimtetype`, `doelgroep`, `gebruikscontext`, `aanpak`, `onderbouwing` | — |
| **Material** (BUILD-012) | `dict → list` | `stijlfamilie`, `ontwerprichting` | `kleurpalet`, `complexiteit`, `motiefschaal`, (uitbreidbaar: `aanpak`/strategie-onderbouwing) | — |
| **Pattern** (BUILD-013) | `dict → list` | `stijlfamilie`, `ontwerprichting`, `structuur`, `pooltype` | `kleurpalet`, `complexiteit`, `motiefschaal`, `uitstraling` | — |
| **SVG-rendering** (AB-005/BUILD-018, deterministisch) | `dict → str` | `stijlfamilie`, `motiefstructuur`, `motiefschaal`, `kleurpalet` | `complexiteit`, `ontwerprichting`, `structuur`, `pooltype`, `uitstraling`, `dichtheid`, `herhalingskarakter` | genormaliseerd `kleurpalet`, `style`-sleutel, int-`motief_schaal` (BUILD-018-adapter) |
| **Visualisatie** (FVE, deterministisch) | `dict → dict` | `svg`, `achtergrond_url`, `polygon` (4 punten) | `ontwerprichting`, `uitstraling` | — |
| **Transfer** (DTP, deterministisch) | `dict → object` | de vijf bundel-snapshots (visie, floor design, material, svg, visualisatie) | — | — |

**Geen impliciete afhankelijkheden:** alles wat een boundary nodig heeft staat expliciet in het contract; er is geen verborgen toegang tot andere lagen.

## 2. Resultaatobjecten (per object)

Legenda velden: **V** verplicht · **O** optioneel · **S** status · **H** herkomst · **K** kwaliteitsinformatie (opaque).

| Object | V (verplicht) | O (optioneel) | S (status) | H (herkomst) |
|---|---|---|---|---|
| **Ontwerpstrategie** (laag 3) | `aanpak` | `onderbouwing` | `status` ∈ {"in ontwikkeling","vastgesteld"} | — (laag-3, in DesignContext) |
| **Concept** (laag 4) | `stijlfamilie`, `kleurpalet`, `complexiteit`, `motiefschaal` | — | `status` ∈ {"voorgesteld","bevestigd"} (kleine letter) | — (laag-4, in DesignContext) |
| **FloorDesign** | `identifier`, `ontwerprichting`, `motivering` | `kwaliteitsinformatie` | `status` ∈ {"Voorgesteld","Bevestigd"} (**hoofdletter, AB-006**) | `concept_herkomst` |
| **MaterialProfile** | `identifier`, `materiaalsoort`, `structuur`, `pooltype`, `motivering` | `tactiliteit`, `uitstraling`, `kwaliteitsinformatie` (uitbreidbaar: `glans`, `textuur`) | `status` ∈ {"Voorgesteld","Bevestigd"} | `concept_herkomst`, `floor_design_herkomst` |
| **PatternProfile** | `identifier`, `motiefstructuur`, `motiefschaal`, `motivering` | `dichtheid`, `herhalingskarakter`, `kwaliteitsinformatie` | `status` ∈ {"Voorgesteld","Bevestigd"} | `concept_/floor_design_/material_profile_herkomst` |
| **SVGResultaat** | `identifier`, `svg`, `weergave_motivering` | `kwaliteitsinformatie` | **geen** (deterministisch) | `concept_/floor_design_/material_profile_/pattern_profile_herkomst` |
| **Visualisatie** | `identifier`, `beeld`, `weergave_motivering` | `kwaliteitsinformatie` | **geen** | `svgresultaat_herkomst`, `scene_herkomst` |
| **DesignTransferPackage** | `identifier`, `inhoud`, `overdracht_representatie`, `overdracht_motivering`, `herkomst` | `kwaliteitsinformatie` | **geen** | `herkomst` (alle onderdelen + transitief) |

- **Versiegedrag:** uitsluitend **additief** — nieuwe velden zijn optioneel; verplichte velden, statusvocabulaires en herkomst-veldnamen worden nooit hernoemd of verwijderd. Een ontbrekend optioneel veld is een geldige, oudere versie.
- **Uitbreidbaarheid:** rijkere reasoning voegt uitsluitend **optionele** velden toe (bv. `glans`/`textuur` op MaterialProfile; extra patroonparameters) zonder de bestaande consumenten te breken.
- **Geen interpretatie door afnemers:** afnemers lezen uitsluitend de gecontracteerde velden; `motivering`/`weergave_motivering`/`onderbouwing` zijn vrije tekst (nooit geparsed voor logica), `kwaliteitsinformatie` is opaque, en de `svg`-/`beeld`-inhoud is een payload, geen beslisbron.

## 3. Contractstabiliteit

- **Stabiel (verandert nooit):** de boundary-signaturen; de **verplichte** invoer-sleutels en **verplichte** uitvoervelden; de herkomst-veldnamen; de statusvocabulaires (incl. het bewuste hoofd-/kleine-letterverschil, AB-006 vs laag-4); het besluit "geen eigen status" op SVGResultaat/Visualisatie/DTP.
- **Uitbreidbaar (additief):** optionele invoer-sleutels; optionele uitvoervelden; de inhoud van `kwaliteitsinformatie`.
- **Nooit door consumers geïnterpreteerd:** `kwaliteitsinformatie` (opaque diagnostiek), alle vrije-tekst-motiveringen, en de interne structuur van `svg`/`beeld` — consumenten behandelen deze als ondoorzichtige payload en vertakken er nooit op.

## 4. Validatieregels

- **Minimale contractvalidatie:** de **component** valideert de boundary-**uitvoer** op de verplichte velden (bestaande checks: `_valideer_voorstel`/`_valideer_svg`/`_valideer_compositie`/`_valideer_representatie`). De **gate** (BUILD-008) borgt de verplichte **invoer**-bron. Geen nieuwe validatie in de boundary zelf.
- **Ontbrekende invoer:** een afwezig **optioneel** veld is geldig (boundary werkt gracieus verder); een afwezig **verplicht** veld wordt door de gate voorkomen (upstream niet bevestigd → geen aanroep).
- **Ongeldige invoer/uitvoer:** een onvolledig of type-onjuist boundary-resultaat wordt door de output-validatie afgewezen → signalering, geen registratie (bestaand gedrag).
- **Versieconflicten:** door de additieve regel bestaan er geen brekende versieconflicten — een nieuwe consumer verdraagt afwezige optionele velden; een oude consumer negeert nieuwe optionele velden. Verwijderen/hernoemen is verboden.

## 5. Boundary-onafhankelijkheid

Elke reasoning-boundary is aantoonbaar afhankelijk van **uitsluitend het contract** (een platte dict) en **niet** van:
- **DesignContext** — de boundary ontvangt platte waarden, geen `DesignContext`-object of laag-dataclass;
- **Orchestrator** — de boundary kent geen guards, cache, `Gesprekstoestand` of gesprek_id;
- **Opslagstructuur** — de boundary leest/schrijft niets; registratie (herkomst/status/serialisatie) doet de component/integratielaag;
- **API-implementatie** — de boundary kent geen endpoints, request/response of AI-sleutel (AB-012).

Dit is reeds zo in de code gestructureerd (`RedeneerFunctie`/`*RedeneerFunctie`/`SVGRenderFunctie`/`VisualisatieBoundary`/`TransferFunctie` = `Callable[[dict], …]`, met deterministische placeholders); BUILD-024 legt dit vast als **bindend contract**, zodat een toekomstige productie-boundary uitsluitend het contract implementeert.

---

## Consistentietoets

- **AB-006:** het FloorDesign/MaterialProfile/PatternProfile-statusvocabulaire (`"Voorgesteld"`/`"Bevestigd"`, hoofdletter) staat als **stabiel** vastgelegd (§2/§3).
- **AB-009:** de Floor Design-generatie is als **Fase 2-boundary binnen de Reasoning Engine** gecontracteerd (§1), geen aparte component.
- **AB-012:** de AI-sleutel/provider/model staat als **universeel uitgesloten invoer** in élk contract (§1).
- **BUILD-007 / BUILD-023 / IMP-014:** ketenvolgorde, gates, orchestratorlogica, caching en invalidatie blijven ongewijzigd; dit document raakt uitsluitend de contractdefinitie.
- **Backward compatibility:** de additief-only versieregel (§2/§4) borgt dat bestaande consumenten en toekomstige rijkere boundaries elkaar niet breken.

---

**Reviewgereed:** dit TD legt de formele, stabiele en additief-uitbreidbare contracten vast tussen DesignContext, orchestrator en reasoning-boundaries — inputprojecties (verplicht/optioneel/afgeleid/uitgesloten), resultaatobjecten (velden/status/herkomst/versie/uitbreidbaarheid), contractstabiliteit, validatieregels en boundary-onafhankelijkheid — zonder wijziging aan de orchestrator, caching, invalidatie, reasoning, prompts, API-flow of BUILD-007. Hierna is de architectuur contractvast en kan de eerste productie-reasoning-boundary zonder aanvullende architectuurwijziging worden aangesloten.
