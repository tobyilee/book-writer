# 웹 리서치: AI 에이전틱 코딩 시대의 DDD

> 수집 기간: 2026-05-17
> 수집자: research-lead (web 갈래)
> 대상 독자: DDD를 알고 AI 코딩 도구를 도입 중인 시니어 개발자·테크 리드·아키텍트

## 자료 1: Backend Coding Rules for AI Coding Agents — DDD and Hexagonal Architecture

- 출처: https://medium.com/@bardia.khosravi/backend-coding-rules-for-ai-coding-agents-ddd-and-hexagonal-architecture-ecafe91c753f
- 저자·날짜: Bardia Khosravi, 2025-07-12
- 핵심 주장:
  - AI 코딩 에이전트는 사람이 한 번에 작성하는 양보다 훨씬 많은 코드를 짧은 시간에 쏟아낸다. 그 코드를 검토·반복하려면 **예측 가능한 패턴**이 필수다.
  - "AI 코딩 에이전트를 팀의 또 다른 개발자로 본다. 같은 모범 사례를 기대한다."
  - 도메인 계층은 표준 라이브러리 외 외부 의존성을 가져서는 안 된다 — DDD 원칙은 AI 시대에 **더 중요해진다**.
  - 24개의 규칙(엔티티/밸류/애그리거트, hexagonal 포트·어댑터, repository, use case 등)을 명시해 에이전트에게 제공하면, 생성된 코드의 품질과 일관성이 극적으로 올라간다.
- 인용 가능한 구절:
  - "Following design patterns is even more important now with AI code generation, since these tools generate way more code at once."
  - "I think of AI coding agents as another developer on my team — I expect them to follow the same best practices I'd expect from any team member."
- 관련 섹션: DDD 더 중요해짐 / 패턴별 영향 분석(hexagonal·port·adapter)

## 자료 2: Domain Driven Design in AI-Driven Era

- 출처: https://dev.to/aws-heroes/domain-driven-design-in-ai-driven-era-4l3h
- 저자·날짜: Bhuvaneswari Subramani (AWS Hero), 2025-02-18
- 핵심 주장:
  - "AI-Native Trailblazer"는 인프라/프론트/백/데브옵스/보안의 사일로를 뛰어넘는다. 이때 모두에게 DDD 기본 소양이 필요하다.
  - DDD는 더 이상 핵심 엔지니어링 팀만의 전문 영역으로 남을 수 없다 — AI 시대에는 **민주화**된다.
  - 차량 렌탈 도메인 예시로 Bounded Context(고객/차량/렌탈)와 Ubiquitous Language(Vehicle, Customer, Payment)를 설명한다.
  - 높은 응집도(high cohesion)와 낮은 결합도(low coupling)는 AI가 도메인을 침범하지 않는 가드레일이다.
- 인용 가능한 구절:
  - "By using Domain-Driven Design, you ensure that your application is well-organized, with clear boundaries and a shared understanding among everyone involved."
- 관련 섹션: DDD 더 중요해짐 / 시대 변화 관찰

## 자료 3: Spec-Driven Development is Domain-Driven Design's Impatient Cousin

- 출처: https://www.innoq.com/en/blog/2026/03/sdd-ddd-why-bmad-wont-save-you/
- 저자·날짜: Daniel Westheide (INNOQ Senior Consultant), 2026-03-18
- 핵심 주장:
  - BMAD 같은 SDD 도구는 **DDD가 실패하는 조직적 문제를 해결하지 못한다**. 둘은 같은 장벽에 부딪힌다 — 도메인 전문가 접근성.
  - 폭포수처럼 한 번에 인터뷰해서 spec을 받아내려는 시도는 실패한다. 모델은 구현과 반복적 협업 속에서 emergent하게 만들어진다.
  - BMAD는 "솔로 창업자"에게 통한다 — 한 사람이 도메인 전문가, 제품 책임자, 개발자 역할을 동시에 가질 때. 큰 조직에서는 구조적 문제를 증폭시킨다.
