# 19장. 백업·복구·PITR — pgBackRest·Barman·WAL-G

백업이 있다고 안심하던 팀이 막상 복구를 시도하다 손이 멈춘 적이 있다. 디스크가 깨졌다는 알람 한 통, S3 콘솔에 가지런히 쌓여 있는 어제 자 백업 파일, 그리고 `pg_restore`를 두드리는 순간 — 그제야 알게 되는 사실이 하나 있다. "백업이 있다"는 명제와 "복구가 된다"는 명제는 결코 같은 명제가 아니라는 것이다.

같은 일이라고 믿고 싶은 마음은 이해한다. 백업 잡이 매일 밤 성공으로 끝나고, 디스크 사용량 그래프가 차곡차곡 늘어나고, 모니터링 대시보드는 초록색이다. 그런데 그 초록색이 보증하는 것은 "파일이 쓰였다"는 사실까지다. 그 파일이 실제로 일관된 상태인지, 그 파일로부터 어제 오후 3시 47분의 데이터까지 정확히 되돌아갈 수 있는지, 그 복구가 우리 RTO 안에 끝날 수 있는지 — 이런 질문들에는 따로 답해야 한다.

이번 장에서 함께 살펴볼 도구들은 그 둘을 같은 일로 만들어주는 도구들이다. pgBackRest, Barman, WAL-G 셋이 사실상의 후보다. 어떤 도구를 고르든 결국 우리가 마주해야 하는 질문은 두 가지로 좁혀진다 — 사고가 났을 때 어느 시점까지 되돌릴 수 있는가, 그리고 그 되돌리기가 실제로 작동한다는 것을 어떻게 증명할 것인가. 차근차근 이야기해보자.

## 19.1 pg_basebackup — 내장의 한계

가장 정직한 출발점은 PostgreSQL이 박스에 담아 보내주는 도구다. `pg_basebackup`. 이름 그대로 "베이스 백업"을 만들어주는 명령으로, 추가 설치 없이 즉시 쓸 수 있다. 명령 한 줄이면 클러스터 전체의 물리적 사본이 하나 생긴다.

```bash
pg_basebackup -h primary.db -U replicator -D /backups/base \
  -X stream -P -R
```

`-X stream` 옵션은 백업이 진행되는 동안 발생한 WAL을 함께 받아 두라는 지시다. 이것이 빠지면 백업이 끝난 시점에 데이터가 일관된 상태로 복원될 수 없다. `-R`은 standby용 설정 파일을 함께 생성해주는 옵션. 새로운 standby 서버를 띄울 때 유용하다.

여기까지만 보면 "굳이 외부 도구가 왜 필요한가" 하는 의문이 들 수도 있다. 그런데 운영 규모가 어느 선을 넘으면, `pg_basebackup`의 단순함은 곧 한계가 된다. 다음 세 가지가 결정적이다.

**첫째, 항상 전체를 통째로 받는다.** 증분 백업도, 차등 백업도 없다. 100GB 데이터베이스라면 매일 100GB를 새로 만들어 어딘가에 쌓아야 한다는 뜻이다. 1TB가 되면 그 부담은 단순히 열 배가 아니다. 디스크 I/O가 운영 시스템에 미치는 영향, 네트워크 대역폭, 보존 정책에 따른 스토리지 비용 — 모든 게 선형보다 가파르게 늘어난다. 멀티 TB 데이터베이스에서 `pg_basebackup`만으로 운영하려 들면 정말 난감해진다.

**둘째, 백업 자체에 대한 운영성이 비어 있다.** 보존 기간 관리, 백업 카탈로그, 무결성 검증, 압축·암호화, 병렬 처리 — 이 모든 것을 손으로 구현해야 한다. 매일 새벽 3시에 도는 cron 스크립트가 한 줄 한 줄 늘어나고, 두 달쯤 지나면 그 스크립트가 클러스터의 또 다른 SPoF가 되어 있다. 끔찍한 일이다.

**셋째, PITR 운영성이 약하다.** PITR(Point-in-Time Recovery, 시점 복구)은 베이스 백업 하나와 그 이후의 WAL 아카이브를 합쳐서 만들어진다. `pg_basebackup`은 베이스 백업까지는 해주지만, WAL 아카이브의 안전한 보관·관리·검색은 별도다. `archive_command`를 직접 짜고, 보존 정책을 직접 관리하고, 복구 시 필요한 WAL을 직접 찾아내야 한다. 사고가 난 새벽 두 시에 이 작업을 처음 해본다고 상상해보자. 손이 떨릴 수밖에 없다.

그렇다면 `pg_basebackup`을 아예 쓰지 말라는 이야기일까? 그렇지는 않다. 단일 노드 소규모 클러스터, 개발용 환경의 빠른 사본 만들기, 새 standby를 빠르게 부트스트랩할 때 — 이런 용도에서는 여전히 가장 빠르고 정직한 도구다. 내장이라는 사실 자체가 큰 안심이기도 하다. 외부 도구의 메이저 업그레이드가 망가뜨릴 가능성도 없고, 매니지드 PG가 빌트인으로 제공하는 base backup 기능과 같은 프로토콜 위에서 돈다는 점도 마음에 안정감을 준다. 다만 "프로덕션 백업 도구"로 끌어다 쓰려고 하면 곧 한계에 부딪힌다는 점만 기억해두자. 외부 도구 셋이 결국 모두 `pg_basebackup` 프로토콜이나 그에 준하는 방식 위에 운영성을 얹은 것이라는 사실도 — 내장의 가치를 다시 보게 만든다.

이 한계를 출발점으로 삼아, 그 위에 운영성을 얹은 외부 도구 셋을 차례로 살펴보자.

## 19.2 pgBackRest — 사실상 표준

PostgreSQL 백업 도구를 골라야 할 때, 특별한 사정이 없다면 첫 후보는 pgBackRest다. 이건 어떤 마케팅 문구가 아니라 운영 커뮤니티의 사실상 합의다. Crunchy Data가 메인테이닝하고, Christophe Pettus 같은 PG 베테랑들이 운영 가이드를 쓰고 있으며, 멀티 TB 데이터베이스 사례가 가장 풍부한 도구이기도 하다.

pgBackRest가 잘 하는 일을 풀어 적으면 다음과 같다.

