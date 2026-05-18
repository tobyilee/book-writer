# PostgreSQL 종합 바이블 — Phase 1 레퍼런스

리서치 일자: 2026-05-18.
대상 독자: MySQL을 오래 써온 베테랑 개발자/DBA/tech lead. PostgreSQL을 메인 DB로 본격 도입하려는 조직의 핵심 인력.
소스 구성: web(공식 문서·벤더 블로그·기술 매체) + papers(SIGMOD·VLDB·arXiv) + community(HN·Reddit·한국 기술 블로그·Korean PostgreSQL User Group).
출처 표기 규칙: 문장 끝에 `[web]`, `[paper]`, `[community]`. URL은 §8에 모아 둠.

---

## 1. 핵심 개념과 정의 — PostgreSQL 아키텍처의 진짜 모습

### 1.1 출생과 DNA

PostgreSQL은 Michael Stonebraker가 1986년 버클리에서 시작한 POSTGRES 프로젝트의 후예다(Stonebraker & Rowe, SIGMOD 1986) [paper]. Postgres95 → PostgreSQL로 이어진 academic origin이 오늘날의 풍부한 데이터 타입(array, range, jsonb, hstore, geometric, network, …)과 익스텐션 친화 설계의 뿌리다. ‘객체-관계형’이라는 표현은 마케팅이 아니라 이 역사적 사실의 결과다.

### 1.2 프로세스 모델 — 스레드가 아닌 fork

PostgreSQL은 스레드를 쓰지 않는다. postmaster가 클라이언트 접속마다 `fork()`로 backend process를 만든다 [web]. **1 connection = 1 OS process**. 이게 MySQL과 가장 먼저 부딪히는 차이다. MySQL은 thread-per-connection이므로 수천 커넥션이 비교적 싸지만, PG는 그렇게 두면 메모리·컨텍스트 스위치가 폭주한다. 그래서 PG에서 PgBouncer/Pgcat 같은 외부 풀러는 권장이 아니라 사실상 필수다 [web].

부속 백그라운드 프로세스:

- **Background Writer** — dirty buffer를 디스크로 천천히 흘림
- **Checkpointer** — checkpoint 시점에 모든 dirty page flush
- **WAL Writer** — WAL buffer → WAL file
- **WAL Archiver** — WAL을 archive_command로 외부에 복사
- **Autovacuum Launcher / Worker** — dead tuple 회수
- **Logger / Stats Collector / Replication Worker** — 기타

`shared_buffers`는 일반적으로 RAM의 25%를 권장. WAL buffer는 기본 shared_buffers의 1/32 정도(보통 16MB 한계) [web].

### 1.3 MVCC — append-only tuple versioning

PostgreSQL의 MVCC는 *“같은 테이블에 row의 새 버전을 하나 더 쓴다”*는 단순한 규칙이다 [web]. UPDATE가 들어오면 기존 row는 그대로 두고 `xmax`에 종료 트랜잭션 ID를 표시한 뒤, 새 row를 같은 테이블 페이지(가능하면)에 추가한다. 이 dead tuple을 회수하는 일이 VACUUM이다.

MySQL InnoDB는 다르게 한다. 클러스터 인덱스에는 항상 최신 버전만 두고, 이전 값은 별도의 **undo log**에 압축적으로 적어둔다 [web]. 결과적으로 PG는 VACUUM이 필수지만 MySQL은 purge thread가 자동 처리한다. 같은 “MVCC”라는 이름 아래 운영 부담이 완전히 다르다.

이 차이가 만드는 두 가지 비용:

1. **Table bloat** — dead tuple이 vacuum보다 빨리 쌓이면 데이터 페이지가 부풀고 캐시 효율이 떨어진다.
2. **Index amplification** — 새 row 위치를 가리키려면 모든 secondary index에도 새 entry가 들어간다.

Andy Pavlo는 이를 “PostgreSQL의 우리가 가장 싫어하는 부분”이라 못박았다 [paper]. Uber가 PG에서 MySQL로 회귀한 일화의 기술적 핵심이 바로 이 index amplification이었다 [paper].

### 1.4 HOT — MVCC 비용을 깎는 단일 최적화

PostgreSQL은 **Heap-Only Tuple(HOT)**로 이 비용의 큰 덩어리를 해결한다 [web][paper]. 두 조건이 맞으면 새 row 버전은 같은 페이지의 빈 공간에 들어가고, 인덱스 항목은 새로 만들지 않는다.

- 변경된 컬럼이 어떤 인덱스에도 속하지 않을 것
- 같은 페이지에 free space가 충분할 것

두 row는 ctid 체인으로 연결된다. 인덱스 페이지에는 첫 버전 row 포인터만 살아남는다 [web]. 즉 “인덱스 컬럼은 함부로 건드리지 말 것, 페이지 free space(fillfactor)를 의도적으로 남겨둘 것”이 PG 성능 튜닝의 깊은 격언이 되는 이유다.

### 1.5 WAL — 모든 것의 기록자

WAL(Write-Ahead Log)은 PG의 다른 모든 기능의 토대다. 복구, 스트리밍 복제, 논리적 복제, PITR 백업, CDC가 전부 WAL을 소비한다. PostgreSQL 17은 WAL writer의 메모리 사용을 줄이고 vacuum 메모리 관리를 다시 썼다 [web]. 18은 major upgrade 시에도 planner statistics를 보존해 업그레이드 직후의 성능 절벽을 완화한다 [web].

### 1.6 SSI — 진짜 직렬화 가능성

PG 9.1에서 도입된 **Serializable Snapshot Isolation**(Ports & Grittner, VLDB 2012) [paper]은 잠금 없이 서로 충돌하는 동시 트랜잭션을 탐지해 한쪽을 abort 시킨다. 금융·결제 시스템처럼 진짜 직렬화 가능성이 필요한 워크로드에서 PG가 선택되는 이론적 근거다.

---

## 2. MySQL 베테랑이 가장 먼저 만날 8가지 차이

MySQL을 오래 써온 사람이 PG로 옮기면 가장 먼저 부딪히는 지점들이다. 책 본문의 ‘진입점’ 역할.

| # | 차이 영역 | MySQL(InnoDB) | PostgreSQL |
|---|---|---|---|
| 1 | 동시성 모델 | thread-per-connection | process-per-connection (fork) [web] |
| 2 | MVCC 저장 | undo log + 클러스터 인덱스 in-place | append-only tuple versioning + VACUUM [web][paper] |
| 3 | 기본 인덱스 | 클러스터형 (PK가 곧 row 위치) | heap + 별도 인덱스, 클러스터링은 명시적 |
| 4 | 데이터 타입 | 표준 + JSON | 표준 + JSON + JSONB + array + range + hstore + 사용자 정의 |
| 5 | 트랜잭션 DDL | 거의 불가 | 대부분 트랜잭션 안에서 안전 |
| 6 | 시퀀스/PK | AUTO_INCREMENT | SEQUENCE + identity column (uuidv7도 18에서 내장) [web] |
| 7 | LIMIT/timezone | 자체 문법, 암묵적 처리 | 표준 SQL 따름 — 마이그레이션 시 모든 LIMIT/timezone 점검 필수 [community] |
| 8 | 확장성 | 플러그인 제한적 | extension system이 핵심 가치(PostGIS, pgvector, Citus, …) [web] |

