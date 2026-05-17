# AI 에이전틱 코딩 시대의 DDD 저술 계획

> 작성일: 2026-05-17
> 작성자: book-planner
> 입력: `01_reference.md`, `research/web.md`, `research/papers.md`, `research/community.md`, `toby-book-writing-style.md`
> 대상 독자: DDD를 알고 있고 AI 에이전틱 코딩을 실무에서 경험/도입 중인 시니어 개발자, 테크 리드, 아키텍트

---

## 제목 후보

1. **DDD는 죽지 않는다 — AI 에이전틱 코딩 시대에 다시 묻는 도메인 주도 설계**
   - 톤: 단언형, 도전적
   - 포지셔닝: "DDD 무용론에 맞서는 시니어 개발자의 반론서". 표지에서부터 명확한 입장 표명. AI 시대에 흔들리는 시니어·아키텍트가 손에 잡고 "그래, 이 책이 내가 찾던 답이다" 느끼게 한다.
   - 약점: 단언형이라 책 본문이 "사라지는 것도 있다"는 균형 잡힌 시각을 가질 텐데 제목과 충돌 우려.

2. **AI는 도메인을 모른다 — 에이전틱 코딩 시대, 우리가 다시 짚어야 할 것들**
   - 톤: 시적·관조적
   - 포지셔닝: "에세이형 기술서". AI의 한계와 사람의 역할을 동시에 환기. 시니어가 야간에 위스키 한 잔과 함께 읽고 싶어할 만한 책. 입문서가 아니라 같은 고민을 하는 동료의 깊은 회고.
   - 약점: 실무 적용서를 기대한 독자에게 추상적으로 보일 수 있음.

3. **에이전트의 시대, DDD는 여전히 유효한가? — 변하는 것, 살아남는 것, 사라지는 것**
   - 톤: 질문형, 분석적
   - 포지셔닝: "현재진행형 논쟁의 정리·재구성서". 제목 자체가 책의 구조를 드러낸다. 균형 잡힌 시선으로 양측 진영을 모두 비춘다. 컨퍼런스 발표를 책으로 풀어낸 듯한 진중함.
   - 약점: 제목이 길고, "질문"에 머무는 듯한 인상으로 결단력 있는 답을 원하는 독자에게 약하게 보일 수 있음.

**추천: 3번 — 에이전트의 시대, DDD는 여전히 유효한가? — 변하는 것, 살아남는 것, 사라지는 것**

이유:
- 책의 핵심 명제 다섯 가지가 모두 "어디까지 유효하고 어디는 변하는가"라는 정밀한 질문에 답하는 구조다. 제목이 책의 골격을 그대로 드러내야 한다.
- 부제 "변하는 것, 살아남는 것, 사라지는 것"이 5~7장 패턴 분석부의 기조를 미리 공표한다 — 독자가 "아, 이 책은 분류와 분석을 해주는구나" 하고 기대 정렬.
- 시니어·아키텍트는 결론을 강요하는 책보다 자기 사고를 도와주는 책을 좋아한다. 질문형이 그들의 자율성을 존중한다.
- 1번이 너무 단호하고 2번이 너무 시적인 사이의 균형점이다.

---

## 책 특성

| 항목 | 내용 |
|------|------|
| **장르** | 에세이형 기술서 (실용 적용 패턴 + 철학적 회고 + 논쟁 정리의 하이브리드). 가까운 비교 사례: Martin Fowler의 *Refactoring* 보다는 *Patterns of Enterprise Application Architecture* 의 사유 깊이에 가깝되, 한국형 평어체로 친밀하게 풀어낸다. |
| **분량** | 약 14만~17만 자 (200자 원고지 700~850매 / 한국어 기술서 기준 약 400~480쪽). 챕터당 평균 1만~1만 2천 자. 핵심 분석 챕터(5·7·8·11장)는 1만 5천 자 가까이까지. |
| **난이도** | 중급~고급. DDD 기본 개념(Entity, VO, Aggregate, Bounded Context, Ubiquitous Language)을 한 번이라도 들어본 독자를 전제로 한다. 단, 2장에서 핵심 어휘를 빠르게 재정리해 5년 전 DDD를 공부한 독자도 따라올 수 있게 한다. AI 도구 사용 경험은 Cursor/Claude Code/Copilot 중 하나라도 일주일 이상 써본 수준을 전제. |
| **독자 여정** | **진입:** "AI 도구로 코드는 빨라졌는데, 내가 설계 직관을 잃어가는 것 같다", "DDD를 어떻게 AI 시대에 적용해야 할지 모르겠다", "팀에 DDD를 도입하고 싶은데 vibe coding 흐름과 어떻게 양립시킬지 막막하다" → **출구:** "AI 시대에 DDD 패턴 중 어느 것이 강화되고 어느 것이 변형되고 어느 것이 사라지는지 분명히 안다", "내일 출근해서 `docs/glossary.md`를 만들고 첫 bounded context를 에이전트에 매핑할 자신감이 있다", "Core 도메인에 사람 시간을 어떻게 재배분해야 하는지 안다", "AI 시대의 시니어 정체성을 다시 잡았다". |

---

## 내러티브 아크

이 책은 **의문 제기 → 시대 진단 → 기초 재방문 → 논쟁 정리 → 패턴별 정밀 분석 → 실증 사례 → 사람과 팀의 영역 → 적용 전략 → 미래 전망** 의 9단 구조로 흐른다.

1~2장은 **의문 제기와 시대 진단**이다. 시니어 개발자가 AI 도구로 일하면서 느끼는 모호한 불안을 글의 첫 화두로 삼고("뭔가 빨라진 것 같은데, 정말 내가 더 잘하고 있는 것일까?"), 그 불안의 정체를 vibe coding·agentic coding·context engineering·harness engineering이라는 시대 언어로 해부한다. METR 19% 격차, Anthropic 0~20% 위임 가능성 같은 수치가 독자의 직감을 데이터로 확정해 준다.

3장은 **DDD 기초 재방문**이다. 책의 본격 논쟁에 들어가기 전, ubiquitous language·bounded context·aggregate·entity·VO·domain event·ACL·context map을 빠르게 다시 짚는다. 5년 전 *DDD Start!* 를 읽은 독자가 손때 묻은 기억을 되살릴 수 있게.

