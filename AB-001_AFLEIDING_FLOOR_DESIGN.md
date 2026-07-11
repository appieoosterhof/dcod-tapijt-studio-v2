# AB-001 — Concept-Architectuurbesluit: afleiding van Floor Design uit DesignContext

**Status:** concept, ter beoordeling. Geen enkel bestaand document is gewijzigd. Vervolg op AR-002, besluitpunt 2 en 3.

**Vraagstelling:** vormen de nog niet gerealiseerde begrippen Ontwerpstrategie-stap, Reasoning Engine en Pattern Planner (uit `DESIGN_BRAIN_ARCHITECTUURVISIE.md`) daadwerkelijk de ontbrekende architectuurlaag tussen DesignContext en Floor Design, zoals in BUILD-007 Technisch Ontwerp (hoofdstuk 8) als open punt is vastgelegd?

---

## 1. Vastgestelde feiten

Uitsluitend letterlijke of ondubbelzinnige inhoud uit bestaande documenten, geen interpretatie:

- **F1.** `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, Regel 2: "Ontwerpstrategie is geen onderdeel van de Reasoning Engine. Het wordt gemodelleerd als een afzonderlijke stap tussen Context en Reasoning, met behoud van het eigenaarschap dat het bevroren model daaraan toekent." Interne opbouw: "Context Interpreter → Ontwerpstrategie (eigen stap) → Reasoning Engine → Material Planner / Pattern Planner / SVG Planner."
- **F2.** `DESIGN_CONTEXT_MODEL.md`, laag 3 (Ontwerpstrategie): "de professionele vertaalslag tussen Ontwerpvisie + Projectcontext en het uiteindelijke Concept." Eigenaar: gezamenlijk (DCOD + architect). Vastgelegde informatie: "de gezamenlijk ontwikkelde aanpak in benoembare termen."
- **F3.** `DESIGN_CONTEXT_MODEL.md`, laag 4 (Concept): "de strategie concreet en zichtbaar maken — het eerste tastbare resultaat in de dialoog." Eigenaar: gedeeld (DCOD stelt voor, architect stuurt bij). Vastgelegde informatie: "stijlfamilie, kleurpalet, complexiteit/motiefschaal."
- **F4.** `BUILD-007_TOEKOMSTIGE_WORKFLOW_FUNCTIONEEL_ONTWERP.md` (na review gecorrigeerd, door gebruiker bevestigd): "Floor Design — het centrale domeinobject **ná de ontwerpfase**. Geen samenvoeging van Ontwerpstrategie en Concept, en geen tweede centraliteitsclaim naast DesignContext — **een andere fase, een andere reikwijdte**."
- **F5.** `BUILD-007_TOEKOMSTIGE_WORKFLOW_TECHNISCH_ONTWERP.md`, hoofdstuk 3: "DesignContext → Floor Design: Floor Design wordt afgeleid uit de op dat moment vastgelegde inhoud van DesignContext. **De precieze afleiding is een open punt** (hoofdstuk 8), geen vastgesteld mechanisme."
- **F6.** `BUILD-005_CONVERSATION_PLANNER_FUNCTIONEEL_ONTWERP.md`, hoofdstuk 2: de Conversation Planner interpreteert zelf geen informatie, neemt zelf geen ontwerpbeslissingen, en voert zelf geen ontwerpstudie uit — hij bepaalt uitsluitend óf en wannéér een van drie uitkomsten volgt, waaronder "het voorstel om een eerste ontwerpstudie te starten."
- **F7.** `SPEC-000_PROJECT_CHARTER.md`, §14: "Een Ontwerpstudie is een mogelijke ontwerprichting binnen een project. Een studie vormt het uitgangspunt voor verdere ontwikkeling en kan meerdere varianten bevatten."
- **F8.** `SPEC-000_PROJECT_CHARTER.md`, §16 (Toekomstvisie): noemt Ontwerpstrategie-stap, Reasoning Engine, Material Planner, Pattern Planner en SVG Planner letterlijk als nog te bouwen, afzonderlijke Design Brain-componenten.
- **F9.** Geen van de gereviewde documenten (SPEC-000, DESIGN_CONTEXT_MODEL.md, DESIGN_BRAIN_ARCHITECTUURVISIE.md, BUILD-004 t/m BUILD-007, VISION-001) beschrijft een expliciet mechanisme dat een bevestigd Concept (DesignContext laag 4) omzet in een Floor Design-object.

## 2. Architectuurinterpretaties

Redeneringen die de bovenstaande feiten verbinden — zelf geen vaststaand feit, wel direct herleidbaar:

- **I1.** F1 en F2/F3 samen suggereren dat "Ontwerpstrategie (eigen stap)" en "Reasoning Engine" zijn bedoeld als de (nog te bouwen) verwerkende componenten die respectievelijk DesignContext-laag 3 (Ontwerpstrategie) en laag 4 (Concept) van voorgestelde inhoud voorzien — naar hetzelfde patroon waarop Context Interpreter (BUILD-004) de lagen 1 en 2 vult.
- **I2.** F4 legt vast dat Floor Design nadrukkelijk **niet** gelijk is aan, of een samenvoeging van, Ontwerpstrategie en Concept. Floor Design hoort bij "een andere fase, een andere reikwijdte" dan de ontwerpfase-lagen van DesignContext.
- **I3.** I1 en I2 samen leveren een spanning op: als Reasoning Engine (via I1) inhoudelijk gericht is op het vullen van DesignContext-laag 4 (Concept — nog steeds binnen de ontwerpfase, nog steeds onder het gedeelde eigenaarschap van die laag), dan is de meest voor de hand liggende output van Reasoning Engine/Pattern Planner **Concept**, niet **Floor Design** — want Floor Design is expliciet gedefinieerd als iets ná, niet binnen, die fase.
- **I4.** F6 en F7 samen suggereren een derde mogelijke lezing die in AR-002 nog niet was onderzocht: de Conversation Planner stelt voor om een **Ontwerpstudie** te starten (F6), en een Ontwerpstudie is "een mogelijke ontwerprichting... uitgangspunt voor verdere ontwikkeling, kan meerdere varianten bevatten" (F7) — een omschrijving die inhoudelijk sterk overeenkomt met hoe Floor Design zelf wordt omschreven in BUILD-007 fase 4 ("een richting die de architect kan herkennen, bijstellen of afwijzen"). Het is op basis van de huidige documenten niet vast te stellen of Floor Design **is** het resultaat van een gestarte Ontwerpstudie, dan wel of dit twee onafhankelijke begrippen zijn die toevallig gelijksoortig zijn omschreven.
- **I5.** F9 bevestigt dat er, onafhankelijk van I1-I4, geen enkel document een expliciete "Concept → Floor Design"-vertaalstap benoemt — deze ontbreekt hoe dan ook, ongeacht welke van de bovenstaande lezingen juist blijkt.

## 3. Spanning (kern van dit besluit)

De oorspronkelijke AR-002-hypothese (Ontwerpstrategie-stap + Reasoning Engine + Pattern Planner vormen samen de ontbrekende laag tussen DesignContext én Floor Design) blijkt bij nadere toetsing **te grof**: het brondocument (`DESIGN_BRAIN_ARCHITECTUURVISIE.md`) positioneert deze componenten als producenten van DesignContext-lagen 3 en 4 — dus **binnen** de ontwerpfase — terwijl Floor Design in BUILD-007 juist expliciet en recent is bevestigd als "een andere fase, een andere reikwijdte" — dus **buiten** die lagen. Beide vaststellingen zijn zelf correct en blijven overeind; ze zijn alleen nooit met elkaar in verband gebracht.

## 4. Voorgestelde keuze

Gesplitst in het deel waarover op basis van de huidige documenten wél een uitspraak te onderbouwen is, en het deel waarover niet:

**A — wél te onderbouwen:** Ontwerpstrategie-stap en Reasoning Engine worden voorgesteld als de nog te bouwen componenten die DesignContext-lagen 3 (Ontwerpstrategie) en 4 (Concept) van voorgestelde inhoud voorzien, naar hetzelfde, al bewezen patroon als Context Interpreter voor lagen 1 en 2. Dit blijft **volledig binnen** de bestaande DesignContext-architectuur en wijzigt niets aan BUILD-007.

**B — niet te onderbouwen, dus niet besloten:** of (en hoe) de output van Reasoning Engine/Pattern Planner vervolgens Floor Design oplevert, blijft onbeslist. De drie in F9/I4/I5 blootgelegde alternatieve lezingen (Floor Design als vertaalslag ná een bevestigd Concept; Floor Design als resultaat van een gestarte Ontwerpstudie; Floor Design als volledig zelfstandig, niet van Concept afgeleid object) zijn met de huidige documenten niet van elkaar te onderscheiden.

**Dit Architectuurbesluit wordt daarom uitsluitend voor deel A voorgesteld ter goedkeuring. Voor deel B wordt hier expliciet geconcludeerd dat een definitief besluit nog niet mogelijk is (zie hoofdstuk 7).**

## 5. Overwogen alternatieven

- **Alternatief 1 — Reasoning Engine/Pattern Planner produceren Floor Design rechtstreeks** (de oorspronkelijke AR-002-hypothese). *Afgewezen als definitief besluit*: in spanning met F4 (Floor Design is expliciet geen Ontwerpstrategie/Concept, andere fase). Niet te weerleggen, maar ook niet te bevestigen — vandaar dat dit als open vraag terugkomt in hoofdstuk 7, niet als afwijzing van de mogelijkheid zelf.
- **Alternatief 2 — Reasoning Engine/Pattern Planner laten vervallen, Floor Design krijgt een volledig nieuw, naamloos generatiemechanisme, los van de DESIGN_BRAIN-terminologie.** *Afgewezen*: dit zou Regel 1 van `DESIGN_BRAIN_ARCHITECTUURVISIE.md` (canonieke woordenschat) doorkruisen zonder enige onderbouwing, en gooit een mogelijk bruikbare eerdere denkstap weg zonder dat is aangetoond dat die overbodig is.
- **Alternatief 3 — Ontwerpstrategie-stap en Reasoning Engine uitsluitend positioneren als producenten van DesignContext-lagen 3/4, met Floor Design's afleiding als aparte, nog open vraag.** *Voorgesteld* (zie hoofdstuk 4, deel A) — de enige lezing die volledig consistent is met alle negen vastgestelde feiten, zonder een niet-onderbouwde aanname over Floor Design toe te voegen.
- **Alternatief 4 — Volledig besluiten dat Floor Design het resultaat is van een gestarte Ontwerpstudie (F6/F7/I4).** *Niet afgewezen, maar nog niet rijp*: geen van de documenten bevestigt of ontkent dit; het zou een nieuw, niet eerder vastgesteld verband tussen Conversation Planner-uitkomst en Floor Design vastleggen dat een eigen, apart Architectuurbesluit verdient — niet iets om terloops binnen AB-001 mee te nemen.

## 6. Consequenties van de voorgestelde keuze (deel A)

- Ontwerpstrategie-stap en Reasoning Engine kunnen als toekomstige, afzonderlijke BUILD's op de bestaande manier worden voorbereid (functioneel ontwerp → technisch ontwerp → implementatie), op dezelfde wijze als BUILD-004/BUILD-005, gericht op het vullen van DesignContext-lagen 3 en 4.
- Dit besluit **sluit geen enkele optie voor Floor Design's afleiding uit** — het legt uitsluitend vast dát Reasoning Engine ergens vóór Floor Design in de keten zit (als Concept-producent), niet dat Reasoning Engine Floor Design zelf produceert.
- BUILD-007 Technisch Ontwerp hoofdstuk 8 blijft, ook na dit besluit, een open punt bevatten — dit besluit maakt dat punt scherper (de vraag is niet meer "hoe wordt Floor Design afgeleid", maar specifiek "hoe wordt een bevestigd Concept vertaald naar Floor Design"), maar sluit het niet.

## 7. Conclusie: gedeeltelijk besluit mogelijk

Een **volledig** Architectuurbesluit zoals oorspronkelijk gevraagd (bevestigen dat Ontwerpstrategie-stap, Reasoning Engine én Pattern Planner samen de laag tussen DesignContext én Floor Design vormen) is **niet mogelijk** met de huidige documenten — de bestaande, recent bevestigde omschrijving van Floor Design (F4) staat op gespannen voet met de meest voor de hand liggende lezing van Reasoning Engine's rol (I1/I3).

Een **deelbesluit** (deel A, hoofdstuk 4) is wel te onderbouwen en wordt hier ter goedkeuring voorgesteld.

**Benodigde aanvullende informatie om deel B alsnog te kunnen besluiten:**

1. Een expliciete uitspraak of Floor Design wordt afgeleid van een bevestigd Concept (en zo ja, via welk mechanisme — een hernieuwde rol voor Pattern Planner, of een nieuw, nog naamloos onderdeel), dan wel volledig autonoom tot stand komt.
2. Verduidelijking van wat "andere fase, andere reikwijdte" (F4) precies uitsluit: uitsluitend dat Floor Design geen synoniem/samenvoeging is (wat vaststaat), of ook dat er geen enkele directe afleidingsrelatie met Concept bestaat (wat nog niet vaststaat).
3. Een uitspraak of de relatie tussen Conversation Planner's "voorstel tot een Ontwerpstudie" (F6) en Floor Design (I4) toeval is (twee gelijksoortig omschreven maar onafhankelijke begrippen), of een daadwerkelijk architectuurverband dat nog moet worden vastgelegd.

Zolang deze drie punten open staan, geldt voor Floor Design's afleidingsmechanisme: **geen architectuurwijziging, huidige open status in BUILD-007 hoofdstuk 8 gehandhaafd.**
