# Cover Design Brief — 자바 개발자를 위한 Node.js

## 채택 콘셉트

권고안 1번(두 런타임의 시각적 대비) + 2번(단색 미니멀)의 하이브리드. 단색 미니멀 배경 위에 추상 모티프 두 개를 좌우에 배치해 "두 진영을 모두 가진 백엔드 개발자"의 정체성을 시각화.

## 디자인 시스템

### 색상

| 역할 | 값 | 의도 |
|------|----|----|
| 배경 (메인) | `#0F1626` (딥 네이비) | 시니어 기술서 톤. 어두운 단색으로 깊이감과 절제 |
| 배경 (그라디언트 하단) | `#1A2138` | 미세한 수직 그라디언트로 단조로움 회피 |
| Spring 모티프 | `#6DB33F` (Spring Green) | 좌측 — Java/Spring 진영 |
| Node 모티프 | `#5FA04E` (Node Green) | 우측 — Node.js 진영 |
| 메인 타이포 | `#F5F2E8` (웜 화이트) | 차가운 흰색 대신 약간 따뜻해 책장에 두고 싶은 톤 |
| 부제·저자 | `#A8B2C7` (다운 그레이) | 메인 타이포에 종속되는 보조 정보 |
| 액센트 라인 | `#C9A66B` (머스타드 골드) | 두 모티프가 만나는 지점에 1px 가로선. 만남의 상징 |

### 타이포그래피

- **메인 제목** "자바 개발자를 위한 Node.js" — Pretendard Bold, 약 110pt, 자간 살짝 좁힘
- **부제** "Spring 직관을 그대로 들고 가는 / 두 번째 런타임 가이드" — Pretendard Medium, 약 42pt, 두 줄 분할
- **슬로건** "도구만 바뀌었을 뿐, 우리는 여전히 백엔드 개발자다." — Pretendard Regular, 약 28pt, 머스타드 골드
- **저자** "Toby-AI" — Pretendard Medium, 약 36pt, 표지 하단

### 그래픽 모티프

**좌측 (Spring 진영):**
- 추상화된 코일 스프링 — 사선으로 흐르는 타원 호 4-5개를 스택. Spring Green 단색의 가는 라인 아트.
- 위치: 표지 좌측 상단, 약 1/4 영역

**우측 (Node 진영):**
- 이벤트 루프를 상징하는 원형 점선 + 한 점. 비동기성을 암시.
- 위치: 표지 우측 상단, 약 1/4 영역

**중앙 액센트:**
- 두 모티프 사이에 가는 머스타드 골드 가로선 (1px). "두 진영의 만남"을 직관적으로 시사.

## 레이아웃 (1600 × 2560)

```
┌─────────────────────────────────────┐
│                                     │  상단 마진 200px
│   [Spring 모티프]    [Node 모티프]   │  Y=300~700
│                                     │
│   ──── 머스타드 가로선 ────           │  Y=820 (1px)
│                                     │
│   자바 개발자를 위한                  │  Y=950
│   Node.js                           │  Y=1100  (메인 타이포)
│                                     │
│   Spring 직관을 그대로 들고 가는      │  Y=1380
│   두 번째 런타임 가이드               │  Y=1450
│                                     │
│                                     │
│   "도구만 바뀌었을 뿐,               │  Y=1900
│    우리는 여전히 백엔드 개발자다."    │  Y=1960
│                                     │
│                                     │
│              Toby-AI                │  Y=2380
│                                     │  하단 마진 100px
└─────────────────────────────────────┘
```

## 사용한 도구

- Python 3 + Pillow (PIL) — 외부 이미지 생성 API 미가용 환경, 로컬 렌더링.
- Pretendard Variable (`~/Library/Fonts/PretendardVariable.ttf`) — 한글 가독성 최우선.

## 영문 프롬프트 (이미지 생성 모델로 재생성하고 싶을 때)

```
Minimalist senior technical book cover, dark deep navy background (#0F1626) with subtle vertical gradient.
Top half: two abstract motifs side by side — left a stylized coil spring rendered in thin Spring Green (#6DB33F)
line art, right an event loop circle with dotted path and a single highlighted node in Node Green (#5FA04E).
A thin mustard gold horizontal line (#C9A66B) cuts between the motifs and the title block, symbolizing the
meeting of two runtimes. Title in large warm-white Korean sans-serif: "자바 개발자를 위한 Node.js".
Subtitle two lines below in muted gray: "Spring 직관을 그대로 들고 가는 / 두 번째 런타임 가이드".
Slogan in mustard gold near bottom: "도구만 바뀌었을 뿐, 우리는 여전히 백엔드 개발자다."
Author "Toby-AI" centered at the very bottom in medium gray.
Restrained, calm, precise. Senior O'Reilly / 인사이트 출판사 vibe. No glow, no gradient on type, no decoration.
1600 × 2560 portrait, EPUB cover.
```

## A/B 변형 후보

사용자 피드백이 들어오면 다음 축으로 변형 가능하다.

1. **배경 색조 전환** — 딥 네이비 → 차콜 그레이(`#1B1B1B`) 또는 오프 화이트(`#F5F2E8` + 다크 텍스트). "라이트 모드" 표지.
2. **모티프 강도** — 라인 아트가 약하게 느껴지면 stroke를 두껍게(2px → 4px) 또는 모티프 크기 확대.
3. **슬로건 제거** — 시니어 톤에 슬로건이 거슬릴 경우 슬로건 줄을 빼고 부제만 유지.
4. **타이포 정렬** — 가운데 정렬 → 좌측 정렬(시니어 기술서에 더 흔한 레이아웃).
5. **콘셉트 3번(아키텍처 다이어그램)** — Strangler Fig 박스 다이어그램으로 전면 교체. 8장의 절정을 표지에 직접 시각화.

## 폴백 트리거

- Pretendard 폰트 부재 시 → Apple SD Gothic Neo (`/System/Library/Fonts/AppleSDGothicNeo.ttc`)로 자동 대체.
- PIL 부재 시 → 단순 단색 PNG + 기본 텍스트만 (시스템 기본 폰트). 책 빌드 진행은 보장.
