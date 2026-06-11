#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_no_store_cache.py
----------------------
Twee fixes voor het laatste cache-probleem:

1) static/js/app.js: voeg cache:'no-store' toe aan de fetch naar /api/generate.
   Bewezen: SVG + base64-<img>-weergave zijn correct (test_img.html toonde de
   perfecte chevron). Het enige verschil is dat de browser bij klikken een
   oude API-respons hergebruikt. no-store dwingt elke keer een verse SVG af.

2) templates/index.html: cache-stempel van app.js ophogen, zodat de browser
   de bijgewerkte app.js daadwerkelijk laadt.

Timestamped backups vooraf. Idempotent.

Draai vanuit de projectmap:  python3 fix_no_store_cache.py
BELANGRIJK: stop Flask (Ctrl+C) eerst.
"""

import os, re, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(path):
    bak = path + ".bak_" + STAMP
    shutil.copy2(path, bak)
    print("  + Backup: " + bak)

def patch_appjs():
    path = os.path.join("static", "js", "app.js")
    print("[1/2] " + path)
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()

    # Doel: in de fetch naar /api/generate, na "method: 'POST'," de regel
    # "cache: 'no-store'," invoegen. We haken specifiek op DEZE fetch in.
    anchor = ("    const response = await fetch('/api/generate', {\n"
              "      method: 'POST',\n"
              "      headers: { 'Content-Type': 'application/json' },\n")
    new = ("    const response = await fetch('/api/generate', {\n"
           "      method: 'POST',\n"
           "      cache: 'no-store',\n"
           "      headers: { 'Content-Type': 'application/json' },\n")

    if "cache: 'no-store'" in txt and "/api/generate" in txt:
        # Ruwe check: staat no-store al ergens vlak bij de generate-fetch?
        idx = txt.find("/api/generate")
        if "no-store" in txt[idx-50:idx+200]:
            print("  = no-store al aanwezig bij /api/generate -- overgeslagen")
            return
    if anchor not in txt:
        print("  ! Kon de exacte fetch-regels niet vinden -- handmatig nodig")
        print("    Stuur: sed -n '88,96p' static/js/app.js")
        return
    backup(path)
    txt = txt.replace(anchor, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("  + cache:'no-store' toegevoegd aan /api/generate fetch")

def patch_index():
    path = os.path.join("templates", "index.html")
    print("[2/2] " + path)
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    new_stamp = STAMP
    if 'app.js?v=' + new_stamp in txt:
        print("  = Cache-stempel al op deze waarde -- overgeslagen")
        return
    m = re.search(r'app\.js\?v=[0-9_]+', txt)
    if not m:
        print("  ! Kon de app.js-stempel niet vinden -- handmatig nodig")
        return
    backup(path)
    txt = re.sub(r'app\.js\?v=[0-9_]+', 'app.js?v=' + new_stamp, txt, count=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("  + Cache-stempel opgehoogd naar v=" + new_stamp)

def main():
    if not (os.path.exists(os.path.join("static","js","app.js"))
            and os.path.exists(os.path.join("templates","index.html"))):
        sys.exit("FOUT: draai dit vanuit de projectmap (~/Desktop/tapijt-studio).")
    print("=== no-store + cache-stempel (" + STAMP + ") ===")
    patch_appjs()
    patch_index()
    print("")
    print("Hierna (GEEN Flask-herstart nodig voor JS/HTML, maar mag wel):")
    print("  1) Start Flask opnieuw (zekerheid)")
    print("  2) Hard refresh (Cmd+Shift+R)")
    print("  3) Klik 'Chevron Bold' -> nu verse SVG, de chevron zou moeten verschijnen")

if __name__ == "__main__":
    main()
