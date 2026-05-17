# AI 에이전틱 코딩 시대의 DDD — 레퍼런스 문서

> 책: "AI 에이전틱 코딩 시대의 DDD — 여전히 유효한가?"
> 대상 독자: DDD를 알고 AI 에이전틱 코딩을 실무에서 경험/도입 중인 시니어 개발자, 테크 리드, 아키텍트
> 수집일: 2026-05-17
> 통합자: research-lead
> 출처 라벨: [W]=웹 자료, [P]=논문, [C]=커뮤니티

---

## 1. 개념과 정의

### 1.1 DDD 핵심 개념 재정리

DDD(Domain-Driven Design)는 Eric Evans가 2003년 *Domain-Driven Design: Tackling Complexity in the Heart of Software* 에서 정립한 설계 방법론이다. 한국에서는 최범균의 *DDD Start!* 가 표준 입문서로 자리 잡았다 [C: medium myrealtrip].

| 개념 | 정의 | 한국어 통용 표기 |
|---|---|---|
| **Domain** | 소프트웨어로 해결하려는 문제 영역 [C: medium myrealtrip] | 도메인 |
| **Ubiquitous Language** | 도메인 전문가와 개발자가 함께 사용하는, bounded context 내에서 일관된 공용어 | 유비쿼터스 언어 / 공용어 |
| **Bounded Context** | 특정 도메인 모델과 ubiquitous language가 일관되게 적용되는 경계 | 바운디드 컨텍스트 / 경계 컨텍스트 / 제한된 맥락 (혼용) |
| **Subdomain** | 도메인을 더 작은 영역으로 분할한 것 (Core / Supporting / Generic) | 서브도메인 |
| **Context Map** | bounded context 간의 관계(Customer-Supplier, Conformist, ACL, Shared Kernel, Published Language 등)를 명시한 지도 | 컨텍스트 맵 |
| **Entity** | 고유 식별자로 구분되며 자신의 상태와 라이프사이클을 갖는 도메인 객체 [C: medium myrealtrip] | 엔티티 |
| **Value Object** | 개념적으로 묶이는 데이터 집합, 식별자 없이 값으로 동등성 비교 | 밸류 / 값 객체 |
| **Aggregate** | 도메인 객체들의 묶음. 루트 엔티티를 통해 외부와 소통하고 내부 일관성을 보장 [C: medium myrealtrip] | 애그리거트 (주류) / 집합체 |
| **Repository** | 애그리거트 단위로 영속성을 추상화하는 컬렉션 같은 인터페이스 | 리포지터리 |
| **Domain Service** | 엔티티/밸류에 자연스럽게 속하지 않는 도메인 로직 | 도메인 서비스 |
| **Domain Event** | 도메인에서 발생한 사실(fact). 다른 컨텍스트가 반응할 수 있도록 발행 | 도메인 이벤트 |
| **Anti-Corruption Layer (ACL)** | 외부 컨텍스트의 모델이 내 컨텍스트에 침투해 오염시키는 것을 막는 번역 계층 | 부패 방지 계층 / 안티커럽션 레이어 |
| **Strategic vs Tactical DDD** | Strategic = 거시(컨텍스트, 도메인 분할, 매핑). Tactical = 미시(엔티티·VO·애그리거트·서비스·이벤트·리포지터리·팩토리) | 전략적 / 전술적 |

> **관점 메모**: Eric Evans 본인이 *"DDD는 은탄환이 아니다"* 라고 지속적으로 강조한다 [C: medium myrealtrip]. 이 책의 핵심 질문 — "AI 시대에도 여전히 유효한가?" — 은 그래서 "어디까지 유효하고 어디는 변하는가?"라는 정밀한 질문으로 다시 던져야 한다.

### 1.2 AI 에이전틱 코딩과 Vibe Coding

| 용어 | 정의 | 출처 |
|---|---|---|
| **AI Coding Agent** | LLM이 코드베이스를 읽고, 행동 계획을 세우고, 실제 개발 도구로 실행하고, 결과를 평가해 접근 방식을 조정하는 자율적 코딩 도구 (예: Claude Code, Cursor, Windsurf, Devin) | [W] Anthropic, [W] Khosravi |
| **Vibe Coding** | 2025년 2월 Andrej Karpathy가 제시한 개념. 엄밀한 논리·설계 없이 직관(vibe)에 따라 큰 그림만 제시하고 AI에게 구체 구현을 맡기는 방식 | [C] 나무위키 / brunch |
| **Agentic Coding** | 단일 어시스턴트가 아니라 **조율된 다수 에이전트가 시간 단위·일 단위로 자율 실행**, 엔지니어는 코드 작성이 아니라 그 시스템을 조율하는 방식 | [W] Anthropic 2026 Trends Report |
| **Context Engineering** | "에이전트가 내가 원하는 걸 이해 못해" → "에이전트에게 필요한 컨텍스트가 없어"로 병목이 이동한 시대의 새 분야. high-signal 토큰의 최소 집합을 찾아내는 일 | [W] Anthropic Engineering |
| **Harness Engineering** | 에이전트 행동을 통제하는 specification, quality check, workflow guidance를 사람이 설계·관리하는 일. "Humans on the loop" 모델의 핵심 | [W] Kief Morris (martinfowler.com) |
| **Vibe Modeling** | 코드 생성 전에 도메인 이벤트, 경계, 사용자 흐름을 시각적으로 AI와 함께 탐색하는 단계. "vibe coding의 차량, vibe modeling은 어디로 갈지 아는 것" | [W] vibemodeling.app |

> **상충 관점 A vs B**:
> - 관점 A (vibe coding 사망): "Vibe coding은 죽었다. Agentic coding이 그 자리를 채운다." [W] Alek Dobrohotov, 2026
> - 관점 B (vibe coding 부활/공존): "Prototyping과 소규모 자동화엔 여전히 최고" — 나무위키 정의도 유효 [C]

