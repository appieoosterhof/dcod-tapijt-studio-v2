# BUILD-005 — Conversation Planner: leidend ontwerpprincipe

**Status:** architectuurbesluit vastgesteld. Nog geen functioneel ontwerp, nog geen technisch ontwerp, nog geen implementatie. Uitgangspunt voor de Conversation Planner — het onderdeel van de Design Brain dat, zoals vastgesteld bij BUILD-004, verantwoordelijk is voor het kiezen, formuleren en timen van vragen aan de architect. *(Deze positionering onder Design Brain is open architectuurvraag AV-001, vastgelegd in `OPEN_ARCHITECTUURVRAGEN.md` — gehandhaafd tot een expliciet besluit, geen vaststaand gegeven.)*

---

## Leidend principe

> **De DCOD Dessinator gedraagt zich als een ervaren ontwerpcollega die op het juiste moment de juiste vraag stelt, zonder ooit op de stoel van de ontwerper te gaan zitten.**

## Ontwerpregels

- Stel zo min mogelijk vragen.
- Stel alleen vragen die het ontwerp aantoonbaar verder helpen.
- Vraag nooit naar informatie die al bekend is of logisch kan worden afgeleid.
- De vraag moet de ontwerper helpen beter te ontwerpen, niet meer werk te geven.
- De ontwerper blijft altijd eigenaar van alle ontwerpbeslissingen.

## Aanvullend ontwerpprincipe: vraagkwaliteit

> **Een goede vraag opent ontwerpvrijheid; een slechte vraag beperkt die.**

### Uitwerking

De Conversation Planner bepaalt de volgende vraag op basis van twee informatiebronnen:

1. De huidige **DesignContext** (wat al bekend is).
2. De **gesprekscontext** (wat al besproken is).

Voordat een vraag wordt gesteld, toetst de Conversation Planner deze aan vier criteria:

1. Is deze informatie echt nodig?
2. Kan deze informatie al worden afgeleid?
3. Helpt deze vraag het ontwerp aantoonbaar verder?
4. Is dit het juiste moment om deze vraag te stellen?

Alleen wanneer aan deze criteria wordt voldaan, wordt de vraag gesteld.

## Aanvullend ontwerpprincipe: de vervolgstap is niet altijd een vraag

> **De beste volgende stap is niet altijd een vraag. Soms is het een samenvatting of een eerste ontwerpstudie.**

### Mogelijke uitkomsten van de Conversation Planner

De planner bepaalt de meest waardevolle vervolgstap. Dat kan zijn:

1. ❓ Een gerichte vervolgvraag.
2. 💬 Een samenvatting ter bevestiging van de huidige interpretatie.
3. 🎨 Het voorstel om een eerste ontwerpstudie te starten wanneer de context voldoende compleet is.

### Open punt: naamgeving

De naam **Conversation Planner** blijft voorlopig gehandhaafd. Tijdens BUILD-005 wordt onderzocht of deze naam de verantwoordelijkheid nog volledig dekt — nu duidelijk is dat de vervolgstap niet altijd een vraag is — of dat een bredere benaming beter past. Nog geen besluit hierover.

## Verhouding tot eerder vastgestelde principes

Dit uitgangspunt staat niet op zichzelf, maar sluit direct aan bij wat al eerder is vastgesteld:

- **DISCOVERY-004**: *"De Dessinator genereert geen vragen omdat informatie ontbreekt. De Dessinator genereert alleen vragen wanneer de kwaliteit van het uiteindelijke ontwerp daardoor aantoonbaar verbetert."* — dezelfde regel, hier specifiek toegepast op de Conversation Planner.
- **BUILD-004**: de Context Interpreter levert per interpretatie een mate van zekerheid, en stelt zelf nooit vragen. De regel *"vraag nooit naar informatie die al bekend is of logisch kan worden afgeleid"* is daarmee direct uitvoerbaar: de Conversation Planner heeft al het materiaal (interpretaties mét zekerheid) om te bepalen wat al voldoende zeker is en dus geen vraag behoeft.
- **SPEC-000, De Gouden Regel**: *"Helpt deze functie de architect een betere ontwerpbeslissing te nemen, zonder de rol van ontwerper over te nemen?"* — dit BUILD-005-principe is een concrete toepassing van diezelfde regel op vraagformulering specifiek.

Geen van deze eerdere principes wordt door dit besluit gewijzigd; dit maakt ze specifiek voor de Conversation Planner.

## Status

Vastgesteld als uitgangspunt. Functioneel ontwerp, technisch ontwerp en implementatie van BUILD-005 volgen in latere, aparte stappen.
