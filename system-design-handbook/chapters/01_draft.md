# 1장. 관계형 DB — 시스템의 backbone을 다시 보기

어제 50ms이던 쿼리가 오늘 5초가 되는 경험을 안 해 본 백엔드 개발자가 있을까? 새벽에 alert가 울려 들어왔는데, slow query log를 펴 보니 어제와 같은 쿼리다. 인덱스가 빠진 것도 아니고, 코드가 바뀐 것도 아닌데 plan이 통째로 달라져 있다. 사람을 가장 난감하게 만드는 종류의 장애다.

이런 경험은 흔하다. 토스 SLASH 23의 결제 DB 디버깅 발표를 보고 OKKY에 올라온 첫 댓글이 "통계 정보 갱신 안 된 게 진짜 자주 발생함"이었다. r/PostgreSQL에는 한 달 평균 5건쯤 "어제는 50ms, 오늘은 5초" 토픽이 올라온다. Cloudflare가 사내 블로그에 "We debugged a slow query for 3 days"를 시리즈로 연재하는 이유도 같다. 그러니까 이 장면이 우리만의 무능이 아니라는 점부터 합의하고 시작하자. 관계형 DB는 우리가 가장 오래 써온 부품인데도, 가장 자주 우리를 배신한다.

그러니 배신의 자리에서 시작해보자. Postgres와 MySQL을 10년 써왔다는 사람이 어제 빠르던 쿼리가 오늘 5초 걸리는 이유를 5분 안에 후보 3개로 좁힐 수 있는가. 이 질문에 답할 수 있어야 비로소 "RDB를 안다"고 말할 수 있다.

## 왜 아직도 RDB가 90%인가

먼저 던져야 할 질문이 있다. NoSQL이 등장한 지 15년, NewSQL이 등장한 지 10년이 넘었는데도 왜 새로 시작하는 시스템의 절대다수는 여전히 Postgres나 MySQL부터 켜는가?

HN에서 "Just use Postgres"라는 글이 1,500+ 추천을 받는 이유는 단순하다 (커뮤니티 휴리스틱 3). Simon Willison과 Will Larson을 비롯해 권위자 다수가 같은 말을 한다.

> Postgres can be your queue (LISTEN/NOTIFY, SKIP LOCKED), your full-text search (tsvector), your time-series (Timescale), your JSON store (jsonb), your vector DB (pgvector), and your relational DB. Start there.

이 말을 처음 들으면 과한 농담처럼 느껴진다. 하지만 차분히 곱씹어보면 농담이 아니다. 작은 팀이 시스템을 만든다고 해보자. 큐를 따로 띄우고, 검색을 따로 운영하고, JSON store를 따로 박는 비용을 한 번에 다 치를 여력이 없다. Postgres 하나로 시작해서, 트래픽이 정말로 그 부품의 한계를 넘었을 때 그제서야 분리하는 편이 낫다. 처음부터 Kafka를 쓰고, Elasticsearch를 박고, MongoDB를 곁들이는 시스템은 트래픽이 오기도 전에 운영자가 먼저 지친다.

물론 한계는 분명히 있다. 검색은 한국어 형태소 분석이 들어가는 순간 Elasticsearch가 답이고(5장에서 살펴보자), 시계열은 InfluxDB가, 채팅 메시지처럼 한 사용자당 수십만 row가 쌓이는 곳은 NoSQL이 답이다(2장). 그러나 그 한계가 오기 전까지, 우리는 RDB가 줄 수 있는 것을 다 받아 쓰는 편이 낫다. 그 이유를 한 줄로 줄이면 이렇다. **schema, SQL, ACID, 그리고 30년 누적된 운영 도구다.** 이것을 다른 부품으로 갈아끼우는 일은 생각보다 비싸다 — r/ExperiencedDevs의 한 댓글이 가장 정확하다.

> We changed our cache, our queue, our auth — all 'easy'. We changed our primary DB — it took 18 months.

