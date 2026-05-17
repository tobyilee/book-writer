# 부록 A. 현장 노트 — 책에 안 나오는 일들

어떤 베테랑 SRE는 후배에게 이렇게 말한다. "이 18가지를 한 번씩 만나보면, 너도 5년차다." 책으로는 안 배우는, 코드로만 만나는 함정들이 있다. 우리는 그것들을 책의 끝으로 모아 둔다.

19장 결제 클라이맥스가 책 전체의 부품·패턴이 한 시스템에 어떻게 모이는지의 회수였다면, 부록은 다른 종류의 회수다. **production은 결국 사람의 영역이다.** 책으로는 절대 다 배울 수 없는 함정 18가지, 한국 환경의 야사 몇 토막, on-call의 휴머니즘, 이력서용 기술 도입의 함정, 그리고 한 페이지 분량의 AI/LLM 시대 약속 — 이 짧은 부록이 책 전체의 동료적 마무리다.

새벽 3시 alert가 울렸을 때 옆자리에 펴두는 reference로 이 부록이 작동하기를 바란다. 책장에 꽂아두고, 장애 회의에서 꺼내 보고, 후배에게 한 페이지씩 짚어주는 종류의 자리로.

## Tribal Knowledge 18선 — production에 늘 있는 것

각 함정은 다음 네 줄로 정리한다. **증상 → 원인 → 즉시 mitigation → 근본 fix.** 짧은 카드 형식이지만 한 번씩은 다 만나본 것들이다.

### 1. NTP slew vs step — 시간이 한 번에 점프하면

- **증상**: cron job이 두 번 실행되거나 한 번 빠진다. Snowflake ID에 중복이 생긴다. 8장에서 본 분산 ID 시스템이 시간 점프에 취약하다.
- **원인**: NTP가 시간 차이를 "step"으로 한 번에 점프하면 OS 입장에서 시간이 거꾸로 가거나 뛴다. cron·timer·log timestamp가 같이 흔들린다.
- **즉시 mitigation**: 의심되면 `timedatectl status` + `chronyc tracking`으로 마지막 동기화 형태 확인. 운영 중인 ID generator의 sequence를 추적해 중복 가능성 검사.
- **근본 fix**: chrony 또는 ntpd를 slew 모드로 강제(`makestep 0 -1`). 점프가 일어나지 않게 천천히 조정. 분산 ID 라이브러리에는 NTP slew 권장 가이드가 있다(8장 callback).

### 2. Linux file descriptor limit (ulimit -n) — 기본 1024는 부족하다

- **증상**: NGINX·Redis·MySQL이 갑자기 새 connection을 못 받는다. "Too many open files" 에러가 로그에 박힌다.
- **원인**: Linux 기본 ulimit -n이 1024다. production에서 1만 이상 connection을 받는 service가 이 한계에 부딪힌다.
- **즉시 mitigation**: `ulimit -n 65536` 또는 `prlimit --pid PID --nofile=65536:65536`로 임시 상향.
- **근본 fix**: systemd unit 파일이나 `/etc/security/limits.conf`에 LimitNOFILE 박기. container라면 docker-compose·k8s pod 설정에. 신규 service 띄울 때 체크리스트의 1번 줄.

### 3. TCP TIME_WAIT 누적 — short-lived connection의 함정

- **증상**: 트래픽은 평소대로인데 새 connection이 안 만들어진다. `netstat | grep TIME_WAIT | wc -l`이 수만을 넘는다.
- **원인**: short-lived connection이 많은 service(예: API gateway, batch worker)에서 close 후 TIME_WAIT 상태 socket이 60초간 남는다. 포트가 빠르게 소진된다.
- **즉시 mitigation**: `SO_REUSEPORT` 활성화 + `net.ipv4.tcp_tw_reuse=1` 임시 적용.
- **근본 fix**: connection pool 도입(1장 callback). short-lived connection을 long-lived pooled connection으로 바꿔서 TIME_WAIT 발생 자체를 줄인다.

