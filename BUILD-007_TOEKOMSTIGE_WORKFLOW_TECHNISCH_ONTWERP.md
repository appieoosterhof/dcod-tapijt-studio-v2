# BUILD-007 — De toekomstige Dessinator-workflow: technisch ontwerp

**Status:** technisch ontwerp, ter bespreking. Geen implementatie, geen Python-klassen, geen API-endpoints, geen database, geen UI. Bouwt uitsluitend voort op het goedgekeurde `BUILD-007_TOEKOMSTIGE_WORKFLOW_FUNCTIONEEL_ONTWERP.md` en op de reeds vastgestelde architectuur (SPEC-000, het DesignContext Model, BUILD-004, BUILD-005, BUILD-006, VISION-001).

---

## 0. Architectuurprincipes (herbevestigd, geen nieuwe)

Dit document introduceert geen nieuwe principes. Twee bestaande principes gelden onverkort voor de volledige keten, niet uitsluitend voor de componenten waarvoor ze oorspronkelijk zijn vastgesteld:

- **"Iedere AI-component produceert interpretaties, nooit waarheden"** (BUILD-004, hoofdstuk 0). Dit geldt voor elk AI-gedreven onderdeel in de keten — niet alleen Context Interpreter, maar ook elk toekomstig AI-gedreven onderdeel van Floor Design en Material Profile. Elk resultaat van zo'n component draagt de status "voorgesteld" totdat de architect het bevestigt.
- **Additieve, geïsoleerde koppeling** (BUILD-001B/Fase 2a, herhaald in BUILD-004 en BUILD-005): componenten kennen elkaar niet rechtstreeks, ze delen uitsluitend een gegevensstructuur of communiceren via een expliciet gedefinieerde interface. Geen component roept een ander component aan "omdat het toevallig kan."

Nieuw in dit document is uitsluitend de **toepassing** van deze principes op de volledige, vastgestelde keten — geen nieuwe architectuurbesluiten.

## 1. Overzicht van de keten en type van elk object

De vastgestelde keten bestaat uit objecten van verschillende aard. Om verantwoordelijkheden scherp te houden, wordt dat onderscheid hier expliciet gemaakt:

| # | Object | Aard | Status |
|---|---|---|---|
| 1 | Project | Gegevenscontainer (identiteit/opdrachtcontext) | Nieuw, nog niet technisch uitgewerkt |
| 2 | Ontwerpvraag | Ruwe invoer (vrije tekst + evt. voorbeeldvisies) | Nieuw, nog niet technisch uitgewerkt |
| 3 | DesignContext | Domeinmodel | Vastgesteld, geïmplementeerd (BUILD-001 t/m 004) |
| 4 | Context Interpreter | Verwerkende component (AI) | Vastgesteld, geïmplementeerd (BUILD-004) |
| 5 | Conversation Planner | Verwerkende component (deels regelgebaseerd, deels AI) | Vastgesteld, ontworpen, nog niet geïmplementeerd (BUILD-005) |
| 6 | Floor Design | Resultaat-object van de ontwerpfase | Nieuw, nog niet technisch uitgewerkt |
| 7 | Material Profile | Resultaat-object (materiaaleigenschappen) | Nieuw, nog niet technisch uitgewerkt |
| 8 | Scene | Gestandaardiseerd invoer-object (ruimte) | Vastgesteld, geïmplementeerd (BUILD-006) |
| 9 | Floor Visualization Engine | Verwerkende component | Vastgesteld in naam/rol (VISION-001), nog niet gebouwd |
| 10 | Visualisatie | Resultaat-artefact (geen eigen verwerkingslogica) | Nieuw, nog niet technisch uitgewerkt |
| 11 | Design Transfer Package | Resultaat-object (bundeling) | Nieuw, nog niet technisch uitgewerkt |
| 12 | DCOD | Ontvangende partij (mens) | Geen technisch object — buiten de technische architectuur |

Dit onderscheid is functioneel: alleen object 4, 5 en 9 zijn *verwerkende componenten* met eigen logica. De overige objecten zijn gegevenscontainers of resultaten. Dat is relevant voor hoofdstuk 5 — een resultaat-object kan namelijk geen "verantwoordelijkheid" schenden, alleen een verwerkende component kan dat.