마이그레이션 비용의 실제 사례 — 4억 row 마이그레이션에 6개월, 다운타임 18시간, 발견 버그 127개, LIMIT 절 전부 수정, timezone 차이로 47개 쿼리 깨짐 [community]. PG로 가는 길은 “DDL 변환”이 아니라 “쿼리 semantics 변환”이라는 말이 한국 velog 후기에서도 똑같이 나온다 [community].

**상충 관점:**
- **PG 옹호:** “PG는 정확성 → 기능 → 성능 순, MySQL은 그 반대” — PG가 복잡 쿼리·대용량 혼합 워크로드에서 우위 [community].
- **MySQL 옹호:** 극단적 write 집중 워크로드는 InnoDB가 여전히 유리. PG의 VACUUM 운영 부담이 작은 팀에 부담 [community][paper].
- **공통 합의:** 대부분 워크로드에서 성능 차이는 ±30% 이내. 진짜 선택지는 “데이터 타입 표현력 + 익스텐션 생태계” vs “운영 단순성” [web][community].

---

## 3. 9가지 활용 시나리오 — 깊이 있는 자료

### 3.1 RDB 정통: 트랜잭션·쿼리·SQL 표준

#### 개요
PG는 SQL 표준 준수가 모토. 윈도우 함수, CTE(WITH RECURSIVE), MERGE(15), JSON_TABLE(17), `RETURNING OLD/NEW`(18), temporal constraint(18) [web].

#### 핵심 기술
- 트랜잭션 DDL, SAVEPOINT
- SSI (진짜 직렬화 가능성) [paper]
- 윈도우/CTE/CUBE/ROLLUP
- MERGE + RETURNING, JSON_TABLE [web]

#### 도구·인용
- PostgreSQL 17 / 18 release notes [web]
- Andy Atkinson, *JSON_TABLE, MERGE with RETURNING, Updatable Views* [web]

### 3.2 JSON / 문서 DB 대체

#### 개요
JSONB는 binary 표현으로 저장. 키 기반 검색은 GIN 인덱스로 가속. 문서 DB의 80% 케이스를 PG에서 처리 가능 [web].

#### 핵심 기술
- `jsonb_path_ops` operator class (좁은 연산자 집합, 더 빠름)
- 부분 인덱스 / expression index (특정 키만 인덱싱)
- JSON_TABLE (17) — JSON을 SQL FROM 절 테이블로 펼치기

#### 한계와 상충
- GIN은 write overhead 큼 — 자주 갱신되는 거대 JSONB에 부적합 [web]
- 모든 JSONB 연산자가 GIN에 매핑되지 않음 → seq scan 폴백 발생 [web]
- 일부 워크로드는 1.25M row 이상에서 GIN이 seq scan보다 느려진다는 보고 — 확인 필요(워크로드 의존성 큼) [web]
- 관점 A: “JSON 워크로드 80%는 PG로 충분, MongoDB 운영 부담을 없앨 수 있다” [web][community]
- 관점 B: “복합 multi-key 인덱스(country_id + product_id + created_at)는 MongoDB가 더 깔끔, JSONB 갱신 부하가 큰 워크로드는 여전히 도큐먼트 DB가 유리” [web]

#### 도구·인용
- 공식 docs §8.14 [web], Crunchy Data, pganalyze, Sitepoint guides [web]

### 3.3 전문 검색 — Elasticsearch 없이 가기

#### 개요
PG 검색은 세 층:
1. **내장 tsvector/tsquery** — stemmer 기반 풀텍스트. 영문/유럽어에 충분 [web].
2. **pg_trgm** — trigram 유사도. fuzzy match에 좋지만 non-ASCII 처리에 제약(한국어 부적합) [web].
3. **PGroonga** — Groonga 기반, 한국어·일본어·중국어 zero-ETL 지원. Supabase에 공식 익스텐션으로 포함 [web].
4. **ParadeDB / pg_search (BM25)** — Tantivy 기반. PG-native 인덱스 access method. 1M row 기준 tsvector 대비 인덱싱 50초 단축, 랭킹 20배, ES와 비슷한 성능 [web].
5. **pg_textsearch (Tiger Data)** — 같은 BM25를 PG 페이지 위에 다르게 구현. 17 access method API 개선이 경쟁을 촉발 [web].

#### 한국어 시나리오
- 한국어 풀텍스트 검색을 PG로 한다면 첫 후보는 **PGroonga**. pg_trgm은 비라틴 처리 제약, 내장 FTS는 한국어 분석기 부재 [web].
- BM25 랭킹이 중요하면 PGroonga + pg_search 조합 검토.

#### 인용
- ParadeDB intro & docs [web], PGroonga 공식 [web], Tiger Data pg_textsearch [web]

### 3.4 GIS / 지도 — PostGIS

#### 개요
PostGIS는 사실상 OSS GIS 표준. GiST/SP-GiST 공간 인덱스, GEOMETRY/GEOGRAPHY 타입, ST_* 함수군. 좌표계(SRID), 토폴로지, 라우팅(pgRouting), 래스터까지.

#### 2025 production 사례
- **State Farm** — 허리케인·산불 대응 클레임 처리 플랫폼. AWS 위 PostGIS, 재난 시 자동 스케일 [web].
- **NIBIO 노르웨이** — 전국 토지이용 topology. 수백만 edge 공유 모델 [web].
- **Telkom Kenya** — 영업 영역(territory) 추적 + 라우팅 최적화 [web].
- 한국 velog 운영기 — 공간 쿼리 성능 이슈 → 인덱스/EXPLAIN으로 개선 [community].

#### 인용
- Snowflake PostGIS Day 2025 recap [web], Crunchy Data PostGIS performance [web], FOSS4G Europe 2025 talks [web].

### 3.5 벡터 / RAG 백엔드

#### 개요
**pgvector**: HNSW + IVFFlat. **pgvectorscale (Timescale/Tiger Data)**: DiskANN + Statistical Binary Quantization (SBQ) [web][paper].

#### 벤치마크
- pgvector HNSW: 5M 벡터 이하, 95% recall에서 p95 <20ms [web].
- pgvectorscale on 50M 벡터, 99% recall: **471 QPS**.
  - 같은 조건 Qdrant 41 QPS → **11.4배** [web].
  - p95 latency 28ms vs Pinecone 784ms, 비용 **75% 절감** [web].

