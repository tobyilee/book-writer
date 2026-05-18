# Cover Design Log — capability-overhang

## 책 정보
- 제목: AI의 숨은 능력 — 우리가 아직 꺼내지 못한 90%
- 저자: Toby-AI
- 슬러그: capability-overhang
- 장르: 에세이형 기술·사회 비평서
- 분위기 키워드: 잠재력 / 빙산 / 숨겨진 능력 / 격차 / 가능성. 차분·사색적, 한낮의 응시.

## 검토한 콘셉트 3안

### A — 빙산 비유 (선택)
수면 위 작은 일부분(10%) + 수면 아래 거대한 음영(90%). 제목 주제와 직관적으로 1:1 매핑.
강점: 직관성, 메타포 명료, 썸네일에서도 형태 인지.
약점: 흔히 본 비유.

### B — 추상적 격차
다층 평면(모델/사람/도구/조직/평가) 사이의 간극을 색면으로 표현.
강점: 신선함, 본문 5-layer overhang 모형과 직결.
약점: 추상도가 높아 표지만 봐서는 책 주제가 명확히 안 떠오를 위험.

### C — 윤곽선의 미완성
완성된 노트북/도구 + 옆에 미완성 윤곽선.
강점: "우리가 아직 꺼내지 못한"의 직접 시각화.
약점: 일러스트 정밀도가 필요해 ImageMagick 폴백으로는 품질 보장 어려움.

→ **A 선택**. 직관성과 ImageMagick으로 안정적으로 표현 가능한 형태라는 점.

## Version 1 (2026-05-18)
- 콘셉트: A (빙산 비유 + 미니멀 타이포)
- 도구: ImageMagick 7.1.2 (`/opt/homebrew/bin/magick`)
- 폰트: Pretendard Bold / Light (`~/Library/Fonts/`)
- 결과: `cover.png` (1600×2560, 225KB)
- 백업: `cover_v1.png` (텍스트 정렬 시도 1차본)

### 시각 컨셉
- **상단(0~1024px)**: 한낮의 하늘 그라데이션 `#eef4f7 → #a8c8d8` — 밝고 사색적
- **수면선(y=1020~1042)**: 흰색 광선 + 옅은 음영 띠로 명확한 분단
- **하단(1024~2560px)**: 깊어지는 청록 `#3d6878 → #0a1e28` — 깊이·미지
- **빙산 위쪽**: 화면 중앙 약간 왼쪽, 작은 사다리꼴 (폭 230px = 캔버스의 14%). 흰색 + 그림자
- **빙산 아래쪽**: 거대한 비대칭 다각형 (폭 ~1040px = 캔버스의 65%). 청록 반투명 음영 + 더 진한 음영으로 입체감
- **타이포**: 제목 140pt Bold, 부제 56pt Light, 저자 54pt Bold, 푸터 28pt Light

### 색상 팔레트
| 역할 | 색상 |
|-----|-----|
| 하늘 상단 | `#eef4f7` |
| 하늘 하단 | `#a8c8d8` |
| 수면선 | `#ffffff` 85% |
| 수면 직하 | `#3d6878` |
| 심해 | `#0a1e28` |
| 빙산 상부 | `#fafcfd` / `#e8f0f4` / `#d8e6ed` |
| 빙산 하부 | `rgba(20,55,75,0.62)` / `rgba(8,25,38,0.45)` |
| 제목 텍스트 | `#0a1e28` |
| 부제 텍스트 | `#1a3445` |
| 저자 텍스트 | `#f0f6f9` |

