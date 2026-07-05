#!/usr/bin/env python3
"""
Robuuste versie: voegt /api/refine toe door te zoeken naar de regel
'@app.route("/api/export/svg"...)' en daar de nieuwe route vlak voor te
plaatsen. Werkt regel-voor-regel, dus ongevoelig voor het aantal lege
regels of spaties eromheen.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_add_refine_route.py
Maakt automatisch een timestamped .bak van app.py
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("app.py")

ANKER_REGEL = '@app.route("/api/export/svg", methods=["POST"])'

NIEUWE_ROUTE = '''REFINE_SYSTEM_INSTRUCTIE = """Je bent een assistent die vrije-tekst-instructies voor een
tapijtdessin vertaalt naar EEN parameter-aanpassing. Je verzint GEEN nieuwe
stijl en GEEN nieuw kleurenpalet. Je past alleen bestaande parameters aan.

Geef ALLEEN een JSON-object terug (geen uitleg, geen markdown), met dit exacte format:

{
  "lw_factor": 1.3,
  "toelichting_nl": "Korte uitleg van wat je hebt aangepast en waarom"
}

Regels voor lw_factor (lijndikte-vermenigvuldiger):
- 1.0 = ongewijzigd (standaard dikte)
- Groter dan 1.0 = dikkere lijnen (bv. "30% breder" -> 1.3)
- Kleiner dan 1.0 = dunnere lijnen (bv. "de helft dunner" -> 0.5)
- Blijf binnen het bereik 0.3 tot 3.0, ook als de gebruiker iets extremers vraagt
- Als de instructie niets met lijndikte te maken heeft, geef dan lw_factor: 1.0
  en leg in toelichting_nl uit dat dit (nog) niet ondersteund wordt.
"""


@app.route("/api/refine", methods=["POST"])
def api_refine():
    data = request.json
    api_key = (data.get("api_key", "") or "").strip()
    instructie = (data.get("instructie", "") or "").strip()
    prompt = (data.get("prompt", "") or "").strip()
    palet_in = data.get("palet") or {}
    tile_cm = int(data.get("tile_cm", 40))
    repeat_type = data.get("repeat_type", "full")
    dpi = int(data.get("dpi", 150))
    motief_schaal = int(data.get("motief_schaal", 100))
    try:
        huidige_lw_factor = float(data.get("lw_factor", 1.0) or 1.0)
    except (TypeError, ValueError):
        huidige_lw_factor = 1.0

    if not api_key:
        return jsonify({"error": "Vul uw API-sleutel in."}), 400
    if not instructie:
        return jsonify({"error": "Voer een verfijn-instructie in."}), 400

    p = prompt.lower()
    if not any(w in p for w in ["aardlagen", "aardlaag", "natuursteen", "agaat"]):
        return jsonify({"error": "Verfijnen met AI wordt op dit moment alleen ondersteund voor het dessin Aardlagen."}), 400

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=REFINE_SYSTEM_INSTRUCTIE,
            messages=[{"role": "user", "content": instructie}],
        )
        ruwe_tekst = message.content[0].text.strip()
        schoon = ruwe_tekst
        if schoon.startswith("```"):
            schoon = schoon.split("\\n", 1)[1] if "\\n" in schoon else schoon
            if schoon.rstrip().endswith("```"):
                schoon = schoon.rstrip()[:-3]
            schoon = schoon.strip()
            if schoon.startswith("json"):
                schoon = schoon[4:].strip()
        refine_resultaat = json.loads(schoon)
    except json.JSONDecodeError:
        return jsonify({"error": "AI gaf een onverwacht antwoord. Probeer opnieuw."}), 500
    except Exception as e:
        return jsonify({"error": f"AI-fout: {str(e)}"}), 500

    try:
        nieuwe_lw_factor = float(refine_resultaat.get("lw_factor", huidige_lw_factor))
    except (TypeError, ValueError):
        nieuwe_lw_factor = huidige_lw_factor
    nieuwe_lw_factor = max(0.3, min(3.0, nieuwe_lw_factor))
    toelichting = refine_resultaat.get("toelichting_nl", "")

    palette = {
        "background": palet_in.get("background", "#e9e0c8"),
        "primary": palet_in.get("primary", "#6f8a4e"),
        "secondary": palet_in.get("secondary", "#a7c58e"),
        "accent1": palet_in.get("accent1", "#42502e"),
        "accent2": palet_in.get("accent2", "#8aa06a"),
    }
    palette["_tile_cm"] = tile_cm
    palette["_al_lw_factor"] = nieuwe_lw_factor

    analysis = {
        "style": "aardlagen",
        "palette": palette,
        "_prompt": prompt.lower(),
        "_tile_cm": tile_cm,
        "complexity": data.get("complexity", "medium"),
    }

    try:
        tile_svg = build_tile_svg(analysis, tile_size=400, motief_schaal=motief_schaal)
        repeat_svg = build_repeat_svg(tile_svg, analysis, tile_cm, repeat_type, dpi)
        tile_b64 = base64.b64encode(tile_svg.encode()).decode()
        repeat_b64 = base64.b64encode(repeat_svg.encode()).decode()
    except Exception as e:
        return jsonify({"error": f"Generatie-fout: {str(e)}"}), 500

    return jsonify({
        "success": True,
        "lw_factor": nieuwe_lw_factor,
        "toelichting_nl": toelichting,
        "tile_svg_b64": tile_b64,
        "repeat_svg_b64": repeat_b64,
    })


'''


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    lines = TARGET.read_text(encoding="utf-8").splitlines(keepends=True)

    if any("/api/refine" in line for line in lines):
        print("FOUT: er bestaat al een /api/refine route in app.py. Stop om dubbele registratie te voorkomen.")
        sys.exit(1)

    anker_indices = [i for i, line in enumerate(lines) if line.strip() == ANKER_REGEL]
    if len(anker_indices) == 0:
        print(f"FOUT: ankerregel niet gevonden: {ANKER_REGEL}")
        sys.exit(1)
    if len(anker_indices) > 1:
        print(f"FOUT: ankerregel komt {len(anker_indices)}x voor, verwacht precies 1x. Stop voor de veiligheid.")
        sys.exit(1)

    idx = anker_indices[0]

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"app.py.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    nieuwe_lines = lines[:idx] + [NIEUWE_ROUTE] + lines[idx:]
    TARGET.write_text("".join(nieuwe_lines), encoding="utf-8")

    print("app.py aangepast: nieuwe route /api/refine toegevoegd (regel-gebaseerde invoeging)")
    print(f"  Oude grootte: {backup.stat().st_size} bytes")
    print(f"  Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  python3 -c "import app"   (moet zonder foutmelding importeren)')
    print('  grep -n "api/refine" app.py')


if __name__ == "__main__":
    main()
