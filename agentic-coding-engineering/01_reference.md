<!-- 검색 시점: 2026-06-10 기준 / 합성: research-lead -->
# AI Agentic Coding의 4대 엔지니어링 (Prompt · Context · Harness · Loop) 레퍼런스

> 대상 독자: Claude Code·Codex 주력, 가끔 Gemini CLI·중국계 코딩 모델(Qwen Coder·DeepSeek·GLM·Kimi)도 쓰는 현업 개발자.
> 책의 핵심 약속: **네 용어를 명확히 정의하고 기억하게 한다.**
> tech-book 신선도 규율 적용 — 모든 수치·버전·점수는 "{버전/연도} 기준"으로 못 박았고, 소스 발행일은 맨 아래 "신선도 원장"에 보존했다.
> 출처 표기 약자: [웹] / [논문] / [커뮤]

---

## 1. 개념과 정의

네 용어는 **추상화 계층이 다르다.** 한 문장 정의 + 한 줄 기억 장치 + 무엇을 다루는 분과인지로 정리한다.

### 1-1. Prompt Engineering (프롬프트 엔지니어링)
- **한 문장:** LLM에게 주는 **단일 지시(프롬프트)**를 잘 쓰는 기술 — 무엇을, 어떤 형식으로, 어떤 예시와 함께 말할지. [웹][논문]
- **기억 장치:** "한 번의 대화를 최적화한다." (Prompt engineering optimizes a single interaction.) [웹]
- **다루는 것:** 지시문 문구, few-shot 예시, 출력 형식, 역할 지정, chain-of-thought 유도.
- **Anthropic 정의:** 프롬프트 엔지니어링 = "최적의 결과를 위해 LLM 지시를 쓰고 조직하는 방법." 컨텍스트 엔지니어링의 부분집합. [웹: Anthropic 2025-09-29]

### 1-2. Context Engineering (컨텍스트 엔지니어링)
- **한 문장:** LLM 추론 중에 **컨텍스트 윈도에 들어가는 모든 토큰(정보)**을 동적으로 큐레이션·유지하는 전략 집합 — 프롬프트뿐 아니라 대화 이력·검색 결과·툴 출력·에이전트 상태 전부. [웹: Anthropic]
- **기억 장치:** "전체 정보 환경을 최적화한다. 프롬프트는 그중 일부일 뿐." [웹]
- **정전 정의 3종(거의 동의어):**
  - Karpathy: "the delicate art and science of filling the context window with just the right information for the next step." [웹: X 2025-06-25]
  - Tobi Lütke: "the art of providing all the context for the task to be plausibly solvable by the LLM." [웹: X 2025-06-19]
  - Harrison Chase(LangChain): "building dynamic systems to provide the right information and tools in the right format such that the LLM can plausibly accomplish the task." [웹: 2025-06-23]
  - Anthropic: "the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference." [웹: 2025-09-29]
- **핵심 원리:** 컨텍스트는 **유한 자원**(diminishing marginal returns). "가장 작은 high-signal 토큰 집합"을 찾는 것. [웹: Anthropic]

### 1-3. Harness Engineering (하네스 엔지니어링)
- **한 문장:** LLM(모델)을 **실제로 행동하는 에이전트로 바꾸는 실행 시스템**을 설계하는 일 — 모델 호출, 툴 실행, 컨텍스트 관리, 에러 처리, 중단 조건, 안전장치. [웹]
- **기억 장치:** **"Agent = Model + Harness."** 모델이 아니면 다 하네스다. [웹: HF 글로서리]
- **정전 정의:**
  - HF: harness = "The execution layer inside the agent: it calls the model, handles its tool calls, decides when to stop." [웹: 2026-05-25]
  - 비유: "everything between the language model and the real world. The harness decides what that text can touch." [웹: MindStudio]
- **인접 용어 구분 (중요):**
  - **Scaffold(스캐폴드)** = 행동 정의층 = 모델이 **무엇**을 보는가 (시스템 프롬프트·툴 설명·파싱·기억).
  - **Harness(하네스)** = 실행층 = 모델이 **어떻게** 실행하는가 (호출·툴콜 처리·중단).
  - 둘은 자주 혼용되나 다르다. [웹: HF]
- **학술 뿌리:** SWE-agent의 Agent-Computer Interface(ACI) — "인터페이스 설계가 에이전트 성능을 좌우한다"를 입증. [논문: Yang et al. NeurIPS 2024]

