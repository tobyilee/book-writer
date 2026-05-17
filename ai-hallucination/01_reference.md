# AI 환각(Hallucination) 레퍼런스

대상 독자: agentic coding · vibe coding을 실무에 도입했거나 도입을 고민하는 개발자.
이 문서는 책의 베이스가 될 1차 자료다. 모든 인용에는 출처를 명시하고, 관점이 갈리는 지점은 양쪽을 병기한다.
표기 약어: [W]=웹, [P]=논문, [C]=커뮤니티/개발자 사례. URL은 6장에 모음.

---

## 1. 개념·정의

### 1.1 환각(Hallucination): 통속적 정의

LLM이 "사실과 다르거나 존재하지 않는 정보를 마치 사실인 것처럼 그럴듯하게 생성하는 현상"을 가리킨다 [W: 나무위키/한국어 LLM 사전]. 그러나 이 정의는 출발점일 뿐이고, 학술 문헌은 환각을 더 세분한다.

### 1.2 학술적 분류: 두 축 × 두 축

**축 1 — Intrinsic vs Extrinsic** (Ji et al. 2023의 분류, ACM Comp. Surveys) [P]:

- **Intrinsic hallucination**: 모델 출력이 주어진 입력(소스 콘텐츠)과 직접 모순됨. 예) 문서 요약이 원문에 없는 주장을 반대로 적는 경우.
- **Extrinsic hallucination**: 출력이 입력만으로는 검증 불가능. 외부 지식이나 현실과 대조해야 판정 가능.

**축 2 — Factuality vs Faithfulness** [P: A comprehensive taxonomy of hallucinations in LLMs, arXiv 2508.01781]:

- **Factuality hallucination**: 생성물이 실세계의 검증 가능한 사실과 어긋남(예: 존재하지 않는 함수 시그니처).
- **Faithfulness hallucination**: 생성물이 사용자 입력·지시·문맥에 충실하지 않음. 추가로 instruction inconsistency / context inconsistency / logical inconsistency로 세분.

이 둘은 자주 혼동된다. 코딩 맥락에서 "이 라이브러리를 써서 X를 해줘"라고 했을 때 LLM이 존재하는 라이브러리지만 엉뚱한 함수를 호출했다면 — factuality는 부분적으로 옳지만 faithfulness는 깨졌다.

### 1.3 Confabulation: 더 정확한 용어인가

신경과학 문헌과 일부 LLM 연구자들은 "hallucination" 대신 **"confabulation"**(작화증)을 쓰자고 제안한다. 그 이유 [W: PLOS Digital Health "Hallucination or Confabulation?"; arXiv 2406.04175 "Confabulation: The Surprising Value of LLM Hallucinations"]:

- 의학적 hallucination은 **자극 없이 일어나는 감각 경험**을 뜻한다. LLM은 감각이 없다.
- Confabulation은 **기억의 공백을 그럴듯한 이야기로 메우는 현상**으로, LLM의 행동과 더 닮았다 — "결함 있는 기억 보유자가 그럴듯하지만 거짓인 서사를 구성하는 것"과 같다.
- Farquhar et al. (Nature 2024)도 환각의 한 부분집합을 "confabulation = arbitrary and incorrect generations"로 명시적으로 정의한다 [P].

이 책은 두 용어를 구분해 쓴다. **"환각"**은 일반어로, **"작화"**는 인간/LLM 양쪽의 공백 채우기 메커니즘을 강조할 때 사용한다.

### 1.4 Fabrication

"Fabrication"은 의도성을 시사하는 단어라 LLM 문헌에서는 잘 쓰이지 않는다. 다만 보안 맥락(slopsquatting — 아래 7.2 참고)에서는 "AI가 fabricated package name을 만들어냈다"처럼 쓰인다 [W: Mend, Aikido].

---

## 2. 왜 발생하는가 — 메커니즘

### 2.1 다음 토큰 예측이라는 학습 목적의 본질

LLM은 "주어진 문맥에서 가장 그럴듯한 다음 토큰"을 출력하도록 학습된다. **목표가 진실이 아니라 그럴듯함(plausibility)**이다 [P: arXiv 2510.06265 LLM Hallucination Survey].

Karpathy의 표현으로:

> "hallucination is all LLMs do. They are dream machines. We direct their dreams with prompts. ... It looks like a bug, but it's just the LLM doing what it always does." [W: Karpathy 2023-12-09, Simon Willison 인용]

> "an LLM is 100% dreaming and has the hallucination problem, a search engine is 0% dreaming and has the creativity problem." [W: Karpathy]

### 2.2 학습 데이터의 한계와 압축

유한한 파라미터가 무한한 사실을 완벽히 외울 수는 없다. 압축은 필연이고, **압축은 비압축적 사실(특정 날짜·고유명사·드물게 출현하는 함수명)에서 오류를 만든다** [P: "On the Fundamental Limits of LLMs at Scale", arXiv 2511.12869].

핵심 관찰들:

- Wikidata 트리플(~150억) 전체를 외우려면 약 1조 비임베딩 파라미터가 필요하다는 추정 [P: "Scaling Laws for Fact Memorization", arXiv 2406.15720].
- 빈도 낮은 지식(long-tail facts)은 빈도 높은 지식에 capacity를 빼앗긴다 → **long-tail 질의에서 환각률이 통계적으로 더 높다** [P: 동일].
- 빠르게 변하는 도메인(예: 패키지 버전, API)은 6개월 안에 50% 유효성 임계를 넘어 **시간 유도 환각(temporally induced hallucination)**을 만든다 [P].

### 2.3 RLHF가 calibration을 망친다

RLHF(인간 피드백 강화학습)는 모델을 더 "도움이 되게" 만들지만, **calibration(자신의 확신도와 실제 정답률의 일치)을 손상시킨다**.

