# Cover Design Log

## Version 1 (2026-05-13)

- **Concept:** C — 타이포그래피 + 터미널 모티프
- **Tool:** ImageMagick 7.1.2 (한글 안정성을 위해 외부 이미지 모델 대신 타이포 합성)
- **Rationale:** 책의 핵심 모티프인 "코드가 회로가 된다"를 터미널 화면 메타포로 표현. 모노스페이스 ASCII 박스로 8비트 회로 다이어그램을 암시하면서, 굵은 한글 산세리프로 제목을 압도적으로 노출. 1980년대 8비트 시대 향수(검정 CRT 배경, 시안 라인, 앰버 액센트)와 모던 개발자 감성(미니멀 그리드, 깔끔한 타이포)을 동시에 잡는다.
- **Palette:**
  - Background: `#0a0e1a` (검정에 가까운 딥 네이비) → `#0d1b2a` (CRT 글로우 느낌으로 살짝 그라데이션)
  - Title: `#e0e1dd` (오프 화이트, CRT 인광)
  - Accent line / brackets: `#00d4ff` (터미널 시안)
  - Subtitle: `#5eead4` (민트-시안, 가독성용 중간 밝기)
  - Highlight `8비트` / `RISC` 강조 토큰: `#ffb627` (앰버 — 80s 모노크롬 디스플레이의 호박색)
  - Circuit ASCII art: `#1b4d6b` (어둡게 깔린 시안, 배경 텍스처)
- **Layout (1600×2560 portrait):**
  - Top 7%: 작은 시리얼 라벨 `> KOTLIN_CPU.kt — v1` (모노스페이스, 시안)
  - Upper third (y≈680): 시리즈 라인 `// 코드로 짓는` (얇은 시안)
  - Center-top (y≈900): 메인 제목 `CPU` 거대 산세리프 (앰버, 무거움)
  - Below title (y≈1180): 한글 제목 `코드로 짓는 CPU` (오프화이트, Apple SD Gothic Neo Heavy, ~180pt) — *재배치: CPU 글자 자체는 거대 영문, 한글이 보조로 들어가는 모호함을 피하기 위해 v1.1에서 단일 한글 제목으로 통합*
  - Mid (y≈1500): 시안 가로 라인 + 부제 `Kotlin으로 SAP-1에서 8비트 RISC까지`
  - Lower mid (y≈1800~2100): ASCII 회로 박스 (모노스페이스, 어두운 시안) — 8비트 레지스터/버스 느낌
  - Bottom (y≈2350): `Toby-AI` (시안)
  - Bottom right corner: `SAP-1 → RISC` 작은 모노스페이스 (앰버)
- **Prompt (사용 시 영문 모델용 백업):**
  ```
  A bold retro-techno book cover, portrait 1600x2560.
  Deep navy-black CRT background with subtle scanlines.
  Title "코드로 짓는 CPU" in massive heavy Korean sans-serif,
  off-white, centered upper-third. Subtitle "Kotlin으로 SAP-1에서
  8비트 RISC까지" in cyan-mint below a thin cyan rule. Faint
  ASCII-art circuit diagram (registers, bus lines) in dark cyan
  occupies the lower half as background texture. Amber accent tokens
  for "8비트" and corner annotation "SAP-1 → RISC". Tiny serial
  label "> KOTLIN_CPU.kt — v1" at top in cyan monospace.
  Author "Toby-AI" small at bottom. 80s terminal aesthetic, modern
  grid, no clichéd tech gradient, no stock circuit photography.
  ```
- **Result:** `cover.png` (1600×2560 PNG, ~866KB)
- **Notes:**
  - ImageMagick 7.1.2 `magick` 커맨드 사용
  - 한글 폰트: `/System/Library/Fonts/AppleSDGothicNeo.ttc` — `.ttc` face index 지정은 macOS IM에서 동작 안 함. 굵기는 `-stroke <같은색> -strokewidth 3~6`으로 보강
  - 모노스페이스: `/System/Library/Fonts/Menlo.ttc` (박스 드로잉 문자 ─│┌┐└┘╔╗╚╝═║▶▼ 안정 렌더)
  - Noto Sans KR variable 폰트는 IM에서 default Thin axis로 떨어져 사용 불가
  - Jalnan/잘난체는 너무 친근한 결로 기술서 톤과 안 맞아 제외

