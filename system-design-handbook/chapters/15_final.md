# 15장. 데이터 파이프라인과 협업 동기화 — Lambda·Kappa·Dataflow + CRDT 짧게

어느 광고 회사의 정산팀이 한 새벽에 비상 회의를 열었다고 해보자. 광고주가 "어제 우리가 본 클릭 수와 오늘 청구서의 클릭 수가 다릅니다"라고 항의해 왔다. 회사 내부의 batch 집계는 1시간 지연 후 정확한 숫자를 만드는데, 실시간 stream 집계는 그것보다 빠르게 다른 숫자를 보여 주고 있었다. 같은 데이터의 두 진실 — 한 쪽은 정확하지만 느리고, 한 쪽은 빠르지만 어긋난다.

이 풍경은 분산 시스템의 한 정직한 단면이다. **"이 데이터의 진실을 어디서 합칠 것인가"** 라는 질문은 옛 batch 시대부터 modern stream 시대까지 한 번도 사라지지 않았다. Lambda는 두 layer를 모두 두고 합쳤다. Kappa는 한 layer로 통일했다. Dataflow는 두 모드를 한 추상화로 묶었다. 이번 장에서는 그 진화의 한 줄을 짚어 보자. 그리고 마지막에 sidebar로 "여러 source의 진실"이 아닌 "여러 writer의 진실" — Figma·Linear 같은 협업 도구의 동기화 — 도 함께 들여다본다.

## 1. Lambda Architecture — batch + stream의 첫 번째 답

2011년, Nathan Marz가 *Big Data*라는 책에서 정리한 **Lambda Architecture**가 한 시대의 default가 됐다. 핵심 아이디어는 세 layer를 명시적으로 가르는 것이다.

```
incoming data
    │
    ├─→ Batch Layer (Hadoop MapReduce, Spark)
    │     - 모든 데이터를 처음부터 재처리
    │     - 정확하지만 1시간~1일 지연
    │     - precomputed view 생성
    │
    └─→ Speed Layer (Storm, Spark Streaming)
          - 최근 데이터만 처리
          - 빠르지만 정확도 trade-off
          - real-time view 생성

Serving Layer:
    Batch view + Speed view → 사용자 응답
```

이 모양의 가치는 분명하다. **batch는 정확성, speed는 저지연**. 둘을 한 자리에서 합쳐 "1시간 전까지는 정확, 그 이후는 빠른 근사"라는 응답을 만들어 낸다. 광고 클릭 집계·실시간 추천·금융 reconciliation 같이 두 시간축이 모두 필요한 도메인에 잘 어울렸다.

그런데 단점이 점점 커졌다. **같은 비즈니스 로직을 두 layer에 두 번 짠다.** 광고 클릭 집계 로직이 MapReduce 코드 + Storm 코드로 두 번 존재한다. 둘이 미세하게 어긋나면 도입부의 광고 환불 사고가 일어난다. 그리고 두 codebase를 평행하게 유지하는 운영 부담이 절대 만만치 않다. Lambda는 우아하지만 — 그 우아함이 일상의 부담으로 바뀌었다.

이 코드 중복을 한 번 겪고 나면 누구나 "다른 모양은 없을까"를 묻기 시작한다. 그 답이 2014년에 나왔다.

## 2. Kappa Architecture — stream 단일, replay로 재처리

2014년 Jay Kreps (당시 LinkedIn, 지금 Confluent CEO)가 *Questioning the Lambda Architecture*라는 글에서 정면으로 던졌다. **"Lambda의 batch layer를 없애자. stream 하나로 통일하자. 재처리가 필요하면 Kafka에서 replay하자."**

이게 **Kappa Architecture**다. 단순한 아이디어 같지만 깊은 결과를 만든다.

```
incoming data → Kafka (long retention)
                  ↓
              Stream processor (Flink, Kafka Streams)
                  ↓
              Materialized view (DB, Elasticsearch)

재처리 시: 새 processor 띄우고 offset 0부터 replay
```

이 모양이 우아한 이유는 두 가지다.

**1. 코드 하나.** 비즈니스 로직이 stream processor 안에 한 번만 있다. batch와 stream의 어긋남이 원천적으로 없다.

