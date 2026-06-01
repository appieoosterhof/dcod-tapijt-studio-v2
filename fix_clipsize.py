content = open('app.py').read()

old = '    <clipPath id="canvas">\n      <rect width="{total_w}" height="{total_h}"/>\n    </clipPath>'
new = '    <clipPath id="clipCanvas">\n      <rect x="0" y="0" width="{total_w}" height="{total_h}"/>\n    </clipPath>'

content2 = content.replace('url(#canvas)', 'url(#clipCanvas)')
content2 = content2.replace(old, new)
open('app.py', 'w').write(content2)
print("Klaar!")
