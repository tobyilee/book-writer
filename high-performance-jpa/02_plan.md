# 고성능 JPA/Hibernate 저술 계획

## v2 개정 사항 (2026-05-17)

plan-reviewer의 피드백을 반영해 10장 → **12장 구조**로 확장했다. 핵심 변경은 다섯 가지다.

1. **Projection을 독립 5장으로 신설.** 기존 9장에 흡수돼 있던 §2.10/§2.11 + 권고 #10이 자기 자리를 갖는다. *N+1 직후*에 배치 — "fetch를 줄였으면 가져오는 형태도 다시 봐야 한다"는 흐름.
2. **5장 ↔ 6장 순서 뒤집기.** 1차 캐시는 트랜잭션 스코프이므로, **트랜잭션·OSIV(6장) → 캐시(7장)** 순으로 재배치. 백트래킹 제거.
3. **Bytecode enhancement 절을 3장에 추가.** 레퍼런스 §2.5에 있던 항목이 누락돼 있었다. 식별자·equals와 같은 자리(엔티티 설계)에서 다뤄야 마땅.
4. **9장(모니터링·안티패턴) 정체성 좁히기.** 11장 *보이지 않는 비용을 본다*는 **관찰·진단 도구에 집중**한다. 안티패턴 카탈로그는 마지막 회수 절로 짧게, Projection은 빠져나갔다.
5. **배치/페이지네이션 분리.** 8장 → **9장 배치(대량 write)** + **10장 페이지네이션(깊은 read)**. 정반대 워크로드를 한 챕터에 묶으면 독자가 어느 쪽도 깊이 못 갖는다.

부차 변경: Statement caching을 2장의 정식 절로 승격, 1장 도입부에 Vlad의 64-tx 수치(149/272/128) 충격 추가, 6장에 `enable_lazy_load_no_trans` 안티패턴 명시 절, 8장에 MySQL InnoDB gap lock 절, 12장에 JPAB·ORM Battle 인용 자리 명시, 각 챕터 끝 "내 코드 체크리스트 3개" 형식 약속. Should #7(10장 분리)은 12장 안의 *두 절 구조*로 흡수 — 챕터 수를 13으로 늘리면 운영 기능과 미래가 각각 얇아지는 부작용이 있어 한 챕터 안에서 균형을 잡는다.

기존 계획은 `02_plan_v1.md`로 백업했다.

---

## 제목 후보

1. **느린 JPA에는 이유가 있다 — Vlad의 눈으로 보는 고성능 영속성**
   - 슬러그: `slow-jpa-has-reasons`
   - logline: "쿼리 한 줄이 백 번 나가는 그 순간을 거꾸로 풀어내는 책. JDBC 토대부터 Hibernate 6까지, '왜 느린가'를 한 번에 정리한다."
   - 톤: 진단·해부. 독자가 자기 코드를 의심하기 시작하게 만드는 톤.
   - 포지셔닝: 'CRUD는 짠다, 그러나 왜 느린지는 모른다'는 미드 레벨 개발자가 첫 챕터부터 끄덕이며 자기 코드를 떠올리도록 설계.

2. **JPA를 다시 본다 — JDBC, 트랜잭션, 그리고 라운드트립**
   - 슬러그: `jpa-revisited`
   - logline: "ORM을 한 겹 벗기면 무엇이 보이는가. PersistenceContext와 JDBC 사이에서 일어나는 일들을 처음부터 다시 본다."
   - 톤: 학습·재발견. 이미 JPA를 쓰지만 '진짜 무엇이 도는지'를 처음부터 다시 정리하고 싶은 독자에게.
   - 포지셔닝: Vlad의 *High-Performance Java Persistence* 1·2부의 한국어 정수에 가깝다. 입문서가 아니라 '재학습서'.

3. **JPA 고성능의 정석 — 라운드트립, 트랜잭션, 그리고 동시성**
   - 슬러그: `jpa-high-performance-orthodox`
   - logline: "JPA·Hibernate 실무자를 위한 한 권의 정석. Vlad Mihalcea의 시각으로 정리한 라운드트립·트랜잭션·동시성 설계."
   - 톤: 표준·정석. 사수가 후배에게 건네주는 두꺼운 매뉴얼.
   - 포지셔닝: '레퍼런스로 곁에 두는 책'으로 자리잡는 노선. 다른 두 후보보다 무게감·완결성을 강조.

**추천:** **1번 — 느린 JPA에는 이유가 있다**.

이유는 세 가지다. 첫째, 토비 문체의 핵심인 '독자 공감과 수사적 질문'을 표지에서부터 시동한다. 둘째, '왜 느린가'는 본 책의 일관된 내러티브 축(라운드트립과 트랜잭션을 모르면 ORM은 안 풀린다)과 한 줄로 맞물린다. 셋째, 미드 레벨 한국 개발자의 검색 동선("JPA 느림", "N+1", "성능 튜닝")과 자연스럽게 만난다. 부제로 *Vlad의 눈으로 보는 고성능 영속성*을 달아 권위 있는 출처를 명시한다.

---

## 책 특성

- **장르:** 에세이형 기술서. 절차서 톤이 아니라, 함께 코드를 들여다보며 "왜 이게 느린가"를 풀어가는 해설서. 코드·표·벤치 수치는 풍부하되, 본문은 평어체 산문으로 이어진다.
- **분량:** 본문 약 320~380p 상당 (예상 한글 글자 수 **22~25만 자**). 챕터당 평균 17,000~22,000자, 코드/표는 별도. 챕터 12개를 가정한 산출.
- **난이도:** 중상. 입문자가 아니라 '동작은 시킬 줄 알지만 왜 느린지 모르는' 미드~시니어를 타깃. JPA 어노테이션 기본, 단위 테스트, Spring Boot 구조, JDBC의 PreparedStatement 정도는 안다고 가정한다.
- **독자 여정:** *"JPA는 쓰지만 왜 느린지 모르는 사람"* → *"라운드트립과 트랜잭션 동작을 머릿속에서 그릴 수 있고, 자기 코드의 비용을 수치로 추정하며, 안티패턴을 발견하면 정정할 수 있는 사람"*. 책을 덮을 때쯤 독자는 자기 프로젝트의 `application.yml`을 다시 열어 `open-in-view`, `batch_size`, `default_batch_fetch_size`를 확인하고 싶어진다.

### 책의 약속 — 챕터 끝 체크리스트

