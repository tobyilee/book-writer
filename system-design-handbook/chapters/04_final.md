# 4장. 메시지 큐 — 비동기와 decoupling의 토대

오전 9시, 슬랙에 "큐 lag 4시간"이라는 메시지가 떴다고 해보자. 누가 봐도 1주일 전 배포가 원인 같다. 그런데 이상하게 누구도 처음엔 그 배포를 의심하지 않는다. 어제까지 멀쩡했으니까. 메트릭 대시보드를 펴 보니 그제부터 consumer lag이 조금씩 쌓이기 시작해서, 지난 새벽에 갑자기 직선으로 솟구쳐 있다.

큐는 조용히 망가진다. DB가 느려지면 latency 알람이 즉시 뜨고, 캐시가 비면 origin이 비명을 지른다. 그런데 큐는 다르다 — producer는 멀쩡히 send에 성공하고, broker도 조용히 메시지를 받아 쌓는다. 망가지는 곳은 consumer이고, 망가지는 모양은 "쌓이는 메시지의 모양"이다. 큐 모니터링이 없으면 우리는 그 모양을 볼 수 없다. 그게 큐를 가장 무서운 부품으로 만든다.

그래서 큐는 두 모양을 같이 머릿속에 그려야 다룰 수 있는 부품이다. **잘 작동할 때** — Kafka·RabbitMQ·SQS가 무엇을 약속하고 무엇을 양보하는지. **망가질 때** — consumer lag, rebalance storm, retention loss, exactly-once의 진실. 도입 자격을 묻는 6가지 질문이 마지막에 손에 잡힌다면, 큐를 잡는 두려움이 한 단계 가벼워진다.

## 큐를 도입한다는 결정은 무엇을 양보하는 결정인가

큐는 두 service를 비동기로 갈라 놓는다. producer는 send만 하고 끝낸다. consumer는 자기 속도로 받아서 처리한다. 이 한 줄짜리 구조 변경이 시스템에 가져오는 효과는 크게 네 가지다.

**1. 시간 디커플링.** producer가 보내는 시점과 consumer가 받는 시점이 분리된다. consumer가 잠시 죽어도 큐에 메시지가 쌓여 있어 producer는 영향이 없다.

**2. 부하 평탄화 (load smoothing).** 짧은 burst를 큐가 흡수하고, consumer는 평균 속도로 처리한다. 카카오의 0시 트래픽, 토스의 새벽 이자 정산 같은 burst 패턴이 큐 없이는 견디기 어렵다.

**3. 디커플링.** producer는 누가 메시지를 받는지 모른다. 새 consumer를 추가해도 producer 코드는 안 바뀐다. event-driven 아키텍처의 토대다.

**4. retry·재처리 가능성.** 메시지가 큐에 저장되어 있으니, 실패한 consumer가 재시도하거나, 새 버전의 consumer가 옛 메시지를 다시 처리할 수 있다.

이 네 효과가 정말 매력적이라서, 많은 팀이 큐를 default로 깐다. 그런데 큐를 깐다는 결정은 거꾸로 보면 **양보**의 결정이기도 하다. 무엇을 양보하는가?

**1. 즉시 응답을 양보한다.** "보냈다"는 producer의 약속이고, "정말 처리됐다"는 약속이 아니다. 결제 confirm 같은 sync 응답이 필요한 도메인은 큐로 갈 수 없다.

**2. 일관성을 양보한다.** producer가 DB에 commit하고 큐에 메시지를 보내는 사이에 시스템이 죽으면, DB만 변하고 메시지는 안 보내진 상태가 된다. 그 반대도 가능하다. 이 dual-write 문제를 어떻게 푸는가가 11장 Saga·Outbox 챕터의 핵심이다.

**3. 디버깅 가시성을 양보한다.** sync 호출이면 stack trace 한 번으로 누가 뭘 보냈는지 보인다. 큐는 producer와 consumer의 trace가 따로 떠다닌다. distributed tracing(W3C trace context) 없이는 디버깅이 끔찍해진다.

**4. 운영 부담을 추가한다.** broker 자체를 운영해야 한다. 모니터링, 백업, upgrade, partition rebalance — 새로운 종류의 새벽 alert가 추가된다.

