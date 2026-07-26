# 커뮤니티 리서치: MCP 서버 개발 실무 (토픽 4·5·6 + 논쟁점)

> **검색 시점: 2026-07-26 기준.** MCP는 변화가 빠르다 — 아래 모든 인용에 **작성일**을 병기했고, 오래된 글은 "{날짜} 시점 기준"으로 못 박았다.
> **담당 범위:** 토픽 4(클라이언트 연결 실무) · 토픽 5(디버깅·모니터링) · 토픽 6(MCP 서버가 코딩 에이전트를 호출하는 패턴) + 논쟁점 수집.
>
> **수집 방법론 (재현 가능하게 기록):** SEO 요약 블로그를 걷어내고 **1차 소스**로 갔다 — (1) `gh search issues/repos` + `gh issue view`로 `anthropics/claude-code` 이슈 본문·댓글을 날짜와 함께 직접 수집, (2) `anthropics/claude-code`의 `CHANGELOG.md`를 API로 내려받아 MCP 항목을 **버전 번호에 매핑**, (3) HN Algolia API(`hn.algolia.com/api/v1`)로 스레드 메타(점수·댓글수·작성일)와 댓글 본문을 직접 수집, (4) GeekNews 스레드 직접 열람. 그 결과 아래 대부분의 인용은 **작성일과 버전이 붙은 1차 근거**다.
>
> **⚠️ 저자에게:** 아래 버전 번호(`2.1.x`)와 환경변수 이름은 모두 **2026-07-26 시점의 `anthropics/claude-code` CHANGELOG 원문**에서 뽑았다. **인용문의 버전은 전부 "해당 문장이 실린 줄 번호 → 직전 `## 버전` 헤더" 매핑으로 기계적으로 검증했다** (추정 아님). 그래도 책에 쓸 때 재확인할 것 — 이 파일이 인쇄될 즈음이면 또 바뀌어 있다. 최신 릴리스는 이 스냅샷 기준 **2.1.220**.

---

## 토픽 4 — 클라이언트 연결 실무

### 4-1. 스코프(local/project/user): 사람들이 실제로 헷갈리는 지점

**핵심 함정: "어제는 됐는데 오늘은 안 보인다."**

`claude mcp add`의 기본 스코프는 `local`이고, **local 스코프는 "그 프로젝트 디렉터리"에 묶인다.** 다른 폴더에서 `claude`를 띄우면 그 서버는 존재하지 않는다. 이게 초심자가 가장 많이 밟는 지뢰다.

