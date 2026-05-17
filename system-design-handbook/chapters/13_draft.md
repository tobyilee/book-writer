# 13장. 샤딩·파티셔닝·Fan-out — 수평으로 늘리는 기술

Sharding key를 잘 골랐다고 자신했던 어떤 팀이 있다. 새 시스템 출시일, 모든 부하 테스트가 통과했고, 데이터 분포 시뮬레이션도 정상이었다. 그런데 출시 30분 만에 한 partition이 전체 트래픽의 95%를 받고 있는 광경을 목격한다. 알고 보니 그날 어떤 인플루언서가 자기 SNS에 우리 서비스 링크를 올렸다. 그 한 사람의 ID가 모든 트래픽을 한 partition으로 몰아넣었다.

이 순간 "celebrity"라는 단어가 단순한 비유가 아니라 진짜 운영 용어가 된다. 우리 시스템에는 항상 celebrity가 있고, sharding 설계는 그 celebrity의 존재를 가정해야 한다. 그게 이 챕터의 출발점이다.

수평 확장(horizontal scaling)이 분산 시스템의 핵심 약속이라면, 그 약속을 가능하게 하는 것이 sharding(또는 partitioning)이다. sharding의 세 방식, consistent hashing의 모양, hot partition을 만드는 5가지 안티패턴, fan-out 패턴(push/pull/hybrid), 그리고 re-sharding의 잔혹함까지 — 한 박자씩 짚어 보자. 한국 사례로 당근 동(neighborhood) 단위 partition도 함께 본다.

## Sharding의 세 가지 방식 — Range, Hash, Directory

데이터를 여러 노드에 나눠 두는 방법은 크게 세 가지다. 각각 다른 trade-off를 갖는다.

### Range-based — 정렬된 key 범위로 분할

key 범위를 노드별로 나눈다. Bigtable, HBase, MongoDB(기본)이 이 모델이다.

```
shard 1: key A-F
shard 2: key G-M
shard 3: key N-S
shard 4: key T-Z
```

장점은 **범위 쿼리가 효율적**이라는 점. `WHERE name BETWEEN 'C' AND 'E'`는 shard 1만 보면 끝난다.

단점은 **hot partition이 잘 생긴다**는 점. 만약 key가 timestamp라면 최신 데이터가 항상 한 shard로 몰린다. 모든 write가 마지막 shard에 가는 상태가 된다.

### Hash-based — 해시값으로 균등 분할

key를 hash 함수에 통과시켜 그 결과로 shard를 정한다. Dynamo, Cassandra, Riak이 이 모델이다.

```
shard_id = hash(key) % N
```

장점은 **균등 분포**가 자연스럽다. timestamp가 key라도, hash가 충돌하지 않으면 모든 shard에 균등하게 흩어진다.

단점은 **범위 쿼리가 불가능**하다는 점. `WHERE timestamp BETWEEN ...`은 모든 shard를 다 봐야 한다. 그리고 **노드 추가·제거 시 거의 모든 key가 재배치**된다. `hash % 4`에서 `hash % 5`로 바뀌면 약 80%의 key가 다른 shard로 이동한다.

### Directory-based — 명시적 매핑

별도의 lookup table이 "이 key는 어느 shard"를 알려 준다. Vitess의 VSchema, MongoDB의 일부 sharding 모드가 이 모델이다.

```
lookup table:
  shop_id 100 → shard 1
  shop_id 101 → shard 1
  shop_id 102 → shard 2
  ...
```

장점은 **유연성**. 특정 shop을 다른 shard로 옮기고 싶으면 lookup table만 갱신하면 된다. hot tenant를 별도 shard로 분리하는 식의 운영이 가능하다.

단점은 **lookup table 자체가 SPOF**가 될 수 있다는 점. 이걸 잘 분산·캐싱해야 한다.

| 방식 | 분포 균등성 | 범위 쿼리 | 재배치 부담 | 대표 사례 |
|------|-----------|---------|------------|---------|
| Range-based | 약함 (hot partition 위험) | 강함 | 노드 추가 시 일부 재배치 | Bigtable, HBase |
| Hash-based | 강함 | 약함 | 노드 추가 시 거의 전체 | Dynamo, Cassandra |
| Directory-based | 운영자 결정 | 약함 | 명시적 마이그레이션 | Vitess, MongoDB (일부) |

