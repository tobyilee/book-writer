# 21장. Connection pooling과 모니터링 — PgBouncer·pg_stat_statements

느린 쿼리 하나를 찾고 싶다고 해보자. 어디서부터 시작해야 할까. 누군가는 운영 로그를 처음부터 끝까지 뒤지자 하고, 누군가는 APM부터 깔자 한다. 비싼 도구를 도입하고, 트레이싱 SDK를 애플리케이션에 박아 넣고, 며칠을 들여 대시보드를 만든다. 그런데 PostgreSQL을 쓴다면 더 가까운 답이 있다. 데이터베이스 자신이 이미 거의 모든 답을 들고 있다는 사실이다.

문제는 그 답을 꺼내는 방법을 모른다는 것이다. `pg_stat_statements`라는 이름을 들어본 적은 있어도, 막상 켜본 적은 없다. `pg_stat_activity`로 락 분석을 할 수 있다는 말은 들었어도, 실제 그 뷰에서 뭘 봐야 하는지는 흐릿하다. 게다가 모니터링 이야기를 꺼내기 전에 풀러부터 골라야 한다. 4장에서 우리는 "PostgreSQL에는 왜 풀러가 필수인가"의 답을 잡았다. fork 모델이라는 구조적 결과다. 그렇다면 이번 장의 질문은 한 발 더 나간 곳에 있다. 풀러는 무엇을 어떤 기준으로 고를 것이며, 모니터링은 어디서부터 시작해야 하는가.

이 두 질문은 사실 한 덩어리다. 풀러를 잘 골랐다는 말은 "어떤 모드로 운영해야 우리 워크로드가 안전한지"를 안다는 뜻이고, 모니터링이 살아있다는 말은 "그 결정이 실제로 어떻게 작동하는지를 본다"는 뜻이기 때문이다. 둘 다 운영 가시성이라는 같은 단어의 다른 얼굴이다. 함께 살펴보자.

## 21.1 PgBouncer — session·transaction·statement 모드

먼저 풀러의 표준부터 짚자. PgBouncer는 2007년 Skype에서 시작된 경량 connection pooler다. C로 작성된 단일 프로세스 single-threaded 구조이고, libev 기반 이벤트 루프로 수만 개의 클라이언트 연결을 적은 메모리로 소화한다. PostgreSQL 생태계에서 "풀러"라는 말이 나오면 사실상 PgBouncer를 가리키는 상태가 십수 년 이어졌다. 매니지드 PG든 자체 운영이든, 첫 풀러로 PgBouncer를 거치지 않는 팀은 드물다.

PgBouncer의 본질은 단순하다. 클라이언트 쪽과 PostgreSQL 쪽 사이에 앉아서, 클라이언트의 연결 요청은 가볍게 받아주고, 실제로 PG로 가는 연결은 미리 만들어둔 풀에서 빌려준다. 클라이언트가 PG에 직접 붙으면 매번 fork·setup·tear-down 비용이 발생하지만, 풀러 뒤에 두면 "이미 살아 있는 backend process"를 빌려 쓰는 모양이 된다. 4장에서 본 fork 비용의 문제를 풀러가 풀어주는 셈이다.

여기까지는 어떤 풀러나 다 한다. PgBouncer를 다룰 때 진짜 어려운 결정은 따로 있다. 풀링 모드를 무엇으로 둘 것인가의 결정이다. PgBouncer는 세 가지 모드를 제공한다. **session**, **transaction**, **statement**다. 이름은 단순하지만, 이 셋의 차이가 사실상 PgBouncer 운영의 거의 모든 함정을 결정한다. 하나씩 들여다보자.

**session 모드**는 가장 보수적인 방식이다. 클라이언트가 풀러에 연결을 잡으면, 그 클라이언트가 연결을 끊을 때까지 풀러는 한 PG backend를 해당 클라이언트에게 전용으로 묶어둔다. 클라이언트 100명이 있다면 풀러도 100개의 PG 연결을 들고 있어야 한다는 뜻이다. 풀링의 효과가 거의 없다고 봐도 된다. "그럼 왜 쓰는가" 싶겠지만, session 모드의 의미는 다른 데 있다. **세션 상태가 깨지지 않는다.** prepared statement, `SET LOCAL`, advisory lock, temporary table, cursor, listen/notify 같은 "세션에 묶이는" 모든 것이 그대로 작동한다. 안전이라는 가치를 풀링 효율과 맞바꾼 모드다.

**transaction 모드**가 PgBouncer의 진짜 무대다. 클라이언트가 트랜잭션을 시작하면 풀러가 PG backend 하나를 빌려주고, `COMMIT`/`ROLLBACK`이 떨어지는 순간 backend를 풀로 반환한다. 다음 트랜잭션은 완전히 다른 backend로 갈 수 있다. 같은 클라이언트의 연속된 두 트랜잭션이라도 그 사이에 어떤 다른 클라이언트의 트랜잭션이 끼어들어 같은 backend를 빌려 쓸 수 있다는 뜻이다. 풀링 효율은 극적으로 좋아진다. 클라이언트 5,000명, PG backend 50개라는 비율도 가능해진다. OLTP 워크로드 대부분이 transaction 모드를 선택하는 이유다.

**statement 모드**는 가장 공격적이다. 단일 SQL 문장이 끝나는 순간 backend를 회수한다. multi-statement 트랜잭션 자체를 허용하지 않는다는 강한 제약이 붙는다. 사실상 stateless한 쿼리 워크로드 — 예컨대 단순 lookup 위주의 분석 게이트웨이 — 에서만 쓸 만한 모드다. 일반 애플리케이션에는 거의 안 맞는다.

세 모드를 비교하면 이렇다.

| 모드 | 백엔드 반환 시점 | 풀링 효율 | 세션 상태 보존 | 적합 |
|------|----------------|----------|---------------|------|
| session | 클라이언트 연결 종료 시 | 낮음 (사실상 없음) | 완전 보존 | 마이그레이션 직후, 세션 상태 의존 워크로드 |
| transaction | COMMIT/ROLLBACK 시 | 매우 높음 | 트랜잭션 단위만 | 일반 OLTP — 대다수의 표준 |
| statement | 한 문장 끝날 때마다 | 극단적 | 거의 없음 | 단순 lookup, multi-statement 없음 |

기억해두자. 풀링 모드는 한번 골라서 끝나는 결정이 아니다. 어떤 애플리케이션은 같은 PG 클러스터에서 transaction 모드로, 어떤 워크로드는 session 모드로 운영해야 할 수 있다. PgBouncer에는 데이터베이스 별로 풀 설정을 다르게 줄 수 있고, 여러 풀러 인스턴스를 띄워 워크로드를 갈라놓는 패턴도 흔하다. "풀러 한 대로 모든 워크로드를 통일하려는" 욕망이야말로 운영 사고의 단골 원인이다.

