# BUILD-017 — Conversation Planner: technisch ontwerp (TD-007)

**Status:** technisch ontwerp, ter review. Geen programmacode. Beschrijft uitsluitend **hoe** de Conversation Planner wordt gerealiseerd; het **wat** ligt vast in BUILD-017 en mag niet wijzigen. Geen nieuwe architectuurcomponent — de Conversation Planner is de reeds vastgestelde conversationele voorkant (BUILD-005/BUILD-017) en hergebruikt de bestaande Context Interpreter (BUILD-004) ongewijzigd.

**Normatief:** BUILD-004 (leidend voor interpretatie), BUILD-008 (laag-eigenaarschap), BUILD-009 en BUILD-010 (downstream-precondities), BUILD-017 (functioneel), en het bestaande datamodel `design_context.py`.

**Architectuurprincipe (technisch geborgd):** de Conversation Planner is een **orchestrerende, uitsluitend op laag 1 schrijvende** component. Hij **interpreteert niet zelf** (dat delegeert hij volledig aan de Context Interpreter) en **bevestigt nooit** (dat is exclusief de architect). Zijn eigen beslislogica — welke vervolgstap — is **deterministisch** gegeven de DesignContext-stand; de interpretatie zelf loopt via de bestaande, injecteerbare Context Interpreter-grens (waarachter het AI-model zit). Volledig additief: geen wijziging aan `design_context.py`, `context_interpreter.py` of de bestaande pipeline.

---

## Beslechting van het VR-029-punt (harmonisatie interpretaties ↔ laag 1-velden)

Het bestaande datamodel verankert de scheiding al (`design_context.py`, docstring `interpretaties`: *"het record van de interpretaties zelf; de resulterende waarden worden daarnaast in de betreffende velden … gezet"*). TD-007 beslecht wie wat aanstuurt:

- **Besluit A — twee rollen, één bron van waarheid.** `DesignContext.interpretaties` is het **append-only record** van voorstellen (`Interpretatie(laag, veld, waarde, zekerheid)`) — de volledige herkomst. De **laag 1-velden** (`OntwerpVisie.sfeer/gewenste_identiteit/ontwerpambitie/…`) zijn de **projectie** van dat record naar de huidige voorlopige visie. De velden dragen zelf **geen zekerheid** (die blijft op de `Interpretatie`).
- **Besluit B — de Conversation Planner voert géén interpretatie uit.** Interpreteren = het afleiden van een `Interpretatie` uit vrije tekst; dat is en blijft exclusief de Context Interpreter (`interpreteer_context`). De Conversation Planner **projecteert** uitsluitend reeds geïnterpreteerde waarden in de velden (een verbatim waarde-kopie, geen betekenisafleiding), via de bestaande functie `pas_interpretaties_toe` — die hij aanroept met **uitsluitend de `laag == "ontwerpvisie"`-interpretaties**, zodat hij alleen laag 1 schrijft. `pas_interpretaties_toe` wordt hiervoor **niet gewijzigd** (de functie itereert de meegegeven lijst).
- **Besluit B-bis — de ruwe wens (`vrije_tekst`).** `pas_interpretaties_toe` mapt `vrije_tekst` niet (dat is geen geïnterpreteerd veld maar de oorspronkelijke verwoording). De Conversation Planner schrijft `OntwerpVisie.vrije_tekst` daarom **rechtstreeks en verbatim uit de ruwe gebruikersinvoer** — een laag-1-schrijfactie, géén interpretatie, en net als alle laag-1-schrijfacties gegate't op `not bevestigd_door_architect`. Zo bestaat er altijd een schrijver van `vrije_tekst`, wat nodig is voor de model-invariant "een bevestigde visie mag niet leeg zijn" (`design_context.valideer()`: `vrije_tekst or voorgestelde_interpretatie`).
- **Besluit C — laag 2 en de reikwijdte van de record-schrijfactie.** De Conversation Planner geeft **uitsluitend** de laag-1-interpretaties aan de projectie mee; hij schrijft daardoor noch een laag-2-**veld** noch een laag-2-**record**. De projectcontext-interpretaties (laag 2) die dezelfde interpretatie-aanroep oplevert, zijn niet zijn verantwoordelijkheid; die horen bij de bestaande context-/inspiratieflow (BUILD-008: laag 2 zijn architect-feiten die DCOD structureert). "Schrijft uitsluitend laag 1" omvat dus de laag-1-**velden** plus hun **herkomst-record** (de laag-1-interpretaties in `dc.interpretaties`). Consistent met BUILD-017 §8.

