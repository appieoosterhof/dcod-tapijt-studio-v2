# AB-006 — Concept-Architectuurbesluit T5: Floor Design

**Status:** T5 inhoudelijk afgerond. Kernbesluiten K-A (eigenaarschap) en K-B (statusmechanisme) vastgesteld; K-C gedelegeerd naar T9, K-D gedelegeerd naar T13, K-E optioneel (VR-002). Hierdoor vrijgegeven: T9, T11, T13. Geen bestaand document gewijzigd, geen nieuw onderzoek, geen nieuwe architectuur.

**Scope:** uitsluitend agendapunt T5 (Floor Design — eigenaarschap, statusmechanisme, relatie tot Ontwerpstudie).

---

## 1. Onomstotelijke feiten

- **F1.** Floor Design is een resultaat-object *ná de ontwerpfase*: geen samenvoeging van Ontwerpstrategie/Concept, geen tweede centraliteitsclaim naast DesignContext — "een andere fase, een andere reikwijdte." Bron: BUILD-007 Functioneel r. 15; AB-001 F4.
- **F2.** Floor Design is het *voorgestelde* ontwerpresultaat; het draagt de status "voorgesteld" totdat de architect het bevestigt. Bron: BUILD-007 Technisch r. 11, 44.
- **F3.** Floor Design ontstaat op het enige vertakkingspunt in de keten: wanneer de Conversation Planner een andere uitkomst dan "vraag" kiest. Bron: BUILD-007 Technisch r. 60.
- **F4.** Floor Design heeft drie expliciete downstream-consumenten: Material Profile, Floor Visualization Engine, Design Transfer Package. Bron: BUILD-007 Technisch r. 62/64/66; AB-002 r. 24.

## 2. Wat door eerdere onderzoeken expliciet niet kon worden bewezen

- **N1.** Het *creërende component* van Floor Design: geen enkel document noemt een component die Floor Design maakt. Bron: AB-002 r. 55; AR-003 §4.
- **N2.** De *precieze afleiding* uit DesignContext: expliciet open, geen vastgesteld mechanisme. Bron: BUILD-007 Technisch h. 8; AB-001 h. 7.
- **N3.** *Eigenaarschap en statusmechanisme*: als principe verondersteld, technisch/architectonisch niet uitgewerkt; onbeslist. Bron: AB-002 r. 86; BUILD-007 Technisch r. 144.
- **N4.** De *relatie tot Ontwerpstudie* (SPEC-000 §14): niet vast te stellen of Floor Design hetzelfde begrip, een specialisatie, of onafhankelijk is. Bron: AB-001 I4/h. 7.
- **N5.** De *interne objectvorm/definitie*: nog niet technisch uitgewerkt; geen formele objectdefinitie. Bron: BUILD-007 Technisch r. 27; VR-001.
- **Grondslag:** AB-002 heeft vastgesteld dat het beschikbare historische bewijs voor N1–N4 is uitgeput — deze punten zijn *constitutief* (te kiezen), niet *afleidbaar*.

## 3. Architectuurkeuzes die de architect nu bewust moet nemen

Geen van deze volgt uit bewijs (hoofdstuk 2); elke keuze is een bewuste vaststelling.

### 3.1 Kernbesluiten — noodzakelijk om T5 af te sluiten

- **K-A — Eigenaarschap.** Wie bevestigt Floor Design definitief: de architect alleen, of gedeeld (DCOD stelt voor, architect stuurt bij)? *(betreft N3)*
- **K-B — Statusmechanisme.** Bevestigen dat Floor Design het "voorgesteld → bevestigd"-mechanisme volgt (consistent met F2), en vastleggen wie de status naar "bevestigd" mag zetten. *(betreft N3)*

> **K-D — Relatie tot Ontwerpstudie** is verwijderd uit de kernbesluiten van T5 en gedelegeerd naar **T13**; K-D blokkeert T5 niet langer. (Oorspronkelijke keuze, onveranderd: Floor Design is hetzelfde begrip als Ontwerpstudie, een specialisatie ervan, of onafhankelijk. *(betreft N4)*)

