# 16장. 채팅 시스템 — Discord·LINE·당근·Slack

Discord 엔지니어가 어느 날 사내 블로그에 한 줄을 올렸다. "We had a single message that was getting requested 30,000 times per second. Our database was suffering." 메시지 하나가 시스템 전체를 위협한다. 인기 채널의 누군가가 농담 한 줄을 던졌고, 그 한 줄을 모두가 동시에 본다. 같은 row가 초당 3만 번 read되는 그림 — 단순한 KV조회처럼 들리지만, partition 하나가 그 부하를 받기 시작하면 cluster 전체가 휘청거린다.

채팅 시스템은 듣기에 평범하다. 메시지 보내고, 받고, 저장하고, 보여준다. 그런데 운영해 보면 가장 잔인한 시스템 중 하나다. **메시지 1조 건이 쌓이는 시스템은 무엇을 양보했고, 무엇을 지켜냈는가** — 이 질문에 답할 수 있어야 채팅 시스템을 안다고 말할 수 있다.

3부 케이스 스터디의 첫 챕터로 채팅을 고른 이유가 있다. 채팅은 1·2부에서 배운 부품과 패턴이 거의 모두 한 시스템 안에 등장한다. 2장 NoSQL의 hot partition, 3장 캐시의 stampede, 4장 큐의 fan-out, 9장 보안의 token 인증, 13장 sharding, 14장 관측성·on-call — 모두 채팅의 어느 자리에서 다시 만난다. 1·2부의 학습이 한 도메인에서 어떻게 동시에 쓰이는지를 보는 첫 자리다.

## 도메인이 요구하는 5가지 — ordering·durability·history·real-time·fan-out

채팅 시스템 설계는 도메인 요구 5가지의 정의에서 시작한다. 한 줄로 줄이면 다음과 같다.

- **Ordering**: 같은 채팅방 안에서 메시지 순서는 결코 뒤바뀌면 안 된다. 8장에서 본 시간·순서 문제가 채팅 도메인의 1번 줄이다.
- **Durability**: "보낸 메시지가 사라졌다"는 채팅 시스템의 가장 큰 죄다. 한 번 ack한 메시지는 잃지 않는다.
- **History**: 사용자는 1년 전 메시지도 검색해서 본다. cold data가 hot data의 100배 이상이다.
- **Real-time delivery**: 메시지 보낸 사람이 손가락을 떼는 순간 받는 사람 화면에 떠야 한다. p50 100ms 이내가 사용자 체감 기준선.
- **Fan-out**: group chat에서 메시지 하나가 1000명에게 동시에 가야 한다. 1조 건 stored = N조 건 delivered.

이 5가지가 서로 충돌한다. Ordering을 지키려면 single-leader가 편하지만, fan-out과 real-time을 위해서는 horizontal scale이 필요하다. Durability를 위해서는 WAL을 강제해야 하지만, real-time을 위해서는 sync write가 부담된다. 그래서 채팅 시스템 설계는 **5축의 trade-off 어디에 점을 찍을지**의 문제다.

Discord·LINE·당근·Slack은 각자 다른 자리에 점을 찍었다. 이제 네 시스템이 어디에 무엇을 양보했는지를 차례로 살펴보자.

## WebSocket connection — 듣기에 단순하지만 운영하면 잔인하다

채팅의 첫 번째 기술 결정은 어떤 transport로 메시지를 보내는가다. HTTP polling? Long polling? Server-Sent Events? 정답은 명확하다. **WebSocket이다.** 양방향 + 낮은 latency + 1억 단위 동시 connection을 운영 가능하다.

그런데 WebSocket이 운영하기 시작하면 채팅 시스템의 가장 골치 아픈 자리가 된다. 상황을 가정해보자. 사용자 1억 명이 동시 접속해 있다. server pod 하나가 떨어진다. 그 pod이 들고 있던 1만 connection이 한꺼번에 다른 pod으로 reconnect 시도를 한다. reconnect storm이 시작되면 다른 pod도 OOM kill되기 시작한다. 끔찍한 일이다.

LINE이 이 자리를 어떻게 풀었는지가 인상적이다. LINE Engineering blog의 messaging hub 시리즈가 정리해준다(W30).

> connection-manager (WebSocket) ↔ message-router (gRPC) ↔ Kafka 큐 (LINE Engineering, 2022)

