content = open('app.py').read()

old = "        afmeting = data.get('afmeting', 'Niet opgegeven')"
new = """        afmeting = data.get('afmeting', 'Niet opgegeven')
        staaltje = data.get('staaltje', 'Nee')
        adres = data.get('adres', '')"""

old2 = "            <tr><td style=\"padding:8px;background:#E8F0E6;font-weight:bold\">Wensen</td><td style=\"padding:8px\">{wensen}</td></tr>\n            </table></body></html>\"\"\""
new2 = """            <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Wensen</td><td style="padding:8px">{wensen}</td></tr>
            <tr><td style="padding:8px;background:#E8F0E6;font-weight:bold">Staaltje</td><td style="padding:8px">{staaltje}{(' — ' + adres) if adres else ''}</td></tr>
            </table></body></html>"""

old3 = '            <h2 style="color:#4A7C3F;">Bedankt voor uw aanvraag!</h2>'
new3 = '            <p style="color:#666;font-style:italic;">Hierbij een kopie van uw aanvraag.</p>\n            <h2 style="color:#4A7C3F;">Bedankt voor uw aanvraag!</h2>'

content = content.replace(old, new).replace(old2, new2).replace(old3, new3)
open('app.py', 'w').write(content)
print("Stap 4 klaar!")
