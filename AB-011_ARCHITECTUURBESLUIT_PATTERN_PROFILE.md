# AB-011 — Concept-Architectuurbesluit: identiteit en eigenaarschap van het patroonresultaat (Pattern Profile)

**Status:** VASTGESTELD — architectuurbesluit. De identiteit en het eigenaarschap van het resultaat-object van de Pattern Planner (het **Pattern Profile**) zijn hiermee formeel vastgesteld. Geen technische implementatie. Verankerd in AB-006, AB-009, AB-010(A), BUILD-007, BUILD-010, BUILD-011, BUILD-012 en BUILD-013.

**Kern:** het patroonresultaat wordt vastgesteld naar hetzelfde, reeds bekrachtigde model als Floor Design (AB-006/AB-009) en Material Profile (AB-010). Er wordt **geen nieuwe component** geïntroduceerd — de Pattern Planner bestaat al (DESIGN_BRAIN). Wél krijgt het reeds impliciet bestaande patroon-**resultaat-object** een canonieke naam, **Pattern Profile** (zie de motivering in hoofdstuk 4); een resultaat-object is geen component en voegt geen verantwoordelijkheid toe.

---

## 1. Vaststaande feiten

- **F1.** De Pattern Planner is één van de planners in de Design Brain (DESIGN_BRAIN: Reasoning Engine → Material Planner / Pattern Planner / SVG Planner) en produceert patroonvoorstellen (BUILD-013).
- **F2.** Precedent: Floor Design (AB-006/AB-009) en Material Profile (AB-010) zijn elk een **zelfstandig resultaat-object buiten de DesignContext**, met status **Voorgesteld → Bevestigd**, geproduceerd door hun component (Reasoning Engine resp. Material Planner) en **bevestigd door de architect**.
- **F3.** De SVG Planner is **uitsluitend uitvoerend** (rendering); alle ontwerpintelligentie — dus ook de patroonbeslissing — ligt vóór de generator (DESIGN_BRAIN uitgangspunt 4; AB-005/AR-004).
- **F4.** Het patroon is een ontwerpbeslissing die vóór de generator ligt; laag 4 (Concept) bevat weliswaar "complexiteit/motiefschaal" binnen de ontwerpfase, maar het patroonresultaat ná de ontwerpfase is daarvan te onderscheiden — net zoals Floor Design en Material Profile te onderscheiden zijn van hun DesignContext-lagen.
- **F5.** Consistent gate-patroon: elke downstream-stap start op bevestigde upstream-objecten (Concept bevestigd → Floor Design; Floor Design bevestigd → Material Profile; per analogie Material Profile bevestigd → Pattern Profile).
- **Grondslag:** zoals AB-002 voor Floor Design vaststelde, zijn identiteit, eigenaarschap en statusmechanisme *constitutief* (te kiezen, niet uit bewijs af te leiden). De onderstaande keuzes worden voorgesteld op basis van F1–F5 en de bekrachtigde precedenten Floor Design/Material Profile, ter vaststelling.

## 2. Identiteit van het patroonresultaat (Pattern Profile)

- **K1-A — Wat het is.** Het **Pattern Profile** is het resultaat-object dat het voorgestelde patroon (de motiefstructuur/-uitwerking) vastlegt dat past bij het bevestigde Floor Design en Material Profile.
- **K1-B — Zelfstandig resultaat-object.** Het is een **zelfstandig resultaat-object**, geen onderdeel van een andere component.
- **K1-C — Buiten de DesignContext.** Het Pattern Profile bestaat **buiten** de DesignContext (analoog aan Floor Design en Material Profile); het is geen DesignContext-laag.
- **K1-D — Verhouding tot Materialisatie (laag 5).** Het Pattern Profile is **geen** synoniem voor en heeft **geen** relatie met laag 5 (Materialisatie): laag 5 betreft de materiaaleigenschap binnen de ontwerpfase, het Pattern Profile betreft het patroon als downstream-resultaat. Het staat er volledig los van.
- **K1-E — Producent.** De **Pattern Planner** produceert het Pattern Profile (F1), naar hetzelfde patroon als de Reasoning Engine het Floor Design en de Material Planner het Material Profile produceert.
- **K1-F — Eigenaar van de bevestiging.** De **architect** bevestigt het Pattern Profile (F2; het bevroren principe "de architect blijft eigenaar van alle bevestigingen").
- **K1-G — Statusovergangen.** **Voorgesteld → Bevestigd**. De Pattern Planner schrijft uitsluitend "Voorgesteld"; uitsluitend de architect kent "Bevestigd" toe.

## 3. Relatie Pattern Planner ↔ Pattern Profile

