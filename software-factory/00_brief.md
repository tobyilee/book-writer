# 저술 브리프 — Software Factory

- slug: `software-factory`
- genre: `tech-book` (활성 프로필: `profiles/tech-book/`)
- 저자: `Toby-AI` (기본값)
- 라이선스: 기본값 (`CC BY-NC-SA 4.0`, 매니페스트 `license` 비움)
- delegation_mode: `production`
- 작업 시작일: 2026-09-28

## 주제

AI를 이용해 요구사항을 받아 **구현 → 테스트 → 수정 → 배포**로 이어지는 작업을 반복적으로 수행하도록 만든 개발 시스템, **Software Factory**의 개념과 실무 활용 방법.

## 주요 내용 (사용자 요구)

1. Software Factory의 개념 — 무엇이고, 왜 지금 나왔고, 기존 CI/CD·자동화와 무엇이 다른가.
2. 사용 기술: **Claude Code (Opus 5.5 메인)**, **Codex (GPT-Sol-6 메인)**. 부가적으로 **Grok**, **Muse Spark** 등.
3. **1인 개발자**가 Software Factory를 만들어 다양한 개발 업무를 진행하는 방법.
4. **여러 명으로 구성된 개발팀**이 Software Factory를 팀 개발 업무에 활용하는 방법.
5. **단계적 발전 경로** — AI 코딩을 개발자 업무에 처음 도입하는 단계에서 출발해, AI가 점점 더 많은 작업을 자동으로·정해진 워크플로우를 따라 수행하도록 발전시키고, 궁극적으로 인간 개발자는 필요할 때에만 참여·결정·리뷰하는 단계까지. 이 과정을 자세히.
6. **다양한 workflow와 pipeline** 소개.
7. 최신 개념이므로 커뮤니티·인터넷·소셜미디어, 필요하면 YouTube 내용까지 분석해 반영.

## 대상 독자

- 백엔드: Java, Kotlin, Spring, Python, Node.js 경험
- 프론트엔드: React, Next.js 경험
- 배포: Cloudflare, AWS
- 개발 과정: GitHub의 각종 CI/CD 도구(GitHub Actions 등) 활용 경험
- → 예제·파이프라인은 이 스택(Spring/Kotlin·Python·Node 백엔드, React/Next.js 프론트, GitHub Actions, Cloudflare·AWS 배포) 위에서 보여준다.

## 리서치 착수 단서 (검증 필요 — 사실로 가정하지 말 것)

오늘은 2026-09-28이다. 아래는 출발점일 뿐이며, 각 항목의 실재·날짜·내용을 1차 출처로 확인해야 한다.

- "Software Factory" 용어의 최근 쓰임: StrongDM의 AI 팀이 공개한 software factory 사례("사람이 코드를 쓰지도 리뷰하지도 않는다" 원칙, 시나리오/홀드아웃 테스트, digital twin), Simon Willison 등의 해설, Factory.ai(Droids), "dark factory" 비유(Dan Shapiro의 AI 코딩 5단계 등).
- 자율 루프·오케스트레이션 패턴: Ralph (Wiggum) loop(Geoffrey Huntley), Steve Yegge의 Gas Town, spec-driven development(GitHub Spec Kit, Kiro 등), OpenAI의 harness engineering 글, Anthropic의 long-running agent/harness 관련 글, Martin Fowler 사이트의 관련 글.
- 도구 기능: Claude Code(서브에이전트·스킬·훅·헤드리스 `-p`·Agent SDK·GitHub Actions·백그라운드/클라우드 실행·플러그인), Codex(CLI·`codex exec`·cloud·GitHub 연동·AGENTS.md), GitHub Copilot coding agent·Agentic Workflows·"Continuous AI", 기타 백그라운드 에이전트.
- 모델: Opus 5.5, GPT-Sol-6, Grok(최신 버전), Muse Spark(Meta) — 각각의 출시 시점·특성·쓰임새.
- 팀 도입 사례·지표: DORA 보고서의 AI 관련 발견, METR 연구, 실무자 회고, 비용·보안·리뷰 병목 논쟁.