매 챕터 끝에 **"내 코드 체크리스트 3개"**를 둔다. 추상적 권고가 아니라 *오늘 자기 IDE에서 30초 안에 확인할 수 있는 항목*으로. 11장에서 12개 챕터의 체크리스트(총 36개 항목)를 한 표로 회수한다. 이 구조는 책 전체를 *읽고 끝*이 아니라 *읽고 자기 코드로 돌아가게* 만드는 장치다.

---

## 내러티브 아크

이 책은 **"한 트랜잭션이 시작해서 끝나기까지 무슨 일이 일어나는가"**를 큰 골격으로 삼는다. 챕터 순서는 그 흐름을 따른다.

먼저 **1~2장에서 토대**를 깐다. 1장은 "왜 JPA가 느린가"라는 질문에서 시작하되, 곧장 Vlad의 64-트랜잭션 실험 수치(149/272/128ms)와 USL 그래프를 박아 *"커넥션 많이 잡으면 빨라진다"*는 통념을 깬다. 그 충격 위에서 ORM 성능의 본질(라운드트립과 트랜잭션 동작)을 선언한다. 2장은 그 토대인 JDBC와 커넥션 풀로 내려간다 — FlexyPool 사례, `provider_disables_autocommit`, 그리고 본 개정에서 정식 절로 승격된 **Statement caching**(PostgreSQL `prepareThreshold` / MySQL prepStmtCache / Oracle defaultRowPrefetch / `StatementInspector`까지). 여기까지 읽은 독자는 "내 코드 위의 비용이 사실 JDBC 한 줄에서 결정된다"는 감각을 얻는다.

**3~5장은 엔티티·페치·프로젝션**이다. 토대 위에 데이터가 올라간다. 3장은 식별자·equals/hashCode·관계 매핑·**bytecode enhancement**(본 개정에서 추가) — 즉 '엔티티가 정확히 어떤 SQL을 만들어내게 되는가'의 설계. 4장은 그 엔티티들이 query 시점에 어떻게 뽑혀 나오는가 — N+1, fetch join, EntityGraph, batch fetch. 한국 커뮤니티의 게시판 페이지네이션 사례를 길게 풀어내는 자리. 그리고 **5장 Projection은 본 개정의 신설 챕터**다. "fetch를 줄였다면 그 형태도 다시 봐야 한다" — JPQL constructor / Tuple / `@SqlResultSetMapping` / `TupleTransformer`(H6) / Spring Data Interface / Java Records / `@Subselect` / Native vs HQL vs JPQL vs Criteria의 선택 기준까지. 권고 #10 *"수정 안 할 read는 모두 DTO"*가 이 챕터의 슬로건.

**6~7장은 트랜잭션과 캐시**다. 본 개정에서 순서를 뒤집었다 — 1차 캐시는 트랜잭션 스코프인데 트랜잭션 정의 없이 캐시를 다루면 백트래킹이 생기기 때문. 6장은 Spring `@Transactional`과 read-only 최적화, 그리고 책에서 가장 강하게 비판할 OSIV. `enable_lazy_load_no_trans`가 더 큰 함정이라는 점도 명시 절로. 7장은 1차/2차/쿼리 캐시 — *왜 켜는가, 언제 위험한가, 2차 캐시의 정당화 조건*. 여기서 책의 중간 매듭이 묶인다 — *"JPA는 entity fetch만 해서는 안 된다, 트랜잭션 경계와 캐시 정책도 설계해야 한다."*

**8~10장은 동시성·배치·페이지네이션**이다. 정반대 끝의 워크로드를 차례로 본다. 8장은 락과 isolation — 낙관·비관·MVCC, anomaly 표, MySQL InnoDB **gap lock**(본 개정에서 명시 절). 9장은 대량 write — `batch_size` 4종 세트, PostgreSQL 30만 건 벤치(51,785→16,052ms), `reWriteBatchedInserts`, StatelessSession 부활, 벌크 UPDATE/DELETE. 10장은 깊은 read — OFFSET의 한계, keyset pagination, Spring Data 3.x `ScrollPosition`, H6의 JPQL window function 한 방. 8~10장의 분리로 각 워크로드를 충분히 풀어낼 공간이 생긴다.

**11장은 관찰**이다. 본 개정에서 정체성을 좁혔다 — 책 전체의 진단 도구만 정리한다. datasource-proxy의 SQL 그룹화, `SQLStatementCountValidator`로 단위 테스트에서 N+1 잡기, Hibernate Statistics, FlexyPool metrics, Hypersistence Optimizer 정적 분석. 마지막 절에서 책 전체의 안티패턴 카탈로그(2.17)와 36개 체크리스트 회수.

**12장은 운영 기능과 다음 세계**다. 본 개정에서 *운영 기능*(Audit Envers·Soft Delete·Multi-tenancy·Stored Procedure)과 *다음 세계*(Hibernate 6/7 신기능·Jakarta Data·jOOQ 조합·Reactive 입장)를 한 챕터 안의 두 절로 통합. 운영 기능은 "오늘 당장 쓸 수 있는 도구", 다음 세계는 "여기서 한 발 더 가면 무엇이 있는가". JPAB.org 표준 벤치와 ORM Battle 2025 인용은 jOOQ 조합 단원에 자리. 마지막에 1장의 북극성(*"라운드트립과 트랜잭션 동작"*)을 다시 가리키고 책을 닫는다.

이 아크의 핵심은 여전히 **"넓게 펼친 뒤 모아 닫는다"**다. 토대(1~2장) → 엔티티·페치·프로젝션(3~5장) → 트랜잭션·캐시(6~7장) → 동시성·배치·페이지네이션(8~10장) → 진단(11장) → 다음(12장). 독자는 매 챕터에서 자기 코드를 떠올릴 수밖에 없고, 챕터를 닫을 때마다 한 가지씩 의심스러운 곳이 생긴다. 11장에서 그 의심들이 한 장의 체크리스트로 모이고, 12장에서 다음 걸음을 가리키며 책이 닫힌다.

---

## 챕터 목록

### 1장. 왜 JPA는 느릴까 — 라운드트립이라는 진짜 비용

