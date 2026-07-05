#!/usr/bin/env python3
"""
Verwijdert het hele '.brief'-blok (zoekveld + 'Ontwikkel vloerconcept ->'
knop) uit alle vier de projectpanelen op /inspiratie. Dit voorkomt dat de
pagina een vrije-tekst-invoer suggereert die nog niet werkt/aangesloten is.
De conceptkaarten blijven de enige (werkende) ingang.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_remove_brief.py
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import re
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/inspiratie.html")

PATTERN = re.compile(
    r'\s*<div class="brief">\s*'
    r'<span class="brief-label">Vertel iets over uw project</span>\s*'
    r'<div class="brief-row">\s*'
    r'<input[^>]*>\s*'
    r'<button class="brief-btn" onclick="startConcept\(\'[^\']*\'\)">Ontwikkel vloerconcept →</button>\s*'
    r'</div>\s*'
    r'</div>',
    re.DOTALL,
)

VERWACHT = 4


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    matches = PATTERN.findall(content)
    gevonden = len(PATTERN.findall(content))
    if gevonden != VERWACHT:
        print(f"FOUT: {gevonden}x brief-blok gevonden, verwacht {VERWACHT}x. Stop voor de veiligheid.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"inspiratie.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = PATTERN.sub("", content)
    TARGET.write_text(new_content, encoding="utf-8")
    print(f"{VERWACHT}x brief-blok (zoekveld + knop) verwijderd")
    print(f"Oude grootte: {backup.stat().st_size} bytes")
    print(f"Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "brief-row" templates/inspiratie.html   (verwacht: 0)')
    print('  grep -c "Vertel iets over uw project" templates/inspiratie.html   (verwacht: 0)')


if __name__ == "__main__":
    main()
