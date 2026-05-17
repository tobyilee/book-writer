# 시스템 디자인 핸드북 — 저술 계획

작성일: 2026-05-16
대상: 3~7년차 실무 백엔드 엔지니어 (인터뷰 대비 X, production 운영 가이드 O)
구성 철학: Bottom-up — 빌딩 블록 → 패턴 → 케이스 스터디
기준 분량: 22 챕터(0장 포함) + 부록 1개, 총 ~478페이지
저자: Toby-AI

---

## 1. 책 제목 후보 3개

### 후보 A. **현장에서 살아남는 시스템 디자인**
- **부제:** 작은 internal 시스템부터 글로벌 SaaS까지, 백엔드의 빌딩 블록·패턴·케이스 스터디
- **Logline:** "면접이 아닌 production에서 통하는 설계 감각."
- **포지셔닝/정서:** 인터뷰서 일색의 한국 시장에서 "이 책은 다르다"를 정면으로 선언. 운영 현장의 고생을 인정하는 동료적 톤. *Acing*과 가장 대비되는 제목.

### 후보 B. **시스템 디자인 실전 핸드북 — 빌딩 블록부터 글로벌 서비스까지**
- **부제:** 캐시·큐·DB·합의·샤딩·채팅·피드·결제를 한 권으로
- **Logline:** "옆에 펴두고 매일 참조하는 백엔드 사전."
- **포지셔닝/정서:** "사전(handbook)"이라는 무거운 신뢰감. 책장에 오래 꽂아두고 싶은 reference 본능을 자극. 가장 보수적·안전한 제목.

### 후보 C. **분산 시스템, 어떻게 짜고 어떻게 굴리는가**
- **부제:** 한국 백엔드를 위한 시스템 디자인 — 부품·패턴·실제 사례·운영
- **Logline:** "설계도 운영도 모두 다루는 한국형 시스템 디자인 책."
- **포지셔닝/정서:** 질문형 제목으로 호기심 자극. "한국 백엔드"를 부제에 명시해 독자 식별성 ↑. *Acing*·DDIA·Alex Xu 모두 영어책이라는 점을 정면 차별화.

### 추천: **후보 A — "현장에서 살아남는 시스템 디자인"**
이유: (1) 실무 가이드라는 정체성을 가장 직접 드러냄. (2) "살아남는다"는 동사가 운영 고생을 인정하는 동료적 정서를 만든다 — Toby 문체의 "공감대 형성"과 일치. (3) *Acing*과 정반대 방향("이 책은 통과용이 아니라 매일을 위한 책")을 한 문장에 압축. (4) 한국 독자에게 친숙한 표현(살아남기, 현장)이라 서점 진열에서 눈에 띈다.

---

## 2. 책의 특성

- **장르:** 기술서 — 실무 가이드 (입문서 X, 인터뷰 대비서 X)
- **분량:** 0장 + 1~20 (20 챕터) + 부록 A, 약 462페이지
- **난이도:** 중급~고급. 3~7년차 백엔드 (Spring/Node/Go/Python 어느 쪽이든)
- **독자 여정 (Before → After):**
  - **Before:** 캐시·큐·DB를 "쓸 줄은 안다." 단일 시스템은 만들어 봤지만, 트래픽이 커지거나 장애가 나면 무엇을 어디서부터 의심해야 하는지 모른다. 시중 인터뷰 책을 읽었으나 "내일 production에서 뭘 해야 하지"에는 답이 안 됨.
  - **After:** 각 빌딩 블록의 trade-off를 자기 도메인 언어로 설명할 수 있다. 모든 새 기능에 "이 부분이 깨지면 어떻게 되는가"를 자동으로 떠올린다. 채팅·피드·결제 같은 대표 시스템의 설계 결정을 자기 회사 코드에 매핑해서 본다. 장애 회의에서 "우리 hot partition일 가능성 있어요" 같은 진단 어휘로 말할 수 있다.

- **차별화 (시중 대비):**
  - *Acing the System Design Interview* (Manning): 인터뷰 통과가 목표라 의사결정 trade-off를 압축적으로 다룸. 운영·on-call·한국 맥락은 거의 없음. → **본 책은 인터뷰 통과가 아닌 production 운영을 목표로 한다.** *Acing*은 토픽 카탈로그로만 활용.
  - *Designing Data-Intensive Applications* (Kleppmann): 이론·논문 기반이 강력하나 두껍고 추상적. 한국 사례·요즘 운영 문화(SLO·OpenTelemetry·on-call·FinOps)는 부분 커버. → **본 책은 DDIA의 이론을 한국 백엔드 일상으로 번역하는 layer.** DDIA를 다 읽은 사람도 "그래서 우리 회사 어디서 어떻게 쓰지"의 답을 얻는다.
  - *System Design Interview* (Alex Xu): 케이스 스터디 위주, 그림 친화적. trade-off 깊이·운영 관점·논쟁점은 옅다. → **본 책은 그림보다 trade-off 표·실패담·한국 사례·논문 인용으로 무게를 둔다.**
  - **보안 본문 편입:** 시중 인터뷰서 3종은 모두 보안을 "별도 책의 주제"로 미루거나 한 페이지로 처리. → **본 책은 보안(인증·인가·secret·망분리)을 9장 빌딩 블록의 일부로 본문 16p 본격 다룬다.** 한국 망분리·전자금융감독규정 맥락이 이 챕터의 차별화 핵심.
  - **AI/LLM 본문 챕터 거절:** 사용자 결정 — AI/LLM 인프라(vector DB·RAG·LLM serving)는 본 책의 정체성(분산 시스템 fundamental)에서 한 발 떨어진 주제이며, 2026년 이후 빠르게 변할 영역이라 본문 챕터로는 시기상조다. 별권에서 다룰 주제로 남기고, 부록 1페이지 "다음 책의 약속"으로만 시야를 던진다.

- **한국 독자 맥락:** 다음 4가지를 의도적으로 녹인다.
  1. **0시 동시 트래픽 (한국 1):** 이자 받기·청약·콘서트 예매 등 정시 burst — *Acing*에는 없는 패턴. 캐시·rate limiting·queue 챕터에 한국 사례로 등장.
  2. **본인인증·PG 결제 vendor lock-in (한국 8):** wrapper layer 설계, failover. 결제 챕터의 핵심.
  3. **망분리·하이브리드 클라우드 (한국 2, 9):** 토스 hybrid, LINE 자체 IDC, 2022 카카오 화재. 보안·운영·인프라 챕터의 한국적 색깔.
  4. **한국어 형태소 분석 (한국 3):** 검색 챕터에서 "영어 분석기로는 '쿠팡 배송' 못 찾는다" 사례.

  추가로 한국 백엔드의 Java/Spring·우아한형제들 모듈러 모놀리스·당근 hyperlocal·카카오톡 메시지 fan-out 등을 케이스 스터디 챕터마다 1~2개씩 박아 둔다. 영어책에서 못 본 사례가 항상 한 챕터에 한 번씩 등장하도록.

---

## 3. 챕터 목록

총 21 챕터 (0장 + 1~20장) + 부록 A. 1부(빌딩 블록) 9 챕터 · 2부(패턴) 6 챕터 · 3부(케이스) 5 챕터 + 부록 1.

> 사용자 결정 (2026-05-16 라운드 2): 보안 챕터(현 9장)를 1부에 신설, AI/LLM 챕터는 부록 1페이지 유지로 거절.

### 0장. 들어가며 — 이 책을 어떻게 읽을 것인가
- **부제:** 약속 · 표기 규약 · 4축 지형도 · 도입의 자격
- **3부 위치:** 서장
- **핵심 질문:** 시스템 디자인이라는 광활한 영역에서, 이 책은 어디를 비추고 어디는 비추지 않는가? 그리고 우리가 "도입할까"라고 묻기 전에 묻어야 할 질문은 무엇인가?
- **주요 내용:**
  - 이 책이 인터뷰서가 아닌 이유, *Acing*·DDIA·Alex Xu와의 관계.
  - 4축 지형도(빌딩 블록·패턴·케이스·운영) 한 페이지 다이어그램 — `01_reference.md` §1 인용.
  - 독자가 가져야 할 사전 지식 (HTTP·SQL 기초·하나 이상의 백엔드 프레임워크).
  - 표기 규약: 인용 (논문·blog·커뮤니티), trade-off 표 형식, "검증 필요" 라벨.
  - **이 책의 6가지 약속** (§5에서 회수) 미리 제시.
  - 챕터 의존도 맵 — 1·2·3부 중 어느 챕터를 어느 챕터 뒤에 읽으면 되는지 그림.
  - **"이력서용 기술 도입의 함정"** 섹션 (3p) — 한국 10 패턴 인용. "Kafka를 이력서에 쓰려고 도입했다, 실제로는 RabbitMQ면 충분했다." 모든 챕터를 "도입할까"가 아닌 "도입할 자격이 있는 결정인가"로 읽도록 만드는 메타 시각.
