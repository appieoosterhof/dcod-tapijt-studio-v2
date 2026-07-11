# BUILD-005 — Conversation Planner: functioneel ontwerp

**Status:** functioneel ontwerp, ter review. Geen technisch ontwerp, geen implementatie, geen commit. Bouwt voort op `BUILD-005_CONVERSATION_PLANNER_ONTWERPPRINCIPE.md` (architectuurbesluit) en op de werkende BUILD-004-implementatie (`design_context.py`, `context_interpreter.py`).

**Doelzin:** *De Dessinator leert doorvragen.*

---

## 1. Doel

BUILD-004 levert losse, voorgestelde interpretaties op — elk met een eigen mate van zekerheid, maar zonder dat er iets gebeurt met de vraag "en wat nu?". De Conversation Planner is de stap die van een verzameling interpretaties een lopend, natuurlijk gesprek maakt: hij bepaalt telkens wat de meest waardevolle volgende interactie is, zodat het gesprek vooruitgaat zonder de architect te overladen met vragen die niet nodig zijn.

## 2. Verantwoordelijkheid

De Conversation Planner heeft precies één verantwoordelijkheid: **de meest waardevolle volgende interactie bepalen.**

Dit betekent expliciet niet:

- zelf informatie interpreteren (dat blijft de Context Interpreter);
- zelf ontwerpbeslissingen nemen of bevestigen (dat blijft de architect, of de gezamenlijke dialoog tussen architect en DCOD bij Ontwerpstrategie);
- een ontwerpstudie zelf uitvoeren (alleen bepalen of het moment daarvoor is aangebroken).

Conform het architectuurprincipe uit BUILD-004 (hoofdstuk 0 van het technisch ontwerp) is ook de Conversation Planner een AI-component: hij produceert een interpretatie van "wat nu het beste is", nooit een waarheid. Zijn keuze is zelf ook een voorstel, geen beslissing.

## 3. Input

- **DesignContext** — de huidige stand van alle lagen.
- **Interpretaties inclusief mate van zekerheid** — `DesignContext.interpretaties`, zoals BUILD-004 deze al oplevert.
- **Gespreksgeschiedenis** — de reeds gevoerde interacties binnen het project. Geen laag van het DesignContext Model; een contextbron die uitsluitend door de Conversation Planner wordt gebruikt (zie hoofdstuk 8).
- **Projectfase** — geeft aan waar het project zich bevindt binnen het ontwerptraject. Eveneens geen laag van het DesignContext Model, en eveneens uitsluitend gebruikt door de Conversation Planner (zie hoofdstuk 8).

## 4. Verwerking

De planner doorloopt bij elke aanroep dezelfde, vaste beslisvolgorde:

1. **Is de context voldoende?** Beoordeelt of er, over de relevante velden van Project-/Ruimtecontext en Ontwerpvisie heen, genoeg is voorgesteld om iets zinnigs te doen — niet elk veld hoeft gevuld te zijn, maar een te dunne context levert geen zinvolle vervolgstap op.
2. **Is bevestiging nodig?** Beoordeelt of er interpretaties zijn die belangrijk genoeg zijn om niet ongemerkt "voorgesteld" te blijven — bijvoorbeeld interpretaties met een lagere mate van zekerheid die het vervolg sterk beïnvloeden.
3. **Kan een eerste ontwerpstudie verantwoord worden voorgesteld?** Alleen wanneer de context zowel voldoende (stap 1) als voldoende bevestigd is (stap 2 al doorlopen en positief), is er ruimte om een ontwerpstudie voor te stellen. De planner start nooit zelfstandig een ontwerpstudie — hij stelt uitsluitend voor.

Deze drie stappen bepalen samen, in vaste volgorde, welke van de drie mogelijke uitkomsten wordt gekozen: onvoldoende context → gerichte vraag; voldoende context maar onbevestigd → samenvatting ter bevestiging; voldoende én bevestigd → voorstel tot een eerste ontwerpstudie.

## 5. Output

De planner kiest **exact één** vervolgstap:

- **Eén gerichte vraag** — kort, in de vorm van een uitnodiging, niet als instructie (conform de communicatieregel uit SPEC-000, hoofdstuk 10).
- **Een korte samenvatting ter bevestiging** — een weergave van de huidige interpretatie die de architect kan bevestigen, aanpassen of afwijzen; zelf geen ontwerpvoorstel, maar een controlemoment.
- **Een voorstel om een eerste ontwerpstudie te starten** — de Conversation Planner stelt voor, hij start nooit zelfstandig. Dit sluit aan op het architectuurprincipe dat AI-componenten interpretaties en voorstellen doen, geen definitieve beslissingen nemen.

Nooit nul vervolgstappen, nooit meerdere tegelijk.

## 6. Acceptatiecriteria

- Bij elke aanroep wordt precies één vervolgstap gekozen — nooit geen, nooit meerdere.
- De drie beslisstappen (context voldoende / bevestiging nodig / ontwerpstudie verantwoord) worden altijd in dezelfde vaste volgorde doorlopen.
- Er wordt nooit een vraag gesteld over een gegeven waarvoor al een interpretatie met voldoende zekerheid bestaat.
- De planner bevestigt of beslist zelf niets — elke uitkomst is een voorstel, conform het architectuurprincipe "iedere AI-component produceert interpretaties, nooit waarheden" (BUILD-004).
- Eenzelfde DesignContext-toestand levert een consistente, herleidbare keuze op (geen willekeurige variatie tussen twee aanroepen op identieke input).

## 7. Definition of Done

BUILD-005 (functioneel niveau) wordt als afgerond beschouwd wanneer:

- ✓ de drie beslisstappen zijn eenduidig gedefinieerd, inclusief wat "voldoende context" en "bevestiging nodig" concreet betekenen;
- ✓ voor elke DesignContext-toestand levert de planner precies één van de drie vervolgstappen op, nooit nul of meerdere;
- ✓ geen enkele vervolgstap impliceert dat de planner zelf een ontwerpbeslissing bevestigt of neemt;
- ✓ gespreksgeschiedenis en projectfase worden consistent behandeld als contextbronnen buiten het DesignContext Model (opgehelderd na review, zie hoofdstuk 8);
- ✓ elke output rond een ontwerpstudie is consequent geformuleerd als voorstel, nooit als zelfstandige start (opgehelderd na review, zie hoofdstuk 8).

## 8. Afbakening

**Niet opgenomen in BUILD-005:**

- Het daadwerkelijk voeren van de dialoog/chatinterface met de architect.
- Het daadwerkelijk uitvoeren van een ontwerpstudie — Ontwerpstudies zijn, conform SPEC-000, een eigen concept ("een mogelijke ontwerprichting binnen een project... kan meerdere varianten bevatten"); BUILD-005 bepaalt alleen of het moment daarvoor is aangebroken.
- Wijzigingen aan de Context Interpreter of aan de bestaande `/api/generate`-flow.
- Enige koppeling aan de gebruikersinterface.

**"Voorstellen" in plaats van "starten" (opgehelderd na review):**

De opdracht noemde als derde mogelijke output aanvankelijk letterlijk *"Start een eerste ontwerpstudie"*, terwijl het ontwerpprincipe-document dezelfde uitkomst omschreef als *"het voorstel om een eerste ontwerpstudie te starten"*. Dit is expliciet opgehelderd: **de Conversation Planner stelt voor om een eerste ontwerpstudie te starten — hij start nooit zelfstandig.** Dit sluit aan op het architectuurprincipe dat AI-componenten interpretaties en voorstellen doen, maar geen definitieve beslissingen nemen. Deze formulering is consequent doorgevoerd in hoofdstuk 4 en 5.

**Gespreksgeschiedenis en Projectfase (opgehelderd na review):**

Beide zijn geen nieuwe lagen binnen het DesignContext Model. Het zijn contextbronnen die uitsluitend door de Conversation Planner worden gebruikt, niet onderdeel van de DesignContext zelf:

- **Gespreksgeschiedenis** bevat de reeds gevoerde interacties binnen het project.
- **Projectfase** geeft aan waar het project zich bevindt binnen het ontwerptraject.

Deze informatie ondersteunt de planner bij het bepalen van de meest waardevolle volgende interactie, maar wordt niet vastgelegd als DesignContext-laag en raakt daarmee ook geen van de bestaande, bevroren lagen (Ontwerpvisie, Project-/Ruimtecontext, Ontwerpstrategie, Concept, Materialisatie, Productierealisatie, Ontwerpredenering).