- 인용 가능한 구절:
  - "The specification layer depends completely on the quality of domain knowledge the human brings to the interview."
  - "A domain model that emerges through implementation and repeated collaboration will capture things no upfront interview process reliably surfaces."
  - "If the answer is no, you have an organisational problem that no interviewing agent can fix."
- 관련 섹션: 논쟁점(도구 vs 조직) / DDD 더 중요해짐 / 사례

## 자료 4: Applying Domain-Driven Design Principles to Multi-Agent AI Systems

- 출처: https://www.jamescroft.co.uk/applying-domain-driven-design-principles-to-multi-agent-ai-systems/
- 저자·날짜: James Croft, 2026-04-08 (업데이트 2026-05-04)
- 핵심 주장:
  - 멀티 에이전트 시스템 설계에 DDD 3축을 그대로 적용한다.
    - Bounded Context: 에이전트 하나가 곧 컨텍스트 하나. "Inventory Management 에이전트가 재고 도메인의 지식과 규칙을 캡슐화한다."
    - Ubiquitous Language: 각 에이전트는 도메인 전문가가 쓰는 용어를 일관되게 사용한다. "policy check", "regulation clause" 같은.
    - Domain Alignment: 에이전트는 실제 비즈니스 역량과 매핑되어야 한다 — 기술적 편의로 임의로 쪼개지 않는다.
- 인용 가능한 구절:
  - "One or more agents represent a bounded context...an agent encapsulates the knowledge and rules of its specific domain."
  - "Ensure each AI agent's purpose aligns with a real business capability or domain need. Don't create agents arbitrarily."
- 관련 섹션: 패턴별 영향 분석(strategic patterns) / 사례

## 자료 5: Eric Evans Encourages DDD Practitioners to Experiment with LLMs (InfoQ)

- 출처: https://www.infoq.com/news/2024/03/Evans-ddd-experiment-llm/
- 저자·날짜: InfoQ 기사, Explore DDD 2024 Keynote (Eric Evans), 2024-03
- 핵심 주장:
  - Evans는 LLM 자체를 **하나의 bounded context로 다루자**고 제안한다 — 특정 도메인 ubiquitous language로 fine-tune 된 모델은 범용 모델보다 훨씬 유용하다.
  - "여러 개의 fine-tuned 모델을 각각 다른 목적에 쓰는 것이 강력한 관심사 분리"라고 본다 — 거대한 ChatGPT 프롬프트 하나가 아니라.
  - NPC 실험에서 긴 프롬프트보다 작은 chunk로 나눴을 때 응답이 더 일관됐다 — DDD가 복잡성을 분해하는 방식과 일치.
  - "미래의 도메인 모델러는 자연어 해석이 필요한 subdomain을 자연스럽게 식별하고 LLM-supported로 슬롯한다"고 예측.
  - 단, "내 발언은 2024년 3월 시점이라는 점을 감안하라. 1년 후엔 무관해질 수 있다"고 명시적으로 경고.
- 인용 가능한 구절:
  - "Several fine-tuned models, each intended for a different purpose" → "strong separation of concerns."
- 관련 섹션: 거장 시각 / 패턴별 영향 분석(bounded context as model) / 미래 예측

## 자료 6: How Creating a Ubiquitous Language Ensures AI Builds What You Actually Want

- 출처: https://www.danielschleicher.com/software/engineering,/ai,/spec-driven/development/2026/01/04/removing-ambiguity-with-spec-driven-development.html
- 저자·날짜: Daniel Schleicher, 2026-01-04
- 핵심 주장:
  - "LLM은 증폭기다(LLMs are amplifiers)". 모호한 지시는 카오스를 증폭시키고, 정확한 의미 합의는 명료함을 증폭시킨다.
  - "order"의 다의성(체크아웃 commit / 결제 기록 / 배송 manifest) 같은 모호어를 사전에 해결하는 것이 핵심.
  - Spec Ambiguity Resolver 같은 도구는 모호어를 표시하고 정의 후보를 제안한다 — AI가 의미를 **자율적으로 결정하지 않는다**.
  - 산출물은 `domain-terms.md` 같은 살아있는 용어집으로 관리하고, 이후 모든 산출물의 일관성 기준이 된다.