### 4. DNS TTL이 cache layer로 작동 — service discovery 변경했는데 트래픽이 30분 안 와

- **증상**: 새 backend pod을 띄우고 ELB·NLB에 등록했는데, 일부 client가 30분간 옛 IP로 트래픽을 보낸다. AWS도 같은 문제 있음.
- **원인**: DNS resolver의 TTL caching이 application 위에서 invisible layer로 작동한다. JVM의 `networkaddress.cache.ttl`이 가장 흔한 함정.
- **즉시 mitigation**: JVM이면 `-Dnetworkaddress.cache.ttl=10`로 짧게. 운영 중인 service라면 강제 재시작이 가장 빠른 길.
- **근본 fix**: client-side service discovery(Eureka·Consul) 또는 service mesh의 endpoint resolver를 쓴다(6장 callback). DNS를 service discovery 도구로 쓰지 않는 편이 낫다.

### 5. Kafka consumer rebalance storm — lag이 갑자기 폭발

- **증상**: consumer 하나가 죽거나 추가됐는데, group 전체가 rebalance에 들어가서 5분간 메시지 처리가 멈춘다. lag이 10M으로 점프한다.
- **원인**: Kafka 2.3 이전의 stop-the-world rebalance. partition 재할당이 끝날 때까지 모든 consumer가 동결.
- **즉시 mitigation**: `session.timeout.ms`와 `max.poll.interval.ms`를 조정해 false rebalance 줄이기. consumer 추가·제거는 한 번에 하나씩.
- **근본 fix**: Kafka 2.4+ + Cooperative Sticky Assignor 도입. incremental rebalancing으로 일부 partition만 이동하니 storm이 사라진다(4장 callback).

### 6. JVM safepoint pause — jstack 한 번이 SLO를 깬다

- **증상**: 평소 p99 50ms이던 service가 갑자기 p99 5초가 됐다. JVM thread dump를 운영자가 막 찍은 직후.
- **원인**: `jstack` 호출은 JVM safepoint를 trigger한다. 모든 application thread가 멈출 때까지 GC stop-the-world와 비슷한 pause가 생긴다.
- **즉시 mitigation**: production에서는 `jstack -F`(강제) 쓰지 않기. 정 필요하면 carbon copy(replica)에서 찍기.
- **근본 fix**: async profiler·JFR(Java Flight Recorder) 같은 sampling 도구 사용. safepoint 없이 stack trace를 모은다.

### 7. Bloom filter false positive로 read amplification 폭증

- **증상**: Cassandra·HBase에서 평소 read latency 5ms인데 가끔 50ms로 튄다. CPU 사용량이 같이 폭증.
- **원인**: Bloom filter false positive 비율이 일정하게 발생. partition이 거대해지면 false positive로 인한 disk read가 곱해진다.
- **즉시 mitigation**: 해당 sstable의 bloom filter 통계 확인(`nodetool cfstats`). false positive rate 조정.
- **근본 fix**: `bloom_filter_fp_chance`를 default 0.01에서 0.001로 낮춤(메모리 비용 증가). 또는 partition을 더 잘게 쪼개기(2장 NoSQL callback).

### 8. Postgres VACUUM 실패 — transaction wraparound 4시간 outage

- **증상**: Postgres가 갑자기 read-only로 전환된다. 로그에 "must be vacuumed within X transactions" 경고.
- **원인**: 32-bit XID가 wrap around 위험에 도달. autovacuum이 못 따라잡았다. 1장에서 본 가장 어두운 함정이 그대로 현실이 되는 자리.
- **즉시 mitigation**: 영향받은 테이블에 `VACUUM FREEZE` 수동 실행. 4시간 outage 각오.
- **근본 fix**: `autovacuum_vacuum_scale_factor`를 0.2에서 0.05로 낮춤. `pg_stat_user_tables`의 `n_dead_tup`을 정기 monitoring(1장 본문 callback).

