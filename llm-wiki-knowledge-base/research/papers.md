# 논문 리서치: LLM Wiki 패턴으로 만드는 사내 지식 베이스

- 검색 시점: 2026-10-11
- 검색 소스: arXiv API(메타데이터·초록 전수 확인), arXiv HTML 전문(핵심 수치 추출), Semantic Scholar Graph API(피인용수·발표처, 2026-10-11 조회). 발표처 중 arXiv 코멘트로 교차 확인된 것은 "확인", Semantic Scholar 표기만 있는 것은 "S2 표기"로 구분했다.
- 장르: tech-book / 독자: 소프트웨어 개발자. 증명은 생략하고 결과·직관·수치 위주로 정리.
- 표기 규칙: 피인용수는 Semantic Scholar 2026-10-11 기준. 수치 중 "(계산값)"은 논문 표에서 리서처가 계산한 것으로 본문에 그 문장이 없다. 인용문은 영문 원문 그대로 두었다(번역은 저술가 재량).
- 수집 범위: 5개 목표 영역 × 서베이 1편 + seminal 2~3편 + 최근 3년 논문. 총 38편 + 1차 비학술 소스 2건(Karpathy gist, Chroma 기술 보고서).

---

## 0. 1차 소스 (논문 아님, 책의 출발점)

### S-1. Karpathy, "LLM Wiki" gist
- 출처: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (2026-10-11 열람)
- 성격: 패턴 설명 문서. 저자 Andrej Karpathy. 발행일은 gist 본문에 명시되지 않아 미확인.
- 구조 요약 (본문 "Architecture" 섹션):
  - 3계층 — **Raw sources**(불변 입력), **Wiki**(LLM이 소유·생성하는 markdown), **Schema**(CLAUDE.md/AGENTS.md 같은 규약 문서).
  - 3작업 — **Ingest**(소스 1건 읽고 → 요약 페이지 작성 → index 갱신 → 관련 entity/concept 페이지 수정 → log 추가; 소스 1건이 10~15페이지를 건드림), **Query**(index를 먼저 읽고 → 관련 페이지 읽고 → 인용 달아 답변; 좋은 답은 다시 wiki 페이지로 저장), **Lint**(모순·낡은 주장·고아 페이지·개념 페이지 누락·누락 교차참조·데이터 공백 점검).
  - `index.md` = 페이지 카탈로그(링크 + 한 줄 요약 + 카테고리). `log.md` = append-only 시간순 기록(일관된 prefix로 Unix 도구로 파싱 가능).
  - gist는 "backlink"라는 단어를 쓰지 않고 "inbound link / cross-reference"로 표현. 고아 페이지 = inbound link 없는 페이지.
- 인용할 만한 문장:
  > "the LLM incrementally builds and maintains a persistent wiki" (Core idea)
  > "the wiki is a persistent, compounding artifact." (Core idea)
  > "These are immutable — the LLM reads from them but never modifies them." (Architecture, Raw sources)
  > "good answers can be filed back into the wiki as new pages." (Operations, Query)
  > "This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)" (Indexing and logging, index.md)
- 책 관련성: 책 전체의 설계 원형. 아래 논문들은 이 패턴의 각 요소(계층적 요약=RAPTOR/GraphRAG, 노트 간 링크·진화=A-MEM, lint=knowledge conflict/stale-fact 연구, "index 먼저 읽기"=에이전틱 검색, 답변 환류=Generative Agents reflection)에 학술적 근거를 댄다.
- 주의: gist의 유일한 수치는 "~100 sources, ~hundreds of pages"와 "10–15 pages per ingest"다. 그 외 규모 수치를 책에 적으면 날조가 된다.

### S-2. Hong, Troynikov, Huber (Chroma), "Context Rot: How Increasing Input Tokens Impacts LLM Performance"
- 출처: https://www.trychroma.com/research/context-rot — 기술 보고서(비동료심사). 2025-07-14 발행. arXiv ID 없음(미확인 — arXiv에 "Context Rot" 제목으로 검색 시 이 보고서는 나오지 않음).
- 요약: 18개 모델(GPT-4.1, Claude 4, Gemini 2.5, Qwen3 계열)을 8개 입력 길이 × 11개 needle 위치로 평가. 입력이 길어질수록 모든 실험에서 성능이 일관되게 떨어진다. needle-질문 유사도가 낮을수록 길이에 따른 하락이 가파르고, distractor 1개만 있어도 baseline 대비 하락하며 4개면 더 떨어진다. 논리적으로 정합한(coherent) 건초더미가 섞인(shuffled) 건초더미보다 성능이 나쁘다. LongMemEval 306문항에서 모든 모델이 focused prompt(~300 토큰)가 full prompt(~113k 토큰)보다 높았다.
- 핵심 수치: 18 모델 / needle-질문 코사인 유사도 범위 0.445~0.775(PG essays), 0.521~0.829(arXiv) / 반복 단어 과제 거부율 2.55%(GPT-4.1)~2.89%(Claude Opus 4), Qwen3-8B 미시도 4.21%.
- 인용할 만한 문장:
  > "their performance grows increasingly unreliable as input length grows."
  > "Surprisingly, we find that structural coherence consistently hurts model performance."
  > "Even a single distractor reduces performance relative to the baseline (needle only)"
- 책 관련성: "그냥 전부 컨텍스트에 넣으면 되지 않나?"에 대한 2025년 시점 반박. wiki가 질문마다 작은 focused 컨텍스트를 만들어 주는 이유. "context rot"이라는 용어의 출처로 인용.
- 독자 전달: "컨텍스트 윈도우는 용량이지 성능 보증이 아니다" 한 줄. LongMemEval focused vs full 결과를 wiki 페이지 vs 원본 덤프 비유로.

---

## 1. LLM을 위한 지식 조직 (wiki·그래프·메모리·계층 요약·노트 vs 청크)

### 논문 1-1: A Survey on the Memory Mechanism of Large Language Model based Agents (서베이)
- 저자·연도: Zeyu Zhang, Xiaohe Bo, Chen Ma 외 (9인), 2024
- 발표처: ACM Transactions on Information Systems (S2 표기; 볼륨·호 미확인). arXiv v1 2024-04-21.
- arXiv ID: 2404.13501
- 피인용수: 845
- 요약: LLM 에이전트 메모리를 "왜 필요한가 → 어떻게 설계하는가(메모리 소스·형식·연산) → 어떻게 평가하는가"로 체계화한 첫 포괄 서베이. 메모리 연산을 writing·management·reading으로 나누고, 형식은 텍스트(원문·요약·구조화)와 파라메트릭으로 구분한다. 평가는 직접 평가(결과 정확도)와 간접 평가(다운스트림 과제)로 분류.
- 방법론 요약: 문헌 분류 + GitHub 저장소(nuster1128/LLM_Agent_Memory_Survey)로 지속 갱신.
- 핵심 수치: 서베이라 실험 수치 없음.
- 인용할 만한 문장:
  > "The key component to support agent-environment interactions is the memory of the agents." (Abstract)
- 책 관련성: 책의 용어 체계(쓰기/관리/읽기, 텍스트 메모리 vs 파라미터 메모리)를 빌려올 기준점. LLM Wiki = "텍스트 형식·구조화 메모리 + 명시적 관리 연산(lint)"으로 위치시킬 수 있다.
- 독자 전달: 메모리 연산 3분류를 wiki의 ingest(write)/lint(manage)/query(read)에 1:1로 매핑한 표.

### 논문 1-2: Generative Agents: Interactive Simulacra of Human Behavior (seminal)
- 저자·연도: Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein, 2023
- 발표처: UIST 2023 (ACM Symposium on User Interface Software and Technology; S2 표기, arXiv 코멘트 없음)
- arXiv ID: 2304.03442
- 피인용수: 5,937
- 요약: 25명의 에이전트가 사는 샌드박스 마을. 각 에이전트는 경험을 자연어로 **memory stream**에 전부 기록하고, 이를 주기적으로 **reflection**(상위 수준 통찰)으로 합성하며, 계획 수립 시 동적으로 검색한다. 밸런타인 파티 초대가 자발적으로 퍼지는 등 창발 행동을 보였다. 관찰·계획·성찰 각각이 "믿을 만함"에 기여함을 ablation으로 보였다.
- 방법론 요약: 검색 점수 = recency + importance + relevance 가중합(가중치 모두 1, min-max 정규화). recency는 마지막 검색 이후 게임 시간에 대한 지수 감쇠(감쇠율 0.995). importance는 생성 시 LLM이 1~10점 부여. relevance는 임베딩 코사인 유사도. reflection은 최근 사건들의 importance 합이 임계치(150)를 넘으면 발동, 최근 100개 기억을 읽고 질문 3개를 만들어 검색 → 근거 기억을 인용하는 통찰을 생성. 성찰이 성찰을 인용해 트리를 이룬다.
- 핵심 수치: 에이전트는 하루 2~3회 reflection. TrueSkill μ: 전체 아키텍처 29.89 > 성찰 제거 26.88 > 성찰+계획 제거 25.64 > 인간 크라우드워커 22.95 > 관찰+성찰+계획 제거 21.21 (Kruskal-Wallis H(4)=150.29, p<0.001). 전체 vs 완전 ablation Cohen's d = 8.16.
- 인용할 만한 문장:
  > "we generate reflections when the sum of the importance scores for the latest events perceived by the agents exceeds a threshold (150 in our implementation)." (§4.2 Reflection)
  > "Each additional ablation reduces the performance of the architecture." (§6 Evaluation)
- 책 관련성: LLM Wiki의 "답변을 다시 wiki에 저장"과 "요약 페이지 생성"의 이론적 선조가 reflection이다. 또 원본 기록(memory stream = raw sources)과 합성된 통찰(reflection = wiki page)을 분리하는 설계 자체가 이 논문에서 왔다. recency/importance/relevance 3축은 wiki의 "최근 수정/중요도/관련성" 메타데이터 설계에 직접 쓸 수 있다.
- 독자 전달: "일기(raw) → 주간 회고(reflection)" 비유. 점수식은 가중합 한 줄만 보여 주고 감쇠율 0.995는 "하루 지나면 0.995^24 ≈ 0.89"로 체감시킨다.
- 재현성: 코드 공개(joonspk-research/generative_agents).

