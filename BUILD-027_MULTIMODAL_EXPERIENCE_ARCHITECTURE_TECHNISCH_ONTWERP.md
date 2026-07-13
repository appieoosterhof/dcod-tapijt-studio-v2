# BUILD-027 — Multimodal Experience Architecture: technisch ontwerp

**Status:** architectuurspecificatie (Studio Experience Architecture, deel 2). **Geen code, geen implementatie, geen wijziging aan de Design Brain.** Beschrijft alle huidige en toekomstige in- en uitvoermodaliteiten en legt vast dat modaliteiten **uitsluitend Experience Layers** zijn: elke modaliteit is een adapter die reduceert tot de bestaande platte contract-invoer, en de Design Brain blijft volledig ongewijzigd.

**Bindend / respecteert:** AB-006, AB-009, AB-012, BUILD-004, BUILD-007, BUILD-023, IMP-014, BUILD-024, PLATFORM-001, PLATFORM-002, REASONING-001, SEC-001, BUILD-025, BUILD-026.

**Kernprincipe (architectonisch geborgd):** een modaliteit verandert **hoe** invoer wordt aangeleverd en uitvoer wordt getoond, nooit **wat** de Design Brain ontvangt. Elke invoermodaliteit-adapter produceert uiteindelijk óf platte tekst (de bestaande `invoer` voor de Context Interpreter/`/dialoog`) óf platte parameters binnen de bestaande contracten (BUILD-024). Elke uitvoermodaliteit-adapter presenteert uitsluitend de reeds bepaalde studio-resultaten.

---

## 1. Het reductieprincipe

```
[modaliteit] → modaliteit-adapter (Experience Layer) → platte tekst / platte parameters → bestaande endpoints → Design Brain (ongewijzigd)
```

Geen enkele modaliteit bereikt een reasoning-boundary in zijn oorspronkelijke vorm. Audio, beeld, PDF of scan worden door hun adapter **eerst gereduceerd** tot de bestaande contract-invoer. Zo erft elke nieuwe modaliteit automatisch de volledige, ongewijzigde Design Brain.

## 2. Invoermodaliteiten

| Modaliteit | Adapterrol (Experience Layer) | Reduceert tot |
|---|---|---|
| **Toetsenbord** | directe tekstinvoer (huidig gedrag) | `invoer` (tekst) → Context Interpreter |
| **Spraak** | Speech-to-Text (BUILD-025) | dezelfde `invoer` (tekst) |
| **Foto's** | beeld → beschrijving/kenmerken (interpretatie-rol, BUILD-004-analoog) | tekst/parameters (bv. sfeer, kleuren, ruimtetype) als interpretaties (zekerheid!) |
| **PDF** | document → relevante tekst (offerte, PvE, moodboardtekst) | tekst → Context Interpreter |
| **Moodboards** | beeldcollage → sfeer-/kleur-/stijlkenmerken | interpretaties (nooit bevestigde waarden) |
| **Camera (live)** | momentopname van de ruimte | zoals Foto's; plus optioneel ruimteparameters |
| **Video** | bewegend beeld → sleutelframes/beschrijving | zoals Foto's/Camera |
| **AR** | ruimte-overlay, plaatsing in situ | invoer: ruimtescan/positie; uitvoer: presentatie |
| **LiDAR** | ruimtescan → afmetingen/geometrie | platte parameters (ruimtemaat, vloeroppervlak) |
| **Toekomstige modaliteiten** | idem: een nieuwe adapter | tekst/parameters binnen de bestaande contracten |

**Belangrijk (REASONING-001 / BUILD-004):** beeld-/scan-afgeleide gegevens zijn **interpretaties met een zekerheid**, nooit bevestigde waarheden — exact zoals vrije tekst vandaag. De gebruiker bevestigt; de modaliteit stelt hooguit voor. Beeldinterpretatie is een *interpretatie-rol* (mogelijk een toekomstige capability/adapter), geen ontwerpbeslissing, en verandert de Design Brain niet.

## 3. Uitvoermodaliteiten