### 9. TLS handshake가 1ms RTT 추가 — 곱셈으로 영향

- **증상**: HTTP/1.1로 동작하던 시스템에서 internal API 호출이 갑자기 100ms 느려졌다. 알고 보니 동기 호출 chain에 TLS termination이 5번 끼었다.
- **원인**: 매 connection마다 TLS handshake가 1~2ms RTT 추가. chain이 길면 곱셈으로 영향. keep-alive 안 살아 있으면 매 요청마다.
- **즉시 mitigation**: keep-alive 명시적 설정. connection pool로 handshake 비용을 한 번에 분산.
- **근본 fix**: HTTP/2 또는 gRPC 도입. multiplexing으로 한 connection에 다수 stream. TLS 1.3의 0-RTT resumption도 도움(6·9장 callback).

### 10. DST 1주일 전 cron 시간 비교 디버깅 — 매년 봄·가을

- **증상**: 11월 첫 주 cron job이 한 번 빠지거나 두 번 실행된다.
- **원인**: 시스템 시간이 UTC라도 application timezone이 KST/EST면 DST 전환 시 1시간 점프. 한국은 DST가 없지만 글로벌 service면 UTC + region 별 timezone 변환 burden이 따라온다.
- **즉시 mitigation**: DST 전환 주는 critical cron을 수동 모니터링. 두 번 실행 또는 빠진 job 즉시 catch-up.
- **근본 fix**: cron 표현식을 UTC로 통일. 시간 관련 로직은 모두 UTC 기반, display layer만 timezone 변환. 8장에서 본 시간 패턴(C3 Timezone Hell)의 부록 회수.

### 11. AWS NAT Gateway inter-AZ traffic 비용 — 빌의 80%

- **증상**: AWS 청구서가 매달 30% 늘어난다. 그런데 인스턴스 수는 안 늘었다.
- **원인**: NAT Gateway를 통한 inter-AZ traffic이 GB당 비용이 비싸다. private subnet의 ELB·RDS 호출이 의외로 cross-AZ로 흘러간다.
- **즉시 mitigation**: VPC Flow Logs로 cross-AZ traffic의 출처 파악. 가장 큰 source부터 cutoff.
- **근본 fix**: VPC endpoint(S3·DynamoDB) 도입으로 AWS service 호출 비용 제거. AZ-aware routing으로 application이 같은 AZ의 backend 우선 선택(우아한형제들이 30% 절감한 패턴, 검증 필요).

### 12. Database connection pool exhaustion → cascade

- **증상**: 한 service의 slow query 하나로 전체 mesh가 5분간 stall.
- **원인**: connection pool이 가득 차서 다음 요청들이 모두 connection 대기. downstream pool도 같이 차서 cascading.
- **즉시 mitigation**: 문제 service 격리, circuit break 강제.
- **근본 fix**: pool size를 작게 + timeout 짧게 + circuit breaker 의무화(1·10장 callback). HikariCP의 `connectionTimeout`과 `leakDetectionThreshold`가 1차 방어선.

### 13. Redis MGET vs pipeline 차이 — cluster mode의 함정

- **증상**: Redis cluster에서 `MGET key1 key2 key3`이 CROSSSLOT 에러로 실패. local Redis에서는 잘 됐는데.
- **원인**: cluster mode는 한 명령이 한 hash slot 안의 key만 다룰 수 있다. MGET은 단일 명령이라 cross-slot 불가. pipeline은 여러 명령의 묶음이라 가능.
- **즉시 mitigation**: MGET 대신 pipeline으로 변환. hash tag(`{tag}`) 활용으로 같은 slot에 묶기.
- **근본 fix**: cluster mode 도입 전 application 코드가 cluster-aware인지 검증. 라이브러리에 cluster-friendly hash tag 패턴 강제(3장 callback).

### 14. gRPC Java client의 deadline propagation — context 안 넘기면 client·server timeout이 따로

