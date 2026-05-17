# 12장. 합의·복제·일관성 모델 — Raft를 알면 무엇이 보이는가

회의에서 동료가 묻는다고 해보자. "우리 결제 시스템은 strong consistency가 필요한가요?" 답이 입에서 나오기 전에 머리 안에서 단어 한 무더기가 부딪힌다 — linearizability, sequential, causal, eventual, PACELC. 정의는 책에서 본 적이 있는데, 우리 결제 시스템이 정확히 이 중 어느 줄에 있는지 한 박자에 답하기는 어렵다. DDIA를 다 읽었다고 해도, 한 달 뒤 그 질문 앞에서 똑같이 막힌다. 답은 책 안에 있지만, 책의 단어와 우리 회사의 단어가 다르기 때문이다.

이 한 줄을 풀려고 우리는 분산 시스템 50년의 이론을 다섯 페이지로 압축해야 한다. 그 압축이 이번 장의 목적이다. Paxos가 1989년에 시작한 합의의 사고법, Raft가 2014년에 그걸 "이해 가능하게" 다시 쓴 결정, ZAB이 ZooKeeper에 자리 잡았다가 Kafka가 KRaft로 옮겨 간 운영의 진실, single-leader·multi-leader·leaderless 복제가 약속하는 것·양보하는 것, 그리고 마지막으로 CAP→PACELC→CALM이라는 일관성 이론의 세 단계 — 이걸 우리 도메인 언어로 다시 묶어 보자.

## 1. FLP impossibility — 분산 합의의 출발점에 박힌 한 줄

분산 합의에 관한 이야기를 시작할 때 빼놓을 수 없는 한 편의 논문이 있다. **FLP impossibility (Fischer·Lynch·Paterson, 1985, P30)**다. 한 줄로 요약하면 — **"완전 비동기 네트워크에서, 결정적 알고리즘으로는 합의를 보장할 수 없다."** 한 노드가 영원히 멈춰 있는지, 단순히 느린지 — 비동기 모델에서는 이걸 결정적으로 구별할 수 없기 때문이다.

이 결과는 분산 시스템 학계에 큰 충격이었다. 그렇다면 합의는 어떻게 가능한가? 답은 **"실용 알고리즘은 무엇을 양보해서 가능하게 만들었는지 정확히 봐야 한다"**는 것이다. Paxos·Raft·ZAB 같은 알고리즘들은 모두 FLP의 그림자 안에서 작동한다. 보통은 두 가지 중 하나(또는 둘 다)를 양보한다.

- **Liveness 양보.** 네트워크가 안정될 때까지 진행이 멈출 수 있다. 안정되면 결국 합의가 끝난다 — eventual progress.
- **Stable leader 가정.** leader가 가끔 바뀌어도 대부분 시간 동안은 한 명의 leader가 유지된다고 가정한다.

기억해 두자. **분산 합의는 마법이 아니라 trade-off다.** "Raft를 도입하니 다 해결됐다"가 아니라, "Raft가 어떤 가정 아래에서 어떤 보장을 주는지 알고 도입하면 새벽 alert이 줄어든다"는 자세가 시니어와 그렇지 않은 사람의 차이다.

## 2. Paxos — 유명하기 어렵게 유명한 합의

1989년 Leslie Lamport가 *The Part-Time Parliament* (P1)에서 처음 제시한 Paxos는, 학계에서 "이 논문 이해하기 너무 어려워서 reject 당한" 일화로 유명하다. 결국 1998년에 출판됐고, 그 후 2001년 Lamport가 *Paxos Made Simple*이라는 친절한 후속 논문을 또 써야 했다. 그래도 어렵다는 평가는 사라지지 않았다.

