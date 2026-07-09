# SPEC-000 — Project Charter

**Status:** concept, ter review. Nog niet gecommit. Dit document vormt het fundament waarop `DESIGN_CONTEXT_MODEL.md`, `DISCOVERY-004_ONTWERPPRINCIPE.md`, `DESIGN_BRAIN_ARCHITECTUURVISIE.md` en de BUILD-/RELEASE-serie worden gepositioneerd. Het bevat uitsluitend architectuurbesluiten die tijdens eerdere sessies definitief zijn vastgesteld — er is geen nieuwe inhoud toegevoegd.

---

## 1. Missie

De DCOD Dessinator laat architecten en interieurontwerpers binnen minuten een passend vloerconcept vinden.

De Dessinator heeft niet als doel een ontwerpvisie te bedenken of te ontdekken. De architect beschikt al over een ontwerpvisie. De missie van de Dessinator is deze bestaande ontwerpvisie te begrijpen, te verrijken en te vertalen naar een realiseerbaar vloerconcept.

## 2. Visie

De DCOD Dessinator is geen configurator, geen patroonbibliotheek en geen AI-afbeeldingengenerator. De Dessinator is een digitale ontwerpassistent die samen met een interieurarchitect een vloerconcept ontwikkelt.

Vóór de introductie van het DesignContext Model was de Dessinator in essentie een SVG-generator: een functie die tekst omzette in een patroon. De visie is dat de Dessinator, gebouwd op een eigen ontwerpmodel (DesignContext), toekomstige intelligente begeleiding van architecten mogelijk maakt — niet als los generatie-hulpmiddel, maar als partij in een ontwerpdialoog.

*(Ter onderscheid van de gelijknamige, specifiek gedefinieerde term "Ontwerpvisie" uit het DesignContext Model — hoofdstuk 2 hier betreft de visie van het project/product zelf, niet de ontwerpvisie van een individuele architect.)*

## 3. Kernwaarden

- **Evolueren, niet herbouwen.** De bestaande, bewezen Dessinator blijft de basis. Nieuwe architectuur bewijst zichzelf ernaast, niet in plaats van.
- **Eén bron van waarheid.** Voor elke gemigreerde beslissing bestaat precies één plek waar die wordt vastgesteld — nooit twee concurrerende implementaties van dezelfde vertaalslag.
- **Gecontroleerde migraties.** Elke BUILD migreert één, scherp afgebakende beslissing, nooit meerdere tegelijk.
- **Rollback bij iedere BUILD.** Elke stap is in minuten terug te draaien door een enkele, geïsoleerde wijziging ongedaan te maken.
- **Bewijs vóór aannames.** Elke migratie wordt getest op identieke output vóór livegang — nooit op basis van "dit zou moeten werken".
- **De architect bepaalt de ontwerpvisie.** DCOD's systemen mogen interpreteren en voorstellen, maar alleen de architect kan de ontwerpvisie definitief bevestigen.
- **DCOD ondersteunt en faciliteert.** De rol van DCOD — en van elke functie die namens DCOD handelt — is het inbrengen van vakkennis en het bewaken van haalbaarheid, niet het overnemen van de beslissing die bij de architect hoort.

## 4. Doelgroep

- **Architecten en interieurontwerpers** — de gebruikers van de Dessinator, eigenaar van de ontwerpvisie en het project.
- **DCOD** — drager van vakkennis namens het bedrijf: stijlkennis, materiaalkennis en productiekennis; vertaalt en bewaakt de haalbaarheid.

## 5. Wat de Dessinator niet is

- Geen configurator.
- Geen patroonbibliotheek.
- Geen AI-afbeeldingengenerator.
- Geen systeem dat informatie verzamelt via een vragenlijst.
- Geen systeem dat bepaalt welke oplossing "de juiste" is.
- Geen vervanging van de architect: de Dessinator neemt nooit de rol van ontwerper over.

## 6. Architectuurprincipes

