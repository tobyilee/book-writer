# 18장. 검색·매칭·지오 — 쿠팡·Airbnb·Uber·당근

당근에 글을 올리면 우리 동네에서만 보이고 옆 동네에서는 안 보인다. 이 단순한 사실이 처음에는 당연해 보인다. 그런데 한 번 멈춰서 생각해보자. 사용자가 "사당동"에 살고, 검색은 "30분 안에 만날 수 있는 거리"여야 하고, 글은 "동네 단위"로만 보여야 한다. 그리고 이 모든 결정이 동시에 빠르게 — 보통 50ms 안에 — 일어나야 한다. 한국이라는 도메인이 시스템 설계 결정에 미친 영향이 가장 노골적으로 드러나는 사례다.

검색·매칭·지오라는 세 도메인을 한 챕터에 묶은 이유가 있다. 셋이 같은 골격 위에 서 있다. **"index에서 후보를 좁히고, scoring으로 순위를 매기고, dispatch로 사용자에게 흘려보낸다."** 어떤 도메인이든 이 세 단계의 합이다. 쿠팡 검색이 이걸 한 가지 방식으로, Airbnb 검색이 다른 방식으로, Uber dispatch가 또 다른 방식으로 푼다. 같은 골격, 다른 압력이다.

"근처 어디"와 "찾고 싶은 무엇"을 합치는 시스템은 어떻게 만들어지는가 — 이 질문에 답할 수 있어야 검색·매칭·지오를 안다고 말할 수 있다. 그리고 한국 hyperlocal이 미국 글로벌 매칭과 어떻게 다른 게임인지를 정확히 셈할 수 있어야 한다.

## 검색·매칭·지오의 공통 골격 — index + scoring + ranking + dispatch

먼저 셋의 공통 구조를 한 페이지에 압축해보자. 어떤 검색·매칭·지오 시스템을 떼어 보더라도 다음 4단계로 분해된다.

1. **Index 구축**: 검색 가능한 모든 entity(상품·숙소·드라이버·매물)를 어떤 기준으로 색인한다. inverted index, vector embedding, H3 hexagonal grid가 모두 index의 한 형태다.
2. **Candidate retrieval**: 사용자 query에 대해 후보를 N개 추린다. 보통 1만~10만 → 200개 수준의 1차 필터링. 5장에서 본 ES inverted index, Airbnb의 IVF ANN, Uber의 H3 k-ring이 모두 이 단계다.
3. **Scoring + ranking**: 후보를 정밀하게 점수 매긴다. ML 모델, business rule, 가격·평점·거리의 weighted sum이 여기서 동작한다. 후보 200개 → 정렬된 20개.
4. **Dispatch**: 결과를 사용자에게 흘려보낸다. 검색은 list 응답으로, 매칭은 driver assignment로, 지오는 인접 cell의 entity 노출로. 응답 latency는 보통 p99 100~500ms.

이 4단계가 검색·매칭·지오의 본체다. 도메인이 달라져도 이 골격은 거의 안 바뀐다. 다른 것은 1단계 index가 무엇으로 구성되는가, 그리고 4단계 dispatch에서 무엇이 사용자 체감의 1번 신호인가다.

이 골격을 머리에 박아두고 네 시스템을 차례로 살펴보자. 같은 골격, 다른 압력의 그림을 본다.

## 쿠팡 검색 — 한국어 형태소와 indexing pipeline의 silent killer

쿠팡 검색은 한국 e-commerce 검색의 베이스라인이다. 쿠팡 엔지니어링 블로그가 정리한 시스템 구조를 한 단락으로 줄이면 다음과 같다(W32).

> Elasticsearch + Kafka indexing pipeline. 상품 update event는 Kafka로 흘러 들어가고, indexer가 ES shard에 반영한다. 검색 query는 ES에 직접 들어가지 않고 search service가 한 layer 더 위에서 처리한다. (쿠팡 엔지니어링)

