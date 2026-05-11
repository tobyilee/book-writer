# 저술 계획: EventStorming for DDD Developers

## 책 제목 후보 (3개)

### 후보 A — 정직·직설형
**제목:** Spring 개발자를 위한 EventStorming
**부제:** 오렌지색 sticky가 Java 코드가 되기까지

이 제목은 검색 결과 페이지에서 클릭당하기 위한 제목이다. "EventStorming"과 "Spring 개발자"라는 두 단어가 정확히 청중의 검색어와 일치한다. 약속은 단순하다 — 워크숍의 sticky가 자기 IDE에 보일 Java 코드와 어떻게 연결되는지를 책임지고 보여준다. 부제는 책의 척추(Brandolini의 색상 grammar → Spring 토큰 매핑)를 한 줄로 압축한다. *DDD를 책 1~2권 읽었지만 워크숍은 못 돌려본 백엔드 개발자*가 서점에서 표지만 보고도 "내 책이네" 하고 집어든다. 톤은 가이드북에 가깝다 — 모험서가 아니라 동반자.

### 후보 B — 약속·여정형
**제목:** 도메인을 다시 발견하는 시간
**부제:** EventStorming으로 Spring 모놀리스를 다시 짠다

청중이 "EventStorming"이라는 단어로 검색하지 않더라도, "DDD가 잘 안 풀린다", "모놀리스를 어떻게 자를지 모르겠다"고 느끼는 사람을 끌어들이는 제목이다. "다시 발견"은 청중의 자기 진단(이미 도메인을 다 안다고 믿었지만, 사실은 코드 구조에 갇혀 있었음)을 건드린다. 부제로 도구(EventStorming)와 결과물(Spring 모놀리스 재구성)을 못 박는다. *DDD 책을 4~5권 읽었지만 실무에서 좌절감이 쌓인 시니어*가 끌릴 만한 톤. 다만 검색 노출이 약하므로 마케팅 부담은 커진다.

### 후보 C — 도발·각성형
**제목:** 코드 이전에, 모델이 있다
**부제:** Brandolini를 한국 Spring 팀의 벽에 옮겨붙이는 법

가장 도발적이다. "코드 이전에 모델"은 한국 SI/스타트업에서 익숙한 "Database Driven Development" 관성에 대한 정면 공격이고, 컬리 회고가 짚은 그 지점을 표지에서부터 건드린다. 부제로 Brandolini라는 인물을 명시해 권위를 빌리되, "한국 Spring 팀의 벽"이라는 표현으로 청중에게 "이 책은 영어책 번역이 아니다, 너희 회의실 벽 이야기다"를 약속한다. *DDD에 진심이고 자기 팀에 변화를 일으키고 싶은 시니어/테크리드*가 가장 깊이 반응할 톤. 매니페스토에 가깝다.

**추천:** **후보 A (Spring 개발자를 위한 EventStorming)** — 표지에서 가장 확실히 청중을 잡는다. 책 안의 톤은 후보 C의 각성·도발 정신을 유지하되, 외피는 검색·노출이 강한 후보 A로 가는 편이 낫다. 후보 B의 "다시 발견" 어휘는 서문 헤드라인이나 챕터 1 제목으로 흡수하자.

---

## 책 특성

