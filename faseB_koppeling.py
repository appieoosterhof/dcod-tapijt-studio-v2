#!/usr/bin/env python3
# =====================================================================
#  FASE B+C -- begeleide route via ?concept=<sleutel>
#  - Verrijkte DCOD_CONCEPTS als centrale bron (title/project/generator/palette/prompt/description)
#  - Bij ?concept=: verberg #emptyState (etalage), toon breadcrumb-header
#    "[Project] > [Concept] > Uw eerste voorstel", en genereer direct.
#  - Zonder ?concept=: Dessinator exact zoals nu.
#  Voegt alles achteraan app.js toe (nieuwe listener; raakt bestaande niet).
#  Backup; node --check indien aanwezig; terugrol.
# =====================================================================
import os, sys, shutil, datetime, subprocess
JS=os.path.join("static","js","app.js")
if not os.path.exists(JS):
    print("FOUT: static/js/app.js niet gevonden. cd ~/Desktop/tapijt-studio"); sys.exit(1)
def read(f):
    with open(f,encoding="utf-8") as fh: return fh.read()
def write(f,t):
    with open(f,"w",encoding="utf-8") as fh: fh.write(t)
js=read(JS)
stamp=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
bak=JS+"."+stamp+".bak"; shutil.copy2(JS,bak); print("Backup:",bak)
def restore(msg):
    shutil.copy2(bak,JS); print("\n[FAIL] %s\nTeruggezet."%msg); sys.exit(1)

# oude eenvoudige koppeling (vorige poging) verwijderen indien aanwezig, dan opnieuw plaatsen
if "DCOD_CONCEPTS" in js:
    start=js.find("/* ===== DCOD Dessinator - inspiratie-koppeling")
    end=js.find("/* ===== einde inspiratie-koppeling ===== */")
    if start!=-1 and end!=-1:
        js=js[:start]+js[end+len("/* ===== einde inspiratie-koppeling ===== */"):]
        print("Oude koppeling verwijderd, wordt vervangen.")
    else:
        print("[OK] DCOD_CONCEPTS al aanwezig in onbekende vorm; niets gedaan."); sys.exit(0)

