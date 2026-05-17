# 14장. Rate Limiting·백프레셔·SLO·관측성·on-call — 시스템이 자기 자신을 보는 법

어떤 팀의 alert가 새벽 3시에 울렸다고 해보자. on-call 엔지니어가 컴퓨터를 켜고 보니, 5분 안에 자동 해결된 일이었다. 같은 alert가 그 주에만 11번 울렸다. 한 달 뒤 그 엔지니어는 퇴사했다.

on-call burnout은 alert 설계의 실패다. 사람을 깨우는 모든 page는 그만한 가치가 있어야 한다. Charity Majors의 한 줄이 정확히 짚었다 — "**3am에 사람이 할 게 없으면 page 보내지 마라**." 이 한 문장이 운영 문화의 핵심이고, 동시에 우리 시스템이 자기 자신을 보는 능력의 척도다.

시스템이 자기 한계를 표현하는 5가지 도구가 있다. Rate limiting, backpressure, SLO/Error Budget, 관측성 3-pillar, 배포 전략, chaos engineering. 그리고 그 위에 얹히는 운영 문화 — blameless postmortem, on-call humanism. 빌딩 블록과 패턴을 다 갖춘 시스템이 production에서 살아남으려면 이 도구들이 모두 깔려 있어야 한다. 한 박자씩 짚어 보자.

## Rate Limiting — 자기 처리량을 외부에 알리는 법

Rate limiting은 시스템이 "나는 분당 N개까지만 처리할 수 있다"고 외부에 선언하는 도구다. 잘 깔린 rate limiter는 시스템 한계 이상의 트래픽이 들어오기 전에 일부를 거절(429 Too Many Requests)해, 시스템 자체가 무너지지 않게 한다.

Cloudflare 사내 블로그가 정리한 5가지 알고리즘을 보자.

### 1. Token Bucket — Default

매 초 N개씩 token이 bucket에 추가된다. 요청이 올 때마다 token 1개를 꺼낸다. bucket이 비면 거절.

```
bucket capacity: 100 (burst 허용)
refill rate: 10/sec
요청 들어옴 → token 1개 차감 (남으면 통과, 없으면 거절)
```

장점: **burst 허용**. 순간 burst가 와도 capacity 안에서는 통과. AWS API의 client-side throttling이 이 모델이다.

### 2. Leaky Bucket — Constant Egress

요청을 큐에 쌓고, 일정 속도로만 처리. burst가 와도 출력 속도는 일정.

```
incoming → queue → constant rate output
```

장점: **smooth output**. 단점: burst 거부, queue가 가득 차면 drop.

### 3. Fixed Window

1분 단위로 카운터. "이 분에 100개 처리"하면 다음 요청은 다음 분까지 거절.

```
00:00 - 00:59: 100 requests
01:00 - 01:59: 카운터 reset
```

단점: **boundary burst 문제**. 00:59에 100개 + 01:00에 100개 = 1초 안에 200개 가능.

### 4. Sliding Window Log — 정확

모든 요청의 timestamp를 저장. 최근 1분 안의 요청 수가 임계 넘는지 체크.

```
log = [00:01, 00:15, 00:42, ...]
새 요청 시 1분 이전 timestamp 모두 삭제 + 남은 수 체크
```

장점: 가장 정확. 단점: **메모리 비싸다**. 요청마다 timestamp 저장.

### 5. Sliding Window Counter — Cloudflare Default

두 fixed window의 가중평균.

```
현재 window 카운트 + (이전 window 카운트 × 남은 시간 비율)
```

Cloudflare 실측 0.003% error로 사실상 표준. 정확도와 메모리 효율의 균형.

| 알고리즘 | burst 허용 | 정확도 | 메모리 | 추천 |
|---------|-----------|--------|--------|------|
| Token bucket | yes | medium | 작음 | 일반 API default |
| Leaky bucket | no | high | 중간 | smooth output 필요 시 |
| Fixed window | yes (boundary) | 낮음 | 작음 | 단순 구현 |
| Sliding window log | yes | 매우 높음 | 큼 | 정확도 critical |
| Sliding window counter | yes | 매우 높음 | 작음 | **default 권장** |

### 분산 Rate Limit 구현

여러 server가 같은 limit을 공유하려면 중앙 카운터가 필요하다. Redis가 표준이다.

```lua
-- Lua script (atomic)
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local current = redis.call('INCR', key)
if current == 1 then
    redis.call('EXPIRE', key, 60)  -- 1분 window
end
if current > limit then
    return 0  -- 거절
end
return 1  -- 통과
```

