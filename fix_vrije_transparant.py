#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zet de opacity van Vrije vormen van 0.88 naar 0.75 voor subtiele
kleurmenging waar vormen overlappen. Raakt alleen modules_extra.py.
Backup. Idempotent. Draai vanuit projectmap; stop Flask eerst."""
import os, shutil, datetime, sys
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "modules_extra.py"
def main():
    if not os.path.exists(PATH): sys.exit("FOUT: draai vanuit ~/Desktop/tapijt-studio.")
    with open(PATH, encoding="utf-8") as f: txt = f.read()
    old = 'fill="{kleur}" opacity="0.88"'
    new = 'fill="{kleur}" opacity="0.75"'
    if new in txt:
        print("= Staat al op 0.75 -- overgeslagen"); return
    if old not in txt:
        print("! Kon opacity 0.88 niet vinden. Stuur: grep -n 'opacity' modules_extra.py"); return
    shutil.copy2(PATH, PATH + ".bak_" + STAMP)
    print("+ Backup: " + PATH + ".bak_" + STAMP)
    txt = txt.replace(old, new, 1)
    with open(PATH, "w", encoding="utf-8") as f: f.write(txt)
    print("+ Opacity Vrije vormen -> 0.75 (subtiele menging)")
    print("\nHierna: python3 -m py_compile modules_extra.py ; start Flask ; hard refresh")
if __name__ == "__main__": main()
