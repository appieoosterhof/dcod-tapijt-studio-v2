#!/usr/bin/env python3
# Voegt de losse route /inspiratie toe die templates/inspiratie.html rendert.
# Raakt de bestaande route '/' (de Dessinator) NIET. Backup; compile-check; terugrol.
import os, re, sys, shutil, datetime, py_compile
APP="app.py"; TPL=os.path.join("templates","inspiratie.html")
if not os.path.exists(APP):
    print("FOUT: app.py niet gevonden. cd ~/Desktop/tapijt-studio"); sys.exit(1)
if not os.path.exists(TPL):
    print("LET OP: templates/inspiratie.html ontbreekt nog. Kopieer eerst inspiratie.html naar de templates-map:"); 
    print("   cp ~/Downloads/inspiratie.html templates/"); sys.exit(1)
def read(f):
    with open(f,encoding="utf-8") as fh: return fh.read()
def write(f,t):
    with open(f,"w",encoding="utf-8") as fh: fh.write(t)
app=read(APP)
stamp=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
bak=APP+"."+stamp+".bak"; shutil.copy2(APP,bak); print("Backup:",bak)
def restore(msg):
    shutil.copy2(bak,APP); print("\n[FAIL] %s\nTeruggezet."%msg); sys.exit(1)
if '"/inspiratie"' in app or "'/inspiratie'" in app:
    print("[OK] route /inspiratie bestaat al; niets te doen."); sys.exit(0)
anchor='@app.route("/")\ndef index():\n    return render_template("index.html")'
if anchor not in app:
    restore("kon de index-route niet exact vinden om na te plaatsen.")
nieuw=anchor+'\n\n\n@app.route("/inspiratie")\ndef inspiratie():\n    return render_template("inspiratie.html")'
app=app.replace(anchor,nieuw,1)
write(APP,app)
try: py_compile.compile(APP,doraise=True)
except Exception as ex: restore("compile-fout: %s"%ex)
print("\n[PASS] Route /inspiratie toegevoegd. De Dessinator op / is ongewijzigd.")
print("Start Flask en open http://localhost:5000/inspiratie")