- **핵심 질문:** 커넥션을 더 늘리면 빨라질 것 같은데, 왜 오히려 느려질까? 그리고 ORM이 느린 이유는 매핑 비용일까, 다른 무언가일까?
- **주요 내용:**
  - **충격 도입 (본 개정):** Vlad의 64 트랜잭션 실험을 첫 페이지에 박는다 — HikariCP 기본 10개 → 149ms, 64개로 키우면 → 272ms, FlexyPool이 찾아낸 4개 → 128ms. 그래프 한 장과 함께. *"커넥션은 많을수록 빠르다"는 직관이 깨지는 자리.*
  - Universal Scalability Law(Neil Gunther) 직관 — 동시성이 자원 경합으로 바뀌는 임계점.
  - "JPA가 느리다"는 통념의 해부 — 매핑 비용은 사실 1%, 99%는 *라운드트립과 트랜잭션 동작*.
  - Vlad의 북극성 *"Fetching too much data is the number one problem"* 인용.
  - JPA / Hibernate / JDBC 계층 구조 한 장 그림.
  - 두 가지 사고 도구 도입: ① PersistenceContext = 1차 캐시 + dirty checking 스냅샷 + write-behind 큐, ② Database response time ≠ Application throughput.
  - 책의 약속 — 매 챕터 끝 "내 코드 체크리스트 3개", 11장에서 36개 한 번에 회수.
- **다룰 reference 섹션:** §1.1, §1.2, §1.3, §2.1 64-tx 수치(충격 도입), §5 14 tips 도입부.
- **내 코드 체크리스트 3개 예시:**
  - 우리 서비스의 현재 HikariCP `maximumPoolSize`가 몇인지 안다.
  - 가장 자주 호출되는 read API의 평균 응답시간 중 *DB 응답시간 비중*을 안다.
  - `application.yml`의 `spring.jpa.open-in-view` 값을 안다.
- **독자가 얻는 것:** "내가 만든 ORM 성능 문제는 어디서 봐야 하는가"의 좌표계. 책 전체를 읽을 동기와 자기 코드를 의심할 출발선.
- **예상 분량:** 약 16,000자.

---

### 2장. 커넥션은 적을수록 빠르다 — JDBC, 풀, 그리고 statement caching

- **핵심 질문:** 트랜잭션은 정확히 *언제* 커넥션을 잡을까? 그리고 같은 PreparedStatement를 천 번 던지면 정말 한 번만 컴파일될까?
- **주요 내용:**
  - HikariCP 기본값과 풀 사이즈 통념 깨기 (1장의 64-tx 수치를 풀-사이징 관점에서 다시 깊게).
  - FlexyPool로 *실측을 통한 발견* — `IncrementPoolOnTimeoutConnectionAcquisitionStrategy`, 메트릭(acquire time, retry count, concurrent connections).
  - `hibernate.connection.provider_disables_autocommit=true` — 트랜잭션은 *첫 SQL이 나갈 때* 커넥션을 잡아야 한다.
  - **Statement caching 정식 절 (본 개정에서 승격):**
    - **PostgreSQL pgjdbc** — `prepareThreshold=1` (기본 5)로 서버사이드 prepare 즉시 전환, `preparedStatementCacheQueries`, `preparedStatementCacheSizeMiB`. wire protocol의 V2/V3 차이.
    - **MySQL connector-j** — `cachePrepStmts=true`, `prepStmtCacheSize=250`, `prepStmtCacheSqlLimit=2048`, `useServerPrepStmts=true`. 클라이언트 캐시와 서버사이드 prepare의 분리.
    - **Oracle ojdbc** — `defaultRowPrefetch`, statement cache 관리.
  - `StatementInspector`로 모든 SQL 가로채기 — 멀티테넌시·강제 hint·감사 활용 예고(12장과 연결).
- **다룰 reference 섹션:** §2.1, §2.6 전체, §3.1 풀 실험, §2.18 (DB별 튜닝 포인트).
- **내 코드 체크리스트 3개 예시:**
  - 우리 PG/MySQL JDBC URL에 statement cache 옵션이 명시돼 있는지.
  - `provider_disables_autocommit=true`가 켜져 있는지.
  - FlexyPool이든 HikariCP 자체 메트릭이든, *connection acquire time*을 지표로 보고 있는지.
- **독자가 얻는 것:** *"커넥션을 더 많이 잡는 게 답이 아니다"*라는 반직관. 풀 사이징과 client-side 캐싱을 자기 환경에서 검증할 수치 감각.
- **예상 분량:** 약 20,000자.

---

### 3장. 엔티티를 잘 빚는다는 것 — 식별자, equals, 그리고 bytecode enhancement

- **핵심 질문:** 똑같이 동작하는 엔티티 두 개가 있는데, 왜 한쪽은 배치가 묶이고 다른 쪽은 한 줄씩 INSERT가 나갈까? 그리고 LAZY를 켰는데 왜 컬렉션 fetch가 줄지 않을까?
- **주요 내용:**
  - 식별자 전략 비교 표 — IDENTITY는 배치를 죽인다, SEQUENCE(pooled-lo)가 정석, TABLE은 `SELECT … FOR UPDATE`로 비싸다, AUTO는 DB별 지뢰.
  - MySQL에는 SEQUENCE가 없다는 현실 — 수동 ID + Stateless session 우회.
  - `@Inheritance` 전략 비교 — SINGLE_TABLE 디폴트, JOINED는 무결성용, TABLE_PER_CLASS는 UNION ALL 폭발, `@MappedSuperclass`의 의의.
  - equals/hashCode의 두 가지 정석 — 비즈니스 키 / DB 생성 PK + `getClass().hashCode()`. *Set 슬립* 사례를 길게 풀이.
  - 컬렉션 매핑의 함정 — 단방향 `@OneToMany`의 join table, `@ManyToMany List`의 delete-all-and-reinsert, 양방향 `Set` 사용 시 equals 폭발.
  - `@Immutable` + dirty checking 비용 차단 — 7장 캐시와 연결되는 다리.
  - **Bytecode enhancement 정식 절 (본 개정에서 추가):** `hibernate-enhance-maven-plugin` / Gradle plugin. 세 가지 옵션 — `enableLazyInitialization`(LAZY ToOne을 진짜 LAZY로), `enableDirtyTracking`(스냅샷 비교 → 인터셉터 기반), `enableAssociationManagement`(양방향 자동 동기화). 기본 LAZY의 한계(`@ManyToOne`에서 안 먹는 이유)와 bytecode enhancement가 그 한계를 어떻게 푸는지. 도입 비용(빌드 단계 추가)과 운영 이득(dirty checking 비용 절감)의 트레이드오프.
  - 권고 #6(컬럼 타입 적정성) 회수 자리 — `@Column(length=...)`, `@Lob`의 함정, JSON 컬럼 매핑은 5장 Projection·12장 H6 신기능에서 다시.
- **다룰 reference 섹션:** §2.2 전체, §2.5 bytecode enhancement, §5 권고 6·7·8, §2.17 안티패턴 표의 매핑 관련 항목.
- **내 코드 체크리스트 3개 예시:**
  - 우리 핵심 엔티티 5개의 `@Id` 전략이 무엇인지, 그게 의도된 선택인지.
  - equals/hashCode가 PK 기반으로 짜여 있다면, transient 시점에 안전한 형태인지.
  - bytecode enhancement를 켰다면 어떤 옵션을, 왜 켰는지 설명 가능한지.
