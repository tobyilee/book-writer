# Web Research — PostgreSQL Bible

리서치 일자: 2026-05-18. 공식 문서, 벤더 블로그(Crunchy, Supabase, Neon, Tiger Data, AWS, Microsoft, MotherDuck, ParadeDB, EDB, Percona, Snowflake), 커뮤니티 글로벌 매체 위주.

## 1. PostgreSQL 17/18 핵심 변경

- **PostgreSQL 17 (2024-09 GA)**
  - VACUUM 메모리 관리 재구현 → 대용량 테이블 vacuum 메모리 사용량 대폭 감소
  - 고동시성 워크로드 최적화, 벌크 로드/익스포트 가속, 인덱스 쿼리 실행 개선
  - `JSON_TABLE` (SQL/JSON) 추가 — JSON 데이터를 관계형 테이블처럼 FROM 절에서 사용 가능
  - Logical replication 슬롯 동기화 / 페일오버 슬롯 도입 — 17부터 logical slot이 standby로 복제되어 HA에서 logical replication 지속
  - 17부터 major upgrade 시 logical replication slot drop 불필요
  - 내장 immutable collation provider (UTF-8 기반) — 어디서 돌리든 정렬 결과 동일
  - 출처: <https://www.postgresql.org/about/news/postgresql-17-released-2936/>, <https://www.postgresql.org/docs/release/17.0/>

- **PostgreSQL 18 (2025-09 GA)**
  - OAuth 인증 지원
  - `RETURNING` 절에서 `OLD`/`NEW` 사용 가능 (INSERT/UPDATE/DELETE/MERGE 모두)
  - PRIMARY KEY / UNIQUE / FOREIGN KEY에 temporal constraint
  - Virtual generated columns (쿼리 시점 계산)
  - `uuidv7()` 내장 — 인덱싱·읽기 친화 UUID
  - Major upgrade 시 planner 통계 보존 — 업그레이드 직후 성능 저하 완화
  - 출처: <https://www.postgresql.org/about/news/postgresql-18-released-3142/>, <https://www.postgresql.org/docs/release/18.0/>

- **MERGE / JSON_TABLE (17)**
  - 15에서 도입된 MERGE가 17에서 `RETURNING` 지원으로 강화
  - JSON_TABLE은 JSONPath로 JSON을 행으로 펼쳐 SQL과 자연스럽게 결합
  - 출처: <https://andyatkinson.com/postgresql-17-json-table-merge-returning-updatable-views>, <https://medium.com/@atarax/finally-json-table-is-here-postgres-17-a9b5245649bd>

## 2. 아키텍처와 MVCC

- **프로세스 모델**: postmaster가 클라이언트 접속마다 fork()로 backend 생성. 1 connection = 1 process. PostgreSQL은 스레드를 쓰지 않는다. 따라서 connection 수가 늘면 메모리/컨텍스트 스위치 비용 급증 → PgBouncer/Pgcat 같은 풀러가 사실상 필수.
  - 출처: <https://severalnines.com/blog/understanding-postgresql-architecture/>

- **공유 메모리**: `shared_buffers`(권장 RAM 25%), WAL buffer(기본 shared_buffers의 1/32). Background processes: Background Writer, Checkpointer, WAL Writer, WAL Archiver, Autovacuum launcher, Logger, Stats Collector.
  - 출처: <https://medium.com/@sumeet.k.shukla/postgresql-architecture-6df259dc1145>

- **MVCC 구현 차이 (vs MySQL InnoDB)**: PostgreSQL은 갱신 시 새 row 버전을 같은 테이블에 추가(tuple versioning). InnoDB는 클러스터 인덱스에 최신 버전만 두고 undo log에 이전 값을 둔다. 결과적으로 PG는 VACUUM이 필수, MySQL은 purge thread가 자동 처리.
  - 출처: <https://medium.com/sys-base/postgresql-day-5-mvcc-postgres-vs-mysql-61a06f475984>, <https://kernelmaker.github.io/mysql-vs-pg-mvcc>