---

## 1. Architectuur

- **Eén module, één publieke component** (bijv. `conversation_planner.py` / `ConversationPlanner`), naast de bestaande bestanden — niet erin.
- **Interne modulegrenzen** (drie):
  - **Orkestratie** — stuurt per gespreksbeurt de keten aan (interpretatie → projectie → vervolgstapkeuze) en geeft het resultaat terug.
  - **Interpretatie-grens (injecteerbaar)** — de aanroep van de Context Interpreter (`interpreteer_context`), waarachter het AI-model zit. De Conversation Planner kent de interne werking niet en bevat geen interpretatielogica; voor test kan een deterministische interpretatie-functie worden geïnjecteerd.
  - **Beslislogica (deterministisch)** — de vaste beslisvolgorde uit BUILD-005 (context voldoende? → bevestiging nodig? ) die exact één vervolgstap kiest; dezelfde stand levert dezelfde keuze (geen willekeur).
- **Schrijfbevoegdheid:** uitsluitend de **onbevestigde** `OntwerpVisie` (laag 1). Alle overige lagen en de `interpretaties`-lijst-als-record worden geschreven door de bestaande projectie (`pas_interpretaties_toe`), die de Conversation Planner met een laag-1-gefilterde lijst aanroept; hij schrijft nooit een andere laag en zet nooit `bevestigd_door_architect`.
- **Afhankelijkheden (read-only, m.u.v. onbevestigde laag 1):** de `DesignContext` (stand + `interpretaties`), gebruikersinvoer, gespreksgeschiedenis en projectfase (contextbronnen buiten het model, BUILD-005).

## 2. Verwerkingsketen

Per gespreksbeurt:
- **Invoer:** de huidige `DesignContext`, de gebruikersinvoer (vrije tekst), gespreksgeschiedenis en projectfase.
- **Verwerking:**
  1. **Write-gate:** is `dc.ontwerpvisie.bevestigd_door_architect` waar? Dan is laag 1 **read-only** — geen enkele projectie/schrijfactie; de component levert enkel nog de bevestigde visie op (zie §4).
  2. **Ruwe wens vastleggen:** de Conversation Planner schrijft de ruwe gebruikersinvoer verbatim naar `OntwerpVisie.vrije_tekst` (laag-1-schrijfactie, geen interpretatie).
  3. **Interpretatie (gedelegeerd):** bij nieuwe vrije tekst roept de Conversation Planner de Context Interpreter aan → een lijst `Interpretatie`.
  4. **Projectie (laag 1):** uitsluitend de interpretaties met `laag == "ontwerpvisie"` worden via `pas_interpretaties_toe` in `dc.interpretaties` (record) én in de voorlopige laag 1-velden gezet. Laag-2-interpretaties uit dezelfde aanroep worden niet door deze component geprojecteerd of geregistreerd.
  5. **Vervolgstapkeuze (deterministisch):** de vaste beslisvolgorde kiest exact één vervolgstap — een gerichte vraag óf een samenvatting ter bevestiging. De derde BUILD-005-uitkomst (voorstel tot ontwerpstudie) is in BUILD-017 vervangen door het overdrachtsmoment: zodra de architect bevestigt, is de bevestigde visie de levering (zie Uitvoer), zonder dat de component downstream start.
