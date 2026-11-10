# Cover Design Log

## Version 1 (2026-11-10)
- Concept: A+C 혼합 (미니멀 심볼 + 타이포 중심) — 차분한 기술서
  - 기각: B 일러스트형(사람·에이전트 인물화) — 썸네일에서 제목 가독성이 떨어지고 클리셰 위험
- Tool: headless Chrome으로 SVG/HTML 타이포 표지 렌더 (폴백)
  - 이미지 생성 MCP·API 키 없음, ImageMagick 미설치 → 동일 목적의 타이포 폴백을 Chrome 스크린샷으로 대체
  - 소스: `cover_source.html` (재렌더: `chrome --headless=new --hide-scrollbars --force-device-scale-factor=1 --window-size=1600,2560 --screenshot=cover.png file://.../cover_source.html`)
- Design:
  - 배경: 잉크 블루 #13243a 단색 + 옅은 블루프린트 그리드 (그라데이션 없음)
  - 상단: 앰버 라벨 "SPEC-DRIVEN DEVELOPMENT" / "AI 에이전트와 함께하는" / 큰 제목 "스펙 주도 개발" (Apple SD Gothic Neo ExtraBold)
  - 부제 2줄: "도구 없이 시작해" / "OpenSpec · Spec Kit · Superpowers까지" (텍스트만, 로고·상표 이미지 없음)
  - 중앙 심볼: 왼쪽 `spec.md` 카드(R1~R6 요구사항 줄) → 앰버 곡선이 오른쪽 `impl` 카드의 코드 줄로 흐름. 스펙 카드의 흰색·청록 캐럿 두 개 = 같은 페이지를 읽는 사람과 에이전트
  - 카피: "스펙을 먼저, 그러나 필요한 만큼만" (앰버)
  - 하단 우측: 저자 "Toby-AI" (모노스페이스, 작게)
- Equivalent prompt (이미지 모델 사용 시 참고용):
  ```
  Minimalist book cover, portrait 1600x2560. Flat deep ink-blue background with a faint
  blueprint grid. Large bold Korean sans-serif title in the upper third. Center: two
  clean document panels — a spec document with numbered requirement lines on the left,
  a code panel with indented lines on the right — thin amber curves flowing from spec
  lines into code lines. Two small cursors on the spec page suggest a human and an agent
  reading the same page. Small author name bottom-right. Precise, calm, trustworthy.
  No logos, no trademarks, no stock photography, no generic tech gradient, no robots.
  ```
- Result: cover.png (1600x2560)
- Notes: 1차 렌더에서 연결선 끝점이 줄 번호와 겹쳐 줄 번호 열을 제거. 320px 썸네일에서 제목·부제 판독 확인.
