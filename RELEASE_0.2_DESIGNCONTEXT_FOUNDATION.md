# Release 0.2 – DesignContext Foundation

**Doelgroep van dit document:** een DCOD-ontwikkelaar die de codebase kent, maar niet aanwezig was bij de ontwerpbeslissingen tijdens deze release. Dit document beschrijft daarom niet alleen wát is gebouwd, maar vooral waaróm — zodat de redenering navolgbaar blijft, ook wanneer de mensen die deze beslissingen namen niet meer om uitleg gevraagd kunnen worden.

---

## Status

Release 0.2 is de eerste architectuurrelease van de nieuwe DCOD Dessinator.

De bestaande functionaliteit is volledig behouden. Elke stap in deze release is getest tegen de bestaande output, en niets in de gebruikerservaring is veranderd. Alle wijzigingen zijn intern en vormen het fundament voor de verdere ontwikkeling van de DesignContext-architectuur.

---

## Doel van deze release

De Dessinator werkte, vóór deze release, als een rechte lijn: een prompt ging naar Claude, Claude gaf een JSON-analyse terug, keyword-matching bepaalde een stijl, en een generator-functie tekende een SVG. Die lijn functioneerde, maar had geen geheugen van *waarom* een keuze was gemaakt, geen onderscheid tussen wat een architect had vastgesteld en wat de AI had geraden, en geen plek om een beslissing als "de vloer" (stijl, materiaal, productie) uit elkaar te trekken. Elke uitbreiding moest worden ingebouwd als nóg een keyword-check in een functie die daar al te veel van had.

Tijdens de Discovery-fase is een kern-inzicht geformuleerd dat de aanleiding vormt voor deze hele release: **de kern van de Dessinator is niet de prompt, maar de ontwerpcontext.** Een prompt is een momentopname. Een ontwerpproces — van vaag idee, via een gekozen aanpak, naar een concreet en produceerbaar vloerconcept — is een opeenvolging van beslissingen die op elkaar voortbouwen en elkaar niet mogen tegenspreken.

Er is bewust gekozen om de Dessinator **niet opnieuw te bouwen**. De bestaande generator-functies (28 stuks, in `modules_extra.py`) zijn stabiel, bewezen, en in productie gebruikt. Een rewrite zou dat vertrouwen wegvegen zonder aantoonbare winst. In plaats daarvan is gekozen voor een gecontroleerde evolutie: een nieuw domeinmodel, **DesignContext**, is naast de bestaande architectuur gebouwd en heeft er stap voor stap, bewezen stap voor stap, autoriteit van overgenomen — nooit meer dan wat op dat moment kon worden aangetoond als veilig.

DesignContext is met deze release het centrale domeinmodel geworden waarop toekomstige functionaliteit wordt gebaseerd. Niet omdat het model "mooier" is dan de oude aanpak, maar omdat het een structureel probleem oplost dat de oude aanpak niet kón oplossen: het onderscheid tussen wie een beslissing mag nemen, wanneer die beslissing vaststaat, en waarom die is genomen.

---

## Opgeleverde BUILD's

### BUILD-001A – Foundation

DesignContext is geïntroduceerd als een volledig geïsoleerde module (`design_context.py`), losstaand van `app.py` en `modules_extra.py`. Het bevatte bij oplevering uitsluitend een datastructuur — de zes lagen van het DesignContext Model (Ontwerpvisie, Project-/Ruimtecontext, Ontwerpstrategie, Concept, Materialisatie, Productierealisatie) plus de doorlopende Ontwerpredenering — zonder enige bedrijfslogica.

Geen enkel bestaand bestand kreeg een afhankelijkheid van deze module. Er waren daarmee, per constructie, geen functionele wijzigingen mogelijk: het skelet kon volledig verwijderd worden zonder de Dessinator te raken. Dat was precies het punt — bewijzen dat het domeinmodel kon bestaan, vóórdat het ergens op zou steunen.

### BUILD-001B – Observation

DesignContext werd voor het eerst gekoppeld aan de bestaande generatie-flow (`api_generate()`), maar uitsluitend **observationeel**: bij elke request werd een DesignContext opgebouwd uit dezelfde gegevens als de bestaande `analysis`-dictionary, en beide werden met elkaar vergeleken (de "Parallelle Validatie"). De bestaande pipeline bleef volledig leidend — DesignContext keek toe, het stuurde niets.

