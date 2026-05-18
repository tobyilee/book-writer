# 7장. WAL과 SSI — 모든 기능의 토대

PostgreSQL을 오래 써온 사람에게 한 가지 질문을 던져 보자. "PG가 자랑하는 기능을 다섯 개만 골라 본다면 무엇이겠는가?" 누군가는 스트리밍 복제를 말할 것이다. 누군가는 Debezium 같은 CDC 파이프라인을 들 것이다. 또 누군가는 PITR — 사고 시각 1분 전으로 클러스터를 되돌리는 그 짜릿한 능력을 꺼낼 것이다. 금융 시스템을 다뤄 본 사람이라면 SERIALIZABLE 격리 수준이 실제로 작동한다는 사실을 들 것이고, 운영자라면 크래시 후의 자동 복구를 첫 줄에 둘 것이다.

그런데 이 다섯 가지가 사실은 하나의 메커니즘에서 갈라져 나왔다고 하면 어떨까? 그것도 1992년 ARIES 논문 한 편에서 시작된, 이름조차 단출한 한 줄짜리 약속 — "데이터를 디스크에 쓰기 전에 로그를 먼저 쓴다(Write-Ahead)" — 그것 하나에서.

PostgreSQL의 거의 모든 자랑은 WAL 하나로 거슬러 올라간다. 복제도, CDC도, PITR도, 진짜 직렬화도 다 거기서 나온다. 한 번 제대로 들여다볼 만하지 않을까? 그리고 이 토대 위에 9.1부터 얹힌 또 하나의 보석 — SSI(Serializable Snapshot Isolation)까지 같이 살펴보자. 이번 장이 끝날 무렵에는, 책 나머지 절반(Part 3와 Part 4)이 어떤 단일 기반 위에 서 있는지 손에 잡힐 것이다.

## 7.1 WAL의 형식과 흐름

먼저 한 가지 상황을 가정해 보자. 은행 시스템에서 누군가의 계좌에 100만 원을 이체하는 트랜잭션이 시작됐다고 하자. UPDATE가 한 줄 돌고, COMMIT이 떨어진다. 클라이언트에게는 "성공"이라는 응답이 나갔다. 바로 그 순간, 서버 전원이 뽑힌다. 정전이든 누군가의 발길질이든 상관없다. 메모리에 있던 모든 페이지는 사라졌다. 디스크에 적힌 데이터 파일은 아직 갱신되기 전이다.

이때 시스템이 다시 살아나면 어떤 일이 벌어져야 할까? "성공"이라고 답한 그 100만 원의 이체는 반드시 살아 있어야 한다. 그렇지 않으면 클라이언트가 본 응답은 거짓말이 된다. DB가 거짓말을 하는 순간, 그 위에 쌓아 올린 모든 비즈니스가 무너진다.

이 문제를 푸는 가장 단순한 답은 — "데이터를 디스크에 적은 다음에야 클라이언트에게 성공이라고 말한다"는 약속이다. 그런데 이 단순한 답에는 치명적인 비용이 따른다. 트랜잭션 하나마다 데이터 페이지를 디스크에 강제로 내려 써야 한다. 페이지는 8KB짜리 블록이고, 한 트랜잭션이 건드리는 row가 다섯 줄이라면 적어도 다섯 페이지를 fsync 해야 한다. 디스크 헤드는 페이지마다 다른 위치로 점프한다. 랜덤 I/O의 지옥이다. TPS는 바닥을 친다.

그렇다면 어떻게 해야 할까? 1992년 IBM의 Mohan 등이 쓴 ARIES 논문이 답을 제시했다. **변경 사실 자체를 작은 레코드로 만들어, 순차 로그에 먼저 쓰는 것이다.** 이 로그가 디스크에 안전히 안착했다면, 실제 데이터 페이지가 아직 디스크에 안 내려가 있더라도 COMMIT으로 인정해도 좋다. 왜냐하면 — 시스템이 죽고 다시 살아났을 때 그 로그를 다시 읽으면 잃어버린 변경을 재현할 수 있기 때문이다. 이것이 Write-Ahead Logging, 줄여서 WAL이다.

PostgreSQL의 WAL이 어떻게 생겼는지 살펴보자. 디스크 상으로는 `$PGDATA/pg_wal/` 디렉터리 아래에 16MB(기본값) 크기의 세그먼트 파일들이 차곡차곡 쌓인다. 파일명은 `000000010000000000000001` 같은 24자리 16진수로, 앞 8자리는 timeline ID, 가운데 8자리는 로그 ID, 뒤 8자리는 세그먼트 번호다. 세그먼트가 가득 차면 자동으로 다음 세그먼트가 생긴다. 이 파일들 안에는 변경 레코드가 순차적으로 append-only로 쌓여 있다.

각 레코드는 LSN(Log Sequence Number)이라는 단조 증가하는 위치값으로 식별된다. LSN은 `0/16B7378` 같은 형태로 보이는데, 슬래시 앞은 로그 파일 번호의 상위 비트, 뒤는 파일 내 바이트 오프셋이다. 트랜잭션이 어떤 변경을 한 뒤 COMMIT을 발사하면, 해당 COMMIT 레코드의 LSN까지 로그가 디스크에 fsync 되어야 비로소 "정말 커밋됐다"고 말할 수 있다. 이 fsync 약속을 지키는 함수가 PG 내부의 `XLogFlush()`다.

흐름은 이렇다. 백엔드 프로세스가 트랜잭션을 처리하면서 발생시키는 변경은 일단 메모리 상의 **WAL buffer**(`wal_buffers` 파라미터로 크기 조절)에 쓰여진다. COMMIT 시점에 백엔드가 직접 fsync 하거나, 또는 별도의 백그라운드 프로세스인 **WAL writer**가 주기적으로(`wal_writer_delay`, 기본 200ms) 비워 준다. 데이터 페이지 자체는 **checkpointer**라는 또 다른 백그라운드가 훨씬 느슨한 주기(`checkpoint_timeout`, 기본 5분)로 dirty 페이지를 디스크로 흘려 보낸다. 핵심은 — **데이터 페이지보다 WAL 레코드가 항상 먼저 디스크에 안착한다**는 순서가 깨지지 않는 것이다.

크래시 복구는 이 순서 덕분에 가능해진다. PG가 다시 켜질 때, 마지막 체크포인트 이후의 WAL 레코드를 모두 다시 재생(replay)한다. 페이지에 적용됐는지 안 됐는지는 페이지 헤더의 LSN을 보면 안다. 페이지의 LSN이 WAL 레코드의 LSN보다 작으면 — 아직 적용 안 된 것이므로 재생한다. 크면 — 이미 적용된 것이므로 건너뛴다. 이걸 IDempotent하게 만든 것이 ARIES의 첫 번째 기여다.

여기서 한 가지 의문이 생긴다. "그러면 트랜잭션 하나당 fsync는 반드시 한 번씩 일어나는가? 그것도 결국 비용 아닌가?" 맞다. 그래서 PG는 **group commit**이라는 기술을 쓴다. 여러 백엔드가 거의 동시에 COMMIT을 요청하면, WAL을 한 번의 fsync로 묶어서 내린다. `commit_delay`(기본 0, 보통 안 건드림)와 `commit_siblings`로 조절할 수 있다. OLTP 시스템처럼 동시에 많은 짧은 트랜잭션이 도는 환경에서는 group commit이 디스크 I/O를 극적으로 줄여 준다. fsync 한 번에 수십 개의 COMMIT이 묶이는 광경이 흔하다.

