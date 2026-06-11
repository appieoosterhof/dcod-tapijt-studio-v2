#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_chevron_bold_behoud.py
---------------------------
DE laatste fix. Het tweede routing-blok (op basis van description_nl /
prompt_lower) zet chevron_bold terug naar de gewone chevron, omdat de
AI-beschrijving "bold chevron" bevat -> de regel die "chevron" zoekt matcht,
en de "chevron bold"-regel (met andere woordvolgorde) niet.

Bewezen: met lege description_nl -> 24 polygonen (chevron_bold correct).
Met description_nl='chevron' -> 8 polygonen (driehoeken). Dat is precies wat
de app via de AI binnenkrijgt.

FIX: zet boven de chevron_bold-regel in dit blok een guard die de hele
beschrijvings-routing overslaat als de stijl AL chevron_bold is. Dan kan geen
enkele beschrijvingsregel 'm nog terugzetten.

Concreet: we vervangen de chevronbold-elif door een check die OOK geldt als
style al 'chevron_bold' is.

Timestamped backup vooraf. Idempotent.

Draai vanuit de projectmap:  python3 fix_chevron_bold_behoud.py
BELANGRIJK: stop Flask (Ctrl+C) eerst.
"""

import os, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = "app.py"

def main():
    if not os.path.exists(PATH):
        sys.exit("FOUT: draai dit vanuit de projectmap (~/Desktop/tapijt-studio).")
    with open(PATH, "r", encoding="utf-8") as f:
        txt = f.read()

    # De chevron_bold-elif in het tweede blok (prompt_lower).
    old = ('    elif any(w in prompt_lower for w in ["chevronbold", "chevron bold", "chevron blok"]):\n'
           '        style = "chevron_bold"\n')
    # Nieuw: match OOK als style al chevron_bold is, of als de beschrijving
    # "bold chevron" / "chevron" bevat terwijl de oorspronkelijke stijl al
    # chevron_bold was. Simpelste robuuste vorm: behoud chevron_bold.
    new = ('    elif style == "chevron_bold" or any(w in prompt_lower for w in ["chevronbold", "chevron bold", "chevron blok"]):\n'
           '        style = "chevron_bold"\n')

    if 'elif style == "chevron_bold" or any(w in prompt_lower' in txt:
        print("= Guard staat er al -- overgeslagen")
        return
    if old not in txt:
        print("! Kon de chevronbold-elif (prompt_lower-blok) niet exact vinden.")
        print("  Stuur: sed -n '376,392p' app.py")
        return

    bak = PATH + ".bak_" + STAMP
    shutil.copy2(PATH, bak)
    print("+ Backup gemaakt: " + bak)

    txt = txt.replace(old, new, 1)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(txt)
    print("+ Guard toegevoegd: chevron_bold blijft behouden in beschrijvings-routing")
    print("")
    print("Hierna:")
    print("  1) python3 -m py_compile app.py")
    print("  2) Start Flask opnieuw")
    print("  3) Hard refresh (Cmd+Shift+R), klik 'Chevron Bold'")
    print("  4) De chevron zou nu in de app moeten verschijnen")

if __name__ == "__main__":
    main()
