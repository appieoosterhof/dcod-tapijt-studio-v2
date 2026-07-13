# BUILD-028 — Studio UX Architecture: technisch ontwerp

**Status:** architectuurspecificatie (Studio Experience Architecture, deel 3). **Geen code, geen implementatie, geen wijziging aan de Design Brain.** Beschrijft de complete gebruikerservaring van de DCOD Studio: de reis van eerste kennismaking tot vervolgprojecten, met de Dessinator als **ontwerpcollega** — geen chatbot, geen AI-assistent.

**Bindend / respecteert:** AB-006, AB-009, AB-012, BUILD-007, BUILD-021, BUILD-022, BUILD-023, IMP-014, BUILD-024, PLATFORM-001, PLATFORM-002, REASONING-001, SEC-001, BUILD-025, BUILD-026, BUILD-027.

**Kernprincipe (belevingsniveau):** de gebruiker ervaart **één ontwerpstudio**, niet een verzameling AI-functies. De UX-architectuur bindt de gespreksstroom (BUILD-025), de gesprekstoestand (BUILD-026) en de modaliteiten (BUILD-027) tot één samenhangende beleving bovenop de ongewijzigde Design Brain. De studio *begeleidt*; de mens *beslist*.

---

## 1. De Dessinator als ontwerpcollega

- **Geen chatbot** — geen vraag-antwoordritme, geen "commando's"; een doorlopend, samenhangend ontwerpgesprek.
- **Geen AI-assistent** — de gebruiker ziet nooit "AI", model, techniek of instellingen (AB-012); hij ervaart een vakkundige studio.
- **Samen ontwerpen** — de studio bouwt context op, verklaart keuzes, bewaakt consistentie en stelt onderbouwd voor (REASONING-001); de architect/ontwerper houdt de regie en bevestigt (AB-006/BUILD-007).

Dit is de directe voortzetting van het Ontwerpstudio-principe (BUILD-022 §9) en de belevingslaag (BUILD-021/IMP-013).

## 2. De gebruikersreis

| Stap | Beleving | Onderliggend (bestaand) |
|---|---|---|
| **Eerste kennismaking** | de studio verwelkomt, nodigt uit te vertellen wat de ruimte nodig heeft | Begroeting/Verkennen (BUILD-026); Context Interpreter |
| **Ontwerpgesprek** | een natuurlijk gesprek waarin wensen, functie en sfeer helder worden | Verdiepen/Samenvatten; Conversation Planner |
| **Ontwerpbegeleiding** | de studio denkt mee, legt afwegingen uit, biedt bewuste alternatieven | Bevestigen → Ontwerpen; strategie/concept/floor/material/pattern |
| **Visualisatie** | de gebruiker ziet het dessin — en in de ruimte | SVG-pipeline (BUILD-018), Floor Visualization Engine |
| **Materiaalkeuze** | technisch verantwoorde materiaalopties, uitlegbaar en vergelijkbaar | Material Planning (IMP-018) |
| **Presentatie** | een heldere, professionele weergave van het ontwerp en de onderbouwing | Presenteren (BUILD-026); Design Transfer Package |
| **Vervolgprojecten** | de studio onthoudt de context en helpt bij een volgend project | persistente `Gesprekstoestand`; nieuw `gesprek_id` per project |

De reis is **iteratief en niet-lineair**: de gebruiker mag terug, verfijnen, of van modaliteit wisselen zonder de draad te verliezen (BUILD-026-contextbehoud, BUILD-027-hybride gebruik).

## 3. Belevingsprincipes

- **Rust en continuïteit** — geen "opnieuw genereren"-ruis; hergebruikte resultaten verschijnen direct (BUILD-023 R2/R6), wat vakkundig aanvoelt.
- **Alles uitlegbaar** — elke ontwerpkeuze draagt een begrijpelijke motivering (REASONING-001); de gebruiker kan een voorstel vertrouwen én bijsturen.
- **De mens beslist** — voorstellen zijn "voorgesteld" tot de gebruiker bevestigt; de studio dwingt nooit (AB-006/§6 REASONING-001).
- **Eén verhaal** — "elke ruimte verdient een verhaal; de vloer maakt het compleet" (BUILD-022): de UX plaatst de vloer dienend binnen het ruimteverhaal, nooit als doel op zich.
- **Onzichtbare techniek** — laden, terugval, caching en AI blijven volledig onzichtbaar (AB-012); bij onbeschikbaarheid uitsluitend de neutrale studio-melding.

## 4. Toegankelijkheid & modaliteit

De UX is **modaliteit-agnostisch** (BUILD-027): dezelfde reis werkt via toetsenbord, spraak of beeld, op web, tablet en mobiel. Toegankelijkheid (spraak voor wie niet wil/kan typen, visuele weergave voor wie niet wil luisteren, `prefers-reduced-motion` uit IMP-013) is een eerste-klas UX-eis, geen bijzaak. Geen enkele modaliteit is verplicht; de gebruiker kiest en wisselt vrij.

## 5. Grenzen (expliciet)

- **UX ≠ Reasoning** — de UX rangschikt beleving en presentatie; alle ontwerpbeslissingen liggen in de Design Brain.
- **UX ≠ Workflow** — de UX begeleidt de gebruiker door de bestaande workflow (BUILD-007), zij herdefinieert die niet.
- **Experience ≠ Design Brain** — branding, toon, modaliteit en presentatie zijn Experience Layer; de Design Brain is er blind voor (PLATFORM-001/002).

## 6. Toekomstvastheid

Nieuwe kanalen, merken (DCOD, Dutch Carpets, dealers, white-label) en modaliteiten erven dezelfde UX-architectuur en dezelfde Design Brain; een nieuwe Experience Layer verandert branding/navigatie/rechten, nooit de ontwerpbeleving-in-de-kern of de contracten. Concrete implementatie- en privacykeuzes (bv. spraak/beeld naar externe diensten) zijn expliciete latere IMP-beslissingen (SEC-001).

---

## Consistentietoets

- **BUILD-021/022 / IMP-013:** de UX zet de bestaande belevingslaag en het Ontwerpstudio-principe voort; geen breuk.
- **REASONING-001:** uitlegbaarheid, bewuste variatie en "de mens beslist" zijn de dragende UX-principes.
- **AB-012:** de gehele beleving is techniek-loos; nooit model/sleutel/fout in beeld of spraak.
- **BUILD-007 / BUILD-023 / AB-006:** de reis volgt de bestaande ketenvolgorde, bevestigingsmomenten en reuse-/invalidatieregels.
- **BUILD-025/026/027:** de UX bindt gespreksstroom, gesprekstoestand en modaliteiten tot één beleving zonder hun grenzen te overschrijden.
- **PLATFORM-001/002 / SEC-001:** de UX leeft in de Experience Layer; merk/kanaal/modaliteit staan buiten de Design Brain; gevoelige data valt onder het privacybeleid.

---

**Reviewgereed:** dit ontwerp legt de Studio UX Architecture vast als de samenhangende beleving van de DCOD Studio — de Dessinator als ontwerpcollega (geen chatbot, geen AI-assistent), een iteratieve gebruikersreis van eerste kennismaking tot vervolgprojecten, belevingsprincipes (rust, uitlegbaarheid, de mens beslist, één verhaal, onzichtbare techniek), modaliteit-agnostische toegankelijkheid, en harde grenzen (UX≠Reasoning, UX≠Workflow, Experience≠Design Brain) — die de gespreksstroom (BUILD-025), gesprekstoestand (BUILD-026) en modaliteiten (BUILD-027) binden bovenop de volledig ongewijzigde Design Brain.
