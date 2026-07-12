# REASONING-001 — Ontwerpfilosofie & Reasoning Principles

**Status:** architectuur- en kennisdocument. **Geen code, geen API-wijziging, geen boundary-wijziging, geen prompt-implementatie.** Legt de inhoudelijke ontwerpfilosofie van de Design Brain vast, zodat toekomstige Reasoning Capabilities redeneren vanuit de vastgelegde **ontwerpkennis van DCOD** — niet vanuit een AI-model.

**Aard:** dit document is **inhoudelijk leidend voor reasoning** en **model-, leverancier- en technologie-onafhankelijk**. Het beschrijft *waarop* een Reasoning Capability moet redeneren, niet *hoe* zij technisch wordt uitgevoerd. Waar deze filosofie en een bestaand architectuurbesluit elkaar zouden lijken te raken, blijft het bestaande besluit leidend; REASONING-001 introduceert geen nieuwe architectuur.

**Bindend / respecteert:** AB-006, AB-009, AB-012, BUILD-007, BUILD-023, IMP-014, BUILD-024, PLATFORM-001.

---

## Doel en scope

**Doel:** de ontwerpfilosofie van de Design Brain expliciet vastleggen, zodat elke huidige en toekomstige Reasoning Capability dezelfde onderbouwde, uitlegbare en reproduceerbare ontwerpkennis toepast — ongeacht welk model of welke leverancier de capability later implementeert.

**Binnen scope:** uitsluitend de ontwerpfilosofie en de reasoning-principes.
**Buiten scope:** technische implementatie, prompts, API-calls, modelkeuze en elke leveranciersspecifieke eigenschap (Anthropic, OpenAI of anderszins). Die horen bij latere IMP-trajecten en bij de boundary-implementatie, niet bij deze filosofie.

---

## 1. Ontwerpvisie

**De ontwerpvisie van DCOD.** Een vloer is geen achtergrond maar een **dragend ontwerpelement** van de ruimte. DCOD ontwerpt vloeren die een ruimte helpen *kloppen*: die de architectuur ondersteunen, de functie versterken en het verhaal van de ruimte compleet maken. Het dessin is nooit doel op zich; het is dienend aan de ruimte, de gebruiker en het gebruik. (Dit sluit aan op het studio-uitgangspunt "elke ruimte verdient een verhaal — de vloer maakt het compleet, maar ís niet het verhaal".)

**De rol van vloerontwerp binnen een interieur.** De vloer is het grootste aaneengesloten oppervlak in de meeste ruimtes en bepaalt mede: de sfeer, de akoestiek, de looproutes, de zonering en de eerste indruk. Een goed vloerontwerp maakt een ruimte rustiger of levendiger, groter of intiemer, formeler of informeler — bewust, niet toevallig.

**De relatie tussen architectuur, functie en vloer.** De vloer bemiddelt tussen wat de architectuur *is* (vorm, licht, materiaal, verhoudingen) en wat de ruimte *doet* (functie, doelgroep, gebruik). Ontwerpkeuzes vertrekken daarom altijd vanuit die driehoek — architectuur, functie, vloer — en nooit vanuit een losstaand esthetisch idee.

---

## 2. Reasoning Principles

Elke Reasoning Capability redeneert volgens dezelfde algemene principes:

- **Onderbouwd** — iedere ontwerpkeuze heeft een reden die naar de ontwerpvisie en de ontwerpfactoren herleidbaar is; geen keuze "omdat het mooi is".
- **Reproduceerbaar** — dezelfde bevestigde invoer en context leiden tot een consistente, navolgbare uitkomst; niet grillig per aanroep.
- **Bewuste variatie** — variatie ontstaat doelgericht (om betekenisvolle alternatieven te tonen), niet als willekeurige ruis.
- **Consistentie boven willekeur** — bij twijfel wint de keuze die samenhangt met eerdere, bevestigde keuzes en met de ontwerpvisie.
- **Uitlegbaar** — iedere aanbeveling gaat vergezeld van een begrijpelijke motivering in mensentaal, zonder jargon, model- of techniekverwijzing.
- **Dienend, niet dwingend** — reasoning stelt voor en onderbouwt; de gebruiker beslist (zie §6).

Deze principes zijn **capability-overstijgend**: strategie, concept, floor design, materiaal en patroon redeneren allemaal binnen hetzelfde kader, elk op hun eigen niveau.

---

## 3. Ontwerpfactoren

Een Design Brain weegt minimaal de volgende factoren af. Ze zijn geordend van *ruimtebepalend* (wat de ruimte vraagt) naar *realisatiebepalend* (wat haalbaar en houdbaar is):

