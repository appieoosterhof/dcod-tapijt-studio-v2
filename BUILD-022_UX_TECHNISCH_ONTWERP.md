# BUILD-022 — Technisch UX-/Frontendontwerp (de belevingslaag)

**Status:** technisch ontwerp, ter review (TR). Geen implementatie, geen code. Beschrijft uitsluitend **hoe** de experience uit BUILD-022 wordt gerealiseerd als **presentatielaag** bovenop de bestaande BUILD-021-frontend (`templates/ontwerp.html` + `static/js/ontwerp.js`). **Geen** nieuwe architectuur, component, endpoint, businesslogica of Design Brain-wijziging. Uitsluitend markup, CSS, animatie, microcopy en beeld — én statische beeld-assets.

**Scope van aanraking:** uitsluitend `templates/ontwerp.html` (markup + `<style>`) en `static/js/ontwerp.js` (render-/presentatiegedrag), plus optioneel statische afbeeldingen onder `static/`. Cache-stamp `?v=` wordt bij elke wijziging opgehoogd (CLAUDE.md-valkuil). De state-flow, de `fase()`-machine, alle endpoint-aanroepen en de ketenlogica blijven **byte-voor-byte in gedrag** gelijk; alleen hoe het resultaat wordt *getoond* verandert.

**Inventarisatie (bestaand):** IDs `#apiKey #nieuwGesprek #voortgang #gesprek #invoerrij #invoer #verstuur #actie #melding #samenvatting #viz #ruimte #eind #eindinhoud`; render via `render()` → `renderVoortgang/Gesprek/Actie/Viz/Samenvatting/Eind` (innerHTML-vervanging na elke respons); klassen `.paneel .kop .mijlpaal(.actief/.klaar/.bol) .bericht(.gebruiker/.dessinator) .kaart .keuze .stalen/.staal .mockup .leeg .bezig .eind.zichtbaar`; thema via CSS-variabelen; enige animatie nu `transition:opacity .15s` op knoppen.

---

## 1. Ruimtelijke compositie — atelier, geen dashboard

- **Van "panelen" naar "werkbank + beeldwand".** De rechter `#viz` wordt de **beeldwand**: dominant, groot, rustig — het beeld voert. De linker kolom wordt de **werkbank**: intiem, smal, met veel witruimte. Technisch: het bestaande `main`-grid herproportioneren (beeld zwaarder; bv. `minmax(340px,.85fr) minmax(420px,1.15fr)`), `max-width` ruimer, `gap`/`padding` genereuzer.
- **Paneel-chrome weg.** De `.paneel`-randen en de uppercase `h2.kop`-labels ("VOORTGANG", "GESPREK", "BEELD") lezen als software. Technisch: `.paneel` wordt borderloos/achtergrondloos met alleen witruimte als scheiding; de `.kop`-labels vervallen of worden vervangen door een zachte, kleine, niet-schreeuwende bijschrift-toon (lowercase, gedempt) — of verdwijnen geheel waar het beeld/gesprek voor zichzelf spreekt.
- **Focuspunt (spotlight).** Op elk moment heeft één ding de aandacht: de huidige vraag, óf de huidige onthulling. Technisch: een `focus`-toestand in de controller die niet-actieve secties licht dimt (`opacity`/`filter`) via een klasse `.gedempt`; de actieve sectie staat op volle helderheid. Geen nieuwe logica — puur een presentatie-klasse afgeleid van `fase()`.
- **Hiërarchie:** beeldwand (voert) › het huidige gesprek/onthulling (intiem) › de samenvatting (stil, terzijde) › de voortgang (fluistering, §6). Typografisch afgedwongen met schaal en kleur (`--text-strong` alleen voor het ene focuspunt).

## 2. Hero — de eerste indruk

