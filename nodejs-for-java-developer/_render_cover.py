"""Render the EPUB cover for 자바 개발자를 위한 Node.js using PIL.

Concept: dark navy minimalist senior-technical-book cover with two abstract
motifs (Spring coil on the left, Node event loop on the right) separated from
the title block by a thin mustard gold line.

Output: 1600 x 2560 PNG.
"""

from __future__ import annotations

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Layout & palette
# ---------------------------------------------------------------------------

W, H = 1600, 2560

NAVY_TOP = (15, 22, 38)        # #0F1626
NAVY_BOTTOM = (26, 33, 56)     # #1A2138
SPRING_GREEN = (109, 179, 63)  # #6DB33F
NODE_GREEN = (95, 160, 78)     # #5FA04E
WARM_WHITE = (245, 242, 232)   # #F5F2E8
MUTED_GRAY = (168, 178, 199)   # #A8B2C7
MUSTARD = (201, 166, 107)      # #C9A66B
DIM_GREEN_SPRING = (109, 179, 63, 90)
DIM_GREEN_NODE = (95, 160, 78, 90)


# ---------------------------------------------------------------------------
# Font loading
# ---------------------------------------------------------------------------

HOME = Path.home()
PRETENDARD_VAR = HOME / "Library/Fonts/PretendardVariable.ttf"
PRETENDARD_BOLD = HOME / "Library/Fonts/Pretendard-Bold.otf"
APPLE_SD = Path("/System/Library/Fonts/AppleSDGothicNeo.ttc")
JETBRAINS = HOME / "Library/Fonts/JetBrainsMono-VariableFont_wght.ttf"


def load_font(size: int, weight: str = "bold") -> ImageFont.FreeTypeFont:
    """Pick the best available Korean-capable font.

    Pretendard preferred; fall back to Apple SD Gothic Neo, then default.
    """
    candidates = []
    if weight == "bold" and PRETENDARD_BOLD.exists():
        candidates.append(PRETENDARD_BOLD)
    if PRETENDARD_VAR.exists():
        candidates.append(PRETENDARD_VAR)
    if APPLE_SD.exists():
        candidates.append(APPLE_SD)

    for path in candidates:
        try:
            return ImageFont.truetype(str(path), size)
        except OSError:
            continue
    return ImageFont.load_default()


