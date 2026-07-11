# AB-003 — Concept-Architectuurbesluit: canonieke naamswijzigingen (Ontwerpvisie, Project-/Ruimtecontext)

**Status:** concept, ter beoordeling. Geen enkel bestaand document is gewijzigd. Uitwerking van agendapunt **T1** uit `ARCHITECTUUR_BESLUITVORMINGSAGENDA_FASE_2.md` (roadmap Sprint 1 — Opruiming; §5 markeert T1 als Architectuurbesluit).

**Vraagstelling:** worden de twee door Regel 1 van `DESIGN_BRAIN_ARCHITECTUURVISIE.md` voorgeschreven hernoemingen — Projectcontext → Project-/Ruimtecontext en Ontwerpintentie → Ontwerpvisie — hierbij definitief als canonieke architectuurwoordenschat vastgesteld?

**Scope:** uitsluitend deze twee hernoemingen. De derde koppeling uit Regel 1 (Design Reasoning ↔ Ontwerpredenering) valt onder een apart agendapunt (T4) en wordt hier nadrukkelijk **niet** besloten.

---

## 1. Vastgestelde feiten

Uitsluitend letterlijke of ondubbelzinnige inhoud uit bestaande documenten, geen interpretatie:

- **F1.** `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, Regel 1 (regel 51): "Concreet minimaal te koppelen: Projectcontext ↔ Project-/Ruimtecontext, Ontwerpintentie ↔ Ontwerpvisie, Design Reasoning ↔ Ontwerpredenering. Deze mapping moet zijn vastgesteld vóórdat er componenten op worden gebouwd."
- **F2.** `DESIGN_CONTEXT_MODEL.md` hanteert de nieuwe termen al als canonieke laagnamen: Laag 1 = **Ontwerpvisie** (regel 19), Laag 2 = **Project-/Ruimtecontext** (regel 35). De nieuwe termen zijn dus geen nieuw te introduceren begrippen, maar de reeds bestaande, bevroren laagnamen.
- **F3.** `DESIGN_CONTEXT_MODEL.md` is het bevroren model v1.0 en de canonieke domeinbeschrijving; `DESIGN_BRAIN_ARCHITECTUURVISIE.md` (regels 41–43) stelt expliciet dat dit model "ongewijzigd blijft" en dat de Architectuurvisie "nadrukkelijk geen vervanging of herziening daarvan" is.
- **F4.** `AR-002_DESIGN_BRAIN_HARMONISATIE_ANALYSE.md`, regel 41: Regel 1 is "gedeeltelijk uitgevoerd in de praktijk ... maar nooit als het voorgeschreven, zelfstandige artefact opgeleverd." De formele afronding ontbreekt dus, ook al is de praktijk grotendeels al zo.
- **F5.** De oude term **"Ontwerpintentie"** komt in de operationele/bevroren documenten (`DESIGN_CONTEXT_MODEL.md`, `SPEC-000_PROJECT_CHARTER.md`, `BUILD-004`) nergens meer voor als werkterm; hij staat alleen nog in de mapping zelf (F1) en in analysedocumenten (AR-001, AR-002). Deze term is in de praktijk dus al volledig vervangen door Ontwerpvisie.
- **F6.** De oude term **"Projectcontext"** komt daarentegen nog letterlijk voor, uitsluitend als informele prozaterm, niet als concurrerende laagnaam:
  - `DESIGN_CONTEXT_MODEL.md`, regel 54 (doel van laag 3): "de professionele vertaalslag tussen Ontwerpvisie + Projectcontext ..." — binnen het bevroren model zelf, terwijl de canonieke laag-2-naam in datzelfde document Project-/Ruimtecontext is (F2);
  - `SPEC-000_PROJECT_CHARTER.md`, regel 51 (uitgangspunt): "Projectcontext is leidend ...";
  - `DESIGN_BRAIN_ARCHITECTUURVISIE.md`, regels 16 en 24 (de ontwerpketen en het tweede uitgangspunt);
  - `BUILD-004_CONTEXT_INTERPRETER_FUNCTIONEEL_ONTWERP.md`, regels 9 en 88 (proza en een tussenkopje).
- **F7.** `BUILD-004_CONTEXT_INTERPRETER_FUNCTIONEEL_ONTWERP.md`, regel 90, heeft "Projectcontext" al expliciet ontleed naar de canonieke lagen: "Gewenste beleving" hoort bij Laag 1 (Ontwerpvisie), de overige informatie bij Laag 2 (Project-/Ruimtecontext). Waar de oude umbrella-term nog opdook, is de laagtoewijzing dus al vastgesteld.

## 2. Architectuurinterpretaties

Redeneringen die de feiten verbinden — zelf geen feit, wel direct herleidbaar:

- **I1.** Uit F2 + F5 volgt dat de hernoeming Ontwerpintentie → Ontwerpvisie feitelijk al volledig is doorgevoerd: er bestaat geen enkele werkterm meer die met "Ontwerpvisie" concurreert. Het besluit is hier louter bekrachtiging van een voldongen feit.
- **I2.** Uit F2 + F6 + F7 volgt dat de hernoeming Projectcontext → Project-/Ruimtecontext op laagnaam-niveau al is voltooid (de canonieke laagnaam is eenduidig Project-/Ruimtecontext), maar dat het oude woord nog als informele prozaterm rondloopt. Er is dus geen tweede, concurrerend vocabulaire; er is één canoniek begrip met een verouderd synoniem dat plaatselijk in proza is blijven staan.
- **I3.** Uit F3 volgt dat dit besluit de resterende prozavermeldingen van "Projectcontext" niet kan noch mag "repareren" in de bevroren documenten: dat zou wijziging van het bevroren model (F6, regel 54) en van SPEC-000 vergen, wat buiten de aard van dit besluit en buiten de opdracht valt.

## 3. Architectuurkeuze

**K1.** De canonieke architectuurwoordenschat gebruikt vanaf nu uitsluitend:
  - **Ontwerpvisie** (DesignContext Model, Laag 1) — de term "Ontwerpintentie" vervalt als architectuurbegrip en is voortaan uitsluitend een historisch synoniem;
  - **Project-/Ruimtecontext** (DesignContext Model, Laag 2) — de term "Projectcontext" vervalt als architectuurbegrip en is voortaan uitsluitend een historisch synoniem (informele afkorting).

**K2.** Hiermee zijn twee van de drie koppelingen uit Regel 1 (F1) formeel afgerond. De derde koppeling (Design Reasoning ↔ Ontwerpredenering) blijft expliciet buiten dit besluit en wordt onder T4 behandeld.

**K3.** Dit besluit introduceert geen nieuw begrip: beide canonieke termen bestaan al als bevroren laagnamen (F2). De keuze is uitsluitend het formeel buiten gebruik stellen van de twee oude synoniemen als architectuurterm.

### Toepassingsregels

Wat "canonieke terminologie" concreet betekent:

- **Verplicht** in alle nieuwe of herziene architectuur-, ontwerp- en BUILD-documenten, en in alle nieuwe code, identifiers en interfaces: uitsluitend Ontwerpvisie en Project-/Ruimtecontext.
- **Nog toegestaan** blijven de historische termen (Ontwerpintentie, Projectcontext) uitsluitend als citaat uit, of verwijzing naar, bestaande documenten, en in analyse-/historische documenten die de oude situatie beschrijven — nooit als werkterm in nieuw materiaal.
- **Geen terugwerkende kracht:** bestaande, bevroren documenten (waaronder DesignContext Model v1.0 en SPEC-000) worden op grond van dit besluit niet aangepast; hun bestaande formuleringen blijven staan onder hun eigen wijzigingsregime.

## 4. Overwogen alternatieven

- **Alternatief 1 — Beide vocabulaires als gelijkwaardige synoniemen naast elkaar toestaan.** *Afgewezen*: in directe strijd met de intentie van Regel 1 (F1), die stelt dat "er nooit twee vocabulaires naast elkaar bestaan voor dezelfde werkelijkheid."
- **Alternatief 2 — De oude termen tot canoniek verheffen en de laagnamen aanpassen.** *Afgewezen*: zou wijziging van het bevroren DesignContext Model v1.0 vergen (F3) en de reeds bestaande, breed toegepaste laagnamen (F2) omgooien — onnodig en in strijd met het bevriezingsprincipe.
- **Alternatief 3 — Niets formeel besluiten, want "in de praktijk al zo".** *Afgewezen*: F4 legt vast dat Regel 1 een expliciet, zelfstandig artefact als precondition eist ("Deze mapping moet zijn vastgesteld vóórdat er componenten op worden gebouwd"). Zolang dat ontbreekt, blijft de precondition formeel open, ook al is de praktijk al gemigreerd.
- **Alternatief 4 (voorgesteld) — De twee canonieke termen bekrachtigen en de oude termen tot historisch synoniem verklaren, zonder enige bevroren of bestaande tekst te wijzigen.** Zie hoofdstuk 3. De enige lezing die consistent is met alle feiten (F1–F7) én met het bevriezingsprincipe (F3).

## 5. Consequenties van het besluit

- De precondition van Regel 1 ("mapping vastgesteld vóórdat componenten worden gebouwd") is voor déze twee termen formeel vervuld. Toekomstige component-BUILD's kunnen zich zonder terminologische dubbelzinnigheid op Ontwerpvisie en Project-/Ruimtecontext baseren.
- **Geen enkel bestaand document wordt door dit besluit gewijzigd.** In het bijzonder blijven het bevroren DesignContext Model v1.0 en SPEC-000 ongemoeid; de resterende prozavermeldingen van "Projectcontext" (F6) zijn geen fouten die dit besluit herstelt, maar verouderd synoniem-gebruik dat onder het eigen wijzigingsregime van elk document valt.
- De prozavermeldingen in `DESIGN_BRAIN_ARCHITECTUURVISIE.md` (F6: de ontwerpketen op regel 16 en het uitgangspunt op regel 24) zijn kandidaten om mee te lopen wanneer de Architectuurvisie zelf wordt herschreven of vervangen — dat is agendapunt **T12** (consolidatie), niet dit besluit.
- Geen codewijziging: dit besluit speelt zich uitsluitend op documentatie-/woordenschatniveau af.
- Er ontstaat een stabiele terminologische basis als randvoorwaarde voor T4 (Design Reasoning ↔ Ontwerpredenering) en de latere component-BUILD's.

## 6. Scope-afbakening (wat dit besluit uitdrukkelijk niet doet)

- Het besluit **niet** over Design Reasoning ↔ Ontwerpredenering (T4).
- Het herschrijft of archiveert de Architectuurvisie **niet** (T12).
- Het wijzigt het bevroren DesignContext Model of SPEC-000 **niet** (F3), ook niet om de residuele "Projectcontext"-vermeldingen op te schonen.
- Het raakt geen andere ketenbegrippen (Ontwerpsignatuur, Concept, Materialisatie, e.d.).

## 7. Conclusie

Anders dan bij AB-001 is hier een **volledig** Architectuurbesluit mogelijk: de canonieke termen bestaan al (F2), de oude termen zijn óf volledig vervangen (Ontwerpintentie, F5/I1) óf uitsluitend nog als informeel synoniem aanwezig (Projectcontext, F6/I2), en het besluit vergt geen wijziging van enig bevroren document (I3). Het voorstel (hoofdstuk 3, K1–K3) wordt in zijn geheel ter goedkeuring voorgelegd.