### 논문 1-3: MemGPT: Towards LLMs as Operating Systems (seminal → Letta)
- 저자·연도: Charles Packer, Sarah Wooders, Kevin Lin 외 (7인), 2023 (v2 2024-02)
- 발표처: arXiv 프리프린트(학회 게재 미확인). 이후 Letta 제품으로 발전.
- arXiv ID: 2310.08560
- 피인용수: 1,572
- 요약: OS의 가상 메모리에서 영감을 받아 LLM이 자기 컨텍스트를 스스로 페이징하는 **virtual context management**를 제안. 메모리 계층은 main context(시스템 지시·working context·FIFO 큐)와 external context(recall storage=메시지 DB, archival storage=임의 길이 텍스트 읽기/쓰기 DB). LLM이 함수 호출로 계층 간 데이터를 옮기고, 인터럽트로 제어 흐름을 관리한다.
- 방법론 요약: 다세션 대화(Deep Memory Retrieval, DMR)와 문서 분석(NaturalQuestions-Open 50문항, 중첩 key-value 검색)으로 고정 컨텍스트 베이스라인과 비교.
- 핵심 수치 (DMR 정확도 / ROUGE-L R): GPT-3.5 Turbo 단독 38.7% / 0.394 → MemGPT 66.9% / 0.629. GPT-4 단독 32.1% → MemGPT 92.5%. GPT-4 Turbo 단독 35.3% → MemGPT 93.4%. 중첩 KV 검색: GPT-3.5는 1단계 중첩에서 0%, GPT-4·GPT-4 Turbo는 3단계에서 0%, MemGPT(GPT-4)는 중첩 수에 무관. 문서 QA: 고정 컨텍스트 베이스라인은 "retriever 성능에 상한이 걸림", 문서를 잘라 넣을수록(압축) 정확도 하락.
- 인용할 만한 문장:
  > "MemGPT significantly outperforms the fixed-context baselines." (§4.1)
  > "MemGPT's performance is unaffected by increased context length." (Figure 5 caption)
- 책 관련성: "컨텍스트에 뭘 둘지 LLM이 스스로 결정한다"는 에이전틱 메모리의 원형. LLM Wiki에서 index.md = working context, 페이지들 = archival storage, log.md = recall storage로 대응시킬 수 있다.
- 독자 전달: RAM/디스크/스왑 비유 — 개발자 독자에게 가장 직관적.
- 재현성: 코드 공개(letta-ai/letta, 구 cpacker/MemGPT).

### 논문 1-4: A-MEM: Agentic Memory for LLM Agents
- 저자·연도: Wujiang Xu, Zujie Liang, Kai Mei 외 (6인), 2025 (v11 2025-10-08)
- 발표처: NeurIPS 2025 (arXiv 코멘트로 확인)
- arXiv ID: 2502.12110
- 피인용수: 1,172
- 요약: **Zettelkasten** 원리를 LLM 메모리에 적용. 새 기억이 들어오면 구조화된 노트(내용·타임스탬프·키워드·태그·문맥 설명·임베딩·링크)를 생성하고, 기존 노트와의 연결을 LLM이 판단해 링크를 만들며, 연결된 기존 노트의 문맥·태그를 갱신하는 **memory evolution**을 수행한다. 6개 기반 모델에서 SOTA 대비 우위.
- 방법론 요약: 노트 m_i = {c_i, t_i, K_i, G_i, X_i, e_i, L_i}. 링크 생성 = 임베딩 코사인 top-k 후보 → LLM이 연결 여부 결정. 진화 = 각 이웃 노트에 대해 LLM이 문맥·태그 갱신 여부 결정 후 교체. LoCoMo·DialSim 벤치마크.
- 핵심 수치 (LoCoMo, GPT-4o-mini, F1/BLEU-1 %): A-MEM Temporal 45.85/36.67 vs MemGPT 25.52/19.44 vs LoCoMo 18.41/14.77; Single-hop 44.65 vs MemGPT 41.04; Multi-hop 27.02 vs MemGPT 26.65(차이 작음). Adversarial은 LoCoMo 베이스라인(69.23)이 더 높음. 토큰: 본문은 "약 1,200 토큰/연산, 85~93% 절감"이라 쓰지만 표의 GPT-4o-mini 행은 2,520 토큰(GPT-4o 1,216; LoCoMo·MemGPT ≈ 16,900) — 인용 시 "최대 약 93% 절감" 정도로 보수적으로.
- 인용할 만한 문장:
  > "Following the basic principles of the Zettelkasten method, we designed our memory system to create interconnected knowledge networks through dynamic indexing and linking." (Abstract)
  > "as new memories are integrated, they can trigger updates to the contextual representations and attributes of existing historical memories" (Abstract)
- 책 관련성: LLM Wiki의 "소스 1건이 10~15페이지를 건드린다"는 ingest 동작이 바로 memory evolution이다. 백링크·태그·한 줄 문맥 설명을 노트에 넣는 설계의 학술 근거. "multi-hop에서 2배" 주장은 표와 어긋나므로 책에서 쓰지 말 것.
- 독자 전달: Zettelkasten 카드 상자 비유. "새 카드를 꽂을 때 옆 카드의 메모도 고쳐 쓴다".
- 재현성: 코드 공개(WujiangXu/A-mem, A-mem-sys).

### 논문 1-5: Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory
- 저자·연도: Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, Deshraj Yadav, 2025
- 발표처: ECAI 2025 (S2 표기; arXiv 코멘트 없음 → 트랙 미확인)
- arXiv ID: 2504.19413
- 피인용수: 770
- 요약: 대화에서 핵심 정보를 추출·통합·검색하는 메모리 아키텍처와, 관계를 그래프로 저장하는 변형(Mem0^g). LOCOMO에서 6종 베이스라인(메모리 시스템, 청크 크기/k를 바꾼 RAG, full-context, 오픈소스 메모리, 독점 모델, 메모리 플랫폼)과 비교.
- 핵심 수치: LLM-as-a-Judge 기준 OpenAI 메모리 대비 26% 상대 개선. 그래프 메모리는 기본 대비 약 2% 추가. full-context 대비 p95 지연 91% 감소, 토큰 비용 90% 이상 절감.
- 인용할 만한 문장:
  > "Mem0 attains a 91% lower p95 latency and saves more than 90% token cost" (Abstract)
- 책 관련성: "그래프를 붙이면 얼마나 좋아지나?" — 약 2%. 즉 그래프 자체보다 **추출·통합·갱신 루프**가 효과의 대부분이라는 실무적 메시지. LLM Wiki가 그래프 DB 없이 markdown+링크로 시작해도 되는 근거.
- 주의: 벤더(Mem0) 자체 평가. 중립 재현은 미확인.
- 재현성: mem0ai/mem0 오픈소스.

### 논문 1-6: Zep: A Temporal Knowledge Graph Architecture for Agent Memory
- 저자·연도: Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, Daniel Chalef, 2025
- 발표처: arXiv 프리프린트(학회 미확인)
- arXiv ID: 2501.13956
- 피인용수: 411
- 요약: Graphiti 엔진으로 대화·업무 데이터를 **시간 인식 지식 그래프**로 합성. 각 사실(edge)은 4개 타임스탬프(t_created, t_expired = 시스템 시간; t_valid, t_invalid = 사실이 참이었던 기간)를 가진다. 새 edge가 기존 edge와 모순되면 기존 edge의 t_invalid를 새 edge의 t_valid로 설정해 **무효화**(삭제가 아님).
- 핵심 수치: DMR 94.8%(gpt-4-turbo) vs MemGPT 93.4%; gpt-4o-mini로는 98.2%. LongMemEval: gpt-4o-mini 63.8% vs full-context 55.4%, gpt-4o 71.2% vs 60.2% (최대 18.5% 개선); 지연 3.20s vs 31.3s(gpt-4o-mini), 2.58s vs 28.9s(gpt-4o) → 약 90% 감소.
- 인용할 만한 문장:
  > "it invalidates the affected edges by setting their t_invalid to the t_valid of the invalidating edge." (§2 Graphiti, edge invalidation)
- 책 관련성: 3장(지식 유지보수)의 "as-of 사실" 모델. wiki 페이지의 사실 줄에 `valid_from / valid_to` 메타를 두고, 모순 시 덮어쓰지 않고 만료 처리하는 패턴의 직접 근거.
- 주의: 벤더(Zep) 자체 평가.
- 재현성: getzep/graphiti 오픈소스.

### 논문 1-7: RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval
- 저자·연도: Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, Christopher D. Manning, 2024
- 발표처: ICLR 2024 (S2 표기; arXiv 코멘트 없음)
- arXiv ID: 2401.18059
- 피인용수: 783
- 요약: 청크를 임베딩 → 클러스터링 → 요약을 재귀적으로 반복해 **아래에서 위로 요약 트리**를 만들고, 질의 시 여러 추상화 수준에서 동시에 검색한다. 짧은 연속 청크만 검색하는 기존 RAG의 "전체 맥락 부재"를 해결.
- 방법론 요약: 트리 순회(tree traversal) vs 전 계층을 평탄화해 검색하는 collapsed tree 비교 → collapsed tree 채택(2,000토큰 상한).
- 핵심 수치: QuALITY: RAPTOR+GPT-4 82.6% (이전 최고 62.3%), HARD 76.2% (CoLISA 54.7%). QASPER F1 55.7% (CoLT5 XL 53.9%). NarrativeQA METEOR 19.1 (vs 10.6). 검색된 노드의 18.5%~57%가 비-리프(요약) 노드.
- 인용할 만한 문장:
  > "RAPTOR paired with GPT-4 sets a new state-of-the-art with an accuracy of 82.6%, surpassing the previous best result of 62.3%." (§5 Results, QuALITY)
  > "We observe that between 18.5% to 57% of the retrieved nodes come from non-leaf nodes." (§5, Contribution of the tree structure)
  > "The collapsed tree approach consistently performs better." (§5)