별로 새로운 그림이 아니다. ES + Kafka 조합은 5장에서 본 표준 indexing 패턴이다. 그런데 쿠팡이 이 시스템에서 가장 자주 부딪힌 함정 두 가지가 인상적이다.

**첫 번째, 한국어 형태소 분석.** 영어 분석기로 한국어 검색을 그대로 돌리면 "쿠팡 배송"으로 검색했을 때 "쿠팡배송"이 안 나온다. 한국어는 띄어쓰기와 조사가 검색을 어렵게 만든다. 5장에서 본 mecab-ko, NORI, KOMORAN, Khaiii, KIWI 같은 한국어 형태소 분석기 중 하나를 골라 색인 단계에 박아야 한다. 분석기 선택이 검색 품질의 30%를 결정한다(한국 3).

쿠팡은 NORI를 기반으로 자체 dictionary를 쌓아 올리는 길을 갔다고 알려져 있다(검증 필요). "로켓배송"·"새벽배송"처럼 쿠팡 도메인 고유 용어를 dictionary에 박지 않으면, 사용자가 "로켓"으로 검색했을 때 "로켓배송" 상품이 안 나오는 끔찍한 일이 생긴다.

**두 번째, indexing pipeline의 silent killer.** 1장 sidebar에서 한국 백엔드의 silent killer로 JPA N+1을 봤다. 5장에서는 검색 인덱싱 파이프라인의 silent killer가 따로 있다. 가장 흔한 시나리오를 떠올려보자.

- 상품 가격이 update된다 → Kafka에 event 발행
- indexer가 event를 consume → ES bulk update
- 사용자 검색 query는 cache hit 상태 → 30초간 stale 가격 노출
- 그 30초 사이에 누군가 cache 만료된 가격으로 결제 시도 → 가격이 안 맞아 실패

이 silent killer는 production에서는 들키지 않는다. 사용자가 한 명씩 결제 실패하는데, "왜 안 되지?" 새로고침하면 그새 cache가 갱신돼 잘 된다. 일주일에 한 번씩 OKKY에 "쿠팡에서 결제할 때 가격이 바뀌었다는 알림 뜨는데 뭐죠?" 같은 글이 올라온다. 이게 indexing pipeline의 staleness가 사용자에게 새는 자리다.

쿠팡이 어떻게 대응했는지는 명확히 공개되지 않았지만(검증 필요), 일반적인 대응은 다음 세 가지의 조합이다.

1. **가격 같은 hot data는 short TTL (10초 이하).**
2. **search service가 ES 결과를 받은 직후 가격을 primary DB에서 한 번 더 verify.** latency 비용은 늘지만 staleness가 잡힌다.
3. **결제 단계에서 다시 한 번 가격을 verify.** 사용자가 결제 버튼을 누른 순간이 진실의 기준점.

이게 검색이 1·2부의 캐시·NoSQL·Kafka·결제 모두와 어떻게 묶이는지의 한 사례다. 검색은 검색 단독으로 안 끝난다. 데이터 파이프라인 전체의 정합성이 사용자 마지막 클릭까지 이어진다.

## Airbnb 검색 — IVF ANN을 HNSW 대신 고른 이유

검색 도메인을 더 깊게 보려면 vector search의 결정 한 자리를 짚고 가야 한다. Airbnb는 embedding-based retrieval 시스템에서 한 가지 인상적인 결정을 했다(W28, 자료 4.8).

> IVF(Inverted File Index) ANN을 HNSW 대비 채택. 이유: high real-time update rate — 가격과 가용성이 빈번히 변경되기 때문. (Airbnb Tech)

vector search 알고리즘 두 가지를 빠르게 비교해보자.

| 항목 | HNSW (Hierarchical Navigable Small World) | IVF (Inverted File Index) |
|------|--------------------------------------------|----------------------------|
| **search latency** | 빠름 (수십μs~수ms) | 약간 느림 (수~수십ms) |
| **build cost** | 높음 (graph 구축) | 중간 (centroid clustering) |
| **incremental update** | 어려움 — graph 재구축 필요 | 쉬움 — 단순 inverted list 추가 |
| **recall (정확도)** | 매우 높음 | 비슷하지만 약간 낮음 |
| **권장 케이스** | static catalog, 정밀 검색 | high real-time update |

