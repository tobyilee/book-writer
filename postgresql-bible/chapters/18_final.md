# 18장. VACUUM과 XID wraparound — 진짜로 멈추는 사고

autovacuum을 꺼두고 싶었던 적이 있는가? 평일 오후, 대시보드의 CPU 그래프가 갑자기 70%까지 치솟고 디스크 I/O가 출렁인다. 누군가 `pg_stat_activity`를 뒤져보더니 한마디 한다. "autovacuum 워커가 거대한 테이블을 잡고 있다." 그 자리에서 누군가 또 묻는다. "이거 꺼버리면 안 되나?" 잠깐의 성능 문제 앞에서 그 유혹은 강하다. 게다가 매뉴얼에는 `ALTER TABLE ... SET (autovacuum_enabled = false)`라고 친절하게 적혀 있다. 한 줄이면 끝난다.

그런데 그 한 줄의 결정이 한 달 뒤에 클러스터를 read-only로 만든다고 해보자. 끔찍한 일이다. 그것도 야간 점검 시간이 아니라, 평일 오후의 결제 트래픽 한복판에서. 모든 쓰기 쿼리가 `ERROR: database is not accepting commands to avoid wraparound data loss in database "..."`라는 메시지를 토해낸다. 슬랙은 비명소리로 도배되고, 단톡방은 "지금 뭘 한 거냐"는 추궁으로 채워진다.

5장에서 MVCC가 왜 VACUUM을 운명처럼 데리고 다니는지를 봤다. dead tuple이 어떻게 쌓이고, table bloat가 어떻게 생기고, long-running transaction이 어떻게 도미노를 만드는지. 5장이 원리의 이야기였다면, 18장은 처방의 이야기다. autovacuum을 어떻게 길들이는가, 대용량 테이블에서 기본값이 왜 위험한가, 모니터링은 어떤 지표로 해야 하는가, 그리고 가장 무서운 XID wraparound 사고를 어떻게 예방하고 복구하는가. 마지막으로 bloat가 이미 쌓였을 때의 무중단 회수 도구까지 같이 묶었다. 5장 5.7에서 예고한 "운영에서 bloat가 어떻게 보이는가"의 답이 여기에 있다. 하나씩 풀어보자.

## 18.1 autovacuum 트리거 — threshold + scale_factor

먼저 autovacuum이 언제 동작하는지부터 정확히 짚자. 의외로 이 부분을 흐릿하게 알고 있는 사람이 많다. "자동으로 알아서 도는 거 아니에요?" 정도의 인식이면 곤란하다. autovacuum이 도는 시점은 단순한 공식 하나로 결정된다.

```
threshold = autovacuum_vacuum_threshold + autovacuum_vacuum_scale_factor × n_live_tuples
```

기본값을 대입해보자. `autovacuum_vacuum_threshold`의 기본값은 50, `autovacuum_vacuum_scale_factor`의 기본값은 0.2다. 그러니까 어떤 테이블이 1,000행을 가지고 있다면, dead tuple이 `50 + 0.2 × 1,000 = 250`개가 쌓일 때 autovacuum이 한 번 깨어난다. 작은 테이블에서는 별로 어색하지 않다.

그런데 행이 100만 개인 테이블이라면 어떻게 될까? `50 + 0.2 × 1,000,000 = 200,050`개의 dead tuple이 쌓일 때까지 autovacuum이 가만히 있는다. 1,000만 개 테이블이면 200만 개, 1억 개 테이블이면 2,000만 개의 dead tuple이 누적될 때까지 침묵한다. 한 번 깨어나면 한꺼번에 처리해야 하니 I/O가 폭발한다. 한밤중에 디스크 그래프가 절벽처럼 솟구치는 그 패턴이 바로 이 공식에서 나온다.

ANALYZE 쪽도 같은 구조다.

```
threshold = autovacuum_analyze_threshold + autovacuum_analyze_scale_factor × n_live_tuples
```

`autovacuum_analyze_threshold`는 50, `autovacuum_analyze_scale_factor`는 0.1이 기본값이다. 통계 갱신은 vacuum보다 조금 더 빈번하게 잡혀 있다. 통계가 오래되면 옵티마이저가 엉뚱한 플랜을 짜기 때문이다.

여기까지 보면 의문이 생긴다. "왜 PostgreSQL 기본값은 이렇게 보수적일까?" 답은 의외로 단순하다. PostgreSQL은 1990년대 후반부터 이어진 기본값을 큰 변동 없이 유지해 왔다. 그 시절의 "큰 테이블"은 수십만 행 정도였다. 행 수가 수십억으로 늘어난 시대에 0.2라는 비율은 너무 게으르다. 그러니까 기본값은 "안전한 출발점"이지 "운영 최적값"이 아니다. 이 둘을 혼동하지 말자.

그렇다면 어떻게 조정해야 할까? 핵심 원리는 이거다. **테이블이 크면 scale_factor를 낮추고 threshold를 키운다.** 큰 테이블일수록 비율이 아니라 절대값으로 잡는 게 합리적이다. 예를 들어 1,000만 행 이상의 큰 테이블이라면 다음처럼 잡는 편이 낫다.

```sql
ALTER TABLE orders SET (
  autovacuum_vacuum_threshold   = 10000,
  autovacuum_vacuum_scale_factor = 0.01,
  autovacuum_analyze_threshold   = 5000,
  autovacuum_analyze_scale_factor = 0.005
);
```

`scale_factor`를 0.01로 떨어뜨리면 1억 행 테이블도 100만 dead tuple 즈음에서 vacuum이 깨어난다. 1억 row 테이블에서 2,000만이 아니라 100만이다. 차이가 한눈에 보인다. 작은 단위로 자주 처리하면 한 번에 토해내는 I/O 폭발도 줄어든다.

물론 모든 테이블에 같은 값을 박는 건 곤란하다. write가 거의 없는 마스터 데이터 테이블에 일률적으로 적용하면 의미 없이 vacuum이 도는 비용만 늘어난다. 그러니까 "큰 테이블 + 쓰기 비율 높은 테이블"만 골라서 별도 튜닝하는 편이 좋다. 어느 테이블이 그런지 알아내는 건 18.3 모니터링에서 다룬다.

한 가지 더 챙길 것이 있다. `autovacuum_naptime`이다. 기본값 1분. autovacuum launcher가 1분에 한 번 모든 데이터베이스를 훑어 vacuum이 필요한지 확인한다. 데이터베이스가 100개라면 한 데이터베이스당 평균 0.6초마다 점검을 받는 셈이다. 데이터베이스가 수백 개로 늘어나면 naptime을 줄이거나 워커 수(`autovacuum_max_workers`, 기본 3)를 늘리는 편이 안전하다.

`autovacuum_max_workers`도 짚자. 기본 3이라는 숫자는 의외로 빨리 소진된다. 거대 테이블 하나가 워커 한 자리를 한참 잡고 있으면, 동시에 vacuum이 필요한 다른 테이블들이 줄서서 기다린다. CPU와 I/O 여유가 있다면 5~6 정도로 올려놓는 사이트도 많다. 단, 워커가 많아지면 그만큼 동시에 떨어지는 I/O 압박도 커진다는 점은 기억해두자.

