# 12장. 벡터 DB와 RAG 백엔드 — pgvector·pgvectorscale

OpenAI든 Anthropic이든, 임베딩 API를 한 번 호출해본 적이 있다고 해보자. 텍스트를 던지면 1,536차원이든 3,072차원이든 float 배열이 돌아온다. 그 숫자 다발을 어디엔가 쌓아두어야 한다. 그래야 다음 질문이 들어왔을 때 "비슷한 것"을 꺼내 LLM에 던져줄 수 있다. RAG라는 이름이 붙기 전에도 이 구조는 똑같았다.

자, 그러면 그 "어딘가"는 어떤 모양이어야 할까?

요즘은 이름 있는 벡터 DB가 한 트럭이다. Pinecone, Weaviate, Qdrant, Milvus, Chroma, Vespa, LanceDB. 광고는 화려하고 SDK는 친절하다. 그런데 잠깐 멈춰서 생각해보자. 우리 서비스의 사용자 정보, 주문 내역, 문서 메타데이터는 어디에 있는가? 거의 대부분의 경우 PostgreSQL 같은 RDB에 있다. 그렇다면 임베딩만 따로 다른 DB에 빼두는 일이 정말 그렇게 자연스러운가?

같은 트랜잭션 안에서 "주문을 저장하면서 그 주문 설명의 임베딩도 같이" 쓸 수 있다면 무엇이 달라질까? 두 DB 사이의 일관성을 걱정하느라 outbox 패턴을 끌어들이고, 동기화가 깨질까봐 모니터링 알람을 만들고, 운영 중에 한쪽만 복구되는 사고를 상상하지 않아도 된다고 하면? 그것만으로도 한참 마음이 가벼워진다.

한 줄로 묻자. **dedicated 벡터 DB 대신 PostgreSQL을 쓰는 선은 어디까지인가.** 답을 내려놓기 전에, 우선 pgvector라는 익스텐션이 실제로 어떻게 생겼는지부터 만져보자. 그러고 나서 그 위에 얹는 pgvectorscale은 어디까지 밀어붙였는지, 벤치마크는 무엇을 말하고 무엇을 감추는지, 알고리즘의 진짜 배경은 무엇인지를 차례로 보고, 마지막에 의사결정표를 그리자.

## 12.1 pgvector — HNSW와 IVFFlat

pgvector는 PostgreSQL에 `vector`라는 데이터 타입과 그 위의 ANN(Approximate Nearest Neighbor) 인덱스를 더해주는 익스텐션이다. 설치는 한 줄이다.

```sql
CREATE EXTENSION vector;
```

그러면 곧바로 이런 테이블을 만들 수 있다.

```sql
CREATE TABLE documents (
  id           bigserial PRIMARY KEY,
  source_id    bigint REFERENCES sources(id),
  chunk_no     int,
  body         text,
  metadata     jsonb,
  embedding    vector(1536),    -- OpenAI text-embedding-3-small
  created_at   timestamptz DEFAULT now()
);
```

여기서 멈춰 잠깐 음미해보자. 이 테이블은 그냥 우리가 늘 쓰던 PostgreSQL 테이블이다. `source_id`로 외래 키를 걸고, `metadata`는 jsonb고, `embedding`이 1,536차원짜리 float 배열일 뿐이다. 인덱스도 평소처럼 건다.

```sql
CREATE INDEX ON documents (source_id);
CREATE INDEX ON documents USING gin (metadata jsonb_path_ops);
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
```

마지막 줄이 핵심이다. **HNSW(Hierarchical Navigable Small World)** 인덱스를 코사인 거리 연산자로 건다. 쿼리는 더 단순하다.

```sql
SELECT id, body
  FROM documents
 WHERE source_id = $1
 ORDER BY embedding <=> $2   -- $2 = 질의 임베딩
 LIMIT 10;
```

`<=>`가 코사인 거리 연산자다. 그밖에 `<->`(L2 거리), `<#>`(내적의 음수)도 있다. SQL은 평범하다 못해 심심하다. 그런데 그 심심함이 바로 핵심이다. 이 한 줄짜리 ORDER BY로, 우리는 RDB가 늘 해주던 모든 것 — JOIN, WHERE, GROUP BY, 트랜잭션, 권한, 백업, point-in-time 복구 — 을 그대로 누리면서 벡터 유사도 검색을 얹은 셈이다.

### HNSW가 무엇을 하는가

HNSW는 이름이 무섭게 생겼지만 직관은 단순하다. "고속도로와 동네 골목을 함께 가진 지도"라고 생각하면 이해하기 쉽다.

상상해보자. 서울에서 부산까지 가야 한다. 모든 사거리를 다 들르며 가면 평생 못 도착한다. 그래서 우리는 자연스럽게 큰 도로를 먼저 탄다. 고속도로로 대전쯤까지 빠르게 내려가고, 거기서 더 좁은 국도로 갈아타고, 마지막에는 동네 길로 들어선다.

HNSW의 그래프도 그렇게 생겼다. 가장 위 레이어에는 듬성듬성한 노드들이 멀리멀리 연결돼 있다. 한 번 점프하면 멀리 간다. 아래로 내려갈수록 노드가 빽빽해지고, 연결은 짧아진다. 검색은 위에서 시작해 아래로 내려간다. 위층에서 빠르게 "대략 어디쯤"을 잡고, 아래층에서 동네를 뒤진다. 그래서 수백만 벡터 중에서도 수십~수백 노드만 들러봐도 "꽤 가까운" 답을 찾을 수 있다.

물론 "꽤 가까운"이라는 말이 마음에 걸린다. ANN은 말 그대로 근사다. 진짜 정답(exact nearest neighbor)을 보장하지 않는다. 대신 **recall@k**라는 지표를 둔다. "정답 후보 k개 중 진짜 정답 몇 퍼센트를 우리가 찾았느냐"다. recall 95%면 100번 검색했을 때 진짜 1등이 평균 95번은 포함됐다는 뜻이다. RAG 용도라면 보통 95~99%면 충분하다. 어차피 LLM이 후보 여러 개를 보고 추론하니까.

### HNSW의 파라미터 — m과 ef_construction, ef_search

HNSW에는 세 개의 손잡이가 있다. 처음 보면 헷갈리지만, 한 번 잡으면 평생 쓴다.

- `m`: 각 노드가 가질 평균 연결 수. 보통 16. 크면 recall이 좋아지지만 인덱스가 커지고 빌드가 느려진다.
- `ef_construction`: 인덱스를 만들 때 후보를 얼마나 넓게 둘러보느냐. 보통 64~200. 크면 빌드는 느린데 인덱스 품질이 좋아진다.
- `ef_search`: 검색할 때 후보를 얼마나 둘러보느냐. 기본 40. 크면 recall은 올라가는데 latency가 올라간다.

```sql
CREATE INDEX ON documents
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 200);

-- 쿼리 시에는 세션 단위로 조정
SET hnsw.ef_search = 100;
```

`ef_search`를 세션 단위로 바꿀 수 있다는 점이 실전에서 묘하게 편하다. 평소엔 40으로 빠르게 답하다가, 정밀도가 필요한 배치 작업에서는 200으로 끌어올린다. RDB의 익숙한 트레이드오프와 다르지 않다.

### IVFFlat은 왜 살아 있는가

pgvector에는 HNSW 말고도 IVFFlat이 있다. **IVFFlat(Inverted File with Flat compression)** 은 다른 결의 알고리즘이다.

상상해보자. 도시를 100개 구역으로 나눈다. 새로운 주소를 받으면 가장 가까운 구역의 중심점을 먼저 찾고, 그 구역 안에서만 진짜 가까운 이웃을 찾는다. 100개 중심점만 비교하고 그 안에서 다시 작은 후보군만 보면, 전체를 다 보지 않아도 된다.

