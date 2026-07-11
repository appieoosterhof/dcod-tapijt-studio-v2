# BUILD-007 — De toekomstige Dessinator-workflow: functioneel ontwerp

**Status:** functioneel ontwerp op ervaringsniveau, ter review. Geen schermontwerpen, geen code, geen implementatievoorstellen. Beschrijft de gebruikerservaring vanuit de vastgestelde platformarchitectuur (VISION-001, SPEC-000, het DesignContext Model), niet vanuit de huidige interface — de huidige interface (inclusief BUILD-006) is een proof of concept, geen blauwdruk.

---

## Terminologie (vastgesteld na architectuurreview)

De volledige keten is: Project → Ontwerpvraag → DesignContext → Context Interpreter → Conversation Planner → Floor Design → Material Profile → Scene → Floor Visualization Engine → Visualisatie → Design Transfer Package → DCOD.

De onderstaande begrippen zijn geen hernoeming van bestaande BUILD-004/DesignContext Model-objecten, maar vertegenwoordigen een hoger architectuurniveau, ontstaan in VISION-001:

- **Ontwerpvraag** — de volledige vraag waarmee het ontwerpteam de Dessinator benadert. Geen alias voor Ontwerpvisie.
- **DesignContext** — blijft, ongewijzigd, het centrale domeinmodel **van de ontwerpfase** (SPEC-000, het bevroren DesignContext Model).
- **Floor Design** — het centrale domeinobject **ná de ontwerpfase**. Geen samenvoeging van Ontwerpstrategie en Concept, en geen tweede centraliteitsclaim naast DesignContext — een andere fase, een andere reikwijdte.
- **Material Profile** — de visuele en materiële eigenschappen van de gekozen vloerafwerking, gebruikt door de Floor Visualization Engine. Materialisatie (DesignContext Model, laag 5) blijft een eigenschap ván een ontwerp binnen de ontwerpfase; Material Profile is daarvan geen synoniem.
- **Design Transfer Package** — de overdracht van de ontwerpintentie aan DCOD's technische specialisten. Nadrukkelijk niet de opvolger van de bestaande offerte-/bestelfunctionaliteit — offerte, werkvoorbereiding en productie blijven aparte bedrijfsprocessen.

**DesignContext, Context Interpreter en Conversation Planner zijn interne platformfasen.** Ze horen in de architectuurketen thuis, maar zijn bewust geen eigen, zichtbare stap in de gebruikerservaring hieronder — de gebruiker ervaart het gesprek, niet de architectuur die het draagt.

---

## Het uitgangspunt dat de hele workflow stuurt

De Dessinator is niet een tool die een architect bedient, maar **de digitale vloerexpert binnen het ontwerpteam** — een rol, geen interface. Net zoals een ervaren DCOD-adviseur aan tafel niet met een intakeformulier begint, begint de Dessinator niet met velden, maar met een gesprek. Alles hieronder is een poging om te beschrijven hoe dat gesprek natuurlijk aanvoelt, terwijl er onder water een volledige, gestructureerde architectuur meeloopt die de architect nooit hoeft te zien tenzij hij erom vraagt.

Drie principes lopen door elke fase heen en worden daarom niet steeds herhaald: **complexiteit alleen tonen wanneer nodig**, **eenvoudig aan de voorkant, intelligent aan de achterkant**, en **de architect blijft altijd eigenaar van elke beslissing** (conform SPEC-000, De Gouden Regel).

---

## De workflow

### 1. Project

De ervaring begint niet met een schoon scherm, maar met een vraag die een goede adviseur ook als eerste zou stellen: *voor welk project is dit?* Dat kan een geheel nieuw project zijn, of het hervatten van een lopend gesprek. Op dit niveau wordt nog niets over vloeren gevraagd — alleen de context waarbinnen het gesprek gaat plaatsvinden. Voor een architect die net begint voelt dit als het openen van een dossier, niet als een formulier invullen.

### 2. Ontwerpvraag

Hier krijgt de architect het woord, in zijn eigen taal. Geen stijlkeuze, geen vragenlijst — een open uitnodiging om te vertellen wat hij voor ogen heeft, desgewenst geholpen door herkenbare voorbeeldvisies (zoals eerder vastgesteld in DISCOVERY-004) als hij nog geen woorden heeft. Dit is het enige moment in de hele workflow waarop de Dessinator bewust niets terugzegt behalve "ik luister" — de intelligentie zit in wat er hierna gebeurt, niet hier.

### 3. Van vraag naar begrip

Dit gebeurt onzichtbaar. De architect merkt niet dat zijn woorden worden geïnterpreteerd — hij merkt alleen het resultaat: de Dessinator lijkt te *begrijpen* wat hij bedoelt, zonder dat te hoeven bevestigen met een lijst technische velden.

