# Cover Design Log — LLM 내부로 들어가기

## Version 1 (2026-04-17)

- **Book:** LLM 내부로 들어가기 — 백엔드 개발자를 위한 한 걸음씩 입문
- **Author:** Toby-AI
- **Concept:** A — Minimalist geometric illustration
  (considered: B illustrated journey-map, C typography-only — rejected in favor of A because the brief asked for "차분한 안내자 톤 + 교과서·인문 에세이에 가까운 품위")
- **Tool used:** Python/Pillow (no AI image-gen MCP available; used programmatic vector-style drawing + precise Korean typography). This avoids the "glossy AI aesthetic" pitfall the brief called out.
- **Why not AI image gen:** Most gen models render Korean hangul poorly and trend toward cyberpunk tech aesthetics for LLM-adjacent prompts. Typography-controlled PIL rendering produces cleaner, more academic results and guarantees the Korean title is exactly correct.

### Dimensions & output
- `cover.png` — 1600×2560, PNG, 87 KB
- Thumbnail `cover_thumb.png` — 200×320, title still readable

### Color palette
- Background: vertical gradient from `#1a2332` (midnight navy) → `#2d3e50` (slate blue)
- Primary ink: `#f5e6c8` (warm off-white / soft amber)
- Dim ink: `#c8b896` (for subtitle, captions)
- Faint ink: `#6e7887` (for traces, decorative lines)

### Typography
- Title — **AppleMyungjo** (serif hangul), 200pt, 2-line horizontal layout
  - Line 1: `LLM 내부로`
  - Line 2: `들어가기`
- Subtitle — **Noto Sans KR Regular**, 62pt: `백엔드 개발자를 위한 한 걸음씩 입문`
- Tag (top) — Noto Sans KR, 34pt, letter-spaced: `BACKEND DEVELOPER SERIES`
- Author — Times New Roman Italic, 52pt, bottom-right: `Toby-AI`
- Year — Noto Sans KR, 36pt, bottom-left: `2026`
- Caption under illustration — `· a gentle path into the black box ·`, 36pt

### Illustration
Minimal line-art of a half-opened box (front face + trapezoidal lid tilted back), with six hollow circles of varying size ascending — representing tokens emerging from the container. A faint dotted trajectory suggests the "path emerging from inside". Stroke weight 3–6 px, all in warm off-white.

### Equivalent English prompt (for future AI-image regeneration)
```
A minimalist book cover, portrait 1600x2560. Dark navy background
(#1a2332 to #2d3e50 gradient). Center-lower: a single abstract
line-art illustration of a box with its lid opening upward, and
six hollow dots of varying size ascending from it (suggesting
tokens emerging). All illustration strokes in warm off-white
(#f5e6c8). Upper third: clean Korean serif title "LLM 내부로 /
들어가기" in two lines, followed by a thin horizontal rule and a
sans-serif subtitle "백엔드 개발자를 위한 한 걸음씩 입문".
Bottom-right: "Toby-AI" in small italic serif. Bottom-left: "2026".
Top: small caps label "BACKEND DEVELOPER SERIES" flanked by short
rules. Calm, humanistic, early-20th-century academic book cover
mood. Morandi palette. NOT cyberpunk, NOT glossy AI aesthetic,
NOT generic tech gradient. NO stock photography.
```

### Verification checklist
- [x] Resolution ≥ 1600×2560 — exact
- [x] Thumbnail 200×320 — title "LLM 내부로 들어가기" still readable
- [x] Author `Toby-AI` present on cover (bottom-right)
- [x] Korean title renders correctly (hangul ligatures intact)
- [x] Mood: textbook/humanistic — not cyberpunk or gradient-tech
- [x] Illustration reads as "opening box + emerging tokens" metaphor

### Regeneration script
`make_cover.py` in this directory. Edit colors/font sizes/illustration scale and re-run:
```
python3 /Users/tobylee/workspace/ai/book-writer/_workspace/llm-intro/make_cover.py
```
