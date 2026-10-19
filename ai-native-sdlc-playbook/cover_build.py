#!/usr/bin/env python3
"""Build the cover for 'AI 네이티브 SDLC 플레이북' with ImageMagick draw primitives.
Concept A: dark engineering base, one amber accent, six-node loop diagram, big Korean title.
"""
import math
import subprocess
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "cover.png"
F = "/private/tmp/claude-501/-Users-tobylee-workspace-ai-book-writer/ad84f7b5-f900-4494-9eac-0f196310ede8/scratchpad/fonts/"
GOTHIC_HEAVY = F + "AppleSDGothicNeo-Heavy.ttf"
GOTHIC_BOLD = F + "AppleSDGothicNeo-Bold.ttf"
GOTHIC_MED = F + "AppleSDGothicNeo-Medium.ttf"
GOTHIC_REG = F + "AppleSDGothicNeo-Regular.ttf"
MONO = F + "Menlo-Regular.ttf"
MONO_B = F + "Menlo-Bold.ttf"
D2 = F + "D2Coding.ttf"

W, H = 1600, 2560
BG0, BG1 = "#13203A", "#0A1020"      # radial gradient center -> edge
INK = "#EEF2F7"                      # title white
INK2 = "#B9C4D3"                     # subtitle grey
DIM = "#6B7A90"                      # dim labels
RING = "#2E3F5C"                     # muted ring
ACCENT = "#F2A93B"                   # single accent (amber)
MARGIN = 140

CX, CY, R = 800, 1660, 430           # loop center / radius


def text_width(font, size, text, kerning=0):
    out = subprocess.check_output([
        "magick", "-font", font, "-pointsize", str(size), "-kerning", str(kerning),
        f"label:{text}", "-format", "%w", "info:"]).decode().strip()
    return int(out)


def pt(angle_deg, radius, cx=CX, cy=CY):
    a = math.radians(angle_deg)
    return cx + radius * math.cos(a), cy + radius * math.sin(a)


cmd = ["magick", "-size", f"{W}x{H}", f"radial-gradient:{BG0}-{BG1}"]

# --- subtle dot grid texture -------------------------------------------------
dots = []
for y in range(60, H, 80):
    for x in range(60, W, 80):
        dots.append(f"point {x},{y}")
cmd += ["-fill", "#FFFFFF", "-draw", "fill-opacity 0.10 " + " ".join(dots)]
# thicker 2x2 dots read better at full size
cmd += ["-stroke", "none", "-fill", "#FFFFFF", "-draw",
        "fill-opacity 0.08 " + " ".join(f"rectangle {x},{y} {x+1},{y+1}" for y in range(60, H, 80) for x in range(60, W, 80))]

# --- top label strip ---------------------------------------------------------
cmd += ["-fill", ACCENT, "-draw", f"rectangle {MARGIN},150 {MARGIN+56},155"]
cmd += ["-font", MONO_B, "-pointsize", "30", "-kerning", "6", "-fill", ACCENT,
        "-gravity", "NorthWest", "-annotate", f"+{MARGIN+80}+136", "PLAYBOOK  /  12 PLAYS  /  6 STAGES"]

# --- title -------------------------------------------------------------------
title1, title2 = "AI 네이티브", "SDLC 플레이북"
tsize = 168
while text_width(GOTHIC_HEAVY, tsize, title2) > W - 2 * MARGIN:
    tsize -= 4
cmd += ["-font", GOTHIC_HEAVY, "-pointsize", str(tsize), "-kerning", "-2", "-fill", INK,
        "-gravity", "NorthWest",
        "-annotate", f"+{MARGIN-6}+250", title1,
        "-annotate", f"+{MARGIN-6}+{250+int(tsize*1.18)}", title2]

# --- subtitle ----------------------------------------------------------------
sub1, sub2 = "Claude Code로 내 개발 루프를", "다시 짜는 12가지 플레이"
sy = 250 + int(tsize * 1.18) + int(tsize * 1.3) + 10
cmd += ["-font", GOTHIC_MED, "-pointsize", "58", "-kerning", "0", "-fill", INK2,
        "-annotate", f"+{MARGIN}+{sy}", sub1,
        "-annotate", f"+{MARGIN}+{sy+82}", sub2]

# --- human judgement line (above the loop) -----------------------------------
hy = CY - R - 300
cmd += ["-font", MONO, "-pointsize", "28", "-kerning", "2", "-fill", DIM, "-gravity", "North",
        "-annotate", f"+0+{hy-44}", "The loop keeps running.  Human judgement stays above it."]
cmd += ["-stroke", "none", "-fill", INK2, "-draw", f"fill-opacity 0.55 rectangle {MARGIN},{hy} {W-MARGIN},{hy+2}"]
# small "human" marker: a hollow circle sitting on the line, centered
cmd += ["-fill", BG1, "-stroke", ACCENT, "-strokewidth", "6",
        "-draw", f"circle {CX},{hy+1} {CX+22},{hy+1}"]

# --- the loop ----------------------------------------------------------------
stages = ["PLAN", "DESIGN", "BUILD", "TEST", "DEPLOY", "MAINTAIN"]
angles = [-90, -30, 30, 90, 150, 210]
artifacts = ["intent.md", "spec.md", "plan.md + diff", "tests pass", "PR + REVIEW.md", "new intent.md"]

