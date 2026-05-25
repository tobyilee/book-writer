# Cover Design — autoresearch: 사람이 자는 동안 진화하는 코드

## 최종 콘셉트 (선택안)

**"Loss Curve as Constellation"** — 시간축에 따라 떨어지는 train loss curve가 별빛처럼
점점이 사라지는 모더니즘 표지. 좌상단에서 출발한 곡선이 우하단으로 내려가며 각 데이터
포인트가 별처럼 흩뿌려진다. 사람이 자는 동안에도 모델이 학습 손실을 깎아내려가는 정적인
밤의 이미지.

## 콘셉트 비교 (3안)

1. **Loss Curve as Constellation** (채택) — train loss 곡선 + 별 + 깊은 밤. 곡선 자체가
   메인 비주얼, 곡선 위/아래 별들이 데이터 포인트로 산재. 시적이면서 단단함.
2. **Commit Graph Sky** — git 그래프가 밤하늘처럼 분기·병합되는 형태. 좋지만 git에 너무
   특정됨 — 책의 범용성을 줄임.
3. **Empty Desk + Glowing Monitor** — 너무 illustrative. 모더니즘에서 벗어남.

## 색상 팔레트

- `#0A0E1F` — 베이스 background (검정 80% + 푸른 20%)
- `#0F1530` — 약간 밝은 그라데이션 상단
- `#1A2447` — 중간 톤
- `#7EC8F5` — cyan-glow accent (별/곡선 highlight)
- `#F4C77B` — amber line (loss curve 본체, 따뜻한 단일 accent)
- `#E8EAF0` — 제목 본문 흰색 (살짝 푸른빛)
- `#8B95B5` — 부제·메타 정보 muted

## 타이포그래피

- 한국어 제목 "사람이 자는 동안 / 진화하는 코드" — **Pretendard Bold/ExtraBold** 약 110pt,
  두 줄 분리, 행간 1.1
- 영문 main mark "autoresearch" — **JetBrains Mono Bold** 약 70pt, 모노스페이스로 코드성 강조
- 부제 — **Pretendard Light** 약 36pt, muted color
- 저자 — **Pretendard Medium** 약 42pt, 하단 정렬
- 하네스 메타 (small) — **JetBrains Mono Regular** 약 22pt

## 레이아웃 (1600 × 2560)

```
┌──────────────────────────────┐
│  ┌ 그라데이션 night sky      │
│  ┌ 별들 (random, 다양한 밝기)│
│                              │
│   autoresearch               │  ← 상단 1/4, mono code mark
│   ─────────                  │
│                              │
│   사람이 자는 동안           │  ← 중앙: 큰 한글 제목 2줄
│   진화하는 코드              │
│                              │
│                              │
│        [loss curve]          │  ← 중하단: amber curve + stars
│         \                    │
│          \____               │
│              \__             │
│                 \___         │
│                              │
│   Karpathy의 자율 연구       │  ← 부제 (작게)
│   루프를 Claude Code 환경으로│
│                              │
│   Toby-AI                    │  ← 하단 저자
│   v1.0.0 · 2026              │
└──────────────────────────────┘
```

## 영문 image-gen 프롬프트 (참조용 — 실제 산출은 PIL 직접 렌더링)

> Minimalist modernist book cover, deep midnight navy background with subtle
> gradient, scattered tiny stars at various brightness levels like real night
> sky, a gentle amber-gold train loss curve descending from upper-left to
> lower-right with data points glowing as stars along its path, no humans, no
> robots, no green Matrix code, MIT Press / O'Reilly minimalism aesthetic,
> serene but weighty, cyan glow accents, 1600x2560 portrait orientation,
> typography area reserved at top and bottom, photorealistic noise texture.

## 사용 방법

Pillow (PIL)로 직접 렌더링. ImageMagick 미설치 환경이라 Python 기반으로 진행.
- random seed 고정으로 재현 가능
- 별들은 가우시안 distribution, 곡선은 noisy exponential decay (실제 loss curve 시뮬레이션)
- 타이포는 시스템 폰트(Pretendard, JetBrains Mono) 사용
