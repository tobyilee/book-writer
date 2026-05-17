# 20장. 이커머스·재고·정합성 — Shopify·쿠팡·Amazon

쿠팡 로켓배송의 자정 cutoff는 절대 어길 수 없다고 해보자. 자정 1초 전에 들어온 주문은 오늘 새벽에 출발하는 트럭에 실려야 한다. 그 1초 사이에 재고 확인·결제 승인·배차 결정·창고 배정이 모두 정확하게 일관되어야 한다. 자정 0시 1초에 들어온 같은 주문은 — 같은 사용자가 같은 상품을 같은 가격에 클릭했어도 — 내일 새벽 트럭에 실린다. 단 2초 차이가 사용자 경험을 완전히 다른 모양으로 만든다.

이 1초의 결정이 이커머스 시스템의 정직한 단면이다. 속도(2초 안에 모든 결정)와 정합성(재고 1개의 마지막 한 명을 누구에게 줄 것인가)을 동시에 잡아야 한다. **속도는 단축할수록 정합성이 흔들리고, 정합성은 강할수록 속도가 무너진다.** 이 trade-off의 가장 잔인한 자리들이 한국 이커머스에 모여 있다 — 그 잔인함을 한 번 들여다보면, 1·2부에서 익힌 부품·패턴들이 한꺼번에 다시 등장하는 광경을 볼 수 있다.

여기서는 Shopify의 majestic monolith + pods 모델, 쿠팡 로켓배송의 자정 cutoff, Amazon의 Dynamo 원전 도메인을 짚으면서 — **reserve → confirm → settle** 3단계 일관성 패턴으로 이커머스의 정직한 결정 모양을 그려 보자. 19장 결제가 한 번도 두 번 결제되지 않는 자리였다면, 20장은 한 번도 두 번 팔리지 않는 자리다.

## 1. Shopify Pods — Majestic Monolith의 정직한 답

Ruby on Rails 진영에서 일했던 사람이라면 "majestic monolith"라는 단어를 들어본 적이 있을 것이다. Shopify가 자기 시스템을 부르는 이름이다(W27). 모든 마이크로서비스 트렌드와 반대 방향 — **하나의 거대한 Ruby on Rails monolith**가 Shopify의 핵심이다.

이 결정의 정직한 배경은 무엇일까? Shopify의 사용자는 거대 enterprise가 아니라 **수백만 개의 작은 쇼핑몰**이다. 각 shop이 자기 데이터·자기 트래픽 패턴을 가진다. 그리고 shop 단위로는 트래픽이 작다. 이 워크로드에 마이크로서비스를 깔면 — 서비스 간 통신 latency + 분산 트랜잭션 비용 + 운영 부담이 비즈니스 가치를 압도한다. monolith가 단순하고 빠르고 정확하다.

### Packwerk — Monolith 안의 module boundary

다만 monolith가 진짜로 한 덩어리라면 — 코드베이스가 무너진다. Shopify의 답은 **Packwerk**라는 자체 도구다. 같은 Ruby application 안에서 module boundary를 정의하고, "이 module은 저 module의 internal API에 접근할 수 없다"는 컴파일 타임 enforcement를 건다. **모듈러 모놀리스**가 그 이름이다.

이게 마이크로서비스와 무엇이 다른가? 핵심 차이는 — **마이크로서비스는 process boundary로 분리, 모듈러 모놀리스는 코드 boundary로만 분리**. 모듈러 모놀리스는 같은 process·같은 DB·같은 transaction을 공유한다. **분산 시스템의 비용 없이 코드 boundary의 가치를 얻는 길**이다. 5명짜리 팀이 Istio·Kafka·k8s 위에 mesh를 깔지 않고도 코드를 정리할 수 있다 — 0장의 도입 자격 5문항이 정확히 이 자리에서 작동한다.

### MySQL podding by shop_id

Shopify의 규모가 커지면서 — 한 monolith·한 DB로는 모든 shop을 담을 수 없다. 답은 **podding by shop_id**다. 13장 샤딩의 directory-based sharding 패턴 그대로다.

