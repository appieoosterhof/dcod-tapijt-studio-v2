# BUILD-019 — Integratie Design Brain in de bestaande Flask-app: technisch ontwerp (TD-008)

> **Geamendeerd door BUILD-020** (`BUILD-020_TD-008_AMENDEMENT_LAAG2_ONTWERPSTRATEGIE.md`): de orkestratie-keten (§2) en de importlijst (Besluit B) worden aangevuld met de **laag-2-projectie** (Context Interpreter) en de **Ontwerpstrategie-stap** (BUILD-009) vóór het Concept. Zie BUILD-020 voor de geamendeerde keten; de rest van dit document blijft gelden.

**Status:** technisch ontwerp, ter review. Geen programmacode. Beschrijft uitsluitend **hoe** de integratie wordt gerealiseerd; het **wat** ligt vast in BUILD-019 en mag niet wijzigen. Geen nieuwe architectuurcomponent — een dunne, additieve ontsluitingslaag die de bestaande Design Brain-componenten aanstuurt.

**Normatief:** BUILD-019 (functioneel), BUILD-007 (workflow), BUILD-017 (Conversation Planner), BUILD-018 (SVG Planner ↔ pipeline, met de lui-import van `build_tile_svg`), AB-005/AR-004/AR-005, en het bestaande `app.py`/`scene_builder.py`/`design_context.py`.

**Architectuurprincipe (technisch geborgd):** de integratielaag is **uitsluitend ontsluitend/orkestrerend** en **stateless per request**: elk verzoek laadt de gesprekstoestand op grond van een `gesprek_id`, roept precies één bestaande component aan, en slaat de toestand terug op. Geen mutabele globals, geen gedeelde toestand tussen gesprekken, geen ontwerplogica of duplicatie. Volledig additief: de enige aanraking van `app.py` is één additieve registratieregel (§Besluit B); geen bestaande route, flow of pipeline wordt gewijzigd.

---

## Besluit A — sessie-/toestandsbeheer

**Besluit:** de gesprekstoestand wordt bewaard in een **id-gesleutelde, persistente store** die het bestaande Scene Builder-patroon spiegelt (BUILD-006: één entiteit = één JSON onder een map, gesleuteld op id). Per gesprek is er één `gesprek_id` (server-gegenereerde UUID, teruggegeven bij het starten van een gesprek) dat een geserialiseerde **`Gesprekstoestand`** sleutelt (§3). Elke request verloopt **laden → één component aanroepen → opslaan** (atomair).

**Onderbouwing tegen de gestelde eisen:**
- **Geen toestand in de Design Brain:** de componenten blijven puur — zij ontvangen en retourneren objecten; de `DesignContext` en de ketenartefacten worden buiten de componenten, in de integratielaag, bewaard.
- **Geen nieuwe architectuur:** het hergebruikt het bestaande, bewezen persistentie*patroon* van de Scene Builder (JSON per entiteit, gesleuteld op id); geen nieuw infrastructuurtype, geen Flask-session (die de app niet kent), geen database.
- **Niet web-benaderbaar (privacy):** anders dan de Scene Builder — die bewust onder `static/` staat omdat de achtergrondafbeeldingen door Flask geserveerd moeten worden — wordt de `Gesprekstoestand` in een **niet-geserveerde** map bewaard (buiten `static/`). De gesprekstoestand bevat de vrije-tekst-briefing van de gebruiker en is geen publiek asset; zij mag niet via een URL opvraagbaar zijn.
- **Geen mutabele globals:** de toestand leeft niet in een module-level dict maar in de per-`gesprek_id` store; er wordt niets in `globals()` gezet (anders dan de bestaande, ongemoeide `/api/generate`).
- **Geen gedeelde DesignContext tussen gesprekken:** elk `gesprek_id` heeft zijn eigen store-entry; er is geen enkel gedeeld `DesignContext`-object.
- **Stateless Flask blijft uitgangspunt:** er is geen proces-interne sessie; elke request reconstrueert de toestand uit de store en schrijft haar terug — precies zoals `/api/scenes` doet.
- **Oplossing uitsluitend in de integratielaag:** de store en de laad/opslag-logica horen bij de integratielaag; `design_context.py` en de keten-modules worden niet aangeraakt.

