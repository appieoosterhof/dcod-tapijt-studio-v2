#!/usr/bin/env python3
"""
Past .btn-export CSS aan zodat 'Bekijk in ruimte' dezelfde roze kleur en
een vergelijkbaar formaat krijgt als .btn-generate ('Genereer dessin').

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_btn_export_styling.py
Maakt automatisch een timestamped .bak van templates/index.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/index.html")

OLD = ".btn-export{padding:11px 17px;background:transparent;border:1px solid var(--line-strong);color:var(--text);border-radius:var(--radius-sm);font-size:13.5px;cursor:pointer;font-family:var(--font);display:flex;align-items:center;gap:8px;transition:.15s;}"
NEW = ".btn-export{padding:14px 22px;background:var(--roze);border:none;color:#33141b;border-radius:var(--radius-sm);font-size:15px;font-weight:700;cursor:pointer;font-family:var(--font);display:flex;align-items:center;gap:8px;transition:.15s;}"


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    count = content.count(OLD)
    if count == 0:
        print("FOUT: de verwachte oude .btn-export CSS is niet exact gevonden.")
        sys.exit(1)
    if count > 1:
        print(f"FOUT: komt {count}x voor, verwacht precies 1x. Stop voor de veiligheid.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"index.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD, NEW)
    TARGET.write_text(new_content, encoding="utf-8")
    print("index.html aangepast: .btn-export is nu roze en groter, net als .btn-generate")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -n "btn-export{" templates/index.html')


if __name__ == "__main__":
    main()
