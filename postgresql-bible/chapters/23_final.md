# 23장. 성능 튜닝 종합 — 인덱스부터 파티셔닝까지

느린 쿼리 하나를 받았다고 해보자. 어제까지 200ms로 잘 돌던 주문 조회가 오늘 아침 갑자기 4초가 됐고, 알람이 울리고, Slack 한구석에서 누군가가 스크린샷을 던졌다. 그 자리에 모인 셋 중 하나는 "인덱스부터 추가하자"고 하고, 다른 하나는 "EXPLAIN부터 보자"고 한다. 또 한 사람은 조용히 `pg_stat_activity`를 열어본다. 셋 다 옳다. 그런데 그 셋 사이에는 사실 작은 단계들이 잔뜩 있다. 그 단계를 한 번 같이 밟아보자.

이 챕터는 새로운 지식을 던지는 챕터가 아니다. 지금까지 책에서 본 것들 — 4장의 fork 모델, 5장의 MVCC, 6장의 HOT, 18장의 vacuum, 21장의 옵저버빌리티 — 을 한 의사결정으로 합치는 챕터다. 인덱스 매트릭스부터 EXPLAIN 읽기, 흔한 함정 여섯 가지, 병렬 쿼리, 파티셔닝, OS 레벨 체크리스트까지 짚고 마지막에는 "느린 쿼리 한 장을 받았을 때 어떤 순서로 진단하고 어떻게 처방할 것인가"의 한 페이지짜리 흐름도로 마무리한다. 23장이 끝날 무렵에는, EXPLAIN 출력 한 장을 손에 받았을 때 "다음 한 수"가 머릿속에서 떠오르는 단계까지 가보자.

## 23.1 인덱스 선택 매트릭스

인덱스를 추가하는 일이 성능 문제의 첫 처방으로 떠오르는 데는 이유가 있다. 잘 맞는 인덱스 하나가 4초짜리 쿼리를 40ms로 만드는 일은 실제로 일어난다. 그런데 잘 맞지 않는 인덱스를 더하면, 읽기는 조금 빨라지지만 쓰기가 느려지고, 디스크가 잠식되고, vacuum이 무거워진다. 그러니 추가하기 전에 한 번은 생각해보자. **이 컬럼, 이 쿼리, 이 데이터 분포에 어떤 인덱스가 어울리는가?**

PostgreSQL은 여섯 종류의 인덱스를 기본으로 들고 있다. 각자 다른 데이터 모양을 위해 설계됐다. 한 종류로 모든 문제를 풀려고 하면 어딘가에서 반드시 비효율이 새 나온다.

### B-tree — 의심스러우면 일단 B-tree

`CREATE INDEX` 뒤에 아무 옵션도 안 붙이면 PostgreSQL은 B-tree를 만든다. 그게 디폴트인 데는 합당한 이유가 있다. equality(`=`), 범위(`<`, `>`, `BETWEEN`), 정렬(`ORDER BY`), `IS NULL` — 일상 OLTP 쿼리가 만지는 거의 모든 술어에 작동한다. 만약 어떤 인덱스를 써야 할지 잘 모르겠다면, 일단 B-tree를 만들고 EXPLAIN으로 확인해보는 편이 낫다. 95%의 경우 답이다.

B-tree의 한계는 한 가지다. 한 컬럼에 여러 값이 들어가는 다값(multi-value) 컬럼 — 예를 들면 JSONB의 key set, 배열, tsvector — 에는 안 맞는다. 이런 경우는 잠시 뒤에 GIN을 살펴보자.

### Hash — 거의 안 쓰지만 알아는 두자

PG 10부터 Hash 인덱스가 WAL을 남기고 crash-safe가 됐다. 그 이전엔 사실상 쓸 수 없었다. 지금은 쓸 수는 있지만, 그래도 거의 안 쓴다. 이유는 단순하다. **B-tree가 거의 모든 경우 같이 잘하거나 더 잘한다.** Hash가 이론적으로 유리한 영역은 equality only(범위·정렬 안 함) + 매우 긴 키(예: 긴 SHA-256 문자열) 정도다. 이 좁은 영역에서 Hash 인덱스가 B-tree보다 작고, 그래서 조금 빠를 수 있다.

그런데 실무에서는 "지금 equality만 쓰지만 6개월 뒤 누가 정렬을 걸지도 모른다"는 불확실성이 항상 있다. 그 미래를 닫지 않으려면 B-tree가 안전한 선택이다. Hash는 알아두되, 첫 선택지에는 두지 말자.

### GIN — 다값 컬럼의 정답

`SELECT * FROM documents WHERE tags @> ARRAY['postgres', 'tutorial']` 같은 쿼리를 본 적이 있는가? `tags`가 텍스트 배열이고, 그 안에 두 값이 모두 포함된 행을 찾는 쿼리다. 여기서 B-tree는 무력하다. 한 행이 컬럼 하나에 여러 값을 들고 있기 때문이다.

이런 다값 컬럼 — 배열, JSONB, tsvector(전문 검색용) — 에 GIN(Generalized Inverted Index)이 답이다. 이름에 inverted가 들어가는 데서 짐작할 수 있듯, 역색인 구조다. "이 값이 어떤 행들에 들어 있는가"를 거꾸로 추적한다.

GIN의 진가는 JSONB에서 드러난다. `idx ON docs USING GIN(payload jsonb_path_ops)` 한 줄이면 `payload @> '{"status":"paid"}'` 같은 containment 쿼리가 수십 ms 안에 끝난다. 3장에서 JSONB 이야기를 했고, 거기서 "검색은 GIN이 떠받친다"고 한 줄 적어둔 그 GIN이 바로 이것이다.

다만 GIN에는 함정이 있다. **인덱스 빌드와 갱신이 무겁다.** 한 행이 여러 키를 들고 있으니, 한 행을 갱신할 때 인덱스의 여러 자리를 건드려야 한다. 대량 갱신 워크로드에서 GIN은 자주 병목이 된다. 완화 수단으로 `fastupdate` 옵션이 있는데, 펜딩 리스트에 쌓아두고 나중에 합치는 방식이다. 부하 패턴에 따라 켜고 끄는 결정이 갈리니, 한 번에 정답을 내기보다 EXPLAIN과 `pg_stat_user_indexes`로 모니터링하면서 조정하는 편이 낫다.

### GiST — 공간과 범위의 친구

GiST(Generalized Search Tree)는 "트리 구조를 임의 타입에 적용할 수 있는 프레임워크"다. 직관적으로 말하면, 거리·포함 같은 공간적 술어를 다루는 인덱스다. PostGIS의 모든 지리 인덱스가 GiST 위에 올라가 있고, 범위 타입(`int4range`, `tsrange`, `daterange`)의 포함·중복 검색도 GiST가 떠받친다.

지도 위의 "이 좌표에서 가장 가까운 상점 10곳"(KNN 검색)이나, 예약 시스템의 "이 시간대와 겹치는 예약이 있는가"(범위 중복 검사) 같은 쿼리가 GiST의 영역이다. 3.4에서 PostGIS 이야기를 했고, 13장에서 예약·이벤트 패턴을 다뤘다면, 그 두 챕터의 보이지 않는 토대가 GiST다.

GiST의 함정은 equality 위주 쿼리에서는 B-tree보다 느리다는 점이다. "이 컬럼에 equality 쿼리도 자주 나오고 범위 쿼리도 자주 나온다"면, 두 인덱스를 따로 만드는 편이 낫다. 인덱스 디스크를 아끼겠다고 GiST 하나로 모두 풀려고 하지 말자.

### SP-GiST — 비균형 트리가 필요할 때

