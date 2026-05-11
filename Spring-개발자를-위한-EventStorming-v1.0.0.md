# Spring 개발자를 위한 EventStorming
## 오렌지색 sticky가 Java 코드가 되기까지

**저자:** Toby-AI · **버전:** v1.0.0 · **발행일:** 2026-05-11 · **언어:** 한국어 · **라이선스:** CC BY-NC-SA 4.0

## Logline

EventStorming 워크숍의 sticky가 어떻게 Spring·React 코드로 환생하는지를 한국 개발자 관점에서 풀어낸 책.

## 이 책은 무엇인가

EventStorming은 Alberto Brandolini가 2013년 발표한 도메인 발견 워크숍 기법이다. 회의실 벽에 색깔별 sticky note를 붙여 도메인 전문가와 개발자가 같은 그림을 보게 만든다 — 오렌지색은 Domain Event, 파란색은 Command, 노란색은 Actor, 보라색은 Policy, 초록색은 Read Model, 빨간색은 Hotspot. 단순한 규약이지만, 이 색상 grammar가 만들어내는 합의의 밀도는 어떤 다이어그램 도구도 따라가지 못한다.

문제는 그 다음이다. 워크숍이 끝나고 sticky를 사진으로 찍은 뒤, 개발자는 자기 자리로 돌아온다. 그리고 묻는다. "오렌지색 sticky가 내 Spring 프로젝트 어디에 들어가지?" "Pivotal Event를 그었는데, 이걸 패키지로 어떻게 자르지?" "Read Model은 React 어디서 만들어야 하지?" 이 책은 바로 그 질문에 답한다. 워크숍의 sticky 하나하나가 Java record, `@TransactionalEventListener`, Spring Modulith의 `@ApplicationModule`, Next.js Server Component, React Query 캐시로 환생하는 구체적인 매핑을 12장에 걸쳐 따라간다.

다른 EventStorming 자료가 워크숍 진행법에 머무르거나, 다른 DDD 책이 코드 패턴에 머무를 때, 이 책은 두 세계를 잇는다. Brandolini의 *Introducing EventStorming*과 Vaughn Vernon의 DDD 시리즈를 1차 자료로 삼되, 컬리·우아한형제들·카카오·오토피디아의 EventStorming 회고를 한국 출발선으로 인용한다. 모든 코드는 Spring Boot 3.x + Java 21 + NextJS 14 + Spring Modulith 1.3 환경에서 동작하는 실전 스니펫이다.

## 누구를 위한 책인가

- **Java + Spring(Boot) 백엔드를 메인으로 쓰는 중급~시니어 개발자.** 1~2년차 Spring 경험에 DDD 책 1~2권을 읽었거나 적어도 Aggregate·Bounded Context 용어가 익숙한 사람.
- **ReactJS/NextJS로 프론트엔드도 다루는 풀스택 또는 백엔드 중심 개발자.** Read Model을 React Server Component와 React Query 캐시로 어떻게 내려보내는지 궁금한 사람.
- **DDD에 진심이지만 팀 정렬에서 막혀온 사람.** 혼자 Aggregate를 그릴 줄은 알지만, 도메인 전문가·기획자·QA와 같은 모델을 공유하는 방법을 찾고 있는 사람.
- **EventStorming의 색상 규약은 들어봤지만 실무 워크숍을 주도해본 적 없는 사람.** Brandolini의 영문 자료나 컬리·우아한형제들의 회고를 읽고 "우리 팀에도 해보고 싶다"고 느꼈던 사람.
- **Spring Modulith·Outbox·Kafka로 모듈러 모놀리스 또는 이벤트 기반 아키텍처를 도입 중인 팀의 테크 리드.** 도메인 경계를 어디서 그어야 할지의 근거를 찾는 사람.

## 무엇을 얻게 되는가

- EventStorming 6가지 색상 grammar를 한국어로 정확히 다루고, sticky 하나를 Java/TypeScript 코드로 환생시키는 매핑 규칙
- Big Picture·Process Modeling·Software Design 세 레벨을 상황에 맞게 선택해 워크숍을 설계하는 능력
- Pivotal Event 기법으로 Bounded Context 경계를 그어 Spring Modulith `@ApplicationModule`로 옮기는 절차
- `@DomainEvents`·`@TransactionalEventListener`·Outbox·Kafka를 조합한 도메인 이벤트 발행 패턴(코드 템플릿 포함)
- Read Model을 NextJS Server Component·React Query·projection 테이블로 내려보내는 풀스택 구현법
- 원격 환경에서 Miro/Mural로 워크숍을 진행하는 facilitator 가이드와 흔히 빠지는 7가지 안티패턴
- Hotspot으로 표시된 의문점을 백로그·ADR·Sprout Method PR로 옮기는 짧은 다리

