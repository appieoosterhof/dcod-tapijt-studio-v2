# BUILD-002 — Voorstel (nog niet goedgekeurd)

**Status:** voorstel. Geen implementatie, geen code. Pas te starten na akkoord.
**Vervolg op:** BUILD-001 (afgerond: Foundation + Observation, zie BUILD-001_DESIGNCONTEXT_INTEGRATIE.md).

## Doel van BUILD-002

BUILD-001 heeft DesignContext puur observationeel gemaakt: het loopt mee, het vergelijkt, maar het beïnvloedt niets. BUILD-002 zet de eerste, kleinst mogelijke stap waarbij DesignContext voor **één specifieke ontwerpbeslissing** daadwerkelijk leidend wordt in plaats van de bestaande `analysis`-dictionary — de eerste keer dat het model van "toeschouwer" naar "bron van waarheid" gaat, op precies één punt.

## Welke eerste ontwerpbeslissing wordt leidend

**`Concept.kleurpalet`** — het kleurpalet.

`build_tile_svg()` gaat het palet lezen uit `DesignContext.concept.kleurpalet` in plaats van uit `analysis.get("palette", ...)`, met de bestaande `analysis`-waarde als vangnet zolang DesignContext geen waarde heeft.

Nadrukkelijk **niet** de stijlkeuze (`Ontwerpstrategie.aanpak` / `Concept.stijlfamilie`) — dat blijft bewust bij Fase 5 van BUILD-001 horen, niet bij het begin van BUILD-002.

## Waarom dit de veiligste eerste migratie vormt

Uit de architectuuranalyse en de Fase 2b-validatie is één concreet, verifieerbaar verschil naar voren gekomen tussen de kandidaten:

- **Stijl** wordt op **twee plekken** bepaald (de keyword-overrides in `api_generate()` én, opnieuw en apart, in `build_tile_svg()` zelf). DesignContext ziet vandaag alleen het eerste moment. Stijl leidend maken zou dus impliciet de tweede keyword-laag buitenspel zetten — een echte gedragswijziging, niet alleen een verplaatsing.
- **Kleurpalet** wordt in de huidige code precies **één keer** vastgesteld (in `api_generate()`, via `analyse_prompt()`, de directe-modus, of `aangepast_palet`) en daarna nergens meer inhoudelijk gewijzigd — `build_tile_svg()` voegt alleen technische sleutels toe (`_tile_cm`, `_jp_prompt`), maar wijzigt nooit de kleurwaarden zelf.
- De Parallelle Validatie uit BUILD-001B heeft dit empirisch bevestigd: bij alle geteste generaties kwam `Concept.kleurpalet` exact overeen met de uiteindelijk gebruikte `analysis["palette"]` — nul afwijkingen.

Dat maakt dit een migratie waarbij de nieuwe en de oude bron **per definitie identiek** zijn, in plaats van een migratie die op vertrouwen rust.

## Definition of Done

- ✓ `build_tile_svg()` leest het kleurpalet uit `DesignContext.concept.kleurpalet`, met `analysis["palette"]` als expliciete fallback wanneer DesignContext geen waarde heeft.
- ✓ Geen andere ontwerpbeslissing (stijl, complexiteit, motiefschaal, repeat, resolutie) wordt aangeraakt.
- ✓ De Parallelle Validatie (Fase 2b) blijft actief en gebruikt om te bevestigen dat er vóór livegang nul afwijkingen zijn op het palet-veld.
- ✓ Geen wijziging aan `modules_extra.py`, de frontend, of het response-contract.
- ✓ De migratie is volledig transparant voor de gebruiker: BUILD-002 is de eerste gecontroleerde autoriteitsoverdracht van de oude architectuur naar het DesignContext Model, en niemand aan de buitenkant (architect, frontend) mag kunnen zien dát die overdracht heeft plaatsgevonden.

## Acceptatietest

- Voor een reeks bestaande stijlen (o.a. via de etalage-directgeneratie, zonder AI-sleutel nodig) is de gegenereerde SVG **pixel-voor-kleur identiek** aan de output vóór deze wijziging.
- Een generatie met een handmatig aangepast kleurenpalet (`aangepast_palet`) geeft nog steeds exact dat palet terug.
- Een gesimuleerde situatie waarin DesignContext geen kleurpalet heeft (leeg/`None`) valt terug op `analysis["palette"]` zonder fout of lege kleuren.
- De Flask-app start zonder fouten en de bestaande generatie-flow (inclusief "Bekijk in ruimte") werkt ongewijzigd.

**Transparantie voor de gebruiker (nieuw criterium):** oude en nieuwe pipeline moeten, voor dezelfde input, exact hetzelfde resultaat opleveren. Minimaal gecontroleerd:
- **Identieke SVG-output** — de tegel-SVG (`tile_svg_b64`) is byte-voor-byte gelijk vóór en na de migratie.
- **Identieke kleurwaarden** — elke hexkleur in de gegenereerde SVG komt exact overeen.
- **Identieke JSON-response richting frontend** — `analysis`, `info.colors` en alle overige velden in de `/api/generate`-respons blijven ongewijzigd van vorm en inhoud.
- **Identieke mockup-weergave** — "Bekijk in ruimte" toont met de nieuwe pipeline exact hetzelfde beeld als met de oude, omdat de mockup-engine uitsluitend de (ongewijzigde) SVG consumeert.

De gebruiker mag op geen enkele manier kunnen zien dat de bron van het kleurpalet is gewijzigd.

## Rollback

Eén functie, één regel: de bron van het palet in `build_tile_svg()` terugzetten van `DesignContext.concept.kleurpalet` naar `analysis.get("palette", ...)`. Geen andere bestanden zijn hiervan afhankelijk geworden. Geen database, geen migratie, geen onomkeerbare stap.

---

Wachtend op akkoord voordat BUILD-002 daadwerkelijk gestart wordt.
