# Karpathy "LLM Wiki" 패턴으로 만드는 사내 지식 베이스 — 레퍼런스

- 합성 시점: 2026-10-11 (세 리서처의 검색 시점도 모두 2026-10-11)
- 장르: tech-book / 대상 독자: Claude Code 등 에이전틱 코딩 도구로 사내 지식 베이스(브랜드 정보·마케팅 전략·SaaS 도구 사용법·활용 시나리오·최근 전략 결정)를 만들고, 그 위에 Claude 기반 사내 에이전트(Claude Agent SDK 또는 직접 API)를 올리려는 소프트웨어 개발자
- 원천: `research/web.md`(웹 45건), `research/papers.md`(논문 38편 + 1차 비학술 2건), `research/community.md`(HN·gist 댓글·GitHub Issues·구현 보고 11편·한국 소스 6건). 세 파일은 fact-checker의 1차 대조 근거이므로 그대로 보존한다.
- 출처 표기: `[W{n}]` = web.md 자료 번호, `[P{s}-{n}]` = papers.md 논문 번호(`[P-S1]`·`[P-S2]`는 1차 비학술 소스), `[C]` = community.md(출처명 병기). 출처 유형은 각 항목에 (웹)/(논문)/(커뮤니티)/(공식 문서)로 적는다.
- 수치·연도·인물 귀속은 원문 표현을 그대로 옮겼다. "(사실 확인 필요)"·"(계산값)"·"확인 필요"·"사용 금지" 경고는 원본 파일의 경고를 그대로 이어받은 것이며, 17절 "사실 확인 원장"에 한 번 더 모았다.
- 커뮤니티 출처의 모든 수치는 **자기 보고이며 통제 실험이 아니다**(community.md 머리말). 인용 시 원문 링크를 다시 열어 확인할 것.
- 신선도 주의: Claude 모델명·가격·캐시 배수·SDK 버전은 2026-10-11 공식 문서 열람 기준이며 빠르게 바뀐다. 본문 집필 시점에 재확인할 것.

---

## 1. 개념과 정의