WebSocket connection을 받는 pod(connection-manager)과 비즈니스 로직을 처리하는 pod(message-router)을 분리했다. connection-manager는 connection의 상태와 user identity만 관리한다. 메시지가 들어오면 gRPC로 message-router에 던지고, Kafka로 흘려보낸다. **WebSocket의 stateful 책임과 메시지 처리의 stateless 책임을 분리한 것**이다.

이렇게 분리하면 무엇이 좋은가? message-router를 무중단으로 배포할 수 있다. WebSocket connection은 connection-manager가 들고 있고, message-router는 stateless라 rolling deploy가 자유롭다. 한쪽이 죽어도 다른 쪽은 살아있다. resilience 패턴이 두 layer로 분리된 셈이다.

물론 한 가지 함정이 있다. LINE이 발표에서 정직하게 풀어놓은 실패담이다.

> Apache HTTP client 라이브러리 버전 업그레이드 한 번으로 throughput이 1/3로 떨어진 적이 있다. (LINE Engineering, W30)

라이브러리 한 줄 업그레이드가 메신저의 처리량을 1/3로 만든다. 다른 시스템 같으면 한 번에 못 발견할 수도 있었을 것이다. 채팅처럼 latency·throughput에 민감한 도메인이라 빠르게 잡혔다. 잊지 말자. WebSocket 시스템은 의존성 한 줄도 검증 없이 올리면 안 된다. 14장의 관측성 패턴 — p99 latency·throughput·error rate — 가 매일 신뢰의 1차 신호다.

## Discord 마이그레이션 — Cassandra에서 ScyllaDB로 가는 9일

채팅 시스템 케이스 스터디에서 가장 인기 있는 deep dive가 Discord의 Cassandra → ScyllaDB 마이그레이션이다. 숫자가 인상적이다(W21, 자료 4.1).

| 항목 | Cassandra (before) | ScyllaDB (after) |
|------|---------------------|--------------------|
| 노드 수 | 177 | 72 |
| p99 read latency | 40~125ms | 15ms |
| p99 write latency | 5~70ms | 5ms |
| 운영자 부담 | GC pause로 새벽 page 잦음 | GC 없음, page 격감 |

왜 노드가 절반 이하로 줄었는데 latency가 더 좋아졌는가? 두 가지 이유다.

**첫 번째, JVM GC를 떼어냈다.** Cassandra는 JVM 기반이라 GC pause를 피할 수 없다. p99에서 100ms 안팎의 stop-the-world가 정기적으로 찍힌다. ScyllaDB는 C++로 작성됐고 shared-nothing per-core 모델이라 GC가 없다. p99이 깨끗하게 떨어진다.

**두 번째, 더 중요한 결정 — Rust로 작성한 data services layer를 추가했다.** 이 layer가 application과 ScyllaDB 사이에 끼어서 한 가지 일을 한다. **Request coalescing.** Discord 글이 직접 인용한다.

> Request coalescing is an important responsibility to avoid multiple database calls when many users request the same message. (Discord Engineering, W21)

상황을 다시 떠올려보자. 인기 채널의 한 메시지가 초당 3만 번 read된다. 만약 모든 read가 ScyllaDB까지 내려간다면 그 partition은 즉시 hot이 된다. data services가 그 앞에 서서 **같은 메시지에 대한 1000개의 동시 request를 1개의 DB call로 묶어서** 보낸다. 응답이 오면 그 1000개에 fan-out한다. 같은 결과를 가져오는 일을 1000배 줄인 것이다.

이게 3장 캐시 챕터에서 본 stampede 패턴의 채팅 도메인 변주다. 일반적인 캐시는 TTL 만료 시 stampede를 막기 위해 singleflight를 쓰는데, 채팅의 hot 메시지는 그것이 read 자체의 정상 상태다. **싱글 키 stampede가 일상이라서 coalescing이 application 옆에 layer로 박혀야 했다.** 같은 원리, 다른 모양이다.

그리고 마이그레이션 자체가 인상적이다. 처음 추정치는 "3개월". 실제로 걸린 시간은 **9일**. 무엇이 달랐는가? 마이그레이션 도구를 Rust로 다시 짰다. Cassandra에서 ScyllaDB로 row를 옮기는 streaming engine을, throughput을 한계까지 끌어올린 도구로 자체 제작한 것이다. 마이그레이션이 본업이 아닌 회사가 마이그레이션 도구를 처음부터 짜기로 결정한 것은 이례적이지만, 결과적으로 그 결정이 비용을 90% 줄였다.