- **Uitvoer:** de bijgewerkte `DesignContext` (laag 1) + precies één vervolgstap. Zodra de architect (buiten de component) bevestigt, is de bevestigde `OntwerpVisie` de levering.
- **Foutafhandeling:** een fout in de interpretatie-grens → signalering; **geen partiële/corrupte laag 1** (projectie vindt alleen plaats op een geslaagde interpretatielijst); de DesignContext blijft anders ongewijzigd.

## 3. Gegevensmodellen (technische representatie)

- **Geen nieuw resultaat-object buiten de DesignContext.** De Conversation Planner bouwt laag 1 **in-place** op; hij produceert geen result-object zoals de downstream-planners.
- **`Interpretatie` (bestaand, BUILD-004):** `laag, veld, waarde, zekerheid` — het herkomst-record. Ongewijzigd hergebruikt.
- **`OntwerpVisie` (bestaand, laag 1):** de voorlopige velden + `bevestigd_door_architect` (uitsluitend gelezen door de component).
- **`Vervolgstap` (licht, intern):** het type (`vraag` | `samenvatting_ter_bevestiging`) en de inhoud; een structuur binnen de Conversation Planner-module (BUILD-005, hoofdstuk 8), **geen** DesignContext-laag. **Geen eigen status.**
- **Returnwikkel:** de bijgewerkte DesignContext-referentie + de gekozen `Vervolgstap`, of uitsluitend een signalering bij een fout.

## 4. Validatie

- **Write-gate (read-only na bevestiging):** elke schrijfactie naar laag 1 wordt voorafgegaan door de toets `not dc.ontwerpvisie.bevestigd_door_architect`. Is de visie bevestigd, dan schrijft de component niets (laag 1 is onaantastbaar, BUILD-008).
- **Laag-scope:** uitsluitend `laag == "ontwerpvisie"`-interpretaties worden geprojecteerd; laag 2 en verder worden nooit door deze component geschreven.
- **Nooit bevestigen:** de component zet `bevestigd_door_architect` nooit; bevestiging is exclusief de architect (`mag_bevestigen("ontwerpvisie", Eigenaar.ARCHITECT)`, BUILD-008 §5/AB-008).
- **Consistentie interpretaties ↔ velden:** de velden zijn steeds een verbatim projectie van de geregistreerde interpretaties (+ de directe `vrije_tekst`); de component voegt geen eigen, van het record afwijkende waarde toe. Zo blijft `dc.interpretaties` een getrouw herkomst-record van elke laag 1-waarde.
- **Samenvatting ter bevestiging** wordt alleen aangeboden bij een niet-lege visie (aansluitend op de invariant in `design_context.valideer()`: een bevestigde visie mag niet leeg zijn).

## 5. Regeneratie / herstel

- **Turn-gedreven:** de component draait per gespreksbeurt; er is geen interne lus die zichzelf herhaalt. Nieuwe gebruikersinvoer → nieuwe beurt.
- **Idempotente projectie:** het opnieuw projecteren van dezelfde interpretaties levert dezelfde laag 1-velden (verbatim kopie) — herhaling is veilig en deterministisch.
- **Herstel bij interpretatiefout:** faalt de interpretatie-grens, dan volgt een signalering en blijft laag 1 ongewijzigd; de gebruiker kan het opnieuw formuleren. Geen partiële projectie.

## 6. Interfaces

- **Gebruiker ↔ Conversation Planner:** de dialoog (vrije tekst in, vervolgstap uit). De feitelijke chat-/UI-koppeling valt buiten deze component (BUILD-005 §8).
- **Conversation Planner → Context Interpreter (BUILD-004):** `interpreteer_context(vrije_tekst, …)` als **data-in/interpretaties-uit**; injecteerbaar; de Conversation Planner roept aan maar interpreteert niet zelf.
- **Conversation Planner → projectie (`pas_interpretaties_toe`, bestaand):** aangeroepen met **uitsluitend** de laag-1-interpretaties; schrijft het record + de laag 1-velden. Geen wijziging aan de functie.
- **Conversation Planner → DesignContext:** schrijft uitsluitend de onbevestigde laag 1; leest de overige stand read-only.
- **Architect → DesignContext:** zet `bevestigd_door_architect = True` (buiten de component; exclusieve autoriteit).
- **Conversation Planner → downstream (Ontwerpstrategie-stap, Reasoning Engine, …):** **geen aanroep.** De component levert uitsluitend de bevestigde `OntwerpVisie` op; downstream wordt niet gestart.

