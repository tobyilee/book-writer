# 15장. 데이터 파이프라인과 협업 동기화 — Lambda·Kappa·Dataflow + CRDT 짧게

어떤 회사가 데이터팀과 백엔드팀을 따로 운영하다가, 한 사건을 계기로 통합했다고 해보자. 광고 클릭 집계가 batch (1시간 지연)와 stream (실시간) 두 곳에서 달라져 광고주에게 환불을 해줘야 했던 사건이다. 같은 데이터의 두 진실은 종종 두 번째 사고를 낸다.

배치와 스트림은 정말 다른 일일까, 아니면 같은 일의 두 단면일까? 이 질문이 데이터 파이프라인 아키텍처 진화의 핵심에 있다. Lambda는 둘이 다르다고 가정하고 두 layer를 따로 운영했다. Kappa는 둘이 같다고 본다 — stream 하나로 통일하고 batch는 stream의 특수 case로 본다. Dataflow는 그 둘을 추상화로 통합했다.

그리고 이 챕터 뒤편에 또 다른 "데이터 합치기" 문제 — **multi-writer 협업의 동기화**가 있다. Figma·Linear·Notion 같은 협업 도구가 어떻게 여러 사용자의 동시 편집을 합치는가. CRDT라는 수학적 기반이 그 답을 만든다. 분산 파이프라인이 "여러 source의 진실"을 합친다면, CRDT는 "여러 writer의 진실"을 합친다. 같은 주제의 두 단면을 함께 살펴보자.

## Lambda Architecture — Batch + Speed + Serving 3-layer

Nathan Marz가 2011년경 제안한 **Lambda Architecture**는 한 시대의 데이터 파이프라인 default였다. 핵심 아이디어는 세 layer를 명시적으로 가르는 것.

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

이 모양의 가치가 분명하다. Batch는 **정확성**, Speed는 **저지연**. 둘을 합쳐 "1시간 전까지는 정확, 그 이후는 빠른 근사값"이라는 응답이 만들어진다.

대신 단점이 크다. **같은 비즈니스 로직을 두 layer에 두 번 짠다.** 광고 클릭 집계 로직이 MapReduce 코드 + Storm 코드로 두 번 존재. 둘이 미세하게 어긋나면 도입부의 광고 환불 사고가 일어난다. 이 코드 중복 비용을 누구나 한 번씩 겪고 나면 "다른 모양은 없을까"를 묻기 시작한다.

## Kappa Architecture — Stream 단일, Replay로 재처리

2014년 Jay Kreps(Confluent CEO)가 LinkedIn 시절 제안한 **Kappa Architecture**는 Lambda의 코드 중복을 정면으로 푼다. 아이디어 한 줄.

> Lambda의 batch layer를 없애자. stream layer 하나로 통일하자. 재처리가 필요하면 Kafka에서 replay하자.

Kafka의 retention 안에서 모든 데이터가 보존된다. 새 버전의 stream processor를 띄우면 offset 0부터 다시 consume해 view를 재구성할 수 있다. batch가 따로 필요 없다.

```
incoming data → Kafka (long retention)
                  ↓
              Stream processor (Flink, Kafka Streams)
                  ↓
              Materialized view (DB, Elasticsearch)

재처리 시: 새 processor 띄우고 offset 0부터 replay
```

이 모양이 우아한 이유가 두 가지다.

**1. 코드 하나.** 비즈니스 로직이 stream processor 안에 한 번만 있다. batch와 stream의 어긋남이 원천적으로 없다.

**2. 재처리가 자연스럽다.** 새 schema, 새 비즈니스 로직, 버그 수정 — 모두 replay로 처리. Kafka는 단순한 큐가 아니라 **immutable log**다.

대신 Kappa의 가정이 있다 — **모든 데이터가 Kafka에 충분히 retention된다.** 1년치 데이터 재처리가 필요하면 Kafka에 1년치 데이터가 있어야 한다. storage 비용 + 운영 부담이 크다. 그래서 hot data는 Kafka, cold data는 별도 storage(S3, HDFS)로 가는 hybrid 모델도 흔하다.

## Dataflow — 4축으로 batch와 stream을 통합

2015년 Google의 Tyler Akidau 등이 발표한 *The Dataflow Model* (P20)이 이 분야의 추상화를 한 단계 끌어올렸다. 핵심 통찰은 다음과 같다.

> batch와 stream은 다른 일이 아니다. 같은 4축의 다른 설정값이다.

4축은 이렇다.

**1. Event-time.** 이벤트가 실제로 일어난 시각. processing-time(시스템이 처리한 시각)과 구분.

**2. Watermark.** 시간 t 이전의 모든 데이터가 도착했다고 시스템이 추정하는 시점. 늦게 도착하는 데이터를 어떻게 다룰지 결정.

