# 20장. HA와 페일오버 — Patroni·pg_auto_failover·17 failover slot

가용성을 자동화하는 도구를 설치했다고 가용성이 보장되지는 않는다. 실제로 작동하는지 확인할 단 한 가지 방법이 있다. 정기적으로 일부러 죽이는 것이다.

이 말이 농담처럼 들린다면, 한 번도 진짜 페일오버를 안 겪어본 사람일 가능성이 높다. 새벽 세 시에 알람이 울리고, 화면 너머에 보이는 건 "primary unreachable" 한 줄이다. 평소 데모에선 1.2초 만에 standby가 승격됐는데, 오늘은 38초가 흐르고도 새 primary가 안 올라온다. 그 38초 동안 머릿속에서 도는 질문은 하나다. "도구가 자동으로 처리해 줄 거라고 했잖아?"

자동화는 마법이 아니다. 자동화는 우리가 미리 정의한 조건 안에서, 미리 짠 스크립트를 미리 정한 순서대로 돌리는 일이다. 조건이 어긋나면 자동화는 그대로 멈춘다. 더 나쁜 건, 잘못된 조건에서 자동화가 멋대로 돌아 split-brain을 만드는 경우다. 둘 다 primary라고 우기는 두 노드를 보면 그제야 깨닫게 된다 — 가용성 도구는 "절대 안 죽게 해주는 도구"가 아니라 "죽었을 때 우리 대신 결정을 내려주는 도구"라는 사실을.

그래서 이번 장의 화두는 두 가지다. 하나, 도구 자체를 이해하자. Patroni와 pg_auto_failover가 무엇을 해주고 무엇을 안 해주는지, 어디서 트레이드오프가 갈리는지를 정직하게 본다. 둘, 페일오버 훈련을 운영의 일부로 박아 두자. 분기마다 일부러 primary를 죽이고, 체크리스트를 들고 시계를 재고, 그 결과를 다음 분기 개선 목록으로 남긴다. 이 두 가지가 갖춰지지 않은 HA 구성은 "있다고 적힌 HA"일 뿐, 사고가 났을 때 우리 편을 들어주지는 않는다.

먼저 모든 HA의 토대인 streaming replication부터 살펴보자.

## 20.1 Streaming replication 기초 — 동기와 비동기 사이

PostgreSQL의 HA를 이야기할 때 빠지지 않고 등장하는 단어가 "streaming replication"이다. 그런데 이게 어떻게 작동하는지부터 짚지 않으면, 그 뒤의 모든 의사결정이 모래 위에 짓는 집이 된다. 한 번 살펴보자.

streaming replication의 출발점은 WAL이다. 7장에서 본 그 WAL이다. primary는 모든 변경을 일단 WAL에 적는다. 이 WAL이 디스크에 fsync되는 순간 트랜잭션은 "내구화"됐다고 본다. streaming replication은 이 WAL을 standby에게 네트워크로 흘려보낸다. standby는 받은 WAL을 자기 데이터 디렉터리에 그대로 재생한다 — replay라고 부른다. 결과적으로 standby는 primary와 거의 같은 상태를 유지하게 된다. 거의 같은 상태.

여기서 "거의"라는 단어가 중요하다. 얼마나 거의 같은지를 정하는 것이 동기·비동기의 차이다.

**비동기(asynchronous) 복제**는 primary가 트랜잭션을 커밋할 때 standby의 응답을 기다리지 않는다. WAL을 standby에게 보내긴 보내지만, 그 도착·반영을 확인하지 않고 클라이언트에게 "커밋됐다"고 답한다. 그래서 빠르다. 응답 지연이 거의 안 늘어난다. 그런데 primary가 갑자기 죽으면, 아직 standby에 안 도착한 WAL 몇 KB가 그대로 사라진다. 그 안에 들어 있던 트랜잭션은 영원히 잃어버린다. 이걸 "data loss window"라 부르는데, 정상 운영 시에는 보통 수 ms 수준이지만, 네트워크가 흔들리거나 standby가 늦으면 수 초까지 벌어지기도 한다.

**동기(synchronous) 복제**는 한 발 더 간다. primary가 커밋을 클라이언트에 알리기 전에, 지정된 standby가 WAL을 받았다(또는 fsync까지 마쳤다)는 확인을 기다린다. data loss window가 사실상 0이 된다. 대신 응답 지연이 늘어난다. 가장 가까운 standby까지의 네트워크 왕복 시간만큼은 무조건 더 걸린다. 같은 데이터센터 안이면 1~3ms 정도지만, 다른 AZ로 가면 5~15ms, 다른 리전이면 수십 ms까지 뛴다.

그렇다면 어느 쪽을 골라야 할까? "데이터 손실 0이 최고니까 무조건 동기"라고 답하고 싶지만, 그게 함정이다. 동기 복제는 한 가지 결정적인 위험을 같이 들고 온다. **지정된 동기 standby가 모두 응답을 못 하면 primary의 커밋이 멈춘다.** standby 한 대만 지정해 두고 그 한 대가 죽으면, primary는 "응답 기다리는 중"으로 영원히 멈춰 있다. 사용자가 보기엔 primary가 살아 있는데도 모든 쓰기가 막힌다. 끔찍한 일이다.

그래서 동기 복제를 쓰려면 최소 두 대 이상의 standby를 동기 후보로 묶고, `synchronous_standby_names`에 `ANY 1 (s1, s2)` 같은 정족수(quorum) 표현을 써서 "둘 중 하나만 응답하면 된다"고 풀어줘야 한다. 한 대가 죽어도 다른 한 대가 응답하면 커밋이 진행된다. 이게 우리가 베스트 프랙티스로 "최소 3노드(primary + 2 standby)"를 말하는 이유 중 하나다 — 동기 복제의 가용성 함정을 피하려면 standby가 두 대는 있어야 한다.

`synchronous_commit` 파라미터도 한 번 정리해 두는 편이 낫다. 이 값은 트랜잭션 커밋이 어디까지 확인됐을 때 "성공"으로 응답할지를 정한다.

- `off`: primary 메모리에만 쓰여도 성공으로 본다. 가장 빠르고 가장 위험하다.
- `local`: primary 디스크에 fsync된 것까지 확인. standby는 안 본다. 비동기 복제의 표준 동작.
- `remote_write`: 동기 standby의 OS 버퍼까지 도달. 디스크 fsync는 안 기다린다.
- `remote_apply`: 동기 standby가 WAL을 replay까지 마쳐서 standby에서 읽어도 같은 결과가 나오는 상태.
- `on`(기본값): 동기 standby가 fsync까지 마친 것까지 확인.

대부분의 OLTP 시스템은 `on` 또는 `remote_apply`다. 분석 워크로드라 약간의 손실은 감내할 수 있다면 `local`도 답이 된다. 한 가지만 기억하자. 이 파라미터는 트랜잭션 단위로 바꿀 수 있다. 결제 같은 절대 손실 안 되는 트랜잭션은 `SET LOCAL synchronous_commit = remote_apply`로 강화하고, 로그 같은 가벼운 쓰기는 `SET LOCAL synchronous_commit = local`로 풀어주는 식의 차등 운영이 가능하다. 모든 트랜잭션을 같은 강도로 처리할 필요는 없다.

