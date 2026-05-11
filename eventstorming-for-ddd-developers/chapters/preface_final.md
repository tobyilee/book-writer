# 서문

DDD 책 한 권쯤은 책장에 있는 한국 백엔드 개발자에게 이 책을 권한다. *Implementing Domain-Driven Design*의 빨간 책, Eric Evans의 그 두툼한 책, 조영호의 *우아한 객체지향* 발표 자료. 어느 한 자리는 이미 통과한 독자. 그리고 월요일 아침에 IntelliJ를 열어 `com.company.order.domain` 패키지를 펼치면 어딘가 어색하다고 느끼는 독자. 책장의 지식과 화면의 코드 사이에 *건너지 못한 다리*가 있다고 느끼는 독자. 정확히 그 자리에서 이 책이 시작된다.

EventStorming은 Alberto Brandolini가 만든 워크숍 도구다. 회의실 벽에 종이 롤을 붙이고, 도메인 전문가와 개발자를 한 자리에 모아, sticky note 한 묶음으로 도메인 전체를 펼치는 도구. 한국에도 이미 많이 알려졌다. 컬리, 우아한형제들, 카카오, 오토피디아 같은 회사가 *진심으로 한 번씩 시도*해본 흔적이 블로그에 남아 있다. 그런데 그 회고들을 나란히 놓고 읽으면 묘한 공통점이 보인다 — *워크숍 자체*에 대한 자료는 영어권에 충분히 있지만, *그 워크숍이 어떻게 한국 Spring 코드로 환생하는가*에 대한 자료는 거의 없다. Brandolini의 *Introducing EventStorming*은 코드를 거의 다루지 않는다. 한국 블로그는 *워크숍을 했다*는 이야기는 있어도 *그 결과가 우리 IDE 안에서 어떻게 살아 움직이는지*까지 따라가는 글은 드물다. 그 빈자리에 이 책을 두려고 한다.

## 이 책이 약속하는 것

- 워크숍 벽 위의 *오렌지색 sticky가* Java record로, *파란색 sticky가* `PlaceOrderUseCase` 인터페이스로, *라일락 sticky가* `@TransactionalEventListener`로, *초록색 sticky가* React Query 캐시 키와 Next.js Server Component로 환생하는 *구체적인 매핑*.
- *Pivotal Event*가 Spring Modulith의 `@ApplicationModule` 경계가 되는 한 흐름. 모놀리스 한 덩어리를 *모듈러 모놀리스*로 다듬는 첫 다리.
- Domain Event가 트랜잭션을 안전하게 통과해 Kafka까지 흘러나가는 *Outbox 패턴*의 Spring Modulith 구현. Event Publication Registry, idempotency, 스키마 호환성까지.
- 워크숍의 핫핑크 sticky가 git churn 분석과 만나 *다음 스프린트의 PR 시리즈*가 되는 짧은 다리. Sprout Method까지의 실전 시나리오.
- 원격 EventStorming의 5대 패턴(Brandolini가 COVID 이후 정리)을 한국 글로벌 팀의 비대칭 시차에 맞춘 변형.
- 개발자가 facilitator 역할을 처음 맡을 때 *예외 없이* 빠지는 7가지 안티패턴. 빠진 자리에서 빠져나오는 길.

## 이 책이 약속하지 *않는* 것

- *Introducing EventStorming*의 한국어 번역도, 요약도 아니다. Brandolini의 원서는 facilitator 운영의 디테일이 훨씬 깊다. 워크숍을 본격적으로 돌리고 싶다면 한 번은 원서를 통과하자.
- DDD 입문서가 아니다. *Implementing DDD*나 조영호의 *우아한 객체지향* 정도의 사전 지식을 가정한다.
- 마이크로서비스 결정론을 따르지 않는다. *모듈러 모놀리스 먼저, 필요할 때 분리* — 이 입장을 권유형으로 추천하지만 결정은 독자의 팀이 한다.
- 모든 도메인 모델링 도구를 다루지 않는다. Event Modeling, Domain Storytelling, Example Mapping은 잠시 언급할 뿐, 본격적으로 풀지 않는다.
- 정답을 약속하지 않는다. 워크숍은 *발견*이고, 발견은 매번 *우리 팀의 자리*에서 다시 일어난다. 책은 *지도*일 뿐 *영토*가 아니다.

## 어떻게 읽으면 좋을까

책은 세 개의 방을 차례로 통과시킨다.

