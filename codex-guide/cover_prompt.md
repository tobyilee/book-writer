# Cover Design Log — 『같은 이름, 다른 동작』

- 책 제목: 같은 이름, 다른 동작
- 부제: Claude Code 사용자를 위한 OpenAI Codex 완전 정리
- 저자 표기: Toby-AI
- 장르·톤: tech-book, 차분하고 전문적인 톤, 과장 금지
- 대상 독자: AI 에이전틱 코딩 경험 개발자 (Claude Code 사용자가 Codex로 확장)

## 콘셉트 3안

- **A — 미니멀리즘 (채택)**: 하나의 트렁크 선이 위에서 내려오다가 한 지점에서 두 갈래(호박색·틸색)로 갈라져 각각 다른 종점(`$ run`)에 닿는 심볼. "같은 출발점(같은 이름의 명령/개념) → 다른 경로(다른 동작)"라는 책의 핵심 은유를 문자 그대로 도해. 큰 타이포 + 심볼 하나 조합, 톤은 어둡고 차분한 네이비/차콜.
- **B — 일러스트형**: 두 개의 터미널 창을 나란히 배치하고 같은 명령을 입력했을 때 다른 출력이 나오는 모습을 묘사. 정보량이 많아 축소 시 가독성이 떨어지고 스크린샷풍이라 클리셰 위험 → 기각.
- **C — 타이포그래피 중심**: 제목 "같은 이름, 다른 동작"에서 "다른" 부분만 다른 색/서체로 처리해 제목 자체가 메시지를 전달. 심볼이 없어 시각적 앵커가 약하고 다른 책들과 차별화가 부족 → 기각.

→ **A안 채택**: 갈라지는 경로 모티프가 책의 핵심 주장(같은 표면, 다른 하네스)을 가장 직접적으로, 과장 없이 전달함. 실제 브랜드 로고·색상은 사용하지 않고 추상적인 호박색/틸색 두 계열로만 구분(상표 회피 + 클리셰 회피).

## 제작 방식

이미지 생성 MCP/외부 API가 연결되어 있지 않아(도구 목록에 image-gen MCP 없음), 스킬의 우선순위에 따라 벡터 기반 타이포그래피 표지로 제작:

1. `rsvg-convert`(librsvg, 이 머신에 설치되어 있음)로 SVG를 1600×2560 PNG로 래스터화 — ImageMagick 내장 SVG 파서(MSVG)는 베지어 path의 fill 처리가 불안정해(채워진 삼각형으로 오염) 폐기, `rsvg-convert`가 정상 렌더링을 확인.
2. 한글 타이포는 `Pretendard`(ExtraBold/SemiBold/Medium, `/Users/tobylee/Library/Fonts/`에 설치되어 fontconfig가 인식) 사용. 모노스페이스 요소(`> claude to codex`, `$ run`, 캡션)는 `JetBrains Mono`.
3. Playwright MCP로 HTML→스크린샷 방식도 시도했으나 이 환경에서 `file://` 프로토콜과 로컬 루프백 네트워크가 차단되어 있어 포기, SVG+rsvg-convert 경로로 전환.

## SVG 소스 요약 (재생성용)

- 배경: 대각선 그라디언트 `#10121c → #14172a → #1a1526` + 중앙 은은한 glow + 하단 vignette
- 상단 eyebrow: `> claude to codex` (JetBrains Mono, claude=호박색 `#e2a05c`, codex=틸색 `#5cc2b8`)
- 타이틀: "같은 이름," / "다른 동작" — Pretendard 800, 128px, `#f7f5f0`
- 부제: "Claude Code 사용자를 위한" / "**OpenAI Codex** 완전 정리" — Pretendard 500/600, 44px, `#a9aec4`/`#cfd3e2`
- 심볼: 단일 트렁크(`#9aa0b8`)가 (800,1150)에서 두 갈래로 분기 — 좌측 호박색 `#e2a05c` 종점 (430,1760), 우측 틸색 `#5cc2b8` 종점 (1170,1760), 각 종점 아래 `$ run` 라벨
- 캡션: `SAME SHAPE · DIFFERENT BEHAVIOR` (JetBrains Mono, letter-spacing 4)
- 하단: 구분선 + `TECH · CLAUDE CODE → CODEX` (좌) + `Toby-AI` (우, Pretendard 600 40px)

원본 SVG: `/private/tmp/claude-501/-Users-tobylee-workspace-ai-book-writer/d7c22e65-5355-494b-814e-337aa75cf12e/scratchpad/cover/cover.svg`
(재생성 시 이 SVG를 편집 후 `rsvg-convert -w 1600 -h 2560 -o cover.png cover.svg` 재실행)

## Version 1 (2026-08-02)

- Concept: A (미니멀리즘 — 분기 심볼 + 타이포)
- Tool: rsvg-convert (SVG → PNG), 폰트 Pretendard + JetBrains Mono
- Prompt: (이미지 생성 API 대신 직접 설계한 SVG 벡터 명세 — 위 "SVG 소스 요약" 참조)
- Result: cover.png (1600×2560)
- Notes: 썸네일(200×320) 검증 완료 — 축소해도 제목·심볼·저자명 가독. 클리셰(기본 그라데이션·스톡사진) 회피, 실제 브랜드 로고/색상 미사용.
