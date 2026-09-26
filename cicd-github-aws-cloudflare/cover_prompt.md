# Cover Design Log

## Version 1 (2026-09-26)
- Concept: A (minimalist — big typography + a single symbol)
- Tool: HTML/SVG rendered with headless Google Chrome (image-gen MCP/API and ImageMagick not available in this environment). Source: `cover_source.html`.
- Design:
  - Background: deep navy #0D1624 with a faint 80px engineering grid
  - Kicker: `CI/CD · VERIFY BEFORE DEPLOY` (mono, teal #5FD4C0)
  - Title: "배포는 / 검증이다" (Noto Sans KR 800, 260px, "검증" in teal)
  - Subtitle: "GitHub·AWS·Cloudflare로 짜는 / AI 시대의 CI/CD" (Noto Sans KR 500)
  - Symbol: horizontal pipeline commit → build → test → amber gate with check → deploy; no vendor logos
  - Author: "Toby-AI" small at bottom-left under a hairline rule
- Equivalent image-model prompt (for future regeneration):
  ```
  A minimalist tech book cover, portrait 1600x2560. Deep navy background with a
  faint blueprint grid. Large bold Korean sans-serif title in the upper half,
  one word highlighted in calm teal. Lower third: a single clean horizontal
  pipeline line with three small ring nodes, an amber gate/checkpoint with a
  check mark, and a final teal deploy node with an arrow. Small author name at
  bottom. Calm, trustworthy, engineering editorial. No vendor logos, no stock
  photography, no generic tech gradient, no glow effects.
  ```
- Result: cover.png (1600x2560), title legible at 200x320 thumbnail
- Notes: Typographic cover chosen so Korean text renders correctly.
