# 부록 C. 용어집 — Brandolini ↔ Spring ↔ React 매핑

책 본문에서 EventStorming 어휘를 처음 만난 순간, *이게 내 IDE의 어느 자리에 떨어지지?*라는 질문이 자주 따라온다. 이 부록은 그 질문에 *한 줄 답*을 주기 위한 자리다. 본문을 읽다 막혔을 때 펴자. 정의를 통째로 외울 필요는 없다 — *워크숍 sticky의 색깔이 코드의 어느 토큰에 대응하는지*만 손에 잡히면 충분하다.

세 표로 나눠 정리한다. EventStorming의 핵심 grammar는 *Spring/Java 토큰*과 *React/Next 토큰*의 양쪽으로 환생한다. 그래서 같은 색의 sticky를 *백엔드 자리에서 보는 모양*과 *프론트엔드 자리에서 보는 모양*을 나란히 두는 편이 직관적이다. 마지막에는 워크숍 안에서만 쓰는 단어들과, 자주 혼동되는 표기를 정리했다.

## EventStorming 용어 → Spring / Java 토큰

| EventStorming 어휘 | 워크숍 sticky | Spring·Java 코드 토큰 | 본문 챕터 |
|---|---|---|---|
| **Domain Event** | 오렌지, 과거 시제 동사구 | `record OrderPlaced(...) implements DomainEvent` · `ApplicationEventPublisher.publishEvent()` · `@TransactionalEventListener(phase=AFTER_COMMIT)` · `AbstractAggregateRoot.registerEvent()` | 2·6·7장 |
| **Command** | 파랑, 명령형 동사구 | `record PlaceOrder(...) implements Command` · REST controller `@RequestBody` · use case inbound port의 메서드 파라미터 | 2·6장 |
| **Aggregate (Root)** | 큰 노란 사각형, 명사 | JPA `@Entity` + `@Id` + `@Version`(optimistic locking) · `AbstractAggregateRoot<Order>` · Aggregate 클래스 안의 상태 전이 메서드 | 6장 |
| **External System** | 큰 분홍, 시스템 이름 | `@Service` 외부 어댑터 · Spring Cloud OpenFeign client · Stripe/Toss SDK adapter · outbound port + outbound adapter 한 쌍 | 2·6장 |
| **Actor / Persona** | 작은 노랑 사람 모양 | Spring Security `Authentication` 주체 · `@AuthenticationPrincipal` · API caller의 `Principal` · BFF의 user context | 2장 |
| **Read Model** | 초록 사각형 | CQRS read projection 테이블 · DB materialized view · JPA `@SqlResultSetMapping` · 별도 read service · inbound port `FindOrderQuery` | 4·6·8장 |
| **Policy** | 라일락, "Whenever ... then ..." | `@TransactionalEventListener(phase=AFTER_COMMIT)` 메서드 · `@ApplicationModuleListener` · Spring `ApplicationListener<T>` | 2·5·7장 |
| **Hotspot** | 핫핑크/빨강, 자유 메모 | 워크숍 안: 안전한 finger-pointing 표적 · 코드 안: git churn 분석으로 발견되는 *hotspot 파일*(Adam Tornhill) · GitHub `// FIXME` 주석 · ADR 후보 | 3·9·11장 |
| **Pain Point** | 종종 핫핑크와 혼용 | 도메인 전문가의 운영 우려 · NFR(비기능 요구사항) · production incident 기록 | 9장 |
| **Pivotal Event** | 오렌지 + 보라색 테이프 | Bounded Context 경계 후보 · Spring Modulith `@ApplicationModule` 경계 · 모놀리스 분리의 *칼날* | 3·5장 |
| **Bounded Context** | 워크숍 후 Pivotal Event 사이 구간 | Spring Modulith `@ApplicationModule` · `@NamedInterface("api")` · 별도 Maven module · 마이크로서비스 경계 | 5장 |
| **Opportunity** | 연두/라임 sticky | 새 비즈니스 기회의 메모 · 백로그 candidate 티켓 | 본문 거의 안 다룸 |

## EventStorming 용어 → React / Next 토큰