- 책 관련성: LLM Wiki의 "소스 요약 페이지 → 개념 페이지 → 개요(overview) 페이지"가 곧 RAPTOR의 수동/의미 기반 요약 트리다. "요약 노드가 실제로 검색된다(최대 57%)"는 수치가 요약 페이지를 유지할 가치의 근거.
- 독자 전달: 파일 트리 비유 — "README가 있는 폴더가 검색이 잘 된다".
- 재현성: 코드 공개(parthsarthi03/raptor).

### 논문 1-8: From Local to Global: A Graph RAG Approach to Query-Focused Summarization (GraphRAG)
- 저자·연도: Darren Edge, Ha Trinh, Newman Cheng 외 (10인, Microsoft Research), 2024 (v2 2025-02-19)
- 발표처: arXiv 프리프린트(학회 미확인)
- arXiv ID: 2404.16130
- 피인용수: 2,323
- 요약: "이 데이터셋의 주요 주제는?" 같은 **전역(global) 질문**은 검색이 아니라 query-focused summarization 문제라서 vector RAG가 실패한다. LLM으로 엔티티 지식 그래프를 뽑고, 커뮤니티(밀접한 엔티티 묶음)마다 요약을 미리 생성해 두었다가, 질의 시 커뮤니티 요약별 부분 답변을 만들고 다시 합친다.
- 방법론 요약: 팟캐스트(1,669청크×600토큰 ≈ 100만 토큰)·뉴스(3,197청크 ≈ 170만 토큰) 코퍼스. 커뮤니티 수준 C0(루트)~C3(리프), 소스 텍스트 요약(TS), vector RAG(SS) 비교. LLM-as-judge 승률(comprehensiveness·diversity·empowerment·directness).
- 핵심 수치: 전역 접근의 comprehensiveness 승률 72~83%(팟캐스트, p<.001), 72~80%(뉴스); diversity 75~82%(팟캐스트), 62~71%(뉴스). 루트 요약 C0는 vector RAG 대비 comprehensiveness 72%, diversity 62%를 유지하면서 질의당 토큰이 9~43배 적음(팟캐스트 C0 26,657토큰 = TS의 2.6%). 그래프 크기: 팟캐스트 8,564 노드/20,691 엣지, 인덱싱 281분. 답변당 평균 주장 수: C0 34.18(뉴스) vs SS 25.23.
- 인용할 만한 문장:
  > "RAG fails on global questions directed at an entire text corpus, such as 'What are the main themes in the dataset?'" (Abstract)
  > "Root-level community summaries (C0) require dramatically fewer tokens per query (9x-43x)." (§3 Results)
  > "the ability to provide specific examples, quotes, and citations was judged to be key to helping users reach an informed understanding." (§3, Empowerment)
- 책 관련성: wiki의 overview/개념 페이지 = 커뮤니티 요약. "전역 질문에는 상위 요약, 세부 질문에는 하위 페이지" 라우팅의 근거. 인덱싱 비용(281분, 100만 토큰 코퍼스)은 "그래프를 전부 다시 만들지 말고 증분 ingest 하라"는 LLM Wiki 주장의 반대편 근거로 쓸 수 있다.
- 주의: 평가는 LLM-as-judge. directness에서는 vector RAG가 우세(논문 명시).
- 재현성: microsoft/graphrag 오픈소스.

### 논문 1-9: LightRAG: Simple and Fast Retrieval-Augmented Generation
- 저자·연도: Zirui Guo, Lianghao Xia, Yanhua Yu, Tuantuan Ao, Chao Huang, 2024 (v3 2025-04-28)
- 발표처: EMNLP (S2 표기; 연도·트랙 미확인)
- arXiv ID: 2410.05779
- 피인용수: 532
- 요약: 그래프 구조를 인덱싱·검색에 넣되 커뮤니티 요약 없이 **low-level(엔티티)·high-level(주제) 이중 검색**과 **증분 업데이트 알고리즘**을 제공. GraphRAG의 비용 문제를 겨냥.
- 핵심 수치: 초록에 구체 수치 없음(본문 승률 표는 미추출). 인용 시 "GraphRAG 대비 검색 효율·증분 갱신" 정성 주장으로만.
- 인용할 만한 문장:
  > "an incremental update algorithm that ensures the timely integration of new data, allowing the system to remain effective and responsive in rapidly changing data environments." (Abstract)
- 책 관련성: "증분 ingest가 가능한 그래프"의 오픈소스 사례. LLM Wiki의 ingest-one-source-at-a-time 원칙과 같은 방향.
- 재현성: HKUDS/LightRAG 오픈소스.

### 논문 1-10: HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models
- 저자·연도: Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, Yu Su, 2024
- 발표처: NeurIPS 2024 (arXiv 코멘트로 확인)
- arXiv ID: 2405.14831
- 피인용수: 398
- 요약: 해마 인덱싱 이론을 본떠 LLM(신피질)·지식 그래프(해마 인덱스)·Personalized PageRank(패턴 완성)를 결합. 단일 검색 단계로 다단계(multi-hop) QA에서 반복 검색(IRCoT)과 맞먹는다.
- 핵심 수치: multi-hop QA에서 SOTA 대비 최대 20% 향상. 단일 검색이 IRCoT와 비슷하거나 나으면서 10~30배 저렴, 6~13배 빠름. IRCoT와 결합 시 추가 향상.
- 인용할 만한 문장:
  > "Single-step retrieval with HippoRAG achieves comparable or better performance than iterative retrieval like IRCoT while being 10-30 times cheaper and 6-13 times faster" (Abstract)
- 책 관련성: 링크 구조(백링크)를 따라 PageRank를 돌리면 반복 검색 없이도 연관 페이지를 찾는다 — wiki의 링크 그래프가 "싸고 빠른 multi-hop"의 자산이라는 근거.
- 재현성: OSU-NLP-Group/HippoRAG 공개.

### 논문 1-11: Dense X Retrieval: What Retrieval Granularity Should We Use?
- 저자·연도: Tong Chen, Hongwei Wang, Sihao Chen 외 (8인), 2023 (v3 2024-10)
- 발표처: EMNLP (S2 표기; 2024 추정, 미확인)
- arXiv ID: 2312.06648
- 피인용수: 161
- 요약: 검색 단위를 문서/단락/문장이 아닌 **proposition**(문맥이 자족적인 원자 사실 한 줄, 대명사 해소 포함)으로 바꾸면 검색·QA 모두 좋아진다. 영어 위키 600만 페이지를 4,100만 단락·1억 1,400만 문장·2억 5,700만 proposition으로 분해한 FactoidWiki 공개.
- 핵심 수치: proposition 평균 11.2단어 vs 단락 58.5단어. Recall@20 평균 +10.1(비지도 dense retriever), +2.7(지도). Recall@5 상대 개선 35.0%(SimCSE), 22.5%(Contriever). 미학습 데이터셋에서 이득이 가장 큼(EntityQuestions DPR 약 25% 상대). 다운스트림 EM(LLaMA-2-7B, 500토큰 예산) +2.7~+4.1.
- 인용할 만한 문장:
  > "Propositions are defined as atomic expressions within text, each encapsulating a distinct factoid and presented in a concise, self-contained natural language format." (Abstract)
  > "Retrieval by proposition-level index achieves the highest average exact match (EM) on all four retriever models." (§5.2)
- 책 관련성: "구조화 노트 vs 평탄 청크" 질문의 정량 답. wiki 페이지의 bullet 한 줄을 proposition처럼 쓰면(주어 명시·자족적) 검색이 좋아진다는 작성 규약의 근거.
- 재현성: FactoidWiki·코드 공개(chentong0/factoid-wiki).

### 논문 1-12: Is Semantic Chunking Worth the Computational Cost?
- 저자·연도: Renyi Qu, Ruixuan Tu, Forrest Bao, 2024
- 발표처: arXiv 프리프린트
- arXiv ID: 2410.13070
- 피인용수: 75
- 요약: 문서 검색·근거 검색·답변 생성 3과제에서 의미 기반 청킹이 고정 크기 청킹보다 일관되게 낫지 않으며 비용은 더 든다.
- 핵심 수치: 초록에 수치 없음("consistent performance gains" 부재라는 정성 결론).
- 인용할 만한 문장:
  > "the computational costs associated with semantic chunking are not justified by consistent performance gains." (Abstract)
- 책 관련성: "청킹을 더 똑똑하게"보다 "LLM이 쓴 페이지(이미 의미 단위)"가 답이라는 LLM Wiki의 전제를 간접 지지. 반대로, wiki가 없다면 고정 청킹으로 시작해도 손해가 아니라는 실무 팁.

---

## 2. 에이전틱 검색 vs 고전 RAG (반복 검색·자기 반성·long context 논쟁)

### 논문 2-1: Retrieval-Augmented Generation for Large Language Models: A Survey (서베이)
- 저자·연도: Yunfan Gao, Yun Xiong, Xinyu Gao 외 (10인), 2023 (v5 2024-03)
- 발표처: arXiv (Ongoing Work; 학회 미확인)
- arXiv ID: 2312.10997
- 피인용수: 4,260
- 요약: RAG를 Naive → Advanced → Modular 3단계 패러다임으로 정리하고, 검색·생성·증강 3요소별 기법과 평가 프레임워크를 집대성. RAG 입문 인용의 표준.
- 인용할 만한 문장:
  > "Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes." (Abstract)
- 책 관련성: 2장 도입부에서 "고전 RAG"를 정의할 때 인용. Modular RAG의 라우팅·반복 모듈이 에이전틱 검색으로 가는 다리.

### 논문 2-2: Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG (서베이)
- 저자·연도: Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, 2025 (v4 2026-04-01)
- 발표처: arXiv 프리프린트
- arXiv ID: 2501.09136
- 피인용수: 444
- 요약: RAG 파이프라인에 에이전트(reflection·planning·tool use·multi-agent)를 넣은 Agentic RAG의 분류 체계(에이전트 수·제어 구조·자율성·지식 표현)와 설계 트레이드오프, 평가·조율·메모리 관리·거버넌스의 열린 문제를 정리.
- 인용할 만한 문장:
  > "traditional RAG systems are constrained by static workflows and lack the adaptability required for multi-step reasoning and complex task management." (Abstract)
