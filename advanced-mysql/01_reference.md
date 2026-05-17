# 자바 스프링 개발자를 위한 고급 MySQL DB 기술 종합 레퍼런스

> 이 문서는 책 *"자바 스프링 개발자를 위한 고급 MySQL DB 기술 종합서"*의 토대가 되는 리서치 산출물이다.
> 대상 독자는 기본 SQL을 다룰 수 있는 중급 스프링 개발자이며, 목표는 DBA에 준하는 MySQL 8.x 전문성 확보다.
> 출처는 (웹) (논문) (커뮤니티) 표기로 구분한다.

---

## 0. 책 한 권을 위한 핵심 토픽 지도

리서치를 통해 도출한 영역별 무게중심은 다음과 같다.

| 영역 | 책에서의 비중 | 강조점 |
|------|---------------|--------|
| InnoDB 내부(MVCC·redo/undo·버퍼풀·B+Tree) | 高 | 모든 튜닝/락 논의의 기반. 시각화·은유로 직관 확립 |
| 트랜잭션·격리수준·락 | 高 | RR vs RC 선택, gap/next-key lock 디버깅, 데드락 패턴 |
| 인덱스 설계와 EXPLAIN ANALYZE | 高 | 복합 인덱스 leftmost prefix, 커버링, histogram, optimizer_trace |
| 고급 SQL (윈도우 함수·CTE·JSON) | 中 | 한 챕터로 묶기 좋은 단단한 주제 |
| AWS 멀티 인스턴스·복제·파티셔닝·샤딩 | 高 | RDS vs Aurora 의사결정, GTID·반동기·MGR, PITR, 메이저 업그레이드 |
| JPA + Native SQL 혼용 | 高 | 스프링 개발자의 일상 — N+1·페이지네이션·배치·락 |
| 운영·관측·보안 | 中 | sys/performance_schema, 모니터링 지표, TLS·감사·RLS, 캐릭터셋·콜레이션 |

이 무게중심은 챕터 분량과도 직결된다.

---

## 1. 개념과 정의

### 1.1 InnoDB와 트랜잭션 엔진

- **WAL(Write-Ahead Logging)**: 데이터 페이지에 변경을 반영하기 전 redo log에 기록한다. (웹: MySQL Ref 17.6.5; 커뮤니티: tech.kakao "InnoDB Log 이해")
- **Redo log**: 크래시 복구용 물리 로그. 8.0.30부터 `innodb_redo_log_capacity`로 동적 리사이즈, 내부에서 32개 redo 파일로 분할. (웹: Mydbops; 공식 문서)
- **Undo log**: row의 이전 버전을 보관해 (a) 트랜잭션 롤백, (b) MVCC 스냅샷 재구성에 사용한다. 각 row에 6바이트 `DB_TRX_ID`와 7바이트 `DB_ROLL_PTR`이 따라붙는다. (웹: MySQL 17.3 Multi-Versioning)
- **Binlog**: 논리 로그, 복제·PITR의 원천. row/statement/mixed 포맷 중 row가 사실상 표준.
- **MVCC**: 트랜잭션이 read view를 잡는 시점에 보이는 row 버전만 인식한다. 비잠금 SELECT가 가능한 근거. (논문: Cahill 2009; 웹: MySQL 17.3)
- **버퍼풀(Buffer Pool)**: 디스크 페이지의 인메모리 캐시. 운영에서는 가용 RAM의 70~80%, 8GB↑면 `innodb_buffer_pool_instances`로 분할. (웹: Datacamp, Burnison)
- **Adaptive Hash Index(AHI)**: 자주 들어오는 단일 키 lookup을 B-Tree 트래버스 없이 해시로 직행. 단, 일부 쓰기 무거운 워크로드에서 락 경합을 늘려 8.4 LTS에서는 기본 OFF로 변경. (커뮤니티: tech.kakao AHI / Skeema "8.4 surprises")

### 1.2 격리수준·락 용어

- **READ COMMITTED(RC)**: 매 SELECT마다 새 스냅샷. gap lock 거의 없음 → 데드락 감소, 단 phantom read 허용.
- **REPEATABLE READ(RR)**: InnoDB 기본. 트랜잭션 시작 시 한 번 스냅샷 고정. next-key lock으로 phantom 차단. (웹: MySQL 17.7.2.1)
- **레코드 락(Record lock)**: 인덱스 레코드에 거는 락.
- **갭 락(Gap lock)**: 인덱스 레코드들 사이의 *gap*에 거는 락. 목적은 INSERT 차단이지, gap 진입 차단이 아님. gap lock끼리는 호환된다. (웹: Percona Gap Locks)
- **넥스트키 락(Next-key lock)**: 레코드 락 + 직전 gap 락. RR의 phantom 방지 메커니즘.
- **인텐션 락(Intention lock)**: 테이블 단위로 "이 안에 행 락이 있다"를 알리는 IS/IX 락.
- **데드락**: 두 트랜잭션이 서로의 락을 기다리는 순환 대기. InnoDB는 사이클을 감지해 한쪽을 롤백한다.
- **낙관적 락(Optimistic)**: 충돌이 드물다고 가정, `@Version` 컬럼 체크. 비잠금 읽기. (웹: Baeldung)
- **비관적 락(Pessimistic)**: 읽는 시점부터 잠금, `SELECT ... FOR UPDATE`로 발급. (웹: CodeWiz; 우아한형제들 분산락)

