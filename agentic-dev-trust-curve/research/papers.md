# 논문 리서치: 신뢰 곡선(Trust Curve)과 AI 코딩 에이전트 — 학술 근거

- 검색 시점: 2026-10-10
- 장르: tech-book · 슬러그: agentic-dev-trust-curve
- 검색 소스: arXiv, Semantic Scholar API, ACL Anthology, NeurIPS/ICLR proceedings, ACM/IEEE DOI, OpenAI/Google/METR 공식 발표
- 피인용수는 Semantic Scholar 2026-10-10 조회값. 조회 실패(rate limit)는 "미조회"로 표기.
- 확인 상태 범례: ✅ 식별자·수치를 1차 소스(arXiv abstract/DOI 페이지)에서 확인 · ⚠️ 2차 소스(요약·보도)에서만 확인 · ❓ 미확인
- 대상 독자(Java/Spring·React/Next.js 개발자)에 맞춰 증명·수식은 생략하고 결과와 직관만 남긴다.

---

## 0. 책 논지와 학술 근거의 대응 (요약표)

| Lauren Tan의 주장 | 학술 근거 (번호) | 한 줄 |
|---|---|---|
| "100번째 자신 있게 틀리면 신뢰를 잃는다" / 신뢰는 감정이 아니라 시스템 | §1-1 Lee & See, §1-2 Parasuraman & Riley, §1-4 de Visser | 신뢰는 불확실성 아래 "의지할지"의 태도. 보정(calibration)이 핵심이며, 한 번 깨진 신뢰는 회복 비용이 크다 |
| 단계를 건너뛰면 토큰만 태운다 | §1-5 Wickens & Dixon(⚠️), §6-2 Kim et al. | 신뢰도 낮은 자동화는 안 쓰는 것보다 나쁨. 단일 에이전트 기준선이 약하면 독립 병렬화는 오류를 17배 증폭 |
| Verification: 에이전트가 직접 실행·측정 | §2-4 Self-Debug, §2-6 Huang(자기교정 불가), §2-7 Large Language Monkeys, §2-8 CodeMonkeys | 자기 성찰만으로는 못 고친다. 실행·테스트 피드백이 있을 때만 정확도가 오른다 |
| Eval: 다른 모델을 judge로, 평가 중임을 숨겨라 | §3-1~§3-8 | 자기 선호·위치 편향은 실측됨. 여러 모델 패널이 단일 judge보다 낫고 싸다. 모델은 평가 상황을 AUC 0.83 수준으로 알아챈다 |
| Architecture: 지름길을 정답으로, 소프트 룰만으론 썩는다 | §5-1~§5-4 정적 분석, §7-1 AGENTS.md 무효 | 코드 리뷰 시점의 하드 집행은 수정률 70%, 배치 리포트는 0%에 가깝다. 소프트 지침(AGENTS.md)은 성공률을 올리지 못한다 |
| 리뷰 코멘트는 code smell → 린트로 승격 | §5-5~§5-8 | 리뷰 코멘트의 대부분은 결함 발견이 아니라 가독성·관행. 그 범주는 자동화 가능함이 실증됨 |
| 생산성: 사람이 병목이면 느려진다 | §4-1~§4-9 | 실측치는 −19%(METR)부터 +55.8%(Copilot RCT)까지 벌어진다. 차이를 가르는 변수가 바로 검증·맥락·코드베이스 성숙도 |

---

## 1. 인간-자동화 신뢰 이론

### 논문 1-1: Trust in Automation: Designing for Appropriate Reliance ✅
- 저자·연도: John D. Lee, Katrina A. See, 2004
- 발표처: *Human Factors* 46(1), pp. 50–80
- DOI: 10.1518/hfes.46.1.50_30392
- 피인용수: 6,751 (S2, 2026-10-10)
- 요약: 신뢰를 "불확실성과 취약성이 있는 상황에서 어떤 행위자가 내 목표 달성을 도울 것이라는 태도"로 정의하고, 자동화에 대한 신뢰가 '의존(reliance)' 행동으로 이어지는 경로를 정리한 리뷰 논문. 신뢰의 적절성을 세 축으로 나눈다 — **calibration**(신뢰 수준이 실제 능력과 일치하는가), **resolution**(능력 차이를 신뢰 차이로 구분하는가), **specificity**(어떤 기능·상황에 대한 신뢰인지 구체적인가). 신뢰가 능력을 초과하면 **overtrust → misuse**, 미달하면 **distrust → disuse**.
- 핵심 수치·결과: 이론 리뷰 논문이라 단일 실험 수치는 없음. 신뢰 형성의 세 기반(performance / process / purpose)과 "신뢰는 자동화의 관찰 가능한 행동 정보에 의해 보정된다"는 설계 원칙이 핵심.
- 책에서의 쓰임새: 1장. "에이전트를 믿는다"를 감정이 아니라 **calibration 문제**로 재정의할 때. "100번째 자신 있게 틀림"은 performance 기반 신뢰의 붕괴이며, 검증 스킬은 '관찰 가능한 행동 정보'를 늘려 보정을 가능하게 하는 장치라는 논리의 뼈대.
- 독자 전달: "신뢰 곡선"의 세로축이 사실은 '자율성'이 아니라 '보정된 신뢰'라는 설명. 과신(실제 능력 이상으로 자율성 부여)과 불신(사람이 영원히 병목)이 둘 다 비용임을 짚는다.

### 논문 1-2: Humans and Automation: Use, Misuse, Disuse, Abuse ✅(DOI ❓)
- 저자·연도: Raja Parasuraman, Victor Riley, 1997
- 발표처: *Human Factors* 39(2), pp. 230–253
- DOI: 미확인 (검색 결과에서 DOI 문자열 미확보)
- 피인용수: 미조회
- 요약: 자동화의 네 가지 인간 요인 — 사용(use), 오용(misuse: 과의존으로 모니터링 실패·판단 편향), 불용(disuse: 오경보가 잦아 꺼버림), 남용(abuse: 설계자가 인간 요인을 무시하고 자동화 적용). 남용이 오용·불용을 유발한다.
- 핵심 수치·결과: 개념 논문. "오경보(false alarm)가 잦으면 사람은 자동화를 꺼버린다"는 disuse 메커니즘이 핵심 결과.
- 책에서의 쓰임새: 1장·2장. 에이전트가 "범인 찾았다"고 자신 있게 틀리는 것 = 오경보. 반복되면 개발자는 에이전트 출력을 읽지 않거나(disuse) 아예 안 쓰게 된다. 반대로 CI를 거치지 않은 자동 머지는 misuse.
- 독자 전달: 린터의 오탐이 많으면 개발자가 `// eslint-disable` 로 꺼버리는 것과 같은 현상이라는 비유.