마지막으로 한 가지. streaming replication은 standby에서 읽기 쿼리를 받을 수 있다(`hot_standby = on`이 기본값). 그래서 "read replica"라고 부르기도 한다. 그런데 standby는 primary의 WAL을 replay하는 동안 잠금 충돌이 생기면 진행 중인 standby 쿼리를 강제로 중단시킨다. `max_standby_streaming_delay`로 어느 정도 기다려 줄지 정할 수 있는데, 너무 크게 두면 standby가 점점 뒤처지고, 너무 작게 두면 standby 쿼리가 자주 죽는다. read replica를 적극적으로 쓸 거면 이 파라미터의 의미를 한 번은 곱씹어 보자.

이와 묶이는 또 하나가 **replication slot**이다. slot은 "이 컨슈머가 어디까지 받았는지"를 primary가 기억하게 만드는 장치다. physical slot은 standby용이고, logical slot은 Debezium 같은 CDC 컨슈머용이다. slot이 있으면 컨슈머가 잠시 끊겨도 primary가 그 위치 이전의 WAL을 함부로 삭제하지 않는다. 안전한 대신 위험도 같이 들어온다. 컨슈머가 영구히 사라지거나 멈춰 있는데 slot을 안 지우면, WAL이 디스크에 무한정 쌓여 어느 날 disk full로 primary가 멈춘다. `pg_replication_slots` 뷰의 `active`와 `confirmed_flush_lsn`을 모니터링 대시보드에 올려 두는 편이 낫다. 안 쓰는 slot은 빠르게 삭제하는 운영 습관도 필요하다.

여기까지가 streaming replication의 큰 그림이다. 한 가지만 다시 짚자. **HA 도구들이 자동으로 처리해주는 모든 일이 결국 이 streaming replication 위에서 일어난다.** 그래서 자동화 도구의 옵션을 이해하려면 그 옵션이 streaming replication의 어떤 손잡이를 돌리는지를 알아야 한다. 그 위에 가용성 자동화를 얹는 도구들을 만날 차례다.

## 20.2 Patroni — 자동화의 표준이 된 이유

Patroni를 한 줄로 요약하면 "분산 합의 시스템에 PostgreSQL의 상태를 등록해 두고, 그 합의에 따라 누가 primary가 될지를 자동으로 결정하는 도구"다. Zalando가 만들었고, 지금은 사실상 PG HA의 표준이 됐다. 왜 표준이 됐는지부터 풀어보자.

Patroni가 풀어낸 문제는 단순해 보이지만 실은 분산 시스템 교과서의 한 장이다. 노드가 여러 대 있고, 그중 한 대가 primary다. primary가 죽으면 살아 있는 standby 중 누군가가 새 primary가 돼야 한다. 이때 가장 두려운 시나리오는 **split-brain** — 네트워크가 일시적으로 갈라져 양쪽 모두 자기를 primary로 인식하는 상황이다. 양쪽이 각각 쓰기를 받기 시작하면 데이터는 재앙적으로 갈라진다. 합치는 길은 사람 손으로 한쪽을 버리는 것뿐이다. 끔찍하다.

이 문제를 푸는 방법은 의외로 단순하다. **외부의 합의 시스템에게 "지금 primary가 누구인지"의 진실을 맡긴다.** 합의 시스템은 그 자체로 분산되어 있고(보통 3~5대), 다수결로만 진실을 결정한다. 어떤 노드가 primary가 되려면 합의 시스템에 가서 "내가 primary다"라는 락(leader key)을 얻어야 한다. 락은 TTL이 짧아서(보통 30초 안팎) 주기적으로 갱신해야 유지된다. 갱신을 못 하면 락이 만료되고, 다른 노드가 락을 얻어 새 primary가 된다.

합의 시스템으로 Patroni가 지원하는 것이 etcd, Consul, ZooKeeper, Kubernetes API다. 가장 흔히 쓰이는 게 etcd 또는 Kubernetes 환경의 Kubernetes API다. etcd는 Raft 합의 알고리즘을 쓰는 가벼운 키-값 저장소로, 보통 3대 또는 5대로 클러스터를 구성한다. Patroni는 이 etcd에 자기 클러스터의 모든 노드 상태를 적어 두고, leader key를 두고 경쟁한다.

Patroni가 좋은 점은 단순히 "장애 감지하고 승격"만 하는 게 아니라는 점이다. 한 번 정리해 보자.

- **자동 페일오버**: leader key의 TTL이 만료되면 가장 적합한 standby가 새 primary로 승격된다.
- **자동 페일백 없음**: 죽었던 primary가 돌아와도 자동으로 primary로 복귀하지 않는다. 그대로 standby가 된다. "장애 직후의 자동 페일백"이 일으키는 사고를 막기 위해서다. 의도적인 설계다.
- **REST API**: 모든 노드가 8008 포트(기본값)에 REST API를 띄운다. `/primary`, `/replica`, `/health`, `/cluster` 같은 엔드포인트로 상태를 조회·제어할 수 있다. 이게 라우팅 계층(20.5)과 만나면 진짜 강력해진다.
- **patronictl CLI**: 클러스터 상태 조회, 수동 페일오버(switchover), 노드 재시작, 설정 변경을 한 곳에서. 운영자 친화적이다.
- **PostgreSQL 설정 관리**: `postgresql.conf`를 Patroni 설정으로부터 생성·관리한다. 노드 간 설정 drift를 막아준다.
- **base backup 자동화**: 새 standby를 붙일 때 `pg_basebackup` 또는 사용자 정의 스크립트(예: pgBackRest)로 자동 초기화한다.

설정 파일은 YAML이고, 각 노드마다 자기 정보가 들어간다. 핵심만 추려보자.

```yaml
scope: pg-prod-cluster
namespace: /service/
name: pg-node-1

restapi:
  listen: 0.0.0.0:8008
  connect_address: 10.0.1.11:8008

etcd3:
  hosts: 10.0.10.11:2379,10.0.10.12:2379,10.0.10.13:2379

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576  # 1MB
    synchronous_mode: true
    synchronous_mode_strict: false
    postgresql:
      use_pg_rewind: true
      parameters:
        max_connections: 200
        shared_buffers: 8GB
        wal_level: replica
        hot_standby: on
        max_wal_senders: 10
        max_replication_slots: 10
        synchronous_commit: on
        synchronous_standby_names: 'ANY 1 (*)'

postgresql:
  listen: 0.0.0.0:5432
  connect_address: 10.0.1.11:5432
  data_dir: /var/lib/postgresql/data
  authentication:
    replication:
      username: replicator
      password: ${REPLICATION_PASSWORD}
    superuser:
      username: postgres
      password: ${POSTGRES_PASSWORD}
```

이 YAML에서 눈여겨볼 항목 몇 개를 짚어보자.

`ttl: 30`은 leader key의 유효 시간이다. 30초 동안 갱신이 없으면 leader 자리가 비고 페일오버가 시작된다. 이걸 더 줄이면 페일오버는 빨라지지만 잘못된 페일오버(false positive)도 늘어난다. 네트워크 hiccup 한 번에 페일오버가 도는 건 더 큰 사고를 만든다. 보통 20~60초 범위에서 운영 환경에 맞게 잡는다.

`maximum_lag_on_failover`는 페일오버 시점에 standby가 primary 대비 얼마까지 뒤처져 있어도 승격 후보로 받을지를 정한다. 1MB로 두면 그보다 더 뒤처진 standby는 후보에서 빠진다. 이 값이 너무 크면 데이터 손실을 감수해야 하고, 너무 작으면 페일오버할 후보가 없어 클러스터가 정지한다.

