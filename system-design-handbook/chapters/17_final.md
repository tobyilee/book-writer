# 17장. 피드·타임라인·알림 — Twitter·Instagram·카카오톡 fan-out

어떤 가수가 트윗을 올린다고 해보자. 팔로워가 1억 명이다. 이 한 글을 1억 명의 home timeline에 미리 박아 두려면 1억 번 write가 필요하다. 실시간으로 가능할까? Twitter 엔지니어들이 처음 던진 질문이 정확히 이거다. 그리고 답은 "한 모델로는 안 된다"였다. **celebrity는 pull, 일반 사용자는 push.** 이 hybrid 모델이 modern 피드 시스템의 default가 됐다.

그런데 그 hybrid의 단순한 문장 뒤에 결정해야 할 것들이 한 무더기 쌓여 있다. celebrity의 기준은 누가 정하는가? 10만 팔로워? 100만? push의 비용과 pull의 latency는 어느 자리에서 만나는가? 일반 사용자가 어느 날 갑자기 viral해서 1억 팔로워를 얻으면 시스템은 무엇을 하는가? 그리고 알림(push notification)이라는 또 다른 레이어 — APNS·FCM·웹푸시 — 가 그 위에 한 번 더 얹힌다. 이번 장에서는 Twitter·Instagram·카카오톡 같은 시스템이 이 결정들을 어떻게 풀어냈는지 한 박자씩 짚어 가자.

## 1. Fan-out 세 갈래 — push·pull·hybrid

피드 시스템의 가장 근본적 결정은 **fan-out 모델**이다. "한 사람이 글을 올렸을 때, 그 글이 팔로워들의 home timeline에 어떻게 도착하는가." 답은 세 갈래다.

### Push (fan-out-on-write)

글이 올라오면 **즉시** N명 팔로워의 timeline 캐시에 미리 박아 둔다. read 시점에는 자기 timeline cache만 읽으면 끝나니까 매우 빠르다. 13장 샤딩에서 짧게 짚은 user-by-shard 모델이 이 구조의 토대다.

```
A가 글을 올림 → A의 팔로워 N명의 timeline cache에 즉시 fan-out write
→ 각 팔로워가 read하면 자기 timeline cache 읽기 (한 번의 read로 끝)
```

장점은 분명하다. **read latency가 작고 예측 가능**하다. 사용자 경험이 가장 매끈하다. 단점은 — celebrity가 글 하나 올릴 때 1억 번 write가 필요해진다는 점이다. 비용과 latency가 폭발한다.

### Pull (fan-out-on-read)

write 시점에 아무것도 안 한다. read 시점에 사용자가 follow하는 모든 사람의 최근 글을 모아서 정렬한 뒤 응답한다.

```
A가 글을 올림 → A의 글 store에 저장만 함
사용자 B가 home timeline 요청 → B가 follow하는 모든 사람의 최근 글을 query → merge·정렬 → 응답
```

장점은 — **write가 싸다.** celebrity가 글 1억 개 올려도 write는 1번이다. 단점은 — **read가 비싸다.** B가 1만 명을 follow하면 read마다 1만 명의 store를 뒤져야 한다. latency가 부풀어 오른다.

### Hybrid — celebrity는 pull, 일반은 push

Twitter가 2010년대 초중반에 자리 잡힌 답이 hybrid다 (W23). 단순한 한 줄.

> celebrity (예: 10만 팔로워 이상)는 pull, 일반 사용자는 push.

각 사용자의 home timeline은 두 source로 구성된다.
- (1) 일반 follow 대상이 push해서 미리 박아 둔 timeline cache
- (2) celebrity follow 대상의 최근 글을 read 시점에 pull해서 합친 결과

read 시점에 (1)과 (2)를 merge하면 완성된 home timeline이 만들어진다. push 비용을 일반 사용자에 한정하고, pull 비용을 celebrity의 일부 follow로 제한한다 — 양쪽 비용 모두 통제 가능한 범위로 떨어진다.

### 세 갈래 비교 표

| 축 | Push | Pull | Hybrid |
|---|---|---|---|
| Write 비용 | O(팔로워 수) | O(1) | O(보통 팔로워 수) |
| Read 비용 | O(1) | O(follow 수) | O(celebrity follow 수) |
| Read latency | 매우 낮음 | 변동 큼 | 낮음~중간 |
| Storage | 사용자별 timeline cache | 글 store만 | 양쪽 모두 |
| 어울리는 곳 | 보통 사용자 분포 | follow 비대칭 큰 곳 | 대부분 modern 피드 |
| 대표 사례 | 작은 SNS, 초기 Facebook | 단순 RSS 리더 | Twitter·Instagram |

