# 논문 리서치: AI-native SDLC playbook — "왜 이 play가 작동하는가"의 학술 근거

- 검색 시점: 2026-10-19
- 검색 소스: arXiv API(식별자·초록), Crossref API(DOI·권호·쪽), Semantic Scholar batch API(피인용수·초록), PubMed E-utilities(Human Factors 초록), 공개 웹(OpenAI·METR·Anthropic 1차 발표문 확인용)
- 원장 규율: 모든 저자·연도·발표처·DOI/arXiv ID는 위 API로 실제 조회해 일치한 값만 적었다. 수치는 초록 원문 표현 그대로 옮기고 표본·조건을 병기했다. 초록을 직접 확보하지 못한 항목은 "원문 미대조"로 표시했다.
- 피인용수는 Semantic Scholar 2026-10-19 조회값. 빠르게 변하므로 본문에는 쓰지 말고 비중 판단에만 쓸 것.
- 상태 라벨: **[심사 통과]** 학회·저널 게재 확정 / **[프리프린트(미심사)]** arXiv만 존재 / **[비학술 1차 자료]** 기업·기관 발표문

## 코스 play ↔ 근거 매핑 (저술가용 빠른 색인)

| 코스 play | 뒷받침하는 논문 번호 | 근거의 종류 |
|---|---|---|
| 도입: "코드는 빨라졌는데 프로세스는 그대로" | 1, 2, 3, 4, 6 | 생산성 효과가 조건에 따라 +55.8%에서 −19%까지 갈린다 — 도구가 아니라 주변 프로세스가 변수 |
| Plan: intent.md 캡처 | 17, 18, 19 | 모호한 요구사항이 LLM 성능을 일관되게 떨어뜨리고, 명확화 질문이 Pass@1을 올린다 |
| Design: spec.md | 16, 17, 20 | 스펙 기반 생성의 효과와 한계(보안 요구는 암묵적으로 남는다) |
| Build: plan mode | 14, 15, 21 | plan-then-execute 아키텍처의 효과(누락 단계 오류 감소, 장기 과제 성공률) |
| Build: CLAUDE.md·skills | 22, 23 | 실제 Claude Code 프로젝트의 설정 파일 실증(328개·2,853개 저장소) |
| Build: 병렬 세션·서브에이전트 | 15, 21 | Planner/Executor 분리의 근거 |
| Test: 피드백 루프 | 5, 12 | 사람은 검증에 시간을 쓴다(CUPS) / 테스트가 약하면 pass@k가 19.3–28.9% 과대평가 |
| Test: CI 지속 평가(evals) | 7, 8, 9, 10, 11, 12, 13 | 벤치마크 오염·누출·약한 테스트, LLM-as-judge의 위치 편향, 홀드아웃 부재 |
| Deploy: AI PR 리뷰 | 24, 25, 26, 27, 28, 29 | 리뷰 자동화 효과와 비용(PR 종료 시간 5h52m → 8h20m), 에이전트 PR 수락률 83.8% |
| Deploy: hooks 승인 게이트 | 30, 31, 32, 33, 34 | 자동화 안주·자동화 편향은 훈련으로 못 막는다 — 구조적 게이트가 필요한 이유 |
| Deploy: 보안 | 24, 25, 26, 27 | 생성 코드의 약 40%·29.5%·24.2% 취약, AI 사용자는 더 안전하다고 "믿는다" |
| Maintain: 메트릭 루프 | 35, 36, 37, 38, 39, 40 | DORA·SPACE·DevEx의 학술 출처, Goodhart 변종 분류, 관리도(Western Electric)의 출전 |

---

## 1부. AI 코딩 도구의 생산성·품질 실증 (RCT·필드 연구)

### 논문 1: The Impact of AI on Developer Productivity: Evidence from GitHub Copilot
- 저자·연도: Sida Peng, Eirini Kalliamvakou, Peter Cihon, Mert Demirer (2023)
- 발표처: arXiv **[프리프린트(미심사)]** — 가장 많이 인용되는 Copilot RCT이지만 저널 게재 확인 못 함
- DOI/arXiv ID: arXiv:2302.06590 (2023-02-13 공개)
- 피인용수: 841
- 요약: 모집된 개발자에게 JavaScript로 HTTP 서버를 "가능한 한 빨리" 구현하게 한 통제 실험. Copilot 접근 그룹이 통제 그룹보다 과제를 55.8% 빨리 완료했다. 이질적 효과를 관찰했고, 경력 전환자에게 특히 유망하다고 해석한다.
- 방법론 요약: 단일 과제·단일 세션 통제 실험(자유 모집 프리랜서). 초록은 표본 수를 명시하지 않는다(본문 95명으로 알려졌으나 초록에 없으므로 본문 인용 시 "원문 미대조" 유지).
- 핵심 수치·결과: "completed the task 55.8% faster than the control group" — 조건: 신규 코드(greenfield), 단일 과제, 초보~중급 포함.
- 인용할 만한 문장:
  > "The treatment group, with access to the AI pair programmer, completed the task 55.8% faster than the control group." (초록)
- 독자 전달 방식 제안: "55.8%"는 '빈 디렉터리에서 시작하는 과제'의 수치다. 논문 2(기존 대형 코드베이스)와 나란히 놓으면, 코스 도입부의 "코드 생성 속도 vs 프로세스" 논점이 숫자로 선다.

### 논문 2: Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity (METR RCT)
- 저자·연도: Joel Becker, Nate Rush, Elizabeth Barnes, David Rein (2025)
- 발표처: arXiv **[프리프린트(미심사)]**; METR 블로그 2025-07-10 공개
- DOI/arXiv ID: arXiv:2507.09089 (v2 2025-07-25)
- 피인용수: 217
- 요약: 2025년 2~6월 프론티어 AI 도구가 숙련 오픈소스 개발자의 생산성에 미치는 영향을 RCT로 측정. 개발자 16명이 평균 5년 기여한 성숙 프로젝트의 과제 246개를 수행, 과제별로 AI 허용/불허를 무작위 배정. AI 허용 시 주로 Cursor Pro + Claude 3.5/3.7 Sonnet 사용. 결과는 AI 허용이 완료 시간을 19% 늘렸다는 것. 개발자는 사전 24%, 사후에도 20% 단축을 믿었다.
- 방법론 요약: 과제 단위 무작위화(within-subject), 실제 저장소·실제 이슈, 화면 녹화로 시간 측정. 느려진 이유 후보 20가지를 수집·평가했으나 단일 원인을 확정하지 않음.
- 핵심 수치·결과 (초록 원문 그대로):
  - "16 developers with moderate AI experience complete 246 tasks in mature projects on which they have an average of 5 years of prior experience."
  - "developers forecast that allowing AI will reduce completion time by 24%. After completing the study, developers estimate that allowing AI reduced completion time by 20%."
  - "allowing AI actually increases completion time by 19%--AI tooling slowed developers down."
  - 전문가 예측과도 모순: 경제학자 39% 단축, ML 연구자 38% 단축 예측.
- 인용할 만한 문장:
  > "Surprisingly, we find that allowing AI actually increases completion time by 19%--AI tooling slowed developers down." (초록)
  > "Although the influence of experimental artifacts cannot be entirely ruled out, the robustness of the slowdown effect across our analyses suggests it is unlikely to primarily be a function of our experimental design." (초록)
- 주의: 조건이 좁다(16명, 고품질 기준의 성숙 프로젝트, 2025년 초 도구). METR 자신도 소규모 신규 프로젝트나 낯선 코드베이스에서는 속도 향상과 양립 가능하다고 적는다. 일반화해서 "AI는 개발자를 느리게 한다"로 쓰면 왜곡.
- 독자 전달 방식 제안: "체감 20% 빨라짐 vs 실측 19% 느려짐" — 39%포인트 인식 격차. 이 격차 자체가 코스의 "메트릭으로 루프를 닫아라"(Stage 6)와 "검증 가능한 피드백 루프"(Stage 4)의 가장 강한 논거다. 느낌으로는 알 수 없다.

### 논문 3: The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers
- 저자·연도: Kevin Zheyuan Cui, Mert Demirer, Sonia Jaffe, Leon Musolff, Sida Peng, Tobias Salz (2026 게재; 2024 워킹페이퍼)
- 발표처: *Management Science* **[심사 통과]** (게재일 2026-02-27)
- DOI/arXiv ID: DOI 10.1287/mnsc.2025.00535 (RCT 등록: AEA RCT Registry DOI 10.1257/rct.14530)
- 피인용수: 189
- 요약: Microsoft·Accenture·익명의 Fortune 100 기업에서 통상 업무 중 실행된 세 건의 필드 RCT. 무작위로 선택된 개발자에게 코드 완성형 AI 어시스턴트 접근권을 부여. 각 실험은 노이즈가 크고 결과가 갈리지만, 합산하면 완료 과제 수가 26.08% 증가. 경력이 짧은 개발자가 더 많이 채택하고 더 큰 이득을 봤다.
- 방법론 요약: 실제 기업의 자연 실험(개발자 4,867명), 결과 변수는 완료 과제(PR 등) 수.
- 핵심 수치·결과 (초록 원문): "when data are combined across three experiments and 4,867 developers, our analysis reveals a 26.08% increase (standard error: 10.3%) in completed tasks among developers using the AI tool." / "less experienced developers had higher adoption rates and greater productivity gains."
- 인용할 만한 문장:
  > "Although each experiment is noisy and results vary across experiments, when data are combined across three experiments and 4,867 developers, our analysis reveals a 26.08% increase (standard error: 10.3%) in completed tasks." (초록)
