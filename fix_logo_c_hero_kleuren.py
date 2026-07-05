#!/usr/bin/env python3
"""
Twee aanpassingen aan de hero-C op /inspiratie:
1. Groter: 0.62em -> 0.88em
2. Drie ringen met eigen kleur i.p.v. currentColor+opacity:
   buiten=lichtgroen (#A7C58E), midden=roze (#C38D96), binnen=licht
   grijsgroen (#D5E0DF)

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_logo_c_hero_kleuren.py
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/inspiratie.html")

OLD_SVG = '''<svg class="logo-c-hero" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M25.96,24.36 A13,13 0 1,1 25.96,7.64" stroke="currentColor" stroke-width="4.2" stroke-linecap="round" opacity="0.85"/><path d="M20.6,19.86 A6,6 0 1,1 20.6,12.14" stroke="currentColor" stroke-width="4.2" stroke-linecap="round" opacity="0.55"/></svg>'''
NEW_SVG = '''<svg class="logo-c-hero" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M25.96,24.36 A13,13 0 1,1 25.96,7.64" stroke="#A7C58E" stroke-width="4.2" stroke-linecap="round"/><path d="M23.28,22.11 A9.5,9.5 0 1,1 23.28,9.89" stroke="#C38D96" stroke-width="4.2" stroke-linecap="round"/><path d="M20.6,19.86 A6,6 0 1,1 20.6,12.14" stroke="#D5E0DF" stroke-width="4.2" stroke-linecap="round"/></svg>'''

OLD_CSS = ".logo-c-hero{width:0.62em;height:0.62em;display:inline-block;vertical-align:-0.04em;margin:0 0.01em;color:inherit}"
NEW_CSS = ".logo-c-hero{width:0.88em;height:0.88em;display:inline-block;vertical-align:-0.09em;margin:0 0.02em;color:inherit}"


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    problemen = []
    if content.count(OLD_SVG) != 1:
        problemen.append(f"SVG-regel: {content.count(OLD_SVG)}x gevonden, verwacht 1x")
    if content.count(OLD_CSS) != 1:
        problemen.append(f"CSS-regel: {content.count(OLD_CSS)}x gevonden, verwacht 1x")

    if problemen:
        print("FOUT: onverwachte inhoud gevonden, stop voor de veiligheid:")
        for p in problemen:
            print(f"  - {p}")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"inspiratie.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD_SVG, NEW_SVG)
    new_content = new_content.replace(OLD_CSS, NEW_CSS)
    TARGET.write_text(new_content, encoding="utf-8")

    print("inspiratie.html aangepast: hero-C is groter en heeft nu 3 eigen kleuren")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "A7C58E.*C38D96\\|logo-c-hero" templates/inspiratie.html')


if __name__ == "__main__":
    main()
