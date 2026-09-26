# Cover Design Log

## Version 1 (2026-09-26)
- Concept: A (미니멀리즘 — 큰 한글 타이포 + 심볼 하나)
- Tool: HTML/SVG 타이포 표지 → headless Chrome 스크린샷 (1600×2560). 이미지 생성 MCP·API 키 없음, ImageMagick 미설치라 폴백 경로로 대체.
- Source: `cover_source.html` (Noto Sans KR variable, `~/Library/Fonts/NotoSansKR-VariableFont_wght.ttf`)
- Design:
  - 배경 딥 네이비 `#0D141D`, 본문 오프화이트, 액센트 GitHub 그린 `#3FB950`
  - 상단: 영문 키커 "DEV WORKFLOW STRATEGY" + 그린 룰
  - 제목 3줄(개발 / 워크플로 / 전략) 205px 굵게, 부제 2줄 62px 회청색
  - 하단 그래픽: 왼쪽에서 다섯 개의 슬레이트/블루 브랜치 선(커밋 점 포함)이 한 점으로 합류 → 오른쪽으로 곧게 뻗는 굵은 초록 main 줄기, 등간격 커밋 원 4개 = 머지 큐의 질서
  - 좌하단 저자 "Toby-AI", 우하단 "MERGE · QUEUE · MAIN"
- Reference prompt (이미지 모델로 재생성할 경우):
  ```
  Minimalist tech book cover, portrait 1600x2560, deep navy background.
  Lower half: several thin slate-blue git branch lines with hollow commit
  dots flowing in from the left, converging into a single point, then
  continuing to the right as one thick bright green (#3FB950) main line
  with evenly spaced commit circles, conveying the order of a merge queue.
  Upper half left empty for typography. Clean, calm, editorial.
  No text, no stock photo, no generic tech gradient.
  ```
- Result: cover.png — 200×320 썸네일에서 제목 판독 확인
- Notes: v1 첫 렌더에서 제목·부제 겹침 → 제목 크기 230→205px, 부제·그래픽 하향 조정으로 해소
