# 13장. 이벤트·큐·실시간 — Kafka를 미루는 법

신규 서비스를 하나 만든다고 해보자. 주문이 들어오면 결제·재고·알림이 차례로 흘러가야 한다. 누군가 회의실에서 그림판을 켜고 화살표를 그리기 시작한다. 주문 서비스 옆에 동그라미 하나가 더 생긴다. 라벨은 "Kafka". 그러면 또 옆에는 ZooKeeper(혹은 KRaft 컨트롤러), 그 옆에는 Schema Registry, 또 그 옆에는 Connect 클러스터. 동그라미 다섯 개를 그렸을 뿐인데 운영 부담은 다섯 배가 아니라 스무 배쯤으로 부풀어 오른다. 그리고 첫 분기 트래픽은 초당 50건 정도다.

물론 Kafka는 훌륭한 도구다. 하지만 메시지 큐 하나 쓰자고 새 클러스터를 띄우는 일이 늘 정답일까? 작은 팀이라면, 또 다른 답이 있을 수 있다. 그 답은 책상 위에 이미 올라와 있는 PostgreSQL이다.

PG가 메시지 버스로서 어디까지 변신할 수 있는지 함께 따라가보자. 가벼운 알림은 `LISTEN/NOTIFY`로, 변경 캡처는 logical decoding으로, 스케줄과 영속 큐는 `pg_cron`과 `pgmq`로, 그리고 트랜잭션 안전한 이벤트 발행은 Outbox 패턴으로. 마지막에는 "Just Use Postgres" 진영의 논리를 정리하고, 그 위에서 카카오가 실제로 어떻게 PG → Elasticsearch CDC 파이프라인을 만들어 썼는지를 들여다본다. 단, 카카오 사례에서는 "이런 패턴이 가능하다"의 시연까지만 보자. "그 결정이 옳았는가, 무엇이 남았는가"는 25장에서 다시 만난다.

## 13.1 LISTEN/NOTIFY — 8KB짜리 가벼운 알림

밤 11시, 운영팀 채팅방에 알림 하나가 떴다고 상상해보자. "결제 실패율 5% 초과". 이 알림이 어떻게 떠올랐는지 거슬러 올라가다 보면, 어딘가에서 어플리케이션이 "결제 실패가 늘었어"라고 외쳤고, 누군가는 그 외침을 듣고 있었어야 한다. 외치는 쪽과 듣는 쪽이 서로 누구인지 몰라도 동작하는 것 — 그것이 가장 단순한 형태의 pub/sub이다.

PostgreSQL은 이 단순한 pub/sub을 1990년대부터 내장해두었다. `LISTEN`과 `NOTIFY`. 외부 미들웨어 없이도 DB 안에서 채널을 만들고, 채널에 가입하고, 채널로 메시지를 던지는 일이 가능하다.

가장 작은 예부터 보자. 두 개의 세션이 필요하다. 하나는 듣는 쪽, 하나는 외치는 쪽이다.

```sql
-- 세션 A: 듣는 쪽
LISTEN payment_failed;
```

```sql
-- 세션 B: 외치는 쪽
NOTIFY payment_failed, '{"order_id": 1024, "reason": "card_declined"}';
```

세션 B에서 `NOTIFY`를 날린 순간, 세션 A는 자신이 `LISTEN`해둔 채널에 알림이 도착했다는 사실을 통보받는다. 어플리케이션 드라이버(JDBC, libpq, asyncpg 등)는 이 알림을 콜백이나 비동기 이터레이터로 노출한다. 매번 폴링하지 않아도 "왔어요"라는 신호를 그 자리에서 받을 수 있다.

여기서 한 가지 짚고 넘어가자. `NOTIFY`는 언제 발사될까? 답은 "트랜잭션 커밋 시점"이다. `BEGIN ... NOTIFY ... ROLLBACK`으로 묶으면 알림은 사라진다. 비즈니스 로직과 같은 트랜잭션에 묶어 두면, 비즈니스가 성공해야만 알림이 나간다. 이 작은 약속이 의외로 큰 안전망이 된다. "결제는 실패했는데 결제 실패 알림은 안 나갔다"거나 "결제는 성공했는데 실패 알림이 나갔다" 같은 끔찍한 일이 줄어든다.

### payload 8KB라는 단단한 벽

LISTEN/NOTIFY를 쓰기 시작하면 곧 하나의 벽을 만난다. payload 크기 제한 8000바이트. 정확히는 8000바이트(PostgreSQL이 일반적으로 가지는 `NAMEDATALEN` 관련 기본값에 묶여 있고, 빌드 시점에 결정된다 — 직접 늘리려면 소스를 고쳐 빌드해야 한다는 뜻이다). JSON 한 덩어리를 통째로 밀어 넣다 보면 어느 순간 `payload string too long` 에러가 튀어나온다. 처음 보면 난감하다.

해법은 단순하다. payload에는 식별자만 싣자. 본문은 테이블에 두고, 알림은 "이 id를 보러 와"라고만 외친다.

```sql
-- 외치는 쪽: payload는 행 식별자만
INSERT INTO order_events (order_id, type, payload)
VALUES (1024, 'payment_failed', '{"reason":"card_declined", ...큰 JSON...}')
RETURNING id;

NOTIFY order_events_chan, '{"event_id": 31415}';
```

```python
# 듣는 쪽 (psycopg3 의사 코드)
async with conn.cursor() as cur:
    await cur.execute("LISTEN order_events_chan;")
    async for n in conn.notifies():
        event_id = json.loads(n.payload)["event_id"]
        row = await fetch_event(event_id)   # 본문은 테이블에서
        await handle(row)
```

이렇게만 해도 "가벼운 알림 + 무거운 본문"의 분리가 깔끔하게 떨어진다. payload는 트랜잭션 ID·이벤트 ID 정도로만 쓰고, 컨슈머가 자기 속도에 맞춰 본문을 읽어 가게 두자.

### 영속성이 없다는 약점

LISTEN/NOTIFY의 또 하나의 진실은 "받지 못한 알림은 사라진다"는 것이다. 컨슈머가 죽어 있는 동안 발사된 `NOTIFY`는 컨슈머가 살아 돌아와도 다시 들리지 않는다. 메시지 큐로서의 영속성이 없다. Kafka의 retention.ms 같은 개념이 없다고 보면 된다.

이 한계를 모르는 채 LISTEN/NOTIFY 위에 결제 같은 중요한 흐름을 얹는 일은 위험하다. 컨슈머가 재시작되는 그 5초 사이에 발사된 알림은 어디로 갔는지 알 길이 없다. 그러니 LISTEN/NOTIFY는 다음과 같은 자리에서 빛난다.