PgBouncer 첫 도입 시의 권장 시작점도 짚어두자. `pool_mode = transaction`, `default_pool_size = 20~30` 부터 시작하는 것이 OLTP 표준이다. 그리고 `max_client_conn`은 충분히 크게(수천 단위), `default_pool_size`는 PG의 `max_connections`보다 훨씬 작게. 풀러 뒤의 PG에 `max_connections = 200` 같은 보수적인 값을 쥐어주고, 풀러가 그 200개를 잘게 쪼개 수천 클라이언트에 빌려주는 그림이 PgBouncer 운영의 정공법이다.

여기서 한 가지 의문이 생긴다. "transaction 모드의 풀링 효율이 그렇게 좋다면, 모두가 그것만 쓰면 되지 않나?" 답은 단순하지 않다. transaction 모드는 그 효율의 대가로 세션 상태를 잃는다. 그리고 그 잃는 상태가 어떤 워크로드에서는 결정적인 기능을 무력화한다. 다음 절에서 그 함정들을 정면으로 보자.

## 21.2 transaction pooling의 함정 — prepared statement·advisory lock·SET LOCAL

transaction 모드를 켜고 운영을 시작하면, 어느 날 갑자기 애플리케이션이 이상하게 작동하기 시작하는 경우가 있다. 어떤 클라이언트는 잘 도는데 어떤 클라이언트는 `prepared statement "S_3" does not exist` 같은 에러를 뱉는다. advisory lock이 의도와 다르게 동작한다. `SET LOCAL`로 거는 줄 알았던 timezone 설정이 다음 트랜잭션에는 사라져 있다. 디버깅이 정말 난감해지는 순간이다. 무엇이 잘못된 걸까.

답은 한 줄이다. **transaction pooling은 트랜잭션 단위로만 상태를 보장한다.** 트랜잭션을 넘어 살아남아야 하는 모든 세션 상태가 풀러를 통과하지 못한다. 함정의 정체를 하나씩 풀어보자.

**prepared statement** 함정이 가장 흔하다. JDBC, asyncpg, psycopg 같은 클라이언트 라이브러리는 보통 자동으로 server-side prepared statement를 만들어 쓴다. 처음에 `PREPARE`로 plan을 캐시해두고, 이후엔 `EXECUTE`로 호출만 한다. plan 캐시가 reuse되어 빠르다는 게 핵심이다. 그런데 transaction 모드에서는 PREPARE를 했던 backend와 EXECUTE를 요청한 backend가 다른 프로세스다. EXECUTE 시점의 backend에는 그 prepared statement가 없다. "S_3는 무엇이냐"라는 에러가 그래서 떨어진다.

이 함정의 우회법은 몇 가지 있다. 첫째, 클라이언트 라이브러리에서 prepared statement를 끄는 것이다. JDBC는 `prepareThreshold=0`, psycopg는 `prepare_threshold=None`. 가장 단순한 해법이지만 plan 캐시 효율이 떨어진다. 둘째, 애플리케이션 차원에서 `DEALLOCATE`로 명시 관리하는 것이다. 번거롭다. 셋째, **PgBouncer 1.21부터 들어온 server-side prepared statement protocol 지원**이다. PgBouncer가 prepared statement를 풀 차원에서 캐시하고, transaction 모드에서도 reuse가 가능해진다. 이쪽이 가장 깔끔한 답이다. 다만 모든 클라이언트와 protocol이 다 지원하는 것은 아니라서, 도입 전에 운영 중인 드라이버 호환성은 점검해두는 편이 낫다.

**advisory lock**도 비슷한 사정이다. `pg_advisory_lock(key)`는 세션에 묶이는 락이다. 트랜잭션 단위가 아니다. transaction 모드에서 한 트랜잭션 안에서 `pg_advisory_lock`을 걸고, 다음 트랜잭션에서 `pg_advisory_unlock`을 호출하려 하면 — 두 트랜잭션은 다른 backend로 갈 수 있고, 락을 건 backend는 이미 다른 클라이언트가 빌려 쓰는 중이다. 풀어야 할 락이 다른 곳에 있는 것이다. 분산 작업 큐의 경합 방지로 advisory lock을 즐겨 쓰던 팀이 transaction 풀러로 옮기면서 락이 영원히 안 풀리거나, 엉뚱한 곳에서 풀리는 사고를 만난다. 대응법은 두 가지다. 그런 워크로드는 **session 모드 풀러로 분리**하거나, **트랜잭션 범위 advisory lock(`pg_advisory_xact_lock`)을 쓰는 것**이다. 후자가 transaction 모드와 깨끗하게 어울린다.

**`SET LOCAL`이 아닌 `SET`** 도 사고 단골이다. `SET timezone = 'Asia/Seoul'`은 세션 단위 설정이다. transaction 모드에서 이걸 트랜잭션 안에 걸면 — 다음 트랜잭션이 같은 backend에 다시 올라탔을 때 그 timezone이 그대로 살아있다. 다른 클라이언트가 그 backend를 빌려 갔다면, 그 클라이언트는 자기가 설정하지 않은 timezone으로 쿼리를 돌리는 것이다. 끔찍한 일이다. 데이터가 조용히 어긋난다. `SET LOCAL`은 트랜잭션이 끝나면 자동으로 리셋되므로 transaction 모드와 호환된다. 운영 룰을 하나만 두자면 — **transaction 모드 뒤에서는 `SET LOCAL`만 쓰자.** 일반 `SET`은 PgBouncer의 `server_reset_query`(보통 `DISCARD ALL`)에 맡기되, 그것도 충분히 신뢰하기 어렵다는 것을 기억해두는 편이 안전하다.

여기에 더해 잘 안 보이는 함정이 둘 더 있다. **temporary table**은 세션에 묶인다. transaction 풀러 뒤에서 temp table을 만들고 다음 트랜잭션에서 참조하려 하면 사라져 있다. **LISTEN/NOTIFY**도 마찬가지다. listen한 backend와 notify를 받을 backend가 다르면 알림이 누구에게도 도착하지 않는다. 이벤트 기반 워크로드를 풀러 뒤에서 운영하려면 LISTEN 전용 연결을 session 모드로 분리해두는 편이 낫다.

이 함정들을 다 정리해 한 표로 잡아두자. 운영 결정의 거의 모든 것이 여기 있다.