### 1.1 패턴의 원전과 날짜
- Andrej Karpathy의 "LLM Wiki" gist(https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). gist 페이지 메타 기준 생성 2026-04-04(Revisions: 1), 본문 1,959단어, 별/포크 5,000+(2026-10-11 기준) `[W1]`(웹, 1차).
- 같은 아이디어를 알린 X 포스트 "LLM Knowledge Bases"는 2026-04-02(https://x.com/karpathy/status/2039805659525644595; fxtwitter API 기준 조회 21,958,561 / 좋아요 61,003 / 답글 2,939) `[C]`(커뮤니티, 메타데이터만 확보·본문 미열람).
- **날짜 상충 메모**: Platformer·HackerNoon 등 2차 자료는 "4월 2일 게시"로 적음(트윗 일자), gist 메타는 04-04. papers.md는 "발행일 gist 본문에 미명시"로 기록. 본문에서는 "2026년 4월 초"로 쓰는 것이 안전 `[W1]`. 트윗과 gist를 구분해 적을 때는 X 포스트 04-02 / gist 04-04.
- 반응 규모(커뮤니티, 검증 필요): 국내 Threads 계정(@choi.openai)은 "하루 만에 270만 회"를 언급. HN 원 스레드 "LLM Wiki – example of an 'idea file'"(2026-04-04, 296p / 95댓글). 이후 6개월 동안 HN에 "LLM wiki"를 제목에 단 Show HN이 40건 이상(Algolia 검색 286 hits). GeekNews GN#352(2026-04) 편집자 코멘트: "이 LLM-Wiki는 LLM을 단순 질의 응답기가 아닌 자동화된 위키 관리자로 다루는 새로운 패러다임을 보여줍니다." VentureBeat 헤드라인("bypasses RAG")이 "RAG 대 위키" 양자택일 프레임을 키웠다는 지적이 여러 글에서 반복 `[C]`.
- 성격: "idea file" — 에이전트에 붙여 넣어 각자 구체화하라는 의도적으로 추상적인 문서. 원문: "This is an idea file, it is designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.). Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you." / "This document is intentionally abstract. It describes the idea, not a specific implementation. [...] Everything mentioned above is optional and modular — pick what's useful, ignore what isn't." `[W1]`

### 1.2 핵심 아이디어 (원문 인용)
- RAG 비판: "Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation." `[W1]`
- 대안: "Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources." / "The knowledge is compiled once and then *kept current*, not re-derived on every query." / "**the wiki is a persistent, compounding artifact.** The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read." `[W1]`
- 역할 분담: "You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions." / "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else." `[W1]`
- 작업 환경 비유: "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase." `[W1]`
- 왜 사람 위키는 죽고 LLM 위키는 사는가: "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. [...] Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. The wiki stays maintained because the cost of maintenance is near zero." `[W1]`
- 팀 적용 원문: "**Business/team**: an internal wiki maintained by LLMs, fed by Slack threads, meeting transcripts, project documents, customer calls. Possibly with humans in the loop reviewing updates. The wiki stays current because the LLM does the maintenance that no one on the team wants to do." `[W1]`
- 역사적 배경: "The idea is related in spirit to Vannevar Bush's Memex (1945) — a personal, curated knowledge store with associative trails between documents. [...] The part he couldn't solve was who does the maintenance. The LLM handles that." `[W1]`

### 1.3 아키텍처: 3계층 · 3연산 · 2특수 파일
| 요소 | 원문 정의 `[W1]` | 비고 |
|---|---|---|
| Raw sources | "your curated collection of source documents. Articles, papers, images, data files. These are immutable — the LLM reads from them but never modifies them. This is your source of truth." | 불변. 커뮤니티에서 가장 자주 깨지는 원칙(패턴 8, H1) |
| Wiki | "a directory of LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely." | |
| Schema | "a document (e.g. CLAUDE.md for Claude Code or AGENTS.md for Codex) that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki. This is the key configuration file — it's what makes the LLM a disciplined wiki maintainer rather than a generic chatbot. You and the LLM co-evolve this over time as you figure out what works for your domain." | 5절(스키마 작성)의 출발점 |
| Ingest | "You drop a new source into the raw collection and tell the LLM to process it. An example flow: the LLM reads the source, discusses key takeaways with you, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. A single source might touch 10-15 wiki pages." / "Personally I prefer to ingest sources one at a time and stay involved [...] But you could also batch-ingest many sources at once with less supervision." | |
| Query | "You ask questions against the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. [...] The important insight: **good answers can be filed back into the wiki as new pages.**" | |
| Lint | "Periodically, ask the LLM to health-check the wiki. Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search." | |
| index.md | "content-oriented. It's a catalog of everything in the wiki — each page listed with a link, a one-line summary, and optionally metadata like date or source count. [...] When answering a query, the LLM reads the index first to find relevant pages, then drills into them. This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure." | 규모 한계 수치의 유일한 1차 출처 |
| log.md | "chronological. It's an append-only record of what happened and when — ingests, queries, lint passes. A useful tip: if each entry starts with a consistent prefix (e.g. `## [2026-04-02] ingest \| Article Title`), the log becomes parseable with simple unix tools — `grep \"^## \\[\" log.md \| tail -5` gives you the last 5 entries." | |

- 용어 메모(논문 리서처 관찰): gist는 "backlink"라는 단어를 쓰지 않고 "inbound link / cross-reference"로 표현한다. 고아 페이지 = inbound link 없는 페이지 `[P-S1]`.
- **gist의 유일한 규모 수치는 "~100 sources, ~hundreds of pages"와 "10–15 pages per ingest"다. 그 외 규모 수치(예: "100 articles / 400,000 words" 같은 2차 블로그의 Karpathy 위키 규모 주장)는 근거 미확인 — 책에 적으면 날조가 되므로 사용 금지** `[P-S1]` `[W 교차검증 메모]`.
- 기타 원문 팁: "A search engine over the wiki pages is the most obvious one — at small scale the index file is enough, but as the wiki grows you want proper search. [qmd](https://github.com/tobi/qmd) is a good option: it's a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device. It has both a CLI (so the LLM can shell out to it) and an MCP server (so the LLM can use it as a native tool)." / "The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free." / "Note that LLMs can't natively read markdown with inline images in one pass — the workaround is to have the LLM read the text first, then view some or all of the referenced images separately to gain additional context." / Dataview: "If your LLM adds YAML frontmatter to wiki pages (tags, dates, source counts), Dataview can generate dynamic tables and lists." `[W1]`

### 1.4 학술 용어로 자리매김하기
- 에이전트 메모리 서베이(Zhang 외 2024, arXiv 2404.13501, ACM TOIS S2 표기, 피인용 845)는 메모리 연산을 writing·management·reading으로, 형식을 텍스트(원문·요약·구조화)와 파라메트릭으로 나눈다. LLM Wiki = "텍스트 형식·구조화 메모리 + 명시적 관리 연산(lint)". ingest(write)/lint(manage)/query(read)에 1:1 매핑 가능 `[P1-1]`(논문).
- 지식 편집 분류(Zhang 외 2024, arXiv 2401.01286)는 지식 편집을 "resorting to external knowledge, merging knowledge into the model, and editing intrinsic knowledge" 3군으로 나눈다. LLM Wiki는 "resorting to external knowledge" 계열의 극단적으로 단순한 구현 `[P3-6]`(논문).
- Agentic RAG 서베이(Singh 외 2025, arXiv 2501.09136, v4 2026-04-01, 피인용 444)의 분류 축(에이전트 수·제어 구조·자율성·지식 표현)에서 LLM Wiki의 query는 "단일 에이전트·순차·높은 자율성·텍스트 지식 표현"에 놓인다 `[P2-2]`(논문).
- 지식 충돌 서베이(Xu 외 2024, arXiv 2403.08319, EMNLP 2024 S2 표기)의 3범주 — context-memory / inter-context / intra-memory. lint의 "모순 탐지"는 inter-context 충돌을 위키 안에서 사전에 해소하는 작업 `[P3-1]`(논문).
- 메모리 아키텍처 계보(개발자 비유와 함께):
  - Generative Agents(Park 외 2023, arXiv 2304.03442, UIST 2023 S2 표기, 피인용 5,937): memory stream(원본 기록) → reflection(합성 통찰) 분리가 raw/wiki 분리의 선조. 검색 점수 = recency + importance + relevance 가중합(가중치 모두 1, min-max 정규화), recency 지수 감쇠율 0.995, importance는 LLM이 1~10점, reflection은 최근 사건 importance 합이 임계치(150)를 넘으면 발동. 원문: "we generate reflections when the sum of the importance scores for the latest events perceived by the agents exceeds a threshold (150 in our implementation)." 비유: "일기(raw) → 주간 회고(reflection)"; 감쇠율은 "하루 지나면 0.995^24 ≈ 0.89" `[P1-2]`.
  - MemGPT(Packer 외 2023, arXiv 2310.08560, 프리프린트, 피인용 1,572): OS 가상 메모리 비유. index.md = working context, 페이지 = archival storage, log.md = recall storage. DMR 정확도 GPT-4 단독 32.1% → MemGPT 92.5%; GPT-4 Turbo 35.3% → 93.4%. "MemGPT's performance is unaffected by increased context length." `[P1-3]`
  - A-MEM(Xu 외 2025, arXiv 2502.12110, NeurIPS 2025 확인, 피인용 1,172): Zettelkasten 원리. 새 노트가 들어오면 링크 생성 + 이웃 노트의 문맥·태그를 갱신하는 memory evolution — gist의 "소스 1건이 10~15페이지를 건드린다"의 학술 대응물. 원문: "as new memories are integrated, they can trigger updates to the contextual representations and attributes of existing historical memories". **주의: "multi-hop에서 2배" 주장은 표와 어긋나므로 책에서 쓰지 말 것. 토큰 절감은 본문 "약 1,200 토큰/연산, 85~93% 절감"이지만 표의 GPT-4o-mini 행은 2,520 토큰(GPT-4o 1,216; LoCoMo·MemGPT ≈ 16,900) → "최대 약 93% 절감" 정도로 보수적으로** `[P1-4]`.

---

## 2. 왜 위키인가 — 근거와 반론

### 2.1 "전부 컨텍스트에 넣으면 되지 않나"에 대한 답
- Anthropic 공식 정의: 컨텍스트 엔지니어링은 "the set of strategies for curating and maintaining the optimal set of tokens (information)" / 목표는 "finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." / "LLMs have an 'attention budget'" / "the concept of context rot" `[W14]`(공식, 2025-09-29).
- Claude API 문서: "A larger context window allows the model to handle more complex and lengthy prompts, but more context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as *context rot*. This makes curating what's in context just as important as how much space is available." `[W17]`(공식, 2026-10-11 열람).
- Context Rot 기술 보고서(Chroma, Hong·Troynikov·Huber, 2025-07-14, 비동료심사, arXiv ID 없음): 18개 모델, 8개 입력 길이 × 11개 needle 위치. "their performance grows increasingly unreliable as input length grows." / "Surprisingly, we find that structural coherence consistently hurts model performance." / "Even a single distractor reduces performance relative to the baseline (needle only)". LongMemEval 306문항에서 모든 모델이 focused prompt(~300 토큰)가 full prompt(~113k 토큰)보다 높았다 `[P-S2]`. 독자 전달: "컨텍스트 윈도우는 용량이지 성능 보증이 아니다".
- Lost in the Middle(Liu 외 2023, arXiv 2307.03172, TACL 2023 확인, 피인용 5,438): "performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models." / "Using more than 20 retrieved documents only marginally improves reader performance." 20문서 설정: 정답이 맨 앞 75.8%, 중간(index 9) 53.8%, 맨 끝 63.2% (계산값, 부록 표); closed-book 56.1%, oracle 88.3%. **2023년 모델 기준이라는 신선도 한계 명시** `[P2-8]`.
- Same Task, More Tokens(Levy 외 2024, arXiv 2402.14848, ACL 2024 확인): 500토큰을 넘으면서 유의한 하락, 전체 평균 정확도 0.92 → 0.68(3,000토큰). perplexity와 추론 정확도 Pearson ρ = −0.95 (p=0.01). "a notable degradation in LLMs' reasoning performance at much shorter input lengths than their technical maximum." → 위키 페이지를 짧고 밀도 있게 `[P2-9]`.
- RULER(Hsieh 외 2024, arXiv 2404.06654, COLM 2024 확인): "While these models all claim context sizes of 32K tokens or greater, only half of them can maintain satisfactory performance at the length of 32K." → "표기 컨텍스트 ≠ 유효 컨텍스트" `[P2-10]`.
- NoLiMa(Modarressi 외 2025, arXiv 2502.05167, ICML 2025 확인): "At 32K, for instance, 11 models drop below 50% of their strong short-length baselines." GPT-4o 99.3% → 69.7%(32K); 유효 길이 대부분 ≤2K, GPT-4o 8K; Llama 3.1 70B 표방 128K·유효 2K·32K에서 42.7%. → 위키가 질문 언어와 페이지 언어를 맞춰 주는(용어 정규화·동의어 페이지) 가치 `[P2-11]`.
- LY Corporation(Databricks 연구 인용): "GPT-4나 Llama-3.1 같은 모델에서도 컨텍스트가 특정 구간(32K~64K 토큰)을 넘어가면 RAG 성능이 하락하기 시작했습니다." `[W40]`(웹, 회사 블로그, 발행일 미표시 — 사실 확인 필요).
- 커뮤니티: HN lelanthran — "What use is 10M context if degradation starts at 200k - 300k?" `[C]`.
- **반대편 기준**(둘 다 Anthropic): 지식베이스가 작으면 검색 없이 통째로. "If your knowledge base is smaller than 200,000 tokens (about 500 pages of material)," 전체를 프롬프트에 넣고 캐싱 `[W15]`(공식, **2024-09-19 기준** — Claude 3 계열 실험). 현재 1M 컨텍스트 모델 목록은 6.6절.

### 2.2 "RAG와 뭐가 다른가"
- 고전 RAG 정의의 표준 인용: RAG 서베이(Gao 외 2023, arXiv 2312.10997, 피인용 4,260) — "Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes." Naive → Advanced → Modular 3단계 `[P2-1]`.
- 전역 질문에서 RAG가 실패한다: GraphRAG(Edge 외 2024, arXiv 2404.16130, 프리프린트, 피인용 2,323) — "RAG fails on global questions directed at an entire text corpus, such as 'What are the main themes in the dataset?'" 커뮤니티 요약을 미리 생성. 루트 요약 C0는 "Root-level community summaries (C0) require dramatically fewer tokens per query (9x-43x)." comprehensiveness 승률 72~83%(팟캐스트, p<.001), 72~80%(뉴스). 인덱싱 281분(팟캐스트 ≈ 100만 토큰 코퍼스, 8,564 노드/20,691 엣지). **주의: LLM-as-judge 평가. directness에서는 vector RAG가 우세(논문 명시)**. 위키의 overview/개념 페이지 = 커뮤니티 요약; 인덱싱 비용은 "그래프를 전부 다시 만들지 말고 증분 ingest 하라"의 반대편 근거 `[P1-8]`.
- 요약 노드는 실제로 검색된다: RAPTOR(Sarthi 외 2024, arXiv 2401.18059, ICLR 2024 S2 표기) — "We observe that between 18.5% to 57% of the retrieved nodes come from non-leaf nodes." QuALITY RAPTOR+GPT-4 82.6%(이전 최고 62.3%). "The collapsed tree approach consistently performs better." 비유: "README가 있는 폴더가 검색이 잘 된다" `[P1-7]`.
- 그래프 자체보다 추출·통합·갱신 루프가 효과의 대부분: Mem0(Chhikara 외 2025, arXiv 2504.19413, ECAI 2025 S2 표기) — 그래프 메모리는 기본 대비 약 2% 추가. "Mem0 attains a 91% lower p95 latency and saves more than 90% token cost". **벤더 자체 평가, 중립 재현 미확인** `[P1-5]`.
- 링크 그래프는 싸고 빠른 multi-hop 자산: HippoRAG(Gutiérrez 외 2024, arXiv 2405.14831, NeurIPS 2024 확인) — "Single-step retrieval with HippoRAG achieves comparable or better performance than iterative retrieval like IRCoT while being 10-30 times cheaper and 6-13 times faster" `[P1-10]`.
- 증분 갱신 가능한 그래프: LightRAG(Guo 외 2024, arXiv 2410.05779, EMNLP S2 표기) — "an incremental update algorithm that ensures the timely integration of new data" (초록에 구체 수치 없음 — 정성 주장으로만) `[P1-9]`.
- LLM 위키 vs 청크 RAG의 직접 벤치마크(**2차 요약만 확보**): "Retrieval as Reasoning"(arXiv 2605.25480) GeekNews 소개 `[W5]`(웹, 2026-08경, 게시자 alfadur) — "**컴파일**: 원문서를 양방향 링크가 걸린 위키 페이지로 변환 (검색하는 단위가 청크가 아니라 링크된 페이지)" / "멀티홉 QA 세 종류에서 기준 모델들보다 2.0~8.1 F1 앞섬" / ablation "순회를 뺐을 때: −11.7 / −13.8 / −12.2 (가장 치명적)" / "위키 구조를 뺐을 때: −6.1 / −7.0 / −6.7" / "Error Book을 뺐을 때: −3.8 / −4.0 / −3.4". 단 잘 튜닝된 agentic RAG와는 비교 안 함(alfadur 본인 인정) `[C]`. **papers.md에 이 논문 항목이 없음 — 수치는 논문 원문 대조 (사실 확인 필요)**. 한 사전등록식 비교는 위키가 교차 논문 질문에서 더 낫지만 "약 21배 더 많은 토큰"을 쓴다고 보고 (2차 인용, 검증 필요) `[C]`.
- 커뮤니티 논쟁 "이건 그냥 RAG다" vs "쓰기 루프가 다르다"는 12절 논쟁 A.

### 2.3 "모델을 고치지 말고 위키를 고쳐라"
- Editing LLMs(Yao 외 2023, arXiv 2305.13172, EMNLP 2023 확인): 단일 편집은 잘 되지만(GPT-J/ZsRE ROME reliability 99.18, MEMIT 99.23) portability는 SERAC 세 항목 모두 20% 미만(17.79/1.30/5.53), one-hop은 최고 방법도 약 55%(IKE 55.38, MEMIT 52.74). "current model editing techniques continue to face challenges in managing the ramifications of an edit." `[P3-5]`
- Ripple Effects(Cohen 외 2023, arXiv 2307.12976, TACL 2024 확인): "a simple in-context editing baseline obtains the best scores on our benchmark" — ingest에서 관련 페이지 10~15개를 같이 고치는 것이 ripple 처리 `[P3-7]`.
- 시간 유효 기간: Time-Aware LM(Dhingra 외 2021, arXiv 2106.15110, TACL 2022 vol.10 pp.257–273) — "Many facts come with an expiration date, from the name of the President to the basketball team Lebron James plays for." `[P3-8]`. TemporalWiki(Jang 외 2022, arXiv 2204.14211, EMNLP 2022 확인) — "training an LM on the diff data through continual learning methods achieves similar or better perplexity than on the entire snapshot in our benchmark with 12 times less computational cost" → diff만 처리하는 증분 ingest의 근거, log.md = diff 원장 `[P3-9]`.
- FreshLLMs(Vu 외 2023, arXiv 2310.03214, ACL 2024 Findings S2 표기): "all models (regardless of model size) struggle on questions that involve fast-changing knowledge and false premises." / "instructing the LLM to generate concise and direct answers helps reduce hallucination compared to encouraging more verbose answers." 사내 지식은 대부분 fast-changing → 답변 프롬프트에 "간결하게, 근거 페이지 명시" `[P3-10]`.

### 2.4 위키 접근의 실증 vs 회의 (커뮤니티·실사용)
- 긍정 실사용: Platformer Casey Newton(2026-08-18) — 한 달 남짓 만에 "More than 1,440 wiki pages." Meta 페이지 "more than 12,000 words" · "more than 1,300 links to other wiki pages." 단점 "more or less constant maintenance", Claude의 "hyper-compressed, borderline-unreadable house style" `[W3]`(웹). Taktile(회사, 2026-07-13) — 실행당 라이브 조회 9m40s·$2.50 → 위키 답변 1m19s·$0.98 (86% 빠르고 61% 저렴) `[C]`(자기 보고). 클리앙 카일라스(2026-04-26) — "LLM wiki/RAG 둘 다 500 개가 넘는 메모를 처리하는데 별 부족함이 없었고 대부분 답변도 유사하게 나왔습니다." / "RAG 를 Agent 에 붙이기 위해 구현/설정/튜닝을 하는거 보다 LLM 위키를 사용하는 것이 간단하고 효율적" / "하지만 느림. 500+ 메모를 위키에 등록하는데 20분 넘게 걸림..." `[W6]` `[C]`.
- 회의: HN 원 스레드 Imanari — "kicking the can down the road"; 위키가 컨텍스트에 다 안 들어가면 LLM은 원본 대신 위키를 다시 읽고 "subtle errors as we start to regurgitate 2nd-order information"가 쌓인다. devnullbrain — "I don't see why this wouldn't just lead to model collapse." (반론 gojomo: 2024년식 collapse 공포는 직관을 흐린다; ChrisGreenHeur: 학습이 아니라 개인 위키 얘기라 핀트가 다르다) `[C]`. GeekNews HN 요약: "위키를 유지하려면 LLM이 매번 원본 대신 위키를 다시 읽어야 하고, 그 과정에서 2차 오류가 누적됨" / 회사 프로젝트 적용 결과 "새로운 형태의 기술 부채" `[W4]`.
- "그냥 위키만으론 부족": PyTorchKR requests.selenium(윤기석, 2026-06-24) — "위키 페이지에 내용이 누락되는 경우가 너무 많으며, 그럴 경우 결국 원본 페이지를 봐야해서"; clue.oz4e(구영수, 08-10) — "위키를 '내용 저장소'에서 '지도'로 강등시켰습니다" → 하이브리드 RAG 결합 후 recall@5 93%(자기 보고) `[C]`.
- 업무 지식은 다르다는 반론: @_avichawla(2026-04-08, 조회 218,573) — "But this pattern breaks when you apply it to actual work" — 연구는 개념과 관계가 안정적이지만 업무는 마감·계획·회의가 계속 바뀐다 → 사람·결정·약속·마감이라는 타입 엔티티의 지식 그래프(Rowboat) 제안. 후속 포스트 "Karpathy liked this one!" `[C]`. **사내 KB의 "전략 결정·시나리오" 페이지 설계에 직결되는 반론.**
- 생각 외주화 불안(사람 쪽 비용): HN qaadika — "Learn how to learn and answer your own damn questions." nidnogg — "a persistent brain gap"; "the wiki workflow is just too addictive to stop." loveparade — "Most of the value of writing docs or a wiki is not in the final artifacts." `[C]`. 사내 KB에서의 반전: 사내 지식은 "개인의 학습"이 아니라 "조직의 기억"이라 무게가 다르다 — 단, 결정의 이유를 남기는 사람의 역할은 남는다(당근 발표, AI월드 2026 보도: "판단의 결과뿐 아니라 이유와 근거를 남겨야 다음 사람과 에이전트가 이를 바탕으로 일할 수 있다", https://www.fnnews.com/news/202609091826242004) `[C]`.

---

## 3. 위키를 어떻게 짓는가 (디렉터리·페이지 규약·ingest)

### 3.1 디렉터리 구조 — 파생 구현들의 공통형
- Astro-Han/karpathy-llm-wiki README 그대로 `[W9]`(웹, ★2.5k, 커밋 28, MIT, "2026년 4월부터 매일 유지"):
  ```
  your-project/
  ├── raw/          (immutable source material, organized by topic)
  ├── wiki/         (compiled knowledge pages maintained by the LLM)
  │   ├── topic/
  │   ├── index.md  (global table of contents)
  │   └── log.md    (append-only operation log)
  ```
- HagaiHen/podcast-wiki: `wiki/{concepts,hubs,episodes,people,shows,takeaways}/ + index.md` `[W11]`.
- Taktile(회사): 질문 범주별 서브위키 + 각 레벨 index.md(top-down 탐색), 마크다운+프런트매터를 전용 브랜치에 `[C]`.
- 토스 하네스 글의 회사 지식 3계층(디렉터리 설계에 차용 가능): "Global Layer: 전사 공통 규정 (보안 정책, 기본 코딩 스타일)" / "Domain Layer: 팀/비즈니스별 지식 (결제, 정산, 회원 등 특정 도메인 로직)" / "Local Layer: 특정 레포지토리의 구현 디테일 및 프로젝트 특화 규칙" `[W38]`(웹, 토스 김용성, 2026-02-26; 저자 스스로 "지금까지의 이야기는 대부분 가설이고 방향성입니다"라고 명시).
- 업무용 타입 엔티티(사람·결정·약속·마감) 제안은 @_avichawla `[C]`(2.4절).

### 3.2 페이지 작성 규약
- **TL;DR 상단 + 토큰 예산 계층** `[C]`(커뮤니티, 자기 보고):
  - gist 댓글 YokoPunk(첫날): 각 위키 글 맨 위에 TLDR → 사람과 LLM 모두 본문을 읽을지 판단.
  - Jim Liu(6개월 보고, 2026-05-06): 모든 페이지가 50자 이하 TL;DR로 시작. 35개 TL;DR을 한 번에 훑을 수 있어 인덱스보다 이게 더 중요.
  - gist 댓글 bluewater8008/hejiajiudeeyu(2026-04-05, 프로덕션 팀): 인덱스에 토큰 예산 — L0 ~200, L1 ~1–2K, L2 ~2–5K, L3 5–20K 토큰. 엔티티 유형별 템플릿 하나씩(7종). "The LLM is the writer. You're the editor-in-chief."
  - gist 댓글 tomjwxf: 점진 공개 — L0 ~50, L1 ~200, L2 ~1K 토큰, L3 전체.
  - gist 댓글 AgriciDaniel: 핫 캐시를 세션 컨텍스트 "under 500 tokens"로 유지.
  - Ghelbur "For future Claude" 서문: 더 읽어야 하는지 알려주는 짧은 블록. 프런트매터는 "in three lines"로 노트 종류를 알려야 함.
- **한 줄 = 자족적 원자 사실(proposition)**: Dense X Retrieval(Chen 외 2023, arXiv 2312.06648, EMNLP S2 표기·2024 추정) — "Propositions are defined as atomic expressions within text, each encapsulating a distinct factoid and presented in a concise, self-contained natural language format." proposition 평균 11.2단어 vs 단락 58.5단어. Recall@20 평균 +10.1(비지도 dense retriever), +2.7(지도). → 위키 bullet 한 줄을 주어 명시·자족적으로 쓰면 검색이 좋아진다 `[P1-11]`(논문).
- **청킹을 더 똑똑하게 하는 것보다 LLM이 쓴 페이지(이미 의미 단위)**: Qu 외 2024(arXiv 2410.13070) — "the computational costs associated with semantic chunking are not justified by consistent performance gains." 반대로 위키가 없다면 고정 청킹으로 시작해도 손해가 아님 `[P1-12]`.
- **프런트매터 필드** `[C]`:
  - Jim Liu schema.md: 프런트매터 필드, 슬러그 규칙, 모순 해소 프로토콜. 페이지 수명 필드 `last_verified`, `confidence`, `superseded_by`, `contradicts`.
  - Aaron Fulkerson(2026-04-12): YAML 프런트매터에 human-written / LLM-generated / LLM-generated-human-reviewed 태그. "Without this metadata, the model couldn't assess its own confidence in a source."
  - gist 댓글 l-mb: 폴더 대신 태그·속성(status: raw/tagged/processed, tagged_on) — 모델이 좋아지면 재태깅 가능.
  - 반대 의견: asakin — YAML 대신 굵은 글씨 필드 메타데이터, index.md 없이 요약·태그 스캔. mfittko/repo-wiki PR #48 — GitHub Wiki는 프런트매터를 그대로 노출하고 Jekyll은 먹어 버려서 처리가 갈린다.
  - 우아한형제들 물어보새: "문서 제목, 팀명, 생성일, 라벨 등 메타데이터도 함께 저장하여 검색의 정밀도를 한층 끌어올렸습니다." `[W39]`(웹, 2025-10-15).
  - 토스 Topic의 신뢰 상태 필드(`trusted`, `partly_trusted`, `disputed`, `stale_risk`, `insufficient_evidence`)와 관계 유형 `contradicted_by` `[W37]`(웹, 2026-07-30) — 위키 frontmatter에 신뢰 상태·최신성 필드를 두는 모델.
  - Zep의 as-of 모델(Rasmussen 외 2025, arXiv 2501.13956, 프리프린트): 각 사실(edge)에 4개 타임스탬프(t_created, t_expired = 시스템 시간; t_valid, t_invalid = 사실이 참이었던 기간). 모순 시 "it invalidates the affected edges by setting their t_invalid to the t_valid of the invalidating edge." (삭제가 아님) → 위키 사실 줄에 `valid_from / valid_to` 메타를 두고 덮어쓰지 않고 만료 처리. **벤더 자체 평가** `[P1-6]`.
- **메타데이터 3축**: Generative Agents의 recency/importance/relevance를 위키의 "최근 수정/중요도/관련성" 메타로 `[P1-2]`.
- **마크다운 인라인 이미지**: LLM은 한 번에 못 읽으므로 텍스트 먼저, 이미지 별도 열람 `[W1]`. WikiAutoGen(Yang 외 2025, arXiv 2503.19065, ICCV 2025 확인, 피인용 5)은 멀티모달 위키 생성의 "최근 방향" 정도로만 `[P5-3]`.

### 3.3 ingest 설계
- 원문 흐름(1.3절) + "한 번에 하나" 원칙. Anthropic 장기 실행 에이전트 하네스 글(Justin Young, 2025-11-26): "This incremental approach turned out to be critical to addressing the agent's tendency to do too much at once." / "leaving the environment in a clean state at the end of a session" / 세션 간 상태 파일 "the claude-progress.txt file alongside the git history" `[W21]`(공식) → 야간 ingest/lint 잡을 log.md로 잇는 설계.
- **소스는 유형별로 분류하고 입력 단위는 작게** `[C]`: bluewater8008 — 추출 전에 소스 유형 분류, 안 하면 "you get shallow, uniform summaries of everything." vbarsoum — 책 한 권 = 파일 하나는 slop; 챕터 단위 파일로 바꾸니 "changed the output categorically" (210 개념 페이지, 교차참조 4,597개, 페이지당 평균 19.2 링크).
- **페이지 폭발 예산** `[C]`: xoai — 논문 1편이 10–15 페이지를 건드린다, "Ontology is the hardest part"(개념 중복 제거). AgriciDaniel — 소스 1개 → 8–15 페이지. MetamusicX — 소스 1개 → 38 페이지. Jim Liu — 최근 30회 인제스트에서 터치 파일 중앙값 9개(범위 4–23).
- **"확장 우선, 생성 금지"**: HagaiHen(2026-10-08, 팟캐스트 위키, 60회 → 69 개념 페이지, 몇 시간마다 무인) — "Extend, don't create. The default failure is near-duplicate pages." / "Rewrite the summary, don't append." / 주기적 "dream" 패스가 같은 아이디어로 표류한 페이지를 병합 `[W2]` `[C]`.
- **append가 아니라 rewrite**: Ghelbur — append만 하면 사람 페이지가 옛 직장을 계속 설명 → "Append-only knowledge bases get stale invisibly because nothing about reading them tells you that a fact is from 2024." 주장별 최신성 마커 + rewrite `[C]`.
- **기록 트리거와 do-not-record 목록**: @vellumkasane(Dev.to, 2026-09-22) — 기록 트리거 = 사람이 고른 선택지, 뒤집힌 결정, 사람이 말한 암묵 규칙, 측정값. 명시적 do-not-record 목록. 에이전트가 자꾸 "should I record this?" 묻기 — "Noise, not missing entries, was the failure mode." `[C]`
- **결정 vs 논의 구분**(최근 전략 결정 수집에 직결): 토스 Topic — 메신저는 스레드 단위로 요약하고 "결정된 내용과 결론이 나지 않은 내용을 명시적으로 나눠요." 문서와 코드가 다를 때 항상 코드가 옳은 건 아니다(문서=목표 상태일 수 있음) `[W37]`.
- **개념 페이지 작성 프롬프트의 근거(STORM)**: Shao 외 2024(arXiv 2402.14207, NAACL 2024 Main 확인) — pre-writing(관점 발견 → 질문-답 대화 시뮬레이션 → 개요)이 핵심. "more of STORM's articles are deemed to be organized (by a 25% absolute increase) and broad in coverage (by 10%)." 편집자가 꼽은 새 실패 "source bias transfer and over-association of unrelated facts" → lint 점검 항목으로 `[P5-1]`. Co-STORM(arXiv 2408.15232, EMNLP 2024 Main 확인): "70% of participants prefer Co-STORM over a search engine, and 78% favor it over a RAG chatbot." 탐색 중 지식을 마인드맵에 누적 = 답변 환류 `[P5-2]`.
- **Claude 문체 문제**: Platformer — Claude의 "hyper-compressed, borderline-unreadable house style" 때문에 스타일 재작성이 필요했다(GPT로 AP 스타일 재작성) `[W3]` `[C]`.
- **답변 환류의 이론적 선조**: Generative Agents reflection `[P1-2]`; Reflexion(Shinn 외 2023, arXiv 2303.11366, NeurIPS 2023 미확인) — 실패를 말로 성찰해 episodic memory에 쌓음(HumanEval pass@1 91% vs GPT-4 80%) → "lint 결과를 다음 ingest에 반영" 루프 `[P 부록A]`. Agent Workflow Memory(arXiv 2409.07429) — 과거 궤적에서 재사용 가능한 워크플로를 귀납(Mind2Web +24.6%, WebArena +51.1% 상대) → schema에 "자주 쓰는 질의 절차"를 쌓는 아이디어 `[P 부록A]`. Taktile — 사전 인제스트 없이 "the wiki fills itself as a byproduct of answering questions." 긍정 평가된 답만 사실 항목으로 증류 `[C]`.

### 3.4 소요 시간·비용 기대치 (전부 자기 보고)
- julianoczkowski 가이드: 수집은 소스당 5~15분 `[W10]`(웹, ★54).
- vbarsoum(HN): 책 3권(68파일, 약 15.5만 단어) 컴파일에 약 12M 토큰, 10~15분, 173K 단어 출력 `[C]`.
- 클리앙: 500+ 메모 등록 20분+ `[W6]`; 클리앙 댓글 프밍(2026-04-27): 업무 글 약 60개로 Claude Pro 토큰 이틀 가까이 소진 `[C]`.
- gist 댓글 Helleeni: 한 시간 만에 개인 위키 → "burnt through my tokens for one Claude Code session". grishasen: 이틀 걸려 만들었는데 하루 만에 만든 로컬 RAG보다 못하고 "consumes a significant number of tokens." `[C]`
- Ghelbur: /x-read ~$0.05, /research-deep $0.40–0.80 `[C]`. Jim Liu: 하루 ~15분 유지, 주간 린트 20분, 격주 서브에이전트 모순 탐지 1회 < $0.40(Opus 1M 컨텍스트) `[C]`.
- GeekNews alfadur(2026-07): 자율 멀티에이전트로 돌리니 "토큰만 5~10배 잡아먹고 컨텍스트도 자주 놓칩니다." `[C]`
- 반대 사례: glaucobrito(gist, 2026-04-09) — 33일, 1,493 관측, 부팅 ~8K 토큰, "$0 cost"(구독 범위 내). Jim Liu — Claude Pro $20/월 기존 구독이라 한계비용 0 `[C]`.
- AI매터스가 인용한 LinkedIn 분석: "위키의 모든 컴파일, 린트, 쿼리는 클로드 코드의 토큰을 태운다. 진짜 돈이다." `[C]`

---

## 4. 어디에 저장하고 어떻게 호스팅하는가

### 4.1 마크다운 + git이 기본
- 원문: "The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free." `[W1]`
- lucasastorian/llmwiki(★1.7k, 포크 235, 커밋 185, Apache-2.0): "The filesystem is the source of truth; the index just makes it fast to search." `VaultFS` 추상화로 로컬(SQLite+파일시스템)/호스팅(Postgres+S3) 전환. 스택 Python 3.11+, Node 20+/Next.js, Docker Compose, 선택적 LibreOffice·Mistral OCR `[W8]`(웹, README 1차).
- Stigmergy(팀용, 2026-08): "Postgres is operational state and a rebuildable index, never a second wiki." + 야간 전체 리빌드로 수렴 보장 `[C]`.
- 마크다운파: HN dhruv3006·left-struck — 마크다운은 내구성이 있고 어디서나 읽힌다. Google OKF — 텍스트 파일 + 규약 `[C]`.
- 마크다운을 떠날 시점(H15) `[C]`: bradwmorris — 파일시스템 접근 6–12개월 뒤 지식과 에이전트 수가 늘자 SQLite가 "the best abstraction for agents". mpazik — "Flat markdown doesn't query well and gets inconsistent" → 구조화 DB가 마크다운으로 렌더 + 양방향 동기화. rjbudzynski — index.md·log.md를 SQLite/DuckDB 테이블로? YIING99 — 다중 에이전트·연속 write-back이면 pgvector 원격 MCP 층. 절충 신호: 수백 페이지·다중 writer·연속 write-back이 겹치면 DB.
- 한국: kurthong — Obsidian vault를 GitHub으로 머신 간 백업 `[C]`. velog theafh — 위키를 코드 저장소에 함께 커밋, 결정 근거·런북 기록 `[C]`.

### 4.2 Claude Files API에 올릴 것인가
- "Upload files once, reference them by file_id in Messages requests" / "**Uploaded files are accessible to your entire workspace, not scoped to an end user, conversation, or session.** [...] Never accept `file_id` values from end users or other untrusted sources" / "If you are building a multi-tenant application on the Files API, create a separate workspace for each tenant. [...] Each organization can have up to 100 workspaces" / 한도 "**Maximum file size:** 500 MB per file" / "**Total storage:** 1 TB per organization" / "approximately 500 requests per minute" / "Files cannot be modified or renamed after upload. To change a file's content, upload a new file and delete the old one" / 만료 `expires_in_seconds` 3,600(1시간)~7,776,000(90일) / ".md files, can either be read in this way or uploaded through the Files API with an explicit `text/plain` content type." / "The Files API is out of beta and needs no beta header." (SDK: Python 1.2.0, TypeScript 0.122.0 이후 `client.files`) / "Files API operations are free" / "File content used in Messages requests is priced as input tokens." `[W19]`(공식, GA, 2026-10-11 열람). 구 헤더 `anthropic-beta: files-api-2025-04-14` 설명은 구버전 정보일 수 있음 `[W 교차검증 메모]`.
- 함의: 불변 파일 특성은 raw/에 맞고, 자주 고치는 wiki/는 로컬 파일시스템·git이 맞다(리서처 해석).

### 4.3 사람이 읽는 뷰 — Obsidian / Quartz / Docusaurus
- Obsidian: Karpathy·Newton·Jim Liu·julianoczkowski 모두 Obsidian 볼트 + Claude Code `[W1]` `[W3]` `[W10]` `[C]`. Newton 설정: Claude Fable 5로 프롬프트 작성 → Ghostty 터미널 → Obsidian 볼트 + Web Clipper + Claudian 플러그인(기사 요약) `[W3]`.
- Quartz v5.0.0(Jacky Zhao): "Quartz is a fast, batteries-included static-site generator that transforms Markdown content into fully functional websites." backlinks·graph view·full-text search·wikilinks·Obsidian 호환, 배포 GitHub Pages/Cloudflare/Netlify/Vercel. **인증/비공개 호스팅은 문서에 없음** — 사내용은 리버스 프록시/SSO 뒤에(별도 확인 필요). 커뮤니티 플러그인 "Private Quartz Publish"는 추측 불가 슬러그 방식(보안 아님) `[W31]`(웹, 공식 문서).
- Docusaurus vs Quartz vs Obsidian Publish: 셋 다 네이티브 인증 없음. 사내 위키는 SSO 프록시(예: Cloudflare Access, oauth2-proxy) 뒤에 — **1차 소스 미확보 (사실 확인 필요)** `[W32]`(웹, 비교 사이트/벤더 글, 신뢰성 하~중).
- 논쟁 D(Obsidian vs 커스텀) `[C]`: WUPHF OP najmuzzaman — Obsidian은 "a single-user editor", 승격 상태 기계와 MCP 표면이 에디터 밖에 필요. rothnic — 분산 공유 KB엔 "wasn't well suited". Zetaphor — Obsidian은 로컬 마크다운 위의 클라이언트일 뿐이라 에이전트 하네스와 같은 머신이면 잘 맞음. SOLAR_FIELDS — QMD + Obsidian vault면 2시간 안에 80%. 팀 함의: 뷰어로서의 Obsidian은 무해, 동시 쓰기·권한·승인 흐름은 Obsidian 밖(git/CI/MCP)에.
- 민감 문서 우려: HN sails — 민감 비즈니스 문서를 GitHub에 올리는 것이 꺼려짐, Cloudflare·GCP 내부 배포 원함 `[C]`. 노션 AI 활용 블로그 — 민감 DB는 접근 제한 (https://maketimelab.com/ai-2026/, 개인 블로그 권고) `[C]`.

### 4.4 팀 공유 시 터지는 것들 (패턴 9)
- gist 첫날 geetansharora — 팀과 어떻게 공유하나? 이미 쓰는 RAG + MCP 서버 방식을 따라야 하나? (답 없음). MoserMichael — "Who decides what becomes a memory, and how is it evaluated?" alinawab — "What's the failure mode? Where does it start fighting you?" (답글 없음) `[C]`.
- HN WUPHF: Abby_101 — 에이전트가 스스로 승격해도 되나, 사람 리뷰가 필요한가? psteinweber — 소규모 마케팅 팀, 사람 여러 명 + human-in-the-loop 지원 여부 `[C]`.
- ap0phasi — 조직 간 데이터 출처 오염 우려 → 인제스트마다 git 브랜치. xoai — 미해결 갭 "proposition-level provenance and multi-writer wikis." renan_warmling — 스냅샷·롤백 기록 부재, 시간적/비시간적 기억 미분리 `[C]`.
- Stigmergy README: 여러 사람·에이전트가 공유하는 순간 "you need what a shared deployment forces on you: identity, visibility, concurrency, binary evidence, Slack, audit." `[C]`
- 멀티테넌트 격리는 Files API 워크스페이스(4.2) 또는 자체 인프라.

---

## 5. 스키마(CLAUDE.md)와 시스템 프롬프트를 어떻게 쓰는가

### 5.1 스키마 파일이 가장 중요한 파일
- Karpathy 원문(1.3절 Schema 행). Jim Liu: "The pattern works, but only if you treat the schema file as the most important file." `[C]`. GPTers 비케이(2026-05-27): "CLAUDE.md에 명령어 체계를 정의했습니다." / "클로드 코드 CLI 환경이 필요합니다 (웹 클로드로는 어려움)" `[W7]`(웹). velog 댓글 ColonelPanicX·AgriciDaniel — 스키마 파일로 규칙을 고정해야 세션마다 일관 `[C]`.
- 토스 하네스 글의 관점: "사람이 읽으면: 업무 가이드라인이자 매뉴얼이 되고," / "LLM이 읽으면: 정확한 지시사항이 담긴 시스템 프롬프트가 됩니다." / "문서 관리의 패러다임이 '기록'에서 '실행'으로 바뀌는 셈입니다." `[W38]`.

### 5.2 Claude Code 공식 작성 규칙 (CLAUDE.md)
`[W24]`(공식, https://code.claude.com/docs/en/memory, 2026-10-11 열람; 일부 기능은 Claude Code v2.1.2xx 이상) `[W25]`(공식, best practices):
- "Each Claude Code session begins with a fresh context window. Two mechanisms carry knowledge across sessions: **CLAUDE.md files** [...] **Auto memory**: notes Claude writes itself based on your corrections and preferences" — 표: CLAUDE.md "Who writes it: You / What it contains: Instructions and rules" vs Auto memory "Who writes it: Claude / Loaded into: Every session (first 200 lines or 25KB)".
- "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead." / "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens."
- "Keep it to facts Claude should hold in every session: build commands, conventions, project layout, 'always do X' rules. If an entry is a multi-step procedure or only matters for one part of the codebase, move it to a skill or a path-scoped rule instead."
- "**Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." / "**Consistency**: if two instructions contradict each other, Claude may pick one arbitrarily."
- "Keep it concise. For each line, ask: *'Would removing this cause Claude to make mistakes?'* If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" / "The over-specified CLAUDE.md. If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise."
- 포함/제외 표: Include "Bash commands Claude can't guess", "Architectural decisions specific to your project", "Common gotchas" / Exclude "Anything Claude can figure out by reading code", "Information that changes frequently", "File-by-file descriptions of the codebase".
- import: "CLAUDE.md files can import additional files using `@path/to/import` syntax. [...] maximum depth of four hops." / "Imports help you organize a long file but don't reduce its context cost, because imported files also load at launch."
- 위치: Managed policy(`/Library/Application Support/ClaudeCode/CLAUDE.md` 등) / User(`~/.claude/CLAUDE.md`) / Project(`./CLAUDE.md` 또는 `./.claude/CLAUDE.md`) / Local(`./CLAUDE.local.md`, gitignore). "CLAUDE.md and CLAUDE.local.md files in the directory hierarchy above the working directory are loaded at launch. Files in subdirectories load on demand." → raw/·wiki/ 별 하위 CLAUDE.md로 규칙 분리.
- `.claude/rules/`: "Rules can also be scoped to specific file paths, so they only load into context when Claude works with matching files".
- AGENTS.md: "By default, Claude reads `AGENTS.md` only when you have no `CLAUDE.md` in your working directory or above it." (v2.1.277+).
- `/doctor prompt-audit`: "Claude looks for problems such as instructions written for older models, references to files or commands that don't exist, and files that contradict each other." (v2.1.283+).
- 검증 가능하게: "Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from."
- 커뮤니티 교차 근거: Claude Code 이슈 #42796(2026-04-02, 댓글 583) — 5,000+ 단어 CLAUDE.md의 규약을 모델이 무시했다는 보고 `[C]`. HN kwar13 — 모델이 "can't even keep up with a simple claude.md let alone a whole wiki." criley2 — "bloated CLAUDE.md files filled with data that agents can gather on the spot"가 결과를 해친다, arXiv 2602.11988(자동 생성 AGENTS.md가 더 나쁨) 인용 — **이 논문은 papers.md에 없음 (사실 확인 필요)**; 사람이 쓰고 짧게 유지하라는 쪽 `[C]`. Yuncun — 성숙한 코드베이스에서 "keep docs updated" 같은 긴 문서는 그냥 AI slop `[C]`.
- 역할 호칭 함정: justinzhang2039(2026-04-06) — 스키마에서 사람을 "You"라고 쓰면 자기 페르소나를 "You"로 보는 에이전트와 "role-mapping conflict"가 난다 → "User"/"Assistant"로 `[C]`.

### 5.3 시스템 프롬프트의 "고도"와 구조
- Anthropic: "The right altitude is the Goldilocks zone between two common failure modes." `[W14]`.
- 에이전트는 "maintain lightweight identifiers (file paths, stored queries, web links, etc.)"를 유지하고 런타임에 로드; Claude Code는 "glob and grep"로 "navigate its environment and retrieve files just-in-time." 자율 탐색은 "enables progressive disclosure" — 에이전트가 "incrementally discover relevant context through exploration." `[W14]` → index.md + grep가 통하는 이유.
- LY Corporation 설계 메모: 응답 가이드라인을 시스템 프롬프트가 아니라 도구 메시지로 주입(강제 지침이 아닌 참고로 인식되게), API 응답에 필드 설명 스키마를 붙이고 YAML 채택(토큰 효율). 질문별 도구 선별: "Redis 클러스터 상태" 질문 시 도구 8개만 제공하고 252개는 제외(제품군 27개, API 260여 개, 문서 수백 페이지). "'컨텍스트 엔지니어링'은 LLM에게 '필요한 정보만 선별해서 제공하는 것'입니다." `[W40]`.
- 판정 단계를 프롬프트에: Self-RAG(Asai 외 2023, arXiv 2310.11511, ICLR 2024 S2 표기, 피인용 2,809)의 reflection token 4종(Retrieve / IsRel / IsSup / IsUse) — "indiscriminately retrieving and incorporating a fixed number of retrieved passages, regardless of whether retrieval is necessary, or passages are relevant, diminishes LM versatility or can lead to unhelpful response generation." → 시스템 프롬프트에 IsRel/IsSup 판정을 흉내 내는 체크 단계 `[P2-5]`. CRAG(Yan 외 2024, arXiv 2401.15884, 프리프린트)의 Correct / Incorrect / Ambiguous 3분기 — "a lightweight retrieval evaluator is designed to assess the overall quality of retrieved documents for a query, returning a confidence degree based on which different knowledge retrieval actions can be triggered." → "wiki에 없으면 없다고 말하기"의 판정 구조. 재현 보고: Yalavarthi 2026, arXiv 2603.16169 `[P2-6]` `[P 부록A]`.
- 간결·근거 명시 지시(FreshLLMs) `[P3-10]`. 초안 → 근거 있는 사실만 남기기(WikiChat, Semnani 외 2023, arXiv 2305.14292, Findings of EMNLP 2023 확인): "WikiChat generates a response from an LLM, retains only the grounded facts, and combines them with additional information it retrieves from the corpus"; GPT-4 대비 head/tail/recent 지식에서 +3.9%/+38.6%/+51.0% → 사내 지식(대부분 tail·recent)에 맞는 메시지 `[P4-8]`.
- 모순 출력은 구조화해서: Resolving Knowledge Conflicts(Wang 외 2023, arXiv 2310.00935, COLM 2024 확인) — "while LLMs perform well in identifying the existence of knowledge conflicts, they struggle to determine the specific conflicting knowledge and produce a response with distinct answers amidst conflicting information." → lint 프롬프트는 "어느 줄과 어느 줄이 충돌하는지" 출력 `[P3-4]`.
- 소스 텍스트는 데이터: Stigmergy — "Captured content is data, never instructions." / Fontoura — 소스 텍스트는 데이터로 취급(프롬프트 인젝션 방어) `[C]`.
- 토스 Topic의 "없음" 답변 설계: "`insufficient_evidence`도 실패가 아니에요." / "이 조각은 답변을 만드는 재료로는 유용하지만, 그 자체로 신뢰할 수 있는 컨텍스트는 아니에요." `[W37]`.

### 5.4 스키마 vs 스킬 vs 훅 — 역할 분담
- Agent Skills(Anthropic, 2025-10-16, 2025-12-18 업데이트: Agent Skills 오픈 표준): "A skill is a directory containing a SKILL.md file" / 필수 frontmatter "`name` and `description`" / 3단계 progressive disclosure(메타데이터 preload → SKILL.md 본문 → 참조 파일) / 번들 가능한 컨텍스트는 "effectively unbounded." / "Agent Skills are supported today across Claude.ai, Claude Code, the Claude Agent SDK, and the Claude Developer Platform." **2차 자료의 "SKILL.md 본문 5,000토큰/500줄 이하", "스킬당 메타 ~100토큰"은 이 글에 없음 — 사용 시 (사실 확인 필요)** `[W23]`(공식).
- 패턴을 스킬로 패키징한 사례: Astro-Han — `npx add-skill Astro-Han/karpathy-llm-wiki`(Claude Code·Cursor·OpenCode), Codex CLI는 `.agents/skills/karpathy-llm-wiki/`에 복사; ingest(raw 수집→triage→생성/갱신/로그), query(인용 포함 답변), lint(index 무결성·링크·건강; 자동수정+보고) `[W9]`. LY ODW #5 — MCP만으로는 "도구 호출법"만 공유되므로 DB의 컬렉션·ID 형식·메타데이터를 가르치는 스킬을 얹음; "'SE-0500을 조사해줘'와 같은 최소한의 지시만으로 Swift Evolution 내용을 검색할 수 있게 되었습니다." `n_results` 축소로 출력 잘림 대응 `[W41]`(웹, 발행일 미표시).
- 훅으로 강제(H1): "Instructions set intent. Hooks enforce behavior" / "A hook script that exits with code 2 blocks the action deterministically." (Fulkerson) `[C]`. @vellumkasane — "'raw is immutable' in a CLAUDE.md is a wish, not a rule."; PreToolUse 훅으로 raw/ 아래 기존 파일 수정·덮어쓰기 차단(신규 추가·append만 허용), Stop 훅이 `git status --porcelain`과 미푸시 커밋을 검사해 푸시 전엔 턴을 못 끝내게 `[C]`. Agent SDK 훅 세부는 6.8절.
- 입문 프롬프트 원문(julianoczkowski) `[W10]`: 설정 "You are my LLM Wiki agent. Build my complete second brain from this file." / 수집 "I just added a new file to raw. Please ingest it." / 점검 "Run a health check on the wiki" / "Run a lint on the wiki" / "What do I know about [topic]?"

---

## 6. 에이전트가 위키를 어떻게 참조하는가 (검색 계층·Claude 플랫폼 기능)

### 6.1 질의 루프의 원형 — ReAct·IRCoT
- ReAct(Yao 외 2022, arXiv 2210.03629, ICLR 2023 확인, 피인용 12,364): "ReAct overcomes issues of hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a simple Wikipedia API". ALFWorld·WebShop에서 +34%·+10% 절대 향상. "Wikipedia API"를 "사내 wiki 파일 시스템"으로 치환하면 그대로 책의 아키텍처 — `grep`·`read file`·`follow link`를 번갈아 호출 `[P2-3]`.
- IRCoT(Trivedi 외 2022, arXiv 2212.10509, ACL 2023 확인): "what to retrieve depends on what has already been derived, which in turn may depend on what was previously retrieved." GPT-3로 검색 최대 +21점, 다운스트림 QA 최대 +15점. "질문 한 번에 top-k 한 번"이 왜 사내 Q&A에서 자주 틀리는지; 위키 링크를 따라가며 재검색 = IRCoT의 수동 구현 `[P2-4]`.
- Search-R1(Jin 외 2025, arXiv 2503.09516, 프리프린트, 피인용 1,587): "Prompting advanced LLMs with reasoning capabilities to use search engines during inference is often suboptimal, as the LLM might not fully possess the capability on how to interact optimally with the search engine." **버전 간 불일치: RAG 대비 상대 개선이 arXiv v5 초록 41%(Qwen2.5-7B)·20%(3B), HTML 본문 초록 24%·20% → 인용 시 "20~41% 상대 개선(버전에 따라 상이)"**. 사내 에이전트는 학습 대신 schema의 검색 규약으로 같은 효과를 노린다는 대비 구도 `[P2-7]`.
- 우아한형제들 물어보새: 고정 워크플로가 "개발자가 설계한 순서에만 의존했기 때문에 새로운 질문이 등장할 때마다 코드를 수정해야 하는 비효율적이고 유지보수 불가능한 구조로 이어졌습니다." → ReAct 에이전트로 전환. (Anthropic 엔지니어 조언) "LLM에게 믿고 위임하세요." `[W39]`.
- Dev.to 2차: Claude Code는 정적 임베딩 대신 grep/ls/cat을 Plan–Act–Observe 루프에서 동적으로 쓴다. 벡터 RAG는 "구조가 약한 산문·표현이 다양한 개념 질문"에 여전히 유리 — 숫자 인용은 삼갈 것 `[W45]`(웹, 신뢰성 중~하).

### 6.2 검색 계층 로드맵: index.md → grep → BM25 → 하이브리드 → 벡터
- **0단계 index.md 먼저 읽기**: gist "~100 sources, ~hundreds of pages" `[W1]`. 규모 한계에 관한 자기 보고들(서로 모순되지 않으나 "경험치") `[W 교차검증 메모]` `[C]`:
  - singularityjason(2026-04-07): index.md는 "~100 pages" 넘으면 깨진다. bitsofchris(노트 4,000+개): "Index files will break" at scale. manavgup: index.md/log.md가 "scales worse than expected." mpazik: 수백 페이지 넘으면 쿼리가 깨지고 규칙이 슬금슬금 늘어난다.
  - rohitg00 "LLM Wiki v2" gist: "This works up to maybe 100-200 pages." 인덱스는 사람용 카탈로그로만, "don't rely on it as the LLM's primary search mechanism past ~100 pages."
  - julianoczkowski: "수백 문서까지는 잘 되고, 그 이상은 임베딩+벡터DB RAG 권장" `[W10]`. 클리앙: 500+ 메모 문제없음(단 느림) `[W6]`. tashisleepy: 약 50문서까지는 위키만으로 충분, "The Memvid layer earns its keep at 500+ docs when grep gets slow." Jim Liu: 35페이지에서 grep 40–50ms면 충분, 500페이지쯤 재검토.
  - 인덱스를 아예 계산하거나 빼라(H5): jermolene(TiddlyWiki 창시자) — LLM은 인덱스 동기화를 못 지키므로 computed views가 hand-maintained index.md보다 낫다. panakh — "you don't really need the index for it" — LLM이 `ls` 하면 된다. 0xjaishy — 메타 쿼리에 index 페이지가 top-1로 뜨는 문제; clue.oz4e — 인덱스 파일을 검색 색인에서 빼야 한다.
  - AI매터스: "자료가 늘어날수록 인덱스 자체가 비대해져 매 쿼리에 들어가는 컨텍스트가 커진다."
- **1단계 grep**: Anthropic "glob and grep" just-in-time `[W14]`. 한계 — Taktile 벤치(88항목 위키, 24쿼리): grep은 K=3에서 관련 항목의 약 1/5만 — "grep is not viable." 지연: LLM 판단 69.1초/쿼리(정확도 1위), 벡터 12.28ms, grep 6.00ms, BM25 0.47ms. RRF 하이브리드는 K=10에서 recall 0.90이지만 쓰레기 8건 동반. 결론 "BM25 is the pragmatic middle." `[C]`(자기 보고). HN softwaredoug(해설 인용): "grep is fine if you don't care about tokens and you have less than 100k files." `[W44]`.
- **grep vs 벡터 — 하네스가 좌우한다**: PwC 논문 "Is Grep All You Need?"(arXiv 2605.15184, 2026-05-14) LatentEval 해설(2026-08-03): LongMemEval 116문항, 하네스 4종(Chronos, Claude Code, Codex CLI, Gemini CLI) × 모델 5종. 결과를 인라인으로 돌려주면 grep이 10쌍 전부에서 벡터를 이김; 결과를 파일에 쓰면 5/10에서 역전. 같은 Opus 4.6도 하네스에 따라 93.1% vs 76.7%. 저자 결론: 하네스를 바꾸면 "shifts the ceiling by roughly as much as swapping retrievers within a fixed harness." 범위 한정: "tied to long-memory conversational QA"이며 grep이 일반적으로 "beats" vector라고 주장하지 않음. **주의: 116문항 단일 점추정·신뢰구간 없음, 동일 조건을 76.7%/94.0%로 다르게 적은 표 불일치, v1 프리프린트. papers.md에 항목 없음 — 수치는 논문 대조 필요** `[W44]`(웹, 2차 해설).
- **2단계 BM25 (+ 하이브리드)**: Anthropic Contextual Retrieval(2024-09-19, **2024년 기준**): "BM25 (Best Matching 25) is a ranking function that uses lexical matching to find precise word or phrase matches." 청크에 맥락 문장을 붙이면 — "Contextual Embeddings reduced the top-20-chunk retrieval failure rate by 35%" (5.7% → 3.7%) / "Combining Contextual Embeddings and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 49%" (5.7% → 2.9%) / "Reranked Contextual Embedding and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 67%" (5.7% → 1.9%) / "the one-time cost to generate contextualized chunks is $1.02 per million document tokens" (800토큰 청크·8k 문서 가정, 2024 가격). 청크 맥락 프롬프트 원문: "Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else." `[W15]`(공식) → 위키 페이지 상단 TL;DR이 사실상 "맥락 문장" 역할.
  - HN WUPHF OP: 500 아티팩트·50 쿼리에서 BM25 단독 recall@20 85%; 특정 쿼리 클래스가 그 아래면 sqlite-vec 폴백 `[C]`(자기 보고, 확인 필요). 우아한형제들: BM25s로 "약 15%의 검색 품질 향상을 확인했습니다" — **"BM25s 최대 500배 빠름"은 요약 수치, 원문 대조 (사실 확인 필요)** `[W39]`.
  - BM25 편향 경고: Blake Crosley — BM25는 키워드 밀도를 보상하므로 "잘 태깅된 얕은 문서가 깊은 문서를 이길 수 있음". FTS5 BM25 + Model2Vec 벡터 + RRF; "16,894 files → 49,746 chunks, 83 MB". 권장: FTS5 가상 테이블(BM25만)부터 시작해 RRF는 마지막에 `[W13]`(웹, 2026, 정확 일자 미확인). 반론: TheLazyLizzard — BM25는 빠르지만 "results in a lack of accuracy." Daniel-sims — BM25 문서 조회가 토큰을 더 많이 돌려준다 `[C]`.
  - **한국어 특이사항**: kurthong — BM25가 한국어 검색에 약해 한국어 쿼리용 가드레일을 추가 `[C]`.
- **3단계 qmd (Karpathy 지명 도구)**: tobi/qmd ★30.3k, 포크 1.9k, 커밋 781, MIT(2026-10-11 기준). "mini cli search engine for your docs, knowledge bases, meeting notes, whatever." BM25 + 벡터 + LLM 재순위를 node-llama-cpp/GGUF로 온디바이스. CLI `qmd search`(BM25), `qmd vsearch`(벡터), `qmd query`(쿼리 확장+하이브리드+재순위), `get`, `multi-get`, `collection`, `context`, `embed`, `update`, `status`; MCP 서버(`query`, `get`, `multi_get`, `status`, `metadata`; stdio/HTTP). 설치 `npm install -g @tobilu/qmd` 또는 `bun install -g @tobilu/qmd`; Node.js 22+ 또는 Bun 1.0+; macOS는 Homebrew SQLite 필요. 자동 다운로드 모델: embeddinggemma-300M(~300MB), qwen3-reranker-0.6b(~640MB), qmd-query-expansion-1.7B(~1.1GB). 아키텍처: SQLite FTS5(BM25) + sqlite-vec(벡터), ~900토큰 청크 15% 겹침 `[W12]`(웹, README 1차 + mintlify 문서). 한국: mosfet1kg — qmd + qwen 0.6B 임베딩 "이정도는 로컬로도 충분히 다 하네요." `[C]`.
- **벡터는 "모르는 단어"용**: 커뮤니티 합의에 가까운 것 — "작은 규모·고정 용어는 grep+긴 컨텍스트, 수백 문서 넘으면 BM25, 용어를 모를 때만 벡터" — 그리고 셋 중 무엇이든 "쓰기 루프(컴파일·린트)"가 진짜 차별점 `[C]`. bitsofchris — 3배 overfetch → 중복 제거 → MMR 재순위 `[C]`. NoLiMa의 어휘 불일치 결과가 벡터/동의어 페이지의 근거 `[P2-11]`.
- **위키=지도 + 하이브리드 RAG**: clue.oz4e — 위키를 "지도"로 격하하고 내용 검색은 하이브리드 RAG → recall@5 93%(자기 보고). 역할 분리: 위키는 누적 이해, 근거 문장은 원본에서, provenance 부착 `[C]`.
- **싼 경로/비싼 경로 라우팅**: LC vs RAG(Li 외 2024, arXiv 2407.16833, EMNLP 2024 Industry 확인): "when resourced sufficiently, LC consistently outperforms RAG in terms of average performance. However, RAG's significantly lower cost remains a distinct advantage." LC가 RAG를 평균 7.6%(Gemini-1.5-Pro), 13.1%(GPT-4O), 3.6%(GPT-3.5-Turbo) 앞섬; Self-Route 비용 65%(Gemini-1.5-Pro)·39%(GPT-4O) 절감, 성능 차 −0.2%(GPT-4O)·−2.2%(Gemini)·+1.7%(GPT-3.5). **RAG 실패 유형은 4개 범주(A~D)+기타 — "7가지"가 아님**. index.md 읽기(싼 경로) vs 소스 원문 전체 읽기(비싼 경로)를 LLM이 고르는 것이 Self-Route의 실무판 `[P2-12]`.
- 실시간 소스 병행: 우아한형제들 — "Atlassian MCP 서버로 Confluence Wiki·Jira의 최신 정보와 저장하지 않았던 데이터까지 실시간으로 가져올 수 있게 되었습니다." / "연결 실패 시에는 자동으로 벡터 스토어 기반 검색으로 전환하는 Fallback 전략을 적용했습니다." `[W39]`.

### 6.3 MCP로 위키 노출하기
- Claude Code MCP 문서: "Claude Code can connect to hundreds of external tools and data sources through the Model Context Protocol (MCP), an open source standard for AI-tool integrations." `claude mcp add --transport http <name> <url>` / `claude mcp add [options] <name> -- <command> [args...]`(stdio). "HTTP servers are the recommended option for connecting to remote MCP servers." / "The SSE (Server-Sent Events) transport is deprecated." / "Project-scoped servers enable team collaboration by storing configurations in a `.mcp.json` file at your project's root directory." / "For security reasons, Claude Code prompts for approval in interactive sessions before using project-scoped servers from `.mcp.json` files." / tool search "which is on by default" `[W30]`(공식). 예: `claude mcp add --transport http notion https://mcp.notion.com/mcp` `[W25]`.
- llmwiki MCP 도구 목록: `guide`, `read`, `create`, `edit`, `append`, `delete`, `search`(브라우즈·전문검색·인용그래프·stale/uncited 조회), `lint` `[W8]`. qmd MCP(6.2). Agent SDK의 MCP: "Connect external tools and data sources via the Model Context Protocol" `[W26]`.
- MCP + Skill 조합(LY ODW #5)은 5.4절 `[W41]`.

### 6.4 서브에이전트로 위키 탐색 격리
- Anthropic: "specialized sub-agents can handle focused tasks with clean context windows." `[W14]`. best practices: "Delegate research with 'use subagents to investigate X'. They explore in a separate context, keeping your main conversation clean for implementation." `[W25]`.
- Agent SDK Subagents: "**Context isolation**: each subagent runs in its own conversation [...] A `research-assistant` subagent can explore dozens of files without any of that content accumulating in the main conversation. The parent receives a concise summary, not every file the subagent read." / "**Tool restrictions**: subagents can be limited to specific tools [...] A `doc-reviewer` subagent might only have access to Read and Grep tools, ensuring it can analyze but never accidentally modify your documentation files." AgentDefinition 필드: `description`(필수), `prompt`(필수), `tools`, `disallowedTools`, `model`, `skills`, `memory`('user'|'project'|'local'), `mcpServers`, `maxTurns`, `background`, `omitClaudeMd`, `effort`, `permissionMode`. "The only content you pass from parent to subagent is the Agent tool's prompt string". 한도 기본값: 깊이 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`=3, 동시 `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`=20, 비용 `maxBudgetUsd`/`max_budget_usd`(TS v0.3.219 / Py v0.2.127 이후). "Claude Opus 5 delegates to subagents more readily than earlier models, so the depth, concurrency, and spend limits matter most on queries that run Opus 5." `[W27]`(공식).
- Python 예(문서 그대로 일부) `[W27]`:
  ```python
  from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition
  async for message in query(
      prompt="Review the authentication module for security issues",
      options=ClaudeAgentOptions(
          allowed_tools=["Read", "Grep", "Glob", "Agent"],
          agents={"code-reviewer": AgentDefinition(
              description="Expert code review specialist. Use for quality, security, and maintainability reviews.",
              prompt="...", tools=["Read", "Grep", "Glob"], model="sonnet")},
      )): ...
  ```
- 커뮤니티 경고: 자율 멀티에이전트는 토큰 5~10배(alfadur) `[C]`; writer와 judge 분리, judge는 writer 의도를 못 보게 `[C]`.

### 6.5 Citations API — 답변에 출처 강제
- "Ground Claude's responses in your source documents. Citations return the exact passages that support each claim, so you can verify answers and surface sources to your users." / "All active models support citations." / 활성화: document 블록에 `"citations": {"enabled": true}` / "By default, plain text and PDF documents are automatically chunked into sentences. If you need more control over citation granularity (for example, for bullet points or transcripts), use custom content documents instead." / "**Better citation reliability:** Because the API parses citations into the response formats described in the following sections and extracts `cited_text` directly, citations are guaranteed to contain valid pointers to the provided documents." / "Enabling citations incurs a slight increase in input tokens because of system prompt additions and document chunking." / "The `cited_text` field is provided for convenience and does not count toward output tokens." / "**Citations cannot be used together with structured outputs.** [...] the API returns a 400 error." / citation 객체 예: `"type": "char_location"`, `"cited_text"`, `"document_index": 0`, `"start_char_index"`(0-indexed). `search_result` 블록으로 자체 검색 결과 전달 가능 `[W18]`(공식, GA, 2026-10-11 열람).
- 왜 API 수준 인용이 필요한가(커뮤니티 패턴 3): manavgup — 위키링크를 "hallucinates 404s". ShootJackal — 노트가 파일 경계를 위조해 조작된 답에 VERIFIED 표식을 받은 적이 있다; 지금은 "a check with no model in it confirms each quote is in the cited note at that commit." tomjwxf — "가장 중요한 미해결 문제": 인용 없이 합성, 원본에서 멀어짐, 거짓 확신. Valentin-Laurent — 정확한 출처 인용이 "one of the trickiest parts". Marekai — 페이지 번호가 사라지고 paraphrase가 생겨 "(Author, Year, p. 47)" 식 인용을 못 만든다 → 학술·규제 용도 치명 `[C]`. llmwiki 이슈 #52 — 인용이 페이지 수준인지 주장 수준인지 미정의 `[C]`.
- 인용 품질 측정 근거는 9절(ALCE·Verifiability).

### 6.6 컨텍스트 윈도우 · 프롬프트 캐싱 (2026-10-11 공식 문서 기준 — 집필 시 재확인)
- 컨텍스트: "Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5, Claude Opus 5.5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5.5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Haiku 5.5, and Claude Mythos Preview have a 1M-token context window. A single request to any of them can generate up to 128k output tokens (`max_tokens`). Other Claude models, including Claude Sonnet 4.5 (deprecated), have a 200k-token context window." / "For every model with a 1M-token context window, 1M is the default: you don't need a beta header, and long-context requests are billed at standard pricing, except on Claude Haiku 5.5, where prompts over 100,000 tokens cost more." / "Everything in the request counts toward the context window: the system prompt, every message in `messages` (including tool results, images, and documents), and your tool definitions." / "Cached prompt prefixes still occupy the context window: prompt caching changes what you pay for those tokens, not whether they count." `[W17]`. **2차 블로그의 "2026-03-13 1M GA(Opus 4.6/Sonnet 4.6)" 날짜는 1차 문서에서 미확인 (사실 확인 필요)**.
- 캐싱: "By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used." / "You can specify a 1-hour TTL at 2x the base input token price." / "5-minute cache write tokens are 1.25 times the base input tokens price" / "1-hour cache write tokens are 2 times the base input tokens price" / "Cache read tokens are 0.1 times the base input tokens price (see the table footnote for per-model exceptions)" / 각주 "Cache hits and refreshes on Claude Fable 5.1 and Claude Mythos 5.1 are priced at 0.025x the base input price." / "Cache hits and refreshes on Claude Opus 5.5 and Claude Sonnet 5.5 are priced at 0.05x the base input price." / 최소 캐시 길이 512 토큰(Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Sonnet 5.5, Fable 5, Mythos 5, Haiku 5.5) / 1,024 토큰(Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5 등) / 2,048 / 4,096(구모델). "Shorter prompts cannot be cached, even if marked with `cache_control`." / 자동 캐싱: "add a single `cache_control` field at the top level of your request body. The system automatically applies the cache breakpoint to the last cacheable block." / "the automatic cache breakpoint uses one of the 4 available breakpoint slots." / usage 필드 `cache_creation_input_tokens`, `cache_read_input_tokens`, `input_tokens` `[W16]`(공식). → 시스템 프롬프트+index.md+스키마를 캐시 접두사로 고정, 1시간 TTL로 야간 배치 비용 절감.
- Context Rot·Lost in the Middle 등 "많이 넣을수록 좋다"의 반례는 2.1절.

### 6.7 직접 API로 지을 때: Memory tool · Files · 세션
- Memory tool(`memory_20250818`, Claude 4 이상 전 모델): "The memory tool lets Claude store and retrieve information across conversations in a directory of memory files. [...] building up knowledge over time without keeping everything in the context window." / "The memory tool operates client-side: Claude requests file operations, and your application executes them." / 설정 `{"type": "memory_20250818", "name": "memory"}` — "the `name` must be `memory`"; 명령 `view`, `create`, `str_replace`, `insert`, `delete`, `rename`; 경로 접두사 `/memories` / 자동 주입 시스템 프롬프트 "IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE. [...] ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory." / 보안 "A malicious path such as `/memories/../../secrets.env` can reach files outside the `/memories` directory. Your implementation must validate every path in every command to prevent directory traversal attacks." `[W20]`(공식). → "에이전트 메모리"(에이전트가 자기 작업용으로 쓰는 노트)와 "위키"(팀 지식)를 구분.
- Agent SDK Sessions: "A session is the conversation history the SDK accumulates while your agent works. [...] The SDK writes it to disk automatically" / "Sessions persist the **conversation**, not the filesystem." / Continue / Resume("Required when you have multiple sessions (for example, one per user in a multi-user app)") / Fork / 저장 위치 "`~/.claude/projects/<encoded-cwd>/*.jsonl`" / "To resume sessions across machines or in serverless environments, mirror transcripts to shared storage with a `SessionStore` adapter." / "**Don't rely on session resume.** Capture the results you need [...] as application state and pass them into a fresh session's prompt." `[W28]`(공식). 관련 이슈: Agent SDK #772 컴팩션·컨텍스트 임계 훅 요청(위키 재주입용), #23 비대화형 /compact, #1320 worktree 세션 키 불일치로 재개 실패 `[C]`.
- 위키를 "중간에도" 읽게: orcosto-lab(2026-09-21) — 실제 세션 9개를 감사하니 위키를 세션 시작 때만 읽고 작업 중엔 안 읽었다. "In 2 of those sessions the agent re-diagnosed from scratch a failure that already had a written lesson." `[C]`. bluewater8008 — 모든 작업은 두 가지 출력(답 + 위키 업데이트). Fulkerson — "Every skill that reads from the vault also writes back to it." `[C]`.

### 6.8 Agent SDK 훅 — raw/ 불변성·감사 로그
- "Hooks are callback functions that run your code in response to agent events, like a tool being called, a session starting, or execution stopping." 이벤트(Python+TS 공통): `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `UserPromptSubmit`, `Stop`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PermissionRequest`, `Notification`; TS 전용 다수(`SessionStart`, `SessionEnd`, `PostCompact`, `InstructionsLoaded`, `FileChanged` 등). PreToolUse 출력: `permissionDecision`("allow" | "deny" | "ask" | "defer"), `permissionDecisionReason`, `updatedInput`. "When multiple hooks or permission rules apply, `deny` takes priority over `defer`, which takes priority over `ask`, which takes priority over `allow`." matcher: "MCP tools use the pattern `mcp__<server>__<action>`". "`SessionStart` and `SessionEnd` can be registered as SDK callback hooks in TypeScript, but aren't available in the Python SDK" `[W29]`(공식).
- 예(문서 그대로, `.env` 쓰기 차단 — raw/ 차단으로 치환 가능) `[W29]`:
  ```python
  async def protect_env_files(input_data, tool_use_id, context):
      file_path = input_data["tool_input"].get("file_path", "")
      if file_path.split("/")[-1] == ".env":
          return {"hookSpecificOutput": {"hookEventName": input_data["hook_event_name"],
                  "permissionDecision": "deny", "permissionDecisionReason": "Cannot modify .env files"}}
      return {}
  options = ClaudeAgentOptions(hooks={"PreToolUse": [HookMatcher(matcher="Write|Edit", hooks=[protect_env_files])]})
  ```

---

## 7. 수집(ingest) 파이프라인 — Notion·Slack·PDF·Confluence

- **Notion**: `GET /v1/pages/{page_id}/markdown` — "Retrieve the content of a page rendered as markdown." 응답 `object: page_markdown`, `markdown`(`markdown_version=v2`면 Notion-flavored), `truncated`(레코드 한도 ~20,000 블록 또는 권한으로 잘림), `unknown_block_ids`(최대 100개; 다시 같은 엔드포인트에 넘겨 하위 트리 조회). 권한: 연결(integration)에 read content 권한 필요(없으면 403, 접근 불가/없는 페이지 404). `Notion-Version: 2026-03-11`. TypeScript SDK `notion.pages.retrieveMarkdown({ page_id })`; 같은 포맷으로 `POST /v1/pages`·`PATCH /v1/pages/:page_id/markdown`. **`include_transcript` 파라미터(2026-02-26 체인지로그; 2차 자료 matthiasfrank.de) — 사실 확인 필요** `[W34]`(공식 API 레퍼런스, 2026-10-11 열람).
- **Slack**: rusq/slackdump — 관리자 권한 없이 공개/비공개 메시지·스레드·파일·사용자 덤프, Standard/Mattermost 내보내기 모드, 뷰어·검색 내장. **마크다운 직접 출력은 미확인** — JSON을 스레드 단위 마크다운으로 바꾸는 변환 스크립트 필요 `[W36]`(웹, README 요약 수준). 토스 Topic의 "스레드 단위 요약 + 결정/미결 구분" 원칙과 결합 `[W37]`.
- **PDF/Office → Markdown**: Docling(IBM)은 레이아웃·표가 복잡한 문서에 강하지만 무겁고 GPU 없으면 느림. MarkItDown(Microsoft)은 가볍고 빠르지만 헤딩 구조·표가 깨지고 스캔 PDF는 빈 문자열(OCR 플러그인 미사용 시). Marker(선택적 LLM 패스), PyMuPDF4LLM도 후보. 결론: 자기 문서 샘플로 직접 돌려 보고 결정. **벤더/블로그 비교 — 수치 인용 금지** `[W35]`(웹, 신뢰성 중~하). llmwiki는 선택적 LibreOffice·Mistral OCR `[W8]`.
- **Confluence/Jira**: 우아한형제들 — Atlassian MCP 실시간 조회 + 벡터 스토어 fallback; 소스 선별 기준 "Wiki 공간별 문서 생성 수와 최근 2주 조회수를 기준으로 핵심 문서만 자동으로 선별해 수집했습니다." `[W39]`.
- **웹 클리핑**: Obsidian Web Clipper 저장 위치를 `raw`로 `[W10]` `[W3]`. Chrome 확장(llmwiki) + 야간 Claude Routine이 캡처물을 위키로 합성 `[W8]`.
- **한국어 파일명 함정**: GPTers — "파일명에 특수문자가 섞여있으면 가끔 인코딩 이슈가 있습니다" `[W7]`. @vellumkasane 린트는 ASCII 파일명 검사 포함 `[C]`.
- 미수집: Google Docs → 마크다운 공식 경로(Drive API export MIME `text/markdown` 지원 여부 미확인) `[W 수집 한계]`.

---

## 8. 운영: lint · 승격 · 신선도 · 보안 격리 · 스케줄

### 8.1 가장 많이 반복된 고통 — 조용한 부패(silent rot)
- Abby_101(HN, 2026-04-25): "Six months in, you have entries that are confidently wrong and the lint pass can't tell which." johntash — 예전 시도가 "looked good until you read the actual data". ryanshrott — 틀린 항목을 다른 에이전트가 인용하면서 "a knowledge base full of confident BS". Jwcjwc12(gist, 2026-04-05): "the moment those files change, the compiled knowledge might be wrong — and doesn't know it." laphilosophia(2026-04-04): LLM은 "fail quietly"; "the real product problem is not organization, it is epistemic integrity." XBlueSky(2026-09-22): "A transcript-filter payload drift silently produced unusable records for two weeks before I noticed it." Fontoura(2026-10-06): "A wiki maintained by an LLM never looks neglected. It stays fluent, linked, and current-sounding while the content drifts." Glukhov: "An LLM Wiki fails when old facts remain plausible" / "A page without a review date is a page that will eventually lie quietly." clue.oz4e(2026-08-21): "노트가 바뀌었을 때 위키가 조용히 낡는데, 그걸 알려주는 신호가 없다는 게 제가 겪은 가장 큰 위험이었습니다." Taktile(2026-07-13): "Keeping a compiled knowledge layer trustworthy when its underlying sources drift silently turned out to be the hard part." `[C]`
- 커뮤니티 공유 진단: 원본이 바뀌어도 컴파일된 페이지에 신호가 없다 / 구조 린트(깨진 링크·고아)는 잡지만 의미 린트(낡은 주장·모순)는 못 잡는다 / 린트조차 LLM이 하면 자기 채점이 된다 `[C]`.
- 요약의 요약(패턴 2): asong56 — AI 환각이 사실로 영구히 박힌다. velog a-a-k 요지: "원본 문서를 LLM이 위키 페이지로 재작성할 때 단서, 날짜, 소수 견해, 엣지 케이스, 정확한 표현이 소실될 수 있다." / "위키가 커질수록 요약 오류가 진실처럼 굳어진다." AI매터스 김탄휴(2026-05-21): "한 페이지의 작은 오해가 연결된 여러 페이지로 조용히 전파된다." / "마크다운 무덤이 되거나, 잘못된 정보가 우아하게 정리된 거짓 위키가 되거나" `[C]`.
- 정량 근거(위키 오류 = 답변 오류): ClashEval(Wu·Wu·Zou 2024, arXiv 2404.10198, NeurIPS 2024 S2 표기·트랙 미확인) — 모델들은 "are susceptible to adopting incorrect retrieved content, overriding their own correct prior knowledge." `[P3-3]`. Chameleon/Sloth(Xie 외 2023, arXiv 2305.13300, ICLR 2024 Spotlight 확인) — "LLMs can be highly receptive to external evidence even when that conflicts with their parametric memory, given that the external evidence is coherent and convincing." / "LLMs also demonstrate a strong confirmation bias when the external evidence contains some information that is consistent with their parametric memory". PopQA에서 기억 일치 증거 비율 0/2 → 2/2일 때 ChatGPT 기억 채택률 3.7% → 99.8%; 무관한 단락 1개만 주면 Llama2-7B는 92.4%가 그 내용으로 답변 → 모순된 두 페이지가 공존하면 모델은 사전 지식에 가까운 쪽을 고른다; lint로 모순을 남기지 말 것 `[P3-2]`. RAGTruth(Niu 외 2023, arXiv 2401.00396) — 검색을 줘도 환각 응답 비율 GPT-4 13.7%(계산값, Table 3 ÷ 2,965); "Despite the integration of RAG, LLMs may still present unsupported or contradictory claims to the retrieved contents." `[P4-6]`.

### 8.2 lint는 두 층 — 구조는 스크립트, 의미만 모델
- Fontoura: 구조 린트(깨진 링크, 고아)는 모델 토큰 없이 스크립트로, 모델은 모순·낡은 주장 같은 판단에만 `[C]`. llmwiki `lint`는 결정론적 검사(인용 해상·dangling link·orphan·stale·frontmatter) `[W8]`. podcast-wiki `tools/lint_wiki.py`(기계적 검사만) + `/lint-wiki`(깨진 링크·orphan·drift 수정) + `/dream`(중복 개념 병합) `[W11]`.
- @vellumkasane 150줄 린트 스크립트: 프런트매터, index.md에서 도달 가능성, `[[link]]` 해소, ASCII 파일명, stale 페이지. CI에서 nonzero exit, 세션 종료 전 실행 `[C]`.
- Glukhov 체크리스트 — (구조) 깨진 내부 링크, 고아, 중복 제목, 소스 섹션 누락, 검토일 누락, 백링크 없는 페이지, 빈 섹션, 구조 없는 긴 페이지, 인덱스 미연결, 명명 불일치, 잘못된 프런트매터, 검토 기한 초과. (의미) 출처 없는 주장, 상충 주장, 낡은 결정의 현재형 서술, 이름만 다른 중복 개념, 여러 의미가 섞인 개념 페이지, 제약 생략 요약, 기준 없는 "best", 버전 없는 버전 주장, 최신 소스와 모순 `[C]`.
- 범용 도구의 한계: markdownlint(스타일)·lychee(외부 URL; lychee-action 2.0.2 이전 코드 인젝션 취약점 패치됨)는 `[[wikilink]]`·frontmatter를 모른다. 위키 전용 검사는 sidequery/mdlint(Rust, backlink·wikilink·heading anchor·image 검증)나 claude-obsidian `wiki-lint` 스킬 또는 자체 스크립트 `[W33]`(웹, 검색 요약 수준).
- 실측: Jim Liu — 주간 수동 린트 약 20분(일요일 아침), 격주 서브에이전트 모순 탐지 < $0.40, 주간 외부 링크 스크립트가 6개월간 약 24개 깨진 링크. Fulkerson 첫 린트 "23 orphaned files and 11 broken cross-references." GPTers lint 결과 예: "sources 경로 오류 4개 자동 수정" / "미처리 raw 파일 1개 발견" / "개념 페이지 stub 6개 제안" `[W7]` `[C]`.
- 모순 검사의 복잡도: Covenant0028 — N개 파일 간 모순 검사는 N*N. ChrisGreenHeur — 무작위 샘플링을 시간에 걸쳐 돌리면 대부분 드러난다 `[C]`. alfabarisl18-ops(2026-10-05): 구조 검사는 모순·낡은 주장·사실 오류를 못 잡는다 — 여전히 사람 검토 필요 `[C]`.
- 중복 탐지 기법: Dedup(Lee 외 2021, arXiv 2107.06499, ACL 2022 확인) — exact substring, NearDup/MinHash; "removing from C4 a single 61 word English sentence that is repeated over 60,000 times." (학습 데이터 맥락 — 검색 코퍼스 dedup 효과를 직접 측정한 논문은 아님, 과잉 일반화 주의) `[P3-11]`. SemDeDup(Abbas 외 2023, arXiv 2303.09540) — "SemDeDup can remove 50% of the data with minimal performance loss, effectively halving training time." → 임베딩 클러스터링으로 후보를 찾고 LLM이 병합 판단 `[P3-12]`.
- 페이지 사실 정밀도 측정 모델: FActScore(Min 외 2023, arXiv 2305.14251, EMNLP 2023 확인) — 긴 생성문을 원자 사실로 쪼개 지지 비율 계산; "ChatGPT only achieves 58%"(인물 전기); 자동 추정기 "less than a 2% error rate." `[P4-5]`.
- lint 모순 발견 시 처리 — "뭉개지 말 것"(패턴 4): Jim Liu — "Contradictions are assets, not errors." Glukhov — "Do not let the agent silently resolve contradictions by blending both claims into a vague compromise." Fontoura 계약 조항 — "Record contradictions and divergences. Never smooth them into one story." HagaiHen — "Never silently overwrite." 상충 견해는 출처와 함께 나란히. Ghelbur — 모순을 플래그만 하고 수동 해소 → 수백 페이지 넘자 "accumulated faster than they could be fixed", 답변이 헤지됨 `[C]`. lucasastorian 이슈 #93 — 신규 인제스트 직후 lint의 stale-page 검사가 모든 페이지를 낡았다고 플래그 `[C]`.

### 8.3 신선도: 검토 주기·소스 해시
- Glukhov 검토 주기 표: 도구 버전 페이지 30–90일, 가격·가용성 7–30일, 비교 페이지 30–180일, 용어집 3–12개월, 아키텍처 원칙 6–18개월, 소스 요약은 소스 변경 시, 과거 결정은 대체될 때만. `review_after` = `last_reviewed` + 3개월 `[C]`.
- 소스 해시(H8): Taktile 계획 — 연결 소스의 타임스탬프/콘텐츠 해시 저장, 바뀌었을 때만 재검증. "If it hasn't changed, we _know_ nothing about the source moved, so we can trust the compiled wiki fact." 현재 상태(해시 전): "we're still paying to fetch the source on every answer." Jwcjwc12 — 명제별 콘텐츠 해시. viberesearch — 인제스트마다 SHA-256 `[C]`.
- Fulkerson LOG.md — "every significant vault mutation with a timestamp"; 90일 이상 낡은 항목 추적 `[C]`.

### 8.4 승격(promotion) 게이트와 사람의 자리
- 캡처와 승격 분리(H9): ryanshrott — 다중 에이전트 수렴을 신호로. drewbatcheller — 자유롭게 초안, 승인 시 승격. saadn92 — 6개월째 트랜스크립트에서 결정·기각된 접근을 추출하는 백그라운드 프로세스 + 승격 전 사람 리뷰. Fontoura — 근거·재사용·실제 결정을 얻은 뒤에만 정전(canonical) 층에 승격, "a ripe page next month" > "a canonical page that is really a first impression." `[C]`
- Glukhov 리뷰 위험 등급: 낮음(링크·포맷·오타·별칭) / 중간(소스 요약, 새 개념, 병합, 상태 변경) / 높음(주장 삭제, 정전 페이지 재작성, 결정 변경, 보안·법·가격·벤치마크, 모순 해소) — 높음은 사람 검토 `[C]`.
- anuramat — cron이 쉬운 수정은 PR로; 미검토 코드는 `// SLOP` 표시. @techwithhari — "PRs always target `dev` branch. Never auto-merge. Human review required." Ghelbur — 에이전트 변경은 24시간 뒤 영구화("everything reversibly") `[C]`.
- 반대 극단 Stigmergy: "Nobody approves a queue" / "No write waits for a human." 대신 단일 직렬 writer + 변경 기록 + 가시성(ACL) `[C]`.
- 유지보수가 사람을 잡아먹는다(패턴 7): simsla — "Everyone is writing. Nobody is reading." mplappert — "a serious issue with people using AI to do an immense amount of busywork and then never look at it again." saberience — "it's more fun to build than to actually use." Theo James(2026-04-21): "The system didn't fail because the model was bad. It failed because I couldn't maintain the inputs." / "Maintenance is where good systems go to die." / "Missing 5 percent is fine. Missing three weeks is not." Ask HN "Do you use LLM-Wikis?"(2026-07-17) — "haven't gotten much value from it", 댓글 0. Fulkerson — "That's how every wiki I've ever built eventually died — under the weight of its own bookkeeping." `[C]`

### 8.5 보안 격리·권한
- podcast-wiki: **신뢰할 수 없는 트랜스크립트를 읽는 headless Claude는 `wiki/` 안에만 쓰고 git 명령을 못 돌리게** 하고, 커밋·푸시는 스크립트가 한다(launchd로 6시간마다 `tools/scheduled_ingest.sh`) `[W11]`.
- 에이전트가 하면 안 되는 일(패턴 8): @vellumkasane — 에이전트가 raw/ 안 CSV의 "오타를 고쳐" 버림; "The wiki repo sat dirty until someone noticed."; "Every 'helpful' session added a page nobody linked to." Jim Liu — Claude가 originals/의 원문 어투를 매끈하게 고쳐 버림 → do-not-rewrite 태그. llmwiki 이슈 #93(2026-09-19) — 삭제가 사용자 원본 파일까지 디스크에서 지움(README의 "never modify your files" 약속과 모순) `[C]`.
- Memory tool 경로 탐색 검증 `[W20]`; Files API `file_id`를 신뢰할 수 없는 출처에서 받지 말 것 `[W19]`; Agent SDK 인증: "Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Use the API key authentication methods" `[W26]`.
- 검증기는 모델 없는 코드(H13): Stigmergy — "The answer verifier is pure code." 못 답하면 "an honest refusal." (README 자체 평가 Recall@5 1.00, 정직성 1.00, 근거성 1.00 — 15문항, 자기 보고) `[C]`. sovahc — 캐시 포이즈닝 위험, 모든 단계 검증 `[C]`. Fontoura — 외부 인용 전 URL fetch 필수 `[C]`.

### 8.6 스케줄 실행·세션 운영
- `claude -p "your prompt"` / `--output-format json` / `--output-format stream-json --verbose`; 팬아웃 예 `claude -p "Migrate $file ..." --allowedTools "Edit,Bash(git commit *)" --permission-mode dontAsk` `[W25]` → 야간 lint를 CI에.
- podcast-wiki launchd 6시간 주기 `[W11]`; HagaiHen "running unattended every few hours" `[W2]`; llmwiki 야간 Claude Routine `[W8]`; Taktile 주간 린트 잡 `[C]`; Ghelbur 예약 에이전트 4개 `[C]`.
- 짧게 자주(H14): dataviz1000 — "Don't let them run long enough to trip." / "It is better to let them run twice for 5 minutes than once for 10 minutes." asakin — 30일 "훈련 기간" 후 AI가 점점 조용해짐 `[C]`.
- log.md 실무(H6): Jim Liu — 작업당 타임스탬프 한 줄, 주 2회 grep. 주의 aakarim — log.md가 "seems to only confuse less intelligent models". otomatty/zedi PR #604 — 활동 로그 쓰기는 throw 대신 로그 에러로 `[C]`.
- 비결정성: daydreamblend — "LLM이 관리를 하면 RAG보다는 비결정론적이기에 모델마다 성능이 크게 달라질 거 같은데" `[W5]`; Medium "메모 인제스트를 이틀 뒤 재실행하니 다른 결과"(2차 인용) → alfadur: 초안을 그대로 믿지 않고 반복 검증 사다리 `[C]`.

---

## 9. 평가 — 골든셋·회귀·인용 품질

- Anthropic evals 글(2026-01-09): "An **evaluation** ('eval') is a test for an AI system" / Task "is a single test with defined inputs and success criteria." / "Each attempt at a task is a **trial**." / "A **grader** is logic that scores some aspect of the agent's performance." / "**Capability or 'quality' evals** ask, 'What can this agent do well?'" / "**Regression evals** ask, 'Does the agent still handle all the tasks it used to?'" / pass@k "measures the likelihood that an agent gets at least one correct solution in _k_ attempts." / pass^k "measures the probability that _all k_ trials succeed." / "Agent evaluations typically combine three types of graders: code-based, model-based, and human." / "20-50 simple tasks drawn from real failures is a great start." / "**Eval saturation** occurs when an agent passes all of the solvable tasks" `[W22]`(공식).
- RAGAS(Es 외 2023, arXiv 2309.15217, EACL 2024 S2 표기): context relevance / faithfulness / answer relevance — "a suite of metrics which can be used to evaluate these different dimensions without having to rely on ground truth human annotations" `[P4-1]`. ARES(Saad-Falcon 외 2023, arXiv 2311.09476, NAACL 2024 확인): "ARES accurately evaluates RAG systems while using only a few hundred human annotations during evaluation." → 골든셋 예산 기준점 `[P4-2]`.
- 인용 품질: ALCE(Gao 외 2023, arXiv 2305.14627, EMNLP 2023 확인) — "on the ELI5 dataset, even the best models lack complete citation support 50% of the time." citation recall/precision 정의 `[P4-3]`. Verifiability(Liu·Zhang·Liang 2023, arXiv 2304.09848, Findings of EMNLP 2023 확인) — "on average, a mere 51.5% of generated sentences are fully supported by citations and only 74.5% of citations support their associated sentence." / "especially given their facade of trustworthiness." **2023년 초 상용 시스템 기준 — 최신 상태로 일반화 금지** `[P4-4]`.
- "모르면 거부"와 "지식 갱신"을 평가 축에 넣은 유일한 표준 벤치마크: LongMemEval(Wu 외 2024, arXiv 2410.10813, ICLR 2025 확인) — 5능력(정보 추출·다세션 추론·시간 추론·지식 갱신·거부). "commercial chat assistants and long-context LLMs showing a 30% accuracy drop on memorizing information across sustained interactions" / "Instead of sessions, round is the more optimal granularity for storing and utilizing the interactive history." 사실 보강 키 확장 recall@k +9.4%, 정확도 +5.4% `[P4-7]`. 커뮤니티의 "없는 답 환각"(clue.oz4e: "답이 없는 질문 10개를 던지면 10개 전부 아무 노트나 근거로 물고 나왔고") `[C]`이 거부 평가 항목의 동기.
- 환각 탐지기: RAGTruth — 미세조정 Llama-2-13B 탐지기 응답 수준 F1 78.7% vs 프롬프트 GPT-4-turbo 63.4%; "a fine-tuned Llama-2-13B can achieve the best performance with an average 78.7% f1 score." → 작은 전용 탐지기가 대형 범용 프롬프트보다 `[P4-6]`.
- 국내 사례: 우아한형제들 — Langfuse 추적 + "LLM 기반 자동 평가(G-Eval)를 도입했습니다." `[W39]`. 토스 Topic — 평가 수치 없음(본문 "0.87", "세 번/두 번"은 예시값) `[W37]`.
- 커뮤니티 자기 평가(검증 필요): @techwithhari 정확도 3/10 → 7/10; Stigmergy 1.00; Taktile 벤치 `[C]`.

---

## 10. Agent SDK vs 직접 API vs Managed Agents

- 공식 비교표: Agent SDK = "A library that runs the Claude Code binary, with Claude Code's capabilities, such as built-in tools, permissions, sessions, and hooks." / Client SDK = "You write the tool loop yourself, or let the client SDK's beta tool runner drive it." / Managed Agents = "A hosted agent harness that runs the agent loop, with sessions in an Anthropic-managed cloud sandbox". "The Agent SDK gives you the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript." 기능표: Built-in tools "Read, write, edit files, run commands, and search the web" / Hooks / Subagents / MCP / Sessions "Maintain context across exchanges, resume or fork later" / Skills, commands, and memory "Load automatically from your project's `.claude/` and from `~/.claude/`, same as Claude Code" `[W26]`(공식).
- 패키지 버전(1차 확인, 2026-10-11): PyPI `claude-agent-sdk` 0.2.165(2026-10-08, Python ≥3.10, `pip install claude-agent-sdk`); npm `@anthropic-ai/claude-agent-sdk` 0.3.296(2026-10-09, Node ≥18). **책에는 "2026년 10월 기준 0.2.x / 0.3.x"로 쓰는 것이 안전** `[W26]` `[W 교차검증 메모]`.
- 선택 기준(리서치 종합): 파일시스템 위키 + grep/MCP + 훅으로 raw/ 보호 → Agent SDK가 Claude Code와 동일 동작(스킬·CLAUDE.md 자동 로드). 위키를 문서 블록으로 넘겨 API 수준 인용(Citations)·캐싱·Memory tool을 직접 제어 → 직접 API. 둘 다 API 키 인증(claude.ai 로그인 재판매 금지) `[W26]`.
- GPTers: "클로드 코드 CLI 환경이 필요합니다 (웹 클로드로는 어려움)" `[W7]`.

---

## 11. 대표 사례 (구현 보고 — 전부 자기 보고, 통제군 없음)

| 보고자 / 출처 | 규모·스택 | 깨진 것 | 숫자 | 출처 |
|---|---|---|---|---|
| **Taktile** (회사, 2026-07-13) https://engineering.taktile.com/blog/llm-wiki-agent-memory/ | 사내 질문 답변 에이전트, 마크다운+프런트매터를 전용 브랜치에, 질문 범주별 서브위키, 주간 린트 잡 | 소스가 조용히 바뀜 → 매 답변 소스 재검증(비용 그대로), grep 부적합, LLM이 쓴 인덱스/프런트매터의 오류 복합 | 88항목·24쿼리 벤치: BM25 0.47ms vs LLM 판단 69.1s; 실행당 라이브 조회 9m40s·$2.50 → 위키 답변 1m19s·$0.98 (86% 빠르고 61% 저렴) | `[C]` |
| **Casey Newton / Platformer** (언론, 2026-08-18) | Obsidian + Claude(Claudian), 아카이브 시드 + 일일 클리핑 | 상시 유지보수, 긴 페이지 압축, 코드 오류로 프로세스 중단, Claude 문체 → GPT로 AP 스타일 재작성 | 약 1개월 만에 1,440+ 페이지; Meta 페이지 12,000+ 단어·내부 링크 1,300+ | `[W3]` `[C]` |
| **Jim Liu** (개인, 6개월, 2026-05-06) https://www.openaitoolshub.org/en/blog/karpathy-llm-wiki | Obsidian + Claude Pro, schema.md 중심 | 린트 건너뛰자 3개월 차에 고아·미표시 모순; 원문 어투 훼손; 모순 덮어쓰기; 도구 이전 중 aliases 필드 유실로 중복 인물 페이지 | 하루 ~15분 유지, 주간 린트 20분, 격주 모순 패스 <$0.40, 인제스트당 9파일(4–23), 35페이지·grep 40–50ms | `[C]` |
| **Eugeniu Ghelbur** (마케팅 에이전시 AI 엔지니어, 6개월, 2026-04-29) https://theaioperator.io/p/i-rebuilt-karpathys-llm-wiki-heres | Claude Code 슬래시 커맨드 31개 + 예약 에이전트 4개 | 50–100 소스에서 1차 붕괴, 수백 페이지에서 모순 폭증, 첫 /research-deep이 하드코딩 1만 단어 보고서·`<think>` 태그 그대로 저장·프런트매터가 파이썬 dict 문자열 | /x-read ~$0.05, /research-deep $0.40–0.80, 변경 24시간 유예 | `[C]` |
| **@vellumkasane** (Dev.to, 2026-09-22; 프로덕션 CRM/회계 앱 옆에서 4곳 운영) https://dev.to/vellumkasane/four-things-that-broke-when-i-ran-karpathys-llm-wiki-with-claude-code-and-the-fixes-4h4f | Claude Code + 훅 + 150줄 린트 | raw/ 수정, 미커밋, 고아 페이지, 과잉 질문 | 2주 안에 4건 발생 | `[C]` |
| **@techwithhari** (Dev.to, 2026-05-10) SEO/마케팅 KB | Cognee(Neo4j+Chroma) → 마크다운 9페이지 위키 + AGENTS.md, 결정적 스킬 함수가 코드 수정, LLM은 분류만 | 이전 파이프라인이 3회+ 고장 — "spent more time fixing the pipeline than reading its output" | 비용 $35/월 → ~$0(토큰 제외); 자기 평가 정확도 3/10 → 7/10; 1주 병렬 운영 | `[C]` |
| **vbarsoum** (HN 원 스레드) | 책 3권, 68파일, ~155K 단어 | 책 단위 파일 = slop | 210 개념 페이지, 4,597 교차참조, 173K 단어 출력, ~12M 토큰, 10–15분 | `[C]` |
| **psanchez** (HN WUPHF 스레드) 회사 KB | git 기반, Claude Opus 4.6, 티케팅·위키·GitHub·Jenkins 연결 | — | "a few hours"에 구축; "Agents without structure produce slop, but with a well-curated knowledge base and iteration, they can be useful." | `[C]` |
| **glaucobrito** (gist, 2026-04-09) | 관측 기반 메모리, wip.md, 30일 자동 가지치기 | — | 33일, 1,493 관측, 부팅 ~8K 토큰, $0 | `[C]` |
| **HagaiHen** (gist, 2026-10-08) 팟캐스트 위키 https://github.com/HagaiHen/podcast-wiki | CLAUDE.md 절차, 몇 시간마다 무인, launchd, 권한 격리 | near-duplicate 페이지가 기본 실패 | 60회 → 69 개념 페이지; 커밋 124 | `[W2]` `[W11]` `[C]` |
| **orcosto-lab** (gist, 2026-09-21) | 세션 감사 | 위키를 작업 중에 안 읽음 | 9세션 중 2세션이 이미 기록된 교훈을 재진단 | `[C]` |
| **kaimys** (gist, 2026-09-21) | 모바일 앱 개발 + 회의록·ADR | — | "it worked great" | `[C]` |
| **alfadur** (GeekNews, 2026-06~08) 뉴스 스크랩 KB | Claude Code 기반 지식 팩토리, 멀티에이전트 → "신문 편집국" | 자율 멀티에이전트가 토큰 5–10배·컨텍스트 유실; 위키 비대 → writer/judge 분리 | 비공개 저장소에서 수천 기사 운영 | `[C]` |
| **clue.oz4e** (PyTorchKR, 수개월) | 자체 구현 → 위키=지도 + 하이브리드 RAG | 페이지 누락, 없는 답 환각, 조용한 노후화 | recall@5 93% | `[C]` |
| **카일라스** (클리앙, 2026-04-26, 조회 15,497) | JSON 메모 500+, NotebookLM과 비교 | 느림 | 등록 20분+, 답변 품질 "대부분 유사" | `[W6]` `[C]` |
| **Theo James** (Medium, 2026-04-21) | 개인 | 2주 뒤 사용 감소, 3주 공백 뒤 "ingestion debt" | — | `[C]` |
| **비케이** (GPTers, 2026-05-27) | Claude Code CLI, CLAUDE.md 명령어 체계 | 한국어 파일명 인코딩, 수백 페이지 컨텍스트 | lint: 경로 오류 4개 자동 수정·미처리 raw 1개·stub 6개 제안 | `[W7]` |
| **lucasastorian/llmwiki** 이슈 | 호스팅 + MCP | #93 삭제가 원본 삭제, lint가 전 페이지 stale; #47 워처가 .md를 청킹 안 해 370파일이 검색 불가; #52 인용이 페이지 수준인지 주장 수준인지 미정의 | https://github.com/lucasastorian/llmwiki/issues | `[W8]` `[C]` |

### 11.1 국내 기업 사례 (LLM Wiki 패턴 그 자체는 아니나 사내 지식 에이전트의 참조점)
- **토스 — Topic 컨텍스트 레이어**(김병균, 2026-07-30): "LLM은 똑똑한데, 왜 우리 회사 일은 모를까" — "이런 질문에는 모델의 추론 능력만으로 답할 수 없어요." / "찾은 문서가 최신인지, 사내 메신저에서의 논의가 최종 결정인지, 문서의 설명과 실제 코드가 일치하는지는 검색만으로 판단하기 어려웠어요." 답변 재료와 함께 신뢰 상태를 반환. 평가 수치 없음 `[W37]`.
- **토스페이먼츠 — 하네스**(김용성, 2026-02-26): 문서=실행 지시, 3계층(Global/Domain/Local), "잘 관리된 플러그인(프롬프트+코드)들의 집합이 곧 우리 조직의 기술 자산이 되는 셈입니다." 가설·방향성임을 명시 `[W38]`.
- **우아한형제들 — 물어보새 3부**(BADA팀, 2025-10-15): ReAct 전환, 사용량 기반 문서 선별, 메타데이터, Atlassian MCP + 벡터 fallback, Langfuse·G-Eval, BM25s 약 15%↑. "중요한 것은 기술이 아니라 사용자의 문제를 해결하는 일이며, 기술은 문제 해결 과정에서 자연스럽게 발전한다는 점". **"BM25s 최대 500배 빠름", "임직원 4명 중 1명 사용"은 요약 수치 — 원문 대조 (사실 확인 필요)** `[W39]`.
- **LY Corporation — 엔터프라이즈 LLM 서비스 구축기 1**(한우형, 발행일 미표시 — 사실 확인 필요): 일반 RAG 챗봇 예 "서버 접속이 안 되면 네트워크 상태나 VPC ACL을 확인해 보세요" → 일반론적인 가이드; 질문별 도구 선별 `[W40]`. **ODW #5**(giginet, 발행일 미표시): ChromaDB + MCP + Skill `[W41]`.
- **Samsung Tech Blog — DeepDive**(송하연, 2026-01-29): "DeepDive는 삼성리서치에서 개발 중인 사내 AI 서비스로, 검색 증강 생성(RAG, Retrieval-Augmented Generation) 기술을 활용해 방대한 사내 문서의 정보 탐색과 보고서 작성을 자동화합니다." 본문 대부분 접근 실패(Cloudflare 520) — 도입부만. "Agentic Search 시스템 구축기"(2026-02) URL 미확보 `[W42]`.
- **당근**(AI월드 2026 보도): 판단의 이유와 근거를 남겨야 한다 `[C]`.
- **국내 사내 도입 후기 부재**: GeekNews alfadur(뉴스 스크랩 팩토리)와 kurthong 외에 사실상 없음 — 책에서 "국내 사내 사례 부재"를 명시할 것 `[C 수집 한계]`.

---

## 12. 논쟁점·상충 관점

### 논쟁 A: 벡터 RAG vs 에이전틱 grep/파일 탐색 vs LLM 위키
- 관점 1 "이건 그냥 RAG다": HN kenforthewin — "This is just RAG." devmor — "persistent memory RAG." mememememememo — "compaction for RAG." panarky — "nothing about RAG that requires embeddings." (grep도 RAG다) `[C]`.
- 관점 2 "쓰기 루프가 다르다": darkhanakh — "in vanilla RAG your corpus is static, here it isnt." LLM이 코퍼스를 유지보수하고 린트를 돈다는 점이 본질. Dev.to dishant0406 — RAG는 매 쿼리 합성을 처음부터 다시 하고 교차참조가 누적되지 않는다 `[C]`. Karpathy 원문 "There's no accumulation." `[W1]`.
- 관점 3 "상호보완": visakadev — mempalace는 RAG, 위키는 컴파일된 지식. Taktile·clue.oz4e — 위키는 지도/캐시, 내용 검색은 BM25/하이브리드 `[C]`.
- 데이터: xguru — Farzapedia(약 2,500 항목 → 400페이지)에서 기존 RAG는 성능이 나빴고 에이전트가 파일을 직접 탐색하니 훨씬 나았다 `[C]`. Retrieval as Reasoning(2.2절, 2차). PwC Is Grep All You Need(6.2절, 2차). VentureBeat 헤드라인("bypasses RAG")이 양자택일 프레임을 키웠다는 지적(https://atlan.com/know/llm-wiki-vs-rag-knowledge-base/ 등) `[C]`.

### 논쟁 B: 위키(컴파일) vs 원문(raw) 그대로
- 원문파: jdthedisciple — 팩트체크할 시간이 없는 LLM 위키보다 원본을 직접. Marekai — 인용 정확도가 깨진다. a-a-k — 손실 압축 `[C]`.
- 컴파일파: Karpathy "compile once, keep current" `[W1]`; dishant0406 `[C]`.
- 절충: 위키는 "지도", 답의 근거 문장은 원문에서(H13). Fontoura — 요약이 아닌 "메커니즘"을 추출하고, AI 요약 대신 전체 트랜스크립트를 요구 `[C]`. Newton — 쓰기 전 원본을 열어 "to make sure nothing I was about to say was hallucinated." `[C]`

### 논쟁 C: 마크다운 vs 데이터베이스
- 4.1절. 마크다운파(dhruv3006·left-struck·OKF·Stigmergy "never a second wiki") vs DB파(mpazik Binder, bradwmorris SQLite, buremba PostgreSQL 엔티티 + 이벤트 로그, YIING99 pgvector). 절충 신호: 수백 페이지·다중 writer·연속 write-back `[C]`. HN 10x 스레드 xnx·eikenberry — 텍스트 파일 + 가벼운 규약이면 충분(https://news.ycombinator.com/item?id=48586811, OKF https://news.ycombinator.com/item?id=48620068) `[C]`.

### 논쟁 D: Obsidian vs 커스텀
- 4.3절. jurajskuska — "OBSIDIAN COULD BE A STANDARD for all." davedigerati — "why not an Obsidian vault with a plugin?" vs najmuzzaman·rothnic `[C]`.

### 논쟁 E: 전체 리빌드 vs 증분
- 증분파(다수): Karpathy "surgically update only affected pages"(community.md 인용) `[C]`; ethanj — 바뀐 소스만 모델에; wumborti — 최근은 원문 창, 과거는 롤링 다이제스트, 델타만; Jim Liu — 인제스트당 중앙값 9파일; LightRAG 증분 알고리즘 `[P1-9]`; TemporalWiki diff 학습 1/12 비용 `[P3-9]`.
- 리빌드/계산파: Stigmergy — "a nightly full rebuild guarantees convergence"(인덱스). jermolene — 인덱스는 계산. Jwcjwc12 — "compile-at-query-time with validation on every read" 제안 `[C]`. GraphRAG 인덱싱 281분은 전체 리빌드 비용의 참고치 `[P1-8]`.
- 증분의 위험: 비결정성(8.6절).

### 논쟁 F: human-in-the-loop vs 자율
- 자율파: Stigmergy — "No write waits for a human."; HagaiHen — 몇 시간마다 무인; Ghelbur — 자동 반영 + 24시간 되돌리기 창 `[C]`. Karpathy — "Possibly with humans in the loop reviewing updates." (팀 위키 설명) / "batch-ingest many sources at once with less supervision" 가능 `[W1]`.
- HITL파: SOLAR_FIELDS — 완전 자율 자기참조 층은 "completely valueless", 가치는 "a system that supports a human coming in." stingraycharles — 완전 LLM 유지 마크다운은 품질이 떨어진다는 연구 인용(criley2는 근거 범위에 이의). bluewater8008 — "The LLM is the writer. You're the editor-in-chief." jurajskuska — 신뢰가 병목이라 사람 감사 체크포인트. Glukhov — 높은 위험 변경만 사람 `[C]`. Karpathy 본인은 "ingest sources one at a time and stay involved" 선호 `[W1]`.
- 중간: 캡처 자율 + 승격 승인(H9). alfadur — writer와 judge 분리 `[C]`.

### 논쟁 G(소스 간 상충 — 합성에서 발견)
- **gist 날짜**: 04-02(트윗·2차 자료) vs 04-04(gist 메타) → "2026년 4월 초"(1.1절).
- **Karpathy 트윗 문구**: "Something I'm finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest." 는 Platformer 인용 `[W3]` 외 1차 확인 못 함(x.com 직접 fetch 402/451). community.md는 포스트 ID·메타데이터와 요지만 확보 `[C]`. GeekNews 요약 "코드보다 개인 지식 저장소 구축에 토큰을 더 많이 쓰고 있다며" `[W4]`는 요지 일치.
- **index.md 규모 한계**: gist "~100 sources, ~hundreds of pages" vs 커뮤니티 "~100 pages"·"100-200 pages" vs 클리앙 500+ 메모 문제없음 → 서로 모순되지 않는 "경험치"(6.2절). 책에서는 gist 수치만 1차로, 나머지는 자기 보고로.
- **"Retrieval as Reasoning" 수치**: web.md(GN 요약)에만 존재, papers.md에 항목 없음 → 논문 원문 대조 전까지 (사실 확인 필요).
- **PwC grep 논문**: web.md 2차 해설만, papers.md 항목 없음, 해설 자체가 표 불일치(76.7% vs 94.0%)를 지적.
- **arXiv 2602.11988(자동 생성 AGENTS.md)**: community.md의 HN 댓글 인용만 → (사실 확인 필요).
- **Search-R1 상대 개선**: 41% vs 24%(버전 간) → 범위로.
- **A-MEM 토큰 절감**: 본문 vs 표 불일치 → "최대 약 93%".
- **Context Rot 보고서**: arXiv ID 없음(검색 시 미노출) — 트라이크로마 URL로만 인용.
- **"200K 토큰이면 통째로"**(Anthropic 2024) vs context rot(Anthropic 2025·2026·Chroma): 시점과 모델 세대가 다르다. 책에서는 "작으면 통째로 + 캐싱, 그래도 context rot 존재"로 병기하고 2024 수치는 "2024년 기준"으로 못 박을 것.
- **벤더 자체 평가**(Mem0·Zep·Chroma·Stigmergy·Taktile 등)는 그 사실을 본문에 밝힐 것.

---

## 13. 실무 적용 팁 (휴리스틱 통합 — 커뮤니티 H1~H15 + 논문·공식 근거)

| # | 팁 | 근거 |
|---|---|---|
| T1 | raw/는 불변 — 지시문이 아니라 PreToolUse 훅으로 강제. Stop 훅으로 미커밋 상태 차단 | `[C]` H1, `[W24]` `[W25]` `[W29]` |
| T2 | 스키마(CLAUDE.md)가 가장 중요한 파일. 200줄 이하, 모순 제거, "You" 대신 "User/Assistant", 절차는 스킬·path-scoped rule로 | `[C]` H2, `[W24]` `[W25]` `[W23]` |
| T3 | 모든 페이지 상단 TL;DR + 토큰 예산 계층(L0~L3). 세션 핫 캐시 500토큰 이하 | `[C]` H3, `[W15]` 맥락 문장 |
| T4 | 프런트매터에 출처 유형(human/LLM/reviewed)·confidence·last_verified·review_after·superseded_by·contradicts·valid_from/to | `[C]` H4, `[W37]`, `[P1-6]`, `[P3-8]` |
| T5 | 인덱스는 손으로 유지하지 말고 계산(스크립트)하거나 검색 색인에서 제외. ~100 소스 넘으면 BM25 | `[C]` H5·H12, `[W1]` `[W12]` |
| T6 | log.md는 작업당 한 줄 append-only, 일관 prefix로 grep 가능하게. 로그 실패가 본작업을 깨지 않게 | `[W1]`, `[C]` H6 |
| T7 | lint 두 층 — 구조는 토큰 없는 스크립트(CI nonzero exit), 의미(모순·낡음·중복)만 모델. 모순은 "어느 줄 vs 어느 줄"로 구조화 출력, 뭉개지 말고 병기 | `[C]` H7, `[P3-4]`, `[P3-2]` |
| T8 | 소스 해시/타임스탬프를 저장해 바뀐 소스만 재검증. 검토 주기는 페이지 유형별(가격 7–30일 … 아키텍처 6–18개월) | `[C]` H8, Glukhov |
| T9 | 캡처(자율)와 승격(사람 게이트) 분리. 고위험 변경(주장 삭제·정전 재작성·결정 변경·보안·가격)만 사람 검토. PR은 dev 브랜치, auto-merge 금지 | `[C]` H9 |
| T10 | 기록 트리거(선택지·뒤집힌 결정·암묵 규칙·측정값)와 do-not-record 목록 명시. "확장 우선, 생성 금지"; append 대신 rewrite + 주장별 날짜 | `[C]` H10 |
| T11 | 소스는 유형 분류 후 작은 단위(챕터·스레드)로 투입. 소스당 8~38 페이지 변동을 예산에 반영 | `[C]` H11, `[W1]` 10–15 |
| T12 | 검색 로드맵: index.md → grep → BM25(FTS5) → 하이브리드/RRF → 벡터(용어 불일치용). 한국어는 BM25 가드레일 | `[C]` H12, `[W13]` `[W15]` `[P2-11]` |
| T13 | 답변은 위키에서, 근거 문장은 원본에서(provenance). 검증기는 모델 없는 코드. Citations API로 인용 포인터 보장. 없으면 "없음"(insufficient_evidence) | `[C]` H13, `[W18]` `[W37]`, `[P2-6]` |
| T14 | 세션은 짧게 자주. 위키를 작업 중에도 읽게(답 + 위키 갱신 두 출력). 야간 잡은 `claude -p` + 1시간 캐시 TTL | `[C]` H14, `[W16]` `[W21]` `[W25]` |
| T15 | 마크다운을 떠날 신호: 수백 페이지 + 다중 writer + 연속 write-back. 그래도 "Postgres는 리빌드 가능한 인덱스일 뿐" | `[C]` H15 |
| T16 | 신뢰할 수 없는 소스를 읽는 headless 에이전트는 wiki/ 쓰기 전용·git 금지, 커밋은 스크립트. 소스 텍스트는 데이터로 취급 | `[W11]`, `[C]` Stigmergy·Fontoura |
| T17 | 골든 Q&A 20~50개(실제 실패에서), "없는 답" 거부 항목 포함, 회귀 평가로 고정. faithfulness·citation precision/recall 측정 | `[W22]`, `[P4-1]` `[P4-3]` `[P4-7]` |
| T18 | 업무 지식은 사람·결정·약속·마감 타입 엔티티로; 결정 vs 미결 구분; 결정의 이유를 남기는 건 사람 | `[C]` @_avichawla·당근, `[W37]` |
| T19 | 그래프 DB는 뒤로 미뤄도 된다 — 그래프 자체의 이득은 약 2%(Mem0 자체 평가), 효과는 추출·통합·갱신 루프 | `[P1-5]` |
| T20 | 모델 가중치 편집이 아니라 외부 텍스트(위키)에서 지식 갱신 | `[P3-5]` `[P3-7]` |

---

## 14. 챕터 오프닝용 날것 인용 (community.md §7 그대로 보존)

1. "Six months in, you have entries that are confidently wrong and the lint pass can't tell which." — Abby_101, HN
2. "Everyone is writing. Nobody is reading." — simsla, HN
3. "'raw is immutable' in a CLAUDE.md is a wish, not a rule." — @vellumkasane, Dev.to
4. "답이 없는 질문 10개를 던지면 10개 전부 아무 노트나 근거로 물고 나왔고" — clue.oz4e, PyTorchKR
5. "the moment those files change, the compiled knowledge might be wrong — and doesn't know it." — Jwcjwc12, gist
6. "What's the failure mode? Where does it start fighting you?" — alinawab, gist (답글 없음)
7. "it's more fun to build than to actually use." — saberience, HN
8. "The LLM is the writer. You're the editor-in-chief." — bluewater8008, gist
9. "Contradictions are assets, not errors." — Jim Liu
10. "토큰만 5~10배 잡아먹고 컨텍스트도 자주 놓칩니다." — alfadur, GeekNews
11. "But this pattern breaks when you apply it to actual work" — @_avichawla
12. "Yes, I set up Karpathy's LLM wiki. Now what?" — @keane42443
13. "Missing 5 percent is fine. Missing three weeks is not." — Theo James
14. "Instructions set intent. Hooks enforce behavior" — Aaron Fulkerson
15. "A page without a review date is a page that will eventually lie quietly." — Rost Glukhov
16. "노트가 바뀌었을 때 위키가 조용히 낡는데, 그걸 알려주는 신호가 없다는 게 제가 겪은 가장 큰 위험이었습니다." — clue.oz4e
17. "No write waits for a human." — Stigmergy README (반대 극단)
18. "Who decides what becomes a memory, and how is it evaluated?" — MoserMichael, gist

추가 후보(웹·논문·공식에서):
19. "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase." — Karpathy gist `[W1]`
20. "The hard part of an LLM-maintained wiki is trusting what it tells you later." — ShootJackal, gist 댓글(2026-10-01) `[W2]`
21. "Extend, don't create. The default failure is near-duplicate pages." — HagaiHen `[W2]`
22. "이런 질문에는 모델의 추론 능력만으로 답할 수 없어요." — 토스 김병균 `[W37]`
23. "Many facts come with an expiration date, from the name of the President to the basketball team Lebron James plays for." — Dhingra 외, TACL 2022 `[P3-8]`
24. "what to retrieve depends on what has already been derived, which in turn may depend on what was previously retrieved." — IRCoT `[P2-4]`
25. "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills." — Claude Code best practices `[W25]`
26. "Surprisingly, we find that structural coherence consistently hurts model performance." — Chroma Context Rot `[P-S2]`
27. "남의 시스템을 그대로 쓰면 반드시 어딘가에서 안 맞는 부분이 생긴다." — 한국 개발자, AI매터스 인용 `[C]`
28. "the ultimate self-improving second brain, and it takes zero manual editing" — @DataChaz (실사용 보고들과 정면 충돌하는 과장 사례) `[C]`

---

## 15. 참고문헌

### 15.1 1차 소스·파생 구현 (웹)
- [W1] Andrej Karpathy. LLM Wiki (gist). https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f , gist 생성 2026-04-04 (2026-10-11 열람).
- [W2] 위 gist Comments(2026-09-29 ~ 2026-10-08 구간: ShootJackal, HagaiHen, bg-numarqe 등).
- [C] Andrej Karpathy. X 포스트 "LLM Knowledge Bases". https://x.com/karpathy/status/2039805659525644595 , 2026-04-02 (fxtwitter 메타데이터만).
- [W3] Casey Newton. An LLM wiki changed how I work. Platformer, https://www.platformer.news/karpathy-llm-wiki-journalism-productivity/ , 2026-08-18.
- [W4] GeekNews. LLM-Wiki - LLM을 활용하여 개인 지식저장소 구축 하기. https://news.hada.io/topic?id=28208 , 2026-04경.
- [W5] GeekNews(alfadur). Retrieval as Reasoning - LLM Wiki가 RAG보다 나은 이유에 대한 실증 벤치마크. https://news.hada.io/topic?go=comments&id=32164 , 2026-08경. (원 논문 arXiv 2605.25480 — 미대조)
- [W6] 카일라스. LLM 위키 vs RAG 500+ 메모 실측. 클리앙 팁과강좌, https://www.clien.net/service/board/lecture/19182891 , 2026-04-26.
- [W7] 비케이. "AI 사서를 고용했습니다" 클로드 코드로 개인 LLM Wiki 만들기. GPTers, https://www.gpters.org/nocode/post/we-hired-ai-librarian-0l2pOuNs3RSkWFx , 2026-05-27.
- [W8] Lucas Astorian 외. llmwiki — Open Source Implementation of Karpathy's LLM Wiki. https://github.com/lucasastorian/llmwiki (★1.7k, 2026-10-11 기준).
- [W9] Astro-Han. karpathy-llm-wiki (Agent Skill). https://github.com/Astro-Han/karpathy-llm-wiki (★2.5k).
- [W10] Julian Oczkowski. karpathy-llm-wiki — 단계별 가이드. https://github.com/julianoczkowski/karpathy-llm-wiki (★54, © 2026).
- [W11] HagaiHen. podcast-wiki. https://github.com/HagaiHen/podcast-wiki (커밋 124, 2026-10).
- [W12] tobi. qmd. https://github.com/tobi/qmd (★30.3k, 2026-10-11 기준); 아키텍처 문서 https://mintlify.com/tobi/qmd/architecture/overview
- [W13] Blake Crosley. Hybrid retriever for Obsidian vault (FTS5 + vector + RRF). https://blakecrosley.com/blog/hybrid-retriever-obsidian , 2026(일자 미확인).
- [C] rohitg00. LLM Wiki v2 (gist). https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2
- [C] Stigmergy README. https://github.com/sturlese/stigmergy , 2026-08.

### 15.2 Anthropic 공식 문서·엔지니어링 블로그
- [W14] Rajasekaran, Dixon, Ryan, Hadfield. Effective context engineering for AI agents. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents , 2025-09-29.
- [W15] Anthropic. Introducing Contextual Retrieval. https://www.anthropic.com/news/contextual-retrieval , 2024-09-19.
- [W16] Claude API 문서. Prompt caching. https://platform.claude.com/docs/en/build-with-claude/prompt-caching (2026-10-11 열람).
- [W17] Claude API 문서. Context windows. https://platform.claude.com/docs/en/build-with-claude/context-windows (2026-10-11 열람).
- [W18] Claude API 문서. Citations. https://platform.claude.com/docs/en/build-with-claude/citations (2026-10-11 열람).
- [W19] Claude API 문서. Files API. https://platform.claude.com/docs/en/build-with-claude/files (2026-10-11 열람).
- [W20] Claude API 문서. Memory tool. https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (2026-10-11 열람).
- [W21] Justin Young. Effective harnesses for long-running agents. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents , 2025-11-26.
- [W22] Grace, Hadfield, Olivares, De Jonghe. Demystifying evals for AI agents. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents , 2026-01-09.
- [W23] Zhang, Lazuka, Murag. Equipping agents for the real world with Agent Skills. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills , 2025-10-16 (2025-12-18 업데이트).
- [W24] Claude Code 문서. How Claude remembers your project. https://code.claude.com/docs/en/memory (2026-10-11 열람).
- [W25] Claude Code 문서. Best practices. https://code.claude.com/docs/en/best-practices (2026-10-11 열람; 구 URL은 308 리다이렉트).
- [W26] Claude Agent SDK. Overview. https://code.claude.com/docs/en/agent-sdk/overview (2026-10-11 열람).
- [W27] Claude Agent SDK. Subagents. https://code.claude.com/docs/en/agent-sdk/subagents (2026-10-11 열람).
- [W28] Claude Agent SDK. Sessions. https://code.claude.com/docs/en/agent-sdk/sessions (2026-10-11 열람).
- [W29] Claude Agent SDK. Hooks. https://code.claude.com/docs/en/agent-sdk/hooks (2026-10-11 열람).
- [W30] Claude Code 문서. MCP. https://code.claude.com/docs/en/mcp (2026-10-11 열람).
- [C] anthropics/claude-code 이슈 #42796. https://github.com/anthropics/claude-code/issues/42796 , 2026-04-02.
- [C] anthropics/claude-agent-sdk-python 이슈 #772(·#23·#1320). https://github.com/anthropics/claude-agent-sdk-python/issues/772

### 15.3 저장·발행·수집 도구
- [W31] Jacky Zhao. Quartz 5. https://quartz.jzhao.xyz/ (v5.0.0, 2026-10-11 기준).
- [W32] Docusaurus vs Quartz 비교. https://www.wmtips.com/technologies/compare/docusaurus-vs-quartz ; https://www.featurebase.app/blog/docusaurus-alternatives (2026, 벤더 글).
- [W33] lychee-action https://github.com/lycheeverse/lychee-action ; sidequery/mdlint https://gitblind.noratr.app/sidequery/mdlint ; claude-obsidian wiki-lint https://tessl.io/registry/skills/github/AgriciDaniel/claude-obsidian/wiki-lint (2026-10 기준).
- [W34] Notion API. Retrieve page markdown. https://developers.notion.com/reference/retrieve-page-markdown (Notion-Version 2026-03-11, 2026-10-11 열람).
- [W35] PDF→Markdown 비교. https://themenonlab.blog/blog/best-open-source-pdf-to-markdown-tools-2026 ; https://dev.to/felipe_anyformat/pdf-to-markdown-for-llms-o2e ; https://www.file2markdown.ai/blog/docling-vs-markitdown (2026, 벤더 글).
- [W36] rusq. slackdump. https://github.com/rusq/slackdump (2026-10 기준).

### 15.4 한국 엔지니어링 블로그·보도
- [W37] 김병균. LLM은 똑똑한데, 왜 우리 회사 일은 모를까. 토스 테크, https://toss.tech/article/llm_context_topic , 2026-07-30.
- [W38] 김용성. Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기. 토스 테크, https://toss.tech/article/harness-for-team-productivity , 2026-02-26.
- [W39] BADA팀. AI 데이터 분석가 '물어보새' 3부. 우아한형제들 기술블로그, https://techblog.woowahan.com/23273/ (1부 https://techblog.woowahan.com/18144/), 2025-10-15.
- [W40] 한우형. 엔터프라이즈 LLM 서비스 구축기 1: 컨텍스트 엔지니어링. LY Corporation, https://techblog.lycorp.co.jp/ko/building-an-llm-service-for-enterprise-1-context-engineering (발행일 미표시).
- [W41] giginet. ODW #5: 벡터 DB와 에이전트 스킬로 RAG 시스템 만들기. LY Corporation, https://techblog.lycorp.co.jp/ko/building-rag-system-with-vector-db-and-agent-skills (발행일 미표시).
- [W42] 송하연. 업무 생산성 향상을 위한 Agentic RAG 기반 서비스. Samsung Tech Blog, https://techblog.samsung.com/blog/article/76 , 2026-01-29.
- [W43] 기타: fastcampus https://fastcampus.co.kr/story_article_llmwiki_2 ; brunch https://brunch.co.kr/@ghidesigner/488 ; velog https://velog.io/@qlgks1/RAG-is-dead-long-live-RAG-Agentic-Retrieval ; GeekNews WUPHF https://news.hada.io/topic?go=comments&id=28910 (2026, 2차).
- [C] PyTorchKR 토론. https://discuss.pytorch.kr/t/llm-wiki-karpathy/10843 , 2026-06~08.
- [C] GeekNews GN#352 주간. https://news.hada.io/weekly/202614 , 2026-04.
- [C] GeekNews alfadur 멀티에이전트. https://news.hada.io/topic?go=comments&id=31140 , 2026-07.
- [C] 박채빈. LLM Wiki (Karpathy). velog, https://velog.io/@parkchaebin/LLM-Wiki-Karpathy , 2026-05-12.
- [C] 김탄휴. AI매터스 칼럼. https://aimatters.co.kr/news-report/42742/ , 2026-05-21.
- [C] 박재홍. wikidocs 블로그. https://wikidocs.net/blog/@jaehong/10695/ (본문 접근 차단, 스니펫만 — 검증 필요).
- [C] 파이낸셜뉴스. 당근 발표(AI월드 2026). https://www.fnnews.com/news/202609091826242004
- [C] maketimelab. 노션 AI 에이전트 활용. https://maketimelab.com/ai-2026/ (개인 블로그).
- [C] Threads @choi.openai. https://www.threads.com/@choi.openai/post/DWvW8IvicHN/ (검증 필요).

### 15.5 커뮤니티 — HN·gist·구현 보고·X
- [C] HN. LLM Wiki – example of an 'idea file'. https://news.ycombinator.com/item?id=47640875 , 2026-04-04 (296p / 95댓글).
- [C] HN. WUPHF 스레드. https://news.ycombinator.com/item?id=47899844 , 2026-04-25.
- [C] HN. vault-operator 스레드. https://news.ycombinator.com/item?id=48351115 , 2026-06-01.
- [C] HN. Ask HN: Do you use LLM-Wikis? https://news.ycombinator.com/item?id=48952492 , 2026-07-17.
- [C] HN. 10x 스레드 https://news.ycombinator.com/item?id=48586811 ; OKF 스펙 https://news.ycombinator.com/item?id=48620068
- [C] Felipe Fontoura. https://felipefontoura.com/articles/llm-wiki/ , 2026-10-06.
- [C] Rost Glukhov. https://www.glukhov.org/knowledge-management/knowledge-systems-architectures/compiled-knowledge/llm-wiki-maintenance-knowledge-drift/
- [C] Taktile Engineering. https://engineering.taktile.com/blog/llm-wiki-agent-memory/ , 2026-07-13.
- [C] Jim Liu. https://www.openaitoolshub.org/en/blog/karpathy-llm-wiki , 2026-05-06.
- [C] Eugeniu Ghelbur. https://theaioperator.io/p/i-rebuilt-karpathys-llm-wiki-heres , 2026-04-29.
- [C] Theo James. Medium, https://medium.com/@theo-james/i-tried-to-build-karpathy-llm-wiki-heres-where-it-broke-down-for-me-9c3eef65af21 , 2026-04-21.
- [C] Aaron Fulkerson. https://aaronfulkerson.com/2026/04/12/karpathys-pattern-for-an-llm-wiki-in-production/ , 2026-04-12.
- [C] @vellumkasane. Dev.to, https://dev.to/vellumkasane/four-things-that-broke-when-i-ran-karpathys-llm-wiki-with-claude-code-and-the-fixes-4h4f , 2026-09-22.
- [C] dishant0406. Dev.to, https://dev.to/dishant0406/why-your-ai-keeps-forgetting-everything-you-told-it-1mkl
- [C] atlan. https://atlan.com/know/llm-wiki-vs-rag-knowledge-base/
- [C] lucasastorian/llmwiki 이슈 #93. https://github.com/lucasastorian/llmwiki/issues/93 , 2026-09-19.
- [C] @_avichawla. https://x.com/_avichawla/status/2041798871383441807 , 2026-04-08.
- [W44] LatentEval. Is Grep All You Need? How Agent Harnesses Reshape Agentic Search. https://latenteval.ai/research/is-grep-all-you-need , 2026-08-03 (논문 arXiv 2605.15184, 2026-05-14 — 미대조).
- [W45] Dev.to. https://dev.to/nimay_04/rag-is-not-always-the-answer-anymore-how-ai-agents-search-code-in-2026-43m3 ; https://dev.to/pueding/is-grep-all-you-need-grep-vs-vector-retrieval-for-agentic-search-534k (2026).

### 15.6 논문 (arXiv ID · 발표처 · 피인용수는 Semantic Scholar 2026-10-11 기준)
- [P-S2] Hong, Troynikov, Huber (Chroma). Context Rot: How Increasing Input Tokens Impacts LLM Performance. https://www.trychroma.com/research/context-rot , 2025-07-14. 기술 보고서(비동료심사, arXiv ID 없음).
- [P1-1] Zhang 외. A Survey on the Memory Mechanism of LLM based Agents. arXiv 2404.13501, 2024. ACM TOIS(S2 표기). 피인용 845.
- [P1-2] Park 외. Generative Agents: Interactive Simulacra of Human Behavior. arXiv 2304.03442, 2023. UIST 2023(S2 표기). 피인용 5,937.
- [P1-3] Packer 외. MemGPT: Towards LLMs as Operating Systems. arXiv 2310.08560, 2023(v2 2024-02). 프리프린트. 피인용 1,572.
- [P1-4] Xu 외. A-MEM: Agentic Memory for LLM Agents. arXiv 2502.12110, 2025(v11 2025-10-08). NeurIPS 2025(확인). 피인용 1,172.
- [P1-5] Chhikara 외. Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory. arXiv 2504.19413, 2025. ECAI 2025(S2 표기). 피인용 770.
- [P1-6] Rasmussen 외. Zep: A Temporal Knowledge Graph Architecture for Agent Memory. arXiv 2501.13956, 2025. 프리프린트. 피인용 411.
- [P1-7] Sarthi 외. RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval. arXiv 2401.18059, 2024. ICLR 2024(S2 표기). 피인용 783.
- [P1-8] Edge 외. From Local to Global: A Graph RAG Approach to Query-Focused Summarization. arXiv 2404.16130, 2024(v2 2025-02-19). 프리프린트. 피인용 2,323.
- [P1-9] Guo 외. LightRAG: Simple and Fast Retrieval-Augmented Generation. arXiv 2410.05779, 2024(v3 2025-04-28). EMNLP(S2 표기). 피인용 532.
- [P1-10] Gutiérrez 외. HippoRAG. arXiv 2405.14831, 2024. NeurIPS 2024(확인). 피인용 398.
- [P1-11] Chen 외. Dense X Retrieval: What Retrieval Granularity Should We Use? arXiv 2312.06648, 2023(v3 2024-10). EMNLP(S2 표기, 2024 추정). 피인용 161.
- [P1-12] Qu, Tu, Bao. Is Semantic Chunking Worth the Computational Cost? arXiv 2410.13070, 2024. 프리프린트. 피인용 75.
- [P2-1] Gao 외. Retrieval-Augmented Generation for Large Language Models: A Survey. arXiv 2312.10997, 2023(v5 2024-03). 피인용 4,260.
- [P2-2] Singh 외. Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG. arXiv 2501.09136, 2025(v4 2026-04-01). 피인용 444.
- [P2-3] Yao 외. ReAct: Synergizing Reasoning and Acting in Language Models. arXiv 2210.03629, 2022. ICLR 2023(확인). 피인용 12,364.
- [P2-4] Trivedi 외. Interleaving Retrieval with Chain-of-Thought Reasoning (IRCoT). arXiv 2212.10509, 2022. ACL 2023(확인). 피인용 1,395.
- [P2-5] Asai 외. Self-RAG. arXiv 2310.11511, 2023. ICLR 2024(S2 표기). 피인용 2,809.
- [P2-6] Yan 외. Corrective Retrieval Augmented Generation (CRAG). arXiv 2401.15884, 2024(v3 2024-10). 프리프린트. 피인용 325.
- [P2-7] Jin 외. Search-R1. arXiv 2503.09516, 2025(v5 2025-08). 프리프린트. 피인용 1,587.
- [P2-8] Liu 외. Lost in the Middle: How Language Models Use Long Contexts. arXiv 2307.03172, 2023. TACL 2023(확인). 피인용 5,438.
- [P2-9] Levy, Jacoby, Goldberg. Same Task, More Tokens. arXiv 2402.14848, 2024. ACL 2024(확인). 피인용 256.
- [P2-10] Hsieh 외. RULER. arXiv 2404.06654, 2024. COLM 2024(확인). 피인용 1,452.
- [P2-11] Modarressi 외. NoLiMa. arXiv 2502.05167, 2025. ICML 2025(확인). 피인용 147.
- [P2-12] Li 외 (Google DeepMind). Retrieval Augmented Generation or Long-Context LLMs? arXiv 2407.16833, 2024. EMNLP 2024 Industry Track(확인). 피인용 193.
- [P3-1] Xu 외. Knowledge Conflicts for LLMs: A Survey. arXiv 2403.08319, 2024. EMNLP 2024(S2 표기). 피인용 376.
- [P3-2] Xie 외. Adaptive Chameleon or Stubborn Sloth. arXiv 2305.13300, 2023. ICLR 2024 Spotlight(확인). 피인용 428.
- [P3-3] Wu, Wu, Zou. ClashEval. arXiv 2404.10198, 2024(v3 2025-02). NeurIPS 2024(S2 표기, 트랙 미확인). 피인용 144.
- [P3-4] Wang 외. Resolving Knowledge Conflicts in Large Language Models. arXiv 2310.00935, 2023(v3 2024-10). COLM 2024(확인). 피인용 51.
- [P3-5] Yao 외. Editing Large Language Models: Problems, Methods, and Opportunities. arXiv 2305.13172, 2023. EMNLP 2023(확인). 피인용 505.
- [P3-6] Zhang 외. A Comprehensive Study of Knowledge Editing for Large Language Models. arXiv 2401.01286, 2024(v5 2024-11). 피인용 186.
- [P3-7] Cohen 외. Evaluating the Ripple Effects of Knowledge Editing in Language Models. arXiv 2307.12976, 2023. TACL 2024(확인). 피인용 332.
- [P3-8] Dhingra 외. Time-Aware Language Models as Temporal Knowledge Bases. arXiv 2106.15110, 2021. TACL 2022 vol.10 pp.257–273. 피인용 426.
- [P3-9] Jang 외. TemporalWiki. arXiv 2204.14211, 2022. EMNLP 2022(확인). 피인용 미조회.
- [P3-10] Vu 외 (Google). FreshLLMs. arXiv 2310.03214, 2023. ACL 2024 Findings(S2 표기). 피인용 450.
- [P3-11] Lee 외 (Google). Deduplicating Training Data Makes Language Models Better. arXiv 2107.06499, 2021. ACL 2022(확인). 피인용 1,012.
- [P3-12] Abbas 외 (Meta). SemDeDup. arXiv 2303.09540, 2023. 프리프린트. 피인용 미조회.
- [P4-1] Es 외. Ragas. arXiv 2309.15217, 2023(v2 2025-04). EACL 2024(S2 표기). 피인용 1,154.
- [P4-2] Saad-Falcon 외. ARES. arXiv 2311.09476, 2023. NAACL 2024(확인). 피인용 444.
- [P4-3] Gao 외 (Princeton). Enabling LLMs to Generate Text with Citations (ALCE). arXiv 2305.14627, 2023. EMNLP 2023(확인). 피인용 864.
- [P4-4] Liu, Zhang, Liang. Evaluating Verifiability in Generative Search Engines. arXiv 2304.09848, 2023. Findings of EMNLP 2023(확인). 피인용 476.
- [P4-5] Min 외. FActScore. arXiv 2305.14251, 2023. EMNLP 2023(확인). 피인용 1,819.
- [P4-6] Niu 외. RAGTruth. arXiv 2401.00396, 2023(v2 2024-05). ACL 2024(S2 표기). 피인용 434.
- [P4-7] Wu 외. LongMemEval. arXiv 2410.10813, 2024(v2 2025-03). ICLR 2025(확인). 피인용 750.
- [P4-8] Semnani 외 (Stanford). WikiChat. arXiv 2305.14292, 2023. Findings of EMNLP 2023(확인). 피인용 미조회.
- [P5-1] Shao 외 (Stanford). STORM. arXiv 2402.14207, 2024. NAACL 2024 Main(확인). 피인용 210.
- [P5-2] Jiang 외. Co-STORM. arXiv 2408.15232, 2024. EMNLP 2024 Main(확인). 피인용 64.
- [P5-3] Yang 외. WikiAutoGen. arXiv 2503.19065, 2025(v3 2025-09). ICCV 2025(확인). 피인용 5.
- [P 부록A] Reflexion arXiv 2303.11366 (NeurIPS 2023 미확인); Agent Workflow Memory arXiv 2409.07429; MemoryBank arXiv 2305.10250 (AAAI 2024 미확인); MemoRAG arXiv 2409.05591 (TheWebConf 2025 확인); MemOS arXiv 2507.03724; CRAG 재현 arXiv 2603.16169 (2026).
- 2차 인용만 존재(미대조): Retrieval as Reasoning arXiv 2605.25480; Is Grep All You Need arXiv 2605.15184; 자동 생성 AGENTS.md 성능 저하 arXiv 2602.11988.

---

## 16. 리서치 한계 (세 리서처의 공백 통합)

### 16.1 접근 실패·미수집
- **Reddit 전면 미접근**(old/www/미러 모두 차단; WebSearch도 r/ObsidianMD·r/ClaudeAI·r/LocalLLaMA 미반환). Fontoura가 인용한 Reddit 발언 "Maintaining AI curated vault is just not sustainable"은 원 스레드 미발견 → 2차 인용만 `[C]`.
- **X 본문**: x.com 직접 fetch 402/451. fxtwitter로 메타데이터·핵심 문장만. Karpathy 포스트 답글 2,939개 미열람. Karpathy 원 트윗 문구는 Platformer 인용 외 1차 미확인 `[C]` `[W]`.
- **Lobsters**: Anubis 봇 차단, WebSearch 미노출 `[C]`.
- **gist 댓글**: 약 250개 열람(4페이지 각 앞 100K자). 2026-04-09 이후~9월 중순 일부 미열람; web 리서처는 offset 100000 이후(9~10월)만 읽음. 댓글 상당수가 자기 제품 홍보(페이지당 약 40–50%) `[C]` `[W2]`.
- **HN**: 원 스레드·WUPHF 접힌 댓글 일부 미확인 `[C]`.
- **한국**: OKKY·커리어리 관련 토론 미발견. wikidocs 박재홍 글 스니펫만. brunch 유훈식 글은 3인칭. youngju.dev "사내 지식베이스를 LLM으로 만든다는 것"(2026-07-31) 도메인 만료. 카카오·네이버 D2의 사내 지식베이스 글 미노출. **국내 사내 도입 후기는 사실상 없음** `[C]` `[W]`.
- **웹**: Cerebras 사내 지식베이스 원문(2026-07-15 추정) 공식 URL 미발견(2차 요약만, 인용 보류). Samsung Tech Blog 본문 Cloudflare 520·"Agentic Search 시스템 구축기"(2026-02) URL 미확보. npmjs 403 → `npm view`로 대체. Google Docs → 마크다운 공식 경로(Drive API export `text/markdown`) 미확인. Quartz/Docusaurus 사내 인증(SSO 프록시) 1차 문서 미확보. Obsidian Web Clipper 공식 문서 미수집. Claude Code MCP 문서 "tool search" 절 미열람 `[W]`.
- **논문**: Semantic Scholar 검색 429 → batch로 피인용수만; TemporalWiki·WikiChat·SemDeDup 피인용 미조회. 발표처는 arXiv 코멘트 명시만 "확인", 나머지 "S2 표기"(트랙·연도 미확인). 전문은 HTML 버전 일부만 처음 100K자까지. **LLM Wiki 패턴과 직접 관련된 2026년 논문 3편(2605.25480, 2605.15184, 2602.11988)이 papers.md에 없음** — 웹·커뮤니티 2차 인용만 `[P]`.
- **회사 규모 사례 희소**: Taktile(회사 블로그), psanchez(HN 댓글), Stigmergy(README), pnakamura($132M 프로그램 언급, 상세 없음). "팀 승인 흐름을 6개월 이상 운영한" 보고는 saadn92 한 건 `[C]`.
- **언어 편중**: 영어 HN·gist 중심; 중국어·일본어는 X 스니펫만(@yusaku_0426 3층·4사이클 정리, @op7418 "跟我用的方法也很相似") `[C]`.

### 16.2 구조적 공백
- "LLM이 유지보수하는 wiki" 자체를 직접 연구한 동료심사 논문은 찾지 못했다(가장 가까운 것: A-MEM의 Zettelkasten 메모리, STORM의 문서 생성, Zep의 시간 그래프). 주장의 근거를 인접 연구에서 끌어와야 한다는 제약이자 책의 차별점 `[P]`.
- 수치 신뢰도: 커뮤니티 모든 숫자는 자기 보고. 특히 WUPHF recall 85%, Stigmergy 1.00, techwithhari 3/10→7/10, "21배 토큰", Taktile 벤치는 fact-checker가 원문 대조 필요 `[C]`.
- 의도적 제외(web): 출처·날짜 없는 나열형 "2026 가이드"(mindstudio, agentpedia, kunalganglani 등), 벤더 홍보성 비교(file2markdown 등 참고 표시만) `[W]`.
- 모델 비결정성(모델/버전마다 위키 산출이 달라지는 문제)에 대한 통제 실험 부재 `[C]` `[W5]`.
- 사내 KB 특유의 주제(권한 인지 검색·개인정보·감사 로그)를 1차로 다룬 자료가 youngju.dev 글 하나였고 접근 실패.

---

## 17. 사실 확인 원장 (세 파일의 경고 플래그 전부 — fact-checker용)

| # | 항목 | 상태/지시 | 출처 |
|---|---|---|---|
| F1 | Karpathy gist 날짜 04-02 vs 04-04 | "2026년 4월 초"로; 트윗 04-02 / gist 04-04 구분 | W1, C |
| F2 | Karpathy 트윗 원문 문구 | Platformer 인용 외 1차 미확인; 요지만 사용 | W3, C |
| F3 | "100 articles / 400,000 words" 등 Karpathy 위키 규모 | 근거 미확인 — **사용 금지** | W 교차검증, P-S1 |
| F4 | gist 규모 수치는 "~100 sources, ~hundreds of pages"·"10–15 pages per ingest"뿐 | 그 외 규모 수치를 gist 귀속으로 쓰면 날조 | P-S1 |
| F5 | Retrieval as Reasoning(arXiv 2605.25480) F1 2.0~8.1, ablation −11.7/−13.8/−12.2 등 | GN 2차 요약 — 논문 원문 대조 (사실 확인 필요) | W5, C |
| F6 | "위키가 약 21배 더 많은 토큰" 사전등록식 비교 | 2차 인용, 검증 필요 | C |
| F7 | PwC Is Grep All You Need(arXiv 2605.15184) 93.1% vs 76.7%, 10/10·5/10 | 2차 해설; 해설 자체가 76.7%/94.0% 표 불일치 지적; 신뢰구간 없음 | W44 |
| F8 | arXiv 2602.11988 "자동 생성 AGENTS.md가 더 나쁨" | HN 댓글 인용만 (사실 확인 필요) | C |
| F9 | 1M 컨텍스트 GA 날짜 "2026-03-13(Opus 4.6/Sonnet 4.6)" | 1차 문서 미확인 (사실 확인 필요) | W17 |
| F10 | 모델명·캐시 배수(Fable 5.1·Mythos 5.1 0.025x; Opus 5.5·Sonnet 5.5 0.05x)·최소 캐시 길이 | 2026-10-11 공식 문서 기준 — 집필 시 재확인 | W16, W17 |
| F11 | Agent SDK 버전 PyPI 0.2.165(2026-10-08) / npm 0.3.296(2026-10-09) | "2026년 10월 기준 0.2.x / 0.3.x"로 | W26 |
| F12 | Files API 구 헤더 `files-api-2025-04-14` | GA — 베타 헤더 불필요; 구 자료 주의 | W19 |
| F13 | Contextual Retrieval 35%/49%/67%, $1.02/M, "200K 토큰 ≈ 500 pages" | "2024년 기준"으로 못 박을 것 | W15 |
| F14 | SKILL.md "5,000토큰/500줄 이하", "스킬당 메타 ~100토큰" | 공식 글에 없음 (사실 확인 필요) | W23 |
| F15 | Notion `include_transcript` 파라미터(2026-02-26 체인지로그) | 2차 자료 (사실 확인 필요) | W34 |
| F16 | slackdump 마크다운 직접 출력 | 미확인 | W36 |
| F17 | Quartz/Docusaurus 사내 SSO 프록시(Cloudflare Access, oauth2-proxy) | 1차 소스 미확보 (사실 확인 필요) | W31, W32 |
| F18 | PDF→Markdown 도구 비교 수치 | 벤더/블로그 — 수치 인용 금지 | W35 |
| F19 | 우아한형제들 "BM25s 최대 500배 빠름", "임직원 4명 중 1명 사용" | 요약 수치 — 원문 대조 (사실 확인 필요); "약 15%"는 원문 | W39 |
| F20 | LY Corporation 두 글 발행일 | 페이지 미표시(2025~2026 추정) (사실 확인 필요) | W40, W41 |
| F21 | 토스 Topic "0.87", "세 번/두 번" | 예시값 — 평가 수치 아님 | W37 |
| F22 | Blake Crosley 글 일자 | 미확인(2026) | W13 |
| F23 | A-MEM "multi-hop 2배" | 표와 어긋남 — 쓰지 말 것; 토큰 절감은 "최대 약 93%" | P1-4 |
| F24 | Search-R1 상대 개선 41% vs 24% | "20~41%(버전에 따라 상이)" | P2-7 |
| F25 | LC vs RAG 실패 유형 | 4개 범주(A~D)+기타 — "7가지" 아님 | P2-12 |
| F26 | Lost in the Middle 75.8/53.8/63.2, RAGTruth 환각 비율, CRAG Self-CRAG 차이 | (계산값) — 논문 문장 아님 | P2-8, P4-6, P2-6 |
| F27 | Context Rot 보고서 arXiv ID | 없음(검색 미노출) — URL로 인용, 비동료심사 명시 | P-S2 |
| F28 | 벤더 자체 평가(Mem0 26%·2%, Zep DMR 94.8%, Chroma) | 본문에 "자체 평가" 명시 | P1-5, P1-6, P-S2 |
| F29 | 발표처 "S2 표기"·"미확인" 항목(RAPTOR, Self-RAG, Mem0, Dense X, ClashEval, RAGAS, RAGTruth, FreshLLMs, Reflexion, MemoryBank, SemDeDup 등) | 본문 인용 전 재조회 | P 수집 한계 |
| F30 | Verifiability 51.5%/74.5% | 2023년 초 상용 시스템 기준 — 일반화 금지 | P4-4 |
| F31 | Dedup 논문(학습 데이터 맥락) | 검색 코퍼스 dedup 효과 직접 측정 아님 — 과잉 일반화 주의 | P3-11 |
| F32 | WikiAutoGen | 피인용 5 — "최근 방향"으로만 | P5-3 |
| F33 | 커뮤니티 수치 전부(Taktile 벤치·Jim Liu·Ghelbur·vbarsoum·HagaiHen·glaucobrito·clue.oz4e recall@5 93%·WUPHF recall@20 85%·Stigmergy 1.00·techwithhari 3/10→7/10·클리앙 20분) | 자기 보고, 통제군 없음 — 원문 링크 재확인 | C |
| F34 | Threads "하루 만에 270만 회" | 검증 필요 | C |
| F35 | 박재홍 wikidocs "빈틈이 너무 많다", "새로운 유형의 기술 부채" | 스니펫만 — 검증 필요 | C |
| F36 | Fontoura 인용 Reddit 발언 | 원 스레드 미발견 — 2차 인용만 | C |
| F37 | Medium "메모 인제스트 이틀 뒤 재실행하니 다른 결과" | 2차 인용 | C |
| F38 | GN⁺ HN 의견 요약("모델 붕괴", "새로운 형태의 기술 부채") | 2차 요약 — 원 HN 댓글은 community.md의 devnullbrain·Imanari로 대조 | W4, C |
| F39 | julianoczkowski "수백 문서까지, 그 이상은 벡터DB" / 커뮤니티 "~100 pages" | 경험치 — gist 수치와 구분 | W10, C |
| F40 | psanchez "Claude Opus 4.6" | HN 댓글 자기 보고 | C |
| F41 | Claude Code 이슈 #42796 "5,000+ 단어 CLAUDE.md" | 이슈 보고 — 공식 문서 "200줄 이하"와 함께 인용 | C, W24 |
| F42 | Karpathy "surgically update only affected pages" 인용구 | community.md에만 등장(web.md 원문 발췌에 없음) — gist 원문 재확인 | C |

---

## 신선도 원장 (소스별 발행일 · 버전 시점 · 검색 시점)

| 소스 | 발행/버전 시점 | 검색·열람 시점 | 비고 |
|---|---|---|---|
| Karpathy gist | gist 생성 2026-04-04(Revisions: 1); X 포스트 2026-04-02 | 2026-10-11 | 별/포크 5,000+; 조회 21,958,561 |
| gist 댓글 | 2026-04-04 ~ 2026-10-08 | 2026-10-11 | 약 250개 + 9~10월 구간 |
| Platformer (Newton) | 2026-08-18 | 2026-10-11 | Claude Fable 5 사용 |
| GeekNews 28208 / 32164 / 28910 / 31140 / 주간 202614 | 2026-04 / 2026-08 / 2026-05 / 2026-07 / 2026-04 | 2026-10-11 | 상대 시간("6달전") 표기 |
| 클리앙 카일라스 | 2026-04-26 | 2026-10-11 | 조회 15,497 |
| GPTers 비케이 | 2026-05-27 | 2026-10-11 | |
| lucasastorian/llmwiki | ★1.7k·커밋 185 (2026-10-11 기준); 이슈 #93 2026-09-19 | 2026-10-11 | 최종 커밋일 미표시("약 62일 전") |
| Astro-Han/karpathy-llm-wiki | ★2.5k·커밋 28; "2026년 4월부터" | 2026-10-11 | SKILL.md 미열람 |
| julianoczkowski | ★54·커밋 3·© 2026 | 2026-10-11 | |
| HagaiHen/podcast-wiki | 커밋 124 (2026-10) | 2026-10-11 | |
| tobi/qmd | ★30.3k·커밋 781 (2026-10-11 기준); Node 22+/Bun 1.0+ | 2026-10-11 | 모델 파일 크기 README 기준 |
| Blake Crosley | 2026(일자 미확인) | 2026-10-11 | |
| Anthropic context engineering | 2025-09-29 | 2026-10-11 | |
| Anthropic Contextual Retrieval | 2024-09-19 | 2026-10-11 | **2024 기준 수치** |
| Claude API Prompt caching | 2026-10-11 열람 | 2026-10-11 | 모델별 배수 변동 가능 |
| Claude API Context windows | 2026-10-11 열람 | 2026-10-11 | 1M 기본; GA 날짜 미확인 |
| Claude API Citations | GA, 2026-10-11 열람 | 2026-10-11 | |
| Claude API Files | GA(베타 헤더 불필요), 2026-10-11 열람; SDK Py 1.2.0 / TS 0.122.0 | 2026-10-11 | |
| Claude API Memory tool | `memory_20250818`, 2026-10-11 열람 | 2026-10-11 | |
| Anthropic long-running harnesses | 2025-11-26 | 2026-10-11 | |
| Anthropic evals | 2026-01-09 | 2026-10-11 | |
| Anthropic Agent Skills | 2025-10-16 (업데이트 2025-12-18) | 2026-10-11 | |
| Claude Code memory 문서 | 2026-10-11 열람; v2.1.277+ (AGENTS.md), v2.1.283+ (prompt-audit) | 2026-10-11 | |
| Claude Code best practices | 2026-10-11 열람 | 2026-10-11 | 구 URL 308 |
| Agent SDK overview/subagents/sessions/hooks | 2026-10-11 열람; PyPI 0.2.165(2026-10-08), npm 0.3.296(2026-10-09); budget TS v0.3.219 / Py v0.2.127 이후 | 2026-10-11 | |
| Claude Code MCP 문서 | 2026-10-11 열람 | 2026-10-11 | tool search 절 미열람 |
| Quartz | v5.0.0 | 2026-10-11 | |
| Docusaurus 비교 글 | 2026(일자 미확인) | 2026-10-11 | 벤더 글 |
| lychee/mdlint/wiki-lint | 2026-10 기준 | 2026-10-11 | README 미확인 |
| Notion Markdown API | Notion-Version 2026-03-11 | 2026-10-11 | |
| PDF→MD 비교 | 2026 | 2026-10-11 | 벤더 글 |
| slackdump | 2026-10 활동 중 | 2026-10-11 | |
| 토스 Topic | 2026-07-30 | 2026-10-11 | |
| 토스 하네스 | 2026-02-26 | 2026-10-11 | 가설·방향성 |
| 우아한형제들 물어보새 3부 | 2025-10-15 | 2026-10-11 | |
| LY Corporation ×2 | 미표시(2025~2026 추정) | 2026-10-11 | |
| Samsung DeepDive | 2026-01-29 | 2026-10-11 | 도입부만 |
| LatentEval grep 해설 | 2026-08-03 (논문 2026-05-14, v1) | 2026-10-11 | |
| Dev.to 2차 글 | 2026 | 2026-10-11 | |
| HN 원 스레드 / WUPHF / vault-operator / Ask HN | 2026-04-04 / 04-25 / 06-01 / 07-17 | 2026-10-11 | |
| Taktile | 2026-07-13 | 2026-10-11 | |
| Jim Liu / Ghelbur / Theo James / Fulkerson / Fontoura / Glukhov | 2026-05-06 / 04-29 / 04-21 / 04-12 / 10-06 / 미표시 | 2026-10-11 | |
| @vellumkasane / @techwithhari | 2026-09-22 / 2026-05-10 | 2026-10-11 | |
| PyTorchKR 토론 | 2026-06-24 ~ 08-21 | 2026-10-11 | |
| velog 박채빈 / AI매터스 | 2026-05-12 / 2026-05-21 | 2026-10-11 | |
| @_avichawla | 2026-04-08 | 2026-10-11 | fxtwitter |
| Stigmergy | 2026-08 | 2026-10-11 | |
| Claude Code 이슈 #42796 | 2026-04-02 (댓글 583) | 2026-10-11 | |
| 논문 38편 | 각 arXiv 버전 일자(15.6절) | arXiv API·HTML 2026-10-11; Semantic Scholar 피인용 2026-10-11 | 전문은 HTML 일부 100K자 |
| Chroma Context Rot | 2025-07-14 | 2026-10-11 | 비동료심사 |