IVFFlat은 빠르게 만들 수 있다. 인덱스 빌드가 HNSW보다 훨씬 가볍다. 그리고 자료가 자주 바뀌지 않는 경우, 메모리 사용량이 더 작다. 단, 데이터가 늘어날수록 구역 재학습이 필요해서 점차 recall이 떨어진다.

그렇다면 우리는 어느 쪽을 골라야 할까? 거의 모든 RAG 워크로드에서는 **HNSW가 첫 선택**이다. 데이터가 계속 추가되는 환경에서 안정적이고, 같은 recall에서 latency가 더 짧다. IVFFlat은 "벡터가 한 번 쌓이면 거의 안 바뀌고, 인덱스 빌드 시간을 매우 짧게 가져가야 하는" 특수한 경우에나 의미가 있다. 입문서에서는 둘을 나란히 두지만, 실무에서는 HNSW부터 시작하자.

### 거리 함수는 어떻게 고르나 — cosine, L2, inner product

pgvector는 세 가지 거리 연산자를 제공한다. 각각 인덱스 옵션 클래스가 다르다.

- `<=>` 코사인 거리 — `vector_cosine_ops`
- `<->` L2(유클리드) 거리 — `vector_l2_ops`
- `<#>` 음의 내적 — `vector_ip_ops`

어느 쪽을 골라야 할지 헷갈리는 게 정상이다. 임베딩 모델의 학습 방식이 답을 알려준다. OpenAI의 `text-embedding-3-*`, Cohere의 `embed-*`, BGE·E5 같은 오픈 모델은 거의 모두 **유사도 = 코사인**을 가정해 학습됐다. 그러니 특별한 이유가 없으면 `<=>`(코사인)을 쓰자. 모델이 출력을 이미 정규화(L2 norm = 1)한 상태라면 cosine과 inner product가 수학적으로 같다. 다만 PG 인덱스 입장에서는 연산자가 다르면 다른 클래스다. 인덱스 만들 때 쿼리에서 쓸 연산자와 같은 클래스를 골라야 한다는 점을 잊지 말자.

```sql
-- 잘못된 조합 (인덱스가 안 쓰인다)
CREATE INDEX ON documents USING hnsw (embedding vector_l2_ops);
SELECT ... ORDER BY embedding <=> $1 ...;   -- 코사인 연산자, 인덱스 미사용

-- 올바른 조합
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
SELECT ... ORDER BY embedding <=> $1 ...;
```

EXPLAIN으로 확인하지 않으면 한참 뒤에야 "왜 이렇게 느리지?"하고 발견하게 된다. 그제서야 인덱스가 한 번도 안 쓰였다는 걸 알게 되면, 정말 찜찜하다. 운영에 올리기 전에 한 번 EXPLAIN을 돌려보는 편이 낫다.

### RAG 백엔드의 실전 스키마

좀 더 현실적인 RAG 백엔드 스키마를 함께 그려보자. 단순한 `documents` 테이블 한 장이 아니라, 실제 운영을 가정한 모양이다.

```sql
-- 원문 문서
CREATE TABLE sources (
  id            bigserial PRIMARY KEY,
  external_id   text UNIQUE,        -- Notion/Confluence/Drive의 원본 id
  title         text NOT NULL,
  url           text,
  author        text,
  org_id        bigint NOT NULL,    -- 권한 분리
  language      text DEFAULT 'ko',
  published_at  timestamptz,
  fetched_at    timestamptz DEFAULT now(),
  raw_content   text                -- 원문 (감사·재청크용)
);

-- 청크와 임베딩
CREATE TABLE chunks (
  id            bigserial PRIMARY KEY,
  source_id     bigint NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  chunk_no      int NOT NULL,
  body          text NOT NULL,
  tokens        int,
  model         text NOT NULL,      -- 'text-embedding-3-small' 등
  model_version text NOT NULL,      -- 모델 교체 추적
  embedding     vector(1536),
  metadata      jsonb DEFAULT '{}',
  created_at    timestamptz DEFAULT now(),
  UNIQUE (source_id, chunk_no, model, model_version)
);

CREATE INDEX ON chunks (source_id);
CREATE INDEX ON chunks USING gin (metadata jsonb_path_ops);
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 200);
```

여기 몇 가지 작은 선택이 들어 있다. 함께 살펴보자.

- `sources`와 `chunks`를 분리했다. 같은 문서를 다른 청크 크기로 다시 임베딩할 일이 생긴다. 원문이 한 군데 있어야 그게 가능하다.
- `model`과 `model_version`을 컬럼으로 뒀다. `text-embedding-3-small`에서 `-large`로 갈아탈 때, 같은 청크에 새 모델의 벡터를 추가해 비교 테스트를 돌릴 수 있다.
- `org_id`를 `sources`에 뒀다. 멀티 테넌트 환경에서 RLS(Row Level Security)로 조직별 접근 분리를 거는 자리다. dedicated 벡터 DB에서 이런 권한 분리는 별도 인덱스 분리거나 자체 ACL 설계가 필요한데, PG는 그냥 익숙한 RLS다.
- HNSW 인덱스의 `m`과 `ef_construction`을 명시했다. 디폴트는 `m=16, ef_construction=64`인데, RAG에서 96% 이상의 recall이 필요하면 `ef_construction`을 200쯤으로 올리는 편이 낫다.

### 한 트랜잭션 안에서 임베딩까지

이 스키마의 진가는 INSERT 시점에 드러난다.

```python
# 의사 코드 — 한 트랜잭션 안에서 원문·청크·임베딩이 함께 커밋된다.
async with pool.transaction() as tx:
    source_id = await tx.fetchval(
        """
        INSERT INTO sources (external_id, title, url, author, org_id, raw_content)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (external_id)
          DO UPDATE SET title = EXCLUDED.title,
                        raw_content = EXCLUDED.raw_content,
                        fetched_at = now()
        RETURNING id
        """,
        ext_id, title, url, author, org_id, raw,
    )

    chunks = chunk_text(raw, max_tokens=500, overlap=50)
    embeddings = await embedding_client.embed(chunks)  # OpenAI 배치 호출

    await tx.executemany(
        """
        INSERT INTO chunks (source_id, chunk_no, body, tokens,
                            model, model_version, embedding, metadata)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ON CONFLICT (source_id, chunk_no, model, model_version)
          DO UPDATE SET body = EXCLUDED.body,
                        embedding = EXCLUDED.embedding
        """,
        [(source_id, i, c.text, c.tokens,
          'text-embedding-3-small', '2024-01',
          embeddings[i], {'lang': lang})
         for i, c in enumerate(chunks)],
    )
```

여기서 한 번 멈춰서 음미하자. 이 코드의 핵심은 `INSERT INTO sources`와 `INSERT INTO chunks`가 **같은 트랜잭션 안**에서 일어난다는 점이다. 임베딩 API 호출이 실패하면 sources도 롤백된다. chunks INSERT가 일부만 성공하고 나머지가 실패해도, 전부 롤백된다. 동기화 대상이 PG 한 군데뿐이라, "한쪽만 성공한" 어중간한 상태가 존재할 수 없다.

dedicated 벡터 DB를 쓰면 이 단순함이 사라진다. 원문은 PG에 INSERT, 임베딩은 Pinecone에 upsert. 둘 사이의 일관성을 위해 outbox 테이블을 두고, 백그라운드 워커로 재시도하고, 실패 카운트를 모니터링한다. 잘 만들면 동작은 한다. 그러나 운영 중 한쪽 DB만 복구되는 사고를 한 번이라도 겪어보면, 그 뒷맛이 두고두고 찜찜하다. 만들기와 운영의 부담이 만만치 않다.

### 메타 필터와 결합된 벡터 검색

쿼리 시간도 보자. 진짜 RAG 쿼리는 "벡터 유사도 ORDER BY"만으로 끝나지 않는다. 권한과 시간 범위, 출처 필터가 거의 빠짐없이 함께 들어온다.

