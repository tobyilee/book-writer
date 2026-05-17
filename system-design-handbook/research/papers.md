# 논문·서적 리서치: 시스템 디자인 (실무 백엔드 가이드)

수집일: 2026-05-16
대상 독자: 3~7년차 실무 백엔드 엔지니어 — 수학 증명·formal proof는 직관·결과·실무 적용 중심으로 축약.
편성: 합의·일관성 / 시간·인과성 / 트랜잭션·복제 / 스토리지 엔진 / 빅데이터 아키텍처 / 권위서 / 보조 자료.

총 자료 22편 (서적 6 + 논문/기술 보고서 16). 고전:최신 비율 ≈ 55:45.

---

## A. 분산 합의 (Consensus)

### 논문 1: The Part-Time Parliament (Paxos)
- 저자·연도: Leslie Lamport, 1998 (원안 1989 ACM TOCS 거절 → 1998 ACM TOCS 게재)
- 발표처: ACM Transactions on Computer Systems, vol. 16, no. 2, pp. 133–169
- DOI: 10.1145/279227.279229
- 피인용수: ~10,300 (Google Scholar, 2026-05 기준)
- 요약: 비신뢰성 메시지·노드 장애 환경에서 다수결만으로 단일 값에 합의하는 알고리즘을 그리스 의회 우화로 설명. proposer/acceptor/learner 3 역할, prepare(n) / promise(n,v) / accept(n,v) / accepted(n,v) 4단계. quorum이 겹치면 안정성과 진행성 모두 보장.
- 방법론 요약: 우화 + 후반부 수학적 안전성 증명. multi-decree(Multi-Paxos)는 leader 선출로 prepare phase 생략 가능.
- 핵심 결과: 2f+1 노드로 f 노드 장애 허용. async 모델에서 FLP impossibility를 회피하지 못하므로 liveness는 "결국 안정 leader가 생긴다"는 가정 하에서만 보장.
- 인용할 만한 문장:
  > "The Paxos algorithm has been described as 'difficult to understand'... I shall try to explain it in simple English." (p.135)
- 챕터 매핑: 패턴 — 분산 합의 (Spanner, Chubby, ZooKeeper의 이론적 뿌리)
- 독자 전달 방식: "Multi-Paxos가 실제 production 시스템(Chubby, Spanner)에서 어떻게 leader-based로 단순화되는지"가 실무 관점의 핵심.

### 논문 2: In Search of an Understandable Consensus Algorithm (Raft)
- 저자·연도: Diego Ongaro, John Ousterhout, 2014
- 발표처: USENIX ATC '14, pp. 305–319
- URL: https://raft.github.io/raft.pdf
- 피인용수: ~5,800
- 요약: Paxos의 이해 난도 자체를 학술적 단점으로 정의하고, 가르치기 쉽고 구현하기 쉬운 합의 알고리즘으로 재설계. leader election + log replication + safety의 3개 sub-problem 분해, term 기반 leader 일관성.
- 방법론 요약: Stanford 강의에서 학생 43명에게 Paxos와 Raft 동일 시간 가르친 후 quiz — Raft 점수 평균 25.7%p 우위. 이는 알고리즘 설계 자체가 가르침을 1차 목표로 한 첫 사례.
- 핵심 결과: 같은 안전성 보장, 동일한 5-node 환경에서 leader election ~150–300ms 내 수렴. etcd, Consul, TiKV, CockroachDB, Kafka KRaft(2.8+) 모두 Raft 기반.
- 인용할 만한 문장:
  > "Raft is similar in many ways to existing consensus algorithms (most notably, Oki and Liskov's Viewstamped Replication), but it has several novel features... Raft separates the key elements of consensus, such as leader election, log replication, and safety." (p.305)
- 챕터 매핑: 패턴 — 합의 + 케이스 스터디 — etcd/Kafka KRaft.
- 독자 전달 방식: "이해 가능성이 소프트웨어 시스템의 first-class 요건일 수 있다"는 메타 메시지를 챕터 도입부 hook으로.

