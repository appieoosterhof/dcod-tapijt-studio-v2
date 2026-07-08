# DesignContext Model v1.0

**Status: definitief — bevroren.**
Wijzigingen worden uitsluitend nog doorgevoerd wanneer praktijktesten aantonen dat het model op een specifiek punt tekortschiet. Dit document is een domeinmodel van het ontwerpproces van DCOD, geen softwarearchitectuur. Er wordt in dit document niet gesproken over code, datastructuren of implementatie — dat is een bewust volgende, latere stap.

---

## 0. Uitgangspunt

De Dessinator is geen generator die tekst omzet in een SVG-bestand. De Dessinator legt een **ontwerpdialoog** vast tussen twee partijen met elk hun eigen rol, hun eigen kennis en hun eigen verantwoordelijkheid:

- **Architect** — eigenaar van de ontwerpvisie en het project. Brengt de wens, het gevoel, de ruimte in.
- **DCOD** — drager van vakkennis namens het bedrijf: stijlkennis, materiaalkennis en productiekennis. Vertaalt en bewaakt de haalbaarheid.

Het DesignContext Model bestaat uit zes opeenvolgende lagen en één doorlopende laag. Elke laag heeft een eigen eigenaar, een eigen beslisproces en een eigen verantwoordelijkheid — dit model kent bewust geen generieke, uniforme status die voor alle lagen gelijk is. Dat is de kern van het model: het weerspiegelt hoe DCOD vandaag daadwerkelijk met architecten samenwerkt.

---

## 1. Ontwerpvisie

**Doel:** vastleggen wat de architect wil bereiken — in beleving en bedoeling, niet in technische termen.

**Eigenaar:** de Architect, exclusief. Dit is de enige laag met één ondubbelzinnige eigenaar.

**Verantwoordelijkheid:** DCOD mag de visie interpreteren en een lezing daarvan voorstellen, maar die interpretatie blijft voorlopig totdat de architect haar bevestigt. Na bevestiging is de visie onaantastbaar voor de rest van het proces.

**Relatie met volgende laag (Project-/Ruimtecontext):** de visie staat naast de context, niet erna — beide vormen samen de basis waaraan de Ontwerpstrategie wordt getoetst.

**Vastgelegde informatie:** de oorspronkelijke, vrije verwoording van de wens; de sfeer/beleving die wordt nagestreefd; de voorgestelde interpretatie door DCOD; bevestigingsstatus door de architect.

**Waarom noodzakelijk:** zonder een stabiel anker heeft geen enkele latere correctie een vast referentiepunt. Elke latere bijsturing wordt afgezet tegen deze laag.

---

## 2. Project-/Ruimtecontext

**Doel:** de visie situeren in een concrete opdracht — voor wie, welk type ruimte, welke gebruikscontext.

**Eigenaar:** de Architect levert de feiten (het is zijn project); DCOD structureert en categoriseert deze (zoals nu al deels gebeurt via de inspiratie-flow).

**Verantwoordelijkheid:** de visie inkleuren zonder haar te overschrijven. Dezelfde visie ("rustig") betekent iets anders in een kantoor dan in een hotellobby — deze laag levert dat onderscheid.

**Relatie met vorige laag (Ontwerpvisie):** gelijktijdig aanwezig, geen volgorde-afhankelijkheid.
**Relatie met volgende laag (Ontwerpstrategie):** samen met de visie de volledige input voor de strategie.

