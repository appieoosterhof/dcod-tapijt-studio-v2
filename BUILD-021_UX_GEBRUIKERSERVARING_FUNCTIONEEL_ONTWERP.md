# BUILD-021 — Gebruikerservaring (UX) Dessinator: functioneel ontwerp

**Status:** functioneel ontwerp, gereed voor functionele review (VR). Beschrijft uitsluitend **wat de gebruiker ervaart**, niet **hoe** het technisch wordt gebouwd. Geen implementatie, geen code, geen architectuurwijziging. Ontwerpt de "Ontwerp zelf met AI"-ingang (CLAUDE.md openstaand punt) bovenop de reeds beschikbare Design Brain (BUILD-007/017/019/020) en de bestaande `/api/design-brain`-endpoints.

**Leidend principe (BUILD-005):** *De Dessinator gedraagt zich als een ervaren interieurarchitect die op het juiste moment de juiste vraag stelt, zonder ooit op de stoel van de ontwerper te gaan zitten.* De machinerie (lagen, profielen, gates, statussen, endpoints) blijft **volledig verborgen**; de gebruiker beleeft uitsluitend een ontwerpgesprek met begeleiding en beeld.

---

## 1. De gebruikersreis (overzicht)

Van **"Ik wil een vloer ontwerpen"** tot **"DCOD ontvangt een volledig overdrachtspakket"**, in vijf beleefde fasen (de technische keten eronder tussen haakjes):

1. **Vertellen** — de gebruiker beschrijft in eigen woorden wat hij wil; de Dessinator luistert en vraagt gericht door. *(Conversation Planner + Context Interpreter → visie + context)*
2. **Richting bepalen** — samen wordt de ontwerprichting scherp; de gebruiker bevestigt de kern. *(Ontwerpstrategie → Concept)*
3. **Vorm kiezen** — de gebruiker ziet een of enkele ontwerprichtingen en kiest er één. *(Floor Design)*
4. **Verfijnen** — materiaal en patroon worden voorgesteld en bijgesteld; het beeld groeit mee. *(Material Planner → Pattern Planner → SVG → Floor Visualization Engine)*
5. **Afronden** — de gebruiker ziet het eindresultaat in de ruimte, is tevreden, en draagt het over aan DCOD. *(Design Transfer Package)*

De gebruiker klikt nooit door een "wizard met stappen"; het voelt als één doorlopend gesprek waarin telkens beeld en keuze verschijnen.

## 2. Iedere gebruikersstap

Per stap: **ziet** · **doet** · *component (verborgen)* · **bevestiging** · **zichtbaar** / **verborgen**.

**Stap 0 — Start**
- **Ziet:** een rustige startpagina met één uitnodiging: *"Vertel me over de ruimte die u wilt aankleden."* Eén tekstveld, geen formulier.
- **Doet:** begint te typen (of kiest een voorbeeldzin).
- *Component:* nieuw gesprek wordt geopend.
- **Verborgen:** dat er een gesprek-identiteit en een sessie ontstaat.

**Stap 1 — Vertellen & doorvragen**
- **Ziet:** zijn eigen woorden, en daaronder — indien nodig — één korte, warme vervolgvraag ("Wat voor sfeer heeft u voor ogen: eerder ingetogen of juist uitgesproken?").
- **Doet:** antwoordt vrij; kan meerdere berichten sturen.
- *Component:* Conversation Planner (bouwt de visie, laag 1) + Context Interpreter (leidt óók de projectfeiten af, laag 2) — **één** interpretatie per beurt.
- **Bevestiging:** nog geen; de Dessinator vat pas samen als er genoeg is.
- **Zichtbaar:** de groeiende "begrepen kern" in mensentaal (sfeer, gewenste uitstraling, type ruimte). **Verborgen:** dat dit twee modellagen vult; alle veldnamen/zekerheden.

**Stap 2 — Visie bevestigen**
- **Ziet:** een korte samenvatting: *"U wilt een rustige, warme vloer voor de lobby van een boutique hotel — klopt dat?"*
- **Doet:** bevestigt, of stuurt bij in woorden.
- *Component:* de architect zet de visie vast (bevestig-visie).
- **Bevestiging:** **de visie** (mijlpaal 1).
- **Verborgen:** dat de visie hierna onaantastbaar/read-only wordt.

