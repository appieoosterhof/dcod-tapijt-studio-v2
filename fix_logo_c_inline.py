#!/usr/bin/env python3
"""
Twee dingen in templates/index.html:
1. Verwijdert het losse logo-mark icoontje (de concentrische bogen die
   nu VOOR de tekst 'DCOD Dessinator' stonden).
2. Vervangt de letter C binnen het woord 'DCOD' zelf door een kleine
   inline SVG met dezelfde concentrische bogen, zodat het woord niet
   meer als 'DOOD' leesbaar is -- de C zelf draagt nu het motief.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_logo_c_inline.py
Maakt automatisch een timestamped .bak van templates/index.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/index.html")

OLD_LOGOMARK = '''      <div class="logo-mark" aria-hidden="true">
        <svg width="29" height="29" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M25.96,24.36 A13,13 0 1,1 25.96,7.64" stroke="#C38D96" stroke-width="2.6" stroke-linecap="round"/>
          <path d="M23.28,22.11 A9.5,9.5 0 1,1 23.28,9.89" stroke="#A7C58E" stroke-width="2.6" stroke-linecap="round"/>
          <path d="M20.6,19.86 A6,6 0 1,1 20.6,12.14" stroke="#6f8a4e" stroke-width="2.6" stroke-linecap="round"/>
        </svg>
      </div>
'''
NEW_LOGOMARK = ''

OLD_NAME = '''<div class="name"><b>DCOD</b> Dessinator<span class="tm">™</span></div>'''
NEW_NAME = '''<div class="name"><b>D</b><svg class="logo-c" width="14" height="14" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M25.96,24.36 A13,13 0 1,1 25.96,7.64" stroke="#C38D96" stroke-width="4.2" stroke-linecap="round"/><path d="M20.6,19.86 A6,6 0 1,1 20.6,12.14" stroke="#6f8a4e" stroke-width="4.2" stroke-linecap="round"/></svg><b>OD</b> Dessinator<span class="tm">™</span></div>'''

CSS_ANKER = ".brand-text .name .tm{font-size:11px;vertical-align:super;color:var(--green);font-weight:600;}"
CSS_TOEVOEGING = CSS_ANKER + "\n.name .logo-c{display:inline-block;vertical-align:-1px;margin:0 1px;}"


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    problemen = []
    if content.count(OLD_LOGOMARK) != 1:
        problemen.append(f"logo-mark blok: {content.count(OLD_LOGOMARK)}x gevonden, verwacht 1x")
    if content.count(OLD_NAME) != 1:
        problemen.append(f".name regel: {content.count(OLD_NAME)}x gevonden, verwacht 1x")
    if content.count(CSS_ANKER) != 1:
        problemen.append(f"CSS-ankerregel: {content.count(CSS_ANKER)}x gevonden, verwacht 1x")

    if problemen:
        print("FOUT: onverwachte inhoud gevonden, stop voor de veiligheid:")
        for p in problemen:
            print(f"  - {p}")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"index.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD_LOGOMARK, NEW_LOGOMARK)
    new_content = new_content.replace(OLD_NAME, NEW_NAME)
    new_content = new_content.replace(CSS_ANKER, CSS_TOEVOEGING)
    TARGET.write_text(new_content, encoding="utf-8")

    print("index.html aangepast: los icoontje verwijderd, C in 'DCOD' is nu inline SVG")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "logo-c" templates/index.html   (verwacht: 3)')
    print('  grep -c "logo-mark" templates/index.html   (verwacht: 1, alleen nog de CSS-regel)')


if __name__ == "__main__":
    main()
