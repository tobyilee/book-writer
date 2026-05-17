# Cover Design Brief — 바이브 너머의 엔지니어

## Final Concept (Selected)

**Concept A — "경계선 너머의 한 줄"**

타이포그래피 + 미세 텍스처 기반의 차분한 표지. 화려한 일러스트나 메탈릭/네온 효과를 배제하고, *읽지 않은 코드 한 줄*과 *너머의 경계선* 두 모티프를 결합한다.

### 시각 요소

- **배경:** 깊은 차콜-남색 수직 그라데이션 (`#0E1420` → `#1A2238`). 종이 입자 같은 미세 노이즈 추가.
- **상단 1/3 — "바이브" 영역:** 흐릿한 영문 의사 코드 라인 한 줄 (반투명, 낮은 채도). 독자가 "있긴 한데 정확히 안 읽힘"을 느낄 정도. AI가 짠 코드의 메타포.
- **수평 경계선:** 화면 중앙에 가는 흐린 청동(`#C9A86A`) 선 — "너머"로 가는 경계. 끊어진 점선이 아니라 정직한 단색 선 1px.
- **중앙 (선 아래) — 메인 제목:** "바이브 너머의 엔지니어" (AppleMyungjo, 명조). 두 줄: "바이브 너머의" / "엔지니어". 화이트(`#F2EFE9` warm white). 큰 사이즈, 자간 약간 조임.
- **부제:** "Agentic Coding 시대, 무엇을 위임하고 / 무엇을 끝까지 알아야 하는가" — Apple SD Gothic Neo Light, 회색(`#9AA3B2`). 두 줄.
- **영문 라인 (부제 보조):** "Beyond the Vibe — An Engineer's Stance" — 작게, Apple SD Gothic Neo, 청동(`#C9A86A`).
- **하단:** 저자 `Toby-AI` + 작은 마크. 회색(`#7A8290`).

### 톤 가이드

- 가볍지 않다. 무게감 + 정직함.
- AI 트로피컬 스톡 이미지 완전 회피 — 메탈릭, 홀로그래픽, 네온, 글로우 금지.
- *Pragmatic Programmer* / *Refactoring* 계열 — 글자 중심, 잡소리 없음.
- 1포인트 컬러(청동)는 단 한 곳에만 강하게 — 경계선.

## 생성 방법

- 이미지 생성 MCP 도구(DALL-E, Imagen 등)는 현재 환경에서 사용 불가
- **Python PIL** 기반 타이포그래피 생성으로 진행
- 한국어: AppleMyungjo (명조), Apple SD Gothic Neo (산세리프)
- 영문: Apple SD Gothic Neo (산세리프), Helvetica
- 해상도: 1600 × 2560 (EPUB 권장)

## Alternative Concepts (Not Used)

**Concept B — "통과하는 문":** 어두운 화면 중앙에 미세히 밝은 사각 프레임 (문 또는 portal). 글자보다 메타포가 강해서 1포인트 컬러로는 과할 수 있어 보류.

**Concept C — "diff 두 줄":** 상단에 `- vibe coded` / 하단에 `+ engineered` 식 diff 메타포. 재밌지만 *처방적 단정*에 가까워서 책 톤(재정의, 동료의 자세)과 어긋남. 보류.
