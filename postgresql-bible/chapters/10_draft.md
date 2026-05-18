# 10장. 전문 검색 — Elasticsearch 없이 가는 길

검색이 필요해서 Elasticsearch를 또 하나 세운다고 해보자. 운영팀이 한숨을 쉴 것이다. 그 한숨이 어디서 오는지는 직접 굴려본 사람이라면 안다. JVM 힙을 어디까지 줄까, shard 수는 몇으로 잡을까, 색인 노드와 검색 노드를 분리할까, snapshot 저장소는 어디로 둘까, 그리고 무엇보다 — 원본 데이터는 PostgreSQL에 있는데 그걸 ES로 어떻게 동기화할까. CDC 파이프라인을 또 한 줄 세워야 한다. Debezium을 깔고, Kafka를 띄우고, 토픽을 만들고, 컨슈머를 짜고, 스키마가 바뀌면 reindex 절차를 만든다. 그 모든 게 한 회사의 검색 한 줄을 지탱한다.

그렇게 만든 시스템이 잘못된 건 아니다. 검색 트래픽이 충분히 크고, 랭킹 모델을 매주 튜닝하고, 다국어와 동의어와 synonym dictionary를 본격적으로 운영하는 회사라면 dedicated 검색 엔진이 답이다. 그런데 그렇지 않은 회사도 꽤 많다. 그저 게시판 검색이 필요하거나, 상품 이름과 설명을 같이 뒤지고 싶거나, 사용자가 오타를 좀 내도 적당히 찾아주면 된다거나, 한국어 본문을 형태소 단위로 잘라 검색하고 싶을 뿐인 경우다. 그런 회사가 ES를 한 벌 더 운영하는 건 어딘가 찜찜하다. 데이터는 두 군데에 살고, 일관성은 어디까지 보장될지 모호하고, 장애 표면적은 두 배가 된다.

PostgreSQL 진영에는 그 한숨을 줄여보려는 도구들이 차곡차곡 쌓여 왔다. 내장 풀텍스트 검색에서 출발해 pg_trgm, PGroonga, 그리고 최근의 BM25 기반 익스텐션인 ParadeDB의 pg_search와 Tiger Data의 pg_textsearch까지. 이 도구들을 하나씩 살펴보면서, "검색이 필요할 때 또 다른 DB를 세울 것인가, PG 안에서 끝낼 것인가"의 의사결정 지도를 그려보자. 그리고 결국 가장 어려운 문제 — 한국어 검색을 PG로 어디까지 잘 할 수 있는가 — 에 답하는 절을 마지막에 두었다.

한 가지 미리 짚어둘 게 있다. 이 장은 "ES를 쓰지 말자"는 주장이 아니다. 검색이 비즈니스의 본업이라면 dedicated 검색 엔진의 정당성은 분명히 살아 있다. 다만 검색이 본업이 아닌데 ES를 한 벌 더 짊어지고 있는 회사가 꽤 많고, 그 짐을 줄일 수 있는 시점이 이제 왔다는 이야기다. 의사결정의 기준을 같이 세워보자.

## 10.1 내장 tsvector/tsquery — 무료로 따라오는 풀텍스트

가장 먼저 펼쳐볼 카드는 PostgreSQL이 기본으로 제공하는 풀텍스트 검색이다. 별도 익스텐션을 깔 필요도 없고, 라이선스를 걱정할 일도 없고, RDS든 Cloud SQL이든 Aurora든 Supabase든 어디서나 돌아간다. 도구 비용이 0이라는 사실은 의외로 강력한 출발점이다. "ES를 먼저 깔자"는 의사결정이 정말 필요한지 아닌지를 가르는 첫 번째 질문은 "내장 풀텍스트로 안 될까?"여야 한다. 안 된다는 증거가 나오기 전까진 비용 0의 카드를 먼저 써보는 편이 낫다.

핵심 자료형은 두 개다. `tsvector`는 문서를 토큰으로 잘라 저장한 형태이고, `tsquery`는 그 토큰들을 조건으로 묻는 질의문이다. 이 둘을 `@@` 연산자로 매칭한다. 간단한 예를 들어보자.

```sql
-- 문서 컬럼이 있다고 가정
SELECT id, title
FROM articles
WHERE to_tsvector('english', title || ' ' || body)
      @@ to_tsquery('english', 'postgres & extension');
```

영문 문서라면 이 한 줄로 풀텍스트 검색이 작동한다. 그런데 매 쿼리마다 `to_tsvector`로 문자열을 토큰으로 잘라내는 건 비싸다. 매 호출마다 같은 문서를 다시 파싱하기 때문이다. 인덱스가 없다면 모든 row의 본문을 매번 처음부터 다시 잘라야 한다. 그래서 보통은 컬럼을 따로 두고, generated column이나 trigger로 미리 채워둔 뒤 GIN 인덱스를 건다.

```sql
ALTER TABLE articles
  ADD COLUMN tsv tsvector
  GENERATED ALWAYS AS (to_tsvector('english', title || ' ' || body)) STORED;

CREATE INDEX articles_tsv_gin ON articles USING GIN (tsv);
```

이 구성이면 1천만 row 정도까지는 무난하게 돌아가는 게 일반적이다. 영문 위주 워크로드에서 ES를 따로 띄울 이유는 거의 없다. generated column이 PostgreSQL 12부터 stored 형태로 들어왔기 때문에, trigger를 직접 짤 일도 줄었다. 본문이 바뀌면 `tsv` 컬럼이 자동으로 함께 바뀌고, GIN 인덱스가 따라간다. 한 번 만들어두면 잊고 사는 구조다.

내장 FTS가 잘 하는 일은 분명하다. **stemmer**가 있어서 "running"과 "runs"를 같은 토큰으로 본다. **stop word**를 빼준다. "the", "and" 같이 검색에 의미 없는 단어는 인덱스에서 빠진다. **가중치(weight)**를 줘서 제목 매칭과 본문 매칭을 다르게 평가할 수 있다.

```sql
-- 제목은 A 가중치, 본문은 D 가중치
SELECT id, title,
       ts_rank(
         setweight(to_tsvector('english', title), 'A') ||
         setweight(to_tsvector('english', body),  'D'),
         to_tsquery('english', 'postgres & extension')
       ) AS rank
FROM articles
WHERE to_tsvector('english', title || ' ' || body)
      @@ to_tsquery('english', 'postgres & extension')
ORDER BY rank DESC
LIMIT 10;
```

가중치 A·B·C·D 각각의 곱수는 설정으로 조정할 수 있다. 검색 결과 정렬에 제목 매칭이 더 큰 점수를 갖게 되는 식이다. **phrase 검색** (`<->`), **prefix 검색** (`:*`), `&`·`|`·`!`의 boolean 조합도 자연스럽게 표현된다. 영문이라면 이 정도면 대부분의 요구를 채운다.

내장 FTS의 또 다른 미덕은 **언어별 dictionary**의 다양함이다. `english`, `german`, `french`, `spanish` 등 주요 유럽어를 위한 dictionary가 기본 패키지에 들어 있다. 언어별로 stemmer 규칙과 stop word 목록이 다르고, 그 차이가 검색 품질에 직접 반영된다. `pg_ts_config` 카탈로그를 들여다보면 어떤 언어가 지원되는지 한눈에 보인다. 다국어를 다루더라도 라틴 계열에 한정된다면 dictionary만 골라 쓰면 끝이다.

여기까지가 좋은 소식이고, 한계로 넘어가보자. 두 가지 벽이 있다.

