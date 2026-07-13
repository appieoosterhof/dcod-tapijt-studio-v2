# BUILD-025 — Conversation Experience & Voice Architecture: technisch ontwerp

**Status:** architectuur- en contractspecificatie. **Geen code, geen wijziging aan enige bestaande component, geen wijziging aan enige Reasoning Capability.** Legt de additieve architectuur vast waarmee de gebruiker de Dessinator niet alleen typt maar ook kan *spreken*. Technische uitwerking van de visie in PLATFORM-002 (Design Dialogue); PLATFORM-002 blijft leidend voor het "waarom", BUILD-025 beschrijft het "hoe/waar" — zonder de bestaande architectuur te raken.

**Bindend / respecteert:** AB-006, AB-009, AB-012, BUILD-007, BUILD-023, IMP-014, BUILD-024, PLATFORM-001, PLATFORM-002, REASONING-001, SEC-001.

**Kernprincipe (architectonisch geborgd):** spraak is uitsluitend een **in-/uitvoermodaliteit in de Experience Layer**. Speech-to-Text (STT) levert exact dezelfde platte tekst-`invoer` die het toetsenbord vandaag al aan het bestaande `/dialoog`-endpoint geeft; Text-to-Speech (TTS) spreekt exact dezelfde tekst uit die de studio vandaag al toont. **De Design Brain, de contracten en de workflow ontvangen nooit audio en veranderen niet.**

---

## Uitgangspunten

De bestaande keten blijft exact:

```
Gebruiker → Conversation Planner (BUILD-017) → Context Interpreter (BUILD-004) → Design Brain → Design Workflow (BUILD-007)
```

De Conversation Experience is een **nieuwe Experience Layer** (PLATFORM-001 §2) *boven* deze keten. Zij voegt modaliteiten en gespreksregie toe; zij voegt **geen** ontwerpintelligentie toe en wijzigt de keten niet.

## 1. Conversation Experience

De Conversation Experience ondersteunt drie modaliteiten die alle op dezelfde tekst-`invoer` uitkomen:

- **Getypte interactie** — het huidige gedrag (`/dialoog` met `{invoer: tekst}`), ongewijzigd.
- **Gesproken interactie** — audio → STT → dezelfde tekst-`invoer`; het antwoord (studio-tekst) → TTS → audio.
- **Hybride interactie** — de gebruiker wisselt vrij tussen spreken en typen binnen hetzelfde gesprek (`gesprek_id`); de modaliteit is een presentatiekeuze, niet een gespreks- of ontwerpkeuze.

Gespreksregie (uitsluitend Experience Layer, zonder reasoning):
- **Onderbreken** — de gebruiker kan de TTS-weergave onderbreken; dit stopt alleen de *presentatie*, niet een reeds afgeronde reasoning-stap.
- **Verduidelijken** — bij lage zekerheid vraagt de studio door; dit gebruikt de bestaande Context Interpreter-interpretaties (`zekerheid`) en de Conversation Planner, niet een nieuwe capability.
- **Samenvatten** — de studio vat de opgebouwde context/keuzes samen; puur presentatie van reeds vastgelegde `DesignContext`-/resultaatgegevens.
- **Bevestigen** — bevestiging blijft een expliciete gebruikersactie op de bestaande gates (AB-006, BUILD-007); spraak ("ja, bevestig") mag de bevestiging *aansturen*, maar de bevestiging zelf blijft dezelfde expliciete stap.

## 2. Voice Architecture

Vier duidelijk gescheiden verantwoordelijkheden; **Voice is géén onderdeel van de Design Brain**:

| Component | Verantwoordelijkheid | Laag | Kent de Design Brain? |
|---|---|---|---|
| **Speech-to-Text (STT)** | audio → tekst | Experience Layer (modaliteit-adapter) | nee — levert alleen tekst |
| **Text-to-Speech (TTS)** | studio-tekst → audio | Experience Layer (modaliteit-adapter) | nee — ontvangt alleen tekst |
| **Conversation Manager** | turn-taking, onderbreken, modaliteitswissel, samenvatten/verduidelijken aansturen | Experience Layer (regie) | nee — roept de bestaande endpoints aan |
| **Design Brain** | ontwerpredenering (de vijf Reasoning Capabilities + planners) | Domein | n.v.t. — ongewijzigd |