| EventStorming 어휘 | 워크숍 sticky | React·Next.js 코드 토큰 | 본문 챕터 |
|---|---|---|---|
| **Read Model** | 초록 | Next.js App Router `app/.../page.tsx` Server Component · `fetch(url, { next: { revalidate, tags }})` · TanStack Query `useQuery({ queryKey })` · SWR `useSWR(key)` | 8장 |
| **Read Model 갱신/무효화** | 라일락(write 쪽 정책의 그림자) | `revalidatePath()` · `revalidateTag('orders')` · `queryClient.invalidateQueries({ queryKey })` · WebSocket push로의 invalidation | 8장 |
| **Command** (사용자 발생) | 파랑 | `<form action={...}>` server action · `useMutation({ mutationFn })` · Next.js Route Handler `POST` · tRPC procedure | 8장 |
| **External System** | 큰 분홍 | BFF API route · `fetch`/Axios client · tRPC procedure · Stripe Element 같은 외부 widget | 8장 |
| **Actor** | 작은 노랑 사람 | NextAuth session · `cookies()`로 읽은 세션 · middleware의 `auth()` · 클라이언트의 `useSession()` | 8장 |
| **Domain Event 도착** | 오렌지(backend → frontend) | mutation `onSuccess` 콜백 · Server-Sent Events listener · WebSocket `onmessage` · Pusher/Ably 채널 | 8장 |
| **Aggregate** | 큰 노랑 사각형 | (프론트에 *직접* 노출하지 않음. read model로 변환되어 흐른다) | 8장 |
| **Hotspot** | 핫핑크 | UX 마찰점 · 사용자 행동 로깅으로 드러나는 *드롭 자리* · Sentry/Datadog 알람 패턴 | 8·11장 |

## 워크숍 단어 사전

본문에서 *한 번 짧게 등장하고 지나간* 단어들을 한 줄씩 정리했다. 본문에서 만났는데 정의가 흐릿하다면 여기서 빠르게 확인하자.

| 단어 | 한 줄 정의 |
|---|---|
| **Big Picture** | 도메인 *전체*를 한 벽에 펼치는 워크숍 격. 두세 시간, 9명 안팎. *발견*이 목적이다. (3장) |
| **Process Modeling** | Big Picture에서 고른 한 구간을 *깊게* 푸는 워크숍 격. 두 시간, 4~5명. *Hotspot 0이 되는 cooperative game*. (4장) |
| **Software Design** | Process Modeling에서 추려진 자리를 *코드 직전*까지 정교화하는 가장 좁은 격. 개발팀 중심. (4장 끝, 5장으로 이어짐) |
| **Chaotic Exploration** | Big Picture 2단계. 사람들이 *각자* sticky를 흩뿌리는 카오스의 시간. (3장) |
| **Enforcing the Timeline** | Big Picture 3단계. 흩어진 sticky를 *시간 순*으로 정렬한다. 토론이 가장 격렬한 자리. (3장) |
| **Explicit Walk-through** | Big Picture 5단계. 흐름을 *거꾸로* 다시 읽으며 모델을 검증한다. 원격에서도 살아남는 의식. (3·10장) |
| **Postpone precision** | 정확함을 *뒤로* 미루는 정신. 첫 라운드에서는 토씨가 틀려도 괜찮다. (1·11장) |
| **Unlimited modeling resources** | sticky·마커·종이를 *풍족하게* 깔자는 원칙. *depleted marker*가 워크숍을 죽인다. (1장) |
| **Maximize engagement** | 가장 많은 시각을 끌어들이는 표기법을 쓴다. UML이 아닌 *sticky*인 이유. (1장) |
| **Visible Legend** | 회의실 벽에 *늘 보이는* 색상 범례. 5분이면 만들고, 워크숍 30분의 손실을 막는다. (2장) |
| **Pivotal Event 보라 테이프** | 오렌지 sticky 아래 가로로 붙이는 색 테이프. Bounded Context 경계 후보의 시각화. (3·5장) |
| **arrow voting** | 워크숍 마지막의 우선순위 결정 도구. 각자 두 표씩 화살표로 hotspot에 던진다. (3·9장) |
| **Seats are poisonous** | 의자를 두면 사람들이 앉고, 앉으면 멈추고, 멈추면 워크숍이 죽는다. (3·11장) |
| **Depleted marker** | 마커가 다 떨어진 5분의 작은 손실. 워크숍 에너지를 갉아먹는 흔한 자리. (1장) |
| **PO fallacy** | "이 도메인은 PO 한 명이 다 안다"는 환상. 단일 실패 지점이다. (3·11장) |
| **Sprout Method** | Michael Feathers의 리팩토링 기법. 원본을 *직접 안 고치고* 새 메서드를 옆에 만들어 한 줄 호출로 옮긴다. (9장, 부록 D) |
| **Seam** | Feathers의 어휘. *원본을 수정하지 않고도 동작을 바꿀 수 있는 자리.* (9장) |
| **Outbox pattern** | Chris Richardson이 정리한 dual-write 해법. DB·메시지 브로커에 *동시에 쓰지 않고*, DB의 outbox 테이블에 쓴 다음 별도 프로세스가 발행한다. (7장) |
| **Event Publication Registry** | Spring Modulith의 *in-process outbox*. `event_publication` 테이블 한 개로 모듈 사이 dual-write를 해결한다. (7장) |
| **Iterate on Copy** | 원격 EventStorming의 5대 패턴 중 하나. 원본 보드를 두고 *복사본*에서 실험한다. (10장) |
| **Silent Ideation** | 원격에서 chaotic exploration의 대체물. 10~15분간 말 없이 sticky만 붙인다. (10장) |