### 1-4. Loop Engineering (루프 엔지니어링)
- **한 문장:** 에이전트가 **반복 사이클(act → observe → reason → repeat)**로 목표에 수렴하도록, 무엇을·언제 프롬프트하고 결과가 수용 가능한지 판단하는 **자율 반복 시스템을 설계**하는 일. [웹: MindStudio]
- **기억 장치:** "한 번의 지시가 아니라, 반복하는 시스템을 설계한다." (직접 매번 타이핑하는 대신 루프가 프롬프트하게 만든다.) [웹]
- **에이전틱 루프 정의:** "Runs tools in a loop to achieve a goal." [웹: Willison 2025-09-30] / Solomon Hykes 인용: "An AI agent is an LLM wrecking its environment in a loop." [웹]
- **필수 구성요소:** 명확한 목표, 유용한 툴, 컨텍스트 관리, **종료 로직**, 진짜 에러 처리. 패턴: retry / plan-execute-verify / explore-narrow / human-in-the-loop. [웹]
- **학술 뿌리:** ReAct(reason+act 교차 루프). [논문: Yao et al. 2022]

### 1-5. 한눈에 보는 계층 (핵심 표)

| 용어 | 추상화 계층 | 최적화 대상 | 한 줄 정의 | 학술 뿌리 |
|------|-----------|-----------|-----------|----------|
| Prompt Eng. | 단일 발화 | 한 번의 지시 | 무엇을·어떻게 말할까 | in-context learning(Brown 2020), CoT(Wei 2022) |
| Context Eng. | 추론 1회의 전체 입력 | 컨텍스트 윈도 전체 | 윈도에 무엇을 채울까 | (산업 용어; 뿌리는 RAG·메모리) |
| Harness Eng. | 에이전트 실행 1스텝 | 모델↔세계 실행층 | 모델을 어떻게 행동하게 할까 | ACI/SWE-agent(Yang 2024), Toolformer(2023) |
| Loop Eng. | 다스텝 자율 반복 | 반복 사이클 전체 | 언제까지·어떻게 반복할까 | ReAct(Yao 2022) |

> 포함 관계(공식 입장): **Loop ⊃ Harness ⊃ Context ⊃ Prompt** 의 느슨한 동심원. 바깥일수록 더 넓은 시스템, 안쪽일수록 더 국소적. 단 칼로 자르는 위계가 아니라 관점의 줌 레벨로 보는 게 정확.

---

## 2. 핵심 관점들 (기원·발전 과정)

### 2-1. Prompt Engineering — 가장 오래된 분과 (2020~)
- 용어는 2020년 무렵 GPT-3와 함께 등장. Gwern Branwen이 GPT-3 입력 작성 맥락에서 처음 쓴 것으로 널리 귀속됨. [웹 — 귀속은 2차 소스 다수, **검증 필요**]
- GPT-3(2020)가 분수령: 파인튜닝 없이 **프롬프트 문구에 따라 출력 품질이 극적으로 달라진다**는 발견이 "프롬프트를 어떻게 쓰는가"를 일급 변수로 만듦. [논문: Brown 2020]
- 2021~2022: 커뮤니티·OpenAI 가이드가 베스트 프랙티스 축적. CoT(2022)가 대표 테크닉으로 학술화. [논문: Wei 2022]

### 2-2. Context Engineering — 2025년 중반에 이름을 얻다
- **타임라인 (정밀):**
  - 2025-06-19: **Tobi Lütke**(Shopify CEO) 트윗 — 용어 촉발. [웹]
  - 2025-06-23: **Harrison Chase**(LangChain) 블로그로 정식화. [웹]
  - 2025-06-25: **Andrej Karpathy** 트윗으로 대중화 폭발("+1 for context engineering"). [웹]
  - 2025-09-29: **Anthropic** 엔지니어링 블로그로 벤더 차원 공식화(전략 4종 제시). [웹]
- 핵심 메시지: 프롬프트는 프로덕션 에이전트 컨텍스트의 작은 일부. 나머지는 대화 이력·검색 문서·툴 출력·에이전트 상태·동적 조립 지식. [웹]

### 2-3. Harness Engineering — 에이전트 도구가 흔해지며 떠오름
- "Agent = Model + Harness"가 커뮤니티 공통어로 정착. 정의의 정밀화는 HF 글로서리(2026-05-25)가 대표. [웹]
- 학술 뿌리는 더 이르다: SWE-agent/ACI(2024)가 "인터페이스 설계 = 성능"을 입증, 오늘날 코딩 에이전트에서 가장 모방된 아이디어. [논문]
- 한국에서도 "하네스 엔지니어링"이 교육 상품으로 등장(패스트캠퍼스) — 용어가 현업 어휘로 안착 중. [웹][커뮤]

