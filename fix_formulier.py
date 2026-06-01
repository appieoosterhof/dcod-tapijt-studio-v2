content = open('static/js/app.js').read()

# Fix 1: Sluit knop na verzenden
old = '''document.getElementById('bestelModal').innerHTML = '<div style=\\"background:white;padding:40px;border-radius:12px;text-align:center;max-width:400px;\\"><div style=\\"font-size:48px;\\">\\u2713</div><h2 style=\\"color:#4A7C3F;\\">Aanvraag verzonden!</h2><p>Wij nemen binnen 2 werkdagen contact met u op.</p><button onclick=\\"document.getElementById(\\\\\\\"bestelModal\\\\\\\").style.display=\\\\\\\"none\\\\\\\"\\" style=\\"margin-top:20px;padding:12px 32px;background:#4A7C3F;color:white;border:none;border-radius:8px;cursor:pointer;font-size:16px;\\">Sluiten</button></div>';'''

new = '''document.getElementById('bestelModal').style.display = 'none';
      alert('Uw aanvraag is verzonden! U ontvangt een kopie per e-mail. Wij nemen binnen 2 werkdagen contact met u op.');'''

content = content.replace(old, new)

# Fix 2: Betere validatie melding
old2 = "    document.getElementById('bestelFout').textContent = 'Vul minimaal naam en e-mail in.';"
new2 = "    document.getElementById('bestelFout').textContent = 'Vul uw naam en e-mailadres in zodat wij u kunnen bereiken.';"

content = content.replace(old2, new2)

open('static/js/app.js', 'w').write(content)
print("Stap 1 klaar!")