그래서 큐 도입은 "필요한가"를 먼저 묻는 편이 낫다. 큐 없이 sync API로 충분히 풀리는 도메인에 굳이 큐를 깔면, 운영 부담만 늘고 새 종류의 사고가 생긴다. **"큐의 4가지 효과 중 우리에게 정말 필요한 게 무엇인가"를 자기 도메인 언어로 답할 수 있어야 도입 자격이 생긴다.**

## Kafka vs RabbitMQ vs SQS vs Pulsar — 어디가 어떻게 다른가

큐 선택지로 가장 자주 거론되는 4가지를 한 표로 정리하자. 한국 백엔드에서는 Kafka와 RabbitMQ가 가장 흔하고, AWS 친화 팀은 SQS를 쓰고, Pulsar는 채택률이 낮지만 일부 팀이 검토한다.

| 차원 | Kafka | RabbitMQ | SQS (AWS) | Pulsar |
|------|-------|----------|-----------|--------|
| 기본 모델 | log + partition + offset | exchange + queue + routing key | distributed queue | log + tiered storage |
| 메시지 소비 후 | retention 동안 유지 (default 7일) | ack 시 삭제 | ack 시 삭제 (visibility timeout) | retention 동안 유지 |
| ordering | partition 내 순서 보장 | FIFO 큐만 보장 | FIFO 큐 또는 standard | partition 내 |
| throughput | 매우 높음 (~10만 msg/sec/partition) | 중간 (~1만/sec) | 무제한 (manage) | 매우 높음 |
| replay 가능 | 됨 (retention 안에서) | 안 됨 (소비 후 삭제) | 안 됨 | 됨 |
| consumer model | consumer group, pull | push 또는 pull | poll only | consumer group |
| 운영 모델 | 자체 cluster 또는 managed (MSK·Confluent) | 자체 cluster | 완전 managed | 자체 cluster |
| 학습 곡선 | 가파름 | 완만 | 매우 완만 | 가파름 |
| 가장 강한 곳 | event streaming, 데이터 파이프라인, 높은 throughput | RPC-like 비동기, 복잡한 routing | AWS 단일 region 비동기 | tiered storage, multi-tenancy |

이 표를 보면 두 모델이 갈린다. Kafka·Pulsar는 **"simple broker, complex consumer"** — broker는 그냥 log를 쌓고, consumer가 offset을 관리한다. RabbitMQ·SQS는 **"complex broker, simple consumer"** — broker가 routing·delivery·retry를 다 책임지고, consumer는 그냥 받기만 한다.

이 차이가 왜 중요한가? Jack Vanlightly의 RabbitMQ 시리즈가 가장 명확히 설명한다.

> Kafka uses a "simple broker, complex consumer" approach, while RabbitMQ follows a "complex broker, simple consumer" model. (Quix Comparison)

Kafka에서는 같은 토픽을 두 그룹의 consumer가 각자 자기 offset으로 따로 소비할 수 있다. event sourcing, audit trail, 데이터 파이프라인의 fanout에 잘 맞는다. RabbitMQ에서는 메시지가 소비되면 사라진다. 작업 큐, RPC-like 비동기, 복잡한 routing(direct·topic·fanout exchange)에 잘 맞는다.

선택의 한 줄 가이드를 굳이 만들면 이렇다.

- **데이터 파이프라인·event log·replay가 필요한가?** Kafka.
- **routing·dead letter queue·작업 큐가 단순한가?** RabbitMQ.
- **AWS only이고 운영 비용 최소화가 우선인가?** SQS.
- **multi-tenant·glacier 같은 tiered storage가 필요한가?** Pulsar (단, 운영 인력 필요).

한국 백엔드에서는 Kafka가 압도적이다. 카카오·라인·쿠팡·우아한형제들 모두 Kafka 기반 인프라가 있다. 그러나 도메인에 따라 RabbitMQ가 답인 경우도 적지 않다. 토스의 결제 후처리 일부, 우아한형제들의 일부 작업 큐가 RabbitMQ로 운영된다는 사례가 있다. **"이력서에 Kafka 쓰려고 도입했다. 실제로는 RabbitMQ로 충분했다"**는 한국 백엔드 익명 후회 글이 OKKY에 정기적으로 올라오는 이유다(community 휴리스틱 10). 도구 선택은 도메인이 먼저고 이력서가 다음이다.