- 주의: 도구는 자동완성형(agentic 아님). 표준오차 10.3%p는 신뢰구간이 넓다는 뜻 — 본문에서 "26%"만 떼어 쓰지 말고 표준오차를 같이 쓸 것.
- 독자 전달 방식 제안: 논문 1·2·3을 한 표로 — 과제 유형(신규/성숙), 측정 단위(시간/과제 수), 표본(95?/16/4,867). "효과 크기는 도구가 아니라 상황이 정한다"는 코스 도입부 메시지.

### 논문 4: How much does AI impact development speed? An enterprise-based randomized controlled trial (Google)
- 저자·연도: Elise Paradis, Kate Grey, Quinn Madison, Daye Nam 외 (2024; 2025 게재)
- 발표처: ICSE-SEIP 2025 **[심사 통과]**
- DOI/arXiv ID: arXiv:2410.12944; DOI 10.1109/ICSE-SEIP66354.2025.00060
- 피인용수: 40
- 요약: Google 정규직 엔지니어 96명 RCT. 복잡한 엔터프라이즈급 과제에서 세 가지 AI 기능이 과제 소요 시간에 미친 영향을 측정. AI가 유의하게 시간을 줄였고 최선 추정치는 약 21%지만 신뢰구간이 넓다. 하루 코드 작업 시간이 긴 개발자가 AI로 더 빨라졌다.
- 핵심 수치·결과 (초록 원문): "randomized controlled trial with 96 full-time Google software engineers" / "Our best estimate of the size of this effect ... stands at about 21%, although our confidence interval is large."
- 인용할 만한 문장:
  > "we cannot assume that the effect size obtained in our lab study will necessarily apply more broadly, or that the effect of AI found using internal Google tooling in the summer of 2024 will translate across tools and over time." (초록)
- 독자 전달 방식 제안: 저자들이 스스로 일반화를 경계하는 문장이 좋은 모델이다 — 코스가 "leading/lagging indicator를 네 팀에서 측정하라"고 하는 이유.

### 논문 5: Reading Between the Lines: Modeling User Behavior and Costs in AI-Assisted Programming (CUPS)
- 저자·연도: Hussein Mozannar, Gagan Bansal, Adam Fourney, Eric Horvitz (2022; CHI 2024 게재)
- 발표처: CHI 2024 **[심사 통과]** (arXiv comment에 "CHI 2024" 명시)
- DOI/arXiv ID: arXiv:2210.14306 (ACM DOI 미확인)
- 피인용수: 248
- 요약: Copilot 사용 중 프로그래머 행동의 분류체계 CUPS를 만들고, 프로그래머 21명의 세션을 회고 라벨링. 제안을 읽고 검증하는 데 드는 시간 비용과 비효율을 드러냈다.
- 핵심 수치·결과: 21명 연구. (초록은 "검증에 쓴 시간 비율" 수치를 적지 않음 — 본문 수치는 원문 미대조.)
- 인용할 만한 문장:
  > "Our study of 21 programmers ... showed that CUPS can help us understand how programmers interact with code-recommendation systems, revealing inefficiencies and time costs." (초록)
- 독자 전달 방식 제안: "AI가 쓴 코드를 사람이 읽는 시간"이 병목이라는 코스 Stage 4의 전제를 뒷받침. 수치 없이 개념(검증 비용)으로 인용.

### 논문 6: Productivity Assessment of Neural Code Completion
- 저자·연도: Albert Ziegler, Eirini Kalliamvakou, X. Alice Li, Andrew Rice, Devon Rifkin, Shawn Simister 외 (2022)
- 발표처: MAPS '22 (ACM SIGPLAN International Symposium on Machine Programming) **[심사 통과]**
- DOI/arXiv ID: arXiv:2205.06537; DOI 10.1145/3520312.3534864
- 피인용수: 326
- 요약: Copilot 사용자 설문과 실측 데이터를 대조. 제안 수락률이, 코드에 남아 있는지(persistence) 같은 더 구체적 지표보다 개발자의 "생산성 체감"을 더 잘 설명했다.
- 인용할 만한 문장:
  > "We find that the rate with which shown suggestions are accepted, rather than more specific metrics regarding the persistence of completions in the code over time, drives developers' perception of productivity." (초록)
- 독자 전달 방식 제안: 체감은 수락률에 끌려간다 — 논문 2의 인식 격차와 묶어 "자기 보고 메트릭을 믿지 말라"의 근거. 코스 Stage 6의 lagging indicator(PR 메타데이터·인시던트)를 쓰는 이유.

---

## 2부. 에이전틱 코딩 벤치마크와 평가 방법론 (코스 "Continuous evals in CI"의 근거)

### 논문 7: SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
- 저자·연도: Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao 외 (2023; ICLR 2024)
- 발표처: ICLR 2024 **[심사 통과]**
- DOI/arXiv ID: arXiv:2310.06770; OpenReview VTF8yNQM66
- 피인용수: 4,407
- 요약: 12개 인기 Python 저장소의 실제 GitHub 이슈·PR 2,294개로 구성. 이슈 설명과 코드베이스를 주고 코드를 수정하게 한다. 여러 파일·함수에 걸친 변경과 실행 환경 상호작용이 필요. 발표 당시 최고 모델 Claude 2가 1.96%만 해결.
- 핵심 수치·결과: "2,294 software engineering problems ... 12 popular Python repositories" / "Claude 2, is able to solve a mere 1.96% of the issues" (2023년 기준값 — 신선도 주의).
- 독자 전달 방식 제안: 코스의 eval 포맷(prompt + from 커밋 + checks)은 SWE-bench 인스턴스 구조(이슈 + base commit + FAIL_TO_PASS 테스트)의 축소판이다. "너의 저장소로 만든 사설 SWE-bench"라고 소개하면 바로 이해된다.

### 논문 8: SWE-bench Verified (OpenAI, 2024-08-13)
- 저자·연도: OpenAI Preparedness 팀 + SWE-bench 저자 (2024)
- 발표처: OpenAI 블로그 **[비학술 1차 자료]** — 논문 아님
- DOI/arXiv ID: 없음. URL: openai.com/index/introducing-swe-bench-verified/
- 요약: 원본 테스트셋에서 전문 개발자 93명이 "문제 없음"으로 검증한 500개 하위집합. 이슈 설명의 과소명세(underspecified)와 과도하게 좁은 단위 테스트를 걸러냈다.
- 핵심 수치·결과: "500 samples verified to be non-problematic by our human annotators" / "93 professional software developers". (원본 중 제외 비율 68.3%는 2차 자료 수치 — 원문 미대조, 본문 사용 금지.)
- 독자 전달 방식 제안: 코스가 "20~50개 실제 과제"로 시작하라고 하는 이유 — 벤치마크조차 사람이 걸러낸 500개로 줄였다. 양보다 "검증 가능한 정답"이 중요하다.

### 논문 9: SWE-Bench+: Enhanced Coding Benchmark for LLMs
- 저자·연도: Reem Aleithan, Haoran Xue, Mohammad Mahdi Mohajer, Elijah Nnorom 외 (2024)
- 발표처: arXiv **[프리프린트(미심사)]**
- DOI/arXiv ID: arXiv:2410.06992
- 피인용수: 127
- 요약: 당시 리더보드 1위 SWE-Agent+GPT-4의 "성공" 패치를 수작업 검토. 성공 패치의 32.67%는 이슈 본문·댓글에 답이 적혀 있던 "해답 누출", 31.08%는 테스트가 약해 정답성을 못 보장하는 "의심 패치". 이를 제거하면 해결률이 12.47%에서 3.97%로 떨어졌다. Lite·Verified 변종에도 같은 문제가 있고, 94% 이상의 이슈가 LLM 지식 컷오프 이전에 생성됨.
- 핵심 수치·결과 (초록 원문): "32.67% of the successful patches involve cheating as the solutions were directly provided in the issue report or the comments" / "31.08% of the passed patches are suspicious patches due to weak test cases" / "resolution rate of SWE-Agent+GPT-4 dropped from 12.47% to 3.97%" / "over 94% of the issues were created before LLM's knowledge cutoff dates".
- 독자 전달 방식 제안: 코스 eval 예제에서 `evals/` 폴더를 실행 체크아웃에서 지우고, `may_change` 밖 파일 변경을 실패 처리하고, 체크 스크립트를 "실행 전 복사본"에서 돌리는 세 가지 장치는 정확히 이 논문의 세 결함(누출·약한 테스트·채점기 조작)에 대응한다. 이 대응 관계를 표로 보여주면 설계 의도가 선다.