SP-GiST(Space-Partitioned GiST)는 quadtree, k-d tree, trie 같은 비균형 분할 구조를 인덱스로 만드는 변형이다. 들어본 적이 없다면, 그건 정상이다. 평범한 OLTP에서는 거의 마주칠 일이 없다. 그런데 특정 데이터에서 SP-GiST가 GiST보다 훨씬 깔끔하게 일을 한다.

대표 사례 세 가지를 짚어두자. (1) 전화번호 prefix 라우팅 — `010-1234-5678`을 trie로 인덱싱하면 prefix 검색이 매우 빠르다. (2) IP 주소·CIDR — 네트워크 prefix 매칭이 trie와 잘 맞는다. (3) 비균형 분포의 GIS 데이터 — 한쪽 지역에 점이 몰려 있는 경우 quadtree가 균형 트리보다 효율적이다.

평범하게 쓸 일은 적지만, "이 데이터 모양은 분명히 trie구나" 싶을 때 SP-GiST를 떠올릴 수 있어야 한다. 알아두자, 그것으로 충분하다.

### BRIN — 거대한 정렬된 테이블의 가벼운 동반자

BRIN(Block Range INdex)은 발상이 신박하다. 각 "블록 범위"(기본 128 페이지)의 min·max만 인덱스로 저장한다. 인덱스 크기가 데이터 크기의 0.1%도 안 될 수 있다. B-tree가 데이터의 10%를 먹는다고 치면, 100배 차이다.

대신 BRIN은 데이터가 **자연 정렬돼 있을 때**만 빛난다. 시계열(시간 순서로 인서트되는 로그·이벤트), 자연 증가하는 시리얼 ID — 이런 데이터에서 BRIN은 거의 무료에 가까운 비용으로 큰 효과를 낸다. 반대로 무작위 분포 데이터에는 거의 도움이 안 된다. min·max 범위가 너무 넓어져서 모든 블록을 다 읽어야 하기 때문이다.

전형적인 쓰임은 이렇다. 일간 1억 건 들어오는 events 테이블, `created_at` 컬럼에 BRIN 인덱스. 인덱스가 수십 MB 수준이고, 시간 범위 조회가 빠르다. 만약 같은 컬럼에 B-tree를 걸었다면 인덱스 크기가 수 GB 수준이 됐을 것이다. 끔찍한 일이다.

23.5에서 다룰 파티셔닝과 BRIN은 자주 짝을 이룬다. monthly range partition + 각 파티션에 `created_at` BRIN — 시계열 운영의 정석 조합이다.

### 복합 인덱스의 컬럼 순서

여기서부터는 종류 선택을 넘어선 "어떻게 만들 것인가"의 영역이다. 복합 인덱스 — 여러 컬럼을 함께 인덱싱하는 — 의 컬럼 순서가 성능을 가른다.

`CREATE INDEX ON orders (user_id, status, created_at)`라는 인덱스가 있다고 해보자. 이 인덱스는 다음 쿼리들에 효과적이다.

- `WHERE user_id = 5` (왼쪽 한 컬럼만)
- `WHERE user_id = 5 AND status = 'paid'` (왼쪽 두 컬럼)
- `WHERE user_id = 5 AND status = 'paid' AND created_at > now() - interval '1 day'` (세 컬럼 모두)
- `WHERE user_id = 5 ORDER BY created_at DESC` — 정렬도 인덱스가 떠받친다

그런데 `WHERE status = 'paid'`만 있는 쿼리에는 거의 도움이 안 된다. `user_id`를 건너뛰고 `status`부터 검색하려면 인덱스 전체를 훑어야 하기 때문이다. 인덱스의 "왼쪽 prefix"만 효율적이라는 원칙을 기억해두자.

그렇다면 컬럼 순서를 어떻게 정할까? **선택도(selectivity)가 높은 컬럼을 앞에 두는 편이 낫다.** 예를 들어 `user_id`는 사용자가 1만 명이라면 한 값이 데이터의 0.01%를 골라낸다(고선택도). `status`가 paid/pending/cancelled 세 값뿐이라면 한 값이 33%를 골라낸다(저선택도). `user_id`를 앞에 두는 게 자연스럽다.

물론 늘 답이 깔끔한 건 아니다. "쿼리 패턴에 따라 다르다"는 게 정직한 답이다. 가장 자주 나오는 쿼리의 `WHERE` 절을 보고, 그 컬럼들을 왼쪽부터 채우는 식으로 시작하자. EXPLAIN으로 검증하고, 안 맞으면 다시 그리자.

### INCLUDE column — 인덱스 onlyscan을 위한 보태기

PG 11부터 추가된 기능이다. `CREATE INDEX ON orders (user_id) INCLUDE (total, status)` — `user_id`로 검색하고, 결과로 `total`과 `status`만 필요하다면, 이 인덱스 하나로 테이블에 손도 안 대고 답을 낼 수 있다. Index Only Scan이라고 부른다.

핵심은 `INCLUDE`로 묶인 컬럼은 인덱스의 leaf에 저장되지만 키로는 쓰이지 않는다는 점이다. 그래서 정렬·검색에는 영향을 안 주고, 인덱스 크기만 조금 늘리면서 cover index를 만들 수 있다.

OLTP에서 "특정 패턴의 SELECT가 핫하고, 그 결과 컬럼이 적다"면 INCLUDE가 강력한 처방이다. 다만 모든 컬럼을 INCLUDE에 욱여넣지는 말자. 그 순간 인덱스가 테이블만 해진다. 두세 컬럼, 핫한 쿼리에 정조준해서 쓰는 편이 낫다.

### Partial index — 데이터의 일부만 인덱싱하기

`CREATE INDEX ON orders (created_at) WHERE status = 'pending'` — 이런 식이다. 전체 행이 아니라 술어를 만족하는 행만 인덱싱한다.

이게 왜 강력한가? 주문 테이블에 1억 건이 있고, 그중 처리 대기 중인 `pending` 상태가 1만 건이라고 해보자. "오래된 pending 주문을 빨리 찾고 싶다"면 전체 1억 건을 인덱싱한 B-tree보다, `pending`만 골라 인덱싱한 partial index가 훨씬 작고 빠르다. 인덱스 크기가 1억분의 1만 수준이 된다.

전형적인 활용은 (1) soft delete 패턴 — `WHERE deleted_at IS NULL`만 인덱싱, (2) 작업 큐 — `WHERE status = 'pending'`만 인덱싱, (3) 활성 사용자만 — `WHERE last_login_at > now() - interval '30 days'`. 13장에서 이벤트 큐 패턴을 봤다면, partial index가 그 패턴의 숨은 동력이다.

여기서 한 가지 매트릭스로 정리해보자.

| 데이터 모양 / 쿼리 | 첫 선택지 | 비고 |
|---|---|---|
| equality, 범위, 정렬, NULL | **B-tree** | 의심스러우면 일단 이것 |
| equality only + 매우 긴 키 | Hash | 거의 안 쓴다, B-tree로도 충분 |
| 배열, JSONB, 전문검색 | **GIN** | 갱신 무거움 주의 |
| 공간, 범위 타입, KNN | **GiST** | PostGIS의 기본 |
| trie, IP, prefix, 비균형 GIS | SP-GiST | 평범한 OLTP에는 안 씀 |
| 자연 정렬된 거대 테이블(시계열) | **BRIN** | 인덱스 크기 1/100 |
| cover index(테이블 접근 제거) | B-tree + **INCLUDE** | 핫한 SELECT 정조준 |
| 데이터의 일부만 자주 조회 | **Partial index** | 큐·soft delete·활성만 |

선택지가 많아 보이지만, 정작 일상적으로 만지는 건 B-tree, GIN, BRIN, partial index 네 개다. 나머지는 알아두고, 필요할 때 꺼내자.

## 23.2 EXPLAIN ANALYZE 읽기

