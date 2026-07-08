# BUILD-001 — Technische integratie van het DesignContext Model

**Status:** architectuurontwerp, nog geen implementatie.
**Basis:** [DESIGN_CONTEXT_MODEL.md](DESIGN_CONTEXT_MODEL.md) (bevroren domeinmodel), de bestaande codebase (`app.py`, `modules_extra.py`, `static/js/app.js`, templates).
**Uitgangspunt:** de bestaande Dessinator wordt uitgebreid, niet herbouwd. Het bestaande response-contract, de SVG-generatoren, de mockup-engine en de Flask-architectuur blijven volledig intact.

---

## 1. Waar leeft het DesignContext Model in de codebase?

Een nieuwe, geïsoleerde module: **`design_context.py`**, naast `app.py` en `modules_extra.py` — niet erin.

Redenen voor deze plek:
- **Niet in `app.py`**: dat bestand is al 1171 regels en bevat routing, e-maillogica en AI-aanroepen door elkaar. Het domeinmodel moet er niet nog een verantwoordelijkheid bij krijgen.
- **Niet in `modules_extra.py`**: dat bestand heeft een heel andere, bewezen-stabiele rol (28 pure SVG-generator-functies, input → SVG-string, zonder enige kennis van "waarom" een kleur of stijl is gekozen). Die puurheid is precies wat we in de architectuuranalyse als waardevol hebben bestempeld — daar voegen we niets aan toe.
- **Wel dezelfde isolatie-filosofie als ooit bedoeld voor `geometry_engine/`**: een eigen module, met een eenrichtingsafhankelijkheid vanuit `app.py`, zelf onwetend van Flask, van SVG, en van de generator-functies.

`design_context.py` bevat het domeinmodel zelf (de zes lagen + de doorlopende Ontwerpredenering) en de functies die de eigenaarschaps- en autoriteitsregels uit het domeinmodel afdwingen (bijvoorbeeld: alleen een expliciete bevestiging door de architect maakt de Ontwerpvisie onaantastbaar). Het kent geen enkele afhankelijkheid richting `app.py` of `modules_extra.py` — de afhankelijkheid loopt uitsluitend één kant op: `app.py` → `design_context.py`.

---

## 2. Welke bestaande modules vullen het model?

| Laag | Gevuld door (bestaand) | Status |
|---|---|---|
| Ontwerpvisie | request-payload van `api_generate()` (het `prompt`-veld) | bestaat al, wordt nu ook in DesignContext gelegd |
| Project-/Ruimtecontext | inspiratie-flow (`?concept=`/`?project=` in `app.js`) → momenteel alleen impliciet aanwezig, verstopt in de `direct`-payload (`style`, `prompt`, `palet`) | **gedeeltelijk aanwezig, niet expliciet** — vraagt een kleine, additieve uitbreiding van de payload (zie §5) |
| Ontwerpstrategie | vandaag impliciet: de keyword-overrides in `api_generate()` én in `build_tile_svg()`, plus de stijlkeuze die uit `analyse_prompt()` komt | **bestaat, maar ongestructureerd en dubbel** |
| Concept | `analyse_prompt()`-resultaat: `style`, `palette`, `complexity`, `motif_size`, `shapes` | bestaat al, wordt 1-op-1 overgenomen |
| Materialisatie | **niets** — materiaalsoort, structuur, pooltype, tactiliteit, uitstraling, glans, textuur bestaan nergens in de huidige Dessinator | **volledig nieuw, geen bestaande vulling** |
| Productierealisatie | `tile_cm`, `repeat_type`, `dpi` (losse request-parameters), plus `build_repeat_svg()`'s interne repeat-logica en de (stub) `svg_to_png()` | bestaat al, maar als losse functieargumenten, niet als samenhangende laag |

---

## 3. Welke modules lezen het model?