이 사례에 한 가지 교훈이 있다. tribal #10에 들어 있는 휴리스틱이다. "DB는 마지막에 바꿔라 — 가장 비싼 마이그레이션." Discord는 그걸 알면서도 결정을 내렸다. 그리고 마이그레이션 도구라는 본업 외 자원에 투자해 비용을 줄였다. **마이그레이션 도구가 마이그레이션의 비용을 결정한다**는 사실은 기억해두자.

## 당근 채팅 — DynamoDB를 고른 한국 hyperlocal

한국 사례로 넘어와 보자. 당근마켓이 채팅을 따로 분리하면서 내린 결정은 책 전체에서 가장 흥미로운 한국 케이스 중 하나다(W31, 자료 4.11).

당근 채팅팀이 정리한 결정 사항을 한 줄로 줄이면 이렇다.

> 채팅을 별도 MSA로 분리 + 회사 첫 Go 도입 + DynamoDB를 storage로 선택. Cassandra 운영 부담을 회피하기 위함. (당근 blog, W31)

Cassandra가 아닌 DynamoDB를 고른 이유가 명시적으로 적혀 있다. **운영 부담 회피.** Discord 같은 회사는 Cassandra를 깊이 운영할 인력이 있지만, 당근은 채팅이라는 한 도메인에 그만한 운영 자원을 쓸 수 없다. 그래서 AWS managed service로 그 부담을 outsource한 것이다. 정직한 trade-off다.

물론 trade-off의 다른 쪽도 있다. DynamoDB는 vendor lock-in이 강하고, write 비용이 read 비용의 5배 이상이다. group chat의 fan-out이 많은 도메인에서는 비용이 빠르게 늘 수 있다. 그래서 당근은 도메인을 정확히 잘랐다. **거래 위치 기반의 1대1 채팅, 거래 완료 후 chat archive라는 라이프사이클** — 카카오톡 같은 영구 group chat과는 다른 게임이다(한국 7).

푸시 알림은 또 다른 결정이다. Node.js로 짠 push service가 초당 1500 RPS를 처리한다. 1500이 큰 숫자는 아니지만, 한국 hyperlocal의 트래픽 패턴(동네 단위 부분 spike)에 맞춘 capacity 결정이다. 글로벌 시스템처럼 10만 RPS를 미리 박지 않는다.

이게 도메인을 정확히 자른 시스템 디자인의 한 사례다. "쿠팡처럼 만들어야 한다"는 강박이 없다. 자기 도메인이 무엇이고, 어떤 라이프사이클을 가지고 있고, 운영자가 몇 명이고, 트래픽 패턴이 어떤지를 정확히 셈한 결과의 그림이다. 다른 회사 운영 시스템을 그대로 베끼면 안 된다는 점을 한국 사례가 거꾸로 증명한다.

## Slack — workspace sharding의 단단함

Slack은 또 다른 길을 갔다. 10B+ messages를 처리하는 시스템인데, 핵심 결정 하나가 모든 것을 단단하게 만든다(W22, 자료 4.2).

> Workspace-based sharding. shop_id처럼 workspace_id 기준으로 MySQL을 샤딩한다. PHP WebApp(저장) + Java RTM(real-time messaging). Elasticsearch가 search, 자체 KalDB가 logging. (Slack Engineering)

Slack의 채팅은 회사 단위(workspace) 안에서만 일어난다. 같은 workspace 안의 사용자만 같은 채널을 공유한다. 즉 **cross-workspace 쿼리가 사실상 없다**. 이게 sharding key를 결정할 때의 황금 같은 조건이다. 13장에서 본 hot partition의 함정이 거의 발생하지 않는다 — workspace는 자연스럽게 적당히 균등하게 분포한다.

Slack은 KalDB라는 자체 로그 스토리지까지 만들었다. 왜? Elasticsearch가 logging에 안 맞아서다. 5장에서 본 ES의 한계 — JVM heap 32GB cap, refresh interval 1초로 인한 write 부하 — 가 trillions of log를 다루기 시작하면 한계가 명확해진다. 회사가 자체 로그 store를 만든다는 결정은 엄청난 비용이지만, Slack 같은 규모에서는 운영비 절감이 그 비용을 회수한다.