- **독자가 얻는 것:** 엔티티 한 줄(어노테이션 한 개)이 SQL을 *어떻게* 바꾸는지를 머릿속에서 그릴 수 있다. 자기 프로젝트의 `@Id`와 `@OneToMany`를 다시 보는 즉시 점검 능력.
- **예상 분량:** 약 22,000자.

---

### 4장. 쿼리 한 줄이 백 번 나가는 이유 — N+1을 다시 본다

- **핵심 질문:** N+1은 누구나 안다고 한다. 그런데 왜 우리 코드에는 여전히 N+1이 있을까?
- **주요 내용:**
  - N+1의 정의를 다시 — 슬로우 쿼리 로그에 안 잡힌다는 점, 각 쿼리는 충분히 빠르다는 점.
  - 발생 트리거 두 가지 — `@ManyToOne`/`@OneToOne`의 기본값 EAGER, LAZY 컬렉션의 view·stream iterate.
  - 해결책 권장 순서: ① `JOIN FETCH`(JPQL/Criteria) ② `@EntityGraph` (fetchgraph vs loadgraph) ③ `@BatchSize` + `default_batch_fetch_size` ④ `FetchMode.SUBSELECT`.
  - **HHH000104 — 컬렉션 fetch + 페이지네이션** — *2-query 패턴* 코드 길게 풀이. 한국 커뮤니티 게시판 사례(velog gwanghyeonkim, sdsd0908) 인용.
  - "ToOne만 fetch join, ToMany는 batch_size 100~1000"라는 한국 실무 합의 정리.
  - EAGER이 코드 스멜인 이유 — *전역 fetch plan에 묶이는 비용*. "LAZY globally, JOIN FETCH per query" 슬로건.
  - N+1 자동 회귀 테스트 예고 — 자세한 도구는 11장에서, 여기서는 "어떻게 *발견*하느냐"의 윤곽만.
- **다룰 reference 섹션:** §2.3 전체, §3.3 OSIV 게시판 사례 일부, §5 권고 13, §2.17 안티패턴의 fetch 관련.
- **내 코드 체크리스트 3개 예시:**
  - 우리 코드에 `@ManyToOne`/`@OneToOne`에 명시적 `fetch = LAZY`가 붙어 있는지.
  - 컬렉션 fetch가 있는 쿼리에 페이지네이션이 함께 걸린 곳이 있는지.
  - 가장 큰 list API의 SQL 카운트를 단위 테스트에서 검증하고 있는지.
- **독자가 얻는 것:** N+1을 *발견하는 눈*. 컬렉션 페이지네이션을 만나도 패닉하지 않는다. (Projection은 다음 챕터에서.)
- **예상 분량:** 약 20,000자.

---

### 5장. 가져오는 형태도 다시 본다 — Projection과 query 선택 *[본 개정에서 신설]*

- **핵심 질문:** N+1을 막았다고 끝일까? 4개 컬럼만 필요한데 엔티티 전체를 가져오는 건 무엇을 낭비하는가?
- **주요 내용:**
  - 권고 #10 *"수정 안 할 read는 모두 DTO"* 선언으로 시작.
  - Projection 옵션 비교 표 — **JPQL constructor expression**(`new com.foo.Dto(...)`), **Tuple**(컬럼 인덱스/별칭 접근), **`@SqlResultSetMapping`**(native 결과를 DTO로), **`TupleTransformer`**(Hibernate 6의 신규), **Spring Data Interface Projection**(closed/open), **Java Records + JPQL**(가장 깔끔), **`@Subselect`**(read-only 가상 엔티티).
  - 각 옵션의 *쓸 자리*와 *피할 자리* — Open Interface Projection의 SELECT * 함정, `@Subselect`로 분석 쿼리를 도메인으로 들고 오기.
  - **One-to-Many DTO projection** — `ResultTransformer.distinct()`, Hibernate 6의 `TupleTransformer.LIST` + 메모리 그룹화. 부모-자식 한 번에.
  - **Query 선택 기준 (§2.11):** JPQL / HQL / Criteria / Native / jOOQ / Blaze-Persistence 결정 트리. *동적 쿼리는 Criteria, 정적 read는 JPQL, 복잡한 분석은 jOOQ나 Native*.
  - Hibernate 6의 SQM(Semantic Query Model)이 가능하게 한 것들 — JPQL window function, CTE, derived table, multiset (12장과 연결되는 다리).
  - dirty checking 비용 차단으로서의 projection — 엔티티가 아니면 PersistenceContext에 등록되지 않는다.
  - JPAB.org 표준 벤치(§3.4) 인용 자리 — projection vs entity fetch의 throughput 차이.
- **다룰 reference 섹션:** §2.10 전체, §2.11 전체, §5 권고 10, §3.4 JPAB 일부, §2.15 (SQM 다리).
- **내 코드 체크리스트 3개 예시:**
  - 가장 자주 호출되는 read API 5개가 엔티티를 반환하는지, DTO를 반환하는지.
  - Open Interface Projection을 쓰는 곳이 있다면, 그게 SELECT *을 유발하는지 검증했는지.
  - 분석/리포트성 쿼리에 Native나 jOOQ를 검토해 본 적이 있는지.
- **독자가 얻는 것:** *어떻게 가져오느냐*만큼 *어떤 형태로 가져오느냐*가 비용을 가른다는 시각. Projection 결정 트리 한 장.
- **예상 분량:** 약 18,000자.

---

### 6장. 트랜잭션 경계를 설계한다 — `@Transactional`과 OSIV

