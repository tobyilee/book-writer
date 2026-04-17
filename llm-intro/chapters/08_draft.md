# 8장. RAG 최소 구현 — 파인튜닝보다 먼저

## 8.0 지금 우리가 어디에 있나

한 가지 상황을 상상해보자. 월요일 오전 팀장이 자리에 찾아와 이렇게 말한다. "우리 사내 개발 문서가 너무 많아졌어. LLM으로 Q&A 봇 하나 만들어볼래? 다음 주까지 데모." 당신은 고개를 끄덕이고 자리에 돌아왔다. 자, 어디서부터 시작할까?

머릿속에 떠오르는 선택지는 대략 네 가지다. 하나. 4장처럼 **밑바닥에서 모델을 훈련시킨다**. 둘. 6장에서 해본 대로 **오픈 모델을 파인튜닝한다**. 셋. 7장처럼 **API에 프롬프트 하나 잘 써서 던진다**. 넷. 이 장에서 배울 **RAG(Retrieval-Augmented Generation)로 푼다**.

같은 "사내 개발 문서 요약/Q&A"라는 공통 태스크가 2장부터 우리를 따라왔다. 4장에서는 작은 한국어 코퍼스로 미니 GPT를 처음부터 짰다. 6장에서는 Llama 3 8B에 QLoRA를 얹어봤다. 7장에서는 API를 한 줄로 호출해 같은 문제를 풀었다. 그리고 이번 장이 네 번째 답이다. **가장 실무에서 먼저 꺼내는 답**이기도 하다.

왜 "먼저"일까? 이 장에서 풀어낼 한 줄 결론을 미리 적어두면 이렇다.

> **첫 직감이 "fine-tune"이면 그건 빨간 깃발이다. 먼저 프롬프트와 RAG로 가볼 수 있는지 확인하는 편이 낫다.**

이 문장이 바로 **현장 실무 1원칙**이다(Reference 4.2). 어떤 사람은 이걸 "RAG 먼저"로 줄여 부르고, 어떤 사람은 "파인튜닝은 최후 수단"이라고 표현한다. 말은 다양하지만 가리키는 방향은 같다. 조직 내부 문서를 가지고 LLM에게 답을 시키고 싶다면, 90%의 경우 RAG가 먼저다.

이 장에서 같이 할 일은 이렇다. 첫째, "파인튜닝이냐 RAG냐" 판단 체크리스트를 편다. 둘째, RAG 파이프라인의 구성요소를 하나씩 열어본다. 청킹, 임베딩, 벡터 DB, 하이브리드 검색, 리랭커, 컨텍스트 주입과 출처 인용. 셋째, Python으로 최소 RAG 파이프라인을 직접 만든다. 넷째, 같은 파이프라인을 Spring AI `VectorStore`로 이식한다. 다섯째, 실패 패턴 셋과 평가 방법. 마지막으로, 4·6·7·8장의 네 해법을 한 장면에 겹쳐본다. 이 겹침이 9장 결정 플로차트로 넘어가는 다리다.

시작하기 전에 하나만 더 기억해두자. 이 장은 **"마법의 파이프라인"**을 보여주는 장이 아니다. RAG는 마법이 아니다. 문서 검색이라는 평범한 소프트웨어 공학이 LLM 앞에 끼어들어, 모델이 답하기 직전에 관련 문서를 손에 쥐여주는 구조일 뿐이다. 그 "평범함"을 잘 설계하는 일이 이 장 전체의 주제다. 같이 하나씩 쌓아 올려보자.

---

## 8.1 왜 RAG 먼저인가 — 파인튜닝과의 갈림길

먼저 한 발짝 물러나서 생각해보자. 어떤 문제를 왜 파인튜닝으로 풀면 곤란할까?

"사내 개발 문서 Q&A"를 예로 들어보자. 문서는 어제도 한 건 추가됐고, 오늘 아침 누군가 오래된 API 문서 두 건을 deprecated로 바꿨다. 다음 주에는 새 인프라 가이드 다섯 건이 올라온다. 문서는 살아 있고, 계속 움직인다.

이 문서들을 파인튜닝으로 모델 가중치에 새긴다고 해보자. 어떤 일이 벌어질까. 첫 번째, 문서가 바뀔 때마다 **재학습**이 필요하다. QLoRA 한 번 돌리는 데 GPU 시간과 비용이 든다(6장에서 확인했다). 두 번째, 모델이 "이 답이 어느 문서 어느 줄에서 왔는지"를 알려줄 방법이 사실상 없다. 파라미터 속에 녹아들어 버렸기 때문이다. **출처 추적이 불가능**하다는 뜻이다. 세 번째, 어제 추가된 문서가 오늘 답변에 반영되려면 또 재학습. 네 번째, 파인튜닝된 가중치는 "이 문서는 옛날 것이니 무시해라" 같은 동적 제어가 어렵다.

반면 RAG는 어떤가. 새 문서가 추가되면 벡터 저장소에 `add(document)` 한 번 호출이면 끝이다. 모델 가중치는 건드리지 않는다. 답변마다 검색에 걸린 문서를 출처로 붙여줄 수 있다. 오래된 문서에 `deprecated: true` 메타데이터 하나 박아두면 필터로 걸러진다. 같은 Q&A 봇을 조직 내 다른 팀에 이식할 때도 **문서만 갈아끼우면** 된다.

두 접근의 역할을 한 표로 정리해두자. 실무에서 여러 번 꺼내 볼 표다.

| 비교 축 | 파인튜닝 (QLoRA 등) | RAG |
|---|---|---|
| 배우는 것 | 톤, 스타일, 구조, 반복 패턴 | 사실, 최신 지식, 조직 내부 문서 |
| 데이터 갱신 | 재학습 필요 | 벡터 저장소에 추가 |
| 출처 추적 | 사실상 불가 | 검색 문서 그대로 인용 가능 |
| 환각 제어 | 간접 | 직접 (근거 문서 유무로) |
| 초기 비용 | GPU·시간·데이터 셋 | 벡터 DB + 임베딩 API |
| 바뀌는 대상 | 모델 가중치 | 지식 베이스 |
| 버그 수습 | 재학습 | 문서 수정 |

눈여겨볼 지점은 **왼쪽과 오른쪽이 푸는 문제가 다르다**는 것이다. 파인튜닝은 **"어떻게 말할 것인가"**를 배우는 도구다. 회사 특유의 응답 톤, 특정 JSON 스키마, 금융 도메인의 완곡한 표현. 이런 건 RAG로 못 푼다. 한편 RAG는 **"무엇을 말할 것인가"**의 정확성을 지키는 도구다. "우리 회사 결제 API의 최대 재시도 횟수는 몇 번이냐"에 대한 답이 가중치에 녹아 있을 이유가 없다. 문서에 적혀 있으면 된다.

현장 합의는 이렇게 수렴한다. **RAG가 먼저, 톤이 정말 중요하면 파인튜닝 얹기, 하이브리드가 종점**. 국내 기술 블로그도 대체로 이 지형을 따라간다. 카카오페이, 당근, 토스 모두 "먼저 RAG로 얼마나 가는지 보고, 부족한 부분만 파인튜닝으로 메운다"는 순서를 기본값으로 둔다(Reference 4.2).

### "첫 직감이 fine-tune이면 red flag" — 판단 체크리스트

