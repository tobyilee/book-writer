"""Cover renderer for 에이전틱 코딩의 시대.

Generates 1600x2560 PNG at {slug}/cover.png with:
- deep navy background + subtle vignette
- engineering grid in lower half
- flowing gold/coral curves crossing the grid
- Pretendard typography stack for title/subtitle/copy/author
"""

from __future__ import annotations

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path("/Users/tobylee/workspace/ai/book-writer/agentic-coding-harness-engineering/cover.png")
W, H = 1600, 2560

NAVY = (10, 22, 40)            # #0A1628 base
NAVY_DEEP = (6, 14, 28)        # vignette outer
GRID = (62, 86, 124, 90)       # muted slate blue, alpha
GRID_STRONG = (96, 130, 178, 140)
GOLD = (212, 165, 116)         # #D4A574
GOLD_GLOW = (212, 165, 116, 50)
CORAL = (224, 122, 95)         # #E07A5F
SLATE = (170, 188, 214)        # subtitle ink
WHITE = (245, 247, 250)

FONTS = Path("/Users/tobylee/Library/Fonts")
F_BLACK = str(FONTS / "Pretendard-Black.otf")
F_BOLD = str(FONTS / "Pretendard-Bold.otf")
F_SEMI = str(FONTS / "Pretendard-SemiBold.otf")
F_MED = str(FONTS / "Pretendard-Medium.otf")
F_LIGHT = str(FONTS / "Pretendard-Light.otf")


def vertical_gradient(size, top, bottom):
    img = Image.new("RGB", size, top)
    px = img.load()
    w, h = size
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


def radial_vignette(size, strength=0.55):
    """darken corners; transparent center."""
    w, h = size
    mask = Image.new("L", size, 0)
    px = mask.load()
    cx, cy = w / 2, h / 2
    max_d = math.hypot(cx, cy)
    for y in range(h):
        for x in range(w):
            d = math.hypot(x - cx, y - cy) / max_d
            v = max(0.0, (d - 0.45)) / 0.55  # start fade at 45% radius
            px[x, y] = int(min(255, v * 255 * strength))
    return mask


def draw_grid(layer: Image.Image):
    """draw an engineering grid in the lower portion. perspective-light: grid stays orthographic but fades upward."""
    draw = ImageDraw.Draw(layer, "RGBA")
    grid_top = int(H * 0.50)
    grid_bottom = H - 60
    cell = 64
    # vertical lines
    for x in range(60, W - 60, cell):
        # alpha modulated by horizontal position (slightly stronger at center)
        for y in range(grid_top, grid_bottom, 2):
            t = (y - grid_top) / (grid_bottom - grid_top)
            alpha = int(40 + 80 * t)  # stronger near bottom
            draw.point((x, y), fill=(GRID[0], GRID[1], GRID[2], alpha))
    # horizontal lines
    for y in range(grid_top, grid_bottom, cell):
        t = (y - grid_top) / (grid_bottom - grid_top)
        alpha = int(40 + 80 * t)
        draw.line([(60, y), (W - 60, y)], fill=(GRID[0], GRID[1], GRID[2], alpha), width=1)
    # accent intersections — small plus marks every 3rd cell
    for y in range(grid_top, grid_bottom, cell * 3):
        for x in range(60 + cell, W - 60, cell * 3):
            t = (y - grid_top) / (grid_bottom - grid_top)
            a = int(120 + 100 * t)
            draw.line([(x - 6, y), (x + 6, y)], fill=(GRID_STRONG[0], GRID_STRONG[1], GRID_STRONG[2], a), width=1)
            draw.line([(x, y - 6), (x, y + 6)], fill=(GRID_STRONG[0], GRID_STRONG[1], GRID_STRONG[2], a), width=1)


def bezier(p0, p1, p2, p3, steps=400):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0]
        y = u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1]
        pts.append((x, y))
    return pts