- **핵심 질문:** `@Transactional`을 붙이면 끝일까? 그리고 컨트롤러에서 lazy를 호출했는데 동작하는 이 환경은 *정상*인가?
- **주요 내용:**
  - Spring `@Transactional`의 속성 분해 — propagation(REQUIRED/REQUIRES_NEW/NESTED), isolation, rollbackFor의 함정(checked exception은 기본 롤백 X).
  - `readOnly=true`의 두 가지 효과 — FlushMode MANUAL + LoadedState 스냅샷 생략. *"서비스 디폴트 readOnly, write 메서드만 오버라이드"*의 코드 패턴.
  - read-write/read-only **라우팅** — `AbstractRoutingDataSource`로 replica에 read를 보낸다. `provider_disables_autocommit`이 필수 조건인 이유.
  - **OSIV 안티패턴 5가지** — 커넥션 lease, 트랜잭션 경계 깨짐, 계층 책임 누설, N+1 자유 발생, 테스트 어려움. Vlad 인용 박스 *"a solution to a problem that should not exist"*.
  - Spring Boot 2.0+의 경고와 `spring.jpa.open-in-view=false` 기본값. 새 프로젝트 첫 줄.
  - OSIV 옹호 입장(§4.1)과 타협안 — OSIV를 끄는 대신 5장의 EntityGraph + DTO Projection으로 보강.
  - **`hibernate.enable_lazy_load_no_trans=true` 명시 절 (본 개정에서 강조):** OSIV가 안티패턴이라면 이것은 *더 큰* 함정이다. lazy 호출마다 새 트랜잭션 = 커넥션 폭주 = 동일 트랜잭션 일관성 깨짐. *어떤 상황에서도 켜지 않는다*가 결론. 켜져 있는 환경 발견 시 즉시 끄는 절차.
- **다룰 reference 섹션:** §2.8 전체, §4.1 OSIV 논쟁, §2.17 enable_lazy_load_no_trans, §5 권고 17·18.
- **내 코드 체크리스트 3개 예시:**
  - `spring.jpa.open-in-view`가 `false`로 설정돼 있는지.
  - 서비스 클래스에 디폴트 `@Transactional(readOnly = true)`이 걸려 있는지, write 메서드는 오버라이드돼 있는지.
  - `enable_lazy_load_no_trans`가 *꺼져* 있는지 (켜진 상태가 사고 위치).
- **독자가 얻는 것:** 트랜잭션 경계를 *코드 한 줄이 아니라 시스템 설계*로 보는 시각. OSIV를 끄는 결단과 그 결과를 감당할 도구(5장의 Projection + 4장의 EntityGraph).
- **예상 분량:** 약 20,000자.

---

### 7장. 캐시는 정말 답인가 — 1차·2차·쿼리 캐시의 자리

- **핵심 질문:** 캐시를 켜면 빨라진다는 말은 어디까지 진실일까? 2차 캐시는 *언제* 켤 만한가?
- **주요 내용:**
  - 1차 캐시(PersistenceContext) — 트랜잭션 스코프, application-level repeatable read의 의미. 6장의 트랜잭션 정의 위에서 자연스럽게 풀린다. 배치에서는 OOM의 원인이라는 점(9장과 연결).
  - 2차 캐시를 켜는 정당한 조건 세 가지 — DB buffer pool 튜닝 후, replica로도 안 풀릴 때, 변경 빈도가 낮은 데이터.
  - Cache Concurrency Strategy 비교 표 — READ_ONLY / NONSTRICT_READ_WRITE / READ_WRITE / TRANSACTIONAL. 각 전략이 *어떤 일관성 모델*을 약속하는지 동사로 풀이.
  - **쿼리 캐시의 함정** — PK 목록만 저장하기 때문에 엔티티 캐시 없이 쓰면 N+1 재발. 단독 사용 금지.
  - Hibernate 자체 Query Plan Cache와 `in_clause_parameter_padding=true` — 동적 IN 절 plan 미스 방지.
  - 대규모 SaaS에서 2차 캐시 대신 application-level Redis cache aside를 쓰는 입장의 정당성(§4.4).
  - "DB가 못 받쳐주니까 캐시"가 아니라 "DB 부담을 분산"이 본래 목적이라는 결론.
- **다룰 reference 섹션:** §2.4 전체, §4.4 캐시 논쟁, §2.17의 query cache 안티패턴.
- **내 코드 체크리스트 3개 예시:**
  - 2차 캐시가 켜져 있다면, 어떤 엔티티에 어떤 concurrency strategy로 걸려 있는지.
  - 쿼리 캐시가 켜져 있다면, 그 쿼리가 가리키는 엔티티에 2차 캐시가 함께 켜져 있는지.
  - `in_clause_parameter_padding`이 켜져 있는지 (동적 IN을 쓰는 경우).
- **독자가 얻는 것:** 캐시를 켜기 *전에* 던져야 할 질문들. 2차 캐시의 정당화 기준과 쿼리 캐시의 위험을 분리해서 본다.
- **예상 분량:** 약 17,000자.

---

### 8장. 같은 row를 둘이 동시에 본다 — 락과 isolation의 실전

- **핵심 질문:** Read Committed에서도 일어나는 lost update를 어떻게 막을까? 그리고 낙관락과 비관락 중 무엇이 디폴트가 되어야 할까?
- **주요 내용:**
  - 동시성 anomaly 표 — Dirty read / Non-repeatable read / Phantom read / Lost update / Read/Write skew × Read Committed / Repeatable Read / Snapshot / Serializable. DB별 default(PG·Oracle·SQL Server = RC, MySQL InnoDB = RR).
  - MVCC와 Snapshot Isolation 직관 — PostgreSQL RR이 실제로는 SI라는 점, Hibernate의 PersistenceContext가 *application-level repeatable read*를 흉내내는 의의.
  - `@Version` 낙관락 — UPDATE 절의 `WHERE id=? AND version=?`, `OptimisticLockException`의 의미. *여러 HTTP 요청에 걸친 동시성 제어는 사실상 낙관락만이 답*.
  - `OPTIMISTIC_FORCE_INCREMENT`/`PESSIMISTIC_FORCE_INCREMENT` — 자식 변경을 부모 버전으로 전파.
  - Pessimistic locking — `PESSIMISTIC_READ/WRITE`, `SELECT ... FOR UPDATE`, PostgreSQL `SKIP LOCKED`로 job queue 만들기.
  - **MySQL InnoDB gap lock 명시 절 (본 개정에서 추가):** InnoDB의 RR 디폴트가 만들어내는 next-key lock = row lock + gap lock. Phantom 방지 메커니즘이지만 *예상치 못한 락 확장*의 원인. `@Lock` + LIMIT 조합에서의 사고 사례, READ COMMITTED로 내려서 푸는 선택의 트레이드오프, `innodb_locks_unsafe_for_binlog`의 역사적 맥락.
  - 결제·재고 도메인 사례 — 비관락이 정당화되는 자리. §4.2 논쟁 회수.
  - 합의 지점 — *낙관이 디폴트, 비관은 정당화가 필요한 선택*.
- **다룰 reference 섹션:** §2.7 전체, §4.2 낙관 vs 비관 논쟁, §3.6 학술 인용, §5 권고 12.
- **내 코드 체크리스트 3개 예시:**
  - 동시 수정 가능성이 있는 엔티티에 `@Version`이 있는지.
  - MySQL을 쓴다면, 핵심 트랜잭션의 isolation을 확인해 본 적이 있는지.
  - `SELECT ... FOR UPDATE`를 쓰는 곳이 있다면, gap lock의 범위를 추적해 봤는지.