Airbnb의 도메인을 떠올려보자. 숙소 가격은 시즌·요일·이벤트마다 바뀐다. 가용성(available/unavailable)은 예약 한 건만 들어와도 즉시 바뀐다. 이런 도메인에서 HNSW를 쓰면 graph 재구축 비용이 비명을 지른다. 그래서 약간의 latency를 양보하고 incremental update가 쉬운 IVF를 택했다.

이 결정에 한 가지 교훈이 있다. **"가장 빠른 알고리즘이 가장 좋은 알고리즘이 아니다."** 도메인의 update 패턴이 알고리즘 선택의 1번 변수다. Discord가 ScyllaDB를 고른 결정(16장)도 같은 결이다. 자기 도메인의 가장 큰 적이 무엇인지를 정직하게 정의했기 때문에 비싼 결정을 할 수 있었다.

그리고 Airbnb 글에서 한 가지 더 인상적인 부분이 있다. 시스템 운영 standards다.

> SOA service platform standards로 모든 신규 service에 outlier detection과 circuit breaker를 강제. (Airbnb Tech, W28)

10장에서 본 회복력 패턴(circuit breaker)을 organization-wide standard로 강제했다. 한 service가 느려지면 다른 service가 그걸 자동으로 차단한다. mesh를 깐 게 아니라, 모든 service의 코드 standard로 circuit breaker가 들어 있다. 잊지 말자. 회복력은 mesh의 기능이기 전에 조직 standard의 결정이다.

## Uber Dispatch — H3 hexagonal grid가 풀어준 매칭의 본질

매칭 도메인의 가장 유명한 케이스가 Uber Dispatch다(W26, 자료 4.6). 핵심 결정 한 자리가 모든 것을 단단하게 만든다.

> 지구를 icosahedron(20면체)으로 분할한 다음, hexagon 계층 grid로 나눈다 — 0~15 resolution. H3라고 부른다. (Uber Engineering)

왜 hexagon인가? square grid나 geohash와 비교해보면 답이 나온다.

| 격자 방식 | 이웃 cell 수 | 이웃 거리 균등성 | 계층 구조 | 한국 활용 |
|------------|---------------|--------------------|-------------|-------------|
| **Geohash** | 8개 (모서리 vs 변) | 비균등 — 모서리가 멀다 | base32 prefix 자연 계층 | 흔함 |
| **S2 (Google)** | 8개 | 비균등 | Hilbert curve 기반 | Google 계열 |
| **H3 (Uber)** | 6개 (모두 변) | **균등** | parent-child 계층 | Uber·당근(추정) |

hexagon은 이웃이 6개고, 모든 이웃과의 거리가 같다. 매칭처럼 "가장 가까운 후보 N개"를 찾는 도메인에서는 이 균등성이 결정적이다. square grid에서는 같은 cell 두 칸 옆이 대각선 이웃보다 더 가깝다는 어이없는 일이 생긴다. H3에서는 그런 모순이 없다.

H3 위에 Uber가 얹은 dispatch optimizer가 DISCO다. 한 줄로 줄이면 이렇다.

> 매칭은 단순 "가장 가까운 driver"가 아니다. wait time, repositioning cost, ML acceptance probability, driver preference의 multi-objective optimization. (Uber Engineering, W26)

"가장 가까운 driver를 보낸다"는 직관은 틀렸다. 가까운 driver가 거절할 수도 있고, 그 driver를 보내면 다른 zone에 공급이 부족해질 수도 있다. ML 모델이 "이 driver가 이 ride를 받을 확률은 70%"라고 예측하면, 그 70%와 거리·repositioning cost를 같이 셈해서 최종 후보를 고른다. 이게 multi-objective optimization의 실전 사례다.