```sql
SELECT
    c.id,
    c.body,
    s.title,
    s.url,
    1 - (c.embedding <=> $1) AS similarity
FROM chunks c
JOIN sources s ON s.id = c.source_id
WHERE
    s.org_id = $2                              -- 권한
    AND s.published_at >= now() - interval '180 days'  -- 시간 범위
    AND c.metadata @> '{"lang": "ko"}'         -- jsonb 필터
    AND c.model = 'text-embedding-3-small'     -- 같은 모델끼리만
ORDER BY c.embedding <=> $1
LIMIT 20;
```

이 쿼리가 PG 안에서 자연스러운 이유는 단순하다. **JOIN, jsonb 필터, B-tree 범위 조건이 다 같은 옵티마이저의 손바닥 안**이기 때문이다. dedicated 벡터 DB도 메타 필터를 흉내내긴 하지만, jsonb 같은 임의 구조의 필터는 인덱스 활용이 제한적인 경우가 많다. PG는 그냥 평범한 SQL이다.

여기서 한 가지 주의할 점이 있다. **메타 필터의 선택도가 매우 높으면**(전체 1억 행 중 1만 행만 통과) HNSW 인덱스를 우회하고 메타 인덱스로 좁힌 뒤 거리 정렬하는 게 더 빠를 수 있다. 반대로 메타 필터가 느슨하면 HNSW 인덱스로 후보를 먼저 좁히는 게 낫다. PG 옵티마이저가 항상 최적의 선택을 하진 않아서, `EXPLAIN ANALYZE`로 확인하고 필요하면 `SET enable_indexscan` 같은 힌트로 조정해야 할 때도 있다. 처음 운영에 올릴 때 한 번 점검하고 가자.

### pgvector 0.7 이후의 변화 — halfvec와 binary 양자화

pgvector도 한가하지 않다. 0.7부터는 `halfvec`(반정밀도 float16)와 `bit`(이진 양자화)를 지원하기 시작했다. 1,536차원짜리 float32 벡터는 한 행에 6KB가 넘는다. 1억 개면 600GB. 디스크와 메모리가 휘청거린다. 그런데 halfvec으로 절반(3KB), 이진으로 1/32(192바이트)까지 줄일 수 있다.

```sql
ALTER TABLE documents
  ADD COLUMN embedding_half halfvec(1536);

CREATE INDEX ON documents
  USING hnsw (embedding_half halfvec_cosine_ops);
```

손실은? 의외로 작다. 좋은 임베딩 모델일수록 정보가 차원 전반에 잘 분산돼 있어, 정밀도를 줄여도 코사인 유사도의 순위는 잘 보존된다. 다음 절에서 보겠지만, pgvectorscale의 SBQ(Statistical Binary Quantization)는 이 직관을 한 발 더 밀어붙인 것이다.

여기까지가 pgvector의 본체다. 작고, 평범하고, PostgreSQL스럽다. "이게 다라고?" 하는 의문이 들 수 있다. 그렇다면 다음을 보자. pgvector 위에 얹는 pgvectorscale이 어디까지 가는지를.

## 12.2 pgvectorscale — DiskANN + Statistical Binary Quantization

pgvectorscale은 Timescale(현 Tiger Data)이 만든 익스텐션이다. pgvector를 부정하지 않는다. pgvector의 `vector` 타입을 그대로 받아, 그 위에 **새로운 인덱스 두 가지**와 **새로운 양자화 한 가지**를 더한다. 이름하여 **StreamingDiskANN** 인덱스와 **SBQ(Statistical Binary Quantization)** 다.

설치는 pgvector와 짝을 이룬다.

```sql
CREATE EXTENSION vector;
CREATE EXTENSION vectorscale CASCADE;

CREATE INDEX ON documents
  USING diskann (embedding);
```

평소처럼 인덱스 한 줄이다. 그런데 그 한 줄 뒤에는 마이크로소프트 리서치의 DiskANN 논문이 통째로 들어 있다. 잠깐 살펴보자.

### DiskANN이 왜 디스크인가

HNSW에는 한 가지 큰 약점이 있다. 인덱스가 **메모리에 다 올라가야** 빠르다. 5,000만 벡터면 그래프 노드와 임베딩 합쳐서 100GB가 훌쩍 넘는다. 우리가 RAM 128GB짜리 인스턴스를 한참 쓰다가, 데이터가 1억 개로 늘면 어떻게 될까? RAM 256GB 인스턴스로 갈아타거나, 인덱스를 잘게 쪼개거나, 결국은 dedicated 벡터 DB로 마이그레이션하는 회의를 잡게 된다. 어느 쪽이든 난감한 선택지다. 한숨이 나온다.

DiskANN은 그 한숨을 정조준한 알고리즘이다. **그래프를 디스크에 두고도 SSD 한두 번 읽기로 답을 내자**가 발상이다. 어떻게? Vamana라는 그래프를 만든다. 각 노드의 이웃을 단순히 가까운 것만 두지 않고, **"방향이 다양한" 이웃**을 골라 그래프 지름을 짧게 만든다. 그래서 노드 몇 개만 거쳐도 멀리 도달한다. 그러면 디스크에서 읽어와야 하는 페이지 수가 극적으로 줄어든다.

원 논문은 NeurIPS 2019에서 발표됐다. 1억 개 벡터에 대해 단일 머신에서 95% recall, 5ms로 답한다는 결과를 보였다. 인덱스 빌드도 SSD를 활용해 메모리 한계 너머의 데이터셋을 다룬다. 마이크로소프트 빙(Bing)에서 검색 인프라로 쓴다.

### StreamingDiskANN — 새 데이터를 받아들이는 DiskANN

원 DiskANN은 정적이었다. 즉 한 번 빌드하면 잘 바뀌지 않는 데이터셋용이다. 그런데 우리 RAG는 매일 문서가 추가된다. 새 문서가 들어올 때마다 인덱스를 다시 빌드하는 건 끔찍한 일이다.

pgvectorscale의 **StreamingDiskANN**은 이걸 풀었다. 인덱스에 노드를 점진적으로 추가·갱신할 수 있게 한다. 마치 B-tree에 INSERT가 들어와도 인덱스가 깨지지 않고 적절히 정렬되는 것처럼, StreamingDiskANN도 새 벡터를 받아 그래프에 적절히 끼워 넣는다. 그래서 OLTP 워크로드와도 어울린다. 트랜잭션 안에서 INSERT가 일어나고, 같은 트랜잭션 안에서 검색 인덱스에 즉시 반영된다. 별도 동기화 잡을 돌릴 일이 없다.

### SBQ — 통계로 압축하는 양자화

두 번째 무기는 **Statistical Binary Quantization**이다. 이름은 어렵지만 아이디어는 깔끔하다.

이진 양자화 자체는 단순하다. 각 차원의 값이 0보다 크면 1, 아니면 0으로 표기한다. 1,536차원이면 1,536 비트 = 192바이트로 줄어든다. float32(6KB)의 1/32다. 그런데 이렇게 거칠게 잘라내면 정보가 너무 많이 날아간다. 검색 품질이 곤두박질친다.

SBQ는 여기에 통계 한 줌을 더한다. 모든 벡터의 차원별 분포를 보고, **차원마다 적절한 임계값**을 따로 잡는다. 어떤 차원은 평균이 +0.1쯤이고 또 어떤 차원은 -0.2 근처에 몰려 있다. 단순히 0을 기준으로 자르면 한쪽으로 쏠리는데, 각 차원의 중앙값(혹은 그에 준하는 통계 기반 임계값)으로 자르면 정보가 훨씬 잘 보존된다. 거기에 "양자화된 비트 비교로 1차 후보를 빠르게 좁히고, 원본 벡터로 최종 순위만 다시 매기는"(re-ranking) 2단계 검색을 더하면, 디스크 I/O와 메모리는 1/32로 줄고 recall은 95% 이상을 지킨다.

