# AR-001 — Architectuurreview Fase 1

**Status:** formele architectuurreview, ter beoordeling. Geen BUILD, geen implementatie, geen nieuwe architectuur, geen nieuwe functionaliteit. Doel: vaststellen of de architectuur van Fase 1 voldoende stabiel is om de volgende BUILD's hierop te baseren.

**Gereviewde documenten:** `RELEASE_0.2_DESIGNCONTEXT_FOUNDATION.md`, `SPEC-000_PROJECT_CHARTER.md`, `DESIGN_CONTEXT_MODEL.md`, `DISCOVERY-004_ONTWERPPRINCIPE.md`, `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, `VISION-001_FLOOR_VISUALIZATION_PLATFORM.md`, `OPEN_ARCHITECTUURVRAGEN.md`, BUILD-004 (functioneel + technisch), BUILD-005 (ontwerpprincipe + functioneel + technisch), BUILD-006, BUILD-007 (functioneel + technisch).

---

## 1. Sterke punten

- **Eén architectuurprincipe, consequent toegepast op steeds meer lagen.** "Iedere AI-component produceert interpretaties, nooit waarheden" (BUILD-004, hoofdstuk 0) is letterlijk overgenomen in BUILD-005 (hoofdstuk 2) en herbevestigd in BUILD-007 Technisch Ontwerp (hoofdstuk 0) — nergens herformuleerd, nergens verzwakt.
- **Eigenaarschap propageert aantoonbaar omlaag.** De regel uit `DESIGN_BRAIN_ARCHITECTUURVISIE.md` ("Geen enkele component van de Design Brain mag zelfstandig ontwerpbeslissingen definitief bevestigen...") is terug te vinden in SPEC-000 (hoofdstuk 7), BUILD-004 (hoofdstuk 2), BUILD-005 (hoofdstuk 2) en BUILD-007 (impliciet, via de voorgesteld/bevestigd-discipline die in hoofdstuk 8 van het technisch ontwerp bewust als open punt is benoemd in plaats van stilzwijgend verondersteld).
- **Bewijs-vóór-aannames-discipline is geen loze tekst.** BUILD-002/003 zijn getest via AST-analyse en identieke-output-vergelijking; BUILD-006 is getest via een live render tegen de bestaande, ongewijzigde Mockup Engine. Dit is zichtbaar in de acceptatiecriteria, niet alleen in de intentieverklaringen.
- **De governance rond openstaande vragen werkt in de praktijk.** AV-001 en AV-002 zijn niet stilzwijgend weggewerkt of terloops besloten — ze staan nog exact zo open als op het moment van ontstaan, en latere BUILD's (BUILD-005, BUILD-007) zijn expliciet gebouwd mét die onzekerheid, niet eromheen.
- **Zelfcorrigerend documentproces.** De laatste reviewronde op BUILD-007 Functioneel Ontwerp corrigeerde zelf drie eigen inconsistenties (Context Interpreter ontbrak in de lijst interne fasen; Floor Design leende gedrag van de Conversation Planner; Design Brain dook ongeankerd op) — dat is precies het soort zelfcontrole dat deze architectuur beoogt te bewijzen.
- **Scheiding UX/interne architectuur is in BUILD-007 Functioneel Ontwerp goed doorgevoerd.** Fase 3 ("Van vraag naar begrip") benoemt DesignContext, Context Interpreter en Conversation Planner expliciet voor de lezer van het document, maar articuleert steeds waarom dit voor de architect onzichtbaar blijft. Geen van de overige fasen lekt interne componentnamen naar de gebruikerservaring.

## 2. Risico's

### 2.1 Consistentie van architectuurobjecten — twee onverzoende architectuurketens

`DESIGN_BRAIN_ARCHITECTUURVISIE.md` (hoofdstuk "De ontwerpketen") legt vast:

```
Projectcontext → Ontwerpintentie → Ontwerpsignatuur
    → DCOD Design Brain (Context → Strategie → Reasoning → Materiaal/Patroon/SVG)
    → Mock-up → Iteratieve verfijning
```

`BUILD-007` legt vast:

```
Project → Ontwerpvraag → DesignContext → Context Interpreter → Conversation Planner
    → Floor Design → Material Profile → Scene → Floor Visualization Engine
    → Visualisatie → Design Transfer Package → DCOD