- **HOT 업데이트**: 인덱스 컬럼이 변경되지 않고 같은 페이지에 공간이 있으면 새 row를 추가하되 인덱스 항목을 재생성하지 않는다. ctid 체인으로 연결. 인덱스 페이지에는 첫 버전 row 포인터만 유지.
  - 출처: <https://www.postgresql.org/docs/current/storage-hot.html>, <https://postgrespro.com/blog/pgsql/5967910>

## 3. PostgreSQL vs MySQL

- 철학: PG는 “정확성 → 기능 → 성능”, MySQL은 “성능 → 기능 → 정확성”. (Rick Branson 등 인용)
- PG가 강한 영역: 복잡 쿼리, 대용량/혼합 워크로드, 데이터 타입 풍부함, 확장 생태계. MySQL이 강한 영역: 극단적 write 집중, 단순 KV/세션, 운영 단순성.
- 마이그레이션 비용 보고: 4억 row 마이그레이션에 6개월, 다운타임 18시간, 127개 버그, LIMIT 문법/timezone 차이로 47개 쿼리 깨짐.
- 출처: <https://medium.com/@codewar_with_me/postgresql-vs-mysql-i-migrated-400m-rows-heres-what-actually-broke-7b7978051c35>, <https://www.liquibase.com/resources/guides/postgresql-vs-mysql>, <https://aws.amazon.com/compare/the-difference-between-mysql-vs-postgresql/>, <https://rbranson.medium.com/10-things-i-hate-about-postgresql-20dbab8c2791>

## 4. JSON / 문서 DB

- JSONB는 GIN 인덱스로 키/값 검색을 가속. `jsonb_path_ops` operator class는 연산자가 적지만 더 빠르다.
- 한계: GIN 인덱스는 쓰기 비용이 크고, 모든 JSONB 연산자를 지원하지 않아서 의도치 않게 seq scan 폴백 발생.
- 1.25M 데이터 이상에서 일부 GIN 패턴이 seq scan보다 느려진다는 보고도 있음(워크로드 의존).
- MongoDB 대체 가능성: 대다수 워크로드에서는 충분, 그러나 `multi-key index` 조합 인덱스는 PG에서 더 까다롭다.
- 출처: <https://www.crunchydata.com/blog/indexing-jsonb-in-postgres>, <https://pganalyze.com/blog/gin-index>, <https://medium.com/@yurexus/can-postgresql-with-its-jsonb-column-type-replace-mongodb-30dc7feffaf3>, <https://www.postgresql.org/docs/current/datatype-json.html>

## 5. 전문 검색

- **내장 tsvector/tsquery + pg_trgm**: 영문/유럽어 풀텍스트와 fuzzy similarity에 적합. pg_trgm은 non-ASCII 처리에 제약 — 한국어/일본어 토큰화는 부적합.
  - 출처: <https://www.postgresql.org/docs/current/pgtrgm.html>, <https://www.aapelivuorinen.com/blog/2021/02/24/postgres-text-search/>

- **PGroonga**: Groonga 기반 다국어 풀텍스트. 한국어·일본어·중국어·아랍어 등 비라틴 언어를 zero-ETL로 지원. JSON 검색도 가능. Supabase가 공식 익스텐션으로 제공.
  - 출처: <https://pgroonga.github.io/>, <https://supabase.com/docs/guides/database/extensions/pgroonga>

- **ParadeDB / pg_search (BM25)**: Rust로 작성된 Tantivy 기반 BM25 인덱스. 1M row 기준 tsvector보다 인덱싱 50초 빠르고 랭킹 20배 빠름, dedicated Elasticsearch와 비슷한 성능. ACID·MVCC와 통합되므로 ES 동기화 ETL이 사라진다는 게 마케팅 포인트.
  - 출처: <https://www.paradedb.com/blog/introducing-search>, <https://github.com/paradedb/paradedb>, <https://www.tigerdata.com/blog/you-dont-need-elasticsearch-bm25-is-now-in-postgres>

