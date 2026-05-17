#!/bin/bash
# Cover generation script for "에이전트의 시대, DDD는 여전히 유효한가?"
# Concept: Minimalist + 3-layer horizontal motif (변하는 것/살아남는 것/사라지는 것)
# Palette: deep teal-navy base, warm amber accent
#
# Layout zones (y coordinates on 2560 canvas):
#   0    -  240   : top margin + version mark (top-right)
#   240  -  380   : genre eyebrow label
#   380  -  1180  : main title block (3 lines)
#   1180 -  1280  : amber rule
#   1280 -  1380  : subtitle
#   1380 -  1900  : breathing room
#   1900 -  2150  : 3-layer motif (변/살/사)
#   2150 -  2300  : breathing room
#   2300 -  2440  : author + tagline
#   2440 -  2560  : bottom margin

set -euo pipefail

OUT="/Users/tobylee/workspace/ai/book-writer/.claude/worktrees/ai-ddd/ddd-in-ai-era/cover.png"
W=1600
H=2560

# Fonts
FONT_BOLD="$HOME/Library/Fonts/Pretendard-Black.otf"
FONT_SEMIBOLD="$HOME/Library/Fonts/Pretendard-SemiBold.otf"
FONT_REGULAR="$HOME/Library/Fonts/Pretendard-Regular.otf"
FONT_LIGHT="$HOME/Library/Fonts/Pretendard-Light.otf"

# Palette
BG_TOP="#0a1e2a"
BG_BOTTOM="#15102a"
ACCENT_AMBER="#d4a64a"
ACCENT_DIM="#8a6f3a"
TEXT_PRIMARY="#f5efe0"
TEXT_MUTED="#9a9ab5"
LAYER1="#5a7488"           # surviving (brightest)
LAYER2="#3a4a5e"           # changing (mid)
LAYER3="#252a3a"           # disappearing (faded)

TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

# 1. Gradient base
magick -size ${W}x${H} \
  gradient:"${BG_TOP}-${BG_BOTTOM}" \
  "$TMP/base.png"

# 2. Subtle noise overlay
magick "$TMP/base.png" \
  \( -size ${W}x${H} xc:gray50 +noise Gaussian -colorspace gray \
     -evaluate multiply 0.04 \) \
  -compose overlay -composite \
  "$TMP/base.png"

# 3. Three horizontal layers (lower-middle) — 변/살/사 metaphor
LAYER_X1=200
LAYER_X2=1400
magick "$TMP/base.png" \
  -fill "${LAYER1}" -draw "rectangle ${LAYER_X1},1940 ${LAYER_X2},1948" \
  -fill "${LAYER2}" -draw "rectangle ${LAYER_X1},2030 ${LAYER_X2},2036" \
  -fill "${LAYER3}" -draw "rectangle ${LAYER_X1},2120 ${LAYER_X2},2124" \
  "$TMP/base.png"

# 4. Dots: agent nodes / BC mapping. Three rows aligned with three layers.
python3 <<'PY' > /tmp/_dots.mvg
cols = 24
x_start = 220
x_end = 1380
y_positions = [1970, 2060, 2150]
step = (x_end - x_start) / (cols - 1)
print("push graphic-context")
for yi, y in enumerate(y_positions):
    for c in range(cols):
        x = int(x_start + c * step)
        opacity = [0.65, 0.40, 0.20][yi]
        r = 4 if yi == 0 else 3 if yi == 1 else 2
        # accent every 6th node in top row
        if yi == 0 and c % 6 == 0:
            print(f'fill "rgba(212,166,74,{min(opacity + 0.25, 1.0):.2f})" circle {x},{y} {x+r+1},{y}')
        else:
            print(f'fill "rgba(245,239,224,{opacity:.2f})" circle {x},{y} {x+r},{y}')
print("pop graphic-context")
PY
cp /tmp/_dots.mvg "$TMP/dots.mvg"
magick "$TMP/base.png" -draw "@$TMP/dots.mvg" "$TMP/base.png"

