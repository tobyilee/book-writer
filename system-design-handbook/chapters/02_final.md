# 2장. NoSQL — Dynamo 계열과 Bigtable 계열을 가르기

AWS Summit Korea의 어느 발표에서, 한 엔지니어가 이런 말을 했다고 해보자. "DynamoDB 마이그레이션 중에 부하 테스트는 모두 통과했다. 그런데 출시 30분 만에 한 partition이 전체 트래픽의 95%를 받기 시작했다. 우리 서비스에 celebrity 사용자가 있었다는 사실은 그날 밤 12시에 알게 됐다."

이 한 토막에 NoSQL이라는 영역의 모든 어려움이 농축돼 있다. 어제까지 RDB가 자기 일을 잘하고 있었는데, "확장이 안 된다"는 이유로 NoSQL을 도입하면 그날부터 새로운 종류의 고통이 시작된다. 그 고통의 이름은 대부분의 경우 **hot partition**이다. 그리고 이 단어가 무서운 진짜 이유는, 부하 테스트로는 잘 안 잡힌다는 데 있다. 우리는 보통 uniform random key로 부하를 흘리는데, 실제 사용자는 절대 uniform하지 않다.

NoSQL이 "schema-less라 편하다"는 이유로 도입된 적이 있다면, 이미 우리 회사 어딘가에는 hot partition 폭탄이 깔려 있을 가능성이 적지 않다. 1장에서 RDB를 다뤘으니, 이제 RDB의 결을 따라가지 않는 시스템들 — Dynamo 계열과 Bigtable 계열의 두 큰 갈래 — 을 함께 짚어 보자. 이 둘을 가르고 나면 NoSQL이라는 막연한 단어가 훨씬 또렷한 두 모양으로 보이기 시작한다.

## 1. NoSQL이라는 단어가 진짜로 양보한 것

먼저 솔직하게 짚자. "NoSQL"이라는 단어 자체는 마케팅 용어에 가깝다. SQL이 없다는 것보다, 무엇을 양보하고 무엇을 얻었는지가 본질이다. NoSQL이라는 우산 아래 들어가는 시스템들의 공통 양보 항목은 대체로 다음과 같다.

- **schema의 강제력**을 양보했다. 컬럼 추가가 쉬워지지만, 그 대신 application이 schema를 책임진다.
- **다중 row JOIN과 복잡 트랜잭션**을 양보했다. 단일 row의 빠른 read·write를 얻는 대신.
- **strong consistency를 (대부분) 양보**했다. Dynamo 계열은 양보하고, Bigtable 계열은 부분만 양보한다 — 이게 두 갈래의 본질적 차이다.

그 대신 무엇을 얻었는가? horizontal scale, write throughput, write-heavy workload, 그리고 "schema migration이 비교적 덜 아픈" 구조. 이게 NoSQL의 표면 가치다.

여기서 자주 오해되는 단어가 하나 있다 — "schema-less"다. 정확한 표현은 **"schema-on-read"(읽을 때 비로소 schema가 적용된다)** 또는 **"query-first schema"**다. 데이터 모델링을 안 해도 된다는 뜻이 아니라, 어떤 query를 자주 던질 것인지를 먼저 결정하고 그 query에 맞게 데이터 모양을 박는다는 뜻이다. RDB는 데이터를 정규화해 두고 query 시점에 join으로 합치지만, NoSQL은 query 모양대로 데이터를 미리 비정규화해서 박는다. 이 인지가 없으면 NoSQL을 도입한 뒤 "왜 우리 쿼리가 다 secondary index가 필요하지?"라며 찜찜해진다 — 처음부터 query-first로 설계하지 않은 결과다.

기억해 두자. **NoSQL은 schema-less가 아니라 query-first다**. 이 한 줄이 이 챕터를 관통하는 한 줄의 지도다.

## 2. Dynamo 계열 — leaderless·eventual·vector clock의 세계

