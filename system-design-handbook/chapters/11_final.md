# 11장. Saga·Transactional Outbox·이벤트 소싱 — 분산 트랜잭션의 현실적 길

어떤 결제 시스템에서, 카드 승인은 성공했는데 우리 DB에 기록을 못 남기는 사고가 있다고 해보자. 사용자 입장에서는 돈이 빠져나갔다. 카드사 명세서에 결제 기록이 찍혔다. 그런데 우리 DB에는 그 결제가 없다. 결제 영수증을 발급하라는 후속 작업도 안 일어난다. 사용자가 "왜 영수증이 안 와요?"라고 문의를 넣는다. 우리는 시스템 로그를 펴 보고 한참 뒤에야 무슨 일이 일어났는지 추측한다.

이런 상황을 한 번 겪고 나면 "dual-write 문제"라는 단어가 평생 따라다닌다. **두 시스템(우리 DB + 카드사)에 같은 트랜잭션을 atomic하게 쓰는 게 불가능하다**는 진실. 둘 중 하나는 성공하고 다른 하나는 실패할 수 있는 그 가능성이 분산 시스템의 가장 어두운 균열이다.

그래서 이 균열을 어떻게 메우는지가 이번 장의 주된 사고 실험이다. 가장 단순한 해법인 2PC가 왜 거의 안 쓰이는지, 그 대신 무엇이 들어왔는지. Saga, Transactional Outbox + CDC, Event Sourcing의 세 갈래를 짚고, 각각이 어떤 도메인에 맞는지 의사결정 트리를 손에 잡자. 한국 토스 코어뱅킹의 SAGA + 2PC 혼합 사례까지 함께 본다.

## 왜 2PC를 거의 안 쓰는가

분산 시스템의 일관성을 보장하는 가장 단순한 답은 **2PC (Two-Phase Commit)**다. 1980년대부터 알려진 표준 프로토콜이다. 흐름은 단순하다.

```
Phase 1 (Prepare):
  Coordinator → Participants: "이 트랜잭션 commit할 수 있어?"
  Participants → Coordinator: "yes" 또는 "no"

Phase 2 (Commit):
  모두가 yes면 → "commit해라" 명령
  하나라도 no면 → "abort해라" 명령
```

이론적으로 깔끔하다. 그런데 production에서 2PC를 쓰는 마이크로서비스 시스템은 거의 없다. 왜?

**1. Blocking.** Phase 1에서 yes를 답한 participant는 commit이 결정될 때까지 lock을 잡고 대기한다. coordinator가 죽거나 응답이 늦어지면 그동안 자원이 잠긴다. 한 transaction이 1분 동안 lock을 잡으면, 그 자원을 쓰려는 다른 트랜잭션이 다 막힌다. 끔찍하다.

**2. SPOF (Single Point of Failure).** Coordinator가 죽으면 전체 트랜잭션이 stuck된다. Phase 2 명령이 안 와서, participant는 영원히 lock을 잡고 기다린다.

**3. Network Partition 취약성.** Network split이 나면 participant들이 서로 다른 결정을 받을 수 있다. 일관성이 깨진다.

**4. Throughput 한계.** Lock과 latency 때문에 throughput이 단일 DB의 1/10~1/100로 떨어진다. 마이크로서비스 환경에서 감당이 안 된다.

그래서 마이크로서비스 시대 이후로 2PC는 거의 자취를 감췄다. 대신 등장한 세 패턴이 Saga, Transactional Outbox, Event Sourcing이다. 이 셋이 각자 다른 방식으로 "분산 트랜잭션 없이도 일관성을 만드는" 길을 제시한다.

## Saga — 일련의 local transaction으로 분해

Saga는 1987년 Princeton에서 제안된 패턴인데, 마이크로서비스 시대에 다시 주목받았다. Chris Richardson의 *Microservices Patterns*가 가장 정리된 설명이다.

핵심 아이디어는 단순하다. **하나의 큰 분산 트랜잭션을 여러 개의 local transaction의 sequence로 분해한다.** 각 step은 자기 service의 DB에서 local로 commit한다. 중간에 실패하면 이미 commit된 step들을 **compensating action**(보상 작업)으로 되돌린다.

```
주문 처리 Saga:
  1. 재고 차감 (inventory service local commit)
  2. 결제 처리 (payment service local commit)
  3. 배송 등록 (shipping service local commit)
  
  실패 시 compensating action:
  1. 배송 등록 실패 → 결제 환불 + 재고 복원
  2. 결제 실패 → 재고 복원
```