- **장르:** 기술서 — 방법론 해설(전반부) + 실전 가이드(후반부) 혼합. 단순 번역서가 아닌 "코드로 끌어내리는 다리".
- **분량:** 본문 약 12만 자(한글 공백 포함 기준) / 약 280~320페이지. 부록 포함 시 350페이지 내외. 챕터당 평균 9,000~11,000자.
- **난이도:** 중급. Spring Boot 1~2년 + JPA/REST 경험 + DDD 책 1~2권(*Implementing DDD* 또는 조영호의 *우아한 객체지향* 발표 수준) 통과한 독자를 기준선으로 잡는다. 워크숍 진행 경험은 *없어도 된다* — 그게 출발 가설이다.
- **독자 여정:** *"DDD 책은 읽었는데 내 Spring 프로젝트 폴더 구조랑 연결이 안 된다"* → *"월요일에 우리 팀 회의실 벽에 sticky를 붙여 첫 Big Picture를 돌리고, 그 결과를 다음 스프린트의 Spring Modulith 모듈 분리로 옮길 수 있다"*.
- **톤:** 토비 문체 — 평어체 기반에 청유형 적극 활용. "워크숍을 한번 상상해보자", "이쯤에서 코드를 한번 살펴보자", "그렇다면 이 sticky는 Spring에서 무엇이 될까?" 같은 호흡. 강의가 아니라 옆자리에서 함께 화이트보드 앞에 선 동료의 목소리.

---

## 내러티브 아크

이 책은 독자를 세 개의 방을 차례로 통과시킨다 — **워크숍의 방**, **코드의 방**, **팀의 방**. 첫 번째 방(1~4장)에서 독자는 EventStorming이라는 도구의 정신·색상 grammar·세 가지 레벨을 익힌다. 여기까지는 Brandolini의 영토다. 다만 모든 설명이 "내 Spring 프로젝트의 OrderService에서는 이게 어떻게 보일까?"라는 질문으로 착륙한다. 두 번째 방(5~8장)에서 책은 결정적으로 갈라진다 — 워크숍에서 발견한 큰 경계(Pivotal Event → Bounded Context → Spring Modulith 모듈)를 먼저 코드로 옮기고(5장), 그 안의 작은 단위(Aggregate → JPA + Hexagonal Architecture)로 줌인하고(6장), 다음으로 sticky의 색깔들이 `@DomainEvents`·Outbox·Kafka·React Query·RSC로 환생한다(7~8장). "큰 경계 → 작은 단위 → 메시징 → 화면" 순서가 reference §3.1의 시퀀스(Big Picture → Software Design)와 일치하고, 독자의 인지 순서(굵게 자른 다음 안을 채운다)와도 맞는다. 이 구간이 책의 진짜 차별화 지점이고, 가장 많은 코드 스니펫이 들어간다. 세 번째 방(9~12장)에서는 도구·코드를 다 익힌 독자가 *팀과 조직*이라는 가장 어려운 현실로 돌아온다 — 워크숍 hotspot을 PR backlog로 옮기는 짧은 다리(9장), 원격에서 돌리는 법(10장), facilitator의 함정(11장), 그리고 한국 팀의 출발선(컬리·우아한형제들·카카오 회고)을 보며 자기 자리를 찾는다(12장).

이 흐름이 청중에게 자연스러운 이유는, 그들이 이미 *코드를 짤 줄 안다*는 자신감을 갖고 책을 펴기 때문이다. 그래서 책은 "코드 → 방법론"이 아니라 "방법론 → 코드 → 팀"으로 가야 한다. 코드는 약속이고, 팀은 도전이다. 그 사이에 방법론이 끼어든다.

---

## 챕터 목록

### 1장. 왜 지금 EventStorming인가
- **핵심 질문:** DDD에 진심인 우리가 왜 sticky note를 꺼내야 할까?
- **주요 내용:**
  - 한국 Spring 팀의 익숙한 출발선 — "DDD 책은 읽었는데 폴더 구조는 그대로다"
  - 컬리 helloworld 회고("Database Driven Development에서 진짜 DDD로의 선회")와 오토피디아 실패담을 인용해 독자 자기진단
  - EventStorming의 세 정신(Postpone precision / Unlimited modeling resources / Maximize engagement) 소개
  - 이 책이 약속하는 것 — 색상 grammar가 Spring 코드 토큰으로 환생하는 다리
  - 이 책이 약속하지 않는 것 — Brandolini 원서 대체, 모든 DDD 입문, 마이크로서비스 결정론
- **reference 활용:** §1.1, §9.5, §9.6, §12
- **원서 참조:** Preface, ch.1
- **예상 분량:** 약 8,000자 (도입부, 가볍게)