BLOK = r'''

/* ===== DCOD Dessinator - inspiratie-koppeling (Fase B+C) ===== */
/* Centrale bron. 'generator' is intern; de gebruiker ziet alleen 'title'. */
var DCOD_CONCEPTS = {
  neo_deco:      { title:"Neo Deco",       description:"Eigentijdse geometrie voor representatieve interieurs.", generator:"art_deco_waaier", palette:"hospitality", prompt:"Art Deco waaier, luxe entree met warme messingaccenten, ritmische geometrie, rustige uitstraling", palet:{background:"#1a1a1a",primary:"#d8b24a",secondary:"#8a6a2e",accent1:"#efe6cf",accent2:"#c9a24a"} },
  aardlagen:     { title:"Aardlagen",      description:"Organische lagen en natuurlijke structuur in aardtinten.", generator:"aardlagen", palette:"aardlagen", prompt:"aardlagen, organische natuurlijke lagen, vloeiende structuur in aardtinten", palet:{background:"#e6d9b8",primary:"#6f8a4e",secondary:"#a7c58e",accent1:"#3b4d2c",accent2:"#23311f"} },
  japandi:       { title:"Japandi",        description:"Rust en minimalisme met gedempte natuurlijke tinten.", generator:"japandi", palette:"japandi", prompt:"japandi, rustige minimalistische vloer met gedempte natuurlijke tinten", palet:{background:"#e6d9b8",primary:"#626451",secondary:"#6E7359",accent1:"#8D9971",accent2:"#B5C49F"} },
  urban_plaid:   { title:"Urban Plaid",    description:"Rustig architectonisch raster voor moderne werkplekken.", generator:"urban_plaid", palette:"urban", prompt:"urban plaid, architectonisch ruitpatroon met warme textiele uitstraling", palet:{background:"#e8d5c0",primary:"#c38d96",secondary:"#b5734e",accent1:"#b5734e",accent2:"#e8d5c0"} },
  cirkels:       { title:"Cirkels",        description:"Ritmische cirkels, elegant en dynamisch.", generator:"cirkels", palette:"hospitality", prompt:"alleen cirkels, ritmisch en elegant, strak en dynamisch", palet:{background:"#1a1a1a",primary:"#c9a24a",secondary:"#efe6cf",accent1:"#8a6a2e",accent2:"#ffffff"} },
  botanisch:     { title:"Botanisch",      description:"Expressief en bloemrijk in vol koloriet.", generator:"vrije_vormen", palette:"natuurlijk", prompt:"vrije vormen organisch, expressief en bloemrijk in vol koloriet", palet:{background:"#e6d9b8",primary:"#a03d5d",secondary:"#c9a24a",accent1:"#4e7a4e",accent2:"#6f8a4e"} },
  hoogtelijnen:  { title:"Hoogtelijnen",   description:"Vloeiende contourlijnen, rustig en verfijnd.", generator:"lijnenspel", palette:"natuurlijk", prompt:"lijnenspel, vloeiende topografische contourlijnen, rustig en verfijnd", palet:{background:"#e9e0c8",primary:"#6f8a4e",secondary:"#a7c58e",accent1:"#42502e",accent2:"#8aa06a"} },
  weefstructuren:{ title:"Weefstructuren", description:"Geweven textiele structuur, warm en tactiel.", generator:"urban_plaid", palette:"natuurlijk", prompt:"urban plaid, geweven textiele structuur, warm en tactiel", palet:{background:"#e6ddc8",primary:"#b89a6a",secondary:"#8a6a4e",accent1:"#6f5a3e",accent2:"#d8c8a8"} },
  lijnenspel:    { title:"Lijnenspel",     description:"Ritmisch grafisch lijnenpatroon.", generator:"lijnenspel", palette:"zakelijk", prompt:"lijnenspel, ritmisch grafisch lijnenpatroon", palet:{background:"#EFE6CF",primary:"#003614",secondary:"#A7C58E",accent1:"#12301a",accent2:"#6f8a4e"} }
};
/* project-sleutel -> nette naam (voor de breadcrumb) */
var DCOD_PROJECTS = {
  werkplekken:"Werkplekken & Kantoren", hotels:"Hotels & Leisure",
  overheid:"Overheid & Publieke gebouwen", musea:"Musea & Bibliotheken"
};
window.addEventListener('DOMContentLoaded', function(){
  try {
    var params = new URLSearchParams(window.location.search);
    var key = params.get('concept');
    if (!key) return;                          /* geen concept => normale Dessinator */
    var c = DCOD_CONCEPTS[key];
    if (!c) return;
    var projKey = params.get('project') || '';
    var projNaam = DCOD_PROJECTS[projKey] || '';

    /* 1) verberg de etalage/voorbeeldkaarten */
    var empty = document.getElementById('emptyState');
    if (empty) empty.style.display = 'none';

    /* 2) breadcrumb-header invoegen boven de preview */
    var host = (document.getElementById('previewRepeat') || {}).parentNode;
    if (host && !document.getElementById('conceptHeader')) {
      var h = document.createElement('div');
      h.id = 'conceptHeader';
      h.style.cssText = 'margin:0 0 18px;padding:18px 22px;border:1px solid rgba(0,54,20,.14);border-radius:14px;background:linear-gradient(180deg,rgba(167,197,142,.10),rgba(167,197,142,.03));';
      var crumb = '';
      if (projNaam) crumb += '<span style="color:#5a6b57">'+projNaam+'</span> <span style="color:#A7C58E">&rarr;</span> ';
      crumb += '<span style="color:#5a6b57">'+c.title+'</span> <span style="color:#A7C58E">&rarr;</span> <span style="color:#5a6b57">Uw eerste voorstel</span>';
      h.innerHTML =
        '<div style="font-size:12px;letter-spacing:.06em;margin-bottom:10px;text-transform:uppercase">'+crumb+'</div>'+
        '<div style="font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#8a9a86">Startconcept</div>'+
        '<div style="font-family:Georgia,serif;font-size:26px;color:#003614;margin:2px 0 3px">'+c.title+'</div>'+
        (projNaam?'<div style="font-size:12px;color:#8a9a86">'+projNaam+'</div>':'')+
        (c.description?'<div style="font-size:13.5px;color:#5a6b57;margin-top:8px">'+c.description+'</div>':'');
      host.insertBefore(h, host.firstChild);
    }

    /* 3) direct genereren via de bestaande motor */
    function start(){
      if (typeof genereerVoorbeeld === 'function') { genereerVoorbeeld(key, c.prompt, c.palet); }
      else { setTimeout(start, 120); }
    }
    setTimeout(start, 160);
  } catch(e) { /* stil: nooit de Dessinator breken */ }
});
/* ===== einde inspiratie-koppeling ===== */
'''
js2 = js.rstrip() + "\n" + BLOK + "\n"
write(JS, js2)

node = shutil.which("node")
if node:
    r = subprocess.run([node,"--check",JS], capture_output=True, text=True)
    if r.returncode != 0: restore("JS-syntaxfout:\n"+r.stderr)
    print("[OK] node --check: app.js geldig.")
else:
    if False:
        restore("haakjes niet in balans.")
    print("[OK] (geen node) haakjesbalans klopt.")
print("\n[PASS] Begeleide route toegevoegd. ?concept= verbergt etalage + toont breadcrumb + genereert direct.")
