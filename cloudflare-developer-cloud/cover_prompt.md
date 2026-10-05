# Cover Design Log

## Version 1 (2026-10-03)
- Concept: A (minimalism: one symbol and large type), the recommended concept for a calm tech book
- Tool: typography fallback. No image-gen MCP, no `OPENAI_API_KEY`, and ImageMagick is not installed, so the cover was laid out as HTML/SVG (`cover_source.html`) and rendered to a 1600x2560 PNG with headless Google Chrome.
- Font: Apple SD Gothic Neo (system CJK font). The Korean title renders correctly.
- Design:
  - Background: deep navy radial gradient (#16304a to #0b1522)
  - Title: "Cloudflare를 / 나의 클라우드로", 168px ExtraBold, white, top third, with a short teal accent rule above it
  - Subtitle: "정적 사이트부터 Spring 백엔드까지, / 무료로 시작해 안전하게 운영하기", 56px, muted blue
  - Motif: a wireframe globe with edge nodes and links (the global edge network), three concentric teal rings (layers of protection) around a nested gold square at the center (the developer's own service growing from a small site)
  - Author: "Toby-AI", small and centered at the bottom
  - No Cloudflare logo, orange cloud, or brand colors. The palette is teal, navy, and gold.
- Equivalent image-gen prompt (for a later regeneration if an image tool becomes available):
  ```
  A minimalist book cover in portrait format (1600x2560). Deep navy background
  with a subtle radial glow. Lower two-thirds: an abstract wireframe globe made of
  thin latitude/longitude lines, scattered glowing teal edge nodes connected by
  fine lines, and three concentric translucent teal rings around a small nested
  gold square at the center, suggesting a personal service protected by layers
  on a global edge network. Top third left empty for the title typography.
  Calm, trustworthy, editorial. No logos, no orange cloud, no brand marks,
  no stock photography, no generic tech gradient, no text.
  ```
  (Overlay the Korean title, subtitle, and author afterward. Image models should not render Korean text.)
- Regenerate: edit `cover_source.html`, then run headless Chrome:
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --force-device-scale-factor=1 --window-size=1600,2560 --virtual-time-budget=2000 --screenshot=cover.png file://$PWD/cover_source.html`
- Result: cover.png (1600x2560). The title stays readable at a 200x320 thumbnail.
- Notes: none