**Stap 3 — Ontwerprichting (strategie + concept)**
- **Ziet:** een korte, professioneel geformuleerde ontwerprichting ("Een ingetogen, organische lijn met natuurlijke tinten past bij deze rust") en een **eerste sfeerbeeld**: kleurpalet + stijlkarakter.
- **Doet:** herkent, bevestigt, of nuanceert.
- *Component:* Ontwerpstrategie-stap (laag 3) → Reasoning Engine vormt het Concept (laag 4).
- **Bevestiging:** **de ontwerpstrategie** (mijlpaal 2) en **het concept** (mijlpaal 3) — voor de gebruiker voelt dit als één natuurlijke "ja, deze richting".
- **Zichtbaar:** kleurpalet, stijlkarakter, gewenste complexiteit in beeld. **Verborgen:** dat strategie en concept twee aparte bevestigingen zijn en dat de een de ander poort.

**Stap 4 — Vorm kiezen (Floor Design)**
- **Ziet:** één herkenbare ontwerprichting om op te reageren (en desgewenst enkele varianten).
- **Doet:** kiest er één (of vraagt om een alternatief).
- *Component:* Reasoning Engine (Floor Designs).
- **Bevestiging:** **het floor design** (mijlpaal 4).
- **Zichtbaar:** de gekozen richting met korte motivering. **Verborgen:** dat dit een resultaat-object buiten het model is.

**Stap 5 — Materiaal**
- **Ziet:** een voorgesteld materiaalkarakter in gewone woorden ("een zachte, laagpolige wol met een warme uitstraling") — met, waar zinvol, een tactiel/visueel accent in het beeld.
- **Doet:** bevestigt of kiest een ander voorstel.
- *Component:* Material Planner.
- **Bevestiging:** **het materiaal** (mijlpaal 5).

**Stap 5b — De ruimte kiezen**
- **Ziet:** een uitnodiging om de ruimte te kiezen waarin hij het resultaat wil zien — een van enkele voorbeeldruimtes óf een eigen foto van de werkelijke ruimte.
- **Doet:** kiest een voorbeeldruimte of uploadt een foto en zet (indien nodig) kort de vloerhoeken vast.
- *Component:* de bestaande Scene Builder (`/scene-builder`, `/api/scenes`) — read-only door de Floor Visualization Engine gebruikt.
- **Bevestiging:** geen ontwerpmijlpaal; een praktische keuze die het eindbeeld mogelijk maakt.
- **Verborgen:** dat dit een aparte Scene is met een gekalibreerd vloerpolygon. *(Dit kan al eerder in de reis, maar uiterlijk vóór het eerste beeld in de ruimte.)*

**Stap 6 — Patroon → eerste echte dessin**
- **Ziet:** het **daadwerkelijke dessin** verschijnt (het patroon, gerenderd), eerst als staal en direct daarna **in de gekozen ruimte** (mockup).
- **Doet:** bevestigt of laat het patroon bijstellen (schaal, dichtheid).
- *Component:* Pattern Planner → SVG Planner (productie-pipeline) → Floor Visualization Engine (met de in stap 5b gekozen ruimte).
- **Bevestiging:** **het patroon** (mijlpaal 6).
- **Zichtbaar:** het dessin en het dessin-in-de-ruimte. **Verborgen:** dat hier meerdere componenten samenwerken.

**Stap 7 — Afronden**
- **Ziet:** het eindbeeld in de ruimte + een heldere samenvatting van alle keuzes.
- **Doet:** verklaart zich tevreden ("Dit is 'm").
- *Component:* Design Transfer Package.
- **Bevestiging:** **het eindontwerp** (mijlpaal 7) → overdracht naar DCOD.

## 3. De conversatie (toon en ritme)

Geen chatbot, geen technisch jargon, geen eindeloze vragenlijst — maar een **meedenkende vakgenoot**:

- **Zo min mogelijk vragen.** Er wordt alleen gevraagd wat het ontwerp aantoonbaar verder helpt (BUILD-005). Wat al blijkt uit de woorden van de gebruiker, wordt niet nagevraagd.
- **Uitnodigend, niet instruerend.** *"Zullen we voor deze lobby een wat warmere ondertoon aanhouden?"* — niet: *"Kies een kleur."*
- **Terugkoppelen in beeld en taal.** Elke bevestiging is een kort, herkenbaar moment ("Klopt dit beeld?"), nooit een technische status.
- **Voorstellen, nooit opleggen.** Elke suggestie is een voorstel dat de gebruiker kan overnemen, bijstellen of afwijzen.

**Voorbeeld-uitwisseling (indicatief):**
> **Gebruiker:** "Ik wil een rustige vloer voor de lobby van ons boutique hotel."
> **Dessinator:** "Fijn — een lobby zet meteen de toon. Zoekt u eerder ingetogen en natuurlijk, of mag het een uitgesproken statement zijn?"
> **Gebruiker:** "Ingetogen, warm, een beetje organisch."
> **Dessinator:** "Helder. Ik zie een rustige, warme vloer met een organische lijn voor uw hotellobby. Klopt dat beeld?" *(→ visie bevestigen)*

## 4. Visualisatie — wanneer verschijnt/vernieuwt het beeld

- **Eerste sfeerbeeld** (kleurpalet + stijlkarakter): zodra het **concept** is bevestigd — nog niet het echte dessin, wel de sfeer.
- **Eerste echte dessin** (het gerenderde patroon als staal): zodra het **patroon** tot een SVG is gerenderd.
- **Eerste beeld in de ruimte** (mockup): direct daarna, wanneer het dessin op de vloer van de in stap 5b gekozen ruimte (Scene Builder) wordt geprojecteerd.
- **Bij materiaalwijziging:** het materiaalkarakter verandert; omdat het patroon op het bevestigde materiaal voortbouwt, wordt het dessin opnieuw opgebouwd en het beeld ververst.
- **Bij patroonwijziging:** het dessin wordt opnieuw gerenderd en het ruimtebeeld ververst.
- **Bij een nieuw dessin (SVG):** het ruimtebeeld ververst automatisch (het oude beeld hoort niet meer bij het nieuwe dessin).
- **Bij een andere ruimte (mockup):** kiest de gebruiker een andere ruimte, dan wordt hetzelfde dessin in die nieuwe ruimte getoond.

Het beeld **loopt altijd mee met de laatst bevestigde keuze**; de gebruiker ziet nooit een beeld dat niet meer bij zijn keuzes hoort.

## 5. Bevestigingsmomenten (zeven mijlpalen)

Elk moment is voor de gebruiker één natuurlijke "ja"; technisch zijn het aparte bevestigingen, maar dat blijft verborgen. De architect bevestigt **altijd zelf** — de Dessinator vinkt niets voor hem af.

| # | Mijlpaal | Wat de gebruiker bevestigt |
|---|---|---|
| 1 | **Visie** | "Dit is de sfeer/uitstraling die ik wil." |
| 2 | **Ontwerpstrategie** | "Deze richting doet mijn wens recht." |
| 3 | **Concept** | "Dit stijl-/kleurkarakter klopt." |
| 4 | **Floor Design** | "Deze ontwerprichting kies ik." |
| 5 | **Materiaal** | "Dit materiaalkarakter past." |
| 6 | **Patroon** | "Dit dessin is het." |
| 7 | **Eindontwerp** | "Ik ben tevreden — draag over aan DCOD." |

Mijlpalen 2 en 3 worden in de beleving samengevoegd tot één "ja, deze richting"; onderliggend blijven het twee bevestigingen (strategie poort het concept).

## 6. Fouten en hulp

De Dessinator "faalt" nooit hard; hij begeleidt:

- **Ontbrekende informatie:** in plaats van een foutmelding stelt hij **één** gerichte vraag ("Om een passende richting te kiezen, mag ik vragen wat voor ruimte dit is?"). Geen technische term, geen lijst.
- **Botsende keuzes:** hij benoemt de spanning in mensentaal en laat de gebruiker beslissen ("Een druk patroon kan de rust die u zoekt in de weg zitten — wilt u het rustiger houden of juist dit accent?"). De Dessinator kiest nooit zelf.
- **Onvoldoende context:** hij vraagt niet door om het doorvragen, maar legt kort uit waaróm iets helpt ("Met een idee van de gewenste sfeer kan ik gerichter voorstellen"), en biedt een voorbeeld als opstap.
- **Terugstappen:** de gebruiker kan altijd een eerdere keuze heroverwegen; het beeld en de vervolgstappen passen zich aan.

## 7. UX-principes (expliciet vastgelegd)

- **Zo min mogelijk klikken:** één doorlopend gesprek; elke stap is een korte bevestiging of bijsturing, geen formulier.
- **Zo min mogelijk technische termen:** geen "laag", "profiel", "SVG", "status", "gate" — uitsluitend sfeer, stijl, materiaal, patroon, ruimte.
- **De gebruiker voelt zich begeleid:** de Dessinator neemt initiatief in het vragen én in het tonen van beeld, maar houdt het tempo van de gebruiker.
- **De AI beslist nooit zelfstandig:** elke uitkomst is een voorstel; niets wordt zonder bevestiging vastgelegd.
- **De architect blijft eigenaar van iedere ontwerpbeslissing:** elke mijlpaal wordt door de gebruiker (als architect) bevestigd; de Dessinator legt uitsluitend vast wat de gebruiker heeft goedgekeurd.

## 8. Eindscherm

Nadat de gebruiker tevreden is, verschijnt één rustig, compleet overzicht:

- **Visualisatie:** het eindontwerp getoond in de gekozen ruimte (en desgewenst als staal), groot en centraal.
- **Samenvatting:** alle keuzes in gewone taal — sfeer/visie, ontwerprichting, materiaalkarakter, patroon — als een leesbaar ontwerpverhaal, niet als parameterlijst.
- **Design Transfer Package:** de bevestiging dat het volledige ontwerp is gebundeld voor DCOD; de gebruiker ziet *wat* wordt overgedragen (visie, ontwerp, materiaal, beeld), niet het technische formaat.
- **Vervolgstappen richting DCOD:** een heldere afsluiting ("DCOD ontvangt uw ontwerp en neemt contact op voor de uitvoering"). Nadrukkelijk **geen** bestelling of prijs — de overdracht is een aanzet tot het bestaande DCOD-proces, geen afrekening (BUILD-007).

## 9. Consistentietoets

- **Geen nieuwe component:** de UX map t volledig op de bestaande Design Brain-componenten en de bestaande `/api/design-brain`-endpoints; er wordt niets nieuws bedacht.
- **Geen bestaande component gewijzigd:** de UX vraagt geen enkele wijziging aan de Design Brain, de pipeline, de Scene Builder of `/api/generate`.
- **Past binnen BUILD-007:** de vijf fasen en zeven mijlpalen zijn exact de BUILD-007-workflow (visie → strategie → concept → floor design → materiaal → patroon → visualisatie → overdracht).
- **Past binnen BUILD-019:** elke gebruikersstap correspondeert met een bestaand endpoint (gesprek starten, dialoog, bevestig-visie, ontwerpstrategie, bevestig-strategie, concept, bevestig-concept, floor-designs, bevestig-floor-design, material-profiles, bevestig-material-profile, pattern-profiles, bevestig-pattern-profile, svg, visualisatie, transfer-package, status); de ruimtekeuze (stap 5b) gebruikt de bestaande Scene Builder-routes (`/api/scenes`).
- **Past binnen de huidige Design Brain:** de "AI beslist nooit zelf / architect bevestigt altijd"-regel is exact de bestaande gate-/bevestigingsarchitectuur (BUILD-008/AR-007).

---

**Reviewgereed:** dit document beschrijft uitsluitend de gebruikerservaring — reis, stappen, dialoog, visualisatie-timing, bevestigingsmomenten, foutbegeleiding, principes en eindscherm — volledig passend op de bestaande Design Brain en endpoints, zonder nieuwe of gewijzigde componenten. Het vormt de basis voor een later technisch UX-/frontend-ontwerp (bewust hier nog niet uitgewerkt).