인덱스를 적절히 깔았는데도 쿼리가 느리다면, 그다음 펼칠 도구는 `EXPLAIN ANALYZE`다. 정확히는 `EXPLAIN (ANALYZE, BUFFERS, SETTINGS)`를 펼치자. 단순 `EXPLAIN`은 옵티마이저의 추정만 보여주고, `ANALYZE`를 붙여야 실제 실행 시간이 같이 나온다.

```sql
EXPLAIN (ANALYZE, BUFFERS, SETTINGS, VERBOSE)
SELECT * FROM orders
WHERE user_id = 12345 AND created_at > now() - interval '30 days'
ORDER BY created_at DESC LIMIT 20;
```

출력은 트리 구조다. 안쪽(들여쓰기 깊은 쪽)이 먼저 실행되고, 바깥쪽으로 결과가 흘러간다. 익숙해지면 한눈에 읽히지만, 처음 보면 난감하다. 그러니 어디부터 봐야 하는지 순서를 잡아두자.

### 첫째, estimate vs actual의 갭

각 노드에는 `rows=...`가 두 번 나온다. 앞은 옵티마이저가 추정한 rows, 뒤는 실제 rows다.

```
Index Scan using orders_user_id_idx on orders
  (cost=0.42..8.44 rows=10 width=44)
  (actual time=0.024..0.045 rows=8 loops=1)
```

추정 10, 실제 8 — 이건 거의 일치한다. 옵티마이저가 잘 본 거다. 그런데 만약 `rows=10`인데 `actual rows=50000`이라고 해보자. 5천 배 갭이다. 옵티마이저가 "이 결과는 작을 거야"라고 보고 nested loop 같은 작은 결과셋용 플랜을 골랐을 텐데, 실제로는 5만 건이 나오니 그 플랜이 처참하게 느려진다.

이 갭의 원인은 거의 항상 **통계가 부정확하다**는 것이다. 처방은 세 단계다. (1) 우선 `ANALYZE 테이블명;`을 실행한다. 통계 재수집이다. (2) 그래도 갭이 크면 `ALTER TABLE 테이블명 ALTER COLUMN 컬럼명 SET STATISTICS 1000;`으로 컬럼별 통계 정밀도를 올린다(기본 100, 최대 10000). (3) 컬럼 간 상관관계가 원인이라면 `CREATE STATISTICS`로 다중 컬럼 통계를 만들자. 예를 들어 도시와 우편번호처럼 함께 움직이는 컬럼들.

### 둘째, Gather / Gather Merge의 유무

쿼리가 큰 테이블 스캔을 동반한다면 병렬 쿼리가 작동하는지 봐야 한다. 플랜에 `Gather`나 `Gather Merge` 노드가 보이면 병렬이 켜진 것이고, 안 보이면 직렬 실행이다. 23.4에서 더 들어가지만, 여기서는 "병렬 가동 여부는 EXPLAIN에서 한 번에 보인다"는 사실만 기억해두자.

병렬이 작동해야 하는 쿼리인데 안 보인다면 의심할 점은 두 가지다. `max_parallel_workers_per_gather`가 0이거나, 쿼리에 parallel-unsafe 함수가 끼어 있다. 후자는 EXPLAIN VERBOSE로 어떤 함수인지 같이 볼 수 있다.

### 셋째, Buffers — 캐시 효율의 진실

`BUFFERS` 옵션을 켜면 각 노드에 다음과 같이 나온다.

```
Buffers: shared hit=120 read=8 dirtied=2
```

- `shared hit` — shared_buffers에서 바로 찾은 페이지 수(빠름)
- `shared read` — 디스크(또는 OS page cache)에서 읽어온 페이지 수(느림)
- `dirtied` — 이 노드가 더럽힌 페이지 수(checkpoint 부담)

비율이 의미를 갖는다. `hit/(hit+read)`가 95% 이상이면 캐시 효율이 좋다. 60% 이하면 shared_buffers가 부족하거나, 워킹셋이 너무 크거나, 어쩌면 한 쿼리에서 너무 많은 페이지를 읽고 있다.

여기서 함정 하나를 짚어두자. 같은 쿼리를 두 번 EXPLAIN ANALYZE 돌리면 두 번째는 거의 hit이 된다. 이미 캐시에 올라와 있기 때문이다. 그래서 실험할 때는 "cold(첫 실행)와 warm(두 번째 이후)을 모두 보고 비교"하는 편이 낫다. 운영 환경의 진짜 모습은 둘 사이 어딘가다.

### 넷째, SETTINGS — 환경 차이의 추적

`SETTINGS` 옵션은 PG 12부터 추가됐다. 출력 맨 아래에 "기본값과 다른 설정"이 함께 찍힌다.

```
Settings: work_mem = '512MB', random_page_cost = '1.1'
```

이게 왜 중요할까? "스테이징에선 빠른데 프로덕션에선 느리다"는 흔한 문제의 절반이 환경 차이다. SETTINGS를 켜두면 EXPLAIN 출력 한 장만 봐도 "어 여기 work_mem이 다르네"가 잡힌다. 디버깅에서 한참 헤맬 일을 한 줄로 줄여준다. 늘 같이 켜두자.

### 시각화 도구 — explain.depesz.com과 pev2

긴 EXPLAIN 출력을 텍스트로만 읽으면 눈이 빠진다. 두 도구를 알아두자.

**explain.depesz.com**은 Hubert "depesz" Lubaczewski가 만든 웹 도구다. EXPLAIN 출력을 붙여넣으면, 각 노드의 cost·시간·rows 비율을 색으로 표시해준다. 빨간색이 짙은 노드가 병목이다. 한눈에 "여기서 시간을 잡아먹고 있다"가 보인다. 운영 중인 시스템의 EXPLAIN을 외부로 붙여넣어도 되는지는 회사 정책 확인이 필요하지만, 익명화된 쿼리나 개발 환경에서는 매우 유용하다.

**pev2(PostgreSQL Explain Visualizer 2)**는 트리 구조를 인터랙티브한 다이어그램으로 보여주는 도구다. 로컬에서 돌릴 수 있어 사내 정책상 외부 업로드가 어려울 때 적합하다. JetBrains DataGrip이나 DBeaver에도 비슷한 시각화가 내장돼 있어 편의에 따라 고르면 된다.

도구가 분석을 대신해주지는 않는다. 다만 긴 텍스트에서 병목을 찾는 시간을 크게 줄여준다. 그 시간을 가설 세우고 처방하는 데 쓰는 편이 낫다.

### 노드 종류 — 세 가지만 일단

EXPLAIN의 모든 노드 종류를 외울 필요는 없다. 자주 마주치는 셋만 짚자.

**Seq Scan**(순차 스캔)은 테이블 전체를 처음부터 끝까지 읽는다. 작은 테이블이라면 이게 인덱스 스캔보다 빠를 수 있다. 옵티마이저가 그렇게 판단해서 골랐다면 비난할 일이 아니다. 다만 큰 테이블에 Seq Scan이 보이고 쿼리가 느리다면, 인덱스가 없거나 인덱스가 무력화된 상황이다. 무력화는 23.3에서 자세히.

**Index Scan**은 인덱스를 타고 들어가서 테이블에서 행을 읽어온다. **Index Only Scan**은 한 발 더 가서 테이블도 건드리지 않는다. INCLUDE column이나 visibility map 덕에 가능해진다. 후자가 보이면 잘 깔린 쿼리다.

**Nested Loop / Hash Join / Merge Join**은 조인 알고리즘이다. Nested Loop은 한쪽이 작을 때, Hash Join은 양쪽이 클 때, Merge Join은 양쪽이 정렬돼 있을 때 유리하다. 옵티마이저가 통계를 보고 고르는데, 통계가 어긋나면 잘못된 알고리즘을 고른다. 다시 estimate vs actual 갭의 이야기로 돌아온다.