## Besluit B — importstructuur

**Besluit:** de integratielaag is **één nieuw bestand** (bijv. `design_brain_api.py`) met een **Flask Blueprint**. Dat bestand importeert de keten-modules op moduleniveau (`conversation_planner`, `context_interpreter`, `reasoning_engine`, `material_planner`, `pattern_planner`, `svg_planner`, `svg_planner_pipeline`, `floor_visualization_engine`, `design_transfer_package`, `scene_builder`, `design_context`). `app.py` krijgt **één additieve regel**: het registreren van de Blueprint (`app.register_blueprint(...)`).

**Waarom dit architectonisch correct is (geen cyclus, geen module-load-probleem):**
- De afhankelijkheidsrichting is **eenzijdig neerwaarts**: `app.py → design_brain_api → keten-modules → design_context/scene_builder`. Geen enkele keten-module importeert `app` op moduleniveau (geverifieerd in de eindvalidatie: cyclusvrije DAG).
- De **BUILD-018 lui-import** blijft leidend: `svg_planner_pipeline` importeert `build_tile_svg` **binnen** de boundary-functie, niet op moduleniveau. Op het moment dat die import draait (request-tijd) is `app` volledig geladen. Zo ontstaat er ook met de nieuwe integratielaag **geen** import-cyclus bij module-load.
- Omdat de integratie een **Blueprint** is (het idiomatische, additieve Flask-uitbreidingspunt), blijven alle bestaande routes en de pipeline byte-voor-byte ongewijzigd; de enige toevoeging aan `app.py` is de registratieregel.

## Besluit C — concurrency

**Besluit:** volledige isolatie via het per-`gesprek_id`-gesleutelde store-model, aangevuld met **atomaire schrijfacties** (schrijf naar tijdelijk bestand + `os.replace`) en een **per-`gesprek_id`-slot** rond de kritieke sectie *laden → muteren → opslaan*.

**Expliciete controle:**
- **Geen gedeelde DesignContext:** elk gesprek heeft een eigen store-entry; twee gesprekken raken elkaars `DesignContext` nooit.
- **Geen gedeelde state:** er zijn geen module-globals die gesprekstoestand dragen.
- **Geen race conditions / geen corruptie:** de **harde garantie** berust op de **atomaire, id-gesleutelde schrijf** (`os.replace`): geen half-geschreven toestand en absolute isolatie tussen gesprekken. Het per-id-slot is een **in-process** best-effort-optimalisatie die binnen één proces twee snel opeenvolgende beurten serialiseert; onder een **multi-process** WSGI-server (meerdere workers) serialiseert het niet tussen processen. Dat is acceptabel omdat de beurten binnen één gesprek in de praktijk sequentieel zijn (lost-updates onwaarschijnlijk); zou strikte per-gesprek-serialisatie over processen heen ooit nodig zijn, dan is file-locking de weg — geen architectuurwijziging.
- **Geen invloed op `/api/generate`:** die flow deelt niets met de store (eigen request-scoped lichtgewicht-`DesignContext` + de bestaande `_ETALAGE_DIRECT_PAL`-global), en wordt niet aangeraakt.
- **Geen invloed op de live Dessinator:** de integratie is additief; de bestaande routes/pipeline draaien onveranderd.

---

## 1. Architectuur

- **Eén nieuw bestand met een Flask Blueprint** (`design_brain_api.py`) + een kleine **`Gesprekstoestand`-store** (mag in hetzelfde bestand of een submodule, maar hoort bij de integratielaag).
- **Interne grenzen:**
  - **Ontsluiting (Blueprint-endpoints)** — ontvangt requests, valideert het `gesprek_id`/de payload, roept één component aan, serialiseert het resultaat.
  - **Toestand-store** — laden/opslaan van de `Gesprekstoestand` per `gesprek_id` (Scene Builder-patroon, atomair, per-id-slot).
  - **Component-injectie** — o.a. de Conversation Planner met een via `api_key` bedrade Context Interpreter (BUILD-017-boundary) en de SVG Planner via `maak_svg_planner()` (BUILD-018-adapter).