## 2. Verantwoordelijkheden per architectuurobject

- **Project** — identificeert en bundelt de opdrachtcontext waarbinnen één of meer Ontwerpvragen plaatsvinden. Geen relatie met de gelijknamige architectuurlaag "DCOD Project Brain" (de overkoepelende architectuur uit BUILD-005, hoofdstuk 5) — die naamsovereenkomst is toeval, geen synoniem (zie hoofdstuk 8).
- **Ontwerpvraag** — legt de ruwe, ongeïnterpreteerde vraag van de architect vast, inclusief eventuele herhalingsrondes binnen hetzelfde gesprek (zie de vraag-lus in hoofdstuk 4). Bevat zelf geen interpretatie, geen laagtoewijzing.
- **DesignContext** — ongewijzigd, het bevroren domeinmodel (SPEC-000, DesignContext Model v1.0). Enige structuur die interpretaties, lagen en de doorlopende Ontwerpredenering bundelt.
- **Context Interpreter** — ongewijzigd (BUILD-004). Zet vrije tekst om in voorgestelde interpretaties, elk met een mate van zekerheid, ondergebracht in de juiste DesignContext-laag.
- **Conversation Planner** — ongewijzigd (BUILD-005-ontwerp). Bepaalt op basis van `DesignContext.interpretaties` precies één vervolgstap: vraag, samenvatting, of stilzwijgend doorgaan.
- **Floor Design** — het voorgestelde ontwerpresultaat van de ontwerpfase: een herkenbare richting die de architect kan bevestigen, bijstellen of afwijzen. Zoals in het functioneel ontwerp vastgesteld: geen samenvoeging van bestaande DesignContext-lagen en geen tweede centraliteitsclaim naast DesignContext. **De precieze technische afleiding uit DesignContext wordt in dit document bewust niet vastgelegd** (zie hoofdstuk 8) — dat zou een architectuurbesluit zijn dat nog niet is genomen.
- **Material Profile** — de visuele en materiële eigenschappen (uitstraling, structuur, pooltype) van de gekozen vloerafwerking, afgeleid in samenhang met het Floor Design. Geen synoniem voor Materialisatie (DesignContext Model, laag 5) — die blijft een eigenschap van een ontwerp binnen de ontwerpfase.
- **Scene** — ongewijzigd (BUILD-006). Standaardiseert elke ruimte-invoer (DCOD Scene, eigen projectfoto, eigen 3D-impressie) tot één achtergrond + één vloerpolygon, ongeacht de bron.
- **Floor Visualization Engine** — voegt Floor Design, Material Profile en Scene samen tot één beeld. Werkt, conform VISION-001, uitsluitend met deze drie gestandaardiseerde objecten — nooit rechtstreeks met DesignContext of met de ruwe scene-brongegevens.
- **Visualisatie** — het resultaat-artefact van de Floor Visualization Engine. Geen eigen verwerkingslogica; puur het getoonde eindbeeld.
- **Design Transfer Package** — bundelt, zodra de architect tevreden is, de op dat moment bevestigde inhoud van DesignContext (de visie), Floor Design, Material Profile en Visualisatie tot één geheel dat DCOD's technische specialisten direct kunnen oppakken. Nadrukkelijk niet de opvolger van de offerte-/bestelfunctionaliteit — die blijft een apart bedrijfsproces.
- **DCOD** — de ontvangende partij (mens). Geen technisch object, het eindpunt van de keten.

## 3. Interfaces tussen de architectuurobjecten

Elke pijl hieronder is een expliciete interface — geen enkel object communiceert buiten deze lijst om met een ander:

- **Project → Ontwerpvraag**: de Ontwerpvraag draagt een verwijzing naar het Project waarbinnen ze gesteld is. Eenrichtingsafhankelijkheid.
- **Ontwerpvraag → DesignContext**: vrije tekst (initieel of een vervolgronde) wordt aan een DesignContext-instantie toegevoegd — nieuw bij een nieuw gesprek, aanvullend bij een vervolgronde.
- **DesignContext ↔ Context Interpreter**: bestaande interface uit BUILD-004. Context Interpreter leest vrije tekst en eventuele bestaande DesignContext-inhoud, en schrijft uitsluitend interpretaties terug.
- **DesignContext → Conversation Planner**: bestaande interface uit BUILD-005. Conversation Planner leest uitsluitend `DesignContext.interpretaties` — geen rechtstreekse aanroep van of naar Context Interpreter (bevestigd in BUILD-005, hoofdstuk 3: "kennen elkaar niet").
- **Conversation Planner → Ontwerpvraag (lus) of → Floor Design**: het enige vertakkingspunt in de keten. Bij de uitkomst "vraag" ontstaat een nieuwe ronde van architect-input die opnieuw als Ontwerpvraag de keten binnenkomt (zie hoofdstuk 4). Bij "samenvatting ter bevestiging" of "voldoende vastgesteld" gaat de keten door naar Floor Design.
- **DesignContext → Floor Design**: Floor Design wordt afgeleid uit de op dat moment vastgelegde inhoud van DesignContext. De precieze afleiding is een open punt (hoofdstuk 8), geen vastgesteld mechanisme.
- **Floor Design → Material Profile**: Material Profile wordt bepaald in samenhang met het al vastgestelde Floor Design — nooit andersom, conform de volgorde uit het functioneel ontwerp ("zodra de richting staat, verschuift het gesprek...").
- **Scene**: onafhankelijk aangeleverd, geen afhankelijkheid van Floor Design of Material Profile — kan op elk moment in het gesprek gekozen of aangemaakt worden (bestaand, BUILD-006).
- **Floor Design + Material Profile + Scene → Floor Visualization Engine**: het eerste convergentiepunt — drie gestandaardiseerde objecten, geen enkele rechtstreekse toegang tot DesignContext of ruwe scene-brongegevens.
- **Floor Visualization Engine → Visualisatie**: resultaat, geen aparte interface-onderhandeling — Visualisatie is het artefact zelf.
- **DesignContext (visie) + Floor Design + Material Profile + Visualisatie → Design Transfer Package**: het tweede convergentiepunt, exact de vier elementen die het functioneel ontwerp noemt ("de visie, het Floor Design, het Material Profile, de visualisatie").
- **Design Transfer Package → DCOD**: levering aan een mens, geen technische interface in de zin van de overige pijlen — het eindpunt van de technische keten.

## 4. Gegevensstroom door de volledige keten

```
Project
   │  identiteit/opdrachtcontext
   ▼
Ontwerpvraag ◄────────────────────────────────┐
   │  vrije tekst                              │  "vraag"-uitkomst:
   ▼                                           │  nieuwe architect-input
DesignContext ──────► Context Interpreter      │  (herhaalt deze lus)
   │  ▲                  │ interpretaties       │
   │  └──────────────────┘                      │
   │                                            │
   ▼                                            │
Conversation Planner ───────────────────────────┘
   │  uitkomst: "voldoende vastgesteld" / "samenvatting bevestigd"
   ▼
Floor Design
   │
   ▼
Material Profile
   │
   │         Scene (onafhankelijk aangeleverd)
   │              │
   ▼              ▼
Floor Visualization Engine
   │  (uitsluitend Floor Design + Material Profile + Scene)
   ▼
Visualisatie
   │
   ▼  (samen met DesignContext-visie, Floor Design, Material Profile)
Design Transfer Package
   │
   ▼
DCOD
```

De lus tussen Ontwerpvraag, DesignContext en Conversation Planner is geen nieuwe scope — het is de technische vertaling van fase 3 uit het functioneel ontwerp ("soms een korte, gerichte vervolgvraag"), die per definitie een nieuwe ronde van architect-input veronderstelt.

## 5. Verificatie: één verantwoordelijkheid per component, uitsluitend interfaces