### 1.3 인덱스 종류

- **클러스터링 인덱스**: InnoDB는 PK가 곧 클러스터링 인덱스. 테이블 자체가 PK 기준 B+Tree.
- **세컨더리 인덱스**: 클러스터링 인덱스의 PK 값을 포인터로 가진다. SELECT 시 PK 룩업이 추가됨(=**back to table**).
- **커버링 인덱스(Covering index)**: 쿼리가 인덱스만으로 답을 낼 수 있는 경우. `EXPLAIN`의 Extra에 `Using index` 표시. (웹: DEV.to chat2db; 커뮤니티: velog 커버링 인덱스)
- **복합 인덱스(Composite)**: 컬럼 순서가 운명. **leftmost prefix rule** — `(A,B,C)`는 A / A,B / A,B,C에만 쓰임. 컬럼 순서 휴리스틱: equality → range, 고카디널리티 → 저카디널리티. (웹: DoHost, Red-Gate)
- **프리픽스 인덱스(Prefix index)**: VARCHAR/TEXT 앞 N바이트만 인덱싱. 카디널리티 손실 트레이드오프.
- **Functional index**: 8.0.13부터 표현식 인덱스(`CREATE INDEX ... ((LOWER(name)))`).
- **JSON functional index**: 8.0.21부터 `JSON_VALUE`로 가능. 그 이전엔 generated column + secondary index 패턴. (웹: Vlad Mihalcea "Index JSON columns")
- **Descending index**: 8.0부터 진짜 ASC/DESC 혼합 정렬을 인덱스로 처리. (커뮤니티: tech.kakao Ascending vs Descending)
- **Invisible index**: 옵티마이저가 무시하는 인덱스. 인덱스 제거 전 영향 테스트용 안전장치.

### 1.4 옵티마이저와 통계

- **Cost-based optimizer**: `mysql.server_cost`, `mysql.engine_cost` 테이블의 상수로 cost 계산. (웹: Alibaba Cost Estimator)
- **Statistics**: `information_schema.STATISTICS` + `ANALYZE TABLE`. 8.0의 **histogram statistics**는 비인덱스 컬럼 분포까지 추정(`ANALYZE TABLE ... UPDATE HISTOGRAM`). (웹: MySQL Histogram statistics 블로그)
- **EXPLAIN vs EXPLAIN ANALYZE**: 전자는 추정 plan, 후자는 8.0.18부터 실제 실행하며 actual time/rows 트리 출력. (웹: MySQL EXPLAIN ANALYZE)
- **optimizer_trace**: ON으로 켜면 고려된 plan과 cost를 JSON으로 덤프. 의사결정 근거 확인용.

### 1.5 복제·HA 용어

- **GTID(Global Transaction Identifier)**: `server_uuid:transaction_number` 형식. binlog 좌표 추적이 필요 없어 페일오버를 단순화. (웹: Percona replication overview)
- **Async replication**: 기본값. 데이터 손실 위험 있음.
- **Semi-sync replication**: 최소 1개 리플리카가 receive ACK한 뒤 커밋. TCP RTT만큼 지연. (웹: MySQL 19.4.10)
- **Group Replication(MGR)**: Paxos 기반 그룹 합의 복제. 최대 9 노드, InnoDB 전용, 모든 테이블에 PK 필수.
- **InnoDB Cluster**: MGR + MySQL Shell + MySQL Router의 묶음 솔루션.
- **Aurora 스토리지**: 3 AZ × 6-way 분산 스토리지에 redo만 전송. 리플리카 lag이 ms 수준. (웹: Mydbops; Bytebase)

### 1.6 파티셔닝과 샤딩

- **RANGE / LIST / HASH / KEY** 네 종류. RANGE+날짜가 가장 흔한 유즈 케이스. (웹: MySQL 26.1)
- **Partition pruning**: WHERE에 파티션 키가 들어와야 작동. 들어오지 않으면 모든 파티션 풀스캔.
- **Partitioning vs Sharding**: 파티셔닝은 단일 인스턴스 내부 분할(엔진이 라우팅). 샤딩은 여러 인스턴스에 분산(애플리케이션/미들웨어가 라우팅). (웹: Rapydo)

---

## 2. 핵심 관점들

### 2.1 격리수준 선택

- (웹/공식) MySQL InnoDB 기본은 RR. next-key lock으로 phantom 방지.
- (커뮤니티) Jepsen 분석은 8.0.34의 RR에서 여전히 fractured read·lost update가 발생함을 보였다. 금전 트랜잭션은 **READ COMMITTED + 명시적 비관적 락**이나 SERIALIZABLE로 가는 것이 안전하다는 견해. (커뮤니티: jepsen.io)
- (웹) PostgreSQL 진영은 RC 기본 + SERIALIZABLE 활용을 권고. MySQL 진영은 RR을 유지하되 명시적 락 사용을 추가하라는 입장. **상충 정보**.

### 2.2 RDS for MySQL vs Aurora MySQL

| 관점 A: Aurora 우선 | 관점 B: RDS 충분 |
|----------------------|--------------------|
| 읽기 트래픽 비대칭, ms 수준 lag 필요, 자동 페일오버·15 리플리카 필요 | 단순 워크로드, IO 가벼움, 비용 민감 |
| (웹: Mydbops, Bytebase 2025, Percona) | (웹: devrocks.de) |

