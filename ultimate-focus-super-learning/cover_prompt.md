# Cover Design — 시니어의 학습법

생성된 표지에 사용한 콘셉트, 프롬프트, 색상·폰트·도형 결정을 기록한다. 재생성·A/B 테스트 시 출발점.

## 책 정보

- **제목:** 시니어의 학습법
- **부제:** FIT, PACER, RAIL로 다시 짜는 집중과 학습의 운영체제
- **저자:** Toby — AI
- **언어:** 한국어
- **장르:** 에세이형 기술서 — 시스템적 사고 + 시니어 회고 톤
- **대상:** 5년+ 시니어 개발자

## 채택 콘셉트 — A안 (미니멀 타이포 + 6레이어 도식)

3안 중 A안을 채택. 이유:

1. 부제에 영문 약어(FIT/PACER/RAIL)가 들어있어 활자가 기능적으로 중요 → 타이포 우선
2. 책의 1~6장이 학습 운영체제의 6개 레이어를 분해하는 구조 → 6레이어 도식이 책의 핵심 구조를 그대로 시각화
3. 마지막 메시지가 메타인지(Metacognition) → 도식의 마지막 라인을 머스터드로 강조해 "메타인지가 모든 것을 떠받친다"는 메시지를 시각적으로 전달
4. Penguin Press / Stripe Press / NoStarch 톤의 에디토리얼 결을 유지

## 사용 도구

- **이미지 생성 MCP:** 사용 가능한 이미지 생성 MCP/외부 API 없음
- **외부 API (gpt-image-1, DALL-E):** API 키 미설정
- **ImageMagick:** 시스템 미설치 (`convert`, `magick` 둘 다 없음)
- **채택: Pillow (PIL)** — Python 기반, 시스템에 설치되어 있음. 폰트 + 도형 렌더링으로 미니멀 타이포 표지 구현에 충분.

스크립트: `_make_cover.py` (이 폴더)

## 프롬프트 (이미지 생성 API 사용 시 참고용 영문 프롬프트)

향후 API 기반으로 재생성하고 싶을 때 참고:

```
Editorial book cover, minimalist typography-driven design, 1600x2560 portrait.

Background: deep indigo (#181a3a), no gradient, flat solid.

Top: small caps tracked-out text "A LEARNING OPERATING SYSTEM" in warm mustard
(#d6b96a), centered, with a tiny mustard divider line below.

Center upper: large bold sans-serif Korean title "시니어의 / 학습법" in two
lines, warm off-white (#f1ece0), Apple SD Gothic Neo Bold or similar, ~200pt,
centered.

Below title: "FIT · PACER · RAIL" in mustard Helvetica/Inter Bold, then a
single Korean subtitle line "다시 짜는 집중과 학습의 운영체제" in muted
lavender-grey (#a09ebc).

Lower half: six thin horizontal lines stacked vertically (operating-system
layer metaphor). Each line has a single uppercase letter on the left
(F, E, R, S, A, M) and a small word on the right (Focus, Encoding,
Retrieval, Skill, AI, Metacognition). The bottom line (Metacognition) is
mustard and slightly thicker — emphasizing it as the foundation.

Bottom: small mustard divider, then "Toby — AI" in off-white, then tiny
tracked caps "FOR SENIOR ENGINEERS" in muted grey.

Style: Penguin Press / Stripe Press / NoStarch editorial. No illustrations,
no gradients, no stock photo. Pure typography + minimal geometric lines.
High contrast, calm and trustworthy mood.
```

## 디자인 결정 — 디테일

### 색상 팔레트

| 역할 | HEX | 용도 |
| --- | --- | --- |
| 배경 | `#181a3a` | 깊은 인디고 — 차분 + 신뢰 |
| 메인 활자 | `#f1ece0` | 따뜻한 오프화이트 — 인쇄책 종이 톤 |
| 강조 | `#d6b96a` | 머스터드 — 한 점 강조 (top label / FIT·PACER·RAIL / Metacognition 라인) |
| 부제·보조 | `#a09ebc` | 라벤더 그레이 — 부제, layer 단어 |