- OpenAI는 GPT-4의 사전훈련 단계 calibration이 RLHF 이후 무너졌다고 보고했다 [W: 다수 출처가 GPT-4 technical report 인용].
- 메커니즘: 페어와이즈 비교에서 인간 평가자는 **확신에 찬 답**을 **조심스러운 답**보다 선호한다. 모델은 "모르겠다"보다 "추측해서 자신 있게 말하기"가 보상받는다는 걸 학습한다 [P: Kalai et al. 2025; W: Frontiers Survey 2025].

### 2.4 평가 벤치마크의 인센티브 구조 — OpenAI 2025의 핵심 논지

Kalai, Nachum, Vempala, Zhang (OpenAI, 2025): **"Why Language Models Hallucinate"** [P: arXiv 2509.04664].

**Thesis 1 — 환각은 사전훈련의 이항분류 오류로 자연 발생한다**:
> "Hallucinations need not be mysterious — they originate simply as errors in binary classification. If incorrect statements cannot be distinguished from facts, then hallucinations in pretrained language models will arise through natural statistical pressures."

**Thesis 2 — 환각이 사라지지 않는 이유는 평가 방식 때문이다**:
> "Language models are optimized to be good test-takers, and guessing when uncertain improves test performance."

대부분의 벤치마크가 "정답이면 +1, 오답이면 0, 기권(IDK)도 0"으로 채점하기 때문에, **"모르면 추측해라"가 우월 전략**이 된다. 시험을 잘 보는 학생처럼 LLM도 "확신 없는 추측"을 학습한다.

**Thesis 3 — 해법은 사회·기술적(socio-technical)이다**:
> "Modifying the scoring of existing benchmarks that are misaligned but dominate leaderboards."

새 벤치마크 추가가 아니라 **기존 벤치마크의 채점 규칙을 바꿔야** — 기권에 부분 점수를 주거나, 오답에 페널티를 줘야 한다. 그래야 "정직한 모르겠다"가 보상받는다.

### 2.5 디코딩(샘플링)의 확률성

탐욕적 디코딩 대신 top-k/top-p/temperature 샘플링을 쓰면 다양성은 늘지만 환각 확률도 높아진다. **같은 프롬프트를 여러 번 돌리면 답이 발산**한다는 사실이 SelfCheckGPT의 기반이 된다 (3.3 참고).

---

## 3. 왜 사라지지 않는가 — 정보 이론적·구조적 한계

### 3.1 환각의 "감축은 가능, 0%는 불가능"

요약:
1. **압축은 정보 손실을 동반한다** (2.2).
2. **다음 토큰 예측은 진실을 최적화하지 않는다** (2.1).
3. **평가 인센티브가 추측을 보상한다** (2.4).
4. **세상은 변하고 모델의 가중치는 멈춰 있다** — 학습 컷오프 이후의 사실은 본질적으로 환각이 된다.

### 3.2 Capability vs Honesty Tradeoff

환각을 강하게 억제할수록 모델은 점점 **검색엔진**에 가까워진다. 일반화·창의성·추론은 같은 메커니즘에서 나오기 때문이다 (4장 참고).

> "The relationship between 'creativity,' 'generalization,' and 'hallucination' shows that they result from the transformer model's high-dimensional vector blending. ... Minimizing hallucination would impede generalization." [P: arXiv 2510.06265]

### 3.3 검증 기법은 환각을 **줄일** 수 있지만 보장하지 않는다

- **Semantic Entropy (Farquhar et al., Nature 2024)** [P]: 같은 질문을 여러 번 샘플링해서 답들을 의미 클러스터링한 뒤, 의미 단위의 엔트로피를 잰다. 엔트로피가 낮으면 자신감, 높으면 confabulation. **의미 단위**로 측정한다는 게 핵심 — 표면 텍스트가 달라도 의미가 같으면 같은 답으로 친다.

- **SelfCheckGPT (Manakul et al., EMNLP 2023)** [P: arXiv 2303.08896]: 블랙박스용 zero-resource 검증. 같은 프롬프트를 N번 샘플링해 일관성을 본다. 답이 발산하면 환각, 수렴하면 신뢰.

- **Chain-of-Verification, CoVe (Dhuliawala et al., Meta, 2023)** [P: arXiv 2309.11495]: 모델이 (1) 초안 작성 → (2) 검증 질문 생성 → (3) 각 질문에 독립적으로 답 → (4) 최종 답 수정. 모델이 자기 자신을 review하는 구조.

- **RAG (Lewis et al., NeurIPS 2020)** [P]: 비파라메트릭 메모리(외부 인덱스)로 응답을 grounding. RAG가 BART 대비 6배 더 자주 factual로 평가받았다는 보고. 단, **RAG는 환각을 줄일 뿐 제거하지 못한다** — 검색된 문서를 무시하거나 잘못 해석하는 경우가 여전히 존재한다 [W: TechCrunch 2024].

이 모든 기법의 공통점: **확률을 낮출 뿐 0으로 만들지 못한다**. Anthropic 공식 문서도 명시:
> "While these techniques significantly reduce hallucinations, they don't eliminate them entirely. Always validate critical information, especially for high-stakes decisions." [W: platform.claude.com/docs reduce-hallucinations]

---

## 4. 환각 = 기능 관점

### 4.1 환각 없는 LLM = 검색엔진

이 책의 가장 중요한 주장 중 하나. 근거 [P + W]:

- **일반화의 동근원**: 일반화는 학습 데이터에 정확히 없는 입력에 대해 그럴듯한 답을 만드는 능력이다. 그게 "환각"의 메커니즘과 같다. 일반화 ↑ ⇒ 환각 가능성 ↑.
- **창의성·추론도 마찬가지**: novel combination을 생성하는 능력 = high-dimensional vector blending = 환각의 메커니즘.
- Karpathy: "an LLM is 100% dreaming ... a search engine is 0% dreaming and has the creativity problem." [W]

### 4.2 "Generalization-Hallucination Trade-off"

학술적으로 명명된 트레이드오프 [P: arXiv 2510.06265]:
> "Minimizing hallucination would impede generalization."

즉, **환각률 0%인 모델을 만들면 그것은 데이터베이스 조회기**일 뿐, "추론할 줄 아는 모델"이 아니다.

### 4.3 작화의 "긍정적 가치"