def load_mono(size: int) -> ImageFont.FreeTypeFont:
    if JETBRAINS.exists():
        try:
            return ImageFont.truetype(str(JETBRAINS), size)
        except OSError:
            pass
    return load_font(size, "bold")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def vertical_gradient(size: tuple[int, int], top: tuple[int, int, int], bot: tuple[int, int, int]) -> Image.Image:
    """Generate a vertical RGB gradient image."""
    w, h = size
    img = Image.new("RGB", size, top)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        # Ease-in for darker upper half, lighter lower edge
        r = int(top[0] * (1 - t) + bot[0] * t)
        g = int(top[1] * (1 - t) + bot[1] * t)
        b = int(top[2] * (1 - t) + bot[2] * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


def text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered(draw: ImageDraw.ImageDraw, text: str, y: int, font, fill, *, anchor_offset_x: int = 0, letter_spacing: float = 0.0) -> int:
    """Draw text centered at canvas width=W; return baseline-bottom y."""
    if letter_spacing == 0.0:
        w, h = text_size(draw, text, font)
        x = (W - w) // 2 + anchor_offset_x
        draw.text((x, y), text, font=font, fill=fill)
        return y + h

    # Manual letter spacing
    widths = [text_size(draw, ch, font)[0] for ch in text]
    total = sum(widths) + int(letter_spacing * (len(text) - 1))
    x = (W - total) // 2 + anchor_offset_x
    h = 0
    for ch, w in zip(text, widths):
        cw, ch_h = text_size(draw, ch, font)
        h = max(h, ch_h)
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + int(letter_spacing)
    return y + h


# ---------------------------------------------------------------------------
# Motif: Spring coil (left)
# ---------------------------------------------------------------------------

def draw_spring_coil(canvas: Image.Image) -> None:
    """Draw an abstract coil spring as 4 stacked tilted ellipses."""
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    cx = 470
    cy_start = 380
    spacing = 60
    coil_count = 6
    ellipse_w = 240
    ellipse_h = 90
    stroke = 3

    for i in range(coil_count):
        cy = cy_start + i * spacing
        # Slight horizontal drift to suggest perspective tilt
        dx = int(8 * (i - coil_count / 2))
        bbox = (cx - ellipse_w // 2 + dx, cy - ellipse_h // 2,
                cx + ellipse_w // 2 + dx, cy + ellipse_h // 2)
        # Top half slightly transparent to suggest coil hidden behind next loop
        alpha = 230 if i % 2 == 0 else 180
        od.ellipse(bbox, outline=(*SPRING_GREEN, alpha), width=stroke)

    # Vertical guideline at the spring's axis (very faint)
    od.line([(cx, cy_start - 20), (cx, cy_start + spacing * (coil_count - 1) + 20)],
            fill=(*SPRING_GREEN, 50), width=1)

    # Tiny label "JVM" in mono near the coil
    label_font = load_mono(22)
    label = "JVM · Spring"
    lw, lh = text_size(od, label, label_font)
    od.text((cx - lw // 2, cy_start + spacing * coil_count + 20),
            label, font=label_font, fill=(*MUTED_GRAY, 200))

    canvas.alpha_composite(overlay)


# ---------------------------------------------------------------------------
# Motif: Event loop (right)
# ---------------------------------------------------------------------------

def draw_event_loop(canvas: Image.Image) -> None:
    """Draw an abstract event loop as a dashed circle with a single highlighted node."""
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    cx, cy = 1130, 560
    radius = 170
    stroke = 3

    # Dashed circle made of short arcs
    dash_count = 24
    arc_deg = 360 / dash_count
    gap = arc_deg * 0.35
    for i in range(dash_count):
        start = i * arc_deg + gap / 2
        end = start + arc_deg - gap
        bbox = (cx - radius, cy - radius, cx + radius, cy + radius)
        od.arc(bbox, start=start, end=end,
               fill=(*NODE_GREEN, 230), width=stroke)

    # Node marker at the top of the loop
    node_angle = -90  # top
    nx = cx + int(radius * math.cos(math.radians(node_angle)))
    ny = cy + int(radius * math.sin(math.radians(node_angle)))
    node_r = 14
    od.ellipse((nx - node_r, ny - node_r, nx + node_r, ny + node_r),
               fill=(*NODE_GREEN, 255))
    # Soft glow ring
    od.ellipse((nx - node_r - 8, ny - node_r - 8, nx + node_r + 8, ny + node_r + 8),
               outline=(*NODE_GREEN, 100), width=2)

    # Inner dot for "callback" suggestion
    od.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=(*MUTED_GRAY, 160))

    # Tiny label "V8 · Node.js"
    label_font = load_mono(22)
    label = "V8 · Node.js"
    lw, lh = text_size(od, label, label_font)
    od.text((cx - lw // 2, cy + radius + 30),
            label, font=label_font, fill=(*MUTED_GRAY, 200))

    canvas.alpha_composite(overlay)


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render() -> Path:
    out_path = Path(__file__).parent / "cover.png"

    bg = vertical_gradient((W, H), NAVY_TOP, NAVY_BOTTOM).convert("RGBA")

    # Subtle grain dots in the background to break up flatness
    grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grain)
    import random
    random.seed(42)
    for _ in range(280):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        a = random.randint(8, 22)
        gd.point((x, y), fill=(255, 255, 255, a))
    bg.alpha_composite(grain)

    draw_spring_coil(bg)
    draw_event_loop(bg)

    # Overlay layer for text + meeting line
    layer = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # Mustard horizontal "meeting" line — the place where two runtimes meet
    line_y = 880
    line_x_start = 380
    line_x_end = W - 380
    d.line([(line_x_start, line_y), (line_x_end, line_y)],
           fill=(*MUSTARD, 220), width=2)
    # Tiny center notch
    d.line([(W // 2 - 25, line_y - 6), (W // 2 + 25, line_y - 6)],
           fill=(*MUSTARD, 180), width=1)

    # Eyebrow / kicker above the title
    kicker_font = load_mono(28)
    kicker = "BACKEND  ·  TWO  RUNTIMES"
    kw, kh = text_size(d, kicker, kicker_font)
    d.text(((W - kw) // 2, line_y + 40), kicker,
           font=kicker_font, fill=(*MUSTARD, 230))

    # Main title — two-line block in Korean
    title_top_font = load_font(96, "bold")
    title_bottom_font = load_font(160, "bold")

    y = line_y + 130
    y = draw_centered(d, "자바 개발자를 위한", y, title_top_font, WARM_WHITE)
    y += 30
    y = draw_centered(d, "Node.js", y, title_bottom_font, WARM_WHITE)

    # Subtitle (two lines)
    sub_font = load_font(46, "bold")
    y += 70
    y = draw_centered(d, "Spring 직관을 그대로 들고 가는", y, sub_font, MUTED_GRAY)
    y += 18
    y = draw_centered(d, "두 번째 런타임 가이드", y, sub_font, MUTED_GRAY)

    # Slogan band — quote in mustard gold, near lower-third
    slogan_font = load_font(34, "bold")
    slogan_y = 2050
    quote_open = "“"
    quote_close = "”"
    line1 = f"{quote_open}도구만 바뀌었을 뿐,"
    line2 = f"우리는 여전히 백엔드 개발자다.{quote_close}"
    draw_centered(d, line1, slogan_y, slogan_font, MUSTARD)
    draw_centered(d, line2, slogan_y + 60, slogan_font, MUSTARD)

    # Author at the bottom
    author_font = load_font(40, "bold")
    author_y = 2400
    # Thin separator above the author
    d.line([(W // 2 - 60, author_y - 30), (W // 2 + 60, author_y - 30)],
           fill=(*MUTED_GRAY, 160), width=1)
    draw_centered(d, "Toby-AI", author_y, author_font, WARM_WHITE)

    # Compose & save
    final = Image.alpha_composite(bg, layer).convert("RGB")
    final.save(out_path, "PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    p = render()
    print(f"Cover written to {p}")
    print(f"Size: {p.stat().st_size} bytes")