자리에 앉은 김에 짧은 체크리스트를 펴보자. 팀원이 "그거 파인튜닝해야 하지 않아요?"라고 말할 때, 다음 여섯 항목을 먼저 물어보는 편이 낫다.

1. **데이터가 자주 바뀌는가?** (매주/매일 갱신된다면 → RAG)
2. **출처 인용이 필요한가?** (감사, 규제, 금융, 의료 등 → RAG)
3. **문서가 조직 내부에서 흩어져 있는가?** (위키, Confluence, Notion, GitHub wiki → RAG)
4. **원하는 것이 "특정한 말투/스키마"인가?** (공식 답변 포맷, 고객 응대 톤 → 파인튜닝 고려)
5. **아주 반복적인 task를 inline 지시 없이 재현해야 하는가?** (매번 프롬프트가 길어진다면 → 파인튜닝 고려)
6. **16GB 이상의 VRAM과 며칠의 학습 시간이 확보되어 있는가?** (없다면 → RAG가 현실적)

여섯 항목 중 1·2·3 중 하나라도 해당하면 RAG가 먼저다. 4·5가 강하고 1~3이 약할 때만 파인튜닝을 저울에 올린다. 그리고 실무에서 정말 자주 놓치는 지점—**체크리스트를 돌려본 적 없이 "당연히 파인튜닝해야지"로 점프**하는 그 순간이 빨간 깃발이다. 이 책의 독자라면 여기서 잠깐 멈추고 체크리스트를 펴는 습관을 들여두자.

좋다. 철학은 충분히 깔았다. 그럼 RAG가 실제로 어떤 부품들로 이루어져 있는지, 한 부품씩 열어보자.

---

## 8.2 RAG 파이프라인의 해부

RAG 파이프라인은 크게 두 단계로 나뉜다. **인덱싱(indexing)**과 **검색+생성(retrieve + generate)**. 박스 그림으로 그리면 이런 모양이다.

```text
[인덱싱 단계 — 사전에 한 번]
  문서 → 로더 → 청킹 → 임베딩 → 벡터 저장소

[질의 단계 — 매 요청마다]
  질문 → 임베딩 → 벡터 검색 → (+ BM25) → 리랭커 → 컨텍스트 주입 → LLM → 답변 + 출처
```

인덱싱은 사전 작업이다. 사내 문서 500건이 있다면 한 번에 처리해서 벡터 저장소에 넣어둔다. 질의는 매번의 요청마다 발동한다. 사용자 질문 → 관련 문서 검색 → 프롬프트에 끼워넣기 → LLM 호출 → 답변. 이 사이클이 RAG의 전부다. 각 단계를 차례로 열어보자.

### 8.2.1 청킹(chunking) — 문서를 어떻게 자를 것인가

"사내 API 가이드" PDF 하나를 통째로 LLM에 넣을 수는 없다. 컨텍스트 창이 128K 토큰이라 해도 500쪽짜리 문서 수십 개를 한꺼번에 넣기는 빡빡하다. 더 중요하게는, **LLM은 관련 없는 긴 컨텍스트에서 오히려 혼란스러워한다**. 짧고 관련성 높은 청크 5~8개가 긴 통문서 하나보다 답변 품질이 낫다. 그래서 문서를 **청크(chunk)**로 쪼갠다.

청크 크기 결정에는 갈림길이 있다. 너무 크면 한 청크 안에 주제가 여럿 섞여 임베딩 벡터가 흐려진다. 너무 작으면 맥락이 잘려서 검색된 청크만으로는 답을 못 만든다. 현장 휴리스틱은 대략 이렇게 수렴한다.

- **문장/문단 단위 (100~300 토큰):** Q&A처럼 답이 한 문단 안에 있는 경우 적합.
- **섹션 단위 (500~1000 토큰):** 기술 문서, 가이드류. 가장 흔한 기본값.
- **페이지/문서 단위 (1500+ 토큰):** 사례별로 맥락이 길게 필요한 경우.

권장 기본값은 **"500~800 토큰, 10~20% 오버랩"**이다. 오버랩은 청크 경계에 걸친 문장이 양쪽에 모두 포함되도록 하는 트릭이다. `청크1: [A B C D E]`, `청크2: [D E F G H]` 같은 식이다. 이렇게 하면 경계선 근처의 질문도 놓치지 않는다.

주의할 점 하나. **JSON, 표, 코드 블록은 임의로 쪼개면 안 된다.** 당근페이 FDS 사례가 정확히 이 함정에 빠졌다. RAG retrieve 결과의 JSON이 중간에서 잘려 반환되는 일이 벌어졌고, 결국 "사기 케이스별 파일 1개 = 청크 1개, `ChunkingStrategy=NONE`"로 재설계해야 했다(supplementary_gap3 1.2). 구조가 있는 데이터는 구조 단위로 청킹하는 편이 낫다. Markdown은 헤더 단위, 코드는 함수 단위, JSON은 레코드 단위. 이걸 **의미 단위 청킹(semantic chunking)**이라 부른다.

### 8.2.2 임베딩 모델 선택 — BERT 계열이 여기서 본격 등장한다

3장에서 트랜스포머 아키텍처 세 변형을 비교하며 **BERT(encoder-only)는 "검색·임베딩에 지금도 쓰인다" 한 줄**만 남기고 넘어갔던 걸 기억하자. 그 한 줄을 지금 펼친다. 본격 착지점이 8장 RAG다.

decoder-only LLM(GPT, Claude, Llama)이 "다음 토큰을 뽑는 일"에 특화됐다면, encoder-only 모델은 **"문장 전체의 의미를 하나의 벡터로 압축하는 일"**에 특화됐다. 이름도 그래서 "문장 임베딩 모델(sentence embedding model)" 또는 "인코더 모델"이라 부른다. 양쪽 방향으로 문맥을 본다는 점(bidirectional attention)이 decoder-only와 결정적으로 다르다. 검색용 임베딩에서는 이 양방향성이 유리하다. 한 문장을 "왼쪽에서 오른쪽으로" 한 번 훑고 끝나는 게 아니라, 문장 전체를 동시에 보며 핵심 의미를 벡터 한 개로 응축한다.

2025~2026년 실무에서 자주 만날 임베딩 모델은 대략 셋이다. 각각의 위치와 장단점을 정리해두자.

| 모델 | 제공자 | 차원 | 한국어 품질 | 호출 방식 | 특징 |
|---|---|---|---|---|---|
| `text-embedding-3-small` | OpenAI | 1536 | 중~상 | API 유료 | 영어 최적, 한국어도 무난. 저렴. |
| `text-embedding-3-large` | OpenAI | 3072 | 상 | API 유료 | 3-small의 약 6배 가격, 품질 향상. |
| `bge-m3` | BAAI (중국 AI연구원) | 1024 | 상 | 로컬/Ollama/HF | **다국어·한국어 최상위권**. 오픈 가중치. |
| `multilingual-e5-large` | Microsoft | 1024 | 상 | 로컬/HF | 100+ 언어, 한국어 경쟁력 있음. |