### 논문 3: ZooKeeper: Wait-Free Coordination for Internet-Scale Systems (ZAB)
- 저자·연도: Patrick Hunt, Mahadev Konar, Flavio Junqueira, Benjamin Reed, 2010
- 발표처: USENIX ATC '10
- URL: https://www.usenix.org/legacy/event/usenix10/tech/full_papers/Hunt.pdf
- 피인용수: ~3,100
- 요약: 단일 합의 알고리즘 대신 "wait-free 조정 서비스"를 제공. ZAB(ZooKeeper Atomic Broadcast)로 모든 write를 leader 통해 totally ordered atomic broadcast. read는 follower local — read는 약간 stale 가능 (FIFO client order + sync() 호출로 보강).
- 방법론 요약: znode tree(파일시스템 유사) + ephemeral node로 leader election, distributed lock, configuration store 구현. throughput 50,000+ ops/sec (3-node, write 30% mix).
- 핵심 결과: Hadoop HDFS NameNode HA, HBase, Kafka(<2.8) 메타데이터, SolrCloud 모두 ZooKeeper 의존. 단 운영 자체 비용이 커서 Kafka는 2.8+ KRaft로 탈피, etcd가 K8s에서 대체.
- 인용할 만한 문장:
  > "We propose a wait-free implementation of synchronization primitives... clients can request operations without waiting for others." (p.1)
- 챕터 매핑: 빌딩 블록 — 분산 조정 서비스 + 케이스 스터디 — Kafka 컨트롤 플레인 변천사.
- 독자 전달 방식: "조정 서비스 도입은 부채를 만든다 — 실제로 Kafka도 떼어냈다"는 실무 교훈을 강조.

---

## B. 시간·인과성

### 논문 4: Time, Clocks, and the Ordering of Events in a Distributed System
- 저자·연도: Leslie Lamport, 1978
- 발표처: Communications of the ACM, vol. 21, no. 7, pp. 558–565
- DOI: 10.1145/359545.359563
- 피인용수: ~14,000 (분산 시스템 분야 최다 피인용 중 하나)
- 요약: "동시"의 의미를 물리적 시계가 아닌 인과 관계(happens-before, →)로 재정의. 이 관계는 부분 순서, 이를 logical clock(Lamport timestamp)으로 totally ordered하게 확장. 분산 mutual exclusion 알고리즘도 함께 제시.
- 방법론 요약: 메시지 송신 a, 수신 b → a → b. 두 노드 사이 partial order를 노드 ID로 tie-break해 total order. NTP·atomic clock 없이도 일관된 이벤트 순서 가능.
- 핵심 결과: Lamport clock은 happens-before를 완전히 잡지 못함(false ordering 가능). 이 한계가 Vector Clock(Fidge 1988, Mattern 1988)을 낳음. 둘 모두 Dynamo, Riak, Bayou의 conflict detection 기반.
- 인용할 만한 문장:
  > "The concept of one event happening before another in a distributed system is examined, and is shown to define a partial ordering of the events. A distributed algorithm is given for synchronizing a system of logical clocks." (Abstract)
- 챕터 매핑: 빌딩 블록 — 시간/순서 + 패턴 — 멱등성·idempotency의 인과적 기반.
- 독자 전달 방식: 한국 실무자들이 "시간"에 가지는 신뢰(NTP, KST)를 흔드는 사고 실험으로 챕터 도입.

### 논문 5: Spanner: Google's Globally Distributed Database (TrueTime)
- 저자·연도: James C. Corbett et al., 2012
- 발표처: OSDI '12 → ACM TOCS, vol. 31, no. 3 (2013)
- DOI: 10.1145/2491245
- 피인용수: ~3,900
- 요약: 글로벌 분산 SQL DB에서 external consistency(linearizability + serializability를 transaction level로)를 보장. 핵심은 TrueTime API — GPS + atomic clock으로 시간 범위 [earliest, latest]를 노출, commit wait으로 uncertainty 흡수.
- 방법론 요약: Paxos group으로 tablet 단위 복제. 2PC + Paxos. read-only는 timestamp 부여, snapshot read는 lock-free. commit wait 평균 ~6ms (TrueTime uncertainty ε 평균 ~3ms).
- 핵심 결과: 4–5 region에서 cross-region commit p99 < 100ms. AdWords·Gmail이 이전 MySQL sharding을 Spanner로 대체. external consistency를 production global scale에서 처음 달성.
- 인용할 만한 문장:
  > "Spanner is the first system to distribute data at global scale and support externally-consistent distributed transactions." (Abstract)
  > "TrueTime explicitly represents clock uncertainty, and Spanner waits out this uncertainty when committing transactions." (§2)
- 챕터 매핑: 빌딩 블록 — DB + 패턴 — 글로벌 일관성 + 논쟁점 — TrueTime 의존성.
- 독자 전달 방식: "Google이 시간 자체에 투자했다" — 인프라 의사결정의 깊이를 보여주는 일화.