- 책 관련성: "LLM이 index를 읽고 파일을 열어 보며 답한다"는 LLM Wiki의 query 방식이 Agentic RAG 분류 어디에 놓이는지(단일 에이전트·순차·높은 자율성·텍스트 지식 표현) 설명할 때.

### 논문 2-3: ReAct: Synergizing Reasoning and Acting in Language Models (seminal)
- 저자·연도: Shunyu Yao, Jeffrey Zhao, Dian Yu 외 (7인), 2022 (ICLR 2023 camera-ready v3 2023-03)
- 발표처: ICLR 2023 (arXiv 코멘트로 확인)
- arXiv ID: 2210.03629
- 피인용수: 12,364
- 요약: 추론 트레이스와 행동(도구 호출)을 교차 생성. HotpotQA·FEVER에서 단순 Wikipedia API와 상호작용해 CoT의 환각·오류 전파를 줄였고, ALFWorld·WebShop에서 모방/강화학습 대비 성공률 +34%·+10% 절대 향상.
- 인용할 만한 문장:
  > "ReAct overcomes issues of hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a simple Wikipedia API" (Abstract)
- 책 관련성: 사내 에이전트가 `grep`·`read file`·`follow link`를 번갈아 호출하며 wiki를 탐색하는 루프의 원형. "Wikipedia API"를 "사내 wiki 파일 시스템"으로 치환하면 그대로 책의 아키텍처.
- 재현성: 코드 공개(react-lm.github.io).

### 논문 2-4: Interleaving Retrieval with Chain-of-Thought Reasoning (IRCoT)
- 저자·연도: Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, Ashish Sabharwal, 2022 (ACL 2023)
- 발표처: ACL 2023 (arXiv 코멘트로 확인)
- arXiv ID: 2212.10509
- 피인용수: 1,395
- 요약: 다단계 질문에서 "무엇을 검색할지"는 "지금까지 무엇을 도출했는지"에 의존하므로, 한 번 검색-읽기는 부족하다. CoT 문장마다 검색을 끼워 넣는다.
- 핵심 수치: GPT-3로 검색 최대 +21점, 다운스트림 QA 최대 +15점(HotpotQA·2WikiMultihopQA·MuSiQue·IIRC). Flan-T5-large 등 소형 모델·OOD에서도 유사 이득. 환각 감소.
- 인용할 만한 문장:
  > "what to retrieve depends on what has already been derived, which in turn may depend on what was previously retrieved." (Abstract)
- 책 관련성: "질문 한 번에 top-k 한 번"이 왜 사내 Q&A에서 자주 틀리는지 설명. wiki 링크를 따라가며 재검색하는 것이 IRCoT의 수동 구현.
- 재현성: 코드·프롬프트 공개(stonybrooknlp/ircot).

### 논문 2-5: Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
- 저자·연도: Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, Hannaneh Hajishirzi, 2023
- 발표처: ICLR 2024 (S2 표기; arXiv 코멘트 없음)
- arXiv ID: 2310.11511
- 피인용수: 2,809
- 요약: 검색이 필요한지, 검색 결과가 관련 있는지, 생성이 근거에 지지되는지, 유용한지를 **reflection token**(Retrieve / IsRel / IsSup / IsUse) 4종으로 모델이 스스로 판단하도록 학습. 7B/13B가 ChatGPT·검색 증강 Llama2-chat을 여러 과제에서 앞섬.
- 핵심 수치 (Table 2): PopQA 정확도 Self-RAG 7B 54.9 / 13B 55.8 vs ChatGPT 29.3, Ret-ChatGPT 50.8, Ret-Llama2-chat 13B 51.8. PubHealth 72.4 / 74.5 vs ChatGPT 70.1. ASQA 인용 정밀도/재현율 Self-RAG 13B 70.3/71.3 vs Ret-ChatGPT 65.1/76.6.
- 인용할 만한 문장:
  > "indiscriminately retrieving and incorporating a fixed number of retrieved passages, regardless of whether retrieval is necessary, or passages are relevant, diminishes LM versatility or can lead to unhelpful response generation." (Abstract)
- 책 관련성: "검색할지 말지, 읽은 페이지가 답에 쓸모 있는지"를 명시적 판정으로 둔다는 설계. 사내 에이전트의 시스템 프롬프트에 IsRel/IsSup 판정을 흉내 내는 체크 단계를 넣는 근거.
- 재현성: 코드·모델 공개(AkariAsai/self-rag).

### 논문 2-6: Corrective Retrieval Augmented Generation (CRAG)
- 저자·연도: Shi-Qi Yan, Jia-Chen Gu, Yun Zhu, Zhen-Hua Ling, 2024 (v3 2024-10)
- 발표처: arXiv 프리프린트(학회 미확인)
- arXiv ID: 2401.15884
- 피인용수: 325
- 요약: 경량 retrieval evaluator(T5-large, 0.77B)가 검색 결과 품질을 점수화해 **Correct / Incorrect / Ambiguous** 3행동을 분기. Incorrect면 웹 검색으로 보강, 문서는 decompose-then-recompose로 핵심만 남긴다. 플러그인 방식.
- 핵심 수치: 임계치(상/하) PopQA 0.59/−0.99, PubHealth 0.5/−0.91, Biography 0.95/−0.91. CRAG가 RAG 대비(SelfRAG-LLaMA2-7b 생성기) PopQA +7.0, Biography(FactScore) +14.9, PubHealth +36.6, Arc-Challenge +15.4. Self-CRAG vs Self-RAG(LLaMA2-hf-7b) PopQA +20.0, Biography +36.9 (계산값; PubHealth −0.1, 일부 역전 있음).
- 인용할 만한 문장:
  > "a lightweight retrieval evaluator is designed to assess the overall quality of retrieved documents for a query, returning a confidence degree based on which different knowledge retrieval actions can be triggered." (Abstract)
- 책 관련성: lint의 "데이터 공백 → 웹 검색으로 채우기"와 query 시 "wiki에 없으면 없다고 말하기"의 판정 구조. 작은 평가기 하나로 분기한다는 점이 실무 친화적.
- 재현성: 코드 공개(HuskyInSalt/CRAG).

### 논문 2-7: Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning
- 저자·연도: Bowen Jin, Hansi Zeng, Zhenrui Yue 외 (8인), 2025 (v5 2025-08)
- 발표처: arXiv 프리프린트(학회 미확인)
- arXiv ID: 2503.09516
- 피인용수: 1,587
- 요약: 추론 중 `<search>` 질의를 여러 번 생성하고 `<information>`으로 결과를 받는 다회차 검색을 RL(PPO/GRPO)로 학습. 검색된 토큰은 loss에서 마스킹, 보상은 정답 EM만.
- 핵심 수치: 7개 QA 데이터셋(NQ, TriviaQA, PopQA, HotpotQA, 2Wiki, Musique, Bamboogle). RAG 베이스라인 대비 상대 개선 — **버전 간 불일치 주의**: arXiv API 초록(v5)은 41%(Qwen2.5-7B)·20%(3B), HTML 본문 초록은 24%·20%, 서론은 41%·20%. 인용 시 "20~41% 상대 개선(버전에 따라 상이)"로. 마스킹 ablation: 평균 EM 0.431 vs 0.343.
- 인용할 만한 문장:
  > "Prompting advanced LLMs with reasoning capabilities to use search engines during inference is often suboptimal, as the LLM might not fully possess the capability on how to interact optimally with the search engine." (Abstract)
- 책 관련성: "검색을 잘하는 것도 학습 대상"이라는 메시지. 사내 wiki를 뒤지는 Claude 에이전트는 학습 대신 schema(CLAUDE.md)의 검색 규약으로 같은 효과를 노린다는 대비 구도.
- 재현성: 코드·체크포인트 공개(PeterGriffinJin/Search-R1).

### 논문 2-8: Lost in the Middle: How Language Models Use Long Contexts (seminal)
- 저자·연도: Nelson F. Liu, Kevin Lin, John Hewitt 외 (7인), 2023
- 발표처: TACL 2023 (arXiv 코멘트로 확인)
- arXiv ID: 2307.03172
- 피인용수: 5,438
- 요약: 다문서 QA(NaturalQuestions-Open 2,655문항, 100토큰 위키 단락 10/20/30개 중 정답 문서 1개)와 key-value 검색에서, 관련 정보가 입력의 **처음·끝**에 있을 때 성능이 가장 높고 **중간**이면 크게 떨어지는 U자 곡선. 확장 컨텍스트 모델도 마찬가지.
- 핵심 수치: GPT-3.5-Turbo closed-book 56.1%, oracle 88.3%. 20문서 설정: 정답이 맨 앞 75.8%, 중간(index 9) 53.8%, 맨 끝 63.2% (계산값, 부록 표). 중간일 때 closed-book보다 낮음. 논문 본문: "performance can drop by more than 20%". 검색 문서를 20→50개로 늘려도 정확도 +1.5%(GPT-3.5)·+1%(Claude-1.3)에 그침. GPT-3.5-Turbo vs 16K 변형: 입력이 둘 다 들어가면 성능 거의 동일. KV 검색: Claude-1.3은 거의 완벽, GPT-3.5·MPT-30B는 중간에서 최악; query-aware contextualization 없으면 최악 45.6%.
- 인용할 만한 문장:
  > "performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models." (Abstract)
  > "Using more than 20 retrieved documents only marginally improves reader performance." (§5)
- 책 관련성: "많이 넣을수록 좋다"의 반례. wiki 답변 시 관련 페이지 몇 개만 골라 앞쪽에 배치하라는 실무 규칙의 근거. 2023년 모델 기준이라는 신선도 한계를 명시하고, 2025년 후속(NoLiMa·Context Rot)과 함께 인용.
- 재현성: 코드·데이터 공개(nelson-liu/lost-in-the-middle).