- **`build_tile_svg()`** leest (uiteindelijk) de Concept-laag: stijl, palet, complexiteit, motiefschaal.
- **`build_repeat_svg()`** leest (uiteindelijk) de Productierealisatie-laag: tegelmaat, repeat-type, resolutie.
- **`api_bestelling()`** kán optioneel later een samenvatting van Ontwerpvisie/Concept lezen voor de offerte-e-mail — dit is een mogelijke verrijking, geen vereiste van BUILD-001.
- **De frontend (`app.js`, templates) leest het model nooit.** Dit is een expliciete architectuurbeslissing: DesignContext is een **server-side, intern domeinmodel**. De browser blijft uitsluitend het bestaande response-contract zien (`tile_svg_b64`, `repeat_svg_b64`, `info{...}`). Dit is wat de instructie "response-contract blijft volledig intact" in de praktijk betekent.

---

## 4. Welke modules mogen het model wijzigen?

**Uitsluitend `design_context.py` zelf.** Geen enkele andere module muteert het domeinmodel rechtstreeks. `app.py`'s route-functies roepen functies ván `design_context.py` aan (bijvoorbeeld: "leg deze visie vast", "bevestig deze visie", "ontwikkel de strategie") — ze grijpen nooit zelf in de onderliggende structuur.

Dit is bewust restrictief, om twee redenen:
1. De autoriteitsregels uit het domeinmodel (alleen de architect bevestigt de visie definitief; DCOD en architect ontwikkelen de strategie gezamenlijk) moeten **op één plek** worden afgedwongen. Als meerdere modules vrij mogen schrijven, verwatert die regel onvermijdelijk.
2. De generator-functies in `modules_extra.py` blijven zo gegarandeerd puur: zij ontvangen afgeleide parameters (palet, tegelgrootte, complexiteit), nooit het DesignContext-object zelf. Dat behoudt exact de eigenschap die we in de architectuuranalyse als stabiel en waardevol markeerden.

---

## 5. Welke bestaande functies moeten worden aangepast?

- **`api_generate()`**: krijgt aan het begin een aanroep die een DesignContext opbouwt/bijwerkt uit de inkomende payload. Dit is **additief** — de bestaande verwerkingsstappen (Claude-aanroep, stijl-overrides, SVG-opbouw) blijven ongewijzigd functioneren; DesignContext loopt in eerste instantie *naast* de bestaande flow, niet erin.
- **Request-payload**: een klein, additief nieuw veld voor het projecttype/ruimtecontext (vandaag alleen impliciet aanwezig via welk `direct`-voorbeeld is aangeklikt). Dit is een uitbreiding, geen wijziging van bestaande velden — bestaande aanroepen zonder dit veld blijven werken.
- **`build_tile_svg()` en `build_repeat_svg()`**: pas in een latere fase (zie §8, Fase 4) aangepast om hun waarden uit DesignContext te lezen in plaats van uit de losse `analysis`-dict / functieargumenten. Hun **interne werking verandert niet** — alleen waar ze hun input vandaan halen.

## 6. Welke functies blijven volledig ongewijzigd?

- Alle 28 `generate_*_svg()`-functies in `modules_extra.py` — geen enkele aanraking.
- `STYLE_GENERATORS`-registratie en de aanroepmechaniek ervan.
- `analyse_prompt()` — de Claude-aanroep zelf, het model, het system-prompt-schema: ongewijzigd. (De **interpretatie** van zijn output verandert — die wordt straks ook in DesignContext gelegd — maar de functie zelf doet niets anders dan vandaag.)
- De volledige mockup-/floorvisualizer-engine in `app.js` — buiten scope, zoals al vastgesteld bij het domeinmodel.
- `/api/export/svg`, `/api/export/png` (inclusief de bekende `svg_to_png()`-stub — dat blijft een apart, niet in deze bouwfase op te lossen punt).
- `api_bestelling()` — ongewijzigd in deze fase.
- Alle templates en alle bestaande frontend-JS.

---

## 7. Volledige gegevensstroom