여기서 한 가지 흥미로운 비교를 해보자.

| 항목 | Discord | LINE | 당근 | Slack |
|------|---------|-------|------|-------|
| **scale** | trillions of messages | 새해 0시 정상 평균 수십 배 | 한국 hyperlocal | 10B+ messages |
| **transport** | WebSocket | WebSocket (connection-manager 분리) | WebSocket | WebSocket (Java RTM) |
| **storage** | Cassandra → ScyllaDB | Akka actor + Redis Cluster (LIVE) | DynamoDB | MySQL workspace sharding |
| **sharding key** | channel_id | user_id | room_id (거래) | workspace_id |
| **fan-out 전략** | data services coalescing | message-router → Kafka | DynamoDB stream + Node.js | RTM Java service |
| **운영 철학** | 직접 다 만든다 | platform화 후 분리 | managed service 활용 | 자체 도구 투자 |
| **trade-off 회피** | JVM GC, hot partition | reconnect storm | Cassandra 운영 부담 | ES logging 한계 |

표를 한 줄로 줄이면 이렇다. **네 시스템은 모두 자기 도메인의 가장 큰 적을 명확히 정의했고, 그 적을 피하기 위해 비싼 결정을 했다.** Discord는 GC와 hot partition을, LINE은 reconnect storm을, 당근은 운영 부담을, Slack은 ES limit을 적으로 정의했다. 채팅 시스템 설계의 본질은 **자기 도메인의 1번 적을 정직하게 정의하는 일**이다.

## Sidebar: 카카오톡 새해·설날 트래픽 — fan-out 비용의 한국 버전

한국 메신저의 트래픽 패턴을 한 페이지 따로 보고 가자. 카카오 if(kakao) 발표가 정리한 카카오톡의 비정상 트래픽 시기다(한국 4).

- **새해 0시**: 평상시 대비 메시지 트래픽 5~30배 spike (시기마다 다름).
- **설날 아침**: 부모님께 보내는 메시지의 fan-out이 가장 거대한 도메인 spike 중 하나.
- **어버이날·발렌타인·크리스마스**: 같은 패턴.

평상시 카카오톡의 초당 메시지 수가 수십만 건 단위인데, 그게 5~30배가 되면 산술적으로 분당 수억 건의 메시지가 처리돼야 한다. 이걸 단순히 "노드를 30배 늘려 두자"로 풀 수 있을까? 두 가지 이유로 답은 No다.

첫째, **비용**. 30배 capacity를 평소에 들고 있는 비용은 한 회사가 감당하기 어렵다. 둘째, **autoscale의 한계**. 0시 정각에 트래픽이 30배 점프하는 데, 그 시점에 autoscale로 노드 늘리려고 하면 이미 늦었다. cold start latency가 5~10분이라, 그 사이 1번 메시지부터 30번 메시지까지가 모두 지연된다.

그래서 한국 메신저들이 채택하는 패턴이 몇 가지 있다. 카카오 발표에서 명시적으로 풀이된 부분과 추정으로 정리해보면 다음과 같다.

1. **사전 예열(pre-warming)**: 새해 0시·설날 아침 같은 정해진 시간 전에 capacity를 미리 늘린다. autoscale에 기대지 않고, 운영자가 명시적으로 노드를 띄운다.
2. **백프레셔 + queue 흡수**: 메시지 큐(4장)를 두텁게 만들어 burst를 흡수한다. 메시지 일부에는 1~5초의 지연을 받아들이고, ordering을 보장한 채 흘려보낸다.
3. **group push fan-out 분리**: 1대N의 fan-out은 별도 layer에서 처리한다. 메시지 저장과 별개의 파이프라인이라, 저장이 빠르게 ack된 뒤 push가 비동기로 일어난다.
4. **광고 트래픽은 다른 패턴**: 점심·퇴근 시간대 spike는 메시지와 다른 시스템에서 처리한다 — 트래픽 분리가 곧 안전이다.

