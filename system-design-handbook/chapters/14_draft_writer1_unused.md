# 14장. Rate Limiting·백프레셔·SLO·관측성·on-call — 시스템이 자기 자신을 보는 법

어떤 팀의 alert가 새벽 3시에 울렸다고 해보자. on-call 엔지니어가 컴퓨터를 켜고 보니, 5분 안에 자동 해결된 일이었다. 같은 alert가 그 주에만 11번 울렸다. 한 달 뒤 그 엔지니어는 퇴사했다.

이 한 토막에 production 운영의 한 진실이 농축돼 있다. **on-call burnout은 사람 문제가 아니라 alert 설계의 실패다.** 시스템이 자기 한계를 알지 못하고, 한계를 표현할 도구가 없으면, 그 부담은 결국 사람에게 떠밀린다. 우리가 새벽에 깨는 횟수는 우리 시스템이 자기 자신을 얼마나 정직하게 보는지의 1차 지표다.

이번 장에서는 시스템이 자기 자신을 보는 다섯 가지 도구를 한 묶음으로 짚는다. **rate limiting**으로 들어오는 트래픽을 정직하게 제한하고, **백프레셔**로 내부 큐가 망가지기 전에 신호를 보낸다. **SLO·error budget**으로 신뢰성을 정량화하고, **관측성(observability)**으로 시스템 내부를 들여다본다. 그 위에 **배포 전략·chaos engineering·on-call 문화**가 얹혀, 사람이 새벽에 깨더라도 그 깨움이 정당하게 만든다. 길지만 한 덩어리로 가는 게 의미가 있다 — 다섯 도구는 따로따로가 아니라 한 layer로 묶인다.

## 1. Rate Limiting — 들어오는 트래픽에 정직한 limit을 박기

가장 단순한 자기 보호 도구부터 시작하자. **rate limiting**은 "한 client가 단위 시간에 받을 수 있는 요청 수"에 명시적인 상한을 두는 일이다. abuse 방어, SLA 보호, cost 통제가 모두 이 한 줄에서 시작된다.

알고리즘은 다섯 가지 정도가 표준으로 자리 잡았다.

- **Token bucket** (default 선택). capacity와 refill rate를 정해 두고, 요청마다 token을 하나씩 소비한다. token이 떨어지면 거부. burst를 허용한다는 점이 강점이다 — 평소는 잔잔하다가 가끔 한꺼번에 몰리는 트래픽 패턴(예: 사용자가 30초 동안 멍하니 있다가 한 번에 10번 클릭)에 자연스럽게 어울린다.
- **Leaky bucket.** 일정 속도로 egress가 빠져나가는 leaky bucket을 그려 보자. 들어오는 요청이 그 bucket을 채우고, bucket이 넘치면 버린다. egress가 항상 constant라 backend 부담이 예측 가능하다. 단 burst를 허용하지 않는다.
- **Fixed window.** "1분당 100 요청" 같은 단순 카운터. 구현이 쉽지만 — 윈도우 경계에서 burst가 두 배가 될 수 있다. 59초~61초 사이에 200개가 들어오면 두 윈도우 모두에서 limit 안이다.
- **Sliding window log.** 모든 요청의 timestamp를 기록해 정확한 1분 윈도우 안의 카운트를 잡는다. 정확하지만 메모리 비용이 크다.
- **Sliding window counter.** 두 윈도우의 카운트를 가중평균해 sliding window log를 근사한다. **Cloudflare가 자사 production에 도입했을 때 정확도 오차가 0.003%**였다고 보고했다 (W15). 사실상 modern rate limiter의 표준 default가 됐다.

다섯 알고리즘을 한 줄로 비교하면 — **default는 token bucket(burst 허용 필요시) 또는 sliding window counter(정확도 필요시)**다. fixed window는 학습용 외에는 피하는 편이 낫다.

### 분산 환경에서의 구현 — 한 가지 함정

