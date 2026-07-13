# PLATFORM-002 — Conversation Experience & Design Dialogue

**Status:** strategisch platform-visiedocument / toekomstige uitbreidingsrichting van PLATFORM-001. **Geen code-, architectuur- of boundary-wijziging.** Beschrijft hoe het Studio Platform een natuurlijke ontwerpdialoog krijgt waarin de gebruiker met een "digitale ontwerpcollega" een volledig ontwerpgesprek voert dat de bestaande Design Workflow aanstuurt.

**Aard:** dit document is **richtinggevend, niet normatief**. De bestaande, bekrachtigde architectuur (AB-006/009/012, BUILD-007/023/024, IMP-014, PLATFORM-001, REASONING-001, IMP-015/016) blijft **volledig leidend**. Waar deze visie en een bestaand architectuurbesluit ooit zouden lijken te botsen, wint het bestaande besluit; PLATFORM-002 introduceert geen afwijkende architectuur en verplicht tot geen enkele herstructurering.

---

## Doel

Het Studio Platform uitbreiden met een **Design Dialogue**: een natuurlijke ontwerpdialoog die als **Experience Layer** boven op de bestaande Design Workflow ligt. De gebruiker communiceert niet met een AI-chatbot, maar met een digitale ontwerpcollega die het ontwerpproces begeleidt. De Studio vertaalt het gesprek automatisch naar de bestaande workflow.

## Uitgangspunt

De gebruiker denkt niet in *Ontwerpstrategie*, *Conceptvorming*, *Floor Design*, *SVG* of *Mockups*, maar in:

> "Ik wil een vloer ontwerpen die past bij mijn project."

De Design Dialogue vertaalt dat gesprek naar de bestaande, ongewijzigde workflow — de gebruiker ziet de interne stappen nooit als techniek (AB-012, BUILD-022 §9 Ontwerpstudio-principe).

## Architectuurprincipe

**De Design Dialogue bevat geen ontwerpintelligentie.** De bestaande Design Brain blijft volledig verantwoordelijk voor alle ontwerpbeslissingen (Ontwerpstrategie, Conceptvorming, Floor Design en overige Reasoning Capabilities). De Design Dialogue:

- verzamelt context;
- stelt verdiepende, relevante vragen;
- bewaakt het gesprek (geheugen, consistentie);
- activeert de juiste capability op het juiste moment — **via de bestaande gates en orchestratie**, nooit eromheen;
- presenteert de resultaten op natuurlijke wijze.

Dit onderscheid — dialoog verzamelt/presenteert, Design Brain redeneert — is exact de bestaande scheiding (Conversation Planner/Context Interpreter vs. Reasoning Capabilities) en blijft ongewijzigd.

## Ontwerpprincipes

De Design Dialogue voert een professioneel ontwerpgesprek: zij stelt alleen relevante vervolgvragen, onthoudt eerdere keuzes, voorkomt tegenstrijdigheden, motiveert ontwerpkeuzes (op basis van wat de Design Brain aanreikt), vraagt om verduidelijking wanneer informatie ontbreekt, en doet geen ongefundeerde aannames. Dit sluit naadloos aan op REASONING-001 (onderbouwd, uitlegbaar, geen willekeur) en op de grens "de dialoog beslist niet, zij begeleidt".

## Relatie met PLATFORM-001

De Design Dialogue is een **uitbreiding van de Experience Layer** (PLATFORM-001 §2). De bestaande architectuur blijft volledig intact; er worden **geen** wijzigingen aangebracht aan de Design Workflow, de Design Brain, de orchestrator, de contracten, de resultaatobjecten of de componentgrenzen.

## Verankering in de bestaande architectuur

De Design Dialogue is geen nieuwe laag bovenop het systeem; zij is de **strategische naam en groeirichting** van gespreksfunctionaliteit die deels al bestaat. De begrippen mappen op bestaande onderdelen:

| Design Dialogue-aspect (PLATFORM-002) | Bestaand onderdeel | Bindend document |
|---|---|---|
| Context verzamelen uit vrije tekst | Context Interpreter (interpretaties, nooit waarheden) | BUILD-004 |
| Gespreksregie, vragen stellen, laag 1 vullen | Conversation Planner | BUILD-017 |
| Gesprek bewaken / geheugen / consistentie | persistente `Gesprekstoestand` (per `gesprek_id`) | BUILD-019 |
| Capability op het juiste moment activeren | de bestaande gates + orchestratie-/reuse-guards (AP-001) | BUILD-007, BUILD-023, IMP-014 |
| Resultaten natuurlijk presenteren | de belevingslaag / atelier-UX (`/ontwerp`) | BUILD-021, BUILD-022, IMP-013 |
| "Ontwerpcollega, geen AI-chatbot" | AI-infrastructuur volledig verborgen | AB-012 |

