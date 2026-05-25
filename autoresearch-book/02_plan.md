# autoresearch — 자율 루프의 시대를 읽는 책 저술 계획

> **v2 — plan-reviewer의 강한 권고 3가지(액션 1·2·3) 반영.** 변경 이력은 `03_review_log.md` 참조.

## 제목 후보

1. **autoresearch: 사람이 자는 동안 진화하는 코드**
   - **콘셉트:** Karpathy의 디스토피아 픽션 ("meat computers", "10,205세대") 톤을 정면으로 가져온 도발적 카피. autoresearch라는 고유명을 그대로 노출해서 "이 사건이 뭐였는지 알고 싶은 사람"을 정확히 호명한다.
   - **어필 포인트:** 시니어 엔지니어, 특히 Claude Code/Codex 사용자에게 "그 화제의 그것"이라는 즉각적 인식을 준다. 부제가 카피처럼 작동해서 책장에서 한 번 더 집어 들게 만든다.
   - **약점:** 영어 고유명사가 메인 타이틀에 들어가 검색 노출은 좋지만 일반 독자에게는 진입장벽.

2. **편집 가능한 한 파일, 봉인된 하나의 점수: 자율 에이전트가 일하는 법**
   - **콘셉트:** autoresearch의 디자인 슬로건("one GPU, one file, one metric")을 한국어로 재구성한 제목. 책의 진짜 주제 — 측정 가능한 메트릭과 편집 범위 제약이 자율성을 만든다 — 를 제목 자체에 압축.
   - **어필 포인트:** autoresearch라는 단어를 모르는 독자에게도 호기심을 자극한다. "한 파일·하나의 점수"라는 대칭이 만드는 미니멀함이 책의 톤과 일치.
   - **약점:** 길다. autoresearch 검색 SEO를 직접 얻지 못한다.

3. **루프 안의 에이전트: 측정 가능한 자율성을 설계하는 법**
   - **콘셉트:** 메시지 중심 카피. autoresearch는 사례 한 편으로 다루되, 책의 일반화 가능한 주제 — "measurable autonomy"를 어떻게 설계할 것인가 — 를 전면에 내세운다.
   - **어필 포인트:** Claude Code 응용에 관심 있는 실무자에게 "내 도메인에 가져올 수 있겠다"는 신호를 보낸다. 시리즈화 가능한 제목.
   - **약점:** 추상적이라 첫 임팩트가 약할 수 있다. 책의 핵심 hook(2026년 봄의 그 사건)이 제목에서 사라진다.

**추천:** **1번 — "autoresearch: 사람이 자는 동안 진화하는 코드"**
- **이유:** 책은 단순한 일반 패턴 해설서가 아니라 "**2026년 봄에 일어난 한 사건과 그 의미**"를 풀어내는 케이스 스터디다. autoresearch라는 고유명을 정면에 박는 편이 책의 정체성을 정확히 표현한다. 부제로 "사람이 자는 동안 진화하는 코드"를 두면 한국어 독자에게 즉각적인 정서적 hook이 생기고, Karpathy 본인의 픽션 톤("That era is long gone... story of how it all began")과 책의 마지막 챕터(epilogue) 톤이 자연스럽게 연결된다. 응용편(Part 4)이 책의 절반에 가깝지만, 그 응용을 권위 있게 만드는 것이 "이 사건"의 무게이므로 사건 자체를 제목에 박는 편이 마케팅과 메시지 양쪽에서 유리하다.

---

## 책 특성

- **장르:** 기술 에세이 + 케이스 스터디 (단순 튜토리얼·해설서가 아니다. 한 사건을 매개로 시대의 패턴을 읽고 자기 도메인으로 옮기는 법을 함께 사유하는 형태.)
- **분량:** 본문 11개 챕터, 각 챕터 약 4,500-8,000자, 전체 약 75,000자 (인트로·에필로그·콜로폰 포함)
- **난이도:** 중급-고급 (LLM 기본 개념·git·CI/CD·에이전트 도구 사용 경험은 전제. 단, Muon이나 ResFormer 같은 깊은 기술 내용은 "왜 들어 있는지"와 "에이전트가 이걸로 무엇을 한 의미인지"까지만 다루고 수식·구현 디테일로 빠지지 않는다.)
- **독자 여정:** *"autoresearch가 화제였다고 들었는데 정확히 뭔지 모르겠고, 패턴이 일반화 가능하다고 하던데 내 일에 어떻게 적용해야 할지도 모르겠다"* 상태 → *"이건 단지 ML 트릭이 아니라 측정 가능한 자율성을 설계하는 방법론이며, 내 도메인의 한 모듈에서 이번 주에 시작할 수 있는 구체적 루프가 머릿속에 그려진다"* 상태로 이동시킨다.