## 7. Traceerbaarheid

- **`dc.interpretaties`** is het volledige, append-only **herkomst-record** van elke laag 1-waarde: per waarde is herleidbaar uit welke interpretatie (`veld`, `waarde`, `zekerheid`) zij is geprojecteerd. De laag 1-velden zijn de actuele projectie daarvan.
- Er wordt **niets buiten de DesignContext** vastgelegd; de component muteert uitsluitend de onbevestigde laag 1 en (via de bestaande projectie) het interpretatie-record.

## 8. Robuustheid

- **Single-writer-discipline:** laag 1 wordt uitsluitend door deze component (via de projectie) geschreven; interpretaties uitsluitend door de Context Interpreter geproduceerd; de bevestigingsvlag uitsluitend door de architect gezet. Dat voorkomt tegenstrijdige schrijvers.
- **Read-only na bevestiging — technische afdwinging:** Python-dataclasses zijn niet taalkundig immutabel; "read-only" wordt daarom afgedwongen doordat de **enige** laag 1-schrijver (deze component) op `bevestigd_door_architect` gate't en na bevestiging niet meer schrijft. De model-invariant (`design_context.valideer()`: bevestigde visie niet leeg) vult dit aan. Geen andere keten-component schrijft laag 1 (geverifieerd in de kwaliteitsronde: downstream is volledig read-only).
- **AI-model-onafhankelijk / deterministisch:** de eigen beslislogica is deterministisch; het AI-model zit uitsluitend achter de injecteerbare Context Interpreter-grens.
- **Additief:** nieuw bestand; geen wijziging aan `design_context.py`, `context_interpreter.py`, de downstream-componenten of de bestaande pipeline.

## Consistentietoets (gevraagde ankers)

- **BUILD-004:** ✔ hergebruikt `interpreteer_context` (interpretatie) en `pas_interpretaties_toe` (projectie) ongewijzigd; de Conversation Planner interpreteert niet zelf.
- **BUILD-008:** ✔ laag 1 is architect-eigendom; de component stelt voorlopig voor, bevestigt nooit (`mag_bevestigen`), en behandelt de bevestigde visie als onaantastbaar. Laag 2 buiten scope.
- **BUILD-009:** ✔ levert precies de vereiste `bevestigd_door_architect is True` + niet-lege visie als vertrekpunt voor de Ontwerpstrategie-stap.
- **BUILD-010:** ✔ de Reasoning Engine Fase 1 gate't op `dc.ontwerpvisie.bevestigd_door_architect`; de Conversation Planner levert die toestand op maar roept de Reasoning Engine niet aan.
- **BUILD-017:** ✔ realiseert exact het functionele "wat" (laag 1 opbouwen, nooit bevestigen, read-only na bevestiging, geen downstream-start).
- **Downstream-keten (BUILD-011 t/m BUILD-016):** ✔ dezelfde read-only/gate-discipline; de Conversation Planner start niets en muteert geen downstream-object.

---

**Acceptatie:** de Conversation Planner bouwt, uitsluitend zolang `bevestigd_door_architect` onwaar is, de laag 1-velden op als verbatim projectie van de door de Context Interpreter geleverde `ontwerpvisie`-interpretaties (record in `dc.interpretaties`), kiest per beurt deterministisch precies één vervolgstap (vraag of samenvatting ter bevestiging), bevestigt nooit, schrijft nooit een andere laag, en levert na bevestiging uitsluitend de read-only bevestigde `OntwerpVisie` op zonder downstream te starten; een interpretatiefout leidt tot een signalering zonder mutatie — alles additief en zonder wijziging aan bestaande bestanden.