### 2-4. Loop Engineering — 가장 최신 (2025~2026 부상)
- **Ralph loop**(Geoffrey Huntley, 2025-07-14)가 자율 반복의 대표 밈·패턴: `while :; do cat PROMPT.md | claude-code ; done`. 신선한 컨텍스트로 같은 프롬프트 반복, 파일시스템이 메모리. [웹]
- **"loop engineering"** 용어 자체는 Addy Osmani가 명명·대중화(2026-06-07). Peter Steinberger("you should be designing loops that prompt your agents")가 촉발, Anthropic Boris Cherny("My job is to write loops")가 증폭, Osmani가 `Loop Engineering`이라는 분과로 패키징. [웹: Osmani 2026-06-07 — **1차 출처 확보 완료(2026-06-10), 심화는 §8 참조**]
- 학술 원형: ReAct(2022)의 act-observe-reason 루프. [논문]

---

## 3. 대표 사례 (도구 생태계 — 독자가 매일 쓰는 것)

각 도구가 4대 엔지니어링을 어떻게 구체화하는지로 정리. (도구 사실은 fact-checker 대조 대상)

### 3-1. Claude Code (Anthropic)
- **Context Eng.:** `CLAUDE.md`(항상 켜진 컨텍스트) + Skills(필요시 로드되는 온디맨드 지식·워크플로). [웹]
- **Harness Eng.:** Hooks(PreToolUse·PostToolUse·UserPromptSubmit 등 이벤트 핸들러), MCP(외부 툴 연결), Subagents(별도 컨텍스트 윈도에서 작업 후 요약만 반환). [웹: Claude Code docs]
- **Loop Eng.:** `--dangerously-skip-permissions`(YOLO 모드), 단일 스레드 마스터 루프. [웹]
- 역할 분담 요약: CLAUDE.md=항상-켜진 컨텍스트 / Skills=온디맨드 / MCP=외부 연결 / Subagents=격리 / Hooks=자동화. [웹]

### 3-2. OpenAI Codex CLI
- **Context Eng.:** `AGENTS.md` — 표준 Markdown. 빌드·테스트·컨벤션을 담는 에이전트 전용 지침 파일. README는 사람용, AGENTS.md는 에이전트용. [웹: developers.openai.com]
- **Harness Eng.:** 작업 전 AGENTS.md instruction chain 구성(글로벌 → 프로젝트 루트 → cwd 하향, AGENTS.override.md 우선). Agent Skills 지원. [웹]
- `AGENTS.md`는 사실상 업계 표준(agents.md)으로 다른 도구도 채택. [웹]

### 3-3. Gemini CLI (Google, Apache 2.0 오픈소스, 2025 출시)
- **Context Eng.:** `GEMINI.md` — 계층적 컨텍스트(~/.gemini/GEMINI.md 글로벌 + 워크스페이스·상위 디렉토리). 찾은 파일을 연결해 매 프롬프트와 함께 전송. [웹: geminicli.com]

### 3-4. Aider (Paul Gauthier, 오픈소스, 2023~)
- **Harness/Context:** 터미널 페어 프로그래밍. repository map(함수 시그니처·파일 구조)으로 코드베이스 컨텍스트 제공, 변경 자동 git 커밋. Claude·GPT-4o·DeepSeek 등 거의 모든 LLM 연결 → **모델 무관 하네스**의 사례. [웹: GitHub 41.6k stars / 2026-03 기준]

### 3-5. SWE-agent (Princeton, 학술 + 오픈소스, NeurIPS 2024)
- **Harness Eng. 원형:** GitHub 이슈 → 자동 수정. ACI가 핵심. 학술이 실무 하네스에 직접 영향. [논문]

### 3-6. 중국계 / 오픈웨이트 코딩 모델 (2026 기준 — 변동성 매우 높음)
> ⚠️ 아래 수치·버전은 모두 "2026-04~05 기준"이며 빠르게 낡는다. 본문 인용 시 반드시 날짜 명기 + fact-check.
- **Kimi K2.6**(Moonshot): 2026-04-20 출시 주장, 1T MoE/32B active. **Kimi Code**라는 Claude Code급 터미널 에이전트 동반. SWE-Bench Pro 58.6 주장(GPT-5.4 xhigh 57.7, Claude Opus 4.6 max 53.4 상회 주장). [커뮤 — **검증 필요**, 벤치마크 단일 출처]
- **Qwen 3.6 Plus**(Alibaba): 1M 토큰 컨텍스트, 에이전틱 코딩 상위 오픈웨이트. **Qwen Code**(CLI) 계열. [커뮤]
- **DeepSeek V4**: 자가호스팅 성능/추론비 비율 우수. [커뮤]
- **GLM 5.1**(Zhipu): MIT 라이선스가 차별점(상업·파인튜닝). [커뮤]
- 공통 교훈: **어떤 오픈웨이트든 구조화된 하네스 안에서 raw chat보다 훨씬 잘한다 — 하네스 투자는 선택이 아니라 필수.** [커뮤: MindStudio 2026]