- Het **DesignContext Model** is het centrale domeinmodel waarop alle functionaliteit wordt gebaseerd.
- Nieuwe intelligentie wordt vóór de bestaande AI-pipeline geplaatst; de SVG-generator is uitsluitend een uitvoerende component — alle ontwerpintelligentie bevindt zich vóór de generator.
- Elke ontwerpbeslissing kent een eigen eigenaar, een eigen beslisproces en een eigen verantwoordelijkheid — geen generieke, uniforme status voor alle lagen.
- Componenten die met DesignContext werken, worden niet als één monolithisch geheel ontworpen, maar als een verzameling afzonderlijke, onafhankelijk migreerbare componenten.
- Projectcontext is leidend: de Dessinator gebruikt de beschikbare context om zelf te bepalen welke informatie al bekend is en welke vragen nog relevant zijn.
- Snelheid is een harde ontwerpregel: iedere nieuwe functie moet de weg van idee naar vloer verkorten.
- Collecties zijn optioneel: ze kunnen inspiratie bieden maar bepalen nooit zelfstandig het ontwerp.

## 7. Governance

- **Ontwerpvisie:** uitsluitend de architect kan deze definitief bevestigen.
- **Project-/Ruimtecontext:** de architect levert de feiten (het is zijn project), DCOD structureert en categoriseert deze.
- **Ontwerpstrategie:** DCOD ontwikkelt deze samen met de architect — DCOD brengt vakkennis in, de architect bewaakt dat de strategie de ontwerpvisie recht blijft doen.
- **Concept en Materialisatie:** gedeeld eigenaarschap — DCOD stelt voor, de architect stuurt bij.
- **Productierealisatie:** volledig DCOD-eigendom (zuivere techniek en productiekennis).
- **Geen enkele component van de Design Brain mag zelfstandig ontwerpbeslissingen definitief bevestigen wanneer die volgens het DesignContext Model eigendom zijn van de architect of van de gezamenlijke dialoog tussen architect en DCOD.** De Design Brain mag voorstellen doen, onderbouwen en signaleren, maar nooit de rol van de architect overnemen.
- **Git-governance:** `main` vertegenwoordigt altijd de huidige productieversie en is beschermd. Alle ontwikkeling vindt uitsluitend plaats op `preview`. Workflow: preview → uitgebreid testen → DCOD akkoord → merge naar main → automatische productie-deploy.

## 8. Documenthiërarchie

```
SPEC-000 (dit document)                        — fundament, positioneert alle overige documenten
   └── DESIGN_CONTEXT_MODEL.md                 — bevroren domeinmodel (het "wat" en "wie beslist")
         ├── DISCOVERY-004_ONTWERPPRINCIPE.md      — ontwerpprincipes voor de dialoog met de architect
         ├── BUILD-serie (BUILD-001 t/m BUILD-003) — concrete, gefaseerde implementatiestappen
         │     └── RELEASE-serie                    — periodieke samenvattingen van opgeleverde BUILD's
         └── DESIGN_BRAIN_ARCHITECTUURVISIE.md     — softwarelaag die het domeinmodel gebruikt (het "hoe"),
                                                       geen nieuw domeinmodel; uitgangspunt voor toekomstige BUILD's
```

Het DesignContext Model is en blijft de canonieke domeinbeschrijving. Architectuurschetsen zoals de Design Brain-visie zijn nadrukkelijk geen vervanging of herziening daarvan.

## 9. BUILD-methodiek

- Elke BUILD migreert of introduceert één, scherp afgebakende verantwoordelijkheid — nooit meerdere tegelijk.
- Voorafgaand aan iedere migratie wordt een adviesdocument opgesteld dat kandidaten rangschikt op migratierisico, impact op architectuur, impact op gebruiker en technische complexiteit.
- Elke BUILD kent een expliciete Definition of Done, Acceptatietest en Rollback-beschrijving.
- Elke migratie wordt getest op identieke output vóór livegang (Parallelle Validatie), zodat de migratie transparant is voor de gebruiker.
- Nieuwe componenten van de Design Brain worden niet als één geheel geïmplementeerd, maar als afzonderlijke BUILD's die elk één verantwoordelijkheid toevoegen, apart worden getest, en pas daarna de basis vormen voor de volgende BUILD.

## 10. Samenwerking

De Dessinator ondersteunt de dialoog tussen vakgenoten, niet de instructie van een systeem aan een gebruiker. DCOD ontwikkelt de ontwerpstrategie samen met de architect: DCOD brengt vakkennis in, de architect bewaakt de ontwerpvisie.

De Dessinator spreekt nooit in absolute adviezen. Vermijd formuleringen zoals "Ik adviseer...", "De beste oplossing is...", "U moet...". Gebruik formuleringen zoals "U zou kunnen overwegen...", "Deze richting sluit waarschijnlijk goed aan bij uw ontwerpvisie omdat...", "Ik laat u graag meerdere richtingen zien.", "Welke richting past volgens u het beste bij uw ontwerp?".

