# BUILD-003 — Architectuuranalyse en adviesdocument

**Status:** analyse, geen implementatie. Doel is een onderbouwde keuze voor BUILD-003, niet nog een veld migreren.
**Vervolg op:** BUILD-001 (Foundation + Observation) en BUILD-002 (kleurpalet leidend vanuit DesignContext).

---

## 1. Welke ontwerpbeslissingen worden slechts op één plaats genomen?

Onderzocht: elke plek in `app.py` waar een van de generatie-bepalende waarden wordt vastgesteld of overschreven.

| Beslissing | Waar vastgesteld | Single source? |
|---|---|---|
| **Kleurpalet** | `api_generate()`, éénmalig (`analyse_prompt()` / direct-modus / `aangepast_palet`) | ✅ Ja — **al gemigreerd in BUILD-002** |
| **Complexiteit** (`complexity`) | `api_generate()`, uitsluitend via `analysis.get("complexity", "medium")` (afkomstig van `analyse_prompt()`) | ✅ Ja — geen enkele keyword-override raakt dit veld |
| **Repeat-type** (`repeat_type`) | `api_generate()`, uitsluitend `data.get("repeat_type", "full")`, direct doorgegeven aan `build_repeat_svg()` | ✅ Ja |
| **Tegelmaat** (`tile_cm`) | `api_generate()`, uitsluitend `data.get("tile_cm", 40)` | ✅ Ja |
| **Resolutie** (`dpi`) | `api_generate()`, uitsluitend `data.get("dpi", 150)` | ✅ Ja |
| **Motief-schaal** (`motief_schaal`, het tegelherhalingspercentage 25–200%) | `api_generate()`, uitsluitend `data.get("motief_schaal", 100)`, stuurt de deler-/tegelberekening in `build_tile_svg()` | ✅ Ja |
| Stijl (`style`) | `api_generate()` Stap 2 **én** nogmaals, onafhankelijk, in `build_tile_svg()` | ❌ Nee — bekende dubbele routering, bewust buiten scope (Fase 5) |
| Vormen (`shapes`) | Grotendeels via `analyse_prompt()`, maar de "alleen cirkel"-override in `api_generate()` zet `shapes` **en** `style` gelijktijdig | ⚠️ Grotendeels wel, maar verstrengeld met de stijl-beslissing — geen zuiver geïsoleerde beslissing |

---

## 2. Welke daarvan zijn inhoudelijk belangrijk genoeg?

Niet elke single-source-beslissing is een echte *ontwerpbeslissing* in de zin van het DesignContext Model — sommige zijn puur dimensionale configuratie zonder enige vertaalslag of keuzelogica:

- **Complexiteit** — inhoudelijk relevant: stuurt daadwerkelijk andere generator-parameters aan (zie bv. `generate_floral_svg`, `generate_medallion_svg`, `generate_bauhaus_svg` — complexiteit bepaalt aantal kolommen/zijden/rastercellen). Dit is een echte Concept-laag-beslissing, al gemodelleerd in `design_context.py`.
- **Repeat-type** — inhoudelijk relevant: vier wezenlijk verschillende visuele uitwerkingen (full/half-drop/brick/mirror) met eigen transformatielogica in `build_repeat_svg()`. Een Productierealisatie-beslissing met echte impact op het eindresultaat.
- **Motief-schaal** — technisch relevant (bepaalt tegeldichtheid/-grootte), maar definitorisch grensgeval: dit is vandaag een pure gebruikersslider zonder enige AI- of DCOD-tussenkomst, dus het past minder natuurlijk bij "DCOD stelt voor, architect stuurt bij" dan bij een zuiver technisch renderparameter.
- **Tegelmaat en resolutie** (`tile_cm`, `dpi`) — puur dimensionale doorgifte, geen enkele keuzelogica of vertaling. Laag inhoudelijk gewicht; migreren bewijst architectonisch weinig nieuws bovenop wat BUILD-002 al aantoonde.
- **Vormen** — inhoudelijk relevant, maar door de koppeling met stijl niet geschikt als *geïsoleerde* volgende stap.

Blijven over als serieuze kandidaten: **Complexiteit**, **Repeat-type**, **Motief-schaal**.

---

## 3. Rangschikking

| Kandidaat | Migratierisico | Impact op architectuur | Impact op gebruiker | Technische complexiteit |
|---|---|---|---|---|
| **Complexiteit** | Zeer laag (identiek profiel aan kleurpalet) | Laag (bewijst niets nieuws t.o.v. BUILD-002 — zelfde functie, zelfde patroon) | Onzichtbaar | Zeer laag |
| **Repeat-type** | Laag (single source, deterministisch, geen AI-ambiguïteit) | **Hoog** (bewijst dat DesignContext een *andere* consumerende functie kan aansturen — `build_repeat_svg()` i.p.v. `build_tile_svg()`) | Onzichtbaar bij correcte migratie | Gemiddeld (vier te onderscheiden codepaden) |
| **Motief-schaal** | Gemiddeld (raakt de kernberekening van tegelherhaling — n/deler-logica) | Gemiddeld (interessant, maar definitorisch geen zuivere "ontwerpbeslissing") | Onzichtbaar bij correcte migratie, maar rekenfout is direct zichtbaar (vervormd patroon) | Hoog (rekenlogica, niet alleen doorgifte) |