이 정도가 EXPLAIN의 첫걸음이다. 깊이는 더 있지만, 거기까지 가기 전에 절반의 문제는 흔한 함정 여섯 가지에서 잡힌다. 그쪽을 먼저 보자.

## 23.3 흔한 함정 여섯 가지

PostgreSQL 운영에서 "쿼리가 느리다"의 80%는 사실 새로운 인덱스가 필요해서가 아니라, 이미 있는 인덱스가 무력화돼서다. 누가 일부러 그런 게 아니다. 코드 한 줄, 타입 하나, 설정 하나가 인덱스를 못 쓰게 만든다. 자주 마주치는 여섯 가지를 짚어두자. 이 여섯 가지만 머리에 박혀 있어도 야간에 호출당하는 횟수가 줄어든다.

### 함정 1. 함수로 감싸서 인덱스 무력화

```sql
-- 잘못된 쿼리
SELECT * FROM users WHERE lower(email) = 'toby@example.com';
```

`email` 컬럼에 B-tree 인덱스를 깔아뒀어도, 이 쿼리는 인덱스를 못 탄다. 왜일까? 인덱스는 `email`의 값을 정렬해서 들고 있는데, 쿼리에서 묻는 건 `lower(email)`이다. 인덱스 입장에서는 "내가 가진 값이 아니야"라는 답이 나온다. 결과는 Seq Scan, 그리고 느린 쿼리.

처방은 두 가지다. (1) **표현식 인덱스**(expression index)를 만든다 — `CREATE INDEX ON users (lower(email))`. 이러면 인덱스가 미리 lower한 값을 들고 있어서 쿼리가 그대로 인덱스를 탄다. (2) 또는 쿼리를 바꿔서 함수를 안 쓴다 — 입력 단계에서 이메일을 소문자로 정규화해 저장하는 식이다. 어느 쪽이든 좋다.

이 함정은 시간 함수에서도 자주 일어난다. `WHERE date_trunc('day', created_at) = '2026-05-18'` 같은 쿼리도 마찬가지다. `created_at`에 인덱스가 있어도 못 탄다. 처방은 술어를 바꾸는 것 — `WHERE created_at >= '2026-05-18' AND created_at < '2026-05-19'`. 같은 의미인데 인덱스를 탄다. 늘 그렇듯, 인덱스가 "있는 그대로의 값"으로 비교받게 해주는 편이 낫다.

### 함정 2. 암시적 캐스트

```sql
-- varchar 컬럼인 phone에 정수로 비교
SELECT * FROM users WHERE phone = 821012345678;
```

`phone`이 `varchar`인데 우변이 `bigint`다. PostgreSQL은 양쪽 타입이 다르면 한쪽을 캐스트하는데, 이 경우 컬럼 쪽을 캐스트한다(`phone::bigint = 821012345678`). 그러면 결과적으로 좌변이 함수로 감싸진 모양이 되고, 인덱스가 무력화된다. 함정 1과 사실상 같은 원리다.

이 함정의 무서움은 "쿼리만 보면 정상으로 보인다"는 점이다. 코드 리뷰에서 잡기 어렵다. ORM이 잘못된 타입을 박아 보내는 경우가 흔한데, 운영 환경에서 갑자기 한 쿼리가 느려져서 한참 뒤에 발견된다. 처방은 (1) 우변 타입을 컬럼에 맞춰 명시적으로 캐스트 — `WHERE phone = '821012345678'`, (2) 또는 ORM 레이어에서 타입을 정확히 박아 보내도록 수정.

찜찜한 일이지만, 한 번 잡히면 같은 버그를 다시 만들지는 않는다. 새 코드 리뷰할 때 의심 한 번씩 해보자.

### 함정 3. OR 조건의 인덱스 선택

```sql
SELECT * FROM orders
WHERE user_id = 5 OR coupon_code = 'WELCOME';
```

`user_id`에 인덱스가 있고, `coupon_code`에도 인덱스가 있다. 둘 다 잘 작동한다. 그런데 OR로 묶이면 옵티마이저가 BitmapOr 같은 기법으로 처리하기도 하지만, 통계가 어긋나면 그냥 Seq Scan으로 떨어진다. AND였다면 한 인덱스만 써도 되니까 깔끔한데, OR는 양쪽 인덱스를 다 써야 한다.

처방으로 자주 쓰는 게 **UNION**으로 풀어쓰기다.

```sql
SELECT * FROM orders WHERE user_id = 5
UNION
SELECT * FROM orders WHERE coupon_code = 'WELCOME';
```

이러면 각 가지가 자기 인덱스를 깔끔하게 탄다. 단, 양쪽에 같은 행이 나올 수 있다면 UNION(중복 제거)을, 그렇지 않다면 UNION ALL을 쓰자. UNION ALL이 정렬·중복 제거가 없어 더 빠르다.

OR가 무조건 나쁜 건 아니다. 옵티마이저가 BitmapOr로 잘 처리하는 경우도 많다. EXPLAIN을 보고 안 풀리면 그때 UNION으로 풀어쓰는 편이 낫다.

### 함정 4. LIKE의 leading wildcard

```sql
SELECT * FROM products WHERE name LIKE '%phone%';
```

`name`에 B-tree 인덱스가 있어도 못 탄다. B-tree 인덱스는 prefix 검색에 강한데, 앞에 `%`가 붙으면 prefix가 없는 셈이다. 만약 `LIKE 'phone%'`였다면 인덱스를 탔을 거다.

처방은 두 갈래다.

(1) **앞에 wildcard가 꼭 필요한가**를 한 번 더 묻자. 전화기 모델명을 찾을 때 사용자가 'iphone'을 칠 거라면 prefix만으로 충분하다. UX가 끌어가는 결정이긴 한데, prefix only로 풀 수 있다면 그게 가장 깔끔하다.

(2) **앞에 wildcard가 정말 필요하다면 pg_trgm 익스텐션**을 켜자. 트라이그램 기반 GIN 인덱스를 만들면 `LIKE '%phone%'`이 인덱스를 탄다.

```sql
CREATE EXTENSION pg_trgm;
CREATE INDEX products_name_trgm ON products USING GIN (name gin_trgm_ops);
```

3.3에서 전문 검색 이야기를 했다면, pg_trgm은 그 가벼운 버전이다. tsvector + GIN이 본격적 전문 검색이라면, pg_trgm은 LIKE 가속이다. 한국어처럼 morpheme 분석이 필요한 텍스트엔 한계가 있지만, 영문 부분 매칭에는 충분하다.

### 함정 5. 통계 미수집

```sql
-- 어제 야간에 ETL로 100만 건을 새로 적재했다고 해보자
INSERT INTO events SELECT ... FROM staging.events_2026_05_18;
-- 그리고 다음 쿼리가 갑자기 느려졌다
SELECT * FROM events WHERE event_type = 'click' AND created_at > now() - interval '1 hour';
```

문제는 통계가 새 데이터를 반영하지 못한 것이다. autovacuum이 통계를 다시 모으긴 하지만, 임계치(`autovacuum_analyze_scale_factor` 기본 0.1, 즉 10% 변경)를 넘어야 동작한다. 대량 적재 직후엔 그 임계를 지나도 아직 작업이 안 끝났을 수 있다.

옵티마이저는 "events 테이블에 어제까지 1만 건 있었다"는 통계로 플랜을 짠다. 그래서 작은 결과셋을 가정한 nested loop를 골랐는데, 실제 데이터는 100만 건이 됐다. 결과는 처참한 느려짐이다.

처방은 단순하다. **대량 적재나 대량 변경 직후엔 `ANALYZE`를 명시적으로 실행하자.**

```sql
ANALYZE events;
```