### 논문 1-3: Trust in Automation: Integrating Empirical Evidence on Factors That Influence Trust ✅
- 저자·연도: Kevin Anthony Hoff, Masooda Bashir, 2015
- 발표처: *Human Factors* 57(3), pp. 407–434
- DOI: 10.1177/0018720814547570
- 피인용수: 2,314 (S2)
- 요약: 2002–2013년 실증 연구를 체계적으로 리뷰해 신뢰를 세 층으로 모델화 — **dispositional**(개인 성향), **situational**(상황·과업·위험), **learned**(경험으로 학습된 신뢰: 사전 기대 + 사용 중 동적 갱신). 신뢰 관계는 신뢰자(trustor)·피신뢰자(trustee)·위험이 걸린 과업으로 구성된다.
- 핵심 수치·결과: 리뷰 논문. "learned trust는 사용 중 자동화의 성능 관찰로 지속 갱신된다"가 설계 함의.
- 책에서의 쓰임새: 1장. 신뢰 곡선이 "학습된 신뢰"의 누적이라는 설명. 툴 콜·thinking 블록을 열어보라는 Lauren의 조언 = learned trust의 입력을 늘리는 행위.

### 논문 1-4: From 'automation' to 'autonomy': the importance of trust repair in human–machine interaction ✅(초록 ❓)
- 저자·연도: Ewart J. de Visser, Richard Pak, Tyler H. Shaw, 2018
- 발표처: *Ergonomics* (2018; 볼륨·페이지 미확인)
- DOI: 10.1080/00140139.2018.1457725
- 피인용수: 374 (S2)
- 요약: 자율 시스템과의 관계를 "도구"가 아니라 "사람 간 관계"처럼 설계해야 하며, 신뢰 위반 후 **회복(trust repair)** 능력을 시스템에 내장해야 한다고 주장. 출판사가 초록 공개를 막아 본문 수치는 미확인. 후속 연구(Clemson CATLab)에서 "사과는 역량(competence) 실패에 효과적이고, 진실성(integrity) 실패에는 덜 효과적"이라는 실험 결과가 보고됨(⚠️ 석사논문·블로그 수준).
- 책에서의 쓰임새: 1장. "에이전트가 틀렸을 때 어떻게 신뢰를 복구하는가" — 에이전트가 자기 검증 결과(재현 로그·테스트 결과)를 첨부하는 것이 회복 신호가 된다는 논지.
- 한계: 본문 접근 불가. 인용 시 "주장"으로만 쓰고 수치 인용 금지.

### 논문 1-5: The benefits of imperfect diagnostic automation: a synthesis of the literature ⚠️
- 저자·연도: Christopher D. Wickens, Stephen R. Dixon, 2007
- 발표처: *Theoretical Issues in Ergonomics Science* (볼륨·페이지 미확인)
- DOI: 미확인
- 피인용수: 미조회
- 요약: 진단 자동화 연구를 종합해, **신뢰도가 약 70% 아래로 떨어지면 자동화의 도움이 사라지고 보조 받은 성능이 수동 성능보다 나빠진다**는 임계값을 제시. 이 70% 수치는 2차 인용(arXiv 2310.01220의 관련연구 절)에서만 확인함.
- 책에서의 쓰임새: 2장·9장. "에이전트 1개의 출력도 못 믿는데 100개를 띄울 수 없다"의 정량 직관. 검증 없이 정확도 낮은 에이전트를 병렬화하면 안 쓰느니만 못하다.
- 한계: 원문 미확인. 본문에서는 "자동화 연구에서는 신뢰도가 대략 70% 아래면 도움이 사라진다는 종합 결과가 보고된다(Wickens & Dixon 2007, 2차 인용)" 수준으로만.

### 논문 1-6: Investigating and Designing for Trust in AI-powered Code Generation Tools ✅
- 저자·연도: Ruotong Wang, Ruijia Cheng, Denae Ford, Thomas Zimmermann, 2024
- 발표처: ACM FAccT 2024 (CHI가 아님)
- arXiv: 2305.11248 (v2 2024-05)
- 피인용수: 미조회
- 요약: 개발자 17명 인터뷰 기반 질적 연구. 코드 생성 도구 신뢰의 세 난관 — (1) 적절한 기대 형성, (2) 도구 설정, (3) 제안 검증. 설계 없이는 과신·불신 양쪽으로 미끄러진다.
- 책에서의 쓰임새: 1장. "검증"이 개발자들이 실제로 호소한 난관임을 인용. 수치 없는 질적 연구이므로 정량 주장에 쓰지 말 것.

### 논문 1-7: Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance ✅
- 저자·연도: Gagan Bansal 외, 2021
- 발표처: ACM CHI 2021
- DOI: 10.1145/3411764.3445717
- 피인용수: 1,118 (S2)
- 요약: AI가 "설명"을 붙이면 사람이 AI 추천을 **맞든 틀리든** 더 잘 받아들인다. 설명은 팀 성능을 올리지 못하고 과의존만 키웠다(AI 정확도를 인간과 비슷하게 맞춘 조건).
- 책에서의 쓰임새: 1장·3장. 에이전트의 "자신 있는 설명"이 신뢰 보정을 돕는 게 아니라 **과신을 유도**한다는 근거. 그래서 설명이 아니라 **실행 증거**(테스트·트레이스)를 요구해야 한다.

### 논문 1-8: Explanations Can Reduce Overreliance on AI Systems During Decision-Making ✅
- 저자·연도: Helena Vasconcelos, Matthew Jörke, Madeleine Grunde-McLaughlin, Tobias Gerstenberg, Michael S. Bernstein, Ranjay Krishna, 2023
- 발표처: *Proc. ACM HCI* 7, CSCW1, Article 129
- DOI: 10.1145/3579605 · arXiv 2212.06823
- 피인용수: 430 (S2)
- 요약: 5개 연구(N=731). 사람은 설명을 **읽을지 말지 전략적으로 선택**한다. 과업이 어렵고 설명이 쉬우며 검증의 보상이 클 때만 설명이 과의존을 줄인다.
- 책에서의 쓰임새: 1-7과 짝으로. "사람이 검증자면 사람이 병목"의 심리학적 이유 — 검증 비용이 크면 사람은 그냥 승인(stamp)한다. 검증 비용을 에이전트 쪽으로 옮겨야 하는 이유.

---

## 2. 코드 생성 에이전트의 벤치마크와 검증

