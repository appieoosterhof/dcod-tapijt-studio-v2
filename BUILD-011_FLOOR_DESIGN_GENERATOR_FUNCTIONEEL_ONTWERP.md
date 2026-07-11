# BUILD-011 — Floor Design Generator: functioneel ontwerp

**Status:** functioneel ontwerp, ter review. Geen technisch ontwerp, geen implementatie, geen nieuwe architectuur, geen nieuwe component. Beschrijft de **creatieve Floor Design-generatiefase binnen de Reasoning Engine** (AB-009, lezing a; de producent is de Reasoning Engine, conform C2). Dit is **geen zelfstandige component naast de Reasoning Engine**, maar de fase waarin een reeds bevestigd Concept creatief wordt uitgewerkt tot Floor Designs.

**Uitgangspunt:** de Floor Design Generator **creëert nieuwe vloerontwerpen** — nadrukkelijk méér dan een patroonmaker. Hij zet een bevestigd Concept om naar **één of meer voorgestelde Floor Designs**, motiveert elk voorstel, bevestigt niets en wijzigt de DesignContext niet.

---

## 1. Doel

Een **bevestigd Concept** (DesignContext-laag 4) creatief omzetten naar **één of meer voorgestelde Floor Designs** — het eerste tastbare ontwerpresultaat ná de ontwerpfase (BUILD-007; AB-009 lezing a). Deze generatiefase van de Reasoning Engine ondersteunt de ontwerper door **meerdere kansrijke ontwerprichtingen** aan te bieden waarop hij kan reageren, in plaats van één opgelegde uitkomst.

## 2. Input

Het **bevestigde Concept** (laag 4), met de onderliggende, reeds vastgelegde **Ontwerpvisie** (laag 1) en **Project-/Ruimtecontext** (laag 2) als onderbouwende context. **Inputconditie om te mogen starten:** het Concept is bevestigd (AB-009). De component **leest** deze lagen en **muteert ze niet**.

## 3. Output

**Eén of meer Floor Design-objecten**, elk met de status **"Voorgesteld"** (AB-006) en elk **voorzien van een motivering** die bij het object zelf hoort. De component produceert **uitsluitend Floor Design-objecten** — geen andere artefacten.

## 4. Verantwoordelijkheden

- **Meerdere kansrijke ontwerprichtingen genereren** uit hetzelfde bevestigde Concept, zodat de ontwerper kan kiezen en bijsturen.
- **Nieuwe vloerontwerpen creëren** — een ontwerprichting vormgeven, niet slechts een patroon herhalen.
- **Elk voorstel motiveren**, waarbij de motivering onderdeel is van het Floor Design-object.
- **Binnen het bevestigde Concept blijven** — alle voorgestelde Floor Designs blijven aantoonbaar binnen het bevestigde Concept en de daaruit voortvloeiende ontwerpstrategie; deze fase vergroot de creatieve ontwerpvrijheid, maar verlaat het bevestigde Concept nooit.
- **Signaleren** wanneer het bevestigde Concept onvoldoende is om een onderbouwd Floor Design te genereren; ontbrekende informatie wordt **nooit zelf ingevuld**.
- Alle voorstellen dragen uitsluitend de status "Voorgesteld" — de architect beoordeelt, wijzigt of bevestigt (AB-006).

## 5. Wat de component nadrukkelijk niet doet

- **Niets bevestigen** — bevestiging van een Floor Design ligt bij de architect (AB-006).
- **De DesignContext niet wijzigen** — ook niet de doorlopende Ontwerpredenering; de motivering leeft in het Floor Design-object, niet in de DesignContext.
- **Zelf geen Concept vormen** — het vormen van het Concept (laag 4) is een andere, eerdere fase van de Reasoning Engine; deze generatiefase begint pas ná een bevestigd Concept.
- **Geen materiaal bepalen** (Material Profile).
- **Geen SVG maken** (SVG Planner).
- **Geen visualisatie maken** (Floor Visualization Engine).
- **Geen vrije tekst interpreteren of vragen timen** (Context Interpreter, Conversation Planner).