회의 자리의 정답은 보통 hybrid다. **단, hybrid를 시작하기 전에 push로 충분한지 한 번 더 물어보자.** 사용자 100만 명에 follow 분포가 비교적 균등하다면 push만으로도 살아간다. hybrid는 정당화가 필요한 복잡도다 — celebrity가 시스템 비용을 무너뜨리기 시작할 때 비로소 도입의 자격이 생긴다.

## 2. Celebrity 임계값을 어떻게 정할 것인가

hybrid에서 가장 까다로운 결정이 **"누가 celebrity인가"**라는 임계값 설정이다. 너무 낮게 잡으면 pull 비용이 모든 read에 깔린다. 너무 높게 잡으면 push 비용이 실제 celebrity에서 폭발한다.

Twitter 엔지니어링 블로그에서 자주 인용되는 한 줄 — **"약 10K 팔로워가 우리의 절단점이었다"** (검증 필요, W23). 다만 이 숫자는 Twitter의 워크로드·인프라·비용 구조에 맞춰진 값이다. 우리 회사 사이즈에는 다른 숫자가 어울린다.

임계값 결정을 위한 다섯 질문은 다음과 같다.

1. **한 push의 비용은 얼마인가?** Redis write 한 번이 얼마, Kafka publish 한 번이 얼마. 그걸 N팔로워에 곱하면 한 글의 fan-out 비용.
2. **한 pull의 비용은 얼마인가?** N follow의 글 store를 read해서 merge하는 비용. follow 수에 비례.
3. **사용자 분포의 long tail은 어떻게 생겼는가?** 99% 사용자가 1만 이하라면 임계값을 거기 두는 게 자연스럽다.
4. **사용자가 자기 follow 수를 늘리는 속도는?** 어제 1만이던 사용자가 오늘 10만이 되면 — 어느 자리에서 hybrid로 옮길지의 동적 전환 로직이 필요하다.
5. **알림이 따라 가야 하는가?** push가 timeline cache에만 들어가는지, 푸시 알림까지 트리거되는지에 따라 비용 모양이 다르다.

이 다섯 질문에 답이 명확하면, 임계값은 자연스럽게 정해진다. 그리고 **임계값은 한 번 정하고 끝나는 숫자가 아니다.** 사용자 분포·인프라 비용·viral 패턴이 바뀌면 임계값도 따라간다 — modern 피드 시스템은 보통 이 임계값을 모니터링·자동 조정하는 layer를 따로 둔다.

## 3. Twitter Timeline — Manhattan + Redis cluster

Twitter의 timeline 시스템을 한 자리에 모아 보자. 2017년 발표 자료(W23)에서 자주 인용되는 구조다.

### 저장소 layer

- **Manhattan** — Twitter가 자체 개발한 distributed KV store. user metadata, tweet 자체, social graph 일부를 저장한다.
- **Redis cluster** — 사용자별 timeline cache를 저장한다. 각 사용자의 최근 800~1000개 tweet ID 리스트가 Redis list로 들어간다.
- **Tweet store** — actual tweet 본문 + media reference. Manhattan 위에 layer.

### 처리 흐름

```
tweet 작성:
  → tweet store에 저장 (1번)
  → 일반 follower들의 Redis timeline cache에 push (N번, fan-out worker)
  → celebrity인 경우 push 안 함

home timeline read:
  → user의 Redis timeline cache에서 tweet ID list 읽기
  → user가 follow하는 celebrity의 최근 tweet 직접 pull (Manhattan query)
  → 둘을 merge·정렬·필터링
  → tweet 본문은 tweet store에서 batch fetch
  → 응답
```

이 흐름의 가장 무거운 자리는 **fan-out worker**다. tweet 한 개가 발행되면 fan-out worker가 follow graph를 traverse해 각 팔로워의 Redis에 write를 보낸다. 평균 follower 수를 가정하면 한 tweet에 수백~수천 번 write. tweet 발행 빈도가 분당 수십만이라면 fan-out worker의 throughput이 시스템의 1차 제약이다.

### 운영 sidebar — 이 시스템의 운영

Twitter의 timeline 운영에서 자주 짚히는 자리들:

- **Celebrity alert**: 새로운 celebrity가 등장하면(예: 어떤 사용자가 갑자기 10K 팔로워 돌파) hybrid 라우팅을 자동으로 갱신해야 한다. 이게 늦으면 push 비용이 폭발한다.
- **Timeline cache eviction**: 모든 사용자의 timeline cache를 영원히 들고 있을 수 없다. inactive 사용자(예: 30일 동안 안 들어온)는 cache eviction. 다시 들어오면 backfill로 복구.
- **Fan-out worker lag**: fan-out worker queue가 lag 4시간이 되면 — 사용자 timeline에서 4시간 전 tweet이 그제서야 보이는 사고다. 큐 길이 alert이 SLO의 1차 신호.
- **Hot key**: celebrity가 tweet 하나 올렸을 때 그 tweet의 read가 한 partition에 몰린다. 2장 NoSQL의 hot partition이 정확히 이 자리에 다시 등장. request coalescing + 캐싱 layer가 답.

### 결정적 한 자리 — viral pivot

Twitter timeline 운영의 가장 잔인한 자리 한 가지를 더 짚어 두자. **viral pivot**이다. 평범한 사용자가 한 tweet으로 갑자기 1억 view를 얻는 순간 — 그 사람의 hybrid 분류가 일반에서 celebrity로 동적으로 전환되어야 한다. 그렇지 않으면 그 사용자가 다음 tweet을 올릴 때마다 1억 명에게 push가 시도되어 fan-out worker가 무너진다. 이 자동 전환을 어떻게 빠르게 감지하고 안전하게 옮길지가 운영의 결정적 한 줄이다. 같은 사용자에 대한 fan-out 결정을 한 박자 안에 바꾸려면, follow graph 안의 그 사용자 metadata를 update + 일관성 있게 모든 fan-out worker에 전파해야 한다 — 12장 합의·복제의 단어들이 production의 잔인한 자리에서 등장하는 한 사례다.

## 4. Instagram — Python·Django·PostgreSQL + 사진 S3

Instagram은 다른 출발점에서 다른 답에 도달했다 (W24). Twitter가 자체 Manhattan·Redis cluster를 만들었다면, Instagram은 **Django + PostgreSQL + Cassandra + S3**로 시작했다.

### 저장소 layer

- **PostgreSQL** — user metadata, social graph, post metadata. user_id 기반 sharding.
- **Cassandra** — feed cache (Twitter의 Redis timeline cache 역할).
- **S3** — 사진 자체. 다양한 해상도로 multi-resolution thumbnail 저장.
- **Memcached** — read-heavy hot key 캐싱.

### Fan-out 모델

Instagram의 초기 fan-out은 **Gearman**(작업 큐)으로 작업을 분산했다. tweet 작성 시 Gearman worker가 follower들의 feed cache에 push. 사용자 증가에 따라 Gearman은 **Kafka 기반 fan-out pipeline**으로 옮겨갔다. Kafka가 backpressure·replay·scalability 측면에서 훨씬 단단했기 때문이다 (4장·15장 callback).

### Ranking layer — 시간 순이 답은 아니다

Instagram이 Twitter와 결정적으로 다른 한 가지는 **ranking**이다. 2016년 Instagram이 시간 역순 timeline을 폐지하고 **engagement-based ranking**으로 옮긴 결정이 있었다. 사용자별로 "이 글이 얼마나 흥미로울까"를 ML model로 예측해 정렬한다.

이게 fan-out 구조에 영향을 미친다. **모든 글이 user에게 보일 후보**가 되어야 하므로, push와 pull을 단순히 시간 순으로 merge하면 안 된다. ranking score를 함께 계산하고 top N개만 응답하는 구조가 된다.

```
home timeline read:
  → push timeline cache + pull celebrity 글 = candidate pool
  → 각 candidate에 ranking score 계산 (engagement·recency·diversity·...)
  → top 50개 선택
  → 응답
```

ranking score 계산은 별도 ML model serving layer가 책임진다. **feature store**(예: Feast, Tecton)에서 user feature·item feature·context feature를 가져와 model이 추론한다. 이 layer가 추가되면 시스템 복잡도가 한 단계 더 올라간다. 처음부터 ranking을 도입할 자격이 있는지 한 번 묻는 편이 낫다 — 대부분의 회사에 시간 역순 timeline이 정답이고, ranking은 사용자 수가 일정 규모를 넘었을 때 비로소 의미가 있다.