각 shop은 자기 pod에 묶인다. pod 하나에 수만 개 shop이 들어가고, pod마다 독립된 MySQL primary + replica + Redis + worker가 있다. shop A의 주문은 pod 1에서만 처리되고, shop B의 주문은 pod 2에서만. **shop 단위 데이터 격리 + pod 단위 인프라 분리**가 이 모델의 핵심이다.

장점이 분명하다. ① **pod 하나의 사고가 다른 pod에 안 전파된다.** 한 인기 shop의 트래픽 폭증이 다른 shop을 무너뜨리지 않는다. ② **pod 단위 deploy·rollback이 가능하다.** canary가 자연스럽다 (14장 callback). ③ **MySQL의 단일 leader 한계 안에서 글로벌 확장 가능**. 13장의 5가지 sharding 안티패턴을 피하면서 직관적 분할 기준(shop_id)을 택한 결과.

### BFCM 대응 — Load Shedding과 Queue Throttling

Shopify의 1년 중 가장 큰 사건은 **Black Friday Cyber Monday (BFCM)**다. 11월 마지막 주 + 12월 첫 주 — 평상시 대비 10~30배 트래픽이 한 번에 몰린다(검증 필요, Shopify Engineering 블로그 다년간 발표).

이 spike 앞에서 Shopify가 쓰는 도구 두 가지가 인상적이다.

**1. Load shedding.** 시스템이 한계에 가까워지면 **일부 요청을 의도적으로 거부**한다. 단순 rate limit이 아니라 — "지금 5xx 응답률이 임계 넘었다 → 가장 덜 critical한 요청부터 거부 시작" 같은 dynamic logic. 14장 SLO·burn rate 도구의 본격 적용이다.

**2. Queue-based throttling.** 결제 요청을 직접 받지 않고 **큐로 받는다**. 큐에서 일정 속도로 dequeue해 처리한다. 사용자는 "잠시만 기다려 주세요"라는 페이지를 본다. 끔찍해 보이지만 — 시스템이 무너지는 것보다 1분 기다리는 게 훨씬 낫다. 사용자도 그 사실을 안다.

이 두 도구가 BFCM 운영의 핵심이다. **시스템에 한계를 정직하게 표현하는 일이 사용자 신뢰의 토대다** — 14장의 SLO·rate limit 일반론이 BFCM이라는 도메인에서 정확히 적용되는 사례다.

## 2. 쿠팡 로켓배송 — 자정 cutoff와 한국 5

한국 백엔드 시각에서 가장 잔인한 이커머스 사례가 쿠팡 로켓배송이다(community 한국 5). Shopify가 "각 shop 단위로 격리"를 답했다면, 쿠팡은 정반대 — **전국 단일 시스템에서 자정 cutoff를 절대 어기지 않는 것**이 핵심이다.

### 자정 cutoff의 의미

쿠팡 로켓배송의 약속은 단순하다. "오늘 자정 전에 주문하면 내일 새벽에 받는다." 이 약속을 지키려면 — 자정 시점까지 **재고·결제·배차·창고 배정**이 모두 결정돼야 한다. 자정 0시 1초의 주문은 다음 날로 밀린다.

이 cutoff의 잔인함은 — **trade-off의 양 끝을 동시에 잡아야 한다**는 점이다.

- **속도** — 1초 안에 재고 확인 + 결제 승인 + 창고 배정 + 트럭 배차 결정.
- **정합성** — 재고 1개의 마지막 한 명을 누구에게 줄지 한 번도 두 번 팔리지 않도록.

이 두 가지가 정면충돌할 때 — 보통 시스템은 "지연되더라도 정확하게" 또는 "빠르게라도 가끔 어긋나게"를 고른다. 쿠팡은 둘 다 양보할 수 없는 입장이다.

### Reserve → Confirm → Settle 3단계 패턴

이 trade-off를 풀어내는 표준 패턴이 **reserve → confirm → settle** 3단계 일관성이다. 책 전체 부품·패턴이 한 자리에 모이는 도구다.

