# 14장. FDW·CDC·동기화 — 데이터 경계를 허무는 법

회사의 데이터 지형도를 한 장 그려보자고 해보자. 메인 OLTP는 MySQL 8, 결제 원장은 오래된 Oracle, 상품 카탈로그는 어느새 MongoDB에 들어가 있고, 로그·분석은 ClickHouse, 이벤트는 Kafka로 흐른다. 거기에 누군가 "AI 검색에 벡터 인덱스가 필요하다"는 말을 꺼낸다. 자, 화이트보드 위에 화살표가 몇 개 그어질까. 다섯? 일곱? 어느새 화살표가 거미줄처럼 얽힌다.

데이터가 여러 DB로 흩어진 회사에서 일해본 사람은 안다. 한쪽에서 다른 쪽으로 데이터를 옮기는 일이 얼마나 번거로운지. 평소에는 잘 굴러가다가도, 한쪽 스키마가 살짝 바뀌거나 네트워크가 한 번 끊기는 순간 파이프라인 어디선가 사일런트 오류가 쌓이기 시작한다. 어느 날 분석팀에서 "지난주 매출 숫자가 이상하다"는 메시지가 오면, 누가 어디서부터 풀어줘야 할지 한참 막막하다.

그런 회사들이 점점 PostgreSQL을 데이터 허브로 세우기 시작했다. 메인 DB로 쓰는 김에, 다른 시스템과의 경계를 PG가 흡수하게 만드는 패턴이다. 한쪽에는 FDW(Foreign Data Wrapper)로 외부 DB를 마치 내 테이블처럼 끌어들이고, 다른 한쪽에는 logical replication으로 PG 안의 변경을 외부로 흘려보낸다. 들어오는 길과 나가는 길이 모두 PG의 표준 도구 위에서 돌아가니, 거미줄이 그래도 한결 단정해진다.

이 장에서는 그 두 길을 차례로 따라가본다. postgres_fdw로 시작해 80개가 넘는 FDW 카탈로그를 살펴보고, Debezium CDC와 17에서 새로 들어온 failover slot까지 본다. 마지막에는 pglogical과 내장 logical replication 사이의 미묘한 경계도 짚는다. 시작은 가장 친숙한 곳, 같은 PG끼리 잇는 postgres_fdw다.

## 14.1 postgres_fdw — 다른 PG를 외부 테이블로

상황을 하나 가정해보자. 사내에 PG 클러스터가 두 개 있다. 하나는 주문 시스템, 다른 하나는 회원 시스템이다. 어느 날 마케팅팀에서 "가입 30일 이상 회원의 최근 구매 내역을 뽑아달라"고 한다. 평소라면 어떻게 처리할까? 회원 시스템에서 조건에 맞는 user_id 목록을 뽑아 CSV로 떨군다. 그 CSV를 주문 시스템 DB에 적재한다. 그 임시 테이블과 주문 테이블을 조인한다. 결과를 또 CSV로 떨군다. 마케팅팀 슬랙에 올린다.

번거롭다. 단발성이면 참고 하겠지만, 이런 요청이 주 단위로 반복되면 어느 순간 누군가가 "그냥 두 DB를 합쳐버리자"는 말을 꺼낸다. 그건 더 끔찍한 일이다. 합치는 순간 결제 시스템 장애가 회원 시스템까지 끌고 들어간다. 분리해놓은 데에는 이유가 있다.

`postgres_fdw`는 이 두 극단 사이의 답이다. 다른 PG 클러스터의 테이블을 내 DB에서 마치 로컬 테이블처럼 SELECT·INSERT·UPDATE·DELETE할 수 있게 해준다. 합치지는 않되, 연결만은 표준 SQL로 잇는다.

### 설치와 첫 연결

확장으로 들어있다. 따로 컴파일할 필요 없이 켜기만 하면 된다.

```sql
CREATE EXTENSION postgres_fdw;
```

다음으로 외부 서버를 등록한다. 마치 코드에서 데이터 소스를 정의하듯, FDW에도 "어디로 접속할지"를 한 번 적어둔다.

```sql
CREATE SERVER member_db
  FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS (
    host 'member-pg.internal',
    port '5432',
    dbname 'members'
  );
```

그리고 사용자 매핑이다. 어느 로컬 유저가 어느 원격 계정으로 들어갈지를 정한다.

```sql
CREATE USER MAPPING FOR app_user
  SERVER member_db
  OPTIONS (user 'read_only', password 'xxxx');
```

이제 외부 테이블을 만들 차례다. 한 줄씩 직접 적어줘도 되지만, 원격 스키마를 통째로 끌어오는 편이 편하다.

```sql
IMPORT FOREIGN SCHEMA public
  LIMIT TO (users, user_profiles)
  FROM SERVER member_db
  INTO mirror;
```

`mirror.users`라는 외부 테이블이 생긴다. 평범한 SELECT가 그대로 통한다.

```sql
SELECT u.email, o.total
  FROM orders o
  JOIN mirror.users u ON u.id = o.user_id
 WHERE o.created_at >= now() - interval '30 days';
```

겉으로만 보면 그저 평범한 조인이지만, 내부에서는 외부 PG와 네트워크 RPC를 주고받으며 결과를 끌어오는 중이다. 표준 SQL 한 줄이 통신·직렬화·매핑까지 다 감춰주니, 애플리케이션 입장에서는 두 DB의 경계가 거의 보이지 않는다.

### push-down — 성능의 핵심

여기까지만 보면 "그냥 ODBC 같은 거 아닌가" 싶을 수 있다. 그런데 postgres_fdw의 진짜 가치는 **push-down**에 있다. 평범한 ODBC 드라이버는 원격 데이터를 전부 가져와 로컬에서 필터·조인을 한다. 그러면 작은 결과를 위해 거대한 raw 데이터를 네트워크로 끌어와야 한다. 번거롭고 느리다.

postgres_fdw는 다르다. WHERE 절·ORDER BY·LIMIT·집계 함수까지 가능한 만큼 원격에서 미리 처리하라고 요청한다. 같은 PG끼리 말이 통하니, 거의 모든 표준 연산이 원격에서 끝나고 PG는 결과만 받아온다.

EXPLAIN으로 확인하는 습관을 들여두는 편이 낫다.

```sql
EXPLAIN (VERBOSE, COSTS OFF)
SELECT count(*) FROM mirror.users WHERE created_at >= '2026-01-01';
```

출력에 `Foreign Scan`이 보이고, `Remote SQL`에 `WHERE created_at >= ...`까지 그대로 박혀 있다면 push-down이 잘 된 것이다. 만약 `Remote SQL`이 그냥 `SELECT ... FROM public.users`로만 끝나 있고, 필터가 로컬에서 다시 도는 모양이라면, 원격에서 추론 못한 표현식이 끼었을 가능성이 높다. 그럴 때는 SQL을 살짝 다듬어보자.

조인도 마찬가지다. 같은 외부 서버에 있는 두 테이블끼리 조인하면 PG 9.6 이후로는 조인 자체를 원격에 위임한다. 이걸 join push-down이라고 한다. 그런데 한쪽 테이블이 로컬, 다른 한쪽이 원격이면 어쩔 수 없이 PG가 두 결과를 받아서 자기 자리에서 합친다. 이때 자주 부닥치는 함정이 "원격 테이블 통계가 비어 있다"는 점이다. ANALYZE를 외부 테이블에 직접 걸어주자.

```sql
ANALYZE mirror.users;
```

