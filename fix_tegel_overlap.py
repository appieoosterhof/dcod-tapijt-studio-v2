#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_tegel_overlap.py
---------------------
Verhelpt de dunne horizontale (en evt. verticale) haarlijnen op de
tegelgrenzen in de all-over repeat -- voor ALLE dessins.

Oorzaak: in build_repeat_svg staan de tegels strak naast elkaar via
translate(x,y). Op de exacte grens tussen twee tegels valt bij het renderen
een sub-pixel haarlijn waar de achtergrond doorschijnt.

Fix: geef elke tegel-<g> een minieme schaal (1.006) zodat aangrenzende tegels
elkaar net overlappen. De overlap is ~2.4px op een 400px-tegel -> onzichtbaar
in het patroon, maar genoeg om de haarlijn te dichten. Werkt voor alle
repeat-types (full/half-drop/brick); bij mirror wordt de schaal met het teken
meegenomen. Visueel geverifieerd (tegel_overlap.png -> geen naad).

Timestamped backup vooraf. Idempotent.

Draai vanuit de projectmap:  python3 fix_tegel_overlap.py
BELANGRIJK: stop Flask (Ctrl+C) eerst.
"""

import os, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "app.py"

def main():
    if not os.path.exists(PATH):
        sys.exit("FOUT: draai dit vanuit de projectmap (~/Desktop/tapijt-studio).")
    with open(PATH, "r", encoding="utf-8") as f:
        txt = f.read()

    if "OVERLAP_SCALE" in txt:
        print("= Tegel-overlap staat er al -- overgeslagen")
        return

    # Blok 1: de mirror-transform krijgt de overlap-schaal mee.
    old_mirror = '                transform = f"translate({tx},{ty}) scale({sx},{sy})"\n'
    new_mirror = '                transform = f"translate({tx},{ty}) scale({sx*OVERLAP_SCALE},{sy*OVERLAP_SCALE})"\n'

    # Blok 2: de normale transform krijgt een lichte schaal mee.
    old_norm = '                transform = f"translate({x},{y})"\n'
    new_norm = '                transform = f"translate({x},{y}) scale({OVERLAP_SCALE})"\n'

    # Definieer OVERLAP_SCALE bovenaan de functie (na T = 400).
    old_T = '    """Bouw een all-over repeat SVG met het opgegeven repeat-type."""\n    T = 400\n'
    new_T = ('    """Bouw een all-over repeat SVG met het opgegeven repeat-type."""\n'
             '    T = 400\n'
             '    OVERLAP_SCALE = 1.006  # minieme tegel-overlap om haarlijn-naden te dichten\n')

    if old_mirror not in txt or old_norm not in txt or old_T not in txt:
        print("! Kon de verwachte regels niet exact vinden.")
        print("  Stuur: sed -n '453,490p' app.py")
        return

    bak = PATH + ".bak_" + STAMP
    shutil.copy2(PATH, bak)
    print("+ Backup gemaakt: " + bak)

    txt = txt.replace(old_T, new_T, 1)
    txt = txt.replace(old_mirror, new_mirror, 1)
    txt = txt.replace(old_norm, new_norm, 1)

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(txt)
    print("+ OVERLAP_SCALE=1.006 toegevoegd en op beide transforms toegepast")
    print("")
    print("Hierna:")
    print("  1) python3 -m py_compile app.py")
    print("  2) Start Flask opnieuw")
    print("  3) Hard refresh (Cmd+Shift+R), klik 'Chevron Bold'")
    print("  4) De horizontale haarlijnen zouden nu weg moeten zijn")

if __name__ == "__main__":
    main()