| Modaliteit | Adapterrol | Presenteert |
|---|---|---|
| **Scherm/tekst** | huidige weergave | studio-resultaten (concept, floor designs, materiaal, patroon, SVG, mockup) |
| **Spraak (TTS)** | Text-to-Speech (BUILD-025) | dezelfde studio-tekst, uitgesproken |
| **Beeld/SVG** | de bestaande productie-pipeline (AB-005/BUILD-018) | het gerenderde dessin |
| **Mockup/visualisatie** | Floor Visualization Engine | het dessin in de ruimte |
| **AR/VR** | 3D-presentatie-adapter | dezelfde resultaten, ruimtelijk getoond |

Alle uitvoer betreft **reeds bepaalde** resultaten; een uitvoermodaliteit neemt nooit een ontwerpbeslissing en toont nooit techniek/model/fout (AB-012).

## 4. Modaliteiten zijn uitsluitend Experience Layers

- Een modaliteit-adapter zit volledig in de **Experience Layer**; hij kent de Design Brain niet en wordt via configuratie gekozen (net als STT/TTS en de `ModelClient`).
- De **contracten (BUILD-024) veranderen niet**: boundaries ontvangen platte dicts, ongeacht welke modaliteit de waarden aanleverde.
- De **workflow (BUILD-007) verandert niet**: dezelfde ketenvolgorde en bevestigingsmomenten, ongeacht modaliteit.
- **Hybride gebruik** is triviaal: verschillende modaliteiten voeden hetzelfde `gesprek_id` (BUILD-026-contextbehoud); de gebruiker spreekt, typt en toont foto's door elkaar zonder statusverlies.

## 5. Grenzen (expliciet)

- **Modaliteit ≠ Reasoning** — een adapter reduceert/presenteert; hij redeneert niet.
- **Modaliteit ≠ Contract** — een adapter levert waarden *binnen* de bestaande contracten; hij wijzigt ze niet.
- **Modaliteit ≠ Design Brain** — de Design Brain is modaliteit-blind; zij ziet alleen platte tekst/parameters.

## 6. Toekomstvastheid

Elke toekomstige modaliteit (nieuwe sensor, nieuw kanaal, nieuw AI-model voor beeld/spraak) is een **additieve adapter**: zij sluit aan op het reductieprincipe (§1) en erft de ongewijzigde Design Brain. Er is nooit een wijziging aan de contracten, de orchestratie of de Reasoning Capabilities nodig om een modaliteit toe te voegen. Privacy- en providerkeuzes per modaliteit (bv. beeld/audio naar een externe dienst) zijn expliciete IMP-/beslismomenten (SEC-001), geen onderdeel van deze architectuur.

---

## Consistentietoets

- **BUILD-024:** alle modaliteiten reduceren tot de bestaande platte contract-invoer; geen contractwijziging.
- **BUILD-007 / BUILD-023:** ketenvolgorde, gates en orkestratie ongewijzigd; modaliteit start geen extra reasoning.
- **BUILD-004 / REASONING-001:** beeld-/scan-afgeleide gegevens zijn interpretaties met zekerheid, nooit bevestigde waarheden; de gebruiker bevestigt.
- **BUILD-025 / BUILD-026:** spraak en de gespreksstroom/-toestand zijn bijzondere gevallen van dit algemene modaliteit-adaptermodel.
- **PLATFORM-001/002:** modaliteiten zijn Experience Layers; merk/kanaal/modaliteit staan buiten de Design Brain.
- **AB-012 / SEC-001:** geen techniek/model/fout in enige modaliteit; beeld-/audio-/scandata is gevoelig en valt onder het privacybeleid, met provider-/privacykeuzes als expliciete IMP-beslissingen.

---

**Reviewgereed:** dit ontwerp legt de Multimodal Experience Architecture vast rond één reductieprincipe — elke in- of uitvoermodaliteit (toetsenbord, spraak, foto's, PDF, moodboards, camera, video, AR, LiDAR, toekomstige) is een Experience-Layer-adapter die reduceert tot de bestaande platte contract-invoer respectievelijk de reeds bepaalde studio-resultaten — zodat elke modaliteit de ongewijzigde Design Brain erft, met beeld-/scan-invoer als interpretatie (nooit waarheid) en met privacy-/providerkeuzes als expliciete latere IMP-beslissingen, zonder enige wijziging aan de contracten, de orchestratie of de Reasoning Capabilities.
