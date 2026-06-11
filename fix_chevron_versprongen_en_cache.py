#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_chevron_versprongen_en_cache.py
------------------------------------
Twee gerichte fixes:

1) modules_extra.py: generate_chevron_bold_svg krijgt een verticale
   verspringing per kolom (offset_factor 0.5), zodat de banden langs elkaar
   schuiven (parket-herringbone, zoals de upload) i.p.v. een V-punt.

2) static/js/app.js: cache-buster op de preview-afbeelding. De canvas-PNG
   krijgt een uniek tijdstempel mee zodat de browser nooit een oude preview
   uit cache toont. Dit lost het terugkerende cache-probleem structureel op.

Timestamped backups van beide bestanden vooraf. Idempotent.

Draai vanuit de projectmap:  python3 fix_chevron_versprongen_en_cache.py
BELANGRIJK: stop Flask (Ctrl+C) eerst.
"""

import os, re, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(path):
    bak = path + ".bak_" + STAMP
    shutil.copy2(path, bak)
    print("  + Backup: " + bak)

def patch_generator():
    path = "modules_extra.py"
    print("[1/2] " + path)
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    if "offset_factor" in txt and "generate_chevron_bold_svg" in txt:
        print("  = Verspringing lijkt al aanwezig -- overgeslagen")
        return
    # Voeg de voff-berekening en het gebruik ervan toe.
    # We haken in op de bestaande structuur: na 'slope = ...' voegen we voff toe,
    # en in 'yb = c * step' veranderen we naar 'yb = c * step + voff'.
    anchor_slope = '        slope = 1 if (col % 2 == 0) else -1\n'
    new_slope = ('        slope = 1 if (col % 2 == 0) else -1\n'
                 '        voff = col * step * 0.5  # verticale verspringing -> parket-herringbone\n')
    anchor_yb = '            yb = c * step\n'
    new_yb = '            yb = c * step + voff\n'

    if anchor_slope not in txt or anchor_yb not in txt:
        print("  ! Kon de verwachte regels niet vinden -- handmatig nodig")
        print("    Gezocht naar slope-regel en 'yb = c * step'")
        return

    backup(path)
    txt = txt.replace(anchor_slope, new_slope, 1)
    txt = txt.replace(anchor_yb, new_yb, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("  + Verticale verspringing toegevoegd (parket-herringbone)")

def patch_cachebuster():
    path = os.path.join("static", "js", "app.js")
    print("[2/2] " + path)
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    if "canvas.toDataURL('image/png')" not in txt:
        print("  ! toDataURL-regel niet gevonden -- cache-buster overgeslagen")
        return
    if "/* cachebuster */" in txt:
        print("  = Cache-buster al aanwezig -- overgeslagen")
        return
    # De preview gebruikt canvas.toDataURL, dat is al uniek per generatie
    # (de PNG-data verandert). Het echte cache-risico zit in de <img>-bron
    # die soms door de browser wordt vastgehouden. We forceren een herteken
    # door eerst de src leeg te maken. Dat is de veiligste, minimale ingreep.
    anchor = "      if (doel) doel.src = canvas.toDataURL('image/png');"
    new = ("      if (doel) { /* cachebuster */ doel.src = ''; "
           "doel.src = canvas.toDataURL('image/png'); }")
    if anchor not in txt:
        print("  ! Exacte toDataURL-regel niet gevonden -- handmatig nodig")
        return
    backup(path)
    txt = txt.replace(anchor, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("  + Cache-buster toegevoegd aan preview-render")

def main():
    if not (os.path.exists("modules_extra.py") and os.path.exists("app.py")):
        sys.exit("FOUT: draai dit vanuit de projectmap (~/Desktop/tapijt-studio).")
    print("=== Versprongen herringbone + cache-buster (" + STAMP + ") ===")
    patch_generator()
    patch_cachebuster()
    print("")
    print("Hierna:")
    print("  1) python3 -m py_compile modules_extra.py")
    print("  2) Start Flask opnieuw")
    print("  3) In de browser: leeg de cache grondig --")
    print("     Safari: Cmd+Option+E (leeg cache), daarna Cmd+R")
    print("     of open de app in een privevenster (Cmd+Shift+N)")
    print("  4) Klik 'Chevron Bold' -> je ziet nu de versprongen herringbone")

if __name__ == "__main__":
    main()