## Kafka의 모양 — partition, offset, consumer group

가장 많이 쓰이는 Kafka의 모양을 한 번 깊이 들여다보자. 다른 큐들도 모양은 다르지만 개념은 비슷하다.

### Topic, Partition, Offset

Kafka의 모든 메시지는 **topic**에 속한다. topic은 여러 **partition**으로 나뉘는데, 각 partition은 순서가 있는 append-only log다. 메시지는 partition 안에서 0부터 차례로 **offset**을 부여받는다.

```
topic: orders
  partition 0: [msg0, msg1, msg2, msg3, ...]   offset 0~3
  partition 1: [msg0, msg1, msg2, ...]          offset 0~2
  partition 2: [msg0, msg1, ...]                offset 0~1
```

같은 partition 안에서는 순서가 엄격히 보장된다. partition 사이에는 순서가 없다. 그래서 "한 사용자의 모든 이벤트는 같은 partition으로"라는 규칙이 자주 쓰인다. partition key를 user_id로 잡으면, 한 사용자의 메시지는 항상 같은 partition으로 가니 순서가 보장된다.

> 💡 partition 수는 한 번 정하면 늘리기는 쉬워도 줄이기는 어렵다. 그리고 partition을 늘리면, 같은 key가 다른 partition으로 가 순서 보장이 깨질 수 있다. **초기에 적당히 넉넉하게 잡는 편이 낫다.** 보통 consumer 최대 수 × 2~3 정도가 시작점이다.

### Consumer Group과 offset commit

consumer 여러 개가 모여 **consumer group**을 이룬다. 같은 group의 consumer들은 partition을 나눠서 소비한다. 한 partition은 한 group 안에서 정확히 한 consumer만 소비한다. 즉 **group 안에서 병렬도는 partition 수가 상한**이다.

```
topic: orders (3 partitions)
group: payment-processor (2 consumers)
  consumer A → partition 0, partition 1
  consumer B → partition 2
```

consumer를 3개로 늘리면 1:1로 매핑된다. 4개로 늘리면 한 consumer는 놀게 된다. partition 수를 미리 넉넉하게 잡아 두라는 이유가 여기에도 있다.

각 consumer는 어느 offset까지 처리했는지를 **commit**한다. commit은 두 가지 방식이 있다.

- **Auto commit (default):** `enable.auto.commit=true`로 두면 5초마다 자동 commit. 편하지만 **메시지 손실 위험**이 있다. consumer가 메시지를 받았는데 처리 전에 죽고 그 사이 auto commit이 일어나면, 그 메시지는 영영 안 처리된다.
- **Manual commit:** 처리 끝난 뒤에 명시적으로 `commitSync()` 호출. 안전하지만 코드가 더 복잡하고, **duplicate 위험**이 있다. 처리는 끝났는데 commit 직전에 죽으면, 다음에 같은 메시지를 또 처리한다.

이 두 모양이 곧 **at-least-once vs at-most-once**의 갈림이다. 둘 중 어느 쪽도 "정확히 한 번"은 아니다.

### Exactly-once의 진짜 의미

"Kafka는 exactly-once를 지원합니다"라는 말을 자주 듣는다. 사실은 그 말이 약간 부정확하다. Kafka의 transactional producer + read_committed consumer + idempotent producer를 함께 쓰면 **Kafka 내부에서는** exactly-once가 가능하다. 그런데 consumer가 메시지를 받아 **외부 시스템(DB, 다른 API)에 쓸 때** exactly-once는 보장되지 않는다. 외부 시스템도 transactional하게 묶어야 한다.

그래서 현실적으로는 거의 모든 시스템이 **at-least-once + idempotent consumer** 패턴을 쓴다. consumer 쪽에 idempotency key·중복 제거 로직을 두어, 같은 메시지가 두 번 와도 한 번만 효과가 나게 만든다. 이 패턴은 10장 멱등성·재시도·서킷 브레이커 챕터에서 깊게 다룬다. exactly-once를 약속하기보다, at-least-once를 받아들이고 idempotent하게 짜는 편이 훨씬 견고하다.

### KRaft — ZooKeeper와의 결별