2007년, Amazon이 SOSP 학회에 발표한 한 편의 논문이 NoSQL의 한 갈래를 결정지었다. Werner Vogels와 동료들이 쓴 *Dynamo: Amazon's Highly Available Key-value Store*다. 이 논문이 던진 질문은 이거였다 — **장바구니가 절대 사라지지 않도록 만들려면, 일관성을 어디까지 양보해야 하는가?**

Amazon의 답은 분명했다. 장바구니에 물건을 담을 때 잠시 두 버전이 동시에 존재하더라도, "장바구니에 물건이 들어갔다는 사실 자체는 반드시 살아남아야" 한다는 것이다. 즉 **availability와 partition tolerance를 우선하고, consistency를 application 레벨에서 합친다**. CAP 정리의 단어로 말하면 AP를 골랐다는 뜻이다.

### Dynamo 계열의 네 가지 핵심 결정

1. **Leaderless replication.** master가 없다. 모든 노드가 read·write를 받는다. 이건 SPOF를 없애고 write availability를 끌어올리는 결정이다. 대신 conflict가 생긴다.
2. **Consistent hashing + virtual node.** 키를 ring 위에 매핑하고, vnode 100~200개로 나누어 노드 추가·제거 시 데이터 이동을 최소화한다. 이건 13장 샤딩에서 더 자세히 다룬다.
3. **N/R/W tunable quorum.** 데이터를 N개 노드에 복제하고, read에 R개·write에 W개의 응답을 기다린다. R + W > N이면 strong-ish consistency를 얻고, 그렇지 않으면 더 빠른 응답을 얻는다. trade-off는 application이 정한다.
4. **Vector clock으로 conflict 해소.** 두 노드가 동시에 같은 key에 write를 하면 vector clock이 두 버전을 모두 들고 다닌다. 그리고 application이 "어떤 버전을 살릴 것인가"를 결정한다. 장바구니라면 union, 카운터라면 max — 도메인 의미가 conflict 해소에 들어온다.

이 네 가지 결정이 합쳐져, **Dynamo 계열은 "느슨한 합의로 always-writable(언제나 쓸 수 있다)"**라는 한 줄로 요약된다. 그 후예가 오늘날의 DynamoDB (Amazon이 만든 managed 서비스), Cassandra (Facebook이 SIGOPS 2010에 발표한 P9), ScyllaDB (Cassandra wire-compatible 재구현), Riak (지금은 명맥이 약해진 OSS Dynamo) 등이다.

여기서 흥미로운 사실 — **DynamoDB와 Dynamo 논문은 다른 시스템**이다. 논문의 Dynamo는 내부 시스템이었고, 오늘의 DynamoDB는 그 영감을 받았지만 single-leader per partition + Paxos 기반 metadata로 구현됐다. 그래서 DynamoDB는 strong consistency 옵션도 제공한다. "Dynamo 계열"이라는 분류는 마케팅이 아니라 설계 철학을 가리키는 단어로 받아들이는 편이 낫다.

## 3. Bigtable 계열 — single-leader·tablet·strong consistency

같은 시기, 다른 회사의 답은 달랐다. 2006년 OSDI 학회에 Google이 발표한 *Bigtable: A Distributed Storage System for Structured Data* (P8)는 또 다른 갈래를 만들었다. Bigtable이 풀려고 한 문제는 Dynamo와 정반대였다 — **거대한 sparse 테이블을 strong consistency로 잘게 쪼개서, 빠른 range scan을 가능하게 하자**.

### Bigtable 계열의 네 가지 핵심 결정