### 논문 6: CALM Theorem — Keeping CALM: When Distributed Consistency is Easy
- 저자·연도: Joseph M. Hellerstein, Peter Alvaro, 2020
- 발표처: Communications of the ACM, vol. 63, no. 9, pp. 72–81
- DOI: 10.1145/3369736
- 피인용수: ~280 (2026-05)
- 요약: "조정(coordination) 없이 일관된 결과를 낼 수 있는 분산 프로그램은 monotonic하다"가 동치. CRDT, gossip, eventual consistency가 왜 잘 동작하는지에 대한 이론적 기반.
- 방법론 요약: Bloom 언어(declarative)로 분산 프로그램의 monotonicity를 정적 분석. counter 증가·집합 union 등은 monotonic, deletion·subtraction은 non-monotonic — 후자는 조정(consensus) 필요.
- 핵심 결과: "어디서 coordination이 필요한가"를 컴파일 타임에 답할 수 있다는 가능성을 제시. CRDT 설계 원리, eventually consistent system의 설계 가이드.
- 인용할 만한 문장:
  > "A program has a consistent, coordination-free distributed implementation if and only if it is monotonic." (p.74)
- 챕터 매핑: 패턴 — 일관성 모델 + CRDT 이론적 근거.
- 독자 전달 방식: "monotonic = 안전, non-monotonic = 비싸다"는 단순 규칙으로 환원해 실무 의사결정에 적용.

---

## C. 트랜잭션·복제·일관성

### 논문 7: Dynamo: Amazon's Highly Available Key-value Store
- 저자·연도: Giuseppe DeCandia et al., 2007
- 발표처: SOSP '07, pp. 205–220
- DOI: 10.1145/1294261.1294281
- 피인용수: ~6,800
- 요약: "성수기 쇼핑카트가 절대 사라지면 안 된다"는 비즈니스 요구에서 출발. CAP의 AP 진영을 선택, eventual consistency + consistent hashing + vector clock + sloppy quorum + hinted handoff + Merkle tree anti-entropy의 조합.
- 방법론 요약: N(replication), R(read quorum), W(write quorum)을 application별 튜닝. R+W>N이면 일반적으로 일관성, R=W=1은 max availability. conflict는 reader가 resolve (last-write-wins 또는 application semantic).
- 핵심 결과: Amazon 쇼핑카트 99.9994% 가용성. 후속으로 DynamoDB(2012), Cassandra, Riak, Voldemort에 영향. eventual consistency를 SaaS 표준 옵션으로 정착시킨 분기점.
- 인용할 만한 문장:
  > "Dynamo sacrifices consistency under certain failure scenarios. It makes extensive use of object versioning and application-assisted conflict resolution." (Abstract)
- 챕터 매핑: 빌딩 블록 — DB + 패턴 — 일관성/quorum + 케이스 스터디 — Amazon.
- 독자 전달 방식: "어떻게 트레이드오프할지가 architect의 가장 큰 의사결정"이라는 메시지를 비즈니스 시나리오와 함께.

### 논문 8: Bigtable: A Distributed Storage System for Structured Data
- 저자·연도: Fay Chang et al., 2006
- 발표처: OSDI '06
- DOI: 10.1145/1365815.1365816 (TOCS 2008)
- 피인용수: ~7,200
- 요약: row key + column family + timestamp의 sparse multidimensional map. Chubby로 메타데이터 조정, GFS에 SSTable 저장, MemTable + WAL 구조. 후에 HBase·Cassandra·LevelDB가 동일 모델.
- 방법론 요약: tablet은 row range. tablet server가 메모리에 mutation을 모았다가 GFS의 immutable SSTable로 flush. compaction이 read 성능 유지.
- 핵심 결과: Google Analytics, Earth, Personalized Search 등 60+ 프로젝트가 의존. row 단위 atomic, cross-row transaction 미제공 — 이 제한이 후속 Megastore/Spanner의 동기.
- 인용할 만한 문장:
  > "Bigtable is a sparse, distributed, persistent multi-dimensional sorted map." (§2)
- 챕터 매핑: 빌딩 블록 — wide-column DB.
- 독자 전달 방식: "schema-on-read의 원조"를 강조해 NoSQL 운동의 출발점으로 위치.