### 3-7. Ralph loop (자율 반복 패턴의 대표)
- `while :; do cat PROMPT.md | claude-code ; done`. 루프당 한 작업, 파일시스템=메모리, 서브에이전트=병렬. Claude Code·Amp에서 동작. [웹: Huntley 2025-07-14]

---

## 4. 논쟁점·상충 관점

### 논쟁 A: "Prompt engineering은 죽었나?"
- **관점 1 (대체됨):** Gartner "context engineering is in, prompt engineering is out." 2026 설문 — 리더 82% "프롬프트만으론 프로덕션 불충분", 95% 2026 컨텍스트 엔지니어링 투자 계획. [커뮤 — **설문 수치 1차 미확인, 검증 필요**]
- **관점 2 (이름만 바뀐 확장/포함):** Karpathy·Anthropic·Chase 모두 "대체"가 아니라 **자연스러운 다음 단계·포함 관계**라고 명시. 프롬프트 작성은 여전히 중요하나 프로덕션 컨텍스트의 일부. [웹: Anthropic 2025-09-29, LangChain 2025-06-23]
- **레퍼런스 판단:** "죽음"은 클릭베이트. 정확한 정리는 **context engineering ⊃ prompt engineering**.

### 논쟁 B: 자율 루프(YOLO/Ralph) — 혁명인가 도박인가?
- **관점 1 (혁명):** Ralph로 "$50k 계약을 $297에" 류 그린필드 자동화. "LLMs are surprisingly good at reasoning about what is important to implement." [웹: Huntley — **저자 자체 주장·단일 사례, 일반화 금지**]
- **관점 2 (위험·비용):** $47,000 무한루프 사고(2025-11, 4개 에이전트 11일, 예산 캡 없음). 비용은 단계 수에 따라 3.2x(5스텝)→100x+(200스텝) 폭증. YOLO는 blast radius 통제 없으면 위험. [커뮤: dev.to·LeanOps 2026]
- **레퍼런스 판단:** 자율 루프는 **검증 신호(테스트)·하드 가드레일·샌드박스**가 갖춰질 때만 net-positive. 도구가 아니라 설계의 문제.

### 논쟁 C: 코딩 에이전트 비용 — 지금 쓸 만한가?
- **관점 1:** 2025-11이 "mostly works → actually works" 변곡점. 오픈웨이트로 비용↓. [웹: Willison]
- **관점 2:** 에이전트는 챗봇 대비 ~50x 토큰, 자율 디버깅 100x+. 통제 없으면 위험. [커뮤: LeanOps 2026]

### 논쟁 D: "harness/loop engineering"은 실체인가 용어 인플레이션인가?
- **관점 1 (실체):** "Agent = Model + Harness" 정착, 한국서도 강좌 상품화. [웹: HF, 패스트캠퍼스]
- **관점 2 (인플레이션):** 매달 새 "~engineering" 등장 피로감. loop engineering도 2026-06 갓 나온 신조어. [커뮤 — **정서, 검증 필요**]
- **레퍼런스 판단:** 용어는 새롭지만 가리키는 현상은 실재. 책은 "신조어 마케팅"과 "실재하는 분과"를 구분해 줄 것.

### 논쟁 E: context rot — 컨텍스트는 길수록 좋은가?
- **합의에 가까움:** 길수록 멍청해진다. Chroma(2025) — 18개 프런티어 모델 전부가 입력 길이 증가에 따라 F1 단조 감소. lost-in-the-middle, attention dilution, distractor interference. **놀라운 발견:** 논리적으로 일관된 문서보다 셔플된 건초더미에서 성능이 더 좋았다(구조적 일관성이 오히려 성능을 해침). [웹/커뮤: trychroma.com 2025]
- 함의: "컨텍스트를 많이 넣기"가 아니라 "딱 맞게 넣기"가 컨텍스트 엔지니어링의 본질.

---

## 5. 실무 적용 팁 (현업 개발자가 매일 익히는 법)

### Prompt Engineering 익히기
- CoT 유도("단계별로 생각해"), 역할·형식 지정, few-shot 예시 1~2개. [논문: Wei 2022]
- 한 번의 지시를 정확·구체·검증가능하게. 가장 작은 변경으로 가장 큰 효과 찾기.