`synchronous_mode: true`는 Patroni가 동기 standby를 자동으로 관리하게 한다. Patroni가 standby의 상태를 보고 `synchronous_standby_names`를 동적으로 갱신해 준다. `synchronous_mode_strict: false`는 "동기 standby가 하나도 없으면 비동기로 떨어진다"는 뜻이다. `strict: true`로 두면 동기 standby가 없을 때 쓰기가 막힌다. 이게 더 안전해 보이지만 운영의 무게가 다르다. 트레이드오프를 자기 시스템의 RPO 요구에 맞게 골라야 한다.

`use_pg_rewind: true`는 페일오버 후 옛 primary가 돌아왔을 때 처음부터 base backup을 다시 받지 않고 `pg_rewind`로 빠르게 재동기화한다는 설정이다. 4TB짜리 클러스터를 매번 처음부터 받을 순 없다.

Patroni의 강점 하나가 더 있다. **DCS(Distributed Configuration Store) 추상화**다. etcd가 아니라 Consul, ZooKeeper, Kubernetes로 바꿔도 Patroni 자체 설정은 거의 그대로다. 인프라 진영의 선택에 따라 합의 시스템을 바꿀 수 있다. Kubernetes 환경에서 PG를 돌린다면 Kubernetes API를 DCS로 쓰는 게 보통이고, 별도 etcd를 띄울 필요가 없어진다.

Patroni의 callback 기능도 한 번 짚어 두자. Patroni는 클러스터 상태가 바뀔 때마다(예: `on_start`, `on_stop`, `on_restart`, `on_role_change`) 운영자가 지정한 외부 스크립트를 호출해 준다. role change 시점에 DNS 레코드를 갱신한다든지, Slack에 알림을 던진다든지, 외부 모니터링에 페일오버 이벤트를 표시하는 식의 hook을 여기에 건다. 자동화의 마지막 1마일을 채우는 데 유용한 기능이다.

물론 Patroni가 만능은 아니다. 학습 곡선이 있다. YAML이 길고, etcd를 따로 운영해야 하고(또는 다른 DCS를 골라야 하고), `pg_rewind` 시나리오·`bootstrap` 시나리오·`callback`을 한 번씩은 다 한 번 다뤄봐야 운영자가 안심할 수 있다. 작은 팀이 처음부터 Patroni를 끌어들이는 건 부담스러울 수 있다. 그래서 다음에 살펴볼 pg_auto_failover 같은 더 가벼운 대안이 생긴 것이다.

한 가지만 더. Patroni가 사실상 표준이 됐다고 해서 다른 도구들이 사라진 건 아니다. 2ndQuadrant의 **repmgr**은 가장 오래된 PG HA 도구 중 하나로, 가볍지만 자동 페일오버 자동화 측면에서는 Patroni만큼의 정밀함을 갖지 못한다. **Stolon**은 Sorint.lab이 만든 Patroni의 대안 격으로 Kubernetes 환경에서 한때 인기였지만 커뮤니티 활성도가 점차 줄었다. **PAF**(PostgreSQL Automatic Failover)는 Pacemaker/Corosync 기반의 전통적 HA 스택으로, 리눅스 클러스터링 운영 경험이 있는 팀이 손에 맞을 수 있다. 도구 선택은 우리 팀이 이미 쓰는 인프라 스택과의 궁합으로 정하는 편이 낫다. Kubernetes 위라면 Patroni 또는 Stolon이 자연스럽고, 베어메탈 + Pacemaker 경험이 있다면 PAF도 답이 된다.

## 20.3 pg_auto_failover — 단순함의 무게와 SPoF의 트레이드오프

pg_auto_failover는 Citus 팀(현 Microsoft) 이 만든 도구다. Patroni가 "외부 분산 합의를 끼워 단단한 자동화를 만든다"는 길을 갔다면, pg_auto_failover는 "PostgreSQL 한 대를 monitor로 띄워 모든 상태 관리를 거기서 한다"는 길을 갔다. 한 마디로 정리하면, monitor 한 대가 cluster의 상태를 책임진다.

설정이 정말 단순하다. PostgreSQL을 monitor 모드로 한 대 띄우고, 데이터 노드들이 `pg_autoctl` 명령으로 자기를 등록한다.

```bash
# monitor 노드
pg_autoctl create monitor \
    --hostname monitor.internal \
    --auth scram-sha-256 \
    --ssl-self-signed \
    --run

# primary 후보 노드
pg_autoctl create postgres \
    --hostname pg-1.internal \
    --auth scram-sha-256 \
    --ssl-self-signed \
    --monitor 'postgres://autoctl_node@monitor.internal/pg_auto_failover' \
    --run

# standby 후보 노드
pg_autoctl create postgres \
    --hostname pg-2.internal \
    --auth scram-sha-256 \
    --ssl-self-signed \
    --monitor 'postgres://autoctl_node@monitor.internal/pg_auto_failover' \
    --run
```

이게 거의 전부다. monitor가 두 노드의 상태를 보면서 누가 primary일지, 언제 페일오버해야 할지를 정한다. monitor와 데이터 노드들이 주기적으로 heartbeat를 주고받으며 상태 머신이 돌아간다. 상태 전이가 잘 정의돼 있어서 운영자가 머릿속에 그림을 그리기 쉽다.

번거로운 etcd 클러스터를 따로 운영할 필요가 없다는 점, YAML 더미를 다듬을 일이 없다는 점, `pg_autoctl show state` 한 줄로 클러스터 상태가 한눈에 들어온다는 점은 진짜 매력이다. 작은 팀이 빠르게 HA를 구축하려 할 때 pg_auto_failover는 좋은 첫 선택이다.

그런데 — 여기서 한 가지 찜찜한 지점이 있다. **monitor가 한 대다.** monitor가 죽으면 어떻게 될까?

월요일 점심, monitor가 다운된다고 해보자. 데이터 노드들은 monitor를 못 찾아 페일오버 결정을 내리지 못한다. 다행히 현재 primary가 잘 살아 있다면 서비스는 계속 돌아간다 — pg_auto_failover는 monitor가 죽었다고 해서 primary를 셧다운하지는 않는다. 그런데 만약 primary까지 같이 죽으면? monitor도 죽었고 primary도 죽었으니, standby가 알아서 승격할 수 없다. 사람 손이 필요하다. 새벽 세 시의 사람 손이.

문서에는 "monitor의 가용성이 페일오버 자동화에 필수"라고 분명히 적혀 있다. monitor를 HA로 띄우는 권장 패턴(예: PostgreSQL streaming replication + 외부 라우팅)이 따로 있긴 하지만, 그 순간 "단순함"이라는 pg_auto_failover의 가장 큰 무기가 줄어든다. monitor도 HA, 데이터도 HA로 두 겹의 HA를 운영하게 되는 셈이다.

그렇다면 pg_auto_failover를 언제 고르는 게 합리적일까? 정리해 보자.

- **소~중 규모 클러스터** (primary + 1~2 standby 정도)
- **운영 인력이 한정적**이고, etcd 클러스터까지 책임지기 어려운 팀
- **monitor 노드의 SPoF를 감수**할 수 있는 SLA (또는 monitor를 HA로 띄울 의지가 있음)
- **단일 데이터센터** 안의 단순한 토폴로지

반대로 Patroni가 더 적합한 경우는 이렇다.