분기점: (1) 읽기 확장, (2) 페일오버 RTO, (3) IO bound 여부, (4) 락-인 감수 가능 여부. (커뮤니티: 우아한형제들은 Aurora MySQL의 인덱스 DDL이 200GB 테이블에서 1시간+ 걸려 PostgreSQL 대비 약점을 지적)

### 2.3 JPA만 쓸까, native SQL을 적극 쓸까

- 관점 A: JPA로 도메인 + native/JdbcTemplate로 무거운 쿼리(하이브리드). Vlad Mihalcea, Thorben Janssen 등의 사실상 표준 권고.
- 관점 B: SQL-mapper(MyBatis) 단독 채택. 도메인 모델보다 SQL 자유도가 중요한 시스템.
- 관점 C: JdbcTemplate 단독. 데이터 액세스가 단순할 때.
- 합의된 휴리스틱: **CRUD/단일 aggregate 영속화 → JPA**, **N개 테이블 조인+집계 보고서 → JdbcTemplate/MyBatis**, **bulk update/delete → JdbcTemplate batchUpdate 또는 native + LIMIT 청크 분할**. (웹: Medium "JPA vs MyBatis", Vlad "Java data access survey")

### 2.4 락 전략: 낙관적 vs 비관적 vs 분산락

- (웹) 일반 룰: 충돌 빈도 낮음 → 낙관적, 충돌 잦음·재시도 비쌈 → 비관적.
- (커뮤니티) 우아한형제들은 단일 DB를 락 매개체로 쓰는 **named lock 분산락** 패턴을 운영. SELECT FOR UPDATE는 record에 락이 묶여 다른 로직과 충돌하지만, named lock은 record와 무관해 자유도가 높다. **락 획득용 커넥션 풀을 비즈니스 풀과 분리**가 핵심 패턴.
- 대안: Redis Redlock. 단순성/속도는 우위지만 일관성 측면에선 MySQL named lock이 더 보수적인 선택이라는 의견도 존재.

### 2.5 Soft Delete 찬반

- 관점 A: brandur.org, cultured.systems는 "거의 가치 없다" — 모든 쿼리/JOIN/unique/FK에 `deleted_at IS NULL`을 끼워야 하고 누락 시 정합성이 깨진다.
- 관점 B: Brent Ozar 등은 "감사·복원이 필요한 도메인에는 유효". 합의는 "조건부 적용 + partial unique index와 같은 도구가 있을 때". MySQL은 partial unique가 없어 함수 기반 unique index 또는 별도 이력 테이블로 대체. (웹: brandur.org, Brent Ozar, Cultured Systems)

### 2.6 8.0 → 8.4 LTS 업그레이드

- (웹/커뮤니티) Skeema가 정리한 "Five Surprises": **adaptive hash index 기본 OFF**, **change buffer 기본 OFF**, **FK가 부모의 정확히 일치하는 unique key 요구**, 인증 플러그인 변경 등. 이전 default에 의존한 워크로드는 회귀 가능. (커뮤니티: Skeema "Five Surprises")
- 권장 전략: pt-upgrade로 쿼리 호환성 사전 검증, AWS Blue/Green Deployment 또는 8.0 리플리카 승격 패턴, 다운그레이드는 **불가**이므로 5.7 리플리카를 일정 기간 유지하는 escape hatch. (웹: Percona, Severalnines)

---

## 3. 대표 사례

### 3.1 인덱스 한 줄 추가로 6초 → 0.02초

- (커뮤니티: velog "슬로우 쿼리 개선기") `promotion_option.promotion_id`에 인덱스가 없어 LEFT JOIN 풀스캔 → 인덱스 추가만으로 6초 → 0.02초. 후속 단계에서 옵티마이저가 JOIN 컬럼 인덱스를 우선 선택해 다른 인덱스를 무시하는 함정도 만남.
- 시사점: **인덱스 누락을 EXPLAIN으로 발견 → 추가 → 옵티마이저 선택까지 점검**이 1사이클.

### 3.2 OKKY 11초 → 0.1초

- (커뮤니티: OKKY 질의, velog "쿼리 속도 개선기") 단순 인덱스 추가가 아니라 **복합 인덱스의 컬럼 순서**가 핵심이었던 사례. 11초 → 0.1초로 단축.

### 3.3 우아한형제들 광고 시스템의 named lock 분산락

- (커뮤니티: 우아한형제들 기술블로그) `GET_LOCK("ad:campaign:42")` + 별도 커넥션 풀로 분산락 구현. Spring NamedJdbcTemplate, Supplier 콜백으로 lock acquire/release를 일관되게 처리. MySQL 5.7 미만에서는 중복 GET_LOCK 시 이전 락이 해제되는 트랩 주의.

### 3.4 JSON 인덱싱: 5.7초 → 280ms

- (웹: Medium "1mg JSON index", Vlad "Index JSON columns") VIRTUAL generated column + secondary index 추가로 JSON path 조회 속도 약 20배 개선. 8.0.21 이후는 functional index로 generated column 없이 동일 효과.

### 3.5 LINE의 performance_schema 영향 측정

- (커뮤니티: LINE Engineering) 전체 instrument를 ON 했을 때 TPS가 15% 떨어짐을 실측. "운영에선 필요한 instrument만 켜라"는 명제의 근거.

