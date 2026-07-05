#!/usr/bin/env python3
"""
Twee dingen in templates/index.html:
1. De 7 subknoppen (3x Art Deco/Neo Deco, 4x Japandi) geven zichzelf nu
   mee aan setPrompt() als tweede argument ('this'), zodat de JS-kant weet
   welke knop is aangeklikt.
2. Nieuwe CSS-regel .chip.sub-active met een lichtere kleur dan de
   standaard subknop-kleur, zodat de aangeklikte variant duidelijk opvalt.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_subknop_active_html.py
Maakt automatisch een timestamped .bak van templates/index.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/index.html")

# (label, oude regel, nieuwe regel)
KNOP_VERVANGINGEN = [
    (
        "Waaier",
        '''<button class="chip adeco-sub" onclick="setPrompt('Art Deco waaier, goud en zwart, jaren 20 stijl')">Waaier</button>''',
        '''<button class="chip adeco-sub" onclick="setPrompt('Art Deco waaier, goud en zwart, jaren 20 stijl', this)">Waaier</button>''',
    ),
    (
        "Zonnestralen",
        '''<button class="chip adeco-sub" onclick="setPrompt('Art Deco zonnestralen, goud en zwart, jaren 20 stijl')">Zonnestralen</button>''',
        '''<button class="chip adeco-sub" onclick="setPrompt('Art Deco zonnestralen, goud en zwart, jaren 20 stijl', this)">Zonnestralen</button>''',
    ),
    (
        "Honingraat",
        '''<button class="chip adeco-sub" onclick="setPrompt('Art Deco hexagon honingraat, goud en zwart, jaren 20 stijl')">Honingraat</button>''',
        '''<button class="chip adeco-sub" onclick="setPrompt('Art Deco hexagon honingraat, goud en zwart, jaren 20 stijl', this)">Honingraat</button>''',
    ),
    (
        "River Stones",
        '''<button class="chip" onclick="setPrompt('Japandi variant: river_stones')">River Stones</button>''',
        '''<button class="chip" onclick="setPrompt('Japandi variant: river_stones', this)">River Stones</button>''',
    ),
    (
        "Stroming",
        '''<button class="chip" onclick="setPrompt('Japandi variant: stroming')">Stroming</button>''',
        '''<button class="chip" onclick="setPrompt('Japandi variant: stroming', this)">Stroming</button>''',
    ),
    (
        "Organic Leaves",
        '''<button class="chip" onclick="setPrompt('Japandi variant: organic_leaves')">Organic Leaves</button>''',
        '''<button class="chip" onclick="setPrompt('Japandi variant: organic_leaves', this)">Organic Leaves</button>''',
    ),
    (
        "Golven",
        '''<button class="chip" onclick="setPrompt('Japandi variant: golven')">Golven</button>''',
        '''<button class="chip" onclick="setPrompt('Japandi variant: golven', this)">Golven</button>''',
    ),
]

CSS_ANKER = '''#artdecoSub .chip:hover{background:#B9D4A6 !important;}'''
CSS_TOEVOEGING = '''#artdecoSub .chip:hover{background:#B9D4A6 !important;}
.chip.sub-active{background:#D9ECC9 !important;border:2px solid #4C7A3A !important;color:#0E2117 !important;font-weight:700;}'''


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    if "sub-active" in content:
        print("FOUT: 'sub-active' komt al voor in index.html. Stop om dubbele toepassing te voorkomen.")
        sys.exit(1)

    problemen = []
    for label, oud, nieuw in KNOP_VERVANGINGEN:
        n = content.count(oud)
        if n != 1:
            problemen.append(f"{label}: {n}x gevonden, verwacht 1x")
    if content.count(CSS_ANKER) != 1:
        problemen.append(f"CSS-ankerregel: {content.count(CSS_ANKER)}x gevonden, verwacht 1x")

    if problemen:
        print("FOUT: onverwachte inhoud gevonden, stop voor de veiligheid:")
        for p in problemen:
            print(f"  - {p}")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"index.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content
    for label, oud, nieuw in KNOP_VERVANGINGEN:
        new_content = new_content.replace(oud, nieuw)
        print(f"Bijgewerkt: {label}")
    new_content = new_content.replace(CSS_ANKER, CSS_TOEVOEGING)
    print("CSS .chip.sub-active toegevoegd")

    TARGET.write_text(new_content, encoding="utf-8")
    print(f"Oude grootte: {backup.stat().st_size} bytes")
    print(f"Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c ", this)" templates/index.html   (verwacht: 7)')
    print('  grep -c "sub-active" templates/index.html   (verwacht: 2)')


if __name__ == "__main__":
    main()