- 인용 가능한 구절:
  - "LLMs are amplifiers. When we give an AI agent ambiguous instructions where 'order' could mean a dozen different things, it amplifies the chaos."
  - "Precision before code."
- 관련 섹션: Ubiquitous Language 강화 / 실무 적용 팁

## 자료 7: From Prompt Spaghetti to Bounded Contexts — DDD for Agentic Codebases

- 출처: https://gitnation.com/contents/from-prompt-spaghetti-to-bounded-contexts-ddd-for-agentic-codebases
- 저자·날짜: Nikita Golovko (Siemens AI Portfolio Architect), 2026 강연
- 핵심 주장:
  - 1개월차에는 깔끔하던 3개 에이전트가 6개월차에는 토큰 3,000개짜리 프롬프트 spaghetti가 된다. 그 중 ~85%가 도메인 로직이 아니라 **파싱·통합 로직**이다.
  - 에이전트 시스템은 사실상 분산 시스템 — 그런데 타입 안전성, 명시적 계약, 명확한 경계가 빠져 있다. cascade failure의 온상.
  - 4가지 DDD 패턴 적용:
    1. **Bounded Context** — 에이전트 하나에 책임 하나. (quality/security/testing 분리)
    2. **Schemas as Contracts** — 자연어 API를 Pydantic 스키마로 대체.
    3. **Anti-Corruption Layer** — 같은 단어(예: "function")가 다른 의미를 갖는 컨텍스트 사이 "의미적 방화벽".
    4. **Context Map** — 통합 아키텍처를 다이어그램이 아니라 **실행 가능한 코드**로.
  - Before vs After: 에이전트당 3,000+ 토큰(85% 통합 spaghetti) → ~500 토큰(90% 도메인 로직).
- 인용 가능한 구절:
  - "The best time to start was six months ago. The second best time is Monday."
- 관련 섹션: 패턴별 영향 분석 / 사례 / 실무 적용 팁

## 자료 8: When AI Agents Meet Bad Architecture — Why DDD and Cell-Based Design Start to Matter

- 출처: https://nwijesekare.medium.com/when-ai-agents-meet-bad-architecture-why-ddd-and-cell-based-design-start-to-matter-d9b42f707d86
- 저자·날짜: Natasha Wijesekare, 2026-03-27
- 핵심 주장:
  - "Agents don't break systems — they expose them." 에이전트는 예측 불가능한 호출 시퀀스로 **숨겨진 아키텍처 결함을 표면화**한다.
  - 시스템이 "caller가 알아서 잘 호출하겠지"라는 암묵적 가정에 의존하면, 에이전트는 그 가정을 매번 깨뜨린다.
  - DDD가 제공: 명확한 소유권 경계, intent-based API(전제조건을 검증), 도메인이 내부에서 invariant를 강제.
  - Cell-Based Architecture가 추가: 런타임 격리, 에이전트 retry에 대한 예측 가능한 부하 특성.
- 인용 가능한 구절:
  - "Agentic systems don't remove the need for good architecture. If anything they make it more obvious when it's missing."
- 관련 섹션: DDD 더 중요해짐 / 사례 / 실무 적용 팁

## 자료 9: From Vibe Coding to a Six-Agent Claude Code Team

- 출처: https://www.decodingai.com/p/squid-my-agentic-coding-setup-may-2026
- 저자·날짜: Paul Iusztin, 2026-05-12
- 핵심 주장:
  - 6개 에이전트(Product Manager / Software Engineer / Tester / PR Reviewer / On-Call / Self-Improve) 셋업. 각자 책임 분리, "코드 짠 에이전트가 정합성 판정하지 않는다."
  - **PM 에이전트가 DDD 글로사리(`docs/glossary.md`)를 유지** — code identifier, OpenAPI 스키마, DB 컬럼, 고객 인터페이스가 같은 단어를 쓰도록 강제.
  - 코드는 파일 타입이 아니라 **bounded context(=actionability) 기준으로 조직**할 때 에이전트 reasoning이 좋아진다.
  - 휴먼 체크포인트 2개 + 재시도 상한 5회로 폭주 방지.
