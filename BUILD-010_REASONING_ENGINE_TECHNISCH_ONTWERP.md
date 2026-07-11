# BUILD-010 — Reasoning Engine: technisch ontwerp

**Status:** technisch ontwerp, ter review. Geen programmacode. Beschrijft uitsluitend **hoe** de Reasoning Engine wordt gerealiseerd; het **wat** ligt vast in BUILD-010 functioneel en mag niet wijzigen. Geen nieuwe architectuurcomponent, geen nieuwe functionele verantwoordelijkheid.

**Normatief:** BUILD-010 (leidend), BUILD-011 (leidend voor Fase 2), AB-001 Deel A, AB-006, AB-008, AB-009, DESIGN_BRAIN, BUILD-008 (fundament), BUILD-009 (bewezen patroon).

**Architectuurprincipe (technisch geborgd):** de component **stelt voor, bevestigt nooit** (AB-008) en is **AI-model-onafhankelijk** — elke redeneerstap loopt via een injecteerbare grens (BUILD-009-patroon), zonder model of prompt in dit ontwerp. Volledig additief en losstaand.

---

## 1. Technische architectuur

- **Eén module, één publieke component** (bijv. `reasoning_engine.py` / `ReasoningEngine`), naast `design_context.py` en `ontwerpstrategie_stap.py` — niet erin.
- **Interne modulegrenzen** (drie soorten, per fase gescheiden):
  - **Orkestratie** — de component die de fasen aanstuurt en resultaten teruggeeft.
  - **Reasoning boundary** — de redeneerstap per fase; kent DesignContext noch registratie; ontvangt een platte invoer en retourneert uitsluitend een voorstel (BUILD-009-patroon). Injecteerbaar, met een deterministische placeholder voor test.
  - **Validatie & kwaliteitsborging** — controles vóór en ná de boundary; muteren niets.
- **Afhankelijkheden:** leest/schrijft de DesignContext-dataclasses uit BUILD-008 (lagen 1–4, Ontwerpredenering) en hergebruikt `valideer()`, `eigenaar_van()`, `mag_bevestigen()`. Het **Floor Design-datamodel** (§3) leeft **buiten** de DesignContext, in deze module — nooit als DesignContext-laag.

## 2. Interne uitvoeringsfasen

### Fase 1 — Conceptvorming
- **Invoer:** DesignContext (laag 1 bevestigd, laag 2 vastgelegd, laag 3 Ontwerpstrategie).
- **Verwerking:** preconditie-validatie → reasoning boundary (visie+context+strategie → Concept-voorstel) → kwaliteitsborging (§4) → wegschrijven als voorgesteld Concept in laag 4.
- **Uitvoer:** DesignContext met voorgesteld Concept (laag 4) + resultaatwikkel.
- **Validatie:** visie bevestigd en niet leeg; context voldoende; strategie aanwezig; Concept volledig en binnen de strategie-bandbreedte.
- **Foutafhandeling:** bij falende preconditie of boundary → signalering/foutresultaat; **geen partieel Concept**; DesignContext ongewijzigd.

### Externe overdracht na Conceptbevestiging (deterministische fase-gate)
- Na Fase 1 schrijft de Reasoning Engine uitsluitend **`Concept.status = "voorgesteld"`** — nooit een andere waarde.
- De status **`"bevestigd"`** wordt **uitsluitend door de architect** toegekend (externe gebeurtenis, buiten de component); geen enkele fase van de Reasoning Engine schrijft deze waarde.
- De Reasoning Engine **leest** `Concept.status` uitsluitend; zij bevestigt nooit.
- **Fase 2 mag uitsluitend starten wanneer `Concept.status == "bevestigd"`.** Bij elke andere waarde start Fase 2 niet en volgt een signalering. Daarmee is de fase-overgang eenduidig en deterministisch.
- Deze twee waarden vormen het laag-4-statusvocabulaire (`"voorgesteld"` → `"bevestigd"`), consistent met het bestaande gebruik in `design_context.py` (`vertaal_analysis_naar_concept` zet reeds `status="voorgesteld"`); er is geen wijziging aan het `Concept`-datamodel nodig.