### 2장. 색상 grammar — 처음 만난 sticky note를 이해하기
- **핵심 질문:** 오렌지·블루·라일락·핑크·노랑·초록·핫핑크가 각각 왜 그 색이어야 하는가?
- **주요 내용:**
  - 9개 색상 표(Domain Event부터 Opportunity까지)와 각각의 정확한 정의
  - alpha-and-omega 문장 — "Pink System between Blue Command and Orange Event, Lilac Policy between Orange Event and Blue Command"의 해부
  - "Visible Legend"의 의미 — 벽에 legend를 붙여둔다는 사소해 보이는 디테일이 왜 결정적인지
  - 색상 grammar를 Java 타입 시스템에 비유 — `Event`/`Command`/`Policy`/`Aggregate`를 별도 클래스로 잡는 것과 같은 이유
  - 색상 강박 안티패턴은 *짧은 예시 한 줄*로만 언급(본격 처방은 11장)
  - 첫 번째 코드 스니펫: Event/Command/Policy를 표현하는 Java record 한 세트
- **reference 활용:** §1.3, §2.1, §8.3
- **원서 참조:** ch.8 "Visible Legend", ch.14 building blocks
- **예상 분량:** 약 10,000자

### 3장. Big Picture — 도메인 전체를 한 벽에 펼치기
- **핵심 질문:** 첫 워크숍에서 무엇을 기대하고, 무엇을 기대하지 말아야 하는가?
- **주요 내용:**
  - 6단계 절차(Kick-off → Chaotic Exploration → Enforcing the Timeline → People and Systems → Explicit Walk-through → Pick your problem)를 *상황 가정* 형식으로 풀어쓰기
  - "지금 우리 회사 주문 도메인을 회의실 벽에 펼친다고 상상해보자" 시나리오로 6단계 시뮬레이션
  - Pivotal Event 찾기 휴리스틱 — "follow the money", "여러 부서가 동시에 반응하는 이벤트"
  - "seats are poisonous", "depleted marker", "PO fallacy" 등 Brandolini 안티패턴 미리보기
  - artifact의 휘발성 — 종이 롤을 며칠 더 붙여둔다는 것의 의미
- **reference 활용:** §1.2, §2.2, §3.1, §4.1, §4.2, §8.1
- **원서 참조:** ch.3, ch.4, ch.7
- **예상 분량:** 약 11,000자

### 4장. Process Modeling — 흐름과 트리거를 드러내기
- **핵심 질문:** Big Picture에서 발견한 hotspot 영역을 어떻게 게임처럼 풀어낼까?
- **주요 내용:**
  - Process Modeling을 "cooperative game"으로 다시 정의 — 승리 조건은 hotspot 0
  - Event ↔ Command ↔ Policy ↔ Read Model 순환의 색상 grammar 본격 작동
  - 세 가지 시작 전략(Start from the beginning / from the end / Make a little mess)
  - Brandolini가 추천하는 "end에서 거꾸로" 전략을 한국 이커머스 시나리오로 시뮬레이션
  - Read Model이 단순한 "조회 데이터"가 아니라 "결정의 근거"라는 관점 전환
  - 코드 스니펫: Policy를 표현하는 `@TransactionalEventListener` 미리보기 (7장에서 본격 다룸)
- **reference 활용:** §1.2, §2.3, §4.2, §5.1
- **원서 참조:** ch.13, ch.14, ch.15
- **예상 분량:** 약 10,000자