```
1. Reserve (수십 ms)
   - 재고 in-memory reservation
   - "이 사용자가 N초 동안 이 상품 1개를 잡아 둠"
   - 정합성: 같은 상품을 동시에 다른 사용자가 reserve 못함

2. Confirm (수백 ms)
   - 결제 승인 (19장 결제 시스템 호출)
   - 결제 성공 시 reservation을 confirm으로 전환
   - idempotency key 필수 (10장 callback)

3. Settle (분~시간)
   - 창고에 출고 지시
   - 배차 결정
   - eventual reconciliation으로 모든 layer에 전파
```

각 단계의 trade-off가 다르다.

- **Reserve 단계**는 strong consistency가 필요하다. 같은 상품 1개에 동시 reserve 두 번은 안 된다. **distributed lock (Redis Redlock with fencing) 또는 RDB row-level lock**이 답이다 (8장 분산 lock callback).
- **Confirm 단계**는 idempotency가 핵심. retry해도 결제는 한 번만, reservation 전환도 한 번만 (10장·19장 callback).
- **Settle 단계**는 eventual consistency 허용. 창고 시스템·배차 시스템·웹 UI가 결국 같은 상태에 도달하면 된다 (12장 일관성 회수).

이 3단계가 분명히 분리돼 있어야 — 자정 cutoff 안에 모든 결정이 끝난다. 단계 하나라도 섞이면 — 예컨대 confirm 단계에서 strong consistency를 강제하면 — 한 트랜잭션이 수초 걸리고 cutoff를 어긴다.

### 이 시스템의 운영 — 자정 cutoff 알림

쿠팡 로켓배송의 운영에서 가장 무거운 자리는 자정 자체의 트래픽이다. 22:00 ~ 24:00 사이에 트래픽이 평상시의 5~10배가 된다. 그리고 **자정 직전 1~5분**이 가장 잔인하다 — 사용자들이 "마지막 1분"을 노리고 클릭한다.

이 패턴에 대응하는 운영 도구들:

- **자정 cutoff burn rate alert** — error budget이 23시 50분 시점에 정상 비율을 넘으면 즉시 page. 자정 후 fix는 너무 늦다.
- **Pre-warm**: 22시쯤부터 reservation system·결제 시스템·창고 시스템의 instance를 N배 늘려 둔다. 17장 카카오톡 새해 인사 pre-warm 패턴과 같은 결.
- **Load shedding ladder**: 23:55 ~ 24:00 사이에 "재고 확인 요청만 받음, 결제 비핵심 endpoint는 거부" 같은 dynamic load shedding이 발동된다.
- **Postmortem 매주**: 매주 자정 시점의 SLO 위반·user impact·시스템 hot spot을 회고. blameless 문화로 사람을 비판하지 않고 시스템·프로세스를 점검 (14장 callback).

자정이라는 한 시점이 — 14장 운영 5도구(SLO·observability·배포·chaos·on-call)가 모두 모이는 운영의 가장 단단한 자리가 되는 셈이다.

## 3. Amazon — Dynamo 원전 도메인

이커머스 시스템의 또 다른 거대 사례는 Amazon이다. 그런데 Amazon은 다른 두 회사와 결을 달리한다. **Amazon의 핵심은 Dynamo가 태어난 그 자리**다 (2장 NoSQL callback).

2007년 SOSP에 발표된 Dynamo 논문(P7)이 풀려고 한 문제는 단순했다 — **"BlackFriday에 한 사용자의 장바구니에 물건을 담을 때, 절대로 'item could not be added'라는 에러가 보이면 안 된다."** Amazon은 매년 BFCM에 단 1초의 장바구니 다운타임도 허용하지 않으려 했고, 그래서 **eventual consistency + always-writable**라는 결정을 정면으로 골랐다.

그 결과가 — 같은 물건을 두 번 담을 수 있는 conflict가 가끔 발생한다는 점이다. Dynamo는 두 버전을 모두 저장하고, **장바구니 도메인의 의미로 conflict를 해소한다** — "두 버전을 union하면 된다, 사용자가 의도한 건 두 물건 모두 담는 것이다." application-level conflict resolution이 이 결정의 비결이다.