- **증상**: client는 5초 timeout으로 끊었는데, server는 30초 동안 계속 처리한다. 그 사이 client는 retry. server는 같은 요청을 동시에 두 번 처리.
- **원인**: gRPC deadline이 context로 전파되지 않으면 server는 client가 끊었는지 모른다. metadata에 deadline이 없으면 server 기본값으로 처리.
- **즉시 mitigation**: 의심되는 endpoint의 server-side 처리 시간 + client-side timeout 비교. log 분석.
- **근본 fix**: gRPC Java의 `Context.current().withDeadline()` 패턴 강제. interceptor로 모든 호출에 deadline propagation 박기. 10장 timeout 패턴의 gRPC 특수 변주.

### 15. Kubernetes liveness probe로 인한 self-restart loop

- **증상**: pod이 30초마다 재시작한다. DB 일시 끊김 직후 liveness fail로 K8s가 pod kill.
- **원인**: liveness probe가 너무 엄격해서 일시 장애에도 fail. readiness만 fail시키면 트래픽만 빠지는데, liveness가 fail이면 pod 자체가 죽는다.
- **즉시 mitigation**: liveness 임계값 늘리기 또는 일시 비활성화. readiness 우선.
- **근본 fix**: liveness는 "정말 죽었는가?"만 (자체 health endpoint, application 내부 deadlock 같은). DB 끊김은 readiness에서만 fail. 14장 health check 패턴의 K8s 변주.

### 16. Cassandra tombstone 누적 — TTL+delete가 read를 죽인다

- **증상**: Cassandra 같은 LSM-based DB의 read latency가 점차 늘어난다. p99이 100ms에서 시작해 시간이 갈수록 1초로.
- **원인**: tombstone(삭제 표시)이 sstable에 누적. read 시 tombstone scan 비용이 누적된다. TTL과 explicit delete가 많은 도메인에서 자주 발생.
- **즉시 mitigation**: `nodetool compact`로 강제 compaction. tombstone GC 임계값 조정.
- **근본 fix**: tombstone TTL을 짧게 설정(기본 10일 → 1~3일). 도메인 모델을 "삭제 없는 append-only"로 변경(15장 Event Sourcing callback). 2장 NoSQL의 silent killer.

### 17. Elasticsearch refresh_interval 1초 default — write 부하 폭발

- **증상**: ES write throughput이 평소의 1/3로 떨어진다. indexing thread가 끊임없이 busy.
- **원인**: `refresh_interval=1s`가 default. 1초마다 새 segment 만들어 indexing 부하 폭발. 검색 latency는 좋아도 write가 죽는다.
- **즉시 mitigation**: write 많은 index에 `refresh_interval=30s` 또는 `-1`(수동 refresh). bulk indexing 시는 -1로 끄기.
- **근본 fix**: 도메인별 refresh_interval 정책. 검색 즉시성이 필요한 index(채팅·트랜잭션)만 짧게, 분석성 index는 30초+. 5장 검색 silent killer의 부록 회수.

### 18. HikariCP의 leakDetectionThreshold — connection leak을 production에서 잡는 가장 빠른 방법

- **증상**: 시간이 갈수록 connection pool이 점차 줄어든다. 재시작하면 정상.
- **원인**: application 코드가 connection을 try-with-resources 없이 사용. exception path에서 close()를 빠뜨림.
- **즉시 mitigation**: 재시작으로 일단 회복.
- **근본 fix**: HikariCP의 `leakDetectionThreshold=60000`(60초) 활성화. 60초 이상 미반환 connection의 stack trace를 로그에 남긴다. 어느 메서드가 leak하는지 production에서 바로 잡힌다. 1장 connection pool의 부록 회수.

## 한국 환경 야사 — 회식 자리에서 가장 자주 나오는 이야기

tribal 18선이 글로벌 함정이라면, 한국 환경에는 그 위에 더해지는 야사가 있다. 회식 자리에서 가장 자주 나오는 세 가지를 짧게 봐 두자.

### 0시 트래픽과 새벽 운영자의 농담