그리고 또 하나 — **full_page_writes**. PG는 체크포인트 직후 처음으로 변경되는 페이지에 대해서, 변경 레코드만이 아니라 **페이지 전체**를 WAL에 박아 넣는다. 왜 그럴까? OS가 8KB 페이지를 디스크에 쓰는 도중 전원이 끊기면 — 페이지가 반쪽만 적힌 "torn page"가 될 수 있다. 이 페이지에는 일부 비트는 새 값, 일부 비트는 옛 값이 섞여 있어서 그대로는 신뢰할 수 없다. full_page_writes를 켜 두면, 복구 시 WAL에 박힌 페이지 전체를 그대로 덮어 쓸 수 있어 안전하다. 켜 두는 편이 낫다. 켜지 않으면 데이터 파일이 silent corruption으로 미끄러질 위험이 생긴다.

물론 full_page_writes는 비용이 있다. 체크포인트 직후의 WAL 양이 폭증한다. 그래서 운영에서는 `checkpoint_timeout`을 너무 짧게 두지 말자(기본 5분이지만 OLTP에서는 15~30분으로 늘리는 경우가 많다)는 권고가 나온다. 체크포인트가 자주 일어날수록, 다음 체크포인트까지 누적되는 "처음 변경 페이지" 비율이 커져서 WAL이 부풀기 때문이다.

WAL이 실제로 어떻게 생겼는지 한 번 들여다보자. PG에 내장된 `pg_waldump` 명령으로 세그먼트의 내용을 사람이 읽을 수 있게 풀어 볼 수 있다. 출력의 한 줄은 대략 이렇게 생겼다.

```
rmgr: Heap        len (rec/tot): 79/79, tx: 845, lsn: 0/016B7378,
prev 0/016B7340, desc: INSERT off 12 flags 0x00, blkref #0: rel 1663/16384/16389 blk 0
```

읽어 보면 — Heap이라는 resource manager(테이블 데이터를 다루는 모듈)가 발행한 79바이트짜리 레코드이고, 트랜잭션 845번이 일으켰고, LSN은 `0/016B7378`이며, 1663/16384/16389라는 OID 조합의 테이블 0번 블록에 12번 슬롯으로 INSERT 했다는 사실이 들어 있다. **이 한 줄만 있으면 같은 INSERT를 정확히 한 번 더 재현할 수 있다.** 복구도, 복제도, CDC도 결국 같은 줄을 다르게 소비하는 일이다.

여기까지가 WAL의 기본 형식과 흐름이다. 한 번 정리해 보자. **모든 변경은 페이지에 적용되기 전에 WAL 레코드로 먼저 기록되고, COMMIT 시점까지 디스크에 fsync 된다. 페이지는 훨씬 느슨한 주기로 따로 내려 간다. 크래시 복구는 마지막 체크포인트 이후의 WAL을 멱등적으로 재생한다.** 이게 다다. 단순하지 않은가?

그런데 — 이 단순한 메커니즘이 PostgreSQL의 거의 모든 자랑을 떠받친다. 어떻게 그게 가능한지 다음 절에서 살펴보자.

## 7.2 WAL이 떠받치는 다섯 가지

WAL의 진짜 위력은 "복구 도구"라는 출생 신분을 훌쩍 넘어선다. 한 번 만들어진 변경 로그가, 시간이 지나면서 다섯 가지 기능을 동시에 떠받치는 토대로 자리 잡았다. 하나씩 살펴보자.

### 7.2.1 첫째 — 크래시 복구

방금 7.1에서 다룬 이야기다. 그러나 한 번 더 강조해 둘 만하다. **PostgreSQL이 "이상한 종료" 후에 자동으로 일관된 상태로 돌아올 수 있는 유일한 이유는 WAL이다.** 데이터 디렉터리에 무엇이 남아 있든, `pg_wal/` 안의 마지막 체크포인트 이후 레코드들만 살아 있다면 PG는 일어선다. 그래서 백업 운영에서 가장 중요한 한 가지는 — 데이터 디렉터리 백업과 WAL 보관을 함께 묶는 것이다. WAL이 빠진 백업은 사실상 "잘려 나간 시점의 스냅샷"일 뿐, 살아 있는 복구 도구가 아니다.

### 7.2.2 둘째 — 스트리밍 복제

primary가 만든 WAL을 그대로 standby에 흘려 보내고, standby에서 똑같이 재생하면 어떻게 될까? 둘 사이의 데이터가 byte 수준에서 같아진다. 이것이 **streaming replication**이다. PostgreSQL 9.0(2010년)부터 내장된 기본 복제 메커니즘으로, 동작 원리는 의외로 단순하다. standby의 **walreceiver** 프로세스가 primary의 **walsender**에게 접속해 마지막으로 받은 LSN을 알리면, primary는 그 LSN 이후의 WAL을 실시간으로 흘려 준다. standby의 **startup** 프로세스(또는 v17부터의 wal recovery 메커니즘)가 그 WAL을 받아 자기 데이터 파일에 재생한다.

여기서 한 가지 결정이 운영의 색깔을 바꾼다. **synchronous_commit** 파라미터다. `off`로 두면 primary는 standby의 응답을 기다리지 않고 즉시 COMMIT을 반환한다 — 빠르지만, primary가 죽는 순간 마지막 몇 ms의 데이터를 잃을 수 있다. `on`(기본값)은 primary 자신의 디스크 fsync까지만 기다리는 모드다. `remote_apply`로 두면 standby가 WAL을 실제로 재생할 때까지 기다린다 — 가장 안전하지만 latency가 늘어난다. 금융 시스템이라면 `remote_apply` 또는 적어도 `remote_write`(standby가 OS 캐시에 받은 시점) 쪽으로 기우는 편이 낫다. 분석 워크로드라면 `off`도 받아들일 수 있다.

스트리밍 복제로 만들어지는 standby는 **read-only로 쿼리도 받을 수 있다(hot_standby = on)**. 그래서 단순한 read scale-out이나 long-running 분석 쿼리를 standby로 미는 패턴이 자연스럽다. 다만 — standby에서 long-running 쿼리가 돌면 primary에서 vacuum이 dead tuple을 회수 못 하는 도미노가 발생할 수 있다(`hot_standby_feedback = on` 옵션). 5장에서 살펴본 vacuum의 어두운 면이 여기서도 한 번 더 인사를 건넨다.

### 7.2.3 셋째 — 논리적 복제

스트리밍 복제는 "byte 단위로 똑같은 클러스터"를 만든다. 그런데 — 다른 메이저 버전 사이에서 복제하고 싶다면? 일부 테이블만 다른 클러스터로 복제하고 싶다면? 같은 row를 받되 컬럼 일부만 받고 싶다면? 이런 욕구는 streaming만으로는 답이 안 된다.

여기서 나오는 게 **logical replication**이다. 2017년 PostgreSQL 10에 정식 내장됐다. 핵심은 **logical decoding**이라는 메커니즘 — WAL에 들어 있는 페이지 단위의 물리적 변경을 **테이블·row·컬럼 단위의 논리적 변경**으로 다시 읽어 내는 것이다. WAL 자체는 "데이터 페이지 16번의 32번 오프셋에 이러이러한 바이트를 적었다" 같은 물리적 정보지만, logical decoding은 거기에 카탈로그 정보를 결합해 "users 테이블의 id=42 row가 INSERT 됐고, 컬럼 값은 이러이러하다"는 논리적 사실로 재구성한다.

이 결과를 외부로 내보내는 출력 포맷이 **logical decoding output plugin**이다. PG 내장 기본은 `pgoutput`이고, 오래 쓰여 온 외부 플러그인 중 가장 유명한 게 `wal2json`이다. Debezium 같은 CDC 도구는 둘 중 하나를 골라 쓴다.