- **캐시 무효화 신호.** "어떤 키가 바뀌었으니 캐시 비워" 정도는 놓쳐도 다음 변경 때 다시 외친다.
- **관리자 대시보드의 실시간 새로고침.** WebSocket 게이트웨이가 DB 알림을 받아 클라이언트에 푸시.
- **워커 깨우기.** 작업 큐 테이블을 폴링하던 워커가 "새 작업 들어왔으니 한 번 더 봐" 신호로 깨어남.

세 번째 패턴이 특히 깔끔하다. 워커는 평소에는 30초마다 한 번 큐 테이블을 본다. 그런데 누가 작업을 넣으면서 `NOTIFY job_inserted`도 함께 발사하면, 워커는 "왔다는데?" 하면서 그 자리에서 한 번 더 본다. 폴링 주기를 길게 두고도 즉시성을 살릴 수 있다. 알림이 누락돼도 어차피 다음 폴링이 잡아내니 영속성 결함이 치명상이 되지 않는다. 폴링과 푸시의 좋은 점을 함께 가져가는 셈이다.

조금 더 풀어보자. 컨슈머가 살아 있는 동안에는 LISTEN/NOTIFY의 즉시성이 일을 한다. 작업이 들어오자마자 워커가 그 자리에서 깨어나니 평균 지연이 수밀리초 수준으로 떨어진다. 반대로 컨슈머가 죽거나 네트워크가 끊긴 동안 들어온 작업은 polling이 책임진다. 폴링 주기가 30초라면 워크로드의 평균 지연은 평소 수밀리초, 컨슈머 장애 동안만 0~30초. 두 모드의 장점이 자연스럽게 얹힌다. 이런 hybrid 패턴이 의외로 견고하다. 한쪽 메커니즘이 잠시 흔들려도 다른 쪽이 받쳐주니까.

### 운영 시 주의할 두세 가지

LISTEN/NOTIFY는 무료로 보이지만 공짜는 아니다. 잊지 말자.

첫째, **NOTIFY queue**가 디스크에 쌓일 수 있다. 컨슈머가 따라오지 못하는 동안 발사된 알림은 `pg_notify_queue_usage` 함수로 사용량을 볼 수 있다(0.0~1.0). 1.0에 가까워지면 새 `NOTIFY`가 거부된다. 컨슈머가 죽은 채 며칠을 방치하면 클러스터 전체가 영향을 받는다.

둘째, **PgBouncer transaction pooling 모드에서는 사실상 쓸 수 없다.** LISTEN은 세션 단위로 유지되어야 하는데, transaction pooling은 매 트랜잭션 끝에 connection을 풀로 돌려보낸다. session pooling 모드로 두거나, LISTEN 전용 connection은 풀을 거치지 않게 우회하자. 이걸 모르고 LISTEN을 걸어두면 "왜 알림이 안 오지" 하면서 한참 헤매게 된다. 찜찜한 디버깅 시간이 줄줄 흐른다.

셋째, **같은 트랜잭션 안에서 동일한 채널·payload의 NOTIFY는 중복 제거된다.** 트리거에서 한 트랜잭션에 100개의 row가 바뀌어 100번 `NOTIFY`를 했다고 해도, payload가 같으면 한 번만 발사된다. 일괄 업데이트 후 "전부 새로고침해" 식의 신호에는 오히려 친절한 동작이지만, 행 단위 알림이 필요하다면 payload에 행 식별자를 꼭 담아야 한다.

넷째, **순서는 채널 단위로 보존된다.** 동일 채널 안에서 발사된 NOTIFY는 발사 순서대로 컨슈머에게 도착한다. 그러나 채널이 여러 개라면 채널 간 순서는 보장되지 않는다. 순서가 중요한 신호는 같은 채널을 쓰자. 한 가지 더, 컨슈머가 여러 명이라면 각 컨슈머는 동일한 알림을 모두 받는다. 큐 시맨틱이 아니라 pub/sub 시맨틱이라는 점도 기억해두자. "한 컨슈머가 처리하면 다른 컨슈머는 안 받는다"가 필요하면 LISTEN/NOTIFY가 아니라 `SKIP LOCKED` 기반의 큐 패턴(13.3)으로 가야 한다.

자, LISTEN/NOTIFY는 가벼운 알림에 어울리고 영속성에 약하다는 정리까지 왔다. 그렇다면 영속성과 순서가 필요한 경우에는 어떻게 해야 할까? 자연스럽게 다음 도구로 넘어간다.

## 13.2 logical decoding — Debezium이 서 있는 토대

영속적인 변경 스트림을 PG 밖으로 보내고 싶다면, 새 길이 열린다. **logical decoding**이다. 이름이 거창해 보이지만 발상은 간단하다. PG는 모든 변경을 WAL(Write-Ahead Log)에 적어둔다. 그 WAL을 외부에서 "읽기 쉬운 형태"로 풀어주는 기능이 logical decoding이다.

물리 복제(physical replication)는 WAL을 바이트 그대로 standby에 복사한다. 페이지 레벨이다. 그러니 standby는 primary와 똑같은 모양이어야 한다. 반면 logical decoding은 WAL을 해석해 `INSERT into orders values(...)`, `UPDATE orders set status=... where id=...`처럼 행 단위로 풀어준다. 그러면 PG가 아닌 곳, 예를 들어 Elasticsearch나 Kafka로도 흘려보낼 수 있다.

### 가장 작은 시연

logical decoding을 켜려면 `wal_level = logical`을 잡아주어야 한다. RDS·Aurora 같은 매니지드에서도 파라미터 그룹으로 토글 가능하다(`rds.logical_replication = 1`). 그 다음은 replication slot을 만들고, 거기서 변경을 뽑아 읽으면 된다.

```sql
-- 출력 플러그인을 지정해 슬롯 생성
SELECT pg_create_logical_replication_slot('demo_slot', 'pgoutput');

-- 시연용: 변경 발생
INSERT INTO orders(id, status) VALUES (1, 'paid');
UPDATE orders SET status = 'shipped' WHERE id = 1;

-- 변경 사항 풀어보기 (pgoutput은 바이너리이므로 실제로는 클라이언트가 디코딩)
-- wal2json을 쓰면 JSON으로 읽기 좋다
SELECT * FROM pg_logical_slot_peek_changes('demo_slot', NULL, NULL);
```