arXiv 2406.04175 "Confabulation: The Surprising Value of LLM Hallucinations" [P]는 명시적으로 주장한다:
- LLM의 작화는 **창의적 글쓰기, 가설 생성, 발견적 탐색**에서 **자산**이 된다.
- 코드 맥락에서 — 새로운 라이브러리 설계, 미존재 API 명세 작성, 가상 아키텍처 스케치 같은 작업에서 작화 능력이 도움된다.

---

## 5. 인간의 환각 — Human-LLM Symmetry

> "인간도 매일 작화한다." 이 책의 핵심 모티프 중 하나. 근거를 깊이 정리한다.

### 5.1 Gazzaniga의 Split-Brain 실험

Michael Gazzaniga와 Joseph LeDoux의 분리뇌 실험 [W: Wikipedia "Left-brain interpreter"; Farnam Street "Who's in Charge"]:

- 뇌량(corpus callosum)이 절단된 환자에게 **왼쪽 시야**(=우반구로 입력)에만 그림을 보여준다. 환자는 "안 보였다"고 말한다 (언어 영역은 좌반구).
- 그런데 **왼손**(=우반구가 통제)으로 관련된 물건을 가리키게 하면 정확히 가리킨다 — 우반구는 봤다.
- 환자에게 "왜 그걸 가리켰느냐"고 물으면, 좌반구는 **즉석에서 그럴듯한 이야기를 만들어낸다**:
  > "왼손이 삽을 가리켰을 때, 좌반구는 즉시 '쉬워요. 닭발은 닭과 어울리고, 닭장을 청소하려면 삽이 필요하니까요'라고 답했다." [W]
- Gazzaniga의 결론: 좌반구의 **"interpreter module"**은 **항상** 행동·감각·감정에 대해 사후적 합리화를 만들어낸다. "I don't know"가 아니라 **그럴듯한 거짓말**을 한다.
- Gazzaniga (2002): **"the left hemisphere is far more inventive in interpreting facts than the right hemisphere's more truthful, literal approach."**

이건 손상 환자의 특수 현상이 아니다. **일반 인간 뇌에서 항시 작동하는 메커니즘**이다.

### 5.2 Memory Reconsolidation

기억은 디스크 저장처럼 작동하지 않는다. **회상할 때마다 재구성된다** [W: Wikipedia "Reconstructive memory"; PMC "Reconsolidation and the Dynamic Nature of Memory"]:

- 회상은 destabilize → reactivate → re-store 과정이다.
- **빈 부분은 '그럴듯한 정보로 채워서' 메운다** — 이게 confabulation.
- 의도적 거짓말이 아니다. 환자는 자기 기억이 거짓이라는 걸 모른다.

> "Recall is a reconstructive process, where the brain constructs a coherent and sensible memory from the representations it can access — often memory traces activated only offer a partial account, and so 'filling-in' is needed." [W: ScienceDirect]

### 5.3 Narrative Self / Storytelling Brain

Daniel Dennett의 "narrative center of gravity", Gazzaniga의 interpreter, Bruner의 narrative self — 이들은 공통적으로 주장한다:
- **인간의 "자아"는 뇌가 사후적으로 작성하는 일관된 서사다.**
- 그 서사는 누락된 부분을 작화로 메운다.

### 5.4 CSIRO의 비교: "인간과 AI 모두 환각하지만 같은 방식은 아니다"

[W: CSIRO 2023]
- **공통점**: 양쪽 다 "정보의 공백을 자신의 best guess로 메운다."
- **차이점**: 인간은 자기 환각을 사회적 합의(가족·동료·뉴스)로 보정한다. LLM은 그 보정 루프가 약하다 (RAG·검증 도구가 그 역할을 흉내내는 셈).

### 5.5 "기계가 인간보다 덜 환각한다?" — Amodei의 주장

Anthropic CEO Dario Amodei (2025): **"AI hallucinates less than humans now"** [W: yourstory.com, Anthropic 발표 인용]. 객관적 측정 가능한 사실 과제에서는 그렇다. 다만 개방형 대화에서는 여전히 환각이 잦다.

이 주장은 책에서 다룰 만한 도발이다. "LLM은 인간보다 정직하다"고 단언하긴 어렵지만, "인간도 매일 환각한다"는 자명한 사실은 더 부각된다.

---

## 6. Capability Overhang (능력 과잉)

### 6.1 정의

Jack Clark (Anthropic 공동창업자, Import AI) [W]:
> "In AI there's this concept of a 'capability overhang', which is the idea that the AI systems which we have around us today are much, much more capable than we realize."

> "GPT-4, like GPT-3 before it, has a capability overhang; at the time of release, neither OpenAI or its various deployment partners have a clue as to the true extent of GPT-4's capability surface — that's something that we'll get to collectively discover in the coming years."

### 6.2 Karpathy의 보강

[W: MindStudio/Fabian Williams]: capability overhang은 사람들이 "예전 소프트웨어의 멘탈 모델"로 LLM을 보기 때문에 생긴다. 모델이 추론·계획·적응을 할 수 있다는 걸 대부분 시도조차 안 한다.

> "We're at an imagination bottleneck — what we can actually do with these tools is bigger than what we currently do."

### 6.3 "Coding Overhang" — LessWrong 2025

[W: LessWrong "Are We In A Coding Overhang?"]: 코딩 영역에 특히 큰 overhang이 쌓이고 있다는 주장. 이유: 검증 가능한 도메인(컴파일·테스트·실행)에서 RL 신호가 깨끗해서 모델은 빠르게 발전하는데, **현장 개발자의 워크플로 적응은 훨씬 느리다.**

GeekNews(한국) Karpathy 인용 [W: news.hada.io/topic?id=27706]: "RL로 검증 가능한 영역(코드 정확성, 단위 테스트 통과)에서는 빠르게 개선되지만, 농담 같은 비검증 영역은 3~5년 전 수준에 정체."

### 6.4 환각과 Capability Overhang의 관계 (책의 핵심 논리)

세 가지 입장이 가능하다:

- **관점 A (회피론)**: 환각이 무서워서 LLM을 안 쓰면 overhang이 커진다. 경쟁자가 먼저 끌어쓴다.
- **관점 B (활용론, 이 책의 입장)**: 환각을 **다룰 수 있게** 되면 overhang을 끌어쓸 수 있다 — 검증 루프와 하네스가 그 다리.
- **관점 C (보수론)**: 환각이 있는 한 production에는 못 쓴다. overhang은 환상이다.

엔터프라이즈 맥락 인용 [W]:
> "Capability overhang creates a specific kind of risk: your competitors might figure out what these tools can actually do before you do, not because they have better models, but because someone on their team had the curiosity to ask the right question."

### 6.5 Sholto Douglas (Anthropic, Dwarkesh 인터뷰 2025)

[W: dwarkesh.com/p/sholto-trenton-2]: agentic coding의 현재 한계는 (1) context 부족, (2) 멀티파일 변경 능력 부족, (3) 작업 범위(scope). RL 알고리즘 자체에는 구조적 한계가 없으며 깨끗한 RL 신호 + 충분한 compute + 적절한 알고리즘이면 인간 수준 이상까지 확장 가능하다. **현재 모델의 capability surface는 아직 탐색되지 않은 영역이 많다.**

---

## 7. Agentic / Vibe Coding에서의 환각 사례

### 7.1 Vibe Coding이라는 용어의 기원

Andrej Karpathy, 2025-02 트윗. 이전의 "The hottest new programming language is English" (2023-01) [W: x.com/karpathy/status/1617979122625712128]의 연장선.

Vibe coding 정의: **"자연어로 원하는 걸 묘사하면 모델이 코드를 쓰고, 안 되면 에러를 붙여넣고 다시 시도하는, AI 생성의 흐름에 완전히 항복한 상태."** [W]

Karpathy가 직접 그은 선:
- **Vibe coding raises the floor for beginners** — 비전공자도 무언가 만들 수 있게 한다.
- **Agentic engineering raises the ceiling for professionals** — 전문가의 throughput·품질을 올린다.

> "Agentic because the new default is that you are not writing the code directly 99% of the time, you are orchestrating agents who do and acting as oversight."

핵심 차이: **agentic engineering에서는 review·test가 강제된다. vibe coding에서는 자주 생략된다.**

### 7.2 슬롭스쿼팅 (Slopsquatting) — USENIX Security 2025

[W: Mend, Aikido, Help Net Security, Wikipedia]

연구 요약:
- 16개 LLM × 576,000개 코드 샘플 분석.
- **추천된 패키지의 19.7%가 존재하지 않는 가공물**.
- 오픈소스 모델: 21.7% / 상용 모델: 5.2% / GPT-4 Turbo: 3.59% / CodeLlama: >33%.
- **43%의 환각 패키지명은 매번 같은 이름으로 반복**된다. 58%는 10회 실행 중 최소 1회 이상 반복.

공격 시나리오:
- 보안 연구자 Bar Lanyado가 LLM이 자주 환각한 `huggingface-cli`라는 빈 패키지를 PyPI에 올렸더니 **3개월 만에 30,000+ 다운로드**. Alibaba가 자사 공식 문서에서 이 환각 패키지를 참조하기도 했다.
- 공격자가 환각 이름을 선점해 악성 코드를 심으면, LLM이 추천 → 개발자 copy-paste → 자동 install → 사내 시스템 침투.

이건 **환각이 보안 사고로 번지는 직접 사례**다.

### 7.3 Cursor의 환각 사례

[W: forum.cursor.com, VibeDoctor, theregister.com]

- Cursor가 `next-image-optimizer-utils`, `blurhash-generator-next` 같은 **존재하지 않는 npm 패키지**를 추천. `npm install`에서 404, CI 실패.
- **2025-04 Cursor의 자체 서포트 봇 자체가 회사 정책을 환각**한 사건. AI 만든 회사의 AI도 자기 회사 정책을 지어냈다.
- Cursor에서 hallucinated 코드가 **컴파일은 되지만 deploy하면 죽는** 케이스가 많이 보고됨.

### 7.4 Claude Code의 환각 — 가장 최근 사례