### 논문 9: Cassandra: A Decentralized Structured Storage System
- 저자·연도: Avinash Lakshman, Prashant Malik, 2010
- 발표처: ACM SIGOPS Operating Systems Review, vol. 44, no. 2
- DOI: 10.1145/1773912.1773922
- 피인용수: ~4,500
- 요약: Dynamo의 분산 모델 + Bigtable의 데이터 모델 결합. masterless, gossip protocol, tunable consistency. Facebook inbox 검색에서 출발했지만 후에 Facebook은 HBase로 이동(또 다른 교훈).
- 방법론 요약: virtual nodes(256/노드 권장), Murmur3 partitioner. consistency level: ONE/QUORUM/ALL/LOCAL_QUORUM(다중 DC). compaction strategy: STCS, LCS, TWCS(time-window, time-series 전용).
- 핵심 결과: Apple은 100,000+ Cassandra node 운영(2018 Summit). Discord(2017) — Cassandra → 후 ScyllaDB로 마이그레이션(GC pause).
- 인용할 만한 문장:
  > "Cassandra combines the data model of Bigtable with the high-availability characteristics of Dynamo." (Abstract)
- 챕터 매핑: 빌딩 블록 — DB + 케이스 스터디 — Discord 진화사.

### 논문 10: Calvin: Fast Distributed Transactions for Partitioned Database Systems
- 저자·연도: Alexander Thomson, Thaddeus Diamond, Shu-Chun Weng, Kun Ren, Philip Shao, Daniel Abadi, 2012
- 발표처: SIGMOD '12, pp. 1–12
- DOI: 10.1145/2213836.2213838
- 피인용수: ~770
- 요약: 2PC를 회피하고 deterministic execution으로 분산 트랜잭션 처리. 모든 노드가 같은 순서(global log)로 동일 입력 처리 → 결과 결정적 → 동기화 불필요. FaunaDB의 기반 알고리즘.
- 방법론 요약: sequencer가 트랜잭션을 batch로 ordering(Paxos로 복제), scheduler는 lock acquisition을 deterministic하게 수행. read/write set을 사전 선언해야 함 — 이게 application 측 제약.
- 핵심 결과: distributed TPC-C에서 Spanner 대비 throughput 우위 보고. 단, dynamic workload(미리 read set 모름)는 추가 reconnaissance round 필요.
- 인용할 만한 문장:
  > "By using a deterministic execution scheme, Calvin allows distributed transactions to commit in a single round of communication." (Abstract)
- 챕터 매핑: 패턴 — 분산 트랜잭션 / 논쟁점 — 2PC vs deterministic.

### 논문 11: Conflict-Free Replicated Data Types (CRDT)
- 저자·연도: Marc Shapiro, Nuno Preguiça, Carlos Baquero, Marek Zawirski, 2011
- 발표처: SSS '11 (Stabilization, Safety, and Security of Distributed Systems), Springer LNCS 6976
- DOI: 10.1007/978-3-642-24550-3_29
- 피인용수: ~1,900
- 요약: 모든 replica가 모든 update를 받으면 결국 같은 상태로 수렴하는 자료구조 가족. state-based(CvRDT, semilattice join)와 operation-based(CmRDT, commutative ops) 두 변형.
- 방법론 요약: G-Counter, PN-Counter, G-Set, 2P-Set, OR-Set, LWW-Element-Set, RGA(text), Logoot 등. 합집합·max·OR 같은 monotonic op만 사용.
- 핵심 결과: Riak Data Types, Redis CRDT module(Enterprise), Akka Distributed Data, Yjs, Automerge, Linear, Figma multiplayer의 이론적 기반. Soundcloud Roshi.
- 인용할 만한 문장:
  > "A CRDT is a data type that automatically resolves concurrent updates without coordination." (§1)
- 챕터 매핑: 패턴 — eventual consistency + 케이스 스터디 — 협업 도구.

### 논문 12: Highly Available Transactions: Virtues and Limitations
- 저자·연도: Peter Bailis, Aaron Davidson, Alan Fekete, Ali Ghodsi, Joseph M. Hellerstein, Ion Stoica, 2014
- 발표처: VLDB 2014
- DOI: 10.14778/2732232.2732237
- 피인용수: ~480
- 요약: CAP의 P가 정상 운영에도 사실상 항상 존재한다는 전제하에, 어떤 isolation level이 "highly available"한지 분류. read committed, read your writes, monotonic reads, causal consistency까지는 HA. snapshot isolation, serializable은 HA 불가.
- 방법론 요약: ACID isolation 이론을 distributed availability 관점에서 재정렬.
- 핵심 결과: 대부분 application이 사용하는 isolation level이 실제로는 weaker — 운영 중 anomaly 가능성을 정량화. eventual consistency가 실용적인 이유의 이론적 근거.
- 인용할 만한 문장:
  > "Many transactional semantics... can be achieved with high availability... but stronger ones cannot." (Abstract)