`peek_changes`는 슬롯의 위치(LSN)를 진행시키지 않고 보기만 한다. 실제 소비는 `pg_logical_slot_get_changes`나 streaming replication 프로토콜로 받아 LSN을 advance한다. LSN을 advance하지 않으면 슬롯은 변경 사항을 영원히 잡아 두며, 그 때문에 WAL 파일이 정리되지 않는다. 슬롯이 살아 있는데 컨슈머가 죽어 있으면 디스크가 야금야금 차오른다. 이건 정말 끔찍한 일이다. 운영자에게는 "어느 날 갑자기 디스크가 꽉 찼는데 원인이 뭔지 모르겠다"의 1순위 후보다.

그래서 logical replication slot을 만들었다면 다음 두 가지를 같이 챙기자.

- 모니터링에 `pg_replication_slots.confirmed_flush_lsn`과 `restart_lsn`을 노출한다. 슬롯이 얼마나 뒤처져 있는지(`pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)`)를 알람으로 잡는다.
- "사람이 잠깐 만든 슬롯"이 방치되지 않도록, 슬롯에는 만든 사람과 용도를 댓글처럼 적어두자(예: `slot_name`에 `debezium_search_v1` 같은 명시적 이름을 쓰는 식). 익명 슬롯은 무조건 의심의 대상이 된다.

### wal2json과 pgoutput — 두 출력 플러그인

logical decoding은 "어떤 모양으로 풀어줄지"를 출력 플러그인에 위임한다. 대표적인 두 가지가 `wal2json`과 `pgoutput`이다.

`wal2json`은 변경을 JSON으로 풀어준다. 사람이 읽기 좋고, 디버깅하기 좋다. 외부 익스텐션이라 매니지드 PG에서 지원 여부를 먼저 확인해야 한다. RDS PG는 지원, Aurora PG도 최근 버전은 지원하지만, 자체 운영이라면 직접 설치해야 한다는 차이가 있다.

`pgoutput`은 PG 10부터 내장된 바이너리 출력 플러그인이다. PG의 logical replication이 자기 자신을 위해 만든 포맷이다. 효율적이지만 사람이 읽기 어렵다. Debezium은 두 플러그인 모두를 지원한다.

선택의 기준은 대체로 이렇게 정리할 수 있다.

| 항목 | wal2json | pgoutput |
|------|----------|----------|
| 설치 | 외부 익스텐션 | 내장 |
| 포맷 | JSON (사람이 읽기 좋음) | 바이너리 |
| 매니지드 지원 | RDS/Aurora 일부 지원 | 거의 모두 지원 |
| 디버깅 | 직접 SELECT로 확인 가능 | 클라이언트 디코더 필요 |
| 성능 | 텍스트 직렬화 오버헤드 | 더 효율적 |
| publication 필요 | 아니오 | 예 (테이블 필터 가능) |

`pgoutput`을 쓰면 PG의 publication 문법(`CREATE PUBLICATION ...`)으로 어떤 테이블을 흘려보낼지를 선언적으로 관리할 수 있다는 이점이 있다. wal2json은 슬롯 옵션으로 필터를 거는 방식이라 publication만큼 깔끔하지는 않다. 운영을 길게 가져갈 거라면 pgoutput이 점점 더 마음에 든다. 디버깅 용도로는 wal2json이 여전히 편하다.

### PG 17의 failover slot — 페일오버의 오랜 트라우마를 끊다

logical replication slot에는 오랫동안 운영자들이 안고 살던 고질병이 있었다. **slot이 primary에만 존재한다**는 점. 그러니 primary가 죽고 standby가 승격하면, slot은 새 primary에 없다. CDC 컨슈머는 위치 정보를 잃고 처음부터 다시 시작해야 한다. 페일오버 = CDC 파이프라인 재구축. 이걸 한 번 겪고 나면 "logical replication slot은 가능하면 만들지 말자"는 보수적 운영 문화가 자리 잡는다.

PG 17에서 이 트라우마에 답이 나왔다. **failover-capable replication slot**이다. 슬롯을 standby로 동기화해 두고, standby가 primary로 승격하면 그 슬롯을 그대로 이어 받는다. Debezium 같은 컨슈머는 새 primary에 다시 붙어 원래 LSN에서 이어 읽으면 된다. 페일오버 후에도 컨슈머가 죽지 않는다.

설정은 슬롯 생성 시 옵션 한 줄을 더하는 정도다.

```sql
SELECT pg_create_logical_replication_slot(
  'demo_slot', 'pgoutput', false, false, true  -- 마지막 인자가 failover
);
```

여기에 standby 쪽 `synchronized_standby_slots`와 `sync_replication_slots = on`을 함께 설정해야 한다. 매니지드 PG에서 17 이상이라면 옵션 노출 여부를 먼저 확인하자. 이 기능 하나로 PG 위의 CDC 안정성이 한 단계 올라간다. 17이 나오기 전과 후의 운영 부담이 다른 차원이다.

### 그래서 logical decoding은 언제 쓰는가

logical decoding 그 자체는 도구다. 그 위에 얹는 것이 패턴이다. 가장 흔한 활용 둘은 이렇다.

1. **CDC(Change Data Capture)** — PG의 변경을 Kafka·Elasticsearch·BigQuery 같은 곳으로 흘려보낸다. Debezium이 사실상 표준이다.
2. **Outbox 패턴** — 비즈니스 트랜잭션과 같은 트랜잭션에 outbox row를 적고, 그 row를 logical decoding으로 외부에 푸시한다. 13.4에서 자세히 본다.

LISTEN/NOTIFY가 "가볍지만 영속성 없음"이었다면, logical decoding은 "영속적이며 순서가 보장되지만 운영에 신경 써야 함"이다. 슬롯 모니터링, 페일오버 대비, 출력 플러그인 선택 — 이 셋을 챙기지 않으면 좋은 도구가 발등을 찍는다.

자, 영속적이고 무거운 변경 스트림은 logical decoding으로 해결한다. 그렇다면 "주기적으로 무언가를 돌려야 한다"는 평범한 요구는 어디에 맡길까? 다음 도구로 넘어간다.

## 13.3 pg_cron + pgmq — 스케줄과 영속 큐를 DB 안에

매주 월요일 새벽 3시에 통계 테이블을 갱신해야 한다고 해보자. 가장 흔한 답은 OS의 cron이다. 서버에 SSH로 들어가 `crontab -e`. 새 줄을 하나 더한다. 그런데 그 서버가 죽으면? 그래서 두 대를 띄우고 leader election을 한다. 그러다 보면 cron 한 줄을 위해 인프라가 점점 비대해진다. 번거롭다.

PG 안에서 cron을 돌릴 수 있다면 어떨까. `pg_cron` 익스텐션이 정확히 그 일을 한다.

### pg_cron — DB에 내장된 cron

