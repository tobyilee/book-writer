---
generated: 2026-06-10
tool: ImageMagick 7 (typography + vector fallback)
output: cover.png (1600x2560)
---

# 표지 생성 기록 — 네 겹의 엔지니어링

## 콘셉트 후보 3안

1. **동심원 + 미니멀 타이포 (채택)** — 딥 네이비 배경, 틸 계열 동심원 4겹(Prompt → Context → Harness → Loop), 한글 Heavy 타이포. 책의 핵심 은유(줌 레벨)를 시각적으로 직결.
2. **레이어드 그라디언트** — 4색 그라디언트 밴드로 겹을 표현, 텍스트 오버레이. 더 화려하지만 의미 전달이 약함.
3. **코드 배경 타이포** — 희미한 코드 텍스처 위에 대형 제목. 전형적 tech-book 패턴, 차별성 낮음.

## 채택 콘셉트 상세 (1안)

- **배경:** `#0d1b2a` (딥 네이비)
- **동심원 4겹:** 가장 바깥(Loop) → `#0f3d4d`, Harness → `#134f61`, Context → `#176175`, Prompt(내부) → `#1b7389`; 각 링 hairline accent `#26a3b4` (틸)
- **중심 dot:** `#26a3b4` 솔리드 원 — 프롬프트의 핵으로 포인트
- **링 라벨:** LOOP / HARNESS / CONTEXT / PROMPT — 소형 틸 텍스트로 각 원 우측 표기
- **제목:** Apple SD Gothic Neo Heavy, 110pt, 흰색 — 2행 분리 (`네 겹의` / `엔지니어링`)
- **부제:** 44pt, `#8ecdd8` (연한 틸) — 2행
- **저자:** 48pt, `#8ecdd8` — 하단
- **액센트 바:** 틸 수평선 (상단 200px, 하단 2310px)
- **폰트:** `/System/Library/Fonts/AppleSDGothicNeo.ttc`

## 재현 명령 (단축)

```bash
magick -size 1600x2560 xc:"#0d1b2a" \
  [동심원 4겹 + hairline] \
  [링 라벨] \
  [제목/부제/저자 텍스트] \
  agentic-coding-engineering/cover.png
```

## cover_alt

`네 겹의 엔지니어링 표지` — book_manifest.json의 cover_alt 필드와 동일.
