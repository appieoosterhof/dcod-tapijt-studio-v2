content = open('/Users/abmac/Desktop/tapijt-studio/templates/index.html').read()

kleuren_labels = ['Achtergrond', 'Primair', 'Secundair', 'Accent 1', 'Accent 2']
defaults_hex = ['#F5F5F5', '#C4753A', '#8B4513', '#D4A055', '#F0C080']
defaults_rgb = ['245,245,245', '196,117,58', '139,69,19', '212,160,85', '240,192,128']

nieuw_palet = '''      <!-- Kleurenpalet kiezer -->
      <section class="card" id="card-kleuren">
        <h2>Kleurenpalet (optioneel)</h2>
        <p class="hint">Laat leeg voor automatische kleuren, of kies uw eigen palet.</p>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:12px;">
'''

for i, (label, hex_val, rgb_val) in enumerate(zip(kleuren_labels, defaults_hex, defaults_rgb)):
    nieuw_palet += f'''          <div>
            <label style="font-size:11px;color:#666;display:block;margin-bottom:4px;">{label}</label>
            <input type="color" id="kleur{i}" value="{hex_val}" style="width:100%;height:36px;border:1px solid #ddd;border-radius:6px;cursor:pointer;padding:2px;">
            <input type="text" id="kleur{i}hex" value="{hex_val}" maxlength="7" placeholder="HEX" style="width:100%;margin-top:4px;padding:4px;border:1px solid #ddd;border-radius:4px;font-size:10px;font-family:monospace;text-align:center;">
            <input type="text" id="kleur{i}rgb" value="{rgb_val}" placeholder="R,G,B" style="width:100%;margin-top:4px;padding:4px;border:1px solid #ddd;border-radius:4px;font-size:10px;font-family:monospace;text-align:center;">
          </div>
'''

nieuw_palet += '''        </div>
        <label style="display:flex;align-items:center;gap:8px;font-size:14px;cursor:pointer;">
          <input type="checkbox" id="gebruikKleuren" style="width:16px;height:16px;accent-color:#4A7C3F;">
          Gebruik mijn kleuren (overschrijft AI kleuren)
        </label>
      </section>

      <!-- Genereer knop -->'''

# Verwijder oude kleurenkiezer en vervang
import re
old_pattern = r'      <!-- Kleurenpalet kiezer -->.*?<!-- Genereer knop -->'
if re.search(old_pattern, content, re.DOTALL):
    content = re.sub(old_pattern, nieuw_palet, content, flags=re.DOTALL)
    print("Kleurenkiezer bijgewerkt met RGB!")
else:
    print("Niet gevonden")

open('/Users/abmac/Desktop/tapijt-studio/templates/index.html', 'w').write(content)
print("HTML opgeslagen!")