이 한 줄을 빼먹으면 PG의 planner가 "원격 테이블이 1000 row쯤 되겠지"라는 너무 낙관적인 추정으로 끔찍한 실행 계획을 짠다. 4억 row 테이블을 nested loop로 돌리는 광경을 본 적이 있다면, 그 출처는 십중팔구 ANALYZE 누락이다.

### 트랜잭션 경계의 진실

여기서 한 가지 솔직하게 짚고 가자. postgres_fdw로 여러 외부 서버에 쓰기를 동시에 한다고 해보자. 한쪽이 성공하고 다른 쪽이 실패하면 어떻게 될까? PG는 기본적으로 **두-단계 커밋(2PC)을 자동으로 해주지 않는다**. 각 외부 서버에 대해 별도 트랜잭션이 열리고, 메인 트랜잭션이 커밋될 때 외부 트랜잭션도 차례로 커밋된다. 그 사이에 외부 서버 하나가 죽으면, 이미 커밋된 쪽과 못 한 쪽이 갈리면서 데이터가 어긋난다.

그래서 postgres_fdw는 "읽기 중심" 또는 "단일 외부 서버 쓰기"에 무게가 실린다. 정말 강한 일관성이 필요한 분산 쓰기라면, FDW가 아니라 애플리케이션 레벨에서 saga 패턴 같은 보상 트랜잭션을 설계하거나, 차라리 단일 PG로 정규화하는 편이 안전하다. 이 경계를 흐려놓고 "트랜잭션 됩니다"라고 영업하면 운영팀이 한밤중에 깨어나야 한다.

### 운영 옵션 — 한 번쯤 들여다볼 만한 손잡이

postgres_fdw에는 깊이 파고들지 않으면 잘 안 보이는 옵션이 몇 개 있다. 운영을 어느 정도 해본 뒤 한 번씩 들여다보면 좋다.

`fetch_size`는 한 번의 round-trip에 몇 row를 받아올지를 정한다. 기본값은 100이다. 적은 row를 자주 받으면 latency가 누적된다. 한 번에 많이 받으면 메모리가 늘어난다. 큰 결과 집합을 자주 다룬다면 1000·5000으로 올려보자. EXPLAIN(ANALYZE)에서 외부 스캔 시간이 줄어드는 모습이 보이면 효과가 있는 것이다.

```sql
ALTER SERVER member_db OPTIONS (SET fetch_size '1000');
```

`use_remote_estimate`도 기억해두자. 기본값은 `false`다. 그러면 PG는 원격 테이블의 비용을 자기 통계로만 추정한다. `true`로 바꾸면 매번 원격에 EXPLAIN을 보내 실제 비용을 묻는다. 정확도가 올라가지만 plan 시간이 늘어난다. 운영 OLTP라면 false로 두고 ANALYZE를 잘 챙기는 편이 낫고, 분석 쿼리 위주라면 true가 도움이 된다.

`async_capable`은 PG 14 이후의 비동기 외부 스캔 옵션이다. 여러 외부 서버를 동시에 스캔할 때, 한 서버의 응답을 기다리는 동안 다른 서버에 미리 요청을 던진다. shard fan-out 패턴에서 응답 시간을 절반 가까이 깎는다. 외부 서버를 만들 때 한 번 켜두면 그만이다.

```sql
CREATE SERVER shard_1
  FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS (host '...', port '5432', dbname '...', async_capable 'true');
```

`keep_connections`는 외부 서버와의 커넥션을 세션 종료까지 유지할지를 정한다. 기본값 `true`. 한 세션에서 외부 테이블을 여러 번 조회한다면 그대로 두자. 커넥션 풀러를 PG 앞에 두고 transaction pooling을 쓰는 환경이라면 살짝 미묘해진다. 한 번 트랜잭션이 끝나면 풀러가 새 백엔드에 트랜잭션을 묶을 수 있는데, 그 백엔드가 원격 커넥션을 처음부터 다시 만든다. 그게 누적되면 외부 서버 쪽 max_connections를 위협한다. 의심스러우면 `keep_connections=false`로 두고 외부 서버 쪽 PgBouncer를 통한 풀링도 함께 고려하자.

### 어디까지가 FDW의 자리인가

정리해보자. postgres_fdw가 빛나는 자리는 대체로 이런 모양이다.

- **읽기 중심의 통합 쿼리** — 한 화면에 회원·주문·정산을 합쳐 보여주는 백오피스, 분석 대시보드
- **임시 데이터 이동** — ETL 도구를 따로 세우기 부담스러운 단발 마이그레이션
- **마이크로서비스 간 경계 조회** — 도메인은 분리하되, 운영팀이 가끔 cross-DB 조회를 해야 하는 경우
- **shard fan-out의 시발점** — 같은 스키마를 가진 여러 PG에 데이터를 나눠 두고, 게이트웨이 PG에서 union all로 묶기

반대로 무리하는 자리는 이렇다.

- 초당 수천 건 쓰기를 여러 외부 서버에 분산하는 OLTP — 2PC 부재가 발목 잡는다
- 외부 서버가 PG가 아닌 OLAP 엔진인데 raw 데이터까지 다 끌어와 로컬에서 조인 — push-down이 안 통한다
- 외부 네트워크 RTT가 100ms 넘는 원거리 클러스터 — 한 쿼리당 round-trip이 누적된다
- 강한 일관성이 필요한 분산 쓰기 — saga나 단일 DB 정규화가 더 정직한 답

여기서 한 가지 솔직한 조언을 덧붙이자. postgres_fdw는 마치 만능 칼처럼 보이지만, 실제로는 **"DB 경계를 흐릿하게 만들어도 좋은 자리"와 "경계를 또렷이 유지해야 할 자리"를 구분하는 감각**이 운영 비용을 결정한다. 모든 cross-DB 조회를 FDW로 풀려고 들면, 어느 순간 PG가 여러 외부 서버의 부하를 한 자리에서 받아 자기 자원이 동난다. 비싼 cross-DB 조회는 야간 배치로 돌리고, 그 결과를 materialized view로 저장해두는 패턴이 운영자에게 친절하다.

다음 절에서는 postgres_fdw 한 종류만으로 부족할 때 — 그러니까 MySQL·Oracle·Mongo·Kafka 같은 이종 DB를 함께 묶고 싶을 때 — 어떤 카탈로그가 기다리고 있는지를 둘러본다.

## 14.2 80+ FDW 카탈로그 — MySQL, Oracle, Mongo, Kafka, ClickHouse, DuckDB

PG의 FDW 생태계가 80개를 넘긴다는 통계가 한동안 떠돌았다. 정확한 숫자는 매년 바뀌지만, 본질은 변하지 않는다. **"PG 안에서 외부 시스템을 표준 SQL로 본다"는 약속이 거의 모든 흔한 데이터 소스에 대해 구현되어 있다.** 이 카탈로그가 PG를 데이터 허브로 세우는 출발점이다.

전부 다 외울 필요는 없다. 자주 만날 만한 것들을 큰 묶음으로 보자.

### 이종 RDB — MySQL, Oracle, SQL Server

`mysql_fdw`는 가장 오래 쓰인 대표 주자다. MySQL의 변경된 데이터를 PG에서 외부 테이블로 보고, 마이그레이션 dual-run 기간에 양쪽을 잇는 도구로 자주 쓰인다. 다만 push-down 범위가 postgres_fdw만큼 풍부하지는 않다. 같은 PG끼리는 거의 모든 표준 표현이 원격에서 처리되지만, 이종 RDB로 가면 함수 호환성 문제 때문에 일부 필터가 로컬로 떨어진다.