요약하면 이렇다.

> **pgvectorscale = pgvector + DiskANN(메모리 너머) + SBQ(저장공간 1/32)**

```sql
-- 인덱스 옵션은 자동으로 합리적 디폴트가 적용된다.
-- 필요할 때만 명시적으로 손본다.
CREATE INDEX ON documents
  USING diskann (embedding)
  WITH (
    storage_layout = 'memory_optimized',  -- SBQ 활용
    num_neighbors = 50,
    search_list_size = 100,
    max_alpha = 1.2
  );
```

손잡이가 좀 더 많지만, 사실 디폴트로도 잘 나온다. 처음에는 `CREATE INDEX ... USING diskann (embedding);` 한 줄로 시작하자. 운영하면서 EXPLAIN과 메트릭을 보고 조정하자.

### 그래서 pgvector만 쓸 때와 무엇이 다른가

세 가지로 정리할 수 있다.

1. **데이터가 RAM을 넘어서도 동작한다.** 1억 벡터를 128GB RAM 한 대로 검색해야 하는 상황이 생각보다 자주 온다. pgvectorscale은 거기서 살아남는다.
2. **저장공간 자체가 줄어든다.** SBQ로 임베딩 열의 메모리 풋프린트가 1/32까지. 클라우드에서 RDS 한 단계 더 작은 인스턴스를 쓸 수 있다는 의미다.
3. **PostgreSQL 메타데이터·필터와 자연스럽게 결합한다.** dedicated 벡터 DB가 따로 흉내 내야 했던 "벡터 + 메타 필터" 조합 쿼리가, 그냥 SQL의 `WHERE`다.

### 운영 중 무엇을 보아야 하나

pgvectorscale을 운영에 올린 뒤 일주일은 다음 네 가지를 본다. 너무 많지도 너무 적지도 않다.

- **인덱스 크기 vs 테이블 크기.** `\di+` 또는 `pg_relation_size('chunks_embedding_idx')`. 인덱스가 RAM을 얼마나 차지하는지 감을 잡는다. SBQ를 켜면 메모리 풋프린트가 극적으로 줄어드는 게 여기서 보인다.
- **buffer hit ratio.** `pg_stat_user_indexes`의 `idx_blks_hit / (idx_blks_hit + idx_blks_read)`. SSD 읽기에 의존하는 DiskANN은 이 비율이 100%가 아니어도 정상이다. 다만 너무 낮으면(가령 50% 미만) RAM이 작거나 동시성이 높다는 신호다.
- **검색 latency 분포.** p50, p95, p99를 따로 본다. p99가 튀면 한 번씩 디스크에서 콜드 페이지를 읽는다는 뜻이다. 워크로드에 따라 정상이지만, p99가 SLA를 넘으면 인덱스 옵션을 조정한다.
- **autovacuum과 인덱스 빌드 큐.** 대량 INSERT 직후엔 인덱스 갱신과 vacuum이 백로그를 만든다. `pg_stat_progress_create_index`로 빌드 진행을 본다.

```sql
-- 인덱스 크기 한 줄
SELECT pg_size_pretty(pg_relation_size('chunks_embedding_idx'));

-- 인덱스 사용 통계
SELECT
    indexrelname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE indexrelname LIKE '%embedding%';

-- 빌드 진행 (긴 인덱스 빌드 중에)
SELECT * FROM pg_stat_progress_create_index;
```

이 네 가지를 보면 "지금 이 인덱스가 행복한가, 아닌가"가 보인다. 행복하지 않으면 옵션을 조정한다. `num_neighbors`를 키우거나, `search_list_size`를 줄이거나, 인스턴스 RAM을 한 단계 올리거나. 평범한 PG 튜닝이다.

### "그럼 처음부터 pgvectorscale을 쓰면 되는가"

자연스러운 질문이다. 답은 "거의 그렇다, 다만 환경 확인이 먼저다"다. 매니지드 PG 중 일부는 pgvectorscale을 지원하지 않는다(특히 AWS Aurora는 2026.05 기준 미지원으로 보고됨 — 사실 확인 필요). pgvector는 거의 모든 매니지드가 기본 지원이지만, pgvectorscale은 익스텐션 추가 권한이 있는 셀프 호스팅이나 Tiger Cloud, Supabase 같은 LLM 친화 매니지드에서 더 자유롭다.

운영 환경이 pgvectorscale을 받아주면 처음부터 DiskANN으로 시작하자. 데이터가 작더라도 손해는 거의 없다. 받아주지 않으면 pgvector HNSW로 시작하고, 5M쯤에서 데이터를 옮길 인프라를 검토하자. 어느 쪽이든 PG라는 한 지붕 안이다.

여기까지 보면 "그러면 거의 안 갈아탈 이유가 없는데?"라는 인상이 든다. 그 직감을 벤치마크가 뒷받침해주는지, 아니면 광고일 뿐인지 다음 절에서 따져보자.

## 12.3 벤치마크 — 75% 절감과 11.4배의 진실

벡터 DB 마케팅 자료를 한 번이라도 본 적이 있다면, "X배 빠르다", "Y% 저렴하다"라는 막대그래프에 익숙할 것이다. 그런데 그 막대 뒤에는 늘 작은 글씨로 조건이 적혀 있다. 우리도 그 작은 글씨를 같이 읽어보자.

### Tiger Data의 두 벤치마크

pgvectorscale을 만든 Tiger Data(전 Timescale)가 공개한 두 벤치마크는 자주 인용된다.

**벤치마크 A — pgvectorscale vs Pinecone.** 50M 벡터, 99% recall.

- pgvectorscale: **p95 latency 28ms**.
- Pinecone(s1 pod): p95 latency 784ms.
- 동일 처리량 기준 인프라 비용 **75% 절감**.

**벤치마크 B — pgvectorscale vs Qdrant.** 50M 벡터, 99% recall.

- pgvectorscale: **471 QPS**.
- Qdrant: 41 QPS.
- 즉 **11.4배** 처리량.

수치만 보면 압도적이다. 그런데 우리, 잠깐 의심해보자. 벤치마크의 작성자는 누구인가? Tiger Data다. 자기들이 만든 익스텐션이다. 비교 대상은 Pinecone과 Qdrant의 특정 구성이다. 다른 구성으로 잡으면 결과가 어떻게 달라지는지는 그 글에 다 적혀 있지 않다.

물론 그렇다고 해서 이 벤치마크가 거짓이라는 뜻은 아니다. Tiger Data는 데이터셋과 코드, 인스턴스 타입을 공개했다. 그 위에서 재현 가능한 숫자다. 다만 우리가 가져갈 결론은 "pgvectorscale이 모든 dedicated 벡터 DB를 11.4배 압도한다"가 아니라, **"많은 RAG 워크로드에서 pgvectorscale이 dedicated와 같은 급의 성능을 낸다"**가 안전하다.

같은 맥락의 다른 측정도 있다. pgvector 단독, HNSW로 5M 벡터 이하 규모에서는 **95% recall에서 p95 20ms 미만**이 통상 보고되는 수치다. 5M짜리 임베딩이라면 RAG 입장에서 결코 작은 코퍼스가 아니다. 회사 전체 위키, 고객지원 문서, 제품 매뉴얼을 다 모아도 보통 1M 이하다. 즉 **"중규모 RAG는 pgvector 단독으로 충분히 빠르다"** 가 일반화 가능한 첫 결론이다.

### "비용 75% 절감"의 분해

비용 절감의 정체는 셋으로 쪼개진다.

