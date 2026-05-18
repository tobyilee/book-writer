# 4장. 프로세스 모델과 메모리 — fork가 만드는 모든 것

커넥션 풀이 왜 필요한지 누군가 묻는다고 해보자. MySQL을 오래 쓴 사람이라면 "비용 절감"이라고 답할 것이다. 매번 인증하고 세션을 여는 일이 공짜는 아니니까, 미리 열어둔 커넥션을 재사용하면 응답이 빨라진다 — 그 정도의 논리다. 풀러가 없다고 시스템이 무너지지는 않는다. 그저 조금 느려질 뿐이다.

그런데 PostgreSQL에서 같은 질문을 던지면 답이 사뭇 달라진다. "비용 절감"이 아니라 "생존"이다. 풀러를 빼면 시스템이 천천히 느려지는 게 아니라, 어느 순간 메모리가 폭주하고 OS 스케줄러가 비명을 지르며 클러스터가 멈춰선다. 같은 단어인데 무게가 전혀 다르다.

왜 이런 차이가 생길까? 답은 한 줄로 요약된다. **PostgreSQL은 커넥션 하나당 OS 프로세스 하나를 띄운다.** MySQL은 스레드를 띄운다. 이 한 줄짜리 사실이 메모리 모델, 설정값, 운영 도구, 심지어 시스템 아키텍처 전체의 모양을 바꿔놓는다.

차이가 어디서 오는지 따라가보자. postmaster가 fork로 백엔드를 만드는 순간부터 시작해서, 클러스터 뒤에서 묵묵히 돌아가는 백그라운드 프로세스들, shared_buffers와 work_mem이 어떻게 나뉘어 사는지, max_connections를 무심코 1000으로 올리면 어떤 일이 벌어지는지, 그리고 끝에서는 — 왜 PG 진영에서 풀러가 "권장"이 아니라 "필수"라는 단어로 불리는지가 손에 잡힐 것이다. 같이 들여다보자.

## 4.1 postmaster와 fork — 1 connection = 1 process

처음으로 PG 서버를 띄웠다고 상상해보자. `pg_ctl start`를 치든, systemd로 올리든, 결과적으로 부모 프로세스 하나가 떠 있다. `ps` 명령으로 보면 `postgres` 또는 `postmaster`라는 이름의 프로세스 하나가 보일 것이다. 이 친구가 PG 클러스터 전체의 root다. postmaster라는 이름은 옛 이름인데 여전히 문서와 소스 코드에 자주 등장하니 익숙해두는 편이 낫다.

postmaster는 직접 쿼리를 처리하지 않는다. 그가 하는 일은 단 두 가지다. **들어오는 접속을 listen하고, 들어올 때마다 자식 프로세스를 fork한다.** 그게 전부다. 사장은 손님을 맞이만 하고, 주문은 직원 한 명을 새로 뽑아 그 직원에게 맡긴다고 보면 된다. 그 새 직원이 바로 *backend process*다.

```
postgres (postmaster)  ← 부모, listen만
 ├─ postgres: user1 db1 1.2.3.4 idle           ← 백엔드 1
 ├─ postgres: user2 db1 5.6.7.8 SELECT          ← 백엔드 2
 ├─ postgres: user1 db2 1.2.3.4 idle in tx     ← 백엔드 3
 ├─ postgres: background writer
 ├─ postgres: checkpointer
 ├─ postgres: wal writer
 ├─ postgres: autovacuum launcher
 ├─ postgres: logical replication launcher
 └─ postgres: stats collector
```

`ps -ef | grep postgres` 한 번만 쳐도 위 같은 그림을 그대로 본다. 커넥션 하나에 프로세스 하나. 위에서 사용자 `user1`이 같은 클라이언트(1.2.3.4)에서 두 개의 커넥션(db1, db2)을 들고 있다고 해도 OS 입장에서는 별개의 프로세스 두 개가 떠 있다. 같은 사용자, 같은 IP, 다른 DB — 셋 다 같아도 커넥션이 둘이면 프로세스도 둘이다.

여기서 잠시 멈춰서 묻자. **왜 이런 구조를 택했을까?** PG의 출생 시점인 1986년으로 돌아가보면 답이 자연스럽다. 그 시절 UNIX 세계는 fork 모델이 표준이었다. Apache HTTP Server의 prefork MPM, qmail, sendmail — 모두 같은 패턴이다. 스레드는 아직 portability가 약했고, 프로세스 격리가 가져다주는 안정성과 디버깅 용이성이 컸다. 한 프로세스가 죽어도 다른 백엔드에 거의 영향이 없다는 점은 지금까지도 PG의 강점으로 남아 있다.

물론 시대가 바뀌었다. 스레드는 이제 어디서나 잘 돌아간다. MySQL은 처음부터 thread-per-connection을 택했고, 그래서 한 인스턴스에 수천 커넥션을 무리 없이 들고 있을 수 있다. 그렇다면 PG도 스레드로 바꾸면 되지 않을까? 이 질문은 pgsql-hackers 메일링 리스트에서 주기적으로 올라온다. 그때마다 결론은 비슷하다 — "기술적으로 가능하긴 한데, PG의 모든 코드와 익스텐션이 프로세스 격리를 전제로 짜여 있다. 다 뜯어고치는 비용이 이득보다 훨씬 크다." 그래서 PG는 fork 모델을 고수한다.

이 결정이 평화로워 보이는 건 커넥션이 적을 때까지다. 백엔드 하나가 얼마나 무거운지부터 따져보자.

### 백엔드 한 개의 무게

새 커넥션이 들어오면 postmaster는 다음 일을 한다.

1. `fork()` 시스템 콜 호출 — 자식 프로세스 생성
2. 자식이 자신의 메모리 컨텍스트 초기화 — local memory 할당
3. 인증 절차 — `pg_hba.conf` 매칭, scram-sha-256 challenge/response
4. catalog 로드 — `pg_class`, `pg_attribute` 등의 시스템 카탈로그를 자기 캐시로
5. 사용자 정보, search_path, 세션 변수 세팅
6. 이제 비로소 쿼리를 받을 준비 완료

이 과정에 얼마나 걸릴까? 보통 5~50ms. 짧아 보이지만 OLTP 워크로드에서는 결코 짧지 않다. 1ms 안에 끝나는 쿼리를 받기 위해 50ms를 쓰는 건 본말이 전도된 셈이다. 그래서 어떤 애플리케이션도 PG에 직접 매 요청마다 새 커넥션을 열어 쓰지 않는다. 풀러를 쓰든, 애플리케이션 안에 connection pool을 두든, 어떻게든 재사용한다.

연결이 끊어질 때도 비슷한 일이 일어난다. 백엔드 프로세스는 즉시 종료되고, 그 프로세스가 점유하던 메모리는 OS에게 반환된다. 다음 새 커넥션이 들어오면 또 처음부터 fork를 한다. 즉 *커넥션 lifecycle은 곧 프로세스 lifecycle이다*. 짧은 커넥션을 빈번하게 열고 닫는 패턴은 PG에서는 가장 비싼 방식이다.

