# Cover Design Record — 개발자를 위한 제텔카스텐

- **Output:** `cover.png` (1600 × 2560, RGB PNG, ~687 KB)
- **Generator:** Local Python + PIL (`_make_cover.py`) — used as deterministic fallback because no image-gen MCP/API was wired in this run, and the design brief was specific enough (Obsidian graph + dark IDE feel) that a controlled vector-style render beats a generic SDXL prompt.
- **Author imprint:** `Toby-AI` rendered directly on cover (bottom-left author block).

## Concepts considered

1. **Knowledge Graph (selected).** Obsidian-style node/edge constellation in upper half, large left-aligned bilingual typography in lower half. Yellow accent on a few "lit" nodes + the keyword "제텔카스텐". Reads as: scattered notes connect into a single system.
2. **Code-as-Notes.** Stylized markdown / wikilink syntax (`[[note]]`) cascading down the cover with one link highlighted. Risk: too text-heavy at thumbnail size, and the syntax flavor would alienate non-Obsidian readers.
3. **Card stack + connection.** Isometric stack of index cards with glowing wires linking three of them. Risk: easy to read as "flashcards" / Anki, which is the wrong mental model for Zettelkasten.

Concept 1 won because it (a) reads instantly at thumbnail size as "network of ideas", (b) maps 1:1 to the Obsidian graph view that the book teaches, and (c) leaves a clean lower band for typography.

## Visual spec

| Element | Value |
|---|---|
| Canvas | 1600 × 2560 (1.6:1, EPUB recommended) |
| Background | Vertical gradient `#080E1C` → `#101A30` + light film grain + radial vignette |
| Primary accent | `#FFD60A` (signature yellow — title keyword, lit nodes, accent rule) |
| Secondary accent | `#5AE6C8` (mint — eyebrow tag, "author" label) |
| Body ink | `#ECF0F8` (near-white) |
| Dim/UI gray | `#80A0A8` / `#3C4E6C` (corner ticks, faint edges) |
| Title font | Apple SD Gothic Neo Bold (TTC index 1), 168px |
| Subtitle font | Apple SD Gothic Neo SemiBold (TTC index 2), 52px |
| Mono accents | Menlo, 36px / 28px |
| Graph nodes | 6 lit "anchor" nodes + 120 small dim satellites in elliptical cloud, kNN edges |

## Typography layout

```
┌──── // for developers ─────────────────────────┐
│                                                │
│         (Obsidian graph constellation)         │
│                                                │
│  개발자를 위한                                 │  ← INK
│  제텔카스텐                                    │  ← YELLOW (key term)
│  ▬▬                                            │  ← yellow rule
│  옵시디언으로 코드와 글을                      │
│  함께 키우는 법                                │
│                                                │
│  author                                        │  ← MINT
│  Toby-AI                                       │  ← INK
└────────────────────────────────────────────────┘
```

## English prompt (for future image-gen API regeneration)

> Book cover, vertical 1600x2560. Dark navy gradient background (#080E1C top to #101A30 bottom) with subtle film grain and a soft radial vignette. Upper two-thirds: an Obsidian-graph-view-style network — small dim gray dots scattered in a loose elliptical cloud, connected by hairline edges; six brighter nodes glow in warm yellow (#FFD60A) with soft halos and slightly thicker yellow connecting lines among them, suggesting a few important hubs in a sea of notes. Lower third: bold left-aligned Korean typography. First title line "개발자를 위한" in near-white. Second title line "제텔카스텐" in the same warm yellow as the lit nodes. A short yellow horizontal rule under the title. Two-line subtitle below in lighter weight: "옵시디언으로 코드와 글을" / "함께 키우는 법". Top-left small mint monospaced eyebrow text "// for developers". Bottom-left author block: tiny mint mono label "author" above the name "Toby-AI" in semibold. Subtle thin gray IDE-style L-brackets in the four corners as registration marks. Mood: intellectual, calm, focused, developer aesthetic — like a quality programming book published by a thoughtful indie press.

## Regeneration / A/B notes

- Re-run via `python3 _make_cover.py` from the book folder. Random seed is fixed (`Random(42)` for nodes, `Random(7)` for grain) so output is deterministic — change the seeds to explore variants without touching layout.
- To swap the accent yellow for the alt mint palette: set `NODE_LIT = (90, 230, 200)` and the title keyword color follows.
- To make the graph denser/sparser, adjust the `120` satellite count and the kNN `k` in `draw_graph`.
- If a future run wants a hosted image-gen result instead, feed the English prompt above to `gpt-image-1` / equivalent at `1024x1536` or `1024x1792`, then upscale to 1600×2560 with PIL `LANCZOS` resampling.