이 패턴이 modern 이커머스의 한 한 자리를 차지한다. **장바구니는 eventual consistency가 default**, 결제는 strong consistency, 재고는 reserve-confirm-settle 3단계. 모든 도메인에 같은 일관성을 강제하지 않는 게 운영 비용을 결정한다 — 12장 카카오뱅크 패턴 회수다.

### 사이드 박스 — 다른 유사 시스템 1단락: Stripe Sigma·Amazon Aurora

본 챕터가 다루지 못한 한 자리를 짚어 두자. **Amazon Aurora**(P14)는 Amazon이 자기 운영 부담을 풀려고 만든 modern RDBMS다. "log is the database"라는 한 줄로 1장 RDB 챕터에서 다뤘는데, 이커머스 시각에서는 — **상품·주문 데이터의 글로벌 region 확장**을 가능하게 한 도구다. Aurora Global Database가 cross-region replication을 자동으로 한다. 그리고 **Stripe Sigma**는 모든 거래 데이터를 SQL로 쿼리할 수 있게 하는 자체 서비스 — 19장 결제의 한 사례지만, 이커머스 회사가 결제 데이터를 직접 분석하는 시각으로 보면 한 단계 더 강력하다. 두 도구 모두 "이커머스의 거대 SQL 데이터를 어떻게 다루는가"라는 같은 문제의 다른 답들이다.

## 4. 재고 일관성 — Reserve의 잔인함

이커머스 시스템에서 가장 자주 데이는 자리가 **재고 일관성**이다. "재고 1개의 마지막 한 명을 누구에게 줄 것인가." 이 한 줄을 풀어내는 답은 도메인마다 다르다.

### Distributed Lock

가장 직설적인 답이다. 재고 차감 시 distributed lock을 잡는다.

```
1. Redis에 SETNX inventory_lock:sku_123 with TTL
2. 잠금 성공 → DB에서 inventory_count >= 1 확인 → 차감
3. lock 해제
```

문제는 8장에서 짚은 Redlock의 NTP 함정 + lock 자체의 SPOF다. **fencing token + ZooKeeper/etcd 기반 합의가 안전한 default**다 (12장 합의 callback). 단 모든 재고 차감에 합의 호출이 들어가면 — 자정 cutoff 안에 끝나기 어렵다. trade-off가 정직하게 트인다.

### In-Memory Reservation

대안 — 재고를 Redis 또는 application memory에 두고, atomic decrement를 쓴다.

```
1. Redis DECR inventory:sku_123
2. 결과 >= 0이면 reserve 성공, < 0이면 거부 (atomic)
3. 비동기로 DB에 reflect
```

이게 쿠팡·11번가 같은 대형 한국 이커머스가 자주 쓰는 패턴이다. 속도는 빠르지만 — **Redis 장애 시 재고 손실**이 핵심 함정이다. 1차 방어는 Redis cluster + persistence, 2차 방어는 DB 기반 reconciliation job(예: 5분마다 Redis·DB 일관성 점검).

### Eventual Reconciliation

가장 느슨한 답 — reserve 시점에 정확한 확인 없이 일단 받고, 사후에 reconciliation으로 정리. **재고가 충분한 경우 99%** 작동하지만, **재고 1개에 100명이 동시 클릭하는 1%의 자리**가 문제다. "주문은 받았는데 발송이 안 되네요" 같은 사용자 불만이 그 1%의 자리에서 흘러나온다.

세 답의 비교 표.

| 축 | Distributed Lock | In-memory Reservation | Eventual Reconciliation |
|---|---|---|---|
| 일관성 | 매우 강 | 강 | 약 |
| 속도 | 느림 | 매우 빠름 | 매우 빠름 |
| Redis 의존 | 부분 | 매우 큼 | 없음 |
| 어울리는 곳 | 한정판·금융 | 일반 대형 이커머스 | 재고 풍부 |