4장은 **논쟁의 한복판으로 진입**한다. "DDD는 더 중요해진다 / 의식은 죽고 본질은 더 load-bearing해진다 / 더 비중이 줄어든다"는 세 관점을 마치 토론장의 사회자처럼 차분히 펼친다. 결론을 미리 주지 않고, 다음 장들이 그 판정을 내릴 거라는 약속을 한다.

5~9장은 책의 심장부, **패턴별·자산별 정밀 분석**이다. 5장 ubiquitous language의 격상, 6장 bounded context와 agent의 매핑, 7장 aggregate와 invariant — 사람의 마지막 영역, 8장 context map과 ACL의 새로운 의미, 9장 domain event와 멀티 에이전트 통신. 각 장은 "이 패턴이 어떻게 변하는가 / 강화되는가 / 사라지는가"를 결판낸다.

10장은 **복잡 도메인 가상 프로젝트**다. 글로벌 결제 게이트웨이 사례를 들어 1~9장의 모든 개념이 한 시스템에서 어떻게 함께 작동하는지 그린다. 추상적 분석을 손에 잡히는 코드와 설계로 응축하는 장.

11~12장은 **사람과 팀의 영역**이다. 11장에서 AI 시대 팀 구성과 역할(PO, 아키텍트, 시니어, 주니어)이 어떻게 재편되는지, 한국 조직의 사일로 문제와 도메인 전문가 접근성을 정면으로 다룬다. 12장은 시니어 자신의 정체성과 학습 — Evan Moon의 "AI 없이도 코드를 판단할 수 있는 개발자가 AI를 가장 잘 쓴다"는 역설을 깊이 파고든다.

13장은 **적용 전략**이다. 책을 덮자마자 월요일 아침에 무엇을 할 것인지 — `docs/glossary.md`부터 첫 bounded context, 휴먼 체크포인트, 측정 지표까지 구체적 로드맵.

14장은 **미래 전망과 닫는 글**이다. DDD의 진화 시나리오 세 갈래(흡수·강화·잔존), AI 시대 소프트웨어 엔지니어링의 새 정의, 그리고 독자에게 남기는 마지막 권유.

이 흐름은 의도적으로 **"의문 → 진단 → 기초 → 논쟁 → 분석 → 종합 → 사람 → 행동 → 전망"** 의 곡선을 그린다. 갑작스러운 도약 없이, 한 챕터가 다음 챕터의 질문을 자연스럽게 부른다.

---

## 챕터 목록

### 1장. AI가 코드를 짜는데, 나는 왜 더 불안해질까?

- **핵심 질문:** AI 도구를 도입한 시니어 개발자가 느끼는 모호한 불안의 정체는 무엇인가? 그리고 그 불안이 우리에게 무엇을 알려주려 하는가?
- **주요 내용:**
  - 박정현(NDS Cloud Tech, 2026-03)의 8년차 AI 엔지니어 사례: 채팅 기능 하나 더 붙이려다 기존 코드가 깨졌다는 증언으로 책을 연다.
  - METR 2025의 충격적 결과: 경험 많은 개발자가 AI 도구로 실제 19% 더 느려졌는데 본인은 20% 빨라졌다고 인식했다. 인지와 실제의 격차.
  - "AI 공저 코드의 보안 취약점이 사람 코드의 2.74배"라는 NDS Cloud Tech 데이터.
  - 시니어가 느끼는 세 가지 불안: 코드 검증 비용 폭증, 도메인 직관의 마모, 팀 내 자신의 위치 모호.
  - 이 책이 다루는 핵심 질문 다섯 가지의 선언: ① DDD의 의식과 본질, ② Bounded Context와 Agent, ③ Ubiquitous Language의 격상, ④ Aggregate와 invariant의 인간 영역, ⑤ AI를 잘 쓰는 개발자의 정의.
  - "이 책을 다 읽고 나면 무엇이 달라질 것인가" — 독자에게 던지는 약속.
- **독자가 얻는 것:** 자신이 느끼던 불안의 정체를 데이터와 사례로 확인하는 위로. 동시에, 그 불안이 곧 다음 학습의 출발점이라는 자각.
- **예상 분량:** 약 9,000자
- **사용할 reference 섹션:** 2.2 생산성·역할 변화 데이터 / 5.6 한국 vibe coding 포기 사례 / 7.3 한국 실무 사례·증언 / community.md 패턴 1, 5

---

### 2장. Vibe coding부터 Harness engineering까지 — 우리는 지금 어디 서 있나?

- **핵심 질문:** AI 에이전틱 코딩 시대를 둘러싼 용어들(vibe coding, agentic coding, context engineering, harness engineering, vibe modeling)은 각각 무엇이고, 그 변천이 우리에게 말해 주는 것은 무엇인가?
- **주요 내용:**
  - Karpathy의 vibe coding(2025-02) 원형: 직관에 따라 큰 그림만 제시하고 AI에게 구체 구현 위임.
  - Dobrohotov의 "Vibe Coding Is Dead. Long Live Agentic Coding" (2026-02): 본인 사례로 본 사망 선언과 진정한 후행 평가.
  - Anthropic 2026 Trends Report: agentic coding의 정의 — 다수 에이전트가 시간·일 단위로 자율 실행, 엔지니어는 조율자.
  - Context engineering: "에이전트가 이해 못해" → "에이전트에게 컨텍스트가 없어"로의 병목 이동 (Anthropic Engineering).
  - Kief Morris의 Harness engineering: humans on the loop 모델 — spec·quality check·workflow guidance를 사람이 설계.
  - Vibe modeling (vibemodeling.app): 코드 생성 전 도메인 이벤트·경계·사용자 흐름을 시각 보드에서 AI와 함께 탐색.
  - 용어 변천이 그리는 큰 곡선: "AI에게 모두 맡긴다" → "AI에게 컨텍스트를 잘 준다" → "AI를 둘러싼 시스템을 설계한다". 사람의 역할이 코드에서 시스템·도메인 설계로 이동.
  - 한국 실무 맥락: 박정현·Evan Moon의 vibe coding 후행 평가, IT World 한국의 "바이브 코딩 배우거나 은퇴하거나" 기사.