이 sidebar의 핵심은 한국 환경의 정시(0시·9시) 일제 트래픽이 **시스템 디자인을 elastic이 아닌 burst-tolerant로 만든다**는 점이다. 17장 fan-out 챕터에서 Twitter·Instagram의 fan-out 패턴을 볼 텐데, 그것이 글로벌 일상의 fan-out이라면 카카오톡 fan-out은 한국 정시 트래픽의 fan-out이다. 같은 패턴, 다른 압력. 잊지 말자.

## 채팅 시스템에서 1·2부가 모두 재등장하는 자리

여기까지 보고 나면 한 가지 그림이 자연스럽게 떠오른다. 채팅 시스템은 1·2부 모든 챕터의 회수 장면이다. 한 줄로 정리해보자.

- **2장 NoSQL hot partition** → Discord의 30K req/s 같은 메시지가 같은 partition을 두드리는 자리. data services의 coalescing이 그 답.
- **3장 캐시 stampede** → Discord coalescing의 다른 이름. 인기 채널 메시지가 곧 stampede의 대상.
- **4장 메시지 큐** → LINE의 Kafka, 카카오톡의 burst 흡수 queue. 비동기로 ordering을 지키는 1번 layer.
- **8장 시간·순서** → 채팅의 ordering 요구. 같은 채팅방의 단일 leader 또는 채널별 sequence number.
- **9장 보안** → WebSocket 위의 JWT·session token, secret rotation, 카카오톡의 E2E 암호화 도입 흐름.
- **13장 sharding** → Slack의 workspace, 당근의 거래(room_id), Discord의 channel_id가 모두 sharding key.
- **14장 관측성·on-call** → LINE의 Apache HTTP client 사건이 어떻게 일찍 잡혔는지, autoscale 미작동을 사전 예열로 어떻게 막는지.

이게 케이스 스터디의 약속이다. 1·2부의 학습이 한 시스템 안에서 어떻게 동시에 쓰이는지를 채팅이라는 도메인에서 처음 본다. 이 패턴이 17장 피드, 18장 검색·매칭, 19장 결제, 20장 이커머스로 가면서 반복된다. 어떤 시스템을 봐도 "이건 X장 Y절과 비슷하군"이라는 자동 mapping이 머릿속에 생기기 시작한다.

## Sidebar: 다른 유사 시스템 한 단락 — WhatsApp의 Erlang VM

본문이 다루지 못한 채팅 도메인의 또 다른 대표 사례를 한 단락으로 봐 두자. **WhatsApp**이다(검증 필요).

WhatsApp이 1조 메시지 단계로 가는 동안 한 가지 결정으로 유명하다. 처음부터 끝까지 **Erlang VM** 위에서 돌아간다. Erlang은 1980년대 통신사 스위치를 위해 설계된 언어인데, lightweight process(한 노드에 수십만 프로세스 가능)와 supervisor tree(실패 격리)가 채팅 도메인의 connection management·fault tolerance에 절묘하게 맞아떨어진다. 한 노드에 수십만 동시 connection을 운영하면서도 한 connection이 죽어도 다른 connection이 영향받지 않는다.

WhatsApp 인수 당시 50명도 안 되는 엔지니어가 5억 사용자를 운영했다는 사실이 자주 회자된다(검증 필요). 그 비밀의 절반은 Erlang의 선택이다. 나머지 절반은 단순함 — feature를 의도적으로 줄이고, 핵심 도메인(1대1·group 메시지)만 깊게 만든 것이다. **단순함이 운영의 무기**라는 점도 잊지 말자.

## Sidebar: 이 시스템의 운영 — SLO·alert·rollback

채팅 시스템의 운영을 한 페이지 따로 보자. 14장에서 본 일반 운영론이 채팅 도메인에서 어떻게 변주되는지의 한 사례다.

**핵심 SLI**: 메시지 send latency p99 (목표 100ms), message delivery success rate (목표 99.99%), WebSocket connection success rate (목표 99.95%). 이 셋이 채팅의 사용자 체감과 직결된다.

**SLO burn rate alerting**: 빠른 소진(1시간 동안 budget 2% 이상 소진)은 즉시 page, 느린 소진(6시간 5% 또는 24시간 10%)은 다음 영업일 ticket. WebSocket 끊김은 사용자가 직접 알아채는 자리라 page 임계값을 낮게 잡는다.