> "Local-scoped servers are tied to the project where you added them: the repository root, or the exact directory if you weren't in a git repository."
> — [Claude Code 공식 문서 / MCP quickstart](https://code.claude.com/docs/en/mcp-quickstart), 검색 2026-07-26 기준
> *(주: 스코프 우선순위(local > project > user)는 여러 2차 블로그가 동일하게 서술하나, **본 리서치에서 1차 문서로 직접 확인하지 못했다.** 책에 단정하기 전 공식 문서 재확인 필요. → 「확인하지 못한 것」 섹션 참조)*

**커뮤니티가 스코프에 대해 실제로 올린 요구 (전부 1차 GitHub 이슈, 날짜 확인됨):**

| 이슈 | 날짜 | 요지 |
|---|---|---|
| [#8288](https://github.com/anthropics/claude-code/issues/8288) | **2025-09-28** ⚠️구식 (closed) | `claude mcp list` 출력에 **스코프 정보가 안 나온다** — ↓ 아래 상세 |
| [#68603](https://github.com/anthropics/claude-code/issues/68603) | 2026-06-15 | **부모 디렉터리 스코프**를 달라 (모노레포에서 서브패키지마다 다시 등록해야 하는 고통) |
| [#68605](https://github.com/anthropics/claude-code/issues/68605) | 2026-06-15 | **프로젝트별 MCP 제외** — user 스코프 전역 서버를 특정 프로젝트에서만 끄고 싶다 |
| [#17668](https://github.com/anthropics/claude-code/issues/17668) | 2026-01-12 (댓글 10) | MCP를 **포크된 에이전트/스킬 컨텍스트에 격리 할당**하고 싶다 |
| [#43057](https://github.com/anthropics/claude-code/issues/43057) | 2026-04-03 | 메인 세션 vs 서브에이전트 MCP 분리 |
| [#42916](https://github.com/anthropics/claude-code/issues/42916) | 2026-04-03 | `/mcp` 다이얼로그가 설정된 서버를 **전부 보여주지 않는다** |
| [#48857](https://github.com/anthropics/claude-code/issues/48857) | 2026-04-16 | 스코프 우선순위 문서가 **같은 이름·다른 엔드포인트 서버에 대한 `/doctor` 경고를 설명 안 함** |

**[#8288] 상세 — 스코프 가시성 문제를 가장 잘 증언하는 1차 사례** (2025-09-28 작성, **2025년 9월 시점 기준**, closed):

> "Users cannot determine if an MCP server is configured at local, project, or user scope"
> "**Debugging difficulties**: When MCP tools appear/disappear in `/context`, users cannot understand why"
> "**Token usage confusion**: Context window fluctuations are unexplained without scope visibility"
> "**Team collaboration problems**: No way to distinguish between personal vs. shared (project-scoped) servers"

작성자가 첨부한 **실측 컨텍스트 변동** (토픽 5의 컨텍스트 비용 논의에도 직결되는 1차 수치):
> - "**79k tokens (40%)**: Full MCP toolset loaded (~59.4k MCP tools + project files)"
> - "**36k tokens (18%)**: MCP tools unloaded, project files present"
> - "**20k tokens (10%)**: Minimal context, no MCP tools"
> "Without scope information, it was impossible to un[derstand]..."

→ **이건 커뮤니티가 직접 잰 "MCP 도구 정의가 먹는 컨텍스트" 수치다.** 도구 정의만 **약 59.4k 토큰**. 다만 **2025-09 시점 기준**이며 deferred loading 이전 데이터일 가능성이 높다 → 5-7 신선도 경고와 반드시 함께 제시할 것.
※ 이 이슈도 봇이 중복 후보 3건([#6547](https://github.com/anthropics/claude-code/issues/6547)·[#5963](https://github.com/anthropics/claude-code/issues/5963)·[#1955](https://github.com/anthropics/claude-code/issues/1955))을 붙였다 — **같은 불만이 최소 4번 중복 제기**됐다는 뜻.

> **패턴 (챕터 오프닝 소재):** 스코프 관련 이슈 20건 중 **절반 이상이 "기능 요청"이 아니라 "어디에 뭐가 설정됐는지 모르겠다"는 가시성 문제**다. 사람들은 스코프 개념 자체보다 **"지금 이 서버가 어느 스코프에서 로드됐는지 알 방법이 없다"**에 좌절한다. #8288의 "토큰이 79k에서 20k로 널뛰는데 이유를 알 수 없었다"가 이 고통의 전형이다.

**증상 → 원인 → 해결**

- **증상:** 프로젝트 A에서 잘 되던 MCP 서버가 프로젝트 B에서 `claude mcp list`에 안 보인다.
  **원인:** `--scope` 없이 추가 → 기본값 `local` → 추가한 디렉터리에 묶임.
  **해결:** `--scope user`로 재등록(전역), 또는 팀 공유가 목적이면 `--scope project`(`.mcp.json` 커밋).

- **증상:** `.mcp.json`을 커밋했는데 팀원 환경에서 서버가 `⏸ Pending approval`로 뜬다.
  **원인:** 보안 강화. **v2.1.196**(CHANGELOG): *"Security: `claude mcp list`/`get` no longer spawn `.mcp.json` servers that a repo self-approved via a committed `.claude/settings.json`; untrusted workspaces show `⏸ Pending approval`"*
  **해결:** 신뢰 승인 절차를 팀 온보딩 문서에 명시. 리포지토리가 스스로를 승인하는 경로는 의도적으로 막혔다.
  → **책 소재:** "설정 파일을 커밋한다"는 게 곧 "임의 프로세스 실행을 커밋한다"는 뜻임을 독자가 자각하게 만드는 지점.

- **증상:** 파이프로 넘길 때만 서버가 자동 연결된다.
  **원인/변경:** **v2.1.154**: *"`claude mcp list`/`get` now show unapproved `.mcp.json` servers as `⏸ Pending approval` instead of auto-approving and connecting when output is piped"*

### 4-2. 시크릿·환경변수 주입 — 실제로 터진 사고

**`claude mcp list`가 시크릿을 터미널에 뿌렸다.** CHANGELOG **v2.1.161**:

> "Fixed `claude mcp` list/get/add printing secrets to the terminal: `${VAR}` references are no longer expanded, and credential headers and URL secrets are redacted"
> — [anthropics/claude-code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md), 2026-07-26 확인

즉 **v2.1.161 이전 버전에서는 `claude mcp list` 출력을 그대로 이슈나 슬랙에 붙여넣으면 토큰이 샜다.** 스크린샷 공유 문화를 생각하면 실제 유출이 있었을 가능성이 높다. 책의 보안 섹션에 그대로 쓸 수 있는 사례.

관련 항목들:
- **v2.1.207**: 플러그인 훅/`headersHelper`에서 `${user_config.*}`의 셸 형태 명령 사용이 **셸 인젝션 수정**으로 거부됨 → exec 형태(`args` 배열) 또는 `$CLAUDE_PLUGIN_OPTION_<KEY>` 사용 권장.
- **[#47789](https://github.com/anthropics/claude-code/issues/47789)** (2026-04-14), **[#69083](https://github.com/anthropics/claude-code/issues/69083)** (2026-06-17): `headersHelper`가 `${CLAUDE_PLUGIN_ROOT}`를 확장하지 않거나 `CLAUDE_PLUGIN_ROOT`/`CLAUDE_PLUGIN_DATA` 환경변수를 못 받는다.
- **[#68229](https://github.com/anthropics/claude-code/issues/68229)** (2026-06-13): 플러그인 MCP의 상대경로 `headersHelper`가 **플러그인 루트가 아니라 세션 CWD 기준으로 해석**된다.
- **v2.1.219**: *"a warning for MCP config values with hidden leading or trailing whitespace"* → **설정값 앞뒤 공백**이 실제 장애 원인이었다는 뜻. 복붙 토큰의 고전적 함정.

**증상 → 원인 → 해결**
- **증상:** 토큰이 분명 맞는데 401.
  **원인 후보:** 설정값 앞뒤 보이지 않는 공백(위 v2.1.218 경고가 생긴 이유).
  **해결:** 최신 CLI의 경고 확인, 또는 값 자체를 `| cat -A`류로 검증.

### 4-3. stdio 서버가 "안 붙는" 케이스 카탈로그 (전부 1차 이슈)

이 절이 "왜 내 서버가 안 붙나"에 대한 실제 답변 모음이다.

| 증상 | 이슈 / 출처 | 날짜 | 원인·해결 |
|---|---|---|---|
| **stdout에 로그 한 줄 찍고 연결 끊김** | [dirmacs/daedra#4](https://github.com/dirmacs/daedra/issues/4), [#48866](https://github.com/anthropics/claude-code/issues/48866) | #48866: 2026-04-16 | stdout은 프로토콜 채널. **stderr로 보내라.** ↓ 5-1 상세 |
| **stdio 서버 프로세스가 아예 스폰되지 않음** | [#37952](https://github.com/anthropics/claude-code/issues/37952) | 2026-03-23 | (closed) |
| **RHEL 8 + 네이티브 바이너리에서 stdio 서버 연결 실패** | [#28011](https://github.com/anthropics/claude-code/issues/28011) | 2026-02-23 | 플랫폼 의존 |
| **Windows: VS Code/VSCodium 확장이 stdio 서버 스폰 실패 ("The system cannot find the path specified.") — CLI는 정상** | [#66262](https://github.com/anthropics/claude-code/issues/66262) | 2026-06-08 | **같은 설정, 다른 클라이언트, 다른 결과.** PATH 상속 차이 |
| **Windows 자동 업데이트가 MCP 자식 프로세스를 고아로 만들어 다음 실행 시 npx 기반 서버가 EBUSY** | [#62419](https://github.com/anthropics/claude-code/issues/62419) | 2026-05-26 | 프로세스 정리 실패 |
| **`NO_PROXY`가 MCP 서브프로세스 환경에 주입되지 않음** | [#56664](https://github.com/anthropics/claude-code/issues/56664) | 2026-05-06 | 사내 프록시 환경의 고전 |
| **프록시 환경에서 원격 MCP 연결 실패** | [#38021](https://github.com/anthropics/claude-code/issues/38021) | 2026-03-24 | |
| **HTTP MCP가 project 스코프에선 헬스체크 실패, user 스코프에선 성공 (같은 URL/베어러/헤더)** | [#46510](https://github.com/anthropics/claude-code/issues/46510) | 2026-04-11 | 스코프별 동작 차이 — 재현 어려운 부류 |
| **`url`은 있는데 `type`이 없어 "command: expected string"이라는 엉뚱한 에러** | CHANGELOG **v2.1.202** | | 이제 `"type": "http"`를 제안하는 메시지로 개선됨. **이전 버전 사용자는 이 오해에 걸렸다.** |
| **`✓ Connected`인데 도구가 하나도 없음** | CHANGELOG **v2.1.181** | | *"Fixed `claude mcp get`/`list` showing `✓ Connected` when tools/list fails; they now show `! Connected · tools fetch failed`"* → **"연결됨"이 "동작함"이 아니었다.** |
| **`tools/list`가 페이지네이션되면 1페이지 이후 도구가 조용히 사라짐** | CHANGELOG v2.1.144 | | *"only returning the first page, silently dropping tools"* — 도구 많은 서버 만드는 사람은 반드시 알아야 할 함정 |

> **패턴 (챕터 오프닝 소재):** **"Connected"라는 초록 체크는 거짓말을 한다.** 핸드셰이크 성공 ≠ 도구 사용 가능. 이 카탈로그의 상당수가 "연결은 됐다는데 도구가 없다/안 불린다" 형태다.

### 4-4. Claude Desktop 특유의 함정

- **[#80016](https://github.com/anthropics/claude-code/issues/80016)** (2026-07-22, 댓글 9, **open**): *"Claude Desktop (Windows): Filesystem extension handshake succeeds but tools/call never dispatched — same as closed #22299, reinstall does not fix"* → **핸드셰이크는 되는데 `tools/call`이 아예 디스패치되지 않는다.** 재설치로도 안 고쳐진다는 게 핵심 고통.
- **[#42823](https://github.com/anthropics/claude-code/issues/42823)** (2026-04-02): Claude Desktop이 stdio MCP 도구 호출 시 **무한 정지**.
- **[#80276](https://github.com/anthropics/claude-code/issues/80276)** (2026-07-22): **Claude Desktop이 심링크된 `claude_desktop_config.json`을 저장 시 일반 파일로 갈아치운다** (atomic write가 심링크를 인식 못 함). → dotfiles로 설정을 관리하는 사람이 정확히 당하는 함정.
- **[#56263](https://github.com/anthropics/claude-code/issues/56263)** (2026-05-05, **open**): **`inputSchema`의 property-level `anyOf [X, null]` (즉 Python의 `Optional[X]`)이 모델에 도달하기 전 조용히 제거된다.** → Python으로 서버 짜는 사람이 `Optional[str]` 파라미터를 쓰면 스키마가 뭉개진다. **책에 반드시 넣을 실무 함정.**
- **[#77296](https://github.com/anthropics/claude-code/issues/77296)** (2026-07-13): claude.ai 커넥터 인제스천이 **`inputSchema` 16,384바이트 초과 도구를 조용히 드롭**한다.
- **[#77388](https://github.com/anthropics/claude-code/issues/77388)** (2026-07-14): `.mcpb` Desktop Extension의 MCP 도구가 Chat에는 노출되지 않고 Cowork에서는 된다 — **양쪽 다 "연결됨"으로 표시**.
- **[#74768](https://github.com/anthropics/claude-code/issues/74768)** (2026-07-06): Desktop의 DCR이 `client_name`을 `"Claude Desktop (…)"`로 보내 **Figma MCP 등록 엔드포인트가 403 거부** — CLI는 `"Claude Code"`를 보내서 성공. **같은 서버, 다른 클라이언트, 다른 결과의 극단적 예.**
- **한국 사례:** velog 글들이 공통적으로 "설정 파일은 단순하게 유지하고 `claude_desktop_config.json`의 **오타**에 주의"를 반복 조언 — [velog @takuya, "Claude Code와 MCP 서버로 구현하는 차세대 개발 환경"](https://velog.io/@takuya/claude-code-mcp-servers-guide-2025) 등. (2025 작성 추정, **2025년 시점 기준** — 검색 2026-07-26)

### 4-5. Claude Agent SDK — in-process(SDK 내장) MCP 서버

- **API:** TS `createSdkMcpServer(...)` + `tool(...)`, Python `create_sdk_mcp_server(...)` + `@tool` 데코레이터. **별도 프로세스 없이 애플리케이션 내부에서 실행**되므로 서브프로세스 오버헤드가 없다. — [Claude API Docs / Give Claude custom tools](https://platform.claude.com/docs/en/agent-sdk/custom-tools), 검색 2026-07-26 기준. Go·Rust·Elixir·Perl 서드파티 포팅도 존재.
- **실무 함정 (1차 이슈):** [**#7279**](https://github.com/anthropics/claude-code/issues/7279) (2025-09-07, **2025년 9월 시점 기준**, closed) — *"When I try to run the example in-process MCP server from the Claude Code TypeScript SDK documentation, the `query` silently fails and doesn't yield."* **공식 문서 예제를 그대로 복붙했는데 조용히 실패**했다는 보고. 에러 로그도 없음.
  → **책 소재:** in-process MCP는 프로세스 경계가 없어 편하지만, **경계가 없다는 건 실패도 조용하다는 뜻**이다.
- **SDK MCP 서버 관련 CHANGELOG 항목:**
  - **v2.1.210**: *"Fixed SDK MCP servers registered via an `initialize` control request waiting until the next turn to start connecting"*
  - **v2.1.153**: *"`--strict-mcp-config` no longer strips inline `mcpServers` from explicitly-passed agent definitions (`--agents` / SDK `agents`), and blocked subagent MCP servers now surface a visible warning"*
  - **v2.1.153**: *"Fixed subagent (Agent tool) frontmatter MCP servers ignoring `--strict-mcp-config`, `--bare`, remote mode, enterprise managed MCP config, and managed-settings MCP server allow/deny policies"*

### 4-6. 기타 클라이언트 — 설정 파일 파편화

- **파편화 자체가 커뮤니티의 고통:** GitHub 전역 검색에서 서드파티 MCP 서버 리포지토리들이 **"Claude Desktop 설정 자동 작성" 기능을 별도 이슈로 관리**하는 패턴이 반복 관측됨 — 예: [`Filmroom#40`](https://github.com/nethum529/Filmroom/issues/40) "auto-write config.json and add install guide" (2026-06-27), [`apple-mail-fast-mcp#399`](https://github.com/s-morgan-jeffries/apple-mail-fast-mcp/issues/399) "Guided config subcommand" (2026-07-02), [`mcp-studio#4`](https://github.com/K-Khushal/mcp-studio/issues/4) "Implement import from claude_desktop_config.json" (2026-04-25), [`mcp-manager#10`](https://github.com/Rocho-EL-Locho/mcp-manager/issues/10) (2026-07-02).
  → **패턴:** **"내 서버를 어떻게 설치시키지"가 서버 개발자의 실제 업무가 됐다.** 설정 파일이 클라이언트마다 다르니 서버 저자가 클라이언트별 설치 가이드/자동 설정 기능을 짜고 있다. 이게 파편화의 진짜 비용.
- **크로스 플랫폼 경로 고통:** [`bastra-recall#83`](https://github.com/n0mad-ai/bastra-recall/issues/83) (2026-06-07) — *"Windows: cross-platform paths — %APPDATA% instead of ~/Library/Application Support"*. [`m4#51`](https://github.com/hannesill/m4/issues/51) (2026-07-24) — Windows **MSIX** 설치본의 Claude Desktop 설정 경로를 아무도 모름(질문 형태).
- **[`zotero-mcp#392`](https://github.com/54yyyu/zotero-mcp/issues/392)** (2026-07-19): "Wrong path recognition for `claude_desktop_config.json`".
- **한국 사례:** [gpters, "MCP 서버 활용법: Claude Code와 OpenCode 동시 지원하기"](https://www.gpters.org/nocode/post/how-use-mcp-server-q3MjQBeUFgeOTmf) — 클라이언트 두 개를 동시에 지원하려는 시도 자체가 글의 주제. 검색 2026-07-26.

---

## 토픽 5 — 디버깅·모니터링

### 5-1. stdout 함정 — "한 번은 다 당하는" 실수 1위

**가장 잘 문서화된 커뮤니티 고통.** 그리고 결정적으로, **공식 문서가 이걸 설명하지 않는다는 이슈가 따로 있다.**

[**anthropics/claude-code #48866**](https://github.com/anthropics/claude-code/issues/48866) — `[DOCS] MCP stdio server docs missing stdout/stderr protocol guidance`, **coygeek**, **2026-04-16** 작성 (closed as not planned):

> "for stdio MCP servers, stdout is the protocol channel. If a custom server, wrapper script, shell startup, or dependency prints banners/logging/non-JSON text to stdout, the connection can fail or behave unpredictably."

이 이슈가 인용한 **실제 체인지로그 항목**:

> "Fixed stdio MCP servers that print stray non-JSON lines to stdout being disconnected on the first stray line (**regression in 2.1.105**)"

→ **즉 한때는 stdout에 이물질 한 줄만 나와도 즉시 연결이 끊겼다.** (2.1.105 리그레션, 이후 수정)

이슈가 제안한 문서 문구(그대로 책에 인용 가능):
> "**Important:** For stdio MCP servers, stdout is reserved for MCP protocol messages. Do not print banners, logs, or other non-JSON text to stdout. Send diagnostics to stderr instead."

**독립 확인 (다른 리포지토리에서 같은 함정):** [`dirmacs/daedra` Issue #4](https://github.com/dirmacs/daedra/issues/4) — *"stdio transport: log output on stdout breaks MCP JSON-RPC; use stderr for logging"*. 검색 2026-07-26.

**증상 → 원인 → 해결 (책에 바로 쓸 형태)**

- **증상:** `Parse error: Unexpected token ... '[2m2026-0' ... is not valid JSON` / `Protocol error: Method not found: notifications/initialized` / 시작하자마자 `Connection closed`
- **원인:** stdout이 프로토콜 채널인데 여기에 배너·타임스탬프·**ANSI 컬러 코드**·`print()`·의존 라이브러리의 로그가 섞였다. **래퍼 셸 스크립트나 셸 시작 파일(`.zshrc` 등)의 출력도 포함**된다 — 이게 특히 안 보이는 원인.
- **해결:** stdout엔 JSON-RPC만. 로깅은 전부 stderr. Python `logging`의 기본 핸들러, Node의 `console.log`가 어디로 가는지 반드시 확인. 래퍼 스크립트의 `echo`도 제거.
- **부가 주의:** stderr도 공짜가 아니다 — v2.1.208 CHANGELOG: *"MCP stdio server stderr accumulating up to **64 MB per server**"* 메모리 누수가 수정됐다. **stderr에 무한정 쏟아부으면 클라이언트 메모리를 먹는다.**

### 5-2. MCP Inspector — 유용한 점과 한계

`npx @modelcontextprotocol/inspector`.

**한계 (커뮤니티 관측, 2차 소스 — 확인 필요 표시):**
- "MCP Inspector shows **protocol frames, not your app logs**" / "Inspector acts as a **client, not a proxy**" — [digitalapplied.com, "Anthropic MCP Inspector Deep Dive: Developer Workflow 2026"](https://www.digitalapplied.com/blog/anthropic-mcp-inspector-deep-dive-developer-workflow-2026) 및 [apigene.ai](https://apigene.ai/blog/mcp-inspector), 검색 2026-07-26. **⚠️ 2차 요약 블로그. 원 출처 미확인 (확인 필요).**
- **핵심 시사점(이건 구조상 참):** Inspector는 **당신의 서버와 직접** 말한다. 그래서 "Inspector에선 되는데 Claude Code에선 안 된다"가 발생한다 — 스코프·환경변수·PATH·승인 상태는 Inspector가 재현하지 않는 층이기 때문. 위 4-3의 [#66262](https://github.com/anthropics/claude-code/issues/66262)(CLI는 되는데 VS Code 확장은 실패)가 같은 층위의 증거다.
- **실제 사용 로그 사례:** [`github/gh-aw` Discussion #34749](https://github.com/github/gh-aw/discussions/34749) — "[mcp-inspector] MCP Inspector Report - 2026-05-25". Inspector를 CI에 물려 리포트를 남기는 실무 패턴.

**🔴 Inspector 보안 사고 — 책에 반드시 넣을 사례:**

**CVE-2025-49596** (CVSS **9.4**): MCP Inspector **0.14.1 미만**에서 Inspector 클라이언트와 프록시 사이에 **인증이 없어**, 인증되지 않은 요청이 stdio로 MCP 명령을 실행시킬 수 있었다. 브라우저의 **"0.0.0.0 Day"** 결함 + CSRF를 체이닝하면 **악성 웹사이트를 방문하는 것만으로 개발자 워크스테이션에서 임의 코드 실행**이 가능했다.
— [GitHub Advisory GHSA-7f8r-222p-6f5g](https://github.com/advisories/GHSA-7f8r-222p-6f5g), [Oligo Security 상세 분석](https://www.oligo.security/blog/critical-rce-vulnerability-in-anthropic-mcp-inspector-cve-2025-49596), [Tenable Research](https://www.tenable.com/blog/how-tenable-research-discovered-a-critical-remote-code-execution-vulnerability-on-anthropic). 공개 **2025년 7월** (Qualys ThreatPROTECT 게시 2025-07-03) — **2025년 7월 시점 기준**, 검색 2026-07-26.
→ **교훈:** "로컬 개발 도구니까 안전하다"는 가정이 깨진 사례. 로컬호스트에 뜬 디버깅 프록시는 브라우저에서 도달 가능하다.

### 5-3. 로그 위치와 디버그 플래그

- **MCP 로그 실제 경로 (1차 확인):** [#81268](https://github.com/anthropics/claude-code/issues/81268) 본문이 실제 경로를 명시 — `~/Library/Caches/claude-cli-nodejs/*/mcp-logs-*/*.jsonl` (macOS, **2.1.220** 기준, 2026-07-26 작성). **JSONL 형식**이라 `jq`로 바로 분석 가능하다는 점이 실무적으로 중요.
- **`--debug` 출력 실제 형태 (1차 인용, [#68375](https://github.com/anthropics/claude-code/issues/68375), 2026-06-14):**
  ```
  [DEBUG] MCP server "X": Successfully connected (transport: stdio) in 3727ms
  [DEBUG] MCP server "X": Calling MCP tool: my_tool
  [DEBUG] MCP server "X": Tool 'my_tool' still running (30s elapsed)
  [DEBUG] MCP server "X": Tool 'my_tool' failed after 68s: MCP error -32000: Connection closed
  ```
  → **`MCP error -32000: Connection closed`가 실무에서 가장 자주 보게 될 에러 문자열**이다. 책에 그대로 실을 것.
- **에러 메시지 개선 이력 (CHANGELOG):** **v2.1.219** *"Added HTTP status and error text to `claude mcp list` and `/mcp` when a server fails to connect"* / **v2.1.191** *"HTTP 404 errors now show the URL and point to your MCP config"* / [#70706](https://github.com/anthropics/claude-code/issues/70706) (2026-06-25)는 이 개선(**v2.1.191**)이 문서에 반영 안 됐다는 DOCS 이슈.
- **헤드리스 진단 (토픽 6과 직결):** v2.1.219 *"Added `mcp_server_errors` to the headless stream-json init event, listing `--mcp-config` entries skipped by config validation; terminal runs print a startup warning"* → **오케스트레이터가 MCP 실패를 기계적으로 감지할 경로가 최근에야 생겼다.**
- **`--safe-mode`:** **v2.1.169** *"Added `--safe-mode` flag (and `CLAUDE_CODE_SAFE_MODE`) to start Claude Code with all customizations (CLAUDE.md, plugins, skills, hooks, MCP servers) disabled for troubleshooting"* → **이분 탐색 디버깅의 출발점.**
- **`--strict-mcp-config`:** 특정 서버만 로드해 문제를 격리하는 실전 기법. [#68375](https://github.com/anthropics/claude-code/issues/68375)에서 실제로 이 플래그가 **진단 도구로 사용**됐다(전체 함대에선 행, 단일 서버로 제한하면 5초).

### 5-4. 조용한 손실 — 로그에 안 남는 것들

이 절이 토픽 5에서 가장 책에 쓸 만한 발견이다.

[**#81268**](https://github.com/anthropics/claude-code/issues/81268) — *"MCP truncation at 2048 chars is invisible"*, **2026-07-26 작성 (본 리서치 당일!)**, 버전 **2.1.220**:

> "Claude Code truncates two MCP server-provided strings at 2048 characters before they reach the model: 1. `InitializeResult.instructions` 2. every tool's `description`"
> "Neither limit is part of the MCP specification — the spec types `instructions` as an unbounded optional string, and reference SDKs impose no length cap. The truncation is a client-side decision, and **the server is never told it happened**: no error, no field in the response, no warning."
> 실측: "**502 truncation events** across all MCP logs" / 최악 사례 "**10780 → 2048 chars, an 81% loss**" / 영향받은 서버 상위에 **Anthropic 자체 커넥터**(claude-ai-Figma 87건, pencil 57건) 포함.

→ **책 소재로 최고:** "도구 설명을 길고 자세히 쓰면 모델이 잘 쓰겠지"라는 직관이 **2048자에서 잘린다.** 그것도 **말없이**. 그리고 `/mcp`는 안 잘린 원문을 보여주니 **개발자는 잘린 걸 눈으로 확인할 수조차 없다.**

같은 계열의 "조용한 손실":
- **v2.1.144:** `tools/list` 페이지네이션 2페이지 이후 도구 조용히 드롭.
- **[#56263](https://github.com/anthropics/claude-code/issues/56263)** (2026-05-05): `Optional[X]` 스키마가 모델 도달 전 조용히 제거.
- **[#77296](https://github.com/anthropics/claude-code/issues/77296)** (2026-07-13): 16KB 초과 `inputSchema` 도구 조용히 드롭.
- **[#43968](https://github.com/anthropics/claude-code/issues/43968)** (2026-04-05): 헤드리스에서 MCP 연결 실패가 **"zero signal in stderr or the stream-json output"**.

> **패턴 (챕터 오프닝 소재 · 강력):** **MCP 실무 고통의 큰 갈래는 "에러"가 아니라 "침묵"이다.** 잘리고, 드롭되고, 제거되고, 신호가 없다. 초보자는 에러를 고치는 법을 배우지만, MCP 서버 개발자는 **아무 일도 안 일어난 것처럼 보이는 상황을 의심하는 법**을 배워야 한다.

### 5-5. 타임아웃 — 구체적 숫자와 노브 (전부 CHANGELOG 1차)

| 항목 | 버전 | 내용 |
|---|---|---|
| 기본 60초 타임아웃 & `request_timeout_ms` 무시 버그 | **v2.1.206** | *"Fixed MCP servers configured via `--mcp-config` or `.mcp.json` ignoring a per-server `request_timeout_ms`, which caused long-running MCP tool calls to **time out at the 60s default** in fresh sessions"* |
| 2분 초과 시 자동 백그라운드 | **v2.1.212** | *"MCP tool calls running longer than 2 minutes now move to the background automatically so the session stays usable; configure the threshold or disable with **`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`**"* |
| 원격 MCP 5분 무응답 행 | **v2.1.187** | *"Fixed remote MCP tool calls that hang with no response for 5 minutes — they now abort with an error instead of blocking indefinitely (override with **`CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`**)"* |
| 1000ms 미만 timeout이 모든 호출을 죽인 버그 | **v2.1.162** | *"Fixed MCP per-server `timeout` config values below 1000 ms being floored to a 1-second watchdog that **aborted every tool call**; sub-1000 ms values are now ignored (falling back to `MCP_TOOL_TIMEOUT` or default)"* |
| 연결 배치 크기 노브 | 2.1.177 당시 확인 | **`MCP_SERVER_CONNECTION_BATCH_SIZE`** — [#68375](https://github.com/anthropics/claude-code/issues/68375) 댓글(HundeSohnJr, 2026-06-14)에서 **바이너리 grep으로 실존 확인**. 같은 댓글이 *"`MCP_MAX_CONCURRENT_INIT` does **not** exist in 2.1.177"*라고 **틀린 환경변수 이름을 명시적으로 반증**함 → 커뮤니티에 잘못된 노브 이름이 돌아다녔다는 증거. **책에 쓸 땐 반드시 현재 버전에서 재검증할 것.** |
| `/mcp reconnect`가 공유 배치 데드라인으로 멀쩡한 서버를 죽임 | [#78726](https://github.com/anthropics/claude-code/issues/78726) (2026-07-18, open) | *"kills already-connected stdio servers via shared batch deadline (-32000)"* |

### 5-6. 도구 개수·컨텍스트 비용 — 실측 숫자

**커뮤니티가 실제로 인용한 숫자 (HN 1차 댓글, 출처·작성자·날짜 확인):**
- **0xbadcafebee** (HN 48330436, 2026-05-29): 도구 50개짜리 큰 MCP = *"150 * 50, or **7500 tokens**, dumped into the beginning of every session"*
- **익명 댓글** (HN 47208398 스레드, 2026-03-01): *"Reading on GH issue with MCP burns **54k tokens** just to load the spec"* — **⚠️ 단일 익명 주장, 미검증 (확인 필요)**
- **SOLAR_FIELDS** (HN 47208398, 2026-03-01T18:06:59Z): *"Tools themselves take up a ton of token context"* — 여러 MCP를 붙이면 *"upper bound"*에 금방 닿는다
- **JoshGlazebrook** (HN 48330436, 2026-05-29): *"Tool Search with Deferred Loading ... reduces context usage by **85%+**. The context bloat ... is largely addressed"* — **⚠️ 커뮤니티 주장. Anthropic 공식 수치인지 원 출처 미확인 (확인 필요).** 단, `total_deferred_tools` 필드가 [#43968](https://github.com/anthropics/claude-code/issues/43968) 로그에 실제로 등장하므로 **deferred loading 기능 자체의 존재는 1차 확인됨**.
- **red_hare** (HN 48330436, 2026-05-29): *"**Deferred tool loading was added in Nov 2025** ... so these numbers are at least 7 months out of date. Why is this being posted now?"* — **⚠️ 단일 주장, 날짜 미검증 (확인 필요).** 하지만 논지 자체는 이 책에 결정적이다 → 5-7 참조.
- **성능 측면 (CHANGELOG **v2.1.208**, 1차):** *"Reduced per-tool-call CPU overhead in print/SDK sessions with many MCP tools by caching tool-pool assembly (**up to 7x faster** tool rounds at high tool counts)"* → **도구가 많으면 CPU 비용도 든다**는 걸 Anthropic이 최적화로 인정한 셈.
- **`/usage` 기능 (CHANGELOG **v2.1.149**):** *"`/usage` now shows a per-category breakdown of what's driving your limits usage — skills, subagents, plugins, and **per-MCP-server cost**"* → **MCP 서버별 비용을 볼 도구가 이제 존재한다.** 실무 모니터링 절에 필수.
- **v2.1.174 [VSCode]:** `/usage` 다이얼로그에 *"cache misses, long context, subagents, and per-skill/agent/plugin/MCP breakdowns over the last 24h or 7d"*

### 5-7. ⏱️ 신선도 경고 — 이 책이 반드시 다뤄야 할 메타 이슈

**"MCP는 컨텍스트를 낭비한다"는 비판의 상당수가 deferred tool loading 이전 데이터에 기반한다.**

HN "MCP is dead?" 스레드(2026-05-29)에서 **red_hare**가 정확히 이 지적을 했고, **JoshGlazebrook**가 deferred loading으로 대부분 해소됐다고 반박했다. 한국 GeekNews에서도 **newdps**가 같은 말을 했다: *"claude 같은 경우 deferred tool로 분류해서 이름만 넣도록 최적화하긴 합니다"* ([GeekNews "MCP는 죽었나?"](https://news.hada.io/topic?id=30028), 게시 ~2026-05).

→ **책의 태도:** 컨텍스트 비용 비판을 소개하되, **"어느 시점의, 어느 클라이언트 동작을 전제한 비판인가"를 반드시 함께 표시**해야 한다. 이게 이 책이 다른 MCP 글과 차별화될 지점이다.
→ **⚠️ 단, deferred loading의 도입 시점(2025-11?)과 85% 수치는 본 리서치에서 1차 검증하지 못했다.** 저술 전 Anthropic 공식 릴리스 노트로 반드시 확인할 것.

### 5-8. 프로덕션 관찰성 (OpenTelemetry)

- **MCP 스펙 차원의 OTel 논의:** [modelcontextprotocol/modelcontextprotocol Discussion #269](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/269) — "[Proposal] Adding OpenTelemetry Trace Support to MCP". **스펙 레벨에서 아직 논의 중**이라는 것 자체가 중요한 사실(= 표준 관찰성 계층이 없다).
- **핵심 기술 제약 (여러 벤더 가이드가 일치):** HTTP 계열 전송(SSE, Streamable HTTP)은 **HTTP 헤더로 trace context 전파가 자연스럽지만, stdio는 헤더가 없어** 도구 호출 파라미터나 환경변수로 **명시적으로 실어 날라야 한다**. — [Elastic Observability Labs](https://www.elastic.co/observability-labs/blog/mcp-tracing-opentelemetry-elastic-apm), [SigNoz](https://signoz.io/blog/mcp-observability-with-otel/), [OneUptime (2026-03-26)](https://oneuptime.com/blog/post/2026-03-26-how-to-instrument-mcp-servers-with-opentelemetry/view). 검색 2026-07-26.
  → **이건 stdio vs HTTP 선택의 실무적 귀결**이다. 논쟁점 섹션과 연결하면 좋다.
- **권장 span 계층:** `session → task → turn → tool.call`.
- **Claude Code 측 텔레메트리 (1차, CHANGELOG **v2.1.157**):** *"`tool_decision` telemetry events now include `tool_parameters` (bash commands, MCP/skill names) when **`OTEL_LOG_TOOL_DETAILS=1`**"* → **클라이언트 쪽에서 MCP 도구 결정을 OTel로 뽑을 수 있는 실제 환경변수.**

---

## 토픽 6 — MCP 서버가 역으로 코딩 에이전트를 호출하는 패턴

> **정직한 전제: 이 토픽은 소스가 얇다.** 체계적 검색을 여러 각도로 돌렸으나(아래 「부정적 발견」 참조), **블로그·포럼의 실무 회고는 거의 없고 대부분 리포지토리 README와 이슈 트래커에만 존재한다.** 아래는 발견한 것 전부다.

### 6-0. 먼저 구분할 것 — 두 패턴은 다르다

책에서 반드시 분리해야 할 개념:

- **패턴 A — 에이전트를 MCP 서버로 *노출*:** Claude Code 자체를 MCP 서버로 띄워 다른 도구가 쓰게 함.
- **패턴 B — MCP 서버가 에이전트를 *호출*(오케스트레이션):** 서버 코드 안에서 `claude -p` / `codex exec` 등을 스폰해 결과를 도구 응답으로 반환. **본 토픽의 주제.**

혼동이 실제로 커뮤니티에 존재한다 (아래 리포지토리들이 두 성격을 섞어 설명함).

### 6-1. 발견한 실제 구현체 (`gh repo view`로 메타데이터 1차 확인, 2026-07-26)

| 리포 | ⭐ | 생성 | 마지막 푸시 | 상태 | 성격 |
|---|---|---|---|---|---|
| [**steipete/claude-code-mcp**](https://github.com/steipete/claude-code-mcp) | **1,313** | 2025-05-13 | 2026-05-15 | **🔴 아카이브됨** | *"Claude Code as one-shot MCP server to have an agent in your agent."* |
| [**grahama1970/claude-code-mcp-enhanced**](https://github.com/grahama1970/claude-code-mcp-enhanced) | 125 | 2025-05-15 | **2025-05-20 (14개월 방치)** | 사실상 미유지 | 오케스트레이션·"boomerang pattern" |
| [**SinanTufekci/agent-intern**](https://github.com/SinanTufekci/agent-intern) (구 `Claude-Code-Antigravity-CLI-MCP-Server`) | 16 | 2026-05-22 | **2026-07-24 (활발)** | ✅ 활발 | MCP 서버가 **Antigravity·Codex·Copilot·Cursor 4개 CLI를 서브에이전트로 구동** |

> **🚨 가장 중요한 신선도 신호:** 이 패턴의 **대표 리포지토리(1,313⭐)가 아카이브됐고**, 2위(125⭐)는 **14개월 방치**다. 반면 활발한 것은 16⭐짜리 신생 프로젝트다.
> → **책의 태도:** 이 패턴을 "떠오르는 베스트 프랙티스"로 소개하면 안 된다. **"실험적이고, 대표 구현이 유지보수를 멈춘 영역"**으로 정직하게 프레이밍해야 한다. 이건 부정적 발견이지만 **독자에게 가장 값진 정보**다.

### 6-2. `steipete/claude-code-mcp` — 저자가 직접 쓴 동기와 경고 (README 1차 인용)

**동기:** *"Cursor sometimes struggles with complex, multi-step edits or operations."* + 비용 절감(*"save costs with offloading tasks to cheaper models"*).

**저자가 명시한 경고:**
- *"This wrapper is **not an OS-level sandbox**; for a hard file-system boundary, run the MCP server or Claude CLI inside your own container, VM, or platform sandbox."*
- *"[the wrapper] cannot approve prompts that belong to a parent MCP client, bypass macOS privacy prompts, or make another Claude Code session inherit its settings."* → **중첩 에이전트의 권한 경계가 상속되지 않는다**는 핵심 함정.
- 사전 조건: *"must first run the Claude CLI manually once with the `--dangerously-skip-permissions` flag, login and accept the terms."* → **패턴 진입 자체가 권한 우회 플래그를 요구**한다.
- 타임아웃 노브: **`CLAUDE_CLI_TIMEOUT_SECONDS`**, 기본 **3600초(1시간)**. → 일반 MCP 도구 타임아웃(60초~5분, 5-5 참조)과 **두 자릿수 배 차이**. 이 패턴의 시간 스케일이 근본적으로 다르다는 증거.
- README에 *"Agents in Agents"* 밈이 실려 있고 *"Multiple commands can be queued instead of direct execution"*로 중첩 워크플로를 명시 지원.

### 6-3. `SinanTufekci/agent-intern` — 이 패턴의 함정이 가장 잘 문서화된 사례

README(2026-07-24 푸시)에서 뽑은 **실무 함정**:

**(a) 헤드리스 CLI의 stdout 신뢰성 문제 — 토픽 5의 stdout 함정과 정확히 대칭:**
> Antigravity의 *"headless print mode (`agy -p`) historically had a **stdout bug**: it wrote the answer to the *controlling terminal* instead of its stdout, so anything capturing stdout got nothing (and, under a TUI, agy's text leaked into the host's prompt). **agy 1.0.15 fixed this on Windows**"*

→ 그래서 브리지는 **stdout을 우선 읽고, 비어 있으면 에이전트 자신의 트랜스크립트 파일을 긁는 폴백**을 쓴다:
`~/.gemini/antigravity-cli/brain/<conv-id>/.system_generated/logs/transcript.jsonl`
→ **책 소재 최상:** "MCP 서버가 에이전트를 호출한다"는 건 **에이전트의 출력 규약에 인질로 잡힌다**는 뜻이다. 각 CLI가 답을 돌려주는 방식이 제각각이다:

| CLI | 답을 읽는 방법 (README 1차) |
|---|---|
| `agy -p` (Antigravity) | agy 1.0.15+(Windows)는 stdout; 아니면 `transcript.jsonl` **스크래핑** |
| `codex exec` (OpenAI) | `-o/--output-last-message` 로 **파일에 씀** (스크래핑 불필요) |
| `copilot -p` (GitHub) | stdout (`-s` silent 모드) |
| `cursor-agent -p` (Cursor) | stdout (`--output-format text`) |

**(b) 샌드박스 — 이 패턴 최대의 위험 (README의 `[!WARNING]` 블록 그대로):**
> "**This runs unsandboxed code with your privileges.** `agy -p` auto-executes its tools (read/write files, run shell commands, reach the network) with **no usable approval gate** — its `--sandbox` blocks only *shell commands*, leaving file writes and network egress wide open."
> "`codex exec` also runs autonomously, but its `sandbox` flag (default `read-only`) **is** a real, enforced boundary."
> "in all four cases the `workspace` argument is a *starting context*, **not a security boundary**."
> "Only use these with **trusted prompts on trusted content**; for real isolation, run the bridge inside a container or VM."

→ **책의 보안 섹션 핵심 문장:** MCP 도구 하나를 노출하는 순간, 그 뒤에 **승인 게이트 없는 자율 에이전트**가 있을 수 있다. 그리고 **호출한 쪽(Claude Code)의 권한 시스템은 그 안까지 미치지 않는다.**

**(c) 상태 경합:** 스웜(병렬 실행) 시 agy는 *"Runs with an isolated `HOME` to avoid state races"*. → **중첩 에이전트를 병렬로 돌리면 홈 디렉터리 상태가 충돌한다.** 나머지 셋은 one-shot이라 격리 불필요.

**(d) 동기 = 비용 차익거래:** *"💸 Cheap delegation | Burn Antigravity / Codex quota on grunt work instead of Claude tokens."* → 이 패턴의 현실적 동기가 "구독 쿼터 차익거래"라는 걸 저자가 명시. **비용 폭발의 반대 방향 동기.**

### 6-4. 이 패턴이 실제로 깨지는 지점 (Claude Code 이슈 1차 — 오케스트레이터 관점)

토픽 6의 함정을 **가장 잘 증언하는 건 리포지토리가 아니라 오케스트레이션을 실제로 운영하는 사람들의 이슈**다.

**① 헤드리스에서 MCP 실패가 무신호 — [#43968](https://github.com/anthropics/claude-code/issues/43968), 2026-04-05, Claude Code 2.1.92:**
> "When an MCP server fails to connect during a `-p` (headless) session, Claude Code silently proceeds without those tools. There is **zero signal** in stderr or the `stream-json` output. ... Orchestrators have no way to detect the failure except by counting tools and comparing against an expected baseline."
> "We've observed this multiple times in a **production orchestration system**."

실제 로그 대비(그대로 인용 가능):
```
1차 요청:  system/init → tools: 70 (22 built-in + 48 MCP), mcp_servers: [{"name":"...","status":"connected"}]
--resume:  system/init → tools: 22 (built-in only, 0 MCP), mcp_servers: []
```
→ 모델은 이전 히스토리에서 도구를 봤는데 ToolSearch는 빈 결과, 직접 호출은 "No such tool available". **사용자에겐 아무 설명 없는 고장.**
※ 이 이슈는 봇에 의해 [#36833](https://github.com/anthropics/claude-code/issues/36833) 중복으로 **자동 종료**됐다.
※ **후속:** v2.1.219의 `mcp_server_errors`(5-3 참조)가 이 계열 문제에 대한 부분적 답이다.

**② 헤드리스 무인 세션의 복구 경로 부재 — [#80996](https://github.com/anthropics/claude-code/issues/80996), 2026-07-24 (open, 2일 전!):**
> "our agents' **only inbound-message path is an MCP server**, so a session that resumes with the MCP down is **functionally deaf while looking alive from the outside**."
> 요구사항: (1) 수렴하는 재연결, (2) *"a CLI flag or slash-command-equivalent that a supervisor (or the model itself via a Bash tool) can invoke to force MCP reconnect — today `/mcp` is **interactive-only**"*, (3) 기계 판독 가능한 실패 신호.
> 현재 우회책: *"we ship every agent a standing rule: on wake with MCP tools unavailable, retry briefly, then disarm its liveness monitor and end the turn, so an external watchdog restarts the whole session (**~15 min penalty per event**)"*

→ **책 소재:** 무인 오케스트레이션의 진짜 비용은 "실패"가 아니라 **"살아 있는 척하는 실패"**. 그리고 회복 수단이 대화형 UI에만 있으면 자동화는 불가능하다.

**③ 함대 규모가 커지면 헤드리스 도구 호출이 행 — [#68375](https://github.com/anthropics/claude-code/issues/68375), 2026-06-14 (open), 2.1.177 리그레션:**
> "a single call to a local stdio MCP tool **hangs indefinitely** under `claude -p` when several MCP servers are configured"
> 격리 결과: 전체 함대(~11개 서버) → 행(>68초, kill). `--strict-mcp-config`로 1개만 → **~5초** ✅. 독립 JSON-RPC 클라이언트로 직접 → ~6초 (서버는 건강).
> "A nightly headless job ... ran fine through 2026-06-12; the first run after the 2.1.177 auto-update (2026-06-13) hung."

→ **자동 업데이트 + 헤드리스 배치 = 어느 날 아침 갑자기 멈춘다.** 오케스트레이션 운영의 현실적 교훈.

**④ 프로세스 누수 — [#74329](https://github.com/anthropics/claude-code/issues/74329), 2026-07-05 (open), 2.1.201:**
> stdio 서버가 세션 중 종료되면 lazy 재스폰이 **1회는 성공**하지만 그 뒤 도구가 부당하게 등록 해제되고, *"Each occurrence also **leaks the respawned server process**, which stays running, reparented to init."*
> 문서와 모순: *"This also contradicts the docs, which say stdio servers are never reconnected automatically"* ([code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp) 인용)
> 댓글 **fxspeiser** (2026-07-20): *"over one long session we accumulated **5 concurrent duplicate process trees** ... none torn down by `/mcp reconnect` attempts or multiple full app restarts."* 우회책으로 **서버 진입점에 pidfile 단일 인스턴스 가드**를 직접 넣었다.
> 댓글 **jph00** (2026-07-05): 봇의 중복 판정에 *"None of those are dupes."*

→ **책 소재:** 장수 세션에서 서버 프로세스는 샌다. **서버 저자가 클라이언트의 버그를 방어하는 코드(pidfile 가드)를 자기 서버에 넣는다** — 이게 현재 MCP 생태계의 성숙도를 보여주는 장면.

### 6-5. 코드 검색으로 확인한 실존 패턴 (얕은 신호)

GitHub 코드 검색(`"claude -p"` + `"McpServer"`)에서 나온 리포지토리들 — **대부분 문서·SDK 노트이고 프로덕션 구현은 소수.** 추가 조사 대상 후보:
[`nayagamez/claude-cli-mcp`](https://github.com/nayagamez/claude-cli-mcp) (`src/index.ts`), [`bakabaka91/claude-baton`](https://github.com/bakabaka91/claude-baton) (`src/cli.ts`), [`rblank9/cross-claude-mcp`](https://github.com/rblank9/cross-claude-mcp) (`docs/channels.md`), [`nyldn/claude-octopus`](https://github.com/nyldn/claude-octopus), [`ZachHandley/ZMCPTools`](https://github.com/ZachHandley/ZMCPTools). **⚠️ 메타데이터·스타 수·유지 상태 미확인 (확인 필요).**

관련 생태계 인덱스: [`bradAGI/awesome-cli-coding-agents`](https://github.com/bradAGI/awesome-cli-coding-agents) — *"terminal-native AI coding agents and the harnesses that orchestrate them"*. 열거용 리드로 유용.

---

## 논쟁점

> 책의 "논쟁점" 섹션 재료. **관점 A / 관점 B 병기**, 모든 인용에 스레드·작성자·날짜 명시.

### 논쟁 1 — MCP가 필요한가, CLI면 충분한가 (가장 큰 논쟁)

**논쟁의 규모 (HN Algolia API 1차 메타데이터, 2026-07-26 확인):**

| 스레드 | 점수 | 댓글 | 날짜 |
|---|---|---|---|
| ["I still prefer MCP over skills"](https://news.ycombinator.com/item?id=47712718) (david.coffee) | **460** | **375** | 2026-04-10 |
| ["When does MCP make sense vs CLI?"](https://news.ycombinator.com/item?id=47208398) (원제: "MCP is dead, long live the CLI", ejholmes) | **447** | **284** | 2026-03-01 |
| ["MCP is dead?"](https://news.ycombinator.com/item?id=48330436) (quandri.io) | **400** | **410** | 2026-05-29 |
| ["Making MCP cheaper via CLI"](https://news.ycombinator.com/item?id=47157398) (kanyilmaz.me) | **324** | 119 | 2026-02-25 |
| ["MCP is dead; long live MCP"](https://news.ycombinator.com/item?id=47380270) (chrlschn) | **295** | 205 | 2026-03-14 |
| ["Mcp2cli – One CLI for every API, 96-99% fewer tokens"](https://news.ycombinator.com/item?id=47305149) | 146 | 100 | 2026-03-09 |

> **패턴:** 2026년 2월~5월에 **4개월 연속으로 "MCP는 죽었다"류 대형 스레드**가 올라왔다. 이건 단발성 백래시가 아니라 **지속적 논쟁**이다. 그리고 **매번 방어 측이 400+ 댓글로 반론**했다.

---

**🅰️ 관점 A — "그냥 CLI를 써라"**

- **rvz** (HN 47305149, 2026-03-09T07:51:52Z): MCP 자체가 근본적으로 결함이 있으며, **API를 직접 부르는 CLI 도구를 만들면 같은 결과**를 얻는다.
- **edgyquant** (HN 47305149, 2026-03-09T09:59:40Z): *"We had curl, HTTP and OpenAPI specs, but we created MCP. Now we're wrapping MCP into CLIs..."* — **순환 논리 조롱.**
- **Doublon** (HN 47305149, 2026-03-09T09:25:40Z): MCP는 서버 명령 실행 대안이 없어서 존재할 뿐. **SSH나 표준 CLI가 왜 기본이 아닌가.**
- **lukol** (HN 47208398, 2026-03-01T17:45:33Z): *"Simple REST APIs often do the job as well. **MCP felt like a vibe-coded fever dream from the start.**"*
- **qalmakka** (HN 47712718, 2026-04-10T07:03:39Z): *"**CLI is massively superior to MCP in my experience**"* — 토큰 경제성과 이해 가능성.
- **bb88** (HN 48330436, 2026-05-29): *"I was writing MCP servers, now I just write tools for agents to consume. **It's often easier.**"* — **전향 사례.**
- **jauntywundrkind** (HN 47712718, 2026-04-10T03:20:28Z): *"**With CLI tools, it all composes**"* — 파이프·스크립트 조합 가능. MCP는 모든 조합이 LLM을 거쳐야 한다.
- **zvoque** (HN 48330436, 2026-05-29): *"they always end up using **more tool calls/tokens** than if i had just written a script + skill"*
- **speff** (HN 48330436): *"Chrome/Ghidra MCP does have a tendency of **crashing**"* — 신뢰성.
- **eddythompson80** (HN 48330436): *"every MCP that could have been a CLI call is **a new opportunity for sandbox escape**"* — 보안 관점의 반대.
- **bluegatty** (HN 48330436): Codex의 MCP 관리가 *"really bad ... Everything from discovery, to management, to context window, to documentation — **it feels unfinished**"*
- **demorro** (HN 48330436): *"I fundamentally fail to understand how a protocol can make interfaces discoverable ... in a way that wouldn't also be achieved by making traditional interfaces more discoverable"*
- **🇰🇷 hulryung** (GeekNews 27129, ~2026-03): *"MCP보다 CLI로 툴을 직접 만들어 쓰기 시작했습니다"*
- **🇰🇷 jamsya** (GeekNews 27129, ~2026-03): *"**AWS MCP 안 깔아도 클로드 코드가 알아서 AWS CLI로 필요한 거 가져다 쓰더라구요**"* — 한국 실무자의 가장 구체적인 반증 사례.
- **🇰🇷 sonnet** (GeekNews 27129, ~2026-03): *"MCP가 이점이 없는 게 아니라 **무차별적으로 사용하던 환상에서 깨어난 거죠**"* — 균형 잡힌 요약으로 인용 가치 높음.
- **🇰🇷 kaydash** (GeekNews 30028, ~2026-05): *"개발할때는 쓸만하고 **서비스할때에는 비용문제 때문에 skill정도만** 쓰고있어요"* — **개발/운영 단계별 분기**라는 실무적 결론.

**🅱️ 관점 B — "MCP는 CLI가 못 하는 걸 한다"**

- **p_ing** (HN 47208398, 2026-03-01T18:13:20Z): *"**Tell my business users to use CLI when they create their agents. It's just not happening.** MCP is point-and-click for them."* — **가장 자주 인용될 반박.**
- **sebast_bake** (HN 47208398, 2026-03-01T19:09:57Z): *"CLI based integration does not exist in a single consumer grade ai agent product"*; MCP는 비개발자에게 *"security guardrails and simple consistent auth"* 제공.
- **0x696C6961** (HN 48330436, 2026-05-29): *"I have a couple MCP servers connected to my **Claude web & mobile** clients. **How would your clis work there?**"* — **CLI가 존재할 수 없는 환경**이라는 결정적 반론.
- **CharlieDigital** (HN 48330436): *"How do I guard those keys from both developer and agent? **Put it behind MCP; neither dev nor agent ever sees the key**"* — 자격증명 격리.
- **CharlieDigital** (HN 47305149, 2026-03-09T14:32:53Z): 엔터프라이즈에서 표준화된 스킬, 중앙화된 문서, **OTEL 관찰성**, OAuth 기반 신원 추적.
- **bb88** (HN 48330436, 관점 A와 같은 인물의 다른 각도): *"**MCP exists to take capability away from agents** ... tightly allowlist what the agent is capable of executing"* — **MCP를 "능력 제한 장치"로 재해석.** 논쟁 프레임을 바꾸는 인용.
- **DieErde** (HN 47305149, 2026-03-09T07:44:47Z): 검증·인가 계층으로서의 MCP — 세밀한 접근 제어.
- **SyneRyder** (HN 47305149, 2026-03-09T08:32:40Z): MCP는 에이전트가 **의도치 않은 엔드포인트를 발견·악용하는 걸 막고**, 파라미터 검증을 하며, **바이너리 파일·대용량 데이터 전송을 CLI보다 잘 다룬다.**
- **0xbadcafebee** (HN 48330436): *"MCP calls ... more likely to succeed because they have a **schema, well-defined errors** ... Compare that to shell one-liners"*
- **didibus** (HN 48330436): *"MCP is a JSON-RPC + a fixed auth/discovery handshake ... **Having a standard for that is really nice**"*; 또한 *"**MCPs are impossible to combine [like shell]** ... everything you feed or get from them goes through the model"* (한계도 인정); Asana·Square·Linear·Dropbox·Canva·Slack이 **MCP는 제공하지만 동등한 CLI는 없다**.
- **raincole** (HN 48330436): *"it's literally the only api standard that we truly made **plug and play** ... thousands of mcps"*
- **eikenberry** (HN 48330436): *"if you have **300 employees** ... you want to push an update to the skill, mcp provides you with a standard way"*
- **woeirua** (HN 47712718, 2026-04-10T03:17:16Z): 일부 **엔터프라이즈 환경에선 CLI를 쓸 수 없다.**
- **phpnode** (HN 47208398, 2026-03-01T17:47:35Z): 비개발자 앱이 임의 데이터 소스에 안전하게 붙으려면 *"there's really no sensible, safe path to using CLIs instead."*
- **mt42or** (HN 47208398, 2026-03-01T17:54:06Z): MCP 회의론자를 **쿠버네티스 회의론자에 비유** — 초기 비판에도 기술은 성숙한다.
- **🇰🇷 develosopher** (GeekNews 27129, ~2026-03): *"[SaaS 개발자라면] MCP를 먼저 선택할 것 같아요. **CLI 지원은 관리 포인트가 늘어나니까요**"* — 제공자(서버 저자) 관점의 반전.
- **🇰🇷 aer0700** (GeekNews 30028, ~2026-05): *"**죽었다기엔 이미 너무 많이 쓰고 있는데**"*

**⚖️ 중재적 관점 (책의 결론부에 유용)**
- **ejholmes** (원저자 본인, HN 47208398, 2026-03-01T19:12:25Z): *"The article title and content is **intentionally provocative**"* — MCP가 *"probably does actually make sense"*한 영역이 있음을 인정. **"MCP는 죽었다" 글의 저자조차 제목이 낚시였다고 인정했다**는 사실은 책에 반드시 넣을 것.
- **goodmythical** (HN 47208398, 2026-03-01T19:31:34Z): 학습 데이터에 없는 새 도구라면 **MCP든 CLI든 토큰 낭비는 똑같다** — 차이는 형식이 아니라 **친숙도**.
- **wenc** (HN 47208398, 2026-03-01T19:45:48Z): CLI는 *"precision instruments"* — DuckDB·jq 같은 도구가 구조화 데이터에 특히 강력.
- **goranmoomin** (HN 47208398, 2026-03-01T18:05:44Z): **MCP와 CLI 모두 skill 프레임워크 안에서 더 잘 동작**한다.
- **leonidasv** (HN 47712718, 2026-04-10T02:56:48Z): *"I still prefer hammer over screwdriver"* — **거짓 이분법**이라는 일침.
- **kristopolous** (HN 47305149, 2026-03-09T10:57:11Z): 벡터 검색(Qdrant)으로 **관련 MCP 서버만 동적 발견**하는 무한-MCP 게이트웨이 자작. → 문제를 프로토콜이 아니라 **아키텍처로** 푸는 3의 길.
- **jofzar** (HN 47305149, 2026-03-09T08:11:18Z): *"approximately the fifth similar tool seen in one week"* — 같은 해법의 반복 재발명.

### 논쟁 2 — MCP vs Skills (2026년의 새 전선)

- **robotobos** (HN 47712718, 2026-04-10T02:15:37Z): *"Skills are good for instilling **non-repeatable, yet intuitive or institutional knowledge**"*; 반복 작업은 MCP가 빠르고 결정론적.
- **charcircuit** (HN 47712718, 2026-04-10T02:42:09Z): *"**skills can call APIs**"* — 원글의 전제 자체를 반박.
- **dvcrn** (원저자, HN 47712718, 2026-04-10T09:28:19Z): *"can use the same MCP servers through **remote MCP on my phone, web, iPad**"* — 이식성.
- **Aperocky/alierfan** (HN 47712718, 2026-04-10T16:26:11Z): MCP의 **구조화된 I/O**가 텍스트 기반 도구 설명보다 도구 선택 일관성이 높다.
- **imron** (HN 47712718, 2026-04-10T04:20:31Z): **Skills 지시가 명확한데도 자주 무시된다**는 실무 보고. → Skills 옹호론의 약점.
- **simianwords** (HN 47712718, 2026-04-10T06:55:32Z): Skills에 설치 훅·의존성이 붙어 정식화되면 **MCP를 대체할 것**이라 예측.
- **BenFrantzDale** (HN 47712718, 2026-04-10T02:49:38Z): 왜 "documentation"이 아니라 "skills"라 부르나 — **사람에게서 정보를 숨기는 것**에 회의적.
- **🇰🇷 ng0301** (GeekNews 30028, ~2026-05): *"근데 저마저도 **mcp를 skills로 랩핑해서 쓰면 거기서 거기** 아니려나"*

### 논쟁 3 — 컨텍스트 비용은 여전히 문제인가

- **관점 A(문제다):** 0xbadcafebee의 7,500토큰 계산, SOLAR_FIELDS의 "upper bound", 여러 컨텍스트 절감 도구의 폭발적 등장 자체가 증거. 관련 대형 HN 스레드: ["MCP server that reduces Claude Code context consumption by 98%"](https://news.ycombinator.com/item?id=47193064) — **570점 / 107댓글 / 2026-02-28** (한국: [GeekNews 27108](https://news.hada.io/topic?id=27108), [29106](https://news.hada.io/topic?id=29106)).
- **관점 B(이미 해결됐다):** JoshGlazebrook의 deferred loading 85%+ 주장, red_hare의 "데이터가 7개월 낡았다", 🇰🇷 newdps의 "deferred tool로 이름만 넣도록 최적화". **→ 5-7 신선도 경고 참조.**
- **관점 C(문제는 다른 데 있다):** 🇰🇷 **newdps** (GeekNews 30028, ~2026-05)는 컨텍스트보다 **디버깅과 상태 관리의 어려움**이 더 큰 문제라고 지적. **이 책의 토픽 5가 존재하는 이유를 한국 실무자가 직접 말해준 셈.**

### 논쟁 4 — 보안: MCP는 방벽인가 공격면인가

- **방벽론:** CharlieDigital(키 격리), bb88(능력 제한), SyneRyder(엔드포인트 노출 차단), DieErde(인가 계층).
- **공격면론:** eddythompson80 — *"every MCP that could have been a CLI call is a new opportunity for sandbox escape"*.
- **경험적 증거 (양쪽 다 아닌 제3의 사실):** **CVE-2025-49596** (Inspector RCE, CVSS 9.4, 2025-07) — 방벽으로 만든 게 아니라 **디버깅 도구가 뚫렸다.** + `claude mcp list` 시크릿 유출(v2.1.161 수정) + 커밋된 `.mcp.json` 자기승인 차단(v2.1.196) + `headersHelper` 셸 인젝션 수정. → **MCP 생태계의 보안 문제는 프로토콜 논쟁이 아니라 툴체인에서 실제로 터졌다.**
- **미수집:** 프롬프트 인젝션·도구 포이즈닝에 대한 **커뮤니티 1차 토론**은 이번 범위에서 충분히 확보하지 못했다 (→ 부정적 발견).

### 논쟁 5 — stdio vs HTTP / 로컬 vs 원격

- **원격 옹호:** 0x696C6961(웹·모바일 클라이언트엔 CLI가 없다), dvcrn(폰·웹·iPad 이식성), didibus(대기업 SaaS는 MCP만 제공).
- **stdio의 구조적 약점 (1차 근거로 뒷받침됨):**
  - stdout 오염 취약 (5-1)
  - **OTel trace context 전파 불가** — 헤더가 없어 수동으로 실어야 함 (5-8)
  - 프로세스 생명주기 관리가 클라이언트 몫 → 누수·좀비 ([#74329](https://github.com/anthropics/claude-code/issues/74329))
  - 자동 재연결 동작이 **문서와 실제가 불일치** ([#74329](https://github.com/anthropics/claude-code/issues/74329))
- **HTTP/원격의 약점 (1차 근거):** OAuth 지옥 — [#67291](https://github.com/anthropics/claude-code/issues/67291) *"HTTP MCP server that requires OAuth **freezes entire CLI**"* (2026-06-11), [#44652](https://github.com/anthropics/claude-code/issues/44652) 403 step-up 재인가 미작동 (2026-04-07), [#47390](https://github.com/anthropics/claude-code/issues/47390) *"MCP OAuth SDK sends **empty User-Agent**, causing 403 from WAF/Cloudflare-protected servers"* (2026-04-13), [#67999](https://github.com/anthropics/claude-code/issues/67999) Google Desktop OAuth 클라이언트 시크릿 거부 (2026-06-12), [#62419](https://github.com/anthropics/claude-code/issues/62419) 등.
  - **v2.1.196:** *"Fixed MCP OAuth requesting the authorization server's full `scopes_supported` catalog when no scope is specified, causing `invalid_scope` failures on GitLab self-hosted and other enterprise IdPs"* → **자체 호스팅 IdP를 쓰는 한국 기업 환경에 특히 관련.**
  - **🇰🇷 CORS 함정:** 한 한국어 자료가 *"OAuth discovery 엔드포인트에 CORS 헤더가 빠져 브라우저 로그인이 자동으로 안 열리는 문제 ... curl로 테스트하면 정상이라 원인 찾는 데 시간이 걸렸다. MCP SDK가 fetch API로 호출하기 때문에 CORS preflight가 필요"*라고 보고. **⚠️ 검색 요약에서 수집, 원문 URL·작성일 특정 실패 (확인 필요).** 다만 "curl은 되는데 브라우저는 안 된다"는 증상 패턴은 실무적으로 매우 그럴듯하며 책에 넣을 가치가 있음 — **저술 전 원문 확보 필요.**
- **중립적 사실:** 원격 MCP 진영은 인증 표준화가 진행 중 — ["Zero-Touch OAuth for MCP"](https://news.ycombinator.com/item?id=48592163) (blog.modelcontextprotocol.io), **278점 / 103댓글 / 2026-06-18**.

---

## 신선도 원장

모든 소스의 작성일. **검색 시점 2026-07-26.**

### 1차 소스 — GitHub 이슈 (`gh issue view`로 본문·댓글 직접 확인)
| 소스 | 작성일 | 상태 | 명시된 버전 |
|---|---|---|---|
| [claude-code #48866](https://github.com/anthropics/claude-code/issues/48866) stdout/stderr 문서 누락 | 2026-04-16 | closed(not planned) | 2.1.105 리그레션 언급 |
| [claude-code #43968](https://github.com/anthropics/claude-code/issues/43968) 헤드리스 MCP 실패 무신호 | 2026-04-05 | closed(중복 자동종료) | **2.1.92** |
| [claude-code #68375](https://github.com/anthropics/claude-code/issues/68375) `claude -p` 도구 호출 행 | 2026-06-14 | **open** | **2.1.177 리그레션** |
| [claude-code #74329](https://github.com/anthropics/claude-code/issues/74329) 프로세스 누수·오등록해제 | 2026-07-05 (댓글 2026-07-20) | **open** | **2.1.201** |
| [claude-code #80996](https://github.com/anthropics/claude-code/issues/80996) `--resume` 후 복구 경로 없음 | **2026-07-24** | **open** | — |
| [claude-code #81268](https://github.com/anthropics/claude-code/issues/81268) 2048자 조용한 절단 | **2026-07-26 (당일)** | **open** | **2.1.220** |
| [claude-code #7279](https://github.com/anthropics/claude-code/issues/7279) in-process SDK MCP 무음 실패 | **2025-09-07** ⚠️구식 | closed | — |
| [claude-code #56263](https://github.com/anthropics/claude-code/issues/56263) `Optional[X]` 스키마 제거 | 2026-05-05 | **open** | — |
| [claude-code #80016](https://github.com/anthropics/claude-code/issues/80016) Desktop `tools/call` 미디스패치 | 2026-07-22 | **open** | — |
| [claude-code #78726](https://github.com/anthropics/claude-code/issues/78726) `/mcp reconnect`가 멀쩡한 서버 죽임 | 2026-07-18 | **open** | — |
| [claude-code #77296](https://github.com/anthropics/claude-code/issues/77296) 16KB 스키마 드롭 | 2026-07-13 | closed | — |
| [claude-code #80276](https://github.com/anthropics/claude-code/issues/80276) Desktop 심링크 설정 파괴 | 2026-07-22 | **open** | — |
| [claude-code #74768](https://github.com/anthropics/claude-code/issues/74768) Desktop DCR client_name 403 | 2026-07-06 | **open** | — |
| [dirmacs/daedra #4](https://github.com/dirmacs/daedra/issues/4) stdout 로깅 | (날짜 미확인 ⚠️) | — | — |
| [claude-code #8288](https://github.com/anthropics/claude-code/issues/8288) 스코프 가시성 + 79k/36k/20k 토큰 실측 | **2025-09-28** ⚠️구식 | closed | — |
| 스코프 이슈군 #68603/#68605 | 2026-06-15 | closed | — |
| 스코프 이슈군 #17668 | 2026-01-12 | **open** | — |
| OAuth 이슈군 #44652/#47390/#67291/#67999 | 2026-04-07 / 04-13 / 06-11 / 06-12 | 대부분 closed | — |

### 1차 소스 — CHANGELOG (버전 매핑 확인, 2026-07-26 스냅샷)
최신 릴리스: **2.1.220**. 인용한 항목의 버전: 2.1.219(`mcp_server_errors`), 2.1.212(2분 자동 백그라운드), 2.1.208(stderr 64MB 누수, 7배 CPU 최적화), 2.1.206(60초 기본 타임아웃 버그), 2.1.196(`.mcp.json` 자기승인 차단, OAuth scope), 2.1.190·2.1.191(에러 메시지 개선), 2.1.187(5분 원격 행), 2.1.179(`tools fetch failed`), 2.1.170(`--safe-mode`), 2.1.163(`CLAUDE_CODE_SESSION_ID`), 2.1.162(sub-1000ms timeout), 2.1.161(**시크릿 유출 수정**), 2.1.159(`OTEL_LOG_TOOL_DETAILS`), 2.1.154(pending approval), 2.1.152(strict-mcp-config/subagent), 2.1.148·2.1.150(`/usage` MCP별 비용), 2.1.144(페이지네이션 도구 드롭), 2.1.105(stdout 리그레션, #48866 인용).

### 1차 소스 — HN 스레드 (Algolia API로 점수·댓글수·작성일 확인)
| 스레드 | 날짜 | 점수/댓글 |
|---|---|---|
| I still prefer MCP over skills (47712718) | 2026-04-10 | 460/375 |
| When does MCP make sense vs CLI (47208398) | 2026-03-01 | 447/284 |
| MCP is dead? (48330436) | 2026-05-29 | 400/410 |
| Making MCP cheaper via CLI (47157398) | 2026-02-25 | 324/119 |
| MCP is dead; long live MCP (47380270) | 2026-03-14 | 295/205 |
| Zero-Touch OAuth for MCP (48592163) | 2026-06-18 | 278/103 |
| Context 98% 절감 MCP (47193064) | 2026-02-28 | 570/107 |
| Mcp2cli (47305149) | 2026-03-09 | 146/100 |
| MCP Spec 2025-06-18 changelog (44314289) | 2025-06-18 ⚠️구식 | 200/121 |
| 원조 MCP 발표 (42237424) | **2024-11-25** ⚠️매우 구식 | 872/258 |

### 1차 소스 — 리포지토리 (`gh repo view`, 2026-07-26)
- steipete/claude-code-mcp: 생성 2025-05-13, 마지막 푸시 2026-05-15, **아카이브됨**, 1,313⭐
- grahama1970/claude-code-mcp-enhanced: 생성 2025-05-15, 마지막 푸시 **2025-05-20**, 125⭐
- SinanTufekci/agent-intern: 생성 2026-05-22, 마지막 푸시 **2026-07-24**, 16⭐. README에 검증 버전 명시: agy 1.1.6 / codex-cli 0.144.1 / copilot-cli 1.0.69 / cursor-agent 2026.07.08

### 국내 커뮤니티
- [GeekNews 30028 "MCP는 죽었나?"](https://news.hada.io/topic?id=30028) — 게시 "2달전" ≈ **2026-05** (원문 2026-05-29 기준)
- [GeekNews 27129 "MCP는 죽었다. CLI 만세"](https://news.hada.io/topic?id=27129) — 게시 "4달전" ≈ **2026-03** (원문 2026-02-28), 36P
- [GeekNews 27108 / 29106](https://news.hada.io/topic?id=27108) Context Mode — 2026-02·2026-04 추정
- velog @takuya, @co-vol, @s_soo100 글들 — **작성일 개별 특정 실패 ⚠️** (2025~2026 추정)
- [wikidocs 클로드 코드 가이드 08. MCP 서버](https://wikidocs.net/333423) — 날짜 미확인

### 2차 소스 (요약 블로그 — 원 출처 미확인, 인용 시 주의)
digitalapplied.com·apigene.ai(Inspector 한계), elastic.co·signoz.io·oneuptime.com(OTel, OneUptime은 2026-03-26), builder.io·mcpbundles.com·chatforest.com·skiln.co(설정/디버깅 요약). **→ 책에는 위 1차 소스를 우선 인용할 것.**

### 보안 공시
CVE-2025-49596 (MCP Inspector RCE, CVSS 9.4, <0.14.1) — 공개 **2025-07** (Qualys 2025-07-03). [GHSA-7f8r-222p-6f5g](https://github.com/advisories/GHSA-7f8r-222p-6f5g)

---

## 확인하지 못한 것 / 부정적 발견

**부정적 발견도 1급 결과다. 아래는 "찾아봤으나 없었다" 또는 "확인 실패"의 정직한 목록이다.**

> **📌 Phase 4 fact-checker에게:** 이 섹션의 `(확인 필요)`·`⚠️` 표시는 **챕터 초고의 `(사실 확인 필요)` 마커가 아니다.** 리서처 수준의 **출처 확보 실패 기록**이며, 이미 내가 찾다 실패한 항목들이다(특히 6·7번의 Perplexity·21k토큰 수치는 상당한 검색 후에도 원 출처를 못 찾았다). **당신의 백로그로 삼아 Critical 등급 웹 예산을 재소모하지 말 것.** 대신 이 라벨들은 **저술가가 해당 주장을 본문에 쓰지 못하도록 막는 차단선**으로 기능해야 한다. 반대로 11번(CLI 플래그)은 저술 시점에 `claude mcp --help`로 **반드시 채워야 하는** 항목이다.

### 접근 차단
1. **Reddit 전면 차단.** `old.reddit.com/r/mcp/search?...`에 대해 도구가 *"Claude Code is unable to fetch from old.reddit.com"* 반환. **r/mcp·r/ClaudeAI·r/LocalLLaMA의 1차 토론을 이번 리서치에서 전혀 수집하지 못했다.** 브리프가 지정한 주요 소스 중 가장 큰 공백. → 필요 시 특정 퍼머링크를 웹 검색으로 발견한 뒤 개별 fetch하는 우회가 필요.
2. **Lobsters·Dev.to·Mastodon·X·Discord/Slack 공개 로그** — 시간 배분상 체계적으로 탐색하지 못했다. Dev.to 글 1건이 검색에 걸렸으나 2차 요약 성격이라 채택하지 않음.

### 검증 실패 / 확인 필요 항목 (책에 쓰기 전 반드시 재확인)
3. **MCP 스코프 우선순위(local > project > user)** — 다수 2차 블로그가 일치하나 **1차 공식 문서로 직접 확인하지 못했다.** 단정 금지.
4. **"Deferred tool loading은 2025년 11월 추가"** (red_hare 주장) — **날짜 미검증.** 기능 존재 자체는 `total_deferred_tools` 필드로 1차 확인됨.
5. **"deferred loading이 컨텍스트를 85%+ 절감"** (JoshGlazebrook 주장) — Anthropic 공식 수치인지 **원 출처 미확인.**
6. **"Linear/Notion/Slack/Postgres MCP 도구 정의가 21,000토큰 = 200K 컨텍스트의 10.5%"** — 초기 검색의 2차 요약에서 나왔으나 **원 출처를 찾지 못해 본문에서 제외했다.** 유사 취지의 1차 인용(0xbadcafebee의 7,500토큰)으로 대체함.
7. **"Perplexity CTO Denis Yarats가 MCP 이탈 선언, 72% 컨텍스트 세금"** — 초기 검색의 2차 요약 주장. **1차 확인 실패로 본문에서 제외.** 사실이라면 강력한 소재이니 별도 검증 권장.
8. **"HN 논쟁 195점/174댓글"** — 초기 2차 요약의 수치. **어느 스레드인지 특정 실패.** 대신 HN API로 직접 확인한 6개 스레드의 정확한 수치로 대체함.
9. **한국어 CORS/OAuth discovery 함정 사례** — 검색 요약에는 구체적으로 나오나 **원문 URL·작성자·작성일 특정 실패.**
10. **`dirmacs/daedra#4`의 작성일** — 미확인.
11. **`claude mcp add` / `claude mcp list` / `remove`의 정확한 현행 플래그 세트** — **의도적으로 기억에서 쓰지 않았다.** 저술 시 `claude mcp --help` 실행 결과 또는 공식 문서로 채울 것.
12. ~~**[#8288]의 본문·날짜 미확인**~~ → **해소됨 (2026-07-26 재확인):** 2025-09-28 작성, 본문·실측 토큰 수치 확보. 4-1 절에 반영.

### 실제로 논의가 희소한 영역 (검색했으나 나오지 않음)
13. **토픽 6은 정말로 얇다.** `gh search repos`를 "mcp server spawns claude code subagent", "codex cli mcp server delegate", "mcp server claude code sub-agent orchestrator" 등 여러 쿼리로 돌렸으나 **모두 빈 결과**. 발견한 구현체는 3개뿐이고, 그중 **최대 리포는 아카이브, 2위는 14개월 방치**다. → **이건 실패가 아니라 결과다: 이 패턴은 2026-07 현재 소수의 실험적 프로젝트만 존재하며, 정착된 실무 관행이 아니다.**
14. **토픽 6의 "비용 폭발·재귀" 사례 없음.** 중첩 에이전트의 비용 폭주나 무한 재귀에 대한 **구체적 사고 보고를 하나도 찾지 못했다.** 발견한 것은 (a) 샌드박스 부재 경고, (b) 타임아웃 1시간 설정, (c) 병렬 시 HOME 상태 경합 — 즉 **비용보다 권한·상태 문제가 먼저 보고되고 있다.** 오히려 이 패턴의 명시적 동기가 **비용 절감(쿼터 차익거래)**이었다는 점이 반직관적 발견.
15. **MCP 프롬프트 인젝션·도구 포이즈닝의 커뮤니티 1차 토론** — 보안 벤더 블로그는 많으나 **실무자 커뮤니티의 날것 토론을 확보하지 못했다.** 별도 리서치 권장.
16. **Java/Kotlin MCP 서버 개발 실무 논의 미발견.** 대상 독자에 Java 실무자가 포함되는데, 커뮤니티 토론은 **TypeScript·Python에 압도적으로 편중**되어 있다. C# 가이드 1건이 검색에 걸린 게 전부. → **책이 Java를 다룬다면 커뮤니티 근거 없이 1차 SDK 문서에 의존해야 한다.** 기획 단계에서 인지할 것.
17. **국내 커뮤니티의 토픽 5·6 논의 없음.** GeekNews는 **논쟁(토픽 4의 일부와 논쟁점)에는 활발**하지만, **디버깅 실무(토픽 5)나 에이전트 오케스트레이션(토픽 6)에 대한 한국어 1차 토론은 발견하지 못했다.** OKKY·커리어리에서도 유의미한 MCP 개발 스레드를 찾지 못함. velog는 대부분 "사용법 소개" 성격이고 삽질 회고는 드물다.
    → **책의 포지셔닝 기회:** 토픽 5·6에 대한 **한국어 자료가 사실상 없다.** 이 책이 채울 수 있는 진짜 공백.
