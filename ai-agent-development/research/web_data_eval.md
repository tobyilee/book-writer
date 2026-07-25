<!-- 검색 시점: 2026-07-25 기준 -->

# 웹 리서치 (web-researcher #2): 데이터·벡터 DB·임베딩·평가·가드레일

**담당 축:** `[축 3]` 데이터·벡터 DB / `[축 4]` 평가·모니터링·가드레일 / `[축 6]` 용도별 조합의 원재료
**담당 아님:** 프레임워크·런타임·MCP (web-researcher #1)
**대상 독자:** LLM API는 써봤지만 에이전트를 직접 설계·배포·운영해본 적 없는 백엔드/풀스택 개발자·테크리드

## 이 문서의 검증 방법론 (fact-checker 필독)

버전·라이선스·활동 신호 열은 **2026-07-25에 실제 API 호출로 확인한 값**이다. 확인 경로는 셋뿐이다.

- `gh api repos/{owner}/{repo}/releases/latest` → `tag_name`, `published_at`
- `gh api repos/{owner}/{repo}` → `license.spdx_id`, `pushed_at`, `stargazers_count`, `archived`
- `https://pypi.org/pypi/{pkg}/json` → `.info.version` / `https://registry.npmjs.org/{pkg}/latest` → `.version`

확인하지 못한 셀은 **추측하지 않고 `미확인`으로 남겼다.** 문서 하단 "미확인 항목 목록"에 전부 모아두었다. 본문에서 이 셀을 근거로 단정을 쓰면 안 된다.

> **가장 위험한 두 열에 대한 경고**
> 1. **벤치마크 점수** — 대부분의 리더보드(MTEB, SWE-bench, GAIA)는 JS 렌더링이라 정적 fetch로 점수를 못 읽었다. **Terminal-Bench 2.0만 실제 점수를 확보**했다. 나머지는 전부 `미확인`이다. 기억으로 채우지 마라.
> 2. **임베딩 가격** — OpenAI는 **공식 페이지 두 곳이 서로 다른 값을 말한다**(아래 자료 3 참조). Cohere는 현재 가격 페이지에서 토큰 단가를 아예 걷어냈다.

---

## 표 1. 벡터 DB·검색 엔진 `[축 3]`

| 도구 | 카테고리 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 확인일 |
|------|---------|---------------------|-------------|---------|------------|----------|--------|
| pgvector | Postgres 확장 | `v0.8.5` (git tag) | https://github.com/pgvector/pgvector | `NOASSERTION` (GitHub API 판정; 실제 라이선스 문구는 미확인) | 이미 쓰는 Postgres에 벡터 타입·인덱스를 더한다 — 새 인프라가 없다 | pushed 2026-07-11, ★22,338. `releases/latest`가 404 (릴리스 미등록, 태그만 운영) | 2026-07-25 |
| pgvectorscale | pgvector 성능 확장 | `0.9.0` (2025-11-04) | https://github.com/timescale/pgvectorscale/releases/tag/0.9.0 | `PostgreSQL` | pgvector에 StreamingDiskANN 인덱스를 얹는다 | pushed 2026-04-30, ★3,097. **릴리스 20개월·푸시 3개월 정체 — 구버전 정보일 수 있음** | 2026-07-25 |
| Qdrant | 전용 벡터 DB | `v1.18.3` (2026-07-17) | https://github.com/qdrant/qdrant/releases/tag/v1.18.3 | `Apache-2.0` | Query API의 `prefetch` 기반 다단계 쿼리 + RRF/DBSF 융합 | pushed 2026-07-25 (당일), ★33,573 | 2026-07-25 |
| Weaviate | 전용 벡터 DB | `v1.38.6` (2026-07-21) | https://github.com/weaviate/weaviate/releases/tag/v1.38.6 | `BSD-3-Clause` | `alpha` 하나로 키워드↔벡터 비중을 조절하는 하이브리드 | pushed 2026-07-25 (당일), ★16,648 | 2026-07-25 |
| Milvus | 전용 벡터 DB | `v2.6.21` (2026-07-24) | https://github.com/milvus-io/milvus/releases/tag/v2.6.21 | `Apache-2.0` | 다중 벡터 필드 동시 ANN + 내장 BM25로 sparse 임베딩 자동 생성 | pushed 2026-07-25 (당일), ★45,373. PyPI `pymilvus` 3.0.0 (2026-05-07) | 2026-07-25 |
| Pinecone | 매니지드 벡터 DB | `미확인 (managed service, 버전 개념 없음)` | https://docs.pinecone.io/guides/index-data/indexing-overview | 상용 (프로프라이어터리) | 서버리스 인덱스 — 운영 부담이 0에 가장 가깝다 | 매니지드. 가격은 표 5 | 2026-07-25 |
| Chroma | 임베디드→서버 벡터 DB | `1.5.9` (2026-05-05) | https://github.com/chroma-core/chroma/releases/tag/1.5.9 | `Apache-2.0` | 프로토타입에서 `pip install`만으로 시작하는 최단 경로 | pushed 2026-07-25 (당일), ★28,873. PyPI `chromadb` 1.5.9 / npm `chromadb` 3.5.0 | 2026-07-25 |
| LanceDB | 임베디드 벡터 DB | Python SDK `0.34.0` (2026-07-02). **GitHub `releases/latest`는 `v0.32.0-beta.3` (프리릴리스)** | https://pypi.org/pypi/lancedb/json · https://github.com/lancedb/lancedb/releases | `Apache-2.0` | Lance 컬럼 포맷 위의 임베디드 DB — 객체 스토리지에 바로 얹힌다 | pushed 2026-07-25, ★10,988. 안정 태그 없이 beta 채널로 굴러가는 릴리스 관행 (`v0.33.0-beta.0`이 최신 태그) | 2026-07-25 |
| Turbopuffer | 매니지드 (객체 스토리지 네이티브) | `미확인 (managed service, 버전 개념 없음)` | https://turbopuffer.com/docs | 상용 | "object-storage native" — 캐시되면 인메모리급, 안 되면 훨씬 싸다 | 매니지드. 공식 문서 주장: "4T+ documents, 10M+ writes/s, 25k+ queries/s" | 2026-07-25 |
| Vespa | 검색+ML 플랫폼 | `v8.719.5` (2026-07-07) | https://github.com/vespa-engine/vespa/releases/tag/v8.719.5 | `Apache-2.0` | 검색·랭킹·ML 추론을 한 엔진에서 — 가장 무겁고 가장 강력 | pushed 2026-07-25 (당일), ★7,029 | 2026-07-25 |
| Elasticsearch | 검색 엔진 (+벡터) | `v9.4.4` (2026-07-21) | https://github.com/elastic/elasticsearch/releases/tag/v9.4.4 | `NOASSERTION` (Elastic License 계열 — SPDX 미판정) | retriever 문법 + RRF로 lexical/vector 하이브리드 | pushed 2026-07-25, ★77,597 | 2026-07-25 |
| OpenSearch | 검색 엔진 (+벡터) | `3.7.0` (2026-06-09) | https://github.com/opensearch-project/OpenSearch/releases/tag/3.7.0 | `Apache-2.0` | Elasticsearch의 Apache-2.0 포크 — 라이선스가 선택 이유 | pushed 2026-07-24, ★13,374 | 2026-07-25 |
| Redis (RediSearch) | 인메모리 (+벡터) | `v2.10.31` (2026-06-17) | https://github.com/RediSearch/RediSearch/releases/tag/v2.10.31 | `NOASSERTION` (RSAL 계열 — SPDX 미판정) | 이미 캐시로 쓰는 Redis에 벡터 인덱스를 겸업 | pushed 2026-07-24, ★6,191 | 2026-07-25 |
| MongoDB Atlas Vector Search | 매니지드 문서 DB (+벡터) | `미확인 (managed service, 버전 개념 없음)` | https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/ | 상용 | 문서 DB 안에서 HNSW/ENN — 최대 8,192차원, 양자화 지원 | 매니지드 | 2026-07-25 |
| sqlite-vec | SQLite 확장 | `v0.1.9` (2026-03-31) | https://github.com/asg017/sqlite-vec/releases/tag/v0.1.9 | `Apache-2.0` | 단일 파일 SQLite에 벡터 검색 — 서버가 아예 없다 | pushed 2026-05-18, ★7,929. **4개월 정체 + 0.1.x 대 버전** | 2026-07-25 |
| FAISS | 라이브러리 (DB 아님) | `v1.14.3` (2026-06-13) | https://github.com/facebookresearch/faiss/releases/tag/v1.14.3 | `MIT` | ANN 알고리즘 라이브러리 — 영속성·필터·API는 직접 짠다 | pushed 2026-07-24, ★40,582. PyPI `faiss-cpu` 1.14.3 | 2026-07-25 |
| Typesense | 검색 엔진 (+벡터) | `v30.2` (2026-04-19) | https://github.com/typesense/typesense/releases/tag/v30.2 | `GPL-3.0` | 오타 허용 즉시 검색이 본업, 벡터는 겸업 | pushed 2026-07-18, ★26,354 | 2026-07-25 |
| Meilisearch | 검색 엔진 (+벡터) | `v1.50.0` (2026-07-20) | https://github.com/meilisearch/meilisearch/releases/tag/v1.50.0 | `NOASSERTION` (MIT 계열 — SPDX 미판정) | DX 우선 검색 엔진, 하이브리드 축 겸비 | pushed 2026-07-24, ★58,722 | 2026-07-25 |

**소계: 18개**

### 하이브리드 검색 구현이 갈리는 지점 (공식 문서 확인분) `[축 3]`

| 엔진 | 융합 방식 | 확인된 세부 | 1차 소스 |
|------|----------|-----------|---------|
| Qdrant | RRF, DBSF | RRF의 `k` 상수 조절 v1.16.0+, 가중 RRF v1.17.0+, Formula Queries v1.14.0+. DBSF는 "3-sigma extremes as endpoints"로 정규화. 리스코어 전용 벡터는 `m=0`으로 HNSW 비활성 권장 | https://qdrant.tech/documentation/concepts/hybrid-queries/ |
| Weaviate | Relative Score Fusion (v1.24부터 기본), Ranked Fusion | `alpha=1`은 순수 벡터, `alpha=0`은 순수 키워드. 키워드 측은 `BM25F`. **기본 alpha 값은 미확인** | https://docs.weaviate.io/weaviate/search/hybrid |
| Milvus | RRF Ranker, Weighted Ranker | 여러 벡터 필드에 ANN 동시 실행 후 병합. **내장 BM25로 텍스트 필드에서 sparse 임베딩 자동 생성**, `SPARSE_FLOAT_VECTOR` + `SPARSE_INVERTED_INDEX` | https://milvus.io/docs/multi-vector-search.md |
| Elasticsearch | RRF | retriever 문법으로 full-text와 vector 쿼리 랭킹 병합. Elastic Cloud Serverless·Elastic Stack 모두 GA. **`rank_constant`/`rank_window_size` 기본값은 해당 페이지에서 미확인** | https://www.elastic.co/docs/solutions/search/hybrid-search |

**책에 쓸 값:** 하이브리드는 "지원한다/안 한다"가 아니라 **융합 알고리즘이 무엇이고 조절 손잡이가 몇 개인가**로 갈린다. Weaviate는 `alpha` 하나(직관적), Qdrant는 prefetch+fusion+formula(표현력 높음), Milvus는 sparse 생성까지 엔진이 대신한다(BM25 파이프라인을 안 짜도 된다).

---

## 표 2. 임베딩 모델 `[축 3]`

**차원·컨텍스트·가격 전부 공식 모델/가격 페이지 확인분이다.** 확인 못 한 셀은 `미확인`.

| 모델 | 제공 형태 | 버전/세대 (2026-07-25 기준) | 차원 | 최대 입력 | 가격 (per 1M tokens) | 1차 소스 | 확인일 |
|------|---------|------------------------|------|---------|-------------------|---------|--------|
| `text-embedding-3-small` | OpenAI API | 3세대 | **1,536** (기본, `dimensions`로 축소 가능) — 가이드 원문: "the length of the embedding vector is `1536` for `text-embedding-3-small`" | **8,192 tokens** (가이드 명시) | **$0.02** (모델 카드) | 차원·입력: https://developers.openai.com/api/docs/guides/embeddings · 가격: https://developers.openai.com/api/docs/models/text-embedding-3-small | 2026-07-25 |
| `text-embedding-3-large` | OpenAI API | 3세대 | **3,072** (기본, 축소 가능) — 가이드 원문: "or `3072` for `text-embedding-3-large`" | **8,192 tokens** (가이드 명시) | **$0.13** (모델 카드). ⚠️ 가격 페이지는 $0.065라는 **포럼 보고**가 있음 — 자료 3 참조 | 차원·입력: https://developers.openai.com/api/docs/guides/embeddings · 가격: https://developers.openai.com/api/docs/models/text-embedding-3-large | 2026-07-25 |
| `text-embedding-ada-002` | OpenAI API | 2세대 (레거시) | `미확인` (가이드에 차원 명시 없음 — 흔히 1,536이라 하나 이번 세션 미확인) | **8,192 tokens** (가이드 명시) | `미확인` | https://developers.openai.com/api/docs/guides/embeddings | 2026-07-25 |
| `embed-v4.0` | Cohere API | v4 | **선택형: 256 / 512 / 1024 / 1536(기본)** | **128k tokens** | `미확인` (가격 페이지에 토큰 단가 없음 — Model Vault 시간당 요금만: Small $4.00/h·$2,500/mo, Medium $5.00/h·$3,250/mo) | https://docs.cohere.com/docs/cohere-embed · https://cohere.com/pricing | 2026-07-25 |
| `embed-english-v3.0` / `embed-multilingual-v3.0` | Cohere API | v3 (레거시) | 1,024 | 512 tokens | `미확인` | https://docs.cohere.com/docs/cohere-embed | 2026-07-25 |
| `embed-*-light-v3.0` | Cohere API | v3 light | 384 | 512 tokens | `미확인` | https://docs.cohere.com/docs/cohere-embed | 2026-07-25 |
| `voyage-4-large` | Voyage API | v4 | 1024(기본)/256/512/2048 | 32,000 tokens | **$0.12** | https://docs.voyageai.com/docs/embeddings · https://docs.voyageai.com/docs/pricing | 2026-07-25 |
| `voyage-4` | Voyage API | v4 | 1024(기본)/256/512/2048 | 32,000 tokens | **$0.06** | 동일 | 2026-07-25 |
| `voyage-4-lite` | Voyage API | v4 | 1024(기본)/256/512/2048 | 32,000 tokens | **$0.02** | 동일 | 2026-07-25 |
| `voyage-4-nano` | **오픈 웨이트** | v4 | 1024(기본)/256/512/2048 | 32,000 tokens | 자체 호스팅 (API 단가 `미확인`) | https://docs.voyageai.com/docs/embeddings | 2026-07-25 |
| `voyage-code-3` | Voyage API | 코드 특화 | 1024(기본)/256/512/2048 | 32,000 tokens | **$0.18** | 동일 | 2026-07-25 |
| `voyage-context-4` | Voyage API | 컨텍스트형 | `미확인` | `미확인` | **$0.12** | https://docs.voyageai.com/docs/pricing | 2026-07-25 |
| `gemini-embedding-2` | Google Gemini API | 2세대 | **유연: 128–3072 (권장 768/1536/3072)** | 8,192 tokens | **텍스트 $0.20** / 이미지 $0.45 / 오디오 $6.50 / 비디오 $12.00. Batch API는 "50% of the default Embedding price" | https://ai.google.dev/gemini-api/docs/embeddings · https://ai.google.dev/gemini-api/docs/pricing | 2026-07-25 |
| `gemini-embedding-001` | Google Gemini API | 1세대 | `미확인` | `미확인` | **텍스트 $0.15** | https://ai.google.dev/gemini-api/docs/pricing | 2026-07-25 |
| `jina-embeddings-v5-omni` | Jina API | v5 | Matryoshka (하한 `미확인`) | 32k tokens | `미확인` (무료 체험 10M tokens) | https://jina.ai/embeddings/ | 2026-07-25 |
| `jina-embeddings-v5-text` | Jina API / 오픈 | v5 | Matryoshka, **최소 32차원까지** | 8,192 tokens | `미확인`. small 677M / nano 239M 파라미터 | https://jina.ai/embeddings/ | 2026-07-25 |
| BGE (FlagEmbedding) | 오픈 모델·라이브러리 | `v1.4.0` (2026-04-22) | 모델별 상이 (`미확인`) | 모델별 상이 (`미확인`) | 자체 호스팅 | https://github.com/FlagOpen/FlagEmbedding/releases/tag/v1.4.0 | 2026-07-25 |
| ColBERT (late-interaction) | 오픈 라이브러리 | `v0.2.22` (2025-08-11) | late-interaction (단일 벡터 아님) | `미확인` | 자체 호스팅 | https://github.com/stanford-futuredata/ColBERT/releases/tag/v0.2.22 | 2026-07-25 |
| Nomic Embed | API / 오픈 | `미확인` (문서 URL 404) | `미확인` | `미확인` | `미확인` | 접근 실패 — "수집 한계" 참조 | 2026-07-25 |

**소계: 19개**

### 표 2-1. 리랭커 `[축 3]`

| 모델 | 제공 형태 | 버전 | 컨텍스트 | 가격 (per 1M tokens) | 1차 소스 | 확인일 |
|------|---------|------|---------|-------------------|---------|--------|
| `rerank-v4.0-pro` | Cohere API | v4 | `미확인` | `미확인` (Model Vault: Medium $5.00/h·$3,250/mo, Large $10.00/h·$6,500/mo) | https://docs.cohere.com/docs/rerank | 2026-07-25 |
| `rerank-v4.0-fast` | Cohere API | v4 | `미확인` | `미확인` | 동일 | 2026-07-25 |
| `rerank-v3.5` | Cohere API | v3.5 | **4,096 tokens** | `미확인` | 동일 | 2026-07-25 |
| `rerank-2.5` | Voyage API | v2.5 | `미확인` | **$0.05** | https://docs.voyageai.com/docs/pricing | 2026-07-25 |
| `rerank-2.5-lite` | Voyage API | v2.5 lite | `미확인` | **$0.02** | 동일 | 2026-07-25 |
| BGE reranker | 오픈 (FlagEmbedding) | `v1.4.0` (2026-04-22) | `미확인` | 자체 호스팅 | https://github.com/FlagOpen/FlagEmbedding | 2026-07-25 |
| `rerankers` (통합 래퍼) | 오픈 라이브러리 | `0.6.0` (2024-11-12) | — | 자체 호스팅 | https://github.com/AnswerDotAI/rerankers/releases/tag/0.6.0 | 2026-07-25 |

**소계: 7개** · ⚠️ `rerankers`는 릴리스 2024-11, 푸시 2025-12-20 — **약 20개월 정체, 구버전 정보일 수 있음**

### 표 2-2. MTEB 리더보드 현황 `[축 3]`

| 항목 | 확인된 사실 | 출처 |
|------|-----------|------|
| 패키지 버전 | `2.18.6` (2026-07-22 릴리스), PyPI `mteb` 2.18.6 (2026-07-22) | https://github.com/embeddings-benchmark/mteb/releases/tag/2.18.6 |
| 라이선스·활동 | `Apache-2.0`, pushed 2026-07-24, ★3,369 — **매우 활발** | `gh api` |
| 벤치마크 갈래 | MTEB(원본), MMTEB(2025년 도입 다국어 확장), MTEB(eng, v2) | README |
| 리더보드 위치 | https://huggingface.co/spaces/mteb/leaderboard | README |
| **모델별 점수** | **`미확인`** — HF Space가 JS/Docker 렌더링이라 정적 fetch 시 "Fetching metadata from the HF Docker repository..." 로딩 화면만 나옴 | 직접 fetch 실패 |
| 과적합·오염 논쟁 | README에는 **관련 경고 문구 없음** (없다는 사실 자체를 확인) | README |

> **책에 쓸 때:** MTEB 순위표의 특정 모델·점수를 본문에 박지 마라. 확인이 안 됐고, 순위는 주 단위로 바뀐다. "리더보드는 출발점이지 결론이 아니다 — 자기 도메인 데이터로 다시 재라"는 서술이 안전하고 실무적으로도 옳다.

---

## 표 3. eval·관측성 `[축 4]`

| 도구 | 카테고리 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 확인일 |
|------|---------|---------------------|-------------|---------|------------|----------|--------|
| Langfuse | trace + eval (OSS+클라우드) | 메인 리포(플랫폼) `v3.224.1` (2026-07-23). PyPI `langfuse` **4.14.1** (2026-07-20), npm `langfuse` 3.38.20 | https://github.com/langfuse/langfuse/releases/tag/v3.224.1 | `NOASSERTION` (SPDX 미판정) | 셀프호스팅 가능한 LLM 관측성 — 무료 자체 운영이 기본 옵션 | pushed 2026-07-25 (당일), ★31,828 | 2026-07-25 |
| ↳ Langfuse 버전 체계 주의 | — | 메인 리포 태그는 `v3.x`, Python SDK는 `4.x`, JS SDK는 `3.38.x` — **세 계열이 서로 다르다** | 릴리스 노트 본문이 플랫폼 기능(cloud AI features, api)을 다루므로 `v3.224.1`은 **플랫폼/서버 라인으로 판단**되나, **서버↔SDK 대응 관계는 미확인** | — | **"Langfuse 4.x"라고 쓰면 제품 버전으로 오독된다.** 본문에서 버전을 언급할 땐 반드시 "Python SDK 4.14.1" / "플랫폼 v3.224.1"처럼 계열을 특정하라 | — | 2026-07-25 |
| LangSmith | trace + eval (매니지드) | `미확인 (managed service, 버전 개념 없음)` | https://www.langchain.com/pricing-langsmith | 상용 | LangChain 생태계와 가장 밀착된 트레이싱 | 매니지드. 가격은 표 5 | 2026-07-25 |
| Braintrust | eval 플랫폼 (매니지드) | `미확인 (managed service)`. SDK: PyPI `braintrust` 0.30.1 (2026-07-21), npm `braintrust` 3.24.0 | https://www.braintrust.dev/pricing | 상용 (SDK `autoevals`는 MIT) | 실험·프롬프트 플레이그라운드 중심의 eval 워크플로 | `autoevals` 최신 `js-0.3.0` (2026-06-09), pushed 2026-07-24 | 2026-07-25 |
| Arize Phoenix | OSS 관측성 + eval | `arize-phoenix-v19.6.0` (2026-07-24). PyPI `arize-phoenix` 19.6.0 (2026-07-24) | https://github.com/Arize-ai/phoenix/releases/tag/arize-phoenix-v19.6.0 | `NOASSERTION` (SPDX 미판정) | OpenTelemetry 기반 로컬 실행 가능한 trace UI | pushed 2026-07-25 (당일), ★10,728 | 2026-07-25 |
| W&B Weave | trace + eval | `v0.53.2` (2026-07-16). PyPI `weave` 0.53.2 (2026-07-16) | https://github.com/wandb/weave/releases/tag/v0.53.2 | `Apache-2.0` | 기존 W&B 실험 관리 워크플로의 연장선 | pushed 2026-07-25 (당일), ★1,108 | 2026-07-25 |
| Helicone | LLM 프록시·관측성 | `v2025.08.21-1` (2025-08-21) | https://github.com/Helicone/helicone/releases/tag/v2025.08.21-1 | `Apache-2.0` | 게이트웨이 프록시 한 줄로 붙는 관측성 | pushed 2026-07-25 (당일), ★5,993. **릴리스 태그는 11개월 정체 but 코드는 당일 푸시 — 릴리스를 태깅 안 하는 관행** | 2026-07-25 |
| OpenLLMetry (Traceloop) | OTel 기반 계측 SDK | `0.62.1` (2026-06-28). npm `@traceloop/node-server-sdk` 0.27.0 | https://github.com/traceloop/openllmetry/releases/tag/0.62.1 | `Apache-2.0` | 벤더 중립 OTel 계측 — 백엔드를 나중에 갈아탈 수 있다 | pushed 2026-07-13, ★7,325 | 2026-07-25 |
| **OTel GenAI semantic conventions** | 스펙 | **별도 리포로 분리됨** (`open-telemetry/semantic-conventions-genai`). 릴리스 태그 없음. 코어 semconv는 `v1.43.0` (2026-07-03) | https://github.com/open-telemetry/semantic-conventions-genai | `Apache-2.0` | 벤더 중립 GenAI 트레이스 스키마의 표준 후보 | **상태: `Status: Development`** (stable 아님). pushed 2026-07-24, ★192 | 2026-07-25 |
| Ragas | RAG eval 라이브러리 | `v0.4.3` (2026-01-13). PyPI `ragas` 0.4.3 (2026-01-13) | https://github.com/explodinggradients/ragas/releases/tag/v0.4.3 | `Apache-2.0` | RAG 특화 지표(faithfulness 등)의 사실상 표준 | ⚠️ pushed **2026-02-24** — 5개월 정체. **리포가 `vibrantlabsai/ragas`로 이전됨** (릴리스 URL이 그쪽으로 리다이렉트). ★14,981 | 2026-07-25 |
| DeepEval | LLM eval 프레임워크 | `v4.1.3` (2026-07-12). PyPI `deepeval` 4.1.3 (2026-07-22) | https://github.com/confident-ai/deepeval/releases/tag/v4.1.3 | `Apache-2.0` | pytest 스타일로 쓰는 LLM 단위 테스트 | pushed 2026-07-24, ★17,108 | 2026-07-25 |
| promptfoo | eval + 레드팀 CLI | `0.121.19` (2026-07-14). npm `promptfoo` 0.121.19 | https://github.com/promptfoo/promptfoo/releases/tag/0.121.19 | `MIT` | 선언적 YAML로 CI에 꽂는 eval + 레드팀 | pushed 2026-07-24, ★23,580. ⚠️ **PyPI `promptfoo` 0.1.4는 동일 프로젝트가 아님 — npm이 정본** | 2026-07-25 |
| Inspect AI (UK AISI) | eval 프레임워크 | **PyPI `inspect-ai` 0.3.249 (2026-07-21)**. GitHub `releases/latest` 404, 태그는 `release/2025-11-28` 형식 | https://pypi.org/pypi/inspect-ai/json · https://github.com/UKGovernmentBEIS/inspect_ai | `MIT` | 정부 AI 안전 기관이 만든 에이전트 eval — 솔버/스코어러 추상화 | pushed 2026-07-24, ★2,405 | 2026-07-25 |
| OpenAI Evals | eval 프레임워크 | `미확인` (릴리스·태그 미등록) | https://github.com/openai/evals | `NOASSERTION` (SPDX 미판정) | eval 레지스트리 형태의 원조 구현 | ⚠️ pushed **2026-04-14** — 3개월 정체, ★18,996 | 2026-07-25 |
| HELM (Stanford CRFM) | 벤치마크 하네스 | `v0.5.16` (2026-04-30) | https://github.com/stanford-crfm/helm/releases/tag/v0.5.16 | `Apache-2.0` | 다면 평가(정확도·견고성·공정성) 학술 하네스 | pushed 2026-07-01, ★2,864 | 2026-07-25 |
| autoevals (Braintrust) | LLM-as-judge 스코어러 | `js-0.3.0` (2026-06-09) | https://github.com/braintrustdata/autoevals/releases/tag/js-0.3.0 | `MIT` | 바로 쓰는 judge 스코어러 모음 | pushed 2026-07-24, ★977 | 2026-07-25 |

**소계: 15개**

### 표 3-1. OTel GenAI semantic conventions — 이 책에서 가장 중요한 "표준" 사실 `[축 4]`

2026-07-25 확인 결과, 이 스펙에는 **두 가지 중요한 변화**가 있다. 둘 다 본문에서 단정하기 전에 반드시 반영해야 한다.

| 항목 | 확인된 사실 | 출처 |
|------|-----------|------|
| **리포 분리** | GenAI semconv가 코어 `semantic-conventions`에서 **별도 리포로 이전**됐다. 기존 문서 URL(`opentelemetry.io/docs/specs/semconv/gen-ai/`)은 "moved to the OpenTelemetry GenAI semantic conventions repository ... no longer maintained in the current location" 안내만 남았다 | https://opentelemetry.io/docs/specs/semconv/gen-ai/ |
| **안정성 상태** | **`Status: Development`** — stable도, experimental 승격도 아니다 | https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/README.md |
| 정의 범위 | Events(입출력), Exceptions, Metrics, **Model Spans**, **Agent Spans** | 동일 |
| 벤더별 규약 | Anthropic, Azure AI Inference, AWS Bedrock, OpenAI + **MCP 가이던스** | 동일 |
| 코어 semconv 버전 | `v1.43.0` (2026-07-03) — GenAI 리포는 Weaver로 코어 의존성 관리 | `gh api` + 리포 README |
| GenAI 리포 릴리스 | **태그된 릴리스 없음** (`releases` 비어 있음), ★192, pushed 2026-07-24 | `gh api` |

> **책에 쓸 값 (중요):** "OTel GenAI semconv를 따르면 벤더 중립 관측성이 된다"는 서술은 **현재 시점에서 과장**이다. 상태가 `Development`이고 리포가 막 분리됐으며 릴리스 태그조차 없다. 정확한 서술은 "표준화가 진행 중이고, **Agent Spans까지 규약 범위에 들어왔다**. 지금 붙이면 스키마 변경을 감수해야 한다" 쪽이다. Agent Spans가 규약에 포함됐다는 사실 자체가 이 책 독자에게 중요한 신호다.

---

## 표 4. 에이전트 벤치마크 (제품·리더보드 축) `[축 4]`

**⚠️ 이 표의 점수 열은 대부분 `미확인`이다.** 리더보드가 클라이언트 렌더링이라 정적 fetch로 점수를 못 읽었다. 유일한 예외가 Terminal-Bench 2.0이다.

| 벤치마크 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 리더보드 최고 점수 | 확인일 |
|---------|---------------------|-------------|---------|------------|----------|-----------------|--------|
| SWE-bench | `v4.1.0` (git tag). PyPI `swebench` 4.1.0 (2025-09-11) | https://github.com/SWE-bench/SWE-bench | `MIT` | 실제 GitHub 이슈를 실제 테스트로 채점 | ⚠️ pushed **2026-04-01** — 4개월 정체, ★5,484. `releases/latest` 404 | **`미확인`** — swebench.com 리더보드 fetch 시 본문이 truncate돼 점수 미노출. splits: Verified/Multilingual/Lite/Full/Multimodal | 2026-07-25 |
| Terminal-Bench | 리포 태그 없음. PyPI `terminal-bench` **0.2.18 (2025-09-26)** — 리포 pushed 2026-07-11이므로 **PyPI가 리포보다 낡음** | https://www.tbench.ai/leaderboard · https://github.com/laude-institute/terminal-bench | `Apache-2.0` | 터미널에서 끝까지 해내는지 — 에이전트 하네스째로 평가 | pushed 2026-07-11, ★2,482. 리더보드에 1.0 / 2.0 / 2.1 공존 | **확인됨 (2.0):** 1위 NexAU-AHE (GPT-5.5) **84.7% ±2.1**, 2위 LemonHarness **84.5% ±2.6**, 3위 Capy (GPT-5.5) **83.1% ±2.1**, 4위 Codex CLI (GPT-5.5) **82.2% ±2.2**, 6위 WOZCODE (Claude Opus 4.7) **80.2% ±2.1**, 7위 TongAgents (Gemini 3.1 Pro) **80.2% ±2.6** | 2026-07-25 |
| τ-bench 계열 | 리포 `sierra-research/tau2-bench` (릴리스·태그 없음). **README는 현재 버전을 τ³-bench(tau3-bench)로 기술** | https://github.com/sierra-research/tau2-bench | `MIT` | 고객 응대 도메인(airline·retail·telecom·banking_knowledge·mock) 시뮬레이션 + 음성·지식 검색 평가 | pushed 2026-07-24, ★1,660 | **`미확인`** — 리포 페이지에 수치 베이스라인 없음 | 2026-07-25 |
| GAIA | `미확인` | https://huggingface.co/spaces/gaia-benchmark/leaderboard | `미확인` | 도구 사용이 필수인 일반 어시스턴트 과제 | HF Space | **`미확인`** — Space가 로딩 화면만 반환 | 2026-07-25 |
| WebArena | `v0.2.0` (**2023-10-21**) | https://github.com/web-arena-x/webarena/releases/tag/v0.2.0 | `Apache-2.0` | 자체 호스팅 웹 환경에서의 브라우저 에이전트 평가 | ⚠️ pushed 2025-11-26, ★1,556. **릴리스 2023년 — 구버전 정보일 수 있음, 사실상 정체** | `미확인` | 2026-07-25 |
| AgentBench | 릴리스·태그 없음 | https://github.com/THUDM/AgentBench | `Apache-2.0` | 8개 환경 다면 에이전트 평가 | ⚠️ pushed **2026-02-08** — 5개월 정체, ★3,602 | `미확인` | 2026-07-25 |

**소계: 6개**

> **책에 쓸 값:** 벤치마크 활동 신호가 극명하게 갈린다. Terminal-Bench(pushed 2026-07-11, 리더보드 2.1까지)와 τ-bench 계열(pushed 2026-07-24)은 살아 있고, WebArena(2023년 릴리스)·AgentBench(5개월 정체)는 사실상 멈췄다. "표준 벤치마크"로 나열하면 독자를 죽은 벤치마크로 보낸다. 신선도까지 같이 적어야 한다.
> **Terminal-Bench 2.0 점수는 상단이 80%대로 몰려 있고 오차범위가 ±2%대**라 1~5위 간 차이는 통계적으로 겹친다. "1위 모델" 식 서술보다 "상단이 포화 구간에 들어섰다"가 정확하다.

---

## 표 5. 가드레일 `[축 4]`

| 도구 | 카테고리 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 확인일 |
|------|---------|---------------------|-------------|---------|------------|----------|--------|
| Guardrails AI | 입출력 검증 프레임워크 | `v0.10.2` (2026-06-04). PyPI `guardrails-ai` 0.10.2 | https://github.com/guardrails-ai/guardrails/releases/tag/v0.10.2 | `Apache-2.0` | validator 허브 방식의 선언적 입출력 검증 | pushed 2026-07-24, ★7,203 | 2026-07-25 |
| NeMo Guardrails | 대화 흐름 레일 | `v0.23.0` (2026-07-01). PyPI `nemoguardrails` 0.23.0 | https://github.com/NVIDIA/NeMo-Guardrails/releases/tag/v0.23.0 | `NOASSERTION` (SPDX 미판정) | Colang DSL로 대화 흐름 자체를 제약 | pushed 2026-07-25 (당일), ★6,786. **리포가 `NVIDIA-NeMo/Guardrails`로 이전** (릴리스 URL 리다이렉트) | 2026-07-25 |
| OpenAI Moderation | 콘텐츠 안전 API | `omni-moderation-latest` | https://developers.openai.com/api/docs/guides/moderation | 상용 API | **무료**, 이미지 입력 지원(최대 20MB), 13개 카테고리 | 매니지드 | 2026-07-25 |
| Azure AI Content Safety | 콘텐츠 안전 + 에이전트 안전 | API 버전 `미확인` (문서에 GA/preview 혼재) | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview | 상용 | **Prompt Shields**(탈옥·주입 탐지) + **Task adherence API**(에이전트 도구 사용 이탈 탐지) | 문서 갱신 2026-06-05. F0/S0 티어 | 2026-07-25 |
| Llama Guard | 오픈 안전 분류 모델 | `미확인` (모델 카드 페이지 본문 fetch 실패) | https://github.com/meta-llama/PurpleLlama | `NOASSERTION` (Llama 라이선스 계열) | 자체 호스팅 가능한 입출력 안전 분류기 | pushed 2026-07-24, ★4,309. 릴리스 태그 없음 | 2026-07-25 |
| Prompt Guard | 오픈 주입 탐지 모델 | `미확인` | https://github.com/meta-llama/PurpleLlama | `NOASSERTION` | 프롬프트 인젝션·탈옥 전용 소형 분류기 | PurpleLlama 리포 동일 | 2026-07-25 |
| OpenAI Agents SDK guardrails | 프레임워크 내장 가드레일 | 리포 `openai/openai-agents-python` pushed 2026-07-25, ★28,160 | https://openai.github.io/openai-agents-python/guardrails/ | `MIT` | input/output 가드레일 + **tripwire 예외로 실행 즉시 중단** | pushed 2026-07-25 (당일) | 2026-07-25 |
| Rebuff | 프롬프트 인젝션 방어 | `v0.1.1` (**2024-01-20**) | https://github.com/protectai/rebuff/releases/tag/v0.1.1 | `Apache-2.0` | (역사적 참조용) 다층 인젝션 탐지 | ❌ **`archived: true` — 아카이브된 죽은 프로젝트.** pushed 2024-08-07, ★1,515 | 2026-07-25 |
| invariant | 에이전트 분석·가드레일 | 릴리스·태그 없음 | https://github.com/invariantlabs-ai/invariant | `Apache-2.0` | 에이전트 트레이스에 대한 규칙 기반 검사 | ⚠️ pushed **2026-01-12** — 6개월 정체, ★436 | 2026-07-25 |
| Lakera | 상용 인젝션 방어 | `미확인` | — | 상용 | (제품 상세 확인 실패) | 리포 접근 실패 — "수집 한계" 참조 | 2026-07-25 |

**소계: 10개**

### 표 5-1. 가드레일 아키텍처 패턴 (벤더 권장 배치) `[축 4]` `[축 6]`

공식 문서에서 확인한 배치 패턴만 적는다.

| 패턴 | 벤더가 말하는 것 | 1차 소스 |
|------|---------------|---------|
| **입력 가드레일 + tripwire 중단** | OpenAI Agents SDK: "Input guardrails run only for the first agent in the chain", "Output guardrails run only for the agent that produces the final output". 발동 시 `{Input,Output}GuardrailTripwireTriggered` 예외를 **즉시 raise하고 실행을 중단**한다 | https://openai.github.io/openai-agents-python/guardrails/ |
| **값싼 모델로 먼저 걸러라** | 같은 문서: 가드레일 함수 안에 별도 검증 에이전트를 두는 패턴. "a lightweight model runs guardrail checks before deploying expensive models, thereby reducing costs for blocked requests" | 동일 |
| **탈옥·주입은 전용 분류기로** | Azure **Prompt Shields**: "Scans text for the risk of a User input attack on a Large Language Model." 입력 한도 10K자, 문서 최대 5개·총 10K자 | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview |
| **도구 사용 이탈 감시 (에이전트 특화)** | Azure **Task adherence API** (preview): "Detects when tool use by AI agents is misaligned, unintended, or premature in the context of a user interaction." 입력 한도 **100K자** | 동일 |
| **환각을 출력단에서 잡기** | Azure **Groundedness detection** (preview): LLM 응답이 제공된 소스에 근거하는지 판정. grounding source 최대 55,000자, 쿼리 최대 7,500자·최소 3단어 | 동일 |
| **도구 호출 승인 게이트 / 최소권한** | Claude Code 문서: 기본적으로 파일 쓰기·Bash·MCP 도구에 **권한을 요청**한다. 완화 수단 3종 — ① auto mode(별도 classifier가 "scope escalation, unknown infrastructure, or hostile-content-driven actions"만 차단), ② 허용목록(`npm run lint` 등 개별 허용), ③ **OS 레벨 샌드박싱**(파일시스템·네트워크 제한). 비대화형 배치 실행 시 `--allowedTools`로 권한 축소 권장 | https://code.claude.com/docs/en/best-practices |
| **결정적 게이트는 훅으로** | 같은 문서: "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." 예: "a hook that blocks writes to the migrations folder" | 동일 |

> **책에 쓸 값:** 가드레일을 "필터 하나"로 그리면 안 된다. 확인된 배치는 **4층**이다 — ① 입력단 주입·탈옥 분류기(Prompt Shields / Prompt Guard) → ② 실행 중 도구 호출 승인·권한 축소(허용목록 / 샌드박스 / auto-mode classifier) → ③ 출력단 근거성·콘텐츠 검사(Groundedness / Moderation) → ④ 결정적 훅(어드바이저리 지시가 아니라 코드로 강제). 그리고 "advisory 지시 vs deterministic 훅"의 구분은 이 책 독자가 가장 자주 틀리는 지점이다.

---

## 표 6. RAG 파이프라인·인덱싱·청킹 `[축 3]`

| 도구 | 카테고리 | 버전 (2026-07-25 기준) | 1차 소스 URL | 라이선스 | 한 줄 차별점 | 활동 신호 | 확인일 |
|------|---------|---------------------|-------------|---------|------------|----------|--------|
| LlamaIndex (인덱싱 축) | RAG 프레임워크 | `v0.14.23` (2026-06-24). PyPI 0.14.23, npm `llamaindex` 0.12.1 | https://github.com/run-llama/llama_index/releases/tag/v0.14.23 | `MIT` | 인덱스·리트리버 추상화가 가장 촘촘하다 | pushed 2026-07-25 (당일), ★51,078 | 2026-07-25 |
| Haystack | RAG·검색 파이프라인 | **`v3.0.0` (2026-07-20 — 메이저 릴리스 5일 전)** | https://github.com/deepset-ai/haystack/releases/tag/v3.0.0 | `Apache-2.0` | 명시적 파이프라인 그래프로 조립 | pushed 2026-07-25 (당일), ★26,010. **v3.0.0이 갓 나옴 — v2 기준 자료는 구버전** | 2026-07-25 |
| Unstructured | 문서 파싱·전처리 | `0.24.1` (2026-07-11) | https://github.com/Unstructured-IO/unstructured/releases/tag/0.24.1 | `Apache-2.0` | 잡다한 파일 포맷을 요소 단위로 정규화 | pushed 2026-07-23, ★15,197 | 2026-07-25 |
| Docling | 문서 변환 | `v2.115.0` (2026-07-23) | https://github.com/docling-project/docling/releases/tag/v2.115.0 | `MIT` | PDF 레이아웃·표 구조를 살려서 변환 | pushed 2026-07-24, **★63,754 (이 표 최다)** | 2026-07-25 |
| Chonkie | 청킹 라이브러리 | `v1.7.0` (2026-07-07) | https://github.com/chonkie-inc/chonkie/releases/tag/v1.7.0 | `MIT` | 청킹만 전담하는 경량 라이브러리 | pushed 2026-07-24, ★4,565. 리포가 `feyninc/chonkie`로 이전 (릴리스 URL 리다이렉트) | 2026-07-25 |
| Cognee | 메모리·graph RAG | `v1.4.0.dev0` (2026-07-20, **dev 프리릴리스**) | https://github.com/topoteretes/cognee/releases/tag/v1.4.0.dev0 | `Apache-2.0` | 에이전트 메모리를 그래프로 | pushed 2026-07-25 (당일), ★29,300. **최신 태그가 `.dev0` — 안정 버전 미확인** | 2026-07-25 |
| Microsoft GraphRAG | graph RAG | `v3.1.1` (2026-07-18) | https://github.com/microsoft/graphrag/releases/tag/v3.1.1 | `MIT` | 엔티티 그래프 + 커뮤니티 요약으로 전역 질의 | pushed 2026-07-25 (당일), ★34,827 | 2026-07-25 |

**소계: 7개**

### 표 6-1. 청킹·컨텍스트 공급 실무 수치 (출처 있는 것만) `[축 3]`

| 지침 | 확인된 수치 | 출처 | 신선도 |
|------|-----------|------|--------|
| 청크 크기 (일반) | "usually no more than a few hundred tokens" | Anthropic, Contextual Retrieval | **2024-09-19 — 구버전 정보일 수 있음** |
| 청크 크기 (작게) | **128–256 tokens** | Pinecone, Chunking strategies | 발행일 미확인 |
| 청크 크기 (크게) | **512–1024 tokens** | 동일 | 발행일 미확인 |
| 고정 크기 전략 | 임베딩 모델 최대 컨텍스트에 맞춤 (예: `llama-text-embed-v2` 1024, `text-embedding-3-small` 8196) | 동일 | 발행일 미확인 |
| 오버랩 | **`미확인`** — Pinecone 청킹 문서에 구체 수치 없음, Anthropic 글에도 없음 | — | — |
| 청킹 전략 이름 | ① 고정 크기 ② 문장·문단 분할 ③ recursive character ④ 문서 구조 기반(PDF/HTML/Markdown/LaTeX) ⑤ semantic chunking ⑥ **contextual chunking with LLMs** | Pinecone | 발행일 미확인 |
| 컨텍스트 보강 효과 | Contextual Embeddings 단독: top-20 검색 실패율 **35% 감소** (5.7% → 3.7%). + Contextual BM25: **49% 감소** (5.7% → 2.9%). + 리랭킹까지: **67% 감소** (5.7% → 1.9%) | Anthropic, Contextual Retrieval | **2024-09-19 — 모델이 바뀌었으므로 수치는 재현 보장 없음. "이 실험에서"를 반드시 붙여라** |

> **오버랩 수치는 어떤 1차 소스에서도 확인하지 못했다.** 흔히 "10~20% 오버랩"이라 말하지만 이번 세션에서 공식 문서 근거를 찾지 못했다. 본문에 숫자를 박지 말고 "오버랩은 모델·문서 구조에 따라 조정하는 튜닝 대상"으로 서술하라.

---

## 6. 벡터 DB 선택 축 — "우리 규모에 pgvector로 충분한가" `[축 3]` `[축 6]`

독자가 실제로 묻는 질문에 맞춰, **확인된 사실로만** 축을 세운다.

### 축 A. 내장(기존 DB 겸업) vs 전용 엔진

| 갈림길 | 내장형 (pgvector / Redis / MongoDB Atlas / sqlite-vec) | 전용형 (Qdrant / Weaviate / Milvus / Pinecone) |
|--------|--------------------------------------|-----------------------------------|
| 새 인프라 | 없음 — 이미 운영하는 DB에 확장/인덱스만 | 새 서비스 하나를 운영 대상에 추가 |
| 트랜잭션 정합성 | 본문·메타데이터와 **같은 트랜잭션** 안에서 갱신 | 원본 DB와 인덱스 사이 동기화 파이프라인이 별도 필요 |
| 확인된 한계 | **pgvector: HNSW/IVFFlat 인덱스는 `vector` 최대 2,000차원.** `halfvec` 4,000, `bit` 64,000, `sparsevec` 비영요소 1,000. 타입 자체는 `vector`/`halfvec` 최대 16,000차원 | Milvus는 다중 벡터 필드 동시 ANN + 내장 BM25, Qdrant는 prefetch 다단계 쿼리 등 검색 표현력이 앞선다 |
| 1차 소스 | https://github.com/pgvector/pgvector · https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/ | 표 1 각 행 |

> **이 축에서 나오는 가장 실용적인 결론(양쪽 수치 모두 1차 소스 직접 확인):** pgvector에서 **`text-embedding-3-large`의 기본 3,072차원은 HNSW 인덱스 한계(2,000)를 넘는다.**
> — 3,072는 OpenAI 임베딩 가이드 원문("or `3072` for `text-embedding-3-large`"), 2,000은 pgvector README에서 각각 직접 확인했다. **두 숫자가 서로 다른 1차 소스에서 왔고 둘 다 인용문으로 뒷받침된다** — 이 결론은 fact-checker 대조를 통과할 수 있는 형태다. 그래서 선택은 셋 중 하나다 — ① 차원 축소(`dimensions` 파라미터로 1536 이하), ② `halfvec`(4,000까지), ③ 전용 엔진. **"pgvector로 충분한가"가 인덱스 차원 한계라는 아주 구체적인 숫자에서 갈린다**는 것이 이 책이 줄 수 있는 실무 지식이다. MongoDB Atlas는 최대 8,192차원이므로 이 제약이 없다.

### 축 B. 하이브리드 검색 지원 깊이
표 1-1 참조. "지원/미지원"이 아니라 **융합 알고리즘 수와 조절 손잡이 수**로 갈린다. Milvus만 **BM25 sparse 임베딩 생성까지 엔진이 대신한다**(파이프라인 코드가 줄어든다).

### 축 C. 운영 부담 (스펙트럼)
`sqlite-vec`(서버 없음, 단일 파일) → `Chroma`/`LanceDB`(임베디드) → `pgvector`(기존 Postgres) → `Qdrant`/`Weaviate`/`Milvus`(전용 서비스 운영) → `Vespa`(가장 무거움) → `Pinecone`/`Turbopuffer`/`MongoDB Atlas`(매니지드, 운영 부담을 돈으로 치환)

### 축 D. 스케일 임계점 (벤더가 스스로 말하는 숫자)
- Turbopuffer 공식 문서: "4T+ documents, 10M+ writes/s, and 25k+ queries/s" 서비스 중. 쓰기 지연 "p90=248ms for 512KB upserts", **콜드 쿼리 "p90=1214ms on 1M documents"** (캐시 미적용/미고정 시)
- → **책에 쓸 값:** 객체 스토리지 기반 설계는 **캐시 히트 여부가 지연을 5배 이상 가른다**. "싸다"의 대가가 콜드 스타트라는 걸 벤더가 자기 문서에 적어 놨다. 이건 아키텍처 트레이드오프를 가르치기에 아주 좋은 1차 인용이다.
- Pinecone 확인된 한계: 메타데이터 **레코드당 40KB**, sparse 벡터 비영값 **1,000개**, `top_k` 최대 **1,000**, 쿼리 결과 크기 **4MB**, sparse 인덱스 쓰기 **10 QPS**·읽기 **100 QPS**. 10만 네임스페이스 초과 시 문의
- Azure Content Safety 처리량(가드레일 쪽 임계점): F0 5 RPS / S0 1000 RP10S, Groundedness 50 RPS

### 축 E. 라이선스 (조직에서 실제로 막히는 축)
`Apache-2.0`: Qdrant, Milvus, Chroma, LanceDB, Vespa, OpenSearch, sqlite-vec / `BSD-3-Clause`: Weaviate / `MIT`: FAISS / `GPL-3.0`: **Typesense** / `NOASSERTION`(비-OSI 계열 주의): **Elasticsearch, Redis(RediSearch)**, pgvector(판정 불가)
> Typesense의 GPL-3.0과 Elasticsearch/Redis의 소스 가용 라이선스는 사내 배포 정책에서 실제로 걸린다. 라이선스는 성능 열 다음이 아니라 성능 열과 같은 급으로 다뤄야 한다.

---

## 7. 벡터 DB가 필요 없는 경우 (1차 소스 근거) `[축 3]` `[축 6]`

이 책에서 가장 값진 절이 될 수 있는 부분이다. **벤더·모델 제공자가 스스로 "안 써도 된다"고 말한 근거만** 모았다.

### 근거 1 — 코퍼스가 작으면 그냥 다 넣어라 (가장 명확한 1차 인용)

> "If your knowledge base is smaller than 200,000 tokens (about 500 pages of material), you can just include the entire knowledge base in the prompt that you give the model, with no need for RAG or similar methods."
> — Anthropic, *Introducing Contextual Retrieval*, **2024-09-19**
> https://www.anthropic.com/news/contextual-retrieval

- **20만 토큰 / 약 500페이지**라는 구체적 임계값이 제공자 공식 발표문에 박혀 있다.
- 신선도 주의: 2024-09 글이다. 그 사이 컨텍스트 창은 더 커졌으므로 이 임계값은 **보수적 하한**으로 읽는 게 맞다. 본문에서는 "2024년 Anthropic 기준 20만 토큰"으로 연도를 반드시 붙여라.
- 프롬프트 캐싱과 함께 쓰면 비용 논리도 바뀐다는 점이 같은 글의 맥락이다.

### 근거 2 — 코딩 에이전트는 인덱스 대신 탐색 도구를 쓴다

Claude Code 공식 문서에서 확인된 코드베이스 탐색 방식은 **임베딩 인덱스가 아니라 에이전틱 탐색**이다.

- 파일을 직접 읽고(`@` 참조), 명령을 실행하며 자율적으로 문제를 해결하는 구조: "Claude Code can read your files, run commands, make changes, and autonomously work through problems"
- 탐색이 컨텍스트를 잡아먹는 문제는 **인덱스가 아니라 서브에이전트로** 해결한다: "When Claude researches a codebase it reads lots of files, all of which consume your context. Subagents run in separate context windows and report back summaries"
- 외부 시스템 조회도 인덱스가 아니라 **CLI 도구**를 권장한다: "CLI tools are the most context-efficient way to interact with external services"
- 실패 패턴으로 **범위 없는 탐색**을 명시: "The infinite exploration. You ask Claude to 'investigate' something without scoping it. Claude reads hundreds of files, filling the context." → 처방은 "Scope investigations narrowly or use subagents"
- 1차 소스: https://code.claude.com/docs/en/best-practices

> ⚠️ **정직한 한계 표기:** 이 문서에는 "우리는 RAG/임베딩 인덱스를 쓰지 않는다"는 **명시적 부정 문장이 없다.** 확인된 것은 "문서 전반이 인덱스 없는 에이전틱 탐색(파일 읽기·명령 실행·서브에이전트·CLI)을 전제로 기술돼 있다"는 사실뿐이다. 본문에서 "공식적으로 인덱싱을 쓰지 않는다고 밝혔다"고 쓰면 과장이다. **"공식 문서가 권장하는 워크플로는 인덱스가 아니라 탐색 도구와 서브에이전트 기반이다"**가 확인 가능한 서술의 상한선이다.

### 근거 3 — 검색 실패의 상당 부분은 리랭킹으로 해결된다 (DB 교체 전에 할 일)

Anthropic 실험(2024-09-19)에서 top-20 검색 실패율은 **5.7% → 1.9%**로 떨어졌는데, 그 경로는 벡터 DB 교체가 아니라 **컨텍스트 보강 + BM25 병용 + 리랭킹**이었다.
> **책에 쓸 값:** "검색이 안 맞는다 → 벡터 DB를 바꾼다"는 흔한 오진이다. 같은 DB에서 ① 하이브리드(BM25 병용) ② 컨텍스트 보강 청킹 ③ 리랭커 세 가지가 먼저다. 리랭커 단가는 임베딩보다 싸다(Voyage `rerank-2.5-lite` $0.02/1M).

### 근거 4 — 첫 단계 후보 축소용이지 정답 도출용이 아니다

Turbopuffer 공식 문서는 자기 제품 포지션을 이렇게 규정한다: "first-stage retrieval to efficiently narrow millions of documents ... down to tens or hundreds"
> 벡터 검색은 **1차 후보 축소기**다. 정답을 고르는 건 리랭커와 LLM이다. 이 프레이밍이 명확하면 "벡터 검색 정확도"에 과투자하는 실수를 막을 수 있다.

### 근거 5 — 정형 데이터는 SQL이 맞다
확인된 1차 소스를 이번 세션에서 찾지 못했다. 논리적으로 자명하지만 **인용 가능한 벤더 문장을 확보하지 못했으므로** 본문에서 출처를 붙이지 말고 저자 주장으로 쓰거나, fact-checker 단계에서 별도 확인을 요청하라. → "미확인 항목 목록"에 기재.

---

## 8. 자료별 신선도·신뢰성 카드

축 태그와 신뢰성 등급을 붙인 개별 자료 카드. (표에 이미 반영된 리포·레지스트리 조회는 생략)

### 자료 1: Anthropic — Introducing Contextual Retrieval `[축 3]`
- 출처: https://www.anthropic.com/news/contextual-retrieval
- 저자·날짜: Anthropic, **2024-09-19**
- 신뢰성: **최상** (모델 제공자 1차 발표, 수치와 방법 명시)
- 핵심 주장: 청크에 문맥을 덧붙여 임베딩하고 BM25를 병용하면 검색 실패율이 크게 떨어진다. 20만 토큰 미만 코퍼스는 RAG 자체가 불필요하다.
- 인용 가능한 구절: "If your knowledge base is smaller than 200,000 tokens (about 500 pages of material), you can just include the entire knowledge base in the prompt that you give the model, with no need for RAG or similar methods." / 청크는 "usually no more than a few hundred tokens"
- 신선도 경고: **약 22개월 전 자료. 수치는 "2024년 실험 기준"으로 못 박아야 한다.**
- 관련 섹션: 데이터·RAG 챕터 도입부, "벡터 DB가 필요 없는 경우", 청킹 실무

### 자료 2: OpenTelemetry GenAI semantic conventions `[축 4]`
- 출처: https://github.com/open-telemetry/semantic-conventions-genai · https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/README.md
- 저자·날짜: OpenTelemetry, pushed **2026-07-24** (릴리스 태그 없음)
- 신뢰성: **최상** (스펙 1차 소스)
- 핵심 주장: GenAI 규약이 코어 semconv에서 분리돼 독립 리포로 운영된다. 상태는 `Development`. **Agent Spans**와 MCP 가이던스가 규약 범위에 포함.
- 인용 가능한 구절: "Status: Development" / 구 문서 위치는 "no longer maintained in the current location"
- 관련 섹션: 관측성 챕터 — "표준은 어디까지 왔나"

### 자료 3: OpenAI 임베딩 가격의 공식 페이지 간 불일치 `[축 3]` ⚠️
- 출처: https://developers.openai.com/api/docs/models/text-embedding-3-large (모델 카드) vs 가격 페이지
- 확인 내용: 모델 카드 fetch 결과 `text-embedding-3-large` = **$0.13 / 1M tokens**, `text-embedding-3-small` = **$0.02 / 1M tokens** (둘 다 직접 fetch). 한편 3-large를 **$0.065**로 표기한다는 보고가 있다 — 단 **이 $0.065는 내가 직접 fetch한 값이 아니라 WebSearch가 요약한 OpenAI 개발자 포럼 글(2025-08 시점 보고)의 내용이다.** 가격 페이지 자체는 도달 실패(수집 한계 6번).
- 신뢰성: **최상** (모델 카드 직접 확인) — 단, **공식 표면 간 불일치 가능성**으로 단일 값 단정은 불가
- ⚠️ 두 값의 출처 등급이 다르다: **$0.13 = 직접 fetch(검증됨)**, **$0.065 = 포럼 글의 검색 요약(미검증)**. fact-checker는 후자를 확인된 사실로 취급하면 안 된다.
- 관련 섹션: 임베딩 비용 계산 예시
- **fact-checker 지시:** 본문에 임베딩 단가를 쓸 경우 반드시 "모델 카드 기준 $0.13(2026-07 확인), 가격 페이지와 불일치 보고 있음"처럼 출처 표면을 특정하라. 이 값으로 총비용 계산 예시를 만들면 배수 오류가 난다.

### 자료 4: Claude Code Best practices `[축 1]` `[축 4]`
- 출처: https://code.claude.com/docs/en/best-practices (구 URL `anthropic.com/engineering/claude-code-best-practices`에서 308 리다이렉트)
- 저자·날짜: Anthropic, 발행일 미표기 (문서 상시 갱신형)
- 신뢰성: **최상** (제공자 공식 문서)
- 핵심 주장: 에이전트 품질의 지배 변수는 **컨텍스트 예산**과 **검증 루프**다. "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills."
- 인용 가능한 구절: "Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from." / "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." / 실패 패턴 "The trust-then-verify gap. Claude produces a plausible-looking implementation that doesn't handle edge cases."
- 관련 섹션: 에이전트 원리(축 1), 가드레일·권한 설계(축 4), 평가 루프 설계

### 자료 5: OpenAI Agents SDK — Guardrails `[축 4]`
- 출처: https://openai.github.io/openai-agents-python/guardrails/
- 신뢰성: **최상** (공식 프레임워크 문서)
- 인용 가능한 구절: "Input guardrails run only for the first agent in the chain" / "Output guardrails run only for the agent that produces the final output" / 발동 시 "immediately raise ... exception and halt the Agent execution"
- 관련 섹션: 가드레일 챕터 — 배치 위치와 비용 논리

### 자료 6: Azure AI Content Safety Overview `[축 4]`
- 출처: https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview
- 저자·날짜: Microsoft, 문서 갱신 **2026-06-05** (ms.date 2025-09-16)
- 신뢰성: **최상**
- 핵심 주장: 콘텐츠 안전이 "유해 표현 필터"를 넘어 **에이전트 행동 감시**로 확장됐다 — Task adherence(도구 사용 이탈 탐지), Groundedness(근거성).
- 인용 가능한 구절: Task adherence는 "Detects when tool use by AI agents is misaligned, unintended, or premature in the context of a user interaction."
- 관련 섹션: 가드레일 챕터 — 에이전트 특화 안전 장치

### 자료 7: Turbopuffer Docs `[축 3]`
- 출처: https://turbopuffer.com/docs
- 신뢰성: **최상** (벤더 1차, 다만 성능 주장은 자사 측정치)
- 인용 가능한 구절: "as fast as in-memory search engines when cached, but far cheaper to run" / 콜드 쿼리 "p90=1214ms on 1M documents" / "first-stage retrieval to efficiently narrow millions of documents ... down to tens or hundreds"
- 관련 섹션: 벡터 DB 아키텍처 트레이드오프, 스케일 임계점

### 자료 8: pgvector README `[축 3]`
- 출처: https://github.com/pgvector/pgvector
- 신뢰성: **최상**
- 인용 가능한 사실: HNSW·IVFFlat 모두 `vector` **2,000차원 한계**, `halfvec` 4,000, `bit` 64,000, `sparsevec` 비영요소 1,000. 타입 한계는 16,000차원. 튜닝: "indexes build significantly faster when the graph fits into `maintenance_work_mem`", `hnsw.ef_construction` 기본 64, `hnsw.ef_search` 기본 40
- 관련 섹션: "우리 규모에 pgvector로 충분한가"

### 자료 9: Terminal-Bench 2.0 리더보드 `[축 4]`
- 출처: https://www.tbench.ai/leaderboard/terminal-bench/2.0
- 신뢰성: **최상** (공식 리더보드 직접 fetch)
- 확인 시점 스냅샷: 1위 84.7%±2.1 (NexAU-AHE / GPT-5.5), 10위 77.3%±2.2 (Droid / GPT-5.3-Codex)
- 신선도 경고: **리더보드는 상시 변동.** 본문에 쓸 때 "2026-07-25 확인 기준"을 반드시 병기하라.
- 관련 섹션: 평가 챕터 — 에이전트 벤치마크 읽는 법

### 자료 10: Pinecone 가격·인덱싱 문서 `[축 3]`
- 출처: https://www.pinecone.io/pricing/ · https://docs.pinecone.io/guides/index-data/indexing-overview
- 신뢰성: **최상**
- 확인된 수치: Starter 무료(2GB / 쓰기 2M / 읽기 1M / egress 1GB), Builder $20/mo(10GB / 5M / 2M), Standard $50/mo 최소 + 스토리지 $0.33/GB/mo·쓰기 $4–4.50/M·읽기 $16–18/M, Enterprise $500/mo 최소 + 쓰기 $6–6.75/M·읽기 $24–27/M
- 관련 섹션: 축 6 비용 비교

---

## 9. 축 6을 위한 조합 원재료 (데이터·eval 스택) `[축 6]`

표에서 확인된 사실만으로 구성 가능한 조합 축. **점수·성능 우열이 아니라 제약 조건으로** 갈라 놨다.

| 상황 | 데이터 계층 | eval·관측성 계층 | 가드레일 계층 | 근거 |
|------|-----------|---------------|-------------|------|
| 코퍼스 20만 토큰 미만 | **벡터 DB 없음** — 전체를 프롬프트에 | 트레이스만 (Langfuse 셀프호스팅 무료) | 입력 분류기 + 출력 검사 | Anthropic 2024-09 (연도 병기 필수) |
| 이미 Postgres 운영, 차원 ≤1536 | pgvector (HNSW) | Langfuse 또는 Phoenix (둘 다 셀프호스팅) | OpenAI Moderation(무료) | pgvector README 2,000차원 한계 |
| 차원 3072 유지 필요 | `halfvec`(4,000) / MongoDB Atlas(8,192) / 전용 엔진 | 동일 | 동일 | pgvector·Atlas 문서 |
| 하이브리드 검색이 핵심 | Milvus(내장 BM25) / Qdrant(prefetch+RRF/DBSF) / Elasticsearch(RRF retriever) | Ragas(단, 5개월 정체) 또는 DeepEval | — | 표 1-1 |
| 운영 인력 없음 | Pinecone / Turbopuffer / Atlas | LangSmith / Braintrust (매니지드) | Azure Content Safety | 표 5 가격 |
| 라이선스가 Apache-2.0이어야 함 | Qdrant / Milvus / Chroma / LanceDB / OpenSearch | Phoenix(SPDX 미판정 주의) / Weave / promptfoo(MIT) | Guardrails AI / OpenAI Agents SDK(MIT) | 표 라이선스 열 |
| CI에 eval 게이트를 꽂아야 함 | — | **promptfoo**(선언적 YAML) / DeepEval(pytest 스타일) / Inspect AI | — | 표 3 |
| 검색 품질이 안 나올 때 (DB 교체 전) | 하이브리드 + 컨텍스트 청킹 + 리랭커(Voyage `rerank-2.5-lite` $0.02/1M) | — | — | Anthropic 5.7%→1.9% 경로 |

---

## 10. 수집 한계 (접근 실패·판단 유보)

1. **JS 렌더링 리더보드 3종 실패** — MTEB(`huggingface.co/spaces/mteb/leaderboard`), GAIA(`gaia-benchmark/leaderboard`)는 HF Docker Space 로딩 화면만 반환. SWE-bench(`swebench.com`)는 본문이 truncate돼 점수 미노출. → 세 벤치마크의 점수는 전부 `미확인`. 정적 fetch로는 불가하며 브라우저 렌더링이 필요하다.
2. **Nomic 문서 404** — `https://docs.nomic.ai/atlas/embeddings-and-retrieval/guides/embedding-model-comparison` HTTP 404. Nomic Embed 관련 모든 셀 `미확인`. (`nomic-ai/contrastors`는 pushed 2025-03-26로 정체 상태이며 임베딩 모델 배포 리포가 아닌 것으로 보여 표에서 제외)
3. **Llama Guard 4 모델 카드 본문 미확보** — `llama.com` → `developer.meta.com` 리다이렉트 후에도 페이지 제목만 반환, 본문 없음. 파라미터 수·멀티모달 여부·hazard 카테고리 수(S1–S14 여부)·라이선스명 전부 `미확인`.
4. **Lakera 미확인** — `lakeraai/*` 리포 추정 경로 404. 제품 상세·버전 확인 실패.
5. **Cohere 토큰 단가 부재** — 현재 `cohere.com/pricing`은 Model Vault(시간당/월 정액)만 노출하고 Embed/Rerank 토큰 단가를 제공하지 않는다. FAQ에 레거시 Command 계열 토큰 단가만 언급. → Cohere 임베딩/리랭크 단가는 `미확인`.
6. **OpenAI 임베딩·moderation 가격 페이지 도달 실패** — `platform.openai.com/docs/pricing` → `developers.openai.com/api/docs/pricing` 리다이렉트 후 fetch했으나 임베딩·moderation 표가 응답에 포함되지 않음(LLM 모델 표만). `developers.openai.com/api/pricing`은 404. 모델 카드 개별 페이지로 우회해 3-small/3-large만 확보. `ada-002` 단가 `미확인`.
7. **OpenAI embeddings 가이드의 "pages per dollar" 표기 — 오염된 fetch를 격리한 기록** — 최초 fetch 시 가이드 문서가 가격을 "62,500 pages per dollar" 식으로 표기했고, fetch 요약 모델이 이를 잘못된 ¢/1M 값으로 환산했다(0.016¢/1M 등). **이 환산값은 전부 폐기했고 표에 넣지 않았다.** 가격은 모델 카드의 명시적 $/1M 값만 채택.
   - ⚠️ **그런데 차원·입력토큰 수치도 최초에 같은 응답에서 왔다.** 같은 응답의 가격을 신뢰할 수 없다고 판정했으면 차원도 같이 의심해야 한다 — 그래서 **가격을 일절 묻지 않는 별도 프롬프트로 재fetch**해서 인용문까지 확보했다: 1,536("the length of the embedding vector is `1536` for `text-embedding-3-small`"), 3,072("or `3072` for `text-embedding-3-large`"), 8,192(세 모델 공통). **모델 카드 페이지에는 차원·입력 한도가 없다**(별도 확인). 이 재검증 덕에 축 A의 핵심 결론이 인용문 기반으로 서게 됐다.
8. **"정형 데이터는 SQL로"에 대한 1차 소스 미확보** — 논리적으로 자명하나 인용 가능한 벤더 문장을 찾지 못했다. 저자 주장으로 처리하고 출처를 붙이지 말라.
9. **오버랩 권장 수치 미확보** — Pinecone 청킹 문서·Anthropic 글 모두 구체 오버랩 수치 없음.
10. **Weaviate `alpha` 기본값 미확보** — 문서가 `alpha=1`/`alpha=0`의 의미는 설명하나 기본값은 해당 페이지에 없음.
11. **Elasticsearch RRF 파라미터 기본값 미확보** — `rank_constant`·`rank_window_size` 기본값이 하이브리드 검색 페이지에 없음.
12. **Pinecone 최대 차원 미확보** — 인덱싱 개요 페이지에 dense 벡터 최대 차원 명시 없음.
13. **SPDX `NOASSERTION` 항목** — GitHub API가 라이선스를 판정하지 못한 항목(Elasticsearch, Redis/RediSearch, Meilisearch, pgvector, Langfuse, Phoenix, NeMo Guardrails, PurpleLlama, openai/evals)은 실제 라이선스 문구를 개별 확인하지 않았다. 본문에서 라이선스를 단정하지 말라.
14. **리포 이전(rename) 4건** — Ragas(`explodinggradients` → `vibrantlabsai`), NeMo Guardrails(`NVIDIA` → `NVIDIA-NeMo/Guardrails`), Chonkie(`chonkie-inc` → `feyninc`), 기타. 기존 URL은 리다이렉트되지만 **책에 URL을 박을 때 리다이렉트 후 주소를 쓰는 편이 안전**하다.

---

## 11. 미확인 항목 목록 (fact-checker 대조 기준 — 본문에서 단정 금지)

### 벤치마크 점수 (가장 위험)
- SWE-bench 리더보드 전 splits 최고 점수 — `미확인`
- GAIA 리더보드 전 점수 — `미확인`
- MTEB 리더보드 모델별 점수·순위 — `미확인`
- τ-bench / τ²-bench / τ³-bench 베이스라인 점수 — `미확인`
- WebArena 점수 — `미확인`
- AgentBench 점수 — `미확인`
- (확인된 유일 항목: Terminal-Bench 2.0 상위 10 — 2026-07-25 스냅샷)

### 임베딩·리랭커 가격·스펙 (두 번째로 위험)
- `text-embedding-ada-002` 단가 — `미확인`
- `text-embedding-ada-002` 차원 — `미확인` (가이드가 3-small/3-large 차원만 명시. 통념은 1,536이지만 이번 세션 미확인 — **본문에 1536을 박지 마라**)
- OpenAI moderation 가격 — "무료"만 확인, 세부 단가 `미확인`
- Langfuse 플랫폼↔SDK 버전 대응 관계 — `미확인` (계열이 셋으로 갈림)
- Cohere `embed-v4.0` 토큰 단가 — `미확인`
- Cohere `embed-*-v3.0` 계열 토큰 단가 — `미확인`
- Cohere `rerank-v4.0-pro` / `rerank-v4.0-fast` / `rerank-v3.5` 토큰 단가 — `미확인`
- Cohere `rerank-v4.0` 계열 컨텍스트 길이 — `미확인`
- Voyage `rerank-2.5` / `rerank-2.5-lite` 컨텍스트 길이 — `미확인`
- `voyage-context-4` 차원·컨텍스트 — `미확인`
- `voyage-4-nano` API 단가 — `미확인`
- `gemini-embedding-001` 차원·최대 입력 — `미확인`
- Jina `v5-omni` / `v5-text` 가격 — `미확인`
- Jina `v5-omni` Matryoshka 차원 하한 — `미확인`
- BGE 개별 모델 차원·컨텍스트 — `미확인`
- ColBERT 컨텍스트 — `미확인`
- Nomic Embed 모델명·차원·컨텍스트·라이선스 — `미확인` (문서 404)

### 버전
- pgvector 릴리스 발행일 — `미확인` (태그 `v0.8.5`만 확인, `releases/latest` 404)
- Azure AI Content Safety API 버전 — `미확인`
- Llama Guard 버전·파라미터 수·멀티모달·hazard 카테고리 수·라이선스명 — `미확인`
- Prompt Guard 버전 — `미확인`
- Lakera 버전·제품 상세 — `미확인`
- OpenAI Evals 버전 — `미확인` (릴리스·태그 미등록)
- Nomic Embed 버전 — `미확인`
- LanceDB 안정 릴리스 태그 — GitHub 최신 태그가 전부 beta (PyPI 0.34.0을 안정 기준으로 채택)
- Cognee 안정 릴리스 — 최신 태그가 `v1.4.0.dev0` (프리릴리스)
- GAIA 버전·라이선스 — `미확인`

### 매니지드 서비스 (버전 개념 없음 — 공백이 아니라 정답 셀)
- Pinecone, Turbopuffer, MongoDB Atlas Vector Search, LangSmith, Braintrust(플랫폼), Langfuse Cloud → `미확인 (managed service, 버전 개념 없음)`
- (셀프호스트 버전이 따로 있는 Langfuse는 `v3.224.1`로 별도 확인)

### 기타 스펙·수치
- 청킹 오버랩 권장 수치 — `미확인`
- Weaviate `alpha` 기본값 — `미확인`
- Elasticsearch `rank_constant` / `rank_window_size` 기본값 — `미확인`
- Pinecone dense 벡터 최대 차원 — `미확인`
- Turbopuffer per-GB / per-query / per-write 단가 — `미확인` (플랜 최소액만 확인: Launch $16/mo, Scale $256/mo, Enterprise ≥$4,096/mo + 35% 프리미엄)
- MongoDB Atlas 유사도 메트릭 종류 — `미확인`
- Langfuse 셀프호스팅 라이선스 종류 — `미확인` ("open source and you can self-host it for free"만 확인)
- Pinecone 청킹 문서 발행일 — `미확인`
- "정형 데이터는 SQL" 1차 소스 — `미확인`
- SPDX `NOASSERTION` 9건의 실제 라이선스 문구 — `미확인`

---

## 12. 집계

| 표 | 카테고리 | 도구 수 |
|----|---------|--------|
| 표 1 | 벡터 DB·검색 엔진 | 18 |
| 표 2 | 임베딩 모델 | 19 |
| 표 2-1 | 리랭커 | 7 |
| 표 3 | eval·관측성 | 15 |
| 표 4 | 에이전트 벤치마크 | 6 |
| 표 5 | 가드레일 | 10 |
| 표 6 | RAG 파이프라인·청킹 | 7 |
| **합계** | | **82** |

(표 2-2 MTEB는 표 3의 도구가 아니라 리더보드 현황 블록으로 별도 집계 제외. 표 1-1·5-1·6-1은 도구 표가 아닌 패턴·수치 표.)

**활동 신호 요약 (2026-07-25 기준)**
- 당일(2026-07-25) 푸시된 활발한 프로젝트: Qdrant, Weaviate, Milvus, Chroma, LanceDB, Vespa, Elasticsearch, Langfuse, Phoenix, Weave, Helicone, LlamaIndex, Haystack, Cognee, GraphRAG, NeMo Guardrails, OpenAI Agents SDK
- ⚠️ 정체(3개월 이상 푸시 없음): pgvectorscale(2026-04-30), Ragas(2026-02-24), OpenAI Evals(2026-04-14), SWE-bench(2026-04-01), AgentBench(2026-02-08), invariant(2026-01-12), sqlite-vec(2026-05-18), ColBERT(2025-10-14), rerankers(2025-12-20), WebArena(2025-11-26)
- ❌ 아카이브(죽은 프로젝트): **Rebuff** (`archived: true`, 마지막 릴리스 2024-01-20)
- 🔀 리포 이전: Ragas, NeMo Guardrails, Chonkie
- 📌 갓 나온 메이저: **Haystack v3.0.0 (2026-07-20, 5일 전)** — v2 기준 자료는 모두 구버전
