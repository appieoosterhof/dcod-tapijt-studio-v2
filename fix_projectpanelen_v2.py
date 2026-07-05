#!/usr/bin/env python3
"""
Herbouwt de vier project-panelen op /inspiratie met de nieuwe, vastgestelde
kaartselecties (Werkplekken, Overheid, Musea, Hotels-blijft-voorlopig-oude-naam)
en voegt een cc-desc CSS-regel + beschrijvingstekst toe aan elke kaart.

Regel-gebaseerde vervanging: zoekt elk paneel op via zijn <section id="...">
en de eerstvolgende </section>-regel, dus ongevoelig voor exacte witruimte.

Gebruik:
    cd ~/Desktop/tapijt-studio
    python3 fix_projectpanelen_v2.py
Maakt automatisch een timestamped .bak van templates/inspiratie.html
"""
import shutil
import datetime
import sys
from pathlib import Path

TARGET = Path("templates/inspiratie.html")

CC_NAME_CSS = ".cc-name{font-family:'Fraunces';font-size:17px;margin-top:14px;color:var(--cream)}"
CC_DESC_CSS_TOEVOEGING = ".cc-desc{font-family:'Avenir Next','Avenir','Montserrat',sans-serif;font-size:13px;line-height:1.4;margin-top:6px;color:rgba(245,241,232,.6)}"

# ---- Herbruikbare cc-mini blokken ----

MINI = {
    "Urban Plaid": '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/urban_plaid.jpg" alt="Urban Plaid" loading="lazy"></div>',
    "Hoogtelijnen": '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/hoogtelijnen.jpg" alt="Hoogtelijnen" loading="lazy"></div>',
    "Japandi": '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/japandi.jpg" alt="Japandi" loading="lazy"></div>',
    "Lijnenspel": '<div class="cc-mini"><img class="cc-photo" src="/static/img/inspiratie/lijnenspel.jpg" alt="Lijnenspel" loading="lazy"></div>',
    "Aardlagen": '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#6f8a4e"></div><div class="cc-band" style="background:#b7a06a"></div><div class="cc-band" style="background:#e6d9b8"></div></div><svg class="cc-acc" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 18 C 25 12, 50 24, 100 15" fill="none" stroke="#e6d9b8" stroke-width="0.9" opacity="0.55"/><path d="M0 31 C 25 25, 50 37, 100 28" fill="none" stroke="#e6d9b8" stroke-width="0.9" opacity="0.55"/><path d="M0 44 C 25 38, 50 50, 100 41" fill="none" stroke="#e6d9b8" stroke-width="0.9" opacity="0.55"/><path d="M0 57 C 25 51, 50 63, 100 54" fill="none" stroke="#e6d9b8" stroke-width="0.9" opacity="0.55"/><path d="M0 70 C 25 64, 50 76, 100 67" fill="none" stroke="#e6d9b8" stroke-width="0.9" opacity="0.55"/><path d="M0 83 C 25 77, 50 89, 100 80" fill="none" stroke="#e6d9b8" stroke-width="0.9" opacity="0.55"/></svg></div>',
    "Botanisch": '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#C9A24A"></div><div class="cc-band" style="background:#a03d5d"></div><div class="cc-band" style="background:#4e7a4e"></div></div><svg class="cc-acc" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><ellipse cx="18" cy="22" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="40" cy="22" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="62" cy="22" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="84" cy="22" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="18" cy="48" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="40" cy="48" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="62" cy="48" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/><ellipse cx="84" cy="48" rx="6" ry="12" fill="#4e7a4e" opacity="0.35"/></svg></div>',
    "Weefstructuren": '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#b89a6a"></div><div class="cc-band" style="background:#8a6a4e"></div><div class="cc-band" style="background:#e6ddc8"></div></div><svg class="cc-acc" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><line x1="0" y1="8" x2="100" y2="8" stroke="#e6ddc8" stroke-width="3" opacity="0.25"/><line x1="0" y1="22" x2="100" y2="22" stroke="#e6ddc8" stroke-width="3" opacity="0.25"/><line x1="0" y1="36" x2="100" y2="36" stroke="#e6ddc8" stroke-width="3" opacity="0.25"/><line x1="0" y1="50" x2="100" y2="50" stroke="#e6ddc8" stroke-width="3" opacity="0.25"/><line x1="8" y1="0" x2="8" y2="100" stroke="#e6ddc8" stroke-width="3" opacity="0.18"/><line x1="22" y1="0" x2="22" y2="100" stroke="#e6ddc8" stroke-width="3" opacity="0.18"/><line x1="36" y1="0" x2="36" y2="100" stroke="#e6ddc8" stroke-width="3" opacity="0.18"/></svg></div>',
    "Neo Bauhaus": '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#1a1a1a"></div><div class="cc-band" style="background:#d4622a"></div><div class="cc-band" style="background:#4a4a4a"></div></div></div>',
    "Vrije vormen": '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#6f8a4e"></div><div class="cc-band" style="background:#C9A24A"></div><div class="cc-band" style="background:#F5F1E8"></div></div></div>',
}