여기에 하나 더, 의외로 자주 빠뜨리는 파라미터가 있다. `autovacuum_work_mem`이다. 기본값은 -1, 즉 `maintenance_work_mem`을 따라간다. 그런데 `maintenance_work_mem`의 기본값은 64MB. 거대 테이블의 인덱스 vacuum에서 64MB는 턱없이 부족하다. 인덱스 정리에서 메모리가 모자라면 같은 인덱스를 여러 번 스캔해야 하니, vacuum이 갑자기 몇 배로 느려진다. 메모리가 넉넉한 서버라면 `autovacuum_work_mem = 1GB` 정도로 별도로 떼주는 편이 좋다. 한 줄 바꾸는 것만으로 vacuum 시간이 절반으로 줄어드는 사이트도 있다.

그리고 한 번 더 새기자. autovacuum의 트리거 공식은 `pg_class.reltuples`(통계의 추정 행 수)를 기준으로 계산된다. 통계가 노후화되면 트리거 자체가 어긋난다. 그래서 ANALYZE를 따로 챙기는 일이 vacuum 못지않게 중요하다. "vacuum만 신경 쓰고 analyze는 안 봤다"가 의외로 흔한 함정이다.

## 18.2 대용량 테이블에서 기본값이 위험한 이유

위 공식을 한 번 더 곱씹어보자. 대용량 테이블에서 기본값이 왜 진짜로 위험한지 그림이 그려져야 한다.

1억 행짜리 주문 테이블이 있다고 해보자. 기본 `scale_factor = 0.2`라면 dead tuple이 2,000만 개 쌓여야 vacuum이 깨어난다. 하루에 50만 건의 주문이 갱신·삭제된다고 가정하자. 단순 계산으로 40일에 한 번 vacuum이 도는 셈이다. 40일치 dead tuple을 한 번에 처리하면 어떤 일이 벌어질까?

세 가지가 동시에 무너진다.

첫째, **I/O 폭발이다.** vacuum은 dead tuple을 회수하면서 페이지를 읽고, 인덱스 항목도 같이 정리한다. 2,000만 개를 한꺼번에 처리하면 디스크 read/write가 평상시의 몇 배로 뛴다. AWS RDS 같은 환경이면 burst credit이 순식간에 바닥나고, IOPS 제한이 걸리면서 전체 쿼리가 느려진다. 사용자는 "DB가 갑자기 느리네요"라고 신고하고, DBA는 그제서야 vacuum 로그를 본다. 난감하다.

둘째, **bloat의 누적이다.** dead tuple이 회수되지 못하는 40일 동안 테이블 페이지에는 빈 슬롯이 잔뜩 쌓인다. 1억 행짜리 테이블이 물리적으로는 1억 4천만 행 분량의 공간을 차지한다. 이게 바로 5장에서 말한 table bloat다. 시퀀셜 스캔이 40% 더 많은 페이지를 읽고, 인덱스 스캔도 더 많은 페이지를 거친다. 캐시 효율이 떨어지면서 똑같은 쿼리가 갑자기 두 배로 느려진다. 사용자는 "이상해요, 어제까지 멀쩡했는데"라고 말한다.

셋째, **통계의 노후화다.** ANALYZE도 같은 공식 위에 서 있다. 1억 행 테이블이라면 dead tuple이 아니라 modify count가 1,000만 개 넘게 쌓여야 통계가 갱신된다. 그 사이에 데이터 분포가 바뀌면 옵티마이저는 옛 통계로 플랜을 짠다. "원래 인덱스 스캔이던 게 갑자기 시퀀셜 스캔으로 뒤집혔다"는 사건의 8할은 통계 노후화가 범인이다.

이 세 가지가 한꺼번에 터지면 어떻게 보일까? 평소엔 멀쩡하던 시스템이 어느 날 갑자기 느려진다. 메트릭은 다 정상이라고 한다. "트래픽도 안 늘었는데 왜 이래?" CPU·메모리·네트워크 어디에도 빨간 불은 없다. 그런데 응답시간만 두 배다. 이 패턴이 바로 autovacuum이 못 따라가는 사이트의 전형이다.

여기서 잠깐, 흔한 오해 하나를 짚자. "autovacuum이 도는 동안 테이블이 잠기는 거 아닌가?" 다행히 그렇지 않다. 일반 autovacuum은 `SHARE UPDATE EXCLUSIVE` 락만 잡는다. SELECT/INSERT/UPDATE/DELETE는 그대로 진행된다. DDL이나 다른 vacuum과만 충돌한다. 그러니까 autovacuum이 트래픽 중에 도는 것 자체는 문제가 아니다. 문제는 한 번에 너무 많은 I/O를 토해내는 점, 그리고 그동안 누적된 bloat가 쿼리를 느리게 만드는 점이다.

대용량 테이블 튜닝의 또 다른 축은 **`vacuum_cost_*` 파라미터다.** autovacuum이 폭주하지 않도록 의도적으로 속도를 늦추는 장치다. 핵심은 세 개다.

- `autovacuum_vacuum_cost_delay`: 기본 2ms. 한 번 일하고 잠깐 쉬는 시간.
- `autovacuum_vacuum_cost_limit`: 기본 -1(전체 vacuum_cost_limit 200 사용). 한 사이클에 소진할 수 있는 비용 한도.
- `vacuum_cost_page_*`: 페이지를 hit/miss/dirty할 때 드는 비용 점수.

운영 상황별로 조정 방향이 다르다. I/O가 여유롭고 dead tuple을 빨리 치우고 싶다면 `cost_limit`을 올리고 `cost_delay`를 낮춘다. 반대로 vacuum이 트래픽을 죽일 정도로 무겁다면 `cost_limit`을 낮추거나 `cost_delay`를 높여 천천히 돌게 한다. PostgreSQL 12부터는 `cost_delay`가 마이크로초 단위가 아니라 밀리초 단위로 더 세밀하게 조절된다.

큰 사이트의 일반 패턴은 이렇다. 평소 운영 시간에는 `cost_limit = 1000`, `cost_delay = 10ms` 정도로 잡고, 야간에는 `cost_limit = 5000`, `cost_delay = 0`으로 풀어준다. 시간대별 autovacuum 강도를 다르게 가져가는 운영이다. 야간에 빚을 갚는 셈이다.

여기까지 정리하자. **autovacuum의 기본값은 작은 테이블 기준**이다. 큰 테이블이 있다면 `scale_factor`를 낮추고, vacuum 속도는 `cost_*` 파라미터로 별도로 통제한다. 두 축을 같이 만지는 것이 정석이다. 한쪽만 만지면 의도와 어긋난다.

한 가지 더 있다. **insert-only 테이블의 함정이다.** 로그 테이블처럼 INSERT만 일어나고 UPDATE/DELETE가 거의 없는 테이블이 있다. dead tuple이 안 쌓이니 autovacuum이 깨어날 일이 거의 없다. 그런데 freezing은 dead tuple과 무관하게 필요하다. INSERT만 일어나도 XID는 소진된다. 그래서 PostgreSQL 13부터 `autovacuum_vacuum_insert_threshold`와 `autovacuum_vacuum_insert_scale_factor`가 추가됐다. INSERT 누적량 기준으로 vacuum이 깨어나는 트리거다. 13 이전 버전을 쓴다면 insert-only 테이블에 별도 freeze 스케줄이 꼭 필요했다. 13 이상에서는 이 두 파라미터를 챙겨두자.

```sql
ALTER TABLE event_log SET (
  autovacuum_vacuum_insert_threshold = 50000,
  autovacuum_vacuum_insert_scale_factor = 0.01
);
```

