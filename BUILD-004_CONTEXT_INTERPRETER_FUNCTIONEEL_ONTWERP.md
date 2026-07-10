# BUILD-004 — Context Interpreter: functioneel ontwerp

**Status:** functioneel ontwerp, ter review. Geen implementatie, geen technisch BUILD-plan, geen commit. Eerste implementatiestap onder de architectuur van SPEC-000, gebaseerd op de "Context Interpreter"-component uit `DESIGN_BRAIN_ARCHITECTUURVISIE.md`.

---

## 1. Doel

Van een vrij gesprek met de architect naar een gestructureerde, herbruikbare Projectcontext — zodat latere stappen in de Dessinator (Ontwerpstrategie, Concept, Materialisatie) niet zelf de ruwe tekst hoeven te herinterpreteren, en zodat zichtbaar wordt welke informatie al aanwezig is en welke nog ontbreekt.

## 2. Verantwoordelijkheid

De Context Interpreter heeft precies één verantwoordelijkheid: **de projectcontext uit een gesprek begrijpen en structureren.**

Dit betekent concreet:

- interpreteren wat de architect al heeft verteld, ook wanneer dat impliciet of verspreid over meerdere zinnen is;
- dat structureren in de juiste laag van het DesignContext Model, als voorgestelde interpretaties;
- elke interpretatie, waar van toepassing, voorzien van een eigen mate van zekerheid.

**De Context Interpreter stelt zelf geen vragen.** De verantwoordelijkheid voor het kiezen, formuleren en timen van vragen ligt volledig bij de Conversation Planner — een apart onderdeel van de Design Brain (zie `DESIGN_BRAIN_ARCHITECTUURVISIE.md`). De Context Interpreter levert die component uitsluitend het signaal (welke informatie ontbreekt); de Conversation Planner bepaalt wat daarmee gebeurt.