이 모양에는 두 가지 변형이 있다.

### Choreography — 이벤트 기반 분산

각 service가 이벤트를 발행하고 다른 service가 그 이벤트에 반응한다. 중앙 조정자가 없다.

```
주문 service: OrderCreated 이벤트 발행
  ↓
재고 service: 이벤트 수신 → 재고 차감 → InventoryReserved 이벤트 발행
  ↓
결제 service: 이벤트 수신 → 결제 처리 → PaymentCompleted 이벤트 발행
  ↓
배송 service: 이벤트 수신 → 배송 등록
```

장점은 service들이 느슨하게 결합된다는 점. 새 service를 추가해도 기존 service는 모른다. 단점은 **전체 흐름 추적이 어렵다**는 점. 트랜잭션 하나가 어디까지 왔는지 보려면 여러 service의 로그를 다 모아 봐야 한다. 이른바 "event soup"가 만들어진다.

### Orchestration — 중앙 조정자

중앙의 **orchestrator**가 각 service에 명령을 보내고, 응답을 모아 다음 step을 결정한다.

```
Orchestrator:
  1. inventoryService.reserve(orderId) → 성공
  2. paymentService.charge(orderId) → 실패
  3. inventoryService.cancel(orderId) — 보상 실행
```

장점은 흐름이 한눈에 보인다는 점. orchestrator 한 곳만 보면 트랜잭션 상태를 알 수 있다. 단점은 orchestrator가 **SPOF**가 될 수 있다는 점, 그리고 orchestrator 자체의 복잡도가 커진다는 점이다.

대표 도구가 Camunda, Temporal, AWS Step Functions이다. 한국 핀테크에서는 Temporal이 빠르게 채택되고 있다.

### Choreography vs Orchestration

| 차원 | Choreography | Orchestration |
|------|-------------|---------------|
| 결합도 | 낮음 (이벤트로만 연결) | 높음 (orchestrator가 모두 알아야 함) |
| 가시성 | 낮음 (분산 로그) | 높음 (orchestrator 한 곳) |
| 새 step 추가 | 쉬움 (consumer만 추가) | orchestrator 코드 수정 |
| 실패 디버깅 | 어려움 | 쉬움 |
| 적합 규모 | 작은 service 수 (~5개) | 큰 service 수 또는 복잡한 흐름 |

작은 시스템은 choreography로 시작하고, service가 5개를 넘기 시작하면 orchestration으로 옮기는 편이 낫다. 흐름 추적이 어느 순간 운영의 최대 비용이 되기 시작한다.

### 보상 작업 설계의 함정

Saga의 가장 큰 함정이 **보상 작업이 항상 가능한 건 아니라는 사실**이다. 결제 환불은 가능하지만, 이미 발송된 알림은 취소가 불가능하다. 이미 출고된 상품은 회수가 어렵다.

이 한계를 풀어주는 패턴이 **세마틱 보상**이다. 진짜로 되돌리는 게 아니라, "되돌렸다는 상태"를 만든다. 알림을 취소할 수 없다면 "취소 알림"을 다시 보낸다. 출고된 상품을 회수할 수 없다면 "주문 취소 + 환불" 흐름으로 처리한다.

또 한 가지 — **보상 자체도 실패할 수 있다.** 보상 작업이 실패하면 어떻게 할까? 보통 retry + dead letter queue + 운영자 수동 개입 패턴이다. 이 모양이 10장 idempotency·retry·circuit breaker와 그대로 만난다.

> 💡 흔한 오해 — "Saga = 분산 트랜잭션 만능 해법." 실제로는 **보상 가능한 도메인에서만 작동**한다. 보상 불가능한 작업(이메일 발송, 알림, 외부 통신)이 끼면 saga 모델이 깨진다. 이런 경우 그 작업을 saga의 마지막에 두거나, "보상 없이 안전한" 다른 패턴(Outbox)으로 대체해야 한다.

## Transactional Outbox + CDC — Dual-Write 문제의 표준 답

가장 흔한 dual-write 시나리오를 다시 떠올려 보자.

```python
def create_order(order):
    db.insert(order)         # 성공
    kafka.send(event)        # 실패 → 메시지 안 감
```

DB에는 주문이 있는데 Kafka에는 이벤트가 없다. 다음 단계(결제·배송·알림)가 안 일어난다. 이걸 어떻게 안전하게 풀까?

