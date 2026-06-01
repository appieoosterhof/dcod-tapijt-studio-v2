import re

content = open('/Users/abmac/Desktop/tapijt-studio/templates/index.html').read()

kleuren_labels = ['Achtergrond', 'Primair', 'Secundair', 'Accent 1', 'Accent 2']
defaults_hex = ['#F5F5F5', '#C4753A', '#8B4513', '#D4A055', '#F0C080']
defaults_rgb = [
    (245, 245, 245),
    (196, 117, 58),
    (139, 69, 19),
    (212, 160, 85),
    (240, 192, 128)
]

nieuw_palet = '''      <!-- Kleurenpalet kiezer -->
      <section class="card" id="card-kleuren">
        <h2>Kleurenpalet (optioneel)</h2>
        <p class="hint">Laat leeg voor automatische kleuren, of kies uw eigen palet.</p>
'''

for i, (label, hex_val, rgb) in enumerate(zip(kleuren_labels, defaults_hex, defaults_rgb)):
    r, g, b = rgb
    nieuw_palet += f'''        <div style="margin-bottom:14px;padding:10px;border:1px solid #eee;border-radius:8px;background:#fafafa;">
          <div style="display:flex;align-items:center;gap:12px;">
            <input type="color" id="kleur{i}" value="{hex_val}" style="width:48px;height:40px;border:1px solid #ddd;border-radius:6px;cursor:pointer;padding:2px;flex-shrink:0;">
            <div style="flex:1;">
              <label style="font-size:12px;color:#666;font-weight:bold;display:block;margin-bottom:6px;">{label}</label>
              <div style="display:flex;gap:8px;align-items:center;">
                <div style="flex:1.2;">
                  <label style="font-size:10px;color:#999;display:block;margin-bottom:2px;">HEX</label>
                  <input type="text" id="kleur{i}hex" value="{hex_val}" maxlength="7" placeholder="#HEX" style="width:100%;padding:6px;border:1px solid #ddd;border-radius:4px;font-size:12px;font-family:monospace;text-align:center;box-sizing:border-box;">
                </div>
                <div style="flex:1;">
                  <label style="font-size:10px;color:#999;display:block;margin-bottom:2px;">R</label>
                  <input type="number" id="kleur{i}r" value="{r}" min="0" max="255" style="width:100%;padding:6px;border:1px solid #ddd;border-radius:4px;font-size:12px;text-align:center;box-sizing:border-box;">
                </div>
                <div style="flex:1;">
                  <label style="font-size:10px;color:#999;display:block;margin-bottom:2px;">G</label>
                  <input type="number" id="kleur{i}g" value="{g}" min="0" max="255" style="width:100%;padding:6px;border:1px solid #ddd;border-radius:4px;font-size:12px;text-align:center;box-sizing:border-box;">
                </div>
                <div style="flex:1;">
                  <label style="font-size:10px;color:#999;display:block;margin-bottom:2px;">B</label>
                  <input type="number" id="kleur{i}b" value="{b}" min="0" max="255" style="width:100%;padding:6px;border:1px solid #ddd;border-radius:4px;font-size:12px;text-align:center;box-sizing:border-box;">
                </div>
              </div>
            </div>
          </div>
        </div>
'''

nieuw_palet += '''        <label style="display:flex;align-items:center;gap:8px;font-size:14px;cursor:pointer;margin-top:8px;">
          <input type="checkbox" id="gebruikKleuren" style="width:16px;height:16px;accent-color:#4A7C3F;">
          Gebruik mijn kleuren (overschrijft AI kleuren)
        </label>
      </section>

      <!-- Genereer knop -->'''

old_pattern = r'      <!-- Kleurenpalet kiezer -->.*?<!-- Genereer knop -->'
if re.search(old_pattern, content, re.DOTALL):
    content = re.sub(old_pattern, nieuw_palet, content, flags=re.DOTALL)
    print("Kleurenkiezer bijgewerkt!")
else:
    print("Niet gevonden")

open('/Users/abmac/Desktop/tapijt-studio/templates/index.html', 'w').write(content)
print("HTML opgeslagen!")