### 3.6 우아한형제들 배치 INSERT 100배 개선

- (커뮤니티: techblog.woowahan.com "하이버네이트 배치 설정") `jdbc.batch_size` + `order_inserts` + `rewriteBatchedStatements=true` 3종 세트가 다 켜져야 진짜 배치 INSERT가 일어남. IDENTITY ID 전략은 배치 불가 → SEQUENCE/TABLE로 전환.

### 3.7 카카오 MRTE: 운영 트래픽 미러링

- (커뮤니티: tech.kakao MRTE) 운영 트래픽을 새 환경에 미러링해 메이저 업그레이드/튜닝 영향을 미리 본다. 메이저 업그레이드 챕터에서 사례로 인용.

### 3.8 Aurora MySQL의 대용량 DDL 약점

- (커뮤니티: 우아한형제들 "Aurora MySQL vs PostgreSQL") 200GB 테이블 인덱스 생성에 1시간+ 소요. PostgreSQL의 partial index가 부분 인덱싱으로 약 40분에 끝났다는 비교. Aurora MySQL을 쓸 때 무중단 DDL은 `pt-online-schema-change`/`gh-ost`를 진지하게 고려해야 한다는 시사점.

### 3.9 토스의 다중 리전 DR

- (커뮤니티: SLASH 21 "MySQL HA & DR Topology") 토스는 GTID 기반 페일오버 + MHA/orchestrator로 다중 리전 DR을 설계. 24/7 금융 서비스에 RDS/Aurora 선택을 넘어 자체 운영 노하우가 필요함을 보여준다.

---

## 4. 논쟁점·상충 관점

| 주제 | 관점 A | 관점 B |
|------|--------|--------|
| 격리수준 기본값 | RR 유지 + 명시적 락 (MySQL 진영) | RC + SERIALIZABLE 활용 (PostgreSQL 진영, Jepsen 우려) |
| RDS vs Aurora | Aurora가 사실상 표준 (Mydbops, Percona) | 단순 워크로드는 RDS로 충분, Aurora는 락-인+IO 비용 (devrocks) |
| Soft Delete | 거의 항상 안티패턴 (brandur) | 도메인 요구가 명확하면 유효 (Brent Ozar) |
| 페이지네이션 | OFFSET 단순 일관 | 깊은 페이지에 keyset이 절대 우위 (Vlad, Thorben) |
| JPA + Pageable + JOIN FETCH 컬렉션 | 가능 | 메모리 페이징 경고, 안티패턴 — EntityGraph로 대체 |
| 분산락 매개체 | MySQL named lock (보수적, 일관성 우위) | Redis Redlock (단순, 빠름) |
| Partitioning | 단일 인스턴스 한계 안에서 강력 | FK 부재·UNIQUE 제약·표현식 제한 → 부담 |
| Group Replication | 페일오버 자동화 우수 | InnoDB 전용·9 노드 한계·peak throughput은 semi-sync보다 낮음 |
| 8.4 LTS 디폴트 변경 | 모범적 — 사용 안 되는 기능 꺼서 안정성 ↑ | 운영 워크로드 회귀 위험 — 명시적 ON으로 복구 필요 (Skeema) |
| ORM 선택 | JPA + native 하이브리드가 모범 | MyBatis/JdbcTemplate 단독으로도 충분 (SQL 중심 팀) |

각 논쟁은 책에서 결론을 강요하기보다 **선택 기준과 함정**을 제시하는 방향이 어울린다.

---

## 5. 실무 적용 팁

### 5.1 트랜잭션 설계

- 트랜잭션을 짧게. 외부 API 호출, 파일 IO를 트랜잭션 안에 두지 말 것.
- 데드락은 "버그"가 아니라 "신호" — 발생 자체보단 **재시도 가능한 트랜잭션 구조**가 중요. `@Retryable` + idempotent payload 패턴.
- 락 순서를 트랜잭션마다 **일관**되게. 정렬된 키 순서로 접근 → 데드락 사이클 차단.

### 5.2 인덱스 설계

- 컬럼 순서: equality → range → sort. 고카디널리티가 앞.
- 커버링 인덱스를 노릴 때는 SELECT 컬럼 목록까지 같이 설계.
- INSERT/UPDATE가 빈번한 테이블에서 인덱스가 너무 많으면 buffer pool/redo 쓰기 비용 증가. **3~5개 유지** 휴리스틱.
- `EXPLAIN` Extra에 `Using filesort`/`Using temporary`가 보이면 인덱스 + ORDER BY 매핑 재검토.

### 5.3 EXPLAIN ANALYZE 읽기

- 안쪽 노드부터 actual time/rows를 읽기. estimate와 actual rows의 괴리가 크면 통계 갱신/히스토그램.
- 인덱스가 안 쓰이면 (1) leftmost prefix 위반, (2) 함수 적용으로 인덱스 무효, (3) 옵티마이저 cost 잘못 추정 — 옵티마이저 트레이스로 확인.

### 5.4 JPA 함정 회피

- 기본 LAZY → N+1. fetch graph(@EntityGraph) + keyset pagination이 모범.
- `findAll(Pageable)`에 컬렉션 JOIN FETCH 절대 금지(메모리 페이징 경고).
- 영속성 컨텍스트 안에 너무 많은 엔티티(만 단위) 들고 있지 말 것. 배치 처리 시 주기적 `flush()` + `clear()`.
- JdbcTemplate/MyBatis와 같은 트랜잭션을 공유할 때는 `entityManager.flush()`로 JPA pending 쓰기를 먼저 동기화.