**3. Trigger.** 결과를 언제 emit할지. event-time watermark 도달 시, processing-time 주기, 데이터 수 기준 등.

**4. Accumulation.** 같은 window에 대해 결과를 누적할지(accumulating), 매번 새로 시작할지(discarding), 또는 둘 다(retracting).

이 4축을 적절히 설정하면 batch도 stream도 같은 코드로 처리된다. batch는 "모든 데이터가 도착한 후에 한 번 emit", stream은 "watermark마다 emit"의 차이일 뿐. **Apache Beam**이 이 추상화를 구현했고, Flink가 Beam 호환 runner를 제공해 사실상 표준이 됐다.

```python
# Beam 코드 — batch와 stream 모두 같은 코드
import apache_beam as beam

(pipeline
 | 'Read' >> beam.io.ReadFromKafka(...)  # 또는 ReadFromGCS for batch
 | 'Window' >> beam.WindowInto(FixedWindows(60))  # 1분 window
 | 'Count' >> beam.combiners.Count.PerKey()
 | 'Write' >> beam.io.WriteToBigQuery(...)
)
```

이 코드는 Kafka에서 stream으로 읽으면 stream 처리, GCS에서 batch로 읽으면 batch 처리. 같은 비즈니스 로직.

## 도구 풍경 — MapReduce부터 Flink까지

데이터 파이프라인 도구의 진화를 한 표로 정리하자.

| 도구 | 시기 | 모델 | 특징 |
|------|------|------|------|
| MapReduce (Google P16) | 2004 | Batch | Hadoop ecosystem 기반. 디스크 IO 무거움. |
| Spark RDD (P17) | 2010 | Batch + Micro-batch | 메모리 기반, lineage replay. iterative ML 강점. |
| Storm | 2011 | Stream | 초기 stream 처리, low-level API. |
| Spark Streaming | 2013 | Micro-batch (1초 단위) | Spark ecosystem 활용. true stream은 아님. |
| Flink (P18) | 2015 | True stream + batch as bounded stream | event-time, watermark, exactly-once. 현재 mainstream. |
| Kafka Streams | 2016 | Stream (library) | Kafka native, 가벼움, JVM에 임베디드. |
| Beam (Google P20) | 2016 | 추상화 layer | Flink/Dataflow/Spark runner 위에서 같은 코드. |

2026년 기준 현실적 선택은 다음과 같다.

- **단순 ETL batch:** Spark.
- **Real-time stream + complex logic:** Flink.
- **Kafka native, 가볍게:** Kafka Streams.
- **Multi-runner, portable:** Beam.
- **Cloud managed:** GCP Dataflow (Beam runner), AWS Kinesis Analytics for Apache Flink.

## Exactly-once의 진짜 의미 — Checkpoint와 Watermark

stream 처리에서 가장 자주 헷갈리는 개념이 exactly-once다. Flink는 "exactly-once"를 약속하는데, 그 약속의 정확한 의미가 뭘까?

**Flink의 exactly-once는 "state에 대한 보장"이다.** 메시지가 1번만 받아져 1번만 처리된다는 뜻이 아니다. 메시지는 여러 번 받을 수 있지만, **state 갱신은 정확히 한 번**만 적용된다.

이 보장을 가능하게 하는 메커니즘이 **checkpoint**다. Flink는 일정 주기(예: 10초)마다 전체 stream graph의 state를 distributed snapshot으로 저장한다. 장애 시 마지막 checkpoint로 복귀해 거기서부터 다시 처리. Kafka offset도 함께 저장되니, replay가 일관되게 일어난다.

```
T=0   메시지 1 처리, state 갱신
T=10  Checkpoint 1 저장 (state + Kafka offset)
T=15  메시지 2 처리, state 갱신
T=20  장애 발생!
T=21  Checkpoint 1로 복구, T=10 시점의 offset부터 다시 처리
      메시지 2를 또 받지만, state는 정확히 1번만 갱신된 효과
```

이 모양이 가능한 이유는 **state 자체가 checkpoint에 포함**되기 때문이다. application state가 외부에 있고, 그 외부 storage가 transactional하다면(예: Postgres) 같은 모델이 가능. Kafka transactional producer + idempotent consumer + transactional sink가 한 묶음일 때 진짜 end-to-end exactly-once.

**Watermark**는 또 다른 함정이다. "이 시간 t 이전 모든 데이터가 도착했다"고 추정하는 신호인데, 실제로는 늦게 도착하는 데이터(**late arrival**)가 있을 수 있다. 어떻게 다룰까?