**Connection re-balance alert**: server pod이 떨어졌을 때 reconnect storm을 감지하는 alert가 따로 있다. 1분 안에 한 server pod에 reconnect가 평소 5배 이상 몰리면 즉시 page. autoscale이 따라오지 못하면 즉시 capacity 강제 증가.

**Rollback 전략**: 채팅 시스템은 message format 변경이 자주 일어난다. backward-compatibility를 깨는 변경은 절대 한 번에 배포하지 않는다 — feature flag로 1% → 10% → 100% 점진 rollout. 메시지가 한 번이라도 잘못 저장되면 영구 손실이라, blue-green이나 canary 같은 일반 패턴보다 더 엄격하게 적용한다.

**카오스 게임 day**: 분기별로 한 region을 의도적으로 끊는다. 5명 팀이 그 사이 사용자에게 영향이 가는지를 본다. 14장의 chaos engineering 패턴이 채팅 도메인의 안전 검증 1번 도구가 된다.

이 운영 5축이 채팅의 24/7 신뢰를 만든다. 가장 잔인한 시스템 중 하나라는 첫 줄을 다시 떠올려보자. 운영을 어떻게 만드느냐가 사용자가 느끼는 그 잔인함을 흡수한다.

## 이 장의 약속 회수

채팅 시스템을 직접 설계할 일이 없는 사람도, 이 장을 다 읽으면 한 가지를 머릿속에 가지고 갈 수 있다. **어떤 의사결정 축이 있고, 한국 메신저가 무엇을 골랐는지**의 한 페이지 표다.

5축의 trade-off (ordering·durability·history·real-time·fan-out), 그 위에 4개 회사의 결정(Discord·LINE·당근·Slack), 그리고 한국 환경의 트래픽 패턴(카카오톡 spike)이 한 그림으로 묶인다. 새로운 채팅 시스템을 봤을 때 어디에 점이 찍혀 있는지를 물을 수 있게 된다. 그게 1·2부의 약속이 케이스 스터디에서 처음 회수되는 자리다.

기억해두자. **채팅 시스템 설계의 본질은 자기 도메인의 1번 적을 정직하게 정의하는 일이다.** 당근이 Cassandra 운영 부담을 적으로 정의했기 때문에 DynamoDB를 골랐다. Discord가 GC와 hot partition을 적으로 정의했기 때문에 ScyllaDB + Rust coalescing을 만들었다. 적을 잘못 정의하면 비싼 도구를 사도 적이 죽지 않는다.

## 다음 장으로 가는 다리

채팅이 1대1과 group의 fan-out을 다뤘다면, 다음 장 피드·타임라인은 1대N (그것도 N이 1억까지 가는) fan-out의 극단을 본다. **1억 팔로워의 한 게시물을 모두에게 보여주는 비용을 누가 부담하는가?** 같은 fan-out이지만 카카오톡의 group push와는 다른 게임이다. Twitter의 hybrid fan-out, Instagram의 Cassandra timeline, 카카오톡의 group push가 어떻게 같은 문제를 다르게 풀고 있는지를 살펴보자.

가기 전에 한 번 정리하자. **운영해 보면 가장 잔인한 시스템 중 하나라는 사실은 그 시스템의 약점이 아니라 그 시스템의 본질이다.** 잔인함을 정직하게 마주한 회사만이 1조 메시지의 신뢰를 만든다. 우리도 자기 도메인 안에서 같은 정직함을 가질 수 있는가, 가 케이스 스터디 5개 장의 공통 질문이다.

---

*챕터 작성 메모: 02_plan §3 16장 사양 충실 반영. 5축 trade-off (ordering·durability·history·real-time·fan-out) / WebSocket transport + LINE connection-manager 분리 / Discord Cassandra → ScyllaDB 9일 마이그레이션 + Rust coalescing / 당근 DynamoDB 선택 이유 + hyperlocal / Slack workspace sharding + KalDB / 4사 비교표 / 카카오톡 새해 spike sidebar / WhatsApp Erlang sidebar / 운영 SLO sidebar. W21·W22·W30·W31·자료 4.1·4.2·4.10·4.11·한국 4·한국 7·tribal #10 인용. WhatsApp 일부에 (검증 필요) 라벨. 분량 약 24p 추정 (한국어 ~7200자). 1·2부 callback: 2장·3장·4장·8장·9장·13장·14장. 17장(피드 fan-out)으로 다리.*