- **독자가 얻는 것:** "이 책에서 무엇을 기대해야 하고 기대하지 말아야 하는가"의 명료한 그림. 더불어 각 챕터를 읽을 때 "이 도구의 도입 자격을 우리 팀은 충족하는가"라는 자기 검증의 습관.
- **도입부 hook:** "어느 새벽, 결제 시스템 장애 회의를 마치고 자리에 돌아왔다고 해보자. 회의에서는 '아무래도 hot partition 같다'는 말이 오갔다. 정확히 무슨 뜻인지 다시 확인하고 싶다 — 그런데 책장에 꽂힌 인터뷰 책을 펴봐도, 그 단어 옆에는 '이렇게 답하면 통과'라고만 적혀 있다. 우리는 지금 통과가 아니라 답을 알고 싶다."
- **예상 분량:** 13페이지

---

## 1부. 빌딩 블록 — 시스템을 이루는 부품들

9개 챕터. 각 부품의 정의·trade-off·운영 함정·한국 사례. "이 부품을 우리 회사에 도입할까 말까" 결정에 필요한 모든 것. 마지막 9장(보안)이 모든 빌딩 블록 위에 깔리는 control plane으로 자리잡는다.

### 1장. 관계형 DB — 시스템의 backbone을 다시 보기
- **3부 위치:** 1부 (빌딩 블록)
- **핵심 질문:** Postgres/MySQL을 10년 써왔는데도 어제 빠르던 쿼리가 오늘 5초 걸리는 이유를 설명할 수 있는가?
- **주요 내용:**
  - 왜 RDB가 여전히 90% 시스템의 기본인가 (휴리스틱 3 "Just use Postgres" 인용).
  - B+ tree 인덱스 구조 — `01_reference.md` §2.10 + P22 *Database Internals*.
  - Index 함정: composite 순서, implicit type conversion, statistics stale (커뮤니티 패턴 5).
  - Connection pool sizing: HikariCP 공식 `(core × 2) + spindle`, 휴리스틱 2.
  - Postgres VACUUM·transaction wraparound (tribal #8).
  - Aurora의 "log is the database" — P14 SIGMOD'17 인용, 1챕터 안에서 distributed RDB로 살짝 시야 확장.
  - 한국 사례: 토스 SLASH 23 결제 DB 디버깅 발표 — "통계 정보 갱신 안 된 게 진짜 자주" (한국 1, 패턴 5).
  - **한국 6 sidebar (2p):** "JPA N+1과 우아한형제들의 진단 패턴" — ORM이 만든 silent killer. 우아콘 발표 인용. 5장 검색 indexing pipeline과는 다른 한국 백엔드의 일상 함정.
  - Trade-off 표: Postgres vs MySQL vs Aurora vs CockroachDB (W4 + Abadi 비판 W17).
- **독자가 얻는 것:** 느린 쿼리 디버깅을 "인덱스 추가"가 아닌 "쿼리 형태 의심"부터 시작하는 습관 + JPA를 쓰는 한국 백엔드의 N+1 자동 탐지 패턴.
- **도입부 hook:** "어제 50ms이던 쿼리가 오늘 5초가 되는 경험을 안 해 본 백엔드 개발자가 있을까? 새벽에 alert가 울려 들어왔는데, slow query log를 펴 보니 어제와 같은 쿼리다. 인덱스 빠진 것도 아닌데."
- **예상 분량:** 24페이지

### 2장. NoSQL — Dynamo 계열과 Bigtable 계열을 가르기
- **3부 위치:** 1부
- **핵심 질문:** "schema가 유연해서" 또는 "확장이 쉬워서" NoSQL을 골랐다면, 도대체 무엇을 양보한 것인가?
- **주요 내용:**
  - Dynamo 계열 (P7, leaderless, eventual, vector clock) vs Bigtable 계열 (P8, single-leader per tablet, strong, Chubby).
  - Cassandra (P9), DynamoDB, ScyllaDB 비교표 — W9 hello interview + 패턴 2.
  - LSM-tree 내부 (P13 원전 + P22) — write-heavy의 이유.
  - **Hot partition** — 평생의 적. partition key 설계 anti-pattern. 5분의 "신부보다 잔인한 디버깅" (패턴 2, C2).
  - Tombstone (tribal #16), bloom filter false positive (tribal #7).
  - 한국 사례: 당근 채팅 DynamoDB 선택 이유 ("Cassandra 운영 부담 회피", W31, 한국 7).
  - Discord Cassandra → ScyllaDB 마이그레이션 (W21) — 케이스 스터디 11장에서 깊게 다룬다는 callback.
- **독자가 얻는 것:** "NoSQL은 schema-less가 아니라 query-first다"는 mental model. Partition key 첫 줄을 보면 hot 가능성을 직감.
- **도입부 hook:** "AWS Summit에서 한 발표자가 말했다. 'DynamoDB 마이그레이션 중에 부하 테스트는 다 통과했다. 그런데 출시 30분 만에 한 partition이 전체 트래픽의 95%를 받기 시작했다.' 회사에 celebrity 사용자가 있었다는 사실은 그날 밤 12시에 알게 됐다."
- **예상 분량:** 22페이지

### 3장. 캐시 — 거의 모든 시스템의 첫 번째 latency 무기
- **3부 위치:** 1부
- **핵심 질문:** 캐시를 한 번이라도 비워본 경험이 있다면, 그날 DB가 무사했는가?
- **주요 내용:**
  - 캐시 위치: client / CDN / edge / app-level / 분산 (Redis·Memcached) / DB internal.
  - 4가지 패턴: cache-aside (default) / read-through / write-through / write-back. 다이어그램 4장.
  - Redis vs Memcached 비교표 — W1·W2.
  - **Thundering herd / cache stampede** — 휴리스틱 4 + 패턴 4. probabilistic early expiration, singleflight, jittered TTL.
  - Eviction: LRU·LFU·random·TTL. Redis maxmemory-policy.
  - Multi-tier: L1 in-process (Caffeine, Guava) + L2 Redis. consistency 관리.
  - 한국 사례: 카카오 if(kakao) 2021 "트래픽 폭증과 캐시 정책" — single key TTL 동시 만료 (패턴 4); 우아한형제들 배민 jittered TTL + lazy refresh.
  - **Callback 예고:** 14장 피드 시스템에서 "fanout cache"로 재등장.
- **독자가 얻는 것:** 캐시 미스가 cascading failure로 번지는 시나리오 4가지와 각각의 방어 패턴.
- **도입부 hook:** "한 번이라도 production Redis를 FLUSHDB 해본 적이 있다면, 그 다음 1분 동안 무슨 일이 벌어졌는지 생생할 것이다. DB CPU가 100%를 찍고, p99 latency가 30초로 솟구치고, alert가 도미노처럼 울린다. 캐시는 무기지만, 한 번 잘못 쓰면 우리 손에서 폭발한다."
- **예상 분량:** 24페이지

### 4장. 메시지 큐 — 비동기와 decoupling의 토대
- **3부 위치:** 1부
- **핵심 질문:** Kafka·RabbitMQ·SQS 중 하나를 고르는 결정을 trade-off 표 한 장으로 설명할 수 있는가?
- **주요 내용:**
  - "Simple broker, complex consumer" vs "Complex broker, simple consumer" — Kafka(W3) vs RabbitMQ.
  - Kafka 핵심: partition·offset·consumer group·log retention. KRaft (P3 + ZooKeeper 탈피, §2.8).
  - RabbitMQ 핵심: exchange·queue·routing key. Jack Vanlightly 시리즈(W3).
  - SQS/SNS, Pulsar 짧게 (P19).
  - Delivery semantic: at-most-once / at-least-once / exactly-once의 진짜 의미.
  - 운영 함정: consumer lag, rebalance storm (tribal #5), retention 짧음 + consumer down → 데이터 loss (패턴 6).
  - 한국 사례: 카카오 공용 메시징 플랫폼 TF (W33), LINE Apache HTTP client 업그레이드로 throughput 1/3 (W30) — "어떻게 그게 가능?" 실패담.
  - **Callback 예고:** 9장 Transactional Outbox·10장 Saga·17장 결제에서 재등장.
- **독자가 얻는 것:** 큐를 도입할 때 묻게 되는 6가지 trade-off 질문 체크리스트 + 운영 모니터링 5가지.
- **도입부 hook:** "오전 9시 Slack에 '큐 lag 4시간'이라는 메시지가 뜬다. 누가 봐도 1주일 전 배포가 원인이지만, 누구도 처음엔 그 배포를 의심하지 않는다. 어제까지 멀쩡했으니까. 큐는 조용히 망가지고, 큐 모니터링이 없으면 우리가 쌓아둔 메시지가 어떤 모양으로 망가지는지 보지 못한다."
- **예상 분량:** 24페이지

### 5장. 검색 엔진 — 한국어가 영어 분석기로 안 되는 이유부터
- **3부 위치:** 1부
- **핵심 질문:** Elasticsearch shard 100개로 뭘 하려는 것인가? 그게 정말 필요한 결정이었는가?
- **주요 내용:**
  - Inverted index 기본 — Lucene 작동 원리 한 장 그림.
  - ES vs OpenSearch 분기, 자체 엔진(LINE NSE·다음 검색·네이버) — W8, W45, 한국 3.
  - Shard 설계 원칙: 10~50GB / 200M docs 이하 (W8). JVM heap 32GB 이하 (휴리스틱 1, compressed oops).
  - `refresh_interval` 1초 default 함정 (tribal #17) — write 많으면 30초.
  - **한국어 형태소 분석:** mecab-ko, NORI, Khaiii, KIWI. "쿠팡 배송 vs 쿠팡배송" (한국 3).
  - 케이스: 쿠팡 검색 Kafka 기반 indexing pipeline (W32), Slack 검색 KalDB (W22).
  - Vector search / ANN — Airbnb IVF over HNSW (W28) — 15장에서 callback.
- **독자가 얻는 것:** 한국어 검색을 위한 분석기 5종 비교 + ES 운영의 5가지 함정.
- **도입부 hook:** "어떤 신입 개발자가 검색 페이지를 만들었다. 사용자는 '쿠팡 배송'을 검색했는데 '쿠팡배송'이라는 띄어쓰기가 다른 글이 안 잡혔다. 영어로 만든 검색을 한국어에 그냥 갖다 쓰면 이렇게 된다 — 한국어는 띄어쓰기와 조사가 검색을 어렵게 만든다. 영어권 책에는 이 문제가 등장하지 않는다."
- **예상 분량:** 22페이지

### 6장. 로드 밸런서·게이트웨이·서비스 메시
- **3부 위치:** 1부
- **핵심 질문:** L4와 L7의 차이를 운영 관점에서 설명할 수 있고, 서비스 메시가 정말 우리 팀에 필요한지 정량으로 답할 수 있는가?
- **주요 내용:**
  - L4 (TCP/UDP) vs L7 (HTTP/HTTPS) — TLS termination 위치.
  - HAProxy (raw 빠름) / NGINX (workhorse) / Envoy (cloud-native) 비교 — Loggly 벤치마크 W5.
  - API Gateway 패턴 — Kong, AWS API Gateway, Spring Cloud Gateway.
  - **Service mesh:** Istio · Linkerd · Cilium. mTLS·observability·traffic split의 진짜 비용.
  - 정량 비교 — W44: Istio mTLS +166% latency, Linkerd +33%, Istio Ambient +8%, HAProxy 메모리 50MB vs Envoy 150MB.
  - "Mesh 도입했더니 ops 자살" — 논쟁 G와 연계, 5명 팀 ≠ K8s + Istio.
  - 한국 사례: 토스·우아한형제들·라인 mesh 도입 vs 미도입.
- **독자가 얻는 것:** 서비스 메시를 "도입할까"가 아닌 "어디까지 필요한가"로 분해해서 정량적으로 답하는 framework.
- **도입부 hook:** "어느 5명짜리 팀이 우리도 service mesh를 써보자며 Istio를 깔았다. 3개월 후, 그 팀은 mesh를 '튜닝'하느라 한 주의 절반을 보내고 있었다. 본업이 무엇이었는지 점점 흐려진다."
- **예상 분량:** 18페이지

### 7장. CDN·엣지·객체 스토리지 — 사용자 가까이로 가는 길
- **3부 위치:** 1부
- **핵심 질문:** Netflix는 왜 자기 트래픽의 95%를 AWS를 거치지 않고 보내고 있는가?
- **주요 내용:**
  - CDN 기본: PoP·anycast·edge cache·origin shield. Cloudflare 330+ city (W6).
  - **Edge compute:** V8 isolates (Cloudflare Workers) — cold start <5ms vs Lambda ~수백 ms.
  - Netflix Open Connect 케이스 — W25, control(AWS) vs data(자체 ISP-깊은 캐시) 분리, FreeBSD sendfile() zero-copy.
  - 객체 스토리지: S3, GCS, Azure Blob — durability 11 9's, tiered storage, lifecycle policy.
  - S3 함정: list 비용, request rate per prefix, multipart upload.
  - DDoS 방어: anycast + scrubbing center. Cloudflare 2024 사례.
  - 한국 사례: 네이버 CDN, 카카오엔터 콘텐츠 CDN, 한국 캐시 운영.
- **독자가 얻는 것:** "edge에서 처리할 수 있는 것"과 "origin이 해야 할 것"을 가르는 4가지 기준.
- **도입부 hook:** "우리 서비스에 트래픽이 10배 늘면 AWS 청구서는 몇 배 늘까? 답은 '아키텍처에 따라 다르다'다. Netflix는 트래픽의 95%를 자기 ISP 깊은 곳에서 처리해서 AWS 청구서가 거의 안 늘었다. 이게 가능하다는 사실 자체가 우리 설계를 다시 보게 한다."
- **예상 분량:** 18페이지

### 8장. 시간·순서·분산 ID — 분산 시스템의 가장 어두운 코너
- **3부 위치:** 1부
- **핵심 질문:** "지금 몇 시야?"라는 질문에 분산 시스템은 어떻게 답하는가? 그리고 답을 못 한다면, 무엇으로 대신하는가?
- **주요 내용:**
  - Lamport "Time, Clocks" 1978 (P4) — happens-before, 부분 순서.
  - Logical clock vs Vector clock vs Hybrid Logical Clock (CockroachDB) vs TrueTime (Spanner P5).
  - NTP slew vs step (tribal #1) — Snowflake ID 충돌 위험.
  - **분산 ID:** Snowflake (1+41+10+12, W19) · ULID · UUIDv7. timestamp prefix의 가치.
  - **Timezone hell** — UTC 저장 + local 표시의 함정, DST, IANA tz 업데이트 (패턴 3).
  - 분산 lock: Redis Redlock 비판 (Kleppmann vs antirez 논쟁), ZooKeeper · etcd 기반 lock.
  - 한국 사례: 토스 SLASH 22 "분산 시스템에서 시간 다루기" — OKKY 호평 (패턴 3).
- **독자가 얻는 것:** "이 데이터에 진짜 시간 보장이 필요한가, 아니면 순서만 있으면 되는가"를 가르는 의사결정 트리.
- **도입부 hook:** "DST 전환 새벽 2시에 cron이 두 번 또는 0번 실행되는 버그는 매년 봄·가을마다 트위터에 올라온다. 그리고 매년, 새로운 백엔드 개발자들이 같은 함정에 빠진다. 분산 시스템에서 '몇 시야?'는 가장 어려운 질문 중 하나다."
- **예상 분량:** 20페이지

### 9장. 분산 시스템의 보안 — 인증·인가·secret·망분리
- **3부 위치:** 1부 (빌딩 블록 마지막)
- **핵심 질문:** 우리 시스템의 모든 network 호출은 누구에게 "나는 누구다"를 어떻게 증명하는가? 그리고 그 증명서를 잃어버리지 않을 자신이 있는가?
- **주요 내용:**
  - **분산 환경 위협 모델 3축:** service-to-service (내부 service 간), user-to-service (외부 사용자 → API), admin-to-system (운영자 → 인프라). 각 축의 신뢰 경계와 공격 표면.
  - **인증·인가의 두 단계 구분:** OAuth2/OIDC 인가 코드 grant·implicit·client credentials·PKCE, JWT 검증·만료·refresh token rotation, RBAC vs ABAC. token 흐름 다이어그램 한 장.
  - **서비스 간 신뢰:** mTLS, service identity, SPIFFE/SPIRE 개념, service mesh의 mTLS 자동화 (6장 LB·메시 callback).
  - **Secret 관리:** 평문 금지, 환경변수의 함정(`.env` 커밋·CI 로그 leak), HashiCorp Vault·AWS Secrets Manager·GCP Secret Manager·KMS, **rotation·revocation 자동화**가 진짜 운영 과제.
  - **한국 환경의 망분리 (한국 2·9):** 전자금융감독규정·공공기관·일부 대기업의 망분리 요건이 클라우드 아키텍처에 미치는 영향. hybrid cloud, VPN/Direct Connect, 망분리 환경의 CI/CD 사례 — 토스 hybrid cloud, LINE 자체 IDC, 카카오뱅크 보안 architecture.
  - **Zero Trust의 실제:** BeyondCorp 모델 — 신뢰 경계가 사라진 인프라에서 모든 호출에 인증 강제. perimeter security와의 대비.
  - **API 게이트웨이와 백엔드의 책임 분리:** rate limit·WAF·인증 위임은 gateway, 비즈니스 인가·도메인 룰은 백엔드. 6장 callback.
  - **DB 접근 통제:** IAM 기반 DB auth (AWS IAM DB auth·GCP CloudSQL IAM), audit log, secret 없이 접근하는 패턴. least privilege.
  - **비밀번호·PII 저장:** bcrypt/argon2 (rainbow table 방어), encryption at rest·in transit, 한국 개인정보보호법 맥락 한 단락 (주민번호·신용정보 별도 보호).
  - **OWASP API Security Top 10 백엔드 시각:** broken object level authorization, mass assignment, SSRF — 흔한 코드 함정 3가지.
  - **사고 사례 sidebar (1p):** 2022 카카오 SK C&C 화재 대응 또는 한국 공공기관 secret 유출 사례 — community.md 한국 9 + tribal 케이스. 어떤 control이 막아줬고 어떤 게 무너졌는가.
  - **결제 audit과 연결:** 20장 결제 챕터의 audit chain·blameless postmortem이 이 챕터의 control plane(인증·인가·secret) 위에서 작동한다는 callback.
- **독자가 얻는 것:** 모든 새 endpoint 설계 시 자동으로 묻는 5가지 질문 ("인증? 인가? secret 어디서? rotation? audit log?"). 한국 망분리 환경에서 어떤 architecture가 통과되고 어떤 게 막히는지 mental model.
- **도입부 hook:** "팀 슬랙에 누군가 깃허브 public repo에 `.env`를 푸시했다는 알림이 떴다고 해보자. 그 파일 안에는 AWS access key가 통째로 들어 있다. 5분 안에 누군가 그 키로 EC2를 켜고 비트코인을 채굴한다. 청구서는 다음 날 아침에 도착한다 — 만 달러 단위로. secret을 코드에서 분리하지 않은 한 줄의 게으름이 회사를 흔든다. 보안은 production의 가장 약한 고리이고, 우리가 매일 만지는 영역이다."
- **reference 한계 명시:** §9에 적힌 대로 보안은 본 리서치에서 부분 커버. 챕터 저술 시 OAuth2 RFC·OWASP·전자금융감독규정 1차 자료로 보강 필요.
- **예상 분량:** 16페이지

---

## 2부. 분산 시스템 패턴 — 빌딩 블록을 조립하는 규칙

6개 챕터. 1부의 부품들을 어떻게 엮어 분산 시스템의 정합성·확장성·내구성을 만드는가. 보안은 1부 9장에서 빌딩 블록의 일부로 다뤘으니 여기서는 정합성·확장성·관측성·데이터 통합에 집중한다.

### 10장. 멱등성·재시도·서킷 브레이커 — 실패를 가정한 통신
- **3부 위치:** 2부
- **핵심 질문:** 네트워크 호출은 언제 실패하는가? "실패할 수 있다"는 사실을 코드로 표현하면 어떤 모양이 되는가?
- **주요 내용:**
  - 분산 시스템 8가지 오류 (Sun Microsystems "Fallacies").
  - **Idempotency key** — Stripe Brandur W11. client UUID + server-side request status table + cached response.
  - "Retry는 idempotent 호출에만" — 휴리스틱 5.
  - Exponential backoff + **jitter** — AWS Builders Library W16. retry storm 회피.
  - Circuit breaker 3-state (closed/open/half-open) — Hystrix·resilience4j 패턴.
  - Bulkhead — thread pool 격리, cascading failure 차단 (tribal #12).
  - "Timeout 없는 호출은 없다" — 휴리스틱 4. AWS Builders Library W40.
  - 한국 사례: 토스 결제 SLASH 23 "본인인증 vendor 다중 failover" (W29, 패턴 9).
  - **Callback 예고:** 19장 결제 챕터에서 멱등성이 결제 안전망의 1번 줄이 된다 (보안 9장의 audit chain과 함께).
- **독자가 얻는 것:** 모든 network 호출에 대해 자동으로 묻는 5가지 질문 ("timeout? retry? idempotent? circuit breaker? bulkhead?").
- **도입부 hook:** "결제 시스템에서 '재시도'라는 단어는 위험하다. 한 번 카드 결제가 timeout 났다고 retry를 누르면, 실제로는 결제는 됐는데 응답이 안 돌아온 거였다면 — 그 사용자는 같은 금액을 두 번 낸 것이다. retry를 마음대로 누르려면 idempotency key부터 챙기자."
- **예상 분량:** 22페이지

### 11장. Saga·Transactional Outbox·이벤트 소싱 — 분산 트랜잭션의 현실적 길
- **3부 위치:** 2부
- **핵심 질문:** 2PC를 안 쓴다면, 마이크로서비스 사이의 일관성은 누가 책임지는가?
- **주요 내용:**
  - 왜 2PC를 거의 안 쓰는가 — blocking, SPOF, network partition 취약.
  - **Saga** (W12, P25 Richardson) — choreography vs orchestration. Camunda·Temporal·Step Functions.
  - **Transactional Outbox + CDC** (W13 Debezium) — dual-write 문제 해법. WAL/binlog tail → Kafka.
  - **Event Sourcing / CQRS** (W14) — Fowler "신중하게" 경고. Hugo Rocha "event는 영원히 남는다, schema migration이 가장 어렵다".
  - 보상 트랜잭션 설계, ordering, idempotency 결합.
  - 한국 사례: 토스 코어뱅킹 SAGA + 2PC 혼합 (W29).
  - 흔한 오해: "Saga = 분산 트랜잭션 만능 해법" → 실제로는 "보상 가능한 도메인에서만 작동".
  - **Callback 예고:** 19장 결제 챕터 — 외부 vendor failover + saga.
- **독자가 얻는 것:** 분산 트랜잭션 후보 패턴 4가지(2PC/Saga/Outbox+CDC/Event Sourcing) 의사결정 트리.
- **도입부 hook:** "어떤 결제 시스템에서, 카드 승인은 성공했는데 우리 DB에 기록을 못 남기는 사고가 있다고 해보자. 사용자 입장에서는 돈이 빠져나갔지만, 우리 시스템은 그 사실을 모른다. 이런 상황을 한 번 겪고 나면 'dual-write 문제'라는 단어가 평생 따라다닌다."
- **예상 분량:** 22페이지

### 12장. 합의·복제·일관성 모델 — Raft를 알면 무엇이 보이는가
- **3부 위치:** 2부
- **핵심 질문:** CAP·PACELC·linearizability·causal·eventual — 이 단어들을 우리 도메인 언어로 다시 정의할 수 있는가?
- **주요 내용:**
  - **FLP impossibility** (P30) — 비동기 + 결정적 합의 = 불가능. 실용 알고리즘이 무엇을 양보했는지.
  - **Paxos** (P1, 1989) — 어렵게 유명한 합의.
  - **Raft** (P2, Ongaro 2014) — "이해 가능성"을 first-class goal로. etcd·Consul·TiKV·CockroachDB·KRaft.
  - **ZAB** (P3) — ZooKeeper. Kafka가 2.8+에서 ZK→KRaft로 옮긴 이유.
  - **Replication 유형:** single-leader (Postgres) / multi-leader (CRDT 필요) / leaderless (Dynamo). N/R/W 튜닝.
  - **일관성 계층:** linearizability → sequential → causal (HAT, P12) → read-your-writes → eventual.
  - **CAP → PACELC** (Abadi W17). Abadi의 NewSQL 비판: "Spanner default는 실제로는 not serializable".
  - **CALM theorem** (P6) — coordination-free = monotonic의 동치, CRDT 이론적 근거.
  - 한국 사례: 카카오뱅크 99.99% 금융 가용성 (W41).
- **독자가 얻는 것:** "이 데이터에 우리는 어떤 일관성이 필요한가"를 도메인 단어로 답하는 능력.
- **도입부 hook:** "Spanner의 한 노드가 commit을 마치기 직전, TrueTime이 ε=3ms의 불확실 구간을 보고한다. 노드는 그 3ms를 기다린 뒤에야 commit-wait을 끝낸다. 이 3ms 안에 글로벌 strong consistency가 보장된다 — GPS와 atomic clock이 데이터베이스 안에 들어와 있는 것이다. DDIA를 다 읽었다고 해도, 한 달 뒤 동료가 '우리 결제 시스템은 strong consistency가 필요한가?'라고 물으면 막힌다. 답은 책 안에 있지만, 책의 단어와 우리 회사의 단어가 다르기 때문이다."
- **예상 분량:** 22페이지

### 13장. 샤딩·파티셔닝·Fan-out — 수평으로 늘리는 기술
- **3부 위치:** 2부
- **핵심 질문:** 트래픽 10배가 와도 무너지지 않는 시스템은 무엇을 미리 정해 두었는가?
- **주요 내용:**
  - **샤딩 방식:** range-based (Bigtable·HBase) / hash-based (Dynamo) / directory-based (Vitess VSchema, W10).
  - **Consistent hashing** — vnode 100~200 (W7). Cassandra·Dynamo·Riak.
  - **Hot partition 재방문** — 2장 NoSQL의 hot partition을 sharding 관점으로 다시. Shopify pods by shop_id (W27).
  - **Fan-out (push/pull/hybrid)** — Twitter (W23), Instagram (W24). celebrity = 10K followers 기준.
  - Re-sharding의 잔혹함 — online resharding, dual-write, shadow read.
  - 한국 사례: 당근 동(neighborhood) 단위 partition (W31, 한국 7); 우아한형제들 배민 주문 데이터 샤딩.
  - 광역 분산: cross-region replication latency, consistency 양보.
  - **Callback 예고:** 17장 피드, 18장 매칭에서 fan-out·geo partition으로 재등장.
- **독자가 얻는 것:** Sharding key 5가지 안티패턴 + 분포 검증 방법 + re-shard rollout plan.
- **도입부 hook:** "Sharding key를 잘 골랐다고 자신했던 어떤 팀이, 출시 30분 만에 한 사람의 트래픽이 전체의 95%를 받는 광경을 목격했다. 'celebrity'라는 단어가 단순한 비유가 아니라 진짜 운영 용어가 되는 순간이다."
- **예상 분량:** 22페이지

### 14장. Rate Limiting·백프레셔·SLO·관측성·on-call — 시스템이 자기 자신을 보는 법
- **3부 위치:** 2부
- **핵심 질문:** 우리 시스템은 자기 한계를 알고 있는가? 알고 있다는 것을 어떻게 증명할 수 있는가? 그리고 그 한계를 넘었을 때 사람이 무엇을 해야 하는가?
- **주요 내용:**
  - **Rate limiting 알고리즘:** token bucket (default) / leaky bucket / fixed window / sliding window log / sliding window counter — Cloudflare 0.003% error (W15). 분산 rate limit 구현 — Redis INCR + Lua, hierarchical token bucket.
  - **백프레셔** — Reactive Streams, gRPC flow control, Kafka consumer poll throttling. 큐 길이가 시스템 건강의 1차 신호.
  - **SLI / SLO / Error Budget** — Google SRE Workbook (W35, P23·P24). 100%는 잘못된 목표. error budget이 release 속도와 안정성의 협상 테이블.
  - **Burn rate alerting** — multi-window multi-burn-rate. fast/slow burn으로 page를 줄이고 정확도를 높이는 alerting 설계.
  - **Three pillars of observability:** logs / metrics / traces + **OpenTelemetry** (W37). trace_id correlation, sampling 전략, cardinality 관리.
  - **로그 철학:** "Logs are events, not strings" — Charity Majors 휴리스틱 7. wide-event observability.
  - **p99 latency가 진짜 latency** — Gil Tene 휴리스틱 12. averages lie, percentiles tell the truth. coordinated omission 함정.
  - **배포 전략 (reference §5.6 통합):** blue-green, canary (1% → 10% → 100%), **feature flag** (LaunchDarkly·Unleash·Flagsmith) — release를 deploy와 분리. 결제 챕터 19장의 progressive rollout과 callback.
  - **Chaos engineering (reference §5.5):** Principles of Chaos (W38). game day·fault injection. "장애를 평소에 일부러 일으켜 본 사람만이 진짜 장애를 견딘다."
  - **Blameless postmortem 문화:** Google SRE Book (W36). 사람이 아닌 시스템·프로세스를 비판한다. action item 추적의 정직함이 학습 조직을 만든다.
  - **on-call 휴머니즘:** "alert가 사람을 깨운다면 actionable해야 한다" — 휴리스틱 9. runbook·escalation·pager fatigue 방어. 한 달 page 횟수가 SLO 위반이다.
  - 한국 사례: 토스 SLASH 22 on-call 문화 (alert 절반 자동화), 카카오·우아한형제들의 postmortem 공유 문화 (한국 6).
  - **Callback 예고:** 19장 결제·부록 on-call 휴머니즘에서 재등장. 3부 케이스 16~20장 각각에 "이 시스템의 운영 — SLO·alert·rollback" sidebar로 변주된다.
- **독자가 얻는 것:** 시스템에 자기 한계를 표현하는 5가지 도구 (rate limit·backpressure·SLO·observability·배포·chaos)를 한 layer로 묶는 mental model + on-call alert을 줄이고 postmortem을 blameless하게 쓰는 운영 문화의 핵심 5원칙.
- **도입부 hook:** "어떤 팀의 alert가 새벽 3시에 울렸다. on-call 엔지니어가 컴퓨터를 켜고 보니, 5분 안에 자동 해결된 일이었다. 같은 alert가 그 주에만 11번 울렸다. 한 달 뒤 그 엔지니어는 퇴사했다. on-call burnout은 alert 설계의 실패다 — 사람을 깨우는 모든 page는 그만한 가치가 있어야 한다."
- **예상 분량:** 24페이지

### 15장. 데이터 파이프라인과 협업 동기화 — Lambda·Kappa·Dataflow + CRDT 짧게
- **3부 위치:** 2부
- **핵심 질문:** 배치와 스트림은 정말 다른 일인가, 아니면 같은 일의 두 단면인가? 그리고 multi-writer 협업이라는 또 다른 "데이터의 진실 합치기" 문제는 어떻게 풀리고 있는가?
- **주요 내용:**
  - **Lambda Architecture** — batch + speed + serving 3계층. 코드 중복 비용.
  - **Kappa** (Kreps 2014, 자료 19) — stream 단일 + Kafka replay.
  - **Dataflow** (Akidau 2015, P20) — event-time / watermark / trigger / accumulation 4축. Beam의 추상화.
  - 도구 풍경: MapReduce (P16) → Spark (P17) → Flink (P18) → Beam.
  - 현재 mainstream: Flink·Beam이 통합 — batch = bounded stream.
  - 운영: exactly-once의 진짜 의미, checkpoint, savepoint, watermark의 함정.
  - 한국 사례: 카카오 광고·쿠팡 추천 Kafka 기반 stream 파이프라인 (W33). 쿠팡 검색 indexing pipeline (W32) — 5장 callback.
  - **Sidebar (4p) "CRDT·OT — 협업 도구의 수학적 기반":** Shapiro 2011 (P11), state-based vs op-based CRDT, OR-Set·LWW·Yjs·Automerge. OT (Google Docs). Figma multiplayer, Local-first software (자료 28). "이 데이터는 CRDT가 어울리는가, server-side OT면 충분한가"의 4가지 질문. 데이터 통합이라는 같은 주제 — 분산 파이프라인이 "여러 source의 진실"을 합친다면, CRDT는 "여러 writer의 진실"을 합친다.
- **독자가 얻는 것:** 데이터 파이프라인 의사결정 5가지 (latency target / 정확도 / 재처리 빈도 / 운영 인력 / 비용)에 따른 Lambda/Kappa 선택 기준 + 협업 동기화의 수학적 토대 mental model.
- **도입부 hook:** "어떤 회사가 데이터팀과 백엔드팀을 따로 운영하다가, 한 사건을 계기로 통합했다. 광고 클릭 집계가 batch (1시간 지연)와 stream (실시간) 두 곳에서 달라져 광고주에게 환불을 해줘야 했던 사건이다. 같은 데이터의 두 진실은 종종 두 번째 사고를 낸다."
- **예상 분량:** 20페이지

---

## 3부. 케이스 스터디 — 실제 시스템들

5개 챕터. 각 챕터는 한 도메인의 대표 시스템 2~3개를 비교하며 1부·2부에서 익힌 도구로 해부한다.

### 16장. 채팅 시스템 — Discord·LINE·당근·Slack
- **3부 위치:** 3부 (케이스 스터디)
- **핵심 질문:** 메시지 1조 건이 쌓이는 시스템은 무엇을 양보했고, 무엇을 지켜냈는가?
- **주요 내용:**
  - 도메인 요구 — ordering, durability, history, real-time delivery, fan-out (group chat).
  - WebSocket connection management — LINE connection-manager ↔ message-router gRPC (W30).
  - 메시지 storage trade-off — Cassandra (Discord 초기) vs ScyllaDB (W21) vs DynamoDB (당근, W31).
  - **Discord 마이그레이션 deep dive:** 177노드 Cassandra → 72노드 ScyllaDB. p99 read 40~125ms → 15ms. Rust data services + request coalescing. 인용: "Request coalescing is an important responsibility to avoid multiple database calls when many users request the same message."
  - LINE Messaging Hub — Akka actor + Redis Cluster, LINE LIVE. 실패담: Apache HTTP client 업그레이드로 throughput 1/3 (W30).
  - 당근 채팅 — Go 첫 도입 + DynamoDB + Node.js push 1500 RPS, 거래 위치 라이프사이클 (W31, 한국 7).
  - Slack — workspace sharding + KalDB 자체 (W22).
  - **Callback:** 2장 NoSQL · 3장 캐시 · 4장 큐 · 9장 보안 (인증 token·secret) · 13장 sharding · 14장 관측성.
- **독자가 얻는 것:** 채팅 시스템을 직접 설계할 일은 없어도, 어떤 의사결정 축이 있고 한국 메신저가 무엇을 골랐는지 한 페이지 표.
- **도입부 hook:** "Discord 엔지니어가 어느 날 글을 올렸다. 'We had a single message that was getting requested 30,000 times per second. Our database was suffering.' 메시지 하나가 시스템 전체를 위협한다 — 채팅 시스템이 듣기에는 평범하지만 운영해 보면 가장 잔인한 시스템 중 하나라는 것을 보여주는 단면이다."
- **한국 4 sidebar (2p):** "카카오톡 새해·설날 트래픽" — 평상시 대비 5~30배 spike, group push fan-out의 비용 구조, 카카오 if(kakao) 발표 인용. 17장 fan-out 패턴 callback의 한국 버전.
- **예상 분량:** 24페이지

### 17장. 피드·타임라인·알림 — Twitter·Instagram·카카오톡 fan-out
- **3부 위치:** 3부
- **핵심 질문:** 1억 팔로워의 한 게시물을 모두에게 보여주는 비용을 누가 부담하는가?
- **주요 내용:**
  - Push vs Pull vs Hybrid 재방문 (13장 callback).
  - **Twitter (W23):** Manhattan KV + Redis cluster + celebrity 예외.
  - **Instagram (W24):** Python+Django+PostgreSQL+Cassandra, 사진 S3, fanout Gearman→Kafka.
  - 알림 시스템: APNS·FCM·웹푸시. 한국 카카오톡 group push fan-out 비용 (한국 4).
  - 캐시 적용: timeline cache, fanout cache (3장 callback).
  - **Ranking layer** — engagement score, ML feature store 짧게.
  - 한국 사례: 카카오 if(kakao) 2022 카카오톡 트래픽 피크 (새해·발렌타인), 인스타·페북 광고 점심·퇴근 spike.
- **독자가 얻는 것:** Fan-out 의사결정 표 + celebrity 임계값 결정 방법 + 알림 channel 비용 비교.
- **도입부 hook:** "어떤 가수가 트윗을 올린다. 팔로워 1억 명. 이 한 글을 1억 명의 home timeline에 미리 박아 두려면 1억 번 write가 필요하다. 실시간으로 가능할까? Twitter 엔지니어들은 그래서 celebrity는 pull, 일반 사용자는 push라는 hybrid를 만들었다 — 그렇다면 celebrity의 기준은 누가 정하는가?"
- **예상 분량:** 22페이지

### 18장. 검색·매칭·지오 — 쿠팡·Airbnb·Uber·당근
- **3부 위치:** 3부
- **핵심 질문:** "근처 어디"와 "찾고 싶은 무엇"을 합치는 시스템은 어떻게 만들어지는가?
- **주요 내용:**
  - 검색 deep dive (5장 callback): 쿠팡 검색 — Elasticsearch + Kafka indexing pipeline (W32). 네이버 검색 자체 엔진 (W45). Slack 검색 KalDB (W22).
  - **Airbnb 검색** (W28): IVF ANN over HNSW — 가격·가용성 빈번 변경. SOA standards로 circuit breaker 강제 (10장 callback).
  - **Uber Dispatch** (W26): H3 hexagonal grid + DISCO multi-objective optimizer (wait time, repositioning, ML acceptance).
  - 한국 사례: 당근 동 단위 partition + 거래 위치 기반 (W31, 한국 7); 배민 라이더 dispatch.
  - 위치 인덱스: H3 vs S2 vs Geohash 비교표.
  - 운영: 지역별 alert, shard skew (검색·매칭 둘 다 hot region 발생).
  - **Callback:** 13장 sharding · 14장 관측성.
- **독자가 얻는 것:** 검색·매칭·지오의 공통 구조 = "index + scoring + ranking + dispatch" 한 페이지 다이어그램.
- **도입부 hook:** "당근에 글을 올리면 우리 동네에서만 보이고 옆 동네에서는 안 보인다. 이걸 어떻게 만들었을까? 정답은 사용자가 사는 '동(neighborhood)' 단위 partition이다 — 한국이라는 도메인이 시스템 설계 결정에 미친 영향이 가장 노골적으로 드러나는 사례다."
- **예상 분량:** 22페이지

### 19장. 결제·금융 — Toss·카카오뱅크·Stripe
- **3부 위치:** 3부
- **핵심 질문:** "한 번도 두 번 결제되지 않고, 한 번도 누락되지 않는다"를 분산 환경에서 어떻게 보장하는가?
- **주요 내용:**
  - 도메인 요구: idempotency, audit trail, 99.99% SLO, regulatory compliance.
  - **Stripe** — idempotency key 표준 (W11) — 10장 callback. Two-Phase Idempotency, request_lock·response_cache. 보안의 인증·audit chain은 9장 callback.
  - **Toss 결제 시스템 현대화** (W29) — legacy 정리, vendor wrapper, multi-PG failover, 1% progressive rollout.
  - **Toss 코어뱅킹** (W29, SLASH 23) — hybrid cloud (Public+Private) MSA, "이자 받기" 가능. SAGA+2PC 혼합.
  - **카카오뱅크 99.99%** (W41) — 메인프레임 → MSA, 24/7, audit, blameless postmortem.
  - 한국 결제 특수: PG (NHN KCP·NICE·KCB·다날) wrapper layer, 통신 3사 본인인증 failover (한국 8).
  - 0시 동시 트래픽 — 이자·청약·콘서트 (한국 1) — 1·3장 callback.
  - 운영: 결제 SLO, error budget, postmortem (블레임리스), audit chain.
  - **클라이맥스 챕터** (책 전체의).
- **독자가 얻는 것:** 결제 시스템을 직접 만들지 않더라도, "외부 vendor failure를 가정하지 않은 코드는 production이 아니다"의 mental model.
- **도입부 hook:** "한국에서 0시 정각에 이자 받기 버튼을 누른다고 해보자. 같은 순간에 수십만 명이 같은 행동을 한다. 이 트래픽이 결제 시스템뿐 아니라 통신 3사 본인인증 API에까지 도착하면, 그 API는 10초 안에 죽는다. 그래도 우리 시스템은 살아남아야 한다. 결제는 시스템 디자인의 모든 어려움이 한 자리에 모이는 영역이다."
- **예상 분량:** 26페이지

### 20장. 이커머스·재고·정합성 — Shopify·쿠팡·Amazon
- **3부 위치:** 3부
- **핵심 질문:** 재고 1개의 마지막 한 명을 누구에게 줄 것인가? 그리고 그 결정을 자정 cutoff 안에 끝낼 수 있는가?
- **주요 내용:**
  - **Shopify Pods** (W27) — Ruby majestic monolith + Packwerk module boundary + MySQL podding by shop_id. 모듈러 모놀리스 사례 (논쟁 A callback).
  - BFCM (Black Friday Cyber Monday) 대비 — Shopify의 load shedding, queue based throttling.
  - **쿠팡 로켓배송** (한국 5, W32) — 자정 cutoff: 그 시점까지 재고·배차·창고 결정이 일관돼야 함. 정합성 vs 속도의 극단적 trade-off.
  - 재고 일관성: in-memory reservation, distributed lock, eventual reconciliation.
  - 카트·체크아웃의 idempotency (10장 callback).
  - Amazon 사례 짧게 (Dynamo 원전 도메인).
  - 한국 사례: 우아한형제들 배민 주문 처리 (한국 6).
  - **Callback:** 10장 멱등성, 11장 saga, 13장 sharding, 12장 일관성.
- **독자가 얻는 것:** 재고·주문·결제 일관성 패턴 (reserve → confirm → settle) 3단계 다이어그램.
- **도입부 hook:** "쿠팡 로켓배송의 자정 cutoff는 절대 어길 수 없다. 자정 1초 전에 들어온 주문은 오늘 새벽에 출발하는 트럭에 실려야 한다. 그 1초 사이에 재고 확인·결제 승인·배차 결정·창고 배정이 모두 정확하게 일관되어야 한다 — 속도와 정합성을 동시에 잡는 사례는 한국에 가장 많다."
- **예상 분량:** 20페이지

---

## 부록 A. 현장 노트 — 책에 안 나오는 일들
- **3부 위치:** 부록
- **핵심 질문:** 책에서는 안 가르치는데 production에는 늘 있는 18가지 함정은 무엇인가?
- **주요 내용:**
  - Tribal knowledge 18선 — community.md §5 그대로:
    - NTP slew vs step, fd ulimit, TIME_WAIT 누적, DNS TTL, Kafka rebalance storm, JVM safepoint, Bloom filter false positive, Postgres VACUUM 실패, TLS handshake, DST cron, NAT Gateway inter-AZ, DB pool exhaustion, Redis MGET vs pipeline, gRPC deadline propagation, K8s liveness self-restart, Cassandra tombstone, ES refresh_interval, HikariCP leakDetectionThreshold.
  - 각 항목 1~2페이지: 증상 / 원인 / 즉시 mitigation / 근본 fix.
  - **한국 환경 야사:** 0시 트래픽 회식 자리 농담, 카카오 SK C&C 화재 회고 (한국 9), 우아한형제들 배민의 새벽 0시 운영 패턴.
  - **on-call 휴머니즘:** "alert가 사람을 깨운다면 actionable해야 한다" (휴리스틱 9, 패턴 8). pager fatigue에 대한 시각.
  - **이력서용 기술 도입의 함정** (한국 10) — "이력서에 Kafka 쓰려고 도입했다, 실제로는 RabbitMQ면 충분했다." 의사결정 메타. (0장에서 짧게 한 번 다뤘으니 여기서는 사례 2개로 살을 붙임.)
  - **배포·마이그레이션 실패담 2개 (사용자 결정 추가):** (1) 한국 모 핀테크의 blue-green 잘못 끊어 결제 30분 정지 사례 — 14장 본문의 progressive rollout 일반론을 야사로 회수. (2) Slack 2021 outage 또는 GitHub 2020 outage Postmortem 변주 — 마이그레이션 도중 트래픽 routing 잘못, 24h 영향. 운영의 가장 비싼 학습은 항상 사고에서 온다.
  - **AI/LLM 한 페이지 — "다음 책의 약속":** vector DB·RAG·LLM serving·embedding service가 1·2부 도구의 응용임을 한 페이지로 정리하되 본격 다루지 않는다. 2026년 이후 빠르게 변할 영역이라 별권의 주제로 남긴다. ("이 책의 모든 빌딩 블록·패턴이 LLM 시대에도 살아 있다. 도구가 더 늘었을 뿐이다.")
  - 책의 한계 — 모바일 백엔드 특수성, 게임 서버 특수성은 별도 책의 주제. (보안은 9장에서 정식 다룸 — "다음 책의 약속" 항목에서 제외.)
- **독자가 얻는 것:** "production에서 만나본 적 있다"는 18개의 함정 카드. 책장에 펴두고 장애 회의에서 꺼내 보는 reference.
- **도입부 hook:** "어떤 베테랑 SRE는 후배에게 이렇게 말한다. '이 18가지를 한 번씩 만나보면, 너도 5년차다.' 책으로는 안 배우는, 코드로만 만나는 함정들이 있다 — 우리는 그것들을 끝으로 모아 둔다."
- **예상 분량:** 15페이지 (tribal 18선 ~11p + 한국 야사·on-call·이력서 함정 ~2p + 배포 실패담 2개 ~1p + AI/LLM 한 페이지 1p)

---

## 분량 합계

| 부 | 챕터 | 페이지 합 |
|-----|-------|----------|
| 서장 | 0 | 13 |
| 1부 빌딩 블록 | 1~9 (9 챕터, 9장 분산 시스템 보안 신설) | 188 |
| 2부 패턴 | 10~15 (6 챕터, 14장 운영 통합 24p 확장 / 15장 파이프라인 + CRDT 흡수) | 132 |
| 3부 케이스 스터디 | 16~20 (5 챕터) | 114 |
| 부록 | A (tribal knowledge 18선 + 한국 환경 야사 + on-call 휴머니즘 + 이력서용 함정 + AI/LLM 한 페이지 "다음 책의 약속") | 15 |
| **총** | **21 챕터 + 부록 (0장 + 1~20장 + 부록 A)** | **462페이지** |

목표 ~450~480 사이에 안착 (462p). team-lead 제약(420~480, 챕터 18~22) 모두 충족. 챕터 저술 시 ±5% 여유 가능.

### 1·2·3부 분포
- 서장: 1장 / 13p (3%)
- 1부 빌딩 블록: 9 챕터 / 188p (41%) — 보안 9장 16p 포함
- 2부 패턴: 6 챕터 / 132p (29%) — 14장 운영 통합 24p, 15장 파이프라인+CRDT 20p 포함
- 3부 케이스: 5 챕터 / 114p (25%)
- 부록: 1개 / 15p (3%)

빌딩 블록(41%)·패턴(29%)에 무게, 케이스(25%)에서 회수, 부록(3%)으로 마무리. 책의 정체성은 1·2부의 fundamental 깊이와 3부 클라이맥스(19장 결제)에서 모든 부품·패턴이 동시에 등장하는 회수에 있다. **보안을 9장(분산 시스템 보안)에 빌딩 블록의 일부로 본문 편입한 점** 이 *Acing*·DDIA·Alex Xu와의 강한 차별화 — reference §9의 "리서치 한계"는 챕터 저술 시 1차 자료(OAuth2 RFC·OWASP·전자금융감독규정) 보강으로 메우고, "다음 책의 주제"로 미루지 않는다. AI/LLM은 사용자 결정에 따라 부록 한 페이지 "다음 책의 약속"으로 유지 — 본 책의 정체성(분산 시스템 fundamental)에서 한 발 떨어진 주제이며 2026년 이후 빠르게 변할 영역이라 본문 챕터로는 시기상조다. 별권에서 다룰 주제로 남긴다.

운영(D축)은 14장(rate limit·SLO·관측성·on-call·배포·chaos 통합, 24p)·9장(보안 control plane)·19장(결제 SLO·audit)·3부 케이스 운영 sidebar 5개·부록(tribal) 5축으로 다층화. 운영 본문 비중은 14장 24p + 9장 일부(audit·secret rotation 운영 시각) + 3부 sidebar 5 × 2~3p = 약 40p로 책의 차별화 슬로건과 정합.

---

## 4. 내러티브 아크

### 4.1 mental model의 발전
1부에서 독자는 **"부품의 trade-off를 도메인 언어로 말하는 법"**을 익힌다 — 캐시·DB·큐를 "쓸 줄 안다"에서 "이 선택의 대가는 무엇인가"로 한 단계 올라간다. 8장에서 시간·순서를 만나며 이미 "분산"의 어둠을 슬쩍 느끼고, **1부 끝(9장)에서 분산 시스템 보안(인증·인가·secret·망분리)을 빌딩 블록의 control plane으로 박아 둔다** — 모든 빌딩 블록이 그 위에서 작동한다는 것을, 책의 본론으로 들어가기 전에 분명히 한다.

2부에서는 **"부품들을 안전하게 잇는 규칙"**으로 시야가 넓어진다. 10장(멱등성·재시도)에서 "실패는 정상"이라는 인식이 박힌 다음, 11장(Saga)·12장(합의)·13장(샤딩)으로 분산 시스템의 4대 난제(일관성·내구성·확장성·정합성)를 차례로 만난다. 14장(rate limit·SLO·관측성·on-call·배포·chaos 통합)에서 "시스템이 자기 자신을 보는 법"으로 운영 언어가 완성된다. 15장에서 데이터 파이프라인을 통해 "여러 source의 진실 합치기"와 협업 동기화(CRDT sidebar)의 "여러 writer의 진실 합치기"를 한 챕터로 연결하며 2부를 닫는다.

3부에서는 **"우리가 익힌 도구가 실제 어디서 어떻게 쓰이는가"**의 통합. 채팅(16) → 피드(17) → 검색·매칭(18) → 결제(19) → 이커머스(20)로 가면서, 1·2부의 모든 챕터가 callback으로 재등장한다. 각 케이스 챕터에는 "이 시스템의 운영 — SLO·alert·rollback" sidebar와 "유사 시스템 1단락"(Spanner·Figma·Netflix 등) sidebar가 의무 삽입되어 다채로움과 운영 본문 비중을 함께 챙긴다. 마지막에 다다르면 독자는 임의의 시스템을 봤을 때 "이건 1부 ○장, 2부 △장, 3부 □장과 비슷하군"이라는 자동 mapping이 생긴다.

부록(현장 노트)은 그 위에 "production은 결국 사람의 영역"이라는 동료적 마무리. tribal knowledge 18선·한국 환경 야사·on-call 휴머니즘·이력서용 기술 도입의 함정·AI/LLM 한 페이지("다음 책의 약속")가 책의 마지막 인상이다.

### 4.2 챕터 간 Callback 지점 (9개)
1. **3장 캐시 → 17장 fanout cache**: 캐시를 단순 KV에서 fanout 위해 미리 박아두는 자료 구조로 재정의.
2. **2장 NoSQL hot partition → 13장 샤딩의 hot partition → 16장 Discord 마이그레이션**: 같은 현상이 부품 → 패턴 → 실제 시스템 3개 layer로 반복.
3. **8장 분산 ID → 19장 결제 idempotency key**: ID의 timestamp prefix가 결제 멱등성의 안전망에 어떻게 쓰이는지.
4. **9장 보안 → 19장 결제 audit chain → 부록 사고 사례**: 인증·인가·secret·망분리의 control plane이 결제 audit과 한국 환경 운영 사고 사례에서 어떻게 재등장하는지. 보안이 빌딩 블록 → 케이스 → 야사의 3개 layer로 반복.
5. **6장 service mesh mTLS → 9장 분산 시스템 보안**: 서비스 메시의 mTLS 자동화가 보안 챕터의 service-to-service identity로 정식화.
6. **10장 멱등성 → 19장 결제 → 20장 이커머스 reserve→confirm**: 멱등성이 단순 패턴이 아니라 결제·재고의 1번 줄이 됨.
7. **11장 Saga → 19장 토스 코어뱅킹 SAGA+2PC 혼합**: 패턴이 실제 한국 금융에 어떻게 적용되는지.
8. **12장 합의·일관성 → 19장 결제 SLO**: 99.99%라는 숫자가 PACELC 어느 쪽을 양보한 결과인지. **13장 fan-out → 17장 Twitter/Instagram hybrid**도 함께 회수.
9. **14장 SLO·관측성·on-call·배포·chaos → 17·18·19·20장 운영 sidebar → 부록 on-call 휴머니즘**: 모니터링·alert가 결국 사람과 만나는 지점. 14장의 운영 5도구가 3부 케이스 5개 챕터에 sidebar로 변주된다.

### 4.3 책의 클라이맥스 — **19장 결제·금융**
**19장 결제·금융**이 책의 클라이맥스다. 이유: (1) 1부의 9개 부품(RDB·NoSQL·캐시·큐·검색·LB·CDN·시간·**보안**), 2부의 6개 패턴(멱등성·saga·합의·sharding·rate limit·SLO·관측성·파이프라인+CRDT)이 모두 결제 시스템에서 동시에 등장한다. (2) 한국 백엔드의 정체성이 가장 두드러지는 도메인 — 토스·카카오뱅크·통신 3사 본인인증·0시 트래픽·전자금융감독규정 망분리(9장 callback)가 모두 모인다. (3) "한 번도 두 번 결제되지 않고, 한 번도 누락되지 않는다"는 명제가 책 전체의 약속(§5)을 한 도메인에서 가장 강하게 검증한다. (4) 19장을 다 읽은 후 독자는 "이 책의 모든 챕터가 어떻게 한 시스템에 모이는지"를 한눈에 본다 — 그 자체가 책 전체의 회수 장면이다.

20장 이커머스·재고가 클라이맥스 뒤의 차분한 회수다 — 결제만큼 극단적이지는 않으나 1·2부 모든 빌딩 블록이 다시 한 번 다른 조합으로 등장한다. 그리고 부록의 "현장 노트"가 책 전체의 동료적 마무리 — production은 결국 사람의 영역이라는 인상으로 닫는다.

---

## 5. 책의 약속 (Promise)

0장에서 제시하고 마지막에 회수할 6가지:

1. **이 책을 다 읽으면, 임의의 분산 시스템 장애 회의에서 "어디서부터 의심해야 하는가"를 첫 5분 안에 추론할 수 있게 된다.**
2. **이 책을 다 읽으면, 캐시·큐·DB를 도입할 때 묻는 trade-off 질문 체크리스트가 머릿속에 자동으로 펼쳐진다 — 6개 부품 × 5개 질문 = 30개 질문이 도구처럼 손에 잡힌다.**
3. **이 책을 다 읽으면, 멱등성·재시도·서킷 브레이커·timeout을 따로 떠올리지 않고 모든 network 호출에 함께 떠올리게 된다 — "실패는 정상"이라는 인지가 코드 작성 습관으로 박힌다.**
4. **이 책을 다 읽으면, *Acing*·DDIA·Alex Xu의 예시들이 한국 백엔드의 어떤 사례와 매핑되는지 머릿속에 한국어 자막이 생긴다 — 토스·카카오뱅크·당근·쿠팡의 결정이 외국 사례와 어떻게 닮고 어떻게 다른지가 보인다.**
5. **이 책을 다 읽으면, on-call alert가 울릴 때 "이 alert가 정말 사람을 깨워야 하는가"를 묻는 메타적 시선이 생긴다 — 알람을 줄이고, runbook을 만들고, postmortem을 blameless하게 쓰는 사람이 된다.**
6. **이 책을 다 읽으면, 새 endpoint를 설계할 때 자동으로 "인증·인가·secret·rotation·audit log" 5가지를 묻게 된다 — 보안이 별도 영역이 아니라 모든 빌딩 블록 위에 깔린 control plane임을 코드 작성 습관으로 박는다. 한국 망분리·전자금융감독규정 환경에서 무엇이 통과되고 무엇이 막히는지의 mental model이 생긴다.**

각 약속은 9장(보안)·14장(운영)·19장(클라이맥스 결제)·20장(마지막 케이스 이커머스)에서 차례로 회수한다. "1부 ○장에서 던진 약속은 19장에서 이렇게 회수되고, 20장에서 한 번 더 다른 도메인에 적용된다" 식으로 epilogue 형태의 짧은 정리. 20장 마지막 한 페이지가 책 전체 약속의 최종 회수 페이지가 되고, 부록은 "production은 사람의 영역"이라는 동료적 마무리로 닫는다.

---

## 6. 챕터별 reference 인용 매트릭스 (저술 시 빠른 lookup)

| 챕터 | 빌딩블록 (§2) | 패턴 (§3) | 케이스 (§4) | 운영 (§5) | 한국 (§6) | 논문 (§8.1) |
|-----|----|----|----|----|----|----|
| 0 | §1 4축 지형도 | - | - | - | - | - |
| 1 RDB | §2.3, §2.10 | - | - | 휴리스틱 2/3/6 | 한국 1 | P14, P21, P22 |
| 2 NoSQL | §2.4, §2.10 | - | §4.1 Discord, §4.11 당근 | 패턴 2 | 한국 7 | P7, P8, P9, P13 |
| 3 캐시 | §2.1 | §3.8 | - | 패턴 4, 휴리스틱 4 | 한국 4 | - |
| 4 큐 | §2.2 | §3.10 | §4.10 LINE | 패턴 6, tribal 5 | 한국 4 | P19 |
| 5 검색 | §2.5 | - | §4.2 Slack, §4.8 Airbnb | 휴리스틱 1, tribal 17 | 한국 3 | - |
| 6 LB·메시 | §2.6 | - | - | 논쟁 G | - | - |
| 7 CDN | §2.7, §2.8 | - | §4.5 Netflix | - | - | - |
| 8 시간 | §2.9 | §3.9 | - | 패턴 3, tribal 1 | - | P4, P5 |
| **9 보안 (신설)** | §2.6 (mesh mTLS) | - | §4.9 Toss·카뱅 (audit) | §5.4, §9 (한계) | 한국 2 (망분리), 한국 8, 한국 9 | OAuth2 RFC·OWASP·전금감규 (외부) |
| 10 멱등성 | - | §3.3, §3.8 | §4.9 Toss | 휴리스틱 4/5 | 한국 8 | - |
| 11 Saga | - | §3.4, §3.5, §3.6 | §4.9 Toss | 패턴 10 | 한국 1 | P25 |
| 12 합의 | §2.8 | §3.1, §3.2, §3.12 | §4.12 Spanner | - | 한국 (카뱅) | P1, P2, P3, P5, P6, P12, P30, P31 |
| 13 샤딩 | - | §3.11, §3.13 | §4.7 Shopify, §4.11 당근 | 패턴 2 | 한국 7 | - |
| 14 rate limit·SLO·관측성·on-call·배포·chaos | - | §3.7 | - | §5.1~5.3, §5.5, §5.6, 휴리스틱 7/9/12 | 한국 (토스·우아한 postmortem) | P23, P24 |
| 15 파이프라인 + CRDT | - | §3.10, §3.14 | §4.10 카카오 광고, §4.11 Figma | - | - | P11, P16, P17, P18, P20, 자료 28 |
| 16 채팅 | - | §3.13 | §4.1, §4.2, §4.10, §4.11 | - | 한국 4, 7 | - |
| 17 피드 | - | §3.13 | §4.3 Twitter, §4.4 Instagram | - | 한국 4 | - |
| 18 검색·매칭 | - | §3.15 | §4.6 Uber, §4.8 Airbnb, §4.11 당근 | - | 한국 3, 7 | - |
| 19 결제 | - | §3.3, §3.4 | §4.9 Toss, §4.10 카카오뱅크 | §5.1, §5.4 | 한국 1, 2, 8, 9 | - |
| 20 이커머스 | - | §3.3, §3.11 | §4.7 Shopify, §4.11 쿠팡 | - | 한국 5, 6 | - |
| 부록 | - | - | - | §5.3, tribal 1~18 | 한국 9, 10 | - |

이 표는 chapter-writer가 한 챕터를 쓸 때 "내가 인용할 reference 묶음"을 한 번에 꺼낼 수 있도록 만든 lookup.

---

## 7. 챕터 저술가에게 보내는 메모

- **공통 톤:** Toby 스타일 가이드 — 평어체, "-자/-보자" 청유형, "왜 그럴까?" 수사적 질문, "~라고 해보자" 상황 가정, "난감하다·찜찜하다·번거롭다·끔찍한 일이다" 감정 단어, "기억해두자/잊지 말자/주의해야 한다" 강조.
- **도입부 hook은 반드시 community.md·web.md 실제 사례 기반.** 추상적인 도입 금지.
- **각 챕터 끝에 "이번 장의 약속 회수" 짧은 정리 + "다음 장으로 가는 다리" 한 문단.**
- **인용은 P#/W#/C# 식으로 출처 표기 일관 유지** (§01_reference 표기 규약).
- **권위 등급 ★★★/★★/★ 자료 우선순위 지키기**, 검증 필요 자료는 paraphrase + cross-check.
- **분량 ±10% 허용**. 너무 길면 잘라내기보다는 "Deep Dive" sidebar로 분리.
- **[3부 케이스 운영 sidebar 의무화]** 16~20장 각 챕터에 **"이 시스템의 운영 — SLO·alert·rollback"** sidebar(2~3p)를 반드시 포함. 라운드 1·2 리뷰 [C2] 옵션 B + 사용자 결정 사항. 14장(rate limit·SLO·관측성·on-call·배포·chaos 통합 24p)이 일반론을 다뤘다면, 케이스 sidebar는 도메인별 운영 디테일(예: 채팅의 connection re-balance, 피드의 celebrity alert, 검색·매칭의 region별 shard skew alert, 결제의 1% progressive rollout·error budget burn rate, 이커머스의 BFCM load shedding·queue throttling)을 담는다. 4축 D(운영)의 본문 비중을 5개 챕터 × 2~3p = 10~15p로 확보.
- **[3부 유사 시스템 sidebar 의무화]** 16~20장 각 챕터에 **"다른 유사 시스템 1단락"** sidebar를 반드시 포함. 사용자 결정 — [C1] 케이스 챕터 신설 거절을 보강하는 장치. 본문이 다루지 못한 대표 시스템 1개를 1단락으로 압축 (예: 16장 채팅에 WhatsApp Erlang VM, 17장 피드에 TikTok recommendation pipeline, 18장 검색·매칭에 Airbnb의 Categories ML, 19장 결제에 Stripe Sigma·**Spanner의 글로벌 분산 결제 인프라 사례 (reference §4.12)**, 20장 이커머스에 **Figma multiplayer 협업 sidebar (reference §4.11)·Netflix Open Connect (reference §4.5)**). 3부 다채로움 보강 + 라운드 1 reviewer가 우려한 "다른 도메인 부족"의 챕터 신설 없는 해소책.
- **[추가 리서치 권장 챕터]** 9장 보안은 reference §9의 "리서치 한계" 영역 — 챕터 저술 전 1차 자료 보강 필요 (OAuth2 RFC·OWASP·전자금융감독규정·SPIFFE/SPIRE 1차 자료). 14장 운영의 chaos engineering·blameless postmortem도 §5.5·W36 외 1차 자료 보강 권장. 챕터 저술가가 추가 리서치를 요청하면 reference 보강 phase 재실행.
- **[부록 보강]** 부록 A의 "tribal knowledge 18선"에 **배포·마이그레이션 실패담 2개 추가** (예: 한국 모 핀테크의 blue-green 잘못 끊어 결제 30분 정지, 또는 Slack의 2021 outage Postmortem). 14장 본문의 배포 일반론을 부록 야사로 회수.

저술 완료 시 본 plan과 어디서 어떻게 다르게 갔는지 짧은 메모를 챕터 끝 frontmatter에 남길 것.