```
Architect
   │  (typt vrije tekst, of kiest een project/concept in de inspiratie-flow)
   ▼
Invoer
   │  bestaande request-payload aan /api/generate
   │  (prompt, tile_cm, repeat_type, dpi, evt. direct-modus/palet)
   │  + additief: expliciet projecttype/ruimtecontext
   ▼
DesignContext                                    ← NIEUW (design_context.py)
   │  Ontwerpvisie + Project-/Ruimtecontext direct gevuld vanuit Invoer
   ▼
Analyse                                          ← analyse_prompt(), ONGEWIJZIGD
   │  resultaat wordt gelezen als (voorlopige) Ontwerpstrategie + eerste Concept
   ▼
Concept                                          ← bestaande analysis-velden,
   │  nu expliciet als DesignContext-laag benoemd   nu in DesignContext gelegd
   ▼
Materialisatie                                   ← NIEUW, in BUILD-001 een lege/
   │  structurele plek zonder actieve logica          standaard structuur
   ▼
Productierealisatie                              ← bestaande tile_cm/repeat_type/dpi,
   │  nu expliciet als DesignContext-laag benoemd      nu in DesignContext gelegd
   ▼
SVG                                              ← build_tile_svg()/build_repeat_svg(),
   │  interne werking ONGEWIJZIGD                     input komt later uit DesignContext
   ▼
Mockup                                           ← app.js floorvisualizer, volledig
   │  buiten het domeinmodel, ongewijzigd              ongewijzigd, consumeert alleen SVG
   ▼
CTA                                              ← api_bestelling(), ONGEWIJZIGD
      (optioneel later verrijkt met een DesignContext-samenvatting voor het salesteam)
```

De **doorlopende Ontwerpredenering** (uit het domeinmodel) loopt hier dwars doorheen: elke stap van Analyse tot en met Productierealisatie registreert in DesignContext niet alleen zijn resultaat, maar ook waarom — zodat een latere stap (bijvoorbeeld Productierealisatie die iets onhaalbaar verklaart) kan navragen wat de Concept- of Materialisatie-laag daarover al had vastgelegd, in plaats van dat blind te overschrijven.

---

## 8. Gefaseerde implementatie (elke fase blijft volledig werkend)

**Fase 1 — DesignContext als losstaande module, nog nergens aangesloten.**
`design_context.py` wordt gebouwd als volledig zelfstandig domeinmodel (structuur + eigenaarschapsregels uit het bevroren model), met eigen, geïsoleerde verificatie. Raakt `app.py` niet aan. Risico voor de live Dessinator: nihil.

**Fase 2 — Additieve koppeling, nog niet sturend.**
`api_generate()` bouwt bij elke aanroep een DesignContext op uit de bestaande payload en het bestaande `analyse_prompt()`-resultaat, en legt die vast — maar de bestaande flow (stijl-overrides, `build_tile_svg()`, `build_repeat_svg()`) blijft exact zoals hij is en negeert DesignContext volledig. Dit maakt het mogelijk om DesignContext tegen echt gebruik te toetsen zonder enig gedragsrisico.

**Fase 2a — Waarborg tegen uiteenlopen van DesignContext en de bestaande `analysis`-dictionary.**
Zolang DesignContext niet-sturend is, merkt niemand het als de vertaling naar DesignContext stilzwijgend kapot gaat door een latere wijziging aan `analyse_prompt()` of de keyword-overrides — de Dessinator blijft immers gewoon op `analysis` draaien. Om dat risico niet aan discipline alleen over te laten, gelden voor deze fase vier expliciete regels:

1. **Eén enkele vertaalfunctie.** Er komt precies één functie die `analysis` omzet naar `DesignContext.concept`. Geen enkele andere plek in de code leest zelfstandig uit `analysis` om DesignContext te vullen.
2. **Vers afgeleid, niet opgeslagen.** `DesignContext.concept` wordt bij elke request opnieuw afgeleid van de actuele `analysis`, nooit gemerged met een eerdere versie — dit sluit drift binnen één request per definitie uit.
3. **Tijdelijke controle die drift zichtbaar maakt.** Bij elke request worden de kernvelden (stijl, palet, complexiteit) van `analysis` en `DesignContext.concept` naast elkaar gelogd. Doel van Fase 2 is drift *opsporen*, niet aannemen dat hij niet optreedt — uitgewerkt als de **Parallelle Validatie** hieronder.
4. **Fase 2 is een tijdvenster, geen blijvende toestand.** Er geldt een expliciet exitcriterium (een vastgesteld aantal echte requests zonder afwijking) voordat naar Fase 4 wordt overgegaan. Hoe langer twee bronnen van dezelfde waarheid naast elkaar bestaan, hoe groter het risico — dit mag niet onbepaald blijven hangen. Zodra Fase 4 DesignContext sturend maakt, vervalt het risico structureel: er is dan nog maar één bron van waarheid.