---

## 2. 시대 변화 관찰

### 2.1 AI 코딩 도구 지형 (2025-2026)

- **Claude Code (Anthropic)**: 코드베이스를 읽고 계획·실행·평가하는 에이전틱 시스템. "just in time" 컨텍스트 전략으로 큰 데이터 다룸 [W: Anthropic Engineering].
- **Cursor**: IDE 통합형 에이전트. 자체 포럼에 TDD/DDD 가드레일 토론이 활발 [C: Cursor forum].
- **GitHub Copilot**: "대부분은 fancy auto-complete로 쓴다"는 평가 (Fowler).
- **Devin (Cognition Labs)**: 자율 SWE 에이전트의 상징적 사례.
- **AI-DLC** (AWS Heroes 중심): AI가 자율적으로 Aggregate/Value Object/Entity/Domain Event/Repository/Factory를 생성하는 라이프사이클 [C: aidlc-docs/ai-dlc-whitepaper-ko.md].
- **Qlerify / Vibe Modeling**: AI 기반 Event Storming·도메인 모델링 협업 도구 [W: tanstorm, vibemodeling.app].

### 2.2 생산성·역할 변화 데이터

| 지표 | 수치 | 출처 |
|---|---|---|
| AI 활용 작업 중 "AI 없으면 시도조차 안 했을 작업" 비중 | ~27% | [W] Anthropic 2026 Trends Report |
| 개발자가 "완전 위임 가능"이라 답한 작업 비중 | 0-20% | 동일 |
| AI가 개입하는 작업 비중 | ~60% | 동일 |
| 경험 많은 개발자의 AI 도구 사용 시 실제 속도 | **19% 더 느림** (그러나 본인은 20% 빨라졌다고 인식) | [C] METR 2025 (NDS Cloud Tech Blog 인용) |
| AI 공저 코드의 보안 취약점 비율 | 사람 코드의 **2.74×** | [C] NDS Cloud Tech Blog (Park Jung-hyun, 2026-03-09) |
| 커뮤니티 기여 에이전트 스킬 중 취약점 보유 비중 | **26.1%** | [P] arXiv 2602.12430 |
| 대형 기업 사례 — TELUS 절감 시간 | 50만+ 시간 | [W] Anthropic 2026 Trends Report |
| 대형 기업 사례 — 4-8개월 프로젝트가 2주에 완료 | 1건 보고 | 동일 |
| Golovko 사례: 에이전트당 토큰 (DDD 적용 전 → 후) | 3,000+ (85% 통합 spaghetti) → ~500 (90% 도메인 로직) | [W] gitnation.com |

> **핵심 함의**: 생산성은 분명히 올라가지만 "사람이 빠지는" 형태가 아니다. **선언적 위임 가능 영역은 여전히 20% 이하**. 나머지는 thoughtful setup, prompting, supervision, validation, judgment가 필수 [W: Anthropic 2026].

### 2.3 역할 모델의 재편

| 모델 | 사람의 위치 | 비고 | 출처 |
|---|---|---|---|
| **Humans Outside the Loop** | 사람은 "why loop"(아이디어→소프트웨어)만, 에이전트가 "how loop"(코드)를 자유롭게 | 사실상 vibe coding | [W] Kief Morris |
| **Humans In the Loop** | 사람이 매 산출물 직접 검사 | 병목 — "Agents can generate code faster than humans can manually inspect it." | 동일 |
| **Humans On the Loop** (권장) | 사람이 harness(spec, quality check, workflow)를 설계·관리, 에이전트가 그 안에서 실행 | **2026 시니어의 새 핵심 역량** | 동일 |

---

## 3. 핵심 관점들 — DDD는 AI 시대에 어떻게 되는가

### 3.1 관점 A — "DDD는 더 중요해진다" (다수 의견)

핵심 논거:

1. **에이전트가 만드는 코드량 폭증 → 예측 가능한 패턴이 필수** [W: Khosravi 2025]. "Following design patterns is even more important now with AI code generation, since these tools generate way more code at once."
2. **에이전트는 예측 불가능한 호출 시퀀스로 숨겨진 아키텍처 결함을 표면화한다** [W: Wijesekare 2026]. "Agents don't break systems — they expose them." 따라서 도메인이 invariant를 내부에서 강제하는 DDD-style 설계가 필요.
3. **모호한 ubiquitous language는 카오스를 증폭시킨다** [W: Schleicher 2026]. "LLMs are amplifiers... when we give an AI agent ambiguous instructions where 'order' could mean a dozen different things, it amplifies the chaos."
4. **멀티 에이전트 시스템은 사실상 분산 시스템** [W: Golovko 2026] — 그런데 타입 안전성, 명시적 계약, 명확한 경계가 빠져 있다. Bounded context, schema-as-contract, anti-corruption layer가 직접 해결책.
5. **에이전트 책임 분리 = bounded context** [W: Croft 2026, Iusztin 2026]. "One or more agents represent a bounded context."
6. **AI 시대에는 DDD가 민주화된다** [W: Subramani 2025] — 코어 엔지니어만의 비전이 아니라 모두의 기본 소양.

### 3.2 관점 B — "DDD의 의식(ceremony)은 죽었지만 본질(substance)은 더 load-bearing해진다"

[W: innoq.com (Westheide, 2026)] / [W: 종합 평가]

- 형식주의(폴더 구조, 클래스 계층, 패턴 카탈로그 그대로 적용)는 가치가 떨어진다.
- 그러나 **도메인 전문성, ubiquitous language의 정확성, bounded context의 식별**은 그 어느 때보다 결정적이다.
- "BMAD wouldn't save you" — 도구가 조직 문제를 풀지 못한다. DDD가 실패하던 조직은 SDD/AI 도구로도 실패한다 [W: Westheide].

