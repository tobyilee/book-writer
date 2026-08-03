# AI Agentic Coding 학술·기술 리포트 — 검색 2026-08-02 기준

- **책 맥락:** 『OpenAI Codex 사용법 완전 정리』(tech-book, 슬러그 `codex-guide`). 대상 독자는 Claude Code로 agentic coding을 경험해본 개발자.
- **논문의 역할:** 보조 소스. 사용법 실무서에 "근거 있는 한 줄"을 대는 것이 목적이며, 이론 전개가 목적이 아니다.
- **수집 규모:** 22건 (arXiv 논문 21편 + OpenAI 공식 시스템 카드 1건).
- **검증 방식:** 모든 항목을 arXiv abstract 페이지(또는 원문 PDF)에서 직접 확인했다. 검색 결과 요약만 보고 기록한 항목은 없다. 시스템 카드는 PDF를 내려받아 본문 텍스트를 직접 읽었다.
- **표기 규약:**
  - `📄 preprint` = arXiv only, peer-review 확인 안 됨 / `✅ peer-reviewed` = 학회·저널 게재 확인
  - `⏳ 낡음` = 2025년 이전에 측정된 벤치마크 점수. 현재 모델 성능의 근거로 쓰면 안 되고, "그때는 이랬다"는 역사 서술로만 써야 한다.

---

## 1. 코딩 에이전트 벤치마크 (측정하는 것 / 측정 못 하는 것)

이 절이 이 리서치의 중심이다. 책에서 벤치마크 숫자를 쓸 일이 생기면, **숫자보다 이 절의 비판 논문들이 더 유용하다.** "Codex가 SWE-bench에서 몇 점"이라는 문장은 반년이면 낡지만, "벤치마크가 무엇을 못 재는가"는 오래 간다.