### Fase 2 — Floor Design-generatie *(conform BUILD-011)*
- **Invoer:** bevestigd Concept (laag 4) + onderliggende visie/context.
- **Verwerking:** preconditie (Concept bevestigd) → reasoning boundary (Concept → één of meer Floor Design-voorstellen) → kwaliteitsborging (elk voorstel aantoonbaar binnen het Concept) → verpakken als Floor Design-objecten (status "Voorgesteld", met motivering).
- **Uitvoer:** lijst Floor Design-objecten **buiten** de DesignContext + resultaatwikkel.
- **Validatie:** Concept bevestigd; elk Floor Design binnen Concept + strategie; volledig.
- **Foutafhandeling:** ongeldige Floor Designs worden **afgewezen**, niet teruggegeven; DesignContext wordt niet gemuteerd; geen partieel resultaat.

## 3. Gegevensmodellen (technische representatie, functionele betekenis ongewijzigd)

- **Invoer per fase:** een platte projectie van de benodigde laagvelden (analoog aan `_verzamel_invoer` in BUILD-009) → invoer voor de boundary. Houdt de boundary ontkoppeld van de DesignContext.
- **Tussenresultaten:** de boundary-output — voor Fase 1 een Concept-voorstel (velden van laag 4), voor Fase 2 een lijst Floor Design-voorstellen.
- **Concept:** de bestaande `Concept`-dataclass (BUILD-008, laag 4: `stijlfamilie`, `kleurpalet`, `complexiteit`, `motiefschaal`, `status`) — **ongewijzigd; geen nieuw veld.**
- **Floor Design:** een **nieuw technisch datamodel buiten de DesignContext** — minimaal: een identifier, de ontwerprichting, een **herkomst-referentie naar het bevestigde Concept**, de **motivering** (in het object zelf), de status "Voorgesteld", en kwaliteitsinformatie. Dit is uitsluitend de technische representatie van het reeds functioneel gedefinieerde resultaat-object (AB-006/BUILD-011).
- **Motivaties:** de motivatie van het Concept wordt **uitsluitend** vastgelegd in de **Ontwerpredenering** — niet in een `Concept`-veld (`Concept` blijft ongewijzigd). `FloorDesign.motivering` staat in het Floor Design-object zelf, buiten de DesignContext.
- **Kwaliteitsinformatie:** per resultaat een set indicatoren (binnen-strategie, volledigheid, binnen-Concept) — technische velden, geen nieuwe verantwoordelijkheid.

## 4. Validatie en kwaliteitsborging

- **Strategie gevolgd (Fase 1):** consistentiecontrole van het Concept tegen `OntwerpStrategie.aanpak`; een Concept buiten de bandbreedte levert een signalering (model: "Concept buiten de strategie = signaal tot herziening"), geen eigen keuze.
- **Concept volledig:** verplichte laag-4-velden aanwezig.
- **Floor Designs binnen het bevestigde Concept (Fase 2):** elk Floor Design draagt de herkomst-referentie én wordt getoetst tegen het Concept; een voorstel dat het Concept verlaat, wordt afgewezen (BUILD-011: "aantoonbaar binnen").
- **Inconsistenties detecteren:** de controles retourneren een lijst overtredingen (patroon van `valideer()`/`vergelijk_met_analysis()` uit BUILD-008).
- **Ongeldige resultaten afwijzen:** een resultaat met overtredingen wordt niet als geldig teruggegeven en niet weggeschreven; het leidt tot een signalering of regeneratie (§5).

## 5. Regeneratie

- **Wanneer:** bij een afgekeurd resultaat (kwaliteitsborging faalt) of op verzoek van de architect (afwijzen/varianten vragen).
- **Welke fase:** een afgekeurd **Concept** → Fase 1 opnieuw; afgekeurde **Floor Designs** → uitsluitend Fase 2 opnieuw, **zonder** Fase 1 te herhalen.
- **Behoud:** een **bevestigd Concept blijft behouden** bij Fase 2-regeneratie (Fase 2 wijzigt/verlaat het Concept nooit); bevestigde resultaten worden nooit overschreven (overwrite-guard, BUILD-009).
- **Geen oneindige lus:** een **technische regeneratielimiet** per fase (maximaal aantal pogingen); bij overschrijding → signalering, geen verdere retry. De component vult nooit zelf aan om een geldig resultaat te forceren.