Paxos가 어려운 데는 이유가 있다. 한 라운드의 합의를 **prepare·promise·accept·learn 4단계**로 나누어 설명하는데, 각 단계의 의미와 어떻게 안전성·진행성을 보장하는지가 한 번에 머리에 들어오기 어렵다. 그리고 "단일 값 합의"인 basic Paxos를 "log 합의"로 확장한 Multi-Paxos는 또 한 단계 복잡해진다. 그래서 Google Chubby·Spanner 같이 Paxos를 실제 production에 박은 사례는 있지만, 일반 개발자가 Paxos를 직접 다루는 일은 거의 없다 — 대부분 도구가 추상화해 둔다.

그럼 왜 Paxos를 굳이 짚어야 할까? **현대 모든 합의 알고리즘이 Paxos가 만든 사고 틀 위에 있기 때문**이다. Raft도 ZAB도 Paxos가 푼 문제(왜 majority quorum이 안전한가, 왜 한 번 결정된 값은 바뀔 수 없는가)를 다른 표현으로 다시 쓴 것에 가깝다. Paxos를 정복할 필요는 없지만, 그 영향 아래 있다는 사실은 알아 두는 편이 낫다.

## 3. Raft — "이해 가능성"을 first-class goal로

2014년 Diego Ongaro와 John Ousterhout가 발표한 *In Search of an Understandable Consensus Algorithm* (P2)는 합의 알고리즘 영역의 풍경을 바꿨다. Raft 논문은 자기 첫 문단에서 도발적으로 선언한다 — **"Paxos가 어렵다는 사실은 학습·실무 양쪽에 해로웠다. 우리는 이해 가능성(understandability)을 first-class goal로 두는 합의 알고리즘을 만들었다."**

Raft가 단순한 비결은 세 가지 분해다.

1. **Leader election.** 일정 시간 leader로부터 heartbeat이 없으면 follower 중 하나가 candidate가 되고, majority의 표를 받으면 새 leader가 된다. 단순하고 명확하다.
2. **Log replication.** leader가 모든 write를 받아 자기 log에 append하고, follower들에게 복제한다. majority가 commit하면 그 entry는 "committed"로 marking된다.
3. **Safety.** 새 leader는 자기 log가 이전 commit된 entry를 모두 포함하고 있을 때만 선출될 수 있다 — log completeness check.

이 세 분해가 Raft의 강점이다. Paxos가 한 묶음으로 다루던 합의 과정을 세 독립 메커니즘으로 나눠 설명하니, 학습 비용이 훨씬 낮아진다. 그리고 그 효과는 production에 즉시 나타났다 — Raft는 출현 후 10년 사이에 **etcd, Consul, TiKV, CockroachDB, Kafka KRaft, 그리고 수많은 OSS 프로젝트의 default 합의 알고리즘**으로 자리 잡았다. 분산 합의 영역의 사실상 산업 표준이라고 봐도 좋다.

> "Raft separates the key elements of consensus, such as leader election, log replication, and safety." — Ongaro 2014 (P2)

## 4. ZAB — ZooKeeper의 atomic broadcast, 그리고 Kafka의 결정

세 번째 합의 알고리즘 **ZAB (ZooKeeper Atomic Broadcast)**도 짧게 짚어 두자. ZAB는 ZooKeeper 안에서 작동하며, 2008년경부터 Hadoop·HBase·초기 Kafka 같은 거대 시스템들의 coordination 레이어를 책임져 왔다 (P3).

ZAB는 Paxos·Raft와 형제 알고리즘에 가깝다. 안정 leader + log 복제 + majority quorum 같은 핵심 아이디어가 같다. 다만 "broadcast"라는 단어가 보여주듯, ZAB는 client 명령을 전체 ensemble에 atomic하게 퍼뜨리는 데 최적화돼 있다. ZooKeeper API의 단순함이 이 위에 얹혀 있다.

그런데 — Kafka가 2.8부터 ZooKeeper를 떼어내고 **KRaft (Kafka Raft)**로 갈아탔다는 사실이 시사하는 게 있다. 알고리즘 자체보다 **운영 부담**이 더 큰 결정 요인이라는 것이다. ZooKeeper를 Kafka와 함께 운영한다는 건 두 개의 분산 시스템을 동시에 책임진다는 뜻이다 — leader election·split-brain·persistent storage·JVM tuning이 두 배가 된다. Raft를 Kafka broker 자체에 내장하면 그 부담이 절반이 된다. 알고리즘이 더 우수해서가 아니라, 운영의 한 layer를 없애는 게 더 큰 가치였다.

