# BUILD-006 — Scene Builder

**Status:** geïmplementeerd, geverifieerd, nog niet gecommit. Eerste concrete stap onder `VISION-001_FLOOR_VISUALIZATION_PLATFORM.md`. Volledig losstaand van BUILD-004 (Context Interpreter) en BUILD-005 (Conversation Planner, gereserveerd) — geen van beide is aangeraakt.

## Doel

De eerste werkende versie van de Scene Builder realiseren: de basis van het Visualization Framework uit VISION-001.

## Scope (zoals opgegeven, ongewijzigd)

1. Nieuwe Scene aanmaken.
2. Achtergrondafbeelding uploaden.
3. Vier vloerhoeken interactief vastleggen.
4. Kalibratie opslaan in `scene.json`.
5. Bestaande Scene opnieuw kunnen openen.
6. Scene laden in de bestaande render-engine.
7. Verifiëren dat hetzelfde dessin bij iedere render identiek wordt geprojecteerd.

## Uitgangspunten (gehandhaafd)

- Eén Scene bevat één Surface (Floor).
- Eén Surface bevat één polygon (4 hoekpunten).
- Geen automatische detectie, geen AI — de vier hoekpunten worden altijd handmatig gesleept.
- Geen meerdere Surfaces.
- Geen wijziging van BUILD-004.
- Bestaande architectuur en Mockup Engine als basis: het polygon-formaat (`[TL, TR, BL, BR]`, fracties van de scene-afmetingen) is bewust identiek aan de bestaande `floorPoints` in `ROOM_MOCKUPS` (`static/js/app.js`), zodat een Scene zonder omzetting in de bestaande render-engine past.

## Wat is gebouwd

- **`scene_builder.py`** (nieuw) — het Scene-model (`Scene`, `Surface`) en de bijbehorende functies: `maak_scene()`, `sla_kalibratie_op()`, `laad_scene()`, `lijst_scenes()`. Slaat elke scene op als eigen map onder `static/scenes/<id>/` (`scene.json` + achtergrondbestand).
- **`app.py`** (additief) — vijf nieuwe routes (`/scene-builder`, `GET/POST /api/scenes`, `GET /api/scenes/<id>`, `POST /api/scenes/<id>/calibratie`). Geen bestaande route gewijzigd.
- **`templates/scene_builder.html`** + **`static/js/scene_builder.js`** (nieuw) — eigen, losstaande pagina: scene aanmaken (naam + upload), vier sleepbare hoekpunten op de afbeelding, opslaan, en een lijst van bestaande scenes om opnieuw te openen.
- **`.gitignore`** — `static/scenes/` toegevoegd (gebruikersgegenereerde inhoud, zelfde behandeling als de bestaande `exports/`).

## Acceptatiecriteria — geverifieerd

- ✓ **Een gebruiker kan binnen enkele minuten een nieuwe Scene aanmaken.** Geverifieerd via de echte UI: naam invullen, afbeelding uploaden, direct beschikbaar voor kalibratie.
- ✓ **Een opgeslagen Scene kan zonder informatieverlies opnieuw worden geopend.** Geverifieerd: aangemaakt, gekalibreerd, opnieuw opgehaald — polygon en naam kwamen exact overeen.
- ✓ **De render-engine gebruikt uitsluitend de opgeslagen Scene-informatie.** Geverifieerd door een Scene rechtstreeks in de bestaande Mockup Engine (`openVisualizer()`/`ruimteLayout()` in `app.js`, ongewijzigd) te laden — leverde een geldige `matrix3d`-transformatie op, zonder enige aanpassing aan die bestaande code.
- ✓ **Herhaald renderen geeft consistente resultaten.** Geverifieerd: dezelfde Scene tweemaal gerenderd gaf een bit-voor-bit identieke `matrix3d`-transformatie.
- ✓ **Voorbereid op toekomstige uitbreidingen, geen extra functionaliteit buiten scope.** `Surface.type` is al een veld (nu uitsluitend `"floor"`) zodat een toekomstige tweede Surface-type geen structuurwijziging vergt; er is geen automatische detectie, AI, of ondersteuning voor meerdere Surfaces toegevoegd.
- ✓ **Bestaande functionaliteit blijft ongewijzigd.** De bestaande `/api/generate`-flow is na deze wijzigingen opnieuw getest (live, via de etalage-directgeneratie) en werkt exact zoals voorheen.

## Rollback

Vier nieuwe bestanden verwijderen (`scene_builder.py`, `templates/scene_builder.html`, `static/js/scene_builder.js`) en de vijf additieve routes uit `app.py` terugdraaien (geen bestaande route is gewijzigd, alleen nieuwe toegevoegd). `static/scenes/` is niet gecommit (gitignored) en bevat uitsluitend gebruikersgegenereerde data.
