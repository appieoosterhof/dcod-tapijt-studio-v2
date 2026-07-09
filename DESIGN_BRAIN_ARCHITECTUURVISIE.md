# Design Brain — Architectuurvisie en -principes

**Status:** architectuursynchronisatie, geen implementatie. Vastgesteld als uitgangspunt voor de volgende fase (na BUILD-003, vóór een eventuele BUILD-004). Bouwt voort op het bevroren DesignContext Model v1.0 en DISCOVERY-004 — vervangt of herziet geen van beide.

---

## Aanleiding

Tijdens de ontwerpsessies na BUILD-003 is een bredere architectuurvisie geformuleerd: de DCOD Dessinator is geen configurator, geen patroonbibliotheek en geen AI-afbeeldingengenerator, maar een digitale ontwerpassistent die samen met een interieurarchitect een vloerconcept ontwikkelt. De primaire invoer is niet een stijlkeuze, maar de ontwerpcontext.

Dit document legt de resulterende architectuurketen en -principes vast, inclusief de kritische review die daarop is uitgevoerd en de aanpassingen die daaruit zijn voortgekomen.

## De ontwerpketen

```
Projectcontext → Ontwerpintentie → Ontwerpsignatuur
        → DCOD Design Brain (Context → Strategie → Reasoning → Materiaal/Patroon/SVG)
        → Mock-up → Iteratieve verfijning
```

## Uitgangspunten

1. **Conversatie is de ontwerpmotor.** De gebruiker begint met het beschrijven van het project, niet met het kiezen van een stijl.
2. **Projectcontext is leidend.** De Dessinator gebruikt de beschikbare context om zelf te bepalen welke informatie al bekend is en welke vragen nog relevant zijn.
3. **Snelheid is een harde ontwerpregel.** Iedere nieuwe functie moet de weg van idee naar vloer verkorten.
4. **De SVG-generator is uitsluitend een uitvoerende component.** Alle ontwerpintelligentie bevindt zich vóór de generator.
5. **Collecties zijn optioneel.** Ze kunnen inspiratie bieden maar bepalen nooit zelfstandig het ontwerp.

## Ontwerpsignatuur

Iedere ontwerper heeft een eigen manier van ontwerpen (bijvoorbeeld minimalistisch, warm, grafisch, organisch, architectonisch). Deze ontwerpsignatuur is geen vaste stijl en mag nooit beperkend werken — de actuele projectcontext en ontwerpintentie blijven altijd leidend. Ontwerpsignatuur wordt uitsluitend gebruikt als startvoorkeur om sneller tot een passende eerste ontwerprichting te komen.

**Scope v1 (expliciet vastgesteld):** Ontwerpsignatuur is voorlopig **sessiegebonden** — afgeleid uit het huidige gesprek, niet uit een persistent architect-profiel. Een persistent ontwerpersprofiel valt buiten de scope van de eerste versie en wordt pas later, als aparte afweging, overwogen. Dit sluit aan bij de eerder vastgestelde scope-keuze in het DesignContext Model ("v1 is sessiegebonden").

---

## Verhouding tot het bevroren DesignContext Model

Dit is het punt waarop de eerste versie van deze visie kritisch is bevraagd, en waarop de volgende vier principes zijn vastgesteld naar aanleiding daarvan.

**Het bestaande DesignContext Model blijft ongewijzigd en is de canonieke domeinbeschrijving.** Deze architectuurschets is nadrukkelijk geen vervanging of herziening daarvan.

**De DCOD Design Brain is géén nieuw domeinmodel.** Het is een software-/redeneringslaag die gebruikmaakt van het bestaande DesignContext Model om intelligente ontwerpbeslissingen te nemen. De Design Brain *leest en verrijkt* de lagen van het bevroren model; hij definieert ze niet opnieuw.

---

## Vier architectuurregels voor de volgende fase

### 1. Eén canonieke woordenschat (terminologie-mapping)

Er komt een expliciete, woord-voor-woord mapping tussen de architectuurtermen uit deze visie en het bevroren DesignContext Model, zodat er nooit twee vocabulaires naast elkaar bestaan voor dezelfde werkelijkheid. Concreet minimaal te koppelen: Projectcontext ↔ Project-/Ruimtecontext, Ontwerpintentie ↔ Ontwerpvisie, Design Reasoning ↔ Ontwerpredenering. Deze mapping moet zijn vastgesteld vóórdat er componenten op worden gebouwd.

### 2. Ontwerpstrategie als expliciete, eigen stap

Ontwerpstrategie is **geen** onderdeel van de Reasoning Engine. Het wordt gemodelleerd als een afzonderlijke stap tussen Context en Reasoning, met behoud van het eigenaarschap dat het bevroren model daaraan toekent (gezamenlijk ontwikkeld door DCOD en architect — niet eenzijdig door één component bepaald).

Herziene interne opbouw van de Design Brain:

```
Context Interpreter → Ontwerpstrategie (eigen stap) → Reasoning Engine
        → Material Planner / Pattern Planner / SVG Planner
```

(Conversation Planner opereert hier orthogonaal op: hij bepaalt welke vragen relevant zijn, maar schrijft zelf geen ontwerpbeslissingen weg.)

### 3. Eigenaarschap gaat mee omlaag naar elke component

> Geen enkele component van de Design Brain mag zelfstandig ontwerpbeslissingen definitief bevestigen wanneer die volgens het DesignContext Model eigendom zijn van de architect of van de gezamenlijke dialoog tussen architect en DCOD.

De Design Brain mag voorstellen doen, onderbouwen en signaleren, maar nooit de rol van de architect overnemen. Dit principe is een directe verlenging van het bevroren model se eigenaarschapsregels (bijvoorbeeld: alleen de architect bevestigt de Ontwerpvisie definitief) naar het softwareniveau, en van DISCOVERY-004 ("de Dessinator neemt nooit de rol van ontwerper over").

### 4. Gecontroleerde migratie, één component per keer

Nieuwe componenten worden niet als één geheel geïmplementeerd. Elke component wordt een eigen, afzonderlijke BUILD die één verantwoordelijkheid toevoegt, apart wordt getest tegen de bestaande pipeline, en pas daarna de basis vormt voor de volgende BUILD — hetzelfde bewezen principe als BUILD-002 (kleurpalet) en BUILD-003 (repeat-type), nu toegepast op de Design Brain-componenten.

---

## Status

Architectuursynchronisatie afgerond. Dit document vormt het uitgangspunt voor de eerste concrete BUILD op de Design Brain, zodra die wordt gestart. Er is op dit moment geen implementatie, geen architectuurdocument per component, en geen BUILD-004-planning — dat volgt in een latere, aparte stap.