### 3.3 관점 C — "DDD는 과대평가되어 왔고 AI 시대에도 그 비중은 더 줄어든다" (소수 의견)

[C: Hacker News "DDD Is Overrated"]

- 단순 CRUD에 DDD를 적용하면 오히려 악몽이 된다.
- 3년 이상 진화시킬 비전이 없는 시스템에는 ROI가 안 나온다.
- AI가 자동으로 ubiquitous language를 추출하는 시대 [P: arXiv 2509.00140]에는 사람의 모델링 단계 자체가 줄어든다.
- 솔로 창업자 / 단일 expert 환경에서는 BMAD/SDD 같은 가벼운 spec 기반 접근이 충분 [W: Westheide의 negative case].

### 3.4 관점 D — "변형론: DDD가 멀티 에이전트 아키텍처의 1급 시민으로 흡수된다"

- 에이전트 1개 = bounded context 1개 [W: Croft, Golovko, Iusztin].
- 에이전트 간 계약 = ACL + Published Language (스키마 기반) [W: Golovko].
- Context Map = **실행 가능한 코드** (다이어그램이 아니라) [W: Golovko].
- 에이전트 토폴로지(chain, star, mesh, workflow graph) [P: arXiv 2601.12560]는 결국 context map의 한 형태로 해석 가능.
- LLM 자체를 fine-tune하면 "그 도메인의 bounded context로서의 모델"이 된다 [W: Evans 2024 InfoQ]. "Several fine-tuned models, each intended for a different purpose" = "strong separation of concerns."

### 3.5 거장 시각

- **Eric Evans (2024 Explore DDD keynote)**: LLM을 도메인의 ubiquitous language로 fine-tune해 하나의 bounded context로 다루자고 제안. "내 발언은 2024년 3월 시점이라는 점을 감안하라"는 명시적 경고 [W: InfoQ].
- **Martin Fowler (2025-08)**: "OF COURSE IT'S A BUBBLE." LLM 활용의 대부분은 fancy auto-complete. 핵심은 "experienced developer가 AI를 amplifier로 쓴다"는 것 — 아키텍처 판단·도메인 이해는 사람이 진다 [W: martinfowler.com].
- **Vaughn Vernon**: 에이전트와 Event Sourcing·CQRS 결합에 관심 표명 [W: 종합]. 직접 인용 가능한 최근 발언은 LinkedIn 위주 — 책에서는 *Implementing Domain-Driven Design* 의 패턴 카탈로그가 그대로 에이전트 시대에도 인용된다는 점을 강조.

---

## 4. DDD 패턴별 영향 분석

### 4.1 Strategic Patterns

#### Subdomain (Core / Supporting / Generic)
- **AI 시대 변화**: Generic subdomain은 점점 더 AI에게 위임 가능 — 인증, 로깅, 표준 CRUD 등. **Core subdomain은 오히려 사람의 판단·도메인 이해 비중이 늘어난다** [W: Fowler, Westheide].
- **실무 함의**: 시니어는 "Core에 시간을 더 쓰고, Generic에는 에이전트를 풀어라"는 시간 재배분.

#### Bounded Context
- **AI 시대 변화**: **에이전트 1개 = bounded context 1개** 라는 매핑이 사실상 표준 [W: Croft, Golovko, Iusztin].
- 에이전트가 한 컨텍스트에 매여 있으면 reasoning도 정확해진다 — Iusztin은 "코드를 파일 타입이 아니라 actionability(bounded context) 기준으로 조직하라"고 권한다.
- "Inventory Management 에이전트가 모든 재고 상호작용을 캡슐화" 같은 구체적 매핑 [W: Croft].

#### Context Map
- **AI 시대 변화**: 다이어그램에서 **실행 가능한 코드(config + adapter + schema)** 로 격상 [W: Golovko].
- upstream/downstream, contract version, adapter 구현체를 명시적으로 기술 — CI에서 검증.
- 멀티 에이전트 시스템의 토폴로지(chain, star, mesh, workflow graph) [P: arXiv 2601.12560]가 context map 패턴과 자연 매핑.

### 4.2 Tactical Patterns

#### Ubiquitous Language
- **가장 큰 변화**. AI 시대에 ubiquitous language는 **최우선 자산**으로 격상한다.
- 자동화 진척: arXiv 2509.00140 — LLM이 SE 표준 문서에서 zero-shot으로 triple을 추출해 ontology를 자동 생성하는 워크플로 [P].
- 도구화: `domain-terms.md`, `docs/glossary.md` 같은 살아있는 용어집을 모든 에이전트가 참조 [W: Schleicher, Iusztin].
- **반례 위험**: "order"의 다의성을 사전에 해결하지 않으면 LLM이 그 카오스를 증폭시킨다 [W: Schleicher].

#### Entity / Value Object / Aggregate
- **자동화 가능 영역**: 도메인 메타모델 JSON 생성 [P: arXiv 2601.20909] — 작은 fine-tuned 모델로도 syntactically correct.
- **자동화 어려운 영역**: Eisenreich et al.(2026) — DDD 5단계 중 aggregate 설계 단계는 누적 오류로 실용성이 떨어졌다 [P: arXiv 2603.26244].
- **실무 해석**: "엔티티·VO 정의는 AI가 거의 다 한다. Aggregate 경계·invariant·트랜잭션 일관성은 사람이 책임진다."

#### Repository / Factory
- AI-DLC 한국어 백서는 AI가 자율적으로 Repository/Factory도 생성하는 워크플로를 명시 [C].
- 단, Hexagonal 관점에서 Repository는 secondary port의 한 구현 — 도메인 계층이 외부에 의존하지 않도록 사람이 경계 유지 [W: Khosravi].