Lua script로 INCR + EXPIRE를 atomic하게 처리한다. 분산 server들이 모두 같은 Redis key를 보니 글로벌 rate limit이 자연스럽게 가능하다.

복잡한 시스템에서는 **hierarchical token bucket**을 쓴다 — 전역 limit, 사용자별 limit, endpoint별 limit이 계층적으로 적용. AWS API Gateway가 이 모델이다.

## 백프레셔 — Producer가 Consumer를 살린다

Rate limiting이 "외부 → 우리"의 흐름을 제어하면, **백프레셔**(backpressure)는 "우리 내부의 빠른 producer → 느린 consumer" 흐름을 제어한다.

상황을 가정해 보자. service A가 service B에 1초에 1000개 메시지를 보낸다. B는 100개밖에 처리 못한다. A는 어떻게 알 수 있을까?

답은 **B가 A에게 "천천히"라고 말하는 것**이다. 그 신호가 백프레셔다.

표준 패턴들이 있다.

**1. Reactive Streams.** Java 9+, Node.js, Project Reactor의 표준. consumer가 producer에게 `request(N)`을 보내 N개만큼만 요청. consumer가 처리 가능할 때만 다음 N개.

**2. gRPC Flow Control.** HTTP/2 기반의 flow control. 각 stream에 window size가 있고, consumer가 ACK 보낼 때까지 producer가 새 데이터를 못 보냄.

**3. Kafka Consumer Poll Throttling.** consumer가 poll 속도를 조절. lag이 쌓이면 fetch 빈도를 줄임. broker가 backpressure 신호를 producer로 전달하지는 않지만, lag 모니터링으로 producer 측에서 결정.

**4. Queue 길이.** 가장 단순. consumer 앞의 큐 길이가 임계 넘으면 producer에 "stop"을 보낸다. 큐 길이가 시스템 건강의 1차 신호.

> 💡 큐 길이의 한 줄 통찰 — **producer는 queue 길이를 보고 자기 속도를 결정하라.** consumer의 처리 속도가 아니라 queue 길이로 판단해야 한다. consumer가 일시적으로 빠르더라도 queue가 차 있으면 system이 따라가지 못하는 것.

## SLI / SLO / Error Budget — "100%는 잘못된 목표다"

Google SRE Book이 분산 시스템 운영의 표준을 정립했다. 가장 큰 기여 중 하나가 **SLI / SLO / Error Budget**이라는 어휘다.

- **SLI (Service Level Indicator):** 시스템 건강 지표. "성공률", "p99 latency", "처리량".
- **SLO (Service Level Objective):** SLI의 목표값. "성공률 99.9%", "p99 latency < 500ms".
- **SLA (Service Level Agreement):** 외부 약속, 위반 시 비용 (보통 환불). SLO보다 약간 느슨하게.
- **Error Budget:** 100% - SLO. "한 달에 0.1% (43분) 동안 장애 허용."

이 어휘의 가장 큰 통찰은 — **100%는 잘못된 목표다.**

100% 안정성은 무한 비용이다. 99.99% (year에 52분 다운)에서 99.999% (5분 다운)로 가려면 비용이 10배 든다. 사용자 대부분은 그 차이를 못 느낀다. 그래서 SLO를 90%·95%·99%·99.9% 등 도메인에 맞춰 정하고, **그 안의 error budget을 새 기능 출시에 자유롭게 쓴다**는 모델이 합리적이다.

```
SLO 99.9% → error budget 0.1% (한 달 43분)

이번 달:
- 신규 기능 배포로 12분 장애
- 인프라 장애로 8분
- 합계 20분 사용 (남은 budget 23분)
→ 자유롭게 새 기능 배포 가능

다음 달:
- 큰 장애로 50분 다운
→ budget 초과 → 새 기능 freeze, 안정성에 집중
```

이 모양이 **release 속도와 안정성의 협상 테이블**이다. SRE팀이 "더 안전하게"라고만 외치고 product팀이 "더 빨리"라고만 외치면 갈등이 끝나지 않는다. error budget이 그 갈등을 데이터로 풀어 준다.

### Burn Rate Alerting

SLO를 모니터링할 때 단순 임계 alerting은 함정이 많다. "99.9% 미만이면 alert"는 noisy alert를 만든다.

표준은 **multi-window multi-burn-rate alerting**이다. error budget을 소진하는 속도를 본다.

```
fast burn (1시간 window):
  1시간 안에 한 달치 budget의 2%를 소진 → 즉시 page

slow burn (6시간 window):
  6시간 안에 한 달치 budget의 5%를 소진 → 1시간 후 page

dlow burn (3일 window):
  3일 안에 한 달치 budget의 10%를 소진 → 다음 영업일 ticket
```

