# OpenAI Codex 사용법 완전 정리 — 레퍼런스

> **장르:** tech-book (최신 기술 — 신선도 규율 적용)
> **대상 독자:** Claude Code로 AI Agentic Coding을 경험해본 개발자. "Codex가 무엇인가"가 아니라 **"내가 알던 것과 무엇이 다른가"**가 이 책의 축이다.
> **리서치 수행일:** 2026-08-02. 이 문서의 모든 사실은 **2026-08-02 방문 기준**이다.
> **1차 소스:** OpenAI 공식 문서 `https://learn.chatgpt.com` (Codex 섹션 전수 148 URL)
> **보존 산출물:** `research/web-1.md` ~ `web-6.md`, `research/community.md`, `research/community-2.md`, `research/papers.md`, 그리고 **원문 무손실 캐시 `research/codex-docs-raw/` (69개 파일, 1.5MB)**

## 이 문서를 쓰는 법 (저술가·fact-checker 필독)

1. **인용 문구가 정확한지 다툼이 생기면 `research/codex-docs-raw/`의 원문 파일이 최종 판정 기준이다.** 파일명은 URL 경로의 `/`를 `__`로 바꾼 것 (`/codex/config-file/config-reference` → `codex__config-file__config-reference.md`).
2. 이 문서에서 **큰따옴표로 감싼 영문 문장은 원문 verbatim**이다. 따옴표 없는 서술은 정리·요약이다.
3. **공식 문서에는 발행일 표기가 없다.** 유일한 버전 앵커는 문서 본문에 박힌 버전 번호(`0.114`, `0.138.0`)뿐이다. 따라서 모든 사실은 "2026-08-02 기준"으로만 고정된다. 챕터에 버전·모델명·수치를 쓸 때는 **반드시 "2026년 8월 기준"을 병기하라.**
4. ⚠️ 표시는 **문서 간 상충 또는 1차 확인 불가**를 뜻한다. 🕒 표시는 **시점 의존이 극심해 집필 직전 재확인이 필요한 항목**이다.

---

## 1. 개념과 정의

### 1-1. Codex는 제품 하나가 아니라 표면(surface)의 집합이다

Claude Code 경험자가 가장 먼저 교정해야 할 전제다. Claude Code는 CLI가 1급 표면인 단일 도구지만, **Codex는 ChatGPT라는 우산 아래 놓인 여러 표면 중 하나**다.

공식 문서(`/codex/use-chatgpt`)가 제시하는 **3분법**이 이 문서군 전체의 개념 축이다 — 원문 표 그대로:

| Choose | When you want to | Examples |
|---|---|---|
| Chat | Work through something with ChatGPT | Ask a question, search the web, brainstorm, draft a message, compare options |
| ChatGPT Work | Define an outcome and get a reviewable result | Create a deck, analyze files, draft a report, build a project plan |
| Codex | Use developer tools and see technical details | Debug code, run tests, review a PR, implement a feature |

→ **Claude Code에는 이 3분법이 없다.** Codex의 3분법은 "비개발자용 산출물 모드(Work)"를 같은 엔진 위에 얹은 제품 전략이며, Claude Code 사용자에게 가장 낯선 구조다. (출처: 웹 / `/codex/use-chatgpt`)

### 1-2. 두 개의 통제 장치 — 샌드박스와 승인은 다른 것이다

`/codex/permission-modes`의 원문이 이 책의 보안 챕터 전체를 지탱한다:

> "The **sandbox** defines which files and network resources ChatGPT can access."
> "**Approvals** determine when ChatGPT pauses before an action or sends the request to automatic review."
> "Changing who reviews a request doesn't expand the sandbox. For example, **Approve for me** keeps the same workspace boundary as **Ask for approval**; it sends requests to cross that boundary to automatic review."

**이 분리를 도식(mermaid)으로 그리는 것을 강력히 권한다.** 커뮤니티에서 확인된 혼란의 상당수가 이 둘을 하나로 뭉쳐 이해한 데서 온다.

정확히 말하면 통제 축은 **셋**이다 — ⓐ **sandbox**(무엇에 닿을 수 있나) ⓑ **approvals**(언제 멈추나) ⓒ **`approvals_reviewer`**(누가 심사하나 — 기본 `user`, 또는 `auto_review`). 여기에 `granular` 하위 토글 5개가 얹힌다. **Claude Code 대응표는 이 3축 기준으로 작성해야 한다.**

### 1-3. 확장 모델 — 스킬과 플러그인

원문 정의 (`/codex/skills-and-plugins`):

> "A **skill** packages instructions and supporting resources for a specific task or workflow."
> "A **plugin** is an installable bundle that can include skills, connectors, or both. Connectors are backed by **Model Context Protocol (MCP)** servers and can optionally include custom ChatGPT UI."

호출 문법이 표면마다 다르다 — **Claude Code 사용자가 가장 먼저 헷갈릴 지점**:

> "ChatGPT supports **`@` mentions**, while Codex supports **`$` mentions** for skills."

### 1-4. AGENTS.md — "에이전트를 위한 README"

`/codex/learn/best-practices`의 정의가 가장 인용하기 좋다:

> "Think of `AGENTS.md` as **an open-format README for agents**."
> "Keep it practical. **A short, accurate `AGENTS.md` is more useful than a long file full of vague rules.** Start with the basics, then add new rules only after you notice repeated mistakes."
> "**When Codex makes the same mistake twice, ask it for a retrospective and update `AGENTS.md`.**"

### 1-5. 용어 대응 빠른 지도

| Codex | Claude Code | 성격 |
|---|---|---|
| `AGENTS.md` | `CLAUDE.md` | 거의 대응 (단, 중첩 로딩 동작이 다름 — §5-2) |
| `config.toml` | `settings.json` | 형식만 다른 대응 |
| Skills (`.agents/skills`) | Skills (`.claude/skills`) | 대응 (디렉터리명이 벤더 중립) |
| `$skill` 호출 | `/skill` 호출 | **접두사가 다름** |
| execpolicy `.rules` | `permissions.allow/deny/ask` | 대응 + Codex가 테스트 하네스 보유 |
| Hooks | Hooks | **부분 대응** (커버리지 차이 — §5-2) |
| Subagents (`.codex/agents/*.toml`) | Subagents (`.claude/agents/*.md`) | 대응 |
| Custom prompts (`~/.codex/prompts/`) | 커스텀 슬래시 명령 | 대응하나 **Codex 쪽은 deprecated** |
| `codex exec` | `claude -p` | 비대화형 실행 |
| Codex cloud | (대응 없음) | Codex 고유 |
| Chronicle / Computer Use / Appshots | (대응 없음) | Codex 고유 |

---

## 2. Codex 제품 구조 — 표면별

### 2-1. ChatGPT 데스크톱 앱 (1급 표면)

- **2026-07-09 Codex 앱이 ChatGPT 데스크톱 앱으로 병합됐다** (macOS·Windows). 원문: "The updated desktop app is available **globally on every ChatGPT plan, including Free**." (출처: `/codex/whats-new`)
- 온보딩에 **"ChatGPT가 작업할 위치(폴더)를 고르는 단계"**가 명시적으로 존재한다 — "ChatGPT can read and modify files in the folder you choose." Claude Code는 cwd가 암묵적이라는 점에서 대비된다.
- **로컬 vs 클라우드 토글:** 컴포저의 **Work locally** 컨트롤. 클라우드를 고르는 이유는 ⓐ 앱을 닫거나 컴퓨터를 꺼도 계속 실행 ⓑ 웹·모바일에서 대화 이어가기. (출처: `/codex/get-started-with-work`)
- 2026-07-20~24 **다중 폴더 지원**: primary 폴더가 새 채팅·Git 작업·`AGENTS.md`/skills/`config.toml` 자동 탐색을 담당하고, secondary 폴더는 파일 검색·읽기·편집만 가능하다.

### 2-2. Codex CLI

책의 레퍼런스 장 골격. `/codex/cli/reference`(캐노니컬 `/docs/developer-commands?surface=cli`) 한 페이지가 **전역 플래그 20개 + 서브커맨드 28개 + 내장 슬래시 명령 약 60개**를 모두 담는다.

문서가 직접 밝히는 우선순위 규칙:

> "The CLI inherits most defaults from `~/.codex/config.toml`. Any `-c key=value` overrides you pass at the command line take precedence for that invocation."

⚠️ **성숙도 체계를 일반화하지 마라.** `/codex/feature-maturity`에는 **4등급 정의표만 있고 기능별 등급 목록이 없다.** 라벨은 각 기능 문서에 흩어져 인라인으로 붙어 있으며, **정의된 등급명과 실제 사용 라벨("research preview", "public beta")이 일치하지 않는다.** "Codex는 4단계 성숙도 체계를 쓴다"는 서술은 **과잉 일반화**다.

**성숙도 라벨 — `experimental`로 표기된 명령 7개 (2026-08-02 기준):** `codex app-server`, `codex remote-control`, `codex debug app-server send-message-v2`, `codex debug models`, `codex debug prompt-input`, `codex cloud`, `codex execpolicy`. **나머지 21개는 `stable`.**
→ 책에서 이 7개를 소개할 때는 **"실험적 — 예고 없이 바뀔 수 있음"**을 반드시 병기하라. 문서 자체가 `codex app-server`에 대해 "may change without notice"라고 못 박는다.

**핵심 전역 플래그** (원문 표는 `research/web-6.md`에 전량 수록):

| 플래그 | 값 | 기본값 |
|---|---|---|
| `--sandbox, -s` | `read-only` \| `workspace-write` \| `danger-full-access` | (설정 따름) |
| `--ask-for-approval, -a` | `untrusted` \| `on-request` \| `never` | (설정 따름) |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | boolean | `false` |
| `--add-dir` | path (반복 가능) | — |
| `--search` | boolean (`web_search`를 `"cached"`→`"live"`) | `false` |
| `--profile, -p` | `$CODEX_HOME/profile-name.config.toml` 적층 | — |
| `--config, -c` | `key=value` (TOML 파싱) | — |

문서의 안전 권고 원문: "Use `--sandbox workspace-write` for unattended local work that can stay inside the workspace, and avoid `--dangerously-bypass-approvals-and-sandbox` unless you are inside a dedicated sandbox VM." / "When you need to grant Codex write access to more directories, prefer `--add-dir` rather than forcing `--sandbox danger-full-access`."

**`--full-auto`는 deprecated다** — "Prefer `--sandbox workspace-write`; Codex prints a warning when this flag is used."

### 2-3. IDE 확장

- 원문 Note: "**The IDE extension automatically includes your open files as context. In the CLI, mention paths explicitly, or attach files with `/mention` and `@` path autocomplete.**" (출처: `/codex/prompting`)
- 명령 팔레트에 **"Add to Codex Thread"**.
- ⚠️ **Visualizations는 CLI·IDE 확장에서 렌더링되지 않는다** (원문 가용성 표).

### 2-4. 웹 (chatgpt.com)

Chat과 ChatGPT Work를 제공. Codex 전용 개발자 뷰는 데스크톱 앱·CLI·IDE 쪽이다.

### 2-5. Codex cloud