한국어 중심 서비스라면 **`bge-m3`가 현재의 실무 디폴트**에 가깝다. 이유가 몇 가지 있다. 첫째, 가중치가 공개되어 있어 Ollama·HuggingFace로 로컬 호스팅이 가능하다. 즉, 사내 문서를 외부 API로 보내지 않아도 된다(보안). 둘째, 다국어·한국어 벤치마크에서 최상위권. 셋째, 한 모델로 **dense 검색, sparse 검색(lexical), multi-vector 검색을 모두 지원**한다. 하이브리드 검색을 한 번에 받는 모델이 `bge-m3`다.

OpenAI `text-embedding-3-small`은 반대편 선택이다. 사내 보안 정책이 외부 API를 허용하고, 초기 개발 속도가 우선이라면 합리적이다. 1000 토큰당 $0.00002 수준으로 저렴한 편이다. 다만 한국어 품질은 `bge-m3` 대비 "무난"한 정도. 사내 문서가 한국어라면 결과물의 검색 정확도를 꼭 골든셋으로 비교해보자. 이 책의 실습에서는 **디폴트로 `bge-m3`**를 쓰되, 빠른 데모를 위해 OpenAI 대안 경로도 함께 남겨둔다.

하나 기억해둘 원칙이 있다. **질문과 문서는 반드시 같은 임베딩 모델로 벡터화해야 한다.** 질문은 `text-embedding-3-small`로 뽑고 문서는 `bge-m3`로 뽑으면, 두 벡터가 서로 다른 공간에 찍힌다. 검색 자체가 의미를 잃는다. 당연한 이야기 같지만 배포 중에 모델을 바꾸고 인덱스를 다시 만들지 않아 사고가 나는 사례가 의외로 많다. 임베딩 모델을 바꾸면 **인덱스 전체를 재생성**한다고 기억해두자.

### 8.2.3 벡터 DB 선택 — pgvector · Chroma · Qdrant 3종 비교

임베딩을 만들었으면 저장할 곳이 필요하다. 수십만~수백만 개의 1024차원 벡터를 빠르게 유사도 검색할 수 있는 저장소. 이걸 벡터 DB(vector database)라 부른다. 현장에서 자주 만나는 세 가지를 놓고 비교해보자.

| 항목 | pgvector | Chroma | Qdrant |
|---|---|---|---|
| 형태 | PostgreSQL 확장 | Python 임베디드/서버 | Rust 서버 |
| 설치 | 기존 PG에 `CREATE EXTENSION vector` | `pip install chromadb` | Docker 한 줄 |
| 운영 친숙도 | 매우 높음 (백엔드 개발자) | 매우 낮음 (거의 파이썬 객체) | 중간 |
| 스케일 | 수천만 벡터까지 무난 | 로컬/프로토타입 규모 | 수천만~수억 벡터 |
| 하이브리드 검색 | 가능 (full-text search 조합) | 메타 필터만 | BM25 통합 |
| Spring AI 지원 | O (공식) | O | O |
| 추천 지점 | **Java 백엔드와 같이 산다**면 1순위 | 빠른 프로토타입 | 대규모 운영 |

실무 조언 하나. **이미 PostgreSQL을 쓰고 있다면 pgvector가 거의 언제나 정답이다.** 새 인프라를 하나 더 도입할 이유가 약하다. 같은 DB에서 `users` 테이블과 `document_chunks` 테이블이 같이 살면, 트랜잭션·백업·관측성 모두 기존 운영 루틴을 그대로 쓴다. "벡터 DB는 설치하면 끝"이라는 경시가 SK하이닉스 연구 사례에서 드러난 함정이기도 하다—메모리 용량이 부족하면 **검색 시간이 0.088초에서 122.06초로 약 1300배 폭증**한다(supplementary_gap3 1.3). 운영 친숙도가 왜 중요한지를 숫자로 보여주는 사례다.

프로토타입 단계라면 Chroma가 가장 빠르다. `pip install chromadb` 한 줄로 끝난다. 몇 달 돌려보고 스케일이 필요해지면 pgvector나 Qdrant로 이전하는 경로가 무난하다. 이 장의 Python 실습에서는 **Chroma로 프로토타입**하고, Java 실습에서는 **pgvector로 운영형**으로 옮긴다. 같은 파이프라인의 두 얼굴이다.

Spring AI는 이 셋을 모두 `VectorStore` 인터페이스 뒤로 추상화해둔다. 구현체만 갈아끼우면 pgvector ↔ Chroma ↔ Qdrant 스왑이 의존성 한 줄로 된다(Reference 2.5). 7장에서 봤던 `ChatClient`와 같은 철학이다. 개념에 집중하고 구현체는 언제든 갈아끼울 수 있도록 설계되어 있다.

### 8.2.4 하이브리드 검색 — BM25 + 벡터

벡터 검색은 "의미가 비슷한" 문서를 잘 찾는다. `"로그인 오류"`와 `"인증 실패"`는 벡터 공간에서 가깝다. 그런데 벡터 검색이 약한 지점이 하나 있다. **고유명사·코드·오타·약어 같은 "정확 매칭"**이다. `"PAY-ERR-7103"` 같은 에러 코드로 검색하면 벡터가 의미를 잘 못 잡는다. 여기서는 오히려 **전통적 키워드 검색(BM25)**이 강하다.

그래서 실전 RAG는 둘을 섞어 쓴다. **하이브리드 검색(hybrid retrieval)**이라 부른다. 벡터 점수와 BM25 점수를 각각 구하고, 가중 합산 또는 상호 순위 결합(Reciprocal Rank Fusion, RRF)으로 최종 순위를 매긴다. 공식은 이런 모양이다.

```text
final_score(doc) = α · vector_score(doc) + (1 - α) · bm25_score(doc)
또는
RRF_score(doc) = Σ_ranker 1 / (k + rank_ranker(doc))
```

`α`를 튜닝해가며 골든셋에서 최적을 찾는다. 경험적으로 `α ≈ 0.5~0.7`이 시작점으로 무난하다. RRF는 가중치 튜닝 없이도 꽤 잘 작동한다는 장점이 있어 최근 선호되는 방식이다.

smallcherry의 패널 토크 후기에 이런 문장이 있다. "벡터 검색만으로 충분, 키워드 필요 없음"이라는 가정이 현장에서 깨졌다는 관찰이다(supplementary_gap3 1.6). 사내 문서에는 약어·버전 번호·티켓 ID가 빽빽하다. 하이브리드 검색을 기본으로 두는 편이 낫다.

### 8.2.5 리랭커 — 상위 후보를 한 번 더 줄 세우기

벡터 검색으로 Top 20을 꺼냈다고 하자. 이 중 LLM 컨텍스트에 실제로 넣을 건 5개 정도다. 어떻게 고를까? 가장 단순한 방법은 벡터 유사도 순으로 자르는 것이다. 그런데 벡터는 "빠르게 비슷한 것"을 잘 찾을 뿐, "어느 것이 가장 질문에 정확히 답하는가"를 판단하는 데는 약하다.

여기서 **리랭커(reranker)**가 들어온다. 리랭커는 **질문-문서 쌍을 입력으로 받아 관련성 점수 하나를 뱉는 별도의 모델**이다. 보통 크로스 인코더(cross-encoder) 구조다. 질문과 문서를 **함께** 인코딩해서 둘 사이의 상호작용을 본다. 임베딩 기반 검색(bi-encoder)이 질문과 문서를 **따로** 벡터화하는 것과 대비된다.