- **대규모·여러 클러스터**를 일관된 방식으로 관리
- **DCS를 이미 운영** 중(Kubernetes API, 회사 표준 etcd/Consul)
- **callback 같은 세밀한 커스터마이징**이 필요
- **multi-region** 또는 복잡한 토폴로지

도구 선택은 종교가 아니다. 우리 팀의 운영 역량, 클러스터 규모, SLA 요구를 보고 골라야 한다. Patroni가 "더 좋다"는 통념이 있긴 하지만, 그건 어떤 환경에서의 이야기다. 작은 팀이 pg_auto_failover로 1년을 잘 굴리다가 클러스터가 커지면 Patroni로 옮기는 길도 합리적인 경로다.

한 가지만 기억해 두자. 어떤 도구를 고르든 — **도구가 자동으로 결정을 내리는 만큼, 우리는 그 결정의 조건을 정확히 이해해야 한다.** TTL이 몇 초인지, maximum_lag이 얼마인지, monitor가 못 보이면 어떻게 되는지를 모른 채 도구를 깔아 두면, 사고 당시에 "이게 왜 이러지?"라는 질문 앞에서 손이 멈춘다.

## 20.4 최소 3노드 — primary 한 대와 standby 두 대

HA를 처음 설계할 때 가장 흔히 나오는 질문이 "노드 몇 대로 시작해야 하는가"다. 비용을 줄이고 싶은 마음에 "primary 한 대 + standby 한 대로 시작하고, 나중에 늘리자"는 답이 종종 튀어나온다. 그 답은 거의 항상 후회로 돌아온다.

왜 최소 3노드냐. 이유가 세 가지다.

**첫째, 동기 복제의 가용성 함정 때문이다.** 20.1에서 봤듯이 동기 복제는 지정된 standby가 응답을 못 하면 primary의 커밋이 멈춘다. standby가 한 대뿐이라면, 그 standby가 점검·재시작·OS 패치 같은 일상적인 이유로 잠깐 빠질 때마다 primary가 멈춘다. 동기 standby를 두 대 두고 `ANY 1 (s1, s2)` 같은 정족수로 묶으면 한 대가 빠져도 다른 한 대가 응답한다.

**둘째, 페일오버 시 후보 부재의 위험 때문이다.** primary가 죽었을 때 새 primary가 될 수 있는 standby가 한 대뿐이라면, 그 standby가 동시에 문제를 겪고 있을 때(예: 같은 디스크 펌웨어 버그, 같은 네트워크 스위치 장애) 페일오버할 곳이 없다. 두 대의 standby가 다른 가용 영역(AZ)에 있다면 한 AZ가 통째로 죽어도 다른 AZ의 standby가 살아 있을 확률이 훨씬 높다.

**셋째, 페일오버 후의 잠시 동안의 단일성 때문이다.** primary 한 대 + standby 한 대로 운영하다 페일오버가 일어나면, 새 primary가 된 노드 하나만 남는다. 그 시점부터 새 standby를 만들기 전까지는 사실상 HA가 없는 상태가 된다. 그 사이에 새 primary마저 죽으면 데이터 손실 사고로 직결된다. standby가 두 대였다면, 페일오버 후에도 primary + standby 한 대의 구성이 유지된다. 사고의 두 번째 도미노를 막아준다.

그래서 베스트 프랙티스는 **primary + standby 두 대, 가능하면 서로 다른 AZ에 분산**이다. 동기·비동기 구성은 다음 중 한 가지가 흔하다.

- **standby 1은 동기, standby 2는 비동기**: 같은 AZ의 가까운 standby를 동기로, 다른 AZ의 standby를 비동기로. 일상적 가용성과 재해 복구를 동시에 노린다.
- **standby 2대 모두 동기 후보, `ANY 1` 정족수**: 둘 중 빠른 응답을 받는다. 한 대가 빠져도 멈추지 않는다. 두 standby가 비슷한 네트워크 거리에 있을 때 유리하다.
- **모두 비동기, RPO를 일부 포기**: 분석·로그 워크로드처럼 약간의 데이터 손실을 감수할 수 있는 경우. 가장 가볍지만 가장 손실 위험이 크다.

3노드 구성에서 한 가지 더 짚어두자 — **합의 시스템(etcd)의 노드 수**도 3대 또는 5대다. PostgreSQL 노드 수와 별개로, Patroni가 쓰는 etcd 클러스터가 3대 이상의 홀수여야 다수결 합의가 가능하다. 운영하다 보면 PostgreSQL 노드 3대, etcd 노드 3대, monitor 노드 1~2대, 라우팅 계층까지 더해 인프라가 빠르게 늘어난다. 처음 견적 잘못 잡으면 "HA를 위해 인프라 비용이 두 배가 됐다"는 보고가 올라간다. 미리 알고 시작하는 편이 낫다.

3노드 위에 한 단계 더 보태는 패턴도 익숙해질 만하다. **cascading replication**이다. 첫 번째 standby가 primary로부터 WAL을 받고, 그 standby에 두 번째·세 번째 standby가 또 붙어 받는 구조다. 한 primary가 standby 10대에 직접 WAL을 흘리면 네트워크 부하가 부담스럽지만, cascading으로 트리 구조를 만들면 primary는 1~2 노드에만 WAL을 보내고, 그 standby가 또 다음 노드들에 분기해 보낸다. 읽기 부하가 큰 워크로드, 또는 멀리 떨어진 리전에 read replica를 더 두는 경우에 유리한 패턴이다.

비용이 부담이라면 한 가지 대안이 있다. 매니지드 PostgreSQL(RDS, Aurora, Cloud SQL, AlloyDB)을 쓰면 이 3노드·etcd·monitor 같은 인프라 운영을 벤더가 책임진다. 우리는 HA 옵션을 켜는 결정만 하면 된다. 대신 24장에서 다룰 트레이드오프 — 비용 모델, 익스텐션 지원, 라이선스 잠금 — 가 따라온다. 자기 운영을 고를지, 매니지드를 고를지는 24장에서 정직하게 풀어볼 예정이다.

여기서 한 가지만 기억해 두자. **HA 노드 수와 백업의 관계는 별개다.** 3노드 HA를 구성했다고 백업이 필요 없는 게 아니다. HA는 "한 노드가 죽었을 때 다른 노드가 이어받는" 가용성의 문제고, 백업은 "사람의 실수나 데이터 손상으로 모든 노드가 같은 상태로 망가졌을 때 과거 시점으로 되돌리는" 복구의 문제다. DROP TABLE 한 줄이 모든 standby에 똑같이 replay되어 모든 노드에서 같은 테이블이 사라지면, HA 노드 100개로도 데이터를 되찾을 길이 없다. 19장에서 본 pgBackRest와 PITR이 그래서 HA와는 별도의 운영 축이다. 둘 다 챙기는 편이 낫다.

## 20.5 라우팅 — PgBouncer·HAProxy와 `/primary` health check

도구가 자동으로 페일오버를 한다고 해서 끝이 아니다. 애플리케이션이 새 primary에게 어떻게 도달할 것인지가 남는다. 이걸 "라우팅 계층"이라 부른다.

생각해 보자. 페일오버 전에 애플리케이션은 `pg-1.internal:5432`에 연결돼 있었다. 그런데 페일오버가 일어나 `pg-2.internal:5432`가 새 primary가 됐다. 애플리케이션은 어떻게 이 변화를 알게 될까? 가장 단순한 방법은 "애플리케이션 설정에서 호스트를 바꾸고 재시작"이다. 끔찍한 일이다. 페일오버할 때마다 애플리케이션을 재시작할 순 없다.

