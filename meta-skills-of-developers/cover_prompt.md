# Cover Design Log

## Version 1 (2026-05-03)

- **Slug**: meta-skills-of-developers
- **Title**: 코드 밖에서 결정된다
- **Subtitle**: 잘 일하는 개발자의 메타 스킬
- **Author**: Toby-AI
- **Concept**: Hybrid of Direction 1 (structural systems visual) + Direction 2 (typography-centric).
  Korean typography occupies ~70% of the visual weight; an abstract decision-network
  diagram in the upper-right serves as a small accent that visualizes the book's thesis —
  *decisions made outside the code propagate back into the code through feedback loops.*
- **Tool**: Python 3 + Pillow 12.0 (vector primitives, no image-gen model).
  ImageMagick was unavailable on the host; image-gen models would have hallucinated
  Korean glyphs. Pillow gave deterministic Korean rendering and crisp vector control
  over the network diagram — a tradeoff that *favored* the typography-first concept.
- **Fonts**: Apple SD Gothic Neo (system) — Bold for main title, SemiBold for "메타 스킬",
  Light for subtitle, Medium for the small caps category tags.

### Palette (3 colors total on the background)

| Role | Hex | Notes |
|---|---|---|
| Background top | `#141821` | Charcoal-navy, warm undertone — not pure midnight |
| Background bottom | `#1c1e24` | Subtle vertical gradient (eased) |
| Primary ink | `#ebe8e0` | Warm off-white, paper-like (not `#ffffff`) |
| Dim ink | `#a09e96` | Subtitle / supporting copy |
| Accent (single) | `#d08a3c` | Warm amber — used only on title rule + 2 decision nodes |
| Network base | `#5a606e` / `#464c5a` | Edges and non-accent nodes |

Three colors on top of the background, exactly as the brief required (within the
"3색 이내" limit).

### Layout

- **Spine-side rule** at x=96 (left) — trade-paperback hint without an actual logo.
- **Top-left**: tiny `META · SKILLS / FOR DEVELOPERS` cap-tag (publisher mark feel).
- **Upper-right (~35% of canvas height)**: directed graph of 10 nodes / 15 edges.
  - 2 nodes are highlighted in amber and labeled `decision`, `trade-off` (English).
  - The graph is hand-placed (not generative) and contains an outer feedback cycle plus
    cross-links — visualizing the book's recurring claim that meta-skills form a loop,
    not a ladder.
- **Lower-half**: title block, left-aligned at x=196.
  - Category tag `DEVELOPER ESSAY · SYSTEMS THINKING` in dim ink.
  - Two-line title at 200pt Bold.
  - Single 6px amber rule (220px wide) under the title — the lone strong color statement.
  - Subtitle in two parts: light "잘 일하는 개발자의" + bold-weight "메타 스킬".
- **Footer**: short rule + `TOBY-AI` (40pt SemiBold) + a two-line audience descriptor.

### Prompt (recorded for re-generation / A-B testing)

This was code, not a model prompt. The descriptive equivalent for an image model would be:

```
A minimalist editorial-press book cover, 1600x2560 portrait.
Background: deep charcoal-navy (#141821) with a faint vertical gradient
toward (#1c1e24), warm rather than cold-tech.
Upper-right quadrant: an abstract directed-graph diagram of ~10 nodes
and ~15 edges forming an outer feedback cycle with cross-links;
two nodes filled in warm amber (#d08a3c), the rest hollow with
desaturated steel outlines; small lowercase serif/sans labels
"decision" and "trade-off" next to the amber nodes; visualize
"decisions outside the code feeding back into the code".
Left edge: thin vertical rule, with a tiny cap-tag "META · SKILLS
FOR DEVELOPERS" at the top in spaced grey caps.
Lower half, left-aligned at x=196:
  - small dim cap tag: DEVELOPER ESSAY · SYSTEMS THINKING
  - HUGE Korean two-line title in modern bold sans:
    "코드 밖에서" / "결정된다"
  - a single short warm-amber underline rule (the only saturated stroke)
  - subtitle in light: "잘 일하는 개발자의" then in semibold: "메타 스킬"
Bottom-left: short rule + "TOBY-AI" semibold + two-line audience tag.
Style: Stripe Press meets O'Reilly meets Pragmatic Bookshelf.
NO illustrations of people or robots, NO ladders/stairs/light-on-palm,
NO numbered lists, NO generic blue tech gradient, NO stock photo aesthetic.
Three colors max on top of the background.
```

- **Result**: `cover.png` (1600 × 2560, 2.0 MB)
- **Notes**:
  - Korean text rendered correctly via system Apple SD Gothic Neo — no glyph fallback.
  - Vector primitives (lines, ellipses) keep the network diagram crisp at any scale.
  - Thumbnail-tested at 200×320: main title remains legible; small node labels
    fade to texture (intended).

### Cliché-avoidance self-check

| Cliché | Status |
|---|---|
| Self-help cover patterns (ladder/stairs/glow/silhouette) | Avoided |
| "N가지 비밀" / numbered hooks on cover | Avoided |
| Generic blue tech gradient | Avoided (warm charcoal-navy, no rainbow) |
| AI/robot iconography | Avoided |
| Cheesy stock photo / 3D render aesthetic | Avoided (vector + type only) |
| Person illustration / hero pose | Avoided |
| More than 3 colors | Avoided (bg + ink + dim-ink + amber accent only) |
| Big quotation marks as decoration | Avoided |
| Clip-art keyboard / monitor / matrix code rain | Avoided |

Passes all the brief's "절대 금지" constraints.

### Iteration ideas (for future versions)

- **v2 (typography-only)**: drop the network diagram; let the title fill the upper 60% of
  the canvas. Useful if the diagram feels too "infographic" against tech-shelf neighbors.
- **v3 (warmer ground)**: swap charcoal-navy for ink-on-cream — less Stripe Press,
  more Korean publisher (인사이트/한빛) feel. Risk: looks closer to a literary essay
  than a developer book; would hurt tech-shelf placement.
- **v4 (denser graph)**: ~20 nodes with one tiny labeled cluster — leaning further into
  Direction 1. Defer until validating that v1's diagram is read as "system" and not
  "constellation" by sample readers.