#### Domain Service / Domain Event
- Domain Event는 멀티 에이전트 환경에서 **에이전트 간 통신의 기본 단위**가 된다 [W: Croft, Iusztin].
- Event Storming은 AI 보조로 가속화 [W: tanstorm, Qlerify, vibemodeling.app].
- Event Sourcing + CQRS는 Vaughn Vernon이 에이전트 환경에서도 관심을 표명한 패턴.

#### Anti-Corruption Layer (ACL)
- **새로운 의미**: 같은 단어가 에이전트마다 다른 의미를 갖는 컨텍스트 사이 "**semantic firewall**" [W: Golovko].
  - 예: "function"이 코드 생성 에이전트에게는 "signature + implementation", 테스팅 에이전트에게는 "behavior contract".
- AI 시대 ACL은 단순 데이터 변환이 아니라 **의미 변환**까지 책임진다.

### 4.3 새로 등장한 패턴 / 확장된 패턴

| 패턴 | 설명 | 출처 |
|---|---|---|
| **Schema-as-Contract** | 자연어 API 대신 Pydantic/JSON Schema 같은 정형 스키마로 에이전트 간 계약 명시. 자동 검증·버저닝·셀프 도큐먼테이션 가능 | [W] Golovko |
| **Harness Engineering** | 에이전트 행동을 통제하는 spec·quality check·workflow guidance를 사람이 설계 | [W] Kief Morris |
| **Just-in-Time Context** | 모든 컨텍스트를 미리 주입하지 않고 lightweight identifier로 두고 런타임에 동적 로드 | [W] Anthropic Engineering |
| **Vibe Modeling** | 코드 생성 전에 도메인 이벤트·경계·사용자 흐름을 시각 보드에서 AI와 함께 탐색 | [W] vibemodeling.app |
| **Knowledge Priming + Design-First + Encoding Standards + Context Anchoring + Feedback Flywheel** | AI 협업의 5가지 friction 감소 패턴 | [W] Thoughtworks/Garg |
| **DDD Glossary as Living Asset** | `docs/glossary.md`가 코드·OpenAPI·DB·고객 인터페이스에 통과되는 단일 진실 | [W] Iusztin |

---

## 5. 대표 사례

### 5.1 6-Agent Claude Code 팀 (Paul Iusztin, 2026-05)

**구성**:
- **PM 에이전트** — 작업 관리, ADR 작성, DDD 글로사리 유지
- **SWE 에이전트** — Red-Green TDD, 직접 CLI(git/mongosh/gh) 사용
- **Tester 에이전트** — 적대적 E2E edge-case 검증
- **PR Reviewer 에이전트** — diff-only 리뷰, 죽은 코드·중복·테스트 커버리지·문서 준수 확인
- **On-Call 에이전트** — CI 파이프라인이 통과할 때까지 루프
- **Self-Improve 에이전트** — meta. 실행에서 교훈 스캔, 코딩 layer 갱신 제안

**원칙**:
- "No agent both writes code and decides whether the code is correct."
- 휴먼 체크포인트 2개 + 재시도 상한 5회
- 코드 조직: file type이 아니라 bounded context(=actionability)
- DDD 글로사리(`docs/glossary.md`)가 코드·OpenAPI·DB·고객 인터페이스 모두에 단일 진실

**한계 자기 인정**: "에이전트가 글로사리를 일관되게 활용하지 못하는 경우도 있다."

[W: decodingai.com 2026-05-12]

### 5.2 카카오 헤어샵 (Korean Case, 2018, 한국 DDD 도입 초기의 표준 사례)

- Entity / Value Object / Service / Repository / Factory를 JPA로 구현.
- 예약 상태 enum (READY/OK/CANCELED/WAIT_CANCEL/COMPLETED/NO_SHOW)을 비즈니스 운영진의 용어 그대로 코드에 흡수 — ubiquitous language의 한국형 사례.
- 한계: Bounded Context를 완전히 못 나누고 패키지 기반 분할에 머물렀다. 같은 DAO를 여러 컨텍스트가 공유.
- "소프트웨어의 본질은 기술이 아니라 도메인의 문제를 해결하는 것" — 저자의 핵심 메시지.

[C: brunch.co.kr/@cg4jins/7]

> **AI 시대 재해석**: 같은 도메인을 오늘 다시 시작한다면 6-Agent 팀이 각 bounded context를 책임지고, DDD 글로사리에 상태 enum을 등재해 모든 에이전트가 일관 사용하도록 설정할 수 있다.

### 5.3 FTAPI 엔터프라이즈 플랫폼 (Eisenreich et al., 2026)

- 실제 기업 요구사항으로 DDD 5단계 LLM 자동화 프레임워크를 검증.
- 1단계 ubiquitous language, 2단계 event storming 시뮬, 3단계 bounded context 식별 — 신뢰성 있게 작동.
- 4단계 aggregate 설계, 5단계 기술 아키텍처 매핑 — 앞 단계 오류 누적으로 실용성 떨어짐.
- 결론: "LLMs can enhance, but not replace, architectural expertise."

[P: arXiv 2603.26244]

### 5.4 멀티 에이전트 e-Commerce / ERP 시스템 (James Croft, 2026)

- Inventory Management 에이전트, Order Processing 에이전트, Regulatory Compliance 에이전트가 각각 bounded context.
- 각 에이전트는 도메인 전문가 어휘("policy check", "regulation clause")로 일관된 ubiquitous language.
- 에이전트 = 비즈니스 capability와 매핑 — "기술 편의로 임의로 쪼개지 않는다."

[W: jamescroft.co.uk]

### 5.5 Siemens 사례 (Nikita Golovko, 2026)

- 6개월차 prompt spaghetti의 구체적 측정값: 에이전트당 3,000+ 토큰, 그 중 85%가 파싱·통합 로직.
- DDD 4패턴 적용 후: 에이전트당 ~500 토큰, 90%가 도메인 로직.
- Schema-as-contract로 자연어 API 대체.
- Context map을 실행 가능한 코드로.