해결은 두 갈래다. 클라이언트 측 해결과 서버 측 해결.

**클라이언트 측 해결**은 libpq의 multi-host connection string을 쓰는 것이다.

```
postgresql://pg-1.internal,pg-2.internal,pg-3.internal/mydb?target_session_attrs=read-write
```

`target_session_attrs=read-write`는 "쓰기 가능한 노드, 즉 primary에만 연결하라"는 의미다. libpq가 순서대로 시도해서 primary를 찾아 연결한다. 페일오버가 일어나도 다음 연결 시점에 새 primary를 자동으로 찾는다. 가벼운 첫 선택이지만, 이미 맺어진 연결은 끊긴 뒤에야 다시 찾는다는 한계가 있다.

**서버 측 해결**은 라우팅 프록시를 앞에 두는 것이다. 가장 흔한 조합이 PgBouncer + HAProxy다.

- **HAProxy**가 TCP 또는 HTTP 레벨에서 트래픽을 받아, 백엔드 PG 노드들 중 "지금 primary인 노드"에게 라우팅한다.
- **PgBouncer**는 그 앞 또는 뒤에서 connection pooling을 한다(21장에서 자세히).

HAProxy가 "지금 primary가 누구인지"를 어떻게 알까. 여기서 Patroni의 **REST API**가 빛난다. Patroni를 깐 모든 PG 노드는 8008 포트에 REST 엔드포인트를 띄운다. 그중 `/primary`는 자기가 primary면 HTTP 200, 아니면 HTTP 503을 반환한다. HAProxy가 이 엔드포인트를 health check로 쓰면, 자동으로 primary 노드에게만 트래픽을 보내게 된다.

HAProxy 설정 예시를 보자.

```haproxy
global
    maxconn 4000
    log /dev/log local0

defaults
    log global
    mode tcp
    timeout connect 5s
    timeout client 30m
    timeout server 30m

listen pg-primary
    bind *:5000
    option httpchk OPTIONS /primary
    http-check expect status 200
    default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
    server pg-1 10.0.1.11:5432 maxconn 200 check port 8008
    server pg-2 10.0.1.12:5432 maxconn 200 check port 8008
    server pg-3 10.0.1.13:5432 maxconn 200 check port 8008

listen pg-replicas
    bind *:5001
    balance roundrobin
    option httpchk OPTIONS /replica
    http-check expect status 200
    default-server inter 3s fall 3 rise 2
    server pg-1 10.0.1.11:5432 maxconn 200 check port 8008
    server pg-2 10.0.1.12:5432 maxconn 200 check port 8008
    server pg-3 10.0.1.13:5432 maxconn 200 check port 8008
```

이 설정에서 눈여겨볼 점 몇 가지를 짚자.

`listen pg-primary` 블록은 5000 포트에서 쓰기 트래픽을 받는다. health check로 `/primary`를 두드려 200을 받는 노드만 백엔드로 쓴다. 페일오버가 일어나면 옛 primary가 503을 반환하기 시작하고, 새 primary가 200을 반환하기 시작한다. HAProxy의 health check 주기(`inter 3s`)와 실패/성공 임계값(`fall 3 rise 2`)에 따라 약 6~9초 안에 라우팅이 새 primary로 옮겨간다.

`on-marked-down shutdown-sessions` 옵션이 중요하다. 옛 primary가 down 판정을 받으면, HAProxy가 그쪽으로 가던 모든 기존 세션을 강제 종료한다. 그러면 애플리케이션이 connection error를 받고 재연결을 시도한다 — 새 5000 포트로 연결하면 자동으로 새 primary에 도달한다. 이게 빠진 채로 두면, 끊긴 옛 primary와의 연결이 좀비처럼 남아 있다가 timeout이 나야 풀린다. 페일오버 체감 시간이 길어진다.

`listen pg-replicas` 블록은 5001 포트에서 읽기 전용 트래픽을 받는다. `/replica` health check로 standby 노드만 골라 round-robin으로 분산한다. 읽기 쿼리는 standby로 보내 primary 부담을 줄이는 패턴이다. 단, 20.1에서 짚었듯 standby는 replication lag이 있으므로 "방금 쓴 데이터를 바로 읽어야 하는" 쿼리는 primary로 보내야 한다. 애플리케이션이 read-your-writes 일관성이 필요한 시점을 알아서 5000 포트로 가게 해야 한다.

라우팅 계층 자체의 HA도 잊지 말자. HAProxy 한 대만 두면 그게 새 SPoF가 된다. 보통은 **HAProxy 두 대 + Keepalived의 VRRP**로 VIP를 띄워, HAProxy 한 대가 죽으면 다른 한 대가 VIP를 인계받게 한다. 클라우드면 ELB/ALB 같은 매니지드 로드 밸런서가 그 역할을 대신한다.

여기까지 잘 따라왔다면 마음 한구석이 살짝 어지러울 수 있다. PostgreSQL 노드 3대, etcd 3대, HAProxy 2대, Keepalived, PgBouncer까지. 진짜 이 모든 게 다 필요한가? 솔직히 답하면, 모두 다 필요하지는 않다. 우리 시스템의 SLA가 99.9%면 충분한지, 99.99%여야 하는지, 99.999%여야 하는지에 따라 구성이 달라진다. 99.9%는 연간 8.76시간 다운을 허용한다. 99.99%는 52.6분이다. 99.999%는 5.26분이다. 분 단위로 가용성을 줄이려면, 그만큼 인프라 무게가 늘어난다.

설계는 SLA에서 시작하는 편이 낫다. "그냥 좋아 보이는 모든 컴포넌트를 다 깔자"가 아니라, "우리의 SLA를 달성하는 최소 구성은 무엇인가"부터 묻자. 그러면 PostgreSQL 노드도 3대로 충분한지, 5대가 필요한지가 자연스럽게 결정된다.

## 20.6 분기별 페일오버 훈련 — 시나리오 한 개를 깊이

여기까지가 도구의 이야기였다. 이제 더 중요한 이야기를 한다. **도구를 깔았다고 페일오버가 작동한다는 보장은 없다.** 시연 영상에서 1.2초 만에 페일오버되는 클러스터가, 우리 운영 환경에서 실제로 그렇게 작동하는지는 확인해야 안다. 확인할 길은 하나다. 일부러 죽이는 것이다.

분기마다 한 번, 일정한 절차로 페일오버를 실행한다. 처음엔 비운영 환경에서, 손에 익으면 운영 환경의 점검 시간대에. 이걸 "페일오버 훈련" 또는 "Game Day"라 부른다. 이번 절에서는 시나리오 한 개를 끝까지 따라가 본다. 스크립트, 체크리스트, 통과 기준까지.

### 시나리오: primary 강제 종료 후 자동 페일오버 검증

#### 사전 조건과 환경

- 클러스터: PG 17, Patroni 3.x, etcd 3.5.x, HAProxy 2.x
- 노드: primary 1 + standby 2 (모두 다른 AZ), etcd 3대, HAProxy 2대
- 워크로드: pgbench 5분간 32 connection으로 TPC-B 유사 부하
- 목표 RTO: 30초 이하 / 목표 RPO: 0 (동기 복제 사용 중)

#### D-1 준비 (훈련 전날)

