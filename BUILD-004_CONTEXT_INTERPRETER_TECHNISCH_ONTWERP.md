# BUILD-004 — Context Interpreter: technisch ontwerp

**Status:** technisch ontwerp, ter review. Geen implementatie, geen commit. Bouwt voort op `BUILD-004_CONTEXT_INTERPRETER_FUNCTIONEEL_ONTWERP.md` (architectonisch en functioneel gereed) en op de bestaande, werkende codebase (`app.py`, `design_context.py`).

---

## 0. Architectuurprincipe

> **Iedere AI-component binnen de DCOD Dessinator produceert interpretaties, nooit waarheden.**

Dit volgt rechtstreeks uit de architectuurkeuze dat onzekerheid geen eigenschap is van data of van een DesignContext-veld, maar van de interpretatie die een component daaraan geeft. De architect of designer blijft altijd degene die een interpretatie bevestigt, wijzigt of verwerpt — nooit de component zelf.

Dit principe is voor BUILD-004 vastgesteld bij de Context Interpreter, maar geldt als algemeen architectuurprincipe voor de gehele Dessinator: elke huidige en toekomstige AI-component (Context Interpreter, en later bijvoorbeeld Reasoning Engine, Material Planner, Pattern Planner) produceert output met de status "interpretatie", nooit met de status "waarheid" of "bevestigd". Alleen de architect — of, waar van toepassing, de gezamenlijke dialoog tussen architect en DCOD — kan een interpretatie tot een vastgestelde ontwerpbeslissing maken.

*(Signalering: dit principe reikt verder dan BUILD-004 alleen en raakt daarmee mogelijk ook `SPEC-000_PROJECT_CHARTER.md` — met name hoofdstuk 6 (Architectuurprincipes) en 7 (Governance). Ik neem het hier uitsluitend op zoals gevraagd, binnen het technisch ontwerp van BUILD-004, en laat het aan jullie of dit ook in SPEC-000 wordt doorgevoerd.)*

## 1. Technische componenten

- **Context Interpreter-module (nieuw)** — bevat de interpretatielogica: neemt vrije tekst en eventuele basisprojectgegevens, roept een AI-analyse aan die specifiek is toegesneden op het herkennen van Project-/Ruimtecontext- en Ontwerpvisie-gegevens, en zet het resultaat om naar de juiste DesignContext-velden.
- **Vertaalfunctie(s) naar DesignContext** — mappen de AI-output naar `OntwerpVisie`- en `ProjectContext`-velden, volgens hetzelfde patroon als de bestaande `vertaal_analysis_naar_*()`-functies in `design_context.py` (Fase 2a-discipline: precies één vertaalfunctie per doel, geen verspreide mapping-logica).
- **Onzekerheidsregistratie (structurele uitbreiding, ontwerp nog te bepalen)** — conform het architectuurprincipe in hoofdstuk 0 is onzekerheid een eigenschap van de interpretatie, niet van het veld of de data zelf. Dit bestaat nog niet in de huidige `OntwerpVisie`/`ProjectContext`-dataclasses. De technische vormgeving hiervan (hoe een interpretatie, los van het veld dat ze betreft, wordt vastgelegd) is nog niet uitgewerkt en volgt in een latere stap.

## 2. Gegevensstromen

```
Architect
   │  vrije tekst + evt. basisprojectgegevens
   ▼
Context Interpreter (nieuw, losstaand)
   │  1. AI-analyse (zelfde aanroepmechaniek als analyse_prompt(), eigen system-prompt/schema
   │     gericht op Project-/Ruimtecontext + Ontwerpvisie-herkenning)
   │  2. Vertaling naar OntwerpVisie- en ProjectContext-velden
   │  3. Toekennen van een mate van zekerheid aan elke interpretatie
   ▼
DesignContext (OntwerpVisie + ProjectContext gevuld, status uitsluitend "voorgesteld")
   │
   ▼
   [buiten scope BUILD-004: Conversation Planner, Ontwerpstrategie, Concept, generatie]
```

Er is in deze stroom nadrukkelijk **geen koppeling** met de bestaande `/api/generate`-flow. Context Interpreter produceert een DesignContext-fragment dat vooralsnog geen enkele consument heeft binnen de huidige, live Dessinator — dat is een bewuste, tijdelijke situatie (zie hoofdstuk 6).

## 3. Interfaces

- **Input naar Context Interpreter:** vrije tekst (verplicht) en optionele basisprojectgegevens, op dezelfde manier aangeleverd als de bestaande request-payload van `/api/generate` dat vandaag al doet (bijvoorbeeld een reeds gekozen projecttype uit de inspiratie-flow).
- **Output van Context Interpreter:** een (deel van een) `DesignContext`-object — specifiek de velden `ontwerpvisie` en `projectcontext` — waarbij elke interpretatie een eigen mate van zekerheid meekrijgt; de DesignContext-velden zelf bevatten geen onzekerheidsstatus. Geen enkel veld krijgt een bevestigde status; dat blijft, conform het functioneel ontwerp, voorbehouden aan de architect.
- **Interface richting een toekomstige Conversation Planner:** niet gebouwd in BUILD-004, maar wel een randvoorwaarde voor het ontwerp: de vorm waarin de mate van zekerheid per interpretatie wordt vastgelegd, moet bruikbaar zijn als input voor een component die daar later op voortbouwt, zonder dat de Context Interpreter zelf hoeft te weten wat de Conversation Planner ermee doet.
- **Interface richting de bestaande pipeline (`analyse_prompt()`, `api_generate()`, `build_tile_svg()`):** géén. Context Interpreter is in BUILD-004 volledig losstaand, net zoals `design_context.py` dat in BUILD-001A was — bewijzen dat de component zelfstandig correct werkt, vóórdat er iets aan wordt gekoppeld.