- **독자가 얻는 것:** 흩어져 있던 신조어들의 지도. 어디까지가 마케팅이고 어디서부터가 본질적 변화인지의 분별.
- **예상 분량:** 약 11,000자
- **사용할 reference 섹션:** 1.2 AI 에이전틱 코딩과 Vibe Coding / 2.1 AI 코딩 도구 지형 / 2.3 역할 모델 재편 / community.md 패턴 3, 8

---

### 3장. DDD를 다시 펼치자 — 20년의 정전, 핵심만 빠르게

- **핵심 질문:** Eric Evans의 2003년 책이 정립한 DDD의 핵심 어휘는 지금 우리에게 여전히 무엇을 의미하는가? AI 시대 논쟁의 토대로 무엇을 다시 기억해 두어야 하는가?
- **주요 내용:**
  - DDD의 출생: 2003년 *Domain-Driven Design: Tackling Complexity in the Heart of Software*, 그리고 한국 표준 입문서로 자리잡은 최범균의 *DDD Start!*.
  - 전략적 DDD: Domain, Subdomain(Core/Supporting/Generic), Bounded Context, Context Map, Ubiquitous Language.
  - 전술적 DDD: Entity, Value Object, Aggregate, Repository, Factory, Domain Service, Domain Event, Anti-Corruption Layer.
  - Vaughn Vernon의 *Implementing Domain-Driven Design* 이 정전화한 패턴 카탈로그의 위치.
  - 한국 번역어의 분기 — 바운디드 컨텍스트 vs 경계 컨텍스트, 애그리거트 vs 집합체, 유비쿼터스 언어 vs 공용어. 이 책에서는 어떤 번역을 채택할지의 선언.
  - DDD가 약속한 것과 약속하지 못한 것: Evans 본인의 "은탄환 아님" 단서.
  - 23년이 지난 지금, 어떤 패턴이 닳지 않았고 어떤 패턴이 시대적 색이 입혀졌는지 — 다음 장들의 미리보기.
- **독자가 얻는 것:** 본격 분석에 들어가기 전 공통 어휘의 재정렬. DDD를 처음 접한 지 5년 이상 된 독자도 손때 묻은 기억을 단숨에 회복.
- **예상 분량:** 약 10,000자
- **사용할 reference 섹션:** 1.1 DDD 핵심 개념 / 7.1 한국어 DDD 표준 어휘 / 7.2 한국 입문 표준

---

### 4장. 세 진영의 격돌 — DDD는 강화되는가, 사라지는가, 변형되는가?

- **핵심 질문:** AI 시대 DDD의 운명에 대해 업계는 세 가지 입장으로 갈라져 있다. 각각의 논리적 뼈대는 무엇이고, 그 차이가 우리의 일에 어떤 의미를 갖는가?
- **주요 내용:**
  - **관점 A — 강화론:** Khosravi, Subramani, Wijesekare, Golovko, Iusztin, Croft, Schleicher. 핵심 논거: 코드량 폭증, 예측 불가능한 호출 시퀀스의 결함 표면화, 모호한 ubiquitous language의 카오스 증폭, 멀티 에이전트가 곧 분산 시스템.
  - **관점 B — 변형론 (의식은 죽고 본질은 더 load-bearing):** Daniel Westheide의 "BMAD wouldn't save you", "DDD가 실패하던 조직은 SDD/AI 도구로도 실패한다". 폴더 구조·패턴 카탈로그 같은 형식주의는 가치 하락, 도메인 전문성·ULang·BC 식별은 더 결정적.
  - **관점 C — 축소론:** Hacker News "DDD Is Overrated" 떡밥의 재림. 단순 CRUD엔 과한 추상, 3년 미만 시스템엔 ROI 미달, AI가 ULang 자동 추출하면(arXiv 2509.00140) 모델링 단계 축소.
  - **관점 D — 흡수론:** Croft, Golovko, Iusztin. DDD가 멀티 에이전트 아키텍처의 1급 시민으로 흡수된다. Agent 1개 = Bounded Context 1개.
  - 거장들의 시각: Eric Evans(2024 InfoQ) — LLM을 도메인 ULang으로 fine-tune해 하나의 bounded context로. Martin Fowler — "OF COURSE IT'S A BUBBLE", experienced developer가 AI를 amplifier로 쓴다. Vaughn Vernon — Event Sourcing/CQRS와 에이전트의 결합 관심.
  - 이 책의 입장 선언: 강화론 + 변형론 + 흡수론의 통합. 축소론은 단순 CRUD나 단명 시스템에는 정당하지만, 복잡 도메인을 다루는 시니어에게는 해당되지 않는다.
  - 다음 5~9장이 그 통합 입장을 패턴별로 입증할 것이라는 약속.
- **독자가 얻는 것:** 흩어진 의견들의 지도. 자신이 어떤 진영에 가까웠는지, 왜 그렇게 생각했는지 자각.
- **예상 분량:** 약 13,000자
- **사용할 reference 섹션:** 3.1~3.5 핵심 관점들 / 6 논쟁점들 / community.md 논쟁 A·B·C·D

---

### 5장. Ubiquitous Language의 격상 — LLM 시대의 1급 자산