#### 알고리즘 배경
- HNSW: Malkov & Yashunin, IEEE TPAMI 2020 (arXiv:1603.09320) [paper].
- DiskANN: Jayaram Subramanya et al., NeurIPS 2019 [paper].
- 서베이: arXiv:2310.14021 (Han et al.) [paper].

#### 의사결정 가이드
- ~10M 벡터 + 단일 필터: pgvector(+scale) 충분 [web][community].
- 10M+ 벡터 + 복잡 메타데이터 필터 + 높은 동시성: dedicated(Qdrant/Weaviate/Pinecone) 검토 [community].
- 2026 트렌드: dedicated vector DB → relational DB로 통합 [web].

### 3.6 이벤트 / 큐 / 실시간

#### 개요
PG는 메시지 버스로 쓸 수 있는 도구가 세 층 있다.

1. **LISTEN/NOTIFY** — 같은 채널에 LISTEN한 세션에 비동기 알림. 트랜잭션 커밋 시점에 발사. payload 8KB 한계, 영속성 없음 [web].
2. **logical decoding (wal2json, pgoutput)** — WAL을 외부에서 소비. Debezium 등이 사용. outbox/CDC 패턴 기반 [web].
3. **pg_cron + pgmq** — 스케줄링과 영속 큐. Supabase가 적극 도입 [web].

#### 패턴
- **Outbox + logical replication** — 비즈니스 테이블과 같은 트랜잭션에 outbox row 기록 → logical decoding으로 외부 push [web].
- **Just Use Postgres** — 중소 규모면 Kafka 도입 전 PG로 충분 [web].

#### 한국 사례
- 카카오 클린플랫폼 — PostgreSQL → Elasticsearch Kafka Connect CDC 파이프라인. wal2json/pgoutput 선택 근거는 본 라운드에서 원문 인용 못함(WebFetch 한계). 시리즈 존재만 확인 [community].

### 3.7 FDW / CDC / 동기화

#### 개요
- **postgres_fdw + 80+ FDW** — 다른 PG, MySQL, Oracle, Mongo, Kafka, ClickHouse, DuckDB까지 외부 테이블로.
- **Debezium PostgreSQL CDC** — pgoutput 또는 wal2json. PG 12~18 지원. 17의 failover slot으로 standby 승격 후에도 연결 유지 [web].
- **pglogical** — 14 이후 내장 logical replication과 기능 중복, 점차 입지 축소 [web].

#### 17 failover slot의 의미
17부터 logical replication slot이 standby로 동기화된다. 즉 primary가 죽고 standby가 승격해도 Debezium 같은 컨슈머의 슬롯이 살아 있다 [web]. 이전에는 페일오버 = CDC 파이프라인 재구축이었다.

### 3.8 분석 / OLAP / 시계열

#### 개요
PG가 ‘OLAP까지 다 한다’고 말할 수 있게 된 핵심은 컬럼 엔진과 분산 익스텐션.

- **윈도우 함수 + CUBE/ROLLUP + materialized view** — 기본 도구.
- **Citus** — hash partition 분산, co-located join 자동 라우팅. Microsoft 인수 후 OSS 유지 [web][paper].
- **TimescaleDB** — 시계열 hypertable, continuous aggregate, native columnstore. 2.21에서 Hypercore TAM 폐기, 2.22(2025-09)에 sunset — native columnstore로 통일 [web].
- **Hydra** — Citus columnar의 fork. ClickBench에서 PG 진영 최상위 [web].
- **AlloyDB columnar engine** (Google) — 자동 row↔column 변환. 분석 쿼리 최대 100배 [web].
- **pg_duckdb / pg_analytics (ParadeDB)** — DuckDB 벡터 엔진을 PG 안에서 호출. TPC-DS 한 쿼리에서 1500배 가속 보고 [web]. Parquet/Iceberg/Delta 외부 테이블 분석.

#### ClickBench 비교 (Pigsty 요약)
- 순수 PG: ~x1050
- 튜닝된 PG: x47
- ParadeDB(pg_analytics): x10
- ClickHouse/DuckDB: x3~4
- MySQL/MariaDB: x3000~19700 [web]

#### 상충 관점
- 관점 A: “순수 컬럼 분석은 ClickHouse가 빠르다. PG는 그쪽을 따라잡지 못한다.” [web]
- 관점 B: “OLTP + OLAP 혼합과 운영 단순성이라면 PG가 압도. ClickHouse를 별도 운영하지 않아도 80% 케이스 해결.” [web][community]

### 3.9 API 백엔드 — DB가 백엔드다

#### 개요
- **PostgREST** — 스키마에서 REST API 자동 생성. JWT 인증 후 PG role switch [web].
- **pg_graphql** — Supabase 작성. 스키마 reflect로 GraphQL endpoint [web].
- **Hasura** — 멀티 DB GraphQL/REST/gRPC, 큰 RBAC.
- **Supabase** — 위 셋 + Auth + Storage + Realtime + Edge Functions 번들 [web].

#### RLS 패턴 (멀티테넌트 SaaS)
- 모든 테이블에 `tenant_id` 1급 컬럼.
- 세션 변수 `app.current_tenant` 세팅.
- 정책: `USING (tenant_id = current_setting('app.current_tenant')::UUID)` [web].
- 효과: 애플리케이션 코드 버그가 있어도 DB가 격리한다. AWS Database blog가 multi-tenant SaaS 표준 패턴으로 정리 [web].

#### 운영 주의
- RLS 정책 자체가 plan에 들어가므로 EXPLAIN 시 정책 술어 확인 필수.
- admin bypass는 privilege보다 policy 기반이 감사 가능성 면에서 권장 [web].

---

## 4. 클라우드 PostgreSQL — 벤더 매트릭스

### 4.1 한눈에 보는 비교