이게 PHP 같은 stateless 언어에서 PG를 직접 쓰면 끔찍하게 느려지는 이유다. 매 HTTP 요청마다 새 커넥션 → 매번 fork → 매번 인증 → 카탈로그 로드 → 짧은 쿼리 한 번 → 끊김. 50ms 셋업, 1ms 일, 끝. CPU의 99%가 인증과 fork에 쓰인다. PHP 진영에서 `pgbouncer`나 `persistent connection`을 강조하는 이유가 여기에 있다.

그런데 더 큰 문제는 시작 비용이 아니라 **유지 비용**이다. 한 번 만들어진 백엔드 프로세스는 가만히 있어도 메모리를 잡아먹는다. idle 상태에서도 보통 10~20MB의 RSS(Resident Set Size)를 점유한다. 거기에 work_mem, temp_buffers, 카탈로그 캐시가 누적되면 한 백엔드가 50~100MB를 차지하는 일이 흔하다. 5000개 커넥션이라면 — 그 자체로 250GB~500GB의 메모리다. shared_buffers가 들어갈 공간은 어디에 두려 했던가?

리눅스의 copy-on-write 덕분에 fork 직후의 메모리는 부모와 공유한다. 그래서 새 백엔드가 곧바로 50MB를 잡아먹는 건 아니다. 일을 시작하면서 자기 page table을 채워나가고, 결과적으로 RSS가 점점 커진다. 한참 일하다가 idle로 돌아간 백엔드의 RSS를 보면 — 처음 fork 직후와 비교해 메모리를 잘 안 놓아주는 모습을 본다. PG는 자기 안에 메모리 컨텍스트(MemoryContext)를 두고 거기서 할당/해제를 관리하는데, 큰 카탈로그를 한 번 캐시하면 그 자리가 잘 안 사라진다. 이게 *long-lived backend의 메모리 부풀기*다.

그래서 어떤 시스템들은 의도적으로 백엔드의 lifetime을 제한한다. PgBouncer의 `server_lifetime` 파라미터(기본 3600초)는 — 한 시간 산 백엔드는 풀러가 명시적으로 닫고 새로 만들도록 한다. 메모리를 주기적으로 정리하는 효과다. 21장에서 다시 만날 설정인데, 그 존재 이유가 바로 여기에 있다는 걸 알아두면 좋다.

여기까지 들으면 슬슬 불안해지기 시작한다. 그렇다면 어떻게 해야 할까? 답은 잠시 미뤄두자. 4.4와 4.5에서 본격적으로 다룰 이야기다. 지금은 한 가지만 기억해두자. **PostgreSQL에서 커넥션은 비싸다. 그리고 그 비용은 "조금 비싸다"가 아니라 "운영을 설계하는 수준으로 비싸다".**

## 4.2 백그라운드 프로세스 풀세트 — 클러스터 뒤에서 일하는 직원들

`ps`로 PG 프로세스 트리를 봤을 때 백엔드만 있는 건 아니었다. background writer, checkpointer, wal writer, autovacuum launcher 같은 친구들이 같이 떠 있었다. 이들은 누가 커넥션을 열지 않아도 PG가 시작되는 순간 자동으로 같이 뜬다. 그리고 클러스터가 살아 있는 동안 묵묵히 자기 일을 한다.

이 백그라운드 프로세스들이 무슨 일을 하는지 알아두면 PG 운영의 절반은 이해한 셈이다. 왜냐하면 PG의 거의 모든 성능 특성과 운영 통증이 이들의 동작에서 나오기 때문이다. 한 명씩 인사를 시켜보자.

### Background Writer — 더러운 페이지를 천천히 씻는 직원

쿼리가 데이터를 수정하면 그 변경은 일단 메모리(`shared_buffers`)의 페이지에 반영된다. 디스크에 바로 쓰지 않는다. WAL에는 곧바로 적히지만, 데이터 파일 자체는 나중에 한꺼번에 동기화한다. 이 "메모리에서는 바뀌었지만 디스크에는 아직 안 쓴" 페이지를 *dirty page*라고 부른다.

Background Writer는 이 dirty page들을 천천히, 꾸준히, 사용자가 못 느낄 정도의 속도로 디스크에 흘려보낸다. 비유하자면 식기세척기를 조용히 돌리는 친구다. 손님이 한꺼번에 몰릴 때 설거지가 산처럼 쌓이지 않도록, 평상시에 미리미리 정리해둔다.

왜 이 직원이 필요할까? 만약 background writer가 없다면, checkpoint 시점에 모든 dirty page를 한꺼번에 flush해야 한다. 그 순간 디스크 I/O가 폭주하고, 응답 지연이 튄다. 우리는 그것을 *checkpoint spike*라고 부르는데, 모니터링 대시보드에서 톱니 모양으로 튀어오르는 게 보이면 십중팔구 이 친구다. background writer가 평시에 일을 잘 해두면 checkpoint 때 할 일이 줄고, 톱니가 평탄해진다.

설정으로는 `bgwriter_delay`(기본 200ms), `bgwriter_lru_maxpages`(한 번에 쓸 최대 페이지), `bgwriter_lru_multiplier` 같은 파라미터가 있다. 보통은 기본값으로 충분하지만, write-heavy 워크로드에서 checkpoint spike가 심하면 `bgwriter_lru_maxpages`를 늘려 일을 더 시키는 편이 낫다.

### Checkpointer — 정해진 시각의 대청소

Checkpointer는 이름 그대로 *checkpoint*를 수행하는 친구다. Checkpoint란 무엇인가? "이 시점까지 commit된 모든 변경은 디스크에 영구히 반영되었다"고 선언하는 행위다. 이 선언은 두 가지 의미를 가진다.

첫째, 그 시점 이전의 WAL은 더 이상 복구에 필요 없다는 뜻이다(아카이브 보관 정책은 별개로 두고). 그래서 checkpoint가 끝나면 오래된 WAL 세그먼트를 재활용하거나 삭제할 수 있다. WAL 파티션 용량을 안 잡아먹게 하는 핵심 메커니즘이다.

둘째, 만약 클러스터가 갑자기 죽으면, 재시작할 때 *마지막 checkpoint 이후의 WAL만* replay하면 된다는 뜻이다. checkpoint가 자주 일어나면 복구가 빠르다. 대신 평시 I/O가 많아진다. 둘 사이의 균형을 잡는 게 운영자의 일이다.

