# 웹 리서치: 시스템 디자인 (실무 백엔드 가이드)

수집일: 2026-05-16
대상 독자: 3~7년차 실무 백엔드 엔지니어 (인터뷰 대비 아님)
4축 분배: A. 빌딩 블록 / B. 분산 시스템 패턴 / C. 케이스 스터디 / D. 운영·관측성·SRE

수집 자료 총 45건. 한국어/영어 혼합, 공식 docs·기업 engineering blog 우선.

---

## A. 빌딩 블록

### 자료 1: Redis vs Memcached 캐싱 전략 (AWS 공식 whitepaper)
- 출처: https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html
- 저자·날짜: AWS (whitepaper, 지속 업데이트)
- 신뢰성: 최상 (공식 docs)
- 핵심 주장: cache-aside는 가장 일반적인 패턴. read-through·write-through·write-back·write-around 모두 trade-off 명확. cache-aside는 stale data를 TTL로 견디는 게 핵심.
- 인용 가능한 구절:
  > "A cache-aside cache is updated after the data is requested. A read-through cache updates itself."
- 관련 섹션: 빌딩 블록 - 캐시
- 보강 자료: Redis Labs의 cache optimization 글 (https://redis.io/blog/guide-to-cache-optimization-strategies/) — multi-tier cache, cache stampede 방지(probabilistic early expiration, mutex).

### 자료 2: Redis vs Memcached eviction & 캐시 전략 (Tech Interview Dot Org)
- 출처: https://www.techinterview.org/post/3233474139/system-design-distributed-caching-redis-memcached-cache-aside-write-through-eviction-policies-cache-stampede-consistency/
- 신뢰성: 중
- 핵심 주장: Memcached는 LRU만 지원, Redis는 allkeys-lru/lfu/random/volatile-* 등 다중 정책. 실무에서는 Redis 선택이 압도적. 단 Memcached가 simpler & faster for pure cache(no persistence).
- 관련 섹션: 빌딩 블록 - 캐시

### 자료 3: Kafka vs RabbitMQ vs Pulsar 비교 (Quix)
- 출처: https://quix.io/blog/apache-kafka-vs-rabbitmq-comparison
- 보강: https://jack-vanlightly.com/blog/2017/12/15/rabbitmq-vs-kafka-part-4-message-delivery-semantics-and-guarantees (Jack Vanlightly, RabbitMQ team member 시절 작성)
- 신뢰성: 최상 (Jack Vanlightly 글), 중 (Quix)
- 핵심 주장: Kafka는 "simple broker, complex consumer". RabbitMQ는 "complex broker, simple consumer". Kafka는 retention 기반 log, RabbitMQ는 큐 소비 후 삭제. exactly-once는 Kafka transactional producer + idempotent consumer로 가능하나 "신중한 구현 필요". RabbitMQ는 application-level idempotency에 의존.
- 인용 가능한 구절:
  > "Kafka uses a 'simple broker, complex consumer' approach, while RabbitMQ follows a 'complex broker, simple consumer' model."
  > "exactly-once는 financial pipeline에서 critical — duplicate event는 double-billing을 의미한다"
- 관련 섹션: 빌딩 블록 - 메시지 큐 + 패턴 - 멱등성

### 자료 4: NewSQL 비교 (CockroachDB Labs 공식)
- 출처: https://www.cockroachlabs.com/blog/spanner-vs-cockroachdb/
- 보강: http://dbmsmusings.blogspot.com/2018/09/newsql-database-systems-are-failing-to.html (Daniel Abadi, "NewSQL is failing to guarantee consistency, and I blame Spanner")
- 신뢰성: 최상 (CockroachDB 자사 글 + Abadi 학술 블로그)
- 핵심 주장: Spanner는 TrueTime(원자시계+GPS) 기반 globally consistent. CockroachDB는 commodity HW + HLC(Hybrid Logical Clock). 후자는 약간의 정확도를 양보하는 대신 self-hosted 가능. "Spanner의 default isolation level이 실제로는 serializable이 아니"라는 Abadi의 지적은 NewSQL marketing의 한계를 폭로하는 자료로 인용 가치 큼.
- 관련 섹션: 빌딩 블록 - DB + 패턴 - 일관성

### 자료 5: HAProxy / NGINX / Envoy 비교 벤치마크 (Loggly)
- 출처: https://www.loggly.com/blog/benchmarking-5-popular-load-balancers-nginx-haproxy-envoy-traefik-and-alb/
- 보강: https://www.envoyproxy.io/docs/envoy/latest/intro/comparison (Envoy 공식)
- 신뢰성: 최상 (Envoy docs), 중 (Loggly)
- 핵심 주장: HAProxy는 raw L7 throughput per core에서 1위. Envoy는 250 concurrency 이상에서 더 우수, 메모리 ~150MB (HAProxy 50MB, NGINX 80MB). NGINX는 "안정적 workhorse", Envoy는 cloud-native·service mesh 용. mesh 도입 시 Envoy 사실상 표준.
- 관련 섹션: 빌딩 블록 - 로드밸런서

### 자료 6: Cloudflare Workers 글로벌 anycast 아키텍처
- 출처: https://workers.cloudflare.com/solutions/network/
- 보강: https://www.educative.io/newsletter/system-design/cloudfare-edge-network-60-million
- 신뢰성: 최상 (Cloudflare 공식)
- 핵심 주장: 330+ cities, BGP anycast 라우팅으로 nearest PoP. V8 isolates는 컨테이너/VM보다 메모리 1/10, cold start <5ms. p95 user 기준 50ms 이내 도달. Lambda@Edge·Vercel과 다른 점은 isolate 기반 (process 기반 X).
- 관련 섹션: 빌딩 블록 - CDN/Edge

### 자료 7: Consistent Hashing 심화 (ByteByteGo + Hello Interview)
- 출처: https://blog.bytebytego.com/p/consistent-hashing-101-how-modern
- 보강: https://www.hellointerview.com/learn/system-design/core-concepts/consistent-hashing
- 신뢰성: 중
- 핵심 주장: 노드 추가/제거 시 평균 K/N 키만 재배치. 단순 hash ring은 hot spot 발생 — virtual node(VNode)로 해결, 노드당 100~200 vnode가 일반적. Dynamo·Cassandra·Riak·memcached(client-side) 모두 채택.
- 관련 섹션: 빌딩 블록 - 캐시/DB + 패턴 - 샤딩

### 자료 8: Elasticsearch architecture 공식 가이드
- 출처: https://www.elastic.co/search-labs/blog/elasticsearch-shards-and-replicas-guide
- 보강: https://www.elastic.co/blog/found-elasticsearch-top-down
- 신뢰성: 최상 (Elastic 공식)
- 핵심 주장: shard는 Lucene index. shard당 10~50GB / 200M docs 이하. replica는 운영 중에도 변경 가능. inverted index는 term → doc list 매핑이 핵심. ES default settings는 dev용 — production tuning 필수 (refresh_interval, indices.memory, JVM heap < 32GB).
- 인용 가능한 구절:
  > "An optimal shard should hold 10-50GB of data, with fewer than 200 million documents per shard."
- 관련 섹션: 빌딩 블록 - 검색 + 케이스 스터디 - Slack/Coupang 검색

### 자료 9: DynamoDB vs Cassandra (wide column LSM)
- 출처: https://www.hellointerview.com/learn/system-design/deep-dives/cassandra
- 보강: https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html (Cassandra 공식)
- 신뢰성: 최상 (Cassandra 공식), 중
- 핵심 주장: Cassandra는 LSM-tree, peer-to-peer, 모든 노드가 write 가능. DynamoDB는 managed + B-tree 기반 storage(추정). LSM은 write 압도적 (memtable→sstable flush, compaction 부담), B-tree는 read latency 예측 가능. partition key가 잘못되면 hot partition 발생.
- 관련 섹션: 빌딩 블록 - DB

### 자료 10: Vitess - YouTube MySQL sharding (PlanetScale)
- 출처: https://github.com/vitessio/vitess + https://planetscale.com/sharding
- 보강: https://blog.bytebytego.com/p/how-youtube-supports-billions-of
- 신뢰성: 최상 (Vitess 공식)
- 핵심 주장: YouTube 초기 MySQL → connection 한계 → Vitess 개발. connection pooling, query rewriting (cross-shard JOIN 차단), VSchema 기반 sharding key 관리. PlanetScale은 Vitess 기반 SaaS, 2025년 Postgres sharding(Neki) 발표 — Vitess MySQL 대비 from scratch.
- 관련 섹션: 빌딩 블록 - DB + 패턴 - 샤딩

---

## B. 분산 시스템 패턴

### 자료 11: Stripe Idempotency keys (Stripe blog + Brandur)
- 출처: https://stripe.com/blog/idempotency (Brandur Leach, 2017)
- 보강: https://brandur.org/idempotency-keys (Postgres 구현), https://brandur.org/fragments/idempotency-keys-crunchy
- 신뢰성: 최상 (Stripe 공식 + 저자 권위)
- 핵심 주장: idempotency key는 client-generated unique value. server는 key로 request status 저장 → 동일 key 재요청 시 cached response 반환. IETF Idempotency-Key 헤더 표준화 진행. Stripe는 결제 retry 안전성을 보장하기 위해 모든 mutation endpoint에 적용.
- 인용 가능한 구절:
  > "An idempotency key is a unique value generated by a client and sent to an API along with a request, with the server storing the key for bookkeeping the status of that request."
- 관련 섹션: 패턴 - 멱등성 + 케이스 스터디 - Stripe

### 자료 12: Saga pattern - choreography vs orchestration (microservices.io)
- 출처: https://microservices.io/patterns/data/saga.html (Chris Richardson)
- 보강: https://microservices.io/microservices/2019/12/02/sagas-part-4.html, https://www.infoq.com/articles/saga-orchestration-outbox/
- 신뢰성: 최상 (Richardson, Microservices Patterns 저자)
- 핵심 주장: Saga는 long-running 분산 트랜잭션을 local transaction의 sequence로 분해. choreography는 각 서비스가 event 발행/소비, decentralized — 추적 어려움. orchestration은 중앙 orchestrator가 명령 — 단일 가시성, 단점 SPOF. 보상 트랜잭션(compensating action) 설계가 핵심.
- 인용 가능한 구절:
  > "In choreography, services announce what they have done. In orchestration, a coordinator tells participants what to do."
- 관련 섹션: 패턴 - Saga

### 자료 13: Transactional Outbox + Debezium CDC (Debezium 공식)
- 출처: https://debezium.io/blog/2019/02/19/reliable-microservices-data-exchange-with-the-outbox-pattern/
- 보강: https://www.decodable.co/blog/revisiting-the-outbox-pattern
- 신뢰성: 최상 (Debezium 공식)
- 핵심 주장: dual-write 문제(DB 커밋 + 메시지 발행 atomic 불가) 해결책. 같은 트랜잭션으로 outbox 테이블에 event 행 insert → Debezium이 WAL/binlog tail해서 Kafka 발행. polling 불필요, near-zero latency, ordering 보존.
- 관련 섹션: 패턴 - Outbox/CDC + 케이스 스터디

### 자료 14: Event Sourcing + CQRS (Greg Young + Martin Fowler)
- 출처: https://martinfowler.com/bliki/CQRS.html
- 보강: http://codebetter.com/gregyoung/2010/02/13/cqrs-and-event-sourcing/ (Greg Young, 원조)
- 추가: https://medium.com/@hugo.oliveira.rocha/what-they-dont-tell-you-about-event-sourcing-6afc23c69e9a (실패담)
- 신뢰성: 최상 (Fowler, Young 원저)
- 핵심 주장: CQRS는 read/write 모델 분리. Event Sourcing은 state 대신 event log 저장. 둘은 별개 패턴이지만 자주 함께 쓰임. Fowler 경고: "복잡도 추가, 대부분 시스템은 CRUD로 충분하다". Hugo Rocha의 글은 "schema migration이 가장 어렵다 — event는 영원히 남는다"를 명확히 지적.
- 인용 가능한 구절 (Fowler):
  > "You should be very cautious about using CQRS... it can add significant complexity and make a significant drag on productivity."
- 관련 섹션: 패턴 - 이벤트 소싱/CQRS + 논쟁점

### 자료 15: Rate limiting algorithms (Cloudflare + Arcjet)
- 출처: https://blog.cloudflare.com/counting-things-a-lot-of-different-things/ (Cloudflare 자사 구현)
- 보강: https://blog.arcjet.com/rate-limiting-algorithms-token-bucket-vs-sliding-window-vs-fixed-window/
- 추가: https://smudge.ai/blog/ratelimit-algorithms (visualization)
- 신뢰성: 최상 (Cloudflare 공식)
- 핵심 주장: Token bucket = capacity + refill rate, burst 허용. Leaky bucket = constant rate egress. Fixed window = boundary burst 문제. Sliding window log = 정확하지만 메모리 비싸. Sliding window counter = 가중평균 근사, Cloudflare 실측 0.003% error로 사실상 표준. 대부분 API는 token bucket이 default가 적절.
- 관련 섹션: 패턴 - rate limiting + 케이스 스터디 - rate limiter

### 자료 16: 분산 retry/circuit breaker/bulkhead (AWS Builders' Library)
- 출처: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- 보강: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/circuit-breaker.html
- 신뢰성: 최상 (AWS Builders Library, 그들의 internal best practice 공개)
- 핵심 주장: retry는 동기화된 retry storm을 만들 수 있어 jitter 필수 (full jitter, equal jitter, decorrelated jitter). circuit breaker는 closed/open/half-open 3-state. bulkhead는 thread pool/connection pool 격리로 cascading failure 방지. AWS SDK는 2016년부터 token bucket 기반 client-side retry throttling.
- 인용 가능한 구절:
  > "Jitter adds randomness to backoff to spread retries around in time."
- 관련 섹션: 패턴 - resilience + 운영

### 자료 17: PACELC theorem (Marc Brooker + Daniel Abadi)
- 출처: https://brooker.co.za/blog/2014/07/16/pacelc.html (Marc Brooker, AWS Distinguished Engineer)
- 보강: https://www.designgurus.io/blog/system-design-interview-basics-cap-vs-pacelc
- 신뢰성: 최상 (Brooker는 AWS DB·storage 분야 권위자)
- 핵심 주장: CAP은 partition 시점만 다룸 — 평상시 latency/consistency trade-off도 결정해야 함. Else-Latency vs Else-Consistency (EL vs EC). Cassandra/Dynamo/Riak = PA/EL. Spanner = PC/EC. eventual consistency는 partition이 아니라 latency 때문에 선택되는 경우가 사실 더 많음.
- 인용 가능한 구절 (Abadi):
  > "Eventual consistency is often chosen for performance reasons during normal operation, not just for partition resilience."
- 관련 섹션: 패턴 - 일관성 + 논쟁점

### 자료 18: Martin Kleppmann CRDT & eventual consistency
- 출처: https://martin.kleppmann.com/2018/03/05/qcon-london.html (QCon 강연)
- 보강: https://martin.kleppmann.com/2016/11/03/code-mesh.html, https://queue.acm.org/detail.cfm?id=3546931 (ACM Queue "Convergence")
- 신뢰성: 최상 (Kleppmann, DDIA 저자)
- 핵심 주장: CRDT는 conflict-free replicated data type — concurrent update를 자동 merge하는 자료구조. G-Counter, PN-Counter, LWW-Element-Set, OR-Set, RGA(text), Yjs/Automerge 등. Riak·Redis(CRDT module)·Figma·Linear·CodeMirror 등 collaborative editing의 기반. OT(Operational Transform, Google Docs)와 비교 가능.
- 관련 섹션: 패턴 - 일관성 + 케이스 스터디 - 협업 도구

### 자료 19: Snowflake ID + base62 URL shortener
- 출처: https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly
- 보강: https://nileshblog.tech/designing-a-scalable-url-shortener-snowflake-ids-base62-encoding-and-microservices/
- 신뢰성: 중
- 핵심 주장: Twitter Snowflake는 64-bit (1 sign + 41 timestamp + 10 machine + 12 sequence). base62 (0-9,A-Z,a-z)는 7자로 ~3.5T 키. 단일 sequence 카운터로 hot spot 회피. 단 clock skew·NTP 재동기화 시 ID 충돌 가능 — NTP 모드를 slew(부드러운 조정)로 설정 권장.
- 관련 섹션: 패턴 - 분산 ID + 케이스 스터디 - URL shortener

### 자료 20: Lambda vs Kappa architecture (Kai Waehner)
- 출처: https://www.kai-waehner.de/blog/2021/09/23/real-time-kappa-architecture-mainstream-replacing-batch-lambda/
- 보강: https://hazelcast.com/foundations/software-architecture/kappa-architecture/
- 신뢰성: 최상 (Kai Waehner, Confluent)
- 핵심 주장: Lambda는 batch + speed + serving 3-layer — 코드 중복이 단점 (같은 로직을 batch와 stream에 각각). Kappa(Jay Kreps 제안)는 stream만으로 통일, 재처리 시 Kafka에서 replay. Flink·Kafka Streams 발전으로 Kappa가 mainstream화. 단 highly accurate batch가 필요한 financial reconciliation 등은 Lambda 적합.
- 관련 섹션: 패턴 - 데이터 파이프라인 + 논쟁점

---

## C. 케이스 스터디

### 자료 21: Discord - Cassandra → ScyllaDB 마이그레이션
- 출처: https://discord.com/blog/how-discord-stores-trillions-of-messages (Discord 공식)
- 보강: https://www.scylladb.com/tech-talk/how-discord-migrated-trillions-of-messages-from-cassandra-to-scylladb/
- 신뢰성: 최상 (Discord 공식 + ScyllaDB)
- 핵심 주장: 177 Cassandra → 72 ScyllaDB. p99 read 40~125ms → 15ms, p99 write 5~70ms → 5ms. 핵심: hot partition 문제 해결 위해 Rust로 작성한 data services 레이어(gRPC) 도입 — request coalescing으로 같은 메시지 다수 요청을 단일 DB call로 통합. 마이그레이션 도구는 Rust 작성, 예상 3개월을 9일로 단축. GC pause(JVM)에서 벗어남이 주요 동기.
- 인용 가능한 구절:
  > "Request coalescing is an important responsibility to avoid multiple database calls when many users request the same message."
- 관련 섹션: 케이스 스터디 - 채팅 + 빌딩 블록 - DB

### 자료 22: Slack 아키텍처 (10B+ messages)
- 출처: https://singhajit.com/slack-system-design/
- 보강: https://logz.io/blog/enterprise-observability-elasticsearch-challenge/ (KalDB)
- 신뢰성: 중
- 핵심 주장: workspace-based sharding (shop_id처럼 workspace_id 기준 DB shard). PHP WebApp(저장) + Java RTM(WebSocket 푸시). MySQL + Redis + S3 tiered storage. 검색은 Elasticsearch but logging은 자체 KalDB(ES 한계 극복). gRPC로 microservices 통신.
- 관련 섹션: 케이스 스터디 - 채팅 + 검색

### 자료 23: Twitter timeline (fan-out hybrid)
- 출처: https://blog.twitter.com/engineering/en_us/topics/infrastructure/2017/the-infrastructure-behind-twitter-scale
- 보강: https://blog.mi.hdm-stuttgart.de/index.php/2021/03/10/how-to-scale-real-time-tweet-delivery-architecture-at-twitter/
- 신뢰성: 최상 (Twitter 공식)
- 핵심 주장: 초기 fanout-on-write → MySQL 한계 → Manhattan(자체 key-value store) 개발. Redis cluster로 home timeline 캐싱. celebrity(10K+ followers) 예외 처리: fanout-on-read로 분리. 일반 사용자는 write 시 push, celeb는 read 시 merge. Twitter Engineering 2017 글 "The Infrastructure Behind Twitter"가 원전.
- 관련 섹션: 케이스 스터디 - 피드 + 패턴 - fan-out

### 자료 24: Instagram - Python/PostgreSQL/Cassandra (3 engineers → 14M users)
- 출처: https://read.engineerscodex.com/p/how-instagram-scaled-to-14-million
- 보강: https://betterengineers.substack.com/p/instagram-system-design
- 신뢰성: 중
- 핵심 주장: 초기 Python + PostgreSQL + memcached. 사진은 S3, EC2. fanout은 Gearman → 후에 Kafka로 변경. timeline은 Redis sorted set. follow list는 Redis. Twitter와 동일한 hybrid fanout 전략(celebrity 예외).
- 관련 섹션: 케이스 스터디 - 피드

### 자료 25: Netflix Open Connect CDN
- 출처: https://netflixtechblog.com/netflix-live-origin-41f1b0ad5371 (Netflix TechBlog, 2025 최신)
- 보강: https://freebsdfoundation.org/wp-content/uploads/2020/10/netflixcasestudy_final.pdf
- 신뢰성: 최상 (Netflix 공식)
- 핵심 주장: control plane(AWS) ↔ data plane(Open Connect) 분리. OCA(Open Connect Appliance)는 ISP 내부에 배치, 거의 전체 카탈로그 storage. 95% 트래픽이 AWS 안 거치고 Open Connect에서 직접 서빙. FreeBSD + sendfile() zero-copy로 disk → NIC 직송. SSL은 specialized NIC offload.
- 인용 가능한 구절:
  > "Around 95% of Netflix traffic is served from Open Connect without touching Netflix's AWS infrastructure at all."
- 관련 섹션: 케이스 스터디 - 스트리밍 + 빌딩 블록 - CDN

### 자료 26: Uber H3 + Dispatch (DISCO)
- 출처: https://www.uber.com/us/en/blog/h3/ (Uber 공식)
- 보강: https://systemdesigndoc.com/case-studies/how-uber-works/
- 신뢰성: 최상 (Uber 공식 + open source)
- 핵심 주장: 지구를 icosahedron으로 분할 → hexagon 계층 grid (resolution 0~15). 이웃 거리가 균등 — Voronoi와 routing 알고리즘에 유리. 매칭: pickup point → H3 cell → k-ring(이웃 cell)에서 driver 후보 set. DISCO(Dispatch Optimizer)는 wait time, repositioning cost, acceptance probability(ML), driver preference의 multi-objective 최적화.
- 관련 섹션: 케이스 스터디 - 매칭/공유 + 빌딩 블록 - geo

### 자료 27: Shopify Pods + Modular Monolith
- 출처: https://shopify.engineering/a-pods-architecture-to-allow-shopify-to-scale (Shopify 공식)
- 보강: https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity
- 추가: https://newsletter.techworld-with-milan.com/p/inside-shopifys-modular-monolith
- 신뢰성: 최상 (Shopify 공식)
- 핵심 주장: Ruby on Rails majestic monolith "Shopify Core" 유지. 내부적으로 Packwerk로 module boundary 강제. DB만 podding (MySQL cluster를 shop_id로 샤딩, 완전 독립 cluster). 무상태 컴포넌트는 K8s autoscale. Black Friday/Cyber Monday(BFCM) 트래픽 대응이 검증 무대.
- 인용 가능한 구절:
  > "Only the databases are podded since they are the hardest component to scale, and everything else that is stateless is scaled automatically."
- 관련 섹션: 케이스 스터디 - 멀티테넌트 + 패턴 - 샤딩 + 논쟁점 - 모놀리스/MSA

### 자료 28: Airbnb 검색 + 가용성 서비스
- 출처: https://airbnb.tech/uncategorized/embedding-based-retrieval-for-airbnb-search/ (Airbnb 공식)
- 보강: https://medium.com/airbnb-engineering/building-services-at-airbnb-part-3-ac6d4972fc2d
- 신뢰성: 최상 (Airbnb 공식)
- 핵심 주장: IVF(Inverted File Index) ANN을 HNSW 대비 채택 — high real-time update rate(가격/가용성 빈번 변경)에 적합. availability service는 reservation event를 구독, 동시성 충돌은 optimistic locking. SOA service platform standards로 모든 신규 서비스에 outlier detection·circuit breaker 강제.
- 관련 섹션: 케이스 스터디 - 검색/예약

### 자료 29: 토스 - 결제 레거시 현대화 + 코어뱅킹 MSA
- 출처: https://toss.tech/article/payments-legacy-1 (토스 tech)
- 보강: https://toss.tech/article/slash23-corebanking, https://toss.tech/article/22910 (Gateway), https://haon.blog/article/toss-slash/distribution-transaction/
- 신뢰성: 최상 (토스 공식)
- 핵심 주장: 토스페이먼츠는 hybrid cloud (Public + Private). 1% 단위 progressive rollout CI/CD platform. 토스뱅크는 코어뱅킹을 MSA로 전환 — "지금 이자 받기" 같은 대량 트래픽 ad-hoc feature가 가능해진 배경. 분산 트랜잭션은 SAGA + 2PC 혼합 적용.
- 관련 섹션: 케이스 스터디 - 결제 + 한국 실무 맥락

### 자료 30: LINE messaging-hub (전용 메시징 플랫폼)
- 출처: https://engineering.linecorp.com/ko/blog/about-messaging-hub-2 (LINE 공식)
- 보강: https://engineering.linecorp.com/ko/blog/how-line-messaging-servers-prepare-for-new-year-traffic/, https://engineering.linecorp.com/ko/blog/the-architecture-behind-chatting-on-line-live
- 신뢰성: 최상 (LINE 공식)
- 핵심 주장: connection-manager(WebSocket) ↔ message-router(gRPC) ↔ Kafka 큐. LINE LIVE 채팅은 Akka actor + Redis Cluster (상태 + queue). 새해 0시 트래픽이 정점 — 정상 평균의 수십 배. Apache HTTP client 버전 업그레이드가 성능 저하의 주범이 된 사례 등 실제 성능 회귀 디버깅 story가 풍부.
- 관련 섹션: 케이스 스터디 - 채팅 + 운영 - 트래픽 피크

### 자료 31: 당근마켓 채팅 + DynamoDB
- 출처: https://about.daangn.com/blog/archive/%EB%8B%B9%EA%B7%BC-%EC%B1%84%ED%8C%85%ED%8C%80-%EC%B1%84%EC%9A%A9-%EB%B9%84%EC%A0%84-%EB%AC%B8%ED%99%94/ (당근 공식)
- 보강: https://byline.network/2022/05/0512-2/, AWS Summit Korea 2022 - "2200만 사용자를 위한 채팅 시스템 아키텍처" (변규현)
- 신뢰성: 최상 (당근 공식 + AWS Summit 발표)
- 핵심 주장: 채팅을 별도 MSA로 분리 + 처음으로 Go 도입. DynamoDB를 채팅 storage로 선택 (Cassandra 운영 부담 회피). 푸시 알림은 Node.js로 초당 1500 RPS. "당근 채팅은 단순 메시지 전달이 아니라 hyperlocal 거래 매개"라는 도메인 시각이 특이점.
- 관련 섹션: 케이스 스터디 - 채팅 + 한국 실무 맥락

### 자료 32: 쿠팡 - 대용량 트래픽 백엔드 전략
- 출처: https://medium.com/coupang-engineering/대용량-트래픽-처리를-위한-쿠팡의-백엔드-전략-184f7fdb1367 (쿠팡 엔지니어링)
- 보강: https://medium.com/coupang-engineering/fueling-the-coupang-search-engine-c361c9896334 (검색 인덱싱)
- 신뢰성: 최상 (쿠팡 공식)
- 핵심 주장: core serving layer는 high availability를 최우선. 홈/검색/주문 페이지가 매출 직결. multi-tier cache (local + remote Redis + DB). 검색 indexing platform은 별도 — Coupang search engine은 ES 기반이지만 indexing pipeline은 자체 구축.
- 관련 섹션: 케이스 스터디 - 이커머스 + 한국 실무

### 자료 33: 카카오 인프라팀 + 공용 Kafka/RabbitMQ
- 출처: https://tech.kakao.com/posts/414 (인프라팀 소개)
- 보강: https://tech.kakao.com/2021/12/23/kafka-rabbitmq/ (공용 메시징 플랫폼), https://tech.kakao.com/posts/506 (광고 추천 Kafka 스트리밍)
- 신뢰성: 최상 (카카오 공식)
- 핵심 주장: 카카오 인프라팀은 모든 서비스의 1차 대응 조직 — DC, 네트워크, OS, DB, 모니터링까지. 공용 Kafka·RabbitMQ MessageQueue TF가 2021 정식 신설 — 서비스팀의 self-managed broker 문제 해결. "광고 추천"은 카프카 기반 streaming 데이터 플랫폼의 대표 사례.
- 관련 섹션: 케이스 스터디 - 메시징 인프라 + 한국 실무

### 자료 34: URL shortener (bit.ly 패턴)
- 출처: https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly
- 보강: https://www.systemdesignhandbook.com/guides/design-bitly/
- 신뢰성: 중
- 핵심 주장: write QPS는 적지만 read QPS는 매우 높음 (광고 redirect 등). Snowflake ID → base62 → 7 chars. Redis cache로 HOT URL 처리, CDN(Cloudflare) edge cache. analytics는 Kafka로 async. abuse 차단 (malware URL) 필수.
- 관련 섹션: 케이스 스터디 - URL shortener

---

## D. 운영·관측성·SRE

### 자료 35: Google SRE - SLO/SLI/Error Budget
- 출처: https://sre.google/workbook/implementing-slos/ (Google SRE Workbook)
- 보강: https://sre.google/workbook/error-budget-policy/, https://sre.google/workbook/alerting-on-slos/, https://www.datadoghq.com/blog/burn-rate-is-better-error-rate/
- 신뢰성: 최상 (Google 공식)
- 핵심 주장: SLI = good events / total events. SLO = SLI 목표 (예: 99.9%). Error budget = 1 - SLO (예: 0.1%). burn rate = 실제 에러율 / 허용 에러율 — 1이면 정시 소진, 2 이상이면 가속. multi-window multi-burn-rate alerting이 "1% 에러를 1시간 vs 1주" 같은 폭발/만성 양쪽 모두 잡는 표준.
- 인용 가능한 구절:
  > "If you have a 99.9% success ratio SLO, then a service that receives 3 million requests over a four-week period had a budget of 3,000 (0.1%) errors."
- 관련 섹션: 운영 - SLO

### 자료 36: Blameless postmortem culture (Google SRE)
- 출처: https://sre.google/sre-book/postmortem-culture/
- 보강: https://sre.google/sre-book/example-postmortem/ (실제 sample), https://incident.io/blog/sre-incident-postmortem-best-practices
- 신뢰성: 최상 (Google 공식)
- 핵심 주장: blameless는 "모두 그 순간 가진 정보로 최선을 다했다"는 전제. 의료·항공에서 기원. 핵심: blame culture → incident 은폐 → 더 큰 리스크. Google template은 timeline, root cause, action items, what went well, what went wrong, lessons learned. action item은 owner + due date 필수.
- 관련 섹션: 운영 - incident response + 한국 실무 - postmortem 도입기

### 자료 37: OpenTelemetry - 통합 telemetry standard
- 출처: https://opentelemetry.io/docs/concepts/observability-primer/
- 보강: https://opentelemetry.io/docs/specs/otel/logs/, https://www.dash0.com/knowledge/logs-metrics-and-traces-observability
- 신뢰성: 최상 (CNCF 공식)
- 핵심 주장: 3 signals: traces, metrics, logs. 모두 OTLP wire format으로 통일. OTel Collector가 production에서 batching·filtering·routing 담당. trace_id로 logs/metrics를 trace에 자동 correlation. 기존 vendor lock-in(Datadog agent, NewRelic agent)을 OSS로 대체.
- 관련 섹션: 운영 - 관측성

### 자료 38: Netflix Chaos Engineering (Chaos Monkey + Simian Army)
- 출처: https://principlesofchaos.org/ (Principles of Chaos Engineering, Netflix 공식 community)
- 보강: https://www.gremlin.com/chaos-monkey, https://medium.com/@tahirbalarabe2/what-is-chaos-engineering-chaos-by-design-fad9e39ab5e0
- 신뢰성: 최상 (Netflix 공식 community)
- 핵심 주장: Chaos Monkey(2011)는 production VM 무작위 종료. Simian Army는 Latency Monkey, Conformity Monkey, Janitor Monkey, Chaos Gorilla(AZ 종료), Chaos Kong(region 종료)으로 확장. 4 원칙: hypothesis 정의 → real-world event 시뮬레이션 → production 환경에서 → blast radius 최소화. 핵심은 "장애를 예방하는 게 아니라 장애 내성을 검증한다".
- 관련 섹션: 운영 - 장애 내성

### 자료 39: 배포 전략 - blue-green vs canary vs feature flag (LaunchDarkly)
- 출처: https://launchdarkly.com/blog/deploying-without-downtime/
- 보강: https://harness.io/blog/blue-green-canary-deployment-strategies, https://www.improwised.com/blog/blue-green-vs-canary-deployment/
- 신뢰성: 최상 (LaunchDarkly 공식)
- 핵심 주장: blue-green = 두 환경 + 트래픽 스위치. canary = 일부 트래픽 → 모니터링 → 점진 확대. feature flag = 코드 배포 ≠ 기능 노출 (deploy/release decoupling). Progressive delivery = canary + flag. Argo Rollouts/Flagger는 metric-based auto-promotion. "deploy를 두려워하지 않는 조직"의 핵심 인프라.
- 관련 섹션: 운영 - 배포

### 자료 40: AWS Builders Library - timeouts/retries (재정리)
- 출처: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- 신뢰성: 최상
- 핵심 주장: timeout은 latency 분포의 p99.9 + 여유. retry는 transient failure 한정, idempotent 한정. backoff는 exponential 기본, jitter 필수. AWS SDK 모든 client는 client-side throttling (token bucket) 기본 적용.
- 관련 섹션: 운영 - 클라이언트 신뢰성

### 자료 41: 카카오뱅크 기술 블로그 (운영·신뢰성)
- 출처: https://tech.kakaobank.com/
- 신뢰성: 최상 (카카오뱅크 공식)
- 핵심 주장: 금융권 시스템의 99.99% 가용성 요건, 감사 추적, 24/7 운영. 메인프레임 마이그레이션, MSA 적용, 거래 일관성 확보 사례. 책에서 한국 금융권 인프라의 특수성(전자금융감독규정, 망 분리 등)을 다룰 때 1차 자료로 활용.
- 관련 섹션: 한국 실무 + 운영

### 자료 42: Marc Brooker - distributed systems 일반 (보강)
- 출처: https://brooker.co.za/blog/
- 신뢰성: 최상 (AWS Distinguished Engineer)
- 핵심 주장: AWS Lambda, Aurora 등의 architect가 운영하는 블로그. "100% reliable systems don't exist" → 95~99.99% 사이에서 어떻게 trade-off할지. PACELC 외에도 latency budgets, scaling laws 글들 다수.
- 관련 섹션: 패턴 + 운영 (저자 권위 자료)

### 자료 43: ByteByteGo system design newsletter (인덱스 자료)
- 출처: https://blog.bytebytego.com/
- 신뢰성: 중 (Alex Xu 운영, 인터뷰 책 저자라 깊이는 변동, 인덱스 용도로 유용)
- 핵심 주장: 광범위한 case study를 시각화. Discord/Slack/Shopify/YouTube 등 위에서 다룬 자료 다수가 ByteByteGo에 요약 형태로 있음. 책에서 다이어그램 영감 또는 비교 자료로 활용 가능.
- 관련 섹션: 케이스 스터디 보강

### 자료 44: Service mesh - Istio vs Linkerd 비교 (Buoyant)
- 출처: https://www.buoyant.io/linkerd-vs-istio
- 보강: https://arxiv.org/html/2411.02267v1 (mTLS 성능 정량 비교)
- 신뢰성: 최상 (Linkerd 모회사 — 다소 편향, 정량 데이터는 신뢰)
- 핵심 주장: mTLS 적용 시 latency: Istio +166%, Linkerd +33%, Istio Ambient +8%. Linkerd proxy는 Envoy 대비 메모리 5~10배 적음. Istio는 feature 풍부·복잡, Linkerd는 simple·efficient. ambient mesh(sidecar-less)가 새 트렌드.
- 관련 섹션: 빌딩 블록 - 서비스 메시 + 논쟁점

### 자료 45: 네이버 검색 (대규모 분산 검색 엔진)
- 출처: https://naver-career.gitbook.io/kr/service/search/engine-and-solution/search-engine
- 보강: 네이버 D2 (https://d2.naver.com/) 에 검색·인프라 관련 글 다수 (개별 글 링크는 필요 시 챕터 저술 시 추가 발굴)
- 신뢰성: 최상 (네이버 공식)
- 핵심 주장: 매초 수천 query, 수십억 문서. 분산 색인·분산 검색 자체 구현, ES 외에 자체 엔진(NSE 등) 운영. 한국어 형태소 분석(NORI, KOMORAN, Mecab-ko) 고려가 한국 검색의 특수성.
- 관련 섹션: 케이스 스터디 - 검색 + 한국 실무 - 한국어 처리

---

## 수집 한계

- **접근 실패한 자료**: 네이버 D2의 개별 article URL을 다수 검색했으나 키워드 매칭이 약했음. 챕터별로 깊이 들어갈 때 직접 d2.naver.com 사이트 검색이 필요.
- **개별 글 미발굴**: Cloudflare engineering blog의 "How we built a real-time global rate limiter" 같은 특정 포스트는 일반 검색으로는 떠올랐지만 모든 글을 개별 검증하진 않았음. 책 저술 단계에서 보강 필요.
- **카카오뱅크 개별 글**: blog index만 확보, 개별 article 깊이 탐색은 후속 단계로 미룸.
- **의도적 제외**: "system design interview" 위주 사이트(GeeksForGeeks의 일반 정리글, Educative 인터뷰 코스)는 인덱스 1~2건만 포함. 본 책은 인터뷰 대비서가 아니므로 깊이가 부족한 자료는 배제.
- **DDIA 본문**: Martin Kleppmann의 책 "Designing Data-Intensive Applications"는 web 자료가 아니므로 paper-researcher가 다룰 영역. 본 리서치에서는 Kleppmann의 공개 글·talk만 수집.
- **OKKY/HN/Reddit thread**: community-researcher의 영역으로 명시적 배제.

---

자료 분배 요약:
- A. 빌딩 블록: 10건 (자료 1~10)
- B. 분산 패턴: 10건 (자료 11~20)
- C. 케이스 스터디: 14건 (자료 21~34)
- D. 운영·SRE: 11건 (자료 35~45)
- 한국 자료 비중: 토스, 라인, 당근, 쿠팡, 카카오, 카카오뱅크, 네이버 = 7건 (~15%)
- 공식 docs·자사 engineering blog: ~30건 (~67%)
