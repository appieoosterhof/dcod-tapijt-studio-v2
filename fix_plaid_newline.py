#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verwijdert de letterlijke \\n tekst die tussen de Terrazzo- en Urban Plaid-
knop in index.html staat, en vervangt 'm door een echt regeleinde + inspringing.
Raakt alleen templates/index.html. Backup. Idempotent."""
import os, shutil, datetime, sys
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "templates/index.html"
def main():
    if not os.path.exists(PATH): sys.exit("FOUT: draai vanuit ~/Desktop/tapijt-studio.")
    with open(PATH, encoding="utf-8") as f: txt = f.read()
    # de letterlijke twee tekens backslash-n tussen de twee knoppen
    target = '>Terrazzo</button>\\n          <button'
    repl = '>Terrazzo</button>\n          <button'
    if target not in txt:
        print("! Letterlijke \\n niet gevonden (misschien al opgelost).")
        print("  Stuur: grep -n 'Urban Plaid' templates/index.html"); return
    shutil.copy2(PATH, PATH + ".bak_" + STAMP)
    print("+ Backup: " + PATH + ".bak_" + STAMP)
    txt = txt.replace(target, repl, 1)
    with open(PATH, "w", encoding="utf-8") as f: f.write(txt)
    print("+ Letterlijke \\n vervangen door echt regeleinde")
    print("\nHierna: hard refresh (Cmd+Shift+R). Geen Flask-herstart nodig.")
if __name__ == "__main__": main()