- **Een landingstoestand vóór het canvas.** Een sectie `#hero` (nieuw in de markup, geen component: het is een presentatietoestand van dezelfde pagina) vult bij binnenkomst het scherm: een **groot, warm ruimtebeeld** met de vloer als hoofdrol, één kop, één subregel, en **één invoerveld** (hergebruik van `#invoer`, hier centraal geplaatst). Geen zichtbare knoppenbalk, geen `#apiKey`, geen "Start".
- **Kanteling naar de werkbank.** Zodra de architect de eerste zin verstuurt, krijgt `<body>` de klasse `.gestart`; `#hero` vervaagt/schaalt zacht weg (`opacity` + lichte `scale`, ~600–800 ms ease-in-out) en het werkende twee-paneel-canvas verschijnt in dezelfde beweging. Eén doorlopende ervaring, geen paginawissel.
- **Typografie:** de herokop groot en licht (font-weight 300, ruime `line-height`), rustig; de subregel klein en gedempt. Geen hoofdletters-als-UI.
- **CTA = het gesprek zelf.** Geen knop met "Ontwerp nu". De call-to-action is de placeholder-vraag in het veld (§8) + enter.
- **De sleutel is geen poort.** Het bestaande `#apiKey`-veld is bij binnenkomst **verborgen** (uit hero én header). Pas wanneer de backend bij de eerste beurt signaleert dat de sleutel nodig is (de bestaande "even uw sleutel"-begeleiding, §8), verschijnt het veld **terloops inline** in de werkbank, direct bij die zin — één keer, zacht, en daarna weg. Technisch: `#apiKey` start `hidden`; de controller onthult het bij de betreffende foutbegeleiding. Geen logica-wijziging.

## 3. Interactie-ritme — geen wizard, geen chat

- **Berichten verschijnen bedachtzaam.** Nieuwe `.bericht`-elementen komen op met een zachte fade + lichte stijging (`opacity 0→1`, `translateY 6px→0`, ~400 ms ease-out). Technisch: een klasse `.verschijnt` die de controller op het nieuwe element zet.
- **Een beat vóór het antwoord.** De reeds bestaande `.bezig`-indicator ("De Dessinator denkt met u mee…") blijft ~600–900 ms zichtbaar vóór het antwoord onthuld wordt — een *presentatie*-beat op reeds ontvangen inhoud (geen kunstmatige data, geen extra call). Dit geeft "overwogen", niet "traag".
- **Bevestigingen als een knik, niet een systeemstap.** De `#actie`-kaarten verschijnen als zachte onthulling (fade-in), niet als pop-up; de knoplabels zijn menselijk (§8).
- **Overgangen tussen fasen = focusverschuiving,** niet een schermwissel: de spotlight (§1) verplaatst zich naar de nieuwe onthulling.
- **Geen wizard/chat-signalen:** geen "volgende", geen stapnummers, geen avatars, geen tijdstempels, geen verzend-icoon. Het gesprek is een rustige dialoog, geen messenger.

## 4. Visuele onthulling (per stap: wanneer · waarom · animatie · timing)

| Stap | Wanneer (bestaande trigger) | Waarom (emotie) | Animatie | Timing |
|---|---|---|---|---|
| **Sfeer** | direct na de eerste beschreven zin (`renderViz`/beeldwand) | de ruimte "luistert" — vroeg wow | achtergrond cross-fade naar een op stemming gekozen sfeerbeeld | ~1,2 s |
| **Richting (concept)** | bij `concept` (bestaande `stalen`-render) | "dit wordt iets" | kleurcompositie fade-in, stijl als zacht bijschrift | ~800 ms |
| **Materiaal** | bij bevestigd materiaal | tastbaarheid | subtiele textuur-wash over de beeldwand, cross-fade | ~800 ms |
| **Dessin** | na `/svg` (bestaande `#viz img`) | "mijn dessin" | zachte schaal-in (`scale .985→1` + opacity) | ~700 ms |
| **Mockup** | na `/visualisatie` (bestaande `.mockup`) | "mijn vloer, in mijn ruimte" — het grote wow | het dessin "zakt" in de vloer (`.dessin-overlay` opacity 0→.92), langzaam | ~1 s |
| **DTP** | na `/transfer-package` (bestaande `#eind`) | trots + afronding | beeld vergroot, het ontwerpverhaal verschijnt rustig | ~900 ms |

De **stemming-gestuurde sfeerwissel** is uitsluitend **decoratief behang**, met een **harde grens**: een lichte client-side match van enkele vaste trefwoorden (bv. *rustig/warm/grafisch/organisch/natuurlijk*) op een **gecureerde, statische** beeldenset. Expliciet:
- het **interpreteert niets in de domein-zin** — het produceert geen `Interpretatie`, raakt geen laag, geen veld, geen profiel;
- het **voedt of seedt de dialoog/keten niet** — de door de gebruiker getypte tekst gaat onveranderd naar de bestaande dialoog-endpoint; de beeldkeuze staat daar volledig los van;
- het **roept geen endpoint aan** en wordt **niet bewaard**;
- als de sfeer van het decoratieve beeld en de echte, door de Context Interpreter afgeleide richting ooit "niet matchen", is dat irrelevant: de **echte** redenering bepaalt altijd het ontwerp; het beeld is enkel ambiance.
Zo blijft de interpretatie exclusief bij de Context Interpreter (BUILD-004/017) en de Design Brain volledig onaangeraakt.