# 5. Genre eyebrow label (small caps, amber)
magick -background none -fill "${ACCENT_AMBER}" \
  -font "$FONT_SEMIBOLD" -pointsize 38 -kerning 8 \
  -size 1300x label:"AI · ARCHITECTURE · DDD" \
  "$TMP/genre.png"
magick "$TMP/base.png" \
  "$TMP/genre.png" -geometry +200+340 -composite \
  "$TMP/base.png"

# 6. Main title — three separate lines for clean stacking
#    Line 1: "에이전트의 시대,"
#    Line 2: "DDD는 여전히"
#    Line 3: "유효한가?"
#    Each line: pointsize 130, height ~ 180px including descenders
TITLE_FONT_SIZE=125

magick -background none -fill "${TEXT_PRIMARY}" \
  -font "$FONT_BOLD" -pointsize $TITLE_FONT_SIZE -kerning -2 \
  label:"에이전트의 시대," \
  "$TMP/t1.png"

magick -background none -fill "${TEXT_PRIMARY}" \
  -font "$FONT_BOLD" -pointsize $TITLE_FONT_SIZE -kerning -2 \
  label:"DDD는 여전히" \
  "$TMP/t2.png"

magick -background none -fill "${TEXT_PRIMARY}" \
  -font "$FONT_BOLD" -pointsize $TITLE_FONT_SIZE -kerning -2 \
  label:"유효한가?" \
  "$TMP/t3.png"

# Stack title lines starting at y=460, line height 175
magick "$TMP/base.png" \
  "$TMP/t1.png" -geometry +200+460 -composite \
  "$TMP/t2.png" -geometry +200+635 -composite \
  "$TMP/t3.png" -geometry +200+810 -composite \
  "$TMP/base.png"

# 7. Amber rule beneath title
magick "$TMP/base.png" \
  -fill "${ACCENT_AMBER}" -draw "rectangle 200,1030 380,1034" \
  "$TMP/base.png"

# 8. Subtitle — three phrases separated by amber middots
magick -background none -fill "${TEXT_MUTED}" \
  -font "$FONT_LIGHT" -pointsize 54 -kerning 2 \
  label:"변하는 것  ·  살아남는 것  ·  사라지는 것" \
  "$TMP/subtitle.png"
magick "$TMP/base.png" \
  "$TMP/subtitle.png" -geometry +200+1080 -composite \
  "$TMP/base.png"

# 9. Author block — bottom area
magick -background none -fill "${TEXT_PRIMARY}" \
  -font "$FONT_SEMIBOLD" -pointsize 58 -kerning 4 \
  label:"Toby-AI" \
  "$TMP/author.png"
magick "$TMP/base.png" \
  "$TMP/author.png" -geometry +200+2310 -composite \
  "$TMP/base.png"

# 10. Tagline under author
magick -background none -fill "${TEXT_MUTED}" \
  -font "$FONT_LIGHT" -pointsize 30 -kerning 3 \
  label:"An Essay on Domain-Driven Design in the Age of Agents" \
  "$TMP/tagline.png"
magick "$TMP/base.png" \
  "$TMP/tagline.png" -geometry +200+2400 -composite \
  "$TMP/base.png"

# 11. Top-right corner mark — vertical accent + version
magick "$TMP/base.png" \
  -fill "${ACCENT_DIM}" -draw "rectangle 1370,200 1374,310" \
  "$TMP/base.png"

magick -background none -fill "${TEXT_MUTED}" \
  -font "$FONT_REGULAR" -pointsize 26 -kerning 3 \
  label:"v1.0" \
  "$TMP/version.png"
magick "$TMP/base.png" \
  "$TMP/version.png" -geometry +1390+250 -composite \
  "$TMP/base.png"

# 12. Final output
magick "$TMP/base.png" -strip -quality 95 "$OUT"

echo "Cover generated: $OUT"
identify "$OUT"
