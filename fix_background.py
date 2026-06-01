content = open('app.py').read()

old = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {total_w} {total_h}"
     width="{px_w}px" height="{px_h}px">
  <defs>'''

new = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {total_w} {total_h}"
     width="{px_w}px" height="{px_h}px">
  <rect width="100%" height="100%" fill="{bg_color}"/>
  <defs>'''

if old in content:
    open('app.py', 'w').write(content.replace(old, new))
    print("Fix toegepast!")
else:
    print("Niet gevonden - andere aanpak nodig")