### 생성 명령 (재현용)
```bash
PRETENDARD_BOLD="$HOME/Library/Fonts/Pretendard-Bold.otf"
PRETENDARD_LIGHT="$HOME/Library/Fonts/Pretendard-Light.otf"

# 배경 그라데이션 (위/아래 결합)
magick -size 1600x1024 gradient:'#eef4f7-#a8c8d8' /tmp/cover_top.png
magick -size 1600x1536 gradient:'#3d6878-#0a1e28' /tmp/cover_bottom.png
magick /tmp/cover_top.png /tmp/cover_bottom.png -append /tmp/cover_bg.png

# 수면선 + 빙산 도형
magick /tmp/cover_bg.png \
  -fill 'rgba(255,255,255,0.85)' -draw "rectangle 0,1020 1600,1024" \
  -fill 'rgba(255,255,255,0.18)' -draw "rectangle 0,1024 1600,1042" \
  -fill 'rgba(10,30,42,0.15)' -draw "rectangle 0,1042 1600,1080" \
  -fill '#fafcfd' -draw "polygon 700,830 870,830 920,1024 660,1024" \
  -fill '#d8e6ed' -draw "polygon 870,830 920,1024 870,920" \
  -fill '#e8f0f4' -draw "polygon 700,830 660,1024 705,920" \
  -fill 'rgba(20,55,75,0.62)' -draw "polygon 660,1024 920,1024 1180,1280 1330,1620 1260,2000 1000,2220 620,2220 360,2000 290,1620 440,1280" \
  -fill 'rgba(8,25,38,0.45)' -draw "polygon 920,1024 1180,1280 1330,1620 1260,2000 1080,1700 980,1380" \
  -fill 'rgba(255,255,255,0.06)' -draw "polygon 660,1024 920,1024 880,1200 720,1180" \
  /tmp/cover_iceberg.png

# 텍스트 라벨을 개별 PNG로 렌더 (한글 + gravity 안정성)
magick -background none -fill '#0a1e28' -font "$PRETENDARD_BOLD" -pointsize 140 \
  label:"AI의 숨은 능력" /tmp/title.png
magick -background none -fill '#1a3445' -font "$PRETENDARD_LIGHT" -pointsize 56 \
  label:"— 우리가 아직 꺼내지 못한 90%" /tmp/subtitle.png
magick -background none -fill '#f0f6f9' -font "$PRETENDARD_BOLD" -pointsize 54 \
  label:"Toby-AI" /tmp/author.png
magick -background none -fill 'rgba(240,246,249,0.65)' -font "$PRETENDARD_LIGHT" -pointsize 28 \
  label:"Book Writer Harness" /tmp/footer.png

# 최종 합성 (절대 좌표)
magick /tmp/cover_iceberg.png \
  /tmp/title.png    -gravity North -geometry +0+200  -composite \
  /tmp/subtitle.png -gravity North -geometry +0+400  -composite \
  /tmp/author.png   -gravity North -geometry +0+2370 -composite \
  /tmp/footer.png   -gravity North -geometry +0+2450 -composite \
  cover.png
```

### 영문 프롬프트 (외부 이미지 생성 API 사용 시 참고용)
```
A minimalist book cover in portrait format (1600x2560).

Composition: a clean horizontal waterline divides the canvas at 40%.
Above the waterline: a calm, light daylight sky gradient (#eef4f7 → #a8c8d8).
Below: deepening teal water (#3d6878 → #0a1e28).

A small iceberg tip — soft white with subtle facets — peaks slightly above
the waterline at the center, occupying ~14% of canvas width.
Below, a massive, asymmetric submerged iceberg silhouette in translucent
deep teal, occupying ~65% of canvas width and extending down to ~85% of the
canvas height. The submerged mass has subtle internal shading suggesting volume.

Title "AI의 숨은 능력" in bold modern sans-serif (Pretendard Bold) at the top
third, color #0a1e28, large and confident.
Subtitle "— 우리가 아직 꺼내지 못한 90%" in light weight just below,
color #1a3445.
Author "Toby-AI" in light bold at the bottom, color #f0f6f9.

Mood: contemplative, serene, with quiet tension. Editorial. No stock photo
aesthetic. No generic tech gradient. No glow effects. No 3D rendering.
```

### 검증
- [x] 해상도 1600×2560
- [x] 썸네일(200×320) 축소 시 "AI의 숨은 능력" 제목 명확히 읽힘
- [x] 저자 표기 `Toby-AI` 존재 (하단)
- [x] 클리셰 회피 (기본 그라데이션 아닌 톤 곡선, 스톡사진 없음)
- [x] 주제 메타포(빙산 10% / 90%)와 책 주제 직접 연결

### Notes
- 한글 폰트 + ImageMagick `-gravity South`/`-annotate` 조합이 의도와 다르게 텍스트를 캔버스 중앙에 그리는 현상이 발견됨. 텍스트를 `label:`로 먼저 PNG로 렌더한 뒤 `-composite`로 합성하니 절대 좌표 배치가 안정적이었음. 한글 표지 재생성 시 동일 패턴 권장.
- 다음 버전 후보(필요 시):
  - 빙산을 화면 우측 또는 좌측으로 약간 더 오프셋해서 비대칭성 강화
  - 수면 위에 옅은 안개/햇살 광선 추가로 한낮 분위기 강화
  - 빙산 아래쪽 음영을 더 세분화하여 5-layer(모델/사람/도구/조직/평가) 암시