논리적 복제의 활용 시나리오는 풍부하다. **다른 메이저 버전으로 무중단 업그레이드** — 16에서 17로 옮길 때 logical replication으로 데이터를 실시간 동기화하면서 cutover 한 번으로 끝낼 수 있다. **부분 테이블 복제** — A 클러스터의 일부 테이블만 B 클러스터로 보낸다. **이종 DB 동기화** — Debezium을 통하면 PG → Kafka → 어디든 흘려 보낼 수 있다. 17장 마이그레이션 실전에서 다시 만날 패턴이다.

### 7.2.4 넷째 — PITR(Point-In-Time Recovery)

다음 상황을 가정해 보자. 어제 오후 3시 27분, 누군가가 DELETE FROM orders WHERE customer_id = ... 를 WHERE 절을 잘못 적은 채로 실행했다. 4억 건짜리 orders 테이블에서 5천만 건이 날아갔다. 사고는 4시간 뒤 모니터링에서 발견됐다. 백업은 어제 새벽 3시에 떠 둔 게 있다. 그렇다면 — **사고 직전인 3시 26분 시점의 상태로 클러스터를 되돌릴 수 있을까?**

답은 — 어제 새벽 3시 백업 이후의 WAL 세그먼트가 빠짐없이 보관돼 있다면, 가능하다. 백업본을 복원한 뒤, WAL을 처음부터 재생하되 **3시 26분 시점에 멈추라는 명령**을 주면 된다. PostgreSQL의 `recovery_target_time` 파라미터가 그 역할을 한다.

```
recovery_target_time = '2026-05-17 15:26:00 KST'
```

또는 특정 트랜잭션 ID나 LSN, 또는 named restore point도 타겟이 될 수 있다. 이게 **Point-In-Time Recovery**다. 백업과 WAL 보관만 제대로 돼 있으면, 임의의 시각으로 클러스터를 되돌릴 수 있다.

여기서 잠시 멈춰 생각해 보자. PITR이 가능하다는 건 — **단순한 정전 복구를 넘어, 인적 사고에서도 클러스터를 살릴 수 있다**는 뜻이다. 잘못된 DELETE, 잘못된 UPDATE, 잘못된 DROP TABLE까지. 백업 도구로 사실상 표준이 된 **pgBackRest**, EDB의 **Barman**, 클라우드 친화적 **WAL-G**가 전부 이 PITR을 깔끔히 지원한다. 19장에서 이 도구들을 본격적으로 다룬다.

PITR이 작동하려면 한 가지 약속이 필요하다. **archive_mode = on**과 **archive_command**(또는 더 모던한 `archive_library`)를 설정해, 채워진 WAL 세그먼트를 백업 저장소로 자동 복사해 둬야 한다. 운영에서 가장 흔한 사고가 — "백업은 있는데 WAL이 빠져 있어서 백업 시점 이후로는 못 돌아간다"는 상황이다. 끔찍한 일이다. 백업과 WAL 보관은 한 쌍으로 묶어 놓자.

조금 더 깊이 들어가 보자. PITR을 실제로 돌리면 PG는 새로운 **timeline**을 만든다. timeline은 WAL의 분기점이다. 사고 시각으로 되돌아가 새 클러스터가 살아나면, 그 시점부터의 변경은 옛 timeline과 다른 길을 걷는다. PG는 timeline ID를 WAL 파일명 앞 8자리에 박아 넣어 — `000000020000000000000016` 같은 식으로 — 분기를 구분한다. 이 덕분에 "사고 직전으로 되돌렸다가 또 잘못돼서 다시 되돌리는" 작업도 안전하게 반복할 수 있다. 각 시도가 자기 timeline을 갖고, 옛 timeline의 WAL은 그대로 보존된다. 한 번 시작한 PITR을 망쳐도, 또 다른 시점으로 새 timeline을 파서 다시 시도할 수 있는 셈이다.

### 7.2.5 다섯째 — CDC

마지막 다섯 번째 — **Change Data Capture**. 7.2.3에서 다룬 logical decoding을 외부 시스템이 소비하는 패턴이 곧 CDC다. Debezium이 가장 유명한 도구다. Debezium은 PG의 `pgoutput` 또는 `wal2json` 슬롯에 붙어, 트랜잭션 단위로 commit된 변경을 Kafka 토픽에 흘려 보낸다.

이 패턴이 왜 강력한지 한 가지 예를 보자. 주문 시스템이 PG에 있다고 하자. 주문이 들어올 때마다 — 검색 인덱스를 업데이트해야 하고, 캐시를 무효화해야 하고, 분석 시스템에 이벤트를 보내야 하고, 이메일 발송 큐에 넣어야 한다. 이걸 애플리케이션 코드에서 한 트랜잭션 안에 다 묶으면 어떻게 될까? — Kafka가 죽거나 검색 시스템이 느릴 때, 주문 자체가 실패한다. 비즈니스 트랜잭션이 외부 시스템 가용성에 묶여 버린다. 끔찍한 일이다.

대신 — 주문 트랜잭션에서는 **orders 테이블에만 INSERT 하고**, Debezium이 WAL을 읽어 Kafka에 흘려 보내면 된다. 검색·캐시·분석·이메일은 Kafka 컨슈머로 각자 처리한다. **outbox 패턴**의 가장 정직한 구현이다. 외부 시스템 장애가 비즈니스 트랜잭션을 깨지 못한다. 그리고 한 번 commit된 변경은 절대 잃지 않는다 — WAL이 영속화돼 있고, Debezium의 슬롯이 어디까지 읽었는지를 PG가 기억하기 때문이다.

13장(이벤트·큐·실시간), 14장(FDW·CDC·동기화), 그리고 카카오 클린플랫폼 케이스를 다루는 25장에서 이 패턴의 운영 디테일을 깊이 본다. 그런데 잠깐 — 5번 다 살펴보고 나니, 한 가지 사실이 또렷해진다.

**WAL이라는 단 하나의 메커니즘이 다섯 가지 기능을 동시에 떠받친다.** 그것도 한 가지 위에 다른 게 얹힌 게 아니라, 각자 독립적으로 활용한다. 크래시 복구는 로컬 disk에서 WAL을 읽고, 스트리밍 복제는 standby가 네트워크로 WAL을 받고, 논리적 복제는 logical decoding이 WAL을 다시 읽고, PITR은 백업 저장소에 보관된 WAL을 재생하고, CDC는 Debezium이 WAL을 외부로 흘려 보낸다. 같은 강물에서 다섯 명이 다른 통으로 물을 길어 가는 셈이다.

이게 PostgreSQL의 아키텍처적 우아함이다. 단일 메커니즘이 잘 설계되면, 그 위에서 자라는 기능들이 자연스럽게 정합성을 갖춘다. 사후에 끼워 맞춘 게 아니라, 처음부터 같은 토대 위에서 자랐다는 사실이 운영에서도 드러난다. 예를 들어 — PITR 복원 도중의 standby에서도 logical replication slot을 미리 만들어 둘 수 있고, streaming standby에서 logical decoding을 돌릴 수도 있고(v16 이후), Debezium 컨슈머가 페일오버 후에도 살아남는다(v17의 failover slot, 7.2.3에서 잠시 만났던).

그러면 이 토대를 더 단단하게 만들기 위해 PostgreSQL 17이 무엇을 새로 깎았는지, 다음 절에서 살펴보자.

## 7.3 v17의 WAL writer 메모리 개선

새 버전이 나올 때마다 release note에서 가장 눈에 띄지 않는 항목들이 있다. "내부 메모리 관리 개선", "락 경합 완화" 같은 줄들이다. 화려한 새 SQL 문법도 아니고, 눈에 보이는 새 기능도 아니다. 그런데 — 운영하는 사람에게는 이런 항목이 종종 가장 큰 선물이다. 잠시 멈추고 한 번 들여다볼 만하다.

