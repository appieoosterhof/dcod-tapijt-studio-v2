#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_knitwerk_slot.py
--------------------
Laatste fix. In build_tile_svg staan nog twee routings die style op de
NIET-MEER-BESTAANDE waarde 'nordic' zetten:
  - regel ~378-379 (op basis van _prompt)
  - regel ~405-406 (op basis van description_nl = AI-beschrijving)
Omdat 'nordic' niet meer in STYLE_GENERATORS staat, valt de tekening terug op
generate_geometric_svg (sterren/achthoeken). Daardoor klopt het label (knitwerk)
maar het dessin niet.

Fix: vervang die twee 'style = "nordic"' toewijzingen door 'style = "knitwerk"'.
Dan leidt elke nordic/scandinavisch/noors-match naar het knitwerk-dessin, ongeacht
welke routing wint.

Veilig: backup + alleen exact gematchte regels; anders overslaan + melden.

Gebruik:
  1) Stop Flask (Ctrl+C)
  2) cd ~/Desktop/tapijt-studio
  3) python3 fix_knitwerk_slot.py
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

    # Routing 1 (op _prompt): de nordic-regel -> knitwerk
    old1 = ('    elif any(w in p for w in ["nordic", "scandinavisch", "noors", "kruis", "sneeuwvlok"]):\n'
            '        style = "nordic"\n')
    new1 = ('    elif any(w in p for w in ["nordic", "scandinavisch", "noors", "kruis", "sneeuwvlok", "knitwerk", "knit", "gebreid", "breiwerk"]):\n'
            '        style = "knitwerk"\n')
    if old1 in src:
        src = src.replace(old1, new1)
        changes += 1
        print("OK  - routing 1 (_prompt): nordic -> knitwerk.")
    else:
        print("OVERGESLAGEN - routing 1 nordic-regel niet exact gevonden.")

    # Routing 2 (op description_nl): de nordic-regel -> knitwerk
    old2 = ('    elif any(w in prompt_lower for w in ["nordic", "scandinavisch", "noors", "kruis", "ruitpatroon"]):\n'
            '        style = "nordic"\n')
    new2 = ('    elif any(w in prompt_lower for w in ["nordic", "scandinavisch", "noors", "knitwerk", "knit", "gebreid", "breiwerk", "fair isle"]):\n'
            '        style = "knitwerk"\n')
    if old2 in src:
        src = src.replace(old2, new2)
        changes += 1
        print("OK  - routing 2 (description_nl): nordic -> knitwerk.")
    else:
        print("OVERGESLAGEN - routing 2 nordic-regel niet exact gevonden.")

    if changes == 0:
        print("\nGEEN wijzigingen. app.py ongewijzigd.")
        sys.exit(0)

    open(APP, "w", encoding="utf-8").write(src)
    print(f"\nKLAAR: {changes} aanpassing(en) opgeslagen.")
    print('Controleer met:  python3 -c "import app"')
    print(f"Terugzetten kan met:  cp {backup} {APP}")


if __name__ == "__main__":
    main()
