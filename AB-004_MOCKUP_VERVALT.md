# AB-004 — Concept-Architectuurbesluit: Mock-up vervalt als zelfstandig ketenbegrip

**Status:** concept, ter beoordeling. Geen enkel bestaand document is gewijzigd. Uitwerking van agendapunt **T2** uit `ARCHITECTUUR_BESLUITVORMINGSAGENDA_FASE_2.md` (roadmap Sprint 1 — Opruiming; §5 markeert T2 als Architectuurbesluit + visiewijziging). Aanleiding: `AR-002_DESIGN_BRAIN_HARMONISATIE_ANALYSE.md`, aanbeveling 6.

**Vraagstelling:** vervalt het ketenbegrip "Mock-up" (uit de ontwerpketen van `DESIGN_BRAIN_ARCHITECTUURVISIE.md`) als zelfstandig architectuurbegrip, ten gunste van de drie afzonderlijk vastgelegde begrippen Scene, Floor Visualization Engine en Visualisatie?

**Scope:** uitsluitend het ketenbegrip "Mock-up". Nadrukkelijk niet de bestaande, werkende **Mockup Engine** (de implementatie in `static/js/app.js`), en niet enig ander begrip uit dezelfde ketenregel (zoals "Iteratieve verfijning").

---

## 1. Vastgestelde feiten

Uitsluitend letterlijke of ondubbelzinnige inhoud uit bestaande documenten, geen interpretatie:

- **F1.** `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, regel 18: de ontwerpketen bevat de stap "... → Mock-up → Iteratieve verfijning". Dit is de enige plek waar "Mock-up" nog als ongedifferentieerd ketenbegrip voorkomt (afgezien van het letterlijke citaat daarvan in `AR-001_ARCHITECTUURREVIEW_FASE_1.md`, regel 27).
- **F2.** `BUILD-007_TOEKOMSTIGE_WORKFLOW_FUNCTIONEEL_ONTWERP.md`, regel 9, formuleert de volledige keten zónder het begrip "Mock-up": "... → Floor Design → Material Profile → **Scene → Floor Visualization Engine → Visualisatie** → Design Transfer Package → DCOD." De opsplitsing is in BUILD-007 dus al doorgevoerd.
- **F3.** De drie vervangende begrippen zijn elk afzonderlijk vastgelegd, elk met een eigen, onderscheiden verantwoordelijkheid (`BUILD-007_TOEKOMSTIGE_WORKFLOW_TECHNISCH_ONTWERP.md`, statustabel regels 29–31 en hoofdstuk 2, regels 46–48):
  - **Scene** (ketenstap 8) — "Gestandaardiseerd invoer-object (ruimte)", *vastgesteld, geïmplementeerd (BUILD-006)*; standaardiseert elke ruimte-invoer tot één achtergrond + één vloerpolygon, ongeacht de bron.
  - **Floor Visualization Engine** (ketenstap 9) — "Verwerkende component", *vastgesteld in naam/rol (VISION-001), nog niet gebouwd*; voegt Floor Design, Material Profile en Scene samen tot één beeld.
  - **Visualisatie** (ketenstap 10) — "Resultaat-artefact (geen eigen verwerkingslogica)", *nieuw, nog niet technisch uitgewerkt*; het getoonde eindbeeld.
- **F4.** `AR-002_DESIGN_BRAIN_HARMONISATIE_ANALYSE.md`, regel 33, legt de opsplitsing expliciet vast: "Mock-up | Opgesplitst | Scene (BUILD-006) + Floor Visualization Engine (VISION-001/BUILD-007) + Visualisatie (BUILD-007) | Eén ongedifferentieerde eindstap is drie afzonderlijke architectuurobjecten geworden, elk met een eigen, in BUILD-007 vastgelegde verantwoordelijkheid."
- **F5.** De bestaande **Mockup Engine** is een ander begrip dan het ketenbegrip "Mock-up": het is een van de vier deelsystemen (`CLAUDE.md`, "Bekijk in ruimte", `ROOM_MOCKUPS` in `static/js/app.js`), een werkend, geïmplementeerd systeem. `BUILD-006_SCENE_BUILDER.md` (regel 26) en `VISION-001_FLOOR_VISUALIZATION_PLATFORM.md` (regel 29) benoemen deze Mockup Engine juist als de bestaande **basis** waarop Scene voortbouwt (identiek polygon-formaat, ongewijzigde render-engine).
- **F6.** `DESIGN_CONTEXT_MODEL.md` (regel 46) en `VISION-001` (regel 30) plaatsen fysieke ruimte-informatie ("foto's, mockups") expliciet buiten de v1-scope van het DesignContext Model; VISION-001 stelt daarbij dat die scope-keuze "niet met terugwerkende kracht" wordt gewijzigd.

## 2. Architectuurinterpretaties

Redeneringen die de feiten verbinden — zelf geen feit, wel direct herleidbaar:

- **I1.** Uit F2 + F3 + F4 volgt dat de opsplitsing van "Mock-up" geen voorstel meer is maar een reeds voltrokken feit in de actuele keten (BUILD-007); alleen de oudere Architectuurvisie (F1) draagt het begrip nog. Het besluit is daarmee het formeel buiten gebruik stellen van een reeds vervangen term.
- **I2.** De drie vervangers zijn geen synoniemen van elkaar maar dekken drie verschillende rollen — invoer (Scene), verwerking (Floor Visualization Engine) en resultaat (Visualisatie). "Mock-up" verenigde die drie in één ongedifferentieerde stap; dat is precies wat de opsplitsing opheft.
- **I3.** Uit F5 volgt dat "Mock-up laten vervallen" uitsluitend het abstracte ketenbegrip betreft en niet de gelijknamige implementatie: die implementatie (Mockup Engine) blijft niet alleen bestaan, maar is de aantoonbare technische fundering onder Scene.

## 3. Architectuurkeuze

**K1.** Het ketenbegrip **"Mock-up"** vervalt als zelfstandig architectuurbegrip. In de architectuurwoordenschat wordt het vervangen door de drie afzonderlijke, elk reeds vastgelegde begrippen **Scene**, **Floor Visualization Engine** en **Visualisatie**, elk met de in F3 benoemde eigen verantwoordelijkheid.

**K2.** "Mock-up" is voortaan uitsluitend een historisch begrip (verouderde, ongedifferentieerde voorloper van de drie); het wordt niet meer als werkterm in nieuw architectuur- of ontwerpmateriaal gebruikt (conform de Toepassingsregels van AB-003).

**K3.** Dit besluit introduceert geen nieuw begrip: Scene, Floor Visualization Engine en Visualisatie bestaan alle drie al in BUILD-006/VISION-001/BUILD-007. De keuze is uitsluitend het formeel opheffen van het verouderde verzamelbegrip.

## 4. Overwogen alternatieven

- **Alternatief 1 — "Mock-up" behouden als koepelbegrip naast de drie deelbegrippen.** *Afgewezen*: houdt twee vocabulaires voor dezelfde werkelijkheid in stand (in strijd met Regel 1-intentie van `DESIGN_BRAIN_ARCHITECTUURVISIE.md` en met AB-003), en verhult juist het onderscheid tussen invoer, verwerking en resultaat dat de opsplitsing zichtbaar maakt (I2).
- **Alternatief 2 — "Mock-up" laten vervallen én de bestaande Mockup Engine-implementatie meteen hernoemen.** *Afgewezen als onderdeel van dit besluit*: de implementatienaam (`ROOM_MOCKUPS`, "Mockup Engine" in `CLAUDE.md`) is een code-/deelsysteemkwestie, geen ketenbegrip; buiten de scope van T2 (zie hoofdstuk 6).
- **Alternatief 3 (voorgesteld) — Uitsluitend het ketenbegrip "Mock-up" laten vervallen ten gunste van de drie reeds vastgelegde begrippen, zonder de implementatie of enig ander ketenbegrip te raken.** Zie hoofdstuk 3. De enige lezing die consistent is met alle feiten (F1–F6) en met de reeds voltrokken opsplitsing in BUILD-007.

## 5. Consequenties van het besluit

- De architectuurwoordenschat kent voortaan drie onderscheiden begrippen (Scene, Floor Visualization Engine, Visualisatie) op de plaats waar de Architectuurvisie ooit "Mock-up" had; dit sluit naadloos aan op de keten zoals BUILD-007 die al beschrijft (F2).
- **Geen enkel bestaand document wordt door dit besluit gewijzigd.** De vermelding "Mock-up" in de ontwerpketen van `DESIGN_BRAIN_ARCHITECTUURVISIE.md` (F1, regel 18) blijft staan tot de Architectuurvisie zelf wordt herschreven of vervangen — dat is agendapunt **T12** (consolidatie), niet dit besluit.
- De bestaande **Mockup Engine** (implementatie in `app.js`) blijft volledig ongewijzigd en behoudt haar rol als technische basis onder Scene (F5). Dit besluit raakt geen code.
- De v1-scope-keuze "mockups (fysieke ruimte-informatie) vallen buiten het DesignContext Model" (F6) blijft ongewijzigd; dit besluit gaat daar niet over.

## 6. Scope-afbakening (wat dit besluit uitdrukkelijk niet doet)

- Het raakt de bestaande **Mockup Engine**-implementatie **niet** (geen hernoeming, geen buitengebruikstelling, geen codewijziging).
- Het besluit **niet** over "Iteratieve verfijning", het andere begrip op dezelfde ketenregel (F1) — dat valt buiten T2.
- Het herschrijft of archiveert de Architectuurvisie **niet** (T12).
- Het wijzigt de DesignContext-v1-scope rond mockups/fysieke ruimte-informatie **niet** (F6).

### Verduidelijking (begrip versus implementatie)

Ter voorkoming van verwarring tussen het gelijknamige begrip en systeem:

- **"Mock-up" vervalt als architectuurbegrip** — het is geen zelfstandig ketenbegrip meer (hoofdstuk 3).
- **De bestaande Mockup Engine is een technische implementatie** ("Bekijk in ruimte", `ROOM_MOCKUPS` in `static/js/app.js`) en valt **buiten de scope van dit besluit**; zij wordt hier niet gewijzigd, hernoemd of buiten gebruik gesteld.
- **Toekomstige implementaties van Scene zijn niet afhankelijk van de huidige Mockup Engine.** Scene is een gestandaardiseerd invoer-object (F3); de huidige Mockup Engine is slechts de eerste render-basis en kan later worden vervangen **zonder architectuurwijziging**, zolang Scene hetzelfde gestandaardiseerde object blijft leveren.

## 7. Conclusie

Een **volledig** Architectuurbesluit is hier mogelijk: de opsplitsing is in de actuele keten al voltrokken (F2/F4), de drie vervangers bestaan elk afzonderlijk en met eigen verantwoordelijkheid (F3), en het verouderde begrip leeft alleen nog in de nog te herschrijven Architectuurvisie (F1/T12). Het onderscheid met de gelijknamige, blijvende Mockup Engine-implementatie is expliciet bewaakt (F5/I3). Het voorstel (hoofdstuk 3, K1–K3) wordt in zijn geheel ter goedkeuring voorgelegd.
