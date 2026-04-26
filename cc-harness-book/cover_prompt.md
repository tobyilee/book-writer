# Cover Design — 하네스 엔지니어링

## 콘셉트 (1순위 채택)

**미니멀 톱니 메커니즘 (Ratchet)** — 어두운 남청색 배경 위에 정밀하게 그려진 맞물린 톱니바퀴들. 각 톱니에 누적된 점 표식으로 ratchet 효과 암시. 큰 한글 타이포그래피와 결합.

대안 콘셉트 (미채택):
- B: 추상 그리드/와이어프레임 — 빌딩블록 네트워크
- C: 타이포그래피 우선 — 시각 요소 최소화

## 영문 이미지 생성 프롬프트 (이미지 생성 MCP/API 사용 시)

```
A minimalist book cover, 1600x2560, dark navy background (#0a1929 to #1e293b gradient).
Centered: precisely engineered interlocking gears (ratchet mechanism) with one tiny accent
mark on each tooth, suggesting accumulated learning. Gears in light cyan (#22d3ee) line art,
slightly luminous. Above gears: large Korean title typography "하네스 엔지니어링" in
crisp white bold sans-serif. Below title: smaller subtitle "Claude Code를 팀의 무기로 길들이기".
At the bottom: thin horizontal line and tagline "모델은 수렴하고, 차이는 하네스에서 만들어진다"
in muted gray. Author "Toby-AI" in small text bottom-right.
Aesthetic: O'Reilly meets a German engineering manual. Calm, technical, professional. No clutter.
No AI/brain/robot imagery. No bright pinks or purples.
```

## 실제 사용한 방법

이미지 생성 MCP 미연결 → ImageMagick 미설치 → **Python/PIL 폴백**으로 진행.
- Pretendard 폰트(시스템 설치)로 한글 타이포그래피 렌더링
- 톱니바퀴 메커니즘은 벡터 드로잉(원, 호, 사다리꼴 톱니)으로 직접 그려 라인아트 구현
- 누적 ratchet 도트는 한 톱니에 점진적으로 채워 넣어 학습 누적 의미 강조
- 색상 팔레트: 배경 그래디언트(#0a1929 → #1e293b), 액센트 시안(#22d3ee), 흰색 타이포

## 색상 팔레트

- 배경: `#0a1929` (top) → `#1e293b` (bottom) 수직 그래디언트
- 톱니/액센트: `#22d3ee` (시안), 보조 `#06b6d4`
- 타이포: `#ffffff` (제목), `#cbd5e1` (부제), `#94a3b8` (헤드라인 카피, 저자)

## 타이포그래피

- 제목 "하네스 엔지니어링": Pretendard ExtraBold, 약 200pt
- 부제 "Claude Code를 팀의 무기로 길들이기": Pretendard SemiBold, 약 60pt
- 헤드라인 카피: Pretendard Regular, 약 38pt, letter-spacing 약간 +
- 저자 "Toby-AI": Pretendard Medium, 약 44pt

## 재생성 메모

- 톱니가 너무 화려해 보이면 단일 큰 톱니 + 작은 보조 톱니 1개로 줄인다.
- 헤드라인 카피가 길어 두 줄로 줄바꿈 시 균형 확인.
- 시안 액센트가 마케팅스러우면 호박색(#f59e0b) 또는 무채색(라이트 그레이)으로 대체 검토.
