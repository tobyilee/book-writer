# Cover Prompt — 에이전틱 코딩의 시대

## 콘셉트 후보 (3안)

### A. 격자 위의 흐름 (선정)
어둡고 깊은 네이비 캔버스 위에 미세한 기하학적 그리드가 깔리고, 그 위로 따뜻한 골드 곡선들이 격자를 가로지른다. 격자는 통제·구조·하네스, 곡선은 모델의 자유로운 추론·데이터 흐름을 상징한다. 둘이 충돌하지 않고 정합한다는 점이 핵심.

### B. 노드 토폴로지
점과 선으로 구성된 에이전트 그래프. 중심에 큰 노드(모델), 주변에 작은 노드들(서브에이전트·툴·체크포인트). 가장자리는 흐릿하게 사라진다. 너무 흔한 시각이라 후순위.

### C. 미니멀 타이포 + 단일 심볼
배경은 차콜 단색. 중앙에 골드 굴레 형상의 추상화된 곡선 한 줄. 상하단 여백 최대화. 가장 안전하지만 보수적.

→ A안을 채택. 무게감 있으면서도 “통제와 자유의 균형”이라는 책의 테제를 시각으로 옮긴다.

## 영어 Image Generation Prompt (gpt-image-1 / DALL-E 3 / Midjourney 호환)

```
A premium technical book cover, portrait orientation 1600x2560, deep navy background (#0A1628) with subtle vignette toward the edges. The lower two-thirds of the canvas is filled with an abstract geometric composition: a fine, precise grid of thin lines in muted slate-blue, like architectural blueprint or engineering schematic, occupying the lower half. Across this grid, several flowing organic curves sweep diagonally — warm gold (#D4A574) and a single hint of coral (#E07A5F) — translucent, with soft glow, suggesting harnessed flow of energy or data being guided. The curves cross the grid intersections at natural points, never breaking the grid but interacting with it, evoking equilibrium between control and freedom. No human figures. No literal horse imagery. No mascots, no cartoon, no AI slop. Composition leaves clean negative space in the upper third for typography (will be added in post). Style: minimal, sophisticated, scholarly — the visual language of "Designing Data-Intensive Applications", "The Pragmatic Programmer", "SICP". Texture: matte paper feel, slight grain. Mood: serious, future-leaning, weighty. High contrast between dark navy and warm gold. No text in the image.
```

## 타이포 레이아웃 (PIL post-process)

- 상단 카피: "프롬프트의 시대는 끝났다. 이제 하네스를 설계하라." — Pretendard Light, 코랄 톤, 작게.
- 메인 제목: "에이전틱 코딩의 시대" — Pretendard Black, 화이트, 큰 사이즈, 상단 1/3.
- 부제: "모델을 통제하는 하네스 엔지니어링" — Pretendard Medium, 옅은 슬레이트, 제목 바로 아래.
- 영문 부제: "The Age of Agentic Coding — Engineering the Harness That Tames the Model" — Pretendard Light, 골드, 한 줄.
- 저자: "Toby-AI" — Pretendard SemiBold, 골드, 하단 중앙.

## 폴백 (실제 사용한 방법)

이미지 생성 MCP가 환경에 없어 PIL(Pillow 12.0.0)로 직접 그래픽을 합성했다. 격자 + 베지어 곡선 + 비네트를 코드로 구성하고, Pretendard 패밀리로 타이포를 얹었다. 폰트 경로는 `~/Library/Fonts/Pretendard-*.otf`.

재생성 방법:

```bash
cd agentic-coding-harness-engineering && python3 _make_cover.py
```

기존 `cover.png`가 있으면 자동으로 `cover_v1.png`(이후 `v2`, `v3`...)로 백업한 뒤 새 표지를 쓴다. A/B 테스트하려면 `_make_cover.py`의 곡선 배열·색·타이포 값을 수정하면 된다.
