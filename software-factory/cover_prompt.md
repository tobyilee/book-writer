# Cover Design Log

## Version 1 (2026-09-28)
- Concept: A (미니멀리즘 — 큰 한글 타이포 + 심볼 하나). 차분한 기술서 톤, 로봇 클리셰 회피.
- 검토한 3안:
  - A (채택): 다섯 동의 계단식 공장 건물 = 자율성 사다리, 불 켜진 창 = 사람이 개입하는 지점
  - B: 불 꺼진 공장 내부에 결정 지점 몇 곳만 조명이 켜진 일러스트 — 한글 제목을 이미지 모델이 그려야 해 기각
  - C: 구현→테스트→수정→배포 루프를 원형 타이포로 — 사다리·조명이라는 책의 두 축이 드러나지 않아 기각
- Tool: HTML/SVG 타이포 표지를 headless Google Chrome으로 스크린샷(1600×2560). 이미지 생성 MCP·API 키가 없고 ImageMagick도 설치되어 있지 않아 폴백 경로로 만들었다 (이전 책들과 같은 방식).
- Source: `cover_source.html` (Noto Sans KR ExtraBold/Bold/Medium, Meslo Mono — `~/Library/Fonts`)
- Design:
  - 배경: 잉크 네이비 `#0B0F16` 단색. 그라데이션 없음
  - 키커: 앰버색 작은 사각형(불 켜진 창) + `SOFTWARE FACTORY` (모노, 앰버 `#F0B447`)
  - 제목: "소프트웨어"(오프화이트) / "팩토리"(앰버), Noto Sans KR 800, 252px
  - 부제: "첫 페어 프로그래밍부터 / 사람을 필요할 때만 부르는 개발 시스템까지" (Medium 60px, 슬레이트 `#8E9AAD`)
  - 심볼: 톱니 지붕을 얹은 공장 동 다섯 개가 L1→L5로 높아진다 (보조·협업·위임·승인·온콜). 불 켜진 창은 7→6→4→2→1개로 줄어들지만 마지막 동도 완전히 꺼지지 않는다. 다크 팩토리가 아니라 비싼 결정 지점에만 불을 켜 둔 라이트 팩토리라는 뜻이다. 승인 단계는 맨 위 두 창(게이트), 온콜 단계는 맨 위 한 창만 켜 두었다.
  - 하단: 가는 줄 아래 좌측에 저자 "Toby-AI", 우측에 `LIGHTS ON WHERE IT MATTERS` (모노, 흐린 슬레이트)
- 이미지 모델로 다시 만들 때 쓸 참고 프롬프트:
  ```
  Minimalist tech book cover, portrait 1600x2560, flat deep ink-navy background.
  Lower half: five simple flat factory bays with single sawtooth roofs standing
  side by side on one ground line, rising in height from left to right like a
  staircase. Each bay has a two-column grid of square windows. Warm amber lit
  windows thin out from left to right (seven, six, four, two, one); the tallest
  bay on the right has only one lit window near the top, so it is never fully
  dark. Unlit windows are dark slate. Subtle soft glow on lit windows only.
  Upper half left empty for typography. Calm, precise, editorial, geometric.
  No robots, no circuit boards, no stock photography, no generic tech gradient,
  no text.
  ```
- Alt text (편집자가 `book_manifest.json`의 `cover_alt`로 옮길 것):
  `짙은 남색 바탕에 '소프트웨어 팩토리' 제목이 크게 적혀 있고, 아래에는 보조·협업·위임·승인·온콜 순으로 높아지는 공장 건물 다섯 동이 서 있다. 오른쪽으로 갈수록 불 켜진 창이 줄어들지만 마지막 건물에도 창 하나는 켜져 있다.`
- Result: cover.png (1600×2560 PNG). 200×320 썸네일에서도 제목이 읽히는 것을 확인했다.
- Notes: 첫 렌더에서는 창의 빛번짐 레이어가 건물 본체 아래에 깔려 보이지 않았다. 레이어 순서를 바꿔 해결했다.