`oracle_fdw`는 사실상 Oracle→PG 마이그레이션의 표준 도구다. Oracle 클라이언트 라이브러리(Instant Client)가 컴파일 시점에 필요하다는 점이 진입 장벽이지만, 한 번 설정해두면 Oracle 쪽 NUMBER·DATE·CLOB 같은 까다로운 타입까지 자동 매핑해준다. Oracle을 PG로 옮기는 17장의 마이그레이션 시나리오에서, dual-run 기간 동안 PG 안에서 Oracle 테이블을 그대로 비교 쿼리로 검증하는 데 자주 쓰인다.

`tds_fdw`는 SQL Server와 Sybase를 묶는다. Microsoft 진영에서 PG로 데이터를 끌어올 때 첫 후보가 된다.

### 문서·검색 — MongoDB, Elasticsearch

`mongo_fdw`는 MongoDB의 컬렉션을 PG에서 외부 테이블로 본다. document → row 매핑이 자동은 아니다. PG 쪽에 어떤 컬럼으로 받을지를 명시해야 한다. 그래서 스키마가 천차만별인 컬렉션을 끌어오려면 jsonb 컬럼 하나로 통째로 받아 GIN 인덱스를 거는 패턴이 자주 쓰인다.

흥미로운 점은, MongoDB→PG 마이그레이션 시나리오에서 종종 `mongo_fdw`로 점진적 이전을 한다는 것이다. PG 안에 운영 테이블을 새로 만들어두고, 일정 기간 동안 MongoDB의 변경을 PG로 흘려보내며 양쪽을 비교한다. 이전 검증이 끝나면 애플리케이션의 데이터 소스 한 줄만 바꿔서 cutover한다. 비교적 안전한 마이그레이션 패턴이다.

`multicorn`이라는 메타 FDW도 있다. Python으로 FDW를 짤 수 있게 해주는 프레임워크인데, "공식 FDW가 없는 시스템을 빠르게 잇고 싶다"는 상황에서 효자다. Elasticsearch FDW도 multicorn 기반 구현이 여럿 돌아다닌다.

### 메시지·스트림 — Kafka, Redis

`kafka_fdw`는 살짝 결이 다르다. Kafka 토픽을 외부 테이블로 보고 SELECT로 메시지를 읽는다. 메시지 큐를 SQL로 들여다본다는 발상이 묘하게 매력적이다. 다만 메시지를 한 번 읽으면 offset이 어떻게 관리되는지가 구현체마다 다르니, 운영에 들이기 전에 그 부분을 꼼꼼히 확인해야 한다. 단순 모니터링·디버깅용으로 쓰는 편이 안전하고, 진짜 컨슈머 역할은 다른 도구에 맡기는 게 좋다.

`redis_fdw`도 비슷하다. Redis의 키 공간을 테이블처럼 본다. 캐시 진단이나 운영 데이터 점검에는 쓸 만하지만, OLTP 경로에 끼우는 도구는 아니다.

### 분석·컬럼·파일 — ClickHouse, DuckDB, Parquet

여기서부터가 최근 흐름이다. PG를 OLTP의 중심에 두고, 분석은 다른 컬럼 엔진에 맡기되, **그 엔진을 마치 PG의 한 부분처럼 보이게 만든다**.

`clickhouse_fdw`는 ClickHouse의 거대한 팩트 테이블을 PG에서 SELECT하면, 가능한 한 필터·집계까지 ClickHouse에 위임한다. PG 쪽 OLTP 테이블과 ClickHouse 팩트를 조인하는 시나리오도 가능은 하지만, 그건 추천하지 않는다. 카디널리티 차이가 너무 커서 plan이 거의 항상 깨진다. 보통은 ClickHouse 쪽에 집계를 끝내라고 시키고, PG에서는 그 결과만 받는다.

`pg_duckdb`는 더 흥미롭다. DuckDB의 벡터 분석 엔진을 PG 프로세스 안에 임베드한다. 외부 시스템과 통신할 필요가 없다. PG 안에서 S3 위의 Parquet·Iceberg·Delta Lake를 그대로 조회할 수 있다. ClickBench에서 한 쿼리가 1500배 빨라졌다는 보고도 있다. 분석 워크로드를 위해 ClickHouse를 따로 세우기 망설여진다면, pg_duckdb를 먼저 검토해볼 만하다. (15장에서 더 다룬다.)

`parquet_fdw`·`file_fdw` 같은 파일 기반 FDW도 잊지 말자. data lake에 떨어뜨려둔 Parquet을 PG에서 SELECT 한 번으로 끌어오면, 별도 ETL 없이 보고서 한 장이 나온다. 작은 회사일수록 이 조합이 ROI가 크다.

### FDW의 품질 — 다 같은 FDW가 아니다

80개라는 숫자에는 솔직한 진실이 하나 숨어 있다. **모든 FDW가 같은 수준으로 잘 관리되지는 않는다.** 어떤 건 PG 코어 팀이 사실상 보증한다(postgres_fdw, file_fdw). 어떤 건 큰 회사가 지속적으로 유지한다(oracle_fdw, mysql_fdw, mongo_fdw). 어떤 건 한 사람의 사이드 프로젝트로 출발해 그 사람이 떠나면 정체된다. 운영에 들이기 전에 다음을 확인하는 편이 낫다.

- **최근 커밋 시점.** GitHub에서 한 번 들여다본다. 마지막 커밋이 2년 전이라면 PG 새 버전에서 안 빌드될 가능성을 미리 본다.
- **지원 PG 버전 범위.** PG 14에서만 테스트됐다고 README에 적혀 있으면, PG 17로 올릴 때 어디선가 깨질 수 있다.
- **push-down 지원 범위.** 문서에 명시되어 있지 않으면, 작은 샘플로 EXPLAIN을 직접 찍어보자. 모든 WHERE가 로컬로 떨어진다면 운영 OLTP에는 쓰기 어렵다.
- **트랜잭션 모델.** 쓰기를 지원한다고 적혀 있어도, 정확히 어떤 격리수준에서 어떤 보장이 있는지 명시되지 않은 경우가 많다.
- **인증·암호화.** 외부 시스템과의 통신이 평문이라면 사내망이라도 짚어둬야 한다.

이게 별일 아닌 듯 보여도, 어느 날 메인 OLTP 쿼리 한 줄이 잘 안 도는 FDW 때문에 무너지는 광경을 보면 그 5분의 사전 확인이 얼마나 값진지 새삼 느낀다.

### 카탈로그를 어떻게 활용할까

리스트만 봐서는 그저 도구의 나열로 보인다. 실제로는 다음과 같은 의사결정으로 쓰는 편이 낫다.

**시나리오 A — 이종 RDB가 섞인 마이그레이션 기간.** PG가 목적지라면, 출발지 DB에 맞는 FDW(mysql_fdw·oracle_fdw·tds_fdw)를 PG에 설치한다. dual-run 기간에 PG 안에서 양쪽을 비교하는 쿼리를 직접 돌릴 수 있다. 17장에서 다룰 마이그레이션 시나리오의 가장 든든한 도구 중 하나다.

**시나리오 B — 백오피스의 통합 조회.** 메인 서비스 DB는 PG, 정산은 외부 SaaS의 PG, 회원은 또 다른 PG. 각각을 postgres_fdw로 끌어오면, 백오피스 한 화면에서 cross-DB 리포트를 자연스럽게 만들 수 있다. 굳이 데이터 웨어하우스를 별도로 세우지 않아도 된다.

**시나리오 C — OLTP + OLAP 혼합.** PG에 OLTP, ClickHouse나 pg_duckdb에 분석. SELECT 한 줄로 양쪽을 잇되, 무리한 조인은 피한다. 사용자에게는 "PG 한 곳에 물으면 다 답한다"는 인상을 주는 패턴이다.

