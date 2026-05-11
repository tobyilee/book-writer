# Cover Design Record — Spring 개발자를 위한 EventStorming

## 채택 콘셉트: "Sticky → Code Bridge"

부제 "오렌지색 sticky가 Java 코드가 되기까지"를 표지 위에서 그대로 시각화한다. 워크숍 벽에서 막 떼어낸 듯한 sticky note 모임 → 화살표 → 실제 Java record 한 줄 → 한글 제목. EventStorming 색상 grammar(오렌지 Domain Event, 노랑 Aggregate, 블루 Command, 라일락 Policy)를 표지의 부 시그니처로 노출.

## 검토했던 3개 안

1. **(채택) Sticky → Code Bridge** — 부제를 그대로 시각화. 워크숍 에너지 + 기술서 정합성.
2. **타이포 미니멀** — 큰 한글 제목 + 오렌지 점 하나. 깔끔하나 EventStorming 정체성이 약함. 탈락.
3. **벽 사진 무드** — 실제 sticky 벽 사진 느낌. 이미지 생성 도구 없이는 재현 난이도 ↑. 탈락.

## 컴포지션

- **배경:** `#f4ede0` 따뜻한 베이지 + 약한 노이즈 텍스처 (화이트보드/오프화이트 페이퍼 느낌)
- **상단:** 보조 sticky 3종이 모서리에서 peeking
  - 좌상단: 노랑 Aggregate "Order"
  - 우상단: 블루 Command "Place Order"
  - 우중앙: 라일락 Policy "Notify User"
- **중앙:** 오렌지 Domain Event sticky "Order Placed" — 화면 중심, 약간 좌측 회전(-3°), 드롭 섀도우로 입체감
- **중간:** 손그림 느낌 곡선 화살표가 hero sticky → 코드 패널로 내려감
- **코드 패널:** 흰 라운드 박스 위에 모노스페이스 Java 한 줄
  - `record OrderPlaced(OrderId id, Money total) {}`
- **타이틀 블록:**
  - 1행: `Spring 개발자를 위한` (Pretendard Bold, 96pt, 다크 잉크)
  - 2행: `EventStorming` (Pretendard Bold, 168pt, 짙은 오렌지 `#d97a07`)
- **부제:** `오렌지색 sticky가 Java 코드가 되기까지` (Noto Sans KR, 48pt, 부드러운 잉크 톤)
- **하단:** 오렌지 작은 룰 라인 + `Toby-AI` (Pretendard Bold, 44pt)

## 사용 폰트

| 용도 | 폰트 |
|------|------|
| 한글 제목·부제·저자 | Pretendard Bold / Noto Sans KR |
| Sticky 손글씨 | Marker Felt (macOS 시스템) |
| Java 코드 라인 | SF NS Mono |

## 컬러 팔레트

| 역할 | HEX | 설명 |
|------|-----|------|
| 배경 | `#f4ede0` | 따뜻한 종이/화이트보드 |
| Domain Event (메인) | `#f59e2c` | 오렌지 — 책 정체성 |
| Domain Event 어둡게 | `#d97a07` | 제목 컬러 강조 |
| Command | `#5fa8e6` | EventStorming 블루 |
| Policy | `#c9a8e6` | 라일락 |
| Aggregate | `#f4d35e` | 노랑 |
| 본문 잉크 | `#1f1d18` | 따뜻한 다크 (순흑 회피) |

## 생성 방법

- **도구:** ImageMagick 7.1.2 (`magick` 커맨드)
- **이미지 생성 MCP:** 사용하지 않음 (Agent SDK MCP 미연결, 환경 폴백)
- **스크립트:** `/tmp/cover-work/build_cover.sh` — 9단계 합성 (배경 → sticky 4종 → 합성 → 화살표 → 코드 패널 → 타이틀 → 부제 → 저자 → 1600×2560 리사이즈)
- **재생성:** sticky 위치·회전·라벨만 바꿔 빠르게 A/B 가능. 동일 스크립트에서 색상 변수만 조정.

## 회피한 클리셰

- 회로기판/네트워크 노드 패턴 — 사용 안 함
- 단색 그라데이션 + 큰 글자만 — 거부
- AI 생성티 코드 텍스트 — `record OrderPlaced(OrderId id, Money total) {}` 의미 있는 실제 Java 17 record 한 줄로 작성

## 향후 A/B 옵션

- 오렌지 sticky를 한 장 더 추가해 EventStorming 워크숍의 "여러 이벤트가 시간순으로 흐르는" 느낌 강화
- 화살표를 시간축(왼→오)으로 회전해 BigPicture EventStorming의 timeline 모티프 차용
- 부제 위치를 sticky 옆으로 옮기고 제목을 상단으로 끌어올리는 타이포 우선 레이아웃