기억해두자. 캐시·큐·인증은 갈아끼울 수 있어도 primary DB는 마지막에 바꾸는 부품이다. 그래서 처음 결정을 잘 해야 하고, 그래서 우리가 이 책의 1장을 RDB에 쓰는 것이다.

## B+ tree — 인덱스가 정말로 무엇을 약속하는가

"인덱스 추가하면 빠른 거 아닌가요?"라는 질문은 가장 흔하면서 가장 위험하다. 인덱스가 무엇이고 왜 빠른지를 모르고 추가하기 시작하면, 어느 순간 인덱스가 16개쯤 박혀 있는 테이블이 만들어진다. write가 느려지고, plan이 자꾸 잘못된 인덱스를 골라잡고, 디스크는 데이터보다 인덱스가 더 큰 상태가 된다. 끔찍한 일이다.

그러니 인덱스가 정확히 무엇을 약속하는지부터 짚고 가자. 대부분의 RDB가 쓰는 인덱스 구조는 **B+ tree**다. *Database Internals*(P22)이 가장 간결하게 정리한다.

> B+ tree는 정렬된 key를 leaf node에 doubly linked list로 연결한다. internal node는 routing만 한다. leaf 사이의 link 덕분에 range scan이 한 번의 traversal로 끝난다. (Petrov, *Database Internals*)

이 한 문장에 인덱스의 약속이 다 들어 있다. B+ tree는 두 가지를 약속한다.

1. **점 조회는 log N**: `WHERE id = 12345`는 root에서 leaf까지 trace 한 번. 100억 row여도 30번 정도의 노드 traverse면 끝난다.
2. **범위 조회는 log N + scan 길이**: `WHERE id BETWEEN 1000 AND 2000`은 시작점만 찾으면 leaf 사이의 link로 1000개를 줄줄이 읽으면 된다.

여기까지가 우리가 평소 떠올리는 인덱스의 효용이다. 그렇다면 왜 인덱스가 있는데도 plan이 안 타는 일이 생기는가? 왜 "어제는 50ms, 오늘은 5초"가 되는가?

B+ tree의 성질이 깨지는 순간이 따로 있기 때문이다. 한 가지씩 살펴보자.

### 함정 1. composite index 순서

`(user_id, created_at)`으로 묶인 인덱스가 있다고 해보자. 그런데 쿼리가 `WHERE created_at > '2026-01-01'`만 걸려 있다면, 이 인덱스는 안 탄다. B+ tree는 정렬이다. `user_id`로 먼저 정렬되고, 같은 `user_id` 안에서 `created_at`으로 정렬된다. `created_at` 단독으로는 정렬이 안 돼 있으니, full scan 외에 다른 방법이 없다.

이걸 처음 만나면 어이가 없다. "분명 created_at에 인덱스가 있다고 떴는데?" 그래서 composite의 첫 컬럼이 왜 중요한지를 한 번 강하게 박아두자. **첫 컬럼이 WHERE 절에 등호 또는 IN으로 등장하지 않으면, 그 인덱스는 안 탄다.** Markus Winand의 *Use The Index, Luke!*가 한 페이지 전체를 이 주제에 쓰는 이유다.

### 함정 2. implicit type conversion

`phone_number`가 `VARCHAR`인데 `WHERE phone_number = 01012345678`로 쿼리를 날리면 어떻게 될까? 옵티마이저는 모든 row의 `phone_number`를 숫자로 변환해서 비교한다. 인덱스는 정렬된 문자열의 트리인데, 우리가 비교하는 값은 정수다. 정렬 순서가 일치하지 않으니 full scan이다.

이런 일은 ORM이 type을 잘못 추론할 때 자주 일어난다. 특히 한국 백엔드에서 흔한 패턴은 BIGINT id를 String으로 받아서 JPA가 native query를 만들 때 캐스팅이 뒤집히는 경우다. 찜찜한 마음으로 EXPLAIN을 펴 보면 어이없이 full scan이 박혀 있다. 한 번 당하면 평생 기억하게 되는 함정이다.

### 함정 3. 통계 정보가 stale