Architectonisch zitten hier drie interne stappen achter elkaar, geen van alle zichtbaar voor de gebruiker: de Ontwerpvraag wordt vastgelegd in de **DesignContext** (het domeinmodel van de ontwerpfase); de **Context Interpreter** verrijkt die DesignContext met interpretaties — wat is er gezegd, in welke laag hoort het, hoe zeker is die lezing; en de **Conversation Planner** leest die interpretaties en bepaalt wat het gesprek nu het beste kan doen. Voor de architect vertaalt zich dat in precies één ervaring: soms een korte, gerichte vervolgvraag, soms een samenvatting ter bevestiging, en soms — wanneer er al genoeg vaststaat — helemaal niets, en gaat het gesprek vanzelf door naar Floor Design. Nooit meer dan nodig, nooit een vraag over iets dat al duidelijk was.

Dit is het punt waar "complexiteit alleen tonen wanneer nodig" voor het eerst concreet voelbaar wordt: een architect die alles al helder heeft aangegeven, komt deze fase bijna ongemerkt doorheen; een architect die nog zoekende is, krijgt meer begeleiding, zonder dat het als een ondervraging aanvoelt.

### 4. Floor Design

Hier verschijnt voor het eerst iets tastbaars: het Floor Design — het resultaat van de ontwerpfase, niet één definitief antwoord, maar een richting die de architect kan herkennen, bijstellen of afwijzen. Voor een architect die snel wil, is dit een enkel, herkenbaar ontwerp om op te reageren; voor wie wil verkennen, is er ruimte om varianten te zien.

### 5. Material Profile

Zodra de richting staat, verschuift het gesprek van "hoe ziet het eruit" naar "hoe voelt en presteert het". Ook hier geldt: dit is een voorstel, geen keuzemenu met tientallen opties tegelijk. De Dessinator brengt zijn materiaalkennis in — welke uitstraling, structuur en pooltype passen bij wat er al is vastgesteld — en de architect stuurt bij op wat voor de ruimte en het gebruik telt. Een architect die hier geen mening over heeft, hoeft er niet doorheen te klikken; een architect die dit juist belangrijk vindt, kan er dieper op ingaan.

### 6. Scene

Dit is waar het ontwerp een plek krijgt. Niet als aparte, technische stap ("upload nu een foto en kalibreer"), maar als een vraag die past bij het gesprek: *in welke ruimte moet ik dit voor je laten zien?* Dat kan een kant-en-klare DCOD-scene zijn, een eigen projectfoto, of een 3D-impressie — de architect voelt het verschil niet in hoe hij die ruimte aanlevert, alleen in wat hij vervolgens ziet. De techniek die dit mogelijk maakt (BUILD-006) blijft volledig achter de schermen; wat de architect ervaart is simpelweg "mijn ruimte", niet "een gekalibreerde polygon".

### 7. Floor Visualization Engine

Ook dit is onzichtbaar werk — de plek waar het Floor Design, het Material Profile en de Scene samenkomen tot één beeld. De architect ervaart dit niet als een aparte stap; hij ervaart alleen dat het volgende dat hij ziet klopt.

### 8. Visualisatie

Het eerste échte "wow"-moment: de vloer, in de eigen ruimte, met het gekozen materiaal, alsof het al ligt. Dit is het moment waarop het gesprek even stilvalt — niet omdat er niets meer te doen is, maar omdat de architect nu kan *kijken* in plaats van *beschrijven*. Vanaf hier kan het gesprek weer terug (een andere richting, een ander materiaal, een andere ruimte) zonder dat eerdere stappen overnieuw hoeven — precies zoals een goed gesprek met een adviseur nooit terug naar het begin hoeft, alleen naar het punt waar iets bijgesteld moet worden.

### 9. Design Transfer Package

Wanneer de architect tevreden is, verandert de rol van de Dessinator van ontwerpgesprek naar overdracht: alles wat is vastgesteld — de visie, het Floor Design, het Material Profile, de visualisatie — wordt gebundeld tot iets dat DCOD direct kan oppakken. Voor de architect voelt dit als het afronden van het gesprek, niet als het invullen van een nieuw formulier: wat hij al heeft besproken en bevestigd, hoeft hij niet nog eens te herhalen.

### 10. DCOD

Het pakket komt aan bij een mens, niet bij een systeem dat opnieuw begint. Alles wat de architect en de Dessinator samen hebben vastgesteld is direct bruikbaar voor het vervolg — offerte, productie, of verdere afstemming.

---

## Wat dit ontwerp niet is

Dit document beschrijft de ervaring en de volgorde, geen schermen, geen componentnamen, geen technische keuzes. De architectuur die dit mogelijk maakt (DesignContext Model, Floor Visualization Platform) bepaalt wát er kan gebeuren; dit document beschrijft alleen hoe dat voor de architect *voelt*. De vertaalslag naar concrete interfaces, technische componenten en implementatie is nadrukkelijk een latere, aparte stap.
