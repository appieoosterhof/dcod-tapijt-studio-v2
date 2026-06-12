#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_knitwerk_stap1_app.py
-------------------------
STAP 1 van 2: past app.py aan.

Wat dit doet:
  1) Vervangt generate_nordic_svg door generate_knitwerk_svg (Fair Isle knitwerk,
     V-vormige steken, naadloos: cells deelt 400 exact, bandperiode 5 deelt rows).
  2) Verwijdert generate_abstract_svg (niet meer nodig).
  3) Werkt STYLE_GENERATORS bij: 'nordic' en 'abstract' eruit, 'knitwerk' erin.
  4) Routing in het generate-blok: de nordic-regel wordt een knitwerk-regel met
     ruimere keywords (knit, gebreid, fair isle, noorse trui, nordic, scandinavisch...).
  5) label_map: nordic-regel -> knitwerk; abstract-regel verwijderd.

STAP 2 (apart script) past templates/index.html aan (knoppen + cache-buster).

Veiligheid:
  - Maakt eerst backup app.py.bak_JJJJMMDD_UUMMSS
  - Vervangt alleen EXACT gematchte blokken; niet-gevonden blokken worden
    overgeslagen en gemeld. Niets wordt half aangepast.

Gebruik:
  1) Stop Flask (Ctrl+C)
  2) cd ~/Desktop/tapijt-studio
  3) python3 fix_knitwerk_stap1_app.py