ETL 파이프라인의 마지막 스텝으로 박아두는 편이 낫다. 18장에서 vacuum 운영 이야기를 자세히 했지만, 통계는 vacuum과 별개의 운영 책임이다. 잊지 말자.

### 함정 6. max_connections 과대 설정

이건 쿼리 차원이 아니라 클러스터 설정 차원의 함정이다. 그런데 "쿼리가 느리다"의 원인이 자주 여기 있다.

4장에서 fork 모델을 다뤘다. PostgreSQL은 연결 하나당 OS 프로세스 하나를 띄운다. 그래서 `max_connections = 2000` 같은 설정은 "2천 개의 프로세스를 띄울 수 있게 한다"는 뜻이다. 각 프로세스는 work_mem(기본 4MB, 운영에서 64MB~256MB로 올리는 경우 많음)을 정렬·해시 작업마다 따로 잡고, 백엔드 자체도 수 MB의 메모리를 쓴다. 산수해보면 무서워진다. 2000 × 64MB = 128GB. work_mem만 가지고 시스템 메모리가 다 날아간다.

증상은 잠복형이다. 평소엔 멀쩡하다가 트래픽이 몰리면 갑자기 메모리 폭주, OOM Killer 발동, 모든 백엔드가 종료된다. 또는 OS 스케줄러가 2천 개 프로세스를 컨텍스트 스위칭하느라 CPU를 다 까먹는다. 야간에 호출당하는 사고의 단골이다.

처방은 두 가지로 정리된다. (1) **`max_connections`를 무리해서 키우지 말자.** 코어 수와 워킹셋을 보고 500 안쪽으로 잡는 게 일반적이다. 정확한 수치는 워크로드별로 다르지만, 4000 같은 숫자는 거의 항상 잘못된 답이다. (2) **앱과 DB 사이에 풀러를 둔다.** PgBouncer transaction pool 모드로 앱 측 1만 커넥션을 DB 측 100 커넥션으로 줄이는 게 정석이다. 21장에서 PgBouncer·Pgcat·Odyssey의 도구 선택을 자세히 다뤘으니 거기를 참조하자.

이 여섯 가지를 한 번 정리하자.

| 함정 | 증상 | 처방 |
|---|---|---|
| 1. 함수로 감싸기 | 인덱스 안 탐 | 표현식 인덱스 또는 쿼리 재작성 |
| 2. 암시적 캐스트 | 인덱스 안 탐 | 우변 타입 맞추기 |
| 3. OR 조건 | BitmapOr 실패 → Seq Scan | UNION으로 풀어쓰기 |
| 4. LIKE leading % | B-tree 무력 | pg_trgm + GIN |
| 5. 통계 미수집 | estimate vs actual 갭 | 대량 변경 후 ANALYZE |
| 6. max_connections 과대 | OOM, 컨텍스트 스위치 | 줄이고 풀러 도입 |

한 번 더 강조하자. **느린 쿼리가 등장하면 새 인덱스를 만들기 전에 이 여섯 가지부터 의심하자.** 이미 있는 인덱스가 일을 안 하고 있는 경우가 훨씬 흔하다.

## 23.4 Parallel query

여기서부터는 단일 쿼리의 한계를 넘어서는 영역이다. PG 9.6부터 parallel query가 들어왔고, 버전이 올라갈수록 적용 범위가 넓어졌다. v17부터는 일부 인덱스 쿼리도 병렬화가 개선됐다.

원리는 단순하다. 큰 테이블 스캔이나 집계가 들어오면, PostgreSQL이 worker 프로세스를 여러 개 띄워서 일을 나눠 한다. 마지막에 leader가 결과를 모은다(Gather). 8코어 CPU에서 4 worker가 일하면 단순 계산으로 4배 빨라질 수 있다. 실제로는 그만큼은 안 나오지만, 큰 분석 쿼리에선 2~3배 향상이 흔하다.

### 켜기 — 설정 세 가지

병렬 쿼리는 기본으로 켜져 있다. 다만 worker 수와 임계값이 보수적으로 잡혀 있어서 작은 쿼리는 직렬로 도는 경우가 많다.

```
max_worker_processes = 8           -- 전체 background worker 한도
max_parallel_workers = 8           -- 그중 parallel 전용
max_parallel_workers_per_gather = 2 -- 한 쿼리당 최대 worker 수
```

`max_parallel_workers_per_gather`가 핵심이다. 기본 2를 4나 8로 올리면 큰 쿼리가 더 많은 worker를 쓸 수 있다. 다만 OLTP에서 모든 쿼리가 병렬을 쓰면 컨텍스트 스위치만 폭증한다. **분석 쿼리가 도는 세션에만 SET LOCAL로 올리거나, 분석 전용 리플리카에서만 올리는 편이 낫다.**

`min_parallel_table_scan_size`(기본 8MB)와 `min_parallel_index_scan_size`(기본 512KB)는 "이 크기 이하 테이블/인덱스는 병렬화 안 함"의 임계다. 작은 테이블 병렬화는 오버헤드가 더 크다는 판단인데, 워크로드에 따라 조정 여지가 있다.

### Parallel-safe 함수

병렬 쿼리에 걸림돌이 되는 게 함수의 parallel safety다. PostgreSQL 함수는 세 등급으로 표시된다.

- **PARALLEL SAFE** — 안전하게 worker에서 실행 가능. 대부분의 순수 함수.
- **PARALLEL RESTRICTED** — leader에서만 실행. 시퀀스 사용·임시 테이블 접근 등.
- **PARALLEL UNSAFE** — 병렬 자체가 불가. 데이터를 변경하는 함수, 부작용 있는 함수.

흔한 함정이 사용자 정의 함수에 표시를 안 해서 디폴트 `PARALLEL UNSAFE`가 되는 것이다. 결과적으로 그 함수가 쿼리에 끼면 병렬화가 통째로 꺼진다.

```sql
CREATE FUNCTION normalize_phone(text) RETURNS text AS $$
  SELECT regexp_replace($1, '[^0-9]', '', 'g');
$$ LANGUAGE SQL IMMUTABLE PARALLEL SAFE;
```

`PARALLEL SAFE`를 명시해두자. 함수에 사이드 이펙트가 없다면 거의 항상 SAFE다. 잊지 말자.

### EXPLAIN VERBOSE로 확인

병렬이 안 켜지는데 이유를 모르겠다면 `EXPLAIN (ANALYZE, VERBOSE)`를 보자. VERBOSE는 어떤 함수가 어떤 등급인지, 왜 worker가 0인지를 더 자세히 보여준다.

```
Gather  (cost=1000.00..15234.50 rows=5000 width=64) (actual rows=4823 loops=1)
  Workers Planned: 4
  Workers Launched: 4
  ->  Parallel Seq Scan on orders ...
```

`Workers Planned: 4 / Launched: 4`면 정상. `Launched: 0`이면 worker가 부족했다는 뜻 — `max_parallel_workers`나 시스템 부하를 의심하자. `Workers Planned: 0`이면 옵티마이저가 처음부터 병렬을 고려조차 안 했다는 뜻 — 임계값(`min_parallel_table_scan_size`)이나 함수 안전 등급을 다시 보자.

### 어떤 쿼리가 병렬에 잘 맞는가

평이한 OLTP 점 조회 — `SELECT * FROM users WHERE id = 5` — 같은 쿼리는 병렬과 무관하다. 결과가 한 행인데 worker를 띄울 이유가 없다.

병렬의 진가는 **(1) 큰 테이블의 집계, (2) 큰 테이블 간 조인, (3) 큰 결과셋의 정렬**에서 나온다. 분석 워크로드, 리포트 생성, ETL의 큰 집계 단계 — 이런 데서 4배·8배의 향상이 실제로 일어난다.