이 한 줄이 없으면, INSERT만 받는 로그 테이블이 6개월 뒤에 wraparound 위험 1순위가 된다. 18.5에서 볼 사고 케이스의 변종이다. insert-only 테이블을 무시하지 말자.

## 18.3 모니터링 — n_dead_tup, last_autovacuum, n_mod_since_analyze

autovacuum을 길들이려면 먼저 보이게 만들어야 한다. PostgreSQL은 다행히 풍부한 통계 뷰를 제공한다. 그중에서 매일 들여다봐야 할 핵심 세 가지가 있다. `n_dead_tup`, `last_autovacuum`, `n_mod_since_analyze`다.

가장 먼저 들여다볼 곳은 `pg_stat_user_tables`다.

```sql
SELECT
  schemaname,
  relname,
  n_live_tup,
  n_dead_tup,
  ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup, 0), 2) AS dead_pct,
  n_mod_since_analyze,
  last_autovacuum,
  last_autoanalyze
FROM pg_stat_user_tables
WHERE n_live_tup > 10000
ORDER BY n_dead_tup DESC
LIMIT 20;
```

이 쿼리 하나면 "지금 어떤 테이블이 위험한가"가 한눈에 들어온다. 보는 법을 짚자.

**`n_dead_tup`** — 현재 회수되지 않은 dead tuple 수. 18.1 공식에서 본 threshold를 넘어서면 autovacuum이 깨어나야 한다. 그런데 이 숫자가 계속 커지는데 `last_autovacuum`이 며칠째 변하지 않는다면, autovacuum이 그 테이블을 처리하지 못하고 있다는 뜻이다. 다른 워커들이 모두 다른 거대 테이블을 잡고 있거나, long-running transaction이 dead tuple을 못 회수하게 막고 있거나, 어딘가에 문제가 있다.

**`last_autovacuum`** — 마지막으로 autovacuum이 끝난 시각. NULL이면 한 번도 자동으로 vacuum이 돌지 않았다는 뜻이다. 갓 생긴 테이블이라면 이상한 일이 아니지만, 오래된 테이블에서 NULL이라면 `autovacuum_enabled = false`로 꺼져 있는지 의심해야 한다. 이 한 줄이 18장 첫머리에서 말한 그 사고의 출발점이다.

**`n_mod_since_analyze`** — 마지막 ANALYZE 이후 누적된 수정 횟수. 이 값이 threshold를 한참 넘었는데 `last_autoanalyze`가 며칠 전이라면, 통계가 노후화됐다는 뜻이다. 옵티마이저가 엉뚱한 플랜을 짤 가능성이 높아진다.

세 컬럼을 같이 보는 게 핵심이다. `n_dead_tup`만 보면 "쌓이고는 있는데 그게 문제인지 아닌지" 알 수가 없다. `last_autovacuum`과 같이 보면 "쌓이고 있는데 처리도 안 되고 있다"가 보인다. 거기에 `n_mod_since_analyze`까지 같이 보면 "통계까지 같이 늙고 있다"가 드러난다.

조금 더 깊이 들어가면 `pg_stat_activity`로 지금 진행 중인 vacuum을 볼 수 있다.

```sql
SELECT
  pid,
  datname,
  usename,
  state,
  wait_event_type,
  wait_event,
  query_start,
  now() - query_start AS elapsed,
  query
FROM pg_stat_activity
WHERE query LIKE 'autovacuum:%'
   OR query LIKE 'VACUUM%';
```

PostgreSQL 9.6부터는 `pg_stat_progress_vacuum`이 추가됐다. 한층 더 친절하다.

```sql
SELECT
  pid,
  datname,
  relid::regclass AS table_name,
  phase,
  heap_blks_total,
  heap_blks_scanned,
  ROUND(100.0 * heap_blks_scanned / NULLIF(heap_blks_total, 0), 2) AS pct_done,
  index_vacuum_count
FROM pg_stat_progress_vacuum;
```

`phase` 컬럼이 `scanning heap`, `vacuuming indexes`, `vacuuming heap`, `cleaning up indexes` 같은 단계를 그대로 알려준다. "지금 vacuum이 어디쯤 가고 있는지" 진행률이 한눈에 보인다. 거대 테이블 vacuum이 두 시간째 돌고 있을 때 "얼마나 남았나" 묻는 사람이 있으면 이 뷰를 보여주면 된다.

그리고 vacuum이 진짜로 못 따라가고 있는지 확인하는 결정적 한 줄이 있다.

```sql
SELECT
  datname,
  age(datfrozenxid) AS xid_age
FROM pg_database
ORDER BY xid_age DESC;
```

`age(datfrozenxid)`는 해당 데이터베이스의 가장 오래된 XID와 현재 XID의 차이다. 이 숫자가 커지면 wraparound가 가까워지고 있다는 뜻이다. 자세한 이야기는 18.4에서 한다. 일단 이 숫자가 무엇인지만 기억해두자.

테이블 단위로는 `pg_stat_all_tables.relfrozenxid`를 본다.

```sql
SELECT
  schemaname,
  relname,
  age(relfrozenxid) AS xid_age,
  pg_size_pretty(pg_total_relation_size(schemaname || '.' || relname)) AS size
FROM pg_stat_all_tables s
JOIN pg_class c ON c.relname = s.relname
WHERE c.relkind = 'r'
ORDER BY age(relfrozenxid) DESC
LIMIT 20;
```

xid_age가 큰 테이블이 위험 테이블이다. autovacuum이 그 테이블에 한참 손을 못 댔다는 신호다. 이런 테이블이 발견되면 즉시 수동으로 `VACUUM (FREEZE)`를 거는 편이 안전하다.

마지막으로 운영 메트릭으로 끌어올리자. 위 쿼리들을 그대로 두면 데이터가 흩어져 의미가 없다. Prometheus + `postgres_exporter`를 깔면 `pg_stat_user_tables_n_dead_tup`, `pg_stat_user_tables_last_autovacuum`, `pg_database_xid_age` 같은 메트릭이 자동으로 수집된다. Grafana 대시보드에 다음 세 가지는 최소한 깔아두는 편이 좋다.

- 테이블별 `n_dead_tup` 추이 — 우상향 그래프가 있으면 누가 못 따라가고 있다는 신호.
- 데이터베이스별 `age(datfrozenxid)` — 2억(20만 단위 200,000,000) 넘으면 노란불, 10억 넘으면 빨간불.
- autovacuum 워커 사용률 — 항상 만석이면 워커가 부족하다.

알람 임계치도 같이 정하자. `age(datfrozenxid)`는 보수적으로 200,000,000(2억)부터 1차 알람, 500,000,000(5억)부터 2차 알람, 1,000,000,000(10억)부터 페이저 알람을 권하는 운영팀이 많다. 한참 여유로워 보이는 숫자지만, 한 번 미끄러지기 시작하면 며칠 안에 흘러간다. 이 숫자가 왜 무서운지 다음 절에서 본격적으로 풀어보자.

## 18.4 XID wraparound — 7.5개월의 시한폭탄

여기서부터가 진짜다. 이 절을 안 읽고 PostgreSQL을 운영한다는 건 안전벨트 없이 운전하는 것과 같다.