## 5. Micro-interacties

- **Hover:** `.keuze`/kaarten lichten zacht op (rand warmt, minieme `translateY(-1px)`), ~150 ms.
- **Fades bij inhoudswissel:** in plaats van een harde innerHTML-vervanging krijgt elke onthulling een **cross-fade** (oud element `opacity→0`, dan swap, nieuw `opacity→1`), ~250–400 ms. Technisch: een kleine `vervang(el, html)`-hulp in de controller die de fade orkestreert; geen logica-wijziging. **Alleen daadwerkelijk gewijzigde secties animeren** — de controller vergelijkt de nieuwe HTML met de huidige en fade't uitsluitend bij een verschil, zodat ongewijzigde panelen niet flikkeren bij elke respons (de bestaande volledige-re-render blijft, maar zonder zichtbare flits op statische inhoud).
- **Focus:** het invoerveld krijgt bij focus een zachte gloed (border/box-shadow in `--green-dim`); de actieve sectie brightent terwijl de rest gedempt blijft (§1).
- **Scroll:** de pagina scrollt in principe niet (één canvas); alleen `#gesprek` scrollt, met `scroll-behavior:smooth`.
- **Stilte & vertraging:** bewuste lege beats (de "denkt mee"-pauze §3); de samenvattingsregels verschijnen **gestaffeld** (elk ~80 ms na de vorige) i.p.v. in één klap.

## 6. Voortgang — atelierwaardig, geen teller

BUILD-021 blijft leidend: **de zeven mijlpalen en bevestigingsmomenten blijven exact** (dezelfde `mijlpaalStatus()`/`fase()`-data). Alleen de **expressie** verandert:

- De huidige `#voortgang`-rij met zeven blokjes (leest als stap-tracker) vervalt als teller. In plaats daarvan een **fluistering**: één zachte, gedempte regel die het huidige hoofdstuk benoemt in mensentaal, afgeleid uit `fase()` — bv. *"We bepalen de sfeer…" → "We kiezen het materiaal…" → "We leggen uw vloer in de ruimte…"*. Geen cijfers, geen "Stap 3 van 7", geen balk die vult.
- Optioneel een uiterst subtiele, niet-tellende voortgangsindicatie (bv. een zacht oplichtende reeks stippen zonder getal), of het geheel opgaand in beeld en gesprek. Technisch: `renderVoortgang` levert deze fluistering i.p.v. de blokjesrij — zelfde bron, andere weergave.

## 7. Beelden

- **Herkomst zonder nieuwe backend:** statische assets onder `static/` (bv. `static/sfeer/*.jpg`) voor hero en inspiratie; de **echte** beelden (dessin, mockup) blijven uit de bestaande respons (`svg_resultaat`, `visualisatie.beeld`) en de bestaande Scene Builder-achtergronden.
- **Hero-wisselingen:** een trage cross-fade-cyclus (JS-interval, ~6–8 s, `opacity`-transitie ~1,2 s) tussen enkele gecureerde in-situ-beelden.
- **Licht & sfeer:** warme, ingetogen beelden, in het thema getrokken met een subtiele donker-groene gradient-overlay (`--bg` → transparant) zodat tekst leesbaar blijft en het beeld "atelier" aanvoelt.
- **Mockups:** voor het eigen ontwerp de bestaande FVE-`beeld`-render (BUILD-021); voor hero/inspiratie de gecureerde in-situ-foto's.

## 8. Microcopy — "Niet zomaar een vloer, een verhaal"

De **conversatieregels van de Dessinator komen uit de backend (de CP) en worden niet herschreven** — dat zou de Design Brain raken. De frontend-microcopy is uitsluitend de **omlijsting**: hero, bijschriften, knoplabels, wacht- en foutteksten.