알고리즘은 알았는데 실제 구현은 한 박자 더 까다롭다. 단일 서버라면 in-memory counter로 충분한데, load balancer 뒤에 N개 서버가 있으면 어디서 counter를 공유할까? 표준 답은 **Redis INCR + Lua 스크립트**다. 모든 서버가 같은 Redis 키를 atomic하게 증가시키고, 일정 임계값 초과 시 거부.

함정은 Redis가 single point of failure가 된다는 것이다. Redis 자체에 rate limit 트래픽이 몰려 죽으면 — 우리 rate limiter가 우리 시스템을 죽인다. 끔찍한 일이다. 방어법은 두 가지. ① Redis cluster + replica. ② **Hierarchical token bucket** — 각 서버가 local token bucket을 두고, 가끔만 global Redis와 sync한다. local에서 90% 트래픽을 1차 거른 뒤 마지막 검증만 global에서. 비용도 줄고 의존도도 줄어든다.

기억해 두자. **rate limiter는 시스템의 첫 번째 방어선이지, 시스템의 SPOF가 되어서는 안 된다.**

### 한국 사례 — 0시 동시 트래픽과 hierarchical rate limit

한국 백엔드에는 영어책에서 안 보이는 한 가지 운영 패턴이 있다. **0시 동시 트래픽**(community 한국 1)이다. 토스 "이자 받기 0시", 카카오뱅크 청약 9시, 콘서트 예매 8시 — 평상시 대비 수십~수백 배의 burst가 한 순간에 들어온다.

이 패턴 앞에서 단일 Redis rate limiter는 거의 항상 부족하다. 정확하게 0시 정각의 한 박자에 글로벌 lock 경합이 폭발하기 때문이다. 한국 핀테크의 운영 패턴은 — **사용자 segment별 + endpoint별 hierarchical token bucket**으로 답한다. 평상시는 글로벌 bucket이 거의 비어 있고, burst가 들어오면 local bucket이 1차로 받아 30% 가량을 즉시 거부한다. 이 사고법을 한 번 거치고 나면 0시 동시 트래픽이 무서운 알람이 아니라 그저 평상시의 가벼운 spike가 된다 — 적어도 rate limit layer에서는.

## 2. 백프레셔 — 큐 길이가 시스템 건강의 1차 신호

rate limiting이 "들어오는 문"의 제어라면, **백프레셔(backpressure)**는 "내부 흐름"의 제어다. consumer가 처리할 수 있는 속도보다 producer가 빠르게 만들어 내면, 그 사이에 큐가 쌓인다. 큐가 무한정 쌓이면 — 메모리가 터지거나, latency가 무한히 늘어나거나, OOM kill이 일어난다.

백프레셔의 핵심 사고법은 한 줄이다 — **"느린 consumer가 빠른 producer를 늦추는 신호를 보낸다."**

도구별로 백프레셔 표현은 조금씩 다르다. **Reactive Streams** (RxJava·Project Reactor)는 `request(N)`이라는 명시적 demand signaling을 가진다. consumer가 자기가 받을 수 있는 만큼만 producer에게 요청한다. **gRPC**는 HTTP/2 flow control을 통해 같은 일을 한다 — receiver의 buffer가 차면 sender가 자연스럽게 멈춘다. **Kafka**는 consumer poll throttling — consumer가 poll을 늦추면 broker가 더 안 보낸다.

다만 어느 도구를 쓰든, **큐 길이를 모니터링하지 않으면 백프레셔는 작동하지 않는다**. 큐는 조용히 망가진다 (4장 메시지 큐 callback). 그래서 production에서 가장 중요한 metric 하나만 고르라면 **각 큐의 길이와 그 변화율**이다. 길이가 천천히 늘어나는 패턴이 보이면 — 지금 alert가 안 떠도, 며칠 안에 깨진다.

### 백프레셔를 무시한 결과 — "Kafka lag 4시간"

