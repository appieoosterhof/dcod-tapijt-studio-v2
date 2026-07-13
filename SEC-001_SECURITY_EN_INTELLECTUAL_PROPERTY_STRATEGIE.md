# SEC-001 — Security & Intellectual Property Strategie

**Status:** strategisch governance-document. Legt de Security & Intellectual Property-strategie van het Studio Platform vast: bescherming van broncode, architectuur, Design Brain, kennis, datasets, documentatie en bedrijfscontinuïteit. **Geen code-, architectuur- of capability-wijziging.** SEC-001 introduceert geen nieuwe architectuur; het duidt bestaande keuzes als beveiligingskeuzes en legt het governancekader vast vóór verdere uitbreiding.

**Aard:** richtinggevend governancekader. Onderscheid tussen **[Geborgd]** (in deze codebase geverifieerd) en **[Aanbevolen]** (beleid/roadmap dat DCOD nog moet bevestigen of inrichten). Waar SEC-001 en een bestaand architectuurbesluit elkaar zouden lijken te raken, blijft het bestaande besluit leidend.

**Bindend / respecteert:** AB-006, AB-009, AB-012, BUILD-007, BUILD-023, IMP-014, BUILD-024, PLATFORM-001, PLATFORM-002, REASONING-001.

---

## 1. Security by Architecture

Verschillende reeds bekrachtigde architectuurkeuzes zijn tegelijk beveiligingsmaatregelen:

- **Server-side reasoning [Geborgd]** — alle AI-aanroepen lopen server-side; de frontend roept nooit een AI-provider aan (AB-012). De browser krijgt geen sleutel, model of provider te zien.
- **Server-side geheimen [Geborgd]** — de AI-sleutel komt uitsluitend uit serverconfiguratie (`_ai_sleutel()`: env `ANTHROPIC_API_KEY`/`DCOD_AI_KEY`, of het gitignorede `api_key.txt` voor dev). `api_key.txt` staat in `.gitignore`, is niet getrackt en komt niet in de git-historie voor (geverifieerd).
- **Capability-isolatie [Geborgd]** — een Reasoning Capability kent geen HTTP, opslag, sessies, DesignContext of orchestratie; zij ontvangt platte invoer en levert een contract-resultaat (IMP-015/016).
- **Boundary-isolatie [Geborgd]** — boundaries zijn pure functies (`Callable[[dict], …]`); geen toegang tot andere lagen, geen impliciete afhankelijkheden (BUILD-024 §5).
- **Contractgebaseerde communicatie [Geborgd]** — componenten wisselen uitsluitend gecontracteerde platte waarden uit; nooit objecten, herkomst-identifiers of de AI-sleutel (BUILD-024 §1).
- **AI-provider-onafhankelijkheid [Geborgd]** — uitsluitend de `AnthropicModelClient`-adapter raakt de leverancier; capabilities kennen enkel de abstracte `ModelClient` (reasoning_client.py).
- **Onzichtbare degradatie [Geborgd]** — bij een productiefout valt de keten terug op de deterministische placeholder en toont nooit model, sleutel, foutcode of technische melding (AB-012 / BUILD-023 R5).

## 2. Intellectueel Eigendom

**Auteurschap / initiatief:** de heer A. Oosterhof (zie §2.1). **Formeel eigendom / IP-rechten:** conform de overeenkomsten tussen A. Oosterhof en DCOD Printtapijt en de toepasselijke wet- en regelgeving; [Aanbevolen] leg dit schriftelijk vast. De onderstaande classificatie betreft opslaglocatie en beschermingsniveau, ongeacht de formele eigendomsverdeling.

### 2.1 Auteurschap

Het oorspronkelijke concept, de architectuurvisie, de ontwerpfilosofie en de functionele uitwerking van de **Dessinator** zijn ontwikkeld onder verantwoordelijkheid van **de heer A. Oosterhof**.

Binnen de governance van het Studio Platform wordt de heer A. Oosterhof aangemerkt als de **oorspronkelijke ontwerper en initiatiefnemer** van de Dessinator en de daaraan ten grondslag liggende ontwerpfilosofie, platformvisie en Design Brain-architectuur.

Alle architectuurdocumenten, ontwerpprincipes, Design Brain-concepten, redeneerstructuren, workflows en overige intellectuele uitwerkingen worden beheerd en beschermd conform de in dit document (SEC-001) vastgelegde Security & Intellectual Property Strategie.