### Context Engineering 익히기
- **컨텍스트를 유한 자원으로:** high-signal 최소 토큰. [웹: Anthropic]
- 4대 전략: **Compaction**(이력 요약 후 재초기화) · **Structured Note-Taking**(컨텍스트 밖 노트 영속) · **Sub-Agents**(깨끗한 컨텍스트로 작업 후 요약 반환) · **Just-in-Time**(식별자만 들고 런타임 동적 로드). [웹: Anthropic]
- 프로젝트 규칙을 파일로 영속화: `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`(도구마다 이름만 다름). [웹]
- context rot 회피: 불필요한 긴 컨텍스트를 넣지 말 것. [웹: Chroma]

### Harness Engineering 익히기
- Agent = Model + Harness 관점으로 도구를 분해해 보기: 내 도구의 툴 실행·컨텍스트 관리·에러·중단·안전장치는 어디 있나? [웹: HF]
- Claude Code: Hooks로 린트·포맷·보안 검사를 매번 강제. Subagents로 컨텍스트 격리. MCP로 외부 연결. [웹]
- "나만의 하네스 설계" — 반복 작업을 스킬/훅/서브에이전트로 구조화. [커뮤: 패스트캠퍼스]
- ACI 교훈: 모델이 쓰기 좋은 인터페이스(명확한 툴·간결한 출력)가 성능을 올린다. [논문]

### Loop Engineering 익히기
- **깨끗하게 통과하는 테스트 스위트가 루프 가치를 증폭** — 검증 신호가 곧 안전장치. [웹: Willison]
- **루프당 한 작업**(Ralph 제약). [웹: Huntley]
- **하드 가드레일:** max iteration, no-progress detection, 토큰/비용 예산을 알림이 아니라 **강제 차단**으로. [커뮤]
- **YOLO는 샌드박스에서:** 컨테이너·외부 머신(Codespaces)·네트워크 잠금 위에서만. [웹: Willison]
- 패턴 선택: retry / plan-execute-verify / explore-narrow / human-in-the-loop를 작업 유형에 맞게. [웹]

### 모델 무관 실전 팁
- 어떤 모델이든(Claude·Codex·Gemini·Qwen·DeepSeek·GLM·Kimi) **하네스 안에서 raw chat보다 훨씬 잘한다.** 하네스·컨텍스트 파일에 투자하면 모델을 갈아끼워도 자산이 남는다. [커뮤]

---

## 6. 참고문헌 (URL·DOI 포함, 발행일 명기)

### 1차 발언·블로그 (웹)
1. Karpathy, A. (2025-06-25). "+1 for context engineering over prompt engineering." X. https://x.com/karpathy/status/1937902205765607626
2. Lütke, T. (2025-06-19). "I really like the term 'context engineering'." X. https://x.com/tobi/status/1935533422589399127
3. Anthropic Engineering. (2025-09-29). "Effective context engineering for AI agents." https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
4. Anthropic. (2024-12-19). "Building Effective Agents." https://www.anthropic.com/research/building-effective-agents
5. Chase, H. / LangChain. (2025-06-23). "The rise of context engineering." https://blog.langchain.com/the-rise-of-context-engineering/
6. Huntley, G. (2025-07-14). "Ralph Wiggum as a software engineer." https://ghuntley.com/ralph/
7. Willison, S. (2025-09-30). "Designing agentic loops." https://simonwillison.net/2025/Sep/30/designing-agentic-loops/
8. Willison, S. (2024-12-20). "Building effective agents (notes)." https://simonwillison.net/2024/Dec/20/building-effective-agents/

### 용어 정의·해설 (웹)
9. Paniego, S. & Gosthipaty, A.R. / Hugging Face. (2026-05-25). "Harness, Scaffold, and the AI Agent Terms Worth Getting Right." https://huggingface.co/blog/agent-glossary
10. MindStudio. (2026). "What Is an Agent Harness?" https://www.mindstudio.ai/blog/what-is-agent-harness-architecture-explained
11. MindStudio. (2026). "What Is Loop Engineering?" https://www.mindstudio.ai/blog/what-is-loop-engineering-ai-coding-agents

### 도구 공식 문서 (웹)
12. OpenAI Developers. (2026 기준). "Custom instructions with AGENTS.md." https://developers.openai.com/codex/guides/agents-md / 표준: https://agents.md/
13. Google Gemini. (2025~). "Provide context with GEMINI.md files." https://geminicli.com/docs/cli/gemini-md/ / https://github.com/google-gemini/gemini-cli
14. Claude Code Docs. (2026 기준). "Extend Claude Code." https://code.claude.com/docs/en/features-overview
15. Aider (Gauthier, P.). (2023~, 최신 2026-03-03 기준). https://github.com/Aider-AI/aider