**시나리오 D — 임시 통합.** "한 번만 묶어 보고 싶다"는 요청에는 file_fdw나 parquet_fdw로 빠르게 끝낸다. 새 인프라를 안 세우는 것이 답일 때가 있다.

기억해두자. FDW의 가치는 "어떤 DB든 다 된다"가 아니라, **"PG의 표준 SQL과 트랜잭션 모델 안으로 외부를 끌어들인다"**는 데 있다. 그 약속이 깨지는 자리(2PC 부재, push-down 한계, 잘못된 통계)를 미리 알고 쓰는 사람이 FDW를 잘 다루는 사람이다.

지금까지 본 FDW는 "들어오는 길"의 이야기였다. 그렇다면 PG 안에서 일어난 변경을 외부로 흘려보내고 싶다면? 이제 CDC, 그러니까 Change Data Capture의 차례다.

## 14.3 Debezium PostgreSQL CDC — pgoutput vs wal2json 선택

상황 하나를 더 가정해보자. PG에 회원·주문·결제 테이블이 있다. 마케팅팀에서는 Elasticsearch로 그 데이터를 실시간 검색하고 싶어 한다. 분석팀은 ClickHouse로 받아 시계열 대시보드를 만들고 싶어 한다. 머신러닝팀은 같은 데이터를 BigQuery로 옮겨 학습 파이프라인에 태우고 싶어 한다. 모두 같은 변경 사건을 보고 싶다.

방법 하나는, 애플리케이션이 매번 PG에 쓸 때마다 Elasticsearch·ClickHouse·BigQuery에도 같은 데이터를 같이 쓰는 것이다. 자, 끔찍하다. 한 군데라도 실패하면? 트랜잭션 경계가 깨진다. 한 군데가 느리면? PG 응답까지 느려진다. 외부 시스템 하나 추가될 때마다 애플리케이션을 또 고쳐야 한다. 이 길은 답이 아니다.

PG가 이미 한 번 일을 했다. 트랜잭션의 결과를 WAL에 적어두지 않았는가. **그 WAL을 외부에서 다시 읽으면, 같은 사건을 여러 컨슈머가 자기 속도로 가져갈 수 있다.** 애플리케이션은 하나의 PG에만 쓰면 되고, 외부 시스템은 WAL에서 자기에게 필요한 변경만 골라 받는다. 이 발상이 PostgreSQL CDC의 핵심이다.

### Logical decoding — CDC의 토대

PG에는 두 종류의 복제가 있다. **physical replication**은 WAL을 byte-by-byte로 복제한다. standby가 primary의 거울이 된다. 복구·HA에는 안성맞춤이지만, 외부 시스템이 소비하기엔 너무 raw하다.

**logical decoding**은 그 WAL을 한 번 풀어서 "INSERT 했음, 어떤 row를", "UPDATE 했음, 무엇을 무엇으로" 같은 의미 있는 사건으로 다시 만들어 외부에 흘려보낸다. 9.4부터 들어 있다. PG의 CDC, Debezium, pglogical, Sequin·Decodable 같은 SaaS CDC 도구가 전부 logical decoding을 토대로 한다.

켜는 데는 두 가지 설정이 필요하다.

```ini
# postgresql.conf
wal_level = logical
max_replication_slots = 10
max_wal_senders = 10
```

`wal_level = logical`은 WAL에 "logical decoding이 풀어 쓸 수 있는 추가 정보"를 함께 기록하라는 뜻이다. WAL이 살짝 더 커진다. 슬롯은 컨슈머마다 하나씩이라 보면 된다. Debezium 1대, 사내 다른 컨슈머 1대를 쓰면 슬롯이 두 개 필요하다.

이 설정을 바꾸려면 PG를 재시작해야 한다. 운영 PG라면 정기 점검 윈도우에 같이 묶어 처리하는 편이 낫다.

### Publication과 Replication Slot

logical decoding을 쓰려면 두 개념이 필요하다. **publication**은 "어떤 테이블을, 어떤 종류의 변경 사건을 외부에 공개할지"를 선언한다. **replication slot**은 "어디까지 컨슈머가 읽었는지"를 PG가 기억해두는 북마크다.

```sql
-- 어떤 테이블을 외부에 공개할지
CREATE PUBLICATION cdc_pub FOR TABLE users, orders, payments;

-- 컨슈머의 북마크 자리
SELECT pg_create_logical_replication_slot('debezium_slot', 'pgoutput');
```

여기서 한 가지 위험을 짚고 가자. **슬롯은 한 번 만들면, 외부 컨슈머가 잘 따라오든 말든 PG는 그 위치 이후의 WAL을 절대 지우지 않는다.** 컨슈머가 죽어 한 달 동안 안 따라오면, 한 달치 WAL이 디스크에 그대로 쌓인다. 그 사이에 PG는 평소처럼 트랜잭션을 받고, WAL은 계속 늘어난다. 어느 날 새벽, 디스크가 99%를 찍고 PG가 멈춘다. 끔찍한 일이다.

그래서 운영 시작과 동시에 슬롯의 lag을 모니터링해야 한다.

```sql
SELECT slot_name,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)) AS lag
  FROM pg_replication_slots;
```

이 lag이 의심스럽게 커지면 컨슈머 쪽에 알람을 보내자. PG의 디스크가 사고 나기 전에 알아채는 것이 운영 비용의 절반을 결정한다.

### Output plugin — wal2json vs pgoutput

여기서 흔한 갈림길이 나온다. logical decoding이 풀어쓴 사건을 어떤 형식으로 외부에 보낼까? PG는 **output plugin**이라는 슬롯을 두고, 형식을 플러그인 단위로 갈아 끼울 수 있게 만들었다. 두 가지가 사실상 표준이다.

**wal2json**은 그 이름대로 JSON으로 변경 사건을 토해낸다. PG 9.4부터 가장 오랫동안 쓰여온 외부 플러그인이다. JSON이라 사람이 눈으로 읽기 쉽고, Debezium이 아닌 자체 컨슈머를 짤 때 진입 장벽이 낮다. 카카오 클린플랫폼처럼 직접 컨슈머를 만든 케이스에서는 wal2json이 자주 선택된다.

```json
{
  "change": [
    {
      "kind": "update",
      "schema": "public",
      "table": "users",
      "columnnames": ["id", "email", "updated_at"],
      "columntypes": ["bigint", "varchar", "timestamp"],
      "columnvalues": [42, "new@example.com", "2026-05-18 10:23:11"],
      "oldkeys": {
        "keynames": ["id"],
        "keytypes": ["bigint"],
        "keyvalues": [42]
      }
    }
  ]
}
```

장점: 직관적, 디버깅 쉬움, 자체 컨슈머에 친화. 단점: JSON이라 페이로드가 크다. 초당 수만 건 사건이 흐르는 큰 시스템에선 직렬화·네트워크 비용이 누적된다.

**pgoutput**은 PG 10부터 PostgreSQL 본체에 **내장된** output plugin이다. logical replication을 위해 PG가 직접 만든 바이너리 프로토콜이다. 외부 설치가 필요 없다. RDS·Aurora·Cloud SQL 같은 매니지드 PG에서도 기본으로 켜져 있다. 페이로드가 압축되어 있어 효율이 좋고, PG 본체가 같이 업그레이드하므로 호환성 걱정이 작다.