준비를 안 한 훈련은 사고다. 다음을 모두 확인하고 시작하자.

- [ ] **모든 노드의 상태가 정상**: `patronictl -c /etc/patroni/patroni.yml list`로 클러스터 상태가 모두 `running` + `streaming`인지 확인.
- [ ] **streaming lag이 0 byte에 가까운지**: `SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) FROM pg_stat_replication;`
- [ ] **백업이 최근 24시간 안에 성공**: pgBackRest의 `info` 명령으로 확인.
- [ ] **etcd 클러스터 정족수 정상**: `etcdctl endpoint status` 모든 노드 healthy.
- [ ] **HAProxy 모든 백엔드 health 정상**: 5000 포트는 1개 노드만 UP, 5001 포트는 2개 standby UP.
- [ ] **모니터링 대시보드가 작동**: Grafana로 primary CPU, 연결 수, replication lag을 실시간으로 볼 수 있어야 함.
- [ ] **롤백 시나리오 합의**: 페일오버가 의도대로 안 됐을 때 어디까지 사람이 개입할지를 미리 합의. 의사 결정자(누가 "수동 개입" 콜을 할지)도 미리 지정.
- [ ] **이해관계자 통보**: 운영팀, 애플리케이션팀, 비즈니스팀에 훈련 시간대 공유. "실제 사고가 아님"을 사전 공지.

#### 훈련 시나리오 스크립트

```bash
#!/bin/bash
# fail-over-drill.sh
# 분기 페일오버 훈련 자동화 스크립트

set -euo pipefail

DRILL_ID="drill-$(date +%Y%m%d-%H%M)"
LOG_DIR="/var/log/pg-drill/${DRILL_ID}"
mkdir -p "${LOG_DIR}"

echo "==> [${DRILL_ID}] 페일오버 훈련 시작" | tee "${LOG_DIR}/timeline.log"

# 0. 사전 상태 캡처
echo "==> T+0s: 사전 상태 캡처" | tee -a "${LOG_DIR}/timeline.log"
patronictl -c /etc/patroni/patroni.yml list > "${LOG_DIR}/before.txt"
psql -h pg-haproxy -p 5000 -c "SELECT pg_is_in_recovery(), inet_server_addr();" >> "${LOG_DIR}/before.txt"

# 1. 부하 시작 (백그라운드)
echo "==> T+5s: pgbench 부하 시작 (5분, 32 connection)" | tee -a "${LOG_DIR}/timeline.log"
pgbench -h pg-haproxy -p 5000 -U bench bench \
    -c 32 -j 4 -T 300 -P 5 \
    > "${LOG_DIR}/pgbench.log" 2>&1 &
PGBENCH_PID=$!

sleep 30
echo "==> T+35s: 부하 안정화 확인" | tee -a "${LOG_DIR}/timeline.log"

# 2. 현재 primary 식별
PRIMARY_NODE=$(patronictl -c /etc/patroni/patroni.yml list -f json \
    | jq -r '.[] | select(.Role == "Leader") | .Member')
echo "==> 현재 primary: ${PRIMARY_NODE}" | tee -a "${LOG_DIR}/timeline.log"

# 3. T+60s: primary 강제 종료
FAIL_START=$(date +%s%3N)
echo "==> T+60s: ${PRIMARY_NODE} 강제 종료 (kill -9 postgres)" | tee -a "${LOG_DIR}/timeline.log"
ssh "${PRIMARY_NODE}" "sudo pkill -9 -f 'postgres: '"

# 4. 새 primary 등장 대기 + 타이밍 측정
echo "==> T+60s+: 새 primary 등장 대기" | tee -a "${LOG_DIR}/timeline.log"
NEW_PRIMARY=""
for i in $(seq 1 60); do
    NEW_PRIMARY=$(patronictl -c /etc/patroni/patroni.yml list -f json 2>/dev/null \
        | jq -r '.[] | select(.Role == "Leader") | .Member' || true)
    if [[ -n "${NEW_PRIMARY}" && "${NEW_PRIMARY}" != "${PRIMARY_NODE}" ]]; then
        FAIL_END=$(date +%s%3N)
        FAILOVER_MS=$((FAIL_END - FAIL_START))
        echo "==> 새 primary 등장: ${NEW_PRIMARY} (${FAILOVER_MS}ms)" | tee -a "${LOG_DIR}/timeline.log"
        break
    fi
    sleep 1
done

if [[ -z "${NEW_PRIMARY}" || "${NEW_PRIMARY}" == "${PRIMARY_NODE}" ]]; then
    echo "!! 60초 안에 페일오버 미완료. 수동 개입 필요." | tee -a "${LOG_DIR}/timeline.log"
    exit 1
fi

# 5. 애플리케이션 측 연결 회복 시간 측정
echo "==> HAProxy 라우팅 회복 대기" | tee -a "${LOG_DIR}/timeline.log"
ROUTING_START=$(date +%s%3N)
for i in $(seq 1 30); do
    ADDR=$(psql -h pg-haproxy -p 5000 -t -c "SELECT inet_server_addr();" 2>/dev/null \
        | tr -d ' \n' || true)
    if [[ -n "${ADDR}" ]]; then
        ROUTING_END=$(date +%s%3N)
        ROUTING_MS=$((ROUTING_END - ROUTING_START))
        echo "==> HAProxy 라우팅 회복: ${ADDR} (${ROUTING_MS}ms)" | tee -a "${LOG_DIR}/timeline.log"
        break
    fi
    sleep 1
done

# 6. 부하 완료 대기
wait ${PGBENCH_PID}
echo "==> pgbench 종료" | tee -a "${LOG_DIR}/timeline.log"

# 7. 사후 상태 캡처
echo "==> 사후 상태 캡처" | tee -a "${LOG_DIR}/timeline.log"
patronictl -c /etc/patroni/patroni.yml list > "${LOG_DIR}/after.txt"
psql -h pg-haproxy -p 5000 -c "SELECT pg_is_in_recovery(), inet_server_addr();" >> "${LOG_DIR}/after.txt"

# 8. 통과 기준 자동 검증
echo "==> 통과 기준 자동 검증" | tee -a "${LOG_DIR}/timeline.log"
PASS=true

if (( FAILOVER_MS > 30000 )); then
    echo "  FAIL: 페일오버 시간 ${FAILOVER_MS}ms > 30000ms 기준" | tee -a "${LOG_DIR}/timeline.log"
    PASS=false
fi

ERROR_COUNT=$(grep -c "error" "${LOG_DIR}/pgbench.log" || true)
if (( ERROR_COUNT > 100 )); then
    echo "  FAIL: pgbench error ${ERROR_COUNT}건 > 100건 기준" | tee -a "${LOG_DIR}/timeline.log"
    PASS=false
fi

REPLAY_LAG=$(ssh "${NEW_PRIMARY}" "psql -t -c 'SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) FROM pg_stat_replication;'" \
    | awk '{print $1}')
if [[ -n "${REPLAY_LAG}" && "${REPLAY_LAG}" -gt 1048576 ]]; then
    echo "  FAIL: 새 primary의 standby replay lag ${REPLAY_LAG} byte > 1MB" | tee -a "${LOG_DIR}/timeline.log"
    PASS=false
fi

if [[ "${PASS}" == "true" ]]; then
    echo "==> 훈련 통과" | tee -a "${LOG_DIR}/timeline.log"
else
    echo "==> 훈련 실패 — 위 항목 점검 필요" | tee -a "${LOG_DIR}/timeline.log"
fi
```