PostgreSQL은 모든 트랜잭션에 32비트 정수 ID를 발급한다. **Transaction ID**, 줄여서 XID다. 32비트면 약 42억(2^32 = 4,294,967,296)이다. 그런데 실질적으로 사용 가능한 범위는 절반인 약 21억(2^31)이다. 왜 절반만 쓰냐고? PostgreSQL의 가시성 판정은 "현재 XID 기준으로 과거인가 미래인가"로 이뤄지는데, 그러려면 한쪽으로만 비교할 수 있어야 한다. 그래서 항상 "내 XID 기준 과거 21억 ~ 미래 21억"의 원형 범위만 의미가 있다.

이 21억이라는 숫자가 의외로 빨리 소진된다. TPS가 1,000이라고 가정해보자. 초당 1,000건의 트랜잭션이 들어가면 하루에 8,640만 건이다. 21억을 8,640만으로 나누면 약 24일이다. **TPS 1,000이면 24일이면 XID가 다 떨어진다.** TPS가 100이면 240일, 약 8개월. 그래서 평균적인 사이트라면 7~8개월이 한계 시한이라는 말이 나오는 것이다.

다행히 PostgreSQL은 이 문제를 알고 있다. dead tuple 회수와 별개로, autovacuum은 **freezing**이라는 추가 작업을 한다. 충분히 오래된 row의 xmin을 특수한 "FrozenXID"(예전에는 별도 값, 9.4부터는 tuple header의 hint bit)로 표시한다. frozen tuple은 미래 어떤 XID와 비교해도 항상 보인다. 즉, XID 비교 대상에서 제외된다. 그러니 freezing이 잘 돌면 XID는 계속 재활용된다.

freezing의 트리거는 두 가지다.

- `vacuum_freeze_min_age` (기본 5천만): vacuum이 돌 때 이보다 오래된 row를 freeze.
- `autovacuum_freeze_max_age` (기본 2억): 테이블의 oldest XID 나이가 이 값을 넘으면 **강제로** autovacuum이 freeze 전용으로 도는 모드(`anti-wraparound vacuum`)에 들어간다.

핵심은 두 번째다. `autovacuum_freeze_max_age = 200,000,000`. 어떤 테이블이든 이 나이를 넘는 row를 가지고 있으면 autovacuum이 "이건 무조건 처리해야 해" 하고 강제로 들어간다. 사용자가 `autovacuum_enabled = false`로 그 테이블을 꺼뒀더라도, anti-wraparound vacuum은 무시하고 들어간다. PostgreSQL의 최후의 방어선이다.

그렇다면 왜 read-only 사고가 터질까? autovacuum이 무조건 들어가는데?

답은 anti-wraparound vacuum이 들어가더라도 끝까지 처리하지 못하는 경우가 있다는 데에 있다. 가장 흔한 원인 세 가지다.

**1. long-running transaction.** 누가 트랜잭션을 열어놓고 한 달째 커밋도 롤백도 안 하고 있다고 해보자. vacuum은 그 트랜잭션의 snapshot보다 오래된 row를 회수할 수 있다. 그런데 그 트랜잭션이 한 달 전에 시작됐다면, vacuum이 회수할 수 있는 범위가 한 달 전 시점에서 멈춘다. anti-wraparound vacuum도 마찬가지다. long-running tx 너머로는 freezing이 불가능하다. 그 사이에도 XID는 계속 소진되니, 결국 한계에 도달한다.

이런 경우가 의외로 흔하다. 분석가가 BI 도구에서 무거운 쿼리를 띄워놓고 화면을 끄지 않았다든가, 애플리케이션 버그로 트랜잭션을 안 닫고 있다든가, replication consumer가 멈춰 있다든가. `pg_stat_activity`에서 `xact_start`가 며칠 전인 세션이 있으면 즉시 죽이는 편이 안전하다.

**2. `autovacuum_enabled = false`.** 누가 의도적으로 끈 테이블. 자동 freeze가 도는 트리거 자체가 사라진다. 다만 anti-wraparound vacuum은 무시하고 들어가니, 이것만으로 read-only가 되지는 않는다. 그런데 이것이 1번과 결합되면 진짜 위험해진다.

**3. replication slot 정체.** logical replication slot이 consumer 부재로 멈춰 있으면 WAL이 회수되지 않을 뿐 아니라, 그 slot이 보고 있는 snapshot 너머의 row를 vacuum이 회수할 수 없다. 이것도 long-running tx와 같은 효과다.

XID 나이가 더 올라가면 PostgreSQL은 점점 더 시끄럽게 경고한다.

- `age = 1,000,000,000` (10억) — 로그에 경고 출력 시작.
- `age = 1,500,000,000` (15억) — 더 진한 경고. autovacuum의 freeze 압박이 강해진다.
- `age = 2,000,000,000` (20억) — `autovacuum_freeze_max_age`의 10배. 매우 적극적인 freeze 시도.
- `age = 2,146,483,647` (21억 - 1만) — **wraparound protection mode 진입**. 클러스터가 모든 쓰기를 거부한다.

마지막 줄을 한 번 더 읽자. **클러스터가 모든 쓰기를 거부한다.** 단일 테이블이 아니라 전체 클러스터다. 한 데이터베이스의 한 테이블이 미끄러져도 전체가 멈춘다. 단일 테이블만의 문제가 아니라는 점이 무서운 부분이다.

protection mode에 들어가면 사용자에게 다음 메시지가 뜬다.

```
ERROR:  database is not accepting commands to avoid wraparound data loss in database "..."
HINT:  Stop the postmaster and vacuum that database in single-user mode.
```

힌트 줄을 보자. "single-user mode로 들어가서 vacuum 해라." 즉, 정상 서비스 상태로는 복구가 안 된다. 클러스터를 내리고, single-user mode로 띄우고, `VACUUM FREEZE`를 돌려야 한다. 다운타임이 발생한다. 대형 테이블이면 그 vacuum이 몇 시간을 잡아먹는다. 이게 18장 첫머리에서 말한 "한 달 만에 read-only가 된 클러스터"의 결말이다.

7.5개월이라는 숫자를 다시 떠올려보자. TPS 100~200 정도의 평범한 사이트가 평범하게 운영되고 있을 때, 어느 한 테이블의 autovacuum이 무력화되면 약 7.5개월 뒤에 클러스터가 멈춘다. 이 시한이 무서운 이유는, 평소엔 아무런 증상도 없다는 점이다. 메트릭이 다 녹색이다. 쿼리도 정상이다. 그런데 어느 날 갑자기 read-only가 된다. "잘 되고 있었는데 갑자기 왜?"라고 묻게 되는 사고가 바로 이것이다.

## 18.5 wraparound 사고 케이스 — 한 달 만에 클러스터 read-only

추상적인 이야기는 충분하다. 실제 사례를 들어보자. 커뮤니티에 자주 회자되는 패턴 하나를 재구성해본다.

한 SaaS 회사의 신입 DBA가 있었다. 합류 첫 주, 시니어 엔지니어가 한 시간짜리 인수인계를 해줬다. 시스템은 PostgreSQL 13, 8TB짜리 단일 클러스터. 가장 큰 테이블은 약 12억 행짜리 `events` 테이블이었다. write-heavy. 하루에 1억 건 정도가 쌓인다.

둘째 주에 운영팀이 불평을 했다. "주말마다 vacuum이 도는데 그때 응답시간이 30% 느려져요. 좀 어떻게 안 되나요?" 신입 DBA는 vacuum 로그를 봤다. `events` 테이블의 autovacuum이 매주 토요일 밤마다 5시간 이상 돌고 있었다. 평일 야간에는 작은 vacuum이 짧게 도는데, 누적된 dead tuple이 너무 많아 주말에 한 번 크게 도는 패턴이었다.

