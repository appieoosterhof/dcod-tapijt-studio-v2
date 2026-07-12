# BUILD-017 — Conversation Planner: functioneel ontwerp

**Status:** functioneel ontwerp, gereed voor architectuurreview (VR). Beschrijft uitsluitend **wat** de Conversation Planner doet, niet **hoe**. Geen nieuwe architectuurcomponent — de Conversation Planner is de reeds vastgestelde conversationele voorkant van de Design Brain (BUILD-005, principe + functioneel). BUILD-017 **positioneert en scherpt** die component specifiek aan als de bouwer van de **OntwerpVisie** (DesignContext laag 1) die de downstream-keten voedt; het vervangt BUILD-005 niet, maar bouwt erop voort. Verankerd in AB-001, AB-002, AB-005, BUILD-004, BUILD-005, BUILD-007, BUILD-008 en BUILD-009.

**Uitgangspunt:** de Conversation Planner **bouwt samen met de gebruiker de OntwerpVisie op**. Zolang de visie nog niet is bevestigd, schrijft hij uitsluitend naar die OntwerpVisie (laag 1) — nooit naar een andere laag. Hij **maakt nooit ontwerpbeslissingen** en **bevestigt nooit**: alleen de architect kan de OntwerpVisie definitief bevestigen (`bevestigd_door_architect`). Na bevestiging is de OntwerpVisie voor de Conversation Planner volledig **read-only**. Hij **start geen downstream-componenten**; zijn levering is uitsluitend de bevestigde OntwerpVisie.

---

## 1. Plaats in de architectuur

De Conversation Planner staat **helemaal vooraan** in de Design Brain — vóór de gehele downstream-keten. Waar de nageschakelde componenten (Ontwerpstrategie-stap → Reasoning Engine → Material Planner → Pattern Planner → SVG Planner → Floor Visualization Engine → Design Transfer Package) een **bevestigde** OntwerpVisie als vertrekpunt veronderstellen, is de Conversation Planner juist de component die die bevestigde OntwerpVisie tot stand helpt komen, in dialoog met de gebruiker. Hij vult laag 1 van het DesignContext Model; de interpretatie van losse invoer naar velden blijft bij de Context Interpreter (BUILD-004).

## 2. Verantwoordelijkheid

De Conversation Planner **voert het gesprek dat de OntwerpVisie opbouwt**. Zijn verantwoordelijkheid is het, samen met de gebruiker, de OntwerpVisie (laag 1) zó ver en zó zuiver op te bouwen dat de architect haar kan bevestigen. Concreet betekent dat: de meest waardevolle volgende interactie bepalen (conform BUILD-005: een gerichte vraag óf een samenvatting ter bevestiging), en de voorlopige inhoud van de OntwerpVisie bijwerken op grond van wat de gebruiker aanreikt en wat de Context Interpreter interpreteert. Expliciet: hij **beslist niets**, **interpreteert niet zelf** (dat is de Context Interpreter), **bevestigt nooit** en voegt geen ontwerpintelligentie toe.

## 3. Input

- **Gebruikersinvoer** — de vrije verwoording van wens, sfeer, identiteit en ambitie door de gebruiker, in dialoogvorm.
- **DesignContext (huidige stand)** — met name de huidige (voorlopige) OntwerpVisie (laag 1) en de door de Context Interpreter voorgestelde **interpretaties met mate van zekerheid** (BUILD-004).
- **Gespreksgeschiedenis** — de reeds gevoerde interacties; een contextbron buiten het DesignContext Model (BUILD-005, hoofdstuk 8).
- **Projectfase** — waar het project zich in het traject bevindt; eveneens een contextbron buiten het model (BUILD-005).

Alle invoer wordt read-only gebruikt, met één uitzondering: de **nog niet bevestigde** OntwerpVisie, die de Conversation Planner mag bijwerken (§4/§8).

## 4. Output

