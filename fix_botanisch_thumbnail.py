#!/usr/bin/env python3
"""
Vervangt de Botanisch cc-mini placeholder (kleurbanden + ellipse-SVG) door de
echte dessin-foto op /inspiratie (komt voor in Musea & Bibliotheken en
Hotels & Hospitality).

Vereist: static/img/inspiratie/botanisch.jpg
         (kopieer eerst vanuit ~/Downloads/)

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_botanisch_thumbnail.py
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/inspiratie.html")

OLD = '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#C9A24A"></div><div class="cc-band" style="background:#a03d5d"></div><div class="cc-band" style="background:#4e7a4e"></div></div><svg class="cc-acc" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><ellipse cx="18" cy="22" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="40" cy="22" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="62" cy="22" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="84" cy="22" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="18" cy="48" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="40" cy="48" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="62" cy="48" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="84" cy="48" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/></svg></div>'
NEW = '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/botanisch.jpg" alt="Botanisch" loading="lazy"></div>'
VERWACHT = 2


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
    print(f"Botanisch: {VERWACHT}x vervangen door foto-thumbnail")
    print(f"Oude grootte: {backup.stat().st_size} bytes")
    print(f"Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "cc-photo" templates/inspiratie.html   (verwacht: 25 = alle 24 kaarten + 1 CSS-regel)')


if __name__ == "__main__":
    main()