**워크숍의 방(1~4장)**에서는 EventStorming의 정신과 색상 grammar, 그리고 Big Picture·Process Modeling 두 워크숍의 호흡을 익힌다. Brandolini의 영토를 한국어로 다시 짠다. 다만 매 설명은 *"내 Spring 프로젝트의 `OrderService`에서는 이게 어떻게 보일까?"*라는 질문으로 착륙한다.

**코드의 방(5~8장)**에서는 워크숍에서 발견한 것이 Spring 코드로 내려온다. Pivotal Event가 Spring Modulith 모듈 경계가 되고(5장), Aggregate가 JPA + Hexagonal Architecture로 자리잡고(6장), Domain Event가 `@DomainEvents`·Outbox·Kafka로 외부화되고(7장), Read Model이 CQRS read projection·React Query·Next.js RSC로 환생한다(8장). 이 구간이 책의 척추다.

**팀의 방(9~12장)**에서는 도구·코드를 다 익힌 독자가 *팀과 조직*이라는 가장 어려운 현실로 돌아온다. 워크숍의 hotspot이 PR 백로그로 옮겨가는 다리(9장), 원격 환경에서 워크숍을 살리는 5대 패턴(10장), facilitator의 7가지 안티패턴(11장), 한국 팀의 출발선에서 첫 30분(12장).

순서대로 읽는 게 기본이다. 다만 *이미 워크숍을 한두 번 돌려본 독자*라면 1~4장은 가볍게 훑고 5장부터 본격적으로 들어가도 좋다. *현재 facilitator 역할을 맡고 있는데 곧 첫 워크숍이 잡혀 있는 독자*라면, 11장(함정)과 12장(한국 팀 시작) 두 장을 먼저 읽고 본문으로 돌아오는 경로도 있다. 부록은 워크숍 직후 *코드를 깔고 보드를 세팅하고 PR 시리즈를 그리는* 자리에서 펴자.

## 코드 환경

본문의 모든 Spring 코드는 **Spring Boot 3.x + Java 21** 위에 깔린다. 모듈러 모놀리스 도구로 **Spring Modulith 1.3.0**을 기준 삼는다(부록 A에 버전 명시). 프론트엔드 코드는 **Next.js 14 App Router + React 18 + TanStack Query 5**를 가정한다. 책이 인쇄될 시점에 Spring Modulith 2.0이 정식 릴리스됐다면 본문 7장에서 다룬 *externalization* 기능이 더 단단해져 있을 것이다. 큰 흐름은 그대로다.

## 감사

먼저 EventStorming이라는 도구 자체를 만든 **Alberto Brandolini**. 워크숍을 *cooperative game*으로 정의해준 그의 어휘 없이는 이 책은 한 줄도 시작될 수 없었다. *All our aggregates are wrong*의 **Mauro Servienti**, *Effective Aggregate Design*의 **Vaughn Vernon**, *Working Effectively with Legacy Code*의 **Michael Feathers**, *Your Code as a Crime Scene*의 **Adam Tornhill**, *Get Your Hands Dirty on Clean Architecture*의 **Tom Hombergs** — 각자 한 챕터의 척추를 빌려왔다. Spring Modulith를 만든 **Oliver Drotbohm**의 작업이 없었다면 책의 후반부 절반은 다른 모양이 됐을 것이다.

한국에서 EventStorming을 진심으로 시도하고 그 회고를 *솔직하게 공개한* 회사들에 특별히 감사한다. **컬리** helloworld의 *"Database Driven Development에서 진짜 DDD로의 선회"*, **우아한형제들**의 사내 학습·우아콘 발표, **카카오** 추천팀의 DDD 도입기, **카카오스타일(지그재그)**의 PDP 회고, **오토피디아(닥터차)**의 *실패에 가까운 워크숍* 회고, **Goodfriends**의 도입기. 한국 독자가 *남의 이야기가 아니라 우리 이야기*를 발견할 수 있는 자리들이다.

## 마지막 한 줄

이 책의 마지막 장(12장)은 한 줄로 끝난다 — *"이번 주 안에 30분만 어떨까요. 종이 한 장이면 됩니다."* 그 한 줄을 위해 책 전체가 깔린다. 책장을 닫고 노트북을 닫고 일어선 다음, 옆자리 동료에게 한 마디 던지는 그 작은 동작 — 거기까지가 이 책의 영토다.

그럼 함께 첫 sticky를 꺼내보자.
