# Cover Design Log

## Version 1 (2026-10-10)
- Concept: A (미니멀리즘 — 심볼 하나 + 큰 타이포). 심볼은 "신뢰 곡선": 좌하→우상으로 오르는 완만한 S자 베지어 곡선 하나, 4개 단계 지점(지켜보기 → 자가 검증 → 클라우드 → 자동 머지)마다 링 마커 위로 에이전트 점이 1·2·3·5개로 늘어남.
- Tool: ImageMagick 7.1.2 (`magick`) — 이미지 생성 MCP/API 없음. 곡선은 Python으로 큐빅 베지어 점 200개를 계산해 `-draw polyline`으로 그림 (`cover_make.py`로 재생성 가능).
- Fonts: Noto Sans KR (Bold 제목 176pt / Light·Regular 부제 54pt / Medium 단계 라벨 36pt), `/Users/tobylee/Library/Fonts/NotoSansKR-*.ttf`
- Palette: 배경 잉크 네이비 `#15202f`, 타이포 페이퍼 `#f2ede3`, 곡선 앰버 `#e3a94f`, 보조 `#9aa6b5`. 그라데이션·네온·로봇 없음.
- Layout: 상단 1/3 제목 2행 + 부제, 하단 2/3 곡선·단계 라벨·베이스라인, 좌하 `Toby-AI`, 우하 대상 독자 한 줄.
- Prompt (이미지 모델용 보존, 미사용):
  ```
  A minimalist editorial book cover, portrait 1600x2560. Deep ink-navy background.
  Title "에이전트를 믿어도 될까" in bold Korean sans-serif, top third. Subtitle
  "신뢰 곡선으로 배우는 Claude Code · Codex 실전 개발" below in light weight.
  Center-lower: one calm amber S-curve rising from bottom-left to upper-right,
  four ring markers along it; above each marker a small column of off-white dots
  growing 1, 2, 3, 5. Stage labels beneath a thin baseline. Small "Toby-AI" bottom-left.
  Confident, quiet, trustworthy. No neon, no generic tech gradient, no robots.
  ```
- Result: cover.png (1600×2560, 8-bit sRGB)
- Verified: 500×800·200×320 축소본에서 한글 제목 깨짐 없음, 썸네일에서 제목·곡선 판독 가능.
- cover_alt (book_manifest.json에 넣을 대체 텍스트): "짙은 남색 배경 위에 책 제목 '에이전트를 믿어도 될까'와 부제, 그 아래 지켜보기·자가 검증·클라우드·자동 머지 네 단계를 따라 오른쪽 위로 오르는 앰버색 신뢰 곡선과 단계마다 늘어나는 흰 점들"
