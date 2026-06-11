#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sorteer_knoppen.py
-------------------
1) Hernoemt de knop 'Hanenpoot' naar 'Houndstooth'.
2) Sorteert alle chip-knoppen in <div class="suggestions"> alfabetisch
   op zichtbare tekst.
3) Hoogt de cache-stempel op.

Raakt alleen templates/index.html. Backup. Idempotent.
Draai vanuit de projectmap.
"""
import os, re, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "templates/index.html"

def main():
    if not os.path.exists(PATH):
        sys.exit("FOUT: draai vanuit ~/Desktop/tapijt-studio.")
    with open(PATH, encoding="utf-8") as f:
        txt = f.read()

    # 1) Hernoem Hanenpoot -> Houndstooth (alleen de zichtbare knoptekst)
    txt = txt.replace(
        ">Hanenpoot</button>",
        ">Houndstooth</button>", 1)

    # 2) Vind het suggestions-blok
    m = re.search(r'(<div class="suggestions">)(.*?)(</div>)', txt, re.DOTALL)
    if not m:
        print("! Kon <div class=\"suggestions\"> niet vinden"); return
    head, body, tail = m.group(1), m.group(2), m.group(3)

    # Alle chip-knoppen eruit halen
    buttons = re.findall(r'<button class="chip"[^>]*>.*?</button>', body)
    if not buttons:
        print("! Geen knoppen gevonden"); return

    # Sorteer op zichtbare tekst (tussen > en </button>), hoofdletterongevoelig
    def label(b):
        mm = re.search(r'>([^<]+)</button>', b)
        return (mm.group(1).strip().lower() if mm else b)
    buttons_sorted = sorted(buttons, key=label)

    # Herbouw het blok netjes ingesprongen
    indent = "          "
    new_body = "\n" + "\n".join(indent + b for b in buttons_sorted) + "\n        "
    new_block = head + new_body + tail

    backup = PATH + ".bak_" + STAMP
    shutil.copy2(PATH, backup)
    print("  + Backup: " + backup)

    txt = txt[:m.start()] + new_block + txt[m.end():]

    # 3) cache-stempel ophogen
    txt = re.sub(r'app\.js\?v=[0-9_]+', 'app.js?v=' + STAMP, txt, count=1)

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(txt)
    print("  + Hanenpoot -> Houndstooth")
    print("  + %d knoppen alfabetisch gesorteerd" % len(buttons_sorted))
    print("  + cache-stempel -> v=" + STAMP)
    print("")
    print("Volgorde nu:")
    for b in buttons_sorted:
        print("   - " + label(b))
    print("")
    print("Hierna: hard refresh (Cmd+Shift+R). Geen Flask-herstart nodig voor HTML.")

if __name__ == "__main__":
    main()
