# Reference: EventStorming for DDD Developers

대상 독자: Java/Spring(Boot) 백엔드 + React/Next.js 프론트엔드를 다루며 DDD에 진심인 중급~시니어 한국 개발자. 본 reference는 chapter-writer가 인용할 근거 모음이다. **1차 자료**는 Brandolini의 원서(`source/brandolini_original.md`)이며, `[B § …]` 표기로 챕터·섹션을 가리킨다. **2차 자료**는 URL로 표기한다.

---

## 1. EventStorming 기본 개념 (원서 기반)

### 1.1 정의와 정신
EventStorming은 "복잡한 비즈니스 도메인을 빠르게 탐색하기 위한 유연한 워크숍 포맷"이다. 큰 종이 롤(또는 무한 캔버스)과 오렌지색 sticky note 위에 **과거 시제로 적힌 Domain Event들**을 시간순으로 늘어놓는 데서 시작한다. Brandolini는 이를 "an act of Deliberate Collective Learning(의도된 집단 학습 행위)"이라 부른다 [B Preface].

핵심 정신은 세 가지로 압축할 수 있다 [B ch.1 Preface; B ch.23 "Why are Domain Events so special?"]:
- **Postpone precision** — 처음부터 정확한 명세를 시도하지 말 것. 정확함은 점진적으로 도입한다.
- **Unlimited modeling resources** — 종이·sticky·마커가 모자라는 순간 학습은 멈춘다. 풍족하게 깔아라.
- **Maximize engagement** — 가장 많은 시각을 끌어들이는 표기법이 가장 효과적이다. UML이 아니라 오렌지색 sticky를 쓰는 이유다.

### 1.2 세 가지 레벨 (스코프)
원서는 EventStorming을 **세 가지 격(格)**으로 구분한다 [B ch.4 "Running a Big Picture Workshop"; B ch.13 "Process Modeling as a cooperative game"; B ch.17 "Running a Design-Level EventStorming"].

| 레벨 | 목적 | 참가자 | 결과물 |
|------|------|--------|--------|
| **Big Picture** | 조직 전체 도메인의 전경(全景) 학습 | 전 부서·도메인 전문가·개발자 | 시간순 이벤트 타임라인, hotspot, pivotal event 후보 |
| **Process Modeling** | 특정 프로세스의 협력적 게임 | 도메인 전문가 + 기술 인력 | Event ↔ Command ↔ Policy ↔ Read Model 흐름 |
| **Software Design (Design-Level)** | Aggregate·UI·코드 설계로의 전이 | 주로 개발자 + 도메인 전문가 1~2명 | Aggregate 후보, command/event 시그니처, view 스케치 |

청중에게 중요한 메시지: Big Picture는 회의가 아니라 **발견**이다. 코드 얘기로 점프하면 그 효용이 70% 휘발한다. 반대로 Software Design 레벨은 충분히 기술적이며, 그래서 매핑이 잘 되면 곧장 Spring 코드로 흐른다.

### 1.3 핵심 빌딩 블록 [B ch.14 "Process Modeling Building Blocks"]
- **Domain Event (Orange)** — *과거 시제로 적힌, 도메인에서 일어난 사실*. "Order Placed", "Payment Received".
- **Command / Action / Decision (Blue)** — 이벤트를 유발하는 의도. "Place Order".
- **Actor / Persona (Yellow small)** — 명령을 내리는 사람.
- **Aggregate (Yellow)** — 명령을 받아 일관성을 보장하는 상태 머신.
- **External System (Pink)** — 우리 통제 밖의 시스템.
- **Policy (Lilac/Purple)** — "Whenever X happens, do Y" — 반응 규칙.
- **Read Model (Green)** — 결정을 내리기 위해 읽는 정보.
- **Hotspot (Hot Pink/Red)** — 의문·갈등·이슈를 시각화하는 sticky.
- **Pivotal Event (Orange + 색 테이프)** — 비즈니스 흐름의 중요한 분기점 [B ch.4 "Pivotal Events" §1506].

원서의 "the picture that explains everything" [B ch.14 §3696]은 다음 문장으로 요약된다:
> *"There has to be a **Pink System** between a **Blue Command** and an **Orange Event**, there has to be a **Lilac Policy** between an **Orange Event** and a **Blue Command**."* [B §3589]

이 문장이 색상 grammar의 alpha이자 omega다.

---

## 2. 색상 규약과 워크숍 절차 (원서)

