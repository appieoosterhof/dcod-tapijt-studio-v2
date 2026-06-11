#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_overlap_uit.py  -  RepeatTile Studio
Draait de tegel-overlap in build_repeat_svg terug. Die 1%-schaling per tegel
(toegevoegd voor de schubben) verschuift de dots net genoeg om op de tegel-
grens een naad te geven. Terug naar de simpele translate zonder schaling.

Past alleen de 'else'-tak van de tegel-transform in app.py aan.
- Maakt automatisch een backup
- Veilig om opnieuw te draaien
"""

import os
import shutil
import time
import py_compile

BASE = os.path.expanduser("~/Desktop/tapijt-studio")
APP = os.path.join(BASE, "app.py")
STAMP = time.strftime("%Y%m%d_%H%M%S")

OUD = (
    '            else:\n'
    '                _ov = 2.0\n'
    '                _f = (T + 2 * _ov) / T\n'
    '                transform = f"translate({x - _ov},{y - _ov}) scale({_f})"'
)
NIEUW = (
    '            else:\n'
    '                transform = f"translate({x},{y})"'
)


def main():
    if not os.path.exists(APP):
        print("AFGEBROKEN: niet gevonden -> " + APP)
        return
    print("=" * 52)
    print(" Tegel-overlap terugdraaien (dots-naad weg)")
    print("=" * 52)

    with open(APP, "r", encoding="utf-8") as f:
        inhoud = f.read()

    if NIEUW in inhoud and "_ov = 2.0" not in inhoud:
        print("  al teruggedraaid - overgeslagen")
    elif OUD not in inhoud:
        print("  LET OP: overlap-blok niet exact gevonden - geen wijziging")
        return
    else:
        bak = APP + ".bak_" + STAMP
        shutil.copy2(APP, bak)
        print("  backup -> " + os.path.basename(bak))
        inhoud = inhoud.replace(OUD, NIEUW, 1)
        with open(APP, "w", encoding="utf-8") as f:
            f.write(inhoud)
        print("  overlap uitgezet: ok")

    try:
        py_compile.compile(APP, doraise=True)
        print("  controle: geen syntaxfouten")
    except py_compile.PyCompileError as e:
        print("  FOUT bij compileren:")
        print("  " + str(e))
        return

    print("=" * 52)
    print(" Klaar. Herstart de app en test Dots EN Schubben.")
    print("=" * 52)


if __name__ == "__main__":
    main()