- **핵심 질문:** Ubiquitous Language는 DDD의 한 패턴이었지만, LLM 시대에 왜 갑자기 모든 것의 출발점으로 격상되는가? 그리고 이를 어떻게 살아있는 자산으로 운영할 것인가?
- **주요 내용:**
  - Daniel Schleicher의 핵심 진단: "LLMs are amplifiers. 'order'가 12가지 의미일 때 AI에게 모호한 명령을 주면 카오스가 증폭된다."
  - Paul Iusztin의 6-Agent 팀: `docs/glossary.md`가 모든 산출물의 단일 진실. 코드, OpenAPI, DB 컬럼, 고객 인터페이스 모두.
  - 자동화의 진척: arXiv 2509.00140 — LLM이 SE 표준 문서에서 zero-shot으로 triple을 추출해 ontology 자동 생성.
  - 카카오 헤어샵 사례 재해석: 예약 상태 enum(READY/OK/CANCELED/WAIT_CANCEL/COMPLETED/NO_SHOW)이 운영진의 raw 비즈니스 어휘 그대로 코드까지 통과했다. AI 시대에 같은 시스템을 다시 만든다면 에이전트들에게도 같은 어휘로 컨텍스트를 줄 것이다.
  - 살아있는 글로사리 운영 패턴: 자동 추출 → 사람 검토 → 글로사리 등재의 하이브리드. 핵심 어휘일수록 사람 비중 ↑.
  - 한국 실무의 현실 — Kerry Kim(velog, 2026-01): "도메인 전문가와 개발자가 모여서 같은 언어를 쓰도록 정리하는 것이 현실적으로 어렵다." 1주일간 SDR 업무를 체험한 후에야 진짜 시작됐다는 증언.
  - 실행 체크리스트: `docs/glossary.md` 시작 템플릿, 용어 등재 워크플로, 에이전트 시스템 프롬프트에 글로사리 주입하는 패턴, CI에서 글로사리-코드 일관성 검증하는 방법.
  - Spec Ambiguity Resolver 류 도구의 위치: AI는 후보만 제시, 사람이 결정.
- **독자가 얻는 것:** 월요일 아침부터 `docs/glossary.md`를 만들 수 있는 구체적 시작점. 그리고 ULang이 왜 다른 모든 패턴의 기초가 되는지에 대한 깊은 이해.
- **예상 분량:** 약 13,000자
- **사용할 reference 섹션:** 4.2 Ubiquitous Language / 5.1 6-Agent Claude Code 팀 / 5.2 카카오 헤어샵 / 8.1 시작점·8.3 도메인 모델링 / papers.md 논문 12

---

### 6장. Bounded Context = Agent 1개 — 사실상의 산업 표준 매핑

- **핵심 질문:** "에이전트 1개 = bounded context 1개"라는 매핑이 왜 업계의 사실상 표준이 되었는가? 그것이 실무에 의미하는 바는 무엇인가?
- **주요 내용:**
  - James Croft의 e-Commerce 사례: Inventory Management 에이전트, Order Processing 에이전트, Regulatory Compliance 에이전트. 각 에이전트는 도메인 전문가 어휘로 일관된 ULang을 가진다.
  - Paul Iusztin: "코드를 파일 타입이 아니라 actionability(bounded context) 기준으로 조직하라." 에이전트가 한 컨텍스트에 매여 있으면 reasoning이 정확해진다.
  - Nikita Golovko의 Siemens 사례: 6개월차 prompt spaghetti — 에이전트당 3,000+ 토큰 중 85%가 파싱·통합 로직. DDD 4패턴 적용 후 ~500 토큰, 90%가 도메인 로직. 정량적 KPI.
  - 멀티 에이전트 토폴로지(chain, star, mesh, workflow graph; arXiv 2601.12560)가 결국 Context Map의 한 형태.
  - 에이전트 책임 분리의 강한 규칙(Iusztin): "No agent both writes code and decides whether the code is correct."
  - 에이전트 = 비즈니스 capability와 매핑 (Croft). 기술 편의로 임의 분할 금지.
  - 한계 자기 인정: Iusztin도 "에이전트가 글로사리를 일관되게 활용하지 못하는 경우가 있다"고 인정.
  - 실행 체크리스트: 첫 bounded context 식별, 에이전트 책임 정의, 에이전트 간 호출 패턴, 토큰·도메인 로직 비중 측정.
- **독자가 얻는 것:** "내일 우리 팀의 6-agent 구성을 어떻게 설계할 것인가"에 대한 구체적 청사진. 그리고 에이전트당 토큰·도메인 로직 비중이라는 새로운 KPI.
- **예상 분량:** 약 12,000자
- **사용할 reference 섹션:** 4.1 Strategic Patterns (Bounded Context, Context Map) / 5.1 6-Agent / 5.4 James Croft / 5.5 Siemens Golovko / 8.4 패턴 적용

---

### 7장. Aggregate와 invariant — 사람의 마지막 영역

- **핵심 질문:** AI가 자동화에 거의 성공한 영역과 여전히 실패하는 영역의 경계는 어디인가? 그리고 그 경계가 우리의 일과 책임에 의미하는 바는 무엇인가?
- **주요 내용:**
  - Eisenreich et al.(arXiv 2603.26244, 2026) FTAPI 사례: DDD 5단계 자동화 중 1-3단계(ULang, event storming, BC 식별)는 신뢰성 있게 작동, 4-5단계(aggregate 설계, 기술 매핑)는 누적 오류로 실용성 떨어짐. "LLMs can enhance, but not replace, architectural expertise."
  - Wiegand et al.(arXiv 2601.20909, 2026): 도메인 메타모델 JSON 생성은 Code Llama 4-bit + LoRA로도 잘 한다. Entity·VO 정의는 AI 자동화 가능 영역.
  - 자동화 가능: Entity·VO·Repository·Factory·메타모델 생성. AI-DLC 한국어 백서도 이를 명시.
  - 자동화 어려움: Aggregate 경계, invariant, 트랜잭션 일관성, cross-aggregate 정합성.
  - 왜 사람의 영역인가: aggregate는 비즈니스 규칙의 응집이고, 그 규칙은 도메인 전문가의 머릿속과 비공식 문서에 분산되어 있다. 5층 추론 chain에서 누적 오류는 폭발한다.
  - Mimul의 12원칙 중 "비즈니스 규칙은 반드시 도메인 모델 내부에 명시적으로 표현되어야 한다"의 재해석.
  - Hexagonal 원칙 엄수: "도메인 계층은 표준 라이브러리 외 외부 의존성 0" (Khosravi). AI 시대에도 사람이 지키는 원칙.
  - 실행 패턴: AI에게 entity·VO 초안 → 사람이 aggregate 경계 정의 → AI에게 repository/factory 생성 위임 → 사람이 invariant 검증 케이스 작성 → 테스터 에이전트에게 적대적 검증.
  - 시사: "Aggregate·invariant는 사람이 책임진다"는 명제가 단순한 자존심이 아니라 실증 데이터에 기반한 분업의 권고다.