| 벤더 / 서비스 | 정체성 | 차별 포인트 | 가격 / 비용 특이 | 주 사용 시나리오 |
|---|---|---|---|---|
| **AWS RDS for PostgreSQL** | 표준 매니지드 PG | 가장 보편, 익스텐션 다수, RDS Proxy | 인스턴스 기반 | 표준 OLTP, 마이그레이션 1순위 |
| **AWS Aurora PostgreSQL** | 분산 스토리지 PG-호환 | redo log를 6 copies/3 AZ 비동기 복제, fast crash recovery [paper] | RDS 대비 ~20% 비싸지만 throughput당 가격 우위 [web] | 대규모 OLTP, multi-AZ HA |
| **GCP Cloud SQL for PostgreSQL** | 표준 매니지드 | 단순함, GCP 통합 | 인스턴스 기반 | GCP 워크로드 표준 |
| **GCP AlloyDB** | PG + ML 기반 자동 튜닝 + 컬럼 엔진 | 분석 쿼리 최대 100배 [web] | Cloud SQL Enterprise Plus 대비 +39% [web] | HTAP, 분석 혼합 |
| **Azure Database for PostgreSQL (Flexible)** | 표준 매니지드 | Azure 생태계 통합 | 인스턴스 기반 | Azure 워크로드 |
| **Supabase** | PG + 풀스택 BaaS | PostgREST + pg_graphql + Auth + Storage + Realtime + Edge Functions | 무료 티어 500MB DB, 50K MAU [web] | 풀스택 빠른 출시, BaaS |
| **Neon** | 서버리스 PG | compute/storage 분리, branching | Compute $0.106/CU-h, Storage $0.35/GB-mo (인하 후) [web] | 개발/CI 환경, 가변 트래픽 |
| **Crunchy Bridge** | 모던 매니지드 PG | HA·PITR 기본, multi-cloud | $10/mo부터 [web] | 익스텐션 풍부한 표준 PG |
| **Tembo** | dev-first PG | 익스텐션 마켓플레이스, K8s operator | 인스턴스 기반 | 익스텐션 활용 극대화 |
| **Xata** | PG 성능 특화 | Aurora 대비 가격당 성능 ~80% 우위 주장 [web] | 트래픽 기반 | 비용 민감 워크로드 |

### 4.2 선택 가이드 (요지)

- “PG 그대로, 마이그레이션 단순”: **RDS** 또는 **Crunchy Bridge** [web].
- “write 처리량 + HA + 멀티 AZ”: **Aurora** [paper][web]. 단, Aurora는 PG-호환이지 진짜 PG 코어가 아니라는 점 유의 — SIGMOD 2024 OpenAurora 평가가 disaggregated storage의 latency 특성을 정량화 [paper].
- “분석 + OLTP 혼합”: **AlloyDB** (자동 columnar) [web] 또는 RDS + pg_duckdb [web].
- “브랜칭, 가변 트래픽”: **Neon** [web].
- “풀스택 BaaS”: **Supabase** [web].
- “익스텐션을 정말 많이 쓸 거다”: **Tembo** 또는 **Crunchy Bridge** [web].

### 4.3 함정과 상충

- Aurora의 “PG-호환”은 마케팅에 가까운 비유. 진짜 PG core와 다른 스토리지, 다른 wraparound 특성. 운영 노하우를 그대로 옮기지 말 것 [paper][community].
- 매니지드 PG의 “지원하는 익스텐션 목록”이 결정적 — 평가 단계에서 PGroonga, pg_search, pgvectorscale, pg_partman, pg_cron 지원 여부를 반드시 확인 [web].
- Supabase는 PG 위 풀스택이라 좋지만 lock-in 면이 있다(Edge Function, Auth). 풀스택 가치 vs 표준 PG 가치를 저울질해야 [community].

---

## 5. DBA 운영 노하우 정수

### 5.1 VACUUM / Autovacuum

- 기본 트리거: `autovacuum_vacuum_threshold(50)` + `autovacuum_vacuum_scale_factor(0.2) × n_rows` [web].
- 1억 row 테이블이면 2천만 dead tuple까지 기다림 → 너무 늦다. 대량 테이블은 200만 row 기준으로 lower scale factor 권장 [web].
- 모니터링: `pg_stat_user_tables.n_dead_tup`, `last_autovacuum`, `n_mod_since_analyze`. `vacuum_cost_*`로 I/O 압박 조절 [web].

### 5.2 XID wraparound — 진짜로 멈춘다

7.5개월이면 wraparound 위험 진입. 실제 사례: DBA 합류 한 달 만에 일부 테이블 autovacuum 비활성 → wraparound protection mode → 전체 클러스터 read-only [community][web]. 복구는 수동 `VACUUM FREEZE` + long-running tx 종료. 사전 예방:

- `pg_stat_all_tables.relfrozenxid`와 `age(relfrozenxid)` 모니터링
- 절대 autovacuum을 꺼두지 말 것 (꼭 꺼야 한다면 명시적 freeze schedule 운영)
- AWS는 `postgres_get_av_diag()`로 autovacuum 진단 권장 [web]

### 5.3 Bloat 처리

- 평시: autovacuum 튜닝으로 충분.
- 누적 후: **VACUUM FULL**은 exclusive lock 필요(다운타임).
- 무중단: **pg_repack**(외부 카피 + trigger 동기화 + 짧은 swap lock) [web], **pg_squeeze**(BGW + logical decoding으로 자동 재구성, 임계치 모니터링) [web].
- 운영 패턴: 자동 정리는 pg_squeeze, 일회성 큰 회수는 pg_repack [web].

### 5.4 WAL과 백업

| 도구 | 강점 | 약점 | 적합 |
|---|---|---|---|
| `pg_basebackup` | 내장, 검증됨 | 대규모/PITR 운영성 부족 | 소규모 단일 클러스터 [web] |
| **pgBackRest** | full/diff/incremental, multi-TB 검증, 사실상 표준 | 설정 학습곡선 | 프로덕션 표준 [web] |
| **Barman** | EDB 산하, multi-server 중앙관리, S3/Azure/GCS | 일부 시나리오에서 성능 한계 | 다중 서버 백업 호스트 [web] |
| **WAL-G** | Go, object storage 친화, 병렬 backup/restore | 일부 엔터프라이즈 기능 부재 | 클라우드 네이티브 [web] |

PITR가 필요하면 pgBackRest가 안전한 첫 선택, 클라우드 네이티브면 WAL-G가 가볍다 [web].

### 5.5 HA — Patroni vs pg_auto_failover

- **Patroni**: etcd/Consul/ZK + REST API. 대규모·자동화 환경에 표준. 가장 풍부한 기능 [web].
- **pg_auto_failover**: monitor 1대로 단순. 다만 monitor가 SPoF [web].
- 베스트 프랙티스: 동기 streaming, 최소 3노드(primary + 2 standby), 분기별 페일오버 훈련, PgBouncer/HAProxy로 라우팅, `/primary` health check [web].
- 17 failover slot 도입으로 logical replication도 HA 안에서 연속성 확보 [web].

### 5.6 Connection pooling

- **PgBouncer**: 표준. session/transaction/statement 모드. 시작 풀 사이즈 20~30(OLTP).
- **Pgcat**: 멀티스레드, read/write split, 모던 클라우드 환경 강함 [web].
- **Odyssey**: Yandex, 엔터프라이즈 라인 [web].
- 함정: transaction pooling은 prepared statement, advisory lock, SET LOCAL이 부서질 수 있다. 그런 워크로드는 session 풀로.

### 5.7 모니터링 / 옵저버빌리티

