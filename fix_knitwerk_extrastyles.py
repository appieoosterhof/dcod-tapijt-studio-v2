#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_knitwerk_extrastyles.py
---------------------------
DE ECHTE OORZAAK: in build_tile_svg staat een lijst 'extra_styles' die bepaalt
welke stijlen via STYLE_GENERATORS getekend worden. 'knitwerk' ontbrak in die
lijst. Daardoor viel knitwerk door naar de shape-based tak (generate_geometric_svg
met de AI-shapes) -> achthoeken/ruiten/driehoeken in plaats van V-steken.

Fix: voeg 'knitwerk' toe aan extra_styles. Eén woord, en de juiste generator
wordt aangeroepen.

Veilig: backup + alleen exact gematchte regel; anders overslaan + melden.

Gebruik:
  1) Stop Flask (Ctrl+C)
  2) cd ~/Desktop/tapijt-studio
  3) python3 fix_knitwerk_extrastyles.py
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

    # Robuust: zoek de exacte extra_styles-regel en voeg "knitwerk" toe als
    # die er nog niet in staat. We werken op de hele regel (één regel in app.py).
    import re
    pattern = re.compile(r'(\n[ \t]*extra_styles\s*=\s*\[)("strepen")')
    if '"knitwerk"' in (src[src.find('extra_styles'):src.find('extra_styles')+400] if 'extra_styles' in src else ''):
        print("OVERGESLAGEN - 'knitwerk' lijkt al in extra_styles te staan.")
    elif pattern.search(src):
        src = pattern.sub(r'\1"knitwerk",\2', src, count=1)
        open(APP, "w", encoding="utf-8").write(src)
        print("OK  - 'knitwerk' toegevoegd aan extra_styles (vooraan).")
        print(f"\nKLAAR. Backup: {backup}")
        print('Controleer met:  python3 -c "import app"')
        print(f"Terugzetten kan met:  cp {backup} {APP}")
    else:
        print("OVERGESLAGEN - extra_styles regel niet herkend.")
        print("Stuur de exacte regel met:  grep -n 'extra_styles' app.py")


if __name__ == "__main__":
    main()
