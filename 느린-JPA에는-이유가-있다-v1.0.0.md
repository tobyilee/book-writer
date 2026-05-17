# 느린 JPA에는 이유가 있다

> JPA는 매핑 비용 때문에 느린 게 아니다. 라운드트립과 트랜잭션 동작 때문에 느리다 — 이 책은 그 이유를 12개 챕터로 풀어낸다.

- **저자:** Toby-AI
- **부제:** Vlad의 눈으로 보는 고성능 영속성
- **버전:** v1.0.0
- **발행일:** 2026-05-17
- **언어:** ko
- **분량:** 12개 챕터 / 본문 약 28만 자 (단행본 320~380p 상당)
- **라이선스:** CC BY-NC-SA 4.0

## 이 책은 무엇인가

JPA와 Hibernate를 쓰는 한국 백엔드 개발자라면 한 번쯤 같은 의문 앞에 선다. *왜 우리 서비스의 list API는 트래픽이 조금만 늘어도 응답시간이 무너지는가. 왜 분명 LAZY를 걸었는데도 쿼리가 백 번씩 나가는가. 왜 `batch_size`를 넣었는데도 INSERT은 여전히 하나씩 나가는가.* 이 책은 그 의문들을 우회하지 않는다. Vlad Mihalcea의 시각 — **라운드트립과 트랜잭션 동작**이라는 두 개의 축 — 위에서 JPA가 느려지는 모든 자리를 차례로 들여다본다.

책은 절차서가 아니다. "이렇게 하세요"의 권고문이 아니라, 함께 코드 앞에 앉아 *왜 이 한 줄이 SQL을 이렇게 만들어내는가*를 풀어내는 해설서다. JDBC 토대(2장), 엔티티 설계(3장), N+1과 fetch 전략(4~5장), 트랜잭션과 캐시(6~7장), 동시성·배치·페이지네이션(8~10장), 진단(11장), 그리고 다음 세계(12장)까지 — 한 트랜잭션이 시작해서 끝나기까지 무슨 일이 일어나는가의 흐름을 따라 한 권으로 이어진다.

다른 자료와의 차이는 두 가지다. 첫째, **충격 도입**으로 책을 연다. Vlad의 64-트랜잭션 실험(HikariCP 10개 → 149ms, 64개 → 272ms, 4개 → 128ms)을 첫 페이지에 박아 *"커넥션은 많을수록 빠르다"*는 통념을 깬다. 그 충격 위에서 ORM 성능의 본질을 다시 정의한다. 둘째, **매 챕터 끝 "내 코드 체크리스트 3개"**로 책을 닫는다. 추상적 권고가 아니라 오늘 자기 IDE에서 30초 안에 확인할 수 있는 항목들이다. 12개 챕터의 36개 항목이 11장에서 한 표로 회수되어, 책을 덮은 독자가 곧장 자기 프로젝트의 `application.yml`을 다시 열게 만든다.

Hibernate 6의 새 기능(SQM, `TupleTransformer`, JPQL window function, `@SoftDelete`, `@JdbcTypeCode`)과 Hibernate 6.6의 Jakarta Data, 그리고 ORM Battle 2025 벤치까지 — 2026년 시점의 최신 지형도 담고 있다.

## 누구를 위한 책인가

이 책은 **JPA/Hibernate 실무 경험이 있는 미드~시니어 백엔드 개발자**를 위한 책이다. 입문서가 아니다. 어노테이션 기본, Spring Boot 구조, JDBC의 `PreparedStatement` 정도는 안다고 가정한다.

- **진입 상태:** "JPA는 쓰지만 왜 느린지는 모른다. 슬로우 쿼리 로그에는 안 잡히는데 응답시간은 무너지는 경험을 해봤다. 누가 *N+1*이나 *OSIV*를 말하면 고개는 끄덕이지만, 우리 코드 어디에 그게 있는지는 명확히 짚지 못한다."
- **출구 상태:** "라운드트립과 트랜잭션 동작을 머릿속에서 그릴 수 있다. 자기 코드의 비용을 수치로 추정한다. 안티패턴을 발견하면 정정할 수 있다. 책을 덮은 다음 날 자기 프로젝트의 `application.yml`을 열어 `open-in-view`, `batch_size`, `default_batch_fetch_size`를 확인하고 싶어진다."

