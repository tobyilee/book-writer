# Cover Design Log

## Version 1 (2026-10-12)
- Concept: A (미니멀리즘 — 심볼 하나 + 큰 타이포). 차분한 기술서 톤에 맞춤.
- Tool: imagemagick (폴백). 이미지 생성 MCP 없음, OPENAI/STABILITY/GEMINI API 키 없음.
  ImageMagick 7.1.2 + Python 레이아웃 스크립트(`cover_make.py`)로 그래프를 직접 그림.
- 심볼: 연결된 마크다운 페이지(작은 세로 사각형 + 세 줄)의 격자 — 쌓여 가는 위키.
  가운데 호박색 원 하나가 에이전트, 거기서 두 홉까지 뻗는 호박색 간선이 "읽기 경로".
  격자에 빈 칸이 몇 개 있어 아직 자라는 중임을 암시.
- 팔레트: 배경 `#0F1420 → #131B2C` 그라데이션 + 80px 엔지니어링 격자(`#1A2232`),
  본문 `#F3F5F8`, 보조 `#9AA5B8`, 간선 `#2C3850`, 페이지 `#6A7A96`, 악센트 1색 `#E8A33D`.
- 타이포: Apple SD Gothic Neo (제목 154pt, 3px 동색 스트로크로 볼드 대체; 부제 54pt),
  저자 Helvetica Neue 46pt. 한글은 시스템 폰트로 직접 렌더 — 깨짐 없음.
- Prompt (이미지 모델을 쓸 수 있게 될 때를 위한 동일 콘셉트 영어 프롬프트):
  ```
  A minimalist book cover in portrait format (1600x2560), for software developers.
  Muted dark navy background (#0F1420) with a faint engineering grid. Upper third:
  Korean title "쌓이는 지식, 답하는 에이전트" in large bold modern sans-serif, white,
  left-aligned, with a short amber rule above it; below it the subtitle
  "LLM 위키 패턴으로 짓는 사내 지식 베이스와 Claude 에이전트" in small muted grey.
  Lower half: a sparse lattice of small markdown page icons (portrait rectangles
  with three text lines) linked by thin slate-blue edges, like a wiki graph. One
  glowing amber node near the centre is an agent; its reading path to neighbouring
  pages is drawn in the same amber. Bottom centre: "Toby-AI" in small sans-serif.
  Calm, precise, editorial. Single accent colour. No stock photo look, no generic
  tech gradient, no robots, no garbled text.
  ```
- Result: cover.png (1600x2560, sRGB PNG)
- Notes: 200x320 썸네일에서 제목 두 줄 모두 판독됨. 재생성은
  `python3 -I cover_make.py cover.png` (시드 고정이라 동일 배치 재현).