장점: 매니지드 PG에서 그대로 됨, 효율 좋음, PG 본체와 함께 진화. 단점: 바이너리라 사람이 못 본다. 컨슈머 쪽 라이브러리(Debezium·Sequin 등)가 디코딩을 해줘야 한다.

### 무엇을 고를까

기준은 단순하게 잡자.

| 환경 | 권장 | 이유 |
|------|------|------|
| 매니지드 PG (RDS·Aurora·Cloud SQL) | **pgoutput** | wal2json 설치가 까다롭거나 불가. pgoutput은 기본 내장 |
| 자체 운영 + 컨슈머가 Debezium | **pgoutput** | 효율 좋고, Debezium이 가장 잘 지원 |
| 자체 운영 + 자체 컨슈머 + JSON 친화 | **wal2json** | 디버깅과 컨슈머 구현 비용이 낮음 |
| 카카오 클린플랫폼 같은 직접 구현 파이프라인 | 케이스 따라 | wal2json이 진입 쉬움, 규모 커지면 pgoutput으로 이전 |

2026년 시점에서 새로 시작한다면 pgoutput이 무난한 첫 선택이다. 매니지드 PG에서 그대로 돌고, Debezium·Sequin·Decodable이 모두 pgoutput을 1급 시민으로 다룬다. wal2json은 "이미 wal2json으로 운영 중이거나, 자체 컨슈머의 JSON 의존이 강하거나, 디버깅 편의가 중요한" 자리에서 여전히 살아 있다.

### Snapshot 시점에 무엇이 일어나는가

CDC를 처음 켤 때 가장 헷갈리는 부분이 snapshot 단계다. logical replication slot을 만든 순간, PG는 "이 시점부터의 WAL을 보관해두겠다"고 표시한다. 그러나 컨슈머는 그 시점에 이미 테이블에 있는 기존 데이터를 알지 못한다. 그래서 한 번은 기존 데이터를 통째로 읽어야 한다. 이게 snapshot이다.

Debezium은 기본적으로 connector를 처음 띄울 때 자동 snapshot을 돈다. 큰 테이블이라면 몇 시간이 걸린다. 그 사이에 PG에는 새 변경이 계속 들어온다. Debezium은 snapshot을 도는 동안에도 슬롯을 통해 WAL을 따라가며, snapshot이 끝나면 그 시점부터 streaming으로 자연스럽게 넘어간다. 컨슈머가 받는 사건의 순서는 "snapshot 이벤트 → streaming 이벤트"이고, snapshot 단계의 row는 마치 모두 INSERT인 것처럼 들어온다.

여기서 한 가지 함정. **snapshot 자체가 PG에 SELECT 부하를 준다.** 큰 테이블이라면 운영 피크 시간에 시작하지 말자. 또한 snapshot은 일관성을 위해 PG의 한 트랜잭션 안에서 진행된다. 그 사이에 autovacuum이 그 트랜잭션을 가로질러 dead tuple을 회수하려 들면 막힌다. 5장에서 다룬 "long-running transaction이 가져오는 도미노"의 한 사례다. 큰 테이블의 첫 snapshot은 autovacuum lag을 잠시 키운다는 점을 알아두자.

snapshot 모드를 미세하게 제어하고 싶다면 Debezium의 `snapshot.mode`를 본다. `initial`은 기본값, `never`는 snapshot 없이 슬롯 생성 시점부터 streaming만, `when_needed`는 sink의 offset이 사라졌을 때만 다시 snapshot. 운영 중에 connector를 재시작했다고 매번 snapshot이 다시 돌면 끔찍한 일이다. `never` 또는 `when_needed`로 두는 편이 안전하다.

### REPLICA IDENTITY — 자주 빠지는 함정

CDC를 처음 켜고 며칠 지나면, 컨슈머에서 "UPDATE 사건은 오는데 변경 전 값이 비어 있다"는 호소가 올라온다. 이게 REPLICA IDENTITY 함정이다.

PG의 logical decoding은 기본적으로 UPDATE·DELETE 사건에 "어떤 row가 바뀌었는지를 식별할 정보"만 함께 보낸다. 기본값은 primary key다. 그 정도면 PK로 식별은 되니까. 그런데 사건 메시지에 "변경 전 값 전부"를 포함시키고 싶다면, 테이블별로 REPLICA IDENTITY를 FULL로 바꿔야 한다.

```sql
ALTER TABLE users REPLICA IDENTITY FULL;
```

FULL은 변경 전 모든 컬럼을 WAL에 기록한다. WAL이 커지고, autovacuum 시점에 약간 더 일이 늘어난다. 정말 필요한 테이블에만 FULL을 쓰자. 보통은 기본값(DEFAULT, 즉 PK 기준)으로 두고, 컨슈머 쪽에서 PK로 현재 상태를 조회하는 패턴이 비용 대비 합리적이다.

### Debezium의 구조 — 운영 관점에서

Debezium은 Kafka Connect 플랫폼 위에 도는 source connector다. Kafka Connect 클러스터를 따로 세우고, PG connector를 그 위에 배포한다. PG의 replication slot에서 변경 사건을 읽어 Kafka 토픽으로 흘려보낸다. 한 번 Kafka에 들어가면, Elasticsearch·ClickHouse·BigQuery·S3 어디로든 sink connector를 통해 자유롭게 분기한다. 이 아키텍처가 카카오 클린플랫폼이 택한 길이다.

운영에서 가장 자주 보는 통증 세 가지를 짚어두자.

**첫째, 슬롯 lag.** 컨슈머(Kafka Connect)가 죽으면 슬롯이 멈춘다. WAL이 디스크에 쌓인다. Connect 클러스터의 HA, 디스크 사용량 알람, 슬롯 lag 알람을 세트로 운영하는 편이 낫다.

**둘째, 스키마 진화.** PG에서 ALTER TABLE로 컬럼을 추가했다. Debezium은 그 사건을 잡아 스키마 변경 메시지로 흘려보낸다. sink 쪽이 그 변경을 잘 받아들이는지가 별개의 문제다. Elasticsearch는 동적 매핑이라 그럭저럭 견디지만, ClickHouse나 정형 sink는 사전 합의가 필요하다. 스키마 변경 정책을 사전에 정해두자.

**셋째, snapshot vs streaming의 경계.** 앞서 본 대로 snapshot은 한 번 도는 데 시간이 든다. 운영 중 connector 재기동 패턴을 정해두고, 슬롯이 살아 있는 한 snapshot을 다시 돌지 않는 방향으로 운영하자.

### 자체 컨슈머를 짤 때

Debezium이 모든 곳에서 1순위는 아니다. 작은 팀이라면 Kafka Connect 클러스터 자체가 부담일 수 있다. 그럴 때 자체 컨슈머를 직접 짜는 길도 있다.

PG의 logical decoding은 두 가지 API를 외부에 노출한다. SQL 함수 `pg_logical_slot_get_changes()`를 polling으로 부르는 방식과, **replication protocol**을 streaming으로 받는 방식이다. 운영용으로는 streaming이 답이다. polling은 호출마다 latency가 누적되고, PG 입장에선 매번 새 트랜잭션이 도는 셈이라 부하가 늘어난다.

Python에서는 `psycopg2`나 `psycopg3`가 `start_replication()` 헬퍼를 제공한다. Go에서는 `jackc/pglogrepl` 라이브러리가 가장 잘 관리된다. 이런 라이브러리가 PG의 replication protocol을 추상화해주므로, 컨슈머 본체는 "사건이 오면 무엇을 할지"의 비즈니스 로직에 집중할 수 있다.

자체 구현에서 자주 놓치는 일이 두 가지 있다.

