<!-- 검색 시점: 2026-06-10 기준 -->
# 논문 리서치: AI Agentic Coding의 4대 엔지니어링 — 학술적 뿌리

> 4대 엔지니어링은 산업·커뮤니티에서 태어난 실무 용어다. 학술 논문은 그 "엔지니어링"이 다루는 기저 현상(in-context learning, CoT, ReAct, tool use, agent-computer interface, 평가 벤치마크)을 정초한다. 비학문 개발자 독자를 위해 결과·직관 위주로 정리.

---

## 논문 1: Language Models are Few-Shot Learners (GPT-3)
- 저자·연도: Brown et al., 2020
- 발표처: NeurIPS 2020
- DOI/arXiv: arXiv:2005.14165
- 요약: 1,750억 파라미터 GPT-3가 별도 파인튜닝 없이 few-shot "in-context learning"으로 다양한 과제를 수행함을 보임. 입력(프롬프트)에 예시를 넣는 것만으로 동작이 바뀐다는 발견이 "프롬프트를 어떻게 쓰는가"를 일급 변수로 만들었다. → prompt engineering의 학술적 출발점.
- 핵심 수치·결과: 175B 파라미터. 프롬프트 내 예시(few-shot)만으로 과제 적응.
- 인용할 만한 문장: in-context learning — 모델 가중치를 바꾸지 않고 프롬프트 안의 예시로 과제를 학습.
- 독자 전달 제안: "프롬프트 엔지니어링이 왜 갑자기 중요해졌나"의 기원 — GPT-3가 '프롬프트에 따라 행동이 극적으로 달라지는' 모델이었기 때문.

## 논문 2: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- 저자·연도: Wei et al., 2022
- 발표처: NeurIPS 2022
- DOI/arXiv: arXiv:2201.11903
- 요약: "질문 → 중간 추론 단계 → 답" 형식의 few-shot 예시를 주면(=CoT 프롬프팅) 큰 모델의 수학·상식·기호 추론 성능이 크게 향상됨. 입력이 아니라 출력을 reasoning chain으로 증강한다는 직교적 방향. 추론은 모델 규모의 창발적(emergent) 성질.
- 핵심 수치·결과: 충분히 큰 모델에서만 효과가 나타나는 emergent property. 추론 벤치마크에서 큰 폭 향상.
- 인용할 만한 문장: chain-of-thought는 "few-shot 데모로 복잡 추론 능력을 끌어내는 in-context learning 기법."
- 독자 전달 제안: 프롬프트 엔지니어링의 대표 테크닉(=생각을 단계로 풀게 시키기)이 어떻게 '학술적 기법'이 됐는지의 사례. "Let's think step by step."

## 논문 3: ReAct: Synergizing Reasoning and Acting in Language Models
- 저자·연도: Yao et al., 2022 (Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao)
- 발표처: ICLR 2023 (arXiv 2022-10-06)
- DOI/arXiv: arXiv:2210.03629
- 요약: LLM이 추론 트레이스(reasoning)와 작업별 액션(acting)을 번갈아 생성하게 함. 추론은 계획을 세우고 예외를 처리하고, 액션은 외부 소스(위키 API·환경)와 상호작용해 정보를 모은다. CoT의 환각·오류 전파를 외부 상호작용으로 보완. → agentic loop("생각하고-행동하고-관찰하고 반복")의 직접적 학술 원형.
- 핵심 수치·결과: ALFWorld·WebShop에서 모방학습·강화학습 대비 절대 성공률 +34%, +10%. 단 1~2개 in-context 예시만으로.
- 인용할 만한 문장: 추론 트레이스는 "행동 계획을 유도·추적·갱신하고 예외를 처리," 액션은 "외부 소스와 인터페이스해 추가 정보 수집."
- 독자 전달 제안: "loop engineering"의 act-observe-reason-repeat 패턴이 어디서 왔는지 — ReAct가 그 핵심 루프를 이름 붙인 논문.

## 논문 4: Toolformer: Language Models Can Teach Themselves to Use Tools
- 저자·연도: Schick et al., 2023 (Timo Schick 외, Meta AI)
- 발표처: NeurIPS 2023 (arXiv 2023-02-09)
- DOI/arXiv: arXiv:2302.04761
- 요약: 모델이 어떤 API를, 언제, 어떤 인자로 호출하고 결과를 어떻게 다음 토큰 예측에 통합할지 스스로 학습. 계산기·QA·검색·번역·캘린더 도구를 통합. 도구 사용을 모델 학습에 내재화 → 하네스의 "툴 실행" 층과 에이전트 정의("툴을 루프로 사용")의 학술 기반.
- 핵심 수치·결과: 다양한 다운스트림 과제에서 zero-shot 성능 대폭 향상, 핵심 언어모델링 능력 손상 없이 훨씬 큰 모델과 경쟁.
- 인용할 만한 문장: "trained to decide which APIs to call, when to call them, what arguments to pass, and how to best incorporate the results."
- 독자 전달 제안: "에이전트 = LLM이 툴을 루프로 사용"이라는 정의의 기술적 뿌리. 하네스가 왜 '툴 실행'을 핵심 컴포넌트로 두는지.

