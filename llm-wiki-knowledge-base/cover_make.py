#!/usr/bin/env python3
"""Typography + wiki-lattice cover, rendered with ImageMagick.
Concept A: one symbol (a lattice of linked markdown pages, one agent node
reading through it) + large Korean typography on a muted dark ground."""
import math
import random
import subprocess
import sys

OUT = sys.argv[1]
W, H = 1600, 2560
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
FONT_LATIN = "/System/Library/Fonts/HelveticaNeue.ttc"

BG_TOP, BG_BOT = "#0F1420", "#131B2C"
INK = "#F3F5F8"
MUTED = "#9AA5B8"
EDGE = "#2C3850"
NODE = "#6A7A96"
NODE_LINE = "#1B2232"
ACCENT = "#E8A33D"

TITLE_1 = "쌓이는 지식,"
TITLE_2 = "답하는 에이전트"
SUB_1 = "LLM 위키 패턴으로 짓는"
SUB_2 = "사내 지식 베이스와 Claude 에이전트"
AUTHOR = "Toby-AI"

# ---- lattice layout --------------------------------------------------------
rng = random.Random(20261012)
X0, X1, Y0, Y1 = 180, 1420, 1080, 2180
COLS, ROWS = 5, 5
nodes = []
cw, rh = (X1 - X0) / (COLS - 1), (Y1 - Y0) / (ROWS - 1)
for r in range(ROWS):
    for c in range(COLS):
        if rng.random() < 0.14:          # a few gaps: the lattice is still growing
            continue
        x = X0 + c * cw + rng.uniform(-70, 70)
        y = Y0 + r * rh + rng.uniform(-55, 55)
        nodes.append((x, y))

def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

edges = set()
for i, a in enumerate(nodes):
    near = sorted(((dist(a, b), j) for j, b in enumerate(nodes) if j != i))[:3]
    for k, (_, j) in enumerate(near):
        if k < 2 or rng.random() < 0.45:
            edges.add(tuple(sorted((i, j))))

# agent node: the one nearest the lattice centre, slightly lower
cx, cy = (X0 + X1) / 2, (Y0 + Y1) / 2 + 60
agent = min(range(len(nodes)), key=lambda i: dist(nodes[i], (cx, cy)))
agent_edges = {e for e in edges if agent in e}
# reading path: hop two steps out from the agent along existing edges
path = set(agent_edges)
frontier = {j for e in agent_edges for j in e if j != agent}
for j in frontier:
    for e in edges:
        if j in e and agent not in e and rng.random() < 0.5:
            path.add(e)

PW, PH = 54, 70  # a page is a small portrait rectangle

def page(x, y, fill, line, alpha=1.0):
    d = [f"fill {fill} stroke {line} stroke-width 2 "
         f"roundrectangle {x-PW/2:.0f},{y-PH/2:.0f} {x+PW/2:.0f},{y+PH/2:.0f} 6,6"]
    # three "text lines" on the page
    for k in range(3):
        ly = y - PH / 2 + 16 + k * 14
        lw = PW - 18 - (10 if k == 2 else 0)
        d.append(f"fill none stroke {line} stroke-width 3 "
                 f"line {x-PW/2+9:.0f},{ly:.0f} {x-PW/2+9+lw:.0f},{ly:.0f}")
    return d

draw = []
# edges (muted first, accent path on top)
for i, j in edges:
    if (i, j) in path:
        continue
    (xa, ya), (xb, yb) = nodes[i], nodes[j]
    draw.append(f"fill none stroke {EDGE} stroke-width 3 line {xa:.0f},{ya:.0f} {xb:.0f},{yb:.0f}")
for i, j in path:
    (xa, ya), (xb, yb) = nodes[i], nodes[j]
    draw.append(f"fill none stroke {ACCENT} stroke-width 4 line {xa:.0f},{ya:.0f} {xb:.0f},{yb:0f}")
# pages
path_nodes = {n for e in path for n in e}
for i, (x, y) in enumerate(nodes):
    if i == agent:
        continue
    if i in path_nodes:
        draw += page(x, y, "#2A2415", ACCENT)
    else:
        draw += page(x, y, "#161E2E", NODE)
# agent node: soft glow + solid disc + small reading mark
ax, ay = nodes[agent]
for rad, a in ((110, 0.05), (80, 0.09), (55, 0.16)):
    draw.append(f"fill rgba(232,163,61,{a}) stroke none circle {ax:.0f},{ay:.0f} {ax+rad:.0f},{ay:.0f}")
draw.append(f"fill {ACCENT} stroke none circle {ax:.0f},{ay:.0f} {ax+30:.0f},{ay:.0f}")
draw.append(f"fill {BG_TOP} stroke none circle {ax:.0f},{ay:.0f} {ax+11:.0f},{ay:.0f}")

# ---- compose ---------------------------------------------------------------
cmd = [
    "magick", "-size", f"{W}x{H}", f"gradient:{BG_TOP}-{BG_BOT}",
    # faint grid texture to hint at engineering paper
    "(", "-size", f"{W}x{H}", "xc:none", "-fill", "none", "-stroke", "#1A2232",
    "-strokewidth", "1", "-draw",
    " ".join(f"line {x},0 {x},{H}" for x in range(0, W, 80)) + " " +
    " ".join(f"line 0,{y} {W},{y}" for y in range(0, H, 80)), ")",
    "-compose", "over", "-composite",
    "-draw", " ".join(draw),
    # accent rule above the title
    "-fill", ACCENT, "-stroke", "none",
    "-draw", "rectangle 160,300 300,308",
    # title
    "-font", FONT, "-gravity", "NorthWest",
    "-fill", INK, "-stroke", INK, "-strokewidth", "3", "-pointsize", "154",
    "-annotate", "+160+360", TITLE_1,
    "-annotate", "+160+540", TITLE_2,
    # subtitle
    "-stroke", "none", "-fill", MUTED, "-pointsize", "54",
    "-annotate", "+164+790", SUB_1,
    "-annotate", "+164+868", SUB_2,
    # author
    "-gravity", "South", "-fill", ACCENT, "-draw", "rectangle 770,2318 830,2322",
    "-font", FONT_LATIN, "-fill", MUTED, "-pointsize", "46",
    "-annotate", "+0+150", AUTHOR,
    "-strip", OUT,
]
subprocess.run(cmd, check=True)
print("wrote", OUT)
