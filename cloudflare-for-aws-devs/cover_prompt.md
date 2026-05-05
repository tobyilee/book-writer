# Cover Design Notes — 『AWS 개발자를 위한 Cloudflare 본격 활용 가이드』

## 메타
- 슬러그: `cloudflare-for-aws-devs`
- 출력: `cover.png` (1600 × 2560, PNG, RGBA)
- 백업: `cover_v1.png` (1차 시안)
- 저자: Toby-AI
- 빌드 방식: ImageMagick 7.1.2 + Python(SVG 네트워크 생성) 폴백 (image-gen MCP 미가용)

## 선정 컨셉
**"하나의 중앙 리전이 아닌, 흩뿌려진 빛의 네트워크"**

모티프 1번(글로벌 네트워크 그래프)과 3번(edge의 추상화)을 융합. 지구 위에 흩어진 PoP들을 노드와 얇은 연결선으로 표현하되, 격자(grid) 형태가 아닌 유기적 산포로 그려서 AWS의 사각 컨테이너 격자 모델과 시각적으로 대비된다. 일부 노드만 오렌지로 빛나 PoP 캐시 hit를 연상시키고, 나머지는 차가운 청회색 배경 노드로 가라앉혀 깊이감을 만든다.

## 색상 팔레트 (다크 모드)
- 배경: `#101A2E → #060912` 세로 그라디언트 (AWS 다크 네이비 계열을 더 진하게 끌어내림)
- 중앙 글로우: `#1A2A48` 부드러운 방사형 라이트
- 본문 텍스트: `#E8ECF3` (오프화이트)
- 강조 타이틀: `#FFFFFF` (Cloudflare 단어만 순백)
- 액센트: `#F38020` (Cloudflare 오렌지) — 부제 키 라인 + PoP 노드 + 구분선
- 보조: `#A8B8D2` (서브타이틀, 차분한 청회색)
- PoP 노드 코어: `#FFC48C` (오렌지 그라디언트의 밝은 끝)

## 타이포그래피
- "AWS 개발자를 위한" — Pretendard Bold 100pt
- "Cloudflare" — Pretendard Black 200pt (히어로)
- "본격 활용 가이드" — Pretendard Bold 132pt, Cloudflare Orange
- "EDGE · FIRST · PLATFORM" — Pretendard Medium 38pt, 오렌지 / 단락 위 짧은 액센트 바
- 부제 3줄 — Pretendard Regular 46pt, `#A8B8D2`
- 저자 "Toby-AI" — Pretendard Bold 50pt 하단 중앙
- 보조 캡션 "AI-AUTHORED · 2026" — Pretendard Light 30pt
- 우상단 마이크로 카피 "330+ PoPs · 120+ countries" — 28pt + 작은 오렌지 점 3개 (분산된 PoP를 시각화)

## 구도
```
┌─────────────────────────────────────┐
│                       330+ PoPs ⋯   │  ← 우상단 마이크로 캡션
│ ── EDGE · FIRST · PLATFORM          │  ← 오렌지 액센트 바 + 태그
│ AWS 개발자를 위한                    │  ← 1단계 (오프화이트)
│ Cloudflare                          │  ← 히어로 단어 (순백, 가장 큼)
│ 본격 활용 가이드                     │  ← 2단계 (오렌지)
│ ──                                  │  ← 짧은 오렌지 구분선
│ Workers · D1 · R2 부터              │  ← 부제 3줄
│ OpenNext · AI Gateway 까지,         │
│ 멘탈 모델을 다시 그리는 길잡이       │
│                                     │
│   · ·  · ·  ●  · · · ·  ●           │  ← 글로벌 네트워크 그래프
│  · ●·  · · · ●  · · ●  ·            │     (~85 노드, ~104 엣지,
│   ·  · · ●  · ·   · ●               │      18% 오렌지 PoP 노드)
│                                     │
│              Toby-AI                │
│         AI-AUTHORED · 2026          │
└─────────────────────────────────────┘
```

상단 1/3은 텍스트 위계, 하단 2/3는 시각 모티프. 좌측 정렬 타이포(220px 좌측 마진)와 중앙 정렬 푸터의 대비로 정적이면서도 균형감을 만든다.

## 영문 image-gen 프롬프트 (외부 모델용 — 향후 재생성 대비)

```
Book cover, vertical 1600x2560, dark navy gradient background (#101A2E to
#060912) with a subtle warm radial glow at lower-center. The lower two-thirds
shows an abstract global edge network: about 85 small dots scattered organically
across a wide horizontal band, connected by thin faint steel-blue lines forming
a sparse mesh — NOT a grid, NOT a globe outline, just constellation-like
distribution suggesting points of presence around the planet. About 18% of the
dots glow warm orange (#F38020) with a soft halo, like cache hits lighting up
across continents; the rest are cool muted blue-gray (#a4b6d2). No country
borders, no map outlines, no logos.

Upper third reserved for typography (left-aligned):
  - small orange tag "EDGE · FIRST · PLATFORM" preceded by a short orange bar
  - Korean title in three weights: "AWS 개발자를 위한" (off-white, bold),
    "Cloudflare" (massive ultra-black white), "본격 활용 가이드" (orange bold)
  - thin orange divider, then a 3-line subtitle in cool gray:
    "Workers · D1 · R2 부터 / OpenNext · AI Gateway 까지, /
     멘탈 모델을 다시 그리는 길잡이"

Bottom-center: author "Toby-AI" in white bold, with a fine-print
"AI-AUTHORED · 2026" beneath in muted gray.

Top-right corner: three small orange dots followed by tiny caption
"330+ PoPs · 120+ countries".

Style: technical-publishing, calm, serious, no marketing flair, no glossy
reflections, no 3D, no AWS/Cloudflare logos. Inspired by O'Reilly + A Book Apart
+ minimal Swiss design, but with the Cloudflare orange as the only warm note
inside an otherwise cold technical palette.
```

## 재생성 시 주의
- ImageMagick 폴백은 한국어 폰트(Pretendard) 경로가 `/Users/tobylee/Library/Fonts/`에 있어야 한다.
- 네트워크 SVG는 시드 11 (Python `random.seed(11)`)로 재현 가능. 다른 분포 원하면 시드 변경.
- AWS / Cloudflare 로고나 지도 외곽선은 라이선스·상표 이슈로 절대 삽입 금지.