def card(naam, beschrijving):
    return (
        f'        <button class="cc" onclick="event.stopPropagation(); startConcept(\'{naam}\')" aria-label="{naam}">\n'
        f'          {MINI[naam]}\n'
        f'          <div class="cc-name">{naam}</div>\n'
        f'          <div class="cc-desc">{beschrijving}</div>\n'
        f'        </button>\n'
    )


WERKPLEKKEN = [
    ("Urban Plaid", "Modern raster met een warme, textiele uitstraling."),
    ("Neo Bauhaus", "Eigentijdse geometrie voor moderne architectuur en creatieve werkplekken."),
    ("Hoogtelijnen", "Organische contourlijnen die rust en richting geven."),
    ("Japandi", "Minimalistische eenvoud met een rustige, tijdloze uitstraling."),
    ("Weefstructuren", "Geïnspireerd op geweven textiel voor grote kantoorvloeren."),
    ("Aardlagen", "Organische patronen voor representatieve ontvangst- en ontmoetingsruimten."),
]

OVERHEID = [
    ("Urban Plaid", "Professionele, tijdloze basis voor publieke gebouwen."),
    ("Hoogtelijnen", "Rustige contourlijnen voor grote openbare ruimten."),
    ("Weefstructuren", "Warme textiele uitstraling met een duurzaam karakter."),
    ("Aardlagen", "Natuurlijke uitstraling voor ontvangst- en wachtruimten."),
    ("Japandi", "Minimalistische rust voor vergader- en bestuursruimten."),
    ("Neo Bauhaus", "Heldere geometrie voor eigentijdse overheidsarchitectuur."),
]

MUSEA = [
    ("Botanisch", "Organische patronen die verwondering en natuur uitstralen."),
    ("Aardlagen", "Geïnspireerd op landschap, geologie en cultuur."),
    ("Hoogtelijnen", "Contourlijnen die ontdekken en oriëntatie verbeelden."),
    ("Vrije vormen", "Artistieke composities voor culturele ruimtes."),
    ("Neo Bauhaus", "Moderne geometrie voor hedendaagse musea."),
    ("Urban Plaid", "Rustige textielstructuur voor lees- en verblijfsruimten."),
]

HOTELS = [
    ("Neo Deco", "Eigentijdse geometrie met een luxe uitstraling voor hotels en hospitality."),
    ("Aardlagen", "Organische patronen die warmte, rust en natuurlijke elegantie brengen."),
    ("Urban Plaid", "Een verfijnde textielstructuur voor eigentijdse boutique hotels en lounges."),
    ("Botanisch", "Abstracte natuurlijke vormen die een ontspannen en gastvrije sfeer creëren."),
    ("Vrije vormen", "Artistieke composities die lobby's en hospitalityruimten een eigen identiteit geven."),
    ("Neo Bauhaus", "Heldere geometrische vormen voor moderne designhotels en hospitalityconcepten."),
]