대용량 트래픽 서비스의 성능 튜닝을 맡은 미드 시니어, JPA 도입 결정을 다시 짚어야 하는 테크 리드, 다른 사람의 ORM 코드를 리뷰해야 하는 시니어 — 이 셋 모두에게 같은 좌표계를 제공한다.

## 무엇을 얻게 되는가

- **두 개의 사고 도구.** ① PersistenceContext = 1차 캐시 + dirty checking 스냅샷 + write-behind 큐. ② Database response time ≠ Application throughput. 이 둘만으로도 자기 코드의 성능 문제를 어디서 봐야 하는지의 좌표가 잡힌다.
- **JDBC 토대와 statement caching.** PostgreSQL `prepareThreshold`, MySQL `prepStmtCache`, Oracle `defaultRowPrefetch`까지 DB별 튜닝 포인트. FlexyPool로 실측을 통해 풀 사이즈를 찾는 절차.
- **N+1을 발견하는 눈.** `JOIN FETCH` → `@EntityGraph` → `@BatchSize` → `FetchMode.SUBSELECT`의 권장 순서. 컬렉션 fetch + 페이지네이션(HHH000104)의 2-query 패턴.
- **Projection 결정 트리.** JPQL constructor / Tuple / `@SqlResultSetMapping` / `TupleTransformer` / Spring Data Interface / Java Records / `@Subselect` 각각의 쓸 자리. "수정 안 할 read는 모두 DTO" 원칙의 구현 카탈로그.
- **트랜잭션 경계 설계.** `readOnly=true`의 두 가지 효과, OSIV 안티패턴 5가지, `enable_lazy_load_no_trans`가 OSIV보다 더 큰 함정인 이유.
- **캐시의 정당화 기준.** 2차 캐시를 켜는 세 가지 조건, 쿼리 캐시가 단독으로 위험한 이유, query plan cache와 `in_clause_parameter_padding`의 자리.
- **동시성 안티패턴 표.** Dirty read / Non-repeatable read / Phantom / Lost update / Skew × Read Committed / RR / SI / Serializable의 매트릭스. MySQL InnoDB gap lock의 추적법.
- **대량 write의 정석.** `batch_size` 4종 세트, PostgreSQL 30만 건 벤치 3.2x 개선, `reWriteBatchedInserts`의 추가 2~3x, StatelessSession 부활(H6.3+).
- **Keyset pagination.** OFFSET이 무너지는 자리, `WHERE (created_at, id) < (?, ?)` 패턴, Spring Data 3.x `ScrollPosition`, Hibernate 6 JPQL window function 한 방.
- **진단 도구 한 세트.** datasource-proxy, `SQLStatementCountValidator`로 CI에 N+1 회귀 테스트 박기, Hibernate Statistics, Hypersistence Optimizer 정적 분석.
- **다음 세계의 지도.** Hibernate 6/7 신기능, Jakarta Data, JPA + jOOQ 분업, Reactive에 대한 입장 — 책을 덮은 뒤 다음에 펼칠 자료의 좌표.
- **36개 체크리스트.** 12개 챕터 × 3개 항목. 11장에서 한 표로 회수. 책을 덮고 자기 코드로 돌아가는 자리.

## 차례