- **Uitsluitend orkestrerend:** de laag beslist/interpreteert/bevestigt niets; alle logica blijft in de componenten.
- **Additief:** geen wijziging aan bestaande routes, flows of de pipeline; enige aanraking = de Blueprint-registratie.

## 2. Verwerkingsketen

Elke endpoint volgt hetzelfde patroon: **`gesprek_id` → toestand laden → één component aanroepen → toestand opslaan → JSON terug**. De keten (conform BUILD-007) verloopt over meerdere requests:
1. **Gesprek starten** → nieuwe `gesprek_id` + lege `Gesprekstoestand`.
2. **Dialoog-beurt** → Conversation Planner bouwt laag 1 (schrijft uitsluitend de onbevestigde visie); retourneert de vervolgstap.
3. **Visie bevestigen** → een expliciete architect-actie zet `bevestigd_door_architect = True` (de laag zet dit nooit zelf).
4. **Concept vormen / Floor Designs genereren** → Reasoning Engine (Fase 1/2) op de bevestigde visie.
5. **Floor Design bevestigen** → architect-actie zet de status van het gekozen artefact op "Bevestigd".
6. **Material Profile → Pattern Profile → SVGResultaat → Visualisatie → Design Transfer Package** → de respectieve componenten, elk op bevestigde upstream-inhoud; de Scene komt uit de Scene Builder.
- **Gate-borging:** de volgorde wordt **niet** door de integratielaag afgedwongen maar door de **bestaande gates** van de componenten (een stap faalt met een signalering als de upstream niet bevestigd is). De integratielaag geeft die signalering door als foutrespons.
- **Foutafhandeling:** een component-signalering → nette JSON-foutrespons; de opgeslagen toestand wordt **alleen bij succes** (atomair) bijgewerkt, zodat een mislukte beurt de toestand niet corrumpeert.

## 3. Gegevensmodellen (technische representatie)

- **`Gesprekstoestand`** — een container in de integratielaag, geserialiseerd als JSON, gesleuteld op `gesprek_id`. Bevat: de geserialiseerde `DesignContext` (`to_dict`/`from_dict`, reeds round-trip-veilig) en de reeds geproduceerde **ketenartefacten** (voorgestelde/bevestigde Floor Design(s), Material Profile, Pattern Profile, `SVGResultaat`, Visualisatie, Design Transfer Package) — elk een bestaand dataclass. Zij hebben, anders dan `DesignContext`/`Scene`, geen eigen `to_dict`; serialisatie verloopt via `dataclasses.asdict` en reconstructie via `Cls(**data)` (de velden zijn platte waarden/dicts, dus round-trip-veilig). **Geen nieuw domeinobject**: het is een verzameling van reeds bestaande objecten + het `gesprek_id`.
- **Geen eigen status op de container;** de statussen leven op de bestaande objecten (visie-vlag, Concept/Floor Design/Material/Pattern "status").
- De **architect-bevestiging** is een veldmutatie op het betreffende bestaande object (de vlag of de status), uitgevoerd namens de expliciete architect-actie — nooit door een component zelf.

## 4. Validatie

- **`gesprek_id`-validatie:** onbekend/ontbrekend id → nette foutrespons; geen impliciete aanmaak buiten de start-endpoint.
- **Gate-respect:** de integratielaag omzeilt geen enkele gate; zij roept de component aan en laat diens preconditie beslissen. Bevestig-acties zetten uitsluitend de vlag/status en **slaan geen stap over**.
- **Read-only grenzen:** de integratielaag schrijft zelf niets ín de `DesignContext` behalve via de componenten; laag 1 wordt uitsluitend door de Conversation Planner geschreven en is read-only na bevestiging (BUILD-017).
- **Payload-validatie:** ontbrekende `api_key` (voor de Context Interpreter) of Scene-referentie (voor de FVE) → nette foutrespons, geen crash.

## 5. Herstel / regeneratie

- **Component-niveau:** de bestaande gelimiteerde regeneratie (`MAX_*_POGINGEN`) blijft binnen elke component gelden.
- **Integratie-niveau:** een mislukte/afgebroken request laat de laatst opgeslagen `Gesprekstoestand` **intact** (atomaire schrijf; opslaan alleen bij succes). De gebruiker kan de beurt opnieuw doen.
- **Deterministische herhaling:** op de BUILD-018-basislijn levert het opnieuw uitvoeren van een stap met dezelfde bevestigde inputs hetzelfde resultaat.