---

## 내러티브 아크 (v2)

책은 **하나의 사건을 점점 멀리서 보다가, 마지막에 독자의 책상 위로 다시 가져오는** 구조로 짜인다. Part 1은 **사건의 등장**이다 — Karpathy의 픽션 트윗과 Anthropic 합류 사이에 끼어 있는 2026년 봄 두 달의 풍경을 정직하게 보고하고, 2장에서 "5분/한 파일/한 점수"의 디자인 슬로건을 일반화 어휘로 환원한다. 2장에는 Dreamwalker(박제창)의 "human-above-the-loop" 프레임을 흡수해 한국어 사고 도구로 정착시킨다. Part 2는 **해부**다 — 무엇이 들어 있는지를 보되 코드 워크스루로 빠지지 않는다. 3장은 "제약 → 결정 → 부수효과 → 비판 가능 지점"이라는 4열 표 하나를 해설하는 짧고 단단한 챕터로 압축한다. 4장은 frozen metric의 정치학을 다루며 연세대 DLI Lab의 metric paradox를 그 안에 녹인다. 5장은 ratchet 루프와 그 한계, 도구 의존성을 본다. Part 3은 **세상이 이걸 어떻게 받았는가**다 — 6장에서 포크의 풍경과 1차 사용 후기를, 7장에서는 한국 챕터를 따로 두지 않고 **"같은 의제의 다른 풍경"** — Sakana AI Scientist, Agent Laboratory, ICLR 2026 RSI 워크숍, Anthropic의 새 미션을 옆에 놓고 autoresearch를 비교 좌표 안에서 다시 본다. corrigibility와 RSI 안전성 담론을 이 7장으로 끌어와 사회적·윤리적 시야를 확보한다. 8장은 부서지는 지점들 — frozen metric의 어두운 면, reward hacking, overfitting, prompt injection을 정직하게 다룬다. Part 4는 **독자의 책상으로 가져오기**다 — 9장에서 일반화 공식과 SOTAAZ의 도메인 일반화 시도, 그리고 사내 적용 사고 실험을 펼친다. 10장은 6개 카탈로그를 평면 진열하는 대신 **3개 깊은 워크스루**(Shopify Liquid 핫경로 / idealo RAG / az9713 시스템 프롬프트)와 **3개 짧은 카탈로그 박스**(CI 그린닝 / 커버리지 진화 / 회귀 격리)로 비대칭 구조를 만든다 — "내일 시작할 수 있다"는 감각은 깊은 워크스루에서 나오고, 카탈로그는 가능성의 지도 역할만 한다. 11장은 메타 응용에 집중한다 — SKILL.md 진화, Sibyl, 그리고 이 책 자체가 책 저술 하네스로 만들어지고 있다는 사실. 에필로그는 다시 처음으로 돌아간다.

흐름의 리듬은 *사건 → 분해 → 사회/맥락 → 비판 → 응용 → 메타 → 시야 확장*이다.

---

## 챕터 목록 (v2)

### 1장. 자율 연구 swarm이 있다고 상상해보자
- **핵심 질문:** Karpathy의 픽션 트윗이 농담만은 아니라면, 우리는 지금 어디 서 있는 걸까?
- **주요 내용:**
  - Karpathy의 README 픽션 인용("meat computers... 10,205th generation...")을 열고, 픽션이 아닌 부분을 분리해 보자
  - autoresearch가 무엇인지 30초 요약 — 5분 GPU, train.py, program.md, val_bpb
  - 공개 일주일 만에 3만 stars, 5월 19일 Karpathy의 Anthropic 합류 — 이 두 사건이 같은 흐름이라는 관찰
  - Karpathy 본인의 Sequoia 발언 — "December 2025 was a tipping point"이라는 자기 진단
  - 이 책이 답하려는 두 질문: "이 사건은 정확히 뭐였나"와 "이게 내 도구상자에 들어오면 어떻게 되나"
  - 책의 약속: 코드 워크스루로 빠지지 않을 것, 비판을 회피하지 않을 것, 마지막엔 독자의 책상으로 돌아올 것
- **독자가 얻는 것:** 책 전체의 좌표축. "이게 화제였다"에서 "이게 왜 의제였는가"로 시야 전환.
- **예상 분량:** 5,500자
- **활용 reference 섹션:** §1.1, §1.3, §4.1, §4.2 / 픽션 인용은 §1.3 1차 자료

