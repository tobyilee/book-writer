# Modern Java Bible — 표지 디자인 기록

## 콘셉트 (선택된 1안)

**"권위 있는 레퍼런스 + 11년의 진화 타임라인"**

- 미드나잇 블루 그래디언트(#0A1929 → #1B2A4E) 위에 자바 시그니처 골드(#F89820) 액센트
- 우상단 골드 글로우 — "Bible"의 무게값과 자바 정체성을 한 점으로 압축
- 좌하단 청색 글로우 — 시각적 균형
- 좌상단 모노스페이스 타임라인 `8 → 11 → 17 → 21 → 25` — 책이 다루는 시간 범위를 작게 명시
- 하단 모듈 그래프(노드 7개 + 엣지) — 모듈 시스템 + 그래프 구조의 추상화, 골드로 통일
- 키워드 라인 `lambda records sealed virtual threads pattern matching` — 책의 핵심 기능을 모노스페이스로 나열
- "BIBLE"을 골드로 가장 크게 — 책의 두께값/권위 강조
- 부제 윗줄에 짧은 골드 디바이더 — 클래식한 레퍼런스 책 느낌

## 사용 폰트

- 제목 (MODERN JAVA BIBLE): Helvetica Neue Heavy/Black (900 weight)
- 부제·키워드·타임라인: Menlo (모노스페이스)
- 저자명: Helvetica Neue Medium (500 weight)

## 색상 팔레트

| 용도 | HEX |
|---|---|
| 배경 그래디언트 상단 | #0A1929 |
| 배경 그래디언트 하단 | #1B2A4E |
| 자바 골드 (BIBLE, 디바이더, 그래프) | #F89820 |
| 푸른 글로우 | #3D5FA8 |
| 메인 흰색 (MODERN JAVA) | #FFFFFF |
| 저자명 | #F2F5FB |
| 부제 | #C8D2E8 |
| 키워드 | #6E84B5 |
| 타임라인 (작은 모노) | #7589B8 |

## 검토하지 않은 대안 콘셉트 (A/B 재생성용)

### 2안 — 미니멀 타이포그래피
배경은 단일 그래파이트 그레이(#1E2530), 글로우·그래프 모두 제거. 제목만 거대한 골드+화이트 타이포로. 부제 한 줄. "성경" 같은 절제미.

### 3안 — 람다 모티프
중앙에 거대한 반투명 λ(람다) 심볼을 배경 워터마크처럼 배치. 그 위에 제목. 함수형 패러다임의 도입을 강조하고 싶을 때.

## 재생성 명령 (요약)

```bash
TITLE_FONT="/System/Library/Fonts/HelveticaNeue.ttc"
MONO_FONT="/System/Library/Fonts/Menlo.ttc"

# 1. 그래디언트 배경
magick -size 1600x2560 gradient:'#0A1929-#1B2A4E' bg.png

# 2. 글로우 레이어 (radial-gradient, 알파 곱셈)
magick -size 1200x1200 radial-gradient:'#F89820'-'#F8982000' \
  -channel A -evaluate multiply 0.7 +channel glow_gold.png
magick -size 1400x1400 radial-gradient:'#3D5FA8'-'#3D5FA800' \
  -channel A -evaluate multiply 0.65 +channel glow_blue.png

# 3. 모듈 그래프 (노드 + 엣지, 알파 45%)
# (cover_prompt.md 본문에는 생략 — cover.png 만드는 스크립트 참고)

# 4. 합성 + 타이포그래피
# (Helvetica Neue 900으로 제목, Menlo로 모노, 골드 디바이더, 저자명 하단 중앙)
```

## AI 이미지 생성 도구용 영문 프롬프트 (이미지-gen MCP 가용 시)

> A high-end book cover, portrait 1600x2560, deep midnight-blue gradient background (#0A1929 to #1B2A4E) with a soft warm-gold radial glow in the upper right and a subtle blue radial glow in the lower left. Bold sans-serif typography stacked center: "MODERN" and "JAVA" in heavy white Helvetica, then "BIBLE" massive in Java orange (#F89820). Below, a thin gold horizontal divider, then a monospaced subtitle "Java 8 -> 25, And Beyond" in light lavender. Upper-left corner shows a small monospaced timeline "8 -> 11 -> 17 -> 21 -> 25". Lower third features an abstract module graph: seven gold dots connected by thin lines suggesting a node graph. Bottom center: author "Toby-AI" in medium-weight Helvetica. Refined, authoritative, classic-meets-modern reference book aesthetic. No coffee cups, no clichés. Clean typography, minimal but dense.

## 저자 표기

매니페스트의 `author: "Toby-AI"`를 그대로 사용. 표지 하단 중앙에 노출.