`pg_cron`은 Citus Data(현재 Microsoft)가 만든 익스텐션이다. cron 표현으로 SQL 또는 함수 호출을 스케줄링한다. 작업 정보는 DB 안 테이블에 들어가므로 페일오버 후에도 그대로 살아 있다(매니지드에서는 보통 primary에만 cron worker가 붙는 식으로 동작한다).

설치 후 첫 cron job은 한 줄이면 된다.

```sql
-- 매일 새벽 3시에 통계 갱신
SELECT cron.schedule(
  'refresh-daily-stats',
  '0 3 * * *',
  $$REFRESH MATERIALIZED VIEW CONCURRENTLY daily_stats$$
);

-- 매분 큐 처리
SELECT cron.schedule(
  'process-jobs',
  '* * * * *',
  $$SELECT process_pending_jobs(100)$$
);
```

작업 이력은 `cron.job_run_details` 테이블에 남는다. 성공·실패·반환 메시지·실행 시간이 그대로 기록된다. "어제 새벽에 batch가 돌긴 했나요?"라는 질문에 SSH 없이 SQL로 답할 수 있다는 점이 의외로 큰 자산이 된다.

매니지드 PG의 지원 현황도 짚자. AWS RDS PG와 Aurora PG는 11 이상에서 `pg_cron`을 지원한다. Supabase는 적극 도입해 콘솔에 cron UI까지 붙여 두었다. GCP Cloud SQL과 AlloyDB도 지원한다. 매니지드를 고를 때 지원 익스텐션 목록을 미리 보는 편이 낫다는 이야기는 책 다른 곳(24장)에서도 반복되니 기억해두자.

`pg_cron`을 쓸 때 주의할 점은 두 가지다.

첫째, **DB의 default database 한 곳에만 cron worker가 붙는다.** RDS는 `cron.database_name` 파라미터로 어느 DB를 쓸지 지정한다. 다른 DB의 작업을 돌리려면 cron job 안에서 `dblink`나 `postgres_fdw`로 우회해야 한다. 처음 만나면 난감한 함정이다.

둘째, **cron job은 superuser 또는 pg_cron 권한이 부여된 역할로 동작한다.** SQL이 어떤 권한으로 돌지를 명시적으로 분리해두지 않으면, 누가 어떤 일을 시킨 건지 추적이 어렵다. 익스텐션의 `cron.schedule_in_database`나 `cron.alter_job`을 활용해 책임자별로 명확히 분리하자.

### pgmq — DB 안의 영속 큐

스케줄러 옆에는 큐가 있어야 마무리가 된다. Outbox 패턴(13.4)으로 충분한 경우도 많지만, "Redis나 SQS처럼 가시성 타임아웃 가지는 진짜 큐"가 필요한 경우도 있다. 그럴 때 `pgmq`(PostgreSQL Message Queue)가 답이 된다.

`pgmq`는 Tembo가 만든 익스텐션으로, AWS SQS·Redis Streams의 인터페이스를 PG 위에 얹어준다. 큐를 만들고, 메시지를 보내고, 읽으면서 가시성 타임아웃을 잡고, 처리 후 삭제하는 흐름이 SQL 함수로 노출된다. 핵심 API는 다섯 개 정도다.

```sql
-- 큐 생성
SELECT pgmq.create('order_jobs');

-- 메시지 발행
SELECT pgmq.send('order_jobs', '{"order_id": 1024, "task": "send_email"}');

-- 읽기 (30초간 다른 컨슈머에게는 보이지 않게 잡아 둠)
SELECT * FROM pgmq.read('order_jobs', vt => 30, qty => 5);

-- 처리 완료 후 삭제
SELECT pgmq.delete('order_jobs', msg_id => 42);

-- 또는 한 번에: pop
SELECT * FROM pgmq.pop('order_jobs');
```

`vt`는 visibility timeout이다. SQS와 같다. 컨슈머가 메시지를 읽고 처리하는 동안 30초 잠가 두고, 처리 후 `delete`로 지운다. 처리에 실패해 30초가 지나면 메시지가 다시 보이게 된다. 자연스럽게 재시도가 된다.

내부 구현은 단순하다. 큐는 일반 테이블이고, 메시지는 row다. 가시성은 `vt` 컬럼(visible_at 타임스탬프)으로 표현한다. `read`는 본질적으로 `SELECT ... FOR UPDATE SKIP LOCKED`다. 동시 컨슈머가 같은 메시지를 잡지 않게 막아주는 게 그 패턴의 핵심이다.

`SKIP LOCKED`는 PG 9.5부터 들어왔다. 이 한 줄이 PG를 큐로 쓰는 길을 열었다. 그 전에는 동시 컨슈머가 같은 행에서 락을 두고 충돌하느라 throughput이 처참했다. `SKIP LOCKED`가 생기면서 "잠긴 행은 건너뛰고 다음 행을 봐"가 가능해졌고, 그 위에 `pgmq` 같은 익스텐션이 얹혔다.

### 그래서 PG 큐는 어디까지 쓸 수 있는가

`pgmq`의 throughput은 일반 PG의 OLTP throughput과 같은 자리에서 논의된다. 잘 튜닝된 PG가 수천에서 수만 TPS를 받아낸다는 것을 알고 있으니, 큐도 그 정도 범위에서 동작한다. 초당 수만 메시지면 대부분의 비즈니스 시스템에 충분하다. SQS·Kafka로 가야 하는 자리는 그 위, 초당 수십만~수백만 단위의 영역이다.

`pgmq`와 `pg_cron`을 짝지으면 "정기적으로 깨어나 큐를 비우는 워커"를 SQL만으로 구성할 수 있다.

```sql
-- 컨슈머 함수
CREATE OR REPLACE FUNCTION process_order_jobs(batch_size int)
RETURNS int AS $$
DECLARE
  msg record;
  processed int := 0;
BEGIN
  FOR msg IN
    SELECT * FROM pgmq.read('order_jobs', 30, batch_size)
  LOOP
    BEGIN
      PERFORM handle_order_job(msg.message);
      PERFORM pgmq.delete('order_jobs', msg.msg_id);
      processed := processed + 1;
    EXCEPTION WHEN OTHERS THEN
      -- 실패 시 vt가 끝나면 자동 재시도
      RAISE WARNING 'job % failed: %', msg.msg_id, SQLERRM;
    END;
  END LOOP;
  RETURN processed;
END;
$$ LANGUAGE plpgsql;

-- 매분 100건씩 처리
SELECT cron.schedule('drain-orders', '* * * * *',
  $$SELECT process_order_jobs(100)$$);
```

이렇게 짜면 별도 워커 프로세스도, 별도 메시지 브로커도 없다. DB 한 대로 큐와 워커 스케줄을 함께 굴린다. 작은 팀에는 이만큼 깔끔한 출발점이 드물다. 그렇다면 트랜잭션 안전성까지 챙겨야 할 때는 어디로 가야 할까? Outbox 패턴이 그 답이다.