한국으로 옮겨와 보자. **배민 라이더 dispatch도 같은 골격을 쓰지만, 압력이 다르다.** 배민은 한 점심 시간에 한 라이더가 여러 주문을 묶음 배달한다. 1대1 매칭이 아니라 1대N batching이다. multi-objective에 batching constraint가 더 들어간다. 도메인이 미세하게 다르면 같은 H3 + optimizer 위에서도 결정의 변수가 한 차원 더 생긴다.

이게 매칭 시스템이 한국 도메인에서 어떻게 변주되는지의 한 사례다. 라이브러리는 글로벌이지만, 도메인 압력은 항상 로컬이다.

## 당근 hyperlocal — 동(neighborhood) 단위 partition

이제 당근으로 와 보자. 한국 hyperlocal이 시스템 설계에 미친 영향이 가장 노골적인 사례다(W31, 한국 7, 자료 4.11).

당근의 sharding key는 **동(neighborhood)**이다. 사용자가 사는 동을 partition key로 박는다. 같은 동의 사용자만 같은 상품을 본다. 옆 동은 partition이 다르다.

이 결정이 무엇을 풀어주는가? 세 가지를 한꺼번에 푼다.

1. **검색 query 좁히기**: "사당동"이라는 partition 안에서만 search한다. ES shard가 자연스럽게 동 단위로 갈린다. cross-shard query가 거의 없으니 latency가 안정적이다.
2. **dispatch 규칙 단순화**: 옆 동 글은 옆 동 사용자에게만. 1대N fan-out의 범위가 동의 크기로 제한된다 — group push 비용이 카카오톡 같은 거대 fan-out과는 다른 게임이다(16장 sidebar callback).
3. **거래 라이프사이클 명확**: 거래는 같은 동에서, 거래 완료 후 chat이 archive되는 흐름. 한 partition 안에서 모든 흐름이 닫힌다.

이게 13장 sharding에서 본 "도메인에 맞는 partition key 선택"의 가장 깨끗한 한국 사례다. Shopify가 shop_id를 골랐고, Slack이 workspace_id를 골랐다면, 당근은 neighborhood_id를 골랐다. 그리고 그 결정이 검색·매칭·dispatch·결제·운영 모두를 단단하게 만든다.

물론 trade-off도 있다. 동 단위 partition은 **공급 부족 동**의 함정이 있다. 신도시처럼 사용자가 적은 동에서는 search 결과가 비어 있을 수 있다. 그래서 당근은 "인접 동" 개념을 두고, 일정 거리 안의 동들을 logical group으로 묶어 검색할 수 있게 한다(추정, 검증 필요). 한 partition을 절대 안 넘는 게 아니라, "도메인이 허용하는 만큼만" 넘는다. 이게 13장 fan-out 패턴의 hyperlocal 변주다.

## hot region — 검색·매칭·지오 공통의 가장 큰 적

여기까지 네 시스템을 봤으면, 한 가지 공통의 적이 보인다. **hot region**이다.

- **쿠팡 검색**: 신상품 출시 직후 검색 query 90%가 한 카테고리에 몰림.
- **Airbnb 검색**: 휴가철 한 region의 숙소 검색이 정상 50배.
- **Uber dispatch**: 야구 경기 끝난 시점, 한 H3 cell의 ride 요청이 폭주.
- **당근**: 인기 거래 동(예: 강남)의 트래픽이 다른 동의 100배.

같은 그림이다. 13장에서 본 hot partition의 검색·매칭·지오 도메인 변주다. 모든 시스템이 평소에는 잘 돌다가, 한 region의 burst가 들어오면 시스템이 비명을 지른다.

대응 패턴 셋만 정리해두자.

1. **shard skew 모니터링**: 14장 관측성의 한 자리. 한 shard의 QPS가 평소 5배 이상이면 즉시 alert. region 단위로 트래픽 분포를 시각화한다.
2. **hot region replica 추가**: 인기 region은 read replica를 더 둔다. 신도시·강남·휴가지 같은 자리에 미리 capacity를 예치한다.
3. **rate limit by region**: 13장 rate limit과 14장 백프레셔 패턴. 한 region이 cluster 전체를 못 죽이도록 region별 token bucket을 둔다.