**기억해 두자 — 합의 알고리즘 선택은 보통 알고리즘 자체보다 그것을 운영하는 시스템의 layer 수가 더 큰 변수다.** 우리가 새 시스템을 만들 때 ZooKeeper를 떠올리기 전에 "정말 외부 coordination service가 필요한가, etcd로 충분한가, 아니면 application 안에 Raft library를 박는 게 더 단순한가"를 한 번 더 묻는 편이 낫다.

## 5. Replication — leader 수로 보는 세 갈래

합의는 보통 "복제 log를 안전하게 합치는 방법"으로 쓰인다. 그렇다면 복제 자체는 어떤 모양들이 있을까? Leader 수로 가르는 게 가장 명쾌한 분류다.

### Single-leader replication

한 명의 leader가 모든 write를 받고, follower들이 비동기 또는 동기로 그 write를 복제받는다. Postgres·MySQL·Redis(default)·MongoDB(primary-secondary)가 모두 이 모델이다. 단순하고 빠르고, 대부분 시스템의 default다.

양보한 것은 명확하다. **write 가용성이 leader 1명에 묶여 있다.** leader가 죽으면 새 leader가 선출되기 전까지 write가 멈춘다 — failover 기간 동안 짧은 다운타임이 생긴다. Single-leader 시스템의 운영 깊이는 보통 이 failover의 정밀도(자동·수동·시간)에서 결정된다.

### Multi-leader replication

여러 leader가 각자 write를 받는다. 데이터센터마다 하나씩 leader를 두고 사용자 가까운 leader에 write를 보내는 모델이다. 글로벌 서비스에서 latency를 줄이는 데 강하지만 — **write conflict가 필연적**이다. 같은 row를 두 leader가 동시에 수정하면 어떤 버전을 살릴지 결정해야 한다. last-write-wins, application-level merge, CRDT 같은 도구가 동원된다.

Multi-leader는 운영이 까다로워 일반 시스템에는 잘 쓰이지 않는다. 대신 **multi-datacenter Cassandra, BDR(Bi-Directional Replication) for Postgres, CouchDB 같은 특수 케이스**에 등장한다. 그리고 15장에서 다룰 CRDT가 이론적 기반을 제공한다 — CALM theorem과 연결된다(이건 잠시 후에 본다).

### Leaderless replication

leader가 없다. 모든 노드가 write를 받고, quorum 합의로 consistency를 만든다. **Dynamo·Cassandra·Riak**이 이 모델의 대표다. N(복제본 수)·R(read quorum)·W(write quorum)을 application이 튜닝한다 — R + W > N이면 strong-ish consistency, 그렇지 않으면 더 빠른 응답. 2장 NoSQL에서 짧게 본 내용이다.

Leaderless의 강점은 분명하다 — **write가 멈추지 않는다.** 노드 하나가 죽어도 다른 노드들이 write를 받는다. 양보한 것은 strong consistency다. 모든 conflict가 application 책임이 된다.

세 갈래를 한 줄 표로 정리해 보자.

| 축 | Single-leader | Multi-leader | Leaderless |
|---|---|---|---|
| Write 가용성 | leader 살아 있을 때만 | 항상 (각 leader 독립) | 항상 (quorum 살아 있으면) |
| Consistency | 강함 | 충돌 — application | quorum 튜닝 |
| 운영 복잡도 | 낮음 | 매우 높음 | 중간 |
| 대표 사례 | Postgres·MySQL·Redis | Cassandra multi-DC·BDR·CouchDB | Dynamo·Cassandra·Riak |
| 어울리는 곳 | 90% 시스템 | 글로벌 다중 데이터센터 | write-heavy + AP 선호 |