[W: gitnation.com]

### 5.6 한국 vibe coding 포기 사례 (Park Jung-hyun, 2026-03)

- 8년차 AI 엔지니어가 순수 vibe coding을 포기한 과정.
- 채팅 기능 추가 시 기존 코드 깨짐 → 검증·수정·이해 시간 증가.
- 새 워크플로: (1) 아키텍처·데이터 흐름 먼저 정의 → (2) 반복 작업만 AI 위임 → (3) 모든 코드 검증.
- "AI는 생산성을 높여주는 도구이지, 나를 대체하는 도구가 아닙니다."

[C: tech.cloud.nongshim.co.kr]

---

## 6. 논쟁점·상충 관점

### 논쟁 1: DDD는 AI 시대에 더 중요해지는가, 사라지는가?

| 관점 A — 더 중요해진다 | 관점 B — 의식은 죽고 본질은 load-bearing | 관점 C — 더 비중 줄어든다 |
|---|---|---|
| 코드 폭증, 예측 불가 호출, 의미 모호성 모두 DDD가 직접 해결 [W: Khosravi, Wijesekare, Schleicher, Golovko] | 형식주의는 가치 하락, 도메인 전문성·ULang·BC는 더 결정적 [W: Westheide] | 단순 CRUD는 DDD 없이 충분, AI가 자동 추출하면 모델링 단계 자체 축소 [C: HN, P: arXiv 2509.00140] |

### 논쟁 2: Vibe coding은 죽었나?

- **A — 사망**: production에서 안 된다 [W: Dobrohotov, C: 박정현, medevel.com]
- **B — 부활/공존**: prototyping·소규모 자동화엔 최고, 본질은 "사람이 더 깊이 관여"로 회귀(=agentic coding으로 개명) [C: 나무위키, 본 통합 해석]

### 논쟁 3: AI 코드도 "Clean code"여야 하나?

- **A — Yes**: 사람이 검토·진화시키려면 깨끗해야 [W: Khosravi, 12 principles by Mimul]
- **B — 문제 제기**: "LLM이 사람 없이도 짜고 바꾼다면 clean이 의미가 있나?" — Kief Morris가 진지하게 던진 질문. 결론은 결국 humans on the loop이 정답이라는 동의 [W: martinfowler.com]

### 논쟁 4: BMAD/SDD vs DDD

- **A — BMAD 옹호**: 리얼타임 spec 협업이 폭포수 인터뷰보다 낫다
- **B — DDD 옹호**: 도구는 조직 문제를 못 푼다, "BMAD won't save you" [W: Westheide]
- **합의 가능**: SDD는 small team / solo에 강하고, 큰 조직에서는 DDD의 emergent modeling이 여전히 필수

### 논쟁 5: 시니어의 새 핵심 역량 — "조율자" vs "harness engineer" vs "도메인 모델러"

- A — 조율자 (Anthropic 2026 Trends): 엔지니어는 코드 작성에서 에이전트 조율로 이동
- B — Harness Engineer (Morris): 에이전트 행동을 통제하는 시스템을 설계
- C — 도메인 모델러 (Fowler, Evans, Mimul): 결국 도메인 이해·아키텍처 판단이 중심
- **합의**: 세 역할은 배타적이지 않다 — 모두 "코드 한 줄보다 시스템·도메인·에이전트 행동을 설계하는 일이 중심"이라는 같은 명제의 세 면이다.

### 논쟁 6: AI가 ubiquitous language를 자율 결정해야 하나?

- **A — 인간 승인 필수**: Spec Ambiguity Resolver 같이 AI는 후보만 제시, 사람이 결정 [W: Schleicher]
- **B — 자율 추출 가능**: zero-shot triple extraction으로 ontology 자동 생성 [P: arXiv 2509.00140]
- **실무 권고**: 자동 추출 → 사람 검토 → 글로사리 등재 의 하이브리드. 핵심 어휘일수록 사람 비중 ↑.

### 논쟁 7: AI 사용은 시니어의 도메인 직관을 마모시키는가?

- **Evan Moon (2026-04)**: Yes — "뇌는 편하면 기억하지 않는다", "AI를 가장 잘 활용할 수 있는 개발자는 AI 없이도 코드를 판단할 수 있는 개발자다" [C]
- 반론은 명시적으로 발견되지 않음 — 주류 의견은 "균형이 필요하다"로 수렴.

---

## 7. 한국 실무자 목소리 / 한국어 맥락

### 7.1 한국어 DDD 표준 어휘 / 번역어 분기

- **Bounded Context**: 바운디드 컨텍스트(주류) / 경계 컨텍스트 / 제한된 맥락
- **Aggregate**: 애그리거트(주류) / 집합체 / 어그리게이트
- **Domain Event**: 도메인 이벤트 (거의 통일)
- **Ubiquitous Language**: 유비쿼터스 언어 / 공용어 / 보편 언어
- **Value Object**: 밸류 / 값 객체 / VO
- **Repository**: 리포지터리 / 저장소
- **Anti-Corruption Layer**: 부패 방지 계층 / 안티커럽션 레이어 / ACL

### 7.2 한국 입문 표준

- 최범균, *DDD Start!* — 입문서 표준 [C: medium myrealtrip]
- 인프런 "도메인 주도 설계 마이크로서비스" 강의가 여전히 인기

### 7.3 한국 실무 사례·증언

