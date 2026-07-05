#!/usr/bin/env python3
"""
Voegt twee nieuwe concepten toe aan DCOD_CONCEPTS in static/js/app.js:
- neo_bauhaus: zelfde generator als de bestaande Bauhaus-knop (generator:"bauhaus")
- vrije_vormen: eigen generator (generate_vrije_vormen_svg bestaat al)

Regel-gebaseerde invoeging (zoekt op de unieke lijnenspel-regel), dus
ongevoelig voor exacte witruimte elders in het bestand.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_add_concepts_neobauhaus_vrijevormen.py
Maakt automatisch een timestamped .bak van static/js/app.js
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("static/js/app.js")

ANKER_REGEL = '  lijnenspel:    { title:"Lijnenspel",     description:"Ritmisch grafisch lijnenpatroon.", generator:"lijnenspel", palette:"zakelijk", prompt:"lijnenspel, ritmisch grafisch lijnenpatroon", palet:{background:"#EFE6CF",primary:"#003614",secondary:"#A7C58E",accent1:"#12301a",accent2:"#6f8a4e"} }'

NIEUWE_REGELS = ''',
  neo_bauhaus:   { title:"Neo Bauhaus",    description:"Heldere geometrische composities met een moderne, architectonische uitstraling.", generator:"bauhaus", palette:"geometrisch", prompt:"Bauhaus geometrisch patroon, halve cirkels driehoeken en ringen, oranje zwart grijs", palet:{background:"#1a1a1a",primary:"#d4622a",secondary:"#4a4a4a",accent1:"#c9a24a",accent2:"#efe6cf"} },
  vrije_vormen:  { title:"Vrije vormen",   description:"Speelse organische composities met een eigentijds karakter.", generator:"vrije_vormen", palette:"artistiek", prompt:"Vrije organische vormen, vloeiend en natuurlijk", palet:{background:"#F5F1E8",primary:"#6f8a4e",secondary:"#C9A24A",accent1:"#0E2117",accent2:"#A7C58E"} }'''


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    lines = TARGET.read_text(encoding="utf-8").splitlines(keepends=True)

    if any("neo_bauhaus:" in line for line in lines):
        print("FOUT: neo_bauhaus bestaat al in app.js. Stop om dubbele registratie te voorkomen.")
        sys.exit(1)
    if any("vrije_vormen:  {" in line or "vrije_vormen: {" in line for line in lines):
        print("FOUT: vrije_vormen lijkt al te bestaan als DCOD_CONCEPTS-entry. Stop voor de veiligheid.")
        sys.exit(1)

    anker_indices = [i for i, line in enumerate(lines) if line.rstrip("\n") == ANKER_REGEL]
    if len(anker_indices) == 0:
        print("FOUT: ankerregel (lijnenspel-entry) niet exact gevonden.")
        sys.exit(1)
    if len(anker_indices) > 1:
        print(f"FOUT: ankerregel komt {len(anker_indices)}x voor, verwacht precies 1x. Stop voor de veiligheid.")
        sys.exit(1)

    idx = anker_indices[0]

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"app.js.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    # Vervang de ankerregel (zonder newline) door zichzelf + de nieuwe regels + newline
    lines[idx] = ANKER_REGEL + NIEUWE_REGELS + "\n"

    TARGET.write_text("".join(lines), encoding="utf-8")
    print("app.js aangepast: neo_bauhaus en vrije_vormen toegevoegd aan DCOD_CONCEPTS")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -n "neo_bauhaus\\|vrije_vormen:" static/js/app.js')


if __name__ == "__main__":
    main()
