# 표지 생성 기록 — 꺼내 쓰는 뇌

## 책 정보

- **제목:** 꺼내 쓰는 뇌
- **부제:** 지식을 성과로 바꾸는 완벽한 기억과 인출의 과학
- **저자:** Toby-AI
- **장르:** 학습법/자기계발/인지과학 대중서
- **언어:** 한국어 (ko)

## 컨셉 결정

계획서 02_plan.md 6절은 두 안을 트레이드오프로 제시했다.

- **1안 (손이 종이에서 글자를 끄집어내는 일러스트)** — 한국 학습법 시장 친숙성 ↑, 학술 신뢰 ↓
- **2안 (머리 안 그물망에서 한 가닥이 빠져나오는 추상 도형)** — 학술 무게 ↑, 학습법 코너 진입 위험

**채택: 융합형.** 종이결 위에 미니멀 신경 그물망을 그리고, 그물망 한 가닥이 골드 광선으로 변환되어 화면 우상단 바깥으로 빠져나가도록 했다.

- "그물망 = 인지망/스키마" → 2안의 학술 무게
- "종이결 베이스" → 1안의 학습 코너 친숙성
- "한 가닥이 빛으로 빠져나가는 흐름" → 인출(retrieval)의 시각적 은유 — 책의 핵심 약속을 한 컷에 압축

## 비주얼 시스템

| 요소 | 결정 |
|------|------|
| 비율 | 1600 × 2560 (EPUB 표준 1.6:1) |
| 베이스 | 따뜻한 아이보리 (#F4EEE2) + 미세 노이즈 종이결 + 비네팅 |
| 강조색 | 깊은 인디고 (#182448) — 그물망·본제 |
| 포인트 | 골드 (#BE984E / #DCBC7C) — 룰 라인·인출 가닥·핵심 노드 외곽 링 |
| 본제 폰트 | Apple SD Gothic Neo Heavy 260pt |
| 부제 폰트 | Apple SD Gothic Neo SemiBold 64pt (두 줄 줄바꿈) |
| 띠지 폰트 | Apple SD Gothic Neo SemiBold 34pt |
| 저자 폰트 | Apple SD Gothic Neo Bold 52pt |

## 텍스트 배치

```
┌─────────────────────────────────┐
│  ─────────                       │  상단 띠지 (4대 차별 키워드)
│  인코딩 우선 · 생성적 인출 · …    │
│  ─────────                       │
│                                  │
│         · ·  · 그물망            │  ← 인지망 + 골드 인출 가닥
│        · ·●·· · ─────→            │     (우상단 바깥으로 빠져나감)
│         · ·  · ·                 │
│                                  │
│       꺼내 쓰는 뇌                 │  본제 (Heavy, 260pt)
│        ─────                     │  골드 룰
│     지식을 성과로 바꾸는            │  부제 (SemiBold, 64pt)
│     완벽한 기억과 인출의 과학       │
│                                  │
│   공부했는데 안 떠오른 적, 있는가?   │  후크 (Regular, 32pt)
│           ────                   │  골드 룰
│         Toby-AI                  │  저자 (Bold, 52pt)
└─────────────────────────────────┘
```

## 사용 도구

- **선택:** PIL/Pillow 직접 합성 (Python 3)
- **이유:** 외부 image-gen MCP·OpenAI/Gemini API 키 미설정 환경. ImageMagick 미설치. 그러나 모티프가 "추상 그물망 + 종이결 + 타이포"로 이미 단순한 그래픽 합성으로 충분히 표현 가능 — 외부 API의 한국어 텍스트 렌더링 불안정 문제도 회피.
- **폰트:** 시스템 설치 한국어 폰트 사용 (Apple SD Gothic Neo .ttc — Regular/Bold/Heavy 인덱스).
- **스크립트:** `retrieval-brain/_make_cover.py` (재실행 가능).

## 외부 API 사용 시 영문 프롬프트 (참고용)

만약 향후 DALL-E/Imagen/Gemini Image로 재생성하려면 다음 프롬프트를 권장:

```
Minimalist Korean book cover illustration, no text, vertical 1600x2560.
Warm ivory paper texture background with subtle paper grain and soft vignette.
Center: a delicate abstract neural mesh — about 25 small dark indigo nodes
connected by thin lines, forming a loose web that suggests cognition and
knowledge structure. Three core nodes near center are slightly larger and
encircled by thin gold rings.
A single thin gold luminous strand flows out from the inner mesh, curving
upward and rightward, exiting the canvas at upper right corner — symbolizing
retrieval, the act of pulling knowledge out.
Color palette: warm ivory base (#F4EEE2), deep indigo accent (#182448),
muted gold highlight (#BE984E). No bright white background. No anatomical
brain illustration. No neon. No flashy gradients.
Editorial book cover aesthetic in the style of contemporary Korean nonfiction
bestsellers (학습법/인지과학 코너). Clean, calm, intellectually serious yet
inviting. Leave generous bottom half empty for typography overlay.
```

후처리: PIL로 한국어 본제·부제·저자·띠지 텍스트 합성 (외부 모델은 한국어 글자 깨짐).

## 산출물

- `retrieval-brain/cover.png` (v2, 최종) — 1600×2560 RGB PNG, 약 3.0 MB
- `retrieval-brain/cover_v1.png` (v1, 백업) — 첫 시안, 그물망 절제 전
- `retrieval-brain/_make_cover.py` — 재실행 가능한 생성 스크립트

## 재생성 가이드

```bash
cd retrieval-brain
python3 _make_cover.py
```

스크립트의 `random.Random(11)` 시드를 바꾸면 그물망 노드 배치가 바뀐다.
색감 변경은 파일 상단 `IVORY/INDIGO/GOLD` 상수에서.

## 한 줄 컨셉 (epub-builder 활용)

> 종이결 위에 인지망의 한 가닥이 빛으로 변해 빠져나가는, 인출 행위의 미니멀 시각화.