3.8에서 분석 워크로드 이야기를 했다면, parallel query는 그 워크로드의 기본 동력이다. 시간당 1억 건 들어오는 로그에서 일간 집계를 5분 안에 뽑아야 한다면, 직렬로는 불가능한 일이 병렬로는 가능해진다.

## 23.5 Partitioning과 pg_partman

테이블이 1억 건을 넘어가면 단일 테이블의 운영 부담이 슬슬 무거워진다. 인덱스 빌드 시간이 시간 단위로 길어지고, vacuum이 한 번 돌면 몇 시간이 걸리고, 디스크 회수도 어려워진다. 이때 답으로 등장하는 게 파티셔닝이다.

### Declarative partitioning — PG 10 이후의 표준

PG 10 이전엔 파티셔닝을 trigger와 상속으로 흉내 내야 했다. 코드가 지저분하고 운영이 까다로웠다. PG 10부터 **declarative partitioning**이 들어와서 SQL로 자연스럽게 표현된다.

```sql
CREATE TABLE events (
  id BIGSERIAL,
  created_at TIMESTAMPTZ NOT NULL,
  event_type TEXT,
  payload JSONB
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_05 PARTITION OF events
  FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
CREATE TABLE events_2026_06 PARTITION OF events
  FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
```

세 종류 — Range(범위, 시간 등), List(목록, 지역·상태 등), Hash(균등 분산) — 가 있다. 가장 흔한 게 시계열 데이터의 Range 파티셔닝이다.

### Partition pruning — 파티셔닝의 진짜 효용

파티셔닝의 진짜 효용은 디스크를 나눈 것보다 **쿼리 시 필요한 파티션만 읽는다**는 점에 있다. PostgreSQL이 술어를 보고 "이 쿼리는 events_2026_05만 보면 된다"고 판단해서 다른 파티션은 건드리지도 않는다. 이걸 partition pruning이라고 부른다.

```sql
SELECT count(*) FROM events
WHERE created_at >= '2026-05-15' AND created_at < '2026-05-16';
```

이 쿼리는 events_2026_05 파티션만 본다. 다른 파티션은 무시된다. 1억 건 테이블이 효과적으로 300만 건 테이블처럼 동작한다.

EXPLAIN으로 확인할 수 있다.

```
Append  (cost=...)
  ->  Seq Scan on events_2026_05 events_1
        Filter: (created_at >= ... AND created_at < ...)
```

다른 파티션 이름이 안 나오면 pruning이 잘 작동한 것이다. 만약 모든 파티션이 다 나오면, 술어가 파티션 키와 정확히 안 맞거나 함수로 감싸진 상태일 가능성이 크다(함정 1을 떠올리자).

v17부터는 partition pruning이 더 다양한 술어 모양에서 작동하도록 개선됐다. 특히 IN 절·OR 절에서의 pruning이 좋아졌다.

### pg_partman 5.x — 파티션 운영의 자동화

declarative partitioning은 좋은데, 매달 다음 달 파티션을 누가 만들 것인가? 매년 오래된 파티션을 누가 지울 것인가? 사람이 cron으로 할 수도 있지만, 그건 잊어버리기 좋은 일이다.

**pg_partman**이 그 자동화를 대신한다. 5.x 버전부터는 trigger 방식을 완전히 버리고 declarative partitioning만 지원한다. 더 깔끔해졌다.

```sql
CREATE EXTENSION pg_partman;

SELECT partman.create_parent(
  p_parent_table => 'public.events',
  p_control => 'created_at',
  p_type => 'native',
  p_interval => '1 month',
  p_premake => 4
);
```

`p_premake => 4`는 "미리 4개월 치 파티션을 만들어둔다"는 뜻이다. 그리고 pg_partman의 background worker가 주기적으로 깨어나서 새 파티션을 만들고, retention 정책에 따라 오래된 파티션을 떼어내거나 삭제한다.

```sql
UPDATE partman.part_config
SET retention = '12 months',
    retention_keep_table = false
WHERE parent_table = 'public.events';
```

12개월 지난 파티션은 자동으로 삭제. 외부 cron 없이, BGW가 알아서 돈다. RDS for PostgreSQL도 공식 지원하니 매니지드 환경에서도 그대로 쓸 수 있다.

### 시계열 + BRIN + pg_partman의 황금 조합

23.1 마지막에 슬쩍 언급했던 그 조합이 여기서 완성된다.

```sql
-- monthly range partition
CREATE TABLE events (...) PARTITION BY RANGE (created_at);

-- 각 파티션에 BRIN
CREATE INDEX ON events_2026_05 USING BRIN (created_at);

-- pg_partman으로 자동 생성·삭제
SELECT partman.create_parent('public.events', 'created_at', 'native', '1 month', p_premake => 4);
```

세 가지가 합쳐서 만드는 결과는 이렇다. (1) 파티셔닝으로 쿼리는 한 달 치 데이터만 본다. (2) BRIN으로 인덱스는 거의 무료 수준의 크기다. (3) pg_partman으로 운영은 자동이다. 시계열 1억 건 / 일 같은 워크로드를 한두 사람이 운영할 수 있게 만드는 정석 조합이다.

### Native vs declarative — 이름이 헷갈리는 이유

"native partitioning"이라는 말과 "declarative partitioning"이라는 말이 같이 돌아다닌다. 같은 걸 가리키는 두 이름이다. PG 10 이후의 빌트인 파티셔닝을 말한다. 반대편에 trigger·inheritance 기반의 옛 방식이 있었고, pg_partman은 옛날엔 그쪽도 지원했다. 5.x부터는 native(=declarative)만 남았다.

새 시스템 설계라면 declarative만 생각하면 된다. 옛 코드베이스 마이그레이션이라면, trigger 방식의 흔적을 declarative로 옮기는 작업이 필요할 수 있다. 17장에서 마이그레이션 패턴을 봤다면, 그 일환이다.

### 파티셔닝의 함정 — 외래키와 UNIQUE 제약

파티셔닝이 만능은 아니다. 두 가지 제약을 미리 알아두자.

(1) **외래키가 파티션된 테이블을 참조하는 게 PG 12까지 불가능했다.** PG 12부터 가능해졌지만, 여전히 미세한 제약이 남아 있다. 외래키가 많은 상호참조 모델이라면 파티셔닝이 깔끔하지 않을 수 있다.

(2) **UNIQUE 제약은 반드시 파티션 키를 포함해야 한다.** `UNIQUE (email)`을 events 테이블에 걸 수 없다. `UNIQUE (email, created_at)`처럼 파티션 키를 포함해야 한다. 이건 native partitioning의 구조적 한계다. 비즈니스 모델이 "이메일은 시스템 전체에서 유일하다"고 요구한다면, 그 테이블은 파티셔닝과 잘 안 맞는다.

이 두 제약 때문에 **모든 큰 테이블을 파티셔닝하는 게 답은 아니다.** 시계열·이벤트 로그·트랜잭션 이력처럼 자연스럽게 시간으로 갈라지고 외래키 의존이 적은 데이터가 파티셔닝의 단골이다. 사용자·상품처럼 외래키가 많이 들어오고 전역 UNIQUE가 필요한 마스터 데이터는 파티셔닝하지 않는 편이 낫다.

## 23.6 OS·하드웨어 레벨 체크리스트

여기까지는 PostgreSQL 안쪽 이야기였다. 그런데 PG는 결국 Linux 위에서 도는 프로세스다. 운영체제 레벨 설정이 어긋나 있으면, 아무리 인덱스를 잘 깔고 쿼리를 잘 짜도 성능이 안 나온다. DBA가 야간에 호출당하는 영역의 절반이 사실 이쪽이다. 여섯 항목을 짚어두자.

### 1. dirty_ratio와 dirty_background_ratio

Linux 커널은 디스크 쓰기를 메모리에 캐시해두고 background로 flush한다. 그 비율을 두 파라미터가 정한다.

