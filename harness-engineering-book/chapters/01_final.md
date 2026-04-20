# 1장. 하네스라는 마구(馬具)

금요일 오후, 팀 슬랙에 누군가 스크린샷을 올렸다고 해보자. 방금 Claude Code에게 시킨 리팩토링이 11개 파일을 가로지르며 단번에 끝났다는 자랑이다. 댓글은 "대단하다"로 채워진다. 그런데 그 세션의 토큰 소비량을 묻는 사람은 없다. 실행된 테스트가 진짜 실패를 걸러냈는지, 커밋의 "all green"이 수십 개 `expect(true).to.be(true)` 위에 앉아 있는지도 확인하지 않는다. 찜찜하다.

이 찜찜함이 책의 출발점이다. 우리는 도구를 능숙하게 쓰고 있는 게 아니라, 도구 주변에 어떤 마구(馬具)를 채울지를 아직 언어화하지 못한 상태다. 그래서 좋은 결과가 나와도 왜 좋은지 설명하지 못하고, 나쁜 결과는 프롬프트 탓으로 돌린다.

"하네스(harness)"라는 말은 이 공백에 뒤늦게 붙은 이름이다. 프롬프트 파일, 규칙 문서, 루프 스크립트, 도구 권한, 감시 훅 — 조각은 10년 전부터 있었다. cron, Makefile, CI 파이프라인, pre-commit 훅이 각자의 이름으로 있었다. 달라진 건 조립 순서가 아니라 조립 대상이 LLM으로 바뀌었다는 점뿐이다. 그 차이가 왜 새 이름 하나를 끌고 왔는지부터 풀어보자.

## 1.1 하네스의 정의와 성숙도

먼저 **이 책이 채택하는 정의**부터 못 박자. 하네스란, LLM을 생산 업무에 쓸 때 단일 프롬프트가 아니라 **프롬프트 + 규칙 파일 + 루프 + 도구 권한 + 관측**을 한 덩어리로 조립한 운영 구조다. 말 그대로 모델에 씌우는 마구. 고삐만 있다고 말이 달리지는 않는다. 재갈·안장·배띠까지 맞물려야 비로소 사람을 태운다.

이 덩어리가 얼마나 완성되어야 "하네스를 갖췄다"고 말할 수 있을까. HumanLayer의 Dexter Horthy가 2025년 블로그 "Skill Issue — Harness Engineering for Coding Agents"에서 제안한 프레이밍이 있다.

> "A basic production harness = CLAUDE.md + type checks + occasional subagents (covers ~15% of requirements). A complete harness = custom architectural rules, machine-readable constraint documents, dynamic tool scoping, verification hooks, cost dashboards (~80%)."
> ([HumanLayer, Skill Issue — Harness Engineering for Coding Agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents))

번역하면 이렇다. `CLAUDE.md` 한 장과 타입 체크, 가끔 서브에이전트를 부르는 수준은 **요구사항의 15%쯤만 감당하는 basic 하네스**다. 아키텍처 규칙을 커스텀으로 쓰고, 기계가 읽는 제약 문서를 갖추고, 툴 권한을 동적으로 조이며, 검증 훅과 비용 대시보드까지 돌리는 수준이 **80%를 감당하는 complete 하네스**다.

주의해야 한다. 이 "15%·80%"는 학술 메트릭이 아니다. Horthy 본인의 **교수법적 프레이밍**이며, 업계 표준이라고 말하는 순간 거짓이 된다. Linux Foundation 산하 Agentic AI Foundation이 `AGENTS.md`를 표준으로 관리하는 층위와는 결이 다르다. 그럼에도 이 프레이밍을 버리지 않는 이유는, 독자가 "내 하네스가 어디쯤에 있는가"를 묻게 만드는 데에는 이만한 장치가 아직 없기 때문이다.