- **모델 제약이 결정적이다.** GPT-5.6 3종 중 **Codex cloud에서 쓸 수 있는 것은 Sol 뿐**이며, 원문은 "Currently, you can't change the default model for Codex cloud chats."라고 못 박는다. (출처: `/codex/models`)
- 네트워크 기본 차단: "Tasks delegated to the cloud run in isolated environments. **Internet access is off during the agent phase unless you enable it for the environment.**" (출처: `/codex/prompting`)
- CLI에서 접근: `codex cloud`(experimental), `codex cloud exec --env {ENV_ID} --attempts 1-4`, `codex cloud list --limit 1-20`, `codex apply {TASK_ID}`.

### 2-6. SDK · app-server · MCP 서버

- **SDK는 app-server의 얇은 래퍼다** — 원문 확인: "The Python SDK controls the local Codex app-server over JSON-RPC." Python SDK는 **2026-08 기준 beta**.
- 문서가 선택 기준을 직접 제시한다: SDK는 코딩 스레드용, **MCP 서버 + Agents SDK는 Codex를 더 큰 워크플로의 한 전문가로 쓸 때**.
- `codex mcp-server` — Codex 자신을 MCP 서버로 노출한다. "Useful when another agent consumes Codex." → **Claude Code가 Codex를 도구로 부르는 구성이 문서상 가능하다.**

### 2-7. ⭐ 오픈소스 경계가 비대칭이다 — "Codex는 오픈소스다"는 사실 오류

`/codex/open-source` 기준: **CLI · SDK · app-server · skills는 오픈소스**지만 **IDE 확장과 cloud는 명시적으로 "Not open source"**다.

→ 그런데 Claude Code는 **CLI 층이 비공개**다. 즉 **CLI 층에서 정확히 뒤집힌 구도**이며, 이것이 두 제품의 생태계 전략 차이를 보여주는 가장 선명한 사실이다. 비교 챕터의 좋은 소재이되, "Codex는 오픈소스"라는 뭉뚱그린 서술은 **틀린 문장**이 된다.

### 2-8. 그 외 표면·주변부

Chrome 확장, 내장 브라우저(Computer Use), Appshots(양쪽 Command 키), 음성(Ctrl+M 받아쓰기 / ChatGPT Voice), iOS Remote, Sites, Codex Micro(2026-07-15 출시, OpenAI × Work Louder 한정 생산), Amazon Bedrock 경유 사용.

---

## 3. 기능별 정리 (공식 문서 트리 순)

### 3-1. 모델 — `/codex/models`를 단일 출처로 삼는다

⚠️ **모델명이 문서 여러 곳에서 흔들린다.** `/codex/overview`의 **UI 삽화 속 문자열**과 `/codex/community/codex-for-oss`의 "GPT-5.4" 등은 **단독 근거로 쓰지 마라.** `/codex/models`가 정전이다.

⚠️ **주의 — 이 삽화 문자열은 리서처 두 명이 서로 다르게 읽었다**(한쪽은 "5.6 Sol Extra High", 다른 쪽은 "5.6 Sol Extended"). **어느 쪽도 책에 인용하지 마라.** 확정된 사실은 두 가지뿐이다: ⓐ 정식 모델 ID는 `gpt-5.6-sol`/`terra`/`luna` ⓑ 본문의 추론 티어는 Light/Medium/High/Extra High(+ Max/Ultra 표기 존재)이며 **삽화 문자열은 티어명이 아니다.**

**권장 모델 3종 + 프리뷰 1종 (2026-08-02 기준, 원문 데이터 전수):**

| 모델 ID | 표시명 | 원문 설명 | Capability | Speed |
|---|---|---|---|---|
| `gpt-5.6-sol` | 5.6 Sol | "Flagship GPT-5.6 model with the strongest capability for complex coding, computer use, research, and cybersecurity." | ★5 | ⚡2 |
| `gpt-5.6-terra` | 5.6 Terra | "Balanced GPT-5.6 model for everyday work, with performance competitive with GPT-5.5 at a lower cost." | ★4 | ⚡3 |
| `gpt-5.6-luna` | 5.6 Luna | "Fast and affordable GPT-5.6 model that delivers strong capability at the lowest cost in the family." | ★3 | ⚡4 |
| `gpt-5.3-codex-spark` | 5.3 Codex Spark | "Text-only research preview model optimized for near-instant, real-time coding iteration. **Available to ChatGPT Pro users.**" | ★2 | ⚡5 |

**표면별 가용성 — cloud 열이 핵심:**

| 모델 | 데스크톱 | 웹 | CLI | IDE | **cloud** | Credits | API |
|---|---|---|---|---|---|---|---|
| `gpt-5.6-sol` | ✅ | ✅ | ✅ | ✅ | **✅** | ✅ | ✅ |
| `gpt-5.6-terra` | ✅ | ✅ | ✅ | ✅ | **❌** | ✅ | ✅ |
| `gpt-5.6-luna` | ✅ | ✅ | ✅ | ✅ | **❌** | ✅ | ✅ |
| `gpt-5.3-codex-spark` | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |

기타 모델 `gpt-5.5` / `gpt-5.4` / `gpt-5.4-mini`는 cloud만 ❌, 나머지 전부 ✅.

**선택 기준 (원문 그대로 — 인용 가치 최상):**

> "Codex offers three GPT-5.6 models: **Sol** for detail and polish, **Terra** as the everyday workhorse, and **Luna** for clear, repeatable work. If you are unsure, start with Sol."

Terra 설명의 실무적 함의: "It is a natural starting point for work you previously gave **GPT-5.5**."

**추론 강도:** Light(앱·웹·IDE) 또는 Low(CLI) / Medium / High / Extra High. 원칙은 "Use the **lowest** reasoning effort that produces the result you need." 그리고 결정적 경고:

> "**There is no exact mapping from GPT-5.5 reasoning efforts to GPT-5.6.** Try a familiar task at a lower setting and adjust based on the result."

🕒 **모델 은퇴 예고:** `gpt-5.4`와 `gpt-5.4-mini`가 **2026년 8월 31일** 은퇴한다(ChatGPT 로그인 사용자 한정, API 키 인증은 영향 없음). 대체는 `gpt-5.4` → `gpt-5.6-terra`, `gpt-5.4-mini` → `gpt-5.6-luna`. (출처: `/codex/enterprise/workspace-model-availability`)
→ **이 책이 나오는 시점엔 이미 지난 날짜다.** 집필 시 반드시 반영하라.

### 3-2. 요금과 사용량 한도 — 🕒 최고 위험 원장

**요금 (2026-08-02 기준, `/codex/pricing`):** Free `$0` / Go `$8` / Plus `$20` / Pro `$100`(5x) / Pro `$200`(20x) / Business `$20`(2+ users, **연간 결제 기준**; 월 결제 시 **$25/user/month**).

**사용량 한도 표가 실제로 존재한다.** 플랜 탭 5개(`Plus` / `Pro 5x` / `Pro 20x` / `Business` / `API Key`) 각각에 모델별 × (Local Messages / Cloud chats / Code Reviews) / 5h 표가 있다.

Plus 탭 실측값 (원문 그대로 — **범위를 단일 수치로 뭉개지 말 것**):

| 모델 | Local Messages / 5h | Cloud chats / 5h | Code Reviews / 5h |
|---|---|---|---|
| GPT-5.6 Sol | `10-100` | Not available | Not available |
| GPT-5.6 Terra | `25-200` | Not available | Not available |
| GPT-5.6 Luna | `250-2,000` | Not available | Not available |
| GPT-5.5 | `15-80` | Not available | Not available |
| GPT-5.4 | `20-100` | Not available | Not available |
| GPT-5.4 mini | `60-350` | Not available | Not available |

각주가 결정적이다: "The usage limits for local messages and cloud chats **share a five-hour window**. Additional weekly limits may apply."

**크레딧 요율 (2026-08-02 기준, `/codex/pricing`):** 입력 Sol/Terra/Luna = **125 / 50 / 5**, 출력 = **750 / 300 / 30**. 문서 표현으로 메시지당 평균 **"5-40 credits per message"**.
→ Sol과 Luna의 입력 요율 차가 **25배**다. 모델 선택이 곧 비용 설계라는 점을 이 숫자로 설명할 수 있다.

⚠️ **문서에는 한도 변경 이력이 없다.** 따라서 커뮤니티의 "2026-06 한도 급등" 주장을 **공식 문서로 확인할 수도 반박할 수도 없다**(§5-6).

⚠️ **반대로 `/codex/enterprise/usage-limits`에는 수치가 하나도 없다.** 전문 37줄이며 원문이 명시적으로 선을 긋는다: "These controls aren't a universal Codex limit system and don't govern OpenAI API Platform billing." 구체 수치는 help.openai.com으로 위임된다.
→ 따라서 **개인 요금제 한도의 1차 소스는 `/codex/pricing` 하나뿐**이다.

### 3-3. 권한·샌드박스 — 구 체계가 기본, 신 체계가 Beta로 병행

**이 절은 그룹 D가 1차 수집에서 원문에 없는 문장을 합성했다가 재수집으로 정정한 영역이다.** 인용 시 반드시 원문 캐시를 대조하라.

**권한 모드 3종** (`/codex/permission-modes`): **Ask for approval**(항상 사용 가능, 권장 기본값) / **Approve for me**(설정에서는 **Auto-review**로 표기) / **Full access**. 데스크톱 앱은 **Settings > General > Permissions**에서 먼저 모드를 켜야 메뉴에 나타난다 — "Enabling a mode makes it available in the menu; **it doesn't select the mode or change an existing chat.**"

⚠️ `/codex/sandboxing`의 app·ide 서피스 절에는 **Custom을 포함한 4종**(Ask for approval / Approve for me / Full access / Custom)이 나온다. 페이지마다 노출 범위가 다르니 하나의 표로 뭉치면 오류가 된다.

**설정 값 층위 — 3층이 겹쳐 있어 섞으면 즉시 틀린다:**

1. **UI 라벨:** Ask for approval / Approve for me(Auto-review) / Full access / Custom
2. **구 설정 값:** `approval_policy` = `untrusted` \| `on-request` \| `never` × `sandbox_mode` = `read-only` \| `workspace-write` \| `danger-full-access`
3. **`granular` 하위 토글 5개:** `sandbox_approval` · `rules` · `mcp_elicitations` · `request_permissions` · `skill_approval`

**권한 프로필 (Beta)** — `/codex/permissions` 5행 원문: "**Beta. Permission profiles are under active development and may change.**" 책이 이 체계를 정전처럼 서술하면 안 된다.

폴백 규칙이 결정적이다 (원문):

> "Permission profiles do not compose with the older sandbox settings. Configure either `default_permissions` and `[permissions]`, or `sandbox_mode` / `sandbox_workspace_write`, but not both. If `sandbox_mode` appears in any loaded config file, you pass `--sandbox`, or the selected config profile sets `sandbox_mode`, Codex uses those older sandbox settings instead of `default_permissions`."

→ **구 설정이 어디에라도 있으면 구 체계가 이긴다.** 유일한 예외가 관리자의 `allowed_permission_profiles`이며, 그 경우 **Codex 0.138.0 이상**이 필요하다(0.137.0 이하는 무시).

내장 프로필 3종: `:read-only` / `:workspace` / `:danger-full-access`. `extends`는 `:danger-full-access`를 상속할 수 없고, 알 수 없는 부모와 상속 순환도 거부된다.

**Auto-review 서킷 브레이커 (정확한 수치 주의):** "after `3` consecutive denials or `10` denials within a rolling window of **the last `50` reviews** in the same turn" — 50건 창 조건을 빠뜨리면 틀린 서술이 된다.