## 4. Bestaande modules die hergebruikt kunnen worden

- **`design_context.py`** — de dataclasses `OntwerpVisie` en `ProjectContext` (en `DesignContext` zelf, met `to_dict()`/`from_dict()`/`kopie()`) zijn direct te gebruiken als doelstructuur. Geen noodzaak om deze opnieuw te modelleren.
- **Het aanroepmechaniek van `analyse_prompt()`** — niet de functie zelf hergebruiken (die is specifiek voor stijl/palet-analyse en blijft ongewijzigd), maar wél het bewezen patroon: een Claude-aanroep met een gestructureerd JSON-schema als system-prompt, en dezelfde manier van API-sleutel-doorgifte die de rest van de Dessinator al gebruikt.
- **De additieve-koppeling-discipline uit BUILD-001B/Fase 2a** (één vertaalfunctie per doel, vers afgeleid, geen gedeelde mutable state) — een architectuurpatroon om te hergebruiken, geen code.

## 5. Nieuwe modules die nodig zijn

- **Een nieuwe, losstaande Context Interpreter-module**, met dezelfde isolatiefilosofie als `design_context.py`: geen afhankelijkheid vanuit bestaande bestanden totdat bewust gekozen wordt iets aan te sluiten.
- **Een structurele uitbreiding van `design_context.py`** voor het vastleggen van de mate van zekerheid per interpretatie — niet als eigenschap van een DesignContext-veld, maar als eigenschap van de interpretatie zelf. Dit raakt een bestaand bestand, maar op dezelfde additieve manier als eerdere BUILD's (nieuwe velden/structuren toevoegen, niets bestaands wijzigen).
- **Optioneel: een geïsoleerd test-toegangspunt** (geen productie-route) om de Context Interpreter apart te kunnen beproeven, zonder de bestaande `/api/generate`-route aan te raken — vergelijkbaar met hoe `design_context.py` in BUILD-001A eerst zelfstandig werd getoetst vóór enige koppeling.

## 6. Migratie-impact op de huidige codebase

| Bestand | Impact |
|---|---|
| `app.py` | **Geen wijziging.** Er is nog geen consument (Conversation Planner) voor de output, dus koppeling aan `/api/generate` is voor BUILD-004 niet aan de orde. |
| `design_context.py` | **Additieve uitbreiding** (vastleggen van de mate van zekerheid per interpretatie). Geen bestaande velden of functies wijzigen. |
| `modules_extra.py` | Geen impact. |
| Frontend (`app.js`, templates) | Geen impact — buiten scope volgens het functioneel ontwerp (geen SVG, geen mock-ups). |
| Nieuw: Context Interpreter-module | Nieuw, geïsoleerd bestand, geen bestaande afhankelijkheden. |

**Methodologisch verschil met BUILD-002/003:** die migraties verplaatsten een reeds bestaande beslissing (kleurpalet, repeat-type) van een oude naar een nieuwe bron, en konden daarom worden getoetst met Parallelle Validatie (nieuwe bron vergeleken met de oude). BUILD-004 introduceert een **geheel nieuwe capaciteit** zonder legacy-equivalent — er is geen "oude bron" om tegen te vergelijken. Validatie zal daarom moeten steunen op de acceptatiecriteria uit het functioneel ontwerp (geen aannames invullen, correcte laagtoewijzing, correcte mate van zekerheid per interpretatie, consistente output bij gelijke input), niet op een output-vergelijking zoals bij eerdere BUILD's.

**Rollback:** zoals bij alle voorgaande BUILD's — het nieuwe Context Interpreter-bestand verwijderen en de additieve uitbreiding in `design_context.py` ongedaan maken. Niets in de huidige, live Dessinator is op enig moment aangeraakt.

## 7. Definition of Done

BUILD-004 wordt als afgerond beschouwd wanneer:

- ✓ de Context Interpreter-module bestaat als losstaande, zelfstandig testbare component, zonder afhankelijkheid vanuit bestaande bestanden;
- ✓ voor vrije tekst-invoer levert de component uitsluitend voorgestelde interpretaties op, elk ondergebracht in de juiste laag van het DesignContext Model (Project-/Ruimtecontext of Ontwerpvisie), conform het functioneel ontwerp;
- ✓ elke interpretatie krijgt, waar van toepassing, een eigen mate van zekerheid, zonder dat daarvoor een apart "onzekerheden"-veld bestaat;
- ✓ geen enkele interpretatie krijgt de status "bevestigd" — uitsluitend "voorgesteld";
- ✓ de Context Interpreter stelt zelf geen vragen aan de architect;
- ✓ `app.py`, `modules_extra.py` en de frontend zijn op geen enkele manier gewijzigd;
- ✓ de uitbreiding van `design_context.py` is uitsluitend additief — geen bestaande velden of functies zijn aangepast;
- ✓ de bestaande Dessinator functioneert aantoonbaar exact zoals vóór BUILD-004.
