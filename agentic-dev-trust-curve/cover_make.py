import subprocess, math
W, H = 1600, 2560
OUT = "/private/tmp/claude-501/-Users-tobylee-workspace-ai-book-writer/07574c00-f2e3-4bf3-b5e9-4c7ea302df03/scratchpad/cover/cover.png"
F = "/Users/tobylee/Library/Fonts/NotoSansKR-%s.ttf"
BG, INK, PAPER, AMBER, MUTED, LINE = "#15202f", "#15202f", "#f2ede3", "#e3a94f", "#9aa6b5", "#2a3a4e"

# ---- trust curve: smooth cubic bezier, left-low -> right-high ----
P0, P1, P2, P3 = (170, 1980), (650, 1980), (900, 1250), (1430, 1230)
def bez(t):
    u = 1 - t
    x = u**3*P0[0] + 3*u*u*t*P1[0] + 3*u*t*t*P2[0] + t**3*P3[0]
    y = u**3*P0[1] + 3*u*u*t*P1[1] + 3*u*t*t*P2[1] + t**3*P3[1]
    return x, y
pts = [bez(i/200) for i in range(201)]
poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def y_at(xq):
    best = min(pts, key=lambda p: abs(p[0]-xq)); return best[1]

stages = [  # (x, label, dot count)
    (300, "지켜보기", 1),
    (640, "자가 검증", 2),
    (980, "클라우드", 3),
    (1320, "자동 머지", 5),
]

draw = []
# subtle grid baseline rule under the curve area
draw += [f"-fill none -stroke '{LINE}' -strokewidth 2 -draw \"line 170,2060 1430,2060\""]
# faint stage ticks
for x, _, _ in stages:
    draw += [f"-stroke '{LINE}' -strokewidth 2 -draw \"line {x},2040 {x},2080\""]
# the curve (soft glow under + crisp line)
draw += [f"-fill none -stroke '#e3a94f22' -strokewidth 34 -draw \"polyline {poly}\""]
draw += [f"-fill none -stroke '{AMBER}' -strokewidth 11 -draw \"polyline {poly}\""]
# stage markers: hollow ring on curve + dot clusters rising above
for x, label, n in stages:
    y = y_at(x)
    draw += [f"-fill '{BG}' -stroke '{AMBER}' -strokewidth 8 -draw \"circle {x},{y:.0f} {x+18},{y:.0f}\""]
    # agents: small filled dots stacked in a tidy column above the ring
    gap = 46
    for k in range(n):
        dy = 70 + k*gap
        r = 13
        draw += [f"-fill '{PAPER}' -stroke none -draw \"circle {x},{y-dy:.0f} {x+r},{y-dy:.0f}\""]
    # label below baseline

cmd = f"""/opt/homebrew/bin/magick -size {W}x{H} xc:'{BG}' \
  -gravity NorthWest \
  -font '{F % 'Medium'}' -pointsize 34 -fill '{AMBER}' -kerning 8 -annotate +170+300 'TRUST CURVE' \
  -font '{F % 'Bold'}' -pointsize 176 -fill '{PAPER}' -kerning -4 -interline-spacing -20 -annotate +160+380 '에이전트를\\n믿어도 될까' \
  -font '{F % 'Light'}' -pointsize 54 -fill '{PAPER}' -kerning 0 -interline-spacing 10 -annotate +170+880 '신뢰 곡선으로 배우는' \
  -font '{F % 'Regular'}' -pointsize 54 -fill '{PAPER}' -annotate +170+960 'Claude Code · Codex 실전 개발' \
  {" ".join(draw)} \
  -gravity NorthWest -stroke none -fill '{MUTED}' -font '{F % 'Medium'}' -pointsize 36 \
"""
# centered stage labels via gravity North with x offset from center
for x, label, _ in stages:
    off = x - W//2
    sign = "+" if off >= 0 else "-"
    cmd += f"  -gravity North -annotate {sign}{abs(off)}+2100 '{label}' \\\n"
cmd += f"""  -gravity SouthWest -fill '{PAPER}' -font '{F % 'Regular'}' -pointsize 40 -kerning 2 -annotate +170+200 'Toby-AI' \
  -gravity SouthEast -fill '{MUTED}' -font '{F % 'Light'}' -pointsize 30 -kerning 3 -annotate +170+206 'for Java/Spring · React/Next.js developers' \
  '{OUT}'"""
print(cmd)
subprocess.run(cmd, shell=True, check=True)
