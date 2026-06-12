#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_knitwerk_grof_knop.py
-------------------------
Afronding knitwerk, drie dingen in een keer:

  A) app.py: steken EXTRA grof in generate_knitwerk_svg.
     cells -> 5 (8 cm per steek bij 40cm-tegel). 5 deelt 400 exact en de
     bandperiode is 5, dus naadloos (1 band-cyclus per tegel).
     low=5, medium=5, high=10 (high iets fijner als variatie).

  B) templates/index.html:
     - verwijder Abstract-knop
     - verwijder Nordic-knop
     - voeg Knitwerk-knop toe (na Houndstooth) met SCHONE prompt zonder 'ruit'

  C) cache-buster ?v= ophogen.

Veilig: backups van app.py en index.html, exact-match vervangingen.

Gebruik:
  1) Stop Flask (Ctrl+C)
  2) cd ~/Desktop/tapijt-studio
  3) python3 fix_knitwerk_grof_knop.py
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

    # ===== A) app.py - extra grof =====
    backup(APP, stamp)
    src = open(APP, encoding="utf-8").read()
    # We accepteren de huidige waarde (na vorige fix kan dat 20 of 25 zijn).
    cells_re = re.compile(r'cells = \{"low": \d+, "medium": \d+, "high": \d+\}\.get\(complexity, \d+\)')
    new_cells = 'cells = {"low": 5, "medium": 5, "high": 10}.get(complexity, 5)'
    if cells_re.search(src):
        src = cells_re.sub(new_cells, src, count=1)
        open(APP, "w", encoding="utf-8").write(src)
        changes += 1
        print("OK  - app.py: knitwerk EXTRA grof (cells -> 5).")
    else:
        print("OVERGESLAGEN - cells-regel in generate_knitwerk_svg niet gevonden.")

    # ===== B + C) index.html =====
    backup(HTML, stamp)
    html = open(HTML, encoding="utf-8").read()

    abstract_btn = ("          <button class=\"chip\" onclick=\"setPrompt('Abstracte kleurrijke vlakken, "
                    "moderne kunst stijl, helder contrast')\">Abstract</button>\n")
    if abstract_btn in html:
        html = html.replace(abstract_btn, "")
        changes += 1
        print("OK  - index.html: Abstract-knop verwijderd.")
    else:
        print("OVERGESLAGEN - Abstract-knop niet exact gevonden (mogelijk al weg).")

    nordic_btn = ("          <button class=\"chip\" onclick=\"setPrompt('Scandinavisch nordic geometrisch "
                  "met ruitpatroon, blauw en wit, strak en minimalistisch')\">Nordic</button>\n")
    if nordic_btn in html:
        html = html.replace(nordic_btn, "")
        changes += 1
        print("OK  - index.html: Nordic-knop verwijderd.")
    else:
        print("OVERGESLAGEN - Nordic-knop niet exact gevonden (mogelijk al weg).")

    houndstooth_btn = ("          <button class=\"chip\" onclick=\"setPrompt('houndstooth patroon, "
                       "hanenpoot pied-de-poule, zwart wit')\">Houndstooth</button>\n")
    knitwerk_btn = ("          <button class=\"chip\" onclick=\"setPrompt('Scandinavisch knitwerk patroon, "
                    "gebreide steken, zigzag banden in blauw en wit')\">Knitwerk</button>\n")
    if "Knitwerk</button>" in html:
        print("OVERGESLAGEN - Knitwerk-knop bestaat al.")
    elif houndstooth_btn in html:
        html = html.replace(houndstooth_btn, houndstooth_btn + knitwerk_btn)
        changes += 1
        print("OK  - index.html: Knitwerk-knop toegevoegd (na Houndstooth).")
    else:
        print("OVERGESLAGEN - Houndstooth-knop niet gevonden (kon Knitwerk niet plaatsen).")

    new_v = datetime.now().strftime("%Y%m%d_%H%M%S")
    if re.search(r'app\.js\?v=[0-9_]+', html):
        html = re.sub(r'(app\.js\?v=)[0-9_]+', r'\g<1>' + new_v, html)
        changes += 1
        print(f"OK  - index.html: cache-buster -> ?v={new_v}.")
    else:
        print("OVERGESLAGEN - cache-buster ?v= niet gevonden.")

    open(HTML, "w", encoding="utf-8").write(html)

    if changes == 0:
        print("\nGEEN wijzigingen.")
        sys.exit(0)
    print(f"\nKLAAR: {changes} aanpassing(en). Backups met tijdstempel _{stamp}")
    print('Controleer met:  python3 -c "import app"')


if __name__ == "__main__":
    main()