이게 "어제는 50ms, 오늘은 5초"의 진짜 범인이다. 옵티마이저는 plan을 짤 때 통계 정보(planner cardinality)에 기댄다. "이 컬럼의 distinct 값이 1000개 정도다", "이 값 범위의 row가 전체의 10% 정도다" 같은 추정치다.

문제는 데이터가 빠르게 늘면 통계가 따라가지 못한다는 점이다. 예를 들어 `orders` 테이블에 `status` 컬럼이 있다고 해보자. 한 달 전 통계로는 `status = 'PENDING'`인 row가 0.1%였다. 옵티마이저는 "그럼 status 인덱스를 타고 0.1%만 읽으면 되겠군" 하고 plan을 짠다. 그런데 오늘 갑자기 PG가 죽어서 PENDING이 30%로 늘어 있다. 같은 plan으로는 30%를 인덱스로 읽고 row마다 heap을 fetch하니, 차라리 full scan보다 느려진다.

토스 SLASH 23에서 "통계 정보 갱신 안 된 게 진짜 자주" 발생한다고 한 게 이 얘기다. autoVACUUM·autoANALYZE가 못 따라가는 burst가 들어오면 plan이 박살난다. 그래서 운영 패턴 중 하나가 큰 batch 후에 명시적으로 `ANALYZE`를 돌리는 것이다.

### 함정 4. bind parameter peek과 plan cache

같은 쿼리도 어떤 파라미터로 처음 컴파일됐는지에 따라 cached plan이 다르다. 흔치 않은 값(`user_id = 99999999`, 본인만 가지고 있는 ID)으로 prepared statement가 먼저 컴파일됐는데, 그 plan이 캐시에 박혔다. 그 다음부터 흔한 값(`user_id = 1`, 100만 row 매칭)이 들어오면, 안 맞는 plan으로 100만 row를 인덱스 타고 fetch한다. 끔찍하다.

Postgres에서는 `plan_cache_mode`로, Oracle에서는 bind variable peek 설정으로 제어할 수 있다. 다만 이 함정은 처음 만나면 plan이 왜 갑자기 폭주하는지 단서가 거의 없으니, 한 번 당해본 사람이 두 번째에 의심하는 종류의 함정이다.

### 그래서 어떻게 디버깅하는가

네 함정을 다 모아 보면 한 가지 결론이 나온다. **인덱스가 안 타는 90%는 인덱스가 빠져서가 아니라, query 형태나 데이터 분포가 어긋나서다.** *Use The Index, Luke!*의 Markus Winand가 단호하게 정리한다.

> 90% of slow queries are not 'missing index' but 'wrong query shape'. Adding indexes is the band-aid. (커뮤니티 휴리스틱 6)

이게 휴리스틱 6, "index를 추가하기 전에 query를 의심해라"다. 새벽 3시에 slow query가 떴다고 무작정 `CREATE INDEX`부터 치지 말자. 먼저 EXPLAIN을 펴고, `Rows`가 실제와 얼마나 어긋나 있는지 보자. 통계가 stale인지 의심하고, type cast를 의심하고, composite의 첫 컬럼이 빠졌는지 의심하자. 그 다음에도 답이 없을 때 인덱스를 추가하는 편이 낫다.

이 습관 하나만 박혀도 RDB가 가장 자주 우리를 배신하는 새벽 alert를 절반은 막을 수 있다.

## Connection Pool — 정말로 (core × 2) + 1인가

DB가 느려지는 두 번째 큰 범인은 connection pool이다. 의외로 많은 팀이 pool size를 100, 200으로 박아 두고 "왜 이렇게 늦지" 한다. 답을 먼저 말하면, **pool은 작을수록 좋다**.

HikariCP 공식 wiki가 가장 직설적이다.

> connections = ((core_count * 2) + effective_spindle_count) (HikariCP, About Pool Sizing)