- **STT/TTS zijn injecteerbare, vervangbare adapters** (net als de `ModelClient`-poort voor reasoning): een concrete STT-/TTS-implementatie (browser-API of externe dienst) wordt via configuratie gekozen; de Conversation Manager kent alleen een abstracte `SpraakInvoer`- en `SpraakUitvoer`-interface, geen leverancier.
- **De Conversation Manager praat uitsluitend met de bestaande HTTP-endpoints** (`/dialoog`, `/ontwerpstrategie`, `/concept`, `/floor-designs`, …) en de bestaande `Gesprekstoestand` (`gesprek_id`); hij introduceert geen nieuw domeinobject en geen nieuwe reasoning.
- **AB-012 blijft gelden in spraak:** TTS spreekt uitsluitend de neutrale studio-taal; nooit model-, sleutel-, kosten- of foutdetails. Bij onbeschikbaarheid dezelfde neutrale melding, uitgesproken.

## 3. Platform-onafhankelijkheid

Dezelfde, ongewijzigde Design Brain wordt door elke Experience Layer via dezelfde endpoints gebruikt:

```
Web Studio ─┐
Tablet ─────┤
Mobiele app ┤→  Conversation Experience (modaliteit + regie)  →  bestaande /api/design-brain-endpoints  →  Design Brain
Dealer Portal ┤
Dutch Carpets ┘   (branding/rechten/navigatie = Experience Layer; PLATFORM-001 §2/§6)
```

Elke modaliteit (tekst, spraak, later beeld) levert uiteindelijk dezelfde platte contract-invoer aan de bestaande boundaries (BUILD-024). Een nieuw kanaal of merk is een nieuwe Experience Layer-instantie, geen wijziging aan de Design Brain.

## 4. Gespreksfilosofie

De Dessinator is een **ontwerpcollega**, geen chatbot en geen vraag-antwoordmachine: samen ontwerpen, context opbouwen, keuzes verklaren, consistentie bewaken. Dit is de directe voortzetting van REASONING-001 (onderbouwd, uitlegbaar, dienend; de studio stelt voor, de mens beslist) en van het Ontwerpstudio-principe (BUILD-022 §9, AB-012). Spraak verandert de *toon en toegankelijkheid* van het gesprek, niet de rol: de ontwerpintelligentie blijft volledig in de Design Brain.

## 5. Gespreksstroom

De canonieke stroom kent **acht fasen**, alle uitgedrukt in de bestaande keten (geen nieuwe reasoning, geen nieuwe workflow):

```
Gebruiker → Begroeting → Verkennen → Verdiepen → Samenvatten → Bevestigen → Ontwerpen → Presenteren → Vervolg
```

| # | Fase | Wat gebeurt er | Laag / mechanisme |
|---|---|---|---|
| 1 | **Begroeting** | de studio opent en verwelkomt; toon zetten als ontwerpcollega | Experience Layer (presentatie); nog geen reasoning |
| 2 | **Verkennen** | de gebruiker vertelt (tekst/spraak) wat hij wil; eerste context wordt herkend | Context Interpreter (BUILD-004) → laag 1/2 interpretaties (nog niets bevestigd) |
| 3 | **Verdiepen** | de studio stelt relevante vervolgvragen en bouwt context verder op | Conversation Planner (BUILD-017); groeit in de `Gesprekstoestand` |
| 4 | **Samenvatten** | de studio vat de opgebouwde context en keuzes terug, ter controle | Experience Layer (presentatie van `DesignContext`); geen reasoning |
| 5 | **Bevestigen** | de gebruiker bevestigt expliciet (visie/strategie/concept/…); spraak kan dit aansturen | de bestaande gates (AB-006, BUILD-007); blijft een expliciete gebruikersactie |
| 6 | **Ontwerpen** | de Design Brain redeneert: Ontwerpstrategie → Concept → Floor Design → Material → Pattern | bestaande capabilities + BUILD-023-orkestratie (reasoning alleen bij nieuwe ontwerpwaarde) |
| 7 | **Presenteren** | resultaten worden getoond en desgewenst uitgesproken, in studio-taal | Experience Layer + TTS (AB-012: geen techniek/model/fout) |
| 8 | **Vervolg** | de gebruiker verfijnt; gewijzigde bevestigde upstream invalideert gericht downstream | BUILD-023 R4 (gerichte invalidatie), exact zoals nu |