## Consistent Hashing — Hash-based의 진화

Hash-based의 가장 큰 약점이 "노드 추가·제거 시 거의 전체 재배치"였다. 이 문제를 푸는 자료구조가 **consistent hashing**이다.

핵심 아이디어는 단순하다. hash 결과 공간을 ring으로 시각화하고, 각 노드를 ring 위 여러 지점에 배치한다. key의 hash가 떨어지는 지점에서 ring을 따라 시계 방향으로 가다가 처음 만나는 노드가 그 key를 소유한다.

```
Ring (0 ~ 2^32):
   Node A: 위치 10, 100, 1000, ... (여러 vnode)
   Node B: 위치 50, 200, 500, ...
   Node C: 위치 30, 300, 800, ...
   
key X의 hash = 250 → 다음 노드가 Node B → Node B가 소유
```

노드 D를 추가하면? D를 ring 위 여러 지점에 배치하면, **D 주변의 일부 key만** D로 이동한다. 다른 노드는 그대로다. 평균적으로 `K/N` 만큼의 key만 이동한다 (K=전체 key, N=노드 수).

여기서 중요한 디테일이 **virtual node**(vnode)다. 노드를 ring 위 한 지점에만 두면 분포가 불균등해진다. 각 노드를 100~200개의 vnode로 ring에 흩어 놓으면 분포가 균등해진다.

> 노드당 100~200 vnode가 일반적. Dynamo·Cassandra·Riak·memcached(client-side) 모두 채택. (ByteByteGo, Consistent Hashing 101)

Consistent hashing은 캐시 cluster(Memcached, Redis Cluster)와 분산 DB(Dynamo, Cassandra)의 backbone이다. 이 모양 없이 큰 분산 시스템을 운영하는 건 거의 불가능하다.

## Hot Partition을 만드는 5가지 안티패턴

2장 NoSQL에서 hot partition은 "평생의 적"이라고 말했다. 그 적을 만드는 5가지 안티패턴을 정리하자. 새 시스템의 sharding key를 정할 때 자기 코드를 한 번 체크해 보자.

### 안티패턴 1. Timestamp를 partition key로

```
PRIMARY KEY (created_at, ...)
```

최신 데이터가 모두 한 partition으로 몰린다. write-heavy 시스템이라면 그 partition은 5분도 못 버틴다.

**해결:** date를 day 단위로 자르고 user_id나 다른 차원과 조합. 예: `PRIMARY KEY ((user_id, date_bucket), ...)`.

### 안티패턴 2. Boolean 또는 enum을 partition key로

```
PRIMARY KEY (status, ...)  -- status: PENDING / COMPLETED / FAILED
```

distinct 값이 3개뿐이라 3개 partition만 쓴다. 나머지 노드는 모두 idle.

**해결:** 더 cardinality가 높은 차원을 partition key로. status는 secondary index로.

### 안티패턴 3. Celebrity user를 가정 안 함

```
PRIMARY KEY (user_id, ...)
```

대부분 user는 100개씩 row를 가지는데, 한 celebrity user는 1억 row를 가질 수 있다. 그 user의 partition이 비대해진다.

**해결:** celebrity의 데이터를 별도 partition으로 분리 (Twitter의 fanout-on-read 모델 참고).

### 안티패턴 4. Sequential ID를 partition key로

```
PRIMARY KEY (id, ...)  -- id가 auto-increment
```

새 row가 모두 마지막 partition으로 간다 (range-based 시). 또는 hash-based여도 cardinality는 높지만 한 partition 안에 너무 많은 row가 쌓일 수 있다.

**해결:** prefix 또는 hash 첨가로 분산.

### 안티패턴 5. Compound key의 첫 컬럼만 보고 분포 가정

```
PRIMARY KEY ((tenant_id, doc_id), ...)
```

tenant_id가 균등 분포라고 가정. 실제로는 한 tenant가 전체 트래픽의 95%인 경우.

**해결:** tenant 단위 분포 분석 + hot tenant 분리.

## 분포 검증의 두 가지 방법

sharding key를 정했다면 분포를 미리 검증해야 한다. 두 가지 방법이 있다.