**Transactional Outbox** 패턴이 사실상의 표준 답이다. 핵심 아이디어는 단순하다. **DB 트랜잭션 안에 메시지 자체를 outbox 테이블에 함께 insert한다.** 별도 워커가 outbox 테이블을 tail해 Kafka에 발행한다.

```python
def create_order(order):
    with db.transaction():
        db.insert(order)
        db.insert_outbox(event)  # 같은 트랜잭션
    # commit 끝, DB만 변경됨
    # 별도 worker가 outbox를 polling하거나 CDC로 tail
```

이 한 줄짜리 변경이 dual-write 문제를 통째로 해결한다. DB 트랜잭션이 atomic이니, order와 outbox row가 동시에 commit되거나 동시에 롤백된다.

별도 worker가 outbox를 처리하는 방법은 두 가지다.

### Polling 기반

worker가 일정 주기로 outbox 테이블을 SELECT해 미처리 row를 처리한다.

```python
while True:
    rows = db.query("SELECT * FROM outbox WHERE published=FALSE LIMIT 100")
    for row in rows:
        kafka.send(row.event)
        db.update("UPDATE outbox SET published=TRUE WHERE id=?", row.id)
    time.sleep(1)
```

장점은 단순함. 단점은 polling 주기에 따른 latency, 그리고 DB 부하.

### CDC (Change Data Capture) 기반

**Debezium** 같은 도구가 DB의 WAL(Write-Ahead Log) 또는 binlog를 tail해, 변경 사항을 Kafka로 자동 발행한다. polling 없이 거의 실시간 (~ms 단위).

```
Postgres WAL → Debezium → Kafka topic "outbox-events"
```

이 모양이 가장 우아하다. 거의 zero-latency, ordering 보존, DB 부하 최소. 한국 백엔드에서도 Debezium 채택이 늘고 있다.

Debezium 공식 문서의 한 줄이 그 가치를 정리한다.

> The Outbox Event Router SMT can be used to forward outbox events to a destination topic for asynchronous propagation, providing an at-least-once delivery guarantee. (Debezium docs)

### Polling vs CDC

| 차원 | Polling | CDC (Debezium) |
|------|---------|----------------|
| Latency | 초 단위 | ms 단위 |
| DB 부하 | 추가 query | log tail만 |
| 구현 복잡도 | 매우 단순 | Debezium·Kafka Connect 운영 필요 |
| Ordering | LIMIT 순서 | DB log 순서 자동 보존 |
| Throughput | 제한적 | 매우 높음 |

작은 시스템은 polling으로 충분하다. 마이크로서비스가 늘고 throughput이 커지면 CDC로 옮기는 편이 낫다.

### Outbox + Saga = 안전한 분산 흐름

Outbox와 Saga를 함께 쓰면 진짜 안전한 분산 흐름이 만들어진다. 각 step은 outbox로 다음 step을 트리거하고, 실패 시 compensating outbox로 보상한다.

```
주문 service:
  TRANSACTION:
    INSERT order
    INSERT outbox(OrderCreated event)
  
재고 service:
  consume(OrderCreated)
  TRANSACTION:
    UPDATE inventory SET qty = qty - 1
    INSERT outbox(InventoryReserved event)
  
결제 service:
  consume(InventoryReserved)
  ... 같은 패턴
```

이 모양은 어떻게 실패가 발생해도 다음 두 가지가 보장된다.

1. **로컬 DB와 outbox는 atomic.** DB가 변경되면 이벤트도 반드시 발행된다.
2. **At-least-once delivery.** 이벤트가 최소 한 번은 전달된다. 같은 이벤트가 두 번 와도 idempotent consumer가 한 번만 처리.

이 두 약속이 분산 시스템의 일관성을 만든다. **idempotent consumer**의 패턴은 10장에서 다룬 idempotency key가 그대로 사용된다. 10장과 11장이 한 쌍으로 작동하는 셈이다.

## Event Sourcing — State를 event log로 대체

세 번째 갈래가 **Event Sourcing**이다. 보다 깊은 패턴이고, 모든 시스템에 적용할 만한 패턴은 아니다.

전통적인 데이터 모델은 현재 state를 저장한다. "사용자 잔고 = 10,000원". Event Sourcing은 그 대신 모든 변경 이벤트를 저장한다.

```
event log:
  AccountCreated(userId=1, balance=0)
  DepositMade(userId=1, amount=10000)
  WithdrawMade(userId=1, amount=3000)
  DepositMade(userId=1, amount=3000)
```

