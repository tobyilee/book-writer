# Cover Design Log

## Version 1 (2026-07-26)

- Concept: **A (미니멀리즘)** — 심볼(단일 궤적) + 큰 타이포. tech-book 톤에 맞춰 3안 중 A 채택.
  - A안(채택): 단일 점이 경로를 따라 흐르다 여러 갈래로 퍼지는 궤적 + 절제된 타이포
  - B안(기각): 파이프라인 다이어그램형 일러스트(수집→스트림→저장→세그먼트 아이콘 나열) — 벤더 인포그래픽처럼 보일 위험이 커서 기각
  - C안(기각): 타이포그래피 단독(심볼 없음) — 이 책의 핵심 은유(이벤트 하나 → 파이프라인 → 메시지들)를 시각적으로 못 살려서 기각
- Tool: **hybrid** — 배경/그래픽은 `gpt-image-bridge` (gpt-image-2, codex CLI 경유)로 생성, 한글 타이포는 ImageMagick으로 별도 합성
  - 이유: gpt-image-2에게 한글 텍스트를 직접 그리게 하면 글자가 깨질 위험이 커서, 텍스트 없는 배경만 생성하고 제목·부제·저자명은 로컬 폰트 렌더링으로 확정 처리했다.
- Background prompt (English, gpt-image-2, size 1024x1536):
  ```
  Minimalist editorial book cover background illustration, portrait orientation,
  aspect ratio 1600x2560 (5:8), no text anywhere in the image. Deep charcoal-navy
  background (#12141c to #1a1e2b), flat and restrained, almost matte -- not a
  glossy 3D render, not a gradient wallpaper. Composition: in the lower two-thirds
  of the frame, a single thin luminous line begins as one clean point of light near
  the bottom-center and traces a calm, deliberate path upward -- like a single data
  event moving through a pipeline. Partway up, that single line passes through
  three small, precise geometric nodes (thin-stroke circles, not glowing orbs, not
  spheres) and then divides into several thinner branching lines that fan out
  gently toward the upper portion of the frame, like a signal fanning out into
  multiple downstream messages. The branching lines fade in opacity as they reach
  the top, leaving the upper third of the composition mostly clear, dark, and
  empty -- deliberately reserved negative space for large title typography to be
  added later. Line and node color: a single restrained accent -- muted amber-gold
  (#c9973f) or cool cyan-teal (#4fb3bf), used sparingly, thin 1-2px linework, no
  thick shapes. Style: precise technical-editorial illustration, like a diagram in
  a serious systems engineering book -- flat vector-adjacent linework, subtle grain
  texture, no cheesy stock-photo aesthetic, no generic tech gradient, no bokeh, no
  lens flare, no glossy 3D rendering, no exaggerated glow, no human figures, no
  icons of megaphones, crowds, or upward arrows, no bright saturated marketing
  colors. Mood: calm, precise, trustworthy, quietly confident -- the visual
  opposite of a marketing brochure.
  ```
- Post-processing (ImageMagick, `magick`):
  1. `-resize 1600x2400 -gravity center -background "rgb(8,14,28)" -extent 1600x2560` — 1024×1536 원본을 1600×2560으로 확대·캔버스 보정 (배경이 균일한 짙은 남색이라 이음매 없이 확장됨)
  2. 한글 폰트: `/System/Library/Fonts/AppleSDGothicNeo.ttc`를 `fontTools`로 Bold(index 6)·Medium(index 2) 페이스를 개별 `.ttf`로 추출해 사용 (ImageMagick 7 빌드에 fontconfig 딜리게이트가 없어 페이스명으로 직접 지정 불가 — 파일 경로 방식만 동작)
  3. 제목 "이벤트 하나가 / 캠페인이 되기까지" — Bold, 118pt, `#f4f1ea`(따뜻한 오프화이트), 상단 정렬
  4. 부제 "Martech 회사로 가는 개발자를 위한 안내서" — Medium, 46pt, `#c9973f`(궤적과 동일한 앰버 골드로 통일)
  5. 저자 "Toby-AI" — Medium, 42pt, `#9aa0ad`(중성 그레이), 하단 중앙
- Result: `cover.png` (1600×2560, PNG, ~3.2MB)
- Notes:
  - 200×320 썸네일로 축소해도 제목·부제 모두 가독 확인 완료
  - 확성기·군중 아이콘·상승 화살표·밝은 그라데이션·과장된 3D 렌더링 전부 회피
  - 궤적의 골드와 부제 색을 동일 계열로 통일해 "벤더 마케팅 문구가 아니라 근거를 다루는 책"이라는 논지와 시각적으로 상충하지 않도록 했다