회의 자리의 정답은 보통 **"우선 single-leader. multi-leader·leaderless는 강한 정당화가 있어야 한다."**다. 한국 백엔드의 90%는 single-leader RDB로 충분하고, 운영 깊이는 그 위에 read replica·read 분산·partitioning을 얹는 데서 결정된다. multi-leader를 떠올렸다면 그 회의 자리에서 한 번 더 의심해 보자.

## 6. 일관성 모델 — 강 → 약 한 줄로 늘어놓기

이제 본격적으로 동료의 질문 — "우리 시스템에 strong consistency가 필요한가?" — 에 답할 수 있는 어휘를 정리하자. 일관성 모델은 강한 것부터 약한 것까지 한 줄로 늘어놓는 게 가장 명쾌하다.

### Linearizability — 가장 강한 보장

**linearizability**는 "분산 시스템이 마치 single-machine atomic 연산을 하는 것처럼 보이는" 가장 강한 보장이다. 한 client가 write를 끝낸 직후, 다른 client가 read하면 그 write가 반드시 보인다. global wall clock 시각에 맞춰진 단일 순서가 모든 노드에 일관되게 보이는 모델이다.

대가는 크다. 글로벌 strong consistency를 보장하려면 commit 전에 cross-region quorum 응답을 기다려야 한다 — latency가 region 간 RTT만큼 늘어난다. Spanner의 commit wait이 그 비용 중 하나다 (8장 callback). 거의 모든 시스템이 이 비용을 감당할 가치가 있는 자리는 매우 좁다 — 금융 거래, 글로벌 inventory, audit chain 같이 한 줄도 어긋나면 안 되는 자리.

### Sequential consistency — 단일 순서, but wall clock 자유

**sequential consistency**는 모든 노드가 같은 순서로 연산을 본다는 보장. 다만 그 순서가 실제 시간(wall clock)에 맞을 필요는 없다. "한 client가 A → B 순서로 호출하면 다른 모든 client에서도 A → B 순서로 보인다"가 핵심이다. linearizability보다 한 단계 약하지만, 분산 시스템에서 흔히 보는 보장이다.

### Causal consistency — 인과만 보존

**causal consistency**는 인과 관계가 있는 연산들의 순서만 보존한다. A가 B를 일으켰다면 모든 노드가 A를 먼저 본다. 인과 관계가 없는 연산들은 순서가 자유롭다. 8장에서 다룬 Lamport의 happens-before가 정확히 이 보장을 만든다.

흥미로운 점은 — **causal consistency는 HAT (Highly Available Transactions) 영역에서 도달 가능한 가장 강한 보장**이다. Bailis와 동료들이 2013년 발표한 *Highly Available Transactions* (P12)에서 정리한 결과다. 네트워크 partition이 일어나도 양쪽 partition에서 모두 진행이 가능하면서, causal 순서는 깨지지 않는다. multi-master·offline-first 시스템이 이 결을 따라간다 — Figma·Linear 같은 협업 도구가 대표 사례다 (15장 callback).

### Read-your-writes, monotonic reads — 약하지만 자주 필요한 보장

**read-your-writes** = "내가 방금 쓴 값은 내가 다시 읽으면 반드시 보인다." session 단위로 제공되는 보장이다. 캐시 layer가 있는 시스템에서 자주 깨지는데, 사용자 경험에 즉시 영향을 준다 — "방금 댓글 달았는데 새로고침하니 사라졌어요"의 정체. session affinity나 read 후 write까지 단일 노드로 라우팅하는 게 방어법이다.

**monotonic reads** = "내가 한 번 본 값보다 옛 값을 다시 보지는 않는다." 시간이 거꾸로 가는 듯한 광경을 막는다. 약하지만 사용자에게는 일관성의 최소 단위다.

### Eventual consistency — 가장 약한 보장

**eventual consistency**는 "충분한 시간이 지나면 결국 모든 노드가 같은 값을 본다"는 보장. 그 사이의 임시 불일치는 허용한다. Dynamo·Cassandra의 default이고, 캐시·CDN·검색 인덱스 같은 layer가 대부분 이 모델에서 작동한다.

