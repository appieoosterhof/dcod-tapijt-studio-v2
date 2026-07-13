# BUILD-026 — Conversation State Architecture: technisch ontwerp

**Status:** architectuurspecificatie (Studio Experience Architecture, deel 1). **Geen code, geen implementatie, geen wijziging aan de Design Brain.** Legt de architectuur van de volledige ontwerpdialoog vast: welke gesprekstoestanden bestaan, hoe zij overgaan, waar bevestigd wordt, en hoe onderbreken/hervatten/samenvatten en contextbehoud werken — volledig additief bovenop de bestaande mechanismen.

**Bindend / respecteert:** AB-006, AB-009, AB-012, BUILD-007, BUILD-017, BUILD-019, BUILD-023, IMP-014, BUILD-024, PLATFORM-001, PLATFORM-002, REASONING-001, SEC-001, BUILD-025.

**Kernprincipe (architectonisch geborgd):** de gesprekstoestand is **geen nieuwe store en geen nieuw domeinobject**. Zij wordt **afgeleid** uit de reeds bestaande, persistente `Gesprekstoestand` (per `gesprek_id`, BUILD-019) en de DesignContext-lagen/statussen. De Conversation State Architecture beschrijft dus hoe bestaande gegevens als *gespreksfase* worden geïnterpreteerd; zij voegt geen toestand aan het domein toe.

---

## 1. Gesprekstoestanden (afgeleid, niet opgeslagen)

De actieve fase volgt deterministisch uit wat er al in de `Gesprekstoestand`/DesignContext staat:

| Fase (BUILD-025 §5) | Afgeleid uit (bestaand) |
|---|---|
| **Begroeting** | nieuw `gesprek_id`, lege DesignContext |
| **Verkennen** | interpretaties aanwezig (laag 1/2), `ontwerpvisie.bevestigd_door_architect == False` |
| **Verdiepen** | Conversation Planner stelt vervolgvragen; context groeit, nog niet bevestigd |
| **Samenvatten** | voldoende context om terug te koppelen; presentatie van de huidige DesignContext |
| **Bevestigen** | een gate staat open (visie/strategie/concept/material/pattern nog te bevestigen) |
| **Ontwerpen** | een upstream is bevestigd; het volgende resultaat-object bestaat nog niet (reasoning mag draaien) |
| **Presenteren** | het resultaat-object bestaat (concept/floor designs/material/pattern/…); tonen/uitspreken |
| **Vervolg** | de gebruiker verfijnt; gewijzigde bevestigde upstream → gerichte invalidatie (BUILD-023 R4) |

Er is dus **één bron van waarheid** (de persistente `Gesprekstoestand`); de fase is een *lezing* daarvan, geen apart bijgehouden veld.

## 2. Ontwerpfasen ↔ Design Workflow

De gespreksfasen mappen één-op-één op de bestaande ketenstappen (BUILD-007); de dialoog herdefinieert de workflow niet, zij *begeleidt* hem:

```
Verkennen/Verdiepen → Context (laag 1/2)
Bevestigen(visie)   → gate → Ontwerpstrategie
Bevestigen(strategie) → gate → Concept
Bevestigen(concept) → gate → Floor Design → (bevestig) → Material → (bevestig) → Pattern → (bevestig) → SVG/Visualisatie/DTP
```

Elke "Ontwerpen"-fase is exact een bestaande reasoning-stap onder de bestaande gates en BUILD-023-orkestratie (reasoning uitsluitend bij nieuwe ontwerpwaarde).

## 3. Bevestigingsmomenten

Bevestigen blijft een **expliciete gebruikersactie** op de bestaande gates (AB-006-statusvocabulaire; BUILD-007-bevestigingsmomenten): `bevestig-visie`, `bevestig-strategie`, `bevestig-concept`, `bevestig-material-profile`, `bevestig-pattern-profile`. De Conversation State Architecture voegt geen nieuwe bevestiging toe en verplaatst geen bestaande; spraak/tekst kunnen een bevestiging *aansturen*, maar de status wordt nooit door de studio zelf gezet.

## 4. Onderbreken

