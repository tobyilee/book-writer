# AI 시대 개발자의 학습과 성장 — 레퍼런스 문서

> 본 문서는 책 *AI 시대 개발자의 학습과 성장*의 1차 종합 자료다. Agentic Coding / Vibe Coding 환경에서 개발자가 피상적 개발에 빠지지 않고 깊이 있는 기술 이해를 유지하며 성장하는 법을 다룬다. 3층 독자(학생·신입 / 주니어·시니어 / CTO·테크 리더)를 모두 염두에 둔다.
>
> 자료 출처 라벨: **[웹]** 블로그·뉴스·공식문서 · **[논문]** arXiv·ACM·peer-reviewed · **[커뮤니티]** HN·Reddit·OKKY·velog·X · **[데이터]** DORA/Stack Overflow Survey/GitClear/METR 등 정량 보고서
>
> 본 리서치는 single agent 환경에서 web/paper/community 세 갈래를 직렬로 수집해 한 문서로 종합한 결과다. 세 갈래의 raw 산출물(`research/web.md`, `papers.md`, `community.md`)은 별도로 분리 저장하지 않았다.

---

## 1. 개념과 정의

AI 코딩을 둘러싼 용어가 18개월 사이에 폭발했다. 모호한 채로 두면 본문이 흐려진다. 본 책에서 사용할 용어를 먼저 못 박는다.

### 1.1 Vibe Coding (바이브 코딩)