```text
bi-encoder  : 질문 → 벡터 A,  문서 → 벡터 B,  유사도(A, B)
cross-encoder: (질문, 문서) → 관련성 점수
```

크로스 인코더는 느리다. 쿼리당 Top 20만 해도 20번의 모델 호출이 필요하다. 그래서 전체 검색에는 쓰지 않고, **"빠른 검색으로 후보 20개를 뽑고, 느린 리랭커로 5개로 좁힌다"**는 2단 구조가 표준이다. `bge-reranker-v2-m3` 같은 모델이 이 용도로 자주 쓰인다.

리랭커는 RAG 품질을 올리는 가성비 좋은 장치다. 단, 없어도 쓸 만한 RAG는 만들 수 있다. 이 장 실습에서는 기본 파이프라인을 먼저 완성하고, 리랭커는 "품질을 더 올리고 싶을 때" 끼워넣는 옵션으로 소개한다.

### 8.2.6 컨텍스트 주입과 출처 인용

검색으로 상위 청크 5개를 확보했다. 이제 LLM에게 넘길 차례다. 프롬프트 설계가 의외로 결과 품질을 크게 좌우한다. 기본형은 이런 모양이다.

```text
[시스템]
당신은 사내 개발 문서 Q&A 어시스턴트다.
아래 제공된 문서 안에서만 답변한다. 문서에 없는 내용은 "문서에서 찾을 수 없습니다"라고 답한다.
답변 끝에 참고한 문서 번호를 [1][3] 같은 형식으로 표시한다.

[문서 1] (출처: api-guide.md, 섹션 "재시도")
…내용…

[문서 2] (출처: infra/db.md)
…내용…

[질문]
우리 결제 API의 최대 재시도 횟수는?
```

몇 가지 원칙이 녹아 있다. 첫째, **"제공된 문서 안에서만 답하라"**를 명시적으로 지시한다. 이 한 줄이 없으면 모델은 학습 때 배운 일반 지식으로 떼워 답하는 경향이 있다. 둘째, **"없으면 없다고 답하라"**를 허용한다. 이게 없으면 모델은 어떻게든 답을 쥐어짜낸다. 셋째, **문서마다 출처를 같이 박아둔다**. 사용자는 "LLM이 이렇게 말했다"만 보는 게 아니라 "어느 문서의 어느 섹션에서 왔다"를 같이 본다. 신뢰성의 근거다.

카카오페이 춘시리 팀이 남긴 문장이 의미심장하다. "증권사에서 AI를 도입하며 가장 어려웠던 측면은 아무래도 보안이었습니다"(supplementary_gap3 1.4). RAG에서 보안·신뢰의 시작점은 **출처 인용**이다. 출처가 없으면 감사도, 디버깅도, 사용자 설득도 불가능하다. 이 부분은 뒤에서 실패 패턴으로도 다시 만난다.

자, 구성요소 해부는 여기까지다. 이제 직접 손으로 만들어보자.

---

## 8.3 Python 실습 — LangChain으로 최소 RAG 파이프라인 만들기

"사내 개발 문서" 자리에 무엇을 놓을까. 이 실습에서는 Markdown 파일 다섯 개로 구성된 가짜 사내 위키를 만들어 쓴다. 실제 조직에서는 이 자리에 Confluence 페이지 덤프, GitHub wiki, Notion 내보내기가 들어온다. 구조는 동일하다.

준비물은 이렇다. 환경은 Python 3.11+ 기준이다.

```bash
pip install langchain langchain-community langchain-openai langchain-chroma
pip install chromadb sentence-transformers
pip install pypdf unstructured markdown
```

실습 디렉토리 구조는 이렇게 잡는다.

```text
rag-demo/
├── docs/
│   ├── api-guide.md
│   ├── db-migration.md
│   ├── deploy-checklist.md
│   ├── incident-runbook.md
│   └── oncall-rotation.md
├── rag.py
└── eval_set.json
```

`docs/` 아래의 다섯 파일은 독자가 사내 위키에서 실제 문서 몇 개를 복사해 넣어도 되고, 이 책 저장소의 샘플을 써도 된다. 각 파일은 평범한 Markdown이다. 헤더, 본문, 표, 코드 블록이 섞여 있다.

### 8.3.1 인덱싱 파이프라인

아래 스크립트는 `docs/` 전체를 로드해서 청킹하고, `bge-m3`로 임베딩한 뒤 Chroma에 저장한다. 핵심 로직은 40줄 안에 들어온다.

```python
# rag.py  (인덱싱 부분)
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DOCS_DIR = Path("docs")
CHROMA_DIR = Path(".chroma")
COLLECTION = "dev-wiki"


def build_index() -> Chroma:
    # 1) 문서 로드
    loader = DirectoryLoader(
        str(DOCS_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()

    # 2) 청킹: 500자 ±10% 오버랩, 마크다운 친화 분할
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"문서 {len(documents)}개 → 청크 {len(chunks)}개")

    # 3) 임베딩 모델: bge-m3 (한국어·다국어 강점)
    embedder = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        encode_kwargs={"normalize_embeddings": True},
    )

    # 4) Chroma에 영속 저장
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedder,
        collection_name=COLLECTION,
        persist_directory=str(CHROMA_DIR),
    )
    return vectorstore
```

몇 가지 실무 포인트가 코드에 녹아 있다.

- `RecursiveCharacterTextSplitter`의 `separators`에 Markdown 헤더(`\n## `, `\n### `)를 앞쪽에 놓았다. 헤더를 우선 경계로 잡아 섹션 단위 청킹에 가깝게 만드는 트릭이다.
- `chunk_size=500, chunk_overlap=50`. 한국어에서 500자는 대략 250~400 토큰 사이. 실습에 적당한 크기다.
- `normalize_embeddings=True`. 벡터를 단위 길이로 정규화하면 코사인 유사도 계산이 내적과 같아져서 성능상 유리하다. `bge-m3` 공식 권장 설정이기도 하다.
- `persist_directory`. Chroma가 로컬 디스크에 인덱스를 저장한다. 스크립트 재실행 때 인덱싱을 건너뛸 수 있도록.

GPU 없는 환경이라면 `bge-m3` 로딩이 CPU에서 느릴 수 있다. Colab 무료 T4에서는 1~2분이면 충분하고, M 시리즈 Mac에서도 MPS로 자동 가속된다. 정말 GPU가 안 된다면 대안은 OpenAI 임베딩 API다.

```python
# 대안: OpenAI API로 임베딩
from langchain_openai import OpenAIEmbeddings

embedder = OpenAIEmbeddings(model="text-embedding-3-small")
```

한 줄만 바꾸면 된다. 다만 이 경우 사내 문서가 외부 API로 나간다는 점을 보안 담당자와 먼저 합의해야 한다. 업무 문서의 외부 전송이 금지된 조직에서는 로컬 `bge-m3`가 유일한 선택지다.

### 8.3.2 검색 + 생성 파이프라인

인덱스가 만들어졌으니, 질문이 들어왔을 때 검색하고 LLM에 넘기는 부분을 쓴다.

