#!/usr/bin/env python3
"""
Vervangt de letter C in de hero-titel "DCOD Dessinator" op /inspiratie
door dezelfde concentrische-bogen-C als in de Dessinator zelf, maar
geschaald met em-eenheden zodat hij meegroeit met de responsive
lettergrootte (clamp(40px,6vw,70px)).

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_logo_c_inline_hero.py
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/inspiratie.html")

OLD_H1 = '''<h1 class="studio-title">DCOD Dessinator <sup class="tm">™</sup></h1>'''
NEW_H1 = '''<h1 class="studio-title">D<svg class="logo-c-hero" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M25.96,24.36 A13,13 0 1,1 25.96,7.64" stroke="currentColor" stroke-width="4.2" stroke-linecap="round" opacity="0.85"/><path d="M20.6,19.86 A6,6 0 1,1 20.6,12.14" stroke="currentColor" stroke-width="4.2" stroke-linecap="round" opacity="0.55"/></svg>OD Dessinator <sup class="tm">™</sup></h1>'''

CSS_ANKER = ".hero h1{font-family:'Fraunces';font-weight:400;font-size:clamp(40px,6vw,70px);line-height:1.04;letter-spacing:-.015em;margin:0 auto}"
CSS_TOEVOEGING = CSS_ANKER + "\n.logo-c-hero{width:0.62em;height:0.62em;display:inline-block;vertical-align:-0.04em;margin:0 0.01em;color:inherit}"


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    problemen = []
    if content.count(OLD_H1) != 1:
        problemen.append(f"h1-regel: {content.count(OLD_H1)}x gevonden, verwacht 1x")
    if content.count(CSS_ANKER) != 1:
        problemen.append(f"CSS-ankerregel: {content.count(CSS_ANKER)}x gevonden, verwacht 1x")

    if problemen:
        print("FOUT: onverwachte inhoud gevonden, stop voor de veiligheid:")
        for p in problemen:
            print(f"  - {p}")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"inspiratie.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD_H1, NEW_H1)
    new_content = new_content.replace(CSS_ANKER, CSS_TOEVOEGING)
    TARGET.write_text(new_content, encoding="utf-8")

    print("inspiratie.html aangepast: hero-titel C is nu inline SVG (em-geschaald)")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "logo-c-hero" templates/inspiratie.html')


if __name__ == "__main__":
    main()
