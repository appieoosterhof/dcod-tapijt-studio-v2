#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
voeg_chevron_bold_toe.py
-------------------------
Voegt een NIEUWE dessin-generator 'chevron_bold' toe (herringbone-plankjes,
gevuld, helling klapt per kolom om). Raakt de bestaande 'chevron' NIET aan.

Wijzigt drie bestanden, elk met timestamped backup VOORAF:
  1) modules_extra.py     -> nieuwe functie generate_chevron_bold_svg
  2) app.py               -> import + STYLE_GENERATORS + trefwoord in build_tile_svg
  3) templates/index.html -> nieuwe knop "Chevron Bold"

Veilig opnieuw te draaien: slaat stappen over die al gedaan zijn.
Draai vanuit de projectmap:  python3 voeg_chevron_bold_toe.py
BELANGRIJK: stop Flask (Ctrl+C) voordat je dit draait.
"""

import os
import shutil
import datetime
import sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(path):
    if not os.path.exists(path):
        print("  ! Bestand niet gevonden: " + path + " -- overgeslagen")
        return False
    bak = path + ".bak_" + STAMP
    shutil.copy2(path, bak)
    print("  + Backup gemaakt: " + bak)
    return True

def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write(path, txt):
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)

NEW_FUNC = r'''

def generate_chevron_bold_svg(palette, tile_size, complexity):
    """Chevron Bold: gevulde herringbone-plankjes in verticale kolommen.
    De helling klapt per kolom om (V-vorm waar kolommen samenkomen).
    Naadloos: cel-breedte en cel-hoogte delen de tegel (400) exact.
    Kleur-klaar via _palet: k[0]=achtergrond, k[1]/k[2]=plankkleuren."""
    T = float(tile_size)
    k = _palet(palette)
    cols = {'low': 5, 'medium': 8, 'high': 10}.get(complexity, 8)
    cw = T / cols
    ch = cw
    slant = cw
    s = ['<rect width="%.1f" height="%.1f" fill="%s"/>' % (T, T, k[0])]
    n_rows = int(T / ch) + 3
    for col in range(-1, cols + 1):
        x0 = col * cw
        direction = 1 if (col % 2 == 0) else -1
        for row in range(-1, n_rows):
            y0 = row * ch
            tweede = k[2] if len(k) > 2 else k[1]
            kleur = k[1] if ((row + col) % 2 == 0) else tweede
            dx = slant * direction
            pts = [
                (x0,            y0),
                (x0 + cw,       y0),
                (x0 + cw + dx,  y0 + ch),
                (x0 + dx,       y0 + ch),
            ]
            pts_str = ' '.join('%.1f,%.1f' % (px, py) for px, py in pts)
            s.append('<polygon points="%s" fill="%s"/>' % (pts_str, kleur))
    return '\n'.join(s)
'''

def patch_modules_extra():
    path = "modules_extra.py"
    print("[1/3] " + path)
    txt = read(path)
    if "def generate_chevron_bold_svg" in txt:
        print("  = generate_chevron_bold_svg bestaat al -- overgeslagen")
        return
    if not backup(path):
        sys.exit("  ! Kan niet doorgaan zonder modules_extra.py")
    txt = txt.rstrip() + "\n" + NEW_FUNC + "\n"
    write(path, txt)
    print("  + Functie generate_chevron_bold_svg toegevoegd")

def patch_app():
    path = "app.py"
    print("[2/3] " + path)
    txt = read(path)
    changed = False

    if "generate_chevron_bold_svg" not in txt:
        lines = txt.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("from modules_extra import") and "generate_chevron_svg" in line:
                lines[i] = line.rstrip() + ", generate_chevron_bold_svg"
                changed = True
                print("  + Import uitgebreid met generate_chevron_bold_svg")
                break
        txt = "\n".join(lines)
    else:
        print("  = Import bevat al generate_chevron_bold_svg")

    if '"chevron_bold":' not in txt:
        marker = '    "chevron": generate_chevron_svg,\n'
        if marker in txt:
            txt = txt.replace(marker, marker + '    "chevron_bold": generate_chevron_bold_svg,\n', 1)
            changed = True
            print("  + STYLE_GENERATORS uitgebreid met chevron_bold")
        else:
            print("  ! Kon de 'chevron'-regel in STYLE_GENERATORS niet vinden -- handmatig nodig")
    else:
        print("  = STYLE_GENERATORS bevat al chevron_bold")

    if 'style = "chevron_bold"' not in txt:
        chevron_elif = ('    elif any(w in p for w in ["chevron", "zigzag"]):\n'
                        '        style = "chevron"\n')
        new_block = ('    elif any(w in p for w in ["chevron bold", "herringbone", "chevron blok"]):\n'
                     '        style = "chevron_bold"\n' + chevron_elif)
        if chevron_elif in txt:
            txt = txt.replace(chevron_elif, new_block, 1)
            changed = True
            print("  + Trefwoord-regel voor chevron_bold toegevoegd in build_tile_svg")
        else:
            print("  ! Kon de chevron-elif in build_tile_svg niet exact vinden -- handmatig nodig")
    else:
        print("  = build_tile_svg bevat al chevron_bold-trefwoord")

    if changed:
        if not backup(path):
            sys.exit("  ! Kan niet doorgaan zonder app.py")
        write(path, txt)
        print("  + app.py opgeslagen")
    else:
        print("  = app.py ongewijzigd")

def patch_index():
    path = os.path.join("templates", "index.html")
    print("[3/3] " + path)
    txt = read(path)
    if ">Chevron Bold<" in txt:
        print("  = Knop 'Chevron Bold' bestaat al -- overgeslagen")
        return
    anchor = None
    for line in txt.split("\n"):
        if "setPrompt(" in line and ">Visgraat<" in line:
            anchor = line
            break
    if anchor is None:
        print("  ! Visgraat-knop niet gevonden -- handmatig nodig")
        return
    if not backup(path):
        sys.exit("  ! Kan niet doorgaan zonder index.html")
    indent = anchor[:len(anchor) - len(anchor.lstrip())]
    prompt_txt = "Chevron Bold patroon, gevulde herringbone plankjes, zwart wit"
    new_button = (indent + '<button class="chip" onclick="setPrompt('
                  + chr(39) + prompt_txt + chr(39) + ')">Chevron Bold</button>')
    txt = txt.replace(anchor, anchor + "\n" + new_button, 1)
    write(path, txt)
    print("  + Knop 'Chevron Bold' toegevoegd na Visgraat")

def main():
    if not (os.path.exists("app.py") and os.path.exists("modules_extra.py")):
        sys.exit("FOUT: draai dit script vanuit de projectmap (~/Desktop/tapijt-studio).")
    print("=== Chevron Bold toevoegen (timestamp " + STAMP + ") ===")
    patch_modules_extra()
    patch_app()
    patch_index()
    print("")
    print("Klaar. Controleer hierna:")
    print("  1) Start Flask opnieuw")
    print("  2) Hard refresh in de browser (Cmd+Shift+R)")
    print("  3) Klik 'Chevron Bold' en check patroon + naadloze tegeling")

if __name__ == "__main__":
    main()