첫째, **랭킹의 품질이 BM25에 못 미친다**. 내장 `ts_rank`는 토큰 빈도 기반의 단순한 모델이라, 문서 길이 정규화나 inverse document frequency 같은 BM25의 핵심 항을 깊게 반영하지 않는다. `ts_rank_cd`는 cover density 모델로 phrase 근접도를 좀 더 반영하지만, BM25 수준의 정교한 통계 모델은 아니다. 검색 결과의 "느낌"이 ES만큼 자연스럽지 않다는 후기는 흔하다. "그래도 결과가 나오긴 하잖아"로 만족할 수 있는지가 분기점이다. 게시판 검색이라면 충분하지만, 상품 검색에서 매출에 직결되는 정렬 품질을 원한다면 BM25를 갖춘 도구로 갈아탈 때다.

둘째, **한국어를 토큰으로 자르지 못한다**. PostgreSQL이 기본으로 제공하는 dictionary와 parser에는 한국어 형태소 분석기가 없다. `to_tsvector('simple', ...)`로 띄어쓰기 기준 분리는 되지만, 그건 검색이 아니다. "데이터베이스를"과 "데이터베이스"가 다른 토큰으로 잡힌다는 뜻이다. 같은 의미인데 토큰이 달라지면 검색에 잡히지 않는다. 형태소 분석기 없이 한국어 풀텍스트는 사실상 불가능에 가깝다. 영문 쓰던 사람이 한국어 본문에 같은 방식을 적용했다가 검색 결과가 텅 비어버리는 광경은 꽤 흔하다. 이 지점에서 내장 FTS는 한국 서비스에 답이 아니다.

물론 사용자 사전이나 외부 형태소 분석기와 연동하는 길도 있긴 하다. mecab-ko 같은 분석기를 wrapper로 붙이는 시도들이 있어 왔다. 하지만 그건 도구 한 벌을 또 세팅하는 일이고, 운영 부담이 작지 않다. 한국어를 진지하게 다룰 거라면 차라리 다음 절들에서 다룰 PGroonga로 가는 편이 낫다. 직접 wrapper를 깎는 것보다 한국어를 일급으로 다루는 엔진을 그대로 가져다 쓰는 게 시간 대비 효율이 훨씬 좋다.

운영에서 자주 마주치는 함정 한 가지를 짚어두자. **검색 쿼리에서 `to_tsvector(...)` 함수를 직접 호출하면서 동시에 GIN 인덱스를 기대하는 경우**다. 인덱스를 컬럼 자체가 아니라 표현식에 걸어뒀다면, 쿼리의 표현식과 인덱스의 표현식이 정확히 일치해야 인덱스가 쓰인다. dictionary 이름 하나 다르거나, 파라미터 순서 하나 어긋나면 인덱스가 무력화돼 seq scan으로 떨어진다. `EXPLAIN`을 한 번 찍어보면 알 수 있지만, 운영 중 모니터링에서야 뒤늦게 발견하면 난감해진다. 가장 안전한 패턴은 위 예제처럼 `tsv` 컬럼을 generated column으로 따로 두고 그 컬럼에 GIN 인덱스를 거는 방식이다.

정리하자면, 내장 tsvector/tsquery는 영문 워크로드의 출발점으로는 더할 나위 없이 좋다. 무료고, 모든 매니지드 PG에서 돌고, 통합 검증된다. 단, **한국어**와 **고급 랭킹**이라는 두 벽 앞에서 멈춘다. 그 두 벽이 우리 서비스의 요구와 겹친다면, 다음 도구를 꺼낼 시점이다.

## 10.2 pg_trgm — 오타를 견디는 fuzzy match

내장 FTS의 한계 중 하나로 "오타 허용"이 잘 안 된다는 점이 있다. 사용자가 "postgresql"을 "postgresqi"로 쳤다고 해보자. 토큰 단위 정확 매칭만 하는 풀텍스트로는 한 글자 차이가 영영 다른 단어다. 검색 결과가 텅 비어 돌아오면 사용자는 "이 사이트는 검색이 안 되네"라고 닫고 떠난다. 이런 fuzzy 매칭을 풀어주는 카드가 `pg_trgm`이다.

이름 그대로 `pg_trgm`은 문자열을 trigram(연속한 세 글자)으로 쪼개 비교한다. "postgres"라는 문자열은 `pos`, `ost`, `stg`, ... 같은 trigram의 집합으로 표현되고, 두 문자열의 trigram 집합 교집합이 얼마나 큰가로 유사도를 잰다. 수식으로 단순화하면 자카드 유사도(Jaccard similarity)에 가깝다. 이 모델은 한 글자 오타나 어미 차이에 강하다. 단어가 살짝 어긋나도 trigram의 상당수는 겹치기 때문이다.

```sql
CREATE EXTENSION pg_trgm;

CREATE INDEX products_name_trgm
  ON products USING GIN (name gin_trgm_ops);

SELECT id, name, similarity(name, 'postgresqi') AS sim
FROM products
WHERE name % 'postgresqi'
ORDER BY sim DESC
LIMIT 10;
```

검색어가 오타여도 그럭저럭 결과가 나온다. autocomplete 같은 시나리오 — 사용자가 한 글자씩 타이핑하는 동안 즉시 후보를 보여주는 경우 — 에도 유용하다. `LIKE 'foo%'` 패턴을 인덱스로 가속하는 부수적인 효과도 있다. 일반 B-tree 인덱스는 leading wildcard(`%foo%`)에 무력한데, trigram GIN 인덱스는 양쪽 wildcard도 가속한다. "어딘가에 'foo'가 들어간 행"을 빠르게 찾는 패턴이 인덱스로 풀린다는 점만으로도 pg_trgm을 깔아둘 가치가 충분한 경우가 많다.

pg_trgm이 제공하는 도구를 좀 더 펼쳐보자. 비교 연산자로는 `%`(유사도 임계치 초과)와 `<%`(왼쪽 인자가 오른쪽의 일부와 닮음)가 있다. 거리 함수로는 `<->`가 있어서, `similarity(a, b)`의 반대 개념으로 0에 가까울수록 가까운 문자열이다. 임계치는 `pg_trgm.similarity_threshold` 세션 변수로 조정할 수 있다. 기본값은 0.3 정도지만 자기 서비스의 데이터 특성에 맞춰 한 번은 조정해보는 편이 낫다. 임계치가 너무 낮으면 결과가 폭주하고, 너무 높으면 오타 허용이 사라진다.

```sql
-- 임계치를 0.4로 올려서 더 엄격하게
SET pg_trgm.similarity_threshold = 0.4;

-- 거리 기준 정렬 (KNN 스타일)
SELECT id, name
FROM products
ORDER BY name <-> 'postgres'
LIMIT 10;
```

`<->` 거리 기준 정렬은 GiST 인덱스와 결합하면 KNN 검색처럼 작동한다. "가장 닮은 것 K개"를 인덱스 한 번 타고 끝낸다. fuzzy 자동완성의 모범 답안 같은 패턴이다.

그런데 `pg_trgm`을 한국어 검색에 그대로 들이밀면 곧 난감한 상황을 만난다. trigram은 본래 단일 바이트 문자에 맞춰 설계된 모델이다. UTF-8 한글 한 글자는 3바이트이고, 형태소 단위로 의미가 갈리는 한국어에 "연속한 3글자" 기준이 의미적으로 잘 들어맞지 않는다. 게다가 한자·한글·일본어처럼 비라틴 문자 처리에 제약이 있다는 점이 PGroonga 공식 문서에서 명시적으로 비교 항목으로 등장할 정도다. "한국어 처리는 부적합"이라는 한 줄이 거기 박혀 있다.

