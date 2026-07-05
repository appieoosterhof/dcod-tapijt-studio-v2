#!/usr/bin/env python3
"""
Vervangt de 3-ringen hero-C door het geprefereerde 2-ringen-ontwerp
(roze buiten #C38D96, olijfgroen binnen #6f8a4e), consistent met de
kleine C in de Dessinator-sidebar.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_logo_c_hero_2ring.py
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/inspiratie.html")

OLD_SVG = '''<svg class="logo-c-hero" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M22.5,27.258 A13,13 0 1,1 22.5,4.742" stroke="#A7C58E" stroke-width="3.4" stroke-linecap="round"/><path d="M20.75,24.227 A9.5,9.5 0 1,1 20.75,7.773" stroke="#C38D96" stroke-width="3.4" stroke-linecap="round"/><path d="M19,21.196 A6,6 0 1,1 19,10.804" stroke="#D5E0DF" stroke-width="3.4" stroke-linecap="round"/></svg>'''
NEW_SVG = '''<svg class="logo-c-hero" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M22.5,27.258 A13,13 0 1,1 22.5,4.742" stroke="#C38D96" stroke-width="3.4" stroke-linecap="round"/><path d="M19,21.196 A6,6 0 1,1 19,10.804" stroke="#6f8a4e" stroke-width="3.4" stroke-linecap="round"/></svg>'''


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    count = content.count(OLD_SVG)
    if count == 0:
        print("FOUT: de verwachte oude 3-ringen SVG is niet exact gevonden.")
        sys.exit(1)
    if count > 1:
        print(f"FOUT: komt {count}x voor, verwacht precies 1x. Stop voor de veiligheid.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"inspiratie.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD_SVG, NEW_SVG)
    TARGET.write_text(new_content, encoding="utf-8")
    print("inspiratie.html aangepast: hero-C is nu 2 ringen (roze/olijfgroen), consistent met sidebar")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")


if __name__ == "__main__":
    main()