### 5장. Pivotal Event는 Bounded Context의 칼이다
- **핵심 질문:** 워크숍에서 그린 pivotal event 사이의 구간을, 어떻게 Spring Modulith 모듈로 옮기는가?
- **주요 내용:**
  - "Big Picture는 발견, Software Design은 결정" — 격(格)의 차이를 5장 첫머리에 명시
  - Pivotal Event ↔ Bounded Context 경계 매핑(ContextMapper, ArchiLab 근거)
  - "follow the money" 휴리스틱과 "business phases" 휴리스틱
  - Bounded Context ↔ Spring Modulith의 `module` ↔ 패키지 단위 모듈 분리
  - ArchUnit 기반 모듈 간 직접 의존 차단
  - "modular monolith first" 논쟁 — Frankel과 Servienti의 양쪽 입장 병기(*다른 시각* 박스 컨벤션 첫 등장)
  - 코드 스니펫: `@ApplicationModule` 어노테이션이 붙은 모듈 두 개와 ArchUnit 테스트 한 개
- **reference 활용:** §3.2, §4.1, §5.1, §10.4
- **원서 참조:** ch.6 "Discovering Bounded Contexts"
- **예상 분량:** 약 11,000자

### 6장. Aggregate를 발견해 코드로 내려보내기 — JPA와 Hexagonal Architecture
- **핵심 질문:** 잘라낸 모듈 안에서 sticky 위의 Aggregate 후보가 어떻게 Spring Data JPA 클래스가 되고, 어떻게 port/adapter로 분리되는가?
- **주요 내용:**
  - **Reading guide 한 줄:** "이미 Vernon의 *Implementing DDD*를 읽은 시니어 독자는 6.3절을 건너뛰어도 좋다"
  - "Postpone aggregate naming" — 너무 일찍 이름 붙이지 않기
  - Aggregate를 *상태 머신*으로 보기 [B §4835], Domain Event = state transition의 가시화
  - Vernon의 Effective Aggregate Design 4규칙 (transaction boundary, small, ID 참조, eventual consistency)을 sticky 위에서 어떻게 검증하는지
  - Mauro Servienti의 "All our aggregates are wrong" 관점 — 데이터 관계가 아니라 behavior로 자르기
  - **6.x Hexagonal Architecture로 패키지 구조 잡기 (~2,000자)** — Tom Hombergs *Get Your Hands Dirty on Clean Architecture*의 매핑을 그대로 도입. Blue Command → Inbound port, Pink External System → Outbound adapter, Orange Domain Event → 도메인 코어가 발행하는 사건. Domain은 plain POJO, port/adapter로 자르는 컨벤션
  - 코드 스니펫: Spring Data JPA + `@Version` + `@DomainEvents` 메서드를 가진 Aggregate Root 한 개 + inbound port 인터페이스 + outbound adapter 한 묶음
- **reference 활용:** §1.2, §2.4, §3.2, §5.4, §5.5
- **원서 참조:** ch.17~22, ch.20 (Aggregate as state machine)
- **예상 분량:** 약 12,000자

### 7장. Domain Event를 Spring에 꽂기 — `@DomainEvents`·Outbox·Kafka
- **핵심 질문:** sticky 위의 오렌지색 사실을, 우리 서비스가 정말로 안전하게 발행하고 소비하게 만들려면 무엇이 필요한가?
- **주요 내용:**
  - Spring Modulith의 `ApplicationEventPublisher` + `@ApplicationModuleListener` 기본기
  - Event Publication Registry — 실패해도 DB에 보존되는 in-process outbox
  - Dual-write 문제와 Transactional Outbox 패턴의 정수
  - Polling vs CDC(Debezium) 두 가지 relay 전략
  - Spring Cloud Stream으로 Kafka로 externalize — `Supplier<Flux<OrderPlaced>>` 패턴
  - 소비자의 idempotency — at-least-once 환경에서의 필수 방어
  - 코드 스니펫: `OrderPlaced` 이벤트가 발행→outbox→Kafka→warehouse 모듈까지 흐르는 한 묶음
- **reference 활용:** §5.1, §5.2, §5.3
- **원서 참조:** ch.14 (Policy 색상의 코드화)
- **예상 분량:** 약 13,000자 (가장 무거운 챕터)