- **독자가 얻는 것:** AI 자동화의 한계선에 대한 실증적 확신. 사람이 지켜야 할 영역에 대한 명확한 자기 정의.
- **예상 분량:** 약 13,000자
- **사용할 reference 섹션:** 4.2 Entity/VO/Aggregate / 5.3 FTAPI / papers.md 논문 1·2·3 / 8.4 패턴 적용 (특히 15)

---

### 8장. Context Map과 ACL의 새로운 의미 — Schema-as-Contract와 Semantic Firewall

- **핵심 질문:** 다이어그램으로 그려지던 Context Map과 데이터 변환 계층이던 ACL은 AI 시대에 어떻게 변했는가? 그리고 이 변화가 멀티 에이전트 아키텍처에 무엇을 가져오는가?
- **주요 내용:**
  - Golovko의 Context Map 격상: 더 이상 다이어그램이 아니라 **실행 가능한 코드** (config + adapter + schema). upstream/downstream, contract version, adapter 구현체 명시. CI에서 검증.
  - Schema-as-Contract 패턴: Pydantic, JSON Schema. 자연어 API 금지. 자동 검증·버저닝·셀프 도큐먼테이션.
  - ACL의 새 의미 — Semantic Firewall: 같은 단어가 컨텍스트마다 다른 의미일 때 의미 변환까지 책임진다. 예: "function"이 코드 생성 에이전트엔 "signature + implementation", 테스팅 에이전트엔 "behavior contract".
  - Customer-Supplier, Conformist, Shared Kernel, Published Language 같은 고전 Context Map 패턴이 에이전트 간 관계로 자연 매핑.
  - 에이전트 토폴로지(chain, star, mesh, workflow graph; arXiv 2601.12560)와 Context Map 패턴의 대응표.
  - Anti-Corruption Layer의 한국 사례 부재 — 카카오 헤어샵이 비즈니스 어휘를 raw로 코드에 통과시킨 것은 ACL 없는 시스템의 좋은 면과 나쁜 면을 동시에 보여준다.
  - 실행 패턴: 에이전트 간 첫 schema 정의, 버저닝 전략, contract test, semantic firewall이 필요한 경계의 식별 휴리스틱.
  - 한계: schema가 너무 엄격하면 에이전트의 자유도가 줄고, 너무 느슨하면 spaghetti로 회귀. 균형점 찾기.
- **독자가 얻는 것:** "내 시스템의 에이전트들이 자연어로 대화하던 부분을 어디부터 schema로 바꿀 것인가"의 명확한 우선순위. Context Map을 도면이 아닌 코드로 진화시키는 첫 걸음.
- **예상 분량:** 약 11,000자
- **사용할 reference 섹션:** 4.1 Context Map / 4.2 ACL / 4.3 Schema-as-Contract / 5.5 Siemens Golovko / papers.md 논문 6

---

### 9장. Domain Event와 멀티 에이전트 통신 — Event Storming의 부활

- **핵심 질문:** Domain Event는 항상 DDD의 매력적인 패턴이었지만 실무 도입은 망설여졌다. 멀티 에이전트 환경에서 Domain Event는 왜 갑자기 필수가 되는가?
- **주요 내용:**
  - Domain Event가 에이전트 간 통신의 기본 단위가 되는 이유 — 비동기, 느슨한 결합, 명시적 사실(fact), 관찰 가능성.
  - Croft·Iusztin의 멀티 에이전트 사례에서 Domain Event의 위치: "OrderPlaced", "InventoryReserved", "PaymentAuthorized" 같은 이벤트가 에이전트들을 엮는다.
  - Event Sourcing + CQRS가 에이전트 환경에서 갖는 새 의미: Vaughn Vernon의 관심 표명. 이벤트 로그가 곧 에이전트 행동의 audit trail이 된다.
  - Event Storming의 AI 보조 가속: Qlerify, tanstorm, vibemodeling.app. 분산 팀 실시간 협업.
  - "Vibe Modeling" 단계의 의미: 코드 생성 전 도메인 이벤트·경계·사용자 흐름을 시각 보드에서 AI와 함께 탐색. "vibe coding의 차량, vibe modeling은 어디로 갈지 아는 것."
  - Just-in-Time Context와의 결합: 모든 이벤트 히스토리를 미리 주입하지 않고 lightweight identifier로 두고 런타임에 동적 로드 (Anthropic Engineering).
  - 실행 패턴: 첫 Event Storming 세션을 AI와 함께 여는 방법, 도메인 이벤트 카탈로그 만들기, 에이전트 통신을 event-driven으로 전환하는 마이그레이션 패턴.
  - 한국 실무 함의 — 도메인 전문가 워크숍의 한국형 운영 (Kerry Kim의 SDR 체험 사례를 확장).
- **독자가 얻는 것:** 한 번도 시도해 보지 못한 Event Storming을 AI 도구의 도움으로 시작할 수 있는 자신감. Domain Event 중심 설계로 가는 첫 발.
- **예상 분량:** 약 10,000자
- **사용할 reference 섹션:** 4.2 Domain Service/Event / 4.3 Vibe Modeling / 3.5 거장 시각 (Vernon) / 8.3 도메인 모델링

---

### 10장. 가상 프로젝트 — 글로벌 결제 게이트웨이를 6-Agent로 설계하다

