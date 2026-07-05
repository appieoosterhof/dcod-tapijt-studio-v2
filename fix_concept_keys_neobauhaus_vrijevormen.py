#!/usr/bin/env python3
"""
Voegt "Neo Bauhaus":"neo_bauhaus" en "Vrije vormen":"vrije_vormen" toe aan
DCOD_CONCEPT_KEYS in templates/inspiratie.html, zodat startConcept() deze
namen correct naar hun sleutel vertaalt.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_concept_keys_neobauhaus_vrijevormen.py
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/inspiratie.html")

OLD = '''  "Weefstructuren":"weefstructuren",
  "Lijnenspel":"lijnenspel"
};'''

NEW = '''  "Weefstructuren":"weefstructuren",
  "Lijnenspel":"lijnenspel",
  "Neo Bauhaus":"neo_bauhaus",
  "Vrije vormen":"vrije_vormen"
};'''


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
    backup = TARGET.with_name(f"inspiratie.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD, NEW)
    TARGET.write_text(new_content, encoding="utf-8")
    print("inspiratie.html aangepast: Neo Bauhaus en Vrije vormen toegevoegd aan DCOD_CONCEPT_KEYS")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -n "Neo Bauhaus\\|Vrije vormen" templates/inspiratie.html')


if __name__ == "__main__":
    main()