- **K2-A — Verantwoordelijkheid Pattern Planner.** De Pattern Planner vormt patroonvoorstellen op basis van het bevestigde Concept, Floor Design en Material Profile, motiveert elk voorstel, en bevestigt nooit (BUILD-013).
- **K2-B — Voorstel = voorgesteld Pattern Profile.** Een **patroonvoorstel is een Pattern Profile met status "Voorgesteld"**. Hiermee zijn de twee begrippen verzoend: "patroonvoorstel" (BUILD-013) en "Pattern Profile" beschrijven hetzelfde resultaat-object in respectievelijk de status Voorgesteld en (na bevestiging) Bevestigd.
- **K2-C — Verhouding component ↔ resultaat.** De **Pattern Planner is de component** (producent); het **Pattern Profile is het resultaat-object**. Dezelfde verhouding als Reasoning Engine ↔ Floor Design en Material Planner ↔ Material Profile.
- **K2-D — Einde van de verantwoordelijkheid.** De verantwoordelijkheid van de Pattern Planner eindigt bij het opleveren van één of meer voorgestelde Pattern Profiles (buiten de DesignContext, met motivering en herkomst). Hij bevestigt niet en voert geen downstream-verwerking uit.
- **K2-E — Bevestiging door de architect.** De architect kiest en bevestigt één voorgesteld Pattern Profile; daarmee gaat de status naar "Bevestigd".
- **K2-F — Downstream.** Het bevestigde Pattern Profile wordt geconsumeerd door de **SVG Planner** (die het patroon rendert; AB-005/AR-004 — uitsluitend uitvoerend). De verdere downstream-keten (Floor Visualization Engine, Design Transfer Package) werkt met het gerenderde resultaat conform de bestaande architectuur (BUILD-007); de precieze technische koppeling SVG ↔ visualisatie blijft een technische interface (AR-003, C4) en wordt hier niet heropend.

## 4. Overwogen alternatieven

- **Alternatief 1 — Het patroonresultaat gelijkstellen aan laag 4 (Concept, motiefschaal/complexiteit).** *Afgewezen*: laag 4 is een ontwerpfase-laag binnen de DesignContext; het patroonresultaat is een downstream-resultaat-object ná de ontwerpfase (F4), analoog aan Floor Design/Material Profile.
- **Alternatief 2 — Het patroonresultaat binnen de DesignContext plaatsen.** *Afgewezen*: strijdig met het precedent (resultaat-objecten buiten de DesignContext) en met "de DesignContext ongewijzigd houden".
- **Alternatief 3 — De Pattern Planner laten bevestigen, of het patroon in de SVG Planner laten ontstaan.** *Afgewezen*: strijdig met "de architect blijft eigenaar van alle bevestigingen" en met uitgangspunt 4 (de SVG Planner is uitsluitend uitvoerend; de patroonbeslissing ligt ervóór).
- **Alternatief 4 — Geen canonieke naam geven ("patroonresultaat" laten).** *Afgewezen als onvoldoende*: een resultaat-object dat door downstream-componenten wordt geconsumeerd en door de architect wordt bevestigd, heeft een eenduidige identiteit/naam nodig. **Pattern Profile** is de aantoonbaar noodzakelijke, minimale keuze, consistent met de naamgeving Material Profile — een resultaat-object, geen nieuwe component.
- **Alternatief 5 (voorgesteld) — Pattern Profile als zelfstandig resultaat-object buiten de DesignContext, geproduceerd door de Pattern Planner (status Voorgesteld), bevestigd door de architect, gerenderd door de SVG Planner.** Zie hoofdstuk 2 en 3 — de enige lezing die consistent is met F1–F5 en de bekrachtigde precedenten.

## 5. Consistentietoets en consequenties

- **AB-006 / AB-009 (Floor Design):** identieke structuur (zelfstandig resultaat-object, buiten DesignContext, Voorgesteld/Bevestigd, architect bevestigt). ✓
- **AB-010(A) (Material Profile):** identieke structuur, inclusief het gate-patroon (start op bevestigde upstream-objecten). ✓
- **BUILD-007:** het bevestigde patroon voedt, via rendering, de visualisatieketen; laag 5 (Materialisatie) blijft ongemoeid. ✓
- **BUILD-010/011/012/013:** consistent — Reasoning Engine, Material Planner en Pattern Planner delen hetzelfde component-↔-resultaat-patroon. **BUILD-013 §9 (openstaand punt) wordt hiermee gesloten**: de patroonvoorstellen van de Pattern Planner zijn voorgestelde Pattern Profiles.
- **Geen nieuwe component; de DesignContext blijft ongewijzigd; geen nieuwe functionele verantwoordelijkheid.**

## 6. Scope-afbakening (wat dit besluit niet doet)

- Geen technische implementatie of objectdefinitie op veldniveau.
- Geen uitspraak over de interne werking van de SVG Planner, de Floor Visualization Engine of de Design Transfer Package; de technische koppeling SVG ↔ visualisatie (AR-003 C4) wordt niet heropend.
- Geen wijziging aan het bevroren DesignContext Model of aan laag 4/laag 5.

---

De architect heeft K1-A t/m K1-G en K2-A t/m K2-F vastgesteld; de identiteit en het eigenaarschap van het Pattern Profile zijn hiermee formeel besloten en de onafhankelijke review van BUILD-013 kan worden uitgevoerd.