- **핵심 질문:** 1~9장의 모든 개념이 한 시스템에서 어떻게 함께 작동하는가? 충분히 복잡한 도메인을 처음부터 끝까지 AI 에이전틱 코딩 시대의 DDD로 설계해 보자.
- **주요 내용:**
  - 가상 프로젝트 설정: 글로벌 결제 게이트웨이 — 다국가, 다통화, 환불·분쟁·정산·규제 준수를 모두 다루는 충분히 복잡한 도메인. (선택지로 의료 보험 청구 시스템도 후보였으나, 결제는 한국 시니어에게 더 친숙하고 공개 도메인 지식이 풍부하므로 채택.)
  - 1단계 — Vibe Modeling 워크숍: 도메인 전문가, 시니어 개발자, AI가 함께 Event Storming. 핵심 도메인 이벤트 추출.
  - 2단계 — `docs/glossary.md` 작성: 결제 도메인의 ULang. "결제 시도(PaymentAttempt)" vs "결제 완료(Payment)", "환불(Refund)" vs "취소(Cancellation)" vs "분쟁(Dispute)"의 정밀한 정의.
  - 3단계 — Bounded Context 식별: ① 결제 처리(Payment Processing) ② 정산(Settlement) ③ 분쟁·환불(Dispute & Refund) ④ 규제 준수(Compliance) ⑤ 라우팅·라이센싱(Routing) ⑥ 부정거래 감지(Fraud Detection). 6개 BC = 6개 Agent.
  - 4단계 — Context Map을 코드로: 각 에이전트 간 Pydantic schema, contract version, adapter.
  - 5단계 — Aggregate 설계 (사람의 영역): Payment, Settlement, Dispute, Refund의 invariant. 예: "Refund는 원 Payment의 sum을 넘지 못한다", "Dispute가 진행 중인 Payment는 Settle될 수 없다".
  - 6단계 — Domain Event 카탈로그: PaymentInitiated, PaymentAuthorized, PaymentSettled, RefundRequested, DisputeOpened, ComplianceFlagRaised 등.
  - 7단계 — 6-Agent 팀 구성: PM, SWE×6 (각 BC), Tester, PR Reviewer, On-Call, Self-Improve. Iusztin의 패턴 적용.
  - 8단계 — Anti-Corruption Layer 설계: 외부 카드사 PG의 raw 응답을 내 ULang으로 번역하는 ACL. Semantic firewall로서의 ACL 사례.
  - 9단계 — 휴먼 체크포인트 설계: 어디서 사람이 반드시 개입하는가. invariant 위반 검사, 신규 도메인 이벤트 추가, schema 버저닝.
  - 10단계 — 측정 지표 운영: 에이전트당 토큰·도메인 로직 비중, 글로사리-코드 일관도, AI 공저 코드 보안 취약점 비율.
  - 의도적으로 다루지 않은 것 — 책 한 권의 가상 프로젝트는 완전체일 수 없다. 독자가 자기 도메인에 어떻게 옮길지 안내.
- **독자가 얻는 것:** 추상 개념의 손에 잡히는 응축. "내 도메인에 적용하면 이렇게 그릴 수 있겠다"는 패턴 인식.
- **예상 분량:** 약 16,000자 (책에서 가장 긴 챕터)
- **사용할 reference 섹션:** 모든 장의 종합 / 5.1 6-Agent / 5.4 Croft / 5.5 Siemens / 8 실무 적용 팁 전체

---

### 11장. AI 시대의 팀과 역할 — PO·아키텍트·시니어·주니어는 어떻게 일하는가

- **핵심 질문:** AI 에이전틱 코딩이 보편화된 팀에서 PO, 아키텍트, 시니어, 주니어의 역할은 어떻게 재편되는가? 그리고 한국 조직의 사일로 문제와 도메인 전문가 접근성을 어떻게 다룰 것인가?
- **주요 내용:**
  - Humans Outside / In / On the Loop 세 모델 재조명 (Kief Morris) — 권장은 On the Loop.
  - **PO의 역할 재편:** spec 작성이 AI 협업의 최전선. "vibe modeling" 세션의 호스트. ULang 관리의 1차 책임자.
  - **아키텍트의 역할 재편:** Bounded Context 식별과 Context Map 설계. Harness 엔지니어로서 spec·quality check·workflow guidance 설계. 에이전트 토폴로지 결정.
  - **시니어의 역할 재편:** Aggregate·invariant 책임. Core subdomain 직접 코딩. 다른 에이전트의 PR Reviewer 역할. 주니어와 AI 사이의 멘토.
  - **주니어의 역할 재편 (가장 어려운 문제):** AI가 entry-level 코드를 거의 다 만든다. 주니어는 어떻게 성장하나? 의도적 학습 시간(딥 워크), generation effect 활용(직접 짠 후 AI와 비교), Core 도메인 학습 우선.
  - **한국 조직의 사일로 문제:** Kerry Kim 사례 — 도메인 전문가와 개발자의 거리. 1주일 SDR 체험이 진짜 시작이었다. PO·기획자·디자이너·세일즈의 용어 표준화 어려움.
  - **카카오 헤어샵 사례 재해석:** 비즈니스 운영진이 쓰는 어휘를 코드까지 통과시킨 것은 ULang의 한국형 모범. 같은 시스템을 오늘 다시 한다면 6-Agent 팀이 각 BC를 책임지고 글로사리를 통과시킬 수 있다.
  - Anthropic 2026 Trends의 두 데이터: 27%가 "AI 없으면 시도조차 안 했을 작업", 0-20%만 "완전 위임 가능". 나머지는 사람의 thoughtful setup·prompting·supervision·validation·judgment.
  - 실행 체크리스트: 우리 팀의 humans on the loop 적용 단계, ULang 워크숍 진행 가이드, 주니어 학습 로드맵.
- **독자가 얻는 것:** 자기 팀의 역할 재편 청사진. 한국 조직 특유의 사일로 문제에 대한 구체적 접근법.
- **예상 분량:** 약 13,000자
- **사용할 reference 섹션:** 2.3 역할 모델 재편 / 7.3·7.4 한국 실무·문화 / 5.2 카카오 헤어샵 / community.md 패턴 2 (Kerry Kim) / 8.2 협업 패턴

---

### 12장. AI를 잘 쓰는 개발자가 된다는 것 — 시니어 정체성과 학습의 역설

