content = open('app.py').read()

idx = content.find('def build_repeat_svg')
end = content.find('\n# ───', idx)
if end == -1:
    end = content.find('\ndef ', idx + 100)

old_func = content[idx:end]

new_func = '''def build_repeat_svg(tile_svg: str, analysis: dict,
                     tile_cm: int, repeat_type: str,
                     dpi: int, cols: int = 3, rows: int = 3) -> str:
    """Bouw een all-over repeat SVG met het opgegeven repeat-type."""
    T = 400
    bg_color = analysis.get('background_color', '#F5F5F5')
    total_w = T * cols
    total_h = T * rows

    inner_start = tile_svg.index(">", tile_svg.index("<svg")) + 1
    inner_end = tile_svg.rindex("</svg>")
    inner_content = tile_svg[inner_start:inner_end].strip()

    tiles = []
    clip_defs = []
    clip_id = 0

    for r in range(-1, rows + 2):
        for c in range(-1, cols + 2):
            x = c * T
            y = r * T
            if repeat_type == "half-drop":
                y += (c % 2) * (T // 2)
            elif repeat_type == "brick":
                x += (r % 2) * (T // 2)

            if repeat_type == "mirror":
                sx = -1 if c % 2 == 1 else 1
                sy = -1 if r % 2 == 1 else 1
                tx = x + (T if sx == -1 else 0)
                ty = y + (T if sy == -1 else 0)
                transform = f"translate({tx},{ty}) scale({sx},{sy})"
            else:
                transform = f"translate({x},{y})"

            cid = f"c{clip_id}"
            clip_id += 1
            clip_defs.append(f\'\'\'<clipPath id="{cid}"><rect x="0" y="0" width="{T}" height="{T}"/></clipPath>\'\'\')
            tiles.append(f\'\'\'<g transform="{transform}" clip-path="url(#{cid})">{inner_content}</g>\'\'\')

    px_w = round(total_w / 400 * (tile_cm / 2.54 * dpi))
    px_h = round(total_h / 400 * (tile_cm / 2.54 * dpi))

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {total_w} {total_h}"
     width="{px_w}px" height="{px_h}px">
  <defs>
    <clipPath id="canvas"><rect width="{total_w}" height="{total_h}"/></clipPath>
    {"".join(clip_defs)}
  </defs>
  <rect width="{total_w}" height="{total_h}" fill="{bg_color}"/>
  <g clip-path="url(#canvas)">{"".join(tiles)}</g>
</svg>"""
    return svg

'''

open('app.py', 'w').write(content.replace(old_func, new_func))
print("Functie herschreven!")
