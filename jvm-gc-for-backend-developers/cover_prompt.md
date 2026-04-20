# Cover Design Record

## Book
- Title: JVM을 알아야 서버가 산다
- Author: Toby-AI
- Series: Backend Engineering Series

## Concept Shortlist

### Concept A (used): JVM Heap Diagram — Technical Blueprint
Dark navy background with a glowing grid overlay. Central visual is a
labeled JVM heap memory diagram (Eden, Survivor 0/1, Old Generation,
Metaspace) with connecting arrows showing the object promotion flow.
GC type badges (Minor GC, Major GC, Full GC, G1/ZGC) sit below the
diagram. Cyan/green accent colors represent live memory; muted blue
represents stable long-lived objects.

### Concept B (not used): Minimalist Symbol
Single large recycling-arrow symbol built from circuit-board traces on
a deep navy field. Title in bold white sans-serif; no diagram.

### Concept C (not used): Server Rack + Trash Can
Isometric server rack illustration with a glowing garbage-collection
indicator overlaid. More illustrative, less technical-blueprint feel.

## Implementation
Tool: ImageMagick 7 (magick CLI)
Method: Multi-layer compositing via Python subprocess
Layers (bottom to top):
1. Dark navy gradient base (#0a1628 → #040c1e)
2. Radial color blooms — deep blue top-right, dark green bottom-left
3. Grid overlay (80px cells, #1a3a6e, 15% opacity)
4. Cyan/green glow nodes
5. Typography (Apple SD Gothic Neo, Korean + Latin)
6. JVM heap diagram (rectangles + labels + arrows)
7. GC type badge row
8. Tagline panel
9. Bottom author bar

## Color Palette
| Role              | Hex       |
|-------------------|-----------|
| Background        | #0a1628   |
| Grid lines        | #1a3a6e   |
| Title white       | #ffffff   |
| Title accent      | #00e5cc   |
| Cyan glow         | #00d4ff   |
| Eden / Minor GC   | #00c875   |
| Survivor          | #7acc00   |
| Old Gen           | #3a6ab4   |
| Metaspace         | #6a4aaa   |
| Full GC warning   | #ff9944   |
| Author bar bg     | #0d1e3a   |

## Output
- cover.png — 1600x2560 px, PNG, ~2.9 MiB

## Regeneration Notes
- To swap concept B: replace diagram section with a single large
  `circle`-based recycling symbol drawn in cyan on the base layers.
- To A/B test: run concept B and name output cover_v2.png.
- Korean font path: /System/Library/Fonts/AppleSDGothicNeo.ttc