- **핵심 질문:** "AI를 가장 잘 활용할 수 있는 개발자는 AI 없이도 코드를 판단할 수 있는 개발자다." 이 역설을 어떻게 받아들이고, 어떻게 자신의 학습 전략에 녹여낼 것인가?
- **주요 내용:**
  - Evan Moon의 진단(2026-04): "뇌는 편하면 기억하지 않는다", "AI에 의존할수록 코드 판단 청크가 형성되지 않는다", "30분 끙끙대며 짠 코드가 AI가 3초 만에 만든 코드보다 기억에 깊이 남는다."
  - 시니어가 직면하는 정체성 위기 — "내가 시니어인데 주니어보다 빨라야 하나, 더 잘 판단해야 하나, 둘 다인가?"
  - Generation effect: 인지심리학의 고전. 자기가 직접 만든 정보가 외부에서 받은 정보보다 기억과 이해에 강하다.
  - 실천 전략 1 — AI 사용 전 자기 설계안 먼저: 5분이라도 자기 머리로 풀어보고 AI에게 가서 비교.
  - 실천 전략 2 — Core subdomain은 직접 짠다: Generic subdomain은 AI에 풀고, 시간을 Core에 더 쓴다.
  - 실천 전략 3 — 의도적 딥 워크 시간 확보: AI 끄고 도메인 책 읽기, 도메인 전문가와 대화, 직접 손으로 모델링.
  - 실천 전략 4 — AI 산출물의 의도적 비평: PR Reviewer 에이전트 외에 자기 자신이 매일 1개는 깊이 본다.
  - 실천 전략 5 — 도메인 깊이 우선의 학습 — 새 프레임워크보다 도메인 깊이가 더 오래 간다.
  - Anthropic 2026 Trends의 27% 데이터 재해석: "AI 없으면 시도조차 안 했을 작업"이 늘어나는 것은 좋은 일이지만, "사람이 깊이 이해해야 하는 작업"은 줄어들지 않는다.
  - 시니어의 자기 점검 질문 10개: "이번 주 내 머리로 푼 문제는 몇 개인가?", "이번 주 도메인 전문가와 대화한 시간은?", "마지막으로 AI 끄고 코드를 짠 때는?" 등.
  - Mimul의 12원칙 중 "코드가 명확하고 의도적으로 작성되었는지가 AI의 추론 품질과 직결된다"의 재해석 — 결국 사람의 명확함이 AI의 품질을 결정한다.
- **독자가 얻는 것:** 자기 학습 전략의 재정렬. 시니어 정체성의 새 정의 — 코드 한 줄보다 시스템·도메인·판단·멘토링.
- **예상 분량:** 약 12,000자
- **사용할 reference 섹션:** 7.3 한국 실무 (Evan Moon, Mimul) / 6 논쟁 7 (직관 마모) / 8.5 거버넌스·안전 / community.md 패턴 5

---

### 13장. 월요일 아침의 적용 전략 — 어디서부터 시작할 것인가

- **핵심 질문:** 책을 덮자마자 우리 팀에서 무엇을 시작할 것인가? 1주, 1개월, 3개월의 구체적 로드맵은?
- **주요 내용:**
  - **1주차:** `docs/glossary.md`를 시작한다. 핵심 어휘 30개 등재. 도메인 전문가 1명과 30분 인터뷰.
  - **2주차:** 우리 시스템의 Bounded Context 후보를 종이에 그린다. 현재 모놀리스라도 논리적 경계를 선언.
  - **1개월차:** 한 BC를 골라 첫 에이전트화 시도. 시스템 프롬프트에 글로사리 주입. 측정 지표(에이전트당 토큰, 도메인 로직 비중) 설정.
  - **2개월차:** Aggregate·invariant 점검 워크숍. AI에게 적대적 케이스 생성 요청. 사람이 invariant 명세화.
  - **3개월차:** 휴먼 체크포인트 2개 + 재시도 상한 5회의 거버넌스 안착. PR Reviewer 에이전트 도입.
  - 안티패턴 8가지: ① 글로사리 없이 에이전트 늘리기 ② 한 에이전트에 여러 BC 떠넘기기 ③ schema 없이 자연어 API ④ aggregate 자동화 위임 ⑤ 코드 짠 에이전트에게 검증 맡기기 ⑥ Core subdomain을 vibe coding으로 ⑦ 보안 리뷰 생략 ⑧ 시니어가 직접 코드 안 짜기.
  - 측정 지표 카드: 에이전트당 토큰 ~500 목표 / 도메인 로직 비중 ~90% / 글로사리-코드 일관도 / AI 공저 코드 보안 취약점 비율 / METR 19% 격차 자기 점검.
  - 도구 추천 (편향 없는 정리): Claude Code, Cursor, Copilot, Devin, Qlerify, vibemodeling.app, Pydantic — 각각의 위치와 한계.
  - 한국 조직의 도입 순서 제안: PO·기획자 워크숍 → ULang 정렬 → 시니어 1명이 PoC → 팀 전파.
  - 실패해도 괜찮은 영역과 실패하면 큰일나는 영역의 구분: 사이드 프로젝트 vs Core 도메인.
- **독자가 얻는 것:** 책을 덮자마자 행동에 옮길 수 있는 구체적 단계. 그리고 무엇을 측정해야 잘하고 있는지 안다는 자신감.
- **예상 분량:** 약 11,000자
- **사용할 reference 섹션:** 8 실무 적용 팁 (8.1~8.6 전부) / 5.1 6-Agent의 휴먼 체크포인트

---

### 14장. DDD의 진화 시나리오와 우리에게 남은 일

- **핵심 질문:** 5년 후, 10년 후 DDD는 어떤 모습일까? 그리고 그 미래에서 역산해 지금 우리가 무엇을 준비해야 할까?
- **주요 내용:**
  - **시나리오 1 — 흡수:** DDD는 더 이상 별도 방법론으로 불리지 않고 AI 에이전틱 시스템의 기본 골격이 된다. Bounded Context, ULang, Aggregate, Context Map이 도구 자체에 내장된다(Cursor·Claude Code의 미래 버전이 글로사리·BC 매핑을 1급 기능으로 제공). DDD라는 이름은 사라져도 본질은 더 깊이 살아남는다.
  - **시나리오 2 — 강화:** 멀티 에이전트 시스템의 폭증과 함께 DDD가 핵심 거버넌스 방법론으로 격상. "AI 시대 시니어 = DDD를 깊이 아는 개발자"라는 등식이 굳어진다. Eric Evans의 책이 다시 베스트셀러가 된다.
  - **시나리오 3 — 잔존:** 복잡 도메인에서만 살아남고, 단순 CRUD·자동화·prototype은 SDD/BMAD/vibe coding이 차지. DDD는 enterprise·금융·의료·정부 같은 segment의 방법론으로 좁아진다.
  - 세 시나리오의 공통점: 어느 쪽이든 도메인 전문성·ULang·BC 식별의 본질은 살아남는다. 형식주의만 다른 옷을 입을 뿐.
  - 책의 미해결 영역 (의도적 한계 인정):
    - HN raw thread, Reddit deep dive, OKKY 라이브 토론의 직접 인용은 추가 보강이 필요하다.
    - Vaughn Vernon, Alberto Brandolini, Mathias Verraes, Nick Tune의 최신 발언은 더 깊이 파야 한다.
    - 도구별 DDD 친화도 비교 매트릭스, 도메인별(금융·의료·게임) 사례, AI 생성 코드의 IP·라이선스 윤리는 후속 연구·후속 책의 몫.
  - 독자에게 남기는 마지막 권유: "DDD는 죽지 않는다. 그 의식은 변하고, 본질은 더 무거워진다. 그리고 그 무게를 어깨에 지는 것은 결국 우리 — 시니어 개발자·테크 리드·아키텍트다. 월요일 아침에 `docs/glossary.md`를 열자."
  - 감사의 말 / 후속 자료 / 참고문헌 안내.