- `vm.dirty_background_ratio` — 이 비율(기본 10%)을 넘으면 background flush 시작
- `vm.dirty_ratio` — 이 비율(기본 20%)을 넘으면 모든 쓰기가 멈추고 동기 flush

기본값이 DB 워크로드에 너무 크다. 메모리 256GB 머신에서 20%면 51GB 더티 데이터가 쌓일 수 있다는 뜻이다. 그러다가 임계를 넘으면 51GB 쓰기가 한 번에 일어나면서 시스템이 수십 초 멈춘다. 이게 흔히 말하는 "I/O 스파이크"다.

처방은 비율 대신 절대값으로 잡는 것이다.

```bash
sysctl -w vm.dirty_background_bytes=268435456    # 256MB
sysctl -w vm.dirty_bytes=536870912               # 512MB
```

`_bytes`를 설정하면 `_ratio`는 무시된다. 256MB·512MB가 만능 답은 아니다. 디스크 쓰기 처리량(MB/s)을 보고, 1~2초 안에 다 flush할 수 있는 크기로 잡는 게 원칙이다. NVMe 환경에선 더 크게, HDD 환경에선 더 작게.

### 2. Transparent Huge Pages — 끄자

THP(Transparent Huge Pages)는 2MB 단위로 페이지를 다루게 해주는 기능이다. 일부 워크로드에선 좋은데, **데이터베이스에는 거의 항상 해롭다.** 무작위 접근 패턴이 THP의 가정과 안 맞고, page fault 비용이 늘고, latency spike가 일어난다.

```bash
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag
```

부팅 시에도 적용되도록 `/etc/rc.local`이나 systemd unit에 박아두자. PostgreSQL 공식 권장이기도 하다.

대신 PG는 명시적 huge pages를 쓸 수 있다 — `huge_pages = try`(기본). 이건 다른 이야기다. THP는 끄고, explicit huge pages는 켜는 게 정석이다.

### 3. NUMA 정책

요즘 서버는 대부분 NUMA(Non-Uniform Memory Access)다. CPU 소켓이 둘 이상 있고, 각 소켓이 자기 로컬 메모리를 가진다. 다른 소켓의 메모리를 접근하면 느리다.

기본 정책에선 OS가 "메모리를 한 노드에 우선 할당"하는데, PG 같은 큰 단일 프로세스 그룹엔 안 맞을 수 있다. shared_buffers가 한 노드에 몰리고, 다른 노드의 백엔드가 그걸 원격으로 접근하면서 느려진다.

```bash
sysctl -w vm.zone_reclaim_mode=0
# 그리고 PG를 numactl로 interleave 모드로 실행
numactl --interleave=all postgres -D /data/pg
```

`vm.zone_reclaim_mode=0`이 핵심이다. 이걸 1로 두면 NUMA 노드가 채워질 때 cache를 회수하느라 I/O가 폭증한다. 의외로 옛 시스템에 1로 설정된 곳이 있다 — 확인해두자.

### 4. NVMe scheduler — none이 정답

I/O scheduler는 디스크 요청을 OS가 어떻게 정렬할지의 정책이다. SSD/NVMe 시대엔 OS가 끼어들지 않는 게 가장 빠르다.

```bash
echo none > /sys/block/nvme0n1/queue/scheduler
```

`none`(또는 옛 이름 `noop`)이 NVMe의 답이다. `cfq`·`deadline` 같은 HDD 시대 scheduler는 NVMe 성능을 깎는다. 부팅 시 적용되게 udev rule이나 systemd로 잡자.

### 5. swappiness — 1로 낮추자

`vm.swappiness`는 "OS가 메모리 회수 시 swap을 얼마나 좋아할지"의 0~100 척도다. 기본 60이 데스크톱엔 합리적인데, DB엔 너무 높다. shared_buffers가 swap으로 밀려나면 일이 끔찍해진다.

```bash
sysctl -w vm.swappiness=1
```

0이 아니라 1이다. 0은 swap을 완전히 금지하는데, OOM 위험이 있다. 1은 "정말 마지막 수단으로만 swap"을 의미한다. 안전한 절충이다.

### 6. 파일시스템 — ext4 vs xfs

ext4와 xfs 둘 다 PG에 잘 맞는다. **둘 사이 큰 성능 차이는 없다.** 다만 운영 특성에 미세한 차이가 있다.

- **ext4** — 작은 파일이 많을 때 안정적. journal 모드가 명료.
- **xfs** — 큰 파일·큰 디렉터리에 최적화. delete가 빠름. 대용량 DB에 많이 쓰임.

엔터프라이즈 PG 운영의 다수가 xfs를 쓴다. 이유는 (1) 큰 테이블(수십 GB 이상)에 강하고, (2) parallel I/O에 강하고, (3) RHEL 계열의 기본이라 잘 검증됐기 때문이다. 새로 까는 DB 서버라면 xfs로 시작하는 편이 무난하다.

마운트 옵션도 같이 짚어두자. **`noatime`을 켜자.** `atime`(access time) 업데이트는 모든 read마다 metadata write를 일으킨다. DB 워크로드에서 atime을 쓸 일이 거의 없으니 끄는 게 이득이다.

```bash
# /etc/fstab
/dev/nvme0n1p1 /data xfs defaults,noatime,nodiratime 0 0
```

이 여섯 항목을 한 표로 정리하자.

| 항목 | 권장 설정 | 이유 |
|---|---|---|
| dirty_background_bytes / dirty_bytes | 256MB / 512MB (NVMe 기준) | I/O spike 방지 |
| Transparent Huge Pages | never | latency spike |
| NUMA zone_reclaim_mode | 0 + interleave 실행 | 메모리 편중 회피 |
| NVMe scheduler | none | OS 큐가 NVMe엔 방해 |
| swappiness | 1 | shared_buffers swap 방지 |
| 파일시스템 | xfs, noatime | 대용량 친화 |

회사마다 표준이 있겠지만, 신규 PG 서버를 받았을 때 이 체크리스트를 한 번 돌리는 편이 낫다. 야간에 한 번이라도 호출받아본 사람은 이 표의 가치를 안다.

## 23.7 튜닝 의사결정 흐름도

이제 모든 조각을 한 흐름으로 합쳐보자. **느린 쿼리가 등장했을 때 어떤 순서로 진단하고 처방할 것인가** — 23장이 답하려던 한 질문이다.

이걸 한 페이지 흐름도로 옮겨두자.

### 1단계. 발견 — "느리다"의 정의부터

"느리다"는 주관이다. 어떤 쿼리가 평소 50ms인데 갑자기 500ms가 됐다면 10배 회귀다. 어떤 쿼리가 평소 5초인데 7초가 됐다면 마음에 안 들지만 사실 정상 변동일 수 있다. 정의 없이 튜닝하면 끝없는 작업이 된다.

**21장의 옵저버빌리티 도구**가 발견의 첫 자리다. `pg_stat_statements`로 "평균 실행 시간이 가장 긴 쿼리"나 "최근 24시간 동안 가장 많이 호출된 쿼리" 같은 view를 만들어두자. APM(DataDog·New Relic·Pinpoint 등)이 깔려 있다면 거기서 쿼리 단위 latency를 보자. Grafana 대시보드에서 p95/p99 latency를 추적하자.

핵심은 **"느리다"를 숫자로 정의**하는 것이다. "p95가 200ms를 넘으면 회귀로 본다" 같은 임계가 정해져야 진단이 시작된다.

### 2단계. 격리 — 한 쿼리에 집중

"DB 전체가 느리다"는 거의 항상 잘못된 가설이다. 진짜는 "한두 쿼리가 느리고, 그게 lock·풀·CPU를 점유해서 나머지가 같이 느려진다"인 경우가 압도적이다.

