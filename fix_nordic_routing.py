#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_nordic_routing.py
---------------------
Doel: Voorkomen dat een Nordic-prompt naar 'urban_plaid' wordt gerouteerd
omdat de AI-beschrijving het woord "ruit"/"ruitpatroon" bevat, of omdat de
AI zelf analysis['style'] op 'urban_plaid' zette.

Principe (zoals eerder vastgesteld): een EXPLICIETE prompt van de gebruiker
("nordic", "scandinavisch", "noors") moet altijd winnen van de AI-gok.

Aanpak: de nordic-check wordt VOOR de urban_plaid-check geplaatst, op twee
plekken in app.py:
  1) het generate-blok (bepaalt de daadwerkelijke tekening)
  2) het label_map-blok (bepaalt alleen het weergave-label)

Veiligheid:
  - Maakt eerst een timestamped backup: app.py.bak_JJJJMMDD_UUMMSS
  - Vervangt alleen exact gematchte blokken
  - Vindt het een blok niet exact, dan wordt DAT deel overgeslagen en
    gemeld; er wordt niets half-aangepast.

Gebruik:
  1) Stop Flask (Ctrl+C) als die draait
  2) Leg dit bestand in de projectmap ~/Desktop/tapijt-studio
  3) python3 fix_nordic_routing.py
"""

import os
import sys
import shutil
from datetime import datetime

APP = "app.py"


def main():
    if not os.path.exists(APP):
        print(f"FOUT: {APP} niet gevonden in de huidige map.")
        print("Ga eerst naar de projectmap:  cd ~/Desktop/tapijt-studio")
        sys.exit(1)

    with open(APP, "r", encoding="utf-8") as f:
        src = f.read()

    # --- Backup ---
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = f"{APP}.bak_{stamp}"
    shutil.copy2(APP, backup)
    print(f"Backup gemaakt: {backup}")

    veranderingen = 0

    # ------------------------------------------------------------------
    # AANPASSING 1 — generate-blok
    # In het blok rond regel 583-593 staat de urban_plaid-check VOOR de
    # nordic-check. We draaien die twee om, zodat nordic eerst wordt
    # getest. De houndstooth-regel ervoor en de chevron-regel erna laten
    # we ongemoeid.
    #
    # Oud (volgorde: urban_plaid -> chevron -> hexagon -> ogee -> nordic)
    # Nieuw (volgorde: nordic -> urban_plaid -> chevron -> hexagon -> ogee)
    # ------------------------------------------------------------------
    oud_1 = (
        "        elif analysis.get('style') == 'urban_plaid' or any(w in p for w in ['urban plaid', 'plaid', 'tartan', 'ruit', 'schots']):\n"
        "            analysis['style'] = 'urban_plaid'\n"
        "        elif any(w in p for w in ['chevron', 'zigzag']):\n"
        "            analysis['style'] = 'chevron'\n"
        "        elif any(w in p for w in ['hexagon', 'honingraat', 'zeshoek']):\n"
        "            analysis['style'] = 'hexagon'\n"
        "        elif any(w in p for w in ['ogee', 'schub', 'dakpan']):\n"
        "            analysis['style'] = 'ogee'\n"
        "        elif any(w in p for w in ['nordic', 'scandinavisch', 'noors', 'kruis', 'sneeuwvlok']):\n"
        "            analysis['style'] = 'nordic'\n"
    )

    nieuw_1 = (
        "        elif any(w in p for w in ['nordic', 'scandinavisch', 'noors', 'sneeuwvlok']):\n"
        "            analysis['style'] = 'nordic'\n"
        "        elif analysis.get('style') == 'urban_plaid' or any(w in p for w in ['urban plaid', 'plaid', 'tartan', 'ruit', 'schots']):\n"
        "            analysis['style'] = 'urban_plaid'\n"
        "        elif any(w in p for w in ['chevron', 'zigzag']):\n"
        "            analysis['style'] = 'chevron'\n"
        "        elif any(w in p for w in ['hexagon', 'honingraat', 'zeshoek']):\n"
        "            analysis['style'] = 'hexagon'\n"
        "        elif any(w in p for w in ['ogee', 'schub', 'dakpan']):\n"
        "            analysis['style'] = 'ogee'\n"
    )

    if oud_1 in src:
        src = src.replace(oud_1, nieuw_1)
        veranderingen += 1
        print("OK  - Aanpassing 1 toegepast (generate-blok: nordic nu vóór urban_plaid).")
    else:
        print("OVERGESLAGEN - Aanpassing 1: exact blok niet gevonden. Niets gewijzigd in dit deel.")

    # ------------------------------------------------------------------
    # AANPASSING 2 — label_map-blok (alleen weergave-label)
    # In de label_map staat de urban_plaid-regel vóór de nordic-regel.
    # We zetten de nordic-regel ervoor zodat het label klopt.
    #
    # Let op: 'ruit' staat hier ook in urban_plaid. Omdat nordic nu eerst
    # gematcht wordt, krijgt een nordic-prompt het juiste label.
    # ------------------------------------------------------------------
    oud_2 = (
        "            (['urban plaid', 'plaid', 'tartan', 'ruit', 'schots'], 'urban_plaid'),\n"
        "            (['chevron', 'zigzag'], 'chevron'),\n"
        "            (['hexagon', 'honingraat', 'zeshoek'], 'hexagon'),\n"
        "            (['nordic', 'scandinavisch', 'noors'], 'nordic'),\n"
    )

    nieuw_2 = (
        "            (['nordic', 'scandinavisch', 'noors'], 'nordic'),\n"
        "            (['urban plaid', 'plaid', 'tartan', 'ruit', 'schots'], 'urban_plaid'),\n"
        "            (['chevron', 'zigzag'], 'chevron'),\n"
        "            (['hexagon', 'honingraat', 'zeshoek'], 'hexagon'),\n"
    )

    if oud_2 in src:
        src = src.replace(oud_2, nieuw_2)
        veranderingen += 1
        print("OK  - Aanpassing 2 toegepast (label_map: nordic nu vóór urban_plaid).")
    else:
        print("OVERGESLAGEN - Aanpassing 2: exact blok niet gevonden. Niets gewijzigd in dit deel.")

    # ------------------------------------------------------------------
    if veranderingen == 0:
        print("\nGEEN wijzigingen doorgevoerd. app.py is ongewijzigd gebleven.")
        print("De backup is wel aangemaakt maar identiek aan het origineel.")
        sys.exit(0)

    with open(APP, "w", encoding="utf-8") as f:
        f.write(src)

    print(f"\nKLAAR: {veranderingen} aanpassing(en) opgeslagen in {APP}.")
    print("Controleer het resultaat en herstart Flask om te testen.")
    print(f"Terugzetten kan altijd met:  cp {backup} {APP}")


if __name__ == "__main__":
    main()
