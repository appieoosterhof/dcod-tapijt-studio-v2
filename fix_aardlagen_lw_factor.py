#!/usr/bin/env python3
"""
Voegt een instelbare lijndikte-factor toe aan generate_aardlagen_svg.
Standaard 1.0 (ongewijzigd gedrag) tenzij palette["_al_lw_factor"] is gezet.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_aardlagen_lw_factor.py
Maakt automatisch een timestamped .bak van modules_extra.py
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("modules_extra.py")

OLD = """    tile_cm = 40
    if isinstance(palette, dict):
        try:
            tile_cm = int(palette.get("_tile_cm", 40))
        except (TypeError, ValueError):
            tile_cm = 40
    lw = max(0.5, 3.0 / (tile_cm / 40.0))"""

NEW = """    tile_cm = 40
    if isinstance(palette, dict):
        try:
            tile_cm = int(palette.get("_tile_cm", 40))
        except (TypeError, ValueError):
            tile_cm = 40
    lw_factor = 1.0
    if isinstance(palette, dict):
        try:
            lw_factor = float(palette.get("_al_lw_factor", 1.0))
        except (TypeError, ValueError):
            lw_factor = 1.0
    lw_factor = max(0.3, min(3.0, lw_factor))
    lw = max(0.5, 3.0 / (tile_cm / 40.0)) * lw_factor"""


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    count = content.count(OLD)
    if count == 0:
        print("FOUT: de verwachte oude regels zijn niet (exact) gevonden.")
        sys.exit(1)
    if count > 1:
        print(f"FOUT: de oude regels komen {count}x voor, verwacht precies 1x. Stop voor de veiligheid.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"modules_extra.py.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD, NEW)
    TARGET.write_text(new_content, encoding="utf-8")
    print("modules_extra.py aangepast: generate_aardlagen_svg ondersteunt nu _al_lw_factor")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -n "_al_lw_factor" modules_extra.py')


if __name__ == "__main__":
    main()
