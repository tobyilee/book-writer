# Harness Engineering — 학습 자료

현업 개발자가 "agentic coding에서의 하네스 엔지니어링"을 제대로 학습하기 위한 자료 묶음.

## 읽는 순서

1. **[DEVELOPER_CURRICULUM.md](DEVELOPER_CURRICULUM.md)** ⭐
   현업 엔지니어 대상 8주 커리큘럼. 리서치·비평 결과를 모두 반영한 **정본**.
   Module 0~5 + Capstone, 도구 선택 매트릭스, 위협 모델, 프로덕션 운영까지 포함.

2. **[LEARNING_PLAN.md](LEARNING_PLAN.md)**
   최초에 주어진 강의 커리큘럼(Ralph Loop → Karpathy Loop → 미니 랄프톤)을 그대로 따라 만든 6주 학습 플랜. 강의 과정과 1:1 대응되는 참조용.

## 근거 자료 (research/)

- **[web-research.md](research/web-research.md)** — Claude Code / Codex CLI / Cursor / Aider 실제 동작, AGENTS.md 스펙, 훅 메커니즘, MCP 통합, 비용 특성. 공식 docs + 실무 블로그 기반 ~2,100 단어.
- **[community-research.md](research/community-research.md)** — Reddit · HN · GitHub Issues · Twitter · 한국 개발자 커뮤니티에서 수집한 실전 페인포인트. 10개 테마 + Contrarian Signals.
- **[paper-research.md](research/paper-research.md)** — 학술 27편 (ReAct, Reflexion, CoVe, SWE-agent, Agent-SafetyBench, FrugalGPT 등) 6토픽 정리. 각 논문의 실용적 함의 한 줄씩.

## 핵심 결론 (TL;DR)

- **도구 선택이 첫 결정이다.** Claude Code / Codex / Cursor / Aider는 비용·통제·관측성이 모두 다르다. "아무거나 하나" 는 실무에서 락인 비용으로 돌아온다.
- **컨텍스트 엔지니어링이 99%다.** 루프·MCP는 그 위에 얹히는 껍질. `AGENTS.md`(Linux Foundation 표준)가 크로스-툴 공통어.
- **Ralph Loop는 4개 루프 패턴 중 하나다.** ReAct, Plan-and-Execute, Reflexion과 함께 고려해야 한다.
- **LLM 자체 검증은 편향이 크다.** Generator–Critic 분리 + pairwise-with-swap + 테스트/린터 back-pressure가 현실적 검증.
- **보안은 프롬프트가 아니라 아키텍처다.** 간접 프롬프트 인젝션·MCP 토큰 팽창·샌드박스 내 비밀 노출은 프롬프트로 못 막는다.
- **파레토로 평가하라.** 단일 scalar metric은 Goodhart 함정. 비용 × 품질 2축 + 개입률.

## 상태

- 기반 브랜치: `harness-engineering`
- 작성 방식: 4개 병렬 에이전트(web/community/paper researchers + critic)로 수집 → 편집 통합
