#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zet OVERLAP_SCALE terug naar 1.006 (beste versie: alleen fijne haarlijn,
geen knik). Schalen groter dan dit geeft een zichtbare verspringing op de
tegelgrens. Backup. Idempotent."""
import os, shutil, datetime, sys, re
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "app.py"
def main():
    if not os.path.exists(PATH): sys.exit("FOUT: draai vanuit ~/Desktop/tapijt-studio.")
    with open(PATH, encoding="utf-8") as f: txt = f.read()
    m = re.search(r'OVERLAP_SCALE = 1\.\d+', txt)
    if not m:
        print("! Kon OVERLAP_SCALE niet vinden. Stuur: grep -n OVERLAP_SCALE app.py"); return
    if "OVERLAP_SCALE = 1.006" in txt:
        print("= Staat al op 1.006 -- overgeslagen"); return
    shutil.copy2(PATH, PATH + ".bak_" + STAMP)
    print("+ Backup: " + PATH + ".bak_" + STAMP)
    txt = re.sub(r'OVERLAP_SCALE = 1\.\d+', 'OVERLAP_SCALE = 1.006', txt, count=1)
    with open(PATH, "w", encoding="utf-8") as f: f.write(txt)
    print("+ OVERLAP_SCALE teruggezet naar 1.006 (beste versie)")
    print("\nHierna: python3 -m py_compile app.py ; start Flask ; hard refresh")
if __name__ == "__main__": main()