| Component | Eigen verantwoordelijkheid | Geen overlap met |
|---|---|---|
| Context Interpreter | Vrije tekst → interpretaties | Bepaalt geen vervolgstap (dat is Conversation Planner) |
| Conversation Planner | Interpretaties → vervolgstap | Wijzigt geen interpretaties, roept Context Interpreter niet aan |
| Floor Design | Ontwerprichting voorstellen | Neemt geen materiaal- of ruimtebeslissingen |
| Material Profile | Materiaaleigenschappen voorstellen | Neemt geen ontwerprichting, geen ruimtebeslissing |
| Scene | Ruimte-invoer standaardiseren | Weet niets van Floor Design, Material Profile of DesignContext |
| Floor Visualization Engine | Drie gestandaardiseerde objecten samenvoegen tot beeld | Leest nooit rechtstreeks DesignContext of ruwe scene-brongegevens |
| Design Transfer Package | Bevestigde eindstand bundelen | Genereert zelf niets nieuws, herformuleert niets |

Geen van de verwerkende componenten (Context Interpreter, Conversation Planner, Floor Visualization Engine) heeft een directe afhankelijkheid op een ander verwerkend component buiten de in hoofdstuk 3 genoemde interfaces — dit is dezelfde discipline die BUILD-003 al bewees voor `build_tile_svg()`/`build_repeat_svg()` en die BUILD-005 bevestigde voor Context Interpreter/Conversation Planner.

## 6. Relatie met bestaande BUILD's en VISION-001

- **BUILD-001 t/m 004 (DesignContext Model, Context Interpreter)** — ongewijzigd, vormen samen de technische basis van ketenstappen 3-4.
- **BUILD-005 (Conversation Planner)** — ongewijzigd, vormt de technische basis van ketenstap 5. Blijft gereserveerd, niet geïmplementeerd.
- **BUILD-006 (Scene Builder)** — ongewijzigd, vormt de technische basis van ketenstap 8.
- **VISION-001 (Floor Visualization Platform)** — levert het architectuurprincipe achter ketenstap 9 ("De vloerafwerking is het primaire ontwerpobject; de ruimte is uitsluitend context"), hier voor het eerst technisch toegepast op de volledige keten.
- **Ketenstappen 1, 2, 6, 7, 10, 11** (Project, Ontwerpvraag, Floor Design, Material Profile, Visualisatie, Design Transfer Package) hebben nog geen eigen BUILD — dit document beschrijft uitsluitend hun rol en interfaces, geen technische uitwerking op componentniveau.

## 7. Afbakening

Dit document bevat nadrukkelijk niet:
- Python-klassen of datastructuren.
- API-endpoints of routes.
- Databasekeuzes of opslagvorm.
- Schermontwerpen of UI-componenten.
- Een beslissing over welke ketenstappen een eigen BUILD worden of in welke volgorde.

## 8. Openstaande punten

- **Precieze afleiding van Floor Design uit DesignContext** — welke lagen, welke mate van bevestiging vereist is, is hier bewust niet vastgelegd. Kandidaat voor een eigen, toekomstig BUILD.
- **Naamsoverlap "Project" (ketenstap) versus "DCOD Project Brain" (architectuurlaag)** — geen synoniem, maar de gelijkenis is een risico voor toekomstige verwarring; aandachtspunt, geen besluit.
- **Persistentie van Floor Design, Material Profile en Design Transfer Package** — nog geen besluit, vergelijkbaar met hoe gespreksgeschiedenis en projectfase in BUILD-005 bewust abstract zijn gehouden.
- **Status-mechanisme (voorgesteld/bevestigd) voor Floor Design, Material Profile, Visualisatie en Design Transfer Package** — in dit document als principe verondersteld (consistent met het DesignContext Model), maar het technische mechanisme daarvoor is niet uitgewerkt.
- **De vervolgvraag-lus** (Conversation Planner → nieuwe architect-input → Context Interpreter opnieuw) is hier als patroon benoemd, maar hoe een vervolgantwoord technisch wordt herkend als aanvulling op dezelfde DesignContext — in plaats van een nieuw gesprek — is niet uitgewerkt.

Geen van deze punten vereist een besluit om dit technisch ontwerp te kunnen beoordelen — ze zijn hier zichtbaar gemaakt, niet opgelost, conform de werkwijze die dit gehele traject tot nu toe heeft gevolgd.