| 기능 | session | transaction | 우회법 |
|------|---------|-------------|--------|
| Prepared statement | 안전 | 깨짐 | PgBouncer 1.21+ protocol 지원 / 드라이버에서 끄기 |
| Advisory lock (session) | 안전 | 깨짐 | `pg_advisory_xact_lock`으로 전환 |
| `SET LOCAL` | 안전 | 안전 | (트랜잭션 단위라서) |
| `SET` (세션 단위) | 안전 | 누수 위험 | `SET LOCAL`로 통일 |
| Temporary table | 안전 | 깨짐 | session 풀로 분리 |
| LISTEN/NOTIFY | 안전 | 깨짐 | LISTEN 전용 session 풀 |
| Cursor (held) | 안전 | 깨짐 | 트랜잭션 안에서 완료 |

이 표를 보면 답이 한쪽으로 모인다. transaction 모드의 효율은 누리되, "세션에 묶이는 기능들"은 따로 격리하는 편이 낫다. 한 PG 클러스터 앞에 풀러 두 대를 띄워서 — 하나는 OLTP transaction 풀, 하나는 LISTEN/advisory lock용 session 풀 — 워크로드를 갈라놓는 패턴이 그래서 흔하다. 풀러는 한 대여야 한다는 고정관념을 버리자.

여기까지가 PgBouncer 본진의 이야기다. 그런데 시대가 바뀌면서 PgBouncer 외의 선택지도 늘었다. 가장 주목할 만한 두 가지가 Pgcat과 Odyssey다. 살펴보자.

## 21.3 Pgcat — 멀티스레드, read/write split

PgBouncer는 단일 스레드다. 십수 년간 그 단순함이 강점이었다. 하지만 32코어, 64코어 서버가 흔해진 2020년대에는 단일 스레드 풀러가 코어 하나만 태우면서 병목이 되는 장면이 점점 많아진다. 클라우드 환경에서 풀러를 컨테이너 한 대로 띄우려는데, 그 한 대가 트래픽을 못 받쳐주는 것이다. 이 빈자리를 채우러 등장한 것이 **Pgcat**이다.

Pgcat은 Rust로 작성된 PostgreSQL pooler다. 가장 큰 차별점은 **멀티스레드**다. tokio 런타임 위에서 worker 풀을 돌리고, 들어오는 클라이언트 연결을 여러 코어로 분산한다. 단일 인스턴스로 PgBouncer 여러 대를 모은 만큼의 처리량을 낼 수 있다. 컨테이너 한 대로 충분한 풀러를 운영하고 싶다면 매력적인 선택지다.

여기까지는 "더 빠른 PgBouncer" 정도의 이야기지만, Pgcat이 진짜 흥미로워지는 지점은 다른 곳에 있다. **read/write split을 풀러 레이어에서 처리해준다.** 무슨 말인지 풀어보자. 일반적으로 read replica를 활용하려면 애플리케이션이 직접 "이 쿼리는 read-only이니 replica로 보내야지"라고 결정해야 한다. ORM마다, 프레임워크마다 별도의 라우팅 설정이 필요하고, 트랜잭션 안에서는 또 primary로 강제해야 하고, replication lag을 어떻게 다룰지도 고민해야 한다. 번거롭다.

Pgcat은 이 결정을 풀러 레이어로 끌어올린다. 단일 PG 클러스터를 primary + N replicas로 묶어두면, Pgcat이 들어오는 쿼리를 파싱해서 read-only는 replica로, write를 포함한 트랜잭션은 primary로 자동 라우팅한다. **shard-aware 라우팅**도 지원해서, 사실상 Citus 비슷한 sharded PG 클러스터의 query router 역할까지 한다. 단순 풀러를 넘어 "PG용 query proxy"로 진화한 모양이다.

물론 그 편리함의 대가는 있다. SQL 파싱을 풀러가 하게 된다는 말은 — **풀러가 알아듣지 못하는 SQL이 있을 수 있다**는 뜻이다. CTE 안에 DML이 있는 복잡한 쿼리, prepared statement의 EXECUTE 형태, custom function 호출 등에서 파싱이 어긋날 가능성이 있다. Pgcat은 빠르게 개선되고 있지만, 도입 전에는 운영 워크로드의 대표 쿼리들을 Pgcat 뒤에서 한 번 흘려보고 라우팅이 의도대로 되는지 확인하는 단계가 꼭 필요하다. 그리고 **prepared statement protocol 지원**도 Pgcat이 더 늦게 따라온 영역이다. PgBouncer 1.21이 이미 안정화된 protocol level prepared statement 지원을 들고 있는 만큼, 그 한 가지로는 PgBouncer가 여전히 앞선다.

언제 Pgcat을 골라야 할까. 정리하면 이렇다.

- **트래픽이 단일 PgBouncer로 부족할 때.** 컨테이너당 처리량을 끌어올리고 싶거나, 풀러 수평 확장에 들어가는 운영 부담을 줄이고 싶을 때.
- **read replica를 적극적으로 활용하고 싶은데, 애플리케이션 레벨 라우팅 로직을 두기 싫을 때.** ORM 다루기 까다로운 레거시 서비스에서 특히 효과가 크다.
- **모던 클라우드/k8s 환경에서 풀러를 stateless하게 운영하고 싶을 때.** Pgcat은 hot reload, 메트릭 노출 등 운영 자동화에 친화적이다.

반대로 **transaction pooling의 깨끗한 표준 동작이 절대적으로 중요하다면 PgBouncer가 여전히 정답에 가깝다.** 13~15년 검증된 단일 프로세스의 신뢰성과, prepared statement protocol 지원의 성숙도가 그 이유다. "새로운 게 더 낫다"는 직감보다, 실제로 우리 워크로드의 어느 부분이 풀러 병목인지 측정하고 결정하는 편이 낫다. 그 측정이 안 되어 있다면 — 아직 PgBouncer를 떠나야 할 이유가 없다는 뜻이다.

## 21.4 Odyssey — Yandex 엔터프라이즈 라인

세 번째 선택지가 **Odyssey**다. Yandex가 자사 대규모 PG 인프라를 굴리려고 만든 풀러이고, 오픈소스로 공개되어 있다. Pgcat과 비슷하게 멀티스레드 구조이지만, 기술적 접근은 또 다르다. **multi-threaded multi-storage**가 Odyssey의 키워드다. 여러 PG backend pool을 효율적으로 관리하고, 다중 storage(여러 PG 클러스터)를 동시에 다루는 시나리오에 강점이 있다.

