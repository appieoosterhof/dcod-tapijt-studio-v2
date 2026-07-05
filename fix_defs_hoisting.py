#!/usr/bin/env python3
"""
Kleine, veilige uitbreiding van build_tile_svg() en build_repeat_svg():
als een tegel een <defs>...</defs> blok bevat (zoals bij een ingebedde
foto), wordt dat blok EENMALIG naar de buitenste <defs> verplaatst in
plaats van bij elke herhaalde kopie gedupliceerd. Voor alle bestaande
dessins (die geen <defs> in hun tegel hebben) verandert er niets -- dus
geen risico voor de andere dessins.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_defs_hoisting.py
Maakt automatisch een timestamped .bak van app.py
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("app.py")

# ---- build_tile_svg: n x n motief-schaal tiling ----
OLD_TILE = '''    if n > 1:
        kopieen = []
        for iy in range(n):
            for ix in range(n):
                kopieen.append(f'<g transform="translate({ix * g},{iy * g})">{inner}</g>')
        inner = "".join(kopieen)
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TEGEL} {TEGEL}"
     width="{TEGEL}" height="{TEGEL}">
  <rect width="{TEGEL}" height="{TEGEL}" fill="{palette['background']}"/>
  {inner}
</svg>"""'''

NEW_TILE = '''    _defs_content = ""
    if "<defs>" in inner and "</defs>" in inner:
        _d_start = inner.index("<defs>")
        _d_end = inner.index("</defs>") + len("</defs>")
        _defs_content = inner[_d_start + len("<defs>"):_d_end - len("</defs>")]
        inner = inner[:_d_start] + inner[_d_end:]
    if n > 1:
        kopieen = []
        for iy in range(n):
            for ix in range(n):
                kopieen.append(f'<g transform="translate({ix * g},{iy * g})">{inner}</g>')
        inner = "".join(kopieen)
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TEGEL} {TEGEL}"
     width="{TEGEL}" height="{TEGEL}">
  <defs>{_defs_content}</defs>
  <rect width="{TEGEL}" height="{TEGEL}" fill="{palette['background']}"/>
  {inner}
</svg>"""'''

# ---- build_repeat_svg: all-over repeat tiling ----
OLD_REPEAT = '''    inner_start = tile_svg.index(">", tile_svg.index("<svg")) + 1
    inner_end = tile_svg.rindex("</svg>")
    inner_content = tile_svg[inner_start:inner_end].strip()

    tiles = []'''

NEW_REPEAT = '''    inner_start = tile_svg.index(">", tile_svg.index("<svg")) + 1
    inner_end = tile_svg.rindex("</svg>")
    inner_content = tile_svg[inner_start:inner_end].strip()

    repeat_defs_content = ""
    if "<defs>" in inner_content and "</defs>" in inner_content:
        _rd_start = inner_content.index("<defs>")
        _rd_end = inner_content.index("</defs>") + len("</defs>")
        repeat_defs_content = inner_content[_rd_start + len("<defs>"):_rd_end - len("</defs>")]
        inner_content = inner_content[:_rd_start] + inner_content[_rd_end:]

    tiles = []'''

OLD_REPEAT_SVG_OUTPUT = '''  <defs>
    <clipPath id="canvas"><rect width="{total_w}" height="{total_h}"/></clipPath>
    {"".join(clip_defs)}
  </defs>'''

NEW_REPEAT_SVG_OUTPUT = '''  <defs>
    <clipPath id="canvas"><rect width="{total_w}" height="{total_h}"/></clipPath>
    {"".join(clip_defs)}
    {repeat_defs_content}
  </defs>'''


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    if "_defs_content" in content or "repeat_defs_content" in content:
        print("FOUT: defs-hoisting lijkt al aanwezig. Stop om dubbele toepassing te voorkomen.")
        sys.exit(1)

    problemen = []
    for naam, old in [("build_tile_svg-blok", OLD_TILE), ("build_repeat_svg-extractie", OLD_REPEAT), ("build_repeat_svg-output", OLD_REPEAT_SVG_OUTPUT)]:
        n = content.count(old)
        if n != 1:
            problemen.append(f"{naam}: {n}x gevonden, verwacht 1x")

    if problemen:
        print("FOUT: onverwachte inhoud gevonden, stop voor de veiligheid:")
        for p in problemen:
            print(f"  - {p}")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"app.py.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD_TILE, NEW_TILE, 1)
    new_content = new_content.replace(OLD_REPEAT, NEW_REPEAT, 1)
    new_content = new_content.replace(OLD_REPEAT_SVG_OUTPUT, NEW_REPEAT_SVG_OUTPUT, 1)
    TARGET.write_text(new_content, encoding="utf-8")

    print("app.py aangepast: defs-hoisting toegevoegd aan build_tile_svg en build_repeat_svg")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  python3 -c "import app"')


if __name__ == "__main__":
    main()