```python
# rag.py  (질의 부분)
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


SYSTEM_PROMPT = """\
당신은 사내 개발 문서 Q&A 어시스턴트다.
아래 제공된 문서 안에서만 답변한다.
문서에 없는 내용은 "문서에서 찾을 수 없습니다"라고만 답한다.
답변 끝에 참고한 문서 번호를 [1][2] 형식으로 표시한다.
"""

USER_PROMPT = """\
[문서]
{context}

[질문]
{question}
"""


def format_context(docs) -> str:
    lines = []
    for i, d in enumerate(docs, start=1):
        source = d.metadata.get("source", "unknown")
        lines.append(f"[문서 {i}] (출처: {source})\n{d.page_content}")
    return "\n\n".join(lines)


def answer(vectorstore: Chroma, question: str, k: int = 5) -> dict:
    # 1) 벡터 검색 Top-k
    docs = vectorstore.similarity_search(question, k=k)

    # 2) 프롬프트 구성
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", USER_PROMPT),
    ])
    messages = prompt.format_messages(
        context=format_context(docs),
        question=question,
    )

    # 3) LLM 호출 (OpenAI 예시; Anthropic으로 교체 가능)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = llm.invoke(messages)

    # 4) 답변 + 출처 반환
    sources = [d.metadata.get("source", "unknown") for d in docs]
    return {"answer": response.content, "sources": sources}


if __name__ == "__main__":
    vs = build_index()
    result = answer(vs, "우리 결제 API의 최대 재시도 횟수는?")
    print(result["answer"])
    print("출처:", result["sources"])
```

실행 로그는 대략 이런 모양이다.

```text
$ python rag.py
문서 5개 → 청크 37개
답변: 결제 API의 최대 재시도 횟수는 3회이며, 지수 백오프(exponential backoff)로
 1초, 2초, 4초 간격으로 재시도합니다. [1]
출처: ['docs/api-guide.md', 'docs/incident-runbook.md', ...]
```

여기서 몇 가지가 동시에 일어났다. 질문이 `bge-m3`로 벡터화됐고, Chroma가 Top 5 청크를 꺼냈고, 그 청크들이 프롬프트 `[문서 1]`, `[문서 2]` 자리에 들어갔고, GPT-4o-mini가 "문서 안에서만" 답을 만들었다. 답변 끝의 `[1]`은 모델이 첫 번째 문서를 참조했다고 스스로 표시한 부분이다.

### 8.3.3 하이브리드 검색과 리랭커 얹기

기본 파이프라인이 돌면, 품질을 한 단계 올리는 두 장치가 남아 있다. **하이브리드 검색**과 **리랭커**다. 선택 사항이지만 실무에서 종종 차이를 만든다.

```python
# 하이브리드 검색: 벡터 + BM25
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever


def build_hybrid_retriever(vectorstore: Chroma, chunks, k: int = 5):
    # BM25 인덱스 (키워드 검색)
    bm25 = BM25Retriever.from_documents(chunks)
    bm25.k = k

    # 벡터 리트리버
    dense = vectorstore.as_retriever(search_kwargs={"k": k})

    # 앙상블: 벡터 0.6 + BM25 0.4
    return EnsembleRetriever(
        retrievers=[dense, bm25],
        weights=[0.6, 0.4],
    )
```

`EnsembleRetriever`가 내부적으로 RRF를 써서 두 순위를 합친다. `"PAY-ERR-7103"` 같은 고유 코드가 질문에 들어오면 BM25가 꺼내고, `"결제 오류 복구 절차"` 같은 의미 질문은 벡터가 꺼낸다. 두 쪽 다 놓치지 않는다.

리랭커도 얹을 수 있다. `bge-reranker-v2-m3`를 크로스 인코더로 불러와 Top 20을 Top 5로 줄 세운다.

```python
# 리랭커: 크로스 인코더로 상위 후보 재정렬
from sentence_transformers import CrossEncoder


def rerank(query: str, docs, top_n: int = 5):
    model = CrossEncoder("BAAI/bge-reranker-v2-m3")
    pairs = [(query, d.page_content) for d in docs]
    scores = model.predict(pairs)
    ranked = sorted(zip(docs, scores), key=lambda x: -x[1])
    return [d for d, _ in ranked[:top_n]]
```

리랭커는 쿼리당 Top 20이면 20번의 forward pass가 일어난다. Colab T4에서도 100~300ms 수준이라 실시간 Q&A에 감당 가능하다. 품질 향상은 골든셋에서 대략 Hit@5가 +5~10%p 올라가는 체감이 보통이다. 없어도 되지만, 있으면 좋은 부품.

여기까지 Python 파이프라인은 완성됐다. 이제 같은 파이프라인을 **Java 서비스에 붙여볼** 차례다.

---

## 8.4 Java 실습 — Spring AI로 같은 파이프라인 이식

7장에서 `ChatClient`로 LLM을 호출했던 Java 코드 기억하는가. Spring AI는 그 위에 `VectorStore` 추상을 하나 더 얹어서 RAG를 **거의 자연스러운 Spring 빈 주입**처럼 만든다. 같은 사내 문서 Q&A를 Spring Boot 3.x + Spring AI 1.x + pgvector로 옮겨보자.

### 8.4.1 의존성과 설정

`pom.xml`에 Spring AI의 pgvector 스타터를 추가한다.

```xml
<!-- pom.xml 일부 -->
<dependency>
  <groupId>org.springframework.ai</groupId>
  <artifactId>spring-ai-openai-spring-boot-starter</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.ai</groupId>
  <artifactId>spring-ai-pgvector-store-spring-boot-starter</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.ai</groupId>
  <artifactId>spring-ai-advisors-vector-store</artifactId>
</dependency>
```

`application.yml`에서 DB와 임베딩 모델을 설정한다.

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/ragdb
    username: rag
    password: rag
  ai:
    openai:
      api-key: ${OPENAI_API_KEY}
      embedding:
        options:
          model: text-embedding-3-small
    vectorstore:
      pgvector:
        index-type: hnsw
        distance-type: cosine_distance
        dimensions: 1536
```

PostgreSQL 쪽은 `CREATE EXTENSION vector;` 한 줄로 pgvector가 붙는다. 기존 운영 DB에 추가 테이블 하나 더 생긴다고 생각하면 된다. 임베딩 모델로는 설정 간결성을 위해 OpenAI `text-embedding-3-small`을 썼다. 보안 요건이 엄격하면 Ollama 스타터를 추가하고 `bge-m3`를 로컬 호스팅으로 돌리면 된다. Spring AI는 이걸 의존성 스왑 한 줄로 해준다.

### 8.4.2 인덱싱 서비스

`VectorStore`가 빈으로 자동 주입된다. 문서 하나를 넣는 코드는 이렇게 간결하다.

```java
@Service
@RequiredArgsConstructor
public class DocIndexer {

    private final VectorStore vectorStore;
    private final TokenTextSplitter splitter = new TokenTextSplitter(500, 50, 5, 10000, true);

    public void index(Path docsDir) throws IOException {
        List<Document> loaded = new ArrayList<>();
        try (Stream<Path> paths = Files.walk(docsDir)) {
            paths.filter(p -> p.toString().endsWith(".md")).forEach(p -> {
                String content = readString(p);
                loaded.add(new Document(content, Map.of("source", p.toString())));
            });
        }

        // 청킹
        List<Document> chunks = splitter.apply(loaded);

        // 벡터 저장소에 추가 (임베딩은 Spring AI가 자동 호출)
        vectorStore.add(chunks);
    }