## 13.4 Outbox + logical replication — 트랜잭션이 보장하는 이벤트 발행

다음 시나리오를 떠올려보자. 주문이 들어왔다. 어플리케이션은 두 가지 일을 해야 한다.

1. `orders` 테이블에 행을 적는다.
2. 외부 시스템(검색 인덱스, 알림 서비스, 분석 파이프라인)에 `OrderCreated` 이벤트를 푸시한다.

가장 흔한 첫 구현은 이렇다. DB에 INSERT 하고 → 그 다음 줄에서 Kafka에 publish 한다. 둘이 한 트랜잭션처럼 묶여 있는 것처럼 보인다. 그런데 둘 사이의 어딘가에서 어플리케이션이 죽는다면? DB에는 행이 들어갔는데 Kafka 메시지는 안 나갔다. 또는 Kafka에는 갔는데 DB 커밋이 실패했다. **분산 트랜잭션의 묵은 통증**이 그대로 재현된다.

XA 같은 분산 트랜잭션 매니저로 묶을 수도 있겠지만, 운영 부담이 만만치 않고 성능도 떨어진다. 대부분의 시스템은 이 길을 가지 않는다. 대신 우회로를 택한다. 그 우회로의 이름이 **Outbox 패턴**이다.

### 발상의 핵심

DB와 Kafka를 한 트랜잭션으로 묶을 수 없다면, 한 트랜잭션 안에서 끝나는 일만 하자. 비즈니스 변경과 함께 "내가 발행해야 할 이벤트"를 같은 DB의 같은 트랜잭션에 적어두는 것이다. 그 테이블을 outbox 테이블이라 부른다.

```sql
CREATE TABLE outbox (
  id          bigserial PRIMARY KEY,
  aggregate   text       NOT NULL,
  event_type  text       NOT NULL,
  payload     jsonb      NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT now()
);

-- 비즈니스 트랜잭션
BEGIN;
  INSERT INTO orders(id, status, total)
  VALUES (1024, 'paid', 49000);

  INSERT INTO outbox(aggregate, event_type, payload)
  VALUES (
    'order',
    'OrderCreated',
    jsonb_build_object('order_id', 1024, 'total', 49000)
  );
COMMIT;
```

비즈니스 변경과 이벤트 기록은 하나의 트랜잭션 안에 있다. 둘 다 커밋되거나, 둘 다 롤백된다. 중간이 없다. 가장 단순하고 가장 강한 보장이다.

이제 남은 문제는 outbox에 적힌 row를 어떻게 외부로 보내느냐다. 두 가지 접근이 있다.

### Polling 방식 — 단순하지만 지연이 있다

가장 단순한 답은 폴링이다. 워커 하나가 주기적으로 outbox를 본다.

```sql
SELECT * FROM outbox
WHERE published_at IS NULL
ORDER BY id
LIMIT 100
FOR UPDATE SKIP LOCKED;
```

읽은 후 외부에 publish하고, `published_at`을 갱신한 다음 COMMIT. 실패하면 다음 폴링이 잡아낸다. `SKIP LOCKED` 덕분에 여러 워커를 띄워도 같은 row를 두 번 처리하지 않는다.

장점은 단순하다는 것. 단점은 폴링 주기만큼 지연이 발생하고, outbox 테이블이 계속 커지므로 정리해야 한다는 것이다. 13.1의 LISTEN/NOTIFY를 짝지어 "INSERT 시점에 워커 깨우기"까지 더하면 폴링 주기를 길게 두고도 즉시성을 살릴 수 있다. 작은 시스템이라면 이 조합으로 충분하다.

### Push 방식 — logical decoding으로 outbox를 끌어낸다

규모가 커지거나 지연을 더 줄이고 싶다면 push로 간다. outbox 테이블에 logical decoding의 publication을 걸어두고, Debezium이나 자체 컨슈머가 행이 들어오는 즉시 받아 외부로 보낸다.

```sql
ALTER TABLE outbox REPLICA IDENTITY FULL;

CREATE PUBLICATION outbox_pub FOR TABLE outbox;

-- Debezium 또는 pgoutput 클라이언트가 슬롯에서 변경을 받는다
SELECT pg_create_logical_replication_slot('outbox_slot', 'pgoutput');
```

Debezium의 **Outbox Event Router**가 사실상 이 패턴의 레퍼런스 구현이다. outbox row를 Kafka 토픽으로 라우팅하면서, `aggregate` 컬럼을 토픽 이름으로, `id`를 메시지 키로 매핑한다. 이렇게 두면 각 aggregate별 메시지 순서가 보장되고, 컨슈머는 보통의 Kafka 컨슈머와 같은 방식으로 처리한다.

이 패턴의 매력은 분명하다. **어플리케이션 코드에서는 Kafka가 안 보인다.** 어플리케이션은 DB만 쓴다. Kafka는 운영팀이 따로 굴리고, 컨슈머도 따로 굴린다. 어플리케이션이 죽어도 Debezium은 LSN을 기억하고 있으니 다시 살아나 그 자리부터 이어 보낸다. "비즈니스 트랜잭션 = 이벤트 발행"이라는 한 줄의 약속이 그대로 지켜진다.

### outbox 테이블 청소

push든 polling이든, outbox는 행이 계속 쌓인다. 영원히 두면 테이블이 부풀고 vacuum 부담이 커진다. 보통은 두 가지 전략 중 하나를 쓴다.

- **TTL 삭제.** 발행된 지 N일 지난 행을 `pg_cron`으로 매일 한 번 삭제한다.
- **파티셔닝 + 드롭.** outbox를 일자별·주별로 PARTITION BY RANGE 해 두고, 오래된 파티션을 통째로 DROP한다. DELETE보다 훨씬 가볍고 bloat가 안 쌓인다.

파티셔닝 쪽이 운영적으로 안정적이라 큰 시스템에서는 점점 표준에 가까워진다. 그리고 outbox의 `id`가 bigserial이라면 wraparound 위험도 의식해두자. bigint면 사실상 안전하지만, integer로 잘못 선언했다가 23억 건 돌파 후 발등을 찍는 사례가 종종 들린다. 처음부터 `bigserial` 또는 `bigint generated by default as identity`로 두는 편이 낫다.

### Outbox가 주는 진짜 선물

Outbox 패턴은 "분산 트랜잭션을 피하면서 이벤트 발행을 트랜잭션에 묶는다"는 기술적 문제를 푼다. 그런데 더 큰 선물이 있다. **이벤트 발행의 책임을 한 곳에 모은다**는 점이다.