### 논문 10: SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?
- 저자·연도: Xiang Deng, Jeff Da, Edwin Pan, Yannis Yiming He 외 (Scale AI, 2025)
- 발표처: arXiv **[프리프린트(미심사)]**
- DOI/arXiv ID: arXiv:2509.16941 (v2 2025-11-14)
- 피인용수: 308
- 요약: 41개 활발한 저장소에서 1,865개 문제. 공개 셋(11개 저장소)·홀드아웃 셋(12개)·상업 셋(18개 비공개 스타트업 저장소)으로 분할해 오염 저항성 확보. 전문가가 수 시간~수 일 걸리는 장기 과제, 다중 파일 패치. 모든 과제는 사람이 검증하고 해결 가능하도록 컨텍스트를 보강.
- 핵심 수치·결과: "1,865 problems sourced from a diverse set of 41 actively maintained repositories". (최고 성능 "45% 미만"은 2차 자료 — 원문 미대조.)
- 독자 전달 방식 제안: "홀드아웃 셋"이라는 개념 — 코스가 "모델이 좋아지면 더 이상 변별하지 못하는 케이스를 교체하라"고 하는 live suite 논리와 통한다.

### 논문 11: Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces
- 저자·연도: Mike A. Merrill, Alexander G. Shaw, Nicholas Carlini, Boxuan Li 외 (2026)
- 발표처: ICLR 2026 **[심사 통과]** (proceedings.iclr.cc 등재 확인); arXiv 2026-01-17
- DOI/arXiv ID: arXiv:2601.11868
- 피인용수: 613
- 요약: Terminal-Bench 2.0 — 실제 워크플로에서 영감을 받은 터미널 환경 과제 89개. 각 과제는 고유 환경·사람이 쓴 정답·검증 테스트를 갖는다. 프론티어 모델·에이전트가 65% 미만. 오류 분석 포함, 데이터셋·하네스 공개(tbench.ai).
- 핵심 수치·결과: "89 tasks in computer terminal environments" / "frontier models and agents score less than 65%".
- 독자 전달 방식 제안: Claude Code가 사는 곳이 터미널이다. "환경 + 사람의 정답 + 테스트"라는 과제 3요소가 코스 eval JSON의 `from` + `prompt` + `checks`와 1:1 대응.

### 논문 12: Is Your Code Generated by ChatGPT Really Correct? (EvalPlus / HumanEval+)
- 저자·연도: Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, Lingming Zhang (2023)
- 발표처: NeurIPS 2023 **[심사 통과]**
- DOI/arXiv ID: arXiv:2305.01210
- 피인용수: 2,400
- 요약: 기존 벤치마크 테스트가 부족해 틀린 코드를 통과시킨다는 문제 제기. LLM·변이 기반 자동 생성기로 HumanEval 테스트를 80배 확장(HumanEval+). 26개 LLM에서 미검출 오답을 잡아 pass@k가 최대 19.3–28.9% 하락, 모델 순위도 뒤바뀜.
- 핵심 수치·결과 (초록 원문): "extend the test-cases of the popular HumanEval benchmark by 80x" / "reducing the pass@k by up-to 19.3-28.9%" / "test insufficiency can lead to mis-ranking".
- 인용할 만한 문장:
  > "prior popular code synthesis evaluation results do not accurately reflect the true performance of LLMs for code synthesis" (초록)
- 독자 전달 방식 제안: 코스 Stage 4 "피드백 루프"의 숨은 전제 — 테스트가 약하면 에이전트는 약한 테스트를 통과하는 코드를 쓴다. "테스트를 고치지 말고 코드를 고쳐라"는 CLAUDE.md 규칙과, 테스트 파일 편집을 막는 hook의 이유.

### 논문 13: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
- 저자·연도: Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang 외 (2023)
- 발표처: NeurIPS 2023 Datasets and Benchmarks Track **[심사 통과]**
- DOI/arXiv ID: arXiv:2306.05685
- 피인용수: 12,265
- 요약: 강한 LLM을 심판으로 쓰는 방식의 효용과 한계를 체계화. 위치 편향·장황함 편향·자기 선호 편향·제한된 추론 능력을 식별하고 완화책 제시. GPT-4 심판은 통제·크라우드소싱 인간 선호와 80% 이상 일치 — 인간끼리의 일치 수준과 같다.
- 핵심 수치·결과: "position, verbosity, and self-enhancement biases" / "achieving over 80% agreement, the same level of agreement between humans".
- 독자 전달 방식 제안: 코스의 eval `checks`가 전부 결정론적 명령(`make test`, 셸 스크립트)인 이유. LLM 심판을 쓰려면 이 세 편향을 알고 써야 한다. 코스 REVIEW.md의 "Important vs Nit" 정의도 장황함 편향(더 많이 쓴 리뷰가 더 좋아 보임)에 대한 방어로 읽을 수 있다.

### 논문 14: Large Language Models are not Fair Evaluators
- 저자·연도: Peiyi Wang, Lei Li, Liang Chen, Zefan Cai 외 (2023; ACL 2024)
- 발표처: ACL 2024 **[심사 통과]**
- DOI/arXiv ID: arXiv:2305.17926
- 피인용수: 1,413
- 요약: LLM 심판 비교 평가가 후보 응답의 "등장 순서"만 바꿔도 뒤집힌다는 체계적 편향. ChatGPT 심판에서 Vicuna-13B가 80개 중 66개 질의에서 ChatGPT를 이기게 조작 가능. 완화책: 다중 근거 생성, 순서 균형(양방향 평균), 어려운 사례는 사람에게.
- 핵심 수치·결과: "Vicuna-13B could beat ChatGPT on 66 over 80 tested queries with ChatGPT as an evaluator" (순서 조작 시).
- 독자 전달 방식 제안: "평가자 위치 편향"을 한 문장으로 — 같은 두 답을 순서만 바꿔 두 번 물어보라. 답이 바뀌면 그 심판은 쓰면 안 된다.

### 논문 15: AI Agents That Matter
- 저자·연도: Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, Arvind Narayanan (2024)
- 발표처: TMLR (Transactions on Machine Learning Research) **[심사 통과]** (Semantic Scholar venue 기준)
- DOI/arXiv ID: arXiv:2407.01502
- 피인용수: 265
- 요약: 에이전트 벤치마크 관행의 네 결함 — 정확도만 보고 비용을 무시(불필요하게 복잡·고비용 SOTA), 모델 개발자와 응용 개발자의 벤치마킹 요구 혼동, 홀드아웃 셋 부재(지름길·과적합으로 취약한 에이전트), 평가 표준화 부재(재현성 결여). 정확도·비용 공동 최적화와 과적합 방지 프레임워크를 제안.
- 인용할 만한 문장:
  > "many agent benchmarks have inadequate holdout sets, and sometimes none at all. This has led to agents that are fragile because they take shortcuts and overfit to the benchmark in various ways." (초록)
- 독자 전달 방식 제안: 코스가 eval 인프라에 "API key with budget"을 명시하고 "매 변경 대신 정기 실행도 가능"이라 쓴 것은 비용 축을 인정한 것. 이 논문의 "비용도 메트릭"을 붙이면 소규모 팀 독자에게 현실적이다.

### 논문 16 (서베이): A Survey on LLM-as-a-Judge
- 저자·연도: Jiawei Gu, Xuhui Jiang, Zhichao Shi, Hexiang Tan 외 (2024; v6 2025-10-19)
- 발표처: arXiv **[프리프린트(미심사)]**
- DOI/arXiv ID: arXiv:2411.15594
- 피인용수: 1,955
- 요약: "신뢰할 수 있는 LLM 심판을 어떻게 만드는가"를 중심 질문으로 한 종합 서베이. 일관성 개선·편향 완화·시나리오 적응 전략과, 심판 신뢰성 자체를 평가하는 벤치마크를 제안.
- 독자 전달 방식 제안: 저술가가 LLM 심판 절(코스 Stage 4·5 접점)을 쓸 때 배경 지도로만 사용. 본문 인용은 논문 13·14의 구체 수치가 낫다.

---

## 3부. 명세·의도 기반 개발과 plan-then-execute (코스 Plan·Design·plan mode의 근거)