직접 확인해보고 싶다면 한국어 짧은 문자열로 `similarity()`를 한 번 호출해보자. 의미적으로 비슷한 두 단어("데이터베이스"와 "데이타베이스")의 점수가 의외로 낮게 나오거나, 의미적으로 전혀 다른 두 단어가 같은 받침을 공유한다는 이유로 점수가 높게 나오는 광경을 만날 수 있다. 한국어를 trigram으로 다루는 건 글자가 아니라 자모 단위로 분해해서 비교하는 식의 별도 기법이 필요한데, 그건 pg_trgm의 기본 동작이 아니다.

물론 "이름이 짧고 영문이 많이 섞인 상품명" 정도라면 한국어 환경에서도 pg_trgm이 쓸 만한 케이스가 있다. 한영 혼용 검색에서 영문 토큰의 fuzzy 매칭은 충분히 잡아준다. SKU 코드, 제품 모델명, 브랜드명 같이 영숫자가 섞인 짧은 문자열의 자동완성·오타 허용에 pg_trgm은 여전히 유효하다. 다만 한국어 본문을 어절·형태소 수준으로 가르는 진짜 풀텍스트가 필요하다면, pg_trgm은 답이 아니다.

그렇다면 pg_trgm은 어떤 자리에 두면 좋을까. 두 가지 용도가 가장 잘 어울린다.

첫째, **사용자 입력 fuzzy 매칭**. 자동완성, 오타 허용 검색, "이거 찾으셨나요?" 제안. 영문 위주의 짧은 문자열이라면 trigram이 가볍고 빠르다. 검색창 옆에 KNN 스타일 자동완성 한 줄을 다는 일이 인덱스 하나로 끝난다.

둘째, **다른 풀텍스트 도구의 보완재**. 내장 FTS나 PGroonga로 메인 검색을 하고, 결과가 비었거나 부족할 때 pg_trgm으로 한 번 더 시도하는 fallback 패턴이다. "정확 매칭 → fuzzy 매칭" 단계를 한 SQL 안에서 짤 수 있다는 점이 매력이다.

```sql
-- 메인 풀텍스트 검색
WITH primary_hits AS (
  SELECT id, title, ts_rank(tsv, query) AS rank
  FROM articles, to_tsquery('english', 'postgres & extension') query
  WHERE tsv @@ query
  ORDER BY rank DESC
  LIMIT 20
)
SELECT * FROM primary_hits
UNION ALL
-- 결과가 비었거나 너무 적으면 fuzzy로 보강
SELECT id, title, 0::real AS rank
FROM articles
WHERE NOT EXISTS (SELECT 1 FROM primary_hits)
  AND title % 'postgres extension'
ORDER BY rank DESC
LIMIT 20;
```

이런 fallback 패턴 한 줄이 사용자 경험을 꽤 부드럽게 만든다. 메인 검색이 정확한 답을 못 줄 때, 묵묵히 0건을 반환하는 대신 "닮은 것"을 제시한다. 사용자가 떠나기 전에 한 번 더 붙잡는다는 의미다.

운영 함정도 짚어두자. **trigram GIN 인덱스는 write 비용이 크다**. 한 문자열을 N개 trigram으로 쪼개 인덱스에 넣기 때문에, 인덱스 크기가 본문 컬럼보다 훨씬 커지는 경우가 흔하다. 자주 갱신되는 거대 텍스트 컬럼에 무조건 trigram 인덱스를 거는 건 신중해야 한다. 갱신 빈도가 낮은 마스터 데이터, 또는 변동이 적은 상품명·이름 컬럼 정도가 가장 잘 맞는다. 갱신이 잦으면 `gist_trgm_ops` GiST 인덱스를 검토하거나, partial index로 검색 대상을 좁히는 패턴을 함께 본다.

기억해두자. pg_trgm은 풀텍스트 검색의 대체재가 아니다. 풀텍스트의 옆자리에 두고 fuzzy 보강을 맡기는 도구다. 한국어 본문 검색의 본진은 다음 절부터 등장한다.

## 10.3 PGroonga — 한국어·일본어·중국어를 zero-ETL로

한국어 풀텍스트가 필요하다면, PostgreSQL 진영에서 가장 먼저 펼쳐볼 카드는 PGroonga다. 이름의 어원은 PostgreSQL + Groonga. Groonga는 일본에서 시작된 오픈소스 풀텍스트 검색 엔진이고, 그 엔진을 PostgreSQL의 인덱스 access method로 감싼 것이 PGroonga다. 일본·한국·중국 등 CJK 환경을 일급으로 다루는 풀텍스트 엔진이 PG의 인덱스로 직접 들어왔다는 게 핵심이다. MySQL 진영의 Mroonga와 형제뻘 도구라 들어본 사람도 있을 것이다. 같은 Groonga 엔진을 어느 DB에 붙였느냐의 차이다.

왜 zero-ETL이라고 부르는지부터 보자. PG에 본문이 들어 있는데 검색만 ES로 보내야 한다면, 본문이 바뀔 때마다 ES로 흘려보내는 파이프라인이 필요하다. CDC를 깔든 dual-write를 하든, 한 군데 더 쓰는 비용이 든다. 데이터가 두 군데 사는 순간 "일관성"이라는 단어가 회의실에 등장한다. 어느 한쪽이 잠깐 뒤처지면 사용자에겐 "방금 올린 글이 검색에 안 잡힌다"는 현상으로 보인다. PGroonga는 인덱스를 PG 안에 둔다. `INSERT`·`UPDATE`·`DELETE`가 정상 트랜잭션 안에서 흘러가고, 인덱스는 그 트랜잭션의 일부로 갱신된다. ETL이 사라지는 건 그래서다. 본문이 있는 곳에 인덱스도 있다.

이 모델의 부수적 효과 한 가지를 짚어두자. **검색 결과가 트랜잭션 가시성을 그대로 따른다**. 같은 트랜잭션 안에서 row를 넣고 곧바로 검색하면, MVCC의 가시성 규칙에 따라 자기 자신의 변경이 보인다. 외부 ES와 동기화할 때 발목을 잡는 "방금 쓴 row가 안 검색됨" 현상이 구조적으로 사라진다. 9장에서 본 트랜잭션 가시성 모델이 검색 결과에까지 일관되게 적용된다는 뜻이다. 작은 차이 같지만, 운영에서는 큰 안심이다.

가장 단순한 사용 모양은 이렇다.

```sql
CREATE EXTENSION pgroonga;

CREATE INDEX articles_body_pgroonga
  ON articles USING pgroonga (body);

SELECT id, title
FROM articles
WHERE body &@ '데이터베이스';
```

`&@` 연산자가 PGroonga의 풀텍스트 매칭이다. 그밖에도 `&@~`로 query 구문(스페이스로 AND, OR 키워드 등) 지원, `&@*`로 prefix 검색, `&@|`로 OR 매칭이 가능하다. 풀텍스트 검색이 일상적으로 필요한 패턴은 거의 다 연산자로 제공된다.

랭킹이 필요하다면 `pgroonga_score()` 함수로 점수를 받는다.

```sql
SELECT id, title,
       pgroonga_score(tableoid, ctid) AS score
FROM articles
WHERE body &@~ '데이터베이스 인덱스'
ORDER BY score DESC
LIMIT 20;
```

`&@~` 연산자는 query 문법을 해석한다. 공백은 AND, `OR` 키워드는 OR, `-`로 NOT을 표현한다. 사용자가 검색창에 익숙하게 치는 구문이 그대로 들어간다.

### 토크나이저 — 검색 품질의 첫 번째 결정

한국어를 어떻게 자를 것인가는 토크나이저 설정으로 정한다. PGroonga가 제공하는 토크나이저는 여럿이지만, 한국어 환경에서 주로 검토하는 카드는 셋이다.

