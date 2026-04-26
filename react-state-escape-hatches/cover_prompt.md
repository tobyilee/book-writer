# Cover Design — 리액트, 상태와 경계

## Concept (selected)

**"경계선 위의 상태"** — minimalist typographic cover.
A single thin vertical line divides the canvas into two zones (state vs. escape hatch),
echoing the "boundary" metaphor in the subtitle. Deep navy field with cream serif
title, a subtle warm-orange accent dot on the dividing line representing the moment
state crosses the boundary.

## Concept candidates considered

1. **Boundary line (chosen)** — typographic, minimalist, two-zone composition
2. **Flowing nodes** — abstract state graph with arrows (rejected: too noisy at thumbnail size)
3. **Code minimalism** — code snippet motif (rejected: dates the cover, intermediate readers see this daily)

## Visual spec

- Canvas: 1600 x 2560 portrait (EPUB standard)
- Background: deep navy `#1a2540`
- Title color: cream `#f4ecd8`
- Accent: muted warm orange `#d97742` (single dot on boundary)
- Title typography: large serif (Korean: AppleMyungjo / Nanum Myeongjo / Noto Serif CJK KR)
- Subtitle typography: smaller sans, cream at 75% opacity
- Author "Toby-AI": small caps, bottom center, 60% opacity
- Vertical thin line at horizontal center, ~2px, cream at 30% opacity

## Image-gen prompt (English, for future regeneration via DALL-E / gpt-image-1)

> Minimalist book cover, portrait 1600x2560.
> Deep navy background (#1a2540). A single thin vertical cream line splits the
> canvas vertically. A small warm-orange dot sits on that line, slightly above
> center. Above the dot in large cream serif Korean type: "리액트, 상태와 경계".
> Below in smaller cream sans: "흔들리지 않는 멘탈 모델로 다시 쓰는 React".
> At the bottom, small cream type: "Toby-AI". Calm, intellectual, developer-book
> aesthetic. No code, no neon, no busy patterns. Negative space dominates.

## Generation method used

ImageMagick 7 fallback (no image-gen MCP wired in this worktree). Pure typographic
composition matches the chosen concept exactly — no loss vs. a generative pass.

## Regeneration

To regenerate with a different palette, edit the `magick` command in
`scripts/render_cover.sh` (if present) or rerun the inline command logged in
this file's git history.
