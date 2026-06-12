#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_knitwerk_knop_en_grootte.py
-------------------------------
Afronding knitwerk. Drie dingen in een keer:

  A) app.py: steken groter maken in generate_knitwerk_svg
     (cells medium/high 25->20, low 20->16). 20 en 16 delen 400 exact -> naadloos.

  B) templates/index.html:
     - verwijder de Abstract-knop (regel ~59)
     - verwijder de Nordic-knop (regel ~69)
     - voeg een Knitwerk-knop toe (alfabetisch, na Houndstooth) met SCHONE prompt
       zonder het woord 'ruit' (anders kaping naar urban_plaid).

  C) templates/index.html: hoog de ?v=-cache-buster op zodat de browser de
     nieuwste app.js/HTML laadt.

Veilig: backups van BEIDE bestanden + alleen exact gematchte stukken; anders
overslaan + melden. Niets wordt half aangepast.

Gebruik:
  1) Stop Flask (Ctrl+C)
  2) cd ~/Desktop/tapijt-studio
  3) python3 fix_knitwerk_knop_en_grootte.py
"""

import os, sys, shutil, re
from datetime import datetime

APP = "app.py"
HTML = "templates/index.html"


def backup(path, stamp):
    b = f"{path}.bak_{stamp}"
    shutil.copy2(path, b)
    print(f"Backup gemaakt: {b}")
    return b


def main():
    for p in (APP, HTML):
        if not os.path.exists(p):
            print(f"FOUT: {p} niet gevonden. cd ~/Desktop/tapijt-studio")
            sys.exit(1)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    changes = 0

    # ===== A) app.py - steken groter =====
    backup(APP, stamp)
    src = open(APP, encoding="utf-8").read()
    old_cells = '    cells = {"low": 20, "medium": 25, "high": 25}.get(complexity, 25)'
    new_cells = '    cells = {"low": 16, "medium": 20, "high": 20}.get(complexity, 20)'
    if old_cells in src:
        src = src.replace(old_cells, new_cells)
        open(APP, "w", encoding="utf-8").write(src)
        changes += 1
        print("OK  - app.py: knitwerk-steken groter (cells -> 20).")
    else:
        print("OVERGESLAGEN - cells-regel in generate_knitwerk_svg niet exact gevonden.")

    # ===== B + C) index.html =====
    backup(HTML, stamp)
    html = open(HTML, encoding="utf-8").read()

    # B1: Abstract-knop verwijderen (hele regel incl. omliggende newline)
    abstract_btn = ("          <button class=\"chip\" onclick=\"setPrompt('Abstracte kleurrijke vlakken, "
                    "moderne kunst stijl, helder contrast')\">Abstract</button>\n")
    if abstract_btn in html:
        html = html.replace(abstract_btn, "")
        changes += 1
        print("OK  - index.html: Abstract-knop verwijderd.")
    else:
        print("OVERGESLAGEN - Abstract-knop niet exact gevonden.")

    # B2: Nordic-knop verwijderen
    nordic_btn = ("          <button class=\"chip\" onclick=\"setPrompt('Scandinavisch nordic geometrisch "
                  "met ruitpatroon, blauw en wit, strak en minimalistisch')\">Nordic</button>\n")
    if nordic_btn in html:
        html = html.replace(nordic_btn, "")
        changes += 1
        print("OK  - index.html: Nordic-knop verwijderd.")
    else:
        print("OVERGESLAGEN - Nordic-knop niet exact gevonden.")

    # B3: Knitwerk-knop toevoegen, net na de Houndstooth-knop (alfabetische plek)
    houndstooth_btn = ("          <button class=\"chip\" onclick=\"setPrompt('houndstooth patroon, "
                       "hanenpoot pied-de-poule, zwart wit')\">Houndstooth</button>\n")
    knitwerk_btn = ("          <button class=\"chip\" onclick=\"setPrompt('Scandinavisch knitwerk patroon, "
                    "gebreide steken, zigzag banden in blauw en wit')\">Knitwerk</button>\n")
    if houndstooth_btn in html and "Knitwerk</button>" not in html:
        html = html.replace(houndstooth_btn, houndstooth_btn + knitwerk_btn)
        changes += 1
        print("OK  - index.html: Knitwerk-knop toegevoegd (na Houndstooth).")
    elif "Knitwerk</button>" in html:
        print("OVERGESLAGEN - Knitwerk-knop bestaat al.")
    else:
        print("OVERGESLAGEN - Houndstooth-knop niet gevonden (kon Knitwerk niet plaatsen).")

    # C: cache-buster ?v=... ophogen naar nieuwe timestamp
    new_v = datetime.now().strftime("%Y%m%d_%H%M%S")
    m = re.search(r'app\.js\?v=([0-9_]+)', html)
    if m:
        html = re.sub(r'(app\.js\?v=)[0-9_]+', r'\g<1>' + new_v, html)
        changes += 1
        print(f"OK  - index.html: cache-buster opgehoogd naar ?v={new_v}.")
    else:
        print("OVERGESLAGEN - cache-buster ?v= niet gevonden in index.html.")

    open(HTML, "w", encoding="utf-8").write(html)

    if changes == 0:
        print("\nGEEN wijzigingen doorgevoerd.")
        sys.exit(0)

    print(f"\nKLAAR: {changes} aanpassing(en).")
    print('Controleer met:  python3 -c "import app"')
    print(f"Backups staan klaar met tijdstempel _{stamp}")


if __name__ == "__main__":
    main()
