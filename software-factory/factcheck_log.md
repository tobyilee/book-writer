
## 01장 (라운드 1)

대조 근거: `01_reference.md`, `research/web.md`·`papers.md`·`community.md`. 저술가가 "추출 인용"으로 표시한 항목은 1차 원문을 curl로 받아 문자열 대조(2026-09-28): factory.strongdm.ai, strongdm.com 블로그, simonwillison.net(2026-02-07), danshapiro.com, claude.com 플레이북, factory.com Factory 2.0, githubnext.com Continuous AI, anthropic.com Opus 5.5 발표, arXiv 초록(MAST·Agentless·HCAST·Bhati), METR TH1.1·PR 노트, NBER w35275. openai.com은 403 — 하네스 엔지니어링 날짜는 검색(InfoQ 2026/02, 원문 인용 노트 타임스탬프)으로 확인.

### ❌ 정정
- "Claude Opus 5.5의 발표 페이지는 68만 줄 규모의 코드 마이그레이션을 하루 안에 끝냈다고 적었다" → "한 초기 테스터가 이 모델로 68만 줄 규모의 … 끝냈다고 소개했다" — 원문: "One tester completed a 680,000-line code migration in less than a day" (anthropic.com/claude-opus-5-5, 2026-09-22). 수행 주체가 벤더가 아니라 초기 테스터. "벤더의 주장" 라벨은 유지.
- "이 팀의 공개 자료에는 어떤 모델을 썼는지가 나와 있지 않다" → "팀을 꾸리는 계기가 된 모델 개선 이야기는 하지만, 팩토리를 지금 어떤 모델로 돌리는지는 밝히지 않는다" — factory.strongdm.ai 본문이 계기로 "second revision of Claude 3.5 (October 2024)"를 언급함. 원문대로면 "모델이 나와 있지 않다"는 틀림. 계획의 "StrongDM 사용 모델 언급 금지"에 따라 모델명은 넣지 않음.
- "엔지니어는 자기 팩토리의 주권자여야 한다고 썼다" → "팩토리를 들이는 조직이 그 팩토리의 주권자여야 한다고 썼다" — 원문 "Sovereign Intelligence. You must be the sovereign of your software factory."는 조직의 호스팅·데이터 통제권 맥락("your organization", "inside your walls")이지 엔지니어 개인의 역할 규정이 아님(factory.com, 2026-06-15).
- "공개하며 맨 앞에 내건 원칙" → "앞머리에 내건 원칙" — 원문에서 rule form 두 줄 앞에 kōan form("Why am I doing this?")이 먼저 나옴.

### ⚠️ 약화·삭제
- "2026년 9월 말까지 … 동료 심사 논문은 없다. 이 용어를 쓴 학술 문헌은 … 하나뿐이다" → "찾아본 범위에서는 … 없었다. 이런 뜻으로 이 용어를 쓴 학술 문헌도 … 하나 정도였다" — 부재 주장은 리서치 범위 한정(papers.md G절). 같은 장에서 Cusumano(1991)를 다루므로 "이런 뜻으로"를 붙여 자기모순을 피함. Bhati arXiv:2609.04681(2026-09-04, 단독 저자, 실험 없음)은 arXiv에서 실재 확인.
- "같은 달 GeekNews가 … 소개하면서" → "비슷한 무렵" — GeekNews 날짜는 "7달전" 상대 표기의 환산(web.md 자료 8, ~2026-02). 원문 페이지 403으로 월 단위 확정 불가.

### 🕒 신선도
- (추가 없음) — METR·Agentless·HCAST·METR PR 연구에 "당시 모델 기준"이 이미 붙어 있고, 도구 성숙 문단은 "2026년 9월 기준" 명기. DORA는 "2025년 보고서"로 명기돼 있음. 2026년판 State of AI-assisted SD 보고서는 검색 시점 미발견(2026.01 ROI 보고서만 존재) — 교체 불요.