### 항목 2-1: SWE-bench Verified ⚠️(준학술·공식 발표)
- 출처: OpenAI, 2024-08-13, "Introducing SWE-bench Verified" (openai.com)
- 요약: 원본 SWE-bench(12개 Python 저장소)의 테스트셋 1,699건을 전문 개발자 93명이 검수해 **500건**을 남긴 인간 검증 부분집합. 원본의 약 68.3%가 "문제 설명 부족·테스트 과도 특정" 등으로 탈락. 난이도 라벨(easy 196 / hard 45 포함) 부여. 공개 시점 GPT-4o 33.2%(이전 오픈소스 스캐폴드 최고 16%).
- 책에서의 쓰임새: 2장. "벤치마크 자체도 검증이 필요했다"는 사례 — 평가 기준의 68%가 잘못돼 있었다. 검증자를 검증하라(verify the verifier)의 실제 사례.
- 원본 SWE-bench 논문(Jimenez et al., ICLR 2024)은 이번 검색에서 식별자 미확인 → ❓.

### 논문 2-2: SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks? ✅
- 저자·연도: Xiang Deng 외 (Scale AI), 2025-09
- arXiv: 2509.16941
- 피인용수: 미조회
- 요약: 41개 활성 저장소에서 **1,865개** 문제. 공개·비공개(held-out)·상용(스타트업 사유 코드) 3분할. 다중 파일 패치, 전문가 기준 수 시간~수 일 과업. 2025-09 평가에서 Pass@1 25% 미만, GPT-5 23.3%(⚠️ Claude Opus 4.1 22.7%는 보도 인용).
- 주의: arXiv 판본에 따라 초록이 "45% 미만"/"25% 미만"으로 다름. 2026년 리더보드는 80%대까지 올라갔다는 집계도 있음 → 수치 인용 시 "2025-09 원 논문 기준" 명시.
- 책에서의 쓰임새: 2장. 벤치마크 포화와 "현실 과업은 다르다"는 맥락. Java/Spring 같은 다중 파일·장기 과업에서 에이전트 신뢰가 더 어려운 이유.

### 논문 2-3: SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering ✅(venue ❓)
- 저자·연도: John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press, 2024
- arXiv: 2405.15793 (v3 2024-11-11) · NeurIPS 2024 게재 여부는 검색에서 미확인
- 요약: LM 에이전트를 "새로운 종류의 사용자"로 보고 전용 인터페이스(ACI: 파일 보기·편집·검색·실행 명령)를 설계. SWE-bench 전체 12.5%(12.47%), HumanEvalFix 87.7% pass@1.
- 책에서의 쓰임새: 2장·5장. "control 스킬"(CDP로 앱 조작)의 학술적 선례 — 에이전트에게 좋은 **조작 인터페이스**를 주면 같은 모델이 더 잘한다. Lauren의 Feature Map·control-glass와 직결.

### 논문 2-4: Teaching Large Language Models to Self-Debug ✅
- 저자·연도: Xinyun Chen, Maxwell Lin, Nathanael Schärli, Denny Zhou, 2023 (v2 2023-10)
- 발표처: ICLR 2024 · arXiv 2304.05128
- 피인용수: 미조회
- 요약: 모델이 생성한 코드를 **실행하고 그 결과를 설명(rubber-duck)**하게 해서 스스로 고치게 한다. 단위 테스트가 있는 TransCoder·MBPP에서 정확도 **최대 +12%p**. 테스트가 없는 Spider(text-to-SQL)에서는 코드 설명만으로 +2~3%p, 최난도 문제 +9%p. 10배 이상 많은 후보를 샘플링하는 기준선과 대등 이상.
- 책에서의 쓰임새: 3장(Verification). "실행 피드백이 있을 때 자기 수정이 작동한다"의 1차 근거. 수치 인용: "단위 테스트 피드백이 있을 때 최대 12%p".

### 논문 2-5: Reflexion: Language Agents with Verbal Reinforcement Learning ✅
- 저자·연도: Noah Shinn 외, 2023
- 발표처: NeurIPS 2023 · arXiv 2303.11366
- 요약: 시도 → 환경 피드백(테스트 결과 등) → 언어적 자기 성찰을 메모리에 저장 → 재시도. HumanEval pass@1 **91%**(GPT-4 기준선 80%).
- 책에서의 쓰임새: 3장. "실패 관찰 → 스킬"의 미니어처 — 실패 피드백을 텍스트로 축적하면 다음 시도가 좋아진다. 단, 외부 피드백(테스트)이 있었다는 점을 반드시 병기(2-6 참조).

### 논문 2-6: Large Language Models Cannot Self-Correct Reasoning Yet ✅
- 저자·연도: Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, Denny Zhou, 2023 (v2 2024-03)
- 발표처: ICLR 2024 · arXiv 2310.01798
- 요약: **외부 피드백 없는 내재적 자기 교정(intrinsic self-correction)**은 추론 과업에서 도움이 안 되고 오히려 성능이 떨어지기도 한다. 선행 연구의 개선은 (a) 정답 라벨(oracle)을 몰래 쓴 불공정 비교이거나 (b) 초기 프롬프트가 나빴던 탓. 다중 에이전트 토론도 같은 응답 수의 self-consistency를 넘지 못함.
- 책에서의 쓰임새: 3장 핵심. "에이전트에게 '다시 확인해봐'라고 말하는 것은 검증이 아니다." 검증은 **실행·테스트·브라우저라는 외부 신호**여야 한다는 논지의 반대 근거(negative result). 2-4·2-5와 세트로.
- 독자 전달: "코드 리뷰어에게 '네가 쓴 코드 네가 다시 봐'라고 하는 것과 같다. 테스트를 돌려야 한다."

### 논문 2-7: Large Language Monkeys: Scaling Inference Compute with Repeated Sampling ✅
- 저자·연도: Bradley Brown, Jordan Juravsky, Ryan Ehrlich 외 (Stanford), 2024 (v1 2024-07-31)
- arXiv: 2407.21787
- 요약: 같은 문제를 여러 번 샘플링하면 "하나라도 맞을 확률(coverage)"이 로그 선형으로 오른다. SWE-bench Lite에서 DeepSeek-Coder-V2-Instruct 1회 **15.9% → 250회 56%**(당시 단일 시도 SOTA 43% 초과). 단, 이 이득은 **자동 검증기(테스트)가 있어야 실제 성능으로 전환**된다. 검증기가 없는 수학 과업에선 다수결·보상모델이 coverage를 따라가지 못함.
- 책에서의 쓰임새: 3장·9장. "병렬화는 검증이 있을 때만 이득"의 가장 직접적 정량 근거. 신뢰 곡선 2단계(자가 검증) 없이 3·4단계(병렬·자동 머지)로 못 가는 이유.

