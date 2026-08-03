# Codex 커뮤니티 리서치 — 검색 2026-08-02 기준

> **독자 전제:** Claude Code로 Agentic Coding을 이미 경험한 개발자. 따라서 "Codex가 뭔지"가 아니라 "내가 알던 것과 뭐가 다른지"에 초점.
>
> **신선도 규칙:** 게시일 6개월 이상 경과(= 2026-02-02 이전) 항목은 `⏳ 오래됨 — 현행 확인 필요`.
> **신뢰 등급:** `[출처 명확]` = 실명/식별 가능 계정 + 재현 로그·수치 포함 / `[익명 주장·확인 필요]` = 익명 단일 진술.
>
> **수집 방법:** HN Algolia API(스토리·댓글 직접 조회), GitHub `openai/codex` Issues API(반응수 정렬), GeekNews 원문, 한국어 블로그. Reddit은 크롤러 차단으로 **직접 접근 실패** — 2차 인용만 존재(§8 참조).

---

## 1. Claude Code → Codex 전환 마찰 (최우선)

### 마찰 1: `/rewind`가 없다 — "대화는 되돌아가는데 코드는 안 돌아간다"

전환자가 가장 크게 부딪히는 지점. Claude Code 사용자는 "되돌리기"를 대화+코드 양쪽으로 학습했는데, Codex의 Esc 되감기는 **대화만** 되돌린다.

- **GitHub Issue #11626** "CLI: Add /rewind checkpoint restore that reverts both chat context and Codex-applied code edits" — 2026-02-12 개설, **👍 192**, 2026-08-02 현재 **open**. `[출처 명확]`
  - 이슈 본문의 재현 절차: "1. Codex CLI에 파일 수정을 요청한다. 2. Esc를 두 번 눌러 이전 사용자 메시지로 되감고 fork한다. 3. 대화는 되감기지만 **이전 파일 수정은 워킹 트리에 그대로 남는다**."
  - 댓글 원문 (archneon, 2026-02-17, 반응 13):
    > "I don't get it. So is there 'rewind' feature in Codex CLI or not? E.g. i am used to Claude code. I can REWIND changes OR conversation OR both. **I don't care about the damn conversation rewind :)** It's important that i can revert / rewind the changes agent made if things go sideways! So is this possible or not? If it is not possible, do not promote double ESC, because reverting conversation is more or less useless."
  - 답변 (Alek2077, 2026-02-17, 반응 **77** — 스레드 최다):
    > "No - the `rewind` or `undo` does NOT exist in Codex CLI. Hence this issue. We really need it."
  - 반대 관점 (suparious, 2026-05-01, 반응 10) — "그건 위생 문제다"는 시각:
    > "When you open codex in a repo, you must start from a clean git tree. This is best practices and proper hygiene. ... at least you can see what it did in your git tree, and simply revert the changes yourself. ... I also always engineer in 'COMMIT but do not PUSH' in the context too. That way I am always the gatekeeper."
  - 관련: gusaidler(2026-02-14, 반응 9) — "This is something I really miss coming from other tools (i.e. Cursor, Claude Code)"
  - **책 활용:** 챕터 오프닝 1순위. "Esc 두 번 눌렀는데 코드가 그대로다"는 순간의 당황이 전환자 공통 체험.

### 마찰 2: 중첩 `AGENTS.md`를 자동으로 안 읽는다 (CLAUDE.md는 읽는다)

Claude Code는 작업 디렉토리에서 위로 올라가며 CLAUDE.md를 모두 로드·연결한다. 모노레포 사용자는 이 동작에 의존해 패키지별 규칙을 나눠 뒀는데, Codex는 그렇게 동작하지 않는다.

- **GitHub Issue #12115** "Dynamically loading nested AGENTS.md" — 2026-02-18 개설, **👍 102**, **open**. `[출처 명확]`
  - 이슈 메타데이터에 **엔터프라이즈 고객 신호가 명시**돼 있다: 고객 `Wix`(제출자 Andrew Ginns, 2026-05-05), 영향 계정 `Stripe LLC`(우선순위 `Must have`, 최근 근거 2026-07-13), 그리고 Clay 언급. → 개인 취향 문제가 아니라 대형 조직 도입 블로커라는 증거.
  - miraclebakelaser(2026-02-18, 반응 11) — AGENTS.md 표준 자체를 근거로 반박:
    > "It's also part of the AGENTS.md standard: '4. Large monorepo? Use nested AGENTS.md files for subprojects... Agents automatically read the nearest file in the directory tree, so the closest one takes precedence.' For example, at time of writing **the main OpenAI repo has 88 AGENTS.md files**."
  - **전환 포기 사유로 직접 언급된 댓글 2건** — 이 책의 핵심 증거:
    - anrooo(2026-05-15): "**This is keeping me from switching from Claude Code**, it's really tough to have pretty well-configured AGENTS.md files everywhere only to have Codex ignore them entirely."
    - leonardo-panseri(2026-06-04): "**Will be staying on Claude Code until this is fixed.** The documentation clearly states that you should open the Codex CLI in the subdirectory if you want AGENTS.md and skills to load, but this is not reasonable for most projects. The agent should be able to work on multiple packages/microservices in the same repo without me having to open one different codex tab for each one."
    - jswny(2026-06-21): "This is a pretty critical feature, how can you possibly support progressive disclosure in a large code base without this? I didn't even realize this wasn't supported."
- **관련 이슈 #13386** "AGENTS.md is silently truncated and instructions near the end ignored" — 2026-03-03, 👍 11, open. `[익명 주장·확인 필요]` — 긴 AGENTS.md의 뒷부분이 조용히 잘린다는 보고.
- **관련 이슈 #28903** "AGENTS.md not loaded from ancestor directories above repo root" — 2026-06-18, open.

### 마찰 3: `~/.codex/AGENTS.md`(글로벌)를 문서대로 안 읽었던 시기 — 지금은 해소

- **GitHub Issue #8759** "CLI fails to read AGENTS.md from the global location by default" — 2026-01-05 개설, **2026-01-07 closed** (이틀 만에 종결). `[출처 명확]` ⏳ 오래됨 — **이미 해결됨으로 판단, 현행 재확인 필요**
  - 보고자 인용(codex-cli 0.77.0): "Codex CLI fails to load the AGENTS.md from the global location (`~/.codex/AGENTS.md`) despite it being listed as a valid location [in the docs]. ... I'm forced to spend time telling it where to find it in every new session."
  - 재미있는 건 **에이전트 자신의 자백**이 이슈 본문에 인용돼 있다는 것: "I defaulted to searching only the workspace because I assumed the instruction file would be colocated with the repo and did not expand to the documented global locations unless prompted; that assumption was wrong."
  - **책 활용:** "오래된 불만은 이미 고쳐졌을 수 있다"의 교과서 사례. 2026년 초 블로그 글을 읽고 따라 하면 안 되는 이유.

### 마찰 4: Plan Mode를 기본값으로 시작할 수 없다

Claude Code 사용자 중 상당수는 Plan Mode에서 시작하는 습관이 있다. Codex는 매 세션 수동 전환.

- **GitHub Issue #13942** "Config option to start in Plan mode by default" — 2026-03-08, 👍 34, **open**. `[출처 명확]`
  - Bdthomson(2026-04-06, 반응 4): "**ClaudeCode has had this option for a while now**, having it in Codex would be a nice quality-of-life improvement."
  - bdcdo(2026-07-10): "**Looking forward to switching from claude code to codex** to use GPT 5.6 and this would be a great quality of life improvement to make this switch have less friction."
  - bdcdo가 포크에 레퍼런스 구현까지 올렸다(`[tui] default_mode = "plan"`). 2026-08-02 현재 미머지.

### 마찰 5: 훅(Hooks) 커버리지가 Claude Code와 다르다 — "부분 지원"이 함정

Claude Code에서 훅으로 짜 둔 자동화(품질 게이트, 알림, 권한 인터셉트)를 그대로 옮기면 **일부 이벤트에서만 발화**한다.

- **GitHub Issue #21753** "Full Claude Code Hook Parity (29+)" — 2026-05-08, 👍 22, **open** (엄브렐라 트래커). `[출처 명확]`
  - 이슈 본문의 이벤트 매트릭스에서 상태를 직접 명시: `SessionStart` Shipped / `Setup` **Missing** / `UserPromptSubmit` Shipped / `UserPromptExpansion` **Missing** / `PreToolUse` **Partial** / `PermissionRequest` Shipped / `PermissionDenied` **Missing** / `PostToolUse` **Partial** / `PostToolUseFailure` **Missing** / `PostToolBatch` **Missing** / `Notification` Partial
  - `PreToolUse` 항목의 원문 주석이 핵심 함정: "Coverage must be consistent **across every tool handler, not only selected paths**." → 훅이 "있다"고 문서에 적혀 있어도 모든 경로에서 발화하지 않는다.
  - pmatos(2026-05-11): "Missing the SessionEnd hook atm."
  - 하위 트래커 인덱스(oxysoft, 2026-05-08)에 #2109(완료), #8929(Notify 미발화, open), #11912(커스텀 compaction 훅, open), #14754(PreToolUse/PostToolUse 추가, 완료) 정리돼 있음.

### 마찰 6: 서브에이전트 모델을 개별 지정할 수 없는 시기가 있었다

Claude Code에서 "설계는 큰 모델, 탐색은 싼 모델"로 라우팅하던 습관이 깨진다.

