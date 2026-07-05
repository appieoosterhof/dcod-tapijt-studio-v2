#!/usr/bin/env python3
"""
Verplaatst de hardcoded vloer-hoekpunten (FR) en de meubellaag-afbeelding
naar een configuratie-object ROOM_MOCKUPS in static/js/app.js. De huidige
waarden blijven identiek (geen visuele wijziging nu) -- dit is puur het
fundament voor toekomstige extra mockups (Werkplekken, Hotels, Overheid,
Musea), die straks alleen een nieuwe entry in dit object nodig hebben.

Voegt ook offsetX, offsetY en rotation toe per mockup (default 0), zodat
die later per dessin/mockup bijgesteld kunnen worden zonder codewijziging.

GEEN interactieve kalibratiemodule -- eenmalig kalibreren, dan vastzetten
als config, zoals afgesproken.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_room_mockup_config.py
Maakt automatisch een timestamped .bak van static/js/app.js
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("static/js/app.js")

OLD = '''(function(){
  var SRC = 600;
  /* vloer-hoekpunten als fractie van de scene (TL,TR,BL,BR) */
  var FR = [[0.150,0.547],[1.02,0.547],[-0.230,1.0],[1.107,1.0]];'''

NEW = '''(function(){
  var SRC = 600;

  /* ---- Mockup-configuratie ----
     Eenmalig gekalibreerde hoekpunten per mockup-foto. Geen interactieve
     kalibratietool: nieuwe mockups worden handmatig 1x uitgelijnd en hier
     als vaste waarden toegevoegd. floorPoints = vloer-hoekpunten als
     fractie van de scene (TL,TR,BL,BR). offsetX/offsetY (in px van de
     patroon-tegel) en rotation (in graden) zijn optioneel, default 0 --
     alleen invullen als een specifiek dessin/mockup dat nodig heeft. */
  window.ROOM_MOCKUPS = window.ROOM_MOCKUPS || {
    kantoor: {
      label: "Werkplekken & Kantoren",
      image: "/static/img/kantoor_meubellaag.png",
      floorPoints: [[0.150,0.547],[1.02,0.547],[-0.230,1.0],[1.107,1.0]],
      offsetX: 0,
      offsetY: 0,
      rotation: 0
    }
    /* Later toe te voegen, zodra de foto's + kalibratie klaar zijn:
    hotels: { label: "Hotels & Hospitality", image: "/static/img/hotels_meubellaag.png", floorPoints: [[...]], offsetX: 0, offsetY: 0, rotation: 0 },
    overheid: { label: "Overheid & Publieke gebouwen", image: "/static/img/overheid_meubellaag.png", floorPoints: [[...]], offsetX: 0, offsetY: 0, rotation: 0 },
    musea: { label: "Musea & Bibliotheken", image: "/static/img/musea_meubellaag.png", floorPoints: [[...]], offsetX: 0, offsetY: 0, rotation: 0 }
    */
  };

  var ACTIEVE_MOCKUP = "kantoor";
  function huidigeMockup(){ return window.ROOM_MOCKUPS[ACTIEVE_MOCKUP] || window.ROOM_MOCKUPS.kantoor; }

  var FR = huidigeMockup().floorPoints;'''


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    if "ROOM_MOCKUPS" in content:
        print("FOUT: ROOM_MOCKUPS bestaat al in app.js. Stop om dubbele registratie te voorkomen.")
        sys.exit(1)

    count = content.count(OLD)
    if count == 0:
        print("FOUT: de verwachte oude regels (FR-array + SRC) zijn niet exact gevonden.")
        sys.exit(1)
    if count > 1:
        print(f"FOUT: de oude regels komen {count}x voor, verwacht precies 1x. Stop voor de veiligheid.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"app.js.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD, NEW)
    TARGET.write_text(new_content, encoding="utf-8")
    print("app.js aangepast: ROOM_MOCKUPS config-object toegevoegd, FR leest nu uit config")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -n "ROOM_MOCKUPS" static/js/app.js')


if __name__ == "__main__":
    main()