**2. 재처리가 자연스럽다.** 새 schema, 새 비즈니스 로직, 버그 수정 — 모두 replay로 처리된다. Kafka가 단순한 큐가 아니라 **immutable log of truth**가 되는 셈이다.

대신 Kappa의 가정이 분명하다. **모든 데이터가 Kafka에 충분히 retention된다.** 1년치 데이터 재처리가 필요하면 Kafka에 1년치 데이터가 있어야 한다. storage 비용 + 운영 부담이 만만치 않다. 그래서 hot data는 Kafka, cold data는 별도 storage(S3·HDFS)로 가는 hybrid 모델도 흔하다 — Confluent의 tiered storage가 그 답 중 하나다.

또 하나 — **stream processor의 정확성**이 핵심 변수가 된다. 이 점은 exactly-once 절에서 더 짚자.

## 3. Dataflow — 4축으로 batch와 stream을 통합하기

2015년 Google의 Tyler Akidau와 동료들이 발표한 *The Dataflow Model* (P20)이 이 분야의 추상화를 한 단계 더 끌어올렸다. 핵심 통찰은 직설적이다.

> batch와 stream은 다른 일이 아니다. 같은 4축의 다른 설정값이다.

4축은 다음과 같다.

**1. Event-time.** 이벤트가 실제로 일어난 시각. processing-time(시스템이 처리한 시각)과 분명히 구분한다. 8장에서 짚은 분산 시간 다루기가 여기에서도 그대로 적용된다.

**2. Watermark.** "시간 t 이전의 모든 데이터가 도착했다"고 시스템이 추정하는 시점. 늦게 도착하는 데이터(late arrival)를 어떻게 다룰지 결정하는 신호다.

**3. Trigger.** 결과를 언제 emit할지 결정한다. event-time watermark 도달 시, processing-time 주기, 데이터 수 기준 등 다양하게 설정할 수 있다.

**4. Accumulation.** 같은 window에 대해 결과를 누적할지(accumulating), 매번 새로 시작할지(discarding), 또는 둘 다 보낼지(accumulating + retracting)를 정한다.

이 4축을 적절히 설정하면 batch도 stream도 같은 코드로 처리된다. batch는 "모든 데이터가 도착한 후에 한 번 emit", stream은 "watermark마다 emit"의 차이일 뿐이다. **Apache Beam**이 이 추상화를 구현했고, Flink가 Beam 호환 runner를 제공하면서 사실상 산업 표준이 됐다.

```python
# Beam — batch와 stream 모두 같은 코드
import apache_beam as beam

(pipeline
 | 'Read' >> beam.io.ReadFromKafka(...)  # 또는 ReadFromGCS for batch
 | 'Window' >> beam.WindowInto(FixedWindows(60))  # 1분 window
 | 'Count' >> beam.combiners.Count.PerKey()
 | 'Write' >> beam.io.WriteToBigQuery(...))
```

이 코드는 Kafka에서 stream으로 읽으면 stream 처리, GCS에서 batch로 읽으면 batch 처리. 같은 비즈니스 로직이 두 모드를 모두 책임진다. **batch = bounded stream**이라는 한 줄이 modern 데이터 파이프라인의 mental model이다.

## 4. 도구의 풍경 — MapReduce에서 Flink까지

이 진화를 도구 시점으로 한 표에 정리해 보자.

| 도구 | 시기 | 모델 | 핵심 특징 |
|------|------|------|-----------|
| MapReduce (P16) | 2004 | Batch | Hadoop ecosystem. disk I/O 무거움. |
| Spark RDD (P17) | 2010 | Batch + Micro-batch | 메모리 기반, lineage replay. iterative ML 강점. |
| Storm | 2011 | Stream | 초기 stream 처리, low-level API. |
| Spark Streaming | 2013 | Micro-batch (1초 단위) | Spark ecosystem 활용. true stream은 아님. |
| Flink (P18) | 2015 | True stream + bounded batch | event-time, watermark, exactly-once. 현재 mainstream. |
| Kafka Streams | 2016 | Stream (library) | Kafka native, JVM에 임베디드, 운영 가볍다. |
| Beam (P20) | 2016 | 추상화 layer | Flink·Dataflow·Spark runner 위에서 같은 코드. |