## 11. Ontwerpfilosofie

De kern van de Dessinator is niet de prompt, maar de ontwerpcontext. De Dessinator verzamelt geen informatie; de Dessinator ontwikkelt samen met de architect een ontwerpdialoog. Hij helpt de architect sneller tot betere ontwerpbeslissingen te komen — niet door het ontwerp over te nemen, maar door de juiste ondersteuning op het juiste moment te bieden.

## 12. Ontwerpprincipes

- Het vertrekpunt van iedere sessie is de ontwerpvisie van de architect. Niet de prompt. Niet de AI. Niet een reeks vragen.
- Een architect hoeft geen goede prompt te schrijven. Een architect hoeft uitsluitend zijn ontwerpvisie te beschrijven. Het is de verantwoordelijkheid van de Dessinator om deze correct te interpreteren.
- De Dessinator genereert geen vragen omdat informatie ontbreekt. De Dessinator genereert alleen vragen wanneer de kwaliteit van het uiteindelijke ontwerp daardoor aantoonbaar verbetert.
- De architect hoeft niet vanaf een leeg scherm te beginnen: de Dessinator biedt herkenbare voorbeeldvisies aan die helpen de eigen ontwerpvisie sneller te formuleren — als inspiratie en herkenning, nooit als beperkende keuze. De eigen ontwerpvisie van de architect blijft altijd leidend. Deze voorbeeldvisies worden geschreven vanuit de taal van architecten — niet vanuit producten, dessins of materialen, maar vanuit ruimtelijke doelen, bijvoorbeeld:
  - Een warme, rustige uitstraling met natuurlijke materialen en veel daglicht.
  - Een vloer die verschillende functies subtiel met elkaar verbindt.
  - Een representatieve entree die bezoekers intuïtief begeleidt.
  - Een rustige werkomgeving waarin akoestisch comfort centraal staat.
  - Een hotellobby waarin ontmoeten en verblijven samenkomen.
  - Een interieur waarin de vloer de identiteit van de organisatie versterkt.

  Deze voorbeeldvisies zijn slechts een startpunt. De Dessinator interpreteert altijd de uiteindelijke ontwerpvisie van de architect, niet de voorbeeldtekst.
- De Dessinator bepaalt nooit welke oplossing "de juiste" is.
- Een ontwerpvoorstel is nooit een ontwerpbeslissing. Een ontwerpvoorstel sluit aantoonbaar aan op de ontwerpvisie, wordt onderbouwd vanuit ruimtelijke doelen, laat ruimte voor alternatieven, en nodigt de architect uit om te bevestigen, aan te passen of af te wijzen.
- De Dessinator voert ongeveer 80% van het denkwerk uit. De architect neemt 100% van de ontwerpbeslissingen. Dit evenwicht vormt de kern van de DCOD Ontwerpdialoog.

## 13. Projectprincipes

- Kleine, geïsoleerde, direct testbare stappen. Altijd een backup/commit vóór een risicovolle wijziging.
- Bij twijfel over scope of aanpak eerst een korte vraag stellen in plaats van aannames te doen — vooral bij dingen die de live Dessinator kunnen breken.
- `git commit` is lokaal en veilig. `git push` triggert een automatische productie-deploy en vereist daarom altijd expliciete toestemming vooraf.
- Architectuurdocumenten worden eerst als concept behandeld totdat ze inhoudelijk zijn gereviewd; pas na expliciete goedkeuring worden ze gecommit.

## 14. Ontwerpstudies

Een Ontwerpstudie is een mogelijke ontwerprichting binnen een project. Een studie vormt het uitgangspunt voor verdere ontwikkeling en kan meerdere varianten bevatten.

## 15. Succescriterium

Een migratie of nieuwe functionaliteit is pas geslaagd wanneer:

- de bestaande functionaliteit volledig behouden blijft;
- de gebruiker het verschil met de vorige situatie niet kan waarnemen, tenzij het expliciete doel van de wijziging is dat wel zichtbaar te maken;
- dit is aangetoond door test, niet aangenomen.

## 16. Toekomstvisie