### 논문 2-9: Same Task, More Tokens: the Impact of Input Length on the Reasoning Performance of LLMs
- 저자·연도: Mosh Levy, Alon Jacoby, Yoav Goldberg, 2024
- 발표처: ACL 2024 (arXiv 코멘트로 확인)
- arXiv ID: 2402.14848
- 피인용수: 256
- 요약: 같은 문제를 패딩 길이·종류·위치만 바꿔 여러 버전으로 만들어(FLenQA) 입력 길이 효과만 분리. 기술적 최대치보다 훨씬 짧은 길이에서 추론 성능이 떨어진다.
- 핵심 수치: 테스트 길이 약 250/500/1,000/2,000/3,000 토큰. 500토큰을 넘으면서 유의한 하락. 전체 평균 정확도 0.92 → 0.68(3,000토큰). 다음 단어 예측 정확도와 추론 정확도의 Pearson ρ = −0.95 (p=0.01) → perplexity는 긴 입력 성능의 대리 지표가 못 됨.
- 인용할 만한 문장:
  > "a notable degradation in LLMs' reasoning performance at much shorter input lengths than their technical maximum." (Abstract)
  > "measuring next word prediction and, similarly, perplexity, cannot substitute downstream task evaluation on long inputs." (§5)
- 책 관련성: 수천 토큰 수준에서도 하락한다는 점 — wiki 페이지를 짧고 밀도 있게 유지하라는 근거.
- 재현성: 데이터셋 공개(FLenQA).

### 논문 2-10: RULER: What's the Real Context Size of Your Long-Context Language Models?
- 저자·연도: Cheng-Ping Hsieh, Simeng Sun, Samuel Kriman 외 (8인, NVIDIA), 2024
- 발표처: COLM 2024 (arXiv 코멘트로 확인)
- arXiv ID: 2404.06654
- 피인용수: 1,452
- 요약: 단순 needle-in-a-haystack을 넘어 다중 needle·multi-hop tracing·aggregation 등 13과제로 17개 long-context 모델 평가. NIAH는 거의 만점이어도 길이가 늘면 거의 모든 모델이 크게 하락.
- 핵심 수치: 17 모델 × 13 과제. 32K 이상을 표방한 모델 중 32K에서 "만족스러운" 성능 유지는 절반.
- 인용할 만한 문장:
  > "While these models all claim context sizes of 32K tokens or greater, only half of them can maintain satisfactory performance at the length of 32K." (Abstract)
- 책 관련성: "표기 컨텍스트 ≠ 유효 컨텍스트". wiki 답변 컨텍스트 예산을 보수적으로 잡는 근거.
- 재현성: 코드 공개(hsiehjackson/RULER).

### 논문 2-11: NoLiMa: Long-Context Evaluation Beyond Literal Matching
- 저자·연도: Ali Modarressi, Hanieh Deilamsalehy, Franck Dernoncourt 외 (7인), 2025
- 발표처: ICML 2025 (arXiv 코멘트로 확인)
- arXiv ID: 2502.05167
- 피인용수: 147
- 요약: needle과 질문의 어휘 중복을 최소화해 "문자열 매칭"이 아닌 연상 추론을 요구. 128K 이상을 표방한 13개 모델이 <1K에선 잘하다가 길이가 늘면 급락.
- 핵심 수치: 32K에서 13개 중 11개가 짧은 길이 기준의 50% 미만. GPT-4o 99.3% → 69.7%(32K). 유효 길이(기준의 85% 유지) 대부분 ≤2K, GPT-4o 8K. Llama 3.1 70B: 표방 128K, 유효 2K, 32K에서 42.7%.
- 인용할 만한 문장:
  > "At 32K, for instance, 11 models drop below 50% of their strong short-length baselines." (Abstract)
  > "Even models with base scores exceeding 90.0% exhibit a significantly shorter effective length than their claimed lengths." (§4)
- 책 관련성: 2025년 최신 모델에서도 long-context가 "의미 연상"에는 약하다는 증거. wiki가 질문 언어와 페이지 언어를 맞춰 주는(용어 정규화·동의어 페이지) 가치의 근거.
- 재현성: 데이터·코드 공개(adobe-research/NoLiMa).

### 논문 2-12: Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach
- 저자·연도: Zhuowan Li, Cheng Li, Mingyang Zhang, Qiaozhu Mei, Michael Bendersky (Google DeepMind), 2024
- 발표처: EMNLP 2024 Industry Track (arXiv 코멘트로 확인)
- arXiv ID: 2407.16833
- 피인용수: 193
- 요약: 자원이 충분하면 long-context(LC)가 RAG보다 평균 성능이 높지만 RAG는 훨씬 싸다. 모델 자기 반성으로 RAG/LC를 라우팅하는 **Self-Route** 제안 — LC와 비슷한 성능에 비용 대폭 절감.
- 핵심 수치: LC가 RAG를 평균 7.6%(Gemini-1.5-Pro), 13.1%(GPT-4O), 3.6%(GPT-3.5-Turbo) 앞섬. Self-Route 비용 65%(Gemini-1.5-Pro)·39%(GPT-4O) 절감, 성능 차 −0.2%(GPT-4O)·−2.2%(Gemini)·+1.7%(GPT-3.5). RAG 실패 유형은 4개 범주(A~D)+기타 — "7가지"가 아님.
- 인용할 만한 문장:
  > "when resourced sufficiently, LC consistently outperforms RAG in terms of average performance. However, RAG's significantly lower cost remains a distinct advantage." (Abstract)
- 책 관련성: "둘 중 하나"가 아니라 라우팅. LLM Wiki에서는 index.md 읽기(싼 경로)와 소스 원문 전체 읽기(비싼 경로)를 LLM이 고르는 것이 Self-Route의 실무판.

---

## 3. 지식 유지보수 (편집·모순 탐지·시간 지식·낡은 사실·중복)

### 논문 3-1: Knowledge Conflicts for LLMs: A Survey (서베이)
- 저자·연도: Rongwu Xu, Zehan Qi, Zhijiang Guo 외 (7인), 2024
- 발표처: EMNLP 2024 (S2 표기; arXiv 코멘트 없음)
- arXiv ID: 2403.08319
- 피인용수: 376
- 요약: 지식 충돌을 **context-memory**(검색 결과 vs 모델 파라미터), **inter-context**(검색 결과끼리), **intra-memory**(모델 내부) 3범주로 분류하고 원인·행동·해법을 정리.
- 인용할 만한 문장:
  > "Our focus is on three categories of knowledge conflicts: context-memory, inter-context, and intra-memory conflict." (Abstract)
- 책 관련성: lint의 "모순 탐지"는 inter-context 충돌을 사전에 wiki 안에서 해소하는 작업이라고 위치시킬 수 있다. 3범주 용어를 책의 분류로 차용.
- 재현성: GitHub 문헌 저장소(pillowsofwind/Knowledge-Conflicts-Survey).

### 논문 3-2: Adaptive Chameleon or Stubborn Sloth: Revealing the Behavior of LLMs in Knowledge Conflicts
- 저자·연도: Jian Xie, Kai Zhang, Jiangjie Chen, Renze Lou, Yu Su, 2023
- 발표처: ICLR 2024 Spotlight (arXiv 코멘트로 확인)
- arXiv ID: 2305.13300
- 피인용수: 428
- 요약: 모델의 파라메트릭 기억을 유도한 뒤 그와 모순되는 counter-memory를 만들어 통제 실험. (1) 외부 증거가 **일관되고 설득력 있으면** 모델은 기억과 달라도 잘 받아들인다. (2) 그러나 증거가 섞여 있으면 자기 기억과 일치하는 쪽을 고르는 **확증 편향**이 강하다. 증거의 순서·수·인기도도 영향.
- 핵심 수치: PopQA에서 기억 일치 증거 비율 0/2 → 2/2일 때 ChatGPT의 기억 채택률 3.7% → 99.8%, Llama2-7B 2.6% → 91.7%. 순서 효과: GPT-4만 안정, PaLM2·Llama2-7B는 30% 이상 변동. 무관한 단락 1개만 주면 Llama2-7B는 92.4%가 그 내용으로 답변. counter-answer만 주면 18.8% 채택 vs 전체 counter-memory 56.7%.
- 인용할 만한 문장:
  > "LLMs can be highly receptive to external evidence even when that conflicts with their parametric memory, given that the external evidence is coherent and convincing." (Abstract)
  > "LLMs also demonstrate a strong confirmation bias when the external evidence contains some information that is consistent with their parametric memory" (Abstract)
- 책 관련성: wiki에 모순된 두 페이지가 공존하면 모델은 자기 사전 지식에 가까운 쪽을 고른다 → lint로 모순을 **남기지 말아야** 하는 정량 근거. 또 "일관된 한 페이지"가 "단편 여러 개"보다 잘 먹힌다는 근거.
- 재현성: OSU-NLP-Group/LLM-Knowledge-Conflict 공개.

### 논문 3-3: ClashEval: Quantifying the tug-of-war between an LLM's internal prior and external evidence
- 저자·연도: Kevin Wu, Eric Wu, James Zou, 2024 (v3 2025-02)
- 발표처: NeurIPS 2024 (S2 표기; 트랙 미확인)
- arXiv ID: 2404.10198
- 피인용수: 144
- 요약: 6개 도메인 1,200+ 질문의 검색 문서에 미세~노골적 오류를 심어 6개 모델(GPT-4o 포함)이 틀린 검색 결과를 얼마나 받아들이는지 측정. 모델은 자기 사전 지식이 맞아도 틀린 검색 내용을 채택하는 경향이 있고, 진실에서 멀수록 거부율이 오르며, 사전 확신이 낮을수록 검색 내용을 채택.
- 인용할 만한 문장:
  > (abstract) 모델들은 "are susceptible to adopting incorrect retrieved content, overriding their own correct prior knowledge."
- 책 관련성: wiki의 오류는 그대로 답변 오류가 된다("쓰레기 넣으면 쓰레기 나온다"의 정량판). ingest 단계의 소스 신뢰도 표기와 lint의 필요성.
- 주의: 발표처 세부(NeurIPS 2024 Datasets & Benchmarks 여부) 미확인.

### 논문 3-4: Resolving Knowledge Conflicts in Large Language Models
- 저자·연도: Yike Wang, Shangbin Feng, Heng Wang 외 (7인), 2023 (v3 2024-10)
- 발표처: COLM 2024 (arXiv 코멘트로 확인)
- arXiv ID: 2310.00935
- 피인용수: 51
- 요약: 충돌 시 LLM이 해야 할 3가지 — (1) 충돌 존재 식별, (2) 충돌 구간 특정, (3) 서로 다른 답/관점 구분 제시 — 를 정의하고 평가 프레임워크 구축. 모델은 (1)은 잘하지만 (2)(3)은 어려워한다.
- 인용할 만한 문장:
  > "while LLMs perform well in identifying the existence of knowledge conflicts, they struggle to determine the specific conflicting knowledge and produce a response with distinct answers amidst conflicting information." (Abstract)