- **pg_stat_statements** — 누적 쿼리 통계(정규화). 가장 먼저 켜야 할 익스텐션 [web].
- **pg_stat_activity** — 실시간 세션 스냅샷. 락 분석.
- **pg_stat_user_tables / pg_stat_user_indexes** — 테이블 헬스, 인덱스 사용도.
- **pg_stat_monitor (Percona)** — pg_stat_statements + activity + auto_explain 통합 [web].
- 노출: `postgres_exporter` → Prometheus → Grafana. 클라우드면 RDS Performance Insights, AlloyDB System Insights 등 벤더 도구 활용 [web].

---

## 6. 성능 튜닝 정수

### 6.1 인덱스 종류 — 언제 무엇을

| 종류 | 적합 | 부적합 |
|---|---|---|
| **B-tree** | equality, range, sort, IS NULL — 기본 선택 [web] | 다값 컬럼 |
| **Hash** | equality only, 큰 값(예: 긴 문자열) [web] | 범위/정렬 |
| **GIN** | JSONB, array, tsvector — 다값 컬럼 [web] | 자주 갱신되는 큰 컬럼 |
| **GiST** | 공간(PostGIS), 범위 타입, KNN 근접 검색 [web] | equality 위주 |
| **SP-GiST** | 비균형 구조(quadtree, k-d, trie) — phone routing, IP, GIS [web] | 일반 OLTP |
| **BRIN** | 자연 정렬된 거대 테이블(time-series 등) [web] | 무작위 분포 |

### 6.2 EXPLAIN ANALYZE 읽기

- **estimate vs actual**: 차이가 크면 통계 부정확. `ANALYZE` 실행, `default_statistics_target` 상향, 컬럼별 stats target 검토 [web].
- **Gather/Gather Merge** 노드 부재면 병렬 미사용. `max_parallel_workers_per_gather` 점검 [web].
- **Buffers**: shared hit/read 비율로 캐시 효율 평가 (`EXPLAIN (ANALYZE, BUFFERS)`).

### 6.3 흔한 함정

- 인덱스 컬럼을 함수로 감싸기 (`lower(email) = '...'`) → 표현식 인덱스 필요 [web].
- 암시적 캐스트 (`varchar_col = 123`) → 인덱스 무효 [web].
- `max_connections` 과대 설정 → 메모리/스케줄링 폭주. 풀러로 해결.
- HOT update 깨지는 컬럼만 자주 갱신 → fillfactor 90→70 등 조정.
- 통계 갱신 누락 — 대량 입수 후 즉시 `ANALYZE`.

### 6.4 Parallel query

- 작은 테이블·non-parallelizable function이면 직렬 실행이 더 빠르다는 판단을 PG가 한다. `EXPLAIN VERBOSE`로 확인 [web].
- 17부터 일부 인덱스 쿼리 병렬 개선 [web].

### 6.5 Partitioning

- 10부터 declarative partitioning(Range/List/Hash). 17부터 partition pruning 추가 개선 [web].
- **pg_partman 5.x** — trigger 제거, declarative만. 시간/시리얼 기반 자동 child 생성·삭제, BGW로 외부 스케줄러 불필요. RDS 공식 지원 [web].
- 패턴: time-series는 monthly/daily range partition + BRIN 인덱스 + pg_partman 자동 retention.

### 6.6 버전간 벤치마크

- pgbench.github.io 자동 측정 — PG16 ~2923 TPS, PG17 ~2991, PG18 ~3011 (단순 TPC-B 유사) [web].
- HammerDB TPC-C에서 18이 17.7보다 낮은 TPM 회귀 가능성 토론 — 확인 필요 [web].

---

## 7. 한국 사례와 커뮤니티 논쟁점

### 7.1 한국 사용자 모임

- **PostgreSQL Korea (postgresql.kr)** — 공식 한국 커뮤니티. PGDay.Seoul 시리즈 (2019, 2024 등) [community].
- **PostgreSQL-Korea/pgdoc-kr (GitHub)** — 한국어 매뉴얼 번역 [community].
- **SKAI Worldwide** (前 비트나인 그룹) — 한국 PG 전문기업, 강점·오라클 사용자 가이드·커뮤니티 버전 기술지원 시리즈 [community].
- **PGTS (비트나인)** — 한국 상용 PG 기술지원 [community].

### 7.2 한국 마이그레이션 후기

- Velog @melon03090 — Oracle → PG 공공 시스템. 핵심 통증은 SQL semantics 변환(`DECODE`, `(+)` 외부 조인, `CONNECT BY`)이 DDL보다 훨씬 어렵다 [community].
- Velog @peace_e — MySQL → PG 사이드 프로젝트. JSONB와 인덱스 표현력이 동기 [community].
- 맞추다 팀 블로그(@Julie, Medium) — MySQL → PG, array 타입을 쓰기 위해 전환 [community].
- iting.co.kr — re:Invent 2025 정리: Oracle → Aurora PG 마이그레이션 가이드. AWS DMS, Babelfish, SCT [community].

### 7.3 한국 기업 사례

- **카카오 클린플랫폼 (tech.kakao.com)** — PG → Elasticsearch Kafka Connect CDC 파이프라인 시리즈. 본문 인용 보강 필요 [community].
- **카카오스타일 (AWS Korea 블로그)** — Amazon Bedrock 기반 생성형 AI. PG 위 분석 자산을 LLM이 활용하는 패턴 [community].
- **당근페이 (AWS Korea 블로그)** — BroQuery(Text-to-SQL) on Bedrock. 데이터 분석 자가서비스 [community].
- **컴퓨터월드 기고** — “오픈소스 DB 전성시대, PG를 선택해야 하는 이유”. 2024 StackOverflow 49% 1위, 2년 연속 가장 많이 쓰는 DB 1위 [community].
- **다음 뉴스 (2026-01)** — “오라클 중심 DB 시장에 균열…포스트그레SQL이 만든 변화”. 공공/금융/제조/플랫폼 신규 시스템 채택 가속 [community].

### 7.4 커뮤니티 논쟁점

#### 논쟁 A: “Just Use Postgres” 단순화 논쟁
- 옹호: Vonng의 “Postgres is eating the database world”. ClickBench·SaaS 트렌드 근거. MySQL+Kafka+RabbitMQ+ES+Mongo+Redis → PG 하나로 [web][community].
- 반론: throughput 한계 워크로드(Kafka 같은 100MB/s+ 메시지), 검색 품질(ES와 비교), 일부 컬럼 분석(ClickHouse)에서는 dedicated가 여전히 우위 [community].
- 공통 합의: 익스텐션 composability가 PG의 진짜 moat. ClickBench에서 순수 PG는 x1050이지만 pg_analytics + DuckDB 결합으로 x10까지 [web].

#### 논쟁 B: MVCC vs 운영 부담
- 옹호: append-only가 long-running read에 강하다(보고 트랜잭션 친화) [paper].
- 비판: Andy Pavlo 4가지 — 전체 row 복제, table bloat, index amplification, autovacuum 튜닝 난이도 [paper]. Uber의 PG → MySQL 회귀가 대표 사례.
- 완화책: HOT, fillfactor 조정, autovacuum 적극 튜닝, pg_repack/pg_squeeze로 reclaim, 17의 vacuum 메모리 개선 [web].

