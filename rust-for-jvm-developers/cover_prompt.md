# Cover Design Log — JVM 출신을 위한 Rust

## Version 1 (2026-05-03)

### Concept
- **Selected motif:** 모티프 4 (미니멀 추상 슬래시) + 모티프 1 (맞물린 기어) 융합
- **Rationale:**
  - 슬래시(/)는 폴리글랏의 시각적 상징 — JVM과 Rust 두 진영을 잇는 "다리".
  - 슬래시 양 끝의 두 기어(rust orange + JVM green)가 "두 진영이 맞물려 돌아간다"는 메시지를 압축.
  - 만화풍 게(Ferris)나 커피잔 클리셰 회피. 추상적이되 의미가 명료.
- **Palette (후보 1 채택):**
  - Background: deep charcoal `#181620` → `#0C0A0E` (vertical gradient)
  - Primary: Rust orange `#CE422B`
  - Accent: Gold `#D4A437` (rule, mark, edge highlight)
  - JVM green `#5A8A5A` — 부제 "Spring" 한 단어 + 좌측 하단 기어에만
  - Title: warm paper `#E8E2D6`
  - Sub: muted grey `#AAA298`
- **Warmth atmosphere:** 우상단 러스트 글로우 + 좌하단 인디고 글로우(미세) → 코퍼레이트 톤이 아닌 동반자적 무드.

### Tool
- Python PIL (Pillow) typography composition.
- Reason: 한글 가독성과 정확한 typographic control이 필요했고, 외부 image-gen API는 한글·고정 레이아웃에서 일관성이 떨어진다.

### Composition (1600 × 2560)
| Zone | Element |
|------|---------|
| Top band | Gold rule + "POLYGLOT BACKEND SERIES · Vol. 02" 라벨, 우측 "T · AI" 모노그램 |
| Title block (380~940px) | "JVM 출신을 위한" (Pretendard Black 188pt, paper) → "Rust" (Pretendard Black 320pt, rust) + 골드 언더라인 |
| Center diagonal | Rust slash + 골드 엣지 하이라이트, 양 끝에 기어 두 개 (rust top-right, JVM-green bottom-left) |
| Subtitle (~74% H) | "**Spring** 다음에 읽는 책" — Spring만 JVM 그린 / "대체가 아니라, 무기 추가." 부설명 |
| Bottom band | "지은이 Toby-AI" (좌) / "Java · Kotlin · Rust  폴리글랏 백엔드 입문" (우) |
| Frame | 30px 인셋 화이트 18% 알파 라인 (눈에 거의 안 보이지만 책 표지 마감감 부여) |

### Verification
- [x] 1600×2560 portrait
- [x] 썸네일 200×320 축소 후에도 "Rust"·"JVM 출신을 위한" 모두 판독 가능
- [x] 저자 표기 "Toby-AI" 명시 (이미지 내)
- [x] AI slop 회피 (번쩍이는 그라디언트, 의미 없는 입자, 클립아트 게/뱀, 코드 스크린샷 모두 없음)
- [x] 동반자적 따뜻함 (러스트 글로우, 페이퍼 톤 타이포, 그레인 텍스처 4%)

### English-equivalent prompt (외부 모델 재생성용)
```
A premium technical book cover, portrait 1600x2560, deep charcoal background
(#181620 to #0C0A0E vertical gradient) with a soft warm rust glow in the
upper-right corner. Editorial layout, left-aligned typography.

Top band: thin gold horizontal rule under a small label
"POLYGLOT BACKEND SERIES · Vol. 02" in muted grey, with monogram "T · AI"
in gold on the right.

Main title: "JVM 출신을 위한" in heavy paper-white sans-serif (Pretendard Black,
~188pt), placed in the upper third. Below it, the wordmark "Rust" set
oversized (~320pt) in Rust signature orange (#CE422B), with a thin gold
underline immediately beneath.

Center: a thick diagonal slash (rust orange, ~46px) running from upper-right
to lower-left, with a subtle gold edge highlight on one side and a soft
rust glow underneath. At the slash's upper-right end, a 14-tooth cog
in rust orange. At the lower-left end, a slightly rotated 14-tooth cog
in muted JVM forest green (#5A8A5A). The cogs lock into the slash like
gears meeting on a bridge.

Subtitle (lower-mid): "Spring 다음에 읽는 책" — the word "Spring"
in JVM green, the rest in paper white, set in Pretendard Medium ~78pt.
Below: "대체가 아니라, 무기 추가." in light grey, smaller.

Bottom band: thin hairline rule, "지은이 Toby-AI" left-aligned (Toby-AI bold),
"Java · Kotlin · Rust / 폴리글랏 백엔드 입문" right-aligned with the second
line in gold.

Mood: warm, confident, companionable — not corporate, not flashy. Subtle
4% film grain. No generic tech gradients. No stock photography. No cartoon
crab or coffee cup. No code screenshots. No publisher logo clutter.
```

### Notes
- 첫 시안에서 기어가 슬래시에서 살짝 떠 있어 "맞물림" 약함 → 기어를 슬래시 끝에 더 붙이고 (offset 130 → 78), 크기를 70 → 78로 키워 시각적 잠금감 강화.
- 한글 폰트는 Pretendard 시리즈 (Black/Bold/ExtraBold/Medium/Regular/Light) 사용.
- 재생성 스크립트: `cover_gen.py` (root 동일 폴더).
