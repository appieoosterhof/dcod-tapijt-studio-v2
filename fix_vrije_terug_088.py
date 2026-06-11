#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zet de opacity van Vrije vormen terug naar 0.88. Lagere opacity maakt de
tegelnaden zichtbaar (dubbele overlap op de rand). Backup. Idempotent.
Draai vanuit projectmap; stop Flask eerst."""
import os, shutil, datetime, sys, re
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "modules_extra.py"
def main():
    if not os.path.exists(PATH): sys.exit("FOUT: draai vanuit ~/Desktop/tapijt-studio.")
    with open(PATH, encoding="utf-8") as f: txt = f.read()
    m = re.search(r'fill="\{kleur\}" opacity="0\.\d+"', txt)
    if not m:
        print("! Kon opacity-regel niet vinden. Stuur: grep -n opacity modules_extra.py"); return
    if 'opacity="0.88"' in txt:
        print("= Staat al op 0.88 -- overgeslagen"); return
    shutil.copy2(PATH, PATH + ".bak_" + STAMP)
    print("+ Backup: " + PATH + ".bak_" + STAMP)
    txt = re.sub(r'(fill="\{kleur\}" opacity=")0\.\d+(")', r'\g<1>0.88\g<2>', txt, count=1)
    with open(PATH, "w", encoding="utf-8") as f: f.write(txt)
    print("+ Opacity teruggezet naar 0.88 (geen zichtbare naden)")
    print("\nHierna: python3 -m py_compile modules_extra.py ; start Flask ; hard refresh")
if __name__ == "__main__": main()