**첫째, LSN 확정(confirmation).** 컨슈머는 사건을 받았다는 사실을 주기적으로 PG에 알려야 한다. `confirmed_flush_lsn`을 업데이트하지 않으면 슬롯이 진척되지 않고, WAL이 쌓인다. 라이브러리에 따라 자동인 곳도 있지만, 어디서 어떻게 보내는지 한 번은 짚어봐야 한다.

**둘째, sink 쪽의 idempotency.** PG는 at-least-once 보장만 한다. 페일오버·재기동·네트워크 끊김 후 같은 사건이 두 번 올 수 있다. sink가 (PK, LSN) 같은 unique key로 멱등하게 받지 않으면, 중복 INSERT가 쌓이거나 잘못된 카운터가 만들어진다.

카카오 클린플랫폼이 자체 컨슈머 라인을 택한 배경에는 "외부 의존을 줄이고, 자기 도메인에 맞는 트랜스포메이션을 자유롭게 끼우고 싶다"는 동기가 있다. Debezium도 SMT(Single Message Transform)로 어느 정도 가능하지만, 깊은 변환은 결국 컨슈머 자체를 짜는 편이 단순하다. 직접 구현의 비용을 감당할 수 있는 팀이라면 충분히 합리적 선택이다.

### CDC의 latency — 어디까지 빠른가

"CDC가 실시간이다"라는 말은 듣기에 좋지만, 실제 latency는 도구·설정·부하에 따라 다르다. 평시 자체에서는 보통 다음과 같다.

| 단계 | 평균 latency |
|------|------|
| PG 커밋 → WAL flush | 1~10ms |
| WAL → logical decoding 풀기 | 1~50ms |
| Debezium → Kafka 토픽 | 10~100ms |
| Kafka → sink connector | 10~100ms |
| sink connector → 대상 시스템 적용 | 10~수백ms |

end-to-end 100~500ms 정도가 평시 기준이고, 부하가 몰리면 초 단위로 늘어난다. "1초 안 보장"을 SLO로 잡으면 평시엔 여유롭게 충족하지만, 큰 트랜잭션·대형 ALTER TABLE·재기동 직후엔 종종 깨진다. SLO를 잡을 때 그런 예외 케이스의 시나리오를 미리 정의해두자.

지금까지가 평시 CDC의 모양이다. 그렇다면, primary가 죽으면 어떻게 될까? 페일오버가 일어나면 standby의 슬롯은 어떻게 될까? 이 질문이 17 이전과 이후의 PG를 가르는 결정적 분기점이다.

## 14.4 v17 failover slot의 의미 — 페일오버 후에도 CDC 컨슈머 생존

PG 16까지의 logical replication slot에는 한 가지 슬프고 묘한 결함이 있었다. **슬롯은 primary에만 존재하고, standby에는 따라가지 않았다.**

평소엔 문제가 없다. 문제는 페일오버다. 어느 날 새벽 primary가 죽고, Patroni가 standby를 promote한다. 새 primary가 트래픽을 받기 시작한다. 그런데 Debezium은? Debezium은 이전 primary의 슬롯을 보고 있었다. 그 슬롯은 죽은 노드와 함께 사라졌다. 새 primary에는 슬롯이 없다. WAL은 새 primary 기준으로 흐르기 시작한다.

이 순간 운영팀이 무엇을 해야 했을까?

1. Debezium connector를 중단한다.
2. 새 primary에서 슬롯을 다시 만든다.
3. 새 publication을 만든다 (없다면).
4. 어디부터 다시 읽을지를 결정한다. snapshot부터 다시? 마지막으로 sink에 들어간 시점부터? 그 시점을 어떻게 알지?
5. 그 사이에 빠진 변경 사건은 어떻게 보강할지?
6. Debezium connector를 다시 띄운다. snapshot이 끝날 때까지 몇 시간을 또 기다린다.

페일오버가 곧 CDC 파이프라인의 재구축이었다. HA를 자동화해놓고도, CDC 때문에 결국 사람이 새벽에 호출됐다. 끔찍한 일이다. 한국·해외 컨퍼런스에서 "logical replication slot의 페일오버 비호환이 CDC 운영의 가장 큰 통증"이라는 호소가 한동안 이어졌다.

PostgreSQL 17은 이 통증에 답을 내놓았다.

### Failover slot — 17이 한 일

17부터, logical replication slot이 **standby로 자동 동기화된다.** 정확히 말하면, 슬롯의 상태가 physical replication을 통해 standby에 함께 흘러간다. primary가 죽고 standby가 promote되면, 새 primary에는 이미 동일한 슬롯이 살아 있다. Debezium은 마치 아무 일도 없었다는 듯 다음 LSN부터 계속 읽는다.

켜는 법도 단순하다. 슬롯을 만들 때 `failover` 옵션을 true로 설정하면 된다.

```sql
SELECT pg_create_logical_replication_slot(
  'debezium_slot',
  'pgoutput',
  false,        -- temporary
  true,         -- two_phase
  true          -- failover (17+)
);
```

또는 SQL 표준 명령으로:

```sql
ALTER_REPLICATION_SLOT debezium_slot (failover);
```

standby 쪽에서도 한 가지 설정이 필요하다.

```ini
# standby의 postgresql.conf
sync_replication_slots = on
```

이걸 켜두면 standby의 worker가 주기적으로 primary의 슬롯 상태를 받아와 자기 노드에도 똑같이 만든다. primary에서 슬롯이 새로 생기거나 LSN이 진척되면 standby도 따라간다. promote가 일어나면, 그 순간의 슬롯 상태가 새 primary의 시작점이 된다.

### 무엇이 진짜로 바뀌는가

기술적으로 한 줄로 정리하면 "슬롯이 HA의 일부가 됐다"는 것이다. 운영 입장에서 다시 풀어보면 이렇다.

- **페일오버 = 슬롯 재구축**이 아니라, **페일오버 ≈ Debezium의 잠깐 끊김** 정도로 격이 떨어진다.
- 페일오버 후 snapshot을 다시 돌 필요가 없다. 큰 테이블의 몇 시간짜리 snapshot이 사라지면, 페일오버 자체가 두렵지 않게 된다.
- CDC를 메인 시스템과 같은 가용성 등급으로 운영할 수 있다. 17 이전엔 CDC가 늘 한 등급 낮았다.

이게 17 릴리스 노트가 "logical replication이 진짜 production-ready가 됐다"고 적은 진짜 이유다. 그 전에도 logical replication은 작동했다. 그러나 페일오버 시나리오가 사람 손을 강하게 요구하는 한, 진짜 운영자는 그걸 "production-ready"라고 부르지 않는다.

### 그래도 남아 있는 주의점

17의 failover slot이 만병통치는 아니다. 몇 가지는 여전히 신경 써야 한다.

**첫째, 비동기 standby라면 동기화 시점에 lag이 있을 수 있다.** primary가 죽기 직전에 막 생긴 슬롯 진척이 standby에 전파되지 않은 상태로 페일오버가 일어나면, 새 primary가 약간 과거의 LSN부터 다시 보내기 시작한다. Debezium은 그 부분에 대해 idempotent하게 처리하지만, sink 쪽에서 중복 사건이 들어왔을 때를 가정한 설계가 여전히 필요하다. at-least-once는 17 이후에도 변함없다.

**둘째, failover slot 호환 컨슈머가 필요하다.** Debezium은 2.6 이후로 17의 failover slot을 1급으로 지원한다. 자체 컨슈머를 짰다면, 페일오버 후 새 primary에 다시 접속해 슬롯이 살아 있음을 확인하고 이어 읽는 흐름을 직접 구현해야 한다. 라이브러리에 따라 자동인 곳도, 수동인 곳도 있다.