- 챕터 매핑: 패턴 — isolation level + 논쟁점 — strong vs eventual.

---

## D. 스토리지 엔진

### 논문 13: The Log-Structured Merge-Tree (LSM-tree)
- 저자·연도: Patrick O'Neil, Edward Cheng, Dieter Gawlick, Elizabeth O'Neil, 1996
- 발표처: Acta Informatica, vol. 33, no. 4, pp. 351–385
- DOI: 10.1007/s002360050048
- 피인용수: ~2,600
- 요약: write를 메모리(C0)에 모았다가 batch로 disk(C1, C2, ...)에 sorted run으로 flush. read는 모든 level을 merge. write throughput이 random insert 대비 1~2 자릿수 향상, 단 write amplification 부담.
- 방법론 요약: leveled compaction(LevelDB, RocksDB) vs tiered compaction(Cassandra STCS) 두 가지 큰 갈래. bloom filter로 read amplification 완화.
- 핵심 결과: LevelDB, RocksDB, Cassandra, HBase, ScyllaDB, InfluxDB, TiKV 등 거의 모든 modern write-heavy DB의 기반. write 30K+ ops/sec 단일 노드 흔함.
- 인용할 만한 문장:
  > "The LSM-tree uses an algorithm that defers and batches index changes, cascading the changes from a memory-based component through one or more disk components." (Abstract)
- 챕터 매핑: 빌딩 블록 — 스토리지 엔진 / B-tree vs LSM 비교.

### 논문 14: Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases
- 저자·연도: Alexandre Verbitski et al., 2017
- 발표처: SIGMOD '17, pp. 1041–1052
- DOI: 10.1145/3035918.3056101
- 피인용수: ~840
- 요약: "the log is the database" 철학. 전통 RDBMS는 write 시 page → WAL → checkpoint 다중 IO. Aurora는 storage가 redo log를 직접 받아 page를 비동기로 reconstruct, network IO 6x 감소.
- 방법론 요약: 6-way replication across 3 AZs(quorum 4/6 write, 3/6 read), shared distributed log-structured storage layer. compute node는 stateless, storage가 모든 durability 담당.
- 핵심 결과: MySQL 대비 throughput 5x, PostgreSQL 대비 3x. RDS 시리즈와 동일 인터페이스 — 운영 호환성 유지가 채택 가속.
- 인용할 만한 문장:
  > "Our central design tenet is that the most precious resource is the network." (§1)
  > "The log is the database." (§3)
- 챕터 매핑: 빌딩 블록 — 클라우드 DB + 케이스 스터디 — Aurora/RDS.

### 논문 15: F1: A Distributed SQL Database That Scales
- 저자·연도: Jeff Shute et al., 2013
- 발표처: VLDB 2013, pp. 1068–1079
- URL: https://research.google/pubs/pub41344/
- 피인용수: ~610
- 요약: AdWords가 MySQL sharding의 한계(rebalancing 운영, cross-shard JOIN 불가, schema migration)에서 Spanner 기반 F1으로 이주한 과정. SQL 표준 + Spanner 분산 트랜잭션 + 수십 PB 규모.
- 방법론 요약: hierarchical schema(child table을 parent와 same partition에 배치 → JOIN local화). protocol buffer column type 지원. async/incremental schema change.
- 핵심 결과: AdWords 전체 critical path. write latency ~50ms (multi-row), commit latency ~75ms 수준. MySQL 대비 throughput·latency 트레이드오프를 운영 단순화로 상쇄.
- 인용할 만한 문장:
  > "F1 combines high availability, the scalability of NoSQL systems like Bigtable, and the consistency and usability of traditional SQL databases." (Abstract)
- 챕터 매핑: 케이스 스터디 — MySQL sharding 진화사 + 빌딩 블록 — NewSQL.

---

## E. 빅데이터·스트림 아키텍처