1. **Tablet 단위 single-leader.** 전체 테이블을 row key 범위로 쪼개 tablet으로 만들고, 각 tablet마다 leader가 한 명 있다. 그 leader가 해당 tablet의 read·write를 모두 책임진다. partition 단위의 strong consistency.
2. **Chubby (지금은 Spanner의 일부)에 의존한 metadata.** tablet location, leader election을 외부 coordination service에 맡긴다. 이게 운영 부담의 진짜 원천이다 — 8장의 분산 조정 서비스 영역과 닿는다.
3. **Range-based partitioning.** Dynamo 계열의 hash 기반과 달리, row key의 사전 순서대로 partition을 만든다. range scan이 빨라지지만, key가 timestamp나 sequential ID이면 latest partition으로 모든 write가 몰린다. 또 다른 hot partition이다.
4. **Column family + sparse storage.** 한 row가 수백만 컬럼을 가질 수 있고, 컬럼 family 단위로 LSM-tree 파일이 갈린다.

Bigtable 계열의 후예는 HBase (Apache, Hadoop 생태계), Google Cloud Bigtable (managed), 그리고 Spanner (TrueTime이 추가된 외부 일관성 글로벌 DB — 12장에서 다룬다). 분류 측면에서는 HBase가 가장 직설적인 Bigtable 후계자다.

## 4. 두 갈래 비교 — 표 하나로 보는 trade-off

말로 풀어 쓴 차이를 한 페이지의 표로 압축해 보자. 이 표는 회의 자리에서 "우리 워크로드는 어느 계열에 어울리는가"를 결정할 때 손에 잡히는 도구가 된다.

| 축 | Dynamo 계열 (Cassandra·DynamoDB·Scylla) | Bigtable 계열 (HBase·Bigtable) |
|---|---|---|
| 복제 모델 | Leaderless quorum (N/R/W) | Tablet-level single-leader |
| 기본 consistency | Eventual (tunable) | Strong (per tablet) |
| Partition 방식 | Hash-based (consistent hashing) | Range-based |
| 핵심 의존성 | gossip protocol | external coordination (ZooKeeper·Chubby) |
| Hot partition 원인 | celebrity key | sequential key |
| Conflict 해소 | vector clock·LWW | leader가 단일 truth |
| Write 친화도 | 매우 높음 | 매우 높음 |
| Range scan | 약함 | 강함 |
| 대표 사례 | Discord·당근·Netflix·Apple iCloud | Spanner·Bigtable·HBase·LINE 일부 |

표는 깔끔하지만, 정작 production에서는 어느 줄 하나가 우리를 새벽에 깨운다. 그게 다음 절의 주제다.

## 5. Hot Partition — 평생의 적

NoSQL을 1년 이상 운영한 팀은 거의 예외 없이 hot partition에 한 번씩 데인다. HN의 한 토론에서 어떤 엔지니어가 적었다고 한다. "We had a celebrity in our user table. 1 partition was 95% of our reads." 그리고 또 다른 사용자는 "Adaptive capacity kicks in after 5-15 min, but we lost 4 hours before figuring out our key was wrong"이라고 적었다. 이 두 줄에 hot partition 디버깅의 잔인함이 다 있다.

왜 hot partition은 막기 어려울까? 이유는 다섯 가지가 겹쳐 있다.

1. **부하 테스트가 uniform random key로 돌아간다.** 실제 사용자는 절대 uniform하지 않다. 한 명의 celebrity, 한 개의 viral content, 한 곳의 이벤트가 분포를 완전히 비튼다.
2. **Alert가 "전체 QPS"만 보고 있다.** shard별 QPS skew는 잡지 않는 경우가 흔하다.
3. **Adaptive capacity가 즉시 발동하지 않는다.** DynamoDB는 5~15분이 지나서야 hot key의 capacity를 다시 분배한다. 그 사이의 5분이 사용자에게는 영원이다.
4. **NoSQL의 partition key는 한 번 정하면 바꾸기 매우 어렵다.** RDB의 인덱스처럼 마음껏 추가·삭제할 수 없다.
5. **Celebrity는 늘 출현한다.** 사용자가 1억 명이면 1억분의 1 확률의 거물이 반드시 한 명 이상 있다.