### 논문 17: ClarifyGPT: Empowering LLM-based Code Generation with Intention Clarification
- 저자·연도: Fangwen Mu, Lin Shi, Song Wang, Zhuohao Yu 외 (2023)
- 발표처: arXiv **[프리프린트(미심사)]** (이후 FSE 2024 게재로 알려졌으나 DOI 미확인 — "미확인")
- DOI/arXiv ID: arXiv:2310.10996
- 피인용수: 78
- 요약: 요구사항이 모호한지 "코드 일관성 검사"(같은 요구로 여러 번 생성해 서로 다르면 모호)로 탐지하고, 모호하면 표적 명확화 질문을 생성, 답을 받아 요구사항을 정제한 뒤 코드 생성. 10명 사용자 평가에서 GPT-4의 MBPP-sanitized Pass@1이 70.96%→80.80%. 시뮬레이션 사용자로 4개 벤치마크 평균 GPT-4 68.02%→75.75%, ChatGPT 58.55%→67.22%.
- 핵심 수치·결과 (초록 원문): "elevates the performance (Pass@1) of GPT-4 from 70.96% to 80.80% on MBPP-sanitized" / "improves the average performance of GPT-4 and ChatGPT across four benchmarks from 68.02% to 75.75% and from 58.55% to 67.22%".
- 독자 전달 방식 제안: 코스 plan mode 지침 "let it interview them"이 바로 이것이다. "모호함 탐지 = 같은 질문에 여러 답이 나오는지 보라"는 직관은 독자가 바로 써볼 수 있다.

### 논문 18: Clarity Is Not Assumed: Understanding LLM-Based Code Generation under Ambiguous Requirements (Orchid)
- 저자·연도: Di Yang, Xinou Xie, Xiuwen Yang, Ming Hu 외 (2026)
- 발표처: ASE 2026 (41st IEEE/ACM International Conference on Automated Software Engineering) **[심사 통과]**
- DOI/arXiv ID: arXiv:2604.21505; DOI 10.1145/3832783.3834403
- 피인용수: 5
- 요약: 모호한 요구사항을 전제로 설계한 첫 코드 생성 벤치마크 Orchid — 함수 수준 과제 1,304개, 네 가지 모호성 유형(어휘·구문·의미·막연함). 모호함은 모든 평가 LLM의 성능을 일관되게 떨어뜨리고, 가장 발전한 모델에서 부정적 효과가 가장 컸다. LLM은 같은 모호한 요구에 기능적으로 다른 구현을 자주 내고, 모호함을 스스로 식별·해소하지 못한다.
- 핵심 수치·결과: "1,304 function-level tasks covering four distinct types of ambiguity" / "ambiguity consistently degrades the performance of all evaluated LLMs, with the most pronounced negative effects observed in highly advanced models".
- 인용할 만한 문장:
  > "LLMs frequently produce functionally divergent implementations for the same ambiguous requirement and lack the capability to identify or resolve such ambiguity autonomously." (초록)
- 독자 전달 방식 제안: "더 좋은 모델일수록 모호한 명세에 더 크게 당한다"는 반직관적 결과 — intent.md·spec.md를 쓰는 이유를 한 줄로 정리해 준다.

### 논문 19: Can Code Language Models Learn Clarification-Seeking Behaviors? (ClarifyCoder)
- 저자·연도: Jie JW Wu, Manav Chaudhary, Davit Abrahamyan, Arhaan Khaku 외 (2025)
- 발표처: arXiv **[프리프린트(미심사)]**
- DOI/arXiv ID: arXiv:2504.16331
- 요약: 사람은 요구사항을 대화로 명확화하는 데 시간을 쓰지만 LLM은 모호해도 그냥 코드를 생성한다는 격차에서 출발. 명확화가 필요한 시나리오를 합성해 파인튜닝. 모호 과제에서 소통률 63%(절대 +40%p), 좋은 질문률 52%(+30%p), 코드 성능 유지.
- 핵심 수치·결과: "achieves a 63% communication rate (40% absolute increase) and a 52% good question rate (30% absolute increase) on ambiguous tasks".
- 독자 전달 방식 제안: 기본 모델은 "질문하기"보다 "바로 생성"으로 치우쳐 있다 — 코스가 plan mode를 "기본 시작점"으로 강제하는 구조적 이유.

### 논문 20: Specification-Driven Development Benchmark: Security Knowledge Transition
- 저자·연도: Oleg Grynets, Andrii Salyk, Vasyl Lyashkevych, Oleh Kaskun 외 (2026)
- 발표처: arXiv **[프리프린트(미심사)]** (2026-05-29)
- DOI/arXiv ID: arXiv:2606.00167
- 요약: 스펙 기반 생성의 보안 문제 — 기능 동작은 명시되지만 보안 동작은 암묵적·일반적이거나 사후 리뷰로 미뤄진다. 다층 명세 보안 모델과 보안 지식 전이 방법을 제안. 숨겨진 221개 블랙박스 API 테스트에서 modal failure가 기준선 50 → ASVS 조건 42 → 다층 모델 36으로 감소, 비즈니스 로직·관리자 안전 범주에서 개선이 가장 컸다.
- 핵심 수치·결과: "Evaluated against a hidden 221-test black-box API suite, modal failures decreased from 50 in the baseline to 42 with ASVS and 36 with the Multilayer Security Model".
- 독자 전달 방식 제안: 코스 spec.md 예제의 "concerns"(위험 목록)와 REVIEW.md의 Security pass가 왜 따로 있어야 하는지 — 스펙에 안 쓴 보안 요구는 생성되지 않는다.

### 논문 21: Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models
- 저자·연도: Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu 외 (2023)
- 발표처: ACL 2023 **[심사 통과]**
- DOI/arXiv ID: arXiv:2305.04091
- 피인용수: 896
- 요약: Zero-shot CoT("단계별로 생각하자")의 세 실패 — 계산 오류, 단계 누락, 의미 오해. 단계 누락을 줄이기 위해 "먼저 과제를 하위 과제로 나누는 계획을 세우고, 계획대로 수행"하는 Plan-and-Solve 프롬프팅 제안. 10개 데이터셋·3가지 추론 문제에서 GPT-3 기준 Zero-shot CoT를 일관되게 큰 폭으로 상회, 수학 추론에서 8-shot CoT와 비슷.
- 독자 전달 방식 제안: "계획을 먼저 쓰면 단계를 빼먹지 않는다"는 가장 단순한 형태의 plan mode 근거. 코스 plan.md 예제의 "Order of work" 섹션이 바로 이 역할.

### 논문 22: Plan-and-Act: Improving Planning of Agents for Long-Horizon Tasks
- 저자·연도: Lutfi Eren Erdogan, Nicholas Lee, Sehoon Kim, Suhong Moon 외 (2025)
- 발표처: ICML 2025 **[심사 통과]** (arXiv journal_ref "ICML 2025")
- DOI/arXiv ID: arXiv:2503.09572
- 피인용수: 232
- 요약: 장기 다단계 과제에서 고수준 계획(Planner)과 저수준 실행(Executor)을 분리하는 프레임워크. 계획 생성 품질을 높이기 위해 실제 궤적에 실행 가능한 계획을 주석해 합성 데이터 생성. WebArena-Lite 57.58%, WebVoyager(텍스트 전용) 81.36% 성공률.
- 핵심 수치·결과: "state-of-the-art 57.58% success rate on the WebArena-Lite benchmark as well as a text-only state-of-the-art 81.36% success rate on WebVoyager".
- 독자 전달 방식 제안: 코스 Stage 3 "서브에이전트"(researcher·verifier·simplifier)와 plan mode의 결합을 설명할 때 — Planner/Executor 분리는 연구에서도 반복 확인된 패턴. 단, 도메인이 웹 탐색이라는 점을 명시.

### 논문 23 (seminal): ReAct: Synergizing Reasoning and Acting in Language Models
- 저자·연도: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du 외 (2022; ICLR 2023)
- 발표처: ICLR 2023 **[심사 통과]**
- DOI/arXiv ID: arXiv:2210.03629
- 피인용수: 12,685
- 요약: 추론 흔적과 행동을 교차 생성 — 추론이 행동 계획을 세우고 갱신하며 예외를 다루고, 행동이 외부 환경에서 정보를 가져온다. ALFWorld·WebShop에서 모방/강화학습 대비 절대 성공률 +34%·+10%, 환각·오류 전파 감소, 해석 가능한 궤적.
- 독자 전달 방식 제안: Claude Code 같은 코딩 에이전트의 "읽고-생각하고-실행하고-다시 읽는" 루프의 학술적 원형. 한 문단 배경으로만.

---

## 3부-보. CLAUDE.md·skills의 실증 (코스 Build 단계)

### 논문 24: Decoding the Configuration of AI Coding Agents: Insights from Claude Code Projects
- 저자·연도: Helio Victor F. Santos, Vitor Costa, Joao Eduardo Montandon, Marco Tulio Valente (2025; 2026 게재)
- 발표처: AGENT 2026 (1st International Workshop on Agentic Engineering, ICSE 2026 co-located), pp. 63–67 **[심사 통과]**
- DOI/arXiv ID: arXiv:2511.09268; DOI 10.1145/3786167.3788412
- 피인용수: 24
- 요약: 공개 Claude Code 프로젝트의 설정 파일(CLAUDE.md) 328개를 수집·분석해 (i) 어떤 SE 관심사·관행을 명시하는지, (ii) 한 파일 안에서 어떤 관심사가 함께 나타나는지 조사. 다양한 관심사를 정의하는 것의 중요성과, 특히 "에이전트가 따라야 할 아키텍처"를 명시하는 경향을 확인.
- 핵심 수치·결과: "328 configuration files from public Claude Code projects".
- 독자 전달 방식 제안: 코스 CLAUDE.md play의 "무엇을 적을까"에 대한 실증 답 — 다른 팀들은 아키텍처 제약을 가장 많이 적는다.

