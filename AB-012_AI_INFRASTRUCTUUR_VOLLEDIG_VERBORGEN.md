# AB-012 — AI-infrastructuur volledig verborgen

**Status:** vastgesteld architectuurbesluit.

> **Nummering:** dit besluit is door de architect aangeleverd onder de titel "AB-010". Omdat `AB-010` (Material Profile T6/T10) en `AB-011` (Pattern Profile) al bestaan, is het genummerd **AB-012** om botsing te vermijden. De inhoud en het gezag zijn ongewijzigd.

## Doel

De gebruiker ontwerpt **met DCOD**, niet met een AI-platform. Alle technische AI-infrastructuur is daarom volledig onzichtbaar binnen de gebruikerservaring. De Dessinator wordt altijd ervaren als de digitale ontwerpstudio van DCOD, nooit als een AI-tool.

## Architectuurprincipe

De volledige AI-infrastructuur behoort tot de technische infrastructuur van DCOD en maakt **geen onderdeel uit van de gebruikerservaring**. De frontend kent uitsluitend de ontwerpdialoog. Alle configuratie, authenticatie en modelkeuzes zijn serververantwoordelijkheid.

## Voor de gebruiker

De gebruiker ziet **nooit**: API-sleutels, providernamen (Anthropic/OpenAI/…), modelnamen, prompts, tokens, temperatuur-/AI-configuratie, technische foutcodes of infrastructuurinstellingen. De gebruiker ervaart uitsluitend: **hij ontwerpt samen met DCOD.**

## Productiemodus

- API-sleutels worden **uitsluitend server-side** beheerd;
- AI-configuraties worden uitsluitend server-side geladen;
- de frontend bevat **geen** API-sleutelveld, modelkeuze, AI-configuratie of technische infrastructuur;
- de frontend weet uitsluitend welke endpoint moet worden aangeroepen.

## Ontwikkelmodus (intern DCOD)

Een interne beheeromgeving mag AI-provider, sleutels, modelkeuze, test, logging en diagnostiek instellen. Die omgeving is **geen onderdeel van de Dessinator**.

## Foutafhandeling

Is de AI-infrastructuur tijdelijk niet beschikbaar, dan ontvangt de gebruiker uitsluitend een mensvriendelijke melding:

> "Onze ontwerpstudio is momenteel niet beschikbaar. Probeert u het later nogmaals of neem contact op met DCOD."

Technische details worden **nooit** getoond.

## Gevolgen voor BUILD-021 / BUILD-022

Dit besluit **vervangt** alle eerdere UX-ontwerpen waarin de gebruiker zelf een API-sleutel kon invoeren. Voortaan: geen API-sleutelveld, geen verborgen veld, geen uitgestelde sleutelvraag, geen microcopy over sleutels, geen interactie rondom AI-configuratie. Alle verwijzingen worden uit de frontend verwijderd. Dit ondersteunt rechtstreeks BUILD-022 §9 (Ontwerpstudio-principe).

## Implementatie-impact (in deze codebase)

Raakt uitsluitend serverconfiguratie/ontsluiting; **Design Brain, BUILD-007-workflow, componentarchitectuur en UX-flow blijven ongewijzigd:**

- **Integratielaag (`design_brain_api.py`):** de dialoog-endpoint haalt de AI-sleutel voortaan uit **serverconfiguratie** — omgevingsvariabele (`ANTHROPIC_API_KEY`/`DCOD_AI_KEY`) met terugval op het reeds bestaande, gitignored `api_key.txt` — en injecteert die in de bestaande Context Interpreter. De sleutel wordt **niet** meer uit de request gelezen. Bij ontbrekende sleutel of een mislukte AI-aanroep retourneert het endpoint een neutrale "onbeschikbaar"-status **zonder technische details**.
- **Frontend (`templates/ontwerp.html` + `static/js/ontwerp.js`):** alle API-sleutel-UI, -microcopy en -interactie zijn verwijderd; de frontend stuurt geen sleutel meer mee; de "onbeschikbaar"-status wordt getoond als de mensvriendelijke studio-melding hierboven.
- De **Context Interpreter** (BUILD-004) en de overige Design Brain-componenten blijven ongewijzigd (zij ontvangen de sleutel nog steeds als parameter; alleen de *bron* is nu serverconfig).

## Ontwerpregel (permanente toets)

Bij iedere toekomstige implementatie: **"Ziet de gebruiker iets van de AI-infrastructuur?"** Zo ja → afgewezen. De enige zichtbare gesprekspartner blijft **DCOD.**