이 multi-window는 fast/slow burn 각각에 맞는 응답을 만든다. 빠른 장애엔 page, 느린 누수엔 ticket. 새벽 3시에 ticket으로 깨지 않는다.

## Three Pillars of Observability — Logs · Metrics · Traces

시스템이 자기 상태를 외부에 보여 주는 3가지 차원이 **logs, metrics, traces**다.

| 차원 | 무엇을 본다 | 대표 도구 |
|------|-----------|---------|
| Logs | 어떤 일이 일어났는가 (events) | ELK·Loki·CloudWatch |
| Metrics | 얼마나 자주·어느 정도 (aggregations) | Prometheus·Datadog |
| Traces | 한 요청이 어디를 거쳤는가 (request flow) | Jaeger·Zipkin·OpenTelemetry |

이 셋이 보완 관계다. 한 가지만 가지고는 production 디버깅이 어렵다.

### OpenTelemetry — vendor lock-in 깨기

2022년경부터 CNCF 표준이 된 **OpenTelemetry**가 관측성 영역에 큰 변화를 만들었다. 핵심은 **OTLP wire format으로 logs·metrics·traces를 통일**한 것.

```
application → OpenTelemetry SDK → OTLP → OTel Collector → 어떤 backend든
```

application code는 OTel SDK만 알면 된다. Collector가 batching·filtering·routing을 처리하고, 어느 backend(Datadog·NewRelic·Jaeger·Prometheus)든 보낼 수 있다. vendor lock-in이 깨졌다.

그리고 가장 강력한 기능이 **trace_id correlation**이다. 한 요청에 trace_id가 부여되면, 그 trace_id가 logs·metrics·traces에 모두 박힌다. 한 요청을 따라가면서 3 pillar를 한 화면에서 본다.

### 로그 철학 — "Logs are events, not strings"

Charity Majors의 한 줄이 wide-event observability를 정리한다.

> Logs should be wide events with high cardinality, not just strings. (휴리스틱 7)

전통 로그는 string이다. `"User 12345 logged in"`. 이 문자열을 parse하기 어렵고, 검색이 비효율적이다.

wide-event 로그는 structured object다.

```json
{
  "event": "user_login",
  "user_id": 12345,
  "device": "ios",
  "ip": "1.2.3.4",
  "auth_method": "password",
  "duration_ms": 230,
  "trace_id": "abc123",
  ...
}
```

cardinality (distinct value 수)가 매우 높은 필드를 자유롭게 박는다. 디버깅 시 "device=ios && duration_ms > 1000인 login 이벤트"를 즉시 query 가능. Honeycomb, Datadog가 이 모델로 인기.

### Cardinality 관리

metrics는 반대 방향이다. cardinality가 너무 높으면 storage·CPU가 폭증한다. label에 user_id를 넣으면 안 되는 이유다 — distinct user 수만큼 series가 만들어진다. Prometheus가 1억 series로 메모리 폭발하는 사고가 자주 일어난다.

원칙: **logs는 high cardinality OK, metrics는 low cardinality.**

### Sampling 전략

traces는 모두 저장하면 storage가 폭증한다. sampling이 필수.

- **Head sampling.** 요청 시작 시점에 10% 비율로 결정. 단순하지만 error trace가 sampling으로 빠질 수 있음.
- **Tail sampling.** 요청 끝난 후 결정. error나 slow trace는 100% 저장, 정상은 1%. 더 똑똑한 sampling이지만 buffer 필요.

production에서는 보통 tail sampling을 쓴다. error·outlier 위주로 저장.

## p99 latency — "Averages Lie, Percentiles Tell the Truth"

Gil Tene의 유명한 강연 "How NOT to Measure Latency"가 분산 시스템 measurement의 표준을 만들었다. 핵심은 한 줄.

> p99 latency가 진짜 latency다. average는 거짓말한다.

상황을 가정해 보자. 1만 요청 중 9900개가 10ms, 100개가 10초가 걸렸다.

- average = `(9900 × 10 + 100 × 10000) / 10000` = 109ms. "괜찮은 듯."
- p99 = 10초. "끔찍."
- p50 = 10ms. "정상."

이 1%의 끔찍한 응답이 시스템의 진짜 모습이다. average는 그걸 가려 버린다. p99·p95·p999가 진짜 보여 주는 그림이다.

### Coordinated Omission 함정

또 한 가지 함정이 **coordinated omission**이다. load test에서 자주 만난다.