- **TokenBigram** — 연속한 두 글자 단위로 자른다. "데이터베이스"를 `데이`, `이터`, `터베`, `베이`, `이스`로 본다. 사전이 필요 없고, 검색 누락이 적다. 정확한 단어 경계가 없어도 "데이터베이스"로 검색하면 본문의 그 부분이 매칭된다.
- **TokenMecab** — MeCab 형태소 분석기 기반. 일본어가 본진이지만, mecab-ko-dic 사전을 깔면 한국어 형태소 분석도 가능하다. 의미 단위로 토큰을 자르므로 인덱스 크기가 작고, "데이터베이스를"과 "데이터베이스"가 같은 토큰으로 잡힌다.
- **TokenNgram** (variable N) — 더 큰 N으로 trigram 이상도 가능. 짧은 키워드 검색이 많지 않다면 검토할 만하다.

인덱스를 만들 때 옵션으로 토크나이저를 지정한다.

```sql
CREATE INDEX articles_body_pgroonga
  ON articles USING pgroonga (body)
  WITH (tokenizer='TokenBigram');

-- MeCab + 한국어 사전을 쓰는 경우 (사전 설치 전제)
CREATE INDEX articles_body_pgroonga_mecab
  ON articles USING pgroonga (body)
  WITH (tokenizer='TokenMecab');
```

토크나이저 선택은 검색 품질에 직접 영향을 준다. N-gram은 정확도가 높고 오타에도 강하지만 인덱스가 커지는 경향이 있다. 형태소 분석기는 인덱스가 작고 의미 단위 매칭이 자연스럽지만 사전을 운영하는 부담이 생긴다. 자기 서비스의 문서 특성과 트래픽을 보고 한 번은 진지하게 비교해보는 편이 낫다.

어느 쪽을 먼저 시도할지 고민된다면, **TokenBigram부터 시작하는 편이 낫다**. 사전을 따로 운영하지 않아도 되고, 결과 누락이 거의 없으며, 운영 부담이 작다. 신규 단어가 자주 등장하는 서비스(상품명, 신조어, 영문 약어 혼용 등)에서는 형태소 분석기의 사전 갱신 부담이 의외로 크다. Bigram은 그런 부담에서 자유롭다. 의미 단위 정밀도가 떨어진다는 약점은 결과 정렬 단계에서 BM25나 사용자 클릭 피드백으로 보완하는 길도 있다. "처음엔 단순하게, 필요해지면 갈아탄다"는 흐름이 안전하다.

### JSON 검색 — JSONB와 풀텍스트의 만남

PGroonga의 또 다른 장점은 **JSON 검색**이다. JSONB 컬럼의 모든 텍스트 값을 한 번에 풀텍스트로 인덱스하는 옵션이 있다. 9장에서 JSON DB로서의 PostgreSQL을 살펴봤다면, 문서 안의 텍스트를 검색하는 시나리오가 곧장 떠올랐을 것이다. PGroonga가 그 자리를 깔끔하게 채운다.

```sql
CREATE INDEX events_payload_pgroonga
  ON events USING pgroonga (payload pgroonga_jsonb_full_text_search_ops_v2);

-- payload JSONB 어딘가에 '결제'가 들어간 row 검색
SELECT id, payload
FROM events
WHERE payload &@ '결제';
```

이벤트 로그·감사 로그·외부 API 응답 같이 스키마가 헐겁고 텍스트가 곳곳에 흩어진 데이터에서 진가가 드러난다. "어떤 key에 들어 있을지 모르겠지만 본문에 '결제'가 들어간 이벤트"를 한 줄 쿼리로 찾는다. JSON 안 깊숙이 있는 텍스트까지 자동으로 인덱스에 포함되므로, 검색 대상 key를 매번 명시할 필요가 없다. 운영 환경에서 troubleshooting 도구로 빛난다.

### 운영 환경에서의 PGroonga

운영 환경에서 PGroonga를 고려할 때 신경 쓸 지점이 세 가지 있다.

첫째, **매니지드 PG의 지원 여부**. Supabase는 공식 익스텐션으로 PGroonga를 제공한다. AWS RDS와 Aurora는 기본 익스텐션 목록에 없어서 자체 운영이거나 Supabase 같은 BaaS를 골라야 하는 제약이 따른다. Cloud SQL, AlloyDB, Azure Flexible 등도 가용성이 그때그때 다르다. 매니지드 PG로 갈 거라면 평가 단계에서 PGroonga 지원 목록을 한 번 확인해두는 편이 낫다. 익스텐션 한 줄 때문에 벤더가 좁아진다는 사실을 시작 단계에서 모르면, D-1에 발견하고 끔찍한 일이 된다. 24장에서 클라우드 PG를 다룰 때 이 매트릭스가 다시 등장하니 기억해두자.

둘째, **GIN과의 트레이드오프**. PGroonga 인덱스는 일반 GIN 인덱스와 비교했을 때 write 비용 양상이 다르다. 검색 품질 — 특히 비라틴 언어 — 에서는 압도적이지만, 인덱스 크기와 갱신 부하는 한 번 측정해두는 게 좋다. 자기 워크로드에서 얼마나 갱신되는 테이블인지, peak 시 write 처리량이 얼마인지를 보고 결정해야 한다. 일반적으로는 갱신이 잦지 않은 본문 위주 테이블(게시글, 상품 설명, 매뉴얼, 위키 등)에 가장 잘 맞는다.

셋째, **백업·복원과 인덱스 빌드 시간**. PGroonga 인덱스는 PG의 access method로 잘 통합돼 있어 `pg_dump`/`pg_restore` 흐름에서 따로 손댈 일이 없다. 다만 거대 테이블에 인덱스를 처음 만드는 시간은 만만치 않다. 마이그레이션이나 복원 시 인덱스 재생성 시간을 미리 측정하고, 운영 윈도우를 잡아두는 편이 낫다. `CREATE INDEX CONCURRENTLY`도 PGroonga에서 동작한다는 점은 다행이다.

운영 패턴을 한 줄 더 짚자면, 보통 **본문 컬럼을 모은 검색 전용 컬럼**을 만들고 거기에 PGroonga 인덱스를 거는 패턴이 깔끔하다.

```sql
ALTER TABLE articles
  ADD COLUMN search_text text
  GENERATED ALWAYS AS (title || ' ' || coalesce(summary, '') || ' ' || body) STORED;

CREATE INDEX articles_search_pgroonga
  ON articles USING pgroonga (search_text);
```

이렇게 두면 어느 필드에 매칭됐든 한 인덱스가 처리한다. 가중치는 결과 정렬 단계에서 SQL로 다시 계산할 수도 있고, BM25 점수가 필요하면 다음 절의 pg_search와 결합한다.

정리하자면, **한국어 본문이 들어가는 검색**이라면 PG 안에서 첫 번째로 펼칠 카드가 PGroonga다. 내장 FTS의 분석기 부재 문제도, pg_trgm의 비라틴 제약도 한꺼번에 푼다. ES 외부 클러스터의 한숨을 없애고, 본문과 같은 트랜잭션 안에서 인덱스를 유지하는 zero-ETL 모델을 얻는다. 그렇다면 BM25 랭킹이 핵심인 시나리오는? 그 자리에 등장하는 게 다음 절의 ParadeDB pg_search다.

## 10.4 ParadeDB pg_search — BM25를 PG 안으로