- **카카오 헤어샵** (2018, brunch.co.kr/@cg4jins/7): JPA 기반 Entity/VO/Service/Repository/Factory 적용, Bounded Context는 패키지 수준 분할에 그침 — 도입 초기의 일반적 한계.
- **8년차 AI 엔지니어의 vibe coding 포기** (tech.cloud.nongshim.co.kr, 박정현 2026-03): "코드 검증·수정·이해 시간이 오히려 늘었다", "AI는 생산성을 높여주는 도구이지, 나를 대체하는 도구가 아니다."
- **DDD가 어려운 이유** (velog/@carrykim, Kerry Kim 2026-01): "도메인 전문가와 개발자가 모여서 하나의 도메인을 분석하고, 서로 같은 언어를 사용하도록 정리하는 것이 현실적으로 어렵다." 성공 사례에서는 개발자가 1주일간 SDR 업무를 체험했다.
- **AI 시대 정체된 개발자** (Evan Moon 2026-04): "AI를 가장 잘 활용할 수 있는 개발자는 AI 없이도 코드를 판단할 수 있는 개발자다", "30분 동안 끙끙대며 직접 짠 코드가 AI가 3초 만에 생성한 코드보다 기억에 더 깊이 남는다."
- **언어 독립적 도메인 중심 코딩 12원칙** (Mimul 2026-01, 업데이트 04-26): "코드의 존재 목적은 도메인 지식을 안전하게 보존하고 발전시키는 것이다", "비즈니스 규칙은 반드시 도메인 모델 내부에 명시적으로 표현되어야 한다", "AI가 코드를 생성하고 수정하는 빈도가 높아질수록 코드가 얼마나 명확하고 의도적으로 작성되었는지가 AI의 추론 품질과 직결된다."
- **AI-DLC 한국어 백서** (Seungwoo321 GitHub): AWS 본가 방법론의 한국어 번역. AI가 자율적으로 Aggregate/VO/Entity/Domain Event/Repository/Factory를 생성하는 워크플로 — 한국 AI 자동화 방법론에서도 DDD 패턴이 1급 시민으로 자리잡음.

### 7.4 한국 문화적·조직적 함의

- 도메인 전문가와 개발자의 거리가 한국 조직 구조상 멀다(직급·부서 사일로). DDD가 어려운 핵심 이유와 AI 시대에도 그대로 유효.
- 일정 압박이 강한 환경에서 vibe coding은 매력적으로 보이지만, 박정현 사례처럼 결국 유지보수 시점에 비용이 폭증한다는 증언.
- 한국형 ubiquitous language 사례(카카오 헤어샵의 예약 상태 enum)는 비즈니스 용어를 그대로 코드에 흡수한 좋은 모범 — AI 에이전트에게도 그대로 컨텍스트 제공 가능.

---

## 8. 실무 적용 팁 (Senior / Tech Lead / Architect용)

### 8.1 시작점

1. **`docs/glossary.md`를 가장 먼저 만들어라** — Iusztin의 6-agent team도 이게 1번. 모든 에이전트 컨텍스트의 단일 진실 [W: Iusztin].
2. **에이전트당 토큰 사용량과 그 중 도메인 로직 비중을 측정하라** — Golovko 지표(~500 토큰, ~90% 도메인 로직)를 KPI로 [W: Golovko].
3. **코드 조직을 파일 타입이 아니라 bounded context로** [W: Iusztin].

### 8.2 협업 패턴

4. **"Humans On the Loop" 모델 채택** — 매 산출물 검사도 아니고, 완전 위임도 아니다. Harness를 설계·관리하라 [W: Morris].
5. **Design-First Collaboration** — capabilities → components → interactions → contracts 순서를 AI와 함께 [W: Garg].
6. **Knowledge Priming** — 모든 에이전트 세션 시작 시 프로젝트 컨텍스트(tech stack, 컨벤션, 패턴) 주입 [W: Garg].
7. **No agent both writes code and decides whether it's correct** [W: Iusztin] — 코드 짠 에이전트와 검증 에이전트를 반드시 분리.

### 8.3 도메인 모델링

8. **Vibe Modeling 단계를 코딩 전에** — 도메인 이벤트, 경계, 사용자 흐름을 시각 보드에서 AI와 탐색 [W: vibemodeling.app].
9. **Event Storming + AI 보조 도구 (Qlerify 등)** 활용 — 분산 팀 실시간 협업 [W: tanstorm].
10. **AI가 ubiquitous language 후보를 추출하면 사람이 승인** [W: Schleicher, P: arXiv 2509.00140] — 자동 vs 수동의 하이브리드.

### 8.4 패턴 적용

11. **Bounded Context = Agent 1개** 매핑을 기본으로 [W: Croft, Iusztin].
12. **Schema-as-Contract** (Pydantic, JSON Schema) — 자연어 API 금지 [W: Golovko].
13. **Anti-Corruption Layer = Semantic Firewall** — 같은 단어가 컨텍스트마다 다른 의미인 경계마다 명시 [W: Golovko].
14. **Context Map을 실행 가능 코드로** — config + adapter + schema [W: Golovko].
15. **Aggregate 설계와 invariant는 사람이 책임진다** [P: Eisenreich et al.] — AI 자동화의 한계 영역.
16. **Hexagonal 원칙 엄수**: "도메인 계층은 표준 라이브러리 외 외부 의존성 0" [W: Khosravi].

### 8.5 거버넌스·안전

17. **휴먼 체크포인트 2개 + 재시도 상한 5회**로 폭주 방지 [W: Iusztin].
18. **AI 공저 코드 보안 리뷰 의무화** — 취약점 2.74×, 에이전트 스킬 취약점 26.1%를 기억하라 [C: 박정현, P: arXiv 2602.12430].
19. **시니어는 AI 사용 전 자신의 설계안을 먼저 작성** — 생성 효과(generation effect)로 도메인 직관 마모 방지 [C: Evan Moon].
20. **Core subdomain에 사람 시간을 더 쓰고, Generic subdomain에 에이전트를 풀어라** [본 통합의 권고].

### 8.6 측정 지표

- 에이전트당 평균 토큰 수, 그 중 도메인 로직 비중
- "완전 위임 가능" 작업 비율 (Anthropic 보고 0-20% 기준)
- 글로사리 등재 용어 수 / 코드·OpenAPI·DB 컬럼·UI 카피의 일관도
- AI 공저 코드의 보안 취약점 비율
- 실제 vs 인지 생산성 격차 (METR 19% 격차 경계)