PostgreSQL 17의 변경 사항 중 WAL과 관련된 항목을 정리해 보면, 두 가지 큰 흐름이 보인다. **첫째, WAL writer와 vacuum의 메모리 사용을 다시 썼다.** 둘째, **logical replication이 "진짜 production-ready"로 한 발 더 나아갔다.** 둘 다 운영 부담을 줄이는 방향이다.

### 7.3.1 WAL writer가 가벼워졌다

v16까지의 WAL writer는 한 가지 답답한 점이 있었다. 트래픽이 폭증해서 WAL이 빠르게 쌓이는 순간, WAL writer가 메모리 안에서 다음 segment를 준비하는 비용이 단조롭게 늘어났다. 평소에는 문제가 없지만, OLTP 워크로드가 burst를 칠 때 — WAL writer 자체가 병목이 되어 latency가 튀는 일이 있었다. PG 17은 이 내부 메모리 관리를 다시 설계해, burst 상황에서도 WAL writer의 동작이 매끄럽게 흐르도록 만들었다.

좀 더 실무적으로 말하면 — 같은 하드웨어, 같은 워크로드인데 PG 16에서 17로 올리는 것만으로 p99 latency가 눈에 띄게 좋아지는 사례가 보고되고 있다. pgbench 회귀 테스트 결과를 봐도 16 → 17 구간에서 OLTP 쪽 처리량이 한 단계 좋아진다. 자세한 벤치마크는 3장에서 다뤘으니 여기서는 — "WAL 토대 자체가 한 번 더 견고해졌다"는 사실만 짚고 넘어 가자.

운영자의 입장에서 한 가지 더 짚자면 — burst 상황의 latency 개선은 단순히 "더 빠르다"는 의미가 아니다. **SLO를 지킬 수 있는 헤드룸이 늘어난다는 의미다.** 결제 시스템처럼 p99 latency를 100ms 안에 묶어야 하는 서비스는, peak 시간에 WAL writer가 잠깐 멎으면 그 한 번이 SLA 위반으로 직결된다. 17이 깎아 준 latency 꼬리는 그런 "한 번"의 빈도를 줄여 준다. 같은 클러스터, 같은 하드웨어로 한 단계 더 안정적인 SLO를 약속할 수 있다는 뜻이다.

### 7.3.2 Vacuum 메모리 재작성과의 연관성

v17은 vacuum이 dead tuple ID를 관리하는 자료구조를 새로 썼다(TID store). 이전에는 maintenance_work_mem 한도 안에서 단순한 배열로 관리했는데, 1GB 한도에 가까워지면 vacuum이 여러 패스(pass)로 나뉘어 돌면서 인덱스를 여러 번 스캔해야 했다. 끔찍한 일이다. 큰 테이블의 vacuum이 며칠 걸리는 이유 중 하나가 이 다중 패스였다.

17은 TID 저장에 radix tree 기반의 압축 자료구조를 도입했다. 같은 메모리 안에 훨씬 더 많은 dead tuple ID를 담을 수 있게 됐다. 그래서 — 큰 테이블의 vacuum이 한 번에 끝나는 비율이 크게 올라간다. WAL과 직접 연관된 건 아니지만, **vacuum이 끝나야 그 결과가 WAL에 기록되고**, WAL이 standby로 복제되어야 standby의 dead tuple도 회수된다는 점에서 — WAL 흐름 전체가 한 박자 빨라진다. 같은 클러스터인데 5장에서 만났던 통증 일부가 누그러진다.

### 7.3.3 Failover slot — logical replication이 HA를 만나다

이게 v17의 가장 중요한 단일 변경일지 모른다. 7.2.3과 7.2.5에서 잠깐 만났던 — **logical replication slot이 standby로 동기화된다**는 그 사실 말이다.

이전까지의 사정을 한 번 정리해 보자. logical replication slot은 primary에만 존재했다. Debezium이 primary의 슬롯에 붙어 있다가, primary가 죽으면 어떻게 될까? standby가 승격해 새 primary가 된다. 그런데 새 primary에는 슬롯이 없다. Debezium이 다시 접속해도 슬롯이 없으니 "어디까지 읽었는지" 정보가 사라진 채로, 처음부터 다시 읽거나(데이터 중복), 또는 그 사이의 변경을 잃어버린다(데이터 손실). 사실상 — **페일오버는 CDC 파이프라인의 재구축을 의미했다.** 운영팀이 페일오버를 두려워하는 진짜 이유 중 하나였다.

17의 failover slot은 이 사정을 뒤집는다. primary의 슬롯 상태가 standby로 자동 동기화되고, standby가 승격하면 새 primary에서 그 슬롯이 살아 있다. Debezium은 새 primary로 접속해 끊긴 LSN부터 계속 읽으면 된다. 데이터 중복도 손실도 없다.

이 한 가지 변경이 무엇을 가능하게 하는지 생각해 보자. **이제 페일오버가 일상이 될 수 있다.** 분기별 페일오버 훈련을 돌려도 CDC 파이프라인이 깨지지 않는다. 매니지드 PG에서 마이너 업그레이드를 위해 강제 페일오버가 돌아도, 외부 CDC 컨슈머가 영향을 안 받는다. logical replication을 운영의 정식 도구로 쓸 수 있는 마지막 장애물이 치워졌다고 봐도 좋다.

failover slot이 없던 시절의 풍경을 한 번 떠올려 보자. 운영팀은 "페일오버는 가능하면 안 하고 싶다"는 보이지 않는 룰을 갖고 있었다. 왜냐하면 — 페일오버를 한 번 하면 그 뒤로 CDC 파이프라인 재구축, Debezium 슬롯 재생성, 컨슈머 오프셋 재조정, 데이터 누락 검증, 이중 전송 정리 같은 작업이 며칠씩 이어졌기 때문이다. 그래서 — primary가 약간 이상해 보여도 "조금만 더 버텨 보자"는 선택을 하게 됐다. 그 미루기가 한 번씩 큰 사고로 이어졌다. 17의 failover slot은 그 미루는 습관 자체를 깨뜨린다. 페일오버가 두렵지 않아지면, 운영팀은 작은 이상을 빠르게 정리할 수 있다. **운영 문화 자체가 한 단계 가벼워진다.**

3장에서 "PostgreSQL 17부터 logical replication이 진짜 production-ready가 됐다"고 말했던 근거가 바로 이 failover slot이다. 14장(FDW·CDC), 17장(마이그레이션), 20장(HA) 모두에서 다시 등장할 친구다.

### 7.3.4 운영에서 무엇이 달라지나

세 가지 변화가 합쳐졌을 때 운영자가 체감하는 결과는 단순하다. **PG 16까지는 "조심해야 할 도구"였던 logical replication이, 17부터는 "쓸 만한 도구"가 된다.** burst 상황에서의 WAL latency가 좋아지고, vacuum이 한 번에 끝날 확률이 높아지고, 페일오버 후에도 CDC가 살아남는다. 이 세 가지가 별개의 변화처럼 보이지만, 운영의 시점에서 보면 같은 방향이다 — **WAL을 활용하는 모든 기능이 한 단계 더 견고해졌다.**

물론 17로 올린다고 모든 통증이 사라지지는 않는다. autovacuum 튜닝의 책임(18장)은 여전하고, HA 도구 선택(20장)도 여전히 고민이다. 다만 — 토대가 단단해진 만큼, 그 위에 쌓는 운영 결정의 여유도 늘어났다. PG 16을 쓰고 있다면, 17로 올리는 것이 단순한 버전 업이 아니라 **운영 부담의 한 단계 경감**임을 기억해 두자.