서비스 곳곳에서 Kafka 클라이언트를 직접 들고 publish 하는 코드는 시간이 지나면 흩어진다. 누가 무엇을 발행하는지 파악이 어려워진다. outbox 테이블 하나에 모이는 패턴을 도입하면, 발행되는 모든 이벤트는 SQL 한 번이면 다 볼 수 있다. 감사·재처리·디버깅이 비교할 수 없을 만큼 쉬워진다. "어제 OrderCreated가 몇 건 나갔지?"라는 질문에 `SELECT count(*) FROM outbox WHERE ...` 한 줄로 답한다. 이 자산이 의외로 든든하다.

한 가지 더 짚어두자. **outbox는 멱등성(idempotency)을 컨슈머 쪽에 강제로 요구한다.** at-least-once 전달이기 때문이다. 같은 메시지가 두 번 전달될 가능성이 0이 아니다(워커가 publish 후 commit 직전에 죽으면 다음 폴링이 같은 행을 다시 처리한다). 컨슈머는 메시지의 식별자(예: outbox `id`)를 키로 두고 중복을 막아야 한다. 이 한 줄의 규칙을 합의해 두지 않으면 어딘가에서 "주문 알림이 두 번 갔다", "재고가 두 번 차감됐다" 같은 사건이 터진다. 멱등성은 분산 시스템의 디폴트 약속이지만, outbox 패턴을 처음 도입하는 팀은 이 약속을 잊기 쉽다. 컨슈머 쪽 코드 리뷰 체크리스트에 "이 핸들러는 멱등한가?"를 박아두는 편이 낫다.

자, 여기까지 따라오면 어떤 그림이 보인다. PG 안에서 가벼운 알림(LISTEN/NOTIFY), 변경 캡처(logical decoding), 영속 큐(pgmq), 트랜잭션 안전한 발행(Outbox)까지 다 된다. 그렇다면 Kafka는 정말 필요한가? 이 질문을 정면으로 보자.

## 13.5 "Just Use Postgres" — Kafka 도입을 미루는 의사결정

요즘 영어권 개발자 커뮤니티에서 한동안 회자된 표어가 있다. **"Just Use Postgres"**. Vonng의 "Postgres is eating the database world" 같은 글이 HN에서 회자되며 더 굳어졌다. 요지는 단순하다. MySQL + Kafka + RabbitMQ + Elasticsearch + MongoDB + Redis로 흩어져 있던 인프라를 PG 하나로 모을 수 있고, 중소 규모라면 그쪽이 운영이 더 행복하다는 주장이다.

물론 ‘만능 망치’ 논리는 위험하다. 그렇다고 반대 극단, ‘새 서비스마다 새 미들웨어’도 위험하긴 마찬가지다. 어디까지 PG로 가고 어디부터 dedicated로 넘어가는지의 선을 함께 그어보자.

### Kafka가 진짜 필요할 때 — 세 가지 기준

Kafka를 도입할지 말지의 판단은 다음 세 가지 기준으로 가지치기하면 깔끔하다.

**1. 처리량의 자릿수.** 초당 메시지가 어디쯤인가?

- **초당 ~1만 건:** PG + Outbox + pgmq로 충분하다. 잘 튜닝된 PG는 이 자리에서 안정적으로 동작한다.
- **초당 1만~10만 건:** PG로 가능은 하다. 다만 vacuum·bloat·디스크 IO에 신경 써야 한다. outbox 파티셔닝과 컨슈머 병렬화가 필수.
- **초당 10만 건 이상:** Kafka의 영역이다. 이 자리에서 PG를 우기는 일은 무리수다. log-structured 설계와 분산 파티션이 주는 throughput 이점이 결정적으로 크다.

**2. 보존 기간.** 메시지를 얼마나 오래 들고 있어야 하는가?

이벤트를 "수일 보관 후 폐기" 정도라면 PG 안에서 파티셔닝으로 충분하다. "수개월~수년 보관 + 새 컨슈머가 처음부터 재생"이 필요하다면 Kafka의 retention과 compacted topic이 어울린다. 이벤트 소싱(event sourcing) 아키텍처처럼 모든 이벤트가 진실의 원천이 되는 설계라면 Kafka가 더 자연스럽다.

**3. 컨슈머 다양성.** 같은 이벤트를 몇 가지 시스템이 동시에 소비하는가?

컨슈머가 1~3개라면 PG에 publication을 여러 개 두거나 Debezium 한 줄로 흘려 보낸다. 컨슈머가 5개 이상으로 늘어나기 시작하면 Kafka의 토픽·컨슈머 그룹 모델이 본격적인 가치를 보인다.

세 기준 중 하나라도 Kafka 쪽으로 분명하게 기울면 그때 Kafka로 가자. 셋 다 PG로 충분한 자리에서 Kafka를 먼저 가져오는 일은, 작은 팀에게는 운영 부담을 사서 짊어지는 일이 된다.

### 미루기의 경제학

Kafka 도입을 미룬다고 해서 영원히 안 쓰겠다는 뜻이 아니다. **필요해질 때까지 미룬다**는 뜻이다. 그 사이에 얻는 것이 무엇인가?

- **인프라 단순성.** 모니터링·백업·페일오버를 PG 한 클러스터에 모은다. 사람이 익혀야 할 도구가 하나 줄어든다.
- **트랜잭션 보장.** outbox 패턴으로 비즈니스 변경과 이벤트 발행을 한 트랜잭션에 묶는다. Kafka 직접 publish의 "DB와 Kafka 사이가 새지 않게 하라"는 영원한 숙제가 사라진다.
- **운영 가시성.** 모든 이벤트가 SQL로 보인다. 감사·재처리·디버깅의 비용이 낮다.
- **온보딩 비용.** 신규 입사자가 익혀야 할 미들웨어가 하나 줄어든다. PG는 어차피 쓰니까.

그리고 결정적으로 — **나중에 Kafka로 옮기는 길이 막히지 않는다.** outbox 패턴 위에서 push하던 컨슈머를 Debezium + Kafka로 갈아끼우는 일은 그렇게 어렵지 않다. outbox 스키마는 그대로 두고, 라우터만 바꾸면 된다. 미루기의 결정이 한 방향 문(one-way door)이 아니라 양방향 문이라는 점이 핵심이다.

### 미루지 말아야 할 자리

반대로, PG로 욱여넣지 말아야 할 자리도 분명히 있다.