| Plek | Copy (indicatief) |
|---|---|
| **Hero-kop** | *"Elke ruimte verdient een verhaal."* (vastgesteld — de vloer *maakt* het verhaal compleet, ís niet het verhaal) |
| **Hero-sub** | *"Vertel ons uw idee. Samen ontwerpen we een vloer die uw verhaal compleet maakt."* |
| **Eerste zin / placeholder** | *"Waar droomt deze ruimte van? Bijv. een rustige, warme lobby…"* |
| **Tussenzinnen (frame)** | zachte bijschriften bij onthullingen: *"Dit is de sfeer die uw woorden opriepen."* / *"Uw vloer, in uw ruimte."* |
| **Bevestigingen (knoppen)** | *"Ja, deze kant op"* · *"Dit klopt"* · *"Deze kies ik"* · *"Dit is 'm — geef door aan DCOD"* |
| **Wachtmomenten** | *"Ik denk met u mee…"* · *"Even schetsen…"* · *"We leggen het in de ruimte…"* |
| **Foutbegeleiding** | ontbrekende sleutel → *"Even uw sleutel, dan begrijp ik uw woorden echt."* · algemeen → *"Er ging even iets mis — zullen we het opnieuw proberen?"* (nooit een code/term) |
| **Eindscherm** | *"Het verhaal van deze ruimte, verteld in uw vloer — klaar voor DCOD."* |

Alle copy in de eerste persoon, warm, kort, zonder één technische term.

## 9. Animatieprincipes

- **Geen fancy effecten:** geen bounces, spins, parallax-excessen of confetti. Uitsluitend **opacity + kleine translate/scale**.
- **Rust & vertrouwen:** durations tussen ~150 ms (micro) en ~1200 ms (grote onthulling); `ease-out`/`ease-in-out`; één gedeeld timing-vocabulaire (CSS-variabelen `--t-snel/-midden/-traag`).
- **Ademruimte:** onthullingen krijgen lucht (nooit twee grote bewegingen tegelijk); stilte is onderdeel van het ritme.
- **Toegankelijkheid:** respecteer `@media (prefers-reduced-motion: reduce)` — dan vallen de bewegingen terug op eenvoudige, directe overgangen.

## 10. Niet doen (expliciet)

- **geen wizard** — geen stapnummers, geen "volgende", geen voortgangsbalk die telt;
- **geen AI-tool** — de woorden "AI", "genereren", "model", "prompt" komen nergens in beeld;
- **geen dashboard** — geen paneel-chrome, geen uppercase UI-labels, geen instellingenraster;
- **geen chat-app** — geen avatars, tijdstempels, verzend-iconen of "typing…"-messenger-signalen;
- **geen formulieren** — geen veldlabels, geen verplicht-markeringen; de sleutel is een terloops moment, geen poort;
- **geen technische termen** — geen laag, profiel, SVG, status, gate, endpoint, id;
- **geen statuscodes** — fouten worden proza (§8), nooit een code of signalering-string;
- **geen machinegevoel** — geen harde, directe innerHTML-flitsen; alles ademt en onthult.

---

## Consistentietoets (scope-bewaking)

- **Uitsluitend presentatie:** alleen `templates/ontwerp.html` en `static/js/ontwerp.js` (+ statische beeld-assets) worden aangeraakt; geen endpoint, component, businesslogica of Design Brain gewijzigd.
- **Gedrag identiek aan BUILD-021:** de `fase()`-machine, alle `/api/design-brain`-aanroepen, `gesprek_id`/localStorage, `api_key` in-memory, stale-veiligheid en de zeven mijlpalen blijven exact; alleen hun weergave/animatie/copy verandert (§6 verzoent dit expliciet).
- **BUILD-007-workflow onaangeroerd:** dezelfde keten en volgorde; de UX ondersteunt haar, vervangt niets.
- **Design Brain verborgen; §9-Ontwerpstudio-principe leidend:** elke keuze hierboven is getoetst aan *"studio of software?"*; de stemming-sfeerwissel is nadrukkelijk decoratief (geen redenering).
- **Slogan ondersteund:** de hele microcopy en onthullingsopbouw dragen *"Niet zomaar een vloer, een verhaal!"*.

---

**Reviewgereed:** dit TD legt uitsluitend de presentatielaag vast — ruimtelijke compositie, hero, ritme, onthullingen, micro-interacties, atelier-voortgang, beeldgebruik, microcopy, animatieprincipes en de niet-doen-lijst — volledig binnen de bestaande BUILD-021-frontend en zonder architectuur-, endpoint-, component- of Design Brain-wijziging. Klaar als basis voor een latere, strikt additieve implementatie (IMP-013).