설정은 `checkpoint_timeout`(기본 5분)과 `max_wal_size`(기본 1GB) 둘 중 먼저 도달하는 쪽에서 checkpoint가 트리거된다. 그리고 `checkpoint_completion_target`(0.9 권장)이 — 다음 checkpoint까지의 시간을 얼마나 길게 잡아 천천히 flush할지를 결정한다. 0.9는 "다음 checkpoint 직전 10% 시점까지 천천히 쓰겠다"는 뜻이다. 톱니를 더 둥글게 만든다.

여기서 자주 보는 함정 하나. `max_wal_size`를 1GB 기본값으로 두고 write 많은 시스템을 돌리면, 5분 timeout보다 1GB 한계가 훨씬 먼저 터진다. 그 결과 checkpoint가 30초에 한 번씩 일어나기도 한다. 그러면 background writer가 일할 틈도 없이 계속 대청소가 도는 셈이다. 끔찍한 일이다. write-heavy 시스템이라면 `max_wal_size`를 4GB, 8GB, 16GB로 과감하게 늘려야 한다. 디스크가 받쳐주는 한.

### WAL Writer — 거래 장부를 적는 직원

WAL(Write-Ahead Log)은 PG의 모든 변경을 기록하는 거래 장부다. 7장에서 WAL 자체의 내부 구조를 깊이 다룰 테니, 여기서는 WAL Writer가 뭘 하는지만 가볍게 짚자.

쿼리가 커밋되면 그 변경은 WAL buffer(메모리)에 먼저 기록된다. 이걸 디스크에 flush해야 진짜 영구적이 된다. flush를 누가 할까? 두 가지 경우다. 첫째, 커밋한 백엔드 본인이 fsync로 직접 한다(synchronous_commit=on의 경우). 둘째, WAL Writer가 주기적으로 깨어나 일괄로 한다.

WAL Writer의 존재 이유는 무엇일까? `synchronous_commit=off` 같은 비동기 모드에서, 그리고 커밋하지 않은 변경의 WAL buffer를 미리미리 디스크로 흘려보내기 위해서다. 그러면 fsync 부담이 분산된다.

PostgreSQL 17은 이 WAL Writer의 메모리 사용을 다시 썼다. 이전에는 작은 변경마다 WAL buffer를 자주 잠그고 풀어야 했는데, 17부터는 lock-free에 가까운 방식으로 처리한다. 17 release note의 "WAL writer memory improvements"가 바로 이 얘기다. 결과적으로 write-heavy OLTP에서 5~15% 정도의 throughput 향상이 보고된다. 18로 가는 길에 이런 작은 개선들이 누적된다.

### WAL Archiver — 장부를 외부 금고로 옮기는 직원

`archive_mode = on`을 켜고 `archive_command`를 지정하면 WAL Archiver가 깨어난다. 이 친구는 닫힌 WAL 세그먼트(보통 16MB짜리 파일)를 S3, NFS, 또는 다른 백업 저장소로 복사한다. 복사가 성공하면 그 WAL은 클러스터에서 안전하게 재활용해도 된다.

이게 왜 중요할까? PITR(Point-In-Time Recovery)의 토대가 되기 때문이다. base backup + WAL archive를 합치면, 사고가 난 시각의 1분 전, 1초 전으로도 클러스터를 되돌릴 수 있다. 19장에서 pgBackRest와 함께 자세히 다룰 친구다.

운영에서 가장 흔히 발생하는 사고는 — archive_command가 실패하기 시작했는데 모니터링이 그걸 못 잡는 경우다. 실패하면 WAL이 안 지워진다. 안 지워지면 pg_wal 파티션이 가득 찬다. 가득 차면 클러스터가 멈춘다. 새벽 3시에 이 사고로 깨어나본 사람은 안다. 진짜로 난감하다. archive_command의 실패를 알리는 알람은 반드시 걸어두어야 한다.

### Autovacuum Launcher와 Worker — 가장 PG다운 직원

이 친구들이야말로 PG의 정체성이다. 5장에서 MVCC와 VACUUM의 운명적인 짝을 깊이 들여다볼 테니, 여기서는 프로세스 모델 관점만 짚자.

Autovacuum Launcher는 부모 프로세스 하나로 떠 있다가, 정해진 주기(`autovacuum_naptime`, 기본 1분)마다 데이터베이스를 스캔하고 vacuum이 필요한 테이블을 찾는다. 필요한 테이블이 있으면 worker process를 fork해서 일을 시킨다. 동시에 일할 수 있는 worker 수는 `autovacuum_max_workers`(기본 3)로 제한된다.

여기서 잠깐. **autovacuum worker도 결국 backend process다.** 즉 max_connections에 들어가는 슬롯을 쓰지는 않지만, 메모리와 CPU는 일반 백엔드와 똑같이 쓴다. 1억 row 테이블 vacuum 한 번이 몇 GB의 메모리와 디스크 I/O를 잡아먹는다는 사실을 잊지 말자. autovacuum_work_mem(기본 -1, 즉 maintenance_work_mem 따라감)을 적절히 잡아야 한다.

### Logical Replication Launcher — 새로운 표준

PG 10에서 logical replication이 들어오면서 추가된 친구다. publication과 subscription을 관리하고, walsender/walreceiver 프로세스를 띄워준다. 13장에서 CDC와 logical decoding을 다룰 때 다시 만날 것이다.

17 이전에는 페일오버 후에 logical replication slot이 사라지는 문제가 있어서 운영에서 골칫거리였는데, 17의 failover slot 기능이 이걸 해결했다. 14장에서 다시 짚는다.

### Stats Collector / Background Worker

PG 15부터 stats collector는 shared memory 기반으로 재작성되어 별도 프로세스가 사라졌다. 하지만 여전히 백그라운드 어딘가에서 통계가 누적된다. 그리고 pg_cron, pgmq 같은 익스텐션들은 background worker 슬롯을 빌려 자기 프로세스를 띄운다. `max_worker_processes`(기본 8) 안에서 익스텐션들이 자리를 나눠 쓴다.

### 백그라운드 프로세스들의 건강을 보는 법

각 프로세스가 자기 건강 정보를 어디에 적는지 알아두면 운영이 한결 수월하다. 자주 보는 뷰만 짧게 정리하자.

- **Background Writer**: `pg_stat_bgwriter`. `buffers_clean`(BG writer가 쓴 양), `buffers_checkpoint`(checkpointer가 쓴 양), `buffers_backend`(백엔드가 직접 flush한 양)의 비율을 본다. backend가 쓴 비율이 높으면 BG writer가 일을 덜 하고 있다는 신호.
- **Checkpointer**: 같은 뷰의 `checkpoints_timed`(정시 발생)와 `checkpoints_req`(WAL 크기 도달로 강제 발생)의 비율. requested가 timed보다 많으면 max_wal_size를 올리자.
- **WAL Writer**: `pg_stat_wal`(14부터). `wal_records`, `wal_bytes`, `wal_buffers_full`(buffer 부족 횟수). wal_buffers_full이 자주 보이면 wal_buffers를 키울 신호.
- **Autovacuum**: `pg_stat_progress_vacuum`(진행 중인 vacuum의 실시간 상태), `pg_stat_user_tables`(테이블별 last_autovacuum 시각). autovacuum이 평균 몇 시간씩 안 돌면 — 그건 테이블 크기 대비 scale_factor가 너무 높다는 신호.