- **Drop late data.** 단순. 일부 데이터 손실 감수.
- **Allowed lateness.** watermark 후에도 일정 시간(예: 1시간) window 유지. 그 안에 들어오면 window 결과 재계산.
- **Side output.** late data를 별도 stream으로 출력. 사후 처리.

이 결정은 도메인이 정한다. real-time analytics는 drop 가능, financial reconciliation은 절대 drop 불가. **"exactly-once + 0 loss"는 매우 좁은 가정의 보장**임을 마음에 새겨 두자.

## 한국 사례 — 카카오 광고·쿠팡 indexing pipeline

한국 백엔드에서 자주 인용되는 두 사례를 짚자.

**카카오 광고 추천 Kafka 기반 stream 파이프라인.** 카카오 광고팀이 if(kakao) 2021·2022에서 발표한 모델. 광고 클릭·노출 이벤트가 Kafka로 들어오고, Flink stream processor가 실시간으로 사용자 모델·광고주 모델을 갱신한다. ML model training과 serving이 분리되어, training pipeline은 batch (Spark), serving은 stream (Flink). batch + stream 두 layer가 같은 Kafka topic을 share하는 모양 — Kappa에 가깝다.

**쿠팡 검색 indexing pipeline.** 5장 검색 챕터에서 이미 짚었지만, 데이터 파이프라인 관점에서 다시 보자. 상품 변경 이벤트가 Kafka로 발행 → Flink가 실시간 indexing pipeline 실행 → Elasticsearch에 색인. 핵심 가치는 **decoupling + replay**. 검색 schema를 바꾸면 새 processor를 띄워 처음부터 replay. 운영 단순성과 확장성 둘을 다 잡은 패턴이다.

이 두 사례가 보여주는 한 가지 — **한국 백엔드의 데이터 파이프라인은 거의 Kappa로 정착 중이다.** Hadoop·MapReduce 기반 Lambda는 legacy로 남아 있고, 새 시스템은 Flink + Kafka 기반. Beam·Dataflow는 GCP 친화 팀에 한해 채택.

## CRDT — 협업 도구의 수학적 기반 (Sidebar)

여기서 잠시 시야를 협업 동기화로 옮기자. Figma·Linear·Notion·Linear 같은 협업 도구의 multi-writer 동기화는 분산 시스템의 흥미로운 자식이다.

상황을 가정해 보자. Figma 디자인 파일에서 두 사용자 A와 B가 동시에 같은 사각형의 색을 바꾼다. A는 빨강, B는 파랑. 네트워크 latency 때문에 두 변경이 거의 동시에 발생. 어떤 색이 최종 결과여야 할까?

이 문제를 푸는 자료구조가 **CRDT** (Conflict-free Replicated Data Type)다. Marc Shapiro 등이 2011년 정리한 *Conflict-free Replicated Data Types* (P11) 논문이 표준.

CRDT의 핵심 약속은 한 줄.

> 모든 replica가 같은 update들을 어떤 순서로 받든, 결국 같은 state로 수렴한다 (strong eventual consistency).

이게 가능한 이유는 update가 **commutative**(교환 가능)와 **idempotent**(중복 적용 가능)하기 때문이다. A의 update를 먼저 적용하든 B의 update를 먼저 적용하든, 결과가 같다. 같은 update를 두 번 적용해도 한 번 적용한 것과 같다.

### State-based vs Op-based CRDT

CRDT에는 두 모양이 있다.

**State-based (CvRDT).** replica들이 서로 state를 통째로 보내 merge한다. merge 함수가 semilattice의 join (commutative, associative, idempotent)이라는 수학적 보장이 핵심.

```
replica A: state_A = {red, ts=10}
replica B: state_B = {blue, ts=15}
merge(A, B) = {blue, ts=15}  -- LWW 기반 merge
```

**Op-based (CmRDT).** replica들이 operation 자체를 broadcast해, 다른 replica들이 같은 op을 적용. op들이 commutative하다는 보장이 핵심.

### 종류

CRDT의 대표적 종류들.

- **G-Counter:** grow-only counter. 증가만 가능.
- **PN-Counter:** positive-negative counter. 증감 모두 가능.
- **OR-Set (Observed-Remove Set):** set에서 add/remove. add가 remove를 이긴다.
- **LWW-Element-Set:** Last-Write-Wins set. timestamp 기반.
- **RGA (Replicated Growable Array):** text editing에 사용. Y.js, Automerge.

### CRDT를 쓰는 도구

- **Riak:** CRDT를 native data type으로.
- **Redis Enterprise:** CRDT module 제공.
- **Y.js, Automerge:** JavaScript CRDT 라이브러리. 협업 도구에서 가장 많이 사용.
- **Figma, Linear, Notion 일부:** 자체 CRDT-like 모델.