- **De opgebouwde OntwerpVisie (voorlopig)** — de Conversation Planner werkt de velden van laag 1 bij (bv. `vrije_tekst`, `sfeer`, `gewenste_identiteit`, `ontwerpambitie`, `voorgestelde_interpretatie`) zolang `bevestigd_door_architect` nog `False` is. Dit is een voorlopige inhoud, geen beslissing.
- **De conversationele vervolgstap** — precies één per interactie: een gerichte vraag óf een samenvatting ter bevestiging (BUILD-005). Nooit nul, nooit meerdere.
- **De bevestigde OntwerpVisie (de levering)** — zodra de architect bevestigt, is de bevestigde OntwerpVisie het eindproduct van de Conversation Planner: het vertrekpunt dat de downstream-keten nodig heeft. De Conversation Planner levert deze op; hij **start de downstream-keten niet**.

## 5. Gebruikte gegevens

- **OntwerpVisie (laag 1)** — de velden die de gewenste beleving/identiteit/ambitie vastleggen; read-write zolang onbevestigd, read-only na bevestiging. De vlag `bevestigd_door_architect` wordt uitsluitend **gelezen** (nooit door de planner gezet).
- **Interpretaties + zekerheid** — van de Context Interpreter, om te bepalen wat al voldoende zeker is en dus geen vraag behoeft.
- **Gespreksgeschiedenis en projectfase** — als contextbronnen buiten het model, ter ondersteuning van de keuze van de vervolgstap.

De Conversation Planner leest of schrijft **geen andere laag** dan laag 1 (geen Project-/Ruimtecontext, Ontwerpstrategie, Concept, Materialisatie, Productierealisatie of Ontwerpredenering).

## 6. Wel / niet verantwoordelijk

**Wel:**
- de **OntwerpVisie opbouwen** in dialoog en haar voorlopige inhoud bijwerken zolang zij onbevestigd is;
- de **meest waardevolle vervolgstap** kiezen (gerichte vraag of samenvatting ter bevestiging);
- de bevestigde OntwerpVisie **opleveren** als vertrekpunt voor de rest van de Design Brain.

**Niet:**
- **niet zelf interpreteren** (dat is de Context Interpreter);
- **niet bevestigen** — `bevestigd_door_architect` is exclusief de architect;
- **geen andere laag wijzigen** dan de onbevestigde OntwerpVisie;
- **niet ontwerpen** en geen Concept/Floor Design/materiaal/patroon/SVG bepalen;
- **geen downstream-component starten** (Ontwerpstrategie-stap, Reasoning Engine, en verder);
- **de bevestigde OntwerpVisie niet meer wijzigen** (na bevestiging read-only).

## 7. Relaties met de overige componenten

- **Context Interpreter (BUILD-004):** interpreteert de gebruikersinvoer naar voorgestelde laag 1-velden met zekerheid; de Conversation Planner benut die interpretaties en delegeert het interpreteren volledig aan de Context Interpreter.
- **Architect (mens):** de enige die de OntwerpVisie definitief bevestigt. De Conversation Planner biedt daartoe een samenvatting ter bevestiging aan, maar voert de bevestiging niet zelf uit.
- **Ontwerpstrategie-stap (BUILD-009) en de verdere downstream-keten:** consumeren de **bevestigde** OntwerpVisie als vertrekpunt. De Conversation Planner levert die op maar kent de werking van de downstream-componenten niet en start ze niet.
- **DesignContext (BUILD-008):** de Conversation Planner schrijft uitsluitend naar de onbevestigde laag 1; alle overige lagen blijven onaangeroerd.

## 8. Grenzen

- De Conversation Planner **schrijft uitsluitend naar de OntwerpVisie (laag 1)** en uitsluitend **zolang deze niet is bevestigd**. Na bevestiging is laag 1 voor hem **read-only** — conform de onaantastbaarheid van laag 1 na bevestiging (BUILD-008).
- Hij draagt **geen ontwerpautoriteit**; elke uitkomst is een voorstel/controlemoment, geen beslissing (BUILD-005).
- Hij **raakt geen andere laag** en **produceert geen resultaat-object** van de ontwerpfase (Floor Design e.v. — AB-002).
- Hij **start geen downstream-keten**; zijn eindproduct is de bevestigde OntwerpVisie.
- Er ontstaat **geen nieuwe architectuurcomponent** — dit is de reeds vastgestelde Conversation Planner (BUILD-005), hier gepositioneerd op zijn visie-bouwende rol.

