#!/usr/bin/env python3
"""
Voegt 'variant: river_stones' toe aan de prompt van de japandi-entry in
DCOD_CONCEPTS (static/js/app.js). De japandi-generator (modules_extra.py)
leest dit patroon uit palette["_jp_prompt"] via _jp_variant_from() en kiest
dan automatisch _jp_sub_river_stones i.p.v. de standaard organic-variant.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_japandi_river_stones.py
Maakt automatisch een timestamped .bak van static/js/app.js en bumpt de
app.js cache-stamp in templates die ernaar verwijzen.
"""
import re
import shutil
import datetime
import sys
from pathlib import Path

APPJS = Path("static/js/app.js")

OLD = 'japandi:       { title:"Japandi",        description:"Rust en minimalisme met gedempte natuurlijke tinten.", generator:"japandi", palette:"japandi", prompt:"japandi, rustige minimalistische vloer met gedempte natuurlijke tinten", palet:{background:"#e6d9b8",primary:"#626451",secondary:"#6E7359",accent1:"#8D9971",accent2:"#B5C49F"} },'
NEW = 'japandi:       { title:"Japandi",        description:"Rust en minimalisme met gedempte natuurlijke tinten.", generator:"japandi", palette:"japandi", prompt:"japandi, rustige minimalistische vloer met gedempte natuurlijke tinten, variant: river_stones", palet:{background:"#e6d9b8",primary:"#626451",secondary:"#6E7359",accent1:"#8D9971",accent2:"#B5C49F"} },'


def bump_cache_stamps():
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
        print("FOUT: de verwachte oude japandi-regel is niet (exact) gevonden.")
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
    print("static/js/app.js aangepast: japandi-prompt bevat nu 'variant: river_stones'")
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
    print('  grep -n "japandi:" static/js/app.js')
    print('  grep -n "app.js?v=" templates/*.html')


if __name__ == "__main__":
    main()