Kafka 2.8+ 부터는 **KRaft**(Kafka Raft) 모드로 ZooKeeper 없이 metadata를 자체 관리한다. 그 전까지는 broker 메타데이터, partition leader 정보, consumer group 정보의 일부를 ZooKeeper에 저장해야 했다. ZooKeeper는 잘 만들어진 도구지만, Kafka와 함께 운영하는 부담이 만만치 않았다.

Raft 알고리즘 자체는 12장 합의·복제·일관성 챕터에서 깊게 다룬다. 여기서 짚어 둘 것은 **운영 부담이 알고리즘 선택보다 크다는 사실**이다. ZooKeeper는 안정적인 ZAB 합의 알고리즘으로 잘 돌았는데, Kafka는 굳이 자기 Raft를 새로 만들었다. 왜? "또 다른 분산 시스템을 운영하는 부담을 없애기 위해"가 가장 큰 동기였다.

이 사실은 우리에게도 시사점이 있다. **새 분산 부품을 도입한다는 건 새 운영 부담을 짊어진다는 것**이다. Kafka는 자기 부담을 줄이려고 결국 ZooKeeper를 떼어냈다. 우리가 큐 하나를 깐다는 것도 비슷한 무게의 결정이다.

## 한국 큐 운영 — LINE·카카오·쿠팡 사례

해외 사례가 모양을 가르쳐 준다면, 한국 사례는 우리 일상의 함정을 가르쳐 준다. 세 가지를 짚어 보자.

### LINE — Apache HTTP client 업그레이드로 throughput 1/3

LINE Engineering blog에 "Kafka 운영 실패담" 시리즈가 올라온 적이 있다. 가장 끔찍한 사례 중 하나는 **Apache HTTP client 라이브러리를 업그레이드한 후 throughput이 1/3로 떨어진** 사건이다. 코드는 안 바꿨고, 큐 설정도 그대로다. 단지 dependency 한 줄을 올렸을 뿐인데.

원인은 HTTP client의 connection pool 동작 변경이었다. 새 버전이 기본 connection 수를 줄였고, Kafka 쪽이 아닌 그 다음 단계 service의 throughput이 막혔다. 큐는 잘 작동했지만, downstream이 막히니 consumer가 lag을 쌓기 시작했고, 새벽이 되어서야 alert가 떴다.

이 사례가 가르쳐 주는 게 두 가지 있다.

1. **dependency upgrade는 dark deployment처럼 (실 트래픽 일부에만 먼저 흘려) 점검하자.** 기능에 변화가 없어도 throughput은 변할 수 있다.
2. **consumer lag을 메인 SLO 지표에 포함하자.** "처리 성공률"만 보면 throughput 저하가 안 보인다. lag 자체가 SLO의 한 축이 되어야 한다.

### 카카오 — 공용 메시징 플랫폼 TF

카카오 인프라팀은 2021년에 공용 Kafka/RabbitMQ MessageQueue TF를 정식으로 신설했다. 그 전까지는 각 서비스팀이 자체적으로 broker를 띄워 쓰는 형태였는데, 결과적으로 다음 문제들이 누적됐다.

- 같은 회사 안에 Kafka·RabbitMQ·자체 큐가 수십 개 운영. 운영자별 노하우가 흩어짐.
- 큐 사이의 메시지 라우팅이 service 코드 안에 박혀, decoupling이 무너짐.
- broker 한 대 장애 시 영향 범위 추적이 어려움.

TF의 결정은 명료했다. **공용 broker를 중앙에서 운영하고, 서비스팀은 producer·consumer 코드만 짠다.** 이 결정 덕분에 서비스팀의 큐 운영 부담이 줄고, 큐 사이의 흐름이 명확해졌다. 한국 백엔드의 일반적인 운영 패턴 중 하나로 자리잡고 있다.

### 쿠팡 — Kafka 기반 검색 indexing pipeline

쿠팡 엔지니어링 Medium에 "대용량 트래픽 처리를 위한 백엔드 전략"이라는 글이 있다. 쿠팡 검색 indexing pipeline은 Kafka가 중심이다. 상품 데이터가 변할 때마다 Kafka에 이벤트가 발행되고, 검색 indexing 파이프라인이 그 이벤트를 consume해 Elasticsearch에 색인한다.

