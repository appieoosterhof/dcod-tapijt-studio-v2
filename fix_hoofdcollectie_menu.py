#!/usr/bin/env python3
"""
Reduceert het linker stijlmenu ("Kies een ontwerprichting") in templates/index.html
naar de 10 vastgestelde hoofdconcepten:
  Neo Deco, Neo Bauhaus, Urban Plaid, Aardlagen, Hoogtelijnen, Japandi,
  Weefstructuren (= Urban Plaid, geen aparte knop), Lijnenspel, Botanisch, Vrije vormen

Acties:
- Hernoemt 'Art Deco' -> 'Neo Deco' (subvarianten Waaier/Zonnestralen/Honingraat blijven)
- Hernoemt 'Bauhaus' -> 'Neo Bauhaus'
- Verwijdert: Chevron Bold, Cirkels, Dots, Houndstooth, Knitwerk, Medaillon,
  Mozaiek, Prism Overlay, Ruiten, Schubben, Sterren, Strepen, Terrazzo

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_hoofdcollectie_menu.py
Maakt automatisch een timestamped .bak van templates/index.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/index.html")

# (label, exacte regel, actie: 'verwijderen' of 'label_vervangen')
HERNOEMINGEN = [
    (
        "Art Deco -> Neo Deco",
        '''<button class="chip" onclick="setPrompt('Art Deco hexagon, goud en zwart, jaren 20 stijl'); showArtdecoSub()">Art Deco</button>''',
        '''<button class="chip" onclick="setPrompt('Art Deco hexagon, goud en zwart, jaren 20 stijl'); showArtdecoSub()">Neo Deco</button>''',
    ),
    (
        "Bauhaus -> Neo Bauhaus",
        '''<button class="chip" onclick="setPrompt('Bauhaus geometrisch patroon, halve cirkels driehoeken en ringen, oranje zwart grijs')">Bauhaus</button>''',
        '''<button class="chip" onclick="setPrompt('Bauhaus geometrisch patroon, halve cirkels driehoeken en ringen, oranje zwart grijs')">Neo Bauhaus</button>''',
    ),
]

TE_VERWIJDEREN = [
    ("Chevron Bold", '''<button class="chip" onclick="setPrompt('chevronbold patroon, gevulde schuine plankjes, zwart wit')">Chevron Bold</button>'''),
    ("Cirkels", '''<button class="chip" onclick="setPrompt('Alleen cirkels, strak en minimalistisch')">Cirkels</button>'''),
    ("Dots", '''<button class="chip" onclick="setPrompt('Dots stippen patroon, polka dots')">Dots</button>'''),
    ("Houndstooth", '''<button class="chip" onclick="setPrompt('houndstooth patroon, hanenpoot pied-de-poule, zwart wit')">Houndstooth</button>'''),
    ("Knitwerk", '''<button class="chip" onclick="setPrompt('Scandinavisch knitwerk patroon, gebreide steken, zigzag banden in blauw en wit')">Knitwerk</button>'''),
    ("Medaillon", '''<button class="chip" onclick="setPrompt('Medaillon geometrisch tegelmotief, donkerblauw en diep rood met gouden accenten')">Medaillon</button>'''),
    ("Mozaiek", '''<button class="chip" onclick="setPrompt('Pixel mozaiek patroon, kleurrijke blokken')">Mozaiek</button>'''),
    ("Prism Overlay", '''<button class="chip" onclick="setPrompt('Prism overlay, prisma kleurmix met verrassende transparante kleurvlakken, levendig')">Prism Overlay</button>'''),
    ("Ruiten", '''<button class="chip" onclick="setPrompt('Alleen ruiten en diamanten, geometrisch')">Ruiten</button>'''),
    ("Schubben", '''<button class="chip" onclick="setPrompt('Ogee schubben dakpan patroon')">Schubben</button>'''),
    ("Sterren", '''<button class="chip" onclick="setPrompt('Alleen sterren, strak patroon')">Sterren</button>'''),
    ("Strepen", '''<button class="chip" onclick="setPrompt('strepen patroon, style:strepen, verticale kleurstroken')">Strepen</button>'''),
    ("Terrazzo", '''<button class="chip" onclick="setPrompt('Terrazzo patroon, gekleurde steensnippers op lichte ondergrond')">Terrazzo</button>'''),
]


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    # Voorcontrole: alles moet precies 1x voorkomen
    problemen = []
    for label, oud, nieuw in HERNOEMINGEN:
        n = content.count(oud)
        if n != 1:
            problemen.append(f"{label}: {n}x gevonden, verwacht 1x")
    for label, regel in TE_VERWIJDEREN:
        n = content.count(regel)
        if n != 1:
            problemen.append(f"{label}: {n}x gevonden, verwacht 1x")

    if problemen:
        print("FOUT: onverwachte inhoud gevonden, stop voor de veiligheid:")
        for p in problemen:
            print(f"  - {p}")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"index.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    nieuwe_content = content
    for label, oud, nieuw in HERNOEMINGEN:
        nieuwe_content = nieuwe_content.replace(oud, nieuw)
        print(f"Hernoemd: {label}")
    for label, regel in TE_VERWIJDEREN:
        nieuwe_content = nieuwe_content.replace(regel, "")
        print(f"Verwijderd: {label}")

    TARGET.write_text(nieuwe_content, encoding="utf-8")
    print(f"Oude grootte: {backup.stat().st_size} bytes")
    print(f"Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "class=\\"chip\\"" templates/index.html')
    print('  grep -n "Neo Deco\\|Neo Bauhaus" templates/index.html')


if __name__ == "__main__":
    main()