### 논문 25: Harness Engineering for Agentic AI Coding Tools: An Exploratory Study
- 저자·연도: Matthias Galster, Seyedmoein Mohsenimofidi, Jai Lal Lulla, Muhammad Auwal Abubakar 외 (2026)
- 발표처: AIware 2026 **[심사 통과]** (원제 "Configuring Agentic AI Coding Tools: An Exploratory Study"; arXiv v5가 확장판)
- DOI/arXiv ID: arXiv:2602.14690 (ACM DOI 미확인)
- 피인용수: 11
- 요약: Claude Code·Copilot·Cursor·Gemini·Codex의 설정 메커니즘 8종(정적 컨텍스트~실행형·외부 통합)을 식별하고, GitHub 저장소 2,853개에서 채택 양상 분석. 컨텍스트 파일이 지배적이고 흔히 유일한 메커니즘이며 AGENTS.md가 도구 간 상호운용 표준으로 부상. Skills·Subagents 같은 고급 메커니즘 채택은 드물고, Skills는 대부분 실행 스크립트가 아닌 정적 지시. Claude Code 사용자가 가장 넓은 범위의 메커니즘을 쓴다.
- 핵심 수치·결과: "an empirical study of 2,853 GitHub repositories" / "few repositories adopt advanced mechanisms such as Skills and Subagents".
- 독자 전달 방식 제안: 코스가 skills·subagents를 play로 격상한 것과 대비 — 현장은 아직 CLAUDE.md 한 장이 대부분이다. 이 책의 독자가 "앞서 가는 소수"임을 숫자로 보여줄 수 있다.

---

## 4부. AI 생성 코드의 보안·품질과 코드 리뷰 자동화 (코스 Deploy 단계의 근거)

### 논문 26 (seminal): Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions
- 저자·연도: Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, Ramesh Karri (2021; S&P 2022)
- 발표처: IEEE Symposium on Security and Privacy 2022 **[심사 통과]** (확장판 Communications of the ACM 2025, DOI 10.1145/3610721)
- DOI/arXiv ID: arXiv:2108.09293
- 피인용수: 1,043
- 요약: MITRE Top-25 등 고위험 CWE에 해당하는 89개 시나리오로 Copilot을 프롬프트해 1,689개 프로그램 생성. 약 40%가 취약. 약점 다양성·프롬프트 다양성·도메인 다양성 세 축으로 분석.
- 핵심 수치·결과: "we produce 89 different scenarios for Copilot to complete, producing 1,689 programs. Of these, we found approximately 40% to be vulnerable." (2021년 Copilot 기준 — 신선도 주의)
- 독자 전달 방식 제안: "40%"는 2021년 모델 수치다. 반드시 논문 27(2023–25 실제 GitHub 코드)과 함께 써서 "줄었지만 사라지지 않았다"로.

### 논문 27: Security Weaknesses of Copilot-Generated Code in GitHub Projects: An Empirical Study
- 저자·연도: Yujia Fu, Peng Liang, Amjed Tahir, Zengyang Li 외 (2023; TOSEM 2025)
- 발표처: ACM Transactions on Software Engineering and Methodology **[심사 통과]**
- DOI/arXiv ID: arXiv:2310.02059 (v4 2025-02-06); DOI 10.1145/3716848
- 피인용수: 133
- 요약: 통제 환경이 아닌 실제 GitHub 프로젝트에서 Copilot·CodeWhisperer·Codeium이 생성한 스니펫 733개 분석. Python 29.5%, JavaScript 24.2%가 보안 약점 보유, 43개 CWE에 걸침(CWE-330·94·79 포함, 8개는 2023 CWE Top-25). 정적 분석 경고를 Copilot Chat에 주면 최대 55.5% 수정.
- 핵심 수치·결과: "733 snippets ... 29.5% of Python and 24.2% of JavaScript snippets affected" / "43 Common Weakness Enumeration (CWE) categories" / "up to 55.5% of the security issues can be fixed".
- 독자 전달 방식 제안: "경고를 넣어주면 절반은 고친다" — 코스 PR 리뷰 play의 "@claude가 리뷰 코멘트를 받아 고친다" 루프의 근거. 피드백만 있으면 고치는데, 피드백이 없으면 그대로 머지된다.

### 논문 28: Do Users Write More Insecure Code with AI Assistants?
- 저자·연도: Neil Perry, Megha Srivastava, Deepak Kumar, Dan Boneh (2023)
- 발표처: ACM CCS 2023, pp. 2785–2799 **[심사 통과]**
- DOI/arXiv ID: arXiv:2211.03622; DOI 10.1145/3576915.3623157
- 피인용수: 482
- 요약: codex-davinci-002 기반 어시스턴트로 보안 관련 과제를 푸는 대규모 사용자 연구. AI 접근 참가자가 유의하게 덜 안전한 코드를 썼고, 동시에 자기 코드가 안전하다고 더 믿었다. AI를 덜 신뢰하고 프롬프트를 더 다듬은 참가자가 취약점이 적었다.
- 인용할 만한 문장:
  > "participants with access to an AI assistant were more likely to believe they wrote secure code than those without access to the AI assistant." (초록)
- 독자 전달 방식 제안: 5부의 자동화 편향과 직접 연결 — 보안에서 "더 안전하다고 믿는데 덜 안전하다"는 패턴. 코스가 보안을 사람 리뷰가 아니라 REVIEW.md Security pass + hook으로 구조화하는 이유.

### 논문 29: Is GitHub's Copilot as Bad as Humans at Introducing Vulnerabilities in Code?
- 저자·연도: Owura Asare, Meiyappan Nagappan, N. Asokan (2022; EMSE 2023)
- 발표처: Empirical Software Engineering **[심사 통과]**
- DOI/arXiv ID: arXiv:2204.04741; DOI 10.1007/s10664-023-10380-1
- 피인용수: 188
- 요약: 사람이 실제로 취약점을 넣었던 C/C++ 시나리오로 Copilot을 프롬프트. 원래 취약 코드를 약 33% 재현, 수정된 코드를 25% 재현. 취약점 유형별로 다르고 오래된 취약점에 더 취약하지만, 전체적으로 "사람만큼 나쁘지는 않다"고 결론.
- 핵심 수치·결과: "Copilot replicates the original vulnerable code about 33% of the time while replicating the fixed code at a 25% rate".
- 독자 전달 방식 제안: 논문 26의 반대편 균형추. "AI 코드는 위험하다" 단정을 피하고 "사람 코드와 같은 종류의 검사가 필요하다"로 쓰게 해준다.

### 논문 30: Automated Code Review In Practice
- 저자·연도: Umut Cihan, Vahid Haratian, Arda İçöz, Mert Kaan Gül 외 (2024; ICSE-SEIP 2025)
- 발표처: ICSE 2025 SEIP Track **[심사 통과]** (arXiv comment 기준; ACM/IEEE DOI 미확인)
- DOI/arXiv ID: arXiv:2412.18531
- 요약: 산업 환경(약 238명, 10개 프로젝트)에 Qodo PR Agent 기반 LLM 리뷰 도입. 3개 프로젝트 PR 4,335개 중 1,568개가 자동 리뷰. 자동 코멘트의 73.8%가 해소됐지만 평균 PR 종료 시간이 5시간 52분에서 8시간 20분으로 늘었다. 버그 탐지·품질 인식·모범 사례 확산에 도움, 그러나 잘못된 리뷰·불필요한 수정·무관한 코멘트라는 단점.
- 핵심 수치·결과 (초록 원문): "4,335 pull requests, 1,568 of which underwent automated reviews" / "73.8% of automated comments were resolved" / "the average pull request closure duration increased from five hours 52 minutes to eight hours 20 minutes".
- 독자 전달 방식 제안: 코스가 REVIEW.md에 "Cap the nits: 최대 5개", "CI가 이미 강제하는 것은 보고하지 말라"를 넣은 이유를 이 수치가 설명한다. AI 리뷰는 공짜가 아니다 — 노이즈를 설계로 줄여야 한다.