Indien intellectuele eigendomsrechten, auteursrechten of andere juridische rechten formeel worden vastgelegd, geregistreerd of overgedragen, prevaleren de daarvoor opgestelde overeenkomsten en de toepasselijke wet- en regelgeving. **Persoonsgegevens ter juridische identificatie (zoals geboortedatum en -plaats) worden bewust niet in deze repository opgenomen, maar uitsluitend vastgelegd in een aparte, niet-openbare overeenkomst** — conform §4 (geen persoonsgegevens/geheimen in de repo).

| Categorie | Beschermingsniveau | Opslaglocatie | Back-up |
|---|---|---|---|
| Broncode | Bedrijfskritisch / vertrouwelijk | GitHub-repo (`origin`); [Aanbevolen] privé + beperkte toegang | Git-gedistribueerd (GitHub + lokale clones); [Aanbevolen] derde kopie buiten GitHub |
| Architectuurdocumenten (AB/BUILD/PLATFORM) | Vertrouwelijk | Repo (versiebeheerd) | idem |
| Ontwerpfilosofie (REASONING-001) | Bedrijfskritisch (kern-IP) | Repo | idem |
| Capabilities + prompts | Bedrijfskritisch | Repo, server-side | idem |
| Validaties (VAL-001/002) | Intern | Repo | idem |
| Datasets / trend-/materiaal-/productiebibliotheken | Vertrouwelijk | Repo / server | idem; [Aanbevolen] aparte, geversioneerde opslag |
| Mockups / beeldmateriaal | Intern | Repo / `static/` | idem |
| Design Brain (geheel) | Bedrijfskritisch | Repo, server-side | idem |

## 3. Repository Governance

- **Branchbeleid [Geborgd]** — `main` = live (Render auto-deploy); `preview` = integratie/staging. Nieuwe wijzigingen landen op `preview`, nooit rechtstreeks op `main`.
- **Protected branches [Aanbevolen]** — schakel branch-protection in op `main` (en bij voorkeur `preview`): geen force-push, vereis review vóór merge naar `main`.
- **Code reviews [Geborgd, procesmatig]** — elke wijziging doorloopt VR/TR/CR (functioneel/technisch/code-review) vóór commit; dit is de vaste werkwijze van dit programma.
- **Releasebeleid [Geborgd]** — pushen uitsluitend op expliciete autorisatie; promotie naar `main` (en dus live) is een bewuste, aparte handeling. `DCOD_REASONING_MODUS` wordt pas op productie gezet wanneer DCOD dat bewust besluit.
- **Versiebeheer [Geborgd]** — git; één logische commit per besluit, met co-author-trailer.
- **Toegangsrechten [Aanbevolen]** — beperk repo- en Render-toegang tot een kleine, benoemde groep; verleen minimale rechten (least privilege).

## 4. Geheimenbeheer

- **Opslag van API-sleutels [Geborgd/Aanbevolen]** — productie: env-variabele op Render (`ANTHROPIC_API_KEY`/`DCOD_AI_KEY`); dev: gitignored `api_key.txt`. **Nooit** in broncode, documentatie, frontend of prompts (geverifieerd voor `api_key.txt`).
- **Configuratiegeheimen [Aanbevolen]** — uitsluitend via omgevingsvariabelen; niet in de repo.
- **Rotatiebeleid [Aanbevolen]** — roteer sleutels periodiek en direct bij (vermoedelijke) blootstelling; de architectuur (één sleutelbron) maakt rotatie triviaal.
- **Toegangsbeheer [Aanbevolen]** — beperk wie de Render-omgevingsvariabelen kan inzien/wijzigen.
- **Auditbeleid [Aanbevolen]** — houd bij wie toegang heeft en wanneer sleutels zijn geroteerd.

## 5. Kennisbescherming

De kern-IP van DCOD is niet de AI-provider, maar de **ontwerpkennis**: de ontwerpfilosofie (REASONING-001), de redeneerpatronen (de prompts/normalisatie in de capability-modules), de capabilitykennis, de validatiecases, en de trend-/materiaal-/productiebibliotheken. Deze worden beschermd doordat zij:

- **server-side** leven en nooit naar de frontend worden verzonden (AB-012);
- in de **centrale repository** staan ([Aanbevolen] privé, met beperkte toegang);
- via **contract-isolatie** niet uit de resultaatobjecten zijn te reconstrueren (afnemers krijgen alleen gecontracteerde velden; motiveringen zijn vrije tekst, geen bloot­gelegde redeneerlogica);
- **provider-onafhankelijk** zijn vastgelegd, zodat de kennis niet aan een leverancier is gebonden.