Yandex 같은 규모의 PG 운영을 상상해보자. 클러스터 수백 개, 풀러 인스턴스 수천 개, 매니지드 PG를 자사 클라우드에서 직접 굴리는 환경이다. 이런 곳에서는 풀러가 단순히 "연결 재사용 도구"가 아니라 **인프라 레이어의 핵심 컴포넌트**다. 풀러 자체의 안정성·확장성·관찰성이 PG 본진만큼 중요해진다. Odyssey의 설계 결정 대부분이 이 맥락에서 나왔다.

구체적으로 Odyssey가 차별화되는 지점들을 보자. **TLS termination이 본격적으로 들어 있다.** PG 클라이언트와 풀러 사이의 SSL을 풀러가 책임지고, PG로 가는 내부 연결은 평문/약식 TLS로 가는 식의 분리가 가능하다. **인증 패스스루**도 더 정교하다. SCRAM, LDAP, Kerberos 등 엔터프라이즈 인증과 통합되는 시나리오를 의식해 만들었다. **라우팅 규칙**을 더 세밀하게 줄 수 있어서, 사용자별·데이터베이스별·세션 옵션별로 다른 풀과 다른 storage로 보내는 식의 운영이 가능하다.

여기에 더해 Odyssey는 **prepared statement 풀링**을 자체적으로 들고 있다. PgBouncer 1.21이 이 기능을 따라잡기 전까지, Odyssey는 transaction 풀링 + prepared statement reuse를 한 풀러에서 깔끔하게 제공한 사실상 유일한 선택지였다. 지금은 PgBouncer도 따라왔지만, Odyssey의 구현이 더 오래 다듬어졌다는 점은 여전히 차별점으로 통한다.

그렇다면 Odyssey는 누구에게 맞을까. 솔직하게 말하면, **대부분의 팀에게는 과한 선택**이다. PgBouncer의 단순함이나 Pgcat의 모던함을 누리면서 시작하는 편이 낫다. Odyssey는 "PG를 매니지드 형태로 다른 팀에게 제공하는 인프라 팀"이나 "수천 개 클러스터를 운영하는 SaaS 백엔드 팀" 정도에서 진가가 나오는 도구다. 일반 애플리케이션 운영에서는 그 정교함이 오히려 학습 비용으로 돌아온다.

세 풀러를 한 표로 정리해두자. 다음에 풀러를 고를 일이 생기면 여기서 출발하면 된다.

| 차원 | PgBouncer | Pgcat | Odyssey |
|------|-----------|-------|---------|
| 언어 | C | Rust | C |
| 스레드 모델 | 단일 스레드 | 멀티스레드(tokio) | 멀티스레드 |
| Read/write split | 없음 | 내장 | 라우팅 규칙으로 가능 |
| Prepared statement (protocol) | 1.21+ 안정 | 추가됨, 성숙 중 | 자체 풀링 성숙 |
| 운영 성숙도 | 매우 높음 (15+ years) | 빠르게 성장 중 | 높음 (Yandex 검증) |
| 도입 학습 곡선 | 낮음 | 중간 | 높음 |
| 적합 | 표준 OLTP, 첫 선택 | 멀티코어 활용·R/W split | 엔터프라이즈/매니지드 인프라 |

기억해두자. 풀러는 가능한 한 보수적으로, 가능한 한 단순하게 고르는 편이 낫다. "최신이라 좋다"는 직감으로 풀러를 바꾸면 거의 항상 후회한다. 우리 워크로드가 PgBouncer로 한계에 부딪힌 증거를 손에 쥐고 나서, 그제야 Pgcat이나 Odyssey의 선택지를 검토하는 순서가 안전하다.

여기까지가 도구 선택의 이야기다. 풀러를 잘 골랐다고 해서 운영이 자동으로 잘 되는 건 아니다. 풀러 뒤에서 실제로 어떤 쿼리가 어떻게 도는지 — 그것을 보지 못하면 다음 사고는 시간문제다. 모니터링으로 넘어가자. 이번 장의 후반부 절반이 그 이야기다.

## 21.5 pg_stat_statements — 가장 먼저 켤 익스텐션

PostgreSQL을 운영하는 팀에게 단 하나의 익스텐션만 켜라고 한다면 — `pg_stat_statements`다. 다른 모든 모니터링 도구가 이 익스텐션 위에 서 있다고 해도 과장이 아니다. 그런데 의외로 켜지 않고 운영하는 팀이 꽤 있다. "기본이 아니니까 부담스럽다"거나 "성능 영향이 있다 들었다"는 막연한 거부감 때문이다. 그 거부감은 정말 근거가 있는 것일까? 미리 답을 말하면 — **거의 없다.** pg_stat_statements는 거의 모든 PG 운영의 전제다. 함께 살펴보자.

이 익스텐션이 하는 일은 단순하다. PG에서 실행되는 모든 SQL 문장을 **정규화한 형태로 누적 통계를 모으는** 것이다. 정규화한다는 말이 핵심이다. `SELECT * FROM users WHERE id = 123`과 `SELECT * FROM users WHERE id = 456`은 다른 SQL이지만, pg_stat_statements 입장에서는 `SELECT * FROM users WHERE id = $1` 하나로 묶인다. 같은 쿼리 패턴의 실행 횟수, 누적 실행 시간, 평균/최대/최소 시간, 읽은 buffer 수, write한 buffer 수, 캐시 hit ratio, 그리고 v13부터는 plan 시간까지 — 한 행에 모두 담긴다.

"느린 쿼리를 찾고 싶다"는 요구의 답이 사실상 한 줄짜리 SQL로 떨어진다.

```sql
SELECT
  queryid,
  query,
  calls,
  total_exec_time,
  mean_exec_time,
  rows,
  100.0 * shared_blks_hit / NULLIF(shared_blks_hit + shared_blks_read, 0) AS hit_pct
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```

이 쿼리 하나로 "총 누적 시간이 큰 상위 20개 쿼리"가 나온다. 한 번에 0.1초밖에 안 걸리지만 하루 천만 번 호출되어 총 시간이 1만 초인 쿼리도 잡히고, 한 번에 10초씩 걸리지만 하루 100번 도는 쿼리도 잡힌다. **둘은 다르게 처방해야 한다.** 전자는 호출 패턴 자체를 줄이거나 캐싱을 도입하는 게 답이고, 후자는 쿼리 자체를 최적화하거나 인덱스를 손봐야 한다. pg_stat_statements 없이 이 구분을 어떻게 할 것인지 상상해보면, 이 익스텐션의 가치가 한눈에 잡힌다.