회의 자리의 정답은 보통 **In-memory Reservation + DB reconciliation hybrid**다. 정확한 합의가 필요한 critical 상품(한정판)만 distributed lock으로, 일반 상품은 in-memory로. 그리고 사후 reconciliation이 정기적으로 일관성을 보강한다. 이게 쿠팡·11번가의 평균 모델일 가능성이 높다 (검증 필요).

## 5. 카트·체크아웃의 멱등성

이커머스의 또 한 자리에 **카트·체크아웃의 멱등성**이 있다. 사용자가 "주문하기" 버튼을 두 번 클릭하면 — 한 번만 주문돼야 한다. 결제 retry도 마찬가지. 10장의 idempotency key 패턴이 정확히 이 자리에서 작동한다.

표준 흐름은 단순하다.

```
1. 카트 → "주문 시작" 버튼 클릭
   → server가 idempotency_key 생성 (UUID v7 권장, 8장 callback)
   → client에 전달
2. client → "결제 요청" with idempotency_key
   → server: 같은 key의 이전 요청 있으면 그 결과 반환, 없으면 새로 처리
3. 결제 완료 → order 생성 → reservation을 confirmed로 전환
```

이 흐름이 "user가 주문 버튼 두 번 클릭"·"네트워크 timeout 후 retry"·"브라우저 새로고침" 같은 모든 unhappy path를 같은 결과로 수렴시킨다. **idempotency key는 카트·체크아웃의 1번 줄**이다.

### 우아한형제들 배민 주문 처리 — 한국 6

한국 백엔드의 또 다른 흥미로운 이커머스 사례가 우아한형제들 배민이다(community 한국 6). 배민은 쿠팡·11번가와 다른 도메인 — **음식점에 주문을 전달하는 시스템**이라 정합성의 결이 다르다.

배민의 핵심 약속은 **"같은 주문이 음식점에 두 번 들어가지 않는다"**다. 이게 깨지면 음식점이 같은 음식을 두 번 만들어 환불 발생, 신뢰 무너짐. 우아한형제들 발표에서 자주 짚히는 패턴은 — **주문을 받는 layer + 음식점에 전달하는 layer의 명시적 분리**다. 사용자 클릭이 바로 음식점에 가는 게 아니라, 중간 reliable layer가 idempotency·retry·timeout을 책임진다. 11장 Saga + Transactional Outbox 패턴이 이 자리에서 정확히 작동한다.

그리고 또 한 가지 — **음식점 영업시간 cutoff**가 쿠팡 자정 cutoff와 비슷한 결의 운영 함정이다. 영업 종료 30분 전에 들어온 주문은 처리·취소·환불 흐름이 까다롭다. 14장의 SLO + alert이 배민에서는 영업시간 단위로 작동한다.

## 6. BFCM·자정 cutoff — Spike 대응의 한 묶음

Shopify의 BFCM과 쿠팡의 자정 cutoff는 — 시간축이 다르지만 본질은 같다. **예측 가능한 거대 spike에 어떻게 대응할 것인가**.

표준 도구 5가지를 정리해 두자.

1. **Pre-warm.** 예측 가능한 spike라면 사전에 instance를 N배 늘려 둔다. cold start 비용을 spike 시점에 부담하지 않는다.
2. **Load shedding ladder.** spike 시점에 점진적으로 덜 critical한 endpoint를 거부한다. 5xx보다 429가 사용자 신뢰에 덜 해롭다.
3. **Queue-based throttling.** 즉시 처리하지 않고 큐로 받는다. "1분 기다려 주세요"가 무너지는 것보다 낫다.
4. **Pre-computed timeline / inventory.** spike 직전에 hot path 데이터를 미리 캐시·warm. 17장 카카오톡 새해 인사 pre-warm 패턴.
5. **Chaos drill before spike.** spike 시점 1주 전에 평소에 일부러 fail-over·throttle을 일으켜 본다. 14장 chaos engineering의 BFCM 도메인 적용.

이 5가지가 머리에 자동으로 펼쳐지면 — 한국·미국·일본 어디서든 거대 spike 도메인 시스템 운영의 1차 도구를 손에 쥔 셈이다.