**Fase 2b — Parallelle Validatie.**

De periode waarin `analysis` en `DesignContext` naast elkaar bestaan wordt actief benut om de kwaliteit van het nieuwe model te bewijzen — niet alleen om afwijkingen te signaleren, maar om te begrijpen waaróm ze ontstaan. `analysis` blijft in deze fase de bestaande waarheid; `DesignContext` wordt bij iedere request opnieuw, vers opgebouwd vanuit datzelfde `analysis`-resultaat (nooit uit een aparte, tweede aanroep van `analyse_prompt()` — anders wordt AI-variatie tussen twee losse aanroepen ten onrechte aangezien voor een vertaalfout). Daarna worden beide automatisch met elkaar vergeleken.

*Wat wordt vergeleken (minimaal):* Ontwerpstrategie (de gekozen aanpak), en binnen Concept: stijlfamilie, kleurpalet, complexiteit.

*Wat een afwijkingsrapport bevat:* per gevonden afwijking wordt vastgelegd (1) welke ontwerpbeslissing afwijkt — de betreffende waarde in `analysis` naast de betreffende waarde in `DesignContext`, (2) een beschrijving van de vermoedelijke oorzaak, en (3) welke laag van het DesignContext Model hierdoor geraakt wordt (Ontwerpstrategie en/of Concept, en of dit doorwerkt naar Materialisatie/Productierealisatie).

*Waarschijnlijke oorzaken van afwijkingen* — dit is waar de validatie zijn waarde bewijst, want niet elke afwijking is een fout in de vertaling zelf:
- **Verkeerd vastgelegd moment.** `analysis` wordt op meerdere momenten aangepast (het ruwe Claude-resultaat, dan de directe overrides in `api_generate()`, dan de interne keyword-matching in `build_tile_svg()`). Als de vertaalfunctie een te vroeg moment vastlegt, ontstaat een schijnbare afwijking die in werkelijkheid een timingfout in de vertaling is.
- **De twee bestaande, elkaar overlappende keyword-blokken spreken elkaar tegen.** Dit is een reeds bestaande zwakte (zie architectuuranalyse) die de Parallelle Validatie voor het eerst zichtbaar kan maken: als `api_generate()` en `build_tile_svg()` het onderling oneens zijn over de stijl, is de afwijking geen DesignContext-probleem maar een bevestiging van een bestaand risico — met directe input voor Fase 5.
- **Semantische mismatch bij het overzetten van velden** (bijvoorbeeld `motif_size` versus `motiefschaal`) — een echte vertaalfout, op te lossen in de vertaalfunctie zelf.

Bevindingen uit deze validatie zijn nuttige input voor Fase 5, ook al is het validatiemechanisme zelf tijdelijk. Na aantoonbaar succesvolle migratie naar een volledig DesignContext-gestuurde architectuur (Fase 4 afgerond) vervalt deze laag volledig — er is dan nog maar één bron van waarheid om tegen te vergelijken.

**Fase 3 — Productierealisatie en Materialisatie expliciet maken.**
`tile_cm`, `repeat_type`, `dpi` worden ook in DesignContext gelegd (naast hun bestaande, ongewijzigde gebruik in `build_repeat_svg()`); Materialisatie krijgt zijn structurele plek met standaardwaarden — nog zonder actieve keuzelogica, want die bestaat vandaag nergens in het product.