#### 논쟁 C: 벡터 DB 통합 vs dedicated
- 옹호: pgvectorscale이 Pinecone 대비 75% 저렴, Qdrant 11.4배. 데이터 소실 없이 OLTP와 동일 DB [web].
- 반론: 10M+ 벡터 + 복잡 filter + 높은 동시성은 dedicated 검토 [community].
- 트렌드: 2026은 통합 방향. relational + vector + search + analytics 통합이 디폴트 [web].

#### 논쟁 D: Aurora PG는 “진짜 PG인가”
- 옹호: PG-호환, 빠른 crash recovery, multi-AZ HA, throughput당 비용 우위 [paper][web].
- 비판: 스토리지가 다르므로 진짜 PG 운영 노하우(특히 vacuum, replication slot, extension)가 그대로 통하지 않음. SIGMOD 2024 OpenAurora의 정량적 평가 참고 [paper].
- 실용 관점: PG 핵심 익스텐션 지원 여부가 결정 — Aurora 지원 익스텐션 목록을 평가 단계에서 반드시 확인 [community].

---

## 8. 참고 문헌

### 8.1 PostgreSQL 공식 / 표준

- PostgreSQL 17 Released — <https://www.postgresql.org/about/news/postgresql-17-released-2936/>
- PostgreSQL 18 Released — <https://www.postgresql.org/about/news/postgresql-18-released-3142/>
- Release Notes 17.0 — <https://www.postgresql.org/docs/release/17.0/>
- Release Notes 18.0 — <https://www.postgresql.org/docs/release/18.0/>
- Datatype JSON/JSONB §8.14 — <https://www.postgresql.org/docs/current/datatype-json.html>
- Index Types §11.2 — <https://www.postgresql.org/docs/current/indexes-types.html>
- GIN Indexes §65.4 — <https://www.postgresql.org/docs/current/gin.html>
- Storage HOT §66.7 — <https://www.postgresql.org/docs/current/storage-hot.html>
- Routine Vacuuming §24.1 — <https://www.postgresql.org/docs/current/routine-vacuuming.html>
- Cumulative Statistics System §27.2 — <https://www.postgresql.org/docs/current/monitoring-stats.html>
- pg_trgm §F.35 — <https://www.postgresql.org/docs/current/pgtrgm.html>
- Logical Replication §29 — <https://www.postgresql.org/docs/current/logical-replication.html>
- Logical Replication Failover §29.3 — <https://www.postgresql.org/docs/current/logical-replication-failover.html>
- LISTEN/NOTIFY — <https://www.postgresql.org/docs/current/sql-notify.html>, <https://www.postgresql.org/docs/current/sql-listen.html>
- EXPLAIN — <https://www.postgresql.org/docs/current/sql-explain.html>
- pgbench — <https://www.postgresql.org/docs/current/pgbench.html>
- JSON Functions §9.16 — <https://www.postgresql.org/docs/current/functions-json.html>
- Wiki: Serializable — <https://wiki.postgresql.org/wiki/Serializable>
- Wiki: Monitoring — <https://wiki.postgresql.org/wiki/Monitoring>

### 8.2 학술 (SIGMOD / VLDB / NeurIPS / arXiv)

- Wu et al., “An Empirical Evaluation of In-Memory MVCC,” PVLDB 10, 2017 — <https://www.vldb.org/pvldb/vol10/p781-Wu.pdf>
- Freitag et al., MVCC evaluation, PVLDB 15, 2022 — <https://www.vldb.org/pvldb/vol15/p2797-freitag.pdf>
- Cubukcu et al., “Citus: Distributed PostgreSQL for Data-Intensive Applications,” SIGMOD 2021 — <https://dl.acm.org/doi/pdf/10.1145/3448016.3457551>
- Verbitski et al., “Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases,” SIGMOD 2017 — <https://web.stanford.edu/class/cs245/readings/aurora.pdf>
- Verbitski et al., “Amazon Aurora: On Avoiding Distributed Consensus,” SIGMOD 2018 — <https://pages.cs.wisc.edu/~yxy/cs839-s20/papers/aurora-sigmod-18.pdf>
- Wang et al., “Understanding the Performance Implications of Storage-Disaggregated Database Design (OpenAurora),” SIGMOD 2024 — <https://www.cs.purdue.edu/homes/csjgwang/pubs/SIGMOD24_OpenAurora.pdf>
- Malkov & Yashunin, “HNSW,” IEEE TPAMI 2020 — arXiv:1603.09320
- Jayaram Subramanya et al., “DiskANN,” NeurIPS 2019
- Han et al., “Survey of Vector DBMS,” arXiv:2310.14021
- “Worst-case Performance of Popular ANN,” arXiv:2310.19126
- “Towards Robustness: Critique of Vector DB Assessments,” arXiv:2507.00379
- Pavlo, “The Part of PostgreSQL We Hate the Most,” CMU blog 2023 — <https://www.cs.cmu.edu/~pavlo/blog/2023/04/the-part-of-postgresql-we-hate-the-most.html>

### 8.3 클라우드 벤더 공식

- AWS RDS PostgreSQL — <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/...>
- AWS Aurora PostgreSQL parameters — <https://aws.amazon.com/blogs/database/amazon-aurora-postgresql-parameters-part-2-replication-security-and-logging/>
- AWS pg_partman 가이드 — <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL_Partitions.html>
- AWS pg_repack 가이드 — <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.pg_repack.html>
- AWS Multi-tenant RLS — <https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/>
- AWS Multixacts — <https://aws.amazon.com/blogs/database/multixacts-in-postgresql-usage-side-effects-and-monitoring/>
- AWS pg_cron — <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL_pg_cron.html>
- AWS postgres_get_av_diag — <https://aws.amazon.com/blogs/database/prevent-transaction-id-wraparound-by-using-postgres_get_av_diag-for-monitoring-autovacuum/>
- GCP AlloyDB overview — <https://cloud.google.com/alloydb/docs/overview>
- GCP AlloyDB columnar engine — <https://cloud.google.com/blog/products/databases/alloydb-for-postgresql-columnar-engine>
- GCP AlloyDB columnar docs — <https://docs.cloud.google.com/alloydb/docs/columnar-engine/about>
- Azure Release Notes — <https://learn.microsoft.com/en-us/azure/postgresql/release-notes/release-notes>

### 8.4 매니지드 PG / 벤더 블로그

