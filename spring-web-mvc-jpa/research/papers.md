<!-- 검색 시점: 2026-05-25 기준 -->

# 논문 리서치: 백엔드 웹 개발 입문의 이론적 토대 (REST · IoC/DI · ORM)

대상 독자가 비학문 개발자이므로 수학적 증명은 생략하고 **seminal(고전) 1차 자료 + 직관·결과** 위주로 정리한다. 이 분야는 빠르게 변하는 프레임워크와 달리, 토대가 되는 개념은 2000년대 초의 고전 문헌에 뿌리를 둔다.

---

## 논문/1차 문헌 1: REST의 정의 — Fielding 박사학위 논문 (seminal)
- 저자·연도: Roy T. Fielding, 2000
- 발표처: University of California, Irvine 박사학위 논문 (지도교수 Richard N. Taylor)
- 제목: "Architectural Styles and the Design of Network-based Software Architectures"
- 원문: https://roy.gbiv.com/pubs/dissertation/top.htm (Chapter 5 = REST: https://roy.gbiv.com/pubs/dissertation/rest_arch_style.htm)
- Semantic Scholar: https://www.semanticscholar.org/paper/49fc9782483bc311c2bd1b902dfb32bcd99ff2d3
- 핵심 주장(인용 가능):
  - REST는 분산 하이퍼미디어 시스템을 위한 **아키텍처 스타일**. 여러 네트워크 기반 스타일에서 파생된 하이브리드 스타일에 **균일한 커넥터 인터페이스(uniform connector interface)** 제약을 추가한 것.
  - 핵심 제약(constraints): client-server, stateless, cacheable, uniform interface, layered system, (선택) code-on-demand.
- 책 활용: 본문에서 "REST 원칙"을 다룰 때 **권위 있는 1차 정의**로 인용. 실무의 "REST API"가 Fielding의 엄밀한 정의(특히 HATEOAS/hypermedia)와 다르다는 점이 논쟁점(아래 참고 글).
- 보충: "Roy Fielding's Misappropriated REST Dissertation"(twobithistory.org, 2020) — 업계가 REST를 어떻게 느슨하게 차용했는지. 본문 논쟁점 소재.
- 신선도: 2000년 고전 — 안정적, 버전 무관.

## 1차 문헌 2: Inversion of Control / Dependency Injection — Fowler (seminal)
- 저자·연도: Martin Fowler, 2004
- 제목: "Inversion of Control Containers and the Dependency Injection pattern"
- 원문: https://martinfowler.com/articles/injection.html
- 핵심 주장:
  - "IoC"라는 용어가 너무 일반적이어서 혼란을 준다 → Fowler가 **Dependency Injection(DI)**이라는 더 구체적 명칭을 제안·정착.
  - DI 형태: constructor injection / setter injection / interface injection. (Spring 권장은 **생성자 주입** — 불변성·테스트 용이성.)
  - 핵심 직관: 객체가 자신의 협력자(collaborator)를 직접 찾지/만들지 않고 외부(컨테이너)가 주입 → 결합도↓, 테스트 시 mock 주입 쉬움.
- 책 활용: Spring DI/IoC 챕터의 개념적 뿌리. NestJS `@Injectable`/Angular DI와 같은 계보임을 프런트 개발자에게 연결.
- 신선도: 2004년 — 안정적. (주의: 이는 블로그형 1차 문헌이지 peer-reviewed 논문은 아님 — "권위 있는 산업 문헌"으로 표기.)

## 1차 문헌 3: 도메인 주도 설계의 엔티티/값 객체/리포지토리 (개념 출처)
- 저자·연도: Eric Evans, 2003
- 제목: "Domain-Driven Design: Tackling Complexity in the Heart of Software" (Addison-Wesley)
- 핵심:
  - **Repository 패턴**의 개념적 출처 중 하나 — 도메인 객체 컬렉션처럼 보이는 추상화로 영속성 세부를 감춤. Spring Data JPA의 `Repository`가 이 패턴의 구현.
  - Entity(식별자로 구분) vs Value Object 구분 — JPA `@Entity`/`@Embeddable` 매핑의 개념적 배경.
- 책 활용: "Repository가 왜 인터페이스만 선언해도 동작하나"의 패턴적 배경 (Spring Data가 프록시로 구현 제공).
- 신선도: 2003년 고전 — 안정적.

## 1차 문헌 4: Object-Relational Mapping의 본질적 난점 — "Vietnam of Computer Science"
- 저자·연도: Ted Neward, 2006
- 제목: "The Vietnam of Computer Science"
- 핵심 주장:
  - ORM은 객체 모델과 관계형 모델의 **임피던스 불일치(impedance mismatch)**를 다루며, 그 추상화는 누수(leaky)되기 쉽다 — 편의를 주지만 결국 SQL을 이해해야 하는 순간이 온다.
  - 책 활용: JPA를 "마법"으로만 쓰지 말고 **생성되는 SQL을 봐야 한다**는 논거 (N+1, 영속성 컨텍스트, fetch 전략의 실무 함정과 직결). 대상 독자가 SQL 기본은 알지만 ORM은 처음이므로 핵심 멘탈 모델.
- 신선도: 2006년 — 개념 안정적.

## 학술 검색 메모 (DBLP/ACM/IEEE/Semantic Scholar)
- "Spring MVC", "JPA", "Spring Boot"는 산업 프레임워크라 **peer-reviewed 학술 논문이 희소**하다. 이 주제의 권위 있는 토대는 위와 같은 **고전 문헌·산업 표준 문서**에 있다.
- 인접 학술 주제(참고용, 직접 인용 우선순위 낮음):
  - 웹 인증/세션 보안: OWASP 가이드라인(표준), JWT 관련 RFC 7519(IETF 표준 — 학술 논문이 아닌 스펙).
  - ORM 성능: 데이터베이스 학회(VLDB/SIGMOD)에 ORM 안티패턴/쿼리 최적화 연구가 산발적으로 존재하나, 입문서 수준엔 과함.
- 인용 정확성 메모: 위 4건 중 1·2·4는 공개 원문 URL 확보. 3(Evans)은 서적이라 DOI 대신 ISBN/출판사 표기 권장.

---

## 커버리지 한계 (papers 레인)
- 이 책 주제는 본질적으로 **실무 프레임워크 입문**이라 학술 논문 밀도가 낮음. 이론 토대는 4건의 seminal 문헌으로 충분히 커버되며, 나머지 근거는 web(1차 릴리스 노트)·community(현장)로 보완하는 것이 적절.
- RFC 7519(JWT), RFC 6265(쿠키), RFC 7231/9110(HTTP semantics)은 보안·HTTP 챕터의 1차 표준 근거로 web 레인 또는 별도 표준 인용에 추가 권장 (이번 패스에서 본문 인용은 미수집).