### 2.1 색상 legend (확인된 standard)
원서와 2차 자료([Wikipedia](https://en.wikipedia.org/wiki/Event_storming), [Kalele blog by Vaughn Vernon](https://kalele.io/symbolsicons-for-event-storming/), [Brandolini Picture that explains everything], [Werner cheatsheet](https://github.com/wwerner/event-storming-cheatsheet))가 일치하는 색상 매핑:

| 색상 | 의미 | 비고 |
|------|------|------|
| Orange | Domain Event (과거 시제) | 가장 먼저 깔리는 sticky |
| Light Blue | Command / Decision | 보통 사각형, 짧은 동사구 |
| Light Yellow (rectangle) | Aggregate / 도메인 개념 | Software Design 단계에서 본격 등장 |
| Small Yellow / Pink (person) | Actor / Persona | 사람을 의미 |
| Pink (large rectangle) | External System | "남의 시스템", Stripe·SendGrid 등 |
| Lilac (purple) | Policy ("whenever … then …") | reactive logic |
| Hot Pink / Red | Hotspot — 미해결 의문·충돌 | "정답은 미루기"의 상징 |
| Green (rectangle) | Read Model / View / Information | 결정의 근거 |
| Dark Green | Opportunity / Bet | 새 기능·실험 후보 |

**중요한 caveat (원서 강조 [B ch.8 "Visible Legend"]):** 색상은 *grammar*이지 *규칙*이 아니다. 워크숍 벽에 항상 "Visible Legend"를 노출해 두는 것이 핵심이지, sticky 색을 두고 싸우는 것이 핵심이 아니다. 한국 팀이 자주 빠지는 함정 중 하나가 "초록색이 모자라서 못해요" 같은 색상 강박 — 그건 안티패턴이다 (섹션 8 참고).

### 2.2 Big Picture 워크숍의 6단계 [B ch.4]
1. **Kick-off** — facilitator가 한두 문장으로 도메인을 던지고 침묵. "지금부터 일어났던 사실을 오렌지에 적어주세요."
2. **Chaotic Exploration** — 모두가 동시에 sticky를 붙인다. 정렬은 나중. 침묵을 견디는 단계.
3. **Enforcing the Timeline** — 흩어진 sticky를 시간순으로 정렬. 여기서 Pivotal Event와 Swimlane이 도구로 등장 [B §1487~1610].
4. **People and Systems** — 누가 / 어떤 외부 시스템이 관여하는지 채운다. Hotspot이 본격적으로 늘어난다.
5. **Explicit Walk-through** — 전체 흐름을 역순(거꾸로) 또는 정순으로 풀어 읽으며 점검 [B §1719~1800].
6. **Problems & Opportunities → Pick your problem** — Hotspot 정렬, arrow voting으로 우선순위 [B §1881].

### 2.3 Process Modeling: 협력 게임 [B ch.13]
Process Modeling 레벨은 **"cooperative game"**으로 기술된다. 모두가 Hotspot을 0으로 만드는 것이 승리 조건. 색상 grammar가 본격적으로 작동하는 단계로, Event ↔ Command ↔ Policy ↔ Read Model의 순환을 그린다. 원서가 강조하는 시작 전략 3가지 [B ch.15 "Process modeling game strategies"]:
- **Start from the beginning** — 가장 직관적이지만 일찍 막힘.
- **Start from the end** — 가치(value)에서 거꾸로 추적. Brandolini의 추천.
- **Make a little mess** — 일부러 작은 카오스를 만들어 빠르게 시각화.

### 2.4 Software Design Level [B ch.17~22]
Big Picture가 발견이면, Software Design은 **결정**이다. Domain Event를 둘러싸고 Command·Aggregate·Read Model·Policy를 정교하게 배치하며, 다음 챕터에서 곧장 코드로 옮길 수 있는 수준까지 다듬는다. 원서가 강조하는 것:
- Aggregate를 너무 일찍 명명하지 말 것 ("Postpone aggregate naming" [B §4646]).
- Aggregate는 **상태 머신**으로 본다 [B §4835].
- Domain Event는 **state transition**의 가시화다 [B §4726].

---

## 3. Big Picture · Process Modeling · Software Design (원서)

### 3.1 레벨 간 전이 (원서)
세 레벨이 한 워크숍에 한꺼번에 일어나지 않는다. 보통 다음 시퀀스다 [B ch.9 "Workshop Aftermath"; ch.10 "Big Picture Variations"]:

```
Big Picture (1~2일)
   └─ Hotspot 우선순위
       └─ Process Modeling (특정 hotspot 영역, 0.5~1일)
           └─ Software Design (개발팀 내, 1~2일)
               └─ 코드/스토리/티켓
```

핵심은 **artifact의 휘발성을 인정**하는 것이다. 종이 롤을 회의실에 며칠 더 붙여두고 [B §3001], "정답 모델"이 아니라 "공유된 이해"를 남기는 것이 목표 [B ch.10 "How do we know we did a good job?"].

### 3.2 청중 매핑: Spring 아키텍처와 어떻게 연결되나
- **Big Picture의 Pivotal Event** ↔ **Bounded Context 경계** [B ch.6 "Discovering Bounded Contexts" §2120; 2차 자료: [ContextMapper docs](https://contextmapper.org/docs/event-storming/), [ArchiLab "DDD Crew Bounded Context"](https://www.archi-lab.io/infopages/ddd/ddd-crew-bounded-context.html)]. Brandolini는 "follow the money" 휴리스틱도 강조 [B ch.6 §2395 "Heuristic: look at the business phases"].
- **Bounded Context** ↔ **Spring Modulith의 module** [Drotbohm, [Introducing Spring Modulith](https://spring.io/blog/2022/10/21/introducing-spring-modulith/)]. Spring Modulith는 의도적으로 DDD의 module 개념을 코드에 노출시키는 toolkit이다.
- **Process Modeling의 Policy** ↔ **Spring의 `@TransactionalEventListener` / Async event consumer**.
- **Software Design의 Aggregate** ↔ **Spring Data JPA의 `@AggregateRoot` 패턴 + `@Version` 낙관적 잠금**.
- **Read Model (Green)** ↔ **CQRS read projection / 프론트엔드 React Query 캐시**.

이 매핑이 책의 척추(spine)다. 챕터 저자는 이 매핑을 풀어내면서 EventStorming 색깔이 곧장 Java/TypeScript 코드 토큰으로 환생하는 그림을 그리면 된다.

---

## 4. Pivotal Event · Hotspot · Pain Point (원서 + 보강)

### 4.1 Pivotal Event — 비즈니스 흐름의 분기점
원서 정의 [B §1506]:
> "Pivotal Events are the few most significant events in the flow. For an e-commerce website, they might look like `Article Added to Catalogue`, `Order Placed`, `Order Shipped`, `Payment Received` and `Order Delivered`."

실용 휴리스틱:
- 보통 4~5개가 적정. 너무 많으면 무의미.
- "여러 부서가 동시에 반응하는 이벤트"를 찾으면 그게 pivotal일 가능성이 높다.
- pivotal event 사이의 구간이 **bounded context 후보** [ContextMapper, ArchiLab].

### 4.2 Hotspot — 안전한 finger-pointing 타깃
원서 [B §1616~1630]은 hotspot을 "a safer target for finger-pointing"이라 표현한다. **사람**이 아닌 **모델 위의 sticky**에 화살을 돌리는 도구다. 한국 조직에서 자주 빠지는 "회의에서 누가 잘못했나"를 차단하는 facilitator 무기다.

### 4.3 Pain Point ↔ 코드 hotspot 매핑 (확장)
EventStorming의 hotspot은 워크숍 안의 시각화 도구다. 이를 **코드 hotspot**(잦은 변경·결함·복잡도가 몰린 파일)과 연결하면 워크숍이 PR·티켓·리팩토링 backlog로 흐른다.

근거 자료:
- Adam Tornhill, *Your Code as a Crime Scene* 2nd ed. — Git commit history로 hotspot 탐지, technical debt 우선순위화 [PragProg](https://pragprog.com/titles/atcrime2/your-code-as-a-crime-scene-second-edition/), [Tornhill](https://www.adamtornhill.com/), [CodeScene](https://codescene.com/).
- Michael Feathers, *Working Effectively with Legacy Code* — Seam·Sprout Method·Wrap Method로 legacy 위에 안전하게 새 코드를 얹기 [Notes](https://understandlegacycode.com/blog/key-points-of-working-effectively-with-legacy-code/).
- 워크숍 hotspot → 코드 hotspot 교차: "도메인 전문가가 갈등하는 영역" + "Git churn이 높은 폴더"가 겹친다면 그 자리가 리팩토링·재모델링 1순위.

이 다리(워크숍 hotspot ↔ 코드 hotspot)는 원서가 **명시적으로 다루지 않는 부분**이다 — 책의 차별화 포인트.

---

## 5. Spring 생태계 통합 (web/paper 갭 1·2·3)

### 5.1 Spring Modulith — Domain Event의 1급 시민화
Oliver Drotbohm이 주도하는 Spring 공식 toolkit. 모듈러 모놀리스를 Spring Boot에서 표현하는 표준화된 방법.

핵심 개념 [공식 문서: [docs.spring.io/spring-modulith](https://docs.spring.io/spring-modulith/reference/events.html), [Introducing Spring Modulith blog](https://spring.io/blog/2022/10/21/introducing-spring-modulith/), [Spring Modulith 2.0 M1 (2025)](https://spring.io/blog/2025/07/26/spring-modulith-2-0-M1-released/)]:
- **Module = Bounded Context 후보.** 패키지 단위로 모듈을 구분하고, 모듈 간 직접 의존을 ArchUnit-기반으로 금지.
- **Application Event 우선.** 모듈 간 호출은 Spring `ApplicationEventPublisher`로 도메인 이벤트를 던지는 방식. 다른 모듈의 bean을 직접 inject하지 않는다.
- **Event Publication Registry.** `@Async @TransactionalEventListener`가 실패해도 이벤트가 DB에 보존되어 재시도 가능 — Transactional Outbox의 in-process 버전.
- **Externalization.** Spring Cloud Stream / RabbitMQ / Kafka로 도메인 이벤트를 외부 브로커에 자동 발행 [ZenWave 360 — [Externalize Spring-Modulith Events](https://www.zenwave360.io/posts/Spring-Modulith-Events-Spring-Cloud-Stream-Externalizer/)].

EventStorming의 lilac Policy("whenever Order Placed → notify warehouse")가 Spring Modulith에서는 다음과 같이 표현된다:

```java
// orders 모듈
@DomainEvent
public record OrderPlaced(OrderId id, Money total) {}

// 발행
publisher.publishEvent(new OrderPlaced(order.id(), order.total()));

// warehouse 모듈
@ApplicationModuleListener   // @Async + @TransactionalEventListener
void on(OrderPlaced event) { ... }
```

[참고: Drotbohm, "A Deep Dive into Spring Application Events"](https://speakerdeck.com/olivergierke/a-deep-dive-into-spring-application-events), [GitHub odrotbohm/spring-events-deep-dive](https://github.com/odrotbohm/spring-events-deep-dive)

### 5.2 Transactional Outbox — dual write 문제 해결
워크숍에서 그려진 도메인 이벤트를 Kafka로 안전하게 내보내는 패턴.

문제 [Chris Richardson, [microservices.io](https://microservices.io/patterns/data/transactional-outbox.html)]:
- DB 저장 + Kafka 발행을 한 트랜잭션에 묶을 수 없다 (2PC 회피).
- 둘 중 하나만 성공하면 일관성 깨짐.

해법:
1. 비즈니스 트랜잭션 안에서 outbox 테이블에 이벤트 row를 INSERT.
2. 별도 relay가 outbox를 polling 또는 CDC(Debezium)로 읽어 Kafka에 발행.
3. 최소 1회 전달(at-least-once)이므로 consumer는 idempotent 처리 필요.

Spring 구현 자료:
- [Wim Deblauwe — Transactional Outbox with Spring Boot (2024)](https://www.wimdeblauwe.com/blog/2024/06/25/transactional-outbox-pattern-with-spring-boot/)
- [Spring 공식 — Outbox Pattern Strategies in Spring Cloud Stream Kafka Binder (2023)](https://spring.io/blog/2023/10/24/a-use-case-for-transactions-adapting-to-transactional-outbox-pattern/)
- [Confluent — The Transactional Outbox Pattern](https://developer.confluent.io/courses/microservices/the-transactional-outbox-pattern/)
- Spring Modulith는 in-JVM 버전을 내장. 외부 브로커가 필요해지면 Spring Cloud Stream + outbox.

### 5.3 Spring Cloud Stream — 메시지 추상화
Kafka/RabbitMQ 구체적 API 대신 `Supplier<>` / `Consumer<>` / `Function<>` 함수형 binding으로 도메인 이벤트를 발행·구독 [Baeldung — [Spring Cloud Stream](https://www.baeldung.com/spring-cloud-stream)].

```java
@Bean
public Supplier<Flux<OrderPlaced>> orderPlacedEvents() {
  return () -> sink.asFlux();
}
```

binding name: `orderPlacedEvents-out-0` → Kafka topic으로 매핑.

### 5.4 Aggregate Root 설계 — Vernon 3부작
원서에는 Aggregate 설계 규칙이 자세히 안 나온다. EventStorming은 Aggregate를 *발견*하는 도구이고, *어떻게 자르냐*는 Vernon의 영역.

**Vaughn Vernon, "Effective Aggregate Design" 3부작** [PDF link](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_3.pdf), [Kalele](https://kalele.io/effective-aggregate-design/), [DDD Community library](https://www.dddcommunity.org/library/vernon_2011/):
1. **Modeling Aggregates with DDD and Entity Framework** — small aggregate rule.
2. **Making Aggregates Work Together** — ID로만 참조 (Reference by Identity).
3. **Gaining Insight Through Discovery** — 진정한 invariant를 발견하는 과정.

핵심 4규칙 (ArchiLab 정리 — [Aggregate Design Rules](https://www.archi-lab.io/infopages/ddd/aggregate-design-rules-vernon.html)):
1. **Aggregate = transaction boundary** (한 트랜잭션 = 한 aggregate 수정).
2. **Aggregate는 작게.** 큰 aggregate는 동시성 충돌 + 메모리 부하.
3. **Aggregate 간 참조는 ID로만.**
4. **Aggregate 간 일관성은 eventual** — Domain Event로 전파.

Spring Data JPA 실전:
- `@Version` 필드로 낙관적 잠금. `OptimisticLockingFailureException`이 비즈니스 충돌을 표현 [Spring Data Relational docs — [Persisting Entities](https://docs.spring.io/spring-data/relational/reference/jdbc/entity-persistence.html), Baeldung [Optimistic Locking in JPA](https://www.baeldung.com/jpa-optimistic-locking)].
- `@DomainEvents` 메서드로 aggregate 저장 시 자동 이벤트 발행 [Spring Data JPA docs — [Publishing Events from Aggregate Roots](https://docs.spring.io/spring-data/jpa/reference/repositories/core-domain-events.html), Petter Holmström — [Publishing Domain Events with Spring Data](https://dev.to/peholmst/publishing-domain-events-with-spring-data-53m2)].

**관점 충돌 — Mauro Servienti의 "All our aggregates are wrong"** [영상](https://www.youtube.com/watch?v=hev65ozmYPI), [GitHub](https://github.com/mauroservienti/all-our-aggregates-are-wrong-demos), [Particular blog](https://particular.net/webinars/all-our-aggregates-are-wrong):
- Servienti는 "데이터 관계로 aggregate를 자르지 말고, **behavior로 잘라라**"라고 주장.
- 같은 "Customer"라도 Sales context와 Shipping context에서 서로 다른 aggregate일 수 있고, 그래야 한다.
- 한 거대한 Order aggregate 대신 OrderPlacement / OrderFulfillment / OrderBilling으로 쪼개는 식.
- EventStorming의 swimlane 발견과 이 통찰이 정확히 맞물린다.

### 5.5 Hexagonal Architecture (Ports & Adapters) — 구조의 뼈대
Tom Hombergs, *Get Your Hands Dirty on Clean Architecture* — Spring Boot에서 Hexagonal을 실전으로 구현한 정전(正典). 

핵심 개념 [Baeldung — [Hexagonal Architecture, DDD, and Spring](https://www.baeldung.com/hexagonal-architecture-ddd-spring), [happycoders](https://www.happycoders.eu/software-craftsmanship/hexagonal-architecture/)]:
- **Port = "시스템이 무엇을 하는가"** (use case interface).
- **Adapter = "외부 세계와 어떻게 연결되는가"** (REST controller, JPA repository, Kafka listener 등).
- Domain은 Spring annotation이 거의 없는 plain POJO.

EventStorming 매핑:
- Blue Command → Inbound port (use case).
- Orange Event → Outbound port (event publisher).
- Pink External System → Outbound adapter (Stripe SDK, SendGrid 등).
- Green Read Model → Inbound port (query).

이 매핑이 책의 후반부 "코드로 옮기기" 챕터의 척추가 될 수 있다.

---

## 6. NextJS·React 프론트엔드 통합 (web 갭 4)

### 6.1 EventStorming Green Read Model ↔ 프론트 캐시
원서에는 read model이 "결정을 위해 읽는 정보" 정도로만 정의된다. 실전에서 이 박스는 프론트엔드의 **서버 상태 캐시**(React Query, SWR, TanStack Query)와 정확히 1:1로 떨어진다.

근거:
- TanStack Query 공식 — [Server Rendering & Hydration](https://tanstack.com/query/latest/docs/framework/react/guides/ssr), [Advanced SSR](https://tanstack.com/query/latest/docs/framework/react/guides/advanced-ssr).
- Frontend Masters — [Combining React Server Components with React Query](https://frontendmasters.com/blog/combining-react-server-components-with-react-query-for-easy-data-management/).
- Supabase — [React Query + Next.js App Router](https://supabase.com/blog/react-query-nextjs-app-router-cache-helpers).

매핑:
- Read Model의 invalidation 트리거 = 해당 도메인 이벤트.
- `OrderPlaced` 이벤트가 발생하면 `queryClient.invalidateQueries(['orders'])` 또는 Server Component를 재요청.

### 6.2 Next.js App Router & RSC — Projection의 새 친구
Server Components는 "서버에서만 실행되는 컴포넌트"로, SQL/HTTP를 직접 호출해 markup을 만든다. CQRS의 read side projection이 그대로 RSC가 되는 시나리오:

```tsx
// app/orders/page.tsx — Server Component
async function OrdersPage() {
  const orders = await orderReadModel.list();  // CQRS read side
  return <OrderList orders={orders} />;
}
```

복잡한 인터랙티브 상태가 필요해지면 React Query를 그 위에 hydrate [Advanced SSR docs above; Prateek Surana — [Mastering data fetching with React Query and Next.js](https://prateeksurana.me/blog/mastering-data-fetching-with-react-query-and-next-js/)].

**Serverless EventSourcing + CQRS 실전 사례:** [Upstash blog — "Serverless Event Sourcing and CQRS with Next.js and Upstash"](https://upstash.com/blog/nextjs-kafka-upstash-cqrs).

### 6.3 BFF (Backend for Frontend) 패턴
EventStorming Software Design 레벨에서 "여러 aggregate를 한 화면에 보여야 함"이 보이면 BFF가 답이다. Next.js API routes를 BFF로 쓰는 것이 가장 가벼운 선택지.

자료:
- [BFF Architecture with tRPC — Pro Next.js workshop](https://www.pronextjs.dev/workshops/next-js-react-server-component-rsc-architecture-jbvxk/bff-architecture-with-t-rpc-ve20t).
- [BFF Architecture with GraphQL — Pro Next.js workshop](https://www.pronextjs.dev/workshops/next-js-react-server-component-rsc-architecture-jbvxk/bff-architecture-with-graph-ql-e20oo).
- [BFF Pattern with Next.js API Routes (DigiGeek/Medium)](https://medium.com/digigeek/bff-backend-for-frontend-pattern-with-next-js-api-routes-secure-and-scalable-architecture-d6e088a39855).
- tRPC 공식 — [trpc.io](https://trpc.io/). React Query 위에 type-safe RPC를 얹는다.

**관점 충돌:** [Rodrigo Estrada — "When BFF and GraphQL Add More Complexity Than Solutions"](https://medium.com/@rodrigo.estrada/when-backend-for-frontend-and-graphql-add-more-complexity-than-solutions-d71320d6a683). BFF·GraphQL은 도메인 경계가 단단할 때 가치가 있지, 작은 팀이 무작정 도입하면 인지부하만 늘어난다. 책에서 균형있게 다뤄야 할 지점.

---

## 7. 원격 워크숍 노하우 (web/community 갭 6)

### 7.1 Brandolini 본인의 입장 변화
원서는 한때 "EventStorming은 원격에서 잘 안 된다"고 했으나, COVID-19를 기점으로 입장이 바뀜.
- [Avanscoperta blog — "EventStorming in COVID-19 times" (2020)](https://blog.avanscoperta.it/2020/03/26/eventstorming-in-covid-19-times/).
- 원서 11장 "Big Picture in remote mode" [B §3122~3392]에 명시적 패턴 추가.

핵심 원격 패턴 [B ch.11]:
- **Split the workshop** — 길게 하루 하지 말고 여러 짧은 세션으로 분할.
- **Anticipate Structure** — 무한 캔버스에 미리 swimlane 골격을 그려놓고 시작.
- **Colors as a signature / progress indicator** — 누가 어떤 색을 썼는지로 참여도 시각화.
- **Make Modelling Log Readable** — Miro/Mural 변경 이력을 일부러 가독성 있게 유지.
- **Iterate on Copy** — sticky 색·문구를 자주 수정 가능하게.

### 7.2 도구
- **Miro 공식 템플릿:**
  - [Event Storming Process Modelling Template](https://miro.com/templates/eventstorming-process-modelling/)
  - [Event Storming Software Design Template](https://miro.com/templates/eventstorming-software-design-template/)
- **Mural** — Miro와 유사. 무한 캔버스 + sticky.
- **공식 리소스 페이지** — [eventstorming.com/resources](https://www.eventstorming.com/resources/).

### 7.3 실전 가이드
- [Selleo — How To Run A Remote Event Storming Session](https://selleo.com/blog/how-to-run-a-remote-event-storming-session).
- [Event Storming Journal — Remote Preparation Guide](https://www.eventstormingjournal.com/remote%20facilitation/remote-event-storming-your-step-by-step-preparation-guide/).
- [Tanzu — How to Conduct a Remote Event Storming Session](https://tanzu.vmware.com/content/blog/how-to-conduct-a-remote-event-storming-session).
- [Aman Agrawal — My Experience Facilitating Big Picture (2025)](https://amanagrawal.blog/2025/01/03/my-experience-facilitating-big-picture-event-storming-sessions/).

**공통 권고:** 10~15분 짧은 silent ideation + facilitated merging의 cycle. Facilitator 2명 운영(한 명은 흐름, 한 명은 hotspot/댓글 관리).

---

## 8. 안티패턴과 facilitator 가이드 (web/community 갭 7)

### 8.1 Brandolini가 직접 경고하는 안티패턴 [B ch.4, ch.7, ch.8, ch.18]
- **너무 일찍 정확함을 추구.** "Postpone precision" — sticky 문구 토씨까지 다투면 첫 30분에 워크숍이 죽는다.
- **Seats are poisonous.** 의자를 두면 사람들이 멈춘다. 서서 모델링 [B §2793].
- **Marker가 부족해서 멈춤.** "Hidden cost of a depleted marker" [B §2558] — 진심이다. 무제한으로 깔아라.
- **개발자가 코드 얘기로 점프.** Big Picture는 코드 표기법(클래스 다이어그램, ER)이 등장하는 순간 망한다.
- **"누가 답을 아는 사람"을 한 명 모시고 끝내려 함.** "Product Owner fallacy" [B ch.3 §984]. 한 사람의 머리에 도메인이 모이는 것이 곧 single point of failure.
- **The mess in the invitation is telling you something** [B §2902]. 초대장이 엉성하면 그 자체가 도메인 문제의 신호.

### 8.2 외부 facilitator 자료
- **Kenny Baas-Schwegler + Evelyn van Kelle + Gien Verschatse, *Collaborative Software Design*** (Manning, 2024) — [Google Books](https://books.google.com/books/about/Collaborative_Software_Design.html?id=kPUuEQAAQBAJ), [Weave IT](https://weave-it.org/). 핵심 메시지: "every voice shapes the software." Deep Democracy로 침묵·갈등을 다루는 facilitator 도구 모음. EventStorming�n 아니라 Example Mapping, Domain Storytelling, Wardley Mapping까지 함께 다룸.
- **Marco Heimeshoff** — [Virtual DDD sessions](https://virtualddd.com/sessions_tag/eventstorming/), [LinkedIn — DDD CQRS & Event Sourcing](https://www.linkedin.com/posts/eventstorming-by-alberto-brandolini_domain-driven-design-cqrs-and-event-sourcing-activity-6965608264654819328-Lbod). semantic modeling alignment.
- **Eric Evans, Model Exploration Whirlpool** [Weave IT — The First 15 Years](https://weave-it.org/blog/model-exploration-whirlpool-domain-driven-design-the-first-15-years/) — EventStorming + Example Mapping + CRC card + TDD를 잇는 사이클. EventStorming만으로 모든 걸 해결하려 하지 말 것의 근거.
- **DDD Academy — Production-Ready DDD course** [ddd.academy](https://ddd.academy/production-ready-ddd) — Evans 본인 + 동료들이 가르치는 현행 커리큘럼.

### 8.3 facilitator 흔한 함정 (외부 자료 종합)
- **색상 강박** — 사람들이 "이건 yellow야 orange야?"로 30분을 쓴다. facilitator는 "둘 다 붙이고 넘어가자"로 끊는다.
- **타임라인 강박** — 모든 sticky가 한 줄에 가지런해야 한다고 믿음. 실제로는 branch와 cycle이 있고, 그 자체가 정보다 [B §2597, §2609].
- **"정답 모델" 추구** — Big Picture artifact는 며칠 후 버려질 수 있고, 그래도 괜찮다 [B §3009].
- **도메인 전문가가 빠진 워크숍** — 가장 흔한 실패 원인. 개발자끼리만 모이면 그냥 ER 다이어그램이 된다.

---

## 9. 한국 개발 현장 사례 (community 갭 6·7)

원서를 한국 독자에게 옮길 때 가장 강력한 reflective surface는 한국 팀의 실제 사례다.

### 9.1 우아한형제들 (배민)
- [우아한 객체지향 (조영호 발표) — Bounded Context와 모듈 분리](https://gist.github.com/ksundong/0ac48bb80d49813235ec789cb6afea58). EventStorming을 명시하진 않지만, 도메인 경계와 모듈 분리의 정전이 된 발표. 책에서 "한국 독자에게 익숙한 출발선"으로 활용 가능.
- [우아한형제들 기술블로그 — 우아한테크러닝 4기](https://techblog.woowahan.com/5240/) — DDD/TS 사내 교육 사례.
- 우아콘 발표 — ["이벤트 스토밍 인 액션" YouTube](https://www.youtube.com/watch?v=gihxS6eE1DM) — 우아한형제들 내부에서 EventStorming을 어떻게 소개하는지에 대한 1차 자료.

### 9.2 카카오
- [tech.kakao.com — 추천팀의 DDD 도입기](https://tech.kakao.com/2022/12/12/ddd-of-recommender-team/) ([또는 posts/555](https://tech.kakao.com/posts/555)). 추천 시스템 도메인에 DDD 전술 패턴을 도입한 실전기.
- [카카오스타일 기술 블로그](https://devblog.kakaostyle.com/ko/) — PDP 서비스가 Domain-Driven 헥사고날 아키텍처로 1년간 운영된 회고 (2024).

### 9.3 컬리
- [컬리 helloworld — Database Driven Development에서 진짜 DDD로의 선회, 이벤트 스토밍 -2-](https://helloworld.kurly.com/blog/event-storming/) — 이커머스 도메인에 EventStorming을 본격 도입한 한국에서 가장 솔직한 회고 중 하나.
- [컬리 — DDD와 MSA 기반으로 좋은 서비스 개발하기](https://helloworld.kurly.com/blog/ddd-msa-service-development/) — Loose Coupling/High Cohesion 강조.

### 9.4 SK C&C / 현대자동차그룹 / 기타
- [SK C&C — 마이크로서비스 모델링 ④: 이벤트 스토밍을 통한 마이크로서비스 도출](https://engineering-skcc.github.io/microservice%20modeling/Event-Storming/).
- [현대자동차그룹 developers — 이벤트 스토밍으로 소프트웨어 설계하기](https://developers.hyundaimotorgroup.com/en).

### 9.5 개인·중소 팀의 솔직한 회고
- [오토피디아(닥터차) — 이벤트 스토밍 후기 (Medium)](https://medium.com/autopedia/%EC%9D%B4%EB%B2%A4%ED%8A%B8-%EC%8A%A4%ED%86%A0%EB%B0%8D-%ED%9B%84%EA%B8%B0-cb01794bff9f) / [blog.doctor-cha.com 원문](https://blog.doctor-cha.com/event-storming-how-and-why). **귀한 자료** — "올해 초 이벤트 스토밍을 시도했고 실패했다"는 솔직한 자기 회고. 책 도입부에 인용 가치가 큼.
- [Goodfriends 팀 — 이벤트 스토밍 도입기](https://devfancy.github.io/Goodfriends-event-storming/) — 빅픽처 단계의 전원 참여, 단계별 인원 조절 같은 실전 팁.
- [Haandol — 쉽게 설명한 이벤트 스토밍](https://haandol.github.io/2020/12/10/demystifying-event-storming.html) — 한국 독자가 가장 자주 인용하는 한국어 입문 글.
- [velog s2moon98 — DDD를 적용하기 위해 Event Storming을 시도해보았다](https://velog.io/@s2moon98/Event-Storming%EC%9D%84-%EC%8B%9C%EB%8F%84%ED%95%B4%EB%B3%B4%EC%9E%90).
- [브런치 graypool — 왜 도메인 이벤트와 이벤트 스토밍이 필요한가](https://brunch.co.kr/@graypool/2308).

### 9.6 한국 사례에서 추출되는 공통 패턴
- "단계별 인원 조정" — 한국 팀이 자주 발견하는 휴리스틱. 빅픽처는 다 같이, Software Design은 개발팀만.
- "타겟 도메인을 좁게" — 한 번에 회사 전체를 그리려다 망한 케이스가 다수.
- "지속적 업데이트" — 워크숍을 1회성 행사로 끝내지 말고 업무 프로세스에 편입.
- "Database Driven Development" 관성과의 싸움 — 컬리 글이 정확히 이 지점을 짚는다. 한국 SI/스타트업 문화 특유의 출발선.

---

## 10. 논쟁점·열린 질문

### 10.1 EventStorming vs Event Modeling (Adam Dymitruk)
| 축 | EventStorming (Brandolini) | Event Modeling (Dymitruk) |
|----|---------------------------|---------------------------|
| 목적 | 문제 공간 탐색 (discovery) | 해법 청사진 (blueprint) |
| 시간선 | branching/loop 허용 | 엄격하게 단방향 |
| Aggregate | 발견 후 명명 | horizontal swimlane으로 미리 배치 |
| UI 통합 | sketch 정도 | UI ↔ command ↔ event ↔ projection ↔ UI vertical slice를 한 화면 단위로 강제 |
| Policy | lilac sticky로 명시 | "process" / "state view"로 재명명 |

근거 자료:
- [eventmodeling.org/about](https://eventmodeling.org/about/).
- [Crafting Tech Teams — Difference between Event Storming and Event Modelling](https://craftingtechteams.substack.com/p/difference-between-event-storming).
- [Semaphore — Adam Dymitruk on Event Modeling](https://semaphore.io/blog/adam-dymitruk-event-modeling).
- [SE Radio 539 — Adam Dymitruk on Event Modeling](https://se-radio.net/2022/11/episode-539-adam-dymitruk-on-event-modeling/).

책에서 양쪽을 다루되, EventStorming을 "발견의 도구", Event Modeling을 "설계 청사진의 도구"로 자리매김해 충돌이 아니라 보완으로 그리는 게 자연스럽다.

### 10.2 DDD 없이 EventStorming만 도입 가능한가?
원서는 **Big Picture는 DDD 사전 지식 없이도 가능**하다고 명시. 반면 Software Design 레벨은 사실상 DDD 어휘(Aggregate, Bounded Context)를 요구한다. 즉 "워크숍 자체"는 DDD를 몰라도 굴러가지만, **결과를 코드로 옮기는 단계에서 DDD가 필요해진다.**

이 책의 청중은 이미 DDD에 진심이므로, 갈등은 적다. 다만 "팀 내 DDD를 모르는 동료를 어떻게 끌어오나"라는 질문은 챕터로 다룰 가치가 있음.

### 10.3 모든 회의를 EventStorming으로?
빈도 높은 함정. EventStorming은 비용이 크고(2일 워크숍 + 도메인 전문가 시간), 모든 회의 대체용이 아니다. 가벼운 경우 Example Mapping이나 Domain Storytelling이 더 낫다 [*Collaborative Software Design*, Baas-Schwegler 외].

### 10.4 Spring Modulith vs 마이크로서비스 — 어느 쪽으로 가는가
한국 팀의 가장 첨예한 결정 지점. 책의 입장 후보:
- **(추천)** 우선 Spring Modulith로 modular monolith를 만들고, 진짜로 분리가 필요한 경계에만 마이크로서비스를 뽑는다 ("modular monolith first").
- 근거: [Frankel blog — Spring Modulith: have we reached modularity maturity?](https://blog.frankel.ch/spring-modulith-modularity-maturity/), [InfoQ launch coverage](https://www.infoq.com/news/2022/11/spring-modulith-launch/).
- 반대 관점: Servienti의 SOA 시각 — 처음부터 service boundary를 분명히. 둘을 병기.

### 10.5 LLM이 EventStorming을 자동화할 수 있는가
[arXiv — "Automating Domain-Driven Design: Experience with a Prompting Framework" (2603.26244)](https://arxiv.org/html/2603.26244v1)는 LLM이 ubiquitous language와 simulated event storming까지 가속할 수 있다고 보고. 단 인간 facilitator를 대체하기보다 보완재. 책 후기에 짧게 언급해 미래 확장을 제시할 수 있음.

---

## 11. 참고문헌

### 11.1 1차 자료 (원서)
- Alberto Brandolini, *Introducing EventStorming* (Leanpub, 2021). 본 reference의 모든 `[B § …]` 표기는 `source/brandolini_original.md`의 라인 번호 또는 챕터 제목을 가리킨다.
- [eventstorming.com](https://www.eventstorming.com/) — Brandolini 공식 사이트.
- [eventstorming.com/resources](https://www.eventstorming.com/resources/) — 공식 리소스 hub.
- [Avanscoperta — EventStorming 페이지](https://www.avanscoperta.it/en/eventstorming/), [블로그](https://blog.avanscoperta.it/).
- [Ziobrando's Lair — Introducing Event Storming (2013)](https://ziobrando.blogspot.com/2013/11/introducing-event-storming.html) — Brandolini의 최초 블로그 글.

### 11.2 책
- Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (Addison-Wesley, 2003) — [Amazon](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215).
- Vaughn Vernon, *Implementing Domain-Driven Design* ("Red Book", 2013) — [vaughnvernon.com](https://vaughnvernon.com/).
- Vaughn Vernon, "Effective Aggregate Design" 3부작 (2011) — [PDF Part 3](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_3.pdf), [DDD Community library page](https://www.dddcommunity.org/library/vernon_2011/).
- Tom Hombergs, *Get Your Hands Dirty on Clean Architecture* — Hexagonal architecture in Spring Boot 정전.
- Adam Tornhill, *Your Code as a Crime Scene*, 2nd ed. (Pragmatic Bookshelf) — [PragProg](https://pragprog.com/titles/atcrime2/your-code-as-a-crime-scene-second-edition/).
- Michael Feathers, *Working Effectively with Legacy Code* (Prentice Hall, 2004) — [Notes](https://understandlegacycode.com/blog/key-points-of-working-effectively-with-legacy-code/).
- Evelyn van Kelle, Gien Verschatse, Kenny Baas-Schwegler, *Collaborative Software Design* (Manning, 2024) — [Google Books](https://books.google.com/books/about/Collaborative_Software_Design.html?id=kPUuEQAAQBAJ).
- Annegret Junker, *Mastering Domain-Driven Design: Collaborative modeling with domain storytelling, event storming, and context mapping* (BPB, 2024) — [Amazon](https://www.amazon.com/Mastering-Domain-Driven-Design-Collaborative-storytelling/dp/936589252X).

### 11.3 Spring·아키텍처
- [Spring Modulith 공식 reference — Events](https://docs.spring.io/spring-modulith/reference/events.html).
- [Spring blog — Introducing Spring Modulith (2022)](https://spring.io/blog/2022/10/21/introducing-spring-modulith/).
- [Spring blog — Spring Modulith 2.0 M1 (2025)](https://spring.io/blog/2025/07/26/spring-modulith-2-0-M1-released/).
- [Spring blog — Simplified Event Externalization with Spring Modulith (2023)](https://spring.io/blog/2023/09/22/simplified-event-externalization-with-spring-modulith/).
- [Drotbohm — A Deep Dive into Spring Application Events (Speaker Deck)](https://speakerdeck.com/olivergierke/a-deep-dive-into-spring-application-events) + [GitHub sample](https://github.com/odrotbohm/spring-events-deep-dive).
- [ArchiLab — Getting Started with Spring Modulith](https://www.archi-lab.io/infopages/spring/spring-modulith-getting-started.html).
- [xsreality/spring-modulith-with-ddd — GitHub demo](https://github.com/xsreality/spring-modulith-with-ddd).
- [InfoQ — Spring Modulith launch coverage](https://www.infoq.com/news/2022/11/spring-modulith-launch/).
- [Frankel — Spring Modulith: have we reached modularity maturity?](https://blog.frankel.ch/spring-modulith-modularity-maturity/).
- [microservices.io — Transactional Outbox](https://microservices.io/patterns/data/transactional-outbox.html).
- [Confluent course — Transactional Outbox Pattern](https://developer.confluent.io/courses/microservices/the-transactional-outbox-pattern/).
- [Wim Deblauwe — Outbox with Spring Boot (2024)](https://www.wimdeblauwe.com/blog/2024/06/25/transactional-outbox-pattern-with-spring-boot/).
- [ZenWave 360 — Externalize Spring-Modulith Events with Spring Cloud Stream](https://www.zenwave360.io/posts/Spring-Modulith-Events-Spring-Cloud-Stream-Externalizer/).
- [Baeldung — Spring Cloud Stream](https://www.baeldung.com/spring-cloud-stream).
- [Baeldung — Hexagonal Architecture, DDD, and Spring](https://www.baeldung.com/hexagonal-architecture-ddd-spring).
- [Baeldung — Optimistic Locking in JPA](https://www.baeldung.com/jpa-optimistic-locking).
- [Spring Data JPA — Publishing Events from Aggregate Roots](https://docs.spring.io/spring-data/jpa/reference/repositories/core-domain-events.html).
- [Spring Data Relational — Persisting Entities](https://docs.spring.io/spring-data/relational/reference/jdbc/entity-persistence.html).
- [Petter Holmström — Publishing Domain Events with Spring Data](https://dev.to/peholmst/publishing-domain-events-with-spring-data-53m2).
- [ArchiLab — Aggregate Design Rules according to Vaughn Vernon](https://www.archi-lab.io/infopages/ddd/aggregate-design-rules-vernon.html).
- [Mauro Servienti — All our aggregates are wrong (Particular)](https://particular.net/webinars/all-our-aggregates-are-wrong) / [YouTube](https://www.youtube.com/watch?v=hev65ozmYPI) / [GitHub demos](https://github.com/mauroservienti/all-our-aggregates-are-wrong-demos).
- [Milestone.topics.it — Someone says event, and magically, coupling goes away (2024)](https://milestone.topics.it/2024/02/16/events-magic.html).

### 11.4 Front-end·CQRS
- [TanStack Query — Server Rendering & Hydration](https://tanstack.com/query/latest/docs/framework/react/guides/ssr).
- [TanStack Query — Advanced Server Rendering](https://tanstack.com/query/latest/docs/framework/react/guides/advanced-ssr).
- [Frontend Masters — Combining RSC with React Query](https://frontendmasters.com/blog/combining-react-server-components-with-react-query-for-easy-data-management/).
- [Supabase — React Query with Next.js App Router](https://supabase.com/blog/react-query-nextjs-app-router-cache-helpers).
- [Upstash — Serverless Event Sourcing and CQRS with Next.js](https://upstash.com/blog/nextjs-kafka-upstash-cqrs).
- [Prateek Surana — Mastering data fetching with React Query and Next.js](https://prateeksurana.me/blog/mastering-data-fetching-with-react-query-and-next-js/).
- [Pro Next.js — BFF Architecture with tRPC](https://www.pronextjs.dev/workshops/next-js-react-server-component-rsc-architecture-jbvxk/bff-architecture-with-t-rpc-ve20t).
- [Pro Next.js — BFF Architecture with GraphQL](https://www.pronextjs.dev/workshops/next-js-react-server-component-rsc-architecture-jbvxk/bff-architecture-with-graph-ql-e20oo).
- [DigiGeek — BFF Pattern with Next.js API Routes](https://medium.com/digigeek/bff-backend-for-frontend-pattern-with-next-js-api-routes-secure-and-scalable-architecture-d6e088a39855).
- [tRPC 공식](https://trpc.io/).

### 11.5 Facilitation·Workshop
- [Miro — Event Storming Process Modelling Template](https://miro.com/templates/eventstorming-process-modelling/).
- [Miro — Event Storming Software Design Template](https://miro.com/templates/eventstorming-software-design-template/).
- [Selleo — How To Run A Remote Event Storming Session](https://selleo.com/blog/how-to-run-a-remote-event-storming-session).
- [Tanzu — How to Conduct a Remote Event Storming Session](https://tanzu.vmware.com/content/blog/how-to-conduct-a-remote-event-storming-session).
- [Event Storming Journal — Remote Preparation Guide](https://www.eventstormingjournal.com/remote%20facilitation/remote-event-storming-your-step-by-step-preparation-guide/).
- [Aman Agrawal — Facilitating Big Picture Event Storming Sessions (2025)](https://amanagrawal.blog/2025/01/03/my-experience-facilitating-big-picture-event-storming-sessions/).
- [Werner — Event Storming Cheatsheet (GitHub)](https://github.com/wwerner/event-storming-cheatsheet).
- [Kalele — Symbols/Icons for Event Storming](https://kalele.io/symbolsicons-for-event-storming/).
- [Virtual DDD — EventStorming sessions](https://virtualddd.com/sessions_tag/eventstorming/).
- [Weave IT — Model Exploration Whirlpool: First 15 Years](https://weave-it.org/blog/model-exploration-whirlpool-domain-driven-design-the-first-15-years/).
- [DDD Academy — Kenny Baas-Schwegler](https://ddd.academy/kenny-baas-schwegler/).
- [Xebia — EventStorming: Continuous Discovery Beyond Software Modeling](https://xebia.com/blog/eventstorming-continuous-discovery-beyond-software-modelling/).
- [VirtualDDD heuristic — Design Bounded Contexts around EventStorming Policies](https://virtualddd.com/heuristics/design-bounded-contexts-around-eventstorming-policies/).
- [ArchiLab — DDD Crew Bounded Context methods](https://www.archi-lab.io/infopages/ddd/ddd-crew-bounded-context.html).
- [ContextMapper — Model Event Storming Results](https://contextmapper.org/docs/event-storming/).

### 11.6 Event Modeling
- [eventmodeling.org](https://eventmodeling.org/) / [/about](https://eventmodeling.org/about/).
- [Crafting Tech Teams — Difference between Event Storming and Event Modelling](https://craftingtechteams.substack.com/p/difference-between-event-storming).
- [Semaphore — Adam Dymitruk interview](https://semaphore.io/blog/adam-dymitruk-event-modeling).
- [SE Radio 539 — Adam Dymitruk on Event Modeling](https://se-radio.net/2022/11/episode-539-adam-dymitruk-on-event-modeling/).

### 11.7 한국어 자료
- [haandol — 쉽게 설명한 이벤트 스토밍 (2020)](https://haandol.github.io/2020/12/10/demystifying-event-storming.html).
- [컬리 helloworld — Database Driven Development에서 진짜 DDD로의 선회](https://helloworld.kurly.com/blog/event-storming/).
- [컬리 helloworld — DDD와 MSA 기반으로 좋은 서비스 개발하기](https://helloworld.kurly.com/blog/ddd-msa-service-development/).
- [tech.kakao.com — 추천팀의 DDD 도입기](https://tech.kakao.com/2022/12/12/ddd-of-recommender-team/).
- [카카오스타일 기술 블로그](https://devblog.kakaostyle.com/ko/).
- [SK C&C Engineering — 이벤트 스토밍을 통한 마이크로서비스 도출](https://engineering-skcc.github.io/microservice%20modeling/Event-Storming/).
- [현대자동차그룹 developers — 이벤트 스토밍으로 소프트웨어 설계하기](https://developers.hyundaimotorgroup.com/en).
- [Goodfriends 팀 — 이벤트 스토밍 도입기](https://devfancy.github.io/Goodfriends-event-storming/).
- [오토피디아 / 닥터차 — 이벤트 스토밍, 어떻게 하는 것이고 왜 해야 하나요? (Medium)](https://medium.com/autopedia/%EC%9D%B4%EB%B2%A4%ED%8A%B8-%EC%8A%A4%ED%86%A0%EB%B0%8D-%ED%9B%84%EA%B8%B0-cb01794bff9f) / [blog.doctor-cha.com](https://blog.doctor-cha.com/event-storming-how-and-why).
- [velog s2moon98 — DDD를 적용하기 위해 Event Storming](https://velog.io/@s2moon98/Event-Storming%EC%9D%84-%EC%8B%9C%EB%8F%84%ED%95%B4%EB%B3%B4%EC%9E%90).
- [velog dobecom — MSA 9. 이벤트 스토밍 과정](https://velog.io/@dobecom/msa9).
- [velog suhongkim98 — DDD 이벤트스토밍](https://velog.io/@suhongkim98/MSA%EC%99%80-DDD-%EC%9D%B4%EB%B2%A4%ED%8A%B8%EC%8A%A4%ED%86%A0%EB%B0%8D-3).
- [브런치 graypool — 왜 도메인 이벤트와 이벤트 스토밍이 필요한가](https://brunch.co.kr/@graypool/2308).
- [bongholee — 이벤트스토밍, 사티어모델, 그리고 비즈니스의 지속 가능성](https://bongholee.com/ibenteuseutoming-satieomodel-geurigo-bijeuniseuyi-jisog-ganeungseong/).
- [tech.junhabaek.net — DDD 전략적 설계: 이벤트 스토밍](https://tech.junhabaek.net/ddd-%EC%A0%84%EB%9E%B5%EC%A0%81-%EC%84%A4%EA%B3%84-event-storming-%EC%9D%B4%EB%B2%A4%ED%8A%B8-%EC%BB%A4%EB%A7%A8%EB%93%9C-%EC%99%B8%EB%B6%80%EC%84%9C%EB%B9%84%EC%8A%A4-%EC%95%A1%ED%84%B0-23ea8af1f457).
- [msaschool.io — 이벤트스토밍이란?](https://www.msaschool.io/operation/design/design-three/).
- [intro-kor.msaez.io — 이벤트스토밍 (한국어 무료 코스)](https://intro-kor.msaez.io/tool/event-storming-tool/).
- [우아한형제들 우아콘 — 이벤트 스토밍 인 액션 YouTube](https://www.youtube.com/watch?v=gihxS6eE1DM).
- [우아한 객체지향 정리 — GitHub gist](https://gist.github.com/ksundong/0ac48bb80d49813235ec789cb6afea58).

### 11.8 학술
- [arXiv 2603.26244 — Automating Domain-Driven Design: Experience with a Prompting Framework](https://arxiv.org/html/2603.26244v1).
- [Vernon — Effective Aggregate Design Part III (PDF)](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_3.pdf).

### 11.9 기타 참고
- [Wikipedia — Event storming](https://en.wikipedia.org/wiki/Event_storming).
- [O'Reilly — Learning Domain-Driven Design, ch.12 EventStorming](https://www.oreilly.com/library/view/learning-domain-driven-design/9781098100124/ch12.html).
- [Bright IT — Guide: Event Storming Workshops](https://www.bright.global/en/blog/guide-to-event-storming-workshop).
- [Qlerify — Event Storming: The Complete Guide](https://www.qlerify.com/post/event-storming-the-complete-guide).
- [codecentric — EventStorming meets DDD with Alberto Brandolini: A workshop review](https://www.codecentric.de/en/knowledge-hub/blog/eventstorming-meets-domain-driven-design-with-alberto-brandolini).
- [Open Group AA Standard — Event Storming Workshop](https://pubs.opengroup.org/architecture/o-aa-standard/event-storming-workshop.html).

---

## 12. 리서치 한계 (커버하지 못한 영역)

- **한국 회사의 *비공개* 후기.** 우아콘·DEVIEW·if(kakao) 일부 발표 영상의 디테일은 검색에서 요약만 노출됨. 챕터 저자가 인용 시 실제 영상 확인 권장.
- **Brandolini 본인의 최신(2024~2026) 1차 발화.** 원서 외 블로그·강연 transcript에 직접 접근 못함. 인용 시 원서 + Avanscoperta blog로 충분.
- **Spring Modulith 2.0 GA.** 2025년 7월 M1까지만 확인. 책 출간 시점에 2.0 GA가 나왔다면 보강 필요.
- **Kenny Baas-Schwegler의 facilitator 안티패턴 목록 직접 인용.** Manning 책 *Collaborative Software Design*은 메타 정보로만 확인했고, 본문 인용은 검증 필요.
- **이벤트 모델링 한국어 사례.** 거의 없음. EventStorming 일변도.
- **DDD 없이 EventStorming만**에 대한 명시적 학술 논증.
- **AI/LLM과의 결합** (arXiv 한 편 외에는 산업 표준이 아직 미성숙).

이 영역들은 책 저술 중 chapter-writer가 필요 시 보강 검색하면 된다.