**셋째, sync_replication_slots는 standby 부담을 약간 늘린다.** 슬롯 동기화는 추가 worker가 주기적으로 도는 일이다. 많은 슬롯을 운영한다면 성능 영향이 측정 가능한 수준이 될 수 있다. 보통은 무시할 만하지만, 알아두자.

**넷째, 매니지드 PG의 지원 시점이 다르다.** RDS for PostgreSQL은 17.x로 올라가야 failover slot을 쓸 수 있다. Aurora PostgreSQL은 자체 분산 스토리지 모델 때문에 동작 의미가 약간 다르다(24장). Cloud SQL·AlloyDB도 17 GA 시점부터 점진 지원한다. 매니지드 PG라면 벤더 문서를 한 번 더 확인하고 활성화하자.

### 17 이전에 머물러야 한다면

운영 사정상 16 이하에 한동안 더 머물러야 한다면, 페일오버 시 CDC 복구 절차를 사전에 룬북으로 만들어두는 편이 낫다. 야간 호출 받은 사람이 그 순간에 6단계를 차분히 밟기는 힘들다. 대략 이런 모양의 룬북이다.

1. (페일오버 자체는 Patroni가 처리한다고 가정)
2. 새 primary에 SSH 또는 콘솔 접속
3. publication 존재 여부 확인 (`\dRp+`)
4. 슬롯 존재 여부 확인 (`SELECT * FROM pg_replication_slots`)
5. 없다면 슬롯 새로 생성 (`pg_create_logical_replication_slot`)
6. Debezium connector의 `database.hostname`을 새 primary로 변경
7. snapshot 모드를 결정 (`initial` vs `never` vs `when_needed`)
8. connector 재시작, 로그로 streaming 진입 확인

이 룬북을 페일오버 훈련의 일부로 포함시키자. 17로 올리고 나면 이 룬북 자체가 사라진다. 그 절감을 운영팀이 가장 먼저 체감한다.

자, 지금까지 본 logical replication 도구들 중에는 PG 본체에 들어 있는 것도, 외부 확장으로 따로 사는 것도 있다. 그 경계가 한때는 꽤 흐릿했다. 마지막 절에서는 pglogical과 내장 logical replication 사이의 경계를 정리해본다.

## 14.5 pglogical과 내장 logical replication의 경계

pglogical이라는 이름을 들으면, PG를 오래 쓴 사람은 한 번쯤 마음이 복잡해진다. 2nd Quadrant(현재 EDB)가 만든 외부 확장으로, 한때는 PG의 logical replication을 사실상 혼자 책임지던 도구였다. PG 9.4·9.5·9.6 시절, "logical replication을 진지하게 운영하려면 pglogical"이라는 말이 자연스러웠다.

그러다 PG 10이 나왔다. logical replication이 본체로 들어왔다. publication·subscription이라는 친근한 SQL 명령으로 외부에서 쉽게 쓸 수 있게 됐다. PG 11·12·13·14로 가며 그 기능이 빠르게 채워졌다. column filter, row filter, two-phase commit, parallel apply, 그리고 17의 failover slot. 한때 pglogical만 줄 수 있던 능력이 하나씩 본체로 들어왔다.

### 지금 시점의 정직한 정리

2026년 시점에서 새로 logical replication을 도입한다면 — 답은 단순하다. **내장 logical replication을 쓰자.**

근거는 이렇다.

- 본체에 들어 있어 설치·업그레이드가 PG와 같이 간다. 매니지드 PG에서 그대로 켤 수 있다.
- pglogical이 한때 자랑하던 기능 대부분이 본체로 흡수됐다.
- PG 코어 팀이 직접 유지보수한다. 보안 패치·성능 개선이 가장 빠르다.
- Debezium·Sequin·Decodable 등 주요 CDC 도구가 모두 내장 logical replication(pgoutput)을 1급으로 지원한다.

그렇다면 pglogical을 지금 새로 도입할 자리는 거의 없다고 봐도 좋다.

### 그래도 pglogical이 남아 있는 이유

남아 있는 이유는 크게 두 가지다.

**첫째, 옛 PG 버전을 운영하는 곳.** PG 9.4·9.6·10에 묶여 있고, 그 위에 pglogical로 logical replication 파이프라인이 돌고 있다. 이걸 어느 날 갑자기 내장으로 옮기는 일은 큰 마이그레이션이다. 보통은 메인 시스템을 PG 14·15·16으로 올리는 시점에 함께 정리한다.

**둘째, pglogical만이 깔끔하게 푸는 한두 시나리오.** 예를 들어 양방향 복제(bidirectional replication)는 본체 logical replication에서 여전히 까다롭다. pglogical은 이걸 좀 더 깔끔하게 다룬다. 다만 양방향 복제 자체가 어느 환경에서나 추천되는 모양은 아니다. 대부분의 시스템은 한 방향으로 흐르는 편이 안전하다.

### 내장 logical replication의 모양

마지막으로, 내장 logical replication을 PG 두 대 사이에서 어떻게 설정하는지만 짧게 짚어두자. 14.3에서 Debezium 같은 외부 컨슈머를 위한 슬롯 이야기를 했다면, 여기는 "PG → PG"의 이야기다.

source 쪽:

```sql
CREATE PUBLICATION app_pub FOR TABLE users, orders;
```

target 쪽:

```sql
CREATE SUBSCRIPTION app_sub
  CONNECTION 'host=source.internal port=5432 dbname=app user=replicator password=xxxx'
  PUBLICATION app_pub
  WITH (copy_data = true, failover = true);
```

이 한 줄에서 PG는 다음 일을 알아서 한다. source의 기존 데이터를 target으로 한 번 복사(`copy_data = true`)하고, 그 시점부터 source의 변경을 source의 슬롯에서 받아 target으로 흘려보낸다. target의 INSERT·UPDATE·DELETE는 source와 무관하게 흐른다. 17의 `failover = true`까지 켜두면, source 페일오버 후에도 subscription이 자동으로 새 primary를 따라간다.

마이그레이션 시나리오에 자주 쓰이는 패턴이 있다. 새 PG로 옮길 때, 한동안 양쪽을 dual-run으로 돌리고 싶다. source는 옛 PG, target은 새 PG. subscription으로 변경을 이어가면서, 양쪽 데이터를 주기적으로 비교한다. 검증이 끝나면 애플리케이션의 데이터 소스를 target으로 바꾸고, subscription을 끊는다. 이 패턴 하나만 잘 다뤄도 마이그레이션의 다운타임을 시간 단위에서 분 단위로 줄일 수 있다. (17장의 마이그레이션 시나리오에서 더 다룬다.)

### 한계와 함정 한 번 더

내장이라고 모든 게 자동으로 안전한 건 아니다. 운영자가 미리 알아두면 좋을 점들이다.

