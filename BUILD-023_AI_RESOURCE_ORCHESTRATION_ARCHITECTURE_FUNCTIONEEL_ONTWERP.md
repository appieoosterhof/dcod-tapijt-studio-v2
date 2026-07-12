# BUILD-023 — AI Resource & Orchestration Architecture: functioneel ontwerp

**Status:** functioneel ontwerp / architectuurbesluit, gereed voor VR. Geen implementatie, geen code, geen nieuwe component, geen wijziging aan de Design Brain of de BUILD-007-workflow. Legt uitsluitend de **orkestratieregels** vast: wanneer AI (reasoning) wél en niet wordt ingezet.

> **Kernherkadering:** BUILD-023 gaat **niet over kostenbeheersing, maar over orkestratie van waardecreatie.** De Design Brain redeneert nooit vanuit *"hoe besparen we tokens?"*, maar altijd vanuit *"wanneer voegt een nieuwe AI-actie daadwerkelijk ontwerpwaarde toe?"*. Voorspelbare kosten, reproduceerbaarheid, caching en performance zijn daarvan het **automatische gevolg**. Dit sluit naadloos aan op het Ontwerpstudio-principe (BUILD-022 §9) en op AB-012 (AI-infrastructuur verborgen).

**Verankerd in / benut:** de reeds bestaande herkomst-referenties en `is_stale`-detectie (SVG Planner/FVE/DTP), de gate-/bevestigingsarchitectuur (BUILD-008/AR-007), de persistente `Gesprekstoestand` (BUILD-019/TD-008) en de injecteerbare boundaries (TD-004/005/006, BUILD-009/010/012/013). BUILD-023 introduceert **niets nieuws** — het legt een **beleidslaag** vast bovenop deze mechanismen.

---

## AP-001 — AI wordt uitsluitend ingezet wanneer een nieuwe ontwerpbeslissing moet worden genomen

*(Eerste architectuurprincipe in de AP-reeks; naast de bestaande AB-/AR-reeksen.)*

**Principe:** een reasoning-/AI-aanroep vindt uitsluitend plaats om een **nieuwe of gewijzigde ontwerpbeslissing** te produceren die nog niet bestaat voor de huidige bevestigde invoer.

**Gevolgen (wat nooit AI start):**
- **gesprek** → geen AI tenzij er nieuwe, te interpreteren invoer is;
- **navigatie** (bladeren, terugkijken, scrollen) → nooit;
- **bevestigen** (een status/vlag zetten) → nooit uit zichzelf;
- **bestaande resultaten bekijken** → nooit;
- **een bestaande SVG tonen** → nooit;
- **een mockup opnieuw projecteren** → nooit;
- alleen **een nieuwe ontwerpvraag** of een **gewijzigde ontwerpbeslissing** kan reasoning starten.

**Automatisch resultaat:** voorspelbare kosten, reproduceerbaarheid, betere caching, betere performance en natuurlijk studio-gedrag.

---

## 1. Doel en uitgangspunten

- **Doel:** vastleggen wanneer AI aantoonbaar ontwerpwaarde toevoegt, zodat AI daar — en uitsluitend daar — wordt ingezet.
- **Uitgangspunten:** geen implementatie; geen nieuwe component; geen wijziging aan BUILD-007 of de Design Brain-componenten; de gebruiker ervaart **nooit** een limiet, budget of technische beperking (AB-012 + BUILD-022 §9). De regels benutten uitsluitend reeds bestaande mechanismen.

## 2. Waarde vóór berekening

Elke AI-aanroep moet corresponderen met een **echte, nieuwe of gewijzigde ontwerpbeslissing**. Waar geen nieuwe ontwerpwaarde ontstaat, wordt geen AI ingezet. De vraag is nooit "kan het goedkoper?", maar altijd "**ontstaat hier nieuwe ontwerpwaarde?**". Zo niet → hergebruik het bestaande resultaat. De besparing volgt vanzelf.

## 3. Typen werkzaamheden