이 뷰들은 모두 누적값이라, 모니터링 도구에서 *delta* 형태로 보는 편이 의미 있다. Prometheus + postgres_exporter + Grafana 조합이 표준이다. 21장에서 모니터링 스택 전체를 다룬다.

### 백엔드 외에도 적어도 10개의 프로세스가 더

`ps`를 다시 한번 보자. 백엔드 외에도 7~10개의 프로세스가 항상 떠 있다. 이게 PG의 "프로세스 비용"의 진짜 모습이다. 백엔드 하나당 메모리 50MB라고 했을 때, 백그라운드 프로세스들도 각자 자기 메모리를 쓴다. 작은 시스템도 PG 한 번 띄우면 500MB는 쉽게 잡아먹는다.

그리고 이 친구들 모두가 같은 `shared_buffers`를 공유한다. 다음 절에서 그 메모리 구조를 들여다보자.

## 4.3 shared_buffers, WAL buffer, work_mem — PG 메모리 모델의 삼각형

PG 메모리 설정에서 가장 많이 보이는 세 가지 파라미터가 있다. `shared_buffers`, `wal_buffers`, `work_mem`. 이름은 비슷해 보여도 사는 곳도, 쓰임새도, 영향 범위도 완전히 다르다. 이 셋을 헷갈리면 메모리 튜닝이 전부 어긋난다. 차례로 알아보자.

### shared_buffers — 모두가 공유하는 큰 풀

`shared_buffers`는 이름 그대로 *공유* 메모리다. postmaster가 시작될 때 OS에게 한 번 거대한 메모리 블록을 요청한다. 그러고 나서 모든 백엔드와 백그라운드 프로세스가 이 블록에 함께 접근한다. 데이터 페이지(보통 8KB 단위)가 여기에 캐시된다.

비유하자면 사무실의 중앙 자료실이다. 직원(백엔드)들이 자기 자리에서 직접 디스크(서고)에서 자료를 꺼내오는 게 아니라, 일단 중앙 자료실에 있는지 보고, 있으면 거기서 빌려 쓴다. 없으면 누군가가 디스크에서 꺼내와 자료실에 비치하고, 그 다음부터는 모두가 거기서 본다.

권장 크기는 시스템 RAM의 25% 정도. 64GB 머신이면 16GB. 왜 50%, 75%가 아닐까? 두 가지 이유가 있다.

첫째, PG는 자기만의 캐시(shared_buffers)와 OS의 페이지 캐시를 둘 다 활용하는 *double caching* 모델이다. shared_buffers를 너무 키우면 OS 페이지 캐시가 줄어들고, 결과적으로 둘 다 효율이 떨어진다. 25%가 경험적으로 좋은 균형점이다.

둘째, work_mem과 백엔드 RSS가 들어갈 자리도 남겨둬야 한다. 500개 커넥션이 work_mem 32MB를 동시에 쓰면 그것만 16GB다. 거기에 백엔드 RSS, 백그라운드 프로세스, OS, 그리고 안전 마진까지. 25%로 잡아두면 보통 다른 것들과의 균형이 맞다.

물론 워크로드에 따라 다르다. 분석 워크로드(OLAP)는 데이터 캐시 hit rate가 결정적이라 40%, 50%까지 잡기도 한다. OLTP는 25%가 무난하다. 실제로 자기 시스템에서 `pg_stat_database.blks_hit / (blks_hit + blks_read)`로 cache hit ratio를 보면 — 99% 이상이면 충분히 큰 것이고, 95% 이하면 더 늘려볼 만하다.

진단 쿼리를 하나 적어두자. 실무에서 자주 쓴다.

```sql
SELECT
  datname,
  blks_hit,
  blks_read,
  ROUND(100.0 * blks_hit / NULLIF(blks_hit + blks_read, 0), 2) AS hit_ratio
FROM pg_stat_database
WHERE datname NOT IN ('template0', 'template1', 'postgres')
ORDER BY blks_read DESC;
```

이 쿼리를 평상시와 피크 시간대에 각각 돌려보자. 평소엔 99%인데 피크에 92%로 떨어진다면 — 그 시간대에 특정 큰 테이블이 들어와 캐시를 밀어내고 있다는 신호다. shared_buffers를 늘리거나, 그 큰 쿼리의 작업 패턴을 바꾸는 방향으로 처방이 갈린다.

한 가지 더. 32GB 이상의 shared_buffers를 쓸 때는 `huge_pages = try` 또는 `huge_pages = on` 설정과 OS의 hugepage 설정을 같이 챙겨야 한다. 일반 4KB 페이지로 32GB를 관리하면 page table만 수 MB가 되고 TLB miss가 잦아진다. 2MB hugepage를 쓰면 page table이 작아져 메모리 접근 효율이 올라간다. 큰 PG 인스턴스의 숨은 튜닝 포인트다.

### WAL buffer — 거래 장부의 임시 메모

`wal_buffers`는 WAL 데이터를 디스크에 쓰기 전 임시로 모아두는 메모리다. 쿼리가 변경을 만들면 그 변경의 WAL 레코드가 일단 여기에 적힌다. WAL Writer나 커밋하는 백엔드가 이걸 fsync로 디스크에 흘려보낸다.

크기는 보통 `shared_buffers / 32` 정도가 자동 계산된 기본값이고, 보통 최대 16MB가 한계다. 굳이 손댈 일이 많지 않다. 다만 한 가지 — `synchronous_commit=off`로 비동기 커밋을 쓰는 시스템이라면 wal_buffers를 32MB나 64MB로 키워두는 편이 throughput에 유리하다는 보고가 있다. write-heavy + sync off 조합이라면 한 번 실험해볼 만하다.

기본값으로 두고 잊어버려도 큰 문제가 안 생기는 친구다. 다만 17부터 WAL writer가 lock-free하게 바뀌면서 이 버퍼의 활용 효율이 올랐다. 16에서 17로 올리는 것만으로도 write throughput이 늘어나는 이유 중 하나다.

### work_mem — 백엔드 한 명이 한 연산에 쓰는 메모리

여기가 가장 까다롭고, 가장 자주 사고가 나는 영역이다. 정신을 똑바로 차리자.

`work_mem`은 백엔드 한 명이, 한 쿼리 안에서, 한 연산(sort, hash join, hash aggregate 등) 한 번에 쓰는 메모리의 최대값이다. 기본값은 4MB. 이 한도를 넘는 sort는 디스크 임시 파일로 떨어진다(*disk sort*). 디스크 sort는 메모리 sort보다 10~100배 느리니, 자주 발생하면 쿼리 성능이 폭락한다.