더 재현 가능한 자가 점검이 필요하다면 Andrej Karpathy가 autoresearch 레포([karpathy/autoresearch](https://github.com/karpathy/autoresearch))에서 내놓은 3요소를 루브릭으로 쓰자. 하네스가 **자동화 가능한지**를 판별하는 세 질문이다.

1. **Editable asset** — 에이전트가 수정 권한을 가진 단 하나의 파일/객체가 있는가? Karpathy의 표현으로 "검색 공간을 해석 가능하게 유지"하는 축이다.
2. **Scalar metric** — 개선 여부를 판정할 단일 숫자가 있는가? autoresearch에서는 `val_bpb`(validation bits per byte)다. 인간 판단이 필요 없어야 한다.
3. **Time-box** — 평가 사이클이 고정되어 있는가? 5분 훈련 × 시간당 12실험 × 수면 중 100실험 식으로 경제학이 성립해야 한다.

Karpathy는 일반화 조건까지 제시한다.

> "Any system that exposes a scriptable asset, produces a measurable scalar outcome, and tolerates a time-boxed evaluation cycle is a candidate."

세 질문에 모두 "예"라고 답할 수 있는 업무만이 하네스로 자동화할 후보다. DB 쿼리 최적화(asset=쿼리 설정, metric=p95 레이턴시)는 해당되고, 티켓 라우팅(asset=분류 프롬프트, metric=hold-out 정확도)도 해당된다. 그렇다면 "디자인 리뷰를 대신하게 하자"는 대부분 해당되지 않는다. 세 번째 요소인 time-box가 성립하지 않기 때문이다. 이 루브릭을 반드시 기억해두자. 책 전체에서 반복 소환된다.

HumanLayer의 basic/complete와 Karpathy 3요소는 같은 질문의 두 얼굴이다. 전자가 "내 하네스가 어디까지 조립됐는가"를 묻는다면, 후자는 "내 업무가 애초에 조립할 만한가"를 묻는다. 두 질문을 나란히 세워두는 편이 안전하다.

## 1.2 3세대 구도 — Prompt → Agent → Harness

커뮤니티가 즐겨 쓰는 내러티브는 3세대 구도다.

- **Prompt 1.0 (2022–2023)** — "더 좋은 프롬프트"가 곧 경쟁력. ChatGPT 초기, GitHub Copilot Chat 초기. `system prompt`와 `role`만 잘 배합하면 된다고 믿던 시기.
- **Agent 2.0 (2023–2025)** — 도구 호출·루프·RAG. AutoGPT와 BabyAGI가 밈으로 떠오르고 Devin이 "세계 첫 AI 소프트웨어 엔지니어"로 광고되던 시기. 툴 사용은 늘었지만 "why-it-works"는 손에 잡히지 않았다.
- **Harness 3.0 (2025– )** — 규칙 파일·훅·서브에이전트·관측·비용 규율까지 한 스택. Claude Code, Codex CLI, Cursor rules, Cline의 slash command 생태가 여기에 해당한다.

이 구도는 편하다. 편한 만큼 **마케팅 용어에 가깝다**. 세 세대를 나누는 조각(템플릿, cron, 권한, 옵저버빌리티)은 이미 10년 전부터 각자의 이름으로 있었다. 새로워진 건 이 조각들 사이를 오가는 **행위자가 결정론적 스크립트에서 확률적 LLM으로 바뀌었다**는 점이다.

그렇다면 왜 굳이 이름을 새로 붙이는가. 기존 언어로는 세 가지 현상이 잡히지 않기 때문이다.

첫째, **편집 가능한 자산(editable asset)이 코드 바깥으로 새어 나간다.** `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/*.mdc` 같은 "규칙 파일"이 실행 성능의 3분의 1을 좌우한다. Makefile 시절엔 자산이 소스 트리 안에만 있었다.

둘째, **루프가 인간의 손을 거치지 않는다.** cron 잡은 입력이 결정론적이었다. Ralph Loop은 `while :; do cat PROMPT.md | claude-code; done`이다. 루프 한 번에 기능이 생겨나기도, 사라지기도 한다.

셋째, **권한과 관측이 모델의 확률적 출력을 견제하기 위해 별도 층으로 들어선다.** Claude Code 훅의 `permissionDecision: "deny"`가 `--dangerously-skip-permissions`마저 이기는 구조가 그 증거다([Claude Code hooks guide](https://code.claude.com/docs/en/hooks-guide)). 결정론적 시스템에는 없던 방어선이다.

이 셋을 묶을 이름이 없으니 "하네스"라는 마구의 은유가 뒤늦게 들어왔다. 은유를 벗기면 남는 건 **자산·루프·권한·관측을 하나의 운영 구조로 조립한다**는 공학 명제 하나다. 그리고 가장 큰 함정 하나는 기억해두자. "3세대가 1·2세대를 무효화한다"는 오해. 좋은 하네스는 좋은 프롬프트를 전제로 하고, 좋은 에이전트 루프를 부품으로 쓴다. 단계는 쌓인다, 갈아치우지 않는다.

## 1.3 복합 시스템으로서의 하네스

하네스를 "프롬프트의 상위 버전"으로 이해하면 가장 중요한 점 하나를 놓친다. **하네스는 단일 모델 프롬프팅이 아니라 시스템 설계다.** 2024년 Berkeley BAIR 블로그에서 Matei Zaharia 등은 이 전환을 **Compound AI Systems**로 정리했다.

> "State-of-the-art AI results are increasingly obtained by compound systems with multiple components, not just monolithic models."
> (Zaharia et al., 2024, [The Shift from Models to Compound AI Systems, BAIR](https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/))

Databricks 자체 서베이에서 60%가 RAG, 30%가 multi-step chain이었다. 단일 모델 호출 하나로 끝나는 프로덕션 시스템은 이미 소수파였다. 이 책은 이 프레이밍을 차용한다. 우리가 배울 것은 "프롬프트를 더 잘 쓰는 법"이 아니라 **"복합 시스템을 설계하는 법"**이다.

설계의 출발점으로 삼기 좋은 1차 자료가 Anthropic이 2024년에 공개한 **"Building Effective Agents"** 가이드다([anthropics/anthropic-cookbook의 patterns/agents](https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents)). 글 자체가 설교 없이 5개 워크플로 패턴만 나열한다.

1. **Prompt Chaining** — 순차 호출 + 검증 게이트. 출력이 다음 입력이 되고, 중간에 조건 분기가 있다.
2. **Routing** — 분류 후 전문 경로. 입력을 유형별로 나눠 전문화된 프롬프트로 보낸다.
3. **Parallelization** — voting(다수결) 또는 sectioning(독립 분할). 동일 입력을 반복 또는 분할해 병렬 처리.
4. **Orchestrator-Workers** — 중앙 LLM이 태스크를 동적으로 분해·위임. 계획자와 실행자가 분리된다.
5. **Evaluator-Optimizer** — 생성/평가 루프, 반복 개선. Critic이 Generator에 되먹임을 건다.

Anthropic의 권고는 뚜렷하다.

> "Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs. (…) simple, composable patterns rather than complex frameworks."

이 인용을 가볍게 넘기지 말자. 프레임워크를 통째로 도입하기보다는 이 5개 패턴을 **레고 블록처럼 갈아끼우며 조립하는 편이 낫다**는 주장이다. 6장의 Generator–Critic 구조는 5번의 실전 버전이고, 7장의 서브에이전트 논의는 4번의 비용 함수 버전이다. 1장에서는 이름만 심어두자.

실무 감각을 하나 더 붙이면, [Cline 팀이 공개한 텔레메트리](https://cline.bot/blog/how-to-think-about-context-engineering-in-cline)는 "AI coding performance dips when context windows exceed 50%"라고 말한다. 광고된 200k 컨텍스트라도 **실효 품질은 100k(50%)에서 꺾인다**. Claude Code의 147–152k 컨텍스트 clip 현상과도 맞물린다. 복합 시스템 설계의 첫 교훈은 단순하다. **컨텍스트는 크기보다 활성 점유율이 KPI다.** 3장에서 본격 전개한다.

## 1.4 6-layer의 진실

하네스 강의를 따라 읽다 보면 "6-layer 하네스"라는 표현을 만난다. GOAL·RULE·Spec·Drift·Permission·Knowledge. 여섯 개의 파일을 만들고 레이어로 쌓으라는 말처럼 들린다. 개념 정리에는 유용하지만, **문자 그대로 파일 6개를 만들라는 지시로 읽으면 곤란하다**. 커리큘럼 Module 1에서 쓰는 **교수법 비유**임을 먼저 못 박자.

각 어휘는 다음 문제를 **가리키기 위한 이름**이다.

- **GOAL** — 하네스가 수행할 최종 목표. "무엇을" 정의한다. 대개 `CLAUDE.md`·`AGENTS.md` 상단 몇 줄.
- **RULE** — 구속 조건(스타일·금지·보안). "어떻게 하지 말 것." Don't 섹션, pre-commit 훅, 정책 파일로 분산된다.
- **Spec** — 입력/출력/성공·실패 기준. 테스트·타입·스키마가 여기에 산다.
- **Drift** — 루프가 길어질수록 에이전트가 초기 지시에서 멀어지는 현상. "파일"이 아니라 "측정 대상"이다. 장시간 세션에서 약 절반가량의 에이전트에서 관찰된다(추정치).
- **Permission** — 도구·파일 접근 통제. Claude Code settings scope, Codex approval policy가 해당한다.
- **Knowledge** — 재사용 가능한 사실·레시피. Skills, memory bank, notepad.

여섯 어휘가 파일 여섯 개로 대응되는 건 깔끔하지만 거짓에 가깝다. GOAL과 RULE은 한 파일 상단에 공존하고, Spec은 테스트와 타입으로 흩어지며, Drift는 파일이 아니라 관측 대시보드에 산다. "6-layer를 갖추자"는 말은 "이 여섯 관점으로 내 하네스를 비춰보자"는 **체크리스트**로 읽는 편이 낫다. 파일 이름에 억지로 매핑하려 들면, 관리 대상만 늘고 작동은 같은 하네스가 나온다. 그럼에도 어휘 자체는 익혀두자. 6장의 Critic rubric, 9장의 prompt injection 방어, 10장의 비용 대시보드에서 이 여섯 관점이 돌아가며 재조명된다.

---

> **Contrarian Signal — "하네스 없는 에이전트"의 비용 곡선**
>
> 조립이 맞물리지 않으면 어떻게 되는가. Princeton의 Sayash Kapoor, Benedikt Ströbl 등이 2024년에 내놓은 논문 **"AI Agents That Matter"** (Kapoor et al., 2024, arXiv:2407.01502)는 현 에이전트 문헌에서 가장 날카로운 비판이다. 네 가지 진단을 제시한다.
>
> 1. accuracy-only 벤치마크가 **비용 폭발을 가린다**.
> 2. 연구 벤치마크가 사용자 필요와 괴리되어 있다.
> 3. 약한 holdout 탓에 overfit이 구조화된다.
> 4. 평가 방식이 비표준이라 결과를 비교할 수 없다.
>
> 저자들이 뽑은 한 줄은 독자의 현업 감각을 한 번에 흔든다.
>
> > "SOTA agents are needlessly complex and costly."
>
> HumanEval·GAIA 등에서 **accuracy 1%p를 추가로 짜내는 데 드는 비용이 로그 스케일로 튀어 오른다**는 도식은 이 책이 끝까지 끌고 갈 뼈대다. 정확도를 외치며 루프를 한 바퀴 더 돌리는 순간, 토큰·시간·개입이 기하급수로 따라 붙는다. 논문은 이 곡선을 **Pareto 2축(cost × accuracy)으로 시각화해 측정하라**고 처방한다. 이 책은 그 처방을 강제한다. 5장에서 본격화하고, 12장에서 한 장의 Pareto 플롯으로 독자의 하네스를 되비추게 만들 것이다. 지금은 한 문장만 챙기자. **하네스 없는 에이전트는 "느린 실패"가 아니라 "비싼 실패"다.**

---

## 1.5 실습과 체크포인트

머리로만 읽은 내용은 다음 장을 펼칠 때쯤 증발한다. 가볍게 손을 먼저 대보자. 두 실습 모두 `[읽기 15분]` 태그로, 본인 레포를 바꾸지 않고 노트 1~2줄만 남기는 수준이다.

**실습 1. `[읽기 15분]` — 내 규칙 파일을 GOAL/RULE/EXAMPLES로 분해하기**

- **할 일:** 본인 레포의 `CLAUDE.md` 또는 `AGENTS.md`를 열어 수정 없이 **주석만** 붙인다. 각 문단/불릿 옆에 `# GOAL`, `# RULE`, `# EXAMPLE` 중 하나를 마킹. 해당 없으면 `# ???`.
- **산출물:** 노트 1~2줄로 세 가지를 적는다 — (a) RULE과 EXAMPLE의 비율, (b) `# ???` 줄 수, (c) "몰빵"된 섹션 이름.
- **관전 포인트:** RULE만 많은 파일은 "금지 사항 선반"이 된다. EXAMPLE 없이 RULE만 늘어난 하네스는 3장의 "200줄 몰빵" 전형이다.

**실습 2. `[읽기 15분]` — Karpathy 3요소 루브릭으로 자가 점수화**

- **할 일:** 최근 2주 안에 돌린 자동화 하나를 떠올려 세 질문에 0/1/2점을 매긴다.
  1. Editable asset이 **단 하나**인가? (0=없음, 1=산발, 2=단 하나)
  2. Scalar metric이 **인간 판단 없이** 계산되는가? (0=사람이 본다, 1=반자동, 2=스크립트 즉시)
  3. Time-box가 **고정**인가? (0=끝날 때까지, 1=무른 상한, 2=분/토큰 hard limit)
- **산출물:** 합산 0~6점 + "가장 약한 요소" 한 줄.
- **관전 포인트:** 대부분의 실무 하네스가 첫 해에는 2~3점이다. 이 점수가 Kapoor Pareto 곡선 어디에 찍히는지, 5장·12장에서 다시 맞춰볼 것이다.

### 체크포인트

장을 덮기 전, 두 질문에 자기 목소리로 답해보자. 메모장에 두세 문장이면 충분하다.

1. 6개 조각(GOAL·RULE·Spec·Drift·Permission·Knowledge)을 **파일 목록이 아니라 관점의 묶음**으로 설명할 수 있는가? 동료가 "하네스가 뭐야"라고 물으면 1분 안에 답할 수 있는가?
2. 내 하네스는 **basic(~15%)인가 complete(~80%)인가**? Karpathy 3요소 점수는 몇 점인가? 수치로 답할 수 없다면, 그 답할 수 없음 자체를 오늘 노트에 남기자. "수치로 답하기 찜찜하다"가 정상이다. 그 찜찜함이 2장부터 10장까지의 연료다.

## 마무리

1장에서는 "하네스"라는 용어가 왜 뒤늦게 생겼는지, 그 말이 가리키는 실체가 무엇인지를 훑었다. HumanLayer의 basic/complete 프레이밍과 Karpathy 3요소는 자가 점검의 두 기둥이고, 3세대 구도는 편리한 마케팅 비유이며, 6-layer는 체크리스트로 읽어야 할 교수법 도구다. 그 배경에는 **Kapoor의 비용 곡선**이 있다. 하네스가 없으면 정확도는 돈으로 환산되어 사라진다.

2장에서는 이 추상을 바닥까지 내린다. Claude Code와 Codex CLI가 물리적으로 어떻게 다른지 — `CLAUDE.md` 상향 병합, 서브에이전트 프런트매터, 27종의 훅 이벤트, `AGENTS.md` 조회 순서, `workspace-write`·`read-only`·`danger-full-access` 샌드박스, approval policy 4종, **4×의 토큰 격차**까지 — 메커니즘을 해부한다. 1장이 "왜 이 단어가 필요했는가"였다면, 2장은 "이 단어를 태울 수레바퀴가 어떻게 생겼는가"다.

---

### 학술 레퍼런스

- Zaharia, M., et al. (Berkeley BAIR, 2024). *The Shift from Models to Compound AI Systems.* BAIR 블로그. <https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/>
- Anthropic (2024). *Building Effective Agents.* <https://www.anthropic.com/research/building-effective-agents>; cookbook <https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents>
- Karpathy, A. (2024). *autoresearch repo.* <https://github.com/karpathy/autoresearch>
- Kapoor, S., Ströbl, B., et al. (Princeton, 2024). *AI Agents That Matter.* arXiv:2407.01502. <https://arxiv.org/abs/2407.01502>
- HumanLayer (Horthy, D.). *Skill Issue — Harness Engineering for Coding Agents.* <https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents>
- Cline (2025). *How to Think About Context Engineering in Cline.* <https://cline.bot/blog/how-to-think-about-context-engineering-in-cline>