### 5.5 배치 처리

- `spring.jpa.properties.hibernate.jdbc.batch_size`(예: 50), `order_inserts=true`, `order_updates=true`.
- JDBC URL: `rewriteBatchedStatements=true`.
- ID 전략: SEQUENCE/TABLE(IDENTITY 금지).
- JdbcTemplate batchUpdate는 1000 이하 청크 단위, 트랜잭션 안에서.
- 수백만 row UPDATE/DELETE: `WHERE id BETWEEN ? AND ? LIMIT N` 청크 분할 → 락 경합·복제 lag 완화.

### 5.6 운영·관측

- 키 지표:
  - **Buffer pool 히트율** ≥ 99%
  - **`Threads_running`** 급증 시 대기 폭증 의심
  - **`Innodb_row_lock_time_avg`**, `data_locks`/`data_lock_waits`
  - **복제 lag**: `Seconds_Behind_Source`보다 PS의 `replication_applier_status_*`의 timestamp 컬럼이 정확.
- `slow_query_log` + `long_query_time`(예: 1초) + `log_queries_not_using_indexes`. 분석은 `pt-query-digest`.
- performance_schema는 8.0에서 기본 ON. 단 모든 instrument ON은 ~15% TPS 손해 — **필요한 것만**.

### 5.7 보안

- `REQUIRE SSL` 강제, 8.0 기본 인증 플러그인 `caching_sha2_password` 사용.
- 감사 로그: MySQL Enterprise Audit 또는 Percona Audit Plugin.
- RLS는 네이티브 미지원 → view + stored function + trigger로 구현하거나 애플리케이션 레이어에서 처리. AWS는 Aurora/RDS for MySQL용 RLS 패턴 블로그 제공.
- 비밀번호가 SQL/general log에 평문으로 남지 않도록 `--log-raw=OFF`, `mysql_config_editor`로 .my.cnf 평문 저장 회피.

### 5.8 캐릭터셋·콜레이션

- 8.0 신규 테이블은 `utf8mb4_0900_ai_ci`. 5.7에서 마이그레이션 시 NO PAD 동작 차이(`'a'` vs `'a '`) 주의.
- 옛 코드를 살리려면 컬럼 단위로 `utf8mb4_unicode_ci`를 명시.

### 5.9 메이저 업그레이드 체크리스트

1. pt-upgrade로 쿼리 호환성 확인.
2. 인증 플러그인 변경(`caching_sha2_password`)에 클라이언트 드라이버 대응 확인.
3. 8.4의 default 변경(AHI/change buffer OFF 등) 영향 측정.
4. Blue/Green 또는 8.0 리플리카 승격 패턴.
5. 5.7 리플리카를 일정 기간 유지(다운그레이드 불가 → escape hatch).
6. MRTE 같은 트래픽 미러링으로 사전 검증.

---

## 6. 참고문헌 (URL·DOI 포함)

### 6.1 공식 문서 (Oracle/MySQL)
- MySQL :: 13.5 The JSON Data Type — https://dev.mysql.com/doc/refman/8.0/en/json.html
- MySQL :: 15.1.20.9 Secondary Indexes and Generated Columns — https://dev.mysql.com/doc/refman/8.0/en/create-table-secondary-indexes.html
- MySQL :: 15.2.20 WITH (Common Table Expressions) — https://dev.mysql.com/doc/refman/8.0/en/with.html
- MySQL :: 17.3 InnoDB Multi-Versioning — https://dev.mysql.com/doc/refman/8.0/en/innodb-multi-versioning.html
- MySQL :: 17.5.1 Buffer Pool — https://dev.mysql.com/doc/refman/8.0/en/innodb-buffer-pool.html
- MySQL :: 17.6.5 Redo Log — https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log.html
- MySQL :: 17.7.1 InnoDB Locking — https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html
- MySQL :: 17.7.2.1 Transaction Isolation Levels — https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html
- MySQL :: 17.7.4 Phantom Rows / Next-Key Locking — https://dev.mysql.com/doc/refman/8.0/en/innodb-next-key-locking.html
- MySQL :: 17.7.5 Deadlocks in InnoDB — https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks.html
- MySQL :: 17.7.5.3 How to Minimize and Handle Deadlocks — https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks-handling.html
- MySQL :: 19.4.10 Semisynchronous Replication — https://dev.mysql.com/doc/refman/8.0/en/replication-semisync.html
- MySQL :: 26.1 Overview of Partitioning — https://dev.mysql.com/doc/refman/8.4/en/partitioning-overview.html
- MySQL :: 10.9.6 Optimizer Statistics — https://dev.mysql.com/doc/refman/8.0/en/optimizer-statistics.html
- MySQL :: EXPLAIN ANALYZE 블로그 아카이브 — https://dev.mysql.com/blog-archive/mysql-explain-analyze/
- MySQL :: Histogram statistics in MySQL — https://dev.mysql.com/blog-archive/histogram-statistics-in-mysql/
- MySQL :: Indexing JSON documents via Virtual Columns — https://dev.mysql.com/blog-archive/indexing-json-documents-via-virtual-columns/
- MySQL :: InnoDB Data Locking — Part 3 "Deadlocks" — https://dev.mysql.com/blog-archive/innodb-data-locking-part-3-deadlocks/
- MySQL :: Dynamic InnoDB Redo Log in MySQL 8.0 — https://dev.mysql.com/blog-archive/dynamic-innodb-redo-log-in-mysql-80/
- MySQL :: Migrating from older collations — https://dev.mysql.com/blog-archive/mysql-8-0-collations-migrating-from-older-collations/
- MySQL Performance Schema Quick Start — https://dev.mysql.com/doc/refman/8.0/en/performance-schema-quick-start.html
- MySQL Internals Manual — https://dev.mysql.com/doc/internals/en/