이제 토대의 절반을 봤다. 남은 절반은 — WAL 위에 얹힌 또 하나의 보석, **SSI(Serializable Snapshot Isolation)**다. 이론적으로 정교하지만, 운영에서는 거의 "잠금 없이 작동하는 마법"처럼 보이는 그 기능을 다음 절부터 들여다 보자.

## 7.4 SSI의 이론적 토대 — Ports & Grittner, VLDB 2012

격리 수준(isolation level)이라는 말을 처음 만났을 때를 떠올려 보자. READ COMMITTED, REPEATABLE READ, SERIALIZABLE — 교과서는 이 네 단계를 사다리처럼 그려 놓고, "위로 올라갈수록 안전하지만 느려진다"고 가르친다. 그런데 SERIALIZABLE까지 실제로 써 본 사람이 얼마나 될까? 대부분의 시스템에서 SERIALIZABLE은 "이론상 존재하지만, 너무 느려서 못 쓰는 모드"였다.

왜 못 썼는가? 전통적인 SERIALIZABLE 구현은 **2PL(Two-Phase Locking)** 위에 서 있었기 때문이다. 모든 read에 shared lock, 모든 write에 exclusive lock을 걸고, 트랜잭션이 끝날 때까지 안 풀어 준다. 그래야 직렬화 가능성이 보장된다. 그런데 — 동시 트랜잭션이 많아지면 잠금이 끝없이 충돌한다. deadlock이 잦아지고, throughput이 추락한다. 그래서 거의 모든 시스템은 SERIALIZABLE 대신 SNAPSHOT ISOLATION(또는 그 변형)을 사실상의 최고 격리로 사용해 왔다. Oracle도, SQL Server도, MySQL InnoDB도 마찬가지다.

그런데 SNAPSHOT ISOLATION에는 알려진 약점이 있다. **write skew**라는 이상 현상이다. 한 번 살펴보자.

### 7.4.1 Write skew — SNAPSHOT ISOLATION이 놓치는 것

병원의 당직 스케줄 시스템을 가정해 보자. 규칙은 단순하다 — **언제든 최소 한 명의 의사가 당직이어야 한다.** 현재 의사 A와 의사 B가 모두 당직 상태(on_call = true)다.

```sql
-- 트랜잭션 T1: 의사 A가 "다른 누군가가 당직이면 나는 빠지겠다"
BEGIN;
SELECT count(*) FROM doctors WHERE on_call = true;  -- 결과: 2
-- "한 명 이상 있으니 나는 빠져도 되겠다"
UPDATE doctors SET on_call = false WHERE id = 'A';
COMMIT;

-- 트랜잭션 T2 (T1과 동시 실행): 의사 B가 같은 논리
BEGIN;
SELECT count(*) FROM doctors WHERE on_call = true;  -- 결과: 2
UPDATE doctors SET on_call = false WHERE id = 'B';
COMMIT;
```

T1과 T2가 동시에 실행되면 무슨 일이 벌어지는가? **둘 다 "다른 누가 있으니 나는 빠져도 된다"는 판단으로 COMMIT 된다.** 결과 — 당직 의사는 0명. 환자가 위급 상황에 들어와도 호출할 사람이 없다. 끔찍한 일이다.

이게 write skew다. 각 트랜잭션은 자기 스냅샷에서는 모든 조건이 옳다. T1은 T2가 쓴 결과를 못 보고, T2도 T1이 쓴 결과를 못 본다. SNAPSHOT ISOLATION은 — **자기 트랜잭션 시작 시점의 일관된 스냅샷을 보장**하지만, 그 사이에 다른 트랜잭션이 자기 결정의 전제를 무너뜨릴 수 있다는 사실은 막지 못한다. 비슷한 예가 은행 시스템의 부부 공동 계좌 인출, 회의실 동시 예약, 재고 차감 등 셀 수 없이 많다.

해결책은 두 가지였다. 첫째 — **SELECT FOR UPDATE** 같은 명시적 row 잠금으로 우회한다. 둘째 — **SERIALIZABLE을 켜고 2PL의 비용을 치른다**. 둘 다 만족스럽지 않다. 첫째는 개발자가 모든 write skew 가능성을 미리 찾아내야 한다(놓치면 사고). 둘째는 시스템이 느려진다(throughput 추락).

이런 와중에 — 2008년, Cahill·Röhm·Fekete가 한 가지 정교한 아이디어를 SIGMOD에 발표했다. **"Serializable Isolation for Snapshot Databases."** SNAPSHOT ISOLATION의 우아함을 그대로 유지하면서, write skew 같은 직렬화 위반만 골라서 탐지·중단하는 방법이 있다는 것이다.

### 7.4.2 SSI의 두 인물 — Ports와 Grittner

이 아이디어를 실제 시스템에 구현한 것이 PostgreSQL이다. Dan Ports(MIT)와 Kevin Grittner(EnterpriseDB)가 PG 9.1(2011년)에 **Serializable Snapshot Isolation**, 줄여서 SSI를 내장했다. 그리고 그 구현 경험을 정리한 논문이 — 2012년 VLDB에 발표된 "Serializable Snapshot Isolation in PostgreSQL"이다. 본 책에서 여러 번 인용되는 그 논문이다.

논문의 핵심 주장은 단순하다. **"우리는 잠금 없이도 직렬화 가능성을 보장할 수 있다. 그것도 운영에서 쓸 만한 성능으로."** 실제 측정 결과 — SSI는 SNAPSHOT ISOLATION 대비 약 5~10%의 오버헤드만 추가했다(워크로드에 따라 다름). 같은 워크로드에서 전통적 2PL SERIALIZABLE보다 수배 빠르다. 그러면서도 직렬화 위반은 100% 잡아 낸다.

이게 왜 중요한가? — **금융, 결제, 의료, 항공 같은 도메인에서 "정말로 직렬화 가능해야 하는" 워크로드가 PG에서 비로소 운영 비용 안에 들어왔다.** 그동안 이런 도메인은 어쩔 수 없이 애플리케이션 레벨에서 잠금을 직접 관리하거나, 큰 단일 트랜잭션으로 묶어 throughput을 포기하거나, 혹은 사고 가능성을 안고 살아왔다. SSI는 그 부담을 DB 안으로 끌어들였다.

### 7.4.3 한 가지 가정 — read-write conflict 그래프

SSI가 어떻게 작동하는지의 직관을 살짝 보자. 자세한 메커니즘은 다음 절(7.5)에서 다룬다.

핵심 아이디어는 — **트랜잭션 사이의 read-write conflict를 그래프로 추적하고, 그 그래프에 "위험한 패턴"이 만들어지는 순간 한쪽 트랜잭션을 abort 시킨다**는 것이다. 위험한 패턴은 정확히 정의돼 있다 — Adya가 2000년 박사논문에서 정리한 "dangerous structure" 또는 "rw-antidependency cycle"이다. 그래프에 이 사이클이 만들어지면, 직렬화 가능성이 깨질 가능성이 생긴다. SSI는 이 순간을 잡아내 한쪽을 abort 시킨다.

abort된 트랜잭션은 **serialization_failure** 에러를 받는다(SQLSTATE 40001). 애플리케이션은 이 에러를 보고 트랜잭션을 재시도하면 된다. 재시도 로직만 잘 짜 두면, 개발자는 잠금이나 SELECT FOR UPDATE 같은 저수준 도구를 신경 쓸 필요가 없다. **그냥 트랜잭션 시작 시 ISOLATION LEVEL SERIALIZABLE을 설정하고, 비즈니스 로직을 평범하게 쓰면 된다.** 직렬화 위반이 생기면 PG가 알아서 한쪽을 abort 시키고, 애플리케이션은 재시도한다.