## 논문 5: SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
- 저자·연도: Yang, Jimenez, Wettig, Lieret, Yao, Narasimhan, Press, 2024 (Princeton)
- 발표처: NeurIPS 2024
- DOI/arXiv: arXiv:2405.15793
- 요약: 코딩 에이전트가 파일 생성·편집, 리포 탐색, 테스트 실행을 잘하게 하는 핵심은 모델용으로 특별히 설계된 인터페이스, 즉 Agent-Computer Interface(ACI). LM 에이전트는 고유한 필요·능력을 가진 새 부류의 "최종 사용자." → harness engineering의 가장 모방된 학술 아이디어.
- 핵심 수치·결과: SWE-bench pass@1 12.5%, HumanEvalFix 87.7% — 비대화형 LM의 종전 SOTA를 크게 상회 (2024 기준 수치).
- 인용할 만한 문장: ACI 설계가 "에이전트의 코드 생성·편집·탐색·테스트 능력을 크게 향상."
- 독자 전달 제안: 하네스 엔지니어링이 단순 래퍼가 아니라 "성능을 좌우하는 인터페이스 설계"임을 입증한 논문. ACI는 오늘날 코딩 에이전트에서 가장 많이 모방된 아이디어.

## 논문 6: SWE-bench (벤치마크) — Can Language Models Resolve Real-World GitHub Issues?
- 저자·연도: Jimenez et al., 2023/2024 (Princeton)
- 발표처: ICLR 2024
- DOI/arXiv: arXiv:2310.06770
- 요약: 실제 GitHub 이슈+PR로 구성된 코딩 에이전트 평가 벤치마크. "에이전트가 실제 소프트웨어 작업을 해내는가"를 정량화. 하네스·루프·컨텍스트 전략의 성능 비교 기준이 됨(예: SWE-bench Verified, SWE-bench Pro 변형).
- 핵심 수치·결과: 출시 초기 모델 해결률 한 자릿수 → 이후 프런티어 모델·하네스 발전으로 급상승(섹션 6의 모델 비교 수치는 변동성 높음, fact-check 대상).
- 인용할 만한 문장: 에이전트 평가의 사실상 표준 벤치마크.
- 독자 전달 제안: "이 모델이 코딩 에이전트로 좋은가"를 말할 때 인용되는 숫자의 출처. 단, 점수는 빠르게 바뀌므로 "{연도} 기준" 명기 필수.

## 이론적 프레임워크 요약 (독자용 직관)
- **프롬프트 엔지니어링의 뿌리**: in-context learning(Brown 2020) → 프롬프트가 행동을 바꾼다. CoT(Wei 2022) → 출력을 추론 사슬로 증강.
- **루프/에이전트의 뿌리**: ReAct(Yao 2022) → reason+act 교차 루프. Toolformer(Schick 2023) → 도구 사용 내재화.
- **하네스의 뿌리**: SWE-agent/ACI(Yang 2024) → 인터페이스 설계가 성능을 좌우.
- **평가의 뿌리**: SWE-bench(Jimenez 2024) → 에이전트 성능의 공통 잣대.
- 주의: "context engineering"·"harness engineering"·"loop engineering"은 학술 용어가 아니라 2025~2026 산업 용어다. 논문은 이 용어들이 가리키는 현상을 다룰 뿐, 용어 자체를 쓰지 않는다 — 책에서 이 구분을 명확히 할 것.

## 수집 한계
- "context engineering" / "harness engineering" / "loop engineering"을 제목에 단 peer-reviewed 논문은 2026-06 기준 사실상 없음(산업 용어). 학술 뿌리만 매핑함.
- SWE-bench 류 벤치마크 점수는 모델·하네스 조합·날짜에 따라 급변 — 본문에서 구체 수치 인용 시 반드시 "{연도/리더보드 시점} 기준" 못 박고 fact-checker 대조.
- 일부 논문은 abstract·2차 요약 기반 기록(전문 PDF 직접 파싱은 제한). DOI/arXiv ID는 정확.
