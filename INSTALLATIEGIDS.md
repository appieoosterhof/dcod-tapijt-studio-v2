# RepeatTile Studio — Installatiehandleiding voor Mac

## Wat u gaat doen (overzicht)

In 4 stappen heeft u de app werkend op uw Mac:

1. Python installeren (eenmalig, 5 min)
2. De app-bestanden op de juiste plek zetten (2 min)
3. Een API-sleutel aanmaken bij Anthropic (5 min)
4. De app starten en gebruiken

---

## Stap 1 — Python installeren

Python is de "motor" van de app. Dit is gratis software.

**1a.** Open de app **Terminal** op uw Mac.
U vindt Terminal via: Finder → Programma's → Hulpprogramma's → Terminal.
Of zoek op "Terminal" via Spotlight (⌘ + spatiebalk).

**1b.** Controleer of Python al aanwezig is. Typ dit in Terminal en druk op Enter:

```
python3 --version
```

- Als u iets ziet als `Python 3.10.x` of hoger: ga door naar Stap 2.
- Als u een foutmelding krijgt: ga naar stap 1c.

**1c.** Installeer Python via Homebrew. Typ achtereenvolgens:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Wacht tot dit klaar is (kan 5-10 minuten duren). Daarna:

```
brew install python3
```

**1d.** Installeer ook Cairo (nodig voor PNG-export op hoge resolutie):

```
brew install cairo
```

---

## Stap 2 — De app-bestanden installeren

**2a.** Download het bestand `tapijt-studio.zip` dat u van ons heeft ontvangen.

**2b.** Dubbelklik op het ZIP-bestand om het uit te pakken.
U krijgt een map genaamd `tapijt-studio`.

**2c.** Verplaats deze map naar uw Bureaublad of een andere handige plek.

**2d.** Open Terminal en navigeer naar de map. Als u de map op uw Bureaublad heeft gezet:

```
cd ~/Desktop/tapijt-studio
```

**2e.** Installeer de benodigde Python-pakketten (eenmalig):

```
pip3 install -r requirements.txt
```

Dit downloadt automatisch alles wat de app nodig heeft. Wacht tot het klaar is.

---

## Stap 3 — API-sleutel aanmaken

De API-sleutel geeft de app toegang tot Claude AI.

**3a.** Ga in uw browser naar: **https://console.anthropic.com**

**3b.** Maak een gratis account aan (of log in als u al een account heeft).

**3c.** Klik linksboven op **"API Keys"**.

**3d.** Klik op **"Create Key"**, geef de sleutel een naam (bijv. "TapijStudio") en klik op "Create".

**3e.** U ziet nu een lange code die begint met `sk-ant-...`
**Kopieer deze code en bewaar hem veilig** — u kunt hem later niet meer zien.

**Over de kosten:**
Het genereren van één dessin kost ongeveer €0,001 tot €0,003.
Voor duizend dessins betaalt u dus slechts €1-3.
U betaalt alleen voor wat u gebruikt, geen abonnement.

---

## Stap 4 — De app starten

**4a.** Open Terminal en ga naar de app-map:

```
cd ~/Desktop/tapijt-studio
```

**4b.** Start de app:

```
python3 app.py
```

U ziet nu:

```
═══════════════════════════════════════════════════════
  RepeatTile Studio — Tapijt Dessin Generator
═══════════════════════════════════════════════════════
  Open uw browser en ga naar: http://localhost:5000
  Druk op Ctrl+C om te stoppen.
═══════════════════════════════════════════════════════
```

**4c.** Open uw browser (Safari, Chrome of Firefox) en ga naar:

```
http://localhost:5000
```

De app opent. U kunt nu aan de slag!

---

## De app gebruiken

**API-sleutel invullen:**
Plak uw API-sleutel in het veld bovenaan. Vink "Onthoud op dit apparaat" aan zodat u dit niet elke keer opnieuw hoeft te doen.

**Een dessin genereren:**
1. Klik op een van de voorbeeldknoppen (Marokkaans, Nordic, etc.) of typ uw eigen beschrijving
2. Kies tegelmaat, repeat-type en resolutie
3. Klik op "Genereer dessin"
4. Na 5-15 seconden verschijnt uw dessin

**Repeat types uitgelegd:**
- **Full repeat** — de tegel herhaalt precies, rechttoe rechtaan
- **Half-drop** — elke rij is een halve tegel naar beneden verschoven (klassiek tapijt)
- **Brick offset** — elke rij is een halve tegel naar rechts verschoven
- **Mirror** — de tegel wordt gespiegeld bij elke herhaling — geeft een rustig, symmetrisch effect

**Exporteren:**
- **SVG vector** — kiest u voor grote formaten; perfect schaalbaar zonder kwaliteitsverlies
- **PNG** — voor gebruik in andere software; resolutie naar keuze (150-300 DPI)

---

## De app elke volgende keer starten

U hoeft Stap 1, 2 en 3 maar één keer te doen.

Daarna alleen:
1. Open Terminal
2. Typ: `cd ~/Desktop/tapijt-studio`
3. Typ: `python3 app.py`
4. Ga naar `http://localhost:5000` in uw browser

---

## Iets gaat fout?

**"command not found: python3"**
→ Herhaal stap 1c en 1d.

**"No module named flask"**
→ Voer opnieuw uit: `pip3 install -r requirements.txt`

**De browser toont een lege pagina of foutmelding**
→ Controleer of Terminal nog actief is en het commando `python3 app.py` draait.

**"Invalid API key"**
→ Controleer of u de sleutel correct heeft geplakt (geen spaties voor of na de sleutel).

---

## Contact & ondersteuning

Bewaar dit document. Bij vragen kunt u dit document laten zien aan een technische medewerker of opnieuw naar Claude vragen voor hulp.