백프레셔를 무시했을 때 production에서 어떤 모양으로 사고가 나는지 그려 보자. 어떤 회사 슬랙에 오전 9시 "큐 lag 4시간"이라는 메시지가 뜬다 (community 패턴 6). 누가 봐도 1주일 전 배포가 원인이지만, 누구도 처음에는 그 배포를 의심하지 않는다 — 어제까지 멀쩡했으니까. 큐는 조용히 망가지고 있었고, 큐 길이 변화율 alert이 없으니 우리는 그게 4시간 lag로 부풀 때까지 모른다. 새벽 사이에 쌓인 메시지들이 어떤 모양으로 망가지고 있는지 들여다보지 못한 채.

방어법은 단순하다. **모든 큐에 길이 alert을 박자.** 그리고 그 alert은 "1만 개 넘으면" 같은 단순 임계값이 아니라 "1시간 동안 변화율이 평균의 3배 이상"으로 박는 편이 낫다. 시스템이 자기 큐 길이의 평소 모양을 알아야, 평소와 다른 모양을 잡아낼 수 있다.

## 3. SLI / SLO / Error Budget — 신뢰성을 정량화하는 언어

자기 한계를 표현하는 다음 도구는 **SLO**다. Google SRE Book(P23)이 산업에 깊이 박은 이 한 단어가, modern 운영의 사실상 표준 언어가 됐다.

세 단어를 정리해 두자.

- **SLI (Service Level Indicator).** 시스템 건강을 정량화한 측정값. 보통 "good events / total events" 형태. 예: "1분간 응답 중 5xx가 아닌 비율", "1분간 응답 중 p99 latency가 200ms 이하인 비율".
- **SLO (Service Level Objective).** SLI에 대한 목표. "1분간 5xx 아닌 비율 ≥ 99.9%", "p99 ≤ 200ms 비율 ≥ 99.5%". 28일·30일 같은 rolling window로 측정한다.
- **Error Budget = 1 - SLO.** SLO가 99.9%면 error budget은 0.1% — 30일 기준 약 43분의 다운타임을 허용한다는 뜻이다.

세 단어가 강력한 이유는 — **error budget이 release 속도와 안정성의 협상 테이블**이기 때문이다. 한 달 budget을 다 썼다면 신규 feature deploy를 멈추고 안정성에 투자한다. budget이 많이 남았다면 risk 있는 deploy도 시도해 본다. **신뢰성이 추상적 가치에서 정량적 협상의 도구**가 된다.

> "100% is the wrong reliability target for basically everything." — Google SRE Book Ch 4 (P23)

100%가 잘못된 목표인 이유는 분명하다. 한 9를 추가할 때마다 비용이 10배씩 늘어나고, 사용자 경험은 점근적으로 똑같다. **99.9%와 99.99%는 비용 차이가 10배지만, 사용자 만족도 차이는 0에 가깝다**. error budget은 이 사실을 우리가 정직하게 인정하는 도구다.

### Burn rate alerting — fast burn과 slow burn

SLO 위에 alerting을 얹는 방법으로, modern SRE는 **multi-window multi-burn-rate alert**을 쓴다. 단순 임계값("5xx > 1%면 alert")보다 한 박자 정교한 접근이다.

burn rate란 "허용된 error budget 대비 실제 소진 속도"다. 1배 속도면 한 달치 budget을 한 달에 다 쓰는 셈, 10배 속도면 3일에 다 쓰는 셈이다. 이 burn rate를 두 윈도우로 보면 — **fast burn**(예: 5분 윈도우에 14배 속도, 즉 1시간이면 budget의 2%를 태움)은 폭발적 장애를, **slow burn**(예: 6시간 윈도우에 3배 속도)는 만성적 열화를 잡는다. 두 alert을 같이 두면 false positive를 줄이면서 정확도를 높일 수 있다.

