# 고성능 JPA/Hibernate 레퍼런스 — Vlad Mihalcea의 시각으로

> 본 문서는 web-researcher / paper-researcher / community-researcher 세 채널을 통합한 결과다. 분량은 책 한 권을 받치는 깊이를 목표로 했으며, 인용·코드 스니펫·수치는 모두 출처를 명시한다. 출처 라벨은 다음과 같다.
> - `[웹]` Vlad Mihalcea 블로그 / Hibernate·Spring 공식 문서 / 일반 기술 블로그
> - `[책]` *High-Performance Java Persistence* (Vlad Mihalcea)
> - `[커뮤니티]` Stack Overflow / Reddit / velog / OKKY / 한국 기술 블로그
> - `[논문]` 학술 / 컨퍼런스 페이퍼

---

## 1. 개념과 정의

### 1.1 JPA / Hibernate / JDBC의 계층 구조

JPA는 자바 표준 영속성 스펙(JSR 338)이고, Hibernate는 그 사실상 표준 구현체다. 둘 다 최종적으로는 **JDBC** API 위에서 PreparedStatement를 실행하며, 그 아래는 DB 벤더의 드라이버와 옵티마이저가 자리한다 `[웹]`. Vlad의 표현을 빌리면 "ORM 위의 성능 문제는 거의 항상 JDBC 계층의 SQL과 트랜잭션 동작을 이해하지 못한 데서 온다" — 그래서 그의 책 *High-Performance Java Persistence*의 1부 전체가 **JDBC, 커넥션 관리, 배치, 스테이트먼트 캐싱, 트랜잭션 ANSI 표준** 같은 ORM 이전의 토대를 다룬다 `[책]`. 출처: <https://vladmihalcea.com/books/high-performance-java-persistence/>.

### 1.2 ORM 성능의 본질

> "Fetching too much data is the number one problem that causes performance issues when it comes to using JPA and Hibernate." — Vlad Mihalcea `[웹]`

ORM 성능은 *"객체 매핑이 빠르냐"*가 아니라 *"필요한 데이터만 정확한 시점에, 가장 적은 라운드트립으로 가져오는가"*의 문제다. 이 명제가 본 문서의 모든 영역(fetching, batching, caching, transaction, projection)에 일관되게 흐른다. 출처: <https://vladmihalcea.com/hibernate-performance-tuning-tips/>, <https://vladmihalcea.com/14-high-performance-java-persistence-tips/>.

### 1.3 두 가지 사고 도구

- **PersistenceContext = 1차 캐시 + dirty checking 스냅샷 + write-behind 큐.** 트랜잭션 동안 관리되는 엔티티 모두를 메모리에 들고 있으며, flush 시점에야 SQL로 토해낸다 `[웹]`. <https://vladmihalcea.com/the-anatomy-of-hibernate-dirty-checking/>
- **Database response time ≠ Application throughput.** 쿼리 하나가 빨라도 커넥션 점유 시간이 길면 동시 처리량은 떨어진다. Vlad는 이를 Universal Scalability Law(Neil Gunther)와 Little's Law로 설명한다 `[웹][논문]`. <https://vladmihalcea.com/optimal-connection-pool-size/>, <https://www.perfdynamics.com/Manifesto/USLscalability.pdf>

---

## 2. 핵심 주제별 정리

### 2.1 JDBC / Connection Pool 튜닝

#### HikariCP & 풀 사이즈

- 풀 사이즈가 클수록 좋다는 통념은 거짓이다. Universal Scalability Law에 따라 **"the maximum throughput of a database system is achieved for a limited number of database connections"**, 그 임계점을 넘으면 throughput은 오히려 떨어진다 `[웹]`.
- Vlad의 실험 — 64개 동시 송금 트랜잭션 워크로드 `[웹]`:
  - HikariCP 기본 10개 커넥션: 149ms
  - 64개로 늘리면: 272ms (악화)
  - FlexyPool이 발견한 최적값 4개: **128ms** (가장 빠름)
- 권장 절차: `connection = (core_count * 2) + effective_spindle_count` 같은 헐겁한 추정값에서 출발하되, **실측을 통해 튜닝한다**. FlexyPool의 `IncrementPoolOnTimeoutConnectionAcquisitionStrategy`로 acquire timeout마다 풀을 키워 가며 적정값을 발견하는 방법이 권장된다. 출처: <https://vladmihalcea.com/optimal-connection-pool-size/>, <https://vladmihalcea.com/connection-pool-sizing-with-flexy-pool/>

#### FlexyPool

- HikariCP, C3P0, DBCP2, Tomcat, Vibur를 감싸 **메트릭 + failover + 동적 리사이즈**를 제공하는 Vlad의 오픈소스 `[웹]`. 핵심 가치는 두 가지:
  1. **관측성** — connection acquire time, retry count, concurrent connections 분포(히스토그램)
  2. **adaptive overflow** — 기본 max-size 위에 임시 buffer를 두고, timeout이 잡힐 때마다 그 안에서 키운다
- 출처: <https://github.com/vladmihalcea/flexy-pool>, <https://vladmihalcea.com/tutorials/flexypool/>

#### 커넥션 lease time 줄이기 — `provider_disables_autocommit`

- Spring/Hibernate의 RESOURCE_LOCAL 트랜잭션은 기본적으로 `Connection.setAutoCommit(false)`을 호출하면서 너무 일찍 커넥션을 잡는다. Vlad는 `hibernate.connection.provider_disables_autocommit=true`를 켜고 풀(HikariCP) 쪽에서 `autoCommit=false`로 설정해, 실제 첫 SQL이 나갈 때까지 커넥션 획득을 지연시키도록 권한다 `[웹]`. 출처: <https://vladmihalcea.com/hibernate-performance-tuning-tips/>, <https://vladmihalcea.com/read-write-read-only-transaction-routing-spring/>

### 2.2 Entity Mapping 최적화

#### Identifier 전략 — IDENTITY는 배치를 죽인다

| 전략 | JDBC 배치 | 비고 |
|------|-----------|------|
| `GenerationType.IDENTITY` | **불가** | INSERT 직후 자동 생성된 PK를 받아야 하므로 write-behind 불가. Vlad: 5건 → 5번의 INSERT `[웹]` |
| `GenerationType.SEQUENCE` (pooled / pooled-lo optimizer) | 가능 | 권장. preallocate로 sequence 호출 자체도 줄임 |
| `GenerationType.TABLE` | 가능하지만 비싸다 | `SELECT ... FOR UPDATE`로 행 잠금. Vlad: "the row-level locking is definitely less efficient than using a native IDENTITY or SEQUENCE" |
| `GenerationType.AUTO` | DB에 따라 다름 | MySQL pre-10.3에선 TABLE로 떨어짐 — 지뢰 |

- 출처: <https://vladmihalcea.com/hibernate-identity-sequence-and-table-sequence-generator/>, <https://vladmihalcea.com/hibernate-batch-sequence-generator/>
- MySQL은 SEQUENCE 객체가 없어 어쩔 수 없이 IDENTITY를 쓰게 되는데, Vlad는 **수동 ID 할당 + 직접 INSERT batching** 기법을 소개한다 `[웹]`. <https://vladmihalcea.com/batch-insert-mysql-hibernate/>

#### `@Inheritance` 전략

`[책]` 12장 *Inheritance* 요지 `[웹]`:

- **SINGLE_TABLE** — 단일 테이블, 가장 빠른 read/write. 단점은 NOT NULL 제약을 자식 필드에 걸 수 없다는 점.
- **JOINED** — 부모/자식 테이블 join. 무결성↑ 성능↓. 자식 1개 fetch에 join 1번.
- **TABLE_PER_CLASS** — 폴리모픽 쿼리가 UNION ALL로 풀려 SQL이 비대해진다. Vlad: "can generate statements that are way too complex"
- **`@MappedSuperclass`** — 단순히 자바 상속만, DB에는 자식 테이블에 컬럼 복제. 폴리모픽 쿼리 필요 없을 때 가장 깔끔.

출처: <https://vladmihalcea.com/the-best-way-to-use-entity-inheritance-with-jpa-and-hibernate/>, <https://vladmihalcea.com/the-best-way-to-map-the-single_table-inheritance-with-jpa-and-hibernate/>

#### equals / hashCode

- **PK 기반 equality의 함정:** transient 상태(PK=null)일 때와 persisted 상태(PK 할당) 때의 hashCode가 달라지면 같은 객체가 Set에서 사라지는 *Set 슬립* 버그가 발생한다 `[웹]`.
- Vlad의 두 가지 정석 패턴:

```java
// 1. 비즈니스 키(자연 키)가 있을 때 — 가장 안전
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Book book)) return false;
    return Objects.equals(getIsbn(), book.getIsbn());
}
@Override public int hashCode() { return Objects.hash(getIsbn()); }

// 2. DB 생성 PK밖에 없을 때 — id null-safe + 상수 hashCode
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Post other)) return false;
    return id != null && id.equals(other.getId());
}
@Override public int hashCode() { return getClass().hashCode(); }
```

> Vlad: "Always return `getClass().hashCode()` for generated IDs — ensures consistency across entity state transitions."

출처: <https://vladmihalcea.com/the-best-way-to-implement-equals-hashcode-and-tostring-with-jpa-and-hibernate/>, <https://vladmihalcea.com/how-to-implement-equals-and-hashcode-using-the-jpa-entity-identifier/>

#### Immutable entities

읽기 전용 마스터 데이터에는 `@Immutable` + `@Cache(strategy=READ_ONLY)`. dirty checking 스냅샷을 만들지 않으므로 메모리/CPU 모두 절약. 자세한 사례는 2.4 캐시 단원과 2.6 dirty checking 단원에서 다룬다.

#### 컬렉션 매핑

- `@OneToMany`의 단방향 `List`는 `JoinTable`을 만들어 join 수가 더 늘어난다. **양방향 매핑 + 부모에서 자식 참조 추가하는 helper method**가 정석 `[웹]`. <https://vladmihalcea.com/the-best-way-to-map-a-onetomany-association-with-jpa-and-hibernate/>
- `@ManyToMany`에는 `List` 대신 `Set` 사용 — 동일 row 중복 삭제 시 전체 컬렉션을 비우고 다시 채우는 동작을 Hibernate가 한다 `[웹]`.
- 그러나 양방향 `@OneToMany`에는 `Set`을 피하라 — Vlad: "Avoid using Set for bidirectional JPA OneToMany collections" — 자식 컬렉션 평가가 모든 자식의 equals/hashCode를 호출하므로 비효율적 `[웹]`. <https://vladmihalcea.com/set-bidirectional-onetomany/>

### 2.3 Fetching 전략

#### N+1 문제

