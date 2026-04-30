#!/usr/bin/env python3
"""표지 생성 — 브리즈번의 부엌에서, 프렌치를 시작하자."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path("/Users/tobylee/workspace/ai/book-writer/french-cooking-guide/cover.png")
W, H = 1600, 2560

BG_TOP = (240, 226, 200)
BG_BOT = (212, 178, 140)
TITLE_COLOR = (62, 39, 24)
SUBTITLE_COLOR = (110, 75, 50)
ACCENT = (170, 60, 35)
AUTHOR_COLOR = (62, 39, 24)

KOR_BOLD = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
KOR_REG = "/System/Library/Fonts/AppleSDGothicNeo.ttc"

img = Image.new("RGB", (W, H), BG_TOP)
draw = ImageDraw.Draw(img)

for y in range(H):
    t = y / H
    r = int(BG_TOP[0] * (1 - t) + BG_BOT[0] * t)
    g = int(BG_TOP[1] * (1 - t) + BG_BOT[1] * t)
    b = int(BG_TOP[2] * (1 - t) + BG_BOT[2] * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

import math
cx, cy, rx, ry = 380, 720, 110, 90
for ring in range(6):
    rr = rx - ring * 14
    rr2 = ry - ring * 12
    if rr <= 0 or rr2 <= 0:
        break
    draw.ellipse([cx - rr, cy - rr2, cx + rr, cy + rr2], outline=(150, 95, 60, 200), width=2)

cx2, cy2 = 1230, 720
for ring in range(5):
    rr = 90 - ring * 14
    rr2 = 80 - ring * 12
    if rr <= 0 or rr2 <= 0:
        break
    draw.ellipse([cx2 - rr, cy2 - rr2, cx2 + rr, cy2 + rr2], outline=(150, 95, 60, 200), width=2)

draw.line([(180, 880), (1420, 880)], fill=(150, 95, 60), width=3)
draw.line([(180, 1980), (1420, 1980)], fill=(150, 95, 60), width=3)

try:
    font_title = ImageFont.truetype(KOR_BOLD, 130, index=2)
except Exception:
    font_title = ImageFont.truetype(KOR_BOLD, 130)
try:
    font_sub = ImageFont.truetype(KOR_REG, 60, index=0)
except Exception:
    font_sub = ImageFont.truetype(KOR_REG, 60)
try:
    font_accent = ImageFont.truetype(KOR_REG, 50, index=0)
except Exception:
    font_accent = ImageFont.truetype(KOR_REG, 50)
try:
    font_author = ImageFont.truetype(KOR_REG, 56, index=2)
except Exception:
    font_author = ImageFont.truetype(KOR_REG, 56)

title_line1 = "브리즈번의 부엌에서,"
title_line2 = "프렌치를 시작하자"

bbox = draw.textbbox((0, 0), title_line1, font=font_title)
w1 = bbox[2] - bbox[0]
draw.text(((W - w1) / 2, 1000), title_line1, fill=TITLE_COLOR, font=font_title)

bbox = draw.textbbox((0, 0), title_line2, font=font_title)
w2 = bbox[2] - bbox[0]
draw.text(((W - w2) / 2, 1180), title_line2, fill=TITLE_COLOR, font=font_title)

draw.line([(W / 2 - 80, 1380), (W / 2 + 80, 1380)], fill=ACCENT, width=4)

subtitle = "한식이 익숙한 우리를 위한"
bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
ws = bbox[2] - bbox[0]
draw.text(((W - ws) / 2, 1430), subtitle, fill=SUBTITLE_COLOR, font=font_sub)

subtitle2 = "프랑스 가정식 입문"
bbox = draw.textbbox((0, 0), subtitle2, font=font_sub)
ws2 = bbox[2] - bbox[0]
draw.text(((W - ws2) / 2, 1520), subtitle2, fill=SUBTITLE_COLOR, font=font_sub)

accent_text = "Brisbane · Korean Home Cook · French Bistro"
bbox = draw.textbbox((0, 0), accent_text, font=font_accent)
wa = bbox[2] - bbox[0]
draw.text(((W - wa) / 2, 1720), accent_text, fill=ACCENT, font=font_accent)

author = "Toby-AI"
bbox = draw.textbbox((0, 0), author, font=font_author)
waut = bbox[2] - bbox[0]
draw.text(((W - waut) / 2, 2280), author, fill=AUTHOR_COLOR, font=font_author)

img.save(OUT, "PNG", optimize=True)
print(f"Cover saved: {OUT}")
print(f"Size: {img.size}")