1. **인프라가 PG 한 덩어리로 통합된다.** Pinecone이나 Qdrant Cloud를 따로 결제할 필요가 없다. 이미 운영 중인 PostgreSQL 클러스터에 인덱스 하나 더 얹는 셈이다.
2. **데이터 이중화가 사라진다.** 임베딩의 원본인 문서/메타데이터를 PG에 두고, 임베딩만 따로 Pinecone에 둘 때 우리는 같은 데이터를 두 번 산다. 한 군데로 합치면 그만큼이 사라진다.
3. **운영 부담이 줄어든다.** 백업·복구·모니터링·HA 도구가 PG용으로 하나만 있으면 된다. 사람 시간이 가장 비싸다.

이 세 가지를 더하면 "75% 절감"이 그리 과한 표현이 아닐 수도 있다. 다만 우리 회사의 실제 구성에서는 비율이 달라진다. 가령 dedicated 벡터 DB는 Pinecone 무료 티어로 쓰고 있었고, PG는 따로 매니지드를 쓰고 있었다면? 그 경우 합쳐도 큰 차이가 안 난다. 마케팅 수치를 그대로 가져다 사장님께 보고하기 전에, 우리 회사 청구서를 한 번 들춰보자.

### 벤치마크에 잘 안 잡히는 것들

수치 비교는 단순한 게 매력인데, 정작 운영을 결정짓는 요인들은 잘 안 잡힌다.

- **메타데이터 필터 결합.** "최근 30일 이내, 한국어, 특정 카테고리"의 필터를 걸고 벡터 검색을 하는 게 RAG의 현실이다. dedicated 벡터 DB는 이걸 자체 인덱스로 풀어야 한다. PG는 jsonb GIN, B-tree, partial index를 자유롭게 조합한다. 단순 ANN QPS만 보면 dedicated가 가끔 더 좋아 보여도, 필터 결합으로 들어가면 PG가 역전하는 경우가 많다.
- **트랜잭션 일관성.** 새 문서 INSERT가 commit되는 순간 검색 결과에 반영돼야 하는가? Pinecone은 eventual이고, pgvector/pgvectorscale은 즉시다.
- **재인덱싱·스키마 변경.** 임베딩 모델을 바꿀 때(예: text-embedding-3-small → -large) dedicated DB는 보통 통째로 새 인덱스로 마이그레이션해야 한다. PG는 새 컬럼을 ALTER로 추가하고, 백필하고, 인덱스를 새로 빌드하면 된다. 친숙한 절차다.
- **장애 대응.** PG의 백업·PITR·logical replication이 그대로 통한다. dedicated 벡터 DB는 자기 백업 도구를 따로 익혀야 한다.

이런 운영적 차이는 막대그래프에 안 그려진다. 하지만 6개월 운영해보면 "그 차이가 거의 전부였구나"를 깨닫게 된다.

### 그렇다면 dedicated가 빛나는 지점은 없는가

있다. 정직하게 말하자.

- **수억 개 벡터 + 수만 QPS + 복잡한 메타데이터 필터.** 이 조합이 동시에 들어오면, dedicated 벡터 DB가 분산·샤딩에 더 적극적이다. Pinecone, Qdrant, Vespa는 분산 검색이 기본 가정이다. PG에서도 Citus나 직접 샤딩으로 따라갈 수는 있지만, 만들기와 운영의 난도가 만만치 않다.
- **벡터 외의 데이터가 거의 없는 워크로드.** 가령 "유사 이미지 검색만 하는 단일 마이크로서비스"가 있고, 메타데이터가 거의 없고, 다른 시스템과 트랜잭션 일관성을 잡을 일이 없으면 dedicated를 따로 쓰는 게 깔끔하다.
- **벡터 DB 특화 기능이 결정적인 경우.** 가령 Qdrant의 payload-aware filtering이나 Vespa의 텐서 연산 같은 고급 기능을 적극 활용해야 한다면, PG에서 흉내내는 게 번거롭다.

요약하면 이렇다. **"중규모 + 메타데이터 풍부 + 기존 PG 인프라"라면 거의 항상 PG가 답이다. "초대규모 + 단순 메타 + 신규 인프라"라면 dedicated를 검토할 가치가 있다.** 의사결정의 결정선은 12.5에서 더 구체적으로 그어보자.

### 우리 워크로드로 직접 측정하기 — 작은 절차

남의 벤치마크는 결국 남의 데이터다. 우리 데이터에서, 우리 인프라에서, 우리 패턴으로 측정하지 않으면 결정의 근거로 쓰기 어렵다. 다행히 PG 환경에서 ANN 벤치마크를 돌리는 절차는 단순하다. 며칠이면 답을 낸다.

1. **데이터셋을 준비한다.** 운영 데이터의 부분 집합 또는 무작위 샘플. 보통 100K~1M 임베딩이면 1차 스크리닝에 충분하다. 정확한 비교를 원하면 풀 사이즈로.
2. **인덱스 옵션을 두세 개 만든다.** 가령 HNSW `(m=16, ef=64)`, HNSW `(m=32, ef=200)`, DiskANN 디폴트. 같은 컬럼에 동시에 만들 수도 있다.
3. **쿼리 집합을 준비한다.** 운영 로그에서 실제 질의 임베딩 1,000~10,000개를 뽑는다. 합성 데이터보다 훨씬 가치 있다.
4. **`pgbench`나 `wrk`로 동시성을 변화시키며 측정한다.** 1, 4, 16, 64 동시 클라이언트. 각 케이스에서 p50, p95, p99, recall@10을 기록.
5. **recall은 별도로 측정한다.** 같은 쿼리를 `WHERE` 절 없이 인덱스 미사용(sequential scan)으로 돌려 "정답 top-10"을 얻고, 인덱스 결과와 교집합 비율을 본다.

```sql
-- recall 측정용 (인덱스 우회)
SET enable_indexscan = off;
SET enable_bitmapscan = off;
SELECT id FROM chunks ORDER BY embedding <=> $1 LIMIT 10;
-- ↑ 이 결과를 정답으로 잡고
RESET enable_indexscan;
RESET enable_bitmapscan;
SELECT id FROM chunks ORDER BY embedding <=> $1 LIMIT 10;
-- ↑ 이 결과와 비교
```

며칠 측정해보면 "우리에게는 이 인덱스 옵션이 가장 잘 맞는다"가 손에 잡힌다. 마케팅 자료의 X배·Y배 대신, 우리 숫자로 의사결정을 한다. 그게 진짜 자신감이다.

그 전에, 우리가 쓰는 알고리즘이 어디에서 왔는지 한 번 짚고 가자. HNSW와 DiskANN은 같은 ANN이지만 발상이 다르다. 둘의 배경을 알면 트레이드오프가 한층 또렷해진다.

## 12.4 알고리즘 배경 — HNSW와 DiskANN의 발상

알고리즘 논문 두 편을 안 읽었다고 RAG를 못 만들지는 않는다. 그러나 그 둘이 왜 그렇게 생겼는지 짧게라도 알고 가면, 인덱스 파라미터를 만질 때 헤매지 않는다. 잠깐 책장을 펼치듯이 살펴보자.

### HNSW — 작은 세상 그래프의 계층화 (Malkov & Yashunin, 2016/2020)

HNSW의 원형은 NSW(Navigable Small World)다. 사회 연결망의 "작은 세상" 현상에서 영감을 받았다. 누구나 6단계만 거치면 누구와도 연결된다는 그 직관이다. 각 노드를 적절히 연결해두면, 무작위 출발점에서 시작해 그리디 탐색만으로도 가까운 목표에 빠르게 도달한다.

문제는 NSW만으로는 데이터가 커지면 탐색 깊이가 늘어진다는 점이었다. Malkov과 Yashunin이 2016년 arXiv(1603.09320)에 올린 HNSW는 이 한계를 **계층(Hierarchy)** 으로 풀었다. 위층에는 노드 일부만, 아래로 갈수록 더 많은 노드. 위층 연결은 길고, 아래층 연결은 짧다. 검색은 위에서 아래로. 직관은 "지하철 + 마을버스"와 비슷하다. 위층에서 지하철로 빠르게 동네 근처까지, 아래층에서 버스로 골목까지. 평균 탐색 횟수가 데이터 크기의 로그 수준으로 유지된다.

