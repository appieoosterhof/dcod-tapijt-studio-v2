#!/usr/bin/env python3
"""
Vervangt de placeholder cc-mini (kleurbanden + SVG-lijntjes) door echte
dessin-foto's voor de conceptkaarten Urban Plaid, Japandi en Lijnenspel
op /inspiratie.

Vereist: static/img/inspiratie/urban_plaid.jpg, japandi.jpg, lijnenspel.jpg
         (kopieer deze eerst vanuit ~/Downloads/inspiratie_thumbs/)

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_cc_thumbnails.py
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/inspiratie.html")

# (conceptnaam, oude cc-mini HTML, nieuwe cc-mini HTML, verwacht aantal voorkomens)
REPLACEMENTS = [
    (
        "Urban Plaid",
        '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#c38d96"></div><div class="cc-band" style="background:#b5734e"></div><div class="cc-band" style="background:#e8d5c0"></div></div><svg class="cc-acc" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><line x1="14" y1="0" x2="14" y2="100" stroke="#e8d5c0" stroke-width="1.2" opacity="0.45"/><line x1="34" y1="0" x2="34" y2="100" stroke="#e8d5c0" stroke-width="1.2" opacity="0.45"/><line x1="54" y1="0" x2="54" y2="100" stroke="#e8d5c0" stroke-width="1.2" opacity="0.45"/><line x1="74" y1="0" x2="74" y2="100" stroke="#e8d5c0" stroke-width="1.2" opacity="0.45"/><line x1="94" y1="0" x2="94" y2="100" stroke="#e8d5c0" stroke-width="1.2" opacity="0.45"/><line x1="0" y1="14" x2="100" y2="14" stroke="#e8d5c0" stroke-width="1.2" opacity="0.45"/><line x1="0" y1="34" x2="100" y2="34" stroke="#e8d5c0" stroke-width="1.2" opacity="0.45"/><line x1="0" y1="54" x2="100" y2="54" stroke="#e8d5c0" stroke-width="1.2" opacity="0.45"/><line x1="0" y1="74" x2="100" y2="74" stroke="#e8d5c0" stroke-width="1.2" opacity="0.45"/><line x1="0" y1="94" x2="100" y2="94" stroke="#e8d5c0" stroke-width="1.2" opacity="0.45"/></svg></div>',
        '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/urban_plaid.jpg" alt="Urban Plaid" loading="lazy"></div>',
        2,
    ),
    (
        "Japandi",
        '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#8D9971"></div><div class="cc-band" style="background:#B5C49F"></div><div class="cc-band" style="background:#e6d9b8"></div></div><svg class="cc-acc" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><ellipse cx="20" cy="25" rx="13" ry="9" fill="#e6d9b8" opacity="0.28"/><ellipse cx="50" cy="25" rx="13" ry="9" fill="#e6d9b8" opacity="0.28"/><ellipse cx="80" cy="25" rx="13" ry="9" fill="#e6d9b8" opacity="0.28"/><ellipse cx="20" cy="55" rx="13" ry="9" fill="#e6d9b8" opacity="0.28"/><ellipse cx="50" cy="55" rx="13" ry="9" fill="#e6d9b8" opacity="0.28"/><ellipse cx="80" cy="55" rx="13" ry="9" fill="#e6d9b8" opacity="0.28"/><ellipse cx="20" cy="85" rx="13" ry="9" fill="#e6d9b8" opacity="0.28"/><ellipse cx="50" cy="85" rx="13" ry="9" fill="#e6d9b8" opacity="0.28"/><ellipse cx="80" cy="85" rx="13" ry="9" fill="#e6d9b8" opacity="0.28"/></svg></div>',
        '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/japandi.jpg" alt="Japandi" loading="lazy"></div>',
        1,
    ),
    (
        "Lijnenspel",
        '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#003614"></div><div class="cc-band" style="background:#A7C58E"></div><div class="cc-band" style="background:#EFE6CF"></div></div><svg class="cc-acc" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><line x1="0" y1="14" x2="100" y2="0" stroke="#EFE6CF" stroke-width="1" opacity="0.5"/><line x1="0" y1="23" x2="100" y2="9" stroke="#EFE6CF" stroke-width="1" opacity="0.5"/><line x1="0" y1="32" x2="100" y2="18" stroke="#EFE6CF" stroke-width="1" opacity="0.5"/><line x1="0" y1="41" x2="100" y2="27" stroke="#EFE6CF" stroke-width="1" opacity="0.5"/><line x1="0" y1="50" x2="100" y2="36" stroke="#EFE6CF" stroke-width="1" opacity="0.5"/><line x1="0" y1="59" x2="100" y2="45" stroke="#EFE6CF" stroke-width="1" opacity="0.5"/><line x1="0" y1="68" x2="100" y2="54" stroke="#EFE6CF" stroke-width="1" opacity="0.5"/><line x1="0" y1="77" x2="100" y2="63" stroke="#EFE6CF" stroke-width="1" opacity="0.5"/><line x1="0" y1="86" x2="100" y2="72" stroke="#EFE6CF" stroke-width="1" opacity="0.5"/><line x1="0" y1="95" x2="100" y2="81" stroke="#EFE6CF" stroke-width="1" opacity="0.5"/><line x1="0" y1="104" x2="100" y2="90" stroke="#EFE6CF" stroke-width="1" opacity="0.5"/><line x1="0" y1="113" x2="100" y2="99" stroke="#EFE6CF" stroke-width="1" opacity="0.5"/></svg></div>',
        '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/lijnenspel.jpg" alt="Lijnenspel" loading="lazy"></div>',
        2,
    ),
]

CSS_OLD = ".cc-acc{position:absolute;inset:0;width:100%;height:100%;mix-blend-mode:soft-light}"
CSS_NEW = CSS_OLD + ".cc-photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}"


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    # Voorcontrole: alle blokken moeten met het verwachte aantal voorkomen
    problems = []
    if content.count(CSS_OLD) != 1:
        problems.append(f"CSS-regel .cc-acc komt {content.count(CSS_OLD)}x voor, verwacht 1x")
    for naam, old, new, verwacht in REPLACEMENTS:
        gevonden = content.count(old)
        if gevonden != verwacht:
            problems.append(f"{naam}: {gevonden}x gevonden, verwacht {verwacht}x")

    if problems:
        print("FOUT: onverwachte inhoud gevonden, stop voor de veiligheid:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"inspiratie.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(CSS_OLD, CSS_NEW)
    for naam, old, new, verwacht in REPLACEMENTS:
        new_content = new_content.replace(old, new)
        print(f"{naam}: {verwacht}x vervangen door foto-thumbnail")

    TARGET.write_text(new_content, encoding="utf-8")

    old_size = backup.stat().st_size
    new_size = TARGET.stat().st_size
    print(f"Oude grootte: {old_size} bytes")
    print(f"Nieuwe grootte: {new_size} bytes")
    print("Fix toegepast op templates/inspiratie.html")
    print()
    print("Controleer met:")
    print('  grep -c "cc-photo" templates/inspiratie.html   (verwacht: 5)')


if __name__ == "__main__":
    main()