이게 "잠금 없이 직렬화 가능성을 보장한다"는 한 줄이 가지는 무게다. write skew 같은 미묘한 버그를 개발자가 미리 다 찾아내지 않아도 된다. SQL은 단순하게 쓰고, DB가 정확성을 보장한다. **정확성을 DB로 위임할 수 있다**는 사실이, 시스템 설계의 무게를 한 단계 가볍게 만든다.

다음 절에서는 SSI가 실제로 어떻게 충돌을 탐지하고 abort 결정을 내리는지, 한 단계 더 들어가 보자.

## 7.5 잠금 없이 직렬화 보장 — 충돌 탐지와 abort

SSI의 마법 같은 약속을 한 번 더 정리해 두자. **잠금을 걸지 않는다. 트랜잭션은 자기 스냅샷 위에서 자유롭게 read·write 한다. 그런데도 SERIALIZABLE이 보장된다.** 어떻게 이게 가능한가? 한 단계씩 들여다 보자.

### 7.5.1 SIREAD lock — "잠금이 아닌 잠금"

먼저 용어 하나를 정리해야 한다. SSI 내부에는 **SIREAD lock**(또는 predicate lock)이라는 게 있다. 이름에 "lock"이 붙어 있지만, **이것은 다른 트랜잭션을 막지 않는다.** 그냥 — "이 트랜잭션이 이 데이터를 read 했다"는 사실을 추적하는 표식일 뿐이다. 그래서 SIREAD lock이 잡혀 있어도 다른 트랜잭션은 같은 데이터를 자유롭게 read·write 할 수 있다.

그러면 왜 lock이라고 부르는가? — 데이터베이스 이론에서 "predicate lock"이라는 개념이 오래 있어 왔고, 그 자리에 들어맞기 때문이다. 실제 동작은 잠금이 아니라 **read 기록**이다. 헷갈리지 않도록 — "SIREAD lock = 어떤 트랜잭션이 무엇을 read 했는지를 추적하는 메타데이터" 정도로 기억해 두자.

SSI는 트랜잭션이 read 할 때마다 SIREAD lock을 기록한다. 단순한 row 단위뿐 아니라 **predicate** 단위로도 — 예를 들어 "doctors 테이블에서 on_call = true인 row를 read 했다"는 조건 자체를 기록한다. 인덱스 페이지 레벨, 또는 술어 레벨에서 잡힌다. 정확한 입자는 PG 내부 구현에 따라 다르지만, 핵심은 — **read의 흔적이 남는다**는 것이다.

### 7.5.2 rw-conflict — "당신이 읽은 것을 내가 바꿨다"

이제 conflict의 정의를 보자. 트랜잭션 T1이 어떤 데이터를 read 하고(SIREAD 기록), 그 뒤에 트랜잭션 T2가 같은 데이터를 write 했다고 하자. 이를 **rw-conflict** (read-write conflict)라고 부른다. PG는 이 conflict를 트랜잭션 사이의 edge로 추적한다.

T1 →rw→ T2

이 edge 하나만으로는 아무 문제가 없다. SNAPSHOT ISOLATION의 정상적인 동작이다. T1은 자기 스냅샷을 보고 있고, T2가 새 값을 써도 T1의 시야에는 안 보인다. 양쪽 다 잘 동작한다.

문제는 — **rw-conflict가 사이클을 만들 때** 생긴다.

### 7.5.3 dangerous structure — abort 트리거

SSI 이론의 핵심 정리(theorem): **SNAPSHOT ISOLATION에서 직렬화 위반이 일어나는 모든 시나리오는, rw-conflict 그래프에 특정한 사이클 패턴을 포함한다.** Adya는 이 패턴을 "dangerous structure"라고 명명했다.

가장 단순한 위험 패턴은 — **세 개의 트랜잭션 T1, T2, T3가 다음 edge를 가질 때**:

T1 →rw→ T2 →rw→ T3

그리고 T2가 그 중간에서 "pivot" 역할을 할 때다. 더 단순화하면 — 두 트랜잭션이 서로 rw-conflict 양방향을 가지면(T1 →rw→ T2 그리고 T2 →rw→ T1) 위험하다.

앞 절 7.4.1의 write skew 예를 다시 보자. 의사 A의 트랜잭션(T1)이 "on_call=true인 row 개수"를 read 했다(SIREAD on predicate). 그 뒤 T1은 의사 A의 on_call을 false로 update. 동시에 T2는 "on_call=true인 row 개수"를 read하고, 의사 B의 on_call을 false로 update. 그러면 — T1의 read와 T2의 write 사이에 rw-conflict, 그리고 T2의 read와 T1의 write 사이에 rw-conflict가 동시에 생긴다. **양방향 rw-conflict — 정확히 dangerous structure다.** SSI는 이 순간을 잡아내 둘 중 한쪽을 abort 시킨다.

### 7.5.4 abort 결정과 재시도

abort 결정이 떨어지면, 해당 트랜잭션의 클라이언트는 다음 에러를 받는다.

```
ERROR:  could not serialize access due to read/write dependencies among transactions
DETAIL:  Reason code: Canceled on identification as a pivot, during commit attempt.
HINT:  The transaction might succeed if retried.
SQLSTATE: 40001
```

핵심은 **HINT의 마지막 줄** — "재시도하면 성공할 수 있다." 그렇다. SSI에서 abort는 사고가 아니라 **정상적인 동작**이다. 직렬화 위반이 일어나려는 순간 PG가 미리 막은 것이고, 애플리케이션은 그저 트랜잭션을 처음부터 다시 돌리면 된다.

그래서 — **SSI를 쓰는 애플리케이션의 의무는 단 하나, 재시도 로직을 갖추는 것이다.** 의사 코드로는 이렇다.

```python
def transfer_money(from_id, to_id, amount, max_retries=5):
    for attempt in range(max_retries):
        try:
            with db.transaction(isolation_level='SERIALIZABLE'):
                # 비즈니스 로직 — 잠금이나 SELECT FOR UPDATE 없이 평범하게
                src = db.query("SELECT balance FROM accounts WHERE id = %s", from_id)
                dst = db.query("SELECT balance FROM accounts WHERE id = %s", to_id)
                if src.balance < amount:
                    raise InsufficientFunds()
                db.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", amount, from_id)
                db.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", amount, to_id)
                return
        except SerializationFailure:
            # 백오프 후 재시도
            time.sleep(0.01 * (2 ** attempt))
    raise TooManyRetries()
```

이게 전부다. **저수준 잠금 코드가 없다. SELECT FOR UPDATE도 없다. write skew를 사전에 분석하는 일도 없다.** 그저 비즈니스 로직을 평범하게 쓰고, SerializationFailure가 나면 재시도한다. DB가 정확성을 책임진다.

물론 — 재시도가 너무 자주 일어나면 throughput에 영향을 준다. 그래서 SSI를 잘 쓰려면 한 가지 운영 감각이 필요하다. **abort 비율을 모니터링하자.** `pg_stat_database`의 `xact_rollback` 카운터, 또는 `log_min_messages`를 조절해 serialization failure 로그를 수집해 분석한다. 비율이 비정상적으로 높다면 — 핫스팟이 있다는 신호다. predicate를 더 좁히거나, 트랜잭션을 더 짧게 끊거나, 일부 쿼리를 SELECT FOR UPDATE로 명시적 잠금으로 바꾸는 식의 튜닝이 필요할 수 있다.

### 7.5.5 SSI의 한계 — 알아 두면 좋은 것들

SSI가 만능은 아니다. 알아 둬야 할 한계가 몇 가지 있다.