켜는 방법도 어렵지 않다. `postgresql.conf`에 두 줄을 추가하고 재시작하면 끝이다.

```
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

`max`는 보관할 쿼리 패턴의 최대 수다. 기본 5,000인데, 운영 클러스터라면 10,000 정도로 늘려두는 편이 낫다. 부족하면 오래된 항목이 LRU로 밀려난다. `track = all`은 함수 내부의 SQL까지 추적한다는 의미이고, `track = top`(기본)은 클라이언트가 보낸 최상위 SQL만 추적한다. 함수 안의 SQL이 문제일 수 있다면 `all`을 고려하자.

성능 영향은 거의 무시할 수 있는 수준이다. Percona, AWS, Crunchy 등 주요 벤더의 측정 자료에서도 일관되게 1~2% 수준의 CPU 오버헤드만 보고된다. 클러스터의 가시성을 통째로 얻는 대가로 1~2%면 — 켜지 않을 이유가 없다. 매니지드 PG (RDS, Aurora, Cloud SQL, AlloyDB, Supabase, Neon)는 거의 모두 기본으로 또는 한 줄 설정으로 켤 수 있게 해두었다. 자체 운영이라면 첫 클러스터 부팅과 함께 켜는 편이 정공법이다.

운영에 들어가면 자주 쓰는 패턴이 몇 가지 더 있다. 알아두자.

**평균 시간이 갑자기 늘어난 쿼리 잡기:**

```sql
SELECT queryid, query, calls, mean_exec_time, stddev_exec_time
FROM pg_stat_statements
WHERE calls > 100
  AND stddev_exec_time > mean_exec_time
ORDER BY stddev_exec_time DESC
LIMIT 20;
```

표준편차가 평균보다 크다는 말은 — **어떤 호출은 빠르고 어떤 호출은 굉장히 느리다**는 신호다. 같은 SQL인데 파라미터에 따라 성능이 들쭉날쭉하다는 뜻이다. parameter sniffing 문제, 통계 부정확, 데이터 분포 skew의 단골 증거다. 24절에서 다룰 EXPLAIN ANALYZE의 대상 후보가 여기서 나온다.

**가장 많이 buffer를 읽은 쿼리 잡기:**

```sql
SELECT queryid, query,
       shared_blks_hit + shared_blks_read AS total_blocks,
       shared_blks_read AS disk_reads
FROM pg_stat_statements
ORDER BY total_blocks DESC
LIMIT 20;
```

I/O 압박의 원인 쿼리가 여기서 드러난다. shared buffer hit이 낮고 disk read가 많다면 — `shared_buffers` 설정을 손볼지, 해당 쿼리에 더 적합한 인덱스를 만들어 random I/O를 줄일지의 결정 자료가 된다.

**통계 리셋:**

```sql
SELECT pg_stat_statements_reset();
```

릴리스 직후, 인덱스 추가 직후, 쿼리 튜닝 직후 — "변경 전후"를 비교하고 싶을 때 리셋한다. 누적 통계가 너무 오래되면 평균값이 옛 데이터에 묻혀서 최근 변화를 못 보기 때문이다. 정기적으로 한 달에 한 번씩 리셋하는 운영 룰도 합리적이다.

여기서 한 가지 한계는 짚어두자. **pg_stat_statements는 현재 실행 중인 쿼리는 안 보여준다.** 그건 다른 뷰의 일이다. 그리고 **개별 호출의 actual plan은 모른다.** plan 시간은 알려주지만 plan 자체는 알려주지 않는다. plan을 알고 싶다면 `auto_explain`이라는 별도 익스텐션이 필요하다. 이 둘 — pg_stat_activity와 auto_explain — 의 자리를 아는 것이 다음 절의 몫이다.

## 21.6 pg_stat_activity·pg_stat_user_tables·pg_stat_user_indexes

pg_stat_statements가 "누적 통계의 창"이라면, **pg_stat_activity는 실시간 스냅샷의 창**이다. 지금 이 순간 어떤 backend가 어떤 쿼리를 돌리고 있는지, 누가 락에 걸려 기다리고 있는지, 어떤 트랜잭션이 idle in transaction 상태로 vacuum을 방해하고 있는지 — 이 뷰가 답한다.

운영에서 가장 자주 쓰는 형태는 이런 쿼리다.

```sql
SELECT
  pid,
  usename,
  application_name,
  state,
  wait_event_type,
  wait_event,
  now() - query_start AS duration,
  query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC NULLS LAST;
```

이 한 쿼리만으로 "지금 가장 오래 도는 쿼리"부터 "락 대기 중인 세션"까지 한눈에 잡힌다. **`wait_event_type`이 `Lock`인 세션은 락 충돌의 피해자**이고, 어떤 다른 세션을 기다리고 있는지는 `pg_blocking_pids(pid)` 함수로 찾을 수 있다. 야간 호출의 90%는 이 한 줄짜리 분석으로 출발한다고 봐도 된다.

특히 주의해서 봐야 할 상태가 **`idle in transaction`**이다. 트랜잭션을 열어두고 아무것도 안 하는 세션이라는 뜻이다. 애플리케이션이 BEGIN을 했다가 무언가 다른 일에 정신이 팔린 사이에 — 혹은 connection을 잃었지만 아직 timeout이 안 떨어진 사이에 — 트랜잭션이 열려 있는 상태다. 이게 위험한 이유는 5장에서 짚었던 그 이유다. **long-running transaction은 그 시작 시점의 XID를 잡고 있어서, 그 이후에 죽은 tuple을 vacuum이 회수하지 못한다.** 한 세션이 idle in transaction으로 한나절 잠들어 있는 동안, 클러스터 전체에 bloat이 쌓이고, 18장에서 본 wraparound 위험까지 가까워진다.

대응법은 두 가지다. 첫째, **`idle_in_transaction_session_timeout`을 설정해 자동으로 끊자.** `idle_in_transaction_session_timeout = '5min'` 정도가 일반적인 OLTP에서 합리적이다. 둘째, **알람을 걸자.** idle in transaction 상태가 1분 넘게 지속되는 세션이 있으면 Slack으로 알람이 가도록 해두면 사고 전에 잡힌다. pg_stat_activity는 그 알람의 데이터 소스가 된다.

pg_stat_activity와 짝을 이루는 뷰가 둘 더 있다. **`pg_stat_user_tables`**와 **`pg_stat_user_indexes`**다. 이름 그대로 사용자 테이블·인덱스의 누적 통계인데, 운영 가시성의 빠진 조각들을 채워준다.

`pg_stat_user_tables`에서 자주 보는 컬럼은 이런 것들이다.

- `n_live_tup` / `n_dead_tup` — 살아있는 / 죽은 tuple 수. 비율이 1:1에 가까워지면 vacuum이 따라오지 못하고 있다는 신호.
- `n_tup_ins` / `n_tup_upd` / `n_tup_del` — INSERT/UPDATE/DELETE 누적 카운트. 어떤 테이블이 write-heavy인지 한눈에.
- `n_tup_hot_upd` — HOT update 카운트. 전체 update 대비 HOT 비율이 낮으면 6장에서 다룬 fillfactor 조정 후보.
- `last_vacuum` / `last_autovacuum` / `last_analyze` — 마지막으로 vacuum/analyze가 돈 시점. 며칠째 안 돌고 있다면 autovacuum이 못 따라가는 테이블이라는 뜻.
- `n_mod_since_analyze` — 마지막 analyze 이후 수정된 row 수. 통계가 얼마나 stale한지의 척도.

운영 클러스터에서 한 달에 한 번은 이런 쿼리를 돌려보는 편이 낫다.

```sql
SELECT
  schemaname || '.' || relname AS table,
  n_live_tup,
  n_dead_tup,
  ROUND(n_dead_tup::NUMERIC / NULLIF(n_live_tup, 0) * 100, 2) AS dead_pct,
  last_autovacuum,
  n_mod_since_analyze
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY dead_pct DESC NULLS LAST
LIMIT 20;
```

dead tuple 비율이 큰 테이블, 자주 수정되는데 analyze가 늦은 테이블이 한 화면에 잡힌다. 18장에서 다룬 autovacuum 튜닝의 출발점이 여기서 나온다.

`pg_stat_user_indexes`의 진가는 정반대 방향에 있다. **"안 쓰이는 인덱스 찾기"**다.

```sql
SELECT
  schemaname || '.' || indexrelname AS index,
  idx_scan,
  pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelid NOT IN (
    SELECT conindid FROM pg_constraint WHERE contype IN ('p', 'u')
  )