`pg_stat_activity`로 지금 도는 쿼리들을 보자. `state = 'active'`인 쿼리, `wait_event_type`이 `Lock`이거나 `IO`인 쿼리. 가장 오래 도는 쿼리부터 잡자. 18장에서 long-running transaction의 도미노 효과를 봤다면, 그 도미노의 머리를 잡는 작업이다.

격리에 성공하면 한 쿼리 텍스트가 손에 들어온다. 그게 3단계의 입력이다.

### 3단계. 진단 — EXPLAIN ANALYZE를 펼치자

```sql
EXPLAIN (ANALYZE, BUFFERS, SETTINGS, VERBOSE)
[문제의 쿼리];
```

23.2에서 본 네 가지를 본다. (1) estimate vs actual 갭, (2) Gather 노드 유무, (3) Buffers 비율, (4) SETTINGS 차이. 출력이 길면 explain.depesz.com에 붙여서 색으로 보자.

진단의 출구는 셋 중 하나다.

- (a) **인덱스가 무력화돼 있다** — Seq Scan이 큰 테이블에 보이고, WHERE 절에 함수·캐스트·OR·leading wildcard가 끼어 있다. → 23.3의 함정 여섯 가지 처방
- (b) **통계가 어긋나 있다** — estimate vs actual 갭이 100배 이상. → ANALYZE 또는 statistics target 상향
- (c) **쿼리 자체가 큰 결과셋을 요구한다** — 100만 행 집계 같은 쿼리. → 23.4의 parallel query 또는 23.5의 partitioning

### 4단계. 원리로 해석 — 5·6장으로 거슬러 올라가기

처방을 내기 전에, 왜 그 일이 일어났는지를 원리 차원에서 한 번 짚자. 그래야 같은 문제가 다시 안 일어난다.

- 인덱스가 무력화됐다면, 그건 6장의 HOT 이야기와 자주 만난다. 인덱스 컬럼을 자주 갱신하면 HOT이 깨지고, 그래서 인덱스가 비대해지고, 그래서 효율이 떨어진다.
- 통계가 어긋났다면, 그건 5장의 MVCC 이야기와 만난다. autovacuum이 통계까지 수집하지만, dead tuple이 많이 쌓이면 분석이 부정확해진다.
- 쿼리가 큰 결과셋을 요구한다면, 그건 데이터 모델 자체의 질문이다. 16장에서 보낸 인사이트 — RLS·view·CTE로 결과셋을 모델 레벨에서 줄일 수 있는지 — 를 떠올리자.

### 5단계. 처방 — 가장 가벼운 것부터

처방의 우선순위는 이 순서가 좋다.

1. **쿼리 재작성** — 함수 안 감싸기, 캐스트 정리, OR를 UNION으로. 코드 변경 없이 즉시 적용 가능.
2. **통계 재수집** — `ANALYZE 테이블명`. 30초 안에 끝나는 일이 5초 쿼리를 50ms로 만들기도 한다.
3. **인덱스 추가/조정** — 표현식 인덱스, INCLUDE, partial. 디스크와 갱신 비용이 따라온다.
4. **설정 조정** — work_mem, parallel_workers_per_gather, statistics_target. 세션 단위로 먼저 검증.
5. **구조 변경** — 파티셔닝, 비정규화, 캐시 계층 추가. 가장 비싸고 가장 늦게.

위에서 아래로 갈수록 비용이 크다. **가벼운 처방으로 끝낼 수 있다면 거기서 멈추자.** 한 사람의 시간으로는 가장 비싼 처방이 가장 화려해 보이지만, 운영의 무게로는 가벼운 처방이 가장 단단하다.

### 6단계. 검증과 모니터링

처방을 적용했으면, 같은 EXPLAIN을 다시 떠서 비교하자. 추정 시간이 줄었는지, 실제 시간이 줄었는지, Buffers 비율이 좋아졌는지. 그리고 21장의 옵저버빌리티 도구로 **다음 며칠** 동안 그 쿼리의 latency를 추적하자. 처방이 다른 쿼리를 느리게 만들지 않았는지도 봐야 한다.

새로 만든 인덱스가 실제로 쓰이는지 `pg_stat_user_indexes.idx_scan` 카운터로 확인하자. 6개월 뒤에 안 쓰이는 인덱스가 있다면 떼어내자. 인덱스도 자산이지만 부채다.

### 한 페이지 흐름도

```
[느린 쿼리 알람]
        │
        ▼
1. 발견 ─── pg_stat_statements / APM / Grafana
   "느리다"를 숫자로 정의 (p95 200ms 등)
        │
        ▼
2. 격리 ─── pg_stat_activity 로 한 쿼리 잡기
   long-running tx, lock, IO wait 확인
        │
        ▼
3. 진단 ─── EXPLAIN (ANALYZE, BUFFERS, SETTINGS, VERBOSE)
   ├─ estimate vs actual 갭?
   ├─ Gather 노드 유무?
   ├─ Buffers shared hit 비율?
   └─ 시각화: explain.depesz.com / pev2
        │
        ▼
4. 원리 해석 ─── 왜 일어났는가
   ├─ 인덱스 무력화 → 6장 HOT, 23.3 함정
   ├─ 통계 어긋남  → 5장 MVCC, vacuum/analyze
   └─ 큰 결과셋   → 16장 데이터 모델, 13장 패턴
        │
        ▼
5. 처방 ─── 가벼운 것부터
   1) 쿼리 재작성 → 2) ANALYZE → 3) 인덱스
   4) 설정 → 5) 파티셔닝/구조 변경
        │
        ▼
6. 검증 ─── EXPLAIN 재실행 + 며칠 모니터링
   pg_stat_user_indexes 로 새 인덱스 사용 확인
```

이 흐름도가 23장에서 얻어야 할 한 페이지짜리 결론이다. 인쇄해서 모니터 옆에 붙여도 좋다.

## 마무리

23장은 새 지식의 챕터가 아니라 **조립의 챕터**였다. 6종류 인덱스의 선택, EXPLAIN 네 가지 관전 포인트, 흔한 함정 여섯, parallel query, partitioning과 pg_partman, OS 레벨 여섯 항목, 그리고 진단·처방의 흐름도 — 모두 책의 다른 챕터에 뿌리를 두고 있다. 4장의 fork 모델 위에 `max_connections` 함정이 서고, 5장의 MVCC와 6장의 HOT 위에 인덱스 무력화의 진짜 원인이 서고, 18장의 vacuum 위에 통계 운영이 서고, 21장의 옵저버빌리티 위에 발견과 격리가 선다.

그 조립이 손에 익으면, EXPLAIN 출력 한 장을 받았을 때 "다음 한 수"가 떠오른다. 그게 23장이 노린 출구다. 누군가 Slack에 EXPLAIN을 던졌을 때 "estimate가 100배 어긋났네요, ANALYZE 한 번 돌려보세요" 한 줄로 답할 수 있는 사람이 되면, 그게 이 챕터를 다 읽은 표시다.

**기억해두자.** 느린 쿼리의 80%는 새 인덱스가 아니라 이미 있는 인덱스가 일을 안 하고 있는 문제다. 그리고 그 문제의 절반은 코드 한 줄 — 함수 감싸기, 캐스트, OR — 에서 시작한다. 새 것을 만들기 전에 있는 것을 의심하는 게 튜닝의 첫 자세다.

다음 24장에서는 매니지드 PostgreSQL — RDS, Aurora, AlloyDB, Supabase, Neon — 의 선택 의사결정으로 넘어간다. 23장에서 본 vacuum·HA·튜닝·익스텐션의 원리가, 매니지드 벤더를 고르는 그 자리에서 정확히 그대로 쓰인다. 사진보다 재료부터 보는 자세 — 그게 24장의 첫 문장이다.