1. **왜 JPA는 느릴까 — 라운드트립이라는 진짜 비용** — Vlad의 64-트랜잭션 실험으로 *"커넥션은 많을수록 빠르다"*는 통념을 깨고, ORM 성능의 본질이 매핑이 아니라 라운드트립과 트랜잭션 동작임을 선언한다.
2. **커넥션은 적을수록 빠르다 — JDBC, 풀, 그리고 statement caching** — HikariCP·FlexyPool·`provider_disables_autocommit`과 PostgreSQL/MySQL/Oracle 각각의 statement cache 옵션까지 — 트랜잭션이 *언제* 커넥션을 잡는가를 풀어낸다.
3. **엔티티를 잘 빚는다는 것 — 식별자, equals, 그리고 bytecode enhancement** — `@Id` 전략이 SQL을 어떻게 바꾸는가. 컬렉션 매핑의 함정과 bytecode enhancement 세 옵션(LazyInitialization / DirtyTracking / AssociationManagement)의 트레이드오프.
4. **쿼리 한 줄이 백 번 나가는 이유 — N+1을 다시 본다** — N+1을 *발견하는 눈*. fetch join → EntityGraph → BatchSize → SUBSELECT의 권장 순서, 컬렉션 fetch + 페이지네이션의 2-query 패턴.
5. **가져오는 형태도 다시 본다 — Projection과 query 선택** — *"수정 안 할 read는 모두 DTO"*의 구현 카탈로그. 7가지 projection 옵션 비교 표와 JPQL/HQL/Criteria/Native/jOOQ의 결정 트리.
6. **트랜잭션 경계를 설계한다 — `@Transactional`과 OSIV** — `readOnly=true`의 두 가지 효과, OSIV 안티패턴 5가지, `enable_lazy_load_no_trans`가 *더 큰* 함정인 이유.
7. **캐시는 정말 답인가 — 1차·2차·쿼리 캐시의 자리** — 2차 캐시를 켜는 세 가지 조건, 쿼리 캐시가 단독으로 N+1을 재발시키는 메커니즘, query plan cache와 `in_clause_parameter_padding`.
8. **같은 row를 둘이 동시에 본다 — 락과 isolation의 실전** — 동시성 anomaly × isolation 매트릭스. `@Version` 낙관락이 디폴트인 이유, MySQL InnoDB next-key lock의 추적법, 결제·재고 도메인의 비관락 정당화.
9. **한꺼번에 처리한다 — 배치와 대량 write** — `batch_size` 4종 세트, PostgreSQL 30만 건 벤치(51,785→16,052ms), `reWriteBatchedInserts`, StatelessSession 부활, 벌크 UPDATE/DELETE의 cascade 함정.
10. **깊은 페이지도 첫 페이지처럼 — 페이지네이션** — OFFSET이 무너지는 자리, keyset pagination 정석, Spring Data 3.x `ScrollPosition`, Hibernate 6 JPQL window function의 한 방.
11. **보이지 않는 비용을 본다 — 관찰과 진단** — datasource-proxy의 그룹화, `SQLStatementCountValidator`로 CI에 N+1 회귀 테스트, Hibernate Statistics, Hypersistence Optimizer. 책 전체 안티패턴 카탈로그와 36개 체크리스트 회수.
12. **그리고 그 다음 — 운영 기능과 다음 세계** — Audit/Soft Delete/Multi-tenancy/Stored Procedure의 운영 기능과 Hibernate 6/7, Jakarta Data, JPA+jOOQ 분업, Reactive에 대한 입장.

각 챕터는 **핵심 질문**으로 열리고, **내 코드 체크리스트 3개**로 닫힌다. 책의 머리말·맺음말·참고문헌과 콜로폰이 본문 앞뒤를 묶는다.

## 저자 소개

Toby-AI는 책-writer 하네스가 활용하는 AI 저자 페르소나다. *Toby 평어체* — 청유형과 수사적 질문을 적극 활용하고, 지시문 대신 상황을 함께 들여다보는 톤 — 으로 기술서를 쓰도록 설계되었다. 이 책 또한 `book-writing-orchestrator` 하네스가 리서치 → 저술 계획 → 계획 리뷰 → 챕터 저술 → 스타일 점검 → 통합 편집 → EPUB 빌드를 거쳐 산출한 결과이며, 모든 인용·도표·코드 예제의 출처는 본문의 「참고문헌」에 명시되어 있다.

이 책의 시각은 한 사람에게 깊이 빚지고 있다. **Vlad Mihalcea** — *High-Performance Java Persistence*의 저자, Hypersistence 창립자, FlexyPool/Hypersistence Optimizer/Hypersistence Utils의 메인테이너 — 의 "라운드트립과 트랜잭션 동작"이라는 두 축이 12개 챕터의 골격을 이루고 있다.

## 책 정보

- **파일:** `느린-JPA에는-이유가-있다-v1.0.0.epub`
- **형식:** EPUB 3 (ko)
- **표준 검증:** epubcheck 통과
- **하네스 버전:** v1.2.0
- **식별자:** `urn:uuid:cea6a8a6-b9be-4fe1-b354-08bc11d179c3`
- **라이선스:** [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) — 저작자 표시 · 비상업적 이용 · 동일조건 변경허락
