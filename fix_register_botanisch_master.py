#!/usr/bin/env python3
"""
Vervangt de generator voor stijl 'botanical' door generate_botanisch_master_svg,
en voegt de bijbehorende import toe. Dit dekt automatisch zowel de
Botanisch-knop in het linker menu als de Botanisch-conceptkaart op
/inspiratie, want beide routeren al naar dezelfde stijl-sleutel 'botanical'.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_register_botanisch_master.py
Maakt automatisch een timestamped .bak van app.py
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("app.py")

OLD_IMPORT_ANKER = "from modules_extra import generate_hoogtelijnen_svg"
NEW_IMPORT = "from modules_extra import generate_hoogtelijnen_svg\nfrom modules_extra import generate_botanisch_master_svg"

OLD_REGISTRATIE = '    "botanical": generate_floral_svg,'
NEW_REGISTRATIE = '    "botanical": generate_botanisch_master_svg,'


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    if "generate_botanisch_master_svg" in content:
        print("FOUT: generate_botanisch_master_svg is al geregistreerd in app.py. Stop voor de veiligheid.")
        sys.exit(1)

    if content.count(OLD_IMPORT_ANKER) != 1:
        print(f"FOUT: import-ankerregel {content.count(OLD_IMPORT_ANKER)}x gevonden, verwacht 1x.")
        sys.exit(1)
    if content.count(OLD_REGISTRATIE) != 1:
        print(f"FOUT: registratie-regel {content.count(OLD_REGISTRATIE)}x gevonden, verwacht 1x.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"app.py.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD_IMPORT_ANKER, NEW_IMPORT, 1)
    new_content = new_content.replace(OLD_REGISTRATIE, NEW_REGISTRATIE, 1)
    TARGET.write_text(new_content, encoding="utf-8")

    print("app.py aangepast: import toegevoegd + 'botanical' wijst nu naar generate_botanisch_master_svg")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -n "botanisch_master" app.py')
    print('  python3 -c "import app"')


if __name__ == "__main__":
    main()
