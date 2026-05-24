#!/usr/bin/env python3
"""
Cover generator for "생각의 상자".
Concept: a box at lower-center from which note-cards rise and connect
into a constellation/network — "외부화된 사고가 연결로 창발한다".
Renders a layered MVG (Magick Vector Graphics) draw script, then ImageMagick
composites typography on top. No external API needed.
"""
import math, random, subprocess, os

random.seed(42)  # deterministic, reproducible cover

W, H = 1600, 2560
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DRAW = os.path.join(OUT_DIR, "_constellation.mvg")
BG = os.path.join(OUT_DIR, "_bg.png")
OUT = os.path.join(OUT_DIR, "cover.png")

# Palette: deep ink blue -> midnight, warm paper accents, muted gold links
INK_TOP    = "#10182b"   # deep blue-black (top)
INK_BOT    = "#1c2a44"   # slightly lighter midnight (bottom)
PAPER      = "#ece3d4"   # warm paper neutral (cards / title)
PAPER_DIM  = "#c9bda6"   # dimmer paper
GOLD       = "#c9a25b"   # muted warm gold (key links / accent)
LINK       = "#5b6b8a"   # cool slate links

# ---- Build node network -------------------------------------------------
# A box anchor near lower third; cards emanate upward forming a constellation.
box_cx, box_cy = W * 0.5, H * 0.74
nodes = []

# central anchor (the box / Zettelkasten)
anchor = (box_cx, box_cy)

# generate cards in an upward fan / scatter (the "thoughts" rising)
n_cards = 16
for i in range(n_cards):
    ang = math.radians(random.uniform(200, 340))  # upward arc
    dist = random.uniform(160, 620)
    x = box_cx + math.cos(ang) * dist
    y = box_cy + math.sin(ang) * dist * 1.05
    # keep within frame, avoid title zone (top ~ up to y=760)
    x = max(150, min(W - 150, x))
    y = max(1230, min(H * 0.66, y))
    size = random.uniform(34, 74)
    nodes.append((x, y, size))

# ---- MVG draw script ----------------------------------------------------
mvg = []
mvg.append("push graphic-context")
mvg.append("fill none")

# faint background link web (subtle depth) between random node pairs
mvg.append(f"stroke '{LINK}40' stroke-width 1.2")
for _ in range(18):
    a = random.choice(nodes); b = random.choice(nodes)
    if a is b: continue
    mvg.append(f"line {a[0]:.0f},{a[1]:.0f} {b[0]:.0f},{b[1]:.0f}")

# primary links: anchor -> each card
mvg.append(f"stroke '{LINK}aa' stroke-width 1.8")
for (x, y, s) in nodes:
    mvg.append(f"line {anchor[0]:.0f},{anchor[1]:.0f} {x:.0f},{y:.0f}")

# a few highlighted GOLD links (the value-chain: notes -> emergent knowledge)
gold_targets = random.sample(nodes, 5)
mvg.append(f"stroke '{GOLD}cc' stroke-width 2.6")
for (x, y, s) in gold_targets:
    mvg.append(f"line {anchor[0]:.0f},{anchor[1]:.0f} {x:.0f},{y:.0f}")

# inter-card gold links to suggest emergence/connection-of-connections
for i in range(4):
    a, b = random.sample(gold_targets, 2)
    mvg.append(f"line {a[0]:.0f},{a[1]:.0f} {b[0]:.0f},{b[1]:.0f}")

# ---- draw the cards (small rounded note-cards, slightly rotated) ---------
def card(x, y, s, fill, op="ff", rot=0):
    h = s * 1.3
    out = ["push graphic-context",
           f"translate {x:.1f},{y:.1f}", f"rotate {rot:.1f}",
           "fill none",
           f"stroke '{PAPER_DIM}80' stroke-width 1",
           f"fill '{fill}{op}'",
           f"roundrectangle {-s/2:.1f},{-h/2:.1f} {s/2:.1f},{h/2:.1f} 5,5"]
    # tiny "text lines" on the card to read as a note
    out.append(f"fill '{INK_TOP}55' stroke none")
    for li in range(3):
        ly = -h/2 + s*0.32 + li*(s*0.28)
        out.append(f"rectangle {-s/2+s*0.18:.1f},{ly:.1f} {s/2-s*0.18:.1f},{ly+2:.1f}")
    out.append("pop graphic-context")
    return out

mvg.append("stroke none")
for (x, y, s) in nodes:
    is_gold = (x, y, s) in gold_targets
    fill = PAPER if is_gold else PAPER_DIM
    op = "ff" if is_gold else "cc"
    rot = random.uniform(-12, 12)
    mvg += card(x, y, s, fill, op, rot)

# ---- the box (Zettelkasten) at the anchor --------------------------------
bw, bh = 290, 188
bx, by = anchor[0], anchor[1]
mvg.append("push graphic-context")
mvg.append(f"translate {bx:.0f},{by:.0f}")
# box body
mvg.append(f"stroke '{GOLD}' stroke-width 3 fill '{INK_BOT}'")
mvg.append(f"roundrectangle {-bw/2:.0f},{-bh*0.25:.0f} {bw/2:.0f},{bh*0.75:.0f} 10,10")
# open lid (perspective trapezoid) using path
lid = f"path 'M {-bw/2:.0f},{-bh*0.25:.0f} L {-bw/2+34:.0f},{-bh*0.78:.0f} L {bw/2+34:.0f},{-bh*0.78:.0f} L {bw/2:.0f},{-bh*0.25:.0f} Z'"
mvg.append(f"stroke '{GOLD}' stroke-width 3 fill '{INK_TOP}'")
mvg.append(lid)
# index-card slots inside
mvg.append(f"stroke '{PAPER_DIM}cc' stroke-width 2 fill none")
for k in range(3):
    yy = -bh*0.1 + k*14
    mvg.append(f"line {-bw/2+22:.0f},{yy:.0f} {bw/2-22:.0f},{yy:.0f}")
mvg.append("pop graphic-context")

# glow nodes (dots) at each card link origin for sparkle
mvg.append(f"stroke none fill '{GOLD}'")
for (x, y, s) in gold_targets:
    mvg.append(f"circle {x:.0f},{y:.0f} {x+3:.0f},{y:.0f}")

mvg.append("pop graphic-context")

with open(DRAW, "w") as f:
    f.write("\n".join(mvg))

# ---- 1. gradient background --------------------------------------------
subprocess.run([
    "magick", "-size", f"{W}x{H}",
    f"gradient:{INK_TOP}-{INK_BOT}", BG
], check=True)

# subtle vignette + paper grain via noise overlay baked at composite stage
# ---- 2. draw constellation on bg ---------------------------------------
LAYER = os.path.join(OUT_DIR, "_layer.png")
subprocess.run([
    "magick", BG,
    "-draw", f"@{DRAW}",
    LAYER
], check=True)

print("constellation layer built:", LAYER)