    private static String readString(Path p) {
        try { return Files.readString(p, StandardCharsets.UTF_8); }
        catch (IOException e) { throw new UncheckedIOException(e); }
    }
}
```

`TokenTextSplitter`의 인자는 순서대로 `(chunkSize, chunkOverlap, minChunkSize, maxNumChunks, keepSeparator)`다. 500 토큰 ±50 토큰 오버랩 설정이 Python 쪽의 `RecursiveCharacterTextSplitter`와 대략 대응된다. `vectorStore.add(chunks)` 호출이 내부적으로 임베딩 API를 돌리고 pgvector에 INSERT를 실행한다. 한 줄이다.

### 8.4.3 질의 서비스 — `QuestionAnswerAdvisor`

Spring AI의 매력이 드러나는 지점이다. RAG 질의 전체 흐름을 `QuestionAnswerAdvisor`가 담당한다. `ChatClient`에 advisor로 끼우기만 하면 된다.

```java
@Service
@RequiredArgsConstructor
public class RagService {

    private final ChatClient.Builder builder;
    private final VectorStore vectorStore;

    public Answer ask(String question) {
        ChatClient chatClient = builder
            .defaultSystem("""
                당신은 사내 개발 문서 Q&A 어시스턴트다.
                아래 제공된 문서 안에서만 답변한다.
                문서에 없으면 "문서에서 찾을 수 없습니다"라고만 답한다.
                답변 끝에 참고한 문서의 출처(source)를 목록으로 표시한다.
                """)
            .defaultAdvisors(
                QuestionAnswerAdvisor.builder(vectorStore)
                    .searchRequest(SearchRequest.builder().topK(5).build())
                    .build()
            )
            .build();

        String answer = chatClient.prompt()
            .user(question)
            .call()
            .content();

        // 사용된 문서 출처는 advisor 컨텍스트에서 꺼낼 수 있다
        return new Answer(answer, List.of());
    }

    public record Answer(String content, List<String> sources) {}
}
```

실행 흐름은 이렇다.

1. 사용자 질문이 `ChatClient`에 들어온다.
2. `QuestionAnswerAdvisor`가 가로채서 `VectorStore.similaritySearch(question, topK=5)`를 부른다.
3. 검색된 문서가 시스템 프롬프트에 자동 주입된다.
4. OpenAI `ChatModel`이 답변을 생성한다.
5. `.content()`로 최종 답변을 받는다.

Python에서 수동으로 짰던 `format_context → prompt → invoke` 사이클이 advisor 한 줄로 축약됐다. **저자가 "Spring AI 맛 들렸다"는 느낌을 받는 지점이 여기다.** 인프라 설정(YAML)과 빈 주입(어노테이션)만 잘하면 도메인 로직은 거의 선언적이다.

Provider 스왑 데모도 잊지 말자. 7장에서 본 것처럼, `spring-ai-openai-*` 대신 `spring-ai-anthropic-*`을 의존성에 넣고 `application.yml`에서 모델명만 바꾸면, 위 `RagService` 코드는 **한 글자도 수정하지 않고** Claude로 갈아탄다. 벡터 DB도 마찬가지다. pgvector 스타터를 Chroma 스타터로 바꾸면 같은 `VectorStore` 빈이 Chroma 구현체로 주입된다.

### 8.4.4 REST 엔드포인트 붙이기

서비스에 붙인다면 컨트롤러 하나로 끝난다.

```java
@RestController
@RequestMapping("/api/rag")
@RequiredArgsConstructor
public class RagController {

    private final RagService rag;

    @PostMapping("/ask")
    public RagService.Answer ask(@RequestBody AskRequest req) {
        return rag.ask(req.question());
    }

    public record AskRequest(String question) {}
}
```

그리고 curl 한 줄.

```bash
curl -X POST http://localhost:8080/api/rag/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "우리 결제 API의 최대 재시도 횟수는?"}'
```

응답은 JSON이다.

```json
{
  "content": "결제 API의 최대 재시도 횟수는 3회이며, 1초/2초/4초 간격의 지수 백오프를 씁니다. [1]",
  "sources": ["docs/api-guide.md"]
}
```

이 네 개 파일—`DocIndexer`, `RagService`, `RagController`, `application.yml`—만 있으면 **사내 Q&A 봇의 80%가 완성**된다. 나머지 20%는 문서 동기화 스케줄러, 인증, 레이트 리미트, 관측성 연결이다. 이건 7장 Spring AI Observation에서 이미 본 궤도 위에 있다.

---

## 8.5 평가 — 골든셋으로 Hit@k 재보기

파이프라인이 돌기 시작했으면 다음 질문은 "얼마나 잘 도나"이다. 감으로 만져보면 "오, 잘되네"라고 말하게 되는데, 이게 가장 위험한 순간이다. 사용자가 들어오면 감이 틀어진다. 그래서 작은 **골든셋(golden set)**을 만들어 정량 측정 해두는 편이 낫다.

골든셋은 거창할 필요 없다. 사내 문서에서 **"실제로 사람이 물어볼 법한 질문 20개"**를 뽑고, 각 질문마다 "이 답이 있을 것으로 기대되는 문서"를 정답으로 표시한다. 이런 JSON 하나면 된다.

```json
[
  {
    "question": "결제 API의 최대 재시도 횟수는?",
    "expected_sources": ["docs/api-guide.md"]
  },
  {
    "question": "DB 마이그레이션 중 롤백 절차는?",
    "expected_sources": ["docs/db-migration.md", "docs/incident-runbook.md"]
  },
  ...
]
```

그리고 두 가지를 잰다.

- **Hit@k:** 검색 결과 Top-k 안에 `expected_sources` 중 하나라도 들어 있으면 히트. k=3, 5, 10으로 각각 잰다.
- **응답 품질:** LLM이 만든 답을 사람이 읽고 1~5점 채점. 20개면 한 사람이 20분 안에 본다.

```python
def evaluate(vectorstore, eval_set, k=5):
    hits = 0
    for item in eval_set:
        docs = vectorstore.similarity_search(item["question"], k=k)
        retrieved = {d.metadata.get("source") for d in docs}
        if retrieved & set(item["expected_sources"]):
            hits += 1
    return hits / len(eval_set)
