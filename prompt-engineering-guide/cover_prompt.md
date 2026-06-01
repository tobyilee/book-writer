# Cover Design Log

## Version 1 (2026-06-01)

### Concept Selected: A — Minimalist

**Three concepts considered:**
- A: Minimalist — deep navy background, abstract A-vs-B balance/scale symbol, bold Korean typography
- B: Illustration — two prompt chat bubbles flanking a glowing measurement scale
- C: Typography-centric — title split layout (좋은 / 더 나은) with grid-line background texture

**Selection rationale:** Concept A best fits the calm, methodological tone for a tech book targeting general users through developers. The balance/scale motif directly expresses the "eval / comparison" core identity without being overwrought.

---

### Design Spec

| Element | Value |
|---------|-------|
| Canvas | 1600 × 2560 px (EPUB portrait 1:1.6) |
| Background | Deep navy gradient #0a0f23 → #1c1353 |
| Accent color | Indigo-violet #7864DC / #A08FFF |
| Title font | Apple SD Gothic Neo Bold (110pt) |
| Subtitle font | Apple SD Gothic Neo (38pt / 32pt) |
| Author font | Apple SD Gothic Neo (44pt) |
| Tool | Python Pillow (custom render) |

### Central Motif

Abstract evaluation balance scale:
- Horizontal beam in indigo-violet
- Left pan: Card "A" (좋은 프롬프트) — slightly lower
- Right pan: Card "B" (더 나은 프롬프트) — elevated, "winning"
- Fulcrum triangle beneath beam
- Three small dots below fulcrum (eval pipeline metaphor)

---

### Equivalent Image Generation Prompt (English, for MCP/API re-generation)

```
A minimalist book cover, portrait format 1600x2560px.
Deep navy to dark indigo gradient background (#0a0f23 to #1a1040).
Center: an abstract precision balance scale with two floating rectangular 
prompt-cards labeled "A" (left, slightly lower) and "B" (right, elevated) — 
rendered in indigo violet lines, subtle glow. The scale symbolizes 
AI prompt evaluation and comparison.
Top third: Korean title "좋은 프롬프트," (light lavender, 110pt bold) 
on line one, "더 나은 프롬프트" (pure white, 110pt bold) on line two.
Below title: subtitle "작성부터 평가까지" in muted violet, 
then "Claude Opus 4.8 · GPT-5.5 · Gemini 3.5 Flash 시대" in smaller text.
Bottom center: "Toby-AI" author attribution in soft lavender.
Thin horizontal accent lines at top and bottom.
Editorial, calm, confident, modern tech. No stock photography. 
No generic gradient blobs. No clipart.
```

---

### Result

- Output: `cover.png`
- Resolution: 1600 × 2560 (verified)
- Korean text: Rendered cleanly via Apple SD Gothic Neo (system font, Pillow TrueType)
- Author: Toby-AI (center-bottom)
- Notes: Clean render; Korean glyphs confirmed via fc-list + Pillow TrueType path

---

## Re-generation Notes

- To regenerate: back up `cover.png` → `cover_v1.png`, rerun script or use prompt above with image MCP
- To change concept: switch to B (illustration) or C (typography) per skill guide
- For MCP image generation: feed English prompt above to `gpt-image-1` or equivalent