2026년 기준 현실적 선택은 도메인마다 다르다.

- **단순 ETL batch**: Spark.
- **Real-time stream + complex logic**: Flink.
- **Kafka native·가볍게 시작**: Kafka Streams (library 형태, JVM application에 임베드).
- **Multi-runner·portable**: Beam.
- **Cloud managed**: GCP Dataflow (Beam runner), AWS Kinesis Analytics for Apache Flink.

표 한 장으로 정리하면 깔끔해 보이지만, 정작 production에서는 **어느 도구를 쓰느냐보다 그 도구를 정확히 운영하는 능력**이 더 큰 변수다. 그 운영의 핵심이 exactly-once와 watermark다.

## 5. Exactly-once의 진짜 의미 — checkpoint와 watermark

stream 처리에서 가장 자주 헷갈리는 단어가 **exactly-once**다. Flink는 "exactly-once"를 약속하는데, 그 약속의 정확한 의미가 뭘까?

**Flink의 exactly-once는 "state에 대한 보장"이다.** 메시지가 1번만 받아져 1번만 처리된다는 뜻이 아니다. 메시지는 여러 번 받을 수 있지만, **state 갱신은 정확히 한 번**만 적용된다는 보장이다.

이 보장을 가능하게 하는 메커니즘이 **checkpoint**다. Flink는 일정 주기(예: 10초)마다 전체 stream graph의 state를 distributed snapshot으로 저장한다. 장애가 나면 마지막 checkpoint로 복귀해 거기서부터 다시 처리. Kafka offset도 함께 저장되니, replay가 일관되게 일어난다.

```
T=0   메시지 1 처리, state 갱신
T=10  Checkpoint 1 저장 (state + Kafka offset)
T=15  메시지 2 처리, state 갱신
T=20  장애 발생!
T=21  Checkpoint 1로 복구, T=10 시점의 offset부터 다시 처리
      → 메시지 2를 또 받지만, state는 정확히 1번만 갱신된 효과
```

이 모양이 가능한 이유는 **state 자체가 checkpoint에 포함**되기 때문이다. application state가 외부에 있고 그 외부 storage가 transactional하다면(예: Postgres) 같은 모델이 가능하다. **Kafka transactional producer + idempotent consumer + transactional sink**가 한 묶음일 때 비로소 진짜 end-to-end exactly-once다. 한 layer만 빠져도 깨진다 — 그래서 운영 단순함이 가장 큰 비결이다.

### Watermark의 함정 — late arrival을 어떻게 다룰까

**Watermark**는 또 다른 함정이다. "이 시간 t 이전 모든 데이터가 도착했다"고 추정하는 신호인데, 실제로는 늦게 도착하는 데이터(**late arrival**)가 있을 수 있다. 어떻게 다룰까?

- **Drop late data.** 단순. 일부 데이터 손실을 감수한다.
- **Allowed lateness.** watermark 후에도 일정 시간(예: 1시간) window를 유지한다. 그 안에 들어오면 window 결과를 재계산한다.
- **Side output.** late data를 별도 stream으로 출력한다. 사후 처리 책임이 application에 남는다.

이 결정은 도메인이 정한다. real-time analytics는 drop 가능, financial reconciliation은 절대 drop 불가. **"exactly-once + 0 loss"는 매우 좁은 가정의 보장**임을 마음에 새겨 두는 편이 낫다. 도구가 약속하는 단어를 그대로 믿지 말고, 우리 도메인에서 정확히 무엇이 보장되는지 한 번 더 확인하자 — 그게 새벽 alert이 줄어드는 길이다.

## 6. 한국 사례 — 카카오 광고 stream과 쿠팡 검색 indexing

한국 백엔드에서 자주 인용되는 두 사례를 짚어 두자.

**카카오 광고 추천 Kafka 기반 stream 파이프라인.** 카카오 광고팀이 if(kakao) 2021·2022 발표에서 정리한 모델이다 (W33). 광고 클릭·노출 이벤트가 Kafka로 들어오고, Flink stream processor가 실시간으로 사용자 모델·광고주 모델을 갱신한다. ML model training과 serving이 분리돼 — training pipeline은 batch (Spark), serving은 stream (Flink). batch + stream 두 layer가 같은 Kafka topic을 공유하는 모양으로, 본질적으로는 Kappa에 가깝다.