### OT — Operational Transform

CRDT의 경쟁자가 **OT** (Operational Transform)다. Google Docs가 2009년부터 쓰는 모델. 중앙 server가 각 client의 operation을 받아, 다른 client의 op과 transform해 일관성을 유지한다.

```
client A: insert "X" at position 5
client B: insert "Y" at position 3 (이미 적용된 op)
server: A의 op을 transform → "X" at position 6 (B의 insert 반영)
```

OT는 중앙 server가 필요하다(authoritative ordering). CRDT는 server 없이도 peer-to-peer로 가능 — local-first software의 핵심.

### "이 데이터는 CRDT가 어울리는가, OT면 충분한가" — 4가지 질문

1. **Offline 편집이 필요한가?** yes → CRDT. server 없이 local로 작업 후 나중에 sync.
2. **중앙 server가 가능한가?** yes → OT 가능. authoritative ordering으로 단순.
3. **데이터 타입이 자연스럽게 commutative한가?** counter·set은 쉬움. text·rich document는 어려움 (RGA, Yjs 같은 특수 자료구조 필요).
4. **conflict resolution을 사용자가 봐도 되는가?** no → CRDT가 자동 merge. yes → 단순 last-write-wins나 사용자 prompt.

Figma는 CRDT-like (offline 가능), Google Docs는 OT (server authoritative), Linear는 hybrid. 도구마다 결정이 다르다.

## 분산 파이프라인과 CRDT — 같은 주제의 두 단면

이 챕터의 한 줄 통찰을 정리하자. **분산 시스템은 결국 "여러 진실을 하나로 합치는" 문제다.**

- **분산 파이프라인**은 여러 source(events, batch records)의 진실을 하나의 view로 합친다. Lambda/Kappa/Dataflow가 그 모양.
- **CRDT/OT**는 여러 writer의 진실을 하나의 state로 합친다. Figma/Google Docs가 그 모양.

둘은 다른 영역처럼 보이지만 본질은 같다. 시간(event-time vs processing-time), 순서(causal happens-before), 충돌(merge function vs OT transform) 같은 개념이 양쪽에서 반복된다. 8장에서 다룬 Lamport happens-before가 양쪽의 토대다.

## 의사결정 — 5가지 차원

새 데이터 파이프라인을 설계할 때 자기에게 던질 다섯이다.

1. **Latency target?** real-time (ms~초) → Flink/Kafka Streams. near-real-time (분~시간) → Spark Streaming. batch (시간~일) → Spark.
2. **정확도 vs 속도?** financial → exactly-once 필수. analytics → at-least-once 또는 best-effort.
3. **재처리 빈도?** 자주 → Kappa (Kafka replay). 드물게 → Lambda 또는 Kappa 둘 다.
4. **운영 인력?** 작음 → managed (GCP Dataflow, AWS Kinesis). 큼 → self-hosted Flink.
5. **비용?** Kafka long retention은 비쌈. cold data는 S3 archive 검토.

이 다섯에 답이 명확하면 도구 선택은 자연스럽게 따라온다.

## Callback 예고

15장의 패턴은 후속 케이스 스터디에 등장한다.

- **17장 피드·타임라인.** Twitter·Instagram의 fanout이 stream processing 기반.
- **18장 검색·매칭·지오.** 매칭 시스템이 real-time stream으로 driver·passenger 상태 관리.
- **19장 결제·금융.** financial reconciliation에서 Lambda + 정확한 batch.
- **20장 이커머스.** 쿠팡 검색 indexing이 Kafka + Flink 기반.

## 마무리

이 챕터에서 우리는 데이터 파이프라인의 세 아키텍처(Lambda·Kappa·Dataflow), MapReduce부터 Flink까지의 도구 진화, exactly-once의 진짜 의미와 watermark의 함정, 카카오 광고·쿠팡 검색 indexing 사례를 살펴보았다. 그리고 sidebar로 CRDT·OT의 수학적 기반과 협업 도구의 결정 질문 4가지까지.

기억해두자. **분산 시스템은 결국 여러 진실을 합치는 문제다.** 그 합침의 방식이 도메인을 결정한다. real-time analytics는 Kappa, financial reconciliation은 정확한 Lambda, multi-writer 협업은 CRDT 또는 OT. 자기 도메인의 본질을 정확히 보고 도구를 고르는 편이 낫다.

다음 부에서는 3부 케이스 스터디로 넘어간다. 빌딩 블록과 패턴을 다 갖춘 우리가, 실제 시스템(채팅·피드·검색·결제·이커머스)을 어떻게 조립하는지 함께 본다. 그 시스템들에서 이 챕터의 stream + state 결합이 핵심 도구로 등장한다.