Onderbreken werkt op **presentatieniveau**, nooit op reeds afgeronde reasoning:
- een lopende **weergave** (TTS/streaming/animatie) kan worden gestopt; het onderliggende resultaat blijft in de `Gesprekstoestand` bestaan;
- een reeds **bevestigde** keuze wordt door onderbreken niet ongedaan gemaakt (dat is een expliciete Vervolg-actie);
- een lopende reasoning-aanroep is kort en atomisch; onderbreken annuleert hooguit de *presentatie* van het resultaat, niet de consistentie van de `Gesprekstoestand` (het per-`gesprek_id`-slot borgt dat, BUILD-019).

## 5. Hervatten

Hervatten is reeds geborgd door de **persistente `Gesprekstoestand`**: elk gesprek is een `gesprek_id`-bestand (JSON, atomair opgeslagen, BUILD-019). Een gebruiker (op elk apparaat/kanaal) laadt hetzelfde `gesprek_id` en krijgt exact de laatste toestand terug; de afgeleide fase (§1) bepaalt waar het gesprek verdergaat. Geen nieuw hervat-mechanisme nodig.

## 6. Samenvatten

Samenvatten is **presentatie van de bestaande DesignContext** (visie, context, strategie, concept, en de resultaat-objecten): de studio koppelt terug wat is opgebouwd en bevestigd. Geen reasoning, geen nieuwe interpretatie — puur een gestructureerde weergave van reeds vastgelegde gegevens, in studio-taal (AB-012).

## 7. Contextbehoud

Contextbehoud = de persistente `Gesprekstoestand` + de defensieve herkomst-snapshots (BUILD-024). Bevestigde keuzes en hun herkomst blijven bevroren behouden; gerichte invalidatie (BUILD-023 R4) raakt uitsluitend het downstream dat niet meer bij de bevestigde upstream hoort. Er gaat geen context verloren bij modaliteitswissel, onderbreken of hervatten.

## 8. Overgang naar Design Workflow

De overgang van *gesprek* naar *ontwerpstap* is uitsluitend de bestaande **gate**: zodra de vereiste upstream bevestigd is, ontsluit dat de volgende reasoning-stap (die één keer draait en wordt gecachet). De Conversation State Architecture bepaalt *wanneer het gesprek klaar is voor* een stap; de Design Workflow bepaalt *welke* stap volgt. De grens Conversation ≠ Workflow (BUILD-025 §6) blijft hard.

---

## Consistentietoets

- **BUILD-019:** de `Gesprekstoestand` is en blijft de enige persistente bron; de gespreksfase is een afleiding, geen nieuwe opslag.
- **BUILD-007 / AB-006:** ketenvolgorde en bevestigingsmomenten ongewijzigd; bevestigen blijft een expliciete gebruikersactie.
- **BUILD-023 / IMP-014:** "Ontwerpen"-fasen volgen de bestaande reuse-/invalidatieregels; onderbreken/hervatten starten geen extra reasoning.
- **BUILD-024:** contextbehoud steunt op de bestaande herkomst-snapshots; geen contractwijziging.
- **BUILD-025 / PLATFORM-002:** de acht fasen zijn die uit de gespreksstroom; de State Architecture legt hun toestandsmodel vast zonder de Experience-Layer-grens te overschrijden.
- **AB-012:** samenvatten/presenteren gebeurt in studio-taal; nooit techniek/model/fout.
- **SEC-001:** gespreksdata valt onder het bestaande opslag-/privacybeleid (gesprekken buiten static/, gitignored); geen extra persoonsgegevens geïntroduceerd.

---

**Reviewgereed:** dit ontwerp legt de Conversation State Architecture vast als volledig afgeleide toestandslaag bovenop de bestaande persistente `Gesprekstoestand` en DesignContext — acht afgeleide gespreksfasen, hun mapping op de Design Workflow, de bestaande bevestigingsmomenten, en de mechanismen voor onderbreken (presentatie), hervatten (persistentie), samenvatten (presentatie) en contextbehoud (herkomst) — zonder nieuwe store, nieuw domeinobject, extra reasoning of enige wijziging aan de Design Brain.