**원전:** Andrej Karpathy, 2025년 2월 2일 X 게시물.
> "There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists. It's possible because the LLMs (e.g. Cursor Composer w Sonnet) are getting too good." **[웹]**
> — Karpathy, X, 2025-02-02 (https://x.com/karpathy/status/1886192184808149383)

Karpathy 본인은 후술 회고에서 "샤워하다 떠오른 throwaway tweet"이라 일축했지만, 이 트윗은 4.5M 뷰를 얻고 *Collins Dictionary*가 선정한 2025년 올해의 단어로 등재되며 산업 용어가 됐다 **[웹]**.

**핵심 행동 패턴:** (1) LLM에 자연어로 지시 → (2) 생성 코드를 읽지 않고 수용 → (3) 동작이 이상하면 에러를 다시 LLM에 던지고 재생성 → (4) 코드 자체를 *소유*하지 않는다.

**Simon Willison의 보존적 정의:** "If an LLM wrote every line of your code, but you've reviewed, tested, and understood it all, that's not vibe coding in my book — that's using an LLM as a typing assistant." **[웹]** (https://simonwillison.net)

### 1.2 Vibe Engineering (바이브 엔지니어링)

Vibe Coding이 "throwaway 프로토타입용 무책임 코딩"으로 굳어가자, Simon Willison이 *생산 코드용 책임 있는 AI-assisted programming*을 가리키는 별도 용어로 제안한 개념 **[웹]** (https://simonw.substack.com/p/vibe-engineering).

> "Vibe engineering establishes a clear distinction from vibe coding. It signals that this is a different, harder and more sophisticated way of working with AI tools to build production software." — Simon Willison

Willison이 vibe engineer에게 요구하는 비-협상 항목: 자동화 테스트(특히 test-first), 아키텍처 사전 설계, 문서, 강한 Git 습관, CI/CD, 코드 리뷰 문화, manual QA, preview 환경, "위임 가능 영역 판단력", 새로운 추정(estimation) 감각. *"Almost all of these are characteristics of senior software engineers already!"*

### 1.3 Agentic Coding (에이전트 코딩)

**도구 측면 정의:** LLM이 단발 자동완성을 넘어 파일 시스템·셸·테스트 러너·웹 검색을 호출하며 *반복적으로* 작업하는 패러다임. 대표 도구: Claude Code(2025-02 출시), Cursor Composer, GitHub Copilot Agent, OpenAI Codex CLI(2025-04), Gemini CLI(2025-06), Aider, Cline, Devin **[웹]**.

> "The rise of coding agents like Claude Code (released February 2025), OpenAI's Codex CLI (April) and Gemini CLI (June) has dramatically increased the usefulness of LLMs for real-world coding problems." — Simon Willison **[웹]**

### 1.4 Software 3.0 (Karpathy)

Karpathy 자신은 vibe coding을 "워밍업"이라 표현하며, *Software 1.0 → 2.0 → 3.0* 패러다임을 제시한다 **[웹]** (https://app.dealroom.co/news/note/vibe-coding-was-just-the-warmup-andrej-karpathy-on-the-dawn-of-software-3-0):

| 패러다임 | 인간이 만드는 것 | 컴퓨터가 실행하는 것 |
|----------|----------------|-------------------|
| Software 1.0 | 명시적 코드 | 컴파일된 명령 |
| Software 2.0 | 학습 데이터 | 학습된 신경망 |
| Software 3.0 | 자연어 프롬프트 | LLM이 해석한 행위 |

요지: 3.0이 1.0/2.0을 *대체*하는 게 아니라 **세 번째 도구로 추가**된다. 개발자는 세 패러다임을 모두 운용해야 한다.

### 1.5 본 책에서의 운용 정의

| 책 본문 용어 | 운용 정의 |
|------------|----------|
| **AI-assisted coding** | LLM/Agent를 사용하는 모든 코딩 행위의 우산어 |
| **Vibe coding** | 코드를 읽지 않고 동작에만 베팅하는, *낮은 책임*의 AI-assisted coding |
| **Vibe engineering / Agentic engineering** | LLM·Agent를 사용하되 *검토·테스트·이해·소유*가 유지되는 코딩 |
| **AI 의존(AI dependency)** | 도구 없이는 동등한 결과를 못 내는 상태. 자체로 가치 중립적이며, 맥락에 따라 정상적 도구 의존이거나 위험한 atrophy |

---

## 2. 현황 데이터 (정량)

### 2.1 채택률과 일상 사용 (Stack Overflow Developer Survey 2025)

- **AI 도구 사용·도입 의지:** 84% (2024년 76%에서 8%p 상승) **[데이터]** (https://survey.stackoverflow.co/2025/ai)
- **일일 사용:** 전문 개발자의 51%가 매일 사용
- **AI를 배우려 코딩을 시작:** 36%
- **AI로 코딩을 학습:** 44% (2024년 37%에서 7%p 상승)
- **전문 vs 학습자 도구 선호:** Claude Sonnet — 전문 45% / 학습자 30%

### 2.2 신뢰의 역설 (같은 보고서)

- **AI 출력의 정확성을 신뢰:** 29% (2024년 40%에서 11%p 하락) **[데이터]**
- **AI 출력을 *적극 불신*:** 46% (신뢰 33%를 추월)
- **AI 호감도:** 60% (2023·24년의 70% 이상에서 추세 하락)
- **최대 불만 1위 (66%):** "AI 해답이 *거의 맞는데* 정확히는 아니다"
- **최대 불만 2위 (45%):** "AI 코드 디버깅이 더 오래 걸린다"
- **여전히 사람에게 물어보는 이유 1위 (75%):** "AI 답을 신뢰할 수 없을 때"

> "Developers Lean on AI More, But Report Growing Doubts About Accuracy." — Stack Overflow press release **[웹]** (https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/)

### 2.3 실측 생산성 (METR, 2025)

> **Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity** — METR, 2025-07-10 (https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) **[데이터][논문 arXiv:2507.09089]**

- **N:** 16명의 숙련 OSS 개발자, 246개 실제 이슈, 평균 작업시간 2시간
- **사용 도구:** 주로 Cursor Pro + Claude 3.5/3.7 Sonnet
- **결과:** AI 사용 시 **19% *느려졌다*** (slower)
- **주관 vs 실제:** 사전에 -24% 예상, 사후에도 -20% 빨라졌다고 답함 → 약 40%p 인식 격차
- **METR의 적용 한계 (저자 본인 명시):** 결과는 (a) "less experienced developers"나 (b) 익숙한 코드베이스가 아닌 경우, (c) 수백 시간 이상 도구를 익힌 사용자에게는 다르게 나올 수 있다

이 연구는 책의 핵심 인용 자산이다. "AI가 빠르다는 느낌"과 "실제 빠름" 사이의 간격을 정량으로 보인 첫 사례.

> "Developers thought AI made them faster. The data said otherwise." — Let's Data Science 요약 **[웹]**

### 2.4 조직 단위 — DORA State of AI-assisted Software Development 2025

DORA 보고서(Google, https://dora.dev/research/2025/dora-report/)는 *AI 사용 ↑*과 *조직 성과*의 관계를 7개 archetype 기반으로 재정의했다 **[데이터]**.

핵심 발견:

- **개인 처리량 증가:** AI 사용자의 task 처리 +21%, PR merge +98% (개인 수준)
- **조직 throughput 증가:** 평균 +2~18%
- **그러나 안정성 하락:** change failure rate가 *유의하게* 상승
- **AI는 증폭기(amplifier):** 강한 조직(관측성·CI/CD·코드 리뷰 문화 보유)은 AI로 더 강해지고, 약한 조직은 더 약해진다
- **on-demand 배포 수준 달성:** 16.2%만이 elite 성과 (다회 일일 배포)

> "AI is fundamentally an amplifier, not a solution. It magnifies the strengths of high-performing organizations with robust observability while exposing the dysfunctions of struggling ones." — DORA 2025 요약 **[웹]**

90% AI adoption 증가가 9% 버그율 상승, 91% 코드 리뷰 시간 상승, 154% PR 크기 증가와 동반된다는 데이터도 자주 인용된다 **[웹]** (mikemason.ca).

### 2.5 코드 품질 — GitClear vs GitHub의 정면 충돌

**GitClear "Coding on Copilot" (2024, 2025):** 4년치·150M+ 라인을 분석한 결과 **[데이터]** (https://www.gitclear.com)
- **Code churn**(2주 내 되돌려지는 라인 비율): 2021 베이스라인 대비 2024 두 배 예측
- **Copy/pasted 코드** 비율이 *added·moved·deleted* 대비 증가
- **2025 후속:** code clones이 4배 증가

**GitHub Research (2024):** AI 사용자가 unit test 통과율 +53.2%, readability +3.62%, maintainability +2.47% **[데이터]** (https://github.blog/news-insights/research/does-github-copilot-improve-code-quality-heres-what-the-data-says/)

→ **본 책의 해석 입장:** 두 결과는 동시에 참이다. *측정 단위*가 다르다(개인 코드 품질 vs 코드베이스 churn). 본문에서 "AI는 좋다/나쁘다"의 단일 결론을 강요하지 말 것.

### 2.6 채용 시장 충격

- **글로벌 신입 채용 73.4% 감소(YoY)** — Ravio 2025 보고서 **[웹]** (https://restofworld.org/2025/engineering-graduates-ai-job-losses/)
- **빅테크 신졸 채용 3년간 50%+ 감소** — SignalFire **[웹]**
- **미국 프로그래머 고용 27.5% 감소** (2023–2025, BLS)
- **CS 졸업자 실업률 6.1%, 컴공 7.5%** (전국 청년 평균의 거의 2배)
- **Pragmatic Engineer 관찰:** "It's a very strange hiring market in tech … companies being swamped by 'fake' candidates and applications created by AI tools" — Gergely Orosz **[웹]** (https://blog.pragmaticengineer.com/tech-hiring-is-this-an-inflection-point/)
- **OpenAI의 'super junior' 실험:** 시니어가 아키텍처·전략을 설계하고, "super junior"가 AI fluency로 속도를 낸다 **[웹]**

한국:
- "신입 IT 개발자 취업난 방치 심각" — 노상범 OKKY 대표 (대선후보에 대책 마련 촉구) **[커뮤니티]** (https://www.aipostkorea.com/news/articleView.html?idxno=7849)
- 토스 기술블로그 *개발자는 AI에게 대체될 것인가*: "이제 평균적으로 하는 정도로는 변별력이 생기지 않는 시대" **[웹]**

---

## 3. 핵심 관점들 (저자별 입장)

세 진영으로 정리한다. 각 진영의 *대표 논거*를 그대로 보존한다.

### 3.1 *증폭론* — AI는 시니어를 더 강하게, 주니어는 위태롭게

대표 인물: **Addy Osmani** (Google Chrome DX), **Birgitta Böckeler** (Thoughtworks), **Steve Yegge**.

> "AI tools help experienced developers more than beginners. This seems backward — shouldn't AI democratize coding? The reality: seniors leverage AI to accelerate what they understand; juniors attempt using it to learn fundamentals, producing dramatically different results." — Addy Osmani, *The 70% Problem* **[웹]** (https://addyo.substack.com/p/the-70-problem-hard-truths-about)

**70% Problem(2024) → 80% Problem(2025) 진화:** AI가 70~80%를 빠르게 만들고, 나머지 30~20%(edge case·security·통합)가 인간의 영역으로 남는다. 시니어에게 그 30%는 처음부터 짜는 것보다 *더 느릴* 수 있다.

**두 사용자 인구:**
- **Bootstrappers (experienced):** AI 결과를 *refactor·강타입화·테스트 추가*해서 받아들임
- **Non-engineers/Juniors:** AI 결과를 *그대로* 수용 → "house of cards code — it looks complete but collapses under real-world pressure"

> "GenAI amplifies indiscriminately. When you ask it to generate code, it doesn't distinguish between good and bad." — Birgitta Böckeler, ThoughtWorks **[웹]**

### 3.2 *재정의론* — 직업의 정의 자체가 변한다

대표 인물: **Andrej Karpathy**, 토스 기술블로그 저자.

Karpathy의 Software 3.0 프레임에서, 개발자의 본질 업무가 *코드 작성*에서 *명세·검증·추상 설계*로 이동한다.

> "기술의 효과는 단기적으로 과대평가되고, 장기적으로 과소평가되는 경향이 있다." — 아마라의 법칙 (토스 기술블로그 인용) **[웹]** (https://toss.tech/article/will-ai-replace-developers)

> "개발자라는 직업이 사라지는 것은 아니지만, 우리가 머릿속에 그리고 있는 '개발자'라는 직업의 정의가 매우 유동적." — 토스 테크 **[웹]**

> "추상화는 복잡성을 없애는 게 아니라, 복잡성을 미래로 이동시키는 것. 좋은 추상화란 그 아래를 몰라도 되게 해주는 것이지만, 좋은 엔지니어란 자신이 어떤 복잡성 위에 서 있는지 아는 사람." — 토스 테크 **[웹]**

### 3.3 *회의론* — 데이터는 다르게 말한다

대표 자료: **METR 2025**, **GitClear 2024–25**, **Stack Overflow Trust 데이터**.

> "Developers expected AI to speed them up by 24% but experienced slowdown. Even after the study, they still believed AI had sped them up by 20%." — METR **[데이터]**

> "AI-driven confidence often comes at the expense of critical thinking." — Microsoft 연구, ThoughtWorks Tech Radar에서 인용 **[웹]** (https://www.thoughtworks.com/en-us/radar/techniques/complacency-with-ai-generated-code)

> "Vibe coding has turned senior devs into 'AI babysitters'." — TechCrunch / HN 토론 헤드라인 **[커뮤니티]** (https://news.ycombinator.com/item?id=45242788)

### 3.4 *중도/실용론* — Vibe Engineering으로 가자

대표 인물: **Simon Willison**, **Martin Fowler**, **Birgitta Böckeler**.

핵심 입장: AI 코딩은 *어렵다*. 시니어 수준의 모든 좋은 습관이 *더* 요구된다.

> "One of the lesser spoken truths of working productively with LLMs as a software engineer on non-toy-projects is that it's *difficult* … If you're going to really exploit the capabilities of these new tools, you need to be operating *at the top of your game*." — Simon Willison **[웹]**

> "AI tools **amplify existing expertise**. The more skills and experience you have as a software engineer the faster and better the results you can get from working with LLMs." — Simon Willison **[웹]**

> "To work effectively with agentic coding assistants, Birgitta Böckeler found she needs to intervene, correct and steer all the time." — Martin Fowler 소개글 **[웹]** (https://martinfowler.com/articles/exploring-gen-ai.html, https://x.com/martinfowler/status/1904553012296659296)

### 3.5 충돌 지점 (보존)

| 충돌 | 진영 A | 진영 B |
|------|------|------|
| **개인 생산성** | AI가 21% task 증가 (DORA) | AI 사용 시 19% 더 느림 (METR) |
| **코드 품질** | readability +3.62%, test 통과 +53% (GitHub) | code churn 2배, clones 4배 (GitClear) |
| **신입에게 도움?** | "주니어가 시니어가 되는 속도 단축" (Quinn Slack via Pragmatic Engineer) | "House of cards code … unemployable pseudo-developers" (HN consensus) |
| **민주화?** | "Vibe coding raises the floor" (Karpathy) | "AI helps experienced developers more than beginners" (Osmani) |

본문에서는 두 결과를 *동시에 참*으로 다루며, 측정 단위·관점 차이로 설명한다.

---

## 4. 실증 연구 발견 (논문 기반)

### 4.1 시스템적 문헌 리뷰

**Wang et al. (2025), *The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study*** — arXiv:2507.03156 **[논문]** (https://arxiv.org/abs/2507.03156)

- **N:** 2014–2024년 peer-reviewed 37편 종합
- **이득 카테고리:** task 시작 부담 감소, code search 최소화, 보조 작업 자동화
- **위험 카테고리 5종 (그대로 인용 가능):**
  1. limit code quality
  2. fail to meet requirements
  3. **promote over-reliance and cognitive offloading**
  4. reduce team collaboration
  5. disrupt the flow
- **공식 발언:** "Survey respondents express concerns about overreliance, reporting *diminished ability to think independently*."

### 4.2 인지적 부채 (Your Brain on ChatGPT)

**Kosmyna et al. (2025), *Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task*** — MIT Media Lab, arXiv:2506.08872 **[논문]** (https://www.media.mit.edu/publications/your-brain-on-chatgpt/)

- **N:** 54명 (LLM / Search / Brain-only 3그룹), EEG·NLP·인간 채점·AI 채점 다중 측정
- **결과:**
  - LLM 그룹 brain connectivity **−55%** vs Brain-only
  - LLM 그룹 **78%가 자기 글의 한 구절도 인용 못함**
  - 자기 글에 대한 *소유감*이 LLM군에서 최저
  - 4개월 추적 시 LLM 그룹 *지속적 저성과*
- **저자 용어:** "cognitive debt" — 단기 노력 절약, 장기 critical thinking 손실

이 연구는 essay writing이지만, 코딩에도 유사 메커니즘이 작동한다는 가설을 깔아주는 *책 본문의 토대 인용*.

### 4.3 인지 편향 분류 (LLM-Assisted Coding 전용)

**Cognitive Biases in LLM-Assisted Software Development** — arXiv:2601.08045 **[논문]**

- **N:** 14명 observational + 22명 survey
- **분류:** 15개 cognitive bias 카테고리 (인지심리학자 검증)
- **핵심 수치:**
  - 프로그래머 행동의 **48.8%가 편향됨**
  - 개발자-LLM 상호작용이 **편향 행동의 56.4%** 차지
- **저자 주장:** AI가 프로그래밍을 *generative*(만드는)에서 *evaluative*(평가하는) 활동으로 변환시킨다

### 4.4 자동화 보안주의 (automation complacency)

- **고전 결과 재확인:** 자동화가 *일관되게* 신뢰할 만하면 운영자는 자동화 오류의 약 30%만 감지. *가끔* 가시적으로 실패할 때 감지율 75%로 상승 — 즉 AI가 *너무 잘하면* 검토 능력이 마비된다 **[논문/리뷰]** (Springer, 2025: *Exploring automation bias in human–AI collaboration*, https://link.springer.com/article/10.1007/s00146-025-02422-7)
- **앵커링:** 첫 AI 추천이 후속 결정을 끌어당김. 인간이 *먼저* 평가하고 *나중에* AI를 보면 효과 완화
- **개입:** verification effort를 *명시적으로* 증가시키면 complacency 감소

### 4.5 프로그래밍 교육 — 초보자와 LLM

- **Code-tracing with ChatGPT (Kazemitabaar et al., 2025 ACM ICER)** **[논문]** (https://dl.acm.org/doi/10.1145/3702652.3744207)
- **메타 발견:** "over-reliance on ChatGPT occurred in approximately 55% of cases and reached up to 95% for about one-third of the students"
- **저-사전지식 학습자에서 학습 손실 큼:** "may have lacked the meta-cognitive skills needed to use it effectively"
- **illusion of understanding:** "students believe they have grasped a concept simply because they can produce working solutions with AI"
- **개입 효과:** Socratic questioning 방식 가드레일이 의존 감소 효과

### 4.6 코드 품질·속도 트레이드오프

**Speed at the Cost of Quality? The Impact of LLM Agent Assistance on Software Development** — arXiv:2511.04427 **[논문]**

LLM agent가 속도 증가 / 품질·유지보수성 감소 트레이드오프를 보임. AI agent 생성 PR이 *더 크다* → 리뷰가 *더 어렵다*.

### 4.7 SPACE Framework의 AI 시대 응용

- **원전:** Forsgren et al., *ACM Queue* 2021 — SPACE(Satisfaction/Performance/Activity/Communication/Efficiency) **[논문]**
- **2025 응용:** AI 시대에는 "activity"(코드 라인 수, PR 수) 증가가 *automatic productivity*가 아니라는 점을 강조. SPACE는 **DX(Developer Experience)**, **flow**, **satisfaction**을 함께 보라고 요구 **[웹]** (https://blog.codacy.com/space-framework)

### 4.8 Code Review with LLM

**Rethinking Code Review Workflows with LLM Assistance: An Empirical Study** — arXiv:2505.16339 **[논문]**

리뷰어가 AI 생성 PR을 다룰 때:
- 리뷰 시간 증가
- 인지 부하 패턴 변화
- 리뷰어가 *작성자보다 책임*을 더 느끼는 비대칭

---

## 5. 단계별 시나리오 — 학생·신입 / 주니어·시니어 / CTO

### 5.1 학생 / 신입 개발자

**진단:**
- *Stack Overflow 2025*: 44%가 AI를 *학습 중* 사용. AI 학습 의존도 가장 높음.
- *Kazemitabaar et al.*: 사전지식 낮을수록 의존이 학습을 *해친다*. 의존율 최대 95%.
- *MIT cognitive debt*: 단기 essay 도움 vs 4개월 후 저성과.

**커뮤니티 목소리:**

> "Vibe coding isn't teaching them to be engineers, it's training them to be 'code assemblers' — people who can prompt a system but cannot read, reason about, or repair the code it produces." **[커뮤니티]** (Data Science Collective on Medium / HN)

> "코딩이 쉬워지면서 오히려 코딩을 더 잘할 수 있게 하는 기회와 환경을 AI에게 빼앗기고 있는 중입니다." — velog *AI 시대의 개발자: 현업 개발자의 솔직한 이야기* (테오) **[커뮤니티]**

**전형적 실패담:** "AI 답을 받아서 잘 돌아가는데, 디버깅 단계에서 자기가 짠 게 아니라 *읽을 줄도 모름*. 시니어 리뷰 때 '왜 이렇게 했어?' 질문에 답할 수 없음." (HN, r/ExperiencedDevs 다수)

**구조 충격:** 신입 채용 73.4% 감소(2025), CS 졸업자 실업 6.1%, 미국 프로그래머 고용 27.5% 감소. "신입이 들어갈 자리 자체가 사라진다"는 mentorship crisis.

> "The traditional software apprenticeship model — where junior developers gradually build expertise through hands-on struggle under senior mentorship — is breaking down, as AI coding assistants automate the struggle that builds deep knowledge." **[커뮤니티/웹]** (SoftwareSeni)

### 5.2 주니어 (1~5년차)

**진단:**
- METR caveats에 따르면 *덜 숙련된 개발자*는 AI로 *빠를 수 있다* — 단, *익숙한 코드베이스가 아닐 경우*에 한해.
- Quinn Slack(Sourcegraph CEO) via Pragmatic Engineer: "I see the new grad engineers being way more fluent using AI when coding than senior engineers." **[웹]**
- *Hacker News:* "Senior engineers with 3+ years of experience reported 40–50% productivity gains when using AI tools, while junior engineers saw only 15–25% improvements" **[커뮤니티]**

**핵심 위험:** AI fluency가 *깊이의 환상*을 만든다. fundamentals 없이 빨라지면, 시니어로 가는 길이 끊긴다.

**커뮤니티 처방:**
- **"먼저 직접 풀고 나중에 비교"** (HN, r/ExperiencedDevs 자주 등장)
- **"AI 코드 라인별로 *왜* 그렇게 짰는지 LLM에 다시 물어라"** — Claude/Cursor를 *튜터*로 사용 **[웹]** (https://medium.com/@unicodeveloper/10-must-have-skills-for-claude-and-any-coding-agent-in-2026, https://www.howtogeek.com/i-transformed-claude-into-the-ultimate-coding-tutor/)
- **"AI 코드를 *내 언어로* 다시 짜라"** — refactor가 학습이 된다

### 5.3 시니어 (6년차 이상)

**진단:**
- METR: AI 사용 시 19% *느려짐* — *익숙한 큰 코드베이스, 짧은 학습시간* 조건에서.
- Osmani: 마지막 30%는 *처음부터 짜는 것보다 느릴 수 있다*.
- Willison/Böckeler: AI가 시니어 스킬(테스트·아키텍처·리뷰)을 *더* 요구한다.

**역할 변화:**
- "AI babysitter" — AI가 만든 코드 검토·교정 작업의 비중 증가
- *Coding agent orchestrator* (Yegge): AI agent를 *지휘*하는 위치
- **"PR이 더 크고, 리뷰 시간 91% 증가"** — DORA 2025

**커뮤니티 처방 — 시니어의 새 스킬:**
1. **AI에 위임할 작업과 직접 할 작업의 경계 판단** (Willison: "judgment about what can be outsourced")
2. **CLAUDE.md / .cursorrules — 프로젝트 컨텍스트 문서화**
3. **planning phase 강제** ("write your own plan first")
4. **자동화 테스트가 단순 좋은 습관에서 *전제조건*으로 격상**
5. **자신의 추상화 위/아래를 인지** — 토스: "좋은 엔지니어란 자신이 어떤 복잡성 위에 서 있는지 아는 사람"

### 5.4 CTO / 테크 리더

**진단:**
- DORA: AI는 *증폭기*. 약한 조직은 더 약해진다.
- if(kakao)25, 우아한형제들·SK플래닛 사례: 한국 빅테크가 유료 Copilot 구독 *전사 지원*을 표준화하는 흐름 **[웹]** (https://techblog.woowahan.com/21240/, https://techtopic.skplanet.com/github-copilot/)
- 채용 시장: 시니어 부족 + 신입 채용 붕괴 → mentorship pipeline 단절

**고려해야 할 의사결정:**

| 결정 | 옵션 A | 옵션 B |
|------|------|------|
| **도구 표준화** | 전사 1종 통일(Cursor or Claude Code) | 개인 선택 + 가드레일 |
| **신입 학습 정책** | AI 사용 제한(첫 3개월) | 자유 사용 + Socratic 리뷰 강제 |
| **코드 리뷰 룰** | AI 생성 명시 라벨 의무 | 무차별, 리뷰 표준만 강화 |
| **측정** | 코드 라인·PR 속도 추적 | DORA/SPACE 다축 측정 |

**우아한형제들의 운영 인사이트:**
> "코파일럿의 역할은 개발자를 대신하는 게 아니라 서포터에 가깝습니다. 잘 활용한다면, 단순 반복 작업은 줄이고 좀 더 중요한 문제를 해결하는 데 집중할 수 있는 여유를 얻을 수 있습니다." **[웹]** (techblog.woowahan.com/21240/)

**Böckeler/Thoughtworks 권고:**
> "Strongly caution against using [vibe coding] for production code. Reinforce established practices such as TDD and static analysis, and embed them directly into coding workflows … Develop a good mental framework about where and when not to use and trust AI." **[웹]** (https://www.thoughtworks.com/en-us/radar/techniques/complacency-with-ai-generated-code)

---

## 6. 학습 이론과의 접점

본 책의 무게중심은 *방법론*이 아닌 *학습 이론*에 둘 수 있다. 이론적 토대 후보:

### 6.1 Deliberate Practice (Ericsson)

- **핵심:** 명확한 목표 → 하위 스킬 분해 → 의도적 반복 → 전문가 피드백 → 교정 **[웹]** (https://fs.blog/deliberate-practice-guide/)
- **Mental representation:** Ericsson은 *멘탈 표상*을 전문성의 핵심 빌딩 블록으로 봄. "Deliberate practice both produces and depends on effective mental representations."

**AI 시대 적용 가설:** AI가 *바로 정답*을 줄 때, deliberate practice의 *struggle* 단계가 사라진다 → mental representation이 형성되지 않는다. (Your Brain on ChatGPT의 EEG 결과와 정합.)

### 6.2 Zone of Proximal Development (Vygotsky)

- **ZPD:** 혼자 못하지만 *More Knowledgeable Other (MKO)의 도움으로 가능한 영역* **[웹]** (https://www.simplypsychology.org/zone-of-proximal-development.html)
- **Scaffolding:** MKO의 *임시* 지원. *점진적으로 제거*되어야 학습자가 자립

**AI = MKO 가설:** AI가 MKO 역할을 한다. 단 핵심 조건은 **scaffolding이 제거되는가**. 영구히 남는 scaffolding은 ZPD를 *늘리는* 게 아니라 *대체*한다.

> "Generative AI significantly expands students' Zone of Proximal Development (ZPD) by **permanently scaffolding** procedural tasks and enabling earlier engagement with higher-order cognitive activities." — Sidorkin, *Leapfrogging Effect Hypothesis* **[논문]** (https://papers.ssrn.com/sol3/Delivery.cfm?abstractid=5230565)

→ 본 책은 *permanent scaffolding*이 좋은가 나쁜가의 질문을 정면으로 다룰 수 있다.

### 6.3 Bloom's / SOLO Taxonomy

- **Bloom:** Remember → Understand → Apply → Analyze → Evaluate → Create
- **AI 사용 단계 매핑(책 자체 제안 후보):**
  - L1: AI에 통째로 위임 → Remember/Apply 수준에 멈춤
  - L2: AI 출력을 *읽고 수정* → Analyze
  - L3: AI에 *어떤 패턴*을 *왜* 적용했는지 다시 묻고 비교 → Evaluate
  - L4: AI를 *튜터로 활용*해 새 영역 탐색 → Create

### 6.4 Cognitive Load Theory (Sweller)

- **3종 부하:** intrinsic(과제 자체) + extraneous(전달 방식) + germane(스키마 형성)
- **AI의 효과:** *extraneous* 부하를 줄임 (보일러플레이트, lookup). *intrinsic*은 그대로. *germane*은 *감소* (스키마 형성 기회 박탈)
- **시사:** AI가 줄여주는 부하가 *어느 종류*인지 구분해야 한다

### 6.5 Acquisition vs Performance (Schmidt & Bjork)

학습 심리학의 고전: *수행이 좋아지는 것*과 *학습이 일어나는 것*은 다르다. AI가 *수행*은 즉시 높이지만 *학습*은 차단할 수 있다. METR의 "성능 +20% 느낌 / 실제 -19%"가 이 프레임에서 잘 설명된다.

---

## 7. 실무 노하우 — 커뮤니티와 도구 가이드에서 정제

### 7.1 학습 보호 패턴 ("AI 쓰면서 학습하기")

| # | 패턴 | 출처 |
|---|------|------|
| 1 | **먼저 혼자 푼다, 그다음에만 AI와 비교한다** | HN, r/ExperiencedDevs 다수 |
| 2 | **AI 코드를 *내 손으로 다시 쓰는* refactor 단계** | r/learnprogramming |
| 3 | **AI에 *왜* 그 패턴을 골랐는지 다시 묻는다 (Socratic 자가 강제)** | Coursera Claude Code, Frontend Masters |
| 4 | **AI 답을 *의심하는 가설*부터 세운다** ("이게 틀렸을 가능성은?") | Böckeler |
| 5 | **테스트를 *먼저* 쓴다 (TDD-first with agents)** | Willison "vibe engineering" |
| 6 | **AI 답을 *문서로* 정리해 코드에 주석 추가** | velog 패턴 |
| 7 | **CLAUDE.md / .cursorrules로 *팀의 mental model*을 코드 옆에 둔다** | Anthropic 공식 가이드 |
| 8 | **AI 사용 시간을 *기록*해 self-METR** | METR 권고 응용 |

### 7.2 도구별 정착 사례 (한국)

- **우아한형제들:** 전사 Copilot 구독 + `.github/copilot-instructions.md` 패턴 + 두 단계 검증(컨텍스트 충분성 + 결과 타당성) **[웹]** (https://techblog.woowahan.com/21240/)
- **SK플래닛:** Copilot 활용기 시리즈 (생산성 향상 vs 학습 보호의 균형) **[웹]** (https://techtopic.skplanet.com/github-copilot/)
- **토스:** *개발자는 AI에게 대체될 것인가* — "위임 가능"이 아닌 "위임해야 하는가"의 윤리적 판단 강조 **[웹]**

### 7.3 "AI를 튜터로 쓰기" 구체 워크플로 (시니어/주니어 공통)

도구 문서·실무자 가이드의 합의:
1. **Read-only mode부터 시작** — agent가 실행 권한 없이 *설명*만
2. **CLAUDE.md를 *반드시 작성*** — 프로젝트 컨벤션, 도메인 용어, 'do not'
3. **Plan-first** — "계획 짜고 보여줘. 코드는 내가 OK 한 다음에"
4. **에러는 LLM에 던지기 전에 *내가 가설* 적기**
5. **diff를 *한 hunk씩* 검토** (vibe accept 금지)

(출처: Anthropic 공식 Claude Code 가이드, builder.io, datacamp, Frontend Masters)

### 7.4 시니어가 AI에 위임 *가능한* 일 vs 위임 *불가* 일

토스 글의 윤리적 구분에 데이터 진영의 권고를 합쳐:

| 위임 가능 | 위임 불가 |
|---------|---------|
| 보일러플레이트, CRUD | 아키텍처 의사결정 |
| 단위 테스트 케이스 생성 | 보안·인증·권한 설계 |
| 문서·주석 초안 | 1:1 멘토링 |
| 코드 검색·grep 대체 | 최종 채용·평가 판단 |
| 마이그레이션 스크립트 | 팀 문화·코드 표준 설계 |
| 단순 리팩토링 후보 제안 | "왜" 질문에 대한 책임 답변 |

---

## 8. 논쟁점·미해결 질문

본 책에서 *정답을 강요하지 말고* 보존해야 할 토론들:

### 8.1 신입은 AI를 *써야 하나, 막아야 하나*

- **써야 한다:** Stack Overflow Survey의 44% 학습자가 이미 사용. 막을 수 없다. ZPD 확장의 기회.
- **막아야 한다:** Kazemitabaar 등의 over-reliance 95% 데이터, MIT cognitive debt 결과.
- **중도:** "처음 3개월 fundamentals만, 이후 AI 허용 + Socratic 리뷰 강제"

### 8.2 AI는 *민주화*인가 *전문가 가속*인가

- Karpathy: "Vibe coding **raises the floor**." (민주화)
- Osmani: "AI helps experienced developers **more than beginners**." (전문가 가속)
- 데이터: 동시에 참 — *진입*은 쉬워지고, *상위 수준 도달*은 더 어려워지는 양극화

### 8.3 측정 단위 — 누구의 생산성을 측정하나

- 개인 라인/PR (GitHub, McKinsey) vs 조직 throughput/stability (DORA) vs 시간 측정 (METR) vs 자기보고 (Stack Overflow)
- 같은 사람이 *어느 척도에서 +20%, 다른 척도에서 -19%*

### 8.4 "이해 없이 잘 돌아가면 된다"는 입장의 윤리

- Karpathy 원전: "forget that the code even exists"
- Willison 반박: production code에서는 "you've reviewed, tested, and understood it all" 필요
- 토스: "위임 가능"과 "위임해야 하는가"는 별개

### 8.5 영구 scaffolding(AI 의존)은 새 정상인가 atrophy인가

- Sidorkin: ZPD를 영구히 확장 — 긍정적 패러다임 전환
- MIT cognitive debt + GitClear churn 데이터: 영구 의존이 *역량 자체*를 침식
- 미해결: 종단 연구(5년+) 부재

### 8.6 사회 구조 — mentorship pipeline은 어떻게 복구되나

신입 채용 73% 감소 + 시니어가 AI babysitter화 → "다음 세대 시니어는 어디서 나오나?" — 산업 차원의 미해결 질문. 본 책의 *CTO 챕터*가 정면 응답할 후보.

---

## 9. 인용·근거 문장 라이브러리 (본문 직접 사용 가능)

### 9.1 원전 핵심 인용

1. **Karpathy(2025-02-02 트윗):**
   "There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists."

2. **Willison(Vibe Engineering):**
   "If an LLM wrote every line of your code, but you've reviewed, tested, and understood it all, that's not vibe coding in my book — that's using an LLM as a typing assistant."

3. **Willison(같은 글):**
   "AI tools amplify existing expertise. The more skills and experience you have as a software engineer the faster and better the results you can get from working with LLMs."

4. **Willison(같은 글, *어려움* 강조):**
   "One of the lesser spoken truths of working productively with LLMs … is that it's difficult … you need to be operating at the top of your game."

5. **Osmani(70% Problem):**
   "AI tools help experienced developers more than beginners. This seems backward — shouldn't AI democratize coding?"

6. **Osmani(70% Problem):**
   "House of cards code — it looks complete but collapses under real-world pressure."

7. **Böckeler(via Fowler):**
   "To work effectively with agentic coding assistants, … intervene, correct and steer all the time."

8. **Böckeler:**
   "GenAI amplifies indiscriminately. When you ask it to generate code, it doesn't distinguish between good and bad."

9. **ThoughtWorks Tech Radar:**
   "AI-driven confidence often comes at the expense of critical thinking."

10. **DORA 2025:**
    "AI is fundamentally an amplifier, not a solution."

11. **METR(2025):**
    "Developers thought AI made them faster. The data said otherwise."

12. **Stack Overflow 2025:**
    "Developers Lean on AI More, But Report Growing Doubts About Accuracy."

### 9.2 한국어 핵심 인용

1. **토스 테크 *개발자는 AI에게 대체될 것인가*:**
   "개발자라는 직업이 사라지는 것은 아니지만, 우리가 머릿속에 그리고 있는 '개발자'라는 직업의 정의가 매우 유동적이다."

2. **토스 테크:**
   "추상화는 복잡성을 없애는 게 아니라, 복잡성을 미래로 이동시키는 것. 좋은 추상화란 그 아래를 몰라도 되게 해주는 것이지만, 좋은 엔지니어란 자신이 어떤 복잡성 위에 서 있는지 아는 사람이다."

3. **토스 테크:**
   "이제 평균적으로 하는 정도로는 변별력이 생기지 않는 시대가 되었다."

4. **velog *AI 시대의 개발자* (테오):**
   "코딩이 쉬워지면서 오히려 코딩을 더 잘할 수 있게 하는 기회와 환경을 AI에게 빼앗기고 있는 중이다."

5. **velog 테오:**
   "인간의 모호하고 막연한 요구사항을 컴퓨터가 해결할 수 있는 문제로 재정의하고 책임지는 것."

6. **velog 테오:**
   "내가 원하는 구체적인 목표와 그림이 머릿속에 있고, AI에게 명확히 지시하며 결과를 비판적으로 검토해야 한다."

7. **우아한형제들 기술블로그:**
   "코파일럿의 역할은 개발자를 대신하는 게 아니라 서포터에 가깝다."

8. **우아한형제들 기술블로그:**
   "의심 없이 코파일럿의 제안을 받아들이다 보면 잘못된 코드 조각이 코드베이스에 추가되는 불상사가 발생하기 십상이다."

### 9.3 강한 통계 숫자 (책 본문에 그대로 인용 가능)

- METR: AI 사용 시 **19% 느려짐** vs 본인 인식 **20% 빠름** (격차 ~40%p)
- Stack Overflow 2025: AI 도구 사용 **84%**, AI 정확성 신뢰 **29%** (전년 40% 대비 ↓)
- MIT Brain on ChatGPT: LLM 사용군 brain connectivity **-55%**, 자기 글 인용 실패 **78%**
- DORA 2025: AI 사용 시 task **+21%**, PR merge **+98%**, 단 안정성 ↓·change failure rate ↑
- Cognitive Biases 논문: 개발자 행동의 **48.8%가 편향**, LLM 상호작용이 편향의 **56.4%**
- 70% Problem: AI가 70% 작성, 나머지 30%가 *처음부터 짜는 것만큼* 시간 소요
- 신입 채용 **-73.4%** YoY (Ravio), 미국 프로그래머 고용 **-27.5%** (BLS, 2023-25)
- ICER 2025: 학생의 over-reliance **55% 평균, 상위 1/3은 95%**
- GitClear: code clone **4배** 증가 (2021 → 2025)

### 9.4 한국 사례 통계

- 한국 AI 코딩 도구 시장 수백억 원 규모, 빅테크 중심 파일럿 → 확산 단계 (CIO Korea)
- if(kakao)25 (2025-09-23~25), 우아한형제들·SK플래닛·토스 등 사내 AI 코딩 도구 도입 표준화 흐름

---

## 10. 참고문헌

### 원전 — 개념·관점

- Karpathy, A. (2025-02-02). *Vibe coding* [Tweet]. X. https://x.com/karpathy/status/1886192184808149383
- Karpathy, A. (2025–2026). *Software 3.0* talks / *Vibe Coding Was Just the Warmup*. https://app.dealroom.co/news/note/vibe-coding-was-just-the-warmup-andrej-karpathy-on-the-dawn-of-software-3-0
- Willison, S. (2025). *Vibe engineering*. Simon Willison's Newsletter. https://simonw.substack.com/p/vibe-engineering
- Willison, S. (2025). *Not all AI-assisted programming is vibe coding*. https://simonw.substack.com/p/not-all-ai-assisted-programming-is
- Willison, S. (2025-12-31). *2025: The year in LLMs*. https://simonwillison.net/2025/Dec/31/the-year-in-llms/
- Willison, S. (2025-07-12). Commentary on METR study. https://simonwillison.net/2025/Jul/12/ai-open-source-productivity/
- Osmani, A. (2024). *The 70% Problem: Hard Truths About AI-Assisted Coding*. https://addyo.substack.com/p/the-70-problem-hard-truths-about
- Osmani, A. (2025). *The 80% Problem in Agentic Coding*. https://addyo.substack.com/p/the-80-problem-in-agentic-coding
- Osmani, A. (2025). *AI-Assisted Engineering: My 2025 Substack Recap*. https://addyosmani.com/blog/ai-assisted-engineering/
- Osmani, A. *AI's 70% Problem* [Zed Blog]. https://zed.dev/blog/ai-70-problem-addy-osmani
- Böckeler, B. & Fowler, M. (continuing series). *Exploring Generative AI*. https://martinfowler.com/articles/exploring-gen-ai.html
- Fowler, M. (2025). *How far can we push AI autonomy in code generation?* https://martinfowler.com/articles/pushing-ai-autonomy.html
- Yegge, S. *The Future of Coding Agents* / *Vibe Coding* (book). LinkedIn post: https://www.linkedin.com/posts/steveyegge_the-future-of-coding-agents-activity-7413768559492952064-6tIE
- Orosz, G. (2025). *The Pragmatic Engineer in 2025*. https://newsletter.pragmaticengineer.com/p/the-pragmatic-engineer-in-2025
- Orosz, G. (2025). *Tech hiring: is this an inflection point?* https://blog.pragmaticengineer.com/tech-hiring-is-this-an-inflection-point/

### 정량 보고서 / 데이터

- METR. (2025-07-10). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*. https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ (arXiv:2507.09089, https://arxiv.org/abs/2507.09089)
- METR. (2026-02-24). *We are Changing our Developer Productivity Experiment Design*. https://metr.org/blog/2026-02-24-uplift-update/
- DORA / Google Cloud. (2025). *State of AI-assisted Software Development*. https://dora.dev/research/2025/dora-report/
- Stack Overflow. (2025). *2025 Developer Survey: AI*. https://survey.stackoverflow.co/2025/ai
- Stack Overflow. (2024). *2024 Developer Survey: AI*. https://survey.stackoverflow.co/2024/ai
- Stack Overflow. (2025-12-29). *Developers remain willing but reluctant to use AI*. https://stackoverflow.blog/2025/12/29/developers-remain-willing-but-reluctant-to-use-ai-the-2025-developer-survey-results-are-here/
- Stack Overflow Press. (2025). *Trust in AI at an All Time Low*. https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/
- Stack Overflow Blog. (2025-12-26). *AI vs Gen Z*. https://stackoverflow.blog/2025/12/26/ai-vs-gen-z/
- GitClear. (2024). *Coding on Copilot: Data Suggests Downward Pressure on Code Quality*. https://www.gitclear.com/coding_on_copilot_data_shows_ais_downward_pressure_on_code_quality
- GitClear. (2025). *AI Copilot Code Quality 2025: 4x Growth in Code Clones*. https://www.gitclear.com/ai_assistant_code_quality_2025_research
- GitHub. (2024). *Does GitHub Copilot improve code quality?* https://github.blog/news-insights/research/does-github-copilot-improve-code-quality-heres-what-the-data-says/

### 학술 논문

- Wang et al. (2025). *The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study*. arXiv:2507.03156. https://arxiv.org/abs/2507.03156
- Kosmyna et al. (2025). *Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task*. arXiv:2506.08872. https://www.media.mit.edu/publications/your-brain-on-chatgpt/
- *Cognitive Biases in LLM-Assisted Software Development*. arXiv:2601.08045. https://arxiv.org/html/2601.08045v1
- *Speed at the Cost of Quality? The Impact of LLM Agent Assistance on Software Development*. arXiv:2511.04427. https://arxiv.org/html/2511.04427v1
- *Rethinking Code Review Workflows with LLM Assistance: An Empirical Study*. arXiv:2505.16339. https://arxiv.org/pdf/2505.16339
- *Relying on LLMs: Student Practices and Instructor Norms are Changing in Computer Science Education*. arXiv:2602.05506. https://arxiv.org/html/2602.05506v1
- *Intuition to Evidence: Measuring AI's True Impact on Developer Productivity*. arXiv:2509.19708. https://arxiv.org/html/2509.19708v1
- Kazemitabaar et al. (2025). *How Do Novice Programmers Solve Code-Tracing Problems When ChatGPT Is Available?* ACM ICER 2025. https://dl.acm.org/doi/10.1145/3702652.3744207
- *ChatGPT in Programming Education: An Empirical Study on Its Impact on Student Performance, Creativity, and Teamwork*. MDPI Education. https://www.mdpi.com/2227-7102/16/1/19
- *LLM Chatbots in High School Programming: Exploring Behaviors and Interventions*. arXiv:2511.18985. https://arxiv.org/html/2511.18985v1
- Sidorkin, A.M. *Leapfrogging Effect Hypothesis: Generative AI as a Permanent Scaffold in Higher Education*. SSRN 5230565. https://papers.ssrn.com/sol3/Delivery.cfm?abstractid=5230565
- *Exploring automation bias in human–AI collaboration*. AI & Society (Springer, 2025). https://link.springer.com/article/10.1007/s00146-025-02422-7
- Ericsson, K.A. *The Influence of Experience and Deliberate Practice on the Development of Superior Expert Performance*. https://www.ida.liu.se/~nilda08/Anders_Ericsson/Ericsson_delib_pract.pdf
- Forsgren, N. et al. (2021). *The SPACE of Developer Productivity*. ACM Queue.

### 산업 분석·블로그 (영어)

- Faros AI. (2025). *DORA Report 2025 Key Takeaways*. https://www.faros.ai/blog/key-takeaways-from-the-dora-report-2025
- Swarmia. (2025). *What the 2025 DORA report tells us about AI readiness*. https://www.swarmia.com/blog/dora-2025-report-ai-readiness/
- ThoughtWorks Tech Radar. *Complacency with AI-generated code*. https://www.thoughtworks.com/en-us/radar/techniques/complacency-with-ai-generated-code
- ThoughtWorks. *AI-first software engineering*. https://www.thoughtworks.com/perspectives/edition36-ai-first-software-engineering/article
- Atomic Robot. *AI Writes Better Code. We're Getting Worse at Reviewing It.* https://atomicrobot.com/blog/ai-review-fatigue/
- Sean Goedecke. *METR's AI productivity study is really good*. https://www.seangoedecke.com/impact-of-ai-study/
- Domenic Denicola. *My Participation in the METR AI Productivity Study*. https://domenic.me/metr-ai-productivity/
- Let's Data Science. *AI Coding Tools Made Developers 19% Slower*. https://letsdatascience.com/blog/developers-thought-ai-made-them-faster-the-data-said-otherwise
- Mike Mason. *AI Coding Agents in 2026: Coherence Through Orchestration, Not Autonomy*. https://mikemason.ca/writing/ai-coding-agents-jan-2026/
- Context Studios. *The Vibe Coding Hangover: Why Developers Are Returning to Engineering Rigor*. https://www.contextstudios.ai/blog/the-vibe-coding-hangover-why-developers-are-returning-to-engineering-rigor

### 산업 분석·블로그 (한국어)

- 토스 테크. (2025). *개발자는 AI에게 대체될 것인가*. https://toss.tech/article/will-ai-replace-developers
- 우아한형제들 기술블로그. *코파일럿 "열일"하게 만드는 방법*. https://techblog.woowahan.com/21240/
- SK플래닛. *GitHub Copilot 활용기: AI-assisted Coding과 개발 생산성 향상*. https://techtopic.skplanet.com/github-copilot/
- velog. (테오). *AI 시대의 개발자: 현업 개발자의 솔직한 이야기*. https://velog.io/@teo/ai-and-developer
- 카카오 모빌리티 Developers. *if(kakao)25 랩업과 리뷰*. https://developers.kakaomobility.com/techblogs/ifkakao-2025.html
- if(kakao)25 공식. https://if.kakao.com/2025
- AI포스트. *노상범 OKKY 대표, 신입 IT 개발자 취업난 대책 마련 촉구*. https://www.aipostkorea.com/news/articleView.html?idxno=7849
- CIO Korea. *AI가 만든 코드, 실전에 투입하려면 왜 이렇게 어려울까?* https://www.cio.com/article/3995481/
- CIO Korea. *직접 써본 AI 코딩 도구 12종*. https://www.cio.com/article/4030150/
- 한컴테크. *AI 코딩 어시스턴트 도입을 위한 완벽 가이드*. https://tech.hancom.com/ai-coding-assistant-guide/

### 커뮤니티 토론

- Hacker News. *How AI Vibe Coding Is Destroying Junior Developers' Careers*. https://news.ycombinator.com/item?id=44593397
- Hacker News. *Vibe coding has turned senior devs into 'AI babysitters'*. https://news.ycombinator.com/item?id=45242788
- Hacker News. *AI is making junior devs useless*. https://news.ycombinator.com/item?id=47206663
- Hacker News. *Vibe coding is a real job now*. https://news.ycombinator.com/item?id=47401666
- TechCrunch. (2025-09-14). *Vibe coding has turned senior devs into 'AI babysitters,' but they say it's worth it*. https://techcrunch.com/2025/09/14/vibe-coding-has-turned-senior-devs-into-ai-babysitters-but-they-say-its-worth-it/
- TechSpot. *Forced to vibe code at work, programmers say their skills are deteriorating*. https://www.techspot.com/news/112415-forced-vibe-code-work-programmers-their-skills-deteriorating.html
- Data Science Collective (Medium). *The Vibe Coding Trap: Why AI Shortcuts Hurt Junior Devs*. https://medium.com/data-science-collective/the-silent-career-killer-how-vibe-coding-is-creating-a-generation-of-unemployable-developers-459fc9431f92
- The New Stack. *AI and Vibe Coding Are Radically Impacting Senior Devs in Code Review*. https://thenewstack.io/ai-and-vibe-coding-are-radically-impacting-senior-devs-in-code-review/
- SoftwareSeni. *Junior Developers in the Age of AI — Who Trains the Next Generation of Engineers*. https://www.softwareseni.com/junior-developers-in-the-age-of-ai-who-trains-the-next-generation-of-engineers/
- Rest of World. *AI is wiping out entry-level tech jobs, leaving graduates stranded*. https://restofworld.org/2025/engineering-graduates-ai-job-losses/
- IEEE Spectrum. *AI Shifts Expectations for Entry Level Jobs*. https://spectrum.ieee.org/ai-effect-entry-level-jobs

### 도구 가이드 (실무 패턴 출처)

- Builder.io. *How I use Claude Code (+ my best tips)*. https://www.builder.io/blog/claude-code
- DataCamp. *Claude Code in Cursor: Setup and Workflow Guide*. https://www.datacamp.com/tutorial/claude-code-in-cursor
- Frontend Masters. *Cursor & Claude Code | Pro AI*. https://frontendmasters.com/courses/pro-ai/
- ChatPRD. *Claude Skills Explained*. https://www.chatprd.ai/how-i-ai/claude-skills-explained
- The Excited Engineer. *Your Best AI Coding Guide with Claude Code and Cursor*. https://theexcitedengineer.substack.com/p/your-best-ai-coding-guide-with-claude
- Coursera. *Claude Code: Software Engineering with Generative AI Agents*. https://www.coursera.org/learn/claude-code

### 학습 이론 보조

- Simply Psychology. *Zone of Proximal Development*. https://www.simplypsychology.org/zone-of-proximal-development.html
- Farnam Street. *The Ultimate Deliberate Practice Guide*. https://fs.blog/deliberate-practice-guide/
- Codacy. *SPACE Framework: How to Measure Developer Productivity*. https://blog.codacy.com/space-framework

---

## 7. 리서치 한계 (커버하지 못한 영역)

본 리서치가 *덜* 단단한 영역을 솔직히 기재한다. 본문 집필 시 추가 1차 자료 수집을 권한다.

### 보강이 필요한 영역

1. **한국 빅테크의 *내부 데이터* 부재**
   - 카카오·네이버·라인·쿠팡·당근의 사내 AI 도입 *전후* 정량 측정은 공개 자료가 거의 없다. 우아한형제들·SK플래닛·토스만 일부 공개. *if(kakao)25*에서 발표된 세션의 실제 영상·슬라이드는 직접 확인하지 않음.
   - **권고:** 챕터 집필 단계에서 if(kakao)25 YouTube playlist (https://www.youtube.com/playlist?list=PLyraqdoIVJhmCIlhXAYjZwqwxT5Ih1kBG)에서 관련 세션 1~2개 직접 시청 후 보강.

2. **한국 커뮤니티 1인칭 원문 부족**
   - OKKY·velog·인프런 댓글의 *생생한 인용*이 영문 HN/Reddit만큼 두껍게 모이지 않았다. 검색 엔진이 OKKY 본문을 잘 못 가져온다.
   - **권고:** 챕터 집필 단계에서 OKKY 직접 사이트 검색(키워드: "AI 코딩", "Cursor", "Copilot", "신입") 1~2시간 추가.

3. **종단(longitudinal) 데이터 부재**
   - MIT cognitive debt는 4개월, METR은 단발성. AI 의존이 *5년 후* 시니어 역량에 미치는 영향을 보여줄 데이터는 *아직 세상에 없다*. 이는 본 책이 *가설*로 다뤄야 할 영역.

4. **Birgitta Böckeler의 개별 memo 본문 미수집**
   - *Exploring Gen AI* 시리즈의 index 페이지만 확인. 개별 글(*"I still care about the code"*, *"How to tackle unreliability"* 등) 본문 인용은 직접 확보 못함.
   - **권고:** Fowler 사이트 개별 글 직접 페치 / 검색 보강.

5. **DORA 2025 PDF 원문**
   - 요약·정리 글에서 인용했지만 PDF 원문의 page 수준 인용은 미확보.
   - **권고:** https://dora.dev/research/2025/dora-report/ 의 PDF 다운로드 후 page 인용.

6. **Cognitive Biases in LLM-Assisted Software Development의 15개 bias 목록**
   - 논문 abstract만 확보. 본문의 15개 bias 카테고리 *이름*은 미확인.
   - **권고:** arXiv:2601.08045 PDF 페치.

7. **Hacker News 원문 댓글 (HN 페이지가 429로 차단)**
   - 챕터 오프닝에 쓸 *1인칭 생생한 인용*은 본 리서치에서 직접 수집 못함. WebSearch가 요약한 헤드라인만 확보.
   - **권고:** HN Algolia 검색(https://hn.algolia.com)으로 *재방문*해서 댓글 직접 인용 5~10개 모으기.

8. **GitHub Octoverse 2024/2025**
   - 본 리서치에서 직접 확인 못함. AI 사용 통계의 또 다른 1차 출처.

### 본 리서치가 *제대로 커버한* 영역 (참고)

- ✅ Karpathy 원문, Software 3.0 패러다임
- ✅ Willison vibe engineering 정의 (원문 페치)
- ✅ Osmani 70% Problem 핵심 (원문 페치)
- ✅ METR 2025 디테일 (저자 caveat 포함, 원문 페치)
- ✅ Stack Overflow Survey 2024/2025 핵심 수치 (원문 페치)
- ✅ DORA 2025 핵심 발견 (요약 다수)
- ✅ MIT Brain on ChatGPT 디테일
- ✅ ThoughtWorks Tech Radar complacency 권고 (원문 페치)
- ✅ 한국 우아한형제들·토스 사례 (원문 페치)
- ✅ 학습 이론(deliberate practice, ZPD, Bloom, cognitive load)의 AI 시대 접목
- ✅ 채용 시장 충격 정량 데이터
- ✅ 4개 입장(증폭론/재정의론/회의론/중도)으로의 입장 정렬과 충돌 보존

---

*리서치 종합 완료. 본 문서는 책 *AI 시대 개발자의 학습과 성장*의 1차 자료다. 챕터별 글쓰기에서는 위 자료를 그대로 인용하지 말고 — 각 챕터의 논지·청자(3층 독자)에 맞게 *발췌·재해석*한다.*
