# Cover Design Log

## Version 1 (2026-11-03)
- Concept: A (minimal — large typography + one symbol), with a customer-journey motif
- Tool: Pillow (via `uv run --with pillow`) programmatic typography — no image-gen MCP/API and no ImageMagick installed in this environment
- Fallback: yes (typography cover instead of generated illustration)
- Font: Malgun Gothic Bold/Regular (`/mnt/c/Windows/Fonts/malgunbd.ttf`, `malgun.ttf`)
- Palette: warm off-white #F6F3EC background, deep navy #162240 type, coral / teal / amber channel branches, blue goal ring
- Layout: coral accent bar → 3-line title (upper third) → subtitle "보내기 전에 설계하라" → journey graphic (entry node → split node → three channel branches: push(phone), email(envelope), in-app/message(chat) → converging goal node with check) → dashed grey "not sent / holdout" line → thin rule + "Toby-AI"
- No Braze / Insider One logos or brand marks.
- Equivalent image-gen prompt (for a future regeneration if a model is available):
  ```
  A clean modern minimalist book cover, portrait 1600x2560. Warm off-white background.
  Upper third: large bold sans-serif Korean title in deep navy. Lower half: an abstract
  customer-journey diagram — one entry node splitting into three smooth curved paths in
  coral, teal and amber, each passing through a small circular node with a simple white
  channel icon (phone, envelope, chat bubble), converging into a navy goal node with a
  check mark. A faint dashed grey line below suggests a holdout group. Flat vector,
  generous whitespace, approachable not technical. No logos, no brand marks, no stock
  photography, no generic tech gradient. Small author name "Toby-AI" bottom-left.
  ```
- Script: `cover_make.py` (rerun: `uv run --with pillow python cover_make.py cover.png thumb.png`)
- Result: cover.png (1600x2560), thumbnail check at 200x320 — title legible