이 셋이 hot region을 흡수하는 일반 패턴이다. 그리고 그 위에 도메인별 미세 조정이 들어간다. 당근의 동 단위 burst는 신도시 launch 일정에 맞춰 사전 capacity를 늘린다. Uber는 콘서트·스포츠 경기 일정을 미리 알고 driver supply를 인센티브로 모은다. 도메인을 알면 burst를 예측할 수 있다 — 이게 글로벌 framework 위의 로컬 지식의 가치다.

## Sidebar: 다른 유사 시스템 한 단락 — Airbnb Categories ML

본문이 다루지 못한 검색 도메인의 또 다른 사례를 한 단락으로 봐 두자. **Airbnb의 Categories ML** 시스템이다(검증 필요).

Airbnb는 검색 결과를 단순 list로만 보여주지 않는다. "초소형 주택", "성", "트리하우스" 같은 카테고리로 묶어서 사용자가 visual하게 탐색하게 한다. 이 카테고리 분류는 ML 모델이 숙소 사진과 description을 보고 자동으로 부여한다. 모델이 새 카테고리를 발견하면 디자이너가 검토하고 출시한다.

이 시스템의 흥미로운 부분은 **사용자 query가 없는 검색**이라는 점이다. 사용자가 단어를 입력하지 않아도, 사진 한 장을 보고 "이거 마음에 들어"로 매칭이 일어난다. 검색·매칭·discovery의 경계가 흐려진 자리다. 한국에서는 무신사의 큐레이션 시스템이 비슷한 결로 운영된다. 검색이 query-driven에서 discovery-driven으로 옮겨가는 큰 흐름 중 하나다.

## Sidebar: 이 시스템의 운영 — region별 shard skew alert

검색·매칭·지오의 운영을 한 페이지 따로 보자. 14장 일반론이 이 도메인에서 어떻게 변주되는지의 사례다.

**핵심 SLI**: search query p99 (목표 200ms), dispatch matching latency p99 (목표 500ms), match success rate (목표 99%), region별 shard QPS skew (목표 평균 대비 3배 이하). 마지막이 도메인 특수 SLI다.

**Region별 alert 임계값**: 일반 시스템은 평균값으로 alert를 잡는데, 검색·매칭·지오는 그러면 안 된다. 강남 동이 정상 트래픽이 다른 동의 10배라, 평균값으로 alert를 잡으면 강남이 항상 alert가 떠 있고 다른 동의 burst는 묻힌다. **region별 historical baseline의 3배 이상**이 alert 기준이 된다. 14장의 fast/slow burn rate alerting을 region 단위로 변주한 셈이다.

**Shard skew 대응 runbook**: alert가 떴을 때 운영자가 무엇을 하는가? 4단계 runbook이 표준이다. (1) 어떤 region·shard인지 확인 → (2) 트래픽 패턴이 정상 burst(예: 콘서트, 신도시 launch)인지 비정상인지 분간 → (3) 정상이면 capacity 늘리기, 비정상이면 rate limit 강화 → (4) 30분 후 재확인. 이 runbook이 새벽 3시 alert를 5분 안에 끝낸다.

**Rollback 전략**: 검색·매칭의 ML 모델 변경은 점진적이어야 한다. canary 1% → 10% → 100%. 모델 변경이 매칭 성공률을 0.5%만 떨어뜨려도 사용자 만족도가 폭락한다. 14장의 progressive rollout이 모델 단위로 적용된다.

**Region-level chaos game day**: 분기별로 한 region의 검색 cluster를 의도적으로 끊는다. 다른 region이 어떻게 그 부하를 흡수하는지를 본다. cross-region routing과 fallback이 잘 동작하는지의 검증 자리다.

