#!/usr/bin/env python3
"""
Root cause fix: de 'hoogtelijnen'-entry in DCOD_CONCEPTS (static/js/app.js)
had generator:"lijnenspel" en een prompt die begon met het woord "lijnenspel".
Daardoor won in app.py altijd de lijnenspel-routing-check, nog voor de
hoogtelijnen-check ooit gecontroleerd werd.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_hoogtelijnen_routing.py
Maakt automatisch een timestamped .bak van static/js/app.js en van elk
template dat de app.js cache-stamp bevat.
"""
import re
import shutil
import datetime
import sys
from pathlib import Path

APPJS = Path("static/js/app.js")

OLD = 'hoogtelijnen:  { title:"Hoogtelijnen",   description:"Vloeiende contourlijnen, rustig en verfijnd.", generator:"lijnenspel", palette:"natuurlijk", prompt:"lijnenspel, vloeiende topografische contourlijnen, rustig en verfijnd", palet:{background:"#e9e0c8",primary:"#6f8a4e",secondary:"#a7c58e",accent1:"#42502e",accent2:"#8aa06a"} },'
NEW = 'hoogtelijnen:  { title:"Hoogtelijnen",   description:"Vloeiende contourlijnen, rustig en verfijnd.", generator:"hoogtelijnen", palette:"natuurlijk", prompt:"hoogtelijnen, vloeiende topografische contourlijnen, rustig en verfijnd", palet:{background:"#e9e0c8",primary:"#6f8a4e",secondary:"#a7c58e",accent1:"#42502e",accent2:"#8aa06a"} },'


def bump_cache_stamps():
    """Zoek in alle templates naar app.js?v=N en verhoog N met 1."""
    bumped = []
    for tpl in Path("templates").glob("*.html"):
        text = tpl.read_text(encoding="utf-8")
        matches = list(re.finditer(r'app\.js\?v=(\d+)', text))
        if not matches:
            continue
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = tpl.with_name(f"{tpl.name}.bak_{ts}")
        shutil.copy2(tpl, backup)

        def repl(m):
            return f'app.js?v={int(m.group(1)) + 1}'

        new_text = re.sub(r'app\.js\?v=(\d+)', repl, text)
        tpl.write_text(new_text, encoding="utf-8")
        old_v = matches[0].group(1)
        new_v = str(int(old_v) + 1)
        bumped.append((tpl.name, old_v, new_v, backup.name))
    return bumped


def main():
    if not APPJS.exists():
        print(f"FOUT: {APPJS} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = APPJS.read_text(encoding="utf-8")
    count = content.count(OLD)
    if count == 0:
        print("FOUT: de verwachte oude hoogtelijnen-regel is niet (exact) gevonden.")
        print("Mogelijk is het bestand al aangepast, of wijkt de inhoud iets af.")
        sys.exit(1)
    if count > 1:
        print(f"FOUT: de oude regel komt {count}x voor, verwacht precies 1x. Stop voor de veiligheid.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = APPJS.with_name(f"app.js.bak_{ts}")
    shutil.copy2(APPJS, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD, NEW)
    APPJS.write_text(new_content, encoding="utf-8")
    print(f"static/js/app.js aangepast: hoogtelijnen generator + prompt hersteld")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {APPJS.stat().st_size} bytes")

    print()
    print("Cache-stamp verhogen in templates...")
    bumped = bump_cache_stamps()
    if not bumped:
        print("  Geen 'app.js?v=N' gevonden in templates/*.html — controleer handmatig.")
    else:
        for name, old_v, new_v, backup_name in bumped:
            print(f"  {name}: v={old_v} -> v={new_v} (backup: {backup_name})")

    print()
    print("Controleer met:")
    print('  grep -n "hoogtelijnen:" static/js/app.js')
    print('  grep -n "app.js?v=" templates/*.html')


if __name__ == "__main__":
    main()