### 3.2 Afgeleide besluiten — pas na T5 te nemen

- **K-C — Ontstaan.** Ontstaat Floor Design door afleiding via een (nog te benoemen) component, of als resultaat van de gezamenlijke dialoog zonder eigen producent? *(betreft N1/N2)*
- **K-E — Objectdefinitie.** Wel/niet nu een formele objectdefinitie vaststellen (er is geen architectuurregel die dit afdwingt — VR-002). *(betreft N5)*

## 4. Vervolgbesluiten die hierdoor worden vrijgemaakt

- **T9** (relatie Reasoning Engine/Pattern Planner ↔ Floor Design) — vrijgegeven; **K-C** (ontstaan/afleiding) wordt binnen T9 behandeld.
- **T11** (asymmetrische DesignContext-toegang: Floor Visualization Engine vs Design Transfer Package) — vrijgegeven; **K-A/K-B** (eigenaarschap/status) zijn vastgesteld, waardoor "rechtstreeks bij DesignContext" begrensbaar wordt.
- **T13** (Conversation Planner: Project Brain of Design Brain) — vrijgegeven; **K-D** (relatie tot Ontwerpstudie) wordt binnen T13 behandeld.

---

Zodra de architect K-A t/m K-E heeft vastgesteld, is T5 besloten en zijn T9, T11 en T13 ontgrendeld.

---

## 5. Invulstructuur — in te vullen door de architect

Uitsluitend invulplaatsen. Nog geen antwoorden; wordt pas ingevuld nadat de architect de keuzes heeft genomen.

**5.1 Wanneer ontstaat Floor Design?** *(betreft K-C)*

> Het moment waarop Floor Design ontstaat wordt niet binnen T5 vastgesteld. Dit behoort tot K-C (ontstaan/afleiding) en wordt behandeld bij T9.

**5.2 Wie is eigenaar van Floor Design in iedere status?** *(betreft K-A)*

| Architectuurstatus | Eigenaar |
|---|---|
| Voorgesteld | Architect |
| Bevestigd | Architect |

> De Design Brain kan Floor Design genereren, maar is nooit eigenaar van Floor Design. Eigenaarschap berust gedurende de volledige levenscyclus bij de architect. De Design Brain heeft uitsluitend een producerende rol.

**5.3 Welke statussen kent Floor Design?** *(betreft K-B)*

> Floor Design kent uitsluitend twee architectuurstatussen:
>
> 1. **Voorgesteld**
>    - gegenereerd door de Design Brain;
>    - nog niet bevestigd door de architect.
>
> 2. **Bevestigd**
>    - expliciet bevestigd door de architect;
>    - vormt vanaf dat moment het geldige Floor Design voor verdere verwerking.
>
> **Verduidelijking.** De architectuurstatus van Floor Design staat los van de ontwerpfase.
>
> Architectuurstatus beschrijft uitsluitend de geldigheid van het Floor Design (Voorgesteld / Bevestigd).
>
> Ontwerpfasen (zoals Voorstudie, Schetsontwerp, Voorlopig Ontwerp en Definitief Ontwerp) behoren tot het ontwerptraject van de architect en maken geen onderdeel uit van de architectuurstatus.

**5.4 Wanneer wordt Floor Design bevestigd?** *(betreft K-B)*

> Floor Design wordt niet automatisch definitief.
>
> De overgang van 'Voorgesteld' naar 'Bevestigd' vindt uitsluitend plaats door een expliciete bevestiging van de architect.
>
> Deze bevestiging vormt een architectuurgebeurtenis. Vanaf dat moment geldt het bevestigde Floor Design als de geldige ontwerpbasis voor verdere verwerking door Material Profile, Floor Visualization Engine en Design Transfer Package.