### 논문 31: AI-Assisted Assessment of Coding Practices in Modern Code Review (Google AutoCommenter)
- 저자·연도: Manushree Vijayvergiya, Małgorzata Salawa, Ivan Budiselić, Dan Zheng, Pascal Lamblin, Marko Ivanković 외 (2024)
- 발표처: AIware '24 **[심사 통과]**
- DOI/arXiv ID: arXiv:2405.13565; DOI 10.1145/3664646.3665664
- 피인용수: 47
- 요약: LLM이 코딩 모범 사례를 학습·강제하는 AutoCommenter를 C++·Java·Python·Go용으로 구현해 Google 규모(수만 명 개발자)로 배포·평가. 종단 시스템이 실현 가능하고 개발자 워크플로에 긍정적 영향. 배포 과제와 교훈 포함.
- 독자 전달 방식 제안: "모범 사례를 문서에 적고 AI가 리뷰에서 강제한다" — 코스의 REVIEW.md + CLAUDE.md 피드백 루프("두 번째로 지적된 실수는 CLAUDE.md로 들어간다")가 대규모로 작동한 사례.

### 논문 32 (seminal, 리뷰 자동화 계열): Using Pre-Trained Models to Boost Code Review Automation
- 저자·연도: Rosalia Tufano, Simone Masiero, Antonio Mastropaolo, Luca Pascarella, Denys Poshyvanyk, Gabriele Bavota (2022)
- 발표처: ICSE 2022 **[심사 통과]**
- DOI/arXiv ID: arXiv:2201.06850; DOI 10.1145/3510003.3510621
- 피인용수: 255
- 요약: 리뷰 자동화 두 과제 — (a) 제출 코드에 리뷰어가 요구할 변경을 미리 적용, (b) 자연어 리뷰 코멘트를 받아 변경을 구현. 사전학습 T5가 이전 DL 모델을 능가, 더 현실적인 데이터셋에서 실험.
- 독자 전달 방식 제안: LLM 이전부터 "리뷰 코멘트 → 코드 변경 자동화"가 연구 주제였다는 배경 한 줄. 코스의 "@claude가 코멘트를 처리한다"가 갑자기 나온 아이디어가 아님을 보여준다.

### 논문 33: On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub
- 저자·연도: Miku Watanabe, Hao Li, Yutaro Kashiwa, Brittany Reid 외 (2025; TOSEM 게재)
- 발표처: ACM Transactions on Software Engineering and Methodology **[심사 통과]**
- DOI/arXiv ID: arXiv:2509.14745 (v3 2026-02-09); DOI 10.1145/3798166
- 피인용수: 105
- 요약: Claude Code로 생성된 PR 567개(157개 오픈소스 프로젝트) 분석. 개발자는 리팩터링·문서화·테스트에 에이전트를 많이 쓴다. 83.8%가 결국 머지됐고, 머지된 것의 54.9%는 추가 수정 없이 통합, 45.1%는 사람 수정이 필요(버그 수정·문서·프로젝트 고유 표준 준수에서 특히).
- 핵심 수치·결과: "567 GitHub pull requests (PRs) generated using Claude Code ... across 157 diverse open-source projects" / "83.8% of these agent-assisted PRs are eventually accepted and merged" / "54.9% of the merged PRs are integrated without further modification".
- 독자 전달 방식 제안: 코스 plan mode의 leading indicator "첫 구현 패스에서 머지되는 비율"의 현장 기준값으로 쓸 수 있다 — 54.9%. 그리고 "프로젝트 고유 표준 준수"가 사람 수정 사유라는 점은 CLAUDE.md·skills의 존재 이유.

### 논문 34: The Rise of AI Teammates in Software Engineering (SE) 3.0 (AIDev 데이터셋)
- 저자·연도: Hao Li, Haoxiang Zhang, Ahmed E. Hassan (2025)
- 발표처: arXiv **[프리프린트(미심사)]**
- DOI/arXiv ID: arXiv:2507.15003
- 요약: Codex·Devin·Copilot·Cursor·Claude Code 5개 에이전트의 PR 456,000+개(61,000개 저장소, 47,000명 개발자) 공개 데이터셋. 에이전트는 속도에서 사람을 앞서지만 PR 수락률은 더 낮다("신뢰·효용 격차"). 한 개발자가 3년 분량 PR을 3일에 제출한 사례, 그러나 구조적으로 더 단순한 변경.
- 핵심 수치·결과: "over 456,000 pull requests by five leading agents ... across 61,000 repositories and 47,000 developers" / "although agents often outperform humans in speed, their PRs are accepted less frequently".
- 독자 전달 방식 제안: 코스 도입부 "코드는 빨라졌는데 주변 프로세스가 못 따라간다"의 데이터 버전. 후속 분석(논문 35·36)의 모집단.

### 논문 35: Comparing AI Coding Agents: A Task-Stratified Analysis of Pull Request Acceptance
- 저자·연도: Giovanni Pinna, Jingzhi Gong, David Williams, Federica Sarro (2026)
- 발표처: MSR 2026 Mining Challenge **[심사 통과]**
- DOI/arXiv ID: arXiv:2602.08915; DOI 10.1145/3793302.3793576
- 요약: AIDev에서 PR 7,156개로 5개 에이전트를 과제 유형별로 비교. 과제 유형이 수락률의 지배 요인 — 문서화 82.1% vs 신기능 66.1%(16%p 격차, 에이전트 간 차이보다 큼). 어떤 에이전트도 모든 유형에서 최고가 아님: Claude Code는 문서화(92.3%)·기능(72.6%)에서 1위, Cursor는 수정(80.4%)에서 1위.
- 핵심 수치·결과: "documentation tasks achieve 82.1% acceptance compared to 66.1% for new features" / "Claude Code leads in documentation (92.3%) and features (72.6%), while Cursor excels in fix tasks (80.4%)".
- 독자 전달 방식 제안: "어떤 작업을 에이전트에게 주는가"가 도구 선택보다 중요하다. 코스 intent.md의 "blast radius 작은 일부터"와 맞물린다.

### 논문 36: Do These Violent Delights Have Violent Ends? Measuring the Post-Merge Fate of Agentic Code
- 저자·연도: Chunqiu Steven Xia, Courtney Miller (2026)
- 발표처: arXiv **[프리프린트(미심사)]** (2026-07-10)
- DOI/arXiv ID: arXiv:2607.09902
- 요약: 182개 저장소에서 에이전트 기여와 사람 기여의 머지 이후 운명을 종단 추적. 전체 유지보수율은 비슷하지만 에이전트 기여는 교정 유지보수(corrective maintenance) 비율이 유의하게 높고 보안 약점·의존성 취약점을 더 많이 들여온다. 프로젝트의 "무리뷰 비율"이 10%p 오를 때마다 에이전트 유지보수 부담이 평균 약 6% 증가.
- 핵심 수치·결과: "each 10 percentage-point increase in a project's no-review rate is associated with roughly a 6% increase in agentic maintenance burden on average".
- 인용할 만한 문장:
  > "our findings highlight the need to evaluate and design agentic tools not only to produce mergeable changes, but to produce contributions that remain secure and maintainable." (초록)
- 독자 전달 방식 제안: 코스 PR 리뷰 play의 lagging indicator("머지 전 잡은 결함 vs 프로덕션으로 빠져나간 결함")가 왜 필요한지의 직접 증거. "리뷰를 건너뛰면 나중에 6%씩 갚는다."

### 논문 37: Augmentation with Dilution: A Large-Scale Empirical Study of Human Contributor Ecosystems After AI Coding Agent Adoption
- 저자·연도: Weixing Zhang, Bowen Jiang, Anne Koziolek (2026)
- 발표처: arXiv **[프리프린트(미심사)]** (2026-06-24)
- DOI/arXiv ID: arXiv:2606.26289
- 요약: 2023-01~2026-05 GitHub 저장소 11,097개, 시차 이중차분(Sun & Abraham 추정량)으로 에이전트 도입이 사람 기여자 생태계에 미친 인과 효과. 사람 기여자 절대 수는 변하지 않지만(ATT 0.014, p=0.224) 사람 비중은 감소(ATT −0.019, p=0.002), 신규 기여자 참여 비중 −3.7%p(p<0.001), 리뷰 깊이 +5.3%(ATT +0.0168, p<0.001) — 부담이 생산에서 리뷰 단계로 이동.
- 핵심 수치·결과: "Review depth increases significantly by 5.3% (ATT = +0.0168, p < 0.001), indicating that AI agents shift burden from the code production stage to the review stage."
- 독자 전달 방식 제안: 코스 전체의 주제문 — "병목이 코드 작성에서 리뷰로 옮겨간다" — 를 인과 추정으로 뒷받침하는 가장 직접적인 자료. 신규 기여자 감소는 5부(기술 형성)와도 연결.

---

## 5부. 인간-AI 협업: 자동화 안주·자동화 편향·기술 퇴화·리뷰 피로 (코스 governance·hooks 승인 게이트의 근거)