여섯 단계의 강도 차이를 한 그림으로 그려 보자.

```
linearizability  >  sequential  >  causal  >  read-your-writes  >  monotonic reads  >  eventual
       강                                                                             약
   global wall                                                              "결국엔 같아짐"
```

이 사다리 어느 줄에 우리 시스템 데이터가 있는지 — 그게 회의 자리에서 동료에게 답하는 첫 단계다.

## 7. CAP → PACELC — 한 박자 더 정직한 trade-off

CAP 정리는 모두 들어봤을 거다. Eric Brewer가 2000년 conjecture로 제시했고, Gilbert·Lynch가 2002년에 증명했다(P31). "분산 시스템은 Consistency·Availability·Partition tolerance 중 두 가지만 동시에 만족할 수 있다." 단순하고 강력한 한 줄이다.

다만 CAP에는 함정이 하나 있다. **CAP가 가정하는 "partition"이 production에서 일어나는 시간은 매우 짧다**는 점이다. 한 시스템이 1년 중 99% 이상은 partition 없는 상태로 돈다. 그 99% 시간 동안 CAP는 답을 주지 않는다 — "consistency vs availability"는 partition 상황의 trade-off일 뿐이다.

그래서 Daniel Abadi가 2010년에 **PACELC** 확장을 제안했다(W17). 한 줄로 풀면 — **"Partition 시에는 A vs C(원래 CAP), Else에는 L(latency) vs C(consistency)."**

이 한 줄이 production의 진짜 trade-off를 잡는다. partition이 없는 99% 시간 동안에도, strong consistency를 원하면 commit 전에 multi-node 합의를 기다려야 한다 — latency가 늘어난다. eventual consistency를 받아들이면 즉시 응답할 수 있다. **이게 평상시 진짜 trade-off**다.

> "Eventual consistency is often chosen for performance reasons during normal operation, not just for partition resilience." — Abadi (W17)

PACELC 한 단어가 회의 자리에서 의외로 강력하다. "우리 시스템은 PA/EL입니다"라고 답할 수 있으면, 동료에게 partition·평상시 두 시나리오에서 무엇을 양보했는지를 한 줄로 전달한 셈이다.

### Abadi의 NewSQL 비판 — 한 박자 짚고 가기

Abadi는 같은 발표에서 NewSQL의 marketing에 한 가지 가시 같은 비판을 던졌다. **"Spanner의 default isolation level은 사실상 not serializable이다"**(W4 — 검증 필요, Abadi 원문 참조 권장). Spanner가 강한 consistency를 약속하지만, default가 snapshot isolation에 가까워 실제 serializable한 동시성 보장이 아니라는 지적이다.

NewSQL 도구들의 마케팅과 실제 보장 사이의 gap을 정직하게 보는 시각이 필요하다는 의미다. **"strong consistency"라는 단어를 도구 광고에서 봤다면, 정확히 어느 줄(linearizability? sequential? causal? snapshot isolation?)에 해당하는지 한 번 더 묻자.** 도구마다 그 단어가 다른 곳을 가리킨다.

## 8. CALM theorem — CRDT가 왜 가능한지의 이론적 근거

마지막으로 짚어 둘 한 가지 — **CALM theorem (Consistency As Logical Monotonicity, 2011, P6)**이다. Hellerstein과 동료들이 발표한 이 정리는 분산 시스템 이론에 한 가지 우아한 답을 제공한다 — **"coordination-free한 분산 계산이 가능한 조건은, 그 계산이 monotonic하다는 것이다."**

monotonic하다는 건 한 번 도달한 결과가 시간이 지나도 뒤집히지 않는다는 뜻이다. 집합에 원소를 추가하기만 하는 연산, max·min을 계산하는 연산, true가 되면 false로 안 돌아가는 flag 같은 게 monotonic이다. 반면 "원소를 추가도 하고 삭제도 한다"는 연산은 monotonic이 아니다 — 결과가 시간에 따라 뒤집힌다.