- 책 관련성: lint 프롬프트 설계 — "모순이 있다/없다"만 묻지 말고 "어느 줄과 어느 줄이 충돌하는지"를 구조화해 출력하게 하라는 근거.

### 논문 3-5: Editing Large Language Models: Problems, Methods, and Opportunities
- 저자·연도: Yunzhi Yao, Peng Wang, Bozhong Tian 외 (8인), 2023
- 발표처: EMNLP 2023 (arXiv 코멘트로 확인)
- arXiv ID: 2305.13172
- 피인용수: 505
- 요약: 모델 가중치/보조 모듈을 고쳐 사실을 바꾸는 knowledge editing 기법(ROME, MEMIT, SERAC, IKE, MEND, FT, KN 등)을 reliability·generalization·locality·**portability**로 비교. 단일 편집은 잘 되지만 편집의 파급(portability)·대량/연속 편집에서 무너진다.
- 핵심 수치: GPT-J/ZsRE에서 ROME reliability 99.18·locality 99.19, MEMIT 99.23·99.62. Portability: SERAC 세 항목 모두 20% 미만(17.79/1.30/5.53), one-hop은 최고 방법도 약 55%(IKE 55.38, MEMIT 52.74). 모델 간 불안정: OPT-13B에서 ROME 22.23, MEMIT 7.95. Batch: MEMIT 1,000편집까지 reliability 유지하나 locality 하락; SERAC 100편집까지 완벽. Sequential: ROME n=10까지 양호, n=100에서 악화; MEND n=10에서 급락.
- 인용할 만한 문장:
  > "current model editing techniques continue to face challenges in managing the ramifications of an edit." (§5 Portability)
- 책 관련성: "모델을 고치지 말고 wiki를 고쳐라"의 정량 근거. 파라미터 편집은 파급 효과·연속 편집에 약하므로, 사내 지식처럼 매일 바뀌는 사실은 외부 텍스트(wiki)에서 관리하는 것이 낫다.
- 재현성: EasyEdit 공개(zjunlp/EasyEdit).

### 논문 3-6: A Comprehensive Study of Knowledge Editing for Large Language Models
- 저자·연도: Ningyu Zhang, Yunzhi Yao, Bozhong Tian 외 (22인), 2024 (v5 2024-11)
- 발표처: arXiv (Ongoing work)
- arXiv ID: 2401.01286
- 피인용수: 186
- 요약: 지식 편집을 **외부 지식 활용 / 지식 병합 / 내재 지식 편집** 3군으로 분류하고 KnowEdit 벤치마크 제안. "외부 지식 활용"(검색·메모리)이 분류의 한 축으로 공식 인정된다는 점이 중요.
- 인용할 만한 문장:
  > "we propose a unified categorization criterion that classifies knowledge editing methods into three groups: resorting to external knowledge, merging knowledge into the model, and editing intrinsic knowledge." (Abstract)
- 책 관련성: LLM Wiki는 "resorting to external knowledge" 계열의 극단적으로 단순한 구현이라고 자리매김.

### 논문 3-7: Evaluating the Ripple Effects of Knowledge Editing in Language Models
- 저자·연도: Roi Cohen, Eden Biran, Ori Yoran, Amir Globerson, Mor Geva, 2023
- 발표처: TACL 2024 (arXiv 코멘트로 확인)
- arXiv ID: 2307.12976
- 피인용수: 332
- 요약: 사실 하나를 고치면 논리적으로 따라 바뀌어야 할 사실들("ripple")이 있다. 5K 편집의 RippleEdits 벤치마크에서 기존 편집법은 일관된 변화를 만들지 못했고, **단순 in-context 편집 베이스라인이 최고점**.
- 인용할 만한 문장:
  > "a simple in-context editing baseline obtains the best scores on our benchmark, suggesting a promising research direction for model editing." (Abstract)
- 책 관련성: LLM Wiki ingest에서 "관련 페이지 10~15개를 같이 고친다"가 바로 ripple 처리다. 또 "컨텍스트에 넣어 고치는 게 가중치 편집보다 낫다"는 결과는 wiki 접근의 직접 지지.
- 재현성: 데이터 공개(edenbiran/RippleEdits).

### 논문 3-8: Time-Aware Language Models as Temporal Knowledge Bases
- 저자·연도: Bhuwan Dhingra, Jeremy R. Cole, Julian Martin Eisenschlos 외 (6인), 2021 (TACL 2022)
- 발표처: TACL 2022, vol.10, pp.257–273 (arXiv journal_ref로 확인)
- arXiv ID: 2106.15110
- 피인용수: 426
- 요약: "많은 사실에는 유효 기간이 있다." 시간에 따라 바뀌는 사실을 탐침하는 진단 데이터셋(TempLAMA)과, 텍스트에 타임스탬프를 함께 모델링하는 기법 제안. 시간 문맥으로 학습한 모델은 재학습 없이 "refresh"가 가능.
- 인용할 만한 문장:
  > "Many facts come with an expiration date, from the name of the President to the basketball team Lebron James plays for." (Abstract)
- 책 관련성: "as-of" 사실 개념의 고전 출처. wiki 페이지 사실마다 날짜를 적는 규약의 동기 인용으로 적합(첫 문장이 인용하기 좋다).

### 논문 3-9: TemporalWiki: A Lifelong Benchmark for Training and Evaluating Ever-Evolving Language Models
- 저자·연도: Joel Jang, Seonghyeon Ye, Changho Lee 외 (8인), 2022
- 발표처: EMNLP 2022 (arXiv 코멘트로 확인)
- arXiv ID: 2204.14211
- 피인용수: S2 조회 실패(미확인)
- 요약: 연속된 영어 Wikipedia/Wikidata 스냅샷의 **diff**로 학습·평가하는 평생 벤치마크. diff만으로 계속 학습하면 전체 스냅샷 학습과 비슷하거나 더 나은 perplexity를 12배 적은 계산으로 얻음.
- 핵심 수치: 계산 비용 1/12.
- 인용할 만한 문장:
  > "training an LM on the diff data through continual learning methods achieves similar or better perplexity than on the entire snapshot in our benchmark with 12 times less computational cost" (Abstract)
- 책 관련성: "변경분(diff)만 처리한다"는 증분 ingest 원칙의 학술 근거. log.md가 사실상 diff 원장이라는 설명에 연결.

### 논문 3-10: FreshLLMs: Refreshing Large Language Models with Search Engine Augmentation
- 저자·연도: Tu Vu, Mohit Iyyer, Xuezhi Wang 외 (11인, Google), 2023
- 발표처: ACL 2024 Findings (S2 표기 ACL; 트랙 미확인)
- arXiv ID: 2310.03214
- 피인용수: 450
- 요약: 빠르게 변하는 사실·거짓 전제 질문을 담은 동적 벤치마크 FreshQA(정기 갱신 약속). 모든 모델이 크기와 무관하게 fast-changing·false-premise에서 약함. 검색 결과를 프롬프트에 넣는 FreshPrompt가 Self-Ask·Perplexity.AI를 앞섬. 검색 근거의 **수와 순서**가 정답률에 영향, **간결한 답을 지시**하면 환각 감소.
- 핵심 수치: 50K+ 인간 판정.
- 인용할 만한 문장:
  > "all models (regardless of model size) struggle on questions that involve fast-changing knowledge and false premises." (Abstract)
  > "instructing the LLM to generate concise and direct answers helps reduce hallucination compared to encouraging more verbose answers." (Abstract)
- 책 관련성: 사내 지식은 대부분 fast-changing이다. 답변 프롬프트에 "간결하게, 근거 페이지 명시"를 넣는 근거.
- 재현성: freshllms/freshqa 공개·정기 갱신.

### 논문 3-11: Deduplicating Training Data Makes Language Models Better
- 저자·연도: Katherine Lee, Daphne Ippolito, Andrew Nystrom 외 (7인, Google), 2021 (ACL 2022)
- 발표처: ACL 2022 (arXiv 코멘트로 확인)
- arXiv ID: 2107.06499
- 피인용수: 1,012
- 요약: 학습 데이터 중복 제거 도구(exact substring, NearDup/MinHash) 제안. C4에서 61단어짜리 한 문장이 6만 번 이상 반복됨을 발견.
- 핵심 수치: 비프롬프트 출력의 1% 이상이 학습 데이터 그대로 복사. 중복 제거 시 암기 출력 10배 감소. train-test 중복이 표준 데이터셋 검증 집합의 4% 이상.
- 인용할 만한 문장:
  > "removing from C4 a single 61 word English sentence that is repeated over 60,000 times." (Abstract)
- 책 관련성: 학습 데이터 맥락이지만 "중복은 편향과 비용을 낳는다"는 일반 원리 + MinHash/suffix array 등 실무 dedup 도구의 출처. wiki lint의 중복 페이지 탐지에 같은 기법 적용 가능. (검색 코퍼스 dedup 효과를 직접 측정한 논문은 아님 — 과잉 일반화 주의.)
- 재현성: google-research/deduplicate-text-datasets 공개.

### 논문 3-12: SemDeDup: Data-efficient learning at web-scale through semantic deduplication
- 저자·연도: Amro Abbas, Kushal Tirumala, Dániel Simig, Surya Ganguli, Ari S. Morcos (Meta), 2023
- 발표처: arXiv 프리프린트(ICLR 2023 워크숍 여부 미확인)
- arXiv ID: 2303.09540
- 피인용수: 미조회
- 요약: 사전학습 임베딩으로 **의미적 중복**(동일하진 않지만 거의 같은 내용)을 찾아 제거. LAION 부분집합에서 50%를 제거해도 성능 손실 최소, 학습 시간 절반.
- 인용할 만한 문장:
  > "SemDeDup can remove 50% of the data with minimal performance loss, effectively halving training time." (Abstract)