- **pg_textsearch (Tiger Data)**: 같은 BM25를 Postgres 페이지 위에 구현한 대안. 17부터 인덱스 access method API가 좋아져서 경쟁 등장.
  - 출처: <https://www.tigerdata.com/blog/pg-textsearch-bm25-full-text-search-postgres>

## 6. GIS / 지도

- PostGIS는 GiST/SP-GiST 공간 인덱스로 사실상 OSS GIS 표준.
- 2025년 PostGIS Day 발표 사례:
  - State Farm — 재난 대응 클레임 처리에 PostGIS, AWS에서 트래픽 급증 대응.
  - NIBIO (노르웨이) — 전국 토지이용 topology 관리, 수백만 edge 공유.
  - Telkom Kenya — 영업 영역 최적화.
  - 출처: <https://www.snowflake.com/en/engineering-blog/postgis-day-2025-recap/>
- 인덱스/EXPLAIN 운영 노트: <https://www.crunchydata.com/blog/postgis-performance-indexing-and-explain>
- 경량/마이크로서비스 GIS 패턴(FOSS4G Europe 2025): <https://talks.osgeo.org/foss4g-europe-2025/talk/7H7P38/>

## 7. 벡터 / RAG 백엔드

- **pgvector**: HNSW와 IVFFlat 두 인덱스. 5M 벡터 미만 RAG에는 production-ready. HNSW로 95% recall에서 p95 <20ms.
- **pgvectorscale (Timescale/Tiger Data)**: DiskANN + Statistical Binary Quantization. 50M 벡터에서 99% recall로 471 QPS — 같은 조건 Qdrant 41 QPS의 11.4배, Pinecone 대비 28ms vs 784ms p95, 비용 75% 절감.
- 결론: ~10M 벡터까지는 Postgres로 충분, 그 이상 동시성 부하면 dedicated 검토.
- 2026 트렌드: 별도 벡터 DB → relational DB로의 통합.
- 출처: <https://www.tigerdata.com/blog/pgvector-is-now-as-fast-as-pinecone-at-75-less-cost>, <https://www.softwareseni.com/pgvector-pgvectorscale-and-the-postgres-vector-search-stack-explained/>, <https://justsoftlab.com/insights/postgres-pgvector-vs-pinecone-production-benchmark>, <https://neon.com/blog/understanding-vector-search-and-hnsw-index-with-pgvector>

## 8. 이벤트/큐/실시간

- **LISTEN/NOTIFY**: 같은 채널에 LISTEN한 모든 세션이 payload string을 받는 비동기 알림. 트랜잭션 커밋 시점에만 발사. 8KB payload 제한, 영속성 없음.
- **logical decoding (wal2json, pgoutput)**: WAL을 외부에서 읽을 수 있게 변환. Debezium 등이 사용. CDC와 outbox 패턴의 기반.
- **메시지 버스로서의 Postgres**: 중소 규모면 Kafka 도입 전에 Postgres로도 충분. JSONB 페이로드, partial index, partitioning, LISTEN/NOTIFY 조합.
- **pg_cron**: 표준 cron 스케줄로 SQL job 실행. AWS RDS, Azure, PlanetScale 등에서 매니지드 지원.
- **pgmq**: Supabase 주도 message queue 익스텐션. pg_cron + Edge Function과 결합해 queue worker 구성.
- 출처: <https://thinhdanggroup.github.io/postgres-as-a-message-bus/>, <https://event-driven.io/en/push_based_outbox_pattern_with_postgres_logical_replication/>, <https://github.com/citusdata/pg_cron>, <https://dev.to/suciptoid/build-queue-worker-using-supabase-cron-queue-and-edge-function-19di>, <https://www.postgresql.org/docs/current/sql-notify.html>

## 9. FDW / CDC / 동기화