그래서 흔히들 "work_mem을 늘려야 한다"고 한다. 64MB, 128MB로 올리면 sort가 디스크로 안 떨어지고 빠르다는 식이다. 맞는 말이긴 하다. 그런데 *어떤 단위*에 곱해지는지가 문제다.

**work_mem은 백엔드 × 연산 단위로 곱해진다.**

다시 한번 강조하자. 백엔드 × 연산. 즉 한 쿼리 안에 sort 3개, hash join 2개가 있으면 그 쿼리 하나가 work_mem × 5만큼 쓴다. 거기에 동시 실행 백엔드가 100개라면 — work_mem × 5 × 100 = work_mem × 500. work_mem이 64MB라면 그 자체로 32GB다.

찜찜하지 않은가? 실제로 이 함정에 빠진 시스템을 본 적이 있다. work_mem을 256MB로 올렸더니 평소엔 잘 돌다가, 어느 날 분석 쿼리 몇 개가 동시에 들어오자 OS OOM killer가 PG postmaster를 죽여버렸다. 한 번에 클러스터가 사라진다. 끔찍한 일이다.

권장 패턴은 이렇다.

- **기본 work_mem은 보수적으로**: 4MB~16MB. 평상시 OLTP에는 충분하다.
- **특정 분석 쿼리에서만 키워라**: 세션 단위로 `SET LOCAL work_mem = '256MB'` 후 쿼리 실행, 트랜잭션 끝나면 자동 복귀. 또는 분석 전용 role에 `ALTER ROLE analyst SET work_mem = '128MB'`로 분리.
- **항상 max_connections와 함께 계산**: `work_mem × max_connections × 평균 연산 개수 < 사용 가능 메모리의 30%` 정도가 안전선이다.

13으로 올라오면서 PG는 `hash_mem_multiplier`라는 친구를 추가했다. hash 연산(hash join, hash aggregate)만 work_mem의 N배까지 쓸 수 있게 허용하는 파라미터다. 기본 2. 즉 work_mem이 16MB면 hash 연산은 32MB까지 쓴다. 분석 쿼리에서 hash 연산이 sort보다 메모리를 더 효율적으로 쓰는 경향이 있어, hash만 더 풀어주자는 취지다.

실전에서 work_mem이 부족한지 어떻게 알 수 있을까? 두 가지 신호다. 첫째는 `log_temp_files = 0`을 설정해두면 — 일정 크기 이상의 임시 파일이 만들어질 때마다 PG가 로그에 남긴다. 그 로그가 자주 보이면 work_mem이 부족하다는 뜻이다. 둘째는 `EXPLAIN (ANALYZE, BUFFERS)`로 쿼리를 실행하면 sort 노드에 `external merge Disk: 12345kB` 같은 표시가 보인다. "Disk"가 보이면 disk sort로 떨어졌다는 신호. work_mem을 그 쿼리 세션에서만 임시로 올려서 다시 실행해보면 비교가 된다.

여기서 흔한 실수 하나 — `SET work_mem = '256MB'`를 후 잊고 그 세션이 계속 살아 있는 경우다. 그 세션에서 도는 모든 쿼리가 256MB를 쓴다. 풀러를 통해 그 세션이 다른 트랜잭션에 재사용되면, 풀러를 거친 모든 트랜잭션이 256MB를 쓴다. `SET LOCAL`을 쓰면 트랜잭션 끝에서 자동 복귀하니, 임시 변경은 항상 `SET LOCAL`로 하는 편이 안전하다.

### maintenance_work_mem과 autovacuum_work_mem

`maintenance_work_mem`은 VACUUM, CREATE INDEX, REINDEX, ALTER TABLE ADD CONSTRAINT 같은 유지보수 작업에서 쓰는 메모리다. 기본 64MB. 큰 테이블의 인덱스 빌드 속도가 여기에 직결되니, 평소 1GB 정도로 잡아두는 편이 낫다.

`autovacuum_work_mem`은 autovacuum worker가 쓰는 메모리. 기본 -1이면 maintenance_work_mem 값을 따라간다. autovacuum_max_workers가 3이면 동시 3개의 worker가 각자 maintenance_work_mem만큼 쓸 수 있다는 뜻 — 1GB로 잡았다면 3GB까지 쓸 수 있다. 큰 테이블 vacuum이 메모리를 많이 먹는 시스템이라면 이걸 따로 작게 잡는 편이 안전하다.

### 메모리 모델 한눈에 정리

지금까지 본 메모리를 그림으로 그려보자.

```
[ OS 메모리 64GB ]
├─ [ OS 페이지 캐시 ]               ← 대략 30~40% (~25GB)
├─ [ shared_buffers ]               ← 25% (~16GB), 모든 PG 프로세스가 공유
│   ├─ data page cache (8KB 단위)
│   ├─ index page cache
│   ├─ catalog cache
│   └─ lock table, predicate locks (SSI용)
├─ [ wal_buffers ]                  ← 16MB 내외
├─ [ 백엔드 프로세스 풀 ]            ← max_connections × (RSS + work_mem 변동)
│   ├─ backend 1: RSS 60MB + work_mem 사용분
│   ├─ backend 2: ...
│   └─ ...
├─ [ 백그라운드 프로세스들 ]         ← 각 10~50MB
└─ [ 안전 마진 / 시스템 ]            ← OS, swap 방지 여유분
```

이 그림에서 한 가지를 잊지 말자. **백엔드 슬롯은 max_connections로 정해진다.** 그리고 백엔드가 늘어나면 가장 먼저 깎아 먹히는 게 OS 페이지 캐시다. 페이지 캐시가 깎이면 PG가 디스크에서 읽어야 할 양이 늘어나고, 쿼리가 느려진다. 느려지면 백엔드가 더 오래 살아남고, 더 많은 새 커넥션이 쌓인다. 악순환이다.

여기까지 오면 자연스럽게 다음 질문이 떠오른다. "그럼 max_connections는 도대체 얼마로 잡아야 하는가?"

## 4.4 max_connections를 함부로 올리면 안 되는 이유

처음 PG를 운영하는 팀에서 가장 흔히 보는 풍경이 있다. 애플리케이션이 "too many connections" 에러를 토하기 시작한다. 슬랙에 알람이 울린다. 누군가가 빠르게 `max_connections`를 100에서 500으로, 다시 1000으로 올린다. 알람이 멈춘다. 평화가 찾아온다. 끝.

이런가? 안타깝게도 그렇지 않다. 알람이 멈춘 게 아니라, **다음 알람이 더 큰 사고로 미뤄진 것**이다. 그리고 그 다음 알람은 더 크게, 더 늦은 시간에, 더 복구하기 어려운 형태로 온다. max_connections를 손볼 때 무엇을 같이 봐야 하는지 같이 따라가보자.