## 차례

**Part 1. 워크숍의 방 — 도구의 정신과 색상 grammar**

1. **왜 지금 EventStorming인가** — 한국 팀에 이 기법이 왜 지금 필요한가
2. **색상 grammar — 처음 만난 sticky note를 이해하기** — 6색 sticky를 도메인 문법으로 읽는 법
3. **Big Picture — 도메인 전체를 한 벽에 펼치기** — 가장 거친 첫 워크숍 설계
4. **Process Modeling — 흐름과 트리거를 드러내기** — Command·Policy·Read Model을 잇는 두 번째 레벨

**Part 2. 코드의 방 — sticky가 Spring/React 코드로 환생**

5. **Pivotal Event는 Bounded Context의 칼이다 — Spring Modulith로 잘라보기** — 도메인 경계를 모듈 경계로
6. **Aggregate를 발견해 코드로 내려보내기 — JPA와 Hexagonal Architecture** — sticky 묶음을 Aggregate root로
7. **Domain Event를 Spring에 꽂기 — `@DomainEvents`·Outbox·Kafka** — 이벤트 발행의 세 단계 패턴
8. **Read Model과 프론트엔드 — 화면은 어디서 만들어지나** — RSC·React Query·projection

**Part 3. 팀의 방 — 워크숍을 일과 한국 팀 현실로**

9. **Hotspot에서 백로그까지 — 워크숍을 일로 옮기는 짧은 다리** — 빨간 sticky를 ADR과 티켓으로
10. **원격 EventStorming — Miro 보드에서 시작하기** — 분산 팀을 위한 워크숍 설계
11. **Facilitator의 함정 — 개발자가 빠지는 7가지 안티패턴** — 흔히 무너지는 지점들
12. **한국 팀의 EventStorming — 우리 자리에서 시작하기** — 컬리·우아한형제들·카카오·오토피디아 회고로 다시 출발선

**부록**

- **A. Spring Modulith·Outbox 코드 템플릿** — 복붙해서 쓸 수 있는 모듈/이벤트/Outbox 스니펫
- **B. Miro/Mural EventStorming 보드 세팅** — 보드 템플릿·스티커 팔레트·세션 진행 체크리스트
- **C. 용어집 — Brandolini ↔ Spring ↔ React 매핑** — 색상·개념·코드 한 페이지 매핑
- **D. Sprout Method 시나리오 — 워크숍 hotspot이 PR로 가는 구체 예** — 빨간 sticky 한 장이 PR로 완결되는 흐름

## 저자

**Toby-AI** — Book Writer Project의 자동화 저술 하네스(v1.2.0)로 산출된 가상의 저자. 이 책은 Brandolini의 *Introducing EventStorming*(2013–2021)을 1차 자료로 하고, 한국 개발 커뮤니티의 실무 회고(컬리·우아한형제들·카카오 등)와 Spring/React 생태계의 최신 도구(Spring Boot 3.x · Spring Modulith 1.3 · NextJS 14 · React Query 5)를 결합해 재해석한 결과물이다. AI가 저술했지만 모든 코드 예제와 인용은 출처를 명시했고, 한국 Spring 개발자 페르소나에 맞춰 평어체로 정돈했다.

## 책 정보

- **파일:** `Spring-개발자를-위한-EventStorming-v1.0.0.epub`
- **형식:** EPUB 3 (한국어, RTL 없음, 코드 블록 monospace 보존)
- **분량:** 본문 약 166,000자 · 12개 챕터 + 부록 4편 + 서문 + 콜로폰
- **난이도:** 중급 (Spring Boot 1~2년 경험 + DDD 기본 용어 숙지 전제)
- **코드 환경:** Spring Boot 3.x · Java 21 · NextJS 14 · React 18 · Spring Modulith 1.3 · Kafka
- **라이선스:** CC BY-NC-SA 4.0 — 저작자 표시·비상업적 이용·동일조건 변경허락. 학술/기술 문서에서 자유롭게 인용 가능, 상업적 사용은 별도 문의.
- **식별자:** `urn:slug:eventstorming-for-ddd-developers:v1.0.0`
- **하네스:** Book Writer Project v1.2.0 — 자동화 저술 하네스로 산출
