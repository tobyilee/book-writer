"""
Cover generator for "JVM 출신을 위한 Rust"

Design concept:
  Slash-divided typography (모티프 4 base) plus subtle interlocking
  cog marks at the slash endpoints (모티프 1 echo). The oversized rust
  slash acts as a polyglot bridge between two engineering traditions.

Palette:
  Rust signature orange (#CE422B) on deep charcoal (#181620),
  gold accent (#D4A437), JVM forest green only on the word "Spring".
"""

from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
import os
import math
import random

OUT = "/Users/tobylee/workspace/ai/book-writer/rust-for-jvm-developers/cover.png"
W, H = 1600, 2560

# ---- Palette
BG_TOP    = (24, 22, 28)
BG_BOTTOM = (12, 10, 14)
RUST      = (206, 66, 43)
GOLD      = (212, 164, 55)
JVM_GREEN = (90, 138, 90)
PAPER     = (232, 226, 214)
SUB_GREY  = (170, 162, 152)
HAIR      = (74, 66, 60)

# ---- Fonts
P_BLACK = "/Users/tobylee/Library/Fonts/Pretendard-Black.otf"
P_BOLD  = "/Users/tobylee/Library/Fonts/Pretendard-Bold.otf"
P_EBOLD = "/Users/tobylee/Library/Fonts/Pretendard-ExtraBold.otf"
P_REG   = "/Users/tobylee/Library/Fonts/Pretendard-Regular.otf"
P_MED   = "/Users/tobylee/Library/Fonts/Pretendard-Medium.otf"
P_LIGHT = "/Users/tobylee/Library/Fonts/Pretendard-Light.otf"

def load(path, size):
    return ImageFont.truetype(path, size)

# ---- Base canvas with vertical gradient
img = Image.new("RGB", (W, H), BG_BOTTOM)
base_draw = ImageDraw.Draw(img)
for y in range(H):
    t = y / H
    e = t * t * (3 - 2 * t)
    r = int(BG_TOP[0] * (1 - e) + BG_BOTTOM[0] * e)
    g = int(BG_TOP[1] * (1 - e) + BG_BOTTOM[1] * e)
    b = int(BG_TOP[2] * (1 - e) + BG_BOTTOM[2] * e)
    base_draw.line([(0, y), (W, y)], fill=(r, g, b))

# ---- Warm rust glow upper-right (suggests sunrise / new direction)
glow = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow)
cx, cy = int(W * 0.78), int(H * 0.18)
for radius, alpha in [(900, 22), (650, 30), (420, 40), (260, 52)]:
    color = (
        int(RUST[0] * alpha / 255),
        int(RUST[1] * alpha / 255),
        int(RUST[2] * alpha / 255),
    )
    gd.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color)
glow = glow.filter(ImageFilter.GaussianBlur(160))
img = ImageChops.add(img, glow)

# Optional: tiny cool indigo glow lower-left for compositional balance
cool = Image.new("RGB", (W, H), (0, 0, 0))
cd = ImageDraw.Draw(cool)
ccx, ccy = int(W * 0.18), int(H * 0.88)
for radius, alpha in [(700, 14), (450, 20), (260, 28)]:
    color = (int(60 * alpha / 255), int(58 * alpha / 255), int(96 * alpha / 255))
    cd.ellipse((ccx - radius, ccy - radius, ccx + radius, ccy + radius), fill=color)
cool = cool.filter(ImageFilter.GaussianBlur(150))
img = ImageChops.add(img, cool)

draw = ImageDraw.Draw(img, "RGBA")

# ---- Top thin gold rule + tagline
draw.line([(180, 240), (W - 180, 240)], fill=GOLD + (180,), width=3)

tag_font = load(P_MED, 38)
draw.text((180, 178), "POLYGLOT  BACKEND  SERIES  ·  Vol. 02",
          font=tag_font, fill=SUB_GREY)

mono_font = load(P_BOLD, 38)
mark = "T · AI"
mw = draw.textlength(mark, font=mono_font)
draw.text((W - 180 - mw, 178), mark, font=mono_font, fill=GOLD)

# ---- Central slash (polyglot bridge)
slash_top    = (int(W * 0.62), int(H * 0.32))
slash_bottom = (int(W * 0.38), int(H * 0.66))
slash_thickness = 46

# Soft glow under slash
glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gl = ImageDraw.Draw(glow_layer)
gl.line([slash_top, slash_bottom], fill=RUST + (110,), width=slash_thickness + 70)
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(48))
img = Image.alpha_composite(img.convert("RGBA"), glow_layer).convert("RGB")
draw = ImageDraw.Draw(img, "RGBA")