- **로그 수집·메트릭 파이프라인.** 초당 수십만 건의 로그를 PG로 받으려는 시도는 처참하게 실패한다. 이건 Kafka·Kinesis·Fluentd의 영역이다.
- **이벤트 소싱이 시스템의 중심 사상인 아키텍처.** 이벤트가 진실의 원천이고, 모든 상태가 이벤트의 폴드(fold)로 만들어진다면, Kafka의 log abstraction이 거의 그 사상과 일대일로 맞다. PG outbox로도 못할 건 없지만, 어울리는 도구가 명확하면 그쪽을 쓰자.
- **외부 시스템과의 표준 인터페이스로서의 이벤트.** 협력사가 "Kafka 토픽 X에 publish 해주세요"라고 요구하는 자리. 외부 계약이 Kafka라면 미루기의 의미가 없다.
- **수십 개 마이크로서비스가 같은 이벤트 위에 합의해 동작해야 하는 자리.** 한두 컨슈머라면 PG로 충분하지만, 컨슈머가 늘어날수록 Kafka의 토픽·컨슈머 그룹·offset 관리 모델이 가진 운영적 가치가 분명해진다. 처음에는 PG로 시작했다가 컨슈머가 늘면서 Kafka로 이주하는 것이 자연스러운 경로다.

### 결정 트리

세 절의 도구를 다 본 입장에서, 결정 트리를 그려두면 이렇다.

```
이벤트가 영속적이어야 하는가?
├── 아니오 → LISTEN/NOTIFY (캐시 무효화, 워커 깨우기)
└── 예
    ├── 트랜잭션과 함께 발행되어야 하는가?
    │   ├── 예 → Outbox 패턴
    │   │   ├── 컨슈머 polling으로 충분 → outbox + polling worker
    │   │   └── 즉시성 필요 → outbox + logical decoding (Debezium)
    │   └── 아니오 → pgmq (visibility timeout 가지는 큐)
    └── 처리량 또는 컨슈머 수가 한계 너머인가?
        └── 예 → Kafka (이때만 도입)
```

이 트리의 마지막 가지가 "이때만 도입"이라는 점이 중요하다. **Kafka는 도구이지 디폴트가 아니다.** 디폴트는 PG이고, 디폴트가 무너지는 자리에서 Kafka가 등장한다. 그 자리가 어디인지 알고 있을 때만 Kafka가 가진 진짜 가치가 산다.

### 미루기 결정에 따라붙는 잔소리 하나

"Just Use Postgres"는 표어가 듣기 좋아서 인기를 끈다. 그런데 표어에 휘둘려 "다 PG로 하면 된다"고 단정 짓는 일은 위험하다. 표어의 진짜 메시지는 "**무엇이 진짜 필요한가를 먼저 묻고, 디폴트는 PG로 두자**"에 가깝다. 진짜 필요가 분명하다면 Kafka도 ES도 Redis도 데리고 오자. 다만 "남들이 쓰니까", "트렌드니까", "나중에 큰일 났을 때 후회할까봐" 같은 막연한 두려움으로 미들웨어를 늘리는 일은 미루는 편이 낫다.

작은 팀일수록 운영 인력은 한정되어 있고, 운영해야 할 시스템 수가 늘면 한 시스템당 들이는 깊이가 얕아진다. PG 한 클러스터를 깊게 운영하는 팀이, 다섯 미들웨어를 얕게 운영하는 팀보다 사고를 덜 친다. 이 단순한 사실을 기억해두자.

자, 결정 트리가 그려졌으니 마지막으로 실제 사례 하나를 본다. 한국 회사가 PG 위에서 어떤 CDC 파이프라인을 굴리고 있는지를. 다만 거듭 강조하자. 여기서는 "패턴이 이렇게 생겼다"의 시연이다. "왜 그 결정이었는가"의 해부는 25장의 몫이다.

## 13.6 카카오 클린플랫폼 CDC — 패턴이 이렇게 생겼다

카카오의 클린플랫폼은 카카오의 여러 서비스에 들어오는 신고·욕설·스팸 같은 콘텐츠를 감지하고 분류·처리하는 시스템이다. 이 시스템은 PostgreSQL을 OLTP 저장소로 쓰고, 검색·분석은 Elasticsearch에 맡긴다. 두 저장소 사이에 PostgreSQL → Kafka Connect → Elasticsearch의 CDC 파이프라인을 두어, PG가 업데이트되면 Elasticsearch 인덱스가 곧 따라잡는 구조다.

이 절에서는 그 파이프라인이 **기술적으로 어떻게 생겼는지**만 본다. 카카오가 왜 그 결정을 했는지, 운영하면서 무엇이 어려웠는지, 무엇을 얻었는지는 25장에서 해부한다.

### 파이프라인 모양

```
[Application] ──write──▶ [PostgreSQL]
                              │
                              │ logical decoding (wal2json or pgoutput)
                              ▼
                       [replication slot]
                              │
                              ▼
                  [Kafka Connect (Debezium PG Source)]
                              │
                              ▼
                          [Kafka]
                              │
                              ▼
                 [Kafka Connect (Elasticsearch Sink)]
                              │
                              ▼
                      [Elasticsearch]
```

핵심 부품은 셋이다.

1. **PostgreSQL의 logical decoding 슬롯.** WAL을 풀어 외부로 흘려보내는 원천.
2. **Debezium PostgreSQL Source Connector.** Kafka Connect 위에서 슬롯을 구독해 변경을 Kafka 토픽으로 보낸다.
3. **Elasticsearch Sink Connector.** Kafka에서 토픽을 읽어 ES 인덱스로 색인한다.

가운데 Kafka가 있는 이유는 단순하다. **PG의 쓰기 속도와 ES의 색인 속도가 다르다.** 그 차이를 흡수할 버퍼가 필요하다. 또 ES만이 컨슈머인 게 아니라 분석 파이프라인이나 알림 서비스 같은 다른 컨슈머가 추가될 수 있는 자리이기도 하다. 컨슈머 다양성과 속도 차 흡수, 두 가지가 가운데 Kafka의 존재 이유다(이 결정의 배경은 25장에서 더 깊이 본다).

### 변경 모양

테이블 한 줄이 바뀌면 Debezium은 다음 같은 envelope을 만들어 Kafka로 보낸다(개략적인 모양이다).

```json
{
  "before": {
    "id": 1024,
    "status": "pending",
    "score": null
  },
  "after": {
    "id": 1024,
    "status": "flagged",
    "score": 0.87
  },
  "source": {
    "version": "2.x",
    "connector": "postgresql",
    "db": "cleanplatform",
    "schema": "public",
    "table": "reports",
    "txId": 8821023,
    "lsn": 1672349712384
  },
  "op": "u",
  "ts_ms": 1700000000000
}
```