- **DDL은 복제되지 않는다.** ALTER TABLE을 source에 하면, target에도 같은 DDL을 사람이 따로 적용해야 한다. 자동 DDL 동기화는 PG 17까지도 본체 기능이 아니다. Debezium 같은 외부 도구나, 자체 마이그레이션 스크립트로 양쪽을 함께 진화시키자. 둘 사이의 스키마가 어긋난 채로 변경이 흐르면 subscription이 멈춘다. 그 순간 source의 슬롯에서 WAL이 쌓이기 시작한다.
- **시퀀스 값은 복제되지 않는다.** PK가 SERIAL이나 IDENTITY인 테이블을 dual-run으로 쓴다면, target에서 시퀀스 충돌이 일어날 수 있다. cutover 직전에 시퀀스 값을 한 번 맞춰주는 절차가 필요하다. v18에서 UUIDv7이 본체에 들어온 이유 중 하나도, 분산 시스템에서 시퀀스 충돌 자체를 사라지게 만들기 위해서다.
- **large object(LO)는 복제되지 않는다.** bytea로 충분한 곳에서 LO를 안 쓰는 편이 일반적으로 낫다.
- **대형 트랜잭션은 메모리를 누른다.** PG 14부터 streaming in-progress transaction이 도입되어 많이 완화됐지만, 수십만 row를 한 트랜잭션으로 처리하는 패턴은 여전히 publisher·subscriber 양쪽에 부담이다. 배치를 작게 쪼개는 편이 낫다.
- **TRUNCATE도 복제된다, 단 publication 옵션에 따라.** `CREATE PUBLICATION ... WITH (publish = 'insert, update, delete, truncate')`가 기본이라 TRUNCATE도 흐른다. dual-run 중에 target 데이터를 한 번 비웠다고 source의 TRUNCATE가 잘못 흘러들어 가는 사고가 종종 생긴다. 의도하지 않은 곳에선 `publish` 옵션에서 truncate를 빼두자.
- **conflict resolution은 거의 사람 몫.** target에 같은 PK가 이미 있으면 subscription이 멈춘다. PG 16부터 `disable_on_error` 옵션과 conflict 메타데이터가 늘었지만, 여전히 해결은 사람이 한다. dual-run에서 양쪽에 같은 PK를 쓰지 않도록 시작 시점부터 격리하는 편이 낫다.

### Subscription의 운영 모니터링

내장 logical replication을 켰다면, 다음 두 뷰는 알람에 묶어두는 편이 낫다.

```sql
-- publisher 쪽 슬롯의 lag
SELECT slot_name,
       active,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)) AS lag
  FROM pg_replication_slots
 WHERE slot_type = 'logical';

-- subscriber 쪽 진척과 에러
SELECT subname,
       received_lsn,
       last_msg_receipt_time,
       latest_end_lsn,
       latest_end_time
  FROM pg_stat_subscription;
```

`active = false`인 슬롯이 보이면 subscriber가 끊겼다는 신호다. lag이 일정 임계치(예: 1GB)를 넘기면 알람을 보내자. publisher의 디스크 사용량이 폭증하기 전에 알아채는 것이 운영의 절반이다.

### 내장 logical replication vs Debezium — 한 번 정리

여기까지 오면 한 가지 질문이 생긴다. "내장 logical replication이 이미 좋은데, Debezium은 왜 따로 있는 거지?"

답은 단순하다. **둘은 같은 도구가 아니다.**

| 구분 | 내장 logical replication | Debezium (logical decoding 기반) |
|------|------|------|
| 대상 | PG → PG | PG → Kafka → 어디로든 |
| 설정 단위 | publication/subscription (SQL) | Kafka Connect connector (JSON) |
| 출력 형식 | PG 내부 (target에 자동 적용) | Kafka 메시지 (Avro/JSON/Protobuf) |
| 운영 인프라 | 추가 없음 | Kafka + Kafka Connect 클러스터 |
| sink 다양성 | PG만 | Elasticsearch·ClickHouse·BigQuery·S3·... |
| 트랜스포메이션 | 없음 (row를 그대로 복사) | SMT, 컨슈머 측 커스텀 가능 |
| HA·페일오버 | 17 failover slot으로 한 자리 | Kafka Connect 자체 HA + 17 failover slot |

선택은 보통 이렇게 갈린다. **"같은 데이터를 다른 PG로만 옮긴다"면 내장이 답이고, "한 사건을 여러 종류의 sink로 뿌린다"면 Debezium(또는 비슷한 CDC 도구)이 답이다.** 둘이 같은 PG 위에서 공존하는 그림도 흔하다. publisher 한 곳에서 슬롯 둘을 만들고, 하나는 내장 subscription이 받고, 다른 하나는 Debezium이 받는다. 슬롯이 두 개라는 점만 잊지 말고 디스크 알람을 챙기자.

기억해두자. 내장 logical replication은 "표준 SQL로 외부 시스템을 끌어들이는" FDW와 함께, PG를 데이터 허브로 세우는 두 기둥이다. 한쪽은 들어오는 길, 다른 한쪽은 나가는 길이다. 14.3·14.4의 CDC가 사실 그 나가는 길의 진화된 형태였다는 점이 이제 자연스럽게 보일 것이다.

## 마무리

데이터가 흩어진 회사를 한 번 떠올려보자. PG 하나로 모든 걸 강제로 합치자는 이야기는 어디에도 없다. 메인 OLTP는 PG, 결제는 Oracle, 검색은 Elasticsearch, 분석은 ClickHouse, 머신러닝은 BigQuery — 각자 잘하는 자리에 머무는 편이 자연스럽다. 다만 그 경계를 누가 어떻게 잇느냐의 문제가 남는다.

이 장에서 본 도구들이 그 경계를 잇는 PG 쪽 답이다. **들어오는 길은 FDW가** 책임진다. 80개가 넘는 카탈로그가 거의 모든 흔한 데이터 소스를 표준 SQL 안으로 끌어들인다. push-down으로 효율을 챙기고, 2PC 부재 같은 한계를 알고 쓰면 백오피스 통합 조회·dual-run 마이그레이션·OLAP 혼합에서 거의 무엇이든 해낸다.

**나가는 길은 logical decoding이** 책임진다. wal2json과 pgoutput 중 매니지드 PG라면 pgoutput을 우선으로 본다. Debezium을 얹어 Kafka 토픽으로 흘려보내면, 한 사건이 Elasticsearch·ClickHouse·BigQuery로 자연스럽게 분기한다. 슬롯 lag 모니터링과 REPLICA IDENTITY를 미리 챙기는 사람이 운영을 잘 다루는 사람이다.

**17의 failover slot이** 이 모든 그림에 빠져 있던 한 조각을 채웠다. 페일오버 후 CDC 컨슈머가 살아남는다는 그 한 가지가, logical replication을 진짜 production 등급으로 끌어올렸다. 17 이전과 이후의 PG 운영을 가르는 결정적 분기점이라 봐도 좋다.

마지막으로, **pglogical은 옛 자리에 머물고 내장 logical replication이 표준이 됐다는** 점도 잊지 말자. 새로 시작한다면 내장을, 옛 환경을 유지해야 한다면 마이그레이션 계획에 pglogical 이전을 함께 포함시키자.

이 모든 도구가 사실 한 메커니즘 위에 서 있다는 점을 잠깐 떠올려보자. 그 메커니즘은 7장에서 봤다. WAL. PG의 모든 자랑이 WAL 하나로 거슬러 올라간다고 했다. 복제도, CDC도, PITR도 다 거기서 나온다. 14장의 도구들도 예외가 아니다. publication·slot·output plugin·subscription — 이름은 다양하지만 결국 WAL을 어떻게 풀어 쓸지의 다른 얼굴들이다.

다음 장에서는 또 다른 통합의 이야기를 한다. **분석·OLAP·시계열** — Citus와 TimescaleDB와 DuckDB가 PG 안에서 어디까지 가는지, ClickHouse를 따로 세우지 않고 어디까지 갈 수 있는지를 살펴본다. 이번 장에서 본 FDW(특히 clickhouse_fdw·pg_duckdb)가 그 자리에서 다시 한 번 빛난다. 데이터 허브 PG의 진면목은, 분석까지 어떻게 끌어안느냐에서 한층 더 분명해진다.