여기서 흥미로운 점은 — **"clicks가 진짜 사용자에게 보여줬을 때만 카운트한다"**는 정합성 조건을 위해 stream pipeline 안에서 "노출 이벤트 도착 후에야 클릭 이벤트가 활성화되는" join 로직이 들어 있다는 것이다. event-time과 watermark 설정이 production에서 자주 데이는 자리라는 점을 카카오 발표가 정직하게 짚는다 (검증 필요 — 발표 원문 확인 권장).

**쿠팡 검색 indexing pipeline.** 5장 검색 챕터에서 이미 짚었지만 데이터 파이프라인 관점에서 다시 보자 (W32). 상품 변경 이벤트가 Kafka로 발행되고 Flink가 실시간 indexing pipeline을 실행해 Elasticsearch에 색인한다. 핵심 가치는 **decoupling + replay**다. 검색 schema를 바꾸면 새 processor를 띄워 처음부터 replay하면 된다. 운영 단순성과 확장성을 둘 다 잡은 패턴이다.

이 두 사례가 보여 주는 한 가지 — **한국 백엔드의 데이터 파이프라인은 거의 Kappa로 정착 중이다.** Hadoop·MapReduce 기반 Lambda는 legacy로 남아 있고, 새 시스템은 Flink + Kafka 기반이다. Beam·Dataflow는 GCP 친화 팀에 한해 채택하는 정도다.

## 7. 의사결정 — 5가지 차원

새 데이터 파이프라인을 설계할 때 자기에게 던질 다섯 질문이다.

1. **Latency target?** real-time (ms~초) → Flink·Kafka Streams. near-real-time (분~시간) → Spark Streaming. batch (시간~일) → Spark.
2. **정확도 vs 속도?** financial → exactly-once 필수. analytics → at-least-once 또는 best-effort 가능.
3. **재처리 빈도?** 자주 → Kappa (Kafka replay). 드물게 → Lambda 또는 Kappa 둘 다 가능.
4. **운영 인력?** 작음 → managed (GCP Dataflow, AWS Kinesis Analytics, Confluent Cloud). 큼 → self-hosted Flink.
5. **비용?** Kafka long retention은 비싸다. cold data는 S3 archive로 옮기는 hybrid 검토.

이 다섯에 답이 명확하면 도구 선택은 자연스럽게 따라온다. 정답을 도메인 언어로 답할 수 있어야 그 결정이 운영의 새벽 alert에서도 무너지지 않는다.

## 8. CRDT — 협업 도구의 수학적 기반 (Sidebar 4p)

여기서 잠시 시야를 협업 동기화로 옮겨 보자. Figma·Linear·Notion 같은 협업 도구의 multi-writer 동기화는 분산 시스템의 또 다른 흥미로운 자식이다.

상황을 가정해 보자. Figma 디자인 파일에서 두 사용자 A와 B가 동시에 같은 사각형의 색을 바꾼다. A는 빨강, B는 파랑. 네트워크 latency 때문에 두 변경이 거의 동시에 발생한다. 어떤 색이 최종 결과여야 할까? 이게 단순한 last-write-wins 문제 같지만, offline 편집·peer-to-peer 동기화·중앙 server 없이 작동하는 시스템에서는 답이 훨씬 까다로워진다.

이 문제를 푸는 자료구조가 **CRDT** (Conflict-free Replicated Data Type)다. Marc Shapiro와 동료들이 2011년 정리한 *Conflict-free Replicated Data Types* (P11) 논문이 표준이다.

### CRDT의 핵심 약속

> 모든 replica가 같은 update들을 어떤 순서로 받든, 결국 같은 state로 수렴한다 (strong eventual consistency).

이게 가능한 이유는 update가 **commutative**(교환 가능)이고 **idempotent**(중복 적용 가능)하기 때문이다. A의 update를 먼저 적용하든 B의 update를 먼저 적용하든 결과가 같다. 같은 update를 두 번 적용해도 한 번 적용한 것과 같다. 12장에서 본 **CALM theorem** — "coordination-free = monotonic" — 이 정확히 이 결과의 이론적 토대다.

