# Cover Design Log — 『결어긋남』 (Decoherence)

## Version 1 (2026-04-20)

### Concept
- **Selected:** Concept A — Minimalist typography hybrid.
- **Rejected B (illustration-heavy):** Risk of clichéd humanoid-AI silhouettes.
- **Rejected C (pure typography):** Loses the scientific apparatus cue that signals hard SF.

### Design rationale
- Deep midnight navy (#0a1226) → black vertical gradient background as a quantum vacuum / cryo chamber backdrop.
- A single faint **sinusoidal wavefunction** crossing the upper middle band, its right half fading into stochastic noise dots — the visual moment of coherence collapsing into decoherence.
- A barely-visible **Bloch sphere wireframe** (ellipse + meridian) ghosted behind the title, representing a qubit in superposition.
- **Title '결어긋남'** set in AppleMyungjo (serif/명조) at large size, center-upper. The middle glyph '어' is shifted by a few pixels on both x and y axes and rendered in slightly dimmer ink — the title literally "dis-aligns" (어긋난다).
- A subtle cyan glow (#5ec8c7) only on the shifted glyph, marking it as the "decohered" element.
- **Subtitle 'DECOHERENCE'** in small, wide-tracked sans (Apple SD Gothic Neo Light) below title — roughly 1/4 the title size.
- **Author 'Toby-AI'** in small monospace-feeling sans at bottom center.
- Single amber hot pixel (#ffb347) near the wave — the "observer" point.

### Color palette
| Role | Hex |
|---|---|
| Background top | #0a1226 (deep navy) |
| Background bottom | #05070f (near-black) |
| Title ink primary | #e8ecf2 (pale bone) |
| Title decohered glyph | #5ec8c7 (pale cyan glow) |
| Subtitle | #7a8ca3 (cool grey) |
| Author | #9fb0c4 |
| Observer hot point | #ffb347 (amber) |
| Wave / sphere wireframe | #2a4a6e → #5ec8c7 at glow |

### Generation method
- **Primary attempt:** image-generation MCP — *not available in this environment.*
- **Fallback (used):** ImageMagick 7.1.2 procedural composition. Chosen because procedural draw guarantees precise control over the "어" glyph offset, avoids generative-AI clichés (no humanoid, no HAL eye, no blockchain nodes), and ships crisp typography.

### ImageMagick command (1600×2560 PNG)

```bash
magick -size 1600x2560 \
  gradient:'#0a1226-#05070f' \
  \( -size 1600x2560 xc:none -fill '#5ec8c7' \
     -draw "circle 800,900 800,880" -blur 0x80 -evaluate multiply 0.18 \) \
  -compose screen -composite \
  \( -size 1600x2560 xc:none -stroke '#2a4a6e' -strokewidth 2 -fill none \
     -draw "ellipse 800,900 420,420 0,360" \
     -draw "ellipse 800,900 420,150 0,360" \
     -draw "line 380,900 1220,900" \
     -draw "line 800,480 800,1320" \) \
  -compose over -composite \
  # ... (wavefunction polyline + decoherence noise + title + offset glyph + amber dot + subtitle + author)
```

Full command is executed by cover-designer agent; see build transcript.

### Output
- File: `cover.png`
- Size: 1600 × 2560
- Format: PNG, sRGB

### Notes / follow-ups
- If a future pass has access to a generative image model, revisit with: *"Minimalist hard-SF book cover, portrait 1600x2560, deep midnight-navy to black gradient, faint Bloch sphere wireframe centered, a sinusoidal wavefunction collapsing into sparse dots on its right side, a single amber observer point, Korean serif title '결어긋남' centered upper with the middle character slightly offset and glowing cyan, small wide-tracked subtitle 'DECOHERENCE', small author 'Toby-AI' bottom. No humanoid figures, no red-eye AI, no generic circuit-brain cliché, no stock gradient."*
