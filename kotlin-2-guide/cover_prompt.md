# Cover Design Log

## Version 1 (2026-04-27)

- **Concept:** B+C hybrid — illustrative bridge metaphor (four arches: 2.0/2.1/2.2/2.3 with 1.9 starting platform) under a clean Korean typographic block. Chosen over pure-minimalism (A) because the "건너가는 길" metaphor needed visual support, and over pure-typography (C) because a 1.9 senior reader scanning a thumbnail needs to read *cumulative progression* at a glance, not just words.
- **Tool used:** ImageMagick 7.1.2-19 (no image-gen MCP / API available in this environment; mood spec was achievable with vector composition + Korean system fonts, so ImageMagick was actually the better fit than a generative model that struggles with Korean glyphs).
- **Fonts:**
  - Korean title / subtitle / author: `Noto Sans KR (variable)` — `/Users/tobylee/Library/Fonts/NotoSansKR-VariableFont_wght.ttf`
  - Latin marks (KOTLIN 2.x, 1.9–2.3 labels, ecosystem strip): `Helvetica Neue` — `/System/Library/Fonts/HelveticaNeue.ttc`
- **Palette:**
  - Background gradient: `#1f2c4a` → `#0a1228` (vertical) with a soft radial highlight blended at 35%
  - Bridge arches (left → right, dark → bright): `#3a4d72`, `#4a6d96`, `#5fa3c5`, `#7fd6e0`
  - 1.9 stub platform: `#243652` outlined `#3a4d72` (intentionally muted — "where you are stuck")
  - 2.3 landing platform: `#94e3eb` outlined `#7fd6e0` (intentionally brightest — "where you are going")
  - Title: `#ffffff` on cobalt (max contrast); subtitle: `#c8d4ec` (one step softer); accents: `#7fd6e0` (cyan-teal)
- **Layout:**
  - Top third (y ≈ 360–1050): KOTLIN 2.x wordmark + 2-line Korean title + 2-line subtitle, all left-aligned to a 200px gutter
  - Middle band (y ≈ 1100–1500): bridge graphic with arch ellipses centered at x=520/760/1000/1240, each labeled below
  - Bottom strip (y ≈ 2300–2410): "K2  COMPILER  -  STDLIB  -  GRADLE  -  ECOSYSTEM" tag, then "Toby-AI", then a small teal accent bar
- **Output:** `kotlin-2-guide/cover.png`, 1600×2560 PNG, 16-bit RGBA, ~2.47 MiB

### Reproduction prompt (English, for any future image-gen API)

> Korean technical book cover, portrait 1600x2560. Vertical cobalt gradient background, deep navy at top (#1f2c4a) fading to near-black (#0a1228) at the bottom, with a soft radial highlight in the upper-middle. Center band: a stylized minimal vector bridge spanning left to right — four arch segments, each progressively brighter cyan-teal as they move right (dark slate #3a4d72 → mid cobalt #4a6d96 → cyan-blue #5fa3c5 → bright teal #7fd6e0), resting on a thin horizontal deck. Far left of the deck: a small muted "1.9" stub platform sitting slightly lower. Far right: a small bright "2.3" landing platform sitting slightly higher. Tiny labels under each column read 1.9, 2.0, 2.1, 2.2, 2.3, also growing brighter from left to right. Top one-third: large white Korean title (two lines) with a small teal "KOTLIN 2.x" wordmark above and a short teal accent line. Below the title: smaller light-blue Korean subtitle (two lines). Bottom: thin teal "K2 COMPILER · STDLIB · GRADLE · ECOSYSTEM" tag and "Toby-AI" author name centered. Mood: serious, authoritative, calm — Korean professional engineering book aesthetic. Clean vector style, no code snippets, no red, no comic style, no generic tech gradient.

### Reproduction command (ImageMagick 7)

The exact build is captured in three magick invocations (background gradient → bridge graphic with arches and version labels → typography overlay). See the harness shell history for `/tmp/cover-build/` build steps. Key parameters:

```
size:      1600x2560
gradient:  #1f2c4a -> #0a1228
arches:    ellipse cx=(520,760,1000,1240), rx=120, ry=(180..240), stroke #3a4d72..#7fd6e0
deck:      rectangle 380,1378 1380,1392 (sectioned by arch color)
title:     Noto Sans KR @ 132pt, white, "Kotlin 2.x로" / "건너가는 길"
subtitle:  Noto Sans KR @ 48pt, #c8d4ec, two lines
author:    Noto Sans KR @ 56pt, white, "Toby-AI", south gravity
```

### Result notes

- Korean glyphs render cleanly (Noto Sans KR resolves both Hangul and Latin without fallback).
- Thumbnail test: at 200×320 the title "Kotlin 2.x로 건너가는 길" stays readable and the arch progression is still visible as a stepped silhouette.
- "건너가는 길" metaphor is reinforced literally (the bridge) and chromatically (dim → bright cyan) — passes the "mood spec 후보 1" check (어두운 코발트 + 다리 실루엣 + 점진 그라디언트).
- No red, no cookbook clichés, no code snippets, no comic style — passes the prohibition list.

## Version 2 ...

(none yet)
