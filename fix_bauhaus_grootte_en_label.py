#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_bauhaus_grootte_en_label.py
-------------------------------
Drie aanpassingen voor Bauhaus:

  1) Grotere cellen: grid medium 5 -> 3 (~13 cm per cel bij 40cm-tegel).
     low blijft 4, high 5 (variatie). Alle delen 400-tegel netjes.

  2) Label-fix: in build_tile_svg overschrijven twee routings de stijl op basis
     van prompt-woorden ("halve cirkels" -> matcht 'cirkel'). We voegen een
     bauhaus-guard toe in BEIDE routings (if style == "bauhaus": ... als eerste
     tak), zodat bauhaus behouden blijft. Net als de knitwerk-guard.

  3) label_map: voeg een bauhaus-regel toe VOOR de cirkels-regel, zodat het
     weergave-label "bauhaus" toont en niet "cirkels".

Veilig: backup + exact-match; niet-gevonden ankers worden overgeslagen + gemeld.

Gebruik:
  1) Stop Flask (Ctrl+C)
  2) cd ~/Desktop/tapijt-studio
  3) python3 fix_bauhaus_grootte_en_label.py
"""

import os, sys, shutil
from datetime import datetime

APP = "app.py"


def main():
    if not os.path.exists(APP):
        print(f"FOUT: {APP} niet gevonden. cd ~/Desktop/tapijt-studio")
        sys.exit(1)

    src = open(APP, encoding="utf-8").read()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = f"{APP}.bak_{stamp}"
    shutil.copy2(APP, backup)
    print(f"Backup gemaakt: {backup}")

    changes = 0

    # ---- 1. grid groter in generate_bauhaus_svg ----
    old_grid = '    grid = {"low": 4, "medium": 5, "high": 6}.get(complexity, 5)'
    new_grid = '    grid = {"low": 3, "medium": 3, "high": 4}.get(complexity, 3)'
    if old_grid in src:
        src = src.replace(old_grid, new_grid)
        changes += 1
        print("OK  - bauhaus grid groter (medium -> 3).")
    else:
        print("OVERGESLAGEN - grid-regel in generate_bauhaus_svg niet gevonden.")

    # ---- 2a. guard in routing 1 (_prompt): net na de knitwerk-guard ----
    # We hangen bauhaus aan dezelfde eerste guard-structuur.
    r1_anchor = ('    if style == "knitwerk" or any(w in p for w in '
                 "['knitwerk', 'knit', 'gebreid', 'breiwerk', 'fair isle', 'noorse trui', "
                 "'nordic', 'scandinavisch', 'noors', 'sneeuwvlok']):\n"
                 '        style = "knitwerk"\n')
    r1_new = ('    if style == "bauhaus" or "bauhaus" in p:\n'
              '        style = "bauhaus"\n'
              '    elif style == "knitwerk" or any(w in p for w in '
              "['knitwerk', 'knit', 'gebreid', 'breiwerk', 'fair isle', 'noorse trui', "
              "'nordic', 'scandinavisch', 'noors', 'sneeuwvlok']):\n"
              '        style = "knitwerk"\n')
    if 'if style == "bauhaus"' in src:
        print("OVERGESLAGEN - bauhaus-guard routing 1 bestaat al.")
    elif r1_anchor in src:
        src = src.replace(r1_anchor, r1_new, 1)
        changes += 1
        print("OK  - bauhaus-guard toegevoegd aan routing 1 (_prompt).")
    else:
        print("OVERGESLAGEN - anker routing 1 (knitwerk-guard) niet gevonden.")

    # ---- 2b. guard in routing 2 (description_nl): net na 'if style == "knitwerk": pass' ----
    r2_anchor = ('    prompt_lower = analysis.get("description_nl", "").lower()\n'
                 '    if style == "knitwerk":\n'
                 '        pass\n')
    r2_new = ('    prompt_lower = analysis.get("description_nl", "").lower()\n'
              '    if style == "bauhaus":\n'
              '        pass\n'
              '    elif style == "knitwerk":\n'
              '        pass\n')
    if 'if style == "bauhaus":\n        pass' in src:
        print("OVERGESLAGEN - bauhaus-guard routing 2 bestaat al.")
    elif r2_anchor in src:
        src = src.replace(r2_anchor, r2_new, 1)
        changes += 1
        print("OK  - bauhaus-guard toegevoegd aan routing 2 (description_nl).")
    else:
        print("OVERGESLAGEN - anker routing 2 (knitwerk pass) niet gevonden.")

    # ---- 3. label_map: bauhaus-regel vóór de cirkels-regel ----
    cirkel_label = "            (['cirkel'], 'cirkels'),\n"
    bauhaus_label = ("            (['bauhaus'], 'bauhaus'),\n"
                     "            (['cirkel'], 'cirkels'),\n")
    if "(['bauhaus'], 'bauhaus')" in src:
        print("OVERGESLAGEN - bauhaus label_map-regel bestaat al.")
    elif cirkel_label in src:
        src = src.replace(cirkel_label, bauhaus_label, 1)
        changes += 1
        print("OK  - label_map: bauhaus-regel toegevoegd vóór cirkels.")
    else:
        print("OVERGESLAGEN - cirkels-regel in label_map niet gevonden.")

    if changes == 0:
        print("\nGEEN wijzigingen.")
        sys.exit(0)

    open(APP, "w", encoding="utf-8").write(src)
    print(f"\nKLAAR: {changes} aanpassing(en).")
    print('Controleer met:  python3 -c "import app"')
    print(f"Terugzetten kan met:  cp {backup} {APP}")


if __name__ == "__main__":
    main()