# Main slash with rounded caps
def thick_line(target_draw, p1, p2, color, thickness, alpha=255):
    target_draw.line([p1, p2], fill=color + (alpha,), width=thickness)
    r = thickness // 2
    target_draw.ellipse((p1[0]-r, p1[1]-r, p1[0]+r, p1[1]+r), fill=color + (alpha,))
    target_draw.ellipse((p2[0]-r, p2[1]-r, p2[0]+r, p2[1]+r), fill=color + (alpha,))

thick_line(draw, slash_top, slash_bottom, RUST, slash_thickness)

# Gold edge highlight along one side of the slash
dx = slash_bottom[0] - slash_top[0]
dy = slash_bottom[1] - slash_top[1]
length = math.hypot(dx, dy)
nx, ny = -dy / length, dx / length
offset = slash_thickness // 2 - 4
hp1 = (slash_top[0] + nx * offset, slash_top[1] + ny * offset)
hp2 = (slash_bottom[0] + nx * offset, slash_bottom[1] + ny * offset)
draw.line([hp1, hp2], fill=GOLD + (215,), width=4)

# ---- Two interlocking cogs at slash ends (모티프 1 echo)
def cog(center, radius, teeth, color, tooth_h=20, rot_deg=0, alpha=220):
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse(
        (center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius),
        outline=color + (alpha,), width=4,
    )
    inr = radius // 3
    d.ellipse(
        (center[0]-inr, center[1]-inr, center[0]+inr, center[1]+inr),
        outline=color + (int(alpha * 0.8),), width=3,
    )
    for i in range(teeth):
        a = math.radians(rot_deg + i * (360 / teeth))
        x1 = center[0] + math.cos(a) * radius
        y1 = center[1] + math.sin(a) * radius
        x2 = center[0] + math.cos(a) * (radius + tooth_h)
        y2 = center[1] + math.sin(a) * (radius + tooth_h)
        d.line([(x1, y1), (x2, y2)], fill=color + (alpha,), width=5)

# Top-right cog locks into slash top end (Rust side)
cog((slash_top[0] + 78, slash_top[1] - 30), 78, 14, RUST,      tooth_h=22, rot_deg=0)
# Bottom-left cog locks into slash bottom end (JVM side), slightly rotated
cog((slash_bottom[0] - 78, slash_bottom[1] + 30), 78, 14, JVM_GREEN, tooth_h=22, rot_deg=12)

draw = ImageDraw.Draw(img, "RGBA")

# ---- Title block (left-aligned)
title_big   = load(P_BLACK, 188)
title_huge  = load(P_BLACK, 320)

draw.text((180, 380), "JVM 출신을 위한", font=title_big, fill=PAPER)
draw.text((180, 600), "Rust",            font=title_huge, fill=RUST)

rl = draw.textlength("Rust", font=title_huge)
draw.line([(180, 940), (180 + rl, 940)], fill=GOLD + (200,), width=6)

# ---- Subtitle (Spring in JVM green, rest in paper)
sub_font = load(P_MED, 78)
sub_y = int(H * 0.74)
sub_x = 180
parts = [("Spring", JVM_GREEN), (" 다음에 읽는 책", PAPER)]
cursor = sub_x
for text, color in parts:
    draw.text((cursor, sub_y), text, font=sub_font, fill=color)
    cursor += draw.textlength(text, font=sub_font)

desc_font = load(P_LIGHT, 40)
draw.text((sub_x, sub_y + 110), "대체가 아니라, 무기 추가.",
          font=desc_font, fill=SUB_GREY)

# ---- Bottom block
draw.line([(180, H - 280), (W - 180, H - 280)], fill=HAIR + (255,), width=2)

author_label_font = load(P_REG, 36)
author_font       = load(P_EBOLD, 64)
draw.text((180, H - 240), "지은이",  font=author_label_font, fill=SUB_GREY)
draw.text((180, H - 200), "Toby-AI", font=author_font,       fill=PAPER)

right_x = W - 180
def right_text(text, y, font, color):
    w = draw.textlength(text, font=font)
    draw.text((right_x - w, y), text, font=font, fill=color)

right_text("Java  ·  Kotlin  ·  Rust", H - 240, author_label_font, SUB_GREY)
right_text("폴리글랏 백엔드 입문",        H - 195, load(P_MED, 44),    GOLD)

# ---- Subtle film grain for warmth
random.seed(7)
grain = Image.new("L", (W // 4, H // 4))
gpx = grain.load()
for y in range(H // 4):
    for x in range(W // 4):
        gpx[x, y] = 128 + random.randint(-12, 12)
grain = grain.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.6))
grain_rgb = Image.merge("RGB", (grain, grain, grain))
img = Image.blend(img, grain_rgb, 0.04)

# ---- Subtle inner frame
ImageDraw.Draw(img, "RGBA").rectangle(
    (30, 30, W - 30, H - 30), outline=(255, 255, 255, 18), width=2
)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(f"Saved: {OUT}  size={img.size}")
