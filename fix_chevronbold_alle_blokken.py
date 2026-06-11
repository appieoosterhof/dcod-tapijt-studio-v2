#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_chevronbold_alle_blokken.py
--------------------------------
Maakt 'Chevron Bold' betrouwbaar via een UNIEK trefwoord 'chevronbold'
dat in geen enkel ander routing-blok botst.

Achtergrond: er zijn VIER routing-blokken in app.py die 'chevron' en
'herringbone' afvangen. Het woord 'herringbone' routeert bovendien naar
'visgraat' (vandaar de driehoekjes). Daarom:

  1) app.py: in alle vier de blokken een 'chevronbold'-check ALS EERSTE
     zetten, zodat geen later blok 'm kan overschrijven.
       - Blok 1 (~358) en Blok 2 (~379): style = "chevron_bold"
       - Blok 3 (~567): analysis['style'] = 'chevron_bold'
       - Blok 4 (~613): (['chevronbold'], 'chevron_bold') bovenaan de lijst
  2) index.html: knoptekst-prompt aanpassen -> 'herringbone' eruit,
     'chevronbold' erin als herkenningswoord. Zichtbare tekst blijft 'Chevron Bold'.

Elke aanpassing is idempotent (slaat over als 'chevronbold' al aanwezig is).
Backups met timestamp vooraf.

Draai vanuit de projectmap:  python3 fix_chevronbold_alle_blokken.py
BELANGRIJK: stop Flask (Ctrl+C) voordat je dit draait.
"""

import os
import shutil
import datetime
import sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(path):
    bak = path + ".bak_" + STAMP
    shutil.copy2(path, bak)
    print("  + Backup gemaakt: " + bak)

def patch_app():
    path = "app.py"
    print("[1/2] " + path)
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()

    if txt.count("chevronbold") >= 4:
        print("  = chevronbold staat al overal (>=4x) -- overgeslagen")
        return

    backup(path)
    changes = 0

    # --- Blok 1 (~358): style = "..." met p ---
    b1_anchor = ('    elif any(w in p for w in ["chevron bold", "herringbone", "chevron blok"]):\n'
                 '        style = "chevron_bold"\n')
    b1_new = ('    elif any(w in p for w in ["chevronbold", "chevron bold", "chevron blok"]):\n'
              '        style = "chevron_bold"\n')
    if b1_anchor in txt:
        txt = txt.replace(b1_anchor, b1_new, 1)
        changes += 1
        print("  + Blok 1 bijgewerkt (herringbone verwijderd, chevronbold toegevoegd)")
    elif 'for w in ["chevronbold"' in txt:
        print("  = Blok 1 al ok")
    else:
        print("  ! Blok 1 anchor niet gevonden")

    # --- Blok 2 (~379): style = "..." met prompt_lower ---
    b2_anchor = ('    elif any(w in prompt_lower for w in ["chevron", "zigzag", "pijl"]):\n'
                 '        style = "chevron"\n')
    b2_new = ('    elif any(w in prompt_lower for w in ["chevronbold", "chevron bold", "chevron blok"]):\n'
              '        style = "chevron_bold"\n'
              + b2_anchor)
    if 'prompt_lower for w in ["chevronbold"' in txt:
        print("  = Blok 2 al ok")
    elif b2_anchor in txt:
        txt = txt.replace(b2_anchor, b2_new, 1)
        changes += 1
        print("  + Blok 2 bijgewerkt (chevronbold-regel toegevoegd voor chevron)")
    else:
        print("  ! Blok 2 anchor niet gevonden")

    # --- Blok 3 (~567): analysis['style'] = '...' ---
    b3_anchor = ("        elif any(w in p for w in ['chevron', 'zigzag']):\n"
                 "            analysis['style'] = 'chevron'\n")
    b3_new = ("        elif any(w in p for w in ['chevronbold', 'chevron bold', 'chevron blok']):\n"
              "            analysis['style'] = 'chevron_bold'\n"
              + b3_anchor)
    if "for w in ['chevronbold'" in txt:
        print("  = Blok 3 al ok")
    elif b3_anchor in txt:
        txt = txt.replace(b3_anchor, b3_new, 1)
        changes += 1
        print("  + Blok 3 bijgewerkt (chevronbold-regel toegevoegd voor chevron)")
    else:
        print("  ! Blok 3 anchor niet gevonden")

    # --- Blok 4 (~613): tuple-lijst ---
    b4_anchor = "            (['chevron', 'zigzag'], 'chevron'),\n"
    b4_new = ("            (['chevronbold', 'chevron bold', 'chevron blok'], 'chevron_bold'),\n"
              + b4_anchor)
    if "'chevron_bold')" in txt:
        print("  = Blok 4 al ok")
    elif b4_anchor in txt:
        txt = txt.replace(b4_anchor, b4_new, 1)
        changes += 1
        print("  + Blok 4 bijgewerkt (chevronbold-tuple toegevoegd voor chevron)")
    else:
        print("  ! Blok 4 anchor niet gevonden")

    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("  -> " + str(changes) + " blok(ken) gewijzigd in app.py")

def patch_index():
    path = os.path.join("templates", "index.html")
    print("[2/2] " + path)
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()

    old_prompt = "Chevron Bold patroon, gevulde herringbone plankjes, zwart wit"
    new_prompt = "chevronbold patroon, gevulde schuine plankjes, zwart wit"

    if new_prompt in txt:
        print("  = Knop-prompt al bijgewerkt -- overgeslagen")
        return
    if old_prompt not in txt:
        print("  ! Oude knop-prompt niet gevonden -- handmatig controleren")
        return

    backup(path)
    txt = txt.replace(old_prompt, new_prompt, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print("  + Knop-prompt bijgewerkt: 'herringbone' eruit, 'chevronbold' erin")
    print("    (zichtbare knoptekst blijft 'Chevron Bold')")

def main():
    if not (os.path.exists("app.py") and os.path.exists("modules_extra.py")):
        sys.exit("FOUT: draai dit vanuit de projectmap (~/Desktop/tapijt-studio).")
    print("=== Chevron Bold routing repareren (timestamp " + STAMP + ") ===")
    patch_app()
    patch_index()
    print("")
    print("Klaar. Hierna:")
    print("  1) python3 -m py_compile app.py")
    print("  2) Start Flask opnieuw")
    print("  3) Hard refresh (Cmd+Shift+R), klik 'Chevron Bold'")
    print("  4) Tag rechtsboven moet nu 'chevron_bold' tonen")

if __name__ == "__main__":
    main()