# muted full ring
cmd += ["-fill", "none", "-stroke", RING, "-strokewidth", "12",
        "-draw", f"circle {CX},{CY} {CX+R},{CY}"]

# accent arc: MAINTAIN (210°) -> PLAN (270°), clockwise in screen space
x0, y0 = pt(210, R)
x1, y1 = pt(270, R)
cmd += ["-fill", "none", "-stroke", ACCENT, "-strokewidth", "14",  
        "-draw", f"stroke-linecap round path 'M {x0:.1f},{y0:.1f} A {R},{R} 0 0,1 {x1:.1f},{y1:.1f}'"]

# direction chevrons at arc midpoints (on the ring)
for i, a in enumerate(angles):
    mid = a + 30
    mx, my = pt(mid, R)
    # tangent direction (clockwise on screen => increasing angle)
    t = math.radians(mid + 90)
    tx, ty = math.cos(t), math.sin(t)
    nx, ny = -math.sin(t), math.cos(t)   # normal (outward is (cos mid, sin mid)); use radial instead
    rx, ry = math.cos(math.radians(mid)), math.sin(math.radians(mid))
    size = 22
    tip = (mx + tx * size, my + ty * size)
    b1 = (mx - tx * size * 0.4 + rx * size, my - ty * size * 0.4 + ry * size)
    b2 = (mx - tx * size * 0.4 - rx * size, my - ty * size * 0.4 - ry * size)
    col = ACCENT if i == 5 else "#4B5E7F"
    cmd += ["-fill", "none", "-stroke", col, "-strokewidth", "10",  
            "-draw", f"stroke-linejoin round polyline {b1[0]:.1f},{b1[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} {b2[0]:.1f},{b2[1]:.1f}"]

# artifact labels inside the ring at arc midpoints
for i, a in enumerate(angles):
    mid = a + 30
    lx, ly = pt(mid, R - 62)
    label = artifacts[i]
    col = ACCENT if i == 5 else DIM
    wdt = text_width(D2, 30, label)
    # anchor so text sits inside: shift toward center by half width along x
    ax = lx - wdt / 2 - math.cos(math.radians(mid)) * (wdt / 2) * 0.9
    ay = ly + 10
    cmd += ["-font", D2, "-pointsize", "30", "-kerning", "0", "-fill", col, "-stroke", "none",
            "-gravity", "NorthWest", "-annotate", f"+{ax:.0f}+{ay-30:.0f}", label]

# nodes
for i, a in enumerate(angles):
    nx, ny = pt(a, R)
    if i == 0:
        cmd += ["-fill", ACCENT, "-stroke", BG1, "-strokewidth", "10",
                "-draw", f"circle {nx:.1f},{ny:.1f} {nx+30:.1f},{ny:.1f}"]
    else:
        cmd += ["-fill", BG1, "-stroke", INK, "-strokewidth", "9",
                "-draw", f"circle {nx:.1f},{ny:.1f} {nx+24:.1f},{ny:.1f}"]

# stage labels outside the ring
for i, a in enumerate(angles):
    label = stages[i]
    wdt = text_width(MONO_B, 40, label, kerning=5)
    lx, ly = pt(a, R + 78)
    c = math.cos(math.radians(a))
    # horizontal anchor: left-side labels end at lx, right-side start at lx, top/bottom centered
    ax = lx - wdt / 2 + c * (wdt / 2) * 1.0
    ay = ly - 20
    if i == 0:
        ay = ly - 40
    if i == 3:
        ay = ly + 0
    col = ACCENT if i == 0 else INK
    cmd += ["-font", MONO_B, "-pointsize", "40", "-kerning", "5", "-fill", col, "-stroke", "none",
            "-gravity", "NorthWest", "-annotate", f"+{ax:.0f}+{ay:.0f}", label]

# --- faint intent.md texture in the center -----------------------------------
lines = ["# intent.md", "", "problem:", "outcome:", "constraints:"]
cmd += ["-font", D2, "-pointsize", "34", "-kerning", "0", "-fill", "#9FB0C8", "-stroke", "none",
        "-gravity", "NorthWest"]
tx0 = CX - text_width(D2, 34, "constraints:") // 2
ty0 = CY - 100
for k, ln in enumerate(lines):
    if ln:
        cmd += ["-annotate", f"+{tx0}+{ty0 + k*44}", ln]
# apply opacity to this text by drawing in low alpha color instead
# (replace colour above with alpha variant)
for idx, v in enumerate(cmd):
    if v == "#9FB0C8":
        cmd[idx] = "#9FB0C833"

# --- author ------------------------------------------------------------------
cmd += ["-fill", ACCENT, "-stroke", "none", "-draw", f"rectangle {CX-24},2368 {CX+24},2372"]
cmd += ["-font", GOTHIC_MED, "-pointsize", "44", "-kerning", "4", "-fill", INK2, "-gravity", "North",
        "-annotate", "+0+2400", "Toby-AI"]

cmd += ["-strip", OUT]
subprocess.check_call(cmd)
print("wrote", OUT, "title size", tsize)