이 운영 5축이 검색·매칭·지오의 24/7 안정성을 만든다. **운영이 도메인 특수성을 담을 수 있을 때 시스템 디자인이 비로소 완성된다는 사실**을 잊지 말자.

## 이 장의 약속 회수

검색·매칭·지오 시스템 셋을 직접 설계할 일이 없는 사람도, 이 장을 다 읽으면 다음 한 페이지를 머릿속에 가지고 갈 수 있다.

- **공통 골격 4단계**: index → candidate retrieval → scoring·ranking → dispatch.
- **5개 시스템의 핵심 결정**: 쿠팡(NORI + Kafka indexing pipeline), Airbnb(IVF over HNSW), Uber(H3 + DISCO multi-objective), 당근(동 단위 partition), 배민(1대N batching).
- **공통의 적**: hot region. 13장의 hot partition이 region 단위로 변주된 그림.
- **운영 1번 신호**: region별 shard skew alert. 평균값이 아닌 region별 historical baseline.

새로운 검색·매칭·지오 시스템을 봤을 때, 이 골격 위에 그 시스템의 결정을 한 자리씩 박을 수 있게 된다. 그게 케이스 스터디의 약속이다.

기억해두자. **검색·매칭·지오 시스템 설계의 본질은 자기 도메인의 update 패턴과 burst 패턴을 정직하게 정의하는 일이다.** Airbnb가 가용성 update 빈도를 적으로 정의했기 때문에 HNSW가 아닌 IVF를 골랐다. 당근이 동 단위 라이프사이클을 정직하게 받아들였기 때문에 동을 partition key로 박았다. 도메인을 정직하게 보면 알고리즘이 알아서 선택된다.

## 다음 장으로 가는 다리

검색·매칭·지오가 "어디·무엇"의 매칭을 다뤘다면, 다음 장은 책의 클라이맥스 — **결제·금융**이다. **"한 번도 두 번 결제되지 않고, 한 번도 누락되지 않는다"**는 명제가 책 전체 약속의 가장 강한 검증이 되는 자리다. Toss·카카오뱅크·Stripe가 어떻게 1·2부의 9개 부품과 6개 패턴을 모두 한 시스템 안에 동시에 박았는지를 본다. 한국 결제의 본인인증·PG vendor lock-in·0시 트래픽·전자금융감독규정·audit chain이 모두 모인다.

가기 전에 한 번 정리하자. **검색·매칭·지오의 가장 흥미로운 자리는 글로벌 알고리즘 위에 로컬 도메인 지식이 얹히는 자리다.** H3는 글로벌 표준이지만, 그 위에 어떤 multi-objective를 얹는가는 한국 환경의 결정이다. 한국 개발자가 그 결정의 깊이에서 일할 수 있는 자리가 점점 많아지고 있다는 사실이 흥미롭다.

---

*챕터 작성 메모: 02_plan §3 18장 사양 충실 반영. 공통 4단계 골격 (index/candidate/scoring/dispatch) / 쿠팡 검색 + 한국어 형태소 + indexing pipeline silent killer / Airbnb IVF vs HNSW / Uber H3 + DISCO multi-objective + 배민 1대N 변주 / 당근 동 단위 partition + 인접 동 logical group / hot region 공통의 적 + 3가지 대응 / Airbnb Categories ML 유사 시스템 sidebar / region별 shard skew alert 운영 sidebar. W26 Uber, W28 Airbnb, W32 쿠팡, W31·한국 7 당근, 한국 3 형태소 분석 인용. 일부 미공개 운영 디테일(쿠팡 NORI 활용, 당근 인접 동 logical group, Airbnb Categories) "(검증 필요)" 라벨. 분량 약 22p 추정 (한국어 ~6800자). 1·2부 callback: 5장(검색·형태소), 10장(circuit breaker organization standard), 13장(sharding·hot region·fan-out), 14장(burn rate alerting·region 변주). 16장 sidebar(카카오톡 group push)도 callback. 다음 19장 결제 클라이맥스로 다리.*