```
부하 테스트:
  10000 req/s 보내기로 설정
  → server가 느려져 응답이 1초 지연됨
  → load gen이 send rate를 자동으로 낮춤 (req/s 유지하려)
  → 측정된 latency는 actual latency를 underreport
```

진짜 latency를 측정하려면 "client가 보내려고 했던 시점부터 응답 받은 시점까지"를 봐야 한다. send 후 응답까지가 아니다. HdrHistogram, k6 같은 도구가 이걸 잘 처리한다.

## 배포 전략 — Deploy ≠ Release

전통적으로 deploy = release였다. 새 코드를 production에 올리면 즉시 모든 사용자에게 노출. 끔찍한 일이 자주 일어났다.

현대 배포는 deploy와 release를 분리한다.

**1. Blue-Green.** 같은 capacity의 두 환경(blue=current, green=new) 동시 운영. load balancer를 green으로 전환. 문제 시 즉시 blue로 rollback.

**2. Canary.** 1% → 10% → 50% → 100% 점진적 트래픽 이동. 각 단계에서 SLO 측정. 문제 시 즉시 rollback.

**3. Feature Flag.** 코드는 모두 배포, **runtime에 일부 사용자에게만 노출**. LaunchDarkly·Unleash·Flagsmith가 표준 도구. "코드 deploy는 매일, feature release는 별도 일정"의 모델.

이 세 도구가 결합되면 **progressive delivery**가 만들어진다. 토스의 결제 시스템이 1% 단위 progressive rollout을 쓰는 이유가 이거다. 새 기능을 1%에만 노출, SLO·error rate 측정, 문제없으면 5%, 10%로 확장. 19장 결제 챕터에서 깊게 다룬다.

> 💡 휴리스틱 8 — **Deploy ≠ Release.** 코드를 production에 올리는 것과 사용자가 그 기능을 보는 것은 다른 일이다. feature flag로 이 둘을 분리하면 deploy 빈도를 무한히 늘릴 수 있다. Etsy·Stripe·Toss는 하루에 수십 번 deploy한다.

## Chaos Engineering — 평소에 일부러 깨자

Netflix가 2011년 Chaos Monkey를 도입했다. production VM을 무작위로 종료한다. 끔찍한 발상 같지만, 통찰은 명확하다.

> 장애를 평소에 일부러 일으켜 본 사람만이 진짜 장애를 견딘다.

Netflix Simian Army가 그 진화 — Latency Monkey (지연 주입), Conformity Monkey (잘못된 설정 식별), Chaos Gorilla (AZ 통째 종료), Chaos Kong (region 통째 종료).

핵심 원칙 4가지가 *Principles of Chaos Engineering*에 정리되어 있다.

1. **Hypothesis 정의.** "AZ 한 곳이 죽어도 5xx 응답이 1%를 안 넘는다."
2. **Real-world event 시뮬레이션.** 실제 일어날 수 있는 장애(network partition, host failure, latency spike).
3. **Production 환경에서.** staging이 아닌. 진짜 환경에서만 진짜 견디는지 안다.
4. **Blast radius 최소화.** 점진적, 일부 사용자만, 즉시 rollback 가능.

한국에서는 토스가 game day 문화를 가장 적극적으로 도입했다. 한 달에 한 번 의도적 장애 주입을 통해 on-call 대응 능력을 검증한다.

## Blameless Postmortem — 학습 조직의 기반

장애가 발생했다고 해보자. 회고에서 두 가지 답이 가능하다.

- **Blameful:** "왜 김OO이 그 deploy를 했지? 누구 책임이지?"
- **Blameless:** "왜 우리 시스템·프로세스가 그 deploy의 위험을 사전에 차단하지 못했지?"

Google SRE Book이 정립한 표준이 **blameless postmortem**이다. 사람이 아닌 시스템·프로세스를 비판한다. 그렇지 않으면 사람들이 사고를 숨기고, 학습이 일어나지 않고, 같은 사고가 반복된다.

표준 postmortem 양식:

1. **Summary.** 한 단락으로 무슨 일이 일어났는지.
2. **Impact.** 사용자·매출에 미친 영향, 시간.
3. **Root Cause.** 5 Whys로 근본 원인 추적.
4. **Detection.** 어떻게 발견했는가? 더 빨리 발견할 수 있었나?
5. **Response.** 어떻게 대응했는가? 잘된 점·아쉬운 점.
6. **Lessons Learned.** 시스템·프로세스 측면에서 무엇을 배웠나.
7. **Action Items.** 누가 언제까지 무엇을 한다. 추적 가능한 ticket.

