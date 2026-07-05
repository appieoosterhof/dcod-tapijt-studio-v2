#!/usr/bin/env python3
"""
Voegt generate_botanisch_master_svg() toe aan modules_extra.py. Deze
functie genereert GEEN nieuw patroon: hij embed het aangeleverde
master-repeatbestand (static/img/dessins/botanisch_master.jpg) direct als
<image> in een SVG. Geen procedurale opbouw, geen rotatie, geen spiegeling,
geen willekeur -- uitsluitend het bestand zelf, op de juiste schaal.

Append-only (voegt toe aan het einde van het bestand), dus geen ankerpunt
nodig en geen risico op conflicten met bestaande code.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_add_botanisch_master_generator.py
Maakt automatisch een timestamped .bak van modules_extra.py
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("modules_extra.py")

TOEVOEGING = '''

# =====================================================================
#  BOTANISCH (MASTER REPEAT) -- embed een aangeleverd, kant-en-klaar
#  naadloos repeatbestand (geen procedurale generatie, geen AI, geen
#  willekeur). Ondersteunt toekomstige "asset-generator" collecties op
#  dezelfde manier: nieuw bestand -> pad aanpassen -> klaar.
# =====================================================================
import base64 as _botmaster_base64
import os as _botmaster_os

_BOTANISCH_MASTER_PAD = _botmaster_os.path.join(
    _botmaster_os.path.dirname(_botmaster_os.path.abspath(__file__)),
    "static", "img", "dessins", "botanisch_master.jpg"
)
_BOTANISCH_MASTER_B64_CACHE = None


def _botanisch_master_b64():
    global _BOTANISCH_MASTER_B64_CACHE
    if _BOTANISCH_MASTER_B64_CACHE is None:
        with open(_BOTANISCH_MASTER_PAD, "rb") as f:
            _BOTANISCH_MASTER_B64_CACHE = _botmaster_base64.b64encode(f.read()).decode("ascii")
    return _BOTANISCH_MASTER_B64_CACHE


def generate_botanisch_master_svg(palette, tile_size, complexity):
    """Embed het aangeleverde Botanisch master-repeatbestand als SVG-tegel.
    Geen re-generatie, geen blending, geen rotatie/spiegeling, originele
    kleuren en schaal behouden."""
    T = int(tile_size)
    b64 = _botanisch_master_b64()
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {T} {T}" '
        f'width="{T}" height="{T}">'
        f'<defs><image id="botMaster" '
        f'href="data:image/jpeg;base64,{b64}" '
        f'width="{T}" height="{T}" preserveAspectRatio="xMidYMid slice"/></defs>'
        f'<use href="#botMaster"/>'
        f'</svg>'
    )
'''


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    if "generate_botanisch_master_svg" in content:
        print("FOUT: generate_botanisch_master_svg bestaat al. Stop om dubbele registratie te voorkomen.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"modules_extra.py.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    with open(TARGET, "a", encoding="utf-8") as f:
        f.write(TOEVOEGING)

    print("modules_extra.py aangepast: generate_botanisch_master_svg toegevoegd (append)")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "generate_botanisch_master_svg" modules_extra.py')
    print('  python3 -c "import modules_extra"')


if __name__ == "__main__":
    main()