**첫째, false positive가 있다.** SSI는 안전을 위해 — 실제로 직렬화 위반이 안 일어날 수도 있는 dangerous structure에 대해서도 abort 시킨다. 정확하게 잡아내려면 비용이 너무 크기 때문이다. 그래서 일부 트랜잭션은 "사실 abort 안 해도 됐을" 케이스에서도 abort 될 수 있다. 운영에서는 — 이런 false positive를 줄이려고 SSI가 결국 더 큰 입자(인덱스 페이지 단위 등)로 추적하므로, **트랜잭션 안에서 read의 범위를 좁힐수록 false positive가 줄어든다.** 모든 row를 SELECT * 하기보다, 필요한 컬럼만 정확한 WHERE 조건으로 가져오는 게 낫다.

**둘째, read-only 트랜잭션의 최적화가 있다.** PG는 read-only 트랜잭션을 자동 감지해, SIREAD 추적을 일부 생략한다. 그래서 read-only 트랜잭션은 SSI에서도 거의 SNAPSHOT ISOLATION만큼 빠르다. `BEGIN TRANSACTION READ ONLY`로 명시하면 더 명확하다.

**셋째, hot_standby에서는 SSI가 안 된다.** standby의 read-only 쿼리는 REPEATABLE READ 수준까지만 지원한다. SSI는 primary에서만 작동한다. 만약 standby로 분산한 read 트랜잭션이 SERIALIZABLE 수준의 보장을 필요로 한다면 — primary로 보내야 한다.

**넷째, 모든 워크로드에서 SSI가 답은 아니다.** 갱신 충돌이 거의 없는 OLTP라면 — abort 비용이 그냥 오버헤드일 뿐이다. 분석 쿼리는 read-only 트랜잭션으로 거의 무료. 그러나 — 같은 row를 여러 트랜잭션이 동시에 읽고 쓰는 패턴(인기 상품의 재고, 인기 좌석 예약 등)에서는 abort 비율이 치솟을 수 있다. 이런 핫스팟은 SSI든 2PL이든 결국 throughput에 영향을 준다. 다만 SSI는 **잠금 대기 없이** 사고를 막는다는 점이 다르다.

여기까지가 SSI의 작동 방식이다. 한 번 정리해 보자. **SIREAD lock으로 read를 추적하고, rw-conflict를 그래프로 잇고, dangerous structure가 만들어지는 순간 한쪽을 abort 시킨다. 애플리케이션은 abort된 트랜잭션을 재시도하면 된다.** 이게 "잠금 없이 직렬화 보장"이라는 한 줄 약속의 모든 것이다.

그런데 — 이 약속이 왜 금융·결제 시스템에게 특별한 의미를 가지는지, 다음 절에서 마지막으로 짚고 가자.

## 7.6 금융과 결제가 PG를 고르는 이론적 근거

이번 장의 마지막 질문이다. 다음 상황을 한 번 가정해 보자. 새로운 결제 시스템을 설계한다고 하자. 일초당 수천 건의 결제가 도는, 정확성이 절대 흔들리면 안 되는 시스템이다. 데이터베이스를 고르는 자리에 앉았다고 해보자. 후보는 — Oracle, MySQL, PostgreSQL, 그리고 어쩌면 NewSQL 계열의 무언가.

기능 매트릭스만 놓고 보면 다 비슷해 보인다. 다 SERIALIZABLE을 지원한다고 말한다. 다 ACID를 약속한다. 다 트랜잭션을 처리한다. 그렇다면 — **차이는 어디에 있을까?**

### 7.6.1 "SERIALIZABLE을 진짜로 켤 수 있느냐"

차이는 한 곳에 있다. **"운영에서 SERIALIZABLE을 실제로 켜고 살 수 있느냐"**라는 점이다.

Oracle은 SERIALIZABLE을 지원하지만, 내부적으로는 SNAPSHOT ISOLATION + serialization error 모드다. write skew를 일부 잡지만 완전하지는 않다. 게다가 운영에서 SERIALIZABLE을 켜면 ORA-08177 에러(serializable transaction failure)가 자주 떠서, 실무에서는 거의 READ COMMITTED + 명시적 잠금 패턴을 쓴다.

MySQL InnoDB는 SERIALIZABLE에서 next-key lock 등 2PL 기반 잠금을 강하게 건다. throughput이 크게 떨어진다. 운영에서 켜는 사례를 찾기 어렵다.

SQL Server는 SERIALIZABLE에서 역시 2PL 기반 잠금을 건다. 또는 SNAPSHOT ISOLATION 레벨을 따로 두는데, write skew 보호는 없다.

**PostgreSQL은 다르다.** SSI 덕분에 SERIALIZABLE을 켜도 잠금이 추가되지 않는다. 충돌이 없는 트랜잭션은 SNAPSHOT ISOLATION과 거의 같은 throughput으로 돈다. 충돌이 있는 트랜잭션만 abort + 재시도로 처리된다. **운영에서 켜고 살 수 있는 유일한 SERIALIZABLE이라고 봐도 좋다.**

이 사실의 무게를 한 번 음미해 보자. 결제 시스템 개발자가 더 이상 "이 쿼리에 SELECT FOR UPDATE를 빠뜨리면 어떻게 되지?"를 매번 고민하지 않아도 된다. 회의실 예약 시스템 개발자가 더 이상 "동시 예약 시 어떤 잠금을 어디까지 거나"를 매번 설계하지 않아도 된다. **정확성을 DB로 위임할 수 있다.** 잠금 없이.

### 7.6.2 WAL이 떠받치는 신뢰성

거기에 — 이번 장의 절반을 차지한 WAL이 결합되면, 그림은 더 단단해진다.

**모든 commit된 트랜잭션은 절대 잃지 않는다(durability).** WAL이 디스크에 fsync 됐기 때문이다. 정전이 와도, 서버가 죽어도, 마지막 commit까지의 결제는 살아 있다.

**모든 정상 종료된 트랜잭션은 일관된 상태로 복구된다(atomicity).** WAL의 COMMIT/ABORT 레코드와 페이지의 LSN이 일치해서 — 중간에 멈춘 트랜잭션의 흔적은 자동으로 지워진다.

**임의의 시각으로 되돌릴 수 있다(PITR).** 사고 직전, 잘못된 DELETE 직전, 잘못된 패치 직전 — 어느 순간이든 백업 + WAL 보관만 있으면 돌아간다.

**복제 standby로 같은 보장을 흘려 보낼 수 있다(streaming replication).** 동기 복제(`remote_apply`)로 두면 primary와 standby가 byte 수준에서 같은 상태를 유지한다. 한 노드가 죽어도 결제는 계속 흘러야 하니까.

**외부 시스템에 변경을 정확하게 흘려 보낼 수 있다(CDC).** Debezium + logical replication으로, 결제 이벤트를 한 번도 잃지 않고 정산 시스템·분석 시스템·알림 시스템으로 흘려 보낸다. WAL이 이미 영속화돼 있고, 슬롯이 어디까지 읽었는지 추적한다.

이 다섯 가지가 다 — **하나의 WAL이라는 토대 위에서 정합성 있게 작동한다.** 사후에 끼워 맞춘 게 아니다. 처음부터 한 자리에서 자란 형제들이다.

### 7.6.3 한 사례 — 결제 시스템의 SSI 활용

좀 더 구체적으로 그려 보자. 결제 시스템에서 가장 흔한 정확성 요구 사항은 — **"한 사용자가 같은 카드로 동시에 두 결제를 보낼 때, 잔액 한도가 정확히 한 번만 체크되어야 한다"**는 것이다.

전통적인 방법으로는 사용자 레코드에 SELECT FOR UPDATE를 걸어 잠그고, 잔액을 확인하고, 결제를 진행한다. 그런데 — 잠금 시간 동안 다른 결제는 대기한다. throughput이 떨어진다. deadlock도 신경 써야 한다.

SSI로 푸는 방법은 단순하다.