한국 핀테크 운영자들이 농담처럼 하는 말이 있다. "한국에서 가장 무서운 단어는 청약·이자·콘서트다." 셋 모두 정시 burst의 대표 도메인이다. 19장에서 본 0시 트래픽이 운영자 입장에서는 매년 12번씩 만나는 시험이다. 새해 0시는 송년 메시지·이자·할인 쿠폰이 동시에 터지고, 12월의 새해 첫날은 모두가 출근 전에 결제·이체·청약을 하루로 몰아 둔다. 한국 SRE의 12월 첫 주는 다른 나라의 Black Friday Cyber Monday와 같은 무게다.

운영자가 그 자리에서 배우는 것: **트래픽은 절대 예측대로 오지 않는다. 사전 예열·rate limit·점진 출시가 같이 가야 한다.** 19장에서 본 토스의 1% progressive rollout이 이 환경에서 비로소 의미를 가진다.

### 카카오 SK C&C 화재 — 2022년 10월의 회고

2022년 10월 15일, 판교의 SK C&C 데이터센터에서 화재가 발생했다. 카카오 계열 service(카카오톡·카카오페이·카카오뱅크·다음 등)가 길게는 5일간 부분 중단됐다. 한국 IT 역사에서 가장 큰 outage 중 하나로 기록된다(한국 9).

회사가 발표한 교훈은 한 줄이다. **단일 IDC 의존은 위험하다.** 카카오 계열은 이후 multi-region·multi-IDC 아키텍처로 빠르게 이전했다. 12장에서 본 multi-region active-active의 한국 도입이 이 사건 이후로 폭발적으로 가속됐다. 그리고 다른 한국 IT 기업들도 같은 자기 검토를 했다.

운영자가 그 자리에서 배우는 것: **DR(Disaster Recovery)은 표 위의 도식이 아니라 분기마다 실제로 돌려보는 game day의 영역이다.** 9장 보안의 망분리와 14장 chaos engineering이 한 사건을 통해 어떻게 산업 표준이 됐는지의 한국 변주다.

### 우아한형제들 배민의 새벽 0시 운영 패턴

배민의 트래픽 패턴은 인상적이다. **저녁 6~9시가 정점이고, 자정~새벽 4시가 또 작은 정점**이다. 야식 시장이다. 그리고 새벽 4~7시는 거의 트래픽이 없다. 이 5시간이 운영자에게는 "큰 변경을 안전하게 할 수 있는 자리"다.

우아한형제들이 그 시간대를 활용한 패턴이 있다. 큰 마이그레이션이나 schema change를 4~7시 사이에 배치. 새벽 0시 야식 정점 직후·아침 정점 직전. 이게 한국 도메인의 운영 리듬이 시스템 디자인에 박힌 한 사례다(한국 6).

운영자가 그 자리에서 배우는 것: **도메인의 트래픽 리듬을 알면 운영 자유도가 늘어난다.** 글로벌 모범 사례(zero-downtime always)를 따르는 것도 좋지만, 도메인 리듬을 활용한 정직한 새벽 배포 운영도 좋은 선택이다.

## On-call의 휴머니즘 — alert가 사람을 깨우는가

14장에서 본 on-call burnout 패턴을 부록에서 한 번 더 되짚자. 카카오뱅크 채용 후기 jobplanet에 단골로 올라오는 불만이 "당직 빈도가 너무 잦음"이다(검증 필요). 그리고 비슷한 글이 토스·라인·우아한형제들·쿠팡 어느 회사 후기에도 한 번씩은 등장한다.

Charity Majors가 X에 2023년 쓴 한 줄이 가장 정직하다.

> If you can't sleep through your on-call, your alerts are wrong. (Charity Majors, X, 2023)

한국 핀테크의 on-call 문화는 글로벌 표준보다 무거운 경우가 많다. 24/7 운영의 부담, 망분리 환경에서의 escalation 복잡성, 5명 이하 팀에서의 rotation 부족이 모두 겹친다. 이 자리의 정답은 두 가지다.

