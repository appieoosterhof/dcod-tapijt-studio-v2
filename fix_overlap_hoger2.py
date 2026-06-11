#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verhoog OVERLAP_SCALE naar 1.02 (laatste restje haarlijn). Backup. Idempotent."""
import os, shutil, datetime, sys, re
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "app.py"
def main():
    if not os.path.exists(PATH): sys.exit("FOUT: draai vanuit ~/Desktop/tapijt-studio.")
    with open(PATH, encoding="utf-8") as f: txt = f.read()
    if "OVERLAP_SCALE = 1.02" in txt:
        print("= Staat al op 1.02 -- overgeslagen"); return
    m = re.search(r'OVERLAP_SCALE = 1\.\d+', txt)
    if not m:
        print("! Kon OVERLAP_SCALE niet vinden. Stuur: grep -n OVERLAP_SCALE app.py"); return
    shutil.copy2(PATH, PATH + ".bak_" + STAMP)
    print("+ Backup: " + PATH + ".bak_" + STAMP)
    txt = re.sub(r'OVERLAP_SCALE = 1\.\d+', 'OVERLAP_SCALE = 1.02', txt, count=1)
    with open(PATH, "w", encoding="utf-8") as f: f.write(txt)
    print("+ OVERLAP_SCALE verhoogd naar 1.02")
    print("\nHierna: python3 -m py_compile app.py ; start Flask ; hard refresh")
if __name__ == "__main__": main()