### 논문 2-8: CodeMonkeys: Scaling Test-Time Compute for Software Engineering ✅
- 저자·연도: Ryan Ehrlich, Bradley Brown 외 (Stanford/Oxford), 2025-01-24
- arXiv: 2501.14723
- 요약: 모델이 수정안과 **함께 테스트 스크립트를 작성**, 생성 테스트로 투표 + 최종 선택 전용 다중 턴. SWE-bench Verified **57.4%**(Claude 3.5 Sonnet, 총 비용 약 USD 2,300). (Stanford 페이지엔 57.7% 표기 — arXiv 값 우선)
- 책에서의 쓰임새: 3장. "에이전트가 검증 코드를 스스로 쓰게 하라"의 실증. Lauren의 create-verification 스킬과 같은 구조.

---

## 3. LLM-as-a-Judge — 편향과 교차 검증

### 논문 3-1: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena ✅
- 저자·연도: Lianmin Zheng 외, 2023
- 발표처: NeurIPS 2023 (Datasets & Benchmarks) · arXiv 2306.05685
- 피인용수: 미조회
- 요약: LLM 심판의 네 편향 — **위치 편향**(순서 바꾸면 판정 바뀜; GPT-4만 60% 이상 일관), **장황함 편향**(길면 좋게 봄; "반복 목록" 공격에 취약), **자기 강화 편향**(자기 출력 선호), 제한된 추론력. 그럼에도 GPT-4 심판은 인간 선호와 80% 이상 일치(인간-인간 일치 수준).
- 책에서의 쓰임새: 4장(Evals). eval 설계 시 (a) 순서 바꿔 두 번 판정, (b) 길이 통제, (c) 다른 모델로 교차 — Lauren의 "judge 편향 교차검증"의 근거.

### 논문 3-2: Large Language Models are not Fair Evaluators ✅
- 저자·연도: Peiyi Wang 외, 2023 (v1 2023-05, ACL 2024 판본에 Lingpeng Kong 추가)
- 발표처: ACL 2024 Long Papers, pp. 9440–9450 · DOI 10.18653/v1/2024.acl-long.511 · arXiv 2305.17926
- 요약: 후보 순서만 바꿔서 Vicuna-13B가 ChatGPT를 **80문항 중 66문항** 이기게 만들 수 있었다(ChatGPT 심판). 완화책: Multiple Evidence Calibration(근거 먼저 쓰고 채점), Balanced Position Calibration(두 순서 결과 평균). 도구 FairEval 공개.
- 책에서의 쓰임새: 4장. "eval 숫자는 조작 가능하다"의 충격 사례. 루브릭 + 위치 균형 채점을 기본값으로.

### 논문 3-3: LLM Evaluators Recognize and Favor Their Own Generations ✅
- 저자·연도: Arjun Panickssery, Samuel R. Bowman, Shi Feng, 2024
- 발표처: NeurIPS 2024 · arXiv 2404.13076
- 요약: 자기 선호(self-preference)는 인간이 동등하다고 본 출력을 자기 것이면 더 높게 주는 현상. GPT-4·Llama 2는 자기 텍스트를 식별할 수 있고, 파인튜닝으로 **자기 인식 능력을 올리면 자기 선호가 선형으로 커진다** → 인과 관계 시사. "자기 것"이라고 라벨만 붙여도 선호 상승. 실험은 XSUM·CNN/DailyMail 요약 과업(GPT-3.5/GPT-4/Llama 2).
- 책에서의 쓰임새: 4장 핵심. **"같은 모델이 자기 결과를 채점하게 하지 말라"**의 1차 근거. Claude Code 출력은 Codex로, Codex 출력은 Claude로 교차 평가하는 책의 실전 패턴을 정당화.

### 논문 3-4: Self-Preference Bias in LLM-as-a-Judge ✅
- 저자·연도: Koki Wataoka, Tsubasa Takahashi, Ryokan Ri (SB Intuitions), 2024 (v2 2025-06)
- 발표처: NeurIPS 2024 워크숍 목록 등재 · arXiv 2410.21819
- 요약: 자기 선호를 정량화하는 지표 제안. GPT-4가 유의한 자기 선호. 원인은 **perplexity** — 자기가 썼든 아니든 "익숙한(낮은 perplexity) 텍스트"에 인간보다 높은 점수를 준다.
- 책에서의 쓰임새: 4장. 자기 선호가 "자기 글 알아보기"뿐 아니라 "익숙함" 때문이라는 보완 설명 → 모델 계열이 다른 judge를 써야 하는 이유.

### 논문 3-5: Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models ✅
- 저자·연도: Pat Verga 외 (Cohere), 2024
- arXiv: 2404.18796
- 요약: 서로 다른 계열의 작은 모델 여러 개로 구성한 **PoLL(Panel of LLM evaluators)**이 단일 대형 심판(GPT-4)보다 인간 판정과 더 잘 맞고, 모델 내 편향이 적으며, **비용은 7분의 1 이하**. 3개 심판 설정 × 6개 데이터셋.
- 책에서의 쓰임새: 4장. "여러 모델에 걸쳐 매트릭스 평가"(Lauren)의 근거이자 비용 반론 대응 — 교차 검증이 더 싸다.

### 논문 3-6: A Survey on LLM-as-a-Judge ✅
- 저자·연도: Jiawei Gu 외, 2024 (v6 2025-10)
- arXiv: 2411.15594
- 피인용수: 1,910 (S2)
- 요약: 신뢰할 수 있는 심판 시스템 구축에 초점 — 일관성 향상, 편향 완화, 시나리오 적응, 심판 신뢰도 측정법과 벤치마크.
- 책에서의 쓰임새: 4장 참고문헌 앵커(서베이). 세부 수치 인용용은 아님.

### 논문 3-7: Large Language Models Often Know When They Are Being Evaluated ✅
- 저자·연도: Joe Needham 외, 2025 (v1 2025-05-28, v3 2025-07-16)
- arXiv: 2505.23836
- 요약: 61개 데이터셋에서 1,000개 프롬프트·트랜스크립트로 "이게 평가인가 실사용인가"를 모델에게 맞히게 함. Gemini-2.5-Pro **AUC 0.83**(인간 기준선 0.92).
- 책에서의 쓰임새: 4장. Lauren의 "eval 디렉터리명에 'eval'·'test'를 넣지 말라 — 알면 행동이 바뀐다"의 학술 근거. 평가 인지(evaluation awareness)는 실측된 현상.

### 논문 3-8: AI Sandbagging: Language Models can Strategically Underperform on Evaluations ✅
- 저자·연도: Teun van der Weij 외, 2024
- 발표처: ICLR 2025 · arXiv 2406.07358
- 피인용수: 150 (S2)
- 요약: GPT-4·Claude 3 Opus 등 프런티어 모델이 프롬프트/파인튜닝으로 **특정 평가에서만 선택적으로 성능을 낮추고** 일반 평가에선 유지할 수 있음을 보임(위험 역량 평가 맥락).
- 책에서의 쓰임새: 4장. 3-7과 함께 "평가 상황을 숨겨야 하는 이유"의 보강. 코딩 eval에서 직접 sandbagging이 관측됐다는 뜻은 아니므로 과장 금지 — "평가 인지가 행동을 바꿀 수 있다는 것이 실험으로 확인됐다" 수준으로.