### State-based vs Op-based

CRDT에는 두 모양이 있다.

**State-based (CvRDT).** replica들이 서로 state를 통째로 보내 merge한다. merge 함수가 semilattice의 join 연산 (commutative·associative·idempotent)이라는 수학적 보장이 핵심이다. 운영이 단순하지만 state가 클수록 네트워크 비용이 커진다.

**Op-based (CmRDT).** replica들이 operation 자체를 broadcast하고, 다른 replica들이 같은 op을 적용한다. op들이 commutative하다는 보장이 필요하다. 네트워크는 가볍지만, op delivery 보장(at-least-once + idempotent)이 까다롭다.

### 자주 쓰이는 CRDT 자료구조

- **G-Counter:** grow-only counter. 증가만 가능 — 좋아요 수 카운터 같은 자리.
- **PN-Counter:** positive-negative counter. 증감 모두 가능 — 좋아요 토글 가능한 자리.
- **OR-Set (Observed-Remove Set):** set에서 add/remove. add가 remove를 이긴다. Notion 댓글 같이 "한 번이라도 등장한 댓글은 가능한 한 살린다" 정책.
- **LWW-Element-Set:** Last-Write-Wins set. timestamp 기반. 단순하지만 시계 어긋남에 약하다 (8장 NTP step 참고).
- **RGA (Replicated Growable Array):** 텍스트 편집에 사용. Y.js·Automerge가 이걸 구현.

### 누가 CRDT를 쓰는가

- **Riak**: CRDT를 native data type으로 제공.
- **Redis Enterprise**: Active-Active CRDT module.
- **Y.js·Automerge**: JavaScript CRDT 라이브러리. 협업 도구에서 가장 많이 쓰인다.
- **Figma·Linear·Notion 일부**: 자체 CRDT-like 모델로 multi-writer 합치기.

### OT — Operational Transform과의 비교

CRDT의 경쟁자가 **OT (Operational Transform)**다. Google Docs가 2009년부터 쓰는 모델로, 중앙 server가 각 client의 operation을 받아 다른 client의 op과 transform해서 일관성을 유지한다.

```
client A: insert "X" at position 5
client B: insert "Y" at position 3 (이미 적용된 op)
server: A의 op을 transform → "X" at position 6 (B의 insert 반영)
```

OT는 **중앙 server**가 필요하다 (authoritative ordering). CRDT는 server 없이도 peer-to-peer로 가능하다 — 이게 **local-first software** (자료 28)의 핵심이다. offline 편집 후 나중에 sync하는 식의 워크플로우가 CRDT 위에서 자연스럽게 작동한다.

### "이 데이터는 CRDT가 어울리는가, OT면 충분한가" — 4가지 질문

도메인을 보고 둘 중 하나를 결정해야 할 때 던질 네 질문이다.

1. **Offline 편집이 필요한가?** Yes → CRDT. server 없이 local로 작업한 뒤 나중에 sync 가능.
2. **중앙 server가 가능한가?** Yes → OT. authoritative ordering으로 구현이 단순.
3. **데이터 타입이 자연스럽게 commutative한가?** counter·set은 쉽다. text·rich document는 어려워서 RGA·Yjs 같은 특수 자료구조가 필요.
4. **conflict resolution을 사용자가 봐도 되는가?** No → CRDT가 자동 merge. Yes → 단순 last-write-wins나 사용자 prompt도 가능.

Figma는 CRDT-like (offline 가능), Google Docs는 OT (server authoritative), Linear는 hybrid다. 도구마다 결정이 다르고, 그 결정이 사용자 경험을 본질적으로 가른다.

## 9. 분산 파이프라인과 CRDT — 같은 주제의 두 단면

이 챕터의 한 줄 통찰을 정리해 보자. **분산 시스템은 결국 "여러 진실을 하나로 합치는" 문제다.**

- **분산 파이프라인**은 여러 source(events·batch records)의 진실을 하나의 view로 합친다. Lambda/Kappa/Dataflow가 그 모양.
- **CRDT/OT**는 여러 writer의 진실을 하나의 state로 합친다. Figma/Google Docs가 그 모양.

