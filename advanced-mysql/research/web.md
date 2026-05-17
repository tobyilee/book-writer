# 웹 리서치 메모: 고급 MySQL × Spring 개발자

수집 출처: 공식 MySQL/AWS/Oracle 문서, Percona·Mydbops·Bytebase·Vlad Mihalcea·Baeldung·DEV·Medium 등 영문 기술 블로그.

---

## 1. InnoDB 내부 구조와 트랜잭션 처리

### 1.1 redo log / undo log / MVCC
- WAL(Write-Ahead Logging) 원리. 데이터 파일에 쓰기 전 redo log에 기록 → 크래시 복구 보장. MySQL 8.0.30부터 `innodb_redo_log_capacity`로 동적 리사이즈 가능, 내부적으로 32개의 redo 파일로 분할 관리. [MySQL Ref 17.6.5](https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log.html), [Mydbops: Dynamic redo log resize](https://www.mydbops.com/blog/dynamic-innodb-redo-log-resize-mysql-8-0-30)
- Undo log는 이전 row 버전을 보관 → (1) 트랜잭션 롤백, (2) MVCC 스냅샷 재구성 두 가지 역할. 각 row에 6바이트 `DB_TRX_ID`와 7바이트 `DB_ROLL_PTR`이 붙음. [MySQL 17.3 Multi-Versioning](https://dev.mysql.com/doc/refman/8.0/en/innodb-multi-versioning.html)
- 8.0 초기 버전(8.0.x)에서 undo log truncation 버그로 데이터 손상 사례 있음 → `innodb_undo_log_truncate` 끄거나 패치 적용 권고. [J-F Gagné blog](https://jfg-mysql.blogspot.com/2026/01/undo-log-truncation-bug-in-80-leads-to-data-corruption.html.html)

### 1.2 격리수준과 락
- InnoDB 기본 격리수준은 REPEATABLE READ. Next-key lock(레코드 락 + gap lock) 알고리즘으로 phantom read 차단. [MySQL 17.7.4 Phantom Rows](https://dev.mysql.com/doc/refman/8.0/en/innodb-next-key-locking.html)
- Gap lock의 목적은 gap 진입 차단이 아니라 *insert* 차단. 따라서 gap lock끼리는 서로 호환된다. [Percona: InnoDB's Gap Locks](https://www.percona.com/blog/innodbs-gap-locks/)
- READ COMMITTED로 낮추면 gap lock이 제거되며 데드락은 줄지만 phantom read가 다시 발생. 격리수준 선택은 일관성/동시성 트레이드오프. [MySQL 17.7.2.1](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html)

### 1.3 데드락
- `SHOW ENGINE INNODB STATUS`의 `LATEST DETECTED DEADLOCK` 섹션이 1순위 분석 도구. `innodb_print_all_deadlocks=ON`으로 에러 로그에 모든 데드락 기록. [MySQL 17.7.5.3](https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks-handling.html)
- 8.0의 `performance_schema.data_locks`, `data_lock_waits`로 실시간 대기 그래프 조회 가능. [Bytebase: how to show MySQL locks](https://www.bytebase.com/reference/mysql/how-to/how-to-show-mysql-locks/)
- 자주 보는 데드락 패턴: INSERT ON DUPLICATE KEY UPDATE 동시 실행, 공유락→배타락 업그레이드, 역순 키 접근. [Medium: real case studies](https://medium.com/@carolyn_chen/unlocking-mysql-real-case-studies-on-deadlocks-and-their-causes-2faab5bc0920), [InnoDB Data Locking Part 3](https://dev.mysql.com/blog-archive/innodb-data-locking-part-3-deadlocks/)

### 1.4 버퍼풀
- 기본 128MB는 운영용으로 부족. 전용 DB 서버는 가용 RAM의 70~80% 권고, 8GB 초과 시 `innodb_buffer_pool_instances`로 분할. [Datacamp: Buffer Pool tuning](https://www.datacamp.com/doc/mysql/mysql-innodb-buffer-pool-tuning), [Burnison: buffer pool fact](https://www.burnison.ca/notes/fun-mysql-fact-of-the-day-buffer-pool-size)
- 너무 크게 잡으면 OS 스왑 발생 → 1~2GB는 OS·커넥션·정렬 버퍼용으로 남길 것. [oneuptime: tune buffer pool](https://oneuptime.com/blog/post/2026-03-31-mysql-how-to-tune-innodb-buffer-pool-size-in-mysql/view)

---

## 2. 고급 SQL: 윈도우 함수·CTE·JSON

### 2.1 윈도우 함수, CTE
- MySQL 8.0부터 윈도우 함수와 CTE(WITH) 정식 지원. 서브쿼리·임시 테이블 대안으로 가독성·성능 모두 향상. [MySQL 15.2.20 WITH](https://dev.mysql.com/doc/refman/8.0/en/with.html)
- 재귀 CTE는 anchor + recursive member + UNION ALL 구조. UNION을 쓰면 매 레벨마다 DISTINCT 정렬이 들어가 대규모 트리에서 치명적으로 느려진다. 큰 결과 셋에서 임시 테이블이 디스크로 떨어지면 성능 저하 → `tmp_table_size`/`max_heap_table_size` 조정 필요. [Percona: Recursive CTE Part 2](https://www.percona.com/blog/introduction-to-mysql-8-0-recursive-common-table-expression-part-2/), [Egnyte: Recursive CTE at Scale](https://www.egnyte.com/blog/post/12780evaluating-mysql-recursive-cte-at-scale/)

### 2.2 JSON 컬럼
- JSON 컬럼은 직접 인덱싱 불가 → virtual generated column + secondary index가 표준 패턴. 8.0.21부터 `JSON_VALUE`를 통한 functional index 사용 가능. [MySQL 13.5 JSON](https://dev.mysql.com/doc/refman/8.0/en/json.html), [Vlad: index JSON columns](https://vladmihalcea.com/index-json-columns-mysql/)
- 실측: 인덱싱된 generated column으로 5.7초 → 280ms 단축. STORED는 디스크/메모리 부담, VIRTUAL은 읽을 때마다 계산하지만 인덱스가 없으면 비용. [Medium: 1mg JSON index](https://medium.com/1mgofficial/mysql-json-support-virtual-columns-and-indexing-json-31df4cc1aa31), [Chat2DB JSON indexing](https://medium.com/chat2db/optimizing-json-queries-with-advanced-indexing-in-mysql-8-0-392f2fdfd842)

### 2.3 인덱스 설계
- B+Tree 기반. 복합 인덱스는 **leftmost prefix rule** — `(A,B,C)`는 A / A,B / A,B,C 조회에 유효, B만으로는 사용 불가. [DoHost: Leftmost prefix rule](https://dohost.us/index.php/2025/08/01/the-leftmost-prefix-rule-optimizing-composite-index-usage/)
- 컬럼 순서 규칙: equality 조건 → range 조건 순서, 고카디널리티 컬럼을 앞쪽으로. [Red-Gate: composite B-tree indexes](https://www.red-gate.com/simple-talk/databases/mysql/mysql-index-overviews-composite-b-tree-indexes/)
- 커버링 인덱스: `EXPLAIN` Extra에 `Using index`가 보이면 클러스터링 인덱스를 만지지 않고 종료. `key_len`으로 인덱스가 실제 어디까지 사용됐는지 확인. [DEV.to: Composite indexes structure](https://dev.to/chat2db/understanding-mysql-composite-indexes-structure-search-behavior-and-optimization-principles-4d5l)

### 2.4 EXPLAIN ANALYZE와 옵티마이저
- 8.0.18부터 `EXPLAIN ANALYZE`는 쿼리를 실제로 실행하며 단계별 actual time/rows를 보여준다. [MySQL EXPLAIN ANALYZE](https://dev.mysql.com/blog-archive/mysql-explain-analyze/)
- 옵티마이저는 cost-based: `mysql.server_cost`, `mysql.engine_cost`로 cost 상수 튜닝 가능. [MySQL 10.9.6 Optimizer Statistics](https://dev.mysql.com/doc/refman/8.0/en/optimizer-statistics.html)
- 8.0에서 도입된 **histogram statistics**(`ANALYZE TABLE ... UPDATE HISTOGRAM`)는 비인덱스 컬럼의 값 분포까지 추정 가능 → 옵티마이저 선택 개선. [MySQL: Histogram statistics](https://dev.mysql.com/blog-archive/histogram-statistics-in-mysql/)
- `optimizer_trace`를 ON으로 켜면 옵티마이저가 고려한 모든 plan과 cost를 JSON으로 덤프해 의사 결정 근거를 확인할 수 있다. [Alibaba: MySQL Cost Estimator](https://www.alibabacloud.com/blog/analysis-of-mysql-cost-estimator_601201)

---

## 3. AWS 멀티 인스턴스/복제/파티셔닝

### 3.1 RDS for MySQL vs Aurora MySQL
- 가장 큰 차이는 **스토리지 아키텍처**. RDS는 인스턴스에 EBS가 붙고 binary log 기반 비동기 복제. Aurora는 3 AZ × 6-way로 redo 스트림이 공유 분산 스토리지에 기록되고, 리플리카는 같은 스토리지에서 읽기 때문에 lag이 ms 수준. [Mydbops: AWS RDS vs Aurora](https://www.mydbops.com/blog/aws-mysql-rds-vs-aurora-vs-serverless-performance), [Bytebase: Aurora vs RDS 2025](https://www.bytebase.com/blog/aurora-vs-rds/)
- 리드 리플리카 수: RDS 5개 vs Aurora 15개. Aurora는 같은 볼륨을 공유하므로 스토리지 비용은 1배만 청구.
- Aurora Limitless Database는 2025년 현재 PostgreSQL 전용 — MySQL은 미지원. MySQL은 여전히 애플리케이션 레벨 샤딩(Vitess 등)이나 RDS Proxy + 수평 분할에 의존. [InfoQ: Aurora Limitless](https://www.infoq.com/news/2024/11/amazon-aurora-limiteless/), [AWS Aurora features](https://aws.amazon.com/rds/aurora/features/)
- 비용 모델: Aurora가 인스턴스/스토리지 가격이 더 비싸지만 IO 비용이 별도 청구되지 않는다(I/O Optimized 옵션). RDS는 IO 단가가 누적되면 Aurora가 더 싸지는 분기점이 자주 나옴. [CloudZero: Aurora vs RDS](https://www.cloudzero.com/blog/aurora-vs-rds/)

### 3.2 복제와 HA
- GTID(Global Transaction Identifier)는 트랜잭션마다 고유 UUID:txnum 형식 ID를 부여 → 페일오버·재구성 시 binlog 좌표 추적 불필요. [Percona: replication overview](https://www.percona.com/blog/overview-of-different-mysql-replication-solutions/)
- Semi-sync 복제: 최소 1개 리플리카가 receive ACK한 뒤 커밋. 비동기보다 데이터 손실 위험은 낮지만 TCP RTT만큼 지연. [MySQL 19.4.10 Semisynchronous](https://dev.mysql.com/doc/refman/8.0/en/replication-semisync.html)
- Group Replication(MGR)은 Paxos 기반 멀티 마스터까지 지원하지만 최대 9 노드, InnoDB만, 모든 테이블에 PK 필수. peak throughput은 semi-sync보다 낮다는 보고. [Alibaba: MGR review](https://www.alibabacloud.com/blog/to-mgr-or-not-mgr-review-of-mysql-group-replication_72374)

### 3.3 파티셔닝
- RANGE/LIST/HASH/KEY 네 종류. RANGE+날짜 파티셔닝이 가장 흔한 케이스(월별/일별). [MySQL 26.1 Overview](https://dev.mysql.com/doc/refman/8.4/en/partitioning-overview.html), [Percona: ultimate guide to partitions](https://www.percona.com/blog/what-is-mysql-partitioning/)
- 한계: 외래키 사용 불가, 글로벌 UNIQUE 제약은 파티션 키를 포함해야만 함, 파티션 키 표현식 제약, ENUM 등 일부 타입 제한. 파티션 프루닝은 WHERE에 파티션 키가 들어와야 작동.
- 파티셔닝 vs 샤딩: 파티셔닝은 단일 인스턴스 내 데이터 분할(엔진이 라우팅), 샤딩은 별개 인스턴스에 분산(애플리케이션/미들웨어가 라우팅). 단일 노드 한계를 넘으면 샤딩으로. [Rapydo: sharding & partitioning](https://www.rapydo.io/blog/sharding-and-partitioning-strategies-in-sql-databases)

### 3.4 백업과 PITR
- binlog + 풀백업(mysqldump / xtrabackup / Percona XtraBackup) 조합으로 Point-in-Time Recovery. Aurora는 연속 백업으로 5분 단위 PITR 가능. [AWS RDS Backup](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.MySQL.Major.html)

### 3.5 메이저 업그레이드 (5.7 → 8.0)
- 다운그레이드 불가. 사전에 `mysqlcheck --check-upgrade`, `pt-upgrade`로 쿼리 호환성 사전 검증 필수. Blue/Green Deployment(AWS RDS), 또는 8.0 리플리카 승격 패턴이 안전. [Percona: upgrade MySQL 8.0](https://www.percona.com/blog/upgrade-mysql-to-8-0-yes-but-avoid-disaster/), [Severalnines: tips for upgrading](https://severalnines.com/blog/tips-for-upgrading-mysql-5-7-to-mysql-8/)
- 8.0 → 8.4 LTS 업그레이드 가이드에서는 charset/collation 기본값, 인증 플러그인(`caching_sha2_password`) 등을 미리 점검. [ReliaDB: 8.0 → 8.4 guide](https://reliadb.com/blog/mysql-8-to-8-4-upgrade-change-management-checklist.html)

---

## 4. JPA + Native SQL

### 4.1 영속성 컨텍스트와 트랜잭션
- 1차 캐시 = Persistence Context. EntityManager가 entity 스냅샷을 보유, **dirty checking**으로 flush 시점에 SQL UPDATE 생성. [Vlad: first-level cache](https://vladmihalcea.com/jpa-hibernate-first-level-cache/), [Vlad: flushing](https://vladmihalcea.com/high-performance-java-persistence-chapter-13-flushing/)
- 기본 FlushMode는 AUTO — commit 직전 + 모든 쿼리 실행 전 flush. JdbcTemplate/MyBatis와 같은 트랜잭션 안에서 섞어 쓰면 JPA flush 누락으로 stale 데이터 읽을 위험 → `EntityManager.flush()` 명시 호출 권고. [JavaCodeGeeks: first-level cache](https://www.javacodegeeks.com/2017/04/understanding-first-level-jpa-cache.html)

### 4.2 N+1과 fetch 전략
- 기본 LAZY 로딩이 N+1의 주범. 해결책: `JOIN FETCH`, `@EntityGraph`, `@BatchSize`/`default_batch_fetch_size`, `@Fetch(SUBSELECT)`. [Baeldung: JPA N+1 patterns](https://www.baeldung.com/jpa-hibernate-batch-insert-update)
- `@EntityGraph`는 페이지네이션과 호환되지만 JOIN FETCH는 컬렉션 + Pageable과 함께 쓰면 메모리 페이징 경고("firstResult/maxResults specified with collection fetch; applying in memory")가 나오며 위험. [DEV.to: N+1 in Spring Data JPA](https://dev.to/sadiul_hakim/understanding-and-solving-the-n1-problem-in-spring-data-jpa-2b6f), [SharpSkill: fetch join vs EntityGraph 2026](https://sharpskill.dev/en/blog/spring-boot/spring-data-jpa-n-plus-1-fetch-join-entitygraph)

### 4.3 페이지네이션
- 깊은 페이지(OFFSET 100000)에서는 인덱스를 OFFSET까지 스캔 → keyset(seek) 방식으로 변경: `WHERE (created_at, id) < (?, ?) ORDER BY created_at DESC, id DESC LIMIT N`. Vlad는 정확성(중간 INSERT에도 일관) + 성능 둘 다 우월하다고 정리. [Vlad: keyset pagination](https://vladmihalcea.com/keyset-pagination-jpa-hibernate/), [Vlad: SQL Seek method](https://vladmihalcea.com/sql-seek-keyset-pagination/), [Thorben Janssen: offset vs keyset](https://thorben-janssen.com/offset-and-keyset-pagination-with-spring-data-jpa/)
- Spring Data 3.x의 `WindowIterator`로 keyset 페이지네이션이 표준 라이브러리에 포함. [Vlad: Spring Data WindowIterator](https://vladmihalcea.com/spring-data-windowiterator/)

### 4.4 배치 처리
- `spring.jpa.properties.hibernate.jdbc.batch_size`, `order_inserts=true`, `order_updates=true`. ID 생성 전략을 IDENTITY로 쓰면 배치 비활성, **SEQUENCE 또는 TABLE 전략**을 사용해야 함. [Baeldung: Spring Data JPA Batch Inserts](https://www.baeldung.com/spring-data-jpa-batch-inserts), [Medium: bulk insert optimization](https://medium.com/@AlexanderObregon/bulk-insert-optimization-with-spring-boot-and-jdbc-batching-57dd031ecad8)
- 권장 batch_size는 다양: 5~30(소형 트랜잭션), 50~100(JDBC 권장), 200(I/O bound 워크로드). DB와 row 크기로 측정.
- JdbcTemplate `batchUpdate()`는 1000 이하로 묶고, 트랜잭션 안에서 호출. MySQL JDBC URL에 `rewriteBatchedStatements=true`를 켜야 multi-row INSERT로 묶인다. [Javabydeveloper: JdbcTemplate batch insert](https://javabydeveloper.com/spring-jdbctemplate-batch-update-with-maxperformance/)
- 수백만 row UPDATE/DELETE는 `WHERE id BETWEEN ? AND ?` + LIMIT로 청크 분할 → 락 경합/리플리카 lag 완화. [Start Data Engineering: update millions](https://www.startdataengineering.com/post/update-mysql-in-batch/), [gabfl/mysql-batch on GitHub](https://github.com/gabfl/mysql-batch)

### 4.5 JPA vs JdbcTemplate vs MyBatis (혼용 기준)
- JPA는 표준 CRUD/도메인 모델에, JdbcTemplate는 단순 SQL 몇 개에, MyBatis는 SQL 자유도가 필요한 보고서/대량 처리에 강점. 한 프로젝트에서 **하이브리드**가 일반적: 트랜잭션 경계는 JPA가 잡고, 무거운 쿼리는 JdbcTemplate로 빠져나간다. [Medium: Spring Data JPA vs MyBatis](https://medium.com/an-idea/spring-boot-spring-data-jpa-vs-mybatis-514d969648ee), [GitHub: persistence frameworks comparison](https://github.com/bwajtr/java-persistence-frameworks-comparison)

### 4.6 락
- 낙관적 락 `@Version`은 읽기 동시성 우수, 충돌 시 `OptimisticLockingFailureException`. 비관적 락은 `@Lock(PESSIMISTIC_WRITE)` → SELECT ... FOR UPDATE 발급. [Baeldung: Optimistic Locking in JPA](https://www.baeldung.com/jpa-optimistic-locking), [CodeWiz: locking strategies](https://codewiz.info/blog/locking-strategies-spring-boot/)
- 락 선택 휴리스틱: 갈등이 드물고 retry 가능 → optimistic, 갈등이 잦고 retry 비용이 큼(예: 결제·재고) → pessimistic.

---

## 5. 모니터링과 보안

- 핵심 지표: QPS, `Innodb_buffer_pool_read_requests` 대비 `Innodb_buffer_pool_reads`로 히트율 산출(99% 이상 권고), `Threads_running`, `Innodb_row_lock_time_avg`, 복제 lag(`Seconds_Behind_Source` + Performance Schema timestamp 컬럼). [oneuptime: monitoring InnoDB buffer pool](https://oneuptime.com/blog/post/2026-02-06-mysql-innodb-buffer-pool-slow-query/view), [hackmysql: monitoring replication lag](https://hackmysql.com/monitoring-replication-lag-with-performance-schema/), [Jesper: replication monitoring with PS](https://mysql.wisborg.dk/2018/10/05/replication-monitoring-with-the-performance-schema/)
- `performance_schema`는 8.0에서 기본 ON. 다만 모든 instrument를 ON으로 켜면 약 15% TPS 손실 보고 → 필요한 것만 선택적으로 켤 것. [LINE Engineering: PS instruments perf impact](https://engineering.linecorp.com/en/blog/mysql-research-performance-schema-instruments)
- 보안: 모든 사용자에 `REQUIRE SSL`, 감사 로그(MySQL Enterprise Audit / Percona Audit Plugin), 비밀번호가 SQL 로그에 평문으로 남지 않도록 `--log-raw=OFF`. [Satori: MySQL security best practices](https://satoricyber.com/mysql-security/mysql-security-common-threats-and-8-best-practices/)
- MySQL은 네이티브 RLS가 없음 — view+stored function+trigger로 구현하거나 애플리케이션 레벨 필터링. AWS는 Aurora MySQL/RDS for MySQL용 RLS 패턴 블로그 제공. [AWS: implement RLS in Aurora MySQL](https://aws.amazon.com/blogs/database/implement-row-level-security-in-amazon-aurora-mysql-and-amazon-rds-for-mysql/)

---

## 6. 캐릭터셋 / 콜레이션

- 8.0 기본 콜레이션은 `utf8mb4_0900_ai_ci`(UCA 9.0.0). 이전 디폴트 `utf8mb4_general_ci`(부정확) / `utf8mb4_unicode_ci`(UCA 4.0.0) 대비 정렬·등가비교 정확도 우월. [MySQL: migrating from older collations](https://dev.mysql.com/blog-archive/mysql-8-0-collations-migrating-from-older-collations/)
- 단, NO PAD collation으로 동작 — `'a'`와 `'a '`가 다르게 비교됨. 기존 5.7 데이터를 8.0으로 마이그레이션할 때 행동 변화 주의. [CodeRed: charsets & collations guide](https://www.coderedcorp.com/blog/guide-to-mysql-charsets-collations/), [kedar.nitty-witty.com](https://kedar.nitty-witty.com/blog/mysql-8-utf8mb4_0900_ai_ci-collation-confusion)

---

## 7. Soft Delete / 이력 테이블 패턴

- `deleted_at` 컬럼 + 모든 쿼리에서 `WHERE deleted_at IS NULL` 추가가 흔한 패턴. JPA는 `@SQLDelete`/`@Where`(Hibernate 6에선 `@SoftDelete`)로 자동 처리 가능.
- 안티패턴 경고: 모든 조회/JOIN/UNIQUE 제약/FK에 deleted 조건을 끼워야 해서 누락 시 정합성 깨짐. PostgreSQL의 partial unique index 같은 도구가 부족함. [brandur.org: Soft Deletion Probably Isn't Worth It](https://brandur.org/soft-deletion), [Cultured Systems: avoiding soft delete anti-pattern](https://www.cultured.systems/2024/04/24/Soft-delete/)
- 대안: 별도 `users_archived` 이력 테이블에 옮기기, 또는 트리거 기반 변경 감사 테이블, 또는 Bi-temporal 모델. [DEV.to: change tracking & soft delete](https://dev.to/davidlastrucci/change-tracking-and-soft-delete-audit-trails-without-the-boilerplate-57oc)
