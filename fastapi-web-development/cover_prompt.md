# Cover Design Log

## Concept selection

3 concepts considered per cover-design skill:
- **A. 미니멀리즘** — 심볼 하나(스레드 그리드 → 이벤트 루프로 흐르는 추상 기하) + 큰 타이포
- **B. 일러스트형** — 문자적 "다리/화살표" 은유 (기각 — 브리프에서 진부하다고 명시적으로 배제)
- **C. 타이포그래피 중심** — 제목 자체가 그래픽, 배경은 단순 그라디언트만

**채택: A + C 혼합.** 제목 가독성이 최우선이라는 요구(서점 썸네일 200px에서도 읽혀야 함) 때문에 순수 일러스트(B)는 배제. 대신 미니멀한 추상 심볼(A)을 배경 그래픽으로 깔고, 그 위에 굵은 타이포그래피(C)를 얹는 방식으로 두 콘셉트를 결합. 한글 렌더링 실패 위험 때문에 이미지 생성 모델에는 텍스트를 전혀 요청하지 않고, 배경 아트워크만 생성 후 ImageMagick으로 타이포를 직접 합성하는 2단계 파이프라인을 사용.

## Version 1 (2026-07-26)

- **Concept:** A(미니멀 추상 심볼) + C(타이포그래피) 결합, 텍스트/그래픽 분리 파이프라인
- **Tool:** `gpt-image-bridge` (codex CLI → gpt-image-2)로 배경 생성 + ImageMagick으로 텍스트 합성
- **배경 생성 프롬프트 (영어, 텍스트 없음 명시):**
  ```
  Abstract modernist book cover background, portrait orientation, no text,
  no letters, no words, no logos. Deep dark navy-to-charcoal gradient
  background (#0d1321 to #1a2332). Center-left: a geometric visual metaphor
  for transitioning from a synchronous threaded model to an asynchronous
  event loop — on the left side, a rigid grid of small solid squares stacked
  in straight parallel columns (representing threads/blocking calls),
  rendered in muted cool gray. On the right side, the same squares dissolve
  and reform into a single flowing continuous curved ribbon or orbit-like
  loop made of teal and cyan gradient light (#2dd4bf to #22d3ee), suggesting
  concurrency and non-blocking flow. The transition between the two happens
  through gradual deformation, not a literal bridge or arrow — the grid
  particles stretch, thin out, and merge into the glowing loop line.
  Composition leaves generous empty negative space in the upper third and
  lower fifth of the frame for large typography to be added later. Fine
  subtle grain texture, soft rim lighting, editorial tech-publishing
  aesthetic, high contrast, serious and confident mood — not playful, not
  cartoonish. No FastAPI logo, no Python logo, no Spring logo, no
  recognizable brand marks. No literal bridge, no literal arrow, no
  stock-photo elements. Portrait aspect ratio close to 1600x2560.
  ```
  (생성 크기 1024x1536 → `magick -resize 1600x2560^ -gravity center -extent 1600x2560`로 크롭/스케일)

- **텍스트 합성 (ImageMagick, 폰트 `/System/Library/Fonts/AppleSDGothicNeo.ttc`):**
  - 제목 (3줄, weight 900, pointsize 122, white, North gravity, +150/+290/+430): "이미 웹을 아는" / "개발자를 위한" / "FastAPI"
  - 부제 (2줄, weight 500, pointsize 50, `#a9d6d0`, South gravity, +680/+610): "Spring Boot·Express에서 건너온" / "사람들의 실전 안내서"
  - 저자 (weight 400, pointsize 42, `#e8e8e8`, South gravity, +180): "Toby-AI"

- **Result:** `cover.png` (1600x2560, ~3.9MB)
- **Notes:**
  - 배경 생성 1회로 원하는 결과(그리드 → 흐르는 루프로 자연스럽게 용해되는 구도, 문자적 다리/화살표 없음) 획득 — 재시도 불필요.
  - 한글 렌더링: ImageMagick + AppleSDGothicNeo 조합으로 완벽하게 렌더링됨 (이미지 생성 모델에는 텍스트를 아예 요청하지 않아 뭉개짐 리스크 원천 차단).
  - 200x320 썸네일 축소 확인 결과 제목 3줄 모두 선명하게 읽힘.
  - 그리드(스레드 모델)와 발광 루프(이벤트 루프)가 화면 중앙~하단부에 위치해 상단 제목·하단 부제/저자 텍스트 영역과 겹치지 않음.