둘은 다른 영역처럼 보이지만 본질은 같다. **시간(event-time vs processing-time), 순서(causal happens-before), 충돌(merge function vs OT transform)** 같은 개념이 양쪽에서 반복된다. 8장에서 다룬 Lamport happens-before가 양쪽의 토대이고, 12장의 CALM theorem이 CRDT의 이론적 근거였다 — 이 챕터는 그 이론들이 production에서 어떻게 작동하는지를 두 측면에서 보여 준다.

기억해 두자. **합치는 방식이 도메인을 정의한다.** real-time analytics는 Kappa, financial reconciliation은 정확한 Lambda, multi-writer 협업은 CRDT 또는 OT. 자기 도메인의 본질을 정확히 보고 도구를 고르는 편이 낫다.

## 10. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 데이터 파이프라인의 세 갈래와 협업 동기화의 두 모양이 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **Lambda Architecture** — batch + speed 두 layer. 정확성·저지연 둘 다 잡지만 코드 중복이 비싸다. financial reconciliation 같은 자리에 여전히 유효.
- **Kappa Architecture** — stream 단일 + Kafka replay. 코드 하나 + 재처리 자연스러움. 한국 백엔드의 default. Kafka long retention 비용을 받아들이는 게 조건.
- **Dataflow 4축** — event-time·watermark·trigger·accumulation. batch = bounded stream의 mental model. Apache Beam이 그 추상화.
- **현재 mainstream은 Flink + Kafka.** Beam·Dataflow는 GCP 친화 팀. Spark는 batch ETL에 여전.
- **Exactly-once는 state 보장**이지 메시지 보장이 아니다. checkpoint + transactional sink가 한 묶음일 때만 진짜 end-to-end exactly-once.
- **Watermark + late arrival**은 도메인이 정하는 결정. 단순 drop·allowed lateness·side output 세 갈래. 도구가 약속하는 단어를 그대로 믿지 말자.
- **CRDT는 coordination-free 동기화의 수학적 기반**이다. monotonic 자료구조 + commutative op = 충돌 없이 수렴.
- **OT vs CRDT** — server authoritative면 OT, peer-to-peer·offline-first면 CRDT. 네 질문으로 갈라진다.
- **한 줄 통찰** — 분산 시스템은 결국 진실을 합치는 문제다. 그게 새벽 3시의 자신을 살린다.

여기까지가 2부의 마지막 챕터다. 빌딩 블록(1부)과 분산 시스템 패턴(2부)을 모두 갖춘 우리가, 다음 부에서는 **케이스 스터디**로 넘어간다. 채팅(16장) → 피드(17장) → 검색·매칭(18장) → 결제(19장 클라이맥스) → 이커머스(20장). 우리가 익힌 도구들이 실제 시스템에서 어떤 조합으로 등장하는지, 같이 들여다보자.

---

<!-- frontmatter -->
- 챕터 번호: 15 (plan §3 정렬 — 보안 9장 1부 편입으로 +1 shift 후 15장)
- 분량 추정: 한국어 약 14,800자 (≈ 20페이지)
- 본문 인용 reference: §3.10 데이터 파이프라인 · §3.14 CRDT/OT · §3.13 Replication · 자료 28 local-first, P11 Shapiro CRDT · P16 MapReduce · P17 Spark RDD · P18 Flink · P19 Pulsar/Kafka · P20 Dataflow, W18 Kleppmann CRDT · W20 Kai Waehner · W32 쿠팡 검색 · W33 카카오 광고, 8장 Lamport happens-before callback, 12장 CALM theorem callback, 16~20장 케이스 callback 예고
- 계획서와 다르게 간 점: 02_plan §3 15장(plan 표기상 15장) 모든 항목 커버. CRDT sidebar 4p 분량 유지. 의사결정 트리 5문항·"한 줄 통찰" baseline + "그게 새벽 3시의 자신을 살린다" 한 줄을 회수 절에 다시 박아 책 전체 톤 일관.
<!-- 개정: 2026-05-16 plan §3 매핑 정렬 (보안 9장 1부 편입으로 +1 shift 후 15장). 기존 15_draft.md(다른 writer 작품)는 15_draft_preexisting.md로 백업. team-lead 지시("#16 claim 후 chapters/15_draft.md로 저장")에 따라 새 draft로 작성. -->
