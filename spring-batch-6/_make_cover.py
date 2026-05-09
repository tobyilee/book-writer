"""Generate cover.png for 직접 짜본 사람을 위한 Spring Batch 6.

Concept: dark navy background with a chunk-processing pipeline motif
(read -> process -> write data blocks flowing through the page) +
bold Korean title in white, sub-title in Spring green, author at the
bottom, and code-like decorative elements to convey "hands-on" tone.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# --- canvas ---------------------------------------------------------------
W, H = 1600, 2400  # 2:3 ratio, EPUB-friendly
OUT = os.path.join(os.path.dirname(__file__), "cover.png")

# --- palette --------------------------------------------------------------
BG_TOP = (12, 20, 38)
BG_BOT = (28, 38, 56)
SPRING = (109, 179, 63)        # #6DB33F
SPRING_DIM = (76, 125, 44)
ACCENT = (148, 226, 115)
WHITE = (245, 245, 245)
GRAY = (170, 180, 190)
DIM = (95, 110, 130)
CHUNK_BG = (32, 50, 72)
CHUNK_BG_HI = (40, 75, 55)
CHUNK_BORDER = (75, 105, 130)

# --- fonts ----------------------------------------------------------------
KO_FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
EN_FONT = "/System/Library/Fonts/Helvetica.ttc"


def kfont(size: int, idx: int = 8) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(KO_FONT, size, index=idx)


def efont(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    # Helvetica.ttc index 0 Regular, 1 Bold ish (varies); we'll try 1 for bold
    return ImageFont.truetype(EN_FONT, size, index=1 if bold else 0)


# --- gradient background ---------------------------------------------------
img = Image.new("RGB", (W, H), BG_TOP)
draw = ImageDraw.Draw(img)
for y in range(H):
    t = y / H
    r = int(BG_TOP[0] * (1 - t) + BG_BOT[0] * t)
    g = int(BG_TOP[1] * (1 - t) + BG_BOT[1] * t)
    b = int(BG_TOP[2] * (1 - t) + BG_BOT[2] * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# --- faint grid -----------------------------------------------------------
grid_color = (38, 52, 72)
step = 80
for x in range(0, W, step):
    draw.line([(x, 0), (x, H)], fill=grid_color, width=1)
for y in range(0, H, step):
    draw.line([(0, y), (W, y)], fill=grid_color, width=1)

# --- top tag bar ---------------------------------------------------------
tag_text = "BACKEND  ·  BATCH PROCESSING  ·  SPRING ECOSYSTEM"
tag_font = efont(34)
tw = draw.textlength(tag_text, font=tag_font)
draw.text(((W - tw) / 2, 150), tag_text, font=tag_font, fill=DIM)

# Accent line under tag
draw.line([(W / 2 - 220, 220), (W / 2 + 220, 220)], fill=SPRING, width=4)

# --- title block ---------------------------------------------------------
# Pre-title (small Korean line)
pre_title = "직접 짜본 사람을 위한"
pre_font = kfont(72, idx=4)
ptw = draw.textlength(pre_title, font=pre_font)
draw.text(((W - ptw) / 2, 360), pre_title, font=pre_font, fill=GRAY)

# Main title - "Spring Batch 6"
big_font = efont(220, bold=True)
main_title = "Spring Batch 6"
mtw = draw.textlength(main_title, font=big_font)
draw.text(((W - mtw) / 2, 470), main_title, font=big_font, fill=WHITE)

# Underline accent
draw.line([(W / 2 - 320, 720), (W / 2 + 320, 720)], fill=SPRING, width=6)

# Subtitle
subt = "첫 잡부터 운영까지"
sub_font = kfont(108, idx=8)
swidth = draw.textlength(subt, font=sub_font)
draw.text(((W - swidth) / 2, 760), subt, font=sub_font, fill=ACCENT)

# --- chunk pipeline (centered, three groups, fits within margins) --------
band_y = 1080
chunk_w, chunk_h = 150, 100
gap_inner = 18
gap_arrow = 60

# Layout: [3 read] -> [3 proc] -> [3 write]
group_w = chunk_w * 3 + gap_inner * 2
total_w = group_w * 3 + gap_arrow * 2
start_x = (W - total_w) // 2


def draw_chunk(x: int, y: int, label: str, mode: str = "normal"):
    if mode == "highlight":
        fill = CHUNK_BG_HI
        border = SPRING
        line_color = ACCENT
    else:
        fill = CHUNK_BG
        border = CHUNK_BORDER
        line_color = (130, 150, 170)
    draw.rounded_rectangle(
        [x, y, x + chunk_w, y + chunk_h],
        radius=10,
        fill=fill,
        outline=border,
        width=3,
    )
    for i in range(3):
        ly = y + 22 + i * 22
        draw.line([(x + 22, ly), (x + chunk_w - 22, ly)], fill=line_color, width=3)
    lf = efont(22, bold=True)
    lw = draw.textlength(label, font=lf)
    draw.text((x + (chunk_w - lw) / 2, y + chunk_h + 12), label, font=lf, fill=GRAY)


def draw_arrow(x: int, y: int, length: int = 50):
    draw.line([(x, y), (x + length, y)], fill=SPRING, width=5)
    draw.polygon(
        [(x + length, y - 10), (x + length, y + 10), (x + length + 18, y)],
        fill=SPRING,
    )


groups = [
    ("READ", "normal"),
    ("PROCESS", "highlight"),
    ("WRITE", "normal"),
]
cx = start_x
for gi, (label, mode) in enumerate(groups):
    for ci in range(3):
        draw_chunk(cx, band_y, label, mode=mode)
        cx += chunk_w + gap_inner
    cx -= gap_inner  # remove last inner gap
    if gi < 2:
        draw_arrow(cx + 10, band_y + chunk_h // 2, length=35)
        cx += gap_arrow

# Pipeline caption
pl_label = "Chunk-Oriented Processing"
pf = efont(34)
plw = draw.textlength(pl_label, font=pf)
draw.text(((W - plw) / 2, band_y + chunk_h + 75), pl_label, font=pf, fill=DIM)

# --- code-style decoration (between pipeline and bottom) -----------------
code_lines = [
    "@Bean",
    "Job paymentSettlementJob(JobRepository jr, Step run) {",
    "    return new JobBuilder(\"settlement\", jr)",
    "            .start(run)",
    "            .build();",
    "}",
]
code_font = ImageFont.truetype(EN_FONT, 30)
code_y = 1450
code_x = 200
# code panel background
panel_pad = 32
panel_w = W - 400
panel_h = len(code_lines) * 44 + panel_pad * 2
draw.rounded_rectangle(
    [code_x - panel_pad, code_y - panel_pad,
     code_x - panel_pad + panel_w, code_y - panel_pad + panel_h],
    radius=14,
    fill=(20, 30, 48),
    outline=(50, 70, 95),
    width=2,
)
# tiny window dots
for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
    dot_x = code_x - panel_pad + 24 + i * 22
    dot_y = code_y - panel_pad + 22
    draw.ellipse([dot_x, dot_y, dot_x + 14, dot_y + 14], fill=c)

# render code with simple syntax color
def render_code_line(x: int, y: int, line: str):
    # naive coloring
    if line.lstrip().startswith("@"):
        draw.text((x, y), line, font=code_font, fill=ACCENT)
    elif line.lstrip().startswith("//"):
        draw.text((x, y), line, font=code_font, fill=(110, 130, 150))
    else:
        # split into tokens for keywords
        keywords = {"return", "new"}
        types = {"Job", "Step", "JobRepository", "JobBuilder"}
        tokens = []
        cur = ""
        for ch in line:
            if ch.isalnum() or ch == "_":
                cur += ch
            else:
                if cur:
                    tokens.append(cur)
                    cur = ""
                tokens.append(ch)
        if cur:
            tokens.append(cur)
        cx = x
        for tok in tokens:
            if tok in keywords:
                color = (199, 146, 234)
            elif tok in types:
                color = (130, 200, 255)
            elif tok.startswith('"') or '"' in tok:
                color = (255, 200, 130)
            else:
                color = (200, 210, 220)
            draw.text((cx, y), tok, font=code_font, fill=color)
            cx += draw.textlength(tok, font=code_font)


for i, line in enumerate(code_lines):
    render_code_line(code_x + 60, code_y + 28 + i * 44, line)
# line numbers
for i in range(len(code_lines)):
    ln = str(i + 1)
    lf2 = ImageFont.truetype(EN_FONT, 24)
    draw.text((code_x + 8, code_y + 32 + i * 44), ln, font=lf2, fill=(80, 100, 125))

# --- bottom block: author + footer --------------------------------------
draw.line([(220, H - 360), (W - 220, H - 360)], fill=SPRING, width=3)

author = "Toby-AI"
af = efont(70, bold=True)
aw = draw.textlength(author, font=af)
draw.text(((W - aw) / 2, H - 310), author, font=af, fill=WHITE)

byline = "지음"
bf = kfont(40, idx=4)
bw = draw.textlength(byline, font=bf)
draw.text(((W - bw) / 2, H - 215), byline, font=bf, fill=GRAY)

# Spring leaf badge bottom-right corner
leaf_cx, leaf_cy = W - 200, H - 250
# stylized leaf: ellipse rotated
leaf_img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
leaf_draw = ImageDraw.Draw(leaf_img)
leaf_draw.ellipse([10, 30, 190, 170], fill=SPRING)
leaf_draw.line([(20, 100), (180, 100)], fill=(20, 40, 20), width=3)
leaf_rot = leaf_img.rotate(-30, resample=Image.BICUBIC, expand=True)
img.paste(leaf_rot, (leaf_cx - leaf_rot.width // 2, leaf_cy - leaf_rot.height // 2), leaf_rot)

# Footer
footer = "Book Writer Harness  v1.0"
ff = efont(28)
fw = draw.textlength(footer, font=ff)
draw.text(((W - fw) / 2, H - 110), footer, font=ff, fill=DIM)

# --- save ----------------------------------------------------------------
img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT} ({W}x{H})")
