#!/usr/bin/env python3
"""
Vervangt de Neo Deco cc-mini placeholder (kleurbanden + cirkel-SVG) door de
echte Art Deco waaier-foto op /inspiratie (komt voor in Hotels & Hospitality).

Vereist: static/img/inspiratie/neo_deco.jpg
         (kopieer eerst vanuit ~/Downloads/)

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_neodeco_thumbnail.py
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/inspiratie.html")

OLD = '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#C9A24A"></div><div class="cc-band" style="background:#1A1A1A"></div><div class="cc-band" style="background:#EFE6CF"></div></div><svg class="cc-acc" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="16" fill="none" stroke="#EFE6CF" stroke-width="0.8" opacity="0.7"/></svg></div>'
NEW = '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/neo_deco.jpg" alt="Neo Deco" loading="lazy"></div>'
VERWACHT = 1


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    gevonden = content.count(OLD)
    if gevonden != VERWACHT:
        print(f"FOUT: {gevonden}x gevonden, verwacht {VERWACHT}x. Stop voor de veiligheid.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"inspiratie.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD, NEW)
    TARGET.write_text(new_content, encoding="utf-8")
    print(f"Neo Deco: {VERWACHT}x vervangen door foto-thumbnail")
    print(f"Oude grootte: {backup.stat().st_size} bytes")
    print(f"Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "cc-photo" templates/inspiratie.html   (verwacht: 23)')


if __name__ == "__main__":
    main()