| Type | Component(en) | Aard | AI? | Herbruikbaar |
|---|---|---|---|---|
| **Reasoning** | Context Interpreter, Ontwerpstrategie-stap, Reasoning Engine (Concept + Floor Design), Material Planner, Pattern Planner | ontwerp*beslissing* afleiden | **Ja** (waardedragend, duur) | ja — gecachet op herkomst |
| **SVG-rendering** | SVG Planner (productiepipeline, AB-005/BUILD-018) | deterministische tekening van een bevestigd patroon | **Nee** | ja — deterministisch |
| **Visualisatie** | Floor Visualization Engine | deterministische compositie op de Scene | **Nee** | ja — deterministisch |
| **Presentatie** | frontend, Design Transfer Package (bundeling) | tonen/bundelen | **Nee** | altijd |

Uitsluitend de **Reasoning**-laag is AI en waardedragend; de overige typen zijn deterministisch en per definitie herbruikbaar. Dit onderscheid is de kern van de orkestratie: **alleen reasoning valt onder AP-001**; deterministisch werk wordt hergebruikt, nooit "opnieuw berekend als AI".

## 4. Wanneer ontstaat nieuwe ontwerpwaarde?

Nieuwe ontwerpwaarde — en dus een legitieme reasoning-aanroep — ontstaat uitsluitend bij:
1. **een nieuwe ontwerpvraag / nieuwe vrije-tekstinvoer** die nog niet is geïnterpreteerd (nieuwe interpretatie nodig);
2. **een gewijzigde bevestigde upstream-beslissing** waardoor het downstream-resultaat *stale* is (het hoort niet meer bij de huidige keuzes);
3. **een nog niet bestaand volgend-laags voorstel** voor de huidige bevestigde invoer (bv. materiaal ná een bevestigd Floor Design — een echte nieuwe ontwerpbeslissing: "welk materiaal past hierbij?").

**Geen** nieuwe ontwerpwaarde (dus geen AI) bij: navigeren, terugkijken, een bestaand voorstel opnieuw bekijken/bevestigen, een reeds gerenderde SVG tonen, of een mockup opnieuw projecteren. De **bevestigingsactie zelf** is nooit AI; zij kan hooguit de *volgende* reasoning-stap ontsluiten (punt 3), die dan één keer draait en wordt gecachet.

## 5. Hergebruik en caching

- **Resultaten worden gecachet op hun bevestigde herkomst.** Zolang de bevestigde invoer (identifiers) ongewijzigd is, wordt het bestaande resultaat **hergebruikt** — geen nieuwe aanroep. De reeds bestaande `Gesprekstoestand` (BUILD-019) bewaart die resultaten al persistent; dat ís de cache.
- **Deterministische artefacten** (SVG, mockup) worden altijd hergebruikt zolang hun bron ongewijzigd is; ze worden nooit "opnieuw berekend als AI".
- **Reasoning-resultaten** (strategie, concept, floor designs, materiaal, patroon) blijven geldig zolang hun herkomst matcht; opnieuw tonen/bevestigen levert nooit een nieuwe aanroep.

## 6. Herkomst, stale-detectie en idempotentie

De keten heeft de invalidatie-mechaniek **al**: elke herkomst-referentie + de `is_stale`-checks bepalen of een resultaat nog bij de huidige bevestigde inputs hoort.
- **Geldig zolang herkomst matcht:** een resultaat is bruikbaar (en wordt hergebruikt) zolang zijn upstream-herkomst overeenkomt met de actuele bevestigde objecten.
- **Stale → mag herberekenen:** wijzigt/wordt een bevestigde upstream opnieuw voorgesteld, dan is strikt het geraakte downstream *stale* en **mag** het op aanvraag opnieuw worden afgeleid — precies zoals `is_stale` nu al signaleert.
- **Idempotentie (AP-001):** een herhaalde identieke actie (dubbele klik, opnieuw bevestigen, opnieuw tonen) produceert **nooit** een tweede reasoning-aanroep; het bestaande, geldige resultaat wordt hergebruikt.

## 7. Orkestratieregels (declaratief)