```

실행 결과로 `Hit@5 = 0.85`가 나왔다면, 20개 중 17개 질문이 Top 5 안에 정답 문서를 포함했다는 뜻이다. 80% 이상이면 프로토타입으로는 합격선. 90% 이상이면 프로덕션 후보. 이 수치 자체가 목적이 아니라, **설정을 바꿨을 때 올라가는지 내려가는지를 재현 가능하게 보기 위한 기준선**이다.

청크 크기를 500 → 300으로 바꾸면 Hit@5가 어디로? 하이브리드 검색을 켜면? 리랭커를 얹으면? 매번 골든셋에 돌려보고 숫자를 본다. **감이 아니라 숫자로** 튜닝하자. smallcherry의 패널 후기에서 "도메인 전문가가 검증한 Golden Dataset"이 왜 중요한지를 강조한 것도 같은 맥락이다(supplementary_gap3 1.6). LLM이 생성한 Silver dataset만으로는 실제 사용자 질문의 분포를 못 잡는다.

응답 품질 수작업 채점표는 대략 이렇게 써본다.

| 항목 | 배점 | 채점 기준 |
|---|---|---|
| 사실 정확성 | 2점 | 문서 근거와 일치하는가 |
| 출처 인용 | 1점 | `[1]` 같은 참조가 달려 있는가 |
| 문서 외 환각 없음 | 1점 | 문서에 없는 사실을 지어내지 않는가 |
| "모르면 모른다" | 1점 | 답 못 찾으면 없다고 답하는가 |

20개 × 5점 = 100점 만점. 초기 파이프라인이 70점대에서 시작해 튜닝하며 85~90점대로 올리는 흐름이 일반적이다. 

---

## 8.6 실패 패턴 세 가지 — 실전에서 자주 터지는 지점

RAG는 만들기는 쉽지만 **잘** 만들기는 어렵다. 현장에서 반복적으로 터지는 실패 패턴 세 가지를 짚어두자. 각각이 나중에 "아, 이거였네" 하고 되돌아볼 지점이다.

### 패턴 1. 청크 크기 과대·과소

가장 흔한 함정이다. 청크가 너무 크면 한 벡터에 여러 주제가 뭉쳐 "의미의 평균화"가 일어난다. 검색 정확도가 떨어진다. 반대로 너무 작으면 맥락이 잘려서, 검색된 청크를 보고도 LLM이 답을 못 만든다. 500~800 토큰이 기본값이라고 했지만, 도메인마다 최적이 다르다.

증상은 이렇다.

- Hit@5는 높은데 답변 품질이 낮다 → 청크가 너무 **커서** 관련 없는 내용이 섞임
- 답변이 툭툭 끊기거나 맥락을 놓친다 → 청크가 너무 **작아서** 필요한 앞뒤 문장이 잘림
- 표·코드·JSON 응답이 깨진다 → 구조 단위로 쪼개지 않아 경계선이 잘못 잡힘

당근페이 FDS 사례를 다시 소환하자. "retrieve 시, 결과의 content가 완전한 Json 형태가 아니라 일부가 잘려서 나오는 문제가 발생했어요"(supplementary_gap3 1.2). 기본 청킹 전략은 텍스트가 균일하다고 가정하지만, JSON·표·코드는 그 가정을 위반한다. **구조 있는 데이터는 `ChunkingStrategy=NONE` 또는 커스텀 분할**로 바꾸자.

### 패턴 2. 질문-문서 언어 불일치

한국어 질문이 들어오는데 문서는 영어 기술 문서다. 또는 반대. 임베딩 모델이 `text-embedding-3-small`처럼 영어 최적이면 한국어 질문이 영어 문서를 잘 못 찾는다. 반대로 한국어 전용 임베딩에 영어 API 레퍼런스를 섞어넣어도 문제가 된다.

해법은 둘 중 하나다.

1. **다국어 임베딩 모델** 쓰기: `bge-m3`, `multilingual-e5-large`가 이 용도. 한국어·영어 혼용 코퍼스에 가장 안전.
2. **질문을 문서 언어로 번역** 후 검색: 질문이 한국어, 문서가 영어뿐이면 LLM으로 질문을 영어로 한 번 번역하고 검색. 답변은 다시 한국어로.

체크 방법은 간단하다. 골든셋에 한국어 질문과 영어 질문을 섞어 넣고 Hit@k를 재본다. 한쪽만 현저히 낮다면 언어 불일치 가능성을 의심.

### 패턴 3. 출처 미표시로 인한 신뢰 붕괴

이게 가장 치명적이다. 기술적으로 RAG가 잘 도는 상황에서도, 사용자에게 **"이 답이 어디서 왔는지"**를 못 보여주면 신뢰가 무너진다. 특히 규제·금융·의료 도메인에서.

증상은 사용자 쪽에서 먼저 터진다. "이거 진짜야?"라는 질문에 답을 못 한다. 개발자는 "LLM이 그렇게 답했어요"라고 말할 수 없다. 당장 감사 로그가 필요한 순간 뭐가 어떤 문서에서 나왔는지 추적할 방법이 없다.

해결은 두 층에서 한다.

1. **프롬프트에서** 모델이 `[1][2]` 인용을 달도록 명시 (이 장 8.2.6)
2. **API 응답에서** 검색된 문서 목록을 별도 필드로 반환 (Python의 `sources`, Java의 `Answer.sources`)

두 층을 모두 유지하자. 프롬프트 인용이 틀리거나 빠질 수 있기 때문에 API 응답의 출처 필드가 **정답**이고, 프롬프트 인용은 **사용자에게 보여주는 용도**다.

그리고 하나 더. smallcherry가 남긴 관찰. "Retrieval한 Context에 상충된 정보가 존재하면 할루시네이션을 유발할 수 밖에 없음"(supplementary_gap3 1.6). Top 5 청크 중 두 청크가 서로 다른 내용을 말하면 LLM은 혼란에 빠진다. 오래된 문서에는 `deprecated: true` 같은 메타데이터를 붙이고, 검색 단계에서 필터링하자. 문서 버전 관리가 RAG의 숨은 뿌리다.

---

## 8.7 "첫 직감이 fine-tune이면 red flag" — 체크리스트 정식 제시

이 장의 시작에서 체크리스트를 짧게 소개했다. 실습을 거친 지금 다시 보면 감각이 바뀌었을 것이다. 각 항목 뒤에 **왜 그런가**를 한 줄씩 덧붙여 정식 버전을 놓아두자.

> **파인튜닝 vs RAG 판단 체크리스트 (v1.0)**
>
> **Step 1. RAG 필수 조건 체크**
> - [ ] 데이터가 **자주 갱신**된다 → RAG 지지. (파인튜닝은 재학습 비용이 크다.)
> - [ ] **출처 인용**이 필요하다 (규제·감사·금융·의료) → RAG 지지. (가중치에 녹은 지식은 추적 불가.)
> - [ ] 문서가 **조직 내부에서 흩어져** 있다 (wiki·Confluence·Notion·GitHub) → RAG 지지.
> - [ ] **최신성**이 중요하다 (API 문서, 뉴스, 정책) → RAG 지지.
>
> **Step 2. 파인튜닝이 빛나는 조건 체크**
> - [ ] 원하는 출력이 **특정 스키마·톤·포맷**이다 → 파인튜닝 고려.
> - [ ] **반복적 태스크를 inline 지시 없이** 재현해야 한다 → 파인튜닝 고려.
> - [ ] 16GB+ VRAM, 파인튜닝 데이터 **수백~수천 건** 확보 → 파인튜닝 가능.
>
> **Step 3. 결정**
> - Step 1에 **한 개라도** 체크 → **RAG 먼저**.
> - Step 2가 강하고 Step 1이 약하면 → **파인튜닝 단독 또는 RAG + 파인튜닝 하이브리드**.
> - 둘 다 불분명 → **프롬프트 엔지니어링 + RAG**부터. 일주일 써보고 부족한 부분만 파인튜닝.
>
> **Step 4. 빨간 깃발**
> - 체크리스트 없이 "당연히 파인튜닝"으로 점프하는가? → 빨간 깃발.
> - 데이터 갱신 주기를 **생각해본 적 없는가**? → 빨간 깃발.
> - 출처 인용 요구를 **확인해본 적 없는가**? → 빨간 깃발.

현장 실무자들의 한 줄 요약: **"첫 직감이 fine-tune이면 그게 빨간 깃발. 먼저 RAG로 얼마까지 가는지 보고 결정하자."** 이 문장을 Git 커밋 메시지처럼 머릿속 한쪽에 박아두면 좋다.

---

## 8.8 공통 태스크 네 해법 겹쳐보기 — 파인튜닝-RAG-프롬프트 3각

자, 이 장의 마지막 장치다. 4장부터 따라온 **"사내 개발 문서 요약/Q&A"**라는 공통 태스크가 이제 네 가지 답을 받았다. 같은 문제의 네 가지 풀이를 한 장면에 겹쳐보자. 이 겹침이 9장 결정 플로차트의 시각적 근거다.

| 해법 | 장 | 구성 | 개발 시간 | GPU | 장점 | 단점 | 적합한 순간 |
|---|---|---|---|---|---|---|---|
| **① From scratch 미니 GPT** | 4장 | nanochat 스타일 100~300줄 | 1~2주 | A100 · T4 | 원리 체득, 완전 제어 | 품질·속도 최하, 유지보수 곤란 | 교육·연구. 프로덕션 불가. |
| **② QLoRA 파인튜닝** | 6장 | Llama 3 8B + peft + trl | 3~5일 | 16~24GB | 톤·스타일 학습, 로컬 가능 | 데이터 갱신 시 재학습, 출처 추적 곤란 | 톤이 고정된 반복 태스크. |
| **③ API + 프롬프트** | 7장 | GPT-4o/Claude + 프롬프트 | 반나절 | 불필요 | 최고 품질, 즉시 배포 | 도메인 지식 반영 제한적, 외부 의존 | 범용 요약, 일반 Q&A. |
| **④ RAG** | 8장 | 임베딩 + 벡터 DB + ③ | 2~5일 | 불필요 (외부 API) 또는 GPU (로컬 임베딩) | 최신 사내 지식 반영, 출처 인용, 파인튜닝 없음 | 문서 품질에 결과가 좌우됨, 검색 튜닝 필요 | **사내 문서 Q&A의 기본값**. |

같은 질문—**"우리 결제 API의 최대 재시도 횟수는?"**—을 네 해법에 던져보면 이런 그림이 나온다.

- **①**: 한국어 문맥은 이해하지만, 모델이 학습한 작은 코퍼스에 우리 회사 API 문서가 없었다. 답이 그럴듯한 **허구**일 가능성이 매우 높다.
- **②**: 파인튜닝 데이터에 정확히 이 질문-답변 페어가 있었다면 잘 답한다. 없었다면 환각. 재시도 횟수가 어제 바뀌었다면 어제의 지식이 없다.
- **③**: GPT-4가 "일반적으로 결제 API는 3회 재시도를 권장합니다"라고 답할 가능성이 높다. **우리 회사**의 답이 아니라 **일반론**이다.
- **④**: `api-guide.md`에서 "최대 3회, 지수 백오프" 문장을 검색해 프롬프트에 주입. GPT-4가 그 문장을 기반으로 답한다. 출처 `[api-guide.md]`까지 같이 붙는다.

네 해법의 위치가 이렇게 다르다. **③이 범용 기본값, ④가 사내 문서 기본값, ②는 톤/스타일 튜닝 용도, ①은 교육용**. 이 감각이 있으면 다음에 팀장이 "LLM으로 뭐 하나 만들어줘"라고 할 때, 즉시 "어떤 문제인지" 물어볼 수 있다. 데이터가 어디서 오느냐, 얼마나 자주 바뀌느냐, 출처가 필요하냐. 답을 들으면 해법이 정해진다.

하나 더 덧붙이자면, 이 네 해법은 **배타적이지 않다**. 실제 현업 시스템은 종종 조합이다. **"RAG + 파인튜닝"**이 대표적이다. RAG가 사내 지식을 책임지고, 그 위에 얇은 QLoRA 파인튜닝으로 회사 고유의 응답 톤을 얹는다. **"RAG + 프롬프트 엔지니어링 + Guardrails"**도 흔하다. 카카오페이 춘시리 사례가 이쪽이다—RAG로 위키 Q&A, 프롬프트로 역할 지정, AWS Bedrock Guardrails로 민감정보 필터(supplementary_gap3 1.4).

기억해두자. **해법은 독립된 선택지가 아니라 쌓을 수 있는 레이어**다. 맨 아래에 ③(프롬프트)을 깔고, 그 위에 ④(RAG)를 얹고, 필요하면 ②(파인튜닝)를 한 층 더. 이 순서가 "머리로 고르지 말고 손으로 고르라"(Reference 5.8)는 현장 규범의 구체화다. 가장 아래 층에서 일주일 써보고, 부족한 부분만 한 층씩 올린다.

---

## 마무리 — 이 장에서 같이 얻은 것

한 번 되짚어보자.

- **RAG는 파인튜닝보다 먼저**다. 데이터가 자주 바뀌고, 출처 인용이 필요하고, 문서가 조직 내부에 흩어져 있는 대부분의 "사내 LLM 첫 과제"는 RAG가 90%를 푼다.
- 파이프라인은 **인덱싱(문서 → 청킹 → 임베딩 → 벡터 저장소)**과 **질의(질문 → 검색 → 컨텍스트 주입 → LLM → 답변 + 출처)**의 두 단계.
- 임베딩은 **BERT 계열이 여전히 주력**이다. 한국어는 `bge-m3`가 현재의 실무 디폴트. API가 허용되면 `text-embedding-3-small`도 실용적.
- 벡터 DB는 **pgvector(운영), Chroma(프로토타입), Qdrant(대규모)** 중에서. 이미 PostgreSQL을 쓰고 있다면 pgvector가 거의 언제나 정답.
- **하이브리드 검색(벡터 + BM25)**과 **리랭커**는 품질을 한 단계 올리는 부품. 없어도 기본은 돌지만, 있으면 +5~10%p의 Hit@k.
- **출처 인용**을 프롬프트와 API 응답 양쪽에서 유지하자. 없으면 신뢰가 붕괴한다.
- **골든셋 20개로 Hit@k와 수작업 채점**. 감으로 튜닝하지 말고 숫자로 튜닝.
- 실패 패턴 세 가지—**청크 크기 과대/과소, 질문-문서 언어 불일치, 출처 미표시**—는 처음 만들 때 반드시 한 번씩 밟게 된다. 미리 표지판을 꽂아두자.
- 4·6·7·8장의 네 해법은 **같은 문제의 서로 다른 층**이다. 독립된 선택지가 아니라 쌓을 수 있는 레이어.

그리고 남긴 질문 하나. **같은 공통 태스크에 네 가지 해법이 있다. 실제 프로젝트 앞에서 어떤 순서로 꺼낼 것인가? 비용·지연·품질의 3축을 어떻게 저울질할 것인가? 관측성과 평가 하네스는 어디에 끼워넣을 것인가?** 이 질문들을 들고 다음 장으로 넘어가자. 9장에서는 이 책에서 만든 부품들을 **결정 플로차트 하나**로 묶는다. 네 해법을 손에 쥐고 있으니, 플로차트의 각 분기가 이론이 아니라 경험으로 읽힐 것이다.