- **세 가지 백업 유형 지원** — full, diff, incremental. 매주 한 번 full, 매일 diff, 매시간 incremental 같은 조합이 가능해진다. 100GB짜리 클러스터라면 매일 100GB가 아니라 평균 10GB 미만의 증분만 쌓이도록 설계할 수 있다.
- **병렬 처리** — 백업·복원 모두 여러 프로세스로 동시에 진행된다. `process-max=8` 같은 설정 하나로 멀티 TB 백업을 몇 시간 단위로 끝낼 수 있다.
- **압축·암호화·체크섬** — 백업 파일에 대한 압축(gz, lz4, zst), AES-256 암호화, SHA1/SHA-256 체크섬을 기본 기능으로 제공한다. 별도 스크립트가 필요 없다.
- **S3·Azure·GCS·로컬·SFTP** — repo 타입을 골라 쓸 수 있고, 여러 repo를 동시에 운영하는 것도 가능하다. 로컬에 한 부, 원격 오브젝트 스토리지에 한 부 — 이런 다중 repo 패턴이 자연스럽다.
- **PITR 일등 시민** — 복구 명령에 `--type=time --target='2026-05-17 14:23:00'` 한 줄을 붙이면 그 시점으로 되돌아간다. 필요한 WAL을 알아서 끌어와 적용한다.

설정 파일 하나로 이 모든 게 묶인다. `/etc/pgbackrest/pgbackrest.conf`의 모습을 살펴보자.

```ini
[global]
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
repo1-retention-diff=7
repo1-cipher-type=aes-256-cbc
repo1-cipher-pass=<long-random-passphrase>

repo2-type=s3
repo2-s3-bucket=our-pg-backups
repo2-s3-endpoint=s3.ap-northeast-2.amazonaws.com
repo2-s3-region=ap-northeast-2
repo2-retention-full=14

process-max=8
log-level-console=info
log-level-file=detail
compress-type=zst
compress-level=3
start-fast=y

[main]
pg1-path=/var/lib/postgresql/17/main
pg1-port=5432
```

`[main]`은 백업 대상 클러스터의 stanza(스탠자, 인스턴스 이름)다. 같은 백업 서버가 여러 클러스터를 백업한다면 stanza를 더 추가하면 된다. repo가 두 개 잡혀 있는 것에 주목하자 — 로컬과 S3로 동시에 보관한다. 한쪽이 망가져도 다른 쪽이 살아 있도록 하는 가장 단순한 보험이다.

PG 쪽 설정도 짚고 가자. `postgresql.conf`에 다음을 박아둔다.

```ini
archive_mode = on
archive_command = 'pgbackrest --stanza=main archive-push %p'
archive_timeout = 60
wal_level = replica   # logical replication을 같이 쓴다면 logical
max_wal_senders = 10
```

`archive_command`가 pgBackRest의 `archive-push`를 호출하도록 잡아두면, PG가 만들어내는 모든 WAL 세그먼트가 자동으로 repo에 차곡차곡 쌓인다. `archive_timeout = 60`은 트래픽이 적은 시간대에도 1분에 한 번씩은 WAL을 강제로 닫아 보낸다는 뜻이다. PITR의 복구 가능 최소 시점 단위를 그만큼 촘촘하게 만들어준다.

이제 운영 명령 몇 가지를 차례로 보자.

```bash
# 스탠자 초기화 (한 번만)
pgbackrest --stanza=main stanza-create

# 첫 full 백업
pgbackrest --stanza=main --type=full backup

# 평소: incremental
pgbackrest --stanza=main --type=incr backup

# 무결성 검증
pgbackrest --stanza=main check
pgbackrest --stanza=main verify

# 백업 목록·메타데이터 확인
pgbackrest --stanza=main info
```

`info` 명령의 출력은 운영 중 가장 자주 들여다보게 되는 화면이다. 각 백업의 시각, 크기, 압축 크기, WAL 범위, 보존 정책에 따른 만료 일자가 한 번에 보인다. 사고가 났을 때 가장 먼저 두드리게 되는 명령이기도 하다.

복원 쪽을 살펴보자. 가장 단순한 케이스는 "최신 백업으로 빈 디렉터리에 복원"이다.

```bash
systemctl stop postgresql
rm -rf /var/lib/postgresql/17/main/*
pgbackrest --stanza=main --delta restore
systemctl start postgresql
```

`--delta` 옵션은 디렉터리에 이미 있는 파일들과 백업의 파일을 비교해 다른 것만 가져온다는 뜻이다. 멀티 TB 클러스터를 통째로 다시 받는 게 아니라 차이만 받게 되니, 부분 손상 복구가 굉장히 빨라진다.

PITR 시나리오는 19.5절에서 본격적으로 다루겠지만, 명령의 모양만 미리 보면 다음과 같다.

```bash
pgbackrest --stanza=main --type=time \
  --target='2026-05-17 14:23:00+09' \
  --target-action=promote restore
```

`--target-action=promote`은 복구가 완료된 직후 클러스터를 즉시 read/write 가능한 상태로 끌어올린다. `--target-action=pause`로 두면 복구만 멈춰서 사람이 한 번 더 확인할 기회를 준다. 운영자 취향과 절차에 따라 고르면 된다.

pgBackRest를 쓰면서 자주 부딪히는 함정이 두 가지 있다.

**첫째, repo 디스크 용량 산정.** 압축 후 크기를 기준으로 산정해야 한다. zstd 압축이면 평균 3~5배의 절약을 보지만, 이미 압축된 JPEG·BLOB이 많은 워크로드라면 압축률이 낮다. "원본 DB 크기의 30%만 있으면 된다"는 식의 일반화는 위험하다. 최소 한 주는 직접 측정해보고 정책을 짜는 편이 낫다.

**둘째, archive-push 실패의 누적.** `archive_command`가 한 번 실패하면 그 WAL이 `pg_wal` 디렉터리에 그대로 남는다. 실패가 누적되면 디스크가 빠르게 차오르고, 결국 PG 자체가 멈춘다. 이걸 모니터링하지 않으면 "백업이 실패하고 있다는 사실"이 디스크 풀 사고로 번져서야 발견되는 일이 생긴다. 끔찍한 일이다. `pg_stat_archiver`의 `last_failed_wal`, `last_failed_time`은 반드시 모니터링 대상에 넣어두자.