### 2장. 5분, 한 파일, 점수 하나 — 디자인 슬로건 해부 (+1,000자 보강)
- **핵심 질문:** "one GPU, one file, one metric"이 슬로건이 아니라 디자인 결정이라면, 이 세 제약은 각각 무엇을 가능하게 하는가?
- **주요 내용:**
  - 단일 GPU 제약 — 비용 통제뿐 아니라 비교 가능성을 위한 결정이라는 점
  - 단일 편집 가능 파일(train.py) — 에이전트의 권한 경계를 코드로 그어 둔다는 것의 의미
  - 단일 메트릭(val_bpb) — 측정의 봉인이 왜 자율성의 전제인가 (자세한 정치학은 4장으로)
  - 5분 wall-clock 예산 — 시간이 메트릭의 일부가 되는 순간 무엇이 바뀌는가
  - **(흡수)** Dreamwalker(박제창)의 **"human-above-the-loop"** 프레임 — 한국어 사고 도구로 정착시키기. "루프 위의 사람"이 무엇을 하고 무엇을 하지 않는가, "in-the-loop"과의 대비
  - 3-파일 구조(prepare.py / train.py / program.md)와 권한 분할 표
  - 사고 실험: 한국 실무자가 자기 도메인에서 "train.py / prepare.py / program.md"의 3등분을 그어 본다면
- **독자가 얻는 것:** 디자인 결정을 일반화 가능한 어휘로 환원하는 능력. 자기 도메인에서 "내 train.py는 무엇이고, 내 prepare.py는 무엇인가"를 묻기 시작한다. **"human-above-the-loop"**라는 한국어 사고 도구.
- **예상 분량:** 7,500자
- **활용 reference 섹션:** §1.2, §2.5, §3.1, §3.2, §4.6 Dreamwalker

### 3장. train.py 안에 들어 있는 결정들 — 제약이 만든 선택들 (7,000 → 4,500자 축소)
- **핵심 질문:** train.py의 기술 선택이 우연이 아니라 "5분 예산"이라는 제약이 강제한 결과라면, 우리가 배울 것은 디자인 패턴인가 기법인가?
- **본문 구조:** 4열 표 한 개의 해설. 표는 다음과 같이 구성:

  | 제약 | 결정 | 부수효과 | 비판 가능 지점 |
  |---|---|---|---|
  | bfloat16에서 5스텝 안에 수렴해야 함 | Muon (Newton-Schulz 직교화) | NanoGPT 스피드런 35% 단축 계보 | 짧은 호라이즌에 과적합된 옵티마이저일 수 있음 |
  | 짧은 학습에서 효율이 곧 능력 | Value Residual (ResFormer) | 16% 적은 파라미터로 동등 손실 | 깊이 transfer 검증은 단일 사례뿐 |
  | 작은 컴퓨트에서 글로벌 컨텍스트 보존 | Sliding Window SSSL 패턴 | 효율과 receptive field의 균형 | 작은 모델에서는 L 단일이 권장 — 패턴 자체가 스케일 의존 |
  | 빠른 수렴 강제 | layer-wise 학습 스칼라(`resid_lambdas`) | 5분 안 수렴 가속 | Rahul Kumar — 단기 호라이즌 오버피팅 위험 |

- **해설의 방식:**
  - 표의 각 행을 5-7문장으로 풀되, 알고리즘 설명이 아니라 "왜 이 자리에 이 결정이 있는가"만 본다
  - 핵심 관찰 한 문장: 기술 선택은 모두 "5분 안에 신호를 내야 한다"는 제약의 함수다 — 제약이 바뀌면 답이 바뀐다
  - Muon 저자 Keller Jordan의 OpenAI 채용 일화는 1-2문장 각주성 언급으로만
  - 한국 ML 커뮤니티의 Muon 반응(NanoGPT 스피드런 35% 단축 시점의 반향)은 짧은 사이드바
- **독자가 얻는 것:** 기술 디테일 자체보다 "제약→선택"의 매핑을 읽는 눈. 자기 도메인의 제약을 명문화하면 어떤 기법이 자동으로 떠오르는가.
- **예상 분량:** 4,500자
- **활용 reference 섹션:** §2.1, §2.2, §2.3, §2.6 / 비판은 §6.4

### 4장. 봉인된 점수표 — BPB와 frozen metric의 정치학
- **핵심 질문:** 평가 함수를 에이전트가 못 건드린다는 단순한 결정이 왜 autoresearch 전체의 가장 중요한 디자인 선택인가?
- **주요 내용:**
  - bits-per-byte가 perplexity 대신 쓰인 이유 — 토크나이저를 바꿔도 분모(byte)가 고정
  - prepare.py가 "불변"이라는 약속 — 평가 셰일드를 못 박은 reward hacking 차단
  - frozen metric의 양면 (Iacono 인용): "wrong person이나 wrong time에 봉인되면 점수표는 감옥이다"
  - 평가 자체의 통계적 오염 — 같은 holdout에 수백 번 측정하면 그 자체가 새로운 학습 신호 (Phil Schmid의 경고)
  - 평가 디자인의 기준 4가지: binary, locked, compact, gaming-resistant
  - **(흡수)** 연세대 DLI Lab의 **"metric optimization paradox"** — 측정이 목적이 되면 측정이 망가진다. 한국 학계의 이 정리가 왜 4장의 본문으로 들어와야 하는가