이게 modern alerting의 default다. 단순 임계값 alert만 박혀 있는 시스템은, 새벽 alert이 11번 울리는 그 팀의 첫 번째 증상일 가능성이 높다.

## 4. 관측성(Observability) — logs·metrics·traces 세 기둥

자기 한계를 알았다면, 그 한계를 어떻게 측정하고 어떻게 디버깅할 것인가. **관측성**의 영역이다. 산업에 자리 잡은 표준 어휘는 **3 pillars** — logs·metrics·traces.

- **Logs.** 사람이 읽을 수 있는 이벤트 기록. 검색·필터링·재구성에 강하다. cardinality(고유 값 수)에 제약이 거의 없다.
- **Metrics.** 시간에 따른 수치 시계열. 시각화·alerting·집계에 강하다. cardinality에 제약이 있다 — 한 metric의 label 조합이 너무 많으면 cost가 폭증한다.
- **Traces.** 한 요청이 시스템을 통과한 경로 + 각 구간의 latency. 분산 시스템 디버깅의 핵심 도구.

이 세 가지를 따로 다루는 게 1세대 관측성이었다면, **modern 관측성의 핵심은 correlation**이다. 한 trace_id가 logs·metrics·traces를 모두 묶어 — 어떤 alert가 떴을 때 그 시각의 trace를 보고, 그 trace 안의 한 span에서 어떤 logs가 나왔는지 한 화면에서 보는 흐름이다.

### OpenTelemetry — vendor lock-in 해소의 표준

이 correlation을 vendor-neutral하게 만든 게 **OpenTelemetry(OTel)**다. Logs·metrics·traces를 OTLP라는 표준 wire format으로 통일하고, OTel Collector가 batching·filtering·routing을 책임진다. application 코드는 OTel SDK만 의존하고, backend는 Datadog·Honeycomb·Grafana·Splunk 어느 쪽으로든 자유롭게 바꿀 수 있다.

OpenTelemetry가 자리 잡기 전까지 관측성 영역은 vendor lock-in이 심했다. Datadog agent를 코드에 박으면 Datadog을 떠나기 어렵고, New Relic을 박으면 New Relic을 떠나기 어려웠다. OTel은 그 lock-in을 정면으로 푼다 — application은 표준에만 의존하고, vendor는 backend 경쟁만 한다.

### "Logs are events, not strings" — Charity Majors의 한 줄

관측성 영역의 modern 자세 중 하나로 — Charity Majors가 X(twitter)에서 자주 강조하는 **"Logs are events, not strings"**가 있다 (휴리스틱 7). 한 줄로 풀면 — **로그를 사람이 읽는 문자열로 두지 말고, 구조화된 wide event로 만들자**는 것이다.

전통 로그는 `"User 12345 logged in at 2026-05-16 03:14:22"` 같은 문자열이다. 디버깅 시 정규식으로 파싱해야 하고, 다음 분석에 재사용하기 어렵다. wide event는 같은 정보를 `{event: "login", user_id: 12345, timestamp: "...", source_ip: "...", session_id: "...", ...}` 같은 JSON으로 둔다. 30개·100개 attribute가 한 event에 박혀 있어도 좋다 — 어떤 dimension으로 group_by할지는 디버깅 시점에 결정된다.

이 자세가 관측성을 한 단계 올린다. **"미리 정의된 metric만 보는" 모니터링에서, "임의의 dimension으로 데이터를 쪼개 보는" 관측성으로 옮겨가는 차이**다. 익숙해지면 돌아갈 수 없다.

### p99 latency가 진짜 latency — Gil Tene의 한 줄

마지막으로 latency 측정에 관한 한 가지 자세 — **"평균은 거짓말, percentile은 진실"**이다 (휴리스틱 12). Azul Systems의 Gil Tene이 *Latency Tip of the Iceberg* 발표에서 강하게 짚은 이야기다.