**1. Production data sample을 hash로 시뮬레이션.** 실제 데이터에서 1만 row sample을 뽑아 sharding key로 hash해 본다. 분포가 균등한지 시각화. 한 partition에 5% 이상 몰리면 안티패턴 의심.

**2. Top-N partition 모니터링.** production에서 partition별 read·write 빈도를 모니터링한다. Top 10 partition이 전체의 50% 이상을 받고 있다면 hot partition 발생 중.

Cassandra에서는 `nodetool tablestats`, DynamoDB에서는 CloudWatch의 ConsumedCapacity per partition으로 확인할 수 있다. 이런 모니터링이 없으면 hot partition은 5분 만의 사고로만 보이고, 그제야 원인을 찾기 시작한다.

## Shopify Pods — Directory-based의 모범 답

한 가지 흥미로운 사례가 Shopify의 pods 아키텍처다. Shopify는 수백만 개의 상점(shop)을 호스팅하는 SaaS다. 각 상점의 트래픽이 크게 다르고, BFCM(Black Friday/Cyber Monday) 시점에 일부 상점이 폭주한다.

Shopify는 **pods**라는 단위를 도입했다. 각 pod은 완전 독립된 MySQL cluster + Redis + 배경 인프라다. shop_id가 어느 pod에 속할지를 directory table이 관리한다.

```
shop 12345 → pod-3
shop 67890 → pod-3
shop 11111 → pod-7
```

이 모양의 장점이 크다.

**1. 운영 격리.** pod-3에 사고가 나도 pod-7은 영향 없다. blast radius가 한 pod으로 한정.
**2. Hot tenant 분리.** 폭주하는 shop이 있으면 그 shop을 자기만의 pod으로 옮길 수 있다.
**3. 점진적 마이그레이션.** 새 기능을 한 pod에만 먼저 배포해 보고, 안정되면 전체로 확장.

Shopify 엔지니어링의 한 줄이 이 결정을 정리한다.

> Only the databases are podded since they are the hardest component to scale, and everything else that is stateless is scaled automatically. (Shopify Engineering)

DB만 pod 단위로 격리하고, 나머지 stateless 컴포넌트는 K8s autoscale로 처리. 운영 부담을 분산 SQL(CockroachDB·Spanner)으로 가는 대신 directory-based sharding으로 푼 사례다.

## Fan-out — Push / Pull / Hybrid

Sharding이 데이터를 가르는 패턴이라면, **fan-out**은 한 이벤트를 여러 대상에 분배하는 패턴이다. 가장 흔한 예가 SNS의 timeline이다.

A가 트윗 한 개를 올렸다. A를 팔로우하는 사람이 1만 명이라면, 그 트윗은 1만 명의 home timeline에 도달해야 한다. 이 1:N 분배를 어떻게 구현할까? 세 가지 모델이 있다.

### Fanout-on-write (Push)

A가 트윗을 올리는 순간, A의 1만 follower의 home timeline에 그 트윗을 미리 분배한다.

```
A의 트윗 → 1만 follower의 timeline cache(예: Redis sorted set)에 모두 insert
```

**장점:** read가 매우 빠르다. follower가 home을 열면 자기 timeline cache를 그대로 read.
**단점:** write가 비싸다. follower가 1만이면 write 1번이 1만 번의 cache insert가 된다.

### Fanout-on-read (Pull)

A가 트윗을 올린다. 다른 곳에 분배하지 않는다. follower가 home을 열 때, follower가 팔로우하는 모든 user의 최근 트윗을 모아 정렬한다.

```
follower B의 home 열기 → B가 팔로우하는 user들의 최근 트윗 모두 read → merge sort
```

**장점:** write가 싸다. 트윗 1번은 그냥 자기 timeline에 1 insert.
**단점:** read가 비싸다. 1000명 팔로우 중인 B가 home을 열면 1000명의 트윗을 read해야 한다.

### Hybrid — 둘을 결합

Twitter, Instagram 같은 큰 SNS의 결정은 hybrid다.

- **일반 사용자:** fanout-on-write (push). follower 수가 적어 cost가 낮음.
- **Celebrity (10K+ followers):** fanout-on-read (pull). 한 트윗으로 100만 cache insert는 감당 불가.