- Supabase RLS·API·Auth — <https://supabase.com/docs/guides/api>, <https://supabase.com/docs/guides/database/extensions/pg_graphql>, <https://supabase.com/docs/guides/database/extensions/pgroonga>, <https://supabase.com/docs/guides/api/securing-your-api>
- Supabase Data APIs 글 — <https://supabase.com/blog/simplify-backend-with-data-api>
- Neon HNSW guide — <https://neon.com/blog/understanding-vector-search-and-hnsw-index-with-pgvector>
- Neon pg_search — <https://neon.com/docs/extensions/pg_search>
- Neon index types — <https://neon.com/postgresql/indexes/index-types>
- Crunchy Bridge 소개 — <https://www.crunchydata.com/products/crunchy-bridge>, <https://www.crunchydata.com/pricing>
- Crunchy: JSONB indexing — <https://www.crunchydata.com/blog/indexing-jsonb-in-postgres>
- Crunchy: PostGIS performance — <https://www.crunchydata.com/blog/postgis-performance-indexing-and-explain>
- Crunchy: EXPLAIN ANALYZE — <https://www.crunchydata.com/blog/get-started-with-explain-analyze>
- Crunchy: XID wraparound — <https://www.crunchydata.com/blog/managing-transaction-id-wraparound-in-postgresql>
- Tiger Data (TimescaleDB): pgvector vs Pinecone — <https://www.tigerdata.com/blog/pgvector-is-now-as-fast-as-pinecone-at-75-less-cost>
- Tiger Data: pgvector vs Qdrant — <https://www.tigerdata.com/blog/pgvector-vs-qdrant>
- Tiger Data: Hypercore 하이브리드 엔진 — <https://www.tigerdata.com/blog/hypercore-a-hybrid-row-storage-engine-for-real-time-analytics>
- Tiger Data: pg_textsearch — <https://www.tigerdata.com/blog/pg-textsearch-bm25-full-text-search-postgres>, <https://www.tigerdata.com/blog/introducing-pg_textsearch-true-bm25-ranking-hybrid-retrieval-postgres>
- Tiger Data: BM25 in Postgres — <https://www.tigerdata.com/blog/you-dont-need-elasticsearch-bm25-is-now-in-postgres>
- ParadeDB intro — <https://www.paradedb.com/blog/introducing-search>, <https://github.com/paradedb/paradedb>, <https://docs.paradedb.com/welcome/introduction>
- ParadeDB BM25 learn — <https://www.paradedb.com/learn/search-in-postgresql/bm25>
- ParadeDB hybrid search — <https://www.paradedb.com/blog/hybrid-search-in-postgresql-the-missing-manual>
- ParadeDB pg_analytics — <https://github.com/paradedb/pg_analytics>
- MotherDuck: pg_duckdb 1.0 — <https://motherduck.com/blog/pg-duckdb-release/>
- MotherDuck: Postgres+DuckDB methods — <https://motherduck.com/blog/postgres-duckdb-options/>
- DuckDB pg_duckdb repo — <https://github.com/duckdb/pg_duckdb>
- Pigsty: Postgres is eating the database world — <https://pigsty.io/blog/pg/pg-eat-db-world/>
- Pigsty extension catalog — <https://pigsty.io/ext/>
- The Build (Christophe Pettus): Aurora 매니지드 평가 — <https://thebuild.com/blog/2026/05/05/managed-postgres-examined-amazon-aurora-postgresql/>
- The Build: Alternative storage engines field guide — <https://thebuild.com/blog/2026/05/08/a-field-guide-to-alternative-storage-engines-for-postgresql/>
- The Build: After pgBackRest — <https://thebuild.com/blog/2026/04/30/after-pgbackrest/>
- PGroonga 공식 — <https://pgroonga.github.io/>, <https://pgroonga.github.io/reference/pgroonga-versus-textsearch-and-pg-trgm.html>
- pg_squeeze — <https://www.cybertec-postgresql.com/en/products/pg_squeeze/>
- pg_partman repo — <https://github.com/pgpartman/pg_partman>
- pg_cron repo — <https://github.com/citusdata/pg_cron>
- Citus repo — <https://github.com/citusdata/citus>
- Patroni repo — <https://github.com/patroni/patroni>
- HammerDB — <https://www.hammerdb.com/>
- pgbench 비교 — <https://pgbench.github.io/>
- awesome-postgres — <https://github.com/dhamaniasad/awesome-postgres>

### 8.5 운영·벤치마크 매체

- Percona: autovacuum tuning — <https://www.percona.com/blog/tuning-autovacuum-in-postgresql-and-autovacuum-internals/>
- Percona: PostGIS — <https://www.percona.com/blog/working-with-geospatial-data-postgis-makes-postgresql-enterprise-ready/>
- Percona: pgBouncer — <https://www.percona.com/blog/pgbouncer-for-postgresql-how-connection-pooling-solves-enterprise-slowdowns/>
- Snowflake: PostGIS Day 2025 recap — <https://www.snowflake.com/en/engineering-blog/postgis-day-2025-recap/>
- Snowflake: VACUUM 튜닝 — <https://www.snowflake.com/en/engineering-blog/tuning-postgres-vacuum/>
- Severalnines: pg_stat_monitor 통합 — <https://severalnines.com/blog/query-observability-and-performance-tuning-with-pg_stat_monitor-and-pg_stat_statements/>
- Severalnines: HA 비교 — <https://severalnines.com/blog/...>, pgBackRest vs Barman — <https://severalnines.com/blog/automating-backups-and-disaster-recovery-in-postgresql-at-scale-pgbackrest-vs-barman/>
- Aiven: Postgres extensions 2025 — <https://aiven.io/blog/postgresql-extensions-you-need-to-know>
- Aiven: 텍스트 검색 — <https://aiven.io/blog/different-ways-to-search-text-in-postgresql>
- Cloudflare: TimescaleDB analytics — <https://blog.cloudflare.com/timescaledb-art/>
- Tinybird: Postgres CDC guide — <https://www.tinybird.co/blog/postgres-cdc>
- Sequinstream: PG CDC reference — <https://blog.sequinstream.com/a-developers-reference-to-postgres-change-data-capture-cdc/>
- Decodable: PG 17 failover slots — <https://www.decodable.co/blog/failover-replication-slots-with-postgres-17>
- pgEdge: PG 17 logical replication features — <https://www.pgedge.com/blog/logical-replication-features-in-pg-17>
- OctaByte: ClickHouse vs PG 분석 — <https://blog.octabyte.io/topics/open-source-databases/clickhouse-vs-postgresql-analytics/>
- onidel: PgBouncer vs Pgcat vs Odyssey 2025 — <https://onidel.com/blog/postgresql-proxy-comparison-2025>
- boringSQL: pg_repack vs pg_squeeze — <https://boringsql.com/posts/the-bloat-busters-pg-repack-pg-squeeze/>
- boringSQL: HOT updates — <https://boringsql.com/posts/hot-updates/>
- thinhdanggroup: Postgres as message bus — <https://thinhdanggroup.github.io/postgres-as-a-message-bus/>
- Event-driven.io: Outbox + logical — <https://event-driven.io/en/push_based_outbox_pattern_with_postgres_logical_replication/>
- Confluent: PG CDC v2 — <https://docs.confluent.io/cloud/current/connectors/cc-postgresql-cdc-source-v2-debezium/cc-postgresql-cdc-source-v2-debezium.html>
- Postgres Pro: MVCC 시리즈 — <https://postgrespro.com/blog/pgsql/5967910>