현재 잔고를 알려면 event들을 순서대로 replay한다. 0 + 10000 - 3000 + 3000 = 10000원. 또는 snapshot을 주기적으로 만들어 그 위에 새 event만 replay하면 빠르다.

이 패턴의 장점이 크다.

**1. 완벽한 audit trail.** 모든 변경 history가 남는다. "왜 이렇게 됐지?"라는 질문에 항상 답할 수 있다.

**2. Time travel.** 특정 시점의 state를 재구성할 수 있다. "어제 오후 3시 사용자 잔고는?" 같은 질문에 답한다.

**3. CQRS와 자연스럽게 결합.** Write 모델은 event를 append, Read 모델은 event로부터 다양한 projection 생성.

**4. 새 view 추가가 쉽다.** 새 read model이 필요하면 event를 처음부터 replay해 새 view를 만든다.

하지만 Martin Fowler가 "신중하게 쓰라"고 경고한 이유도 있다.

> You should be very cautious about using CQRS... it can add significant complexity and make a significant drag on productivity. (Martin Fowler)

Event Sourcing의 함정은 다음과 같다.

**1. Event schema migration이 가장 어렵다.** Hugo Rocha가 자기 글에서 정확히 짚었다 — "event는 영원히 남는다." event schema를 한 번 정하면, 5년 전 event도 새 코드가 해석할 수 있어야 한다. 변경 시 versioning + upcasting 로직이 필요하다.

**2. Query가 직관적이지 않다.** "잔고가 500원 이하인 사용자 목록"을 알려면 모든 사용자의 event를 다 replay해야 한다. CQRS로 read model을 별도 두지 않으면 불가능하다.

**3. 학습 곡선이 가파르다.** 도메인 모델, event design, projection, snapshot, idempotency — 모두 새 개념. team이 이 모델에 익숙해지는 데 시간이 든다.

**4. event 폭증.** "사용자 매 클릭"을 다 event로 저장하면 storage가 폭증한다. 도메인의 의미 있는 결정만 event로 잡아야 한다.

그래서 Event Sourcing은 다음 도메인에서만 가치가 있다.

- **금융·회계.** audit trail이 법적 의무.
- **게임.** 사용자 행동 분석에 event log가 자연스럽다.
- **협업 도구.** time travel, undo가 핵심 기능.

일반 CRUD 도메인에는 과한 패턴이다. Fowler의 경고를 마음에 새기는 편이 낫다.

## 의사결정 트리 — 4가지 후보 패턴 중 무엇을 고를까

지금까지 살펴본 4가지 후보(2PC, Saga, Outbox+CDC, Event Sourcing)를 한 의사결정 트리로 정리하자.

```
분산 트랜잭션이 정말 필요한가?
├── No → 단일 DB에서 처리 (1장 RDB 참고)
└── Yes → 다음 질문
    
    Strong consistency가 critical한가? (예: 잔고 차감, 재고 동시 결정)
    ├── Yes, blocking 견딜 수 있음 → 2PC (드문 경우)
    └── Yes, blocking은 못 견딤 또는 No → Eventual consistency 패턴
        
        도메인의 step이 보상 가능한가?
        ├── No (이메일 발송, 알림 등) → Outbox + CDC (이벤트 발행만)
        └── Yes → Saga 가능
            
            service 수가 적은가? (~5개 이하)
            ├── Yes → Saga choreography (이벤트 기반)
            └── No → Saga orchestration (Temporal/Camunda)
        
        과거 모든 변경 history가 audit·time travel·undo에 필요한가?
        ├── Yes, 도메인이 금융·게임·협업 → Event Sourcing 검토
        └── No → 위 Saga/Outbox로 충분
```

이 트리에서 가장 자주 가는 길은 **Saga + Outbox 결합**이다. 각 step은 outbox로 다음 step 트리거, 실패 시 compensating outbox로 보상. 한국 백엔드의 대부분 분산 트랜잭션이 이 모양으로 가고 있다.

## 한국 사례 — 토스 코어뱅킹 SAGA + 2PC 혼합

한국에서 가장 자주 인용되는 분산 트랜잭션 사례가 토스 코어뱅킹이다. 토스 SLASH 23에서 공개된 발표에 따르면, 토스 뱅킹의 core transaction은 **SAGA와 2PC를 혼합**한 모델을 쓴다.

상황을 한 번 떠올려 보자. 토스에서 A 사용자가 B 사용자에게 송금한다. 두 사용자의 계좌가 같은 은행이면 한 DB 안에서 트랜잭션이라 단순. 그런데 토스에서는 마이크로서비스 분리로 인해 송금이 다음 service들을 거친다.

