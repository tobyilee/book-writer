# Cover Design Log

## Version 1 (2026-07-12)

- **Concept:** A (미니멀리즘) — 심볼(두 개의 루프) + 큰 타이포. 3안 중 A를 선택한 이유: 차분한 기술서 톤 + Java/Spring·React 현업 개발자 대상 → 미니멀·기하학적 심볼이 스톡사진/일러스트보다 신뢰도가 높고 오래 살아남는다.
- **Tool:** ImageMagick 7 (`magick`) 절차적 생성. 이미지 생성 MCP/API가 세션에 연결되어 있지 않아(도구 탐색 결과 없음) 스킬의 ImageMagick 폴백을 사용했다. 단, 기본 그라디언트 플레이스홀더가 아니라 MVG(`ellipse`, `stroke-dasharray`) 프리미티브로 표지 핵심 모티프(두 개의 루프)를 직접 벡터 드로잉했다.
- **핵심 모티프:** 매니페스트의 `cover_alt`에 이미 기술된 컨셉("증발하는 에이전트의 피드백 루프와 누적되는 사람의 학습 루프, 두 개의 루프")을 그대로 시각화.
  - 오른쪽: 굵고 완전한 틸(teal) 원형 루프 + 소프트 글로우 — 누적되는 사람의 학습 루프 (인간 학습 곡선, 굵고 안정적).
  - 왼쪽: 앰버(amber) 색 원형 루프, 하단은 두껍고 불투명, 상단으로 갈수록 얇아지고 점선으로 흩어지며 사라짐 — 증발하는 에이전트 피드백 루프.
  - 두 루프가 중앙에서 겹쳐(interlock) 두 피드백 경로가 같은 지점(현재 순간의 작업)에서 출발하지만 다른 운명을 맞는다는 책의 핵심 논증을 형상화.
- **레이아웃:** 1600×2560. 제목(NanumGothic ExtraBold, 130pt, 상단 1/3) → 앰버 밑줄 액센트 → 부제(NanumGothic Bold, 56pt, 앰버 라이트) → 넉넉한 여백 → 두 루프 모티프(중하단) → 저자명(NanumGothic Regular, 44pt, 하단 중앙).
- **팔레트:** 배경 딥 네이비(`#0a1420`) → 딥 틸(`#0d2a2e`) 수직 그라디언트 + 모티프 중심의 소프트 틸 글로우(`#1f5f5a`, blur). 누적 루프 `#83e6dc`(글로우 `rgba(63,214,198,0.45)`), 증발 루프 `rgba(242,161,84,*)` 12단계 불투명도 감쇠. 제목 `#f5f1e6`(warm white), 부제 `#f2c894`, 저자 `#c9dcda`.
- **폰트:** `/Users/tobylee/Library/Fonts/NanumGothicExtraBold.otf` (제목), `NanumGothicBold.otf` (부제), `NanumGothic.otf` (저자) — 시스템 Apple SD Gothic Neo는 ImageMagick에서 `.ttc` 페이스 직접 지정이 실패해 나눔고딕 계열로 대체.
- **Result:** `cover.png` (1600×2560, PNG 16-bit sRGB)
- **검증:**
  - [x] 해상도 1600×2560
  - [x] 200×320 썸네일 축소본에서도 제목·모티프 식별 가능 (확인 완료)
  - [x] 저자 표기 `Toby-AI` 하단 중앙 명시
  - [x] 클리셰 회피 — 스톡사진/기본 그라디언트 배경 아님, 책의 핵심 은유(두 루프)를 직접 벡터로 표현
- **Notes:** 첫 시도에서 글로우 halo의 blur sigma가 과도해(0x40) 링이 두꺼운 단색 도넛처럼 보이는 문제가 있었음 → sigma를 0x9~0x12로 낮추고 halo 자체의 stroke-opacity를 낮춰 해결. 하단 액센트 라인이 저자명 텍스트와 겹치는 버그가 있었음 → 하단 라인 제거로 해결.

## Reproduction

절차적 생성이므로 "프롬프트" 대신 재현 스크립트를 남긴다. 스크립트 원본은 세션 스크래치패드(`.../scratchpad/cover/`)에 있으며 핵심 단계는:

1. `gradient:'#0a1420'-'#0d2a2e'` 배경 → 모티프 중심에 blur된 원형 글로우(`#1f5f5a`, blur 0x140) 스크린 합성
2. 누적 루프: `ellipse 940,1700 220,300 0,360` — halo(`rgba(63,214,198,0.45)`, strokewidth 15, blur 0x9) + crisp(`#83e6dc`, strokewidth 9)
3. 증발 루프: 동일 중심 오프셋(`700,1700`, 220,300)에 12개 `ellipse` 각도 구간(30~60도 단위)을 불투명도 0.92→0.12로 감쇠, 상단 구간은 `stroke-dasharray`로 점선 처리
4. 텍스트: `-font NanumGothicExtraBold.otf -pointsize 130 -gravity North -annotate +0+270` (제목) 등 순차 `-annotate`
