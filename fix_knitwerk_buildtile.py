#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_knitwerk_buildtile.py
-------------------------
Probleem: build_tile_svg() doet ZELF nog twee extra style-routings (op basis van
analysis["_prompt"] en analysis["description_nl"]). Geen van beide kent 'knitwerk',
en de tweede kijkt naar de AI-beschrijving. Daardoor wordt onze correcte keuze
analysis['style']='knitwerk' in build_tile_svg overschreven -> verkeerd dessin.

Fix: voeg in BEIDE routings een knitwerk-guard toe, helemaal vooraan, zodat een
knitwerk-keuze behouden blijft. We checken op:
  - style == "knitwerk"  (al eerder gezet door het generate-blok)
  - knit-keywords in de tekst

Veiligheid:
  - Backup app.py.bak_JJJJMMDD_UUMMSS
  - Alleen exact gematchte ankers worden aangepast; anders overslaan + melden.

Gebruik:
  1) Stop Flask (Ctrl+C)
  2) cd ~/Desktop/tapijt-studio
  3) python3 fix_knitwerk_buildtile.py
"""

import os, sys, shutil
from datetime import datetime

APP = "app.py"
KNIT_WORDS = "'knitwerk', 'knit', 'gebreid', 'breiwerk', 'fair isle', 'noorse trui', 'nordic', 'scandinavisch', 'noors', 'sneeuwvlok'"


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

    # --- Routing 1: net na 'p = analysis.get("_prompt", "")' ---
    anchor1 = ('    style = analysis.get("style", "geometric")\n'
               '    p = analysis.get("_prompt", "")\n'
               '    if any(w in p for w in ["streep", "strepen", "stripe"]):\n'
               '        style = "strepen"\n')
    guard1 = ('    style = analysis.get("style", "geometric")\n'
              '    p = analysis.get("_prompt", "")\n'
              '    if style == "knitwerk" or any(w in p for w in [' + KNIT_WORDS + ']):\n'
              '        style = "knitwerk"\n'
              '    elif any(w in p for w in ["streep", "strepen", "stripe"]):\n'
              '        style = "strepen"\n')
    if anchor1 in src:
        src = src.replace(anchor1, guard1)
        changes += 1
        print("OK  - knitwerk-guard toegevoegd aan routing 1 (_prompt).")
    else:
        print("OVERGESLAGEN - anker routing 1 niet exact gevonden.")

    # --- Routing 2: net na 'prompt_lower = analysis.get("description_nl", "").lower()' ---
    anchor2 = ('    prompt_lower = analysis.get("description_nl", "").lower()\n'
               '    if any(w in prompt_lower for w in ["streep", "strepen", "stripe", "verticale lijn"]):\n'
               '        style = "strepen"\n')
    guard2 = ('    prompt_lower = analysis.get("description_nl", "").lower()\n'
              '    if style == "knitwerk":\n'
              '        pass\n'
              '    elif any(w in prompt_lower for w in ["streep", "strepen", "stripe", "verticale lijn"]):\n'
              '        style = "strepen"\n')
    if anchor2 in src:
        src = src.replace(anchor2, guard2)
        changes += 1
        print("OK  - knitwerk-guard toegevoegd aan routing 2 (description_nl).")
    else:
        print("OVERGESLAGEN - anker routing 2 niet exact gevonden.")

    if changes == 0:
        print("\nGEEN wijzigingen. app.py ongewijzigd.")
        sys.exit(0)

    open(APP, "w", encoding="utf-8").write(src)
    print(f"\nKLAAR: {changes} aanpassing(en) opgeslagen.")
    print('Controleer met:  python3 -c "import app"')
    print(f"Terugzetten kan met:  cp {backup} {APP}")


if __name__ == "__main__":
    main()