### 6.2 AWS 공식 자료
- Major version upgrades for RDS for MySQL — https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.MySQL.Major.html
- Aurora MySQL major version upgrade — https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Updates.MajorVersionUpgrade.html
- Aurora features — https://aws.amazon.com/rds/aurora/features/
- Implement row-level security in Amazon Aurora MySQL and Amazon RDS for MySQL — https://aws.amazon.com/blogs/database/implement-row-level-security-in-amazon-aurora-mysql-and-amazon-rds-for-mysql/

### 6.3 권위 있는 기술 블로그 (영문)
- Percona — InnoDB's Gap Locks: https://www.percona.com/blog/innodbs-gap-locks/
- Percona — The Ultimate Guide to MySQL Partitions: https://www.percona.com/blog/what-is-mysql-partitioning/
- Percona — Introduction to MySQL 8.0 Recursive CTE (Part 2): https://www.percona.com/blog/introduction-to-mysql-8-0-recursive-common-table-expression-part-2/
- Percona — Aurora vs RDS: https://www.percona.com/blog/when-should-i-use-amazon-aurora-and-when-should-i-use-rds-mysql/
- Percona — Upgrade MySQL to 8.0: Avoid Disaster: https://www.percona.com/blog/upgrade-mysql-to-8-0-yes-but-avoid-disaster/
- Mydbops — AWS MySQL RDS vs Aurora performance: https://www.mydbops.com/blog/aws-mysql-rds-vs-aurora-vs-serverless-performance
- Mydbops — Dynamic InnoDB redo log resize 8.0.30: https://www.mydbops.com/blog/dynamic-innodb-redo-log-resize-mysql-8-0-30
- Bytebase — Aurora vs RDS engineering guide 2025: https://www.bytebase.com/blog/aurora-vs-rds/
- Bytebase — How to show MySQL locks: https://www.bytebase.com/reference/mysql/how-to/how-to-show-mysql-locks/
- Skeema — Five Surprises in MySQL 8.4 LTS: https://www.skeema.io/blog/2024/05/14/mysql84-surprises/
- Vlad Mihalcea — Keyset Pagination with JPA and Hibernate: https://vladmihalcea.com/keyset-pagination-jpa-hibernate/
- Vlad Mihalcea — High-Performance Java Persistence, Chapter 13 Flushing: https://vladmihalcea.com/high-performance-java-persistence-chapter-13-flushing/
- Vlad Mihalcea — JPA First-Level Cache: https://vladmihalcea.com/jpa-hibernate-first-level-cache/
- Vlad Mihalcea — Index JSON columns in MySQL: https://vladmihalcea.com/index-json-columns-mysql/
- Vlad Mihalcea — SQL Seek/Keyset pagination: https://vladmihalcea.com/sql-seek-keyset-pagination/
- Vlad Mihalcea — Java data access technology survey: https://vladmihalcea.com/java-data-access-technology/
- Thorben Janssen — Offset vs Keyset Pagination with Spring Data JPA: https://thorben-janssen.com/offset-and-keyset-pagination-with-spring-data-jpa/
- Baeldung — Batch Insert/Update with Hibernate/JPA: https://www.baeldung.com/jpa-hibernate-batch-insert-update
- Baeldung — Spring Data JPA Batch Inserts: https://www.baeldung.com/spring-data-jpa-batch-inserts
- Baeldung — Optimistic Locking in JPA: https://www.baeldung.com/jpa-optimistic-locking
- Baeldung — DDD aggregates and @DomainEvents: https://www.baeldung.com/spring-data-ddd
- CodeWiz — Locking strategies in Spring Boot: https://codewiz.info/blog/locking-strategies-spring-boot/
- DoHost — Leftmost prefix rule: https://dohost.us/index.php/2025/08/01/the-leftmost-prefix-rule-optimizing-composite-index-usage/
- Red-Gate — Composite B-tree indexes: https://www.red-gate.com/simple-talk/databases/mysql/mysql-index-overviews-composite-b-tree-indexes/
- Egnyte — Evaluating MySQL Recursive CTE at scale: https://www.egnyte.com/blog/post/12780evaluating-mysql-recursive-cte-at-scale/
- Severalnines — Tips for upgrading to MySQL 8: https://severalnines.com/blog/tips-for-upgrading-mysql-5-7-to-mysql-8/
- CloudZero — Aurora vs RDS: https://www.cloudzero.com/blog/aurora-vs-rds/
- brandur.org — Soft Deletion Probably Isn't Worth It: https://brandur.org/soft-deletion
- Brent Ozar — What Are Soft Deletes: https://www.brentozar.com/archive/2020/02/what-are-soft-deletes-and-how-are-they-implemented/
- Cultured Systems — Avoiding the soft delete anti-pattern: https://www.cultured.systems/2024/04/24/Soft-delete/
- CodeRed — Guide to MySQL Charsets & Collations: https://www.coderedcorp.com/blog/guide-to-mysql-charsets-collations/
- Alibaba Cloud — Analysis of MySQL Cost Estimator: https://www.alibabacloud.com/blog/analysis-of-mysql-cost-estimator_601201
- Alibaba Cloud — To MGR or Not MGR: https://www.alibabacloud.com/blog/to-mgr-or-not-mgr-review-of-mysql-group-replication_72374
- hackmysql — Monitoring replication lag with Performance Schema: https://hackmysql.com/monitoring-replication-lag-with-performance-schema/
- InfoQ — Aurora Limitless GA: https://www.infoq.com/news/2024/11/amazon-aurora-limiteless/
- Jepsen — MySQL 8.0.34 분석: https://jepsen.io/analyses/mysql-8.0.34