**Vastgelegde informatie:** projecttype/branche, aard van de ruimte (representatief, functioneel, publiek-intensief), eventueel gekozen startconcept uit de inspiratie-flow. Uitdrukkelijk **geen** fysieke ruimte-informatie (foto's, mockups) — dat blijft buiten dit model.

**Waarom noodzakelijk:** voorkomt dat contextuele kennis onzichtbaar verstopt zit in AI-interpretatie van vrije tekst.

---

## 3. Ontwerpstrategie

**Doel:** de professionele vertaalslag tussen Ontwerpvisie + Projectcontext en het uiteindelijke Concept.

**Eigenaar:** gezamenlijk. **DCOD ontwikkelt samen met de architect de ontwerpstrategie** — dit is nadrukkelijk geen eenzijdig DCOD-voorstel waarop de architect alleen reageert, maar een gezamenlijke ontwikkeling. DCOD brengt de vakkennis in (welke aanpak past bij deze visie en context); de architect bewaakt dat de ontwikkelde strategie de ontwerpvisie recht blijft doen.

**Verantwoordelijkheid:** een aanpak formuleren die expliciet en benoembaar is, zodat er in dialoog op gestuurd kan worden zonder dat de onderliggende visie ter discussie hoeft te staan.

**Relatie met vorige laag:** neemt Visie + Context als gezamenlijk vertrekpunt.
**Relatie met volgende laag (Concept):** bepaalt de bandbreedte waarbinnen het Concept mag worden gevormd. Een Concept dat buiten de vastgestelde strategie ontstaat, is een signaal dat de strategie zelf herzien moet worden.

**Vastgelegde informatie:** de gezamenlijk ontwikkelde aanpak in benoembare termen, de onderbouwing vanuit visie en context, en de status van deze ontwikkeling (in ontwikkeling / vastgesteld).

**Waarom noodzakelijk:** dit is de laag die vandaag ontbreekt en onzichtbaar wordt vervangen door keyword-matching. Ze maakt het mogelijk om een concept af te wijzen op het juiste niveau — de aanpak, niet de visie, niet enkel een kleurdetail.

---

## 4. Concept

**Doel:** de strategie concreet en zichtbaar maken — het eerste tastbare resultaat in de dialoog.

**Eigenaar:** gedeeld, met heldere rolverdeling: DCOD stelt voor (stijlfamilie, kleurpalet, complexiteit, motiefkarakter) binnen de grenzen van de strategie; de architect beoordeelt en stuurt vrij bij.

**Verantwoordelijkheid:** een esthetisch voorstel neerzetten dat binnen de vastgestelde strategie past. Wijzigingen op dit niveau (kleur, schaal) zijn vrij en snel, zolang de strategie niet wordt verlaten.

**Relatie met vorige laag (Ontwerpstrategie):** ontvangt zijn speelruimte van de strategie.
**Relatie met volgende laag (Materialisatie):** het concept is de visuele/patroonmatige intentie; Materialisatie vertaalt die intentie naar een tastbaar product.

**Vastgelegde informatie:** stijlfamilie, kleurpalet, complexiteit/motiefschaal, en per deelkeuze de status (voorgesteld/geaccepteerd).

**Waarom noodzakelijk:** dit is het niveau waarop het gesprek het langst en meest iteratief verloopt. Als eigen laag behandeld, hoeft een kleuraanpassing nooit de strategie of visie opnieuw open te breken.

---

## 5. Materialisatie

**Doel:** de ontwerptechnische vertaalslag van het visuele concept naar het juiste eindproduct — de laag die bepaalt hóé het concept daadwerkelijk wordt ervaren onder de voet.

**Eigenaar:** gedeeld. DCOD brengt materiaalkennis in (welke materiaalsoort, structuur en pooltype passen bij dit concept en deze ruimte); de architect stuurt op tactiliteit en uitstraling, omdat dit direct de beleving raakt die in de Ontwerpvisie is vastgelegd.

**Verantwoordelijkheid:** ontwerpbeslissingen nemen die de beleving van het vloerconcept ondersteunen — dit is nadrukkelijk nog een **ontwerp**-discipline, geen productiediscipline.

**Relatie met vorige laag (Concept):** vertaalt de visuele/patroonmatige intentie naar een fysieke productidentiteit.
**Relatie met volgende laag (Productierealisatie):** levert de materiaal- en textuurkeuzes die vervolgens op technische haalbaarheid worden getoetst. Als die toets faalt, komt de terugkoppeling hierheen terug — niet automatisch helemaal terug naar het Concept.

**Vastgelegde informatie:** materiaalsoort, structuur, pooltype, tactiliteit, uitstraling, glans, textuur — en de status van elke keuze (voorgesteld/geaccepteerd).

**Waarom noodzakelijk:** een vloerconcept is meer dan een patroon — hoe het aanvoelt en oogt als fysiek product is een eigen ontwerpdiscipline, die vandaag nergens expliciet wordt vastgelegd en daardoor volledig ongestructureerd blijft.

---

## 6. Productierealisatie

**Doel:** bewaken dat het gematerialiseerde concept daadwerkelijk als tapijt geproduceerd kan worden.

**Eigenaar:** DCOD, volledig. Dit is zuivere productie- en technische kennis waarover een architect niet beslist, maar waarover hij wel geïnformeerd wordt zodra het zijn concept raakt.

**Verantwoordelijkheid:** uitsluitend technische en productiegerichte aspecten toetsen — geen ontwerpbeslissingen. Bij onhaalbaarheid expliciet terugkoppelen, nooit stilzwijgend een ander resultaat tonen.

**Relatie met vorige laag (Materialisatie):** toetst de materiaal- en textuurkeuzes op technische uitvoerbaarheid.

**Vastgelegde informatie:** technische haalbaarheid, repeat, resolutie, printtechniek, productiecontrole-status, en een expliciete haalbaarheidsstatus (verkennend vs. productierijp).

**Waarom noodzakelijk:** voorkomt dat "een mooi plaatje" wordt verward met "een besteld tapijt" — het scheidt vakmanschap over materiaal en beleving (Materialisatie) nadrukkelijk van vakmanschap over drukbaarheid en repeat (Productierealisatie), twee verschillende expertises die vandaag ten onrechte in één laag zaten.

---

## 7. Ontwerpredenering (doorlopende laag)

**Doel:** niet alleen vastleggen wát op elk niveau is besloten, maar waaróm — en zo de samenhang van het hele traject bewaken.

**Eigenaar:** DCOD (het Dessinator-systeem) is bewaker; de inhoud weerspiegelt beide partijen — elke redenering verwijst naar wie welke beslissing nam en op basis waarvan.

**Verantwoordelijkheid:** bij elke nieuwe beslissing, op elk niveau, controleren of die in lijn is met de redenering van eerdere, hogere lagen. Een latere keuze die een eerdere beslissing feitelijk ondermijnt, moet zichtbaar worden als spanning — nooit stilzwijgend worden geaccepteerd.

**Relatie met de zes lagen:** loopt dwars door alle lagen heen; het is het geheugen van de lógica tussen de lagen, niet van de lagen zelf. Bevat de **Beslisgeschiedenis**: niet een simpele lijst van wijzigingen, maar een keten van "dit verving dat, om deze reden, op dit niveau."

**Vastgelegde informatie:** per beslissing — welke laag, welke reden, welke voorgaande beslissing dit vervangt of bevestigt, en of er spanning bestaat met een hogere laag.

**Waarom noodzakelijk:** dit is het verschil tussen "de Dessinator onthoudt dingen" en "de Dessinator bewaakt de samenhang van een ontwerptraject."

---

## 8. Integraal model

```
                         ┌───────────────────────────────────────────┐
                         │              ONTWERPREDENERING              │
                         │   (bewaakt samenhang, dwars door alle lagen) │
                         └───────────────────────────────────────────┘
                              ▲        ▲        ▲       ▲       ▲       ▲
                              │        │        │       │       │       │
ARCHITECT ──▶ ONTWERPVISIE ───┘        │        │       │       │       │   Architect: exclusief eigenaar,
(exclusief eigenaar,                   │        │       │       │       │   bevestigt definitief
 na bevestiging onaantastbaar)         │        │       │       │       │
        │                              │        │       │       │       │
        ▼                              │        │       │       │       │
PROJECT-/RUIMTECONTEXT ─────────────────┘        │       │       │       │   Architect levert, DCOD categoriseert
        │
        ▼
ONTWERPSTRATEGIE ───────────────────────────────────────┘       │       │   DCOD + Architect: gezamenlijk ontwikkeld
(gezamenlijk ontwikkeld: DCOD vakkennis,                                 │
 Architect bewaakt de visie)                                             │
        │
        ▼
CONCEPT ─────────────────────────────────────────────────────────────────┘   gedeeld: DCOD stelt voor, Architect stuurt bij
(stijl, kleur, complexiteit — binnen de strategie)
        │
        ▼
MATERIALISATIE ──────────────────────────────────────────────────────────┘   gedeeld: DCOD materiaalkennis, Architect
(materiaalsoort, structuur, pooltype,                                        stuurt op tactiliteit/uitstraling
 tactiliteit, uitstraling, glans, textuur)
        │
        ▼
PRODUCTIEREALISATIE ──────────────────────────────────────────────────────┘  DCOD: volledig eigenaar
(technische haalbaarheid, repeat, resolutie,
 printtechniek, productiecontrole)
        │
        ▼
   ↩ terugkoppeling naar Materialisatie (of, indien nodig, Concept) bij onhaalbaarheid — nooit stilzwijgend voorbij
```

**Kernuitspraak van het model:** de Dessinator is een gestructureerd gesprek waarin de Ontwerpvisie (architect-eigendom, onaantastbaar na bevestiging), de Ontwerpstrategie (gezamenlijk ontwikkeld), het Concept en de Materialisatie (gedeeld, iteratief) en de Productierealisatie (DCOD-vakkennis) elk hun eigen plaats, eigen eigenaarschap en eigen wijzigingsregels hebben — bewaakt door een doorlopende Ontwerpredenering die voorkomt dat vooruitgang op het ene niveau stilzwijgend schade doet op een ander niveau.

---

## 9. Wijzigingsbeleid

Dit model is vanaf vaststelling **bevroren**. Wijzigingen worden alleen doorgevoerd wanneer praktijktoetsing (het daadwerkelijk gebruiken van dit model in de ontwerpdialoog met architecten) aantoont dat een laag, een eigenaarschap, of de relatie tussen twee lagen niet standhoudt. Tot die tijd geldt dit document als de definitieve basis voor de fysieke softwarearchitectuur die hierop gebouwd wordt.