`before`/`after`로 변경 전후를 모두 들고 있다. ES Sink Connector는 `after`를 인덱싱하면 되고, 삭제(`op: d`)면 ES에서 문서를 지운다. 이 일관된 envelope이 컨슈머 쪽 코드를 단순하게 만든다. 컨슈머는 "내가 어떤 테이블의 어떤 변경에 반응하는가"만 결정하면 된다.

### REPLICA IDENTITY — 잊지 말자

logical decoding으로 흘려보낼 테이블에는 `REPLICA IDENTITY`를 챙겨야 한다. 기본은 `DEFAULT` — primary key만 `before`에 담긴다. 변경 전 모든 컬럼을 보고 싶으면 `FULL`이 필요하다.

```sql
ALTER TABLE reports REPLICA IDENTITY FULL;
```

`FULL`은 토스트되지 않은 모든 컬럼을 `before`에 포함시키는 대신 WAL 사이즈를 키운다. 큰 테이블에 일률적으로 걸면 WAL 폭증의 원인이 된다. 컨슈머가 정말로 `before` 전체를 봐야 하는 테이블에만 선택적으로 거는 편이 낫다. 변경 검출만 필요하다면 `DEFAULT`로 충분하다.

또 한 가지 잊지 말 점. `REPLICA IDENTITY FULL`을 거는 테이블에는 모든 컬럼에 대한 인덱스가 없어도 동작하지만, UPDATE/DELETE 시 standby가 행을 찾는 비용이 올라간다. 운영 부담이 어느 자리에서 늘어나는지 모르고 켜뒀다가 어느 날 갑자기 무거워진 워크로드의 원인을 찾는 데에 한참을 헤매기 쉽다.

### 슬롯 모니터링 — 다시 한번

13.2에서 이미 짚었지만 한 번 더. logical replication slot은 컨슈머가 advance하지 않으면 WAL을 잡아 둔다. CDC 파이프라인을 운영한다면 다음 두 메트릭을 알람으로 잡아두자.

- `pg_replication_slots.active` — 컨슈머가 붙어 있는지.
- `pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)` — 슬롯이 얼마나 뒤처져 있는지(바이트).

뒤처짐이 1GB를 넘어가기 시작하면 컨슈머가 처리 속도를 못 따라가고 있다는 신호다. 10GB를 넘기 시작하면 디스크가 위태롭다. 100GB를 넘기 시작하면 무언가 단단히 잘못된 것이다. 임계치는 클러스터 디스크 크기에 맞게 잡으면 된다.

### 17 failover slot이 가져온 변화

카카오처럼 24/7 운영되는 시스템에서 페일오버 = CDC 재구축은 큰 트라우마였다. primary가 죽으면 standby가 승격하고, 슬롯은 잃고, CDC 컨슈머는 처음부터 다시 읽어야 한다. 그 사이의 변경은 어떻게 다시 흘려보낼까. 보통은 ES 인덱스를 처음부터 다시 만드는 백필(backfill) 작업으로 이어진다. 며칠씩 시간이 든다.

PG 17의 failover slot은 이 트라우마에 끝이 보이게 했다. 슬롯이 standby로 동기화되고, 페일오버 후에도 슬롯이 살아남는다. Debezium은 새 primary에 다시 붙어 원래 LSN에서 이어 읽는다. CDC 파이프라인이 페일오버를 한 사이에 잠깐 멈췄다가 그대로 이어진다.

이 한 줄의 변화가 PG 위 CDC의 안정성을 한 단계 끌어올린다. CDC를 본격적으로 운영하는 모든 시스템에 PG 17 이상이 권장되는 이유다. 매니지드 PG를 고를 때 failover slot 지원 여부를 확인해두자(2026년 현재 RDS·Aurora·Cloud SQL·AlloyDB 모두 17 이상에서 지원).

### 이 패턴이 보여주는 것

카카오 클린플랫폼 CDC는 13장에서 본 모든 조각이 실제로 어떻게 합쳐지는지를 보여주는 자리다.

- **logical decoding**이 원천을 만든다.
- **Outbox 패턴**까지는 가지 않지만, Debezium의 envelope이 그와 비슷한 역할을 한다(변경의 책임 분리).
- **Kafka가 가운데에 있다.** 13.5의 결정 트리에서 "컨슈머 다양성"과 "속도 차 흡수"가 Kafka 쪽으로 가지친 자리다.
- **REPLICA IDENTITY, 슬롯 모니터링, failover slot** — 운영 디테일이 빠지면 좋은 도구가 발등을 찍는다는 13.2의 경고가 그대로 살아 있다.

다시 강조하자. 여기까지가 "패턴이 이렇게 생겼다"의 시연이다. **왜 카카오는 PG → Kafka → ES를 택했는가? wal2json과 pgoutput 사이에서 무엇을 골랐는가? 운영하면서 가장 아팠던 자리는 어디였는가? 다시 한다면 무엇을 다르게 할 것인가?** 이 질문들의 답은 25장 한국 사례에서 본격적으로 펼쳐진다.

## 마무리

이 장에서 같이 따라온 길을 정리해두자.

PG는 메시지 버스로서 세 층의 도구를 가진다. **가벼운 알림은 LISTEN/NOTIFY**, **변경 캡처는 logical decoding**, **스케줄과 영속 큐는 pg_cron과 pgmq**. 그 위에 **Outbox 패턴**이 트랜잭션 안전한 이벤트 발행이라는 묵은 통증에 우아한 답을 준다.

이 도구들을 쥐고 있다는 사실은 의외로 중요한 자유를 만들어낸다. **"메시지 큐가 필요하니까 Kafka 클러스터를 띄우자"**가 더 이상 첫 답이 아니어도 된다. 초당 1만 건 이하, 컨슈머 1~3개, 보존 기간 수일 이내라면 PG 한 클러스터로도 충분히 깔끔하다. Kafka는 도구이고, 디폴트가 아니다. 그 자리가 분명히 와야 도입할 가치가 산다.

그리고 PG 17의 failover slot 덕분에 CDC가 페일오버에 강해졌다는 변화도 잊지 말자. logical replication slot의 오랜 트라우마를 풀어준 한 줄이다. 새로 시작하는 CDC 파이프라인이 있다면 PG 17 이상을 디폴트로 고려하자.

마지막으로 한 가지 당부를 두고 가자. 13.6의 카카오 사례에서 우리는 패턴의 시연만 봤다. 그 결정의 무게는 25장에서 다시 만난다. 그때는 "왜였는가"를 묻는다. 그 전에 14장에서는 logical decoding과 같은 뿌리에서 자란 또 다른 가지 — FDW와 CDC와 동기화 — 로 넘어간다. 여러 DB가 흩어진 환경에서 PG를 데이터 허브로 만드는 길이 거기에 있다.