**Fase 4 — DesignContext wordt sturend voor Concept en Productierealisatie.**
Pas als Fase 2-3 aantoonbaar correct meelopen met de bestaande output: `build_tile_svg()` en `build_repeat_svg()` gaan hun waarden uit DesignContext lézen in plaats van uit de losse `analysis`-dict/argumenten. Per stijl getoetst tegen de oude output vóór livegang.

**Fase 5 — Consolidatie van de dubbele stijl-routering.**
De twee bestaande, elkaar overlappende keyword-blokken (in `api_generate()` en in `build_tile_svg()`) worden samengevoegd tot één bron, gevoed door DesignContext.Ontwerpstrategie. De globale `_ETALAGE_DIRECT_PAL`-state wordt vervangen door een expliciet DesignContext-veld.

**Fase 6 — Buiten BUILD-001.**
Daadwerkelijke Materialisatie-keuzelogica (materiaalcatalogus, selectieregels), eventuele verrijking van de CTA-e-mail met een DesignContext-samenvatting, reparatie van `svg_to_png()`. Losse, latere trajecten.

---

## 9. Refactoring: noodzakelijk vs. bewust niet

**Noodzakelijk, maar gefaseerd (niet gelijktijdig met de introductie van DesignContext):**
- Consolideren van de dubbele stijl-routeringslogica (Fase 5).
- Vervangen van de `_ETALAGE_DIRECT_PAL`-globalstate door een expliciet DesignContext-veld (Fase 5).
- Expliciet maken van `tile_cm`/`repeat_type`/`dpi` als samenhangende Productierealisatie-laag in plaats van losse functieargumenten (Fase 3-4).

**Bewust niet, in deze bouwfase:**
- Geen wijziging aan de 28 generator-functies in `modules_extra.py`.
- Geen wijziging aan het response-contract richting de frontend.
- Geen wijziging aan de mockup-/floorvisualizer-engine.
- Geen wijziging aan `analyse_prompt()`'s Claude-aanroepmechaniek (model, system-prompt-schema) — het uitsplitsen van Strategie en Concept in aparte AI-stappen is een legitieme toekomstige overweging, maar geen onderdeel van BUILD-001.
- Geen reparatie van `svg_to_png()` — bestaand, los probleem, niet vermengen met dit traject.

---

## 10. Softwarearchitectuur na afronding van BUILD-001

```
Browser (app.js, templates)  ── ONGEWIJZIGD ──────────────────────────────┐
        │ fetch('/api/generate', ...)                                      │
        ▼                                                                  │
Flask app.py (routes)                                                      │
        │                                                                  │
        ├──▶ design_context.py  (NIEUW — domeinmodel + eigenaarschapsregels)│
        │        │  vult/leest: Visie, Context, Strategie, Concept,        │
        │        │  Materialisatie, Productierealisatie, Ontwerpredenering │
        │        ▼                                                        │
        ├──▶ analyse_prompt()  (ONGEWIJZIGD — Claude-aanroep)              │
        │                                                                  │
        ├──▶ build_tile_svg() / build_repeat_svg()                        │
        │        gevoed door design_context.py in plaats van losse dict/args
        │        interne werking ONGEWIJZIGD                              │
        │        │                                                        │
        │        ▼                                                        │
        └──▶ modules_extra.py  (28 generatoren — VOLLEDIG ONGEWIJZIGD)     │
                 │                                                        │
                 ▼                                                        │
        Response { analysis, tile_svg_b64, repeat_svg_b64, info{...} } ────┘
        (contract IDENTIEK aan vandaag)
                 │
                 ▼
        Mockup-engine (app.js) — ONGEWIJZIGD
                 │
                 ▼
        api_bestelling() (CTA) — ONGEWIJZIGD
```

Het verschil met vandaag zit uitsluitend **tussen** de Flask-routes en de bestaande generatie-/repeat-functies: waar nu losse dicts en functieargumenten heen en weer gaan, zit straks één samenhangend, geëigenaarschapt domeinmodel — zonder dat de generator-laag, de mockup-laag, of de buitenkant van de API daar ooit iets van merkt.