### 학술 (논문)
16. Brown, T. et al. (2020). "Language Models are Few-Shot Learners (GPT-3)." NeurIPS 2020. arXiv:2005.14165
17. Wei, J. et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in LLMs." NeurIPS 2022. arXiv:2201.11903
18. Yao, S. et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023. arXiv:2210.03629
19. Schick, T. et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." NeurIPS 2023. arXiv:2302.04761
20. Yang, J. et al. (2024). "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering." NeurIPS 2024. arXiv:2405.15793 / https://github.com/SWE-agent/SWE-agent
21. Jimenez, C. et al. (2024). "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" ICLR 2024. arXiv:2310.06770

### 커뮤니티·논쟁·도구 현황 (커뮤)
22. Chroma Research. (2025). "Context Rot: How Increasing Input Tokens Impacts LLM Performance." https://www.trychroma.com/research/context-rot
23. dev.to. (2026). "The $47,000 Agent Loop." https://dev.to/waxell/the-47000-agent-loop...
24. MindStudio. (2026). "Best Open-Source LLMs for Agentic Coding 2026." https://www.mindstudio.ai/blog/best-open-source-llms-agentic-coding-2026
25. TokenMix. (2026-Q2). "Best Chinese AI Models 2026 (Kimi/DeepSeek/Qwen/GLM)." https://tokenmix.ai/blog/best-chinese-ai-models-2026-comparison-guide
26. (한국) DevOcean/SK. (2026). "진짜 AI 에이전트형 코딩 툴 Claude-Code." https://devocean.sk.com/blog/techBoardDetail.do?id=167718
27. (한국) 패스트캠퍼스. (2026). "전현준의 하네스 엔지니어링: Claude Code·Codex 완벽 가이드." https://fastcampus.co.kr/data_online_harness
28. (한국) youngju.dev. (2026-05-14). "2026 AI 코딩 에이전트 정면 비교." https://www.youngju.dev/blog/...
29. ralph-wiggum.ai / HumanLayer "A Brief History of Ralph." https://www.humanlayer.dev/blog/brief-history-of-ralph

---

## 7. 리서치 한계 (커버하지 못한 영역)

- **X(Twitter) 본문 직접 렌더 제한:** Karpathy·Lütke·Chase 트윗의 날짜·문구는 다중 2차 소스(Zep·LangChain·learnprompting 등)로 교차검증했으나 트윗 페이지 직접 캡처는 아님.
- **"prompt engineering" 용어 최초 귀속(Gwern Branwen):** 2차 소스 다수가 동일 귀속을 하나 1차 확정 출처 미확보 — **검증 필요**.
- ~~**"loop engineering" 용어 귀속(Addy Osmani / Steinberger / Boris Cherny, 2026-06):** MindStudio 정리글 1건 기반, Osmani 원문 미확보 — **검증 필요**.~~ → **해소됨(2026-06-10):** Osmani 1차 원문(addyosmani.com/blog/loop-engineering, 2026-06-07) 확보. 계보 확정(Steinberger 촉발→Cherny 증폭→Osmani 명명). 정밀 요약·인용은 §8 및 `research/loop-engineering-deep.md`. (잔여: Cherny 발언의 1차 단독 링크는 Osmani 경유로만 확보 — 인용 시 "Osmani가 인용한 Cherny" 형식 권장.)
- **벤치마크 수치(SWE-bench/SWE-Bench Pro, 중국계 모델 점수):** 2026-04~05 기준이며 리더보드가 빠르게 바뀜. 본문 인용 시 반드시 "{모델 버전/날짜} 기준" + fact-check 필수.
- **설문 수치(82%·95% 등):** 2차 매체 재인용으로 1차 설문 보고서 미확인 — **검증 필요**.
- **일화적 비용 주장($297·$47,000):** 단일 사례 — 일반화 금지, "사례"로만 인용.
- **한국 커뮤니티 날것 토론:** OKKY·velog·디스코드 개별 스레드 원문은 검색 요약 기반(직접 인용 제한). 한국 자료는 블로그·교육상품 중심으로 수집됨.
- **paper 트랙:** 4대 "엔지니어링" 용어 자체를 단 peer-reviewed 논문은 2026-06 기준 사실상 없음(산업 용어). 학술은 기저 현상의 뿌리만 매핑함.

---

## 신선도 원장 (소스별 발행일·버전 시점)

