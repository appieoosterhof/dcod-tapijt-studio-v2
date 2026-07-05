#!/usr/bin/env python3
"""
Vervangt de cc-mini placeholders/oude foto's door de nieuwste geleverde
dessin-foto's voor: Aardlagen, Vrije vormen, Neo Bauhaus, Weefstructuren.
(Japandi, Hoogtelijnen, Urban Plaid hadden al foto's en blijven ongewijzigd
in dit script, want hun bestandsnamen/src blijven identiek.)

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_meer_thumbnails.py
Vereist dat static/img/inspiratie/{aardlagen,vrije_vormen,neo_bauhaus,weefstructuren}.jpg
al gekopieerd zijn.
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/inspiratie.html")

# (naam, oude cc-mini HTML, nieuwe cc-mini HTML, verwacht aantal voorkomens)
VERVANGINGEN = [
    (
        "Aardlagen",
        '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#6f8a4e"></div><div class="cc-band" style="background:#b7a06a"></div><div class="cc-band" style="background:#e6d9b8"></div></div><svg class="cc-acc" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 18 C 25 12, 50 24, 100 15" fill="none" stroke="#e6d9b8" stroke-width="0.9" opacity="0.55"/><path d="M0 31 C 25 25, 50 37, 100 28" fill="none" stroke="#e6d9b8" stroke-width="0.9" opacity="0.55"/><path d="M0 44 C 25 38, 50 50, 100 41" fill="none" stroke="#e6d9b8" stroke-width="0.9" opacity="0.55"/><path d="M0 57 C 25 51, 50 63, 100 54" fill="none" stroke="#e6d9b8" stroke-width="0.9" opacity="0.55"/><path d="M0 70 C 25 64, 50 76, 100 67" fill="none" stroke="#e6d9b8" stroke-width="0.9" opacity="0.55"/><path d="M0 83 C 25 77, 50 89, 100 80" fill="none" stroke="#e6d9b8" stroke-width="0.9" opacity="0.55"/></svg></div>',
        '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/aardlagen.jpg" alt="Aardlagen" loading="lazy"></div>',
        4,
    ),
    (
        "Weefstructuren",
        '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#b89a6a"></div><div class="cc-band" style="background:#8a6a4e"></div><div class="cc-band" style="background:#e6ddc8"></div></div><svg class="cc-acc" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><line x1="0" y1="8" x2="100" y2="8" stroke="#e6ddc8" stroke-width="3" opacity="0.25"/><line x1="0" y1="22" x2="100" y2="22" stroke="#e6ddc8" stroke-width="3" opacity="0.25"/><line x1="0" y1="36" x2="100" y2="36" stroke="#e6ddc8" stroke-width="3" opacity="0.25"/><line x1="0" y1="50" x2="100" y2="50" stroke="#e6ddc8" stroke-width="3" opacity="0.25"/><line x1="8" y1="0" x2="8" y2="100" stroke="#e6ddc8" stroke-width="3" opacity="0.18"/><line x1="22" y1="0" x2="22" y2="100" stroke="#e6ddc8" stroke-width="3" opacity="0.18"/><line x1="36" y1="0" x2="36" y2="100" stroke="#e6ddc8" stroke-width="3" opacity="0.18"/></svg></div>',
        '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/weefstructuren.jpg" alt="Weefstructuren" loading="lazy"></div>',
        2,
    ),
    (
        "Neo Bauhaus",
        '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#1a1a1a"></div><div class="cc-band" style="background:#d4622a"></div><div class="cc-band" style="background:#4a4a4a"></div></div></div>',
        '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/neo_bauhaus.jpg" alt="Neo Bauhaus" loading="lazy"></div>',
        4,
    ),
    (
        "Vrije vormen",
        '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#6f8a4e"></div><div class="cc-band" style="background:#C9A24A"></div><div class="cc-band" style="background:#F5F1E8"></div></div></div>',
        '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/vrije_vormen.jpg" alt="Vrije vormen" loading="lazy"></div>',
        2,
    ),
]


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    problemen = []
    for naam, old, new, verwacht in VERVANGINGEN:
        gevonden = content.count(old)
        if gevonden != verwacht:
            problemen.append(f"{naam}: {gevonden}x gevonden, verwacht {verwacht}x")

    if problemen:
        print("FOUT: onverwachte inhoud gevonden, stop voor de veiligheid:")
        for p in problemen:
            print(f"  - {p}")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"inspiratie.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content
    for naam, old, new, verwacht in VERVANGINGEN:
        new_content = new_content.replace(old, new)
        print(f"{naam}: {verwacht}x vervangen door foto-thumbnail")

    TARGET.write_text(new_content, encoding="utf-8")
    print(f"Oude grootte: {backup.stat().st_size} bytes")
    print(f"Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "cc-photo" templates/inspiratie.html')


if __name__ == "__main__":
    main()
