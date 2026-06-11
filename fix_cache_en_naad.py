#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_cache_en_naad.py
---------------------
Twee fixes in een run:

1) templates/index.html: de cache-stempel van app.js ophogen.
   Oud: app.js?v=20260606_170726 (vast -> browser blijft oude JS gebruiken,
   met de canvas-preview die driehoekjes maakt). We zetten een NIEUWE stempel
   met de huidige timestamp, zodat de browser de bijgewerkte app.js laadt
   (directe SVG-weergave). Dit lost het terugkerende cache-probleem op.

2) modules_extra.py: naad-fix voor chevron_bold. Het verticale teken-bereik
   ruimer maken zodat de horizontale tegelnaad wordt opgevuld.

Timestamped backups vooraf. Idempotent.

Draai vanuit de projectmap:  python3 fix_cache_en_naad.py
BELANGRIJK: stop Flask (Ctrl+C) eerst.
"""

import os, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(path):
    bak = path + ".bak_" + STAMP
    shutil.copy2(path, bak)
    print("  + Backup: " + bak)

def patch_cache():
    path = os.path.join("templates", "index.html")
    print("[1/2] " + path)
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    old = 'app.js?v=20260606_170726'
    new = 'app.js?v=' + STAMP
    if 'app.js?v=' + STAMP in txt:
        print("  = Cache-stempel al opgehoogd -- overgeslagen")
        return
    if old not in txt:
        # Misschien staat er al een andere stempel; vervang generiek elke app.js?v=...
        import re
        m = re.search(r'app\.js\?v=[0-9_]+', txt)
        if not m:
            print("  ! Kon de app.js-stempel niet vinden -- handmatig nodig")
            return
        backup(path)
        txt = re.sub(r'app\.js\?v=[0-9_]+', new, txt, count=1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(txt)
        print("  + Cache-stempel opgehoogd naar v=" + STAMP)
        return
    backup(path)
    txt = txt.replace(old, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("  + Cache-stempel opgehoogd naar v=" + STAMP)

def patch_naad():
    path = "modules_extra.py"
    print("[2/2] " + path)
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    old_begin = "        c = -int((T + cw) / step) - 2\n"
    new_begin = "        c = -int((T + cw) / step) - 6\n"
    old_while = "        while c * step < 2 * T + cw:\n"
    new_while = "        while c * step < 2 * T + cw + 6 * step:\n"
    if new_while in txt:
        print("  = Naad-fix al toegepast -- overgeslagen")
        return
    if old_begin not in txt or old_while not in txt:
        print("  ! Kon de lus-regels niet exact vinden -- handmatig nodig")
        print("    Stuur: sed -n '419,460p' modules_extra.py")
        return
    backup(path)
    txt = txt.replace(old_begin, new_begin, 1)
    txt = txt.replace(old_while, new_while, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("  + Naad-fix toegepast (verticaal bereik verruimd)")

def main():
    if not (os.path.exists("modules_extra.py") and os.path.exists(os.path.join("templates","index.html"))):
        sys.exit("FOUT: draai dit vanuit de projectmap (~/Desktop/tapijt-studio).")
    print("=== Cache-stempel + naad-fix (" + STAMP + ") ===")
    patch_cache()
    patch_naad()
    print("")
    print("Hierna:")
    print("  1) python3 -m py_compile modules_extra.py")
    print("  2) Start Flask opnieuw")
    print("  3) Gewone hard refresh (Cmd+Shift+R) volstaat nu -- de nieuwe")
    print("     cache-stempel dwingt de browser de bijgewerkte app.js te laden")
    print("  4) Klik 'Chevron Bold' -> herringbone zonder driehoekjes, zonder naad")

if __name__ == "__main__":
    main()