### 논문 38 (seminal): Ironies of Automation
- 저자·연도: Lisanne Bainbridge (1983)
- 발표처: *Automatica* 19(6), pp. 775–779 **[심사 통과]**
- DOI/arXiv ID: DOI 10.1016/0005-1098(83)90046-8
- 피인용수: 2,668 (Crossref 참조 1,692)
- 요약: 자동화의 역설 — 설계자가 "불안정한" 사람을 제거하려 하지만, 사람에게는 자동화하지 못한 과제가 남고, 그 과제는 가장 어려운 상황(자동화 실패 시)에서 수동 개입을 요구하며, 그때 사람은 수동 기술을 잃어 있고 상황 인식도 떨어진 상태다. 초록은 미확보(원문 PDF로 인용문 확인).
- 인용할 만한 문장 (원문 서론, 웹 공개 PDF로 대조):
  > "the designer who tries to eliminate the operator still leaves the operator to do the tasks which the designer cannot think how to automate." (p. 775, Introduction)
- 독자 전달 방식 제안: 코스의 "Humans remain accountable for every decision that requires judgment"를 1983년 문장으로 되받는다. 자동화가 많아질수록 남는 사람 과제는 더 어렵다 — 그래서 승인 게이트는 "쉬운 일"이 아니다.

### 논문 39 (seminal): Humans and Automation: Use, Misuse, Disuse, Abuse
- 저자·연도: Raja Parasuraman, Victor Riley (1997)
- 발표처: *Human Factors* 39(2), pp. 230–253 **[심사 통과]**
- DOI/arXiv ID: DOI 10.1518/001872097778543886
- 피인용수: 4,773
- 요약: 자동화에 대한 인간 반응을 네 범주로 — 사용(use), 오용(misuse: 과신·안주로 과도 의존), 불사용(disuse: 잦은 오경보로 무시), 남용(abuse: 인간 성능 고려 없는 설계자의 자동화). 초록 미확보(원문 미대조) — 분류 틀만 인용 권장.
- 독자 전달 방식 제안: 코스 hooks play의 "deny 목록이 prompt fatigue가 되지 않게 allow로 안전한 내부 루프를 사전 승인하라"는 지침은 정확히 "불사용(disuse)" 방지다. 오경보가 많으면 사람은 게이트를 무시한다.

### 논문 40: Complacency and Bias in Human Use of Automation: An Attentional Integration
- 저자·연도: Raja Parasuraman, Dietrich H. Manzey (2010)
- 발표처: *Human Factors* 52(3), pp. 381–410 **[심사 통과]** (PMID 21077562)
- DOI/arXiv ID: DOI 10.1177/0018720810376055
- 피인용수: 1,586
- 요약: 자동화 안주(complacency)와 자동화 편향(automation bias) 실증 연구를 종합한 리뷰. 안주는 다중 과제 부하에서 수동 과제가 자동화 과제와 주의를 경쟁할 때 발생, 초보와 전문가 모두에서 나타나며 단순 연습으로 극복되지 않는다. 자동화 편향은 결정 보조가 불완전할 때 누락 오류와 실행 오류를 모두 낳고, 초보·전문가 모두에서 발생하며 훈련이나 지시로 예방되지 않고, 개인뿐 아니라 팀의 의사결정에도 영향. 둘은 주의(attention)가 중심인 겹치는 현상.
- 인용할 만한 문장 (PubMed 초록 원문):
  > "Automation complacency is found in both naive and expert participants and cannot be overcome with simple practice."
  > "Automation bias occurs in both naive and expert participants, cannot be prevented by training or instructions, and can affect decision making in individuals as well as in teams."
- 독자 전달 방식 제안: 이 책의 governance 장에서 가장 강한 한 문장 — "훈련이나 지시로 예방되지 않는다". 그러므로 "조심해서 리뷰하세요"는 대책이 아니고, hooks(구조)와 테스트 파일 편집 차단(구조)이 대책이다. 논문 28(AI 사용자가 더 안전하다고 믿음)·논문 2(체감 vs 실측)와 삼각 편대.

### 논문 41: The Impact of Generative AI on Critical Thinking: Self-Reported Reductions in Cognitive Effort and Confidence Effects From a Survey of Knowledge Workers
- 저자·연도: Hao-Ping (Hank) Lee, Advait Sarkar, Lev Tankelevitch, Ian Drosos, Sean Rintel, Richard Banks 외 (Microsoft Research, 2025)
- 발표처: CHI 2025, pp. 1–22 **[심사 통과]**
- DOI/arXiv ID: DOI 10.1145/3706598.3713778
- 피인용수: 718
- 요약: 지식 노동자 319명 설문, 생성 AI 사용 사례 936건. 과제별 자기 확신과 AI에 대한 확신이 비판적 사고의 발동 여부와 노력을 예측 — AI 확신이 높을수록 비판적 사고가 줄고, 자기 확신이 높을수록 늘었다. 질적으로 비판적 사고의 성격이 "정보 검증·응답 통합·과제 관리(stewardship)"로 이동.
- 핵심 수치·결과: "We survey 319 knowledge workers ... Participants shared 936 first-hand examples" / "higher confidence in GenAI is associated with less critical thinking, while higher self-confidence is associated with more critical thinking".
- 독자 전달 방식 제안: 코스가 사람 리뷰를 "의도와 위험 판단"으로 올리라고 하는 것은 이 논문의 "task stewardship"과 같은 방향. 단, 자기 보고 설문이라는 한계를 명시.

### 논문 42: How AI Impacts Skill Formation (Anthropic)
- 저자·연도: Judy Hanwen Shen, Alex Tamkin (2026)
- 발표처: arXiv **[프리프린트(미심사)]**; Anthropic 연구 블로그 2026-01-29
- DOI/arXiv ID: arXiv:2601.20245 (v2 2026-02-01)
- 피인용수: 42
- 요약: 개발자가 새 비동기 프로그래밍 라이브러리를 AI 있이/없이 익히는 무작위 실험. AI 사용은 개념 이해·코드 읽기·디버깅 능력을 손상시켰고, 평균적으로 유의한 효율 이득은 없었다. 코딩을 완전히 위임한 참가자는 약간의 생산성 향상을 봤지만 라이브러리를 배우지 못했다. 6가지 상호작용 패턴 중 3가지(인지적 관여형)는 AI 도움을 받아도 학습을 보존.
- 핵심 수치·결과: 초록은 수치를 적지 않음. (참가자 51~52명, 이해도 점수 격차 약 17%p 등은 2차 보도 — 원문 미대조, 본문 사용 시 본문 PDF 확인 필요.)
- 인용할 만한 문장:
  > "AI-enhanced productivity is not a shortcut to competence and AI assistance should be carefully adopted into workflows to preserve skill formation -- particularly in safety-critical domains." (초록)
- 독자 전달 방식 제안: Bainbridge(1983)의 "수동 기술 상실" 역설의 2026년 코딩 버전. 코스가 plan mode에서 "계획을 interrogate하라"(관여형 패턴)고 하는 것이 학습 보존 패턴과 겹친다는 점을 짚으면 좋다.

### 논문 43 (seminal, 코드 리뷰): Expectations, Outcomes, and Challenges of Modern Code Review
- 저자·연도: Alberto Bacchelli, Christian Bird (2013)
- 발표처: ICSE 2013, pp. 712–721 **[심사 통과]**
- DOI/arXiv ID: DOI 10.1109/ICSE.2013.6606617
- 피인용수: 913
- 요약: Microsoft의 현대적 코드 리뷰(도구 기반·경량)에 대한 기대와 실제 결과를 조사. 리뷰의 명시 목표는 결함 발견이지만 실제 결과는 지식 전달·팀 인식·대안 해법 논의가 중심이고, 결함 발견은 기대보다 적다는 것이 주 결론으로 알려짐. 초록 미확보(원문 미대조) — 수치 없이 결론 방향만 인용.
- 독자 전달 방식 제안: 코스가 사람 리뷰를 "의도·위험"으로 재배치하는 것은 사람 리뷰가 원래 잘하던 것(이해·공유)을 남기고 못하던 것(기계적 결함 찾기)을 AI에 넘기는 것이라고 설명할 수 있다.

### 논문 44: Convergent Contemporary Software Peer Review Practices
- 저자·연도: Peter C. Rigby, Christian Bird (2013)
- 발표처: ESEC/FSE 2013, pp. 202–212 **[심사 통과]**
- DOI/arXiv ID: DOI 10.1145/2491411.2491444
- 피인용수: 383
- 요약: 오픈소스·Microsoft·Google 등 여러 프로젝트의 리뷰 관행이 "작은 변경·소수 리뷰어·빠른 회전"으로 수렴한다는 것을 보임. 초록 미확보(원문 미대조) — 구체 수치(변경 크기 LOC 등)는 본문 확인 전 인용 금지.
- 독자 전달 방식 제안: 에이전트 PR이 "구조적으로 단순"(논문 34)하고 "작은 blast radius"(코스)를 권하는 것은 이 수렴 관행과 일치한다 — 리뷰 가능한 크기를 지켜라.

---

## 6부. 소프트웨어 측정: DORA·SPACE·DevEx·Goodhart·관리도 (코스 Maintain 단계의 근거)

