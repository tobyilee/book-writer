# Cover Design Log

## Version 1 (2026-05-11)

**Book:** 빌드를 다시 짠다 — Spring Boot × Gradle 9.5 × Kotlin DSL 실전 가이드
**Author:** Toby-AI
**Concept choice:** Option A — DAG (directed acyclic graph) build-graph visualization
**Tool:** ImageMagick (pure typography + vector drawing, no generative image model)
**Output:** `cover.png` (1600×2560, PNG, 16-bit sRGB)

### Why ImageMagick over a generative model

The cover's central element is an abstract directed acyclic graph — exactly the kind of "geometric + clean lines" subject that generative image models tend to render with cluttered noise, inconsistent node shapes, and unreadable pseudo-text labels. ImageMagick's primitive drawing operators (`roundrectangle`, `line`) produce crisp, deterministic geometry and let me place real Korean glyphs via Noto Sans KR / Apple SD Gothic Neo — no hallucinated typography.

### Equivalent generative prompt (kept for reference / future A/B)

If we ever swap in a generative pass:

```
A minimalist book cover in portrait format (1600x2560). Top third: large Korean
title "빌드를 다시 짠다" in bold modern sans-serif, ivory white on deep navy
(#02303A → #0A1828 vertical gradient). Below the title, a thin Spring leaf
green (#6DB33F) horizontal rule, then a smaller mint-green subtitle line
"Spring Boot × Gradle 9.5 × Kotlin DSL" and a soft gray "실전 가이드" tag line.

Center: an abstract directed acyclic graph of ~13 rounded-rectangle nodes
connected by thin teal-gray edges. The graph grows from a single node at the
top labeled "app" outward and downward into a multi-module cluster (domain,
order, payment, shared, common, api, build-logic, plugin). Toward the bottom,
four mint-accent nodes (infra, native, release, publish) connected by brighter
spring-green edges represent the growth tip — the book's narrative arc of an
app that scales from a single dependency line into a richly structured build.

Bottom: small "Toby-AI" author byline and "v1.0.0" version tag. Cream-white
typography on deep navy throughout. Editorial, calm, confident, technical but
warm. Avoid neon glow, stock photo aesthetic, gradient tech clichés, isometric
3D renders, and any code-text texture in the background.
```

### Actual ImageMagick build pipeline

1. **Background**: 1600×2560 angled gradient `#02303A → #0A1828` (Gradle navy)
2. **Edges layer**: 15 teal-gray (`#3A6478`) lines forming the DAG topology, plus 3 brighter spring-green (`#6DB33F`) edges marking the "growth tip" branches
3. **Nodes layer**:
   - 9 spring-green-stroked rounded rectangles for the main module nodes
     (`app`, `domain`, `order`, `payment`, `shared`, `common`, `api`,
     `build-logic`, `plugin`)
   - 4 mint-stroked nodes (`infra`, `native`, `release`, `publish`) — the
     growth tip
   - All nodes share a slightly-lighter-than-bg fill (`#0E3A47`) for depth
4. **Node labels**: Apple SD Gothic Neo, cream on green nodes, mint on mint nodes
5. **Title**: Noto Sans KR Bold at 200pt, kerning -6, ivory white (`#F5F1E8`),
   centered at y=280 from top
6. **Divider**: spring-green 4px rule between title and subtitle
7. **Subtitle row 1**: Noto Sans KR at 46pt, mint (`#A8E063`), centered y=640
8. **Subtitle row 2**: Apple SD Gothic Neo at 42pt, soft gray (`#C9D6DE`)
9. **Author block**: "Toby-AI" 56pt cream + "v1.0.0" 26pt slate gray, bottom center

### Color palette

| Token | Hex | Role |
|-------|-----|------|
| Gradle navy (deep) | `#02303A` | Background top |
| Gradle navy (deeper) | `#0A1828` | Background bottom |
| Node fill | `#0E3A47` | Inside of all nodes |
| Edge gray-teal | `#3A6478` | Default DAG edges |
| Spring leaf green | `#6DB33F` | Main module strokes, divider, bright edges |
| Mint accent | `#A8E063` | Growth-tip nodes, subtitle row 1 |
| Cream / ivory | `#F5F1E8` | Title, author byline, node labels |
| Slate gray | `#C9D6DE` | Subtitle row 2 |
| Muted slate | `#7A8B96` | Version tag |

### Thumbnail readability check

At 200×320 (typical EPUB library thumbnail), the title "빌드를 다시 짠다" remains
fully legible; the subtitle row reads as a single light strip; the DAG silhouette
reads as an abstract "growing graph" shape without forcing individual node labels.

### Notes / known limitations

- All-caps roman subtitle is single-line — fits at 46pt with 2px kerning,
  measured to ~1100px wide (well within 1600 canvas).
- Mint-accent node labels are colored mint instead of dark — the original
  dark-on-mint plan failed legibility because the node fill is dark navy, not
  mint solid. Switched to mint-on-navy with mint stroke surround for cohesion.
- No filtering / no noise / no shadow effects — kept the geometry crisp so the
  cover survives heavy downscaling.

### Regeneration command

The full pipeline lives in `/tmp/cover-build/` (transient). To rebuild,
reproduce these stages:

1. `magick -size 1600x2560 gradient:'#02303A-#0A1828' -define gradient:angle=160 bg.png`
2. Run the DAG drawer (edges + nodes) — see `draw_graph_v2.sh` in the build session
3. Add labels with Apple SD Gothic Neo
4. Composite background + graph, then layer title / divider / subtitle / author /
   version with Noto Sans KR and Apple SD Gothic Neo

If a future revision is requested (e.g., "표지 다시"), back up this version as
`cover_v1.png` before regenerating.