- **정의** `[웹]`: "the data access framework executes N additional SQL statements to fetch the same data that could have been retrieved when executing the primary SQL query." 슬로우 쿼리 로그로 안 잡힌다 — 각 추가 쿼리가 충분히 빠르기 때문이다.
- **발생 트리거:**
  - `@ManyToOne` / `@OneToOne`의 기본값 `FetchType.EAGER` — JPQL/Criteria에서 join이 아니라 secondary select로 풀린다 `[웹]`. <https://vladmihalcea.com/eager-fetching-is-a-code-smell/>
  - `FetchType.LAZY` 컬렉션을 view 또는 stream 안에서 iterate

#### 해결책 (Vlad 권장 순서)

1. **`JOIN FETCH` (JPQL/Criteria)** — 가장 단순한 해법. 단, paging과 조합 금지(아래 HHH000104 단원).
2. **`@EntityGraph` (선언적 fetch plan)** — Spring Data Repository에 그대로 붙일 수 있다. fetch graph vs load graph 구분:
   - `javax.persistence.fetchgraph` — 그래프에 있는 노드만 EAGER, 나머지는 강제 LAZY
   - `javax.persistence.loadgraph` — 그래프에 있는 노드는 EAGER, 그래프 밖은 mapping 기본 동작
3. **`@BatchSize` (개별) + `hibernate.default_batch_fetch_size` (글로벌)** — LAZY를 유지하면서도 `WHERE id IN (?, ?, ?, ...)` 한 방으로 묶는다. 한국 커뮤니티에서 가장 많이 추천되는 패턴 — velog `@joonghyun` `[커뮤니티]`: "100~1000 사이를 권장. 단 DB IN 절 제한(MS SQL 등 1000) 고려." 출처: <https://velog.io/@joonghyun/SpringBoot-JPA-JPA-Batch-Size%EC%97%90-%EB%8C%80%ED%95%9C-%EA%B3%A0%EC%B0%B0>, <https://vladmihalcea.com/hibernate-batch-fetching/>
4. **`@Fetch(FetchMode.SUBSELECT)`** — 단 하나의 자식 select로 묶지만, **모든 use case에 영향**을 미친다는 부작용 있음.

#### `JOIN FETCH` + Pagination 문제 (HHH000104)

- Hibernate 경고 `[웹]`: *"firstResult/maxResults specified with collection fetch; applying in memory!"*
- 원인: collection을 join하면 부모 row가 자식 수만큼 부풀려져 DB-level OFFSET이 의도와 어긋난다 — Hibernate가 안전을 위해 전 결과를 메모리에 로드한 뒤 페이징한다.
- **Vlad의 정석 — 2-query pattern:**
  ```java
  // 1) 부모 PK만 페이지로 뽑는다
  List<Long> postIds = em.createQuery("""
      select p.id from Post p where ... order by p.createdOn desc""", Long.class)
      .setFirstResult(0).setMaxResults(10).getResultList();

  // 2) 그 PK를 IN 절로 한 번에 JOIN FETCH
  List<Post> posts = em.createQuery("""
      select distinct p from Post p
      left join fetch p.comments c
      where p.id in :ids order by p.createdOn desc""", Post.class)
      .setParameter("ids", postIds).getResultList();
  ```
- 출처: <https://vladmihalcea.com/fix-hibernate-hhh000104-entity-fetch-pagination-warning-message/>, <https://vladmihalcea.com/join-fetch-pagination-spring/>
- 한국 커뮤니티는 같은 문제를 **"ToOne만 fetch join, ToMany는 `default_batch_fetch_size`로 처리"** 패턴으로 정리한다 `[커뮤니티]`: <https://velog.io/@hyojhand/JPA-%EC%BB%AC%EB%A0%89%EC%85%98-%EC%A1%B0%ED%9A%8C-%EC%B5%9C%EC%A0%81%ED%99%94-N1-fetch-join-batch-size>, <https://cheese10yun.github.io/jpa-fetch-paging/>

#### `FetchType.EAGER`은 코드 스멜이다 `[웹]`

- `@ManyToOne`, `@OneToOne`의 기본값이 EAGER인 것 자체가 함정.
- LAZY는 query 시점에서 EAGER로 끌어올릴 수 있지만, **EAGER는 query에서 다시 LAZY로 내릴 수 없다** — 전역적 fetch plan에 묶여 모든 use case가 비용을 치른다.
- Vlad 권고: "globally LAZY, per-query JOIN FETCH". 출처: <https://vladmihalcea.com/eager-fetching-is-a-code-smell/>

#### N+1 자동 탐지

- **datasource-proxy의 query count listener**로 단위 테스트에서 쿼리 카운트를 assert. Vlad: "leverage the custom listener support to assert the auto-generated statement count" `[웹]`.
- **Hypersistence Utils**의 `SQLStatementCountValidator` — Vlad가 직접 만든 헬퍼. `assertSelectCount(1)` 식으로 쓴다. <https://github.com/vladmihalcea/hypersistence-utils>

### 2.4 캐시 (1차 / 2차 / 쿼리 캐시)

#### 1차 캐시 (PersistenceContext)

- 트랜잭션-스코프, 자동, 끌 수 없음. 같은 PK로 `find`를 두 번 호출하면 두 번째는 DB에 가지 않는다 — *application-level repeatable read* `[웹]`. <https://vladmihalcea.com/non-repeatable-read/>
- 단점: 배치 처리에서 그대로 두면 OOM. `flush()` + `clear()` 주기적으로 (배치 단원 참조).

#### 2차 캐시 (Session 간 공유)

- 활성화: `hibernate.cache.use_second_level_cache=true` + RegionFactory(EhCache, Infinispan, Hazelcast, JCache).
- **언제 켜는가 — Vlad의 기준 `[책]` 16장:**
  1. DB buffer pool이 이미 적정 크기로 튜닝되어 있고
  2. read replica로도 못 막을 만큼 read-heavy
  3. 변경 빈도가 낮은 마스터/카탈로그성 데이터
  - 즉 "DB가 못 받쳐주니까 캐시"가 아니라 "DB 부담을 분산"이 본래 목적이다.

#### Cache Concurrency Strategies

| 전략 | 동작 | 적합한 데이터 |
|------|------|---------------|
| `READ_ONLY` | 캐시에서만 읽음, write 시 invalidate · update 자체가 예외 | 마스터 데이터, country code, immutable |
| `NONSTRICT_READ_WRITE` | "read-through, not write-through" — write 시점에 단순 invalidate. 짧은 DB↔캐시 drift 윈도 존재 `[웹]` | read-mostly + 정합성 약간 양보 가능 |
| `READ_WRITE` | soft lock — concurrent reads는 DB로 우회, write 직렬화 `[웹]` | write 빈도 있지만 강한 일관성 필요 |
| `TRANSACTIONAL` | XA — 캐시도 트랜잭션 참여. JTA 환경 전용 | 가장 비싸고 가장 강함 |

출처: <https://vladmihalcea.com/how-does-hibernate-read_write-cacheconcurrencystrategy-work/>, <https://vladmihalcea.com/how-does-hibernate-nonstrict_read_write-cacheconcurrencystrategy-work/>, <https://vladmihalcea.com/jpa-hibernate-second-level-cache/>

#### Query Cache

- 활성화: `hibernate.cache.use_query_cache=true` + 쿼리에 `org.hibernate.cacheable=true` 힌트.
- **위험:** query cache는 **결과의 PK 목록만** 저장한다. 그 PK들로 다시 엔티티를 들고 오는 단계에서 엔티티 캐시가 없거나 비활성이면 **N개의 추가 select**로 폭발 `[웹]`. Vlad: "ensure that the underlying entities are stored in the cache" — query cache는 단독으로 켜지 말 것.

#### Hibernate 자체 Query Plan Cache

- `hibernate.query.plan_cache_max_size` (default 2048), `hibernate.query.plan_parameter_metadata_max_size` (default 128) `[웹]`. 동적 IN 절을 자주 쓰면 plan cache 미스가 잦아 메모리 폭증 + 컴파일 비용 증가.
- 해결: `hibernate.query.in_clause_parameter_padding=true` — IN 절 파라미터 개수를 2의 멱수로 반올림해 plan을 재사용. 출처: <https://vladmihalcea.com/hibernate-query-plan-cache/>

### 2.5 Dirty Checking / Flush / Batch DML

#### Default dirty checking

- Hibernate는 load 시점에 **모든 속성의 스냅샷 사본**을 PersistenceContext에 저장. flush 시점에 현재값과 비교 — N개 엔티티 × P개 속성의 reflection 비교 `[웹]`. 메모리 두 배가 든다.
- Vlad: 큰 PersistenceContext는 그 자체로 안티패턴 — "Persistence Context Size: never bloat it with tons of managed entities."

#### Bytecode enhancement

- Maven/Gradle 플러그인으로 build-time에 setter에 dirty 플래그 인스트루먼테이션 삽입. 스냅샷 비교 없이 *어느 필드가 더러운지*를 추적 `[웹]`.
- 추가 효과: lazy attribute (필드 단위 lazy), association management, attribute lazy loading.
- 출처: <https://vladmihalcea.com/the-anatomy-of-hibernate-dirty-checking/>, <https://vladmihalcea.com/how-to-enable-bytecode-enhancement-dirty-checking-in-hibernate/>, <https://vladmihalcea.com/maven-gradle-hibernate-enhance-plugin/>

#### Batch INSERT / UPDATE 설정 — Vlad의 정식 세트

```properties
hibernate.jdbc.batch_size=25                  # 25 권장 (5~50)
hibernate.order_inserts=true                  # 같은 테이블끼리 묶음
hibernate.order_updates=true                  # update도 동일
hibernate.batch_versioned_data=true           # @Version 있는 엔티티의 UPDATE batching
hibernate.jdbc.batch_versioned_data=true      # JDBC 드라이버가 executeBatch 결과 정확히 리턴하는 경우만
```

- Vlad의 PostgreSQL 벤치 `[웹]`:

  | INSERT 개수 | no-batch | batch | speedup |
  |-------------|----------|-------|---------|
  | 30,000      | 5,889ms  | 2,640ms | 2.2x |
  | 300,000     | 51,785ms | 16,052ms | 3.2x |

- 함정: IDENTITY 사용 시 batch가 무효 (위 2.2 단원). PostgreSQL의 경우 `reWriteBatchedInserts=true` JDBC URL 옵션을 켜야 multi-VALUES INSERT로 재작성 — 추가 2~3배 성능. 출처: <https://vladmihalcea.com/how-to-batch-insert-and-update-statements-with-hibernate/>, <https://vladmihalcea.com/postgresql-multi-row-insert-rewritebatchedinserts-property/>

#### 정식 배치 처리 패턴