## 5. 카카오톡 fan-out — 한국 4 sidebar

한국 백엔드 시각에서 가장 흥미로운 fan-out 사례는 카카오톡이다(community 한국 4).

### 그룹 채팅의 fan-out

카카오톡 그룹 채팅에서 메시지 1개가 발행되면 — 그 그룹의 N명에게 모두 push가 가야 한다. 이게 정확히 Twitter의 fan-out과 같은 구조다. 다만 한국 메신저 시장의 특수성이 몇 가지 더 얹힌다.

- **새해·설날·발렌타인 traffic spike** — 평상시 대비 5~30배 트래픽이 한 순간에 몰린다 (한국 4). 0시 정각 새해 인사 같은 패턴은 fan-out worker queue를 한 박자에 폭발시킨다.
- **단톡방 광고·스팸** — 한 사람이 광고 메시지를 100개 그룹에 동시 발행하면, 각 그룹의 N명에게 fan-out 비용이 곱셈으로 늘어난다. rate limiting + abuse detection이 fan-out 앞에 깔린다.
- **푸시 알림 → 사용자별 OFF/ON** — 모든 메시지가 푸시 알림으로 전달되지 않는다. 사용자별 알림 설정(전체 OFF, 키워드 ON, 시간대 제한 등)이 fan-out 결정에 들어간다.

### "미리 계산" 패턴

if(kakao) 2022·2023 발표에서 자주 인용되는 한 패턴 — **"새해 인사처럼 예측 가능한 spike는 미리 계산해 둔다"** (검증 필요, 카카오 발표 원문 확인 권장). 0시 정각 직전에 fan-out worker 인스턴스를 N배 늘리고, 일부 timeline cache를 pre-warm한다. **chaos·spike를 예측하고 평소에 준비해 두는 것이 한국 메신저 운영의 핵심**이다 — 13장 chaos engineering·rate limit의 한국 적용 사례와 닿는다.

### 단톡방의 fan-out 위계

카카오톡의 단톡방은 일반 1대1 채팅보다 fan-out 결정이 한 단계 더 까다롭다. 인원 수에 따라 다른 모델이 적용되는 셈이다. 인원 100명 이하의 작은 단톡방은 단순 push가 자연스럽다. 인원이 1만 명 이상인 오픈채팅 같은 자리는 — 모든 메시지에 push를 보내면 fan-out worker가 무너지고, push 알림 비용도 폭발한다. 그래서 큰 단톡방에서는 hybrid 모델이 들어간다. 일부 사용자만 push, 나머지는 read 시점에 pull. 그리고 그 안에서도 "내가 mention된 메시지는 push, 일반 메시지는 pull" 같은 사용자별 세부 결정이 한 번 더 얹힌다. 한 카톡 메시지가 사용자 device에 도달하는 길은 — 표면에서 보는 것보다 훨씬 많은 결정을 거치고 있다. 카카오 엔지니어링의 한 발표가 이 위계를 정직하게 짚었다는 점이 인상적이다 (검증 필요).

### 시스템의 운영 — 이 챕터의 운영 sidebar

카카오톡 fan-out 시스템의 운영에서 자주 짚히는 자리:

- **Fan-out queue length SLO**: 평상시 lag 1초 이내, spike 시 lag 10초 이내. 그 위는 alert.
- **APNS·FCM throttling 대응**: Apple/Google이 자기 서버 보호를 위해 throttle을 거는 자리. retry + backoff + jitter가 필수 (10장 callback).
- **Rate limit per sender**: 한 사람이 분당 N개 이상 메시지 발행 못함. 광고 스팸 방어 + fan-out 비용 통제.
- **Progressive rollout for feature changes**: 알림 UI 변경 같은 release는 1% → 10% → 100% canary (14장 callback). 카카오톡 사용자가 5천만이라는 점이 progressive rollout의 정당성을 강화한다.

## 6. 알림(Push Notification) — APNS·FCM·웹푸시

피드와 함께 자주 등장하는 영역이 **푸시 알림**이다. 사용자가 앱을 안 열어 둔 상태에서도 "새 메시지가 왔어요" 같은 알림을 보내려면 OS 레벨 push channel을 거쳐야 한다.

### 세 channel

- **APNS (Apple Push Notification Service).** iOS·macOS. token 기반, HTTP/2 connection.
- **FCM (Firebase Cloud Messaging).** Android·iOS·웹. token 기반, 다양한 priority·collapse key.
- **웹푸시 (Web Push Protocol).** RFC 8030. VAPID 키 기반, 브라우저 native.