- 인용 가능한 구절:
  - "No agent both writes code and decides whether the code is correct."
  - "You're using agents to write the whole codebase, but you are still the mastermind."
  - "The cost of vibe coding isn't abstract. It's the next feature you can't ship."
- 관련 섹션: 사례 / 실무 적용 팁

## 자료 10: Vibe Modeling — Visual Domain Modeling for Developers

- 출처: https://www.vibemodeling.app/what-is-vibe-modeling/
- 저자·날짜: Vibe Modeling 제품 페이지, 2025~2026
- 핵심 주장:
  - "Vibe coding은 차량, vibe modeling은 어디로 갈지 아는 것." 코드 생성 전에 도메인 이벤트, 경계, 사용자 흐름을 시각적으로 탐색.
  - AI가 DDD 지식(bounded context, aggregate, domain event)을 가져오고, 사람은 도메인 지식을 가져온다. **시각적 보드에서 만난다.**
  - 산출물을 Claude Code, Cursor, Copilot에 context로 export — "AI 도구를 극적으로 효과적으로 만든다."
- 인용 가능한 구절:
  - "Vibe coding is the vehicle. Vibe modeling is knowing where you're going before you start driving."
- 관련 섹션: 시대 변화 관찰 / 사례 / 실무 적용 팁

## 자료 11: Patterns for Reducing Friction in AI-Assisted Development (Thoughtworks)

- 출처: https://martinfowler.com/articles/reduce-friction-ai/
- 저자·날짜: Rahul Garg (Thoughtworks Principal Engineer), 2026-04-08
- 핵심 주장:
  - 5가지 패턴: Knowledge Priming / Design-First Collaboration / Encoding Team Standards / Context Anchoring / Feedback Flywheel.
  - "AI 어시스턴트는 무한 에너지와 0 컨텍스트를 가진 주니어 개발자다."
  - Design-First Collaboration: capabilities → components → interactions → contracts 순으로 디자인 레벨을 진행 — 사람 페어 프로그래밍의 화이트보딩을 재현.
  - 명시적이지 않은 시니어 직관을 **encoding해 팀 전체에 스케일** 시키는 것이 핵심.
- 인용 가능한 구절:
  - "AI assistants are like junior developers with infinite energy but zero context."
- 관련 섹션: 실무 적용 팁 / Design-First

## 자료 12: Humans and Agents in Software Engineering Loops (martinfowler.com)

- 출처: https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html
- 저자·날짜: Kief Morris, 2026-03-04
- 핵심 주장:
  - 휴먼-에이전트 관계의 3가지 모델: **Outside the Loop**(vibe coding), **In the Loop**(매 결과 검사 — 병목), **On the Loop**(권장 — harness 엔지니어링).
  - "Why loop"(아이디어 → 동작하는 소프트웨어)는 사람이, "How loop"(코드·테스트·중간 산출물)는 에이전트가 — 사람은 **harness를 설계·관리**한다.
  - 시니어 개발자의 새 핵심 역량: Harness Engineering — specification, quality check, workflow guidance를 만들어 에이전트 행동을 통제.
- 인용 가능한 구절:
  - "The right place for us humans is to build and manage the working loop rather than either leaving the agents to it or micromanaging what they produce."
  - "Agents can generate code faster than humans can manually inspect it."
- 관련 섹션: 시대 변화 관찰 / 실무 적용 팁 / 사례

## 자료 13: Some Thoughts on LLMs and Software Development (Martin Fowler)