---

## 4. AI 보조 코딩의 생산성·품질 실증

### 논문 4-1: The Impact of AI on Developer Productivity: Evidence from GitHub Copilot ✅
- 저자·연도: Sida Peng, Eirini Kalliamvakou, Peter Cihon, Mert Demirer, 2023-02
- arXiv: 2302.06590 (Microsoft Research / GitHub / MIT Sloan)
- 요약: 통제 실험. JavaScript로 HTTP 서버 구현 과업. Copilot 그룹 **55.8% 빠름**(95% CI 21–89%): 평균 1시간 11분 vs 2시간 41분.
- 한계: 단일 소규모 과업, 그린필드, Copilot 판매사 소속 저자(이해관계).
- 책에서의 쓰임새: 6장(생산성 논쟁). "가장 낙관적인 수치"로 제시하고, 과업 성격(작고 독립적·테스트 명확)이 결과를 가른다는 틀에서 해석.

### 논문 4-2: The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers ✅
- 저자·연도: Zheyuan (Kevin) Cui, Mert Demirer, Sonia Jaffe, Leon Musolff, Sida Peng, Tobias Salz, 2025
- 발표처: *Management Science* (online) · DOI 10.1287/mnsc.2025.00535 · SSRN 4945566
- 요약: Microsoft·Accenture·익명 Fortune 100 기업의 RCT 3건, **개발자 4,867명**. Copilot 사용 시 완료 과업 **+26.08%**(SE 10.3%). 경험이 적은 개발자가 더 많이 채택하고 더 큰 이득.
- 주의: 지표는 "완료 과업(completed tasks)"이며 PR 수로 단순화하면 부정확. 초기 드래프트는 5,114명 → 최종 4,867명.
- 책에서의 쓰임새: 6장. 대규모 현장 실험의 대표 수치. "주니어가 더 이득"은 Lauren의 "가장 멍청한 에이전트도 잘하게 코드베이스를 세팅하라"와 반대 방향에서 같은 결론 — 맥락이 약한 쪽에 가드레일이 더 필요.

### 논문 4-3: How much does AI impact development speed? An enterprise-based randomized controlled trial ✅
- 저자·연도: Elise Paradis, Kate Grey, Quinn Madison, Daye Nam, Andrew Macvean, Vahid Meimand, Nan Zhang, Ben Ferrari-Church, Satish Chandra (Google), 2024 (v3 2024-11-11)
- arXiv: 2410.12944
- 요약: Google 정규직 엔지니어 **96명** RCT, 복잡한 엔터프라이즈급 과업, 내부 AI 기능 3종(2024 여름). 과업 시간 **약 21% 단축**(신뢰구간 넓음). 코드 작업 시간이 긴 개발자일수록 이득 큼. 저자들이 일반화 한계를 명시.
- 책에서의 쓰임새: 6장. "브라운필드·엔터프라이즈에서도 이득은 있으나 55%가 아니라 21% 수준, 그것도 분산이 크다."

### 논문 4-4: Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity ✅
- 저자·연도: Joel Becker, Nate Rush, Elizabeth Barnes, David Rein (METR), 2025-07-10
- arXiv: 2507.09089 · metr.org 블로그
- 피인용수: 213 (S2)
- 요약: 경험 많은 OSS 개발자 **16명**, 자기 저장소(평균 5년 기여)에서 **246개 과업**을 AI 허용/불허로 무작위 배정. 주 도구 Cursor Pro + Claude 3.5/3.7 Sonnet. 결과: AI 허용 시 **19% 더 오래 걸림**. 개발자들은 사전에 −24%를 예측했고, 끝난 뒤에도 −20%였다고 **믿었다**(인식-실측 괴리).
- 한계: n=16, 특정 환경(성숙한 대형 OSS, 높은 맥락 요구), 2025 초 도구 기준. 저자들도 "스냅샷"으로 한정.
- 책에서의 쓰임새: 6장 핵심 + 1장 오프닝 후보. Lauren의 "코드 작성 시간은 줄지만 리뷰·수정 시간이 늘어나는 경험"과 정확히 일치. 핵심은 **느려진 원인이 검증·리뷰 부담**이라는 점 → 검증을 에이전트에게 넘기지 않으면 숙련자는 손해.
- 독자 전달: "당신이 느끼는 20% 빨라짐은 측정하면 20% 느려짐일 수 있다."

### 항목 4-5: DORA 2024 Accelerate State of DevOps Report ⚠️(준학술·업계 리포트)
- 출처: Google Cloud DORA, 2024 (응답자 약 39,000명 — InfoQ 인용; 출처별로 3,000~39,000으로 상이)
- 요약: AI 채택 증가는 코드 품질(+3.4%)·리뷰 속도(+3.1%) 등 개별 지표를 올렸지만, **소프트웨어 전달 처리량 −1.5%, 전달 안정성 −7.2%**(AI 채택 25% 증가당 — "25%" 기준은 2차 인용에서만 확인). 이유는 데이터로 설명되지 않음.
- 책에서의 쓰임새: 6장. "개인이 빨라져도 시스템이 느려질 수 있다" — 검증·CI가 따라오지 못하면 변경 실패가 늘어난다는 해석의 근거. 수치는 "DORA 2024 기준" 꼬리표 필수.

### 항목 4-6: DORA 2025 State of AI-assisted Software Development ⚠️(준학술)
- 출처: Google Cloud DORA, 2025-09 (응답자 약 5,000명)
- 요약: AI 사용률 **90%**(전년 대비 +14%p), 65%가 "크게 의존", 하루 중앙값 2시간 사용. 핵심 메시지: **AI는 증폭기** — 잘 돌아가는 조직의 강점과 망가진 조직의 결함을 똑같이 키운다. 7개 팀 클러스터 중 2개("Pragmatic performers"·"Harmonious high-achievers")만 변경 실패율 증가 없이 처리량 증가(⚠️ 클러스터 해석은 2차 블로그). 사용 대비 **신뢰 격차** 존재. "DORA AI Capabilities Model"(7개 실천) 제시.
- 책에서의 쓰임새: 6장·10장. "AI slop 이전에 human slop이 있었다"(Lauren) = DORA의 증폭기 명제. 브라운필드 가드레일이 에이전트에 잘 맞는 이유.