- 책 관련성: lint의 "같은 얘기를 하는 두 페이지" 탐지는 exact dedup이 아니라 semantic dedup — 임베딩 클러스터링으로 후보를 찾고 LLM이 병합 판단하는 흐름의 근거.

---

## 4. 평가 (RAG/KB-QA 평가·인용 정확도·검색 하 환각)

### 논문 4-1: Ragas: Automated Evaluation of Retrieval Augmented Generation
- 저자·연도: Shahul Es, Jithin James, Luis Espinosa-Anke, Steven Schockaert, 2023 (v2 2025-04)
- 발표처: EACL 2024 (S2 표기; System Demonstrations 트랙 여부 미확인)
- arXiv ID: 2309.15217
- 피인용수: 1,154
- 요약: 정답 레이블 없이(reference-free) RAG를 평가하는 프레임워크. 검색의 **context relevance**, 생성의 **faithfulness**(답변 주장이 검색 문맥에 지지되는가), **answer relevance** 3축을 LLM으로 측정.
- 인용할 만한 문장:
  > "a suite of metrics which can be used to evaluate these different dimensions without having to rely on ground truth human annotations" (Abstract)
- 책 관련성: 사내 KB-QA의 회귀 테스트 지표 세트. 특히 faithfulness = "답변이 wiki 페이지에 근거하는가"를 자동으로 재는 도구.
- 재현성: explodinggradients/ragas 오픈소스.

### 논문 4-2: ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems
- 저자·연도: Jon Saad-Falcon, Omar Khattab, Christopher Potts, Matei Zaharia, 2023
- 발표처: NAACL 2024 (arXiv 코멘트로 확인)
- arXiv ID: 2311.09476
- 피인용수: 444
- 요약: 합성 데이터로 경량 LM 판정기를 미세조정하고, 소수(수백 건)의 인간 레이블로 prediction-powered inference(PPI)를 적용해 신뢰구간을 보정. KILT·SuperGLUE·AIS 8개 과제, 도메인 이동에도 강건.
- 인용할 만한 문장:
  > "ARES accurately evaluates RAG systems while using only a few hundred human annotations during evaluation." (Abstract)
- 책 관련성: "수백 건의 인간 라벨 + 자동 판정기"라는 현실적 평가 예산 설계. 사내 팀이 골든셋을 몇 건 만들어야 하는지의 기준점.
- 재현성: 코드·데이터 공개(stanford-futuredata/ARES).

### 논문 4-3: Enabling Large Language Models to Generate Text with Citations (ALCE)
- 저자·연도: Tianyu Gao, Howard Yen, Jiatong Yu, Danqi Chen (Princeton), 2023
- 발표처: EMNLP 2023 (arXiv 코멘트로 확인)
- arXiv ID: 2305.14627
- 피인용수: 864
- 요약: 인용 생성의 첫 자동 벤치마크. fluency·correctness·**citation quality**(recall/precision) 3축 자동 지표가 인간 판단과 강하게 상관.
- 핵심 수치: ELI5에서 최고 모델도 50%는 인용 근거가 불완전.
- 인용할 만한 문장:
  > "on the ELI5 dataset, even the best models lack complete citation support 50% of the time." (Abstract)
- 책 관련성: "인용을 달게 하면 끝"이 아니라는 경고 + 인용 정밀도/재현율 정의의 출처. wiki 답변의 `[[page]]` 인용을 평가할 때 그대로 쓰는 지표.
- 재현성: princeton-nlp/ALCE 공개.

### 논문 4-4: Evaluating Verifiability in Generative Search Engines
- 저자·연도: Nelson F. Liu, Tianyi Zhang, Percy Liang, 2023
- 발표처: Findings of EMNLP 2023 (arXiv 코멘트로 확인)
- arXiv ID: 2304.09848
- 피인용수: 476
- 요약: Bing Chat·NeevaAI·perplexity.ai·YouChat을 인간 평가. 답변은 유창하고 유익해 보이지만 근거 없는 문장과 틀린 인용이 빈번.
- 핵심 수치: 생성 문장의 평균 51.5%만 인용으로 완전히 지지. 인용의 74.5%만 해당 문장을 실제로 지지.
- 인용할 만한 문장:
  > "on average, a mere 51.5% of generated sentences are fully supported by citations and only 74.5% of citations support their associated sentence." (Abstract)
  > "especially given their facade of trustworthiness." (Abstract)
- 책 관련성: 상용 시스템도 이 정도 — 사내 에이전트의 인용을 믿지 말고 측정하라는 동기 부여용 수치.
- 신선도: 2023년 초 상용 시스템 기준. 최신 상태로 일반화 금지.

### 논문 4-5: FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation
- 저자·연도: Sewon Min, Kalpesh Krishna, Xinxi Lyu 외 (9인), 2023
- 발표처: EMNLP 2023 (arXiv 코멘트로 확인)
- arXiv ID: 2305.14251
- 피인용수: 1,819
- 요약: 긴 생성문을 **원자 사실**로 쪼개 신뢰 소스로 지지되는 비율을 계산. 인물 전기에서 ChatGPT 58%. 자동 추정기 오차 2% 미만. 13개 모델 6,500 생성 평가(인간이면 $26K).
- 인용할 만한 문장:
  > "ChatGPT only achieves 58%" (Abstract)
  > "an automated model that estimates FACTSCORE using retrieval and a strong language model, with less than a 2% error rate." (Abstract)
- 책 관련성: wiki 페이지 자체의 사실 정밀도를 평가하는 방법(페이지를 원자 사실로 쪼개 raw source와 대조). lint 자동화의 측정 모델.
- 재현성: `pip install factscore`.

### 논문 4-6: RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models
- 저자·연도: Cheng Niu, Yuanhao Wu, Juno Zhu 외 (8인), 2023 (v2 2024-05)
- 발표처: ACL 2024 (S2 표기 ACL; 연도·트랙 미확인)
- arXiv ID: 2401.00396
- 피인용수: 434
- 요약: 검색을 줬는데도 생기는 환각을 **단어 수준**으로 주석한 코퍼스. 6개 모델(GPT-3.5/4-0613, Mistral-7B, Llama-2 7B/13B/70B-chat) × 2,965 인스턴스 = 17,790 응답.
- 핵심 수치 (계산값, Table 3 ÷ 2,965): 환각 포함 응답 비율 GPT-3.5 13.5%, GPT-4 13.7%, Llama-2-70B 47.0%, 13B 56.6%, 7B 61.8%, Mistral-7B 65.9%. 미세조정 Llama-2-13B 탐지기 응답 수준 F1 78.7% vs 프롬프트 GPT-4-turbo 63.4%; 스팬 수준 52.7% vs 28.3%.
- 인용할 만한 문장:
  > "Despite the integration of RAG, LLMs may still present unsupported or contradictory claims to the retrieved contents." (Abstract)
  > "a fine-tuned Llama-2-13B can achieve the best performance with an average 78.7% f1 score." (§6.1)
- 책 관련성: "wiki를 줘도 환각은 남는다 — 2023년 GPT-4급도 응답의 ~14%". 또 작은 전용 탐지기가 대형 범용 모델 프롬프트보다 낫다는 결과는 사내 환각 탐지기 구축 근거.
- 재현성: 코퍼스 공개(ParticleMedia/RAGTruth).

### 논문 4-7: LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory
- 저자·연도: Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, Dong Yu, 2024 (v2 2025-03)
- 발표처: ICLR 2025 (arXiv 코멘트로 확인)
- arXiv ID: 2410.10813
- 피인용수: 750
- 요약: 장기 메모리 5능력(정보 추출·다세션 추론·시간 추론·**지식 갱신**·**거부(abstention)**)을 500문항으로 평가. 상용 어시스턴트와 long-context 모델이 30% 정확도 하락. 메모리 설계를 indexing/retrieval/reading 3단계로 분해하고 각 단계 최적화 효과를 측정.
- 핵심 수치: ChatGPT(GPT-4o) 37% 하락, Coze 64% 하락(오프라인 전체 읽기 대비). long-context 모델 30~60% 하락(LongMemEval_S ≈ 115k 토큰; _M은 500세션 ≈ 1.5M 토큰). 세션 대신 **라운드** 단위 분해가 유리. 사실 보강 키 확장: recall@k +9.4%, 정확도 +5.4%. 시간 인식 질의 확장: 시간 추론 recall +6.8~11.3%(강한 LLM이 시간 범위를 뽑을 때만). Chain-of-Note+JSON 읽기: oracle 검색 시 최대 +10점.
- 인용할 만한 문장:
  > "commercial chat assistants and long-context LLMs showing a 30% accuracy drop on memorizing information across sustained interactions" (Abstract)
  > "Instead of sessions, round is the more optimal granularity for storing and utilizing the interactive history." (§5)
- 책 관련성: 평가 축에 "지식 갱신"과 "모르면 거부"가 포함된 유일한 표준 벤치마크 — 사내 KB 평가셋 설계의 틀. "작은 단위 + 사실 키 + 시간 필터"는 wiki 페이지 메타(요약 줄·날짜)의 설계 근거.
- 재현성: xiaowu0162/LongMemEval 공개.

### 논문 4-8: WikiChat: Stopping the Hallucination of LLM Chatbots by Few-Shot Grounding on Wikipedia
- 저자·연도: Sina J. Semnani, Violet Z. Yao, Heidi C. Zhang, Monica S. Lam (Stanford), 2023
- 발표처: Findings of EMNLP 2023 (arXiv 코멘트로 확인)
- arXiv ID: 2305.14292
- 피인용수: 미조회
- 요약: LLM 초안을 생성한 뒤 **근거 있는 사실만 남기고** 위키 검색으로 보강하는 7단계 파이프라인. GPT-4 기반을 7B LLaMA로 증류.
- 핵심 수치: 시뮬레이션 대화 사실 정확도 97.3%. GPT-4 대비 head/tail/recent 지식에서 +3.9%/+38.6%/+51.0%. 실제 사용자와 최신 주제 대화 97.9%(GPT-4보다 55.0% 높음).
- 인용할 만한 문장:
  > "WikiChat generates a response from an LLM, retains only the grounded facts, and combines them with additional information it retrieves from the corpus" (Abstract)