이런 사정을 알면, hot partition을 막는 작업은 도구 도입의 시점이 아니라 **partition key 첫 줄을 쓰는 그 순간**에 시작된다는 것이 이해된다. 그래서 NoSQL을 다루는 시니어 백엔드는 partition key 첫 줄을 보면 거의 직감적으로 "이거 hot 가능성 있다"고 느낀다. 이 직감을 키우는 방법은 안티패턴 몇 개를 손에 익히는 것이다.

### Partition key 안티패턴 5선

다음 다섯 가지 key 설계는 hot partition을 거의 보장한다 — 가능하면 처음부터 피하자.

1. **시간 prefix만 박은 key** (예: `2026-05-16#order-id`) — 자정마다 모든 write가 한 partition에 몰린다. Bigtable 계열에서 특히 치명적이다.
2. **enum 값을 prefix로 박은 key** (예: `status#PENDING#order-id`) — status가 PENDING인 row가 압도적으로 많으면 한 partition이 다 받는다.
3. **순차 증가 ID prefix** (예: auto-increment ID로 partition) — 가장 최신 partition으로 모든 write가 쏠린다.
4. **소수의 정상 사용자 key** — Twitter나 Instagram의 celebrity 사용자가 그대로 partition key가 되면, 그 사람이 트윗 올리는 순간 한 partition으로 모든 트래픽이 쏠린다 — 숫자로 적기 민망한 QPS다.
5. **너무 큰 grain의 key** (예: country code로 partition) — 한국·미국·일본이면 partition이 3개라는 뜻이다. 분산이 거의 안 된다.

이 5개를 피하기만 해도 운영의 절반은 이긴 셈이다. 그렇다면 hot partition이 일단 발생했을 때 무엇을 할 수 있을까?

### Hot partition 발생 후 — 응급 처치 3단계

**1단계: write-side에 jitter·shard 추가.** key 뒤에 random suffix(`#0`~`#15` 같은)를 붙여 한 사용자의 write가 16개 sub-partition으로 흩어지게 한다. read 시점에 16개를 모두 읽어 합쳐야 하므로 비용은 크지만, 응급 처치로는 빠르다.

**2단계: read-side에 cache layer 또는 request coalescing.** 같은 key를 동시에 30,000번 요청하는 게 hot partition의 본질이라면, 그 30,000번을 1번으로 합치는 게 가장 직접적인 방어다. Discord가 정확히 이 길을 택했다 — 잠시 후에 다룬다.

**3단계: 파티션 키 재설계 + 마이그레이션.** 가장 비싼 길이지만, 진짜 root cause다. dual-write·shadow read로 점진 이전하는 plan은 11장에서 다룬다. 한 번 결정하면 보통 2~3개월의 작업이라, 새벽 alert가 1주일 째 안 멈춘다면 결단이 필요하다.

기억해 두자. **hot partition은 거의 모든 NoSQL 운영의 1번 알람이다**. partition key 설계 단계에서 안티패턴을 피하는 비용이, production에서 마이그레이션하는 비용보다 1000배쯤 싸다.

## 6. LSM-tree — write-heavy의 진짜 이유

NoSQL이 write-heavy workload에 강하다는 말은 자주 들리지만, 그 이유가 정확히 무엇인지는 덜 다뤄진다. 답은 대부분 **LSM-tree (Log-Structured Merge Tree)**에 있다. 1996년 P. O'Neil 외 4인이 발표한 원전 논문(P13)이 이 자료구조를 처음 제시했고, 오늘날 Cassandra·RocksDB·LevelDB·DynamoDB 내부·HBase가 모두 이 구조 위에 올라가 있다.

LSM-tree의 핵심 아이디어는 단순하다. **메모리에 정렬된 buffer(memtable)를 두고, full이 되면 disk에 sorted file(SSTable)로 흘려보낸다**. 그러고 나서 정해진 간격으로 여러 SSTable을 merge해 더 큰 SSTable을 만든다. 이걸 compaction이라고 부른다.