- **R1 — Reasoning alleen bij ontbrekende/stale waarde:** een reasoning-boundary wordt uitsluitend aangeroepen wanneer er **geen geldig (niet-stale) resultaat** bestaat voor de huidige bevestigde invoer.
- **R2 — Zicht/navigatie is gratis:** tonen, terugkijken, navigeren, en opnieuw bevestigen starten **nooit** reasoning.
- **R3 — Deterministisch werk wordt hergebruikt:** SVG-rendering en visualisatie draaien alleen wanneer hun invoer wijzigde; anders wordt het bewaarde artefact hergebruikt.
- **R4 — Gerichte invalidatie:** een gewijzigde/opnieuw bevestigde upstream invalideert **uitsluitend** het geraakte downstream (stale), niet de hele keten.
- **R5 — Onzichtbare degradatie, met één heldere grens (verhouding tot AB-012):**
  - is er voor de huidige stap een **geldig (niet-stale) resultaat**, dan wordt dat **onzichtbaar hergebruikt** — geen aanroep, geen melding, geen wachtmoment; de studio voelt juist snel;
  - moet er een **échte nieuwe ontwerpbeslissing** worden geproduceerd (nieuwe/gewijzigde invoer) én is de AI-infrastructuur op dat moment niet beschikbaar én is er **niets geldigs om op terug te vallen**, dan — en uitsluitend dan — verschijnt de neutrale AB-012-melding *"Onze ontwerpstudio is momenteel niet beschikbaar…"*.
  In geen geval een zichtbare limiet, wachtrij, teller of technische foutmelding (AB-012 + BUILD-022 §9).
- **R6 — Idempotente acties:** identieke verzoeken hergebruiken; zij herberekenen nooit.

*(Deze regels zijn beleid; hun implementatie — guards op basis van de bestaande `is_stale`/herkomst in de integratielaag — is een latere, additieve IMP-stap.)*

## 8. UX-principes

- **Studio boven "klik = nieuwe AI-call":** een klik betekent voortgang in het ontwerp, niet automatisch een berekening.
- **Nooit een ervaren limiet:** de gebruiker merkt van budget/caching/degradatie **niets**; hergebruikte resultaten verschijnen juist *direct* (voelt snel en vakkundig).
- **Geen "opnieuw genereren"-ruis:** geen herhaalde laadmomenten voor ongewijzigde keuzes; rust en continuïteit.
- **Onzichtbare kostenkant:** conform AB-012 ziet de gebruiker nooit "call", "cache", "budget" of "token".

## 9. Architectuurgrenzen

- **Geen nieuwe component, geen nieuw domeinobject:** BUILD-023 is een **beleidslaag** die de bestaande herkomst/`is_stale`, de `Gesprekstoestand`-cache, de gates en de boundaries benut.
- **Geen wijziging aan BUILD-007** of aan de Design Brain-componenten; de ketenvolgorde en bevestigingsmomenten blijven exact.
- **Uitdrukking in de bestaande lagen:** de orkestratieregels worden later toegepast in de integratielaag (`design_brain_api.py`) en via de bestaande `is_stale`-checks — niet in de Design Brain zelf.
- **Consistent met AB-012:** de gehele resource-/orkestratielaag is en blijft voor de gebruiker onzichtbaar.

## 10. Toekomstvastheid

- De titel **"AI Resource & Orchestration Architecture"** en de regels blijven geldig ongeacht welk AI-model of welke prijsstructuur later wordt gebruikt: de regels gaan over **ontwerpwaarde**, niet over tokens.
- Elke toekomstige productie-reasoning-boundary valt automatisch onder AP-001 en de orkestratieregels — er is geen herontwerp nodig wanneer echte AI wordt ingeplugd.
- De cache-/herkomstmechaniek is model-agnostisch; nieuwe modellen erven de orkestratie zonder wijziging.

---

**Reviewgereed:** dit document legt de AI-resource- en orkestratiearchitectuur vast als beleidslaag — de herkadering (waarde vóór kosten), AP-001, de werktypen, de waardetriggers, hergebruik/caching, herkomst/stale/idempotentie, de declaratieve orkestratieregels, de UX-principes, de architectuurgrenzen en de toekomstvastheid — zonder implementatie, nieuwe component of wijziging aan BUILD-007/de Design Brain. Na een positieve VR is dit het kader waarbinnen de productie-reasoning-boundaries met vertrouwen kunnen worden ingeplugd.