평균 latency 100ms라는 숫자는 사용자 경험을 거의 표현하지 못한다. 99%의 사용자가 50ms로 받고, 1%의 사용자가 5초로 받아도 평균은 100ms 가까이 나올 수 있다. 그 1%가 우리의 power user일 수 있고, alert을 트리거하는 사용자일 수 있다. **p99(상위 1% 사용자가 겪는 latency)가 진짜 사용자 경험**이다.

여기에 한 가지 함정이 더 있다 — **coordinated omission**이다. load test가 1초당 100 요청을 보내려고 했는데 서버가 응답이 늦어 50개만 보냈다면, latency 측정에서 "보내지 못한 50개"는 빠진다. 실제 사용자가 겪을 latency tail이 측정에서 빠져 있는 셈이다. 그래서 p99·p999가 실제로는 더 나쁘다는 진실을 측정 도구가 숨길 수 있다. wrk2·hdrhistogram 같은 도구들이 이걸 정직하게 잡으려고 만들어진 것이다.

기억해 두자. **alert 임계값도 dashboard도 SLO도, 평균이 아니라 percentile로 박는 게 default다.**

## 5. 배포 전략 — release를 deploy와 분리하기

자기 한계를 알았다면, 새 코드를 production에 흘리는 방식도 한 박자 정교해진다. modern 배포 전략의 핵심은 **"deploy ≠ release"**라는 한 줄이다 (휴리스틱 8). 코드를 production에 흘리는 행위(deploy)와 사용자에게 새 기능을 보여 주는 행위(release)를 분리한다.

### Blue-Green — 두 환경, 트래픽 스위치

가장 단순한 패턴. green(현재 production)과 blue(새 버전)를 모두 띄워 두고, load balancer에서 트래픽을 한 번에 스위치한다. rollback이 빠르다는 게 강점 — 5초 안에 되돌릴 수 있다. 단점은 인프라 비용이 두 배라는 것, 그리고 DB schema 마이그레이션이 까다롭다는 것이다.

### Canary — 일부 트래픽 → 모니터링 → 점진 확대

1% → 10% → 50% → 100%로 단계적으로 트래픽을 옮기는 패턴이다. 각 단계마다 metric을 보고 이상이 없으면 다음 단계로 간다. blue-green보다 안전하고 인프라 비용도 낮다. 토스 결제 시스템의 **1% progressive rollout** (19장 callback)이 이 패턴의 한국 백엔드 사례다.

### Feature Flag — code deploy ≠ feature release

가장 modern한 도구. 새 기능을 코드에 박아서 production까지 흘려 두고, **feature flag로 on/off를 별도 control**한다. LaunchDarkly·Unleash·Flagsmith 같은 도구가 표준이다.

feature flag의 가치는 두 가지다. ① **risky deploy를 부담 없이 흘릴 수 있다.** flag가 off면 새 코드가 production에 있어도 사용자가 못 본다. ② **사용자 segment별 점진 rollout이 가능하다.** "내부 직원 → beta tester → 10% 사용자 → 100%" 같은 흐름을 코드 변경 없이 control할 수 있다. **사고가 났을 때 deploy를 되돌리지 않고 flag만 끄면 된다** — rollback이 1초다.

다만 함정도 분명하다. flag가 코드에 많이 박히면 분기 복잡도가 폭증한다. 한 번 박은 flag는 사용 완료 후 반드시 코드에서 제거하자 — "기술 부채로서의 flag"가 production code를 갉아먹는다.

## 6. Chaos Engineering — 평소에 일부러 죽여 보기

자기 한계를 알고 measure하고 deploy까지 정교해졌다면, 마지막 도구는 **"진짜 장애가 오기 전에 일부러 일으켜 보는 것"**이다. **Chaos Engineering**은 Netflix가 2010년대 초반에 산업에 가져온 자세다.