이 구조의 가치는 두 가지다. 첫째, **write가 sequential I/O**다 — disk seek가 없다. SSD에서도 random write보다 sequential write가 더 빠르고 lifetime에 유리하다. 둘째, **write가 immutable**이다 — 한 번 disk에 쓴 SSTable은 더 이상 수정되지 않는다. 이게 동시성·복제·snapshot을 단순하게 만든다.

대신 양보한 게 있다. **read amplification**이다. 한 key를 읽으려면 memtable 1개 + disk에 있는 N개의 SSTable을 모두 뒤져야 한다. 이걸 완화하는 도구가 **bloom filter**다 — 각 SSTable마다 "이 key가 여기 있을 수도 있다 / 없다"를 빠르게 판단하는 확률적 자료구조. 없다고 판단되면 그 SSTable은 안 본다. 그런데 bloom filter의 false positive ("있을 수도 있다고 잘못 알려줌")가 가끔 over-fetch를 일으킨다. 첫 번째 만남에서는 거의 늘 의심하지 않는 자리라 더 찜찜하다 — 이 함정은 부록 A의 18가지 tribal knowledge 중 7번 항목에서 다시 다룬다.

또 하나의 함정 — **tombstone**이다. delete가 "지우기"가 아니라 "삭제 마커 쓰기"로 구현되는 LSM-tree의 특성상, TTL이나 대량 delete가 많으면 read가 tombstone을 잔뜩 만나게 된다. Cassandra에서는 한 partition의 tombstone이 1000개를 넘으면 alert를 띄우는 게 거의 표준이다. 이 함정도 부록 A에서 다시 다룬다.

LSM-tree와 대비되는 게 1장 RDB에서 다룬 **B+ tree**다. B+ tree는 in-place update라 read가 predictable하고 write amplification이 낮지만, 대신 random write이라 throughput 한계가 더 빠르다. **write/read 비율과 latency 분포의 모양이 둘 중 어느 쪽이 어울리는지를 결정한다** — write가 99%이고 read의 latency tail이 길어도 괜찮다면 LSM, read latency 일관성이 중요하면 B+ tree.

## 7. Discord 마이그레이션 — 디테일까지 들여다보는 사례

Dynamo 계열의 가장 유명한 운영 케이스 하나를 깊이 들여다보자. 2022년경 Discord가 자사 메시지 storage를 **Cassandra 약 177노드에서 ScyllaDB 약 72노드로** 옮긴 이야기다 (정확한 노드 수는 Discord 발표 자료 기준 — 검증 필요).

Discord가 직면한 문제는 두 가지였다. 첫째, **GC pause**다. Cassandra는 JVM 기반이라 stop-the-world GC가 평균 read latency를 흔든다. 둘째, **single message hot key**다. 어느 인기 메시지 하나가 초당 30,000번 요청을 받는다 — 한 partition이 죽기에 충분한 부하다.

ScyllaDB는 C++로 Cassandra wire protocol을 재구현한 시스템이다. JVM이 없으니 GC pause가 없고, shard-per-core 아키텍처로 NUMA 친화적이다. 마이그레이션 후 **p99 read latency가 40~125ms에서 약 15ms로 떨어졌다**고 Discord 엔지니어링 블로그는 적는다. 노드 수도 절반 미만으로 줄었다.

하지만 진짜 흥미로운 부분은 ScyllaDB 자체가 아니라 **Rust로 작성한 data services layer**다. Discord는 이 layer에서 **request coalescing**을 구현했다. 같은 메시지에 대한 동시 요청을 한 묶음으로 합쳐 DB에는 한 번만 보낸다는 뜻이다. 인용을 보자.

> "Request coalescing is an important responsibility to avoid multiple database calls when many users request the same message."

