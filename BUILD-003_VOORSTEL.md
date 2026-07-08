# BUILD-003 — Repeat-type leidend vanuit DesignContext

**Status:** goedgekeurd, implementatie volgt in dit document.
**Gebaseerd op:** BUILD-003_ADVIES.md (kandidaat "Repeat-type" gekozen).

## Doel

Niet nog een veld migreren om de veiligste route te volgen, maar aantonen dat DesignContext een ontwerpbeslissing kan dragen die door een **andere** functie wordt geconsumeerd dan `build_tile_svg()` (BUILD-002 raakte alleen die ene functie). Repeat-type wordt geconsumeerd door `build_repeat_svg()` — een aparte, downstream functie die `build_tile_svg()` niet kent en niet aanroept.

## Definition of Done

- ✓ `build_repeat_svg()` leest het repeat-type uit `DesignContext.productierealisatie.repeat_type`, met de bestaande `repeat_type`-parameter als expliciete fallback.
- ✓ `DesignContext.productierealisatie.repeat_type` wordt gevuld vanuit dezelfde bron als vandaag (`data.get("repeat_type", "full")`), niet vanuit `analysis` (repeat_type heeft nooit in `analysis` gezeten).
- ✓ Geen wijziging aan `build_tile_svg()`, `modules_extra.py`, de frontend, of het response-contract.
- ✓ `api_refine()` blijft buiten scope, exact zoals bij BUILD-002.

## Acceptatietest

**Identieke output (zoals BUILD-002):**
- Voor alle vier repeat-types (full, half-drop, brick, mirror) is de gegenereerde repeat-SVG byte-voor-byte identiek vóór en na de migratie.
- Fallback-scenario (geen override, of lege/`None`-waarde) valt terug op het bestaande gedrag zonder fout.

**Onafhankelijk gebruik door meerdere modules (nieuw criterium):**
Naast identieke output moet worden aangetoond dat dezelfde ontwerpbeslissing vanuit DesignContext door meerdere modules onafhankelijk wordt gebruikt, niet via onderlinge kennis van elkaar:
- `build_tile_svg()` blijft correct functioneren (regressietest — deze functie gebruikt repeat_type niet, maar mag door deze wijziging op geen enkele manier worden beïnvloed).
- `build_repeat_svg()` gebruikt hetzelfde repeat-type vanuit DesignContext als waarmee `build_tile_svg()` zijn kleurpalet kreeg (BUILD-002) — beide via een eigen, expliciete override-parameter, gevuld door `api_generate()` vanuit dezelfde DesignContext-instantie.
- `build_tile_svg()` en `build_repeat_svg()` kennen elkaar niet rechtstreeks: geen van beide functies importeert, roept aan, of leest interne staat van de ander. Ze delen uitsluitend `api_generate()` als aanroeper.
- De enige gedeelde bron is DesignContext: `_design_context` wordt in `api_generate()` één keer opgebouwd, en levert onafhankelijk twee losse waarden (`concept.kleurpalet` aan `build_tile_svg()`, `productierealisatie.repeat_type` aan `build_repeat_svg()`) zonder dat de functies dat van elkaar hoeven te weten.

Bij succes is dit de eerste architectonische bevestiging dat meerdere onderdelen van de Dessinator onafhankelijk op dezelfde DesignContext kunnen vertrouwen.

## Rollback

Twee onafhankelijke, losse regels: de bron van `repeat_type` in `build_repeat_svg()` terug naar de bestaande parameter, en het weglaten van de override-aanroep in `api_generate()`. Geen effect op de kleurpalet-migratie uit BUILD-002 — de twee migraties zijn volledig onafhankelijk terug te draaien.

## Architectuurmijlpaal

BUILD-003 is de eerste BUILD waarin meerdere onafhankelijke onderdelen van de Dessinator dezelfde DesignContext gebruiken zonder onderlinge afhankelijkheid.

Dit bevestigt dat DesignContext daadwerkelijk de centrale bron van waarheid begint te worden.

Daarmee is de architectuur succesvol bewezen voor meer dan één ontwerpbeslissing.
