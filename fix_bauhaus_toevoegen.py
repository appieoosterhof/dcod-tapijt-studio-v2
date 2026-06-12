#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_bauhaus_toevoegen.py
------------------------
Voegt een nieuw Bauhaus-dessin toe als knop (geinspireerd op Bauhaus geometrie:
raster van cellen met halve cirkels, driehoeken, kwartcirkels, ringen, strepen).

Doet:
  1) app.py: voeg generate_bauhaus_svg toe (net voor STYLE_GENERATORS)
  2) app.py: registreer "bauhaus" in STYLE_GENERATORS
  3) app.py: voeg "bauhaus" toe aan extra_styles (anders wordt de generator niet
     bereikt - les uit knitwerk)
  4) app.py: routing in het generate-blok op het woord "bauhaus"
  5) index.html: Bauhaus-knop toevoegen (alfabetisch, na Bamboe) met schone prompt
  6) index.html: cache-buster ophogen

Veilig: backups van app.py en index.html, exact-match vervangingen.

Gebruik:
  1) Stop Flask (Ctrl+C)
  2) cd ~/Desktop/tapijt-studio
  3) python3 fix_bauhaus_toevoegen.py
"""

import os, sys, shutil, re
from datetime import datetime

APP = "app.py"
HTML = "templates/index.html"

BAUHAUS_FUNC = 'def generate_bauhaus_svg(palette: dict, tile_size: int, complexity: str) -> str:\n    import random\n    T = tile_size\n    bg = palette["background"]\n    cols = [palette["primary"], palette["secondary"], palette["accent1"], palette["accent2"], bg]\n    shapes = []\n    grid = {"low": 4, "medium": 5, "high": 6}.get(complexity, 5)\n    cell = T / grid\n    rnd = random.Random(1234 + grid)\n    shapes.append(f\'<rect x="0" y="0" width="{T}" height="{T}" fill="{bg}"/>\')\n\n    def pick(exclude=None):\n        c = rnd.choice(cols)\n        while exclude is not None and c == exclude:\n            c = rnd.choice(cols)\n        return c\n\n    for row in range(grid):\n        for col in range(grid):\n            x = col * cell\n            y = row * cell\n            base = pick()\n            fg = pick(exclude=base)\n            shapes.append(f\'<rect x="{x:.1f}" y="{y:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="{base}"/>\')\n            motif = rnd.choice(["halfcircle", "triangle", "quarter", "rings", "stripes", "circle", "diag"])\n            cx = x + cell / 2\n            cy = y + cell / 2\n            if motif == "halfcircle":\n                r = cell / 2\n                orient = rnd.choice(["t", "b", "l", "rr"])\n                if orient == "t":\n                    d = f\'M {x:.1f} {y+r:.1f} A {r:.1f} {r:.1f} 0 0 1 {x+cell:.1f} {y+r:.1f} Z\'\n                elif orient == "b":\n                    d = f\'M {x:.1f} {y+r:.1f} A {r:.1f} {r:.1f} 0 0 0 {x+cell:.1f} {y+r:.1f} Z\'\n                elif orient == "l":\n                    d = f\'M {x+r:.1f} {y:.1f} A {r:.1f} {r:.1f} 0 0 0 {x+r:.1f} {y+cell:.1f} Z\'\n                else:\n                    d = f\'M {x+r:.1f} {y:.1f} A {r:.1f} {r:.1f} 0 0 1 {x+r:.1f} {y+cell:.1f} Z\'\n                shapes.append(f\'<path d="{d}" fill="{fg}"/>\')\n            elif motif == "triangle":\n                orient = rnd.choice(["u", "d", "l", "rr"])\n                if orient == "u":\n                    pts = f\'{cx:.1f},{y:.1f} {x+cell:.1f},{y+cell:.1f} {x:.1f},{y+cell:.1f}\'\n                elif orient == "d":\n                    pts = f\'{x:.1f},{y:.1f} {x+cell:.1f},{y:.1f} {cx:.1f},{y+cell:.1f}\'\n                elif orient == "l":\n                    pts = f\'{x:.1f},{y:.1f} {x+cell:.1f},{cy:.1f} {x:.1f},{y+cell:.1f}\'\n                else:\n                    pts = f\'{x+cell:.1f},{y:.1f} {x+cell:.1f},{y+cell:.1f} {x:.1f},{cy:.1f}\'\n                shapes.append(f\'<polygon points="{pts}" fill="{fg}"/>\')\n            elif motif == "quarter":\n                corner = rnd.choice(["tl", "tr", "bl", "br"])\n                r = cell\n                if corner == "tl":\n                    d = f\'M {x:.1f} {y:.1f} L {x+r:.1f} {y:.1f} A {r:.1f} {r:.1f} 0 0 1 {x:.1f} {y+r:.1f} Z\'\n                elif corner == "tr":\n                    d = f\'M {x+cell:.1f} {y:.1f} L {x+cell:.1f} {y+r:.1f} A {r:.1f} {r:.1f} 0 0 1 {x+cell-r:.1f} {y:.1f} Z\'\n                elif corner == "bl":\n                    d = f\'M {x:.1f} {y+cell:.1f} L {x:.1f} {y+cell-r:.1f} A {r:.1f} {r:.1f} 0 0 1 {x+r:.1f} {y+cell:.1f} Z\'\n                else:\n                    d = f\'M {x+cell:.1f} {y+cell:.1f} L {x+cell-r:.1f} {y+cell:.1f} A {r:.1f} {r:.1f} 0 0 1 {x+cell:.1f} {y+cell-r:.1f} Z\'\n                shapes.append(f\'<path d="{d}" fill="{fg}"/>\')\n            elif motif == "rings":\n                fg2 = pick(exclude=base)\n                n = 5\n                for i in range(n, 0, -1):\n                    rr = (cell / 2) * (i / n) * 0.9\n                    ringfill = fg if i % 2 == 0 else fg2\n                    shapes.append(f\'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rr:.1f}" fill="{ringfill}"/>\')\n            elif motif == "stripes":\n                n = 5\n                sh = cell / (n * 2)\n                for i in range(n):\n                    yy = y + i * 2 * sh\n                    shapes.append(f\'<rect x="{x:.1f}" y="{yy:.1f}" width="{cell:.1f}" height="{sh:.1f}" fill="{fg}"/>\')\n            elif motif == "circle":\n                shapes.append(f\'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{cell*0.40:.1f}" fill="{fg}"/>\')\n            elif motif == "diag":\n                if rnd.random() < 0.5:\n                    pts = f\'{x:.1f},{y:.1f} {x+cell:.1f},{y:.1f} {x:.1f},{y+cell:.1f}\'\n                else:\n                    pts = f\'{x+cell:.1f},{y:.1f} {x+cell:.1f},{y+cell:.1f} {x:.1f},{y+cell:.1f}\'\n                shapes.append(f\'<polygon points="{pts}" fill="{fg}"/>\')\n    return "\\n".join(shapes)'


def backup(path, stamp):
    b = f"{path}.bak_{stamp}"
    shutil.copy2(path, b)
    print(f"Backup gemaakt: {b}")


def main():
    for p in (APP, HTML):
        if not os.path.exists(p):
            print(f"FOUT: {p} niet gevonden. cd ~/Desktop/tapijt-studio")
            sys.exit(1)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    changes = 0

    backup(APP, stamp)
    src = open(APP, encoding="utf-8").read()

    if "def generate_bauhaus_svg" in src:
        print("OVERGESLAGEN - generate_bauhaus_svg bestaat al.")
    else:
        anchor = "STYLE_GENERATORS = {"
        if anchor in src:
            src = src.replace(anchor, BAUHAUS_FUNC + "\n\n\n" + anchor, 1)
            changes += 1
            print("OK  - generate_bauhaus_svg toegevoegd.")
        else:
            print("OVERGESLAGEN - kon STYLE_GENERATORS niet vinden om functie ervoor te zetten.")

    # Registreer in STYLE_GENERATORS (na de openingsregel)
    reg_anchor = "STYLE_GENERATORS = {\n"
    if '"bauhaus"' in src and "generate_bauhaus_svg," in src:
        print("OVERGESLAGEN - bauhaus al in STYLE_GENERATORS.")
    elif reg_anchor in src:
        src = src.replace(reg_anchor, reg_anchor + '    "bauhaus": generate_bauhaus_svg,\n', 1)
        changes += 1
        print("OK  - bauhaus geregistreerd in STYLE_GENERATORS.")
    else:
        print("OVERGESLAGEN - STYLE_GENERATORS openingsregel niet gevonden.")

    # extra_styles: bauhaus toevoegen vooraan
    es = re.compile(r'(extra_styles = \[)("knitwerk"|"strepen")')
    if '"bauhaus"' in (src[src.find("extra_styles"):src.find("extra_styles")+500] if "extra_styles" in src else ""):
        print("OVERGESLAGEN - bauhaus al in extra_styles.")
    elif es.search(src):
        src = es.sub(r'\1"bauhaus",\2', src, count=1)
        changes += 1
        print("OK  - bauhaus toegevoegd aan extra_styles.")
    else:
        print("OVERGESLAGEN - extra_styles regel niet herkend.")

    # routing in generate-blok: voeg bauhaus-check toe net na 'p = prompt.lower()'
    route_anchor = "        p = prompt.lower()\n"
    route_add = ("        p = prompt.lower()\n"
                 "        if 'bauhaus' in p:\n"
                 "            analysis['style'] = 'bauhaus'\n")
    if "analysis['style'] = 'bauhaus'" in src:
        print("OVERGESLAGEN - bauhaus-routing bestaat al.")
    elif route_anchor in src:
        src = src.replace(route_anchor, route_add, 1)
        changes += 1
        print("OK  - bauhaus-routing toegevoegd in generate-blok.")
    else:
        print("OVERGESLAGEN - kon 'p = prompt.lower()' anker niet vinden.")

    open(APP, "w", encoding="utf-8").write(src)

    # ===== index.html =====
    backup(HTML, stamp)
    html = open(HTML, encoding="utf-8").read()

    bamboe_btn = ("          <button class=\"chip\" onclick=\"setPrompt('Bamboe stokken patroon, "
                  "verticale bamboe in natuurlijke tinten')\">Bamboe</button>\n")
    bauhaus_btn = ("          <button class=\"chip\" onclick=\"setPrompt('Bauhaus geometrisch patroon, "
                   "halve cirkels driehoeken en ringen, oranje zwart grijs')\">Bauhaus</button>\n")
    if "Bauhaus</button>" in html:
        print("OVERGESLAGEN - Bauhaus-knop bestaat al.")
    elif bamboe_btn in html:
        html = html.replace(bamboe_btn, bamboe_btn + bauhaus_btn)
        changes += 1
        print("OK  - Bauhaus-knop toegevoegd (na Bamboe).")
    else:
        print("OVERGESLAGEN - Bamboe-knop niet gevonden (kon Bauhaus niet plaatsen).")

    new_v = datetime.now().strftime("%Y%m%d_%H%M%S")
    if re.search(r'app\.js\?v=[0-9_]+', html):
        html = re.sub(r'(app\.js\?v=)[0-9_]+', r'\g<1>' + new_v, html)
        changes += 1
        print(f"OK  - cache-buster -> ?v={new_v}.")
    else:
        print("OVERGESLAGEN - cache-buster niet gevonden.")

    open(HTML, "w", encoding="utf-8").write(html)

    if changes == 0:
        print("\nGEEN wijzigingen.")
        sys.exit(0)
    print(f"\nKLAAR: {changes} aanpassing(en). Backups met tijdstempel _{stamp}")
    print('Controleer met:  python3 -c "import app"')


if __name__ == "__main__":
    main()