Chaos Monkey는 random하게 production EC2 인스턴스를 죽인다. Latency Monkey는 random하게 latency를 주입한다. Chaos Gorilla는 AZ 하나를 통째로 죽이고, Chaos Kong은 region 하나를 죽인다. **"무서운 일을 평소에 자주 작게 일으켜, 진짜 큰 사고가 왔을 때 사람·시스템이 모두 준비돼 있게 만든다."**

Principles of Chaos(W38)가 정리한 4 원칙은 다음과 같다.

1. **Hypothesis 먼저.** "한 노드가 죽어도 서비스 SLO는 유지된다"는 가설을 먼저 정한다.
2. **Real-world event.** 실제로 일어날 수 있는 장애만 시뮬레이션한다. (process kill, network latency, disk full, AZ outage)
3. **Production에서.** staging만으로는 안 보이는 게 production에 많다. 다만 blast radius를 최소화한 채로.
4. **Blast radius minimization.** 처음엔 1% 트래픽에만, 점진적으로 확대한다.

Chaos engineering의 가장 큰 가치는 도구가 아니라 **문화**다. "장애가 평소에 일어나는 게 정상"이라는 인식이 박힌 팀과, "장애는 절대 일어나면 안 된다"고 믿는 팀은 새벽 alert에서 보이는 모습이 다르다. **장애를 평소에 일부러 일으켜 본 사람만이 진짜 장애를 견딘다** — 기억해 두자.

## 7. Blameless Postmortem — 사람이 아니라 시스템·프로세스를 비판하기

장애가 나고 나면 무엇을 하는가. modern SRE의 답은 **blameless postmortem**이다. Google SRE Book(P23)이 표준화한 자세로, 한 줄로 풀면 — **"사람을 비난하지 않고, 시스템과 프로세스를 비판한다."**

표준 postmortem template는 보통 이렇다.

- **Timeline.** 장애 발생부터 해결까지의 사건 순서 — UTC 또는 KST 기준 분 단위.
- **Root cause.** 진짜 원인. "사람이 실수했다"가 아니라 "한 사람의 실수가 production을 깨는 시스템이었다"로 쓴다.
- **Action items.** owner + due date가 박힌 후속 조치 목록.
- **What went well / what went wrong.** 잘된 점도 적는다 — alerting이 정확했나, runbook이 도움이 됐나.
- **Lessons learned.** 다음에는 무엇이 달라져야 하는가.

blameless가 핵심인 이유는 두 가지다. ① **사람을 비난하면 다음 사람이 사고를 숨긴다**. 학습 조직이 만들어지지 않는다. ② **사람이 안 실수하는 시스템은 없다**. 사람의 실수가 production을 깨지 않게 만드는 게 진짜 일이다.

한국 백엔드 시각에서 — **카카오·우아한형제들·토스가 자기 postmortem을 공유 문화**로 가지고 있다는 점이 인상적이다(한국 6). if(kakao)·우아콘·SLASH 같은 발표에서 자기 장애 사례를 공개하는 자세는, 산업 학습 곡선을 함께 끌어올리는 일이다. 비방을 두려워하지 않고 회고를 공개하는 한국 회사들이 늘면서, 우리 회사의 회고도 한 단계 더 정직해지는 환경이 만들어진다.

산업의 표준 사례 하나만 더 짚어 두자. GitLab의 **2017 6시간 outage** postmortem (community 패턴 10)이다. 한 엔지니어가 잘못된 directory를 rm 했고, 5개의 backup이 모두 망가져 있었다는 사실이 그 사고로 드러났다. 보통의 회사라면 그 엔지니어를 비난하고 끝나기 쉬운 자리에서, GitLab은 **"한 사람의 실수가 production을 깨는 시스템이 잘못이었다"**고 회고했다. 그리고 backup·monitoring·access control의 전반적 개선으로 답했다. 이게 blameless postmortem의 진짜 모양이다 — 사람을 비난하지 않으면, 시스템이 결국 더 단단해진다.