검색 품질에 한 번이라도 진지하게 신경 써봤다면 BM25라는 단어가 익숙할 것이다. BM25는 Okapi BM25라는 이름의 문서-질의 랭킹 함수로, 텀 빈도와 역문서 빈도(IDF), 문서 길이 정규화를 균형 있게 결합한 모델이다. 짧게 말하면 "흔한 단어에는 점수를 적게, 드문 단어에는 점수를 크게, 너무 긴 문서에는 페널티를"이라는 직관을 수학적으로 다듬은 모델이다. Elasticsearch와 Apache Solr가 기본 랭킹 함수로 채택하면서 사실상 텍스트 검색의 산업 표준이 됐다. PG의 내장 `ts_rank`는 좀 더 단순한 모델이라, "검색 결과의 자연스러움"에서 차이가 난다.

그렇다면 BM25를 PostgreSQL 안에서 그대로 쓰는 길은 없을까. 있다. ParadeDB가 만든 `pg_search`다.

`pg_search`의 핵심 아이디어는 단순하다. Rust로 작성된 풀텍스트 검색 라이브러리 **Tantivy**(Lucene을 닮은 디자인의 Rust 구현체)를 PostgreSQL의 인덱스 access method로 감싸 올린 것이다. Tantivy가 BM25 랭킹을 제공하니 PG도 BM25 랭킹을 갖게 된다. ParadeDB가 공개한 벤치마크에 따르면 1M row 기준 인덱싱 시간이 tsvector보다 약 50초 단축되고, 랭킹 쿼리가 20배 빠르며, dedicated Elasticsearch에 견줄 만한 성능이 나온다. 마케팅 문구를 한 줄로 줄이면 "이젠 ES 안 깔아도 BM25는 된다"이다.

문법도 PG 사용자가 친숙하게 받아들이도록 짜여 있다.

```sql
CREATE EXTENSION pg_search;

CREATE INDEX articles_search_idx ON articles
USING bm25 (id, title, body)
WITH (key_field='id');

SELECT id, title, paradedb.score(id) AS rank
FROM articles
WHERE title @@@ 'postgres extension'
   OR body  @@@ 'postgres extension'
ORDER BY rank DESC
LIMIT 20;
```

`USING bm25` 한 줄로 access method를 지정하고, `@@@` 연산자로 검색하고, `paradedb.score(...)`로 BM25 점수를 받는다. 결과는 BM25 점수 순으로 정렬한다. 풀텍스트 검색의 모범 답안 같은 형태다.

복잡한 query는 JSON으로 표현할 수도 있다. Lucene/Elasticsearch DSL에 익숙한 사람이라면 친숙한 모양이다.

```sql
SELECT id, title, paradedb.score(id) AS rank
FROM articles
WHERE id @@@ paradedb.boolean(
  must => ARRAY[
    paradedb.term(field => 'title', value => 'postgres'),
    paradedb.term(field => 'body',  value => 'extension')
  ],
  should => ARRAY[
    paradedb.phrase(field => 'body', phrases => ARRAY['index', 'access', 'method'])
  ]
)
ORDER BY rank DESC
LIMIT 20;
```

`must`/`should`/`must_not` 같은 boolean 조합, `term`/`phrase`/`fuzzy`/`regex` 같은 leaf 질의가 함수 호출로 표현된다. ES DSL을 SQL 안에 박아넣은 형태라고 보면 된다. 이 표현력이 단순 매칭을 넘어 "랭킹 조건을 정교하게 짜는" 시나리오에서 빛을 낸다.

### 하이브리드 검색 — pg_search × pgvector

pg_search가 진짜로 빛나는 자리는 **하이브리드 검색**이다. ParadeDB가 자주 강조하는 시나리오가 있다. BM25로 키워드 매칭을 하고, pgvector로 시맨틱 매칭을 하고, 둘의 점수를 가중 평균이나 **RRF**(Reciprocal Rank Fusion)로 결합한다. 한 트랜잭션, 한 SQL 안에서 둘 다 끝난다.

```sql
-- 키워드 검색 (BM25)과 벡터 검색 (cosine distance)을 RRF로 결합
WITH bm25_hits AS (
  SELECT id, row_number() OVER (ORDER BY paradedb.score(id) DESC) AS rk
  FROM articles
  WHERE body @@@ '데이터베이스 인덱스 튜닝'
  ORDER BY paradedb.score(id) DESC
  LIMIT 100
),
vector_hits AS (
  SELECT id, row_number() OVER (ORDER BY embedding <-> $1) AS rk
  FROM articles
  ORDER BY embedding <-> $1
  LIMIT 100
),
fused AS (
  SELECT id, SUM(1.0 / (60 + rk)) AS score
  FROM (
    SELECT id, rk FROM bm25_hits
    UNION ALL
    SELECT id, rk FROM vector_hits
  ) u
  GROUP BY id
)
SELECT a.id, a.title, f.score
FROM fused f JOIN articles a ON a.id = f.id
ORDER BY f.score DESC
LIMIT 20;
```

RRF 공식은 단순하다. 각 채널에서의 순위 `rk`를 받아 `1 / (k + rk)`로 변환한 뒤 합산한다 (`k`는 보통 60). 점수의 scale이 다른 채널을 robust하게 결합하는 데 잘 알려진 방법이다. 두 채널 모두에 잘 잡힌 문서가 위로 올라온다.

ES로 키워드 검색하고 외부 벡터 DB로 시맨틱 검색한 뒤 애플리케이션에서 결합하는 구조와 비교해보자. 인프라가 한 벌로 줄고, 점수 결합이 단일 쿼리 안에서 이뤄진다. 운영팀이 모니터링할 시스템 수가 줄고, 한 트랜잭션 안에서 일관성이 보장된다. 12장에서 다룰 RAG 백엔드 설계와 자연스럽게 이어지는 그림이다.

### 도입 전에 짚어둘 트레이드오프

물론 좋기만 한 도구는 없다. pg_search를 들이기 전에 고민해둘 지점이 있다.

첫째, **한국어 토큰화는 별도로 챙겨야 한다**. Tantivy의 토크나이저 옵션에 CJK 처리가 있긴 하나, PGroonga가 다국어 풀텍스트 엔진으로 출발한 것에 견주면 한국어 형태소 분석의 성숙도는 다르다. "BM25 랭킹은 갖고 싶은데 한국어 분석은 PGroonga가 더 자연스러워" — 이 조합을 풀어주는 게 다음 의사결정 절에서 살펴볼 PGroonga + pg_search 패턴이다. 영문이나 한영 혼용 위주 워크로드라면 pg_search 단독으로도 충분하다.

둘째, **매니지드 PG 지원 매트릭스**. 신생 익스텐션이라 모든 클라우드에 있지는 않다. Neon이 공식 익스텐션으로 제공한다. AWS RDS와 Aurora는 기본 카탈로그에 없다. ParadeDB가 자체 매니지드 서비스를 운영하고 있고, 이는 본질적으로 ParadeDB 익스텐션을 미리 깐 PostgreSQL 호환 서비스다. 매니지드 환경에서 pg_search가 필수라면 벤더 선택이 같이 좁아진다는 점을 잊지 말자. 17장의 마이그레이션 의사결정에서, 그리고 24장의 클라우드 PG 선택에서 이 한 줄이 분기점이 될 수 있다.

셋째, **인덱스 빌드 비용과 운영 모드**. Tantivy 기반이라 인덱스 자체의 disk footprint와 build 시간은 일반 GIN과 다르다. 대량 데이터에 처음 인덱스를 만드는 경우 시간이 꽤 걸린다. 이 점은 ES도 마찬가지지만, "PG 안에서 자연스럽게 돈다"는 인상에 속아 인덱스 빌드를 가볍게 봤다가는 난감해진다. 운영 환경에서는 `CREATE INDEX CONCURRENTLY`와 함께 maintenance window를 한 번은 짚고 가는 편이 낫다. 인덱스를 다시 만들어야 하는 시나리오(스키마 변경, 토크나이저 옵션 변경, 메이저 업그레이드)도 미리 시나리오로 갖춰두는 게 좋다.

