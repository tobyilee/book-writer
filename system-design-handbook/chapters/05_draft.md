# 5장. 검색 엔진 — 한국어가 영어 분석기로 안 되는 이유부터

신입 개발자가 처음으로 검색 페이지를 만들었다고 해보자. Elasticsearch를 띄우고, `match` 쿼리를 박고, 화면에 결과를 뿌렸다. 로컬에서 테스트하니 잘 된다. 그런데 production에 올렸더니 사용자가 "쿠팡 배송"을 검색했는데, "쿠팡배송"이라고 띄어쓰기가 다른 글이 안 잡힌다고 항의가 들어온다.

개발자는 어이가 없다. "쿠팡 배송"이나 "쿠팡배송"이나 같은 말 아닌가? 그런데 Elasticsearch는 그렇게 보지 않는다. 영어 분석기는 공백을 단어 경계로 보고 토큰을 자른다. "쿠팡 배송"은 "쿠팡"과 "배송" 두 토큰, "쿠팡배송"은 "쿠팡배송"이라는 한 토큰. 둘은 같은 단어가 아니라 완전히 다른 토큰이다. 그러니 매칭이 안 된다.

이게 한국어 검색의 첫 관문이다. 영어책에는 안 나오는 문제다. 영어는 띄어쓰기가 단어 경계라 그냥 두면 된다. 한국어는 조사가 붙고, 띄어쓰기가 규범과 다르게 쓰이고, 합성어가 띄어쓰기를 넘어 만들어진다. 검색이 어렵다.

검색 엔진은 결코 단순한 "match 쿼리 한 줄"이 아니다. 한국어 관점에서 깊게 들어가야 비로소 부품의 진짜 모양이 보인다. inverted index가 무엇을 약속하는지, 한국어 형태소 분석기 5종이 어떻게 다른지, Elasticsearch의 shard 100개가 과연 무슨 결정이었는지, 그리고 vector search가 무대로 올라오는 순간 무엇이 또 바뀌는지 — 한 박자씩 짚어 보자.

## Inverted Index — 검색이 빠른 진짜 이유

검색 엔진의 심장은 **inverted index**다. 일반 인덱스는 "row → 컬럼 값"이지만, inverted index는 "단어 → 그 단어가 등장한 문서들"이다. 마치 책 끝에 붙어 있는 색인을 생각하면 가깝다. 단어가 알파벳 순으로 정렬되어 있고, 그 옆에 등장한 페이지가 적혀 있다.

```
문서 1: "쿠팡 배송 빠르다"
문서 2: "쿠팡 직구 배송"
문서 3: "배송 추적 어디서"

inverted index:
  쿠팡   → [1, 2]
  배송   → [1, 2, 3]
  빠르다 → [1]
  직구   → [2]
  추적   → [3]
  어디서 → [3]
```

이 구조 덕분에 "쿠팡"으로 검색하면, 전체 문서를 다 스캔하지 않고 색인의 "쿠팡" 항목만 보면 끝난다. 100만 개 문서가 있어도 검색은 거의 즉시다.

여기서 두 가지 흥미로운 함의가 나온다.

**첫째, 색인이 무거운 작업이다.** 새 문서가 들어올 때마다 모든 토큰을 추출해 색인을 갱신해야 한다. 이걸 동기로 처리하면 write가 매우 느려진다. 그래서 검색 엔진은 보통 색인을 비동기로 처리한다. write와 read 사이에 **인덱싱 지연(indexing lag)**이 존재한다.

**둘째, 토큰을 어떻게 자르냐가 검색 품질을 결정한다.** "쿠팡 배송"을 어떻게 토큰화하는지가 결국 "쿠팡배송"이라는 검색어가 잡히느냐 안 잡히느냐를 결정한다. 이게 한국어 검색이 영어 검색과 결정적으로 갈리는 지점이다.

## Lucene과 Elasticsearch — 같은 심장, 다른 옷

Elasticsearch는 자체 검색 엔진이 아니다. 심장은 **Lucene**이다. Lucene은 자바로 짠 inverted index 라이브러리고, Elasticsearch는 그 Lucene 위에 분산 처리, REST API, 클러스터 운영, 메트릭 등 엔터프라이즈 기능을 입힌 wrapper(외피)다. Solr도 Lucene 기반이다.