```sql
-- 매분 실행해서 알람으로 연결할 만한 쿼리
SELECT
  archived_count,
  last_archived_wal,
  last_archived_time,
  failed_count,
  last_failed_wal,
  last_failed_time,
  now() - last_archived_time AS time_since_last_archive
FROM pg_stat_archiver;
```

`time_since_last_archive`가 평소 archive_timeout의 두 배를 넘기면 빨간불, 다섯 배를 넘기면 즉시 호출 — 정도의 기준이 무난하다.

여기에 한 단계 더 욕심을 내자면, **async archive-push와 archive-async-queue**를 켜두는 편이 낫다. PG의 `archive_command`는 본래 동기적이라, 백업 repo의 응답이 한 번 늦어지면 다음 WAL을 보낼 때까지 PG가 기다린다. pgBackRest의 비동기 모드는 archive 큐를 별도 디렉터리에 두고 백그라운드로 전송한다. 트래픽이 폭주하는 시간대에 archive가 병목이 되지 않도록 막아주는 가장 단순한 안전장치다.

```ini
# pgbackrest.conf [global]
archive-async=y
archive-push-queue-max=4GiB
spool-path=/var/spool/pgbackrest
```

`archive-push-queue-max`는 spool 디렉터리가 이 크기를 넘으면 그제야 PG에 백프레셔를 돌려준다는 의미다. 4GiB 정도는 평균 트래픽으로 1~2시간의 안전 마진이 된다.

**무결성 검증**도 짚어두자. `pgbackrest verify` 명령은 repo에 있는 백업과 WAL의 체크섬을 처음부터 끝까지 검사한다. 백업이 만들어진 직후의 체크섬과 한 달 뒤의 체크섬을 비교해서, 그 사이 어디선가 비트가 부패하지 않았는지 확인한다. 오브젝트 스토리지가 자체 무결성을 보장한다고 해도 — repo가 끝없이 자라는 환경에서는 정기적인 verify가 한 번씩 안 좋은 소식을 일찍 알려준다. 일주일에 한 번 verify를 도는 cron 잡 하나는 깔아두는 편이 안심이 된다.

**암호화 키 관리**는 한 번 짚고 가야 한다. 위 conf의 `repo1-cipher-pass`는 평문 passphrase다. 이 값이 한 번 노출되면 백업 전체가 노출된 셈이다. 평문으로 conf 파일에 박아두기보다, KMS·Vault·AWS Secrets Manager 같은 시크릿 스토어에서 부팅 시점에 주입하는 방식이 안전하다. 그리고 그 시크릿 자체의 rotate 정책도 따로 갖춰두자. "백업은 잘 되어 있는데 키를 잃어서 복구가 안 된다" — 정말 끔찍한 일이다.

pgBackRest는 학습 곡선이 약간 있는 도구다. 처음 며칠은 conf 파일을 만지고, stanza라는 용어에 익숙해지고, repo 구조를 이해하는 시간이 필요하다. 그런데 그 며칠을 지나면 — 그 이후의 운영은 한결 편안해진다. 사실상 표준이라는 위치가 그저 인기 때문에 만들어진 것은 아니다.

## 19.3 Barman — EDB, 멀티 서버 중앙관리

pgBackRest의 모델이 "각 PG 클러스터마다 백업 도구를 띄운다"라면, Barman의 모델은 다르다. Barman은 "한 대의 백업 서버가 여러 PG 클러스터를 중앙에서 백업·관리한다"는 모델을 따른다. EDB(EnterpriseDB)가 만들고 유지해온 도구로, 엔터프라이즈 환경에서의 운영 친화성이 특히 두드러진다.

언제 Barman을 고르는 게 자연스러울까? 다음과 같은 상황을 떠올려보자.

- 10여 개 이상의 PG 클러스터를 한 팀에서 관리하고 있다
- 각 DB 호스트의 디스크·CPU를 백업 작업이 더 잡아먹지 않았으면 한다
- 백업 정책·보존·모니터링을 한 곳에서 통일된 방식으로 보고 싶다
- DR 사이트에 별도의 백업 호스트를 두는 것이 조직 표준이다

이런 상황이라면 클러스터마다 따로 도구를 깔고 관리하는 것보다 백업 전용 호스트 한 대(혹은 DR용 두 대)를 두는 편이 훨씬 깔끔하다. Barman의 자리가 바로 여기다.

설정의 큰 그림은 이렇다. Barman 서버에서 각 PG 클러스터로 SSH 또는 streaming replication 연결을 맺어둔다. 백업은 두 가지 모드 중 하나를 고른다.

- **rsync/SSH 모드** — 전통적인 방식. SSH로 PG 데이터 디렉터리를 직접 끌어온다. 증분 백업은 hardlink 기반.
- **streaming 모드** — `pg_basebackup` 프로토콜과 WAL streaming을 활용. SSH 없이 PG 프로토콜만으로 끝낸다. 더 모던한 선택지.

`/etc/barman.conf`의 글로벌 설정과 클러스터별 conf의 모습을 살펴보자.

```ini
# /etc/barman.conf
[barman]
barman_user = barman
configuration_files_directory = /etc/barman.d
barman_home = /var/lib/barman
log_file = /var/log/barman/barman.log
compression = gzip
retention_policy = RECOVERY WINDOW OF 30 DAYS
parallel_jobs = 4
```

```ini
# /etc/barman.d/main.conf
[main]
description = "Primary production cluster"
conninfo = host=primary.db user=barman dbname=postgres
streaming_conninfo = host=primary.db user=streaming_barman
backup_method = postgres
streaming_archiver = on
slot_name = barman
create_slot = auto
archiver = off
```

`retention_policy = RECOVERY WINDOW OF 30 DAYS`는 "지난 30일 중 어느 시점으로든 복구할 수 있도록 백업과 WAL을 자동으로 유지하라"는 정책이다. 단순한 기간 보존이 아니라 PITR 가능 시점 윈도우 단위로 정책을 표현할 수 있다는 점 — 이게 Barman의 매력 중 하나다.

운영 명령은 직관적이다.

```bash
# 모든 클러스터 상태 점검
barman check all

# 특정 클러스터 백업
barman backup main

# 백업 목록
barman list-backup main

# 복원 (Barman 서버 → 목적지 호스트로)
barman recover \
  --remote-ssh-command "ssh postgres@new-primary" \
  --target-time "2026-05-17 14:23:00" \
  main latest /var/lib/postgresql/17/main
```