def draw_glow_curve(size, points, color, width, glow_radius=28, glow_alpha=80):
    """draw a curve with a soft glow."""
    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.line(points, fill=(color[0], color[1], color[2], glow_alpha), width=width + 14, joint="curve")
    glow = glow.filter(ImageFilter.GaussianBlur(glow_radius))

    core = Image.new("RGBA", size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(core)
    cd.line(points, fill=(color[0], color[1], color[2], 230), width=width, joint="curve")
    return Image.alpha_composite(glow, core)


def draw_curves(layer: Image.Image):
    # flowing curves spanning the lower 2/3, sweeping diagonally.
    # spread vertically from just below the english subtitle (~1320) down to ~2280
    # so the curves visually bridge title and author block.
    curves = [
        # (color, width, control points)
        (GOLD,  7, [(-80, 1480), (500, 1340), (1100, 1640), (W + 80, 1420)]),
        (CORAL, 5, [(-40, 1620), (600, 1900), (1000, 1380), (W + 40, 1700)]),
        (GOLD,  5, [(-80, 1820), (500, 1620), (1100, 2020), (W + 80, 1760)]),
        (GOLD,  4, [(-60, 2050), (450, 1850), (1180, 2200), (W + 60, 1980)]),
        (CORAL, 4, [(-40, 2200), (600, 2400), (1000, 1980), (W + 40, 2240)]),
        (GOLD,  3, [(-40, 2330), (550, 2160), (1050, 2380), (W + 40, 2200)]),
    ]
    for color, width, ctrl in curves:
        pts = bezier(*ctrl, steps=600)
        glow_layer = draw_glow_curve((W, H), pts, color, width, glow_radius=36, glow_alpha=80)
        layer.alpha_composite(glow_layer)


def draw_corner_marks(layer: Image.Image):
    """thin tick marks in corners — engineering-drawing feel."""
    d = ImageDraw.Draw(layer, "RGBA")
    pad = 60
    L = 32
    col = (GOLD[0], GOLD[1], GOLD[2], 180)
    # top-left
    d.line([(pad, pad), (pad + L, pad)], fill=col, width=2)
    d.line([(pad, pad), (pad, pad + L)], fill=col, width=2)
    # top-right
    d.line([(W - pad, pad), (W - pad - L, pad)], fill=col, width=2)
    d.line([(W - pad, pad), (W - pad, pad + L)], fill=col, width=2)
    # bottom-left
    d.line([(pad, H - pad), (pad + L, H - pad)], fill=col, width=2)
    d.line([(pad, H - pad), (pad, H - pad - L)], fill=col, width=2)
    # bottom-right
    d.line([(W - pad, H - pad), (W - pad - L, H - pad)], fill=col, width=2)
    d.line([(W - pad, H - pad), (W - pad, H - pad - L)], fill=col, width=2)


def draw_text(layer: Image.Image):
    d = ImageDraw.Draw(layer, "RGBA")

    # top tagline (split into two lines for readability)
    tag1 = "프롬프트의 시대는 끝났다."
    tag2 = "이제 하네스를 설계하라."
    f_tag = ImageFont.truetype(F_MED, 50)

    def center_text(y, text, font, fill):
        bbox = d.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        d.text(((W - tw) / 2 - bbox[0], y), text, font=font, fill=fill)

    # small horizontal rule above tagline
    d.line([(W / 2 - 60, 220), (W / 2 + 60, 220)], fill=(CORAL[0], CORAL[1], CORAL[2], 220), width=2)

    center_text(260, tag1, f_tag, (CORAL[0], CORAL[1], CORAL[2], 235))
    center_text(330, tag2, f_tag, (CORAL[0], CORAL[1], CORAL[2], 235))

    # main title — large, bold, white
    f_title = ImageFont.truetype(F_BLACK, 196)
    title_line1 = "에이전틱"
    title_line2 = "코딩의 시대"
    center_text(520, title_line1, f_title, WHITE)
    center_text(520 + 230, title_line2, f_title, WHITE)

    # gold underline accent
    d.line([(W / 2 - 240, 1010), (W / 2 + 240, 1010)], fill=GOLD, width=4)

    # Korean subtitle
    f_sub = ImageFont.truetype(F_SEMI, 64)
    center_text(1060, "모델을 통제하는 하네스 엔지니어링", f_sub, SLATE)

    # English subtitle (two lines)
    f_eng = ImageFont.truetype(F_LIGHT, 38)
    center_text(1170, "THE AGE OF AGENTIC CODING", f_eng, (GOLD[0], GOLD[1], GOLD[2], 230))
    center_text(1218, "Engineering the Harness That Tames the Model", f_eng, (GOLD[0], GOLD[1], GOLD[2], 200))

    # author at bottom
    f_author_label = ImageFont.truetype(F_LIGHT, 32)
    f_author = ImageFont.truetype(F_BOLD, 64)
    center_text(H - 240, "AUTHOR", f_author_label, (SLATE[0], SLATE[1], SLATE[2], 180))
    center_text(H - 190, "Toby-AI", f_author, (GOLD[0], GOLD[1], GOLD[2], 240))

    # tiny series mark / publisher feel
    f_tiny = ImageFont.truetype(F_LIGHT, 26)
    center_text(H - 110, "HARNESS ENGINEERING SERIES — VOL. 01", f_tiny, (SLATE[0], SLATE[1], SLATE[2], 130))


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    # backup if exists
    if OUT.exists():
        backup = OUT.with_name("cover_v1.png")
        if not backup.exists():
            OUT.replace(backup)
            print(f"backed up existing cover to {backup}")
        else:
            # rotate v2, v3...
            i = 2
            while OUT.with_name(f"cover_v{i}.png").exists():
                i += 1
            OUT.replace(OUT.with_name(f"cover_v{i}.png"))

    # base gradient
    base = vertical_gradient((W, H), NAVY, NAVY_DEEP).convert("RGBA")

    # vignette
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vmask = radial_vignette((W, H), strength=0.7)
    vlayer = Image.new("RGBA", (W, H), (0, 0, 0, 200))
    vignette.paste(vlayer, (0, 0), vmask)
    base = Image.alpha_composite(base, vignette)

    # grid
    grid_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_grid(grid_layer)
    base = Image.alpha_composite(base, grid_layer)

    # curves
    curves_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_curves(curves_layer)
    base = Image.alpha_composite(base, curves_layer)

    # corner marks
    corner_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_corner_marks(corner_layer)
    base = Image.alpha_composite(base, corner_layer)

    # text
    text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_text(text_layer)
    base = Image.alpha_composite(base, text_layer)

    # final flatten + save
    final = base.convert("RGB")
    final.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}  ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
