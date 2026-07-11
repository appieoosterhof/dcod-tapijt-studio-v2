# BUILD-008 — Technisch DesignContext Fundament: technisch ontwerp

**Status:** technisch ontwerp, ter review. Geen implementatie, geen commit. Implementeert uitsluitend het bevroren DesignContext Model v1.0. Geen nieuwe architectuur, geen nieuwe begrippen, geen uitbreiding van de DesignContext.

**Doel:** één technisch fundament (dataclasses, JSON-contracten, status, eigenaarschap, validatie, serialisatie, interfaces) waarop alle volgende BUILD's voortbouwen.

---

## 0. Architectuurprincipe

- **Implementeren, niet herdefiniëren.** `DESIGN_CONTEXT_MODEL.md` blijft de canonieke domeinbeschrijving; dit ontwerp voegt uitsluitend een technische representatie toe.
- **Voorstellen, nooit bevestigen.** Elke component schrijft voorstellen weg (status "Voorgesteld"); alleen de eigenaar bevestigt (AB-008; eigenaarschapsregels van het model).

## 1. Technische componenten (dataclasses)

- Zes laag-dataclasses, exact de lagen van het model, met uitsluitend de daar benoemde velden:
  1. **Ontwerpvisie**, 2. **Project-/Ruimtecontext**, 3. **Ontwerpstrategie**, 4. **Concept** (o.a. stijlfamilie, kleurpalet, complexiteit/motiefschaal), 5. **Materialisatie**, 6. **Productierealisatie** (o.a. repeat_type).
- **Ontwerpredenering** als doorlopende laag (registreert per stap resultaat + reden).
- **Status per laag, géén uniforme enum** — elke laag draagt de status en het statusvocabulaire dat het model hem toekent (zie §2); er is bewust geen enkele, uniforme status voor alle lagen.
- **`DesignContext`-container** die de lagen + Ontwerpredenering bundelt.

## 2. Statusmechanisme en eigenaarschap (per laag, geen uniformering)

Elke laag behoudt zijn eigen eigenaarschap én zijn eigen wijzigings-/statusregel exact conform `DESIGN_CONTEXT_MODEL.md`; er is geen uniforme statuslogica over de lagen heen.

| Laag | Eigenaar (conform model) | Status / wijzigingsregel (conform model) |
|---|---|---|
| 1. Ontwerpvisie | Architect, exclusief | DCOD stelt interpretatie voor (voorlopig) → architect bevestigt → ná bevestiging onaantastbaar |
| 2. Project-/Ruimtecontext | Architect levert de feiten; DCOD structureert/categoriseert | volgt de feiten van de architect; DCOD wijzigt de categorisering, niet de feiten |
| 3. Ontwerpstrategie | Gezamenlijk (DCOD + architect) | "in ontwikkeling / vastgesteld" |
| 4. Concept | Gedeeld (DCOD stelt voor, architect stuurt bij) | iteratief bijstuurbaar; door de architect te bevestigen (AB-009) |
| 5. Materialisatie | Gedeeld | iteratief bijstuurbaar in de gedeelde dialoog |
| 6. Productierealisatie | DCOD | DCOD-vakkennis |

**Granulariteit:** de status geldt **per laag**, zoals het model die registreert als onderdeel van de vastgelegde informatie van elke laag (bijv. laag 1 "bevestigingsstatus", laag 3 "status van de ontwikkeling"). Afzonderlijke velden dragen geen eigen status; zij erven die van hun laag.

## 3. Validatieregels

- **Per laag de eigen wijzigingsregel** (§2), geen uniforme overgang: alleen de eigenaar van een laag mag haar status wijzigen (AB-008 — componenten stellen voor, bevestigen nooit).
- Ontwerpvisie: geen terugval ná bevestiging (onaantastbaar).
- Geen component wijzigt of bevestigt een laag die niet zijn eigendom is.
- Verplichte velden per laag conform het model; onzekerheid blijft een eigenschap van de interpretatie, niet van het veld.

## 4. Serialisatie (JSON-contracten)

- `to_dict()` / `from_dict()` per laag en voor `DesignContext`; stabiel JSON-contract dat per laag velden + `status` + eigenaar draagt.
- Round-trip-garantie: `from_dict(to_dict(x)) == x`.

## 5. Interfaces (voor volgende BUILD's)

- **Lezen:** componenten lezen lagen/interpretaties (read-only voor niet-eigenaars).
- **Schrijven:** componenten schrijven uitsluitend voorstellen (status Voorgesteld), nooit bevestigen.
- **Bevestigen:** uitsluitend via een expliciete eigenaar-actie (architect, of gezamenlijke dialoog waar het model dat voorschrijft).
- Dit vormt het contract waarop de Ontwerpstrategie-stap (laag 3), de Reasoning Engine (laag 4) en latere resultaat-objecten aansluiten.

## 6. Bestaande modules en migratie-impact

- Bouwt voort op de bestaande `design_context.py` (`OntwerpVisie`, `ProjectContext`, `DesignContext` bestaan al; `Concept.kleurpalet` en `Productierealisatie.repeat_type` deels aanwezig). Voegt de ontbrekende lagen en het status/eigenaarschap/validatie-apparaat **additief** toe.
- **Geen wijziging** aan `app.py`, de generatie-pipeline of het response-contract. Het fundament staat los tot een volgende BUILD het bewust aansluit (zelfde isolatiefilosofie als eerdere BUILD's).
**Migratie van reeds bestaande velden.** De al gemigreerde velden vallen zonder herdefinitie onder het per-laag status/eigenaarschap-contract van §2:
- `Concept.kleurpalet` (BUILD-002) → laag 4 (Concept), gedeeld eigenaarschap; erft de status van laag 4.
- `Productierealisatie.repeat_type` (BUILD-003) → laag 6 (Productierealisatie), DCOD-eigenaarschap; erft de status van laag 6.

Deze velden behouden hun huidige gedrag; er komt uitsluitend, additief, een statusveld op laagniveau bij.

- **Rollback:** de additieve uitbreiding terugdraaien; de live Dessinator is nooit aangeraakt.

## 7. Buiten scope

- Geen Floor Design- of Material Profile-objecten (latere BUILD's; hergebruiken dit fundament — status/eigenaarschap zijn generiek toepasbaar).
- Geen nieuwe lagen of velden, geen herdefinitie van het bevroren model.
- Geen koppeling aan de live `/api/generate`-flow.

---

**Acceptatie:** alle zes lagen + Ontwerpredenering serialiseren round-trip; statusovergangen respecteren eigenaarschap; een niet-eigenaar kan niet bevestigen; bestaande velden (`kleurpalet`, `repeat_type`) blijven identiek gedragen. Validatie steunt op deze criteria, niet op koppeling aan de bestaande pipeline.