De cyclus is iteratief: **Vervolg** keert terug naar **Verdiepen/Samenvatten/Bevestigen** voor de volgende ontwerpstap. Elke fase valt binnen de bestaande keten en de bestaande bevestigingsmomenten; de Conversation Experience voegt uitsluitend regie en modaliteit toe, geen ontwerpbeslissing.

## 6. Architectuurgrenzen (expliciet)

- **Voice ≠ Reasoning** — STT/TTS raken nooit een reasoning-boundary; zij verwerken alleen audio↔tekst. Een boundary ontvangt uitsluitend platte tekst/dicts (BUILD-024), nooit audio.
- **Conversation ≠ Workflow** — de Conversation Manager bepaalt *hoe* het gesprek loopt (modaliteit, turn-taking, onderbreken); de Design Workflow (BUILD-007) bepaalt *welke* ontwerpstappen volgen. De Manager roept de workflow aan, hij herdefinieert hem niet.
- **Experience ≠ Design Brain** — branding, modaliteit, navigatie en presentatie leven in de Experience Layer; alle ontwerpbeslissingen in de Design Brain. De scheiding is dezelfde als in PLATFORM-001/002.

## 7. Toekomstvastheid

De architectuur is voorbereid op nieuwe modaliteiten en kanalen **zonder wijziging aan de Design Brain**, doordat elke modaliteit een adapter is die op de bestaande platte contract-invoer uitkomt:

| Uitbreiding | Adapterrol (Experience Layer) | Raakt Design Brain? |
|---|---|---|
| Mobiele app / tablet | UI + dezelfde endpoints | nee |
| Spraak | STT/TTS-adapter → tekst | nee |
| Camera / foto's | beeld → context-interpretatie (bestaande interpretatierol) → tekst/parameters | nee |
| LiDAR / AR / VR | ruimtescan → context/parameters, presentatie in 3D | nee |
| Toekomstige AI-modellen | nieuwe `ModelClient`-adapter achter de bestaande boundaries (BUILD-024 §5) | nee |

Elke uitbreiding is additief: zij voegt een adapter of Experience Layer toe, nooit een wijziging aan de contracten, de orchestratie of de Reasoning Capabilities.

---

## Consistentietoets

- **BUILD-007:** de ketenvolgorde en bevestigingsmomenten blijven exact; de Conversation Manager roept de bestaande stappen aan, herdefinieert ze niet.
- **BUILD-023 / IMP-014:** spraak start geen reasoning uit zichzelf; reasoning volgt uitsluitend de bestaande waarde-/reuse-regels (AP-001) via de bestaande endpoints.
- **BUILD-024:** boundaries ontvangen onveranderd platte dicts; audio bereikt nooit een contract. STT/TTS zijn, net als de `ModelClient`, injecteerbare, leverancier-onafhankelijke adapters.
- **PLATFORM-001 / PLATFORM-002:** Voice is een modaliteit binnen de Experience Layer / Design Dialogue; geen nieuwe architectuurlaag in de Design Brain.
- **REASONING-001:** de gespreksfilosofie (ontwerpcollega, onderbouwd, dienend) blijft leidend; spraak verandert de rol niet.
- **AB-012:** STT/TTS en de Conversation Manager tonen/spreken nooit model-, sleutel-, kosten- of foutdetails; onbeschikbaarheid = de neutrale melding.
- **SEC-001:** spraakdata is persoonsgegeven en gevoelig; de STT/TTS-adapter valt onder het geheimen-/privacybeleid ([Aanbevolen] server-side sleutels, dataminimalisatie, geen audio in de repo/logs) — de concrete provider-/privacykeuze is een expliciete IMP-beslissing, geen onderdeel van dit ontwerp.

---

**Reviewgereed:** dit technisch ontwerp legt de Conversation Experience & Voice Architecture vast als volledig additieve Experience Layer — drie modaliteiten (tekst/spraak/hybride) op dezelfde tekst-invoer, vier gescheiden verantwoordelijkheden (STT, TTS, Conversation Manager, Design Brain) met Voice nadrukkelijk buiten de Design Brain, platform-onafhankelijkheid via de bestaande endpoints/contracten, een op REASONING-001 gestoelde gespreksfilosofie, een gespreksstroom in de bestaande keten, harde architectuurgrenzen (Voice≠Reasoning, Conversation≠Workflow, Experience≠Design Brain) en toekomstvastheid voor mobiel/tablet/AR/VR/camera/LiDAR/nieuwe modellen — zonder enige wijziging aan de Design Brain, de contracten, de orchestratie of de Reasoning Capabilities.