```java
EntityManager em = emf.createEntityManager();
EntityTransaction tx = em.getTransaction();
int batchSize = 25;
try {
    tx.begin();
    for (int i = 0; i < entityCount; i++) {
        if (i > 0 && i % batchSize == 0) {
            tx.commit();
            tx.begin();
            em.clear();
        }
        em.persist(new Post("Post " + (i + 1)));
    }
    tx.commit();
} catch (RuntimeException e) {
    if (tx.isActive()) tx.rollback();
    throw e;
} finally {
    em.close();
}
```

출처: <https://vladmihalcea.com/the-best-way-to-do-batch-processing-with-jpa-and-hibernate/>

#### `StatelessSession` — Persistence Context를 끄는 옵션

- Hibernate 6 이전: batching/UPSERT 미지원으로 활용도 낮음.
- Hibernate 6.3+: **batch 지원 + UPSERT 메서드** 추가 — 진정한 high-volume ingest 도구로 부활 `[웹]`.
- 1차 캐시·dirty checking·cascade가 없으므로 단순 INSERT/UPDATE/DELETE 대량 처리에 최적. 출처: <https://vladmihalcea.com/hibernate-statelesssession-jdbc-batching/>, <https://vladmihalcea.com/hibernate-statelesssession-upsert/>

### 2.6 Statement Caching

#### PostgreSQL (pgjdbc)

- 기본 `prepareThreshold=5` — 같은 SQL이 5번 실행되어야 server-side prepare로 승격. 그 전까지는 매번 prepare+execute을 한 round-trip으로 보냄(소위 simple query) `[웹]`.
- 캐시 사이즈: `preparedStatementCacheQueries=256`, `preparedStatementCacheSizeMiB=5`. 출처: <https://vladmihalcea.com/postgresql-jdbc-statement-caching/>
- 동적 SQL이 많으면 plan-cache miss → server-side에 동일 plan이 안 쌓임. `plan_cache_mode=force_custom_plan` 또는 `auto` 활용. <https://vladmihalcea.com/postgresql-plan-cache-mode/>

#### MySQL (mysql-connector-j)

- 기본은 **client-side prepare** (`useServerPrepStmts=false`) — 드라이버가 파라미터를 inlining해서 single round-trip으로 보냄.
- Vlad 권장 (MySQL 8.0.22 벤치 기준) `[웹]`:
  ```properties
  useServerPrepStmts=false        # client-side 유지
  cachePrepStmts=true             # ParseInfo 캐시 켬
  prepStmtCacheSize=500           # 기본 25는 턱없이 작음
  prepStmtCacheSqlLimit=1024      # 긴 SQL도 캐시
  ```
- server-side로 바꾸면 prepare/execute 두 round-trip이 되며, 캐시 없으면 매번 부담. throughput·p99 모두 client-side가 우세. 출처: <https://vladmihalcea.com/mysql-jdbc-statement-caching/>

#### `StatementInspector`

- `hibernate.session_factory.statement_inspector`에 등록된 콜백이 모든 SQL을 가로채 수정·로깅 가능. multi-tenancy의 tenant_id 주입, 강제 hint 삽입, statement-level audit에 활용 `[웹]`. <https://vladmihalcea.com/hibernate-statementinspector/>

### 2.7 Locking · Isolation · MVCC

#### 동시성 anomaly 매핑

| Anomaly | Read Committed | Repeatable Read | Snapshot Isolation | Serializable |
|---------|----------------|-----------------|--------------------|--------------|
| Dirty read | 방지 | 방지 | 방지 | 방지 |
| Non-repeatable read | **발생** | 방지 | 방지 | 방지 |
| Phantom read | 발생 | DB별 다름 | 방지 (MVCC) | 방지 |
| Lost update | **발생** | 방지 (MySQL InnoDB) | 방지 | 방지 |
| Read/Write skew | 발생 | 발생 | 발생 | 방지 (PostgreSQL SSI) |

- 출처: <https://vladmihalcea.com/non-repeatable-read/>, <https://vladmihalcea.com/phantom-read/>, <https://vladmihalcea.com/a-beginners-guide-to-database-locking-and-the-lost-update-phenomena/>, <https://vladmihalcea.com/write-skew-2pl-mvcc/>
- 데이터베이스별 default: PostgreSQL/Oracle/SQL Server = Read Committed, MySQL InnoDB = Repeatable Read.

#### MVCC

- PostgreSQL의 Repeatable Read는 실제로는 **Snapshot Isolation** — read는 write를 블록하지 않고, write도 read를 블록하지 않는다 `[웹][논문]`. Hekaton/HyPer 계열 fast serializable MVCC 연구도 같은 흐름. <https://db.in.tum.de/~muehlbau/papers/mvcc.pdf>
- Hibernate는 application-level repeatable read를 **PersistenceContext 캐싱**으로 흉내낸다 — 같은 트랜잭션 내 같은 PK는 한 번만 SELECT.

#### Optimistic Locking — `@Version`

```java
@Entity
public class Product {
    @Id @GeneratedValue private Long id;
    @Version private Long version;
    private BigDecimal price;
}
```

- UPDATE 시 `WHERE id=? AND version=?` 자동 추가. 매치 0 row면 `OptimisticLockException` (또는 `StaleObjectStateException`) `[웹]`.
- **여러 HTTP 요청(=여러 DB 트랜잭션)에 걸친 동시성 제어가 가능한 거의 유일한 방법.** 비관락은 다음 요청까지 락을 들고 있을 수 없다. 출처: <https://vladmihalcea.com/optimistic-vs-pessimistic-locking/>

#### `OPTIMISTIC_FORCE_INCREMENT` / `PESSIMISTIC_FORCE_INCREMENT`

- 자식의 변경을 부모 엔티티 버전에 propagate해야 할 때 (예: Post에 새 PostComment 추가 시 Post.version 증가) `[웹]`.
- OPTIMISTIC_FORCE_INCREMENT: UPDATE 한 방으로 버전 체크 + 증가, 트랜잭션 끝에서 검증.
- PESSIMISTIC_FORCE_INCREMENT: 즉시 적용 — 현재 트랜잭션에서 곧바로 결과 알 수 있음.
- 출처: <https://vladmihalcea.com/hibernate-locking-patterns-how-does-optimistic_force_increment-lock-mode-work/>, <https://vladmihalcea.com/hibernate-locking-patterns-how-does-pessimistic_force_increment-lock-mode-work/>

#### Pessimistic Locking — `LockModeType.PESSIMISTIC_READ/WRITE`

- DB-level `SELECT ... FOR SHARE` / `FOR UPDATE`. **same-transaction**에만 유효.
- 사용 케이스: 충돌이 극심해 retry 비용이 retry 횟수만큼 누적되는 경우, 또는 외부 시스템 호출 같은 비가역 작업을 보호할 때 `[웹]`.
- Vlad의 권고 — *"낙관락이 디폴트, 비관락은 정당화가 필요한 선택"*.

### 2.8 Transaction · Spring `@Transactional`

#### Spring `@Transactional` 속성

- `propagation` 기본값 `REQUIRED`. `REQUIRES_NEW`는 새 물리 트랜잭션·새 커넥션 — 풀 경쟁 유발 가능. `NESTED`는 savepoint 기반, JDBC만 가능.
- `isolation` — 기본은 DB default. 비즈니스 요구로 올릴 때만 명시.
- `readOnly=true` — 아래 별도 설명.
- `rollbackFor` — 기본은 RuntimeException + Error만. **checked exception**은 기본 롤백 X. 도메인 예외가 checked면 명시 필요.
- 출처: <https://vladmihalcea.com/spring-transactional-annotation/>, <https://vladmihalcea.com/spring-transaction-best-practices/>

#### `@Transactional(readOnly=true)` 최적화

- Hibernate에 두 가지 효과 `[웹]`:
  1. **FlushMode = MANUAL** — auto-flush 안 함, dirty checking 사실상 무효화
  2. (Spring 5.1+) **read-only 플래그가 Hibernate Session까지 전파** — entity의 LoadedState 스냅샷을 만들지 않음 → 메모리 절반
- Vlad의 best practice: 서비스 클래스에 `@Transactional(readOnly=true)` 디폴트, write 메서드만 `@Transactional`로 오버라이드 `[웹]`. 출처: <https://vladmihalcea.com/spring-read-only-transaction-hibernate-optimization/>

#### Read-Write / Read-Only Routing

`AbstractRoutingDataSource` + `TransactionSynchronizationManager.isCurrentTransactionReadOnly()`로 read-only 트랜잭션은 replica로, read-write는 primary로 라우팅 — write scaling을 건드리지 않고 read scaling 확보 `[웹]`:

```java
public class TransactionRoutingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        return TransactionSynchronizationManager.isCurrentTransactionReadOnly()
            ? DataSourceType.READ_ONLY : DataSourceType.READ_WRITE;
    }
}
```

`hibernate.connection.provider_disables_autocommit=true`가 함께 켜져 있어야 routing이 의도대로 동작한다 (커넥션 획득 지연). 출처: <https://vladmihalcea.com/read-write-read-only-transaction-routing-spring/>

#### Open Session in View (OSIV) 안티패턴

Vlad가 시리즈로 가장 강하게 비판하는 패턴 `[웹]`. 다섯 가지 문제:

1. **커넥션 lease time** — view 렌더링 끝날 때까지 DB 커넥션 점유.
2. **트랜잭션 경계 깨짐** — 서비스에서 트랜잭션 종료 후 view에서 lazy 로딩하면 그 statement는 auto-commit으로 실행 → flush per statement.
3. **계층 책임 누설** — view에서 lazy 호출이 SQL을 발생시키니 UI/Repository 경계가 흐려짐.
4. **N+1의 자유로운 발생** — 컨트롤러 작성자가 ORM 비용을 모른 채 lazy navigation.
5. **테스트 어려움** — 통합 테스트 없이는 lazy load 동작 검증 불가.

> "Open Session in View is a solution to a problem that should not exist in the first place. The most likely root cause is relying exclusively on entity fetching."

Spring Boot 2.0+ 부터는 OSIV 활성화 시 경고 출력. `spring.jpa.open-in-view=false`가 정답. 출처: <https://vladmihalcea.com/the-open-session-in-view-anti-pattern/>

### 2.9 Pagination

#### OFFSET 페이지네이션의 한계

- LIMIT/OFFSET은 *"앞에 OFFSET개를 읽고 버린다"* — 깊은 페이지는 비례해서 느려진다. PostgreSQL 인덱스 스캔으로도 page 1000을 가려면 N×1000 row를 훑어야 한다.

#### Keyset Pagination (Seek Method)