이 한 줄에 NoSQL 운영의 한 통찰이 들어 있다. **DB 자체를 더 좋은 것으로 바꾸는 것보다, DB 앞에 코드 한 줄을 잘 짜는 게 훨씬 효과적일 때가 있다**. 30,000번을 1번으로 합치면, 어떤 DB든 살아난다. 이 패턴은 3장 캐시의 singleflight 패턴과 한 가족이다.

Discord 마이그레이션은 16장 채팅 시스템에서 한 번 더 깊이 다룬다. 거기서는 메시지 모델·sharding·WebSocket connection 관리와 함께 본다.

## 8. 한국 사례 — 당근의 DynamoDB 선택

이번엔 한국 사례 한 자락을 짚어 보자. 당근(이전 당근마켓)이 채팅 시스템을 만들 때 한 의사결정이다. 당근 채팅팀은 채팅 storage로 **Cassandra가 아닌 DynamoDB**를 골랐다. 이유는 발표(AWS Summit Korea 2022 "2200만 사용자 채팅")에서 솔직하게 밝혀졌다 — **"Cassandra 운영 부담을 회피"**.

이 결정에는 한국 백엔드의 현실적 맥락이 묻어 있다. 자체 IDC가 아니라 AWS 위에 시스템을 올리는 회사 — 인프라팀이 작거나, 24시간 on-call 인력이 충분하지 않은 회사 — 에서는 Cassandra의 운영 부담이 매우 크다. compaction tuning, JVM heap 관리, repair 운영, gossip protocol 디버깅이 모두 Cassandra 운영의 일이다. DynamoDB는 이 모든 걸 AWS가 책임지는 managed 서비스다.

대신 양보한 것도 있다. **DynamoDB는 cost가 throughput·storage 양쪽에 붙는다.** 트래픽이 급증하는 시점에는 on-demand 모드의 청구서가 무서워질 수 있다. 그리고 DynamoDB의 query 패턴은 매우 제한적이다 — partition key + sort key 조합으로만 빠른 query가 가능하고, secondary index(GSI/LSI)는 별도 비용과 별도 일관성 모델을 갖는다.

당근의 결정에서 우리가 배울 것은 단순하다 — **"운영 부담"이 의사결정의 정당한 한 축이 된다**는 점이다. 기술적으로 더 우월한 도구라도, 우리 팀이 감당할 수 없으면 도입할 자격이 없다. 0장에서 짚은 "도입의 자격" 다섯 물음 중 두 번째(우리 팀의 운영 역량)가 정확히 이 자리에서 작동한 사례다.

## 9. 비교 표 한 장 — Cassandra·DynamoDB·ScyllaDB

Dynamo 계열 안에서도 셋의 선택은 갈린다. Hello Interview의 NoSQL 비교 자료(W9)와 reference §2.4를 기반으로 한 페이지 표로 압축해 보자.

| 축 | Cassandra | DynamoDB | ScyllaDB |
|---|---|---|---|
| Hosting | self-managed (Apache 또는 DataStax) | AWS managed | self-managed 또는 ScyllaCloud |
| 언어 | Java (JVM GC 부담) | (AWS 비공개) | C++ (no GC, shard-per-core) |
| Wire protocol | CQL | proprietary API | CQL (Cassandra 호환) |
| 운영 부담 | 매우 높음 | 매우 낮음 | 중간 (Cassandra보다 적음) |
| 비용 모델 | 인프라 비용 | per-request + storage | 인프라 비용 또는 managed |
| 강점 | 성숙도, OSS 생태계 | 운영 부담 zero에 가까움 | 처리량·latency tail |
| 약점 | GC pause, 운영 인력 필요 | cost 예측 어려움, query 제약 | OSS 생태계 비교적 작음 |
| 어울리는 곳 | 대형 internal, 자체 인프라팀 | startup, AWS lock-in 수용 | high-throughput 채팅·게임·IoT |