[Aanbevolen] Behandel prompts en bibliotheken expliciet als vertrouwelijke bedrijfsmiddelen; deel ze niet buiten de repo.

## 6. Continuïteit

- **Back-up [Geborgd/Aanbevolen]** — git is gedistribueerd: `origin` (GitHub) + elke lokale clone zijn volwaardige kopieën. [Aanbevolen] richt een derde, onafhankelijke back-up in (buiten GitHub).
- **Herstelstrategie [Geborgd]** — volledige repo-herstel via `git clone` van `origin`; de gehele geschiedenis en documentatie komen mee.
- **Documentatiebeheer [Geborgd]** — elk besluit is als document in de repo vastgelegd; de architectuur is daarmee reconstrueerbaar zonder mondelinge overdracht.
- **Sleutelbeheer [Aanbevolen]** — leg de locatie en rotatie van sleutels vast in een korte runbook; bewaar sleutels buiten de repo.
- **Overdraagbaarheid [Geborgd/Aanbevolen]** — de provider-onafhankelijke, gedocumenteerde architectuur maakt overdracht mogelijk; [Aanbevolen] een korte deploy-/runbook voor Render.
- **Kennisborging & bus-factor [Aanbevolen]** — het platform steunt nu op één ontwikkelaar (Ab). De uitgebreide, gecommitte documentatie is de belangrijkste mitigatie; [Aanbevolen] DCOD zorgt dat minstens één tweede partij repo- en Render-toegang heeft en de runbook kent, zodat het platform niet van één persoon afhankelijk is.

## 7. Leveranciersonafhankelijkheid

Vastgelegd en geborgd (BUILD-024 §5, PLATFORM-001 §5, REASONING-001 §7, IMP-015/016):

- **AI-providers blijven vervangbaar** — een andere provider, meerdere providers, een regelsysteem of een hybride oplossing vergt uitsluitend een nieuwe `ModelClient`-adapter.
- **Capabilities blijven leverancier-onafhankelijk** — zij kennen alleen de abstracte interface.
- **Workflows blijven ongewijzigd** — de Design Workflow en ketenvolgorde zijn provider-agnostisch.
- **Contracten blijven ongewijzigd** — de boundary-contracten zijn additief en model-onafhankelijk.

## 8. Roadmap — beveiliging per releasefase

| Vóór… | Verplicht afgerond |
|---|---|
| **Interne pilot** | Sleutels uitsluitend via Render-env (niet `api_key.txt` op prod); privé-repo bevestigd; branch-protection op `main`; tweede persoon met repo-/Render-toegang; korte deploy-runbook. |
| **Externe pilot** | Duurzame opslag van `Gesprekstoestand` (nu efemeer op Render); rate limiting / misbruikbescherming op de publieke endpoints; sleutelrotatie uitgevoerd; back-up buiten GitHub; basale logging/audit; AVG-check op opgeslagen gespreksdata. |
| **Publieke release** | Onafhankelijke security-review/pentest; DoS-/misbruikmitigatie; incident-responsplan; monitoring en alerting; formele IP-vastlegging; volledige AVG-conformiteit. |

---

## Consistentietoets

- **AB-012:** server-side reasoning, verborgen sleutel en onzichtbare degradatie zijn als beveiligingsmaatregelen geduid; niets in SEC-001 maakt AI/sleutel/techniek zichtbaar.
- **BUILD-023 / IMP-014:** de orkestratie-/reuse-laag blijft ongewijzigd; SEC-001 raakt geen code of guard.
- **BUILD-024:** contract-isolatie en additieve, provider-onafhankelijke contracten zijn de dragers van kennis- en leveranciersbescherming.
- **PLATFORM-001 / PLATFORM-002:** capability-/Experience Layer-scheiding en de verborgen AI sluiten aan op de IP- en kennisbescherming.
- **REASONING-001:** de ontwerpfilosofie is als kern-IP geclassificeerd en server-side beschermd.
- **Eerlijkheid:** [Aanbevolen]-punten zijn expliciet gemarkeerd als nog in te richten beleid, niet als bestaande controles.

---

**Reviewgereed:** dit document legt de Security & Intellectual Property-strategie vast — security by architecture, IP-classificatie en eigendom, repository governance, geheimenbeheer, kennisbescherming, continuïteit, leveranciersonafhankelijkheid en een releasegefaseerde beveiligingsroadmap — met een expliciet onderscheid tussen reeds geborgde en nog in te richten maatregelen, zonder enige code-, architectuur- of capability-wijziging en zonder afwijking van de bestaande, leidende architectuur.