### 무엇이 같이 늘어나는가

`max_connections = 1000`으로 잡았다고 해보자. 이 한 줄이 시스템에 가져오는 변화는 단순하지 않다.

먼저 메모리. 백엔드 하나가 idle 상태에서도 RSS 50MB라고 했을 때 — 1000 × 50MB = 50GB가 백엔드 메모리만으로 잡아먹힌다. 64GB 머신이라면 OS와 shared_buffers 자리가 사라진다. 일하지도 않는 idle 커넥션이 메모리 절반을 점유한다. 그 자체로도 손해지만, 진짜 문제는 페이지 캐시가 깎인다는 거다. 페이지 캐시가 깎이면 같은 쿼리가 느려진다. 느려지면 커넥션이 더 오래 점유된다. 악순환.

다음은 컨텍스트 스위치. CPU는 한 번에 한 프로세스만 돌릴 수 있다. 1000개 백엔드가 동시에 일하려고 하면 OS 스케줄러가 광속으로 컨텍스트 스위치를 돈다. 한 번 스위치에 보통 1~10μs가 들고, 캐시 라인이 깨지면서 실효 비용은 더 크다. CPU가 8코어인데 active 백엔드가 200개라면 — 한 코어가 25개를 돌려야 한다. 어느 백엔드도 충분히 일하지 못한다.

여기에 lock 경합이 더해진다. 트랜잭션이 같은 row나 page에 접근하려고 하면 lock을 잡는다. 동시 트랜잭션이 많을수록 wait queue가 길어진다. 더 많은 백엔드가 더 짧은 시간씩 일하려고 하면 — 결국 lock 대기에 더 많은 시간을 쓴다.

마지막으로 **shared 자원의 한계**. PG는 max_connections에 비례해 lock table, semaphore, shared memory 영역을 미리 할당한다. 즉 max_connections를 1000으로 잡으면 PG는 시작할 때 그만큼 자리를 잡아둔다. 안 쓰는 자리도 다 비워둔다. 메모리는 그렇게 사라진다.

### 실제 사고는 어떻게 일어나는가

추상적으로 들리지 않게, 가상의 사고 시나리오 하나를 따라가보자. 흔하다.

월요일 오전 10시. 서비스 트래픽이 평소보다 30% 더 많다. 백엔드 한 곳에서 외부 API 호출이 평소보다 200ms 느려졌다. 그 API 호출이 트랜잭션 안에 있다. 즉 트랜잭션 lifetime이 길어졌다. 활성 백엔드가 평소 50개에서 150개로 늘었다.

10시 15분. "too many connections" 에러가 슬랙에 뜬다. 운영자가 빠르게 max_connections를 200에서 500으로 올린다. PG를 재시작한다 (다행히 페일오버로 다운타임 5초). 알람이 멈춘다.

10시 30분. 응답 시간이 평소의 3배가 됐다. 모니터링을 보니 active 백엔드가 350개. CPU usage는 100%. 그런데 throughput은 평소의 1/2. 컨텍스트 스위치가 분당 수십만 번 일어난다. 어느 백엔드도 충분히 일하지 못한다.

10시 45분. OS의 `free -m`을 보니 buffers/cache가 거의 0. swap에 들어가기 시작한다. 그러면 PG는 더 느려진다. 느려지면 백엔드가 더 오래 살아남고, 더 많은 클라이언트가 재시도하면서 새 커넥션이 더 쌓인다.

11시. OOM killer가 깨어난다. 가장 큰 메모리 사용자를 찾는다 — postmaster다. 죽인다. 클러스터 전체가 사라진다. 페일오버는 standby도 비슷한 부하를 받고 있어 발동에 실패한다. **클러스터 다운.**

이게 max_connections를 무심코 올린 결정 하나가 데려오는 결과다. 시작은 외부 API의 200ms 지연이었는데, 끝은 전체 서비스 다운이다. 그리고 이 시나리오의 매 단계에서 *풀러가 앞에 있었다면 막을 수 있었던 일*이다. 풀러가 active 백엔드 수를 100개로 제한하고, 초과 요청은 풀에서 대기시켰다면 — 트랜잭션 lifetime이 길어진 만큼 처리량이 줄었을 뿐, 시스템이 무너지지는 않는다.

### 황금률 — connection 수 ≈ CPU core × N

운영자들 사이에서 통용되는 경험적 규칙이 있다.

**Active connection 수는 CPU core × 2~3을 넘기지 않는 게 좋다.**

8 core 머신이면 동시 active 백엔드 16~24개가 sweet spot이다. 그 이상으로 늘어나면 컨텍스트 스위치 비용이 처리량 증가를 잡아먹는다. 이 숫자는 PgBouncer 공식 문서, EDB 가이드, Crunchy Data 블로그에서 비슷한 결로 반복해서 나온다.

여기서 의문이 들 수 있다. "active가 24개여야 한다면, max_connections를 100이나 200으로 잡아도 충분하지 않나? 왜 굳이 1000이 필요할까?" 정답은 — *필요하지 않다*. 잘 운영되는 PG 시스템의 max_connections는 보통 100~300 사이다. 그것보다 많이 잡았다면, 그건 풀러가 빠져 있다는 신호다.

### 1000 커넥션을 받아야 한다면

물론 애플리케이션 쪽에서 1000, 2000, 10000개의 동시 연결을 요구하는 경우는 흔하다. 모바일 앱, 마이크로서비스 메시, 서버리스 함수 — 모두 클라이언트 측 커넥션 수가 폭주하는 패턴이다. 이걸 PG가 직접 받지 않는다.

대신 풀러를 앞에 둔다. 클라이언트는 PgBouncer에 1000개 연결을 한다. PgBouncer는 그 1000개를 multiplexing해서 PG에는 50개의 backend connection만 유지한다. 1000개의 클라이언트가 시간을 나눠 그 50개 슬롯을 돌려쓴다. 대부분의 OLTP 쿼리는 ms 단위로 끝나니까, 클라이언트 입장에서는 거의 즉시 자기 슬롯을 얻는다.

여기서 PgBouncer가 어떻게 동작하는지 더 깊이 들어가고 싶을 수 있는데, 그 얘기는 21장으로 미루자. 21장은 PgBouncer의 세 가지 모드(session/transaction/statement), 각 모드의 함정(prepared statement, advisory lock, SET LOCAL), Pgcat과 Odyssey의 차이를 본격적으로 다룬다. 4장의 일은 "왜 풀러를 써야 하는가"의 답을 끝까지 손에 잡히게 만드는 것이다. 도구 선택은 21장에서.

### 매니지드 PG에서는 어떻게 다른가

RDS, Aurora, Cloud SQL을 쓰는 사람이라면 — max_connections가 인스턴스 크기에 따라 자동으로 잡혀 있다. AWS의 default 공식은 대략 `LEAST({DBInstanceClassMemory/9531392}, 5000)` 같은 식인데, db.r5.large(15GB)면 약 1660, db.r5.xlarge(30GB)면 약 3300이다. 너무 크다.