이 사실이 의외로 중요하다. 한 가지 결과로 이어진다 — **Elasticsearch 운영 함정의 절반은 Lucene 함정이다.** segment 구조, refresh, merge, 분석기 동작 — 모두 Lucene 레벨에서 일어난다. Elasticsearch 매뉴얼만 봐서는 어디가 어디인지 헷갈리는 경우가 많다.

Lucene의 핵심 개념을 짧게 정리하자.

- **Index = shard들의 모음**. 각 shard는 Lucene index 한 개.
- **Segment = shard 안의 immutable 파일 단위**. 한 번 쓰여진 segment는 수정 불가, 삭제는 tombstone으로 표시.
- **Refresh = 메모리 buffer의 데이터를 새 segment로 flush해 검색 가능하게 만드는 작업.** default 1초.
- **Merge = 작은 segment들을 큰 segment로 합치는 작업.** I/O 부담이 큼, background에서 진행.
- **Flush = WAL(translog)을 디스크에 동기화.** durability 보장.

이 다섯 개념이 머릿속에 있어야 Elasticsearch 운영 함정을 디버깅할 수 있다. 안 그러면 매번 "왜 검색이 안 되지?", "왜 디스크가 가득 차지?" 같은 새벽 질문을 받게 된다.

## 한국어 분석기 5종 — mecab-ko, NORI, KOMORAN, Khaiii, KIWI

토큰을 어떻게 자르냐의 문제로 돌아오자. 영어는 공백·구두점 기준으로 자르면 거의 끝이다. 한국어는 그렇지 않다. 다음 분석기 5종이 한국어 검색의 주요 선택지다.

| 분석기 | 출처 | 기반 | 특징 |
|--------|------|------|------|
| **mecab-ko (은전한닢)** | 일본 mecab 한국어 포트 | 사전 기반 | 가장 오래되고 안정적. 사전 갱신이 보수적. |
| **NORI** | Lucene 내장 (KOMORAN 기반) | 사전 + 규칙 | Elasticsearch 기본 한국어 분석기. 의존성 없이 깔리는 장점. |
| **KOMORAN** | shineware | 사전 + 규칙 | 사용자 사전 추가 쉬움. 한국어 형태소 분석기 비교 글에 자주 등장. |
| **Khaiii** | 카카오 | CNN 기반 (deep learning) | 비교적 새 모델. 신조어·구어체 강함. |
| **KIWI** | 한국어 형태소 오픈소스 | 사전 + 통계 | 빠른 속도, 사용자 사전 손쉬움. 최근 한국 백엔드에서 인기 상승. |

이 다섯이 각각 어떻게 자를까? "쿠팡 배송 빠르다"라는 문장을 한 번 비교해 보자(개략적인 결과 — 실제 출력은 버전별로 다를 수 있다, 검증 필요).

```
mecab-ko:  [쿠팡(고유명사), 배송(명사), 빠르(형용사 어간), 다(어미)]
NORI:      [쿠팡, 배송, 빠르다]
KIWI:      [쿠팡(NNP), 배송(NNG), 빠르(VA), 다(EF)]
```

조사, 어미가 분리되거나 아니거나, 어간만 남기거나 어형까지 남기거나 차이가 있다. 검색 품질은 이 토큰화의 디테일에 좌우된다.

그리고 한국어 검색에는 두 가지 추가 처리가 거의 필수다.

**1. Synonym (동의어).** "삼성전자" ↔ "삼성", "맥북" ↔ "MacBook" 같은 동의어 사전. 이건 분석기와 별개로 Elasticsearch synonym filter로 처리한다.

**2. n-gram 또는 부분 매칭.** "쿠팡 배송"으로 검색했을 때 "쿠팡배송"도 잡히게 하려면 n-gram을 함께 색인하는 패턴이 자주 쓰인다. 예를 들어 2-gram이면 "쿠팡배송"은 ["쿠팡", "팡배", "배송"]으로 색인된다. 색인 크기가 커지는 부담이 있지만, 부분 매칭이 가능해진다.

