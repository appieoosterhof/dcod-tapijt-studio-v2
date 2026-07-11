# Open architectuurvragen

**Status:** het centrale register voor alle expliciet openstaande architectuurvragen. Dit zijn geen signaleringen binnen één BUILD, maar vragen die een aparte architectuurreview vereisen, los van de BUILD of het SPEC-document waarin ze naar boven kwamen. Zolang een vraag hier openstaat, geldt: huidige positionering handhaven, geen architectuurwijzigingen doorvoeren.

Bestaande en toekomstige BUILD- en SPEC-documenten bevatten zelf geen losse open architectuurvragen meer — uitsluitend een verwijzing hierheen.

---

## Vaste structuur per vraag

Elke vraag in dit register volgt dezelfde opbouw:

- **ID** — uniek volgnummer.
- **Titel** — korte, herkenbare naam.
- **Ontstaan in** — het document/de BUILD waarin de vraag naar boven kwam.
- **Vraag** — de exacte onderzoeksvraag.
- **Waarom nog open** — waarom dit niet terloops kan worden besloten.
- **Impact** — welke documenten/componenten hiervan afhangen.
- **Status** — open / in review / besloten.
- **Besluit** — leeg totdat er een expliciet besluit is; daarna het besluit zelf plus verwijzing naar waar het is vastgelegd.

---

## AV-001 — Conversation Planner: Project Brain of Design Brain?

- **ID:** AV-001
- **Titel:** Positionering van de Conversation Planner binnen Project Brain of Design Brain
- **Ontstaan in:** BUILD-005 (Conversation Planner, technisch ontwerp), naar aanleiding van de canonieke Project Brain/Design Brain-definitie.
- **Vraag:** Is de Conversation Planner een procescomponent van de Project Brain die bepaalt wanneer de Design Brain wordt ingezet, of is de Conversation Planner zelf onderdeel van de Design Brain?
- **Waarom nog open:** de Design Brain is de ontwerpintelligentie binnen de Project Brain (ondersteunt ontwerpdenken en ontwerpredenering); de Project Brain is de bovenliggende architectuur die het volledige projectproces beheert. `DESIGN_BRAIN_ARCHITECTUURVISIE.md` positioneerde de Conversation Planner oorspronkelijk als Design Brain-component, vóórdat deze hiërarchie werd vastgesteld. De Conversation Planner beslist over interactietiming, niet rechtstreeks over ontwerpinhoud — wat net zo goed een Project Brain-verantwoordelijkheid zou kunnen zijn.
- **Impact:** `BUILD-005_CONVERSATION_PLANNER_ONTWERPPRINCIPE.md`, `BUILD-005_CONVERSATION_PLANNER_FUNCTIONEEL_ONTWERP.md`, `BUILD-005_CONVERSATION_PLANNER_TECHNISCH_ONTWERP.md`, en mogelijk `DESIGN_BRAIN_ARCHITECTUURVISIE.md`.
- **Status:** open.
- **Besluit:** —

## AV-002 — Reikwijdte van "AI produceert interpretaties, nooit waarheden" naar SPEC-000

- **ID:** AV-002
- **Titel:** Opname van het AI-interpretatieprincipe in SPEC-000
- **Ontstaan in:** BUILD-004 (Context Interpreter, technisch ontwerp), bij de vaststelling van het architectuurprincipe "Iedere AI-component binnen de DCOD Dessinator produceert interpretaties, nooit waarheden."
- **Vraag:** Moet dit principe, dat breder is dan BUILD-004 alleen, ook expliciet worden opgenomen in `SPEC-000_PROJECT_CHARTER.md` (met name hoofdstuk 6, Architectuurprincipes, en hoofdstuk 7, Governance)?
- **Waarom nog open:** het principe is voor BUILD-004 vastgesteld en toegepast, maar SPEC-000 is het bevroren fundament waarop alle andere documenten worden gepositioneerd — een wijziging daaraan is een aparte afweging, niet iets wat terloops bij een BUILD wordt meegenomen.
- **Impact:** `SPEC-000_PROJECT_CHARTER.md` (hoofdstuk 6 en 7).
- **Status:** in review — expliciet aangemerkt als kandidaat voor een toekomstige revisie van SPEC-000 (v1.1). Tot die revisie wordt SPEC-000 niet gewijzigd.
- **Besluit:** —