## 7. 의사결정 트리 — 우리 이커머스 시스템은 어디서 멈출 것인가

새 이커머스 시스템을 설계하거나 기존 시스템을 손볼 때 자기에게 던질 다섯 질문이다.

1. **monolith·모듈러·MSA 중 무엇인가?** 5명 팀이면 monolith로 시작. shop 수가 폭증하면 모듈러 monolith (Shopify Packwerk 패턴). 도메인이 진짜 분리되면 MSA. 13장 샤딩의 directory-based pattern (shop_id) 우선 검토.
2. **재고 일관성은 어느 수준인가?** 한정판·금융 → distributed lock + fencing. 일반 대형 이커머스 → in-memory reservation + DB reconciliation hybrid. 재고 풍부 → eventual reconciliation.
3. **카트·체크아웃 멱등성은 박혀 있는가?** idempotency_key는 시작점. 결제 retry·사용자 더블 클릭·브라우저 새로고침 모두 같은 결과로 수렴해야 한다 (10장·19장 callback).
4. **거대 spike(BFCM·자정 cutoff)에 대응하는 5가지 도구가 박혀 있는가?** pre-warm·load shedding·queue throttling·pre-computed·chaos drill 5가지. 한 가지라도 빠지면 spike 시점에 시스템이 무너진다.
5. **재고·주문·결제·창고 layer가 reserve → confirm → settle 3단계로 명시 분리돼 있는가?** 한 layer가 다른 layer의 일관성을 가정하면 — cascading failure의 시작점이 된다.

이 다섯 질문이 머릿속에 자동으로 펼쳐지면, 회의 자리에서 이커머스 시스템 결정을 첫 5분 안에 풀어낼 수 있다.

## 8. 책의 약속 회수 — 6가지 약속이 손에 잡혔는가

0장에서 우리는 6가지 약속을 박았다. 이커머스 챕터를 마치면서 — 그 약속들이 얼마나 손에 잡혔는지 한 번 되돌아보자.

1. **장애 회의에서 첫 5분 안에 어디서부터 의심할까.** 이커머스 도메인에서는 — 재고가 어긋나면 reserve layer를, 결제가 두 번 되면 idempotency key를, 자정 cutoff를 못 지키면 spike 대응 5도구를. 도메인 언어가 손에 잡혀 있어야 5분 안에 답이 나온다.
2. **부품 도입 trade-off 체크리스트.** 6개 부품 × 5문항 = 30문항이 의사결정 트리에서 일관되게 등장했다. RDB의 pod 분할(13장), in-memory reservation의 Redis 의존(3장), idempotency key의 멱등성(10장), 결제 vendor failover의 saga(11장).
3. **모든 network 호출에 멱등성·timeout·circuit breaker.** 카트·체크아웃·결제·창고·배차 모든 layer가 이 한 묶음 위에서 작동한다. "실패는 정상"이라는 인지가 이커머스의 1번 줄이다.
4. **외국·한국 사례 한국어 자막.** Shopify pods ↔ 쿠팡 pod 단위 격리, BFCM ↔ 자정 cutoff, Amazon Dynamo ↔ 한국 이커머스 in-memory reservation. 두 결정이 어떻게 닮고 어떻게 다른지가 보이는 게 5번째 자막이다.
5. **on-call alert의 메타 시선.** 자정 cutoff burn rate alert·spike pre-warm·load shedding ladder 모두 14장 운영 도구의 이커머스 도메인 적용. 알람을 줄이고 runbook을 만들고 postmortem을 blameless하게 쓰는 사람이 되는 길에 한 발 더 다가갔다.
6. **모든 endpoint에 인증·인가·secret·rotation·audit log.** 9장 보안의 control plane이 이커머스에서는 — 사용자 결제 정보·shop 결제 정보·창고 운영 API·배차 API 모두에 깔린다. 한국 망분리·전자금융감독규정과 닿는다.