이 자동값을 그대로 쓰면 위에서 말한 모든 문제를 그대로 받는다. RDS Proxy나 PgBouncer를 같이 띄우고 max_connections를 의도적으로 낮춰 잡는 편이 안전하다. AWS는 Aurora의 경우 `aurora_max_connections_per_user`라는 추가 제한도 두니, 이걸 활용하면 폭주를 막을 수 있다. 24장 클라우드 챕터에서 매니지드 PG의 함정을 더 짚는다.

### 안전선 — 어떻게 시작할 것인가

처음 PG를 운영하는 팀이 max_connections를 잡는 보수적 시작점은 이렇다.

- **shared_buffers**: RAM의 25%
- **work_mem**: 8MB (기본보다 약간 위)
- **maintenance_work_mem**: 1GB
- **max_connections**: `(가용 메모리 - shared_buffers - 안전 마진) / (백엔드 평균 메모리)`

64GB 머신, shared_buffers 16GB, OS와 OS 캐시 20GB 남기고 싶다면 — 백엔드 풀에 28GB. 백엔드 하나당 100MB 가정하면 280. 보수적으로 200으로 시작하자. 그리고 풀러를 앞에 둔다.

200이 부족해 보이는가? 풀러가 잘 동작하면 충분하다. PgBouncer transaction pooling 기준 200 backend가 수천 클라이언트의 OLTP를 충분히 받는다. 200으로 부족하다고 느낀다면, 그건 max_connections를 올릴 신호가 아니라 — 쿼리가 너무 오래 걸리고 있거나, 트랜잭션이 너무 길거나, 풀러 설정이 틀린 신호일 가능성이 높다.

200으로 시작한 뒤에 진짜 모니터링해야 할 지표는 max_connections가 아니다. 다음 셋이다.

- **active 백엔드 수**: `SELECT count(*) FROM pg_stat_activity WHERE state = 'active'`. CPU core × 2~3을 자주 넘으면 풀러 설정을 다시 보자.
- **idle in transaction 백엔드 수**: `SELECT count(*) FROM pg_stat_activity WHERE state = 'idle in transaction'`. 0보다 크면 무조건 의심하자. 트랜잭션 중에 멈춰 있는 백엔드가 있다는 뜻이고, 그 자체로 vacuum을 막고 lock을 잡는다.
- **백엔드 별 메모리 사용**: `ps` 또는 `pg_stat_activity`의 `backend_xmin`과 OS 메트릭 결합. 평균 RSS가 100MB를 넘기 시작하면 work_mem 사용 패턴을 의심하자.

이 셋이 평상시에 안정적이라면 — max_connections는 손댈 일이 거의 없다. 시스템이 알려주는 신호를 따르는 운영이 가장 안전하다.

## 4.5 PG에 풀러가 필수인 이유 — fork 모델이 데려오는 결론

여기까지 따라온 사람이라면, 풀러가 왜 필요한지의 답이 거의 자기 안에 있을 것이다. 정리만 하면 된다. 끝까지 같이 와보자.

### 다섯 가지 비용을 한 번 더

PG에서 raw connection이 비싼 이유를 한 번에 모아보자.

**첫째, fork 비용.** 새 커넥션마다 OS fork 시스템 콜이 일어난다. 5~50ms. 단순 OLTP 쿼리 한 번이 1ms라면, 초기화에 50ms 쓰는 셈이다. 50배 오버헤드다.

**둘째, 메모리 비용.** 백엔드 하나가 idle 상태에서 RSS 50MB. work_mem이 더해지면 100MB도 흔하다. 1000 커넥션 = 50~100GB. shared_buffers와 OS 페이지 캐시가 들어갈 자리가 없다.

**셋째, 컨텍스트 스위치 비용.** 1000개 백엔드가 동시에 일하려 들면 OS 스케줄러가 분쇄기처럼 돈다. 어느 백엔드도 충분히 일하지 못한다.

**넷째, lock 경합 비용.** 동시 트랜잭션이 많을수록 lock wait queue가 길어진다. 같은 row, 같은 page에 더 많은 손이 모이면, 진짜로 일하는 시간보다 기다리는 시간이 길어진다.

**다섯째, shared 자원의 사전 할당 비용.** max_connections에 비례해 lock table, semaphore, predicate lock 영역이 미리 할당된다. 안 쓰는 자리도 다 잡혀 있다.

이 다섯 가지가 한꺼번에 시스템을 누른다. 풀러는 이걸 모두 완화한다. fork 비용을 한 번만 치르고 재사용한다. 메모리 사용을 일정하게 묶는다. active 백엔드 수를 CPU core × N 안에 가둔다. lock 경합 빈도를 낮춘다. shared 자원을 작게 잡고 시작하게 한다.

### "권장"이 아니라 "필수"인 이유

MySQL과 비교하면 차이가 선명해진다.

MySQL의 thread-per-connection은 한 커넥션이 메모리 1~2MB 정도다(thread stack + 약간의 buffer). 1000 커넥션이라도 1~2GB. fork도 없다. 컨텍스트 스위치도 스레드 단위라 프로세스보다 가볍다. 그래서 MySQL은 raw connection을 수천 개 들고 있어도 큰 문제가 없다. 풀러를 쓰는 건 성능 최적화의 영역이다.

PG의 process-per-connection은 한 커넥션이 50~100MB. 1000 커넥션이면 50~100GB. fork 비용도 있고, 컨텍스트 스위치도 무겁다. 풀러를 안 쓰면 시스템이 메모리와 스케줄러 양쪽에서 무너진다. 풀러를 쓰는 건 *생존*의 영역이다.

그래서 PG 진영의 거의 모든 가이드 — PostgreSQL 공식 wiki, EDB, Crunchy Data, AWS RDS 베스트 프랙티스, Percona, Tiger Data — 가 동일한 결론을 낸다. "**PgBouncer 같은 외부 풀러는 권장이 아니라 사실상 필수다.**" 단어 선택이 우연이 아니다.

### 풀러 없이 갈 수 있는 경우는 없을까

물론 있다. 다음 조건이 모두 맞으면 풀러가 없어도 큰 문제가 안 생긴다.

- 동시 클라이언트 수가 max_connections보다 충분히 작다 (예: 데이터 분석가 5명만 쓰는 warehouse)
- 클라이언트가 자기 안에 connection pool을 똑똑하게 구현했다 (예: HikariCP, pgbouncer-like client pool)
- 커넥션 lifetime이 길고 reuse rate가 높다

이 조건은 작은 시스템, 또는 잘 통제된 서버 사이드 환경에서 만족된다. Java 애플리케이션이 HikariCP로 50개 백엔드만 유지한다면 — PG 입장에서는 사실상 50 커넥션짜리 풀러가 앞에 있는 셈이다. 추가 풀러가 꼭 필요하지는 않다.

