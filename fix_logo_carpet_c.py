#!/usr/bin/env python3
"""
Vervangt de logo-mark (4 losse gekleurde vierkantjes) door een SVG-icoon
met drie concentrische, naar rechts geopende bogen -- het "opgerolde
tapijtloper"-C-motief van het nieuwe DCOD-logo, opgebouwd in de
bestaande Dessinator-kleuren (roze/sage/olijfgroen).

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_logo_carpet_c.py
Maakt automatisch een timestamped .bak van templates/index.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/index.html")

OLD = '''      <div class="logo-mark" aria-hidden="true">
        <span style="background:#C38D96"></span><span style="background:#A7C58E"></span>
        <span style="background:#A7C58E"></span><span style="background:#6f8a4e"></span>
      </div>'''

NEW = '''      <div class="logo-mark" aria-hidden="true">
        <svg width="29" height="29" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M25.96,24.36 A13,13 0 1,1 25.96,7.64" stroke="#C38D96" stroke-width="2.6" stroke-linecap="round"/>
          <path d="M23.28,22.11 A9.5,9.5 0 1,1 23.28,9.89" stroke="#A7C58E" stroke-width="2.6" stroke-linecap="round"/>
          <path d="M20.6,19.86 A6,6 0 1,1 20.6,12.14" stroke="#6f8a4e" stroke-width="2.6" stroke-linecap="round"/>
        </svg>
      </div>'''


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    count = content.count(OLD)
    if count == 0:
        print("FOUT: de verwachte oude logo-mark HTML is niet exact gevonden.")
        sys.exit(1)
    if count > 1:
        print(f"FOUT: komt {count}x voor, verwacht precies 1x. Stop voor de veiligheid.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"index.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD, NEW)
    TARGET.write_text(new_content, encoding="utf-8")
    print("index.html aangepast: logo-mark is nu de 'opgerolde loper'-C in SVG")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "opgerolde\\|A13,13" templates/index.html')


if __name__ == "__main__":
    main()