**Ruimte & gebruik**
- **Ruimtefunctie** — wat gebeurt er (werken, ontvangen, verblijven, bewegen, rusten)?
- **Doelgroep** — voor wie (bezoekers, bewoners, medewerkers, gasten)?
- **Routing** — hoe bewegen mensen door de ruimte; waar liggen looplijnen en verblijfszones?

**Beleving & identiteit**
- **Sfeer** — de gewenste emotionele toon (rustig, warm, zakelijk, speels, verfijnd).
- **Identiteit** — merk, karakter of signatuur die de ruimte moet uitstralen.
- **Licht** — daglicht en kunstlicht bepalen hoe kleur, glans en textuur overkomen.

**Ontwerptaal**
- **Kleur** — palet en contrast, in relatie tot licht, sfeer en identiteit.
- **Materiaal** — soort, structuur, pooltype, tactiliteit.
- **Patroon** — motiefstructuur, herhaling, dichtheid.
- **Schaal** — motiefschaal in verhouding tot de ruimtemaat en de kijkafstand.

**Prestatie & realisatie**
- **Akoestiek** — bijdrage aan geluidsabsorptie en verblijfscomfort.
- **Onderhoud** — reinigbaarheid en vervuilingsgevoeligheid bij het verwachte gebruik.
- **Duurzaamheid** — levensduur, materiaalkeuze en verantwoorde productie.
- **Budget** — kostenkader dat keuzes begrenst.
- **Productie** — technische maakbaarheid en printbaarheid van het dessin.

Geen factor staat op zichzelf: kleur hangt aan licht, schaal aan ruimtemaat, materiaal aan onderhoud en akoestiek, patroon aan productie. Reasoning weegt ze **in samenhang**.

---

## 4. Afwegingsmodel

**Altijd prioritair (harde ondergrens).** Deze factoren mogen nooit worden weggeredeneerd; ze begrenzen alle overige keuzes:
- **ruimtefunctie** en **gebruik/routing** — een ontwerp dat de functie hindert, is geen goed ontwerp;
- **productie/maakbaarheid** — een onmaakbaar of onprintbaar dessin is geen oplossing;
- **budget** — een voorstel buiten het kader is geen bruikbaar voorstel.

**Contextafhankelijk (zwaarte varieert per opdracht).** Sfeer, identiteit, kleur, materiaal, patroon, schaal, licht, akoestiek, onderhoud en duurzaamheid krijgen hun gewicht *uit de opdracht*: in een hotellobby weegt identiteit/sfeer zwaar, in een zorgomgeving weegt akoestiek/onderhoud zwaar, in een kantoortuin weegt routing/akoestiek zwaar.

**Conflicten wegen.** Wanneer factoren botsen (bv. een gewenst fijn, druk motief versus productie-/onderhoudsgrenzen), geldt: (1) de harde ondergrens wint altijd; (2) daarbinnen wint de keuze die de **ruimtefunctie en de ontwerpvisie** het best dient; (3) de afweging wordt **expliciet gemotiveerd**, zodat de gebruiker de gemaakte prioritering ziet en kan bijsturen.

**Meerdere oplossingen naast elkaar.** Wanneer verschillende, legitieme ontwerprichtingen de opdracht *even goed* dienen (bv. een rustige versus een expressieve interpretatie van dezelfde sfeer), worden ze als **bewuste, onderscheiden alternatieven** naast elkaar voorgesteld — elk met eigen onderbouwing — in plaats van één richting willekeurig te forceren. Dit is de bewuste-variatie uit §2, niet vrijblijvendheid.

---

## 5. Onderbouwing

Elke ontwerpkeuze gaat vergezeld van een motivering die:
- **logisch** is — een navolgbare redenering van factor(en) naar keuze;
- **controleerbaar** is — herleidbaar naar de ontwerpvisie (§1), de principes (§2) en de gewogen factoren (§3/§4);
- **aansluit op de ontwerpvisie** — nooit strijdig met de dienende rol van de vloer;
- **geen willekeur bevat** — geen "smaak zonder reden"; als iets een keuze uit meerdere gelijkwaardige opties is, wordt dát benoemd.

De onderbouwing is bedoeld voor de **gebruiker**, in begrijpelijke taal, zonder model-, techniek- of leveranciersverwijzing (AB-012). Zij is **vrije tekst**: een uitleg om te lezen en op te vertrouwen, nooit een veld dat verderop in de keten machinaal wordt geparsed voor logica (conform BUILD-024).