넷째, **WAL과 백업의 일체감 관점**. pg_search의 인덱스는 Tantivy 형식으로 저장되며, PG 표준 WAL과 100% 자연스럽게 통합되지는 않는 측면이 있다. 백업·복원·streaming replica에서 인덱스 일관성을 다루는 방식이 일반 GIN과 다르므로, 운영 도입 전에 자기 백업·HA 구성에서 한 번은 테스트해보는 편이 낫다. 이 지점에서 다음 절에서 살펴볼 pg_textsearch가 다른 디자인 선택을 내세운다.

### 인덱스 설계 한 줄 더

pg_search의 BM25 인덱스는 여러 컬럼을 한 인덱스에 묶을 수 있다는 점이 GIN과 다르다. 위 예제의 `USING bm25 (id, title, body)`처럼 `key_field`와 검색 대상 필드들을 한 번에 선언한다. 필드별로 분석 옵션(토크나이저, 가중치, BM25 파라미터 k1·b)을 다르게 줄 수 있다는 점이 매력이다.

```sql
CREATE INDEX articles_search_idx ON articles
USING bm25 (id, title, body, tags)
WITH (
  key_field='id',
  text_fields='{
    "title": {"tokenizer": {"type": "default"}, "fast": true},
    "body":  {"tokenizer": {"type": "default"}},
    "tags":  {"tokenizer": {"type": "raw"}}
  }'
);
```

`fast` 필드로 지정하면 정렬·필터링 성능이 빨라진다. `raw` 토크나이저는 토큰을 자르지 않고 원본 그대로 인덱스한다(태그·카테고리·exact 매칭용). 인덱스 한 벌로 풀텍스트, faceting, 정렬을 다 풀려는 시나리오에 깔끔하게 맞는다.

정리하자면, **BM25 품질의 검색이 필요한데 또 다른 클러스터를 띄우긴 부담스럽다**면 pg_search가 첫 번째 카드다. 인프라 한 벌이 줄고, 트랜잭션이 PG 한 곳에서 끝나며, 하이브리드 검색의 길이 자연스럽게 열린다. 한국어를 같이 잡아야 한다면 PGroonga와의 조합이 답이 되는 경우가 많다.

## 10.5 Tiger Data pg_textsearch — 17 access method가 부른 경쟁

ParadeDB pg_search가 BM25를 PG로 가져온 첫 카드라면, 같은 자리에 다른 답을 제출한 두 번째 카드가 Tiger Data의 `pg_textsearch`다. 이 도구는 흥미로운 위치에 서 있다. 같은 BM25, 같은 "ES 없이도 된다"는 약속, 그런데 구현은 다르다. 같은 문제를 푸는 두 진영이 다른 답을 들고 나왔다는 사실이 운영하는 사람 입장에서 무엇을 의미하는지 천천히 보자.

### 같은 BM25, 다른 디자인 선택

이 두 익스텐션이 비슷한 시기에 등장한 데는 배경이 있다. PostgreSQL 17에서 **인덱스 access method API가 개선**되면서, 외부 풀텍스트 엔진을 인덱스로 끼워 넣는 일이 한층 깔끔해졌다. ParadeDB가 Tantivy를 access method로 감싸 BM25 검색을 가능하게 했듯, Tiger Data는 같은 BM25 모델을 **PostgreSQL의 페이지 구조 위에 직접 구현**하는 길을 택했다. 17의 access method 개선이 만든 무대 위에 두 진영이 다른 디자인 선택으로 올라온 셈이다.

이 디자인 차이가 운영에서 어떻게 보이는지가 핵심이다. 두 접근의 차이를 거칠게 정리하면 이렇다.

| 항목 | pg_search (ParadeDB) | pg_textsearch (Tiger Data) |
|------|----------------------|----------------------------|
| 검색 엔진 | Tantivy (Rust, Lucene 계열) | PG 페이지 위에 자체 구현 |
| 인덱스 storage | Tantivy 형식, PG 인덱스로 노출 | PG 표준 페이지 |
| WAL 통합 | 인덱스 자체는 외부 엔진 형식, WAL은 우회 경로 | PG 표준 WAL에 자연스럽게 통합 |
| 백업·복제 | Tantivy 인덱스를 별도로 다룰 필요 | `pg_basebackup`·streaming 복제와 그대로 호환 |
| 운영 성숙도 | 검색 품질·하이브리드 시연 풍부 | PG 운영 도구와의 정합성 강조 |

위 표는 디자인 의도의 차이를 보여주는 거친 스케치이고, 두 도구의 자세한 성능 비교는 시간이 지나면서 더 데이터가 쌓일 영역이다. 핵심은 어느 한쪽이 정답이 아니라는 점이다. **두 진영의 경쟁이 시작됐다**는 사실 자체가 PG 사용자에게는 좋은 소식이다.

### 운영 도구 체인과의 정합성이라는 가치

운영 관점에서 한 번 생각해보자. PostgreSQL을 메인 DB로 쓰는 팀이 가장 신경 쓰는 도구 체인은 백업, PITR, 스트리밍 복제, HA다. 인덱스가 PG 표준 페이지로 들어가 있으면 `pg_basebackup`·`pgBackRest`·streaming replica가 그대로 일관성을 보장한다. 외부 엔진 형식의 인덱스라면 백업 시 그 인덱스 데이터의 일관성을 별도로 챙기거나, 복원 후 reindex 절차를 추가로 두는 식으로 운영 흐름이 한 단계 늘어날 수 있다. 검색 품질만 보고 도구를 고르면 운영 단계에서 뒤늦게 고생할 수 있으니, **백업·복제 호환성을 평가 항목에 꼭 넣어두자**.

좀 더 구체적으로 이런 시나리오를 상상해보자. 새벽 3시에 primary 장애가 나서 standby로 페일오버가 일어난다. 20장에서 다룰 Patroni가 잘 작동해서 페일오버 자체는 자동이다. 그런데 새 primary에 올라간 standby의 검색 인덱스는 어떤 상태인가? PG 표준 WAL로 흘러 들어간 인덱스라면 추가 절차 없이 정상이다. 외부 엔진 형식의 인덱스라면 그 일관성이 streaming 복제로 어떻게 따라왔는지를 한 번 더 확인해야 한다. 어떤 상황에는 인덱스 rebuild가 필요할 수 있고, rebuild 시간 동안 검색이 일부 작동하지 않는 회색 지대가 생긴다. 이 작은 차이가 야간 호출 한 통의 무게를 가른다.

물론 ParadeDB도 이 부분에 대한 운영 가이드와 도구를 계속 보강하고 있다. 어느 시점의 어느 버전이냐에 따라 호환성과 안정성은 빠르게 바뀐다. 도입 직전엔 GitHub 이슈와 changelog를 한 번 훑어보는 편이 낫다.

### 17 access method가 만든 더 큰 흐름

또 하나, **17 access method API의 개선이 만든 흐름**은 검색만의 이야기가 아니다. 같은 API 진화가 12장에서 다룰 pgvectorscale, 15장에서 다룰 columnar 익스텐션의 등장에도 영향을 미친다. 인덱스 access method가 한 단계 깔끔해지면서, "특정 자료구조를 PG 인덱스로 노출하는" 패턴이 더 다양한 영역에서 시도되고 있다. PostgreSQL이 "core를 안 건드리고도 새 자료구조를 깔끔히 추가할 수 있는 플랫폼"이 됐다는 신호다.