- **독자가 얻는 것:** 미래에 대한 확정된 지도는 아니지만, 어떤 미래가 와도 통할 시니어의 자기 정체성과 다음 발걸음.
- **예상 분량:** 약 9,000자
- **사용할 reference 섹션:** 10 리서치 한계 / 3.1~3.5 핵심 관점들 종합 / 1.1 Evans의 "은탄환 아님" 재림

---

## 챕터별 분량·역할 요약

| 장 | 제목 (단축) | 역할 | 예상 분량 |
|----|------------|------|-----------|
| 1 | AI가 코드를 짜는데, 나는 왜 더 불안해질까? | 의문 제기 | 9,000자 |
| 2 | Vibe coding부터 Harness engineering까지 | 시대 진단 | 11,000자 |
| 3 | DDD를 다시 펼치자 | 기초 재방문 | 10,000자 |
| 4 | 세 진영의 격돌 | 논쟁 정리 | 13,000자 |
| 5 | Ubiquitous Language의 격상 | 패턴 분석 (격상) | 13,000자 |
| 6 | Bounded Context = Agent 1개 | 패턴 분석 (흡수) | 12,000자 |
| 7 | Aggregate와 invariant | 패턴 분석 (사람의 영역) | 13,000자 |
| 8 | Context Map과 ACL의 새로운 의미 | 패턴 분석 (변형) | 11,000자 |
| 9 | Domain Event와 멀티 에이전트 통신 | 패턴 분석 (강화) | 10,000자 |
| 10 | 가상 프로젝트 — 글로벌 결제 게이트웨이 | 응축·종합 | 16,000자 |
| 11 | AI 시대의 팀과 역할 | 사람의 영역 (팀) | 13,000자 |
| 12 | AI를 잘 쓰는 개발자가 된다는 것 | 사람의 영역 (개인) | 12,000자 |
| 13 | 월요일 아침의 적용 전략 | 행동 | 11,000자 |
| 14 | DDD의 진화 시나리오와 우리에게 남은 일 | 전망·닫기 | 9,000자 |
| **합계** | | | **약 163,000자** |

---

## 자기 점검 (계획 단계)

- [x] **모든 챕터가 핵심 질문에 답하는가?** 각 챕터에 명시.
- [x] **챕터 순서에 맥이 흐르는가?** 의문→진단→기초→논쟁→분석×5→종합→사람×2→행동→전망의 9단 곡선. 갑작스러운 도약 없음.
- [x] **대상 독자 수준에 맞는가?** 중급~고급 시니어/아키텍트 전제. 3장에서 DDD 기초를 빠르게 재정리하므로 5년 전 *DDD Start!* 를 본 독자도 따라옴.
- [x] **레퍼런스 주요 자료가 빠짐없이 배치되는가?**
  - Anthropic 2026 Trends → 1, 11, 12장
  - Iusztin 6-Agent → 5, 6, 10, 11, 13장
  - Golovko Siemens → 6, 8, 10장
  - Croft e-Commerce → 6, 8장
  - Eisenreich FTAPI → 7장
  - Schleicher ULang → 4, 5장
  - Evan Moon → 1, 12장
  - 카카오 헤어샵 → 5, 11장
  - Kerry Kim → 5, 11장
  - 박정현 → 1, 2장
  - Mimul 12원칙 → 7, 12장
  - Westheide → 4장
  - HN "DDD Overrated" → 4장
  - Evans, Fowler, Vernon → 3, 4, 9, 14장
  - arXiv 12편 → 4, 5, 7, 8, 10장에 배치
- [x] **챕터 간 중복이 없는가?** 5·6·7·8·9장이 각각 다른 패턴군을 책임지고, 10장은 그 종합이라 의도된 중첩. 11·12장은 "팀" vs "개인"으로 분리. 1·2장은 "감정의 불안" vs "용어의 지도"로 분리.
- [x] **분량이 적절한가?** 합계 16만 3천 자는 한국어 기술서 약 460쪽. 사용자가 요구한 "가능한 많은, 다양한 의견과 깊이 있는 분석"에 부합. 단순 정리가 아니라 논쟁·실증·사례·전망 모두 다층 포함.

---

## 다음 단계

1. **계획 리뷰** (plan-reviewer 에이전트): 본 계획서를 audience fit·narrative flow·coverage·redundancy 기준으로 비평.
2. **리뷰 피드백 반영** (book-planner 재실행): `03_review_log.md` 생성, 필요 시 v2 작성.
3. **챕터 저술 시작** (chapter-writer): 1장부터 순차 또는 병렬 저술. Toby 평어체 + 청유형 + 수사적 질문 적극 활용.
4. **스타일 가디언 검수** (style-guardian): 각 챕터 초안의 평어체·청유형·공감 표현·외래어 절제 점검.
5. **편집·통합** (editor): 14개 챕터 + 전문 + 에필로그 + 참고문헌 + 콜로폰.
6. **표지 디자인 + EPUB 빌드** (cover-designer + epub-builder).