---

## 6. Grenzen van reasoning

**Wat de Design Brain wél doet:** de ontwerpfactoren wegen, samenhangende voorstellen doen, alternatieven onderscheiden en elke keuze onderbouwen — als een deskundige ontwerpstudio die meedenkt.

**Wat de Design Brain níét doet:**
- **niet ongevraagd beslissen** — zij stelt voor; zij legt niets dwingend op;
- **niet buiten de opdracht treden** — geen keuzes die functie, budget of maakbaarheid negeren;
- **geen willekeur presenteren als ontwerp** — geen onderbouwingsloze of grillige uitkomsten;
- **geen zekerheid claimen die er niet is** — waar meerdere richtingen kloppen, toont zij die als keuze;
- **geen technische/AI-realiteit tonen** — nooit model, sleutel, kosten of foutdetails (AB-012).

**Wat altijd bij de gebruiker blijft:** de **bevestiging** van elke ontwerpstap. Voorstellen zijn "voorgesteld" tot de gebruiker ze "bevestigt"; pas dan schuift de keten door (BUILD-007 gates, AB-006-statusvocabulaire). De eindregie — welke richting, welk alternatief, wanneer door — ligt bij de mens; de Design Brain adviseert onderbouwd.

---

## 7. Relatie met Capabilities

De ontwerpfilosofie is **leidend**; Reasoning Capabilities zijn **implementaties** ervan (PLATFORM-001 §5). Concreet:
- elke Reasoning Capability (Ontwerpstrategie, Concept, Floor Design, Material, Pattern) **past deze principes toe** binnen haar eigen contract (BUILD-024), zonder de principes te wijzigen;
- een capability mag **rijker** worden (meer factoren fijnmaziger wegen) zolang zij binnen dezelfde filosofie en hetzelfde additieve contract blijft;
- **model-/leverancierswissel verandert de filosofie niet** — of een capability nu door het ene of het andere model, een regelsysteem of een hybride wordt uitgevoerd, zij redeneert op ditzelfde kader (BUILD-024 §5 boundary-onafhankelijkheid, AB-012);
- de filosofie is de **gedeelde bron van waarheid**: capabilities verwijzen ernaar, breiden haar niet eigenmachtig uit. Een wijziging van de filosofie is een bewuste update van REASONING-001, niet een neveneffect van een capability-implementatie.

---

## Consistentietoets

- **PLATFORM-001:** "filosofie is leidend, capabilities zijn implementaties" is de directe invulling van "AI is een capability"; geen strijdigheid.
- **AB-012:** onderbouwingen en voorstellen blijven vrij van model-, sleutel-, kosten- en foutinformatie; reasoning is en blijft voor de gebruiker een ontwerpstudio, geen techniek.
- **AB-006:** de "voorgesteld → bevestigd"-grens (§6) respecteert het bestaande statusvocabulaire en de bevestiging als gebruikersbeslissing.
- **AB-009:** Floor Design als reasoning-niveau valt onder dezelfde principes; geen aparte filosofie.
- **BUILD-007:** de gebruiker behoudt de bevestigingsregie; reasoning verandert de ketenvolgorde niet.
- **BUILD-023 / IMP-014:** "reproduceerbaar" en "bewuste variatie" sluiten aan op de orkestratie (hergebruik van geldige resultaten, reasoning alleen bij nieuwe ontwerpwaarde); de filosofie schrijft geen extra aanroepen voor.
- **BUILD-024:** onderbouwing als niet-geïnterpreteerde vrije tekst en capability-onafhankelijkheid sluiten exact op de contractregels aan.
- **Model-/leverancieronafhankelijkheid:** nergens wordt een model, prompt of leverancier genoemd; de principes zijn puur inhoudelijk en dus toekomstvast.

---

**Reviewgereed:** dit document legt de ontwerpfilosofie en reasoning-principes van de Design Brain vast — ontwerpvisie, algemene principes, ontwerpfactoren, afwegingsmodel, onderbouwing, grenzen van reasoning en de relatie met capabilities — model-, leverancier- en technologie-onafhankelijk, als de inhoudelijke bron van waarheid waarop elke huidige en toekomstige Reasoning Capability redeneert, zonder enige code-, API-, boundary- of prompt-wijziging en zonder afwijking van de bestaande architectuur (AB-006/009/012, BUILD-007/023/024, IMP-014, PLATFORM-001). Hiermee kan de eerste productie-reasoning-capability (Ontwerpstrategie) expliciet op deze filosofie worden gebaseerd.