**Belangrijke afbakening:** de "Design Dialogue" is een **conceptueel koepelbegrip** voor deze reeds bestaande gesprekscomponenten plus hun toekomstige verrijking — geen nieuwe architectuurlaag en geen aanleiding tot hernoemen of herbouwen. De verrijking (rijkere vraagstrategie, spraak, beeld, moodboards, referentieprojecten, realtime gesprek) zijn latere, optionele en additieve trajecten die pas op expliciete opdracht ontstaan en de onderliggende workflow identiek laten.

## Toekomstige uitbreidingen

De Design Dialogue moet later kunnen ondersteunen: tekst, spraak, afbeeldingen, moodboards, referentieprojecten en realtime ontwerpgesprekken. In alle gevallen blijft de onderliggende Design Workflow **identiek**: de modaliteit verandert de invoerverzameling, niet de reasoning of de contracten. Elke modaliteit levert uiteindelijk dezelfde platte context aan de bestaande boundaries.

## Strategische waarde

Het onderscheidend vermogen van DCOD ligt niet uitsluitend in AI, maar in een **volledig ontwerpgesprek**: context wordt opgebouwd, ontwerpkeuzes worden verklaard, consistentie wordt bewaakt, en het volledige ontwerpproces voelt natuurlijk. Zo ontstaat een digitale ontwerpstudio in plaats van een traditionele AI-chat — geheel in lijn met AB-012 en het Ontwerpstudio-principe.

## Opname in de projectroadmap

Na voltooiing van de huidige Design Brain-roadmap wordt PLATFORM-002 ingepland. Indicatieve volgorde:

1. Afronding van de huidige Reasoning Capabilities.
2. Volledige validatie van de Design Brain.
3. Productierijpe Mockup- en SVG-keten.
4. Integratie van de Conversation Experience (PLATFORM-002).
5. Uitbreiding naar spraakgestuurde interactie.
6. Uitbreiding naar meerdere Experience Layers (DCOD, Dutch Carpets, dealers, white-label — PLATFORM-001 §2/§6).

## Langetermijnvisie

De gebruiker ervaart uiteindelijk geen AI-tool, maar één geïntegreerde ontwerpstudio waarin een natuurlijke ontwerpdialoog de bestaande Design Brain aanstuurt. *"Van woord tot vloer"* wordt daarmee letterlijk: een gesprek vormt het begin van een volledig reproduceerbare ontwerpworkflow.

---

## Consistentietoets

- **PLATFORM-001:** de Design Dialogue is een Experience Layer-uitbreiding; workflow, capabilities, merk- en kanaalscheiding blijven zoals vastgelegd.
- **AB-012:** "ontwerpcollega, geen AI-chatbot" is de directe uitdrukking van de verborgen AI-infrastructuur; de dialoog toont nooit model, sleutel of techniek.
- **BUILD-007 / BUILD-023 / IMP-014:** de dialoog activeert capabilities uitsluitend via de bestaande ketenvolgorde, gates en reuse-/orkestratieregels (AP-001) — geen nieuwe reasoning-triggers, geen omzeiling.
- **BUILD-004 / BUILD-017 / BUILD-019:** contextinterpretatie, gespreksregie en persistent geheugen zijn de bestaande dragers van de Design Dialogue; geen nieuw domeinobject nodig.
- **REASONING-001:** de dialoog verklaart keuzes en bewaakt consistentie zonder zelf te redeneren; de ontwerpintelligentie blijft bij de Design Brain.
- **BUILD-024:** modaliteitsuitbreidingen leveren dezelfde platte contractinvoer; de boundary-contracten blijven ongewijzigd en additief.

---

**Reviewgereed:** dit visiedocument legt de Conversation Experience / Design Dialogue vast als richtinggevende Experience Layer-uitbreiding van PLATFORM-001 — een natuurlijke ontwerpdialoog die context verzamelt, het gesprek bewaakt, de bestaande capabilities via de bestaande gates/orkestratie activeert en resultaten natuurlijk presenteert, zonder eigen ontwerpintelligentie en zonder enige wijziging aan de Design Workflow, de Design Brain, de orchestrator, de contracten, de resultaatobjecten of de componentgrenzen. De bestaande architectuur blijft volledig leidend.