- 책 관련성: "초안 → 사실 검증 → 근거 없는 문장 삭제" 패턴은 wiki 답변 파이프라인의 안전 장치로 그대로 이식 가능. tail/recent 지식에서 이득이 큰 것이 사내 지식(대부분 tail·recent)에 딱 맞는 메시지.
- 재현성: stanford-oval/WikiChat 공개.

---

## 5. Wikipedia 생성 연구 (STORM 계열·LLM 백과 문서)

### 논문 5-1: Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models (STORM)
- 저자·연도: Yijia Shao, Yucheng Jiang, Theodore A. Kanell, Peter Xu, Omar Khattab, Monica S. Lam (Stanford), 2024
- 발표처: NAACL 2024 Main (arXiv 코멘트로 확인)
- arXiv ID: 2402.14207
- 피인용수: 210
- 요약: Wikipedia급 긴 글을 처음부터 쓰는 문제에서 **pre-writing**(조사·개요)이 핵심이라고 보고, (1) 다양한 관점 발견, (2) 관점별 작가가 전문가에게 질문하는 대화 시뮬레이션(신뢰 소스 근거), (3) 수집 정보로 개요 작성. FreshWiki(최신 고품질 문서) 데이터셋·개요 평가 지표 제안. 경험 있는 Wikipedia 편집자 피드백 수집.
- 핵심 수치: 개요 기반 RAG 베이스라인 대비 "조직적" 판정 +25%p, "폭넓음" +10%p. 편집자가 지적한 새 문제: **source bias transfer**(출처 편향 전이), **over-association of unrelated facts**(무관한 사실 과잉 연결).
- 인용할 만한 문장:
  > "more of STORM's articles are deemed to be organized (by a 25% absolute increase) and broad in coverage (by 10%)." (Abstract)
  > "The expert feedback also helps identify new challenges for generating grounded long articles, such as source bias transfer and over-association of unrelated facts." (Abstract)
- 책 관련성: 개념 페이지를 "질문 목록을 먼저 만들고 → 소스에서 답을 모으고 → 개요를 짠 뒤" 쓰는 ingest 프롬프트의 근거. 편집자가 꼽은 두 실패(출처 편향 전이·과잉 연결)는 lint 점검 항목으로 바로 쓸 수 있다.
- 재현성: stanford-oval/storm 오픈소스.

### 논문 5-2: Into the Unknown Unknowns: Engaged Human Learning through Participation in LM Agent Conversations (Co-STORM)
- 저자·연도: Yucheng Jiang, Yijia Shao, Dekun Ma, Sina J. Semnani, Monica S. Lam, 2024
- 발표처: EMNLP 2024 Main (arXiv 코멘트로 확인)
- arXiv ID: 2408.15232
- 피인용수: 64
- 요약: 여러 LM 에이전트가 사용자를 대신해 질문하며 토론하고, 발견한 정보를 **동적 마인드맵**으로 정리해 최종 보고서로 만든다. 사용자는 관찰하다 가끔 개입("unknown unknowns" 발견).
- 핵심 수치: 인간 평가에서 70%가 검색엔진보다, 78%가 RAG 챗봇보다 Co-STORM 선호. WildSeek 데이터셋.
- 인용할 만한 문장:
  > "70% of participants prefer Co-STORM over a search engine, and 78% favor it over a RAG chatbot." (Abstract)
- 책 관련성: "질의 → 답변"을 넘어 "탐색 중 생긴 지식을 구조(마인드맵)에 누적"하는 것이 LLM Wiki의 "답변을 wiki로 환류"와 같은 아이디어.
- 재현성: storm 저장소에 포함.

### 논문 5-3: WikiAutoGen: Towards Multi-Modal Wikipedia-Style Article Generation
- 저자·연도: Zhongyu Yang, Jun Chen, Dannong Xu 외 (8인), 2025 (v3 2025-09)
- 발표처: ICCV 2025 (arXiv 코멘트로 확인)
- arXiv ID: 2503.19065
- 피인용수: 5
- 요약: 텍스트+이미지를 함께 검색·통합하는 멀티모달 Wikipedia 문서 생성. **multi-perspective self-reflection**으로 검색 내용의 신뢰성·폭·일관성을 여러 관점에서 비판 점검. WikiSeek 벤치마크.
- 핵심 수치: WikiSeek에서 이전 방법 대비 8~29% 향상.
- 인용할 만한 문장:
  > "WikiAutoGen outperforms previous methods by 8%-29% on our WikiSeek benchmark" (Abstract)
- 책 관련성: 사내 wiki에 다이어그램·스크린샷을 함께 저장하는 확장 방향. 피인용 5건으로 아직 검증 초기 — 책에서는 "최근 방향" 정도로만.
- 재현성: 코드 공개(wikiautogen.github.io).

---

## 부록 A. 보조 참고 (요약만, 본문 인용 시 재확인 필요)

| 논문 | arXiv | 발표처 | 한 줄 |
|---|---|---|---|
| Reflexion: Language Agents with Verbal Reinforcement Learning (Shinn 외, 2023) | 2303.11366 | NeurIPS 2023 (미확인; arXiv 코멘트 없음) | 실패를 말로 성찰해 episodic memory에 쌓아 다음 시도 개선. HumanEval pass@1 91% vs GPT-4 80%. 에이전트가 "lint 결과를 다음 ingest에 반영"하는 루프의 근거. |
| Agent Workflow Memory (Wang 외, 2024) | 2409.07429 | 미확인 | 과거 궤적에서 재사용 가능한 워크플로를 귀납해 메모리에 저장. Mind2Web +24.6%, WebArena +51.1% 상대 성공률. schema(CLAUDE.md)에 "자주 쓰는 질의 절차"를 쌓는 아이디어. |
| MemoryBank (Zhong 외, 2023) | 2305.10250 | AAAI 2024 (미확인) | Ebbinghaus 망각 곡선 기반 메모리 갱신. 시간 감쇠 아이디어의 또 다른 출처. |
| MemoRAG (Qian 외, 2024) | 2409.05591 | TheWebConf 2025 (arXiv 코멘트로 확인) | 전역 메모리 모델이 "답의 단서"를 먼저 만들고 그것으로 검색. |
| MemOS: A Memory OS for AI System (Li 외, 2025) | 2507.03724 | 미확인 | 메모리를 OS 자원으로 다루는 아키텍처 제안(39인 저자). 개념 참고용. |
| Open-Source Reproduction and Explainability Analysis of CRAG (Yalavarthi, 2026) | 2603.16169 | 미확인 | CRAG 재현 보고. CRAG 수치를 인용할 때 재현 가능성 근거로. |

## 부록 B. 책 장별 인용 매핑 제안

| 책의 주제 | 1순위 인용 | 보조 |
|---|---|---|
| 왜 RAG가 아니라 wiki인가 | GraphRAG(1-8), RAPTOR(1-7), Lost in the Middle(2-8), Context Rot(S-2) | NoLiMa(2-11), RULER(2-10), Same Task More Tokens(2-9) |
| 메모리 아키텍처 계보 | Generative Agents(1-2), MemGPT(1-3), A-MEM(1-4) | 메모리 서베이(1-1), Mem0(1-5), Zep(1-6) |
| 페이지 작성 규약(원자 사실·링크) | Dense X(1-11), A-MEM(1-4) | Semantic chunking(1-12), HippoRAG(1-10) |
| 에이전틱 질의 루프 | ReAct(2-3), IRCoT(2-4), Self-RAG(2-5), CRAG(2-6) | Search-R1(2-7), Agentic RAG 서베이(2-2), Self-Route(2-12) |
| lint: 모순·낡은 사실·중복 | Chameleon/Sloth(3-2), ClashEval(3-3), Zep 시간 그래프(1-6), Resolving Conflicts(3-4) | Knowledge Conflicts 서베이(3-1), Time-Aware LM(3-8), TemporalWiki(3-9), Dedup(3-11), SemDeDup(3-12) |
| 왜 모델 편집이 아닌가 | Editing LLMs(3-5), Ripple Effects(3-7) | Comprehensive Study(3-6) |
| 평가 | RAGAS(4-1), ARES(4-2), ALCE(4-3), LongMemEval(4-7) | Verifiability(4-4), FActScore(4-5), RAGTruth(4-6), FreshLLMs(3-10) |
| 문서 생성 품질 | STORM(5-1), WikiChat(4-8) | Co-STORM(5-2), WikiAutoGen(5-3) |

## 수집 한계

- Semantic Scholar는 2026-10-11 조회 시 검색 엔드포인트가 429로 막혀 batch 엔드포인트로 피인용수만 받았다. TemporalWiki·WikiChat·SemDeDup 3편은 피인용수 미조회.
- 발표처는 arXiv 코멘트에 명시된 경우만 "확인"으로 적었고, 나머지는 S2 표기(트랙·연도 미확인). fact-checker는 "S2 표기"·"미확인" 항목을 본문 인용 전 재조회할 것.
- 전문을 읽은 논문은 HTML 버전이 있는 일부(RAPTOR·GraphRAG·MemGPT·Self-RAG·CRAG·A-MEM·Generative Agents·Lost in the Middle·NoLiMa·Same Task·Zep·LongMemEval·Chameleon·RAGTruth·Dense X·Editing LLMs·Search-R1·LC vs RAG)이며, 각 페이지의 처음 100K자까지만 읽었다. "(계산값)" 표기 수치는 표에서 산출한 것으로 논문 문장이 아니다.
- Search-R1의 상대 개선 수치는 arXiv 버전 간 불일치(41% vs 24%)가 있어 인용 시 범위로 적어야 한다.
- Context Rot(Chroma)·LLM Wiki gist는 동료심사 자료가 아니다. 벤더 자체 평가(Mem0·Zep·Chroma)는 그 사실을 본문에 밝힐 것.
- "LLM이 유지보수하는 wiki" 자체를 직접 연구한 동료심사 논문은 찾지 못했다(가장 가까운 것: A-MEM의 Zettelkasten 메모리, STORM의 문서 생성, Zep의 시간 그래프). 이 공백은 책의 차별점이자, 주장의 근거를 인접 연구에서 끌어와야 한다는 제약이다.