하지만 그 외의 모든 경우 — 마이크로서비스 메시, 모바일 앱, 서버리스 함수, 여러 서비스가 같은 DB를 쓰는 환경 — 에서는 풀러를 빼면 시간 문제로 사고가 난다. 그래서 *기본적으로 풀러를 깔고 시작하는 것*이 PG 운영의 표준 패턴이다.

### 풀러의 위치 — 어디에 두는가

풀러는 보통 세 군데 중 하나에 둔다.

**클라이언트 측 (애플리케이션 안)**: HikariCP(Java), psycopg2.pool(Python), pgx pool(Go) 등. 가장 가깝다. 네트워크 hop이 없다. 단점은 각 애플리케이션 인스턴스마다 풀이 따로 산다는 것 — 10개 인스턴스가 각자 50개 커넥션을 들면 PG에는 500 커넥션이 도달한다. 오토스케일링 환경에서는 인스턴스가 늘어나면 그만큼 PG 커넥션도 폭증한다. 클라이언트 풀만으로 모든 트래픽 패턴을 통제하기는 번거롭다.

**중간 레이어 (전용 풀러 서버)**: PgBouncer, Pgcat을 별도 호스트에 띄우거나 사이드카로 둔다. 모든 애플리케이션 인스턴스의 커넥션을 한 곳에서 multiplexing한다. PG의 백엔드 수는 풀러 설정 하나로 통제된다. 가장 일반적인 운영 패턴.

**클라우드 측 (매니지드 풀러)**: AWS RDS Proxy, Cloud SQL Auth Proxy 등. 벤더가 운영을 책임진다. 편하지만 비용이 추가되고, 풀러 설정의 자유도가 제한된다. RDS Proxy는 시간당 과금이라 트래픽이 크지 않으면 비싸게 느껴질 수 있다.

대규모 운영이라면 보통 두 번째와 세 번째를 조합한다. RDS Proxy를 앞에, 그 뒤에 애플리케이션 측 풀도 두는 식이다. 어떤 도구를 어떻게 고를 것인가는 — 다시 말하지만 — 21장의 주제다.

### 풀러가 하는 일을 한 번 더 — multiplexing의 정체

풀러를 너무 신비롭게 들지 않도록, 풀러가 실제로 하는 일을 한 번만 미리 짚어두자. 21장에서 세 가지 모드(session/transaction/statement)와 함정들을 자세히 다룰 것이고, 여기서는 4장이 답해야 할 *왜*의 마지막 조각만 채운다.

PgBouncer 같은 풀러를 PG 앞에 두면 클라이언트와 PG 사이의 관계가 두 단계로 쪼개진다.

```
[ App ] ─ TCP ─ [ PgBouncer ] ─ TCP ─ [ PG backend ]
  (client conn)    (multiplexer)    (server conn)
```

클라이언트는 PgBouncer에 연결한다. PgBouncer는 이 연결을 가볍게 받는다(파이썬 어레이 한 줄 정도의 비용). 클라이언트가 쿼리를 보내면, PgBouncer는 자기 안의 *server connection pool*에서 놀고 있는 PG backend 하나를 빌려와서 그 backend에 쿼리를 전달한다. 쿼리 결과가 돌아오면 backend는 다시 풀로 반환되고, 다음 클라이언트의 쿼리에 재사용된다.

PG 입장에서는 100개의 backend가 평생 유지된다. 그 100개의 backend가 1000명의 클라이언트의 일을 시간을 나눠 처리한다. 클라이언트 1000명이 동시에 1ms 쿼리를 던지면, 평균적으로 한 backend가 10번씩 일하면 끝난다. 클라이언트 입장에서 보면 거의 즉시 응답이 온다. PG 입장에서는 100 커넥션의 부하만 받는다. 양쪽이 다 이기는 구조다.

이 magic이 왜 가능할까? 대부분의 OLTP 쿼리가 ms 단위로 끝나기 때문이다. 한 backend가 1초에 1000개의 쿼리를 처리할 수 있으면, 1000명의 클라이언트가 평균 1초 간격으로 쿼리를 보내도 backend 하나로 충분하다. 시간이 *희소 자원이 아니라 충분 자원*이라 multiplexing이 통한다.

물론 모든 쿼리가 ms 단위는 아니다. 분석 쿼리가 30초 걸리면, 그 30초 동안 backend 하나가 잡혀 있다. 다른 클라이언트들은 풀에서 대기한다. 그래서 OLTP와 분석을 같은 PG에 섞으면 풀러의 효율이 떨어진다 — 분석은 별도 read replica로 보내거나 별도 풀러 instance를 두는 식으로 분리하는 편이 낫다.

여기까지 알면 충분하다. "그래서 어떤 풀러를 어떤 모드로 어떤 함정을 피해서 쓸 것인가"는 21장에서 본다.

### 다음 장으로 — 한 번 더 fork를 보자

여기까지 4장의 길을 같이 따라왔다. postmaster의 fork, 백그라운드 프로세스 풀세트, shared_buffers와 work_mem의 메모리 모델, max_connections의 함정, 그리고 풀러의 당위성까지.

이 모든 이야기의 시작은 한 줄이었다. **PostgreSQL은 커넥션마다 OS 프로세스를 fork한다.** 이 한 줄에서 메모리 모델이 나오고, 백그라운드 프로세스 구성이 나오고, max_connections의 위험이 나오고, 풀러의 필수성이 나왔다. 1986년 버클리에서 내린 한 가지 설계 결정이, 2026년 운영자의 한밤중 호출까지 그대로 이어진다. 설계 결정의 무게가 어디까지 가는지를 보여주는 한 예다.

이 무게는 5장에서 한 번 더 우리를 기다린다. 5장의 주제는 PG의 또 다른 정체성, MVCC와 VACUUM이다. PG의 MVCC는 같은 테이블에 새 row를 그냥 추가한다 — InnoDB와는 전혀 다른 길을 택했다. 그 결정 하나가 dead tuple, table bloat, index amplification이라는 새로운 운영 비용을 만들고, 그것이 다시 VACUUM이라는 운명적인 짝을 데리고 온다. fork가 메모리 모델을 결정했듯, append-only MVCC는 운영의 무게 자체를 결정한다.

두 결정 모두 1980년대에 내려졌다. 우리는 2026년에 그 결정의 결과를 받아 살아간다. 그 결과를 이해하지 않고 PG를 메인 DB로 쓴다는 건 — 무거운 짐을 들면서 손잡이가 어디에 있는지 모르는 일과 같다. 5장에서 손잡이를 같이 찾아보자.

기억해두자. **PG에서 커넥션은 비싸다. 그 비용을 풀러로 묶는 것이 운영의 출발선이다.** 풀러는 옵션이 아니라 전제다.