### 8.6 한국 자료

- PostgreSQL Korea 공식 — <https://postgresql.kr/>
- PGDay.Seoul 2024 — <https://pgday.postgresql.kr/>
- pgdoc-kr — <https://github.com/PostgreSQL-Korea/pgdoc-kr>
- SKAI 블로그(MySQL/Oracle 비교, 커뮤니티 버전 기술지원, 오라클 사용자 가이드) — <https://blog.skaiworldwide.com/516>, <https://blog.skaiworldwide.com/550>, <https://blog.skaiworldwide.com/589>, <https://blog.skaiworldwide.com/616>
- 비트나인 PGTS — <https://bitnine.net/pgts/>
- 카카오 클린플랫폼 PG→ES CDC — <https://tech.kakao.com/posts/776>
- AWS Korea: 카카오스타일 Bedrock — <https://aws.amazon.com/ko/blogs/tech/kakaostyle-leverage-genai-with-amazon-bedrock/>
- AWS Korea: 당근페이 BroQuery — <https://aws.amazon.com/ko/blogs/tech/daangnpay-text-to-sql-1/>
- iting.co.kr: re:Invent 2025 Oracle→Aurora PG — <https://iting.co.kr/reinvent-techblog-2025-post-111/>
- EDB Korea: 레거시 마이그레이션 — <https://edbkorea.com/blog/...>
- 컴퓨터월드 기고: 오픈소스 DB 전성시대 — <https://www.comworld.co.kr/news/articleView.html?idxno=51049>
- 다음 뉴스: 오라클 중심 DB 시장 균열 — <https://v.daum.net/v/20260120141615146>
- 투이컨설팅: 클라우드 오픈소스 DBMS 1부 — <https://2e.co.kr/news/articleView.html?idxno=210373>
- Velog @melon03090: Oracle→PG — <https://velog.io/@melon03090/...>
- Velog @peace_e: MySQL→PG — <https://velog.io/@peace_e/...>
- Velog @this_summer: 왜 PG — <https://velog.io/@this_summer/...>
- Velog @dailylifecoding: PostGIS 성능 — <https://velog.io/@dailylifecoding/...>
- Velog @kr_jkjung: PG HA 솔루션 비교 — <https://velog.io/@kr_jkjung/...>
- Medium @scalalang2: Citus 소개 — <https://medium.com/rate-labs/citus-postgres-%EB%B6%84%EC%82%B0-...>
- Medium @맞추다(Julie): MySQL→PG (array) — <https://medium.com/%EB%A7%9E%EC%B6%94%EB%8B%A4-%ED%8C%80%EB%B8%94%EB%A1%9C%EA%B7%B8/...>
- postgresql.kr 블로그: sharding — <https://postgresql.kr/blog/postgresql-sharding.html>

### 8.7 글로벌 커뮤니티 토론

- HN: Postgres is eating the database world — <https://news.ycombinator.com/item?id=39711863>, <https://news.ycombinator.com/item?id=39759539>
- HN: Leaving MySQL — <https://news.ycombinator.com/item?id=29455852>
- HN: Anyone made the jump? — <https://news.ycombinator.com/item?id=20449731>
- HN: PG production incident wraparound — <https://news.ycombinator.com/item?id=47819305>
- HN: Postgres or MySQL Ask HN — <https://news.ycombinator.com/item?id=21040625>
- Rick Branson: 10 things I hate about PostgreSQL — <https://rbranson.medium.com/10-things-i-hate-about-postgresql-20dbab8c2791>
- Codewar: 400M row migration — <https://medium.com/@codewar_with_me/postgresql-vs-mysql-i-migrated-400m-rows-heres-what-actually-broke-7b7978051c35>
- SQLServerCentral: production wraparound story — <https://www.sqlservercentral.com/articles/i-too-have-a-production-story-a-downtime-caused-by-postgres-transaction-id-wraparound-problem>

---

## 9. 리서치 한계 — 커버하지 못한 영역

이번 라운드는 단일 에이전트(Research Lead 직접 수행) 폴백 모드로 진행했다. 본 환경에서 Agent 도구가 노출되지 않아 web/paper/community-researcher 서브에이전트를 병렬 스폰할 수 없었기 때문이다. 그 결과:

1. **한국 기업의 1차 도입 후기**가 부족하다. 토스, 우아한형제들, 네이버, 라인의 PG 도입에 대한 공식 1차 후기는 본 라운드에서 직접 발견 못함. 후속 라운드에서 다음 도메인을 직접 정조준해야:
   - `techblog.woowahan.com`, `toss.tech`, `techblog.lycorp.co.kr`, `medium.com/naverpay`, `medium.com/coupang-engineering`, `engineering.linecorp.com`
2. **카카오 PG→ES CDC 시리즈 본문 인용**이 비어 있다. WebFetch가 nav만 받았다. 후속에 archive.org 또는 다른 캐시로 본문 확보 필요(wal2json vs pgoutput 선택 근거, 운영 통증).
3. **AlloyDB 학술 paper**가 검색 결과에 명시적으로 잡히지 않았다. VLDB/SIGMOD 2024~2025 proceedings 직접 색인 검색 필요.
4. **Reddit `r/PostgreSQL` 특정 thread quotable URL**이 라운드 내에서 미수집 — 후속에 reddit.com 도메인 한정 검색 필요.
5. **pgsql-general mailing list** 인용은 본 라운드에서 미수집 — `postgresql.org/list/pgsql-general/` 직접 색인 필요.
6. **벤치마크 raw data**: pgbench 자동 비교 사이트의 시계열 데이터와 HammerDB 18 회귀 토론은 GitHub Discussion만 확인 — 실제 결과 표 인용 가능한 보고서 필요.
7. **보안 / pgaudit / RBAC 패턴** — 본 라운드에서는 RLS만 깊게 다루고 pgaudit, scram-sha-256, ssl/tls best practice, CVE 추적은 표면적으로만 다룸. 후속 라운드 필요.
8. **PostgresML / 머신러닝 익스텐션** — 카탈로그 수준만 다룸. RAG·feature store 활용 사례 후속 보강 필요.
9. **Patroni와 Stolon, repmgr 상세 비교** — Patroni 중심, 다른 도구는 표면.
10. **EXPLAIN 시각화 도구**(explain.depesz.com, pg_explain) — 미수집.

후속 Phase 2에서 이 11개 항목을 채우면 책 본문에 필요한 모든 1차 자료를 갖추게 된다.