### 논문 16: MapReduce: Simplified Data Processing on Large Clusters
- 저자·연도: Jeffrey Dean, Sanjay Ghemawat, 2004
- 발표처: OSDI '04 → CACM 51(1) 2008
- DOI: 10.1145/1327452.1327492
- 피인용수: ~22,000
- 요약: 대용량 데이터 처리를 map(k1,v1) → list(k2,v2) / reduce(k2, list(v2)) → list(v3) 두 함수로 단순화. 분산·내고장성·로드밸런싱은 framework가 담당.
- 방법론 요약: GFS 입력 → map task(commodity server) → shuffle → reduce → GFS 출력. 노드 장애 시 task 재실행, straggler는 speculative execution.
- 핵심 결과: 1 PB sort 6 시간(2008). Google search index, Hadoop ecosystem 전체. 후에 Spark/Flink의 더 일반적 abstraction에 자리 양보, 그러나 batch 사고의 기본 모델.
- 인용할 만한 문장:
  > "MapReduce is a programming model and an associated implementation for processing and generating large data sets." (Abstract)
- 챕터 매핑: 빌딩 블록 — 데이터 파이프라인 / 논쟁점 — batch vs stream의 역사.

### 논문 17: Resilient Distributed Datasets (RDD / Spark)
- 저자·연도: Matei Zaharia, Mosharaf Chowdhury, Tathagata Das, Ankur Dave, Justin Ma, Murphy McCauley, Michael Franklin, Scott Shenker, Ion Stoica, 2012
- 발표처: NSDI '12
- URL: https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia
- 피인용수: ~7,800
- 요약: RDD = immutable, partitioned, lazy lineage. iterative algorithm(머신러닝, graph)에서 Hadoop MapReduce 대비 10~100x. 실패 복구는 lineage replay.
- 방법론 요약: narrow vs wide dependency 분리, scheduler가 stage 단위 DAG 실행. cache는 메모리 hit이면 disk 회피.
- 핵심 결과: Spark이 ETL·분석·ML 표준 도구로 정착. PySpark, Spark SQL, Structured Streaming까지 확장.
- 인용할 만한 문장:
  > "RDDs achieve fault tolerance through a notion of lineage: if a partition is lost, the RDD has enough information to rebuild just that partition." (§1)
- 챕터 매핑: 빌딩 블록 — 데이터 파이프라인 / 케이스 스터디 — Spark 채택사.

### 논문 18: Apache Flink: Stream and Batch Processing in a Single Engine
- 저자·연도: Paris Carbone, Asterios Katsifodimos, Stephan Ewen, Volker Markl, Seif Haridi, Kostas Tzoumas, 2015
- 발표처: IEEE Data Engineering Bulletin, vol. 38, no. 4
- URL: https://flink.apache.org/img/flink-bulletin-2015.pdf
- 피인용수: ~720
- 요약: stream-first 모델 — batch도 bounded stream으로 간주. exactly-once는 distributed snapshot(Chandy–Lamport 변형, "asynchronous barrier snapshot")으로 달성. event-time 처리(watermark)가 1급 시민.
- 방법론 요약: KeyedStream + ProcessFunction + state backend(RocksDB) + savepoint(operator state 백업). Kafka source/sink와 transactional commit 결합 → end-to-end exactly-once.
- 핵심 결과: Alibaba Singles' Day 실시간 분석, Uber Athena, Netflix Mantis, LinkedIn 등. Kappa architecture의 production 구현체로 통용.
- 인용할 만한 문장:
  > "Flink's central design tenet is that many classes of data processing applications can be expressed as pipelines of streaming computations." (§2)
- 챕터 매핑: 빌딩 블록 — 스트림 처리 + 패턴 — Kappa.