BUILD-004 richt zich op de eerste echte DesignContext-gestuurde dialoog met de architect — het moment waarop DesignContext niet langer alleen bestaande beslissingen overneemt, maar voor het eerst een rol speelt in hoe die dialoog zelf verloopt. Daarna wordt de Design Brain uitgewerkt als verzameling afzonderlijke componenten (onder andere Context Interpreter, Ontwerpstrategie-stap, Reasoning Engine, Material Planner, Pattern Planner, SVG Planner, Conversation Planner), elk als eigen, gecontroleerde BUILD.

## 17. Begrippenlijst

- **Architect** — de gebruiker van de Dessinator; eigenaar van de ontwerpvisie en het project.
- **DCOD** — drager van vakkennis namens het bedrijf; vertaalt en bewaakt de haalbaarheid.
- **DesignContext** — het centrale domeinmodel/beslisobject van de Dessinator.
- **Visie** — de visie van de DCOD Dessinator als product (zie hoofdstuk 2). Niet te verwarren met "Ontwerpvisie".
- **Ontwerpvisie** — laag 1 van het DesignContext Model; de beleving/bedoeling van de architect binnen een project; exclusief architect-eigendom. Niet te verwarren met "Visie".
- **Project-/Ruimtecontext** — laag 2; situeert de visie in een concrete opdracht.
- **Ontwerpstrategie** — laag 3; de professionele vertaalslag tussen visie/context en concept; gezamenlijk ontwikkeld.
- **Concept** — laag 4; de concrete esthetische invulling (stijl, kleur, complexiteit); gedeeld eigenaarschap.
- **Materialisatie** — laag 5; de ontwerptechnische vertaalslag naar het fysieke eindproduct; gedeeld eigenaarschap.
- **Productierealisatie** — laag 6; zuiver technische/productiegerichte haalbaarheidstoets; volledig DCOD-eigendom.
- **Ontwerpredenering** — de doorlopende laag die niet alleen vastlegt wát is besloten, maar waarom, en de samenhang tussen alle lagen bewaakt.
- **Ontwerpsignatuur** — de eigen manier van ontwerpen van een architect; geen vaste stijl, nooit beperkend; in v1 sessiegebonden.
- **Ontwerpstudie** — een mogelijke ontwerprichting binnen een project; het uitgangspunt voor verdere ontwikkeling; kan meerdere varianten bevatten.
- **Design Brain** — de software-/redeneringslaag die het DesignContext Model gebruikt om intelligente ontwerpbeslissingen te nemen; géén nieuw domeinmodel.
- **BUILD** — een gecontroleerde, gefaseerde implementatiestap die één verantwoordelijkheid toevoegt.
- **SPEC** — een fundamenteel, structureel architectuurdocument (zoals dit charter).
- **DISCOVERY** — een definitief vastgesteld ontwerpprincipe uit de Discovery-fase.
- **preview** — de permanente ontwikkelbranch voor alle toekomstige BUILD's.
- **main** — de branch die de huidige productieversie vertegenwoordigt.

## 18. Wijzigingsprocedure

- Het DesignContext Model is bevroren: wijzigingen worden alleen doorgevoerd wanneer praktijktoetsing aantoont dat het model op een specifiek punt tekortschiet.
- Architectuurdocumenten doorlopen een concept-fase op `preview` vóór commit: eerst inhoudelijke review (consistentie met bevroren documenten, terminologie, volledigheid), dan een revisieronde, dan pas expliciete goedkeuring en commit.
- Wijzigingen aan `main` verlopen uitsluitend via een merge vanuit `preview`, na uitgebreid testen en DCOD-akkoord.
- Nieuwe architectuurprincipes worden nooit stilzwijgend toegevoegd aan een bevroren document; ze worden als nieuw, expliciet besluit vastgelegd.

## 19. De Belofte

Een architect hoeft geen goede prompt te schrijven. Een architect hoeft uitsluitend zijn ontwerpvisie te beschrijven — de Dessinator neemt de verantwoordelijkheid om deze correct te interpreteren, te verrijken en te vertalen naar een realiseerbaar vloerconcept.

De architect behoudt daarbij altijd het gevoel én de werkelijkheid dat hij de volledige controle heeft. De Dessinator ondersteunt en faciliteert; hij beslist nooit namens de architect.

## 20. De Gouden Regel

> Helpt deze functie de architect een betere ontwerpbeslissing te nemen, zonder de rol van ontwerper over te nemen?

Dit is de controlevraag die bij iedere nieuwe functionaliteit geldt. Wanneer het antwoord nee is, past de functionaliteit niet binnen de ontwerpfilosofie van de Dessinator.