CPU 코어가 8개인 DB 서버에 대해 적정 pool size는 16 + 1 = 17 정도다. 직관과 어긋난다. "동시 사용자가 1000명인데 connection이 17개?" 싶다. 하지만 진실은 단순하다. **DB는 CPU에서만 일을 한다.** 동시 active query 수가 코어 수를 넘어가는 순간, 모든 query는 context switch와 lock contention에 시간을 쓴다. 그래서 pool을 키우는 만큼 throughput이 떨어진다.

HikariCP 공식 벤치마크가 보여주는 곡선이 인상적이다. pool size 50일 때보다 10일 때 throughput이 2배 가까이 높다. 같은 시스템인데, pool을 줄였더니 빨라진다. 처음 보면 "정말?" 싶지만, 위의 설명을 곱씹어보면 당연한 결과다.

물론 cloud SSD 시대에 `spindle = 1`로 박는 가정은 단순화다. NVMe·io2 같은 빠른 스토리지에서는 좀 더 키워도 된다. 그러나 시작점은 "core × 2 + 1"이고, 거기서 부하 테스트로 조금씩 늘려가며 throughput이 더 이상 오르지 않는 지점을 찾는 편이 낫다.

### connection pool exhaustion의 도미노

pool을 잘못 잡으면 어떤 일이 일어나는가? 한 service의 slow query가 전체 mesh를 죽인다. tribal #12, "Database connection pool exhaustion → cascade"가 정확한 이름이다.

상황을 가정해보자. 결제 service가 user service의 API를 호출한다. user service는 user DB를 본다. 어느 날 user DB에 slow query가 떠서 한 connection을 5초간 잡고 있다. 그 사이 user service의 다른 요청들이 모두 connection을 기다리느라 막힌다. 결제 service는 user service의 응답을 기다리느라 자기 connection을 잡고 있고, 다른 service들이 결제 service의 응답을 기다리느라 또 막힌다. 한 DB의 slow query 하나가 5분 만에 전체 mesh를 stall시킨다.

그래서 connection pool은 반드시 두 개의 안전장치를 가져야 한다.

- **timeout**: connection 획득에도, query 실행에도 timeout을 박는다. "Every network call MUST have a timeout"이 그냥 나온 말이 아니다(휴리스틱 4 — 10장에서 자세히 다룬다).
- **circuit breaker**: 5초 안에 응답 못 받는 다운스트림은 잠시 차단해서 cascade를 막는다(역시 10장).

물론 connection pool은 부품 한 개의 설정이지만, 그 결정이 분산 시스템 전체의 resilience에 직결된다는 점이 흥미롭다. 빌딩 블록 챕터에서 이미 분산의 어둠이 슬쩍 보이는 셈이다.

## VACUUM과 transaction wraparound — Postgres의 가장 어두운 함정

Postgres를 쓰는 팀이 적어도 한 번은 만나는 함정이 있다. **transaction wraparound**다. tribal #8에 들어가 있는 함정인데, 자주 듣고도 자주 잊는다.

Postgres는 MVCC(Multi-Version Concurrency Control)로 동시성을 처리한다. 한 row를 UPDATE할 때마다 새 버전을 만들고, 옛 버전은 "더 이상 보일 필요 없을 때" VACUUM이 와서 청소한다. 그리고 이 모든 동작에 32-bit transaction ID(XID)가 붙는다.

문제는 XID가 32-bit, 즉 약 40억이라는 점이다. 트랜잭션이 40억 번 발생하면 wraparound가 일어난다. 옛 row의 XID가 미래의 XID보다 커 보이는 모순이 생기고, 그러면 DB가 read-only 모드로 전환되어 버린다. 그 다음 "VACUUM FREEZE 하기 전엔 못 일어난다"는 안내문과 함께 4시간짜리 outage가 시작된다.

이 함정을 처음 듣는 사람은 "40억이면 안전한 거 아닌가?" 싶다. 그런데 초당 1000 트랜잭션이면 46일이면 도달한다. burst 트래픽이 잦은 한국 핀테크 환경에서는 더 빠르다. 카카오뱅크가 청약 0시 트래픽 대응을 하면서 가장 먼저 점검하는 부분 중 하나가 autovacuum 설정이라는 발표가 있었다(한국 1).

