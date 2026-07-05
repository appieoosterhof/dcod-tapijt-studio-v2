#!/usr/bin/env python3
"""
Herstelt de 13 stijlknoppen die eerder vandaag uit het linker menu waren
verwijderd (Chevron Bold, Cirkels, Dots, Houndstooth, Knitwerk, Medaillon,
Mozaiek, Prism Overlay, Ruiten, Schubben, Sterren, Strepen, Terrazzo).
Voegt ze toe NA de bestaande 9 knoppen, mét hideSubmenus() zodat ze
consistent zijn met de andere knoppen van vandaag.

Regel-gebaseerde invoeging (zoekt de Vrije-vormen-knop als anker), dus
ongevoelig voor exacte witruimte elders in het bestand.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_restore_13_knoppen.py
Maakt automatisch een timestamped .bak van templates/index.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/index.html")

ANKER_REGEL = '''<button class="chip" onclick="hideSubmenus(); setPrompt('Vrije organische vormen, vloeiend en natuurlijk')">Vrije vormen</button>'''

HERSTELDE_KNOPPEN = [
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('chevronbold patroon, gevulde schuine plankjes, zwart wit')">Chevron Bold</button>''',
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('Alleen cirkels, strak en minimalistisch')">Cirkels</button>''',
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('Dots stippen patroon, polka dots')">Dots</button>''',
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('houndstooth patroon, hanenpoot pied-de-poule, zwart wit')">Houndstooth</button>''',
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('Scandinavisch knitwerk patroon, gebreide steken, zigzag banden in blauw en wit')">Knitwerk</button>''',
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('Medaillon geometrisch tegelmotief, donkerblauw en diep rood met gouden accenten')">Medaillon</button>''',
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('Pixel mozaiek patroon, kleurrijke blokken')">Mozaiek</button>''',
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('Prism overlay, prisma kleurmix met verrassende transparante kleurvlakken, levendig')">Prism Overlay</button>''',
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('Alleen ruiten en diamanten, geometrisch')">Ruiten</button>''',
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('Ogee schubben dakpan patroon')">Schubben</button>''',
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('Alleen sterren, strak patroon')">Sterren</button>''',
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('strepen patroon, style:strepen, verticale kleurstroken')">Strepen</button>''',
    '''<button class="chip" onclick="hideSubmenus(); setPrompt('Terrazzo patroon, gekleurde steensnippers op lichte ondergrond')">Terrazzo</button>''',
]


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    lines = TARGET.read_text(encoding="utf-8").splitlines(keepends=True)

    if any("Chevron Bold" in line for line in lines):
        print("FOUT: 'Chevron Bold' komt al voor. Lijkt al herstelt, stop om dubbele knoppen te voorkomen.")
        sys.exit(1)

    anker_indices = [i for i, line in enumerate(lines) if line.strip() == ANKER_REGEL]
    if len(anker_indices) == 0:
        print("FOUT: ankerregel (Vrije vormen-knop) niet exact gevonden.")
        sys.exit(1)
    if len(anker_indices) > 1:
        print(f"FOUT: ankerregel komt {len(anker_indices)}x voor, verwacht precies 1x. Stop voor de veiligheid.")
        sys.exit(1)

    idx = anker_indices[0]
    # Bepaal de inspringing van de ankerregel, gebruik die voor de nieuwe regels
    inspringing = lines[idx][:len(lines[idx]) - len(lines[idx].lstrip())]

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"index.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    nieuwe_regels = [inspringing + knop + "\n" for knop in HERSTELDE_KNOPPEN]
    nieuwe_lines = lines[:idx + 1] + nieuwe_regels + lines[idx + 1:]
    TARGET.write_text("".join(nieuwe_lines), encoding="utf-8")

    print(f"{len(HERSTELDE_KNOPPEN)} knoppen herstelt in het linker menu")
    print(f"Oude grootte: {backup.stat().st_size} bytes")
    print(f"Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "class=\\"chip\\"" templates/index.html')
    print('  grep -n "Chevron Bold\\|Terrazzo" templates/index.html')


if __name__ == "__main__":
    main()
