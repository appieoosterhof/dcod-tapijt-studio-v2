#!/usr/bin/env python3
"""
Fix voor DCOD Dessinator /inspiratie:
- kiesProject() onthoudt nu de gekozen projectnaam
- startConcept() vertaalt conceptnaam + projectnaam naar sleutels
  en navigeert naar /?concept=<key>&project=<key>

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_startconcept.py
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/inspiratie.html")

OLD = """function kiesProject(naam){
  var grid=document.getElementById('projgrid'); grid.classList.add('picked');
  document.querySelectorAll('.proj').forEach(p=>p.classList.toggle('active', p.querySelector('h3').textContent===naam));
  var pid='panel_'+naam.toLowerCase().replace(/ /g,'_').replace(/&/g,'en');
  document.querySelectorAll('.cc-panel').forEach(x=>x.classList.remove('open'));
  var panel=document.getElementById(pid);
  if(panel){panel.classList.add('open'); setTimeout(()=>panel.scrollIntoView({behavior:'smooth',block:'start'}),60);}
}
function startConcept(naam){ window.location.href="/"; }"""

NEW = """var DCOD_PROJECT_KEYS = {
  "Werkplekken & Kantoren":"werkplekken",
  "Hotels & Leisure":"hotels",
  "Overheid & Publieke gebouwen":"overheid",
  "Musea & Bibliotheken":"musea"
};
var DCOD_CONCEPT_KEYS = {
  "Neo Deco":"neo_deco",
  "Aardlagen":"aardlagen",
  "Japandi":"japandi",
  "Urban Plaid":"urban_plaid",
  "Cirkels":"cirkels",
  "Botanisch":"botanisch",
  "Hoogtelijnen":"hoogtelijnen",
  "Weefstructuren":"weefstructuren",
  "Lijnenspel":"lijnenspel"
};
var _dcodCurrentProject = '';
function kiesProject(naam){
  _dcodCurrentProject = naam;
  var grid=document.getElementById('projgrid'); grid.classList.add('picked');
  document.querySelectorAll('.proj').forEach(p=>p.classList.toggle('active', p.querySelector('h3').textContent===naam));
  var pid='panel_'+naam.toLowerCase().replace(/ /g,'_').replace(/&/g,'en');
  document.querySelectorAll('.cc-panel').forEach(x=>x.classList.remove('open'));
  var panel=document.getElementById(pid);
  if(panel){panel.classList.add('open'); setTimeout(()=>panel.scrollIntoView({behavior:'smooth',block:'start'}),60);}
}
function startConcept(naam){
  var conceptKey = DCOD_CONCEPT_KEYS[naam];
  if (!conceptKey) {
    /* onbekende naam (bv. brief-btn geeft nu nog een projectnaam mee i.p.v. conceptnaam) */
    console.warn('startConcept: onbekend concept "'+naam+'", geen parameters meegegeven.');
    window.location.href = "/";
    return;
  }
  var projectKey = DCOD_PROJECT_KEYS[_dcodCurrentProject] || '';
  var url = "/?concept=" + encodeURIComponent(conceptKey);
  if (projectKey) url += "&project=" + encodeURIComponent(projectKey);
  window.location.href = url;
}"""


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")

    count = content.count(OLD)
    if count == 0:
        print("FOUT: de verwachte oude functies zijn niet (exact) gevonden.")
        print("Mogelijk is het bestand al aangepast, of wijkt de inhoud iets af.")
        sys.exit(1)
    if count > 1:
        print(f"FOUT: de oude tekst komt {count}x voor, verwacht precies 1x. Stop voor de veiligheid.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"inspiratie.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    new_content = content.replace(OLD, NEW)
    TARGET.write_text(new_content, encoding="utf-8")

    new_size = TARGET.stat().st_size
    old_size = backup.stat().st_size
    print(f"Oude grootte: {old_size} bytes")
    print(f"Nieuwe grootte: {new_size} bytes")
    print("Fix toegepast op templates/inspiratie.html")
    print()
    print("Controleer met:")
    print('  grep -c "DCOD_CONCEPT_KEYS" templates/inspiratie.html   (verwacht: 1)')
    print('  grep -c "window.location.href = url" templates/inspiratie.html   (verwacht: 1)')


if __name__ == "__main__":
    main()