- 마지막으로 본 row의 정렬 키를 cursor로 사용해 `WHERE (created_on, id) > (?, ?) ORDER BY created_on, id LIMIT N` `[웹]`.
- 동일 페이지 크기일 때 인덱스 효율 일정 — **깊이 무관 동일 응답시간**. 모든 페이지를 random access 안 하고 forward iterate하는 워크플로(피드, 무한 스크롤)에 적합.
- JPA에는 native 지원 없음. 옵션:
  - **Blaze-Persistence**의 `withKeysetExtraction(true)` + `PagedList` — Vlad 강력 추천 `[웹]`. <https://vladmihalcea.com/keyset-pagination-jpa-hibernate/>
  - **Spring Data `WindowIterator` / `Window`** — Spring Data JPA 3.x부터 keyset 지원. `findBy...(ScrollPosition.keyset(), Limit.of(10))`. <https://vladmihalcea.com/spring-data-windowiterator/>

#### Window Functions로 한 방에

- `ROW_NUMBER() OVER (...)`로 전체 카운트와 페이지를 한 쿼리에서. Hibernate 6 JPQL window function 지원 — `[웹]` <https://vladmihalcea.com/hibernate-jpql-window-functions/>

### 2.10 Projection

#### 옵션과 선택 기준 `[웹]`

| 방법 | 형태 | 권장 시나리오 |
|------|------|---------------|
| Constructor expression `new com.acme.PostDto(p.id, p.title)` | JPQL only | DTO 클래스 있고 JPQL 사용 |
| `Tuple` | `select p.id as id, p.title as title from Post p` → `tuple.get("title")` | 일회성, DTO 만들기 싫을 때 |
| `@SqlResultSetMapping` + `@ConstructorResult` | Native SQL 매핑 | Native SQL을 JPA 표준으로 매핑 |
| `ResultTransformer` (legacy) / `TupleTransformer` (Hibernate 6+) | Hibernate-specific | 동적 매핑, BigInteger→Long 등 타입 변환 자유도 |
| Spring Data Interface Projection | `interface PostSummary { Long getId(); String getTitle(); }` | Spring Data 환경, 간단한 read-only |
| **Java Records + JPQL constructor expression** | `select new acme.PostDto(p.id, p.title) ...` Record | Java 16+, immutable DTO |

출처: <https://vladmihalcea.com/the-best-way-to-map-a-projection-query-to-a-dto-with-jpa-and-hibernate/>, <https://vladmihalcea.com/hibernate-tupletransformer/>, <https://vladmihalcea.com/java-records-jpa-hibernate/>, <https://vladmihalcea.com/spring-jpa-dto-projection/>

#### `@Subselect`

- 가상의 read-only entity를 임의 SQL/뷰 위에 매핑. 복잡한 분석 쿼리를 Domain 객체로 들고 오면서도 update 안 됨이 보장 `[웹]`.

#### One-to-Many DTO projection

- 여러 row를 하나의 부모 DTO에 모으는 패턴은 `TupleTransformer` 또는 Blaze-Persistence의 **MULTISET**으로 처리 — Hibernate 6.3+는 JPQL에 `multiset` 지원 `[웹]`. <https://vladmihalcea.com/one-to-many-dto-projection-hibernate/>, <https://vladmihalcea.com/blaze-persistence-multiset/>

### 2.11 Native Query / HQL / JPQL / Criteria — 선택 기준

Vlad의 입장 `[웹]`:

> "When it comes to reading data, nothing can beat native SQL because the most commonly-used RDBMS have implemented non-standard data access techniques (window functions, CTE, PIVOT) and the SQL-92 JPA abstraction layer can only focus on common functionalities."

- **JPQL** — 엔티티 graph 따라가는 단순 read/write. 80% 케이스.
- **Criteria API** — *동적 쿼리* (Specification 패턴). 단점은 verbose + plan cache miss 위험.
- **Native SQL** — DB-specific feature(윈도, CTE, JSON 함수, PIVOT, MERGE)가 필요한 모든 read.
- **Blaze-Persistence** — Criteria의 진화형. LATERAL JOIN, CTE, window function을 type-safe API로. Vlad: "if you are using JPA and Hibernate, you should definitely use Blaze Persistence as well." 출처: <https://vladmihalcea.com/blaze-persistence-jpa-criteria-queries/>
- **jOOQ** — JPA write + jOOQ read 조합. type-safe dynamic SQL, SQL-injection 보강, 복잡한 분석 쿼리. JPA의 entity 매핑은 그대로 두고 read 경로만 jOOQ로 분리. <https://vladmihalcea.com/jooq-facts-from-jpa-annotations-to-jooq-table-mappings/>

### 2.12 Bulk Operations

#### 벌크 UPDATE/DELETE

```java
int updated = em.createQuery("""
    update Post p set p.status = :s where p.createdOn < :d""")
    .setParameter("s", Status.ARCHIVED)
    .setParameter("d", oneYearAgo)
    .executeUpdate();
```

- Spring Data Repository에서는 `@Modifying`. `clearAutomatically`로 1차 캐시 초기화, `flushAutomatically`로 사전 flush — 그 전에 변경된 dirty entity가 사라질 수 있다는 점에 주의 `[웹]`. <https://www.baeldung.com/spring-data-jpa-modifying-annotation>
- **`CascadeType.REMOVE`와 `orphanRemoval`은 bulk delete에서 무시된다.** Vlad: "Using CascadeType.REMOVE and orphanRemoval is pointless for bulk operations." — 자식부터 명시적으로 지우거나, DB FK에 `ON DELETE CASCADE` 위임. 출처: <https://vladmihalcea.com/bulk-update-delete-jpa-hibernate/>

#### Criteria API Bulk

JPA 2.1부터 `CriteriaUpdate`, `CriteriaDelete` 지원. 동적 bulk가 필요할 때 사용. <https://vladmihalcea.com/jpa-criteria-api-bulk-update-delete/>

#### Blaze-Persistence Bulk

returning clause(PostgreSQL `RETURNING`, SQL Server `OUTPUT`)와 결합해 *update와 동시에 영향받은 row 회수* 가능. <https://vladmihalcea.com/bulk-update-delete-blaze-persistence/>

### 2.13 Stored Procedure / Function

- `@NamedStoredProcedureQuery`, `EntityManager.createStoredProcedureQuery(...)`. IN/OUT 파라미터, REF_CURSOR.
- Hibernate `MetadataBuilder.applySqlFunction()` 또는 `FunctionContributor` SPI로 **DB 함수를 JPQL에서 호출**할 수 있게 등록 — `function('jsonb_extract_path_text', col, 'key')` 같은 식.

### 2.14 Audit / Soft Delete / Multi-Tenancy

#### Audit — Hibernate Envers

- 감사 대상 엔티티마다 `_AUD` 미러 테이블 자동 생성. revision 단위로 INSERT/UPDATE/DELETE 이력 보관 `[웹]`. <https://vladmihalcea.com/the-best-way-to-implement-an-audit-log-using-hibernate-envers/>
- 단점: 모든 변경마다 추가 INSERT, table 두 배. write heavy 시스템엔 CDC + Debezium이 더 적합.

#### Soft Delete

- 구식 패턴: `@SQLDelete(sql = "UPDATE post SET deleted = true WHERE id = ?")` + `@Where(clause = "deleted = false")`.
- **Hibernate 6.4+** 의 `@SoftDelete` 어노테이션이 정식 지원 — 한 줄로 처리. Vlad: "much easier to just use the native Hibernate mechanism" `[웹]`. <https://vladmihalcea.com/hibernate-softdelete-annotation/>
- 함정: `@OneToOne`, `@ManyToOne` 참조가 deleted row를 가리키면 일관성 보장 어려움 — Vlad: *"you can barely count on consistent behavior."*

#### Multi-Tenancy

- 세 가지 전략:
  - **Database-per-tenant** — 격리 최강, 운영 비용 최대.
  - **Schema-per-tenant** — PostgreSQL `SET search_path`, Hibernate `MultiTenantConnectionProvider` `[웹]`. <https://vladmihalcea.com/hibernate-database-schema-multitenancy/>
  - **Discriminator** — 모든 테이블에 tenant_id 컬럼. SQL마다 WHERE 추가 — `StatementInspector`로 강제하거나 Hibernate `@TenantId` 사용. <https://vladmihalcea.com/database-multitenancy/>
- `CurrentTenantIdentifierResolver`로 현재 tenant 식별, `hibernate.tenant_identifier_resolver`에 등록.

### 2.15 Hibernate 6.x 신기능 정리

- **새로운 query parser (SQM — Semantic Query Model)** — 더 빠른 JPQL 컴파일, 더 정확한 type inference, 더 풍부한 SQL 생성 `[웹]`.
- **JPQL window function · CTE · derived table · multiset** — JPA 표준 밖이지만 Hibernate에서 사용 가능. <https://vladmihalcea.com/hibernate-jpql-window-functions/>
- **`@JdbcTypeCode(SqlTypes.JSON)`** — Hypersistence Utils 없이도 PostgreSQL `jsonb`, MySQL `JSON`, Oracle SODA 매핑 가능 `[웹]`. <https://vladmihalcea.com/how-to-map-json-objects-using-generic-hibernate-types/>
- **`@JdbcTypeCode(SqlTypes.ARRAY)`** — PostgreSQL `text[]`, `integer[]` 등 native array. <https://vladmihalcea.com/how-to-map-java-and-sql-arrays-with-jpa-and-hibernate/>
- **StatelessSession 강화** — 배치, UPSERT 지원 (6.3+).
- **`@SoftDelete` 어노테이션** (6.4+).
- **Jakarta Data 지원 시작** (6.6+) — Spring Data 같은 인터페이스 기반 repository 표준화.
- **ResultSet read by index, not by alias** — Hibernate 5 대비 read 경로 자체가 빨라짐.
- **Embeddable 상속** — `@MappedSuperclass`처럼 embeddable도 상속 가능.

### 2.16 모니터링 / 디버깅

#### Hibernate Statistics

- `hibernate.generate_statistics=true`. `SessionFactory#getStatistics()`로 read/write count, 캐시 hit ratio, slowest query, optimistic lock failure 등 노출. Micrometer로 metric export 가능.
- production에선 통상 disabled — overhead 있음. 트러블슈팅 시 on/off 토글.

#### datasource-proxy vs p6spy `[웹]`

| 항목 | datasource-proxy | p6spy |
|------|------------------|-------|
| 설정 방식 | Java programmatic — Spring 친화 | declarative `spy.properties` — Java EE 친화 |
| Batch 가시화 | 그룹화 우수 | row-by-row |
| Custom listener (N+1 detect) | 강력 | 가능 |
| JDBC 드라이버 프록시 | DataSource만 | 드라이버·DataSource 모두 |

