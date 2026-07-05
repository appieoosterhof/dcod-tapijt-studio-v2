#!/usr/bin/env python3
"""
Laat openVisualizer() de meubellaag-afbeelding uit de actieve mockup-config
zetten (window.ROOM_MOCKUPS), en laat ruimteScale() de offsetX/offsetY uit
diezelfde config toepassen als achtergrond-positie. Rotation wordt bewust
(nog) niet toegepast -- die staat als 0 in de config klaar voor als een
toekomstig dessin/mockup het echt nodig blijkt.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_room_mockup_wiring.py
Vereist dat fix_room_mockup_config.py al gedraaid is.
Maakt automatisch een timestamped .bak van static/js/app.js
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("static/js/app.js")

OLD_SCALE = '''  function ruimteScale(){var s=+document.getElementById('ruimteScale').value;document.getElementById('ruimteCarpet').style.backgroundSize=s+'px '+s+'px';}
  window.openVisualizer=function(){
    if(typeof currentTileSvg==='undefined' || !currentTileSvg){ alert('Genereer eerst een dessin.'); return; }
    document.getElementById('ruimteCarpet').style.backgroundImage="url('data:image/svg+xml;base64,"+currentTileSvg+"')";
    ruimteScale();
    document.getElementById('ruimteModal').style.display='flex';
    setTimeout(ruimteLayout,40);
  };'''

NEW_SCALE = '''  function ruimteScale(){
    var s=+document.getElementById('ruimteScale').value;
    var mockup=huidigeMockup();
    var offX=mockup.offsetX||0, offY=mockup.offsetY||0;
    var c=document.getElementById('ruimteCarpet');
    c.style.backgroundSize=s+'px '+s+'px';
    c.style.backgroundPosition=offX+'px '+offY+'px';
  }
  window.openVisualizer=function(){
    if(typeof currentTileSvg==='undefined' || !currentTileSvg){ alert('Genereer eerst een dessin.'); return; }
    var mockup=huidigeMockup();
    FR = mockup.floorPoints;
    document.getElementById('ruimteCarpet').style.backgroundImage="url('data:image/svg+xml;base64,"+currentTileSvg+"')";
    document.getElementById('ruimteMeubels').src=mockup.image;
    ruimteScale();
    document.getElementById('ruimteModal').style.display='flex';
    setTimeout(ruimteLayout,40);
  };'''


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    if "huidigeMockup" not in content:
        print("FOUT: huidigeMockup() bestaat nog niet. Draai eerst fix_room_mockup_config.py.")
        sys.exit(1)

    if "mockup.offsetX" in content:
        print("FOUT: deze wiring lijkt al aanwezig. Stop om dubbele toepassing te voorkomen.")
        sys.exit(1)

    count = content.count(OLD_SCALE)
    if count == 0:
        print("FOUT: de verwachte oude ruimteScale/openVisualizer-functies zijn niet exact gevonden.")
        sys.exit(1)
    if count > 1:
        print(f"FOUT: de oude functies komen {count}x voor, verwacht precies 1x. Stop voor de veiligheid.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"app.js.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD_SCALE, NEW_SCALE)
    TARGET.write_text(new_content, encoding="utf-8")
    print("app.js aangepast: openVisualizer + ruimteScale lezen nu image/offsetX/offsetY uit config")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -n "mockup.offsetX\\|mockup.image" static/js/app.js')


if __name__ == "__main__":
    main()