`barman recover`에 `--remote-ssh-command`를 함께 넘기면, 복원 결과를 Barman 서버가 아니라 지정한 원격 호스트의 데이터 디렉터리로 직접 풀어낸다. 새 standby를 부트스트랩하거나 복구된 클러스터를 새 호스트에 띄울 때 편하다.

Barman은 S3, Azure Blob, GCS를 cloud backup용 보조 백엔드로 지원한다. 로컬 디스크에 1차 백업을 두고, geo-redundant 사본을 클라우드 오브젝트 스토리지에 비동기로 복제하는 패턴이 흔하다. EDB 진영의 hook 스크립트 생태계가 풍부해서, 백업 전후 처리나 알람 연결도 비교적 깔끔하게 붙는다.

그렇다면 단점은 무엇일까? 실무에서 자주 언급되는 두 가지를 짚어두자.

**첫째, 멀티 TB·고동시성 워크로드에서 pgBackRest 대비 성능 한계가 보고된 사례들이 있다.** Severalnines의 pgBackRest vs Barman 비교 자료가 대표적이다. 병렬 처리 모델이 다르고, hardlink 기반 증분의 한계가 어느 임계를 넘으면 드러난다. 단일 클러스터가 수십 TB를 넘는다면 pgBackRest가 더 안전한 선택일 수 있다.

**둘째, "백업 서버 한 대"라는 모델 자체가 그 백업 서버를 새로운 운영 대상으로 만든다.** Barman 호스트가 죽으면 백업이 멈춘다. 그래서 DR 사이트에 보조 Barman을 두거나, Barman 자체에 대한 HA를 별도로 설계해야 한다. 도구 하나가 작은 운영 시스템이 된다는 사실을 잊지 말자.

그럼에도 "여러 클러스터를 한 자리에서" 관리하는 가치는 작지 않다. 특히 사내 표준화가 중요한 조직, 백업 운영을 DB 호스트와 분리하고 싶은 조직, EDB 생태계와의 연계가 자연스러운 조직이라면 — Barman은 여전히 강력한 선택이다.

## 19.4 WAL-G — 클라우드 네이티브

도구의 출생지를 알면 그 도구의 성격이 보인다. WAL-G는 Yandex가 만들었고, Go로 짜였고, 처음부터 오브젝트 스토리지를 1급 시민으로 가정하고 설계됐다. pgBackRest와 Barman이 "전통적 운영 서버" 위에서의 백업을 가장 잘 한다면, WAL-G는 "S3·GCS·Azure Blob·Swift 위에서의 백업"을 가장 가볍게 해낸다.

WAL-G가 잘 하는 일을 추려보면 이렇다.

- **순수 클라우드 네이티브** — S3·GCS·Azure Blob을 백엔드로 보고 그 위에서의 동작을 최적화. CRC 검증, 멀티파트 업로드, 재시도 정책이 단단하다.
- **병렬 backup·restore** — 환경 변수 `WALG_UPLOAD_CONCURRENCY`, `WALG_DOWNLOAD_CONCURRENCY` 등으로 조절. delta backup 지원.
- **Go 단일 바이너리** — 배포가 단순하다. 컨테이너·이뮤터블 호스트와 잘 어울린다.
- **델타 백업** — 이전 백업과 변경된 페이지만 보내는 모드를 지원. 객체 스토리지의 PUT 비용을 줄이는 데 도움이 된다.
- **PG 외에 MySQL·MS SQL Server·MongoDB·Redis까지** — 한 회사에서 여러 DB를 같은 도구로 백업하고 싶다는 요구를 일부 충족한다.

설정은 거의 환경 변수로 다 된다. 컨테이너 친화적이라는 인상을 받게 되는 이유다.

```bash
export WALG_S3_PREFIX="s3://our-pg-backups/cluster-main"
export AWS_REGION="ap-northeast-2"
export WALG_COMPRESSION_METHOD="brotli"
export WALG_DELTA_MAX_STEPS=7
export WALG_UPLOAD_CONCURRENCY=16
export WALG_DOWNLOAD_CONCURRENCY=16
```

`postgresql.conf`의 `archive_command`는 다음 한 줄로 끝난다.

```ini
archive_command = '/usr/local/bin/wal-g wal-push %p'
```

백업과 복원도 한 줄짜리 명령이다.

```bash
# full backup
wal-g backup-push /var/lib/postgresql/17/main

# 백업 목록
wal-g backup-list

# 가장 최근 백업으로 복원
wal-g backup-fetch /var/lib/postgresql/17/main LATEST
```

복원 직후 PG에 `recovery.signal` 파일을 두고 시작하면 PITR이 진행된다. `restore_command`는 다음과 같은 형태다.

```ini
restore_command = '/usr/local/bin/wal-g wal-fetch %f %p'
recovery_target_time = '2026-05-17 14:23:00+09'
recovery_target_action = 'promote'
```

WAL-G의 매력은 단순함과 클라우드 친화성이다. 컨테이너 기반 환경, Kubernetes 위의 PG, 짧은 수명의 인스턴스를 자주 띄우고 내리는 환경에서 특히 잘 어울린다. 백업 서버라는 별도 인프라가 사실상 필요 없다 — PG 호스트와 오브젝트 스토리지만 있으면 끝난다.

물론 단점도 있다. 엔터프라이즈에서 기대하는 일부 기능 — 정교한 보존 정책의 표현력, GUI 대시보드, 다양한 hook 인터페이스, 트랜잭션 일관성 보장에 대한 세밀한 옵션 — 에서 pgBackRest나 Barman만큼 풍부하지는 않다. 또한 도구 자체의 운영 사례 풍부도, 한국어 문서 풍부도가 pgBackRest 쪽이 더 두텁다는 점도 솔직히 인정해야 한다.

WAL-G의 운영에서 자주 부딪히는 함정 하나만 짚어두자. **오브젝트 스토리지의 latency가 곧 PITR의 RTO에 그대로 박힌다.** 베이스 백업과 수만 개의 WAL 세그먼트를 S3에서 받아 내리는 시간이 복구 시간의 대부분을 차지하기 때문이다. 같은 리전 안에서의 S3 다운로드는 충분히 빠르지만, 다른 리전·다른 클라우드에서 받아내려야 하는 시나리오라면 — `WALG_DOWNLOAD_CONCURRENCY`를 충분히 크게 잡고, 가능하다면 베이스 백업의 사본 한 부를 가까운 곳에 두는 식의 설계가 필요하다.