Vlad: 개발 환경엔 datasource-proxy + `SQLStatementCountValidator`로 단위 테스트 단계에서 N+1을 잡는다. 출처: <https://vladmihalcea.com/the-best-way-to-log-jdbc-statements/>, <https://github.com/vladmihalcea/hypersistence-utils>

#### FlexyPool metrics

- 분포 메트릭: connection acquisition time histogram, max pool size 도달 여부, overflow 사용량, retry count.
- Dropwizard Metrics 또는 Micrometer로 backend 연결.

#### Hypersistence Optimizer

- Vlad가 만든 상용 도구 — 엔티티 매핑·설정의 잘 알려진 안티패턴 50+ 종을 정적 검사. (예: EAGER ManyToOne, IDENTITY 사용 시 batch off, `Set` 양방향 OneToMany 등) `[웹]`. <https://vladmihalcea.com/hypersistence-optimizer/>

### 2.17 안티패턴 카탈로그

| 안티패턴 | 증상 | 정답 |
|----------|------|------|
| `OSIV=true` | 커넥션 lease 증가, view에서 lazy N+1 | `open-in-view=false` + DTO/`JOIN FETCH` |
| `FetchType.EAGER` | 모든 query에 join/secondary select | 모두 LAZY + per-query fetch plan |
| `hibernate.enable_lazy_load_no_trans=true` | LIE 안 나지만 매 lazy마다 새 트랜잭션 — 커넥션 폭주 `[웹]` | 정상 fetch 또는 DTO. <https://vladmihalcea.com/the-hibernate-enable_lazy_load_no_trans-anti-pattern/> |
| `Hibernate.initialize(proxy)`를 view에서 호출 | OSIV 변종 | 서비스에서 fetch 종료 후 반환 |
| `IDENTITY` + batch 기대 | 배치 안 묶임 | SEQUENCE 또는 수동 INSERT batching |
| `@OneToMany List` 양방향 + frequent remove | `delete all + reinsert` 폭발 | `Set` 또는 explicit join entity |
| Repository에 `@Transactional` | 메서드별 트랜잭션 — atomicity 깨짐 | 서비스 계층에 위치 |
| EntityManager 누수 | dev에서는 정상, prod에서 풀 고갈 | 항상 try-with-resources / Spring 위임 |
| 트랜잭션 누수 (`begin` 후 `commit` 없이 return) | warm-up까지는 동작, 부하 시 hang | `TransactionTemplate` 또는 Spring `@Transactional` 일관 사용 |
| 거대한 PersistenceContext | dirty checking이 O(N×P) | 주기적 `flush()` + `clear()`, Stateless session |
| Query cache 단독 사용 | N+1 다시 발생 | 엔티티 캐시와 함께 사용 |
| Bulk delete + `CascadeType.REMOVE` 기대 | 자식 row 안 지워짐 | DB FK ON DELETE CASCADE 또는 명시적 자식 delete 먼저 |
| `@Transactional(rollbackFor=...)` 누락 | checked exception에 commit | 도메인 exception 명시 |

### 2.18 데이터베이스별 튜닝 포인트

#### PostgreSQL

- `reWriteBatchedInserts=true` JDBC URL 옵션 — multi-row VALUES로 재작성 → 2~3x.
- `plan_cache_mode=force_custom_plan` — bind variable peeking이 잘못된 plan을 잡았을 때.
- `jsonb` + GIN 인덱스로 JSON 쿼리 빠르게.
- MVCC = Snapshot Isolation — Repeatable Read를 골라도 SSI Serializable이 별도로 있음.

#### MySQL

- SEQUENCE 없음 — IDENTITY 강제. batch 쓰려면 수동 ID 또는 stateless 우회.
- `useServerPrepStmts=false` + `cachePrepStmts=true` 권장.
- InnoDB Repeatable Read는 **gap lock**으로 phantom 부분 차단 — Oracle/Postgres와 다른 양상.
- `rewriteBatchedStatements=true` JDBC URL 옵션 (Connector/J 5.1.13+).

#### Oracle

- `defaultRowPrefetch` 기본 10 — 큰 ResultSet에선 너무 작음. `hibernate.jdbc.fetch_size=100~500`.
- SEQUENCE 천국. cache·noorder·nocycle 활용.
- AWR/ASH로 부하 분석. server-side hint(`/*+ INDEX(...) */`) 필요한 경우는 native query로 우회.

---

## 3. 사례 / 벤치마크

### 3.1 Vlad의 connection pool 실험 (다시 강조)

- 64 동시 트랜잭션, 10 vs 64 vs 4(FlexyPool 발견치) → 149ms / 272ms / 128ms `[웹]`. 너무 많은 커넥션이 DB-level contention(latch, lock manager)을 키워 더 느려진다는 직관 반증.

### 3.2 PostgreSQL 배치 INSERT 벤치 `[웹]`

| 행 수 | no batch | batch_size=25 | speedup |
|-------|----------|---------------|---------|
| 30,000 | 5,889 ms | 2,640 ms | 2.2x |
| 300,000 | 51,785 ms | 16,052 ms | 3.2x |

여기에 `reWriteBatchedInserts=true`까지 더하면 추가 2~3x.

### 3.3 OSIV 켜진 채 인기 게시판 — 한국 커뮤니티 사례 `[커뮤니티]`

velog `@gwanghyeonkim`, `@sdsd0908` 등의 사례에서 반복되는 패턴: 게시판 목록 화면에서 paging + fetch join + ToMany를 같이 쓰다 HHH000104 경고 → 메모리 OOM → DB OOM 순으로 장애. 해결책으로 모두 `default_batch_fetch_size=100~1000` + ToOne만 fetch join 패턴으로 수렴. 출처: <https://velog.io/@gwanghyeonkim/JPA%EC%97%90%EC%84%9C-Paging%EA%B3%BC-Fetch-Join%EC%9D%84-%EA%B0%99%EC%9D%B4-%EC%82%AC%EC%9A%A9%ED%95%98%EB%A9%B4-%EC%95%88-%EB%90%98%EB%8A%94-%EC%9D%B4%EC%9C%A0>, <https://velog.io/@sdsd0908/Spring-JPA-1N-Fetch-Join-%ED%8E%98%EC%9D%B4%EC%A7%95-%EB%AC%B8%EC%A0%9C%EC%99%80-Batch-Size-%EC%84%A4%EC%A0%95-%EC%8B%9C-%EC%A3%BC%EC%9D%98%EC%82%AC%ED%95%AD>

### 3.4 JPAB.org 표준 벤치

- 다양한 JPA provider (Hibernate, EclipseLink, OpenJPA, DataNucleus) × DBMS 조합으로 CRUD throughput 측정. Hibernate가 "analytical data processing 기준 가장 빠름" 결과가 다수 페이퍼에서 재현 `[논문]`. <https://www.jpab.org/>, <https://www.researchgate.net/publication/313263645_PERFORMANCE_EVALUATION_OF_JPA_BASED_ORM_TECHNIQUES>

### 3.5 ORM Battle 2025 (Hibernate vs jOOQ vs JDBC) `[웹]`

- 단순 read: JDBC > jOOQ > Hibernate(엔티티). 차이는 종종 10~30%.
- 매핑/dirty checking이 필요한 write: Hibernate가 jOOQ + 수동 dirty 추적과 거의 비등.
- 의미: **read는 jOOQ/Native, write는 Hibernate** 조합이 합리적. <https://medium.com/javarevisited/the-great-orm-debate-hibernate-vs-jooq-vs-plain-jdbc-e271b95a2ef5>

### 3.6 학술 — Snapshot Isolation MVCC `[논문]`

- HyPer 그룹의 *"Fast Serializable Multi-Version Concurrency Control"* — MVCC 비용을 거의 0에 가깝게 줄이는 in-memory 구현. PostgreSQL/Oracle/SQL Server의 snapshot isolation이 이론적 baseline. ORM 레벨에서는 PersistenceContext가 *application-level snapshot*을 흉내내며, application과 DB 두 레이어에서 read consistency가 보장된다는 점을 인식해야 한다. <https://db.in.tum.de/~muehlbau/papers/mvcc.pdf>

---

## 4. 논쟁점 / 상충 관점

### 4.1 OSIV: 찬반

- **Vlad·Spring Boot 가이드(반)** `[웹]`: 안티패턴, 무조건 `open-in-view=false`. <https://vladmihalcea.com/the-open-session-in-view-anti-pattern/>
- **레거시 옹호(찬)** `[커뮤니티]`: 표현 계층까지 lazy navigation을 허용해야 DTO 매핑 보일러플레이트를 줄일 수 있다는 입장. 작은 팀·CRUD 위주 사내 도구에선 실용주의로 받아들이기도 함 — Stack Overflow 다수 답변, Spring 1.x 시절 표준이었음.
- **타협안**: 컨트롤러까지 트랜잭션을 끌고 가지 않되, **DTO ProjectionFactory + EntityGraph**로 보일러플레이트를 줄임.

### 4.2 낙관 vs 비관 락

- **Vlad(낙관 우선)** `[웹]`: 다중 HTTP 요청 동시성에는 낙관락만이 답. `@Version` + retry.
- **반대 의견(비관 우선)** `[커뮤니티]`: 결제·재고처럼 충돌 자체가 비싼 워크플로에선 비관락이 코드를 단순화하고 retry storm을 막는다. PostgreSQL의 `SELECT ... FOR UPDATE SKIP LOCKED`는 job queue 구현의 사실상 표준.
- **합의 지점**: 동일 트랜잭션 안의 짧은 critical section은 비관, 사용자 think-time을 거치는 multi-request flow는 낙관.

### 4.3 JPA(Hibernate) vs jOOQ vs MyBatis

- **Vlad(JPA + jOOQ)** `[웹]`: write/엔티티 라이프사이클은 JPA, read/복잡 쿼리는 jOOQ.
- **MyBatis 진영**: ORM의 추상화 비용을 거부, SQL을 일급으로 다룬다. 한국 SI에서 여전히 강세.
- **현실적 권고**: 모놀리식 + 도메인 모델 풍부 → JPA. 데이터 가공·분석 위주 → jOOQ. 거대 레거시 + SQL 표준화 → MyBatis.

### 4.4 2차 캐시 — 켜야 하나?

- **Vlad(조건부 찬)** `[책]` 16장: DB buffer pool 튜닝과 replica로 안 풀릴 때만. 그렇지 않으면 *분산 캐시 무효화의 어려움*이 이득을 잠식.
- **대규모 SaaS 반(예: Netflix, Uber 사례)**: 어차피 외부 Redis/Memcached로 application-level cache를 만들 거면 Hibernate 2차 캐시는 중간 추상화 비용만 추가. 직접 캐시 aside 패턴이 낫다.

### 4.5 EAGER 절대 금지인가?