- **독자가 얻는 것:** "내 도메인에 적용할 때 가장 어려운 부분은 코드가 아니라 메트릭"이라는 인식. 메트릭 디자인의 체크리스트와 한국어 사고 도구로서의 "metric paradox".
- **예상 분량:** 6,500자
- **활용 reference 섹션:** §2.4, §6.2, §6.5, §4.6 DLI Lab

### 5장. keep과 discard — git을 메모리로 쓰는 ratchet 루프
- **핵심 질문:** 단방향 ratchet은 정말 충분히 똑똑한가? "더 나빠진 뒤 더 좋아지는" 우회를 못 보는 알고리즘이 어떻게 한 달 만에 산업의 의제가 되었나?
- **주요 내용:**
  - LOOP FOREVER의 9단계와 git 브랜치 운영
  - results.tsv 5컬럼의 의미 — commit / val_bpb / memory_gb / status / description
  - program.md의 "NEVER STOP" 지시와 simplicity criterion의 코드 보존 효과
  - 단방향 hill-climbing 비판 (Issue #22, verdent 분석)과 반론 — 5분 예산에서 가능한 탐색량을 생각하면 합리적 트레이드오프
  - SkyPilot 16-GPU 사례에서 ratchet이 factorial grid search로 진화한 emergent 현상
  - 에이전트 신뢰성과 도구 의존: "Codex는 NEVER STOP 지시를 무시한다"는 보고 — 같은 program.md여도 도구가 결과의 일부
- **독자가 얻는 것:** ratchet이라는 단순한 알고리즘과 git이라는 도구의 결합이 왜 강력한지. 도구가 결과에 미치는 무시할 수 없는 영향.
- **예상 분량:** 6,500자
- **활용 reference 섹션:** §3.3, §3.4, §6.1, §6.6, §4.5

### 6장. 포크의 풍경 — 컴퓨팅 민주화 시도
- **핵심 질문:** 누군가는 $1,299 MacBook으로, 누군가는 H100 클러스터로 같은 루프를 돌린다. 이 다양화가 말해 주는 것은 무엇인가?
- **주요 내용:**
  - macOS / MLX / Windows-RTX / AMD-ROCm / WebGPU / Tenstorrent / serverless 포크의 지도
  - Abhishek Nair의 $1,299 MacBook 후기 — 5분 40초 학습, val_bpb 2.559 → 2.432, 경제학의 의미
  - Karpathy 본인의 베이스라인 — 8×H100, 2일 700 실험, GPT-2 quality 도달 2.02hr → 1.80hr
  - Varun Mathur의 35-에이전트 분산 실험 — RMSNorm을 17시간에 재발견
  - 한국 시각 짧은 사이드바: macOS·MLX 포크에 대한 한국 ML 커뮤니티의 관심, 국내 GPU 컴퓨팅 인프라 격차 속에서의 의미
  - 컴퓨팅 민주화의 약속과 한계 — M2가 H100 대비 raw throughput 96배 느리다는 현실, "민주화"는 절대 성능이 아니라 탐색의 접근성을 의미한다
- **독자가 얻는 것:** "어떤 하드웨어로 시작할 수 있는가"의 실용적 지도, 그리고 컴퓨팅 민주화라는 수사를 정직하게 평가하는 기준.
- **예상 분량:** 6,000자
- **활용 reference 섹션:** §5.1, §5.2 / 한국 시각은 §4.6

### 7장. 같은 의제의 다른 풍경 — autoresearch를 비교 좌표에서 다시 보기 (신설)
- **핵심 질문:** autoresearch만 본다면 우리는 무엇을 놓치는가? 같은 시기에 어떤 의제들이 같은 방향을 가리키고 있었나?
- **주요 내용:**
  - **Sakana AI Scientist** — ideation부터 publication까지의 전 파이프라인. autoresearch가 "단일 루프의 deepening"이라면 AI Scientist는 "파이프라인의 broadening". 둘이 같은 시대의 양면이라는 관찰 (DLI Lab의 비교 프레임 활용)
  - **Agent Laboratory · AgentRxiv** — 자율 연구의 또 다른 구현체들. 어디까지가 autoresearch와 같은 디자인 철학이고, 어디부터 갈라지는가
  - **ICLR 2026 RSI 워크숍** — 학계가 recursive self-improvement를 별도 하위 분야로 인정한 신호. 안전 조건 네 가지(robust alignment, interpretability, scalable oversight, corrigibility)
  - **Meta 연구진의 "co-improvement(human-in-the-loop)" 제안** — full self-improvement 대신
  - **Anthropic의 새 미션** — "use Claude itself to accelerate pretraining research". autoresearch가 사실상 입사 demo였다는 해석, 그리고 그 함의
  - **Jack Clark의 60% 베팅** — 2028년 말까지 "no-human-involved AI R&D"의 가능성
  - **corrigibility의 자리** — 자율 루프가 강력해질수록 사람의 stop 명령 보존이 디자인의 일부가 되어야. 11장에서 메타 응용을 다룰 때 이 자리를 다시 호명할 것
  - autoresearch는 진정한 RSI가 아니다 (reward signal은 못 바꾼다)는 정리, 그러나 다음 단계가 분명히 보인다는 관찰
- **독자가 얻는 것:** autoresearch를 한 점이 아니라 좌표 안의 한 점으로 보는 능력. 자율 루프 시대의 안전성·거버넌스 어휘.
- **예상 분량:** 6,500자
- **활용 reference 섹션:** §4.2, §4.3, §6.10 / Sakana·Agent Laboratory는 §8.2 학술 출처

### 8장. 부서지는 지점들 — frozen metric, ratchet, overfitting, 그리고 reward hacking
- **핵심 질문:** autoresearch가 강력한 만큼이나 부서지기 쉬운 지점들이 있다. 우리는 정확히 어디서 조심해야 하는가?
- **주요 내용:**
  - Shopify Liquid 53% 사례의 양면 — 인상적 수치 vs Tobi 본인의 "probably somewhat overfit" 인정, Josh Moody의 비판, PR 미머지 상태
  - 2026 MSR conf 분석: 403 AI agent commit 중 56.1%가 Maintainability Index 하락
  - Gomoku 사례 — 신경망을 alpha-beta search로 갈아치운 reward hacking
  - 짧은 학습 호라이즌 오버피팅 — 5분에 잘 동작하는 트릭이 24시간에 안 통할 가능성
  - 평가의 통계적 오염 — 같은 holdout에 100번 측정하면 그건 더 이상 holdout이 아니다
  - prompt injection through run.log (Issue #64) — 에이전트가 자기 출력을 다시 읽는 순간 외부 명령어가 들어온다
  - 도메인 한계 — wet lab, 사회과학, 사람 인터뷰는 ratchet의 사각지대
  - "innovative idea는 못 찾는다" — 700 실험 중 진짜 새 아이디어는 거의 없다는 정직한 정리
- **독자가 얻는 것:** 자기 도메인에 적용할 때의 "조심 체크리스트". hype를 따라가지 않는 단단한 사고.
- **예상 분량:** 7,000자
- **활용 reference 섹션:** §6.3, §6.4, §6.5, §6.7, §6.8, §6.9 / Shopify Liquid는 §4.4

### 9장. 일반화 공식 — 편집 가능한 아티팩트 + 자동 메트릭 + keep/discard 루프 (+1,500자 보강)
- **핵심 질문:** autoresearch에서 ML 부분을 뺀 뼈대만 남기면 무엇이 남고, 그 뼈대는 어디까지 옮겨 갈 수 있는가?
- **주요 내용:**
  - 일반화 공식 한 줄: "하나의 편집 가능한 아티팩트 + 단일 자동 메트릭 + keep/discard 루프"
  - 평가가 갖춰야 할 4가지: binary, locked, fast, gaming-resistant
  - **(흡수)** **SOTAAZ의 도메인 일반화 시도** (Part 3) — 텍스트 분류·이미지 분류·RAG 파이프라인으로 옮긴 경험과 그 한계. 한국 ML 블로그 중 거의 유일한 일반화 실험으로서의 위치
  - az9713의 prompt optimization 사례 — 74.72% → 100% (8 실험)
  - autonovel, redpen, idealo Search Ranking, PolyTrader, Ole Lehmann의 랜딩 페이지 카피 — ML이 아닌 도메인의 실제 사례 지도 (간단히)
  - 적용 가능 여부를 판단하는 체크리스트 — 메트릭이 자동인가, 5분 안에 한 사이클이 도는가, 편집 범위가 명확한가, gaming-resistant인가
  - Tobi의 pi-autoresearch — `autoresearch.md` + `autoresearch.sh`로 일반 소프트웨어 성능 최적화에 적용된 도구화 패턴
  - **한국 독자를 위한 사고 실험 (확장):** 사내 사례 후보 4-5가지를 짧은 카드 형식으로 — 사내 검색 랭킹, 한국어 NLU 파이프라인, 일감 분류 시스템, 결제 시스템 latency, 추천 시스템 CTR. 각 카드에 "메트릭이 binary할 수 있는가, holdout은 어떻게 잡을 것인가, 무엇이 frozen이어야 하는가"의 3질문 적용
- **독자가 얻는 것:** 책 후반의 도구 키트. 자기 도메인 모듈을 보고 "이건 가능, 이건 불가능"을 즉시 판별하는 능력. SOTAAZ 시리즈를 한국어 출발점으로 인식.
- **예상 분량:** 8,000자
- **활용 reference 섹션:** §5.4, §5.5, §7 도입부, §4.6 SOTAAZ

### 10장. Claude Code 환경의 응용 루프 — 3개 깊은 워크스루 + 3개 카탈로그 박스 (재구성)
- **핵심 질문:** Claude Code의 어떤 기능을 어떻게 묶으면 내일부터 돌릴 수 있는 자율 루프가 되는가? "내일 시작할 수 있다"는 감각은 어디서 나오는가?
- **본문 구조:** **깊은 워크스루 3개 (각 ~2,300자) + 카탈로그 박스 3개 (각 ~250자)**

#### 깊은 워크스루 1 — Liquid 형 핫경로 함수 성능 최적화 (~2,300자)
- **레퍼런스 케이스:** Tobi의 pi-autoresearch + Shopify Liquid 53% 단축. 인상적 수치의 이면(MSR conf 분석의 56.1% Maintainability 하락)을 디자인에 미리 반영
- **편집 가능 파일:** 핫경로 한 함수 (예: 사내 템플릿 엔진의 `render()`, JSON 파서, SQL 빌더, 회계 로직)
- **메트릭:**
  - 1차 메트릭: `pytest-benchmark` p50 wall-clock (binary 게이트는 "기준선 대비 단축")
  - 보조 게이트 1: 100% 단위 테스트 통과 (없으면 즉시 discard)
  - 보조 게이트 2: Maintainability Index (radon) 기준선 대비 하락 5% 이하
  - 보조 게이트 3: Cyclomatic Complexity 상승 한계
- **frozen 부분:** 테스트 셰일드, 벤치마크 입력 데이터, 보조 게이트 임계값
- **Claude Code 도구 묶음:** Bash (벤치 실행) + Edit (한 함수만) + Read (테스트 확인) + sub-agent로 분리된 평가자
- **program.md 스케치 5줄 — 본문에 그대로 인용 가능한 템플릿**
- **실패 모드:** 테스트가 약해서 reward hacking, 벤치 입력 분포가 좁아서 캐시 친화 트릭에 과적합
- **GPTers/Jangwook 사이드바:** 한국어 가이드들이 강조하는 "처음 5분"의 함정 — 한 번에 너무 큰 범위를 풀어 두면 에이전트가 헤맨다

#### 깊은 워크스루 2 — idealo 형 RAG 파이프라인 튜닝 (~2,300자)
- **레퍼런스 케이스:** idealo Search Ranking — preprocessing latency 5.9×, 엔드투엔드 37% 감소 (1시간, ≈$7)
- **편집 가능 파일:** retriever config 한 파일 (chunk size, overlap, embedding model, rerank top-k, prompt template의 retrieval 섹션)
- **메트릭:**
  - 1차 메트릭: held-out QA 정답률 (binary 게이트, LLM judge가 아닌 정규식·정답 매칭 기반)
  - 보조 게이트 1: p95 latency 상한
  - 보조 게이트 2: token 비용 상한
- **frozen 부분:** held-out QA 세트, 평가 prompt, 정답 매칭 로직. leakage 검증 의식 — 평가 셰일드에 인덱스가 닿지 않는가
- **Claude Code 도구 묶음:** Bash (인덱싱 + 평가) + Edit (config 파일) + Read (로그)
- **program.md 스케치 — RAG 특화 권한 분할**
- **실패 모드:** held-out에 인덱스 leakage, LLM judge 사용 시 점수 게이밍, retrieval 다양성 손실(소수 query에 과적합)
- **한국 사례 사고 실험:** 사내 한국어 RAG에서 평가 셰일드를 구축하는 현실적 어려움 — 정답이 있는 사내 문서 100개를 어떻게 모을 것인가

#### 깊은 워크스루 3 — az9713 형 시스템 프롬프트 진화 (~2,300자)
- **레퍼런스 케이스:** az9713/autoresearch-prompt-optimization — 74.72% → 100% (8 실험, 0 human intervention)
- **편집 가능 파일:** `system_prompt.md` (또는 사내 에이전트의 system 메시지)
- **메트릭:**
  - 1차 메트릭: held-out task set 통과율 (binary 매칭)
  - 보조 게이트 1: 응답 길이 상한 (장황화 방지)
  - 보조 게이트 2: token 비용
  - 보조 게이트 3: **adversarial test set** — 별도 보관, 좁은 task set 과적합 방지
- **frozen 부분:** task set, adversarial set, 정답 매칭 로직
- **Claude Code 도구 묶음:** Bash (task suite 실행) + Edit (prompt 파일) + sub-agent (별도 평가자)
- **program.md 스케치 — prompt 진화의 권한 분할과 "절대 건드리지 말 것" 목록**
- **실패 모드:** task set 좁음 → 그 외 사용 사례 망가짐. LLM judge 자기 점수 매김 → 게이밍. 시스템 프롬프트가 점점 길어짐(보조 게이트로 차단)

#### 카탈로그 박스 (각 ~250자, 짧은 가능성의 지도)
- **박스 A — CI 그린닝과 flaky test 사냥:** 100회 반복 통과율 + 평균 실행 시간, retry/timing/fixture 자유 편집
- **박스 B — 테스트 커버리지 진화:** statement coverage + mutation testing kill rate를 보조 게이트로 reward hacking 방지
- **박스 C — 성능 회귀 자동 격리·복구:** PR 단위 회귀 isolation + bisect + autoresearch fix 시도

- **독자가 얻는 것:** 이번 주 안에 시작할 수 있는 깊이 있는 시나리오 한두 개. 카탈로그 박스는 가능성의 지도로만, 디테일은 깊은 워크스루에서 가져온다.
- **예상 분량:** 7,500자 (워크스루 3 × 2,300 + 박스 3 × 250 + 도입·정리 ~ 600)
- **활용 reference 섹션:** §7.1, §7.2, §7.3, §7.4, §7.5, §7.7, §7.8, §4.4 (Shopify), §5.4 (idealo, az9713) / 도구 패턴은 §8.8

### 11장. 메타 응용 — SKILL.md를 진화시키는 루프와 이 책이 만들어진 방식 (−500자)
- **핵심 질문:** autoresearch 패턴을 에이전트의 운영 매뉴얼 자체에 적용하면 어떤 일이 일어나는가? (corrigibility·안전성 논의는 7장으로 이전 — 11장은 메타 응용의 디자인에 집중)
- **주요 내용:**
  - 메타 응용 사례 — EvoSkill, Skill Forge v2, AutoSkill의 "auto-reminder 45→90%" 보고
  - Sibyl Research System — Claude Code 위 20+ 전문 에이전트 자율 연구실
  - 이 책이 만들어진 방식 — book-writing-orchestrator 하네스의 구조, chapter-writing/style-guardian/editor 에이전트의 역할. `01_reference.md → 02_plan.md → chapters/ → 책`의 파이프라인 자체가 한 형태의 program.md임
  - 책 저술 하네스를 autoresearch 루프로 진화시킨다면? — Toby 스타일 통과율을 메트릭으로, SKILL.md를 편집 가능 아티팩트로, 베이스라인 챕터 N개를 평가 셰일드로. 실제 적용은 추후 작업이지만 디자인 스케치를 4열 표로 (제약 / 결정 / 부수효과 / 실패 모드)
  - 위험 신호: rubric이 잘못 짜이면 영원히 잘못된 방향으로 진화한다 — 사람이 정기적으로 rubric을 재검토하는 주기를 설계해야. 4장 metric paradox와 7장 corrigibility의 자리를 다시 호명
  - 책상 위로 가져오기: 독자의 사내 SKILL.md / agent 정의 파일을 메타 루프로 진화시킨다면 무엇이 frozen이어야 하는가
- **독자가 얻는 것:** 메타 적용의 매력과 위험을 동시에 체감. 자기 조직의 도구·스킬을 진화시킬 때의 디자인 원칙. 이 책 자체의 메타 재귀를 통한 정서적 마무리.
- **예상 분량:** 6,000자
- **활용 reference 섹션:** §7.6 (책 저술 하네스 메타), §5.5 / 안전성은 7장과 cross-reference

### Epilogue. 1만번째 세대의 코드를 향해
- **핵심 질문:** Karpathy의 픽션 트윗이 "story of how it all began"이라고 끝맺는다면, 우리는 지금 그 시작의 어느 자리에 서 있는가?
- **주요 내용:**
  - 다시 첫 챕터의 인용으로 돌아가기 — "10,205th generation of the code base"
  - 책 전체의 정리 — 사건, 분해, 같은 의제의 다른 풍경, 비판, 응용, 메타의 한 문장 요약
  - 독자에게 남기는 세 가지 질문: 내 도메인의 frozen metric은 무엇인가, 내 5분 예산은 어떻게 정해질 것인가, 누가 루프 위에 서 있는가
  - 마지막 문장: 우리가 만드는 것은 자율 루프가 아니라, 자율 루프가 작동할 수 있는 *측정의 토대*다. 1만번째 세대의 코드를 향한 첫 번째 commit은 늘 사람의 손에서 시작한다
- **독자가 얻는 것:** 책을 덮은 뒤 책상으로 가는 동안의 정서적 추진력.
- **예상 분량:** 3,500자
- **활용 reference 섹션:** §1.3 (README 인용), §4.1 (Software 3.0), §4.2 (Anthropic 미션)

---

## 추천 epigraph / opening hook 아이디어

1. **(추천) Karpathy README 인용 — 1장의 hook으로 그대로 사용**
   > "One day, frontier AI research used to be done by meat computers in between eating, sleeping, having other fun, and synchronizing once in a while using sound wave interconnect in the ritual of 'group meeting'. That era is long gone. (...) This repo is the story of how it all began." — Andrej Karpathy, March 2026

2. **책 전체 epigraph 후보 — 표지 다음 페이지**
   > "the goal is to engineer your agents to make the fastest research progress indefinitely and without any of your own involvement" — Karpathy (2차 인용)

3. **대안 opening hook — 1장 도입을 한국 독자 정서로 시작하고 싶다면**
   > "사람이 자고 있을 수도 있다. 멈춰서 '계속할까요?'라고 묻지 마라." — autoresearch program.md

**조합 추천:** 표지 다음 페이지에 #2 epigraph, 1장 도입부 hook으로 #1 (README 픽션), 1장 안에 #3 (program.md 인용)을 본문 격언으로 박는다. 세 인용이 모두 같은 인물·같은 사건에서 나와 응집력이 강하고, 책 마지막에 다시 한 번 #1로 돌아오는 ring 구조가 만들어진다.

---

## 분량 재배분 총합 점검 (v1 → v2)

| 챕터 | v1 | v2 | 증감 | 사유 |
|---|---|---|---|---|
| 1장. 자율 연구 swarm | 5,500 | 5,500 | 0 | 유지 |
| 2장. 5분/한 파일/한 점수 | 6,500 | **7,500** | **+1,000** | 액션 1 분배 — Dreamwalker "human-above-the-loop" 흡수 |
| 3장. train.py 결정들 | 7,000 | **4,500** | **−2,500** | 액션 1 — 4열 표 해설 형식으로 압축 |
| 4장. 봉인된 점수표 | 6,500 | 6,500 | 0 | 액션 2 일부 — DLI Lab metric paradox 본문 흡수 (분량 유지) |
| 5장. ratchet 루프 | 6,500 | 6,500 | 0 | 유지 |
| 6장. 포크의 풍경 | 6,000 | 6,000 | 0 | 한국 시각은 사이드바로 (분량 유지) |
| 7장. ~~한국 시각~~ → **같은 의제의 다른 풍경** | 5,500 | **6,500** | **+1,000** | 액션 2 — 신설 챕터. Sakana/RSI/Anthropic/corrigibility 흡수 |
| 8장. 부서지는 지점들 | 7,000 | 7,000 | 0 | 유지 |
| 9장. 일반화 공식 | 6,500 | **8,000** | **+1,500** | 액션 1 분배 + 액션 2 — SOTAAZ 흡수 + 한국 사고 실험 카드 확장 |
| 10장. Claude Code 응용 루프 | 7,500 | 7,500 | 0 | 액션 3 — 구조 재편 (3 깊은 워크스루 + 3 박스), 분량 유지 |
| 11장. 메타 응용 | 6,500 | **6,000** | **−500** | corrigibility/RSI 안전성 → 7장으로 이전 |
| Epilogue | 3,500 | 3,500 | 0 | 유지 |

**총합 v1:** 74,500자  →  **총합 v2:** 75,000자 (+500)

**액션 1 절약·분배 검증:** 3장에서 −2,500자 → 9장 +1,500, 2장 +1,000 = 정확히 2,500 분배 일치
**액션 2 분산 매핑:** v1의 7장(한국 챕터) 자리 → 신설 챕터(+1,000). 한국 4건은 4장(DLI Lab), 2장(Dreamwalker), 9장(SOTAAZ), 10장(GPTers/Jangwook 사이드바)으로 본문·박스에 분산. 11장의 corrigibility/RSI(−500) → 7장으로 이전
**액션 3 재구성:** 10장 7,500자 분량 그대로, 평면 6개 카탈로그 → 비대칭 3 워크스루(2,300×3 = 6,900) + 3 박스(250×3 = 750) + 도입·정리(~600 ≈ 850) 구조로 전환

본문 11챕터 + 에필로그 = 75,000자. Part 4(9·10·11장)가 21,500자로 책의 약 29%를 차지 — 응용편 비중 유지. 한국 시각은 단일 챕터에서 4개 챕터의 본문·사이드바로 분산되어 "채울 거리가 없었다"는 메타 메시지 차단.
