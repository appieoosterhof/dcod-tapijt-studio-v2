#!/usr/bin/env python3
"""
Haalt de 4 base64-ingebakken projectfoto's (Werkplekken, Hotels, Overheid,
Musea) uit templates/inspiratie.html, slaat ze op als losse JPG/PNG-bestanden
in static/img/projecten/, en vervangt de enorme data:image;base64,... teksten
door korte src="/static/img/projecten/..." paden.

Dit maakt het bestand drastisch kleiner en toekomstige foto-vervangingen simpel.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_extract_project_photos.py
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import re
import shutil
import datetime
import sys
import base64
from pathlib import Path

TARGET = Path("templates/inspiratie.html")
OUT_DIR = Path("static/img/projecten")

PATTERN = re.compile(r'src="data:image/(jpeg|jpg|png);base64,([A-Za-z0-9+/=]+)"')


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    matches = list(PATTERN.finditer(content))

    if not matches:
        print("FOUT: geen data:image;base64 blokken gevonden. Mogelijk al eerder uitgevoerd?")
        sys.exit(1)

    print(f"{len(matches)} ingebakken afbeelding(en) gevonden.")

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"inspiratie.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    nieuwe_content = content
    for i, m in enumerate(matches, start=1):
        ext = "jpg" if m.group(1) in ("jpeg", "jpg") else "png"
        data = m.group(2)
        try:
            raw = base64.b64decode(data)
        except Exception as e:
            print(f"FOUT bij decoderen van afbeelding {i}: {e}")
            sys.exit(1)

        filename = f"project_{i}.{ext}"
        out_path = OUT_DIR / filename
        out_path.write_bytes(raw)
        size_kb = out_path.stat().st_size / 1024
        print(f"  Afbeelding {i}: opgeslagen als {out_path} ({size_kb:.0f} KB)")

        oude_src = m.group(0)
        nieuwe_src = f'src="/static/img/projecten/{filename}"'
        # Vervang precies deze ene voorkomen (via string replace op het volledige
        # gevonden blok, dat uniek genoeg is door de lange data-inhoud)
        nieuwe_content = nieuwe_content.replace(oude_src, nieuwe_src, 1)

    TARGET.write_text(nieuwe_content, encoding="utf-8")
    print()
    print(f"Oude grootte: {backup.stat().st_size} bytes")
    print(f"Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "data:image" templates/inspiratie.html   (verwacht: 0)')
    print('  ls -la static/img/projecten/')
    print()
    print("Open elk bestand om te zien welk project bij welk nummer hoort, bv.:")
    print("  open static/img/projecten/project_1.jpg")


if __name__ == "__main__":
    main()