> 💡 한국어 검색을 시작할 때 분석기 선택의 한 줄 가이드. **새 프로젝트면 KIWI 또는 NORI로 시작하자.** Khaiii는 신조어·구어체 강점이 명확한 도메인(채팅·SNS)에 한해 검토. mecab-ko는 안정성으로 굳어진 곳에서 계속 쓰는 편이 낫지만, 새 프로젝트의 default로는 KIWI·NORI가 운영 도구 풍부함에서 앞선다.

## "쿠팡 배송" vs "쿠팡배송" — 한국어 검색 7가지 함정

5종 분석기 중 무엇을 골라도 한국어 검색의 함정은 비슷하다. 한국 백엔드에서 자주 만나는 7가지를 정리하자.

**1. 합성어 띄어쓰기.** "쿠팡 배송" vs "쿠팡배송", "강남역" vs "강남 역". 사용자는 자기 마음대로 띄어 쓴다. n-gram 색인 또는 띄어쓰기 정규화가 필요하다.

**2. 조사·어미 처리.** "배송이", "배송을", "배송에서"가 다 "배송"의 변형이다. 형태소 분석기가 어간을 추출하므로 보통 해결되지만, 색인 시와 검색 시 동일한 분석기를 적용해야 한다.

**3. 신조어·외래어.** "맥북" / "MacBook" / "맥북프로" / "Macbook Pro", "갓성비" / "가성비". 사전 기반 분석기는 사용자 사전을 정기 갱신해야 한다.

**4. 영문·한글 혼용.** "iPhone 15" 검색이 "아이폰 15"도 잡히게 할지, "iphone15" 띄어쓰기 없는 입력도 잡히게 할지. synonym + n-gram 조합으로 풀거나, 입력 시점에 normalize한다.

**5. 자동완성·오타 교정.** "쿠팡"을 치다 "쿠퍙"으로 친다든지. edit distance 기반 fuzzy 검색, 또는 자모 단위 색인으로 풀 수 있다. Elasticsearch의 `completion suggester`, `phonetic analyzer` 등이 도구.

**6. 검색 의도 분기.** "쿠팡 배송"을 친 사용자는 (a) 쿠팡의 배송 정책을 찾는 건가 (b) 쿠팡으로 배송된 상품을 찾는 건가? 같은 검색어가 도메인에 따라 다른 의도다. 의도 분류는 검색 quality team의 주요 과제다.

**7. 색인 갱신 지연.** 새 상품 정보를 등록했는데 검색에서 안 잡힌다는 항의. inverted index 특성상 indexing lag이 있다. `refresh_interval`을 줄이거나, 갱신 후 명시적 `_refresh` 호출이 필요한 경우가 있다.

이 7가지를 다 한 번에 풀 수는 없다. 도메인에 따라 우선순위가 다르다. 이커머스는 1·3이 중요하고, 채팅 검색은 5가 중요하고, 뉴스 검색은 6이 중요하다. **무엇을 먼저 풀지 도메인이 결정하게 두는 편이 낫다.**

## Shard 설계 — 100개가 정말 필요했는가

Elasticsearch 운영의 가장 자주 묻는 질문이 "shard를 몇 개로 잡을까"다. 한국 백엔드에서 "shard 100개", "shard 200개"라는 발표를 들으면 멋있어 보이지만, 정작 그게 정말 필요했는지를 묻는 사람은 적다.

Elastic 공식 가이드의 한 줄이 가장 직설적이다.

> An optimal shard should hold 10-50GB of data, with fewer than 200 million documents per shard. (Elastic Docs, *Shards and Replicas Guide*)

shard 하나당 10~50GB, 2억 doc 이하. 이 한 줄에서 시작하자. 우리 인덱스가 100GB라면 shard 2~10개면 충분하다. 100GB 인덱스에 shard 100개를 박는 건 shard당 1GB 꼴이고, 이건 oversharding이다.

oversharding이 왜 문제일까?

- **shard마다 Lucene 오버헤드.** segment 메타데이터, 메모리, 파일 핸들이 shard 수만큼 곱해진다.
- **검색 시 모든 shard에 fan-out.** 검색 한 번이 100개 shard를 거치니, 네트워크·CPU 부담이 곱해진다.
- **cluster state 비대.** shard가 많으면 master node의 cluster state 관리가 무거워져, master가 느려진다.

