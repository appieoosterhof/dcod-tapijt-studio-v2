content = open('/Users/abmac/Desktop/tapijt-studio/templates/index.html').read()

# Stap 1: Kleurenkiezer toevoegen
kleuren_html = '''      <!-- Kleurenpalet kiezer -->
      <section class="card" id="card-kleuren">
        <h2>Kleurenpalet (optioneel)</h2>
        <p class="hint">Laat leeg voor automatische kleuren, of kies uw eigen palet.</p>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:12px;">
          <div>
            <label style="font-size:11px;color:#666;display:block;margin-bottom:4px;">Achtergrond</label>
            <input type="color" id="kleur0" value="#F5F5F5" style="width:100%;height:36px;border:1px solid #ddd;border-radius:6px;cursor:pointer;padding:2px;">
            <input type="text" id="kleur0hex" value="#F5F5F5" maxlength="7" style="width:100%;margin-top:4px;padding:4px;border:1px solid #ddd;border-radius:4px;font-size:11px;font-family:monospace;text-align:center;">
          </div>
          <div>
            <label style="font-size:11px;color:#666;display:block;margin-bottom:4px;">Primair</label>
            <input type="color" id="kleur1" value="#C4753A" style="width:100%;height:36px;border:1px solid #ddd;border-radius:6px;cursor:pointer;padding:2px;">
            <input type="text" id="kleur1hex" value="#C4753A" maxlength="7" style="width:100%;margin-top:4px;padding:4px;border:1px solid #ddd;border-radius:4px;font-size:11px;font-family:monospace;text-align:center;">
          </div>
          <div>
            <label style="font-size:11px;color:#666;display:block;margin-bottom:4px;">Secundair</label>
            <input type="color" id="kleur2" value="#8B4513" style="width:100%;height:36px;border:1px solid #ddd;border-radius:6px;cursor:pointer;padding:2px;">
            <input type="text" id="kleur2hex" value="#8B4513" maxlength="7" style="width:100%;margin-top:4px;padding:4px;border:1px solid #ddd;border-radius:4px;font-size:11px;font-family:monospace;text-align:center;">
          </div>
          <div>
            <label style="font-size:11px;color:#666;display:block;margin-bottom:4px;">Accent 1</label>
            <input type="color" id="kleur3" value="#D4A055" style="width:100%;height:36px;border:1px solid #ddd;border-radius:6px;cursor:pointer;padding:2px;">
            <input type="text" id="kleur3hex" value="#D4A055" maxlength="7" style="width:100%;margin-top:4px;padding:4px;border:1px solid #ddd;border-radius:4px;font-size:11px;font-family:monospace;text-align:center;">
          </div>
          <div>
            <label style="font-size:11px;color:#666;display:block;margin-bottom:4px;">Accent 2</label>
            <input type="color" id="kleur4" value="#F0C080" style="width:100%;height:36px;border:1px solid #ddd;border-radius:6px;cursor:pointer;padding:2px;">
            <input type="text" id="kleur4hex" value="#F0C080" maxlength="7" style="width:100%;margin-top:4px;padding:4px;border:1px solid #ddd;border-radius:4px;font-size:11px;font-family:monospace;text-align:center;">
          </div>
        </div>
        <label style="display:flex;align-items:center;gap:8px;font-size:14px;cursor:pointer;">
          <input type="checkbox" id="gebruikKleuren" style="width:16px;height:16px;accent-color:#4A7C3F;">
          Gebruik mijn kleuren (overschrijft AI kleuren)
        </label>
      </section>

      <!-- Genereer knop -->'''

if '<!-- Kleurenpalet kiezer -->' not in content:
    content = content.replace('      <!-- Genereer knop -->', kleuren_html)
    print("Kleurenkiezer toegevoegd!")
else:
    print("Kleurenkiezer al aanwezig")

# Stap 2: Stijlknoppen uitbreiden
old_chips = "          <button class=\"chip\" onclick=\"setPrompt('Tribal geometrisch patroon, aardetinten, handgeweven uitstraling')\">Tribal</button>"
new_chips = """          <button class="chip" onclick="setPrompt('Tribal geometrisch patroon, aardetinten, handgeweven uitstraling')">Tribal</button>
          <button class="chip" onclick="setPrompt('Alleen cirkels, strak en minimalistisch')">Cirkels</button>
          <button class="chip" onclick="setPrompt('Alleen ruiten en diamanten, geometrisch')">Ruiten</button>
          <button class="chip" onclick="setPrompt('Alleen sterren, strak patroon')">Sterren</button>
          <button class="chip" onclick="setPrompt('Hexagonaal patroon, honingraat structuur')">Hexagonen</button>
          <button class="chip" onclick="setPrompt('Vrije organische vormen, vloeiend en natuurlijk')">Vrije vormen</button>
          <button class="chip" onclick="setPrompt('Japandi minimalistisch, bamboe en natuurlijke lijnen, rustige tinten')">Japandi</button>
          <button class="chip" onclick="setPrompt('Art Deco geometrisch, goud en zwart, jaren 20 stijl')">Art Deco</button>
          <button class="chip" onclick="setPrompt('Terrazzo patroon, gekleurde steensnippers op lichte ondergrond')">Terrazzo</button>"""

if 'Cirkels' not in content:
    content = content.replace(old_chips, new_chips)
    print("Stijlknoppen bijgewerkt!")
else:
    print("Stijlknoppen al aanwezig")

open('/Users/abmac/Desktop/tapijt-studio/templates/index.html', 'w').write(content)
print("HTML opgeslagen!")