## 최종 재생성 커맨드 (참고용)

```bash
APPLE=/System/Library/Fonts/AppleSDGothicNeo.ttc
MENLO=/System/Library/Fonts/Menlo.ttc
OUT=./cover.png

# 1) Background: navy gradient + scanlines + soft vignette
magick -size 1600x2560 gradient:'#102236-#050912' /tmp/bg.png
magick -size 1600x4 xc:'#00000000' -fill '#0d2233aa' -draw 'line 0,3 1600,3' /tmp/tile.png
magick -size 1600x2560 tile:/tmp/tile.png /tmp/scan.png
magick -size 1600x2560 radial-gradient:'#00000000-#00000055' /tmp/vig.png
magick /tmp/bg.png /tmp/scan.png -composite /tmp/bg2.png
magick /tmp/bg2.png /tmp/vig.png -compose multiply -composite /tmp/bg3.png

# 2) ASCII circuit (transparent, dark cyan)
cat > /tmp/ascii.txt <<'EOF'
[ASCII art content - see cover_prompt.md history ]
EOF
magick -background none -fill '#3a6f8e' -font "$MENLO" -pointsize 22 \
  -interline-spacing 4 label:@/tmp/ascii.txt /tmp/ascii.png

# 3) Compose: bg + ASCII + typography
magick /tmp/bg3.png /tmp/ascii.png -geometry +532+1640 -composite /tmp/step1.png
magick /tmp/step1.png \
  -font "$MENLO" -pointsize 34 -fill '#00d4ff' \
    -gravity northwest -annotate +90+110 '> KOTLIN_CPU.kt' \
  -fill '#5eead4' -gravity northeast -annotate +90+115 'v1.0' \
  -pointsize 38 -gravity north -annotate +0+640 '// build_a_cpu_from_scratch' \
  -font "$APPLE" -pointsize 180 -fill '#f4f1de' -stroke '#f4f1de' -strokewidth 3 \
    -gravity north -annotate +0+760 '코드로 짓는' \
  -pointsize 380 -fill '#ffb627' -stroke '#ffb627' -strokewidth 6 \
    -gravity north -annotate +0+990 'CPU' \
  -fill '#00d4ff' -stroke '#00d4ff' -strokewidth 4 -draw 'line 350,1490 1250,1490' \
  -font "$APPLE" -pointsize 60 -fill '#a8dadc' -stroke none \
    -gravity north -annotate +0+1530 'Kotlin으로 SAP-1에서 8비트 RISC까지' \
  -font "$MENLO" -pointsize 32 -fill '#ffb627' \
    -gravity southeast -annotate +90+85 'SAP-1 → 8-bit RISC' \
  -fill '#5eead4' -gravity southwest -annotate +90+85 '[ build • test • boot ]' \
  -font "$APPLE" -pointsize 64 -fill '#00d4ff' -stroke '#00d4ff' -strokewidth 1 \
    -gravity south -annotate +0+155 'Toby-AI' \
  "$OUT"
```

## 검증 체크리스트

- [x] 해상도 1600×2560 (1.6:1 portrait)
- [x] 썸네일(320×512)로 축소해도 "코드로 짓는 CPU" 제목 읽힘
- [x] 부제 "Kotlin으로 SAP-1에서 8비트 RISC까지" 읽힘
- [x] 저자 "Toby-AI" 명시
- [x] 한글 폰트 깨짐 없음 (Apple SD Gothic Neo로 안정)
- [x] 클리셰 회피 (스톡 회로 사진 없음, 일반 기술 그라데이션 없음, AI 일러스트 인공물 없음)
- [x] 8비트 retro-techno + 모던 터미널 톤 양립