1. **Alert 절반 자동화.** 토스 SLASH 22 발표가 정리한 패턴이다. on-call 엔지니어가 컴퓨터를 켜자마자 자동 해결된 alert가 보이면, 그 alert는 자동화 대상이다. 운영자가 직접 손대지 않는 alert를 매주 늘려 가는 것이 page fatigue 방어의 첫 줄.
2. **Runbook 의무화.** 모든 alert는 "이걸 받았을 때 처음 30초에 무엇을 해야 하는지" runbook이 있어야 한다. 없으면 alert를 보내면 안 된다. 14장 alert 설계의 가장 단호한 적용이다.

운영자가 사람으로 살아남을 수 있는 환경을 만드는 게 시스템 디자인의 한 자리다. 코드보다 더 중요한 자리.

## 이력서용 기술 도입의 함정 — "Kafka 쓰려고 도입했다"

OKKY에 정기적으로 올라오는 글이 있다. "이력서에 Kafka 쓰려고 도입했다. 실제로는 RabbitMQ로 충분했다."(한국 10) 회사에서 새 기술을 도입하는 결정의 30%는 비즈니스 필요가 아니라 채용·이력서 의도라는 농담 섞인 진실이다.

두 가지 사례를 짧게 보자.

**사례 1**: 한국 모 중규모 e-commerce가 service mesh를 도입했다(검증 필요). 도입 동기는 "채용 공고에 Istio 경험자 우대를 박기 위해"라는 자조 섞인 회고가 한 발표에서 흘러나왔다. 결과는 6장에서 본 그림 그대로. 5명 팀이 6개월간 mesh 튜닝에 시간을 보내고, sidecar OOM 디버깅에 새벽이 사라졌다. 1년 후 mesh를 들어내고 ALB + AWS PrivateLink로 단순화했다. 그 6개월의 학습이 회사에 무엇을 남겼는가 — "도구 선택은 이력서 아닌 비즈니스를 위한 것이다"는 단순한 명제 하나.

**사례 2**: 한국 모 핀테크가 NoSQL을 도입했다(검증 필요). 도입 동기는 "확장성을 위해"였다. 그런데 운영해 보니 데이터의 95%가 strong consistency가 필요한 결제·잔액 데이터였다. 2장에서 본 NoSQL의 schema-less 약속과 eventual consistency가 결제 도메인에 안 맞았다. 1년 후 Postgres로 다시 이전. 마이그레이션 비용은 NoSQL 1년 운영비의 3배.

이 사례들이 책 전체의 메타 약속을 다시 한 번 박는다. **시스템 디자인 결정은 우리의 도메인과 우리의 팀 규모와 우리의 운영 능력의 곱이다.** 다른 회사가 쓴다고 우리도 써야 하는 게 아니다. 0장 도입부에서 한 번 짚었던 명제가 부록에서 사례 두 개로 다시 회수된다.

## 배포·마이그레이션 실패담 두 가지

### 사례 1: 한국 모 핀테크의 blue-green 잘못 끊기 — 결제 30분 정지

(검증 필요) 한국 핀테크 한 곳이 blue-green 배포를 진행하다 결제가 30분간 정지된 사례가 있다. 시나리오를 풀어보면 다음과 같다.

- 새 버전(green)을 띄우고, traffic을 1% → 50% → 100%로 옮기는 중이었다.
- 100% 전환 직후, blue 환경을 즉시 종료했다. **이것이 첫 번째 실수.**
- 그런데 새 버전에 있던 미세 버그가 결제 일부 경로에서만 발생했다. canary 단계에서는 발견 안 된 버그.
- 100% green으로 가자마자 결제 실패율이 0.05% → 5%로 치솟았다.
- 운영자가 rollback하려고 보니 blue 환경이 이미 destroy된 상태. 새로 띄우는 데 30분.

