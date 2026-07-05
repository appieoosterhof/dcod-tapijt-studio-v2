#!/usr/bin/env python3
"""
Vervangt de placeholder cc-mini (kleurbanden + SVG-golflijnen) door de echte
Hoogtelijnen-foto op /inspiratie.

Vereist: static/img/inspiratie/hoogtelijnen.jpg
         (kopieer eerst vanuit ~/Downloads/inspiratie_thumbs/)

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_cc_hoogtelijnen.py
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/inspiratie.html")

OLD = '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#6f8a4e"></div><div class="cc-band" style="background:#A7C58E"></div><div class="cc-band" style="background:#e9e0c8"></div></div><svg class="cc-acc" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 18 C 25 12, 50 24, 100 15" fill="none" stroke="#e9e0c8" stroke-width="0.9" opacity="0.55"/><path d="M0 31 C 25 25, 50 37, 100 28" fill="none" stroke="#e9e0c8" stroke-width="0.9" opacity="0.55"/><path d="M0 44 C 25 38, 50 50, 100 41" fill="none" stroke="#e9e0c8" stroke-width="0.9" opacity="0.55"/><path d="M0 57 C 25 51, 50 63, 100 54" fill="none" stroke="#e9e0c8" stroke-width="0.9" opacity="0.55"/><path d="M0 70 C 25 64, 50 76, 100 67" fill="none" stroke="#e9e0c8" stroke-width="0.9" opacity="0.55"/><path d="M0 83 C 25 77, 50 89, 100 80" fill="none" stroke="#e9e0c8" stroke-width="0.9" opacity="0.55"/></svg></div>'
NEW = '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/hoogtelijnen.jpg" alt="Hoogtelijnen" loading="lazy"></div>'
VERWACHT = 2


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    gevonden = content.count(OLD)
    if gevonden != VERWACHT:
        print(f"FOUT: {gevonden}x gevonden, verwacht {VERWACHT}x. Stop voor de veiligheid.")
        if gevonden == 0:
            print("Mogelijk is dit blok al vervangen (bijv. als het thumbnail-script al eerder draaide).")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"inspiratie.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD, NEW)
    TARGET.write_text(new_content, encoding="utf-8")
    print(f"Hoogtelijnen: {VERWACHT}x vervangen door foto-thumbnail")
    print(f"Oude grootte: {backup.stat().st_size} bytes")
    print(f"Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "cc-photo" templates/inspiratie.html   (verwacht: 7 als de vorige fix ook al draaide)')


if __name__ == "__main__":
    main()
