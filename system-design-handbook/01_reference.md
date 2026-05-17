# 시스템 디자인 핸드북 — 통합 레퍼런스

생성일: 2026-05-16
대상 독자: 3~7년차 실무 백엔드 엔지니어 (인터뷰 대비 X, production 운영 가이드 O)
원천: `research/web.md` (45건) / `research/papers.md` (22건) / `research/community.md` (38건)
용도: 챕터 저술가가 책 한 권을 쓰는 동안 옆에 펴두고 인용·교차참조하는 단일 인덱스.

표기 규칙:
- 출처 표기: **(W#)** = web.md 자료 번호, **(P#)** = papers.md 번호, **(C#)** = community.md 자료/패턴/논쟁 번호.
- 권위 등급: ★★★ (논문/공식 docs/저자 권위) · ★★ (회사 engineering blog) · ★ (커뮤니티 의견·검증 필요).

---

## 1. 시스템 디자인 영역의 지형도

본 책이 다뤄야 할 토픽을 4축으로 분배한다. 각 항목 옆에 "왜 다뤄야 하는가" 한 줄과 1차 소스 표기.

### A. 빌딩 블록 (개별 부품 — bottom)
- **A1. 캐시 (Redis, Memcached, multi-tier)** — 거의 모든 시스템의 첫 번째 latency 무기. cache-aside · stampede · invalidation이 평생의 숙제. (W1, W2, C4)
- **A2. 메시지 큐 (Kafka, RabbitMQ, Pulsar, SQS)** — 비동기·decoupling·event-driven의 토대. 선택은 broker 복잡도 vs consumer 복잡도 trade-off. (W3, P19, C6)
- **A3. 관계형 DB (Postgres, MySQL, Aurora) / index** — 90% 시스템의 backbone. 인덱스·VACUUM·connection pool 운영 지식이 SRE 깊이를 결정. (W4, W10, P14, 휴리스틱 2/3/6)
- **A4. NoSQL key-value / wide-column (DynamoDB, Cassandra, ScyllaDB)** — write-heavy·schema flexibility의 대안. Hot partition이 평생의 적. (W9, P7, P8, P9, P13, 패턴 2)
- **A5. 검색 엔진 (Elasticsearch, Lucene, OpenSearch)** — text/full-text·로그·observability backbone. shard 설계·JVM heap 튜닝의 정석. (W8, 휴리스틱 1, 한국 3)
- **A6. 로드 밸런서 / 리버스 프록시 (HAProxy, NGINX, Envoy)** — L4/L7 분기, TLS termination, service mesh data plane. (W5, W44)
- **A7. CDN / Edge (Cloudflare, Akamai, Netflix Open Connect)** — origin offload, latency 단축, DDoS 방어. (W6, W25)
- **A8. 객체 스토리지 (S3, GCS, Azure Blob)** — durable storage의 표준. tiered storage·lifecycle policy. (W22, W25)
- **A9. 분산 조정 (ZooKeeper, etcd, Consul)** — leader election·service discovery·configuration. (P3)
- **A10. 시간/순서 (NTP, logical clock, Snowflake ID)** — 분산 시스템의 가장 어두운 코너. (P4, P5, W19, 패턴 3, tribal #1)
- **A11. 컨테이너/오케스트레이션 (K8s, ECS, Nomad)** — 표준 deployment substrate. 단 도입 부담은 큰 논쟁. (논쟁 G, P27)
- **A12. 서비스 메시 (Istio, Linkerd, Cilium)** — mTLS·observability·트래픽 제어. mesh 도입 비용 정량 비교. (W44)
- **A13. 스토리지 엔진 (B+ tree, LSM-tree, bloom filter)** — DB internals의 두 가지 큰 갈래. (P13, P22)

### B. 분산 시스템 패턴 (조립 규칙 — middle)
- **B1. 합의 (Paxos, Raft, ZAB)** — 분산 leader·log 복제의 이론적 핵심. (P1, P2, P3)
- **B2. 일관성 모델 (strong, snapshot, causal, eventual)** — application semantic 결정. PACELC가 CAP의 실용 보완. (W17, P5, P6, P11, P12, P31)
- **B3. 멱등성 (idempotency keys)** — 분산 환경에서 retry-safe 호출의 기본기. (W11, 휴리스틱 5)
- **B4. Saga (choreography vs orchestration)** — long-running 분산 트랜잭션의 표준 해법. (W12)
- **B5. Transactional Outbox / CDC** — dual-write 문제의 표준 해법. (W13)
- **B6. Event Sourcing / CQRS** — read/write 모델 분리, audit·temporal query. (W14)
- **B7. Rate Limiting** — abuse 방어·SLA 보호. token bucket 사실상 표준. (W15)
- **B8. Resilience (retry/backoff/jitter, circuit breaker, bulkhead)** — cascading failure 방지. (W16, W40, 휴리스틱 4)
- **B9. 분산 ID (Snowflake, ULID, UUIDv7)** — 글로벌 고유성·시간 정렬. (W19, P4)
- **B10. 데이터 파이프라인 (Lambda vs Kappa vs Dataflow)** — batch/stream 통합. (W20, P16, P17, P18, P19, P20)
- **B11. 샤딩 / 파티셔닝** — horizontal scaling의 본질. consistent hashing, range-based, hash-based. (W7, W10, W27, P8, P9)
- **B12. Replication (single-leader, multi-leader, leaderless)** — durability·read scale·geo distribution. (P7, P8, DDIA Ch 5)
- **B13. Fan-out (push, pull, hybrid)** — feed·notification 시스템의 trade-off. (W23, W24)
- **B14. CRDT / Operational Transform** — collaborative editing·offline-first 동기화. (W18, P11, 자료 28)
- **B15. Geo / spatial (H3, S2, geohash)** — 위치 기반 서비스·매칭. (W26)

### C. 케이스 스터디 (실제 시스템 — top)
- **C1. 채팅 (Discord, Slack, LINE, 당근, WhatsApp)** — WebSocket·fan-out·메시지 storage trade-off의 정석. (W21, W22, W30, W31, 한국 4, 한국 7)
- **C2. 피드/타임라인 (Twitter, Instagram, Facebook)** — celebrity·viral 처리, hybrid fan-out. (W23, W24)
- **C3. 스트리밍 (Netflix, YouTube)** — CDN·encoding·peering 비용. (W25)
- **C4. 매칭/지오 (Uber, 당근 거래, 배민 라이더)** — H3·dispatch·실시간 추적. (W26)
- **C5. 이커머스 (Shopify, Amazon, 쿠팡)** — pods·BFCM·재고 일관성. (W27, W32, 한국 5)
- **C6. 검색 (Slack, Coupang, Airbnb, 네이버, 카카오/다음)** — Elasticsearch + 자체 indexing + 한국어 형태소. (W22, W28, W32, W45, 한국 3)
- **C7. 결제·금융 (Stripe, Toss, 카카오뱅크)** — 멱등성·SAGA·외부 vendor failover. (W11, W29, W41, 한국 1, 한국 2)
- **C8. URL Shortener (bit.ly)** — read-heavy·base62·analytics async. (W19, W34)
- **C9. Rate Limiter** — Cloudflare 자사 구현 수준의 알고리즘 비교. (W15)
- **C10. 광고/추천 (카카오 광고, 쿠팡 추천)** — Kafka 기반 stream 데이터 파이프라인. (W33)
- **C11. 협업 도구 (Figma, Linear, Notion)** — CRDT 기반 multiplayer. (W18, P11, 자료 28)
- **C12. 글로벌 DB (Spanner, CockroachDB, FaunaDB)** — TrueTime·HLC·deterministic execution. (W4, P5, P10, P15)

### D. 운영·관측성·SRE (cross-cutting — outside)
- **D1. SLO/SLI/Error Budget** — 신뢰성을 정량화하는 언어. burn rate alert가 modern alerting. (W35, P23, P24)
- **D2. 관측성 (logs, metrics, traces, OpenTelemetry)** — 3-pillar + correlation. (W37, 휴리스틱 7)
- **D3. Alert 설계 / On-call** — pager fatigue 방지, runbook, blameless. (W36, 휴리스틱 9, 패턴 8)
- **D4. Postmortem / Blameless culture** — 학습 조직의 기반. (W36, P23, 패턴 10)
- **D5. Chaos Engineering** — 장애 내성 검증. Chaos Monkey → Gameday. (W38)
- **D6. 배포 전략 (blue-green, canary, feature flag, progressive delivery)** — deploy ≠ release. (W39, 휴리스틱 8)
- **D7. Capacity Planning** — 사전 부하 예측, headroom 관리. (P23)
- **D8. 마이그레이션 패턴** — dual-write, shadow read, cutover plan, rollback. (W21, 패턴 10, 한국 5)
- **D9. 비용 최적화 (FinOps)** — inter-AZ, NAT egress, S3 lifecycle. (패턴 7)
- **D10. 보안 (TLS, secret 관리, IAM, network policy)** — production 운영의 가장 약한 고리. (cross-reference 필요, 본 리서치 범위 외 일부)
- **D11. 한국 환경 특수성** — 망분리, 0시 트래픽, 통신 API. (W29, W41, 한국 1~10)

---

## 2. 빌딩 블록별 핵심 자료

각 항목: **정의 · 핵심 trade-off · 대표 사례 · 1차 참고문헌 (web/paper 교차 인덱스).**

### 2.1 캐시
- **정의:** 자주 읽히는 데이터를 빠른 storage(메모리)에 사본 보관해 origin(DB·service) 부하·latency를 줄이는 layer.
- **핵심 trade-off:**
  - 일관성 vs 성능: stale read 허용 정도
  - cache-aside (가장 일반) vs read-through vs write-through vs write-back
  - eviction (LRU·LFU·random·TTL)
- **대표 사례:** Redis는 데이터 구조·persistence 옵션 풍부. Memcached는 단순·빠름. cache stampede·thundering herd는 production 상수 문제(C4).
- **1차 참고문헌:** AWS Caching Whitepaper (W1) ★★★ · Redis Labs 캐시 최적화 (W1 보강) ★★★ · Cloudflare counting blog (W15) ★★★ · 휴리스틱 #4 (C4)
- **챕터 저술 시 활용:**
  - 도입부 hook: 패턴 4 "캐시 비웠더니 DB 죽었다" (C4)
  - 핵심 개념: cache-aside 다이어그램 + Redis vs Memcached 표
  - 깊이: probabilistic early expiration, singleflight 패턴
- **인용 가능 구절:**
  > "A cache-aside cache is updated after the data is requested. A read-through cache updates itself." — AWS Whitepaper (W1)

### 2.2 메시지 큐 (Kafka·RabbitMQ·Pulsar·SQS)
- **정의:** producer와 consumer를 비동기로 분리하는 broker. retention·ordering·delivery semantic이 핵심 차이.
- **핵심 trade-off:**
  - Kafka = "simple broker, complex consumer" (log + partition + offset, replay 가능)
  - RabbitMQ = "complex broker, simple consumer" (큐 소비 후 삭제, routing 풍부)
  - exactly-once는 양쪽 다 가능하나 "신중한 구현 필요"
- **대표 사례:** 카카오 공용 메시징 플랫폼 TF (W33), LINE 메시징 허브 (W30), Coupang Kafka 기반 검색 파이프라인 (W32).
- **1차 참고문헌:** Quix Kafka vs RabbitMQ (W3) ★★ · Jack Vanlightly RabbitMQ 시리즈 (W3) ★★★ · 패턴 6 "Kafka lag 4시간" (C6) ★
- **챕터 저술 시 활용:**
  - 비교표: Kafka·RabbitMQ·Pulsar·SQS의 retention·ordering·exactly-once
  - 실패담: LINE Apache HTTP client 업그레이드로 throughput 1/3 (W30)
  - production 운영: consumer lag 모니터링, rebalance storm

### 2.3 관계형 DB / 인덱스
- **정의:** schema·SQL·ACID. 대부분 시스템의 record of truth.
- **핵심 trade-off:**
  - B+ tree (read-friendly, predictable) vs LSM-tree (write-friendly, compaction 부담) (P13)
  - row-store vs column-store
  - 단일 leader (Postgres·MySQL replication) vs distributed (Aurora·Spanner·CockroachDB)
- **휴리스틱:**
  - "Just use Postgres" — 휴리스틱 3
  - connection pool size ≈ core × 2 + 1 — 휴리스틱 2
  - "index 추가 전 query를 의심해라" — 휴리스틱 6
- **1차 참고문헌:** CockroachDB NewSQL 비교 (W4) ★★★ · Abadi NewSQL 비판 (W4) ★★★ · Aurora SIGMOD'17 (P14) ★★★ · DDIA (P21) ★★★ · Database Internals (P22) ★★★
- **챕터 저술 시 활용:**
  - 도입부 hook: 패턴 5 "Slow query 어제는 빨랐는데"
  - 깊이: B-tree vs LSM-tree 다이어그램, Aurora "log is the database" 인용

### 2.4 NoSQL — wide-column / key-value
- **정의:** schema-on-read, horizontal scale 우선, 약한 consistency 허용.
- **핵심 trade-off:**
  - Dynamo 계열(masterless, eventual consistency, vector clock) vs Bigtable 계열(single-leader per tablet, strong consistency, Chubby/Spanner 의존)
  - LSM 기반 write heavy, hot partition이 평생의 적
- **대표 사례:** Discord Cassandra → ScyllaDB (W21, 패턴 2) · 당근 채팅 DynamoDB (W31, 한국 7)
- **1차 참고문헌:** Dynamo SOSP'07 (P7) ★★★ · Bigtable OSDI'06 (P8) ★★★ · Cassandra paper (P9) ★★★ · DynamoDB / Cassandra hello interview (W9) ★★
- **챕터 저술 시 활용:**
  - 도입부 hook: 패턴 2 "Hot partition 디버깅이 가장 잔인"
  - 깊이: partition key 설계 anti-pattern, Discord request coalescing

### 2.5 검색 엔진 (Elasticsearch)
- **정의:** inverted index · text analyzer · 분산 shard.
- **핵심 trade-off:**
  - shard 10–50GB / 200M docs 이하 (W8)
  - JVM heap 32GB 이하 (휴리스틱 1)
  - refresh_interval default 1s → write heavy면 30s로 (tribal #17)
- **한국 특수:** 한국어 형태소 분석기 — mecab-ko·NORI·KOMORAN·Khaiii·KIWI (한국 3)
- **1차 참고문헌:** Elastic 공식 (W8) ★★★ · 네이버 검색 (W45) ★★★ · 쿠팡 검색 (W32) ★★ · 한국 3 (C)
- **챕터 저술 시 활용:**
  - 도입부 hook: 한국어 검색 — 영어 분석기 그대로 쓰면 "쿠팡 배송" → "쿠팡배송" 못 찾음
  - 깊이: ES vs 자체 엔진 (LINE NSE, 카카오 다음 검색)

### 2.6 로드 밸런서 / 리버스 프록시
- **정의:** L4(TCP) 또는 L7(HTTP) 트래픽 분배 + TLS termination + routing.
- **핵심 trade-off:**
  - HAProxy = raw throughput per core 1위
  - NGINX = 안정적 workhorse, 정적·dynamic 둘 다
  - Envoy = cloud-native, mesh data plane 표준, 메모리 ~150MB (HAProxy 50MB)
- **1차 참고문헌:** Loggly 벤치마크 (W5) ★★ · Envoy 공식 (W5 보강) ★★★ · Linkerd vs Istio mTLS 정량 (W44) ★★★
- **챕터 저술 시 활용:** mesh 도입 비용 정량 (Istio mTLS +166% latency vs Linkerd +33% vs Istio Ambient +8%)

### 2.7 CDN / Edge
- **정의:** 사용자에 가까운 PoP에서 정적·일부 동적 콘텐츠 서빙.
- **대표 사례:** Cloudflare 330+ city anycast (W6) · Netflix Open Connect (W25, 95% 트래픽 AWS 안 거침)
- **새 트렌드:** edge compute (V8 isolates, cold start <5ms vs Lambda~수백ms)
- **1차 참고문헌:** Cloudflare 공식 (W6) ★★★ · Netflix TechBlog (W25) ★★★

### 2.8 분산 조정 서비스
- **정의:** leader election · service discovery · configuration · distributed lock.
- **대표 사례:** ZooKeeper (Hadoop·Kafka<2.8·HBase) · etcd (K8s) · Consul
- **트렌드:** Kafka KRaft가 ZooKeeper 떼어내며 운영 부담 감소 (P3 인용)
- **1차 참고문헌:** ZooKeeper paper (P3) ★★★ · Raft paper (P2) ★★★

### 2.9 시간/순서/분산 ID
- **정의:** distributed system에서 "언제"와 "어떤 순서"를 정의하는 방법.
- **핵심 개념:**
  - happens-before (Lamport 1978) — 인과 관계로 부분 순서 정의 (P4)
  - Lamport clock (totally ordered, false ordering 가능)
  - Vector clock (causality 정확히 잡지만 N에 비례)
  - HLC (Hybrid Logical Clock) — physical + logical 조합 (CockroachDB)
  - TrueTime (Spanner, GPS+atomic, [earliest, latest] uncertainty) (P5)
  - Snowflake ID (1+41+10+12 bit, NTP slew 권장) (W19, tribal #1)
- **1차 참고문헌:** Lamport 1978 (P4) ★★★ · Spanner OSDI'12 (P5) ★★★ · Marc Brooker "It's About Time" (자료 29) ★★★
- **챕터 hook:** 패턴 3 Timezone Hell (C3)

### 2.10 스토리지 엔진 (B+ tree vs LSM)
- **B+ tree:** read predictable, in-place update, write amplification 낮음, fragmentation 가능.
- **LSM tree:** write throughput 압도, compaction 부담, read amplification — bloom filter로 완화.
- **1차 참고문헌:** LSM 원전 (P13) ★★★ · Database Internals (P22) ★★★
- **챕터 저술 시:** Cassandra·RocksDB·LevelDB는 LSM, Postgres·MySQL InnoDB·SQLite는 B+ tree. write/read 비율로 선택.

---

## 3. 분산 시스템 패턴별 핵심 자료

각 패턴: **등장 배경(논문) · 해결 문제 · 반례 · 실패담(community) · 인용 구절.**

### 3.1 합의 (Paxos / Raft / ZAB)
- **배경:** FLP impossibility (1985, P30) — 비동기에서 deterministic consensus 불가. 실용 알고리즘은 안정 leader 가정 + liveness 양보.
- **Paxos (P1):** 1989/1998. 이해 난도가 학문적 표준이 될 만큼 어려움.
- **Raft (P2):** 2014. "이해 가능성"을 first-class goal로. etcd, Consul, TiKV, CockroachDB, Kafka KRaft.
- **ZAB (P3):** ZooKeeper의 atomic broadcast.
- **반례·교훈:** Kafka 2.8+가 ZooKeeper(ZAB) → KRaft(Raft)로 마이그레이션 — 운영 부담이 알고리즘 선택보다 큼.
- **인용:**
  > "Raft separates the key elements of consensus, such as leader election, log replication, and safety." — Ongaro 2014 (P2)

### 3.2 일관성 모델 (CAP, PACELC, isolation level)
- **배경:** CAP (Brewer 2000 conjecture, Gilbert·Lynch 2002 proof, P31) → PACELC (Abadi 2010, W17). 후자가 평상시 latency/consistency trade-off까지 포괄해 실용적.
- **모델 계층 (강 → 약):**
  - linearizability (single-machine atomic처럼 보임)
  - sequential consistency
  - causal consistency (HAT 가능 — P12)
  - read-your-writes / monotonic reads
  - eventual consistency
- **CALM theorem (P6):** "coordination-free = monotonic" 동치 — CRDT 이론적 근거.
- **반례·교훈:** Abadi의 "Spanner default isolation은 사실상 not serializable" (W4) — NewSQL marketing의 한계.
- **인용:**
  > "Eventual consistency is often chosen for performance reasons during normal operation, not just for partition resilience." — Abadi (W17)

### 3.3 멱등성 (Idempotency Keys)
- **배경:** retry-safe 호출 보장. IETF Idempotency-Key 헤더 표준화 진행.
- **표준 구현:** client-generated unique key + server-side request status table + cached response.
- **실패담:** "retry로 두 번 결제됐다" — 휴리스틱 5 (C)
- **1차 참고문헌:** Stripe Brandur (W11) ★★★
- **인용:**
  > "An idempotency key is a unique value generated by a client and sent to an API along with a request, with the server storing the key for bookkeeping." — Stripe (W11)

### 3.4 Saga (choreography vs orchestration)
- **배경:** 분산 트랜잭션에서 2PC 회피. local transaction sequence + compensating action.
- **반례:** choreography는 추적 어려움 → "event soup". orchestration은 SPOF·복잡.
- **한국 사례:** 토스뱅크 코어뱅킹 SAGA + 2PC 혼합 (W29).
- **1차 참고문헌:** Microservices Patterns Ch 4 (Richardson, P25) · microservices.io (W12) ★★★

### 3.5 Transactional Outbox + CDC
- **배경:** dual-write 문제 (DB commit + 메시지 발행 atomic 불가).
- **구현:** 같은 transaction에 outbox 테이블 insert → Debezium이 WAL/binlog tail → Kafka 발행.
- **1차 참고문헌:** Debezium 공식 (W13) ★★★

### 3.6 Event Sourcing / CQRS
- **배경:** state 대신 event log 저장 (Event Sourcing), read/write 모델 분리 (CQRS).
- **반례·교훈:** Fowler 경고 — "복잡도 추가, 대부분 시스템은 CRUD로 충분". Hugo Rocha "event schema migration이 가장 어렵다 — event는 영원히 남는다" (W14).
- **인용:**
  > "You should be very cautious about using CQRS... it can add significant complexity." — Fowler (W14)

### 3.7 Rate Limiting
- **알고리즘 비교:**
  - Token bucket = capacity + refill rate, burst 허용 (default 권장)
  - Leaky bucket = constant egress
  - Fixed window = boundary burst 문제
  - Sliding window log = 정확, 메모리 비쌈
  - Sliding window counter = 가중평균, Cloudflare 0.003% error 사실상 표준
- **1차 참고문헌:** Cloudflare counting (W15) ★★★ · Arcjet visualization (W15 보강) ★★

### 3.8 Resilience — Retry / Backoff / Jitter / Circuit Breaker / Bulkhead
- **요지:** retry storm 방지 위해 jitter 필수. circuit breaker 3-state (closed/open/half-open). bulkhead로 cascading failure 차단.
- **1차 참고문헌:** AWS Builders Library (W16, W40) ★★★
- **휴리스틱 4:** "Timeout 없는 호출은 없다" (C)

### 3.9 분산 ID (Snowflake·ULID·UUIDv7)
- **Snowflake:** 64-bit (1+41+10+12) ~3.5T 키.
- **NTP slew 권장:** step 시 clock 역행으로 ID 충돌 (tribal #1).
- **1차 참고문헌:** hello interview (W19) ★★

### 3.10 데이터 파이프라인 (Lambda / Kappa / Dataflow)
- **Lambda:** batch + speed + serving 3계층 — 코드 중복.
- **Kappa (Kreps 2014, 자료 19):** stream 단일계층 + replay.
- **Dataflow (Akidau 2015, P20):** event-time / watermark / trigger / accumulation 4축 통합 — Apache Beam의 추상화.
- **현재 mainstream:** Flink·Beam이 둘을 통합, batch는 bounded stream의 특수 케이스로.
- **1차 참고문헌:** Kai Waehner (W20) ★★★ · MapReduce (P16) · Spark RDD (P17) · Flink (P18) · Dataflow (P20)

### 3.11 샤딩 / 파티셔닝
- **방식:** range-based (Bigtable·HBase) / hash-based (Dynamo) / directory-based (Vitess VSchema).
- **Consistent Hashing:** 노드당 100~200 vnode로 hot spot 회피 (W7).
- **반례·교훈:** Hot partition (패턴 2, C2) — sharding key 분포 가정이 깨짐. Shopify pods = MySQL을 shop_id로 podding (W27).
- **1차 참고문헌:** Vitess (W10) ★★★ · ByteByteGo consistent hashing (W7) ★★ · Shopify pods (W27) ★★★

### 3.12 Replication
- **유형:** single-leader (Postgres) / multi-leader (CRDT 필요) / leaderless quorum (Dynamo).
- **N/R/W 튜닝:** R+W>N이면 일반적으로 일관성, R=W=1은 max availability.
- **1차 참고문헌:** Dynamo (P7) · DDIA Ch 5 (P21)

### 3.13 Fan-out (Push / Pull / Hybrid)
- **Push (fan-out-on-write):** follow N명에 미리 분배, read 빠름, write·storage 비쌈.
- **Pull (fan-out-on-read):** 읽을 때 merge, write 싸지만 read 비쌈.
- **Hybrid:** celebrity(10K+ followers)만 pull, 일반은 push (Twitter, Instagram).
- **1차 참고문헌:** Twitter Engineering (W23) ★★★ · Instagram (W24) ★★

### 3.14 CRDT / OT
- **CRDT (P11):** state-based (CvRDT, semilattice join) / op-based (CmRDT, commutative).
- **종류:** G-Counter, PN-Counter, OR-Set, LWW-Element-Set, RGA, Yjs, Automerge.
- **OT (Google Docs 기반):** centralized server 필요.
- **현재 사용처:** Linear, Figma multiplayer, Notion 일부, Riak, Redis Enterprise.
- **1차 참고문헌:** Shapiro et al 2011 (P11) ★★★ · Kleppmann QCon (W18) ★★★ · ACM Queue "Convergence" (자료 28) ★★★

### 3.15 Geo / Spatial
- **H3 (Uber):** 지구를 hexagonal cell로 분할, resolution 0~15. k-ring으로 이웃 cell 조회.
- **S2 (Google):** spherical quad-tree.
- **Geohash:** lat/lng → base32 string. prefix 매칭으로 근접 검색.
- **1차 참고문헌:** Uber H3 (W26) ★★★

---

## 4. 케이스 스터디 자료 풀

12개 시스템 — 챕터별 4~6개 deep dive로 활용 가능.

### 4.1 Discord (채팅, trillions of messages)
- **출처:** Discord blog (W21), ScyllaDB case study (W21 보강)
- **핵심 결정:** Cassandra 177노드 → ScyllaDB 72노드. p99 read 40~125ms → 15ms.
- **결정적 도구:** Rust로 작성한 data services layer + request coalescing.
- **인용:**
  > "Request coalescing is an important responsibility to avoid multiple database calls when many users request the same message." (W21)
- **챕터 매핑:** 채팅 + DB 마이그레이션

### 4.2 Slack (10B+ messages)
- **출처:** singhajit.com (W22), logz.io KalDB (W22 보강)
- **핵심 결정:** workspace-based sharding · PHP WebApp + Java RTM · 자체 KalDB.

### 4.3 Twitter Timeline (hybrid fan-out)
- **출처:** Twitter Engineering 2017 (W23)
- **핵심 결정:** Manhattan (자체 KV) · Redis cluster · celebrity 예외 처리.

### 4.4 Instagram (Python+PostgreSQL+Cassandra)
- **출처:** engineerscodex (W24)
- **핵심 결정:** 초기 Python+Django, 사진 S3, fanout Gearman→Kafka.

### 4.5 Netflix Open Connect
- **출처:** Netflix TechBlog 2025 (W25), FreeBSD Foundation 케이스스터디
- **핵심 결정:** control(AWS) vs data(Open Connect) 분리, 95% 트래픽 AWS bypass, FreeBSD sendfile() zero-copy.

### 4.6 Uber Dispatch (H3 + DISCO)
- **출처:** Uber blog (W26)
- **핵심 결정:** H3 hexagonal grid + DISCO multi-objective optimizer (wait time, repositioning, ML acceptance).

### 4.7 Shopify Pods (Modular Monolith)
- **출처:** Shopify Engineering (W27)
- **핵심 결정:** Ruby majestic monolith + Packwerk module boundary + MySQL podding by shop_id.

### 4.8 Airbnb Search
- **출처:** Airbnb Tech (W28)
- **핵심 결정:** IVF ANN over HNSW (가격/가용성 빈번 변경), SOA standards로 circuit breaker 강제.

### 4.9 Toss 결제·코어뱅킹
- **출처:** toss.tech (W29)
- **핵심 결정:** Hybrid cloud (Public + Private) · 1% progressive rollout · 코어뱅킹 MSA → "이자 받기" 가능.
- **챕터 매핑:** 한국 실무 + 결제

### 4.10 LINE Messaging Hub
- **출처:** LINE Engineering ko (W30)
- **핵심 결정:** connection-manager (WebSocket) ↔ message-router (gRPC) ↔ Kafka. LINE LIVE = Akka actor + Redis Cluster.
- **실패담 인용:** Apache HTTP client 업그레이드로 throughput 1/3 (W30).

### 4.11 당근마켓 채팅
- **출처:** 당근 blog (W31), AWS Summit Korea 2022
- **핵심 결정:** MSA + Go 첫 도입 + DynamoDB (Cassandra 운영 부담 회피) + Node.js push 1500 RPS.

### 4.12 Spanner (글로벌 SQL)
- **출처:** OSDI'12 paper (P5)
- **핵심 결정:** TrueTime [earliest, latest] uncertainty + commit wait. external consistency at global scale.

---

## 5. 운영·관측성·SRE 자료

### 5.1 SLO/SLI/Error Budget
- **공식:** SLI = good events / total events. SLO = SLI 목표. Error budget = 1 - SLO.
- **Burn rate alert:** 실제 에러율 / 허용 에러율. multi-window multi-burn-rate가 폭발+만성 양쪽 잡음.
- **인용:**
  > "100% is the wrong reliability target for basically everything." — Google SRE Book Ch 4 (P23)
- **1차 참고문헌:** Google SRE workbook (W35) ★★★ · Datadog burn rate (W35 보강) ★★★

### 5.2 관측성 — 3 signals + correlation
- **OpenTelemetry (W37, ★★★):** traces·metrics·logs를 OTLP wire format으로 통일. OTel Collector가 batching·filtering·routing.
- **휴리스틱 7:** 구조화 로깅 (Charity Majors).
- **trace_id로 logs/metrics correlation** — observability vendor lock-in 해소.

### 5.3 Alert 설계 / On-call
- **휴리스틱 9:** "3am에 사람이 할 게 없으면 page 보내지 마라" (Charity Majors).
- **반복 고통:** pager fatigue, false positive 80%+ (패턴 8, C8).

### 5.4 Postmortem / Blameless
- **template:** timeline · root cause · action items (owner+due) · what went well/wrong · lessons.
- **반례:** GitLab 2017 6시간 outage + backup 5개 중 4개 실패 (패턴 10).
- **1차 참고문헌:** Google SRE postmortem culture (W36) ★★★

### 5.5 Chaos Engineering
- **Netflix Simian Army:** Chaos Monkey · Latency Monkey · Chaos Gorilla(AZ) · Chaos Kong(region).
- **4 원칙:** hypothesis → real-world event → production → blast radius minimization.
- **1차 참고문헌:** Principles of Chaos (W38) ★★★

### 5.6 배포 전략
- **Blue-Green:** 두 환경 + 트래픽 스위치.
- **Canary:** 일부 트래픽 → 모니터링 → 점진 확대.
- **Feature Flag:** code deploy ≠ feature release (휴리스틱 8).
- **Progressive Delivery:** canary + flag + metric-based auto-promotion (Argo Rollouts, Flagger).
- **1차 참고문헌:** LaunchDarkly (W39) ★★★

### 5.7 비용 / FinOps
- **반복 고통:** inter-AZ traffic, NAT egress, S3 list, 미사용 EBS, 무제한 log retention (패턴 7).
- **사례:** 우아한형제들 30% 절감 (VPC endpoint·Aurora I/O optimized·S3 intelligent tiering).

### 5.8 마이그레이션 패턴
- **단계:** dual-write → shadow read → consistency 검증 → cutover → rollback plan.
- **반례:** 당근 Cassandra → DynamoDB 시 consistency 검증 도구 직접 제작 (패턴 10).

---

## 6. 한국 실무 맥락

본 책의 차별점이 될 영역. 도입부 hook·예시에 적극 활용.

### 6.1 0시 동시 트래픽 (한국 고유 패턴)
- **출처:** 토스 코어뱅킹 발표 (W29), 카카오뱅크 청약·청년적금, velog 다수 (한국 1)
- **사례:** "이자 받기 0시" "청약 9시" "콘서트 예매 8시" — 정상의 수십~수백 배 burst.
- **챕터 hook:** 빌딩 블록 도입부 또는 한국 실무 챕터.

### 6.2 망분리 (전자금융감독규정)
- **출처:** 카카오뱅크 if(kakao) 발표, 한국 핀테크 velog (한국 2)
- **시스템 디자인 영향:** 클라우드 도입 제약, hybrid 운영, AWS Outposts·자체 IDC.

### 6.3 한국어 형태소 분석
- **분석기:** mecab-ko·NORI·KOMORAN·Khaiii(카카오)·KIWI(클로바)
- **챕터 hook:** "쿠팡 배송 vs 쿠팡배송" 검색 못 찾는 사례.
- **출처:** 네이버 D2 (W45), 카카오 다음 검색, 쿠팡 검색 (W32)

### 6.4 통신 3사 본인인증 + PG (결제 게이트웨이)
- **출처:** 토스페이먼츠 / 카카오뱅크 / NHN KCP / NICE / KCB / 다날 docs + 패턴 9 (C9)
- **시스템 디자인 영향:** wrapper layer 필수 (vendor 차이 흡수), failover 전략, 0시 폭주 대비.

### 6.5 카카오톡 트래픽 패턴
- **특수성:** 새해·설날·발렌타인·어버이날 spike, group push fan-out 비용, 광고 점심·퇴근 spike.
- **출처:** 카카오 if(kakao) 2022·2023 (한국 4)

### 6.6 쿠팡 로켓배송 — 자정 cutoff
- **출처:** 쿠팡 엔지니어링 Medium (W32), AWS Summit Korea (한국 5)
- **시스템 디자인 영향:** 정합성과 속도의 극단적 trade-off, 재고·배차·창고가 모두 자정 전 일관 결정.

### 6.7 우아한형제들 — Java/Spring + DDD
- **출처:** 우아한형제들 techblog, 우아콘 (한국 6)
- **시스템 디자인 영향:** 한국 백엔드 Java/Spring 표준화의 좋은 reference, 모듈러 모놀리스 진화.

### 6.8 당근 hyperlocal
- **출처:** 당근 채팅 / 검색 발표 (W31, 한국 7)
- **시스템 디자인 영향:** 동(neighborhood) 단위 partition, 거래 위치 기반 chat 라이프사이클.

### 6.9 카카오뱅크 — 99.99% 금융 가용성
- **출처:** tech.kakaobank.com (W41)
- **시스템 디자인 영향:** 메인프레임 → MSA, 거래 일관성, 감사, 24/7.

### 6.10 자체 IDC vs 클라우드 — 2022 SK C&C 화재 후
- **출처:** 카카오 if(kakao) 2022 회고 (한국 9)
- **시스템 디자인 영향:** multi-region이 한국 기업의 표준 화두로 격상.

---

## 7. 논쟁점·관점차

각 논쟁: **관점 A · 관점 B · 양 진영 근거 자료.** 챕터에서 한쪽 편들지 말고 두 관점 모두 제시 권장.

### 7.1 모놀리스 vs 마이크로서비스 vs 모듈러 모놀리스
- **A (모놀리스/모듈러 모놀리스):** 기본은 모놀리스, MSA는 50명+에서 고려. (Shopify W27, DHH, HN 1100+ comments — C 패턴 1, 논쟁 A)
- **B (MSA 옹호):** 처음부터 service boundary 잡으면 늦게 안 아프다. (Sam Newman P26, Netflix·Uber·Airbnb 자생적 진화)
- **한국 진영:** 토스 (점진 + 코어뱅킹은 초기 MSA), 우아한형제들 (모듈러 모놀리스).
- **반복 고통(C 패턴 1):** "8 services for 12 developers" — distributed monolith 함정.
- **본 책의 입장 권장:** "조직 규모·기술 성숙도·도메인 복잡도 3축으로 의사결정 — 한쪽 정답 없음."

### 7.2 REST vs gRPC vs GraphQL
- **REST:** ergonomics, debug 용이, 도구 ecosystem. (HN "Why we left gRPC" 시리즈)
- **gRPC:** 내부 service 간 5x latency 우위, protobuf schema enforcement. (우아한형제들·라인·쿠팡 내부 통신)
- **GraphQL:** client diversity 있는 곳에서만. backend-for-frontend가 더 단순한 경우 많음. (토스 GraphQL 도입 후 캐시·N+1 토로)
- **권장:** 외부 API는 REST, 내부 service 통신은 gRPC, BFF가 복잡해질 때만 GraphQL.

### 7.3 ORM vs Raw SQL vs Query Builder
- **ORM (JPA·ActiveRecord·Prisma):** productivity 높음, 90% 케이스 충분.
- **Raw SQL:** leaky abstraction 피로, N+1·lazy loading 디버깅에 시간 더 듦.
- **Query Builder (JOOQ·Kysely·sqlx·Drizzle):** type-safe + readable + escape hatch.
- **출처:** OKKY 단골 논쟁 (논쟁 C).

### 7.4 Event-driven vs Request/Response
- **Event-driven:** 느슨 결합, scale, audit. 익숙해지면 돌아갈 수 없다.
- **Request/Response:** 추적·테스트·디버깅 쉬움. 80%는 sync가 답.
- **한국 사례:** 토스 결제 critical path = sync, 후처리(영수증·알림) = async.

### 7.5 Cloud vs On-Prem (한국 특수)
- **Cloud first:** managed service 운영 부담 압도적 감소 (당근·토스 페이먼츠).
- **Hybrid/On-Prem:** 라인 자체 IDC, 네이버 클라우드, 금융권 망분리 강제.

### 7.6 SQL vs NoSQL — "MongoDB 망했나"
- **SQL 진영:** NoSQL은 transactional consistency 약함 → 결국 돌아온다.
- **NoSQL 진영:** schema 진화 빈번 도메인에서 SQL 대비 우위.
- **통합:** Postgres jsonb · pgvector · LISTEN/NOTIFY로 "Just use Postgres" 흐름 (휴리스틱 3).

### 7.7 Kubernetes — 필요한가, 과한가
- **K8s 진영:** distributed Linux, 일정 규모 이상 표준.
- **반대:** 5명 팀이 K8s = ops 자살. Heroku/Fly.io/Render로 충분 (DHH).
- **한국:** 토스·쿠팡·우아한형제들 K8s, LINE 자체 PaaS, 카카오 일부 Mesos.

### 7.8 Monorepo vs Polyrepo
- **Monorepo:** Google·Meta·Uber — atomic refactor.
- **Polyrepo:** 작은 조직·명확 ownership.
- **도구:** Bazel·Nx·Turborepo·Rush가 monorepo 진입장벽 낮춤.

### 7.9 Lambda vs Kappa Architecture
- **Lambda:** batch + stream 이중 layer — 코드 중복 비용.
- **Kappa:** stream 단일 — 재처리는 Kafka replay.
- **현재:** Flink·Beam이 통합, batch = bounded stream. 단 financial reconciliation 등 highly accurate batch에는 여전히 Lambda.

### 7.10 Strong vs Eventual Consistency (NewSQL 논쟁)
- **Strong (Spanner·CockroachDB·F1):** external consistency, 글로벌 SQL.
- **Eventual (Dynamo·Cassandra·Riak):** availability·throughput·latency 우위.
- **Abadi 비판:** Spanner default가 실제로는 not serializable (W4).
- **PACELC:** else-latency vs else-consistency가 평상시 진짜 trade-off.

### 7.11 Spanner TrueTime vs HLC
- **TrueTime:** GPS + atomic clock hardware → uncertainty ε 명시.
- **HLC (CockroachDB):** commodity HW, ε 더 큼.
- **trade-off:** TrueTime은 정확하나 GCP/Google 전용, HLC는 self-hosted 가능.

### 7.12 AI/LLM이 시스템 디자인을 바꿀까
- **A:** 벡터 DB·embedding·RAG는 새 빌딩 블록, 결국 또 하나의 도구.
- **B:** LLM이 서비스를 만드는 시대 — 시스템 디자인이 prompt로 흡수.
- **권위자:** Will Larson — "LLM은 도구, 분산 원리는 더 중요해진다" (논쟁 I).

---

## 8. 참고문헌 (인용 가능 형식 통일)

### 8.1 논문 (academic)
- Lamport, L. (1978). Time, Clocks, and the Ordering of Events in a Distributed System. *CACM*, 21(7), 558–565. DOI: 10.1145/359545.359563. **(P4)**
- Fischer, M., Lynch, N., Paterson, M. (1985). Impossibility of Distributed Consensus with One Faulty Process. *JACM*, 32(2), 374–382. DOI: 10.1145/3149.214121. **(P30)**
- Lamport, L. (1998). The Part-Time Parliament. *ACM TOCS*, 16(2), 133–169. DOI: 10.1145/279227.279229. **(P1)**
- Gilbert, S., Lynch, N. (2002). Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services. *SIGACT News*, 33(2). DOI: 10.1145/564585.564601. **(P31)**
- Dean, J., Ghemawat, S. (2004). MapReduce: Simplified Data Processing on Large Clusters. *OSDI '04*. DOI: 10.1145/1327452.1327492. **(P16)**
- Chang, F., et al. (2006). Bigtable: A Distributed Storage System for Structured Data. *OSDI '06* / *ACM TOCS* 2008. DOI: 10.1145/1365815.1365816. **(P8)**
- DeCandia, G., et al. (2007). Dynamo: Amazon's Highly Available Key-value Store. *SOSP '07*, 205–220. DOI: 10.1145/1294261.1294281. **(P7)**
- Hunt, P., Konar, M., Junqueira, F., Reed, B. (2010). ZooKeeper: Wait-Free Coordination for Internet-Scale Systems. *USENIX ATC '10*. **(P3)**
- Lakshman, A., Malik, P. (2010). Cassandra: A Decentralized Structured Storage System. *SIGOPS OSR*, 44(2). DOI: 10.1145/1773912.1773922. **(P9)**
- Shapiro, M., Preguiça, N., Baquero, C., Zawirski, M. (2011). Conflict-Free Replicated Data Types. *SSS '11*, LNCS 6976. DOI: 10.1007/978-3-642-24550-3_29. **(P11)**
- Corbett, J., et al. (2012). Spanner: Google's Globally-Distributed Database. *OSDI '12* → *ACM TOCS* 2013, 31(3). DOI: 10.1145/2491245. **(P5)**
- Thomson, A., et al. (2012). Calvin: Fast Distributed Transactions for Partitioned Database Systems. *SIGMOD '12*. DOI: 10.1145/2213836.2213838. **(P10)**
- Zaharia, M., et al. (2012). Resilient Distributed Datasets. *NSDI '12*. URL: https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia. **(P17)**
- Shute, J., et al. (2013). F1: A Distributed SQL Database That Scales. *VLDB 2013*, 1068–1079. URL: https://research.google/pubs/pub41344/. **(P15)**
- Bailis, P., et al. (2014). Highly Available Transactions: Virtues and Limitations. *VLDB 2014*. DOI: 10.14778/2732232.2732237. **(P12)**
- Ongaro, D., Ousterhout, J. (2014). In Search of an Understandable Consensus Algorithm. *USENIX ATC '14*, 305–319. URL: https://raft.github.io/raft.pdf. **(P2)**
- Akidau, T., et al. (2015). The Dataflow Model. *VLDB 2015*. DOI: 10.14778/2824032.2824076. **(P20)**
- Carbone, P., et al. (2015). Apache Flink: Stream and Batch Processing in a Single Engine. *IEEE Data Engineering Bulletin*, 38(4). URL: https://flink.apache.org/img/flink-bulletin-2015.pdf. **(P18)**
- O'Neil, P., Cheng, E., Gawlick, D., O'Neil, E. (1996). The Log-Structured Merge-Tree. *Acta Informatica*, 33(4), 351–385. DOI: 10.1007/s002360050048. **(P13)**
- Verbitski, A., et al. (2017). Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases. *SIGMOD '17*, 1041–1052. DOI: 10.1145/3035918.3056101. **(P14)**
- Hellerstein, J. M., Alvaro, P. (2020). Keeping CALM: When Distributed Consistency is Easy. *CACM*, 63(9), 72–81. DOI: 10.1145/3369736. **(P6)**
- Kleppmann, M. (2022). Convergence: Local-first software. *ACM Queue*, 20(4). DOI: 10.1145/3546931. **(자료 28)**

### 8.2 서적
- Beyer, B., Jones, C., Petoff, J., Murphy, N. (eds) (2016). *Site Reliability Engineering*. O'Reilly. URL: https://sre.google/sre-book/table-of-contents/. **(P23)**
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. ISBN: 978-1449373320. **(P21)**
- Newman, S. (2021). *Building Microservices*, 2nd ed. O'Reilly. ISBN: 978-1492034025. **(P26)**
- Richardson, C. (2018). *Microservices Patterns*. Manning. ISBN: 978-1617294549. **(P25)**
- Beyer, B., et al. (2018). *The Site Reliability Workbook*. O'Reilly. URL: https://sre.google/workbook/table-of-contents/. **(P24)**
- Burns, B. (2018). *Designing Distributed Systems*. O'Reilly. ISBN: 978-1491983645. **(P27)**
- Petrov, A. (2019). *Database Internals*. O'Reilly. ISBN: 978-1492040347. **(P22)**

### 8.3 공식 docs / 기업 engineering blog (선별 — 전체는 web.md 참조)
- AWS Caching Strategies Whitepaper — https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html **(W1)**
- AWS Builders' Library: Timeouts, Retries and Backoff with Jitter — https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ **(W16)**
- Cloudflare: How we built rate limiting capable of scaling — https://blog.cloudflare.com/counting-things-a-lot-of-different-things/ **(W15)**
- Stripe: Designing robust and predictable APIs with idempotency (Brandur Leach, 2017) — https://stripe.com/blog/idempotency **(W11)**
- Debezium: Reliable Microservices Data Exchange with the Outbox Pattern — https://debezium.io/blog/2019/02/19/reliable-microservices-data-exchange-with-the-outbox-pattern/ **(W13)**
- Discord: How Discord Stores Trillions of Messages — https://discord.com/blog/how-discord-stores-trillions-of-messages **(W21)**
- Netflix TechBlog: Netflix Live Origin (2025) — https://netflixtechblog.com/netflix-live-origin-41f1b0ad5371 **(W25)**
- Uber: H3 — A Hexagonal Hierarchical Geospatial Indexing System — https://www.uber.com/us/en/blog/h3/ **(W26)**
- Shopify Engineering: A Pods Architecture To Allow Shopify To Scale — https://shopify.engineering/a-pods-architecture-to-allow-shopify-to-scale **(W27)**
- Toss tech: 토스의 결제 시스템 현대화 — https://toss.tech/article/payments-legacy-1 **(W29)**
- Toss tech: SLASH 23 코어뱅킹 — https://toss.tech/article/slash23-corebanking **(W29)**
- LINE Engineering ko: 메시징 허브 시리즈 — https://engineering.linecorp.com/ko/blog/about-messaging-hub-2 **(W30)**
- 당근마켓 채팅팀 채용 비전·문화 — https://about.daangn.com/ **(W31)**
- 쿠팡 엔지니어링 (Medium ko) — 대용량 트래픽 백엔드 전략 https://medium.com/coupang-engineering/ **(W32)**
- 카카오 tech: 공용 Kafka/RabbitMQ 메시징 플랫폼 — https://tech.kakao.com/2021/12/23/kafka-rabbitmq/ **(W33)**
- 카카오뱅크 tech — https://tech.kakaobank.com/ **(W41)**
- 네이버 검색 엔지니어링 가이드 — https://naver-career.gitbook.io/kr/service/search/engine-and-solution/search-engine **(W45)**
- 네이버 D2 — https://d2.naver.com/
- 우아한형제들 기술블로그 — https://techblog.woowahan.com/
- Google SRE Workbook: Implementing SLOs — https://sre.google/workbook/implementing-slos/ **(W35)**
- Google SRE Book: Postmortem Culture — https://sre.google/sre-book/postmortem-culture/ **(W36)**
- OpenTelemetry: Observability primer — https://opentelemetry.io/docs/concepts/observability-primer/ **(W37)**
- Principles of Chaos Engineering — https://principlesofchaos.org/ **(W38)**
- LaunchDarkly: Deploying without downtime — https://launchdarkly.com/blog/deploying-without-downtime/ **(W39)**

### 8.4 권위자 블로그·X
- Martin Kleppmann (DDIA 저자) — https://martin.kleppmann.com/ · QCon talks
- Marc Brooker (AWS Distinguished Engineer) — https://brooker.co.za/blog/
- Daniel Abadi (NewSQL 비판) — http://dbmsmusings.blogspot.com/
- Charity Majors (Honeycomb CTO) — https://charity.wtf/ + X @mipsytipsy
- Will Larson (Staff Engineer 저자) — https://lethain.com/
- Camille Fournier — https://skamille.medium.com/
- Cindy Sridharan (Distributed Systems Observability) — https://copyconstruct.medium.com/
- Brandur Leach (Stripe 전 엔지니어) — https://brandur.org/

### 8.5 커뮤니티 인덱스 (검증 필요)
- Hacker News — https://news.ycombinator.com/
- Reddit r/ExperiencedDevs · r/programming · r/devops · r/SRE · r/aws · r/kubernetes
- OKKY — https://okky.kr/
- velog (백엔드 태그) — https://velog.io/tags/backend
- Use The Index, Luke! (Markus Winand) — https://use-the-index-luke.com/

---

## 9. 리서치 한계

- **보안·인증·인가**: TLS, OAuth2/OIDC, secret 관리, network policy 등은 본 리서치에서 부분 커버. 책에서 별도 챕터 다룬다면 추가 리서치 권장.
- **2024–2026 최신 학술 논문**: vector DB·LLM serving 인프라(vLLM, PagedAttention) 논문은 의도적 제외. 12장 "AI/시스템 디자인 미래" 같은 마무리 챕터 작성 시 별도 리서치.
- **수치 재현성**: TrueTime ε ~3ms, Spanner commit ~6ms 등은 Google 발표 수치. external benchmark가 거의 없어 marketing-tinted로 인용 시 주의.
- **국내 학술지**: KIISE·IEIE 등 한국 학회 논문은 검색 범위 밖. 한국 환경 특화 papers는 community/web의 한국 기업 발표로 갈음.
- **익명 커뮤니티 주장**: HN·Reddit 댓글은 익명 다수. 저자명·소속 명시된 글과 명확히 구분해 인용. 책 인용 전 cross-check 최소 2개 권장.
- **세부 URL 검증**: Reddit thread 등 일부 링크는 검색 키워드 기반 보수적 정리 — 챕터 저술 시 정확한 permalink로 교체 필요.
- **장기 변동성**: Kafka·MongoDB·Elasticsearch 같은 도구는 1~2년마다 큰 변경(KRaft, MongoDB Atlas, ES → OpenSearch 분기). 책 출간 시점 기준 verify 권장.
- **편향**: 커뮤니티는 본질적으로 실패담·불만 과대표시. "잘 굴러가는 시스템"의 침묵을 의식하며 사용.
- **언어 편중**: 영어 자료 ~60%, 한국어 ~35%, 일본어·중국어 거의 없음. 라인 일본 운영 사례는 영어 자료로 보강.
- **DDIA 2판**: 2025 작업 중 — 출간 시 일부 인용 갱신 필요.

---

## 부록 A: 4축 매트릭스 (챕터 저술 시 빠른 lookup)

| 토픽 | 빌딩블록 | 패턴 | 케이스 | 운영 |
|------|---------|------|--------|------|
| 채팅 시스템 | DB(C/Dynamo), 큐(Kafka), WebSocket | fan-out, idempotency | Discord, LINE, 당근, Slack | hot partition 알람, lag |
| 피드/타임라인 | 캐시(Redis), 큐, KV | fan-out hybrid | Twitter, Instagram | celebrity 알람 |
| 결제·금융 | RDB, 큐 | idempotency, SAGA | Stripe, Toss, 카카오뱅크 | SLO 99.99%, audit |
| 검색 | ES, 형태소 분석기 | indexing pipeline | Slack, 쿠팡, 네이버 | shard skew |
| 이커머스 | RDB(샤딩), 캐시, CDN | pods, cache stampede | Shopify, 쿠팡 | BFCM 대비 |
| 매칭/지오 | H3, Redis geo | dispatch, real-time | Uber, 배민, 당근 거래 | 지역별 alert |
| 스트리밍 | CDN, encoding | adaptive bitrate | Netflix, YouTube | peering 비용 |
| 협업 도구 | KV, WebSocket | CRDT, OT | Figma, Linear, Notion | end-to-end e2e latency |
| 글로벌 DB | Spanner·Cockroach | TrueTime, HLC, Paxos/Raft | Spanner, F1, FaunaDB | cross-region commit |
| URL Shortener | Redis, KV | Snowflake ID, base62 | bit.ly | abuse 감지 |
| Rate Limiter | Redis | token bucket, sliding window | Cloudflare 자사 | quota alert |
| 광고/추천 | Kafka, ML pipeline | Kappa | 카카오 광고, 쿠팡 추천 | data quality |

---

## 부록 B: 챕터 저술가 사용 가이드

1. **챕터를 쓰기 전:** 부록 A 매트릭스에서 해당 토픽의 4축 자료 묶음을 먼저 본다.
2. **도입부 hook:** §1 "한국 실무 맥락" 또는 §3 "패턴" 또는 community 의 "반복되는 고통" 중 1개를 골라 1단락.
3. **개념 정의:** §2 빌딩 블록 또는 §3 패턴 항목의 "정의 + trade-off"를 paraphrase.
4. **깊이 (이론):** §8.1 논문 또는 P# 인덱스로 이론 backbone 보강.
5. **사례 (실전):** §4 케이스 스터디에서 2~3개 골라 비교.
6. **논쟁 (균형):** §7에서 해당 논쟁이 있으면 양 진영 모두 제시.
7. **운영 (production):** §5 운영·SRE 자료로 알람·배포·rollback까지.
8. **인용:** 직접 인용은 §8 참고문헌 형식으로. 검증 필요 라벨이 붙은 자료는 paraphrase + cross-check.