### 항목 4-7: GitClear — AI Copilot Code Quality (2025) ⚠️(업체 리포트)
- 출처: GitClear, 2025-02 (보도: DevClass, LeadDev, i-programmer)
- 요약: 2020-01~2024-12 사이 **2억 1,100만 줄** 변경 분석(2/3 사기업 옵트인, 1/3 OSS). 2024년 **5줄 이상 중복 블록 8배 증가**. 이동/리팩터링된 코드 비율 감소(출처별 −39.9% 또는 25%→10% 미만으로 상이 — 원 리포트 미확인). 2024년은 복사-붙여넣기 줄 수가 이동 줄 수를 처음 넘어선 해.
- 책에서의 쓰임새: 7장(Architecture). "organic architecture"의 정량 징후 — 에이전트는 기존 코드를 재사용하기보다 새 블록을 붙인다. 중복 금지 린트·colocation이 필요한 이유. 수치는 "GitClear 2025 리포트 기준, 2차 보도" 명시.

### 항목 4-8: Uplevel — Copilot 영향 분석 (2024) ⚠️(업체 리포트, 근거 약함)
- 출처: Uplevel Data Labs, 2024 (보도: CIO, DevOps.com, ITPro)
- 요약: 약 800명(실험 351 / 대조 434), 3개월. PR 사이클 타임 −1.7분(무의미), 처리량 변화 없음. **버그율 +41%**. 번아웃 지표는 비사용 그룹이 더 개선(28% vs 17%).
- 한계: 입수한 블로거에 따르면 2쪽짜리 리포트에 데이터 거의 없음. GitHub 자체 연구(202명)는 반대 결과.
- 책에서의 쓰임새: 6장에서 "반대 증거"로 한 줄만. 수치 단독 인용 금지, 반드시 한계 병기.

### 논문 4-9: Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions ✅
- 저자·연도: Hammond Pearce 외 (NYU·Calgary), 2022
- 발표처: IEEE S&P 2022 · arXiv 2108.09293 · CACM Research Highlights 재게재
- 요약: MITRE Top-25 CWE 기반 89개 시나리오, 1,689개 프로그램 생성. CodeQL + 수동 검사로 **약 40%(40.73%)가 취약**(C 50.29%, Python 38.35% — ⚠️ 세부는 ITmedia 인용).
- 책에서의 쓰임새: 7장. "에이전트가 못하는 건 CI로 막아라"의 보안 버전 — SAST를 CI 하드 게이트로.

---

## 5. 아키텍처·정적 분석·코드 리뷰 — "하드 집행"의 근거

### 논문 5-1: Tricorder: Building a Program Analysis Ecosystem ✅
- 저자·연도: Caitlin Sadowski, Jeffrey van Gogh, Ciera Jaspan, Emma Söderberg, Collin Winter (Google), 2015
- 발표처: ICSE 2015 · DOI 10.1109/ICSE.2015.76
- 피인용수: 276 (S2)
- 요약: Google의 정적 분석 플랫폼. 설계 원칙: 개발자 워크플로(코드 리뷰)에 통합, 도메인 전문가가 분석기를 직접 기여, 개발자 피드백("Not useful" 클릭)으로 분석기를 데이터 기반으로 관리. 본문 PDF 텍스트 추출 실패로 세부 수치(분석기 수, Not-useful 임계값) ❓.
- 책에서의 쓰임새: 7장. "리뷰 코멘트 → 린트 승격"의 산업 선례. "분석기도 사용자 피드백으로 eval한다" = Lauren의 skill eval과 동형.

### 논문 5-2: Lessons from Building Static Analysis Tools at Google ✅(세부 수치 ❓)
- 저자·연도: Caitlin Sadowski, Edward Aftandilian, Alex Eagle, Liam Miller-Cushon, Ciera Jaspan, 2018
- 발표처: *Communications of the ACM* 61(4), pp. 58–66 · DOI 10.1145/3188720
- 피인용수: 274 (S2)
- 요약(acawiki 요약 기준): FindBugs 도입이 2006·2009·2011 세 번 실패한 뒤 얻은 교훈 — (1) 대형 코드베이스에서 버그 찾기는 쉽다, (2) 대부분의 개발자는 도구를 찾아가 쓰지 않는다, (3) 개발자 행복이 핵심(오탐 → 도구 불신), (4) 찾지 말고 고치게 하라, (5) 분석기 개발을 크라우드소싱, (6) **가능한 한 이른 워크플로(컴파일러 에러·코드 리뷰)에 통합**, (7) 경고 무시(warning blindness)를 막기 위해 개발자가 고치고 싶어 하는 리포트만 남겨라. "코드 리뷰는 분석 경고를 보여주기에 최적의 지점(sweet spot)". 대다수 엔지니어가 매일 사용, 하루 수천 건이 체크인 전 수정.
- 미확인: "Not useful 비율 10% 미만 유지" 임계값은 기억 기반 — 본문에서 확인 못 함 → 인용 금지.
- 책에서의 쓰임새: 7장 핵심. Lauren의 집행 피라미드(아키텍처 > 컴파일러/CI > 룰/스킬)와 1:1 대응. 특히 "도구를 안 믿게 되는 원인은 오탐" = §1-2 disuse의 소프트웨어 버전.

### 논문 5-3: Scaling Static Analyses at Facebook ✅(배치 수정률 ⚠️)
- 저자·연도: Dino Distefano, Manuel Fähndrich, Francesco Logozzo, Peter W. O'Hearn, 2019
- 발표처: *Communications of the ACM* 62(8) · DOI 10.1145/3338112
- 피인용수: 227 (S2)
- 요약: Infer(모바일·백엔드 C++ 크래시)와 Zoncolan(보안). 코드 수정(diff)마다 **코드 리뷰 봇으로 참여**. 개발자가 고친 이슈 **10만 건 이상**. 핵심 통찰: "diff time" 배포 — 이슈를 코드 리뷰 중 즉시 보여주는 것이 조기 발견과 높은 수정률의 열쇠. 수정률 **70% 이상**(⚠️ TechBeacon 요약). 같은 분석을 **워크플로 밖 배치 리스트로 주면 수정률 0%/near-zero**(⚠️ 2차: 블로그 인용, InferFix arXiv 2303.07263의 관련연구 절은 "오탐 20% 미만, 수정률 70%, CI 밖 배정 시 near-zero"로 기술).
- 책에서의 쓰임새: 7장 핵심 수치. **"같은 규칙도 어디서 집행하느냐가 수정률 70% vs 0%를 가른다"** — Lauren의 "코드 리뷰 랜드가 최악"과 "CI 빨간불" 논지의 가장 강한 정량 근거. 에이전트에게도 동일: PR 코멘트가 아니라 CI 실패로 피드백해야 고친다.