ORDER BY pg_relation_size(indexrelid) DESC;
```

`idx_scan = 0`은 해당 인덱스가 한 번도 안 쓰였다는 뜻이다(통계 리셋 이후로). primary key나 unique constraint를 지지하는 인덱스는 제외하고, 순수하게 "탐색에 쓰일 의도로 만들어졌지만 아무도 안 쓰는 인덱스"를 찾는다. 이런 인덱스는 **write 성능을 갉아먹고, 디스크를 차지하며, autovacuum 시간을 늘린다.** 운영 클러스터를 인수받았을 때 가장 먼저 돌려볼 만한 쿼리다. 의외로 30~40%의 인덱스가 거의 안 쓰이는 경우가 흔하다. 찜찜하게 들리겠지만 실제로 그렇다.

물론 주의는 필요하다. `idx_scan`은 PG 시작 이후나 마지막 통계 리셋 이후의 누적치다. 분기 결산처럼 가끔만 도는 쿼리가 쓰는 인덱스가 "최근 한 달 안 쓰였다"는 이유로 지워지면 곤란하다. 통계 누적 기간을 충분히 두고(최소 한 달, 가능하면 한 분기), 분기성 batch job이 다 돈 이후 시점에 평가하는 편이 안전하다.

여기까지가 PG가 기본으로 들고 있는 통계 뷰들이다. 이것만으로도 운영의 90%는 보인다. 그런데 더 깊은 가시성이 필요한 순간이 온다. "쿼리는 느린데 왜 느린지 모르겠다", "buffer hit ratio는 멀쩡한데 OS 레벨에서 I/O가 튄다", "plan이 갑자기 바뀌었는데 그 시점의 plan이 어땠는지 모른다" 같은 상황이다. 그때 꺼내는 도구들이 다음 절의 주제다.

## 21.7 pg_stat_monitor·pg_stat_kcache·auto_explain — 통합 옵저버빌리티

pg_stat_statements와 기본 stat 뷰들로 운영을 시작했다. 시간이 지나면 한계가 드러난다. pg_stat_statements는 누적치만 보여줄 뿐 **시간 차원이 없다.** "이 쿼리의 평균 시간이 어제와 오늘 어떻게 달라졌는가"를 묻기 어렵다. 누군가 `pg_stat_statements_reset()`을 호출하면 이전 정보가 다 사라진다. plan이 바뀌어도 그 변화를 잡지 못한다. 이 빈자리를 메우려는 도구들이 등장했다. 가장 주목할 만한 세 가지를 보자.

**pg_stat_monitor**는 Percona가 만든 익스텐션이다. 이름이 비슷하지만 pg_stat_statements와는 다른 차원의 도구다. 핵심 차별점은 **bucket 기반 시계열**이다. 통계를 1분, 5분, 10분 같은 시간 단위로 잘라서 보관한다. "지난 한 시간 동안 5분 단위로 쿼리별 평균 시간이 어떻게 변했는가" 같은 시계열 질문에 답할 수 있다. 누적치만 들고 있는 pg_stat_statements가 못 하는 일이다.

거기에 더해 pg_stat_monitor는 **pg_stat_statements + pg_stat_activity + auto_explain의 정보를 한 뷰에 합쳐 놓았다.** 같은 쿼리에 대해 누적 통계, 현재 실행 중 여부, 실제 plan을 한 자리에서 본다. 워크로드 분석할 때 여러 뷰를 join하지 않아도 되는 편의가 크다. 게다가 **client IP, application name, user, query parameter 값**까지 함께 잡아두어 "어느 클라이언트의 어떤 호출이 느렸나"를 추적할 수 있다.

설정은 pg_stat_statements와 비슷하게 간단하다.

```
shared_preload_libraries = 'pg_stat_monitor'
pg_stat_monitor.pgsm_max = 100MB
pg_stat_monitor.pgsm_query_max_len = 2048
pg_stat_monitor.pgsm_bucket_time = 60
pg_stat_monitor.pgsm_max_buckets = 10
```

이렇게 두면 60초짜리 bucket을 10개(=10분 윈도우) 들고 있게 된다. 시계열을 길게 보고 싶다면 bucket size를 늘리거나 개수를 늘리자.

성능 영향은 pg_stat_statements보다 조금 더 큰 편이다(2~3% 수준). 그래도 얻는 가시성을 생각하면 합리적인 거래다. 다만 한 가지 — **pg_stat_monitor는 매니지드 PG에서 지원이 갈린다.** RDS는 지원하지 않는 경우가 많고, Cloud SQL이나 Aurora도 신중하다. 자체 운영이나 Crunchy/Tembo 같은 모던 매니지드를 쓴다면 어렵지 않게 켤 수 있다. 매니지드 PG라면 도입 전에 지원 여부를 확인하는 편이 낫다.

**pg_stat_kcache**는 또 다른 차원의 도구다. PG의 stat 뷰들은 PG 안에서 일어나는 일만 안다. shared_buffers의 hit/read, WAL write 등은 보이지만, **OS 레벨에서 실제로 디스크 I/O가 얼마나 발생했고 CPU를 얼마나 썼는지는 보이지 않는다.** PG가 "shared_buffers에서 못 찾아 read했다"고 말해도, 그 read가 OS 페이지 캐시에서 왔는지 진짜 디스크에서 왔는지는 모른다. 이 빈자리를 채우는 게 pg_stat_kcache다.

이 익스텐션은 OS의 getrusage 정보(user CPU time, system CPU time, page faults, block I/O)를 쿼리별로 모아준다. pg_stat_statements와 join해서 보면 "이 쿼리는 PG buffer에서는 잘 잡혔는데 실제로 disk I/O가 많이 일어났다"거나 "buffer hit이 낮은데 OS 페이지 캐시에서 거의 다 와서 latency는 괜찮다" 같은 정밀한 진단이 가능해진다. 클라우드 인스턴스 비용을 IOPS 단위로 내고 있다면 — 이 정보 없이 비용 최적화는 사실상 어렵다.

**auto_explain**은 셋 중 가장 단순하지만 가장 자주 쓰는 도구일 수 있다. 이름 그대로, **일정 시간 이상 걸린 쿼리의 EXPLAIN을 자동으로 로그에 남긴다.**

```
shared_preload_libraries = 'auto_explain'
auto_explain.log_min_duration = '1s'
auto_explain.log_analyze = true
auto_explain.log_buffers = true
auto_explain.log_format = 'json'
auto_explain.log_nested_statements = true
```

1초 넘게 걸린 모든 쿼리의 EXPLAIN ANALYZE 결과가 PG 로그에 JSON으로 떨어진다. 새벽 3시에 5초짜리 슬로우 쿼리가 한 번 떴다 — 다시 재현이 안 된다. 그 한 번의 plan을 알아야 원인을 찾는데, 아침에 다시 EXPLAIN을 돌려도 plan이 다르거나 latency가 안 나온다. 정말 난감한 상황이다. auto_explain이 켜져 있었다면 그 한 번의 EXPLAIN이 로그에 남아 있다. 이 한 번의 가치만으로도 auto_explain은 운영 옵션에 넣을 만하다.

물론 부담은 있다. **`log_analyze = true`는 모든 쿼리에 추가 오버헤드를 준다.** EXPLAIN ANALYZE 자체가 측정 비용이 있기 때문이다. 그래서 `auto_explain.sample_rate`로 일부만 샘플링하는 운영도 흔하다. 5%만 샘플링해도 통계적으로 의미 있는 분석이 가능하다.

이 세 도구를 어떻게 조합할지의 권장 패턴을 정리하면 이렇다.

| 단계 | 도구 | 목적 |
|------|------|------|
| 1단계 (필수) | pg_stat_statements | 누적 쿼리 통계 — 시작점 |
| 2단계 (강력 권장) | auto_explain (sample 10%, threshold 1s) | 슬로우 쿼리의 plan 추적 |
| 3단계 (성숙기) | pg_stat_monitor | 시계열·통합 가시성 (매니지드 지원 확인) |
| 4단계 (정밀 진단) | pg_stat_kcache | OS-레벨 자원 사용 (자체 운영 한정) |

순서가 중요하다. 1단계 없이 4단계로 가는 팀이 가끔 있는데, 그건 거의 항상 잘못된 순서다. 가장 단순한 것을 가장 먼저 켜고, 거기서 한계를 만난 다음에 더 정교한 도구로 가는 편이 낫다. 도구가 많을수록 좋다는 직감은 운영에서 종종 배반당한다.

여기까지가 PG 내부의 가시성 도구다. 그런데 운영이라는 말의 무게는 거기서 끝나지 않는다. 이 모든 통계를 **시간에 따라 시각화하고**, **임계치를 넘으면 알람을 받고**, **장애 시점의 정황을 재구성할 수 있어야** 비로소 운영이라 부를 만하다. 마지막 절의 주제다.

## 21.8 postgres_exporter → Prometheus → Grafana

pg_stat_statements와 pg_stat_activity가 아무리 좋아도, 한 가지 본질적 한계가 있다. **psql로 SELECT를 쳐야 보인다.** 새벽 2시에 알람이 울리려면, 누군가가 그 SQL을 주기적으로 돌려서 외부 시스템에 던져줘야 한다. 그 누군가의 표준 이름이 **postgres_exporter**다.

postgres_exporter는 Prometheus 생태계의 표준 PG exporter다. PG에 붙어서 stat 뷰들을 주기적으로 SELECT 하고, 그 결과를 Prometheus가 알아들을 수 있는 메트릭 형식으로 노출한다. Prometheus는 그 메트릭을 scrape해 시계열 DB에 저장하고, Grafana가 그 시계열을 시각화하고, Alertmanager가 임계치 위반에 알람을 쏜다. 이 4단(exporter → Prometheus → Grafana → Alertmanager) 스택이 사실상 오픈소스 PG 운영의 표준이다. 매니지드 PG에서도 동일한 메트릭을 노출하는 옵션을 점점 더 많이 제공하고 있다.

설치는 어렵지 않다. 컨테이너 하나 띄우면 끝이다.

```yaml
# docker-compose.yml 일부
services:
  postgres_exporter:
    image: prometheuscommunity/postgres-exporter:latest
    environment:
      DATA_SOURCE_NAME: "postgresql://exporter:secret@pg-host:5432/postgres?sslmode=disable"
    ports:
      - "9187:9187"