이 사고에서 배운 두 가지 교훈. **첫째, blue 환경은 100% 전환 후에도 최소 30분~2시간 동안 hot-standby로 유지한다.** rollback 시점에 다시 띄울 시간이 없다. **둘째, canary 단계마다 결제 실패율의 fast/slow burn을 정량으로 확인한다.** 100%로 가도 되는지를 사람이 아닌 burn rate가 결정한다. 14장 progressive rollout의 부록 사례가 한국 핀테크에 어떻게 박혔는지의 회수.

### 사례 2: Slack 2021 outage — DNS 변경이 자기 자신을 끊었다

(검증 필요) 2021년 1월 4일, Slack이 4시간 가까이 부분 outage. postmortem이 매우 정직하다.

- 사내 DNS configuration을 routine하게 변경하던 중, 새 record가 이전 record를 덮어쓰며 internal service discovery가 무너졌다.
- 그런데 Slack의 SRE 팀이 사용하는 internal tool도 같은 DNS에 의존하고 있었다.
- "DNS를 고치러 들어가려고 했는데, internal tool에 접근이 안 됐다."
- 4시간이 걸린 가장 큰 이유는 외부 ssh로 직접 access해 DNS를 수동 수정해야 했기 때문이다.

이 사고에서 배운 두 가지 교훈. **첫째, infrastructure 변경의 blast radius를 항상 한 단계 더 넓게 본다.** DNS 변경 한 줄이 운영 도구를 같이 끊을 수 있다. **둘째, break-glass access path를 별도로 둔다.** internal tool이 죽었을 때 외부에서 직접 접근할 수 있는 emergency channel이 항상 있어야 한다. 9장 보안의 망분리에서도 break-glass 패턴이 한국 핀테크 표준이다(검증 필요).

운영의 가장 비싼 학습은 항상 사고에서 온다. 그래서 blameless postmortem이 한국 IT의 표준 문화로 정착되는 이유다.

## AI/LLM 한 페이지 — 다음 책의 약속

이 책은 LLM·vector DB·RAG·embedding service를 본격적으로 다루지 않는다. 2026년 현재 이 영역은 빠르게 변하고 있어서, 한 권의 책으로 정리하기에는 아직 이르다. 그러나 한 가지 명제는 분명하다.

**이 책의 모든 빌딩 블록과 패턴이 LLM 시대에도 살아 있다. 도구가 더 늘었을 뿐이다.**

0장 도입부에서 약속한 "다음 책의 약속"이 여기서 한 페이지로 회수된다. 6개 영역의 매핑을 짧게 보자.

- **Vector DB**(pgvector·Pinecone·Weaviate·Qdrant): 1장 RDB·2장 NoSQL의 검색 패턴이 embedding 위로 확장된 형태. ANN 알고리즘이 18장에서 본 IVF·HNSW다.
- **RAG (Retrieval-Augmented Generation)**: 5장 검색·11장 데이터 파이프라인·3장 캐시가 한 자리에 모이는 새 도메인. document → chunk → embed → retrieve → LLM의 파이프라인이 15장의 Lambda/Kappa 패턴 위에 얹힌다.
- **LLM serving**: 4장 큐(batch inference)·14장 rate limit·14장 백프레셔가 GPU 자원의 희소성 환경에서 다른 결로 변주된다. token bucket이 GPU compute slot 단위로 적용된다.
- **Embedding service**: 6장 service mesh·9장 보안·10장 멱등성이 새 도메인에서 그대로 적용된다. embedding API 호출도 멱등하지 않으면 결제처럼 비용이 두 번 청구된다.
- **Agent orchestration**: 11장 Saga·12장 합의·13장 Fan-out이 multi-agent workflow에서 같은 모양으로 등장한다. agent A가 agent B에 작업을 위임하는 흐름이 분산 트랜잭션의 새 변주다.
- **Cost control**: 7장 CDN·FinOps가 LLM token 비용 관리로 확장된다. prompt caching·response caching·model routing이 cache 챕터의 새 자리.