## 6. Interfaces

- **Nieuwe Blueprint-endpoints** (additief, eigen pad-prefix, buiten `/api/generate`): gesprek starten, dialoog-beurt, visie/artefact bevestigen, ketenstappen uitvoeren, resultaat/DTP ophalen.
- **Integratie → Conversation Planner:** injecteert de Context Interpreter met de `api_key` (BUILD-017-boundary).
- **Integratie → SVG Planner:** via `maak_svg_planner()` (BUILD-018-adapter); rendering loopt door de bestaande `build_tile_svg`-pipeline (lui geïmporteerd).
- **Integratie → Scene Builder:** haalt de `Scene` op via de bestaande `scene_builder`-API (read-only).
- **Integratie → FVE/DTP:** produceert Visualisatie resp. Design Transfer Package.
- **Bestaande routes** (`/api/generate`, `/api/refine`, `/api/export/*`, `/api/scenes`, `/api/bestelling`): **ongewijzigd**; de enige toevoeging aan `app.py` is `app.register_blueprint(...)`.

## 7. Traceerbaarheid

- Het **`gesprek_id`** correleert alle beurten en artefacten van één gesprek.
- Binnen de `DesignContext` blijft `interpretaties` het herkomst-record (BUILD-004/017); de ketenartefacten dragen hun bestaande herkomst-referenties (Concept → … → DTP). De integratielaag voegt **geen** eigen traceerbaarheid toe buiten de correlatie op `gesprek_id`.
- Er wordt **niets buiten de bestaande objecten** geregistreerd (de store bewaart uitsluitend geserialiseerde bestaande objecten).

## 8. Robuustheid

- **Isolatie & concurrency:** per-`gesprek_id`-store + atomaire schrijf + per-id-slot (Besluit C).
- **Additief / regressievrij:** geen bestaande route/flow/pipeline gewijzigd; `app.py` uitsluitend uitgebreid met de Blueprint-registratie. `/api/generate` en de live Dessinator draaien onveranderd.
- **Foutgrens:** elke endpoint vangt component-signaleringen en onverwachte fouten af als nette JSON-respons; nooit een half-geschreven toestand.
- **Geen cyclus / geen module-load-probleem:** eenzijdige import-richting + de BUILD-018 lui-import (Besluit B).
- **AI-model:** het model zit uitsluitend achter de Context Interpreter-boundary (via `api_key` geïnjecteerd); de integratielaag zelf bevat geen model/prompt.

## 9. Technische besluiten (samenvatting)

- **A — Sessie/toestand:** id-gesleutelde, persistente `Gesprekstoestand`-store naar Scene Builder-patroon; laden-muteren-opslaan per request; stateless Flask behouden; geen globals; toestand uitsluitend in de integratielaag.
- **B — Imports:** nieuw Blueprint-bestand `design_brain_api.py`; eenzijdige neerwaartse import-richting; BUILD-018 lui-import blijft leidend; `app.py` krijgt uitsluitend `app.register_blueprint(...)`.
- **C — Concurrency:** per-`gesprek_id`-isolatie + atomaire schrijf + per-id-slot; geen gedeelde state, geen races, geen invloed op `/api/generate` of de live Dessinator.
- **Additiviteit:** de pipeline (`build_tile_svg`/`build_repeat_svg`/generatoren) en alle bestaande routes blijven ongewijzigd; geen nieuw domeinobject; geen nieuwe verantwoordelijkheid.

---

**Acceptatie:** met een `gesprek_id` laadt elke endpoint de `Gesprekstoestand`, roept exact één bestaande Design Brain-component aan (met de Context Interpreter/SVG-adapter/Scene correct geïnjecteerd), respecteert alle bestaande gates en read-only grenzen, en slaat de toestand atomair en per-id-geïsoleerd terug — zonder mutabele globals, zonder gedeelde toestand tussen gesprekken, zonder import-cyclus, en zonder enige wijziging aan `/api/generate`, de bestaande routes of de productiepipeline (afgezien van de additieve Blueprint-registratie).