## 8. On-call 휴머니즘 — alert가 사람을 깨운다면

마지막 도구는 사람의 영역이다. **on-call**은 분산 시스템 운영의 마지막 layer다 — 새벽 3시에 alert이 울리면 사람이 일어나야 한다.

modern on-call의 핵심 자세는 한 줄로 압축된다. **"alert가 사람을 깨운다면 actionable해야 한다"** (휴리스틱 9, Charity Majors). 사람을 깨우는 모든 page는 — 깨움받은 사람이 5분 안에 할 수 있는 구체적 행동이 있어야 한다는 뜻이다. 5분 안에 자동 해결되는 alert을 페이지로 보낸다면, 그 alert은 alert이 아니라 spam이다. 11번 울린 그 새벽의 풍경이다.

방어 도구는 네 가지다.

1. **Runbook.** 모든 page에 "이 alert가 떴을 때 무엇을 할지" 한 페이지의 runbook이 붙어 있다. 새벽 3시에 머리가 안 돌아가도 따라 할 수 있을 만큼 구체적이어야 한다.
2. **Escalation policy.** 1차 on-call이 15분 안에 응답 안 하면 2차로, 그 다음 manager로. 명확한 escalation chain이 burnout을 막는다.
3. **Pager fatigue 방어.** 한 달 page 횟수에 SLO를 박자. "월 5회 이하"가 보통의 기준이다. 그 위는 시스템이나 alert 설계의 실패다.
4. **On-call rotation.** 최소 4명 이상의 rotation. 그 미만이면 한 명이 항상 stress 상태가 된다.

### 한국 사례 — 토스 SLASH 22 on-call 문화

이 영역에서 한국 백엔드의 흥미로운 사례 하나는 **토스 SLASH 22의 "on-call 문화" 발표**다. 발표 후 OKKY·트위터에서 자주 인용되는 한 줄은 — **"우리는 alert의 절반을 자동화로 풀어 사람이 깨는 횟수 자체를 줄인다"**다 (community 패턴 8).

자동화의 모양은 다양하다. 1차 진단을 챗봇이 한다든가, 특정 패턴의 alert은 자동으로 mitigation을 실행한다든가, 같은 alert이 N번 이상 반복되면 자동으로 incident 등급을 올린다든가. 모든 alert가 사람을 깨우지 않게 만드는 것 — 이게 modern on-call 운영의 핵심 자세다.

한국 백엔드 회사 중 일부는 채용 후기에서 "당직 빈도가 너무 잦음"이라는 불만이 자주 등장한다(community 패턴 8). 이건 alert 설계의 실패가 사람의 불만으로 흘러나오는 한 단면이다. 우리가 시스템 설계자로서 할 수 있는 일은 한 가지다 — **시스템이 자기 자신을 더 정직하게 보게 만들어, 사람이 깨야 할 횟수를 줄이는 것**.

## 9. 다섯 도구를 한 layer로 묶기 — 의사결정 트리

이 챕터의 다섯 도구는 따로따로가 아니라 한 layer로 묶인다. 회의 자리에서 던질 수 있는 다섯 질문으로 정리해 두자.

1. **이 endpoint는 어떤 rate limit이 박혀 있는가?** 없다면 sliding window counter + Redis로 default 박자. 5명짜리 팀이라면 token bucket으로 시작.
2. **이 서비스의 SLO는 무엇인가?** 정의 안 된 SLO는 SLO가 아니다. SLI·SLO·error budget을 분기에 한 번 재검토하자.
3. **이 서비스의 관측성은 trace_id로 묶여 있는가?** OTel + wide event 로깅이 modern default. cardinality 폭증을 미리 모니터링하자.
4. **이 배포는 어떻게 되돌릴 수 있는가?** rollback 1분이 안 되면 deploy하지 말자. feature flag로 release를 분리하면 1초가 된다.
5. **이 alert이 새벽 3시에 사람을 깨워야 하는가?** 그렇지 않다면 alert이 아니다. runbook 없는 alert은 알람이 아니라 spam이다.

