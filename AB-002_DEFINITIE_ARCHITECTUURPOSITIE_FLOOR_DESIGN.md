# AB-002 — Concept-Architectuurbesluit: definitie en architectuurpositie van Floor Design

**Status:** concept, ter beoordeling. Geen enkel bestaand document is gewijzigd. Vervolg op AB-001 (concludeerde dat een besluit over de afleiding van Floor Design niet mogelijk is zolang Floor Design's eigen identiteit onvoldoende is vastgelegd). Uitsluitend gebaseerd op `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, `SPEC-000_PROJECT_CHARTER.md`, `DESIGN_CONTEXT_MODEL.md`, BUILD-001 t/m BUILD-007, VISION-001, AR-001, AR-002 en AB-001.

---

## 1. Alle bestaande definities en beschrijvingen van Floor Design

Volledige inventarisatie, letterlijk, met bron:

- **BUILD-007 Functioneel Ontwerp, terminologiesectie:** "Floor Design — het centrale domeinobject ná de ontwerpfase. Geen samenvoeging van Ontwerpstrategie en Concept, en geen tweede centraliteitsclaim naast DesignContext — een andere fase, een andere reikwijdte."
- **BUILD-007 Functioneel Ontwerp, fase 4:** "Hier verschijnt voor het eerst iets tastbaars: het Floor Design — het resultaat van de ontwerpfase, niet één definitief antwoord, maar een richting die de architect kan herkennen, bijstellen of afwijzen. Voor een architect die snel wil, is dit een enkel, herkenbaar ontwerp om op te reageren; voor wie wil verkennen, is er ruimte om varianten te zien."
- **BUILD-007 Technisch Ontwerp, hoofdstuk 1 (classificatietabel):** "Floor Design | Resultaat-object van de ontwerpfase | Nieuw, nog niet technisch uitgewerkt."
- **BUILD-007 Technisch Ontwerp, hoofdstuk 2:** "Floor Design — het voorgestelde ontwerpresultaat van de ontwerpfase: een herkenbare richting die de architect kan bevestigen, bijstellen of afwijzen. [...] geen samenvoeging van bestaande DesignContext-lagen en geen tweede centraliteitsclaim naast DesignContext. De precieze technische afleiding uit DesignContext wordt in dit document bewust niet vastgelegd."
- **BUILD-007 Technisch Ontwerp, hoofdstuk 3 (interfaces):** "DesignContext → Floor Design: Floor Design wordt afgeleid uit de op dat moment vastgelegde inhoud van DesignContext. De precieze afleiding is een open punt." / "Floor Design → Material Profile: Material Profile wordt bepaald in samenhang met het al vastgestelde Floor Design." / "Floor Design + Material Profile + Scene → Floor Visualization Engine." / "DesignContext (visie) + Floor Design + Material Profile + Visualisatie → Design Transfer Package."
- **BUILD-007 Technisch Ontwerp, hoofdstuk 5 (verificatietabel):** "Floor Design | Ontwerprichting voorstellen | Neemt geen materiaal- of ruimtebeslissingen."
- **BUILD-007 Technisch Ontwerp, hoofdstuk 8:** "Precieze afleiding van Floor Design uit DesignContext — welke lagen, welke mate van bevestiging vereist is, is hier bewust niet vastgelegd. Kandidaat voor een eigen, toekomstig BUILD."
- **VISION-001, Architectuurprincipe:** "De vloerafwerking is het primaire ontwerpobject. De ruimte is uitsluitend context voor de visualisatie." — noemt de term "Floor Design" zelf nergens (zie hoofdstuk 9, tegenstrijdigheden/aandachtspunten).
- **`DESIGN_BRAIN_ARCHITECTUURVISIE.md`, `SPEC-000_PROJECT_CHARTER.md`, `DESIGN_CONTEXT_MODEL.md`, DISCOVERY-004, RELEASE_0.2:** geen van deze documenten noemt "Floor Design" — de term komt uitsluitend voor in BUILD-007-documenten en de daarop volgende reviews (AR-001, AR-002, AB-001).

## 2. Aard van Floor Design: architectuurobject, gegevensobject, ontwerpresultaat, tussenresultaat, of iets anders?

- **Feit:** BUILD-007 Technisch Ontwerp classificeert Floor Design expliciet als "Resultaat-object", in een tabel die dit onderscheidt van "Verwerkende component" (hoofdstuk 1). Floor Design is dus, per bestaand document, geen component met eigen verwerkingslogica.
- **Feit:** Floor Design heeft meerdere, elk expliciet benoemde downstream-consumenten (Material Profile, Floor Visualization Engine, Design Transfer Package) — het functioneert daarmee aantoonbaar als resultaatobject in een keten, niet als eindpunt.
- **Interpretatie:** binnen "de ontwerpfase" wordt Floor Design omschreven als "het resultaat" (BUILD-007, fase 4) — dus als afsluiting van die fase; binnen de volledige twaalf-stappen-keten functioneert het als tussenresultaat, omdat er nog drie stappen op volgen vóór DCOD. Beide typeringen zijn correct, maar op een verschillend schaalniveau — geen van beide documenten maakt dit onderscheid zelf expliciet.
- **Nog onbekend:** of Floor Design, net als de lagen van het DesignContext Model, een eigen voorgesteld/bevestigd-statusmechanisme krijgt. BUILD-007 Technisch Ontwerp hoofdstuk 8 noemt dit letterlijk als open punt ("Status-mechanisme... voor Floor Design... niet uitgewerkt"). Zonder een vastgesteld statusmechanisme is niet vast te stellen of Floor Design een eenmalig, definitief resultaat is, of een object dat — zoals de DesignContext-lagen — meerdere versies/statussen kan doorlopen.

## 3. Eigenaarschap van Floor Design

- **Feit:** geen enkel gereviewd document kent Floor Design een formele eigenaarschapsclassificatie toe, zoals SPEC-000 §7 (Governance) dat wel doet voor elke DesignContext-laag (bijvoorbeeld "Concept: gedeeld eigenaarschap — DCOD stelt voor, de architect stuurt bij").
- **Interpretatie:** BUILD-007 fase 4 omschrijft het architect-gedrag ten opzichte van Floor Design als "herkennen, bijstellen of afwijzen" — een interactiepatroon dat sterk lijkt op het gedeelde eigenaarschap van Concept (laag 4: "DCOD stelt voor, architect stuurt bij"). Dit is een aannemelijke gelijkenis, geen vastgelegd besluit.
- **Nog onbekend:** een expliciete eigenaarschapsclassificatie voor Floor Design zelf, conform het format van SPEC-000 §7.

## 4. Wanneer ontstaat Floor Design in de architectuur?

- **Feit:** BUILD-007 Technisch Ontwerp hoofdstuk 3 legt het triggermoment vast: Floor Design ontstaat op het moment dat de Conversation Planner concludeert dat de keten kan doorgaan ("voldoende vastgesteld" / "samenvatting bevestigd" in plaats van de "vraag"-uitkomst).
- **Hypothese (AB-001, I4, onbevestigd):** dit triggermoment valt mogelijk samen met de derde Conversation Planner-uitkomst uit BUILD-005 ("het voorstel om een eerste Ontwerpstudie te starten"), gezien de inhoudelijke gelijkenis tussen de definitie van Ontwerpstudie (SPEC-000 §14) en de omschrijving van Floor Design (BUILD-007, fase 4). Dit is niet bevestigd in enig document.

## 5. Welke input is noodzakelijk?

- **Feit:** BUILD-007 Technisch Ontwerp stelt dat Floor Design wordt afgeleid "uit de op dat moment vastgelegde inhoud van DesignContext" — zonder te specificeren welke lagen.
- **Hypothese (AR-002/AB-001, onbevestigd en deels tegenstrijdig — zie hoofdstuk 9):** Ontwerpstrategie (laag 3) en Concept (laag 4) zijn plausibele kandidaat-inputs, omdat dit de lagen zijn die inhoudelijk het dichtst bij "een ontwerprichting" liggen. AB-001 toonde echter aan dat deze hypothese op gespannen voet staat met de expliciete uitspraak dat Floor Design "geen samenvoeging van Ontwerpstrategie en Concept" is.
- **Nog onbekend:** welke specifieke DesignContext-velden, en welke mate van bevestiging daarvan, noodzakelijk zijn.

## 6. Welke output vormt Floor Design voor de volgende architectuurstap?

- **Feit, goed gedocumenteerd (in tegenstelling tot punt 5):** Floor Design is een expliciet benoemde input voor drie downstream-interfaces:
  - Floor Design → Material Profile (Material Profile "wordt bepaald in samenhang met het al vastgestelde Floor Design");
  - Floor Design (+ Material Profile + Scene) → Floor Visualization Engine;
  - Floor Design (+ DesignContext-visie + Material Profile + Visualisatie) → Design Transfer Package.
- **Observatie:** er bestaat een duidelijke asymmetrie in documentatiegraad — waar Floor Design vandaan komt (input, punt 5) is nauwelijks vastgelegd; waar het naartoe gaat (output, dit punt) is juist drie keer expliciet en consistent beschreven.

## 7. Welke component is verantwoordelijk voor het creëren van Floor Design (indien aantoonbaar)?

- **Feit:** geen enkel document noemt een component die Floor Design creëert. BUILD-007 Technisch Ontwerp hoofdstuk 1 wijst drie "verwerkende componenten" aan (Context Interpreter, Conversation Planner, Floor Visualization Engine) — geen daarvan is elders beschreven als producent van Floor Design: Floor Visualization Engine *consumeert* Floor Design (punt 6), en Conversation Planner produceert expliciet geen ontwerpinhoud (BUILD-005 Functioneel Ontwerp, hoofdstuk 2: "zelf informatie interpreteren (dat blijft de Context Interpreter); zelf ontwerpbeslissingen nemen... (dat blijft de architect)").
- **Hypothese (AR-002, getoetst en niet bevestigd in AB-001):** Reasoning Engine en/of Pattern Planner (`DESIGN_BRAIN_ARCHITECTUURVISIE.md`) zijn kandidaten, maar AB-001 concludeerde dat deze componenten, voor zover te herleiden, eerder gericht lijken op het vullen van DesignContext-lagen 3/4 dan op het produceren van een object dat expliciet "een andere fase, een andere reikwijdte" is dan die lagen.
- **Conclusie van dit punt:** niet aantoonbaar. Er is geen creërend component vast te stellen op basis van de huidige documenten.

## 8. Expliciet nog onbekende onderdelen (samenvatting van punt 2 t/m 7)

- Het statusmechanisme (voorgesteld/bevestigd) van Floor Design zelf.
- De formele eigenaarschapsclassificatie.
- De precieze input (welke DesignContext-lagen/velden, welke bevestigingsgraad).
- Het creërende component.
- De persistentie-/opslagvorm (al benoemd als open punt in BUILD-007 Technisch Ontwerp, hoofdstuk 8).
- De relatie tot Ontwerpstudie (SPEC-000 §14) — toeval of architectuurverband (hypothese, AB-001 I4).
- De relatie tot Reasoning Engine/Pattern Planner (`DESIGN_BRAIN_ARCHITECTUURVISIE.md`) — onbevestigd, deels tegenstrijdig (AB-001).

## 9. Tegenstrijdigheden en aandachtspunten tussen documenten

- **Hoofdbevinding (herhaling van AB-001, hier herbevestigd als uitgangspunt):** `DESIGN_BRAIN_ARCHITECTUURVISIE.md` positioneert zijn nog te bouwen "Reasoning"-laag inhoudelijk bij de DesignContext-ontwerpfase (lagen 3/4); BUILD-007 plaatst Floor Design expliciet buiten die fase. Geen van beide documenten spreekt zichzelf tegen — de spanning ontstaat pas wanneer beide naast elkaar worden gelegd.
- **Nieuwe bevinding (dit document):** VISION-001 — het document waarop BUILD-007 voor het visualisatiedeel van de keten zegt voort te bouwen — noemt de term "Floor Design" zelf nergens. Floor Design is dus uitsluitend gedefinieerd binnen het document dat het zelf ook gebruikt (BUILD-007); het is nooit onafhankelijk voorgesteld of getoetst in het document dat er inhoudelijk aan vooraf zou moeten gaan. Dit is geen woordelijke tegenspraak, wel een aanwijzing dat Floor Design als begrip minder stevig verankerd is dan de andere, al langer bestaande architectuurbegrippen (DesignContext, Context Interpreter, Conversation Planner, Scene).

## 10. Voorgestelde besluittekst

Net als bij AB-001 is een deel van de vraag met de bestaande documenten te onderbouwen, en een deel niet.

**Deel A — wél te onderbouwen, ter goedkeuring voorgesteld:**

- Floor Design wordt formeel vastgelegd als **resultaat-object**, niet als verwerkende component (bevestiging van een reeds bestaande, consistente classificatie — geen wijziging).
- Het ontstaansmoment van Floor Design wordt formeel vastgelegd als: **het moment waarop de Conversation Planner een andere uitkomst dan "vraag" kiest** (bevestiging van een reeds bestaande, consistente vaststelling — geen wijziging).
- De output-relaties van Floor Design (naar Material Profile, Floor Visualization Engine, Design Transfer Package) worden formeel bevestigd zoals reeds vastgelegd in BUILD-007 Technisch Ontwerp — geen wijziging.

**Deel B — niet te onderbouwen, dus niet besloten:**

- Eigenaarschap, statusmechanisme, precieze input/afleiding, creërend component, persistentie, en de relatie tot Ontwerpstudie respectievelijk Reasoning Engine/Pattern Planner blijven onbeslist. Voor geen van deze punten is voldoende, onderling consistent bewijs in de bestaande documenten aanwezig om nu een Architectuurbesluit te nemen.

## 11. Conclusie: gedeeltelijk besluit mogelijk

Deel A bevestigt uitsluitend wat al consistent uit de bestaande documenten volgt — dit is eerder een **formalisering** dan een nieuw besluit, en wijzigt niets aan de architectuur.

Voor Deel B geldt: **een definitief Architectuurbesluit is nog niet mogelijk.** Floor Design's identiteit is, zoals AB-001 al concludeerde, onvoldoende expliciet vastgelegd om de afleidingsvraag te beantwoorden — en dit document toont aan dat dat niet alleen geldt voor de relatie met Reasoning Engine/Pattern Planner, maar ook voor eigenaarschap, statusmechanisme en het creërende component in het algemeen.

**Benodigde aanvullende informatie of besluitvorming om Deel B alsnog te kunnen besluiten:**

1. Een expliciete uitspraak over eigenaarschap van Floor Design (analoog aan SPEC-000 §7), inclusief motivering.
2. Een expliciete uitspraak of Floor Design een eigen voorgesteld/bevestigd-statusmechanisme krijgt, of een ander soort levenscyclus.
3. Een expliciete uitspraak over de relatie tussen Floor Design en Ontwerpstudie (SPEC-000 §14): hetzelfde begrip, een specialisatie ervan, of twee onafhankelijke begrippen.
4. Pas ná 1 t/m 3: hernieuwd onderzoek naar het creërende component en de precieze input — waarschijnlijk het eerstvolgende, logische vervolg op dit besluit (vergelijkbaar met AB-001), maar nadrukkelijk niet in dit document opgenomen conform de instructie om niet verder te gaan met relatieonderzoek voordat de identiteit van Floor Design zelf is vastgesteld.

Zolang deze punten open staan, geldt: **geen architectuurwijziging, huidige open status in BUILD-007 Technisch Ontwerp hoofdstuk 8 gehandhaafd**, aangevuld met de in dit document expliciet benoemde, nog bredere reikwijdte van wat onbekend is (eigenaarschap, statusmechanisme, creërend component).