신입 DBA는 일단 `events` 테이블의 autovacuum scale factor를 0.05로 낮추고 cost_limit을 올렸다. 일주일을 지켜봤다. 주말 vacuum이 짧아졌고, 응답시간 저하도 사라졌다. 잘 됐다고 생각했다.

셋째 주에 다른 팀에서 요청이 왔다. "이벤트 분석 ETL 잡이 매일 새벽 3시에 도는데, autovacuum이랑 겹치면서 ETL이 느려져요. autovacuum을 좀 미룰 수 없을까요?" 신입 DBA는 `events` 테이블에 대해 `ALTER TABLE events SET (autovacuum_enabled = false)`를 걸고, 대신 cron으로 매일 오전 10시에 수동 `VACUUM ANALYZE events`를 돌리도록 했다. ETL과 안 겹치게 시간만 옮긴 거였다.

처음 며칠은 잘 돌았다. 모니터링에는 빨간 불이 하나도 없었다. 그런데 어느 날 cron 잡이 실패했다. 이유는 별 거 아니었다. cron이 실행될 시점에 다른 무거운 마이그레이션 작업이 돌고 있어 lock 충돌이 났다. 다음 날에도 실패했다. 그 사이 누군가 다른 작업으로 바빠 cron 잡 실패 알림을 무시했다.

문제는 여기서부터다. `events` 테이블의 autovacuum은 꺼져 있다. 그러니 평소 autovacuum이 도는 일은 없다. 그렇다면 anti-wraparound vacuum은? 그건 강제로 도니까 괜찮은 거 아닌가?

그게 아니었다. `events` 테이블에는 분석가가 띄워놓은 BI 쿼리 세션이 있었다. 며칠 전 분석가가 트랜잭션을 열고 결과를 보던 중 자리를 비웠다. 화면이 잠들었지만 세션은 살아 있었다. 그 트랜잭션은 일주일째 열려 있었고, snapshot이 일주일 전에 멈춰 있었다.

anti-wraparound vacuum이 자동으로 떠서 freezing을 시도했다. 그런데 그 long-running tx의 snapshot 너머로는 freezing이 안 된다. vacuum은 도는데 oldest XID는 줄어들지 않는다. PostgreSQL 로그에는 매분 다음 메시지가 찍히기 시작했다.

```
WARNING:  oldest xmin is far in the past
HINT:  Close open transactions soon to avoid wraparound problems.
```

그런데 이 경고는 로그 파일 안에서만 도는 메시지였다. 모니터링 시스템에 로그 알람이 안 걸려 있었다. 아무도 안 봤다.

3주차, 신입 DBA가 합류한 지 한 달이 다 되어가던 어느 평일 오후. 결제 API가 갑자기 실패하기 시작했다. 슬랙이 비명으로 도배됐다.

```
ERROR:  database is not accepting commands to avoid wraparound data loss in database "production"
```

전체 클러스터가 read-only가 됐다. 결제·주문·로그인 모두 정지. SaaS의 모든 고객사가 동시에 멈췄다. 신입 DBA는 시니어를 호출하고, 시니어는 매뉴얼을 들고 single-user mode로 들어갈 준비를 했다. 다행히 시니어가 빨랐다.

**복구 절차는 다음과 같이 진행됐다.**

1. 우선 `pg_stat_activity`에서 long-running tx를 찾아 강제로 죽였다. `pg_terminate_backend(pid)`. 일주일 묵은 분석가 세션이었다.
2. 그래도 protection mode는 안 풀린다. XID 나이가 21억 근처라서, vacuum이 끝나야만 protection이 해제된다.
3. 다행히 13 버전에서는 single-user mode 없이도 superuser 권한으로 `VACUUM FREEZE`를 거는 것이 가능했다. 9.x 시절에는 정말로 single-user mode로 들어가야 했다.
4. `events` 테이블에 `VACUUM (FREEZE, VERBOSE) events;`를 걸었다. 12억 행짜리 테이블이라 약 6시간이 걸렸다.
5. 같은 데이터베이스 안의 다른 큰 테이블 몇 개도 같이 freeze했다.
6. `SELECT datname, age(datfrozenxid) FROM pg_database;`로 모든 데이터베이스의 xid_age가 안전 범위(예: 10억 미만)로 떨어진 것을 확인하고, protection mode가 자동으로 해제됐다.

총 다운타임 7시간. 모든 고객사에 사과 메일을 돌렸고, 일부 고객은 SLA 페널티를 청구했다. 사후 분석에서 root cause로 다음이 정리됐다.

- 직접 원인: `events` 테이블의 `autovacuum_enabled = false` 설정.
- 결합 원인: cron 잡 실패 + long-running tx + 로그 알람 부재.
- 시스템 원인: `age(datfrozenxid)` 모니터링 미설치.

신입 DBA가 의도한 건 단지 "ETL이랑 안 겹치게 vacuum 시간을 옮기는 것"이었다. 그런데 그 한 줄이 한 달 뒤에 클러스터를 멈췄다. 이 사고에서 진짜 무서운 부분은 신입 DBA가 잘못된 매뉴얼을 따른 게 아니라는 점이다. 매뉴얼대로 했고, 의도도 합리적이었다. 단지 PostgreSQL의 XID wraparound라는 깊은 메커니즘을 몰랐을 뿐이다.

이 사고가 우리에게 가르치는 것은 세 가지다.

첫째, **`autovacuum_enabled = false`는 거의 항상 잘못된 선택이다.** vacuum 시간이 문제라면 `cost_*` 파라미터로 강도를 조절하거나, scale_factor를 낮춰 더 자주 짧게 돌게 하는 게 정답이다. 끄는 게 답이 아니다. 정말 꺼야 한다면, 명시적인 freeze schedule을 cron이 아니라 더 안정적인 방식으로(예: 스케줄러 + 알람 + dead-man switch) 운영해야 한다.

둘째, **long-running transaction은 사일런트 킬러다.** `pg_stat_activity`에서 `xact_start`가 한 시간 넘은 세션이 있는지 매일 확인하는 모니터링이 필수다. 특히 분석가의 BI 도구, replication consumer, 그리고 애플리케이션의 트랜잭션 누수가 흔한 범인이다.

셋째, **로그 안의 경고는 안 본 것이나 마찬가지다.** PostgreSQL 로그에 `oldest xmin is far in the past` 경고가 찍히기 시작하면, 그건 페이저 알람으로 올라와야 한다. 로그 파일 안에서만 도는 경고는 모니터링이 아니다.

## 18.6 예방과 복구 — relfrozenxid 모니터링, postgres_get_av_diag (AWS)

사고 이야기로 18.5를 끝냈으니, 이제 예방과 복구 쪽으로 가자. 같은 사고를 두 번 겪지 않으려면 어떻게 해야 할까?

**예방의 첫 번째 줄은 모니터링이다.** 18.3에서 본 쿼리들을 그대로 메트릭으로 끌어올린다. 최소한 다음 세 개는 알람으로 묶어두자.