# Neo Deco mist nog een MINI-entry (gebruikt momenteel geen foto); voeg toe met bestaand palet
MINI["Neo Deco"] = '<div class="cc-mini"><div class="cc-bands"><div class="cc-band" style="background:#C9A24A"></div><div class="cc-band" style="background:#1A1A1A"></div><div class="cc-band" style="background:#EFE6CF"></div></div><svg class="cc-acc" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="16" fill="none" stroke="#EFE6CF" stroke-width="0.8" opacity="0.7"/></svg></div>'


def build_grid(kaarten):
    html = '        <div class="cc-grid">\n'
    for naam, beschrijving in kaarten:
        html += card(naam, beschrijving)
    html += '        </div>\n'
    return html


PANELEN = {
    "panel_werkplekken_en_kantoren": WERKPLEKKEN,
    "panel_hotels_en_leisure": HOTELS,
    "panel_overheid_en_publieke_gebouwen": OVERHEID,
    "panel_musea_en_bibliotheken": MUSEA,
}


def vervang_paneel(lines, panel_id, kaarten):
    start_idx = None
    for i, line in enumerate(lines):
        if f'id="{panel_id}"' in line:
            start_idx = i
            break
    if start_idx is None:
        return lines, f"FOUT: paneel {panel_id} niet gevonden"

    end_idx = None
    for i in range(start_idx, len(lines)):
        if lines[i].strip() == "</section>":
            end_idx = i
            break
    if end_idx is None:
        return lines, f"FOUT: sluitende </section> voor {panel_id} niet gevonden"

    # Behoud de <section>- en cc-head-regel (regel start_idx), vervang alleen de cc-grid inhoud erna
    section_regel = lines[start_idx]
    cc_head_idx = start_idx + 1
    if 'cc-head' not in lines[cc_head_idx]:
        return lines, f"FOUT: verwachte cc-head-regel niet gevonden direct na {panel_id}"
    cc_head_regel = lines[cc_head_idx]

    nieuw_blok = [section_regel, cc_head_regel, build_grid(kaarten), "      </section>\n"]
    nieuwe_lines = lines[:start_idx] + nieuw_blok + lines[end_idx + 1:]
    return nieuwe_lines, None


def main():
    if not TARGET.exists():
        print(f"FOUT: {TARGET} niet gevonden. Sta je in ~/Desktop/tapijt-studio ?")
        sys.exit(1)

    content = TARGET.read_text(encoding="utf-8")
    if CC_NAME_CSS not in content:
        print("FOUT: verwachte .cc-name CSS-regel niet gevonden, stop voor de veiligheid.")
        sys.exit(1)
    if content.count(CC_NAME_CSS) > 1:
        print("FOUT: .cc-name CSS-regel komt meerdere keren voor, stop voor de veiligheid.")
        sys.exit(1)
    if ".cc-desc{" in content:
        print("FOUT: .cc-desc CSS bestaat al, stop om dubbele registratie te voorkomen.")
        sys.exit(1)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"inspiratie.html.bak_{ts}")
    shutil.copy2(TARGET, backup)
    print(f"Backup gemaakt: {backup}")

    content = content.replace(CC_NAME_CSS, CC_NAME_CSS + CC_DESC_CSS_TOEVOEGING)
    lines = content.splitlines(keepends=True)

    for panel_id, kaarten in PANELEN.items():
        lines, fout = vervang_paneel(lines, panel_id, kaarten)
        if fout:
            print(fout)
            print("Er is nog niets weggeschreven; herstel niet nodig, backup blijft ongebruikt.")
            sys.exit(1)
        print(f"Paneel vervangen: {panel_id} ({len(kaarten)} kaarten)")

    TARGET.write_text("".join(lines), encoding="utf-8")
    print(f"Oude grootte: {backup.stat().st_size} bytes")
    print(f"Nieuwe grootte: {TARGET.stat().st_size} bytes")
    print()
    print("Controleer met:")
    print('  grep -c "cc-desc" templates/inspiratie.html   (verwacht: 25 = 1 CSS-regel + 24 kaarten)')
    print('  grep -c "class=\\"cc\\"" templates/inspiratie.html   (verwacht: 24)')


if __name__ == "__main__":
    main()