- **독자가 얻는 것:** "내 도메인에 어떤 락을 써야 하는가"를 표 한 장으로 판단할 수 있다. lost update가 자기 코드 어디에서 일어날 수 있는지 알아본다.
- **예상 분량:** 약 22,000자.

---

### 9장. 한꺼번에 처리한다 — 배치와 대량 write

- **핵심 질문:** 30만 건 INSERT을 어떻게 30분이 아니라 1분에 끝낼까? 그리고 왜 `batch_size=25`를 넣었는데도 INSERT이 하나씩 나갈까?
- **주요 내용:**
  - **배치 INSERT/UPDATE 4종 세트** — `batch_size=25`, `order_inserts=true`, `order_updates=true`, `batch_versioned_data=true`. PostgreSQL 30만 건 벤치(51,785ms → 16,052ms, 3.2x).
  - PostgreSQL `reWriteBatchedInserts=true`로 multi-VALUES 재작성 추가 2~3x.
  - **IDENTITY가 batch를 죽이는 메커니즘 회수** — 3장의 결론을 배치 관점에서 다시. SEQUENCE pooled-lo의 정당성을 수치로.
  - 정식 배치 처리 패턴 — `flush()` + `clear()` + `commit()` + `begin()` 루프 코드. 7장의 1차 캐시 OOM 회수.
  - **StatelessSession 부활** (Hibernate 6.3+) — 배치 + UPSERT 지원. 1차 캐시·dirty checking 없이 high-volume ingest.
  - 벌크 UPDATE/DELETE — `@Modifying`, `clearAutomatically`/`flushAutomatically`. `CascadeType.REMOVE`와 `orphanRemoval`이 무시되는 함정, DB FK `ON DELETE CASCADE`로의 위임.
  - Criteria API Bulk, Blaze-Persistence Bulk.
  - 권고 #14(샤딩/스케일) 회수 자리 — 단일 노드 배치의 한계가 어디서 시작하는지, 그 너머로 가는 첫걸음.
- **다룰 reference 섹션:** §2.5(배치 절), §2.12 bulk, §3.2 PG 벤치, §5 권고 3·9·14.
- **내 코드 체크리스트 3개 예시:**
  - `hibernate.jdbc.batch_size` + `order_inserts` + `order_updates`가 함께 켜져 있는지.
  - 대량 INSERT 코드에 `flush() + clear()` 루프가 있는지.
  - 대량 ingest 경로에 StatelessSession 사용을 검토해 봤는지.
- **독자가 얻는 것:** 대용량 write 워크로드의 정석. 자기 프로젝트의 `application.yml`을 다시 열어 batch 4종을 확인하게 된다.
- **예상 분량:** 약 20,000자.

---

### 10장. 깊은 페이지도 첫 페이지처럼 — 페이지네이션 *[본 개정에서 분리]*

- **핵심 질문:** OFFSET 10,000을 넘기는 순간 왜 응답시간이 무너질까? 그리고 무한 스크롤은 어떻게 *depth-independent*하게 만들 수 있을까?
- **주요 내용:**
  - **OFFSET 페이지네이션의 한계 (§2.9):** "앞을 다 읽고 버린다"의 비용 시각화 — OFFSET=N일 때 DB가 N+limit 만큼 스캔한다는 점, 정렬 안정성 문제.
  - **Keyset pagination(seek method) 정석:**
    - `WHERE (created_at, id) < (?, ?) ORDER BY created_at DESC, id DESC LIMIT 20` 패턴.
    - composite key tie-breaking, NULL 처리, descending/ascending 혼합.
  - Blaze-Persistence `withKeysetExtraction(true)`로 자동 생성.
  - Spring Data 3.x **`WindowIterator`/`ScrollPosition`** — `KeysetScrollPosition` API. 무한 스크롤 첫 시민화.
  - **Hibernate 6 JPQL window function** — `ROW_NUMBER() OVER(...)`로 페이지 메타 계산 한 방. SQM이 가능하게 한 것.
  - 4장의 HHH000104(컬렉션 fetch + 페이지네이션) 결론 회수 — 2-query 패턴이 결국 keyset과 합쳐질 때.
  - 페이지네이션 + projection(5장) 결합 — list API의 정석 형태.
- **다룰 reference 섹션:** §2.9 전체, §2.15 (window function), §5 권고 9.
- **내 코드 체크리스트 3개 예시:**
  - 가장 큰 list API가 OFFSET 기반인지, keyset 기반인지.
  - 정렬 컬럼이 tie를 만들 때 두 번째 정렬 키(보통 PK)가 함께 들어가 있는지.
  - 깊은 페이지(예: 500페이지) 응답시간이 첫 페이지와 얼마나 다른지 측정해 본 적 있는지.
- **독자가 얻는 것:** OFFSET을 keyset으로 옮기는 구체적 절차. 무한 스크롤 / 깊은 페이지 / 컬렉션 페이지 세 가지 변종 모두 한 결정 트리에 정리.
- **예상 분량:** 약 16,000자.

---

### 11장. 보이지 않는 비용을 본다 — 관찰과 진단 *[본 개정에서 정체성 좁힘]*

- **핵심 질문:** 코드만 봐서는 모를 비용을 어떻게 *보이게* 만들 수 있을까? 그리고 N+1을 단위 테스트로 *영구히 잡으려면* 무엇이 필요할까?
- **주요 내용:**
  - SQL을 본다 — `org.hibernate.SQL` + `orm.jdbc.bind` 로깅, **datasource-proxy**의 그룹화 우수성, p6spy와 비교 표. 왜 production에서는 datasource-proxy를 권하는가.
  - **테스트에서 N+1을 잡는다** — Hypersistence Utils `SQLStatementCountValidator.assertSelectCount(1)`. CI에 회귀 테스트로 박는 패턴. 4장의 N+1 정의 회수.
  - **Hibernate Statistics** — read/write count, 캐시 hit ratio, slowest query, optimistic lock failure. production toggle 전략(샘플링).
  - **FlexyPool metrics** — connection acquire histogram, overflow 사용량. 2장의 풀 사이징 회수.
  - **Hypersistence Optimizer** — 정적 분석으로 50+ 안티패턴 자동 검출. 책에서 다뤘던 매핑·페치·캐시·트랜잭션 안티패턴을 한 번에.
  - **안티패턴 카탈로그 회수 (마지막 절):** 책 전체에서 다룬 안티패턴 12개를 표 한 장으로. *"내가 이 책을 시작할 때 했던 실수들"* 톤.
  - **36개 체크리스트 회수 표:** 1~10장 + 자기 자신(11장)의 체크리스트 36개를 한 표에 정렬. *책을 덮고 자기 코드로 돌아가는 자리*.