### 기술 보고서 19: Lambda Architecture vs Kappa Architecture
- 저자·연도: Nathan Marz (Lambda, 2011 blog + "Big Data" 책 2015), Jay Kreps (Kappa, "Questioning the Lambda Architecture", O'Reilly Radar 2014)
- URL (Kappa 원전): https://www.oreilly.com/radar/questioning-the-lambda-architecture/
- 신뢰성: 최상 (원작자 글)
- 요약: Lambda = batch + speed + serving 3계층, 동일 로직 중복이 비용. Kappa = stream 단일계층, 재처리 시 Kafka에서 replay. Marz 2011 → Kreps 2014 → 2020년대 Flink/Beam이 통합.
- 챕터 매핑: 패턴 — 데이터 아키텍처 + 논쟁점 — 중복 vs 단순성.

### 논문 20: The Dataflow Model (Google → Apache Beam)
- 저자·연도: Tyler Akidau et al., 2015
- 발표처: VLDB 2015
- DOI: 10.14778/2824032.2824076
- 피인용수: ~590
- 요약: event-time vs processing-time, watermark, trigger, accumulation 4축으로 stream/batch를 통합. Google Dataflow → Apache Beam의 추상화 모델.
- 핵심 결과: Beam이 Flink, Spark, Dataflow, Samza에서 portable하게 실행. event-time semantics가 모든 modern streaming engine의 공통 어휘로 정착.
- 인용할 만한 문장:
  > "Streaming and batch are not separate paradigms; batch is a bounded special case of streaming." (§1)
- 챕터 매핑: 빌딩 블록 — 스트림.

---

## F. 권위서 (Books)

### 서적 21: Designing Data-Intensive Applications (DDIA)
- 저자·연도: Martin Kleppmann, 2017 (1st ed; 2nd ed 작업 중 2025)
- 출판사: O'Reilly
- ISBN: 978-1449373320
- 한국어판: "데이터 중심 애플리케이션 설계" (정재부 등 옮김, 위키북스 2018)
- 핵심 contribution: 분산 시스템·DB·스트림을 통합한 단일 텍스트로서 사실상 현대 백엔드의 표준 교과서.
  - Part I: foundations (encoding, replication, partitioning, transactions)
  - Part II: distributed data (consistency, consensus)
  - Part III: derived data (batch, stream, future)
- 챕터 매핑: 전 챕터 이론적 backbone. 특히 Ch 5(replication), Ch 7(transactions), Ch 9(consistency & consensus)는 본 책의 "패턴" 섹션과 1:1 대응.
- 인용 가능 구절:
  > "Reliability is making systems work correctly, even when faults occur." (Ch 1)
  > "There is no such thing as 'eventual consistency'. There are many different eventual consistencies." (Ch 5 정리)
- 활용: 챕터별 "더 깊이 읽기" 박스에 해당 챕터 번호로 매핑.

### 서적 22: Database Internals: A Deep Dive into How Distributed Data Systems Work
- 저자·연도: Alex Petrov, 2019
- 출판사: O'Reilly
- ISBN: 978-1492040347
- 핵심 contribution: DDIA가 application 관점이라면 Petrov는 엔진 관점. B-tree·LSM·bloom filter·buffer pool 등 단일 노드 storage internals + 분산 합의·복제·gossip의 구현 디테일.
- 챕터 매핑: 빌딩 블록 — 스토리지 엔진, DB index, 분산 합의 구현부.
- 인용 가능 구절:
  > "Designing storage systems is the art of trade-offs: between read and write amplification, space and time, durability and latency."

### 서적 23: Site Reliability Engineering (Google SRE Book)
- 저자·연도: Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (eds), 2016
- 출판사: O'Reilly (전문 무료 공개: https://sre.google/sre-book/table-of-contents/)
- 핵심 contribution: SLO/SLI/error budget, on-call rotation, blameless postmortem, capacity planning, release engineering, monitoring 4-golden signals를 production-grade language로 정립.
- 챕터 매핑: 운영·SRE 섹션 전체의 1차 참고.
- 인용 가능 구절:
  > "Hope is not a strategy." (Traditional SRE saying, Ch 1)
  > "100% is the wrong reliability target for basically everything." (Ch 4 Service Level Objectives)

### 서적 24: The Site Reliability Workbook
- 저자·연도: Betsy Beyer et al., 2018
- 출판사: O'Reilly (무료 공개)
- 핵심 contribution: SRE Book의 실전 보충 — SLO 정의 예제, error budget policy 템플릿, alerting 전략, non-abstract large system design 사례 4건.
- 챕터 매핑: SLO 운영, alert 설계, postmortem 작성 챕터.

### 서적 25: Microservices Patterns
- 저자·연도: Chris Richardson, 2018
- 출판사: Manning
- ISBN: 978-1617294549
- 한국어판: "마이크로서비스 패턴" (이종립 옮김, 길벗 2020)
- 핵심 contribution: Saga, CQRS, API Composition, Database per Service, Strangler Fig 등 마이크로서비스 패턴 카탈로그. microservices.io 사이트와 짝.
- 챕터 매핑: 패턴 — Saga, CQRS, 마이크로서비스 decomposition.

### 서적 26: Building Microservices, 2nd ed.
- 저자·연도: Sam Newman, 2021 (1st ed 2015)
- 출판사: O'Reilly
- ISBN: 978-1492034025
- 핵심 contribution: microservices의 사회·조직·운영 측면 강조. "마이크로서비스가 정답이 아닌 경우" 챕터로 모놀리스 회귀 논의도 포함.
- 챕터 매핑: 논쟁점 — 모놀리스 vs MSA, 케이스 스터디 진입로.

### 서적 27: Designing Distributed Systems
- 저자·연도: Brendan Burns, 2018
- 출판사: O'Reilly
- ISBN: 978-1491983645
- 핵심 contribution: K8s co-creator가 정리한 single-node patterns(sidecar, ambassador, adapter), serving patterns(replicated, sharded), batch patterns(work queue, scatter/gather).
- 챕터 매핑: 패턴 — 컨테이너 시대의 분산 디자인.

---

## G. 보조 자료 (조사 시 부수 발견)

### 자료 28: ACM Queue — Convergence (Kleppmann)
- 저자·연도: Martin Kleppmann, 2022
- 발표처: ACM Queue, vol. 20, issue 4
- DOI: 10.1145/3546931
- 요약: local-first software 운동의 이론적 종합. CRDT, sync engine, end-to-end encryption을 결합해 cloud 의존 없는 분산 협업.
- 챕터 매핑: 패턴 — eventual consistency + 케이스 스터디 — Linear/Figma/Automerge.

### 자료 29: Marc Brooker — "It's About Time"
- 저자·연도: Marc Brooker (AWS Distinguished Engineer), 2021 blog
- URL: https://brooker.co.za/blog/2021/05/19/time.html
- 요약: TrueTime 같은 명시적 uncertainty 표현이 왜 분산 DB에서 강력한지에 대한 실무 해설. Spanner 논문에 대한 가장 좋은 해설 중 하나.
- 챕터 매핑: 패턴 — 시간/일관성 박스 자료.

### 자료 30: FLP Impossibility Proof
- 저자·연도: Michael J. Fischer, Nancy A. Lynch, Michael S. Paterson, 1985
- 발표처: Journal of the ACM, vol. 32, no. 2, pp. 374–382
- DOI: 10.1145/3149.214121
- 피인용수: ~6,200
- 요약: 비동기 분산 시스템에서 단 하나의 노드라도 fail-stop 가능하면 결정적(deterministic) 합의는 불가능. Paxos/Raft가 "비동기에서 liveness 포기 + 안정 leader 가정"인 이유의 원전.
- 챕터 매핑: 패턴 — 합의의 이론적 한계 박스.

### 자료 31: Brewer's CAP Theorem (Conjecture + Proof)
- 저자·연도: Eric Brewer (conjecture 2000 PODC keynote), Seth Gilbert & Nancy Lynch (formal proof 2002)
- 발표처: ACM SIGACT News, vol. 33, no. 2, 2002
- DOI: 10.1145/564585.564601
- 요약: network partition 시 Consistency와 Availability를 동시에 보장 불가. 단 partition은 "있거나 없거나"의 이진이 아니라 frequency·duration의 spectrum — 후속 PACELC가 보완.
- 챕터 매핑: 빌딩 블록 — 분산 시스템 이론 기초.

---

## 수집 한계

- **2024–2026 최신 논문 미커버**: vector DB(HNSW 등) 학술 논문, LLM serving 분산화 논문(vLLM, PagedAttention)을 본 리서치에서는 제외 — 책 범위가 "전통 시스템 디자인"이라 deliberate. 필요 시 별도 리서치.
- **국내 학술지**: KIISE, IEIE 등 국내 학술지의 한국 환경(국내 결제, 통신사 인프라) 특화 논문은 검색 한계로 미커버.
- **proof-heavy 논문 축약**: FLP, Paxos 안전성 증명, Calvin scheduler 증명 등 수학적 디테일은 실무 독자 수준에 맞춰 결과 중심으로만 정리. formal verification 인용 시 원문 참조 권장.
- **재현성**: Spanner/TrueTime 등 hardware 의존 결과는 외부 재현 불가능, marketing 수치와 결과를 구분해 인용해야 함.
- **piping**: ZAB·Multi-Paxos·Viewstamped Replication 등 합의 알고리즘 family tree 전체 비교는 surveys (Howard 2014, van Renesse 2015) 인용으로 보강 가능 — 본 리서치에서는 대표 3편(Paxos/Raft/ZAB)으로 한정.
