import re

content = open('/Users/abmac/Desktop/tapijt-studio/app.py').read()

# Vind de functie
idx_start = content.find('def generate_geometric_svg')
idx_end = content.find('\ndef ', idx_start + 100)

old_func = content[idx_start:idx_end]

new_func = '''def generate_geometric_svg(palette: dict, tile_size: int, complexity: str, shape_list: list = None) -> str:
    T = tile_size
    bg = palette["background"]
    c1 = palette["primary"]
    c2 = palette["secondary"]
    c3 = palette["accent1"]
    c4 = palette["accent2"]
    step = T // 4 if complexity == "high" else T // 3 if complexity == "medium" else T // 2
    if not shape_list:
        shape_list = ["octagon"]
    svgs = []
    colors = [c1, c2, c3, c4]
    for row in range(0, T, step):
        for col in range(0, T, step):
            cx, cy = col + step // 2, row + step // 2
            r = step * 0.42
            idx = (row // step + col // step) % len(colors)
            fill = colors[idx]
            shape = shape_list[(row // step * (T // step) + col // step) % len(shape_list)]

            if shape == "circle":
                svgs.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{c2}" stroke-width="1"/>')
                svgs.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.4:.1f}" fill="{bg}" stroke="{c2}" stroke-width="0.5"/>')

            elif shape == "square":
                x0, y0 = cx - r, cy - r
                svgs.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{r*2:.1f}" height="{r*2:.1f}" fill="{fill}" stroke="{c2}" stroke-width="1"/>')
                svgs.append(f'<rect x="{cx-r*0.4:.1f}" y="{cy-r*0.4:.1f}" width="{r*0.8:.1f}" height="{r*0.8:.1f}" fill="{bg}" stroke="{c2}" stroke-width="0.5"/>')

            elif shape == "triangle":
                pts = f"{cx:.1f},{cy-r:.1f} {cx+r:.1f},{cy+r:.1f} {cx-r:.1f},{cy+r:.1f}"
                svgs.append(f'<polygon points="{pts}" fill="{fill}" stroke="{c2}" stroke-width="1"/>')

            elif shape == "diamond":
                pts = f"{cx:.1f},{cy-r:.1f} {cx+r:.1f},{cy:.1f} {cx:.1f},{cy+r:.1f} {cx-r:.1f},{cy:.1f}"
                svgs.append(f'<polygon points="{pts}" fill="{fill}" stroke="{c2}" stroke-width="1"/>')
                ri = r * 0.45
                inner = f"{cx:.1f},{cy-ri:.1f} {cx+ri:.1f},{cy:.1f} {cx:.1f},{cy+ri:.1f} {cx-ri:.1f},{cy:.1f}"
                svgs.append(f'<polygon points="{inner}" fill="{bg}" stroke="{c2}" stroke-width="0.5"/>')

            elif shape == "hexagon":
                pts = []
                for k in range(6):
                    angle = math.radians(k * 60 + 30)
                    pts.append(f"{cx + r * math.cos(angle):.1f},{cy + r * math.sin(angle):.1f}")
                svgs.append(f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{c2}" stroke-width="1"/>')

            elif shape == "star":
                pts = []
                for k in range(10):
                    angle = math.radians(k * 36 - 90)
                    rad = r if k % 2 == 0 else r * 0.45
                    pts.append(f"{cx + rad * math.cos(angle):.1f},{cy + rad * math.sin(angle):.1f}")
                svgs.append(f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{c2}" stroke-width="1"/>')

            else:
                # Standaard achthoek
                pts = []
                for k in range(8):
                    angle = math.radians(k * 45 + 22.5)
                    pts.append(f"{cx + r * math.cos(angle):.1f},{cy + r * math.sin(angle):.1f}")
                fill2 = c1 if (row // step + col // step) % 2 == 0 else c3
                svgs.append(f'<polygon points="{" ".join(pts)}" fill="{fill2}" stroke="{c2}" stroke-width="1"/>')
                ri = r * 0.45
                inner = [f"{cx:.1f},{cy-ri:.1f}", f"{cx+ri:.1f},{cy:.1f}", f"{cx:.1f},{cy+ri:.1f}", f"{cx-ri:.1f},{cy:.1f}"]
                svgs.append(f'<polygon points="{" ".join(inner)}" fill="{c4}" stroke="{c2}" stroke-width="0.5"/>')
                svgs.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.12:.1f}" fill="{c2}"/>')

    return "\\n".join(svgs)

'''

content = content[:idx_start] + new_func + content[idx_end:]
open('/Users/abmac/Desktop/tapijt-studio/app.py', 'w').write(content)
print("Functie herschreven!")