**OS별 샌드박스 구현** (GPT-5.2-Codex 시스템 카드 §3.1): macOS = Seatbelt, Linux = seccomp + landlock, Windows = 네이티브 샌드박스 또는 WSL 경유. 문서 기준 Codex `0.114`까지 WSL1 지원, `0.115`부터 Linux 샌드박스가 `bubblewrap`으로 이동.

### 3-4. 설정 — `config.toml`

- **설정 키 전수: `config.toml` 274개 + `requirements.toml` 116개.** 전량 표가 `research/codex-docs-raw/_config-reference-tables.md`에 마크다운으로 복원돼 있다.
- **공식 JSON 스키마**가 `https://learn.chatgpt.com/docs/config-schema.json`에 있다 — 설정 키 검증의 1차 근거로 쓸 수 있다.
- 3계층 권고 (원문): 개인 기본값 `~/.codex/config.toml` / 저장소별 `.codex/config.toml` / 일회성만 커맨드라인 오버라이드.
- 프로필 오버라이드: `$CODEX_HOME/profile-name.config.toml` (`--profile`로 적층).
- `/debug-config`로 레이어 순서·정책 출처를 진단할 수 있다.

### 3-5. execpolicy — 규칙을 테스트할 수 있다

Claude Code의 `permissions.allow/deny/ask`에 대응하되, **Codex 고유 강점 3가지**가 있다:

1. `justification`으로 규칙에 이유를 문서화
2. `match`/`not_match`로 **규칙 자체를 테스트**
3. `codex execpolicy check`로 **규칙을 CI에서 검증**

```bash
codex execpolicy check --pretty \
  --rules ~/.codex/rules/default.rules \
  -- gh pr view 7888 --json title,body,comments
```

셸 래퍼 처리 규칙: `&&`, `||`, `;`, `|`로 연결된 명령은 **분리해 각각 평가**하고, 리다이렉션·변수 치환이 있으면 **전체를 하나의 명령으로 취급**한다.

→ **Claude Code에는 규칙 단위 테스트 하네스가 없다.** 비교 챕터의 핵심 소재다.

### 3-6. AGENTS.md · 서브에이전트 · 훅 · 스킬

