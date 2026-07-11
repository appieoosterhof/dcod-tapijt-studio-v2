# AB-007 — Concept-besluitkader T9: harmonisatie Reasoning Engine/Pattern Planner ↔ Floor Design

**Status:** concept-besluitkader, ter beoordeling. **Geen oplossing, geen besluit.** Geen nieuwe component, geen nieuw begrip, geen nieuw onderzoek. Uitsluitend het kader waarbinnen de architect T9 kan besluiten.

**Randvoorwaarde:** T9 is pas afsluitbaar ná T7 (bekrachtiging dat Ontwerpstrategie-stap en Reasoning Engine de producenten van DesignContext-lagen 3/4 zijn — AB-001 Deel A; agenda §3/§4).

---

## 1. Welke bestaande componenten worden binnen T9 geharmoniseerd?

Uitsluitend reeds bestaande componenten uit de Architectuurvisie (Diagram A) en BUILD-007 (Diagram B):

- **Ontwerpstrategie-stap**, **Reasoning Engine**, **Pattern Planner** (Diagram A — Architectuurvisie r. 60–61).
- **Floor Design** (Diagram B — BUILD-007).
- **DesignContext-lagen 3 (Ontwerpstrategie) en 4 (Concept)** als brug tussen beide diagrammen.
- Aangrenzend: **SVG Planner** (uitvoeringsgrens — AB-005/AR-004) en de downstream-consumenten van Floor Design (Material Profile, Floor Visualization Engine, Design Transfer Package).

Kern: het verzoenen van de producerende componenten uit Diagram A met het resultaat-object Floor Design uit Diagram B (de twee nooit-verzoende diagrammen — AR-002/AR-003; T12).

## 2. Welke relaties zijn al bewezen (expliciet)?

- Ontwerpstrategie-stap en Reasoning Engine als producenten van DesignContext-lagen 3 en 4 — consistent met alle vastgestelde feiten, wijzigt niets aan BUILD-007 (AB-001 Deel A).
- Floor Design → Material Profile, Floor Visualization Engine, Design Transfer Package (downstream, expliciet — BUILD-007 h. 3; AB-002 r. 24).
- Dát Floor Design wordt afgeleid uit vastgelegde DesignContext-inhoud (BUILD-007 h. 3, r. 61).
- Reasoning Engine/planners produceren "interpretaties, nooit waarheden" (BUILD-007 Technisch r. 11).
- SVG Planner = uitvoerende renderer, zonder architectuur-contract (AB-005; AR-004).

## 3. Welke relaties kunnen historisch niet meer bewezen worden (niet aantoonbaar)?

- Óf, en hóe, de output van Reasoning Engine/Pattern Planner Floor Design oplevert — drie lezingen niet te onderscheiden (AB-001 Deel B/h. 7).
- De producerende component van Floor Design — geen enkel document benoemt er een (AB-002 r. 55; AR-003 §4).
- De precieze afleiding Concept (laag 4) → Floor Design (BUILD-007 h. 8; AR-003 gat 2).
- De relatie tussen de SVG Planner-output en Floor Design/visualisatie (AR-003 gat 4).
- Het onderscheid tussen Pattern Planner-output en SVG Planner-input (AR-004 F9).
- **Grondslag:** AB-002 stelde vast dat het historische bewijs hiervoor is uitgeput — constitutief, niet afleidbaar.

## 4. Welke expliciete architectuurkeuzes moet de architect nemen?

Uitsluitend als keuzepunten geformuleerd; niet ingevuld:

- **C1 — Afleiding.** Wordt Floor Design afgeleid uit een bevestigd Concept (laag 4), of ontstaat het autonoom? (de drie lezingen van AB-001 Deel B)
- **C2 — Producent.** Welke bestaande component produceert Floor Design: Reasoning Engine, Pattern Planner, een combinatie — of heeft Floor Design geen eigen producent (dialoogresultaat)? (K-C uit AB-006)
- **C3 — Diagramverhouding.** Hoe verhouden Diagram A (Ontwerpstrategie → Reasoning Engine → planners) en Diagram B (… → Floor Design) zich: zitten de planners vóór, of vallen ze samen met, Floor Design? (samenhang met T12)
- **C4 — Uitvoeringsgrens.** Hoe verhoudt de SVG Planner-output zich tot Floor Design (bevat Floor Design de SVG, of levert de SVG Planner aan de Floor Visualization Engine)? (AR-003 gat 4)

---

Zodra T7 is bekrachtigd en de architect C1 t/m C4 heeft vastgesteld, is T9 afsluitbaar. Dit kader neemt die keuzes niet.