De Context Interpreter neemt geen ontwerpbeslissingen en bevestigt niets definitief — dat blijft, conform SPEC-000 (hoofdstuk 7, Governance) en het eigenaarschapsprincipe uit `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, voorbehouden aan de architect zelf of aan de gezamenlijke dialoog tussen architect en DCOD.

## 3. Input

- Vrije tekst van de gebruiker (de beschrijving van het project, in eigen woorden).
- Eventuele basisprojectgegevens die al bekend zijn (bijvoorbeeld via de bestaande inspiratie-flow: een gekozen projecttype of startconcept).

## 4. Verwerking

De Context Interpreter:

1. Leest de beschikbare vrije tekst en eventuele basisprojectgegevens.
2. Herkent welke van de outputvelden (zie hieronder) daarin al — expliciet of impliciet — aanwezig zijn. Deze herkenning kan informatie uit meerdere lagen van het DesignContext Model tegelijk bevatten (bijvoorbeeld zowel projectfeiten als een sfeeraanduiding in dezelfde zin).
3. Brengt elke herkenning onder als een voorgestelde interpretatie in de **juiste laag** van het DesignContext Model — niet alles in één ongedifferentieerde Projectcontext, maar Project-/Ruimtecontext (laag 2) en Ontwerpvisie (laag 1) gescheiden gehouden, zoals hieronder bij Output gespecificeerd.
4. Geeft elke interpretatie, waar van toepassing, een eigen mate van zekerheid mee. Voor een gegeven waarvoor onvoldoende basis in de input aanwezig is, wordt eenvoudigweg geen interpretatie geleverd — er wordt niets geraden en niets stilzwijgend leeg gelaten.

De Context Interpreter **stelt zelf geen vragen**. Het ontbreken van een interpretatie voor een verwacht gegeven, of een interpretatie met een lage mate van zekerheid, is het signaal waarop een ander onderdeel kan voortbouwen. Die verantwoordelijkheid ligt volledig bij de Conversation Planner (zie hoofdstuk 2 en 7).

## 5. Output

De Context Interpreter levert een verzameling **voorgestelde interpretaties**. Elke interpretatie betreft precies één herkend gegeven, wordt ondergebracht in de juiste laag van het DesignContext Model, en krijgt — waar van toepassing — een eigen **mate van zekerheid** mee. Zekerheid is daarmee een eigenschap van de afzonderlijke interpretatie, niet van de DesignContext zelf en niet van een apart "onzekerheden"-veld.

Mogelijke interpretaties, per laag:

**Project-/Ruimtecontext (laag 2)**
- Projecttype
- Ruimtetype
- Doelgroep
- Functionele eisen
- Bijzondere randvoorwaarden

**Ontwerpvisie (laag 1)**
- Gewenste beleving
- Gewenste identiteit
- Ontwerpambitie

Voor een gegeven waarvoor onvoldoende basis in de input aanwezig is, levert de Context Interpreter eenvoudigweg geen interpretatie. Het ontbreken van een interpretatie — of een interpretatie met een lage mate van zekerheid — is zelf het signaal dat iets nog niet vaststaat; er is geen apart veld voor nodig.

Elke interpretatie heeft de status **voorgesteld**, nooit **bevestigd** — conform de status-indeling uit het DesignContext Model. Bevestiging is en blijft een handeling van de architect, niet van de Context Interpreter.

## 6. Acceptatiecriteria

- Voor een gegeven vrije tekst levert de Context Interpreter uitsluitend interpretaties die daadwerkelijk herleidbaar zijn tot die tekst (of de basisprojectgegevens) — hij verzint geen interpretaties zonder basis in de input.
- Elke interpretatie wordt in de juiste laag van het DesignContext Model geplaatst (Project-/Ruimtecontext dan wel Ontwerpvisie) — nooit ongedifferentieerd in één verzamelstructuur.
- Elke interpretatie krijgt, waar van toepassing, een eigen mate van zekerheid mee; zekerheid is een eigenschap van de interpretatie, niet van een apart veld.
- Voor een gegeven zonder voldoende basis in de input wordt geen interpretatie geleverd — er wordt niets geraden.
- De output krijgt nooit de status "bevestigd" — alleen "voorgesteld".
- Bij dezelfde input levert de Context Interpreter een consistente, herleidbare set interpretaties op (geen willekeurige variatie tussen twee interpretaties van dezelfde tekst).
- De Context Interpreter genereert zelf geen vragen aan de architect — het ontbreken van een interpretatie, of een lage mate van zekerheid, is het signaal waarop de Conversation Planner voortbouwt.

## 7. Afbakening

**Niet opgenomen in BUILD-004:**

- SVG-generatie
- Design Brain (als geheel — de Context Interpreter is er één onderdeel van)
- Ontwerpstudies
- Materiaalkeuze
- Mock-ups
- Offertes

**Context Interpreter versus Conversation Planner (opgehelderd na review):**

De eerdere versie van dit ontwerp signaleerde een mogelijke overlap: de opdracht noemde onder "Belangrijk" zowel *"bepaalt welke informatie nog ontbreekt"* als *"stelt alleen vragen die werkelijk nodig zijn"* als eigenschap van de Context Interpreter, terwijl dat tweede punt in `DESIGN_BRAIN_ARCHITECTUURVISIE.md` al bij de Conversation Planner lag. Dit is expliciet opgehelderd: de Context Interpreter interpreteert, structureert en signaleert ontbrekende informatie; het kiezen, formuleren en timen van vragen ligt volledig bij de Conversation Planner. Deze scheiding is nu vastgesteld, niet langer een open signalering.

**Projectcontext versus Ontwerpvisie (opgehelderd na review):**

De eerdere versie signaleerde dat "Gewenste beleving" feitelijk bij Laag 1 (Ontwerpvisie) hoort, niet bij Laag 2 (Project-/Ruimtecontext), terwijl de opdracht dit ongedifferentieerd onder één "Projectcontext" schaarde. Dit is expliciet opgehelderd: de Context Interpreter mag informatie uit meerdere lagen herkennen, maar brengt deze onder in de juiste laag (zie hoofdstuk 5, Output). Deze laagtoewijzing is nu vastgesteld, niet langer een open signalering.

**Onzekerheid als eigenschap van de interpretatie, niet als apart veld (opgehelderd na review):**

Een eerdere versie van dit ontwerp modelleerde "Onzekerheden / ontbrekende informatie" nog als een zelfstandig outputveld, naast de DesignContext-velden. Naar aanleiding van een aparte architectuurdiscussie (vastgelegd in `BUILD-004_CONTEXT_INTERPRETER_TECHNISCH_ONTWERP.md`, hoofdstuk 0) is vastgesteld dat onzekerheid een eigenschap is van de interpretatie, niet van de data of van de DesignContext zelf. Dit functioneel ontwerp is daarop aangepast: de Context Interpreter levert voorgestelde interpretaties, elk met een eigen mate van zekerheid waar van toepassing; een apart "onzekerheden"-veld bestaat niet meer.