또 하나, **delta backup의 보존 정책**도 신경을 써야 한다. delta는 이전 백업에 의존하기 때문에, 의존 사슬 중간의 백업이 만료되면 그 이후 delta들이 함께 무용지물이 된다. `WALG_DELTA_MAX_STEPS`로 사슬 깊이를 제한하는 게 사실상 필수다. 7~10 정도가 흔한 값. 사슬이 너무 길어지면 복원 시점에 많은 단계를 거슬러 올라가야 해서 RTO가 길어진다.

선택의 가이드라인을 한 줄로 정리하면 이렇다. **PITR이 절대로 필요한 프로덕션의 첫 선택은 pgBackRest, 여러 클러스터의 중앙 관리가 가치 있다면 Barman, 클라우드 네이티브·컨테이너 환경의 가벼움이 우선이라면 WAL-G.** 셋 다 production에서 검증된 도구이고, 어느 하나가 "잘못된 선택"인 경우는 거의 없다. 조직의 운영 체질에 맞는 한 가지를 골라 깊이 익히는 편이 — 여러 도구를 얕게 다루는 것보다 훨씬 안전하다.

세 도구의 비교를 한 표로 정리하면 다음과 같다. 결정의 첫 그림으로 삼을 만하다.

| 항목 | pgBackRest | Barman | WAL-G |
|---|---|---|---|
| 출생·메인테이너 | Crunchy Data 중심, C | EDB, Python | Yandex 출발, Go |
| 백업 모델 | 각 PG 호스트에 도구 | 중앙 백업 호스트 | 각 PG 호스트, 오브젝트 스토리지 직행 |
| full/diff/incr | 셋 다 | full + rsync 기반 증분 | full + delta |
| 멀티 TB 운영 사례 | 가장 풍부 | 풍부 | 적당 |
| 오브젝트 스토리지 | 보조 repo | 보조 cloud backup | 1차 시민 |
| 학습 곡선 | 중 | 중 | 낮음 |
| 컨테이너·K8s 친화 | 가능, 약간의 설정 | 약간 어색 | 매우 좋음 |
| 한국어 자료 | 풍부 | 적당 | 적음 |
| 첫 선택 추천 상황 | 멀티 TB OLTP, PITR 필수 | 다수 클러스터 중앙관리 | 컨테이너·서버리스·이뮤터블 호스트 |

## 19.5 PITR 시나리오 — 사고 시각 1분 전으로 되돌리기

도구의 설치와 conf 파일은 머리로 익혀두면 되는 일이다. 진짜 시험은 사고가 났을 때 일어난다. PITR(Point-in-Time Recovery, 시점 복구)이 그 시험의 이름이다.

상황을 가정해보자. 오후 2시 23분, 운영자가 한 줄의 SQL을 실행했다.

```sql
DELETE FROM orders WHERE created_at < '2026-05-01';
```

원래 의도는 검토용으로 만든 임시 테이블의 정리였다. 그런데 `search_path`가 잘못 잡혀 있었고, 운영 `orders` 테이블에 명령이 떨어졌다. 270만 행이 사라졌다. 2시 24분, 모니터링이 비명을 지른다. 2시 25분, 운영자가 사색이 된다.

이 시점에서 우리가 가진 가장 큰 무기가 PITR이다. 사고 직전 — 가령 2시 22분 59초 — 의 상태로 클러스터를 되돌릴 수 있다면, 그 사이 1분의 트래픽은 잃지만 270만 행은 살아 돌아온다. 이 차이가 회사의 하루를 바꾼다.

PITR의 원리를 한 문장으로 요약하면 이렇다. **베이스 백업 한 개와 그 시점 이후의 모든 WAL이 있으면, 그 사이의 어떤 시각·트랜잭션·LSN으로든 클러스터를 되돌릴 수 있다.** 베이스 백업은 출발점이고, WAL은 출발점에서 목표 시점까지의 길이다. 길이 끊겨 있으면 — 그러니까 WAL 아카이브가 빠짐없이 보존되어 있지 않으면 — PITR은 그 끊긴 지점까지밖에 가지 못한다.

복구 목표를 지정하는 방법은 네 가지다.

- `recovery_target_time` — 특정 시각으로. 가장 직관적.
- `recovery_target_xid` — 특정 트랜잭션 ID로. 사고 트랜잭션을 정확히 짚어낼 수 있을 때.
- `recovery_target_lsn` — 특정 LSN으로. WAL 분석으로 정확한 위치를 알아냈을 때.
- `recovery_target_name` — `pg_create_restore_point()`로 미리 박아둔 명명된 지점으로. 마이그레이션 직전 같은 의도적 체크포인트.

가장 흔하게 쓰이는 건 시간이다. 사고 시각 1분 전을 목표로 잡아보자.

```ini
# postgresql.auto.conf 또는 recovery 설정
restore_command = 'pgbackrest --stanza=main archive-get %f "%p"'
recovery_target_time = '2026-05-17 14:22:59+09'
recovery_target_action = 'pause'
recovery_target_inclusive = false
```

`recovery_target_inclusive = false`는 "지정 시각의 트랜잭션은 포함하지 않는다"는 뜻이다. 사고를 일으킨 트랜잭션이 목표 시각에 걸쳐 있을 가능성이 있을 때 안전한 선택.

`recovery_target_action`의 세 가지 값은 짚어둘 만하다.

- `pause` — 목표에 도달하면 멈추고 read-only로 대기. 운영자가 데이터 검증 후 `pg_wal_replay_resume()` 또는 `pg_promote()`로 결정.
- `promote` — 도달 즉시 read/write 가능 상태로 승격. 자동화에 적합.
- `shutdown` — 도달 후 셧다운. 가장 보수적이지만 검증 자동화를 따로 짜야 한다.

사고 대응의 정석은 `pause`다. 일단 멈춰서, 우리가 의도한 시점이 정말 맞는지 — 270만 행이 그대로 있는지, 다른 정상 트랜잭션이 잘리지 않았는지 — 사람의 눈으로 한 번 확인하고, 그 다음에 승격한다. 자동화는 일상 백업 검증 같은 다른 자리에서 빛난다.

pgBackRest로 위 시나리오를 수행하는 전체 흐름은 이렇다.