---

## 4. Kandidaten in detail (max. drie)

### Kandidaat A — Complexiteit

- **Waarom geschikt:** exact hetzelfde bewezen profiel als kleurpalet in BUILD-002 — single source, geen duplicatie, al gemodelleerd in `design_context.py` (`Concept.complexiteit`) en al onderdeel van de Parallelle Validatie sinds BUILD-001B (nul afwijkingen tot nu toe).
- **Geraakte code:** `build_tile_svg()` (parameter `complexity`), analoog aan de `kleurpalet_override`-aanpak.
- **Risico:** zeer laag — vrijwel een kopie van een al bewezen migratie.
- **Rollback:** identiek aan BUILD-002: één parameter, één fallback-regel.

### Kandidaat B — Repeat-type

- **Waarom geschikt:** single source, geen AI-ambiguïteit (puur een gebruikerskeuze uit vier vaste opties), én — belangrijker voor het doel van BUILD-003 — het wordt geconsumeerd door een **andere** functie dan kleurpalet en complexiteit (`build_repeat_svg()` in plaats van `build_tile_svg()`). Dat is precies het soort bewijs dat BUILD-003 vraagt: niet nog een veld in dezelfde functie, maar aantonen dat DesignContext een beslissing kan dragen die ergens anders in de pijplijn wordt gebruikt.
- **Geraakte code:** `build_repeat_svg()` (parameter `repeat_type`), aanroep in `api_generate()`. `Productierealisatie.repeat_type` bestaat al als veld in `design_context.py`, maar wordt nog niet gevuld in Fase 2/2b (dat was in BUILD-001 bewust uitgesteld tot na de Concept-laag) — dit vraagt dus eerst een kleine, additieve uitbreiding van de bestaande vertaalstap, vóór het leidend gemaakt kan worden.
- **Risico:** laag, met één aandachtspunt: `build_repeat_svg()` heeft vier te onderscheiden codepaden (full/half-drop/brick/mirror) — de acceptatietest moet alle vier expliciet doorlopen, niet alleen de standaardwaarde "full" zoals tot nu toe steeds is getest.
- **Rollback:** zelfde patroon als BUILD-002 — één parameter met expliciete fallback op de bestaande waarde.

### Kandidaat C — Motief-schaal (tegelherhalingspercentage)

- **Waarom mogelijk geschikt:** single source, en raakt een ander mechanisme dan beide vorige (de deler-/tegelberekening `n`/`g` in `build_tile_svg()`, niet alleen een doorgegeven waarde).
- **Geraakte code:** `build_tile_svg()`, specifiek de regels die `ratio`/`n`/`g` berekenen.
- **Risico:** hoger dan A en B — dit is de enige kandidaat waarbij de gemigreerde waarde ook daadwerkelijk in een **berekening** wordt gebruikt (niet alleen doorgegeven aan een generator-functie of transformatie-blok). Een fout hier is direct zichtbaar als een vervormd of niet-naadloos patroon.
- **Rollback:** zelfde fallback-patroon, maar de acceptatietest moet expliciet de naadloosheid van de tegeling verifiëren (niet alleen "identieke output", ook "nog steeds deelbaar door 400").
- **Kanttekening:** definitorisch twijfelachtig of dit een *ontwerpbeslissing* is in de zin van het bevroren DesignContext Model, of eerder een technisch renderparameter. Ik zou dit niet als eerste kiezen, maar wel als goede kandidaat voor een latere BUILD bewaren, juist omdat het een ander soort risico beproeft (rekenlogica in plaats van doorgifte).

---

## 5. Advies

**Repeat-type (Kandidaat B).**

Complexiteit is het veiligst, maar bewijst architectonisch niets nieuws — het is in essentie een herhaling van BUILD-002 met een ander veldnaam. Motief-schaal beproeft een interessant, ander risico (rekenlogica), maar is definitorisch minder zuiver een "ontwerpbeslissing" en draagt een reëel hoger risico op zichtbare fouten (vervormde tegeling) als er iets misgaat.

Repeat-type raakt precies de juiste balans die BUILD-003 vraagt: het is nog steeds single source en risicoarm (geen AI-ambiguïteit, vier vaste, bekende opties), maar het dwingt af dat DesignContext voor het eerst een beslissing draagt die door een **andere functie** dan `build_tile_svg()` wordt geconsumeerd — het eerste echte bewijs dat het domeinmodel niet toevallig samenvalt met één functie-aanroep, maar daadwerkelijk als doorlopende bron door de pijplijn heen werkt. Dat is precies wat BUILD-003 volgens de eigen doelstelling moet aantonen.

---

*Dit document is het adviesstuk voor de keuze van BUILD-003. Er is nog geen implementatie gestart.*
