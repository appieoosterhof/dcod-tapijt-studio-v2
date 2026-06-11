#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_preview_directe_svg.py
---------------------------
Vervangt svgNaarPngPreview in static/js/app.js zodat de SVG RECHTSTREEKS in
de <img> wordt gezet, zonder de canvas-naar-PNG tussenstap.

Waarom: de canvas-stap leest img.naturalWidth/naturalHeight van de SVG. Een
SVG met alleen viewBox (geen vaste pixelmaten) geeft in browsers vaak 0 of
een afwijkende waarde, waardoor drawImage de tegel vervormd/gedeeltelijk
tekent -> de 'driehoekjes'. Direct als <img>-src tonen rendert de SVG correct
(zoals het losse bestand echte_tegel.svg liet zien).

Timestamped backup vooraf. Idempotent.

Draai vanuit de projectmap:  python3 fix_preview_directe_svg.py
(Geen Flask-herstart nodig voor JS, maar wel hard refresh in de browser.)
"""

import os, re, shutil, datetime, sys

STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PATH = os.path.join("static", "js", "app.js")

NEW_FUNC = '''function svgNaarPngPreview(svgB64, elementId, breedte) {
  try {
    const doel = document.getElementById(elementId);
    if (doel) {
      // SVG rechtstreeks tonen (geen canvas-tussenstap; voorkomt vervorming
      // bij SVG's met alleen viewBox). Cachebuster via leegmaken + nieuwe src.
      doel.src = '';
      doel.src = 'data:image/svg+xml;base64,' + svgB64;
    }
  } catch (e) {
    console.log('Preview-render fout:', e);
  }
}'''

def main():
    if not os.path.exists(PATH):
        sys.exit("FOUT: draai dit vanuit de projectmap (~/Desktop/tapijt-studio).")
    with open(PATH, "r", encoding="utf-8") as f:
        txt = f.read()

    if "SVG rechtstreeks tonen (geen canvas-tussenstap" in txt:
        print("= Directe-SVG-versie staat er al -- overgeslagen")
        return

    # Vervang de hele functie van 'function svgNaarPngPreview' tot de
    # bijbehorende sluitende '}' op kolom 0 (de regel die alleen '}' bevat).
    pat = re.compile(r'function svgNaarPngPreview\(svgB64, elementId, breedte\) \{.*?\n\}',
                     re.DOTALL)
    m = pat.search(txt)
    if not m:
        print("! Kon svgNaarPngPreview niet vinden -- handmatig nodig")
        return

    bak = PATH + ".bak_" + STAMP
    shutil.copy2(PATH, bak)
    print("+ Backup gemaakt: " + bak)

    txt = txt[:m.start()] + NEW_FUNC + txt[m.end():]
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(txt)
    print("+ svgNaarPngPreview vervangen door directe SVG-weergave")
    print("")
    print("Hierna (GEEN Flask-herstart nodig voor JS):")
    print("  1) In de browser: hard refresh met Cmd+Shift+R")
    print("     (of privevenster Cmd+Shift+N als het blijft hangen)")
    print("  2) Klik 'Chevron Bold' -> je ziet nu de versprongen herringbone")

if __name__ == "__main__":
    main()