논문의 핵심 기여는 두 가지다. (1) 계층 구조를 확률적으로 자연스럽게 만드는 삽입 알고리즘, (2) 이웃 선택 시 단순 거리뿐 아니라 **방향 다양성**을 함께 고려해 그래프 지름을 줄이는 휴리스틱. 이 두 가지 덕분에 HNSW는 같은 메모리 예산에서 다른 그래프 기반 ANN을 압도하는 결과를 냈고, 이후 사실상 표준이 됐다. 2020년에는 IEEE TPAMI에 정식 출판됐다.

그래서 pgvector 인덱스를 만들 때 `m`(이웃 수)과 `ef_construction`(빌드 후보 폭)을 만지는 일은, 사실 이 휴리스틱의 강도를 조절하는 일이다. `m`을 키운다는 건 더 빽빽한 그래프, 더 좋은 recall, 더 큰 메모리. 한쪽이 좋아지면 다른 쪽이 나빠지는 흔한 트레이드오프다. 신비할 게 없다.

### DiskANN — SSD 시대를 위한 그래프 (Jayaram Subramanya et al., NeurIPS 2019)

마이크로소프트 리서치의 DiskANN은 다른 각도에서 출발했다. **"메모리에 다 못 올리는 데이터셋에서 ANN을 잘 하려면?"** 이 질문이었다. 마이크로소프트 Bing은 수십억 개의 임베딩을 다뤄야 했다. 그걸 다 RAM에 올리는 비용이 천문학적이라, 어떻게든 SSD로 내려야 했다.

DiskANN의 그래프 이름은 **Vamana**다. HNSW와 마찬가지로 그래프 ANN이지만, 단일 레이어 평면 그래프다. 대신 이웃 선택에 **alpha**라는 파라미터를 둔다. alpha > 1이면 "이미 가까운 노드와 비슷한 방향에 있는 후보"를 일부러 덜 뽑는다. 그래서 같은 노드의 이웃들이 사방으로 흩어져 있게 된다. 결과적으로 그래프 지름이 짧아지고, 한 번 점프하면 멀리 간다. 디스크에서 페이지를 적게 읽어도 되는 구조다.

여기에 **PQ(Product Quantization)** 같은 압축 코드와 **2단계 검색**을 결합한다. 일단 압축된 코드로 후보 집합을 메모리에서 빠르게 좁히고, 최종 순위는 디스크의 원본 벡터로 정확히 매긴다. 한 쿼리당 SSD 읽기 횟수가 한 자릿수에 머문다. NeurIPS 2019에서 발표될 당시, 단일 머신으로 1억 벡터에 5ms 안에 95% recall을 달성한 결과는 충격적이었다.

pgvectorscale의 StreamingDiskANN은 이 Vamana를 PostgreSQL에 이식하면서, "동적 INSERT/UPDATE를 받아도 그래프가 무너지지 않게" 만들었다. SBQ는 PQ 계열의 발상을 단순화·실용화한 양자화다. 즉 pgvectorscale의 진보는 갑자기 튀어나온 마법이 아니다. **2019년 NeurIPS 논문이 RDB 환경에 안착한 결과**다.

### 서베이 한 편 — 2023년 이후의 풍경

ANN 알고리즘은 매년 새로 나온다. 다 따라가긴 어렵다. 흐름을 잡고 싶다면 Han 외(2023)의 서베이(arXiv:2310.14021)가 출발점으로 쓸 만하다. 그래프 기반(HNSW, Vamana, NSG), 트리 기반(Annoy), 해시 기반(LSH), 양자화 기반(IVF-PQ, ScaNN)을 한자리에 비교한다. 결론은 단순하다. **그래프 기반이 일반적으로 가장 강하고, 양자화와 결합한 디스크 그래프가 대규모에서 가장 효율적이다.** 이게 지금 우리가 pgvector/pgvectorscale에서 만나는 풍경이다.

### 알고리즘을 알면 무엇이 달라지는가

세 가지가 달라진다.

1. **인덱스 파라미터의 의미가 보인다.** `ef_search`를 늘리면 왜 latency가 증가하는지, `num_neighbors`를 키우면 왜 인덱스 크기가 늘어나는지 머릿속에 그림이 그려진다.
2. **"왜 이 양자화가 멀쩡한가"를 안심하고 받아들일 수 있다.** SBQ로 1/32 압축한다는 말이 비현실적으로 들리지만, 차원 단위 통계 기반 임계값 + 2단계 re-ranking이라는 구조를 알면 자연스럽다.
3. **다음 세대 익스텐션이 나왔을 때 빠르게 평가할 수 있다.** 어차피 다음 ANN도 그래프 + 양자화 + 디스크 친화 셋의 어디쯤에 위치할 것이다.

기술서가 알고리즘 디테일에 빠지면 지루해진다. 우리에게 필요한 만큼만 알고, 다시 의사결정으로 돌아오자. 그렇다면 우리 서비스는 어디부터 시작해야 할까?

## 12.5 의사결정 — 어디까지 PG로 가고, 어디부터 dedicated인가

우리가 12장을 펼친 진짜 이유는 결국 이 절이다. 신규 서비스든 기존 시스템 보강이든, "임베딩을 어디에 둘 것인가"를 결정해야 한다. 막연하게 dedicated를 끌어들이지도 말고, 무조건 PG에 욱여넣지도 말자. 결정선을 같이 그어보자.

### 결정에 영향을 주는 다섯 가지 축

벡터 백엔드 선택에 실제로 영향을 주는 변수는 그리 많지 않다. 다섯 가지면 거의 다 설명된다.

1. **벡터 개수.** 100K, 1M, 10M, 100M의 자릿수가 핵심이다.
2. **메타데이터 필터의 복잡도.** "단일 카테고리 필터" vs "5개 이상의 jsonb 조건 + 시간 범위 + 권한 필터"의 차이.
3. **쓰기 패턴.** 거의 정적인가, 분당 수백 건 INSERT가 들어오는가, 트랜잭션 안에서 다른 테이블과 함께 커밋돼야 하는가.
4. **기존 인프라.** PG가 이미 운영의 중심에 있는가, 아니면 신규 인프라를 자유롭게 잡을 수 있는가.
5. **운영 팀 역량.** PG DBA가 있는가, 새로운 벡터 DB의 운영 노하우를 익힐 여유가 있는가.

이 다섯 축을 따라 의사결정표를 그릴 수 있다.

### 의사결정표

| 상황 | 추천 백엔드 | 이유 |
|------|-------------|------|
| 벡터 ≤ 1M, 메타 필터 단순, 기존 PG 있음 | **pgvector** 단독 (HNSW) | 인덱스 1줄로 끝. 추가 운영 비용 거의 0. |
| 벡터 1M~10M, 메타 필터 풍부, 기존 PG 있음 | **pgvector + pgvectorscale** | HNSW로도 가능하지만, DiskANN으로 헤드룸 확보. 메타 결합 쿼리에 강함. |
| 벡터 10M~100M, 메타 필터 풍부, 동시성 보통 | **pgvectorscale** (DiskANN + SBQ) | RAM 한계 너머도 SSD로 흡수. 비용 대비 성능 우수. |
| 벡터 100M+, 단순 메타, 수만 QPS, 신규 인프라 가능 | **dedicated**(Qdrant·Vespa·Pinecone) | 분산·샤딩이 기본 가정. PG에서 흉내내려면 운영 코스트 큼. |
| 벡터 다양 + 트랜잭션 일관성 필수 | **pgvector(+scale)** | "임베딩 INSERT가 비즈니스 트랜잭션과 같은 ACID로 묶여야 한다"는 요구가 있으면 사실상 PG가 유일한 답. |
| 임베딩 모델을 자주 바꿀 가능성 | **pgvector(+scale)** | ALTER로 컬럼 추가, 백필, 재인덱싱이 익숙한 절차. |
| 벡터 외에는 데이터 없음, 단일 마이크로서비스 | **dedicated 검토** | PG를 새로 들이는 게 더 무거울 수 있음. |
| 매니지드 PG 사용 중 | **익스텐션 지원 여부 확인 후** PG | AWS RDS는 pgvector 지원, pgvectorscale은 Aurora 미지원(2026.05 기준 — 사실 확인 필요). Tiger Cloud는 둘 다 기본. |
| 한국어 검색이 핵심, 키워드·벡터 하이브리드 필요 | **pgvector + pg_search/PGroonga** | 같은 PG 안에서 BM25와 벡터를 결합할 수 있는 게 결정타. 10장 참고. |