undersharding은 반대로 한 shard가 너무 커져 검색·인덱싱이 한 노드에 집중된다. 50GB를 넘어가면 GC, merge, recovery가 모두 끔찍해진다.

그래서 정상 범위는 **인덱스 크기 / 30GB 정도가 shard 수의 시작점**이다. 거기에 미래 성장 + 여유분으로 1.5배쯤 잡는다. 100GB 인덱스라면 shard 4~5개, 1TB 인덱스라면 30~40개. 처음부터 100개를 박는 게 아니라, 인덱스가 자라면서 새 인덱스를 만들거나 reindex로 재구성하는 편이 낫다.

> 💡 한국 백엔드의 흔한 함정 — "남들이 shard 100개라고 하니까 우리도." 도구 도입의 자격 검증과 같은 결의 함정이다. 우리 데이터 크기가 shard 100개를 요구하는가? 답이 "아니다"라면 100개는 oversharding이고 운영 부담만 늘린다. **shard 수는 패션이 아니라 데이터 크기의 함수다.**

## JVM Heap — 32GB의 마법선

Elasticsearch는 자바로 짠 시스템이다. JVM 위에서 돌고, JVM의 GC가 latency에 직접 영향을 준다. 그래서 JVM 튜닝의 한 줄 규칙이 한국·해외 모두에 정착되어 있다.

