# BUILD-009 — Ontwerpstrategie-stap: technisch ontwerp

**Status:** technisch ontwerp, ter review. Geen implementatiecode, geen promptteksten, geen nieuwe architectuur. Bouwt voort op het functioneel ontwerp (BUILD-009) en het fundament BUILD-008; werkt de reeds bekrachtigde component uit T7 (AB-008) uit.

**Architectuurprincipe:** de component **stelt voor, bevestigt nooit** (AB-008) en is **AI-model-onafhankelijk** — de redeneerstap wordt achter een abstracte grens aangeroepen (zelfde patroon als BUILD-004: het aanroepmechaniek wordt hergebruikt, niet een specifiek model of een prompt vastgelegd). Volledig losstaand, zoals `context_interpreter.py`.

---

## 1. Publieke interface

- **Eén ingang:** een functie die een `DesignContext` ontvangt en een resultaat teruggeeft dat óf een voorgestelde `OntwerpStrategie` (laag 3) bevat, óf een signalering dat de context onvoldoende is.
- **Redeneer-grens (injecteerbaar):** de daadwerkelijke AI-redenering wordt als een aparte, injecteerbare aanroep meegegeven — de component kent het model niet. Dit houdt de component AI-onafhankelijk en test­baar zonder AI-sleutel.
- **Read-only op de input:** de component muteert laag 1 en 2 niet.

## 2. Interne verwerkingsstappen

1. **Preconditie-check** (zie §3) — bij falen: stop, geef een signalering terug, schrijf niets weg.
2. **Verzamelen** van de relevante inhoud van laag 1 (bevestigde Ontwerpvisie) en laag 2 (Project-/Ruimtecontext).
3. **Redeneren** via de geïnjecteerde redeneer-grens: op basis van visie + context een aanpak in benoembare termen plus onderbouwing afleiden.
4. **Verpakken** van het resultaat als `OntwerpStrategie` met status **"in ontwikkeling"** (BUILD-008).
5. **Registreren** van het "waarom" in de `Ontwerpredenering` (`voeg_beslissing_toe`, laag "ontwerpstrategie").

## 3. Validaties vóór de analyse

- **Ontwerpvisie (laag 1) is bevestigd** (`bevestigd_door_architect` is waar) en niet leeg — het onaantastbare anker.
- **Project-/Ruimtecontext (laag 2)** bevat voldoende vastgelegde context om een onderbouwde strategie te kunnen dragen.
- **Bij onvoldoende context:** de component gaat **niet** over tot de redeneerstap, vult **niets** zelf aan, en geeft uitsluitend een gestructureerde signalering terug.
- Optioneel hergebruik van `valideer()` (BUILD-008) voor de model-invarianten.

## 4. Outputobject

- **Bij succes:** een `OntwerpStrategie` (bestaande dataclass, BUILD-008) met `aanpak`, `onderbouwing` en `status = "in ontwikkeling"` — een voorstel, nog niet "vastgesteld".
- **Begeleidend:** een registratie in `Ontwerpredenering`, plus eventuele signaleringen.
- **Bij onvoldoende context:** géén `OntwerpStrategie`, uitsluitend de signalering(en).
- Het resultaat wordt teruggegeven via een lichte resultaat­wikkel (strategie óf signaleringen); dit is een technische returnvorm, geen nieuw architectuurobject.

## 5. Foutafhandeling

- **Verwachte gevallen** (onvoldoende context) → gestructureerde signalering, geen exception; DesignContext blijft ongewijzigd.
- **Technische fout** in de redeneer-grens (AI-aanroep faalt) → foutresultaat; er wordt **geen** partiële of verzonnen strategie weggeschreven.
- **Nooit zelf aanvullen**, **nooit bevestigen** (status blijft "in ontwikkeling"), **nooit** laag 1/2 muteren.
- De component is herhaalbaar aan te roepen zonder neveneffect op de input.

## 6. Aansluiting op BUILD-008

- Leest laag 1/2 en schrijft laag 3 via de bestaande dataclasses; gebruikt uitsluitend het laag-3-statusvocabulaire ("in ontwikkeling" / "vastgesteld").
- Bevestigt niets: de component roept **geen** bevestiging aan; `eigenaar_van("ontwerpstrategie")` = gezamenlijk (DCOD + architect), en bevestiging blijft aan de eigenaar/dialoog.
- Registreert via `Ontwerpredenering.voeg_beslissing_toe`.
- Volledig **additief en losstaand**: geen afhankelijkheid vanuit `app.py`/de pipeline tot er bewust wordt aangesloten (zelfde isolatiefilosofie als BUILD-004/BUILD-008).

---

**Acceptatie:** met een bevestigde, niet-lege Ontwerpvisie en voldoende context levert de component een `OntwerpStrategie` met status "in ontwikkeling" en een Ontwerpredenering-registratie; bij onbevestigde of onvoldoende context uitsluitend een signalering, zonder mutatie van de input en zonder zelf aanvullen. Validatie steunt op deze criteria, niet op koppeling aan de pipeline.