### 1-1. SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
- **저자·연도:** Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan (2023)
- **발표처:** ICLR 2024 — ✅ peer-reviewed
- **arXiv:** [2310.06770](https://arxiv.org/abs/2310.06770) (v1 2023-10-10, v3 2024-11-11)
- **요약:** 12개 인기 Python 저장소의 실제 GitHub 이슈·PR에서 추출한 2,294개 과제로 구성된다. 모델은 코드베이스와 이슈 설명을 받아 코드를 고쳐야 한다. 이 분야의 seminal 벤치마크로, 이후 거의 모든 코딩 에이전트가 이 축으로 비교된다.
- **핵심 수치:** 최고 성능 모델이었던 **Claude 2가 이슈의 1.96%만 해결** (SWE-bench 전체 세트, 2023년 논문 발표 시점 측정) — ⏳ 낡음
- **인용할 만한 문장:**
  > "understanding and coordinating changes across multiple functions, classes, and even files simultaneously" — 벤치마크가 요구하는 능력 규정 (abstract)
- **독자 전달 방식 제안:** "2023년 최고 모델이 2%를 풀었다"는 숫자는 **오늘 Codex가 얼마나 왔는지가 아니라, 이 분야의 시간 척도가 얼마나 짧은지**를 보여주는 데 써라. 책의 서문·1장 도입부용.

### 1-2. SWE-Bench+: Enhanced Coding Benchmark for LLMs ★ 벤치마크 비판 핵심
- **저자·연도:** Reem Aleithan, Haoran Xue, Mohammad Mahdi Mohajer, Elijah Nnorom, Gias Uddin, Song Wang (2024)
- **발표처:** arXiv cs.SE — 📄 preprint
- **arXiv:** [2410.06992](https://arxiv.org/abs/2410.06992) (2024-10-09)
- **요약:** SWE-bench에서 SWE-Agent + GPT-4가 "성공"한 패치를 사람이 직접 열어봤다. 그 결과 상당수가 실력이 아니라 데이터 문제로 통과한 것이었다. 이슈 본문이나 코멘트에 정답 코드가 그대로 적혀 있거나(solution leakage), 테스트가 너무 약해서 아무거나 통과하는 경우다.
- **핵심 수치 (SWE-bench 원본 세트, SWE-Agent+GPT-4 대상, 2024년 측정):**
  - 성공 패치의 **32.67%가 이슈 리포트·코멘트에 해답이 직접 제시된 경우**
  - 성공 패치의 **31.08%가 약한 테스트로 통과한 의심 패치**
  - 문제 인스턴스를 걸러내자 해결률이 **12.47% → 3.97%로 하락**
  - 이슈의 **94% 이상이 LLM 지식 컷오프 이전 생성** → 데이터 누출 가능성
  - 저자들은 이 문제가 **SWE-bench Lite와 SWE-bench Verified에도 남아 있다**고 명시
- **인용할 만한 문장:**
  > "32.67% of the successful patches involve cheating as the solutions were directly provided in the issue report or the comments" (abstract)
- **독자 전달 방식 제안:** 책에서 "리더보드 점수를 보고 도구를 고르지 마라"를 말할 때의 최강 근거. 비유: **답이 적힌 시험지로 본 모의고사 성적.**

### 1-3. Does SWE-Bench-Verified Test Agent Ability or Model Memory? ★ 오염 근거
- **저자·연도:** Thanosan Prathifkumar, Noble Saji Mathews, Meiyappan Nagappan (2025)
- **발표처:** arXiv cs.SE — 📄 preprint
- **arXiv:** [2512.10218](https://arxiv.org/abs/2512.10218) (v1 2025-12-11, v2 2025-12-22)
- **요약:** SWE-bench Verified(500개 이슈)가 에이전트 능력을 재는지, 학습 데이터 암기를 재는지 물었다. Claude 계열 모델에게 **"어떤 파일을 고쳐야 하는가"라는 파일 지목(localization) 과제**만 세 개 벤치마크에 걸쳐 시켰다. 프로젝트에 대한 추가 컨텍스트 없이도 SWE-bench Verified에서만 성능이 튀었다.
- **핵심 수치 (Claude 계열, 파일 지목 과제, 2025년 12월 발표):**
  - SWE-bench Verified에서 **다른 벤치마크 대비 3배 높은 성능**
  - **수정된 파일을 찾아내는 능력은 6배** — 프로젝트에 대한 추가 컨텍스트 없이
- **인용할 만한 문장:**
  > "scores on this benchmark may not reflect an agent's ability to handle real software issues" (abstract)
- **독자 전달 방식 제안:** 1-2와 짝. 1-2가 "문제지가 새고 있다"면 이건 "모델이 이미 답을 외웠다". 독자에게 던질 질문: **"당신 회사 코드베이스는 SWE-bench에 없다."**

### 1-4. Establishing Best Practices for Building Rigorous Agentic Benchmarks ★ 방법론 비판
- **저자·연도:** Yuxuan Zhu, Tengjun Jin, Yada Pruksachatkun, ... Matei Zaharia, Ion Stoica, Percy Liang, Daniel Kang 외 다수 (2025)
- **발표처:** arXiv cs.AI — 📄 preprint (2025-08-07 개정)
- **arXiv:** [2507.02825](https://arxiv.org/abs/2507.02825) (2025-07-03)
- **요약:** 에이전트 벤치마크 다수가 과제 설계나 보상 설계에 결함이 있음을 보이고, 점검 체크리스트(Agentic Benchmark Checklist, ABC)를 제안했다. SWE-bench Verified는 테스트 케이스가 불충분하고, TAU-bench는 빈 응답을 성공으로 센다고 구체적으로 지목했다.
- **핵심 수치:**
  - 이런 결함이 에이전트 성능을 **상대값 기준 최대 100%까지 과소·과대평가**하게 만듦
  - CVE-Bench에 ABC를 적용하자 **성능 과대평가가 33% 감소**
- **인용할 만한 문장 (전문 verbatim):**
  > "we show that many agentic benchmarks have issues in task setup or reward design. For example, SWE-bench Verified uses insufficient test cases, while TAU-bench counts empty responses as successful. Such issues can lead to under- or overestimation of agents' performance by up to 100% in relative terms." (abstract)
- **독자 전달 방식 제안:** "빈 응답을 성공으로 센다"는 구체 사례가 강력하다. 벤치마크 회의론을 추상적 잔소리가 아니라 **검증 가능한 버그 리포트**로 만들어 준다.

### 1-5. SWE-Lancer: Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering?
- **저자·연도:** Samuel Miserendino, Michele Wang, Tejal Patwardhan, Johannes Heidecke (OpenAI, 2025)
- **발표처:** arXiv cs.LG/cs.SE — 📄 preprint (OpenReview에 제출 기록 있음, 게재 확정 미확인)
- **arXiv:** [2502.12115](https://arxiv.org/abs/2502.12115) (v1 2025-02-17, v4 2025-05-29)
- **요약:** Upwork의 실제 프리랜스 과제 1,400여 건, 총 100만 달러 규모를 벤치마크로 만들었다. 단순 버그 수정($50)부터 기능 구현($32,000)까지 걸쳐 있고, **엔지니어링 과제뿐 아니라 "관리자 과제"** — 여러 기술 제안 중 무엇을 고를지 — 도 포함한다는 점이 특이하다. 엔드투엔드 테스트는 경험 있는 엔지니어가 3중 검증했다.
- **핵심 수치:** "frontier models are still unable to solve the majority of tasks" (2025-02 발표 시점). ※ 개별 모델 pass rate(GPT-4o 8.0%, Claude 3.5 Sonnet 26.2% 등)가 2차 소스에서 인용되나 **abstract에서 직접 확인하지 못했다** — 책에 쓰려면 논문 본문 표로 재확인 필요. ⏳ 어느 쪽이든 낡은 모델 세대다.
- **재현성:** 통합 Docker 이미지와 공개 평가 분할 **SWE-Lancer Diamond** 오픈소스 공개
- **독자 전달 방식 제안:** **"관리자 과제"라는 축**이 이 책에 특히 좋다. Codex를 쓸 때 개발자에게 남는 일이 "코드 타이핑"이 아니라 "제안 중 고르기"라는 서술의 학술적 뒷받침.

### 1-6. SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?
- **저자·연도:** Xiang Deng, Jeff Da, Edwin Pan 외 (Scale AI, 2025)
- **발표처:** arXiv cs.SE/cs.CL — 📄 preprint
- **arXiv:** [2509.16941](https://arxiv.org/abs/2509.16941) (v1 2025-09-21, v2 2025-11-14)
- **요약:** 41개 저장소에서 뽑은 1,865개 문제. 전문 개발자가 **몇 시간~며칠** 걸리는 장기 과제 위주로, 여러 파일에 걸친 패치가 필요하다. 공개(11개 저장소)·비공개 홀드아웃(12개)·상업(스타트업 제휴 사유 저장소 18개) 세 갈래로 나눠 **오염 저항성**을 설계했다.
- **핵심 수치 (2025-09 논문 발표 시점, Pass@1):**
  - 공개 세트(N=731): **GPT-5 23.3%, Claude Opus 4.1 22.7%, Claude Sonnet 4 17.6%, Gemini 2.5 Pro Preview 13.5%**
  - 상업 세트(N=276): **Claude Opus 4.1 17.8%, GPT-5 14.9%, Gemini 2.5 Pro Preview 10.1%, Claude Sonnet 4 9.1%**
  - 저자 결론: 프런티어 모델도 **Pass@1 25% 미만**
- **인용할 만한 문장:**
  > "a contamination-resistant testbed that more faithfully captures the complexity and diversity of real-world software development" (abstract)
- **독자 전달 방식 제안:** SWE-bench Verified 고득점과 이 20%대를 **나란히** 놓는 것이 이 책에서 가장 효과적인 대비다. 같은 모델, 다른 문제지, 세 배 차이. 사내 저장소가 어느 쪽에 가까운지 독자가 스스로 답하게 하라. **공개 세트보다 상업 세트에서 점수가 더 떨어진다**는 사실이 특히 실무적이다.

### 1-7. Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces ★ CLI 에이전트 직결
- **저자·연도:** Mike A. Merrill, Alexander G. Shaw, Nicholas Carlini, ... Andy Konwinski, Ludwig Schmidt 외 다수 (Stanford + Laude Institute, 2026)
- **발표처:** **ICLR 2026** — ✅ peer-reviewed ([OpenReview PDF](https://openreview.net/pdf/417ac3236de7dbf3fc3414c51754dd239271663e.pdf))
- **arXiv:** [2601.11868](https://arxiv.org/abs/2601.11868) (2026-01-17)
- **요약:** 실제 워크플로에서 뽑은 **89개 터미널 과제**. 각 과제는 고유한 컨테이너 환경 + 사람이 작성한 정답 풀이 + 검증 테스트를 갖는다. 코드 조각 생성이 아니라 컴파일·모델 학습·시스템 설정·환경 디버깅 같은 **엔드투엔드 워크플로**를 요구한다. **Claude Code, Codex CLI, OpenHands, Mini-SWE-Agent를 공식 지원**한다.
- **핵심 수치:** "frontier models and agents score less than 65% on the benchmark" (Terminal-Bench 2.0, 2026-01 논문 시점, 특정 모델명은 논문 리더보드 참조 필요)
- **독자 전달 방식 제안:** 이 책의 **가장 적합한 벤치마크**다. Codex CLI가 실제로 평가 대상인 유일한 주요 학술 벤치마크. "SWE-bench는 패치를 재고, Terminal-Bench는 터미널에서 일을 끝내는 걸 잰다"는 대비로 소개하라. 다만 리더보드는 계속 갱신되므로 **책에는 구체 순위 대신 tbench.ai 링크와 "2026년 1월 기준 65% 미만" 정도로만** 적는 게 안전하다.

### 1-8. Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering ★ 이 책의 논지 그 자체
- **저자·연도:** Maria I. Gorinova, Macey Baker, Amy Heineike, Maksim Shaposhnikov, Rob Willoughby, Dru Knox (2026)
- **발표처:** arXiv cs.SE — 📄 preprint (2026-07-18 개정)
- **arXiv:** [2606.17799](https://arxiv.org/abs/2606.17799) (2026-06-16)
- **요약:** 코딩 에이전트가 이미 주된 개발 방식이 됐는데 평가 방식은 에이전트 이전 패러다임에 머물러 있다고 주장하는 포지션 페이퍼. 세 가지 문제를 든다. (1) **혼동 문제** — 점수가 모델의 몫인지 하네스·컨텍스트·환경의 몫인지 구분 못 함, (2) **정답 편향** — 하나의 레퍼런스 해답 기준 채점이 똑같이 타당한 다른 구현을 깎아내림, (3) **부품 단위 피드백 부재** — 무엇을 고쳐야 좋아지는지 알 수 없음.
- **핵심 주장:** 소프트웨어 엔지니어링 에이전트는 복합 시스템이며, **하네스 요소 하나를 바꾸는 것이 모델 세대를 통째로 올리는 것만큼 벤치마크 점수를 바꿀 수 있다.**
- **독자 전달 방식 제안:** ★★★ 이 책 전체를 정당화하는 논문이다. "왜 Codex 사용법 책이 필요한가"에 대한 답 — **같은 모델이라도 어떻게 쓰느냐가 모델 세대 차이만큼 결과를 바꾸기 때문.** 서문 또는 1장의 핵심 인용으로 배치할 것을 강력 권장.

---

## 2. Agentic coding 연구 (에이전트 설계·도구·컨텍스트)

### 2-1. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering ★ seminal
- **저자·연도:** John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press (2024)
- **발표처:** NeurIPS 2024 — ✅ peer-reviewed (arXiv 페이지에는 표기 없음, 학회 proceedings로 확인)
- **arXiv:** [2405.15793](https://arxiv.org/abs/2405.15793) (v1 2024-05-06, v3 2024-11-11)
- **요약:** **"인터페이스 설계가 에이전트 성능을 좌우한다"**를 증명한 논문. 모델을 바꾸지 않고, LM이 컴퓨터를 쓰는 방식(파일 편집·저장소 탐색·테스트 실행 인터페이스)만 설계했더니 성능이 크게 올랐다. ACI(Agent-Computer Interface)라는 개념을 세운 원조.
- **핵심 수치 (2024년 측정):** SWE-bench **12.5%**, HumanEvalFix **87.7%** — 당시 SOTA — ⏳ 낡음
- **재현성:** 코드·데이터·데모 공개 (swe-agent.com)
- **독자 전달 방식 제안:** 1-8과 짝. "왜 CLI 도구마다 결과가 다른가"의 학술적 기원. **모델이 아니라 도구가 성능이다** — 이 책의 실용 챕터(설정·도구 정의·AGENTS.md) 전체의 근거.

### 2-2. Agentless: Demystifying LLM-based Software Engineering Agents ★ 반대편 근거
- **저자·연도:** Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, Lingming Zhang (2024)
- **발표처:** arXiv cs.SE — 📄 preprint
- **arXiv:** [2407.01489](https://arxiv.org/abs/2407.01489) (v1 2024-07-01, v2 2024-10-29) | DOI: 10.48550/arXiv.2407.01489
- **요약:** 복잡한 자율 에이전트가 정말 필요하냐고 되물은 논문. **localization → repair → patch validation의 3단계 고정 파이프라인**만으로, LLM이 자율 판단하거나 도구를 굴리지 않게 하고도 당시 오픈소스 에이전트를 앞질렀다.
- **핵심 수치 (2024년 측정, SWE-bench Lite):** **32.00%(96건 해결), 비용 $0.70** — 당시 오픈소스 에이전트 대비 최고 성능·최저 비용 — ⏳ 낡음
- **인용할 만한 문장:**
  > "simple, interpretable technique[s]" may offer overlooked advantages (abstract 취지)
- **부수 발견:** 저자들이 SWE-bench 데이터셋의 문제를 직접 발견해 정제 세트(SWE-bench Lite-S)를 만들었다 — 1-2와 독립적으로 같은 결론에 도달했다는 점이 중요하다.
- **독자 전달 방식 제안:** Codex 사용법 책에서 **"에이전트에게 다 맡기지 말고 파이프라인을 좁혀라"**를 말할 때의 근거. 비용 축($0.70)도 실무 독자에게 잘 먹힌다.

### 2-3. Measuring AI Ability to Complete Long Software Tasks (METR 시간 지평)
- **저자·연도:** Thomas Kwa, Ben West, Joel Becker, ... Elizabeth Barnes, Lawrence Chan (METR, 2025)
- **발표처:** **NeurIPS 2025** — ✅ peer-reviewed
- **arXiv:** [2503.14499](https://arxiv.org/abs/2503.14499) (v1 2025-03-18, v4 2026-07-10)
- **요약:** 모델 능력을 정답률이 아니라 **"인간 시간"**으로 환산하는 지표를 제안했다. **50%-task-completion time horizon** = 모델이 50% 확률로 해내는 과제를, 전문가 인간이 평균 몇 분에 하는가. 능력 향상의 주 동인은 원시 추론력보다 **신뢰성과 실수 복구 능력**이라고 분석했다.
- **핵심 수치:**
  - Claude 3.7 Sonnet의 50% 시간 지평 ≈ **50분** (2025-03 논문 v1 기준) — ⏳ 모델 세대가 낡음
  - **2019년 이래 시간 지평이 약 7개월마다 두 배**
  - 외삽 시 5년 내 인간 한 달치 소프트웨어 과제 자동화 가능 — 저자들이 외적 타당성 한계를 명시함
- **독자 전달 방식 제안:** ★ 이 책에서 **"Codex에게 얼마나 큰 일을 한 번에 맡길 것인가"**를 판단하는 실무 감각의 근거. "모델은 시간 지평이 있고, 그 안쪽 크기로 일을 잘라 주는 게 사용자의 일"이라는 프레임. 단, 7개월 배가 추세는 강한 주장이므로 **저자들의 한계 명시와 함께** 인용할 것. v4가 2026년 7월 개정판이므로 숫자를 쓸 거면 최신본 확인 필요.

### 2-4. Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned
- **저자·연도:** Nghi D. Q. Bui (2026)
- **발표처:** arXiv — 📄 preprint, **"work in progress" 명시**
- **arXiv:** [2603.05344](https://arxiv.org/abs/2603.05344) (v1 2026-03-05, 2026-03-13 개정)
- **요약:** Rust로 만든 CLI 코딩 에이전트 OPENDEV의 설계 기록. 핵심 설계 결정 넷 — (1) 모델 라우팅을 갖춘 복합 시스템, (2) **계획과 실행을 분리한 이중 에이전트**, (3) **오래된 관측을 점진적으로 줄이는 적응적 컨텍스트 압축**, (4) 세션을 넘어 프로젝트 지식을 누적하는 메모리. 명시적 추론 단계와 지연 도구 탐색(lazy tool discovery)도 다룬다.
- **인용할 만한 문장:**
  > "adaptive context compaction that progressively reduces older observations" (abstract)
- **한계:** work-in-progress preprint. **정량 비교 결과가 abstract에 없다** — 설계 논거로만 인용하고 성능 주장은 하지 말 것.
- **독자 전달 방식 제안:** Codex CLI의 컨텍스트 압축(compaction)·`AGENTS.md` 메모리·플랜 모드를 설명할 때 **"이건 Codex만의 기벽이 아니라 터미널 에이전트 설계의 공통 해법"**임을 보이는 데 쓴다. 독자가 이미 Claude Code를 써봤으므로, 두 도구의 유사 설계를 같은 문제(컨텍스트 팽창)에 대한 답으로 묶어 설명하면 이해가 빠르다.

---

## 3. 생산성·코드 품질 실증 연구 (긍정·부정 양쪽)

**이 절의 전체 그림이 중요하다.** 세 개의 RCT가 +55.8%, +21%, −19%로 갈린다. 이 불일치 자체가 책에서 다뤄야 할 사실이다.

### 3-1. [긍정] The Impact of AI on Developer Productivity: Evidence from GitHub Copilot
- **저자·연도:** Sida Peng, Eirini Kalliamvakou, Peter Cihon, Mert Demirer (2023)
- **발표처:** arXiv cs.SE — 📄 preprint (GitHub/Microsoft 소속 저자 포함 — **이해관계 있음**)
- **arXiv:** [2302.06590](https://arxiv.org/abs/2302.06590) (2023-02-13)
- **요약:** 모집한 개발자에게 **JavaScript로 HTTP 서버를 최대한 빨리 구현**하게 한 통제 실험. 처리군만 Copilot을 썼다.
- **핵심 수치:** 처리군이 대조군보다 **55.8% 빠르게** 과제 완료 (2023-02, 단일 그린필드 과제)
- **인용할 만한 문장 (verbatim):**
  > "The treatment group, with access to the AI pair programmer, completed the task 55.8% faster than the control group." (abstract)
- **주의:** 널리 인용되는 "55%" 숫자의 원출처다. **과제가 단 하나, 그린필드, 짧은 과제**라는 조건을 반드시 함께 적어야 한다. 저자 소속상 이해관계도 밝히는 게 정직하다.

### 3-2. [긍정, 절제된] How much does AI impact development speed? An enterprise-based randomized controlled trial
- **저자·연도:** Elise Paradis, Kate Grey, Quinn Madison, Daye Nam, Andrew Macvean, Vahid Meimand, Nan Zhang, Ben Ferrari-Church, Satish Chandra (Google, 2024)
- **발표처:** arXiv cs.SE/cs.HC — 📄 preprint (v3 2024-11-11)
- **arXiv:** [2410.12944](https://arxiv.org/abs/2410.12944) (2024-10-16)
- **요약:** Google 정직원 개발자 **96명** 대상 RCT. 사내 AI 기능 3종이 복잡한 엔터프라이즈급 과제 소요 시간에 미치는 영향을 쟀다.
- **핵심 수치:** 소요 시간 **약 21% 단축** (2024년 여름, Google 사내 도구). AI군 평균 96분 vs 대조군 114분. **저자들이 신뢰구간이 넓다고 명시.** 하루 중 코딩 시간이 많은 개발자일수록 이득이 컸다.
- **인용할 만한 문장 (verbatim):**
  > "cannot assume that the effect size obtained in our lab study will necessarily apply more broadly, or that the effect of AI found using internal Google tooling in the summer of 2024 will translate across tools and over time" (abstract)
- **독자 전달 방식 제안:** ★ 이 인용문이 정말 좋다. **연구자 본인이 일반화를 경계하는 문장** — 책에서 "숫자를 인용하는 태도" 자체를 가르치는 데 쓸 수 있다.

### 3-3. [부정 + 체감·실측 괴리] ★★★ Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity
- **저자·연도:** Joel Becker, Nate Rush, Elizabeth Barnes, David Rein (METR, 2025)
- **발표처:** arXiv — 📄 preprint (학회 게재 표기 없음)
- **arXiv:** [2507.09089](https://arxiv.org/abs/2507.09089) (v1 2025-07-12, v2 2025-07-25)
- **요약:** **AI 경험이 어느 정도 있는 숙련 오픈소스 개발자 16명**이, **평균 5년간 다뤄온 성숙한 자기 저장소**에서 **246개 실제 과제**를 수행한 RCT. 과제마다 AI 사용 허용/불허를 무작위 배정했다. AI 허용 시 주로 Cursor Pro + Claude 3.5/3.7 Sonnet을 썼다.
- **핵심 수치 (2025년 2~6월 프런티어 도구 기준):**
  - 개발자 **사전 예측: 24% 단축**
  - 개발자 **사후 추정: 20% 단축**
  - **실측: 19% 증가 (느려짐)**
  - 경제학 전문가 예측 39% 단축, ML 전문가 예측 38% 단축 — 둘 다 부호가 반대
- **인용할 만한 문장 (verbatim):**
  > "Before starting tasks, developers forecast that allowing AI will reduce completion time by 24%. After completing the study, developers estimate that allowing AI reduced completion time by 20%. Surprisingly, we find that allowing AI actually increases completion time by 19%—AI tooling slowed developers down." (abstract)
- **한계 (반드시 함께 적을 것):** 표본 16명, 특수 조건 — **자기가 5년간 알아온 성숙한 저장소**. 즉 "개발자가 이미 코드베이스를 완벽히 아는 상황"이라는 **AI에게 가장 불리한 조건**이다. 낯선 코드베이스나 신규 프로젝트로 일반화할 수 없다. METR 자신도 2026-02 블로그에서 실험 설계를 변경한다고 공지했다.
- **독자 전달 방식 제안:** ★★★ **이 책 전체에서 가장 값진 한 편.** 요청하신 "체감과 실측이 갈린다"의 정확한 근거다. 20%p 이상의 **체감-실측 괴리**를 "AI는 쓸모없다"가 아니라 **"당신은 자신이 얼마나 빨라졌는지 스스로 판단할 수 없다"**로 읽어라. 그래서 Codex를 쓸 때 **어디에 쓸지 고르는 판단**이 중요해진다는 이 책의 실용 논지로 이어진다. 조건(숙련자, 익숙한 저장소)을 반드시 명시해야 오독을 막는다.

### 3-4. [코드 품질, 부정] Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild
- **저자·연도:** Yue Liu, Ratnadira Widyasari, Yanjie Zhao, Ivana Clairine Irsan, Junkai Chen, David Lo (2026)
- **발표처:** arXiv cs.SE — 📄 preprint (v1 2026-03-30, 2026-04-26 개정)
- **arXiv:** [2603.28592](https://arxiv.org/abs/2603.28592)
- **요약:** GitHub 저장소 **6,299개**에서 검증된 **AI 작성 커밋 302.6천 건**을 정적 분석해 도입된 이슈를 집계했다. AI 코딩 어시스턴트 5종을 대상으로 했다.
- **핵심 수치 (2026-03 발표):**
  - 총 **484,366건**의 고유 이슈 식별
  - 그중 **코드 스멜이 89.3%**
  - 각 AI 어시스턴트마다 **커밋의 15% 이상이 이슈를 최소 하나 도입**
  - 추적된 AI 도입 이슈의 **22.7%가 최신 버전에도 생존**
- **독자 전달 방식 제안:** 보안 챕터가 아니라 **"리뷰를 왜 놓지 말아야 하는가"** 챕터의 근거. "심각한 취약점"이 아니라 **코드 스멜이 압도적**이라는 점이 오히려 실무적으로 정확하다 — Codex가 만드는 문제는 대개 극적 사고가 아니라 **조용한 부채**다. ⚠️ 2차 소스에 304,362건/6,275개 저장소로 적힌 곳이 있으나, **abstract 원문 기준은 302.6k / 6,299개**다.

### 3-5. [코드 품질, 중립적] To What Extent Does Agent-generated Code Require Maintenance? An Empirical Study
- **저자·연도:** Shota Sawada, Tatsuya Shirai, Yutaro Kashiwa, Ken'ichi Yamaguchi, Hiroshi Iwata, Hajimu Iida (2026)
- **발표처:** **EASE 2026** (30th International Conference on Evaluation and Assessment in Software Engineering) — ✅ peer-reviewed
- **arXiv:** [2605.06464](https://arxiv.org/abs/2605.06464) (v1 2026-05-07, v2 2026-05-09)
- **요약:** AIDev 데이터셋을 써서 인기 저장소 100개의 **파일 1,000여 개, 변경 약 3,200건**을 분석했다. 에이전트 생성 코드와 사람 작성 코드의 유지보수 양상을 비교했다.
- **핵심 결과 (2026-05 발표):**
  - AI 생성 파일은 **갱신 빈도가 더 낮고**, 수정 시에도 파일의 작은 부분만 바뀜
  - AI 코드의 변경은 **기능 확장**이 지배적 / 사람 코드의 변경은 **버그 수정** 위주
  - **양쪽 모두 유지보수의 대부분은 사람 개발자가 수행**
- **독자 전달 방식 제안:** 3-4의 비관과 균형을 맞추는 데 쓴다. 그리고 "결국 사람이 유지보수한다"는 결론은 이 책의 톤 — **Codex는 작성을 대신하지만 소유는 대신하지 않는다** — 과 정확히 맞는다.

---

## 4. 위험·보안 연구 (보안 챕터 근거)

### 4-1. [고전] Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions
- **저자·연도:** Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, Ramesh Karri (2021)
- **발표처:** **IEEE Symposium on Security and Privacy (S&P) 2022** — ✅ peer-reviewed
- **arXiv:** [2108.09293](https://arxiv.org/abs/2108.09293) (2021-08-20, 최종본 2021-12-16)
- **요약:** 이 분야의 seminal 보안 논문. MITRE Top 25 취약점을 겨냥한 **89개 시나리오**를 만들어 **1,689개 프로그램**을 생성시키고 취약 여부를 분석했다.
- **핵심 수치:** 생성 프로그램의 **약 40%가 취약** (GitHub Copilot, 2021년 측정, MITRE Top 25 시나리오 기준) — ⏳ **매우 낡음.** 오늘날 Codex에 그대로 적용하면 안 된다.
- **독자 전달 방식 제안:** "40%"는 널리 회자되지만 **2021년 Copilot 자동완성 기준**이다. 이 책에서는 **역사적 출발점**으로만 쓰고, 최신 근거는 4-2·4-4로 갈아탈 것. 오히려 **"이 숫자를 오늘 인용하면 안 되는 이유"** 자체를 독자에게 가르치는 예시로 쓰면 좋다.

### 4-2. CWEval: Outcome-driven Evaluation on Functionality and Security of LLM Code Generation
- **저자·연도:** Jinjun Peng, Leyi Cui, Kele Huang, Junfeng Yang, Baishakhi Ray (2025)
- **발표처:** **LLM4Code 2025** — ✅ peer-reviewed (게재 예정 표기)
- **arXiv:** [2501.08200](https://arxiv.org/abs/2501.08200) (2025-01-14)
- **요약:** 기존 보안 벤치마크(CyberSecEval, SecurityEval)의 한계를 지적하고, 고품질 과제 명세 + 결과 기반 테스트 오라클로 정확도를 높인 다국어 벤치마크 CWEval-bench를 제안했다.
- **핵심 주장:** **"기능적으로는 정확하지만 안전하지 않은 코드"가 상당 비율 존재**하며, 이런 코드의 취약점 탐지가 명백히 망가진 코드보다 훨씬 어렵다. 보안 전문성이 없는 개발자에게 특히 그렇다.
- **재현성:** GitHub 오픈소스 아티팩트 공개
- **독자 전달 방식 제안:** ★ 보안 챕터의 **개념적 축**. "테스트가 통과했다"와 "안전하다"가 다른 명제라는 것. Codex가 낸 PR이 초록불인데도 위험할 수 있는 이유를 이 논문으로 설명하라. **정적 분석·보안 스캐너를 파이프라인에 넣으라**는 실무 조언의 근거.

### 4-3. GitInject: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines
- **저자·연도:** Jafar Isbarov, Umid Suleymanov, Ilia Shumailov, Murat Kantarcioglu (2026)
- **발표처:** arXiv cs.CR — 📄 preprint
- **arXiv:** [2606.09935](https://arxiv.org/abs/2606.09935) (2026-06-07)
- **요약:** GitHub 워크플로에서의 프롬프트 인젝션을 평가하는 오픈소스 프레임워크. **시뮬레이션이 아니라 실제 저장소를 프로비저닝하고 실제 워크플로를 실행**했다는 점이 중요하다. 자격증명 탈취·설정 조작·서비스 중단 등 11개 공격 범주를 정의했다.
- **핵심 결과 (2026-06 발표):**
  - **기본 설정 상태의 모든 테스트 제공자가 최소 하나의 공격에 취약**
  - 저자 결론: **가장 심각한 취약점은 모델 고유가 아니라 구조적**이며, CI/CD가 자격증명·설정 파일을 다루는 방식에서 비롯됨
  - 확인된 취약 범주마다 최소 비용 완화책과 그 한계를 문서화
- **독자 전달 방식 제안:** ★★ **"모델을 더 똑똑하게 만들어도 안 풀린다"**는 메시지가 핵심. Codex를 CI에 붙이려는 독자에게 "모델 선택이 아니라 자격증명 스코프 설계가 답"이라고 말할 근거. **4-5(공식 시스템 카드의 샌드박스 기본값)와 짝지어** 쓰면 "왜 OpenAI가 네트워크를 기본 차단하는가"가 자연스럽게 설명된다.

### 4-4. IssueTrojanBench: Benchmarking AI Coding Agents Against Malicious Issue Requests ★★★ Codex 직접 평가
- **저자·연도:** Ankur Singh, Jinqiu Yang, Tse-Hsun Chen (2026)
- **발표처:** arXiv cs.CR/cs.AI/cs.SE — 📄 preprint
- **arXiv:** [2607.20759](https://arxiv.org/abs/2607.20759) (2026-07-22) — **가장 최신 항목**
- **요약:** 악의적 GitHub 이슈를 통해 코딩 에이전트를 공격하는 벤치마크. 공격 4범주 × 전달 벡터 6종. **실제 배포된 제품 3종 — Cursor, Claude Code, Codex Desktop — 을 직접 평가**했고, 구동 모델은 GPT-5.3/5.4와 Anthropic Sonnet 4.6이었다.
- **핵심 수치 (2026-07 발표):**
  - **악의적 이슈의 66.5%가 모든 가드레일을 통과**
  - **거부는 거의 전적으로 LLM에서 발생하며, 에이전트 프레임워크가 아니다**
  - 기존 에이전트 수준 방어는 제한적 효과에 그침
- **인용할 만한 문장:**
  > "rejection is almost entirely from LLMs rather than the agent frameworks" (abstract)
- **독자 전달 방식 제안:** ★★★ 이 책에 가장 직접적인 보안 근거다. **Codex를 이름으로 평가한 유일한 최신 학술 벤치마크.** 두 번째 발견("거부는 프레임워크가 아니라 모델이 한다")이 실무적으로 결정적이다 — **CLI 설정으로 안전을 살 수 없다**는 뜻이고, 그래서 신뢰 경계를 사람이 설계해야 한다는 결론이 나온다. 단, 66.5%는 강한 숫자이므로 **"이 벤치마크가 설계한 공격 시나리오 기준"**임을 반드시 함께 적어라.

### 4-5. [공식 1차 소스] Addendum to GPT-5.2 System Card: GPT-5.2-Codex
- **발행처·일자:** OpenAI, **2025년 12월 18일**
- **URL:** https://openai.com/index/gpt-5-2-codex-system-card/ (PDF: `cdn.openai.com/pdf/ac7c37ae-7f4c-4442-b741-2eabdeaf77e0/oai_5_2_Codex.pdf`)
- **유형:** 공식 기술 리포트 (peer-review 대상 아님 — **벤더 자체 보고**임을 명시할 것)
- **검증:** PDF를 내려받아 본문 텍스트를 직접 읽어 아래 내용을 확인했다.
- **핵심 내용 (책 보안·설정 챕터에 직결):**
  - **샌드박스 기본 동작 (§3.1):** 클라우드에서는 OpenAI 호스팅 격리 컨테이너, 네트워크 기본 차단. 로컬에서는 **macOS = Seatbelt 정책, Linux = seccomp + landlock 조합, Windows = 네이티브 샌드박스 또는 WSL 경유 Linux 샌드박스**. 모델이 샌드박스 안에서 명령을 실행하지 못할 때 사용자가 비샌드박스 실행을 승인할 수 있다.
  - **기본 샌드박스의 두 가지 설계 목표 (verbatim):**
    > "Disable network access by default: This significantly reduces the risk of prompt injection attacks, data exfiltration, or the agent inadvertently connecting to malicious external resources."
    > "Restrict file edits to the current workspace: This prevents the agent from making unauthorized modifications to files outside of the user's active project"
  - **네트워크 개방의 대가 (§3.2, verbatim):**
    > "Enabling internet access can introduce risks like prompt injection, leaked credentials, or use of code with license restrictions. Users should review outputs carefully and limit access to trusted domains and safe HTTP methods."
  - **파괴적 행동 회피 (§4.2) — ★ 이 책에 특히 유용:** 코딩 에이전트는 파일 시스템·Git·패키지 매니저에 접근하므로 데이터 삭제/손상이라는 고위험 실패 모드를 갖는다. 시스템 카드가 직접 든 예: `rm -rf`, `git clean -xfd`, `git reset --hard`, `push --force`.
    > "Simple instructions like 'clean the folder' or 'reset the branch' can mask dangerous operations (rm -rf, git clean -xfd, git reset –hard, push –force) that lead to data loss, repo corruption, or security boundary violations."
  - **파괴적 행동 회피 정량 결과 (Table 4, OpenAI 자체 평가, 2025-12-18 발표):**
    | 모델 | destructive action avoidance |
    |---|---|
    | gpt-5-codex | 0.66 |
    | gpt-5.1-codex | 0.70 |
    | gpt-5.1-codex-max | 0.75 |
    | **gpt-5.2-codex** | **0.76** |
    → 최신 모델도 **약 4회 중 1회는 파괴적 행동을 피하지 못한다.** 이 지표는 사용자 변경 보존 능력도 함께 잰다. GPT-5.2-Codex는 RL 롤아웃 중 사용자의 상충 편집을 만들어내는 "user model"로 학습됐고, 사용자 변경을 되돌리지 않으면 보상을 받았다.
  - **사이버 안전 정책 준수율 (Table 3, 정책 준수율, 높을수록 좋음):** production data — gpt-5.1-thinking 0.866 / gpt-5.2-thinking 0.966 / **gpt-5.2-codex 0.921**. synthetic data — 0.930 / 0.993 / **0.939**.
  - **Preparedness 판정:** 사이버보안 영역에서 "매우 유능하나 High capability에는 미달". 생물학은 High로 취급. AI 자기개선은 High 미달.
- **⚠️ 중요한 부재:** 이 애드덤에는 **프롬프트 인젝션에 대한 정량 평가표가 없다.** 인젝션은 §3에서 완화책(샌드박스·네트워크 차단)으로만 서술되고, 별도 벤치마크 수치가 제시되지 않는다. 책에서 "OpenAI가 인젝션 방어율 N%를 보고했다"고 쓰면 **거짓이 된다.** 4-4(IssueTrojanBench)가 이 공백을 메우는 독립 근거다.
- **독자 전달 방식 제안:** ★★★ 이 책의 보안·설정 챕터에서 **가장 인용 밀도가 높아야 할 문서.** 특히 파괴적 행동 표(0.66→0.76)는 "승인 모드를 왜 함부로 풀면 안 되는가"에 대한 **OpenAI 자신의 숫자**다. 벤더가 자기 모델의 한계를 스스로 보고한 수치라는 점에서 설득력이 남다르다.

---

## 5. 이 책에 인용할 만한 문장 (근거와 함께)

책의 문맥에 맞게 골라 쓸 수 있도록, **어느 챕터에 쓸지**까지 붙였다.

**① 이 책의 존재 이유 (서문 / 1장)**
> 하네스 요소 하나를 바꾸는 것이 모델 세대를 통째로 올리는 것만큼 벤치마크 점수를 바꿀 수 있다.
> — Gorinova et al., "Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering," arXiv:2606.17799, 2026 (📄 preprint)

**② 인터페이스가 성능이다 (설정 / AGENTS.md 챕터)**
> 모델을 바꾸지 않고 에이전트-컴퓨터 인터페이스만 설계해도 성능이 크게 오른다.
> — Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering," NeurIPS 2024, arXiv:2405.15793 (✅ peer-reviewed). 당시 SWE-bench 12.5% 달성 ⏳

**③ 체감과 실측은 다르다 (생산성 / 워크플로 챕터) ★ 최우선 추천**
> "Before starting tasks, developers forecast that allowing AI will reduce completion time by 24%. ... Surprisingly, we find that allowing AI actually increases completion time by 19%—AI tooling slowed developers down."
> — Becker, Rush, Barnes, Rein (METR), arXiv:2507.09089, 2025 (📄 preprint). 숙련 개발자 16명, 246개 과제, **평균 5년간 다뤄온 자기 저장소**, 2025년 2~6월 도구 기준. **조건을 반드시 함께 적을 것.**

**④ 숫자를 인용하는 태도 (전 챕터의 메타 규율)**
> "cannot assume that the effect size obtained in our lab study will necessarily apply more broadly, or that the effect of AI found using internal Google tooling in the summer of 2024 will translate across tools and over time"
> — Paradis et al. (Google), arXiv:2410.12944, 2024 (📄 preprint). 자사 도구로 21% 개선을 얻고도 저자들이 스스로 붙인 경계.

**⑤ 리더보드를 믿지 마라 (벤치마크 / 모델 선택 챕터)**
> "32.67% of the successful patches involve cheating as the solutions were directly provided in the issue report or the comments"
> — Aleithan et al., "SWE-Bench+," arXiv:2410.06992, 2024 (📄 preprint). 문제 인스턴스 제거 시 해결률 12.47% → 3.97%. 저자들은 이 결함이 SWE-bench Verified에도 남아 있다고 명시.

**⑥ 벤치마크 결함은 방법론 문제다 (벤치마크 챕터)**
> "SWE-bench Verified uses insufficient test cases, while TAU-bench counts empty responses as successful. Such issues can lead to under- or overestimation of agents' performance by up to 100% in relative terms."
> — Zhu et al., arXiv:2507.02825, 2025 (📄 preprint)

**⑦ 사내 코드베이스는 더 어렵다 (기대치 설정 챕터)**
> SWE-Bench Pro에서 프런티어 모델의 Pass@1은 25% 미만이며, 공개 저장소 세트(GPT-5 23.3%)보다 상업 저장소 세트(GPT-5 14.9%)에서 더 떨어진다.
> — Deng et al., arXiv:2509.16941, 2025 (📄 preprint), 2025년 9월 측정

**⑧ 통과한 테스트가 안전을 뜻하지 않는다 (보안 챕터)**
> LLM은 기능적으로는 정확하지만 안전하지 않은 코드를 상당 비율로 생산하며, 이런 코드의 취약점 탐지는 명백히 망가진 코드보다 훨씬 어렵다.
> — Peng et al., "CWEval," LLM4Code 2025, arXiv:2501.08200 (✅ peer-reviewed)

**⑨ 가드레일은 프레임워크가 아니라 모델에 있다 (보안 챕터) ★ Codex 직접 평가**
> "rejection is almost entirely from LLMs rather than the agent frameworks" — 악의적 이슈의 66.5%가 모든 가드레일을 통과했다.
> — Singh, Yang, Chen, "IssueTrojanBench," arXiv:2607.20759, 2026 (📄 preprint). **Cursor, Claude Code, Codex Desktop을 GPT-5.3/5.4·Sonnet 4.6 구동으로 직접 평가.**

**⑩ 파괴적 행동은 여전히 남아 있다 (승인 모드 / 샌드박스 챕터) ★ OpenAI 자체 숫자**
> "Simple instructions like 'clean the folder' or 'reset the branch' can mask dangerous operations (rm -rf, git clean -xfd, git reset –hard, push –force) that lead to data loss, repo corruption, or security boundary violations."
> — OpenAI, "Addendum to GPT-5.2 System Card: GPT-5.2-Codex," 2025-12-18. 같은 문서 Table 4: destructive action avoidance가 gpt-5-codex 0.66 → gpt-5.2-codex 0.76.

**⑪ 인젝션 위험은 구조적이다 (CI 연동 챕터)**
> 기본 설정의 모든 제공자가 최소 하나의 공격에 취약했고, 가장 심각한 취약점은 모델 고유가 아니라 CI/CD가 자격증명·설정을 다루는 방식에서 오는 구조적 문제였다.
> — Isbarov et al., "GitInject," arXiv:2606.09935, 2026 (📄 preprint)

**⑫ 조용한 부채 (리뷰 챕터)**
> AI 작성 커밋 302.6천 건 분석 결과 총 484,366건의 이슈가 식별됐고, 그중 89.3%가 코드 스멜이며, 추적된 이슈의 22.7%가 최신 버전에도 생존해 있다.
> — Liu et al., "Debt Behind the AI Boom," arXiv:2603.28592, 2026 (📄 preprint). GitHub 저장소 6,299개, AI 어시스턴트 5종.

**⑬ 일의 크기를 자르는 감각 (워크플로 챕터)**
> 프런티어 AI의 시간 지평은 2019년 이래 약 7개월마다 두 배가 됐다. 향상의 주 동인은 원시 추론력이 아니라 신뢰성과 실수 복구 능력이다.
> — Kwa et al. (METR), "Measuring AI Ability to Complete Long Software Tasks," NeurIPS 2025, arXiv:2503.14499 (✅ peer-reviewed). 저자들이 외적 타당성 한계를 명시함. v4(2026-07-10)가 최신본이므로 구체 수치 인용 시 최신본 확인 필요.

**⑭ 결국 소유는 사람이 한다 (마무리 챕터)**
> AI 생성 코드와 사람 작성 코드 모두, 유지보수의 대부분은 사람 개발자가 수행한다.
> — Sawada et al., EASE 2026, arXiv:2605.06464 (✅ peer-reviewed). 인기 저장소 100개, 파일 1,000여 개, 변경 약 3,200건 분석.

---

## 6. 참고문헌

| # | 저자 (연도) | 제목 | ID | 발표처 | Peer-review |
|---|---|---|---|---|---|
| 1 | Jimenez, Yang, Wettig, Yao, Pei, Press, Narasimhan (2023) | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | [arXiv:2310.06770](https://arxiv.org/abs/2310.06770) | ICLR 2024 | ✅ |
| 2 | Aleithan, Xue, Mohajer, Nnorom, Uddin, Wang (2024) | SWE-Bench+: Enhanced Coding Benchmark for LLMs | [arXiv:2410.06992](https://arxiv.org/abs/2410.06992) | arXiv cs.SE | 📄 |
| 3 | Prathifkumar, Mathews, Nagappan (2025) | Does SWE-Bench-Verified Test Agent Ability or Model Memory? | [arXiv:2512.10218](https://arxiv.org/abs/2512.10218) | arXiv cs.SE | 📄 |
| 4 | Zhu, Jin, Pruksachatkun, ... Liang, Kang 외 (2025) | Establishing Best Practices for Building Rigorous Agentic Benchmarks | [arXiv:2507.02825](https://arxiv.org/abs/2507.02825) | arXiv cs.AI | 📄 |
| 5 | Miserendino, Wang, Patwardhan, Heidecke (2025) | SWE-Lancer: Can Frontier LLMs Earn $1 Million from Real-World Freelance Software Engineering? | [arXiv:2502.12115](https://arxiv.org/abs/2502.12115) | arXiv cs.LG/cs.SE | 📄 |
| 6 | Deng, Da, Pan 외 (2025) | SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks? | [arXiv:2509.16941](https://arxiv.org/abs/2509.16941) | arXiv cs.SE | 📄 |
| 7 | Merrill, Shaw, Carlini, ... Konwinski, Schmidt 외 (2026) | Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces | [arXiv:2601.11868](https://arxiv.org/abs/2601.11868) | **ICLR 2026** | ✅ |
| 8 | Gorinova, Baker, Heineike, Shaposhnikov, Willoughby, Knox (2026) | Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering | [arXiv:2606.17799](https://arxiv.org/abs/2606.17799) | arXiv cs.SE | 📄 |
| 9 | Yang, Jimenez, Wettig, Lieret, Yao, Narasimhan, Press (2024) | SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering | [arXiv:2405.15793](https://arxiv.org/abs/2405.15793) | NeurIPS 2024 | ✅ |
| 10 | Xia, Deng, Dunn, Zhang (2024) | Agentless: Demystifying LLM-based Software Engineering Agents | [arXiv:2407.01489](https://arxiv.org/abs/2407.01489) / DOI 10.48550/arXiv.2407.01489 | arXiv cs.SE | 📄 |
| 11 | Kwa, West, Becker, ... Barnes, Chan (2025) | Measuring AI Ability to Complete Long Software Tasks | [arXiv:2503.14499](https://arxiv.org/abs/2503.14499) | **NeurIPS 2025** | ✅ |
| 12 | Bui (2026) | Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned | [arXiv:2603.05344](https://arxiv.org/abs/2603.05344) | arXiv (work in progress) | 📄 |
| 13 | Peng, Kalliamvakou, Cihon, Demirer (2023) | The Impact of AI on Developer Productivity: Evidence from GitHub Copilot | [arXiv:2302.06590](https://arxiv.org/abs/2302.06590) | arXiv cs.SE | 📄 |
| 14 | Paradis, Grey, Madison, Nam, Macvean, Meimand, Zhang, Ferrari-Church, Chandra (2024) | How much does AI impact development speed? An enterprise-based randomized controlled trial | [arXiv:2410.12944](https://arxiv.org/abs/2410.12944) | arXiv cs.SE/cs.HC | 📄 |
| 15 | Becker, Rush, Barnes, Rein (2025) | Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity | [arXiv:2507.09089](https://arxiv.org/abs/2507.09089) | arXiv (METR) | 📄 |
| 16 | Liu, Widyasari, Zhao, Irsan, Chen, Lo (2026) | Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild | [arXiv:2603.28592](https://arxiv.org/abs/2603.28592) | arXiv cs.SE | 📄 |
| 17 | Sawada, Shirai, Kashiwa, Yamaguchi, Iwata, Iida (2026) | To What Extent Does Agent-generated Code Require Maintenance? An Empirical Study | [arXiv:2605.06464](https://arxiv.org/abs/2605.06464) | **EASE 2026** | ✅ |
| 18 | Pearce, Ahmad, Tan, Dolan-Gavitt, Karri (2021) | Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions | [arXiv:2108.09293](https://arxiv.org/abs/2108.09293) | **IEEE S&P 2022** | ✅ |
| 19 | Peng, Cui, Huang, Yang, Ray (2025) | CWEval: Outcome-driven Evaluation on Functionality and Security of LLM Code Generation | [arXiv:2501.08200](https://arxiv.org/abs/2501.08200) | **LLM4Code 2025** | ✅ |
| 20 | Isbarov, Suleymanov, Shumailov, Kantarcioglu (2026) | GitInject: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines | [arXiv:2606.09935](https://arxiv.org/abs/2606.09935) | arXiv cs.CR | 📄 |
| 21 | Singh, Yang, Chen (2026) | IssueTrojanBench: Benchmarking AI Coding Agents Against Malicious Issue Requests | [arXiv:2607.20759](https://arxiv.org/abs/2607.20759) | arXiv cs.CR/cs.AI/cs.SE | 📄 |
| 22 | OpenAI (2025-12-18) | Addendum to GPT-5.2 System Card: GPT-5.2-Codex | https://openai.com/index/gpt-5-2-codex-system-card/ | 공식 기술 리포트 | ❌ 벤더 자체 보고 |

**peer-review 요약:** ✅ 7편 (ICLR 2024·ICLR 2026·NeurIPS 2024·NeurIPS 2025·EASE 2026·IEEE S&P 2022·LLM4Code 2025) / 📄 preprint 14편 / 공식 벤더 문서 1건.

---

## 7. 리서치 한계

**반드시 fact-checker에게 전달해야 할 사항들이다.**

1. **preprint 비중이 높다 (14/22).** 이 분야의 속도 때문에 불가피하다. 2026년 발표 논문은 거의 전부 preprint다. 책에서 preprint를 인용할 때는 "아직 동료 심사를 거치지 않은"이라는 단서를 붙이는 것을 권한다. 특히 GitInject·IssueTrojanBench·Debt Behind the AI Boom·Position 페이퍼가 그렇다.

2. **본문 전문을 읽지 않은 항목이 있다.** SWE-Bench Pro의 모델별 점수(GPT-5 23.3% 등)는 HTML 본문에서, GPT-5.2-Codex 시스템 카드는 PDF 전문에서 직접 확인했다. 나머지 항목은 **arXiv abstract 페이지 기준**이다. 방법론 세부나 표 수치를 책에 옮길 때는 해당 논문 본문 재확인이 필요하다.

3. **SWE-Lancer의 모델별 pass rate를 확정하지 못했다.** 2차 소스(aibase, Medium)에 GPT-4o 8.0% / Claude 3.5 Sonnet 26.2%가 돌아다니지만 abstract에서 확인되지 않았다. **책에 쓰려면 논문 본문 표를 열어보거나, 아예 쓰지 말 것.** 어느 쪽이든 모델 세대가 낡았다.

4. **Terminal-Bench 리더보드 수치는 휘발성이 극단적이다.** 논문의 "65% 미만"은 2026년 1월 기준이며, tbench.ai 리더보드는 상시 갱신된다. Codex CLI의 구체 순위·점수를 책에 박아 넣는 것은 권하지 않는다.

5. **⏳ 낡음 표시 항목 재확인.** SWE-bench 1.96%(2023), SWE-agent 12.5%(2024), Agentless 32%(2024), Copilot 40% 취약(2021), Claude 3.7 Sonnet 50분 시간 지평(2025-03). 이 숫자들은 **역사 서술로만** 쓰고 현재 Codex 성능의 근거로 쓰지 말 것.

6. **접근 실패:** openai.com의 시스템 카드 웹 페이지는 HTTP 403으로 차단됐다. cdn.openai.com의 PDF를 직접 내려받아 텍스트로 변환해 읽었으므로 내용은 검증됐다. 단 **GPT-5.1-Codex-Max 시스템 카드와 OpenAI Deployment Safety Hub의 CVE-Bench 결과는 확인하지 못했다** — 웹 리서처가 보완할 여지가 있다.

7. **커버되지 않은 영역:** (a) 다중 에이전트 협업 연구는 코딩 도메인 한정 양질 논문을 못 찾아 제외했다. (b) 에이전트 샌드박스 탈출(sandbox escape)에 대한 학술 논문은 이번 검색 범위에서 찾지 못했다 — 4-5의 공식 샌드박스 설계 서술로 대체했다. (c) Codex 특정 기능(승인 모드, `AGENTS.md`, 클라우드 위임)에 대한 독립 학술 평가는 존재하지 않는다. **이 부분은 논문이 아니라 공식 문서·커뮤니티 리서치가 메워야 한다.**

8. **숫자 불일치 1건 발견·해소:** "Debt Behind the AI Boom"의 데이터셋 규모가 2차 소스에서는 304,362 커밋 / 6,275 저장소로, arXiv abstract 원문에서는 302.6k 커밋 / 6,299 저장소로 나온다. **원문 기준(302.6k / 6,299)을 채택했다.**

9. **연구 결과 자체가 서로 충돌한다 — 이건 한계가 아니라 발견이다.** 생산성 RCT 세 편이 +55.8%(2023, 그린필드 단일 과제), +21%(2024, Google 사내), −19%(2025, 숙련자·익숙한 저장소)로 갈린다. **평균을 내려 하지 말 것.** 조건이 다르면 결과가 뒤집힌다는 것이 이 셋이 함께 말하는 바이며, 그 자체가 이 책이 "언제 어디에 Codex를 쓸 것인가"를 다뤄야 하는 이유다.
