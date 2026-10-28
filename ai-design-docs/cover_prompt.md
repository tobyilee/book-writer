# Cover Design Log

## Version 1 (2026-10-28)
- Concept: A (minimal) — large Korean title + one symbol: a vertical traceability chain
  REQ → RULE → CONTRACT → ACCEPTANCE → SLICE → TEST → EVIDENCE, with the last node
  filled in amber and checked (the chain ends in evidence).
- Tool: ImageMagick 7 (`magick`) typographic cover. No image-gen MCP or API key was
  available, and image models do not render Korean text reliably, so the typographic
  route was chosen on purpose.
- Fonts: Noto Sans KR Black (title), Noto Sans KR Medium (subtitle, author), Menlo (chain labels, tag line).
- Palette: deep ink #0E1621 with faint 80px blueprint grid #152131, paper #F3EFE6,
  slate #A9B7C6 / #8C9DB1, single accent amber #E3A13B.
- Layout: top rule + mono tag "REQ-001 · TRACEABLE BY DESIGN"; title "검증 가능한 / 약속"
  (236pt, two lines, upper third); amber bar; subtitle two lines (62pt); chain in lower half;
  bottom rule + "Toby-AI" (48pt, bottom right). No robots, no logos, no brand names.
- Commands:
  ```
  magick -size 80x80 xc:'#0E1621' -fill '#152131' \
    -draw "rectangle 0,0 1,79" -draw "rectangle 0,0 79,1" grid.png
  magick -size 1600x2560 tile:grid.png -draw @cover.mvg cover.png
  ```
  (`cover.mvg` holds all text and shapes with literal coordinates; see the values above.)
- Equivalent image-model prompt (for a future regeneration with an image tool; render
  the Korean text separately):
  ```
  Minimalist editorial book cover, portrait 1600x2560. Deep ink-navy background with a
  barely visible blueprint grid. Upper third reserved for a large bold Korean title.
  Lower half: a single thin vertical line with seven small hollow circular nodes, the
  last node filled warm amber with a check mark — a traceability chain. Calm, precise,
  engineering-grade. Off-white and slate tones, one amber accent. No robots, no logos,
  no stock photo look, no generic tech gradient.
  ```
- Result: cover.png (1600x2560). Thumbnail check at 200x320: title readable.
- Suggested cover_alt (for book_manifest.json when the editor creates it):
  "짙은 남색 바탕에 '검증 가능한 약속' 제목과 REQ에서 EVIDENCE까지 이어지는 일곱 단계 추적 사슬이 그려진 표지"