- **GitHub Issue #31814** "GPT-5.6 Sol cannot specify subagent models, forcing all subagents to also be Sol instances" — 2026-07-09, **👍 167**, **closed**. `[출처 명확]`
  - 원인 규명이 이슈 본문에 구체적: GPT-5.6 Sol이 모델 메타데이터로 MultiAgent V2를 선택 → V2가 `hide_spawn_agent_metadata`를 `true`로 기본 설정 → 이름과 달리 **모델 가시 스키마에서 `agent_type`·`model`·`reasoning_effort`·`service_tier` 입력을 제거**. 변경 출처는 PR #26114, 커밋 메시지 "For MAv2 CBv9".
  - 보고자: "Sol's most important use case is as a subagent orchestrator. This setting makes it impossible to use Terra/Luna subagents."
  - 커뮤니티 우회책 (ignatremizov, 2026-07-09, 반응 17) — `~/.codex/config.toml`에 `model_catalog_json`으로 커스텀 카탈로그를 물리고 `multi_agent_version`을 `"v1"`으로 강제:
    ```toml
    model_catalog_json = "~/.codex/models-v1.json"
    [features]
    multi_agent = true
    multi_agent_v2 = false
    ```
  - **관련 open 이슈 #14039** "Allow per-subagent model/provider/profile selection" (2026-03-09, 👍 17) — 근본 요구는 아직 열려 있음.
  - **주의:** closed지만 관련 후속(#34301 "GPT Sol and Terra threads cannot spawn Luna subagents", 2026-07-20, 👍 23, open)이 살아 있어 **현행 확인 필요**.

### 마찰 7: 스킬 메타데이터가 컨텍스트의 2%로 하드코딩 — 스킬 많으면 조용히 잘린다

- **GitHub Issue #19679** "Make skills metadata context budget configurable instead of hardcoded 2%" — 2026-04-26, 👍 31, **open**. `[출처 명확]`
  - 코드 위치까지 특정: `codex-rs/core-skills/src/render.rs`의 `const SKILL_METADATA_CONTEXT_WINDOW_PERCENT: usize = 2;`
  - 실제 경고 문자열: `Warning: Exceeded skills context budget of 2%. Loaded skill descriptions were truncated by an average of N characters per skill.`
  - 실측 데이터 (aldegad, 2026-04-28, codex-cli 0.125.0-alpha.3, macOS): 로컬/프로젝트 스킬 설명만 다듬어 총 페이로드를 **15,822자 → 13,992자**로 줄이자 경고가 사라짐. `[출처 명확 — 단일 환경 측정]`
  - 감정 섞인 반응 (ariccio, 2026-04-28, 반응 4): "Yeah, wait, **WTF**, I need to optimize and heavily prune mine, I know, but **why just truncate them!?**"
  - **관련:** #34328 "Allow repo-committed skills to be opt-in per contributor (**default-off, like Claude Code's @skills-dir + enabledPlugins**)" (2026-07-20, open) — 스킬 배포 모델 자체가 다르다.
  - **관련:** #22943 "Support Claude-style `context: fork` and inline command execution in Codex skills" (2026-05-16, open) — 스킬 문법이 1:1 대응 아님.

### 마찰 8: Claude 설정 마이그레이션 프롬프트가 기존 설정을 덮어썼다

전환자를 정확히 노리는 기능이 전환자를 물었다.

- **GitHub Issue #24515** "Claude settings migration prompt clobbers user-level config.toml when no project-level config exists" — 2026-05-26, 👍 0, **open**. `[출처 명확 — 재현 절차·환경 명시, 다만 단일 보고자]`
  - 환경: Codex CLI 0.133.0, macOS arm64, ChatGPT 로그인.
  - 재현: 프로젝트에 `.claude/settings.json`은 있고 `.codex/config.toml`은 없는 상태에서 "migrate Claude settings" 프롬프트를 수락 → **사용자 레벨** `~/.codex/config.toml`이 수정됨.
  - 증상: `approvals_reviewer = "guardian_subagent"` → `"user"`로 리셋. 결과: "Every subsequent Codex command prompts for user approval (the `guardian_subagent` reviewer had been silently handling routine approvals)."
  - **책 활용:** "전환 버튼을 눌렀더니 승인 지옥이 시작됐다"— 원인이 마이그레이션 자체라는 걸 모르면 영원히 못 찾는다.

### 마찰 9: 없어서 아쉬운 CC 기능들 (요청 이슈 원장)

전부 `openai/codex`에 열려 있는 요청. Claude Code에 있던 것을 찾다 없어서 낸 것들.

| 찾던 것 | 이슈 | 개설일 | 👍 | 상태 |
|---|---|---|---|---|
| 상태 표시줄(status line) | [#17827](https://github.com/openai/codex/issues/17827) | 2026-04-14 | 134 | open |
| `/recap` (Claude-style) | [#18884](https://github.com/openai/codex/issues/18884) | 2026-04-21 | 13 | open |
| `/compact` 요약 가시화·프롬프트 지정 압축 | [#21468](https://github.com/openai/codex/issues/21468) | 2026-05-07 | 13 | open |
| 툴 활동 표시 숨기기 옵션 | [#21252](https://github.com/openai/codex/issues/21252) | 2026-05-05 | 11 | open |
| 컨텍스트/토큰 사용량 표시기 (Desktop에서 제거됨) | [#23794](https://github.com/openai/codex/issues/23794) | 2026-05-21 | 172 | **closed** |
| 사용량 한도 리셋 시 CLI 세션 자동 재개 | [#21073](https://github.com/openai/codex/issues/21073) | 2026-05-04 | 35 | open |

---

## 2. 실사용 경험담 (잘 되는 것 / 안 되는 것)

### 2-1. 압도적 다수 의견: **코드 리뷰는 Codex** — 이건 논쟁이 거의 없다

수집 항목 중 성향이 가장 일관되게 모인 축.

- petesergeant(HN, 2025-12-21) ⏳ 오래됨 `[익명 주장·확인 필요]`:
  > "I have been using Codex as a code review step and it has been **magnificent, truly**. I don't like how it writes code, but as a second line of defence I'm getting better code reviews out of it than I've ever had from a human." — https://news.ycombinator.com/item?id=46347763
- lemming(HN, 2025-12-18) ⏳ 오래됨 `[익명 주장·확인 필요]`:
  > "I have consistently found that Codex does much better code reviews than Claude. Claude will occasionally find real issues, but will **frequently bike shed things I don't care about**. Codex always finds things that I do actually care about and that clearly need fixing." — https://news.ycombinator.com/item?id=46317674
- superfrank(HN, **2026-05-15**) `[익명 주장·확인 필요]` — 신선한 축, 균형 잡힌 평가:
  > "I've been on the codex train for a few months now for personal stuff, but have Claude at work. ... Claude is far better at **front end design**. I think it's still better at **big picture planning**. Codex is far better at **code review and catching bugs that actually matter**. I think it's better at **following directions**, although I think that regressed a bit with 5.5." — https://news.ycombinator.com/item?id=48150929
- bottlepalm(HN, **2026-07-08**) `[익명 주장·확인 필요]` — 3-way 분업:
  > "Currently I use Opus mostly, **Codex for code reviews because it is pedantic**, and Fable for tough problems and high level design." — https://news.ycombinator.com/item?id=48828605
- 국내: bungker (GeekNews 댓글, 2026-04-15): "클로드로 짜고 코덱스로 리뷰하는 것 추천. 시간 걸리지만 회의 전에 걸어두면 완료율 높음"

### 2-2. 실행 스타일 차이: "한 번에 쓰는 작가" vs "정찰 후 패치하는 장인"

가장 구체적인 관찰 기록. **국내 1차 소스로 인용 가치 높음.**

- **AWS 기술 블로그(한국)** — Kyutae Park, Ph.D (AWS AI 스페셜리스트 SA), 2026-06-11. `[출처 명확 — 실명·소속 있음]`
  - https://aws.amazon.com/ko/blogs/tech/codex-claudecode-harness/
  - 관찰: Claude는 "**단일 패스 작성자**" — 정찰 없이 700~800줄을 한 번에 작성. Codex는 "**장인적 접근**" — `pwd`/`ls`로 먼저 정찰한 뒤 `apply_patch`로 쓰고 자가 검증.
  - 요약 문장: "Codex는 에이전트를 개선하는 데 낫고, Claude Code는 에이전트를 실행하는 데 낫다"
  - "Codex는 리뷰 전용 역할에서, Claude는 편집 파트너 역할에서 서로 다른 부분에서 안정적"
  - 교차 리뷰 근거: 다른 모델 계열은 "서로 다른 맹점을 가져" 상대 도구가 못 본 버그를 발견.
  - Codex 차별점으로 **OS 수준 샌드박싱**(macOS Seatbelt, Linux bwrap+seccomp)을 지목.

### 2-3. 조용함(silence)이 낯설다 — 위임 모델의 체감

- Naresh B A, "I Switched from Claude Code to Codex. Here's What Surprised Me." (Medium, 2026-07) `[익명 주장·확인 필요 — 개인 블로그, 수치 없음]`
  - Claude Code는 "continuous progress updates"를 주는데 Codex는 **조용히 일한다**. 워크플로 재적응 필요.
  - 동일 워크플로에서 Codex가 한도 도달 전 "noticeably more work"를 끝냄 (조건·측정 방법 불명).
  - Codex는 "much less attention"을 요구해 병렬 작업이 가능해졌다.
  - 반대로 Claude Code의 "skills, sub-agents, project instructions" 생태계가 몇 달 써 보니 잘 다듬어져 있었고, Codex는 그 스캐폴딩이 덜 성숙하다고 느낌.
  - https://medium.com/@phoenixarjun007/i-switched-from-claude-code-to-codex-heres-what-surprised-me-facaab06a2e6

### 2-4. 안 되는 것: 지시 없이는 탐색을 게을리한다는 반대 보고

§2-2와 정면으로 어긋난다. 병기 필요.

- chandureddyvari(HN, 2026-02-03) `[익명 주장·확인 필요]`:
  > "Codex feels **lazy** - I have to explicitly tell it to research existing code before it stops giving hand-wavy answers. **Doc lookup is particularly bad**; I even gave it access to a Context7 MCP server for documentation and it barely made a difference. The personality also feels off-putting, even after tweaking the experimental flag settings to make it friendlier. For people suggesting it's a skill issue: I've been using Claude Code for the past 6 months and I **genuinely want to make Codex work** - it was highly recommended by peers and friends." — https://news.ycombinator.com/item?id=46866331
- **책 활용:** "커뮤니티가 하나의 목소리로 말하지 않는다"의 좋은 예. 같은 도구를 두고 "정찰을 먼저 한다"와 "정찰을 안 해서 답답하다"가 공존.

### 2-5. 잘 되는 것: 지시 준수(instruction following)

- GeekNews 번역글 "Claude Code(~100시간) vs. Codex(~20시간) 비교" (2026-04-15, 원문 Reddit r/ClaudeCode). `[2차 인용 — 원 게시자 익명, 확인 필요]`
  - https://news.hada.io/topic?id=28538
  - 원문 주장: Claude Code(Opus 4.6)는 "마감에 쫓기는 엔지니어" 같고 CLAUDE.md를 무시하는 경향, 작업 미완료 경향. Codex(GPT-5.4)는 "5~6년차 주니어/시니어" 같은 신중함, **3~4배 느리지만** 품질 우수, "**AGENTS.md를 무시하는 것을 한 번도 목격하지 못함**".
  - ⚠️ 이 주장은 **Codex 서브레딧/Claude 서브레딧 편향** 가능성이 있고 모델 버전(Opus 4.6 / GPT-5.4)이 2026-08 기준 구버전. 지시 준수 우열은 버전마다 뒤집힌다는 반대 증거가 §4에 있음.

### 2-6. 안 되는 것: "완료했다"는 환각 (양쪽 다 있음)

- GeekNews "Claude와 몇 달간 씨름한 뒤 Codex는 바이브 코더의 꿈처럼 느껴짐" (2026-05-17, 원문 Reddit r/codex). `[2차 인용 — 확인 필요]`
  - https://news.hada.io/topic?id=29576
  - 원문 주장: Claude 3개월 사용 후 대규모 프로젝트에서 신뢰성 저하, 토큰 낭비, 과도한 감시 필요. 특히 "**실제 구현이 약 40%인데 완료됐다고 환각**"하는 문제.
  - 한국 댓글 kaydash: "실제 구현이 약 40%인데 완료됐다고 환각하거나 **stub/placeholder 주변에서 과도한 자신감**을 보임"에 강한 공감.
  - 한국 댓글 skageektp의 자기검증 지적: "Codex는 Reddit 서브레딧이라 편향된 평가일 가능성" — **커뮤니티가 스스로 편향을 경계한 사례로 인용 가치 높음.**

---

## 3. 함정·pain point

### 3-1. 승인/샌드박스 — Codex는 OS 샌드박스가 기본이라 CC와 마찰 지점이 다르다

- valleyer(HN, 2026-02-01) — 동작 모델을 정확히 설명한 댓글. `[익명 주장·확인 필요, 다만 문서와 정합]`
  > "commands that you approve get to run **without** the sandbox. The point is that Codex can (by default) run commands on its own, without approval (e.g., running `make`), but they're **subject to the imposed OS sandbox**. This is controlled by the `--sandbox` and `--ask-for-approval` arguments." — https://news.ycombinator.com/item?id=46846201
- quotemstr(HN, 2026-02-20): "One decent approach (which Codex implements) is to run these commands in a **read-only sandbox without approval** and let the model ask your approval when it wants to run outside the sandbox. You want something like `codex -a read-only -s on-failure` (**from memory: look up the exact flags**)" — 본인이 플래그 부정확을 인정. https://news.ycombinator.com/item?id=47095404
- **플래그 이름 대응** (전환자가 헷갈리는 지점, 여러 댓글에서 반복 확인):
  - Claude Code: `claude --dangerously-skip-permissions`
  - Codex: `codex --dangerously-bypass-approvals-and-sandbox`
  - 출처: fragmede(HN, 2025-12-01) ⏳ https://news.ycombinator.com/item?id=46105489, pxc(HN, 2026-04-16) https://news.ycombinator.com/item?id=47794968
- 극단적 실사용 (embedding-shape, HN, 2026-02-19) `[익명 주장·확인 필요]`:
  > "Who has time for that? This is how I run codex: `codex --sandbox danger-full-access --dangerously-bypass-approvals-and-sandbox --search exec \"$PROMPT\"`, having to approve each change would effectively destroy the entire point of using an agent. **Edit: obviously inside something so it doesn't have access to the rest of my system**" — https://news.ycombinator.com/item?id=47076977
- 중간 지대 설계 (miki123211, HN, **2026-07-14**) — 가장 실용적인 정리:
  > "There's a spectrum between a restrictive sandbox and full YOLO mode. ... You can **poke specific holes in the sandbox** (E.G. my Codex one can write to `~/go`, `~/.cache` and `~/.cargo`). You can have **explicit deny rules** that hard-deny and bypass the sandbox and auto-approval. You can allow certain commands to bypass sandbox execution entirely." — https://news.ycombinator.com/item?id=48904705

### 3-2. macOS 샌드박스/격리 속성 때문에 `rg`가 막힌다

- **GitHub Issue #28190** "rg is blocked by macOS" — 2026-06-14, **👍 79**, **open** (Codex CLI 0.139.0, macOS). `[출처 명확 — 원인·해결책 재현됨]`
  - 원인 규명 (pawaca, 2026-06-15, 반응 26): Codex가 번들 바이너리 `/opt/homebrew/Caskroom/codex/0.139.0/codex-path/rg`를 먼저 해석하는데, 그 바이너리에 `com.apple.quarantine` xattr이 붙어 매 호출마다 macOS 경고 발생 — "Apple could not verify 'rg' is free of malware…"
  - 커뮤니티 해결책: `xattr -d com.apple.quarantine /opt/homebrew/Caskroom/codex/0.139.0/codex-path/rg`
  - ⚠️ 스레드에 노이즈(iTerm vs Ghostty 논쟁) 다수. 그리고 backnotprop의 반박 인용: "the issue still occurs in ghostty. it is not a fix" — **터미널 교체는 해결책이 아니다.**

### 3-3. Windows는 사실상 WSL 전제 — 네이티브에서 승인 폭탄

세 개 이상의 독립 진술에서 반복된 패턴.

- jatora(HN, 2025-10-21) ⏳ 오래됨 `[익명 주장·확인 필요]`:
  > "to fix having to approve commands over and over - **use windows WSL**. codex does not play nice with permissions/approvals on windows. WSL solves that completely" — https://news.ycombinator.com/item?id=45652086
- mock-possum(HN, 2025-11-19) ⏳ 오래됨 — 그런데 WSL이 새 문제를 만든다:
  > "My issue with codex is needing to run it in wsl in windows, due to it **spamming confirmation requests for running even the safest of commands** (eg list directory contents, read file, git status) which in turn adds an **extra layer of complexity hooking it up via MCP** to anything running in windows outside of wsl (like say figma). In Claude on the other hand, **MCP connections really do seem to 'just work'**" — https://news.ycombinator.com/item?id=45981432
- 3371(HN, 2026-03-02) `[익명 주장·확인 필요]`: "Codex on Windows. They are known to be very inefficient using only Powershell to interact with files, unless put in WSL. They tend to **make mistakes and have to retry with different commands**." — https://news.ycombinator.com/item?id=47215741
- laurels-marts(HN, 2026-04-19): "the official docs even mention that if you're on Windows you should run Codex CLI via WSL. Meaning, it's specifically designed for unix systems." — https://news.ycombinator.com/item?id=47822774
- **GitHub Issue #13762** "Windows desktop in WSL mode uses the Windows `CODEX_HOME` inside WSL and creates/stores worktrees on `/mnt/c` instead of the WSL filesystem" — 2026-03-06, 👍 55, **open**. `[출처 명확]` → WSL 권장을 따라도 경로 문제가 남는다.
- **GitHub Issue #20214** "Codex App frequently freezes/stutters on Windows 11 Pro despite sufficient system resources" — 2026-04-29, 👍 77, open.
- **GitHub Issue #16717** "feat: configurable Windows agent shell (powershell/git-bash)" — 2026-04-03, 👍 35, **closed**(반영됨) — Windows 상황은 개선 중.

### 3-4. 사용량·한도 — 방향이 뒤집힌 시기가 있다

**이 축은 시점 의존성이 가장 크다. 어떤 수치도 날짜 없이 인용하면 안 된다.**

**(a) 2026년 상반기 지배적 서사: "Codex 한도가 훨씬 넉넉하다"**
- jsLavaGoat(HN, 2026-04-22) `[익명 주장·확인 필요]`: "I can easily hit the weekly limit on Claude even on the $200 plan. **I have yet to ever hit a rate limit on Codex $100.** And the results are almost as good." — https://news.ycombinator.com/item?id=47858803
- esperent(HN, 2026-04-29) `[익명 주장·확인 필요 — 체감 배수, 측정 조건 불명]`: "I get **way more out of the codex $100 plan than I was getting out of the Anthropic $200. Like, probably 2x at least.**" — https://news.ycombinator.com/item?id=47943536
- nsingh2(HN, 2026-06-12): "these days use Codex more **because of the usage limits**" — https://news.ycombinator.com/item?id=48510668
- 한국: helloppfm (GeekNews 댓글, 2026-05-17): "Claude Code는 거의 안 씁니다. Codex가 더 잘하는 것 같기도 하고, **결정적으로 토큰이 원체 줄지가 않습니다.**"
- 한국(⏳ 2026-02-14): velog "Claude Code와 Codex를 알아보자" — Figma 클로닝 작업 실측 인용 "Claude Code 약 623만 토큰, Codex 약 150만 토큰". `[2차 인용·조건 불명 — 어떤 프롬프트/모델/설정인지 미기재. 인용 시 반드시 조건 불명 명시]` https://velog.io/@lovegood/Claude-Code%EC%99%80-Codex%EB%A5%BC-%EC%95%8C%EC%95%84%EB%B3%B4%EC%9E%90

**(b) 2026-06-16 전후 역전 사건 — "레이트 리밋 단가가 10~20배 뛰었다"**
- **GitHub Issue #28879** — 2026-06-18, **👍 362, 💬 210**, **2026-08-02 현재 open**. 이 리서치에서 발견한 **가장 정량적이고 신뢰 높은 항목**. `[출처 명확 — 세션 로그 기반, 대조군 제시, 대안 가설 배제]`
  - 보고자 환경: Codex Desktop / Windows 11 / `gpt-5.5` / `service_tier="default"` / plan=`plus`(`rate_limits.plan_type`으로 확인) / 설정 불변.
  - 측정: 세션 로그의 `token_count`·`rate_limits` 이벤트 직접 비교.

    | 날짜 | 입력 토큰 | 리즈닝 토큰 | 5시간 한도 소모 |
    |---|---|---|---|
    | 06-12 06:51 | 57,112 | 3,645 | 9%→11% |
    | 06-12 06:54 | 79,961 | 5,125 | 15%→16% |
    | 06-18 07:22:30 | 20,480 | **0** | **45%** |
    | 06-18 07:22:50 | 23,839 | **0** | **77%** |

  - 보고자가 **배제한 대안 가설**을 명시한 점이 신뢰도를 크게 올린다: 리즈닝 강도 아님(토큰이 오히려 감소), 컨텍스트 팽창 아님(57~80K→18~23K로 감소), 설정 변경 아님, 주간 캡 아님.
  - 독립 재현 (andr3sdr, 2026-06-19, 반응 17, **Pro 20x**): "Before this change, **I was never able to exhaust my 5-hour allowance**, even during heavy Codex usage sessions involving large codebases and long-running tasks. Since yesterday, the same workflows are consuming the entire 5-hour budget in **roughly one hour**."
  - 한국 사용자 재현 (MDGChamomile, 2026-06-18, 반응 17, Plus/CLI/Linux): "After a single simple conversational interaction, my 5h limit dropped from approximately 99% remaining to '67%'. ... Approximate time: 2026-06-18 22:20~30 **KST**"
  - 전환 반전 (Aesthermortis, 2026-06-19, 반응 20): "**I had to switch to Claude**; now Codex seems like a more aggressive Claude 🤣. Now I feel like Claude doesn't use any resources. **Codex is unusable today.**"
  - 계정 표시 이상 (StrumykTomira, 2026-06-18, 반응 13) `[익명 주장·확인 필요 — 계산 오류 의심을 본인도 표명]`: "my profile shows, for example, **22-26 MILLION (!) tokens used**. And I have reasoning set to Low or, at most, Medium. ... **I think they're being calculated incorrectly.**"
  - **책 활용 (강력):** "한도가 넉넉하다"는 커뮤니티 통념이 이틀 만에 뒤집힌 기록. 요금·한도 서술은 반드시 날짜를 박아야 한다는 근거.
- 관련: **#14593** "Burning tokens very fast" (2026-03-13, 👍 282, **💬 627**, open), **#13568** "Usage dropping too quickly" (2026-03-05, 💬 325, closed) — 토큰 소모 불만은 상시 이슈.
- 관련: **#34035** "Make the temporary removal of the 5-hour usage limit permanent" (2026-07-18, 👍 131, open) → **2026-07 시점에 5시간 한도가 일시적으로 해제된 기간이 있었음**을 시사. 현행 확인 필수.
- 반대 관점 (satvikpendem, HN, 2026-07-08) — 구조적 설명 `[익명 주장·확인 필요 — 추정]`: "It's because Anthropic doesn't have capacity while OpenAI does. ... It is why Codex has much higher, almost unlimited limits, while Claude Code rate limits hourly and weekly much more." — https://news.ycombinator.com/item?id=48829605

### 3-5. 질문이 60초 뒤 자동 응답된다 — CC 사용자가 절대 예상 못 하는 동작

- **GitHub Issue #28969** "Add setting to disable the auto-resolve in 60 seconds for questions" — 2026-06-18, **👍 186**, **open** (codex-cli 0.141.0). `[출처 명확 — 재현 절차 명시]`
  - 재현: "1. Go to plan mode 2. Write a plan prompt that will make Gpt to ask you a question 3. Notice you have a **60 second delay** to answer the question" → 답 안 하면 Codex가 **권장 답을 자동 수락**하고 진행.
  - ScyDev(2026-06-28, 반응 **58**): "**Who thought this was a good idea to auto enable for everyone?**"
  - gergo-hortobagyi(2026-06-24, 반응 57): "This is a **blocker** for everyone using Codex for proper planning and production level development and **renders the `request_user_input` tool completely useless**. The only solution now is **downgrading to 0.140.0**."
  - irm-codebase(2026-06-28, 반응 41): "If your project has high complexity, 60 seconds is simply too little. ... I'd honestly prefer an option for the tool to **fail** rather than the bot merrily implementing changes I did not request."
  - **책 활용:** 챕터 오프닝 후보 2순위. "잠깐 커피 타러 간 사이 Codex가 알아서 결정했다."

### 3-6. 로컬 디스크·리소스 사고 (버전 특정)

- **#28224** "Codex SQLite feedback logs can write ~640 TB/year and rapidly consume SSD endurance" — 2026-06-14, **👍 449**, **closed**. `[출처 명확 — 다만 수치는 연간 환산 추정치]` ⚠️ 인용 시 "연 환산 추정" 명시 필요. https://github.com/openai/codex/issues/28224
- **#25719** "Codex Desktop for macOS repeatedly triggers `syspolicyd`/`trustd` CPU and memory runaway" — 2026-06-01, 👍 386, **open**.
- **#20880** "App silently creates empty `~/Documents/Codex` folder on every launch" — 2026-05-03, 👍 40, open.

### 3-7. 컨텍스트 창 — 광고와 체감의 괴리

- **#32806** "🚨 [SEVERE REGRESSION] GPT-5.6 Sol context cut again: 353K → 258K **despite advertised 1.05M**" — 2026-07-13, 👍 54, **closed**. `[출처 명확 — 제목이 수치 명시]`
- **#19464** "Support 1M token context for GPT-5.5 in Codex" — 2026-04-24, 👍 168, open.
- **#18498** "Fresh-thread token usage is **massively inflated by enabled plugins/skills/apps** in Codex Desktop" — 2026-04-18, open → 스킬을 많이 깔면 새 스레드부터 컨텍스트가 먹힌다.

### 3-8. 보안·데이터 반출 함정 — "레포가 통째로 OpenAI 인프라로 올라갔다"

- HN 스토리 "Asked Codex to redesign a page; it pushed my repo to OpenAI infra" — 2026-07-24, 31 pts, 26 comments. 원문 blog: bhanu.io. `[출처 명확 — 다만 단일 사례, 본인도 승인 프롬프트가 있었음을 인정]`
  - https://news.ycombinator.com/item?id=49037941
  - **원 보고자 본인의 정정**(aarondong의 지적에 대한 npmn의 답, 2026-07-24): "Codex did surface permission prompts for the add, commit, and push. **It didn't run them fully invisibly.** So — didn't I approve this?" → 승인 프롬프트는 떴다. 문제는 **무엇을 승인하는지 몰랐다**는 것.
  - 커뮤니티 진단 (throwitaway222, 2026-07-24): "There are now a lot of **baked in skills** that simplify deployment for people that don't understand deployment. ... Since skills are 'instructions' and making a skill a default, it makes sense that **YOU didn't ask for this, but the skill did.**"
  - 동조 (npmn, 원저자): "it felt like codex was **pushing to my git repo** - I said yes, then quickly realised what was already done."
  - 반대 관점 (applfanboysbgon): "Your repo was on OpenAI infra the moment you let Codex read it." / 원저자 반박: "I know the difference between AI reading **selected part** of the code to get the context and a **git sync**."
  - 가장 균형 잡힌 정리 (gruez, 2026-07-24):
    > "if you let loose a coding agent in a project, you should assume it can read everything. ... That said, AI companies still shouldn't be intentionally building features that upload code wholesale because it **betrays the users trust**. It's like if you hired a cleaner and the first thing it did was go to every room and opened every closet/cabinet."
  - ⚠️ **이 사례는 원 블로그 글 자체가 AI로 상당 부분 작성됐다고 저자가 인정**했다("I used claude to reason about the jsonml file - redact personal information and also to write big chunks of this"). 인용 시 이 사실을 밝힐 것.

### 3-9. Codex Security CLI — 신제품의 비용 사고 (2026-07-28 출시)

같은 날 HN 최상위(596 pts, 227 comments)에 올라온 신제품. 초기 함정이 그대로 기록됨.
- https://news.ycombinator.com/item?id=49089755 / 저장소 https://github.com/openai/codex-security
- **OpenAI 측 응답자가 스레드에 상주**: dangelosaurus (Michael, Promptfoo 공동창업자, OpenAI에서 Codex Security CLI 작업) — `[출처 명확 — 자기 식별한 벤더 측 인사]`
- 실사용 사고 (gregwebs, 2026-07-28) `[출처 명확 — 로그 붙임]`:
  > "Just ran it on a small repo. It ran for **almost an hour** and then got interrupted. It **drained half my weekly usage on a Pro plan**. ... `codex-security: Could not save the Codex Security scan: **Repository HEAD changed while the scan was running.** Start a new scan.`"
- 벤더 인정 (dangelosaurus, 2026-07-28): "Oof, that's a bad outcome. Half your weekly usage and a 50-minute scan just to get a HEAD error at the end is **not acceptable**. `--max-cost` can help limit estimated spend, but that doesn't fix the underlying problem."
- 유사 사례 (Quai): "It said 'Partial output was kept at <...>', but I don't see a obvious way of picking it up in a new scan? (**The failed run cost me ~$13**)" → 벤더 확인: "You can't yet, unfortunately."
- `--max-cost`도 안전망이 아님 (arpinum, 2026-07-29): "I set `--max-cost` to 100, it bailed before finishing. Unknown if I would get full results for $105 or $500. **Either way I lost $100.**"
- 가드레일 거절 함정 (minraws, 2026-07-28→29): 방어 목적 스캔이 모델 가드레일에 걸려 거절 — "is there a way to not have it waste so many tokens if it fails ... **it burnt over 100+$ of tokens** a good chunk of my weekly limit **for nothing**"
  - 벤더 답변: "The CLI **doesn't do a repository-ownership check**. ... The refusals come from **model guardrails, which can be overly cautious.**" 우회 경로는 Trusted Access for Cyber(TAC1/Daybreak) 별도 승인.
- 데이터 반출 (벤더 확인, dangelosaurus, 2026-07-29): "**this isn't an offline scanner.** The CLI runs locally but the code and context needed for analysis are **sent to the hosted model**. ... If your company doesn't allow source code to leave its environment, you shouldn't run this against that codebase."
- ⚠️ **매우 신선(4일 전)하므로 책 집필 시점에 상태가 바뀌었을 가능성 높음. 반드시 재확인.**

---

## 4. 비교 논쟁 (관점 A / 관점 B 병기)

### 논쟁 A: "협업이냐 위임이냐" — 이 프레임 자체가 커뮤니티의 합의점

양쪽 진영이 서로 다른 결론에 도달하면서도 **문제 정의는 같다**. 이 책의 뼈대로 쓸 만하다.

- **관점 A — 협업 도구가 낫다 (Claude Code):**
  - velog(⏳ 2026-02-14): Claude Code는 "개발자가 루프 안에 있는 인터랙티브한 협업 도구다. 터미널에서 실행되고, 로컬 코드베이스를 깊이 이해하며, **변경 전에 질문을 던진다**." Codex는 "위임하고 떠나는 자율형 에이전트에 가깝다."
  - 같은 글 인용: "Claude가 코드베이스 전체를 읽고 **우리 프로젝트 방식 그대로** 구현해냈다. Codex는 **자기 방식대로** 했다."
  - Naresh B A(Medium, 2026-07): Claude Code의 터미널 워크플로 + 서브에이전트 + 스킬이 자신의 프로세스에 "natural"했다.
- **관점 B — 위임 모델이 낫다 (Codex):**
  - Naresh B A(같은 글, 2026-07): Claude Code는 구현 단계마다 계속 붙어 있어야 했지만 Codex는 "much less attention"을 요구해 **병렬 작업이 가능**해졌다.
  - tunesmith(HN, 2026-06-13) — 위임 루틴의 구체적 형태 `[익명 주장·확인 필요]`: "$100/month codex plan ... 5.5-xhigh all the time. I think of what to do next, have a chat session to determine exactly what to ask for **up to the point of being ready to implement**, and then codex churns on a **commit-sized task** whereupon I briefly check it on my local dev server." — https://news.ycombinator.com/item?id=48519556
- **커뮤니티가 도달한 질문 형태:** "협업할 것인가, 위임할 것인가"로 물으면 선택이 쉬워진다 (여러 비교 글에서 반복되는 프레임).

### 논쟁 B: 지시 준수 — Codex가 낫다 vs 둘 다 못 지킨다

- **관점 A — Codex가 AGENTS.md를 더 잘 지킨다:**
  - GeekNews 28538(2026-04-15) 원문: "AGENTS.md를 무시하는 것을 한 번도 목격하지 못함" `[2차 인용·확인 필요]`
  - Razengan(HN, 2026-03-31): "I love how **seamless and intuitive Codex** is in comparison: `~/AGENTS.md < project/AGENTS.md < project/subfolder/AGENTS.override.md`. Meanwhile Claude doesn't even see that I asked for indentation by tabs and not spaces" — https://news.ycombinator.com/item?id=47583980
  - superfrank(HN, 2026-05-15): "I think it's better at following directions, **although I think that regressed a bit with 5.5**."
- **관점 B — 둘 다 못 지킨다, 기법 논쟁은 헛돈다:**
  - toraway(HN, 2026-02-26) `[익명 주장·확인 필요]` — 가장 냉소적이고 인용 가치 높음:
    > "it's somewhat ironic how this is almost the exact opposite of the prevailing folk wisdom I've read for the last 1-2 years: that you should never use negative instructions with specific details because it overweights the exact thing you're trying to avoid. Given my own experience **futilely fighting with Claude/Codex/OpenCode to follow AGENTS.MD/CLAUDE.MD** with different techniques that each purport to solve the problem, I think the better explanation really is that **they just [don't reliably follow]**" — https://news.ycombinator.com/item?id=47173315
  - 한국: gpdir16 (GeekNews 댓글, 2026-04-15): "**코덱스가 지침 무시하는 경우 많았음.** 최근 Opus 성능 낮춘 듯"
  - pmarreck(HN, 2025-12-01) ⏳ — 강조 문법 무용론: "> 'CRITICAL (PRIORITY 0):' There's no need for this level of **performative ridiculousness** with AGENTS.md (Codex) directives, FYI." — https://news.ycombinator.com/item?id=46106261
- **판정 유보:** 이 논쟁은 모델 버전에 따라 뒤집힌다는 증거가 양쪽에 있음. 책에서는 "버전 X 시점 기준" 없이 서술하면 안 됨.

### 논쟁 C: 어느 쪽 코드 품질이 나은가 — 조건부 결론만 존재

- **관점 A — Codex 코드가 더 낫다:**
  - BloondAndDoom(HN, 2026-03-16): "in my experience codex always writes **better code and more sensible** than Claude (**but slower**)" — https://news.ycombinator.com/item?id=47405533
- **관점 B — GPT는 문제를 잘 풀지만 코드는 더 나쁘다:**
  - bottlepalm(HN, 2026-07-08) — 문제해결력과 코드품질을 분리한 관찰:
    > "GPT 5.5 is a good example of a model that's **generally better at solving problems** than Opus 4.8, but the **code it generates is worse - over engineered, shortcuts**, etc."
- **관점 C — 영역별로 갈린다 (가장 지지 많음):**
  - superfrank(2026-05-15): Claude = 프론트엔드 디자인·큰 그림 계획 / Codex = 코드 리뷰·진짜 중요한 버그 잡기
  - 한국: tangokorea(GeekNews, 2026-04-15): "도메인에 따라 다름. 렌더링은 Claude가 낫지만, **프레임워크 기반 웹앱은 Codex가 정신건강에 좋음**"

### 논쟁 D: CLI 품질 — Claude Code TUI가 버그가 많다는 반대 방향 불만

Codex 쪽 불만만 모으면 균형이 깨진다. 반대 방향도 기록.
- tlonny(HN, 2026-04-09) `[익명 주장·확인 필요]`:
  > "**Bugginess in the Claude Code CLI is the reason I switched from Claude Max to Codex Pro.** I experienced: rendering glitches, replaying of old messages, mixing up message origin, generally very sluggish performance. Given how revolutionary Opus is, its crazy to me that they could trip up on something as trivial as a CLI chat app" — https://news.ycombinator.com/item?id=47703506
- 반대로 pxc(HN, 2026-04-16)는 Codex의 투명성을 칭찬: "Codex seems **much more transparent about what it's thinking and what it wants to do next**. I find it much easier to interrupt or jump in the middle if things are going to wrong direction." — https://news.ycombinator.com/item?id=47794968
- 그리고 Claude가 너무 빨리 실행한다는 불만 (rednb, HN, 2026-04-26): "claude tends to **move too fast and execute commands without asking for permission**. For example, if i ask a question regarding an implementation decision while it is implementing a plan, it answers (or not) and **immediately proceeds to make changes it assumes i want**. Other models switch to chat mode, or ask for the best course of action." — https://news.ycombinator.com/item?id=47914718

### 논쟁 E: 하나만 쓸 것인가, 둘 다 쓸 것인가 — 현장은 이미 "둘 다"로 수렴

관점 대립이라기보다 **커뮤니티가 도달한 실질적 답**. 한국·글로벌 양쪽에서 독립적으로 같은 패턴이 나옴.
- 한국 (GeekNews 2026-04-15 댓글):
  - oneforall88: "**100달러 Claude + 200달러 Codex**로, Opus 계획 → Sonnet 구현 → Codex 리뷰 → 반복 루프 스킬 제작"
  - minhoryang: "**쿼타 널널한 모델에 먼저 배정**하는 방식 사용 중"
  - bungker: "클로드로 짜고 코덱스로 리뷰하는 것 추천"
- 한국 (GeekNews 2026-05-17 댓글): gkhcdef — "codex가 더 토큰도 넉넉하고 claude가 짠 계획이나 코드에 결함을 잘 찾아내서 **아예 갈아탈 생각으로 추가 결제**"했으나 결국 **두 모델을 보완적으로 사용 중**
- 글로벌: bobjordan(HN, 2026-04-18) `[익명 주장·확인 필요 — 규모 큰 자체 시스템, 검증 불가]`: 내부 멀티에이전트 오케스트레이터 4개월 구축, 기본 토폴로지가 구현자+리뷰어 2인조 — "**that usually means Opus writing code and Codex reviewing it.** I just finished a 10-hour run with 5 of these teams in parallel, plus a Codex run manager." — https://news.ycombinator.com/item?id=47817892
- 반론 (skageektp, GeekNews 2026-05-17): "**저만 자꾸 구독을 돌아가면서 하게 되나요?**" — 모델 간 성능 변동성에 대한 피로감. **구독 유목민 피로**는 별도 감정 축.
- 한국 Threads 요약 제목(qjc.ai, 날짜 미상): "코덱스 CLI 다 알려드릴게요. 근데 결론부터 말하면, **갈아탈 필요 없어요. 메인은 여전히 Claude Code입니다.**" `[익명 주장·확인 필요 — 게시일 미확인]`

---

## 5. 현장 노하우

### 노하우 1: 설정 파일을 이중 관리하지 말고 한쪽을 심볼릭/포인터로

- steve-atx-7600(HN, 2026-07-09) `[익명 주장·확인 필요]`:
  > "Set yourself up to be able to try / switch between models easily. I was a claude only user and just have my **user level AGENTS.md for codex and others simply point at my user CLAUDE.md**. Have a **script that syncs my skills (just directories)** between all models. Also, if you want to use `/simplify` or similar from claude in another model, you can **ask claude for the prompt** and put that in a skill for the other models." — https://news.ycombinator.com/item?id=48851396
- 업계 권장 패턴(여러 정리 글 공통): AGENTS.md를 단일 진실 소스로, CLAUDE.md는 AGENTS.md를 import하는 얇은 레이어로. `[2차 정리 — 1차 커뮤니티 진술로는 위 steve-atx-7600 건이 대표]`

### 노하우 2: 샌드박스를 끄지 말고 "구멍을 뚫어라"

- miki123211(HN, 2026-07-14): 전면 YOLO 대신 `~/go`, `~/.cache`, `~/.cargo`처럼 **필요한 경로만 쓰기 허용** + **명시적 deny 규칙**으로 하드 차단. (§3-1 원문 인용)
- 외부 샌드박스로 감싸고 내부는 풀 액세스: embedding-shape(2026-02-19), pxc(2026-04-16, `nono` 사용), kstenerud(2026-06-14, Docker/Podman/containerd/seatbelt/tart 지원 `yoloai`) — https://news.ycombinator.com/item?id=48526736

### 노하우 3: Codex에는 "커밋은 하되 푸시는 하지 마" 를 컨텍스트에 박아라

`/rewind` 부재(§마찰 1)에 대한 커뮤니티의 실질적 대응.
- suparious(GitHub #11626, 2026-05-01, 반응 10):
  > "When you open codex in a repo, you **must start from a clean git tree**. ... I normally start Codex by asking it to have '**research this repository, and when you are ready, let's have a back and forth conversation, before we get started**' or similar. I also always engineer in '**COMMIT but do not PUSH**' in the context too. That way **I am always the gatekeeper** for changes to go into the repository."
- 국내에서도 같은 습관 (brunch, kk2daddy, 2026-03-14): "Claude가 변경하기 전에 항상 git commit, 문제 생기면 `git checkout`으로 롤백" — 도구 무관하게 통용되는 안전장치. https://brunch.co.kr/@kk2daddy/112

### 노하우 4: 태스크를 "커밋 하나 크기"로 쪼개라

- tunesmith(HN, 2026-06-13): 채팅으로 **구현 직전까지** 합의한 뒤 "commit-sized task"를 Codex에 던지고 로컬 dev 서버에서 짧게 확인 → 수정 요청 → 커밋 및 다음 단계 추천 요청. (§4 논쟁 A 인용 참조)
- yummyelephant8(HN, 2026-03-09) `[익명 주장·확인 필요 — 자기 블로그 홍보 성격 있음]`:
  > "You might be able to 1-shot prompt a complex app prompt once, but that's **luck**. To do it reliably, you need to **break your project into subcomponents, build each one separately, then bring it all together**. This isolates bugs so you can build on your projects in the future." — https://news.ycombinator.com/item?id=47316658

### 노하우 5: 교차 리뷰 — 다른 모델 계열은 맹점이 다르다

- AWS 한국 기술블로그(Kyutae Park, 2026-06-11): 다른 모델 계열은 "서로 다른 맹점을 가져" 상대 도구가 못 본 버그를 발견. → 교차 리뷰의 **이론적 근거**로 인용 가능한 국내 실명 출처.
- 실행 형태: Opus 구현 → Codex 리뷰 (bobjordan, GeekNews oneforall88, bungker 등 다수)
- 반론 (BloondAndDoom, HN, 2026-03-16): "many people don't understand that you can **just say 'check again' to the model you use** and it will just find bugs, repeat it until there are no bugs. Sounds stupid but it works. It's intuitive to assume another will help more and better review but yeah I don't know." — 교차 리뷰 무용론. `[익명 주장·확인 필요]`

### 노하우 6: Windows면 WSL을 쓰되, `CODEX_HOME`·워크트리 경로를 확인하라

§3-3 종합. WSL 권장은 광범위한 합의지만 #13762(워크트리가 `/mnt/c`에 생김)를 모르면 성능이 무너진다.

### 노하우 7: 서브에이전트가 커스텀 정의를 못 읽으면 인자를 직접 넘겨 본다

- eiphy(GitHub #15250, 2026-06-06, 반응 2) — **문서에 없는 인자**로 우회 성공 보고 `[익명 주장·확인 필요 — 단일 보고]`:
  ```json
  { "task_name": "search_docs", "agent_type": "search-specialist",
    "model": "gpt-5.4-mini", "reasoning_effort": "medium",
    "fork_turns": "none", "message": "..." }
  ```
  > "And its working. I guess these arguments are **not documented but somehow inside of the tool**."

### 노하우 8: 스킬 설명문을 다이어트하라 (2% 예산)

§3-7·마찰 7. aldegad의 실측(15,822자 → 13,992자로 경고 소멸)이 유일한 정량 기준점. 스킬 카탈로그가 큰 조직은 설명문 길이 자체가 예산이다.

---

## 6. 문서와 어긋나는 현장 보고

**이 섹션은 공식 문서 담당 리서처의 결과와 반드시 대조할 것.** 문서를 믿고 따라 했다가 실패한 보고만 모았다.

| # | 문서가 말하는 것 | 현장 보고 | 출처 | 상태(2026-08-02) |
|---|---|---|---|---|
| 1 | `~/.codex/AGENTS.md`(글로벌)가 유효 탐색 위치 | CLI가 워크스페이스만 뒤지고 글로벌을 안 봤다 | [#8759](https://github.com/openai/codex/issues/8759) 2026-01-05, CLI 0.77.0 | **closed** (2026-01-07) — 해소 추정, 재확인 필요 ⏳ |
| 2 | (AGENTS.md 표준) "가장 가까운 파일을 자동으로 읽고 가장 가까운 것이 우선한다" | Codex는 중첩 AGENTS.md를 자동 로드하지 않는다. 문서는 "서브디렉토리에서 CLI를 열어라"고 안내하는데 모노레포에선 비현실적 | [#12115](https://github.com/openai/codex/issues/12115), leonardo-panseri 2026-06-04 | **open** |
| 3 | 커스텀 서브에이전트는 `.codex/agents/*.toml`에 두고 `name`이 진실 소스, `model`/`model_reasoning_effort` 생략 시 부모 상속 | 툴 백엔드 세션의 `spawn_agent`는 일반 `agent_type`만 받고 **이름으로 커스텀 에이전트를 지정할 방법이 없다**. 유일한 우회는 TOML을 직접 읽어 `developer_instructions`를 주입하는 것 — "That is **not the behavior the docs imply**" | [#15250](https://github.com/openai/codex/issues/15250) 2026-03-20 | **open** (2026-07-12 CLI 0.144.1에서 재현 보고) |
| 4 | Pro는 Plus 대비 "5x or 20x higher rate limits" (공개 요금 문서) | Truck0ff(2026-06-19): 하루도 안 된 주간 창에서 5시간 52%/주간 59% 소진. "The practical behavior now feels **materially inconsistent with that representation** unless there is an undisclosed reweighting/multiplier or mis-accounting bug." | [#28879](https://github.com/openai/codex/issues/28879) | **open** |
| 5 | GPT-5.6 Sol 컨텍스트 1.05M 광고 | 실측 353K → 258K로 축소 | [#32806](https://github.com/openai/codex/issues/32806) 2026-07-13 | **closed** — 회복 여부 확인 필요 |
| 6 | `hide_spawn_agent_metadata`는 (이름상) 메타데이터 출력만 숨김 | 실제로는 `agent_type`·`model`·`reasoning_effort`·`service_tier`를 **모델 가시 스키마에서 제거**하는 기능적 변경 | [#31814](https://github.com/openai/codex/issues/31814) 2026-07-09 | closed |
| 7 | `--max-cost`로 예상 지출 제한 가능 (Codex Security CLI) | arpinum: "I set `--max-cost` to 100, **it bailed before finishing**. ... Either way I lost $100." 벤더도 "that doesn't fix the underlying problem" 인정 | [HN 49089755](https://news.ycombinator.com/item?id=49089755) 2026-07-28 | 초기 버전 |
| 8 | Codex Security CLI는 로컬 CLI | 벤더 확인: "**this isn't an offline scanner** ... code and context ... **sent to the hosted model**" | 동상 | 2026-07-29 벤더 발언 |
| 9 | 훅 이벤트 지원 (문서상 "지원") | `PreToolUse`/`PostToolUse`가 **Partial** — "coverage must be consistent across every tool handler, **not only selected paths**" | [#21753](https://github.com/openai/codex/issues/21753) | **open** |
| 10 | (Codex 문서상 "Claude 설정 마이그레이션") | 프로젝트 레벨 설정이 없을 때 **사용자 레벨** `~/.codex/config.toml`을 덮어씀 → `approvals_reviewer`가 리셋돼 승인 폭탄 | [#24515](https://github.com/openai/codex/issues/24515) 2026-05-26, CLI 0.133.0 | **open** |

---

## 7. 신선도·신뢰도 원장

### 7-1. GitHub `openai/codex` 이슈 (1차 소스 — 신뢰도 최상급)

| 이슈 | 제목(요약) | 개설일 | 👍 | 💬 | 상태 | 신선도 | 등급 |
|---|---|---|---|---|---|---|---|
| [#28224](https://github.com/openai/codex/issues/28224) | SQLite 피드백 로그 ~640TB/년 SSD 마모 | 2026-06-14 | 449 | 154 | closed | 신선 | 출처 명확(수치는 연환산 추정) |
| [#25719](https://github.com/openai/codex/issues/25719) | macOS Desktop `syspolicyd`/`trustd` CPU·메모리 폭주 | 2026-06-01 | 386 | 79 | open | 신선 | 출처 명확 |
| [#28879](https://github.com/openai/codex/issues/28879) | 레이트리밋 단가 10~20배 급등 (6/16~) | 2026-06-18 | 362 | 210 | **open** | 신선 | **출처 명확 — 최상급(로그·대조군·대안가설 배제)** |
| [#30364](https://github.com/openai/codex/issues/30364) | GPT-5.5 리즈닝 토큰 클러스터링(516/1034/1552)과 성능 저하 | 2026-06-27 | 288 | 183 | open | 신선 | 출처 명확(인과는 가설) |
| [#14593](https://github.com/openai/codex/issues/14593) | Burning tokens very fast | 2026-03-13 | 282 | 627 | open | 신선 | 익명 다수 집계 |
| [#11626](https://github.com/openai/codex/issues/11626) | `/rewind` 부재 | 2026-02-12 | 192 | 36 | **open** | 경계선 | 출처 명확 |
| [#28969](https://github.com/openai/codex/issues/28969) | 질문 60초 자동 응답 비활성화 옵션 | 2026-06-18 | 186 | 64 | **open** | 신선 | 출처 명확 |
| [#23794](https://github.com/openai/codex/issues/23794) | Desktop 컨텍스트/토큰 표시기 제거 | 2026-05-21 | 172 | 173 | closed | 신선 | 출처 명확 |
| [#19464](https://github.com/openai/codex/issues/19464) | GPT-5.5 1M 컨텍스트 지원 요구 | 2026-04-24 | 168 | 132 | open | 신선 | 출처 명확 |
| [#31814](https://github.com/openai/codex/issues/31814) | Sol이 서브에이전트 모델 지정 불가 | 2026-07-09 | 167 | 100 | closed | 매우 신선 | 출처 명확(원인 PR까지 특정) |
| [#17827](https://github.com/openai/codex/issues/17827) | 커스터마이즈 가능한 status line | 2026-04-14 | 134 | 36 | open | 신선 | 출처 명확 |
| [#34035](https://github.com/openai/codex/issues/34035) | 5시간 한도 임시 해제의 영구화 요구 | 2026-07-18 | 131 | 12 | open | 매우 신선 | 출처 명확 |
| [#12115](https://github.com/openai/codex/issues/12115) | 중첩 AGENTS.md 동적 로딩 | 2026-02-18 | 102 | 23 | **open** | 경계선 | **출처 명확(Wix·Stripe 기업 신호)** |
| [#28190](https://github.com/openai/codex/issues/28190) | macOS가 `rg` 차단 | 2026-06-14 | 79 | 49 | open | 신선 | 출처 명확(해결책 재현) |
| [#20214](https://github.com/openai/codex/issues/20214) | Windows 11 Pro 프리즈/스터터 | 2026-04-29 | 77 | 84 | open | 신선 | 익명 다수 |
| [#13762](https://github.com/openai/codex/issues/13762) | WSL 모드가 Windows `CODEX_HOME` 사용, 워크트리 `/mnt/c` 생성 | 2026-03-06 | 55 | 27 | open | 신선 | 출처 명확 |
| [#32806](https://github.com/openai/codex/issues/32806) | Sol 컨텍스트 353K→258K (광고 1.05M) | 2026-07-13 | 54 | 27 | closed | 매우 신선 | 출처 명확 |
| [#13942](https://github.com/openai/codex/issues/13942) | Plan mode 기본 시작 옵션 | 2026-03-08 | 34 | — | open | 신선 | 출처 명확 |
| [#19679](https://github.com/openai/codex/issues/19679) | 스킬 메타데이터 2% 하드코딩 | 2026-04-26 | 31 | 19 | open | 신선 | 출처 명확(코드 위치·실측) |
| [#21753](https://github.com/openai/codex/issues/21753) | Claude Code 훅 패리티(29+) | 2026-05-08 | 22 | — | open | 신선 | 출처 명확(이벤트 매트릭스) |
| [#14039](https://github.com/openai/codex/issues/14039) | 서브에이전트별 모델/프로바이더 선택 | 2026-03-09 | 17 | 13 | open | 신선 | 출처 명확 |
| [#15250](https://github.com/openai/codex/issues/15250) | `.codex/agents` 커스텀 에이전트가 문서대로 호출 안 됨 | 2026-03-20 | 16 | 13 | open | 신선 | 출처 명확(다중 재현) |
| [#13386](https://github.com/openai/codex/issues/13386) | AGENTS.md 조용한 truncation | 2026-03-03 | 11 | 3 | open | 신선 | 익명·확인 필요 |
| [#22943](https://github.com/openai/codex/issues/22943) | Claude식 `context: fork` 스킬 지원 | 2026-05-16 | 4 | 5 | open | 신선 | 출처 명확 |
| [#34328](https://github.com/openai/codex/issues/34328) | 레포 커밋 스킬 기본 off (CC `enabledPlugins` 방식) | 2026-07-20 | 4 | 1 | open | 매우 신선 | 출처 명확 |
| [#24515](https://github.com/openai/codex/issues/24515) | Claude 설정 마이그레이션이 사용자 config 덮어씀 | 2026-05-26 | 0 | 1 | open | 신선 | 출처 명확(단일 보고) |
| [#8759](https://github.com/openai/codex/issues/8759) | 글로벌 AGENTS.md 미로드 | 2026-01-05 | 3 | — | **closed 2026-01-07** | ⏳ **오래됨 — 해소됨** | 출처 명확 |

### 7-2. Hacker News (스토리·댓글)

| 항목 | 게시일 | 지표 | URL | 등급 |
|---|---|---|---|---|
| 스토리 "Codex Security" (신제품, 벤더 상주) | 2026-07-28 | 596 pts / 227 c | https://news.ycombinator.com/item?id=49089755 | 출처 명확(벤더 자기식별) |
| 스토리 "Asked Codex to redesign a page; it pushed my repo to OpenAI infra" | 2026-07-24 | 31 pts / 26 c | https://news.ycombinator.com/item?id=49037941 | 단일 사례·본문 AI작성 인정 |
| 댓글 miki123211 — 샌드박스 스펙트럼 | 2026-07-14 | — | https://news.ycombinator.com/item?id=48904705 | 익명·확인 필요 |
| 댓글 steve-atx-7600 — AGENTS.md → CLAUDE.md 포인터 | 2026-07-09 | — | https://news.ycombinator.com/item?id=48851396 | 익명·확인 필요 |
| 댓글 satvikpendem — 용량 기반 한도 차이 설명 | 2026-07-08 | — | https://news.ycombinator.com/item?id=48829605 | 익명·추정 |
| 댓글 bottlepalm — 문제해결력 vs 코드품질 분리 | 2026-07-08 | — | https://news.ycombinator.com/item?id=48828605 | 익명·확인 필요 |
| 댓글 me551ah — Claude만 AGENTS.md 미지원, CC 최다 득표 이슈 언급 | 2026-06-22 | — | https://news.ycombinator.com/item?id=48629719 | 익명·확인 필요(교차검증 권장) |
| 댓글 tunesmith — commit-sized task 루틴 | 2026-06-13 | — | https://news.ycombinator.com/item?id=48519556 | 익명·확인 필요 |
| 댓글 kstenerud — `yoloai` 다중 샌드박스 | 2026-06-14 | — | https://news.ycombinator.com/item?id=48526736 | 출처 명확(본인 저장소) |
| 댓글 nsingh2 — 한도 때문에 Codex 사용 + GPT는 분석적/Claude는 직진 | 2026-06-12 | — | https://news.ycombinator.com/item?id=48510668 | 익명·확인 필요 |
| 댓글 superfrank — 영역별 강약 정리 | 2026-05-15 | — | https://news.ycombinator.com/item?id=48150929 | 익명·확인 필요 |
| 댓글 esperent — codex $100 > anthropic $200 (2x 체감) | 2026-04-29 | — | https://news.ycombinator.com/item?id=47943536 | 익명·**조건 불명** |
| 댓글 rednb — Claude가 허락 없이 너무 빨리 실행 | 2026-04-26 | — | https://news.ycombinator.com/item?id=47914718 | 익명·확인 필요 |
| 댓글 jsLavaGoat — Codex $100에서 한도 도달 경험 없음 | 2026-04-22 | — | https://news.ycombinator.com/item?id=47858803 | 익명·**조건 불명** |
| 댓글 laurels-marts — 공식 문서도 Windows는 WSL 권장 | 2026-04-19 | — | https://news.ycombinator.com/item?id=47822774 | 익명(문서 대조 필요) |
| 댓글 bobjordan — Opus 구현 + Codex 리뷰 2인조 오케스트레이터 | 2026-04-18 | — | https://news.ycombinator.com/item?id=47817892 | 익명·검증 불가 |
| 댓글 pxc — Codex가 더 투명, 외부 샌드박스(nono) | 2026-04-16 | — | https://news.ycombinator.com/item?id=47794968 | 익명·확인 필요 |
| 댓글 tlonny — CC CLI 버그 때문에 Codex Pro로 전환 | 2026-04-09 | — | https://news.ycombinator.com/item?id=47703506 | 익명·확인 필요 |
| 댓글 Razengan — Codex의 AGENTS.md 계층이 직관적 | 2026-03-31 | — | https://news.ycombinator.com/item?id=47583980 | 익명·확인 필요 |
| 댓글 BloondAndDoom — Codex가 코드는 낫지만 느림 + 교차리뷰 무용론 | 2026-03-16 | — | https://news.ycombinator.com/item?id=47405533 | 익명·확인 필요 |
| 댓글 yummyelephant8 — 서브컴포넌트 분해 = agentic engineering | 2026-03-09 | — | https://news.ycombinator.com/item?id=47316658 | 익명·자기홍보 성격 |
| 댓글 3371 — Windows PowerShell 비효율, WSL 필요 | 2026-03-02 | — | https://news.ycombinator.com/item?id=47215741 | 익명·확인 필요 |
| 댓글 toraway — AGENTS.md/CLAUDE.md 준수 기법 무용론 | 2026-02-26 | — | https://news.ycombinator.com/item?id=47173315 | 익명·확인 필요 |
| 댓글 quotemstr — read-only 샌드박스 + 승인 승격 (플래그 부정확 자인) | 2026-02-20 | — | https://news.ycombinator.com/item?id=47095404 | 익명·본인 불확실 명시 |
| 댓글 embedding-shape — 전면 우회 실사용 | 2026-02-19 | — | https://news.ycombinator.com/item?id=47076977 | 익명·확인 필요 |
| 댓글 chandureddyvari — Codex가 게으르다, Context7 MCP도 무효 | 2026-02-03 | — | https://news.ycombinator.com/item?id=46866331 | 익명·확인 필요 |
| 댓글 valleyer — 승인/샌드박스 동작 정확 설명 | 2026-02-01 | — | https://news.ycombinator.com/item?id=46846201 | 익명(문서 정합) |
| 댓글 petesergeant — Codex 리뷰 극찬 | 2025-12-21 ⏳ | — | https://news.ycombinator.com/item?id=46347763 | 익명·확인 필요 |
| 댓글 lemming — Codex 리뷰 > Claude 리뷰(bikeshedding) | 2025-12-18 ⏳ | — | https://news.ycombinator.com/item?id=46317674 | 익명·확인 필요 |
| 댓글 fragmede — 두 도구의 위험 플래그 이름 대조 | 2025-12-01 ⏳ | — | https://news.ycombinator.com/item?id=46105489 | 익명(검증 쉬움) |
| 댓글 pmarreck — AGENTS.md 강조 문법 무용론 | 2025-12-01 ⏳ | — | https://news.ycombinator.com/item?id=46106261 | 익명·확인 필요 |
| 댓글 mock-possum — Windows 승인 폭탄 + WSL의 MCP 복잡성 | 2025-11-19 ⏳ | — | https://news.ycombinator.com/item?id=45981432 | 익명·확인 필요 |
| 댓글 jatora — WSL이 승인 문제를 완전히 해결 | 2025-10-21 ⏳ | — | https://news.ycombinator.com/item?id=45652086 | 익명·확인 필요 |

### 7-3. 한국어 소스

| 항목 | 게시일 | URL | 등급 |
|---|---|---|---|
| AWS 기술 블로그(한국) — "Bedrock 위에서 Codex와 Claude Code 함께 쓰기: Harness Engineering" (저자 Kyutae Park, Ph.D, AWS AI 스페셜리스트 SA) | **2026-06-11** | https://aws.amazon.com/ko/blogs/tech/codex-claudecode-harness/ | **출처 명확 — 실명·소속. 국내 최고 신뢰 소스** |
| GeekNews "Claude와 몇 달간 씨름한 뒤 Codex는 바이브 코더의 꿈처럼 느껴짐" + 한국어 댓글(gkhcdef, helloppfm, xguru, kaydash, skageektp, summerz) | **2026-05-17** | https://news.hada.io/topic?id=29576 | 본문=Reddit 2차 인용·확인 필요 / 댓글=국내 실사용 진술 |
| GeekNews "Claude한테 짜게 시키고 Codex한테 까게 시키기 — 두 에이전트를 한 레포에서 분담" | **2026-04-29** | https://news.hada.io/topic?id=29011 | 2차 인용 |
| GeekNews "Claude Code(~100시간) vs. Codex(~20시간) 비교" + 한국어 댓글(loblue, tangokorea, bungker, oneforall88, minhoryang, master6559, gpdir16, brainer) | **2026-04-15** | https://news.hada.io/topic?id=28538 | 본문=Reddit 2차 인용·확인 필요 / 댓글=국내 실사용 진술 |
| brunch "VS Code + Codex 그 다음 이야기" (kk2daddy) | **2026-03-14** | https://brunch.co.kr/@kk2daddy/112 | 개인 후기·확인 필요 |
| velog "Claude Code와 Codex를 알아보자" (@lovegood) — 개념 대응표·토큰 실측 인용 | **2026-02-14** | https://velog.io/@lovegood/... | ⏳ **경계선(6개월 직전)** — 모델 버전 전제가 낡음. 개념 대응표만 참고, 수치는 조건 불명 |
| Threads (qjc.ai) "코덱스 CLI 다 알려드릴게요 — 갈아탈 필요 없어요" | **날짜 미확인** | https://www.threads.com/@qjc.ai/post/DXnXgvaE1W2/ | 익명·**게시일 미확인, 인용 전 날짜 확보 필수** |

### 7-4. 영어권 개인 블로그·미디엄

| 항목 | 게시일 | URL | 등급 |
|---|---|---|---|
| Naresh B A "I Switched from Claude Code to Codex. Here's What Surprised Me." | 2026-07 (일자 미상) | https://medium.com/@phoenixarjun007/i-switched-from-claude-code-to-codex-heres-what-surprised-me-facaab06a2e6 | 개인 후기·수치 없음·확인 필요 |
| bhanu.io "codex pushed my private repo to an openai server" | 2026-07-24 | HN 49037941 경유 | 단일 사례·본문 AI 작성 인정 |
| dev.to "Claude Code vs Codex 2026 — What 500+ Reddit Developers Really Think" | 2026 (일자 미상) | https://dev.to/_46ea277e677b888e0cd13/... | **2차 집계·방법론 불투명. 인용 비권장(§8 참조)** |

---

## 8. 리서치 한계 (못 찾은 영역)

### 8-1. Reddit 직접 접근 실패 — 이 리서치의 가장 큰 구멍

- `reddit.com` JSON API는 봇 차단, WebSearch도 도메인 차단(크롤러 정책). **r/OpenAI, r/ChatGPTCoding, r/ClaudeAI, r/codex 원문 스레드를 직접 읽지 못했다.**
- 확보한 Reddit 자료는 전부 **2차 인용**이다:
  - GeekNews 번역글 2건(28538 → r/ClaudeCode `1sk7e2k`, 29576 → r/codex `1tf4l2i`) — 원문 URL은 확보했으나 본문·댓글 원문 미확인.
  - dev.to의 "500+ Reddit 개발자" 집계 — **"직접 비교 댓글 중 약 65%가 Codex 선호, 업보트 가중 시 약 80%"**라는 수치가 돌아다니지만, **표본 추출 방법·기간·서브레딧 구성이 공개돼 있지 않다.** 이 숫자는 책에 쓰지 말 것. 쓰더라도 "출처 불투명한 2차 집계"로 명시.
- ⚠️ **구조적 편향 경고:** Reddit 자료의 상당수가 r/codex(Codex 서브레딧) 또는 r/ClaudeAI(Claude 서브레딧) 출신이다. GeekNews 댓글의 skageektp가 이미 이 점을 지적했다 — "Codex는 Reddit 서브레딧이라 편향된 평가일 가능성". 이 책이 비교를 다루는 이상, 서브레딧 출신 자료는 항상 진영을 밝히고 인용해야 한다.
- **보완 경로:** 브라우저 도구(claude-in-chrome) 또는 Firecrawl로 재시도 가능. 후속 리서치 요청 시 우선순위 1번.

### 8-2. 접근 못 한 플랫폼

- **Lobsters** — 검색 미수행(HN·GitHub에서 충분한 양이 나와 우선순위 밀림).
- **Discord/Slack 공개 채널** — 검색 경로 없음. OpenAI Codex 커뮤니티 디스코드에 초기 사용자 담론이 몰려 있을 가능성 큼.
- **X / Mastodon** — 개발자 스레드 직접 수집 실패. HN 댓글에 인용된 X 링크 1건(x.com/claudeai) 외 없음.
- **OKKY, 커리어리, 네이버 개발 카페** — 검색 결과에 Codex 관련 유의미한 스레드가 잡히지 않음. 한국 담론이 GeekNews·velog·브런치·Threads에 몰려 있는 것으로 보임.
- **회사 엔지니어링 블로그** — AWS 한국 블로그 1건 외에 우아한형제들·카카오·토스·네이버 D2·LINE에서 Codex 전환 사례를 찾지 못함. (Codex 도입이 아직 사내 공개 사례로 정리될 만큼 성숙하지 않았을 가능성.)

### 8-3. 내용상 못 채운 축

- **클라우드 위임(Codex Cloud) 장시간 작업 경험담** — 목표한 만큼 못 모았다. HN에서 찾은 관련 진술은 iBelieve(2026-03-27, "Your plan gets **3 daily cloud scheduled sessions**" — Max 20x인데도 제한, https://news.ycombinator.com/item?id=47539320) 정도. **클라우드 태스크 → PR 워크플로의 실제 성공/실패담이 부족하다.**
- **MCP 연동 노하우** — Codex 고유의 MCP 팁이 거의 안 나왔다. 찾은 건 문제 보고뿐(#13200 Slack 공식 MCP `Dynamic client registration not supported` 2026-03-02 open / #17265 라우팅된 MCP OAuth 토큰 자동 갱신 실패 2026-04-09 open / #20135 서브에이전트가 상속 MCP 서버 opt-out, open). CC 대비 MCP 설정 형식 차이(`.mcp.json` vs `config.toml`)의 **실전 마이그레이션 사례**는 못 찾음.
- **한국어 "전환 마찰" 1차 후기** — 국내 자료는 대부분 "비교·소개" 성격이고, "Claude Code 쓰다가 Codex 넘어가서 이런 데서 넘어졌다"는 **구체적 실패담이 거의 없다.** §1의 마찰 사례는 전부 영어권 출처. 책에서 한국 독자 공감 포인트를 만들려면 이 부분은 저자 경험으로 메워야 한다.
- **요금 체감의 정량 비교** — "2배 넉넉하다" 류 체감 진술만 많고, **동일 태스크·동일 조건 벤치마크가 없다.** 유일한 준정량 자료가 velog의 Figma 클로닝 토큰 비교(623만 vs 150만)인데 조건이 불명이다. 그리고 §3-4(b)에서 보듯 **한도 정책 자체가 수시로 바뀌어** 어떤 수치도 날짜 없이는 무의미하다.

### 8-4. 집필 시 반드시 재확인해야 할 항목 (버전 민감)

1. **#11626 `/rewind`** — open 상태 유지 여부. 이 책의 핵심 마찰인데 해결되면 챕터가 통째로 무효.
2. **#12115 중첩 AGENTS.md** — Wix·Stripe 압력이 있어 우선순위가 높을 것으로 추정. 해결 시 §1 마찰 2 재작성 필요.
3. **#28969 60초 자동 응답** — 설정 옵션이 추가됐는지.
4. **#28879 레이트리밋 + #34035 5시간 한도** — 요금·한도 서술 전체가 여기 걸려 있다. 집필 직전 재확인 필수.
5. **Codex Security CLI** — 2026-07-28 출시, 4일 차. 여기 기록된 함정 대부분이 초기 버그일 가능성.
6. **#31814 서브에이전트 모델 지정** — closed지만 후속 #34301이 open. 현행 동작 확인.