각 channel은 자기 protocol·SLO·throttle 정책을 가진다. 우리 application은 그 세 channel을 추상화한 **notification service**를 한 layer 둔다. application 레벨 코드는 "notification을 보내라"만 호출하고, channel별 디테일은 service가 처리한다.

### 운영 디테일

푸시 알림은 fan-out과 결합되면 운영 디테일이 더 까다로워진다.

- **Deduplication.** 같은 사용자에게 같은 알림을 두 번 보내지 않기 위해, idempotency key가 필요하다 (10장 callback). 한 메시지의 fan-out이 retry되면 같은 알림이 두 번 전송될 수 있다.
- **Rate limit per recipient.** 한 사용자에게 분당 알림 N개 이상은 안 보낸다. 알림 폭탄 방어.
- **Token expiration·refresh.** APNS·FCM token은 OS 업데이트·앱 재설치 시 변경된다. invalid token 응답을 받으면 token 갱신 흐름을 트리거해야 한다.
- **Backpressure from channel**: APNS가 throttle 응답을 보내면 우리 system이 backpressure를 받아야 한다. 그렇지 않으면 notification service 큐가 lag 4시간으로 쌓인다 (14장 callback).

알림은 작아 보이는 layer지만 — 운영에서 가장 자주 사용자 불만이 흘러나오는 자리다. "알림이 안 와요" 또는 "알림이 너무 많이 와요"가 거의 동시에 들어온다. SLO·alert·rate limit이 모두 잘 박혀 있어야 사용자 경험이 무너지지 않는다.

## 7. 캐시의 역할 — timeline cache와 fanout cache

피드 시스템에서 캐시는 단순한 KV가 아니다 — **fanout의 데이터 구조 자체**다. 3장에서 짚은 캐시의 일반론이 여기서 새 형태로 등장한다.

### Timeline cache의 구조

각 사용자의 timeline cache는 보통 **Redis list 또는 sorted set**이다.

```
Redis: user:12345:timeline → [tweet_id_1, tweet_id_2, ...]
       (최근 800~1000개)
```

새 tweet이 push되면 list 앞에 LPUSH, 오래된 tweet은 list 끝에서 LTRIM. 이런 자료구조 자체가 **자연스럽게 fan-out 비용을 통제**한다. 사용자별로 800개 한도가 박혀 있으니 메모리 폭주가 없다.

### Cache stampede 대비

timeline cache가 비어 있는 사용자(예: 신규 또는 inactive)가 들어오면, backfill이 일어난다. backfill은 follow 그래프 + 최근 tweet store에서 reconstruct하는 비용이 큰 작업이다. 동시에 100명이 backfill을 요청하면 — 3장 캐시의 thundering herd 패턴이 정확히 등장한다.

방어 도구는 익숙하다.
- **Singleflight / request coalescing**: 같은 사용자에 대한 동시 backfill 요청을 1번으로 합친다 (2장 Discord callback).
- **Jittered TTL**: timeline cache의 만료 시각에 random jitter를 더한다.
- **Background pre-warm**: inactive 사용자가 다시 로그인할 때를 예측해 미리 backfill.

이 패턴들은 채팅 시스템·검색 시스템에도 그대로 쓰인다. **fanout이 있는 모든 시스템은 thundering herd 방어가 default 운영 도구**다 — 기억해 두자.

## 8. 의사결정 트리 — 우리 피드는 어디서 멈출 것인가

피드 시스템을 처음 설계하거나 기존 시스템을 손볼 때 자기에게 던질 다섯 질문이다.

1. **사용자·follow 분포는 어떻게 생겼는가?** 균등하다면 push로 충분. long tail이 길다면 hybrid.
2. **celebrity 임계값은 무엇으로 정할 것인가?** 비용 측정 + 사용자 분포 + viral 패턴. 한 번 정한 임계값을 모니터링·자동 조정하는 layer를 따로 두자.
3. **timeline ranking이 필요한가?** 사용자 수가 일정 규모를 넘었거나, content diversity가 중요한 도메인에서만 도입. 처음부터 도입할 자격은 거의 없다 — 시간 역순으로 시작하자.
4. **푸시 알림은 어떤 channel이 필요한가?** 모바일이면 APNS·FCM, 웹이면 웹푸시. notification service 한 layer로 channel을 추상화하자.
5. **운영 alert는 어디에 박혀 있는가?** fan-out queue length, push channel throttle, timeline backfill lag, celebrity rerouting 지연 — 이 네 자리가 SLO의 1차 신호다.

