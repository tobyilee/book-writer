#!/usr/bin/env python3
"""Generate book cover for '잊지 않는 기술'.
Concept A: minimalist symbol (classical arch + neural constellation) on deep navy.
Output: 1600x2560 PNG.
"""
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path("/Users/tobylee/workspace/ai/book-writer/memory-mastery/cover.png")
W, H = 1600, 2560

# Color palette — deep navy + warm gold
BG_TOP = (15, 18, 42)
BG_BOT = (32, 24, 64)
GOLD = (212, 168, 96)
GOLD_DIM = (140, 110, 60)
WHITE = (245, 240, 232)
SUBTLE = (180, 165, 200)

FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"


def vertical_gradient(w, h, top, bot):
    img = Image.new("RGB", (w, h), top)
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        t = t * t * (3 - 2 * t)
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


def draw_starfield(draw, w, h, count=140):
    rnd = random.Random(42)
    for _ in range(count):
        x = rnd.randint(0, w - 1)
        y = rnd.randint(0, int(h * 0.65))
        s = rnd.choice([1, 1, 1, 2, 2, 3])
        a = rnd.randint(60, 180)
        c = (WHITE[0], WHITE[1], WHITE[2], a)
        draw.ellipse([x, y, x + s, y + s], fill=c)


def draw_arch_silhouette(canvas, cx, cy, width, height):
    """Classical arched portico — columns + arch. Drawn on RGBA overlay."""
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # base platform
    plinth_h = 18
    d.rectangle(
        [cx - width // 2 - 40, cy + height // 2,
         cx + width // 2 + 40, cy + height // 2 + plinth_h],
        fill=GOLD,
    )
    d.rectangle(
        [cx - width // 2 - 60, cy + height // 2 + plinth_h,
         cx + width // 2 + 60, cy + height // 2 + plinth_h + 8],
        fill=GOLD_DIM,
    )

    # 4 columns
    n_cols = 4
    col_w = 38
    span = width
    left = cx - span // 2
    right = cx + span // 2
    col_top = cy - height // 2 + 220
    col_bot = cy + height // 2
    for i in range(n_cols):
        x = left + (right - left) * i / (n_cols - 1)
        d.rectangle([x - col_w // 2 - 6, col_top - 14, x + col_w // 2 + 6, col_top], fill=GOLD)
        d.rectangle([x - col_w // 2, col_top, x + col_w // 2, col_bot], fill=GOLD)
        for k in (-1, 0, 1):
            fx = x + k * (col_w // 4)
            d.line([(fx, col_top + 6), (fx, col_bot - 6)], fill=GOLD_DIM, width=1)

    # entablature
    beam_top = col_top - 40
    beam_bot = col_top - 14
    d.rectangle([left - 30, beam_top, right + 30, beam_bot], fill=GOLD)

    # central arch (semi-circle outline)
    arch_w = int(width * 0.55)
    arch_h = 220
    ax0 = cx - arch_w // 2
    ax1 = cx + arch_w // 2
    ay0 = beam_top - arch_h
    ay1 = beam_top + arch_h

    arch_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ad = ImageDraw.Draw(arch_layer)
    ad.ellipse([ax0, ay0, ax1, ay1], outline=GOLD, width=10)

    # crop mask: keep only the upper half (above beam_top)
    mask = Image.new("L", canvas.size, 0)
    md = ImageDraw.Draw(mask)
    md.rectangle([0, 0, canvas.size[0], beam_top], fill=255)
    masked = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    masked.paste(arch_layer, (0, 0), mask)
    layer = Image.alpha_composite(layer, masked)

    # inner faint arch
    arch_layer2 = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ad2 = ImageDraw.Draw(arch_layer2)
    ad2.ellipse([ax0 + 18, ay0 + 18, ax1 - 18, ay1 - 18], outline=GOLD_DIM, width=2)
    masked2 = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    masked2.paste(arch_layer2, (0, 0), mask)
    layer = Image.alpha_composite(layer, masked2)

    # keystone — square at the top of the arch
    ks_w, ks_h = 26, 30
    ks_cx = cx
    ks_cy = ay0 + arch_h - 10  # near apex of arch
    kd = ImageDraw.Draw(layer)
    kd.rectangle([ks_cx - ks_w // 2, ks_cy - ks_h // 2,
                  ks_cx + ks_w // 2, ks_cy + ks_h // 2], fill=GOLD)

    # focus point above the arch — used for neural network origin
    focus = (cx, ay0 + arch_h - 40)
    return layer, focus


def draw_neural_constellation(canvas, origin, n_nodes=18, seed=11):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rnd = random.Random(seed)

    ox, oy = origin
    nodes = [(ox, oy)]
    for _ in range(n_nodes):
        ang = rnd.uniform(-math.pi * 0.95, -math.pi * 0.05)
        rad = rnd.uniform(160, 760)
        x = ox + math.cos(ang) * rad
        y = oy + math.sin(ang) * rad * 0.85
        x = max(140, min(canvas.size[0] - 140, x))
        y = max(140, min(oy - 50, y))
        nodes.append((x, y))

    # connect each node to 1-2 nearest others
    for i, (x, y) in enumerate(nodes):
        others = sorted(
            [(j, math.hypot(x - nx, y - ny)) for j, (nx, ny) in enumerate(nodes) if j != i],
            key=lambda t: t[1],
        )
        k = 2 if i == 0 else rnd.choice([1, 1, 2])
        for j, _dist in others[:k]:
            x2, y2 = nodes[j]
            d.line([(x, y), (x2, y2)], fill=(GOLD[0], GOLD[1], GOLD[2], 110), width=2)

    # nodes with halo
    for i, (x, y) in enumerate(nodes):
        r = 6 if i == 0 else rnd.choice([3, 4, 4, 5, 6])
        for hr, ha in [(r + 8, 28), (r + 4, 60)]:
            d.ellipse([x - hr, y - hr, x + hr, y + hr],
                      fill=(GOLD[0], GOLD[1], GOLD[2], ha))
        d.ellipse([x - r, y - r, x + r, y + r], fill=GOLD)

    layer = layer.filter(ImageFilter.GaussianBlur(radius=0.6))
    return layer


def main():
    # background gradient
    bg = vertical_gradient(W, H, BG_TOP, BG_BOT)

    # vignette
    vignette = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse([-W // 4, -H // 4, W + W // 4, H + H // 4], fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=300))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    bg = Image.composite(bg, dark, vignette)

    # starfield overlay
    star_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(star_layer)
    draw_starfield(sd, W, H, count=180)
    bg_rgba = bg.convert("RGBA")
    bg_rgba = Image.alpha_composite(bg_rgba, star_layer)

    # arch silhouette
    arch_cx = W // 2
    arch_cy = int(H * 0.62)
    arch_w = 720
    arch_h = 720
    arch_layer, focus = draw_arch_silhouette(bg_rgba, arch_cx, arch_cy, arch_w, arch_h)
    arch_layer = arch_layer.filter(ImageFilter.GaussianBlur(radius=0.4))
    bg_rgba = Image.alpha_composite(bg_rgba, arch_layer)

    # neural constellation emanating upward from arch focus
    network = draw_neural_constellation(bg_rgba, focus, n_nodes=18)
    bg_rgba = Image.alpha_composite(bg_rgba, network)

    # soft golden glow around the arch keystone
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gx, gy = focus
    for r, a in [(280, 30), (190, 44), (120, 64)]:
        gd.ellipse([gx - r, gy - r, gx + r, gy + r],
                   fill=(GOLD[0], GOLD[1], GOLD[2], a))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=40))
    bg_rgba = Image.alpha_composite(bg_rgba, glow)

    # typography layer
    txt_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt_layer)

    def load_font(size, index=0):
        try:
            return ImageFont.truetype(FONT_PATH, size, index=index)
        except Exception:
            return ImageFont.truetype(FONT_PATH, size)

    # AppleSDGothicNeo.ttc weights: 0=Thin..8=Heavy
    title_font = load_font(220, index=8)
    sub_font = load_font(64, index=3)
    author_font = load_font(48, index=4)
    label_font = load_font(34, index=5)

    # top decorative label
    label = "MEMORY  ·  기억 설계"
    bbox = td.textbbox((0, 0), label, font=label_font)
    lw = bbox[2] - bbox[0]
    label_y = 240
    line_y = label_y + (bbox[3] - bbox[1]) // 2 + 4
    side_pad = 60
    line_len = (W - lw) // 2 - side_pad - 30
    td.line([(side_pad, line_y), (side_pad + line_len, line_y)],
            fill=(GOLD[0], GOLD[1], GOLD[2], 200), width=2)
    td.line([(W - side_pad - line_len, line_y), (W - side_pad, line_y)],
            fill=(GOLD[0], GOLD[1], GOLD[2], 200), width=2)
    td.text(((W - lw) // 2 - bbox[0], label_y),
            label, font=label_font, fill=(GOLD[0], GOLD[1], GOLD[2], 230))

    # Title — two lines for hierarchy
    title_l1 = "잊지 않는"
    title_l2 = "기술"
    y_t1 = 360
    bbox1 = td.textbbox((0, 0), title_l1, font=title_font)
    tw1 = bbox1[2] - bbox1[0]
    td.text(((W - tw1) // 2 - bbox1[0], y_t1), title_l1, font=title_font, fill=WHITE)
    y_t2 = y_t1 + (bbox1[3] - bbox1[1]) + 30
    bbox2 = td.textbbox((0, 0), title_l2, font=title_font)
    tw2 = bbox2[2] - bbox2[0]
    td.text(((W - tw2) // 2 - bbox2[0], y_t2), title_l2, font=title_font, fill=GOLD)

    # subtitle
    subtitle = "기억의 궁전부터 AI 카드까지"
    y_sub = y_t2 + (bbox2[3] - bbox2[1]) + 60
    bbox_s = td.textbbox((0, 0), subtitle, font=sub_font)
    sw = bbox_s[2] - bbox_s[0]
    td.text(((W - sw) // 2 - bbox_s[0], y_sub), subtitle, font=sub_font, fill=SUBTLE)
    rule_y = y_sub + (bbox_s[3] - bbox_s[1]) + 28
    rule_w = 120
    td.line([((W - rule_w) // 2, rule_y), ((W + rule_w) // 2, rule_y)],
            fill=GOLD, width=3)

    # author
    author = "Toby-AI"
    bbox_a = td.textbbox((0, 0), author, font=author_font)
    aw = bbox_a[2] - bbox_a[0]
    y_a = H - 180
    td.text(((W - aw) // 2 - bbox_a[0], y_a), author, font=author_font,
            fill=(WHITE[0], WHITE[1], WHITE[2], 230))

    bg_rgba = Image.alpha_composite(bg_rgba, txt_layer)

    final = bg_rgba.convert("RGB")
    final.save(OUT, "PNG", optimize=True)
    print(f"Saved: {OUT} ({final.size[0]}x{final.size[1]})")


if __name__ == "__main__":
    main()