```bash
# 1. 사고 난 PG 멈춤 (혹은 별도 호스트에 복구)
systemctl stop postgresql

# 2. 데이터 디렉터리 비움 (또는 별도 디렉터리 준비)
mv /var/lib/postgresql/17/main /var/lib/postgresql/17/main.broken

# 3. PITR 복구 시작
pgbackrest --stanza=main \
  --type=time \
  --target='2026-05-17 14:22:59+09' \
  --target-action=pause \
  --delta restore

# 4. PG 시작 — pause 모드로 들어옴
systemctl start postgresql

# 5. 운영자 검증
psql -c "SELECT count(*) FROM orders WHERE created_at < '2026-05-01';"
# 270만 행이 돌아왔는지 확인

# 6. 만족스러우면 승격
psql -c "SELECT pg_promote();"
```

여기서 짚어야 할 운영적 함정이 두 가지 있다.

**첫째, PITR은 원본 클러스터를 덮어쓰지 말고 별도 호스트·별도 디렉터리에서 진행하는 편이 낫다.** 사고 원인이 정확히 무엇이었는지 분석할 단서가 원본에 남아 있을 수 있다. "복구 → 분석 → 데이터 일부만 이전" 패턴이 안전하다. 270만 행 중 250만 행만 가져오고 나머지는 사고 후 트랜잭션이라 그대로 두는 — 그런 정교한 처리도 가능해진다.

**둘째, 사고 발생 후 timeline 분기가 생긴다는 점.** 복구 후 새로운 클러스터를 promote 하면, PG는 그 시점부터 새로운 timeline ID로 WAL을 쓰기 시작한다. timeline 1 → timeline 2로 갈라지는 것이다. 그 후의 백업은 새로운 timeline에 묶이고, 이전 timeline의 WAL과 섞이지 않도록 정리해야 한다. pgBackRest는 이 정리를 자동으로 처리하지만 — 동작 원리를 이해하고 있어야 사고 후 백업 카탈로그를 읽을 때 헷갈리지 않는다.

LSN 기반 복구도 한 번 짚어두자. WAL 분석으로 정확한 위치를 찾았다면 — 가령 `pg_waldump`로 사고 SQL의 직전 LSN을 알아냈다면 — 그 LSN을 목표로 삼을 수 있다.

```ini
recovery_target_lsn = '1/A2C5B000'
recovery_target_action = 'pause'
recovery_target_inclusive = false
```

LSN 기반은 시간 기반보다 정밀하다. 트랜잭션 단위까지 정확히 잘라낼 수 있다. 다만 LSN을 사람이 직관적으로 알기는 어렵다 — 이걸 알아내는 과정 자체가 WAL 분석이라는 별도 기술을 요구한다. 평소엔 시간 기반으로 충분하고, 시간 기반으로는 정밀도가 모자란 사고에서만 LSN 기반으로 한 단계 더 내려간다고 생각해두자.

또 하나, **명명된 복구 지점**(named restore point)도 운영의 안전망으로 잘 어울린다. 위험한 마이그레이션 직전, 대형 배포 직전, 또는 일괄 데이터 보정 작업 직전 같은 의도적 분기점에 이름표를 박아두자.

```sql
SELECT pg_create_restore_point('before_v18_upgrade_2026_05_17');
```

이 함수는 WAL 안에 이름표 하나를 끼워 넣는다. 만약 마이그레이션이 실패해서 되돌려야 한다면 — 시각을 정확히 기억할 필요 없이, 이름표를 목표로 잡으면 된다.

```ini
recovery_target_name = 'before_v18_upgrade_2026_05_17'
recovery_target_action = 'pause'
```

마이그레이션·대형 배포·DDL 일괄 실행 같은 위험한 변경의 직전에 이 한 줄을 박는 습관은 비용이 거의 0이고, 사고 시 가치가 엄청나다. "그때로 돌아가고 싶은데 정확한 시각을 모르겠다"는 상황을 원천적으로 막아주기 때문이다.

PITR은 "할 수 있다"와 "실제로 한다"가 가장 멀리 떨어진 영역이기도 하다. 도구는 있고, 명령은 알고, 그런데 사고 새벽 두 시에 처음 두드린다면 손이 안 움직인다. 그래서 다음 절이 필요하다.

## 19.6 백업 검증 — "백업이 있다"와 "복구된다"는 다른 일

이 장의 첫 문장으로 돌아가보자. 백업이 있다고 안심하던 팀이 막상 복구를 시도하다 손이 멈췄다. 왜 그런 일이 일어날까? 원인은 거의 항상 같다. **복구를 실제로 해본 적이 없거나, 마지막 시도가 너무 오래전이거나, 시도해본 사람이 지금 휴가 중이거나** — 셋 중 하나다.

이 문제를 푸는 방법도 거의 정해져 있다. **복구를 일상의 일로 만드는 것.** 사고가 났을 때만 하는 일이 아니라, 매일 또는 매주 자동으로 도는 검증 파이프라인의 일부로 만드는 것이다. 어떻게 하면 될까?

가장 단순한 형태는 다음과 같다.

1. 매일 밤 백업이 끝나면, 별도 검증 호스트(VM·컨테이너·DR 사이트의 유휴 노드)에서 복구 잡을 시작한다.
2. 가장 최근 백업으로 빈 디렉터리에 복원한다.
3. PG를 띄우고 미리 정해둔 검증 쿼리들을 돌린다.
4. 결과를 알람·대시보드·Slack에 보낸다.
5. 검증이 끝나면 디렉터리를 비운다.

검증 쿼리는 거창할 필요 없다. 다음 정도면 시작점으로 충분하다.

```sql
-- 1) 클러스터가 살아 있다
SELECT version();
SELECT pg_is_in_recovery();

-- 2) 최신 LSN이 합리적이다
SELECT pg_last_wal_replay_lsn();

-- 3) 주요 테이블의 row count가 어제와 비슷하다
SELECT 'orders' AS table_name, count(*) FROM orders
UNION ALL
SELECT 'users', count(*) FROM users
UNION ALL
SELECT 'payments', count(*) FROM payments;

-- 4) 가장 최근 비즈니스 이벤트가 보인다
SELECT max(created_at) FROM orders;
SELECT max(created_at) FROM payments;

-- 5) 인덱스·시퀀스가 살아 있다
SELECT count(*) FROM pg_indexes WHERE schemaname = 'public';
SELECT last_value FROM orders_id_seq;
```