- **Vlad** `[웹]`: 거의 항상 코드 스멜. <https://vladmihalcea.com/eager-fetching-is-a-code-smell/>
- **예외 옹호**: 1:1 immutable 같은 *항상 함께 다니는* 도메인 객체에는 LAZY proxy의 비용이 더 크다는 주장. Hibernate 6의 LazyAttribute로 흡수 가능해 점차 약해지는 입장.

### 4.6 IDENTITY 사용에 대한 강도

- **Vlad** `[웹]`: SEQUENCE만이 정답.
- **MySQL/MariaDB 진영**: SEQUENCE가 없거나 부족 → IDENTITY는 필수, 다만 batch가 필요하면 수동 ID 또는 Stateless session 우회.

### 4.7 Spring Data Specification vs Blaze-Persistence vs jOOQ (동적 쿼리)

- **Spring Data Specification (찬)** `[웹]`: 표준 Criteria API의 wrapping, Spring 친화. 단점: 복잡해지면 가독성 떨어지고 type-safe라기엔 약함.
- **Blaze-Persistence (Vlad 선호)** `[웹]`: LATERAL JOIN, CTE, window function까지. 진입 장벽 있음.
- **jOOQ** `[웹]`: 가장 강력한 type-safe SQL builder. DSL 학습 곡선, codegen 필요.

---

## 5. 실무 적용 팁 (Vlad 14 tips + 실전 확장)

1. **SQL을 항상 본다.** datasource-proxy 또는 `org.hibernate.SQL` + `orm.jdbc.bind` 로깅. 테스트 단계부터.
2. **커넥션 풀은 작게 시작한다.** Cores×2 근방에서 출발, FlexyPool/메트릭으로 조정.
3. **JDBC batch 4종 세트는 default로 켜둔다.** `batch_size=25`, `order_inserts=true`, `order_updates=true`, `batch_versioned_data=true`.
4. **PreparedStatement 캐시.** PostgreSQL `preparedStatementCacheQueries`, MySQL `cachePrepStmts=true, prepStmtCacheSize=500`.
5. **Identifier는 SEQUENCE + pooled-lo.** MySQL이면 수동 ID 또는 Stateless.
6. **컬럼 타입을 인색하게.** `BIGINT`보다 `INT`, varchar 길이 제한 명확히. 인덱스/캐시 효율 직결.
7. **관계는 `@OneToMany` 단방향 금지, `@ManyToMany List` 금지.** 양방향 또는 join entity.
8. **상속은 SINGLE_TABLE을 디폴트로.** 무결성 필요시 JOINED.
9. **PersistenceContext는 작게.** 배치는 25개마다 `flush()`+`clear()`, 또는 StatelessSession.
10. **DTO projection을 적극 사용.** "수정 안 할 read는 모두 DTO" — 엔티티 fetch는 modification 의도가 있을 때만.
11. **2차 캐시는 정당한 이유 있을 때만.** 켜기 전에 DB·replica·application cache를 먼저.
12. **트랜잭션 isolation은 의식적으로.** Read Committed에서도 lost update가 일어남 — `@Version` 또는 명시적 isolation.
13. **DB 능력을 활용.** window function, CTE, MERGE — JPA가 가린다고 못 쓰는 게 아니다. Hibernate 6 JPQL, Blaze, jOOQ.
14. **수평/수직 스케일.** 리드 레플리카 라우팅(`AbstractRoutingDataSource`), shard. application-level에서 받아들일 준비.
15. **(보강) Hypersistence Optimizer로 정적 검사.** 매핑 안티패턴 자동 검출.
16. **(보강) N+1 자동 회귀 테스트.** `SQLStatementCountValidator.assertSelectCount(1)`.
17. **(보강) `spring.jpa.open-in-view=false`로 시작.** 새 프로젝트 첫 줄.
18. **(보강) `readOnly=true`는 디폴트, write 메서드만 오버라이드.** 라우팅과 메모리 둘 다 잡힌다.

출처: <https://vladmihalcea.com/14-high-performance-java-persistence-tips/>, <https://vladmihalcea.com/hibernate-performance-tuning-tips/>

---

## 6. 참고문헌

### 6.1 Vlad Mihalcea 블로그 — 시그니처 글 (주제별)