이 구조의 가치는 **decoupling**이다. 상품 service는 Elasticsearch를 모른다. 검색 indexing pipeline은 상품 service의 DB 스키마를 모른다. 둘은 Kafka 토픽의 이벤트 schema로만 연결된다. 검색 indexing을 새 버전으로 갈아 끼울 때 상품 service는 영향이 없다.

이런 구조가 가능한 이유는 Kafka가 **retention 안에서 replay 가능**하기 때문이다. 새 indexing pipeline을 띄우면 offset 0부터 다시 읽어 전체를 재색인할 수 있다. RabbitMQ로는 이걸 못한다. Kafka의 "log is the queue" 모양이 이런 패턴을 가능하게 한다.

5장 검색 엔진에서 이 쿠팡 indexing pipeline의 디테일을 다시 다룬다. 큐와 검색은 떼어 놓을 수 없는 쌍이다.

## 메시지 큐의 운영 함정 5가지

큐가 망가지는 모양 다섯 가지를 정리하자. 큐 운영자라면 새벽에 alert가 울렸을 때 가장 먼저 떠올려야 할 후보들이다.

### 함정 1. Consumer Lag — 가장 흔하고 가장 silent

**가장 자주, 가장 silent하게 망가지는 모양**이다 — 1장 sidebar에서 JPA N+1을 두고 "조용히 죽이는 함정"이라 부른 패턴과 같은 결이다. 한국 백엔드는 평생 이런 silent killer를 안고 산다. 메시지는 producer가 잘 보내고 있고 broker는 잘 저장하고 있는데, consumer가 따라가지 못해 점점 쌓인다. lag이 1만, 10만, 100만으로 늘어 가는 동안 producer는 영문도 모른 채 평소처럼 메시지를 보낸다.

원인 후보는 다양하다.

- consumer의 downstream(DB, API)이 느려졌다.
- consumer 코드 안에 thread block이 생겼다(I/O 처리 누락 등).
- partition 수가 적어 병렬도가 부족하다.
- consumer instance 수가 partition보다 많아 일부가 놀고 있다.

대처는 lag 모니터링 + 자동 scale이 답이다. Kafka에서는 `kafka-consumer-groups.sh --describe`로 group별 lag을 볼 수 있고, Datadog·Burrow 같은 도구가 자동 모니터링을 제공한다. lag이 일정 임계를 넘으면 즉시 alert를 띄우자.

### 함정 2. Rebalance Storm

consumer가 죽거나 새로 뜨면 partition을 재할당하는 **rebalance**가 일어난다 — 부록 A의 tribal #5가 정확히 가리키는 함정이다. 이 동안 모든 consumer가 잠시 멈춘다. Kafka의 옛 버전(2.3 이하)에서는 모든 partition이 한 번에 재할당되어, group 전체가 수 초~수십 초 멈춘다. consumer가 자주 죽고 뜨는 환경에서는 rebalance만 1분에 한 번씩 일어나 throughput이 절반이 된다.

해결은 Kafka 2.4+로 올리고 **incremental cooperative rebalancing**을 켜는 것이다. partition 재할당이 점진적으로 일어나, 모든 consumer가 동시에 멈추지 않는다. 그리고 consumer의 죽고 뜨는 빈도 자체를 줄이는 게 더 근본적이다 — K8s에서 readiness probe 잘못 잡아 consumer가 자주 restart하는 경우가 흔하다.

### 함정 3. Retention 짧음 + Consumer down → 데이터 loss

Kafka의 default retention은 7일이다. 그런데 짧게 잡아 둔 경우 끔찍한 일이 일어날 수 있다.

상황을 가정해 보자. retention 1일로 설정된 토픽이 있다. consumer가 무슨 사고로 23시간 멈춰 있었다. 깨어나서 처리하려고 보니, 가장 오래된 메시지는 1시간 안에 만료된다. 그 메시지를 미처 처리하기 전에 retention이 끝나고 메시지가 삭제된다.

HN에 "How we lost 24 hours of data with Kafka"라는 글이 있다. `auto.offset.reset=latest` 설정이 함께 작용해, consumer가 깨어났을 때 옛 메시지를 다 건너뛰고 최신 메시지부터 읽기 시작한 사례다. 24시간치 데이터가 영영 사라졌다.

