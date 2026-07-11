# BUILD-005 — Conversation Planner: technisch ontwerp

**Status:** technisch ontwerp, ter review. Geen implementatie, geen commit. Bouwt voort op `BUILD-005_CONVERSATION_PLANNER_FUNCTIONEEL_ONTWERP.md` (functioneel gereed) en op de werkende BUILD-004-implementatie (`design_context.py`, `context_interpreter.py`).

---

## 1. Technische componenten

Het functioneel ontwerp maakt een onderscheid dat ook technisch moet worden doorgevoerd: **de beslissing** (welke van de drie uitkomsten) is iets anders dan **de formulering** (de daadwerkelijke tekst). Dat leidt tot twee technisch verschillende componenten binnen de Conversation Planner:

- **Beslislogica (deterministisch, geen AI-aanroep)** — doorloopt de drie vaste stappen uit het functioneel ontwerp (context voldoende? / bevestiging nodig? / ontwerpstudie verantwoord voor te stellen?) op basis van `DesignContext` en de meegeleverde interpretaties. Dit is regelgebaseerd, niet AI-gedreven: de vraag "is er genoeg bekend" is een controleerbare toets op aanwezige/afwezige velden en hun zekerheid, geen interpretatievraagstuk.
- **Formuleringslaag (AI-aanroep, zelfde patroon als BUILD-004)** — zodra de beslislogica heeft bepaald wélke uitkomst (vraag/samenvatting/voorstel), formuleert deze laag de daadwerkelijke, natuurlijke tekst — kort, uitnodigend, nooit instructief (SPEC-000, hoofdstuk 10). Dit vereist natuurlijke taal en dus, net als bij de Context Interpreter, een eigen, aparte AI-aanroep.

## 2. Gegevensstromen

```
DesignContext (incl. interpretaties, BUILD-004)
Gespreksgeschiedenis (extern, geen DesignContext-laag)
Projectfase (extern, geen DesignContext-laag)
        │
        ▼
Conversation Planner (nieuw, losstaand)
   │  1. Beslislogica: doorloopt de drie vaste stappen, bepaalt exact
   │     één uitkomsttype (deterministisch, geen AI-aanroep)
   │  2. Formuleringslaag: AI-aanroep die de gekozen uitkomst omzet
   │     in een korte, natuurlijke tekst
   ▼
Eén vervolgstap (type + tekst) -- status uitsluitend "voorgesteld"
   │
   ▼
   [buiten scope BUILD-005: chatinterface, daadwerkelijke ontwerpstudie]
```

Geen koppeling met de bestaande `/api/generate`-flow, dezelfde discipline als BUILD-004.

## 3. Interfaces

- **Input:** `DesignContext` (specifiek `ontwerpvisie`, `projectcontext`, `interpretaties`), plus gespreksgeschiedenis en projectfase als losse, externe gegevens (geen DesignContext-velden, conform het functioneel ontwerp).
- **Output:** één vervolgstap, bestaande uit een type (vraag / samenvatting / voorstel) en de geformuleerde tekst. Nooit een bevestigde status.
- **Interface naar Context Interpreter:** uitsluitend lezend — de Conversation Planner leest `DesignContext.interpretaties`, roept de Context Interpreter niet aan en wordt er niet door aangeroepen. Beide delen alleen dezelfde `DesignContext`-instantie, op dezelfde manier waarop BUILD-003 al aantoonde dat onafhankelijke componenten een gedeelde DesignContext kunnen gebruiken zonder elkaar te kennen.
- **Interface naar een toekomstige chatinterface:** niet gebouwd in BUILD-005, maar de output (type + tekst) moet bruikbaar zijn als weergave-eenheid voor een gesprek, zonder dat de Conversation Planner zelf iets van een interface hoeft te weten.

## 4. Relatie met BUILD-004

- De Conversation Planner **leest** `DesignContext.interpretaties` (met hun mate van zekerheid), maar **wijzigt** deze niet en voegt er niets aan toe.
- Context Interpreter en Conversation Planner blijven, zoals in het functioneel ontwerp vastgesteld, functioneel gescheiden en kennen elkaar niet — hetzelfde architectuurpatroon dat BUILD-003 al bewees voor `build_tile_svg()`/`build_repeat_svg()`, nu toegepast op twee Design Brain-componenten.