### 6.4 InnoDB 내부 / 학술
- Jeremy Cole — InnoDB series (blog.jcole.us): https://blog.jcole.us/innodb/
  - On learning InnoDB: A journey to the core (2013)
  - The physical structure of InnoDB index pages (2013)
  - The physical structure of records in InnoDB (2013)
  - B+Tree index structures in InnoDB (2013)
  - Efficiently traversing InnoDB B+Trees with the page directory (2013)
- Mark Callaghan — Small Datum: http://smalldatum.blogspot.com/
  - MySQL 5.6 thru 9.4: small server, Insert Benchmark (2025): http://smalldatum.blogspot.com/2025/08/mysql-56-thru-94-small-server-insert.html
  - MyRocks vs InnoDB with sysbench (2023): http://smalldatum.blogspot.com/2023/04/myrocks-vs-innodb-with-sysbench.html
- Cahill, M. (2009) *Serializable Isolation for Snapshot Databases* (PhD thesis, USyd): https://ses.library.usyd.edu.au/bitstream/handle/2123/5353/michael-cahill-2009-thesis.pdf
- Neumann, T., Mühlbauer, T., Kemper, A. (2015) *Fast Serializable Multi-Version Concurrency Control for Main-Memory Database Systems* (SIGMOD): https://db.in.tum.de/~muehlbau/papers/mvcc.pdf
- Larson, P.-Å. 외 (Microsoft Research, 2011) *High-Performance Concurrency Control Mechanisms for Main-Memory Databases*: https://www.microsoft.com/en-us/research/wp-content/uploads/2011/12/MVCC-published-revised.pdf
- Alhomssi, A. 외 (2023) *Scalable and Robust Snapshot Isolation for High-Performance Storage Engines* (PVLDB 16): https://www.vldb.org/pvldb/vol16/p1426-alhomssi.pdf
- Gomez Ferro, D., Yabandeh, M. (arXiv) *A Critique of Snapshot Isolation*: https://arxiv.org/pdf/2405.18393

### 6.5 도서
- Schwartz, B., Zaitsev, P., Tkachenko, V. (2012) *High Performance MySQL, 3rd Edition*, O'Reilly.
- Aubin, J., Bell, C. (2021) *High Performance MySQL, 4th Edition*, O'Reilly.
- 백은빈·이성욱 (2021) *Real MySQL 8.0* 1·2권, 위키북스. https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=278488709

### 6.6 한국 기술 블로그·발표
- 우아한형제들 — MySQL을 이용한 분산락: https://techblog.woowahan.com/2631/
- 우아한형제들 — 하이버네이트 배치 설정: https://techblog.woowahan.com/2695/
- 우아한형제들 — Aurora MySQL vs Aurora PostgreSQL: https://techblog.woowahan.com/6550/
- 카카오 — MySQL InnoDB Log 이해: https://tech.kakao.com/posts/721
- 카카오 — InnoDB Adaptive Hash Index 활용: https://tech.kakao.com/posts/319
- 카카오 — Ascending vs Descending index: https://tech.kakao.com/posts/351
- 카카오 — ALTER DDL 수행 방식: https://tech.kakao.com/posts/703
- 카카오 — Instant DDL Algorithm: https://tech.kakao.com/posts/731
- 카카오 — MRTE (MySQL Realtime Traffic Emulator): https://tech.kakao.com/posts/311
- 토스 SLASH 21 — MYSQL HA & DR Topology: https://toss.im/slash-21/sessions/2-3
- LINE Engineering — performance-schema-instruments 영향: https://engineering.linecorp.com/en/blog/mysql-research-performance-schema-instruments
- LINE Engineering — yoku0825 인터뷰: https://engineering.linecorp.com/en/interview/mysql-yoku0825