이 표의 결정선은 절대적인 게 아니다. 회사 사정마다 위로도 아래로도 움직인다. 그러나 "막연한 두려움" 대신 "구체적인 기준"으로 회의에 들어갈 수 있다는 것만으로도 가치가 있다.

### "10M 이하 + 단일 필터"라는 기준은 어디서 나왔나

업계의 경험적 합의가 이 자리에 모인다. Tiger Data, Neon, Crunchy Data 같은 매니지드 PG 벤더의 운영 가이드, 그리고 Reddit r/PostgreSQL과 HackerNews의 실무자 토론을 종합하면 패턴이 보인다. **10M 벡터까지는 pgvector 단독으로도 무리 없고, 50M까지는 pgvectorscale로 충분히 커버되며, 100M을 넘기면서 동시성·필터 복잡도가 동시에 올라가면 dedicated를 진지하게 검토하기 시작한다.**

물론 이 경계는 매년 위로 올라가고 있다. 작년 10M이던 경계가 올해 50M이 된 식이다. pgvector·pgvectorscale의 메이저 업데이트와 PostgreSQL 17/18의 메모리·I/O 개선이 그 흐름을 떠받친다. 즉 우리가 "지금은 dedicated가 필요해 보인다"고 판단해 시작했더라도, 6개월쯤 뒤에 같은 워크로드가 pgvectorscale로 충분히 처리될 수 있다. 그래서 dedicated를 도입하더라도, **메타데이터 원본은 PG에 두는** 구조가 안전하다. 나중에 합칠 때 데이터 이전이 부담이 작다.

### 우리 회사에 적용하기 — 짧은 체크리스트

회의실에 들어가기 전 다섯 줄 체크리스트를 들고 가자.

- 우리가 다룰 벡터 수의 6개월 후, 24개월 후 예측은 자릿수가 어디까지인가?
- 메타데이터 필터는 정말로 복잡한가, 아니면 카테고리 한두 개 수준인가?
- 임베딩 INSERT가 비즈니스 트랜잭션과 같이 묶일 필요가 있는가?
- 기존 PG 운영팀이 있는가? 매니지드라면 pgvectorscale을 지원하는가?
- dedicated를 쓴다면 한 명 이상이 그 도구의 백업·HA·튜닝까지 책임질 수 있는가?

이 다섯 줄에 답하다 보면, "사실 우리는 dedicated가 필요하지 않다"는 결론에 도달하는 경우가 의외로 많다. 그게 잘못된 결론이 아니다. 가장 단순한 구조가 가장 오래 살아남는다는 평범한 사실의 한 사례일 뿐이다.

### 자주 만나는 안티패턴

의사결정 직후 실제로 만들기 시작하면, 흔히 같은 함정에 빠진다. 몇 가지를 미리 짚고 가자.

**안티패턴 1: 청크 크기를 너무 작게 자른다.** 100토큰 단위로 자르면 청크 수가 폭증하고 인덱스가 비대해진다. 그렇다고 너무 크면 의미 단위가 흐려진다. 보통 400~800토큰, overlap 50~100토큰이 한국어·영어 모두에서 안정적이다. 청크 크기는 도메인에 따라 실험하자. 답은 데이터마다 다르다.

**안티패턴 2: 한 테이블에 여러 모델의 임베딩을 컬럼으로 나란히 둔다.** `embedding_v1`, `embedding_v2`, `embedding_v3` 같은 컬럼이 늘어나기 시작한다. 한 인덱스만 봐도 끔찍한 일이다. 위에서 본 스키마처럼 `(model, model_version)` 컬럼으로 행을 나누는 편이 깔끔하다. 마이그레이션도 쉽다.

**안티패턴 3: 메타 필터 없이 ANN만 던진다.** "top-100을 가져와서 애플리케이션에서 필터링"하는 패턴은 recall이 무너진다. 가령 한국어 문서만 보고 싶은데, top-100에 한국어가 5개밖에 없으면 답이 빈약해진다. WHERE 절을 SQL로 함께 거는 편이 낫다. PG의 옵티마이저가 잘 처리한다.

**안티패턴 4: 임베딩 INSERT를 동기로 처리한다.** 사용자 요청 안에서 OpenAI API를 호출해 임베딩을 받고 INSERT까지 끝낸다? 응답 latency가 500ms를 넘기는 게 흔하다. 임베딩 생성은 큐로 미루고(13장의 pgmq나 LISTEN/NOTIFY 패턴이 잘 어울린다), 사용자에게는 즉시 응답을 주자. RAG의 검색 자체는 빠르지만, "쓰기"는 비동기로 두는 게 자연스럽다.

**안티패턴 5: vacuum과 reindex를 잊는다.** 임베딩 컬럼은 6KB짜리 큰 값이 즐비한 행이다. UPDATE가 많으면 bloat가 빠르게 쌓인다. autovacuum 설정을 챙기고, 가끔 `REINDEX CONCURRENTLY`로 HNSW 인덱스를 다시 빌드하면 검색 품질이 회복된다. 24·6장에서 다룬 vacuum 노하우가 여기서도 그대로 쓰인다.

