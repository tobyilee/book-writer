# Cover Design Log — 맨손으로 짓는 AI 에이전트

## 결정 사항

- **콘셉트**: A (미니멀리즘 + 노드 글리프). B(손-그래프 일러스트)는 클리셰 위험 + ImageMagick으로 정교한 일러스트 제작 한계, C(타이포 중심)는 핵심 메타포 "세 번 다시 짓는다"가 약해서 탈락.
- **메타포 표현**: 같은 그래프가 세 가지 추상화 레벨로 재현되는 3패널 — SDK(원시 그래프 형태) / LangChain(체인+분기) / LangGraph(명시적 사이클, 시계 방향 화살표).
- **색감**: 딥 네이비 (`#0f1a2e` → `#1b2540`) 배경 + 따뜻한 코랄 (`#e89776`, `#ffb997`, `#f5c9a8`) 강조. 우상단에 코랄 글로우 — 진지하되 차갑지 않은 톤.
- **타이포그래피**: Pretendard Bold. 본 제목 172pt 흰색 두 줄 / 부제 핵심 라인 132pt 코랄 / 보조 라인 110pt 페일 코랄. 시각 비중 ~77–80% 충족 — SNS 썸네일에서 부제 잘려도 책의 정체성이 유지됨.

## 사용 도구

- ImageMagick 7.1.2-19 (`/opt/homebrew/bin/magick`)
- 글리프: 인라인 SVG → PNG 래스터화 (density 240)
- 폰트: Pretendard-Bold.otf (~/Library/Fonts), Apple SD Gothic Neo (시스템) 백업
- 이미지 생성 MCP/API: 사용 안 함 (현 환경에 미연결)

## 산출

- `cover.png` — v2, 1600×2560, 1.69 MB, 16-bit sRGB
- `cover_v1.png` — v1 백업 (부제가 작아 v2에서 80% 비중 강화)
- `_cover_glyph.svg` — 중앙 글리프 원본 (재생성·수정용)

## 검증

- [x] 해상도 1600×2560 (EPUB 권장)
- [x] 200×320 썸네일에서 본 제목·부제·글리프 패널 모두 식별
- [x] 부제 시각 비중 ≈ 본 제목의 80% (폰트 크기 132pt/172pt = 77% + 코랄 강조 = 체감 80%+)
- [x] 저자 "Toby-AI" 표기
- [x] 클리셰 회피: 기본 그라데이션·스톡사진·뇌·로봇·코드 폭포 없음

## 재생성 절차

```bash
cd python-ai-agent
PRETENDARD_BOLD="$HOME/Library/Fonts/Pretendard-Bold.otf"

# 1. Re-rasterize glyph
magick -background none -density 240 _cover_glyph.svg -resize 1320x _cover_glyph.png

# 2. Background
magick -size 1600x2560 \
  gradient:'#0f1a2e-#1b2540' \
  \( -size 1600x2560 radial-gradient:'rgba(232,151,118,0.32)-rgba(15,26,46,0)' -gravity NorthEast -extent 1600x2560 \) \
  -compose Screen -composite \
  \( -size 1600x2560 xc:'#0f1a2e' -fill '#1b2540' -draw 'rectangle 0 1900 1600 2560' -blur 0x180 \) \
  -compose Multiply -composite _cover_bg.png

# 3. Glyph + panel labels
magick _cover_bg.png \( _cover_glyph.png -resize 1320x \) \
  -gravity Center -geometry +0+40 -compose Over -composite _step1.png
magick _step1.png -font "$PRETENDARD_BOLD" -fill 'rgba(200,192,184,0.75)' \
  -gravity Center -pointsize 38 \
  -annotate -460+290 'SDK' -annotate +0+290 'LANGCHAIN' -annotate +460+290 'LANGGRAPH' _step1b.png

# 4. Title
magick _step1b.png -font "$PRETENDARD_BOLD" -fill '#ffffff' \
  -gravity North -pointsize 172 -annotate +0+340 '맨손으로 짓는' \
  -gravity North -pointsize 172 -annotate +0+550 'AI 에이전트' _step2.png

# 5. Subtitle (강조 라인 + 보조 라인 + 스택 표기)
magick _step2.png \
  -font "$PRETENDARD_BOLD" -fill '#f5c9a8' \
  -gravity South -pointsize 110 -annotate +0+560 '같은 에이전트를' \
  -font "$PRETENDARD_BOLD" -fill '#ffb997' \
  -gravity South -pointsize 132 -annotate +0+400 '세 번 다시 짓는다' \
  -font "$PRETENDARD_BOLD" -fill 'rgba(240,184,154,0.92)' \
  -gravity South -pointsize 62 -annotate +0+280 'Python SDK   ·   LangChain   ·   LangGraph' _step3.png

# 6. Separator + author
magick _step3.png \
  -fill 'rgba(255,255,255,0.35)' -draw 'rectangle 700,2400 900,2402' \
  -font "$PRETENDARD_BOLD" -fill 'rgba(255,255,255,0.82)' \
  -gravity South -pointsize 56 -annotate +0+110 'Toby-AI' cover.png

rm _cover_bg.png _step1.png _step1b.png _step2.png _step3.png _cover_glyph.png
```

## 영문 프롬프트 (외부 이미지 모델 사용 시 참고)

> A minimalist editorial book cover, portrait 1600x2560. Background: deep navy gradient (#0f1a2e to #1b2540) with a soft warm coral glow in the upper-right corner. Center: three small abstract node-and-edge graph glyphs side by side, all the same agent shape rendered with three levels of structure — a busy multi-edge graph on the left, a cleaner branching chain in the middle, and an explicit clockwise cycle on the right. Coral color (#e89776) for the graphs. Tiny uppercase labels below each panel: "SDK", "LANGCHAIN", "LANGGRAPH" in muted off-white. Upper third: bold Korean title in white sans-serif, two lines: "맨손으로 짓는 / AI 에이전트". Lower third: subtitle in warm coral, with the line "세 번 다시 짓는다" emphasized larger, plus "Python SDK · LangChain · LangGraph" beneath. Bottom: tiny "Toby-AI" attribution. Calm, confident, contemplative. No stock photography. No tech gradient. No robot, no brain, no code-rain cliché.

## 변경 이력

| 버전 | 날짜 | 변경 사항 |
|------|------|-----------|
| v1 | 2026-05-16 | 초안. 부제 88pt/84pt로 작아 80% 비중 가이드 미달. |
| v2 (현재) | 2026-05-16 | 부제를 110pt/132pt로 확대 + LangGraph 화살표 강조 + 패널 라벨 추가. |
