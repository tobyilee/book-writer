# Cover Design Log

책: `@Transactional이 없는 세상 — Spring 사고로 FastAPI를 짓는 법`
저자: Toby-AI
산출: `fastapi-for-spring-developers/cover.png` (1600 × 2560, PNG)

## 콘셉트 3안 (검토)

- **A. 미니멀리즘 + 소거 모티프 (선택됨)** — 어두운 잉크 블루 캔버스에 제목이 박혀 있고, 시안 액센트 한 줄이 `@Transactional` 글자를 정확히 관통해 "없음"의 부정을 시각화. 기술서 진중함 + 도발 양립.
- **B. 일러스트형 (끊긴 그래프)** — 끊어진 노드 다이어그램으로 "사라진 자리"를 표현. 정조는 맞지만 테크 일러스트 클리셰 위험 + 썸네일 약함.
- **C. 타이포그래피 중심 (제목 풀화면)** — 강력하지만 도발이 과해 진중함 손상 우려.

**선택 사유:** Java/Spring 경력 백엔드 독자에게 책의 정조(상보·진중·전환)를 한 번에 전달하려면 도발(`@Transactional` 위 시안 라인)을 한 곳에만 응축하고 나머지는 절제하는 게 가장 강하다. 기술서 톤과 어울리고, 200×320 썸네일 크기에서도 제목 두 줄이 또렷이 읽힌다.

## 시각 컨셉 한 단락

짙은 잉크 블루 배경(`#0E1424` → `#070A14` 수직 그러데이션) 위에 흰색 한·영 혼용 타이포로 제목을 2단 조판한다. 1행 `@Transactional`은 라틴 자형 그대로 두고, 시안 액센트 라인(`#00E5FF`, 두께 14px)이 글자 가운데를 정확히 관통해 가짜 strikethrough를 만든다 — 이게 "없는 세상"의 시각적 동의어다. 2행 한글 `이 없는 세상`이 자연스럽게 이어지면서 라틴-한글 위계가 형성된다. 상단에는 작은 라벨 `FOR SPRING DEVELOPERS`(자간 12px, 회색)로 독자 대상을 즉시 명시하고, 부제 `Spring 사고로 FastAPI를 짓는 법` 아래 짧은 시안 인디케이터 바를 둔다. 하단에 저자 `Toby-AI`, 그 아래 작은 회색 라인으로 `BOOK WRITER HARNESS · v1.2`와 `2026` 메타. 외곽에 얇은 회청색 프레임(`#1F2A40`) + 상하 1/4 지점에 절제된 디바이더 라인 두 줄 — 책의 *짓는다·구조* 정조를 미세하게 강화한다.

## Version 1 (2026-05-16)

- **Concept:** A (미니멀리즘 + 소거 모티프)
- **Tool:** ImageMagick 7.1.2 (외부 이미지 생성 MCP 미연결 → 폴백)
- **폰트:** `/System/Library/Fonts/AppleSDGothicNeo.ttc` (한·영 모두 처리)
- **팔레트:**
  - 배경: `#0E1424` → `#070A14` (수직 그러데이션, 짙은 잉크 블루)
  - 본문 흰색: `#FFFFFF`
  - 부제 밝은 회색: `#C8D2E8`
  - 라벨 회색: `#8892A8`
  - 메타 회색: `#6B7388`
  - 프레임/디바이더: `#1F2A40` / `#1A2236`
  - 액센트(취소선·인디케이터 바): `#00E5FF` (시안)

### 영문 프롬프트 (외부 모델 재생성 시 사용)

```
A minimalist book cover, portrait 1600x2560.
Background: deep ink blue (#0E1424 to #070A14 vertical gradient),
near-black with a faint cooler band in the upper third.
Centered-left composition.

Top of cover: small label "FOR SPRING DEVELOPERS" in light grey,
wide letter-spacing, modern geometric sans-serif.

Main title set in two lines, large bold sans-serif, pure white:
  Line 1: "@Transactional"  (Latin glyphs, kept intact)
  Line 2: "이 없는 세상"  (Korean glyphs)
A single thick cyan stroke (#00E5FF, ~14px) cuts horizontally
through the middle of "@Transactional" — a strikethrough that
visualizes the word "없는" (absent / removed). The stroke must
pass through the x-height of the Latin word, not under it.

Beneath the title block, subtitle in light grey:
  "Spring 사고로 FastAPI를 짓는 법"
Followed by a short cyan indicator bar (#00E5FF, ~100x8 px).

Lower-left: author "Toby-AI" in clean white sans-serif.
Below author, smaller grey caps line: "BOOK WRITER HARNESS · v1.2".
Lower-right: year "2026" in the same small grey caps.

Subtle decorative scaffold:
- A thin (2px) deep blue-grey rectangle frame (#1F2A40) inset ~80px.
- Two faint horizontal divider lines (#1A2236) at one-quarter and
  three-quarter heights, splitting the canvas into thirds without
  drawing attention.

Mood: contemplative, confident, technical-but-human. The page
feels engineered, not decorated. No stock photography, no cliché
tech gradients, no Spring/Python logos, no code screenshots,
no neon glow effects. Editorial, restrained, sharp.
```

### 실행 결과

- 해상도 1600×2560 ✓
- 썸네일 200×320 축소 시 제목 두 줄 모두 가독 ✓
- 저자 표기 이미지 내 존재 (`Toby-AI`) ✓
- 시안 액센트가 `@Transactional`을 정확히 관통 — "없는"의 시각적 동의어 성립 ✓
- 테크 클리셰(스톡 사진·기본 그라데이션·로고) 회피 ✓

### 시행착오 (참고용)

- **v1a (폐기):** strikethrough 라인이 글자 아래쪽(밑줄 위치)에 그려져 "소거"가 아니라 "강조 밑줄"로 읽힘 → y 좌표를 +30px 위로 끌어올려 글자 x-height 중앙을 관통하도록 보정.
- **v1b (폐기):** 액센트 라인 그리기 전에 fill/stroke 색이 시안으로 stick되어 부제·저자가 의도치 않게 시안색으로 렌더링됨 → 드로잉 순서 재배열 (텍스트 먼저, 액센트는 마지막) + 액센트 직후 `-stroke none` 명시.

## 재생성 가이드

- **콘셉트는 유지 + 톤만 따뜻하게:** 배경을 짙은 차콜(`#1A1614`)로, 액센트를 호박색(`#FFB300`)으로 바꾸면 같은 구조에서 보다 부드러운 인상.
- **콘셉트 변경 요청 시:** 위 3안 검토부터 다시 시작 — B(끊긴 그래프)나 C(타이포 풀화면)로 전환.
- **이미지 생성 MCP/API 연결 후 재생성:** 위 영문 프롬프트를 그대로 투입. 결과 비교 후 더 강한 안을 `cover.png`로 채택, 이전 안은 `cover_v1.png`로 백업.