대처는 두 가지다.

1. **Critical 토픽의 retention은 충분히 길게 (보통 7일 이상).** 단, retention이 길어지면 storage 비용이 늘어난다.
2. **`auto.offset.reset=earliest`로 설정.** consumer가 깨어났을 때 옛 메시지부터 읽도록.

### 함정 4. Producer의 Dual-Write 문제

producer가 DB에 record를 쓰고, 그 다음에 Kafka에 이벤트를 발행하는 코드가 흔하다.

```python
def create_order(order):
    db.insert(order)        # 성공
    kafka.send(event)       # 실패 → 메시지 안 감
```

이 사이에 시스템이 죽으면? DB에는 주문이 들어 있는데 Kafka에는 이벤트가 없다. 다음 단계(결제·배송·알림)가 안 일어난다. 끔찍하다.

이 dual-write 문제의 정식 해법이 **Transactional Outbox 패턴**이다. DB 트랜잭션 안에서 outbox 테이블에 이벤트를 함께 insert하고, 별도 워커(Debezium 같은 CDC)가 그 테이블의 변경을 tail로 따라가며 Kafka에 발행한다. 같은 트랜잭션이라 atomic하다. 자세한 내용은 11장 Saga·Outbox 챕터에서 다룬다.

### 함정 5. 메시지가 너무 큰 경우

Kafka의 default `message.max.bytes`는 1MB다. 큰 binary payload나 거대한 JSON을 그대로 큐로 흘리려고 하면 broker가 거부한다. 설정을 높여서 보낼 수도 있지만, 그러면 broker·consumer 모두 메모리 부담이 크다.

표준 패턴은 **claim-check pattern(보관증 패턴)**이다. 큰 payload는 S3에 올리고, Kafka에는 그 S3 "보관증"(key)만 보낸다. consumer가 받아서 S3에서 가져온다. binary file processing pipeline에 자주 쓰이는 모양이다.

## Delivery Semantic — at-most-once vs at-least-once vs exactly-once

큐의 delivery 모드 3가지를 한 번 정리하자. 이름이 자주 헷갈리는 부분이다.

| 모드 | 의미 | 위험 |
|------|------|------|
| At-most-once | 0번 또는 1번 처리 | 메시지 손실 가능 |
| At-least-once | 1번 이상 처리 | 중복 처리 가능 |
| Exactly-once | 정확히 1번 처리 | broker·consumer·외부 시스템 모두 transactional 필요 |

Kafka·RabbitMQ·SQS 모두 default는 at-least-once다. consumer 입장에서는 같은 메시지가 두 번 올 수도 있다는 가정으로 코드를 짜야 한다.

**휴리스틱 하나를 마음에 새기자 — idempotent하지 않은 consumer는 큐를 쓸 자격이 없다.** 같은 메시지가 두 번 와도 한 번만 효과가 나도록 짜야 한다. 결제 처리, 잔고 차감, 알림 발송 — 모두 idempotency key로 중복을 제거하는 패턴이 필수다.

exactly-once를 약속하는 broker가 있다고 해도, 외부 시스템(우리 DB, 다른 API)에 쓰는 동작은 결국 우리 책임이다. broker의 exactly-once는 broker 안에서만 유효하다. 그래서 현실은 거의 항상 **at-least-once + idempotent consumer** 패턴이다. 이 두 단어를 마음에 새겨 두자.

## 큐 도입 자격을 묻는 6가지 질문

지금까지 살펴본 내용을 자기 팀 회의실에 가져가 보자. 큐를 도입하려는 결정 앞에서 자기에게 던져야 할 6가지 질문이다.

1. **이 흐름이 정말 비동기여야 하는가?** sync API로 충분히 풀리면, 큐는 차라리 안 까는 편이 낫다.
2. **어떤 delivery semantic이 필요한가?** at-most-once를 견딜 수 있는가, idempotent consumer를 짤 수 있는가?
3. **메시지 ordering이 필요한가, 필요하다면 어느 단위로?** user 단위? order 단위? 전체 토픽 단위? partition key 선택이 거기서 갈린다.
4. **retention이 얼마나 필요한가?** replay가 필요한가, 아니면 소비 후 삭제로 충분한가?
5. **운영 부담을 짊어질 수 있는가?** managed (MSK·SQS·Confluent Cloud)로 갈 것인가, 자체 운영할 것인가?
6. **모니터링은 어떻게 할 것인가?** consumer lag·rebalance·throughput 모니터링이 도입과 동시에 깔리는가?

