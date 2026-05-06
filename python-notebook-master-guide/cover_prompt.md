# Cover Design Log

## Version 1 (2026-05-06)

### Concept
- **Type:** A — Minimalism + symbolic accent
- **Tool:** ImageMagick (no image-gen MCP available in environment)
- **Rationale:** 차분한 기술서 톤 + 큐레이션·에세이 느낌. 셀(가로 줄) 메타포로
  "노트북"을 암시하고, 매직 커맨드 `%`를 강한 마젠타 액센트로 좌상단에 배치해
  "도구 안의 약속된 신호"라는 책의 큐레이션 정체성을 드러냈다. 9개 컬러 도트는
  비교 대상 9개 환경의 다양성을 시각적으로 응축한다.

### Design specs
- **Canvas:** 1600 × 2560 (1.6:1 portrait, EPUB-grade)
- **Palette:**
  - Background: `#0f1729` (deep navy, 신뢰감)
  - Cell-row lines: `#1b253c` (subtle, 56px 간격, 노트북 셀 메타포)
  - Title: `#f5f7fa` (off-white)
  - Subtitle: `#9aa5b8` (muted slate)
  - Accent `%`: `#ec4899` (magenta, 매직 커맨드의 신호 색)
  - Author: `#e2e8f0`
  - 9 dots: blue → cyan → green → lime → yellow → orange → red → pink → purple
- **Font:** Apple SD Gothic Neo (한글 글리프 안전)
- **Layout:**
  - 상단: kicker `PYTHON NOTEBOOK GUIDE` + 거대한 `%` 심볼 + 가로 마젠타 라인
  - 중앙: 제목 2줄 (168pt), 부제 2줄 (64pt)
  - 중하단: `9 ENVIRONMENTS COMPARED` + 컬러 dot 9개
  - 바닥: 짧은 구분선 + `Toby-AI` (56pt) + `BOOK WRITER HARNESS` 캡션

### English image-gen prompt (참고용 — MCP 가용 시 재생성에 사용)

```
A minimalist editorial book cover, portrait format 1600x2560.
Deep navy background (#0f1729) with very subtle horizontal cell-row
lines spaced like a notebook's executable cells. Top-left: a single
oversized magenta '%' glyph in a clean sans-serif (the Jupyter magic
command sigil), with a small uppercase kicker "PYTHON NOTEBOOK GUIDE"
above it and a thin horizontal magenta accent line below. Center:
the Korean title "Python 노트북 마스터 가이드" in two lines, set in
a light, modern Korean sans-serif (Apple SD Gothic Neo / Noto Sans KR),
crisp off-white. Below the title: subtitle "Jupyter부터 Marimo까지,
도구를 가르는 안목" in muted slate gray, two lines, lighter weight.
Mid-lower band: tiny caption "9 ENVIRONMENTS COMPARED" with a
horizontal row of nine small filled circles in a saturated rainbow
(blue, cyan, green, lime, yellow, orange, red, pink, purple).
Bottom: a short white horizontal rule, then "Toby-AI" in elegant
sans-serif, and a small caption "BOOK WRITER HARNESS" beneath.
Editorial, contemplative, confident. No stock photography, no
generic tech gradient, no laptop imagery, no python snake clichés.
```

### ImageMagick command (실제 생성에 사용)

```bash
# Step 1 — base + cell-row lines
DRAW=""
for y in $(seq 120 56 2440); do
  DRAW="$DRAW rectangle 110,${y} 1490,$((y+1))"
done
magick -size 1600x2560 xc:"#0f1729" -fill "#1b253c" -draw "$DRAW" base.png

# Step 2 — accent line + % + kicker + title + subtitle
GOTHIC="/System/Library/Fonts/AppleSDGothicNeo.ttc"
magick base.png \
  \( -size 1380x4 xc:"#ec4899" \) -gravity north -geometry +0+360 -composite \
  -font "$GOTHIC" -fill "#ec4899" -pointsize 240 \
    -gravity northwest -annotate +130+140 "%" \
  -font "$GOTHIC" -fill "#9aa5b8" -pointsize 42 \
    -gravity northwest -annotate +130+90 "PYTHON  NOTEBOOK  GUIDE" \
  -font "$GOTHIC" -fill "#f5f7fa" -pointsize 168 -kerning -4 \
    -gravity center -annotate +0-380 "Python 노트북" \
    -gravity center -annotate +0-180 "마스터 가이드" \
  -font "$GOTHIC" -fill "#9aa5b8" -pointsize 64 \
    -gravity center -annotate +0+80 "Jupyter부터 Marimo까지," \
    -gravity center -annotate +0+170 "도구를 가르는 안목" \
  output_pre.png

# Step 3 — nine dots + caption + author block
# (DRAW built in bash with explicit array indexing; see notes)
DOTS=("#3b82f6" "#06b6d4" "#10b981" "#84cc16" "#eab308" "#f97316" "#ef4444" "#ec4899" "#a855f7")
DRAW="stroke none"
START_X=520; SPACING=70; CY=1700; R=18
for i in 0 1 2 3 4 5 6 7 8; do
  cx=$((START_X + i*SPACING)); c=${DOTS[$i]}
  DRAW="$DRAW fill \"$c\" circle ${cx},${CY} ${cx},$((CY-R))"
done
magick output_pre.png -draw "$DRAW" \
  -font "$GOTHIC" -fill "#9aa5b8" -pointsize 32 \
    -gravity center -annotate +0+390 "9   ENVIRONMENTS   COMPARED" \
  \( -size 200x2 xc:"#e2e8f0" \) -gravity south -geometry +0+260 -composite \
  -font "$GOTHIC" -fill "#e2e8f0" -pointsize 56 \
    -gravity south -annotate +0+170 "Toby-AI" \
  -font "$GOTHIC" -fill "#9aa5b8" -pointsize 32 \
    -gravity south -annotate +0+110 "BOOK  WRITER  HARNESS" \
  cover.png
```

### Validation
- [x] 해상도 1600×2560 ✓
- [x] 한글 글리프 정상 렌더 ✓ (Apple SD Gothic Neo)
- [x] 썸네일 200×320 축소 시 제목 가독성 확보 (제목 168pt → 썸네일 환산 21pt)
- [x] 저자 표기 `Toby-AI` 명시 ✓
- [x] 클리셰 회피 ✓ (스톡 사진/그라데이션/뱀 그래픽 없음)

### Notes / 주의
- bash array index `${DOTS[0]}`이 zsh subshell에서 빈 값으로 평가되는 이슈가
  있어 dot 그리기 단계는 `bash -c` 래퍼 안에서 실행했다. 재생성 시 동일하게
  처리할 것.
- 이미지-gen MCP가 추가되면 위 영문 프롬프트로 한 번 돌려서 A/B 비교 권장.
  현재 ImageMagick 버전은 안전한 베이스라인.