여섯 약속이 다 풀어졌으면 — 이 책의 한 번 통독이 끝난 셈이다. 다 안 풀어졌어도 괜찮다. 책장에 두고 다음에 필요할 때 한 챕터씩 다시 펴 보면 된다. 동료의 어깨를 두드리며 "한 번 같이 들여다보자"는 톤은 그대로 우리 옆에 있다.

## 9. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 이커머스·재고·정합성의 지형이 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **Shopify Pods + Majestic Monolith.** 모듈러 monolith로 분산 시스템 비용 없이 코드 boundary의 가치. 13장 directory-based sharding의 한 사례.
- **BFCM 대응 5도구** — pre-warm·load shedding·queue throttling·pre-computed·chaos drill. 거대 spike 운영의 표준.
- **쿠팡 자정 cutoff** — 속도와 정합성 양 끝을 동시에 잡는 자리. reserve → confirm → settle 3단계 분리가 답.
- **Amazon Dynamo 원전 도메인** — 장바구니 always-writable + application-level conflict resolution. 모든 도메인에 같은 일관성을 강제하지 않는 게 운영 비용을 결정한다 (12장 카카오뱅크 회수).
- **재고 일관성 3답** — distributed lock·in-memory reservation·eventual reconciliation. 일반 대형 이커머스의 default는 hybrid.
- **카트·체크아웃 멱등성** — idempotency_key가 1번 줄. 10장의 패턴이 이커머스에서 가장 직접적으로 작동.
- **우아한형제들 배민** — 음식점 영업시간 cutoff + 주문 layer 분리 + 11장 Saga·Outbox 패턴.
- **이커머스의 한 줄 통찰** — 한 번도 두 번 팔리지 않게, 그리고 자정 cutoff를 어기지 않게. 그게 새벽 3시의 자신을 살린다.

여기까지가 3부 케이스 스터디의 마지막 챕터다. 0장에서 약속했던 책 전체의 그림 — 빌딩 블록 → 패턴 → 케이스 → 운영의 4축 지형도 — 가 손에 잡혔길 바란다. **production은 결국 사람의 영역이다**. 부록 A에서는 그 사람의 영역을 정직하게 들여다본다. 책으로는 안 배우는, 코드로만 만나는 18가지 함정. 동료적 마무리로 책을 닫는 자리다.

---

<!-- frontmatter -->
- 챕터 번호: 20 (plan §3 정렬 — 보안 9장 1부 편입으로 +1 shift 후 20장, 보안이 1부에 들어가도 3부 케이스 마지막은 그대로 20장)
- 분량 추정: 한국어 약 14,000자 (≈ 20페이지)
- 본문 인용 reference: §4.7 Shopify Pods (W27), §C5 이커머스, 한국 5 쿠팡 자정 cutoff (community), 한국 6 우아한형제들 배민 (community), 2장 NoSQL Dynamo·application-level conflict callback, 8장 분산 lock callback, 9장 보안 control plane callback, 10장 idempotency callback, 11장 Saga·Outbox callback, 12장 일관성·카카오뱅크 callback, 13장 directory-based sharding callback, 14장 SLO·chaos·rate limit callback, 17장 spike pre-warm callback, 19장 결제 클라이맥스 callback, 부록 A on-call 휴머니즘 callback
- 계획서와 다르게 간 점: 02_plan §3 20장 모든 항목 커버. 케이스 챕터 의무 sidebar 2개 충족 — (1) "이 시스템의 운영 — 자정 cutoff 알림"(쿠팡 절), (2) "다른 유사 시스템 1단락"(Aurora·Stripe Sigma sidebar). 책 전체 6가지 약속 회수를 절 8에 박아 0장 약속의 최종 회수 페이지로 작용. "그게 새벽 3시의 자신을 살린다" baseline 회수 절 마지막 항목에 다시 박음.
<!-- 개정: 2026-05-16 plan §3 매핑 정렬 + team-lead 지시 "writer-1 17장·20장 담당"에 따라 신규 작성. ls 확인 + TaskUpdate + TaskGet 재확인 패턴 적용해 race 없이 진행. -->