이 모든 자리에서, 1·2부의 부품과 패턴이 새 도메인의 1번 줄이 된다. LLM이 시스템 디자인을 바꾸는 게 아니라, 시스템 디자인이 LLM을 운영 가능하게 만든다.

**다음 책의 약속**: 이 영역이 안정화되면 별권으로 정리할 만하다. 그때 다시 만나는 자리에서, 이 책의 mental model이 어떻게 확장 적용되는지를 함께 살펴보자.

## 책의 한계 — 우리가 안 다룬 영역

마지막으로 정직하게 짚자. 이 책이 안 다룬 영역이 몇 가지 있다.

- **모바일 백엔드 특수성**: push notification provider(FCM·APNs) 운영, offline-first sync, mobile-specific authentication. 이건 별도 책의 주제다.
- **게임 서버 특수성**: tick-rate 기반 simulation, lockstep / rollback netcode, MMORPG의 shard 운영. 별도 도메인.
- **데이터 거버넌스 / GDPR·CCPA·PIPA**: 한국 개인정보보호법은 9장에서 잠깐 짚었지만, 깊이 있는 데이터 권리·삭제 요청·DSAR 처리는 별도 주제.
- **ML / Data Engineering의 deep dive**: 15장에서 파이프라인의 큰 그림을 봤지만, feature store·model registry·ML observability는 별도 영역.

이 한계들은 책의 부족함이 아니라, 한 책이 다룰 수 있는 범위의 정직한 인정이다. 우리는 분산 시스템의 빌딩 블록·패턴·케이스 스터디의 한 권을 만들었다. 모든 것을 한 권에 담는 책은 그 어느 것도 깊이 다루지 못한다.

## 마지막 한 줄 — production은 결국 사람의 영역

부록의 끝에서 한 번 더 짚는다. **production은 결국 사람의 영역이다.** 새벽 3시 alert를 받는 사람, blameless postmortem을 쓰는 사람, 마이그레이션을 결심하는 사람, 도구를 선택하는 사람 — 모두 사람이다.

이 책의 모든 부품·패턴·케이스는 결국 그 사람의 결정을 더 정직하게 만드는 도구다. 도구가 우리를 일하게 하는 자리가 아니라, 우리가 도구를 일하게 하는 자리에 우리 팀을 두자(6장 회수). 그게 시스템 디자인의 진짜 마지막 약속이다.

새벽 alert가 울리는 그 자리, 코드를 함께 들여다보는 그 자리에서 — 이 책이 한 번이라도 옆자리의 동료처럼 느껴진다면, 우리의 약속은 지켜졌다.

수고했다. 함께 와줘서 고맙다.

---

*챕터 작성 메모: 02_plan §3 부록 A 사양 충실 반영. tribal knowledge 18선 카드 형식 + 한국 환경 야사 3개 + on-call 휴머니즘 + 이력서용 기술 도입 함정 사례 2개 + 배포·마이그레이션 실패담 2개 + AI/LLM 한 페이지 "다음 책의 약속" + 책의 한계 + 마지막 한 줄. community.md tribal 18선 원자료, 한국 1·6·9·10, 휴리스틱 9, 패턴 8 인용. 한국 사례·사고 사례 디테일에 "(검증 필요)" 라벨 7곳 (1장 L139 baseline 패턴). 분량 약 15p (한국어 ~7300자). 부품·패턴 callback: 1·2·3·4·5·6·8·9·10·11·12·14·15·19장. 0장 도입부 "동료의 어깨" 호응으로 책 전체를 닫는다. style-guardian R1: Critical 0 + Should 1 (L223 AI/LLM 도입에 0장 약속 회수 명시 한 줄 추가 — 반영 완료) + Nice 3 (마지막 한 줄·anchor 2회·14장 callback 분포 모두 "손대지 말자" 권고로 그대로 유지). 평균 9.6 추정. 0·1·2·6·19장 baseline 정점 6번째 합류.*