Dit was een bewuste tussenstap. Het stelde de vraag "vertaalt DesignContext de werkelijkheid correct?" vóórdat de vraag "mag DesignContext de werkelijkheid bepalen?" aan de orde kwam. De validatie leverde ook een onverwacht, waardevol neveneffect op: ze legde een reeds bestaande zwakte in de oude architectuur bloot — stijl wordt op twee onafhankelijke plekken bepaald (`api_generate()` én `build_tile_svg()`), die elkaar in theorie kunnen tegenspreken. Die bevinding is bewust *niet* meteen opgelost, maar vastgelegd als toekomstig werk (zie "Bewust nog niet uitgevoerd").

### BUILD-002 – First Authority

Het kleurpalet werd de eerste ontwerpbeslissing die daadwerkelijk leidend werd vanuit DesignContext, met de oude `analysis`-bron als expliciete fallback. Dit was niet toevallig de eerste keuze: van alle kandidaten was kleurpalet de enige waarvan empirisch was aangetoond (via de Parallelle Validatie) dat hij op precies één plaats in de code werd vastgesteld en nooit meer werd gewijzigd — in tegenstelling tot stijl.

Er is expliciet getest of oude en nieuwe pipeline **niet te onderscheiden** waren: identieke SVG-output, identieke kleurwaarden, identieke JSON-respons naar de frontend, identieke mockup-weergave. De migratie was daarmee onzichtbaar voor de architect die de Dessinator gebruikt — een randvoorwaarde die vanaf hier voor elke volgende BUILD is blijven gelden.

### BUILD-003 – Shared Authority

Repeat-type (het herhaalpatroon: full, half-drop, brick, mirror) werd de tweede leidende beslissing, dit keer bewust gekozen om een ander punt te bewijzen dan BUILD-002: niet de veiligste migratie, maar de migratie die het sterkste bewijs levert dat DesignContext een echte, gedeelde bron van waarheid is. Repeat-type wordt geconsumeerd door `build_repeat_svg()` — een andere functie dan `build_tile_svg()`, die het kleurpalet gebruikt.

Er is aangetoond, niet aangenomen, dat deze twee functies elkaar niet kennen: een AST-analyse van de broncode bevestigde dat `build_tile_svg()` en `build_repeat_svg()` elkaar nergens aanroepen. De enige plek waar hun beslissingen samenkomen is de ene DesignContext-instantie die `api_generate()` per request opbouwt. Dat is de eerste keer dat meerdere, onafhankelijke onderdelen van de Dessinator dezelfde bron van waarheid gebruiken zonder onderlinge afhankelijkheid.

---

## Architectuurresultaat

```
Architect
   │
   ▼
DesignContext
   │
   ├──▶ build_tile_svg()      (kleurpalet, BUILD-002)
   │
   └──▶ build_repeat_svg()    (repeat-type, BUILD-003)
```

In de oorspronkelijke architectuur bestond geen gedeeld middelpunt: elke functie las rechtstreeks uit dezelfde losse `analysis`-dictionary en dezelfde losse request-parameters, en elke uitbreiding voegde een nieuwe, ad-hoc afhankelijkheid toe tussen willekeurige stukken code. Er was geen plek die kon zeggen "dit is wat er nu geldt, en dit is waarom" — alleen een optelsom van losse aannames verspreid over `app.py`.

Het fundamentele verschil is dat er nu één plek is — DesignContext — waar een ontwerpbeslissing wordt vastgelegd, en dat meerdere, onafhankelijke functies daaruit kunnen putten zonder van elkaar te hoeven weten. Dat is niet alleen netter, het is een andere eigenschap van het systeem: nieuwe functionaliteit kan een beslissing uit DesignContext consumeren zonder de functie te hoeven kennen die diezelfde beslissing ook gebruikt, en zonder het risico dat twee plekken in de code een tegenstrijdig antwoord geven op dezelfde vraag.

---

## Bewust nog NIET uitgevoerd

Deze release is doelbewust onvolledig. Onder andere:

- **De dubbele stijl-routering is niet geconsolideerd.** Stijl wordt nog steeds op twee plekken bepaald (`api_generate()` en `build_tile_svg()`). Dit is de bekendste, meest risicovolle inconsistentie in de bestaande architectuur — en precies daarom bewust *niet* als eerste of tweede migratie gekozen. Eerst is bewezen dat het model werkt op ondubbelzinnige, single-source beslissingen (kleurpalet, repeat-type); pas daarna is het verantwoord om een beslissing te migreren die twee bestaande, elkaar tegensprekende bronnen moet vervangen door één.
- **De keyword-logica is niet samengevoegd.** Dat hangt direct samen met bovenstaand punt en wacht op dezelfde voorwaarde.
- **Er zijn geen verdere ontwerpbeslissingen gemigreerd** buiten kleurpalet en repeat-type. Complexiteit, motief-schaal, tegelmaat en resolutie zijn geïdentificeerd als kandidaten (zie BUILD-003_ADVIES.md), maar bewust niet meegenomen — elke migratie in deze release had een eigen, specifiek architectonisch doel, geen kwantitatieve voortgang ("zoveel mogelijk velden migreren").
- **DesignContext is geen volledige autoriteit.** De bestaande `analysis`-dictionary blijft voor het overgrote deel van de beslissingen (stijl, complexiteit, vormen) de bron van waarheid. DesignContext observeert deze nog, stuurt ze niet aan.

De reden voor dit uitstel is consistent door de hele release heen: elke stap moest **bewijsbaar** zijn voordat de volgende werd gezet. Een architectuur die in één keer volledig wordt overgenomen, is een architectuur waarvan niemand meer met zekerheid kan zeggen welk onderdeel het eventuele probleem veroorzaakt. Een architectuur die veld voor veld, functie voor functie wordt overgenomen — met expliciete rollback per stap — blijft op elk moment controleerbaar.

---

## Belangrijkste ontwerpprincipes

Deze uitgangspunten zijn gedurende de hele release gevolgd en blijven leidend voor toekomstig werk op DesignContext:

- **Evolueren, niet herbouwen.** De bestaande, bewezen Dessinator blijft de basis. Nieuwe architectuur bewijst zichzelf ernaast, niet in plaats van.
- **Eén bron van waarheid.** Voor elke gemigreerde beslissing bestaat precies één plek waar die wordt vastgesteld — nooit twee concurrerende implementaties van dezelfde vertaalslag.
- **Gecontroleerde migraties.** Elke BUILD migreert één, scherp afgebakende beslissing, nooit meerdere tegelijk.
- **Rollback bij iedere BUILD.** Elke stap is in minuten terug te draaien door een enkele, geïsoleerde wijziging ongedaan te maken — nooit door een grotere reeks samenhangende aanpassingen te moeten ontrafelen.
- **Bewijs vóór aannames.** Elke migratie is getest op identieke output vóór livegang — nooit op basis van "dit zou moeten werken".
- **De architect bepaalt de ontwerpvisie.** Dit principe komt rechtstreeks uit het DesignContext Model: DCOD's systemen mogen interpreteren en voorstellen, maar alleen de architect kan de ontwerpvisie definitief bevestigen.
- **DCOD ondersteunt en faciliteert.** De rol van DCOD in het model — en daarmee van elke functie die namens DCOD handelt — is het inbrengen van vakkennis en het bewaken van haalbaarheid, niet het overnemen van de beslissing die bij de architect hoort.

---

## Resultaat

In technische termen: twee ontwerpbeslissingen (kleurpalet, repeat-type) worden nu aantoonbaar en zonder onderlinge afhankelijkheid vanuit één gedeeld domeinmodel aangestuurd, met volledig behoud van bestaande functionaliteit en een bewezen rollback-pad per stap.

Maar de betekenis van deze release reikt verder dan die techniek. Vóór Release 0.2 was de Dessinator een SVG-generator: een functie die tekst omzette in een patroon. Met DesignContext als fundament beschikt de Dessinator nu over een eigen ontwerpmodel — een structuur die onderscheid maakt tussen een visie, een aanpak, een concept en een productiewerkelijkheid, en die vastlegt wie welke beslissing mag nemen en waarom. Dat is niet enkel een interne opschoning. Het is de voorwaarde die nodig is om de Dessinator, in de toekomst, daadwerkelijk als ontwerpadviseur naast de architect te laten functioneren, in plaats van als los generatie-hulpmiddel.

---

## Vooruitblik

BUILD-004 zal zich richten op de eerste echte DesignContext-gestuurde dialoog met de architect — het moment waarop DesignContext niet langer alleen bestaande beslissingen overneemt, maar voor het eerst een rol speelt in hoe die dialoog zelf verloopt. Dit document beschrijft nog geen implementatie voor die stap, alleen de richting: de fundering die met Release 0.2 is gelegd, is bedoeld om precies dát mogelijk te maken.