### 6.7 한국 개인 블로그·velog·OKKY
- velog "MySQL 인덱스 성능 개선하기 - 커버링 인덱스": https://velog.io/@rnjsrntkd95/MySQL-%EC%9D%B8%EB%8D%B1%EC%8A%A4-%EC%84%B1%EB%8A%A5-%EA%B0%9C%EC%84%A0%ED%95%98%EA%B8%B0-%EC%BB%A4%EB%B2%84%EB%A7%81-%EC%9D%B8%EB%8D%B1%EC%8A%A4
- velog "슬로우 쿼리 개선기": https://velog.io/@bruni_23yong/%EC%8A%AC%EB%A1%9C%EC%9A%B0-%EC%BF%BC%EB%A6%AC-%EA%B0%9C%EC%84%A0%EA%B8%B0
- velog "쿼리 속도 개선기": https://velog.io/@gkh4302/%EC%BF%BC%EB%A6%AC-%EC%86%8D%EB%8F%84-%EA%B0%9C%EC%84%A0%EA%B8%B0
- velog "EXPLAIN ANALYZE 해석법": https://velog.io/@wisepine/MySQL-%EC%8A%AC%EB%A1%9C%EC%9A%B0%EC%BF%BC%EB%A6%AC-%EC%9E%A1%EB%8A%94-%EB%AA%85%EB%A0%B9%EC%96%B4-EXPLAIN-ANALIZE-%ED%95%B4%EC%84%9D%EB%B2%95
- velog "MySQL Explain 인덱스 추가 및 QueryDSL 쿼리 튜닝": https://velog.io/@geon_km/MySQL-Explain-%EC%9D%B8%EB%8D%B1%EC%8A%A4-%EC%B6%94%EA%B0%80-%EB%B0%8F-QueryDSL-%EC%BF%BC%EB%A6%AC-%ED%8A%9C%EB%8B%9D
- velog "성능 개선을 위한 프로파일링 1편: 슬로우 쿼리 로그": https://velog.io/@breadkingdom/MySQL-%EC%84%B1%EB%8A%A5-%EA%B0%9C%EC%84%A0%EC%9D%84-%EC%9C%84%ED%95%9C-%ED%94%84%EB%A1%9C%ED%8C%8C%EC%9D%BC%EB%A7%81-1
- haon.blog "MySQL 네임드 락으로 분산 환경에서의 동시성 이슈 해결": https://haon.blog/database/named-lock/
- 권남이 위키 "MySQL User Lock": https://kwonnam.pe.kr/wiki/database/mysql/user_lock
- letmecompile.com "MySQL InnoDB lock & deadlock 이해하기": https://www.letmecompile.com/mysql-innodb-lock-deadlock/
- OKKY "mysql 인덱스 중복으로 걸려 있는건가요?": https://okky.kr/articles/710070

### 6.8 영문 커뮤니티
- DEV.to — Understanding and Solving the N+1 Problem in Spring Data JPA: https://dev.to/sadiul_hakim/understanding-and-solving-the-n1-problem-in-spring-data-jpa-2b6f
- SharpSkill — Spring Data JPA N+1: Fetch Join and EntityGraph (2026): https://sharpskill.dev/en/blog/spring-boot/spring-data-jpa-n-plus-1-fetch-join-entitygraph
- Medium "1mg JSON support virtual columns and indexing": https://medium.com/1mgofficial/mysql-json-support-virtual-columns-and-indexing-json-31df4cc1aa31
- Medium "Unlocking MySQL: Locks and deadlock": https://medium.com/@carolyn_chen/unlocking-mysql-real-case-studies-on-deadlocks-and-their-causes-2faab5bc0920
- Medium "Spring Boot JPA Bulk Insert Performance by 100 times": https://dev.to/amrutprabhu/spring-boot-jpa-bulk-insert-performance-by-100-times-fn4
- Medium "Bulk Insert Optimization with Spring Boot and JDBC Batching": https://medium.com/@AlexanderObregon/bulk-insert-optimization-with-spring-boot-and-jdbc-batching-57dd031ecad8

---

## 7. 리서치 한계 (커버하지 못한 영역)

- **Spring Batch와 JPA 통합 사례**: 일반 JPA bulk 처리는 다뤘지만, Spring Batch의 `JpaItemWriter`/`JdbcBatchItemWriter` 비교, 청크 사이즈와 트랜잭션 경계 설계는 별도 후속 리서치 필요.
- **QueryDSL/jOOQ 비교**: QueryDSL 활용 1차 자료는 있지만 jOOQ와의 함수 매핑/플루언트 API 비교는 더 모아야 한다.
- **시계열·OLAP 워크로드**: MySQL 8.0 HeatWave/Analytics Engine에 대한 자료는 의도적으로 제외했다. 책 범위(OLTP) 밖.
- **Vitess/ProxySQL/MaxScale**: 샤딩 미들웨어는 큰 그림만 잡혀 있다. 실전 구성 사례(특히 한국어)는 부족.
- **Aurora I/O Optimized 가격 모델**: 가격은 변동성이 커 본문에서 비중을 둘 수 없다. 책에서는 "분기점이 존재한다"는 정도로 표시하고 독자가 최신 가격을 확인하도록 안내.
- **MySQL HeatWave (Lakehouse / Vector)**: 2024~2025년에 빠르게 진화 중이지만 본 책의 핵심(트랜잭션·튜닝·운영) 밖.
- **NDB Cluster**: 운영 사례가 한국 시장에서 드물어 의도적으로 제외.
- **MySQL 9.x 신기능**: 8.0/8.4 LTS 중심으로 정리했고 9.x는 사례 부족으로 보류.
- **에이전트 기반 병렬 리서치 미수행**: 환경 제약으로 web/paper/community 에이전트를 독립적으로 spawn하지 못하고, 리서치 리드가 직접 WebSearch/WebFetch로 7개 영역을 훑었다. 그 과정에서 토스 toss.tech 글 일부는 URL이 404였으며, 일본 Qiita는 간접 인용으로만 처리했다.