### 자료 45: Accelerate: The Science of Lean Software and DevOps (DORA의 대중판)
- 저자·연도: Nicole Forsgren, Jez Humble, Gene Kim (2018)
- 발표처: IT Revolution Press, 2018-03-27, 288쪽 **[단행본 — 논문 아님]**. ISBN 978-1-942788-33-1 (서점 서지 다수 일치)
- 요약: 다년 State of DevOps 설문 연구를 바탕으로 소프트웨어 전달 성과를 네 지표(lead time, deployment frequency, mean time to restore, change fail percentage)로 측정하고, 이를 조직 성과와 연결. 24개 역량 제시.
- 학술 원출처(동일 저자):
  - Forsgren & Humble (2015), "The Role of Continuous Delivery in IT and Organizational Performance", SSRN, DOI 10.2139/ssrn.2681909 **[워킹페이퍼]**
  - Forsgren & Humble (2015), "DevOps: Profiles in ITSM Performance and Contributing Factors", SSRN, DOI 10.2139/ssrn.2681906 **[워킹페이퍼]**
- 주의: "다섯 번째 지표(rework rate)"는 DORA 2024 보고서(비학술)에서 추가된 것으로 2차 자료(Thoughtworks Radar)로만 확인 — 본문에 쓰려면 DORA 보고서 원문 확인 필요.
- 독자 전달 방식 제안: 코스 CI/CD play의 lagging indicator가 "DORA measures"다. 네 지표가 설문 기반 상관 연구에서 왔다는 점(인과가 아님)을 한 줄 덧붙이면 정직하다.

### 논문 46: The SPACE of Developer Productivity: There's More to It Than You Think
- 저자·연도: Nicole Forsgren, Margaret-Anne Storey, Chandra Maddila, Thomas Zimmermann, Brian Houck, Jenna Butler (2021)
- 발표처: *Communications of the ACM* 64(6) **[심사 통과]** (ACM Queue 19(1) 2021 선행 게재)
- DOI/arXiv ID: DOI 10.1145/3453928
- 피인용수: 160
- 요약: 개발자 생산성은 단일 지표로 잡히지 않는다 — Satisfaction & well-being, Performance, Activity, Communication & collaboration, Efficiency & flow 다섯 차원. 활동량(커밋·PR 수)만으로 측정하는 것의 위험을 경고하고, 차원을 섞어 최소 3개 이상 지표를 쓰라고 권고(권고 수치는 본문 기준 — 초록 미확보).
- 독자 전달 방식 제안: 코스가 매 play마다 leading + lagging 두 지표를 짝 짓는 구조가 SPACE의 "한 차원만 보지 말라"와 통한다. 에이전트 시대의 함정: Activity(PR 수)는 폭증하는데(논문 34) Performance는 아닐 수 있다.

### 논문 47: DevEx: What Actually Drives Productivity
- 저자·연도: Abi Noda, Margaret-Anne Storey, Nicole Forsgren, Michaela Greiler (2023)
- 발표처: *ACM Queue* 21(2), pp. 35–53 **[심사 통과]**; CACM 66(11) 재게재 DOI 10.1145/3610285
- DOI/arXiv ID: DOI 10.1145/3595878
- 피인용수: 31
- 요약: 개발자 경험(DevEx)을 세 핵심 차원 — 피드백 루프, 인지 부하, 몰입 상태 — 로 정리하고, 개발자 피드백과 시스템 데이터를 결합한 측정 프레임워크를 제시.
- 인용할 만한 문장:
  > "presents a measurement framework that combines feedback from developers with data about the engineering systems they interact with." (초록)
- 독자 전달 방식 제안: 코스 Stage 4 "Give Claude a feedback loop"는 사람의 DevEx 원리(짧은 피드백 루프)를 에이전트에 적용한 것이라고 연결할 수 있다.

### 논문 48: Categorizing Variants of Goodhart's Law
- 저자·연도: David Manheim, Scott Garrabrant (2018)
- 발표처: arXiv **[프리프린트(미심사)]**
- DOI/arXiv ID: arXiv:1803.04585 (v4 2019-02-24)
- 피인용수: 241
- 요약: 대리 지표 과최적화의 실패 모드를 네 가지로 분류 — Regressional(지표와 목표의 상관이 극단값에서 깨짐), Extremal(분포 밖에서 관계가 바뀜), Causal(지표를 건드려도 목표가 안 움직임), Adversarial(행위자가 지표를 게임). 최적화 압력이 커질수록 Goodhart 효과가 커지므로 AI가 특히 위험.
- 인용할 만한 문장:
  > "The importance of Goodhart effects depends on the amount of power directed towards optimizing the proxy, and so the increased optimization power offered by artificial intelligence makes it especially critical for that field." (초록)
- Goodhart 원출처: C. A. E. Goodhart (1984), "Problems of Monetary Management: The UK Experience", in *Monetary Theory and Practice*, pp. 91–121, DOI 10.1007/978-1-349-17295-5_4 (1975년 강연의 재수록). 흔히 인용되는 "When a measure becomes a target, it ceases to be a good measure"는 Goodhart 본인이 아니라 Marilyn Strathern (1997), "'Improving ratings': audit in the British University system", *European Review* 5(3), pp. 305–321, DOI 10.1002/(SICI)1234-981X(199707)5:3<305::AID-EURO184>3.0.CO;2-4 의 문장.
- 독자 전달 방식 제안: 에이전트에게 "테스트 통과율"을 목표로 주면 테스트를 약화시킨다(Adversarial Goodhart) — 코스가 테스트 파일 편집을 hook으로 막는 이유를 네 변종 중 하나로 정확히 이름 붙여 준다. 인용문 출처 오귀속(Goodhart vs Strathern)은 책에서 바로잡을 가치가 있다.

### 자료 49: Western Electric Statistical Quality Control Handbook (1956) 및 Shewhart 관리도
- 저자·연도: Western Electric Company (1956) **[기업 핸드북 — 논문 아님, DOI 없음]**
- 학술 원출처: Walter A. Shewhart (1930), "Economic Quality Control of Manufactured Product", *Bell System Technical Journal* 9(2), pp. 364–389, DOI 10.1002/j.1538-7305.1930.tb00373.x **[심사 통과]**; 단행본 *Economic Control of Quality of Manufactured Product* (1931)
- 요약: 코스 Stage 6가 인용하는 "Western Electric rules"(1σ 위 5개 중 4개, 평균 위 8연속 등)는 1956년 핸드북의 런 규칙. 그 기반인 3σ 관리 한계는 Shewhart가 1920~30년대 벨 연구소에서 세운 것. 코스가 쓰는 1σ/2σ/3σ 초과 확률(1/6, 1/44, 1/740)은 정규분포 단측 꼬리 확률의 근삿값으로 수학적으로 맞다.
- 독자 전달 방식 제안: "1956년 품질 핸드북"이라는 코스 표현을 그대로 쓰되, 핸드북 자체는 DOI가 없음을 참고문헌에서 정직하게 표기. 통계적 공정 관리(SPC)가 70년 된 도구라는 점은 "메트릭 루프"가 새 발명이 아니라 소프트웨어로 옮겨 온 것임을 보여준다.

---

## 수집 한계·저술가 주의사항

1. **초록만으로 수치를 옮긴 항목이 대부분**이다. 본문 특정 쪽수를 요구하는 인용(p.N)은 저술 단계에서 PDF를 열어 확인해야 한다. 초록에 없는 숫자(Peng 95명, Anthropic 52명, SWE-bench Verified 68.3% 제외율, Rigby & Bird LOC 등)는 "원문 미대조"로 표시했으니 그대로 쓰지 말 것.
2. **초록을 확보하지 못한 고전 5편**(Bainbridge, Parasuraman & Riley, Bacchelli & Bird, Rigby & Bird, SPACE)은 서지(DOI·권호·쪽)만 검증됐다. 요약은 널리 알려진 결론을 적은 것이며 구체 수치는 넣지 않았다.
3. **2026년 자료 비중이 높다**(논문 11, 18, 25, 35, 36, 37, 42 등). 이 중 36·37·42는 프리프린트다. fact-checker는 저술 시점에 게재 여부를 재확인하고, 프리프린트는 본문에 "미심사"임을 표기할 것.
4. **"2026년 에이전틱 도구 기업 RCT"는 찾지 못했다.** 2026년의 인과 연구는 관찰 데이터(이중차분, 논문 37) 또는 학습 효과(논문 42) 중심이다. METR(2025)이 여전히 agentic 도구에 가장 가까운 RCT다.
5. 벤치마크 점수(SWE-bench 1.96%, Terminal-Bench <65% 등)는 발표 시점 값이다. 본문에서는 "{연도} 기준"을 반드시 붙일 것.
6. Semantic Scholar 피인용수는 조회일(2026-10-19) 기준이며 수 주 안에 바뀐다. 본문 인용 금지, 비중 판단용.