### ✅ 확인 (요약)
- StrongDM: 원칙 두 줄·"$1,000 on tokens today per human engineer"(원문 일치), 팀 결성 2025-07-14·구성원 3인, 원칙 페이지 2026-02-06(McCarthy 서명), 회사 블로그 2026-02-19, "validation replaces code review"·"runs real scenarios, validates real behavior, and corrects itself without humans in the loop"(블로그 원문 일치), satisfaction 정의, DTU(Okta·Jira·Slack 등), Attractor 설명.
- Willison: 2025-10 방문("back in October … invited guests"), 2026-02-07 글, 정확성 질문 블록 인용(원문 그대로), "$20,000/month" 조건부 문구(원문 일치, 본문도 조건부 환산으로 서술), X 게시글 "most ambitious form…"(X 게시글 검색 확인).
- 계보: 히타치 1969·Cusumano 1991(레퍼런스 기준), MetaGPT ICLR 2024 oral·ChatDev ACL 2024, MAST(2025, 7개 프레임워크·1,600+ 기록·14개 모드·3범주·"often minimal" — arXiv 초록 일치), Continuous AI(Don Syme, GitHub Next, 2025-06), Shapiro 2026-01-23·Glowforge CEO·"neither needed nor welcome"(원문 일치), OpenAI 하네스 엔지니어링 2026-02-11(상충 #8 — 검색으로 2026-02 재확인, 2026-02-11 유지), Anthropic 플레이북 2026-08-21·6단계·"The loop keeps running. Human judgement stays above it."(원문 일치), Factory 2.0 2026-06-15·종단간 신호 체인(원문 일치).
- 정의표: Igor Ostrovsky 2026-09·Addy Osmani 2026-07(레퍼런스 일치). Böckeler Agent = Model + Harness(web.md 자료 11).
- CI/CD 비교: 플레이북의 "가장 시간이 들고 비싼 단계 = 코드 작성" 전제·"Build is no longer the constraint"·리뷰 대기열 문장(원문 일치), gh aw `.lock.yml` 컴파일, "Leave mechanical checks in CI", Kief Morris in/on the loop, Agentless(질문 문구·3단계·32.00%·$0.70·"all existing open-source software agents" — arXiv v2 초록 일치).
- 왜 지금: METR 7개월 배가(초록), Claude 3.7 Sonnet 약 50분, TH1.1 Opus 4.5 320분[170–729]·2024년 이후 88.6일(METR 원문 표 일치), HCAST 70–80%/20% 미만(초록 일치), Opus 5.5 출시 2026-09-22.
- 생성 vs 출하: NBER w35275(2026-05, 개정 2026-09, 50만 명 이상, +30/+180/+240%, 프로젝트 +80%·릴리스 +30%, 결론 문장 — 초록 일치), METR 2026-03-10 PR 노트("roughly half … would not be merged", 피드백 반복 기회 없음 — 원문 일치), DORA 2025(약 5,000명·90%·처리량 양·안정성 음, 상관 분석 명시).
- 수치 약 30건, 날짜 약 20건, 인용 8건 확인.

### 미해소
- (없음)

## 02장 (라운드 1)

대조 근거: `01_reference.md` §2.1, `research/papers.md` D1–D12·B10, `research/web.md` 자료 3·12·17. 원문 대조(curl, 2026-09-28): danshapiro.com(2026-01-23), martinfowler.com Kief Morris(2026-03-04), justin.abrah.ms Yegge 8단계 목록(2026-01-08), anthropic.com/research/measuring-agent-autonomy(2026-02-18), arXiv 초록(Feng 외 2506.12469, Hedwig 2605.11495, Galster 외 2602.14690).

### ❌ 정정
- Yegge 8단계: "다른 블로그에 인용된 문장으로 확인한 것은 1·5·6·7·8단계뿐이다 … 2~4단계의 원래 문구는 확인하지 못했으니 추측으로 빈칸을 채우지는 않겠다" → Stage 2~4 내용을 채움("IDE 사이드바 에이전트가 도구마다 허락을 구함 / 권한 확인을 끈 YOLO 모드 / 에이전트가 화면을 채우고 코드는 diff로만"). 근거: 레퍼런스가 인용한 바로 그 블로그(justin.abrah.ms, 2026-01-08)가 Stage 1~8 전체를 원문 그대로 옮겨 두었음("Stage 2: Coding agent in IDE, permissions turned on…", "Stage 3: Agent in IDE, YOLO mode…", "Stage 4: In IDE, wide agent… Code is just for diffs."). 출처 서술도 "Gas Town을 소개하는 글에서"(원 블로그: "In Welcome to Gas Town, Steve Yegge generated a list…")로 보강. **계획(02_plan.md 2장 "2~4 문구는 없다고 밝힌다")과 달라지는 지점이다.**
- 대응표 Yegge 열: 2단계 협업 "(문구 미확인)" → "Stage 2", 3단계 위임 "Stage 5~6" → "Stage 3~6". Stage 2(도구마다 허락)는 책의 2단계(행동마다 승인)와, Stage 3~4(권한 확인 끔)는 책의 3단계(자동 승인)와 정의가 맞는다. 표는 본문이 이미 "이 책이 정리한 해석"으로 명시 — 운영자가 해석 대응을 한 번 확인할 것.
- Kief Morris 루프 안: "루프 안의 사람은 그 코드를 직접 고친다" → "직접 고치거나, 에이전트에게 그 자리를 고치라고 시킨다" / 다음 문단 "코드를 직접 고치면" → "산출물만 고치면" — 원문: "The 'in the loop' way is to fix the artefact, whether by directly editing it, or by telling the agent to make the correction we want." 루프 안/위를 가르는 기준은 손으로 고치느냐가 아니라 산출물을 고치느냐 하네스를 고치느냐임.
- Anthropic 자율성 연구: "복잡한 작업에서는 Claude Code가 스스로 멈춰 … 두 배를 넘었다" → "가장 복잡한 작업에서는" — 원문: "On the most complex tasks, Claude Code stops to ask for clarification more than twice as often as humans interrupt it."

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (추가 없음) — 사용 데이터 연구는 발표일(2026-02-18) 명기.

### ✅ 확인 (요약)
- Shapiro: 2026-01-23, L0~L5 명칭, L0 "not a character hits the disk without your approval", L3 "You're not a senior developer anymore … You are… a manager.", L4 "You write a spec. You argue with it about the spec. You craft skills", "almost everyone tops out here"(3단계), "level 2, and every level after it, feels like you are done" — 원문 일치.
- Kief Morris: 2026-03-04 martinfowler.com, why/how 루프, outside/in/on, "Agents can generate code faster than humans can manually inspect it", "most visible in what we do when we're not satisfied…", 블록 인용 "The right place for us humans is to build and manage the working loop…" — 원문 그대로 일치.
- 자동화 수준: Sheridan & Verplank 1978(해저 원격 조작기, 10단계 — 원문 미열람, 레퍼런스 기준), Parasuraman·Sheridan·Wickens 2000 10수준 표·4기능·1차/2차 기준(papers.md D2, INL 재수록본 대조), 오른쪽 열이 원 논문에 없는 대응이라는 명시 확인.
- Feng·McDonald·Zhang 2025: 에세이(Knight 1st Amendment Institute 시리즈), operator→observer 5단계, 블록 인용 — arXiv 초록 원문 그대로 일치.
- Meredith Ringel Morris 외 Levels of AGI(Google DeepMind, ICML 2024 position), "No AI"~"AI as an Agent"; Shneiderman 2020 두 축 — papers.md D7·D8.
- Anthropic 2026-02-18(자사 연구 명시): 도구 호출 998,481건(약 100만)·세션 50만, 자동 승인 50세션 미만 약 20% → 750세션 40% 초과, 개입 약 10세션 5% → 경험자 약 9% — 원문 일치.
- Hedwig(Shukla 외, 21명, 동적 자율성), Galster 외(2,853개 저장소, 컨텍스트 파일 우세·유일 메커니즘인 경우 많음·AGENTS.md 부상·스킬/서브에이전트 드묾) — arXiv 초록 일치.
- 수치 약 15건, 날짜 6건, 인용 7건 확인.

### 미해소
- (없음)

## 03장 (라운드 1)

대조 근거: `01_reference.md` §0.2~0.3·§4·§9.2(#10·#18·#23), `research/web.md` 자료 22~45·61, `research/papers.md` A1·A3·E10, `research/community.md` 분업표. 원문 대조(2026-09-28): arXiv 2606.17799(Gorinova 외)·2609.08149(SWE-Bench Pro Verified) 초록, epoch.ai SWE-bench Verified 리뷰, platform.claude.com 모델 개요, developers.openai.com GPT-6 Luna·Sol 모델 문서(.md), research.meta.ai Muse Spark 1.3, TechCrunch Muse Code(2026-08-05), x.ai Grok Build, docs.github.com Copilot cloud agent. openai.com 원문(SWE-bench Verified 중단 글)은 403 — Epoch AI 인용과 보도(2026-02-24)로 확인.

### ❌ 정정
- 모델 표 Claude Fable 5.1 모델 ID "—" → `claude-fable-5-1`, GPT-6 Luna 모델 ID "—" → `gpt-6-luna` — 각각 Anthropic 모델 개요(Claude API ID 열)와 OpenAI 모델 문서("Model ID: `gpt-6-luna`")에서 확인. 틀린 값은 아니었으나 표가 "모델 ID" 열을 두고 있어 확인된 값으로 채움.
- `roles.yml` 예시: `model: Claude Fable 5.1   # 모델 ID는 공식 문서 확인` → `model: claude-fable-5-1`, `model: GPT-6 Luna # 모델 ID는 공식 문서 확인` → `model: gpt-6-luna` — 위와 같은 근거. "공식 문서 확인" 보류 주석을 확인값으로 닫음.

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (추가 없음) — 모델 표에 "2026년 9월 28일 기준", 표면 절에 "2026년 9월 기준", 리서치 프리뷰·gh-aw 0.x 휘발성 경고, 출시 6일째 단서가 이미 있음.

### ✅ 확인 (요약)
- Gorinova 외(2026) 포지션 논문 블록 인용 — arXiv 초록 원문 그대로 일치(2026-06-16 제출). 저술가의 "추출 인용" 표시는 해소.
- SWE-bench: 2023-10 발표·Claude 2 1.96%(초록), Verified 500문항·전문가 검토. OpenAI 보고 중단: Epoch AI 리뷰 원문 "On February 23, 2026, OpenAI released their audit results. They audited 27.6% of the tasks, finding that 59.4% had flawed test cases that rejected functionally correct submissions", "all frontier models tested 'have seen at least some of the problems and solutions during training'" — 본문 서술·괄호 출처 표기와 일치. SWE-bench Pro 권고(보도 확인). SWE-Bench Pro Verified(2026-09-08, 정답 누출·숨은 평가 정보를 통한 보상 해킹·과제 결함) — arXiv 초록 일치.
- 모델 표: Opus 5.5 2026-09-22·`claude-opus-5-5`·"For long-running agentic coding and knowledge work", Fable 5.1 "demanding reasoning and long-horizon agentic work", Anthropic 모델 안내 문장(원문 일치), GPT-6 Sol·Luna 2026-09-22·`gpt-6-sol`·Luna "focused, high-volume tasks"(OpenAI 문서 일치), Grok 4.7 2026-09-21·`grok-4.7`(상충 #10 — 4.7 채택 일치), Muse Spark 1.3 2026-09-02. "비용 면에서 매력적"은 Alexandr Wang의 WSJ 발언(TechCrunch Muse Code 기사 인용)으로, Muse 계열에 대한 Meta 측 발언 — "Meta 측 발언" 라벨로 충분.
- 커뮤니티: Ask HN 2026-09-25(출시 사흘째) 20시간 무입력 실행, Codex 체감(Reddit 2차 정리), velog "AI 하나는 의견, 둘의 토론은 검증", AWS KR 교차 채점 실험, HN "한 LLM이 만들고 다른 LLM이 리뷰해도 단일 패스", Yegge 설계 Fable·구현 Opus 5("전해진다"), "둘 다 쓰라" — 모두 "커뮤니티 보고"로 표시돼 있고 레퍼런스와 일치.
- 표면: `claude -p`·Agent SDK·`--bare`(훅·MCP 자동 로드 생략)·`--output-format json`의 `total_cost_usd`, `codex exec` 기본 읽기 전용·`--sandbox workspace-write`, `claude-code-action@v1` 대화/자동화 모드, `codex-action` `safety-strategy` 기본 `drop-sudo`, Copilot cloud agent 59분 하드 리밋(docs.github.com 원문 일치), gh-aw 엔진, `claude --cloud`·`--teleport`·"Plan locally, execute in the cloud", Codex cloud 시작 채널, `learn.chatgpt.com` 이전, 루틴 트리거 3종, Claude Code Review·`@codex review` P0/P1, 리서치 프리뷰·gh-aw 0.x.
- 보조 설비: Grok Build plan 모드·워크트리 병렬 서브에이전트·`-p`, "Your AGENTS.md, plugins, hooks, skills, and MCP servers all work out of the box"(x.ai 원문 일치), HN 오픈소스 스레드 반응·데이터 반출·ZDR 엔터프라이즈 전용(커뮤니티 보고). 발표일은 본문에 없음(상충 #9 회피 확인). Muse Code 2026-08-05 베타·Zuckerberg "fans out to separate sub-agents working in parallel in isolated worktrees"(TechCrunch 원문 일치), Muse Spark 1.3 도구 호출 ~20%·토큰 ~25% 감소·프롬프트 인젝션 내성(Meta 원문 일치, 벤더 주장 라벨 있음), dev.to 리뷰 2026-09-04.
- 이식성: AAIF 2025-12-09(LF, AGENTS.md·MCP·goose 기부), Claude Code의 AGENTS.md 단독/병행 읽기(code.claude.com 원문), Codex `## Code Review Rules`, 토스 `apps-in-toss-harness` README 문구, `codex-plugin-cc`·`/codex:review`, addyosmani/factory의 정본+어댑터 구조, Grok 4.5/4.6 → 4.7.
- 벤치마크 수치 금지·GPT-6 Astra 날짜·Grok Build 발표일 미기재 — 계획의 주의 사항 준수 확인.
- 참고(부록 A 담당용): OpenAI 문서상 GPT-6 Luna는 1,050,000 컨텍스트·128K 최대 출력·지식 컷오프 2026-05-18·$0.1/$0.01(캐시)/$0.5 per 1M. 레퍼런스 §4.1에서 "(미수집)"이던 값이다.

### 미해소
- (없음)

## 13장 (라운드 1)

대조 근거: `01_reference.md` §2.1(6)·§2.4·§4.2·§4.6·§9.1 논쟁 E·H·§10, `research/web.md` 자료 9·23·26·28·29, `research/papers.md` B6·B11·D2·D12, `research/community.md` 패턴5·휴리스틱14·1인레시피·인물표. 웹 2차 확인(2026-09-28): anthropic.com/research/measuring-agent-autonomy(원문), `gh api`로 anthropics/claude-code#73125·#60705, openai/codex#28969의 생성일·제목·스태프 답변.

### ❌ 정정
- "복잡한 작업에서 Claude Code가 스스로 멈춰 확인을 요청한 빈도는 사람이 끼어든 빈도의 두 배를 넘었다" → "가장 복잡한 작업에서 …" — 원문: "On the most complex tasks, Claude Code asks for clarification more than twice as often as humans interrupt it." (Anthropic, 2026-02-18). 조건이 "가장 복잡한 작업"으로 한정됨. 저술가 요청 항목.

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (추가 없음) — 루틴·Symphony는 "프리뷰 단계라 빠르게 바뀔 수 있으니 공식 문서를 함께 확인하자"가 이미 있음. 루틴 트리거·한도는 "2026-09 기준"으로 명기됨. MAST는 "(당시 모델 기준)" 명기.

### ✅ 확인 (요약)
- 60초 사태: #73125 생성 2026-07-02(제목 "AskUserQuestion: No response after 60s — continued without an answer"), ThariqS 당일 사과·"/config에서 설정 가능, 기본 꺼짐" 릴리스 예고(07-02), 이슈 종료 07-04 → "2026-07-04 무렵" 유지. 버전 번호("v2.100") 미사용(상충 #13 준수). #28969 생성 2026-06-18(60초 자동 수락 비활성화 요청). #60705 생성 2026-05-19·203 댓글(`/goal` Stop 훅 문구를 허락으로 인용). 작성자 "안전 장치" 사용·병렬 세션 호소·포커스 타이머 설명은 community 패턴5와 일치.
- 결정 분류: Parasuraman·Sheridan·Wickens 5~8수준 문구(veto 6·necessarily informs 7·only if asked 8)와 네 칸 대응 일치.
- 이벤트: Igor Ostrovsky(2026-09-10) 정의·1인 프로젝트 발언, 루틴 정의 원문(프롬프트·저장소·커넥터), "컴퓨터가 꺼져 있어도"(개요 문서 원문), 트리거 3종(스케줄 최소 1시간·일회성, `/fire`+bearer, GitHub PR·release), `claude/` 접두 브랜치·보호 브랜치 거부·계정별 일일 한도, 사례 6종(배포 검증·알림 트리아지·백로그·문서 드리프트·포팅), 녹색 표시 문장·"appears as you" 원문 일치. `claude-code-action` automation 모드(prompt 있으면 cron 포함 모든 이벤트), 클라우드 세션·PR Auto-fix, Codex 팀 automations(Every 팟캐스트, "팟캐스트 보고" 표기), OpenAI 기술부채 "가비지 컬렉션"(자료 9).
- Actions YAML: `anthropics/claude-code-action@v1`의 `anthropic_api_key`·`prompt`·`claude_args` 입력, `claude_args` 안의 `--model claude-opus-5-5`·`--allowedTools "mcp__github__list_commits,mcp__github__list_issues"`(공식 문서 예약 실행 예시 원문), `--max-turns`(공식 문서 "Set `--max-turns` in `claude_args` to limit iterations") — 모두 실재. 값 10은 저술가 선택값. cron "30 22 * * *" = UTC 22:30 = KST 07:30 계산 일치. `jobs`·`runs-on`·`steps`는 표준 Actions 키. 비용 가드(`--max-turns`·워크플로 타임아웃·concurrency) 원문 일치.
- 1인 야간 팩토리: "사람 게이트 1~3개 + draft PR"(휴리스틱14), addyosmani/factory `STOP_IF`, Jake Saunders(2026-08-21, 중고 서버·Forgejo+러너·Coolify·월 £20 Codex 구독, 박스 재설치·키 교체, "5분마다 나를 부르는 것"↔"발사 코드") 일치.
- 팀 온콜: Hassan 외 arXiv:2509.06216(v1 2025-09-07, 형식·시점 정상) MRP·CRP 명칭, AEE 정의 초록 요지 일치. Symphony proof of work 4종·Linear 제어면·engineering preview("500%" 미사용), 토스 증거 영상 루프, Will Larson(2026-09-20, 공통 작업 관리 시스템 부재·Linear 단일 진실 공급원·목표 상태를 머릿속에 쌓아 둠) 일치.
- 무리 vs 결과: Gas Town 역할 5종·Beads·Appleton "thousands of dollars a month in API costs"(원문 그대로만 사용), Factory Missions(수 시간~수일, 병렬 트랙), 동적 워크플로(수십~수백 서브에이전트), MAST(7개 프레임워크·1,600+ 기록·14개 모드·"often minimal", 초록 일치), Kent Beck「Nobody Wants Agents」(2026-04-23) 요지, gh-aw 스레드 root_axis 20달러(커뮤니티 보고 표기).
- 수치 약 15건, 날짜 약 12건, 식별자 4건(이슈 3·arXiv 1), 명령·입력 7건 확인.

### 미해소
- (없음)

## 14장 (라운드 1)

대조 근거: `01_reference.md` §2.3·§2.4·§2.5·§3.1~3.3·§6.5·§9.1 논쟁 A·D·E·§9.2 #3·#8·#19, `research/web.md` 자료 1·2·5·9·11, `research/papers.md` C7·C8·D14·E11·E13, `research/community.md` 패턴2·3·6·9·논쟁A·D·인물표. 웹 2차 확인(2026-09-28): OpenAI 하네스 엔지니어링 글 원문 전재본(jaytaylor.com 노트 — openai.com은 403, 검색 결과의 원문 문장과 교차 일치), arxiv.org/html/2511.04427(He 외 표 2), claude.com 플레이북 원문, factory.strongdm.ai 원문(curl).

### ❌ 정정
- "엔지니어 7명이 5개월 동안 … 약 1,500개 PR" → "엔지니어 셋으로 시작해 일곱으로 늘어난 작은 팀이 5개월 동안 …" — 원문: "roughly 1,500 pull requests have been opened and merged with a small team of just three engineers driving Codex. … the throughput has increased as the team has grown to now seven engineers." 1,500 PR은 주로 3인 팀 기간의 산출. 날짜 2026-02-11·0줄·약 100만 줄은 원문 일치. 원문을 확인했으므로 괄호의 "원문 403이라 2차 요약 경유" 단서는 삭제. **레퍼런스 §3.2·web.md 자료 9의 "7명"도 같은 오류 — 다른 장에서 인용 시 주의.** 저술가 요청 항목.
- 비교표 "사람도 사보타주의 94%를 놓치고" → "참가자의 94%가 사보타주를 놓쳤고" — 초록: "94% of developers fail to detect sabotage". 비율의 분모는 사보타주 건수가 아니라 참가자.
- "StrongDM의 세 번째 원칙은" → "StrongDM이 원칙 끝에 "실용적인 형태"로 붙인 문장은" — factory.strongdm.ai 원문은 kōan form("Why am I doing this?") → rule form 두 줄 → "Finally, in practical form: If you haven't spent at least $1,000 …" 순서. "세 번째 원칙"으로 셀 근거가 없음. 1장 final의 "원칙에는 세 번째 줄이 붙어 있다"와는 충돌하지 않음(편집자 참고).

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (추가 없음) — He 외·Xu 외에 "둘 다 당시 도구 기준" 명기, Anthropic 플레이북·PostHog·Addy 글에 날짜 명기.

### ✅ 확인 (요약)
- He 외(MSR 2026): 도입 806개 vs 성향 점수 매칭 1,380개, 속도 증가는 일시적, 정적 분석 경고 +30.26%(±6.66%)·코드 복잡도 +41.64%(±7.62%) — arXiv HTML 표 2 원문 일치("sustained", "persists beyond the initial adoption period"). 품질 악화→장기 속도 저하(패널 GMM) 일치. 저술가 요청 항목.
- Xu 외(arXiv:2607.01810, 2026-07-02): 설정 파일 첫 커밋 식별, Python 인지 복잡도 약 +11%(기존 추정의 1/4), 전 언어 순환 복잡도 +3~4%, 신규 기여자 유입 감소 없음 — 상충 #3 처리대로 조건 병기.
- Anthropic AI-Native SDLC 플레이북(Louis Claxton, 2026-08-21) Deploy 행 "Layers of agentic review with human review reserved for regulated and critical code." — 원문 첫 문장 그대로(뒤에 "Governance is enforced as the AI acts…"가 이어짐). 저술가 요청 항목.
- StrongDM: "validation replaces code review"(블로그), DTU, "$1,000 on tokens today per human engineer"(원문 일치). Willison 조건부 "$20,000/month" — 상충 #19대로 조건부 환산으로만 서술. HN 반응(codingdave·japhyr·jpollock·navanchauhan), Rust 코드 비판(clone·에러 처리·800줄 클로저) — 커뮤니티 보고 표기. 댓글 수 미사용.
- Lopopolo 발표 요지(0% 코드·머지 전 리뷰 0%·머지 후 표본·하루 10억 토큰, Latent Space 2026-04-07 — "발표에서 전해진 요지"), 커스텀 린터로 계층 아키텍처 강제(자료 9), 하네스를 고치는 원칙(휴리스틱2), 무한 병렬·GPU·토큰 제약(논쟁D).
- Boris Cherny(Fortune 2026-06-11) 손코딩 8개월 0·100%, 다중 페르소나 PR 리뷰+사람 최종 승인. iamwil·adamtaylor_13 증언.
- Dex Horthy(WSFF 문서·AI Engineer 2026-07, HumanLayer 판매자 표기), 보상 신호·초 단위 vs 주 단위, HumanLayer 4개월 후 복귀(Addy 인용), 앞단 재투자 처방. HN「Nobody has built a software factory」(2026-08-31)·mentalgear(2026-09-20)·swiftcoder·pydry·CuriouslyC/kaicianflone, Kent Beck 테스트 삭제 성향.
- SpecBench 10배당 28%p, METR "roughly half … would not be merged", Echoes of AI 151명·유지보수성 차이 없음, 사보타주 약 5시간·94%·모니터 조건 56%.
- 한도가 1순위 고통(패턴6: #38335 873댓글·codex#14593 630댓글), Addy「Software Factories, Light and Dark」(2026-07-22), Igor 정형화 작업, PostHog(2026-08-11), Böckeler "direct it to where our input is most important"(자료 11 원문 요지).
- 수치 약 20건, 날짜 약 12건, 인용 4건 확인.

### 미해소
- (없음)

## 15장 (라운드 1)

대조 근거: `01_reference.md` §2.4·§2.5·§9.1 논쟁 F·§10 25번, `research/papers.md` C4·C14·D4·D5·D6·D14, `research/community.md` 패턴2·11·논쟁F·영상. 웹 2차 확인(2026-09-28): arXiv:2601.20245 초록, anthropic.com/research/AI-assistance-coding-skills(검색 결과의 원문 문장, InfoQ 보도 교차).

### ❌ 정정
- "10년 넘게 TDD를 해 온 개발자가" → "10년 동안 TDD를 해 온 개발자가" — community.md: 「AI 없이 보낸 한 달」 저자는 "10년 TDD 경력". "넘게"는 근거 없음.

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (추가 없음) — Shen & Tamkin "(자사 연구, 당시 모델 기준)", METR "(당시 도구 기준)" 명기.

### ✅ 확인 (요약)
- Shen & Tamkin(arXiv:2601.20245, 2026-01-28): 52명의 개발자, Python Trio, 무작위 실험, AI 집단 퀴즈 "17% lower"(Anthropic 연구 글 원문 "participants in the AI group scored 17% lower than those who coded by hand" — "약 17%" 유지), 디버깅 격차 최대, "without delivering significant efficiency gains on average", 완전 위임자는 약간 빨랐으나 학습 손실("some productivity improvements, but at the cost of learning the library"), 여섯 패턴·저득점 3·고득점 3, 결론 문장 "AI-enhanced productivity is not a shortcut to competence" — 초록 원문 일치. 저술가 요청 항목.
- Bainbridge(1983, Automatica) 요지만 사용 — 유명 문구 미인용(계획 준수). Simkute 외(Microsoft Research) 네 요인(초록 일치), Parasuraman & Manzey(2010)·Lee & See(2004) 요지, 사보타주 모니터 조건 56%("절반 넘게").
- "감독에 필요한 기술이 위축될 수 있다"는 관찰을 특정인에게 귀속하지 않음(상충 #15 준수). Karpathy "이해는 외주할 수 없다" 미사용.
- Litt(Notion, AI Engineer 2026-07) 이해의 병목·검증 vs 참여 이해·이해 의례 4종, 세 부채(Addy comprehension debt·Storey cognitive debt·당근 박용권 의도 부채, jdw64 반론), Lars Faye·HN support group(2026-07-10)·60세 개발자(2026-03-07)·Karpathy agentic engineering, Addy "설명하지 못하면 배포하지 마라"(발표 요지), METR 2025 19%(상충 #2대로 논문 원문 값), Boris Cherny 신규 입사자 현상(Fortune 2026-06-11), AGENTS.md 약 100줄 목차(자료 9), DORA 7역량, Opus 5.5·GPT-6 Sol 같은 주(2026-09-22) 출시.
- 수치 약 8건, 날짜 약 8건, 인용 2건 확인.

### 미해소
- (없음)

## 09장 (라운드 1)

대조 근거: `01_reference.md` §8·§2.4·§3.3·§4.2~4.4, `research/web.md`(자료 23·24·26·27·28·31·32·37·47~53)·`papers.md`(C9·D14)·`community.md`(패턴4·12, 휴리스틱6). 웹 2차 확인(2026-09-28): arXiv:2606.23130 초록, Aikido PromptPwnd 원문(aikido.dev, 2025-12-04).

### ❌ 정정
- "2차 보도에 따르면 포천 500 기업 가운데 최소 다섯 곳이 영향을 받은 것으로 확인됐다" → "Aikido는 포천 500 기업 가운데 최소 다섯 곳이 영향을 받았다고 밝혔다" — Aikido 원문에 "At least 5 Fortune 500 companies are impacted"가 있음. 원장의 "2차 보도" 라벨은 틀렸고, 발견 주체의 자체 주장이라 독립 검증된 "확인"도 아님. 발견 주체에게 귀속해 정직하게 표시. (편집자 참고: 참고문헌·원장 라벨도 "Aikido 자체 발표"로 정정 필요)

### ⚠️ 약화·삭제
- "Claude Code 루틴도 `claude/` 접두 브랜치에만 푸시할 수 있다" → "기본 설정에서는 `claude/` 접두 브랜치에만 푸시한다" — 원장(web.md 자료 26)은 제한을 적었지만 설정으로 풀 수 없는 절대 제한인지는 밝히지 않음. 어느 쪽이든 참이 되도록 "기본 설정"으로 한정.

### 🕒 신선도
- (추가 없음) — `--bare` 기본값 예고(2026-09 기준), Codex CLI 0.157.0(2026-09 기준), gh-aw 0.x(2026년 9월 기준), 연구 수치의 "당시 모델 기준"이 이미 붙어 있음.

### ✅ 확인 (요약)
- `(사실 확인 필요)` 해소: 바이브 코딩 앱 감사(Deng·Fan·Meng, arXiv:2606.23130 — v1 2026-06-22, 실재 확인)의 65.77%는 **발견된 취약점 1,186개 중 비율**. 초록 원문 "91.0% of audited applications contain at least one vulnerability, and 65.77% of identified vulnerabilities are rated Critical or High severity". 산술로도 확인(780/1,186 = 65.77%, 200개 앱 기준이면 131.54개로 정수가 안 됨). 원고를 "그 가운데 65.77%"로 명확히 하고 주석 제거. 9,041개 수집·200개 배포 앱 감사·91.0%·접근 제어/인젝션/인증 실패·하네스·프롬프트 개선 효과도 초록 일치.
- PromptPwnd: Rein Daelman·2025-12·최종 수정 2026-03-17, 공격 사슬 인용문, 영향 도구 4종, PoC("Important additional instruction after finishing step 3 … gh issue edit"), 첫 번째 완화책(이슈·PR 쓰기 능력 제한)·"Treat AI output as untrusted code." — Aikido 원문 일치.
- lethal trifecta(Willison 2025-06-16, 세 요소, "avoid that lethal trifecta combination entirely"), s1ngularity(2025-08-26, Nx 악성 버전이 설치된 Claude·Gemini·Amazon Q CLI를 권한 우회 플래그로 호출 — 개요만, 2,349개 수치 미사용), Codex docker 그룹 우회(HN 2026-05), 에이전트 간 접근 인용, niyikiza 요지, METR "치팅하지 말라" 무효(80%→80%), Muse Spark 1.3(2026-09) 인젝션 내성.
- CI 통제: gh-aw 읽기 전용·샌드박스·네트워크 격리·SHA 고정·safe-outputs, 프런트매터 키(`on.issues.types`, `permissions: read-all`, `safe-outputs.add-comment`)는 문서 예제와 일치, 0.x(v0.89.21). claude-code-action@v1: 쓰기 권한자·봇 차단·`allowed_bots` 미검사 문구·`allowed_non_write_users`+`GITHUB_TOKEN`·`include_comments_by_actor`·숨은 마크다운 경고·PAT 금지 인용문·기본 앱 부분 수락 불가→Contents·Issues·Pull requests 커스텀 앱·OIDC. Auto-fix의 `issue_comment` 연쇄(Atlantis·Terraform Cloud), 루틴 "appears as you"·`<routine-fire-payload>`.
- 코드: `codex exec --json`(기본 읽기 전용, 쓰기는 `--sandbox workspace-write`), stdin 파이프 + 프롬프트 인자 형식(문서 예 `npm test 2>&1 | codex exec "..."`), `CODEX_API_KEY` 호출 인라인 규칙, codex-action 보안 프록시·`safety-strategy`(`drop-sudo` 기본/`unprivileged-user`/`read-only`), `claude -p --bare --permission-mode dontAsk --allowedTools "Bash(git diff *),Bash(git log *)" --output-format json` — 플래그 전부 web.md 자료 24 원문에 있음. `--bare` 인용문·CLAUDE.md 자동 탐색 생략·`dontAsk` 정의 일치.
- 실행 환경: 이그레스 인용문, 클라우드 세션 자격증명 VM 밖, Codex 0.157.0 네트워크 제한, "권한 거부면 멈추고 보고"(xg15), VM 5분 복구·devcontainer(커뮤니티), Jake Saunders "상자 재설치 + 키 몇 개 교체", Cloudflare Version URL 공개·Access, Amplify 인용문, 인시던트 에이전트 권한 3개·직접 배포 불가.
- 생성 코드·사람 리뷰: BaxBench(ICML 2025, 392개, o1 62%, 정확한 프로그램 절반가량 익스플로잇), Perry 외 CCS 2023, Ye 외 arXiv:2606.05647(2026-06-04, 100명 이상·네 프런티어 모델·약 5시간·94%·모니터 조건 56%), Anthropic 단계별 통제(계획 보안 리뷰·`/security-review`·이그레스 VM·CI 복수 리뷰어·사람 표본·DAST·외부 펜테스트·SIEM), Jason Clinton 부CISO·클로징 인용문.
- 수치 약 20건, 날짜 약 10건, 인용 9건, 플래그·키 약 15건 확인.

### 미해소
- (없음)

## 부록 A (라운드 1)

대조 근거: `01_reference.md` §0.2·§4.1~4.7·§9.2 #9·#18·#21·#22·§9.3, `research/web.md` 자료 14~17·22~34·37·39·42~48·50. 버전·가격은 핵심 주장으로 보고 1차 재확인(2026-09-28): `gh api` 릴리스·태그(anthropics/claude-code, claude-code-action, openai/codex, openai/codex-action, github/gh-aw, github/spec-kit, gastownhall/gastown, xai-org/grok-build), platform.claude.com 모델 개요, developers.openai.com GPT-6 Sol·Luna 모델 문서, docs.x.ai 릴리스 노트, learn.chatgpt.com 비대화형 모드 문서. 03장 fact-checker 공유 사항(Luna 값·모델 ID) 반영.

### ❌ 정정
- `codex exec` 표 `--ephemeral` "이름 그대로 일회성 실행. 세부 동작은 공식 문서에서 확인" → "세션 기록(rollout) 파일을 디스크에 남기지 않는다" — 공식 문서 원문: "Use `--ephemeral` when you don't want to persist session rollout files to disk." 플래그 이름에서 추측한 설명을 문서 값으로 교체. 저술가 요청 항목.
- 모델 표 Claude Fable 5.1 "— / $10 / — / $50 / — / — / —" → 모델 ID `claude-fable-5-1`, 캐시 읽기 $0.25, 1M / 128K, 적응형 사고 상시·effort 기본 `high`, 컷오프 2026-06 — Anthropic 모델 개요 원문(가격 주석 "prompt cache reads cost … 2.5% on Claude Fable 5.1" → $10×2.5% = $0.25). 출시일은 1차 출처 미확인이라 "—" 유지. 틀린 값은 아니었으나 표의 "—" 정의(1차 미확인)에 더는 해당하지 않음.
- 모델 표 GPT-6 Luna "—" 칸 → `gpt-6-luna`, $0.1 / $0.01 / $0.5, 1,050,000 / 128K, `none`~`max`(기본 `medium`), 컷오프 2026-05-18 — OpenAI 모델 문서 원문(03장 로그 공유 값과 일치, 직접 재확인).
- Grok 4.7 용도 "xAI의 코딩·지식노동용 최고 모델" → "코딩·에이전트 작업·지식노동용 프런티어 모델" — 릴리스 노트 원문 "SpaceXAI's frontier model designed for coding, agentic tasks, and knowledge work".

### ⚠️ 약화·삭제
- 머리말 규칙 "모든 값은 … 벤더의 공식 문서·릴리스 노트·모델 페이지에서 가져왔다 … 2차 보도에만 나오는 값은 싣지 않았다" → "메모에 따로 밝힌 Grok Build 버전 하나를 빼면 … 저장소에서 가져왔다 … 그 밖에 2차 보도에만 나오는 값은 싣지 않았다" — A.2의 Grok Build v1.0.40은 2차 릴리스 추적(releasebot) 값이고, 공식 저장소 xai-org/grok-build에는 태그·릴리스가 없어 1차 확인 불가. Gas Town·Spec Kit 값은 벤더 문서가 아니라 저장소 값. 규칙과 표가 서로 어긋나지 않게 규칙 문장을 좁힘.

### 🕒 신선도
- (추가 없음) — 제목·머리말·A.4 소제목에 "2026-09-28 기준"·"v2.1.28x 문서 기준"·"0.157.x 문서 기준" 명기, 휘발성 경고 있음.

### ✅ 확인 (요약)
- 모델: Opus 5.5 2026-09-22·`claude-opus-5-5`·$4/$0.20(캐시 읽기 5%)/$20·1M/128K·적응형 사고 상시·effort 기본 `medium`·컷오프 2026-06·용도 문구·모델 선택 권고 문장(모델 개요 원문 일치). GPT-6 Sol `gpt-6-sol`·$2/$0.2/$10·1,050,000/128K·effort 6단계(기본 `medium`)·컷오프 2026-04-20(모델 문서 원문 일치), 배포 대상·"GPT‑5.6 promotional pricing 대비 50%"(공지). Grok 4.7 `grok-4.7`·500k·$2/$0.50/$6(200k 이하)·`low`~`xhigh`(기본 `high`)·"SpaceXAI" 표기(릴리스 노트 원문). Muse Spark 1.3 연혁·~20%/~25% 감소·Muse Code 2026-08-05 베타(Meta 1차, 03장 로그 교차).
- 도구 버전(`gh api`): Claude Code v2.1.283 2026-09-25, claude-code-action v1.0.235 2026-09-25·`v1` 2025-08-26, Codex rust-v0.157.0 2026-09-25·rust-v0.157.1 2026-09-26(latest 안정판)·0.159.0-alpha.11 2026-09-28, codex-action 태그 v1.12·GitHub Releases 0건·최종 push 2026-09-19, gh-aw v0.89.21 2026-09-23(최신 비-프리릴리스, 이후 v0.89.22는 프리릴리스), Spec Kit v1.0.12 2026-09-25, Gas Town v1.2.1 2026-06-06·최종 push 2026-09-18 — 전부 일치. v2.1.283의 `/doctor prompt-audit`·`deniedModels`(체인지로그 원문).
- 플래그·입력: `claude -p`의 `--bare`(원문 두 문장), `--output-format json`의 `total_cost_usd`, `--json-schema`, `--allowedTools`, `--permission-mode auto|dontAsk|acceptEdits`(dontAsk 원문), `--permission-prompts none`, `--continue/--resume`, `--max-turns`·`--model`을 `claude_args`로 넘기는 공식 예시, `--cloud`·`--teleport`. `codex exec` 기본 read-only·git 저장소 필요·`--skip-git-repo-check`·`--sandbox workspace-write`·`--full-auto` deprecated·`--json` JSONL·`--output-schema`(JSON Schema 최종 응답)·`-o/--output-last-message`(최종 메시지를 파일로 — 원문 "write it to a file with `-o <path>`", 저술가 요청 항목 확인)·`resume --last`·`CODEX_API_KEY` 인라인 규칙(원문 일치). claude-code-action `prompt`/interactive 모드, `allowed_bots`("Allowed bots are not checked for repository permissions"), `allowed_non_write_users`+`GITHUB_TOKEN`, `include_comments_by_actor`, `show_full_output` 기본 비활성, codex-action `safety-strategy` 4값·`permission-profile ":workspace"`, gh-aw 프런트매터·`safe-outputs`·`gh aw compile`.
- 기능 매트릭스·문서 위치: Copilot cloud agent 59분 하드 리밋·Jira 할당, gh-aw 엔진 5종, Codex cloud 시작 채널 5곳, 자동 리뷰 P0·P1, Grok Build `-p`·AGENTS.md, Wrangler v4.21.0+·2025-07-22 발표·"Version URLs, previously called preview URLs", 문서 URL(learn.chatgpt.com 308 이전, factory.ai→factory.com 307 포함) 레퍼런스와 일치.
- 계획 준수: 벤치마크 점수 0건, Muse Spark API 가격 미기재(언급만), "GPT-5.6 Sol" 미사용, Grok Build 발표일 미기재(상충 #9).

### 미해소
- (없음)

## 부록 B (라운드 1)

대조 근거: `01_reference.md` §4·§5·§6.3·§10, `research/web.md` 자료 10·14~16·23·26~29·33·39·40·46~48·57·60·61, `research/community.md` 1인레시피·휴리스틱3·8·14. 웹 추가 확인 없음(레퍼런스로 판정 완료).

### ❌ 정정
- (없음)

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- B-13 "GitHub Agent HQ(public preview, Copilot Pro+·Enterprise)" → "GitHub Agent HQ(2026-02 발표 기준 public preview, …)" — 상태 근거가 2026-02-04 GitHub 블로그(자료 40)뿐이라 시점 명기.

### ✅ 확인 (요약)
- B-1 계획 우선·1시간 이하 티켓(HCAST)·`claude --cloud`·Every compound engineering, B-2 30만 줄 SaaS 훅 강제(HN cadamsdotcom, 커뮤니티 보고 표기)·exit code 2·PreToolUse/Stop, B-3 Ralph Stop 훅 플러그인·`--completion-promise`·`--max-iterations`, B-4 initializer·기능 목록 JSON pass/fail·`init.sh`·조기 완료 선언 실패 유형(자료 10), B-5 `/batch` 5~30 워크트리·에이전트 팀 파일 소유 분할, B-6 동시 16·실행당 최대 1,000·무진전 2회.
- B-7 Spec Kit Specify→Plan→Tasks→Implement, Kiro requirements→design→tasks·웨이브, B-8 genai-jerry(`factory:*` 라벨·사람 게이트 3·스테이징)·addyosmani/factory(`STOP_IF`·독립 검증자), B-9 Salman Ali Banani(2026-07-04) 흐름·수정 1회·자동 승인 없음·`reviewed_by_codex`·머지까지 Claude(원문 일치), `/codex:adversarial-review`.
- B-10 Cloudflare 최대 7개 리뷰어·재리뷰 수렴(Important만)·하이퍼리즘 Claude Agent SDK·LY Caller–Executor, B-11 `npx wrangler preview --name "pr-<번호>" --json`·`wrangler preview delete`·Version URL 공개·Access·Durable Object 미생성·Amplify 50 브랜치 쿼터·공개 저장소 IAM 롤 차단(원문 일치), B-12 PR Auto-fix·`@codex fix`·`issue_comment` 연쇄 경고·`npm test | codex exec`, B-13 Copilot·Claude·Codex 동시 할당·59분 상한.
- B-14~B-16 루틴 배포 검증·알림 트리아지 원문, 녹색 표시 문장, `<routine-fire-payload>` 신뢰 불가 데이터 표시(원문 일치), 최소 1시간 간격, OpenAI 백그라운드 Codex 가비지 컬렉션.
- 프리뷰·베타 휘발성 경고(루틴·Claude Code Review·에이전트 팀·Agent HQ·gh-aw) 있음.

### 미해소
- (없음)

## 10장 (라운드 1)

대조 근거: `01_reference.md` §2.5·§5.4·§7.2·§7.4, `research/web.md`(자료 5·27·33·56·57·59·61)·`papers.md`(C5·C10)·`community.md`(패턴1, 휴리스틱7·11). 웹 2차 확인(2026-09-28): 카카오페이 기술블로그 원문(tech.kakaopay.com/post/kakaopayins-slow-pr-fast-dev/).

### ❌ 정정
- "Dex Horthy는 … 나쁜 PR이 많다는 데 있다. 에이전트는 리뷰받기 좋게 쓰지 못한다. 한 번에 너무 큰 변경을 만들고 무관한 코드를 건드린다." → "… 나쁜 PR이 많다는 데 있다. 다른 실무자는 에이전트가 리뷰받기 좋게 쓰지 못한다고 짚는다. …" — 원장(§7.2, community 패턴1)에서 "나쁜 PR이 많다"만 Dex Horthy, "리뷰받기 좋게 못 쓴다·너무 큰 변경·무관한 코드"는 HN danpalmer. 원고 흐름상 Horthy 발언으로 읽혀 귀속 분리.

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (추가 없음) — Faros "2025년 중반 도구 기준", 연구 "당시 모델 기준", AI 리뷰어 표 "2026년 9월 기준", Claude Code Review research preview 경고가 이미 있음.

### ✅ 확인 (요약)
- 카카오페이손해보험(원문 대조): long.black·재무서버개발팀·2026-06-12, 제목, 인용 3건·"왜 이렇게 했는가에 대한 답이 자명한가?", 1인 일평균 PR 0.8→1.7건, 리뷰어 1명 63%, **파일 수는 중앙값** 14→5(원문이 중앙값으로 명시 — 원장 표기가 모호했으나 원고 "중앙값"이 맞음), 변경 라인 중앙값 246→158, 200줄 이하 PR 37%→60%, 조르깃 4단계·태그 `[r]`/`[c]`/`[a]`·코멘트 188개 중 30건(16%). 모두 자사 측정 라벨 있음.
- 현상: 플레이북 인용문("When agents multiply code output …" — web.md 자료 5), Faros 2025-07(1,255팀·1만+ 명, 머지 PR +98%·리뷰 시간 +91%·PR 크기 +154%, 회사 수준 상관 없음, 벤더 라벨), NBER +240%→릴리스 +30%, Cihan 외 ICSE 2025 SEIP(=산업 트랙)·3개 프로젝트·PR 4,335건·73.8%·5시간 52분→8시간 20분, GeekNews「AI 없이 보낸 한 달」20분/5분/이틀, Ronacher, 도장 찍기(stackskipton), 400줄/30줄(devonkelley), 당근 박용권 AI월드 2026(2026-09-09) 세 부채.
- 리뷰 재배치: GeekNews 글(~2026-08) 다섯 기능·5단계, Lopopolo 머지 후 표본 리뷰(발표 요지로 표시).
- AI 리뷰어 연구: Chowdhury 외 MSR 2026(3,109건, 45.20% vs 68.37%, −23.17%p, 60.2%·신호 0–30%, 13개 중 12개 60% 미만, 결론 인용문), Ericsson PROFES 2026(검증 이슈 200개 이상 → "200여 개", 96%, 약 69%).
- 세 형태 표: Claude Code Review(병렬 전문 에이전트·검증 단계·🔴🟡🟣·`REVIEW.md`·평균 20분·$15–25·neutral 체크런·`bughunter-severity`·"Length has a cost" 경고·재리뷰 수렴 인용문·라운드 7), `@codex review`(P0·P1·`## Code Review Rules`·`@codex fix`·"Leave mechanical checks in CI."), Cloudflare(2026-04, OpenCode·최대 7개·모델 라우팅·10줄 이하 싼 경로·131,246회→"13만여 회"·중앙값 $0.98·3분 39초·"What NOT to Flag" 두 항목), 하이퍼리즘(2025-10, 코드 유출 우려·Claude Agent SDK·체크리스트→2단계·57개 중 32개 오탐·비즈니스 로직 한계), Anthropic 실질 리뷰 코멘트 PR 16%→54%(자사).
- 수치 약 35건, 날짜 약 8건, 인용 9건 확인.

### 미해소
- (없음)

## 11장 (라운드 1)

대조 근거: `01_reference.md` §2.4·§2.5·§3.3·§3.4·§4.7·§7.1·§7.3·§7.4·§7.6, `research/web.md`(자료 5·38·54·58·61)·`papers.md`(C6·C10·C11·D3·D4)·`community.md`(팀역학, 휴리스틱2·10). 웹 2차 확인(2026-09-28): 파이낸셜뉴스 AI월드 2026 기사(https://www.fnnews.com/news/202609091826242004).

### ❌ 정정
- "국내 행사에서 MS의 이건복이 했다고 전해지는 말 … (커뮤니티 경유)" → "2026년 9월 AI월드 행사에서 마이크로소프트의 이건복이 한 말 … 사람이 잘못 수행하던 절차를 그대로 두고 AI를 끼워 넣어도 그 절차는 나아지지 않는다는 것이다(파이낸셜뉴스 보도)" — 원장에는 URL·행사·날짜 없이 한 줄뿐이었으나, 파이낸셜뉴스 2026-09-09 기사에서 이건복(마이크로소프트 솔루션 어드바이저)의 발언 원문 "기존 프로세스에 사람이 잘못 수행하던 절차를 그대로 두고 AI를 끼워 넣는다고 해서 그 프로세스가 개선되지는 않는다"를 확인. 귀속이 확인돼 이름을 유지하고 출처 라벨을 "커뮤니티 경유"에서 "보도"로 바꿈. 요지는 원문에 맞춰 "그대로 두고"를 보탬. (편집자 참고: 참고문헌에 이 기사 URL 추가 필요 — `research/*.md`에는 없음)

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (추가 없음) — DORA "2025년 보고서", Microsoft 연구 "2026-07 공개", 한국 사례별 연월 명기.

### ✅ 확인 (요약)
- 토스 김용성 2026-02(2026-02-26)·제목「Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기」·LLM 리터러시 개인차·전사→도메인→로컬 계층·"사람에겐 매뉴얼, LLM에겐 지시"·갱신 즉시 반영.
- DORA 2025(Google Cloud, 약 5,000명, 증폭기 인용문, AI 사용 90%·불신 30%, 안정성 음), AI Capabilities Model 7역량 영문명(PDF 대조 원장과 일치), 작은 배치 인용문(p.4).
- Parasuraman & Riley 1997 오용·불용·남용, Lee & See 2004 신뢰 보정(성능·과정·목적 — 논문의 신뢰 근거 세 차원과 일치).
- Anthropic 플레이북 배포 단계("Layers of agentic review with human review reserved for regulated and critical code."), 리뷰부터 플랫폼화한 한국 사례(카카오페이·LY·하이퍼리즘), Igor Ostrovsky(2026-09) 작업군 적합/부적합, Continuous AI 5범주(GitHub Next), Watanabe 외 157개 프로젝트 Claude Code PR(리팩터링·문서·테스트), J-커브는 수치 없이 커뮤니티 표시.
- Microsoft 롤아웃(Murphy-Hill 외, arXiv:2607.01418 v1 2026-07-01): 2026년 초·수만 명·Claude Code와 Copilot CLI·동료 네트워크 확산·인구통계보다 코딩 활동량·머지 PR 약 +24%·4개월 지속·"visible peer use" 인용문.
- 토스 AI Surf Day(4~6월 매주 금요일, 약 200개 클럽·142명, 해커톤 1등 인용문 원문 일치), Deepak Gupta Security Boulevard 2026-08(국민투표·처방 3가지), 경영진-현장 괴리(커뮤니티 보고).
- 공유 하네스: 우아한형제들 프론트엔드 팀 2026-04(globs·스킬, 절감 수치 미사용), `apps-in-toss-harness`(2026-08 생성, 플러그인 1·스킬 9종·MCP 2개, Claude Code·Codex·Cursor, README 인용 원문 일치), 컬리 계층형 CLAUDE.md, Cloudflare 2026-04(3,900+ 저장소 AGENTS.md·"Engineering Codex"·MCP 서버 13개), addyosmani/factory 스킬 정본+`.agents/skills/` 어댑터, Lopopolo 원칙(커뮤니티 전달로 표시), Boris Cherny CLAUDE.md 누적.
- 수치 약 20건, 날짜 약 10건, 인용 6건 확인.

### 미해소
- (없음)

## 12장 (라운드 1)

대조 근거: `01_reference.md` §3.4·§4.1·§4.2·§4.4·§4.7·§6.5·§7.3·§7.5·§9.1(논쟁 B·G)·§9.2(#12), `research/web.md`(자료 20·22·23·26·30·40·57·58·60)·`papers.md`(C6)·`community.md`(패턴6·7, 논쟁 B·G, 휴리스틱12). 웹 2차 확인(2026-09-28): GitHub anthropics/claude-code#42796 원문, Anthropic 포스트모템(anthropic.com/engineering/april-23-postmortem, 검색 결과·보도 교차).

### ❌ 정정
- "읽기 대비 편집 비율이 6.6에서 2.0으로 떨어지고" → "편집 한 번당 파일을 읽는 횟수가 6.6회에서 2.0회로 줄고" — 이슈 원문 지표는 Read:Edit = 편집당 읽기 횟수(6.6 reads per edit → 2.0). "읽기 대비 편집 비율"은 편집/읽기로 읽혀 방향이 거꾸로 됨.
- "같은 문서에 따르면 에이전트 팀은 … 약 7배" → "앞의 Claude Code 비용 문서에 따르면" — 바로 앞 문장이 Microsoft 연구라 "같은 문서"가 Microsoft로 읽힘. 7배 수치 출처는 Claude Code 비용 문서(web.md 자료 30).
- "그래서 서브에이전트의 모델을 지정할 수 없게 바뀌자 … 불만이 이슈로" → "Codex에서는 …" — 근거 이슈는 openai/codex#31814(community 휴리스틱12). 앞 문장들이 Claude Code 스레드라 도구를 명시.
- "eval 가이드는 회귀 eval의 통과율이 거의 100%여야 하고, 에이전트를 바꿀 때마다 … CI에서 돌리는 것이 … 첫 방어선" → "… 거의 100%여야 한다고 하고, 자동 eval을 … 첫 방어선" — 원문(web.md 자료 20)의 "first line of defense" 주어는 회귀 eval이 아니라 "Automated evals".

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- 비용 손잡이 표 effort 행 "(Opus 5.5 기본값 `medium`)" → "(2026-09 기준 Opus 5.5 기본값 `medium`)" — 모델 기본값은 세대마다 바뀌는 값.

### ✅ 확인 (요약)
- 오프닝 사건(원문 대조): anthropics/claude-code#42796, 2026-04-02 생성(stellaraccident), 제목 "Claude Code is unusable for complex engineering tasks…", 읽지 않고 편집 6.2%→33.7%. Anthropic 반박은 bcherny의 고정 답변(2026-04-06) — `redact-thinking` 베타 헤더는 UI에서 추론을 숨길 뿐 "a UI-only change"로 추론·예산에 영향 없음 → 원고 "UI에만 쓰인다고 반박" 일치. 포스트모템 2026-04-23: 기본 reasoning effort high→medium(3월 4일 변경, 4월 7일 되돌림)·캐시 버그·시스템(verbosity) 프롬프트 변경 세 건 — 원고 일치.
- LY: 이동원·LINE NEXT DevOps 팀, 인용문, Caller–Executor, GitHub Actions·조직 공용 GitHub App 러너·Bedrock Claude, 프롬프트 병합, `pull/${PR번호}/head`, 단기 토큰, 한 달 32개 저장소·344회(자사), 출력 형식 상위 명령 주입 문구. 발행일은 상충 #12대로 미기재.
- Cloudflare 단일 프록시 Worker·인용문·MCP 서버 13개(2026-04), `availableModels`·`deniedModels`(v2.1.283, 2026-09-25, 체인지로그 원문 "even when `availableModels` allows them"), Agent HQ(2026-02 퍼블릭 프리뷰, 허용 에이전트·정책·감사 로그, "reviewed, compared, and challenged, not blindly accepted.").
- 비용: 활성일당 약 $13·월 $150–250·90%가 $30 미만(벤더 문서), Microsoft 연 수백만 달러, 에이전트 팀 plan 모드 약 7배, $15–25 vs 중앙값 $0.98, 사소한 변경 $0.20 vs 전체 $1.68, `claude_args`의 `--max-turns`·타임아웃·concurrency(claude-code-action 문서 원문), `/clear`·CLAUDE.md 200줄·훅 전처리, 서브에이전트 7개(mcv)·415개(vinnymac)·~30k 재전송(a_c), OpenTelemetry·게이트웨이·`total_cost_usd`, Pragmatic Engineer 2026-04 tokenmaxxing·Shopify 사용량 대시보드·서킷브레이커·리더 검토, 토큰 태우기 고백(보도·커뮤니티 표시), `CLAUDE_CODE_OAUTH_TOKEN`.
- 품질 표류: marginlab 일일 벤치마크(HN 2026-01-29), Livenerf(2026-09-22, Opus 5.5 출시일), Codex 컨텍스트 축소·서브에이전트 프롬프트 암호화, `--model claude-opus-5-5`(claude-code-action 문서 예제·공식 모델 ID), 회귀 eval ~100%, `/doctor prompt-audit`(v2.1.283 체인지로그 원문), Gas Town Opus 4.7 붕괴·하네스 자체를 고치려 듦(Willison 2026-08-04 인용), 논쟁 G 양측(joshstrange·hdjrudni·danudey), Yegge 2026-08 "chemically bonded in"·Gas Town 자기 자신만 만듦, AIEWF 2026 스킬 중심·"에이전트는 파일", 절충안은 커뮤니티 리서처 해석으로 명시.
- 수치 약 30건, 날짜 약 12건, 인용 6건, 설정 키·플래그 8건 확인.

### 미해소
- (없음)

## 09장 (라운드 1 보충 — 교차 장 사실 반영)

### ❌ 정정
- "에이전트가 몰래 심은 악성 코드를 94%가 발견하지 못했다 … 56%가 경고를 무시하고" → "참가자의 94%가 … 발견하지 못했다 … 참가자의 56%가" — 초록 원문 "94% of developers fail to detect sabotage" / "56% of participants still accept the malicious code"(arXiv:2606.05647). 비율의 모수가 사보타주 건이 아니라 참가자임을 명시(13~15장 검수와 통일).

### ✅ 확인 (교차 장 전달 사항 대조)
- Opus 5.5 68만 줄 마이그레이션, StrongDM 모델 언급, Yegge 8단계, Lopopolo 팀 규모(3명→7명), Anthropic 자율성 연구 2배 수치는 9~12장에 등장하지 않음. 12장의 `claude-opus-5-5`는 공식 모델 ID로 확인됨.

## 04장 (라운드 1)

대조 근거: `01_reference.md` §2.2·§4.2·§6.1·§2.5, `research/web.md`(W9·W18·W22·W25·W30·W61-2·W62), `research/papers.md`(P-C4·P-C14·P-D10·P-A6), `research/community.md`(휴리스틱 1·2). 원문 대조(curl, 2026-09-28): code.claude.com/docs/en/skills.md, code.claude.com/docs/en/hooks.md.

### ❌ 정정
- (사실 확인 필요 해소) 스킬 위치·머리말: "스킬의 디렉터리 구조와 머리말 필드는 … 공식 문서와 대조해 두자 (사실 확인 필요)" → "Claude Code는 `.claude/skills/<스킬 이름>/SKILL.md` 자리에서 프로젝트 스킬을 읽는다. 머리말의 `description`은 … 꼭 적고, `name`은 생략하면 디렉터리 이름이 그대로 쓰인다(Claude Code 스킬 문서, 2026년 9월 기준)" — 스킬 문서 위치표 "Project | `.claude/skills/<skill-name>/SKILL.md`", Frontmatter reference "`name` No — Defaults to the directory name / `description` Recommended". 원고의 `name`·`description` 두 필드 예시는 그대로 유효.
- (사실 확인 필요 해소) 훅 입력·차단 메시지: "필드 이름(`tool_input.file_path`)과 … 전달되는 방식은 훅 문서와 대조해서 확정하자 (사실 확인 필요)" → "훅은 표준 입력으로 JSON을 받는다. `Write`·`Edit` 같은 파일 도구라면 `tool_input.file_path`에 편집 대상의 절대 경로가 들어 있다. PreToolUse 훅이 종료 코드 2로 끝나면 표준 오류에 쓴 메시지가 차단 사유로 에이전트에게 그대로 전달된다" — 훅 문서 "For the file tools `Write`, `Edit`, and `Read`, `tool_input.file_path` is always absolute" / "A hook that blocks by exiting 2 routes the same way as "deny": Claude sees the stderr message as the denial reason." 절대 경로이므로 가드 스크립트의 `*api/src/main/resources/db/migration/*` 패턴·`[ -e "$target" ]` 검사는 그대로 동작.
- "Boris Cherny는 Claude가 뭔가를 잘못할 때마다 그 내용을 `CLAUDE.md`에 추가한다고" → "… 팀이 그 내용을 …" — 인용 원문 주어가 "we"("Anytime we see Claude do something incorrectly we add it to the CLAUDE.md", 레퍼런스 §2.2 W62, 팀 공유 CLAUDE.md).

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- 스킬 머리말 규칙에 "2026년 9월 기준", 훅 입력 규칙에 "v2.1.283 기준" 명기(위 정정에 포함).

### ✅ 확인 (요약)
- 지침 파일: Claude Code의 AGENTS.md 단독/병행 읽기(W22 원문), OpenAI AGENTS.md 약 100줄 목차·`docs/` 구조화(W9), CLAUDE.md 200줄 이하·특화 지시는 스킬로(W30 원문), "실행 중 컨텍스트로 닿을 수 없는 지식은 없는 것과 같다"(W9 인용), Lopopolo 원칙은 커뮤니티 전언으로 표기(휴리스틱 2), 컬리 계층형 지침·작은 요청 멀티턴(W61-2, 한 회사 사례 단서 유지), `/doctor prompt-audit` v2.1.283 추가(W22 체인지로그 원문).
- 훅: 이벤트(PreToolUse·PostToolUse·Stop), 종료 코드 2 = PreToolUse 도구 호출 차단 / Stop 멈춤 방지(훅 문서 표 "Blocks the tool call" / "Prevents Claude from stopping, continues the conversation"), 훅 유형 command·http·mcp_tool·prompt·agent(W25), 설정 위치 `.claude/settings.json`.
- 계획·실행 분리: HN 2026-02-22 스레드·"30분 계획이 몇 시간 리뷰를 아낀다"(커뮤니티 보고 표기 유지), Every 80/20(W18 원문), HCAST 1시간 이하 70~80% / 4시간 초과 20% 미만(P-A6).
- 연구: Grounded Copilot 가속·탐색 모드(Barke 외, OOPSLA 2023), CUPS 검증 시간 비용(Mozannar 외, CHI 2024), METR RCT 16명·246과제·19%·사전 기대 24%·사후 인식 20%·Cursor Pro+Claude 3.5/3.7 Sonnet(P-C4, 논문 원문 19% 사용), METR 2026-02 후속 — 부호 해석 없이 "두 신뢰구간 모두 0 포함"·30~50% 미제출·하한 추정·설계 변경(상충 #1 처리 준수), Shen & Tamkin 생성 후 이해 패턴(P-C14).
- 수치 9건, 버전·날짜 5건, 명령·경로·키 6건 확인.

### 미해소
- (없음)

## 05장 (라운드 1)

대조 근거: `01_reference.md` §2.2·§4.2·§4.3·§5.1·§5.6·§6.6, `research/web.md`(W10·W16·W19·W22·W24·W29·W30·W31), `research/papers.md`(P-B3·P-B6·P-B7), `research/community.md`(휴리스틱 4·8, 패턴 6·8). 원문 대조(curl, 2026-09-28): anthropics/claude-code `plugins/ralph-wiggum/README.md`·`hooks/stop-hook.sh`, code.claude.com/docs/en/skills.md(`/batch`), developers.openai.com/codex/noninteractive.md.

### ❌ 정정
- "Stop 훅이 종료 코드 2로 끝나면 멈추지 못하고 대화가 이어진다는 그 규칙이 이 루프의 엔진인 셈이다" → "Stop 훅이 멈춤을 막으면 멈추지 못하고 대화가 이어진다는 그 규칙이 이 루프의 엔진인 셈이다. 이 플러그인은 종료 코드 2 대신 "막는다(block)"는 결정을 JSON으로 돌려주는 방식을 쓰지만 효과는 같다." — 플러그인 `stop-hook.sh`는 `"decision": "block"` JSON을 출력하고 `exit 0`으로 끝난다(종료 코드 2 미사용). 레퍼런스 §2.2의 "exit code 2 … Ralph 루프의 기반"은 메커니즘 일반론으로만 유효.

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (추가 없음) — 헤드리스 플래그는 "Claude Code v2.1.283 기준", `codex exec`는 "Codex CLI rust-v0.157.1 기준", 병렬 실행 다섯 가지는 "2026년 9월 기준", 에이전트 팀·에이전트 뷰에 휘발성 경고가 이미 있음.

### ✅ 확인 (요약)
- 외부 피드백: Huang 외(ICLR 2024)·Olausson 외(ICLR 2024 — 비용 대비 이득 작음, 병목은 피드백 질, 강한 모델·사람 피드백 시 이득 증가)·Self-Debugging(P-B7), "당시 모델 기준" 표기 있음. 역압·"싸고 확실하게 검증할 수 있는 만큼만"(Addy Osmani 2026-07-22, 휴리스틱 4). Carlini 출력 위생·16 에이전트·`current_tasks/` 파일 락·"each agent picks a different failing test"·Opus 4.6(W19 원문).
- Ralph: Huntley 2025-07(원문 2025-07-14), 원 명령 표기는 상충 #11대로 요지만 서술, "deterministically bad in an undeterministic world", $50k MVP/$297은 저자 주장 라벨 유지, 공식 플러그인 Stop 훅·`/ralph-loop "…" --completion-promise "…" --max-iterations N` 구문(README 원문 일치, `<promise>…</promise>` 출력 형식 일치).
- 인계: Justin Young 2025-11 — initializer·기능 목록 JSON pass/fail·`init.sh`·git·진행 파일·관찰된 실패 4종(W10). 컴팩션 26일 59회·3계층 메모리(claude-code#34556, 커뮤니티 보고 표기).
- 병렬: 워크트리 문서 문장(W29), Boris 워크트리 3~5개·"더 많은 에이전트를 동시에 감독"(휴리스틱 8), 병렬 방식 다섯 가지·동적 워크플로 "수십~수백"·무진전 2회 예시(W29), `/batch` 5~30개 워크트리 격리 서브에이전트 — 스킬 문서가 `/batch`를 번들 스킬로 명시, 에이전트 팀 워크트리 미격리·실험적 기본 꺼짐·에이전트 뷰 research preview, Grok Build·Muse Code 워크트리 병렬(W44·W45).
- 헤드리스: `claude -p`의 `--output-format json`→`total_cost_usd`·모델별 비용, `--allowedTools "Bash(… *)"` 규칙 형식, `--permission-mode acceptEdits`, `--bare`(훅·스킬·플러그인·MCP·CLAUDE.md 자동 탐색 생략, `-p` 기본값 예고, 미신뢰 폴더에서도 `.claude/settings.json` 훅·`.mcp.json` 연결) — W24 원문. `codex exec` 기본 read-only·`--sandbox workspace-write`·`--json` JSONL — Codex 공식 문서 원문 재확인.
- 에이전트 수: MAST(NeurIPS 2025 D&B, 7개 프레임워크·1,600+ 기록·14개 모드·3범주·"often minimal"), Agentless 게재판 32.00%·$0.70·당시 오픈소스 최고(P-B3, 상충 #17 v2 기준), 에이전트 팀 plan 모드 약 7배 토큰(W30 원문), 서브에이전트 7개 예산 소진·에이전트 415개(패턴 6, 커뮤니티 보고 표기).
- 수치 14건, 버전·날짜 6건, 명령·플래그 12건 확인.

### 미해소
- (없음)

## 06장 (라운드 1)

대조 근거: `01_reference.md` §2.2·§2.3·§3.1·§5.7, `research/web.md`(W1·W2·W11·W19·W20·W26·W27·W61·W62), `research/papers.md`(P-A2·P-A7·P-B9·P-E7~E14), `research/community.md`(휴리스틱 3·5, 패턴 9·10). 원문 대조(curl, 2026-09-28): arXiv 2510.20270 HTML(ImpossibleBench — 계획이 지정한 "본문 HTML 추출" 수치 대조).

### ❌ 정정
- "중단 선택지를 주자 GPT-5의 치팅률이 54%에서 9%로 떨어졌다." 뒤에 "다만 이 효과는 OpenAI 모델에서 두드러졌고, Claude Opus 4.1에서는 훨씬 약했다." 추가 — 원문 §5: "lowering the cheating rate of GPT-5 from 54% to 9% and o3 from 49% to 12%. However, the effect is much less pronounced for Claude Opus 4.1." `gather`의 빌더가 Claude이므로 이 단서 없이 쓰면 독자가 효과를 과대평가한다.
- "포기할 출구를 준 것만으로 치팅이 여섯 분의 일로 줄었다" → "… GPT-5의 치팅이 여섯 분의 일로 줄었다" — 같은 근거. 모델 일반으로 확장된 서술을 원문 범위로 좁힘.

### ⚠️ 약화·삭제
- "테스트를 통과한 실행들의 문제는 …" → "테스트를 통과한 실행 네 건의 문제는 …" — METR 2025-08 "Algorithmic vs. Holistic Evaluation"의 해당 분석은 n=4(레퍼런스 §2.3 P-E11). 표본 크기를 드러내 과일반화를 막음.

### 🕒 신선도
- 루틴 green 상태·Claude Code Review neutral 체크런 문장 뒤에 "(둘 다 2026년 9월 기준 연구 미리보기 기능이다)" 추가 — W26·W27 research preview.

### ✅ 확인 (요약)
- METR 2026-03-10: AI PR 296개·메인테이너 4명(scikit-learn·Sphinx·pytest)·약 24%p·"roughly half"·Claude 3.5 Sonnet~GPT-5·수정 기회 없음. METR 2025-08: 과제 18개·PR 15개 중 머지 가능 0개.
- Wang 외(ICSE 2026) 29.6%·6.2%p, Smith 외(ESEC/FSE 2015) 과적합 구별 불가, Qi 외(ISSTA 2015) Kali "deletes functionality".
- ImpossibleBench(ICLR 2026): GPT-5 54.0%·Claude Opus 4.1 50%(Conflicting-SWEbench), 수법 4종, Claude 계열 테스트 수정 >79% — arXiv 원문 일치. METR 2025-06 "80% → 80%"·지시 효과 미미, RHB(ICML 2026) 상대 87.7% 감소·성공률 유지, MacDiarmid 외(2025-11, Anthropic 자사), Baker 외(OpenAI) — 레퍼런스 일치.
- Böckeler 가이드·센서 2×2·행동 하네스 미성숙(W11), OpenAI 커스텀 린터 계층 강제(W9), LLM 심판 편향·"Bias in the Loop"(2026, P-B9).
- StrongDM 시나리오(코드베이스 밖 end-to-end 사용자 이야기)·Willison 홀드아웃 인용 원문·만족도 정의·DTU(Okta·Jira·Slack·Google Docs, "at volumes and rates far exceeding production limits") — W1·W2 원문 일치. SpecBench 10배당 28%p, EvilGenie 홀드아웃 효과 작음·LLM 심판 효과적 — 상충 #4 처리대로 역할 구분 서술.
- Carlini "task verifier is nearly perfect"(W19), 독립 검증자(addyosmani/factory, 휴리스틱 3), AWS KR 블로그(2026-06, 같은 계열 채점관 결함 누락), "한 번 더 훑는 것" 반론(HN, 커뮤니티).
- PBT: Vikram 외 GPT-4 21%(P-E7). SWE-bench Multimodal(ICLR 2025) 617개·SWE-agent 12% vs 6%(P-A2). Boris Chrome 확장(W62), 토스 해커톤 1등 iOS Simulator 루프(W61, 토스 AI Surf Day). LoopsBench 112과제·Opus 4.7+Claude Code 25.00%·전 구성 회귀(P-A7). Anthropic evals 회귀 ~100%·pass@k vs pass^k(W20). 루틴 green ≠ 성공(W26 원문), Code Review neutral(W27 원문).
- 코드: `actions/checkout`의 `repository`·`ssh-key`·`path` 입력, `workflow_call` 입력, `git diff --name-status base...HEAD`, `codex exec --sandbox workspace-write -o <파일>`(Codex 공식 문서 재확인), Kotest `checkAll`·`Arb.int/list/enum`·`shouldBeLessThanOrEqual` — 실재 API.
- 수치 30건 이상, 인용 5건, 명령·키 8건 확인.

### 미해소
- (없음)

## 07장 (라운드 1)

대조 근거: `01_reference.md` §2.3(검증을 앞당기는 기법)·§4.6·§5.2·§6.2·§9.1 논쟁 C, `research/papers.md`(P-A3·P-C13·P-E1·P-E2·P-E3), `research/web.md`(W13·W14·W15), `research/community.md`(논쟁 C, 휴리스틱 1). 원문 대조(curl, 2026-09-28): arXiv 2509.16941v2 HTML(SWE-Bench Pro).

### ❌ 정정
- (사실 확인 필요 해소) SWE-Bench Pro 하락 원인: "제약이 없으면 에이전트는 더 다양한 해법을 내놓는데, … 멀쩡한 해법도 오답 처리된다는 것이다 (사실 확인 필요)" → 주석 삭제, "특히 기능 추가 과제에서" 한정어 추가 — 원문 §6.2 "Ablation: Removing Human Augmentations": "agents are less constrained and can submit more diverse solutions (particularly for feature additions). Since unit tests expect a narrow set of solutions, verifiers are prone to false negatives, resulting in lower pass rates." Table 3 캡션 "Without these augmentations, unit test verifiers are susceptible to false negatives." 저술가가 든 v2 §6.2 위치도 맞다. (레퍼런스에는 이 설명이 없었음 — 원문으로 확정.)

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (추가 없음) — Spec Kit에 "v1.0.12, 2026-09-25 기준", Böckeler 비판에 "2025년 10월 시점의 도구" 단서, 연구 수치에 "당시 모델 기준"이 이미 있음.

### ✅ 확인 (요약)
- SWE-Bench Pro: Scale AI 연구진, 사람이 보강한 요구사항·인터페이스, GPT-5(high) 25.9% → 8.40%(Table 3 원문, "3분의 1"은 32%로 부합), 2025년 논문.
- TiCoder(IEEE TSE 2024) 4개 LLM·2개 데이터셋·5회 이내 +45.97%p·사용자 연구의 평가 정확도·인지 부하(P-E1), ClarifyGPT(FSE 2024) MBPP-sanitized 70.96% → 80.80%(P-E2), Vilas Boas 외(2026) 1인+에이전트 4개·절반 기간·명세 품질과 조직 지식이 제약, n=1·저자 소속 단서(P-C13).
- SDD 세 수준(Böckeler 2025-10, Piskala 2026), spec-as-source의 MDD 경직성 + LLM 비결정성 경고(W13·P-E3), Spec Kit 4단계·constitution(W14), Kiro `requirements.md`(`bugfix.md`) → `design.md` → `tasks.md`·웨이브 순차/웨이브 내 동시(W15), genai-jerry OpenSpec, Spec Kit Agents(2026-04) PM·개발자 역할·저장소 5·기능 32·실행 128·+0.15(만점의 3.0%)·"context blind"(P-E3).
- 폭포수 논쟁: HN「Spec-Driven Development: The Waterfall Strikes Back」(2025-11), Böckeler "I'd rather review code than all these markdown files", Lars Faye, 반대편 경험담(커뮤니티 보고 표기), 명세 1만 줄당 ~1천 줄·계획 100~300줄(휴리스틱 1, 커뮤니티 보고 표기).
- 수치 12건, 인용 2건, 도구 흐름 3건 확인.

### 편집자 참고 (사실 판정 아님)
- constitution 예시와 명세의 "결제·환불 로직을 건드리지 않는다"는 `gather` 명세(모임·예약·리마인더)에 결제가 없다는 오케스트레이터 메모와 어긋난다. 사실 오류는 아니므로 손대지 않았다 — 통권 정합 시 editor 판단.

### 미해소
- (없음)

## 08장 (라운드 1)

대조 근거: `01_reference.md` §4.2~4.4·§5.3·§5.5·§6.3·§6.4·§8.2, `research/web.md`(W23·W28·W31·W32·W33·W37·W39·W40·W46·W47·W48), `research/community.md`(휴리스틱 3·9·14). 원문 대조(curl, 2026-09-28): github/gh-aw README·docs(how-they-work, workflow-structure, permissions, triggers, safe-outputs, engines), developers.cloudflare.com/workers/previews/(index·examples·compare-workflows)·configuration/previews/·framework-guides/web-apps/nextjs/, code.claude.com/docs/en/github-actions.md, anthropics/claude-code-action `action.yml`, openai/codex-action README·`action.yml`, developers.openai.com/codex/noninteractive.md.

### ❌ 정정
- (사실 확인 필요 해소) gh-aw 파일 위치: "파일은 `.github/workflows/factory-plan.md`에 두었다 (사실 확인 필요)" → "gh-aw의 원본은 `.github/workflows/` 아래 마크다운 파일로 두고, 컴파일하면 같은 자리에 `.lock.yml`이 생긴다. `gather`는 `.github/workflows/factory-plan.md`에 두고 원본과 `factory-plan.lock.yml`을 함께 커밋한다." — workflow-structure 문서 "Agentic workflows live in `.github/workflows` as Markdown files (`*.md`) and compile to … (`*.lock.yml`)", "commit both the source `.md` files and generated `.lock.yml` files". 프런트매터 키 `permissions: read-all`(permissions 문서 "`read-all`: Read access to all scopes")·`safe-outputs: add-comment:`(safe-outputs 문서)는 그대로 유효.
- gh-aw 라벨 조건: 프런트매터 예시에 `names: ["factory:ready"]` 추가, "두 가지는 프런트매터에 걸자 … 구체 문법은 gh-aw 문서를 따르자" → "라벨 이름이 `factory:ready`일 때만 도는 조건은 프런트매터의 `names:`로 걸었다. 엔진 선택도 프런트매터에서 한다(`engine:` — 기본은 Copilot CLI …)" — triggers 문서 "Filter issue and pull request triggers by label names using the `names:` field". 원 예시대로 복사하면 어떤 라벨이 붙어도 계획 에이전트가 돈다.
- `factory-build.yml` 권한에 `id-token: write` 추가 + 설명 한 문장 — Claude Code GitHub Actions 문서 "`id-token: write`: required for the Claude Code GitHub Action's default GitHub App authentication"(`github_token` 미지정 시 Claude GitHub 앱으로 인증). 원 예시대로 복사하면 액션이 인증 단계에서 실패한다. 같은 문서의 "remove [github_token] so it authenticates as the Claude GitHub App"은 본문의 "GitHub 앱 권한으로 푸시" 서술을 뒷받침.
- Cloudflare 프리뷰 기능명: "`web`을 Cloudflare Workers의 Version URL로 올리고" → "Cloudflare Workers의 Preview로 올리고" + Preview/Version URL 구분 두 문장, 그림 1 노드 "Workers Version URL" → "Workers Preview", "Version URL은 켜 두면 누구나 접근할 수 있다" → "Preview URL은 기본으로 누구나 접근할 수 있다" — Previews 문서: "Running `npx wrangler preview` creates or updates a Preview", "Worker Previews requires Wrangler 4.135.0 or later", "Preview URLs are public by default. Use Cloudflare Access to require sign-in". Compare workflows 문서: "Version URLs use production resources … Do not use Version URLs for branch or pull request testing. Use Previews instead." 레퍼런스 W47이 두 기능을 한 항목으로 합쳐 적은 데서 온 혼동.
- (사실 확인 필요 해소) Wrangler 인증: 프리뷰 잡 `env`에 `CLOUDFLARE_ACCOUNT_ID` 추가, "Wrangler 인증 변수 이름은 … 대조해서 채우자 (사실 확인 필요)" → "Wrangler 인증은 Cloudflare 예시대로 `CLOUDFLARE_API_TOKEN`과 `CLOUDFLARE_ACCOUNT_ID` 두 시크릿으로 한다" — examples 문서의 GitHub Actions 예시가 두 변수를 함께 설정. `wrangler preview --name … --json`, `jq -er '.preview.urls[0]'`, `wrangler preview delete`(예시는 `--name "pr-N" --skip-confirmation`) 모두 원문 일치.
- Codex 키 인라인 근거: "Codex 문서가 저장소의 코드를 체크아웃해 실행하는 워크플로에서 권하는 방식이다" → "Codex 문서는 … 키를 잡 수준 환경 변수로 두지 말라고 하고, GitHub Actions라면 키 노출을 줄이는 `openai/codex-action`을 쓰라고 권한다. CLI를 직접 부를 때는 이렇게 키를 필요한 호출에만 붙이는 것이 문서의 방식이다." — 원문 "For GitHub Actions, use the Codex GitHub Action instead of installing and authenticating the CLI yourself" / "Do not set `OPENAI_API_KEY` or `CODEX_API_KEY` as a job-level environment variable …" / "For other automation environments, set `CODEX_API_KEY` only for the Codex invocation". 인라인 호출은 Actions에서의 1순위 권고가 아님.
- 코드·산문 불일치: "CI와 나란히 프리뷰 잡이 돈다" → "CI를 통과하면 리뷰 잡과 나란히 프리뷰 잡이 돈다" — 같은 절의 YAML이 `needs: ci`, 그림 1도 CI → 프리뷰.

### ⚠️ 약화·삭제
- "Durable Object를 쓰는 Worker에는 Version URL이 생기지 않는다는 제약도 기억해 두자" 삭제 — Version URL에만 해당하는 제약이고, 이 파이프라인이 쓰는 Preview는 "automatically provisions a new Durable Object namespace … for each Preview"(Previews 문서)라 독자를 오도한다.
- (사실 확인 필요 해소) Next.js 빌드: "Next.js를 Workers에 올리는 빌드 설정 … 대조해서 채우자" → "빌드 방식은 2026년 9월 기준 Cloudflare 문서가 vinext를 권장하고 기존 OpenNext 어댑터 경로도 함께 안내하는 등 빠르게 바뀌는 중이니, 빌드 단계는 그 문서를 보고 채우자" — Next.js 프레임워크 가이드 "vinext is the recommended path … OpenNext adapter … remain documented". 계획 지침대로 구체 설정은 쓰지 않고 파이프라인 수준 유지(YAML 주석의 "어댑터 설정" → "빌드 설정").

### 🕒 신선도
- `wrangler preview`에 "Wrangler 4.135.0 이상, 2026년 9월 기준", Next.js 빌드 경로에 "2026년 9월 기준" 명기.

### ✅ 확인 (요약)
- 참조 팩토리: Salman Ali Banani 2026-07 Two-Agent PR Workflow — 흐름·수정 1회·자동 승인 없음·`reviewed_by_codex`·자기 채점/머지 권한 분리·Claude 머지(W46 원문), addyosmani/factory — 이슈 큐·루틴 5개·독립 검증자·`STOP_IF`·`.agents/skills/` 어댑터(휴리스틱 3·14, 커뮤니티 공유 저장소 표기), genai-jerry — `factory:*` 라벨·OpenSpec·9개 역할·사람 게이트 3개·스테이징 → 사람 main 승격·PreToolUse 브랜치 보호(휴리스틱 9), Will Larson·Igor Ostrovsky(커뮤니티 보고 표기).
- claude-code-action@v1: interactive(`@claude`)/automation(`prompt`) 자동 감지, `claude_args`의 `--max-turns`·`--model`, `anthropic_api_key`·`prompt`·`claude_args`·`allowed_bots`·`github_token` 입력 실재(`action.yml`), 봇 행위자 거부, 기본 `GITHUB_TOKEN` 커밋은 워크플로 미트리거, `/install-github-app`, 비용 가드 `--max-turns`·타임아웃·concurrency — 공식 문서 원문 일치. 모델 ID `claude-opus-5-5`(§4.1, 교차 장 확인).
- codex-action: `safety-strategy` 기본 `drop-sudo`(실행 전 sudo 회수)·`unprivileged-user`·`read-only`·`unsafe`, 보안 프록시, `sandbox`는 레거시·`permission-profile` 권장 — README·`action.yml` 원문 일치. `codex exec` 기본 read-only·`-o`·`CODEX_API_KEY` 인라인·`npm test 2>&1 | codex exec "summarize failing tests and propose fixes"` — Codex 공식 문서 일치. `@codex review` P0·P1·가장 가까운 AGENTS.md의 `## Code Review Rules`·`@codex fix the P1 issue`(W33).
- Copilot cloud agent 59분 하드 리밋·저장소/브랜치/PR 하나(W39), gh-aw v0.89.21(2026-09-23)·0.x·엔진 기본 Copilot CLI(engines 문서 "Copilot CLI is the default"), Agent HQ 2026-02 공개 미리보기·Mario Rodriguez 인용(W40), Amplify 비공개 저장소 PR별 임시 백엔드·공개 저장소 IAM 롤 앱 차단·앱당 50 브랜치(W48), Auto-fix 동작·연쇄 트리거(Atlantis·Terraform Cloud·`issue_comment`, W28 원문).
- GitHub Actions 구문: `concurrency.group`, `if: github.event.label.name == …`, `timeout-minutes`, `gh issue edit --remove-label/--add-label`, `gh pr comment --body`, `$GITHUB_OUTPUT`, AWS OIDC(배포 잡 `id-token: write` 한 구절 명기 — 조정자 요청 항목).
- 수치 8건, 버전·날짜 6건, 액션 입력·플래그·키 25건 확인.

### 교차 장 전달
- Cloudflare 프리뷰는 `wrangler preview` = Workers **Preview**(Version URL 아님). 계획·레퍼런스 W47과 9장·부록 A·B에 "Version URL" 표기가 있으니 해당 장 담당·editor가 통일할 것.
- `gather` 시크릿 목록에 `CLOUDFLARE_ACCOUNT_ID`가 추가됨(9장 권한 지도 대조). 빌드 잡 권한에 `id-token: write` 추가됨.

### 미해소
- (없음)

## 수락 게이트 1차 수정 (라운드 2 — 05_acceptance.md (c) 사실·코드 항목)

대상: `04_manuscript.md` 3·6·7·8·9·13장, 부록 A.4·B-11. 같은 수정을 `chapters/03·06·07·08·09·13_final.md`, `appendix_a_final.md`, `appendix_b_final.md`에 그대로 반영. 원문 대조(2026-09-28): `gh api`로 받은 anthropics/claude-code-action main의 `action.yml`·`src/modes/agent/index.ts`·`src/modes/tag/index.ts`·`src/github/validation/actor.ts`·`permissions.ts`·`src/github/token.ts`·`src/github/constants.ts`·`src/github/operations/git-config.ts`·`src/mcp/install-mcp-server.ts`·`base-action/src/parse-sdk-options.ts`·`docs/faq.md`·`docs/security.md`·`docs/configuration.md`, code.claude.com/docs/en/github-actions.md·routines.md·permissions.md, developers.cloudflare.com/workers/previews/(index·examples), `npx wrangler@4.142.0 preview delete --help`, actions/checkout README, docs.github.com events-that-trigger-workflows, cli/cli#4631. 수정한 YAML 4개는 YAML 파서로 구문 확인.

### ❌ 정정
- **[1] 13장 cron 다이제스트 YAML 권한 누락** → `jobs.digest`에 `permissions: { contents: read, issues: read, id-token: write }` + 주석 "id-token: write가 없으면 Claude GitHub 앱 인증에서 실패한다(8장)". 기존 주석은 "결과는 기본으로 워크플로 실행 로그에 남는다. 이슈 코멘트 등으로 남기려면 …"으로 보강 — 근거: Claude Code 문서 "Run on a schedule" 공식 예시의 권한 블록이 정확히 `contents: read`·`issues: read`·`id-token: write`; "`id-token: write`: required for the Claude Code GitHub Action's default GitHub App authentication"; "By default, results appear in the workflow run log rather than a comment." 액션 `token.ts`는 OIDC 토큰을 못 받으면 "Did you remember to add `id-token: write`…" 오류로 멈춤. GitHub 읽기(MCP `list_commits`·`list_issues`)는 워크플로 토큰이 아니라 교환받은 Claude 앱 토큰으로 한다(`install-mcp-server.ts`) — 그래서 쓰기 권한은 여기에 더하지 않음(잡이 쓰기를 하지 않는다).
- **[2] 8장 수정 잡의 봇 행위자 거부** → 수정 잡 설명에 "`factory-pr.yml`을 깨운 행위자는 앱의 봇 계정 `claude[bot]`이고, 그대로 두면 수정 잡의 액션이 거부한다. 수정 잡의 `allowed_bots`에는 우리 Claude 앱 봇 하나만 적는다" 추가, `factory-pr.yml`의 fix 잡 발췌 YAML 신설(`allowed_bots: "claude[bot]"`, `id-token: write`, `ref: ${{ github.head_ref }}` checkout, review 아티팩트 다운로드, 좁은 `--allowedTools`). 근거: automation 모드도 `prepareAgentMode`에서 `checkHumanActor`를 호출(`src/modes/agent/index.ts`); Claude Code 문서 "on every event, the Claude Code GitHub Action rejects a bot actor unless you list it in `allowed_bots`"; `actor.ts`가 목록 항목과 행위자에서 `[bot]` 접미사를 떼고 비교(따라서 `claude[bot]`·`claude` 모두 일치); 기본 앱 봇 로그인 `CLAUDE_BOT_LOGIN = "claude[bot]"`(`constants.ts`), FAQ "Comments appear as claude[bot] when the action uses its built-in authentication"; `[bot]`으로 끝나는 행위자는 쓰기 권한 검사를 통과(`permissions.ts`); 보안 문서 "Prefer an explicit list over `'*'`". 구현 잡의 푸시·PR은 앱 토큰으로 이뤄지므로(`git-config.ts`가 origin URL을 앱 토큰으로 교체, `run.ts`가 `GH_TOKEN`에 앱 토큰 설정) PR 이벤트 행위자는 `claude[bot]`이 됨.
- **[2-부수] 8장 수정 잡의 라벨 순서(재실행 경쟁)** → "…수정을 한 번 커밋하고 … 뒤 `factory:reviewed` 라벨을 붙인다" → "`factory:reviewed` 라벨을 먼저 붙이고 … 한 번 커밋한 뒤 …" + "라벨을 푸시보다 먼저 붙이는 것은 다시 도는 실행이 이 라벨을 보게 하려는 것이다". 푸시 뒤에 라벨을 붙이면 수정 커밋이 만든 `synchronize` 이벤트 페이로드에 라벨이 없을 수 있어 리뷰·수정이 한 번 더 돈다 — "수정은 구조적으로 한 번뿐"이 성립하도록 코드 순서를 맞춤. 라벨은 워크플로 단계가 `GITHUB_TOKEN`으로 붙이며, `gh pr edit --add-label`은 issues·pull-requests 쓰기가 모두 필요해 잡 권한에 둘 다 둠(cli/cli#4631).
- **[3] `git diff origin/main...HEAD`와 기본 checkout** → 8장: "이 잡과 CI 잡처럼 `git diff`로 기준과 비교하는 잡은 checkout에 `fetch-depth: 0`을 준다. `actions/checkout`은 기본으로 트리거한 커밋 하나만 받아서, 그대로는 러너에 `origin/main`도 7장의 승인 태그도 없다." 추가, `factory-build.yml` checkout에 `with: { fetch-depth: 0 }`(본문의 "구현 브랜치는 승인 태그에서 딴다"가 성립하려면 태그가 필요). 6장: `check-protected-paths.sh`·`verify.sh`의 기본 기준 줄에 fetch-depth 주석. 9장: 교차 리뷰 YAML 위에 fetch-depth 주석. 7장: "기본값으로는 이 태그가 러너에 없고, `pull_request` 이벤트에서 받는 머지 커밋에는 태그 이후 main에 들어온 변경까지 섞인다. 그래서 이 CI 잡의 checkout에는 `fetch-depth: 0`(모든 브랜치와 태그)과 `ref: ${{ github.event.pull_request.head.sha }}`를 준다." — 근거: actions/checkout README "Only a single commit is fetched by default … Set `fetch-depth: 0` to fetch all history for all branches and tags"; GitHub 문서 `pull_request`의 `GITHUB_SHA` = "Last merge commit on the `GITHUB_REF` branch"(`refs/pull/N/merge`). 태그 기준 diff(`tag...머지 커밋`)는 merge-base가 태그라서 그 뒤 main에 머지된 다른 인수 테스트·워크플로 변경까지 잡혀 오탐이 난다 — 수락 게이트가 짚은 "태그를 받으려면 fetch 설정 필요"에 더해 확인한 결함.
- **[4] `wrangler preview delete` 인자** → 8장 "PR이 닫히면 정리 잡이 `npx wrangler preview delete --name "pr-<번호>" --skip-confirmation`으로 프리뷰를 지운다. 이름을 빼면 현재 git 브랜치 이름의 프리뷰를 지우려 하니 …, 사람이 없는 실행이니 확인 프롬프트는 건너뛴다." 부록 A.4 "그 밖에 본문에 나온 명령"과 B-11 흐름 칸도 같은 명령으로 교체 — 근거: Cloudflare Previews 예시 "Delete closed pull request Previews" 원문 `npx wrangler preview delete --name "pr-${{ github.event.pull_request.number }}" --skip-confirmation`; Wrangler 4.142.0 도움말 `--name  Name of the Preview to delete (defaults to current git branch)`, `-y, --skip-confirmation  Skip the confirmation prompt`.
- **[5] 기본 도구로 draft PR을 열 수 있는가 — 열 수 없음** → `factory-build.yml`의 `claude_args`에 `--permission-mode acceptEdits`와 `--allowedTools "Bash(./scripts/dev/check.sh *),Bash(git switch *),Bash(git add *),Bash(git commit *),Bash(git push *),Bash(gh pr create --draft *),Bash(gh issue comment *)"` 추가, 본문에 "automation 모드에서 Claude는 허락받은 도구가 없으면 셸도 GitHub API도 쓰지 못하고 … `gh pr create`는 `--draft`가 붙은 형태만 허락" 설명 추가 — 근거: Claude Code 문서 "For a plain-text prompt, Claude has no shell or GitHub API access until you grant the tools the prompt needs, with `--allowedTools` in `claude_args`"; FAQ "Claude doesn't create PRs by default", "The Bash tool is disabled by default"; agent 모드는 기본 허용 도구·권한 모드를 넣지 않는다(`src/modes/agent/index.ts`). tag 모드 소스 주석 "Headless SDK has no prompt handler, so anything that falls through to 'ask' is denied"와 tag 모드가 따로 `--permission-mode acceptEdits`를 거는 것으로 보아, automation 모드에서는 파일 편집도 허락이 필요함. 프롬프트가 요구하는 "이유를 이슈 코멘트로 남긴다"도 도구가 있어야 하므로 `gh issue comment`를 함께 엶. 규칙 형식(`Bash(… *)`, `*` 앞까지 문자 그대로 일치)은 Claude Code 권한 문서와 5·9장 표기와 같음.
- **[7] 13장 루틴 브랜치 단정** → "루틴은 `claude/` 접두 브랜치에만 푸시하고, 보호 브랜치로의 푸시는 거부된다" → "루틴은 따로 지시하지 않으면 `claude/` 접두 브랜치에만 푸시하고, 프롬프트로 다른 브랜치를 가리켜도 보호 브랜치로의 푸시는 거부된다". 9장도 같은 한정으로 맞춤: "기본 설정에서는 `claude/` 접두 브랜치에만 푸시한다" → "따로 지시하지 않으면 `claude/` 접두 브랜치에만 푸시하고, 보호 브랜치로는 푸시하지 못한다" — 근거: 루틴 문서 원문 "Claude pushes its work to branches prefixed with `claude/`, which are always accepted. When your prompt directs Claude to push to another branch, Claude Code checks the push first and rejects it if … The branch is protected on GitHub / Someone else has an open pull request from that branch / The branch carries commits authored by someone other than you." 제한을 푸는 것은 설정이 아니라 프롬프트의 지시라서, 9장의 "기본 설정에서는"보다 "따로 지시하지 않으면"이 정확함. 두 장의 한정 수준을 같게 둠.

### ⚠️ 약화·삭제
- **[6] 3장 Grok 4.7 "최고 모델"** → "코딩·지식 노동용 최고 모델(xAI 발표)" → "코딩·에이전트 작업·지식노동용 프런티어 모델(xAI 발표)" — 부록 A 사실 검수의 정정 표기와 일치. 릴리스 노트 원문 "SpaceXAI's frontier model designed for coding, agentic tasks, and knowledge work"(부록 A 로그). "최고"의 근거 없음.

### 🕒 신선도
- (추가 없음) — Wrangler 4.135.0 이상·2026년 9월 기준 표기가 8장과 B-11에 이미 있음.

### ✅ 확인 (요약)
- 8장 기존 서술 "`github_token` 입력을 넘기지 않으면 … Claude GitHub 앱으로 인증하는데, 이 인증에 `id-token: write` 권한이 필요" — `token.ts`와 문서 원문 일치.
- 9장 `allowed_bots` 경고("저장소 권한을 확인하지 않는다") — 보안 문서 "Allowed bots are not checked for repository permissions" 원문 일치. 8장의 새 예외(자기 앱 봇 하나를 이름으로 허용)와 9장 경고의 관계 설명은 chapter-writer 몫으로 남김.
- 수정 잡 푸시·코멘트가 Claude 앱 토큰으로 이뤄지는 경로, `pull_request` 이벤트의 `github.head_ref` 사용 — 액션 소스·GitHub 문서 일치.
- 스니펫 4개(`factory-build.yml`, fix 잡, 9장 교차 리뷰, 13장 digest) YAML 구문 확인.

### 편집자·저술가 참고 (사실 판정 아님)
- 9장 권한 지도의 "수정 잡" 행은 이번 YAML과 맞춰 적을 것: 입력은 `review.md`(아티팩트), 모델 쪽 권한은 Claude 앱 토큰으로 자기 PR 브랜치 커밋·푸시와 PR 코멘트(허용 도구로 `check.sh`·git 커밋/푸시·`gh pr comment`만), 라벨은 모델이 아니라 워크플로 단계가 `GITHUB_TOKEN`으로 붙임, 잡 권한 `contents: read`·`issues: write`·`pull-requests: write`·`id-token: write`.
- 9장 "구현 에이전트" 행도 허용 도구가 좁혀졌음(`gh pr create --draft`, `gh issue comment`, git·`check.sh`)을 반영할 수 있음.

### 미해소
- (없음)