이게 1장에서 짚었던 "PG의 진짜 moat는 익스텐션 composability"라는 주장의 구체적 사례 한 줄이다. 검색 한 분야에서 두 진영이 BM25로 경쟁하는 그림은, PG 생태계의 다음 10년이 어디로 흘러갈지를 짧게 보여준다. dedicated 도구를 들이는 비용이 점점 더 정당화하기 어려운 워크로드가 늘어나는 흐름이다. "Just Use Postgres"라는 짧은 슬로건이 어떤 인프라적 토대 위에 서 있는지를 가장 잘 보여주는 한 컷이 검색 익스텐션 경쟁이다.

### 어느 카드를 먼저 살펴볼까

선택의 가이드 한 줄로 정리하자면 이렇다. **검색 품질·하이브리드 시연·생태계 활동성을 중시한다면** pg_search가 현재 가장 두꺼운 자료와 사용 사례를 갖고 있다. 공식 블로그, 벤치마크, GitHub 활동 모두 활발하고, 하이브리드 검색을 SQL 한 줄에 담는 시연이 가장 잘 정리돼 있다. **PG 표준 도구 체인과의 일체감, 백업·복제의 단순함을 중시한다면** pg_textsearch가 차분히 살펴볼 옵션이다. Tiger Data(구 Timescale)가 PG 익스텐션 운영에서 쌓은 노하우가 디자인에 반영돼 있다.

둘 다 신생 영역이라 운영 사례가 빠르게 쌓이는 중이니, 도입 결정 직전에는 GitHub 이슈와 공식 블로그를 한 번 더 들여다보는 편이 낫다. PoC 단계에서 자기 데이터셋(가능하면 production의 1/10 규모 정도)으로 인덱스 빌드 시간, 검색 latency, write 부하, 백업·복원 흐름을 한 번씩 통과시키는 게 가장 안전하다. 마케팅 벤치마크와 자기 워크로드가 다를 가능성은 항상 있다.

기억해두자. **검색 인프라를 새로 고를 때 가장 위험한 의사결정은 "벤치마크 숫자에 끌려가는 것"이다.** 자기 운영 환경의 백업·페일오버·매니지드 PG 지원·기존 도구 체인을 같이 평가표에 올려야 한다. 6개월 뒤에 후회하지 않는 의사결정은 거기서 나온다.

## 10.6 한국어 시나리오 의사결정 — PGroonga, 또는 PGroonga + pg_search

여기까지 다섯 가지 카드를 펼쳤다. 이제 가장 어려운 질문에 답할 차례다. "한국어 본문이 들어가는 검색을 PG로 풀자. 어떤 조합이 답인가?" 의사결정의 출발점이 될 표를 한 장 그려보자.

### 한국어 검색 스택 선택 가이드

| 시나리오 | 도구 조합 | 이유 | 멈춰야 할 선 |
|---------|----------|------|-------------|
| **한국어 본문 풀텍스트 (게시판·문서·상품 설명)** | PGroonga | 형태소·N-gram 토크나이저, zero-ETL, JSON 검색까지 | 형태소 사전을 운영할 인력이 없으면 N-gram으로 시작 |
| **한국어 + BM25 랭킹이 핵심** | PGroonga + pg_search | PGroonga의 한국어 토큰화 + pg_search의 BM25 점수 | 두 인덱스를 함께 유지하므로 write 부하 측정 필수 |
| **한국어 + 시맨틱 검색(RAG)** | PGroonga + pgvector | 키워드는 PGroonga, 의미는 pgvector, 점수는 RRF로 결합 | 12장의 벡터 운영 함정도 같이 짊어진다 |
| **한영 혼용 짧은 문자열 + 오타 허용 자동완성** | pg_trgm (+ PGroonga 보강) | trigram이 영문·숫자 fuzzy에 강함 | 본문 풀텍스트는 PGroonga로 별도 분리 |
| **영문/유럽어 위주 풀텍스트** | 내장 tsvector/tsquery | 비용 0, 모든 매니지드 PG에서 동작, 충분히 빠름 | 랭킹 품질에 만족 못하면 pg_search로 |
| **랭킹 모델 매주 튜닝, 동의어·synonym dict 본격 운영, 검색 트래픽이 메인 트래픽** | dedicated Elasticsearch / OpenSearch | 검색이 비즈니스 그 자체인 회사의 정당한 선택 | PG 안에서 다 풀려고 우기지 말 것 |

표에서 가장 자주 등장하는 조합 두 개를 좀 더 풀어보자.

**기본 한 줄: PGroonga로 시작한다.** 한국어 풀텍스트 검색을 PG로 풀자는 결정이 섰다면, 1순위는 PGroonga다. 내장 FTS는 한국어 분석기가 없고, pg_trgm은 비라틴 처리 제약이 있다. PGroonga는 다국어 풀텍스트 엔진을 PG 안으로 가져오면서 ETL을 없앤다. 토크나이저 선택(N-gram이냐 형태소냐)이라는 하나의 결정만 진지하게 한 번 내리면 된다. 매니지드 PG라면 Supabase가 가장 자연스러운 출발점이고, RDS나 Cloud SQL에서는 익스텐션 지원 여부를 평가 단계에서 확인하자.

**한 걸음 더: 랭킹이 중요하면 pg_search를 얹는다.** "한국어 토큰화는 PGroonga가 더 자연스러운데, 결과 정렬 품질은 BM25였으면 좋겠다"는 욕구를 푸는 길이다. 같은 본문에 PGroonga 인덱스와 pg_search 인덱스를 둘 다 깐다. PGroonga는 매칭과 한국어 토큰화를 맡고, pg_search는 BM25 점수를 매긴다. 두 결과를 한 쿼리 안에서 결합한다. 인덱스가 두 벌이라 write 부하와 디스크 사용량이 늘어나는 비용은 분명히 진다. 그래서 이 조합은 **검색 품질이 매출에 직결되는 시점부터** 정당해진다. 트래픽이 적은 초기에 미리 들이는 건 과한 경우가 많다.

**또 한 걸음 더: RAG라면 PGroonga + pgvector.** RAG 백엔드를 PG 안에서 끝내고 싶다면 키워드 검색은 PGroonga로, 시맨틱 검색은 pgvector로 본다. 두 점수를 RRF로 결합하면 어느 한쪽에 치우치지 않는 결과가 나온다. 이 그림은 12장에서 자세히 다룬다. 여기서는 "한국어 키워드 채널을 PGroonga로 잡는다"는 한 줄만 기억해두자.

### dedicated ES가 정당한 경계

오해를 막고 싶은 한 가지가 있다. 이 장은 "Elasticsearch를 쓰지 말자"는 주장이 아니다. ES가 정당한 자리는 분명히 있다. 다음 조건 중 두세 가지가 한꺼번에 해당된다면, 망설이지 말고 dedicated 검색 엔진으로 가는 편이 낫다.

- **검색 트래픽이 서비스의 메인 트래픽**이고, 검색 지연이 비즈니스 KPI에 직접 잡힌다. (이커머스 검색, 미디어 콘텐츠 검색, 로그 검색 SaaS 등)
- **랭킹 모델을 자주 바꾼다**. 동의어 사전, synonym graph, learning-to-rank, 카테고리별 boost 전략을 매주 튜닝한다.
- **다국어를 본격적으로 운영**한다. 5개 언어 이상, 언어별 다른 analyzer 체인, 언어 자동 감지가 필요하다.
- **수십~수백 TB의 텍스트**를 분산 색인해야 한다. shard·node 단위로 수평 확장이 자연스러운 워크로드.
- **검색 분석(검색 로그 자체에 대한 분석)**이 따로 비즈니스다. ES 위에서 Kibana로 분석 대시보드를 운영한다.