- `postgres_fdw` + 80+ FDW: 다른 PG, MySQL, Oracle, MongoDB, Kafka, ClickHouse, DuckDB까지 외부 테이블로.
- **Debezium PostgreSQL CDC**: pgoutput 또는 wal2json 사용. PG 12~18 지원. 17의 failover slot으로 standby 승격 후에도 끊김 없이 연결 가능.
- **pglogical**: 2ndQuadrant(현 EDB) 출신 logical replication 확장. 14 이후 내장 logical replication과 기능 중복이 많아 입지 축소.
- 출처: <https://www.tinybird.co/blog/postgres-cdc>, <https://docs.confluent.io/cloud/current/connectors/cc-postgresql-cdc-source-v2-debezium/cc-postgresql-cdc-source-v2-debezium.html>, <https://blog.sequinstream.com/a-developers-reference-to-postgres-change-data-capture-cdc/>

## 10. 분석 / OLAP

- **인덱스 + 윈도우 함수 + CUBE/ROLLUP + materialized view**가 기본 무기.
- **Citus**: 분산 PG 익스텐션. hash partition으로 분산 테이블 구성, co-located join 자동 라우팅. multi-tenant SaaS와 real-time analytics에 강함. Microsoft 인수 후 OSS 유지.
- **TimescaleDB**: 시계열 hypertable, 연속 집계, 압축 columnstore. 2.21에서 Hypercore TAM 폐기, 2.22(2025-09)에 sunset — 'native columnstore'로 통일.
- **Hydra**: Citus columnar의 fork+GTM 변형. ClickBench 분석 쿼리에서 PG 진영 최상위.
- **AlloyDB columnar engine**: 자동 row↔column 변환, 분석 쿼리 최대 100배. 39% Cloud SQL Enterprise Plus 대비 markup.
- **pg_duckdb / pg_analytics (ParadeDB)**: DuckDB 벡터 엔진을 PG 안에서 호출. TPC-DS 한 쿼리에서 1500배 가속 보고. Parquet/Iceberg/Delta 위 외부 테이블 분석.
- **ClickHouse vs PG**: 순수 컬럼 분석은 ClickHouse가 우세지만 PG는 OLTP+OLAP 혼합과 운영 단순성에서 유리.
- 출처: <https://thebuild.com/blog/2026/05/08/a-field-guide-to-alternative-storage-engines-for-postgresql/>, <https://www.tigerdata.com/blog/hypercore-a-hybrid-row-storage-engine-for-real-time-analytics>, <https://github.com/duckdb/pg_duckdb>, <https://motherduck.com/blog/pg-duckdb-release/>, <https://github.com/paradedb/pg_analytics>, <https://cloud.google.com/blog/products/databases/alloydb-for-postgresql-columnar-engine>, <https://github.com/citusdata/citus>, <https://blog.cloudflare.com/timescaledb-art/>, <https://blog.octabyte.io/topics/open-source-databases/clickhouse-vs-postgresql-analytics/>

## 11. API 백엔드

- **PostgREST**: 스키마에서 REST API 자동 생성. JWT 인증 후 PG role switch.
- **pg_graphql**: Supabase 작성. 스키마 reflect로 GraphQL endpoint.
- **Hasura**: PG·MySQL·SQL Server 등 멀티 DB 지원, GraphQL+REST+gRPC.
- **Supabase**: PostgREST + pg_graphql + Auth + Storage + Realtime + Edge Functions 번들.
- **RLS 패턴**: `app.current_tenant` 같은 세션 변수로 정책 작성, 애플리케이션 버그가 있어도 DB가 격리. 멀티테넌트 SaaS에 표준화.
- 출처: <https://supabase.com/docs/guides/api>, <https://supabase.com/docs/guides/database/extensions/pg_graphql>, <https://hasura.io/docs/2.0/databases/postgres/index/>, <https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/>, <https://www.thenile.dev/blog/multi-tenant-rls>

## 12. 확장 플랫폼

