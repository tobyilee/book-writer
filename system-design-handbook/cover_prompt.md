# Cover Design Log

책: **현장에서 살아남는 시스템 디자인**
부제: 작은 internal 시스템부터 글로벌 SaaS까지
저자: Toby-AI
대상 독자: 실무 백엔드 엔지니어 3~7년차

## Concepts Considered

| 안 | 설명 | 채택 여부 |
|---|------|----------|
| A | 미니멀리즘 — 흰 배경 + 시스템 다이어그램 메타포 + 네이비/빨강 | **채택** |
| B | 일러스트형 — 빌딩 블록 / 패턴 / 케이스 3층 일러스트 | 부분 차용 (3-기둥 섹션) |
| C | 타이포그래피 중심 — 제목 자체가 그래픽 | 부분 차용 (큰 한국어 제목 + 빨강 마침표) |

A안을 베이스로 두고, B의 "3-pillar" 구조를 mid-section에 흡수하고, C의 큰 한국어 타이포 + 빨강 마침표 시그니처를 가져왔다.

## 디자인 의도

- **흰 종이 정체성**: 인터뷰서가 즐겨 쓰는 짙은 그라데이션과 차별화. 실무자가 책장에 꽂아두고 매일 펼쳐보는 종이 책의 정수.
- **시스템 다이어그램 메타포**: 작은 네이비 박스 1개(internal 도구)에서 fan-out되어 마지막에 빨강 hot node(글로벌 SaaS의 risk / 결제 알람 / SPOF 신호)로 도착하는 구도. 책 부제의 "internal → 글로벌 SaaS"를 그대로 시각화.
- **빨강 accent의 함의**: 결제·alert·hot key 같은 시스템 디자인의 "위험" 신호. 책 전체에 단 두 점(제목 마침표 + 다이어그램 hot node + 저자 점)만 쓰여 진중함을 해치지 않는다.
- **3-pillar 섹션**: 빌딩 블록 → 패턴 → 케이스 스터디. 책의 목차 구조를 표지에서 미리 보여줘 독자가 "이 책의 뼈대"를 한눈에 파악하게 한다.
- **SCALE 축**: INTERNAL → PRODUCT → GLOBAL SAAS. 다이어그램이 단순 장식이 아니라 의미를 갖도록 가로축에 라벨링.

## Tool Used

**Python PIL (Pillow)** — ImageMagick이 시스템에 없어 PIL로 직접 도형·텍스트 합성. 폰트는 시스템 기본 `AppleSDGothicNeo.ttc` (한·영 통합 처리 — HelveticaNeue.ttc는 인덱스 매핑이 macOS 버전마다 달라 일부 글리프가 깨지는 문제가 있어 회피).

스크립트: `/tmp/generate_cover.py` (재현 가능, 산출물에 함께 포함하지는 않음 — 필요 시 이 prompt.md의 의도를 보고 재작성)

## 검증

- 해상도 1600 × 2560 ✓
- 한국어 제목 가독성 (썸네일 200×320 축소 시에도 또렷) ✓
- 저자 표기 "Toby-AI" 좌하단 ✓
- 클리셰 회피: 진부한 클라우드 아이콘 / 그라데이션 / 스톡 사진 0 ✓

## 재생성 시 가이드라인

다른 도구(이미지 생성 MCP / DALL-E 등)로 다시 만든다면 아래 프롬프트를 베이스로:

```
A minimalist Korean technical book cover, portrait 1600x2560, 5:8.
Background: warm off-white paper (#fbfaf7). Top edge: a thin red rule (#c83c32).
Layout (top to bottom):
  1. Tag line "SYSTEM DESIGN HANDBOOK" (top-left, small caps, deep navy).
  2. Korean title in two lines, bold modern sans-serif, deep navy (#162240):
     "현장에서 살아남는 / 시스템 디자인" — second line larger; end with a small
     red dot like a confident period.
  3. Korean subtitle smaller, navy-gray: "작은 internal 시스템부터 글로벌 SaaS까지".
     A short red underline below the subtitle.
  4. Three "pillar" cards in a row, each: large numeral (01 / 02 / 03) in navy,
     vertical red rule, English label in uppercase + Korean label below
     (빌딩 블록 / 패턴 / 케이스 스터디).
  5. Center: abstract system architecture diagram. Left side has a single solid
     navy box (representing "internal tools"). It fans out to the right through
     successive columns of more boxes (2, 3, 4, 5), connected by thin grey
     arrows. The rightmost column contains a single solid red box among
     navy-outlined boxes — the "hot node" representing global SaaS scale and
     risk. Below the diagram: a thin horizontal axis with ticks labeled
     INTERNAL — PRODUCT — GLOBAL SAAS in small grey caps.
  6. Footer: small Korean tagline "실무 백엔드 엔지니어를 위한 현장 가이드",
     then author "Toby-AI" with a tiny red dot beside it, right-aligned
     "2026 EDITION".
Style: editorial, calm, confident, no gradients, no cliché tech imagery,
no stock photo, no glow effects, no 3D, no cloud icons.
```

## Versions

| 버전 | 날짜 | 도구 | 비고 |
|------|------|------|------|
| v1 | 2026-05-17 | PIL (Apple SD Gothic Neo) | 초기 콘셉트 — 다이어그램만, 중간 비어 보임 |
| v2 | 2026-05-17 | PIL | 3-기둥 섹션 + SCALE 축 헤딩 추가 |
| v3 (final) | 2026-05-17 | PIL | 폰트 통일 (Helvetica 글리프 손실 문제 해결), `cover.png` 저장 |
