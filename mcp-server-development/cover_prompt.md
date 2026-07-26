# Cover Design Log

## 콘셉트 검토

- **A: 미니멀리즘** — 심볼 하나(프로토콜 연결 다이어그램) + 큰 타이포. **채택.**
- **B: 일러스트형** — 서버/클라이언트를 구상적으로 그린 장면. 실전 기술서 톤에는 과함 → 기각.
- **C: 타이포그래피 중심** — 제목 자체를 그래픽화. 부제가 길어(TypeScript·Python·Java로 만들고...) 가독성 리스크 → 기각.

추천안: **A (미니멀리즘)** — 차분한 딥 네이비→틸 그라디언트 배경에, 세 언어(TypeScript/Python/Java)가 하나의 중심 노드(MCP 서버/프로토콜 핸드셰이크)로 연결되는 추상 기하학 심볼. 실무 개발자 대상 신뢰감 있는 기술서 톤에 부합.

## Version 1 (2026-07-26)

- Concept: A (미니멀리즘, 프로토콜/연결 모티프)
- Tool: **하이브리드** — (1) `gpt-image-bridge` (codex CLI → gpt-image-2)로 텍스트 없는 배경 아트 생성 → (2) ImageMagick으로 한글 타이포 오버레이 합성
  - 이유: 이미지 생성 모델이 한글 텍스트 렌더링에 취약(깨짐 위험) → 배경은 AI가, 타이포는 정밀 제어 가능한 ImageMagick이 맡는 분업 구조 채택

### Step 1 — 배경 아트 생성 프롬프트 (영어, gpt-image-2)

```
A minimalist modernist book-cover background illustration in portrait
orientation. Deep navy-to-teal gradient background (#12172b at top
transitioning to #0d3b3e at bottom). Central motif occupying the middle
third: an abstract geometric network diagram — three small hexagonal
nodes arranged in a loose triangle, each connected by a thin glowing
cyan-teal line converging into one larger central circular node, evoking
a protocol handshake between a client and a server. Clean precise
vector-style linework with a subtle soft glow, quiet confident engineering
aesthetic, editorial and calm, not busy. Generous empty negative space in
the top third of the frame and in the bottom sixth, reserved for
typography to be added later. Absolutely no text, no letters, no numbers,
no logos, no watermarks anywhere in the image. No stock photography, no
generic gradient mesh, no clichéd circuit-board texture, no glossy 3D
render, no lens flare.
```

- 출력: 1024x1536 → 이후 1600x2560으로 리사이즈

### Step 2 — 타이포 오버레이 (ImageMagick)

```bash
FONT="/System/Library/Fonts/AppleSDGothicNeo.ttc"

convert mcp_bg.png -resize 1600x2560! bg_resized.png

convert bg_resized.png \
  -font "$FONT" -gravity North \
  -fill white -pointsize 118 -annotate +0+150 "MCP 서버 개발 실전" \
  -fill "#a9dfe6" -pointsize 44 -annotate +0+430 "TypeScript · Python · Java로 만들고" \
  -fill "#a9dfe6" -pointsize 44 -annotate +0+500 "Claude Code에 붙이기" \
  -gravity South -fill white -pointsize 46 -annotate +0+140 "Toby-AI" \
  cover.png
```

- Result: `cover.png` (1600x2560)
- Notes:
  - 세 개의 육각 노드(TypeScript/Python/Java)가 중앙 원(MCP 서버)으로 수렴하는 구도로 "세 언어로 같은 서버를 만든다"는 책의 핵심 개념을 시각적으로 반영
  - 썸네일(200x320) 검증 결과 제목·부제·저자명 모두 가독성 확보
  - 클리셰(스톡사진, 범용 그라디언트, 회로기판 텍스처) 회피 확인
  - 저자명 "Toby-AI" 이미지 내 직접 렌더링 완료 (플레이스홀더 아님)