- `awesome-postgres`: 가장 큰 큐레이션 카탈로그.
- 2026 주목 익스텐션 리스트: TimescaleDB, PostgresML, PGroonga, pgvector, pgvectorscale, pg_partman, pg_cron, pg_repack, pg_squeeze, pgaudit, pgRouting, pg_anonymizer, pg_stat_monitor, pg_stat_statements.
- “PostgreSQL이 데이터베이스 세계를 먹어치우고 있다” — 핵심 메시지: PG의 진짜 차별점은 익스텐션 시스템과 ‘composability’. ClickBench에서 PG 자체는 x1050, 그러나 ParadeDB(pg_analytics)는 x10까지, 전용 OLAP은 x3~4. 즉 “Just Use Postgres”로 80% 케이스 해결.
- 출처: <https://github.com/dhamaniasad/awesome-postgres>, <https://pigsty.io/blog/pg/pg-eat-db-world/>, <https://aiven.io/blog/postgresql-extensions-you-need-to-know>, <https://www.tigerdata.com/blog/top-8-postgresql-extensions>

## 13. 클라우드 매트릭스

- **AWS RDS for PostgreSQL**: 가장 보편. 표준 PG 엔진 + 자동 백업.
- **AWS Aurora PostgreSQL**: 로그 구조 분산 스토리지(redo log replication 6 copies, 3 AZ). RDS 대비 20% 비싸지만 throughput당 가격에서 우위. PG 호환이지만 진짜 PG는 아님(스토리지 다름).
- **GCP Cloud SQL for PostgreSQL**: 단순 매니지드.
- **GCP AlloyDB**: 컬럼 엔진 + ML 기반 자동 튜닝. Cloud SQL Enterprise Plus 대비 39% premium.
- **Azure Database for PostgreSQL**: Flexible Server가 표준.
- **Supabase**: PG + Auth + Storage + Realtime + Edge Functions. 무료 티어 500MB DB, 50K MAU.
- **Neon**: serverless PG, compute/storage 분리, branching. 가격 인하: compute $0.106/CU-h, storage $0.35/GB-mo. 개발/CI 환경에 적합.
- **Crunchy Bridge**: AWS/GCP/Azure/Heroku, $10/mo부터. HA·PITR 기본.
- **Tembo**: dev-first, 익스텐션 마켓플레이스, K8s operator.
- **Xata**: Postgres 성능에 집중, Aurora 대비 80% 가격당 성능 우위 주장.
- 출처: <https://dev.to/philip_mcclarence_2ef9475/best-postgresql-hosting-in-2026-rds-vs-supabase-vs-neon-vs-self-hosted-5fkp>, <https://vela.simplyblock.io/neon-vs-supabase/>, <https://cloud.google.com/products/alloydb>, <https://www.crunchydata.com/products/crunchy-bridge>, <https://xata.io/postgres-performance>, <https://seenode.com/blog/top-managed-postgresql-services-compared>

## 14. DBA 운영

- **VACUUM/Autovacuum**: 기본 트리거 50 + 0.2*table_rows. 1억 row 테이블이면 2천만 dead tuple까지 대기 — 너무 늦음. 대량 테이블은 200만 row 기준 등으로 lower threshold. WAL 파라미터(`wal_buffers`, `min/max_wal_size`)도 튜닝 필수.
- **XID wraparound**: 7.5개월이면 위험. 실제 production incident — DBA가 합류한지 한 달만에 일부 테이블에서 autovacuum 비활성, wraparound protection mode로 read-only 전환. 수동 `VACUUM FREEZE` + long-running tx 종료로 복구.
- **백업**:
  - `pg_basebackup`: 내장, 단일 클러스터/소규모.
  - **pgBackRest**: production de facto. full/diff/incremental, 다중 TB 검증.
  - **Barman**: EDB. multi-server 중앙 관리, S3/Azure/GCS 지원.
  - **WAL-G**: Go, object storage 기반 cloud-native, 병렬 backup/restore.
- **HA**:
  - **Patroni**: etcd/Consul/ZooKeeper + REST API. 대규모/자동화 환경 표준.
  - **pg_auto_failover**: monitor 1대로 단순, 그러나 monitor가 SPoF.
  - 베스트 프랙티스: 동기 streaming + 최소 3노드 + 분기별 페일오버 훈련.