이를 막는 방법은 명확하다. **autovacuum을 절대 끄지 말자.** 그리고 큰 테이블에서는 `autovacuum_vacuum_scale_factor`를 기본값(20%)보다 낮춰서, 1~5% 변화에도 vacuum이 돌게 만드는 편이 낫다. 무엇보다 `pg_stat_user_tables`의 `n_dead_tup`과 `last_autovacuum`을 정기적으로 보는 습관을 들이는 것이 좋다.

이 함정의 이름이 한국 SRE 커뮤니티에서 자주 회자되지 않는다는 점이 오히려 위험하다. 너무 드물게 일어나서 잊혀지고, 잊혀진 뒤 첫 번째로 만나는 팀이 4시간 outage를 겪는다. 잊지 말자, 32-bit는 작다.

## Aurora — "log is the database"가 무슨 뜻인가

여기까지가 단일 노드 Postgres·MySQL의 운영 함정이다. 이제 시야를 한 단계 넓혀 보자. AWS Aurora는 무엇이 다른가? 그리고 왜 한국 백엔드의 절반쯤이 RDS Postgres에서 Aurora로 이주하고 있는가?

Aurora 논문(P14, SIGMOD '17)이 가장 단호하게 표현한다.

> The log is the database. (Verbitski et al., 2017)

이 한 줄이 핵심이다. 풀어서 보자.

전통적인 Postgres·MySQL은 write를 처리할 때 여러 IO를 친다. 먼저 WAL(write-ahead log)에 redo를 적고, page를 메모리에서 dirty로 표시하고, 나중에 checkpoint에서 page를 disk로 flush한다. replica가 있다면 binlog/WAL을 따로 전송하고, replica는 받은 log를 다시 apply해서 page를 만든다. 같은 변경이 여러 형태(WAL, page, replica WAL, replica page)로 네 군데 다섯 군데를 옮겨다닌다.

Aurora는 이걸 뒤집는다. compute node는 page를 다루지 않는다. 오직 **redo log만** storage layer로 던진다. storage layer는 6-way replication을 가진 분산 시스템인데, 받은 redo log를 자기네가 알아서 page로 reconstruct한다. compute는 stateless에 가깝고, storage가 모든 durability를 책임진다.

> Our central design tenet is that the most precious resource is the network. (Verbitski et al., §1)

이 결정 덕분에 Aurora는 MySQL 대비 5배, Postgres 대비 3배 throughput을 낸다. 그리고 더 중요한 운영상의 이득이 있다. replica를 띄울 때 데이터를 복사할 필요가 없다. 이미 storage layer가 공유돼 있다. 그래서 "Aurora replica 추가"는 분 단위가 아니라 초 단위다. read replica로 read load를 분산하는 일이 정말로 쉬워진다.

물론 trade-off는 있다. Aurora는 AWS lock-in이고, 비용은 RDS보다 높다. 그리고 "log is the database"라는 우아한 모델이지만, write latency는 결국 6 quorum 중 4의 ack를 기다려야 한다. cross-AZ network round-trip이 끼니, 단일 노드 Postgres보다 write latency가 약간 더 길 수 있다. NewSQL인 CockroachDB·Spanner와 비교했을 때, Aurora는 "single-leader Postgres의 storage만 분산화한" 모델임을 기억해두자(W4 CockroachDB 비교). 진짜 multi-region active-active write를 원하면 Aurora로는 부족하고, Spanner나 CockroachDB가 답이다.

그러나 한국의 90% 케이스에서, RDS Postgres가 한계에 부딪혔다고 느낄 때 가장 먼저 시도할 마이그레이션은 Aurora다. 우아한형제들도 Aurora I/O optimized로 비용을 30% 줄였다는 발표가 있었다(자료 28, 우아한형제들 인프라 비용 발표). RDS에서 Aurora로 가는 길은 거의 무중단으로 가능하다. 그게 가장 큰 강점이다.

## Trade-off 표 — 어떤 DB를 골라야 하는가

여기까지 살펴본 내용을 한 장으로 정리해보자. 새로운 서비스에 RDB를 골라야 할 때, 무엇을 보고 결정하는가? 다음 표가 우리가 평소에 가장 자주 만나는 4개를 정리한 것이다.

| 항목 | Postgres (self-managed) | MySQL (self-managed) | Aurora (Postgres/MySQL) | CockroachDB |
|------|--------------------------|------------------------|--------------------------|-------------|
| **architecture** | single leader + streaming replication | single leader + binlog replication | "log is the database", 6-way storage | distributed SQL, HLC 기반 |
| **write throughput** | 단일 노드 한계 (코어·디스크 종속) | Postgres와 비슷 | Postgres 대비 ~3x (P14) | 수평 확장 가능, 단 single-row write는 더 느림 |
| **read replica 추가** | streaming setup, 분~시간 | binlog setup, 분~시간 | shared storage, 분 단위 즉시 | 자동 |
| **multi-region write** | 불가 (read-only replica만) | 불가 (read-only replica만) | Global Database (write는 한 region) | active-active 가능 |
| **isolation** | true serializable 가능 | repeatable read (default) | Postgres/MySQL 동일 | serializable default |
| **운영 부담** | 자체 backup·HA·VACUUM 모두 직접 | 자체 backup·replication 직접 | AWS가 backup·failover 처리 | 자체 운영, 또는 CockroachDB Cloud |
| **vendor lock-in** | 없음 | 없음 | AWS 강함 | 약함 (self-hosted 가능) |
| **권장 케이스** | 시작점, 작은 팀 | OLTP write-heavy, MySQL 운영 경험 풍부 | RDS의 다음 단계, AWS 친화 팀 | 진짜 multi-region 필요, 글로벌 서비스 |
| **회피 케이스** | 진짜 multi-region | 진짜 multi-region | 진짜 multi-region active-active | OLTP latency 민감, 작은 팀 |

표를 한 줄로 줄이면 이렇다. **시작은 Postgres, 한계가 오면 Aurora, 진짜 글로벌이면 CockroachDB나 Spanner.** 그리고 Daniel Abadi가 NewSQL 비판에서 짚은 대로, "NewSQL이 default로 serializable이라는 marketing은 종종 사실이 아니다"는 점도 기억해두자(자료 4, Abadi 2018). NewSQL의 약속을 곧이곧대로 받아들이지 말고, 자기 isolation level을 한 번은 EXPLAIN으로 검증하는 편이 낫다.

## Sidebar: JPA N+1과 우아한형제들의 진단 패턴

한국 백엔드의 일상에서 가장 흔하면서 가장 silent한 killer를 한 페이지 따로 보고 가자. **JPA N+1**이다.

상황을 가정해보자. `Order` 엔티티가 `User`를 ManyToOne으로 참조하고, `User`가 `Address`를 OneToMany로 가지고 있다. 화면에서 주문 목록 100개를 보여주려고 `orderRepository.findAll()`을 호출한다. 한 번의 SQL로 끝날 것 같지만, fetch type이 LAZY로 잡혀 있으면 N+1 query가 터진다.

- `SELECT * FROM orders LIMIT 100` — 1 쿼리
- `SELECT * FROM users WHERE id = ?` — 100 쿼리 (각 order의 user 조회)
- `SELECT * FROM addresses WHERE user_id = ?` — 100 쿼리 (각 user의 주소 조회)

총 201개의 쿼리가 한 화면 렌더링에 나간다. 끔찍하다. 그리고 더 끔찍한 건, 개발 환경에서는 데이터가 적어서 안 보인다는 점이다. production에 올라가서 트래픽이 들어와야 비로소 DB가 비명을 지른다.

우아한형제들 techblog에 N+1 회피 가이드가 여러 번 올라온 이유가 이거다(한국 6). 한국 백엔드의 절대다수가 Spring + JPA를 쓰니, 이 패턴이 일상의 함정이다. 우아한형제들이 정착시킨 진단 패턴을 한 줄로 줄이면 다음과 같다.

1. **개발 환경에 hibernate.show_sql + p6spy를 켜자.** 실제 query가 몇 개 나가는지를 눈으로 본다.
2. **fetch join 또는 @EntityGraph로 명시적 join을 강제하자.** LAZY가 default라 가정하고, 한 화면에서 함께 보여줄 연관 엔티티는 명시적으로 한 쿼리에 모은다.
3. **DTO projection을 우선시하자.** 화면 전용 view라면 굳이 엔티티 전체를 가져올 필요가 없다. JPQL의 `new com.example.OrderDto(o.id, u.name, ...)`로 select projection을 박는다.
4. **production에서 query log + APM의 SQL count를 모니터링하자.** 한 요청당 query가 갑자기 100개를 넘는 endpoint가 있으면 N+1을 의심한다.

JPA를 쓰지 않는 사람도 같은 함정을 ORM마다 자기 식으로 만난다. Rails의 ActiveRecord에서는 `.includes`로, Prisma에서는 `include`로 해결한다. 도구는 다르지만, "한 화면에 쓰일 데이터는 한 쿼리에 모으자"는 원칙은 같다.

5장 검색 엔진에서 인덱싱 파이프라인의 silent killer를 다룰 것이다. 한국 백엔드는 5장의 silent killer와 이 N+1, 두 개를 평생 안고 산다. 잊지 말자.

## 이 장의 약속 회수

새벽 3시에 slow query alert가 울렸다고 해보자. 이 장을 다 읽은 우리는 무엇을 첫 5분 안에 할 수 있는가?

1. **인덱스 추가부터 의심하지 않는다.** EXPLAIN을 펴고, `Rows estimated`와 `Rows actual`의 괴리부터 본다. 통계가 stale인지 의심한다.
2. **composite index의 첫 컬럼이 WHERE에 등호로 들어 있는지 확인한다.** 빠져 있으면 인덱스는 안 탄다.
3. **type cast가 발생하는지 EXPLAIN의 plan에서 본다.** implicit conversion이 보이면 그게 범인이다.
4. **trace한 query가 prepared statement라면, plan cache가 잘못 박혔는지 의심한다.** 같은 쿼리를 ad-hoc으로 던져 본 plan과 비교한다.
5. **autovacuum이 돌고 있는지, `n_dead_tup`이 얼마나 쌓였는지** `pg_stat_user_tables`로 확인한다. burst 직후라면 명시적 `ANALYZE`를 한 번 돌린다.
6. **그리고 마지막에야 인덱스 추가를 고민한다.**

이 6단계가 머릿속에 자동으로 펼쳐지면, 우리는 "RDB를 안다"고 말할 자격이 있다. 그리고 이 책의 6번째 약속 — "이 책을 다 읽으면 새 endpoint를 설계할 때 자동으로 의심해야 할 5가지가 떠오른다" — 의 첫 번째 회수가 여기서 일어났다.

## 다음 장으로 가는 다리

RDB는 우리에게 schema·SQL·ACID·30년 운영 도구를 약속한다. 그러나 단일 노드의 한계, 한 row당 수십만 versioned write, partition key를 마음대로 정해야 할 도메인을 만나면 RDB는 더 이상 답이 아니다.

그래서 다음 장에서는 NoSQL을 살펴본다. 정확히 말하면, "schema가 유연해서" "확장이 쉬워서" NoSQL을 고른다면 도대체 무엇을 양보한 것인지를 묻는다. Dynamo 계열과 Bigtable 계열이 어떻게 다르고, hot partition이 왜 평생의 적인지를 살펴보자. RDB에서 가장 자주 우리를 배신하던 통계 정보의 함정이, NoSQL에서는 어떻게 다른 모습으로 나타나는지도 함께 본다.

다음 장으로 가기 전에 한 번 정리하자. **RDB가 우리를 배신하는 90%는 인덱스가 빠져서가 아니라, query 형태와 데이터 분포가 어긋나서다.** 이걸 기억하는 것만으로도 우리는 한 단계 위로 올라간 백엔드 개발자다.