follower가 home을 열 때, push로 받은 일반 사용자 트윗 + pull로 가져온 celebrity 트윗을 merge한다. follow 시점에 user별로 push/pull 모드가 결정되어 있다.

이 hybrid 모양이 Twitter, Instagram, Facebook 등의 home timeline 표준이다. 한국에서는 LINE, 카카오스토리, 인스타그램(한국) 모두 비슷한 모양을 쓴다.

> 💡 celebrity 임계 기준 — Twitter는 10K, Instagram은 1K~10K. 도메인마다 다르다. 자기 시스템에서는 **fanout cost가 user별로 어떻게 분포되는지 미리 시뮬레이션**해서 임계를 정하는 편이 낫다.

## 한국 사례 — 당근 동(neighborhood) 단위 partition

당근마켓의 sharding은 특이하다. 일반 SNS는 user_id로 partition하지만, 당근은 **지역(동)** 단위로 partition한다. 왜?

당근의 핵심 도메인은 hyperlocal 거래다. 사용자가 보는 채팅·검색·매물은 모두 자기 동(neighborhood) 안의 데이터다. 그래서 user_id 대신 region_id로 partition하면 다음 이득이 생긴다.

**1. Locality.** 한 사용자의 모든 쿼리가 한 partition으로 간다. cross-partition 쿼리가 거의 없음.
**2. Cache 친화적.** 같은 동 사람들이 같은 데이터를 보니 cache hit이 높다.
**3. Hot region 격리.** 강남·송파처럼 활성도 높은 지역은 별도 partition으로 분리 가능.

당근 채팅 시스템(W31)이 DynamoDB를 채택하면서 동 단위 partition을 채택한 이유가 이거다. AWS Summit Korea 2022 "2200만 사용자를 위한 채팅 시스템 아키텍처"에서 변규현 발표자가 정확히 짚었다. **"hyperlocal 도메인이라면 partition도 hyperlocal이어야 한다."**

이 결정은 도메인이 sharding key를 결정한 사례다. 일반적인 "user_id로 partition"이 모든 시스템의 답은 아니다. 자기 도메인의 본질이 무엇인지 보고, 그 본질에 맞는 partition key를 골라야 한다.

## Re-sharding의 잔혹함

sharding key를 한 번 정하면 바꾸기 매우 어렵다. 그래서 신중하게 정해야 하지만, 그래도 결국 re-shard가 필요한 순간이 온다. 데이터가 커지거나, partition key 결정이 잘못된 게 늦게 발견되거나, 도메인이 변하거나.

re-sharding의 표준 패턴은 다음 4단계다.

```
1. Dual-write: 새 shard와 옛 shard에 모두 write 시작
2. Backfill: 옛 shard의 모든 데이터를 새 shard로 복제
3. Shadow read: 새 shard에서도 read 시작, 옛 shard 결과와 비교 (consistency 검증)
4. Cutover: 새 shard로 read·write 모두 전환, 옛 shard 정리
```

이 패턴은 단순해 보이지만 끔찍한 디테일이 많다.

**1. Dual-write 일관성.** 두 shard에 write가 atomic하지 않으니, 한쪽만 성공하는 경우가 생긴다. retry + idempotency로 해결.

**2. Backfill 시간.** TB급 데이터라면 backfill에 며칠~몇 주가 걸린다. 그 사이 dual-write 부담도 지속.

**3. Consistency 검증.** shadow read에서 두 shard의 결과가 다른 경우, 어느 쪽이 맞는지 판단해야 한다. 당근의 Cassandra → DynamoDB 마이그레이션에서 가장 큰 도전이 이 부분이었다(community 패턴 10).

**4. Rollback 가능성.** cutover 후 문제가 발견되면 옛 shard로 돌아갈 수 있어야 한다. cutover 직후 며칠은 옛 shard도 유지.

re-sharding을 한 번이라도 해본 팀은 그 잔혹함을 평생 기억한다. 그래서 **처음에 sharding key를 정할 때 다음 5년의 트래픽 패턴을 충분히 시뮬레이션**하는 편이 낫다. 또는 directory-based를 채택해 운영 시 유연성을 확보하는 것도 방법이다.

## Cross-region Replication — 광역 분산의 trade-off

마지막으로 광역 분산(multi-region)을 짚자. 단일 region 안에서의 sharding이 끝나면, 다음 단계는 region 단위 분산이다. AWS의 us-east-1과 ap-northeast-2에 데이터를 모두 두는 식.