- 출처: https://martinfowler.com/articles/202508-ai-thoughts.html
- 저자·날짜: Martin Fowler, 2025-08-28
- 핵심 주장:
  - "OF COURSE IT'S A BUBBLE." 철도, 인터넷처럼 거품과 잔존 가치가 공존한다.
  - LLM의 산출물에 hallucination은 버그가 아니라 **the feature** — Rebecca Parsons의 관점 인용: "LLM은 hallucination만 생성한다. 그 중 일부가 유용할 뿐."
  - "all tests green"이라고 거짓 보고하는 행동은 주니어 동료에게는 용납할 수 없는 수준 — 그래도 시니어가 검증 책임을 진다.
  - DDD를 직접 언급하지는 않지만, 아키텍처 판단·도메인 이해·유지보수가 코드 생성보다 압도적으로 중요하다는 입장 일관.
- 인용 가능한 구절:
  - "The vast majority of LLM usage is fancy auto-complete."
  - "Hallucinations aren't a bug, they are the feature."
- 관련 섹션: 거장 시각 / 논쟁점

## 자료 14: Anthropic 2026 Agentic Coding Trends Report

- 출처: https://resources.anthropic.com/2026-agentic-coding-trends-report
- 저자·날짜: Anthropic, 2026
- 핵심 주장:
  - AI 활용 작업 중 **~27%는 AI 없이는 시도조차 안 했을 작업**. 단순 가속이 아니라 새로운 작업의 가능화.
  - TELUS 50만+ 시간 절감, 어느 기업은 4-8개월 프로젝트를 2주에 완료.
  - 그러나 개발자들이 "완전 위임 가능"이라고 답한 작업은 **0-20% 수준** — AI는 60%의 작업에 관여하지만, 인간의 thoughtful setup·prompting·supervision·validation·judgment가 여전히 필수.
  - 2026의 핵심 전환: 단일 어시스턴트 → 조율된 멀티 에이전트 팀. 엔지니어는 코드 작성에서 **에이전트 조율**로 이동.
- 인용 가능한 구절:
  - "Engineers aren't doing the same work more quickly; they're doing substantially more work."
- 관련 섹션: 시대 변화 관찰 / 생산성 데이터 / 새로운 역할

## 자료 15: Effective Context Engineering for AI Agents (Anthropic Engineering)

- 출처: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 저자·날짜: Anthropic Engineering, 2025~2026
- 핵심 주장:
  - 병목은 "에이전트가 내가 원하는 걸 이해 못해"에서 "에이전트에게 필요한 컨텍스트가 없어"로 이동했다.
  - "Context is finite with diminishing marginal returns" — 가장 작은 high-signal 토큰 집합을 찾는 것이 핵심.
  - "Just in time" 컨텍스트 전략: 미리 다 넣지 말고 lightweight identifier로 두고 런타임에 동적으로 로드.
  - Compaction / tool-result clearing / memory 세 가지 컨텍스트 관리 전략.
- 인용 가능한 구절:
  - "The bottleneck has shifted from 'the agent does not understand what I want' to 'the agent does not have the context it needs to do it well.'"
- 관련 섹션: 시대 변화 관찰 / 실무 적용 팁

## 자료 16: Event Storming + AI = Turbocharged DDD (Tania Storm)

- 출처: https://medium.com/@tanstorm/leveraging-the-power-of-event-storming-for-domain-driven-design-3350913f7fe8
- 저자·날짜: Tania Storm, 2024~2025
- 핵심 주장:
  - Event Storming은 Alberto Brandolini가 DDD 맥락에서 만든, 컴퓨터 없이 도메인 이벤트를 발견하는 워크숍 기법.
  - AI를 통합하면 복잡한 시나리오에서 도메인 이벤트와 모델 식별이 가속화된다.
  - Qlerify, Vibe Modeling 같은 AI 기반 도구가 분산팀의 실시간 협업, 자동 문서화, 동적 다이어그램 생성을 지원.
- 관련 섹션: 시대 변화 관찰 / 실무 적용 팁