- **Connection pooling**: PgBouncer가 표준, Pgcat이 멀티스레드+read/write split으로 추격, Odyssey가 엔터프라이즈 라인. transaction pooling이 가장 흔하지만 prepared statement·advisory lock 사용 시 session pooling 강제.
- **모니터링**: `pg_stat_statements`(누적), `pg_stat_activity`(실시간), `pg_stat_user_tables`(테이블 헬스), Percona `pg_stat_monitor`(통합). postgres_exporter + Prometheus가 흔한 조합.
- 출처:
  - Vacuum: <https://www.snowflake.com/en/engineering-blog/tuning-postgres-vacuum/>, <https://www.percona.com/blog/tuning-autovacuum-in-postgresql-and-autovacuum-internals/>
  - XID: <https://www.sqlservercentral.com/articles/i-too-have-a-production-story-a-downtime-caused-by-postgres-transaction-id-wraparound-problem>, <https://news.ycombinator.com/item?id=47819305>
  - Backup: <https://thebuild.com/blog/2026/04/30/after-pgbackrest/>, <https://dev.to/piteradyson/postgresql-backup-tools-comparison-databasus-wal-g-pgbackrest-and-barman-2kg>
  - HA: <https://github.com/patroni/patroni>, <https://dohost.us/index.php/2025/10/02/automating-failover-with-pg_auto_failover-or-patroni-introduction/>
  - Pool: <https://onidel.com/blog/postgresql-proxy-comparison-2025>
  - Monitor: <https://severalnines.com/blog/query-observability-and-performance-tuning-with-pg_stat_monitor-and-pg_stat_statements/>
  - Bloat 도구: <https://boringsql.com/posts/the-bloat-busters-pg-repack-pg-squeeze/>

## 15. 성능 튜닝

- **인덱스 종류**: B-tree(기본·정렬·범위), Hash(equality만, 큰 값에 유리), GIN(JSONB·array·tsvector), GiST(공간·범위·근접), SP-GiST(비균형 트리·trie), BRIN(자연 정렬된 거대 테이블).
- **EXPLAIN ANALYZE**: estimate vs actual 차이가 크면 통계 부정확/플랜 부적절. Gather/Gather Merge 노드 부재 시 병렬 미사용 의심.
- **흔한 함정**: 인덱스 컬럼을 함수로 감싸기(`lower(email)=...`), 암시적 캐스트, 통계 갱신 누락, `max_connections` 과대 설정, vacuum 무시.
- **parallel query**: `max_parallel_workers_per_gather` 올려도 small table·non-parallelizable function이면 직렬 실행. EXPLAIN VERBOSE로 확인.
- 출처: <https://www.crunchydata.com/blog/get-started-with-explain-analyze>, <https://www.enterprisedb.com/blog/postgresql-query-optimization-performance-tuning-with-explain-analyze>, <https://dev.to/philip_mcclarence_2ef9475/postgresql-parallel-query-configuration-performance-tuning-1oih>, <https://neon.com/postgresql/indexes/index-types>, <https://www.postgresql.org/docs/current/indexes-types.html>

## 16. Partitioning

- 10부터 declarative partitioning. Range/List/Hash. 17부터 partition pruning 추가 개선.
- **pg_partman 5.x**: trigger 방식 제거, declarative만. 시간/시리얼 기반 자동 child 추가·삭제, BGW로 외부 스케줄러 불필요. RDS도 공식 지원.
- 출처: <https://github.com/pgpartman/pg_partman>, <https://www.percona.com/blog/postgresql-partitioning-made-easy-using-pg_partman-timebased/>, <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL_Partitions.html>

## 17. 벤치마크 (버전간)

- pgbench.github.io 자동 측정: PG16 ~2923 TPS, PG17 ~2991, PG18 ~3011 (단순 TPC-B 유사).
- HammerDB TPC-C에서 17.7 대비 18이 더 낮은 TPM이 관찰된다는 토론 — 회귀 여부 확인 중.
- 출처: <https://pgbench.github.io/>, <https://github.com/TPC-Council/HammerDB/discussions/849>
