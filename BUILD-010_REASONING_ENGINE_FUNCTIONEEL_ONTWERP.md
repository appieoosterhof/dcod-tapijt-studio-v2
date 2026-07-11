# BUILD-010 — Reasoning Engine: functioneel ontwerp

**Status:** functioneel ontwerp, gereed voor architectuurreview (VR). Beschrijft uitsluitend **wat** de Reasoning Engine functioneel doet, niet **hoe**. Geen nieuwe architectuur, geen nieuwe component, geen nieuwe verantwoordelijkheid buiten de bestaande architectuur. Verankerd in AB-001 Deel A, AB-008, AB-009, BUILD-007, BUILD-009, BUILD-011 en het DesignContext Model.

**Kern:** de Reasoning Engine bestaat uit **twee opeenvolgende functionele fasen** binnen één component — **Conceptvorming** en **Floor Design-generatie** — gescheiden door één externe gebeurtenis: de bevestiging van het Concept door de architect (AB-009).

---

## 1. Plaats binnen de architectuur

De Reasoning Engine staat in de interne opbouw van de Design Brain ná de Ontwerpstrategie-stap (DESIGN_BRAIN Regel 2: Context Interpreter → Ontwerpstrategie-stap → Reasoning Engine → planners). Zij is de verwerkende component die:
- de vastgelegde ontwerpfase-lagen omzet in een voorgesteld **Concept** (laag 4) — AB-008;
- ná bevestiging van dat Concept één of meer **Floor Designs** genereert — AB-009 (producent = Reasoning Engine).

## 2. Functionele verantwoordelijkheid

De Reasoning Engine **stelt voor, bevestigt nooit** (AB-008; "interpretaties, nooit waarheden"). Haar verantwoordelijkheid omvat, over beide fasen:
- het vormen van één voorgesteld Concept uit visie, context en strategie (Fase 1);
- het genereren van één of meer voorgestelde Floor Designs binnen een bevestigd Concept (Fase 2);
- het **motiveren** van elk voorstel;
- het **signaleren** wanneer de beschikbare input onvoldoende is, zonder ontbrekende informatie ooit zelf in te vullen.

## 3. Interne fasen (overzicht)

| Fase | Start­voorwaarde | Output | Bevestigt? |
|---|---|---|---|
| 1. Conceptvorming | Visie, context en strategie zijn vastgelegd | Eén voorgesteld Concept (laag 4) | Nee |
| 2. Floor Design-generatie | Het Concept is **bevestigd** (door de architect) | Eén of meer voorgestelde Floor Designs | Nee |

De overgang tussen de fasen is geen interne beslissing van de Reasoning Engine, maar de **externe bevestiging van het Concept door de architect**. Fase 2 start uitsluitend daarná.

## 4. Fase 1 — Conceptvorming

- **Doel:** één voorgesteld **Design Concept** vormen — de concrete, esthetische invulling van de strategie (DesignContext-laag 4).
- **Input:** de bevestigde **Ontwerpvisie** (laag 1), de vastgelegde **Project-/Ruimtecontext** (laag 2) en de **Ontwerpstrategie** (laag 3, BUILD-009).
- **Output:** één voorgesteld Concept in laag 4, met onderbouwing; status conform het gedeelde eigenaarschap van laag 4 (voorgesteld/bij te sturen), nooit bevestigd.
- **Grenzen:** blijft binnen de bandbreedte van de Ontwerpstrategie (een Concept buiten die strategie is een signaal tot herziening, niet een eigen keuze); **produceert nooit een bevestiging**; **eindigt zodra het Concept is voorgesteld**. Signaleert onvoldoende input; vult niets zelf aan.

## 5. Fase 2 — Floor Design-generatie

Deze fase is functioneel identiek beschreven in BUILD-011 en blijft daarmee volledig consistent.

- **Doel:** een bevestigd Concept creatief uitwerken tot **één of meer voorgestelde Floor Designs** — het eerste tastbare ontwerpresultaat ná de ontwerpfase (BUILD-007; AB-009 lezing a).
- **Startvoorwaarde:** het Concept (laag 4) is **bevestigd**. Zonder bevestigd Concept start deze fase niet.
- **Input:** het bevestigde Concept, met de onderliggende visie en context als onderbouwing.
- **Output:** één of meer Floor Design-objecten, elk met status **"Voorgesteld"** (AB-006) en elk met een eigen motivering; uitsluitend Floor Design-objecten, **buiten** de DesignContext.
- **Grenzen:** blijft **aantoonbaar binnen het bevestigde Concept** en de daaruit voortvloeiende ontwerpstrategie; **wijzigt of verlaat het Concept nooit**; wijzigt de DesignContext (inclusief Ontwerpredenering) niet; bevestigt niets. Signaleert een onvoldoende Concept; vult niets zelf aan.

## 6. Functionele gegevensstroom tussen de fasen

```
lagen 1-3 (Visie + Context + Strategie)
        │
        ▼
   [ Fase 1: Conceptvorming ]
        │  voorgesteld Concept (laag 4)
        ▼
   architect bevestigt het Concept        ← externe gebeurtenis, geen Reasoning Engine-beslissing
        │  bevestigd Concept
        ▼
   [ Fase 2: Floor Design-generatie ]
        │  één of meer voorgestelde Floor Designs (buiten DesignContext)
        ▼
   architect beoordeelt / wijzigt / bevestigt (AB-006)
```

Fase 2 gebruikt uitsluitend het **bevestigde** resultaat van Fase 1; er is geen terugkoppeling waarbij Fase 2 het Concept aanpast.

## 7. Grenzen van de verantwoordelijkheid — welke beslissingen wel/niet

**Wel:** voorstellen vormen (Concept; Floor Designs) en die onderbouwen.

**Niet:**
- **Niets bevestigen** — bevestiging van Concept en Floor Design ligt bij de architect (AB-006, AB-008).
- **Geen vrije tekst interpreteren** (Context Interpreter, BUILD-004).
- **Geen ontwerpstrategie formuleren** (Ontwerpstrategie-stap, laag 3, BUILD-009).
- **Geen vragen kiezen of timen** (Conversation Planner, BUILD-005/007).
- **Geen materiaal bepalen** (Material Profile), **geen SVG** (SVG Planner), **geen visualisatie** (Floor Visualization Engine).
- **De Ontwerpvisie niet wijzigen** — die is na bevestiging onaantastbaar (laag 1).

## 8. Relatie met andere componenten en met de DesignContext

- **Upstream:** de Ontwerpstrategie-stap (BUILD-009) levert laag 3; de Reasoning Engine bouwt daarop voort.
- **DesignContext (BUILD-008):** Fase 1 leest lagen 1-3 en schrijft een voorgesteld Concept in laag 4; Fase 2 leest het bevestigde Concept en produceert Floor Designs **buiten** de DesignContext (wijzigt haar niet).
- **Conversation Planner:** bepaalt orthogonaal de interactietiming; de Reasoning Engine schrijft zelf geen vragen.
- **Architect:** bevestigt het Concept (poort tussen Fase 1 en 2) en later het gekozen Floor Design.
- **Downstream van Floor Design:** Material Profile, Floor Visualization Engine en Design Transfer Package consumeren een bevestigd Floor Design (BUILD-007) — de Reasoning Engine levert het, maar kent hun werking niet.

---

**Reviewgereed:** dit functioneel ontwerp legt uitsluitend de verantwoordelijkheid, de twee fasen, hun in-/output en grenzen vast; het bevat geen technische realisatie. Na een positieve VR kan het als basis dienen voor het technisch ontwerp van de Reasoning Engine.