가장 중요한 건 **action item 추적의 정직함**이다. postmortem만 쓰고 action item이 잊혀지면 의미가 없다. 한국에서는 카카오와 우아한형제들이 postmortem 공유 문화를 일부 외부에 공개하며 정착시켰다.

## On-call 휴머니즘 — alert는 사람을 깨운다

이 챕터의 도입에서 던진 질문으로 돌아오자. on-call burnout은 alert 설계의 실패다. 그 실패를 막는 5가지 원칙을 정리하자.

**1. Actionable alerts only.** 사람이 깨어나서 할 일이 없으면 page 보내지 마라. 자동 해결되는 일은 알람이 아닌 ticket으로.

**2. Burn rate으로 noise 줄이기.** SLO 임계만 보면 false positive가 많다. burn rate alerting으로 fast/slow 가르기.

**3. Runbook 필수.** 모든 alert에 "이 alert이 울리면 무엇을 봐야 하는지" 문서. runbook 없는 alert는 깨우지 마라.

**4. Escalation 정책.** primary on-call이 5분 안에 응답 안 하면 secondary. 한 사람이 항상 책임지지 않게.

**5. Pager fatigue 측정.** 한 명의 on-call이 한 달에 page를 몇 번 받는지 추적. 임계 (예: 5회/주) 넘으면 alert 정책 재점검.

토스 SLASH 22 "토스의 on-call 문화" 발표가 한국 백엔드에 강한 인상을 남겼다. 그 핵심은 **alert의 절반을 자동화**한 것이다. "사람이 안 깨어나도 되는 일"을 정확히 가르고, 그 부분을 자동 복구·자동 ticket으로 전환. 결과적으로 page 빈도가 절반 이하로 줄었다.

> 💡 한 줄 — **사람을 깨우는 모든 page는 그만한 가치가 있어야 한다.** 가치 없는 page를 줄이는 것이 on-call 문화의 기본기다.

## 시스템 한계 표현 도구 — 5가지 정리

이 챕터의 핵심 통찰을 5가지 도구로 압축하자.

| 도구 | 무엇을 표현 | 누구가 보는가 |
|------|----------|---------------|
| Rate limiting | 외부 → 우리의 한계 | 외부 client |
| Backpressure | 내부 producer → consumer 한계 | 내부 system |
| SLO + Error Budget | 우리가 약속하는 신뢰성 | 운영자·사용자·product |
| Observability (logs·metrics·traces) | 우리 시스템의 현재 상태 | 운영자·디버거 |
| 배포 전략 + Chaos | 변경의 위험·복구의 능력 | 운영자·product |

이 5가지가 한 layer로 깔린 시스템은 자기 자신을 안다. 한 가지라도 빠지면 시스템은 자기 한계를 모르고, 한계를 모르는 시스템은 새벽 alert로 우리를 깨운다.

## Callback 예고

14장의 도구들은 후속 챕터에서 그대로 반복 등장한다.

- **3부 케이스 16~20장.** 각 시스템(채팅·피드·검색·결제·이커머스)마다 "이 시스템의 운영 — SLO·alert·rollback" sidebar로 변주.
- **19장 결제·금융.** 토스 결제의 progressive rollout·canary·feature flag·on-call이 이 챕터의 도구를 정확히 활용.
- **부록 A 현장 노트.** on-call 휴머니즘이 한 번 더 깊게.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 시스템이 자기 자신을 보는 5가지 도구가 손에 잡혀 있다. Rate limiting 5 알고리즘, backpressure 패턴, SLI/SLO/Error Budget, three pillars + OpenTelemetry + wide-event observability + cardinality, p99 latency와 coordinated omission, blue-green/canary/feature flag, chaos engineering 4 원칙, blameless postmortem, on-call humanism 5원칙. 토스 on-call 자동화, 카카오·우아한형제들 postmortem 공유 문화까지가 한 묶음이다.

기억해두자. 분산 시스템을 만드는 것만큼 운영하는 일이 어렵다. 우리 시스템에 자기 한계를 표현하는 5가지 도구가 깔려 있고, 그 위에 blameless 문화가 있고, alert이 actionable하다면, 새벽 alert가 사람을 망가뜨리지 않는다. **사람을 깨우는 모든 page는 그만한 가치가 있어야 한다**는 원칙이 이 챕터의 한 줄 요약이다.

다음 장에서는 데이터 파이프라인과 협업 동기화를 살펴본다. Lambda·Kappa·Dataflow 아키텍처와 CRDT의 기초. 그 위에서 협업 도구(Figma·Linear)가 어떻게 multi-writer 일관성을 만드는지 함께 본다.