"""

import os
import sys
import shutil
from datetime import datetime

APP = "app.py"

# De nieuwe generator-functie (vervangt generate_nordic_svg volledig)
NEW_GEN = '''def generate_knitwerk_svg(palette: dict, tile_size: int, complexity: str) -> str:
    T = tile_size
    bg = palette["background"]
    c1 = palette["primary"]
    c2 = palette["secondary"]
    c3 = palette["accent1"]
    c4 = palette["accent2"]
    shapes = []
    # cells MOET T exact opdelen voor naadloze wrap (delers van 400: 20, 25).
    cells = {"low": 20, "medium": 25, "high": 25}.get(complexity, 25)
    step = T / cells
    rows = cells
    cmap = {1: c1, 2: c2, 3: c3, 4: c4}
    shapes.append(f'<rect x="0" y="0" width="{T}" height="{T}" fill="{bg}"/>')
    # Banden met periode 5 (deelt rows=25 exact -> naadloos verticaal).
    #  sub 0: dikke kleurband (wisselt c1/c2 per blok)
    #  sub 1: stippellijn c3
    #  sub 2: diamant-centrum (c2) met armen (c4)
    #  sub 3: diamant-buitenpunten (c2)
    #  sub 4: achtergrond
    grid = [[0] * cells for _ in range(rows)]
    for r in range(rows):
        block = r // 5
        sub = r % 5
        bandcol = 1 if block % 2 == 0 else 2
        if sub == 0:
            for c in range(cells):
                grid[r][c] = bandcol
        elif sub == 1:
            for c in range(cells):
                grid[r][c] = 3 if c % 2 == 0 else 0
        elif sub == 2:
            for c in range(cells):
                if c % 5 == 2:
                    grid[r][c] = 2
                elif c % 5 in (1, 3):
                    grid[r][c] = 4
        elif sub == 3:
            for c in range(cells):
                if c % 5 in (0, 4):
                    grid[r][c] = 2
    for r in range(rows):
        for c in range(cells):
            col = grid[r][c]
            if col == 0:
                continue
            fill = cmap[col]
            x = c * step
            y = r * step
            cxm = x + step / 2
            shapes.append(
                f'<path d="M {x:.2f} {y:.2f} '
                f'L {cxm:.2f} {y+step*0.55:.2f} '
                f'L {x+step:.2f} {y:.2f} '
                f'L {x+step:.2f} {y+step*0.45:.2f} '
                f'L {cxm:.2f} {y+step:.2f} '
                f'L {x:.2f} {y+step*0.45:.2f} Z" fill="{fill}"/>'
            )
    return "\\n".join(shapes)'''


def main():
    if not os.path.exists(APP):
        print(f"FOUT: {APP} niet gevonden. Ga eerst naar: cd ~/Desktop/tapijt-studio")
        sys.exit(1)

    with open(APP, "r", encoding="utf-8") as f:
        src = f.read()

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = f"{APP}.bak_{stamp}"
    shutil.copy2(APP, backup)
    print(f"Backup gemaakt: {backup}")

    changes = 0

    # ---- 1. Vervang generate_nordic_svg volledig door generate_knitwerk_svg ----
    # We zoeken vanaf 'def generate_nordic_svg' tot net voor 'def generate_abstract_svg'.
    start_marker = "def generate_nordic_svg(palette: dict, tile_size: int, complexity: str) -> str:"
    end_marker = "def generate_abstract_svg(palette: dict, tile_size: int, complexity: str) -> str:"
    si = src.find(start_marker)
    ei = src.find(end_marker)
    if si != -1 and ei != -1 and ei > si:
        old_block = src[si:ei]
        src = src[:si] + NEW_GEN + "\n\n\n" + src[ei:]
        changes += 1
        print("OK  - generate_nordic_svg vervangen door generate_knitwerk_svg.")
    else:
        print("OVERGESLAGEN - kon generate_nordic_svg blok niet afbakenen.")

    # ---- 2. Verwijder generate_abstract_svg volledig ----
    # Van 'def generate_abstract_svg' tot net voor de eerstvolgende top-level regel
    # 'STYLE_GENERATORS = {'.
    start_a = "def generate_abstract_svg(palette: dict, tile_size: int, complexity: str) -> str:"
    end_a = "STYLE_GENERATORS = {"
    sa = src.find(start_a)
    ea = src.find(end_a)
    if sa != -1 and ea != -1 and ea > sa:
        src = src[:sa] + src[ea:]
        changes += 1
        print("OK  - generate_abstract_svg verwijderd.")
    else:
        print("OVERGESLAGEN - kon generate_abstract_svg blok niet afbakenen.")

    # ---- 3. STYLE_GENERATORS: nordic -> knitwerk, abstract-regel verwijderen ----
    if '    "nordic": generate_nordic_svg,' in src:
        src = src.replace('    "nordic": generate_nordic_svg,',
                          '    "knitwerk": generate_knitwerk_svg,')
        changes += 1
        print("OK  - STYLE_GENERATORS: nordic -> knitwerk.")
    else:
        print("OVERGESLAGEN - STYLE_GENERATORS nordic-regel niet gevonden.")

    if '    "abstract": generate_abstract_svg,\n' in src:
        src = src.replace('    "abstract": generate_abstract_svg,\n', '')
        changes += 1
        print("OK  - STYLE_GENERATORS: abstract-regel verwijderd.")
    else:
        print("OVERGESLAGEN - STYLE_GENERATORS abstract-regel niet gevonden (mogelijk al weg).")

    # ---- 4. Routing in generate-blok: nordic-regel -> knitwerk met ruimere keywords ----
    old_route = ("        elif any(w in p for w in ['nordic', 'scandinavisch', 'noors', 'sneeuwvlok']):\n"
                 "            analysis['style'] = 'nordic'\n")
    new_route = ("        elif any(w in p for w in ['knitwerk', 'knit', 'gebreid', 'breiwerk', "
                 "'fair isle', 'noorse trui', 'nordic', 'scandinavisch', 'noors', 'sneeuwvlok']):\n"
                 "            analysis['style'] = 'knitwerk'\n")
    if old_route in src:
        src = src.replace(old_route, new_route)
        changes += 1
        print("OK  - routing generate-blok: nordic -> knitwerk.")
    else:
        print("OVERGESLAGEN - routing nordic-regel in generate-blok niet exact gevonden.")

    # ---- 5. label_map: nordic-regel -> knitwerk, abstract-regel verwijderen ----
    if "            (['nordic', 'scandinavisch', 'noors'], 'nordic'),\n" in src:
        src = src.replace(
            "            (['nordic', 'scandinavisch', 'noors'], 'nordic'),\n",
            "            (['knitwerk', 'knit', 'gebreid', 'breiwerk', 'fair isle', 'noorse trui', 'nordic', 'scandinavisch', 'noors'], 'knitwerk'),\n")
        changes += 1
        print("OK  - label_map: nordic -> knitwerk.")
    else:
        print("OVERGESLAGEN - label_map nordic-regel niet gevonden.")

    if "            (['abstract'], 'abstract'),\n" in src:
        src = src.replace("            (['abstract'], 'abstract'),\n", "")
        changes += 1
        print("OK  - label_map: abstract-regel verwijderd.")
    else:
        print("OVERGESLAGEN - label_map abstract-regel niet gevonden (mogelijk al weg).")

    if changes == 0:
        print("\nGEEN wijzigingen doorgevoerd. app.py ongewijzigd.")
        sys.exit(0)

    with open(APP, "w", encoding="utf-8") as f:
        f.write(src)

    print(f"\nKLAAR: {changes} aanpassing(en) opgeslagen in {APP}.")
    print("Controleer met:  python3 -c \"import app\"   (mag geen fout geven)")
    print(f"Terugzetten kan met:  cp {backup} {APP}")


if __name__ == "__main__":
    main()