#### 통과 기준

훈련의 통과 기준은 명시적이어야 한다. 막연한 "잘 작동했다"는 평가가 가장 위험하다. 다음 항목들을 미리 정해 두고, 모두 통과할 때만 "PASS"로 본다.

| 항목 | 기준 | 측정 방법 |
|---|---|---|
| **페일오버 완료 시간(RTO)** | 30초 이내에 새 primary 등장 | Patroni leader 전환 시각 차 |
| **데이터 손실(RPO)** | 0 byte (동기 복제 가정) | 페일오버 직전 LSN과 새 primary 시작 LSN 비교 |
| **HAProxy 라우팅 회복** | 15초 이내 새 primary 라우팅 | `inet_server_addr()` 응답 |
| **pgbench 트랜잭션 오류율** | 1% 이하 (페일오버 구간 포함) | pgbench error 카운트 / 총 시도 |
| **새 standby 복귀 시간** | 5분 이내에 옛 primary가 standby로 재합류 | `pg_stat_replication`에 등장 |
| **모니터링 알람** | 페일오버 시작 60초 이내 PagerDuty/Slack 알람 발화 | 알람 로그 |
| **애플리케이션 헬스체크** | 60초 이내 모든 인스턴스 healthy 복귀 | 애플리케이션 health 엔드포인트 |

#### 사후 회고 — 30분 안에 끝낸다

훈련이 끝나면 바로 회고를 한다. 시간이 지나면 기억이 흐려진다. 30분 안에, 다음 세 가지를 정리한다.

- **무엇이 잘 됐는가**: 자동화가 의도대로 동작한 부분.
- **무엇이 안 됐는가**: 통과 기준 중 실패한 항목, 예상보다 오래 걸린 단계.
- **다음 분기까지의 개선 액션**: 책임자·기한 명시.

흔히 첫 훈련에서 드러나는 문제들을 미리 알려두면 마음의 준비가 된다.

- HAProxy의 `inter` 값이 너무 길어 라우팅 회복이 15초를 넘어선다 → `inter 2s fall 2 rise 1`로 단축 검토.
- pgbench가 페일오버 구간에 connection error를 수백 건 낸다 → 애플리케이션의 retry 로직 점검(`SQLSTATE 57P01` admin shutdown, `08006` connection failure 처리).
- 옛 primary가 자동으로 standby로 재합류 못 하고 timeline divergence가 발생 → `use_pg_rewind: true` 설정 확인, `pg_rewind`가 실행될 수 있도록 `wal_log_hints = on` 또는 data checksums 활성화 점검.
- etcd가 페일오버 직후 leader election에 5초를 쓴다 → etcd 노드 간 latency 점검, snapshot 크기 점검.
- 모니터링 알람이 발화 안 함 → Patroni의 callback으로 페일오버 이벤트를 Prometheus AlertManager로 푸시하는 hook 추가.

이 한 번의 훈련이 끝나면 깨닫게 된다. 페일오버 자동화는 "깔면 끝"이 아니라 "분기마다 정직하게 측정하고 개선하는 운영의 일부"라는 사실을. 한 번 훈련을 끝낸 팀과 한 번도 안 한 팀의 차이는, 새벽 세 시의 알람 앞에서 손이 어디로 가는가에서 갈린다.

#### 더 어려운 시나리오로 — 다음 분기들의 메뉴

첫 분기는 "primary 강제 종료"로 충분하다. 익숙해지면 분기마다 한 단계씩 시나리오를 어렵게 한다.

- **2분기**: AZ 단위 격리 — primary가 있는 AZ를 네트워크에서 분리. 다른 AZ로 페일오버되는지 검증.
- **3분기**: 분할 뇌(split-brain) 시뮬레이션 — primary와 etcd 사이 네트워크를 차단해 leader key 만료 유도, 옛 primary가 정상적으로 demote되는지 검증.
- **4분기**: 디스크 가득 참 시나리오 — primary 디스크를 95%까지 채워 read-only 모드로 가는지, 그때 페일오버가 도는지 검증.

매 분기 어렵게 하는 이유는, 진짜 사고는 우리가 예상한 형태로 안 오기 때문이다. 다양한 시나리오를 거친 팀일수록 처음 보는 사고에도 침착하게 손이 움직인다.

#### 회고에서 자주 나오는 실패 패턴들

훈련을 몇 분기 반복하다 보면 비슷한 실패 패턴이 보이기 시작한다. 미리 알아 두면 첫 훈련의 충격을 줄일 수 있다.

**"페일오버는 됐는데 애플리케이션이 30초간 에러를 쏟았다."** 가장 흔하다. 원인은 보통 두 가지가 겹친다. 첫째, HAProxy의 health check 주기가 길어 새 primary 인식이 느렸다. 둘째, 애플리케이션의 connection retry 로직이 부실해 첫 실패에 그대로 사용자에게 5xx를 던졌다. HAProxy 쪽은 `inter`를 줄이고, 애플리케이션 쪽은 transient error(특히 PostgreSQL의 `57P01 admin_shutdown`, `08006 connection_failure`, `08001 sqlclient_unable_to_establish_sqlconnection`)에 대해 최소 3회 지수 백오프 재시도를 박는 것이 합리적이다.

**"옛 primary가 standby로 못 돌아온다."** timeline divergence라 부르는 상황이다. 옛 primary가 살아 돌아왔을 때, 그 사이 새 primary가 받은 WAL과 옛 primary가 마지막에 갖고 있던 WAL의 history가 갈라져 있다. 이걸 합치려면 `pg_rewind`가 두 노드의 공통 조상 시점을 찾아 옛 primary의 변경을 되돌리고 새 primary의 WAL을 받아오는 과정이 필요하다. 이게 자동으로 돌게 하려면 `wal_log_hints = on` 또는 data checksums가 활성화돼 있어야 한다. 둘 다 없으면 `pg_rewind`가 실패하고 base backup부터 다시 받아야 한다 — 4TB 클러스터에선 끔찍한 일이다.

**"split-brain은 안 났는데 데이터가 일부 사라졌다."** 비동기 복제 상태에서 페일오버가 일어났거나, 동기 복제 설정이 의도와 달랐을 때 발생한다. 페일오버 직전 primary가 받은 트랜잭션 중 standby에 도착 못 한 것들이 그대로 사라진다. RPO 요구가 0인 시스템이라면 `synchronous_mode_strict: true`로 두고, standby가 모두 빠진 경우엔 쓰기가 막히는 동작을 받아들이는 편이 나을 수 있다. 무엇이 답인지는 시스템의 SLA에 달려 있다.

**"훈련 자체가 사고가 됐다."** 가장 슬픈 패턴이다. 운영 시간대에 훈련을 돌렸는데 페일오버가 의도대로 안 돼서 실제 서비스가 멈췄다. 그래서 처음 몇 분기는 무조건 비운영 환경에서, 익숙해진 뒤 운영 환경 점검 시간대에 시작하고, 그때도 반드시 "롤백 신호 한 마디면 사람이 손으로 멈춘다"는 안전망을 같이 걸어 둔다. 도구를 너무 신뢰해서 사람의 손을 빼는 순간이 가장 위험하다.

