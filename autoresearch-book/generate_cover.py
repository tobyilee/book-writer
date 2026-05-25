#!/usr/bin/env python3
"""
Cover generator for: autoresearch: 사람이 자는 동안 진화하는 코드
Concept: Loss Curve as Constellation — modernist, deep navy, amber accent.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# --- Config ----------------------------------------------------------------
W, H = 1600, 2560
OUT = Path(__file__).parent / "cover.png"

# Palette
BG_TOP = (10, 14, 31)        # #0A0E1F
BG_MID = (15, 21, 48)        # #0F1530
BG_BOT = (6, 9, 22)          # darker for bottom vignette
INK = (232, 234, 240)        # title white
MUTED = (139, 149, 181)      # subtitle muted
CYAN = (126, 200, 245)       # accent
AMBER = (244, 199, 123)      # loss curve / data points
AMBER_GLOW = (244, 199, 123, 60)

# Fonts (mac system)
FONTS = {
    "title": "/Users/tobylee/Library/Fonts/Pretendard-ExtraBold.otf",
    "title_alt": "/Users/tobylee/Library/Fonts/Pretendard-Bold.otf",
    "sub": "/Users/tobylee/Library/Fonts/Pretendard-Light.otf",
    "author": "/Users/tobylee/Library/Fonts/Pretendard-Medium.otf",
    "mono": "/Users/tobylee/Library/Fonts/JetBrainsMono-VariableFont_wght.ttf",
    "mono_b": "/Users/tobylee/Library/Fonts/JetBrainsMono-VariableFont_wght.ttf",
}


def load(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONTS[name], size)


# --- Build canvas ----------------------------------------------------------
random.seed(20260524)

img = Image.new("RGB", (W, H), BG_TOP)
px = img.load()

# Vertical gradient: BG_TOP -> BG_MID -> BG_BOT with subtle radial darkening at bottom
for y in range(H):
    if y < H * 0.45:
        t = y / (H * 0.45)
        r = int(BG_TOP[0] * (1 - t) + BG_MID[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_MID[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_MID[2] * t)
    else:
        t = (y - H * 0.45) / (H * 0.55)
        r = int(BG_MID[0] * (1 - t) + BG_BOT[0] * t)
        g = int(BG_MID[1] * (1 - t) + BG_BOT[1] * t)
        b = int(BG_MID[2] * (1 - t) + BG_BOT[2] * t)
    for x in range(W):
        px[x, y] = (r, g, b)

# Subtle noise / film grain
noise_layer = Image.new("RGB", (W, H))
npx = noise_layer.load()
for y in range(H):
    for x in range(W):
        n = random.randint(-4, 4)
        npx[x, y] = (max(0, min(255, n + 8)),) * 3
img = Image.blend(img, noise_layer, alpha=0.04)


# --- Star field ------------------------------------------------------------
star_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(star_layer)


def star(x: float, y: float, brightness: int, size: float, color=(255, 255, 255)):
    r = size
    # core
    sd.ellipse([x - r, y - r, x + r, y + r], fill=(*color, brightness))
    # halo for bright ones
    if brightness > 160:
        halo = int(r * 3.5)
        sd.ellipse(
            [x - halo, y - halo, x + halo, y + halo],
            fill=(*color, max(8, brightness // 12)),
        )


# Distribute ~340 stars; more dense in upper half (sky), thinner near typography zones
star_count = 360
for _ in range(star_count):
    x = random.random() * W
    # Bias toward upper 2/3
    y = (random.random() ** 1.3) * H * 0.92
    bright = random.randint(40, 230)
    size = random.choice([0.6, 0.8, 1.0, 1.0, 1.2, 1.5, 2.0])
    # rare warm star
    color = (255, 255, 255) if random.random() > 0.08 else (240, 220, 180)
    star(x, y, bright, size, color)

# A few extra crisp brighter stars
for _ in range(18):
    x = random.random() * W
    y = random.random() * H * 0.85
    star(x, y, random.randint(200, 255), random.uniform(2.2, 3.4))

img = Image.alpha_composite(img.convert("RGBA"), star_layer)


# --- Loss curve as constellation ------------------------------------------
curve_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(curve_layer)

# Loss curve: start upper-left of curve zone, decay to lower-right
# Curve zone roughly y from 0.55*H to 0.78*H, x from 0.08*W to 0.92*W
x0, y0 = int(0.08 * W), int(0.575 * H)
x1, y1 = int(0.92 * W), int(0.775 * H)

# Generate noisy exponential decay
n_points = 220
xs = []
ys = []
for i in range(n_points):
    t = i / (n_points - 1)
    # exponential decay in normalized space, with mild noise
    base = math.exp(-3.2 * t)
    noise = random.gauss(0, 0.04) * (1 - t * 0.6)
    val = max(0.02, base + noise)
    x = x0 + (x1 - x0) * t
    y = y1 - (y1 - y0) * val
    xs.append(x)
    ys.append(y)

# Draw faint curve line (amber with glow)
points = list(zip(xs, ys))

# Soft glow layer (wide, blurred)
glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow_layer)
for i in range(len(points) - 1):
    gd.line([points[i], points[i + 1]], fill=(*AMBER, 70), width=10)
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=14))

# Crisp curve
for i in range(len(points) - 1):
    cd.line([points[i], points[i + 1]], fill=(*AMBER, 165), width=2)

# Mark data points as stars
for i, (x, y) in enumerate(points):
    if i % 7 == 0:  # not all — keeps it elegant
        r = random.uniform(2.0, 3.5)
        cd.ellipse([x - r, y - r, x + r, y + r], fill=(*AMBER, 230))
        # halo
        hr = r * 3
        cd.ellipse([x - hr, y - hr, x + hr, y + hr], fill=(*AMBER, 22))

# A couple of brighter "epoch" markers — slightly bigger
epoch_idx = [int(n_points * f) for f in (0.05, 0.2, 0.45, 0.78)]
for ei in epoch_idx:
    x, y = points[ei]
    r = 5
    cd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 220, 160, 240))
    hr = r * 4
    cd.ellipse([x - hr, y - hr, x + hr, y + hr], fill=(*AMBER, 36))

img = Image.alpha_composite(img, glow_layer)
img = Image.alpha_composite(img, curve_layer)


# --- Typography ------------------------------------------------------------
draw = ImageDraw.Draw(img)

# Top: small monospace mark
mono_small = load("mono", 28)
draw.text(
    (int(W * 0.08), int(H * 0.075)),
    "// midnight loop · v1.0.0",
    font=mono_small,
    fill=MUTED,
)

# Mono code title "autoresearch" near top
mono_title = load("mono_b", 92)
mono_text = "autoresearch"
tw = draw.textlength(mono_text, font=mono_title)
mtx = int(W * 0.08)
mty = int(H * 0.12)
draw.text((mtx, mty), mono_text, font=mono_title, fill=INK)

# Cyan accent underline for autoresearch
underline_y = mty + 110
draw.line(
    [(mtx, underline_y), (mtx + int(tw * 0.18), underline_y)],
    fill=CYAN,
    width=4,
)

# Two thin separator lines (modernist)
sep_y = int(H * 0.30)
draw.line(
    [(int(W * 0.08), sep_y), (int(W * 0.92), sep_y)],
    fill=(60, 75, 110, 255),
    width=1,
)

# Main Korean title — two lines, big, centered-left
title_font = load("title", 168)
line1 = "사람이 자는 동안"
line2 = "진화하는 코드"
title_x = int(W * 0.08)
title_y1 = int(H * 0.34)

# Get heights
_, t1_h = title_font.getbbox(line1)[2:]
draw.text((title_x, title_y1), line1, font=title_font, fill=INK)
draw.text(
    (title_x, title_y1 + int(t1_h * 1.05)),
    line2,
    font=title_font,
    fill=INK,
)

# Subtitle — smaller, muted
sub_font = load("sub", 44)
sub_y = title_y1 + int(t1_h * 1.05) + 220
draw.text(
    (title_x, sub_y),
    "Karpathy의 자율 연구 루프를",
    font=sub_font,
    fill=MUTED,
)
draw.text(
    (title_x, sub_y + 64),
    "Claude Code 환경으로",
    font=sub_font,
    fill=MUTED,
)

# Bottom block: thin top divider, then "loss" axis label, author, version
bottom_divider_y = int(H * 0.88)
draw.line(
    [(int(W * 0.08), bottom_divider_y), (int(W * 0.92), bottom_divider_y)],
    fill=(60, 75, 110, 255),
    width=1,
)

# Loss axis label tucked under the curve (left of curve start)
mono_tiny = load("mono", 24)
draw.text(
    (int(W * 0.08), int(H * 0.79) + 24),
    "loss ↓   epochs →",
    font=mono_tiny,
    fill=(126, 200, 245, 200),
)

# Author bottom-left
author_font = load("author", 56)
draw.text(
    (int(W * 0.08), bottom_divider_y + 36),
    "Toby-AI",
    font=author_font,
    fill=INK,
)

# Meta line bottom-right (mono)
meta_font = load("mono", 28)
meta_text = "v1.0.0 · 2026"
mw = draw.textlength(meta_text, font=meta_font)
draw.text(
    (int(W * 0.92) - mw, bottom_divider_y + 56),
    meta_text,
    font=meta_font,
    fill=MUTED,
)

# Tiny CC notice (bottom-right, very small)
cc_font = load("mono", 22)
cc_text = "CC BY-NC-SA 4.0"
cw = draw.textlength(cc_text, font=cc_font)
draw.text(
    (int(W * 0.92) - cw, bottom_divider_y + 100),
    cc_text,
    font=cc_font,
    fill=(96, 110, 140),
)


# --- Final touches: vignette ------------------------------------------------
vignette = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vignette)
for i in range(60):
    a = int(60 * (i / 60))
    vd.rectangle([i, i, W - i, H - i], outline=a)
vignette = vignette.filter(ImageFilter.GaussianBlur(radius=80))
black = Image.new("RGB", (W, H), (0, 0, 0))
img_rgb = img.convert("RGB")
img_rgb = Image.composite(black, img_rgb, vignette.point(lambda v: int(v * 0.35)))

img_rgb.save(OUT, "PNG", optimize=True)
print(f"Wrote: {OUT} ({W}x{H})")