1. 송금 service: 송금 요청 검증
2. 계좌 service A: A의 잔고 차감
3. 계좌 service B: B의 잔고 추가
4. 거래 history service: 거래 기록
5. 알림 service: A·B에게 push

핵심 결정은 **2-4 사이는 SAGA, 그 안에서 가장 critical한 잔고 차감/추가는 2PC**라는 모양이다. 왜 이렇게 갈랐을까?

- **잔고 차감/추가의 strong consistency가 절대 critical.** A의 잔고가 줄었는데 B의 잔고가 안 늘면 그건 돈이 증발한 것이다. 절대 일어나면 안 된다. → 2PC로 atomic.
- **거래 history·알림은 eventual consistency 가능.** 거래 기록은 몇 초 늦어도 됨. 알림도 마찬가지. → SAGA로 비동기.

이 혼합 모델이 한국 핀테크의 가장 sophisticated한 패턴이다. 2PC를 완전히 안 쓰는 게 아니라, **2PC를 정말 필요한 좁은 범위로 한정**하고, 나머지는 SAGA로 푸는 것. 토스의 결정은 분산 시스템 설계의 정교한 균형을 보여 준다.

> 한 줄 통찰 — **모든 트랜잭션이 같은 일관성 수준을 요구하지 않는다.** 도메인별로 strong consistency가 진짜 필요한 경계를 찾고, 그 안에는 2PC를 쓰되, 그 밖에는 SAGA/Outbox로 푸는 편이 낫다.

## Saga·Outbox·Event Sourcing 도입 자격 5가지 질문

새 분산 시스템을 설계할 때 자기에게 던질 다섯이다.

1. **이 트랜잭션이 정말 분산이어야 하는가?** 단일 service·DB로 끝낼 수 있으면 그게 가장 단순한 답.
2. **strong consistency가 critical한가?** 잔고·재고 같은 도메인은 strong, 알림·로그 같은 도메인은 eventual.
3. **step들이 보상 가능한가?** 이메일·외부 알림이 끼면 saga 모델이 깨진다.
4. **service 수가 5개 이하인가?** choreography로 시작, 그 이상이면 orchestration(Temporal).
5. **event log가 도메인 가치를 만드는가?** 금융 audit, 게임 분석 같은 도메인 외에는 Event Sourcing은 과하다.

이 다섯에 답이 명확하지 않으면 일단 단일 DB + Outbox 패턴으로 시작하고, 한계가 오면 Saga를 추가하는 편이 낫다. 처음부터 Event Sourcing + CQRS + Saga를 다 깔면 운영 부담만 폭증한다.

## Callback 예고

11장의 세 패턴은 책 후반에 핵심 부품으로 반복 등장한다.

- **19장 결제·금융.** 토스 결제 critical path가 이 챕터의 SAGA + 2PC 모델을 그대로 활용. 외부 vendor failover + Saga + Outbox.
- **20장 이커머스.** 쿠팡 BFCM 주문 흐름이 Saga choreography 기반.

이 챕터의 의사결정 트리가 머릿속에 있어야 후속 케이스 스터디의 결정이 따라온다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 분산 트랜잭션의 네 후보 패턴이 손에 잡혀 있다. 2PC(이론은 깔끔, 실용은 거의 안 씀), Saga(choreography vs orchestration, 보상 가능 도메인 한정), Transactional Outbox + CDC(dual-write 문제의 표준 답), Event Sourcing(audit·time travel 도메인 한정). 토스 코어뱅킹의 SAGA + 2PC 혼합 모델까지가 한 묶음이다.

기억해두자. 분산 시스템에서 일관성은 무료가 아니다. strong consistency를 약속하면 blocking을, eventual을 받아들이면 보상 가능 도메인에 한정된다는 trade-off가 있다. **모든 트랜잭션을 같은 일관성 수준으로 다루지 말자.** 도메인별로 strong이 정말 필요한 좁은 범위를 찾고, 그 밖에는 Saga/Outbox로 푸는 편이 낫다.

다음 장에서는 합의·복제·일관성 모델을 깊이 들여다본다. CAP·PACELC·linearizability·causal·eventual — 이 단어들을 우리 도메인 언어로 다시 정의해 보자. Raft를 알면 무엇이 보이는지, Spanner·CockroachDB의 약속이 정확히 무엇인지 함께 짚자.
