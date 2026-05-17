# Cover Design Log

## Version 1 (2026-05-17)

### Book

- 제목: 꿈꾸는 기계와 일하기
- 부제: AI 환각을 다루는 개발자의 사고법
- 저자: Toby-AI
- 대상 독자: AI agentic coding · vibe coding 개발자
- 분위기: 호기심·차분함 + 약간의 몽환 + 기술적 정확성
- 핵심 메시지: "환각은 버그가 아니라 기능이다"

### Concept

3안 검토:

- **A (미니멀)** — 인디고 배경 + 빛 입자 + 추상 노드 그래프. 차분한 기술서 톤에 부합.
- **B (일러스트)** — 잠재 공간(latent space) 구체화. 몽환적이지만 복잡할 위험.
- **C (타이포 글리치)** — 제목이 환각하는 그래픽. 강하지만 책의 차분한 톤과 충돌.

**선택: A + B 하이브리드.** 깊은 인디고~보랏빛 그라데이션 위에 빛 입자장을 깔고, 중앙에 부분적으로 흐려지는 노드 그래프(잠재 공간 시각화)를 배치. 클리셰(별, 우주, 뇌, 신경망 다이어그램, 회로 기판)는 의도적으로 회피.

### English Prompt (for image-gen models)

```
A minimalist book cover in portrait orientation, 1600x2560 pixels, 1.6:1 aspect ratio.

Background: a deep dreamlike gradient from indigo (#0e0b2e) at the top, 
through a violet midnight (#221a4a), settling into a dusty plum (#3a2a55) 
at the bottom. The gradient evokes the inside of a sleeping mind — not 
outer space. No stars.

Mid-ground: a softly glowing particle field, like dust suspended in a 
beam of light. Particles vary in size and softness, sparse near the 
edges, denser around the center. Subtle bokeh, no lens-flare cliche.

Center composition (occupying middle third): an abstract floating 
constellation of small luminous nodes connected by thin desaturated 
lines — resembling a latent space embedding, partially dissolved at 
the edges as if hallucinating into existence. Some nodes are sharp, 
some bleed into the background. Color of nodes: warm off-white with 
a faint amber glow (#f4e6c8).

Mood: contemplative, mysterious, scientific. Reads as a serious 
technical book that happens to have soul. Editorial, calm, confident.

Negative: no human faces, no brain illustration, no circuit board, 
no robot, no glowing eyes, no generic AI gradient (cyan-magenta), 
no stock photography, no neon glow, no sci-fi font.

Leave the top third clear for title typography (will be composited 
in Korean separately). Leave the bottom 200px clear for author 
attribution.
```

### Typography Plan

- 제목 "꿈꾸는 기계와 일하기": Pretendard Bold, 130pt, off-white (#f4e6c8), top third (y≈480)
- 부제 "AI 환각을 다루는 개발자의 사고법": Pretendard, 60pt, soft lavender (#b8a8d8), y≈900
- 저자 "Toby-AI": Pretendard Medium, 48pt, dim (#9a8ec0), bottom (y≈2400)
- 미세 영문 캡션 "Working with Dreaming Machines": Helvetica italic, 32pt, y≈2470

### Tool Used

- **ImageMagick 7.1.2** — 외부 image-gen API/MCP가 이 워크트리에 연결되어 있지 않다. 절차적 생성으로 진행:
  1. 인디고~플럼 그라데이션 베이스
  2. 1500개 가우시안 빛 입자를 절차적으로 spray
  3. 중앙에 노드 그래프 합성 (원 + 얇은 선)
  4. 가장자리 비네팅
  5. 한국어 타이포 합성 (Pretendard, Apple SD Gothic Neo 폴백)

### Result

- 파일: `cover.png`
- 해상도: 1600 × 2560
- 썸네일 검증: 200×320으로 축소 시 제목 가독성 확인됨

### Notes

- 외부 이미지 생성 API 사용 가능해지면 위 English Prompt로 V2 산출 추천 (DALL-E·gpt-image-1·SDXL).
- 현재 V1은 절차적 합성 — 깔끔하지만 일러스트 모델의 표현력은 없다.
- 재생성 시 입자 시드를 변경해 다양한 변형 생성 가능.

### Iteration Log

내부적으로 V1/V2/V3 변형을 시도했다:

- **V1 (seed=42, 채택)** — 1500개 작은 입자 + 22개 노드. 별빛 우주처럼 보이는 면이 있지만 "잠재 공간의 점들"로 읽힌다. 중앙 노드 그래프가 명확히 도드라지고 부제도 잘 보인다.
- V2 (seed=73, 폐기) — 입자 크기를 키워 보케화. "꿈속 먼지" 의도였으나 수중 거품처럼 보였다.
- V3 (seed=108, 폐기) — 중앙 글로우 강화. 부제를 가리고 보케 디스크가 과했다.

최종 채택: **V1**. 파일 시드 42 보존 (재생성 시 결정성 유지).