머스터드는 책 전체에서 **세 번**만 등장한다 (top label / 약어 / Metacognition 라인). 한 색을 의도적으로 적게 쓰는 것이 미니멀리즘의 핵심.

### 타이포그래피

- **한글 제목/부제:** Apple SD Gothic Neo (`/System/Library/Fonts/AppleSDGothicNeo.ttc`)
  - Bold (index=6): 대제목
  - Medium (index=4): 부제, 저자
- **라틴 활자:** Helvetica (`/System/Library/Fonts/Helvetica.ttc`)
  - Bold (index=2): FIT·PACER·RAIL, F/E/R/S/A/M, Toby — AI
  - Regular (index=0): Focus/Encoding/... layer 단어, 보조 캡션

크기 위계 (px):
- 대제목 200 → 약어 64 → 부제 한글 66 → 6레이어 라벨 56 → 저자 40 → 보조 캡션 28

### 6레이어 도식

- **위 → 아래로 누적:** Focus / Encoding / Retrieval / Skill / AI / Metacognition
- 각 라인은 폭 640px, 선 굵기 2px (얇은 선)
- 마지막 Metacognition 라인만 머스터드 + 4px 두께 → 시각적 무게중심
- 좌측에 1글자 라벨(F·E·R·S·A·M) — 약자가 책의 "운영체제 레이어"라는 메타포를 추상적으로 암시

### 책의 메시지가 표지에 어떻게 박혔는가

| 책의 핵심 메시지 | 표지에서의 시각화 |
| --- | --- |
| "내 학습 시스템을 리팩토링한다" | "A LEARNING OPERATING SYSTEM" 라벨 + 6레이어 스택 |
| "FIT/PACER/RAIL은 도구함" | 약어를 부제에 머스터드로 강조 |
| "메타인지가 모든 걸 떠받친다" | 6레이어 중 맨 아래 M(Metacognition) 라인을 머스터드 + 두꺼운 선으로 강조 |
| "차분하고 신뢰감 있는 톤" | 깊은 인디고 + 오프화이트 + 절제된 머스터드 한 점 |
| "에디토리얼 결" | Penguin/Stripe Press 풍 — 일러스트 0, 활자 + 가는 선만 |

## 검증 결과

- **해상도:** 1600 × 2560 (1.6:1, EPUB 권장)
- **파일 크기:** ~91 KB
- **포맷:** PNG, 8-bit RGB
- **썸네일 200×320 가독성:** "시니어의 학습법" 명확히 읽힘. "FIT · PACER · RAIL"도 또렷. F/E/R/S/A/M 1글자 라벨도 인식 가능 (Focus/Encoding 등 작은 영문 단어는 흐릿해지지만 의도된 그라데이션)
- **저자명 표기:** "Toby — AI" 하단에 명시 ✅
- **클리셰 회피:** 그라데이션 없음, 스톡 없음, AI/뇌 그래픽 없음, 자기계발 클리셰 없음 ✅

## 재생성·A/B 테스트 가이드

같은 콘셉트 안에서 다음을 변형해볼 수 있다:

1. **B안으로 전환:** 따뜻한 크림(`#f1ece0`) 배경 + 차콜(`#1a1a1a`) 활자, 6레이어 도식 제거, 활자만으로 무게중심
2. **C안으로 전환:** 6개 사각형 스택(현재는 가는 선) — 운영체제 스택 메타포를 더 직관화
3. **약어 변형:** `FIT · PACER · RAIL` → `FIT  PACER  RAIL` (점 제거, 더 미니멀)
4. **레이어 단어 한글화:** Focus/Encoding/... → 집중/부호화/... (한글 독자에게 더 친근, 단 영문 약어와의 시각적 통일감 손실)
5. **머스터드 → 다른 강조색:** 짙은 시안 `#5a8fa8` 또는 톤 다운된 코랄 `#c97b6a`