- **`/init`**이 `AGENTS.md` 스캐폴드를 만든다 (Claude Code `/init`과 같은 이름·같은 역할).
- 계층: 전역 `~/.codex` → repo → 하위 디렉터리. 원문 표현은 "more specific file closer to your current directory, that guidance wins".
- **서브에이전트 모델 3종 권장:** `gpt-5.6`(고난도) / `gpt-5.6-terra`(속도) / `gpt-5.6-luna`(빠르고 좁은 작업).
- **스킬 경로:** 개인 `$HOME/.agents/skills`, 팀 공유 `.agents/skills`(저장소 체크인). 스캐폴딩 도구는 `$skill-creator`.
- **Custom prompts는 deprecated다** — 원문 첫 문장: "**Custom prompts are deprecated.** Use skills for reusable instructions that Codex can invoke explicitly or implicitly." 이 기능을 "Codex의 커스텀 슬래시 명령 만들기"로 소개하면 **폐기 예정 기능을 추천하는 셈**이 된다.
- ⭐ **`AGENTS.md`에 명시적 바이트 예산이 있다:** `project_doc_max_bytes = 32768`. 그리고 `project_doc_fallback_filenames`로 **파일명 자체를 커스터마이즈**할 수 있다 — Claude Code가 `CLAUDE.md`로 고정된 것과 대비된다. (커뮤니티 이슈 #13386 "AGENTS.md가 조용히 잘린다"의 문서적 근거가 이 키다.)
- ⭐ **Codex 훅이 `CLAUDE_PLUGIN_ROOT`·`CLAUDE_PLUGIN_DATA`를 호환용으로 설정한다고 문서에 명시돼 있다.** 이벤트명·JSON 스키마·exit code 2 관례까지 사실상 동형이다. 차이는 Codex에만 **해시 기반 훅 신뢰 검토**와 `--dangerously-bypass-hook-trust`가 있다는 점.
  → **경쟁 제품의 환경 변수 이름을 자기 문서에 박아 넣은 것**이라, 마이그레이션 장에서 인용 가치가 매우 높다.

### 3-7. 프롬프팅 — 문서가 제시하는 프레임

⚠️ **4요소 프레임이 두 페이지에서 다르게 나온다.** 둘 다 원문이니 어느 쪽을 쓰는지 밝혀라.

- `/codex/prompting`: **Goal / Context / Output / Boundaries**
- `/codex/learn/best-practices`: **Goal / Context / Constraints / Done when**

**Steering vs Queuing (Codex 고유 개념):**

- **Steer** — 메시지를 **현재 실행 중인 턴에 추가**. CLI에서 <kbd>Enter</kbd>.
- **Queue** — 메시지를 **다음 턴을 위해 저장**. CLI에서 <kbd>Tab</kbd>.
- 데스크톱 기본값은 **Settings > General > Follow-up behavior**.

→ Claude Code에는 이 2모드 구분이 없다(실행 중 입력이 단일 동작으로 큐잉된다). 눈에 띄는 UX 차이다.

**"흔한 실수" 8개 목록** (`/codex/learn/best-practices` 원문) — 챕터 오프닝·마무리 소재로 최상급:

> - Overloading the prompt with durable rules instead of moving them into `AGENTS.md` or a skill
> - Not letting the agent see its work by not giving details on how to best run build and test commands
> - Skipping planning on multi-step and complex tasks
> - Giving Codex full permission to your computer before you understand the workflow
> - Running live tasks on the same files without using Git worktrees
> - Scheduling a recurring task before it's reliable manually
> - Treating Codex like something you have to watch step by step instead of using it in parallel with your own work
> - Using one chat for an entire project instead of one chat per coherent outcome. This leads to bloated context and worse results over time

**chat 단위 원칙:** "**Keep one chat per coherent unit of work.** ... Fork only when the work truly branches."

### 3-8. 코드 리뷰

- OpenAI 자체 주장: **"At OpenAI, Codex reviews 100% of PRs."** (출처: `/codex/learn/best-practices`)
- CLI: `codex review`(비대화형, `--uncommitted` / `--base` / `--commit` 중 택1 — **서로 충돌한다**), TUI: `/review`.
- GitHub PR: `@codex review` 코멘트. 사전에 저장소에 Codex Code review 활성화 필요.
- 리뷰 도구에 대한 문서 자신의 경고: "models must be trained specifically to identify P0 and P1-level bugs, and tuned to provide concise, high-signal feedback; **overly verbose responses are ignored just as easily as noisy lint warnings.**"

### 3-9. 인증 — 개인 개발자 필독

```
codex login                                          # ChatGPT 브라우저 로그인
printenv OPENAI_API_KEY | codex login --with-api-key
printenv CODEX_ACCESS_TOKEN | codex login --with-access-token
codex login --device-auth                            # 헤드리스 (beta)
codex login status                                   # 인증 방식 확인 (로그인 시 exit 0)
codex logout
```

- 자격증명 캐시: `~/.codex/auth.json` (또는 OS 자격증명 저장소). `CODEX_HOME` 기본값은 `~/.codex`.
- 설정 키: `cli_auth_credentials_store = "file" | "keyring" | "auto"`
- 환경 변수: `OPENAI_API_KEY`, `CODEX_ACCESS_TOKEN`, `CODEX_CA_CERTIFICATE`(미설정 시 `SSL_CERT_FILE` 폴백)
- **로그인 콜백 포트 `localhost:1455`** — 원격 작업 시 `ssh -L 1455:localhost:1455 user@remote`
- ⚠️ API 키 로그인 시 기능 제약: "You may also use Codex with an API key. **Some features might not be available**"

### 3-10. Codex Security (별개 제품)

**Codex 자체의 실행 보안과 혼동하지 마라.** `/codex/agent-approvals-security` 원문이 직접 경계를 긋는다:

> "This page covers how to operate Codex safely, including sandboxing, approvals, and network access. If you are looking for Codex Security, the product for scanning connected GitHub repositories, see [Codex Security]."

다만 두 주제는 두 지점에서 만난다: ⓐ CI 실행 시 `codex exec --sandbox workspace-write`가 필요하고, ⓑ **Trusted Access for Cyber** 인증이 스캔 품질의 전제다("For best results, use an account verified for Trusted Access for Cyber." — 4개 페이지에서 반복).

**제품이 자기 비결정성을 스스로 명문화한다** — 인용 가치가 높은 대목: "AI-assisted scans can vary, even with the same scan configuration". 스캔 비교 상태는 **5개**(`new`, `persisting`, `reopened`, `resolved`, `unknown`), 커버리지는 3등급(`complete`/`partial`/`unknown`).

⚠️ **모델명 계열을 섞지 마라 — 여기가 사실 오류가 나기 가장 쉬운 자리다:**

| 계열 | 모델 | 맥락 |
|---|---|---|
| 에이전트 라우팅·사이버 안전 정책 | `GPT-5.3-Codex`(High cybersecurity capability 최초 지정), 리라우팅 대상 `GPT-5.2` | `/codex/cyber-safety` |
| **Codex Security 스캔** | **`gpt-5.6-sol`이 기본이자 유일 권장** | `/codex/security/*` |
| (예시로만 등장) | `gpt-5.6-terra` | CLI 예시 문자열 — **권장 모델로 서술하면 오류** |

또한 **Codex Security 플러그인 `0.1.15`와 CLI `0.1.3`은 별개 버전 계열**이다(모순이 아니다).

`codex-security mcp`·`codex-security skills` 명령이 있다 — **CLI가 스스로 MCP 서버로 등록되고 스킬을 에이전트에 동기화한다.** 즉 Codex Security는 Claude Code를 포함한 다른 에이전트의 **부품으로 편입될 수 있다.** "경쟁 제품"이 아니라 "조합 가능한 부품"이라는 관점의 문서적 근거다.

**protected paths:** `.git`·`.agents`·`.codex`는 writable root 안에서도 읽기 전용이다 — **에이전트가 자기 통제 장치를 못 고치게 막는 자기참조 방어**이며, Claude Code에 명문화된 대응물이 없는 차별점이다.

### 3-11. ⚠️ 문서 내부 불일치 원장 (fact-checker 필수 대조)

공식 문서 안에서 서로 어긋나는 지점들이다. **하나를 정전으로 골라 서술하고, 반대쪽 페이지는 인용하지 마라.**

| # | 불일치 | 정전으로 삼을 페이지 |
|---|---|---|
| 1 | **reasoning effort 값 목록** — `config-sample`·`config-basic`은 `minimal\|low\|medium\|high\|xhigh`, **`subagents`만 `ultra`·`max` 추가** | `config-reference` |
| 2 | **WSL 경로 성능 권고가 정반대** — `windows-app` ↔ `wsl` 두 페이지 | 확정 불가 — **책에 성능 권고를 쓰지 말 것** |
| 3 | **requirements 우선순위** — `managed-configuration`("lower to higher precedence") ↔ `hipaa-configuration`("Earlier requirements take precedence")로 cloud·MDM 상대 순서 표현이 다름 | `managed-configuration` |
| 4 | **access token 지원 플랜** — `access-tokens`는 "Business and Enterprise", `auth`는 "Enterprise"만 | `access-tokens`(전용 페이지) |
| 5 | **권한 모드 개수** — `permission-modes`는 3종, `sandboxing`의 app·ide 절은 **Custom 포함 4종** | 표면별로 병기 |
| 6 | **GPT-5.4 은퇴일** — `models`·`changelog`·`automations` 3중 일치(2026-08-31). `whats-new`에만 없음 | **모순이 아니라 누락** |

**명칭 주의:** `/codex/artifacts-viewer`의 **실제 문서 제목은 "Work with files"**다. "Artifacts viewer"는 문서 본문에 없는 이름이므로 **챕터명·용어로 쓰면 오류**가 된다.

---

## 4. Claude Code 대응 관점 — 이 책의 심장

### 4-1. ⭐ 마이그레이션 매핑은 추측이 아니라 문서에 박혀 있다

이 리서치의 최대 발견이다. **OpenAI가 Claude Code 사용자의 이주 경로를 문서와 프로토콜 양쪽에 구현해뒀다.**

**(a) 사용자용 임포트 표** (`/codex/import` 원문 그대로):

| Imported item | Destination |
|---|---|
| Instruction files | `AGENTS.md` |
| `settings.json` | `config.toml` |
| Skills | Skills |
| Plugins | Plugins |
| Existing project folders | Projects using the same folders |
| Chats from the last 30 days | ChatGPT chats |
| MCP server configuration | Codex MCP configuration |
| Hooks | Codex hooks |
| **Slash commands** | **Skills** |
| Subagents | Codex agents |

- 지원 소스로 **Claude Code와 Claude Cowork가 명시**돼 있다 (changelog 2026-06-09).
- "**Importing doesn't change or delete your existing agent setup.**" (비파괴)
- ⚠️ "**Standard Claude Chat data cannot be imported**"
- **슬래시 명령이 스킬로 접힌다**는 점이 두 제품의 확장 모델 차이를 가장 잘 보여준다.

**(b) 프로토콜 수준** (`/codex/app-server`, `externalAgentConfig/detect` · `import`):

```json
{ "method": "externalAgentConfig/import", "params": {
  "migrationItems": [ ... ], "source": "claude-code" } }
```

마이그레이션 가능한 `itemType` 전수 (원문): `AGENTS_MD`, `CONFIG`, `SKILLS`, `PLUGINS`, `MCP_SERVER_CONFIG`, `SUBAGENTS`, `HOOKS`, `COMMANDS`, `SESSIONS` — **9종**.

구체적 경로 매핑도 응답 예시에 박혀 있다: `/Users/me/project/CLAUDE.md` → `AGENTS.md`, `~/.claude/skills` → `~/.agents/skills`.

중복 방지 규칙: "Codex skips AGENTS migration when `AGENTS.md` already exists and is non-empty, and skill imports don't overwrite existing skill directories."

마켓플레이스 추론까지 구현돼 있다: "When detecting plugins from `.claude/settings.json`, Codex reads configured marketplace sources from `extraKnownMarketplaces`. If `enabledPlugins` contains plugins from `claude-plugins-official` but the marketplace source is missing, Codex infers `anthropics/claude-plugins-official` as the source."

**임포트 후 반드시 검토할 것** (원문 목록): 스킬·에이전트의 도구 제한/권한 / 커스텀 인증·헤더·환경 변수를 쓰는 MCP 서버 설정(재로그인 필요할 수 있음) / 동작이 달라질 수 있는 훅 / 수동 후속이 필요한 플러그인·마켓플레이스 / 인자·셸 보간·파일 경로 플레이스홀더에 의존하는 프롬프트 템플릿.

### 4-2. 같은 이름, 다른 동작 — 가장 위험한 함정

| 항목 | Claude Code | Codex | 위험도 |
|---|---|---|---|
| **`/clear`** | 컨텍스트 초기화 | **터미널을 지우고 새 chat 시작.** 뷰만 지우는 건 <kbd>Ctrl</kbd>+<kbd>L</kbd> | 높음 |
| **되돌리기** | 대화·코드 양쪽 되돌리기 가능 | **Esc 두 번은 대화만 되감고 파일 수정은 워킹 트리에 그대로 남는다** | 최고 |
| **중첩 지침 파일** | 상위로 올라가며 모두 로드·연결 | **중첩 `AGENTS.md`를 자동 로드하지 않는다** | 최고 |
| **스킬 호출 접두사** | `/` | **`$`** (ChatGPT 표면은 `@`) | 중간 |
| **위험 플래그 이름** | `--dangerously-skip-permissions` | `--dangerously-bypass-approvals-and-sandbox` (별칭 `--yolo`) | 중간 |
| **훅 커버리지** | 29+ 이벤트 | **부분 지원** — `PreToolUse`/`PostToolUse`가 Partial | 높음 |

### 4-3. Codex에만 있는 것

`/fork`(전사 복제) · `/side`·`/btw`(임시 곁가지 chat) · `/goal`(지속 목표, **최대 4,000자**) · `/personality`(friendly/pragmatic/none) · `/raw` · `/keymap` · `/statusline` · `/title` · `/theme` · `/vim` · `/pets` · Codex cloud · Chronicle(macOS·ChatGPT Pro 한정 opt-in 리서치 프리뷰) · Computer Use · Appshots · Sites · Record & Replay · execpolicy 테스트 하네스 · **Auto-review**(모델이 승인 요청을 심사하는 별도 리뷰어 — Claude Code에 대응 없음).

### 4-4. Claude Code에만 있는 것 (커뮤니티가 지목한 결손)

`/rewind`(코드까지 되돌리기) · 중첩 지침 파일 자동 로드 · Plan Mode 기본값 시작 · 상태 표시줄 · 서브에이전트별 모델 지정(#14039 여전히 open) · 훅 완전 커버리지.

### 4-5. 구조적 차이 — 진화 방향이 갈렸다

2026년 상반기 Codex의 진화 방향이 뚜렷하다: **터미널 도구 → 데스크톱 앱 → GUI·브라우저·컴퓨터 조작·음성·전용 하드웨어.** 같은 기간 Claude Code는 CLI/SDK 중심을 유지했다. 이 대비가 책의 마지막 장 소재가 된다.

---

## 5. 실무 경험·논쟁점 (커뮤니티 + 논문)

> **규율:** 이 절의 모든 항목은 **날짜와 출처 등급**을 달고 있다. 커뮤니티 주장을 공식 문서와 같은 무게로 쓰지 마라.

### 5-1. 전환의 축을 한 문장으로

r/codex `1tao42q` (2026-05-12) PinEnvironmental6395 — 이 리서치가 찾은 가장 압축적인 정리:

> "GPT-5 is very good at doing what you say. **But if you don't tell it what you want it won't do it.** It's the **opposite tradeoff Claude makes** — good at figuring out what you want **but at the cost of doing things you didn't want it to do. You have to prompt gpt to be proactive and Claude to be non-destructive.**"

### 5-2. 전환 마찰 상위 항목 (GitHub 이슈 = 1차 소스)

| 마찰 | 이슈 | 개설일 | 👍 | 상태(2026-08-02) |
|---|---|---|---|---|
| `/rewind` 부재 — 코드가 안 돌아감 | [#11626](https://github.com/openai/codex/issues/11626) | 2026-02-12 | 192 | **open** |
| 중첩 `AGENTS.md` 미로드 (Wix·Stripe 기업 신호) | [#12115](https://github.com/openai/codex/issues/12115) | 2026-02-18 | 102 | **open** |
| 질문이 60초 뒤 자동 응답됨 | [#28969](https://github.com/openai/codex/issues/28969) | 2026-06-18 | 186 | **open** |
| 훅 커버리지 부분 지원 | [#21753](https://github.com/openai/codex/issues/21753) | 2026-05-08 | 22 | **open** |
| Plan mode 기본 시작 옵션 없음 | [#13942](https://github.com/openai/codex/issues/13942) | 2026-03-08 | 34 | **open** |
| Claude 설정 마이그레이션이 사용자 config 덮어씀 | [#24515](https://github.com/openai/codex/issues/24515) | 2026-05-26 | 0 | **open** |
| 스킬 메타데이터 컨텍스트 예산 2% 하드코딩 | [#19679](https://github.com/openai/codex/issues/19679) | 2026-04-26 | 31 | **open** |

**전환 포기 사유로 직접 언급된 댓글** (#12115) — 이 책의 핵심 증거:

- anrooo (2026-05-15): "**This is keeping me from switching from Claude Code**, it's really tough to have pretty well-configured AGENTS.md files everywhere only to have Codex ignore them entirely."
- leonardo-panseri (2026-06-04): "**Will be staying on Claude Code until this is fixed.**"

**한국어 1차 증언 (유일)** — 코유키1357, dcinside 특이점갤, 2026-04-28:

> "코덱스의 경우 hook은 있는데 rules가 없어 **각 폴더 루트마다 AGENTS.md를 작성해야하고** 이로 인해 프롬프트 관리가 까다로워지는 문제가 있음"

### 5-3. 논쟁 A — "코드 리뷰는 Codex" (가장 널리 퍼진 통념, 그런데 반증이 있다)

**관점 A (다수):** superfrank (HN, 2026-05-15): "Claude is far better at **front end design**. ... Codex is far better at **code review and catching bugs that actually matter**." / bottlepalm (HN, 2026-07-08): "**Codex for code reviews because it is pedantic**".

**관점 B (자기 반증 — 중요):** Ok_Economist3865 (r/codex, 2026-03-17): GPT-5.2로 Opus 코드를 리뷰하면 지적률 90%였는데, **Anthropic 공식 프롬프트 가이드대로 자기 프롬프트를 고치자 25~40%로 떨어졌다.**
→ "Codex 리뷰가 많이 잡는다"의 상당 부분이 **프롬프트 품질 문제**였다는 뜻이다. 다만 역방향 비대칭은 남는다.

### 5-4. 논쟁 B — 실행 스타일 (정면 충돌, 병기 필수)

- **관점 A:** AWS 한국 기술블로그 (Kyutae Park, AWS AI 스페셜리스트 SA, 2026-06-11, **국내 최고 신뢰 소스 — 실명·소속**): Claude는 "단일 패스 작성자"(정찰 없이 700~800줄 한 번에), Codex는 "장인적 접근"(`pwd`/`ls` 정찰 후 `apply_patch`, 자가 검증).
- **관점 B:** chandureddyvari (HN, 2026-02-03): "Codex feels **lazy** - I have to explicitly tell it to research existing code before it stops giving hand-wavy answers."
- **관점 C (조건부 반박):** imperfectlyAware (2026-04-24, macOS/Swift/레거시 ObjC): "Codex ... **replicates existing functionality and ignores existing patterns** ... produces GitHub tutorial code."
→ **코드베이스 성격(레거시·자체 프레임워크 여부)이 변수**로 보인다. 단정하지 마라.

### 5-5. 논쟁 C — 지시 준수 (판정 유보, 버전마다 뒤집힘)

같은 스레드에서 하루 차이로 정반대 증언이 나온다: NootropicDiary(Sol=경직) vs xoStardustt("**Sol tends to go apeshit and refactor half my code ... even with an agents.md that explicitly forbids** cleanup/refactor").
→ **"버전 X 시점 기준" 없이 서술하면 안 된다.**

### 5-6. 🕒 요금·한도 — 이 책에서 가장 위험한 서술 영역

**연대기가 중요하다. 어떤 수치도 날짜 없이 인용하면 안 된다.**

- **2026년 상반기 지배적 서사:** "Codex 한도가 훨씬 넉넉하다" (esperent, HN 2026-04-29: "probably 2x at least" — ⚠️ 측정 조건 불명)
- **그런데 2026-04-10에 이미 개인 단위 반전이 있었다:** maraluke (r/codex) — 제목은 "한도 때문에 Codex로 갈아탔다"인데 본문 끝은 "**melted my 5h limit with 3 prompts... switching right back to Claude Code lol**"
- **2026-06-16 전후 역전 사건:** [#28879](https://github.com/openai/codex/issues/28879) (2026-06-18 개설, 👍 **362**, 💬 210, **open**) — 이 리서치에서 발견한 **가장 정량적이고 신뢰 높은 커뮤니티 항목**. 세션 로그의 `token_count`·`rate_limits` 이벤트를 직접 비교했고, 보고자가 **대안 가설(리즈닝 강도·컨텍스트 팽창·설정 변경·주간 캡)을 명시적으로 배제**했다.

  | 날짜 | 입력 토큰 | 리즈닝 토큰 | 5시간 한도 소모 |
  |---|---|---|---|
  | 06-12 06:51 | 57,112 | 3,645 | 9%→11% |
  | 06-18 07:22:30 | 20,480 | **0** | **45%** |
  | 06-18 07:22:50 | 23,839 | **0** | **77%** |

- **2026-07:** [#34035](https://github.com/openai/codex/issues/34035) "5시간 한도 임시 해제의 영구화 요구" (2026-07-18, 👍 131, open) → **7월 시점에 5시간 한도가 일시 해제된 기간이 있었음을 시사.**

⚠️ **판정:** 이 "10~20배 급등" 주장은 **공식 문서로 확인도 반박도 불가능하다.** `/codex/enterprise/usage-limits`에 수치가 없고 `/codex/pricing`은 현재 값만 보여준다. 책에 쓴다면 반드시 **"커뮤니티 관측"으로 귀속하고 1차 확인 불가를 병기**하라. 등급 ⚠️.

### 5-7. MCP 마이그레이션 — 진짜 함정은 문법이 아니라 컨텍스트다

- buildxjordan (2026-02-11): MCP 8개를 그대로 옮기면 세션이 **컨텍스트 90-91%에서 시작**하고, `[features] search_tool = true`로 **99%까지 회복**된다.
- ChoasMaster777 (2026-03-19): 선언 안 된 MCP가 `rg`로 폴백해 **메모리 100GB**.
- tokovar (2026-07-13): 상주 MCP 서버 하나가 Sol을 **3시간** 멈춤 (자가 진단 프롬프트 공개).
- Prestigiouspite (2026-03-07): WSL에서 Windows `config.toml`이 쓰여 "**MCP etc. not being configured correctly**" — [#13762](https://github.com/openai/codex/issues/13762)의 경로 문제가 MCP 오설정으로 이어지는 인과.

### 5-8. 현장 노하우 (커뮤니티 합의에 가까운 것들)

1. **설정을 이중 관리하지 마라** — 사용자 레벨 `AGENTS.md`가 `CLAUDE.md`를 가리키게 하고, 스킬 디렉터리는 스크립트로 동기화 (steve-atx-7600, HN 2026-07-09).
2. **샌드박스를 끄지 말고 구멍을 뚫어라** — miki123211 (HN, 2026-07-14): "You can **poke specific holes in the sandbox** (E.G. my Codex one can write to `~/go`, `~/.cache` and `~/.cargo`). You can have **explicit deny rules**..."
3. **"커밋은 하되 푸시는 하지 마"를 컨텍스트에 박아라** — `/rewind` 부재에 대한 실질적 대응 (suparious, #11626): "I also always engineer in '**COMMIT but do not PUSH**' in the context too. That way **I am always the gatekeeper.**"
4. **깨끗한 git 트리에서 시작하라** — 같은 출처.
5. **태스크를 "커밋 하나 크기"로 쪼개라** (tunesmith, HN 2026-06-13). 커뮤니티가 확보한 클라우드 위임 성공 사례는 **전부 커밋~MR 한 개 크기**였다.
6. **교차 리뷰** — 다른 모델 계열은 "서로 다른 맹점"을 가진다 (AWS 블로그). 단 반론도 있다 (BloondAndDoom: 같은 모델에 "check again"을 반복해도 된다).
7. **스킬 설명문을 다이어트하라** — 2% 예산. aldegad 실측: 총 페이로드 **15,822자 → 13,992자**로 줄이자 경고 소멸.

### 5-9. 클라우드 위임의 고유 리스크

ModernMech (HN, 2026-07-26): "**same prompting, same model, totally different results because they changed the cloud tool's resource limits**"
→ **클라우드는 실행 환경이 공급자 소유라, 내 쪽 변경 없이도 어제와 다른 도구가 된다.** 위임 축의 핵심 리스크로 책에 반드시 실을 것.

### 5-10. 학술적 근거 (보조 소스 — 정확한 조건과 함께만 인용)

**① 이 책의 존재 이유** — Gorinova et al., arXiv:2606.17799 (2026, 📄 preprint): 코딩 벤치마크가 모델의 몫과 하네스·컨텍스트·환경의 몫을 구분하지 못한다. **하네스 요소 하나를 바꾸는 것이 모델 세대를 통째로 올리는 것만큼 점수를 바꾼다.**

**② 인터페이스가 성능이다** — Yang et al., SWE-agent, NeurIPS 2024 (✅ peer-reviewed), arXiv:2405.15793. 모델을 바꾸지 않고 인터페이스만 설계해 성능을 크게 올렸다.

**③ 체감과 실측이 갈린다** — Becker, Rush, Barnes, Rein (METR), arXiv:2507.09089 (2025, 📄 preprint):

> "Before starting tasks, developers forecast that allowing AI will reduce completion time by 24%. After completing the study, developers estimate that allowing AI reduced completion time by 20%. Surprisingly, we find that allowing AI actually increases completion time by 19%—AI tooling slowed developers down."

⚠️ **조건을 반드시 함께 적어라:** 숙련 개발자 **16명**, **246개** 과제, **평균 5년간 다뤄온 자기 저장소**, 2025년 2~6월 도구 기준. 즉 **AI에게 가장 불리한 조건**이며 낯선 코드베이스로 일반화할 수 없다.

**④ 생산성 RCT 3편이 서로 충돌한다 — 이건 한계가 아니라 발견이다:** +55.8%(2023, Copilot, 그린필드 단일 과제, GitHub/MS 소속 저자 포함) / +21%(2024, Google 사내, 96명, 저자가 신뢰구간 넓다고 명시) / **−19%**(2025, METR). **평균을 내려 하지 마라.** 조건이 다르면 결과가 뒤집힌다는 것이 이 셋이 함께 말하는 바다.

**⑤ 리더보드를 믿지 마라** — Aleithan et al., SWE-Bench+, arXiv:2410.06992 (2024, 📄): 성공 패치의 **32.67%가 이슈에 답이 적혀 있었고**, 문제 인스턴스 제거 시 해결률이 **12.47% → 3.97%**로 붕괴. 저자들은 이 결함이 **SWE-bench Verified에도 남아 있다**고 명시.

**⑥ 사내 코드베이스는 더 어렵다** — Deng et al., SWE-Bench Pro, arXiv:2509.16941 (2025, 📄): 공개 세트 **GPT-5 23.3%** vs 상업 저장소 세트 **GPT-5 14.9%**. 프런티어 모델도 Pass@1 25% 미만.

**⑦ 가드레일은 프레임워크가 아니라 모델에 있다** — Singh, Yang, Chen, IssueTrojanBench, arXiv:2607.20759 (2026-07-22, 📄): **Cursor, Claude Code, Codex Desktop을 이름으로 직접 평가한 유일한 최신 학술 벤치마크.** 악의적 이슈의 **66.5%가 모든 가드레일 통과**, 그리고 "**rejection is almost entirely from LLMs rather than the agent frameworks**".
→ **CLI 설정으로 안전을 살 수 없다**는 뜻이다. 단 66.5%는 "이 벤치마크가 설계한 공격 시나리오 기준"임을 병기하라.

**⑧ OpenAI 자신의 숫자** — "Addendum to GPT-5.2 System Card: GPT-5.2-Codex" (2025-12-18, 벤더 자체 보고):

> "Simple instructions like 'clean the folder' or 'reset the branch' can mask dangerous operations (rm -rf, git clean -xfd, git reset –hard, push –force) that lead to data loss, repo corruption, or security boundary violations."

destructive action avoidance: gpt-5-codex **0.66** → gpt-5.1-codex 0.70 → gpt-5.1-codex-max 0.75 → **gpt-5.2-codex 0.76**.
→ **최신 모델도 약 4회 중 1회는 파괴적 행동을 피하지 못한다.** 승인 모드 챕터의 최강 근거다.
⚠️ **중요한 부재:** 이 애드덤에는 **프롬프트 인젝션 정량 평가표가 없다.** "OpenAI가 인젝션 방어율 N%를 보고했다"고 쓰면 **거짓이 된다.**

**⑨ 조용한 부채** — Liu et al., arXiv:2603.28592 (2026, 📄): AI 작성 커밋 **302.6천 건**(저장소 6,299개) 분석, 총 **484,366건** 이슈, 그중 **89.3%가 코드 스멜**, 추적된 이슈의 **22.7%가 최신 버전에도 생존**.
→ Codex가 만드는 문제는 대개 극적 사고가 아니라 **조용한 부채**다.

**⑩ 결국 소유는 사람이 한다** — Sawada et al., EASE 2026 (✅ peer-reviewed), arXiv:2605.06464: AI 코드든 사람 코드든 **유지보수의 대부분은 사람 개발자가 수행**한다.

### 5-11. ⚠️ 문서와 어긋나는 현장 보고 (fact-checker 대조 필수)

| # | 문서가 말하는 것 | 현장 보고 | 출처 | 상태 |
|---|---|---|---|---|
| 1 | (AGENTS.md 표준) 가장 가까운 파일을 자동으로 읽는다 | Codex는 중첩 AGENTS.md를 자동 로드하지 않는다 | [#12115](https://github.com/openai/codex/issues/12115) | open |
| 2 | 커스텀 서브에이전트는 `.codex/agents/*.toml`의 `name`으로 지정 | `spawn_agent`가 일반 `agent_type`만 받아 이름 지정 불가 — "That is **not the behavior the docs imply**" | [#15250](https://github.com/openai/codex/issues/15250) | open (CLI 0.144.1에서 재현) |
| 3 | Pro는 Plus 대비 "5x or 20x higher rate limits" | 실사용이 그 표현과 "materially inconsistent"하다는 보고 | [#28879](https://github.com/openai/codex/issues/28879) | open |
| 4 | GPT-5.6 Sol 컨텍스트 1.05M 광고 | 실측 353K → 258K | [#32806](https://github.com/openai/codex/issues/32806) | closed — 회복 여부 확인 필요 |
| 5 | 훅 이벤트 "지원" | `PreToolUse`/`PostToolUse`가 **Partial** — "coverage must be consistent across every tool handler, **not only selected paths**" | [#21753](https://github.com/openai/codex/issues/21753) | open |
| 6 | Claude 설정 마이그레이션 | 프로젝트 설정이 없을 때 **사용자 레벨** `~/.codex/config.toml`을 덮어써 승인 폭탄 발생 | [#24515](https://github.com/openai/codex/issues/24515) | open |
| 7 | Codex Security CLI는 로컬 CLI | 벤더 확인: "**this isn't an offline scanner** ... code and context ... **sent to the hosted model**" | HN 49089755 (2026-07-29) | 초기 버전 |

---

## 6. 참고문헌

### 6-1. 공식 문서 URL 전수 (148개, base: `https://learn.chatgpt.com`)

> 각 경로 끝에 `.md`를 붙이면 원문 markdown을 받을 수 있다. 원문 캐시는 `research/codex-docs-raw/`.

#### A. 기초·개념·제품 표면 (web-1.md)

| # | URL | 확인 등급 | 비고 |
|---|---|---|---|
| 1 | `/codex` | 🟢 원문(.md) |  |
| 2 | `/codex/quickstart` | 🟢 원문(.md) |  |
| 3 | `/codex/use-chatgpt` | 🟢 원문(.md) |  |
| 4 | `/codex/get-started-with-work` | 🟢 원문(.md) |  |
| 5 | `/codex/import` | 🟢 원문(.md) | ⚠️ `.md`가 HTML보다 **짧다** — 일부 문장은 HTML에만 존재 |
| 6 | `/codex/prompting` | 🟢 원문(.md) |  |
| 7 | `/codex/personalize` | 🟢 원문(.md) |  |
| 8 | `/codex/skills-and-plugins` | 🟢 원문(.md) |  |
| 9 | `/codex/permission-modes` | 🟢 원문(.md) |  |
| 10 | `/codex/whats-new` | 🟢 원문(.md) |  |
| 11 | `/codex/models` | 🟢 원문(.md) |  |
| 12 | `/codex/pricing` | 🟢 원문(.md) |  |
| 13 | `/codex/glossary` | 🟢 원문(.md) |  |
| 14 | `/codex/app` | 🟢 원문(.md) |  |
| 15 | `/codex/web` | 🟢 원문(.md) |  |
| 16 | `/codex/cli` | 🟢 원문(.md) |  |
| 17 | `/codex/ide` | 🟢 원문(.md) |  |
| 18 | `/codex/cloud` | 🟢 원문(.md) |  |
| 19 | `/codex/changelog` | 🟢 원문(HTML) | `.md` 404 → HTML 복원 |
| 20 | `/codex/feature-maturity` | 🟢 원문(.md) |  |
| 21 | `/codex/open-source` | 🟢 원문(.md) |  |
| 22 | `/codex/features` | 🟢 원문(.md) |  |
| 23 | `/codex/projects` | 🟢 원문(.md) |  |
| 24 | `/codex/visualizations` | 🟢 원문(.md) |  |
| 25 | `/codex/automations` | 🟢 원문(.md) |  |
| 26 | `/codex/long-running-work` | 🟢 원문(.md) |  |
| 27 | `/codex/notifications` | 🟢 원문(.md) |  |
| 28 | `/codex/pets` | 🟢 원문(.md) |  |
| 29 | `/codex/features/codex-micro` | 🟢 원문(.md) |  |
| 30 | `/codex/browser` | 🟢 원문(.md) |  |
| 31 | `/codex/computer-use` | 🟢 원문(.md) |  |
| 32 | `/codex/features/voice` | 🟢 원문(.md) |  |
| 33 | `/codex/plugins` | 🟢 원문(.md) |  |

#### B. 기능·레퍼런스·설정·커스터마이징 (web-2.md)

| # | URL | 확인 등급 | 비고 |
|---|---|---|---|
| 34 | `/codex/web-search` | 🟢 원문(.md) |  |
| 35 | `/codex/image-generation` | 🟢 원문(.md) |  |
| 36 | `/codex/image-inputs` | 🟢 원문(.md) |  |
| 37 | `/codex/appshots` | 🟢 원문(.md) |  |
| 38 | `/codex/chrome-extension` | 🟢 원문(.md) |  |
| 39 | `/codex/artifacts-viewer` | 🟢 원문(.md) | 실제 제목은 **"Work with files"** |
| 40 | `/codex/reference/commands` | 🟢 원문(.md) |  |
| 41 | `/codex/reference/slash-commands` | 🟢 원문(.md) |  |
| 42 | `/codex/reference/settings` | 🟢 원문(.md) |  |
| 43 | `/codex/reference/troubleshooting` | 🟢 원문(.md) |  |
| 44 | `/codex/configuration` | 🟢 원문(.md) |  |
| 45 | `/codex/customization/overview` | 🟢 원문(.md) |  |
| 46 | `/codex/customization/memories` | 🟢 원문(.md) |  |
| 47 | `/codex/customization/chronicle` | 🟢 원문(.md) |  |
| 48 | `/codex/config-file/config-basic` | 🟢 원문(.md) |  |
| 49 | `/codex/config-file/config-advanced` | 🟢 원문(.md) |  |
| 50 | `/codex/config-file/config-reference` | 🟢 원문(.md) | `ConfigTable` 2개 복원 → **config.toml 274키 + requirements.toml 116키** |
| 51 | `/codex/config-file/environment-variables` | 🟢 원문(.md) |  |
| 52 | `/codex/config-file/config-sample` | 🟢 원문(.md) |  |
| 53 | `/codex/agent-configuration/agents-md` | 🟢 원문(.md) |  |
| 54 | `/codex/agent-configuration/subagents` | 🟢 원문(.md) |  |
| 55 | `/codex/agent-configuration/speed` | 🟢 원문(.md) |  |
| 56 | `/codex/agent-configuration/rules` | 🟢 원문(.md) |  |
| 57 | `/codex/extend/record-and-replay` | 🟢 원문(.md) |  |
| 58 | `/codex/extend/mcp` | 🟢 원문(.md) |  |
| 59 | `/codex/windows/windows-app` | 🟢 원문(.md) |  |
| 60 | `/codex/windows/windows-sandbox` | 🟢 원문(.md) |  |
| 61 | `/codex/windows/wsl` | 🟢 원문(.md) |  |
| 62 | `/codex/cli-customization` | 🟢 원문(.md) |  |
| 63 | `/codex/developer-commands` | 🟢 원문(.md) | `ConfigTable` **29개 복원(174행)** |
| 64 | `/codex/developer-settings` | 🟢 원문(.md) |  |
| 65 | `/codex/hooks` | 🟢 원문(.md) |  |
| 66 | `/codex/build-skills` | 🟢 원문(.md) |  |
| 67 | `/codex/build-plugins` | 🟢 원문(.md) |  |

#### C. 개발자 도구·환경·SDK·통합 (web-3.md)

| # | URL | 확인 등급 | 비고 |
|---|---|---|---|
| 68 | `/codex/developers` | 🟢 원문(.md) |  |
| 69 | `/codex/code-review` | 🟢 원문(.md) |  |
| 70 | `/codex/integrated-terminal` | 🟢 원문(.md) |  |
| 71 | `/codex/environments/modes` | 🟢 원문(.md) |  |
| 72 | `/codex/environments/local-environment` | 🟢 원문(.md) |  |
| 73 | `/codex/environments/cloud-environment` | 🟢 원문(.md) |  |
| 74 | `/codex/environments/git-worktrees` | 🟢 원문(.md) |  |
| 75 | `/codex/codex-sdk` | 🟢 원문(.md) |  |
| 76 | `/codex/app-server` | 🟢 원문(.md) |  |
| 77 | `/codex/mcp-server` | 🟢 원문(.md) |  |
| 78 | `/codex/github-action` | 🟢 원문(.md) |  |
| 79 | `/codex/non-interactive-mode` | 🟢 원문(.md) |  |
| 80 | `/codex/third-party/github` | 🟢 원문(.md) |  |
| 81 | `/codex/third-party/slack` | 🟢 원문(.md) |  |
| 82 | `/codex/third-party/linear` | 🟢 원문(.md) |  |
| 83 | `/codex/remote-connections` | 🟢 원문(.md) |  |
| 84 | `/codex/amazon-bedrock` | 🟢 원문(.md) |  |
| 85 | `/codex/use-cases` | 🟡 목록 추출 | `.md` 미제공(동적 SPA). 항목·URL·날짜는 신뢰 가능, **개수 단정 금지** |
| 86 | `/codex/use-cases/collections` | 🟡 목록 추출 | `.md` 미제공(동적 SPA). 항목·URL·날짜는 신뢰 가능, **개수 단정 금지** |
| 87 | `/codex/resources` | 🟡 목록 추출 | `.md` 미제공(동적 SPA). 항목·URL·날짜는 신뢰 가능, **개수 단정 금지** |
| 88 | `/codex/videos` | 🟡 목록 추출 | `.md` 미제공(동적 SPA). 항목·URL·날짜는 신뢰 가능, **개수 단정 금지** |

#### D. 보안·권한·샌드박스·Security 제품 (web-4.md)

| # | URL | 확인 등급 | 비고 |
|---|---|---|---|
| 89 | `/codex/security-administration` | 🟢 원문(.md) |  |
| 90 | `/codex/permissions` | 🟢 원문(.md) |  |
| 91 | `/codex/sandboxing` | 🟢 원문(.md) |  |
| 92 | `/codex/sandboxing/auto-review` | 🟢 원문(.md) |  |
| 93 | `/codex/agent-approvals-security` | 🟢 원문(.md) |  |
| 94 | `/codex/cloud/internet-access` | 🟢 원문(.md) |  |
| 95 | `/codex/security` | 🟢 원문(.md) |  |
| 96 | `/codex/security/plugin` | 🟢 원문(.md) |  |
| 97 | `/codex/security/plugin/workbench` | 🟢 원문(.md) |  |
| 98 | `/codex/security/plugin/scans` | 🟢 원문(.md) |  |
| 99 | `/codex/security/plugin/deep-scans` | 🟢 원문(.md) |  |
| 100 | `/codex/security/plugin/code-changes` | 🟢 원문(.md) |  |
| 101 | `/codex/security/plugin/triage-backlog` | 🟢 원문(.md) |  |
| 102 | `/codex/security/plugin/fix-findings` | 🟢 원문(.md) |  |
| 103 | `/codex/security/plugin/export-findings` | 🟢 원문(.md) |  |
| 104 | `/codex/security/plugin/vulnerability-reports` | 🟢 원문(.md) |  |
| 105 | `/codex/security/plugin/security-hardening` | 🟢 원문(.md) |  |
| 106 | `/codex/security/plugin/changelog` | 🟢 원문(.md) |  |
| 107 | `/codex/security/setup` | 🟢 원문(.md) |  |
| 108 | `/codex/security/threat-model` | 🟢 원문(.md) |  |
| 109 | `/codex/security/faq` | 🟢 원문(.md) |  |
| 110 | `/codex/security/cli` | 🟢 원문(.md) |  |
| 111 | `/codex/security/cli/bulk-scans` | 🟢 원문(.md) |  |
| 112 | `/codex/security/cli/reference` | 🟢 원문(.md) |  |
| 113 | `/codex/security/cli/ci` | 🟢 원문(.md) |  |
| 114 | `/codex/security/cli/faq` | 🟢 원문(.md) |  |
| 115 | `/codex/security/sdk` | 🟢 원문(.md) |  |
| 116 | `/codex/cyber-safety` | 🟢 원문(.md) |  |

#### E. 엔터프라이즈·관리·인증 (web-5.md)

| # | URL | 확인 등급 | 비고 |
|---|---|---|---|
| 117 | `/codex/administration` | 🟢 원문(.md) |  |
| 118 | `/codex/enterprise/admin-setup` | 🟢 원문(.md) |  |
| 119 | `/codex/enterprise/work-admin-faq` | 🟢 원문(.md) |  |
| 120 | `/codex/auth` | 🟢 원문(.md) |  |
| 121 | `/codex/enterprise/access-tokens` | 🟢 원문(.md) |  |
| 122 | `/codex/enterprise/groups-and-provisioning` | 🟢 원문(.md) |  |
| 123 | `/codex/enterprise/roles-and-workspace-permissions` | 🟢 원문(.md) |  |
| 124 | `/codex/enterprise/managed-configuration` | 🟢 원문(.md) |  |
| 125 | `/codex/hipaa-configuration` | 🟢 원문(.md) |  |
| 126 | `/codex/enterprise/workspace-model-availability` | 🟢 원문(.md) |  |
| 127 | `/codex/enterprise/apps-and-connectors` | 🟢 원문(.md) |  |
| 128 | `/codex/enterprise/skills` | 🟢 원문(.md) |  |
| 129 | `/codex/enterprise/governance` | 🟢 원문(.md) |  |
| 130 | `/codex/enterprise/workspace-analytics` | 🟢 원문(.md) |  |
| 131 | `/codex/enterprise/analytics-api` | 🟢 원문(.md) |  |
| 132 | `/codex/enterprise/compliance-api` | 🟢 원문(.md) |  |
| 133 | `/codex/enterprise/windows-deployment` | 🟢 원문(.md) |  |

#### F. 색인 대조로 추가 발견 (web-6.md)

| # | URL | 확인 등급 | 비고 |
|---|---|---|---|
| 134 | `/codex/cli/reference` | 🟢 원문(.md) | 표 29개는 `.md`에 없어 **astro-island JSON 디코드로 복원** |
| 135 | `/codex/cli/slash-commands` | 🟢 원문(.md) | `/codex/cli/reference`와 바이트 단위 동일 문서 |
| 136 | `/codex/custom-prompts` | 🟢 원문(.md) | **deprecated** — skills가 후계 |
| 137 | `/codex/enterprise/usage-limits` | 🟢 원문(.md) | **수치 전무**(37줄). help.openai.com으로 위임 |
| 138 | `/codex/learn/best-practices` | 🟢 원문(HTML) | `.md` 404 → HTML 복원 |
| 139 | `/codex/overview` | 🟢 원문(HTML) | `.md` 404 → HTML 복원 / `/docs` 랜딩 — 산문 거의 없음 |
| 140 | `/codex/app/commands` | 🟢 원문(.md) | `/codex/reference/commands`와 동일 |
| 141 | `/codex/app/settings` | 🟢 원문(.md) | `/codex/reference/settings`와 동일 |
| 142 | `/codex/app/windows` | 🟢 원문(.md) | `/codex/windows/windows-app`와 동일 |
| 143 | `/codex/ide/commands` | 🟢 원문(.md) | `/codex/ide/slash-commands`와 동일 |
| 144 | `/codex/ide/settings` | 🟢 원문(.md) |  |
| 145 | `/codex/ide/slash-commands` | 🟢 원문(.md) | `/codex/ide/commands`와 동일 |
| 146 | `/codex/sites` | 🟢 원문(.md) |  |
| 147 | `/codex/community/codex-for-oss` | 🟢 원문(HTML) | `.md` 404 → HTML 복원 |
| 148 | `/codex/guides/build-ai-native-engineering-team` | 🟢 원문(HTML) | `.md` 404 → HTML 복원 |

### 6-2. 확인 등급 범례

| 등급 | 뜻 |
|---|---|
| 🟢 원문(.md) | 경로 끝 `.md`로 받은 **무손실 원문 markdown**. 코드블록·표·인용문을 그대로 책에 실어도 안전 |
| 🟢 원문(HTML) | `.md` 미제공 → HTML을 변환해 복원. 본문 신뢰 가능 |
| 🟡 목록 추출 | 동적 SPA 목록 페이지. 항목명·URL·날짜는 신뢰 가능하나 **개수를 단정하지 말 것** |

**커버리지 집계: 148 URL 배정 / 148 수집 성공 / 접근 실패 0건.**
단, 148개 URL은 **별칭 중복을 포함**한다 — `/codex/cli/reference` ≡ `/codex/cli/slash-commands`처럼 바이트 단위로 같은 문서가 6쌍 있어, **고유 문서 수는 약 140개**다. 책에서 두 URL을 별개 문서로 취급하지 마라.

### 6-3. 커뮤니티 1차 소스 (등급별)

**최상급 — GitHub `openai/codex` 이슈** (재현 절차·로그·대조군이 있는 것):

| 이슈 | 주제 | 개설일 | 👍 | 상태 |
|---|---|---|---|---|
| [#28879](https://github.com/openai/codex/issues/28879) | 레이트리밋 단가 급등 (세션 로그 기반, 대안가설 배제) | 2026-06-18 | 362 | open |
| [#11626](https://github.com/openai/codex/issues/11626) | `/rewind` 부재 | 2026-02-12 | 192 | open |
| [#28969](https://github.com/openai/codex/issues/28969) | 질문 60초 자동 응답 | 2026-06-18 | 186 | open |
| [#31814](https://github.com/openai/codex/issues/31814) | 서브에이전트 모델 지정 불가 (원인 PR까지 특정) | 2026-07-09 | 167 | closed |
| [#12115](https://github.com/openai/codex/issues/12115) | 중첩 AGENTS.md (Wix·Stripe 기업 신호) | 2026-02-18 | 102 | open |
| [#28190](https://github.com/openai/codex/issues/28190) | macOS가 `rg` 차단 (해결책 재현됨) | 2026-06-14 | 79 | open |
| [#13762](https://github.com/openai/codex/issues/13762) | WSL 모드 `CODEX_HOME`·워크트리 경로 | 2026-03-06 | 55 | open |
| [#19679](https://github.com/openai/codex/issues/19679) | 스킬 메타데이터 2% 하드코딩 (코드 위치·실측) | 2026-04-26 | 31 | open |
| [#21753](https://github.com/openai/codex/issues/21753) | 훅 패리티 (이벤트 매트릭스) | 2026-05-08 | 22 | open |
| [#15250](https://github.com/openai/codex/issues/15250) | 커스텀 서브에이전트가 문서대로 호출 안 됨 | 2026-03-20 | 16 | open |
| [#24515](https://github.com/openai/codex/issues/24515) | 마이그레이션이 사용자 config 덮어씀 | 2026-05-26 | 0 | open |

**국내 최고 신뢰 소스:** AWS 한국 기술블로그 — Kyutae Park, Ph.D (AWS AI 스페셜리스트 SA), 2026-06-11, https://aws.amazon.com/ko/blogs/tech/codex-claudecode-harness/ — **실명·소속이 있는 유일한 국내 심층 비교 자료.**

**한국어 전환 마찰 1차 증언 (유일):** 코유키1357, dcinside 특이점갤, 2026-04-28 (조회 7,507).

**그 외:** Hacker News 댓글·스토리 다수(전부 Algolia API 직접 조회), Reddit r/codex·r/ClaudeAI 원문 59개(Atom RSS 경유 직접 확보), GeekNews 한국어 댓글, velog·브런치.
→ **전체 원장은 `research/community.md` §7, `research/community-2.md` §6에 게시일·URL·신뢰 등급과 함께 있다.**

### 6-4. 학술·기술 리포트

전체 22건의 서지 정보(저자·연도·arXiv ID/DOI·발표처·peer-review 여부)는 **`research/papers.md` §6 표**에 있다. peer-review 확인 ✅ 7편 / 📄 preprint 14편 / 벤더 자체 보고 1건.

이 책에서 인용 우선순위가 높은 것:

| 용도 | 문헌 | 등급 |
|---|---|---|
| 책의 존재 이유 | Gorinova et al., arXiv:2606.17799 (2026) | 📄 preprint |
| 인터페이스가 성능이다 | Yang et al., SWE-agent, NeurIPS 2024, arXiv:2405.15793 | ✅ |
| 체감≠실측 | Becker et al. (METR), arXiv:2507.09089 (2025) | 📄 |
| 벤치마크 오염 | Aleithan et al., arXiv:2410.06992 (2024) | 📄 |
| 사내 코드베이스는 더 어렵다 | Deng et al., arXiv:2509.16941 (2025) | 📄 |
| Codex 직접 보안 평가 | Singh et al., IssueTrojanBench, arXiv:2607.20759 (2026-07) | 📄 |
| 승인 모드 근거 | OpenAI, "Addendum to GPT-5.2 System Card: GPT-5.2-Codex" (2025-12-18) | ❌ 벤더 자체 보고 |
| CLI 에이전트 벤치마크 | Merrill et al., Terminal-Bench, ICLR 2026, arXiv:2601.11868 | ✅ |
| 조용한 부채 | Liu et al., arXiv:2603.28592 (2026) | 📄 |
| 결국 사람이 소유한다 | Sawada et al., EASE 2026, arXiv:2605.06464 | ✅ |

⚠️ **2026년 발표 논문은 거의 전부 preprint다.** 인용 시 "아직 동료 심사를 거치지 않은"이라는 단서를 붙이는 것을 권한다.

---

## 7. 리서치 한계 (커버하지 못한 영역)

### 7-1. 공식 문서가 애초에 제공하지 않는 것

이건 리서치 실패가 아니라 **문서의 부재**다. 추측으로 채우면 안 된다.

1. **한도 변경 이력.** `/codex/pricing`은 현재 값만 보여주고 `/codex/enterprise/usage-limits`에는 수치가 없다. 커뮤니티의 "2026-06 급등" 주장은 **1차 확인 불가**.
2. **Analytics API·Compliance API의 엔드포인트·스키마.** 두 페이지 모두 "This page doesn't duplicate that contract"라며 인증된 레퍼런스로 위임한다.
3. **역할·시트·권한의 구체 목록.** 문서로 확정 가능한 내장 역할은 **Owner / Admin / Member** 3개뿐이며, 나머지는 Help Center로 위임된다.
4. **발행일 메타.** 전 페이지에 발행·갱신일 표기가 없다. 유일한 버전 앵커는 본문에 박힌 `0.114` / `0.138.0`뿐.
5. **한국 지역 가용성.** 문서의 지역 언급은 **EEA·영국·스위스뿐**이다. 확정 가능한 진술은 "공식 문서에 한국 관련 명시 없음"이며, **가용/불가용 어느 쪽도 단정하지 마라.**
6. **데스크톱 버전 체계(`26.727` 형태)의 의미.** 문서에 정의가 없다.
7. **`/codex/permission-modes`의 모드별 설정값.** `PermissionModeSelectorDemo` 컴포넌트의 props가 비어 있어, `Ask for approval`의 설정(`workspace-write` / `on-request` / reviewer `user`)만 회수됐다. **나머지 3개 모드의 설정값은 JS 청크까지 뒤졌으나 없어 공백으로 남겼다.**

### 7-2. 커뮤니티 리서치의 구멍

1. **Reddit 점수·업보트가 없다.** 크롤러 차단을 Atom RSS로 우회했으나 **RSS는 업보트를 제공하지 않는다.** 즉 Reddit 인용에는 "몇 명이 동의했는지"가 빠져 있다. HN·GitHub 인용에는 지표가 있다.
2. **구조적 진영 편향.** 자료 상당수가 r/codex(Codex 진영) 또는 r/ClaudeAI(Claude 진영) 출신이다. 커뮤니티 자신이 이를 자각하고 있다("almost all of us here were once claude code users"). **비교를 다루는 이상 서브레딧 출신 자료는 항상 진영을 밝히고 인용하라.**
3. **한국어 전환 마찰 1차 후기가 거의 없다.** OKKY·회사 기술블로그(토스·카카오·우아한형제들·당근·라인)·커리어리·요즘IT는 **확인 결과 0건**으로 확정 보고됐다. 유일한 예외가 dcinside 1건. **한국 독자 공감 포인트는 저자 경험으로 메워야 한다.**
4. **몇 시간짜리 클라우드 위임 후기가 여전히 공백이다.** 확보된 성공 사례는 **전부 커밋~MR 한 개 크기**였다.
5. **동일 조건 요금 벤치마크가 없다.** "2배 넉넉하다" 류 체감 진술만 있고 조건이 통제된 비교가 없다.
6. Lobsters·Discord/Slack 공개 채널·Mastodon은 미수집.

### 7-3. 인용 금지 판정 목록 (fact-checker 인계)

리서처들이 **출처 불투명·이해충돌·검증 실패**로 인용 금지 판정한 것들이다. **책에 쓰지 마라.**

1. dev.to의 "500+ Reddit 개발자 중 65%가 Codex 선호(업보트 가중 80%)" — 표본 추출 방법·기간·서브레딧 구성 미공개.
2. r/codex의 "**2.2배**" 벤치마크 — 산출 절차 미공개 + 게시자 이해충돌.
3. "Claude Code 세션 6,852건 / 툴 콜 234,760건" — **원 GitHub 이슈 URL 확보 실패.**
4. SWE-Lancer 모델별 pass rate(GPT-4o 8.0% / Claude 3.5 Sonnet 26.2%) — **abstract에서 확인 실패.** 2차 소스 숫자를 그대로 쓰지 말 것.
5. Terminal-Bench 구체 순위 — 리더보드가 상시 갱신된다. "2026년 1월 기준 65% 미만" 정도로만.
6. Threads(qjc.ai) — **게시일 미확인**(2회 시도 실패).
7. `treesoop.com`·`litmers.com`·`blog.gridge.co.kr`·`we0.ai` 계열 — 1차 경험 확인 불가한 SEO성 정리 콘텐츠.
8. velog의 "Figma 클로닝 Claude 623만 토큰 vs Codex 150만 토큰" — **조건 불명**(프롬프트·모델·설정 미기재). 쓰려면 조건 불명을 반드시 병기.

### 7-4. 🕒 집필 직전 반드시 재확인할 항목

이 주제는 **주 단위로 변한다.** 아래는 확인하지 않으면 챕터가 통째로 틀릴 수 있는 것들이다.

1. **GPT-5.4 / GPT-5.4-mini 은퇴 (2026-08-31)** — 이 책 집필 시점엔 **이미 지난 날짜**다. Chat Completions API 지원 제거도 함께.
2. **`/rewind` (#11626)** — 이 책의 핵심 마찰인데, 해결되면 해당 절이 무효가 된다.
3. **중첩 AGENTS.md (#12115)** — Wix·Stripe 압력이 있어 우선순위가 높을 것으로 추정된다.
4. **60초 자동 응답 (#28969)** — 비활성화 옵션이 추가됐는지.
5. **요금·한도 전반 (#28879, #34035)** — 서술 전체가 여기 걸려 있다.
6. **권한 프로필의 Beta 딱지** — 정식 승격 시 §3-3을 다시 써야 한다.
7. **Codex Security** — 2026-07-28 출시, 리서치 시점 기준 **4일 차**. 기록된 함정 대부분이 초기 버그일 가능성이 높다.
8. **모델 라인업** — GPT-5.6 3종 체계 자체가 바뀔 수 있다.

---

## 신선도 원장 (소스별 발행일·버전 시점)

> **이 절이 Phase 4 fact-checker의 그라운딩이다.** `research/*.md`가 나중에 정리되더라도 여기 남는다.

### A. 공식 문서 (1차 소스)

| 항목 | 시점·버전 | 출처 |
|---|---|---|
| **전 페이지 공통** | **발행일 표기 없음. 검색 시점 2026-08-02 기준으로만 고정** | learn.chatgpt.com |
| 문서 원문 접근법 | 경로 끝 `.md` → 원문 markdown (2026-08-02 확인) | 각 페이지 상단 안내문 |
| ⚠️ `learn.chatgpt.com/llms.txt` | **404 (죽어 있음)** — 모든 `.md` 헤더가 이걸 색인으로 안내함에도 | 2026-08-02 확인 |
| ✅ 작동하는 색인 | **`developers.openai.com/llms.txt`** (Codex 경로 140개) | 2026-08-02 확인 |
| 요금 (Free/Go/Plus/Pro/Business) | `$0` / `$8` / `$20` / `$100`·`$200` / `$20`(연간, 월 `$25`) — **2026-08-02 기준** | `/codex/pricing` |
| Plus 한도 (Local Messages/5h) | Sol `10-100`, Terra `25-200`, Luna `250-2,000`, 5.5 `15-80`, 5.4 `20-100`, 5.4mini `60-350` — **2026-08-02 기준** | `/codex/pricing` |
| 크레딧 요율 | 입력 Sol/Terra/Luna **125/50/5**, 출력 **750/300/30** — 2026-08-02 기준 | `/codex/pricing` |
| 권장 모델 | `gpt-5.6-sol` / `gpt-5.6-terra` / `gpt-5.6-luna` — **GPT-5.6/2026 기준** | `/codex/models` |
| 프리뷰 모델 | `gpt-5.3-codex-spark` (ChatGPT Pro 한정) — 2026 기준 | `/codex/models` |
| 🕒 모델 은퇴 | `gpt-5.4`·`gpt-5.4-mini` **2026-08-31** (ChatGPT 로그인 한정) | `/codex/enterprise/workspace-model-availability` (models·changelog·automations 3중 일치) |
| 권한 프로필 | **Beta** — "under active development and may change" | `/codex/permissions` |
| 권한 프로필 허용목록 최소 버전 | **Codex `0.138.0`** (0.137.0 이하 무시) | `/codex/permissions`, `/codex/enterprise/managed-configuration` |
| WSL1 지원 종료 | **Codex `0.114`**까지. `0.115`부터 Linux 샌드박스 `bubblewrap` | `/codex/windows/wsl` |
| 설정 키 규모 | `config.toml` **274개** + `requirements.toml` **116개** — 2026-08-02 스냅샷 | `/codex/config-file/config-reference` |
| 공식 JSON 스키마 | `learn.chatgpt.com/docs/config-schema.json` | config-reference 링크 |
| CLI 명령 성숙도 | 28개 중 **experimental 7 / stable 21** — 2026-08-02 기준 | `/codex/cli/reference` |
| Auto-review 서킷 브레이커 | **3연속 거부 또는 최근 50건 리뷰 중 10건** | `/codex/sandboxing/auto-review` |
| Codex Security 버전 | 플러그인 **`0.1.15`**, CLI **`0.1.3`** (별개 계열) | `/codex/security/plugin/changelog` |
| Codex Security 기본 스캔 모델 | **`gpt-5.6-sol`** (유일 권장) | `/codex/security/*` |
| 사이버 안전 정책 | `GPT-5.3-Codex`가 High cybersecurity capability 최초 지정 | `/codex/cyber-safety` |
| 임포트 대상 채팅 범위 | **최근 30일** | `/codex/import` |
| 마이그레이션 `itemType` | **9종** (`AGENTS_MD`·`CONFIG`·`SKILLS`·`PLUGINS`·`MCP_SERVER_CONFIG`·`SUBAGENTS`·`HOOKS`·`COMMANDS`·`SESSIONS`) | `/codex/app-server` |
| `AGENTS.md` 바이트 예산 | `project_doc_max_bytes = 32768` | `/codex/config-file/config-reference` |
| `/goal` 목표 상한 | **4,000자** | `/codex/cli/reference` |
| CLI 로그인 콜백 포트 | **`localhost:1455`** | `/codex/auth` |
| access token 만료 | 최단 **1일**, 권장 **7/30/60/90일**, 플랜 **Business·Enterprise** | `/codex/enterprise/access-tokens` |
| ChatGPT Work 출시 | **2026-07-09** | `/codex/enterprise/work-admin-faq` |
| Codex 앱 → ChatGPT 데스크톱 앱 병합 | **2026-07-09** | `/codex/whats-new` |
| Codex Micro 출시 | **2026-07-15** | `/codex/whats-new` |
| Codex 앱 macOS 출시 | 2026-02-02~06 / Windows 네이티브 2026-03-02~06 | `/codex/whats-new` |
| changelog 규모 | **95개 항목** 날짜+제목 전수 색인 확보 | `/codex/changelog` |
| OpenAI 내부 코드리뷰 | "At OpenAI, Codex reviews 100% of PRs." — 출처 표기 없는 자체 주장 | `/guides/best-practices` |
| ⚠️ METR 인용 (문서 경유) | "**2시간 17분 / 약 50% 신뢰도**, **2025년 8월 기준**" — **METR 연구이지 OpenAI 측정이 아니다.** 2026-08 시점 기준 **1년 묵음** 🕒 | `/guides/build-ai-native-engineering-team` |
| ⚠️ 출처 미표기 수치 | "주당 2~5시간 코드리뷰" — 원문에 출처 없음 | 동상 |

### B. 커뮤니티 (게시일 필수)

| 항목 | 게시일 | 신선도 |
|---|---|---|
| 레이트리밋 급등 #28879 | 2026-06-18 (사건은 2026-06-16 전후) | 신선 |
| 5시간 한도 임시 해제 논의 #34035 | 2026-07-18 | 매우 신선 |
| Codex Security 출시 HN 스레드 | 2026-07-28 (596 pts) | **4일 차 — 상태 변동 확률 최고** 🕒 |
| Sol 세대 지시 준수 논쟁 | 2026-07-09~20 | 매우 신선 |
| AWS 한국 기술블로그 비교 | 2026-06-11 | 신선 |
| 한국어 전환 마찰 증언(dcinside) | 2026-04-28 | 신선 |
| 리뷰 프롬프트 자기 반증(90%→25~40%) | 2026-03-17 | 신선 |
| MCP 컨텍스트 90-91%→99% | 2026-02-11 | 경계선 |
| 글로벌 AGENTS.md 미로드 #8759 | 2026-01-05 개설 → **2026-01-07 closed** | ⏳ **해소됨** |
| HN 리뷰 극찬 댓글 다수 | 2025-10~12 | ⏳ **오래됨** |

### C. 학술 (발행 연도·심사 상태)

`research/papers.md` §6 표가 정전이다. 요약: ✅ peer-reviewed 7편 / 📄 preprint 14편 / 벤더 보고 1건.
⏳ **낡음 표시 필수 항목:** SWE-bench 1.96%(2023) · SWE-agent 12.5%(2024) · Agentless 32%(2024) · Copilot 40% 취약(2021) · Claude 3.7 Sonnet 50분 시간 지평(2025-03). **역사 서술로만 쓰고 현재 Codex 성능의 근거로 쓰지 마라.**

### D. 리서치 수행 메타

| 항목 | 값 |
|---|---|
| 검색 수행일 | **2026-08-02** |
| 공식 문서 URL | 148 배정 / 148 수집 / 실패 0 (고유 문서 약 140) |
| 원문 무손실 캐시 | `research/codex-docs-raw/` **69개 파일** |
| 커뮤니티 고유 출처 | 약 165개 (community.md 77 + community-2.md 88) |
| 학술·기술 리포트 | 22건 |
| 리서처 구성 | web ×6 (그룹 A~F) + community ×2 + paper ×1 |