#### N+1 / Fetching
- ["N+1 query problem with JPA and Hibernate"](https://vladmihalcea.com/n-plus-1-query-problem/) — N+1의 정의, 발생 케이스, 해결책 카탈로그.
- ["How to detect the Hibernate N+1 query problem during testing"](https://vladmihalcea.com/how-to-detect-the-n-plus-one-query-problem-during-testing/) — 테스트 단계 자동 검증.
- ["A beginner's guide to Hibernate fetching strategies"](https://vladmihalcea.com/hibernate-facts-the-importance-of-fetch-strategy/) — fetch 전략 개론.
- ["JPA and Hibernate FetchType EAGER is a code smell"](https://vladmihalcea.com/eager-fetching-is-a-code-smell/) — EAGER 사용 금지 논거.
- ["JPA Default Fetch Plan"](https://vladmihalcea.com/jpa-default-fetch-plan/) — 기본 fetch plan 동작.
- ["JPA Entity Graph"](https://vladmihalcea.com/jpa-entity-graph/) — EntityGraph 선언적·동적.
- ["Overriding FetchType.EAGER with fetchgraph"](https://vladmihalcea.com/fetchtype-eager-fetchgraph/) — fetchgraph로 EAGER 우회.
- ["The best way to use JOIN FETCH and Pagination with Spring"](https://vladmihalcea.com/join-fetch-pagination-spring/) — 2-query 패턴.
- ["Fix the HHH000104 warning"](https://vladmihalcea.com/fix-hibernate-hhh000104-entity-fetch-pagination-warning-message/) — 컬렉션 fetch + 페이지네이션 문제.

#### Connection Pool / FlexyPool
- ["The best way to determine the optimal connection pool size"](https://vladmihalcea.com/optimal-connection-pool-size/) — USL/Little's Law + 실측.
- ["Professional connection pool sizing with FlexyPool"](https://vladmihalcea.com/connection-pool-sizing-with-flexy-pool/) — FlexyPool로 자동 발견.
- [FlexyPool GitHub](https://github.com/vladmihalcea/flexy-pool) — 라이브러리 본체.
- ["FlexyPool, reactive connection pooling"](https://vladmihalcea.com/flexy-pool-reactive-connection-pooling/) — 리액티브 환경.

#### Identifier / Batch
- ["IDENTITY, SEQUENCE, TABLE generators"](https://vladmihalcea.com/hibernate-identity-sequence-and-table-sequence-generator/) — 3가지 비교.
- ["How to generate identifier using a database sequence"](https://vladmihalcea.com/jpa-entity-identifier-sequence/) — SEQUENCE 활용.
- ["Hibernate Batch Sequence Generator"](https://vladmihalcea.com/hibernate-batch-sequence-generator/) — sequence를 배치로 호출.
- ["How to batch INSERT and UPDATE statements with Hibernate"](https://vladmihalcea.com/how-to-batch-insert-and-update-statements-with-hibernate/) — batch 설정.
- ["How to batch INSERT statements with MySQL and Hibernate"](https://vladmihalcea.com/batch-insert-mysql-hibernate/) — MySQL 우회.
- ["The best way to do batch processing with JPA and Hibernate"](https://vladmihalcea.com/the-best-way-to-do-batch-processing-with-jpa-and-hibernate/) — 정식 배치 패턴.

#### Dirty Checking
- ["The anatomy of Hibernate dirty checking mechanism"](https://vladmihalcea.com/the-anatomy-of-hibernate-dirty-checking/) — 기본 메커니즘.
- ["How to enable bytecode enhancement dirty checking"](https://vladmihalcea.com/how-to-enable-bytecode-enhancement-dirty-checking-in-hibernate/) — bytecode 강화.
- ["Maven and Gradle Hibernate Enhance Plugin"](https://vladmihalcea.com/maven-gradle-hibernate-enhance-plugin/) — 빌드 통합.

#### Caching
- ["The JPA and Hibernate second-level cache"](https://vladmihalcea.com/jpa-hibernate-second-level-cache/) — 2차 캐시 개론.
- ["How does Hibernate READ_WRITE CacheConcurrencyStrategy work"](https://vladmihalcea.com/how-does-hibernate-read_write-cacheconcurrencystrategy-work/)
- ["How does Hibernate NONSTRICT_READ_WRITE CacheConcurrencyStrategy work"](https://vladmihalcea.com/how-does-hibernate-nonstrict_read_write-cacheconcurrencystrategy-work/)
- ["How does Hibernate TRANSACTIONAL CacheConcurrencyStrategy work"](https://vladmihalcea.com/how-does-hibernate-transactional-cacheconcurrencystrategy-work/)
- ["How does Hibernate Query Cache work"](https://vladmihalcea.com/how-does-hibernate-query-cache-work/) — 쿼리 캐시.
- ["How does Hibernate Collection Cache work"](https://vladmihalcea.com/how-does-hibernate-collection-cache-work/) — 컬렉션 캐시.
- ["How does Hibernate store second-level cache entries"](https://vladmihalcea.com/how-does-hibernate-store-second-level-cache-entries/) — 내부 표현.
- ["A beginner's guide to the Hibernate JPQL and Native Query Plan Cache"](https://vladmihalcea.com/hibernate-query-plan-cache/) — plan cache 튜닝.

#### Statement Caching
- ["PostgreSQL JDBC Statement Caching"](https://vladmihalcea.com/postgresql-jdbc-statement-caching/)
- ["MySQL JDBC Statement Caching"](https://vladmihalcea.com/mysql-jdbc-statement-caching/)
- ["How does the MySQL JDBC driver handle prepared statements"](https://vladmihalcea.com/how-does-the-mysql-jdbc-driver-handle-prepared-statements/)
- ["PostgreSQL plan_cache_mode"](https://vladmihalcea.com/postgresql-plan-cache-mode/)

#### Locking / Isolation / MVCC
- ["Optimistic vs. Pessimistic Locking"](https://vladmihalcea.com/optimistic-vs-pessimistic-locking/)
- ["A beginner's guide to Java Persistence locking"](https://vladmihalcea.com/a-beginners-guide-to-java-persistence-locking/)
- ["How does LockModeType.PESSIMISTIC_FORCE_INCREMENT work"](https://vladmihalcea.com/hibernate-locking-patterns-how-does-pessimistic_force_increment-lock-mode-work/)
- ["OPTIMISTIC_FORCE_INCREMENT with JPA and Hibernate"](https://vladmihalcea.com/hibernate-locking-patterns-how-does-optimistic_force_increment-lock-mode-work/)
- ["How to fix optimistic locking race conditions with pessimistic locking"](https://vladmihalcea.com/how-to-fix-optimistic-locking-race-conditions-with-pessimistic-locking/)
- ["A beginner's guide to Non-Repeatable Read anomaly"](https://vladmihalcea.com/non-repeatable-read/)
- ["A beginner's guide to Phantom Read anomaly"](https://vladmihalcea.com/phantom-read/)
- ["A beginner's guide to Read and Write Skew phenomena"](https://vladmihalcea.com/a-beginners-guide-to-read-and-write-skew-phenomena/)
- ["A beginner's guide to the Write Skew anomaly (2PL vs MVCC)"](https://vladmihalcea.com/write-skew-2pl-mvcc/)
- ["A beginner's guide to database locking and the lost update phenomena"](https://vladmihalcea.com/a-beginners-guide-to-database-locking-and-the-lost-update-phenomena/)
- ["A beginner's guide to Serializability"](https://vladmihalcea.com/serializability/)
- ["How does MVCC (Multi-Version Concurrency Control) work"](https://vladmihalcea.com/how-does-mvcc-multi-version-concurrency-control-work/)

#### Transaction / Spring
- ["The best way to use the Spring Transactional annotation"](https://vladmihalcea.com/spring-transactional-annotation/)
- ["Spring Transaction Best Practices"](https://vladmihalcea.com/spring-transaction-best-practices/)
- ["Spring read-only transaction Hibernate optimization"](https://vladmihalcea.com/spring-read-only-transaction-hibernate-optimization/)
- ["Spring Transaction and Connection Management"](https://vladmihalcea.com/spring-transaction-connection-management/)
- ["Read-write and read-only transaction routing with Spring"](https://vladmihalcea.com/read-write-read-only-transaction-routing-spring/)
- ["The Open Session In View Anti-Pattern"](https://vladmihalcea.com/the-open-session-in-view-anti-pattern/)
- ["The best way to handle the LazyInitializationException"](https://vladmihalcea.com/the-best-way-to-handle-the-lazyinitializationexception/)
- ["The hibernate.enable_lazy_load_no_trans Anti-Pattern"](https://vladmihalcea.com/the-hibernate-enable_lazy_load_no_trans-anti-pattern/)

#### Pagination
- ["Query pagination with JPA and Hibernate"](https://vladmihalcea.com/query-pagination-jpa-hibernate/)
- ["Keyset Pagination with JPA and Hibernate"](https://vladmihalcea.com/keyset-pagination-jpa-hibernate/)
- ["Keyset Pagination with Spring"](https://vladmihalcea.com/keyset-pagination-spring/)
- ["Keyset Pagination with Spring Data WindowIterator"](https://vladmihalcea.com/spring-data-windowiterator/)
- ["SQL Seek Method or Keyset Pagination"](https://vladmihalcea.com/sql-seek-keyset-pagination/)

#### Projection
- ["The best way to map a projection query to a DTO"](https://vladmihalcea.com/the-best-way-to-map-a-projection-query-to-a-dto-with-jpa-and-hibernate/)
- ["The best way to fetch a Spring Data JPA DTO Projection"](https://vladmihalcea.com/spring-jpa-dto-projection/)
- ["How to fetch a one-to-many DTO projection"](https://vladmihalcea.com/one-to-many-dto-projection-hibernate/)
- ["The best way to use a Hibernate ResultTransformer"](https://vladmihalcea.com/hibernate-resulttransformer/)
- ["The best way to use the Hibernate TupleTransformer"](https://vladmihalcea.com/hibernate-tupletransformer/)
- ["The best way to use Java Records with JPA and Hibernate"](https://vladmihalcea.com/java-records-jpa-hibernate/)
- ["Mapping Java Records to JSON columns using Hibernate"](https://vladmihalcea.com/java-records-json-hibernate/)

#### Inheritance / Mapping
- ["The best way to use entity inheritance"](https://vladmihalcea.com/the-best-way-to-use-entity-inheritance-with-jpa-and-hibernate/)
- ["The best way to map the SINGLE_TABLE inheritance"](https://vladmihalcea.com/the-best-way-to-map-the-single_table-inheritance-with-jpa-and-hibernate/)
- ["@MappedSuperclass with JPA and Hibernate"](https://vladmihalcea.com/how-to-inherit-properties-from-a-base-class-entity-using-mappedsuperclass-with-jpa-and-hibernate/)
- ["The best way to implement equals, hashCode, and toString"](https://vladmihalcea.com/the-best-way-to-implement-equals-hashcode-and-tostring-with-jpa-and-hibernate/)
- ["How to implement equals and hashCode using the entity identifier"](https://vladmihalcea.com/how-to-implement-equals-and-hashcode-using-the-jpa-entity-identifier/)
- ["The best way to map a @OneToMany relationship"](https://vladmihalcea.com/the-best-way-to-map-a-onetomany-association-with-jpa-and-hibernate/)
- ["Best way to map the @ManyToMany relationship"](https://vladmihalcea.com/the-best-way-to-use-the-manytomany-annotation-with-jpa-and-hibernate/)
- ["Avoid using Set for bidirectional JPA OneToMany collections"](https://vladmihalcea.com/set-bidirectional-onetomany/)
- ["How to synchronize bidirectional entity associations"](https://vladmihalcea.com/jpa-hibernate-synchronize-bidirectional-entity-associations/)

#### Bulk / Native
- ["Bulk Update and Delete with JPA and Hibernate"](https://vladmihalcea.com/bulk-update-delete-jpa-hibernate/)
- ["JPA Criteria API Bulk Update and Delete"](https://vladmihalcea.com/jpa-criteria-api-bulk-update-delete/)
- ["JPA Bulk Update and Delete with Blaze Persistence"](https://vladmihalcea.com/bulk-update-delete-blaze-persistence/)
- ["Blaze Persistence — JPA Criteria Queries"](https://vladmihalcea.com/blaze-persistence-jpa-criteria-queries/)
- ["Fetching multiple JPA collections with Blaze Persistence MULTISET"](https://vladmihalcea.com/blaze-persistence-multiset/)
- ["JOOQ Facts: From JPA Annotations to JOOQ Table Mappings"](https://vladmihalcea.com/jooq-facts-from-jpa-annotations-to-jooq-table-mappings/)
- ["Hibernate and JPQL Window Functions"](https://vladmihalcea.com/hibernate-jpql-window-functions/)

#### Audit / Soft Delete / Multi-Tenancy
- ["The best way to implement an audit log using Hibernate Envers"](https://vladmihalcea.com/the-best-way-to-implement-an-audit-log-using-hibernate-envers/)
- ["The best way to soft delete with Hibernate"](https://vladmihalcea.com/the-best-way-to-soft-delete-with-hibernate/)
- ["Hibernate SoftDelete annotation"](https://vladmihalcea.com/hibernate-softdelete-annotation/)
- ["A beginner's guide to database multitenancy"](https://vladmihalcea.com/database-multitenancy/)
- ["Hibernate database schema multitenancy"](https://vladmihalcea.com/hibernate-database-schema-multitenancy/)
- ["Hibernate database catalog multitenancy"](https://vladmihalcea.com/hibernate-database-catalog-multitenancy/)

#### Hibernate 6 신기능
- ["How to map JSON objects using generic Hibernate Types"](https://vladmihalcea.com/how-to-map-json-objects-using-generic-hibernate-types/)
- ["How to map a JSON collection using JPA and Hibernate"](https://vladmihalcea.com/how-to-map-json-collections-using-jpa-and-hibernate/)
- ["How to map polymorphic JSON objects"](https://vladmihalcea.com/polymorphic-json-objects-hibernate/)
- ["How to map Java and SQL arrays"](https://vladmihalcea.com/how-to-map-java-and-sql-arrays-with-jpa-and-hibernate/)
- ["Hibernate StatelessSession JDBC Batching"](https://vladmihalcea.com/hibernate-statelesssession-jdbc-batching/)
- ["Hibernate StatelessSession Upsert"](https://vladmihalcea.com/hibernate-statelesssession-upsert/)
- ["20 years of Hibernate"](https://vladmihalcea.com/20-years-of-hibernate/) — Hibernate 회고 & 6 정리.

#### 모니터링 / Tooling
- ["The best way to log SQL statements with JDBC, JPA or Hibernate"](https://vladmihalcea.com/the-best-way-to-log-jdbc-statements/)
- ["The best way to log SQL statements with Spring Boot"](https://vladmihalcea.com/log-sql-spring-boot/)
- ["How to monitor a Java EE DataSource"](https://vladmihalcea.com/how-to-monitor-a-java-ee-datasource/)
- ["How to intercept and modify SQL queries with the Hibernate StatementInspector"](https://vladmihalcea.com/hibernate-statementinspector/)
- [Hypersistence Utils GitHub](https://github.com/vladmihalcea/hypersistence-utils) — 통합 유틸 (Hibernate Types 후신).
- ["Hypersistence Optimizer"](https://vladmihalcea.com/hypersistence-optimizer/) — 매핑 정적 분석.

#### 종합 / 가이드
- ["14 High-Performance Java Persistence Tips"](https://vladmihalcea.com/14-high-performance-java-persistence-tips/) — 정수 14.
- ["Hibernate performance tuning tips"](https://vladmihalcea.com/hibernate-performance-tuning-tips/) — 광범위 체크리스트.
- ["Why and when you should use JPA"](https://vladmihalcea.com/why-and-when-use-jpa/) — JPA 사용 정당성.
- ["The best way to use the Spring Data JPA Specification"](https://vladmihalcea.com/spring-data-jpa-specification/) — 동적 query.

### 6.2 책 / 영상

- Vlad Mihalcea, *High-Performance Java Persistence* (Leanpub / Amazon, 2016–현재 개정 중). 1부 JDBC·트랜잭션 기초, 2부 JPA/Hibernate, 3부 jOOQ. <https://leanpub.com/high-performance-java-persistence>, <https://vladmihalcea.com/books/high-performance-java-persistence/>
- High-Performance Java Persistence GitHub 코드 예제 — <https://github.com/vladmihalcea/high-performance-java-persistence>
- *Transactions and Concurrency Control Patterns* (SlideShare, Devoxx 발표 자료) — <https://www.slideshare.net/VladMihalcea/transactions-and-concurrency-control-patterns>

### 6.3 공식 문서

- [Hibernate ORM 6.x User Guide](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html) — 6.x 공식 가이드.
- [Hibernate Performance Tuning (Hibernate 6 ref)](https://docs.jboss.org/hibernate/orm/6.0/userguide/html_single/Hibernate_User_Guide.html#performance) — 공식 성능 챕터.
- [Spring Data JPA Reference](https://docs.spring.io/spring-data/jpa/reference/index.html) — Repository, EntityGraph, Specification, Projection.
- [Spring Framework Transaction Management](https://docs.spring.io/spring-framework/reference/data-access/transaction.html) — `@Transactional` 정식 문서.

### 6.4 커뮤니티 / 한국어 자료

- [velog `@joonghyun` - JPA Batch Size에 대한 고찰](https://velog.io/@joonghyun/SpringBoot-JPA-JPA-Batch-Size%EC%97%90-%EB%8C%80%ED%95%9C-%EA%B3%A0%EC%B0%B0)
- [velog `@imcool2551` - JPA 성능 최적화](https://velog.io/@imcool2551/JPA-%EC%84%B1%EB%8A%A5-%EC%B5%9C%EC%A0%81%ED%99%94)
- [velog `@hyojhand` - ToMany 관계 컬렉션 성능 최적화 (N+1, fetch join, batch size)](https://velog.io/@hyojhand/JPA-%EC%BB%AC%EB%A0%89%EC%85%98-%EC%A1%B0%ED%9A%8C-%EC%B5%9C%EC%A0%81%ED%99%94-N1-fetch-join-batch-size)
- [velog `@sdsd0908` - 1:N Fetch Join 페이징 문제와 Batch Size 주의사항](https://velog.io/@sdsd0908/Spring-JPA-1N-Fetch-Join-%ED%8E%98%EC%9D%B4%EC%A7%95-%EB%AC%B8%EC%A0%9C%EC%99%80-Batch-Size-%EC%84%A4%EC%A0%95-%EC%8B%9C-%EC%A3%BC%EC%9D%98%EC%82%AC%ED%95%AD)
- [velog `@gwanghyeonkim` - Paging과 Fetch Join을 같이 쓰면 안 되는 이유](https://velog.io/@gwanghyeonkim/JPA%EC%97%90%EC%84%9C-Paging%EA%B3%BC-Fetch-Join%EC%9D%84-%EA%B0%99%EC%9D%B4-%EC%82%AC%EC%9A%A9%ED%95%98%EB%A9%B4-%EC%95%88-%EB%90%98%EB%8A%94-%EC%9D%B4%EC%9C%A0)
- [velog `@simgyuhwan` - Hibernate 성능 튜닝 Tips](https://velog.io/@simgyuhwan/Hibernate-%EC%84%B1%EB%8A%A5-%ED%8A%9C%EB%8B%9D-Tips)
- [velog `@lord` - JPA N+1 해결 및 성능 비교](https://velog.io/@lord/JPA-N1-%EB%AC%B8%EC%A0%9C-%ED%95%B4%EA%B2%B0-%EB%B0%8F-%EC%84%B1%EB%8A%A5-%EB%B9%84%EA%B5%90%ED%95%98%EA%B8%B0)
- [velog `@hand_ddong` - Spring Data JPA 성능 최적화 및 대용량 데이터 처리 전략](https://velog.io/@hand_ddong/Spring-%EB%B0%B1%EC%97%94%EB%93%9C-%ED%8A%B8%EB%9E%99-Spring-Data-JPA-%EC%84%B1%EB%8A%A5-%EC%B5%9C%EC%A0%81%ED%99%94-%EB%B0%8F-%EB%8C%80%EC%9A%A9%EB%9F%89-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%B2%98%EB%A6%AC-%EC%A0%84%EB%9E%B5)
- [Junhyunny - JPA Fetch 조인과 페이징 처리](https://junhyunny.github.io/spring-boot/jpa/jpa-fetch-join-paging-problem/)
- [Yun Blog - JPA Fetch Join 적용시 limit 동작하지 않는 이슈](https://cheese10yun.github.io/jpa-fetch-paging/)
- [joont92 - JPA 성능 최적화](https://joont92.github.io/jpa/JPA-%EC%84%B1%EB%8A%A5-%EC%B5%9C%EC%A0%81%ED%99%94/)
- [42Class - JPA N+1 튜닝 과정에서 batch size와 다르게 쿼리 분할되는 이유](https://42class.com/dev/jpa-batchsize/)
- [권남 위키 - Hibernate Performance Tuning](https://kwonnam.pe.kr/wiki/java/hibernate/performance)
- [Baeldung - Hibernate N+1 Problem](https://www.baeldung.com/spring-hibernate-n1-problem)
- [Baeldung - Guide to FlexyPool](https://www.baeldung.com/spring-flexypool-guide)
- [Baeldung - Spring Data JPA @Modifying Annotation](https://www.baeldung.com/spring-data-jpa-modifying-annotation)
- [Baeldung - Hibernate Second-Level Cache](https://www.baeldung.com/hibernate-second-level-cache)
- [Baeldung - Hibernate Query Plan Cache](https://www.baeldung.com/hibernate-query-plan-cache)
- [Thorben Janssen - Hibernate Performance Tuning (2025)](https://thorben-janssen.com/hibernate-performance-tuning/)
- [Thorben Janssen - LazyInitializationException](https://thorben-janssen.com/lazyinitializationexception/)
- [JPA Buddy - Hibernate 6 What's New](https://jpa-buddy.com/blog/hibernate6-whats-new-and-why-its-important/)
- [JPA Buddy - Equals and HashCode for JPA Entities](https://jpa-buddy.com/blog/hopefully-the-final-article-about-equals-and-hashcode-for-jpa-entities-with-db-generated-ids/)
- [ORM Battle 2025: Hibernate vs jOOQ vs JDBC](https://medium.com/javarevisited/the-great-orm-debate-hibernate-vs-jooq-vs-plain-jdbc-e271b95a2ef5)
- [Martinelli - Hidden Performance Killer: OSIV in Spring Boot](https://martinelli.ch/the-hidden-performance-killer-understanding-open-session-in-view-in-spring-boot/)
- [codesoapbox - Disable OSIV best practice](https://codesoapbox.dev/spring-boot-best-practice-disable-osiv-to-start-receiving-lazyinitializationexception-warnings-again/)
- [Vlad Mihalcea Stack Overflow profile](https://stackoverflow.com/users/1025118/vlad-mihalcea) — JPA/Hibernate 5,000+ 답변, 누적 reputation 1M+.

### 6.5 논문 / 학술

- T. Neumann, T. Mühlbauer, A. Kemper, *"Fast Serializable Multi-Version Concurrency Control for Main-Memory Database Systems"*, SIGMOD 2015. <https://db.in.tum.de/~muehlbau/papers/mvcc.pdf>
- Y. Tanabe et al., *"An Analysis of Concurrency Control Protocols for In-Memory Databases"*, PVLDB 2020. <https://vldb.org/pvldb/vol13/p3531-tanabe.pdf>
- A. Alhomssi et al., *"Scalable and Robust Snapshot Isolation for High-Performance Storage Engines"*, PVLDB 2023. <https://www.vldb.org/pvldb/vol16/p1426-alhomssi.pdf>
- Neil J. Gunther, *"Quantifying Scalability — The Universal Scalability Law (USL)"*, Performance Dynamics. <https://www.perfdynamics.com/Manifesto/USLscalability.pdf>
- *"Performance Evaluation of JPA Based ORM Techniques"*, ResearchGate. <https://www.researchgate.net/publication/313263645_PERFORMANCE_EVALUATION_OF_JPA_BASED_ORM_TECHNIQUES>
- *"Review on ORM based JPA implementations"*, ResearchGate. <https://www.researchgate.net/publication/313263324_Review_on_ORM_based_JPA_implementations>
- *"Performance Analysis and Improvement for CRUD Operations in Relational Databases from Java Programs Using JPA, Hibernate, Spring Data JPA"*, Preprints.org 2024. <https://www.preprints.org/manuscript/202401.1182>
- *"The analysis of Java ORM frameworks performance in terms of analytical data processing"*, Journal of Computer Sciences Institute. <https://ph.pollub.pl/index.php/jcsi/article/view/3632>
- JPAB (Java Persistence API Performance Benchmark) — 종합 ORM 벤치마크. <https://www.jpab.org/>

---

## 7. 리서치 한계

본 레퍼런스는 다음 영역에서 보강이 필요하다.

1. **Vlad의 YouTube/컨퍼런스 라이브 강연 트랜스크립트** — Devoxx, JavaZone, Voxxed Days, Spring I/O 등에서 발표한 슬라이드는 일부 SlideShare로 확인되나, 영상 본문 핵심 인용은 본 리서치 단계에서 수집하지 못했다. *Transactions and Concurrency Control Patterns* 슬라이드만 확보.
2. **Spring Data JPA 3.x / Hibernate 7 최신 (2025–2026 시점)** — Jakarta Data, 새 Scrollable 인터페이스, Hibernate 7의 instance creation/embeddable 변화 등은 변화 속도가 빠르므로 책 집필 단계에서 공식 release note를 추가 확인할 것.
3. **Reddit r/java·HackerNews 토론 직접 인용** — 한국 커뮤니티(velog/OKKY/Junhyunny/cheese10yun)와 영문 블로그(Baeldung, Thorben Janssen)는 풍부히 모았으나, 영어권 SNS 토론 원문 thread는 표본이 적다. 책 단계에서 *"the great ORM debate"* 식 인기 토론을 보강하면 좋다.
4. **Database 벤더 specific deep tuning** — Oracle AWR/ASH 분석, MySQL Performance Schema, PostgreSQL pg_stat_statements 같은 *DB-side* 도구 결합은 본 문서가 충분히 다루지 못했다. Vlad는 *ORM 위에서의 튜닝*에 집중하므로, DB 자체 튜닝은 별도 자료(Use The Index, Luke! / Markus Winand)와 병합 필요.
5. **재현 가능한 벤치마크 셋업 코드** — 본 문서는 Vlad의 발표 수치를 인용했으나, 책 집필 단계에서 JMH 기반 자체 마이크로벤치마크를 만들면 신뢰도가 더 올라간다. `vladmihalcea/high-performance-java-persistence` 리포지토리 코드가 좋은 출발점.
6. **Quarkus/Panache·Micronaut Data 등 비-Spring 환경** — JPA 기반이지만 트랜잭션/세션 라이프사이클이 다르다. 본 문서는 Spring Boot 중심.
7. **Reactive (R2DBC, Spring Data R2DBC, Hibernate Reactive)** — 의도적으로 본 레퍼런스 범위에서 제외했다. 대상 독자가 *JPA 실무자*이고 reactive는 별개 패러다임이기 때문이다. 책 후기에서 "다음 단계"로 안내할 수는 있다.
8. **Stack Overflow에서의 Vlad 답변 직접 인용** — Vlad는 SO에서 JPA/Hibernate 태그 답변 1위지만, 본 검색에선 그의 블로그 글로 우회 인용한 형태가 많다. 책 단계에서 결정적 답변 5~10개를 직접 인용 박스로 넣으면 깊이가 살아난다.

이 한계들은 책 저술 단계의 챕터별 리서치 보강 또는 부록으로 흡수할 수 있다.