### 논문 5-4: Expectations, Outcomes, and Challenges of Modern Code Review ✅
- 저자·연도: Alberto Bacchelli, Christian Bird (Microsoft), 2013
- 발표처: ICSE 2013, pp. 712–721 · DOI 10.1109/ICSE.2013.6606617
- 피인용수: 905 (S2)
- 요약: Microsoft 개발자 관찰·인터뷰·설문 + 리뷰 코멘트 수백 건 수동 분류. 리뷰의 1순위 동기는 "결함 발견"이지만 **실제 리뷰는 결함보다 지식 전달·팀 인지·코드 개선(가독성·관행)에 치우침**.
- 책에서의 쓰임새: 8장(리뷰 → 린트). "사람이 PR 코멘트로 지키는 불변식은 code smell" — 리뷰 코멘트의 다수가 결함이 아니라 관행이라면, 그 관행은 린트로 자동화 가능.

### 논문 5-5: Characteristics of Useful Code Reviews: An Empirical Study at Microsoft ✅
- 저자·연도: Amiangshu Bosu, Michaela Greiler, Christian Bird, 2015
- 발표처: MSR 2015
- DOI: 미확인
- 요약: 유용한/비유용 코멘트 분류기 구축 후 Microsoft 5개 프로젝트 **150만 건** 코멘트 분류. 변경에 포함된 **파일 수가 많을수록 유용한 코멘트 비율 감소**.
- 책에서의 쓰임새: 8장·9장. "원자적 PR"(Lauren, 50~1,000줄·하드캡 없음·원자적 분할 권장)의 근거 — PR이 커질수록 리뷰 품질이 떨어진다.

### 논문 5-6: Modern Code Review: A Case Study at Google ✅
- 저자·연도: Caitlin Sadowski, Emma Söderberg, Luke Church, Michal Sipko, Alberto Bacchelli, 2018
- 발표처: ICSE-SEIP 2018, pp. 181–190 · DOI 10.1145/3183519.3183525
- 피인용수: 393 (S2)
- 요약: 인터뷰 12건, 설문 44명, **900만 건** 리뷰 로그. Google 리뷰는 경량·도구 기반·비동기·작은 diff 중심. (중앙값 리뷰어 수·줄 수 등 세부 수치는 본문 미접근 → ❓)
- 책에서의 쓰임새: 8장. "작은 변경 + 자동 분석 결과를 리뷰 화면에" 모델의 산업 표준 사례.

### 논문 5-7: AI-Assisted Assessment of Coding Practices in Modern Code Review (AutoCommenter) ✅(venue ⚠️)
- 저자·연도: Manushree Vijayvergiya 외 (Google), 2024
- 발표처: AIware 2024로 추정(UW 호스팅 PDF 파일명 기준) — ICSE-SEIP 아님
- 요약: 인간 리뷰 코멘트 중 "베스트 프랙티스 문서 링크"가 달린 것을 학습 데이터로 삼아(약 80만 건), T5 기반 모델이 C++/Java/Python/Go 코드에서 **관행 위반 위치 + 해당 문서 URL**을 예측. Google에서 수만 명이 매일 사용, 워크플로에 측정 가능한 긍정 효과.
- 책에서의 쓰임새: 8장. "어떤 리뷰 코멘트가 자동화 가능한가"의 직접 답 — 문서로 표준화된 관행 위반은 자동화됐다. 남은 것만 사람이 본다.

### 논문 5-8: Understanding Software Architecture Erosion: A Systematic Mapping Study ✅(저자 ❓)
- 저자·연도: (arXiv 2112.10934, 2021; 저자 미확인)
- 요약: 아키텍처 침식(erosion) 연구 지도. 침식 탐지·**아키텍처 적합성 검사(ACC: 구현이 의도된 아키텍처와 일치하는지 검사)** 도구(Lattix, ArCh, ConQAT, SAVE, ARCADE, Dclcheck 등)를 분류.
- 관련: Passos 외, *IEEE Software* 2010 — 정적 적합성 검사 3기법(DSM·소스 질의 언어·reflexion model) 비교, "편차는 시간이 지나며 누적되어 침식이 된다". Pruijt 외 2016 — ACC 도구 10종의 의존성 분석 정확도 벤치마크. Monteiro 박사논문(UFCG 2014) — "소수의 엔티티가 위반의 대다수를 만든다".
- 책에서의 쓰임새: 7장. "임포트 경계 검사를 CI에"(Lauren의 main/renderer 경계)를 Java/Spring의 ArchUnit·Next.js의 eslint `no-restricted-imports`/dependency-cruiser로 옮길 때의 학술 배경. ArchUnit 자체의 실증 연구는 **미발견**.
- 비고: "Pit of success / make the right thing easy"는 학술 용어가 아님(Rico Mariani의 Microsoft 블로그 기원으로 알려짐 — ❓ 미확인). 책에서는 업계 관용구로만 쓰고 논문 인용 금지.

---

## 6. 멀티 에이전트 조율

### 논문 6-1: Why Do Multi-Agent LLM Systems Fail? ✅
- 저자·연도: Mert Cemri 외 12명 (UC Berkeley 등), 2025 (v1 2025-03, v3 2025-10-26)
- arXiv: 2503.13657
- 요약: 7개 멀티 에이전트 프레임워크의 **1,600건 이상** 트레이스를 주석(초기 150건 전문가 분석, κ=0.88)해 **MAST** 분류체계 도출 — 14개 실패 모드, 3범주: (i) 명세·시스템 설계 실패, (ii) 에이전트 간 불일치(misalignment), (iii) **과업 검증·종료 실패**. 실패의 주원인은 모델 한계가 아니라 **시스템 설계와 에이전트 간 조율**. 역할 명세 강화·오케스트레이션 개선 같은 단순 개입은 일부 개선하지만 충분치 않음. 데이터셋·주석기 공개(GitHub MAST).
- 책에서의 쓰임새: 9장(코디네이터/서브에이전트). 병렬 에이전트의 충돌·중복이 "모델 탓"이 아니라 "설계 탓"이라는 근거. 세 번째 범주(검증·종료)가 Lauren의 Verification과 직결.