```

Dit zijn twee structureel verschillende ontledingen van hetzelfde proces, met eigen namen voor vergelijkbare stappen, en ze zijn nooit expliciet naast elkaar gelegd:

- **Ontwerpsignatuur** (DESIGN_BRAIN-doc, met een eigen, vastgestelde v1-scope: sessiegebonden) komt in BUILD-007 nergens meer voor. Onduidelijk of dit begrip stilzwijgend is losgelaten, is opgegaan in Ontwerpvraag, of nog steeds geldt maar ontbreekt in de nieuwe keten.
- **Reasoning Engine, Material Planner, Pattern Planner, SVG Planner** (DESIGN_BRAIN-doc, en herhaald in SPEC-000 hoofdstuk 16 als toekomstige Design Brain-componenten) hebben geen aangewezen plek in de BUILD-007-keten. In het bijzonder is onduidelijk of **Material Planner** en **Material Profile** hetzelfde begrip zijn onder twee namen, of twee verschillende dingen.
- **Regel 1 van `DESIGN_BRAIN_ARCHITECTUURVISIE.md`** ("Er komt een expliciete, woord-voor-woord mapping... Deze mapping moet zijn vastgesteld vóórdat er componenten op worden gebouwd") is nooit als zelfstandig artefact opgeleverd. BUILD-004 heeft in de praktijk gewoon de DesignContext Model-terminologie gebruikt in plaats van de DESIGN_BRAIN-doc-terminologie — een redelijke uitkomst, maar de eigen preconditie van het document is daarmee nooit formeel afgesloten, alleen impliciet omzeild.

Dit is al eerder herkend en bewust uitgesteld ("Eerst ronden we BUILD-006 af en bespreken we BUILD-007. Daarna voeren we een gecontroleerde architectuurreview uit op `DESIGN_BRAIN_ARCHITECTUURVISIE.md`") — AR-001 constateert dat dit moment nu is aangebroken: elke volgende BUILD die dieper op Floor Design of Material Profile bouwt, bouwt op een punt waar twee vocabulaires elkaar nog niet hebben ontmoet.

### 2.2 Zuiverheid van verantwoordelijkheden — asymmetrische toegang tot DesignContext

BUILD-007 Technisch Ontwerp stelt expliciet (hoofdstuk 2): *"Floor Visualization Engine... werkt, conform VISION-001, uitsluitend met deze drie gestandaardiseerde objecten [Floor Design, Material Profile, Scene] — nooit rechtstreeks met DesignContext..."*

Diezelfde technisch ontwerp staat toe dat het Design Transfer Package wél rechtstreeks bij DesignContext komt: *"DesignContext (visie) + Floor Design + Material Profile + Visualisatie → Design Transfer Package"* (hoofdstuk 3/4).

Twee downstream-componenten krijgen dus een verschillende regel voor dezelfde bron (DesignContext): de ene mag er niet bij, de andere wel. Dat kan een bewuste, verdedigbare keuze zijn (Design Transfer Package heeft mogelijk de oorspronkelijke, woordelijke visie nodig, die niet in de afgeleide Floor Design-vorm bewaard blijft) — maar die redenering staat nergens uitgeschreven. Zonder motivering is dit een asymmetrie die de eigen regel ("Floor Visualization Engine werkt uitsluitend met gestandaardiseerde objecten") lijkt tegen te spreken.

### 2.3 Zuiverheid van verantwoordelijkheden — onvolledige lijst met open afleidingsvragen

BUILD-007 Technisch Ontwerp (hoofdstuk 8) benoemt expliciet dat de afleiding van **Floor Design** uit DesignContext een open punt is. Dezelfde open vraag geldt structureel identiek voor **Material Profile** ten opzichte van de DesignContext-laag Materialisatie — Material Profile is expliciet gedefinieerd als "geen synoniem" voor Materialisatie (BUILD-007 Functioneel Ontwerp, terminologiesectie), wat automatisch dezelfde vraag oproept die bij Floor Design wél is gesteld: hoe wordt Material Profile dan wél afgeleid? Deze vraag ontbreekt in de openstaande-puntenlijst van hoofdstuk 8, terwijl de onderliggende situatie identiek is.

### 2.4 SPEC-000 Documenthiërarchie is niet meer volledig

SPEC-000 hoofdstuk 8 (Documenthiërarchie) eindigt bij `DESIGN_BRAIN_ARCHITECTUURVISIE.md` en de BUILD-001-t/m-003-serie. VISION-001, BUILD-004 t/m BUILD-007 en `OPEN_ARCHITECTUURVRAGEN.md` hebben geen plaats in dit schema, terwijl SPEC-000 zichzelf omschrijft als het document dat "alle overige documenten" positioneert. Dit is al eerder gesignaleerd en bewust uitgesteld tot een gecontroleerde revisie — AR-001 herbevestigt dit als een structureel, nog open punt, niet als een nieuwe bevinding.

### 2.5 Open architectuurvragen — registerstatus is licht verouderd

AV-001 (`OPEN_ARCHITECTUURVRAGEN.md`) beschrijft zijn Impact-veld nog uitsluitend in termen van de drie BUILD-005-documenten en `DESIGN_BRAIN_ARCHITECTUURVISIE.md`. BUILD-007 is volledig op de nog-onopgeloste positionering van de Conversation Planner (Project Brain vs. Design Brain) gebouwd zonder dat het Impact-veld van AV-001 is bijgewerkt om BUILD-007 te vermelden. Dit is een registeronderhoudspunt, geen inhoudelijke fout.

### 2.6 Procesconsistentie — adviesdocument-stap uit SPEC-000 §9

SPEC-000 (hoofdstuk 9, BUILD-methodiek) stelt: *"Voorafgaand aan iedere migratie wordt een adviesdocument opgesteld dat kandidaten rangschikt op migratierisico..."* Dit is voor BUILD-002/003 gevolgd (`BUILD-002_VOORSTEL.md`, `BUILD-003_VOORSTEL.md`, `BUILD-003_ADVIES.md`), maar niet meer zichtbaar vanaf BUILD-004. Dit is waarschijnlijk een terechte, impliciete koerswijziging — BUILD-004 introduceert zelf al expliciet dat het "een geheel nieuwe capaciteit zonder legacy-equivalent" betreft, niet een migratie van een bestaande beslissing (BUILD-004 Technisch Ontwerp, hoofdstuk 6) — maar SPEC-000 §9 zelf is nooit aangepast om dat onderscheid (migratie van bestaande beslissing vs. introductie van nieuwe capaciteit) te erkennen. De regel zoals hij nu in SPEC-000 staat, dekt de sinds BUILD-004 gevolgde praktijk niet meer letterlijk.

## 3. Toekomstige uitbreidbaarheid

Geen blokkerende bevindingen. De reeds bewezen patronen (additieve koppeling, geïsoleerde modules, gedeelde DesignContext-instantie zonder onderlinge kennis tussen componenten, gestandaardiseerde Scene ongeacht bron) zijn herbruikbaar en worden in BUILD-007 consequent verondersteld voor de nog te bouwen onderdelen. Het enige uitbreidbaarheidsrisico volgt indirect uit 2.1: zolang twee vocabulaires naast elkaar bestaan, is niet vast te stellen of een toekomstige component (bijvoorbeeld een Pattern Planner) een nieuwe BUILD wordt, of stilzwijgend samenvalt met iets dat BUILD-007 al anders heeft genoemd.

## 4. Aanbevelingen

Uitsluitend procesmatig, geen architectuurbesluiten:

- Voer de al geplande, gecontroleerde review van `DESIGN_BRAIN_ARCHITECTUURVISIE.md` uit vóórdat een volgende BUILD start op Floor Design of Material Profile — bevinding 2.1 maakt dit concreter dan voorheen: expliciet vaststellen wat er gebeurt met Ontwerpsignatuur, Reasoning Engine, Material Planner, Pattern Planner en SVG Planner ten opzichte van de BUILD-007-keten.
- Leg de motivering voor de asymmetrische DesignContext-toegang (2.2) expliciet vast — of pas de regel aan zodat Design Transfer Package dezelfde beperking krijgt als Floor Visualization Engine.
- Vul hoofdstuk 8 van BUILD-007 Technisch Ontwerp aan met de ontbrekende, structureel identieke open vraag over Material Profile (2.3).
- Neem de update van SPEC-000 Documenthiërarchie (2.4) mee in de al geplande revisie.
- Werk het Impact-veld van AV-001 bij met een verwijzing naar BUILD-007 (2.5).
- Overweeg bij de eerstvolgende SPEC-000-revisie (die toch al gepland is voor AV-002) ook §9 te verduidelijken met het sinds BUILD-004 gehanteerde onderscheid tussen migratie en nieuwe capaciteit (2.6).

## 5. Blockers voor volgende BUILD's

- **Wel een blocker:** een BUILD die Floor Design of Material Profile technisch verder uitwerkt, zonder eerst bevinding 2.1 te adresseren, loopt het risico een derde vocabulaire te introduceren naast de twee die al naast elkaar bestaan.
- **Geen blocker, wel aandachtspunt vóór bouw:** bevinding 2.2 (asymmetrische DesignContext-toegang) moet zijn opgehelderd vóórdat Design Transfer Package technisch wordt uitgewerkt, anders wordt een niet-onderbouwde uitzondering als vaststaand gegeven meegenomen.
- **Geen blocker:** bevindingen 2.3, 2.4, 2.5 en 2.6 zijn documentatie- en registeronderhoud, niet van invloed op de vraag of de bestaande, reeds geïmplementeerde keten (DesignContext, Context Interpreter, Conversation Planner-ontwerp, Scene Builder) stabiel genoeg is om op voort te bouwen.

## 6. Eindoordeel

De architectuur van Fase 1 is **stabiel voor het reeds geïmplementeerde deel van de keten** (DesignContext Model t/m Scene Builder): consistent getest, consistent gedocumenteerd, consistent teruggekoppeld naar dezelfde, nooit-verzwakte principes. Voor het **nog niet gebouwde deel van de keten** (Floor Design, Material Profile, Floor Visualization Engine, Design Transfer Package) is de architectuur nog niet stabiel genoeg om zonder meer op voort te bouwen — niet omdat er iets fout is vastgesteld, maar omdat een deel van wat er eerder al is vastgesteld (`DESIGN_BRAIN_ARCHITECTUURVISIE.md`) nog niet met deze nieuwere vaststelling is verzoend.
