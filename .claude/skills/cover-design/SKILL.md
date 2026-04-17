---
name: cover-design
description: Generate a book cover image (1600x2560 PNG) based on title, topic mood, and target audience. Craft image generation prompts in English, use available image-gen MCPs or APIs, fallback to ImageMagick typography. Use when creating, revising, or A/B testing book covers. Author attribution is always Toby-AI.
---

# Cover Design

책의 표지 이미지를 설계·생성한다. 결과는 `_workspace/{slug}/cover.png` (1600×2560 권장) + 재생성용 프롬프트 기록.

## 절차

1. **입력 확인** — 책 제목, 부제(있으면), 주제 분위기, 대상 독자
2. **콘셉트 3안 구상**
   - A: 미니멀리즘 — 심볼 하나 + 큰 타이포
   - B: 일러스트형 — 주제 메타포 이미지
   - C: 타이포그래피 중심 — 제목 자체가 그래픽
3. **추천안 선택** — 주제 톤·대상 독자에 가장 맞는 1안
4. **프롬프트 작성** — 영어 프롬프트 권장 (이미지 모델 대부분 영어 최적화)
5. **이미지 생성** — 사용 가능한 도구 순서로 시도
6. **결과 검증** — 해상도, 구도, 제목 가독성 확인
7. **저장** — `cover.png` + `cover_prompt.md`

## 콘셉트 선택 가이드

| 주제 톤 | 추천 콘셉트 |
|---------|------------|
| 차분한 기술서 | A (미니멀리즘, 차분한 색조) |
| 철학·에세이형 | C (타이포그래피, 따뜻한 색) |
| 실전 튜토리얼 | B (일러스트, 선명한 색) |
| 심화·이론서 | A (미니멀, 깊이 있는 색) |

## 프롬프트 작성 원칙

- 스타일 지정: "minimalist book cover", "editorial illustration", "modernist typography"
- 색상 톤: "warm muted palette", "deep blue and gold"
- 분위기: "contemplative", "bold", "serene"
- 구도: "title prominent in upper third, small author attribution at bottom"
- 제외: "no cheesy stock photo aesthetic", "no generic tech gradient"
- 해상도·비율: "portrait orientation, 1.6:1 aspect ratio"

**예시 프롬프트:**
```
A minimalist book cover in portrait format (1600x2560). 
Title "효과적인 SQL 쿼리 튜닝" in bold modern sans-serif 
occupying the top third. Center: a single abstract symbol 
resembling an interconnected graph in deep indigo. 
Background: warm off-white. Bottom-right: "Toby-AI" 
in small elegant serif. Editorial, calm, confident. 
No stock photography. No generic tech gradient.
```

## 이미지 생성 도구 우선순위

1. **이미지 생성 MCP** (설치되어 있으면) — 가장 선호
2. **외부 API** — OpenAI `gpt-image-1`, Stability SDXL 등 (사용자 API 키 필요)
3. **ImageMagick 폴백** — 단순 타이포그래피 플레이스홀더

## ImageMagick 폴백 명령

```bash
convert -size 1600x2560 \
  -gradient '#1a1a2e-#2d1b4e' \
  -gravity center -font 'Apple-SD-Gothic-Neo' -pointsize 120 -fill white \
  -annotate +0-400 "{책 제목}" \
  -pointsize 70 -fill '#c9b8d8' -annotate +0+600 "{부제}" \
  -pointsize 50 -fill white -annotate +0+1000 "Toby-AI" \
  _workspace/{slug}/cover.png
```

폰트가 없으면 `-font Helvetica` 또는 시스템 기본 폰트 사용.

## 검증 체크

- [ ] 해상도 ≥ 1600×2560
- [ ] 썸네일(200×320)로 축소해도 제목 읽힘
- [ ] `Toby-AI` 저자 표기 존재 (이미지 안 또는 메타데이터 예정)
- [ ] 클리셰 회피 (기본 그라데이션, 스톡사진 느낌 없음)

## 프롬프트 기록

`cover_prompt.md`:

```markdown
# Cover Design Log

## Version 1 (YYYY-MM-DD)
- Concept: {A/B/C}
- Tool: {mcp / api / imagemagick}
- Prompt:
  ```
  ...
  ```
- Result: cover.png
- Notes: {성공/조정 필요 부분}

## Version 2 ...
```

## 실패 대응

- 이미지 API 실패 → ImageMagick 폴백
- ImageMagick 미설치 → 오케스트레이터에 `brew install imagemagick` 지시 요청, 임시로 단색 PNG 생성
- 생성 결과가 클리셰이거나 제목이 잘 안 보임 → 프롬프트 구체화 (색상·구도 강화) 후 재시도

## 재생성 시

- 이전 `cover.png`를 `cover_v{N}.png`로 백업
- `cover_prompt.md`에 새 버전 append
- 콘셉트 변경 요청 → 3안부터 다시
