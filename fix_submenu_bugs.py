#!/usr/bin/env python3
"""
Twee fixes in templates/index.html:
1. CSS-specificiteit: .chip.sub-active werd overschaduwd door de sterkere
   #artdecoSub .chip / #japandiSub .chip regels (ID-selector wint altijd
   van class-combinaties). Nieuwe regel krijgt dezelfde ID-scope, dus wint.
2. hideSubmenus() toegevoegd: elke hoofdknop (behalve Art Deco/Japandi
   zelf) sluit nu beide submenu's bij klikken.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_submenu_bugs.py
Maakt automatisch een timestamped .bak van templates/index.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/index.html")

# ---- Fix A: CSS-specificiteit ----
OLD_CSS = ".chip.sub-active{background:#D9ECC9 !important;border:2px solid #4C7A3A !important;color:#0E2117 !important;font-weight:700;}"
NEW_CSS = "#artdecoSub .chip.sub-active,#japandiSub .chip.sub-active{background:#EFE6CF !important;border:2px solid #4C7A3A !important;color:#0E2117 !important;font-weight:700;}"

# ---- Fix B: hoofdknoppen sluiten submenu's ----
KNOP_VERVANGINGEN = [
    (
        "Aardlagen",
        '''<button class="chip" onclick="setPrompt('Aardlagen natuursteen agaat, aardetinten')">Aardlagen</button>''',
        '''<button class="chip" onclick="hideSubmenus(); setPrompt('Aardlagen natuursteen agaat, aardetinten')">Aardlagen</button>''',
    ),
    (
        "Botanisch",
        '''<button class="chip" onclick="setPrompt('Botanisch bloemmotief art nouveau stijl, zachte groene en beige kleuren')">Botanisch</button>''',
        '''<button class="chip" onclick="hideSubmenus(); setPrompt('Botanisch bloemmotief art nouveau stijl, zachte groene en beige kleuren')">Botanisch</button>''',
    ),
    (
        "Neo Bauhaus",
        '''<button class="chip" onclick="setPrompt('Bauhaus geometrisch patroon, halve cirkels driehoeken en ringen, oranje zwart grijs')">Neo Bauhaus</button>''',
        '''<button class="chip" onclick="hideSubmenus(); setPrompt('Bauhaus geometrisch patroon, halve cirkels driehoeken en ringen, oranje zwart grijs')">Neo Bauhaus</button>''',
    ),
    (
        "Hoogtelijnen",
        '''<button class="chip" onclick="setPrompt('hoogtelijnen patroon, style:hoogtelijnen, topografie contourlijnen')">Hoogtelijnen</button>''',
        '''<button class="chip" onclick="hideSubmenus(); setPrompt('hoogtelijnen patroon, style:hoogtelijnen, topografie contourlijnen')">Hoogtelijnen</button>''',
    ),
    (
        "Lijnenspel",
        '''<button class="chip" onclick="setPrompt('Lijnenspel, fijne verticale banen in clusters met horizontale kleurzones op donkere ondergrond')">Lijnenspel</button>''',
        '''<button class="chip" onclick="hideSubmenus(); setPrompt('Lijnenspel, fijne verticale banen in clusters met horizontale kleurzones op donkere ondergrond')">Lijnenspel</button>''',
    ),
    (
        "Urban Plaid",
        '''<button class="chip" onclick="setPrompt('urban plaid tartan ruit patroon, geweven lijnen')">Urban Plaid</button>''',
        '''<button class="chip" onclick="hideSubmenus(); setPrompt('urban plaid tartan ruit patroon, geweven lijnen')">Urban Plaid</button>''',
    ),
    (
        "Vrije vormen",
        '''<button class="chip" onclick="setPrompt('Vrije organische vormen, vloeiend en natuurlijk')">Vrije vormen</button>''',
        '''<button class="chip" onclick="hideSubmenus(); setPrompt('Vrije organische vormen, vloeiend en natuurlijk')">Vrije vormen</button>''',
    ),
]

JS_TOEVOEGING = '''

// Sluit beide submenu's (Neo Deco/Japandi) -- aangeroepen door alle
// andere hoofdknoppen zodat er nooit een oud submenu blijft staan.
function hideSubmenus(){
  var a=document.getElementById('artdecoSub'); if(a) a.style.display='none';
  var j=document.getElementById('japandiSub'); if(j) j.style.display='none';
}
'''


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    if "hideSubmenus" in content:
        print("FOUT: hideSubmenus bestaat al. Stop om dubbele registratie te voorkomen.")
        sys.exit(1)

    problemen = []
    if content.count(OLD_CSS) != 1:
        problemen.append(f"CSS-regel: {content.count(OLD_CSS)}x gevonden, verwacht 1x")
    for label, oud, nieuw in KNOP_VERVANGINGEN:
        n = content.count(oud)
        if n != 1:
            problemen.append(f"{label}: {n}x gevonden, verwacht 1x")

    if problemen:
        print("FOUT: onverwachte inhoud gevonden, stop voor de veiligheid:")
        for p in problemen:
            print(f"  - {p}")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"index.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD_CSS, NEW_CSS)
    print("CSS-specificiteit gecorrigeerd (sub-active wint nu)")
    for label, oud, nieuw in KNOP_VERVANGINGEN:
        new_content = new_content.replace(oud, nieuw)
        print(f"Bijgewerkt: {label} sluit nu submenu's")

    # JS toevoegen vlak voor sluitende </script> van het hoofdscript-blok
    # (append aan het bestaande <script> blok is niet triviaal via regex,
    # dus voegen we een los <script> blok toe vlak voor </body>)
    if "</body>" not in new_content:
        print("FOUT: geen </body> gevonden om JS voor te injecteren.")
        sys.exit(1)
    new_content = new_content.replace(
        "</body>",
        f"<script>{JS_TOEVOEGING}</script>\n</body>",
        1
    )
    print("hideSubmenus() toegevoegd (los <script> blok voor </body>)")

    TARGET.write_text(new_content, encoding="utf-8")
    print(f"Oude grootte: {backup.stat().st_size} bytes")
    print(f"Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "hideSubmenus" templates/index.html   (verwacht: 8 = 7 knoppen + 1 definitie)')


if __name__ == "__main__":
    main()
