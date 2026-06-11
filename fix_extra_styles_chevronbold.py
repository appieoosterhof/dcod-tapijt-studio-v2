#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_extra_styles_chevronbold.py
--------------------------------
Laatste schakel: voeg 'chevron_bold' toe aan de extra_styles-lijst in app.py.

Waarom: build_tile_svg stuurt alleen stijlen die in extra_styles staan direct
naar hun eigen generator. chevron_bold ontbrak in die lijst, waardoor de
code doorviel naar de shapes-afhandeling en generate_geometric_svg met
driehoeken tekende (vandaar de driehoekjes i.p.v. de schuine plankjes).

Fix: chevron_bold in extra_styles zetten, naast de bestaande chevron/visgraat.
Eén gerichte wijziging, timestamped backup vooraf, idempotent.

Draai vanuit de projectmap:  python3 fix_extra_styles_chevronbold.py
BELANGRIJK: stop Flask (Ctrl+C) voordat je dit draait.
"""

import os
import shutil
import datetime
import sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "app.py"

def main():
    if not os.path.exists(PATH):
        sys.exit("FOUT: draai dit vanuit de projectmap (~/Desktop/tapijt-studio).")

    with open(PATH, "r", encoding="utf-8") as f:
        txt = f.read()

    # We zoeken de extra_styles-regel en voegen "chevron_bold" toe vlak na "chevron".
    # De regel bevat o.a. "chevron","hexagon" -- daar haken we op in.
    if '"chevron_bold"' in txt and 'extra_styles = [' in txt:
        # Check of chevron_bold al IN de extra_styles-regel staat.
        for line in txt.split("\n"):
            if line.strip().startswith("extra_styles = [") and "chevron_bold" in line:
                print("= chevron_bold staat al in extra_styles -- overgeslagen")
                return

    anchor = '"strepen","mozaiek","chevron","hexagon"'
    replacement = '"strepen","mozaiek","chevron","chevron_bold","hexagon"'

    if anchor not in txt:
        print("! Kon de extra_styles-regel niet exact vinden.")
        print("  Geen wijziging gemaakt. Stuur de uitvoer van:")
        print('  grep -n "extra_styles = " app.py')
        return

    bak = PATH + ".bak_" + STAMP
    shutil.copy2(PATH, bak)
    print("+ Backup gemaakt: " + bak)

    txt = txt.replace(anchor, replacement, 1)

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(txt)
    print("+ chevron_bold toegevoegd aan extra_styles")
    print("")
    print("Klaar. Hierna:")
    print("  1) python3 -m py_compile app.py")
    print("  2) Start Flask opnieuw")
    print("  3) Hard refresh (Cmd+Shift+R), klik 'Chevron Bold'")
    print("  4) Je zou nu schuine GEVULDE plankjes moeten zien (geen driehoeken)")

if __name__ == "__main__":
    main()
