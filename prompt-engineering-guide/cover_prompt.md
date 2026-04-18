# Cover Design Log

## Version 1 (2026-04-18)

- **Concept:** A — Minimalist blueprint/typography hybrid
- **Tool:** ImageMagick 7 (`magick`) — no image-gen MCP/API was connected in this session, so the cover was composed programmatically with vector primitives and Pretendard (Korean) typography. This is actually a strong fit for a rigorous technical book: pixel-perfect control, no AI hallucinated text, reproducible.
- **Rationale:** Brief asked for "rigorous, systematic, engineering" — a programmatic blueprint grid + precision typography reads more authentic than a generative illustration. Avoids the robot/neon/cyberpunk cliché entirely.

### Visual system

| Element | Spec |
|---|---|
| Canvas | 1600 × 2560 PNG, sRGB |
| Background | Vertical gradient `#0d1b2a` → `#14233a` (deep navy → midnight charcoal) |
| Grid | 80px orthogonal grid, stroke `#1e3a5f` @ 1px — "architect's blueprint" motif |
| Accent color | Amber `#e8a33d` — used for subtitle, bracket marks, short rule |
| Decorative marks | Two L-bracket corners (top-left, bottom-right) + a 120px rule under the series line — subtle engineering / measurement feel |
| Series tag | `PROMPT  ENGINEERING  SERIES` + `Vol. 01` in steel-blue `#7a93b5` / `#5a7aa0` |
| Title | `프롬프트` / `엔지니어링` — Pretendard Black, 210pt, kerning −8, white |
| Subtitle | `원칙, 평가, 운영` — Pretendard Medium, 76pt, amber `#e8a33d` |
| Tagline | `감으로 쓰는 프롬프트에서, / 재현 가능한 공학으로.` — Pretendard Light, 44pt, light-steel `#b8c9de` |
| Author | `TOBY-AI` (Pretendard Bold, 38pt, kerned) + `지음` (Pretendard Light, 26pt) — bottom-left |

### Typography

- **Pretendard** (local install at `~/Library/Fonts/`) — the de-facto modern Korean sans-serif used across Korean tech publishing. Matches the "modern sans-serif Korean typeface" brief exactly.
- Left-aligned hierarchy (series → title → subtitle → tagline → author) for editorial, book-cover feel — not centered-stock-image feel.

### Equivalent natural-language prompt (for future image-gen API regeneration)

```
A minimalist editorial book cover in portrait format (1600x2560). Deep
navy-to-charcoal vertical gradient background (#0d1b2a to #14233a)
overlaid with a faint orthogonal blueprint grid (80px spacing, thin
#1e3a5f lines) evoking an architect's drawing. Upper-left small
cap-letter tag "PROMPT ENGINEERING SERIES" in muted steel-blue, with
"Vol. 01" underneath. Large bold Korean title "프롬프트 / 엔지니어링"
stacked on two lines, Pretendard Black, pure white, occupying the
upper-middle third. Amber accent subtitle "원칙, 평가, 운영" directly
below. A two-line lighter-weight tagline "감으로 쓰는 프롬프트에서, /
재현 가능한 공학으로." in light steel. Small "TOBY-AI 지음" author mark
bottom-left. Two thin amber L-bracket corner marks (top-left and
bottom-right) as engineering/measurement motif. Editorial, calm,
rigorous, engineering-precision feel. No stock photography, no
generic tech gradient, no robot imagery, no neon, no cyberpunk.
```

### Verification

- [x] Resolution 1600×2560 (exact)
- [x] Thumbnail (200×320) test: title "프롬프트 엔지니어링" + subtitle still readable
- [x] Author `TOBY-AI` visible on cover
- [x] No cliché elements (no glowing robot, no cyberpunk neon, no stock-photo AI brain)
- [x] Color palette matches brief (deep navy + amber accent, no flashy)

### Notes / adjustments for possible v2

- If later switching to a generative model (gpt-image-1, imagen), use the natural-language prompt above as seed and specify "book cover, portrait 1600x2560, Korean title text rendered literally" — generative models often mangle Korean glyphs, so the current typography-first approach may still win.
- Could add a subtle abstract shape (e.g., an "iteration arrow" from rough → refined) between the title and tagline for v2 if stakeholders want more visual storytelling.