### 8장. Read Model과 프론트엔드 — 화면은 어디서 만들어지나
- **핵심 질문:** sticky의 초록색(Read Model)이 React/Next.js의 어디로 환생하는가?
- **주요 내용:**
  - Read Model이 CQRS read side projection이라는 개념적 다리
  - React Query / TanStack Query의 캐시 키 = Read Model의 식별자
  - Domain Event를 invalidation 트리거로 보기 — `OrderPlaced` 이벤트가 어떻게 `queryClient.invalidateQueries(['orders'])`로 흐르는가
  - Next.js App Router + RSC — 서버 컴포넌트가 CQRS read side를 그대로 받아오는 시나리오
  - **BFF/GraphQL은 *짧은 사이드바*로 축소** — Rodrigo Estrada의 인지부하 반대 시각만 한 단락으로 인용하고, 본격 비교는 부록 C 옆 짧은 절로 이동. 본문은 RSC + React Query + projection 매핑에 집중
  - 코드 스니펫: Spring 쪽 read projection 한 개 + Next.js Server Component + React Query hydration 한 화면
- **reference 활용:** §6.1, §6.2, §6.3
- **원서 참조:** ch.14 Read Model 정의
- **예상 분량:** 약 11,000자 (BFF/GraphQL 축소로 1,000자 절감)

### 9장. Hotspot에서 백로그까지 — 워크숍을 일로 옮기는 짧은 다리
- **핵심 질문:** 핫핑크 sticky가 어떻게 다음 스프린트의 우선순위가 되는가?
- **주요 내용:** *transitional 챕터 — 다리 역할에 집중*
  - 8장과의 다리 한 단락 — "코드를 만들었으니 이제 워크숍의 핫핑크를 PR로 옮길 차례다"
  - Hotspot의 본질 — "safer target for finger-pointing", 사람 대신 모델 위 sticky를 가리키기
  - 워크숍 hotspot ↔ 코드 hotspot 교차 — Adam Tornhill의 Git churn 기반 hotspot 탐지 (개념 매핑 그림 한 장)
  - "도메인 전문가 갈등 영역" ∩ "Git churn 높은 폴더" = 리팩토링 1순위
  - arrow voting으로 우선순위 정하기
  - Sprout Method 코드 시나리오는 부록 D로 분리 — "구체 적용은 부록 D를 보라"는 안내
  - 후속 판본에서 한국 사례 인터뷰가 확보되면 9장을 확장한다는 노트
- **reference 활용:** §4.2, §4.3
- **원서 참조:** ch.7 Hotspot, ch.4 §1881 arrow voting
- **예상 분량:** 약 6,000자 (transitional로 축소)

### 10장. 원격 EventStorming — Miro 보드에서 시작하기
- **핵심 질문:** 회의실 벽이 없는 분산 팀에서, Big Picture를 어떻게 살려내는가?
- **주요 내용:**
  - Brandolini의 입장 변화 — COVID 이후 "원격은 안 된다"에서 "원격도 된다"로
  - 원격 5대 패턴(Split / Anticipate Structure / Colors as signature / Modelling Log / Iterate on Copy)
  - 10~15분 silent ideation + facilitated merging의 cycle
  - facilitator 2명 운영(흐름 / hotspot 관리)
  - Miro 공식 템플릿 두 개와 보드 세팅의 실전 디테일
  - 비동기 EventStorming의 한계 — 동기적 silent ideation은 결국 필요하다
- **reference 활용:** §7.1, §7.2, §7.3
- **원서 참조:** ch.11 "Big Picture in remote mode"
- **예상 분량:** 약 9,000자