```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;

-- 잔액 확인 (잠금 없음)
SELECT credit_limit, current_balance
FROM cards
WHERE card_id = '...';

-- 한도 체크
-- (애플리케이션 로직)

-- 결제 기록 + 잔액 갱신
INSERT INTO payments (...) VALUES (...);
UPDATE cards SET current_balance = current_balance + amount
WHERE card_id = '...';

COMMIT;
```

같은 카드로 두 결제가 동시에 와도 — 한쪽은 commit되고, 다른 쪽은 serialization failure로 abort 된다. 애플리케이션은 재시도. 그 사이에 첫 결제가 commit돼 잔액이 갱신됐으므로, 재시도된 두 번째 결제는 한도 초과로 정확히 거절된다. **두 결제가 모두 성공해 한도가 초과되는 사고는 절대 일어나지 않는다.** 잠금 한 번 없이.

이게 PostgreSQL이 금융·결제 시스템에서 점점 더 많이 선택되는 이론적 근거다. **정확성을 DB로 위임할 수 있다**는 약속이, 시스템 설계의 무게를 한 단계 가볍게 만든다. 그리고 그 약속을 — SSI는 운영 가능한 비용으로 지킨다. WAL은 그 결과를 영원히 잃지 않게 지킨다.

### 7.6.4 다른 후보들과의 비교

물론 — "SERIALIZABLE이 진짜로 작동하는 DB"는 PG 말고도 있다. 최근의 NewSQL 진영(CockroachDB, YugabyteDB 등)도 분산 환경에서 SERIALIZABLE을 제공한다. Google Spanner도 마찬가지다. 이들은 분산 트랜잭션의 어려운 문제를 다른 방식으로(TrueTime, distributed deadlock detection 등) 풀어낸다.

PG의 강점은 — **단일 노드에서 운영 가능한 SERIALIZABLE**이다. 결제 시스템의 코어 도메인이 한 대의 큰 PG 클러스터로 충분하다면(또는 region 단위로 분리할 수 있다면), 분산 트랜잭션의 복잡성을 끌어들이지 않고도 같은 보장을 받는다. 운영 비용, 디버깅 비용, 도구 생태계 — 모든 측면에서 더 가볍다.

물론 PG도 약점이 있다. 단일 primary 모델이라 write 처리량의 상한이 있다(스케일은 read replica로만). region 간 동기 복제는 latency 부담이 크다. 진짜 multi-region active-active이 필요하면 — 다른 도구를 봐야 한다. 다만 — **현재 80% 이상의 결제 워크로드는 단일 primary로 충분하다.** 그 80%에서, PG는 정확성·복구·복제·CDC를 한 자리에서 단일 메커니즘 위에 묶어 준다.

이게 — 큰 결제·금융 시스템에서 PG가 점점 더 선택되고 있는 진짜 이유다. 마케팅 자료에는 "PG는 빠르고 안정적이다"라고 적혀 있지만, 그 뒤의 진짜 문장은 — **"WAL과 SSI가 결합된 토대 위에서, 정확성·복구·복제·CDC가 단일 정합성을 갖는다"**는 것이다.

한국 시장의 움직임도 같은 방향을 가리킨다. 1장에서 짚었던 공공·금융 분야의 PG 채택 가속, 25장에서 깊이 다룰 카카오 클린플랫폼의 CDC 파이프라인, 그리고 17장에서 만날 4억 row 마이그레이션 후기들 — 표면적으로는 "Oracle 라이선스 비용", "오픈소스 생태계", "확장성" 같은 명분이 자주 인용되지만, 한 꺼풀 벗기면 결국 같은 토대로 수렴한다. **결제 정확성을 DB에 위임할 수 있다.** 그리고 **그 결과를 한 번도 잃지 않는다.** 이 두 약속이 결합된 DB가 — 2026년의 메인 후보로 PG를 끌어올린 진짜 동력이다.

이번 장에서 본 WAL과 SSI는 책 나머지의 거의 모든 챕터로 가지를 뻗는다. 9장의 JSONB도 같은 WAL 위에서 commit되고, 12장의 pgvector 인덱스도 같은 WAL로 영속화된다. 13장의 LISTEN/NOTIFY는 트랜잭션 commit 시점에 발사된다 — WAL의 commit 레코드와 같은 순간이다. 17장의 무중단 마이그레이션은 logical replication이 WAL을 다시 읽는 패턴 위에서 작동하고, 19장의 PITR은 WAL 보관 정책의 직접적 결과다. 20장의 페일오버, 25장의 카카오 케이스 — 모두 이번 장의 토대 위에서 자라난 것들이다.

## 마무리

이번 장에서 다룬 내용을 한 번 모아 보자.

**WAL**은 Write-Ahead Log의 줄임말로, 모든 변경을 페이지에 적용하기 전에 순차 로그에 먼저 기록한다는 단순한 약속이다. 이 단순한 약속이 — **크래시 복구**, **스트리밍 복제**, **논리적 복제**, **PITR**, **CDC** 다섯 가지 기능을 동시에 떠받친다. 각자 독립적으로 작동하지만, 같은 토대 위에서 자란 형제들이라 정합성을 갖춘다.

**PostgreSQL 17**은 이 토대를 한 단계 더 단단하게 만들었다. WAL writer의 메모리 관리를 다시 쓰고, vacuum의 TID store를 도입하고, **failover slot**으로 logical replication이 HA 안에서 살아남게 만들었다. 17부터 logical replication을 운영의 정식 도구로 쓸 수 있다.

**SSI**(Serializable Snapshot Isolation)는 2008년 Cahill 등의 SIGMOD 논문에서 출발해, Ports와 Grittner가 PG 9.1에 내장한 정교한 알고리즘이다. SIREAD lock으로 read를 추적하고, rw-conflict를 그래프로 잇고, dangerous structure가 만들어지는 순간 한쪽을 abort 시킨다. **잠금 없이 SERIALIZABLE을 보장한다.** SNAPSHOT ISOLATION 대비 5~10%의 오버헤드만 추가한다.

이 두 가지가 결합되면 — **금융·결제처럼 정확성이 절대 흔들리면 안 되는 도메인이, 운영 가능한 비용 안에 들어온다.** 한도 체크, 좌석 예약, 잔액 인출 같은 시나리오를 — 잠금 코드 없이, write skew 분석 없이, 그저 비즈니스 로직을 평범하게 쓰고 SerializationFailure를 재시도하는 것만으로 정확하게 처리할 수 있다. 정확성을 DB로 위임할 수 있다는 사실이, 시스템 설계의 무게를 한 단계 가볍게 만든다.

기억해 두자. **PostgreSQL의 거의 모든 자랑은 WAL과 SSI 두 가지로 거슬러 올라간다.** 복제도, CDC도, PITR도, 진짜 직렬화도 다 여기서 나온다. 책의 나머지 절반에서 만날 — 9장의 JSONB, 13장의 Kafka 대체, 14장의 Debezium 파이프라인, 17장의 무중단 마이그레이션, 19장의 PITR 백업, 20장의 페일오버 자동화, 25장의 카카오 CDC 케이스 — 모두 이번 장의 토대 위에서 자란다.

다음 8장부터는 Part 3로 들어간다. PG의 표현력을 9가지 시나리오로 펼쳐 본다. 첫 시나리오는 — 모든 RDB의 기본 무기, **SQL 표준과 트랜잭션의 깊이**다. SQL이 단순한 데이터 조회 언어가 아니라, 애플리케이션 로직의 절반을 짊어질 수 있는 표현력 도구라는 사실을 — 윈도우 함수, MERGE, JSON_TABLE, temporal constraint 같은 도구로 보여 줄 차례다. 함께 살펴보자.