```sql
-- 1. 데이터베이스별 XID age
SELECT datname, age(datfrozenxid) AS xid_age
FROM pg_database;

-- 2. 테이블별 XID age (상위 N개)
SELECT
  schemaname || '.' || relname AS table_name,
  age(c.relfrozenxid) AS xid_age
FROM pg_class c
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE c.relkind = 'r'
  AND n.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY age(c.relfrozenxid) DESC
LIMIT 20;

-- 3. long-running transaction
SELECT pid, usename, datname, xact_start, now() - xact_start AS xact_duration, query
FROM pg_stat_activity
WHERE xact_start IS NOT NULL
  AND now() - xact_start > interval '30 minutes'
ORDER BY xact_start;
```

알람 임계치는 보수적으로 잡는 편이 좋다. 다음이 운영 현장에서 많이 쓰는 임계다.

| 메트릭 | 1차 경고 | 2차 경고 | 페이저 |
|---|---|---|---|
| `age(datfrozenxid)` | 2억 | 5억 | 10억 |
| `age(relfrozenxid)` (테이블) | 2억 | 5억 | 10억 |
| long-running tx 지속 시간 | 30분 | 2시간 | 6시간 |

특히 `age(datfrozenxid) > 10억`은 페이저로 깨워야 한다. 그 시점부터는 시간이 빠르게 흐른다. 며칠 안에 read-only로 들어갈 가능성이 있다.

**예방의 두 번째 줄은 autovacuum 설정 점검이다.** 다음 두 쿼리를 정기적으로 돌려서 "autovacuum이 꺼진 테이블"과 "튜닝되지 않은 큰 테이블"을 찾아내자.

```sql
-- autovacuum이 꺼진 테이블 찾기
SELECT
  schemaname || '.' || relname AS table_name,
  reloptions
FROM pg_class c
JOIN pg_namespace n ON c.relnamespace = n.oid
JOIN pg_stat_user_tables s ON c.relname = s.relname
WHERE reloptions::text LIKE '%autovacuum_enabled=false%';

-- 큰 테이블 중 reloptions가 비어 있는(기본값을 그대로 쓰는) 테이블
SELECT
  schemaname || '.' || relname AS table_name,
  pg_size_pretty(pg_total_relation_size(schemaname || '.' || relname)) AS size,
  n_live_tup
FROM pg_stat_user_tables s
JOIN pg_class c ON c.relname = s.relname
WHERE c.relkind = 'r'
  AND n_live_tup > 10000000  -- 1천만 행 이상
  AND (reloptions IS NULL OR NOT reloptions::text LIKE '%autovacuum_vacuum_scale_factor%')
ORDER BY n_live_tup DESC;
```

첫 쿼리에서 결과가 나오면 그 테이블이 진짜로 꺼두는 게 맞는지 다시 검토하자. 두 번째 쿼리는 "기본값만 믿고 있는 대용량 테이블"을 잡아낸다. 이런 테이블이 다음 사고의 후보다.

**클라우드 환경의 진단 도구도 챙기자.** AWS RDS PostgreSQL은 14 버전 이상에서 `aws_rds_admin` 스키마와 `rds_tools` 익스텐션 안에 autovacuum 진단 함수를 제공한다. 대표적인 것이 `postgres_get_av_diag()`다(정확한 이름과 위치는 RDS 버전마다 약간 다르니 최신 문서를 확인하자). 이 함수는 현재 autovacuum이 어디에서 막혀 있는지, 어떤 테이블이 freezing 대기 중인지, oldest xmin이 어떤 세션 때문에 잡혀 있는지를 한 번에 알려준다. RDS를 쓴다면 매일 이 함수의 결과를 슬랙으로 보내는 잡 하나 만들어두는 편이 좋다.

GCP Cloud SQL은 `cloudsql.enable_pgaudit` 같은 익스텐션은 있지만, autovacuum 진단 전용 함수는 따로 없다. 대신 Query Insights와 Cloud Monitoring으로 long-running tx와 vacuum 진행을 본다. Azure Database for PostgreSQL도 비슷하다. 클라우드는 어떤 벤더든 vacuum 관련 메트릭이 메뉴에 따로 있으니, 이 메뉴를 안 보고 사는 운영팀이 있다면 일단 한 번 들어가보자.

**예방의 세 번째 줄은 정기 점검 루틴이다.** 매주 한 번씩은 다음을 확인하는 운영팀이 많다.

- `pg_database`의 모든 `age(datfrozenxid)`가 5억 미만인지.
- 가장 오래된 `relfrozenxid` 테이블이 5억 미만인지.
- 24시간 넘게 열린 트랜잭션이 없는지.
- 모든 logical replication slot의 `confirmed_flush_lsn`이 24시간 안에 갱신됐는지.

이 네 가지가 다 통과하면 일주일 동안 wraparound 사고를 걱정할 필요가 없다. 사람이 매주 들여다보는 게 번거롭다면 자동화하자. Grafana 대시보드의 health check 패널 하나로 묶으면 충분하다.

**그래도 사고가 나면, 어떻게 복구할까?** protection mode에 들어간 클러스터의 복구 절차를 정리하자.

1. **장애 알림이 뜨면 우선 long-running tx를 죽인다.** `pg_stat_activity`에서 `xact_start`가 가장 오래된 세션부터 `pg_terminate_backend(pid)`로 강제 종료. autovacuum이 freeze를 진행할 수 있도록 길을 터주는 작업이다.

2. **replication slot도 같이 점검한다.** `pg_replication_slots`에서 `active = false`이거나 `confirmed_flush_lsn`이 한참 옛날인 slot이 있으면, 그 slot을 `pg_drop_replication_slot('...')`으로 제거한다. 단, 정말 안 쓰는 slot인지 확인하고. 살아 있는 consumer가 있다면 그쪽을 먼저 복구해야 한다.

3. **xid_age가 가장 큰 테이블에 `VACUUM (FREEZE, VERBOSE)`를 건다.** 이게 한참 걸린다. 12억 행이면 보통 4~8시간. I/O 한도를 풀어주기 위해 `SET vacuum_cost_delay = 0;`을 세션에 걸어두면 더 빠르다. 단, 다른 쿼리에 미치는 영향을 감안하자(어차피 read-only라 영향은 작다).

4. **여러 테이블이 동시에 위험하면 병렬로 돌린다.** 다른 세션에서 또 다른 큰 테이블에 vacuum을 건다. CPU·I/O가 받쳐주는 한 동시에 여러 테이블을 처리하는 게 빠르다.

5. **`age(datfrozenxid)`가 안전 범위로 떨어지면 protection mode가 자동 해제된다.** PostgreSQL 14 이상에서는 `vacuum_failsafe_age` 메커니즘이 더 적극적으로 도와준다. 이전 버전에서는 single-user mode가 필요할 수 있다(`postgres --single -D ...`).

6. **모든 데이터베이스의 xid_age가 정상이면 서비스를 재개한다.** 그리고 즉시 사후 분석에 들어간다. 무엇이 빠져 있었는지, 어떤 알람이 안 울렸는지, 같은 사고가 어떻게 막힐 수 있었는지를 문서로 남긴다.

마지막으로, 절대 잊지 말자. **`autovacuum_enabled = false`는 거의 항상 잘못된 선택이다.** vacuum 부담이 문제라면 `vacuum_cost_delay`, `vacuum_cost_limit`, scale factor로 강도를 조절하고, 시간대를 옮기고 싶다면 cron으로 수동 vacuum을 별도로 거는 한편 autovacuum은 켜둔다. autovacuum을 끄는 것은 시한폭탄을 차는 것과 같다. 7.5개월 뒤에 터질 폭탄이다.