이런 쿼리의 결과를 매일 한 줄 로그로 남기고, "갑작스러운 0", "갑작스러운 큰 변화", "최신 시각이 24시간 이상 뒤처짐" 같은 조건에 알람을 건다. 이렇게만 해도 — "백업이 깨져 있다는 사실"을 사고 직전이 아니라 그 며칠 전에 발견하게 된다.

조금 더 욕심을 내면 **자동화된 PITR 드릴**까지 갈 수 있다. 어제 자정의 베이스 백업을 받아, 오늘 오전 9시까지의 WAL을 적용해, "오늘 오전 8시 30분 시점"으로 PITR 복구한 뒤, 그 시점의 row count가 운영 환경의 어제 오전 8시 30분 row count와 일치하는지 비교한다. 불일치가 0.1% 이내면 통과, 그 이상이면 알람. 운영의 신뢰도를 한 단계 더 끌어올리는 패턴이다.

RTO·RPO라는 지표도 이 자리에서 다시 정의된다.

- **RPO (Recovery Point Objective)** — "사고가 나면 얼마만큼의 데이터까지 잃을 수 있는가". WAL 아카이브 간격과 보존 정책이 결정한다. `archive_timeout = 60`이면 RPO는 이론적으로 최대 1분.
- **RTO (Recovery Time Objective)** — "복구를 얼마 안에 끝낼 수 있는가". 베이스 백업 크기, 다운로드 속도, WAL 적용 속도, 검증 절차 시간이 합쳐진 값.

이 두 지표는 종이 위에 적어두는 숫자가 아니라 — 분기에 한 번씩 실측해야 하는 숫자다. "RPO 1분, RTO 1시간"을 SLA에 적어두고 실제 측정은 안 해봤다는 시스템은 — 사고 한 번에 두 숫자 다 깨진다. 분기별 복구 드릴은 그 숫자를 정직하게 만들어주는 유일한 길이다.

DR(Disaster Recovery) 훈련의 한 시나리오를 그려보자. 매 분기 첫째 주 금요일 오후, 운영팀이 모인다. 절차는 이렇다.

1. DR 사이트의 백업으로 새 클러스터를 복원한다 (어제 자정 baseline + 오늘 오전 9시 시점 PITR).
2. 복원 시작 시각, 종료 시각을 기록한다 → 실측 RTO.
3. 복원된 클러스터의 마지막 트랜잭션 시각을 확인한다 → 실측 RPO.
4. 운영 DB의 9시 시점 데이터와 row 단위로 비교한다.
5. 차이 항목, 검증 통과/실패, 발견 이슈를 한 페이지 보고서로 남긴다.
6. 그 보고서를 다음 분기 시작 전에 한 번 더 읽는다.

이 과정을 한 번 돌리고 나면 — 백업·복구 시스템에 대한 팀의 자신감이 완전히 다른 차원이 된다. "그때 가서 한 번도 안 해본 일을 처음 한다"는 두려움이 사라지기 때문이다.

runbook도 빼놓을 수 없다. PITR 명령을 정확히 어떤 순서로 두드릴지, 어떤 검증을 거칠지, 어떤 의사결정 분기에서 누구의 승인을 받을지, 실패 시 롤백은 어떻게 할지 — 이 모든 걸 위키 또는 Git 저장소에 살아 있는 문서로 두자. 사고 새벽에 누가 검색해서 그대로 따라할 수 있을 만큼 구체적으로. 그리고 그 문서를 분기 드릴 때마다 실제 동작과 맞춰 갱신하자.

한 가지 더, **카오스 스타일의 검증**도 한 번씩 시도해볼 만하다. 운영자가 모르는 사이에, 백업 검증 환경에 일부러 결함을 주입하는 것이다. WAL 한 세그먼트를 일부러 빼고 복구를 시도해보거나, 베이스 백업 파일의 권한을 일부러 깨고 복원을 시도해보거나, 검증 호스트의 네트워크를 일부러 분리한 채로 잡을 돌려본다. 알람이 정확한 시각에 정확한 메시지로 울리는지, runbook의 분기 처리가 실제로 작동하는지가 그제야 드러난다. "정상 시나리오만 검증한 시스템"은 비정상이 닥쳤을 때 자주 무너진다. 검증 자체도 검증되어야 한다 — 그 정신을 잊지 말자.

"백업이 있다"와 "복구된다"를 같은 일로 만드는 마지막 한 걸음은 결국 사람과 절차다. 도구는 80%를 해주고, 나머지 20%는 우리가 채워야 한다.

## 19.7 클라우드별 백업 전략

매니지드 PostgreSQL을 쓰면 백업이 다 해결될까? 부분적으로는 그렇다. 그러나 "다 해결됐다"고 생각하는 순간 위험해진다.

각 벤더가 기본으로 제공하는 백업의 정체를 짚어보자.

- **AWS RDS for PostgreSQL** — 자동 백업(daily snapshot + transaction log 보존). 보존 기간 최대 35일. PITR 가능(기본 보존 기간 내). 수동 snapshot 별도. cross-region copy 옵션.
- **AWS Aurora PostgreSQL** — 분산 스토리지 자체가 6 copies · 3 AZ로 복제. continuous backup이 기본. PITR이 secondary 기능이라기보다 native 기능에 가깝다. backtrack(Aurora MySQL 전용 기능이라 PG에는 없음에 유의)과 혼동 주의.
- **GCP Cloud SQL for PostgreSQL** — 자동 백업, transaction log archiving, PITR. cross-region replica 별도.
- **GCP AlloyDB** — 자동 백업·continuous backup, columnar engine과 무관하게 row store 백업은 표준 PG와 같은 모델.
- **Azure Database for PostgreSQL (Flexible)** — geo-redundant 백업 옵션, long-term retention 옵션.
- **Supabase / Neon** — Supabase는 daily backup(Pro 이상 PITR), Neon은 branching이 사실상 PITR과 비슷한 역할(과거 LSN으로 새 branch 생성).

이 정도면 "그냥 매니지드 쓰면 되겠네"라고 생각하기 쉽다. 그런데 여기서 짚어야 할 함정이 몇 가지 있다.

