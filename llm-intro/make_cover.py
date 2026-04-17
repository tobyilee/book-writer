#!/usr/bin/env python3
"""
Cover generator for "LLM 내부로 들어가기".

Concept (chosen): A — minimalist geometric illustration.
- Dark navy base (#1a2332)
- Warm off-white accent (#f5e6c8) for lines + titles
- Center motif: an opening box with a few token-dots ascending from it
- Title: Korean serif (AppleMyungjo), bold horizontal layout
- Subtitle: sans-serif (Noto Sans KR)
- Author bottom-right: Toby-AI in small serif italics
"""

from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 1600, 2560
BG      = (26, 35, 50)        # #1a2332
BG2     = (45, 62, 80)        # subtle gradient end #2d3e50
INK     = (245, 230, 200)     # #f5e6c8 warm off-white
INK_DIM = (200, 184, 150)     # dimmer accent
INK_FAINT = (110, 120, 135)   # faint contour

OUT = "/Users/tobylee/workspace/ai/book-writer/_workspace/llm-intro/cover.png"

FONT_SERIF_PATH = "/System/Library/Fonts/Supplemental/AppleMyungjo.ttf"
FONT_SANS_PATH  = "/Users/tobylee/Library/Fonts/NotoSansKR-VariableFont_wght.ttf"
FONT_LATIN_PATH = "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"
if not os.path.exists(FONT_LATIN_PATH):
    FONT_LATIN_PATH = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
if not os.path.exists(FONT_LATIN_PATH):
    FONT_LATIN_PATH = FONT_SERIF_PATH


def vertical_gradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h), top)
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        # slight non-linear — keep upper area calmer
        t = t ** 1.15
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


