# Cover Design Log

## Version 1 (2026-05-25)

### Metadata
- Book: 브리즈번 키친, 멕시코를 담다
- Subtitle: 정통 멕시칸 요리, 한국인의 손맛으로
- Author: Toby-AI
- Genre: practical (cookbook)
- Audience: 호주(브리즈번) 거주 한국인, 멕시칸 초보~중급

### Concept Selected: B — Illustrative
Three concepts considered:
- A (Minimalist): Single chili symbol + large Korean title on flat background
- **B (Illustrative): Food motifs (avocado, lime, dried chili, tortilla, cilantro) arranged around title — CHOSEN**
- C (Typography-centric): Title letterforms as primary graphic, minimal imagery

Chosen B because: practical cookbook benefits from visual food cues; warm ingredient motifs
immediately communicate "Mexican cooking"; suits the vibrant, appetising tone requested.

### Design Decisions
- Background: deep terracotta gradient (#3D0F05 → #7A2A0A) — warm, rich, food-oriented
- Border system: lime green (#6BBF4E) top/bottom/side stripes — Mexican vibrancy accent
- Food motifs (ImageMagick primitives):
  - Avocado (top right): layered ellipses in dark green / pale green / brown pit
  - Lime (top left): bright green circle with cross-segment lines
  - Dried chili (top center): elongated ellipse + stem
  - Small chili peppers: flanking elements (upper and lower)
  - Tortilla/corn circle (lower center): concentric warm-brown rings
  - Cilantro leaf clusters: flanking the tortilla (left and right)
- Center band: salsa red (#B52020) with gold accent lines — subtitle zone
- Color palette: terracotta · salsa red · lime green · corn yellow · warm white
- Fonts used:
  - Title: Recipekorea 饭内眉 FONT.otf (food-themed Korean display font)
  - Subtitle: GmarketSansBold.otf (modern Korean sans)
  - Author/Label: Pretendard-Bold.otf / Pretendard-Medium.otf

### Tool Used
ImageMagick 7.1.2-19 (magick CLI) — local fallback
No image generation MCP/API was available in this environment.

### Image Generation Command
```bash
magick \
  -size 1600x2560 gradient:"#3D0F05"-"#7A2A0A" \
  [food motifs via -draw primitives] \
  [text via -font / -annotate with Korean TTF/OTF paths] \
  brisbane-mexican-cooking/cover.png
```

### Result
- File: cover.png
- Resolution: 1600x2560 px (EPUB recommended ratio 1:1.6)
- Size: ~473 KB PNG 16-bit sRGB
- Status: Success

### Notes
- Recipekorea font is thematically ideal for a cookbook — the name literally includes "recipe"
- All Korean text rendered via explicit OTF/TTF file paths (magick -list font returned empty on this system)
- Helvetica system font not accessible via name; HelveticaNeue.ttc available if needed for future versions
- If AI image generation becomes available, recommended prompt follows:

### Equivalent AI Image Generation Prompt (for future regeneration)
```
A vibrant cookbook cover in portrait format (1600x2560). 
Rich deep terracotta background (#3D0F05 to #7A2A0A gradient).
Upper area: overhead-style arrangement of authentic Mexican ingredients —
a halved avocado (top right), a lime cut to show segments (top left),
dried ancho/guajillo chili peppers hanging from center top,
fresh cilantro sprigs, a warm corn tortilla.
Center horizontal band: deep red (#B52020) with gold accent lines,
containing subtitle text.
Lower area: a corn tortilla viewed from above as circular motif,
flanked by cilantro clusters and small chili peppers.
Lime green (#6BBF4E) border stripes on all four edges.
Color palette: terracotta, salsa red, lime green, corn yellow, warm white.
Large Korean title "브리즈번 키친, 멕시코를 담다" in bold display font,
white/cream, upper portion of cover.
Subtitle "정통 멕시칸 요리, 한국인의 손맛으로" in golden yellow on red band.
Author "Toby-AI" small at bottom in golden yellow.
Modern editorial cookbook aesthetic. No Tex-Mex clichés (no yellow cheddar, 
no hard-shell tacos, no sombrero). Authentic Mexican ingredients only.
Bright Brisbane sunlight feeling — warm, vibrant, appetising.
No stock photography aesthetic.
```