---

## 9. 참고문헌

### 9.1 웹 자료 [W]

- Khosravi, Bardia. *Backend Coding Rules for AI Coding Agents: DDD and Hexagonal Architecture*. Medium, 2025-07-12. https://medium.com/@bardia.khosravi/backend-coding-rules-for-ai-coding-agents-ddd-and-hexagonal-architecture-ecafe91c753f
- Subramani, Bhuvaneswari. *Domain Driven Design in AI-Driven Era*. DEV Community (AWS Heroes), 2025-02-18. https://dev.to/aws-heroes/domain-driven-design-in-ai-driven-era-4l3h
- Westheide, Daniel. *Spec-Driven Development is Domain-Driven Design's Impatient Cousin*. INNOQ, 2026-03-18. https://www.innoq.com/en/blog/2026/03/sdd-ddd-why-bmad-wont-save-you/
- Croft, James. *Applying Domain-Driven Design Principles to Multi-Agent AI Systems*. 2026-04-08 (rev. 2026-05-04). https://www.jamescroft.co.uk/applying-domain-driven-design-principles-to-multi-agent-ai-systems/
- InfoQ. *Eric Evans Encourages DDD Practitioners to Experiment with LLMs*. 2024-03. https://www.infoq.com/news/2024/03/Evans-ddd-experiment-llm/
- Schleicher, Daniel. *How Creating a Ubiquitous Language Ensures AI Builds What You Actually Want*. 2026-01-04. https://www.danielschleicher.com/software/engineering,/ai,/spec-driven/development/2026/01/04/removing-ambiguity-with-spec-driven-development.html
- Golovko, Nikita (Siemens). *From Prompt Spaghetti to Bounded Contexts: DDD for Agentic Codebases*. GitNation, 2026. https://gitnation.com/contents/from-prompt-spaghetti-to-bounded-contexts-ddd-for-agentic-codebases
- Wijesekare, Natasha. *When AI Agents Meet Bad Architecture: Why DDD and Cell-Based Design Start to Matter*. Medium, 2026-03-27. https://nwijesekare.medium.com/when-ai-agents-meet-bad-architecture-why-ddd-and-cell-based-design-start-to-matter-d9b42f707d86
- Iusztin, Paul. *From Vibe Coding to a Six-Agent Claude Code Team*. Decoding AI, 2026-05-12. https://www.decodingai.com/p/squid-my-agentic-coding-setup-may-2026
- Vibe Modeling. *What is Vibe Modeling?* https://www.vibemodeling.app/what-is-vibe-modeling/
- Garg, Rahul (Thoughtworks). *Patterns for Reducing Friction in AI-Assisted Development*. martinfowler.com, 2026-04-08. https://martinfowler.com/articles/reduce-friction-ai/
- Morris, Kief. *Humans and Agents in Software Engineering Loops*. martinfowler.com, 2026-03-04. https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html
- Fowler, Martin. *Some Thoughts on LLMs and Software Development*. martinfowler.com, 2025-08-28. https://martinfowler.com/articles/202508-ai-thoughts.html
- Anthropic. *2026 Agentic Coding Trends Report*. https://resources.anthropic.com/2026-agentic-coding-trends-report
- Anthropic Engineering. *Effective Context Engineering for AI Agents*. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Storm, Tania. *Event Storming + AI = Turbocharged DDD*. Medium. https://medium.com/@tanstorm/leveraging-the-power-of-event-storming-for-domain-driven-design-3350913f7fe8
- Dobrohotov, Alek. *Vibe Coding Is Dead. Long Live Agentic Coding.* Medium, 2026-02-25. https://medium.com/@aleksandardobrohotov/vibe-coding-is-dead-long-live-agentic-coding-b3957833f55d
- Mimul. *언어 독립적인 도메인 중심 코딩 원칙과 실천법 (Domain-Centric Coding Principles)*. 2026-01-29 (rev. 04-26). https://www.mimul.com/blog/ai-coding-style/
- Moon, Evan. *AI 코딩 시대, 더이상 성장하지 않는 개발자들*. 2026-04-18. https://evan-moon.github.io/2026/04/18/developers-who-stopped-growing-in-ai-era/
- AI-DLC Whitepaper (한국어 번역). https://github.com/Seungwoo321/aidlc-docs/blob/main/ai-dlc-whitepaper-ko.md

### 9.2 논문 [P]

- Eisenreich, Tobias, Husein Jusic, and Stefan Wagner. *Automating Domain-Driven Design: Experience with a Prompting Framework*. arXiv:2603.26244 (2026). https://arxiv.org/abs/2603.26244
- Wiegand, Götz-Henrik, Filip Stepniak, and Patrick Baier. *Leveraging Generative AI for Enhancing Domain-Driven Software Design*. arXiv:2601.20909 (2026), Proceedings of the Upper-Rhine Artificial Intelligence Symposium 2024. https://arxiv.org/abs/2601.20909
- Özkan, Ozan, Önder Babur, and Mark van den Brand. *Domain-Driven Design in Software Development: A Systematic Literature Review on Implementation, Challenges, and Effectiveness*. arXiv:2310.01905 (2023). https://arxiv.org/abs/2310.01905
- He, Junda, Christoph Treude, and David Lo. *LLM-Based Multi-Agent Systems for Software Engineering: Literature Review, Vision and the Road Ahead*. arXiv:2404.04834 (2024–2025). https://arxiv.org/abs/2404.04834
- *An LLM-Assisted Approach to Designing Software Architectures Using ADD*. arXiv:2506.22688 (2025). https://arxiv.org/abs/2506.22688
- *Agentic Artificial Intelligence (AI): Architectures, Taxonomies, and Evaluation of Large Language Model Agents*. arXiv:2601.12560 (2026). https://arxiv.org/abs/2601.12560
- *Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward*. arXiv:2602.12430 (2026). https://arxiv.org/abs/2602.12430
- *Large Language Model Agent: A Survey on Methodology, Applications and Challenges*. arXiv:2503.21460 (2025). https://arxiv.org/abs/2503.21460
- *A Layered Architecture for Developing and Enhancing Capabilities in LLM-Based Software Systems*. arXiv:2411.12357 (2024-11). https://arxiv.org/abs/2411.12357
- *Guidelines for Empirical Studies in Software Engineering Involving Large Language Models*. arXiv:2508.15503 (2026-03). https://arxiv.org/abs/2508.15503
- *A Survey on Code Generation with LLM-Based Agents*. arXiv:2508.00083 (2025). https://arxiv.org/abs/2508.00083
- *LLM-Based Zero-shot Triple Extraction for Automated Ontology Generation from Software Engineering Standards*. arXiv:2509.00140 (2025). https://arxiv.org/abs/2509.00140