```

`postgres_exporter`가 사용할 PG 사용자는 모니터링 전용으로 따로 만드는 편이 낫다. `pg_monitor` role을 부여하면 stat 뷰 대부분에 read 권한이 자동으로 붙는다.

```sql
CREATE USER exporter WITH PASSWORD 'secret';
GRANT pg_monitor TO exporter;
```

이렇게 띄워두면 9187 포트에서 메트릭이 흘러나온다. Prometheus 설정에 scrape job 하나만 추가하면 된다.

```yaml
scrape_configs:
  - job_name: 'postgres'
    scrape_interval: 30s
    static_configs:
      - targets: ['postgres_exporter:9187']
```

여기까지 와 있다면 어떤 메트릭이 잡히는지 보자. postgres_exporter가 기본으로 노출하는 메트릭은 대략 100가지가 넘는다. 그중 운영에서 정말 자주 보는 것들을 추려보면 이렇다.

- **`pg_up`** — PG가 살아 있는지. 알람 1번 후보.
- **`pg_stat_activity_count`** — 현재 connection 수 (state별로 라벨). idle in transaction 폭증이 여기서 잡힌다.
- **`pg_stat_database_xact_commit` / `_xact_rollback`** — 커밋·롤백 비율. rollback이 갑자기 늘면 애플리케이션 사고의 신호.
- **`pg_stat_database_blks_hit` / `_blks_read`** — buffer hit ratio. 갑자기 떨어지면 메모리 압박.
- **`pg_stat_replication_pg_wal_lsn_diff`** — replica lag (byte). 비동기 복제의 핵심 알람.
- **`pg_database_size`** — DB 사이즈. 디스크 풀 알람.
- **`pg_stat_user_tables_n_dead_tup`** — dead tuple 누적. 18장의 autovacuum 진단.
- **`pg_locks_count`** — 락 카운트 (모드별). 락 폭증 알람.

이 메트릭들을 Grafana에 한 화면으로 모아둔 대시보드가 PG 운영의 일상이다. 다행히 처음부터 다 만들 필요는 없다. **grafana.com에 PostgreSQL 대시보드 템플릿이 수십 개 공개되어 있다.** ID 9628(PostgreSQL Database)이나 ID 12485(PostgreSQL Overview) 같은 검증된 템플릿부터 시작해서, 우리 워크로드에 맞게 조금씩 변형해가는 편이 합리적이다. 빈 캔버스에서 출발해 처음부터 만드는 것은 시간 낭비에 가깝다.

알람도 몇 가지는 첫날부터 걸어두자. 사고 전에 잡혀야 하는 후보들이다.

- **pg_up == 0이 1분 이상** — PG 다운 알람. 가장 단순하고 가장 중요.
- **idle in transaction이 5분 이상인 세션** — wraparound·bloat의 전조.
- **replica lag이 60초 이상** — 데이터 일관성 SLA 위반의 신호.
- **dead tuple 비율이 30% 넘는 테이블** — autovacuum 추적 실패.
- **connection 수가 max_connections의 80% 도달** — 풀러 튜닝 시점.
- **disk 사용률 80% 이상** — 디스크 풀의 전조.

이 여섯 가지 알람만 걸어두어도 PG 운영의 야간 호출의 절반은 사고 전에 잡힌다. 더 정교한 알람은 그다음 단계에서 늘려가면 된다. 처음부터 50개 알람을 만들어두면 — 그게 alert fatigue를 만들고, 진짜 알람이 묻혀버린다. 끔찍한 일이다.

매니지드 PG를 쓰는 경우는 어떨까. AWS RDS는 **Performance Insights**라는 자체 도구를 제공한다. pg_stat_statements + activity의 정보를 시각화한 것에 가깝고, 별도 설치 없이 클릭 한 번으로 켤 수 있다. Aurora도 거의 동일하다. GCP의 AlloyDB는 **System Insights**라는 비슷한 도구를 들고 있고, Cloud SQL은 Query Insights라는 이름으로 같은 자리를 채운다. Azure는 Query Performance Insight. 매니지드 PG의 가장 큰 이점 중 하나가 이런 옵저버빌리티 도구의 기본 탑재다.

그렇다면 매니지드를 쓰면 postgres_exporter는 필요 없는가. 답은 "필요할 수 있다"다. **벤더 도구는 벤더 콘솔 안에서만 본다.** 우리 자체 Grafana에 PG 메트릭을 다른 인프라(애플리케이션, 캐시, Kubernetes 등)와 함께 한 대시보드로 보고 싶다면, postgres_exporter를 매니지드 PG 앞에 띄우는 편이 낫다. 매니지드 PG는 외부에서 stat 뷰 SELECT가 가능하므로, exporter를 별도 컨테이너로 띄우면 같은 방식으로 동작한다. **벤더 콘솔과 자체 Grafana는 보완적이지 대체적이지 않다.** 어느 한쪽만 두지 말자.

## 마무리

여기까지 왔다. 풀러 셋(PgBouncer, Pgcat, Odyssey)을 고르는 기준을 잡았고, transaction pooling의 함정 여섯 가지를 한 표로 정리했다. 그리고 모니터링은 pg_stat_statements 한 줄로 시작해서 auto_explain·pg_stat_monitor·pg_stat_kcache로 깊어지고, postgres_exporter → Prometheus → Grafana로 시각화·알람화되는 흐름을 따라갔다.

기억해두자. 풀러 선택의 핵심은 **"우리 워크로드가 어떤 세션 상태에 의존하는가"**다. transaction 모드의 효율이 매력적이라고 무작정 켜면, 어느 날 prepared statement·advisory lock·SET LOCAL이 조용히 무너진다. 그 결정 전에 워크로드의 의존성을 한 번은 정직하게 점검하는 편이 낫다. 한 풀러로 모든 워크로드를 통일하려는 욕망이 사고의 단골 원인이라는 사실도 잊지 말자. OLTP transaction 풀과 LISTEN/advisory lock용 session 풀을 갈라놓는 패턴이 그래서 안전하다.

그리고 모니터링의 첫 한 줄은 **`shared_preload_libraries = 'pg_stat_statements'`**다. 다른 모든 것은 그 위에서 자라난다. 새 클러스터를 부팅할 때마다 이 한 줄이 빠져 있지 않은지 확인하자. 거기에 `pg_monitor` role을 부여한 exporter 사용자를 만들고, postgres_exporter 컨테이너 하나를 띄워두면 — 운영 가시성의 기반은 첫날에 잡힌다. 그 기반 위에서 알람을 여섯 개 걸고, 대시보드 템플릿 하나를 가져다 우리 색으로 칠하면 — 그것이 우리가 만들 PG 운영의 출발점이다.

운영 가시성을 갖춘 PG 클러스터의 모습이 손에 잡혔다. 다음 장은 그 위에서 한 차원 더 나간 질문으로 간다. 가시성이 있다는 말은 "무엇이 잘못되고 있는지 본다"는 뜻이지만, 본다고 해서 자동으로 안전해지는 건 아니다. **누가 무엇을 볼 수 있는가, 누가 무엇을 바꿀 수 있는가, 사고가 났을 때 그 발자국을 어떻게 추적할 것인가** — 보안과 감사의 영역이다. 22장에서 이어가자.