이 표를 들고 회의 자리에 가면, 적어도 "왜 우리는 X를 골랐나"를 도메인 언어로 설명할 수 있다. 더 좋은 토론은 그 다음에 시작된다.

## 10. NoSQL 도입의 자격 — 다섯 물음 다시 보기

0장에서 우리는 도구 도입의 자격을 묻는 다섯 물음을 정리했다. NoSQL에 적용해 보자.

1. **이 도구를 안 쓰면 정말 못 푸는 문제가 있는가?** RDB의 read replica·partitioning·shard로 풀 수 있는 워크로드라면, NoSQL은 아직 자격이 없다. 정말 write throughput이 RDB의 한계를 넘는가, 정말 schema flexibility가 마이그레이션 비용보다 더 큰 가치인가.
2. **우리 팀의 운영 역량이 이 도구를 감당하는가?** Cassandra라면 JVM·repair·gossip·compaction의 운영을 누가 책임지는가. DynamoDB라면 cost forecasting과 GSI 설계의 한계를 우리 application이 받아들일 수 있는가.
3. **장애가 났을 때 누가 새벽에 일어나는가?** Cassandra 운영자가 1년 뒤에도 우리 회사에 있는가. DynamoDB의 throttling alert를 누가 첫 5분 안에 추적할 수 있는가.
4. **6개월 뒤 이 도구를 걷어낼 길이 있는가?** NoSQL은 데이터 모양이 query-first로 굳어 있어서, RDB로 되돌리는 비용이 매우 크다. 이 결정을 되돌릴 수 없다는 사실을 받아들이는가.
5. **이 결정을 우리 도메인 언어로 설명할 수 있는가?** "scalable해서"가 아니라 "우리 워크로드가 X 패턴을 가져서, partition key를 Y로 잡으면 hot이 안 날 가능성이 높다"고 말할 수 있는가.

이 다섯 물음에 자신 있는 답이 가능할 때, NoSQL을 도입할 자격이 생긴다. 그렇지 않다면, "Just use Postgres" — 1장의 휴리스틱 3이 여전히 정답일 가능성이 높다. RDB의 한계가 오기 전까지 우리가 알지 못하는 NoSQL 운영의 함정이 너무 많기 때문이다.

## 11. 흔히 듣는 오해 다섯 가지

회의 자리에서 자주 도는 오해 다섯 가지를 짚어 보자. 이 다섯 개 답이 손에 익으면, "Mongo 쓰자"는 한 마디에 자동으로 다섯 개의 질문이 떠오른다.

**오해 1: "NoSQL은 스키마가 없어서 schema migration이 없다."** — 틀린 말이다. application 레벨에서 schema가 살아 있고, 그 schema의 변화는 backfill 작업으로 나타난다. RDB의 ALTER TABLE이 안 보일 뿐, 그만큼의 일이 다른 layer에 옮겨 와 있다.

**오해 2: "NoSQL이 RDB보다 빠르다."** — 단일 row read는 그럴 수 있다. 그러나 복잡한 query(join, aggregation)는 거의 항상 RDB가 빠르거나, 아예 안 된다. RDB 인덱스가 잘 잡힌 read는 NoSQL을 가뿐히 이긴다.

**오해 3: "Cassandra가 항상 strong consistency보다 빠르다."** — quorum read(R + W > N)를 쓰면 Cassandra도 latency가 올라간다. eventual 모드일 때만 강점이 빛난다.

**오해 4: "DynamoDB는 매니지드라 운영이 zero다."** — partition key 설계·GSI 관리·cost forecasting·throttling 모니터링은 여전히 우리 일이다. infra 운영은 zero에 가까울 수 있지만, application 레벨의 운영은 그대로 남는다.

**오해 5: "NoSQL은 ACID가 안 된다."** — 더 이상 사실이 아니다. DynamoDB transactions, MongoDB multi-document transactions, Cassandra lightweight transactions가 모두 ACID 일부를 지원한다. 다만 비용이 따로 붙고, 사용 범위에 제한이 있다.