def draw_opening_box(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int):
    """Minimal geometric 'opening box' — a half-open lid in line art."""
    s = size
    # Box base (front face) — slightly perspective
    #    top-left, top-right, bot-right, bot-left
    base = [
        (cx - s, cy - s // 4),
        (cx + s, cy - s // 4),
        (cx + s, cy + s // 2),
        (cx - s, cy + s // 2),
    ]
    draw.polygon(base, outline=INK, width=6)

    # Back edge (side panel hint — a trapezoid going "in")
    depth = int(s * 0.25)
    back = [
        (cx - s + depth, cy - s // 4 - depth),
        (cx + s - depth, cy - s // 4 - depth),
        (cx + s, cy - s // 4),
        (cx - s, cy - s // 4),
    ]
    draw.polygon(back, outline=INK, width=4)

    # Lid — opened upward, tilted backward
    lid_front_y = cy - s // 4 - depth
    lid_back_y  = cy - s - int(s * 0.2)
    lid_left_x_front  = cx - s + depth
    lid_right_x_front = cx + s - depth
    lid_left_x_back   = cx - s + int(depth * 1.8)
    lid_right_x_back  = cx + s - int(depth * 1.8)
    lid = [
        (lid_left_x_front, lid_front_y),
        (lid_right_x_front, lid_front_y),
        (lid_right_x_back, lid_back_y),
        (lid_left_x_back,  lid_back_y),
    ]
    draw.polygon(lid, outline=INK, width=5)

    # Tokens/dots ascending from the opened box (representing tokens emerging)
    tokens = [
        (cx - int(s * 0.45), cy - s - int(s * 0.55), 12),
        (cx - int(s * 0.15), cy - s - int(s * 0.85), 16),
        (cx + int(s * 0.10), cy - s - int(s * 1.20), 10),
        (cx + int(s * 0.35), cy - s - int(s * 0.70), 14),
        (cx - int(s * 0.05), cy - s - int(s * 0.35), 8),
        (cx + int(s * 0.50), cy - s - int(s * 1.05), 9),
    ]
    for (tx, ty, r) in tokens:
        # hollow dot — matches line-art style
        draw.ellipse((tx - r, ty - r, tx + r, ty + r), outline=INK, width=3)

    # Faint connecting dotted trajectory — suggests "path emerging"
    traj_pts = [
        (cx - int(s * 0.3), cy - s // 4 - depth - 10),
        (cx - int(s * 0.15), cy - s - int(s * 0.60)),
        (cx + int(s * 0.05), cy - s - int(s * 0.95)),
        (cx + int(s * 0.25), cy - s - int(s * 0.75)),
    ]
    for i, (px_, py_) in enumerate(traj_pts):
        draw.ellipse((px_ - 3, py_ - 3, px_ + 3, py_ + 3),
                     fill=INK_DIM)


def draw_decorative_rule(draw, x1, y, x2, color=INK_DIM, width=2):
    draw.line([(x1, y), (x2, y)], fill=color, width=width)


def text_w(draw, text, font):
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    return r - l, b - t


def main():
    img = vertical_gradient(W, H, BG, BG2)
    draw = ImageDraw.Draw(img, "RGBA")

    # --- Subtle top/bottom inner frame (barely perceptible) ---
    margin = 80
    draw.rectangle([(margin, margin), (W - margin, H - margin)],
                   outline=(255, 255, 255, 28), width=2)

    # --- Top small tag ---
    tag_font = ImageFont.truetype(FONT_SANS_PATH, 34)
    tag = "BACKEND DEVELOPER SERIES"
    tw, th = text_w(draw, tag, tag_font)
    draw.text(((W - tw) // 2, 200), tag, font=tag_font,
              fill=INK_DIM)
    # tiny rules left/right of the tag
    rule_y = 200 + th // 2
    rule_len = 180
    draw_decorative_rule(draw, (W - tw) // 2 - rule_len - 40, rule_y,
                         (W - tw) // 2 - 40)
    draw_decorative_rule(draw, (W + tw) // 2 + 40, rule_y,
                         (W + tw) // 2 + rule_len + 40)

    # --- Title (top-third region) ---
    title = "LLM 內部로"
    title2 = "들어가기"
    # AppleMyungjo renders '내부' as 내부 — we'll keep hangul. Use 내부.
    title  = "LLM 내부로"
    title2 = "들어가기"
    title_font = ImageFont.truetype(FONT_SERIF_PATH, 200)
    t1w, t1h = text_w(draw, title, title_font)
    t2w, t2h = text_w(draw, title2, title_font)

    title_y = 380
    draw.text(((W - t1w) // 2, title_y), title, font=title_font, fill=INK)
    draw.text(((W - t2w) // 2, title_y + t1h + 30), title2,
              font=title_font, fill=INK)

    # Thin accent rule under title
    rule_top_y = title_y + t1h + 30 + t2h + 70
    draw.line([(W // 2 - 160, rule_top_y),
               (W // 2 + 160, rule_top_y)],
              fill=INK, width=3)

    # --- Subtitle ---
    sub_font = ImageFont.truetype(FONT_SANS_PATH, 62)
    subtitle = "백엔드 개발자를 위한 한 걸음씩 입문"
    sw, sh = text_w(draw, subtitle, sub_font)
    draw.text(((W - sw) // 2, rule_top_y + 45), subtitle,
              font=sub_font, fill=INK_DIM)

    # --- Central illustration ---
    illo_cx = W // 2
    illo_cy = 1780
    draw_opening_box(draw, illo_cx, illo_cy, 280)

    # --- Small caption under illustration ---
    cap_font = ImageFont.truetype(FONT_SANS_PATH, 36)
    caption = "· a gentle path into the black box ·"
    cw, ch = text_w(draw, caption, cap_font)
    draw.text(((W - cw) // 2, 2150), caption, font=cap_font,
              fill=INK_FAINT)

    # --- Author attribution bottom-right ---
    author_font = ImageFont.truetype(FONT_LATIN_PATH, 52)
    author = "Toby-AI"
    aw, ah = text_w(draw, author, author_font)
    draw.text((W - margin - aw - 20, H - margin - ah - 20),
              author, font=author_font, fill=INK)

    # --- Small year / imprint bottom-left ---
    year_font = ImageFont.truetype(FONT_SANS_PATH, 36)
    year = "2026"
    draw.text((margin + 20, H - margin - 60), year,
              font=year_font, fill=INK_DIM)

    img.save(OUT, "PNG", optimize=True)
    print(f"Saved {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