- **다룰 reference 섹션:** §2.16 전체, §2.17 안티패턴 표, §5 권고 1·10·15·16.
- **내 코드 체크리스트 3개 예시:**
  - CI 파이프라인에 SQL count 회귀 테스트가 박혀 있는지.
  - Production에서 Hibernate Statistics 일부라도 메트릭으로 보고 있는지.
  - 정적 분석(Hypersistence Optimizer)을 한 번이라도 돌려본 적 있는지.
- **독자가 얻는 것:** 진단 도구 한 세트와, 책 전체의 회수. 안티패턴이 자기 코드에 보일 때 정정할 수 있는 자신감.
- **예상 분량:** 약 18,000자.

---

### 12장. 그리고 그 다음 — 운영 기능과 다음 세계

- **핵심 질문:** 이 책 다음에 내가 봐야 할 것은 무엇인가? 그리고 *지금 당장* 우리 서비스에 보탤 수 있는 도구는 무엇인가?
- **주요 내용:**

  **12.1 운영 기능 — 오늘 쓸 수 있는 도구 (§2.13, §2.14):**
  - **Audit** — Hibernate Envers의 자리와 한계, *_AUD 테이블 폭발 문제, CDC + Debezium으로 옮겨가는 흐름.
  - **Soft Delete** — `@SoftDelete` 어노테이션(Hibernate 6.4+)이 구식 `@SQLDelete` + `@Where` 패턴을 어떻게 대체하는지.
  - **Multi-tenancy** 세 가지 전략 — DB / Schema / Discriminator. 2장 `StatementInspector`로 강제 주입하는 패턴 회수.
  - **Stored Procedure / `FunctionContributor`** — DB 함수를 JPQL에 노출. 분석 쿼리를 도메인으로 들고 오기 (5장 `@Subselect`와 짝).

  **12.2 다음 세계 — 한 발 더 나갈 자리 (§2.15, §4.3, §3.5, §4.7):**
  - **Hibernate 6의 SQM**이 가능하게 한 것들 — JPQL window function, CTE, derived table, multiset (5장·10장 회수).
  - `@JdbcTypeCode(SqlTypes.JSON)` / `SqlTypes.ARRAY` — PostgreSQL jsonb·text[]을 Hypersistence Utils 없이 매핑.
  - **JPA + jOOQ 조합의 의미 (§4.3):** write는 Hibernate, read는 jOOQ. Blaze-Persistence의 자리. **ORM Battle 2025 (§3.5) 벤치 인용 자리** — Hibernate vs jOOQ vs JDBC throughput 비교, 결론은 *경쟁이 아니라 분업*.
  - **Jakarta Data**(6.6+) — Spring Data 표준화의 흐름. Quarkus·Micronaut에서의 위치(§7 한계 #6 회수).
  - **Reactive(R2DBC)에 대한 입장** — *별개 패러다임*임을 명시. JPA를 잘 쓰는 것이 reactive보다 먼저 와야 한다는 견해(§7 한계 #7 회수).
  - **Hibernate 7 전망** — 집필 시점 release note 재확인 자리(§7 한계 #2 회수).

  **12.3 책의 닫음:**
  - 1장의 북극성 *"라운드트립과 트랜잭션 동작"*을 다시 가리킨다.
  - 11장의 36개 체크리스트를 *"오늘 코드 한 줄부터"*의 약속으로 회수.
  - 마지막 한 문장 — *"느린 JPA에는 이유가 있다. 그리고 그 이유는 거의 항상 들여다보면 보인다."*

- **다룰 reference 섹션:** §2.13, §2.14, §2.15, §3.4 JPAB, §3.5 ORM Battle, §4.3 jOOQ, §4.7 동적 쿼리, §7 한계 #2·#6·#7.
- **내 코드 체크리스트 3개 예시:**
  - Soft delete를 쓰고 있다면, `@SoftDelete`(H6.4+)로 옮길 만한지.
  - 분석성 쿼리에 jOOQ를 *부분 도입*할 만한 자리가 있는지.
  - 다음 분기 학습 계획에 Hibernate 6.6 / Jakarta Data가 포함돼 있는지.
- **독자가 얻는 것:** 책을 덮은 뒤 다음에 펼칠 자료의 지도. *"이 한 권으로 끝났다"가 아니라 "여기서부터 시작할 수 있다"*는 감각. 그리고 *오늘 당장* 보탤 수 있는 운영 기능 4종 카탈로그.
- **예상 분량:** 약 20,000자.

---

## 합계 분량 추정

| 챕터 | 예상 분량 |
|------|-----------|
| 1장 라운드트립 (64-tx 충격) | 16,000자 |
| 2장 커넥션·JDBC·statement caching | 20,000자 |
| 3장 엔티티 빚기 + bytecode enhancement | 22,000자 |
| 4장 N+1 | 20,000자 |
| **5장 Projection·query 선택** *[신설]* | 18,000자 |
| 6장 트랜잭션·OSIV (+ enable_lazy_load_no_trans) | 20,000자 |
| 7장 캐시 | 17,000자 |
| 8장 락·isolation (+ MySQL gap lock) | 22,000자 |
| 9장 배치·대량 write | 20,000자 |
| **10장 페이지네이션** *[분리]* | 16,000자 |
| 11장 관찰·진단 (좁힘) | 18,000자 |
| 12장 운영 기능 + 다음 세계 | 20,000자 |
| **합계** | **약 229,000자 (≈ 330p 상당)** |

서문·머리말·콜로폰·참고문헌 부록을 더하면 약 **24~25만 자 / 340~370p** 범위. 12장 구조의 정석 분량.

---

## reference 매핑 검증 (v2)

레퍼런스(§1~§7)의 모든 핵심 섹션이 챕터에 매핑되어 누락이 없음을 다시 표로 확인한다.

| 레퍼런스 섹션 | 주 챕터 | 보조 챕터 |
|----------------|----------|-----------|
| §1 개념과 정의 | 1장 | - |
| §2.1 Connection Pool | 2장 | 1장(충격 도입) |
| §2.2 Entity Mapping | 3장 | 9장(IDENTITY 회수) |
| §2.3 Fetching | 4장 | 6장(OSIV 연결) |
| §2.4 캐시 | 7장 | - |
| §2.5 Dirty Checking/Batch | 9장 | 3장(bytecode enhancement) |
| §2.6 Statement Caching | 2장 (정식 절) | - |
| §2.7 Locking | 8장 | - |
| §2.8 Transaction/Spring | 6장 | - |
| §2.9 Pagination | 10장 *[분리]* | - |
| §2.10 Projection | 5장 *[신설]* | 4장(예고), 9장(엔티티 회피) |
| §2.11 Query 선택 | 5장 *[신설]* | 12장(jOOQ) |
| §2.12 Bulk | 9장 | - |
| §2.13 Stored Procedure | 12장 | - |
| §2.14 Audit/Soft Delete/Multi-Tenancy | 12장 | 2장(StatementInspector) |
| §2.15 H6 신기능 | 12장 | 5장(SQM), 10장(window), 9장(StatelessSession) |
| §2.16 모니터링 | 11장 | 2장(StatementInspector) |
| §2.17 안티패턴 카탈로그 | 11장 (마지막 절) | 전 챕터 |
| §2.18 DB별 튜닝 | 2장 | 8장(MySQL gap), 9장(reWriteBatchedInserts) |
| §3.1 커넥션 풀 실험 | 1장(충격), 2장(깊이) | - |
| §3.2 PG 배치 벤치 | 9장 | - |
| §3.3 OSIV 게시판 사례 | 6장 | 4장 일부 |
| §3.4 JPAB 표준 벤치 | 5장 (projection 비교) | - |
| §3.5 ORM Battle 2025 | 12장 (jOOQ 절) | - |
| §3.6 학술 SI MVCC | 8장 | - |
| §4.1 OSIV 논쟁 | 6장 | - |
| §4.2 낙관 vs 비관 | 8장 | - |
| §4.3 JPA vs jOOQ | 12장 | - |
| §4.4 2차 캐시 | 7장 | - |
| §4.5 EAGER 절대금지? | 4장 | - |
| §4.6 IDENTITY | 3장, 9장 | - |
| §4.7 동적 쿼리 | 5장, 12장 | - |
| §5 14 tips | 분산 회수 (전 챕터) | - |
| §6 참고문헌 | 부록 | - |
| §7 리서치 한계 | 12장(#2·#6·#7), 부록(나머지) | - |

**누락 없음.** v2에서 §2.6(Statement caching)이 절로 승격, §2.10/§2.11이 5장으로 독립, §2.9가 10장으로 분리, §2.5의 bytecode enhancement가 3장으로 진입, §2.17의 안티패턴이 11장 마지막 절로 좁아졌다.

---

## 토비 스타일 정렬 확인 (v2)

본 개정에서도 토비 문체 요소를 챕터 제목·핵심 질문 단계에서 반영했다.

- **수사적 질문으로 챕터 진입:** 1장 "왜 JPA는 느릴까", 2장 "정확히 *언제* 커넥션을 잡을까", 3장 "왜 한쪽은 배치가 묶이고 다른 쪽은 한 줄씩 INSERT가 나갈까", 4장 "왜 우리 코드에는 여전히 N+1이 있을까", 5장 "N+1을 막았다고 끝일까", 6장 "`@Transactional`을 붙이면 끝일까", 7장 "캐시를 켜면 빨라진다는 말은 어디까지 진실일까", 8장 "낙관락과 비관락 중 무엇이 디폴트가 되어야 할까", 9장 "왜 `batch_size=25`를 넣었는데도 INSERT이 하나씩 나갈까", 10장 "OFFSET 10,000을 넘기는 순간 왜 응답시간이 무너질까", 11장 "코드만 봐서는 모를 비용을 어떻게 *보이게* 만들 수 있을까", 12장 "*지금 당장* 우리 서비스에 보탤 수 있는 도구는 무엇인가".
- **상황 가정 톤:** 핵심 질문 다수가 독자의 경험과 즉시 만나는 형식("우리 코드", "이 환경", "내 도메인").
- **권유형 어미:** 챕터 본문 저술 시 "~하자/살펴보자/주의해야 한다"의 빈도를 토비 스타일 가이드 수준으로 유지.
- **감정·감각 단어 자리:** 5장 *"가져오는 형태도 다시 본다"*, 7장 *"캐시는 정말 답인가"*, 11장 *"내가 이 책을 시작할 때 했던 실수들"* 톤이 예약돼 있다.
- **회수 구조:** 1장 북극성 + 64-tx 충격 → 매 챕터 끝 체크리스트 3개 → 11장 안티패턴 + 36개 체크리스트 한 표 회수 → 12장 마지막 다시 가리키기. 토비 글의 *"흩어 두고 모아 묶는"* 리듬.

---

## 리서치 한계 인지 (v1과 동일, 챕터 번호만 갱신)

레퍼런스 §7의 한계 8가지는 다음과 같이 흡수한다.

- **(1) Vlad의 영상 트랜스크립트** — 책 집필 단계에서 Devoxx/JavaZone 영상의 인상적 인용을 추가 수집해 본문 인용 박스로 보강.
- **(2) Hibernate 7·Jakarta Data 최신** — **12장** 집필 시점에 공식 release note를 재확인. 본 계획은 Hibernate 6.x 베이스라인 기준.
- **(3) 영어권 SNS 토론** — 6·7·8장 논쟁 단원에서 r/java 인기 thread 1~2건씩 추가 인용 보강.
- **(4) DB-side deep tuning** — 본 책의 범위 밖. 부록에서 *Use The Index, Luke!*(Markus Winand) 등 외부 자료를 가이드.
- **(5) 자체 JMH 벤치** — 본 계획에서는 Vlad·JPAB·ORM Battle 수치를 인용하되, 부록 코드 예제로 `vladmihalcea/high-performance-java-persistence` 리포지토리를 안내.
- **(6) Quarkus/Micronaut Data** — **12.2 다음 세계** 절에서 Jakarta Data와 함께 짧게 언급. 깊은 다이브는 후속 자료.
- **(7) Reactive(R2DBC)** — **12.2**에서 명시적으로 *별개 패러다임*임을 선언하고 본 책의 범위에서 제외한 이유를 밝힌다.
- **(8) Stack Overflow 직접 인용** — 4·5·6·8장에서 Vlad의 결정적 SO 답변 5~10개를 인용 박스로 흡수 (집필 단계 보강).

이 한계들은 모두 *책의 깊이를 떨어뜨리지 않는 선에서* 흡수 가능하며, 본 개정 단계에서 추가 리서치 트리거 없이 진행할 수 있다고 판단한다.