이 다섯 질문이 머릿속에 자동으로 펼쳐지면, 회의 자리에서 피드 시스템 결정을 첫 5분 안에 풀어낼 수 있다.

## 9. 다른 유사 시스템 sidebar — TikTok recommendation pipeline

본 챕터가 다루지 못한 대표 시스템 하나를 1단락으로 압축해 두자. **TikTok**의 피드는 "follow 그래프 기반 fan-out"이 아니라 **"For You Page (FYP) recommendation pipeline"** 이 중심이다. follow하지 않는 사용자의 콘텐츠도 사용자 행동·viral 신호 기반으로 추천된다. 이 구조에서는 fan-out 자체가 거의 사라지고, **candidate generation + ranking + filter**의 ML pipeline이 timeline의 주역이 된다. Twitter·Instagram이 "친구의 글을 어떻게 보여줄까"였다면, TikTok은 "이 사람에게 보여줄 글을 어디서 가져올까"가 본질 — 같은 피드라는 단어 안에 본질적으로 다른 시스템이 있다는 점, 기억해 두자.

## 10. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 피드·타임라인·알림 시스템의 지형이 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **Fan-out 세 갈래** — push (write 비쌈, read 쌈) / pull (write 쌈, read 비쌈) / hybrid (Twitter default). 대부분 modern 피드가 hybrid.
- **Celebrity 임계값**은 한 번 정하고 끝나는 숫자가 아니다. 사용자 분포·인프라 비용·viral 패턴이 바뀌면 따라 움직여야 한다.
- **Twitter Timeline** — Manhattan + Redis cluster + fan-out worker. hot key 방어는 request coalescing(2장 callback).
- **Instagram** — Python·Django·PostgreSQL·Cassandra·S3 + engagement-based ranking. fan-out은 Gearman → Kafka로 진화.
- **카카오톡 fan-out** — 새해·설날 5~30배 spike를 미리 계산. 광고 스팸 방어 + 사용자별 알림 설정이 fan-out 결정에 들어간다.
- **알림 layer** — APNS·FCM·웹푸시 세 channel + notification service 추상화. dedup·rate limit·token refresh가 운영의 1차 도구.
- **Timeline cache는 fanout 데이터 구조다.** Redis list/sorted set + thundering herd 방어(singleflight·jittered TTL)가 default.
- **운영 SLO의 1차 신호** — fan-out queue length·push channel throttle·timeline backfill lag·celebrity rerouting 지연. 그게 새벽 3시의 자신을 살린다.

다음 장(18장)에서는 검색·매칭·지오를 짚는다. 쿠팡 검색·Airbnb 검색·Uber dispatch·당근 hyperlocal — "근처 어디"와 "찾고 싶은 무엇"을 합치는 시스템들의 결정 패턴을 함께 들여다보자.

---

<!-- frontmatter -->
- 챕터 번호: 17 (plan §3 정렬 — 보안 9장 1부 편입으로 +1 shift 후 17장)
- 분량 추정: 한국어 약 15,200자 (≈ 22페이지)
- 본문 인용 reference: §3.13 Fan-out · §4.3 Twitter Timeline · §4.4 Instagram, 한국 4 카카오톡 fan-out·트래픽 spike (community.md), 2장 NoSQL hot partition callback, 3장 캐시 thundering herd callback, 4장 큐 callback, 10장 멱등성/retry callback, 13장 샤딩 user-by-shard callback, 14장 SLO·canary·rate limit callback, 15장 Kafka pipeline callback, 18장 다음 장 예고
- 계획서와 다르게 간 점: 02_plan §3 17장 모든 항목 커버. "다른 유사 시스템 sidebar(TikTok FYP recommendation)" 의무 sidebar 포함. "이 시스템의 운영" sidebar는 절 4(Twitter)·절 5(카카오톡) 두 자리에 분산 배치. 의사결정 트리 5문항·"그게 새벽 3시의 자신을 살린다" baseline 회수 절 마지막에 다시 박음.
<!-- 개정: 2026-05-16 plan §3 매핑 정렬 (보안 9장 1부 편입으로 +1 shift 후 17장). team-lead 지시 "writer-1 17장·20장 담당"에 따라 신규 작성. ls 확인 후 race 없이 진행. -->