이 결정의 trade-off는 **latency와 consistency**다.

**1. Active-Passive.** 한 region이 primary, 다른 region은 replica (DR용). write는 항상 primary로, read는 양쪽 가능. failover 시 primary 전환.

**2. Active-Active.** 두 region 모두 write 가능. 같은 데이터에 두 region에서 동시 write 시 conflict resolution 필요.

**3. Geo-partition.** 한 region이 한국 사용자, 다른 region이 일본 사용자. 데이터 자체가 region별로 갈림.

| 모델 | latency | consistency | 운영 복잡도 |
|------|---------|------------|----------|
| Active-Passive | primary 가까운 곳만 빠름 | strong (single primary) | 보통 |
| Active-Active | 모든 region에서 빠름 | conflict resolution 필요 | 매우 높음 |
| Geo-partition | region별 사용자만 빠름 | region 내 strong | 보통 |

Spanner·CockroachDB가 active-active를 약속하지만, 그 비용은 commit wait 또는 cross-region round-trip이다. 한국 백엔드의 90%는 active-passive(DR용)로 충분하다. active-active가 정말 필요한 경우는 글로벌 서비스(LINE 메시징, 카카오엔터 글로벌 콘텐츠 등)에 한정.

## Sharding 도입 자격을 묻는 5가지 질문

새 시스템에 sharding을 도입하기 전에 자기에게 던질 다섯이다.

1. **단일 DB로 정말 안 되는가?** Postgres·MySQL의 single primary는 수십만 QPS까지 견딘다. 한계가 명확히 보인 후에야 sharding.
2. **partition key가 자기 도메인의 본질을 반영하는가?** user_id가 default지만, hyperlocal·tenant·time 등 다른 차원이 맞을 수 있다.
3. **hot partition 가능성을 시뮬레이션했는가?** 5가지 안티패턴 중 어느 하나에 해당하지 않는지 검증.
4. **re-shard rollout plan을 가지고 있는가?** 처음 정한 key가 잘못됐을 때 어떻게 옮길지 미리 준비.
5. **fan-out이 필요한가, 그렇다면 push/pull/hybrid 중 무엇이 맞는가?** celebrity의 존재가 fan-out 모델을 결정.

이 다섯에 답이 명확하지 않으면 sharding을 미루는 편이 낫다. 단일 DB로 시작해서 한계가 오면 그때 sharding을 도입해도 늦지 않다.

## Callback 예고

13장의 sharding·fan-out은 후속 챕터에서 핵심 패턴으로 등장한다.

- **17장 피드·타임라인.** Twitter·Instagram·카카오스토리의 hybrid fan-out 구조.
- **18장 검색·매칭·지오.** Uber H3, 당근 거래 매칭의 geo partition.
- **19장 결제·금융.** 토스 코어뱅킹의 user 단위 partition + 거래 history sharding.

이 챕터의 5가지 안티패턴이 머릿속에 있어야 후속 케이스 스터디의 sharding 결정이 따라온다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 수평 확장의 세 패턴이 손에 잡혀 있다. Range/Hash/Directory 세 sharding 방식, consistent hashing의 ring 모양과 vnode, hot partition을 만드는 5가지 안티패턴, fan-out의 push/pull/hybrid 결정, Shopify pods와 당근 동 단위 partition의 사례, 그리고 re-sharding의 잔혹함과 광역 분산의 trade-off까지가 한 묶음이다.

기억해두자. sharding은 한 번 정하면 바꾸기 어려운 결정이다. partition key를 한 번 잘못 정하면 5년의 운영 부담으로 돌아온다. 그래서 처음에 자기 도메인의 본질을 정확히 보고 key를 정하는 편이 낫다. 그리고 항상 **celebrity가 존재한다**는 사실을 가정하자. 그 가정이 없는 sharding은 출시 30분 만에 무너진다.

다음 장에서는 시스템이 자기 자신을 보는 법을 살펴본다. Rate limiting, 백프레셔, SLO, 관측성, on-call. 분산 시스템을 만드는 것만큼 운영하는 일이 어렵다는 사실을, 그 운영에 필요한 부품들과 함께 짚어 보자.