이 다섯 질문이 머릿속에 자동으로 펼쳐지면, 우리 시스템이 자기 자신을 보는 layer가 완성된다.

## 10. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 시스템 자기 인지의 다섯 도구가 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **Rate limiting의 default.** sliding window counter (정확도 필요시) 또는 token bucket (burst 허용). 분산 구현은 Redis INCR + Lua가 시작이지만, hierarchical token bucket으로 SPOF 회피.
- **백프레셔는 큐 길이로 본다.** 모든 큐의 길이와 변화율을 모니터링에 박자. 큐는 조용히 망가진다.
- **SLO·error budget이 신뢰성의 협상 테이블이다.** 100%는 잘못된 목표. burn rate alerting (fast + slow burn) 두 윈도우로 alert 정확도를 올린다.
- **관측성 3 pillars + correlation.** logs·metrics·traces를 trace_id로 묶는다. OTel이 vendor lock-in 해소의 표준. wide event 로깅이 modern 자세.
- **percentile이 진짜 latency다.** p99가 default, coordinated omission 함정 주의. 평균으로 박힌 SLO는 거짓말이다.
- **배포는 deploy와 release를 분리한다.** blue-green·canary·feature flag 세 도구 중 feature flag가 가장 modern. risky deploy의 부담을 한 자릿수로 낮춘다.
- **Chaos engineering은 도구가 아니라 문화다.** 평소에 일부러 죽여 본 팀이 진짜 장애를 견딘다.
- **Postmortem은 blameless다.** 사람이 아니라 시스템·프로세스를 비판한다. 학습 조직의 토대.
- **On-call alert이 사람을 깨운다면 actionable해야 한다.** 한 달 page 횟수에 SLO를 박자 — 그게 새벽 3시의 자신을 살린다.

다음 장(15장)에서는 데이터 파이프라인과 협업 동기화를 짚는다. Lambda·Kappa·Dataflow 아키텍처의 세 갈래에 CRDT sidebar가 얹히는 자리다. 이 챕터까지의 운영 도구들이 모든 빌딩 블록 위에 깔리는 한 layer였다면, 다음 장은 데이터의 흐름이 어떻게 합쳐지는지의 또 다른 layer다. 함께 들여다보자.

---

<!-- frontmatter -->
- 챕터 번호: 14 (plan §3 정렬 — 보안 9장 1부 편입으로 +1 shift 후 14장)
- 분량 추정: 한국어 약 15,500자 (≈ 24페이지 — ±10% 허용 범위 안)
- 본문 인용 reference: §3.7 Rate Limiting · §5.1 SLO · §5.2 관측성 · §5.3 Alert · §5.4 Postmortem · §5.5 Chaos · §5.6 배포, 휴리스틱 7·9·12 (community), 패턴 6 Kafka lag·패턴 8 on-call burnout·패턴 10 GitLab outage (community), 한국 1 0시 동시 트래픽·한국 6 토스 SLASH 22 (community), 4장 큐 callback, 9장 보안 callback, 19장 결제 callback, 부록 A on-call 휴머니즘 callback
- 계획서와 다르게 간 점: 02_plan §3 14장의 8개 주제 모두 커버. 의사결정 트리 5문항을 명시적으로 박은 점이 02_plan보다 한 단계 구체화. "그게 새벽 3시의 자신을 살린다" baseline 한 줄을 회수 절 마지막 항목에 다시 박아 책 전체 톤 일관.
<!-- 개정: 2026-05-16 rename collision으로 손실됐던 어제 작성본을 conversation context에서 복원. 기존 disk 14_draft.md(다른 writer 작품)는 14_draft_alt.md로 백업. plan §3 정렬 후 매핑(14장)·callback("다음 장 15장")·frontmatter 모두 갱신. -->