이 여섯에 답이 안 나오면 도입을 미루는 편이 낫다. 답이 다 나오면, 그때야 broker 선택의 영역으로 넘어간다. **Kafka·RabbitMQ·SQS의 선택은 마지막 결정이지 첫 결정이 아니다.**

## Callback 예고 — 10·11·19장에서 큐가 다시 등장한다

큐는 빌딩 블록이지만, 본격적인 무대는 패턴과 케이스 스터디에서다.

- **10장 멱등성·재시도·서킷 브레이커.** 큐의 at-least-once가 idempotent consumer를 어떻게 만나는지.
- **11장 Saga·Outbox·이벤트 소싱.** dual-write 문제를 Outbox + CDC가 어떻게 푸는지. Saga의 compensating transaction이 큐 위에서 어떻게 흐르는지.
- **19장 결제 시스템.** 토스 결제 critical path가 어떻게 sync(승인)와 async(영수증·알림·정산)를 가르는지.

이 세 챕터에서 4장의 기초가 그대로 얹힌다. **빌딩 블록의 trade-off를 모르면 패턴의 의사결정이 막막해진다**는 사실이 이 책 전체에 흐르는 메시지다. 큐의 모양을 머릿속에 정확히 그려 두면, 나중 챕터들의 결정 트리가 자연스럽게 따라온다.

## 운영 모니터링 — 메시지 큐 대시보드 7가지

마지막으로 운영 대시보드를 정리하자.

| # | 지표 | 의미 | 위험 임계 |
|---|------|------|----------|
| 1 | producer send rate | 발행 속도 | 평소 ±50% 벗어나면 의심 |
| 2 | consumer fetch rate | 소비 속도 | producer rate보다 낮으면 lag 쌓임 |
| 3 | consumer lag (per group) | 처리 지연 | 임계 (예: 1만) 넘으면 즉시 alert |
| 4 | rebalance count | rebalance 발생 빈도 | 시간당 한 자릿수면 정상, 더 많으면 의심 |
| 5 | broker disk usage | retention storage | 80% 넘으면 retention 축소 또는 storage 증설 |
| 6 | broker network IO | 네트워크 포화 | 80% 넘으면 의심 |
| 7 | producer error rate / consumer error rate | 발행·소비 실패율 | 0이 정상, 0 초과면 즉시 조사 |

특히 **consumer lag**은 큐 운영의 가장 중요한 지표다. lag 그래프 하나가 큐 시스템의 건강을 압축적으로 보여 준다. lag 모니터링이 없는 큐는 안 깐 것과 다름없다고 봐도 좋다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 메시지 큐의 양면이 손에 잡혀 있다. 비동기·decoupling·load smoothing·replay라는 4가지 효과, Kafka·RabbitMQ·SQS·Pulsar의 갈림, 그리고 망가질 때의 5가지 모양 — consumer lag, rebalance storm, retention loss, dual-write, 메시지 크기. 한국 사례도 LINE의 HTTP client 업그레이드 실패담, 카카오 공용 메시징 플랫폼 TF, 쿠팡 검색 indexing pipeline까지 함께 짚었다.

기억해두자. 큐는 두 service를 시간으로 갈라 놓는 부품이다. 그 갈라짐 자체가 효과인 만큼, 갈라진 사이의 시야가 없으면 큐는 silent하게 망가진다. **lag 모니터링이 깔리지 않은 큐는 깔지 않은 것과 같다**는 사실을 마음에 새기자. 그리고 도입 전에 자기에게 6가지 질문을 던지자. 답이 다 안 나오면 도입을 미루는 편이 낫다.

다음 장에서는 검색 엔진을 살펴본다. 한국어가 영어 분석기로 안 되는 이유부터, Elasticsearch shard 100개의 진짜 의미까지. 그곳에서도 우리는 같은 질문을 만난다 — "이 부품을 도입할 자격이 우리에게 있는가."