**안티패턴 6: dedicated를 너무 일찍 들인다.** "1년 뒤에 1억 벡터가 될지도 모르니까 미리 Pinecone부터 깔자"는 결정을 자주 본다. 90%의 경우 그 1년 뒤 1억은 오지 않거나, 와도 그때의 pgvectorscale로 충분히 처리된다. 미리 빌린 비용과 운영 부담은 그대로 남는다. **YAGNI**(You Aren't Gonna Need It)는 벡터 백엔드에도 통한다. 일단 PG로 시작하고, 한계가 진짜로 보이면 그때 옮기자.

### 한국 사례 한 줄 — 카카오스타일 Bedrock

카카오스타일의 Amazon Bedrock 기반 생성형 AI 사례는 25장에서 본격적으로 다루지만, 결론만 미리 흘리자면 이렇다. **운영 중인 PG 위에 분석 자산과 임베딩을 함께 두고, LLM이 그것을 활용하는 패턴.** 정확히 우리가 이 장에서 따라온 흐름이다. 한국에서도, 글로벌에서도, "벡터 DB를 따로 들이지 않고 PG에 합친다"가 점차 디폴트가 돼 가고 있다는 신호다. (자세한 의사결정 디테일은 25.2 참고.)

그렇다면 그 흐름은 어디까지 갈까? 마지막 절에서 2026년의 풍경을 살짝 들춰보자.

## 12.6 2026 트렌드 — relational + vector + search + analytics의 한 지붕

10년 전 우리는 "polyglot persistence"라는 말을 자주 들었다. RDB는 트랜잭션을, NoSQL은 문서를, Elasticsearch는 검색을, Cassandra는 시계열을, Redis는 캐시를. 각 도구가 자기 영역의 최강자라는 신화. 그래서 시스템 아키텍처 다이어그램은 점점 더 복잡해졌고, 한 트랜잭션이 여러 DB를 가로지르면서 일관성 문제가 곳곳에서 터졌다.

2026년의 분위기는 분명히 다른 방향이다. **"한 RDB 안에 다 들어가는 것"** 이 다시 미덕이 됐다. PostgreSQL이 그 흐름의 중심이다.

### 다섯 가지 워크로드의 통합

PostgreSQL이 통합하고 있는 워크로드 다섯 가지를 한자리에 놓아보자.

- **벡터.** pgvector, pgvectorscale (이 장).
- **전문 검색.** pg_search, PGroonga, pg_textsearch (10장).
- **공간.** PostGIS (11장).
- **분석/OLAP.** Citus, TimescaleDB, ParadeDB·pg_duckdb (15장).
- **이벤트/큐.** LISTEN/NOTIFY, pgmq, logical decoding (13장).

각 영역에서 "PG가 그 dedicated 솔루션을 100% 대체하느냐?"고 물으면 답은 "아니오"다. Elasticsearch의 모든 기능, Pinecone의 모든 SLA, Kafka의 모든 throughput을 다 못 따라간다. 그러나 **"우리 회사가 진짜로 필요한 만큼"의 90~95%는 PG가 다 한다.** 그리고 그 90%를 한 DB에 두는 가치가 우리가 한동안 너무 쉽게 잊고 있던 것이다.

### "Postgres is eating the database world" — Pigsty의 진단

Pigsty의 유명한 글 제목 그대로다. 익스텐션 생태계가 폭발했다. PostGIS, pgvector, TimescaleDB, Citus, pg_search, pg_duckdb, pgmq, pg_cron — 이 모든 게 같은 PG 서버에 공존한다. 같은 백업으로 보호되고, 같은 모니터링으로 관측되고, 같은 권한 시스템으로 통제된다. 새 DB를 추가하지 않고, 새 익스텐션을 추가한다.

이 흐름은 우리 일상에 두 가지를 가져온다.

1. **시스템 다이어그램이 다시 단순해진다.** 두 박스 — PG와 애플리케이션 — 가 핵심이고, 나머지는 보조다. 다이어그램이 단순해지는 만큼 사고도 단순해진다.
2. **DBA의 가치가 다시 올라간다.** RDB가 모든 워크로드의 중심이면, PG를 깊게 아는 사람의 영향력이 곧 시스템 전체의 안정성이다.

### 매니지드 벤더의 경주

이 흐름을 가장 빠르게 좇는 건 매니지드 PG 벤더들이다.

- **AWS RDS/Aurora.** pgvector 기본 지원. 다만 pgvectorscale은 2026.05 기준 Aurora 미지원으로 보고됨(사실 확인 필요). 매니지드 선택 시 익스텐션 지원 목록 확인이 결정적이다.
- **Google AlloyDB.** vector indexing을 자체 columnar 엔진과 결합. 분석 + 벡터 통합 사례.
- **Tiger Cloud.** pgvectorscale의 발원지답게 모든 익스텐션이 기본 탑재.
- **Neon.** pgvector 기본, branching으로 임베딩 모델 교체 실험 친화적.
- **Supabase.** pgvector, pgmq, pg_cron, RLS의 조합으로 LLM 앱 백엔드 표준 같은 위치.

매니지드를 고를 때 "그 벤더가 pgvectorscale, pg_search, pgmq, pg_cron, pg_partman 같은 핵심 익스텐션을 지원하는가"가 결정적인 기준이 된다. 지원 목록은 자주 바뀌니, 도입 직전에 한 번 더 확인하자.

### PostgresML — PG 안에서 임베딩 생성까지

지금까지의 모든 코드는 "임베딩은 OpenAI API에서 받아 PG에 INSERT"를 전제로 했다. 그런데 한 걸음 더 갈 수도 있다. **PostgresML**은 임베딩 생성 자체를 PG 안에서 한다.

```sql
-- 카탈로그 수준의 짧은 예시 (사용 패턴만)
CREATE EXTENSION pgml;

UPDATE chunks
SET embedding = pgml.embed(
    transformer => 'intfloat/e5-small-v2',
    text => body
)::vector
WHERE embedding IS NULL;
```

이 한 줄이 하는 일은 작지 않다. 외부 API 호출도, 별도 워커 프로세스도 없이, SQL이 임베딩을 만들어 INSERT한다. 같은 트랜잭션 안에서 텍스트와 벡터가 함께 만들어진다.

물론 트레이드오프가 있다. PG 서버에 GPU가 필요하거나, 무거운 모델은 CPU로 느리다. 자체 호스팅이 가능한 환경에서는 빛나지만, 매니지드 PG에서는 활용이 제한적이다. 본격 활용 사례는 후속 보강이 필요한 영역이지만, "PG 안에서 임베딩까지 다 끝내는" 그림이 가능하다는 점은 기억해두자. 통합의 방향은 거기까지 이어진다.

### "벡터 DB"라는 카테고리가 한 발 작아진다

이 흐름이 시사하는 바는 명확하다. **"벡터 DB"라는 카테고리 자체가 점차 좁아진다.** 5년 전에 "NewSQL"이라는 카테고리가 PG·MySQL의 진화에 흡수되며 작아진 것과 비슷한 풍경이다. 벡터 인덱스는 "그 자체로 DB"라기보다 "RDB의 한 인덱스 타입"이 돼 간다. 마치 GIS가 그랬듯이.

물론 dedicated 벡터 DB가 사라진다는 뜻은 아니다. 초대규모·고급 기능·특화 워크로드에서는 dedicated가 계속 빛난다. 다만 그 영역이 좁아지고 명확해진다는 의미다. 그리고 "기본값"의 자리는 점점 PG에 양보된다.

### 우리 팀의 다음 한 걸음

이 장을 닫으며, 다음 주 월요일에 무엇을 해볼지를 정해보자.

- 신규 RAG 프로토타입이라면 **pgvector 단독으로 시작**하자. 인덱스 한 줄, SQL 한 줄로 동작 확인. 이게 모든 시작이다.
- 이미 운영 중이고 벡터가 5M을 넘기 시작했다면 **pgvectorscale 인덱스를 같은 컬럼에 추가**해 EXPLAIN으로 차이를 측정하자. 무중단 전환이 가능한 구조다.
- dedicated 벡터 DB를 검토 중이라면 **메타데이터 원본은 PG에 남기는 구조**로 설계하자. 6개월 뒤에 흡수할 수 있는 길을 열어두는 게 안전하다.
- 매니지드 PG를 평가 중이라면 **익스텐션 지원 목록을 가장 먼저** 보자. 가격표가 아니다.
- 한국어 RAG라면 **벡터 + BM25 하이브리드 검색**을 처음부터 가정하고 설계하자. 10장의 pg_search/PGroonga 절을 함께 펼쳐 두자.

### 기억해두자

길게 돌아왔지만, 한 장의 핵심은 두 줄로 정리된다.

> **임베딩을 굳이 다른 DB에 빼두지 말자. 우리가 잘 아는 PostgreSQL 안에서, 익숙한 ACID와 SQL과 백업으로 같이 묶어두자.**
>
> **그 한계가 어디인지 막연히 두려워하지 말자. 5M까지는 pgvector, 50M까지는 pgvectorscale, 그 너머에서 비로소 dedicated를 검토하자.**

이게 2026년의 벡터 DB 선택에 대한 가장 정직한 한 줄 가이드다. 5년 뒤에는 경계가 더 위로 올라가 있을 가능성이 높다. 그리고 그때 우리가 후회하지 않으려면, 지금부터 데이터의 중심을 한 PG 안에 모아두는 편이 낫다.

다음 13장에서는 같은 발상의 또 다른 적용을 본다. "메시지 버스도 굳이 따로 두지 말자." Kafka를 들이기 전, PostgreSQL이 어디까지 메시지 시스템 흉내를 낼 수 있는지를 살펴볼 차례다. LISTEN/NOTIFY, logical decoding, pgmq의 삼중주가 의외로 멀리까지 데려간다. 잠시 숨을 고르고 넘어가자.
