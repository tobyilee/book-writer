# Cover Design — 하네스 엔지니어링

## 결정된 콘셉트 (Concept A: 타이포그래피 + 루프 다이어그램)

오라일리/Manning/Pragmatic Bookshelf 계열 전문서 톤. 중앙부에 루프(고리) 모티프를 추상 기하로
표현하여, 책의 핵심 메타포인 '하네스(harness) = 구속과 방향의 제어 구조'를
다이어그램 언어로 드러낸다. 배경은 깊은 네이비(#0E2439), 액센트는 머스타드(#D4A017).

## 구성

- **상단 (25%)**: 작은 대문자 영문 카테고리 라벨 (`HARNESS ENGINEERING` / 트래킹 넓게)
- **중앙 (40%)**: 루프 다이어그램. 원형 궤도 2~3개가 교차하며,
  교차점에 노드(작은 원/사각형)가 놓여 "loop + control" 구조를 암시.
  선 굵기는 균일하지 않게 — 두꺼운 프레임 + 얇은 궤적 조합.
- **중단 (20%)**: 한글 메인 타이틀 `하네스 엔지니어링` (크고 강한 산세리프)
- **하단 부제 (10%)**: `Claude Code와 Codex로 에이전트를 프로덕션에 태우는 법`
- **바닥 (5%)**: 저자명 `TOBY-AI` (소형 대문자 트래킹)

## 색상

- 배경: `#0E2439` (Deep Navy, 오라일리 데이터 시리즈 느낌)
- 타이포: `#F5F1E8` (Off-white / warm paper)
- 액센트: `#D4A017` (Mustard — 루프 다이어그램의 주요 선 1개와 저자명)
- 보조 라인: `#6B8B9E` (Dim steel blue)

## 이미지 생성 프롬프트 (참고 — MCP 미연결로 이번 사이클은 ImageMagick 로컬 렌더링 사용)

```
A minimalist engineering book cover, 1600x2560, deep navy (#0E2439) background.
Centerpiece: abstract loop diagram — two or three intersecting circular orbits
rendered as clean thin strokes in dim steel blue (#6B8B9E), with one orbit
highlighted in mustard (#D4A017). Small square and circular nodes at orbit
intersections, suggesting a control-feedback structure. No illustration, no
photograph — pure geometric diagram, O'Reilly / Pragmatic Bookshelf engineering
book aesthetic. Clean sans-serif typography, Korean title "하네스 엔지니어링"
in large bold off-white, subtitle in smaller off-white below, author "TOBY-AI"
at bottom in small tracked mustard capitals. No gradients, no glow, no AI/robot
imagery, no neon. Feels like a 2019-era technical book on distributed systems.
```

## 폴백 (이번 실행에 사용한 방법)

ImageMagick 7 의 벡터 도형 + 네이티브 한글 폰트로 다이어그램형 표지를 직접 렌더.
- 한글 폰트: `/System/Library/Fonts/AppleSDGothicNeo.ttc` (Heavy / Bold)
- 영문 폰트: 시스템 기본 산세리프 (Helvetica / Arial)
- 루프는 `magick -draw` 의 `circle` 명령으로 표현, 노드는 `rectangle` + `circle` 조합

## 다음 개정 시 고려할 A/B 후보

- **Concept B (Pure typography)**: 다이어그램 제거, 한글 타이틀만 초대형으로.
  Manning 계열처럼 여백이 지배적인 구성.
- **Concept C (Grid of nodes)**: 루프 대신 3x5 노드 격자 + 일부 교차선이 강조.
  '에이전트 팜 / 오케스트레이션' 메타포 강화.