> Above ~32GB, pointers become 64-bit, you lose compressed oops, and you might as well have 60GB to break even. (heuristic #1 in 한국 운영 커뮤니티)

JVM은 64-bit OS에서 기본 포인터가 64-bit지만, heap이 32GB 이하면 **compressed oops**(ordinary object pointers)로 32-bit 포인터를 쓴다. heap이 작아서가 아니라, 메모리 효율을 위해 압축된 포인터를 쓰는 것. 32GB를 넘는 순간 이 압축이 풀려, 같은 객체 수에 메모리가 더 들고 cache miss가 늘어 오히려 느려진다.

그래서 ES·Cassandra·Kafka·Solr 등 JVM 기반 시스템의 heap은 모두 **30GB 또는 31GB 이하로 잡는 게 표준**이다. 한 노드의 메모리가 128GB라면 ES heap은 30GB, 나머지 98GB는 OS file system cache로 쓴다. Lucene의 inverted index는 file system cache의 효과가 매우 크기 때문에 이 분배가 합리적이다.

이 한 줄 규칙을 어기는 운영을 한 번 본 적 있다. 메모리 256GB짜리 ES 노드에 heap을 128GB로 잡았는데, GC pause가 늘어 latency p99가 30초까지 솟구쳤다. 적정 heap(30GB)으로 줄였더니 같은 노드에서 latency p99가 200ms로 돌아왔다. JVM tuning은 작은 결정 같지만 운영에서 가장 큰 차이를 만들 수 있다.

## `refresh_interval` — 1초 default의 함정

Elasticsearch가 새 문서를 색인하면, default 1초마다 segment를 만들어 검색 가능하게 한다(`refresh_interval=1s`). 거의 실시간으로 검색이 된다는 약속이다.

그런데 이 default가 write-heavy 시스템에서는 끔찍한 함정이다. write가 분당 수만 건씩 들어오는 indexing pipeline이라면, 매초 segment가 만들어진다. segment가 빠르게 늘면 merge가 따라가지 못하고, merge가 느려지면 디스크 IO가 폭증하고, GC가 잦아진다. 결과적으로 색인 throughput이 절반으로 떨어진다. 새 ES 클러스터 띄운 첫 주의 일상이다 — 부하 테스트에서는 보이지 않다가 production 트래픽이 들어오자마자 찜찜한 lag 차트가 등장한다.

해결은 단순하다 — **write-heavy 인덱스의 `refresh_interval`을 30초 또는 60초로 늘리자.**

```
PUT /products/_settings
{
  "refresh_interval": "30s"
}
```

이 한 줄로 throughput이 2~3배 올라가는 경우가 흔하다. 단, 새 문서가 검색에 보이기까지 30초 지연이 생긴다. 30초 지연을 못 견디는 도메인(실시간 chat 검색 등)은 1초를 유지하거나, 아예 검색 직전에 `_refresh`를 명시적으로 호출하는 패턴을 쓴다.

그리고 한 가지 더 — **bulk indexing 시에는 `refresh_interval`을 -1로 잡고, 끝난 뒤에 한 번 refresh하는 패턴**이 표준이다. 1억 doc을 색인하는 batch라면 이 패턴이 throughput을 10배 늘릴 수 있다.

tribal #17 — "refresh_interval 1초 default 함정"이 한국 운영 커뮤니티에 단골로 올라오는 이유다. 새 ES 클러스터 만들 때 이 한 줄을 챙기는 편이 낫다.

## ES vs OpenSearch 분기 — 그리고 자체 엔진

2021년 Elastic이 라이선스를 SSPL로 바꿨고, AWS는 그 직전 fork인 ES 7.10을 기반으로 **OpenSearch**를 분리했다. 그 이후 두 엔진은 다른 길로 분기 중이다.

| 항목 | Elasticsearch | OpenSearch |
|------|---------------|-----------|
| 라이선스 | Elastic License v2 / SSPL (상용) | Apache 2.0 (완전 오픈) |
| 매니지드 | Elastic Cloud, AWS Elastic Cloud | AWS OpenSearch Service |
| 부가 기능 | ML, alerting, security 풍부 | 일부 무료 (보안·alerting 포함) |
| ML | Elastic ML 라이선스 별도 | OpenSearch ML 무료 |
| Vector search | dense_vector + HNSW | k-NN plugin (HNSW) |

새 프로젝트가 AWS 중심이고 비용 절감이 우선이라면 OpenSearch가 합리적이다. Elastic의 부가 기능(ML, security)이 필요하면 Elasticsearch. 한국 백엔드에서는 양쪽 모두 채택 사례가 있다.

한 가지 더, 큰 회사는 종종 **자체 엔진**을 만든다. LINE NSE, 카카오 다음 검색, 네이버 자체 검색 엔진. 이유는 단순하다 — ES·OpenSearch가 못 풀어주는 특정 도메인 문제가 있어서다.

- **LINE NSE.** 메신저 대화 검색은 일반 ES로 안 풀리는 이슈가 많다(privacy, encryption, multi-language).
- **네이버.** 한국어 형태소 + 다음·네이버 도메인 + 광고·랭킹 알고리즘. ES로는 부족하다.
- **Slack KalDB.** Slack 메시지 검색은 ES로 했지만, **로그 검색은 ES 한계로 자체 KalDB 개발**. logz.io의 분석에 따르면 ES가 로그 같은 high-volume immutable data에 비싸다는 평가다.

자체 엔진을 만든다는 결정은 거의 항상 **연 100만 query 이상**의 규모이고, **20명 이상의 search team**이 있는 회사의 결정이다. 일반 한국 백엔드 팀의 자격 검증을 통과하지 않는다. ES·OpenSearch가 충분한 선택이고, 자체 엔진은 안 만드는 편이 낫다.

## 쿠팡 검색 — Kafka 기반 indexing pipeline

한국 백엔드에서 가장 자주 인용되는 검색 사례는 쿠팡이다. 쿠팡 엔지니어링 Medium에 "Fueling the Coupang Search Engine"이라는 글이 있다.

핵심 구조는 다음과 같다.

1. **상품 데이터의 변화**(가격·재고·설명 등 변경)가 일어나면, 상품 service가 **Kafka**에 변경 이벤트를 발행한다.
2. **indexing pipeline**(자체 구축)이 이 이벤트를 consume해, 검색용 schema로 변환한다. ML 기반 feature, 카테고리 분류 등이 이 단계에서 추가된다.
3. 변환된 doc을 **Elasticsearch**(또는 자체 엔진)에 색인한다.
4. **검색 API**가 ES를 호출해 결과를 반환한다.

이 구조의 가치는 **decoupling**이다. 상품 service는 검색 schema를 모른다. 검색 indexing pipeline은 상품 DB schema를 모른다. 둘은 Kafka의 이벤트 schema로만 묶인다. 4장 메시지 큐 챕터에서 본 그 decoupling 패턴이 여기서 그대로 작동한다.

그리고 한 가지 더 흥미로운 점 — **rebuild가 쉽다**. 검색 schema를 바꿔야 한다면, 새 ES 인덱스를 만들고 Kafka offset 0부터 다시 consume하면 된다. Kafka의 retention 안에서 replay가 가능하기 때문이다. 검색 schema는 도메인이 진화하면 자주 바뀌는데, 이 rebuild 패턴이 그 진화를 견디는 무기다.

## Slack 검색 — 메시지와 로그를 가르는 결정

Slack은 10B 메시지 이상을 다루는데, **검색은 Elasticsearch, 로그는 자체 KalDB**라는 결정을 했다. 같은 검색이라도 도메인에 따라 도구를 가른 사례다.

왜 갈렸을까? 두 도메인의 특성이 다르기 때문이다.

| 차원 | 메시지 검색 | 로그 검색 |
|------|-----------|----------|
| 빈도 | 사용자가 자주 검색 | 디버깅 시에만 |
| 데이터 양 | 메시지 1개당 작음, 총량 큼 | 로그 1개당 더 작음, 총량 훨씬 큼 |
| ranking | 관련도, 시간, 채널 가중 등 복잡 | 시간 순 + 키워드 필터 단순 |
| 갱신 | append-only | append-only |
| 가용성 | high (사용자 영향 직접) | medium (디버깅용) |

메시지는 ranking이 복잡하고 사용자에게 즉시 영향을 주니 ES가 잘 맞는다. 로그는 단순 시간 순 + 필터, 그리고 데이터 양이 너무 커서 ES의 비용이 감당이 안 된다. 그래서 자체 KalDB로 분리.

**도구는 도메인이 결정한다는 사실**이 여기서도 작동한다. "Slack은 검색에 ES 쓴다"가 아니라, "Slack은 메시지에 ES, 로그에 KalDB"가 정확한 진술이다. 우리도 자기 검색 도메인을 세분화해서, 어디까지 ES이고 어디부터 다른 도구인지 가르는 편이 낫다.

## Vector Search — ANN의 무대

2023년 이후 검색에 새로운 축이 들어왔다. **벡터 검색**, 정확히는 **ANN (Approximate Nearest Neighbor)** 검색이다. LLM이 일상이 된 첫 해에 검색이라는 부품도 자연스럽게 이 새 축을 받아들였다. 텍스트를 임베딩 벡터로 변환해, 의미가 비슷한 문서를 찾는다. "쿠팡 배송"을 검색했을 때 정확히 "쿠팡 배송"이 안 적혀 있어도, 의미가 유사한 "쿠팡 빠른배송", "쿠팡 익일배송" 같은 문서를 찾을 수 있다.

ANN 알고리즘에는 크게 두 갈래가 있다.

- **HNSW (Hierarchical Navigable Small World).** 그래프 기반. 검색 속도 빠름, 메모리 많이 씀, 인덱스 갱신은 비교적 어렵다. Elasticsearch dense_vector, Pinecone, Weaviate가 채택.
- **IVF (Inverted File Index).** 클러스터 기반. 인덱스 갱신 쉬움, 메모리 적게 씀, 검색 정확도는 HNSW보다 약간 낮다. FAISS의 default, Airbnb 채택.

Airbnb의 흥미로운 결정이 여기 있다. Airbnb는 가격·가용성이 매우 자주 바뀌는 도메인이라, **인덱스 갱신 속도가 검색 정확도보다 우선**이라는 결론에 도달했다. 그래서 HNSW가 아닌 IVF를 채택했다. 일반적인 "HNSW가 빠르고 정확하다"는 통념이 도메인에 따라 뒤집힐 수 있다는 사례다.

벡터 검색은 텍스트 검색을 대체하지 않는다. **하이브리드 검색** — 텍스트 매칭 + 벡터 유사도를 함께 쓰는 패턴이 표준이다. Elasticsearch 8.x의 dense_vector + BM25 결합, OpenSearch의 k-NN + 일반 검색 결합이 그 모양이다. 한국 백엔드에서도 2025년부터 본격적으로 채택 사례가 늘고 있다.

자세한 내용은 15장 데이터 파이프라인·CRDT 챕터에서 vector DB(Pinecone, Weaviate, pgvector)와 함께 다시 다룬다. 검색 엔진은 이제 텍스트와 벡터의 양 축을 가르는 부품이다.

## 검색 운영 함정 5가지 정리

지금까지 살펴본 함정들을 한 번 정리하자. 새 ES 클러스터를 띄울 때 챙겨야 할 5가지다.

| # | 함정 | 대처 |
|---|------|------|
| 1 | shard oversharding | 인덱스 크기 / 30GB 시작점. 패션이 아니라 데이터 함수. |
| 2 | JVM heap > 32GB | 30GB 이하로 잡고 나머지는 file system cache로. |
| 3 | refresh_interval 1초 default | write-heavy 인덱스는 30s 또는 60s로. bulk는 -1. |
| 4 | 분석기 mismatch | 색인 시와 검색 시 동일 분석기 사용. 한국어는 NORI·KIWI 시작. |
| 5 | indexing lag 무관심 | producer→Kafka→indexer→ES 사이 latency 모니터링. lag을 SLO에 포함. |

이 5가지를 default로 챙기는 ES 클러스터는 한국 백엔드 평균보다 훨씬 안정적이다.

## 검색 도입 자격을 묻는 5가지 질문

마지막으로 메타 질문. 새 시스템에 검색 엔진을 도입하려는 결정 앞에서 자기에게 던질 5가지 질문이다.

1. **DB로 충분히 풀리지 않는가?** Postgres의 `tsvector`, MySQL의 `FULLTEXT` 인덱스로 처음에는 충분한 경우가 많다. 휴리스틱 3 "Just use Postgres"의 한 영역이다.
2. **검색 트래픽이 어느 정도인가?** QPS가 낮으면 ES의 운영 부담을 정당화하기 어렵다.
3. **한국어 처리가 필요한가?** 필요하다면 분석기를 어디까지 튜닝할 것인가?
4. **indexing pipeline을 어떻게 만들 것인가?** dual-write로 갈 것인가, Kafka 기반 event sourcing으로 갈 것인가?
5. **운영 부담을 짊어질 수 있는가?** ES는 운영이 무거운 시스템이다. 자체 운영할지, 매니지드(Elastic Cloud, AWS OpenSearch)로 갈지 결정해야 한다.

이 다섯에 답이 명확하지 않다면, 우선 Postgres `tsvector`로 시작해서 한계가 오면 ES로 옮기는 편이 낫다. **검색 엔진 도입의 자격은 검색 트래픽이 보장해 준다.**

## Callback 예고

검색 엔진은 책 후반에 다시 나타난다.

- **15장 데이터 파이프라인·CRDT.** vector DB와 ANN 알고리즘을 깊게.
- **18장 검색·매칭·지오.** 매칭 시스템(Uber·당근·배민 라이더)의 search + geo + ranking 결합.

이 두 챕터에서 5장의 기초가 그대로 얹힌다. inverted index, 분석기, shard 설계, JVM tuning — 모두 그 위에서 도메인별 디자인이 펼쳐진다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 검색 엔진의 한국어 관점이 손에 잡혀 있다. inverted index의 약속, Lucene과 Elasticsearch의 관계, 한국어 분석기 5종, "쿠팡 배송 vs 쿠팡배송"의 함정, shard 설계와 JVM heap, refresh_interval, ES vs OpenSearch 분기, 그리고 쿠팡·Slack·Airbnb의 검색 사례까지. 마지막으로 vector search라는 새 축이 어떻게 텍스트 검색 옆에 자리잡았는지가 한 묶음이다.

기억해두자. **검색 엔진은 'match 쿼리'가 아니라 토큰화·shard·refresh의 트리오로 결정된다.** 그리고 영어책에 안 나오는 한국어 함정이 우리 일상이다. 이 함정의 모양이 머릿속에 자동으로 펼쳐질 때, 우리는 "검색을 안다"고 말할 자격이 있는 백엔드 개발자가 되어 있다.

다음 장에서는 로드 밸런서·게이트웨이·서비스 메시를 살펴본다. L4와 L7이 운영 관점에서 어떻게 다른지, 그리고 5명짜리 팀이 Istio를 깔았다가 한 주의 절반을 mesh 튜닝에 쓰게 되는 그 함정의 모양을 함께 짚어 보자.