## 9. Architectuurbewaking (ter attentie van de VR)

### Consistentietoets met de gevraagde ankers

- **AB-001 / AB-002:** de Conversation Planner produceert **geen** Floor Design en leidt niets af; Floor Design is een resultaat van de latere ontwerpfase, downstream, buiten de DesignContext. De Conversation Planner levert uitsluitend het bevestigde laag 1-vertrekpunt waaruit — via strategie en concept — die afleiding pas veel later plaatsvindt. ✔ Consistent.
- **AB-005:** de SVG Planner is de bestaande, uitvoerende generatiepipeline, ver downstream; de Conversation Planner raakt die niet en voegt geen renderlogica toe. ✔ Consistent.
- **BUILD-007:** de Conversation Planner staat vóór de in BUILD-007 beschreven workflow; hij levert de bevestigde OntwerpVisie die de keten veronderstelt, en start die keten niet zelf. ✔ Consistent.
- **BUILD-008:** laag 1 is exclusief eigendom van de architect — DCOD stelt voorlopig voor, de architect bevestigt, en na bevestiging is de laag onaantastbaar. De Conversation Planner is precies die DCOD-voorkant: schrijft voorlopig, bevestigt nooit, en behandelt de bevestigde visie als read-only. ✔ Consistent.
- **BUILD-009:** de Ontwerpstrategie-stap vereist een **bevestigde, niet-lege** OntwerpVisie (`bevestigd_door_architect is True`). Dat is exact de levering van de Conversation Planner — de precondities sluiten naadloos aan. ✔ Consistent.
- **Downstream-keten (BUILD-010 t/m BUILD-016):** elke nageschakelde component start pas op bevestigde upstream-inhoud en is read-only op de DesignContext; de Conversation Planner respecteert diezelfde grens door na bevestiging niet meer te schrijven en de keten niet te starten. ✔ Consistent.

### Aandachtspunten die ik bewust markeer (geen nieuwe architectuur)

1. **Verhouding tot BUILD-005.** BUILD-017 vervangt BUILD-005 niet, maar spitst de rol toe op het opbouwen van de OntwerpVisie. Waar BUILD-005 als derde mogelijke uitkomst "het voorstel om een eerste ontwerpstudie te starten" noemde, wordt dat in de huidige, volledig uitgewerkte keten een **overdrachtsmoment**: zodra de OntwerpVisie is bevestigd, is zij beschikbaar als vertrekpunt voor de downstream-keten. De Conversation Planner **start die keten niet zelf** — consistent met het uitgangspunt "geen downstream starten". Ter bevestiging door de VR.
2. **Schrijfgrens tot laag 1.** BUILD-017 scoping legt de schrijfbevoegdheid uitsluitend bij de onbevestigde OntwerpVisie (laag 1). De Project-/Ruimtecontext (laag 2) valt **buiten** deze component; die wordt, net als de interpretatie van laag 1, door de Context Interpreter/bestaande flow gevoed. Ter bevestiging door de VR.
3. **Interpretatie blijft gedelegeerd.** Consistent met BUILD-005: de Conversation Planner interpreteert niet zelf; hij benut de interpretaties (met zekerheid) van de Context Interpreter en assembleert daarmee de voorlopige OntwerpVisie. De "schrijfactie" is dus het vastleggen van reeds voorgestelde, voorlopige inhoud — geen eigen interpretatie of beslissing.

---

**Reviewgereed:** dit document legt uitsluitend de verantwoordelijkheid, plaats, in-/output, gebruikte gegevens, relaties en grenzen van de Conversation Planner vast op functioneel niveau, met een expliciete consistentietoets tegen AB-001/AB-002/AB-005/BUILD-007/BUILD-008/BUILD-009 en de downstream-keten, en drie bewust gemarkeerde aandachtspunten (§9). Na een positieve VR kan het als basis dienen voor het technisch ontwerp — dat in dit document bewust nog niet is uitgewerkt.