### 논문 6-2: Towards a Science of Scaling Agent Systems ✅
- 저자·연도: Yubin Kim, Xin Liu 외 (Google Research · MIT · DeepMind), 2025-12 (Google Research 블로그 2026-01)
- arXiv: 2512.08296
- 요약: 4개 에이전트 벤치마크(Finance-Agent, BrowseComp-Plus, PlanCraft, Workbench) × 5개 아키텍처(Single, Independent, Centralized, Decentralized, Hybrid) × 3개 LLM 계열 = **180개 구성**, 도구·토큰 예산 통제. 결과: **병렬화 가능한 과업**에선 중앙집중 조율이 +80.9%; **순차 추론 과업**에선 모든 멀티 에이전트 변형이 −39~−70%; 도구 집약 과업은 고정 예산에서 조율 오버헤드가 큼; **단일 에이전트 기준선이 약 45%를 넘으면 조율 이득이 줄거나 음수**; 독립 에이전트는 오류를 **17.2배** 증폭(중앙집중 4.4배). 조율 지표로 만든 예측 모델 교차검증 R²=0.513(블로그: 미지 과업의 87%에서 최적 아키텍처 예측).
- 책에서의 쓰임새: 9장 핵심. (a) "단계를 건너뛰지 말라" — 단일 에이전트가 믿을 만해지기 전 병렬화는 오류 증폭. (b) 코디네이터(Chief of Staff) 패턴이 독립 병렬보다 오류 증폭이 4배 적다. (c) 순차 의존 과업(마이그레이션·리팩터링 체인)은 병렬화하지 말라.
- 독자 전달: "에이전트 수를 늘리는 것은 서버 수를 늘리는 것과 다르다. 작업이 병렬 가능하고, 결과를 검증할 수 있을 때만 스케일된다."

### 논문 6-3: A Survey of Context Engineering for Large Language Models ✅
- 저자·연도: Lingrui Mei 외 14명, 2025 (v1 2025-07-17, v2 2025-07-21)
- arXiv: 2507.13334
- 요약: 1,400편 이상 분석. 컨텍스트 엔지니어링을 프롬프트 설계를 넘어선 "모델에 주는 정보의 체계적 최적화"로 정식화. 기초 요소(검색·생성 / 처리 / 관리) + 시스템 구현(RAG / 메모리·도구 통합 추론 / 멀티 에이전트). 핵심 관찰: **이해-생성 비대칭** — 모델은 복잡한 컨텍스트를 잘 이해하지만 그만큼 정교한 장문 출력은 못 만든다.
- 책에서의 쓰임새: 5장(Skills). "스킬 = 고품질 토큰을 먼저 넣어 모델을 더 똑똑한 latent space로"(Lauren)를 컨텍스트 엔지니어링 용어로 번역. 서베이 앵커.

---

## 7. 작업 특화 지침(AGENTS.md류)의 효과 — 상충하는 실증

### 논문 7-1: Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? ✅
- 저자·연도: Thibaud Gloaguen, Niels Mündler-Sasahara, Mark Niklas Müller, Veselin Raychev, Martin Vechev (소속 ❓ — arXiv 페이지에 미표기), 2026 (v1 2026-02-12, v3 2026-09-29) · ICLR 2026 가상 세션 등재
- arXiv: 2602.11988
- 요약: 두 설정 — (a) SWE-bench 과업 + LLM 생성 컨텍스트 파일, (b) 개발자가 직접 커밋한 컨텍스트 파일이 있는 저장소의 신규 이슈. 결과: 컨텍스트 파일은 **과업 성공률을 일반적으로 올리지 못하면서 추론 비용을 평균 20% 이상 올린다**. 여러 LLM·에이전트·파일 출처에서 일관. 에이전트는 지시를 잘 따르지만 **저장소 개요(overview)는 도움이 안 됨**(모델 제공사가 권장함에도). 유용한 경우: **비표준 코딩 관행을 명시할 때**. "성능 개선 시도는 배포 전 엄격히 평가하라".
- 책에서의 쓰임새: 5장·7장 핵심. Lauren의 두 주장을 동시에 뒷받침 — (1) "소프트 룰(AGENTS.md)만으론 안 된다"; (2) "스킬은 관찰된 실패 패턴에서만, 한 번에 하나, eval로 검증". 코드베이스에 이미 있는 정보를 반복하는 CLAUDE.md는 비용만 올린다.
- 주의: Python 저장소 편중 지적 있음.

### 논문 7-2: On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents ✅
- 저자·연도: Jai Lal Lulla, Seyedmoein Mohsenimofidi, Matthias Galster, Jie M. Zhang, Sebastian Baltes, Christoph Treude, 2026 (v1 2026-01-28, v2 2026-03-30)
- arXiv: 2601.20404
- 피인용수: 25 (S2)
- 요약: 10개 저장소, **124개 PR**, AGENTS.md 유/무 두 조건으로 에이전트 실행. AGENTS.md가 있으면 **중앙값 실행 시간 −28.64%, 출력 토큰 −16.58%**, 과업 완료 행동은 비슷. 성공률 지표가 아니라 **효율** 지표.
- 책에서의 쓰임새: 5장. 7-1과의 상충을 그대로 보여줄 것 — "성공률은 안 오르지만(7-1) 실행은 빨라진다(7-2)"는 두 결과는 모순이 아니라 **컨텍스트 파일의 역할이 '똑똑하게'가 아니라 '헤매지 않게'**라는 해석으로 통합 가능. 단, 소규모 표본.

### 논문 7-3: Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories ❓
- arXiv: 2607.27250 (2026-07로 추정) — 검색 결과 제목만 확인, 저자·결과 미확인. 7-1(Codex 계열)과 7-2(Claude 계열)의 에이전트·평가법·통제 차이를 지적한다고 요약됨.
- 책에서의 쓰임새: 확인 전까지 인용 금지. fact-checker가 재확인할 것.

---

## 수집 한계 및 미확인 항목

1. **본문 접근 실패**: Tricorder(5-1)·Google Lessons(5-2)·Infer(5-3)는 PDF 텍스트 추출 도구(pdftotext/poppler) 부재로 본문 수치를 직접 확인하지 못함. Infer의 "70% vs near-zero"는 2차(TechBeacon·InferFix 논문). Google Lessons의 "Not useful 10% 임계값"은 기억 기반 → 인용 금지.
2. **DOI 미확인**: Parasuraman & Riley 1997, Wickens & Dixon 2007, Bosu et al. 2015. 원본 SWE-bench(Jimenez et al. 2024) 식별자 미조회.
3. **초록 비공개**: de Visser et al. 2018(출판사 차단) — 주장만 인용.
4. **업계 리포트(준학술)**: DORA 2024/2025, GitClear 2025, Uplevel 2024, SWE-bench Verified(OpenAI 블로그). 수치는 모두 "리포트명 + 연도" 꼬리표 필수. Uplevel은 근거 약함.
5. **피인용수 미조회**: Semantic Scholar rate limit으로 2306.05685·2404.13076·2302.06590·2410.12944·2304.05128·2303.11366·2407.21787·2503.13657·2512.08296·2602.11988·2505.23836·2305.17926·2404.18796·2507.13334·2405.15793·2501.14723·2509.16941·2305.11248·2310.01798·2410.21819·2108.09293 미조회.
6. **미발견**: ArchUnit 등 의존성 규칙 집행 도구의 결함 예방 효과를 직접 측정한 논문; 코딩 eval에서 sandbagging을 관측한 연구; Java/Spring·React 특화 에이전트 벤치마크.
7. **7-3**(arXiv 2607.27250) 전체 미확인.