CALM의 핵심 함의는 — **"분산 시스템에서 coordination(합의·잠금) 없이 일관성을 얻고 싶다면, 데이터 모델을 monotonic하게 설계하라"**. 이게 CRDT(Conflict-free Replicated Data Type)의 이론적 근거다. CRDT는 union·max 같은 monotonic 연산만으로 구성된 자료구조라, multi-leader 환경에서도 conflict 없이 동작한다.

CALM의 실무적 가치는 — **"이 데이터에 합의가 필요한가, 아니면 monotonic 설계로 우회할 수 있는가"를 묻는 시각**이다. 예컨대 "총 좋아요 수" 같은 카운터는 add-only로 만들면 monotonic이라 합의가 필요 없다. "삭제 가능한 좋아요"라면 monotonic이 아니라 합의가 필요해진다. 작은 모델링 차이가 운영 비용을 결정한다.

15장에서 CRDT를 짧게 sidebar로 다룬다 — Figma multiplayer·local-first software의 수학적 기반이다. CALM theorem이 그 영역의 출발점이라는 사실만 여기 박아 두자.

## 9. 한국 사례 — 카카오뱅크 99.99% 가용성과 합의의 자리

한국 백엔드 시각으로 합의·일관성이 가장 두드러지는 자리는 금융이다. **카카오뱅크의 99.99% 가용성**(W41)은 이 챕터의 사고법이 production에 어떻게 적용되는지를 보여주는 한 가지 사례다.

99.99%라는 숫자는 한 해 약 53분의 다운타임을 허용한다는 뜻이다. 결제·송금이라는 critical path에서 이 정도를 지키려면 — single-leader RDB의 failover 시간 자체가 SLO budget의 큰 비중을 차지한다. 그래서 카카오뱅크는 메인프레임에서 MSA로 옮겨가면서, **각 도메인의 SLO를 따로 측정하고 각자 적합한 일관성·복제 모델을 골랐다**고 발표에서 짚는다 (검증 필요 — 발표 원문 확인 권장).

핵심은 두 가지다. ① **모든 도메인에 strong consistency를 강제하지 않는다.** 정산은 strong, 알림은 eventual, audit log는 strong + append-only. 도메인마다 그 사다리의 다른 줄에 위치한다. ② **합의가 정말 필요한 자리(이체·결제)와 그렇지 않은 자리(통계·푸시)를 가르는 게 운영 비용을 결정한다.** 모든 데이터에 합의를 강제하면 latency가 무너지고, 모든 데이터에 eventual을 허용하면 audit가 깨진다.

이 결정 패턴이 19장 결제 챕터에서 한 번 더 깊이 다뤄진다. 이 챕터의 사고 도구가 케이스 스터디에서 어떻게 작동하는지 그때 본다.

## 10. 의사결정 트리 — 우리 데이터에 어떤 일관성이 필요한가

여기까지의 어휘를 가지고, 실무에서 한 박자 안에 던질 수 있는 질문 5개를 정리해 두자.

1. **이 데이터가 어긋나면 어떤 손해가 나는가?** 금융·재고 같은 자리는 strong (linearizability·serializable isolation). UI 보여주기·통계는 eventual로 충분.
2. **글로벌 다중 region이 필요한가?** No라면 single-leader RDB로 충분. Yes라면 PACELC를 분명히 정하고 들어가자 — PA/EL이면 multi-leader 또는 leaderless + CRDT, PC/EC이면 Spanner·CockroachDB 계열.
3. **사용자 경험에 필요한 최소 보장은 무엇인가?** read-your-writes·monotonic reads는 약해 보여도 사용자 경험의 바닥이다. session affinity·write-after-read 같은 기본 도구를 챙기자.
4. **데이터 모델을 monotonic하게 설계할 수 있는가?** Yes라면 합의 없이 CRDT로 갈 수 있다. add-only counter, set union, max·min 같은 모양이 monotonic의 후보.
5. **이 결정을 우리 도메인 언어로 설명할 수 있는가?** "Cassandra가 빠르니까"가 아니라 "우리 워크로드는 PA/EL이라 eventual을 허용하지만 read-your-writes는 session affinity로 보장한다"로 말할 수 있는가.

