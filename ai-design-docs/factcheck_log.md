
## 01장 (라운드 1)

### ❌ 정정
- METR 후속(2026-02-24 블로그): "앞선 연구에서 돌아온 개발자 기준으로 완료 시간 18% 단축 … 신뢰구간(−38%~+9%)" → "돌아온 개발자 10명에게서는 18% 단축이, 새로 합류한 47명에게서는 4% 단축이 … 두 신뢰구간(−38%~+9%, −15%~+9%)이 모두 0을 포함". 57명 가운데 복귀자는 10명뿐이라 표본 크기를 밝혔다. "very weak evidence"는 METR 원문에서 "속도 향상의 크기"에 대한 표현이라 그 범위에 맞췄다. 근거: research/papers.md 논문 1-후속, METR 블로그 원문 웹 대조(2026-10-28).
### ⚠️ 약화·삭제
- Stack Overflow 2026 "신뢰에 출처 표시 필요 93%" → "결과 발표 글이 든 수치. 어느 응답자 집단의 비율인지는 글에 없으니 방향만 읽자". 블로그 원문을 웹으로 대조했더니 분모가 적혀 있지 않았다("to trust what the AI gives requires source attribution (93%)").
### 🕒 신선도
- (없음. 설문·도구 수치에 연도와 발표일이 이미 적혀 있다)
### ✅ 확인 (요약)
- METR 원 연구 수치 9건(16명·246과제·도구·−24%/−20%/+19%·39%/38%·암묵적 저장소 맥락은 인과가 아닌 후보): papers.md 논문 1. §7 #1·#2를 지킨다(완료 시간 기준으로 통일, 2025년 초 조건으로 한정).
- METR 후속 57명·143저장소·800+과제·2025-08 시작·30~50% 미제출·"only very weak evidence": METR 블로그 원문 웹 확인.
- Paradis(96명·약 21%·저자 단서), Cui(4,867명·26.08%), Peng(2023 프리프린트·JS HTTP 서버·55.8%, §7 #3 맥락 동반), He 외·Agarwal 외(MSR 2026, 18%·39%, 저자 중복): papers.md 논문 2·3·4·6·7.
- SO 2025 "AI agents are not yet mainstream"·매일 14.1%, DORA 2025 약 5,000명·90%·"mirror and a multiplier": 원문 웹 확인. SO 2026(2026-10-06·3만여 명·73%·Claude Code 66%·Copilot 59%): web.md G2 + 블로그 원문 웹 확인. JetBrains 2026(1만 5천여 명·Claude Code 39%←3%·Codex 16%←0%, 2차 경유라고 본문에 적힘): web.md G4.
- 토스페이먼츠 김용성(2026-02) 인용 2건, 컬리 이준환(2025-12, v2.0.72·Opus 4.5): web.md D1·D3.
- 원전 인용 6건(제목·2026년 10월, 세 가지 일과 질문 3개, 핵심 원칙, 폭포수 아님, 문서 완성률 100%, CAN 가상 예시): research/primary 원문과 일치.
### 미해소
- (없음)

## 02장 (라운드 1)

### ❌ 정정
- Böckeler 분류: "Kiro·Spec Kit·Tessl 모두 실제로는 대부분 spec-first로 쓰이고 있었고, spec-as-source 쪽을 탐색하는 도구로는 Tessl" → "찾아본 SDD 접근은 모두 spec-first였고, Kiro와 Spec Kit은 거기서 크게 나아가지 않았다. spec-anchored를 분명히 지향하면서 spec-as-source까지 탐색하는 도구로는 Tessl". martinfowler.com 원문 웹 대조("Tessl is the only one of these three tools that explicitly aspires to a spec-anchored approach, and is even exploring the spec-as-source level"). Tessl을 "대부분 spec-first"로 묶은 것이 원문과 어긋났다.
### ⚠️ 약화·삭제
- 저술가 HTML 주석(요약 경유 인용 확인 요청, W-C4·W-C5) 삭제. 아래 원문 대조로 닫았다.
### 🕒 신선도
- (없음. 도구 표 "2026-10 기준", Radar "Vol.33 시점·현재판 아님", 카카오페이 흐름 "당시 Spec Kit"이 이미 적혀 있다. §7 #31·#32·#33 준수)
### ✅ 확인 (요약)
- Böckeler 요약 경유 인용 2건("sledgehammer to crack a nut", "I'd rather review code than all these markdown files"): 원문 웹 확인, 한국어 의역 정확.
- Radar Vol.33 요약 경유 표현 3건("elaborate and opinionated", "some generate lengthy spec files that are hard to review", "We may be relearning a bitter lesson")·Assess·2025-11-05·현재판 아님 표시: 원문 웹 확인.
- 도구 표 버전·날짜 5건(Spec Kit v1.2.4/2026-10-27·converge 반복, Kiro GA 2025-11-17·EARS, OpenSpec v1.15.0/2026-10-24, BMAD v6.12.4/2026-10-14 "Small changes go straight to build", Agent OS v3.0.0/2026-01-20), OpenSpec "iterative not waterfall": 레퍼런스 §0, web.md A3·C2·C3·C6·C7·C8 [원문 직접 확인].
- 커뮤니티 인용 귀속: spec-kit #1174(2025-11-13, "30 files changed, < 20 actual LOC", roperi·surajsrivastav "genrated"는 원문 오탈자 그대로·eduvav), HN 45935763(2025-11-15, 191댓글, laserlight·zvr·4ndrewl·yoz-y·podgorniy·macrolime·ErrantX·sgt101). beders는 HN 47197595 "다른 스레드"로 바르게 귀속됨: community.md 원문과 일치.
- 카카오페이 wayne.cai(2026-03) 인용·서술 3건: web.md D4. 원전 인용 4건(폭포수 아님, 작은 프로젝트는 합치고, 금전·민감정보, 테스트는 실행 가능한 표현): research/primary와 일치. spec-anchored 해석은 "이 책의 해석"으로 표시됨.
### 미해소
- (없음)

## 03장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- 저술가 HTML 주석(요약 경유 인용 확인 요청, W-B1·W-B2) 삭제. 아래 원문 대조로 닫았다.
### 🕒 신선도
- "AGENTS.md만 있으면 …" → "기본 설정에서는 AGENTS.md만 있으면 …". 공식 문서(code.claude.com/docs/en/memory, 2026-10-28 조회)는 이 표를 "by default" 동작으로 적고, Project instructions 설정으로 바꿀 수 있다고 밝힌다. (참고: 같은 문서에 "Reading AGENTS.md directly requires Claude Code v2.1.277 or later"가 있어 §7 #23의 2.1.277은 이제 1차로 확인됐다. 본문에 버전을 쓰지 않았으므로 바꾸지 않았다.)
### ✅ 확인 (요약)
- Xu & Wu 프리프린트: arXiv 2610.30571, 2026-10-22 게시, Python 프로젝트 40개·320회·90.1%·79/80·20/80 중 17·4.2%→91.4%·89.4%→100%·원인 설명. arXiv 초록을 웹으로 확인했다(실재함, 의심 식별자 아님). §7 #5 hedge(프리프린트·재현 없음·조건 한정)가 본문에 있다.
- Macke & Doyle(MITRE, Findings of NAACL 2024): papers.md 27. §7 #41의 모델 세대 한정 문구가 있다.
- Claude Code 문서 주장 7건("context, not enforced configuration"+PreToolUse 훅, 200줄·준수 저하, `.claude/rules/`+`paths:`, `@path` 임포트는 컨텍스트 비용을 줄이지 않음, AGENTS.md 읽기 3조합, 모순 시 임의 선택, `/doctor`가 덜어 낼 것·남길 것)과 Best practices "repo에서 찾을 수 없는 것만"·예시 3종: 원문 웹 확인.
- Codex 로드 규칙(루트→작업 디렉터리, 디렉터리당 1개, 뒤 파일이 덮어씀, 32 KiB, 목록 밖 파일명 무시): web.md B4. Hermes first-match 순서·merged chain·progressive discovery: web.md A1 [원문 직접 확인]. 두 규칙을 합친 해석은 본문과 그림 캡션 모두에 "책의 해석"으로 표시됨.
- 예시 AGENTS.md/CLAUDE.md: 특수 문법은 `@AGENTS.md` 임포트 하나뿐이고, 공식 문서가 권하는 형태와 같다. 나머지는 일반 마크다운이며 "(미실행)" 표시가 있다.
- 버전 시점(Claude Code 2.1.312, Codex CLI 0.165.0, Hermes v0.22.5): 레퍼런스 §0.
- Gloaguen(수치 전부, §7 #4 준수: 커뮤니티 수치를 쓰지 않음), Lulla(−28.64%·−16.58%·5쪽 단편), Khatri(17과제·288회·단독 저자), Arabat & Sayagh(148·15,549·27.7%·26.35%), McMillan(1,650회·효과 미검출·단독 저자, §7 #7 hedge): papers.md 17·18·19·10·22.
- varyherb(HN 50227041 "Show HN: ADRs for AI", 2026-10), pamelafox(HN 47034087) 인용: community.md 원문과 일치. 우아한형제들 이재홍(2026-04) 인용 2건: web.md D2. 원전 §02 표·인용 4건: research/primary와 일치.
### 미해소
- (없음)

## 11장 (라운드 1)

### ❌ 정정
- "Codex는 `.agents/skills/`에 둔다고 알려져 있다(Codex 위치는 2차 출처 기준이다)" → "Codex는 저장소의 `.agents/skills/`에 둔다(두 도구의 공식 문서, 2026-10 기준)" — 근거: Codex 공식 문서 learn.chatgpt.com/docs/build-skills.md ("Codex scans `.agents/skills` in every directory from your current working directory up to the repository root.", 2026-10-28 조회). 2차 출처 단서를 1차 확인으로 승격.
- `(사실 확인 필요)` 서브에이전트 정의 파일 위치·형식 → 확인 후 명시: Claude Code `.claude/agents/`(사용자 범위 `~/.claude/agents/`), YAML 머리말 + 마크다운 본문, `name`·`description`만 필수 — 근거: code.claude.com/docs/en/sub-agents ("Subagent files use YAML frontmatter for configuration, followed by the system prompt in Markdown." / "Only `name` and `description` are required."). Codex `.codex/agents/`(개인 `~/.codex/agents/`), 에이전트 하나당 TOML 파일 하나, `name`·`description`·`developer_instructions` 필수 — 근거: learn.chatgpt.com/docs/agent-configuration/subagents.md. "2026-10 공식 문서 기준" + "자주 바뀌니 공식 문서 확인" 휘발성 문구 유지.
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- 서브에이전트·스킬 위치에 "2026-10 기준" 명기(위 정정에 포함).
### ✅ 확인 (요약)
- 원전 인용 4건(§10 첫 문장, 역할표 금지 4종, 공통 입력 꾸러미·단서, 마지막 문장) — primary 원문과 일치.
- 논문 수치 전부 papers.md 원문 대조 일치: MetaGPT 역할 제거 1.0/2.0/2.5/4.0·PM+Project Manager 2.0(P-54, 책의 추론 표시 유지), Cemri 외 7종·14종·11.8/6.8/8.2/9.1%·ProgramDev +15.6%(P-57), Wang 외 ACL 2024(P-58), Yubin Kim 260개 구성·+80.8%/−70.0%(P-60), Zhou 외 TOSEM 정밀도·재현율·64.45~69.42%·1.59~3.24%(P-43), Guardrails Beat Guidance 679개·Opus 4.6·5,000회·+13.8%p(P-20, 단정 금지 #6 hedge 유지), Parasuraman & Manzey(2차 표시), Perry 외 CCS 2023·codex-davinci-002(참가자 수 미기재 — #46 준수), Shen & Tamkin 52명·27점·4.15점·패턴(#44 hedge 유지), Lee 외 CHI 2025 319명·936개.
- 웹: Codex 4요소·서브에이전트 권고·"same mistake twice"(W-B5), Matt Nigh 2025-11-19·2,500개·3단 경계·"Never commit secrets"(github.blog 원문 재대조 일치), 컬리 2025-12-24·v2.0.72·Opus 4.5·PM 1+엔지니어 3·MSA 12·"TPM AI 1 + MSA AI 11"(W-D3), LY 인용·날짜 추정 hedge(W-D5, #49 준수), dots Custom Rules 4행동(2차 hedge 유지).
- 커뮤니티: jankdc(HN 46098838)·joegibbs(HN 49840054) 원문 HN API 재대조 일치.
### 미해소
- (없음)

## 12장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- ADR 63% 문장: "ICSA 2026에 발표된 … 연구는 ADR 5,800개 가운데 약 63%가 … 보고했다. 이 책은 학회 프로그램 페이지를 거쳐 확인했고 전체 저자와 DOI는 확인하지 못했다" → "ICSA 2026에 실린 … 연구는 초록에서 ADR 약 5,800개 가운데 약 63%가 … 보고했다. 이 책은 학회 프로그램 페이지에 실린 초록으로만 확인했고, 논문 본문과 DOI는 확인하지 못했다" — 근거: conf.researchr.org ICSA 2026 논문 페이지 초록(약 5,800개 중 약 3,674개 ≈ 63%가 "accepted"로 생성, 2026-10-28 웹 검색 경유). 단정 금지 #38 준수(2차·초록 기준 hedge 명시). 수치 자체는 초록과 일치해 유지.
### 🕒 신선도
- `/doctor` 문장에 명령 이름과 원문 범위(디렉터리 구조·의존성 목록·아키텍처 개요 / 함정·근거·도구 기본값과 다른 관례)를 정확히 반영, "2026-10 기준" 유지 — 근거: code.claude.com/docs/en/memory 원문 재대조("The `/doctor` checkup proposes trims for a checked-in CLAUDE.md: it cuts content Claude can derive from the codebase, such as directory layouts, dependency lists, and architecture overviews, and keeps pitfalls, rationale, and conventions that differ from tool defaults.").
### ✅ 확인 (요약)
- HN 49376287: 제목·게시일(2026-08-20) 일치. 원 글 인용은 Arainach 댓글이 옮긴 문장과 일치(생략부 "aggressively steering a smarter one…"를 "..."로 처리 — 의미 왜곡 없음). JasonSage 문장 일치(인용은 "stick around"에서 끊음, 원문은 "like it's all still necessary"로 이어짐 — 왜곡 없음). HN Algolia API로 원문 대조.
- 커뮤니티 원문 대조 일치: varyherb·azeirah·esafak(HN 50227041), rfw300(HN 47212355), candiddevmike(HN 46098838).
- Chakrabarti 1,867개·247,694개·226%·4.9개·근거 주석(P-22, 프리프린트·단독 저자 hedge 유지, #7 준수). Nygard 2011 형식·번호 규칙·superseded(W-F1). MADR 4.0.0(2024-09-17) Confirmation(W-F2). Gotel & Finkelstein 1994(2차 표시). "설계 지식의 증발"은 원문 인용 형식 아님(#37 준수).
- IETF 초안 -07 422·-08 미확인, Stripe 오류 거절(W-F6·F7, #35 준수). 원전 §06 "409 IDEMPOTENCY_CONFLICT"·"HTTP 상태 코드는 이 예제의 선택입니다" 원문 일치.
- 원전 §08 생애·ADR 기준·덮어쓰기 금지·Rejected/Withdrawn·상태 표시, §12 머리말 11필드·"필요한 필드만 유지하세요"·Accepted≠구현됨, §09 "변경 이유와 바뀌는 약속" — primary 원문 일치.
### 미해소
- (없음)
### 편집 후속 (editor, 2026-10-29)
- 위 ✅의 "IETF 초안 -07 422·-08 미확인"은 06장 ❌ 항목(-08 원문 직접 확인: 다른 페이로드 재사용 422 SHOULD, RFC 아님)으로 닫혔다. editor가 04_manuscript.md 12장 본문("IETF 초안(-07·-08)은 422를 권하고")과 Draft ADR-002 선례 줄("-07·-08: 422 (SHOULD, 아직 RFC 아님)")을 06장에 맞춰 정렬했다. 새 사실 없음.

## 08장 (라운드 1)

### ❌ 정정
- "`/speckit-assess-decide`도 문서화된 이유와 함께 멈추는 것을 유효한 결과로 인정한다" → "README도 사전 평가 확장의 마지막 단계 `/speckit-assess-decide`가 내린 결정(`go`·`needs-clarification`·`kill`)을 설명하면서, 문서화된 이유와 함께 멈추는 것도 유용한 결과라고 적어 둔다" — 근거: github/spec-kit README 원문(gh api, v1.2.4 2026-10-27) "Stopping with a documented reason is also a useful outcome." (research/web.md C2의 "[valid outcome]" 복원이 원문과 다름)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — Spec Kit v1.2.4/2026-10, Claude Code 모범 사례 2026-10 기준 표기 이미 있음)
### ✅ 확인 (요약)
- 원전 대조 10건(§07 Design Ready 정의, BLOCK/CONDITIONAL/LATER 정의·처리, 게이트 다섯 가지, 스파이크 절차·예시 질문, AI 검토 문장 2개, §13 18개 체크리스트와 단서, INV-CAN-03, POL-CAN-01 예시 조건, API-CAN-01 입력 reasonCode) — research/primary 원문과 일치
- 논문 6건: Barke 외(OOPSLA 2023, 20명, 가속/탐색 모드), Huang 외(ICLR 2024), Kamoi 외(TACL 2024), Kim 외(ICML 2025, 350개+, 60%), Goel 외(ICML 2025), Panickssery 외(NeurIPS 2024) — papers.md 논문 33~37·P-52 행과 일치
- 커뮤니티 인용 2건(mrcode007 "It finds errors CC doesn't.", robertwt7 "it always find something that claude missed.") — community.md 휴리스틱 6과 일치, 경험담으로 hedge됨
- W-B1 "문제를 찾으라고 시킨 리뷰어는 늘 무언가를 찾는다 / 전부 고치면 추상화 계층·불가능한 경우의 테스트가 늘어난다" — code.claude.com/docs/en/best-practices 원문 직접 대조(2026-10-28)로 확인. 요약 경유 hedge 불필요
- §7 단정 금지 #52(HTTP 코드는 예제의 선택) — "원전 예제의 선택으로 진행"으로 이미 처리됨
### 미해소
- (없음)

## 13장 (라운드 1)

### ❌ 정정
- mike_hearn 서술: "밤새 고객 지원 티켓을 처리해 둔 결과가 "waiting for my approval" 상태로 기다리게 한다" → "고객 지원 티켓을 맡기는데, 아침에 일어나 보면 티켓의 수정이나 답변이 이미 "waiting for my approval" 상태로 기다리고 있을 때가 있다" — 근거: HN 49896604 원문("Sometimes I wake up and the fix/response for a ticket filed by a customer is already there waiting for my approval."). 원문의 "Sometimes"를 살려 상시 동작처럼 읽히던 과장을 바로잡음.
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (추가 없음 — Hermes "v0.22.5", dots "2026-10 기준" 이미 명기)
### ✅ 확인 (요약)
- Hermes(1차 문서 재대조): context-files 문서에서 "Only one project context type is loaded per session (first match wins)"와 순서 `.hermes.md` → `AGENTS.override.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`, git 저장소 내 AGENTS.md "merged chain", 하위 디렉터리 "progressively discovers" 일치. 두 규칙의 상호작용은 문서에 명시돼 있지 않음을 확인 → 원고의 "책의 해석이니 문서로 한 번 더 확인하자" hedge가 정확하므로 유지. v0.22.5(2026-10-23)·MIT·README 문구·cron 인용·서브에이전트 인용·agentskills.io·번들 스킬 `claude-code` v2.2.1/`codex`/`opencode`·MEMORY.md 2,200자/USER.md 1,375자·frozen snapshot·초과 시 오류·홈 공유 경고 — W-A1 [원문 직접 확인]과 일치.
- dots: DevDay 2026(2026-09-29), 클라우드 컴퓨터·브라우저, GPT-6 Astra(TechCrunch 귀속), Pro·Business Premium, 채널, Custom Rules 4행동·Auto-review(DataCamp 귀속), Codex 클라우드 태스크 — W-A2 교차 확인 범위 안. 범위 밖(앱 수·가격·기억 삭제)은 쓰지 않는다고 명시(#27 준수). "업계 관행" 서술 없음, 패턴 소절 모두 [저자 제안] 표시(#28 준수). 원고에 고안된 설정 키·명령 없음(cron 작업 문장은 "예시, 미실행" 자연어 초안).
- 커뮤니티 HN API 원문 대조 일치: hadlock(HN 48373851), OliverGuy(HN 49896604, 읽기 전용 자격 증명·MR까지), slurpyb(HN 50229493, "Ask HN: Are people aware OpenAI Dots intercept SSL?" 스레드 댓글 2026-10-28), HN 50084055 제목·게시일 2026-10-14.
- 원전 §09 문서 CI "링크·ID 누락, 스키마 유효성", "CI 초록색의 정확한 의미", §10 프롬프트 4 중단 조건 — primary 원문 일치. "(웹 리서처의 해석)" 귀속 표시 유지.
### 미해소
- (없음)

## 09장 (라운드 1)

### ❌ 정정
- ExecPlan 페이지 표시 "보관됨(archived), 오래된 모델을 언급할 수 있음" → "보관됨(archived), 오래된 모델이나 API를 언급할 수 있음"(2026-10 기준) — 근거: developers.openai.com/cookbook/articles/codex_exec_plans 원문 배너 "This recipe is archived and may reference outdated models or APIs." (2026-10-28 직접 확인). 보관 표시 자체는 확인됨
- Claude Code 플랜 모드: "공식 문서를 검색 요약으로 확인한 바로는 … 검색 요약을 거친 정보라" → "공식 문서(2.1.312/2026-10 기준)에 따르면 … 파일을 읽고 탐색 명령을 실행하며 계획을 쓰되 소스를 편집하지 않는다. `/plan` 접두 또는 `claude --permission-mode plan`" — 근거: code.claude.com/docs/en/permission-modes 원문 직접 대조 "Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source." / "prefixing a single prompt with `/plan`" / `claude --permission-mode plan`. W-B12(검색 요약 경유, 캐시 105일)의 세부가 원문과 일치함을 확인했으므로 "검색 요약" 단서를 사실 표기로 교체
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- 플랜 모드 조작법에 "2.1.312/2026-10 기준" 부착, "버전에 따라 바뀔 수 있다" 휘발성 문구 유지
### ✅ 확인 (요약)
- 원전 대조 9건(§02 plan/ 질문·권위 내용, §03 단계 5·6, SLICE-CAN-01 순서와 출시 단서, AC↔TC 번호 짝·검증 방법 5행, VAL-CAN-01 증거 항목·"AI가 검토 완료" 문장, §12 공통 머리말 필드·검증 기록 템플릿 "실행 전 정의", §06 8단계 추적 경로, FAILED 후 재시도 규칙·AC-CAN-02 "정책으로 결정", §09 "임의로 확정하지 않는다", NFR-I01) — research/primary 원문과 일치
- 공식 문서 4건 원문 직접 대조(2026-10-28): Codex 모범 사례 플랜 모드 문장·"Running live tasks on the same files without using Git worktrees"·서브에이전트 "exploration, tests, or triage" (learn.chatgpt.com/guides/best-practices), Claude Code 모범 사례 증거 요구·"looks done … you the test suite" (code.claude.com/docs/en/best-practices)
- 논문 2건: Abubakar 외(ESEM 2026 ER, arXiv 2608.04661, 36,710개 → 10개 저장소 85개), Vasconcelos 외(CSCW 2023, 5개 연구 N=731) — papers.md와 일치
- 커뮤니티 5건: HN 49840054 "Plan mode is dead"(2026-09-25), bcherny 발언(소속·구현 미확인으로 hedge됨, §7 #24·#50 충족), txhwind ADR 비유, simonw spec.md, ozgung STATUS.md, sermakarevich 세션 재시작 — community.md와 일치. "HN 사용자 simonw"는 레퍼런스가 Simon Willison과 연결하지 않으므로 그대로 둠
### 미해소
- (없음)

## 14장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- "Harper Reed는 자기 작업 흐름을 소개하며" → "Harper Reed는 2025년 2월에 자기 작업 흐름을 소개하며" — 근거: harper.blog 2025-02-16 글(W-E1). "2주 뒤엔 안 통할 수도"라는 인용의 시점을 밝혀 문단 논지(도구 세부는 빨리 낡는다)와 맞춤.
### ✅ 확인 (요약)
- Harper Reed "This is working well NOW, it will probably not work in 2 weeks, or it will work twice as well." — harper.blog 원문 재대조 일치.
- Matt Nigh "Start simple. Test it. Add detail when your agent makes mistakes." — github.blog 원문 재대조 일치(2025-11-19, "over 2,500 agents.md files across public repos").
- pamelafox(HN 47034087), simonw(HN 47938417, 2026-04-28) — HN API 원문 대조 일치.
- 원전 인용 전부 primary 원문 일치: §11 첫 문장·SMALL/MEDIUM 구성·분리 신호·"파일을 합쳐도…" 단서, §11 첫 주 "조정 가능한 예시"·"하루가 밀렸다고 게이트를 생략하지 않습니다", §14 30분 빠른 시작 5단계·"구현 승인이 아니라"·흔한 실패 8가지(대신 할 일 칸은 원문 축약, 의미 동일)·기억할 한 문장, §06 추적 사슬 8단계. 첫 주 일정은 권장 일정이 아닌 예시로 서술(#51 준수).
### 미해소
- (없음)

## 10장 (라운드 1)

### ❌ 정정
- Sakib 외 81.1% `(사실 확인 필요)` 해소: "기존의 자동 검사와 사람 리뷰가 통합 전에 놓친 비율이 81.1%였다(사실 확인 필요: …)" → "유출된 실제 비밀 가운데 81.1%를 기존의 자동 검사와 사람 리뷰가 통합 전에 잡아내지 못했다" — 근거: arXiv 2607.12428 초록 직접 확인 "existing automated and human review processes fail to detect 81.1% of these credentials prior to integration"(these = genuine leaked secrets). 분모는 유출된 실제 비밀. 뒤 문장 "누가 썼든" → "누가 넣었든"(비밀을 넣은 주체에 맞춤)
- Sakib 외 82.3%: "38.9%에서 … 그중 82.3%가 공급망 무결성 문제" → "탐지된 보안 스멜의 82.3%가 공급망 무결성 문제" — 근거: 같은 초록 "supply chain integrity issues accounting for 82.3% of all detected security smells". "그중"이 38.9%의 PR을 가리키는 것으로 읽힘
- Octoverse: "코딩 에이전트로 만든 PR이 100만 건" → "자사의 Copilot 코딩 에이전트 … 이 에이전트로 만든 PR이 100만 건 … 한 제품의 다섯 달치 숫자다" — 근거: github.blog Octoverse 2025 원문 직접 확인, 직전 문장 "GitHub Copilot coding agent went from demo to GA"에 이어 "A first glimpse of coding agent shows 1+ million pull requests…". 코딩 에이전트 일반이 아니라 Copilot coding agent 한 제품의 수치
### ⚠️ 약화·삭제
- "커뮤니티에서 자주 인용되는 정리가 있다" → "커뮤니티에서 눈에 띄는 정리가 하나 있다" — mkw5053(HN 48413629) 댓글 하나뿐, "자주 인용"의 근거 없음
- W-B1 비결정적/결정적 단락 끝의 "(영어 원문은 요약 모델을 거쳐 수집했으므로, 인용 전 원문 대조가 필요하다)" 삭제 — code.claude.com/docs/en/best-practices 원문 직접 대조로 모두 확인(비결정적/결정적 정의, "adding emphasis … belongs in a hook", "If something has to happen every time, make it a hook, a deny rule, or a managed setting. CLAUDE.md is for guidelines, and Claude is allowed to decide a guideline doesn't apply.", "Who has the last word" 표 행). 저술용 메모라 final에 남기지 않음
### 🕒 신선도
- (없음 — Claude Code 모범 사례 2026-10 기준, Spracklen "논문이 평가한 시점의 모델 기준" 표기 이미 있음)
### ✅ 확인 (요약)
- 원전 §09 대조 8건(다섯 칸 흐름과 목적 문장, 영향 매트릭스 "취소 가능 시점 변경"·"내부 리팩터링/무의미한 문서 수정 강제 금지" 행, 설계 PR 승인 항목·큰/작은 변경, 코드 PR 확인 항목, "임의로 확정하지 않는다", 분담표 5행, CI 초록색의 정확한 의미, 출시 연결·복구 계획) — research/primary 원문과 일치
- 논문 4건: Sakib 외(KDD 2026 AgenticSE, 4,022건, 38.9%, 99.6%, 67.6%) arXiv 초록 직접 확인 / Spracklen 외(USENIX Security 2025, 16종, 576,000개, 5.2%·21.7%, 205,474개) / Sharma ContextCov(88.3% vs 67.0% vs 50.3%, SWE-bench Lite 300) / Yan(481개, 약 4~16%, 4.4% CI 2.6~6.7%, "write-only channel") — papers.md와 일치, 프리프린트·단독 저자 hedge(§7 #7) 충족
- 웹 2건: 토스테크(김용성, 2026-02-26, 플러그인·마켓플레이스·main 커밋 훅 예, 린터 비교 인용) — web.md D1과 일치 / Octoverse(정정 외 기간 2025-05~09·100만+ 확인)
- 커뮤니티 6건: claude-code #2544(2025-06-24, 원문 인용 2구절), Milofax 댓글(2026-01-20, "recommendations", "Hooks' hell"), mkw5053(2026-06-05, "types -> lint rules -> tests -> md"), andersco(린트·테스트가 CLAUDE.md 손질보다 효과적), Garlef(고치는 법을 담은 린트 에러), HN 47911524(2026-04-26, grey-area가 옮긴 원 글 문장·guluarte 댓글) — community.md와 일치. 오프닝 사례는 "원 글 세부 경위 미확인·커뮤니티 글"로 hedge 유지
- §7 단정 금지 #47("에이전트가 비밀을 유출한다") — 67.6% 사람 비율과 함께 제시되어 충족
### 미해소
- (없음)

## 15장 부록 (라운드 1)

### ❌ 정정
- B-6 `(사실 확인 필요)` ×2(역할별 서브에이전트 정의, Claude Code·Codex) → Claude Code "`.claude/agents/`의 마크다운 파일, YAML 머리말에 `name`·`description` 필수" / Codex "`.codex/agents/`의 TOML 파일(에이전트 하나당 파일 하나), `name`·`description`·`developer_instructions` 필수" — 근거: code.claude.com/docs/en/sub-agents, learn.chatgpt.com/docs/agent-configuration/subagents.md (2026-10-28 조회).
- B-6 Codex 스킬 "`.agents/skills/` (2차 출처)" → "`.agents/skills/` (작업 디렉터리부터 저장소 루트까지 탐색)" — 근거: learn.chatgpt.com/docs/build-skills.md 공식 문서로 1차 확인.
- B-6 Codex 훅 "`.codex/hooks.json` (2차 출처)" → "`.codex/hooks.json` 또는 `.codex/config.toml`의 `[hooks]`" — 근거: developers.openai.com/codex/hooks 공식 문서(프로젝트 `<repo>/.codex/hooks.json`·`<repo>/.codex/config.toml` 인라인 `[hooks]`, 웹 검색 요약 경유) 확인. 단정 금지 #26 해소.
- B-6 Claude Code 플랜 모드 "(`/plan` 등, 조작법은 검색 요약 경유라 재확인 필요)" → "(`Shift+Tab` 순환, 프롬프트 앞 `/plan`, `claude --permission-mode plan`)" — 근거: code.claude.com/docs/en/permission-modes 원문 재대조 ("Enter plan mode by pressing `Shift+Tab` or prefixing a single prompt with `/plan`."). 단정 금지 #24의 조작법 부분 해소("플랜 모드는 그냥 프롬프트"는 원고에 없음).
- 부록 머리말 "템플릿·프롬프트·체크리스트는 … 그대로 옮겼다" → 대상에 첫 주 일정표·흔한 실패 표를 더하고 "그 밖의 목록과 설명 문장은 뜻을 바꾸지 않고 끝맺음만 이 책의 문체로 맞췄다"를 추가 — 근거: primary 대조 결과 D-4(30분 빠른 시작)·D-1/D-2 끝 문단·B-1·B-5 뒤 문장은 합쇼체→평어체로 바뀌어 "그대로"가 사실과 달랐음.
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- B-6 머리 문장 "이 책의 기준 시점(Claude Code 2.1.312, Codex CLI 0.165.0)에서 확인한 범위" → "…에 두 도구의 공식 문서로 확인한 범위다. 쓰기 전에 공식 문서를 다시 확인하자".
### ✅ 확인 (요약)
- 스크립트로 primary 원문과 정규화 대조: A-1 머리말·A-2 본문 구성·A-3 수용 기준·A-4 검증 기록 템플릿, B-2~B-5 프롬프트 1~4 전문, C 18항목 체크리스트 전 항목, D-3 첫 주 일정표 5행, D-5 흔한 실패 8행 — 모두 원문과 글자 단위 일치. C·D-3 인용 블록 문장도 원문 일치.
- D-1·D-2 목록, D-4 30분 5단계, 부록 E의 ID·경로(202 접수, `ReservationCancellationCompleted.v1`, `architecture/contracts/cancellation.yaml`, "취소 처리 중"/"취소 완료", product brief = spec 첫 페이지, 추적 8단계) — primary와 의미 일치.
- B-6 기타: CLAUDE.md 200줄 이하 권장·`@AGENTS.md` 임포트(code.claude.com/docs/en/memory 재대조), Codex AGENTS.md 디렉터리당 1개·32 KiB(W-B4), 버전 2.1.312/0.165.0(W-A3) 일치.
### 미해소
- (없음)

## 04장 (라운드 1)

### ❌ 정정
- "원전은 이 흐름이 '한 번만 통과하는 폭포수 절차가 아닙니다'라고" → "원전은 §01에서 설계 흐름 전체를 두고 '…'라고" — 이 문장은 §03 여섯 단계가 아니라 §01의 문제→규칙→증거→수직 기능→학습 흐름에 붙은 말 (원전 §01)
- 단계 1·3 종료 조건 인용의 어미 "설명할 수 있다"/"기한이 있다" → 원전 그대로 "설명할 수 있습니다"/"기한이 있습니다" — 따옴표 인용은 원문 일치 (원전 §03)
- Chatlatanagulchai 외: "지시 유형별로 보면 테스트 절차가 75.9%…" → "표본 파일의 지시 내용을 유형별로 분류 … 테스트 절차 지시가 들어 있는 파일은 75.9% …" — 분모는 지시 수가 아니라 파일. 논문 Table 3이 "the proportion of agent context files containing instructions for each category"로 정의하고, 분류는 2,303개 전체가 아니라 선별 표본에서 했다 (arXiv 2511.12884 HTML 본문 확인, 2026-10-28; 표본 크기 332는 요약 경유라 본문에 넣지 않음)

### ⚠️ 약화·삭제
- Grynets 외 "대표 실패" → "대표 실패(초록의 표현은 modal failures)" — 수치 50→42→36과 세 조건(요구 없음/ASVS/다층 보안 모델), 테스트 221개는 초록과 일치. 다만 "modal"의 정확한 정의(반복 실행 최빈값인지)는 PDF 본문을 열지 못해 확인 못 함 → 원어 병기로 오독 방지 (arXiv 2606.00167 초록 확인)

### 🕒 신선도
- Kiro "공식 문서는 … Design-First를 권한다" → "공식 문서(2026-10 기준)는" (W-C3, 문서 갱신 2026-08~10)

### ✅ 확인 (요약)
- CAN 원전 자료: product-brief 블록·NFR 표 3행·"위험이 작은 항목은 합치고…"·"AI가 제안한 숫자를…"·목표치 승인 순서·프롬프트 1 규칙·단계 1 검토자 — 원전 §03·§04·§10과 글자 그대로 일치. 책이 만든 그림 1·CAN 프롬프트 예시는 "(책이 그림)", "(예시, 미실행)"으로 표시됨
- 외부 주장 9건: Spec Kit v1.2.4 명령(W-C2), Kiro 두 흐름·steering product.md(W-C3), Harper Reed 2025-02-16·spec.md·"step 2" 성패·"one question at a time"(W-E1), Claude Code Best practices SPEC.md 인터뷰·새 세션(W-B1), Ubl 2020 non-goals(W-F3), BonanKou·joegibbs(C-패턴7·4), Ambig-SWE ICLR 2026 최대 74%(P-24) — 레퍼런스와 일치
- §7 단정 금지: #51(NFR 예시 수치) 본문이 "권장 기본값이 아니다"로 처리됨

### 미해소
- (없음)

## 05장 (라운드 1)

### ❌ 정정
- `domain/cancellation.md` 블록: "그대로 옮긴다"고 했지만 규칙 문장 어미가 평어("기록한다", "최대 하나다", "전이하지 않는다" 등 12곳)로 바뀌어 있었다 → 원전 그대로 "기록합니다", "최대 하나입니다", "전이하지 않습니다" 등으로 복원. "정상 흐름" → 원전 "정상 상태 흐름" (원전 §06)
- 블록 소개 문장에 "파일 하나로 묶은 배치와 소제목은 책이 붙였다" 추가 — `## 예약 상태`·`## 규칙` 등 소제목과 단일 파일 배치는 원전에 없는 책의 구성 (원전 §06은 표·"도메인 규칙의 원본"·"전이와 권한의 부가 조건"으로 나뉨)

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- (없음 — Anthropic 사례는 이미 "2025년 7월", "당시 도구 기준" 명기)

### ✅ 확인 (요약)
- CAN 원전 자료: REQ-CAN-01 인용, 상태 표, POL/INV 규칙·부가 조건 내용, "화면은 업무 상태를 표현합니다", 도메인 5항목·아키텍처 5항목, §02 원본 예, 프롬프트 2 "미결정은 선택지·장단점·검증 방법으로…" — 원전 §02·§05·§06·§10과 일치. 그림 1·2와 Kotlin 단언 예시, 연동 코드 책임 예시는 책의 것으로 표시됨
- 외부 주장 7건: Anthropic 사내 사례 2025-07-24 Product Design "error states, logic flows, and system statuses"(W-E5), vincentvandeth HN 47135917(C-패턴4), GPTers 제이리 `overtime_order`·인용문(C-패턴4), Endres 외 FSE 2024 nl2postcond Defects4J 64개(P-31), Sun 외 SAIV 2024 Clover 최대 87%·적대적 오답 0(P-30), velog 관찰(커뮤니티 리서처의 관찰로 표시됨) — 레퍼런스와 일치
- §7 단정 금지: #52(404를 표준처럼) 본문이 "이 예제가 고른 방법이고, 정답으로 정해진 코드는 아니다"로 처리됨

### 미해소
- (없음)

## 06장 (라운드 1)

### ❌ 정정
- IETF 표 행 "초안 -07 (2025-10-15) | 422 (SHOULD) | … 최신 -08(2026-10-22)에서 바뀌었는지는 확인하지 못했다" → "초안 -07 (2025-10-15)·-08 (2026-10-22) | 422 (SHOULD) | 두 판 모두 키 누락은 400, 원 요청 처리 중 재시도는 409 (모두 SHOULD)" — -08 원문을 직접 열어 확인: 키 누락 "SHOULD reply with an HTTP 400", 처리 중 재시도 "SHOULD reply with an HTTP 409", 다른 페이로드로 키 재사용 "SHOULD reply with an HTTP 422". 2.2절은 별도로 키를 다른 페이로드에 "MUST NOT be reused"라고 적음. -08은 2026-10-22 게시, Standards Track Internet-Draft, RFC 아님 (ietf.org/archive/id/draft-ietf-httpapi-idempotency-key-header-08.html, -07.html, 2026-10-28 조회). 미결정 표의 "IETF 초안 -07 422"도 "-07·-08 422"로 맞춤. §7 #35 해소
- "원전의 머리말 예시가 가리키는 architecture/contracts/cancellation.yaml" → "원전 §12의 문서 머리말 예시가…" — 해당 경로는 원전 머리말(서문)이 아니라 §12 '공통 문서 머리말' YAML의 references 필드에 있다
- 단계 3 종료 조건 인용 "미결정은 담당자와 기한이 있다" → 원전 그대로 "…기한이 있습니다" (원전 §03)

### ⚠️ 약화·삭제
- "아직 RFC가 아니다. 업계가 하나의 답으로 수렴하지 않았다는 뜻이다" → "이 응답 코드가 표준으로 굳지 않았다는 뜻이고, 표에서 보듯 실제 선택도 갈린다" — RFC가 아니라는 사실만으로 업계 수렴 여부를 추론할 수는 없다. 갈린다는 근거는 표의 세 자료
- `UX-CAN-01` 설명에 "원전은 화면 약속을 따로 적지 않고 AC-CAN-01의 UX 항목에 담아 두었는데, 그 내용을 옮기면 이렇다" 추가 — 원전에서 UX-CAN-01은 추적 표의 "접수와 완료 구분" 한 줄뿐이고, "취소 처리 중/취소 완료", 재방문 조회는 AC-CAN-01의 UX 항목에 있다. 출처를 바로잡아 표시

### 🕒 신선도
- (없음 — Stripe "2026-10 기준", IETF 날짜, 우아한형제들 2026-04-17 이미 명기)

### ✅ 확인 (요약)
- CAN 원전 자료: 계약 체크포인트 표, API-CAN-01·EVT-CAN-01 블록, "HTTP 상태 코드는 이 예제의 선택입니다", "키 기록 정리 후에도…", "outbox는 '정확히 한 번'을…", 추적 사슬 인용, 8단계 추적 표, 미결정 3항목 — 원전 §05·§06과 일치. 시퀀스 다이어그램과 '이 책에서' 열은 책의 것으로 표시됨
- Stripe API 문서(Critical, 직접 재확인 2026-10-28): v1에서 키는 "at least 24 hours old" 뒤 자동 정리될 수 있고, 정리된 키를 다시 쓰면 새 요청으로 처리되며, 재시도 시 `500`까지 포함한 저장 응답을 돌려주고, 파라미터가 다르면 "errors … to prevent accidental misuse", 민감 정보를 키로 쓰지 말라는 권고와 v2 차이 — 본문과 일치. 상태 코드 번호를 "확인하지 못했다"고 적은 것도 사실과 일치 (문서에 번호 없음)
- Outbox / at-least-once: Richardson "The Message relay might publish a message more than once" / "a message consumer must be idempotent"(W-F8)와 원전 §06 문장이 본문 서술과 일치. EVT-CAN-01 "안을 검증"이 확정안이 아니라는 해석도 원문과 맞음
- 외부 기타: Brandur Leach 2017-02-22 "Networks are unreliable"/"uncertain situation"(W-F6), Mäder & Egyed EMSE 2015 71명·24%·50%(P-44, 2차·책의 추론 명시 — §7 #39 처리됨), 우아한형제들 2026-04-17 Swagger→타입·Mock·React Query 훅·테스트, 메타데이터 JSON 요약(W-D2)
- §7 단정 금지: #52 "202·409·404가 표준이라는 뜻은 아니다"로 처리됨

### 미해소
- (없음)

## 07장 (라운드 1)

### ❌ 정정
- 오프닝: "Show HN 스레드에 LambdaLogic이라는 사용자가 남긴 댓글의 첫머리다 … 한 사용자의 경험담이지만" → "LambdaLogic이라는 사용자가 … 자기 도구를 소개하는 Show HN 글을 올리고 덧붙인 댓글의 한 대목이다 … 도구를 만든 사람의 말이지만" — HN API로 원문 직접 확인 (item 49847968, 2026-09-25 UTC, 부모 49847953 "Show HN: Stop shipping AI slop, Executor makes agents prove it works"도 LambdaLogic 작성). 인용 "“Done, all tests pass.” Except they don’t."는 원문과 글자 그대로 일치(곡따옴표 포함). 다만 댓글 첫 문장은 "AI slop in code has a pretty recognizable shape…"라서 "첫머리"가 아니고, 글쓴이는 자기 도구 The Executor의 작성자다. 뒤이은 의역 두 문장("can't reliably tell the difference between what it intended to do and what it actually did", "taking verification authority away from the agent itself")은 원문과 일치

### ⚠️ 약화·삭제
- (없음)

### 🕒 신선도
- "Kiro는 요구사항을 EARS 표기로 쓴다" → "Kiro는 2026-10 기준으로 요구사항을 EARS 표기로 쓴다" (W-C3)

### ✅ 확인 (요약)
- CAN 원전 자료: AC-CAN-01~05의 Given/When/Then 인용 5개, 각 UX·검증 항목 의역, "화면 테스트만으로 권한 검증을 대체하지 않습니다", §02 "테스트가 통과한다고…", §12 수용 기준 템플릿 필드, 프롬프트 4 금지 항목 — 원전 §02·§06·§10·§12와 일치. AC↔규칙·계약 대응표, 세 표기 변환, 채운 AC-CAN-03 템플릿은 "책이 정리/옮긴/채워 넣은 예"로 표시됨
- 논문 3건: Wang·Pradel·Liu ICSE 2026 7.8%·29.6%·6.2%p와 초록 의역(P-11), EvalPlus NeurIPS 2023 80배·26개·19.3~28.9%(P-12), TiCoder IEEE TSE 2024 4 LLM·2 데이터셋·5회 이내 +45.97%p·15명(P-29)
- 웹·커뮤니티: Fowler 2013-08-21 GivenWhenThen, Terhorst-North & Matts(W-F5), Kiro EARS 형식(W-C3), OpenSpec v1.15.0 SHALL+WHEN/THEN(W-C6), Kent Beck 2025-06-25 "disabling or deleting tests"(W-E2), Pragmatic Engineer 소개문 "녹취록 미확인" 명시(C-패턴3 — §7 #11 처리됨), jaemin_ve 2026-03-11 27개 태스크·절반 RED·인용문(C-휴리스틱4), r/AI_Agents 약 5천 줄·Codex+GPT-5.4·계산값→보고값·1M+ 토큰(C-패턴3)

### 미해소
- (없음)