이런 경우 PG 익스텐션의 모든 장점을 모아 와도 dedicated 엔진의 운영 도구 체인과 생태계를 따라잡기 어렵다. "PG로 모든 걸 끝내자"는 매혹적이지만 자기 기만일 수 있다. **검색이 우리의 본업인가, 아닌가**를 정직하게 묻고 답하는 게 첫 번째 의사결정이다.

반대로, 검색이 본업이 아닌 회사가 ES 한 벌을 운영하고 있다면 — 일관성 걱정, CDC 파이프라인, JVM 튜닝, snapshot 보관 — 다음 분기에 한 번쯤은 "PG 안으로 가져올 수 있는가"의 질문을 꺼내볼 만하다. PGroonga와 pg_search가 등장한 지금, 그 질문의 답이 1년 전과 달라졌을 수 있다.

### ES → PG로 검색을 가져오는 단계적 패턴

기존에 ES를 쓰고 있는 시스템이 PG 안으로 검색을 흡수하려고 한다면, 한 번에 갈아엎는 식의 빅뱅 마이그레이션은 위험하다. 단계적인 패턴을 권한다.

**1단계: shadow 운영.** 본 검색 트래픽은 여전히 ES로 보내되, 같은 쿼리를 PG 익스텐션(PGroonga / pg_search)에도 비동기로 보낸다. 결과를 비교 로깅한다. 같은 쿼리에 두 시스템이 얼마나 다른 결과를 내는지, 어느 케이스가 의미 있게 차이 나는지 한 달쯤 관찰한다. 이 단계에서 사용자에게는 아무 변화가 없다.

**2단계: 카나리.** 트래픽의 1~5%를 PG 검색으로 보내고 나머지는 ES로 본다. 응답 시간·결과 클릭률·zero-result 비율 같은 지표를 두 그룹에서 비교한다. 비즈니스 KPI(검색 후 구매 전환율, 검색 후 게시글 클릭률 등)에 회귀가 없는지 확인한다. 회귀가 발견되면 어느 케이스에서 발생하는지 분석해 토크나이저·랭킹 가중치를 조정한다.

**3단계: 점진적 확대.** 카나리에서 회귀가 없다면 트래픽 비중을 점진적으로 올린다. 10%, 30%, 50%, 100% 같은 단계로 한 주씩 간격을 두고 늘린다. 각 단계마다 한 번씩 멈춰서 지표를 확인한다.

**4단계: ES 클러스터 해체.** 100% 전환이 한 달 이상 안정적으로 돌면, ES 클러스터를 해체한다. 이 시점에 CDC 파이프라인이 사라지고, JVM 튜닝 책임이 사라지고, snapshot 저장소 비용이 사라진다. 운영팀의 한숨 한 줄이 줄어든다.

이 전체 흐름의 미덕은 **언제든 돌아갈 수 있다**는 점이다. 각 단계에서 문제가 발견되면 이전 단계로 돌아가서 다시 보강한다. 한 번에 다 옮기려다 실패하면 전체 검색 기능이 무너지는 빅뱅과는 위험도가 다르다. 큰 변화를 작게 쪼개는 운영 미덕은 검색 마이그레이션에서도 그대로 통한다.

### 한국어 검색 운영을 위한 작은 팁 모음

마지막으로, 한국어 검색을 PG로 풀 때 자주 만나는 작은 결정들을 한 묶음으로 정리해두자.

- **동의어 사전**. 사용자가 "DB"라고 쳤을 때 "데이터베이스"가 같이 잡혀야 한다. PGroonga는 동의어 처리를 위한 별도 사전 메커니즘을 제공한다. ES의 synonym filter만큼 풍부하진 않지만 기본은 풀 수 있다. 사전을 운영할 인력이 없다면, 애플리케이션 레벨에서 검색어 확장을 하는 길도 있다(검색어를 LLM에 한 번 보내 동의어 목록을 받아 OR로 묶는 식).
- **stop word**. "을", "를", "이", "가" 같은 조사는 검색에 무의미하다. PGroonga의 N-gram 토크나이저는 이 조사들을 그대로 인덱스에 넣지만 검색 시 매칭 결과에 큰 영향을 주진 않는다. 더 깔끔하게 빼고 싶다면 형태소 분석기 기반 토크나이저로 가야 한다.
- **검색어 정규화**. 사용자가 "Postgres", "postgres", "POSTGRES"를 같은 의미로 친다는 가정은 안전한 출발점이다. PGroonga 인덱스는 기본적으로 case-insensitive 매칭을 지원한다. 한영 혼용 검색어의 경우 한자·일본어가 섞인다면 normalizer 옵션을 한 번 검토하자.
- **검색 결과 캐싱**. 인기 검색어는 결과 캐시로 풀 부담을 줄인다. application 레벨이든 Redis든, 검색 한 줄에 들어가는 비용이 크다면 캐시 한 층을 두는 게 단순하고 효과적이다.
- **검색 로그 분석**. zero-result 검색어를 매주 한 번 들여다보자. 사용자가 무엇을 찾으려 했는데 못 찾았는지가 보인다. 그 목록이 동의어 사전 보강의 가장 좋은 입력이다. 검색 품질 개선의 출발점은 결국 사용자 검색어 로그다.
- **인덱스 모니터링**. `pg_stat_user_indexes`로 인덱스가 실제로 쓰이는지 확인하자. 만들어놓고 안 쓰이는 검색 인덱스가 있다면 그건 디스크와 write 부하의 낭비다. 21장에서 다룰 모니터링 체계 안에 검색 인덱스도 같이 포함하는 편이 낫다.

이런 작은 결정들이 모여 "PG로도 검색이 잘 된다"의 실체를 만든다. 도구 한 줄 깐다고 검색이 자동으로 좋아지지는 않는다는 게 ES든 PG든 마찬가지인 진실이다. 다만 PG의 길에서는 도구 한 벌이 덜 들어간다는 점이 큰 차이다.

## 마무리

검색 한 줄을 위해 또 다른 클러스터를 띄우는 비용은 생각보다 크다. JVM 튜닝, CDC 파이프라인, 일관성 회의실, 야간 호출 — 그 모든 게 검색 한 줄에 따라붙는다. PostgreSQL 진영은 그 부담을 줄이려는 카드들을 한 묶음으로 갖춰 왔다. 내장 tsvector/tsquery로 영문 풀텍스트를 무료로 받고, pg_trgm으로 fuzzy 매칭을 보완한다. 한국어가 들어오는 순간 PGroonga가 답이 되고, BM25 품질의 랭킹이 필요하면 pg_search나 pg_textsearch를 얹는다. 17의 access method API 개선이 이 경쟁의 무대를 만들었고, 그 결과 PG 사용자는 더 좋은 선택지를 더 많이 갖게 됐다.

기억해두자. 도구 선택의 출발점은 **검색이 우리 비즈니스의 무엇인가**라는 질문이다. 검색이 본업이라면 dedicated 엔진의 정당성은 여전히 살아 있다. 검색이 본업이 아닌데 또 한 벌의 인프라를 짊어지고 있다면, PG 안으로 가져오는 길을 한 번 진지하게 검토해보자. 데이터가 한 군데에 살고, 트랜잭션이 한 곳에서 끝나고, 운영팀의 한숨이 줄어든다 — 그것만으로도 의사결정의 무게는 작지 않다.

다음 11장에서는 또 다른 "PG 안에 통째로 들어와 있는" 카드를 펼친다. 공간 데이터를 다루는 PostGIS다. 검색에서 본 패턴 — "외부 dedicated를 세울 것인가, PG 익스텐션으로 끝낼 것인가" — 이 GIS 영역에서는 어떻게 답해왔는지를 같이 따라가보자.