이 다섯 물음을 들고 회의 자리에 가면, 동료의 "strong consistency 필요한가요?" 질문에 첫 5분 안에 답할 수 있다.

## 11. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 분산 합의·복제·일관성이라는 어려운 영역의 지형이 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **FLP impossibility** — 분산 합의는 trade-off의 산물이다. Paxos·Raft·ZAB가 무엇을 양보해서 어떻게 가능하게 만들었는지 알고 도입하자.
- **Raft가 사실상 산업 표준이다.** etcd·Consul·CockroachDB·Kafka KRaft 모두 Raft 위에 있다. Paxos를 외울 필요는 없지만, 그 그림자 안에 있다는 사실은 기억하자.
- **합의 알고리즘 선택보다 layer 수가 더 큰 변수다.** Kafka가 ZooKeeper를 떼어내고 KRaft로 옮긴 결정이 이 진실을 보여 준다.
- **Replication 세 갈래** — single-leader가 90% 시스템의 default. multi-leader·leaderless는 강한 정당화가 있어야 한다.
- **일관성 사다리 6단계** — linearizability → sequential → causal → read-your-writes → monotonic reads → eventual. 우리 데이터가 어느 줄에 있는지 한 박자에 답할 수 있는 어휘다.
- **CAP보다 PACELC가 정직하다.** partition 없는 99% 시간의 latency vs consistency가 진짜 trade-off다. "우리는 PA/EL입니다"라고 답할 수 있는 시스템이 되자 — 그게 새벽 3시의 자신을 살린다.
- **CALM theorem** — coordination-free = monotonic의 동치. CRDT의 이론적 근거이자, 데이터 모델 설계가 운영 비용을 결정한다는 시각.
- **카카오뱅크의 패턴** — 모든 도메인에 같은 일관성을 강제하지 않는다. 정산은 strong, 알림은 eventual. 도메인마다 사다리의 다른 줄을 고르는 게 99.99% SLO의 비결.

다음 장(13장)에서는 샤딩과 파티셔닝을 짚는다. "트래픽 10배가 와도 무너지지 않는 시스템은 무엇을 미리 정해 두었는가" — 이 질문에 답하려면 합의의 자리에서 한 박자 내려와, 데이터를 수평으로 가르는 사고법이 필요하다. 함께 들여다보자.

---

<!-- frontmatter -->
- 챕터 번호: 12 (plan §3 정렬 후, 보안 1부 편입으로 +1 shift)
- 분량 추정: 한국어 약 16,000자 (≈ 22페이지)
- 본문 인용 reference: §3.1 합의(Paxos/Raft/ZAB) · §3.2 일관성 모델 · §7.10 Strong vs Eventual · §7.11 TrueTime vs HLC · §4.12 Spanner, P1·P2·P3·P6·P12·P30·P31 논문 인용, 8장 callback(TrueTime commit wait·Lamport happens-before), 15장 CRDT callback, 19장 결제 callback, 카카오뱅크 W41
- 계획서와 다르게 간 점: 02_plan §3 12장 hook(Spanner 3ms commit wait)이 8장과 겹치므로, 도입부를 "동료의 질문 — strong consistency 필요한가요?"로 변경(02_plan hook의 마지막 한 줄을 살림). 의사결정 트리 5문항을 명시적으로 박은 점이 02_plan보다 한 단계 구체화. Abadi NewSQL 비판은 검증 필요 라벨로 짧게 다룸.
<!-- 개정: 2026-05-16 plan §3 매핑 정렬 (보안 9장 1부 편입으로 챕터 번호 +1 shift). 헤더·"다음 장" 표현·frontmatter 갱신. -->