이 패턴들은 모두 한 번씩은 겪고 지나간다. 처음 훈련에서 모든 항목이 PASS면 오히려 훈련 시나리오가 너무 쉽지 않은지 의심해 보자. 적당히 실패하는 훈련이 가장 가치 있는 훈련이다.

## 20.7 v17 failover slot — logical replication까지 HA 안으로

20.6까지가 streaming replication 기반 HA의 이야기였다. 그런데 한 가지 빠진 게 있다. **logical replication slot은 HA에 들어오지 못했다.**

상황을 그려보자. 카카오 클린플랫폼처럼 PostgreSQL → Elasticsearch로 Debezium CDC 파이프라인을 운영한다고 해보자. Debezium은 PG의 logical replication slot에 연결돼 WAL 변경을 받아간다. 이 slot은 primary에만 있다. primary가 죽고 standby가 승격되면 — slot은 standby에 없으므로 사라진다. Debezium은 연결을 잃고, 새 primary에서 slot을 다시 만들어야 하고, 그 사이의 변경은 어떻게 따라잡을지 따로 고민해야 한다. CDC 파이프라인이 페일오버 한 번에 통째로 흔들린다.

v17 이전에는 이 문제의 답이 사실상 "수동"이었다. 페일오버 직후 운영자가 새 primary에 slot을 다시 만들고, Debezium의 시작 위치를 잘 맞춰서 다시 띄우고, 중간 변경분을 어떻게 처리할지 고민하는 작업이 따라붙었다. CDC를 안 쓰는 팀은 모르지만, CDC를 쓰는 팀에게 페일오버는 "본 DB의 페일오버 + CDC 파이프라인 재구축"이라는 이중의 사고였다. 끔찍한 일이다.

PostgreSQL 17이 이 문제에 답을 내놓았다. **failover slot** — logical replication slot이 standby로 자동 동기화된다. primary에서 slot을 만들 때 `failover = true` 옵션을 주면, 그 slot이 standby에서도 똑같이 유지된다.

```sql
-- v17 이상에서
SELECT pg_create_logical_replication_slot(
    'debezium_slot',
    'pgoutput',
    false,    -- temporary
    false,    -- two_phase
    true      -- failover
);
```

이렇게 만든 slot은 primary가 죽고 standby가 승격될 때 standby에서 그대로 살아 있다. Debezium은 새 primary에 재연결하면, 끊긴 위치 그대로 이어서 받기 시작한다. 페일오버가 CDC에게 사실상 투명해진다.

이게 작동하려면 standby 쪽에서 두 가지 파라미터가 켜져 있어야 한다.

- `sync_replication_slots = on`: standby가 primary의 failover slot을 주기적으로 가져와 자기에게 적용.
- `hot_standby_feedback = on`: standby가 자기가 보유 중인 slot 위치를 primary에 알려, primary의 WAL이 너무 일찍 삭제되는 걸 방지.

여기에 더해 primary 측에서는 `synchronized_standby_slots`로 "어느 standby가 동기화 대상인지"를 명시할 수 있다. 이 standby들로의 동기화가 끝난 뒤에야 primary가 logical decoding을 진행하게 만들어, slot이 항상 일관된 상태를 유지하도록 보장한다.

운영 관점에서 한 가지만 짚자. **failover slot이 켜져 있다고 모든 CDC 시나리오가 끝나는 건 아니다.** 다음을 따로 확인해 두자.

- **Debezium 측 재연결 동작**: Debezium 1.9 이상이 failover slot을 인식. 그 이하 버전이라면 별도 설정 또는 업그레이드가 필요.
- **publication과 subscription의 위치**: publication은 primary에만 있다. failover slot은 slot만 동기화하지 publication을 만들어주진 않는다. 새 primary에서도 같은 publication이 존재해야 하는데, publication 자체는 DDL이므로 logical replication 대상이 아니다. 보통은 양쪽 노드의 초기 셋업 단계에서 같은 publication을 만들어 두는 식으로 풀린다.
- **two_phase commit과의 상호작용**: two_phase = true로 만든 slot이 failover 가능한지, Debezium 같은 컨슈머가 그걸 어떻게 다루는지는 사용 도구별로 한 번 확인. 14장에서 다룬 logical decoding의 디테일이 같이 살아 있다.
- **페일오버 훈련 시나리오에 CDC 회복 검증 추가**: 20.6의 통과 기준에 "CDC 컨슈머가 N초 안에 끊긴 위치에서 이어서 받기 시작하는가"를 추가. 검증 없으면 v17 효과를 자랑하기만 하고 실제론 안 작동할 수 있다.

failover slot은 PG 17이 logical replication을 "진짜 production-ready"로 끌어올린 가장 큰 한 걸음이다. CDC, dual-write, multi-tenant 분리 같은 logical replication 기반 패턴을 쓰는 팀이라면, v17으로의 업그레이드가 단순한 minor 업그레이드가 아니다. CDC 운영의 한 차원이 바뀐다.

## 마무리

가용성은 도구가 아니라 운영의 결과다. Patroni를 깔든 pg_auto_failover를 깔든, 그 위에 HAProxy를 얹든 클라이언트 multi-host를 쓰든, 결국 검증은 "분기마다 일부러 죽이는" 훈련에서 갈린다. 한 번도 안 죽여본 클러스터는 사고 당일에 처음 죽는다.

이번 장에서 같이 짚은 것들을 다시 한 번 묶어보자.

- **streaming replication**은 모든 HA의 토대다. 동기·비동기의 선택은 RPO와 응답 지연 사이의 트레이드오프다. 동기 복제는 standby 두 대 + `ANY 1` 정족수가 가용성 함정을 피하는 패턴이다.
- **Patroni**는 대규모·자동화 환경의 표준이다. etcd 같은 합의 시스템과 REST API가 강점이다. 학습 곡선이 있다.
- **pg_auto_failover**는 단순함이 무기다. 작은 팀에게 빠른 첫 선택. 단, monitor 한 대의 SPoF는 정직하게 받아들여야 한다.
- **최소 3노드** — primary + standby 2대 + (가능하면) 다른 AZ 분산. 비용을 줄이려고 standby 한 대로 시작하면 거의 항상 후회한다.
- **라우팅 계층**은 PgBouncer + HAProxy + `/primary` health check 조합이 보편. 클라이언트 multi-host는 가벼운 첫 답이지만 기존 연결을 끊지는 못한다.
- **분기 페일오버 훈련**은 선택이 아니라 필수다. 스크립트·체크리스트·통과 기준을 미리 정해두고, 회고로 다음 분기를 준비한다.
- **v17 failover slot**은 logical replication까지 HA 안에 들어오게 만들었다. CDC 파이프라인을 쓰는 팀이라면 업그레이드의 가장 큰 동기다.

가용성 도구는 "사고가 안 나게 해주는 도구"가 아니라 "사고가 났을 때 우리 대신 결정을 내려주는 도구"라는 사실을 잊지 말자. 그 결정의 조건을 우리가 정확히 알고 있을 때만, 자동화는 우리 편이다. 모를 때는 자동화가 사고를 키운다.

다음 장은 connection pooling과 모니터링이다. 4장에서 "PG에는 풀러가 왜 필수인가"의 답을 봤다면, 21장에서는 "무엇을 어떻게 골라 어떻게 운영할 것인가"의 답을 찾는다. 그리고 모니터링 — pg_stat_statements부터 시작해 PG 클러스터의 옵저버빌리티를 한 단계씩 쌓아 올린다. HA 다음의 자연스러운 한 걸음이다.
