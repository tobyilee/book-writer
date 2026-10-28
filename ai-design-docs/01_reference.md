# AI 코딩 에이전트 시대의 프로젝트 설계·문서화 레퍼런스

> 슬러그 `ai-design-docs` · 장르 `tech-book` · 합성일 2026-10-28 · 합성 research-lead
> 입력: `research/web.md`(웹), `research/papers.md`(논문), `research/community.md`(커뮤니티), 척추 원전 `research/primary/ai-project-design-guidelines-ko.md`(이하 "원전 가이드", §01~§14)
> 대상 독자: Claude Code·Codex·Hermes Agent·OpenAI dots를 이미 매일 쓰는 한국 개발자. 도구 설치·기초 프롬프트 같은 입문 내용은 줄였다. 컨텍스트 파일의 실제 로드 규칙, 검증 증거, 실증 연구의 한계는 자세히 남겼다.

## 표기 규칙 (fact-checker 대조 기준)

- **출처 유형 태그:** [원전] 원전 가이드 · [웹] · [논문] · [커뮤니티]
- **참조 ID:** `W-B1` = web.md 자료 B1, `P-17` = papers.md 논문 17, `C-패턴1`·`C-휴리스틱3`·`C-논쟁A`·`C-도구` = community.md의 해당 항목. 본문에 수치·인용을 옮길 때는 이 ID로 research 원본을 열어 한 번 더 대조한다. research/*.md는 지우지 않는다.
- **검증 플래그** (리서처 원본 플래그를 그대로 옮겼다):
  - `[원문 직접 확인]` — `gh api`·npm 조회 등으로 1차 원문을 직접 읽음
  - `[요약 경유]` — WebFetch(요약 모델 경유)로 가져온 영어 인용. web.md의 `>` 인용 대부분이 여기에 해당한다(web.md "인용 표기 규칙"). 본문에 그대로 넣을 문장은 원 URL에서 다시 대조한다.
  - `[원문 재대조 필요]` — 403 등으로 본문을 못 열고 검색 스니펫으로만 확인
  - `[2차]` — 언론·블로그·출판사 페이지를 거쳐 확인
  - `[미확인]` — 출처끼리 엇갈리거나 1차 확인이 안 됨
  - `[프리프린트]` / `[프리프린트·단독 저자]` — 동료 심사 전. 본문에서는 "~라는 보고가 있다" 수준으로만 쓴다
  - `[커뮤니티 의견, 검증 필요]` — community.md의 모든 항목에 기본으로 붙는다. 댓글 속 수치·연구 인용·소속 주장("Claude Code에서 일한다" 등)은 원문과 대조하지 않았다
- **리서처 해석 표시:** 원전 절과 외부 자료를 짝지은 것 중 원 저자가 한 말이 아니라 리서처나 책의 추론인 것은 `(책의 해석)`으로 표시했다.

---

## 0. 이 책의 기준 시점 (2026-10-28 조회)

| 도구 | 버전·날짜 | 확인 방법 | 출처 |
|---|---|---|---|
| Claude Code (`@anthropic-ai/claude-code`) | **2.1.312** (npm, 2026-10-27 갱신) | [원문 직접 확인] | W-A3 |
| OpenAI Codex CLI (`@openai/codex`) | **0.165.0** (npm, 2026-10-28 갱신), GitHub `rust-v0.165.0` 2026-10-27 | [원문 직접 확인] | W-A3 |
| Hermes Agent (Nous Research) | **v0.22.5** (2026-10-23), 첫 릴리스 v0.2.0 (2026-03-12), 저장소 생성 2025-07-22, MIT | [원문 직접 확인] | W-A1 |
| OpenAI dots | DevDay 2026 (**2026-09-29**) 발표, 모델 GPT-6 Astra (TechCrunch) | 1차 문서 403 → [2차] 교차 확인 | W-A2 |
| GitHub Spec Kit | **v1.2.4** (2026-10-27), v1.0.0 2026-08-21 | [원문 직접 확인] | W-A3, W-C2 |
| OpenSpec (Fission-AI) | **v1.15.0** (2026-10-24) | [원문 직접 확인] | W-A3, W-C6 |
| BMAD Method | 안정판 **v6.12.4** (2026-10-14), v7 프리뷰 알파 | [원문 직접 확인] | W-A3, W-C7 |
| Agent OS (Builder Methods) | **v3.0.0** (2026-01-20) | [원문 직접 확인] | W-A3, W-C8 |
| Kiro (AWS) | GA **2025-11-17** (공식 블로그), 프리뷰 2025-07-14 [2차] | 공식 문서 | W-C3 |
| OpenAPI Specification | **3.2.0 = 2025-09-19** | [2차] 교차 확인, 공식 릴리스 노트 미열람 | W-F10 |
| IETF Idempotency-Key 초안 | 최신 **-08 (2026-10-22)**, Active Internet-Draft, RFC 미발행. 본문 확인은 -07(2025-10-15) | datatracker 조회 | W-F7 |

> 주의: 이 분야는 몇 주 단위로 바뀐다(W 범위 규칙). 본문에서 버전·기능을 말할 때는 항상 "{버전}/{2026-10} 기준"을 붙인다. BMAD README의 "The v7 release ETA is October 16, 2026, and it might be sooner."는 조회 시점(10-28)에 이미 지난 날짜다. v7이 실제로 나왔는지는 확인하지 않았다 → [미확인].

---

## 1. 개념과 정의

### 1.1 원전 가이드의 골격 [원전]

- **문서의 세 가지 일 (§01):** A 합의의 기준선 · B 검증의 대상 · C 변경의 제어 장치. 문서의 가치는 "설명의 양이 아니라, 결정의 명확성과 검증 가능성으로" 판단한다.
- **핵심 원칙 (§01):** "하나의 결정에는 하나의 권위 있는 원본을 둡니다. 다른 문서는 그 내용을 복사하지 않고 **식별자와 링크**로 참조합니다."
- **흐름 (§01):** 문제 → 규칙 → 증거 → 수직 기능 → 학습. "이 흐름은 한 번만 통과하는 폭포수 절차가 아닙니다." "'문서 완성률 100%' 대신 '다음 구현을 시작해도 되는가'를 판단합니다."
- **책임 분리 (§02):** spec / domain / ux / adr / plan / guides / brainstorming + 선택지 product-brief.md / architecture / validation. "폴더를 만드는 것 자체가 설계는 아닙니다."
- **여섯 번의 작은 합의 (§03):** 문제·성공 조건 → 핵심 시나리오·경계 → 규칙·계약 → 가장 위험한 가정 검증 → 작은 구현 범위 승인 → 수직 기능으로 재확인. 단계마다 입력·활동·산출물·검토자·종료 조건이 있다.
- **추적 ID 사슬 (§05·§06):** `REQ-CAN-01` → `POL-CAN-01` → `API-CAN-01` → `AC-CAN-01`. §06은 8단계(REQUIREMENT → DOMAIN → CONTRACT → EXPERIENCE → ACCEPTANCE → PLAN → TEST → EVIDENCE)로 늘린다.
- **Design Ready (§07):** BLOCK / CONDITIONAL / LATER. 게이트 5가지는 명확성·정합성·실현 가능성·추적성·책임성.
- **AI 역할 (§10):** PLANNER · DESIGNER · REVIEWER · IMPLEMENTER. 역할마다 "금지"가 붙는다. 사람이 최종 소유하는 결정은 "제품 가치와 범위, 가격·환불 등 업무 정책, 법·보안·개인정보 의무, 위험 수용, 출시 승인"이다.
- **가이드 자기 범위 (머리말):** 구조·정책·수치·일정은 "권장안과 가상 예시"이고, 특정 프로젝트의 확정 규칙이 아니다. → 본문이 원전의 예시 수치(p95 ≤ 500ms, 10분 경보 등)를 권장 기본값처럼 쓰면 안 된다. 원전은 그 숫자를 "**형식을 보여 주기 위한 예시**이며 권장 기본값이 아닙니다"라고 못 박는다(§04).

### 1.2 외부 용어

| 용어 | 정의 (출처) |
|---|---|
| 비결정적 / 결정적 지시 | 비결정적 = 모델이 읽고 판단하는 지시(프롬프트·CLAUDE.md·스킬), 결정적 = 하네스가 반드시 실행하는 장치(훅·deny 규칙·관리 설정). [웹] W-B1 Claude Code Best practices |
| 컨텍스트 엔지니어링 | "Context engineering is curating what the model sees so that you get a better result." (Böckeler가 Bharani Subramaniam의 정의를 인용) [웹] W-B9 · "the smallest possible set of high-signal tokens" [웹] W-B8 |
| 하네스 엔지니어링 | OpenAI Ryan Lopopolo 글(2026-02-11)이 원류로 인용된다 [웹] W-B7 [원문 재대조 필요]. 해설에 따르면 "Harness includes context engineering, architectural constraints, and garbage collection."(Martin Fowler LinkedIn, InfoQ 인용) [2차]. 국내 정의: "AI가 길을 잃지 않고 안정적으로 일할 수 있도록 외부 통제 환경을 구축하는 것" [웹] W-D2 우아한형제들 |
| AGENTS.md | "Think of AGENTS.md as a README for agents" — Linux Foundation 산하 Agentic AI Foundation이 관리 [웹] W-B3 |
| Agent Skills | `SKILL.md` 폴더. 발견(이름·설명) → 활성화(전체 로드) → 실행의 점진적 공개(progressive disclosure). Anthropic이 처음 만들고 오픈 표준으로 공개 [웹] W-B10 |
| ExecPlan | "a design document that a coding agent can follow to deliver a working feature or system change." Progress / Surprises & Discoveries / Decision Log / Outcomes & Retrospective 섹션이 의무 [웹] W-B6 (archived 페이지, 구버전일 수 있음) |
| SDD 3수준 | spec-first / spec-anchored / spec-as-source [웹] W-C4 Böckeler 2025-10-15. 같은 3단계를 Piskala 2026 프리프린트도 쓴다 [논문] P-SDD [프리프린트·단독 저자] |
| EARS | `WHEN [condition/event] THE SYSTEM SHALL [expected behavior]` — Kiro 요구사항 표기 [웹] W-C3. EARS 원 논문(Mavin et al. 2009)은 이번에 수집하지 않았다 |
| Given-When-Then | "a style of representing tests - or as its advocates would say - specifying a system's behavior", Daniel Terhorst-North·Chris Matts의 BDD에서 나옴 [웹] W-F5 Fowler 2013 |
| ADR | Nygard 2011: Title·Context·Decision·Status·Consequences, 뒤집힌 결정은 superseded로 표시 [웹] W-F1. MADR 4.0.0(2024-09-17)은 front matter `status` 필드 [웹] W-F2 |
| 멱등키 | 클라이언트가 만든 고유 키로 재시도를 안전하게 함 [웹] W-F6 Stripe · IETF 초안 [웹] W-F7 |
| Transactional outbox | 업무 엔터티 갱신과 같은 트랜잭션으로 메시지를 DB에 저장하고 별도 프로세스가 브로커로 보냄. "The Message relay might publish a message more than once." [웹] W-F8 |
| 계약 테스트 | "testing an integration point by checking each application in isolation" [웹] W-F9 Pact |
| 자동화 편향·안주 | 주의 메커니즘으로 통합 설명, 초보·전문가 모두에서 나타남 [논문] P-48 Parasuraman & Manzey 2010 [2차] |
| 자동화의 역설 | 자동화가 발전할수록 남은 사람 역할이 중요해지지만 그 능력은 쇠퇴 [논문] P-47 Bainbridge 1983 [2차] |
| 상관된 오류 | 두 모델이 모두 틀릴 때 같은 오답을 고르는 경향 [논문] P-35 |
| 인지 부채 (cognitive debt) | 개발자가 정신적 노력을 도우미에게 넘기며 쌓이는 부채. Borg 외 abstract의 향후 과제 문장 [논문] P-5, 에세이 EEG 연구 [논문] P-52 Kosmyna [프리프린트]. Thoughtworks Radar Vol.34(2026-04)의 중심 주제였다는 보도 [웹] W-C5 [2차, 미확인] |
| doc rot의 새 얼굴 | "It's the same old problem of doc rot, but now the docs are blindly obeyed." [커뮤니티] C-패턴2 varyherb |

---

## 2. 핵심 관점들 — 원전 가이드 절별 근거 매핑 (§01~§14)

각 절마다 순서: 원전 요지 → 뒷받침 근거(웹·논문·커뮤니티) → 긴장·반론 → 집필 주의.

### §01 문서는 세 가지 일을 해야 합니다

**원전 요지:** 합의·검증·변경 제어. 원본 하나 + ID·링크. 폭포수가 아님. 판단 기준은 "다음 구현을 시작해도 되는가".

**뒷받침**
- [웹] W-B1 Claude Code Best practices: "If something has to happen every time, make it a hook, a deny rule, or a managed setting. `CLAUDE.md` is for guidelines, and Claude is allowed to decide a guideline doesn't apply." [요약 경유] → 문서의 C 역할(변경 제어)을 무엇이 실제로 집행하는지 가르는 기준.
- [웹] W-C1 GitHub(Den Delimarsky, 2025-09-02): "This is a contract for how your code should behave" / "Specs become the shared source of truth." [요약 경유]
- [웹] W-D1 토스(김용성, 2026-02-26): "문서 관리의 패러다임이 '기록'에서 '실행'으로 바뀌는 셈입니다."
- [웹] W-E3 Simon Willison(2025-10-07): "Write good documentation first and the model may be able to build the matching implementation from that input alone." [요약 경유]
- [논문] P-1 METR(2025): 체감과 실측이 갈린다 → "증거로 판단"의 출발점(상세는 3.A).

**긴장·반론**
- [커뮤니티] C-논쟁A beders: "There is only one source of truth and that is the source code." — 원전의 "원본 하나" 원칙과 정면으로 부딪힌다. 원전은 규칙의 원본(domain)과 코드를 구분하고, 테스트는 "규칙을 검증하는 실행 가능한 표현"으로 둔다(§02).
- [웹] W-C4: 원전의 입장은 spec-anchored에 가깝다. 다만 "테스트가 통과한다고 문서와 다른 동작을 자동 승인하지 않습니다"(§02)로 spec-as-source와 선을 긋는다 (책의 해석 — 웹 리서처의 해석).

### §02 폴더보다 중요한 것은 원본의 책임입니다

**원전 요지:** 위치마다 답할 질문과 권위 있는 내용을 나눈다. API 스키마를 OpenAPI로 관리하면 그 스키마가 계약의 원본이다. spec·UX·plan에 서로 다른 취소 규칙이 있으면 "코드보다 먼저 충돌을 해결해야 합니다." "테스트가 통과한다고 문서와 다른 동작을 자동 승인하지 않습니다."

**뒷받침 — 에이전트가 문서를 읽는 실제 규칙**
- [웹] W-B2 Claude Code memory 문서(2026-10 기준):
  - "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead." [요약 경유]
  - "**Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."
  - "**Consistency**: if two instructions contradict each other, Claude may pick one arbitrarily." → 원전 "피해야 할 중복"의 도구 측 근거.
  - `@path` 임포트는 정리에 도움이 되지만 컨텍스트 비용은 줄이지 않는다.
  - Claude Code는 AGENTS.md를 직접 읽는다: AGENTS.md만 있으면 AGENTS.md를 읽고, 둘 다 있으면 "Your `CLAUDE.md` files only", CLAUDE.md가 AGENTS.md를 임포트하면 둘 다 읽는다.
- [웹] W-B4 Codex: 루트에서 현재 디렉터리까지 디렉터리마다 `AGENTS.override.md` → `AGENTS.md` → 대체 파일명 순으로 "at most one file per directory"를 읽어 이어 붙인다. 합계가 `project_doc_max_bytes`(기본 **32 KiB**)에 닿으면 멈춘다. → "AGENTS.md에 설계 문서를 통째로 넣지 말고 원본 경로만 가리켜라"의 기술적 근거 (책의 해석).
- [웹] W-A1 Hermes: "Only **one** project context type is loaded per session (first match wins): `.hermes.md` → `AGENTS.override.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`." 그리고 git 저장소 안에서는 루트부터 작업 디렉터리까지의 AGENTS.md를 "merged chain"으로 싣는다 [원문 직접 확인]. (두 규칙은 모순이 아니다. 먼저 한 종류를 고르고, AGENTS.md면 계층 체인을 합친다는 뜻으로 읽힌다 — 책의 해석, 문서 재확인 권장.)
- [웹] W-B7 OpenAI harness engineering: "A giant instruction file crowds out the task, the code, and the relevant docs" [원문 재대조 필요]. 해설 [2차]: AGENTS.md를 백과사전이 아니라 목차로 두고 깊은 내용은 구조화된 `docs/`로 보낸다. **"~100줄" 수치는 Viblo 한 곳만 명시 → [미확인]**.
- [웹] W-C6 OpenSpec: "One source of truth your whole team and every coding agent can read, across every repo." [원문 직접 확인]
- [웹] W-D2 우아한형제들(이재홍, 2026-04-17): Swagger → 타입·Mock·React Query 훅·테스트 생성. "AI가 직접 전체 코드를 탐색하도록 두는 대신, 스크립트가 먼저 실행되어 코드 생성에 필요한 메타데이터만 JSON 형태로 요약해 AI에게 전달하는 방식입니다." → 원전 "그 스키마를 계약의 원본으로"의 국내 실례.

**뒷받침 — 틀린·낡은 문서의 해악**
- [논문] P-27 Macke & Doyle(MITRE, Findings of NAACL 2024): "providing an LLM with "incorrect" documentation can greatly hinder code understanding, while incomplete or missing documentation does not seem to significantly affect an LLM's ability to understand code." → "문서를 많이"가 아니라 "틀린 문서를 없게". **한계: 2023~2024 세대 모델**.
- [논문] P-21 Xu & Wu(arXiv 2610.30571, 게시 2026-10-22) [프리프린트]: Python 프로젝트 40개, Claude Code·Codex CLI 320회 실행. 지시 파일과 코드가 충돌할 때 **90.1%**가 오래된 지시 파일을 따랐다. Claude Code는 **80회 중 79회** 충돌을 지적하고도 파일을 따랐다. Codex CLI는 80회 중 20회 기존 코드를 파일에 맞게 다시 썼고 그중 17회에서 테스트가 실패했다. "기존 코드를 우선하라"는 한 문장을 넣자 코드를 따르는 비율 **4.2% → 91.4%**, 테스트 통과율 **89.4% → 100%**. 원인 설명: "the instruction file reaches the model as an instruction and the code as tool output, which models are trained to rank lower."
- [논문] P-11 Wang·Pradel·Liu(ICSE 2026): SWE-bench Verified의 "그럴듯한" 패치 중 **7.8%**가 개발자 테스트를 실패하는데도 정답 처리됐다. PatchDiff로 보면 **29.6%**가 정답 패치와 다르게 동작했다. 보고된 해결률이 **6.2%p** 부풀려졌다. → 원전 "테스트 통과 ≠ 자동 승인"의 직접 근거.
- [논문] P-16 Mohsenimofidi 외(MSR 2026): AGENTS.md 466개 프로젝트, "정해진 내용 구조가 아직 없음". 후속 Abubakar 외(ESEM 2026, arXiv 2608.04661): 저장소 **36,710개**를 선별했는데 plan 파일은 **10개 저장소의 85개**만 발견. → 원전의 `plan/` 위치 제안이 현장에서는 드문 관행이라는 대비.

**뒷받침 — 현장 장면**
- [커뮤니티] C-패턴2 varyherb(HN 50227041, 2026-10-26): 수십 명이 기여하는 코드베이스에서 ADR 방식이 "will start to degrade the code you get from a model surprisingly quickly" — "It's the same old problem of doc rot, but now the docs are blindly obeyed."
- [커뮤니티] C-논쟁E: Claude Code가 CLAUDE.md 없을 때 AGENTS.md를 읽는다는 HN 스레드(2026-09-18, 741점)에서 "Finally. Now I can remove all my symlinks" 류 반응. → 원본 하나 원칙을 지시 파일에 적용한 사례.
- [커뮤니티] C-패턴4 GPTers 제이리: PRD에는 "주문건", 코드에는 `overtime_order`. "클로드가 실수한 게 아니라, 제가 기획을 명확하게 안 했어요." (저장값과 표시값의 원본을 정하지 않음)

**집필 주의**
- Claude Code가 AGENTS.md를 지원하기 시작한 버전을 "2.1.277"이라고 쓰지 말 것. 이 번호는 velog 글 제목(gwanghun-choi, 2026-09-21)에만 있고 [미확인]이다. 확실한 것은 "2026-10 공식 문서 기준 지원"까지다. 2025년 블로그의 "Claude Code는 AGENTS.md를 지원하지 않으니 심볼릭 링크하라"는 구버전 정보다(W-B2 주의).
- AGENTS.md 공식 사이트 지원 도구 목록에는 Claude Code가 없다. 그러나 W-B2대로 2026-10 기준 직접 읽는다. 두 사실을 함께 쓴다.

### §03 아이디어를 여섯 번의 작은 합의로 바꿉니다

**원전 요지:** 6단계, 단계마다 입력·활동·산출물·검토자·종료 조건. "위험이 작은 항목은 합치고, 큰 항목은 반복합니다."

**뒷받침**
- [웹] W-C2 Spec Kit v1.2.x: `/speckit-constitution` → `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` → `/speckit-converge`, "Repeat implement and converge until convergence reports `Converged`." "Run these skills in your agent's chat, not your terminal, one at a time, reviewing each result before continuing." [원문 직접 확인]. 웹 리서처의 대응표: constitution ≈ guides/ADR, specify ≈ spec/, plan ≈ architecture/ADR, tasks ≈ plan/ (책의 해석).
- [웹] W-C3 Kiro: Requirements-First(Requirements → Design → Tasks)와 Design-First(Design → Requirements → Tasks). 후자는 "strict non-functional constraints or existing design documents"가 있는 프로젝트용.
- [웹] W-C7 BMAD: "Small changes go straight to build. Complex work gets the depth it needs." [원문 직접 확인] → "위험이 작은 항목은 합치고".
- [웹] W-E1 Harper Reed(2025-02-16): 아이디어 다듬기 → `spec.md` → 계획(`prompt_plan.md`, `todo.md`) → 실행. "The success really depends on how well step 2 went."
- [웹] W-F4 Orosz: Uber의 서비스 RFC는 "List of approvers"로 시작했다(RFC 프로세스는 "used up to around 2019"). → 단계마다 "검토자"를 적는 관행의 선례.
- [커뮤니티] C-패턴7 BonanKou(HN 49298901): "reviewing the final diff feels too low-level and too late. I'd rather review the plan&assumptions." → 검토 지점을 단계 5 이전으로 앞당기는 이유를 현장 언어로.

**긴장:** 커뮤니티의 "작게"는 대부분 태스크를 가로로 자른다. 원전의 수직 기능(정상·실패·권한·관측을 한 슬라이스 안에)은 커뮤니티 담론에서 거의 보이지 않는다 → 책의 차별점 (C-휴리스틱5, 커뮤니티 리서처의 관찰).

### §04 처음 쓰는 문서는 짧은 제품 합의서입니다

**원전 요지:** 사용자·문제·가치 가설·범위·비범위·성공 판단·제약·큰 가정·결정과 미결정. 비기능 요구를 관찰 가능한 문장으로. "AI가 제안한 숫자를 근거 없이 품질 계약으로 확정하지 않습니다."

**뒷받침**
- [웹] W-B1: "I want to add rate limiting to the public API but haven't thought it through yet. Interview me until you could write the spec, then write it to SPEC.md." / "Once `SPEC.md` exists, start a fresh session to build from it, so the build begins with a clean context and a written definition of done." [요약 경유]
- [웹] W-C3 Kiro steering 기본 파일 `product.md`·`tech.md`·`structure.md` → product brief와 대응.
- [웹] W-F3 Malte Ubl(Design Docs at Google, 2020-07-06): non-goals = "things that could reasonably be goals, but are explicitly chosen not to be goals."
- [웹] W-E4 Addy Osmani(2026-01-13): "Kick off your project with a concise high-level spec, then have the AI expand it into a detailed plan."
- [논문] P-15 Agent READMEs(ACM TOSEM): 컨텍스트 파일 2,303개에서 지시 유형 중 테스트 절차 **75.9%**, 구현 세부 **70.8%**, 아키텍처 **68.1%**인데 **보안 14.8%, 성능 14.5%**. → 비기능 요구가 현장 컨텍스트 파일에서 비어 있다.
- [논문] P-24 Ambig-SWE(ICLR 2026): 모델은 "명세가 충분한 지시와 부족한 지시를 구분하지 못함". 명세가 부족할 때 상호작용하면 **최대 74%** 향상. → 미결정을 사람이 명시해야 한다.
- [논문] P-SDD Grynets 외(arXiv 2606.00167): 명세 주도 생성에서 기능은 명시되지만 보안은 암묵적으로 남는다. 숨은 블랙박스 API 테스트 221개 기준 대표 실패 50(보안 요구 없음) → 42(ASVS) → 36(다층 보안 모델).
- [커뮤니티] C-패턴4 vincentvandeth(HN 47135917): "A refund is a deterministic business rule — order exists, within return window, amount matches. That decision shouldn't be made by an LLM at [all]" → 원전 취소·환불 예제와 직접 맞물린다.
- [커뮤니티] C-패턴4 avhception(HN 47034087): 사소한 리팩터링을 시켰는데 sqlite 코드가 전부 MariaDB 코드로 바뀌었다.

### §05 화면보다 먼저 상태와 경계를 맞춥니다

**원전 요지:** 도메인(용어·소유권·불변식·상태 전이·권한·경합)과 아키텍처(책임 경계·데이터 흐름·일관성·실패 복구·운영 경계), 계약 체크포인트(API·이벤트·권한·UX)와 흔한 누락, 추적 ID.

**뒷받침**
- [웹] W-E5 Anthropic 팀 사례(2025-07-24): 제품 디자인팀이 "mapping out error states, logic flows, and system statuses to identify edge cases during design". → "화면보다 먼저 상태"의 직접 근거.
- [웹] W-F6 Stripe(Brandur Leach, 2017-02-22): "Networks are unreliable." / "Any one of these leaves the client that made the request in an uncertain situation."
- [웹] W-F9 Pact, W-F8 outbox → 계약 체크포인트의 "이벤트: '한 번만 오고 순서대로 온다'는 암묵적 가정" 누락에 대응.
- [논문] P-31 nl2postcond(FSE 2024): 자연어 의도를 실행 가능한 사후조건으로 바꿔 **Defects4J의 실제 과거 버그 64개**를 포착. → 불변식(INV-CAN-02 등)을 assertion으로.
- [논문] P-30 Clover(SAIV 2024): 코드·docstring·형식 주석 3자 일관성 검사. 올바른 사례 수용률 **최대 87%**, 적대적 오답 거짓 양성 **0**. 독자 대부분은 Dafny를 쓰지 않으므로 "일관성 검사" 아이디어만 전달(논문 리서처 권고).
- [논문] P-44 Mäder & Egyed(EMSE 2015) [2차]: 피험자 71명 통제 실험, 추적성이 있을 때 평균 **24% 빠르고**, 정답 솔루션을 평균 **50% 더 많이**. → REQ → POL → API → AC의 가장 직접적인 정량 근거. AI 이전 연구이므로 에이전트에 그대로 적용된다는 연결은 **책의 추론**임을 밝힌다.
- [논문] P-50 Pearce 외(IEEE S&P 2022): 고위험 CWE 시나리오 89개, 프로그램 1,689개 중 **약 40%가 취약**. **2021년 모델 기준**이라는 시점을 반드시 함께 적는다.
- [커뮤니티] 한국 커뮤니티 요약: 한국 velog 회고에서 도메인 규칙·권한·멱등성 같은 설계 내용을 문서화한다는 글은 거의 없다. 문서화 대상이 "작업 방식"(커밋 메시지·코딩 규칙)에 머문다 → 원전 domain/·계약·validation 층은 한국 담론의 빈자리 (커뮤니티 리서처의 관찰).

### §06 하나의 취소 기능을 끝까지 연결해 봅니다

**원전 요지:** 가상 기능 CAN. 상태 `CONFIRMED` → `CANCEL_PENDING` → `CANCELLED`. 타임아웃은 실패 확정이 아니다. POL/INV, API-CAN-01·EVT-CAN-01 계약, AC-CAN-01~05, SLICE-CAN-01, VAL-CAN-01. "'AI가 검토 완료' 한 문장은 증거를 대체하지 않습니다."

**계약 설계 대조표 — 동일 키 + 다른 입력**

| 출처 | 응답 | 비고 |
|---|---|---|
| 원전 API-CAN-01 | `409 IDEMPOTENCY_CONFLICT` | 원전: "HTTP 상태 코드는 이 예제의 선택입니다." |
| IETF 초안 -07 (W-F7) | `422` (SHOULD) | -07 기준. 원문 문장은 재대조 필요. **-08(2026-10-22)에서 바뀌었는지 [미확인]** |
| Stripe API v1 (W-F6) | 오류 ("errors if they're not the same to prevent accidental misuse") | 상태 코드 번호는 리서치에 없음 |
| IETF -07 | 키 누락 → 400, 처리 중 재시도 → 409 | |

→ 이 차이 자체를 ADR 사례로 쓸 수 있다(웹 리서처 제안).

**뒷받침**
- [웹] W-F6 Stripe API 문서(2026-10 기준): "you can remove keys from the system automatically after they're at least 24 hours old. We generate a new request if a key is reused after the original is pruned." → 원전 경고 "키 기록 정리 후에도 예약·시도 이력과 업무 제약이 중복 환불을 방어해야 합니다"의 실례. 같은 문서: "Idempotency keys are up to 255 characters long." "Retries with the same key return the saved response, including `500` errors." API v2는 "retries don't repeat successful operations"로 동작이 다르다.
- [웹] W-F8 outbox: "As a result, a message consumer must be idempotent" → 원전 "outbox는 '정확히 한 번'을 보장하지 않으므로 수신자 중복 처리도 필요합니다"와 1:1.
- [웹] 수용 기준 표기 3종 비교: GWT(W-F5) · EARS `WHEN ... THE SYSTEM SHALL ...`(W-C3) · OpenSpec "SHALL + WHEN/THEN" 시나리오(W-C6, [원문 직접 확인]).
- [논문] P-12 EvalPlus(NeurIPS 2023): 테스트를 80배 늘리자 pass@k가 **최대 19.3~28.9%** 하락. → AC 하나에 테스트 하나로는 부족, AC-CAN-01~05(정상·실패·중복·지연·권한) 구성 논리.
- [논문] P-29 TiCoder(IEEE TSE): 사용자 상호작용 5회 이내 pass@1 **평균 절대 +45.97%p**. 사용자 15명 연구에서 AI 코드를 올바르게 평가할 가능성이 유의하게 높고 인지 부하가 유의하게 낮았다.
- [논문] P-28 Mathews & Nagappan(ASE 2024): 테스트를 함께 주면 성공률이 일관되게 높아졌다. **구체 %p는 abstract에 없음 → [미확인]**.
- [커뮤니티] C-휴리스틱4 jaemin_ve(velog, 2026-03-11): "명세가 테스트 목록을 결정하고, 테스트 목록이 구현 범위를 결정합니다." 27개 태스크 중 절반이 RED(테스트 작성) 태스크.
- [커뮤니티] C-패턴3 LambdaLogic(HN 49847968): "“Done, all tests pass.” Except they don't."

### §07 Design Ready는 위험에 따라 판단합니다

**원전 요지:** BLOCK·CONDITIONAL·LATER, 게이트 5가지, 스파이크는 질문 하나. "다른 AI 역할의 반박은 누락 탐지에 유용하지만 독립적인 현실 검증은 아닙니다. 같은 잘못된 가정을 공유할 수 있습니다." "정책은 책임자가, 사용성은 사용자 관찰이, 연동·성능은 실행 실험이 확인합니다."

**뒷받침**
- [웹] W-C2 Spec Kit `/speckit-assess-decide`: "Stopping with a documented reason is also a [valid outcome]" [원문 직접 확인, 대괄호 부분은 리서처 보충]. → BLOCK을 정상 결과로 인정하는 장치.
- [웹] W-C4 Böckeler: "the workflow was like using a sledgehammer to crack a nut." / 거짓 통제감 지적. ※ web.md 절별 매핑 표가 B9에 "illusion of control"을 달았지만, B9 인용문에는 그 영어 표현이 없다. "거짓 통제감" 지적은 C4에 있다. 영어 원문 표현으로 인용하지 말 것.
- [논문] P-33·34·35·36·37 → AI 리뷰가 독립 검증이 아닌 이유 (상세 3.E).
- [웹] W-G2 Stack Overflow 2026: AI 결과를 신뢰하는 조건 "when they can easily validate the answers" 48%.
- [커뮤니티] C-패턴7 BonanKou "I'd rather review the plan&assumptions." → Design Ready의 존재 이유.
- [논문] P-52 Grounded Copilot(OOPSLA 2023): 가속 모드 vs 탐색 모드. 설계 문서가 있으면 가속 모드로 쓰고, 없으면 탐색 모드에서 AI가 결정을 대신 내린다 → 스파이크를 따로 떼는 이유 (책의 해석).

### §08 결정은 남기고 아이디어는 승격합니다

**원전 요지:** Draft → Accepted → Superseded. Accepted ADR을 조용히 덮어쓰지 않는다. brainstorming → 검증 → 결정 → 승격. 상태 표시 Exploring / Validated / Promoted / Parked / Rejected.

**뒷받침**
- [웹] W-F1 Nygard(2011-11-15): "One ADR describes one significant decision for a specific project." / "ADRs will be numbered sequentially and monotonically. Numbers will not be reused." 상태 proposed / accepted / deprecated / superseded.
- [웹] W-F2 MADR 4.0.0: 필수 "Context and Problem Statement", "Considered Options", "Decision Outcome". 선택 섹션 "Confirmation"(결정 준수를 어떻게 확인할지)은 원전 "검증 증거를 남깁니다"와 연결.
- [웹] W-B6 ExecPlan의 `Decision Log` → ADR과 실행 계획 안의 결정 로그를 어떻게 나누는지 다룰 자리.
- [웹] W-C6 OpenSpec: `openspec/changes/<name>/` 변경 제안 → 적용 후 archive하며 기준 스펙 갱신 → 원전 "결정 계보 보존"과 대조.
- [논문] P-40 Jansen & Bosch(WICSA 2005) [2차]: 아키텍처 = 설계 결정의 집합. **"knowledge vaporization"이라는 표현이 이 논문 원문에 있는지 [미확인]** → 본문에서는 "흔히 '설계 지식의 증발'이라 부른다"로 쓰고 원문 인용 형식은 피한다.
- [논문] P-42 Buchgeher 외(IEEE Access 2023) [2차]: ADR 채택은 낮지만 해마다 증가, ADR 저장소의 약 절반은 기록이 1~5개뿐. Garcia de Santana Junior 외(ICSA 2026) [2차]: ADR 5,800개 중 **약 63%가 처음부터 "accepted"로 생성** — 숙의 과정을 건너뜀. 전체 저자·DOI [미확인].
- [논문] P-43 Zhou 외(ACM TOSEM 2025): LLM 설계 근거 생성, 전문가 근거 대비 정밀도 **0.267~0.278**, 재현율 **0.627~0.715**, F1 0.351~0.389. 전문가가 말하지 않은 논거 중 64.45~69.42%는 유용, **1.59~3.24%는 오도 가능**. → "대안 목록 뽑기에는 좋고, 결론으로는 위험" = 원전 DESIGNER 역할. Dhar 외(ICSA 2024): zero-shot GPT-4는 관련성 있는 결정을 만들지만 사람 수준에는 못 미침.
- [논문] P-22 Chakrabarti(arXiv 2608.11095) [프리프린트·단독 저자]: 저장소 1,867개, 지시 수명 247,694개. 지시 파일은 생애 동안 **+226%** 커지고 커밋당 순 **+4.9개** 지시가 늘며 오래된 지시일수록 삭제되지 않는다. 원인은 **근거(rationale) 상실** — 근거가 사라지면 삭제가 위험해진다. → "ADR이 왜 필요한가"를 에이전트 시대 언어로 다시 말하는 연결 고리.
- [논문] P-45 Gotel & Finkelstein(ICRE 1994) [2차]: 추적성 문제 대부분이 **명세 이전(pre-RS)** 추적성 부족 때문. → brainstorming 메모에 "채택됨 + 대상 링크"를 남기는 행위.
- [커뮤니티] C-논쟁C azeirah: "An ADR directory is an immutable append-only log of transactions over the architecture ... There are no easy shortcuts." / esafak: "Better then to include the decision record in each PR."
- [커뮤니티] C-휴리스틱7 rfw300(HN 47212355): "The agent session is a messy intermediate output ... If the "why" of a code change is important, have your agent write a commit message or a documentation file that is polished and intended for consumption."

### §09 문서를 개발의 통제 지점에 연결합니다

**원전 요지:** 영향 분석 → 설계 승인 → 코드 PR → 검증·리뷰 → 출시·관측. 영향 매트릭스, 설계 PR·코드 PR 확인 항목. 자동 검사(문서 CI·코드 CI)와 사람 리뷰·출시 게이트·출시 후 확인의 분담과 "이것만으로는 증명하지 못하는 것". "CI 초록색의 정확한 의미"는 정확한 PR head 커밋에서 필요한 검사가 실행되었는지다.

**뒷받침 — 문서 규칙을 실행 가능한 통제로**
- [웹] W-B1: "If you keep adding emphasis to a `CLAUDE.md` line and Claude still misses it, that's a sign the line belongs in a hook." / "ask Claude for *evidence*: the command it ran and its output, or the screenshot. "All tests pass" on its own tells you very little" [요약 경유]. 표 "Who has the last word"(비결정적 = "Claude's summary of what it did", 결정적 = "Branch protection, a person who approves the merge")는 원전 §09 분담표와 1:1로 대응한다.
- [웹] W-B7 harness engineering [2차]: 사용자 정의 린터·구조 테스트로 의존 방향을 강제, 주기적 "garbage collection"(문서 정원 가꾸기)으로 drift를 치운다.
- [웹] W-D1 토스: main 브랜치에서 커밋하려 하면 플러그인 Hook이 감지해 feature 브랜치를 만들도록 유도. "기존의 린터(Linter)가 단순히 에러를 뱉고 차단했다면, 플러그인은 팀의 규율에 맞게 행동을 교정(Align)해주는 가이드 역할을 수행할 수 있습니다."
- [논문] P-22 Ting Yan(arXiv 2608.23550) [프리프린트·단독 저자]: 공개 CLAUDE.md 481개의 보안 규칙 중 Claude Code 내장 통제와 대응하는 것은 **약 4~16%**, 가장 엄격한 기준 **4.4%(95% CI 2.6~6.7%)**. CLAUDE.md는 "write-only channel".
- [논문] P-22 ContextCov(Sharma, arXiv 2603.00822) [프리프린트·단독 저자]: 자연어 지시를 AST 질의·셸 심·아키텍처 검증기로 컴파일. 제약 준수 **88.3%** vs 프롬프트만 **67.0%** vs LLM 반성 **50.3%**, 피드백 비용 3.4배 감소.
- [커뮤니티] C-휴리스틱2 andersco: "If the agent keeps doing something you don't like, then a linting update or an additional test often is more effective than trying to tinker with the Claude.md file." / mkw5053: "Try to push as much as possible as far left in the SDLF (types -> lint rules -> tests -> md)" / philipp-gayret: "implement it in an unavoidable way via hooks and not in a handwritten note to your LLM."
- [커뮤니티] C-패턴1 Milofax(claude-code #2544): "The term “rules” is completely misleading at the moment. Anthropic should call them “recommendations.” My workaround is using Hooks, but it's easy to get into “Hooks' hell”" → 훅도 비용이 있다는 반대편 목소리.

**뒷받침 — 품질·보안 부채가 쌓인다**
- [논문] P-6 He 외(MSR 2026): Cursor 도입 DiD. 속도는 "크고 유의하지만 일시적으로" 증가, 정적 분석 경고와 코드 복잡도는 "크고 지속적으로" 증가. "calls for it [quality assurance] to be a first-class citizen in the design of agentic AI coding tools and AI-driven workflows."
- [논문] P-7 Agarwal 외(MSR 2026): 에이전트가 첫 AI 도구일 때만 크고 앞쪽에 몰린 속도 증가. 품질 위험은 모든 조건에서 지속, 정적 분석 경고 약 **18%**, 인지 복잡도 약 **39%** 증가.
- [논문] P-10 Sakib 외(KDD 2026 AgenticSE 워크숍): 에이전트 PR **38.9%**에 보안 스멜 1개 이상, 그중 82.3%가 공급망 무결성, 치명 등급의 99.6%가 하드코딩 자격 증명. 유출된 실제 비밀의 **67.6%는 사람이 넣었고**, 기존 자동·사람 리뷰가 **81.1%를 통합 전 놓쳤다**. ※ "에이전트가 비밀을 유출한다"로 단순화하지 말 것 — 다수는 사람이 넣었다.
- [논문] P-32 Spracklen 외(USENIX Security 2025): 환각 패키지 비율 평균 **상용 모델 최소 5.2%, 오픈소스 21.7%**, 고유 환각 패키지명 **205,474개**. → 코드 CI·출시 게이트의 의존성 검증. 공유 규칙 파일 프롬프트 주입으로 패키지를 바꾸게 하는 공격도 보고됨(P-22 Wang 외, arXiv 2610.09264, 수치 [미확인]).
- [웹] W-G5 Octoverse 2025: "A first glimpse of coding agent shows 1+ million pull requests that were created between May 2025 and September 2025." → 통제 지점이 필요한 규모.
- [커뮤니티] C-휴리스틱9 "An AI agent deleted our production database"(HN 47911524): "The agent itself enumerates the safety rules it was given and admits to violating every one." / guluarte: "Never give non-deterministic software direct write access to production."

### §10 AI에는 역할과 결정 한계를 함께 줍니다

**원전 요지:** PLANNER·DESIGNER·REVIEWER·IMPLEMENTER와 각 금지. 공통 입력 꾸러미(목표·범위·비범위·원본 경로와 버전·관련 ID·미결정 목록·허용 변경 범위·검증 명령·중단 조건). 프롬프트 1~4. 프롬프트 4의 금지는 "범위 밖 리팩터링, 테스트 삭제로 통과 만들기, 미실행 검증 주장". 사람이 최종 소유할 결정.

**공통 입력 꾸러미 vs 도구 공식 권고 (대조표 소재)**

| 원전 공통 입력 꾸러미 | Codex 4요소 (W-B5) | GitHub agents.md 6영역 (W-B11) | dots Custom Rules (W-A2) |
|---|---|---|---|
| 목표 | Goal | — | — |
| 원본 경로·버전, 관련 ID | Context | project structure | — |
| 범위·비범위, 허용 변경 범위 | Constraints | boundaries (always / ask first / never) | 규칙별 4행동 중 택1 |
| 검증 명령 | Done when | commands, testing | — |
| 중단 조건 → "결정 요청을 남긴다" | — | "ask first" 층 | "먼저 묻기 / 넘기기" |

(대응 관계는 책의 해석)

**뒷받침**
- [웹] W-B5 Codex best practices: "A good default is to include four things in your prompt:" (Goal, Context, Constraints, Done when) / "When Codex makes the same mistake twice, ask it for a retrospective and update `AGENTS.md`." / "if you keep reusing the same prompt or correcting the same workflow, it should probably become a skill." [요약 경유]
- [웹] W-B11 Matt Nigh(GitHub, 2025-11-19): "Three-tier boundaries: Set clear rules using always do, ask first, never do." / "“Never commit secrets” was the most common helpful constraint."
- [웹] W-E2 Kent Beck(2025-06-25) 경고 신호: "Loops." / "Functionality I hadn't asked for (even if it was a reasonable next step)." / "Any indication that the genie was cheating, for example by disabling or deleting tests." → 프롬프트 4 금지와 거의 같다.
- [웹] W-D3 컬리(2025-12-24): "AI 답변을 신입 개발자의 제안이라고 생각하고 검증" / "코드 작성 시간은 줄었지만, 코드 품질과 설계 논의는 오히려 증가" / "코드 리뷰 시간이 오히려 더 많아짐". PM 1명 + 엔지니어 3명이 12개 MSA를 운영하며 "TPM AI 1 + MSA AI 11".
- [웹] W-D5 LY Corporation: "테스트/리뷰/릴리스 역시 최종적으로는 사람이 책임지는 한편, 구현 계획 수립/구현/PR 작성/초기 리뷰는 AI에게 맡기는 형태로 구성했습니다." → 원전 역할표의 실사례. 페이지에 날짜 없음, URL 슬러그로 2026-01-29 추정 [미확인].
- [논문] P-20 Guardrails Beat Guidance(arXiv 2604.11088) [프리프린트]: 규칙 파일 679개(규칙 25,532개), Claude Code(Claude Opus 4.6)로 SWE-bench Verified 실행 5,000회 이상. 개별적으로 이로운 규칙은 **모두 금지형**, 해로운 규칙은 **모두 긍정 지시형**. "constrain what agents must not do, rather than prescribing what they should." **반드시 함께 쓸 것:** 무작위 규칙도 전문가 규칙만큼 성능을 올렸다(둘 다 판별 부분집합에서 **+13.8%p**) → 내용보다 "맥락 점화(priming)" 효과일 수 있다.
- [논문] P-54 MetaGPT(ICLR 2024) 역할 제거 실험: Engineer만 1.0 → +Product Manager 2.0 → +PM·Architect 2.5 → 4개 역할 모두 4.0. 단 +Product Manager·Project Manager 조합은 2.0으로 **단조 증가가 아님**. 효과의 원천이 역할 수가 아니라 구조화된 중간 문서(PRD·설계·인터페이스 명세)라는 해석은 **책의 추론**.
- [논문] P-57 Why Do MAS Fail?(NeurIPS 2025 D&B): 실패 모드 14종. 과제 명세 불이행 11.8%, **명확화 질문 실패 6.8%**, **검증 없음·불완전 8.2%, 잘못된 검증 9.1%**, 단계 반복 15.7% 등. 역할 명세 개선 +9.4%, 상위 수준 목표 검증 단계 추가 **+15.6%**(ProgramDev). 주석 실행 기록 수는 "1,600개 이상"(arXiv) vs "1000+"(NeurIPS 판 abstract) — 판본 차이.
- [논문] P-58·59·60: 강한 프롬프트를 가진 단일 에이전트가 최고의 다중 에이전트 토론과 거의 같다(P-58). 단일 대비 상대 성능 변화가 **분해 가능한 금융 추론 +80.8%에서 순차 계획 −70.0%**까지(P-60). → "역할을 나누는 목적은 에이전트 수를 늘리는 것이 아니라 결정 한계와 검증 지점을 나누는 것" (논문 리서처가 제안한 책의 결론).
- [커뮤니티] C-휴리스틱8 jankdc: "Prompt for technical decisions from user when choices are unsure". 반대 방향 주의: joegibbs(C-패턴4) "the questions the models ask are still often irrelevant ... yet it will then make assumptions about other things that were actually ambiguous."
- [커뮤니티] C-논쟁D: AI가 지시 파일을 써도 되는가 (5장 참조).

### §11 문서의 양은 팀 규모보다 위험에 맞춥니다

**원전 요지:** SMALL 구성(spec/overview.md, domain/rules.md, plan/first-slice.md) vs MEDIUM 구성. 나눌 신호는 "길이보다 동시 변경, 다른 승인자, 독립된 계약과 생명주기". 첫 주 예시는 "조정 가능한 예시". "하루가 밀렸다고 게이트를 생략하지 않습니다." "금전·민감정보·외부 연동이 있으면 작은 팀이라도 필요한 안전 검증은 생략하지 않습니다."

**뒷받침**
- [웹] W-C4 Böckeler: "To be honest, I'd rather review code than all these markdown files." / "repetitive, both with each other, and with the code that already existed."
- [웹] W-C5 Thoughtworks Radar Vol.33(2025-11-05, Assess): "some generate lengthy spec files that are hard to review" / "We may be relearning a bitter lesson" / "handcrafting detailed rules for AI ultimately doesn't scale".
- [웹] W-C9 [2차, 원문 미확인]: Spec Kit으로 만든 간단한 기능 하나가 "파일 8개, 약 1,300줄"(Scott Logic 글로 전해짐, 원문 미열람).
- [웹] W-D4 카카오페이(2026-03-13): "일단 파이프라인을 거치면 개발문서가 굉장히 많이 만들어 집니다 이에 따른 토큰도 많이 소모합니다." / "간단한 개발은 어떻게 해야 할지 애매합니다." / "constitution에 있는 말을 가끔 안 들을 때도 있습니다." 개발 기간 단축은 "크게"라고만 서술, **수치 없음**.
- [웹] W-F3 Ubl: "A clear indicator that a doc might not be necessary are design docs that are really implementation manuals."
- [웹] W-B9 Böckeler(2026-02-05): "build context like rules files up gradually, and not pump too much stuff in there right from the start."
- [논문] P-22 McMillan(arXiv 2605.10039) [프리프린트·단독 저자]: Claude Code 세션 1,650회. 파일 크기·지시 위치·파일 구조·인접 파일 모순 모두 **검출 가능한 효과 없음**. 가장 큰 효과는 세션 내부 — 함수를 하나 더 생성할 때마다 준수 오즈 약 5.6% 감소(OR 0.944, 비단조). ※ W-B2 공식 문서의 "Longer files ... reduce adherence"와 엇갈린다 → 5장 논쟁.
- [커뮤니티] C-패턴5 spec-kit #1174: 버튼 하나 추가 커밋이 "30 files changed, < 20 actual LOC" / roperi: "it generated 35 tasks in 3 phases! I was expecting ~10 tasks in one phase." / surajsrivastav: "Spec kit genrated 4 lines of doc for every actual code." / eduvav: "for smaller ones you guys need a different process - this is not going to survive as a framework".
- [웹] W-G3 DORA AI Capabilities Model의 "working in small batches" [2차, 정확한 명칭 미확인].

### §12 문서마다 같은 작은 메타데이터를 붙입니다

**원전 요지:** 공통 머리말(id·title·status·owner·reviewers·updated·scope·canonical_for·references·decisions·validation), 수용 기준·검증 기록 템플릿. "Accepted 명세는 승인된 약속이지 '이미 구현됨'이 아닙니다." "문서가 오래됐는지는 수정 날짜만이 아니라 실제 변경과의 불일치로 판단합니다."

**뒷받침**
- [웹] W-F2 MADR front matter `status: "{proposed | rejected | accepted | deprecated | … | superseded by ADR-0123"` → 원전 머리말과 결합 가능.
- [웹] W-B10 SKILL.md 이름·설명 메타데이터, W-A1 Hermes 기억 상한(`MEMORY.md` 2,200자(~800 토큰), `USER.md` 1,375자(~500 토큰), 넘으면 자동 압축하지 않고 오류) [원문 직접 확인]. 자동 기억 `MEMORY.md`는 Claude Code에서 "first 200 lines or 25KB"만 로드(W-B2).
- [논문] P-21 오래된 지시 파일 우선 → 원전 "실제 변경과의 불일치로 판단"의 강한 사례.
- [논문] P-52 Vasconcelos 외(CSCW 2023): 5개 연구(N=731). 과의존은 **검증 비용 대비 이득의 전략적 선택**이고, 검증 비용을 낮추면 과의존이 줄었다. → "추적 ID·검증 기록 템플릿은 사람의 검증 비용을 낮춰 과의존을 줄이는 장치" (논문 리서처가 제안한 책의 논리).
- [논문] P-22 Chakrabarti: 근거를 "프롬프트 주석"으로 남기면 과잉 지시를 대부분 제거 [프리프린트·단독 저자].
- [커뮤니티] C-패턴6 simonw(HN 46492381): spec.md를 저장소에 두면 "it survives compaction or lets me start a fresh session entirely." / ozgung(HN 49945933): "I have a single STATUS.md. Agents are instructed to read it first and update it at every session/commit."
- [커뮤니티] C-도구 Hermes 경고 문구(W-A1, 공식 문서): "Don't point two agent processes at the same Hermes home directory. ... two writers sharing one home will compound each other's entries into state neither of them (nor you) authored." [원문 직접 확인] → 메타데이터·소유권 없는 공유 기억의 위험.

### §13 첫 구현에 들어가기 전 확인하세요

**원전 요지:** 18개 항목. "체크 표시 자체가 승인이나 실행 증거를 대신하지 않습니다." "18개를 전부 체크해야 항상 착수 가능한 것은 아닙니다."

**뒷받침**
- [웹] W-B1 "All tests pass on its own tells you very little" → 체크 표시와 증거의 구분.
- [웹] W-B6 ExecPlan: "Every ExecPlan must be fully self-contained." / "Acceptance should be phrased as behavior a human can verify".
- [웹] W-E4 Osmani: "After implementing, compare the result with the spec and confirm all requirements are met." ※ 자기 점검 권고는 3.E(자기 교정의 한계)와 함께 읽어야 한다. 외부 신호(테스트·명령 출력) 없이 모델이 스스로 "충족"을 판정하는 것은 증거가 아니다.
- [커뮤니티] C-패턴7 sukhee(velog, 2026-02-06): "결과적으로 52개 테스트(단위 39 / 통합 7 / E2E 6)가 전부 통과했다. 그러나 솔직히 말하면, 내가 코드를 세세히 모른다는 불안감도 있다."

### §14 가장 작은 유효한 기준선부터 시작하세요

**원전 요지:** 흔한 실패 8가지와 대안, 30분 빠른 시작(5·10·5·5·5분). "30분의 결과는 구현 승인이 아니라, 다음 결정과 검증이 보이는 초안입니다."

**뒷받침**
- [웹] W-E1 Harper Reed: "This entire process will take maybe 15 minutes." / "This is working well NOW, it will probably not work in 2 weeks, or it will work twice as well."
- [웹] W-B11: "Start simple. Test it. Add detail when your agent makes mistakes."
- [논문] P-7 → 흔한 실패 "테스트 통과나 CI 초록을 출시 완료로 해석", "AI가 그럴듯하게 채운 빈칸을 확정"의 실증 배경. P-24 → "빈칸 채우기".
- [커뮤니티] C-휴리스틱1 pamelafox(HN 47034087): "I only add information to AGENTS.md when the agent has failed at a task. Then, once I've added the information, I revert the desired changes, re-run the task, and see if the output has improved."
- [커뮤니티] C-휴리스틱2 simonw(HN 47938417, 2026-04-28): "Most of my projects are without an AGENTS.md/CLAUDE.md at the moment. I've found that if the project itself is in good shape - clear docs, comprehensive tests - you don't need to tell the coding agent much"

---

## 3. 핵심 관점들 — 교차 주제

### 3.A 2025~2026 개발자는 AI로 실제로 어떻게 만드는가 (설문·현장 연구·생산성 증거 충돌)

**설문 (업계 보고서 — 본문에서는 "업계 조사에 따르면")**

| 조사 | 표본·시점 | 핵심 수치 (원문 표현 유지) | 플래그 |
|---|---|---|---|
| Stack Overflow 2025 (W-G1) | 49,000명+ / 177개국 [2차로 표본 확인], 2025-07-29 | "84% of respondents are using or planning to use AI tools" · "51% of professional developers use AI tools daily" (차트 50.6%) · 불신 46% vs 신뢰 33% · "AI agents are not yet mainstream." (에이전트 업무 사용 매일 14.1%, 매주 9%) · 최대 불만 66% ("거의 맞지만 완전히 맞지는 않은" 답) · "Most respondents are not vibe coding (72%)." | 2026 조사로 대체된 수치 |
| Stack Overflow 2026 (W-G2) | "more than 30,000 people", human developers only, 블로그 2026-10-06 | "73% of respondents who indicate using AI coding assistants/agents use them daily." · 코딩 도우미·에이전트가 최대 용도(66%), 챗봇 63% · "The agents of choice are Claude Code (66%) and GitHub Copilot (59%)." · 익숙한 영역 코드 생성 67%, 디버깅 61%, 프로덕션 배포·운영·장애 대응 20% · 신뢰에 출처 표시 필요 93% · 매일 사용자 중 하루 4시간+ 30.9%(n=10,926) · 상위 작업(n=12,547) 익숙한 영역 코드 생성 69.3%, 디버깅·리팩터링 63.8%, 테스트 58.1%, 낯선 영역 56.0% | **Codex 30%·Cursor 26%·Google Antigravity 16%는 달레 블로그 단독 → [미확인]**. "신뢰 31% → 87%"는 질문 보기 변경 탓이라는 달레의 경고 동반. 2026-04 펄스(에이전트 사용 59%, Claude Code 41% → 55%) [2차, 원문 재대조 필요] |
| JetBrains 2026 에이전트 조사 (W-G4) | "more than 15,000 developers worldwide", 조사 기간 2026-04~05 (다른 보도는 5~7월 → [미확인]) | 전문 개발자 90%가 최소 주 1회, 68%가 매일 에이전트 사용("early results") · Claude Code 39%(2025: 3%) · Copilot 21%(29%) · **Codex 16%(0%)** · Cursor 12% · JetBrains AI Assistant·Junie 9%(13%) · 미국 Claude Code 47% | JetBrains 원문 403 → i-programmer(2026-09-02) 경유 [2차] |
| DORA 2025 (W-G3) | "nearly 5,000 technology professionals", 2025-09-23 | AI 채택 "surged to 90%", 전년 대비 14%(**리서처가 포인트로 해석**) 증가 · 중앙값 하루 2시간 · 80%+ 생산성 향상 인식 · 59% 코드 품질 긍정 · 30%는 "a little"(23%) 또는 "not at all"(7%) 신뢰 · AI는 "mirror and a multiplier" | 보고서 자체는 표준화 효과 크기를 씀. 처리량↑·불안정성↑는 [2차] |
| DORA 2024 (P-회색) | 39,000명 이상 | AI 도입 증가에 따라 전달 처리량 −1.5%, 안정성 −7.2% 추정 | [2차]. "도입 25% 증가당"은 RedMonk 재진술일 수 있음 |
| Octoverse 2025 (W-G5) | 2025-10-28, 집계 2024-09-01~2025-08-31 [2차] | "180 million-plus developers" · "80% of new developers on GitHub use Copilot in their first week." · 에이전트 PR "1+ million" (2025-05~09) · "518.7M pull requests merged (+29% YoY)" · "72.6% of developers who use Copilot code review said it improved their effectiveness." | 커밋 수는 "nearly 1 billion"과 "more than 986M" 혼재. Octoverse 2026은 조회 시점에 미발행으로 보임 |
| GitClear 2025 (P-회색) | 변경 2억 1,100만 줄(2020~2024) | 이동 코드 24.8%(2021) → 9.5%(2024), 복사·붙여넣기 8.4% → 12.3%, 5줄 이상 중복 블록 포함 커밋 2024년 약 8배 | [2차]. AI가 썼다는 줄 단위 증거가 아니라 시기별 추세 |
| Uplevel 2024 (P-회색) | Copilot 접근 351명 vs 비접근 434명 | PR 사이클 타임 개선 없음, PR 내 버그율 41% 증가 | [2차]. "접근"을 측정, 실제 사용 아님 |
| Anthropic 2026 Agentic Coding Trends Report (W-E6) | 2026-01-21 [2차, 4월이라는 표기도 있음 → 미확인] | 8개 트렌드, "60% of work" 등 | **본문 미열람. 수치 인용 금지(PDF 대조 전)** |

**통제 실험·현장 연구 — 결론이 갈린다**

| 연구 | 설계 | 결과 | 주의 |
|---|---|---|---|
| P-1 METR (arXiv 2507.09089) [프리프린트] | 숙련 OSS 개발자 16명, 자기 저장소(평균 약 10년, 약 110만 줄), 과제 246개, 과제별 무작위 배정. 도구 Cursor Pro + Claude 3.5/3.7 Sonnet | **완료 시간 기준:** 사전 예측 −24%, 사후 체감 −20%, **실측 +19%(느려짐)**. 경제학 전문가 예측 −39%, ML 전문가 −38%. AI 생성물 채택 44% 미만, 시간의 약 9% 검토·정리, 약 4% 대기. 느려짐 요인 후보에 "암묵적 저장소 맥락" | **부호 주의:** papers.md 요약 표는 "체감 +20% vs 실측 −19%"(속도 기준)로, 상세는 완료 시간 기준으로 적었다. 본문에서는 "완료 시간이 19% 늘었다, 개발자는 20% 줄었다고 믿었다"로 쓴다. 요인은 "기여 가능성이 있는 요인"이지 인과 증명이 아니다 |
| P-1 후속 METR uplift update (블로그 2026-02-24, 동료 심사 아님) | 개발자 57명, 저장소 143개, 과제 800+, 2025-08 시작 | 복귀 개발자 −18% (CI −38%~+9%), 신규 −4% (CI −15%~+9%) — 둘 다 0 포함 | 30~50%의 개발자가 AI 없이 하기 싫은 과제를 제출하지 않음 → 속도 향상 **과소 추정** 편향. METR 표현 "only very weak evidence". 정확한 서술: "2025년 초에는 느려졌고, 후반에는 빨라졌을 수 있지만 측정 자체가 어려워졌다" |
| P-2 Google RCT (ICSE-SEIP 2025) | 정규직 엔지니어 96명 | 과제 시간 약 **21% 단축** | 저자: 신뢰구간이 크고, 2024년 여름 사내 도구의 효과가 다른 도구·시점으로 옮겨진다고 가정할 수 없다 |
| P-3 Cui 외 (Management Science) [2차] | Microsoft·Accenture·Fortune 100 현장 RCT 3건, 4,867명 | 완료 과제 수 **26.08% 증가**(표준오차 10.3%) | 개별 실험 잡음 큼. 경력별 이질성 [미확인] |
| P-4 Peng 외 2023 [프리프린트] | JavaScript HTTP 서버 과제 | **55.8% 빠르게** | 업계가 자주 인용하는 "55%"의 출처. 단일·소규모 그린필드 과제였다는 맥락을 함께 |
| P-5 Echoes of AI (ICSME 2025 RR) | 151명, 2단계 설계 | 2단계(다른 개발자가 AI 없이 발전)에서 완료 시간·품질 유의한 차이 없음. 1단계 AI 사용 시 중앙값 30.7% 감소, 습관적 사용자 55.9% 단축 추정 | "AI 코드 = 유지보수 지옥"은 과장 |
| P-6·P-7 (MSR 2026) | DiD | 속도 일시 증가, 경고·복잡도 지속 증가 (P-7: 경고 약 18%, 인지 복잡도 약 39%) | §09 |
| P-8 AIDev (arXiv 2507.15003 / MSR 2026) | 에이전트 5종 PR 456,000+건(2025판) → 932,791건(2026판) | 에이전트 PR은 빠르지만 수락 빈도가 낮음("trust and utility gap") | |
| P-9 Watanabe 외 (ACM TOSEM) | Claude Code PR 567건 | **83.8% 최종 병합**, 그중 **54.9%는 수정 없이**, 나머지 45.1%는 사람 수정 — 특히 버그 수정·문서·**프로젝트별 표준 준수** | |
| P-10 묶음 | AIDev 기반 | AI 생성 PR 대부분은 리뷰를 받지 않고 리뷰돼도 AI가 주도(Duma 외, EASE 2026). 되돌림률 Codex 6.1% vs 사람 11.5% vs Devin 14.5%(Kraishan [프리프린트·단독 저자]). 테스트 포함 PR 증가(Haque 외). AI 생성 파일 유지보수는 덜 빈번하고 대부분 사람이 수행(Sawada 외) | "리뷰 지표를 사람의 감독으로 읽으면 안 된다" |

**국내 현장 (회사 엔지니어링 블로그)**
- 토스(W-D1): "현재 많은 개발팀이 LLM을 도입하고 있지만, 냉정하게 들여다보면 그것은 '각자도생'에 가깝습니다." / "차이는 단 하나, 작업 전에 컨텍스트를 설계했느냐의 여부입니다."
- 컬리(W-D3): 코드 작성 시간 감소, 설계 논의·리뷰 시간 증가 (Claude Code v2.0.72, Opus 4.5 기준 — 구버전).
- 카카오페이(W-D4): Spec Kit 도입, "마지막 단계에서는 AI가 생성한 코드를 검토하고 수정하는 시간이 점점 더 길어졌습니다."
- LY(W-D5): "에이전틱 코딩을 안정적으로 수행하기 위한 핵심은 초기에 구현 계획을 수립해 재작업을 줄이는 것입니다."

**집필 착지점:** "효과는 맥락에 따라 다르다 → 당신 저장소에서 측정하라"(논문 리서처). 측정이 어려워졌다는 사실 자체가 "검증 증거를 설계해야 한다"는 책 주장을 강화한다.

### 3.B 에이전트 컨텍스트 파일과 하네스 (CLAUDE.md · AGENTS.md · 스킬 · 훅 · 플랜 모드 · ExecPlan)

**1) 공식 동작 규칙 (2026-10 기준)** — §02 표에 정리. 핵심만:
- Claude Code: CLAUDE.md는 "context, not enforced configuration", 200줄 이하 권장, 경로 한정 규칙(`.claude/rules/` + `paths:`), AGENTS.md 직접 읽기, `/doctor`가 "directory layouts, dependency lists, and architecture overviews"를 잘라내고 "pitfalls, rationale, and conventions that differ from tool defaults"를 남기도록 제안 (`/doctor prompt-audit`는 "Claude Code v2.1.283 or later") (W-B2).
- Codex: 디렉터리마다 최대 1개, 루트부터 이어 붙이기, 32 KiB 상한, "Filenames not on this list are ignored for instruction discovery." (W-B4).
- Hermes: first-match 컨텍스트 유형 + AGENTS.md 계층 체인 + 하위 디렉터리 진입 시 "progressively discovers" (W-A1). Hermes 저장소 자신도 루트 AGENTS.md + 하위 디렉터리별 AGENTS.md를 "Routing Table — working in X → read X/AGENTS.md" 방식으로 운용 [원문 직접 확인].
- Kiro steering: 포함 모드 always / fileMatch / manual, "Kiro supports providing steering directives via the AGENTS.md standard." (W-C3).
- 우아한형제들 Rules: "globs에 지정한 경로의 파일들을 작업할 때만 해당 규칙이 활성화됩니다." / "LLM의 기본 지식은 제외하고, '프로젝트 특화 규칙'만 포함" (W-D2).
- AGENTS.md: "used by over 60k open-source projects" / "The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything." (W-B3).

**2) 원리 문서**
- W-B8 Anthropic(2025-09-29): 컨텍스트는 유한한 "attention budget". just-in-time 로드·compaction·구조화된 노트·서브에이전트. "CLAUDE.md files are naively dropped into context up front".
- W-B9 Böckeler(2026-02-05): 로드 주체(LLM·사람·에이전트 소프트웨어)로 분류. "Allowing the LLM to decide when to load context is a prerequisite for running agents in an unsupervised way." / "Once the agent gets all these instructions and guidance, execution still depends on how well the LLM interprets them!"

**3) 스킬과 훅**
- 스킬 = agentskills.io 오픈 표준. Claude Code `.claude/skills/`, Codex `.agents/skills/`, Hermes(호환 명시) (W-B10). Codex 스킬 위치는 [2차].
- 훅: Claude Code PreToolUse 훅(W-B2). Codex 훅 `.codex/hooks.json`(기능 플래그 필요하다는 2차 기술) [2차]. **"Claude Code 27 vs Codex 5" 훅 이벤트 수 비교는 비공식 저장소 주장 → [미확인], 쓰지 말 것.**
- 토스: 팀 규칙을 Claude Code 플러그인으로 묶어 마켓플레이스로 배포. "플러그인 코드가 업데이트되면, 팀원들의 에이전트 행동 양식도 즉시 업데이트됩니다." (W-D1)
- 연구: Galster 외(arXiv 2602.14690): 설정 메커니즘 8종, 저장소 2,853개. 컨텍스트 파일이 지배적이고 흔히 유일한 메커니즘, **Skills·Subagents 채택은 드묾**, Skills는 실행 스크립트보다 정적 지시에 의존 (P-16 후속).

**4) 플랜 모드**
- Claude Code: Shift+Tab 순환, `/plan`, `claude --permission-mode plan`, `.claude/settings.json`의 `defaultMode: plan`. 플랜 모드에서는 읽기·탐색은 하되 소스를 편집하지 않는다 (W-B12 — **검색 결과 요약 경유, 검색 엔진 캐시 약 105일 전 → 세부 재확인 필요**).
- Codex: "Plan mode lets Codex gather context, ask clarifying questions, and build a stronger plan before implementation." (W-B5). 토글 `/plan` 또는 Shift+Tab은 [2차].
- 커뮤니티 논쟁 B(5장): "plan mode has always been a prompt"라는 자칭 Claude Code 개발자 발언 [커뮤니티 의견, 검증 필요].

**5) ExecPlan (W-B6)** — "Every ExecPlan is a living document." / "Every ExecPlan must produce a demonstrably working behavior" / AGENTS.md에 넣을 문장 예: "When writing complex features or significant refactors, use an ExecPlan". **페이지가 "archived, may reference outdated models"라고 표시, 본문에 `gpt-5.2-codex` 권장 언급 → 구버전 정보일 수 있음.**

**6) 하네스 엔지니어링 (W-B7) — 인용 시 가장 조심할 자료**
- 저자·날짜: Ryan Lopopolo, 2026-02-11 (검색 스니펫 + InfoQ 2026-02-21로 확인). **본문 403.** 아래 문장은 검색 스니펫에 원문으로 노출된 것이다 [원문 재대조 필요]:
  - "We had weeks to ship what ended up being a million lines of code. Over that period, roughly 1,500 pull requests have been opened and merged with a small team of just three engineers"
  - "The first commit to an empty repository landed in late August 2025. Even the initial AGENTS.md file that directs agents how to work in the repository was itself written by Codex."
  - "Early progress was slower than we expected, not because Codex was incapable, but because the environment was underspecified."
  - "Humans may review pull requests, but aren't required to. Over time, we've pushed almost all review effort towards being handled agent-to-agent."
- "what Codex cannot see does not exist" 표현, "~100줄" 목차형 AGENTS.md → [2차]/[미확인].
- **긴장:** "AGENTS.md도 Codex가 썼다"는 사례는 P-17(LLM 생성 컨텍스트 파일은 효과 없음)·C-논쟁D와 부딪힌다. 둘 다 싣되 사례의 맥락(OpenAI 내부, 하네스 전체 설계)과 연구의 맥락(SWE-bench류 과제)을 구분한다.

**7) 실증 연구 요약 — 컨텍스트 파일 효과는 갈린다**

| 연구 | 결과 | 플래그 |
|---|---|---|
| P-17 Gloaguen 외 (arXiv 2602.11988) | LLM 생성 파일 vs 없음: 해결률 −0.5%(SWE-bench, p=0.87), −2%(CTXbench, p=0.37). 개발자 작성 vs 없음: +2.4%(CTXbench, p=0.21). 모두 유의하지 않음. **개발자 작성 vs LLM 생성: 평균 7%p 높음(p=0.038)**. 비용: LLM 생성 약 20%(SWE-bench)·23%(CTXbench) 증가, 개발자 작성 최대 19%. `uv` 언급 시 인스턴스당 약 1.6회 사용 vs 언급 없으면 0.01회 미만 → 지시는 잘 따름. 저장소 개요는 도움 안 됨, LLM 생성 파일의 95~100%가 개요 포함 | [프리프린트] |
| P-18 Lulla 외 (arXiv 2601.20404) | 저장소 10개, PR 124건. 실행 시간 중앙값 **−28.64%**, 출력 토큰 **−16.58%**, 과제 완료 행동은 비슷 | [프리프린트] 5쪽 단편 |
| P-19 Khatri (arXiv 2607.27250) | Claude Code·Codex, 과제 17개, 실행 288회. 정확도 변화 없음(동등성 검정 10~15%p 이내). 실패 원인은 저장소 지식이 아니라 구현 기술. 난이도 경계가 에이전트마다 다름(Spearman ρ=0.75) | [프리프린트·단독 저자] |
| P-10 Arabat & Sayagh (MSR 2026) | 프로젝트 148개·에이전트 PR 15,549건. 지시 파일 생성 후 병합률 20%p 이상 오른 프로젝트 27.7%, 내린 프로젝트 26.35% → 자동으로 좋은 결과 안 남. 오른 프로젝트는 더 길고 잘 구조화(탐색적 관찰) | |
| P-20 Guardrails Beat Guidance | 금지형 규칙만 이로움, 무작위 규칙도 +13.8%p, 규칙 0~50개에서 통과율 안정 | [프리프린트] |
| P-21 Stale Instruction Files | 충돌 시 90.1%가 낡은 파일 추종 | [프리프린트], 2026-10-22 |
| P-22 Yan / ContextCov / McMillan / Chakrabarti | 보안 규칙 4~16%만 내장 통제와 대응 / 실행 가능 제약 88.3% / 파일 구조 효과 없음 / 지시 파일 +226% 성장 | 모두 [프리프린트·단독 저자] |
| P-14 Chatlatanagulchai 외 (PROFES 2025) | CLAUDE.md 253개: 얕은 계층, 운영 명령·기술 구현 메모·상위 아키텍처 지배 | |
| P-15 Agent READMEs (TOSEM) | 파일 2,303개, 설정 코드처럼 잦고 작은 추가로 진화, 보안 14.8%·성능 14.5% | |

**충돌 주의 — 커뮤니티가 전한 P-17 수치:** HN 47034087에서 medler는 "context files tend to reduce task success rates compared to providing no repository context, while also increasing inference cost by over 20%."를, deaux는 "개발자 작성 파일 평균 4% 향상, LLM 생성 파일 평균 3% 하락"을 인용했다 [커뮤니티 의견, 검증 필요]. papers.md는 HTML 본문에서 위 표의 수치(−0.5%/−2%/+2.4%, 7%p)를 확인했다. abstract 판본 차이일 수 있다. **본문 수치는 papers.md(P-17)를 따르고, 커뮤니티 인용 수치는 쓰지 않는다.** 반론도 함께: energy123 — 이 연구의 "context"는 처방형 스펙·요구사항 파일이 아니라 코드베이스 요약 파일만 다룬다(C-휴리스틱1).

### 3.C 스펙 주도 개발(SDD) 도구와 비판

**도구 지도 (2026-10 기준)**

| 도구 | 산출물 구조 | 특징 | 출처 |
|---|---|---|---|
| GitHub Spec Kit v1.2.4 | constitution → specify → plan → tasks → implement → converge | 확장: 버그(`/speckit-bug-assess|fix|test`), 사전 평가(`/speckit-assess-intake|research|define|shape|decide`). 스타 약 14.3만 | W-C1, W-C2 [원문 직접 확인] |
| Kiro (AWS) | `requirements.md`(또는 `bugfix.md`) + `design.md` + `tasks.md`, steering | EARS 표기, GA에 "property-based testing for spec correctness", 터미널 에이전트 | W-C3 |
| OpenSpec v1.15.0 | `openspec/changes/<name>/`(proposal.md·specs/·design.md·tasks.md) → archive로 기준 스펙 갱신 | brownfield 우선, delta 모델, 팀용 "Stores"(베타). "Your AI writes these; you review the plan before any code is written." 스타 약 7.3만 | W-C6 [원문 직접 확인] |
| BMAD v6.12.4 | 제품·아키텍처·UX·개발·테스트 관점 전문 에이전트 | "Coding assistants are effective at implementation, but they often turn unstated assumptions into code." Claude Code·Codex 플러그인 마켓플레이스 배포. 스타 약 5.5만 | W-C7 [원문 직접 확인] |
| Agent OS v3.0.0 | 표준 주입 + 스펙 | "a system for injecting your codebase standards and writing better specs for spec-driven development." | W-C8 |
| Tessl | spec-as-source 탐색 | "the full framework is currently part of Tessl's closed beta program" [검색 스니펫]. 2026 초 "스킬 패키지 매니저"로 축 이동 주장 [미확인] | W-C8 |
| 국내 k-sdd, ITDA-SDD | velog 공개 (2025-12-29, 2026-01-14) | 강의·도구 홍보 성격, "1,200줄 요구사항을 반나절 만에" 등 성과 수치는 검증 필요 | C-한국 |

**버전 주의 (Spec Kit 명령 표기):** 2026 v1.x README는 하이픈(`/speckit-specify`)과 "skills" 용어. 2025년 자료는 `/speckit.specify`(점), 그 이전은 `/specify`. 카카오페이 사례의 "constitution → specify ↔ clarify → plan → tasks → analyze → implement"는 **구버전 흐름**이다. 본문에서는 "Spec Kit v1.2/2026-10 기준"으로 못 박는다.

**Kiro GA 날짜 주의:** 공식 블로그 **2025-11-17**이 맞다. 2차 출처 일부의 2026-03 또는 2026-05는 틀렸다.

**비판 (관점 A / 관점 B는 5장 논쟁 A에)**
- Böckeler(W-C4): 세 도구 모두 실제로는 대부분 spec-first. "Ultimately, MDD never took off for business applications" / "Are we making something worse in the attempt of making it better?" (Verschlimmbesserung) / "just because the windows are larger, doesn't mean that AI will properly pick up on everything that's in there."
- Thoughtworks Radar Vol.33(W-C5): Assess 링. "the workflows remain elaborate and opinionated". **Vol.34(2026-04) 이후 링 변화 [미확인].** 페이지에 "no longer on the current edition" 표시.
- Scott Logic(2025-11-26)·Conffab(2025-12-09) "재발명된 폭포수" 논쟁 [2차, 원문 미확인]. 반론 Wavect: "스펙 워크플로는 느린 리뷰·테스트 부재·불명확한 소유권을 보완하지 못하지만 그 약점을 드러낸다" [2차].
- 연구: Spec Kit Agents(Taghavi & Bhavani, arXiv 2604.05278): SDD 에이전트가 대형 저장소에서 "context blind"해 API 환각·아키텍처 위반. 저장소 근거 훅으로 LLM-judge **+0.15/5(+3.0%)**, SWE-bench Lite **58.2%** Pass@1 — 효과 크기가 작다는 점도 함께.
- 커뮤니티: spec-kit #75 "SpecKit creates the illusion of work, generating a bunch of text"(NaikSoftware, 2025-09-08) / #620 스펙 일관성 유지 방법 질문 / #1174 tinySpec 제안.

**원전의 답 (책의 해석):** "문서의 양이 아니라 결정과 증거의 연결", "Design Ready는 위험에 따라"(§07), "문서의 양은 위험에 맞춘다"(§11).

### 3.D 독자 도구 스택 프로필 (Claude Code · Codex · Hermes Agent · OpenAI dots)

#### Claude Code — 2.1.312 (npm, 2026-10-27) [원문 직접 확인]
- 지시 계층: CLAUDE.md(200줄 이하 권장), `.claude/rules/` + `paths:`, 자동 기억 `MEMORY.md`(첫 200줄 또는 25KB), AGENTS.md 직접 읽기(W-B2).
- 결정적 통제: 훅(PreToolUse 등)·deny 규칙·관리 설정(W-B1).
- 플랜 모드(W-B12, 세부 재확인 필요), 서브에이전트, 스킬(`.claude/skills/`), 플러그인 마켓플레이스(W-D1, W-C7).
- 설문 위상: Stack Overflow 2026 에이전트 선택 66%(W-G2), JetBrains 2026 업무 사용 39%(2025: 3%)(W-G4) [2차].
- 연구 속 위치: Claude Code PR 567건 중 83.8% 병합(P-9). 첫 사람 리뷰까지 중앙값 12.6시간(P-10 Kraishan [프리프린트·단독 저자]).
- 알려진 고통: CLAUDE.md 무시(#2544, #33603), 세션이 길어지면 규칙이 희미해짐 (C-패턴1·6) [커뮤니티 의견, 검증 필요].

#### OpenAI Codex — CLI 0.165.0 (npm, 2026-10-28) [원문 직접 확인]
- 지시 계층: AGENTS.override.md → AGENTS.md → 대체 파일명, 디렉터리마다 최대 1개, 32 KiB 상한(W-B4).
- 프롬프트 4요소 Goal / Context / Constraints / Done when, 플랜 모드, 서브에이전트, 스킬(`.agents/skills/` [2차]), 훅(`.codex/hooks.json` [2차]) (W-B5).
- 흔한 실수: "Running live tasks on the same files without using Git worktrees" (W-B5).
- 설문: JetBrains 2026 업무 사용 **16%(0%에서)**, 인지도 65%(11%에서) [2차]. Stack Overflow 2026 Codex 30%는 [미확인].
- 연구: 되돌림률 6.1%(P-10 Kraishan [프리프린트·단독 저자]). Stale instruction 실험에서 80회 중 20회 기존 코드를 파일에 맞게 다시 쓰고 그중 17회 테스트 실패(P-21).
- 하네스 엔지니어링 사례(W-B7) [원문 재대조 필요].

#### Hermes Agent (Nous Research) — v0.22.5 (2026-10-23) [원문 직접 확인]
- 정체: "The self-improving AI agent built by Nous Research. It's the only agent with a built-in learning loop ..." [원문 직접 확인]. 코딩 전용이 아니라 범용 상시 에이전트. CLI·TUI·메신저 게이트웨이(Telegram·Discord·Slack 등), cron 스케줄러("Daily reports, nightly backups, weekly audits — all in natural language, running unattended."), 서브에이전트("Spawn isolated subagents for parallel workstreams."), 스킬("Compatible with the agentskills.io open standard."), 장기 기억.
- **독자 환경에서의 위치:** 번들 스킬 `claude-code` v2.2.1("Delegate coding to Claude Code CLI (features, PRs)"), 같은 계열 `codex`, `opencode` → **코딩 에이전트를 부리는 자동화·오케스트레이션 층** (W-A1 식별 결론).
- 컨텍스트 파일·기억 규칙: §02, §12 참조.
- 커뮤니티 [커뮤니티 의견, 검증 필요]: hadlock "Hermes is a more persistent version of claude code, or a harness for claude code/codex and is pro-vendor agnostic by design." / andy_xor_andrew 기본 구성에서 "over 10k of context used just to list them all"(스킬 목록) / jacobgold 용도 "code review, email inbox/spam filtering, website monitoring for bad links/typos" / 표절 논란 언급(내용 미확인).
- **날짜 주의:** 출시일을 두고 2차 출처가 엇갈린다(2025-07 vs 2026-02). 1차 사실은 "저장소 생성 2025-07-22, 첫 태그 릴리스 2026-03-12". "v0.9.0 Everywhere Release 2026-04-13", "v0.20.0 Herald Release 2026-08-03"은 [2차]. GitHub 스타 "약 25.8만 (2026-10-28 조회)" [원문 직접 확인].

#### OpenAI dots — DevDay 2026 (2026-09-29) [2차 교차 확인, 1차 문서 403]
- 표기: 소문자 **"dots"**, 단수 "a dot". ChatGPT 안의 상시 실행 개인 에이전트. 코딩 전용이 아니며 코딩은 Codex로 넘긴다.
- 교차 확인된 사실 (2026-09/10 기준, TechCrunch·DataCamp):
  - 각 dot은 자체 클라우드 컴퓨터와 브라우저에서 실행, 대화 사이에도 목표를 진행.
  - 모델 GPT-6 Astra (TechCrunch: "powered by GPT-6 Astra").
  - 제공: ChatGPT Pro(EEA·스위스·영국 제외)와 Business Premium. Enterprise·Edu·Healthcare는 관리자가 켜는 베타(DataCamp). TechCrunch: "Dots will be available starting Tuesday in ChatGPT, for Pro and Business Premium users in eligible markets."
  - 채널: ChatGPT(데스크톱·웹·모바일), Slack, Teams. 문자 메시지는 이후 또는 제한 베타.
  - 통제: "Custom Rules let you override them per action." 규칙별 4가지 행동(묻지 않고 실행 / 사전 승인 시 실행 / 먼저 묻기 / 넘기기). "Auto-review sits underneath, checking actions that could affect your accounts or share information." (DataCamp가 OpenAI 안전 문서를 인용)
  - 기억: "Your dot inherits memories from ChatGPT and creates its own." (DataCamp). 개별 dot 기억을 보거나 지울 수 없다는 기술은 [2차, 미확인].
  - Codex 연계: dot은 Codex 클라우드 환경에서 클라우드 태스크를 만들 수 있다(환경은 Codex에서 미리 만들어야 함). 로컬 접근을 켜면 사용자 기기에서 Work·Codex 태스크를 만든다. 개발자 예시 "고객 피드백을 모니터링하다가 영상이 첨부된 PR을 돌려주는 dot" (DataCamp).
- [미확인]: "4,000개 이상 앱 연결", "GPT-6.1 Astra 업그레이드 보류"(aiweekly 단독), 가격 세부, 공식 DevDay 요약 URL 본문.
- 커뮤니티 [커뮤니티 의견, 검증 필요]: 공식 페이지를 인용한 댓글 — "Each dot has its own cloud computer, where it can browse, analyze information, create files, and run tools"(nico), "proactive research"는 연결 앱을 "read-only" 도구로(Imnimo), Microsoft Agent 365 연동 계획(CharlieDigital). 정체성 혼란(HeavenFox "I read it a few times and still have zero idea what this thing is." / wxw "The lines between Codex, ChatGPT Work, and Dots is getting a bit blurry to me."). 비용("OpenAI's dot assistant burned 300K+ tokens in a day without a single prompt", HN 제목 2026-10-14). 보안("Ask HN: Are people aware OpenAI Dots intercept SSL?" 2026-10-25 — 주장 자체 미확인). slurpyb(2026-10-28): "The handoff procedure absolutely blows. Just spits in your face re: understanding intent between tasks".
- **책에 쓸 때:** 출시 한 달 된 제품이다. 기능·제공 범위는 "2026-10 기준"으로 못 박고, 위 교차 확인 범위를 넘지 않는다. 공식 도움말 문서를 다시 대조할 것.

#### ⚠ Hermes·dots와 설계 문서를 잇는 공개 실천은 아직 없다
- 커뮤니티 리서처: "설계 문서를 먹여 자동화 에이전트를 운용하는" 실사용 논의를 **찾지 못했다**. Hermes 담론은 개인 비서형(기억·스킬·cron) 중심이고, Hermes 이슈(#29125, #5257, #344)도 설계 문서·스펙과의 연결 논의가 없다(제목만 확인). dots는 출시 한 달 차라 사용 패턴 담론이 형성 전이다.
- 근거로 쓸 수 있는 것은 (1) 공식 문서의 사실(Hermes 컨텍스트 파일 로드 규칙, Claude Code·Codex 위임 스킬, dots Custom Rules·Codex 태스크 생성)과 (2) 원전 §09·§10과의 구조적 대응(dots의 "ask first / hand off"는 원전의 "중단 조건·결정 요청"과 같은 구조 — 웹 리서처의 해석)뿐이다.
- slurpyb의 "handoff에서 의도가 사라진다"는 지적이 이 책 주제(작업 간 의도 전달 = 문서)와 직접 닿는 유일한 커뮤니티 단서다.
- 따라서 Hermes·dots로 설계 문서를 운용하는 장면은 **저자 경험·제안으로 명시**하고, "업계에서 이렇게 한다"로 쓰지 않는다.
- 인접 사례(Hermes·dots가 아님): mike_hearn은 전용 UNIX 계정에서 영구 세션으로 도는 Codex 둘을 "AI employees"로 운영, 고객 지원 티켓을 밤새 처리하고 "waiting for my approval" (HN 49896604). OliverGuy는 읽기 전용 자격 증명으로 에이전트가 MR까지만 열게 한다 (C-휴리스틱9) [커뮤니티 의견, 검증 필요].

### 3.E AI 자기 검토의 한계와 상관된 오류

- **[논문] P-33 Huang 외(ICLR 2024):** "LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction."
- **[논문] P-34 Kamoi 외(TACL 2024)** 3가지 결론: (1) 자기 교정에 특별히 적합한 과제를 빼면 프롬프트된 LLM의 피드백으로 성공한 선행 연구가 없다, (2) 신뢰할 수 있는 외부 피드백이 있는 과제에서는 잘 작동, (3) 대규모 미세조정으로 가능. → 정리 문장: **"AI는 테스트·컴파일러·계약 검사 같은 외부 신호가 있을 때만 스스로 고친다."** (논문 리서처의 요약) → 원전 §10 공통 입력 꾸러미에 "검증 명령"이 있는 이유.
- **[논문] P-35 Kim 외(ICML 2025):** LLM 350개 이상. "on one leaderboard dataset, models agree 60% of the time when both models err." 더 크고 정확한 모델일수록 아키텍처·제공사가 달라도 오류 상관이 높다.
- **[논문] P-36 Goel 외(ICML 2025):** LLM 판정자는 자신과 비슷한 모델을 편애, 능력이 높아질수록 오류가 서로 비슷해지는 추세.
- **[논문] P-37 Panickssery 외(NeurIPS 2024):** 자기 인식 능력과 자기 선호 편향의 강도가 선형 상관.
- **[논문] P-38 Ahmed 외(arXiv 2408.05534, MSR 2025 게재 [미확인]):** 일부 주석 과제에서 LLM이 사람 간 일치도에 근접. 모델-모델 일치도를 "LLM에 맡겨도 되는가"의 예측 지표로 제안 → AI 리뷰를 전면 부정하지 않는 균형 근거.
- **[논문] P-56 AgentCoder [발표처 미확인], P-57:** 효과의 핵심은 역할 이름이 아니라 외부 실행 피드백. MAS 실패의 상당수가 검증 없음·잘못된 검증.
- **[웹] W-B1:** "A reviewer that's asked to find problems will always find *something*. If you fix every finding, you end up with extra abstraction layers and tests for cases that can't happen." → 리뷰 에이전트의 과잉 지적 비용.
- **[커뮤니티] C-휴리스틱6 교차 모델 리뷰 (Claude Code로 쓰고 Codex로 리뷰):** mrcode007 "It finds errors CC doesn't." / robertwt7 "it always find something that claude missed." / stavros "it's crucial that different models write the code vs review it." / nickdichev "One is the sword (claude code) one is the shield (codex)".
  - 반대: HN 49166538에서 mil22가 인용한 초록 — Claude가 Codex 초안을 리뷰하면 71.6% → 89.7%, Codex가 Claude 초안을 리뷰하면 91.4% → 82.8%로 하락. **원 논문 미대조, 논문 리서치에도 없음 → 수치 인용 금지 또는 "댓글이 전한 미확인 결과"로만.**
  - shaftway: "there will be a significant number of engineers who are using AI to write and review the code, rubber stamp it, and push it into prod, with disasterous results."
- **[커뮤니티] C-패턴3:** 에이전트가 테스트를 지우거나 우회해 초록불을 만든다. Kent Beck이 "having trouble stopping AI agents from deleting tests in order to make them “pass!”"라고 했다는 **에피소드 소개문 기준(녹취록 미확인)**. r/AI_Agents: "Codex + GPT-5.4 decided to bypass the validation tests" / "GPT-5.4 likes to just replace the "calculated" value with the "reported" value" (미러 스냅샷). LambdaLogic: "It's taking verification authority away from [the agent]".
- **[원전] §07:** "다른 AI 역할의 반박은 누락 탐지에 유용하지만 독립적인 현실 검증은 아닙니다." §10 REVIEWER 금지 "'문제 없음'을 실행 증거로 취급하기", 프롬프트 3 "역할: 독립적인 관점의 설계 리뷰어. 승인자가 아니다."
- **집필 착지점:** "구현 에이전트와 리뷰 에이전트를 다른 모델로 바꾸면 독립 검증이 된다"는 흔한 믿음은 P-35·36으로 약해진다. 결론은 원전 §07 "위험에 맞는 증거 종류를 선택하세요"로 착지 (논문 리서처 제안).

### 3.F 인간 요인 — 자동화 편향·과의존·탈숙련

- **[논문] P-47 Bainbridge(1983) [2차]:** 자동화의 역설.
- **[논문] P-48 Parasuraman & Manzey(2010) [2차]:** 자동화 편향은 초보·전문가 모두에서, 단순 연습으로 쉽게 없어지지 않는다 → "전문가라서 괜찮다"는 반론에 대한 답.
- **[논문] P-49 Perry 외(ACM CCS 2023):** AI 도우미(codex-davinci-002)를 쓴 참가자가 유의하게 덜 안전한 코드를 썼고, 동시에 자기 코드가 안전하다고 더 믿었다. AI를 덜 신뢰하고 프롬프트를 적극 다듬은 참가자의 코드가 취약점이 적었다. **참가자 수 [미확인]**. → METR의 체감·실측 괴리와 같은 구조: "확신은 증거가 아니다".
- **[논문] P-51 Shen & Tamkin(Anthropic, arXiv 2601.20245) [프리프린트]:** 52명(그룹당 26명), Python 비동기 라이브러리 Trio 학습. AI 그룹이 27점 만점 퀴즈에서 **4.15점 낮음(17% 차이, Cohen's d=0.738, p=0.010)**, 완료 시간 유의한 단축 없음. 저득점(40% 미만) 패턴: AI 위임, 점진적 AI 의존, 반복적 AI 디버깅. 고득점(65% 이상): 생성 후 이해, 코드+설명 혼합, 개념 질문. "We find that AI use impairs conceptual understanding, code reading, and debugging abilities, without delivering significant efficiency gains on average." / "Our findings suggest that AI-enhanced productivity is not a shortcut to competence..."
- **[논문] P-52 Lee 외(CHI 2025) [2차]:** 지식 노동자 319명, 사례 936개. GenAI 신뢰가 높을수록 비판적 사고가 적고, 자기 능력 확신이 높을수록 많다. 비판적 사고가 정보 검증·응답 통합·과제 관리(stewardship)로 이동.
- **[논문] P-52 Vasconcelos 외:** 검증 비용을 낮추면 과의존이 줄어든다 → 템플릿·ID가 사람의 검증 비용을 낮춘다는 책의 논리.
- **[논문] P-52 Prather 외(ICER 2024):** 고전하는 학생은 "유능함의 착각(illusion of competence)"으로 끝난다. Wang 외(FAccT 2024): 적절한 신뢰 형성의 3대 과제 = 기대 설정, 도구 설정, 제안 검증. Mozannar 외(CHI 2024): 제안 검증에 드는 시간 비용 가시화.
- **[논문] P-52 Kosmyna 외(MIT Media Lab, arXiv 2506.08872) [프리프린트]:** 에세이 쓰기 연구, EEG. **코딩 연구가 아니므로 "인지 부채" 용어 소개 정도로만.**
- **[논문] P-10 Sakib 외:** 보안 리뷰 81.1% 누락, 저자가 "개발자 경계심 저하 가능성"을 제기.
- **[커뮤니티]** taurath(HN 49840054): "I'm actively watching understanding slip away from developers, code review getting paired down to no comment checkmarks" / dsign: "Even if the model is smarter than me, it's still working on my project, and thus I need to keep a mental view of the system." / sukhee: "최종 책임은 나에게 있다고 생각한다." / code_able: "생성은 AI가 담당했지만, 통합과 QC 책임은 여전히 개발자의 영역이었다." / k-sdd 소개문: "AI에게 개발을 맡기고 싶지만, 주도권은 넘기기 싫다".
- **[웹] W-D5 LY:** "AI가 작성한 코드를 사람이 책임을 진다는 인식이 반드시 필요합니다."
- **[원전] §10:** "AI 역할을 나누더라도 이 책임이 자동으로 이전되지는 않습니다."
- **집필 착지점:** "사람이 최종 결정을 소유"는 윤리가 아니라 **공학적 필요**다. 사람의 판단력이 마모되면 통제 계층 전체가 무너진다 (논문 리서처 제안). "설계 문서를 직접 쓰는 행위"가 개발자의 이해를 지키는 장치라는 논거로 P-51 고득점 패턴을 쓴다.

---

## 4. 대표 사례

### 4.1 국내 엔지니어링 블로그

| 사례 | 날짜 | 요지 | 연결 절 |
|---|---|---|---|
| 토스페이먼츠 김용성 "Harness를 통한 조직 생산성 저점 높이기" (W-D1) | 2026-02-26 | 팀 규칙을 Claude Code 플러그인으로 묶어 마켓플레이스 배포, 훅으로 main 커밋 방지 | §01 C, §02 guides/, §09 |
| 우아한형제들 이재홍 "하네스 엔지니어링으로 팀 맞춤형 AI 환경 구축하기" (W-D2) | 2026-04-17 | glob 범위 Rules, 스크립트가 메타데이터를 JSON으로 요약해 전달, Swagger 기반 생성 | §02, §05 |
| 컬리 이준환 "OMS에서 Claude AI를 활용하여 변화된 업무 방식" (W-D3) | 2025-12-24 (Claude Code v2.0.72, Opus 4.5 기준 — 구버전) | 역할별 컨텍스트로 TPM AI 1 + MSA AI 11, AI 답을 신입 제안처럼 검증 | §07, §10 |
| 카카오페이 wayne.cai "SDD (spec-kit) 에이전트 코딩 실전기" (W-D4) | 2026-03-13 (if(kakao) 발표 기반 추정) | 마음에 안 들면 코드가 아니라 specify로 돌아가 스펙 재정의, 문서·토큰 과다, 간단한 개발은 애매. "개발자의 역할은 '코드를 작성하는 사람'에서 '스펙을 검증하고 테스트를 설계하는 사람'으로 점점 변화할 것이라고 생각합니다." | §08, §11 |
| LY Corporation Hirano Keisuke "코파일럿에서 파일럿으로" (W-D5) | 날짜 없음, 2026-01-29 추정 [미확인] | Jira·Confluence 명세를 MCP로 연결, 사람=스펙·테스트·리뷰·릴리스 최종 책임, AI=계획·구현·PR·초기 리뷰 | §10 |
| 기타 인덱스 (W-D6, 본문 미확인) | — | 카카오테크 posts/711·762, 배민 전자계약서 화면 개편기(2026-09-15, "AI가 적게 읽어도 되도록 구조를 먼저 설계" [검색 요약, 미확인]), 달레 SDD 글(미열람) | — |

### 4.2 해외 사례·실무 에세이
- OpenAI 하네스 엔지니어링(W-B7) — 수치 인용은 [원문 재대조 필요].
- Anthropic 팀 사례(W-E5): 보안팀 "asking Claude for pseudocode, guiding it through test-driven development, and checking in periodically", 제품 디자인팀 오류 상태 매핑, "set up autonomous loops ...". **"Inference 팀 R&D 시간 80% 단축", "Vim 모드 코드 70%를 Claude가 작성" → [2차, 미확인]. PDF 대조 전 인용 금지.**
- Harper Reed(W-E1), Kent Beck(W-E2), Simon Willison(W-E3; 2026-02 추기 "Agentic Engineering"이 더 널리 쓰이는 용어가 됨, 2025-09 "designing agentic loops"·2026-02-23 "Agentic Engineering Patterns" 연재 [2차]), Addy Osmani(W-E4).

### 4.3 챕터 오프닝 장면 후보 [커뮤니티 의견, 검증 필요]

| 장면 | 출처 | 연결 절 |
|---|---|---|
| CLAUDE.md에 "MANDATORY"라고 써도 문서화 요구·테스트 절차를 건너뜀. "rules가 아니라 recommendations라고 불러야" | claude-code #2544 (2025-06-24, 댓글 34) | §09, §10 |
| 지시 파일을 읽는지 확인하려고 에이전트에게 "Mr Tinkleberry"라고 부르게 함 | HN 46098838 nico | §10 |
| ADR이 낡아 에이전트가 낡은 가정을 근거로 기이한 코드를 씀. "doc rot, but now the docs are blindly obeyed" | HN 50227041 varyherb | §08, §12 |
| 버튼 하나 추가에 30개 파일 변경, 실제 코드는 20줄 미만 | spec-kit #1174 | §11, §14 |
| Spec-Kit으로 몇 시간 스펙을 다듬은 뒤 나온 코드가 "it hadn't built the right thing" | HN 45935763 thomascountz | §01, §07 |
| 사소한 리팩터링 중 sqlite 코드가 전부 MariaDB로 바뀜 | HN 47034087 avhception | §04, §10 |
| PRD엔 "주문건", 코드엔 `overtime_order` — "클로드가 실수한 게 아니라 제가 기획을 명확하게 안 했어요" | GPTers 제이리 (약 3개월 전 게시) | §02, §05 |
| 검증 테스트를 우회하려고 "계산값"을 "보고값"으로 바꿔치기, 몇 시간과 1M+ 토큰 소모 | r/AI_Agents 1subxv6 (미러 스냅샷 2026-04-25) | §06, §10 |
| 테스트 52개 전부 통과, 그런데 "내가 코드를 세세히 모른다" | velog sukhee | §03, §09 |
| 환불은 LLM이 판단할 문제가 아니라 결정론적 업무 규칙 | HN 47135917 vincentvandeth | §04, §06 |
| 자칭 Claude Code 개발자: "plan mode has always been a prompt" | HN 49840054 bcherny (소속 주장 미확인) | §02, §10 |
| 상시 에이전트의 작업 간 handoff가 의도를 잃는다 | HN 50229493 slurpyb (dots) | §10, §12 |
| 에이전트가 프로덕션 DB를 지우고 받은 안전 규칙을 전부 어겼다고 스스로 열거 | HN 47911524 | §09 |
| 한국 velog 대표 서사: "스펙만으로는 안 됐고 테스트를 붙이자 됐다"(jaemin_ve) / "반복 채팅을 문서로 옮겼다"(namyeji, fcwj24) / "만능 개발자로 쓰려다 통합·QC 책임이 돌아왔다"(code_able) | velog | §03, §06, §10 |

---

## 5. 논쟁점·상충 관점

### 논쟁 A: 스펙 주도 개발은 "마크다운 속의 워터폴"인가? (HN 45935763, 2025-11-15, 225점·191댓글)
- **관점 A — 워터폴이다 / 스펙 자체가 문제다:** laserlight "The detailed spec is exactly the problem with the waterfall development. The spec presumes that it is the solution" · constantcrying(스펙 조작이 극도로 복잡해짐) · zvr "I find writing specs much harder than writing code" · beders "There is only one source of truth and that is the source code." · _pdp_ "you can't spec out something you have no clue how to build" · fl0ki "There is always more detail in implementations than can be specified by any less than the code itself" · pipes "it introduces an unreliable compiler" · Böckeler·Thoughtworks·Scott Logic(3.C).
- **관점 B — 기능 단위 스펙은 워터폴이 아니다:** 4ndrewl 워터폴의 문제는 "a) the mulyi-year lead time ... b) no (cheap) way to iterate". "Neither of these are a problem with SDD." · yoz-y "It's a bit funny to see people describe a spec written in days (hours) and iterations lasting multiple weeks as "waterfall"." · canterburry "My iteration takes 8 hours." · podgorniy 스펙은 "a context entrypoint for LLMs" · ReptileMan "4 weeks of frantic developments save two hours of calmly thinking about the task."
- **같은 스레드 안의 정반대 경험:** macrolime "SDD is actually what you need ... above around 100 000 lines of code." ↔ ErrantX "larger apps built using SDD steadily get harder to extend."
- **메타 비판 (책에 실을 가치):** sgt101 "Opinions about "what works" being pushed as fact. No evidence, no attempt to create evidence".
- **원전의 답:** §01 "폭포수 절차가 아닙니다", §07 위험 기반 Design Ready, §11 위험에 맞춘 양.

### 논쟁 B: 플랜 모드는 아직 필요한가? (HN 49840054 "Plan mode is dead", 2026-09-25; 원 글 본문 미확인)
- **관점 A — 필요 없다:** bcherny(자칭 "[I work on Claude Code]", 미확인) "plan mode was useful, and is no longer useful. In Claude Code, all plan mode does is add a little reminder to every user message ... plan mode has always been a prompt — it has never changed the toolset because doing so would break the prompt cache" / "With Opus 5.5, I feel Opus has gotten to that point too." · b0rtb0rt "“discuss your plan with me before implementing anything” theres your plan mode".
- **관점 B — 필요하다:** dbbk "they want to take away the main feature that lets them be an active collaborator" · dsign "I need to keep a mental view of the system." · loveparade 계획을 거의 안 읽지만 "it forces models to gather as much context as possible before implementing" · OutOfHere(C-휴리스틱8) Codex 플랜 모드로 스펙의 심각한 문제를 찾을 때까지 반복.
- **관점 C — "모드"는 필요 없지만 "계획 문서"는 필요하다:** txhwind "The planning tool built in Codex or Claude Code is not persisted, version-controlled, nor well accessible. ... That document mostly serves a historical purpose like ADR" · tamimio, jfaat.
- **사실 충돌 주의:** bcherny의 "plan mode는 툴셋을 바꾸지 않는 프롬프트"와 공식 문서 검색 요약(W-B12) "플랜 모드에서 Claude는 ... 소스를 편집하지 않는다"는 직접 모순은 아니다(편집하지 않는 동작을 프롬프트로 구현할 수도 있다). 그러나 구현 방식은 확인하지 않았다. **"플랜 모드는 그냥 프롬프트다"를 사실로 쓰지 말 것.**
- **책에 주는 시사점:** 도구 기능(plan mode)과 설계 산출물(plan/, spec/)을 구분하라(원전 §02).

### 논쟁 C: ADR·문서를 에이전트에게 주면 좋아지는가, 나빠지는가? (HN 50227041, 47938417)
- **관점 A — 나빠질 수 있다:** varyherb(doc rot이 맹목적으로 복종됨, "I'm still unsure what to recommend instead, especially in a collaborative setting.") · themafia "This is coping behavior." · stbenjam "I haven't yet seen much evidence that this level of documentation meaningfully improves an agent's performance and that it just doesn't rot over time." · 연구 P-21·P-27.
- **관점 B — 유지 규율이 있으면 좋아진다:** azeirah(append-only log) · gregwebs(mattpocock/skills로 ADR 생성, CONTRIBUTING.md·CODING_STANDARDS.md와 함께) · mcapodici "check that docs are consistent across the board after doing so".
- **관점 C — 에이전트 전용 문서는 만들지 마라:** kkapelon "Any well-maintained project should already have a CONTRIBUTING.md" · rmnclmnt · candiddevmike "Write readmes for humans, not LLMs." · foobarbecue.
- **원전의 답:** §08 Draft → Accepted → Superseded + "결정이 바뀌면 새 기록" = azeirah의 "유지 규율".

### 논쟁 D: AI가 지시 파일을 써도 되는가?
- **관점 A — 맡겨라:** astrostl "I have Claude itself write CLAUDE.md" · philipp-gayret `/init` · chickensong "The agent should know how to write a good file." · OpenAI 하네스 사례(W-B7)의 "the initial AGENTS.md ... was itself written by Codex" [원문 재대조 필요].
- **관점 B — 사람이 써야 한다:** prodigycorp "LLMs are generally bad at writing non-noisy prompts and instructions. It's better to have it write instructions post hoc." · fcwj24(LLM 생성 지시는 "일반적이고 추상적인 문장이 대부분") · foobarbecue "it'll just be more slop" · **[논문] P-17: 개발자 작성 파일이 LLM 생성 파일보다 평균 7%p 높음(p=0.038), LLM 생성 파일의 95~100%가 (도움 안 되는) 개요 포함.**
- **원전 연결:** §10 "AI가 제안한 것을 근거 없이 확정하지 않는다" + §12 owner·status 메타데이터를 지시 파일에도.

### 논쟁 E: 컨텍스트 파일은 효과가 있는가 — 연구끼리도 갈린다
- **관점 A — 정확도 효과 없음/비용 증가:** P-17, P-19.
- **관점 B — 효율 향상:** P-18(실행 시간 −28.64%, 출력 토큰 −16.58%).
- **관점 C — 프로젝트마다 갈림:** P-10 Arabat(오른 곳 27.7% vs 내린 곳 26.35%).
- 결론이 갈리는 이유 후보: 과제 표본·측정 지표 차이, 에이전트별 난이도 경계 차이(P-19, ρ=0.75). **책의 착지: "컨텍스트 파일의 효과는 당신 저장소에서 측정해서 확인하라."** 커뮤니티 C-휴리스틱1(pamelafox의 되돌리고 다시 돌려 보기)이 바로 그 방법이다.

### 논쟁 F: 지시 파일 크기·위치는 준수율에 영향을 주는가
- **관점 A — 준다:** W-B2 공식 문서 "Longer files consume more context and reduce adherence." · P-39 Lost in the Middle(정보가 중간에 있으면 성능 하락, **2023년 모델 기준**) · 커뮤니티 nico(무관한 내용이 많을수록 무시됨).
- **관점 B — 검출 가능한 효과 없음:** P-22 McMillan(파일 크기·지시 위치·구조·모순 모두 효과 없음, 세션 내부 함수 생성이 가장 큰 효과) [프리프린트·단독 저자] · P-20(규칙 0~50개에서 통과율 안정).
- 책에서는 "모든 문서를 다 넣으면 오히려 묻힐 수 있다"는 직관 수준으로만 쓰고, 최신 모델에서 효과 크기를 단정하지 않는다(논문 리서처 권고).

### 논쟁 G: 생산성 — 빨라지는가 느려지는가
- **관점 A — 느려진다/체감과 다르다:** P-1 METR(+19% 완료 시간), Uplevel(버그율 41% 증가 [2차]), DORA 2024(안정성 −7.2% [2차]).
- **관점 B — 빨라진다:** P-2(−21% 시간), P-3(+26.08% 과제 수), P-4(55.8%), P-5 1단계(30.7%), METR 후속(복귀 −18%, 단 CI가 0 포함), DORA 2025(80%+ 생산성 향상 인식).
- **관점 C — 속도는 일시적, 품질 부채는 지속:** P-6, P-7.
- **착지:** 생산성은 측정 단위(과제 수 vs 과제 시간 vs 품질)와 맥락(그린필드·사내 표준 과제 vs 오래된 대형 저장소)에 따라 결론이 갈린다.

### 논쟁 H: 교차 모델 리뷰는 독립 검증인가 (3.E 참조)
- **관점 A — 다른 모델이 놓친 것을 잡는다:** C-휴리스틱6 다수 경험담.
- **관점 B — 상관된 오류 때문에 독립이 아니다:** P-35·36·37. 방향에 따라 역효과라는 미확인 초록 인용(mil22).

---

## 6. 실무 적용 팁 (현장 노하우)

각 항목은 근거 출처를 함께 적었다. [커뮤니티] 항목은 의견이다.

1. **지시 파일에는 에이전트가 실제로 실패한 것만 넣고, 넣은 뒤에는 되돌려 다시 돌려 본다.** [커뮤니티] pamelafox·eknkc(C-휴리스틱1), [웹] W-B11 "Add detail when your agent makes mistakes", W-B5 "same mistake twice → retrospective → update AGENTS.md". 금지만 쓰지 말고 대안을 함께 쓴다(fcwj24). 자동 개선 후보도 "반드시 사람이 검토하고 승인해야 문서에 반영되게 해야함"(fcwj24).
2. **지시 파일은 목차, 세부는 별도 문서.** [커뮤니티] vunderba "Table-of-Contents approach", The_Memening "it should be an Index", [웹] W-B7 [2차], W-B2 200줄.
3. **코드에서 알 수 있는 것은 쓰지 않는다.** [웹] W-B1 "Only write down what Claude can't find by reading the repo"; 레포에 없는 것 = "A decision your team made in a meeting / A deploy process that lives in one person's head / The environment variable your integration tests need". W-B2 `/doctor` 제안, W-D2 "LLM의 기본 지식은 제외", [논문] P-17 저장소 개요는 도움 안 됨.
4. **예외가 없어야 하는 규칙은 훅·deny·린트·테스트로.** [웹] W-B1, [커뮤니티] mkw5053 "types -> lint rules -> tests -> md", Garlef(에러 메시지에 고치는 법을 담은 린트 규칙), [논문] P-22 ContextCov. 단 "Hooks' hell" 경고(Milofax).
5. **금지형으로 쓴다.** [논문] P-20(무작위 규칙 효과 단서와 함께), [웹] W-B11 "Never commit secrets", [원전] §10 프롬프트 4 금지.
6. **낡은 지시와 코드가 충돌할 때의 우선순위를 명시한다.** [논문] P-21 "기존 코드를 우선하라" 한 문장으로 4.2% → 91.4% [프리프린트]. 원전 §02 원본 원칙과 결합: 어느 쪽이 원본인지 지시 파일에 적는다 (책의 해석).
7. **지시에 근거를 남긴다.** [논문] P-22 Chakrabarti(근거 없는 지시는 삭제가 위험해져 쌓인다) [프리프린트·단독 저자], [원전] §08 ADR.
8. **계획은 대화가 아니라 파일로.** [커뮤니티] simonw spec.md, ozgung STATUS.md(Claude Code ↔ Codex 전환), txhwind, [웹] W-B1 SPEC.md + 새 세션, W-B6 ExecPlan. 단, 커뮤니티의 plan.md는 대부분 "작업 순서"만 담고 domain 규칙·미결정·검증 증거를 분리하지 않는다 — 책이 메울 틈(커뮤니티 리서처).
9. **질문받기로 시작한다.** [웹] W-E1 "Ask me one question at a time ...", W-B1 "Interview me until you could write the spec", [커뮤니티] jrexilius·rcarmo, [논문] P-24 상호작용 최대 74%. 단 질문의 질이 낮을 수 있다(joegibbs), 추론을 늘려도 모호성 식별은 거의 개선되지 않는다(P-25 ClarifyCodeBench [프리프린트]) → 미결정 목록은 사람이 쓴다.
10. **수용 기준을 곧바로 테스트로, 테스트 먼저.** [커뮤니티] jaemin_ve, canterburry "A spec is not a prompt.", [논문] P-28·29. 단 테스트도 공격 대상이 된다(C-패턴3) → 테스트 삭제·우회 금지를 금지 목록에, 검증 권한은 에이전트 밖으로.
11. **증거를 요구한다.** [웹] W-B1 "the command it ran and its output, or the screenshot", [원전] §06 VAL-CAN-01, §10 프롬프트 4 보고 항목.
12. **작게 끊고 세션을 재시작한다.** [커뮤니티] sermakarevich "You can restart the session after every step ... since all requirements are materialized in specs.", [웹] W-B5 서브에이전트로 탐색·테스트·분류 분리. 원전은 가로 태스크가 아니라 수직 기능으로 자른다.
13. **자동화·상시 에이전트에는 읽기 전용 자격 증명과 사람 승인 지점.** [커뮤니티] OliverGuy, mike_hearn, guluarte. [웹] W-A2 dots Custom Rules 4행동, W-B11 3단 경계, [원전] §10 IMPLEMENTER "권한 확대 시 중단".
14. **Hermes 기억 홈을 두 에이전트가 공유하지 않는다.** [웹] W-A1 공식 경고 [원문 직접 확인].
15. **Codex와 Claude Code를 병행하면 지시 파일 원본을 하나로.** 2026-10 기준 Claude Code가 AGENTS.md를 읽는다(CLAUDE.md가 없을 때). 둘 다 있으면 CLAUDE.md만 읽으므로, CLAUDE.md에서 AGENTS.md를 임포트하거나 하나만 둔다(W-B2). Codex는 디렉터리마다 1개·32 KiB(W-B4).
16. **결정의 "왜"는 정제해서 PR 옆에.** [커뮤니티] rfw300, esafak, bcherny(artifact를 PR에 첨부, 소속 미확인), hakanderyal(devlog id).
17. **AI 답은 신입의 제안처럼.** [웹] W-D3 컬리.
18. **교차 모델 리뷰는 누락 탐지로만, 승인으로 쓰지 않는다.** [커뮤니티] C-휴리스틱6 + [논문] P-35~37 + [원전] §07.
19. **고득점 상호작용 패턴으로 이해를 지킨다.** [논문] P-51 "생성 후 이해, 코드+설명 혼합, 개념 질문" [프리프린트]. [커뮤니티] sukhee의 "A와 B 중 어떤 게 나은가?", "이 설계의 한계는?" 질문법.
20. **"버전이 바뀌면 지시를 다시 본다."** [커뮤니티] HN 49376287 원문 글 "a meaningful percentage of my system prompt is now actively making things worse—instructions written for a model that no longer exists ... But I can't tell which lines those are" / JasonSage. → 원전 §12 updated·owner 메타데이터를 지시 파일에도.

---

## 7. 단정 금지 목록 — 저술가는 아래를 hedge 없이 사실로 쓰지 않는다

| # | 주장 | 이유 / 써도 되는 표현 | 출처 |
|---|---|---|---|
| 1 | "AI를 쓰면 개발자가 19% 느려진다" | 2025년 초 특정 조건(숙련 OSS 개발자 16명, 자기 저장소, Claude 3.5/3.7 시대)의 결과. 후속(2026-02)은 CI가 0을 포함하고 METR 스스로 "only very weak evidence". → "2025년 초 한 RCT에서는 완료 시간이 19% 늘었다" | P-1 |
| 2 | METR "체감 +20% / 실측 −19%" 식 부호 표기 | 완료 시간 기준과 속도 기준이 섞이기 쉽다. 완료 시간 기준으로 통일 | P-1 |
| 3 | "AI로 55% 빨라진다" | 단일·소규모 그린필드 과제(2023). 맥락 동반 | P-4 |
| 4 | AGENTS.md 연구의 "성공률 하락·비용 20%+ 증가", "개발자 +4% / LLM −3%" | 커뮤니티 댓글 인용 수치. papers.md 본문 확인 수치(−0.5%/−2%/+2.4%, 7%p, 약 20%·23%)를 쓴다. 또한 유의하지 않은 결과가 대부분 | C-휴리스틱1 vs P-17 |
| 5 | "지시 파일과 코드가 충돌하면 에이전트는 90.1% 지시를 따른다" | 2026-10-22 게시 프리프린트, 재현 없음, Python 40개 프로젝트 조건. → "최근 보고에 따르면" | P-21 |
| 6 | "금지형 규칙만 효과가 있다" | 무작위 규칙도 +13.8%p라는 결과와 함께 제시. 프리프린트 | P-20 |
| 7 | CLAUDE.md 보안 규칙 4.4%, ContextCov 88.3%, McMillan "효과 없음", Chakrabarti +226% | 모두 프리프린트·단독 저자 | P-22 |
| 8 | 교차 모델 리뷰 "71.6%→89.7%, 91.4%→82.8%" | HN 댓글이 인용한 초록, 원 논문 미대조, 논문 리서치에 없음 → 쓰지 않거나 "확인되지 않은 보고"로만 | C-휴리스틱6 |
| 9 | "명령 150~200개까지 일관 준수" | HN 댓글(andai)이 원문 글을 인용, 미확인 | C-수집 한계 |
| 10 | fcwj24의 "-3%, +8~15%" | 출처 미표기 | C-휴리스틱1 |
| 11 | Kent Beck "AI 에이전트가 테스트를 지운다" 직접 인용 | 에피소드 소개문 기준, 녹취록 미확인. → "Pragmatic Engineer 에피소드 소개에 따르면". 블로그 W-E2의 "disabling or deleting tests" 경고 신호는 [요약 경유]로 인용 가능 | C-패턴3, W-E2 |
| 12 | "We used AI to code 2x faster. Then spent 3x more time fixing bugs." | velog 글이 인용, 원 출처 미확인 | C-한국 |
| 13 | OpenAI 하네스: "100만 줄, PR 약 1,500건, 엔지니어 3명", "AGENTS.md도 Codex가 썼다" | 본문 403, 검색 스니펫 수준 → [원문 재대조 필요]. "~100줄 AGENTS.md"는 Viblo 단독 [미확인] | W-B7 |
| 14 | Anthropic 팀 "R&D 시간 80% 단축", "Vim 모드 코드 70%" | [2차, 미확인]. PDF 대조 전 금지 | W-E5 |
| 15 | Anthropic 2026 Trends Report "60% of work" 등, 발행일 | 본문 미열람, 날짜 1월/4월 엇갈림 | W-E6 |
| 16 | Stack Overflow 2026 "Codex 30%·Cursor 26%·Antigravity 16%" | 달레 블로그 단독 | W-G2 |
| 17 | "개발자의 AI 신뢰가 31%에서 87%로 늘었다" | 질문 보기 변경 탓이라는 경고(달레). → "검증을 전제로 쓰는 방식이 자리 잡았다"가 더 정확하다는 해석 동반 | W-G2 |
| 18 | Stack Overflow 2026-04 펄스 "에이전트 사용 59%, Claude Code 41% → 55%" | [2차, 원문 재대조 필요] | W-G2 |
| 19 | JetBrains 2026 조사 기간 | 4~5월 vs 5~7월 엇갈림. JetBrains 원문 403 | W-G4 |
| 20 | DORA 2025 "14% 증가"를 "14%p"로 단정 | 리서처가 포인트로 "해석"했다. 원문 표현은 "14%" | W-G3 |
| 21 | DORA AI Capabilities Model 7개 역량 명칭 | 정확한 명칭 미확인 | W-G3 |
| 22 | DORA 2024 "도입 25% 증가당 처리량 −1.5%, 안정성 −7.2%" | "25% 증가당"은 RedMonk 재진술일 수 있음 | P-회색 |
| 23 | Claude Code AGENTS.md 지원 시작 버전 "2.1.277" | velog 제목 단독. "2026-10 공식 문서 기준 지원"까지만 | C-논쟁E |
| 24 | Claude Code 플랜 모드 세부 조작법·"플랜 모드는 그냥 프롬프트" | 검색 요약 경유(캐시 약 105일) / 자칭 개발자 발언 | W-B12, C-논쟁B |
| 25 | "Claude Code 훅 이벤트 27개 vs Codex 5개" | 비공식 저장소 주장 | W-B5 |
| 26 | Codex 플랜 모드 토글·스킬 위치·훅 파일 세부 | [2차] | W-B5 |
| 27 | dots의 "4,000개 이상 앱 연결", "GPT-6.1 Astra 업그레이드 보류", 가격, 기억 열람·삭제 불가, "SSL 가로채기" | [미확인]/[2차]/커뮤니티 주장 | W-A2, C-도구 |
| 28 | Hermes·dots로 설계 문서를 운용하는 것이 업계 관행이라는 서술 | 공개 실천 사례 없음. 저자 제안으로 명시 | C-도구 |
| 29 | Hermes 출시일 "2025-07" 또는 "2026-02" | 1차 사실은 저장소 생성 2025-07-22, 첫 태그 릴리스 2026-03-12. 중간 릴리스명·날짜는 [2차] | W-A1 |
| 30 | Hermes 표절 논란 | 내용 미확인 | C-도구 |
| 31 | Kiro GA "2026-03/05" | 공식은 2025-11-17 | W-C3 |
| 32 | Spec Kit 명령을 `/speckit.specify`나 clarify·analyze 단계로 현행처럼 서술 | 구버전. v1.2 기준 하이픈·converge | W-C2, W-D4 |
| 33 | Thoughtworks Radar가 현재도 SDD를 Assess에 둔다 | Vol.33(2025-11-05) 기준, 이후 링 변화 미확인 | W-C5 |
| 34 | "Spec Kit 기능 하나 = 파일 8개, 약 1,300줄" | Scott Logic 원문 미열람, 2차 경유 | W-C9 |
| 35 | IETF 초안이 현재(-08) 다른 페이로드에 422를 요구 | -07 기준, -08 변경 여부 미확인, 원문 문장 재대조 필요 | W-F7 |
| 36 | OpenAPI 3.2.0 날짜를 1차 확인된 사실처럼 | 2차 교차 확인 | W-F10 |
| 37 | "knowledge vaporization"을 Jansen & Bosch 원문 인용으로 | 원문 존재 미확인 → "흔히 그렇게 부른다" | P-40 |
| 38 | ADR "63%가 처음부터 accepted" | ICSA 2026, 2차 확인, 저자·DOI 미확인 | P-42 |
| 39 | Mäder & Egyed "24% 빠르고 50% 더 정확" → "에이전트도 마찬가지" | 수치 [2차]. 에이전트 적용은 책의 추론임을 밝힌다 | P-44 |
| 40 | Pearce "AI 코드 40%가 취약" | 2021년 모델 기준 | P-50 |
| 41 | Macke & Doyle "틀린 문서가 없는 문서보다 해롭다"를 현행 모델 결론으로 | 2023~2024 세대 모델 | P-27 |
| 42 | Lost in the Middle 위치 효과를 현행 모델에 그대로 | 2023년 모델, 2026 McMillan은 효과 미검출 | P-39 |
| 43 | MetaGPT "역할을 늘릴수록 좋아진다" | 단조 증가 아님(+PM·Project Manager 2.0) | P-54 |
| 44 | Shen & Tamkin "AI를 쓰면 실력이 17% 떨어진다" 일반화 | 52명, 낯선 라이브러리 학습 과제, 프리프린트. 고득점 패턴도 함께 | P-51 |
| 45 | Kosmyna EEG 연구를 코딩 근거로 | 에세이 쓰기 연구, 프리프린트 | P-52 |
| 46 | Perry 외 참가자 수, Cui 외 경력별 효과, Mathews & Nagappan %p | 미확인 | P-49, P-3, P-28 |
| 47 | "에이전트가 비밀을 유출한다" | P-10에서 유출된 실제 비밀의 67.6%는 사람이 넣었다 | P-10 |
| 48 | Octoverse 커밋 수 | "nearly 1 billion"과 "more than 986M" 혼재 | W-G5 |
| 49 | LY 블로그 날짜 2026-01-29, 카카오페이 if(kakao) 기반 | 추정 | W-D5, W-D4 |
| 50 | 커뮤니티 닉네임의 소속 주장(bcherny "I work on Claude Code" 등) | 자기 주장, 미확인 | C 전체 |
| 51 | 원전의 예시 수치(p95 ≤ 500ms, 5xx ≤ 0.5%, 10만 건, 초당 20건, 15분, 10분 경보, 첫 주 5일 일정)를 권장 기본값으로 | 원전이 "형식을 보여 주기 위한 예시이며 권장 기본값이 아닙니다", "조정 가능한 예시"라고 명시 | [원전] §04, §11 |
| 52 | 원전 §06의 HTTP 상태 코드·정책(타인 예약 404 등)을 표준처럼 | "HTTP 상태 코드는 이 예제의 선택입니다", "예시상 404" | [원전] §06 |
| 53 | web.md `>` 인용 전반 | 요약 모델 경유. 본문 직접 인용 전 원 URL 재대조 | W 전체 |

---

## 8. 참고문헌

형식: 저자. 제목. 발행처/URL/DOI, 날짜. (참조 ID)

### 8.1 원전
- (저자 미기재). 신규 프로젝트 설계와 AI 개발 통제 가이드 — 한국어판 v1.0. `research/primary/ai-project-design-guidelines-ko.md`, 2026-10.

### 8.2 웹 — 도구·공식 문서
- Nous Research. hermes-agent (README, docs: context-files, memory, bundled skills). https://github.com/NousResearch/hermes-agent · https://hermes-agent.nousresearch.com/docs/, v0.22.5 2026-10-23. (W-A1)
- Lucas Ropek. OpenAI launches dots, its bubbly agentic avatar. TechCrunch, https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/, 2026-09-29. (W-A2)
- Matt Crabtree. OpenAI dots. DataCamp, https://www.datacamp.com/blog/openai-dots, 2026-09-29. (W-A2)
- OpenAI. Getting started with your dot. https://help.openai.com/en/articles/20001530-getting-started-with-your-dot (403). / How we build safety, security and privacy into dots. https://openai.com/index/how-we-build-safety-security-and-privacy-into-dots/ (403). (W-A2)
- npm·GitHub 조회: `@anthropic-ai/claude-code` 2.1.312, `@openai/codex` 0.165.0, github/spec-kit v1.2.4, Fission-AI/OpenSpec v1.15.0, bmad-code-org/BMAD-METHOD v6.12.4, buildermethods/agent-os v3.0.0, 2026-10-28 조회. (W-A3)
- Anthropic. Best practices for Claude Code. https://code.claude.com/docs/en/best-practices, 날짜 없음(2026-10 조회). (W-B1)
- Anthropic. How Claude remembers your project. https://code.claude.com/docs/en/memory, 날짜 없음(2026-10 조회). (W-B2)
- Agentic AI Foundation. AGENTS.md. https://agents.md/, 날짜 없음(2026-10 조회). (W-B3)
- OpenAI. AGENTS.md (Codex agent configuration). https://learn.chatgpt.com/docs/agent-configuration/agents-md, 날짜 없음(2026-10 조회). (W-B4)
- OpenAI. Codex best practices. https://learn.chatgpt.com/guides/best-practices, 날짜 없음(2026-10 조회). (W-B5)
- OpenAI. Using PLANS.md for multi-hour problem solving. https://developers.openai.com/cookbook/articles/codex_exec_plans, 날짜 없음(archived). (W-B6)
- Ryan Lopopolo. Harness engineering: leveraging Codex in an agent-first world. OpenAI, https://openai.com/index/harness-engineering/, 2026-02-11 (403). (W-B7)
- Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield. Effective context engineering for AI agents. Anthropic, https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents, 2025-09-29. (W-B8)
- Birgitta Böckeler. Context Engineering for Coding Agents. martinfowler.com, https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html, 2026-02-05. (W-B9)
- Agent Skills. https://agentskills.io/, 날짜 없음(2026-10 조회). (W-B10)
- Matt Nigh. How to write a great agents.md: Lessons from over 2,500 repositories. GitHub Blog, https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/, 2025-11-19 (2025-11-25 갱신). (W-B11)
- Anthropic. Permission modes / Common workflows. https://code.claude.com/docs/en/permission-modes · https://code.claude.com/docs/en/common-workflows, 2026 (검색 요약 경유). (W-B12)

### 8.3 웹 — SDD 도구·비판
- Den Delimarsky. Spec-driven development with AI: Get started with a new open source toolkit. GitHub Blog, https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/, 2025-09-02. (W-C1)
- GitHub. spec-kit. https://github.com/github/spec-kit, v1.2.4 2026-10-27. (W-C2)
- AWS Kiro. Specs / Feature specs / Steering / General availability. https://kiro.dev/docs/specs/ (2026-10-15 갱신) · https://kiro.dev/docs/specs/feature-specs/ (2026-08-04) · https://kiro.dev/docs/steering/ (2026-10-21) · https://kiro.dev/blog/general-availability/ (2025-11-17). (W-C3)
- Birgitta Böckeler. Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl. martinfowler.com, https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html, 2025-10-15. (W-C4)
- Thoughtworks. Technology Radar Vol. 33 — Spec-driven development (Assess). https://www.thoughtworks.com/radar/techniques/spec-driven-development, 2025-11-05. (W-C5)
- Fission-AI. OpenSpec. https://github.com/Fission-AI/OpenSpec · https://openspec.dev, v1.15.0 2026-10-24. (W-C6)
- BMad Code. BMAD-METHOD. https://github.com/bmad-code-org/BMAD-METHOD · https://docs.bmad-method.org, v6.12.4 2026-10-14. (W-C7)
- Builder Methods. agent-os. https://github.com/buildermethods/agent-os, v3.0.0 2026-01-20. / Tessl. https://docs.tessl.io. (W-C8)
- Scott Logic. Putting Spec Kit Through Its Paces: Radical Idea or Reinvented Waterfall? 2025-11-26 (원문 미열람). / Conffab. Your Spec Driven Workflow Is Just Waterfall With Extra Steps. 2025-12-09. / GeekNews. https://news.hada.io/topic?id=24400, 2025-11-17. (W-C9)

### 8.4 웹 — 국내 엔지니어링 블로그
- 김용성. Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기. 토스테크, https://toss.tech/article/harness-for-team-productivity, 2026-02-26. (W-D1)
- 이재홍. 하네스 엔지니어링(harness engineering)으로 팀 맞춤형 AI 환경 구축하기. 우아한형제들 기술블로그, https://techblog.woowahan.com/26177/, 2026-04-17. (W-D2)
- 이준환. OMS에서 Claude AI를 활용하여 변화된 업무 방식. 컬리 기술 블로그, https://helloworld.kurly.com/blog/oms-claude-ai-workflow/, 2025-12-24. (W-D3)
- wayne.cai. SDD (spec-kit) 에이전트 코딩 실전기. 카카오페이 기술 블로그, https://tech.kakaopay.com/post/ifkakao-agentic-coding/, 2026-03-13. (W-D4)
- Hirano Keisuke. ODW #4: 코파일럿에서 파일럿으로, 에이전틱 코딩으로 구현부터 PR까지 자동화. LY Corporation 기술 블로그, https://techblog.lycorp.co.jp/ko/from-copilot-to-pilot-agentic-coding-implementation-to-pr-automation, 날짜 없음(2026-01-29 추정). / Claude Code Action: 조직 전반의 코드 품질을 지키는 AI 코드 리뷰 플랫폼화. https://techblog.lycorp.co.jp/ko/building-ai-code-review-platform-with-claude-code-action. (W-D5)
- benedict.lee. Beyond Vibe Coding to Agentic Coding. 카카오테크, https://tech.kakao.com/posts/711 (본문 미추출). / 카카오테크. 생산성 혁신의 실험: AI 마일리지 프로그램. https://tech.kakao.com/posts/762. / 홍영민. 배달의민족 전자계약서 화면 개편기. 우아한형제들, 2026-09-15 [미확인]. / 달레. 스펙 주도 개발. https://daleseo.com/spec-driven-development/ (미열람). / 달레. Stack Overflow 2026 설문. https://daleseo.com/stack-overflow-survey-2026/, 2026-10-11. (W-D6, W-G2)

### 8.5 웹 — 실무자 에세이·업계 보고서
- Harper Reed. My LLM codegen workflow atm. https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/, 2025-02-16. (W-E1)
- Kent Beck. Augmented Coding: Beyond the Vibes. https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes, 2025-06-25. (W-E2)
- Simon Willison. Vibe engineering. https://simonwillison.net/2025/Oct/7/vibe-engineering/, 2025-10-07. (W-E3)
- Addy Osmani. How to write a good spec for AI agents. https://addyosmani.com/blog/good-spec/, 2026-01-13. (W-E4)
- Anthropic. How Anthropic teams use Claude Code. https://claude.com/blog/how-anthropic-teams-use-claude-code, 2025-07-24. (W-E5)
- Anthropic. 2026 Agentic Coding Trends Report. https://resources.anthropic.com/2026-agentic-coding-trends-report, 2026-01-21 [미확인]. (W-E6)
- Stack Overflow. 2025 Developer Survey — AI. https://survey.stackoverflow.co/2025/ai, 2025-07-29. (W-G1)
- Ryan Donovan. The results of the 2026 Developer Survey are here. Stack Overflow Blog, https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/, 2026-10-06 · https://survey.stackoverflow.co/2026/ai. (W-G2)
- Ryan J. Salva. DORA 2025 report. Google, https://blog.google/technology/developers/dora-report-2025/, 2025-09-23 · AI Capabilities Model https://dora.dev/ai/capabilities-model/report (2025-11-25 갱신). (W-G3)
- JetBrains. State of Developer Ecosystem 2025. https://blog.jetbrains.com/research/2025/10/state-of-developer-ecosystem-2025/, 2025-10-15. / AI coding agent adoption 2026. https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/ (403). / Janet Swift. JetBrains reveals widespread adoption of AI coding agents. i-programmer, https://www.i-programmer.info/news/99-professional/19118-jetbrains-reveals-widespread-adoption-of-ai-coding-agents-.html, 2026-09-02. (W-G4)
- GitHub Staff. Octoverse 2025. https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-TypeScript-to-1/, 2025-10-28 (2026-02-28 갱신). (W-G5)

### 8.6 웹 — 설계·문서화 고전
- Michael Nygard. Documenting Architecture Decisions. https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions, 2011-11-15. (W-F1)
- ADR GitHub organization. MADR 4.0.0. https://adr.github.io/madr/, 2024-09-17. (W-F2)
- Malte Ubl. Design Docs at Google. https://www.industrialempathy.com/posts/design-docs-at-google/, 2020-07-06. (W-F3)
- Gergely Orosz. Companies Using RFCs or Design Docs and Examples of These. https://blog.pragmaticengineer.com/rfcs-and-design-docs/, 2022-06-21 (2024-02-07 갱신). (W-F4)
- Martin Fowler. GivenWhenThen. https://martinfowler.com/bliki/GivenWhenThen.html, 2013-08-21. (W-F5)
- Brandur Leach. Designing robust and predictable APIs with idempotency. Stripe, https://stripe.com/blog/idempotency, 2017-02-22. / Stripe. Idempotent requests. https://docs.stripe.com/api/idempotent_requests, 2026-10 조회. (W-F6)
- J. Jena, S. Dalal. The Idempotency-Key HTTP Header Field. IETF httpapi WG, https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/, -07 2025-10-15 / -08 2026-10-22. (W-F7)
- Chris Richardson. Pattern: Transactional outbox. https://microservices.io/patterns/data/transactional-outbox.html, 날짜 없음. (W-F8)
- Pact Foundation. Pact docs. https://docs.pact.io/, 2026-10 조회. (W-F9)
- OpenAPI Initiative. OpenAPI Specification 3.2.0. https://spec.openapis.org/oas/v3.2, 2025-09-19. (W-F10)

### 8.7 논문
- Joel Becker, Nate Rush, Elizabeth Barnes, David Rein. Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity. arXiv 2507.09089 / DOI 10.48550/arXiv.2507.09089, 2025-07-12. (P-1) · METR. Uplift update. https://metr.org/blog/2026-02-24-uplift-update/, 2026-02-24.
- Elise Paradis 외. How much does AI impact development speed? An enterprise-based randomized controlled trial. ICSE-SEIP 2025, DOI 10.1109/ICSE-SEIP66354.2025.00060, arXiv 2410.12944. (P-2)
- Kevin Zheyuan Cui, Mert Demirer, Sonia Jaffe, Leon Musolff, Sida Peng, Tobias Salz. The Effects of Generative AI on High-Skilled Work. Management Science, DOI 10.1287/mnsc.2025.00535, 2025. (P-3)
- Sida Peng, Eirini Kalliamvakou, Peter Cihon, Mert Demirer. The Impact of AI on Developer Productivity: Evidence from GitHub Copilot. arXiv 2302.06590, 2023. (P-4)
- Markus Borg 외. Echoes of AI. ICSME 2025 Registered Report, arXiv 2507.00788. (P-5)
- Hao He, Courtney Miller, Shyam Agarwal, Christian Kästner, Bogdan Vasilescu. Speed at the Cost of Quality. MSR 2026, DOI 10.1145/3793302.3793349, arXiv 2511.04427. (P-6)
- Shyam Agarwal, Hao He, Bogdan Vasilescu. AI IDEs or Autonomous Agents? MSR 2026, DOI 10.1145/3793302.3793589, arXiv 2601.13597. (P-7)
- Hao Li, Haoxiang Zhang, Ahmed E. Hassan. The Rise of AI Teammates in SE 3.0 / AIDev. arXiv 2507.15003 (2025) / MSR 2026 arXiv 2602.09185, DOI 10.1145/3793302.3797249. (P-8)
- Miku Watanabe 외. On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub. ACM TOSEM, DOI 10.1145/3798166, arXiv 2509.14745. (P-9)
- A H M Nazmus Sakib, Dipayan Banik, Murtuza Jadliwala. Trust but Verify? KDD 2026 AgenticSE, arXiv 2607.12428. / Kacper Duma 외. These Aren't the Reviews You're Looking For. EASE 2026, arXiv 2605.02273. / Obada Kraishan. Not All Agents Are Equal. arXiv 2609.17598. / Ali Arabat, Mohammed Sayagh. Toward Instructions-as-Code. MSR 2026, DOI 10.1145/3793302.3793601, arXiv 2606.13449. / Sabrina Haque, Sarvesh Ingale, Christoph Csallner. Do Autonomous Agents Contribute Test Code? arXiv 2601.03556. / Shota Sawada 외. To What Extent Does Agent-generated Code Require Maintenance? EASE 2026, arXiv 2605.06464. (P-10)
- You Wang, Michael Pradel, Zhongxin Liu. Are "Solved Issues" in SWE-bench Really Solved Correctly? ICSE 2026, DOI 10.1145/3744916.3764576, arXiv 2503.15223. (P-11)
- Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, Lingming Zhang. Is Your Code Generated by ChatGPT Really Correct? NeurIPS 2023, arXiv 2305.01210. (P-12)
- Carlos E. Jimenez 외. SWE-bench. ICLR 2024, arXiv 2310.06770. / Reem Aleithan 외. SWE-Bench+. arXiv 2410.06992. / Shanchao Liang, Spandan Garg, Roshanak Zilouchian Moghaddam. The SWE-Bench Illusion. arXiv 2506.12286. / Chunqiu Steven Xia 외. Agentless. arXiv 2407.01489. / Xiang Deng 외. SWE-Bench Pro. arXiv 2509.16941 (후속 2609.08149, 2610.24206). (P-13, P-59)
- Worawalan Chatlatanagulchai 외. On the Use of Agentic Coding Manifests. PROFES 2025, DOI 10.1007/978-3-032-12089-2_40, arXiv 2509.14744. (P-14)
- Worawalan Chatlatanagulchai 외. Agent READMEs. ACM TOSEM, DOI 10.1145/3840295, arXiv 2511.12884. (P-15)
- Seyedmoein Mohsenimofidi, Matthias Galster, Christoph Treude, Sebastian Baltes. Context Engineering for AI Agents in Open-Source Software. MSR 2026, DOI 10.1145/3793302.3793350, arXiv 2510.21413. / Matthias Galster 외. Harness Engineering for Agentic AI Coding Tools. arXiv 2602.14690. / Muhammad Auwal Abubakar 외. An Exploratory Study of Agent Plans. ESEM 2026, arXiv 2608.04661. (P-16)
- Thibaud Gloaguen, Niels Mündler-Sasahara, Mark Niklas Müller, Veselin Raychev, Martin Vechev. Evaluating AGENTS.md. arXiv 2602.11988, 2026. (P-17)
- Jai Lal Lulla 외. On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents. arXiv 2601.20404, 2026. (P-18)
- Prakhar Khatri. Do Context Files Help Coding Agents? arXiv 2607.27250, 2026. (P-19)
- Xing Zhang 외. Guardrails Beat Guidance. arXiv 2604.11088, 2026. (P-20)
- Xiaonan Xu, Wenjing Wu. Stale Instruction Files Override the Code in Coding Agents: A One-Sentence Fix. arXiv 2610.30571, 2026-10-22. (P-21)
- Ting Yan. When "Do Not" Is Not Deny. arXiv 2608.23550. / Reshabh K Sharma. ContextCov. arXiv 2603.00822. / Damon McMillan. Instruction Adherence in Coding Agent Configuration Files. arXiv 2605.10039. / Kushal Chakrabarti. Why Does CLAUDE.md Keep Growing? arXiv 2608.11095. / Yupu Wang 외. Package Hallucination Attacks on Coding Agents through Prompt Injection in Rule Files. arXiv 2610.09264. 모두 2026. (P-22)
- Mohammad Amin Zadenoori 외. LLMs for Requirements Engineering: A Systematic Literature Review. arXiv 2509.11446, 2025. / Andreas Vogelsang, Jannik Fischbach. arXiv 2402.13823, 2024. (P-23)
- Sanidhya Vijayvargiya, Xuhui Zhou, Akhila Yerukola, Maarten Sap, Graham Neubig. Ambig-SWE. ICLR 2026, arXiv 2502.13069. (P-24)
- Fangwen Mu 외. ClarifyGPT. arXiv 2310.10996, 2023. / Jie JW Wu, Fatemeh H Fard. HumanEvalComm. ACM TOSEM 2025, DOI 10.1145/3715109. / Zheng Fang 외. ClarifyCodeBench. arXiv 2607.00711, 2026. (P-25)
- Bingyang Wei. Requirements are All You Need. arXiv 2406.10101, 2024. (P-26)
- William Macke, Michael Doyle. Testing the Effect of Code Documentation on LLM Code Understanding. Findings of NAACL 2024, arXiv 2404.03114. (P-27)
- Noble Saji Mathews, Meiyappan Nagappan. Test-Driven Development for Code Generation. ASE 2024, DOI 10.1145/3691620.3695527, arXiv 2402.13521. (P-28)
- Sarah Fakhoury 외. LLM-Based Test-Driven Interactive Code Generation (TiCoder). IEEE TSE 50(9):2254–2268, DOI 10.1109/TSE.2024.3428972, arXiv 2404.10100. (P-29)
- Chuyue Sun, Ying Sheng, Oded Padon, Clark Barrett. Clover. SAIV 2024, arXiv 2310.17807. (P-30)
- Madeline Endres 외. Can LLMs Transform Natural Language Intent into Formal Method Postconditions? FSE 2024, DOI 10.1145/3660791, arXiv 2310.01831. (P-31)
- Joseph Spracklen 외. We Have a Package for You! USENIX Security 2025, arXiv 2406.10279. (P-32)
- Jie Huang 외. Large Language Models Cannot Self-Correct Reasoning Yet. ICLR 2024, arXiv 2310.01798. (P-33)
- Ryo Kamoi 외. When Can LLMs Actually Correct Their Own Mistakes? TACL 12:1417–1440, DOI 10.1162/tacl_a_00713, arXiv 2406.01297. (P-34)
- Elliot Kim, Avi Garg, Kenny Peng, Nikhil Garg. Correlated Errors in Large Language Models. ICML 2025, arXiv 2506.07962. (P-35)
- Shashwat Goel 외. Great Models Think Alike and this Undermines AI Oversight. ICML 2025, arXiv 2502.04313. (P-36)
- Arjun Panickssery, Samuel R. Bowman, Shi Feng. LLM Evaluators Recognize and Favor Their Own Generations. NeurIPS 2024, arXiv 2404.13076. (P-37)
- Toufique Ahmed 외. Can LLMs Replace Manual Annotation of Software Engineering Artifacts? arXiv 2408.05534, 2024. (P-38)
- Nelson F. Liu 외. Lost in the Middle. TACL 2024, DOI 10.1162/tacl_a_00638, arXiv 2307.03172. (P-39)
- Anton Jansen, Jan Bosch. Software Architecture as a Set of Architectural Design Decisions. WICSA 2005. (P-40)
- Jeff Tyree, Art Akerman. Architecture Decisions: Demystifying Architecture. IEEE Software 22(2):19–27, 2005. (P-41)
- Georg Buchgeher 외. Using Architecture Decision Records in Open Source Projects. IEEE Access 11:63725–63740, DOI 10.1109/ACCESS.2023.3287654, 2023. / Enio Garcia de Santana Junior 외. ADR Adoption Impact and Developer Engagement in Open Source. ICSA 2026. (P-42)
- Rudra Dhar, Karthik Vaidhyanathan, Vasudeva Varma. Can LLMs Generate Architectural Design Decisions? ICSA 2024, DOI 10.1109/ICSA59870.2024.00016, arXiv 2403.01709. / Xiyu Zhou 외. Using LLMs in Generating Design Rationale. ACM TOSEM 2025, DOI 10.1145/3785010, arXiv 2504.20781. (P-43)
- Patrick Mäder, Alexander Egyed. Do developers benefit from requirements traceability when evolving and maintaining a software system? Empirical Software Engineering 20(2):413–441, DOI 10.1007/s10664-014-9314-z, 2015. (P-44)
- Orlena C. Z. Gotel, Anthony C. W. Finkelstein. An Analysis of the Requirements Traceability Problem. ICRE 1994, pp. 94–101. / Jin L. C. Guo 외. NLP for Requirements Traceability. arXiv 2405.10845. / Alberto D. Rodriguez 외. Prompts Matter. arXiv 2308.00229. (P-45)
- Emad Aghajani 외. Software Documentation Issues Unveiled. ICSE 2019. (P-46)
- Lisanne Bainbridge. Ironies of Automation. Automatica 19(6):775–779, 1983. (P-47)
- Raja Parasuraman, Dietrich H. Manzey. Complacency and Bias in Human Use of Automation. Human Factors 52(3):381–410, DOI 10.1177/0018720810376055, 2010. (P-48)
- Neil Perry, Megha Srivastava, Deepak Kumar, Dan Boneh. Do Users Write More Insecure Code with AI Assistants? ACM CCS 2023, DOI 10.1145/3576915.3623157, arXiv 2211.03622. (P-49)
- Hammond Pearce 외. Asleep at the Keyboard? IEEE S&P 2022, arXiv 2108.09293. (P-50)
- Judy Hanwen Shen, Alex Tamkin. How AI Impacts Skill Formation. arXiv 2601.20245, 2026. (P-51)
- Hao-Ping (Hank) Lee 외. The Impact of Generative AI on Critical Thinking. CHI 2025, DOI 10.1145/3706598.3713778. / Helena Vasconcelos 외. Explanations Can Reduce Overreliance on AI Systems During Decision-Making. CSCW 2023, DOI 10.1145/3579605. / James Prather 외. The Widening Gap. ICER 2024, DOI 10.1145/3632620.3671116. / Shraddha Barke, Michael B. James, Nadia Polikarpova. Grounded Copilot. OOPSLA 2023, DOI 10.1145/3586030. / Hussein Mozannar 외. Reading Between the Lines. CHI 2024, arXiv 2210.14306. / Ruotong Wang 외. Investigating and Designing for Trust in AI-powered Code Generation Tools. FAccT 2024, DOI 10.1145/3630106.3658984. / Nataliya Kosmyna 외. Your Brain on ChatGPT. arXiv 2506.08872, 2025. (P-52)
- Chen Qian 외. ChatDev. ACL 2024, DOI 10.18653/v1/2024.acl-long.810, arXiv 2307.07924. (P-53)
- Sirui Hong 외. MetaGPT. ICLR 2024, arXiv 2308.00352. (P-54)
- Yihong Dong, Xue Jiang, Zhi Jin, Ge Li. Self-collaboration Code Generation via ChatGPT. ACM TOSEM, DOI 10.1145/3672459, arXiv 2304.07590. (P-55)
- Dong Huang 외. AgentCoder. arXiv 2312.13010, 2023. (P-56)
- Mert Cemri 외. Why Do Multi-Agent LLM Systems Fail? NeurIPS 2025 D&B, arXiv 2503.13657. (P-57)
- Qineng Wang 외. Rethinking the Bounds of LLM Reasoning. ACL 2024, arXiv 2402.18272. (P-58)
- Mingyan Gao 외. Single-agent or Multi-agent Systems? Why Not Both? arXiv 2505.18286, 2025. (P-59)
- Yubin Kim, Ken Gu, Chanwoo Park 외. Towards a Science of Scaling Agent Systems. arXiv 2512.08296, 2025. (P-60)
- Junda He, Christoph Treude, David Lo. LLM-Based Multi-Agent Systems for Software Engineering. ACM TOSEM, DOI 10.1145/3712003, arXiv 2404.04834. (P-보조)
- Deepak Babu Piskala. Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants. arXiv 2602.00180. / Pardis Taghavi, Santosh Bhavani. Spec Kit Agents. arXiv 2604.05278. / Oleg Grynets 외. Specification-Driven Development Benchmark: Security Knowledge Transition. arXiv 2606.00167. / SWE-AGI arXiv 2602.09447 · arXiv 2609.24348 · arXiv 2608.30572. 모두 2026. (P-SDD)
- 회색 문헌: Google DORA 2024 Accelerate State of DevOps · GitClear 2025 AI Copilot Code Quality · Uplevel Data Labs 2024 (모두 [2차]). (P-회색)

### 8.8 커뮤니티 (주요 스레드)
- GitHub anthropics/claude-code #2544 (2025-06-24), #33603 (2026-03-12). https://github.com/anthropics/claude-code/issues/2544 · /33603
- GitHub github/spec-kit #75 (2025-09-08), #620 (2025-09-27), #1174 (2025-11-13). https://github.com/github/spec-kit/issues/
- Hacker News: 46098838 Writing a good Claude.md (2025-11-30) · 49945933 Agents don't need memory, they need documentation (2026-10-03) · 50227041 Show HN: ADRs for AI (2026-10-25) · 49376287 I am morally opposed to updating my Claude.md (2026-08-20) · 47745102 (2026-04-12) · 49847968 Show HN Executor (2026-09-25) · 45935763 Spec-Driven Development: The Waterfall Strikes Back (2025-11-15) · 47034087 Evaluating AGENTS.md (2026-02-16) · 49840054 Plan mode is dead (2026-09-25) · 47135917 Ask HN: controlling AI agents (2026-02-24) · 46492381 (2026-01-04) · 48275853 (2026-05-26) · 49298901 Ask HN: Does a human still review your code? (2026-08-14) · 48413629 Ask HN: AI dev workflow (2026-06-05) · 47938417 A good AGENTS.md is a model upgrade (2026-04-28) · 43094006 Harper Reed 스레드 (2025-02-18) · 43929599 (2025-05-08) · 48150810 Codex to review Claude's code (2026-05-15) · 47800969 (2026-04-16) · 48853334 (2026-07-09) · 49166538 Cross-Model LLM Code Review (2026-08-04) · 47212355 Should the session be part of the commit? (2026-03-02) · 49896604 Dots: Always-on agents (2026-09-29) · 49896565 · 47911524 An AI agent deleted our production database (2026-04-26) · 47197595 Verified SDD (2026-02-28) · 46955747 (2026-02-10) · 49760187 Claude Code now reads AGENTS.md (2026-09-18) · 44957443 AGENTS.md open format (2025-08-20) · 48373851 Hermes Desktop (2026-06-02) · 48455560 (2026-06-09) · 48586005 Migrate from OpenClaw (2026-06-18) · 50084055 dot burned 300K+ tokens (2026-10-14) · 50229493 (2026-10-28) · 49971444 (2026-10-05) · 49897710 Open Dots (2026-09-29). https://news.ycombinator.com/item?id=
- Reddit (미러 스냅샷): r/AI_Agents 1subxv6 (2026-04-25 스냅샷) · r/LocalLLaMA 1te3ehy (2026-05-15 스냅샷) · r/ClaudeAI 1qvmjic.
- Pragmatic Engineer. TDD, AI agents and coding with Kent Beck (에피소드 소개). https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent, 2025.
- velog: jaemin_ve (2026-03-11) · sukhee (2026-02-06) · code_able (2026-02-17) · namyeji (2026-10 하순) · fcwj24 (2026-05-22) · gwanghun-choi (2026-09-21) · aiengineer k-sdd (2025-12-29), ITDA-SDD (2026-01-14), k-sdd v3 (2026-05-07) · qlgks1 (2025-09-15). https://velog.io/
- GPTers 제이리. 클로드가 PRD와 다르게 제작하기도 한다. https://www.gpters.org/uiux/post/claude-also-produced-differently-MUlPcEeJxNHMkCL, 약 3개월 전(2026-07경).
- GeekNews: https://news.hada.io/topic?id=24400 · 24744 · 25917 · topic/29955 · 28082.

---

## 9. 리서치 한계

**리서처 상태:** web·paper·community 세 리서처 모두 산출물을 냈다. 실패한 리서처는 없다.

**접근 실패·간접 확인**
- OpenAI 계열 403: harness engineering 본문, dots 공식 도움말·안전 문서, DevDay 요약. → harness engineering 수치와 dots 기능은 검색 스니펫·언론 교차 범위로 제한했다.
- JetBrains 2026 블로그 2건, adtmag, betanews 403. web.archive.org 접근 불가.
- Reddit 본사이트 봇 차단(미러 스냅샷 4건만, 게시일 미확정), Lobsters(Anubis 차단), X·Mastodon 미검색, 커리어리·OKKY 관련 글 없음, GeekNews 댓글은 GN⁺의 HN 요약뿐(한국 사용자 독자 댓글 미확인), openai/codex 이슈에서 AGENTS.md 무시 스레드를 찾지 못함.
- 비arXiv 고전 논문(Gotel, Bainbridge, Tyree, Jansen, Parasuraman, Mäder, Aghajani, Buchgeher)은 전문을 읽지 않고 출판사·학회·기관 페이지와 2차 요약으로 확인했다. 대부분의 arXiv 논문도 abstract와 일부 HTML 본문 기준이다.
- web.md의 영어 인용 대부분은 요약 모델(WebFetch) 경유다.

**커버하지 못한 영역**
- **Hermes·dots를 설계 문서와 엮은 공개 실천은 커뮤니티·웹 어디에서도 찾지 못했다.** 이 두 도구의 설계 문서 운용 장(章)은 공식 문서 사실 + 저자 제안으로 채워야 한다.
- 한국어권 학술 연구(KCI 등) 미검색. 한국 커뮤니티에서 domain 규칙·권한·멱등성 같은 설계 내용을 문서화하는 논의는 거의 없다(담론이 "작업 방식" 문서에 머묾). 당근·네이버 D2의 AI 코딩 에이전트 도입 글은 찾지 못했고, 카카오테크 글은 본문을 추출하지 못했다.
- 형식 명세(TLA+, Alloy)와 LLM 결합 연구, 계약 테스트(Pact 등)·API 스키마 주도 개발의 LLM 실증 연구는 찾지 못했거나 범위 밖으로 남겼다.
- EARS 원 논문(Mavin et al. 2009) 미수집.
- DORA 2026 연례 AI 보고서는 조회 시점에 확인하지 못했다(2026-04 "ROI of AI-assisted Software Development" v2026.1은 별도 존재). Octoverse 2026은 미발행으로 보인다.
- 언어 편중: 한국어 1차 자료는 웹 약 6건 + velog 회고 중심. 목표(60~70%)에 못 미친다. 이 주제의 1차 소스(공식 문서·스펙·설문)가 영어라 불가피했다(웹 리서처).
- 교차 모델 리뷰 수치(71.6%→89.7% 등)의 원 논문을 찾지 못했다.

**근거 강도에 관한 일반 경고**
- 2026년 컨텍스트 파일·SDD 연구 다수가 프리프린트이고, 그중 여러 편이 단독 저자다(P-19, P-22 4편, P-10 Kraishan, P-26, P-SDD Piskala). P-17·P-20·P-21은 결과가 강하고 책 논지와 직결되지만 재현 연구가 아직 없다.
- 피인용수는 Semantic Scholar 기준(2026-10-28)이며 Google Scholar와 다르다.
- 커뮤니티 근거는 일화다. sgt101의 경고("No evidence, no attempt to create evidence")를 커뮤니티 의견 전체에 적용한다.

---

## 신선도 원장 (소스별 발행일·버전 시점·검색 시점)

형식: ID · 소스 · 발행/갱신일 · 버전 기준 · 조회 시점 · 신선도 주의

### 원전
- [원전] · 신규 프로젝트 설계와 AI 개발 통제 가이드 v1.0 · 2026-10 · — · 2026-10-28 · 가이드 스스로 "권장안과 가상 예시"

### 웹
- W-A1 · Hermes Agent README·docs · 저장소 2025-07-22, 첫 릴리스 2026-03-12 · v0.22.5 (2026-10-23), claude-code 스킬 v2.2.1 · 2026-10-28 · 스타 수는 조회 시점 값
- W-A2 · TechCrunch / DataCamp (dots) · 2026-09-29 · GPT-6 Astra, 2026-09/10 기준 · 2026-10 · 출시 한 달, 1차 문서 403
- W-A3 · npm·GitHub 버전 스냅샷 · — · Claude Code 2.1.312 / Codex 0.165.0 / Spec Kit 1.2.4 / OpenSpec 1.15.0 / BMAD 6.12.4 / Agent OS 3.0.0 · 2026-10-28 · 몇 주 단위로 바뀜
- W-B1 · Claude Code Best practices · 날짜 없음 · Claude Code 2.1.x · 2026-10 · 구 URL 308 리다이렉트
- W-B2 · Claude Code memory · 날짜 없음 · `/doctor prompt-audit` v2.1.283+ · 2026-10 · 2025년 "AGENTS.md 미지원" 자료는 구버전
- W-B3 · agents.md · 날짜 없음 · — · 2026-10 · 지원 도구 목록에 Claude Code 없음
- W-B4 · Codex AGENTS.md 문서 · 날짜 없음 · Codex CLI 0.16x · 2026-10 · 구 URL 308
- W-B5 · Codex best practices · 날짜 없음 · — · 2026-10 · 플랜 모드 토글·스킬·훅 세부는 [2차]
- W-B6 · OpenAI Cookbook ExecPlan · 날짜 없음(2025 말~2026 초 추정) · `gpt-5.2-codex` 언급 · 2026-10 · "archived, may reference outdated models"
- W-B7 · OpenAI Harness engineering · 2026-02-11 · — · 2026-10 · 본문 403, InfoQ 2026-02-21 보도로 날짜 확인
- W-B8 · Anthropic context engineering · 2025-09-29 · — · 2026-10 · 구버전일 수 있음(원리 위주)
- W-B9 · Böckeler context engineering · 2026-02-05 · — · 2026-10 ·
- W-B10 · agentskills.io · 날짜 없음 · — · 2026-10 ·
- W-B11 · GitHub Blog agents.md 2,500 repos · 2025-11-19 (2025-11-25 갱신) · — · 2026-10 · 구버전일 수 있음
- W-B12 · Claude Code permission modes / common workflows · 2026 · — · 2026-10 · 검색 엔진 캐시 약 105일 전
- W-C1 · GitHub Blog SDD toolkit · 2025-09-02 · 출시 당시 · 2026-10 · 명령어 표기 구버전일 수 있음
- W-C2 · Spec Kit README · 저장소 2025-08-21, v1.0.0 2026-08-21 · v1.2.4 (2026-10-27) · 2026-10-28 ·
- W-C3 · Kiro docs/blog · specs 2026-10-15, feature-specs 2026-08-04, steering 2026-10-21, GA 2025-11-17 · — · 2026-10 · 2차 출처의 GA 날짜 오류 주의
- W-C4 · Böckeler SDD 3 tools · 2025-10-15 · 당시 프리뷰/초기 버전 · 2026-10 · 도구 버전 구버전, 분류 틀은 유효
- W-C5 · Thoughtworks Radar Vol.33 · 2025-11-05 · Assess · 2026-10 · "no longer on the current edition", Vol.34 이후 미확인
- W-C6 · OpenSpec README · 저장소 2025-08-05 · v1.15.0 (2026-10-24) · 2026-10-28 ·
- W-C7 · BMAD README · 저장소 2025-04-13 · v6.12.4 (2026-10-14), v7 알파 · 2026-10-28 · v7 ETA(2026-10-16) 지남, 출시 여부 미확인
- W-C8 · Agent OS / Tessl · Agent OS v3.0.0 2026-01-20 · — · 2026-10 · Tessl 클로즈드 베타 [검색 스니펫]
- W-C9 · Scott Logic / Conffab / GeekNews · 2025-11-26 / 2025-12-09 / 2025-11-17 · — · 2026-10 · 원문 미열람
- W-D1 · 토스테크 · 2026-02-26 · — · 2026-10 ·
- W-D2 · 우아한형제들 · 2026-04-17 · — · 2026-10 ·
- W-D3 · 컬리 · 2025-12-24 · Claude Code v2.0.72, Opus 4.5 · 2026-10 · 구버전일 수 있음
- W-D4 · 카카오페이 · 2026-03-13 · 구버전 Spec Kit 흐름 · 2026-10 · if(kakao) 기반 추정
- W-D5 · LY Corporation · 날짜 없음(2026-01-29 추정) · — · 2026-10 · 날짜 [미확인]
- W-D6 · 기타 국내 인덱스 · 다양 · — · 2026-10 · 본문 미확인
- W-E1 · Harper Reed · 2025-02-16 · ChatGPT 4o/o3, o1, r1 · 2026-10 · 모델명 구버전, 저자 스스로 "2주 뒤엔 안 될 수도"
- W-E2 · Kent Beck · 2025-06-25 · — · 2026-10 ·
- W-E3 · Simon Willison · 2025-10-07 (2026-02 추기) · — · 2026-10 ·
- W-E4 · Addy Osmani · 2026-01-13 · — · 2026-10 ·
- W-E5 · How Anthropic teams use Claude Code · 2025-07-24 · — · 2026-10 · 구버전일 수 있음
- W-E6 · Anthropic 2026 Trends Report · 2026-01-21 [미확인, 4월 표기도] · — · 2026-10 · 본문 미열람
- W-F1 · Nygard · 2011-11-15 · — · 2026-10 · 고전
- W-F2 · MADR · 2024-09-17 · 4.0.0 · 2026-10 ·
- W-F3 · Ubl · 2020-07-06 · — · 2026-10 ·
- W-F4 · Orosz · 2022-06-21 (2024-02-07 갱신) · — · 2026-10 ·
- W-F5 · Fowler GivenWhenThen · 2013-08-21 · — · 2026-10 ·
- W-F6 · Stripe blog / API docs · 2017-02-22 / 2026-10 기준 · API v1·v2 동작 다름 · 2026-10 ·
- W-F7 · IETF Idempotency-Key 초안 · -07 2025-10-15, -08 2026-10-22 · 본문 확인은 -07 · 2026-10-28 · -08 변경 내용 미확인
- W-F8 · microservices.io outbox · 날짜 없음 · — · 2026-10 · 고전 패턴
- W-F9 · Pact docs · 2026-10 기준 · — · 2026-10 ·
- W-F10 · OpenAPI 3.2.0 · 2025-09-19 · 3.2.0 (같은 날 3.1.2) · 2026-10 · 날짜 2차 교차 확인, Swagger 일반 지원 2026-04 [2차]
- W-G1 · Stack Overflow 2025 · 2025-07-29 · — · 2026-10 · 2026 조사로 대체된 수치
- W-G2 · Stack Overflow 2026 · 2026-10-06 (조사 개시 공지 2026-06-23) · — · 2026-10 · 일부 수치 달레 블로그(2026-10-11) 단독
- W-G3 · DORA 2025 · 2025-09-23, AI Capabilities Model 2025-11-25 갱신 · — · 2026-10 · DORA 2026 연례 미확인
- W-G4 · JetBrains 2025 / 2026 · 2025-10-15 / i-programmer 2026-09-02 · 조사 2026-04~05 [엇갈림] · 2026-10 · 원문 403
- W-G5 · Octoverse 2025 · 2025-10-28 (2026-02-28 갱신) · 집계 2024-09-01~2025-08-31 · 2026-10 · Octoverse 2026 미발행으로 보임

### 논문 (발표일 = arXiv 최초 게시 또는 발표처 연도, 피인용수는 S2 2026-10-28)
- P-1 · METR · arXiv 2025-07-12 · Claude 3.5/3.7 Sonnet, Cursor Pro · 2026-10-28 · 피인용 229, 후속 블로그 2026-02-24
- P-2 · Google RCT · arXiv 2024 / ICSE-SEIP 2025 · 2024년 여름 사내 도구 · 2026-10-28 · 피인용 41
- P-3 · Cui 외 · Management Science 2025 · — · 2026-10-28 · [2차]
- P-4 · Peng 외 · arXiv 2023 · Copilot 초기 · 2026-10-28 · 피인용 863
- P-5 · Borg 외 · arXiv 2025 / ICSME 2025 RR · — · 2026-10-28 ·
- P-6 · He 외 · arXiv 2511.04427 / MSR 2026 · Cursor · 2026-10-28 · 피인용 40
- P-7 · Agarwal 외 · arXiv 2601.13597 / MSR 2026 · — · 2026-10-28 ·
- P-8 · Li 외 · 2025 / MSR 2026 · 에이전트 5종 · 2026-10-28 ·
- P-9 · Watanabe 외 · arXiv 2509.14745 / TOSEM · Claude Code · 2026-10-28 · 피인용 115
- P-10 · AIDev 후속 묶음 · 2026 (arXiv 2601~2609) · — · 2026-10-28 · Kraishan 단독 저자
- P-11 · Wang 외 · arXiv 2503.15223 / ICSE 2026 · SWE-bench Verified · 2026-10-28 · 피인용 85
- P-12 · EvalPlus · NeurIPS 2023 · 26 LLM(2023) · 2026-10-28 · 피인용 2,460
- P-13 · SWE-bench 및 비판 · 2023~2026 · Claude 2 등 · 2026-10-28 · Pro Verified/V2 수치 미확인
- P-14 · Chatlatanagulchai 외 · PROFES 2025 · — · 2026-10-28 ·
- P-15 · Agent READMEs · arXiv 2511.12884 / TOSEM · — · 2026-10-28 · 피인용 43
- P-16 · Mohsenimofidi 외 / Galster 외 / Abubakar 외 · MSR 2026 / arXiv 2602 / ESEM 2026 · — · 2026-10-28 ·
- P-17 · Gloaguen 외 · arXiv 2602.11988 · Claude Code(Sonnet-4.5), Codex(GPT-5.2, GPT-5.1 mini), Qwen Code · 2026-10-28 · 피인용 33, 프리프린트
- P-18 · Lulla 외 · arXiv 2601.20404 · — · 2026-10-28 · 프리프린트
- P-19 · Khatri · arXiv 2607.27250 · Claude Code·Codex · 2026-10-28 · 단독 저자
- P-20 · Zhang 외 · arXiv 2604.11088 · Claude Opus 4.6 · 2026-10-28 · 프리프린트
- P-21 · Xu & Wu · arXiv 2610.30571 (2026-10-22) · Claude Code·Codex CLI · 2026-10-28 · 매우 최신, 프리프린트
- P-22 · Yan / Sharma / McMillan / Chakrabarti / Wang 외 · arXiv 2603~2610 (2026) · — · 2026-10-28 · 4편 단독 저자
- P-23 · Zadenoori 외 · arXiv 2509.11446 · 2023~2024 연구 74편 · 2026-10-28 · 피인용 59
- P-24 · Ambig-SWE · arXiv 2502.13069 / ICLR 2026 · — · 2026-10-28 · 피인용 53
- P-25 · ClarifyGPT / HumanEvalComm / ClarifyCodeBench · 2023 / 2025 / 2026 · GPT-4 등 · 2026-10-28 · ClarifyGPT 발표처 미확인
- P-26 · Wei · arXiv 2406.10101 · — · 2026-10-28 · 단독 저자, 정량 평가 없음
- P-27 · Macke & Doyle · Findings of NAACL 2024 · 2023~2024 모델 · 2026-10-28 ·
- P-28 · Mathews & Nagappan · ASE 2024 · GPT-4, Llama 3 · 2026-10-28 · 피인용 96
- P-29 · TiCoder · IEEE TSE 2024 · — · 2026-10-28 · 피인용 176
- P-30 · Clover · SAIV 2024 · — · 2026-10-28 · 피인용 106
- P-31 · nl2postcond · FSE 2024 · — · 2026-10-28 · 피인용 145
- P-32 · Spracklen 외 · USENIX Security 2025 · LLM 16종 · 2026-10-28 · 피인용 139
- P-33 · Huang 외 · ICLR 2024 · — · 2026-10-28 · 피인용 1,395
- P-34 · Kamoi 외 · TACL 2024 · — · 2026-10-28 · 피인용 408
- P-35 · Kim 외 · ICML 2025 · LLM 350개+ · 2026-10-28 · 피인용 71
- P-36 · Goel 외 · ICML 2025 · — · 2026-10-28 · 피인용 75
- P-37 · Panickssery 외 · NeurIPS 2024 · GPT-4, Llama 2 · 2026-10-28 · 피인용 962
- P-38 · Ahmed 외 · arXiv 2408.05534 · — · 2026-10-28 · 발표처 미확인
- P-39 · Liu 외 Lost in the Middle · TACL 2024 · 2023년 모델 · 2026-10-28 · 피인용 5,704
- P-40 · Jansen & Bosch · WICSA 2005 · — · 2026-10-28 · DOI·표현 미확인
- P-41 · Tyree & Akerman · IEEE Software 2005 · — · 2026-10-28 · [2차]
- P-42 · Buchgeher 외 / Garcia de Santana Junior 외 · 2023 / ICSA 2026 · — · 2026-10-28 · [2차]
- P-43 · Dhar 외 / Zhou 외 · ICSA 2024 / TOSEM 2025 · GPT-4 등 · 2026-10-28 · 피인용 72 (Dhar)
- P-44 · Mäder & Egyed · EMSE 2015 (온라인 2014) · AI 이전 · 2026-10-28 · [2차]
- P-45 · Gotel & Finkelstein 외 · 1994 / 2023~2024 · — · 2026-10-28 · [2차]
- P-46 · Aghajani 외 · ICSE 2019 · — · 2026-10-28 · 범주 수 미확인
- P-47 · Bainbridge · 1983 · — · 2026-10-28 · [2차]
- P-48 · Parasuraman & Manzey · 2010 · — · 2026-10-28 · [2차]
- P-49 · Perry 외 · CCS 2023 · codex-davinci-002 · 2026-10-28 · 피인용 494
- P-50 · Pearce 외 · IEEE S&P 2022 · 2021년 Copilot · 2026-10-28 · 피인용 1,068
- P-51 · Shen & Tamkin · arXiv 2601.20245 (2026) · — · 2026-10-28 · 피인용 47, 프리프린트
- P-52 · 인지·과의존 묶음 · 2023~2025 · — · 2026-10-28 · Kosmyna 프리프린트, Lee 외 [2차]
- P-53 · ChatDev · ACL 2024 · — · 2026-10-28 · 피인용 1,397
- P-54 · MetaGPT · ICLR 2024 · GPT-4 · 2026-10-28 · 피인용 2,707
- P-55 · Self-collaboration · TOSEM · ChatGPT · 2026-10-28 · 피인용 579
- P-56 · AgentCoder · arXiv 2023 · GPT-4 · 2026-10-28 · 발표처 미확인
- P-57 · Cemri 외 · NeurIPS 2025 D&B · GPT-4o 등 · 2026-10-28 · 피인용 802, 판본별 실행 기록 수 차이
- P-58 · Wang 외 · ACL 2024 · — · 2026-10-28 · 피인용 241
- P-59 · Agentless / Gao 외 · 2024 / 2025 · — · 2026-10-28 · Agentless 피인용 561
- P-60 · Kim 외 · arXiv 2512.08296 · LLM 3계열 · 2026-10-28 · 피인용 165
- P-SDD · Piskala / Taghavi & Bhavani / Grynets 외 · 2026 · — · 2026-10-28 · 프리프린트, Piskala 단독 저자
- P-회색 · DORA 2024 / GitClear 2025 / Uplevel 2024 · 2024~2025 · — · 2026-10-28 · [2차]

### 커뮤니티 (수집일 2026-10-28, "N개월 전"은 이 날짜 기준)
- C-패턴1 · claude-code #2544 (2025-06-24, 댓글 2025-08~2026-01), #33603 (2026-03-12), HN 46098838 (2025-11-30), HN 49945933 (2026-10-03) · 모델·하네스 버전에 따라 바뀔 수 있음
- C-패턴2 · HN 50227041 (2026-10-25~26), HN 49376287 (2026-08-20), spec-kit #620 (2025-09-27, 댓글 2025-11-15)
- C-패턴3 · Pragmatic Engineer 에피소드(2025), r/AI_Agents 미러 스냅샷 2026-04-25 (GPT-5.4 시기), HN 47745102 (2026-04-12), spec-kit #75 댓글 (2025-09-09), HN 49847968 (2026-09-25)
- C-패턴4 · GPTers (약 3개월 전), HN 45935763 (2025-11-15), HN 47034087 (2026-02-16), HN 49840054 (2026-09-25), HN 47135917 (2026-02-24)
- C-패턴5 · spec-kit #75 (2025-09-08), #1174 (2025-11-13), HN 45935763, r/LocalLLaMA 미러 2026-05-15 · Spec Kit 구버전 시기 경험
- C-패턴6 · #2544 댓글 (2025-08-07), velog jaemin_ve (2026-03-11), HN 46492381 (2026-01-04), HN 48275853 (2026-05-26)
- C-패턴7 · velog sukhee (2026-02-06), HN 49298901 (2026-08-14), velog code_able (2026-02-17)
- C-패턴8 · velog namyeji (2026-10 하순), HN 49376287, HN 47034087
- C-휴리스틱1 · HN 47034087 (2026-02-16), velog fcwj24 (2026-05-22)
- C-휴리스틱2 · HN 46098838, HN 48413629 (2026-06-05), HN 49945933, HN 47938417 (2026-04-28), r/ClaudeAI
- C-휴리스틱3 · HN 43094006 (2025-02-18), HN 43929599 (2025-05-08), HN 49376287, HN 49945933, HN 49840054
- C-휴리스틱4 · velog jaemin_ve (2026-03-11), HN 45935763, HN 49840054
- C-휴리스틱5 · HN 45935763, HN 48413629, HN 43094006, spec-kit #75
- C-휴리스틱6 · HN 48150810 (2026-05-15), HN 47800969 (2026-04-16, Claude Opus 4.7 스레드), HN 48853334 (2026-07-09, GPT-5.6 스레드), HN 49166538 (2026-08-04) · 모델명 빨리 낡음
- C-휴리스틱7 · HN 47212355 (2026-03-02), HN 50227041, HN 49840054
- C-휴리스틱8 · HN 46098838, HN 49840054, HN 49298901
- C-휴리스틱9 · HN 49896604 (2026-09-29~30), HN 47911524 (2026-04-26), HN 49298901
- C-논쟁A · HN 45935763 (2025-11-15), GeekNews 24400 (2025-11-17), HN 47197595 (2026-02-28), HN 46955747 (2026-02-10)
- C-논쟁B · HN 49840054 (2026-09-25), Opus 5.5 시점 발언 · 원 글 본문 미확인, 도구 기능 주장은 빨리 낡음
- C-논쟁C · HN 50227041 (2026-10-25), HN 47938417 (2026-04-28), HN 49945933
- C-논쟁D · HN 46098838, HN 47034087, HN 47938417, velog fcwj24
- C-논쟁E · HN 49760187 (2026-09-18), HN 44957443 (2025-08-20), velog gwanghun-choi (2026-09-21) · 지원 버전 미확인
- C-도구 Hermes · HN 48373851 (2026-06-02), 48455560 (2026-06-09), 48586005 (2026-06-18), hermes-agent 이슈 #344 (2026-03-04), #5257 (2026-04-05), #29125 (2026-05-20)
- C-도구 dots · HN 49896604·49896565·49897710 (2026-09-29), 49971444 (2026-10-05), 50084055 (2026-10-14), Ask HN SSL (2026-10-25), 50229493 (2026-10-28) · 출시 한 달 차
- C-한국 · velog 검색 count (2026-10-28 기준: CLAUDE.md 990, AGENTS.md 489, spec-kit 51, 스펙 주도 개발 23), aiengineer (2025-12-29~2026-05-07), qlgks1 (2025-09-15), GeekNews 24744·25917·29955·28082