**첫째, 벤더 백업은 그 벤더의 리전·계정 안에만 산다.** 계정 자체가 lock-out 되거나, 리전 전체가 장기 장애에 빠지거나, 청구 분쟁으로 계정이 정지되는 시나리오 — 이런 경우 벤더 자동 백업으로는 아무것도 못 한다. 그래서 진지한 조직은 매니지드 PG를 쓰더라도 **별도 계정·별도 리전·다른 벤더의 오브젝트 스토리지**로 정기적인 logical dump 또는 WAL-G 기반 cross-vendor 백업을 두는 편이 낫다. "벤더가 모든 걸 안전하게 보관해줄 것"이라는 가정에 회사 전체가 인질이 되는 상황은 피해야 한다.

**둘째, 매니지드 PG의 PITR도 검증되어야 한다는 점은 똑같다.** 콘솔에서 "PITR 활성화" 체크박스가 켜져 있다는 사실이 곧 "복구가 된다"는 보증은 아니다. 분기에 한 번씩, 별도 데이터베이스 인스턴스를 PITR로 띄우고, 검증 쿼리를 돌리고, RTO·RPO를 실측하는 절차가 그대로 필요하다. RDS의 콘솔 PITR이 평균 어느 정도 시간이 걸리는지, Aurora가 같은 시점 복구에 얼마나 빠른지 — 이런 수치는 직접 측정해보지 않으면 모른다.

**셋째, logical dump도 함께 둬야 하는 경우가 있다.** 물리적 백업(snapshot, WAL 기반)은 같은 메이저 버전·같은 엔진 안에서만 복원 가능하다. PG 17 백업을 PG 18에서 그대로 못 푼다. 마이그레이션·다운그레이드·다른 벤더로 이전·재해 후 다른 환경에서 복원 같은 시나리오에서는 `pg_dump`/`pg_dumpall`로 만든 logical dump가 유일한 길이다. 매니지드 PG라도 주기적으로 logical dump를 외부 스토리지에 떨궈두는 편이 안전하다.

**넷째, Aurora의 분산 스토리지에 대한 특별한 이해가 필요하다.** Aurora의 storage는 PG의 일반적 storage와 다르다. continuous backup이 storage layer에서 일어나고, snapshot이 거의 즉시 끝난다. 이게 매력이지만 — 동시에 VACUUM 동작, WAL 처리, replication slot 동작이 표준 PG와 다르다. 사고 시 PITR이 표준 PG와 똑같이 동작할 거라고 막연히 가정하지 말고, Aurora 전용 문서를 한 번 읽어두자. 이 주제는 24장에서 별도 절로 다시 다룬다.

조금 더 일반화하면, 매니지드 PG를 쓸 때 백업 전략은 두 층으로 잡는 편이 낫다.

- **1층 (벤더 기본):** 자동 백업·PITR·snapshot. 가장 빠른 복구. 일상적 사고 대응의 첫 수단.
- **2층 (외부 보험):** 별도 계정·별도 리전·다른 벤더 스토리지로의 logical dump 또는 WAL-G 기반 백업. 벤더 자체가 문제일 때의 최후 수단.

2층 백업의 빈도는 1층보다 훨씬 낮아도 된다. 주 1회 또는 월 1회의 dump면 "벤더 lock-out" 시나리오는 충분히 막을 수 있다. 핵심은 비용이 아니라 **백업이 존재하는 신뢰 도메인을 분리한다**는 원리다.

비용 측면에서 한 가지 짚어두자. 매니지드 PG의 자동 백업 보존 기간을 길게 늘릴수록 vendor 청구서가 가파르게 늘어난다. RDS의 35일 자동 백업과 별도 snapshot 보관 비용은 데이터 크기에 따라 결코 작지 않다. 그래서 "내부 정책상 90일 보존이 필요하다"는 요구가 있다면 — 벤더 보존을 무리해서 늘리기보다, 2층 백업으로 장기 보관을 분리하는 편이 비용 효율도 더 낫다. 자주 쓸 가능성이 거의 없는 보관 백업을 비싼 1층에 두는 건 — 찜찜한 일이다.

마지막으로, **Neon의 branching**은 흥미로운 새 모델이라 한 번 더 짚어두자. 운영 DB의 특정 LSN에서 분기한 새 branch를 몇 초 안에 만들 수 있다는 점은 — 사실상 매우 빠른 PITR과 같다. "어제 오후 3시 시점의 DB를 새 branch로 띄워서 직접 확인" 같은 작업이 명령 한 줄로 끝난다. 개발·검증 워크플로우에서는 백업·복구 운영 자체의 무게를 줄여주는 새로운 패턴이다. 다만 이 모델이 기존의 백업 검증 의무를 대체하지는 않는다는 점은 잊지 말자 — branch를 빠르게 만들 수 있다는 것과, 실제 사고에서 RTO·RPO를 만족시키는 복구를 할 수 있다는 것은 — 다시 한 번 다른 일이다.

## 마무리

백업은 결국 미래의 자기 자신에게 보내는 편지다. 사고가 났을 때, 새벽에 호출 받았을 때, 270만 행이 사라졌을 때 — 그 순간의 자신이 평소의 자신에게 묻는다. "그때 백업 검증 한 번 더 해뒀어야 했지?", "PITR 드릴 분기에 한 번씩 하자고 했는데 두 분기째 안 했지?", "벤더 자동 백업만 믿고 외부 dump 안 두기로 한 게 정말 맞았나?"

이 질문들에 미래의 자신이 "괜찮다, 잘 되어 있다"고 답할 수 있도록 — 그게 백업·복구·PITR 운영의 본질이다. pgBackRest를 깔든, Barman을 쓰든, WAL-G를 띄우든, 매니지드 PG의 콘솔 PITR에 기대든 — 도구는 그 답을 만들어주는 수단이다. 도구를 잘 고르는 일은 중요하지만, 그보다 더 중요한 일이 있다. **복구를 일상으로 만드는 것.** 분기 드릴, 자동 검증, 두 층 백업, 살아 있는 runbook — 이 네 가지를 챙기면 어느 도구를 골랐든 큰 사고는 막힌다.

이렇게 백업·복구의 토대가 단단해지면, 그 다음 자연스러운 질문이 따라온다. 한쪽 노드가 죽었을 때 자동으로 다른 노드로 넘어가는 일은 어떻게 할까? 복구 가능성과 가용성은 닮은 듯 다른 두 영역이다. 다음 장에서 HA와 페일오버 — Patroni, pg_auto_failover, 그리고 v17의 failover slot이 만드는 새로운 그림 — 을 함께 살펴보자.