> fact-checker 1차 대조 그라운딩. 개별 research/*.md가 정리돼도 이 표가 레퍼런스 안에 남는다. 검색 시점: **2026-06-10 기준**.

| 소스 | 발행일 / 버전 시점 | 트랙 | 비고 |
|------|------------------|------|------|
| Lütke 트윗 (context engineering) | 2025-06-19 | 웹 | 용어 촉발, 조회 190만 |
| LangChain "rise of context engineering" | 2025-06-23 | 웹 | Chase 정식화 |
| Karpathy 트윗 (+1 context engineering) | 2025-06-25 | 웹 | 대중화 분수령 |
| Huntley "Ralph Wiggum…" | 2025-07-14 | 웹 | Ralph loop 정전 |
| Anthropic "Effective context engineering" | 2025-09-29 | 웹 | 벤더 공식 정의, 전략 4종 |
| Willison "Designing agentic loops" | 2025-09-30 | 웹 | agentic loop 정의 |
| Anthropic "Building Effective Agents" | 2024-12-19 | 웹 | agent vs workflow |
| HF "Harness, Scaffold…" 글로서리 | 2026-05-25 | 웹 | Agent=Model+Harness 정의 |
| MindStudio loop/harness 해설 | 2026 (월 미상) | 웹 | 정리형, 1차 아님 |
| OpenAI AGENTS.md 문서 | 2026 기준 (지속 갱신) | 웹 | 벤더 1차 |
| Gemini GEMINI.md 문서 | 2025 출시~지속 갱신 | 웹 | Apache 2.0 |
| Claude Code docs | 2026 기준 (지속 갱신) | 웹 | 벤더 1차 |
| Aider GitHub | 첫 릴리스 2023 / 최신 2026-03-03 기준 | 웹 | 41.6k stars(2026-03 기준) |
| GPT-3 (Brown) | 2020 (NeurIPS) | 논문 | arXiv:2005.14165 |
| CoT (Wei) | 2022 (NeurIPS) | 논문 | arXiv:2201.11903 |
| ReAct (Yao) | 2022 (ICLR 2023) | 논문 | arXiv:2210.03629 |
| Toolformer (Schick) | 2023 (NeurIPS) | 논문 | arXiv:2302.04761 |
| SWE-agent (Yang) | 2024 (NeurIPS) | 논문 | arXiv:2405.15793, SWE-bench pass@1 12.5%(2024 기준) |
| SWE-bench (Jimenez) | 2024 (ICLR) | 논문 | arXiv:2310.06770 |
| Chroma "Context Rot" | 2025 | 웹/커뮤 | 18개 프런티어 모델(2025 기준) |
| "$47,000 Agent Loop" 사고 | 2025-11 (보도 2026) | 커뮤 | 단일 일화 |
| 중국계 모델 비교 (Kimi/DeepSeek/Qwen/GLM) | 2026-04~05 기준 | 커뮤 | 점수 변동성 높음, 버전별 명기 필수 |
| Kimi K2.6 | 2026-04-20 출시 주장 | 커뮤 | SWE-Bench Pro 58.6 주장(검증 필요) |
| (한국) 패스트캠퍼스 하네스 강좌 | 2026 기준 | 웹/커뮤 | 용어 대중화 사례 |
| (한국) youngju.dev 비교 | 2026-05-14 | 커뮤 | - |
| **Osmani "Loop Engineering"** | **2026-06-07** | 웹 | **loop engineering 용어 정전(1차) — §8** |
| Steinberger "Just Talk To It" / X | 2025-10 / 재게시 | 웹 | "designing loops" 촉발, "I ship code I don't read" |
| Willison "Designing agentic loops" | 2025-09-30 | 웹 | agentic loop 정의·brute force·YOLO |
| Schmid "Inner Loop vs Outer Loop" | 2026-02-20 | 웹 | inner/outer 구조 분류 |
| Huntley "everything is a ralph loop" | 2026-01-17 | 웹 | Ralph 일반화 |
| Claude Code ralph-wiggum 플러그인 | 2026 기준 | 웹 | Stop hook 재투입, max-iter/completion-promise |
| Codex `/goal` (CLI 0.128.0) | 2026 기준 | 웹 | 내장 Ralph 루프(plan-execute-observe-replan) |
| GitHub "Continuous AI" | 2025~ | 웹 | 에이전틱 CI/CD 루프, human-on-the-loop |

---

## 8. Loop Engineering 심화 (2차 리서치, 2026-06-10)

> 출간 책 5장 빈약 피드백 대응. 1차 출처 확보로 §1-4·§2-4의 ⚠️ 귀속 해소. 정밀 원장: `research/loop-engineering-deep.md`. 인용 원문(영문)은 fact-check 충실성을 위해 보존.

### 8-1. 1차 정의 (Osmani 2026-06-07 — 원문 보존)
- **정의:** "Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead." [웹: Osmani 2026-06-07]
- **루프:** "A loop here can be thought of [as] a recursive goal where you define a purpose and the AI iterates until complete." [웹]
- **전환:** "The agent is a tool and you are holding it the entire time... That part is kind of over." → "Now you build a small system that finds the work, hands it out, checks it, writes down what is done and then decides the next thing." [웹]

### 8-2. 용어 계보 확정 (촉발 → 증폭 → 명명)
- **Steinberger(촉발):** "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." [웹: X @steipete]
- **Cherny(증폭, Anthropic Claude Code 책임):** "I don't prompt Claude anymore. I have loops running that prompt Claude... My job is to write loops." [웹: Osmani가 인용]
- **Osmani(명명):** "loop engineering" 명사구로 분과화·대중화. (context engineering의 Lütke→Karpathy→Anthropic과 동형 3단 패턴.)
- **별개 계보:** Huntley **Ralph loop**(2025-07)는 *구현 패턴*, Willison **agentic loops**(2025-09)는 *기술 정의*, Schmid **inner/outer loop**(2026-02)는 *구조 분류*. Osmani 글은 Huntley·Ralph·Willison을 **명시 인용하지 않음** — 수렴 진화. Ralph는 Loop Engineering의 가장 단순한 구현체.

### 8-3. 루프 구성요소 (Osmani의 5+1)
Automations(스케줄 발견·분류) · Worktrees(병렬 격리) · Skills(프로젝트 지식 기록) · Plugins/Connectors(툴 연결) · Sub-agents("one has the idea and a different one checks it") · **+State/Memory**("a markdown file, or a Linear board, anything that lives outside the single conversation"). → 하네스 요소를 *스케줄·검증·상태*로 엮은 것 = 루프. (Loop ⊃ Harness와 정합.)

### 8-4. inner vs outer loop (Schmid)
- inner = "what happens during a single task, before the agent responds to user with a text" (태스크 내 신뢰성). 
- outer = "across multiple turns/sessions... over time" (시간에 따른 똑똑해짐). 
- "The loop is hardcoded. What the model does inside the loop is not." → Osmani의 loop engineering ≈ **outer loop 설계**.

### 8-5. 종료 조건·검증 신호 (구체화)
- **종료:** completion-promise(문자열 매칭) / max-iterations(하드 캡, "primary safety mechanism") / test-as-oracle / no-progress 감지 / CTRL+C 게이트(Huntley도 인정).
- **검증:** "Verification is still on you." 테스트가 1차 피드백(Willison "a common theme... is automated tests"). Verifier 서브에이전트 = boolean 판정 → 불만족 시 replanning. 계층적(빠른 구문 inner / 느린 의미 outer)으로 비용↔정확도 균형.

### 8-6. 실패 모드 (Osmani 3대 경고 — 5장 핵심 투입)
- **검증 공백:** "A loop running unattended is also a loop making mistakes unattended."
- **이해 부채:** "The faster the loop ships code you did not write, the bigger the gap between what exists and what you actually get."
- **인지적 항복:** "stop having an opinion and just take whatever it gives back" — "the cure when you do it with judgement and the accelerant when you do it to avoid thinking."
- **클로징:** "the leverage point moved. Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go."

### 8-7. 도구별 루프 기능 (2026-06 기준, fact-check 필수)
- **Claude Code:** 공식 **ralph-wiggum/ralph-loop 플러그인** — Stop hook으로 종료 차단·동일 프롬프트 재투입, 파일·git 이력 유지. `--max-iterations`/`--completion-promise`. 외부 bash 루프 불요. (Opus 4.5 4h49m 무인 실행 보도.)
- **Codex:** **`/goal`**(CLI 0.128.0~) = 내장 Ralph 루프, "plan, execute, observe, re-plan, execute again", 서브프로세스·테스트·재시도 자율. 클라우드 백그라운드 샌드박스.
- **Cursor:** Background Agents(서버사이드)지만 "not designed to run unattended for tens of minutes against a token budget" — 인터랙티브 IDE 지향.
- **GitHub Continuous AI:** 에이전틱 CI/CD 루프(Continuous Docs/Triage/Test/Perf), human-on-the-loop 강조.
- **Gemini CLI:** 컨텍스트(GEMINI.md) 중심, 루프 일급화는 상대적으로 약함.

### 8-8. 추가 논쟁 (기존 §4 보강)
- **용어 인플레이션:** "Context → Harness → now Loop Engineering" 피로감. 단 Anthropic·OpenAI가 공식 기능으로 일급화 → 신조어가 아닌 실재 패턴.
- **human-in vs on the loop:** Fowler/Thoughtworks "human-on-the-loop". Osmani의 답 = "stay the engineer."
- **읽지 않는 코드:** Steinberger "I ship code I don't read" vs Osmani "comprehension debt" — 같은 진영 내 긴장.