## 18.7 Bloat 처리 — VACUUM FULL, pg_repack, pg_squeeze 비교

여기까지 잘 막았다고 해도, 이미 쌓인 bloat가 남아 있을 수 있다. 신입으로 들어간 사이트가 몇 년간 vacuum이 부실하게 운영됐다면, 테이블이 이미 두세 배로 부풀어 있을 가능성이 높다. 이 경우 autovacuum 튜닝만으로는 회수가 안 된다. bloat된 공간을 물리적으로 압축해야 한다.

먼저 bloat가 얼마나 쌓였는지 보는 법부터. `pgstattuple` 익스텐션이 가장 정확하다.

```sql
CREATE EXTENSION pgstattuple;

SELECT
  table_name,
  pg_size_pretty(table_len::bigint) AS table_size,
  ROUND(dead_tuple_percent::numeric, 2) AS dead_pct,
  ROUND(free_percent::numeric, 2) AS free_pct
FROM pgstattuple('public.orders') AS t,
     (SELECT 'public.orders' AS table_name) AS n;
```

`dead_tuple_percent`와 `free_percent`를 더한 값이 회수 가능한 공간이다. 둘을 합쳐 30%를 넘으면 bloat 회수 작업을 검토할 만하다. 다만 `pgstattuple`은 테이블을 풀스캔하니, 거대 테이블에 자주 돌리는 건 피하자. 추정 함수인 `pgstattuple_approx`를 쓰는 편이 안전하다.

bloat가 확인됐다면 회수 도구는 세 가지다. **VACUUM FULL**, **pg_repack**, **pg_squeeze**.

### VACUUM FULL

이름이 가장 직관적이다. PostgreSQL 내장 명령. 테이블 전체를 새 파일로 다시 쓴다. 결과적으로 dead tuple과 빈 공간이 모두 제거된 깔끔한 테이블이 만들어진다.

```sql
VACUUM FULL orders;
```

문제는 **`ACCESS EXCLUSIVE` 락**이다. 이 락이 걸려 있는 동안 SELECT조차 막힌다. 12억 행짜리 테이블에 VACUUM FULL을 걸면 몇 시간 동안 그 테이블을 아무도 못 쓴다. 사실상 다운타임이다. 게다가 VACUUM FULL이 도는 동안 디스크 공간이 일시적으로 두 배 필요하다(원본 + 새로 쓰는 파일). 디스크 여유가 빠듯한 사이트에서는 도중에 디스크 풀로 죽는 사고도 가끔 일어난다. 끔찍한 일이다.

VACUUM FULL이 정답인 경우는 두 가지다. 하나, 정말로 작은 테이블이라 잠깐 잠겨도 영향이 없는 경우. 둘, 계획된 다운타임 윈도우가 있는 경우. 그 외에는 다음 두 도구를 검토하는 편이 낫다.

### pg_repack

pg_repack은 PostgreSQL 외부 익스텐션이다. PostgreSQL Korea에서 잘 알려진 도구인데, 핵심 아이디어는 단순하다.

1. 원본 테이블과 똑같은 구조의 임시 테이블을 만든다.
2. 트리거를 걸어 원본 테이블의 변경사항을 임시 테이블에 동기화한다.
3. 원본 테이블의 데이터를 임시 테이블로 복사한다(이때 dead tuple은 제외, 정렬도 가능).
4. 인덱스를 다시 만든다.
5. **아주 짧은 시간만** `ACCESS EXCLUSIVE` 락을 잡고 원본과 임시 테이블을 swap한다.
6. 원본(이제는 옛 데이터)을 drop한다.

핵심은 5번이다. 락 잡는 시간이 초 단위로 짧다. 그 사이에만 잠깐 끊기고, 나머지 시간은 정상 트래픽이 흐른다. 12억 행 테이블도 무중단(에 가깝게) 회수가 가능하다.

```bash
pg_repack --no-superuser-check -d production -t public.orders -j 4
```

`-j 4`는 인덱스를 4개 병렬로 만든다는 뜻이다. 인덱스 재구성이 가장 오래 걸리니, 병렬을 올리는 것이 핵심 튜닝 포인트다.

pg_repack의 함정 두 가지를 짚자.

**1. 디스크 공간.** 원본과 같은 크기의 임시 테이블이 잠시 같이 존재한다. VACUUM FULL과 마찬가지로 일시적으로 두 배의 공간이 필요하다. 8TB 클러스터에서 4TB짜리 테이블을 repack한다면 4TB의 여유가 필요하다. 미리 확인하자.

**2. primary key가 없으면 안 된다.** pg_repack은 PK나 NOT NULL UNIQUE 인덱스가 있어야 동작한다. 없는 테이블이라면 일단 만들어줘야 한다. 거대 테이블에 PK를 새로 만드는 일도 만만치 않으니, 처음부터 PK를 두는 습관이 중요하다.

**3. 트리거 충돌.** pg_repack이 원본 테이블에 자체 트리거를 건다. 사용자 정의 트리거가 많으면 충돌 가능성이 있다. 미리 테스트 환경에서 검증하자.

운영 패턴으로는 **"한 번 크게 정리할 때"** pg_repack을 쓴다. 새로 합류한 사이트의 누적 bloat 회수, 또는 분기별 대정리 같은 일회성 작업에 어울린다.

### pg_squeeze

pg_squeeze는 더 새로운 도구다. 체코 개발자 Antonin Houska가 만들었고, 핵심은 **logical decoding**을 이용한다는 점이다.

pg_repack이 트리거로 변경사항을 동기화한다면, pg_squeeze는 WAL을 logical decoding해서 변경사항을 따라간다. 트리거가 없으니 원본 테이블에 부하가 거의 없다. 그리고 background worker로 동작하기 때문에 외부 명령 호출이 필요 없다. 한 번 설정해두면 자동으로 돈다.

```sql
CREATE EXTENSION pg_squeeze;

INSERT INTO squeeze.tables (
  tabschema,
  tabname,
  schedule,
  free_space_extra,
  min_size
)
VALUES (
  'public', 'orders',
  '(30, 4, NULL, NULL, 0)',  -- 매일 04:30
  20,                          -- 20% 이상 free space일 때 동작
  1024                         -- 1GB 이상 테이블에만 동작
);
```

이 설정 한 번이면 매일 새벽 4시 30분에 `orders` 테이블의 free space가 20% 넘으면 자동으로 squeeze한다. 사람이 명령을 칠 일이 없다.

pg_squeeze의 강점은 **자동화**다. 한 번 깔아두면 dba가 매번 신경 쓸 필요가 없다. 약점은 **logical decoding의 오버헤드**다. WAL을 decoding하니 master에 약간의 부하가 추가된다. 또한 logical replication을 이미 쓰는 사이트라면 slot 관리가 복잡해진다.

운영 패턴으로는 **"평시 자동 정리"**에 pg_squeeze가 어울린다. 매일 야간에 자동으로 돌면서 bloat가 일정 비율을 넘는 테이블을 조용히 압축한다. 사람이 깨어 있을 필요가 없다.

### 비교 정리

세 도구의 선택 기준을 한 표로 정리하자.

