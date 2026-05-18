# Cover Design Log — 다시, C

## Version 1 (2026-05-18)

### Book Meta
- Title (KR): 다시, C
- Subtitle: Apple Silicon에서 ARM 커널까지
- Author: Toby-AI
- Slug: c-rebirth-arm
- Target reader: 옛 C 짧은 경험 → Java/JS/Python 주력 → ARM 커널 자작 목표 개발자

### Mood
- 회귀와 재발견. 차분하고 진지한 톤
- 베어메탈 손맛 + 종합 바이블의 묵직함
- 터미널/CRT 향수 (amber on black)
- 모노스페이스 친화

### Concept Candidates
- **A. Minimalism + ARM monogram** — 검정 + 큰 한글 타이틀 + 기하학적 ARM 칩 다이 모티프
- **B. Illustration** — Apple Silicon SoC 다이 + 코드 오버레이 (ImageMagick 단독으론 표현 한계)
- **C. Typography-centric (terminal nostalgia)** — 검정 배경 + 앰버 모노스페이스 컴포지션. 상단 셸 프롬프트 모티프, 중앙 큰 "다시, C", 하단 부제·저자

### Chosen Concept
**C.** ImageMagick 타이포 베이스에서 가장 강하게 작동. 대상 독자의 "회귀" 정서와도 직결 — 옛 터미널에서 다시 C를 켜는 장면.

### Visual System
- Background: pure black `#0a0a0a`
- Primary text (title): warm off-white `#f5e6cf`
- Accent (amber, terminal cursor·subtitle dot): `#ffb000`
- Secondary (subtitle, author, code lines): muted amber `#a07a3a` ~ `#d0a868`
- Frame: thin amber rule 1px @ 60% opacity, inset 90px

### Layout (1600x2560)
1. Top band (y ~ 220): mono prompt line `$ cd ~/c && ./rebirth` in dim amber
2. Big title block (y ~ 800–1400):
   - "다시," — Pretendard Black, ~360pt, off-white
   - "C" — JetBrainsMono Bold, ~640pt, amber, with a blinking cursor bar `▌` next to it
3. Divider (y ~ 1620): thin amber horizontal rule, full width minus margins
4. Subtitle (y ~ 1780–1920): "Apple Silicon에서" / "ARM 커널까지" 두 줄, Pretendard Medium, off-white, 좌측 정렬 살짝
5. Bottom band (y ~ 2280–2440):
   - 좌하: mono `// from M-series to bare metal` muted amber
   - 우하: "Toby-AI" Pretendard SemiBold, off-white, with small amber prompt `>` prefix

### ImageMagick Build Notes
- Use `magick` (IMv7), avoid deprecated `convert` warnings
- Korean glyphs → `Pretendard` family (Bold/Black for title, Medium for subtitle)
- Mono glyphs → `JetBrainsMono Nerd Font` (Bold for "C", Regular for prompt/comment lines)
- Use `-kerning` for tight title spacing
- Build via layered `-draw` + `-annotate` for precise placement
- 검증: 200×320 썸네일에서도 "다시, C" 읽힘 확인

### Prompt (English, for future image-gen MCP retry)
```
A minimalist book cover in portrait format 1600x2560.
Title in Korean "다시, C" — "다시," in warm off-white bold sans-serif
occupying upper-middle, then "C" enormous in amber monospace bold
with a blinking cursor bar next to it. Background pure black.
Top: a dim amber terminal prompt line "$ cd ~/c && ./rebirth".
Center divider: a thin amber horizontal rule. 
Subtitle below in two lines: "Apple Silicon에서" / "ARM 커널까지"
in off-white medium sans-serif.
Bottom-left: a dim amber code comment "// from M-series to bare metal".
Bottom-right: small "> Toby-AI" with a leading amber chevron.
Mood: terminal nostalgia, contemplative, serious technical bible,
amber-on-black CRT homage. No gradients, no stock photography,
no generic tech glow. Editorial, calm, confident.
```

### Result
- File: `cover.png` (final)
- Backup: `cover_v1.png` (intermediate draft with oversized text-based cursor that collided with the comma)
- Tool: ImageMagick 7.1.2 (`magick` command, IMv7)
- Resolution: 1600×2560 (PNG, 16-bit sRGB)
- Size: ~174 KB

### Adjustments made between drafts
- v1 used a text glyph `_` for the cursor at point-size 700 — it visually collided with the comma of "다시,". Replaced with an explicit `-draw rectangle` block (640,1500 → 760,1560) sized like a CRT cursor.
- Added two thin amber horizontal rules (above the title, between title block and subtitle, between body and author) for editorial grid feel.
- "ARM 커널까지" recolored amber to mirror "C" — both endpoints of the journey (the language, the kernel) glow the same color.
- Removed in-cover license stamp; license is owned by EPUB colophon / OPF `<dc:rights>` per harness v1.2.0 convention.

### How to regenerate
- Re-run the `magick` pipeline from this log (single command, no shell loops).
- If image-gen MCP becomes available, re-prompt with the English prompt block above and overwrite `cover.png` after backing up the current file to `cover_v2.png`.