### 11장. Facilitator의 함정 — 개발자가 빠지는 7가지 안티패턴
- **핵심 질문:** 워크숍을 직접 돌리는 개발자가 가장 많이 실수하는 지점은 어디인가?
- **주요 내용:** *슬림화 — 7가지 안티패턴에 집중*
  - 7가지 안티패턴 큐레이션 — (1) 너무 일찍 정확함 추구, (2) Seats are poisonous, (3) marker 부족, (4) 코드 얘기로 점프, (5) PO fallacy, (6) 색상 강박, (7) "정답 모델" 추구
  - 각 안티패턴마다 *상황 가정 → 증상 → 처방* 3단 구조로
  - Kenny Baas-Schwegler의 *Collaborative Software Design* 정신 — "every voice shapes the software", Deep Democracy (짧은 절)
  - Eric Evans의 Model Exploration Whirlpool 한 단락 — EventStorming만으로 모든 걸 해결하려 하지 말 것
  - **EventStorming vs Event Modeling(Dymitruk) 비교는 12장으로 이동**, 11장에서는 다루지 않음
- **reference 활용:** §8.1, §8.2, §8.3
- **원서 참조:** ch.4, ch.7, ch.8, ch.18
- **예상 분량:** 약 8,000자 (슬림화로 3,000자 절감)

### 12장. 한국 팀의 EventStorming — 우리 자리에서 시작하기
- **핵심 질문:** 월요일 아침, 우리 팀 회의실에서 첫 워크숍을 어떻게 시작할 것인가?
- **주요 내용:**
  - 한국 사례 종합 — 우아한형제들 우아콘, 카카오 추천팀, 컬리 helloworld, 오토피디아 회고
  - 한국 팀이 발견한 공통 패턴 — 단계별 인원 조정, 좁은 타겟 도메인, 지속적 업데이트, Database Driven Development 관성과의 싸움
  - "팀 내 DDD를 모르는 동료를 어떻게 끌어오나" — 입문자용 sticky note 한 시간 게임
  - **이웃 도구와의 자리 잡기 (11장에서 이관)** — EventStorming vs Event Modeling(Dymitruk) 짧은 비교, Example Mapping / Domain Storytelling을 언제 함께 쓰는가
  - 첫 워크숍 체크리스트(준비물 / 초대장 / 시간 배분 / 사후 액션)
  - 책을 덮은 뒤의 한 걸음 — 다음 스프린트에 추가할 한 가지 실험
  - 미래 — LLM이 EventStorming을 어떻게 보완할 것인가(arXiv 2603.26244)에 대한 짧은 코다
- **reference 활용:** §9.1~§9.6, §10.1, §10.2, §10.3, §10.5
- **원서 참조:** ch.9 Workshop Aftermath, ch.18
- **예상 분량:** 약 10,000자 (Event Modeling 비교 흡수로 +1,000자)

---

## 챕터 외 구성요소

### 서문 — 왜 이 책인가
약 2,500자. 청중 자기진단("DDD 책은 읽었는데…")부터 시작해 책의 약속·약속하지 않는 것·읽는 법을 짧게. 컬리 회고와 오토피디아 실패담을 한두 줄 인용해 톤을 잡는다.

### 부록 A. Spring Modulith·Outbox 코드 템플릿
약 6,000자. 7장에서 나누어 보여준 코드 조각을 한 군데 모은 실전 zip — `@ApplicationModule` 패키지 구조, `Event Publication Registry` 설정, Outbox 테이블 DDL, Spring Cloud Stream Kafka 설정, idempotent consumer 한 묶음.

### 부록 B. Miro/Mural EventStorming 보드 세팅
약 3,500자. 10장에서 언급한 Miro 공식 템플릿 두 개의 실제 보드 세팅 — swimlane 골격, legend 위치, 권한 설정, 보드 archive 정책.

### 부록 C. 용어집 — Brandolini 용어 ↔ Spring 용어 매핑
약 3,000자. Domain Event → `@DomainEvents` 메서드 결과, Pivotal Event → Bounded Context 경계, Policy → `@TransactionalEventListener`, Aggregate → `@AggregateRoot`, Read Model → CQRS read projection / React Query 캐시, Hotspot → `git churn` 폴더 등 한 표로.