**Vervolgstap is geen Interpretatie (opgehelderd na review):** de output van de Conversation Planner ("dit is de volgende stap") is van een wezenlijk andere aard dan een `Interpretatie` (die specifiek een laag + veld van het DesignContext Model betreft, bijvoorbeeld `ontwerpvisie.sfeer`). Een vervolgstap gaat niet over een ontwerpveld, maar over het proces zelf, en hoort daarom niet thuis in het DesignContext Model. Deze keuze is bevestigd: de vervolgstap blijft een eigen, nieuwe structuur binnen de Conversation Planner-module zelf (zie hoofdstuk 5), geen `Interpretatie` en geen deel van `DesignContext`.

## 5. Nieuwe modules

- **Een nieuwe, losstaande Conversation Planner-module**, met dezelfde isolatiefilosofie als `design_context.py` en `context_interpreter.py`.
- **Een nieuwe, lokale datastructuur voor de vervolgstap** (type + tekst), gedefinieerd binnen de Conversation Planner-module zelf — niet in `design_context.py`, omdat een vervolgstap geen ontwerpkennis is maar procesbepaling (toegelicht in hoofdstuk 4).

**Gespreksgeschiedenis en projectfase: bewust nog abstract (geen architectuurbesluit).** Conform het functioneel ontwerp hebben deze bewust geen plek in het DesignContext Model. Een technische vorm is hier nadrukkelijk nog niet voor uitgewerkt: er wordt onderzocht of deze informatie uiteindelijk onderdeel wordt van een afzonderlijke sessielaag, mogelijk binnen de bredere DCOD Project Brain (het projectproces-omvattende geheel waar de Design Brain — en daarmee de Conversation Planner — één onderdeel van is; zie de canonieke definitie hieronder). Voor dit technisch ontwerp blijven beide daarom uitsluitend een **abstracte invoerbron** voor de Conversation Planner — een gegeven dat aanwezig verondersteld wordt, zonder vastgelegde structuur, totdat dat onderzoek is afgerond.

**Terminologie Project Brain / Design Brain (opgehelderd na review):**

> **DCOD Project Brain** — de bovenliggende architectuur van de DCOD Dessinator; beheert het volledige projectproces en omvat de verschillende functionele componenten van de Dessinator.
> **DCOD Design Brain** — de ontwerpintelligentie binnen de Project Brain; ondersteunt het ontwerpdenken en de ontwerpredenering, maar vormt slechts één onderdeel van de Project Brain.

Dit is nu canoniek vastgelegd. "Project Brain" en "Design Brain" zijn expliciet géén synoniemen.

**Open architectuurvraag AV-001** (buiten scope van BUILD-005, zie `OPEN_ARCHITECTUURVRAGEN.md`): is de Conversation Planner een procescomponent van de Project Brain die bepaalt wanneer de Design Brain wordt ingezet, of is de Conversation Planner zelf onderdeel van de Design Brain? Tot een expliciet besluit is genomen, handhaaft dit document de bestaande positionering (Conversation Planner als Design Brain-component) en worden hierop geen architectuurwijzigingen doorgevoerd.

## 6. Hergebruik van bestaande modules

- **`design_context.py`** — `DesignContext` en `Interpretatie` worden gelezen, niet gewijzigd. Geen uitbreiding van dit bestand nodig (in tegenstelling tot BUILD-004).
- **Het AI-aanroepmechaniek uit `context_interpreter.py`** (`_interpreteer_vrije_tekst()`-patroon: zelfde model, zelfde manier van JSON/tekst-afdwingen) als voorbeeld voor de formuleringslaag — niet de functie zelf hergebruiken, wel het bewezen patroon.
- **Dezelfde additieve-koppeling-discipline** uit BUILD-001B/Fase 2a en BUILD-004: geen wijziging aan bestaande, werkende code totdat bewust anders besloten wordt.

## 7. Migratie-impact op de huidige codebase

| Bestand | Impact |
|---|---|
| `app.py` | Geen wijziging. |
| `design_context.py` | **Geen wijziging.** De Conversation Planner leest uitsluitend; er wordt niets aan het domeinmodel toegevoegd. Dit is minder impact dan BUILD-004, dat wel additieve velden nodig had. |
| `context_interpreter.py` | Geen wijziging. |
| `modules_extra.py` | Geen impact. |
| Frontend (`app.js`, templates) | Geen impact — buiten scope volgens het functioneel ontwerp. |
| Nieuw: Conversation Planner-module | Nieuw, geïsoleerd bestand, geen bestaande afhankelijkheden. |

## 8. Rollback-strategie

Eenvoudiger dan bij BUILD-004: omdat er geen enkel bestaand bestand wordt gewijzigd (ook `design_context.py` niet), volstaat het verwijderen van het ene nieuwe Conversation Planner-bestand om deze BUILD volledig terug te draaien. Niets in de huidige, live Dessinator — inclusief de BUILD-004-implementatie — wordt op enig moment aangeraakt.