## 혼동하기 쉬운 표기 — 짚고 가자

용어가 비슷해서 자주 헷갈리는 자리 네 가지. 한 번 정리해두자.

**EventStorming(Brandolini) vs Event Modeling(Adam Dymitruk).** 이름이 비슷해서 같은 것으로 오해받는다. EventStorming은 *발견*의 도구다 — 도메인 전문가와 함께 모델을 *찾는다*. Event Modeling은 *청사진*의 도구다 — 발견된 모델을 정확한 vertical slice로 *문서화*한다. 한 팀이 둘 다 쓸 수 있다. 보통 EventStorming이 *먼저*, Event Modeling이 *그 다음*이다. (12장에서 자세히 비교)

**Aggregate(DDD)의 두 의미.** Vernon이 말하는 Aggregate는 *도메인 모델 단위* — 한 책임의 묶음이다. Spring Data JPA의 Aggregate는 *트랜잭션 일관성 경계* — `@Version`이 걸리는 자리다. 두 의미가 *대부분 일치*하지만 항상 같지는 않다. 큰 도메인 Aggregate를 *여러 JPA Entity*로 표현하는 경우가 가능하다(Embedded, ElementCollection). 워크숍에서 "Aggregate"라고 말할 때는 *도메인 단위*의 의미가, 코드에서 `@Entity`를 가리킬 때는 *영속성 경계*의 의미가 강하다. (6장)

**Domain Event vs Integration Event.** 같은 Bounded Context 안에서 흐르는 사건이 *Domain Event*다. Bounded Context 사이로 흐르는 사건이 *Integration Event*다. Spring Modulith의 `@ApplicationModuleListener`로 받는 사건은 *대부분 Domain Event*다. 같은 record를 Kafka로 흘려보낼 때 그것이 *Integration Event*가 된다. 두 자리의 *스키마 안정성 요구*가 다르다 — Integration Event는 backward compatible을 *반드시* 지켜야 한다. (7장)

**Policy vs Saga.** Policy는 *단순한 트리거*다 — "X 사건이 일어나면 Y 명령을 한다". Saga는 *여러 단계의 보상 흐름*이다 — 결제가 실패하면 재고를 다시 늘리고, 알림을 보내고, 사용자에게 메일을 보낸다. 한 자리에 *둘 다* 등장할 수 있지만, 워크숍 sticky로는 보통 *Policy*만 표시한다. Saga는 코드 단계에서 등장하는 어휘다. Spring Modulith는 Saga 자체를 직접 추상화하지는 않는다 — 여러 Policy를 *조합*해서 Saga를 구성한다. (7장에서 짧게 언급)

---

용어집은 *외우는 자료*가 아니다. *책을 읽다 멈춘 자리*에서 한 줄 답을 찾기 위한 자리다. 이 부록을 통째로 읽지 말고, 본문에서 막힐 때마다 한 줄씩 펴서 확인하자. 한 권을 다 통과한 다음에는 이 표를 *팀 위키*에 옮겨두는 편이 낫다. 다음 워크숍에서 누군가 *"이건 무슨 색이지?"*를 물을 때, 답이 한 줄로 손에 잡힌다.