### 9.3 커뮤니티 [C]

- Park Jung-hyun. *8년차 AI 엔지니어는 왜 바이브코딩을 포기했나?* NDS Cloud Tech Blog, 2026-03-09. https://tech.cloud.nongshim.co.kr/blog/aws/ai/3854/
- Kim, Kerry (gimseonjin616). *도메인 주도 설계(DDD), 매력적이지만 어려운 이유*. velog, 2026-01-08. https://velog.io/@carrykim/도메인-주도-설계DDD-매력적이지만-어려운-이유
- Choi Chang-gyu (@cg4jins). *카카오헤어샵의 DDD*. brunch, 2018-05-03. https://brunch.co.kr/@cg4jins/7
- Kim, Joonghyeon. *도메인 주도 설계로 소프트웨어 만들기 — 최범균님 강의 후기*. medium myrealtrip, 2020-06-09. https://medium.com/myrealtrip-product/what-is-domain-driven-design-f6fd54051590
- Hacker News Thread. *DDD Is Overrated*. item 26312652. https://news.ycombinator.com/item?id=26312652
- Hacker News Thread. *Context Engineering is the New Vibe Coding*. item 44740930. https://news.ycombinator.com/item?id=44740930
- Hacker News Thread. *From Vibe Coding to Context Engineering: 2025 in Software Development*. item 45821587. https://news.ycombinator.com/item?id=45821587
- Cursor Community Forum. *Vibe Coding Without TDD and DDD Methodology Is...* https://forum.cursor.com/t/vibe-coding-without-tdd-and-ddd-methodlogy-is/78298
- 나무위키. *바이브 코딩*. https://namu.wiki/w/바이브%20코딩
- IT World Korea. *개발자가 맞닥뜨린 갈림길… '바이브 코딩'을 배우거나, 은퇴하거나*. https://www.itworld.co.kr/article/3967678/

---

## 10. 리서치 한계 (커버하지 못한 영역)

1. **HN 본문 일부 접근 실패**: "DDD Is Overrated"(2021), "Context engineering is the new vibe coding"(2025), "From vibe coding to context engineering"(2025) 등 핵심 thread 본문이 HTTP 429로 직접 fetch 실패. 검색 요약을 통한 간접 인용으로 대체했다. 책 저술 시 댓글의 raw 인용이 필요하면 직접 확인 권장.
2. **Reddit 직접 thread 미수집**: r/programming, r/softwarearchitecture, r/ExperiencedDevs의 raw 토론은 검색 요약 수준에 머물렀다. 시간이 있다면 특정 thread를 deep dive 권장.
3. **한국 커뮤니티 표본 부족**: OKKY 라이브 토론, 네이버 카페(자바스칸 등), 디스코드 공개 로그를 직접 수집하지 못했다. 책 저술의 한국 챕터 보강이 필요하다면 OKKY 검색·디스코드 채널 추가 수집 권장.
4. **Vaughn Vernon 최신 발언**: LinkedIn 포스트가 주류이고 직접 quote 가능한 최근 인터뷰가 부족. 그의 *Implementing Domain-Driven Design* 의 정전 위치는 인용 가능하지만, 2025-2026 AI 시대 견해는 표면적 언급만 확보.
5. **국내 학술 자료(KCI/DBpia)**: 한국어 peer-reviewed DDD-LLM 논문은 별도 검색하지 않았다. 책의 학술 챕터에서 보강 필요.
6. **금융·의료·게임·ERP 등 도메인별 case study**: e-Commerce 외 다른 복잡 도메인의 구체적 AI+DDD 적용 사례는 일반론 수준에 머물렀다. 책의 사례 챕터에서 도메인 특화 자료 추가 수집 권장.
7. **Eric Evans, Vaughn Vernon, Alberto Brandolini, Mathias Verraes, Nick Tune** 등 거장의 최신(2025-2026) 발언 — 학술 논문이 아니라 InfoQ 인터뷰·키노트·트윗 형태가 주류이고, 그 중 InfoQ Evans 2024 외에는 정밀하게 풀어내지 못했다.
8. **AI 도구별 비교(Cursor vs Claude Code vs Devin vs Cody)의 DDD 친화도**: 도구별로 어떤 DDD 패턴을 잘/못 지원하는지의 비교 매트릭스는 미수집.
9. **Aggregate 자동화 한계의 실증 데이터**: Eisenreich et al.(2026)이 유일한 직접 근거. 추가 사례·실패 케이스 보강 시 책의 핵심 명제("Aggregate는 사람이 책임진다")가 더 강해진다.
10. **윤리·라이선스·IP**: AI 생성 코드의 도메인 모델 저작권, 도메인 전문가 인터뷰 데이터 활용 등은 별도 챕터로 다룰 가치가 있지만 본 리서치는 다루지 않음.