### 부록 D. Sprout Method 적용 시나리오 — 워크숍 hotspot을 PR로
약 5,000자. 9장이 transitional로 축소되면서 분리한 구체 코드 시나리오. Michael Feathers의 Seam/Sprout Method로 legacy Spring 모놀리스의 Aggregate 한 조각을 안전하게 떼어내는 PR 시나리오. 워크숍 핫핑크 sticky 한 장이 (a) Git churn 데이터와 교차되어 우선순위로 올라오고, (b) Sprout Method로 새 클래스에 분리되며, (c) 이벤트 발행으로 기존 호출자를 단계적으로 갈아끼우는 3단계 — 코드 스니펫 포함. 후속 판본에서 한국 사례 인터뷰가 확보되면 9장 본문으로 승격하는 것을 명시.

### 콜로폰
editor가 작성. 계획에는 자리만 마련.

---

## 보고

- **파일 절대 경로:** `/Users/tobylee/workspace/ai/book-writer/.claude/worktrees/eventstorming/eventstorming-for-ddd-developers/02_plan.md`
- **챕터 수:** 12개 (+ 서문, 부록 A/B/C/D, 콜로폰)
- **가장 자신 있는 부분:** 챕터 5~8의 "코드의 방" 구간. reference §5(Spring 생태계)와 §6(프론트엔드)이 가장 풍부했고, Pivotal Event → Spring Modulith module → Aggregate → JPA + Hexagonal → Domain Event/Outbox → Read Model/RSC로 이어지는 매핑이 책의 차별화 척추다. 챕터 저자가 가장 명확한 코드 스니펫을 약속할 수 있는 구간이기도 하다. v1.1에서 5·6장 순서를 reference §3.1의 시퀀스(큰 경계 → 작은 단위)와 일치시켰고, 6장에 Hexagonal Architecture 절을 추가해 §5.5의 누락을 메웠다.
- **가장 불안한 부분:** 챕터 9 "Hotspot에서 백로그까지". v1.1에서 transitional 챕터(~6,000자)로 축소하고 Sprout Method 코드 시나리오는 부록 D로 분리했다. 후속 판본에서 한국 Spring 팀의 hotspot 리팩토링 사례가 community-research로 보강되면 9장을 다시 확장하는 것을 노트해두었다.

---

## 개정 이력

### v1.1 (Phase 3 review 반영) - 2026-05-11
- 챕터 5·6 순서 교체 (Aggregate → BC/Modulith 순서를 BC/Modulith → Aggregate로). reference §3.1의 Big Picture → Software Design 시퀀스 및 독자 인지 순서(큰 경계 → 작은 단위)와 일치시킴.
- 챕터 9를 transitional(~6,000자)로 축소, 부록 D "Sprout Method 적용 시나리오" 분리. reference §4.3의 근거 빈약 우려를 책의 신뢰 손상 없이 흡수.
- 챕터 11 슬림화(~8,000자), Event Modeling(Dymitruk) vs EventStorming 비교를 챕터 12 "이웃 도구와의 자리 잡기" 절로 이동.
- 6장(새 Aggregate 챕터)에 Hexagonal Architecture 절(~2,000자) 추가. reference §5.5의 Tom Hombergs 매핑(Blue→Inbound port, Pink→Outbound adapter)을 본문에 박음.
- 8장의 BFF/GraphQL 비중 축소 — Rodrigo Estrada의 반대 시각만 짧은 사이드바로 남기고, 본문은 RSC·React Query·projection 매핑에 집중. 분량 12,000자 → 11,000자.
- 내러티브 아크 단락 두 문장 갱신 — 새 5·6장 순서를 반영해 "큰 경계 → 작은 단위 → 메시징 → 화면" 흐름으로 다듬음.
- 2장 색상 강박을 짧은 예시 한 줄로 축소(본격 처방은 11장으로 일원화) — reviewer가 지적한 2장↔11장 중복 해소.
- 5장(새 BC 챕터)의 Frankel vs Servienti 병기에 *다른 시각* 박스 컨벤션을 첫 도입으로 명시.