이 다섯 오해를 손에 익히는 것이 NoSQL을 다루는 시니어 백엔드가 되는 길이다. "Mongo가 빠르대"라는 한 마디에 회의 자리에서 멈칫하지 않고 한 박자 깊은 질문을 돌려줄 수 있게 된다.

## 12. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 두 갈래의 지형이 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **두 갈래의 결정 트리.** Dynamo 계열(AP, leaderless, eventual)과 Bigtable 계열(CP, single-leader per tablet, strong). 우리 워크로드가 strong consistency를 어디까지 필요로 하는지가 결정한다.
- **query-first.** 데이터 모델링이 사라진 게 아니라, query를 먼저 정하고 그 모양대로 비정규화해서 박는 일이다.
- **Hot partition은 평생의 적이다.** partition key 첫 줄을 보면 거의 직감적으로 "이거 hot 가능성 있다"고 느끼는 게 시니어의 감각이다. alert에 shard별 QPS skew 한 줄만 더 박아 두자 — 그게 새벽 3시의 자신을 살린다. 응급 처치는 jitter·request coalescing·재설계 3단계.
- **LSM-tree가 write-heavy의 근거다.** 그 대가는 read amplification·tombstone·bloom filter false positive. 부록 A의 tribal 7번·16번 항목으로 다시 만난다.
- **Discord가 보여준 통찰** — DB 자체를 바꾸는 것보다 앞에 request coalescing 한 줄을 잘 짜는 게 더 효과적일 수 있다. 30,000번을 1번으로 합치는 사고는 NoSQL 운영의 보편 도구다.
- **당근이 보여준 통찰** — "운영 부담"은 의사결정의 정당한 한 축이다. 기술적으로 우월한 도구라도 우리 팀이 감당 못하면 자격이 없다.

다음 장에서는 캐시를 짚는다. NoSQL과 캐시는 사실 같은 가족에 가깝다 — 둘 다 RDB의 부담을 다른 layer로 옮겨 빠르게 만든다는 점에서. 그런데 캐시는 NoSQL과는 다른 종류의 잔인함을 품고 있다. 캐시를 한 번이라도 비워본 적이 있다면, 그날 DB가 무사했는지 한 번 떠올려 보자. 그게 3장의 시작이다.

---

<!-- frontmatter -->
- 챕터 번호: 2
- 분량 추정: 한국어 약 15,600자 (≈ 22페이지)
- 본문 인용 reference: §2.4 NoSQL · §2.10 LSM · §4.1 Discord · §4.11 당근, 패턴 2 (community), 한국 7 (community), 1장 callback(휴리스틱 3 "Just use Postgres"), 0장 callback(도입의 자격 5문항), 13장·16장·부록 A callback
- 계획서와 다르게 간 점: 02_plan §3 2장의 거의 모든 항목 커버. 추가로 "흔히 듣는 오해 5가지"를 후반에 박아 회의 자리용 도구를 강화함. Discord case는 16장에서 깊이 다룬다고 callback 표시 (계획서와 일치).
<!-- 개정: 2026-05-16 style-guardian 1차 리뷰 반영 (Critical 0건 + Should 4건 + Nice 4건). 회수 절 메타 톤 풀어쓰기(L192~197 "이번 장의 회수" → "손에 남기고 가야 할 것들"), hot partition 회수 항목에 감정 호흡 추가, mental model 앵커 한 번으로 통일(query-first 두 번째 등장은 헤더만), 오탈자 "알 자유롭게"→"마음껏" 수정, "unprintable한 QPS" 한국어로 풀어쓰기, "paraphrase한다"→"검증 필요" 표기 통일, "schema-on-read"/"always-writable" 한국어 풀이 병기, LSM bloom filter 절에 "찜찜하다" 감정어 한 줄 추가, 오해 절 도입 메타 톤 풀어쓰기 + 절 마무리 중복 회피. -->