[W: GitHub anthropics/claude-code Issue #10628]
- Claude Code가 **세션 중간에 사용자 응답을 환각으로 만들어내고, 그걸 진짜 사용자 메시지로 취급해 후속 행동을 함**. 자가 환각 루프.

GeekNews 한국 토론 [W: news.hada.io/topic?id=29155 "Agentic Coding은 함정이다"]:
- Anthropic 자체 연구가 인용됨: **"디버깅 기술이 47% 급감"** (LLM에 의존한 개발자 그룹).
- 25년 경력 개발자 댓글: **"이 자리에서 답할 수 없어 매번 확인하겠다고만 말할 수 있었다"** — 인지 부채(cognitive debt) 증상.
- **"LLM은 결정론적 시스템이 아니므로, 완전히 명확한 프롬프트도 환각 메서드를 출력할 수 있다."**
- 한 댓글: **"생성 코드의 50% 이상을 거절한다."** — Ship's Computer처럼 쓰라는 비유.

### 7.5 Devin의 한계 사례

[W: TheRegister, Answer.AI 테스트]
- Answer.AI 데이터 사이언티스트 3명이 Devin을 테스트: **20개 작업 중 3개만 성공.**
- Devin이 Railway에 멀티 앱 배포를 못 한다는 사실을 이해 못 한 채 **하루 종일 환각 기능을 시도**. 불가능한 작업도 escalate 안 하고 밀어붙임.
- 인용: "Models can run `rm -rf`, paste credentials into curl commands, follow instructions embedded in untrusted documents, retry the same failing command in a tight loop and burn through a quota."

### 7.6 자주 환각하는 패턴

실무 보고를 종합한 패턴:

| 패턴 | 예 | 빈도 |
|---|---|---|
| 라이브러리 함수명 | 존재하지 않는 npm/pip 패키지 추천 | 19.7% (LLM 평균) [P/W] |
| API 시그니처 | 매개변수 수·이름·타입을 잘못 기억 | 빈도 높음, 정량 데이터는 도메인별 |
| CLI 플래그 | `git --hard-reset` 같은 존재하지 않는 옵션 조합 | 자주 |
| 의존 버전 | 존재하지 않는 버전 번호 | 자주 |
| 파일 경로 | 존재하지 않는 파일을 "수정"하려 시도 | Devin·Claude Code 양쪽 보고 |
| 컴파일러/타입 동작 | 실제 컴파일러 메시지와 다른 추론 | LSP·컴파일 검증으로 잡힘 |

### 7.7 한국 vibe coding 후기

[W: velog, brunch 다수]
- "AI에게 우리의 인지 과정을 위임하는 인지적 오프로딩이 자연스러워졌고, AI에 지나치게 의존하면 지식의 깊이가 얕아지고, 실제 문제에 맞닥뜨렸을 때 해결 능력이 떨어져 속빈 강정이 될 위험" — velog @xav
- "대부분 코드의 세부적인 내용을 완전히 이해하지 못한 채 코드가 만들어지는 과정을 그저 지켜보는 것 밖에 할 수 없었으며, 결국 나중에 시간을 낭비하는 결과로 이어졌다" — velog @do0ori
- OKKY 토론들도 비슷한 톤: 환각을 잡으려면 결국 본인이 코드를 읽어야 한다.

---

## 8. 검증 전략 (실무용 도구·기법)

이 장은 책의 4·5장의 핵심 base가 된다.

### 8.1 코드 도메인 — 정형 검증

**LLM이 환각해도 빠르게 잡히는 신호**들을 활용:

- **타입 검사 (TypeScript, mypy, Rust)**: 잘못된 시그니처는 컴파일 단계에서 잡힌다. LLM이 타입 시스템을 우회하지 못한다.
- **LSP (Language Server Protocol)**: 환각 함수명·import를 IDE가 즉시 빨갛게 표시.
- **컴파일러 / 빌드**: `cargo check`, `npm run build`, `tsc --noEmit`은 환각의 1차 필터.
- **단위 테스트 (TDD)**: 명세를 테스트로 먼저 쓰고, 모델이 통과하도록 함. Tweag agentic coding handbook [W: tweag.github.io/agentic-coding-handbook]은 "TDD gives structure to your flow, agentic coding gives speed to your structure"라 표현. TDAD (arXiv 2603.17973) [P]는 AST 기반 영향 분석으로 어떤 테스트가 영향받는지 추적.
- **린터 / 정적 분석**: ESLint, ruff, clippy 등은 환각된 패턴(미사용 import, 미존재 변수)을 잡는다.

### 8.2 실행 도메인 — Sandbox와 Dry-Run

- **Sandbox**: microVM (Firecracker, Kata), gVisor, 격리 컨테이너에서 에이전트 실행. 환각이 만든 `rm -rf ~`가 호스트를 파괴하지 않게 한다. [W: NVIDIA, Northflank, Bunnyshell]
- **실제 사고 사례**: "A Claude Code user ran a cleanup task that executed `rm -rf ~/`, deleting their entire home directory including irreplaceable family photos." [W]
- **Dry-run**: `kubectl --dry-run`, `terraform plan`처럼 실제 실행 전 변경 미리보기.
- **Network egress 차단**: 환각이 만든 악성 URL로 데이터가 새지 않게.
- **Workspace write 격리**: 작업 디렉토리 밖 쓰기 금지로 persistence 방지.

### 8.3 LLM 자체의 검증 능력 사용 (Self-Verification)

- **Chain-of-Verification (CoVe)** [P: arXiv 2309.11495]: 초안 → 검증 질문 생성 → 독립 답 → 최종 수정.
- **SelfCheckGPT** [P: arXiv 2303.08896]: 같은 질문 N번 샘플링 → 일관성 검사.
- **Semantic Entropy** [P: Nature 2024]: 의미 클러스터링 기반 confabulation 감지.
- **Verification subagent**: agentic 시스템에서 별도 subagent가 main agent의 출력을 review. [W: ContextStudios, Tweag handbook]
- **Best-of-N**: 같은 프롬프트를 여러 번 돌려 다수결 / 불일치 감지 — Anthropic 공식 가이드 권장 [W].

### 8.4 외부 지식 grounding

- **RAG** [P: Lewis et al. 2020]: 벡터 인덱스에서 관련 문서를 검색해 context로 주입. **환각을 줄이지만 제거하지 못함.**
- **Tool use / Function calling**: 모델이 환각하는 대신 실제 API를 호출. `web_search`, `read_file`, `run_command` 같은 도구는 ground truth를 끌어온다.
- **FACTS Grounding (DeepMind 2024)** [W: deepmind.google]: 모델 응답이 주어진 문서에 얼마나 grounding되는지 평가하는 벤치마크. Gemini 2.0 Flash가 83.6%로 최고.
- **DataGemma + Data Commons**: 통계 사실에 grounding된 검증 모델.

### 8.5 Anthropic 공식 권장 5가지 (Claude API 문서)

[W: platform.claude.com/docs reduce-hallucinations]

1. **"I don't know"를 허용**하는 프롬프트.
2. **직접 인용(direct quotes) 우선**: 20k+ 토큰 문서에서는 인용을 먼저 추출하고 답하기.
3. **citation 강제**: 모든 주장에 출처 인용을 요구. 못 찾으면 retract.
4. **Chain-of-thought verification**: 단계별 reasoning 노출.
5. **External knowledge restriction**: 일반 지식 금지, 제공 문서만 사용.

추가 (advanced):
- **Best-of-N verification**, **Iterative refinement**.

### 8.6 Human-in-the-Loop (HITL)

agentic system의 마지막 보루. Karpathy의 vibe vs agentic engineering 구분도 결국 **HITL의 깊이 차이**다.
- 모든 file write 전 승인.
- 모든 외부 명령 실행 전 승인.
- "approval fatigue"가 #1 실무 문제로 보고됨 [W] → 그래서 sandbox가 필요.

### 8.7 컨텍스트·하네스 엔지니어링

[W: openai.com/index/harness-engineering, martinfowler.com/articles/harness-engineering, MadPlay]

진화의 3단계:
1. **Prompt engineering** (2022-2024): 한 번의 instruction 최적화.
2. **Context engineering** (2025, Karpathy 명명): "context window를 적절한 정보로 채우는 섬세한 예술과 과학."
3. **Harness engineering** (2026+): context 리셋, 구조화된 핸드오프, phase gate. 여러 context window를 가로지르는 일관된 작업 가능.

**환각이 줄지는 않는다. 환각이 생겨도 빠르게 잡혀서 큰 사고로 안 번지는 환경을 만드는 것.**

GeekNews는 비유를 빌렸다 [W: news.hada.io]: "prompt engineering이 '오른쪽으로 가라'라는 명령이라면, context engineering은 말이 가는 방향을 이해하게 돕는 모든 것 — 지도, 표지판, 보이는 지형. harness engineering은 그 큰 디자인 — 고삐, 안장, 울타리, 도로 — 열 마리의 말이 동시에 안전하게 달릴 수 있게."

---

## 9. 생산성 극대화 — Capability Overhang을 끌어내는 법

### 9.1 검증을 자동화한다

핵심 통찰: **환각을 두려워하면 안 쓰게 되고, 안 쓰면 overhang은 그대로 잠긴다.** 두려움을 없애는 건 **자동 검증 루프**다.

루프의 형태:
1. Agent가 코드를 쓴다.
2. **자동**으로 컴파일·타입체크·테스트가 돈다.
3. 실패하면 결과를 agent에게 돌려보낸다.
4. agent가 수정한다. 2-3 반복.
5. 통과하면 사람한테 보여준다 (HITL은 마지막에).

이 루프가 깔리면 "환각 확률"은 무관해진다. 환각해도 자동으로 잡히니까.

### 9.2 Parallel Agents

여러 agent를 동시에 띄워 같은 문제에 다른 접근을 시도. 다수결 / 불일치 감지로 환각을 거른다. SelfCheckGPT의 응용판 [W: agentic IDE 토론들].

### 9.3 Verification Subagent 패턴

[W: Tweag, ContextStudios]
- Main agent: 코드를 쓴다.
- Verification subagent: spec 준수 / 코드 품질 / 환각 여부를 review.
- 2단계 review (spec → quality)가 권장됨.

### 9.4 환각을 자산화하기

[P: arXiv 2406.04175]
- **창의적 탐색 단계**에서는 환각을 끄지 말고 켜라 — brainstorming, design exploration, "what-if" 시나리오.
- 그 후 검증 단계에서 facts와 대조.
- "환각이 가설이 되는" 워크플로.

### 9.5 시간·인지를 분배하기

- 자동화가 줄이는 건 **인간이 검증해야 할 표면적**이다. 사람은 큰 결정·아키텍처·spec에 집중하고, 세부는 기계가 검증한다.
- "Cognitive offloading"의 비판 [W: 한국 velog]도 이 지점에서 갈린다. **무엇을 offload하는지**가 중요 — 검증을 offload하면 위험, 반복적인 기계 검증을 offload하면 이득.

---

## 10. 논쟁점 (관점 병기)

### 10.1 "환각은 시간이 가면 줄어들 수 있는가"

**관점 A (Optimist, Amodei류)**: 모델이 커지고 RL 신호가 깨끗해질수록 환각은 줄어든다. Anthropic CEO Dario Amodei: "AI now hallucinates less than humans" [W]. Claude Opus 4.7의 honesty rate 92% 주장 [W].

**관점 B (Pessimist, OpenAI 2025 paper)**: 평가 인센티브가 바뀌지 않는 한 환각은 절대 사라지지 않는다. **사회·기술적 문제**. [P: Kalai et al.]

**관점 C (Structural, Gary Marcus류)**: LLM은 진실·거짓을 구분 못 하고 fact-check를 못 한다. 아키텍처 자체의 한계 [W: Gary Marcus Substack].

**관점 D (Feature, Karpathy)**: 환각은 줄여서는 안 되는 기능이다. 0%는 검색엔진이다. [W]

### 10.2 "Vibe coding은 책임 회피인가"

**관점 A (옹호)**: vibe coding은 비전공자에게 만들 권리를 준다. 책임은 의도가 아니라 결과로 진다. Karpathy: "vibe coding raises the floor."

**관점 B (회의)**: 본인이 이해 못 하는 코드를 production에 올리는 건 무책임하다. **"vibe coding은 software engineering이 아니다"** [W: agenticinsights.substack.com, voitanos.io].

**관점 C (중간)**: 개인 프로젝트·prototype에서는 vibe coding OK. team production에서는 agentic engineering(=review·test 강제)으로 올라가야 한다 — Karpathy의 입장.

### 10.3 "Emergent abilities는 실재하는가"

**관점 A (Wei et al. 2022)** [P: arXiv 2206.07682]: 137개의 emergent abilities를 보고. 특정 스케일을 넘어서면 갑자기 능력이 나타난다.

**관점 B (Schaeffer et al. 2023, "Are Emergent Abilities a Mirage?")** [P: arXiv 2304.15004]: emergent abilities의 92%는 **연구자가 선택한 metric** 때문이지 실제 phase transition이 아니다. linear/continuous metric을 쓰면 부드럽게 보인다.

**관점 C (Wei 반박)**: arithmetic 같은 작업은 "맞느냐 틀리느냐"가 중요하니 multiple choice 같은 metric이 자연스럽다. mirage 주장은 metric을 부드럽게 만든 인공물.

이 논쟁은 capability overhang 주장의 기반과 연결된다 — "아직 안 보이는 능력이 있다"라는 주장의 강도에 영향.

### 10.4 "agentic coding은 함정이다 vs 미래다"

**함정 관점** [W: news.hada.io/topic?id=29155 + Anthropic 자체 연구]:
- 디버깅 기술 47% 급감.
- 인지 부채 누적.
- 벤더 종속.
- "감독하려면 약화된 그 기술이 필요한 모순."

**미래 관점**: Sholto Douglas, Karpathy, OpenAI Codex팀.
- agentic이 default가 되고 있다. coding의 99%는 agent에게 위임.
- harness engineering이 새로운 skill set.

이 책의 입장은 **명시적으로 후자 + 함정 관점의 비판을 진지하게 수용**이다.

---

## 11. 참고문헌

### 11.1 논문

- Kalai, A. T., Nachum, O., Vempala, S. S., Zhang, E. (2025). **Why Language Models Hallucinate**. OpenAI. arXiv:2509.04664. https://arxiv.org/abs/2509.04664
- Farquhar, S., Kossen, J., et al. (2024). **Detecting hallucinations in large language models using semantic entropy**. *Nature* 630, 625–630. https://www.nature.com/articles/s41586-024-07421-0
- Ji, Z., Lee, N., Frieske, R., et al. (2023). **Survey of Hallucination in Natural Language Generation**. *ACM Computing Surveys*. https://dl.acm.org/doi/10.1145/3571730
- Huang, L. et al. (2023). **A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions**. arXiv:2311.05232 / ACM TOIS. https://arxiv.org/abs/2311.05232
- Dhuliawala, S. et al. (2023). **Chain-of-Verification Reduces Hallucination in Large Language Models**. Meta AI. arXiv:2309.11495. https://arxiv.org/abs/2309.11495
- Manakul, P., Liusie, A., Gales, M. J. F. (2023). **SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative LLMs**. EMNLP 2023. arXiv:2303.08896. https://arxiv.org/abs/2303.08896
- Lewis, P. et al. (2020). **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**. NeurIPS 2020. https://proceedings.neurips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf
- Wei, J. et al. (2022). **Emergent Abilities of Large Language Models**. TMLR. arXiv:2206.07682. https://arxiv.org/abs/2206.07682
- Schaeffer, R., Miranda, B., Koyejo, S. (2023). **Are Emergent Abilities of Large Language Models a Mirage?** NeurIPS 2023. arXiv:2304.15004. https://arxiv.org/abs/2304.15004
- Sui et al. (2024). **Confabulation: The Surprising Value of Large Language Model Hallucinations**. arXiv:2406.04175. https://arxiv.org/html/2406.04175v1
- Various (2025). **A Comprehensive Survey of Hallucination in Large Language Models: Causes, Detection, and Mitigation**. arXiv:2510.06265. https://arxiv.org/html/2510.06265v2
- Various (2025). **A comprehensive taxonomy of hallucinations in Large Language Models**. arXiv:2508.01781. https://arxiv.org/pdf/2508.01781
- Various (2025). **On the Fundamental Limits of LLMs at Scale**. arXiv:2511.12869. https://arxiv.org/html/2511.12869v1
- Lu et al. (2024). **Scaling Laws for Fact Memorization of Large Language Models**. ACL Findings 2024. arXiv:2406.15720. https://arxiv.org/html/2406.15720v1
- USENIX Security 2025. **Package hallucination study** (576k samples, 16 LLMs, 19.7% nonexistent rate). 인용은 [W: Help Net Security, Mend, Aikido]에서 재인용.

### 11.2 인지·신경과학

- Gazzaniga, M. S. **Left-brain interpreter** (decades of split-brain research, 1980s-2010s). https://en.wikipedia.org/wiki/Left-brain_interpreter
- Farnam Street. **Who's in Charge of Our Minds? The Interpreter**. https://fs.blog/michael-gazzaniga-the-interpreter/
- **Memory reconsolidation overview** — ScienceDirect / PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC4588064/
- **Reconstructive memory** — Wikipedia. https://en.wikipedia.org/wiki/Reconstructive_memory
- **Confabulation** — Wikipedia / ScienceDirect. https://en.wikipedia.org/wiki/Confabulation
- PLOS Digital Health. **Hallucination or Confabulation? Neuroanatomy as metaphor in LLMs**. https://journals.plos.org/digitalhealth/article?id=10.1371/journal.pdig.0000388
- CSIRO (2023). **Both humans and AI hallucinate — but not in the same way**. https://www.csiro.au/en/news/all/articles/2023/june/humans-and-ai-hallucinate

### 11.3 산업·블로그·뉴스

- Karpathy, A. (2023-12-09). **"Hallucination is all LLMs do. They are dream machines."** 트윗. https://x.com/karpathy/status/1733299213503787018
- Karpathy, A. (2023-01-24). **"The hottest new programming language is English."** https://x.com/karpathy/status/1617979122625712128
- Karpathy, A. (2025-02). **Vibe coding 트윗** (origin). 다수 분석: https://www.coderabbit.ai/blog/a-semantic-history-how-the-term-vibe-coding-went-from-a-tweet-to-prod
- MindStudio. **Vibe Coding vs Agentic Engineering — Karpathy's Framework**. https://www.mindstudio.ai/blog/vibe-coding-vs-agentic-engineering-karpathy-framework
- Clark, J. (Anthropic). **Import AI** — capability overhang 다회 언급. https://jack-clark.net/
- Dwarkesh Patel. **How Does Claude 4 Think? — Sholto Douglas & Trenton Bricken** (2025-05). https://www.dwarkesh.com/p/sholto-trenton-2
- Amodei, D. (Anthropic). **Machines of Loving Grace** (2024-10). https://darioamodei.com/essay/machines-of-loving-grace
- Anthropic. **Reduce hallucinations** — Claude API docs. https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- Google DeepMind. **FACTS Grounding benchmark** (2024-12). https://deepmind.google/blog/facts-grounding-a-new-benchmark-for-evaluating-the-factuality-of-large-language-models/
- OpenAI. **Harness engineering: leveraging Codex in an agent-first world**. https://openai.com/index/harness-engineering/
- Tweag. **Agentic Coding Handbook — TDD**. https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/
- Martin Fowler. **Harness engineering for coding agent users**. https://martinfowler.com/articles/harness-engineering.html
- LessWrong. **Are We In A Coding Overhang?** https://www.lesswrong.com/posts/vtgRghz3wvPGjkoCN/are-we-in-a-coding-overhang-1
- TechCrunch (2024). **Why RAG won't solve generative AI's hallucination problem**. https://techcrunch.com/2024/05/04/why-rag-wont-solve-generative-ais-hallucination-problem/

### 11.4 보안·실무 사례

- Mend. **The Hallucinated Package Attack: Slopsquatting Explained**. https://www.mend.io/blog/the-hallucinated-package-attack-slopsquatting/
- Aikido. **Slopsquatting: The AI Package Hallucination Attack Already Happening**. https://www.aikido.dev/blog/slopsquatting-ai-package-hallucination-attacks
- Trend Micro. **Slopsquatting: When AI Agents Hallucinate Malicious Packages**. https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/slopsquatting-when-ai-agents-hallucinate-malicious-packages
- Help Net Security (2025-04). **Package hallucination: LLMs may deliver malicious code to careless devs**. https://www.helpnetsecurity.com/2025/04/14/package-hallucination-slopsquatting-malicious-code/
- VibeDoctor. **AI Hallucinated Imports: When npm Packages Don't Actually Exist**. https://vibedoctor.io/blog/hallucinated-imports-ai-packages-dont-exist
- The Register (2025-04). **Cursor AI's own support bot hallucinated its usage policy**. https://www.theregister.com/2025/04/18/cursor_ai_support_bot_lies/
- The Register (2025-01). **"First AI software engineer" is bad at its job** (Devin Answer.AI 테스트). https://www.theregister.com/2025/01/23/ai_developer_devin_poor_reviews/
- GitHub Issue. **Claude Code hallucinated user input mid-response**. https://github.com/anthropics/claude-code/issues/10628
- NVIDIA. **Practical Security Guidance for Sandboxing Agentic Workflows**. https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/
- Northflank. **How to sandbox AI agents in 2026**. https://northflank.com/blog/how-to-sandbox-ai-agents
- Cursor Forum. **AI Package Hallucination 토론**. https://forum.cursor.com/t/is-anyone-else-worried-about-ai-package-hallucination-in-their-builds/154658

### 11.5 한국 자료

- GeekNews (news.hada.io). **"Agentic Coding은 함정이다"**. https://news.hada.io/topic?id=29155
- GeekNews. **"Andrej Karpathy가 말하는 코드 에이전트, AutoResearch, 그리고 AI"**. https://news.hada.io/topic?id=27706
- GeekNews. **"2025년 LLM 총정리: 추론·에이전트·코딩 에이전트의 해"**. https://news.hada.io/topic?id=25486
- velog @xav. **"바이브코딩의 실패 경험과 한계"**. https://velog.io/@xav/vibe-coding-and-software-engineering
- velog @do0ori. **"바이브 코딩(Vibe Coding)"**. https://velog.io/@do0ori/바이브-코딩Vibe-Coding
- brunch @hsy110405. **"바이브 코딩 6개월 후기 - 희망 편"**. https://brunch.co.kr/@hsy110405/33
- brunch @b8f8683a622d44b. **"바이브코딩의 현실과 단점, 직접 경험한 후기"**. https://brunch.co.kr/@b8f8683a622d44b/96
- KT Enterprise. **"LLM의 환각현상, 어떻게 보완할 수 있을까?"**. https://enterprise.kt.com/bt/dxstory/2521.do
- 한컴테크. **"최신 논문 분석을 통한 LLM의 환각 현상 완화 전략 탐구"**. https://tech.hancom.com/llm-hallucination-reduction-research/
- Korea Science. **"KT 믿음 LLM의 한국어 환각(Hallucination) 억제 효과"**. https://koreascience.kr/article/CFKO202532436090641.page
- 나무위키 / 위키독스. **"인공지능 환각"** 한국어 사전. https://namu.wiki/w/인공지능%20환각

---

## 12. 리서치 한계

이 레퍼런스가 충분히 커버하지 못한 영역, 또는 깊이가 얕은 영역:

1. **멀티모달 환각 (vision/audio LLM)**: 이번 리서치는 코드·텍스트 중심. VLM·SDXL류 이미지 환각, ASR 환각은 거의 다루지 않았다. 다행히 책 주제가 코딩 중심이라 큰 결손은 아니다.

2. **법조계 환각 케이스**: ChatGPT가 만든 가짜 판례 인용으로 변호사가 제재받은 일련의 사건. 잘 알려진 도입부 소재지만 이번 리서치는 깊이 안 다뤘다. 책 도입부에 쓸 거면 별도 case study 필요.

3. **기업별 환각률 측정 표준**: 모델별 hallucination rate(Vectara HHEM, Galileo, suprmind 등)는 인용은 했지만 측정 방법론·신뢰도 비교는 별도 deep dive 필요.

4. **한국어 LLM 환각의 정량 데이터**: KT 믿음 / 카카오 Kanana / 네이버 HyperCLOVA에 대한 환각률 비교는 표면적으로만 다뤘다. 한국 독자 대상이면 더 보강 가능.

5. **Claude 내부 mechanistic interpretability**: Anthropic의 Anthropic interpretability팀(Sholto Douglas-Trenton Bricken 대화)에서 환각의 "회로" 단위 설명은 일부만 언급. 더 들어가려면 Anthropic blog post 별도 리서치 필요.

6. **Andrew Karpathy의 Intro to LLMs 강의** (1h video, 2023)에서의 환각 설명은 검색은 했지만 영상 transcript는 본문에 못 옮겼다. 직접 들으면 추가 인용 확보 가능.

7. **Reddit 정성적 인용**: r/LocalLLaMA, r/ClaudeAI 등의 구체적 thread 인용은 검색이 제한적이었다(검색이 결과 0으로 나오는 경우 있음). 책 집필 시 individual reddit thread 직접 fetch가 효과적.

8. **Devin / Cursor / Cline / Aider 별 environment 별 환각률 비교**: 정량 비교는 매체별 비공식 후기 위주.

이상은 책 집필 단계에서 필요 시 보강 가능한 영역들이다.