## 6. Interfaces

- **Ontwerpstrategie → Reasoning Engine:** leest laag 3 (`OntwerpStrategie`) via de DesignContext; read-only.
- **Reasoning Engine → DesignContext:** Fase 1 leest lagen 1–3 en schrijft een voorgesteld Concept in laag 4 (via de BUILD-008-dataclasses); gebruikt `eigenaar_van`/`mag_bevestigen` maar **bevestigt nooit**. Fase 2 leest het bevestigde laag-4-Concept en **schrijft niet** naar de DesignContext.
- **Reasoning Engine → Floor Design:** produceert Floor Design-objecten (buiten de DesignContext), teruggegeven via de resultaatwikkel — niet in de DesignContext geschreven.
- **Reasoning Engine → downstream planners:** **geen directe aanroep.** De Floor Design-objecten vormen het contract dat downstream later consumeert (BUILD-007). De aansturing van de planners is een aparte, technische interface buiten deze component (AR-004/AB-005) — de engine kent de planners niet.

## 7. Traceerbaarheid

- **Keten Ontwerpstrategie → Concept → Floor Designs:** de relatie tussen de strategie en het Concept wordt vastgelegd in de **Ontwerpredenering** (het "waarom" van het Concept); elk Floor Design draagt een herkomst-referentie naar het bevestigde Concept. Zo is de volledige lijn herleidbaar, zonder veld in `Concept`.
- **Vastlegging van motivaties:** Fase 1 legt het "waarom" van het Concept vast in de **Ontwerpredenering** (`voeg_beslissing_toe`, laag "concept") — laag 4 is DesignContext. Fase 2 legt de motivering vast **in het Floor Design-object** en raakt de Ontwerpredenering niet (BUILD-011).
- **Audit/debug:** elk resultaat draagt zijn kwaliteitsinformatie en een verwijzing naar zijn invoer; validatie-overtredingen worden gestructureerd teruggegeven — voldoende om een afkeuring of regeneratie herleidbaar te maken, zonder nieuwe verantwoordelijkheid.

## 8. Prestatie en robuustheid

- **Fouttolerantie:** elke reasoning boundary-aanroep in een `try/except`; een technische fout → gestructureerd foutresultaat, **nooit** een partieel of verzonnen resultaat; DesignContext ongewijzigd (BUILD-009-patroon).
- **Herstelgedrag:** regeneratie met limiet (§5); bevestigde resultaten blijven behouden.
- **Schaalbaarheid:** de fasen zijn onafhankelijk aanroepbaar en per aanroep stateless (lezen de DesignContext, produceren een resultaat); zwaardere redenering is inpasbaar door een andere boundary te injecteren.
- **Uitbreidbaarheid:** het patroon validatie → boundary → kwaliteitsborging → resultaatwikkel (BUILD-009) is de herbruikbare blauwdruk; een echte, model-specifieke redenering wordt later geïnjecteerd **zonder** de component te wijzigen.
- **Technische randvoorwaarden:** AI-model-onafhankelijk (geen model/prompt vastgelegd); bouwt op het BUILD-008-fundament; geen wijziging aan `design_context.py` nodig (het Floor Design-datamodel leeft buiten de DesignContext); geen koppeling aan de live `/api/generate`-flow tot er bewust wordt aangesloten.

---

**Acceptatie:** met geldige, bevestigde input levert Fase 1 een voorgesteld Concept (laag 4) met Ontwerpredenering-registratie; na externe Conceptbevestiging levert Fase 2 één of meer Floor Design-objecten (status "Voorgesteld", met motivering, aantoonbaar binnen het Concept) buiten de DesignContext. Onvoldoende input, een afgekeurd resultaat of een technische fout leiden tot een signalering/foutresultaat en, waar van toepassing, gelimiteerde regeneratie — zonder mutatie van laag 1–3, zonder bevestiging en zonder zelf aan te vullen. Validatie steunt op deze criteria, niet op koppeling aan de pipeline.