| 도구 | 락 | 다운타임 | 자동화 | 추가 디스크 | 어울리는 상황 |
|---|---|---|---|---|---|
| **VACUUM FULL** | ACCESS EXCLUSIVE | 길다 (테이블 크기 비례) | 수동 | 2배 | 작은 테이블, 계획된 다운타임 |
| **pg_repack** | 짧은 ACCESS EXCLUSIVE (swap 시) | 거의 0 | 수동 (외부 명령) | 2배 | 일회성 대규모 회수 |
| **pg_squeeze** | 짧은 락 (swap 시) | 거의 0 | 자동 (BGW + scheduler) | 2배 | 평시 자동 회수 |

운영 패턴의 권장은 이렇다. **평시 자동 정리는 pg_squeeze, 일회성 큰 회수는 pg_repack, 그 외 정말 작은 테이블에만 VACUUM FULL.** 세 도구가 배제 관계가 아니다. pg_squeeze로 평소를 관리하고, 가끔 큰 정리가 필요하면 pg_repack을 쓰는 식으로 같이 운영하는 사이트도 많다.

한 가지 더 챙길 게 있다. **인덱스 bloat다.** 테이블 bloat만 신경 쓰다가 인덱스가 부풀어 있는 걸 놓치는 경우가 흔하다. 인덱스도 dead entry가 쌓이면 페이지가 부풀고, B-tree 탐색이 느려진다. 인덱스 bloat 확인은 `pgstatindex`로 한다.

```sql
SELECT
  index_name,
  leaf_fragmentation,
  avg_leaf_density
FROM (
  SELECT
    'orders_user_id_idx' AS index_name,
    (pgstatindex('orders_user_id_idx')).*
) t;
```

`avg_leaf_density`가 50% 아래로 떨어지면 회수가 필요한 신호다. 인덱스 회수에는 **`REINDEX CONCURRENTLY`**가 정답이다. PostgreSQL 12부터 지원된다. 락을 최소화하면서 인덱스를 새로 만든다.

```sql
REINDEX INDEX CONCURRENTLY orders_user_id_idx;
```

pg_repack도 인덱스만 따로 재구성하는 `-x` 옵션을 제공한다. 둘 다 무중단으로 인덱스를 회수할 수 있으니, 사이트에 익숙한 도구를 쓰면 된다. 다만 `REINDEX CONCURRENTLY`는 도중에 실패하면 `INVALID` 상태의 좀비 인덱스가 남는다. 이 경우 즉시 drop하고 다시 만들어야 하니, 결과를 꼭 확인하자.

마지막으로 한 가지 더 짚자. **bloat 회수보다 bloat 예방이 먼저다.** 18.1~18.2에서 본 autovacuum 튜닝을 제대로 해두면, 평소에는 bloat가 위험 수준까지 쌓이지 않는다. pg_squeeze든 pg_repack이든 도구는 보조 수단이지 본 처방이 아니다. 본 처방은 autovacuum을 잘 길들이는 것이다. 도구에만 의존하면, 도구가 못 따라가는 어느 날 또 사고가 난다.

그리고 한 가지 더. **PostgreSQL 13부터 vacuum이 인덱스 정리를 병렬로 할 수 있다.** `max_parallel_maintenance_workers`(기본 2)로 제어된다. 인덱스가 많은 테이블에서 vacuum 시간이 절반 이하로 줄어든다. 단, autovacuum은 기본적으로 병렬 vacuum을 안 쓴다(설정 가능). 수동 `VACUUM (PARALLEL 4) orders;`로 명시할 때만 활성화된다. 큰 vacuum이 자주 도는 사이트라면 이 옵션을 활용하는 편이 좋다.

## 마무리

autovacuum의 트리거 공식부터 시작해 대용량 테이블의 위험, 모니터링 지표, XID wraparound의 메커니즘, 실제 사고 케이스, 예방·복구 절차, 그리고 누적된 bloat를 처리하는 세 가지 도구까지 한 바퀴 돌았다. 길게 풀었지만, 핵심 당부는 의외로 짧게 묶인다. 다시 정리하자.

**기억해두자, 첫째.** PostgreSQL의 autovacuum 기본값은 "안전한 출발점"이지 "운영 최적값"이 아니다. 1,000만 행이 넘는 테이블이 있다면 scale_factor를 0.01~0.05로 낮추고, threshold를 절대값으로 잡아주는 편이 좋다. 기본값을 그대로 둔다는 건 "큰 테이블은 vacuum 안 해도 됨"이라고 선언하는 것과 같다.

**기억해두자, 둘째.** `autovacuum_enabled = false`는 거의 항상 잘못된 선택이다. vacuum이 무겁다면 `cost_*` 파라미터로 강도를 조절하고, 시간대 충돌이 문제라면 별도 cron으로 수동 vacuum을 추가하되 autovacuum은 켜둔다. 끄는 것은 시한폭탄이다. 7.5개월 뒤에 터질, 모니터링 그래프에 빨간 불 하나 없이 평온해 보이는 폭탄.

**기억해두자, 셋째.** `age(datfrozenxid)` 모니터링은 페이저로 묶어야 한다. 2억에서 1차 경고, 5억에서 2차, 10억에서 페이저. 로그 안의 `oldest xmin is far in the past` 경고는 안 본 것이나 마찬가지니, 로그를 메트릭으로 끌어올리자.

**기억해두자, 넷째.** long-running transaction은 사일런트 킬러다. 분석가의 BI 세션, 멈춰 있는 replication consumer, 트랜잭션을 안 닫는 애플리케이션 버그. `xact_start`가 한 시간 넘은 세션이 매일 체크되어야 한다. 이걸 안 보면 anti-wraparound vacuum이 떠도 freeze가 안 된다.

**기억해두자, 다섯째.** bloat 회수 도구 세 개의 자리는 분명하다. 평시 자동은 pg_squeeze, 일회성 큰 회수는 pg_repack, 작은 테이블만 VACUUM FULL. 그러나 도구는 보조다. 본 처방은 18.1~18.3의 autovacuum 튜닝이다.

**기억해두자, 여섯째.** PostgreSQL 13 이상에서는 insert-only 테이블에 `autovacuum_vacuum_insert_threshold`를 잊지 말자. 로그 테이블처럼 INSERT만 받는 테이블이 freeze의 사각지대다. UPDATE/DELETE가 없으니 평시엔 조용하다가 6~7개월 뒤에 한꺼번에 사고가 난다.

5장에서 우리는 PostgreSQL의 MVCC가 왜 VACUUM이라는 무거운 짝을 운명처럼 데리고 다니는지를 봤다. 18장은 그 무게를 어떻게 견딜 만한 일과로 바꾸는지에 대한 처방이었다. 5장이 끝나고 "그래서 어떻게 해야 하는데?"라는 질문이 남았다면, 이 장이 그 답이다. autovacuum은 enemy가 아니라 partner다. 잘 길들이면 야간에 발 뻗고 잘 수 있다. 못 길들이면 한 달 뒤에 read-only가 된 클러스터 앞에서 single-user mode 매뉴얼을 펼치게 된다.

다음 장에서는 한층 더 무거운 주제로 간다. 백업과 복구. autovacuum이 멀쩡해도 디스크가 죽거나, 사람이 실수로 테이블을 drop하거나, 데이터센터가 잠기면 클러스터를 처음부터 다시 세워야 한다. "백업은 있는데 복구가 안 된다"는 야간 사고를 막는 도구들 — pgBackRest, Barman, WAL-G, 그리고 PITR 시나리오. 같이 살펴보자.
