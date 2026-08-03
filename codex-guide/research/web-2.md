# 그룹 B: 기능·레퍼런스·설정·커스터마이징 (34 URL) — 검색 2026-08-02 기준

<!-- 검색 시점: 2026-08-02 기준 -->
<!-- 출처: OpenAI Codex 공식 문서 https://learn.chatgpt.com -->
<!-- 수집 방식: 경로 끝에 `.md`를 붙인 원문 markdown을 curl로 수집 (WebFetch는 표·코드블록을 요약 소실시킴) -->
<!-- 신뢰성: 전 항목 "최상" (공식 1차 문서, 원문 무손실) -->
<!-- 개정: 2026-08-02 전 34개 URL을 .md 원문으로 재수집해 표·코드블록 복원. 이전 WebFetch 판본은 web-2_v1_webfetch.md에 보존 -->

## 이 문서 사용법 (fact-checker·저술가 필독)

- **원문 전문은 `research/codex-docs-raw/` 에 34개 파일로 그대로 저장돼 있다.** 파일명은 URL 경로의 `/`를 `__`로 바꾼 것 (예: `/codex/config-file/config-reference` → `codex__config-file__config-reference.md`). 인용 문구가 정확한지 다툼이 생기면 **이 원문 파일이 최종 판정 기준**이다.
- `codex-docs-raw/_config-reference-tables.md` 는 `config-reference` 페이지의 JSX `ConfigTable`을 파싱해 마크다운 표로 변환한 것 — **`config.toml` 274키 + `requirements.toml` 116키 전수**.
- 아래 본문은 그 원문에서 뽑은 **정리본 + 대응 관점 메모**다. 원문에 없는 내용은 쓰지 않았다.
- **수집 기법 메모:** `https://learn.chatgpt.com{경로}.md` 로 요청하면 원문 markdown이 그대로 온다. 각 문서 상단에도 이 사실이 명시돼 있다 — "Markdown versions of documentation pages are available by appending `.md` to the page URL."
- **공식 JSON 스키마:** `config.toml`의 최신 JSON 스키마가 https://learn.chatgpt.com/docs/config-schema.json 에 있다 (config-reference 페이지에서 링크). 설정 키 검증의 1차 근거로 쓸 수 있다.

## 버전·모델 기준선 (2026-08-02 문서 스냅샷)

| 항목 | 값 | 출처 |
|---|---|---|
| 권장 기본 모델 | `gpt-5.6` | config-sample, config-basic |
| 서브에이전트 모델 3종 | `gpt-5.6`(고난도) / `gpt-5.6-terra`(속도) / `gpt-5.6-luna`(빠르고 좁은 작업) | subagents |
| 실시간 코딩 특화 모델 | `gpt-5.3-codex-spark` (리서치 프리뷰, ChatGPT Pro 한정, 별도 한도) | speed, subagents |
| 이미지 생성 모델 | `gpt-image-2` | image-generation |
| Fast mode 지원 모델 | GPT-5.6, GPT-5.5, GPT-5.4 | speed |
| WSL1 지원 종료 | Codex **0.114** | wsl |
| 관리형 permission profile 허용목록 최소 버전 | Codex **0.138.0** 이상 (0.137.0 이하는 무시) | config-reference |

---

## 1. 기능 확장 (Feature)

### Web search
- URL: https://learn.chatgpt.com/codex/web-search
- 원문: `codex-docs-raw/codex__web-search.md`
- 검색: 2026-08-02 기준 / 신뢰성: 최상
- 핵심 내용: 데스크톱 앱·웹·CLI·IDE 확장 전 표면에 내장된 웹 검색. 로컬 Codex는 **기본이 캐시 검색(cached)** — 임의 페이지를 라이브로 긁는 대신 OpenAI가 관리하는 인덱스를 쓴다.
- 설정 키 `web_search` 4값:
  | 값 | 의미 |
  |---|---|
  | `cached` | **기본값.** OpenAI 관리 인덱스에서 사전 색인된 결과를 제공. "lowers—but doesn't remove—prompt injection risk" |
  | `indexed` | 검색 인덱스가 게이트할 때만 외부 웹 접근 허용 |
  | `live` | 최신 데이터를 라이브로 가져옴 (`--search`와 동일) |
  | `disabled` | 도구 끔 |
- CLI: `codex --search "Summarize the latest release notes for this dependency"`
- 제약: **"All web results should be treated as untrusted input."** / `--yolo` 등 full-access 샌드박스에서는 web search 기본값이 `live`로 바뀐다 (config-sample 주석) / 검색은 트랜스크립트와 `codex exec --json` 출력에 `web_search` 항목으로 남는다 / 클라우드 네트워크 경계는 `/codex/cloud/internet-access` 별도 정책.
- Claude Code 대응: WebSearch/WebFetch에 대응하나, Codex는 **"캐시 인덱스 기본 / 라이브는 옵트인"이라는 보안 등급 다이얼을 설정 키 하나로 노출**한다는 점이 구조적 차이.

### Image generation
- URL: https://learn.chatgpt.com/codex/image-generation · 원문: `codex__image-generation.md`
- 모델: **`gpt-image-2`** — "Built-in image generation uses `gpt-image-2`"
- 사용량: "Image generations use included limits **3–5x faster on average** than similar turns without image generation" (품질·크기에 따라)
- 호출: `$imagegen` (명시 호출) / CLI `-i`·`--image` (참조 이미지 첨부)
- 프롬프트 모범 사례: 1~3문장 + 목적·대상 / 주체와 동작 / 배경·구도·시각 스타일 / 프레이밍·조명·색·재질 / 등장 금지 제약. 다중 참조는 콘텐츠용·스타일용 분리. 텍스트는 따옴표 안 정확 문구 + 폰트. 인포그래픽은 정보 위계 서술 + 짧은 라벨. 실존 인물은 참조 사진 + 허가 확인.
- Claude Code 대응: 내장 이미지 생성 도구 없음(MCP 경유). `$` 접두어는 Codex의 스킬 명시 호출 문법.

### Image inputs
- URL: https://learn.chatgpt.com/codex/image-inputs · 원문: `codex__image-inputs.md`
- CLI 예시 (원문 그대로):
  ```
  codex -i screenshot.png "Explain this error and suggest the smallest fix"
  codex --image before.png,after.png "Compare these states and list the regressions"
  ```
- 다중 이미지는 쉼표 구분 또는 `--image` 반복. PNG·JPEG 등 일반 포맷.
- 표면별: 데스크톱 앱·Chrome 확장은 **Shift 누른 채 드래그**(에디터로 넘어가지 않게), 웹은 첨부·붙여넣기·드래그.
- 원칙: "don't rely on the image alone to communicate the task" — 무엇을 볼지, 무엇을 원하는지 문장으로 쓸 것.
- 문서 예시 프롬프트: "Compare this checkout screen with the design. Fix spacing and typography only; do not change behavior. Verify the result with a new screenshot."

### Appshots
- URL: https://learn.chatgpt.com/codex/appshots · 원문: `codex__appshots.md`
- **macOS 데스크톱 앱 전용.** 최전면 앱 창을 캡처해 컨텍스트로 전달.
- 캡처 2종: (1) 보이는 창의 이미지 (2) 그 창의 사용 가능 텍스트 — **앱이 접근성으로 노출하는 화면 밖(off-screen) 텍스트 포함**
- 단축키: **양쪽 Command 키 동시 누름** (커스텀 핫키 가능)
- 동작 규칙: 기본은 새 채팅 시작. 단 **60초 이내**에 어떤 채팅과 상호작용했다면 그 대화에 추가.
- 권한: Screen & System Audio Recording(창 캡처), Accessibility(텍스트 읽기)
- 제약: **CLI에서는 사용 불가.** Google Docs·Gmail·Sheets·Slides는 전체 문서 텍스트 없이 보이는 스크린샷만 줄 수 있음.
- Claude Code 대응: 대응물 없음. claude-in-chrome은 브라우저 한정이나 Appshots는 **OS 레벨 최전면 창 + 접근성 텍스트**.

### Chrome extension
- URL: https://learn.chatgpt.com/codex/chrome-extension · 원문: `codex__chrome-extension.md`
- 이미 로그인된 사이트(LinkedIn·Salesforce·Gmail·사내 도구)를 읽고 조작. 작업은 **Chrome 탭 그룹**으로 정리.
- 설치: 데스크톱 앱의 **Plugins Directory** → Chrome 권한 승인 → 사이드 채팅 로드 확인
- 접근 제어: **새 도메인마다 사전 허가 요청.** 한 번만 / 이 사이트 / 모든 사이트 / 거부
- 데이터: Chrome 액션의 별도 기록은 없으나 채팅 컨텍스트에 들어간 것(읽은 텍스트·스크린샷·요약)은 저장. Computer Use는 **Memories 설정을 존중**. **브라우저 히스토리 접근은 요청마다 확인.**
- 핵심: Chrome 권한은 기능을 가능하게 할 뿐, ChatGPT는 그 위에 자체 확인·설정·허용/차단 목록을 적용한 뒤 사이트를 쓴다.

### Work with files (경로는 `/codex/artifacts-viewer`)
- URL: https://learn.chatgpt.com/codex/artifacts-viewer · 원문: `codex__artifacts-viewer.md`
- **⚠️ 실제 페이지 제목은 "Work with files"다.** 리다이렉트가 아니라 이 경로가 곧 그 문서다 (원문 md의 H1으로 확정).
- 표면별 기능:
  | 표면 | 기능 |
  |---|---|
  | 데스크톱 앱 | 문서·프레젠테이션·스프레드시트·PDF 미리보기. `.html`·`.htm`은 **인터랙티브 HTML 미리보기**. 렌더↔소스 전환. **주석(annotation)** 으로 국소 수정 요청 |
  | ChatGPT Work (웹) | 첨부·리뷰·다운로드·표적 피드백 |
  | Codex CLI | 파일 생성·편집만. **시각적 미리보기·주석 없음.** 출력 경로와 검증 결과 보고 |
  | IDE 확장 | 워크스페이스 파일 생성·편집, 에디터 리뷰, 호환 뷰어로 열기 |
- Claude Code 대응: Artifact와 겹치나 성격이 다름 — Claude는 **공유 가능한 호스팅 페이지**, Codex는 **로컬 파일 + 앱 내 미리보기·주석**. 파일 주석 기반 국소 수정은 Claude Code에 대응물 없음.

---

## 2. 레퍼런스 (Reference)

### Commands — 키보드 단축키 & 딥링크
- URL: https://learn.chatgpt.com/codex/reference/commands · 원문: `codex__reference__commands.md`
- 검색: 2026-08-02 기준 / 신뢰성: 최상
- 핵심: **ChatGPT 데스크톱 앱**의 명령·단축키 레퍼런스. `/` 슬래시 명령은 별도 문서.

**키보드 단축키 (원문 전수)**

| 구분 | Action | Shortcut |
|---|---|---|
| **General** | Command menu | Cmd/Ctrl + Shift + P 또는 Cmd/Ctrl + K |
| | Settings | Cmd/Ctrl + , |
| | Keyboard shortcuts | Cmd/Ctrl + Shift + / |
| | Open folder | Cmd/Ctrl + O |
| | Navigate back | Cmd/Ctrl + [ |
| | Navigate forward | Cmd/Ctrl + ] |
| | Increase font size | Cmd/Ctrl + + |
| | Decrease font size | Cmd/Ctrl + - |
| | Toggle sidebar | Cmd/Ctrl + B |
| | Open review tab | Ctrl + Shift + G |
| | Toggle review panel | Cmd/Ctrl + Alt + B |
| | Toggle bottom panel | Cmd/Ctrl + J |
| | Toggle terminal | Ctrl + ` |
| | Clear the terminal | Ctrl + L |
| **Chat** | Quick chat | Cmd + Option + N (macOS) / Ctrl + Alt + N (Windows) |
| | New chat | Cmd/Ctrl + N 또는 Cmd/Ctrl + Shift + O |
| | Search chats | Cmd/Ctrl + G |
| | Find in chat | Cmd/Ctrl + F |
| | Previous chat | Cmd/Ctrl + Shift + [ |
| | Next chat | Cmd/Ctrl + Shift + ] |
| **Input** | Dictation | Ctrl + Shift + D |

- 커스터마이징: **Settings > Keyboard Shortcuts**. 명령 이름으로 검색하거나 **키스트로크 모드**로 전환해 원하는 조합을 눌러 찾는다.
- 검색: 채팅 검색(Cmd/Ctrl+G)은 "expanded matching"이 가능하면 **채팅 본문과 Git 브랜치 이름까지** 매칭한다 (예: `fix/login-redirect`). Find in chat(Cmd/Ctrl+F)은 현재 채팅 안만 검색한다.

**딥링크 — 지원 링크 (canonical form)**

| Deep link | Opens |
|---|---|
| `codex://threads/new` | A new local chat. |
| `codex://new?<query>` | A new local chat with at least one query parameter. |
| `codex://threads/<thread-id>` | A local chat. `<thread-id>` is its technical thread ID. |
| `codex://settings` | Settings. |
| `codex://settings/connections/<connection-type>` | Computer, device, or SSH connection settings. |
| `codex://settings/connections/ssh/add?name=<ssh-config-host>` | Adds a host from your SSH config to Codex. |
| `codex://skills` | Skills. |
| `codex://automations` | Scheduled with the create flow open. |
| `codex://plugins/install/<plugin-name>?marketplace=<marketplace-name>` | The install flow for a plugin from a known marketplace. |
| `codex://plugins/<plugin-id>` | A plugin detail page. |
| `codex://plugins/<plugin-name>?marketplacePath=<absolute-marketplace-path>` | A local plugin detail page from a local marketplace. |
| `codex://pets/install?name=<pet-name>&imageUrl=<https-image-url>` | The pet install flow. |

> "The ChatGPT desktop app keeps the `codex://` URL scheme for compatibility, so links can open specific parts of the app directly. Encode query string values before adding them to a URL."

**딥링크 — Chats 세부**

| Deep link | Opens |
|---|---|
| `codex://threads/<thread-id>` | A local chat. `<thread-id>` is its technical thread ID. |
| `codex://threads/new` | A new local chat. |
| `codex://threads/new?<query>` | A new local chat with optional query parameters. |
| `codex://new?<query>` | A new local chat. Include at least one of `prompt`, `path`, or `originUrl`; otherwise the link does nothing. |

| Query parameter | Required | What it does |
|---|---|---|
| `prompt=<text>` | No | Sets the initial composer text. |
| `path=<absolute-path>` | No | Opens the new chat in a local workspace. `path` must be an absolute path to a local directory. When valid, Codex uses that directory as the active workspace. |
| `originUrl=<git-remote-url>` | No | Matches one of your current workspace roots by Git remote URL. If `path` is also present, Codex resolves `path` first. |

**플러그인 멘션으로 채팅 시작** — 프롬프트에 플러그인 멘션을 넣고 URI 인코딩한다:
```text
[@Example](plugin://example@openai-curated) Summarize this document: https://example.com/document/123
```
```text
codex://new?prompt=%5B%40Example%5D(plugin%3A%2F%2Fexample%40openai-curated)%20Summarize%20this%20document%3A%20https%3A%2F%2Fexample.com%2Fdocument%2F123
```
링크는 디코드된 프롬프트를 컴포저에 넣을 뿐 **자동 전송하지 않는다.** 플러그인이 미설치면 Codex가 설치와 커넥터 연결을 요청하고, 설정 후 **Continue**로 같은 채팅을 재개한다.

**딥링크 — Settings 세부**

| Deep link | Opens |
|---|---|
| `codex://settings` | Settings. |
| `codex://settings/browser-use` | Browser settings. |
| `codex://settings/computer-use/google-chrome` | Google Chrome settings for computer use. |
| `codex://settings/connections` | Remote connections settings. |
| `codex://settings/connections/computer` | Settings for controlling this Mac or PC from another device. |
| `codex://settings/connections/devices` | Settings for controlling other devices. |
| `codex://settings/connections/ssh` | SSH connection settings. |
| `codex://settings/connections/ssh/add?name=<ssh-config-host>` | Adds the named host alias as a Codex-managed connection, then opens SSH connection settings. |

`name` 값은 `~/.ssh/config`의 host alias와 일치해야 한다. 링크는 추가된 호스트의 자동 연결을 비활성화한다. 호스트를 못 찾으면 SSH 설정을 열고 오류를 표시한다. 지원하지 않는 `codex://settings/...` 경로는 메인 Settings로 간다.

**딥링크 — Plugins 세부**

| Query parameter | Required | What it does |
|---|---|---|
| `marketplace=<marketplace-name>` | Yes | Identifies the marketplace. For an OpenAI-curated plugin, use `openai-curated`. |
| `hostId=<host-id>` | No | Identifies the Codex host that owns the plugin context, such as `local` or one of your configured remote connections. Codex provides these IDs. |
| `source=manage` | No | Preserves the app's plugin-management entry point. It's not admin-only. |
| `marketplacePath=<absolute-marketplace-path>` | Yes (로컬) | Absolute path to the local `marketplace.json`, for example `/Users/alex/.agents/plugins/marketplace.json`. |
| `mode=share` | No | Opens the share flow for that local plugin. |

`<plugin-id>`는 플러그인을 식별해야 하며, OpenAI 큐레이션 플러그인은 `<plugin-name>@openai-curated` 형식을 쓴다.

**딥링크 — Pets 세부**

| Query parameter | Required | What it does |
|---|---|---|
| `name=<pet-name>` | Yes | Sets the pet name. The value must contain at least one non-whitespace character. |
| `imageUrl=<https-image-url>` | Yes | Provides an absolute HTTPS URL for the pet image or sprite sheet. |
| `description=<text>` | No | Adds a description to the install flow. |
| `spriteVersionNumber=<1-or-2>` | No | Selects the sprite-sheet format. The default is `1`; the only other supported value is `2`. |

잘못된 이름, 비-HTTPS 이미지 URL, 미지원 sprite 버전, 추가 경로 세그먼트가 있으면 링크는 아무 동작도 하지 않는다.

- Claude Code 대응: 키바인딩 커스터마이징은 `~/.claude/keybindings.json`과 대응. **`codex://` 딥링크 스킴은 Claude Code에 대응물이 없는 앱 간 연동 진입점** — 특히 `codex://new?prompt=...&path=...`로 외부 도구가 작업을 킥오프할 수 있다는 점이 설계상 큰 차이.

### Slash commands (데스크톱 앱)
- URL: https://learn.chatgpt.com/codex/reference/slash-commands · 원문: `codex__reference__slash-commands.md`
- 사용법: 컴포저에서 `/` 입력 → 목록 선택 또는 계속 입력해 필터(`/status` 등)
- **`$` 접두어로 스킬을 명시 호출**할 수 있다. 활성 스킬도 슬래시 목록에 나타나며, **커스텀 프롬프트는 `/prompts:<name>` 형태**로 나타난다.

| Slash command | Description |
|---|---|
| `/approve` | Approve one retry of a recent automatic-review denial, when automatic review is active. |
| `/cloud` | Run the chat in the cloud, when cloud execution is available. |
| `/cloud-environment` | Choose the cloud environment for the chat. |
| `/compact` | Compact the current chat's context. |
| `/fast` | Turn a catalog-provided Fast service tier on or off, when available. |
| `/feedback` | Open the feedback dialog to submit feedback and optionally include logs. |
| `/fork` | Copy a local chat into a new local chat or worktree. |
| `/goal` | Set a persistent goal for ChatGPT to work toward; use `/plan` first to shape it. |
| `/ide-context` | Turn shared IDE context on or off. |
| `/init` | Generate an `AGENTS.md` scaffold for the current project. |
| `/local` | Run the chat in the selected local project. |
| `/mcp` | Open MCP status to view connected servers. |
| `/memories` | Configure whether the chat can use or generate memories, when Memories is available. |
| `/model` | Choose the model for the current chat. |
| `/pet` | Wake or tuck away the desktop pet. |
| `/personality` | Choose how Codex responds, when the current model supports personalities. |
| `/plan` | Toggle plan mode for multi-step planning. |
| `/project` | Choose a project for new chats. |
| `/reasoning` | Choose the reasoning effort for the current chat. |
| `/review` | Start code review mode to review uncommitted changes or compare against a base branch. |
| `/side` | Start a temporary side chat without interrupting the main chat. |
| `/status` | Show the chat ID, context usage, and rate limits. |
| `/task` | Start a chat without a project. |
| `/worktree` | Run the chat in a new Git worktree. |

- `/goal` 상세: "A goal is a persistent objective that ChatGPT works toward until it finishes the task, pauses, or needs more input." `/plan`으로 먼저 다듬고 `/goal`로 설정. 활성 시 컴포저 위 진행 행의 버튼으로 일시정지·재개·편집·해제. 목표가 도는 동안 후속 메시지로 계속 조정 가능.

### Settings (데스크톱 앱 환경설정)
- URL: https://learn.chatgpt.com/codex/reference/settings · 원문: `codex__reference__settings.md`
- 열기: 앱 메뉴의 **Settings** 또는 macOS `Cmd+,` / Windows `Ctrl+,`

| 섹션 | 항목 |
|---|---|
| **General** | Require Cmd+Enter for multiline prompts / **Prevent sleep while running**(자리 비운 동안 로컬 채팅 계속) / **Follow-up behavior**(작업 중 보낸 메시지가 현재 실행을 조정할지 다음 실행을 기다릴지) |
| **Profile** | activity insights, lifetime tokens, peak tokens, streaks, longest task, token activity / 프로필 사진·표시명·사용자명 / 사용 하이라이트가 담긴 profile card 저장 (프로필 카드 공유는 **소비자 ChatGPT 플랜**에서 제공) / Codex 초대 — 적격 개인 플랜은 **Invite a friend**, 적격 Business 워크스페이스는 **Invite a coworker** |
| **Keyboard shortcuts** | 명령 검토, 바인딩 변경, 기본값 초기화. 명령 이름 검색 또는 키스트로크 검색 |
| **Notifications** | 턴 완료 알림 시점, 알림 권한 요청 여부 |
| **Appearance** | base theme, accent/background/foreground 색, UI 폰트·code 폰트, **커스텀 테마 공유** |
| **Pets** | 내장/커스텀 펫, `/pet`·Wake Pet·Tuck Away Pet |
| **Browser** | 번들 Browser 플러그인, Chrome 확장, 허용/차단 웹사이트 |
| **Computer Use** | 데스크톱 앱 접근 권한 검토 |
| **Personalization** | Default personality(Friendly/Pragmatic/None), **Custom instructions — `AGENTS.md`의 개인 지침을 갱신**, Suggested Prompts, Memories |
| **Archived Chats** | 보관 채팅 목록, Unarchive로 원래 위치 복원 |
| **Keep a chat near your work** | Chat pop-out window, Always on top |

- Claude Code 대응: **"Custom instructions가 `AGENTS.md`를 업데이트한다"** 가 핵심 — Claude Code의 `/memory` 편집이 `CLAUDE.md`를 고치는 것과 같은 구조. GUI 설정과 파일 기반 지침이 하나로 수렴한다.

### Troubleshooting
- URL: https://learn.chatgpt.com/codex/reference/troubleshooting · 원문: `codex__reference__troubleshooting.md`

| 증상 | 원인·해결 |
|---|---|
| Codex가 편집하지 않은 파일이 사이드 패널에 보임 | Git 저장소면 리뷰 패널이 **Git 상태** 기준으로 표시. staged/unstaged 전환·브랜치 비교 가능. Codex의 최근 변경만 보려면 diff 창의 **"Last turn"** 뷰 |
| 사이드바에서 프로젝트 제거 | 이름 위 점 3개 → **Remove**. 복원은 "Add new project" 또는 **Cmd+O** |
| 보관 채팅 찾기 | Settings에 있음. Unarchive하면 원래 사이드바 위치로 |
| 일부 채팅만 사이드바에 보임 | "Chats" 옆 필터 → **Chronological**. 그래도 없으면 Settings의 보관 채팅 확인 |
| 워크트리에서 코드가 안 돌아감 | 워크트리는 기본적으로 **Git 추적 파일만** 상속. 로컬 환경으로 셋업 스크립트를 돌리거나 **`.worktreeinclude`** 로 무시된 파일 복사 |
| 팀원의 공유 로컬 환경을 못 읽음 | 설정이 **프로젝트 루트의 `.codex` 폴더**에 있어야 함. 모노레포는 `.codex`가 있는 디렉터리를 프로젝트로 열 것 |
| Codex가 Apple Music 접근 요청 | 일부 macOS 디렉터리는 사용자 승인 필요. 홈 디렉터리 접근 시 macOS가 승인 요청 |
| 예약 작업이 워크트리를 많이 만듦 | 불필요한 예약 실행을 아카이브하고, 워크트리가 필요 없으면 실행을 pin하지 말 것 |
| 잘못된 대상 선택 후 프롬프트 복구 | 컴포저에서 **위 방향키** |
| CLI에선 되는데 앱에선 안 됨 | 표면마다 버전이 다를 수 있음. CLI: `codex --version` / 앱: `/Applications/Codex.app/Contents/Resources/codex --version` |

**로그·경로 (원문 그대로)**

| 대상 | 경로 |
|---|---|
| 앱 로그 (macOS) | `~/Library/Logs/com.openai.codex/YYYY/MM/DD` |
| 세션 트랜스크립트 | `$CODEX_HOME/sessions` (기본 `~/.codex/sessions`) |
| 보관된 세션 | `$CODEX_HOME/archived_sessions` (기본 `~/.codex/archived_sessions`) |

- 피드백·이슈: 컴포저에 `/` 입력 → 피드백. 기존 세션을 함께 공유하면 세션 ID 생성. 이슈: https://github.com/openai/codex/issues (기존 확인 후 https://github.com/openai/codex/issues/new)
- 막힘 복구: (1) 승인 대기 확인 (2) `git status` (3) 좁힌 프롬프트로 새 채팅. 취소 후 프롬프트 분실은 위 방향키.
- 터미널 멈춤: 패널 닫기 → **Ctrl+`** 로 재개 → `pwd`/`git status`. 계속되면 활성 채팅 완료 후 앱 재시작.
- 폰트: Settings의 **"Code font"**. 리뷰 창·터미널·코드 표시에 동일 적용.
- Claude Code 대응: `$CODEX_HOME/sessions` ↔ `~/.claude/projects/*/[uuid].jsonl`. **`.worktreeinclude`** 는 Claude Code에 대응물이 없는 워크트리 파일 승계 제어 장치.

---

## 3. 설정 (Configuration & Config File)

### Configuration (허브)
- URL: https://learn.chatgpt.com/codex/configuration · 원문: `codex__configuration.md`
- 기본값 설정·지속 컨텍스트 추가·개발 도구 커스터마이징의 진입 허브. "configuration shapes behavior across chats, repositories, and machines for both individuals and teams."
- 구조: **Personal settings**(General·Profile·Appearance·Voice·Configuration·Personalization·Keyboard shortcuts) / **Integrations**(MCP servers·Browser) / **Configuration options**(user config `config.toml`, approval policy, sandbox, network access, personality) / **5개 주제**(Customization · Config File · Agent Configuration · Extend · Windows)
- Claude Code 대응: Codex는 설정 축을 **config.toml(기본값) / AGENTS.md(지침) / rules(명령 허용 정책) / hooks(라이프사이클)** 4분할로 둔다. Claude Code는 `settings.json` + `CLAUDE.md` 2분할 — Codex의 `rules`가 Claude Code `settings.json`의 permissions allow/deny에 해당한다.

### Config basics
- URL: https://learn.chatgpt.com/codex/config-file/config-basic · 원문: `codex__config-file__config-basic.md`
- 저장 위치: 사용자 `~/.codex/config.toml`, 프로젝트 `.codex/config.toml`

**설정 우선순위 (원문 그대로, 높은 것부터)**
1. CLI flags and `--config` overrides
2. Project config files: `.codex/config.toml`, ordered from project root to current working directory (closest wins; trusted projects only)
3. Profile files selected with `--profile profile-name` (`~/.codex/profile-name.config.toml`)
4. User config: `~/.codex/config.toml`
5. System config (if present): `/etc/codex/config.toml` on Unix
6. Built-in defaults

**TOML 예시 (원문 그대로)**
```toml
model = "gpt-5.6"
```
```toml
approval_policy = "on-request"
```
```toml
sandbox_mode = "workspace-write"
```
```toml
[windows]
sandbox = "elevated"   # Recommended
# sandbox = "unelevated" # Fallback if admin permissions/setup are unavailable
```
```toml
web_search = "cached"  # default; serves results from the web search cache
# web_search = "indexed" # gate external web access through the search index
# web_search = "live"  # fetch the most recent data from the web (same as --search)
# web_search = "disabled"
```
```toml
model_reasoning_effort = "high"
```
```toml
personality = "friendly" # or "pragmatic" or "none"
```
```toml
[tui.keymap.global]
open_transcript = "ctrl-t"

[tui.keymap.composer]
submit = ["enter", "ctrl-m"]

[tui.keymap.chat]
interrupt_turn = "f12"
```
```toml
[shell_environment_policy]
include_only = ["PATH", "HOME"]
```
```toml
log_dir = "/absolute/path/to/codex-logs"
```

**`[features]` 표 (원문 그대로 — 2026-08 기준)**

| Key | Default | Maturity | Description |
|---|---|---|---|
| `apps` | true | Stable | Enable app (connector) integrations |
| `goals` | true | Stable | Enable persisted goals and automatic continuation |
| `hooks` | true | Stable | Enable lifecycle hooks from `hooks.json` or inline `[hooks]` |
| `fast_mode` | true | Stable | Enable Fast mode selection and the `service_tier = "fast"` path |
| `memories` | false | Experimental | Enable Memories feature |
| `multi_agent` | true | Stable | Enable subagent collaboration tools |
| `personality` | true | Stable | Enable personality selection controls |
| `remote_plugin` | true | Stable | Enable the remote plugin catalog |
| `shell_snapshot` | true | Stable | Snapshot shell environment to speed up repeated commands |
| `shell_tool` | true | Stable | Enable the default `shell` tool |
| `unified_exec` | `true` except Windows | Stable | Use the unified PTY-backed exec tool |
| `web_search` | true | Deprecated | Legacy toggle; prefer the top-level `web_search` setting |
| `web_search_cached` | false | Deprecated | Legacy toggle that maps to `web_search = "cached"` when unset |
| `web_search_request` | false | Deprecated | Legacy toggle that maps to `web_search = "live"` when unset |

- 관리형 제약 (원문): "On managed machines, your organization may also enforce constraints via `requirements.toml` (for example, disallowing `approval_policy = "never"` or `sandbox_mode = "danger-full-access"`)."
- **신뢰되지 않은 프로젝트는 프로젝트 스코프 레이어를 건너뛴다.**
- Claude Code 대응: 6단계 우선순위는 Claude Code의 settings 계층(enterprise managed → CLI args → `.claude/settings.local.json` → `.claude/settings.json` → `~/.claude/settings.json`)과 구조적으로 대응. `requirements.toml` ↔ managed-settings.json.

### Advanced configuration
- URL: https://learn.chatgpt.com/codex/config-file/config-advanced · 원문: `codex__config-file__config-advanced.md`
- 20개 주제: Profiles / One-off CLI Overrides / Config Locations / Project Config Files / Hooks / Custom Model Providers / Amazon Bedrock / OSS Mode / Azure Provider / Model Settings / Approval Policies & Sandbox / Shell Environment Policy / MCP Servers / Observability(OTel) / Notifications / History Persistence / Citations / Project Instructions / Desktop Options / TUI Options

**Profiles**
```toml
# ~/.codex/deep-review.config.toml
model = "gpt-5.5"
model_reasoning_effort = "xhigh"
approval_policy = "on-request"
model_catalog_json = "/Users/me/.codex/model-catalogs/deep-review.json"
```

**Hooks (인라인 TOML)**
```toml
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py"'
timeout = 30
statusMessage = "Checking Bash command"
```

**커스텀 모델 프로바이더**
```toml
model = "gpt-5.6-terra"
model_provider = "proxy"

[model_providers.proxy]
name = "OpenAI using LLM proxy"
base_url = "http://proxy.example.com"
env_key = "OPENAI_API_KEY"

[model_providers.local_ollama]
name = "Ollama"
base_url = "http://localhost:11434/v1"

[model_providers.mistral]
name = "Mistral"
base_url = "https://api.mistral.ai/v1"
env_key = "MISTRAL_API_KEY"
```

**헤더 / 명령 기반 인증**
```toml
[model_providers.example]
http_headers = { "X-Example-Header" = "example-value" }
env_http_headers = { "X-Example-Features" = "EXAMPLE_FEATURES" }
```
```toml
[model_providers.proxy]
name = "OpenAI using LLM proxy"
base_url = "https://proxy.example.com/v1"
wire_api = "responses"

[model_providers.proxy.auth]
command = "/usr/local/bin/fetch-codex-token"
args = ["--audience", "codex"]
timeout_ms = 5000
refresh_interval_ms = 300000
```

**Amazon Bedrock / OSS / Azure / 데이터 레지던시**
```toml
model_provider = "amazon-bedrock"
model = "<bedrock-model-id>"

[model_providers.amazon-bedrock.aws]
profile = "default"
region = "eu-central-1"
```
```toml
oss_provider = "ollama" # or "lmstudio"
```
```toml
[model_providers.azure]
name = "Azure"
base_url = "https://YOUR_PROJECT_NAME.openai.azure.com/openai"
env_key = "AZURE_OPENAI_API_KEY"
query_params = { api-version = "2025-04-01-preview" }
wire_api = "responses"
request_max_retries = 4
stream_max_retries = 10
stream_idle_timeout_ms = 300000
```
```toml
model_provider = "openaidr"
[model_providers.openaidr]
name = "OpenAI Data Residency"
base_url = "https://us.api.openai.com/v1"
```

**승인 정책 & 샌드박스**
```toml
approval_policy = "untrusted"
approvals_reviewer = "user"
sandbox_mode = "workspace-write"
allow_login_shell = false

[sandbox_workspace_write]
exclude_tmpdir_env_var = false
exclude_slash_tmp = false
writable_roots = ["/Users/YOU/.pyenv/shims"]
network_access = false

[auto_review]
policy = """
Use your organization's automatic review policy.
"""
```
```toml
approval_policy = { granular = {
  sandbox_approval = true,
  rules = true,
  mcp_elicitations = true,
  request_permissions = false,
  skill_approval = false
} }
```

**Shell 환경 정책 / OTel / 알림 / 히스토리 / TUI / 데스크톱 핸들러**
```toml
[shell_environment_policy]
inherit = "none"
set = { PATH = "/usr/bin", MY_FLAG = "1" }
ignore_default_excludes = false
exclude = ["AWS_*", "AZURE_*"]
include_only = ["PATH", "HOME"]
```
```toml
[otel]
environment = "staging"
exporter = "none"
log_user_prompt = false
```
```toml
[otel]
exporter = { otlp-http = {
  endpoint = "https://otel.example.com/v1/logs",
  protocol = "binary",
  headers = { "x-otlp-api-key" = "${OTLP_TOKEN}" }
}}
```
```toml
[otel]
exporter = { otlp-grpc = {
  endpoint = "https://otel.example.com:4317",
  headers = { "x-otlp-meta" = "abc123" }
}}
```
```toml
notify = ["python3", "/path/to/notify.py"]
```
```toml
[analytics]
enabled = false

[feedback]
enabled = false
```
```toml
hide_agent_reasoning = true
show_raw_agent_reasoning = true
```
```toml
[history]
persistence = "none"
max_bytes = 104857600 # 100 MiB
```
```toml
file_opener = "vscode" # or cursor, windsurf, vscode-insiders, none
```
```toml
[tui]
notifications = true
notification_method = "auto"
notification_condition = "unfocused"
animations = true
alternate_screen = "auto"
show_tooltips = true
```
```toml
[desktop.custom_file_handlers.vscodium]
label = "VSCodium"
icon = "/Users/you/.codex/icons/vscodium.png"
command = "codium"

[desktop.custom_file_handlers.textedit]
label = "TextEdit"
icon = "/Users/you/.codex/icons/textedit.png"
command = "/usr/bin/open"
args = ["-a", "TextEdit"]

[desktop.custom_file_handlers.company_editor]
label = "Company Editor"
icon = "/opt/company/editor/icon.png"
command = "/opt/company/bin/editor"
input = "json_argument"
```
- 알림 이벤트: `agent-turn-complete` 등이 외부 프로그램을 트리거.
- Claude Code 대응: `notify` ↔ Notification/Stop hook. `[shell_environment_policy]` ↔ `settings.json`의 `env` (Codex 쪽이 상속·제외·화이트리스트까지 세분화). `file_opener` ↔ 파일 경로 클릭 열기. `[otel]` ↔ Claude Code OTel 환경 변수.

### Environment variables (전수 9개, 원문 그대로)
- URL: https://learn.chatgpt.com/codex/config-file/environment-variables · 원문: `codex__config-file__environment-variables.md`

| Variable | Used by | Default | Description |
|---|---|---|---|
| `CODEX_HOME` | CLI, IDE extension, app-server, installers | `~/.codex` | Sets the root for Codex state, including config, auth, logs, sessions, skills, and standalone package metadata. Directory must already exist if set. |
| `CODEX_SQLITE_HOME` | CLI and app-server state | `CODEX_HOME` | Sets where SQLite-backed state is stored. The `sqlite_home` config option takes precedence. Relative paths resolve from current working directory. |
| `CODEX_NON_INTERACTIVE` | Installer scripts | `false` | Set to `1`, `true`, or `yes` to skip installer prompts, using defaults for scripted installs and updates. |
| `CODEX_INSTALL_DIR` | Installer scripts | `~/.local/bin` (macOS/Linux); `%LOCALAPPDATA%\Programs\OpenAI\Codex\bin` (Windows) | Changes where the visible `codex` command is installed. |
| `CODEX_API_KEY` | `codex exec` | (none) | Provides an API key for a single non-interactive run; only supported in `codex exec`. |
| `CODEX_ACCESS_TOKEN` | CLI, app-server, trusted automation | (none) | Provides a ChatGPT or Codex access token for trusted automation. |
| `CODEX_CA_CERTIFICATE` | HTTPS, login, and WebSocket clients | (none) | Points to a PEM CA bundle for corporate TLS interception or private root CAs; takes precedence over `SSL_CERT_FILE`. |
| `SSL_CERT_FILE` | HTTPS, login, and WebSocket clients | (none) | Fallback PEM CA bundle path when `CODEX_CA_CERTIFICATE` is unset. |
| `RUST_LOG` | CLI and app-server | `error` (for `codex exec`) | Controls Rust log filtering and verbosity; accepts `error`, `warn`, `info`, `debug`, `trace`, or targeted filters. |

- 다른 페이지 출처 환경 변수: `VISUAL`/`EDITOR`(프롬프트 에디터, cli-customization) · `PLUGIN_ROOT`/`PLUGIN_DATA` 및 호환용 `CLAUDE_PLUGIN_ROOT`/`CLAUDE_PLUGIN_DATA`(플러그인 훅, hooks) · `TMPDIR`(Chronicle 캡처 경로)
- Claude Code 대응: `CODEX_HOME` ↔ `CLAUDE_CONFIG_DIR`. `CODEX_API_KEY` ↔ `ANTHROPIC_API_KEY`. **설치 스크립트 전용 변수(`CODEX_NON_INTERACTIVE`·`CODEX_INSTALL_DIR`)를 공식 문서에 명시**한 점은 CI 자동화 관점에서 참고할 만하다.

### Sample config.toml (전문 1,125행)
- URL: https://learn.chatgpt.com/codex/config-file/config-sample · 원문: `codex__config-file__config-sample.md`
- 원문 도입부: "Use this example configuration as a starting point. It includes most keys Codex reads from `config.toml`, along with default behaviors, recommended values where helpful, and short notes."
- **아래는 원문 TOML 전문을 한 줄도 빠짐없이 옮긴 것이다 (주석 포함).**

```toml
# Codex example configuration (config.toml)
#
# This file lists the main keys Codex reads from config.toml, along with default
# behaviors, recommended examples, and concise explanations. Adjust as needed.
#
# Notes
# - Root keys must appear before tables in TOML.
# - Optional keys that default to "unset" are shown commented out with notes.
# - MCP servers, profile files, and model providers are examples; remove or edit.

################################################################################

# Core Model Selection

################################################################################

# Primary model used by Codex. Recommended example for most users: "gpt-5.6".

model = "gpt-5.6"

# Communication style for supported models. Allowed values: none | friendly | pragmatic

# personality = "pragmatic"

# Optional model override for /review. Default: unset (uses current session model).

# review_model = "gpt-5.6"

# Provider id selected from [model_providers]. Default: "openai".

model_provider = "openai"

# Default OSS provider for --oss sessions. When unset, Codex prompts. Default: unset.

# oss_provider = "ollama"

# Preferred service tier. Use fast or another tier supported by the active model.

# service_tier = "fast"

# Optional manual model metadata. When unset, Codex uses model or preset defaults.

# model_context_window = 128000 # tokens; default: auto for model

# model_auto_compact_token_limit = 64000 # tokens; unset uses model defaults

# model_auto_compact_token_limit_scope = "total" # total | body_after_prefix; default: total

# tool_output_token_limit = 12000 # tokens stored per tool output

# model_catalog_json = "/absolute/path/to/models.json" # optional startup-only model catalog override

# background_terminal_max_timeout = 300000 # ms; max empty write_stdin poll window (default 5m)

# log_dir = "/absolute/path/to/codex-logs" # log directory; setting explicitly enables codex-tui.log; default: "$CODEX_HOME/log"

# sqlite_home = "/absolute/path/to/codex-state" # optional SQLite-backed runtime state directory

################################################################################

# Reasoning & Verbosity (Responses API capable models)

################################################################################

# Reasoning effort: minimal | low | medium | high | xhigh

# model_reasoning_effort = "medium"

# Optional override used when Codex runs in plan mode: none | minimal | low | medium | high | xhigh

# plan_mode_reasoning_effort = "high"

# Reasoning summary: auto | concise | detailed | none

# model_reasoning_summary = "auto"

# Text verbosity for GPT-5 family (Responses API): low | medium | high

# model_verbosity = "medium"

# Force enable or disable reasoning summaries for current model.

# model_supports_reasoning_summaries = true

################################################################################

# Instruction Overrides

################################################################################

# Additional user instructions are injected before AGENTS.md. Default: unset.

# developer_instructions = ""

# Inline override for the history compaction prompt. Default: unset.

# compact_prompt = ""

# Override built-in base instructions with a file path. Default: unset.

# model_instructions_file = "/absolute/or/relative/path/to/instructions.txt"

# Load the compact prompt override from a file. Default: unset.

# experimental_compact_prompt_file = "/absolute/or/relative/path/to/compact_prompt.txt"

################################################################################

# Notifications

################################################################################

# External notifier program (argv array). When unset: disabled.

# notify = ["notify-send", "Codex"]

################################################################################

# Approval & Sandbox

################################################################################

# When to ask for command approval:

# - untrusted: only known-safe read-only commands auto-run; others prompt

# - on-request: model decides when to ask (default)

# - never: never prompt (risky)

# - { granular = { ... } }: allow or auto-reject selected prompt categories

approval_policy = "on-request"

# Who reviews eligible approval prompts: user (default) | auto_review

# approvals_reviewer = "user"

# Example granular policy:

# approval_policy = { granular = {

# sandbox_approval = true,

# rules = true,

# mcp_elicitations = true,

# request_permissions = false,

# skill_approval = false

# } }

# Allow login-shell semantics for shell-based tools when they request `login = true`.

# Default: true. Set false to force non-login shells and reject explicit login-shell requests.

allow_login_shell = true

# Filesystem/network sandbox policy for tool calls:

# - read-only (default)

# - workspace-write

# - danger-full-access (no sandbox; extremely risky)

sandbox_mode = "read-only"

# Named permissions profile to apply by default. Built-ins:

# :read-only | :workspace | :danger-full-access

# Use a custom name such as "workspace" only when you also define [permissions.workspace].

# default_permissions = ":workspace"

################################################################################

# Authentication & Login

################################################################################

# Where to persist CLI login credentials: file (default) | keyring | auto

cli_auth_credentials_store = "file"

# Base URL for ChatGPT auth flow (not OpenAI API).

chatgpt_base_url = "https://chatgpt.com/backend-api/"

# Optional base URL override for the built-in OpenAI provider.

# openai_base_url = "https://us.api.openai.com/v1"

# Restrict ChatGPT login to a specific workspace id. Default: unset.

# forced_chatgpt_workspace_id = "00000000-0000-0000-0000-000000000000"

# Force login mechanism when Codex would normally auto-select. Default: unset.

# Allowed values: chatgpt | api

# forced_login_method = "chatgpt"

# Preferred store for MCP OAuth credentials: auto (default) | file | keyring

mcp_oauth_credentials_store = "auto"

# Optional fixed port for MCP OAuth callback: 1-65535. Default: unset.

# mcp_oauth_callback_port = 4321

# Optional redirect URI override for MCP OAuth login (for example, remote devbox ingress).

# Codex appends a server-specific callback ID before OAuth login.

# Register the full derived URI with your provider, not just the base host or unsuffixed path.

# Custom callback paths are supported. `mcp_oauth_callback_port` still controls the listener port.

# mcp_oauth_callback_url = "https://devbox.example.internal/callback"

################################################################################

# Project Documentation Controls

################################################################################

# Max bytes from AGENTS.md to embed into first-turn instructions. Default: 32768

project_doc_max_bytes = 32768

# Ordered fallbacks when AGENTS.md is missing at a directory level. Default: []

project_doc_fallback_filenames = []

# Project root marker filenames used when searching parent directories. Default: [".git"]

# project_root_markers = [".git"]

################################################################################

# History & File Opener

################################################################################

# URI scheme for clickable citations: vscode (default) | vscode-insiders | windsurf | cursor | none

file_opener = "vscode"

################################################################################

# UI, Notifications, and Misc

################################################################################

# Suppress internal reasoning events from output. Default: false

hide_agent_reasoning = false

# Show raw reasoning content when available. Default: false

show_raw_agent_reasoning = false

# Disable burst-paste detection in the TUI. Default: false

disable_paste_burst = false

# Track Windows onboarding acknowledgement (Windows only). Default: false

windows_wsl_setup_acknowledged = false

# Check for updates on startup. Default: true

check_for_update_on_startup = true

################################################################################

# Web Search

################################################################################

# Web search mode: disabled | cached | indexed | live. Default: "cached"

# cached serves results from a web search cache (an OpenAI-maintained index).

# cached returns pre-indexed results; indexed gates external web access through

# the search index; live fetches the most recent data.

# If you use --yolo or another full access sandbox setting, web search defaults to live.

web_search = "cached"

# Config profiles are separate files under CODEX_HOME.

# Example: ~/.codex/ci.config.toml, selected with codex --profile ci.

# Suppress the warning shown when under-development feature flags are enabled.

# suppress_unstable_features_warning = true

################################################################################

# Agents (multi-agent roles and limits)

################################################################################

[agents]

# Enable or disable multi-agent tools. Default: true

# enabled = true

# Maximum concurrently open spawned-agent threads, excluding the primary thread. When unset, Codex chooses the default.

# max_concurrent_threads_per_session = 6

# Default model for spawned agents. An explicit spawn model takes precedence.

# default_subagent_model = "gpt-5.6-terra"

# Default reasoning effort for spawned agents. An explicit spawn effort takes precedence.

# default_subagent_reasoning_effort = "high"

# Record a model-visible message when an agent turn is interrupted. Default: true

# interrupt_message = true

# [agents.reviewer]

# description = "Find correctness, security, and test risks in code."

# config_file = "./agents/reviewer.toml" # relative to the config.toml that defines it

################################################################################

# Skills (per-skill overrides)

################################################################################

# Disable or re-enable a specific skill without deleting it.

[[skills.config]]

# path = "/path/to/skill/SKILL.md"

# enabled = false

################################################################################

# Sandbox settings (tables)

################################################################################

# Extra settings used only when sandbox_mode = "workspace-write".

[sandbox_workspace_write]

# Additional writable roots beyond the workspace (cwd). Default: []

writable_roots = []

# Allow outbound network access inside the sandbox. Default: false

network_access = false

# Exclude $TMPDIR from writable roots. Default: false

exclude_tmpdir_env_var = false

# Exclude /tmp from writable roots. Default: false

exclude_slash_tmp = false

################################################################################

# Shell Environment Policy for spawned processes (table)

################################################################################

[shell_environment_policy]

# inherit: all (default) | core | none

inherit = "all"

# Skip default excludes for names containing KEY/SECRET/TOKEN (case-insensitive). Default: false

ignore_default_excludes = false

# Case-insensitive glob patterns to remove (e.g., "AWS*\*", "AZURE*\*"). Default: []

exclude = []

# Explicit key/value overrides (always win). Default: {}

set = {}

# Whitelist; if non-empty, keep only matching vars. Default: []

include_only = []

# Experimental: run via user shell profile. Default: false

experimental_use_profile = false

################################################################################

# Sandboxed networking settings

################################################################################

# Enable the feature before configuring sandboxed networking rules.

# [features.network_proxy]

# enabled = true

# domains = { "api.openai.com" = "allow", "example.com" = "deny" }

#

# Exact hosts match only themselves.

# "\*.example.com" matches subdomains only; "\*\*.example.com" matches the apex plus subdomains.

# "\*" allows any public host that is not denied, so prefer scoped rules when possible.

# `allow_local_binding = false` blocks loopback and private destinations by default.

# Add an exact local IP literal or `localhost` allow rule for one target, or set it to true only when broader local access is required.

#

# Set `default_permissions = "workspace"` before enabling this profile.

# Example additional workspace roots that inherit this profile's

# `:workspace_roots` filesystem rules.

# [permissions.workspace.workspace_roots]

# "~/code/app" = true

# "~/code/shared-lib" = true

#

# Example filesystem profile. Use `"deny"` to deny reads for exact paths or

# glob patterns. On platforms that need pre-expanded glob matches, set

# glob_scan_max_depth when using unbounded patterns such as `\*\*`.

# [permissions.workspace.filesystem]

# glob_scan_max_depth = 3

# ":workspace_roots" = { "." = "write", "\*\*/\*.env" = "deny" }

# "/absolute/path/to/secrets" = "deny"

#

# [permissions.workspace.network]

# enabled = true

# proxy_url = "http://127.0.0.1:43128"

# admin_url = "http://127.0.0.1:43129"

# enable_socks5 = false

# socks_url = "http://127.0.0.1:43130"

# enable_socks5_udp = false

# allow_upstream_proxy = false

# dangerously_allow_non_loopback_proxy = false

# dangerously_allow_non_loopback_admin = false

# dangerously_allow_all_unix_sockets = false

# mode = "limited" # limited | full

# allow_local_binding = false

#

# [permissions.workspace.network.domains]

# "api.openai.com" = "allow"

# "example.com" = "deny"

#

# [permissions.workspace.network.unix_sockets]

# "/var/run/docker.sock" = "allow"

################################################################################

# History (table)

################################################################################

[history]

# save-all (default) | none

persistence = "save-all"

# Maximum bytes for history file; oldest entries are trimmed when exceeded. Example: 5242880

# max_bytes = 5242880

################################################################################

# UI, Notifications, and Misc (tables)

################################################################################

[tui]

# Desktop notifications from the TUI: boolean or filtered list. Default: true

# Examples: false | ["agent-turn-complete", "approval-requested"]

notifications = false

# Notification mechanism for terminal alerts: auto | osc9 | bel. Default: "auto"

# notification_method = "auto"

# When notifications fire: unfocused (default) | always

# notification_condition = "unfocused"

# Enables welcome/status/spinner animations. Default: true

animations = true

# Show onboarding tooltips in the welcome screen. Default: true

show_tooltips = true

# Control alternate screen usage (auto skips it in Zellij to preserve scrollback).

# alternate_screen = "auto"

# Working directory for resumed or forked sessions: current | session.

# Leave unset to choose when the current and saved session directories differ.

# resume_cwd = "session"

# Ordered list of footer status-line item IDs. When unset, Codex uses:

# ["model-with-reasoning", "context-remaining", "current-dir"].

# Set to [] to hide the footer.

# status_line = ["model", "context-remaining", "git-branch"]

# Ordered list of terminal window/tab title item IDs. When unset, Codex uses:

# ["spinner", "project"]. Set to [] to clear the title.

# Available IDs include app-name, project, spinner, status, thread, git-branch, model,

# and task-progress.

# terminal_title = ["spinner", "project"]

# Syntax-highlighting theme (kebab-case). Use /theme in the TUI to preview and save.

# You can also add custom .tmTheme files under $CODEX_HOME/themes.

# theme = "catppuccin-mocha"

# Custom key bindings. Selected composer actions fall back to matching [tui.keymap.global] bindings.

# Use [] to unbind an action.

# [tui.keymap.global]

# open_transcript = "ctrl-t"

# open_external_editor = []

#

# [tui.keymap.composer]

# submit = ["enter", "ctrl-m"]

# [tui.keymap.chat]

# interrupt_turn = "f12"

# Internal tooltip state keyed by model slug. Usually managed by Codex.

# [tui.model_availability_nux]

# "gpt-5.6-terra" = 1

# Enable or disable analytics for this machine. When unset, Codex uses its default behavior.

[analytics]
enabled = true

# Control whether users can submit feedback from `/feedback`. Default: true

[feedback]
enabled = true

# In-product notices (mostly set automatically by Codex).

[notice]

# hide_full_access_warning = true

# hide_world_writable_warning = true

# hide_rate_limit_model_nudge = true

# hide_gpt5_1_migration_prompt = true

# "hide_gpt-5.1-codex-max_migration_prompt" = true

# model_migrations = { "gpt-5.4" = "gpt-5.6-terra" }

################################################################################

# Centralized Feature Flags (preferred)

################################################################################

[features]

# Leave this table empty to accept defaults. Set explicit booleans to opt in/out.

# shell_tool = true

# apps = true

# hooks = false

# unified_exec = true

# shell_snapshot = true

# multi_agent = true

# remote_plugin = true

# personality = true

# network_proxy = false

# fast_mode = true

# enable_request_compression = true

# skill_mcp_dependency_install = true

# prevent_idle_sleep = false

# Code mode namespaces. This feature is under development and off by default.

# [features.code_mode]

# enabled = true

# excluded_tool_namespaces = ["mcp__codex_apps"]

# direct_only_tool_namespaces = ["mcp__history"]

# Rollout budget tracking. This feature is under development and off by default.

# limit_tokens is required when enabled.

# Optional reminder_interval_tokens defaults to 10% of limit_tokens.

# Token weights default to 1.0.

# [features.rollout_budget]

# enabled = true

# limit_tokens = 100000

# reminder_interval_tokens = 10000

# sampling_token_weight = 1.0

# prefill_token_weight = 1.0

################################################################################

# Memories (table)

################################################################################

# Enable memories with [features].memories, then tune memory behavior here.

# [memories]

# generate_memories = true

# use_memories = true

# disable_on_external_context = false # legacy alias: no_memories_if_mcp_or_web_search

################################################################################

# Lifecycle hooks can be configured here inline or in a sibling hooks.json.

################################################################################

# [hooks]

# [[hooks.PreToolUse]]

# matcher = "^Bash$"

#

# [[hooks.PreToolUse.hooks]]

# type = "command"

# command = 'python3 "/absolute/path/to/pre_tool_use_policy.py"'

# timeout = 30

# statusMessage = "Checking Bash command"

################################################################################

# Define MCP servers under this table. Leave empty to disable.

################################################################################

[mcp_servers]

# --- Example: STDIO transport ---

# [mcp_servers.docs]

# enabled = true # optional; default true

# required = true # optional; fail startup/resume if this server cannot initialize

# command = "docs-server" # required

# args = ["--port", "4000"] # optional

# env = { "API_KEY" = "value" } # optional key/value pairs copied as-is

# env_vars = ["ANOTHER_SECRET"] # optional: forward local parent env vars

# env_vars = ["LOCAL_TOKEN", { name = "REMOTE_TOKEN", source = "remote" }]

# cwd = "/path/to/server" # optional working directory override

# experimental_environment = "remote" # experimental: run stdio via a remote executor

# startup_timeout_sec = 10.0 # optional; default 10.0 seconds

# # startup_timeout_ms = 10000 # optional alias for startup timeout (milliseconds)

# tool_timeout_sec = 60.0 # optional; default 60.0 seconds

# enabled_tools = ["search", "summarize"] # optional allow-list

# disabled_tools = ["slow-tool"] # optional deny-list (applied after allow-list)

# scopes = ["read:docs"] # optional OAuth scopes

# oauth_resource = "https://docs.example.com/" # optional OAuth resource

# --- Example: Streamable HTTP transport ---

# [mcp_servers.github]

# enabled = true # optional; default true

# required = true # optional; fail startup/resume if this server cannot initialize

# url = "https://github-mcp.example.com/mcp" # required

# bearer_token_env_var = "GITHUB_TOKEN" # optional; Authorization: Bearer <token>

# http_headers = { "X-Example" = "value" } # optional static headers

# env_http_headers = { "X-Auth" = "AUTH_ENV" } # optional headers populated from env vars

# startup_timeout_sec = 10.0 # optional

# tool_timeout_sec = 60.0 # optional

# enabled_tools = ["list_issues"] # optional allow-list

# disabled_tools = ["delete_issue"] # optional deny-list

# scopes = ["repo"] # optional OAuth scopes

################################################################################

# Model Providers

################################################################################

# Built-ins include:

# - openai

# - ollama

# - lmstudio

# - amazon-bedrock

# These IDs are reserved. Use a different ID for custom providers.

[model_providers]

# --- Example: built-in Amazon Bedrock provider options ---

# model_provider = "amazon-bedrock"

# model = "<bedrock-model-id>"

# [model_providers.amazon-bedrock.aws]

# profile = "default"

# region = "eu-central-1"

# --- Example: OpenAI data residency with explicit base URL or headers ---

# [model_providers.openaidr]

# name = "OpenAI Data Residency"

# base_url = "https://us.api.openai.com/v1" # example with 'us' domain prefix

# wire_api = "responses" # only supported value

# # requires_openai_auth = true # use only for providers backed by OpenAI auth

# # request_max_retries = 4 # default 4; max 100

# # stream_max_retries = 5 # default 5; max 100

# # stream_idle_timeout_ms = 300000 # default 300_000 (5m)

# # supports_websockets = true # optional

# # experimental_bearer_token = "sk-example" # optional dev-only direct bearer token

# # http_headers = { "X-Example" = "value" }

# # env_http_headers = { "OpenAI-Organization" = "OPENAI_ORGANIZATION", "OpenAI-Project" = "OPENAI_PROJECT" }

# --- Example: Azure/OpenAI-compatible provider ---

# [model_providers.azure]

# name = "Azure"

# base_url = "https://YOUR_PROJECT_NAME.openai.azure.com/openai"

# wire_api = "responses"

# query_params = { api-version = "2025-04-01-preview" }

# env_key = "AZURE_OPENAI_API_KEY"

# env_key_instructions = "Set AZURE_OPENAI_API_KEY in your environment"

# # supports_websockets = false

# --- Example: command-backed bearer token auth ---

# [model_providers.proxy]

# name = "OpenAI using LLM proxy"

# base_url = "https://proxy.example.com/v1"

# wire_api = "responses"

#

# [model_providers.proxy.auth]

# command = "/usr/local/bin/fetch-codex-token"

# args = ["--audience", "codex"]

# timeout_ms = 5000

# refresh_interval_ms = 300000

# --- Example: Local OSS (e.g., Ollama-compatible) ---

# [model_providers.local_ollama]

# name = "Ollama"

# base_url = "http://localhost:11434/v1"

# wire_api = "responses"

################################################################################

# Apps / Connectors

################################################################################

# Optional per-app controls.

[apps]

# [_default] applies to all apps unless overridden per app.

# [apps._default]

# enabled = true

# destructive_enabled = true

# open_world_enabled = true

# approvals_reviewer = "user" # user | auto_review

# default_tools_approval_mode = "auto" # auto | prompt | writes | approve

#

# [apps.google_drive]

# enabled = false

# destructive_enabled = false # block destructive-hint tools for this app

# default_tools_enabled = true

# approvals_reviewer = "auto_review"

# default_tools_approval_mode = "prompt" # auto | prompt | writes | approve

#

# [apps.google_drive.tools."files/delete"]

# enabled = false

# approval_mode = "approve"

# Optional tool suggestion allowlist for connectors or plugins Codex can offer to install.

# [tool_suggest]

# discoverables = [

# { type = "connector", id = "gmail" },

# { type = "plugin", id = "figma@openai-curated" },

# ]

# disabled_tools = [

# { type = "plugin", id = "slack@openai-curated" },

# { type = "connector", id = "connector_googlecalendar" },

# ]

################################################################################

# Config Profiles (separate files)

################################################################################

# To create a config profile, put overrides in a separate profile file under $CODEX_HOME.

# Select it with codex --profile ci.

# For example, a CI profile could live at $CODEX_HOME/ci.config.toml:

# model = "gpt-5.6-terra"

# approval_policy = "on-request"

# sandbox_mode = "read-only"

# service_tier = "fast" # or another supported service tier id

# oss_provider = "ollama"

# model_reasoning_effort = "medium"

# plan_mode_reasoning_effort = "high"

# model_reasoning_summary = "auto"

# model_verbosity = "medium"

# personality = "pragmatic" # or "friendly" or "none"

# chatgpt_base_url = "https://chatgpt.com/backend-api/"

# model_catalog_json = "./models.json"

# model_instructions_file = "/absolute/or/relative/path/to/instructions.txt"

# experimental_compact_prompt_file = "./compact_prompt.txt"

# tools_view_image = true

# features = { unified_exec = false }

################################################################################

# Projects (trust levels)

################################################################################

[projects]

# Mark specific worktrees as trusted or untrusted.

# [projects."/absolute/path/to/project"]

# trust_level = "trusted" # or "untrusted"

################################################################################

# Tools

################################################################################

[tools]

# view_image = true

################################################################################

# OpenTelemetry (OTEL) - disabled by default

################################################################################

[otel]

# Include user prompt text in logs. Default: false

log_user_prompt = false

# Environment label applied to telemetry. Default: "dev"

environment = "dev"

# Exporter: none (default) | otlp-http | otlp-grpc

exporter = "none"

# Trace exporter: none (default) | otlp-http | otlp-grpc

trace_exporter = "none"

# Metrics exporter: none | statsig | otlp-http | otlp-grpc

metrics_exporter = "statsig"

# Example OTLP/HTTP exporter configuration

# [otel.exporter."otlp-http"]

# endpoint = "https://otel.example.com/v1/logs"

# protocol = "binary" # "binary" | "json"

# [otel.exporter."otlp-http".headers]

# "x-otlp-api-key" = "${OTLP_TOKEN}"

# [otel.exporter."otlp-http".tls]

# ca-certificate = "certs/otel-ca.pem"

# client-certificate = "/etc/codex/certs/client.pem"

# client-private-key = "/etc/codex/certs/client-key.pem"

# Example OTLP/gRPC trace exporter configuration

# [otel.trace_exporter."otlp-grpc"]

# endpoint = "https://otel.example.com:4317"

# headers = { "x-otlp-meta" = "abc123" }

################################################################################

# Windows

################################################################################

[windows]

# Native Windows sandbox mode (Windows only): unelevated | elevated

sandbox = "unelevated"
```

**config-sample에서 확정되는 기본값 (fact-checker 대조용)**

| 항목 | 값 |
|---|---|
| 권장 기본 모델 | `gpt-5.6` |
| `approval_policy` 기본 | `on-request` (모델이 물을 시점을 판단) |
| `sandbox_mode` 기본 | `read-only` |
| `web_search` 기본 | `cached` (`--yolo` 등 full access 시 `live`) |
| `project_doc_max_bytes` 기본 | `32768` (32 KiB) |
| `project_root_markers` 기본 | `[".git"]` |
| `file_opener` 기본 | `vscode` (vscode-insiders \| windsurf \| cursor \| none) |
| `history.persistence` 기본 | `save-all` |
| `cli_auth_credentials_store` 기본 | `file` (keyring \| auto) |
| `mcp_oauth_credentials_store` 기본 | `auto` |
| MCP `startup_timeout_sec` 기본 | `10.0`초 |
| MCP `tool_timeout_sec` 기본 | `60.0`초 |
| `background_terminal_max_timeout` 기본 | 300000 ms (5분) |
| `request_max_retries` 기본 | 4 (최대 100) |
| `stream_max_retries` 기본 | 5 (최대 100) |
| `stream_idle_timeout_ms` 기본 | 300000 (5분) |
| `otel.metrics_exporter` 기본 | `statsig` |
| `otel.environment` 기본 | `dev` |
| `shell_environment_policy.inherit` 기본 | `all` (core \| none) |
| 내장 model provider ID (예약) | `openai`, `ollama`, `lmstudio`, `amazon-bedrock` |
| 내장 permissions 프로필 | `:read-only`, `:workspace`, `:danger-full-access` |
| 기본 상태라인 항목 | `["model-with-reasoning", "context-remaining", "current-dir"]` |
| 기본 터미널 타이틀 항목 | `["spinner", "project"]` |
| `model_reasoning_effort` 값 | minimal \| low \| medium \| high \| xhigh |
| `model_reasoning_summary` 값 | auto \| concise \| detailed \| none |
| `model_verbosity` 값 | low \| medium \| high |
| `personality` 값 | none \| friendly \| pragmatic |
| `windows.sandbox` 값 | unelevated \| elevated |

- Claude Code 대응: `project_doc_max_bytes = 32768`은 Claude Code가 `CLAUDE.md`를 무제한 로드하는 것과 대비되는 **명시적 지침 예산**. `[projects."<path>"].trust_level`은 Claude Code의 폴더 신뢰 프롬프트를 파일로 고정한 형태. **`[features.rollout_budget]`(토큰 예산 + 리마인더 간격)** 은 Claude Code에 대응물이 없는 에이전트 토큰 예산 추적 기능.

---

### Configuration Reference — 설정 키 전수 원장
- URL: https://learn.chatgpt.com/codex/config-file/config-reference · 원문: `codex__config-file__config-reference.md`
- 공식 JSON 스키마: https://learn.chatgpt.com/docs/config-schema.json
- **수록 범위: `config.toml` 274키 + `requirements.toml` 116키 = 390키 전수.** 원문 페이지의 `ConfigTable` 2개를 파싱해 마크다운 표로 복원했다 (자리표시자 2개 = 복원 표 2개, 인라인 항목 390개 = 표 행 390개, 1:1 검증 완료).

**프로젝트 스코프 config가 오버라이드할 수 없는 키 (원문 인용)**
> "Project-scoped config can't override machine-local provider, auth, host-owned app request metadata, notification, configuration profile selection, or telemetry routing keys. Codex ignores `openai_base_url`, `chatgpt_base_url`, `apps_mcp_product_sku`, `model_provider`, `model_providers`, `notify`, `profile`, `profiles`, `experimental_realtime_ws_base_url`, and `otel` when they appear in a project-local `.codex/config.toml`; put provider, notification, and telemetry keys in user-level config instead."

**`requirements.toml` 개요 (원문 요지)**
- 관리자가 강제하는 설정 파일로, 사용자가 오버라이드할 수 없는 보안 민감 설정을 제약한다.
- ChatGPT Business·Enterprise는 **클라우드에서 가져온 requirements**도 적용될 수 있다.
- `[features]`로 런타임 feature flag를 `config.toml`과 같은 canonical key로 고정한다. **생략된 키는 제약되지 않은 채 남는다.**
- 일부 관리 요구사항은 허용목록이 아니라 **정확한 값을 강제**한다 — 강제된 경로, 업데이트 선호, login-shell 정책, 피드백 설정, Windows private-desktop 설정은 사용자가 오버라이드할 수 없다.
- **관리형 permission-profile 허용목록은 Codex 0.138.0 이상 필요.** 0.137.0 이하는 `allowed_permission_profiles`와 관리형 `default_permissions`를 무시한다.
- `allowed_sandbox_modes`는 `sandbox_mode`와 함께 쓴다. permission-profile 배포에는 `allowed_permission_profiles`를 관리형 `default_permissions`와 함께 쓴다.
- `[models.new_thread]` 테이블은 **강제가 아니라 관리형 기본값**이다. 전용 CLI 플래그나 `--config` 오버라이드의 명시적 실행 선택이 우선한다. 명시적 모델·추론강도 오버라이드는 두 관리형 모델 필드를 모두 건너뛴다. `service_tier`는 독립적이다.

#### `config.toml` 설정 키 전수 (274개)

| Key | Type | Description |
|---|---|---|
| `model` | string | Model to use (e.g., `gpt-5.5`). |
| `review_model` | string | Optional model override used by `/review` (defaults to the current session model). |
| `model_provider` | string | Provider id from `model_providers` (default: `openai`). |
| `openai_base_url` | string | Base URL override for the built-in `openai` model provider. |
| `model_context_window` | number | Context window tokens available to the active model. |
| `model_auto_compact_token_limit` | number | Token threshold that triggers automatic history compaction (unset uses model defaults). |
| `model_auto_compact_token_limit_scope` | total \| body_after_prefix | Controls whether the auto-compaction threshold counts the full active context (`total`, the default) or only growth after the carried compaction-window prefix (`body_after_prefix`). |
| `model_catalog_json` | string (path) | Optional path to a JSON model catalog loaded on startup. A selected `$CODEX_HOME/profile-name.config.toml` profile file can override this per profile. |
| `oss_provider` | lmstudio \| ollama | Default local provider used when running with `--oss` (defaults to prompting if unset). |
| `approval_policy` | untrusted \| on-request \| never \| { granular = { sandbox_approval = bool, rules = bool, mcp_elicitations = bool, request_permissions = bool, skill_approval = bool } } | Controls when Codex pauses for approval before executing commands. You can also use `approval_policy = { granular = { ... } }` to allow or auto-reject specific prompt categories while keeping other prompts interactive. `on-failure` is deprecated; use `on-request` for interactive runs or `never` for non-interactive runs. |
| `approval_policy.granular.sandbox_approval` | boolean | When `true`, sandbox escalation approval prompts are allowed to surface. |
| `approval_policy.granular.rules` | boolean | When `true`, approvals triggered by execpolicy `prompt` rules are allowed to surface. |
| `approval_policy.granular.mcp_elicitations` | boolean | When `true`, MCP elicitation prompts are allowed to surface instead of being auto-rejected. |
| `approval_policy.granular.request_permissions` | boolean | When `true`, prompts from the `request_permissions` tool are allowed to surface. |
| `approval_policy.granular.skill_approval` | boolean | When `true`, skill-script approval prompts are allowed to surface. |
| `approvals_reviewer` | user \| auto_review | Who reviews eligible approval prompts under `on-request` or granular approval policies. Defaults to `user`; `auto_review` uses the reviewer subagent. This setting doesn't change sandboxing or review actions already allowed inside the sandbox. |
| `auto_review.policy` | string | Local Markdown policy instructions for automatic review. Managed `guardian_policy_config` takes precedence. Blank values are ignored. |
| `allow_login_shell` | boolean | Allow shell-based tools to use login-shell semantics. Defaults to `true`; when `false`, `login = true` requests are rejected and omitted `login` defaults to non-login shells. |
| `sandbox_mode` | read-only \| workspace-write \| danger-full-access | Sandbox policy for filesystem and network access during command execution. |
| `sandbox_workspace_write.writable_roots` | array<string> | 'Additional writable roots when `sandbox_mode = "workspace-write"`.' |
| `sandbox_workspace_write.network_access` | boolean | Allow outbound network access inside the workspace-write sandbox. |
| `sandbox_workspace_write.exclude_tmpdir_env_var` | boolean | Exclude `$TMPDIR` from writable roots in workspace-write mode. |
| `sandbox_workspace_write.exclude_slash_tmp` | boolean | Exclude `/tmp` from writable roots in workspace-write mode. |
| `windows.sandbox` | unelevated \| elevated | Windows-only native sandbox mode when running Codex natively on Windows. |
| `windows.sandbox_private_desktop` | boolean | Run the final sandboxed child process on a private desktop by default on native Windows. Set `false` only for compatibility with the older `Winsta0\\\\Default` behavior. |
| `computer_use.windows.always_allowed_app_ids` | array<string> | Windows app identifiers that Computer Use can open without prompting. Apps not in the list require approval; remove saved entries from the ChatGPT desktop app's Computer Use settings. |
| `notify` | array<string> | Command invoked for notifications; receives a JSON payload from Codex. |
| `check_for_update_on_startup` | boolean | Check for Codex updates on startup (set to false only when updates are centrally managed). |
| `feedback.enabled` | boolean | Enable feedback submission via `/feedback` across local clients (default: true). |
| `analytics.enabled` | boolean | Enable or disable analytics for this machine/profile. When unset, the client default applies. |
| `instructions` | string | Reserved for future use; prefer `model_instructions_file` or `AGENTS.md`. |
| `developer_instructions` | string | Additional developer instructions injected into the session (optional). |
| `log_dir` | string (path) | Directory where Codex writes log files; defaults to `$CODEX_HOME/log`. Setting this explicitly also enables the opt-in plaintext TUI log, `codex-tui.log`, in that directory. |
| `sqlite_home` | string (path) | Directory where Codex stores the SQLite-backed state DB used by agent jobs and other resumable runtime state. |
| `compact_prompt` | string | Inline override for the history compaction prompt. |
| `model_instructions_file` | string (path) | Replacement for built-in instructions instead of `AGENTS.md`. |
| `personality` | none \| friendly \| pragmatic | Default communication style for models that advertise `supportsPersonality`; can be overridden per thread/turn or via `/personality`. |
| `service_tier` | string | Preferred service tier for new turns. Use `fast` or another tier advertised by the active model; `fast` maps to the request value `priority`. |
| `experimental_compact_prompt_file` | string (path) | Load the compaction prompt override from a file (experimental). |
| `skills.config` | array<object> | Per-skill enablement overrides stored in config.toml. |
| `skills.config.<index>.path` | string (path) | Path to a skill folder containing `SKILL.md`. |
| `skills.config.<index>.enabled` | boolean | Enable or disable the referenced skill. |
| `apps.<id>.enabled` | boolean | Enable or disable a specific app/connector by id (default: true). |
| `apps._default.enabled` | boolean | Default app enabled state for all apps unless overridden per app. |
| `apps._default.destructive_enabled` | boolean | Default allow/deny for app tools with `destructive_hint = true`. |
| `apps._default.open_world_enabled` | boolean | Default allow/deny for app tools with `open_world_hint = true`. |
| `apps._default.approvals_reviewer` | user \| auto_review | Default reviewer for app tool approval prompts unless overridden per app. When omitted, apps inherit the top-level `approvals_reviewer` value. |
| `apps._default.default_tools_approval_mode` | auto \| prompt \| writes \| approve | Default approval behavior for app tools without per-app or per-tool overrides. |
| `apps.<id>.destructive_enabled` | boolean | Allow or block tools in this app that advertise `destructive_hint = true`. |
| `apps.<id>.open_world_enabled` | boolean | Allow or block tools in this app that advertise `open_world_hint = true`. |
| `apps.<id>.default_tools_enabled` | boolean | Default enabled state for tools in this app unless a per-tool override exists. |
| `apps.<id>.approvals_reviewer` | user \| auto_review | Reviewer for this app's tool approval prompts. Overrides `apps._default.approvals_reviewer`. |
| `apps.<id>.default_tools_approval_mode` | auto \| prompt \| writes \| approve | Default approval behavior for tools in this app unless a per-tool override exists. |
| `apps.<id>.tools.<tool>.enabled` | boolean | Per-tool enabled override for an app tool (for example `repos/list`). |
| `apps.<id>.tools.<tool>.approval_mode` | auto \| prompt \| writes \| approve | Per-tool approval behavior override for a single app tool. |
| `tool_suggest.discoverables` | array<table> | 'Allow tool suggestions for additional discoverable connectors or plugins. Each entry uses `type = "connector"` or `"plugin"` and an `id`.' |
| `tool_suggest.disabled_tools` | array<table> | 'Disable suggestions for specific discoverable connectors or plugins. Each entry uses `type = "connector"` or `"plugin"` and an `id`.' |
| `features.apps` | boolean | Enable app (connector) integrations (stable; on by default). |
| `features.hooks` | boolean | Enable lifecycle hooks loaded from `hooks.json` or inline `[hooks]` config. `features.codex_hooks` is a deprecated alias. |
| `features.code_mode.enabled` | boolean | Enable code mode feature configuration. This feature is under development and off by default. |
| `features.code_mode.excluded_tool_namespaces` | array<string> | Tool namespaces code mode excludes from nested code-mode tool guidance and executor exposure. |
| `features.code_mode.direct_only_tool_namespaces` | array<string> | Tool namespaces code mode can use only through direct tool calls. |
| `features.rollout_budget.enabled` | boolean | Enable rollout budget tracking. This feature is under development and off by default. When enabled, `features.rollout_budget.limit_tokens` is required. |
| `features.rollout_budget.limit_tokens` | integer | Positive token limit for rollout budget tracking. Required when rollout budget is enabled. |
| `features.rollout_budget.reminder_interval_tokens` | integer | Positive token interval between rollout budget reminders. Defaults to 10% of `limit_tokens`, with a minimum of 1 token. |
| `features.rollout_budget.sampling_token_weight` | number | Finite non-negative multiplier for sampled tokens in rollout budget accounting. Defaults to `1.0`. |
| `features.rollout_budget.prefill_token_weight` | number | Finite non-negative multiplier for prefill tokens in rollout budget accounting. Defaults to `1.0`. |
| `hooks` | table | Lifecycle hooks configured inline in `config.toml`. Uses the same event schema as `hooks.json`; see the Hooks guide for examples and supported events. |
| `hooks.<Event>` | array<table> | Matcher groups for hook events such as `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, or `Stop`. |
| `hooks.<Event>[].hooks` | array<table> | Hook handlers for a matcher group. Command hooks are currently supported; prompt and agent hook handlers are parsed but skipped. |
| `hooks.<Event>[].hooks[].additionalContextLimit` | integer | Approximate per-handler token threshold for saving oversized `additionalContext` to disk and showing the model a shorter preview. Defaults to `2500`; `0` passes the full context directly to the model. See [Large hook output](https://learn.chatgpt.com/docs/hooks#large-hook-output). |
| `hooks.<Event>[].hooks[].commandWindows` | string | Windows-only command override for command hooks. The TOML alias `command_windows` is also accepted. |
| `features.memories` | boolean | Enable [Memories](https://learn.chatgpt.com/docs/customization/memories) (off by default). |
| `mcp_servers.<id>.command` | string | Launcher command for an MCP stdio server. |
| `mcp_servers.<id>.args` | array<string> | Arguments passed to the MCP stdio server command. |
| `mcp_servers.<id>.env` | map<string,string> | Environment variables forwarded to the MCP stdio server. |
| `mcp_servers.<id>.env_vars` | 'array<string \| { name = string, source = "local" \| "remote" }>' | 'Additional environment variables to whitelist for an MCP stdio server. String entries default to `source = "local"`; use `source = "remote"` only with executor-backed remote stdio.' |
| `mcp_servers.<id>.cwd` | string | Working directory for the MCP stdio server process. |
| `mcp_servers.<id>.url` | string | Endpoint for an MCP streamable HTTP server. |
| `mcp_servers.<id>.auth` | oauth \| chatgpt | Authentication fallback for an MCP HTTP server after configured bearer tokens and authorization headers. `oauth` (default) uses stored MCP OAuth credentials when available. `chatgpt` uses the current ChatGPT session for the trusted first-party ChatGPT origin, then falls back to stored OAuth. Both modes can connect without authentication if no credential source resolves. |
| `mcp_servers.<id>.bearer_token_env_var` | string | Environment variable sourcing the bearer token for an MCP HTTP server. |
| `mcp_servers.<id>.http_headers` | map<string,string> | Static HTTP headers included with each MCP HTTP request. |
| `mcp_servers.<id>.env_http_headers` | map<string,string> | HTTP headers populated from environment variables for an MCP HTTP server. |
| `mcp_servers.<id>.enabled` | boolean | Disable an MCP server without removing its configuration. |
| `mcp_servers.<id>.required` | boolean | When true, fail startup/resume if this enabled MCP server cannot initialize. |
| `mcp_servers.<id>.startup_timeout_sec` | number | Override the default 10s startup timeout for an MCP server. |
| `mcp_servers.<id>.startup_timeout_ms` | number | Alias for `startup_timeout_sec` in milliseconds. |
| `mcp_servers.<id>.tool_timeout_sec` | number | Override the default 60s per-tool timeout for an MCP server. |
| `mcp_servers.<id>.enabled_tools` | array<string> | Allow list of tool names exposed by the MCP server. |
| `mcp_servers.<id>.disabled_tools` | array<string> | Deny list applied after `enabled_tools` for the MCP server. |
| `mcp_servers.<id>.default_tools_approval_mode` | auto \| prompt \| writes \| approve | Default approval behavior for MCP tools on this server unless a per-tool override exists. |
| `mcp_servers.<id>.tools.<tool>.approval_mode` | auto \| prompt \| writes \| approve | Per-tool approval behavior override for one MCP tool on this server. |
| `mcp_servers.<id>.scopes` | array<string> | OAuth scopes to request when authenticating to that MCP server. |
| `mcp_servers.<id>.oauth_resource` | string | Optional RFC 8707 OAuth resource parameter to include during MCP login. |
| `mcp_servers.<id>.experimental_environment` | local \| remote | Experimental placement for an MCP server. `remote` starts stdio servers through a remote executor environment; streamable HTTP remote placement is not implemented. |
| `agents` | table | Multi-agent settings and custom role declarations. Scalar setting names are reserved and can't be used as custom role names. |
| `agents.enabled` | boolean | Enable or disable multi-agent tools (default: true). |
| `agents.max_concurrent_threads_per_session` | number | Maximum number of spawned-agent threads that can be open concurrently, excluding the primary thread. When unset, Codex chooses the default. |
| `agents.max_threads` | number | Legacy alias for `agents.max_concurrent_threads_per_session`. |
| `agents.default_subagent_model` | string | Default model for spawned agents. An explicit spawn model takes precedence. |
| `agents.default_subagent_reasoning_effort` | string | Default reasoning effort for spawned agents. An explicit spawn effort takes precedence. |
| `agents.interrupt_message` | boolean | Record a model-visible message when an agent turn is interrupted (default: true). |
| `agents.<name>.description` | string | Role guidance shown to Codex when choosing and spawning that agent type. |
| `agents.<name>.config_file` | string (path) | Path to a TOML config layer for that role; relative paths resolve from the config file that declares the role. |
| `memories.generate_memories` | boolean | When `false`, newly created threads are not stored as memory-generation inputs. Defaults to `true`. |
| `memories.use_memories` | boolean | When `false`, Codex skips injecting existing memories into future sessions. Defaults to `true`. |
| `memories.disable_on_external_context` | boolean | When `true`, threads that use external context such as MCP tool calls, web search, or tool search are kept out of memory generation. Defaults to `false`. Legacy alias: `memories.no_memories_if_mcp_or_web_search`. |
| `memories.max_raw_memories_for_consolidation` | number | Maximum recent raw memories retained for global consolidation. Defaults to `256` and is capped at `4096`. |
| `memories.max_unused_days` | number | Maximum days since a memory was last used before it becomes ineligible for consolidation. Defaults to `30` and is clamped to `0`-`365`. |
| `memories.max_rollout_age_days` | number | Maximum age of threads considered for memory generation. Defaults to `30` and is clamped to `0`-`90`. |
| `memories.max_rollouts_per_startup` | number | Maximum rollout candidates processed per startup pass. Defaults to `16` and is capped at `128`. |
| `memories.min_rollout_idle_hours` | number | Minimum idle time before a thread is considered for memory generation. Defaults to `6` and is clamped to `1`-`48`. |
| `memories.min_rate_limit_remaining_percent` | number | Minimum remaining percentage required in Codex rate-limit windows before memory generation starts. Defaults to `25` and is clamped to `0`-`100`. |
| `memories.extract_model` | string | Optional model override for per-thread memory extraction. |
| `memories.consolidation_model` | string | Optional model override for global memory consolidation. |
| `features.unified_exec` | boolean | Use the unified PTY-backed exec tool (stable; enabled by default except on Windows). |
| `features.shell_snapshot` | boolean | Snapshot shell environment to speed up repeated commands (stable; on by default). |
| `features.multi_agent` | boolean | Enable multi-agent collaboration tools (`spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, and `close_agent`) (stable; on by default). |
| `features.goals` | boolean | Enable persisted goals and automatic continuation (stable; on by default). |
| `features.remote_plugin` | boolean | Enable the remote plugin catalog (stable; on by default). |
| `features.personality` | boolean | Enable personality selection controls (stable; on by default). |
| `features.network_proxy` | boolean \| table | Enable sandboxed networking. Use a table form when setting network policy options such as `domains` (experimental; off by default). |
| `features.network_proxy.enabled` | boolean | Enable sandboxed networking. Defaults to `false`. |
| `features.network_proxy.domains` | map<string, allow \| deny> | Domain policy for sandboxed networking. Unset by default, which means no external destinations are allowed until you add `allow` rules. Supports exact hosts, `*.example.com` for subdomains only, `**.example.com` for apex plus subdomains, and global `*` allow rules; prefer scoped rules because `*` broadly opens public outbound access. Add `deny` rules for blocked destinations; `deny` wins on conflicts. |
| `features.network_proxy.unix_sockets` | map<string, allow \| deny> | Unix socket policy for sandboxed networking. Unset by default; add `allow` entries for permitted sockets. |
| `features.network_proxy.allow_local_binding` | boolean | Allow broader local/private-network access. Defaults to `false`; exact local IP literal or `localhost` allow rules can still permit specific local targets. |
| `features.network_proxy.enable_socks5` | boolean | Expose SOCKS5 support. Defaults to `true`. |
| `features.network_proxy.enable_socks5_udp` | boolean | Allow UDP over SOCKS5. Defaults to `true`. |
| `features.network_proxy.allow_upstream_proxy` | boolean | Allow chaining through an upstream proxy from the environment. Defaults to `true`. |
| `features.network_proxy.dangerously_allow_non_loopback_proxy` | boolean | Permit non-loopback listener addresses. Defaults to `false`; enabling it can expose proxy listeners beyond localhost. |
| `features.network_proxy.dangerously_allow_all_unix_sockets` | boolean | Permit arbitrary Unix socket destinations instead of allowlist-only access. Defaults to `false`; use only in tightly controlled environments. |
| `features.network_proxy.proxy_url` | string | 'HTTP listener URL for sandboxed networking. Defaults to `"http://127.0.0.1:3128"`.' |
| `features.network_proxy.socks_url` | string | 'SOCKS5 listener URL. Defaults to `"http://127.0.0.1:8081"`.' |
| `features.web_search` | boolean | Deprecated legacy toggle; prefer the top-level `web_search` setting. |
| `features.web_search_cached` | boolean | 'Deprecated legacy toggle. When `web_search` is unset, true maps to `web_search = "cached"`.' |
| `features.web_search_request` | boolean | 'Deprecated legacy toggle. When `web_search` is unset, true maps to `web_search = "live"`.' |
| `features.shell_tool` | boolean | Enable the default `shell` tool for running commands (stable; on by default). |
| `features.enable_request_compression` | boolean | Compress streaming request bodies with zstd when supported (stable; on by default). |
| `features.skill_mcp_dependency_install` | boolean | Allow prompting and installing missing MCP dependencies for skills (stable; on by default). |
| `features.fast_mode` | boolean | Enable model-catalog service tier selection in the TUI, including Fast-tier commands when the active model advertises them (stable; on by default). |
| `features.prevent_idle_sleep` | boolean | Prevent the machine from sleeping while a turn is actively running (experimental; off by default). |
| `suppress_unstable_features_warning` | boolean | Suppress the warning that appears when under-development feature flags are enabled. |
| `model_providers.<id>` | table | Custom provider definition. Built-in provider IDs (`openai`, `ollama`, and `lmstudio`) are reserved and cannot be overridden. |
| `model_providers.<id>.name` | string | Display name for a custom model provider. |
| `model_providers.<id>.base_url` | string | API base URL for the model provider. |
| `model_providers.<id>.env_key` | string | Environment variable supplying the provider API key. |
| `model_providers.<id>.env_key_instructions` | string | Optional setup guidance for the provider API key. |
| `model_providers.<id>.experimental_bearer_token` | string | Direct bearer token for the provider (discouraged; use `env_key`). |
| `model_providers.<id>.requires_openai_auth` | boolean | The provider uses OpenAI authentication (defaults to false). |
| `model_providers.<id>.wire_api` | responses | Protocol used by the provider. `responses` is the only supported value, and it is the default when omitted. |
| `model_providers.<id>.query_params` | map<string,string> | Extra query parameters appended to provider requests. |
| `model_providers.<id>.http_headers` | map<string,string> | Static HTTP headers added to provider requests. |
| `model_providers.<id>.env_http_headers` | map<string,string> | HTTP headers populated from environment variables when present. |
| `model_providers.<id>.request_max_retries` | number | Retry count for HTTP requests to the provider (default: 4). |
| `model_providers.<id>.stream_max_retries` | number | Retry count for SSE streaming interruptions (default: 5). |
| `model_providers.<id>.stream_idle_timeout_ms` | number | Idle timeout for SSE streams in milliseconds (default: 300000). |
| `model_providers.<id>.supports_websockets` | boolean | Whether that provider supports the Responses API WebSocket transport. |
| `model_providers.<id>.auth` | table | Command-backed bearer token configuration for a custom provider. Do not combine with `env_key`, `experimental_bearer_token`, or `requires_openai_auth`. |
| `model_providers.<id>.auth.command` | string | Command to run when Codex needs a bearer token. The command must print the token to stdout. |
| `model_providers.<id>.auth.args` | array<string> | Arguments passed to the token command. |
| `model_providers.<id>.auth.timeout_ms` | number | Maximum token command runtime in milliseconds (default: 5000). |
| `model_providers.<id>.auth.refresh_interval_ms` | number | How often Codex proactively refreshes the token in milliseconds (default: 300000). Set to `0` to refresh only after an authentication retry. |
| `model_providers.<id>.auth.cwd` | string (path) | Working directory for the token command. |
| `model_providers.amazon-bedrock.aws.profile` | string | AWS profile name used by the built-in `amazon-bedrock` provider. |
| `model_providers.amazon-bedrock.aws.region` | string | AWS region used by the built-in `amazon-bedrock` provider. |
| `model_reasoning_effort` | minimal \| low \| medium \| high \| xhigh | Adjust reasoning effort for supported models (Responses API only; `xhigh` is model-dependent). |
| `plan_mode_reasoning_effort` | none \| minimal \| low \| medium \| high \| xhigh | Plan-mode-specific reasoning override. When unset, Plan mode uses its built-in preset default. |
| `model_reasoning_summary` | auto \| concise \| detailed \| none | Select reasoning summary detail or disable summaries entirely. |
| `model_verbosity` | low \| medium \| high | Optional GPT-5 Responses API verbosity override; when unset, the selected model/preset default is used. |
| `model_supports_reasoning_summaries` | boolean | Force Codex to send or not send reasoning metadata. |
| `shell_environment_policy.inherit` | all \| core \| none | Baseline environment inheritance when spawning subprocesses. |
| `shell_environment_policy.ignore_default_excludes` | boolean | Keep variables containing KEY/SECRET/TOKEN before other filters run. |
| `shell_environment_policy.exclude` | array<string> | Glob patterns for removing environment variables after the defaults. |
| `shell_environment_policy.include_only` | array<string> | Whitelist of patterns; when set only matching variables are kept. |
| `shell_environment_policy.set` | map<string,string> | Explicit environment overrides injected into every subprocess. |
| `shell_environment_policy.experimental_use_profile` | boolean | Use the user shell profile when spawning subprocesses. |
| `project_root_markers` | array<string> | List of project root marker filenames; used when searching parent directories for the project root. |
| `project_doc_max_bytes` | number | Maximum bytes read from `AGENTS.md` when building project instructions. |
| `project_doc_fallback_filenames` | array<string> | Additional filenames to try when `AGENTS.md` is missing. |
| `history.persistence` | save-all \| none | Control whether Codex saves session transcripts to history.jsonl. |
| `tool_output_token_limit` | number | Token budget for storing individual tool/function outputs in history. |
| `background_terminal_max_timeout` | number | Maximum poll window in milliseconds for empty `write_stdin` polls (background terminal polling). Default: `300000` (5 minutes). Replaces the older `background_terminal_timeout` key. |
| `history.max_bytes` | number | If set, caps the history file size in bytes by dropping oldest entries. |
| `file_opener` | vscode \| vscode-insiders \| windsurf \| cursor \| none | URI scheme used to open citations from Codex output (default: `vscode`). |
| `otel.environment` | string | Environment tag applied to emitted OpenTelemetry events (default: `dev`). |
| `otel.exporter` | none \| otlp-http \| otlp-grpc | Select the OpenTelemetry exporter and provide any endpoint metadata. |
| `otel.trace_exporter` | none \| otlp-http \| otlp-grpc | Select the OpenTelemetry trace exporter and provide any endpoint metadata. |
| `otel.metrics_exporter` | none \| statsig \| otlp-http \| otlp-grpc | Select the OpenTelemetry metrics exporter (defaults to `statsig`). |
| `otel.log_user_prompt` | boolean | Opt in to exporting raw user prompts with OpenTelemetry logs. |
| `otel.exporter.<id>.endpoint` | string | Exporter endpoint for OTEL logs. |
| `otel.exporter.<id>.protocol` | binary \| json | Protocol used by the OTLP/HTTP exporter. |
| `otel.exporter.<id>.headers` | map<string,string> | Static headers included with OTEL exporter requests. |
| `otel.trace_exporter.<id>.endpoint` | string | Trace exporter endpoint for OTEL logs. |
| `otel.trace_exporter.<id>.protocol` | binary \| json | Protocol used by the OTLP/HTTP trace exporter. |
| `otel.trace_exporter.<id>.headers` | map<string,string> | Static headers included with OTEL trace exporter requests. |
| `otel.exporter.<id>.tls.ca-certificate` | string | CA certificate path for OTEL exporter TLS. |
| `otel.exporter.<id>.tls.client-certificate` | string | Client certificate path for OTEL exporter TLS. |
| `otel.exporter.<id>.tls.client-private-key` | string | Client private key path for OTEL exporter TLS. |
| `otel.trace_exporter.<id>.tls.ca-certificate` | string | CA certificate path for OTEL trace exporter TLS. |
| `otel.trace_exporter.<id>.tls.client-certificate` | string | Client certificate path for OTEL trace exporter TLS. |
| `otel.trace_exporter.<id>.tls.client-private-key` | string | Client private key path for OTEL trace exporter TLS. |
| `desktop.custom_file_handlers.<id>` | table | User-level only. Defines an additional **Open in** target for the ChatGPT desktop app. See [Add custom file handlers](https://learn.chatgpt.com/docs/config-file/config-advanced#add-custom-file-handlers) for examples and handler ID constraints. |
| `desktop.custom_file_handlers.<id>.label` | string | Display name shown in **Open in** menus. Required. |
| `desktop.custom_file_handlers.<id>.icon` | string | Bundled asset path, Base64-encoded `data:image/...` URL, file URI, or absolute local path for the handler icon. Required; unsupported sources use the default VS Code icon. |
| `desktop.custom_file_handlers.<id>.command` | string | Executable path or command name to detect and launch. Required. |
| `desktop.custom_file_handlers.<id>.args` | array<string> | Arguments inserted between the command and file input (default: `[]`). |
| `desktop.custom_file_handlers.<id>.input` | path \| json_argument \| json_stdin | How the app sends file input to the handler (default: `path`). |
| `desktop.custom_file_handlers.<id>.supports_ssh` | boolean | Offer the handler for files in SSH workspaces (default: `false`). |
| `tui` | table | TUI-specific options such as enabling inline desktop notifications. |
| `tui.notifications` | boolean \| array<string> | Enable TUI notifications; optionally restrict to specific event types. |
| `tui.notification_method` | auto \| osc9 \| bel | Notification method for terminal notifications (default: auto). |
| `tui.notification_condition` | unfocused \| always | Control whether TUI notifications fire only when the terminal is unfocused or regardless of focus. Defaults to `unfocused`. |
| `tui.animations` | boolean | Enable terminal animations (welcome screen, shimmer, spinner) (default: true). |
| `tui.alternate_screen` | auto \| always \| never | Control alternate screen usage for the TUI (default: auto; auto skips it in Zellij to preserve scrollback). |
| `tui.resume_cwd` | current \| session | Working directory to use when resuming or forking a session. When unset, Codex asks you to choose if your current directory differs from the session's saved directory. |
| `tui.vim_mode_default` | boolean | Start the composer in Vim normal mode instead of insert mode (default: false). You can still toggle it per session with `/vim`. |
| `tui.raw_output_mode` | boolean | Start the TUI in raw scrollback mode for copy-friendly terminal selection (default: false). You can toggle it with `/raw` or the default `alt-r` key binding. |
| `tui.show_tooltips` | boolean | Show onboarding tooltips in the TUI welcome screen (default: true). |
| `tui.status_line` | array<string> \| null | Ordered list of TUI footer status-line item identifiers. `null` disables the status line. |
| `tui.terminal_title` | array<string> \| null | 'Ordered list of terminal window/tab title item identifiers. Defaults to `["spinner", "project"]`; `null` disables title updates.' |
| `tui.theme` | string | Syntax-highlighting theme override (kebab-case theme name). |
| `tui.keymap.<context>.<action>` | string \| array<string> | Keyboard shortcut binding for a TUI action. Supported contexts include `global`, `chat`, `composer`, `editor`, `vim_normal`, `vim_operator`, `vim_text_object`, `pager`, `list`, and `approval`. Selected composer actions fall back to matching `tui.keymap.global` bindings; context-specific bindings take precedence when supported. |
| `tui.keymap.<context>.<action> = []` | empty array | Unbind the action in that keymap context. Key names use normalized strings such as `ctrl-a`, `shift-enter`, `page-down`, or `minus`. |
| `plugins.<plugin>.mcp_servers.<server>.enabled` | boolean | Enable or disable an MCP server bundled by an installed plugin without changing the plugin manifest. |
| `plugins.<plugin>.mcp_servers.<server>.default_tools_approval_mode` | auto \| prompt \| writes \| approve | Default approval behavior for tools on a plugin-provided MCP server. |
| `plugins.<plugin>.mcp_servers.<server>.enabled_tools` | array<string> | Allow list of tools exposed from a plugin-provided MCP server. |
| `plugins.<plugin>.mcp_servers.<server>.disabled_tools` | array<string> | Deny list applied after `enabled_tools` for a plugin-provided MCP server. |
| `plugins.<plugin>.mcp_servers.<server>.tools.<tool>.approval_mode` | auto \| prompt \| writes \| approve | Per-tool approval behavior override for a plugin-provided MCP tool. |
| `tui.model_availability_nux.<model>` | integer | Internal startup-tooltip state keyed by model slug. |
| `hide_agent_reasoning` | boolean | Suppress reasoning events in both the TUI and `codex exec` output. |
| `show_raw_agent_reasoning` | boolean | Surface raw reasoning content when the active model emits it. |
| `disable_paste_burst` | boolean | Disable burst-paste detection in the TUI. |
| `windows_wsl_setup_acknowledged` | boolean | Track Windows onboarding acknowledgement (Windows only). |
| `chatgpt_base_url` | string | Override the base URL used during the ChatGPT login flow. |
| `cli_auth_credentials_store` | file \| keyring \| auto | Control where the CLI stores cached credentials (file-based auth.json vs OS keychain). |
| `mcp_oauth_credentials_store` | auto \| file \| keyring | Preferred store for MCP OAuth credentials. |
| `mcp_oauth_callback_port` | integer | Optional fixed port for the local HTTP callback server used during MCP OAuth login. When unset, Codex binds to an ephemeral port chosen by the OS. |
| `mcp_oauth_callback_url` | string | Optional base callback URL override for MCP OAuth login (for example, a devbox ingress URL). Codex appends a server-specific callback ID before sending the final OAuth `redirect_uri`, so register the full derived URI with your provider. `mcp_oauth_callback_port` still controls the callback listener port. |
| `experimental_use_unified_exec_tool` | boolean | Legacy name for enabling unified exec; prefer `[features].unified_exec` or `codex --enable unified_exec`. |
| `tools.web_search` | 'boolean \| { context_size = "low\|medium\|high", allowed_domains = [string], location = { country, region, city, timezone } }' | Optional web search tool configuration. The legacy boolean form is still accepted, but the object form lets you set search context size, allowed domains, and approximate user location. |
| `tools.view_image` | boolean | Enable the local-image attachment tool `view_image`. |
| `web_search` | disabled \| cached \| indexed \| live | 'Web search mode (default: `"cached"`; cached uses an OpenAI-maintained index without external web access; indexed permits external access only when gated by the search index; if you use `--yolo` or another full access sandbox setting, it defaults to `"live"`). Use `"live"` for unrestricted live retrieval, or `"disabled"` to remove the tool.' |
| `default_permissions` | string | Name of the default permissions profile to apply to sandboxed tool calls. Built-ins are `:read-only`, `:workspace`, and `:danger-full-access`; custom profile names require matching `[permissions.<name>]` tables. Don't combine with `sandbox_mode` or `[sandbox_workspace_write]`. |
| `permissions.<name>.description` | string | Human-readable description for this named profile. A profile does not inherit its parent's description through `extends`. |
| `permissions.<name>.extends` | string | Optional parent profile applied before this named profile. Set it to another named profile, `:read-only`, or `:workspace`; `:danger-full-access`, undefined parents, and cycles are rejected. |
| `permissions.<name>.workspace_roots` | table | Profile-defined workspace roots that receive `:workspace_roots` filesystem rules alongside the session's runtime workspace roots. |
| `permissions.<name>.workspace_roots.<path>` | boolean | Opt a path into the profile's workspace root set when `true`. Disabled entries remain inactive. |
| `permissions.<name>.filesystem` | table | Named filesystem permission profile. Each key is an absolute path or special token such as `:minimal` or `:workspace_roots`. |
| `permissions.<name>.filesystem.glob_scan_max_depth` | number | Maximum depth for expanding deny-read glob patterns on platforms that snapshot matches before sandbox startup. Must be at least `1` when set. |
| `permissions.<name>.filesystem.<path-or-glob>` | '"read" \| "write" \| "deny" \| table' | 'Grant direct access for a path, glob pattern, or special token, or scope nested entries under that root. Use `"deny"` to deny reads for matching paths.' |
| `'permissions.<name>.filesystem.":workspace_roots".<subpath-or-glob>'` | '"read" \| "write" \| "deny"' | 'Scoped filesystem access relative to each effective workspace root. Use `"."` for the root itself; glob subpaths such as `"**/*.env"` can deny reads with `"deny"`.' |
| `permissions.<name>.network.enabled` | boolean | Enable network access for this named permissions profile. This changes the sandbox network policy; it does not start the network proxy by itself. |
| `permissions.<name>.network.proxy_url` | string | HTTP listener URL used when this permissions profile enables sandboxed networking. |
| `permissions.<name>.network.enable_socks5` | boolean | Expose SOCKS5 support when this permissions profile enables sandboxed networking. |
| `permissions.<name>.network.socks_url` | string | SOCKS5 proxy endpoint used by this permissions profile. |
| `permissions.<name>.network.enable_socks5_udp` | boolean | Allow UDP over the SOCKS5 listener when enabled. |
| `permissions.<name>.network.allow_upstream_proxy` | boolean | Allow sandboxed networking to chain through another upstream proxy. |
| `permissions.<name>.network.dangerously_allow_non_loopback_proxy` | boolean | Permit non-loopback bind addresses for sandboxed networking listeners. Enabling it can expose listeners beyond localhost. |
| `permissions.<name>.network.dangerously_allow_all_unix_sockets` | boolean | Allow arbitrary Unix socket destinations instead of the default restricted set. Use only in tightly controlled environments. |
| `permissions.<name>.network.mode` | limited \| full | Network proxy mode used for subprocess traffic. |
| `permissions.<name>.network.domains` | table | Domain rules for sandboxed networking. Supports exact hosts, `*.example.com` for subdomains only, `**.example.com` for apex plus subdomains, and global `*` allow rules. `deny` wins on conflicts. |
| `permissions.<name>.network.domains.<pattern>` | allow \| deny | Allow or deny an exact host or scoped wildcard pattern such as `*.example.com` or `**.example.com`. |
| `permissions.<name>.network.unix_sockets` | table | Unix socket allowlist overrides for sandboxed networking. Use socket paths as keys; `allow` adds a path, and `deny` rejects it. |
| `permissions.<name>.network.unix_sockets.<path>` | allow \| deny | Add an absolute Unix socket path to the effective allowlist with `allow`, or reject it with `deny`. Denied entries are omitted from the effective allowlist. |
| `permissions.<name>.network.allow_local_binding` | boolean | Permit broader local/private-network access through sandboxed networking. Exact local IP literal or `localhost` allow rules can still permit specific local targets when this stays `false`. |
| `projects.<path>.trust_level` | string | 'Mark a project or worktree as trusted or untrusted (`"trusted"` \| `"untrusted"`). Untrusted projects skip project-scoped `.codex/` layers, including project-local config, hooks, and rules.' |
| `notice.hide_full_access_warning` | boolean | Track acknowledgement of the full access warning prompt. |
| `notice.hide_world_writable_warning` | boolean | Track acknowledgement of the Windows world-writable directories warning. |
| `notice.hide_rate_limit_model_nudge` | boolean | Track opt-out of the rate limit model switch reminder. |
| `notice.hide_gpt5_1_migration_prompt` | boolean | Track acknowledgement of the GPT-5.1 migration prompt. |
| `notice.hide_gpt-5.1-codex-max_migration_prompt` | boolean | Track acknowledgement of the gpt-5.1-codex-max migration prompt. |
| `notice.model_migrations` | map<string,string> | Track acknowledged model migrations as old->new mappings. |
| `forced_login_method` | chatgpt \| api | Restrict Codex to a specific authentication method. |
| `forced_chatgpt_workspace_id` | string (uuid) | Limit ChatGPT logins to a specific workspace identifier. |

#### `requirements.toml` 설정 키 전수 (116개)

| Key | Type | Description |
|---|---|---|
| `sqlite_home` | string (path) | Enforce the directory where Codex stores SQLite-backed runtime state. |
| `log_dir` | string (path) | Enforce the directory where Codex writes local log files. |
| `model_catalog_json` | string (path) | Enforce the JSON model catalog Codex uses at startup. |
| `check_for_update_on_startup` | boolean | Enforce whether Codex checks for updates when it starts. |
| `allow_login_shell` | boolean | Enforce whether shell tools can start a login shell. |
| `feedback` | table | Managed feedback settings. |
| `feedback.enabled` | boolean | Enforce whether users can submit feedback across Codex clients. |
| `allowed_approval_policies` | array<string> | Allowed values for `approval_policy` (for example `untrusted`, `on-request`, `never`, and `granular`). |
| `allowed_approvals_reviewers` | array<string> | Allowed values for `approvals_reviewer`, such as `user` and `auto_review`. |
| `guardian_policy_config` | string | Managed Markdown policy instructions for automatic review. This takes precedence over local `[auto_review].policy`. Blank values are ignored. |
| `allowed_permission_profiles` | table<boolean> | Complete list of allowed permission profiles. Profiles set to `true` are allowed. Profiles that are omitted or set to `false` are denied, including profiles added in future versions. When requirements sources are combined, entries are matched by profile name. |
| `allowed_permission_profiles.<name>` | boolean | Allow or deny a built-in or custom permission profile defined in a loaded config or requirements source. A later, higher-precedence requirements source can use `false` to turn off a profile allowed by an earlier, lower-precedence source. |
| `default_permissions` | string | Managed default permission profile. The profile must be allowed by `allowed_permission_profiles`. Set this explicitly for predictable behavior; if omitted, Codex defaults to `:workspace` only when both `:workspace` and `:read-only` are explicitly allowed. |
| `enforce_residency` | string | Require Codex service traffic to use a supported data residency. Currently accepts `us`. |
| `models` | table | Managed model defaults for new threads. These values take priority over user and project defaults, but an explicit selection for the new thread can override them. |
| `models.new_thread` | table | Defaults to apply when a new local thread starts. Each model setting is optional. |
| `models.new_thread.model` | string | Default model for new threads. An explicit `--model` or model/reasoning `--config` override takes precedence. |
| `models.new_thread.model_reasoning_effort` | string | Default reasoning effort for new threads. An explicit model or reasoning-effort override skips both managed model fields. |
| `models.new_thread.service_tier` | string | Default service tier for new threads. An explicit service-tier override takes precedence independently of the model fields. |
| `permissions` | table | Admin-defined permission profiles keyed by profile name. Uses the same profile fields as `config.toml`. |
| `permissions.<name>` | table | Admin-defined permission profile. The name can't start with `:`, use the reserved name `filesystem`, or duplicate a profile from a loaded config. Uses the same profile fields as `config.toml`; see the Permissions guide for the complete profile schema. |
| `allowed_sandbox_modes` | array<string> | Allowed values for `sandbox_mode`. |
| `windows` | table | Native Windows sandbox requirements. |
| `windows.allowed_sandbox_implementations` | array<string> | Allowed native Windows sandbox implementations for `windows.sandbox` (`elevated` and `unelevated`). The list must not be empty. When both are allowed and no mode is selected, Codex prefers `elevated`. |
| `windows.sandbox_private_desktop` | boolean | Enforce whether the native Windows sandbox starts its child process on a private desktop. |
| `remote_sandbox_config` | array<table> | Host-specific sandbox requirements. The first entry whose `hostname_patterns` match the resolved host name overrides top-level `allowed_sandbox_modes` for that requirements source. Host-specific entries currently override sandbox modes only. |
| `remote_sandbox_config[].hostname_patterns` | array<string> | Case-insensitive host name patterns. Supports `*` for any sequence of characters and `?` for one character. |
| `remote_sandbox_config[].allowed_sandbox_modes` | array<string> | Allowed sandbox modes to apply when this host-specific entry matches. |
| `allowed_web_search_modes` | array<string> | Allowed values for `web_search` (`disabled`, `cached`, `indexed`, `live`). `disabled` is always allowed; an empty list effectively allows only `disabled`. |
| `allow_managed_hooks_only` | boolean | When `true`, Codex skips user, project, session, and plugin hooks while still allowing managed hooks from `requirements.toml` and other managed config layers. |
| `allow_appshots` | boolean | Set to `false` to disable Appshots for managed users. If omitted, Appshots remain unconstrained by requirements and follow normal product availability. |
| `allow_remote_control` | boolean | Set to `false` to disable device remote control for managed users. If omitted, device remote control remains unconstrained by requirements and follows normal product availability. |
| `features.plugin_sharing` | boolean | Set to `false` in cloud-managed `requirements.toml` to disable workspace sharing for locally built plugins. |
| `features` | table | Pinned feature values. Use canonical names from `config.toml` for runtime features; documented app-only requirement keys are also supported here. |
| `features.<name>` | boolean | Require a documented runtime or app feature to stay enabled or disabled. |
| `features.apps` | boolean | Pin Apps integration availability on or off for managed users. |
| `features.in_app_updates` | boolean | Set to `false` in `requirements.toml` to disable in-app updates. Updates remain enabled by default when this requirement is omitted. |
| `features.in_app_browser` | boolean | Set to `false` in `requirements.toml` to disable the built-in browser pane. |
| `features.browser_use` | boolean | Set to `false` in `requirements.toml` to disable Computer Use in browsers and Browser Agent availability. |
| `features.browser_use_external` | boolean | Set to `false` in `requirements.toml` to disable Computer Use in external browsers. |
| `features.browser_use_full_cdp_access` | boolean | Set to `false` in `requirements.toml` to disable full Chrome DevTools Protocol access in the local runtime, including Browser Developer mode, and prevent the ChatGPT desktop app from enabling the corresponding setting. If omitted, normal product availability applies. |
| `features.fast_mode` | boolean | Pin the canonical `fast_mode` feature on or off for managed users. |
| `features.guardian_approval` | boolean | Pin Guardian approval availability on or off for managed users. |
| `features.memories` | boolean | Pin Memories availability on or off for managed users. |
| `features.multi_agent` | boolean | Pin multi-agent availability on or off for managed users. |
| `features.plugins` | boolean | Pin plugin availability on or off for managed users. |
| `features.remote_plugin` | boolean | Pin remote plugin catalog availability on or off for managed users. |
| `features.computer_use` | boolean | Set to `false` in `requirements.toml` to disable Computer Use, Record & Replay, and related install or enablement flows. |
| `features.workspace_dependencies` | boolean | Pin bundled workspace-dependency runtime availability on or off for managed users. |
| `computer_use` | table | Computer Use requirements enforced from `requirements.toml`. |
| `computer_use.allow_locked_computer_use` | boolean | Set to `false` to prevent Computer Use from operating after a managed macOS device locks. If omitted, locked use remains unconstrained by requirements. |
| `experimental_network` | table | Network access requirements enforced from `requirements.toml`. These constraints are separate from `features.network_proxy` and can configure sandboxed networking without the user feature flag. |
| `experimental_network.enabled` | boolean | Enable sandboxed networking requirements. This does not grant network access when the active sandbox keeps command networking off. |
| `experimental_network.http_port` | integer | Loopback HTTP listener port to use for `[experimental_network]` requirements. |
| `experimental_network.socks_port` | integer | Loopback SOCKS5 listener port to use for `[experimental_network]` requirements. |
| `experimental_network.allow_upstream_proxy` | boolean | Allow sandboxed networking to chain through an upstream proxy from the environment. |
| `experimental_network.dangerously_allow_non_loopback_proxy` | boolean | Permit non-loopback listener addresses for `[experimental_network]` requirements. Enabling it can expose listeners beyond localhost. |
| `experimental_network.dangerously_allow_all_unix_sockets` | boolean | Permit arbitrary Unix socket destinations instead of allowlist-only access. Use only in tightly controlled environments. |
| `experimental_network.domains` | map<string, allow \| deny> | Map-shaped administrator domain policy for sandboxed networking. Supports exact hosts, `*.example.com` for subdomains only, `**.example.com` for apex plus subdomains, and global `*` allow rules; prefer scoped rules because `*` broadly opens public outbound access. `deny` wins on conflicts. Do not combine this with `experimental_network.allowed_domains` or `experimental_network.denied_domains`. |
| `experimental_network.allowed_domains` | array<string> | List-shaped administrator allow rules for sandboxed networking. Do not combine this with `experimental_network.domains`. |
| `experimental_network.denied_domains` | array<string> | List-shaped administrator deny rules for sandboxed networking. Do not combine this with `experimental_network.domains`. |
| `experimental_network.managed_allowed_domains_only` | boolean | When `true`, only administrator-managed allow rules remain effective while sandboxed networking requirements are active; user allowlist additions are ignored. Without managed allow rules, user-added domain allow rules do not remain effective. |
| `experimental_network.unix_sockets` | map<string, allow \| deny> | Administrator-managed Unix socket policy for sandboxed networking. |
| `experimental_network.allow_local_binding` | boolean | Permit broader local/private-network access for sandboxed networking. Exact local IP literal or `localhost` allow rules can still permit specific local targets when this stays `false`. |
| `hooks` | table | Admin-enforced managed lifecycle hooks. Requires a managed hook directory and uses the same event schema as inline `[hooks]` in `config.toml`. |
| `hooks.managed_dir` | string (absolute path) | Directory containing managed hook scripts on macOS and Linux. Codex validates that it is absolute and exists before loading managed hooks. |
| `hooks.windows_managed_dir` | string (absolute path) | Directory containing managed hook scripts on Windows. Codex validates that it is absolute and exists before loading managed hooks. |
| `hooks.<Event>` | array<table> | Matcher groups for a hook event such as `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, or `Stop`. |
| `hooks.<Event>[].hooks` | array<table> | Hook handlers for a matcher group. Command hooks are currently supported; prompt and agent hook handlers are parsed but skipped. |
| `hooks.<Event>[].hooks[].additionalContextLimit` | integer | Approximate per-handler token threshold for saving oversized `additionalContext` to disk and showing the model a shorter preview. Defaults to `2500`; `0` passes the full context directly to the model. See [Large hook output](https://learn.chatgpt.com/docs/hooks#large-hook-output). |
| `hooks.<Event>[].hooks[].commandWindows` | string | Windows-only command override for command hooks. The TOML alias `command_windows` is also accepted. |
| `permissions.filesystem.deny_read` | array<string> | Admin-enforced filesystem read denials. Entries can be paths or glob patterns, and users cannot weaken them with local config. |
| `mcp_servers` | table | Allowlist of MCP servers that may be enabled. Both the server name (`<id>`) and its identity must match for the MCP server to be enabled. Any configured MCP server not in the allowlist (or with a mismatched identity) is disabled. |
| `mcp_servers.<id>.identity` | table | Identity rule for a single MCP server. Set either `command` (stdio) or `url` (streamable HTTP). |
| `mcp_servers.<id>.identity.command` | string \| table | Allow an MCP stdio server by exact command string, or use a matcher table to require an exact executable and ordered argument matchers. The string form doesn't inspect arguments, `cwd`, `env`, or `env_vars`. |
| `mcp_servers.<id>.identity.command.executable` | string | Executable that the stdio server's configured `command` must match exactly. |
| `mcp_servers.<id>.identity.command.args` | array<table> | Ordered argument matchers for a stdio server. The configured argument list must have the same length, and every position must match. Command matchers don't inspect `cwd`, `env`, or `env_vars`. |
| `mcp_servers.<id>.identity.command.args[].match` | exact \| prefix \| regex | Match operation for this argument position. |
| `mcp_servers.<id>.identity.command.args[].value` | string | Value used by an `exact` or `prefix` argument matcher. |
| `mcp_servers.<id>.identity.command.args[].expression` | string | Regular expression used by a `regex` argument matcher. The expression must be valid and match the complete argument value. |
| `mcp_servers.<id>.identity.url` | string \| table | Allow an MCP streamable HTTP server by exact URL string, or use an `exact`, `prefix`, or `regex` value matcher table. |
| `mcp_servers.<id>.identity.url.match` | exact \| prefix \| regex | Match operation for the configured MCP server URL. |
| `mcp_servers.<id>.identity.url.value` | string | Value used by an `exact` or `prefix` URL matcher. |
| `mcp_servers.<id>.identity.url.expression` | string | Regular expression used by a `regex` URL matcher. The expression must be valid and match the complete URL value. |
| `plugins` | table | Plugin-specific MCP server allowlists keyed by plugin identifier. When this table is present, plugin-bundled servers without a matching plugin and server entry are disabled. |
| `plugins.<plugin>.mcp_servers` | table | Allowlist for MCP servers bundled with one plugin. Plugin server requirements use the same exact identity and matcher forms as top-level `mcp_servers` requirements. |
| `plugins.<plugin>.mcp_servers.<server>.identity` | table | Identity rule for one plugin-bundled MCP server. Set either `command` (stdio) or `url` (streamable HTTP). |
| `plugins.<plugin>.mcp_servers.<server>.identity.command` | string \| table | Allow a plugin's stdio MCP server by exact command string, or use a matcher table to require an exact executable and ordered argument matchers. |
| `plugins.<plugin>.mcp_servers.<server>.identity.command.executable` | string | Executable that the plugin-bundled stdio server's configured command must match exactly. |
| `plugins.<plugin>.mcp_servers.<server>.identity.command.args` | array<table> | Ordered argument matchers for a plugin-bundled stdio server. The configured argument list must have the same length, and every position must match. |
| `plugins.<plugin>.mcp_servers.<server>.identity.command.args[].match` | exact \| prefix \| regex | Match operation for this argument position. |
| `plugins.<plugin>.mcp_servers.<server>.identity.command.args[].value` | string | Value used by an `exact` or `prefix` argument matcher. |
| `plugins.<plugin>.mcp_servers.<server>.identity.command.args[].expression` | string | Regular expression used by a `regex` argument matcher. The expression must match the complete argument value. |
| `plugins.<plugin>.mcp_servers.<server>.identity.url` | string \| table | Allow a plugin's streamable HTTP MCP server by exact URL string, or use an `exact`, `prefix`, or `regex` value matcher table. |
| `plugins.<plugin>.mcp_servers.<server>.identity.url.match` | exact \| prefix \| regex | Match operation for the plugin-bundled MCP server URL. |
| `plugins.<plugin>.mcp_servers.<server>.identity.url.value` | string | Value used by an `exact` or `prefix` URL matcher. |
| `plugins.<plugin>.mcp_servers.<server>.identity.url.expression` | string | Regular expression used by a `regex` URL matcher. The expression must match the complete URL value. |
| `marketplaces` | table | Admin requirements for plugin marketplace sources. Rules take effect when `restrict_to_allowed_sources` is `true`. |
| `marketplaces.restrict_to_allowed_sources` | boolean | When `true`, require user-configured marketplace sources to match `allowed_sources` for marketplace add, plugin install, and configured Git marketplace refresh operations. Codex-managed OpenAI marketplaces remain allowed when their reserved source and name match. This doesn't filter already configured user marketplaces at runtime. |
| `marketplaces.allowed_sources` | table | Allowed marketplace sources keyed by administrator-chosen rule name. Distinct names accumulate across requirements layers; fields under the same name use normal layer precedence. |
| `marketplaces.allowed_sources.<name>` | table | One allowed source rule. The final `source` value after requirements merge determines which sibling fields Codex interprets. |
| `marketplaces.allowed_sources.<name>.source` | git \| host_pattern \| local | Marketplace source matcher type. Use `git` for one repository, `host_pattern` for Git hosts matched by regular expression, or `local` for one directory. |
| `marketplaces.allowed_sources.<name>.url` | string | 'Git repository URL required when `source = "git"`. Codex normalizes the configured and allowed URLs before requiring an exact repository match.' |
| `marketplaces.allowed_sources.<name>.ref` | string | Optional exact Git ref for a `git` rule. When omitted, the rule allows any ref for the matching repository. |
| `marketplaces.allowed_sources.<name>.host_pattern` | string | 'Regular expression required when `source = "host_pattern"`. Codex matches it against the lowercase hostname parsed from an HTTPS, SSH, or SCP-style Git source. Use `^` and `$` to require a whole-host match.' |
| `marketplaces.allowed_sources.<name>.path` | string (absolute path) | 'Local marketplace directory required when `source = "local"`. Codex requires an absolute path and compares paths after normalization.' |
| `apps` | table | Managed app requirements keyed by app identifier. Requirements can disable an app or constrain approval behavior for individual tools. |
| `apps.<id>.enabled` | boolean | Set to `false` to disable an app. A disabled requirement remains restrictive when multiple requirements sources are merged. |
| `apps.<id>.tools.<tool>.approval_mode` | auto \| prompt \| writes \| approve | Set the managed approval mode for one app tool. |
| `rules` | table | Admin-enforced command rules merged with `.rules` files. Requirements rules must be restrictive. |
| `rules.prefix_rules` | array<table> | List of enforced prefix rules. Each rule must include `pattern` and `decision`. |
| `rules.prefix_rules[].pattern` | array<table> | Command prefix expressed as pattern tokens. Each token sets either `token` or `any_of`. |
| `rules.prefix_rules[].pattern[].token` | string | A single literal token at this position. |
| `rules.prefix_rules[].pattern[].any_of` | array<string> | A list of allowed alternative tokens at this position. |
| `rules.prefix_rules[].decision` | prompt \| forbidden | Required. Requirements rules can only prompt or forbid (not allow). |
| `rules.prefix_rules[].justification` | string | Optional non-empty rationale surfaced in approval prompts or rejection messages. |
---

## 4. 커스터마이징 (Customization)

### Customization 개요
- URL: https://learn.chatgpt.com/codex/customization/overview · 원문: `codex__customization__overview.md`
- 보완적 5개 레이어:
  1. **Project guidance (AGENTS.md)** — 저장소와 함께 다니는 지속 지침 (빌드 명령·리뷰 기대치·저장소 관례)
  2. **Memories** — 이전 작업에서 학습된 컨텍스트, 로컬 지속
  3. **Skills** — 재사용 워크플로·도메인 전문성을 반복 가능한 프로세스로 패키징
  4. **MCP** — GitHub·Linear·Figma 등 외부 도구·공유 시스템 통합
  5. **Subagents** — 집중 작업 위임
- 경로: Skills는 `~/.agents/skills`(글로벌) / `.agents/skills`(저장소별). Global AGENTS.md는 `~/.codex/`.
- **AGENTS.md 갱신 신호:** 에이전트가 같은 실수를 반복할 때, 문서를 너무 많이 읽을 때, 같은 피드백을 반복할 때.
- **권장 도입 순서:** AGENTS.md 규칙 → 스킬 설치·작성 → MCP로 외부 시스템 연결 → **마지막으로** 서브에이전트 위임.
- Claude Code 대응: 5레이어가 거의 1:1 대응(AGENTS.md ↔ CLAUDE.md, Skills ↔ Skills, MCP ↔ MCP, Subagents ↔ Subagents). **"지침 먼저, 서브에이전트 마지막"** 이라는 순서 권고는 하네스 설계에도 그대로 적용되는 원칙.

### Memories
- URL: https://learn.chatgpt.com/codex/customization/memories · 원문: `codex__customization__memories.md`
- ChatGPT 웹은 ChatGPT memory를, **로컬 Codex 클라이언트는 별도의 로컬 메모리 저장소를 독립된 제어로** 유지한다.
- 관리: 데스크톱 앱은 `/memories` 또는 **Settings > Personalization**. CLI·IDE 확장은 대화형 세션의 `/memories`.
- 저장 경로: `~/.codex/memories/` — 요약(summaries), 지속 항목, 최근 입력, 근거를 담는다.
- 활성화:
  ```toml
  [features]
  memories = true
  ```
- **메모리 설정 키 (원문 설명 그대로)**

  | 키 | 설명 |
  |---|---|
  | `memories.generate_memories` | controls whether newly created chats can be stored as memory-generation inputs |
  | `memories.use_memories` | controls whether Codex injects existing memories into future sessions |
  | `memories.disable_on_external_context` | when `true`, keeps chats that used external context (MCP tools, web search) out of memory generation. 구 키 `memories.no_memories_if_mcp_or_web_search`는 레거시 별칭 |
  | `memories.min_rate_limit_remaining_percent` | controls the minimum remaining rate-limit percentage before memory generation starts |
  | `memories.extract_model` | overrides the model used for per-chat memory extraction |
  | `memories.consolidation_model` | overrides the model used for global memory consolidation |
  | `memories.max_raw_memories_for_consolidation` | (config-reference 원장 수록) |
  | `memories.max_rollout_age_days` | (config-reference 원장 수록) |
  | `memories.max_rollouts_per_startup` | (config-reference 원장 수록) |
  | `memories.max_unused_days` | (config-reference 원장 수록) |
  | `memories.min_rollout_idle_hours` | (config-reference 원장 수록) |

- 동작: 메모리는 채팅 종료 직후가 아니라 **백그라운드 모드에서 갱신**된다. 잔여 레이트리밋 비율이 임계값 아래면 생성을 건너뛴다.
- 보안: **"Don't store secrets in memories."** Codex는 생성된 메모리에서 시크릿을 리댁션한다.
- **핵심 인용 (설계 원칙):** "Keep required team guidance in `AGENTS.md` or checked-in documentation. Treat memories as a helpful recall layer, not as the only source for rules that must always apply."
- Claude Code 대응: 위 인용이 Codex 문서에서 가장 실용적인 설계 원칙 중 하나 — **"반드시 지켜야 할 규칙은 파일에, 메모리는 회상 보조층에".** `features.memories`가 기본 `false`(Experimental)인 점도 주목.

### Chronicle
- URL: https://learn.chatgpt.com/codex/customization/chronicle · 원문: `codex__customization__chronicle.md`
- **ChatGPT Pro 구독자 대상 macOS 전용 opt-in 리서치 프리뷰.** 최근 화면 컨텍스트를 Codex 메모리에 편입한다.
- 원문 경고 (활성화 전 고지): "Chronicle uses rate limits quickly, increases risk of prompt injection, and stores memories unencrypted on your device."
- 요구: ChatGPT **Pro** 구독 / macOS / Settings > Personalization에서 Memories 활성화 / macOS **Screen Recording**·**Accessibility** 권한
- 경로·보존:
  | 대상 | 경로 | 보존 |
  |---|---|---|
  | 화면 캡처 임시 저장 | `$TMPDIR/chronicle/screen_recording/` | Chronicle 실행 중 **6시간 초과분 삭제** |
  | 생성된 메모리 | `$CODEX_HOME/memories_extensions/chronicle/` (통상 `~/.codex/memories_extensions/chronicle`) | 암호화되지 않은 마크다운 |
- 인용: "Chronicle works by running sandboxed agents in the background to generate memories from captured screen images. These agents currently consume rate limits quickly."
- 인용: "Using Chronicle increases risk to prompt injection attacks from screen content."
- 데이터: 스크린샷은 메모리 생성을 위해 서버에서 처리되나 법적 요구가 없는 한 보관하지 않으며 모델 학습에 쓰이지 않는다.
- 제어: 메뉴 바 아이콘으로 일시정지·재개, Settings에서 완전 비활성화, 채팅 세션별 메모리 사용 제어.
- Claude Code 대응: 대응물 없음. Appshots(수동 1회 캡처)와 대비되는 **상시 화면 관찰형 메모리**. 문서가 프롬프트 인젝션 리스크를 명시 경고한다는 점이 인용 가치가 높다.

### CLI customization
- URL: https://learn.chatgpt.com/codex/cli-customization · 원문: `codex__cli-customization.md`
- **테마:** TUI는 마크다운 펜스 코드 블록과 파일 diff를 구문 강조. `/theme`로 피커를 열어 미리보고 `$CODEX_HOME/config.toml`의 `tui.theme`에 저장. 커스텀 테마는 `.tmTheme` 파일을 **`$CODEX_HOME/themes`** 에 둔다.
- **셸 자동완성:** Bash·Z shell·Fish·PowerShell 지원.
  ```
  eval "$(codex completion zsh)"
  ```
  `command not found: compdef` 오류 시:
  ```
  autoload -Uz compinit && compinit
  eval "$(codex completion zsh)"
  ```
- **프롬프트 에디터:** 컴포저에서 **Ctrl+G** → `VISUAL`(미설정 시 `EDITOR`) 환경 변수의 에디터를 연다. 저장·종료하면 텍스트가 컴포저로 돌아온다.
- Claude Code 대응: `codex completion zsh` ↔ Claude Code에는 표준 문서화된 셸 자동완성 명령이 없음. `$CODEX_HOME/themes`의 `.tmTheme` 지원은 Claude Code의 내장 테마 프리셋보다 확장성이 크다.

---

## 5. 에이전트 구성 (Agent Configuration)

### Custom instructions with AGENTS.md
- URL: https://learn.chatgpt.com/codex/agent-configuration/agents-md · 원문: `codex__agent-configuration__agents-md.md`

**탐색·우선순위 (원문 그대로 인용)**
> "Discovery follows this precedence order:
> 1. **Global scope:** In your Codex home directory (defaults to `~/.codex`), Codex reads `AGENTS.override.md` if it exists. Otherwise, Codex reads `AGENTS.md`.
> 2. **Project scope:** Starting at the project root, Codex walks down to your current working directory, checking for `AGENTS.override.md`, then `AGENTS.md` in each directory.
> 3. **Merge order:** Codex concatenates files from the root down. Files closer to your current directory override earlier guidance because they appear later in the combined prompt."

**`AGENTS.override.md` (원문 인용)**
> "Use `~/.codex/AGENTS.override.md` when you need a temporary global override without deleting the base file. Remove the override to restore the shared guidance."

**예시 (원문 그대로)**
```markdown
# ~/.codex/AGENTS.md

## Working agreements

- Always run `npm test` after modifying JavaScript files.
- Prefer `pnpm` when installing dependencies.
- Ask for confirmation before adding new production dependencies.
```
```markdown
# AGENTS.md

## Repository expectations

- Run `npm run lint` before opening a pull request.
- Document public utilities in `docs/` when you change behavior.
```
```markdown
# services/payments/AGENTS.override.md

## Payments service rules

- Use `make test-payments` instead of `npm test`.
- Never rotate API keys without notifying the security channel.
```

- 전역 지침 생성: `mkdir -p ~/.codex`
- **코드 리뷰 규칙:** 해당 `AGENTS.md`에 `## Code Review Rules` 섹션을 넣으면 GitHub 코드 리뷰 자동화의 체크로 쓰인다.
- **폴백 파일명 커스터마이즈** (`~/.codex/config.toml`):
  ```toml
  project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
  project_doc_max_bytes = 65536
  ```
- 검증: `codex --ask-for-approval never "Summarize current instructions"`
- 트러블슈팅: `AGENTS.override.md` 존재 확인 / 내용이 비지 않았는지 / 설정 문법 / Codex 재시작으로 지침 체인 재구성
- Claude Code 대응: **그룹 B에서 가장 직접적인 대응 지점.** `AGENTS.md` ↔ `CLAUDE.md`. 디렉터리 하향 탐색 + 가까운 파일이 나중에 붙어 우선한다는 병합 규칙도 동일한 발상. **차이:** Codex는 `project_doc_max_bytes`로 **지침 바이트 예산을 강제**하고 `project_doc_fallback_filenames`로 **파일명 자체를 커스터마이즈**할 수 있다(Claude Code는 `CLAUDE.md` 고정). `## Code Review Rules` 섹션 규약, `AGENTS.override.md`의 "삭제 없이 임시 오버라이드" 패턴도 Codex 고유.

### Subagents
- URL: https://learn.chatgpt.com/codex/agent-configuration/subagents · 원문: `codex__agent-configuration__subagents.md`
- 원문: "ChatGPT Work and Codex can run subagent workflows by spawning specialized agents in parallel and then collecting their results in one response."
- **비용 고지 (원문):** "Because each subagent does its own model and tool work, subagent workflows consume more tokens than comparable single-agent runs."

**왜 도움이 되는가 (원문 용어 정의)**
- **Context pollution**: "useful information gets buried under noisy intermediate output."
- **Context rot**: "performance degrades as the chat fills up with less relevant details."
- 참조: Chroma의 context rot 리서치 https://research.trychroma.com/context-rot
- 해법 3원칙: 메인 에이전트는 요구사항·결정·최종 산출에 집중 / 탐색·테스트·로그 분석은 서브에이전트 병렬 / 서브에이전트는 원시 중간 출력이 아니라 **요약을 반환**
- **원문 권고:** "use parallel agents for read-heavy tasks such as exploration, tests, triage, and summarization. Be more careful with parallel write-heavy workflows, because agents editing code at once can create conflicts and increase coordination overhead."

**핵심 용어 (원문)**
- **Subagent workflow**: Codex가 병렬 에이전트를 돌리고 결과를 결합하는 워크플로
- **Subagent**: 특정 작업을 위해 Codex가 시작한 위임 에이전트
- **Agent thread**: 서브에이전트가 작업하는 스레드. 지원 클라이언트에서 열어 진행·결과를 볼 수 있다

**내장 에이전트 3종 (원문)**
| 이름 | 역할 |
|---|---|
| `default` | general-purpose fallback agent |
| `worker` | execution-focused agent for implementation and fixes |
| `explorer` | read-heavy codebase exploration agent |

> "If a custom agent name matches a built-in agent such as `explorer`, your custom agent takes precedence."

**모델 선택 (원문 그대로)**
| 모델 | 용도 |
|---|---|
| `gpt-5.6` | "Start here for demanding agents. It's strongest for ambiguous, multi-step work that needs planning, tool use, validation, and follow-through across a larger context." |
| `gpt-5.6-terra` | "Use for agents that favor speed and efficiency over depth, such as exploration, read-heavy scans, large-file review, or processing supporting documents." |
| `gpt-5.6-luna` | "Use for fast, narrowly scoped agents handling clear, repeatable, or high-volume work." |

**Reasoning effort (`model_reasoning_effort`) — 원문 그대로**
| 값 | 용도 |
|---|---|
| `ultra` | "Use for the deepest reasoning when the selected model supports it." |
| `max` / `xhigh` | "Use for especially demanding reasoning when the selected model supports these levels." |
| `high` | 복잡한 로직 추적·가정 점검·엣지 케이스 (리뷰어·보안 에이전트) |
| `medium` | "A balanced default for most agents." |
| `low` | 단순하고 속도가 중요한 작업 |

> **⚠️ 대조 메모:** config-sample과 config-basic은 `model_reasoning_effort`를 `minimal \| low \| medium \| high \| xhigh`로 표기하고, subagents 문서만 `ultra`·`max`를 추가로 든다. 두 페이지가 다르므로 인용 시 **어느 페이지 기준인지 명시**할 것. (subagents는 "when the selected model supports it"이라는 조건을 붙인다.)

**커스텀 에이전트 정의**
- 위치: `~/.codex/agents/`(개인) 또는 `.codex/agents/`(프로젝트). 파일 하나가 에이전트 하나. **TOML.**
- 원문: "Codex loads these files as configuration layers for spawned sessions, so custom agents can override the same settings as a normal Codex session config. That can feel heavier than a dedicated agent manifest, and the format may evolve as authoring and sharing mature."

| Field | Type | Required | Purpose |
|---|---|---|---|
| `name` | string | Yes | Agent name Codex uses when spawning or referring to this agent. |
| `description` | string | Yes | Human-facing guidance for when Codex should use this agent. |
| `developer_instructions` | string | Yes | Core instructions that define the agent's behavior. |

> "You can also include other supported `config.toml` keys in a custom agent file, such as `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, and `skills.config`."
> "Codex identifies the custom agent by its `name` field. Matching the filename to the agent name is the simplest convention, but the `name` field is the source of truth."

**설정 해석 순서 (원문):** 커스텀 에이전트 파일이 `model`·`model_reasoning_effort`를 설정하면 **파일 값이 우선**한다. 그렇지 않으면 각각 독립적으로 해석 — **명시적 spawn 값 → 해당 `[agents]` 기본값 → 부모 값**. spawn이 다른 모델을 고르고 effort가 명시·설정 모두 없으면 **그 모델의 기본 effort**를 쓴다. `sandbox_mode`·`mcp_servers`·`skills.config` 등 다른 세션 설정은 파일이 생략하면 **부모에서 상속**한다.

**전역 `[agents]` 설정 (원문 표 그대로)**
| Field | Type | Required | Purpose |
|---|---|---|---|
| `agents.enabled` | boolean | No | Enable or disable multi-agent tools. |
| `agents.max_concurrent_threads_per_session` | number | No | Cap concurrently open spawned-agent threads, excluding the primary. |
| `agents.default_subagent_model` | string | No | Set the default model for spawned agents. |
| `agents.default_subagent_reasoning_effort` | string | No | Set the default reasoning effort for spawned agents. |
| `agents.interrupt_message` | boolean | No | Record a model-visible message when an agent turn is interrupted. |

- `agents.enabled` 기본 `true`. `agents.max_concurrent_threads_per_session` 미설정 시 Codex가 기본값 선택. **`agents.max_threads`는 레거시 별칭.** `agents.interrupt_message` 기본 `true`.

**승인·샌드박스**
- 서브에이전트는 **현재 샌드박스 정책을 상속**한다. 앱·IDE는 컴포저 아래에서 고른 permission mode를 상속한다.
- CLI: 비활성 에이전트 스레드에서도 승인 요청이 올라올 수 있다. 승인 오버레이가 출처 스레드 라벨을 보여주며, **`o`를 눌러 해당 스레드를 연 뒤** 승인·거부·응답할 수 있다.
- 비대화형 흐름에서는 새 승인이 필요한 동작이 **실패하고 부모 워크플로에 오류로 전달**된다.
- 원문: "Codex also reapplies the parent turn's live runtime overrides when it spawns a child. That includes sandbox and approval choices you set interactively during the session, such as `/permissions` changes or `--yolo`, even if the selected custom agent file sets different defaults."

**예시 1 — PR 리뷰 (원문 그대로)**
```toml
# .codex/config.toml
[agents]
max_concurrent_threads_per_session = 8
```
```toml
# .codex/agents/pr-explorer.toml
name = "pr_explorer"
description = "Read-only codebase explorer for gathering evidence before changes are proposed."
model = "gpt-5.3-codex-spark"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
developer_instructions = """
Stay in exploration mode.
Trace the real execution path, cite files and symbols, and avoid proposing fixes unless the parent agent asks for them.
Prefer fast search and targeted file reads over broad scans.
"""
```
```toml
# .codex/agents/reviewer.toml
name = "reviewer"
description = "PR reviewer focused on correctness, security, and missing tests."
model = "gpt-5.6-terra"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
developer_instructions = """
Review code like an owner.
Prioritize correctness, security, behavior regressions, and missing test coverage.
Lead with concrete findings, include reproduction steps when possible, and avoid style-only comments unless they hide a real bug.
"""
```
```toml
# .codex/agents/docs-researcher.toml
name = "docs_researcher"
description = "Documentation specialist that uses the docs MCP server to verify APIs and framework behavior."
model = "gpt-5.6-luna"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
developer_instructions = """
Use the docs MCP server to confirm APIs, options, and version-specific behavior.
Return concise answers with links or exact references when available.
Do not make code changes.
"""

[mcp_servers.openaiDeveloperDocs]
url = "https://developers.openai.com/mcp"
```
프롬프트 예시:
```text
Review this branch against main. Have pr_explorer map the affected code paths, reviewer find real risks, and docs_researcher verify the framework APIs that the patch relies on.
```

**예시 2 — 프론트엔드 통합 디버깅 (원문 그대로)**
```toml
# .codex/config.toml
[agents]
max_concurrent_threads_per_session = 6
```
```toml
# .codex/agents/code-mapper.toml
name = "code_mapper"
description = "Read-only codebase explorer for locating the relevant frontend and backend code paths."
model = "gpt-5.6-luna"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
developer_instructions = """
Map the code that owns the failing UI flow.
Identify entry points, state transitions, and likely files before the worker starts editing.
"""
```
```toml
# .codex/agents/browser-debugger.toml
name = "browser_debugger"
description = "UI debugger that uses browser tooling to reproduce issues and capture evidence."
model = "gpt-5.6-terra"
model_reasoning_effort = "high"
sandbox_mode = "workspace-write"
developer_instructions = """
Reproduce the issue in the browser, capture exact steps, and report what the UI actually does.
Use browser tooling for screenshots, console output, and network evidence.
Do not edit application code.
"""

[mcp_servers.chrome_devtools]
url = "http://localhost:3000/mcp"
startup_timeout_sec = 20
```
```toml
# .codex/agents/ui-fixer.toml
name = "ui_fixer"
description = "Implementation-focused agent for small, targeted fixes after the issue is understood."
model = "gpt-5.3-codex-spark"
model_reasoning_effort = "medium"
developer_instructions = """
Own the fix once the issue is reproduced.
Make the smallest defensible change, keep unrelated files untouched, and validate only the behavior you changed.
"""

[[skills.config]]
path = "/Users/me/.agents/skills/docs-editor/SKILL.md"
enabled = false
```
프롬프트 예시:
```text
Investigate why the settings modal fails to save. Have browser_debugger reproduce it, code_mapper trace the responsible code path, and ui_fixer implement the smallest fix once the failure mode is clear.
```
그 외 문서 제공 프롬프트:
```text
Review this branch with parallel subagents. Spawn one subagent for security risks, one for test gaps, and one for maintainability. Wait for all three, then summarize the findings by category with file references.
```
```text
I would like to review the following points on the current PR (this branch vs main). Spawn one agent per point, wait for all of them, and summarize the result for each point.
1. Security issue
2. Code quality
3. Bugs
4. Race
5. Test flakiness
6. Maintainability of the code
```
- 스레드 관리: CLI는 `/agent`로 활성 스레드 전환·검사. 앱·IDE는 패널에서 상태 확인·중지·스레드 열기. "Ask Codex directly to steer a running subagent, stop it, or close completed subagent threads."
- Claude Code 대응: **Claude Code 서브에이전트와 가장 직접 대응.** 차이가 명확하다 — Claude Code는 `.claude/agents/*.md`에 **YAML frontmatter + 마크다운 본문**, Codex는 `.codex/agents/*.toml`에 **순수 TOML + `developer_instructions` 멀티라인 문자열**. Codex 고유: `agents.max_concurrent_threads_per_session`(동시 상한), 내장 3에이전트(`default`/`worker`/`explorer`), **런타임 오버라이드가 커스텀 에이전트 파일 기본값을 이긴다**는 규칙, `/agent`로 스레드 전환. **"context pollution / context rot" 용어 정의**는 인용 가치가 높다.

### Speed (Fast mode & Codex-Spark)
- URL: https://learn.chatgpt.com/codex/agent-configuration/speed · 원문: `codex__agent-configuration__speed.md` (전문 1.8KB로 매우 짧다)
- **Fast mode (2026-08 기준 수치, 원문 인용)**
  - "Codex offers the ability to increase the speed of the model for increased credit consumption."
  - 속도: 지원 모델 속도 **1.5x**
  - 지원 모델: **GPT-5.6, GPT-5.5, GPT-5.4**
  - 크레딧: "GPT-5.6 and GPT-5.5 consume credits at **2.5x** the Standard rate; GPT-5.4 consumes credits at **2x** the Standard rate"
  - API: 토큰 과금이며 크레딧 배수가 아니다. "API Priority processing costs **2x** the Standard API token rate for GPT-5.6"
  - 명령: `/fast on`, `/fast off`, `/fast status`
  - 설정: `service_tier = "fast"` + `[features].fast_mode = true`
  - 표면: ChatGPT 데스크톱, Codex CLI, IDE 확장
- **Codex-Spark:** `GPT-5.3-Codex-Spark`는 모드 조정이 아니라 **실시간 코딩에 최적화된 별개의 더 빠른 모델**. 리서치 프리뷰 기간 **ChatGPT Pro 한정**, **별도 사용 한도**.
- **수집 한계:** 이 페이지에는 모델별 비교 표나 Codex-Spark의 구체 배수 수치가 없다(원문 전문 확인). 위 수치가 문서에 명시된 전부다.
- Claude Code 대응: Claude Code에 서비스 티어 다이얼은 없다. **"속도를 크레딧으로 산다"는 트레이드오프를 UI 명령(`/fast`)으로 노출**한 점이 설계 대비 포인트.

### Rules (execpolicy)
- URL: https://learn.chatgpt.com/codex/agent-configuration/rules · 원문: `codex__agent-configuration__rules.md`
- **Codex가 샌드박스 밖에서 실행할 수 있는 명령을 제어하는 규칙 시스템.**
- 위치: 활성 설정 계층 옆 `rules/` 폴더의 `.rules` 파일. 예: **`~/.codex/rules/default.rules`**
- 언어: **Starlark** (Python 유사 문법)

| `prefix_rule()` 필드 | 필수 | 설명 |
|---|---|---|
| `pattern` | 필수 | 명령어 접두사를 정의하는 비어 있지 않은 리스트 |
| `decision` | 선택 | `"allow"`(기본) / `"prompt"` / `"forbidden"` |
| `justification` | 선택 | 규칙의 이유 |
| `match` | 선택 | 규칙 검증용 매칭 예제 명령 |
| `not_match` | 선택 | 규칙 검증용 비매칭 예제 명령 |

| `decision` | 동작 |
|---|---|
| `allow` | 샌드박스 외부에서 프롬프트 없이 실행 |
| `prompt` | 일치하는 호출마다 실행 전 프롬프트 |
| `forbidden` | 프롬프트 없이 요청 차단 |

```starlark
prefix_rule(
    pattern = ["gh", "pr", "view"],
    decision = "prompt",
    justification = "Viewing PRs is allowed with approval",
    match = [
        "gh pr view 7888",
        "gh pr view --repo openai/codex",
        "gh pr view 7888 --json title,body,comments",
    ],
    not_match = [
        "gh pr --repo openai/codex view 7888",
    ],
)
```

**셸 래퍼 처리:** `bash -lc`, `bash -c` 등에서 —
- **안전한 경우**: `&&`, `||`, `;`, `|`로 연결된 명령을 **분리해 각각 평가**
- **복잡한 경우**: 리다이렉션·변수 치환 등이 있으면 **전체를 하나의 명령으로 취급**

**규칙 테스트 (원문 그대로)**
```bash
codex execpolicy check --pretty \
  --rules ~/.codex/rules/default.rules \
  -- gh pr view 7888 --json title,body,comments
```
- 관련 설정 키: `approval_policy.granular.rules`
- Claude Code 대응: **`settings.json`의 `permissions.allow`/`deny`/`ask`와 직접 대응.** Claude Code는 `Bash(gh pr view:*)` 문자열 패턴, Codex는 Starlark 함수로 접두사 리스트를 쓴다. **Codex 고유 강점 3가지:** (1) `justification`으로 규칙에 이유를 문서화 (2) `match`/`not_match`로 **규칙 자체를 테스트** (3) `codex execpolicy check`로 **규칙을 CI에서 검증**. Claude Code에는 규칙 단위 테스트 하네스가 없다 — 비교 챕터의 핵심 소재.

---

## 6. 확장 (Extend)

### Model Context Protocol (MCP)
- URL: https://learn.chatgpt.com/codex/extend/mcp · 원문: `codex__extend__mcp.md`
- 지원 기능 3범주: **STDIO servers**(로컬 프로세스, 환경 변수) / **Streamable HTTP servers**(원격, bearer token·OAuth) / **Server instructions**(초기화 시 읽는 도구 간 공통 안내)
- 표면별 설정:
  | 표면 | 방법 |
  |---|---|
  | ChatGPT 데스크톱 앱 | Settings → MCP servers → Add server → STDIO 또는 Streamable HTTP → 재시작 |
  | Codex CLI | `codex mcp add <server-name> -- <command>` (환경 변수는 `--env`) |
  | IDE 확장 | 기어 메뉴 → MCP servers → Add server → 확장 재시작 |
- CLI 명령 (원문 그대로):
  ```
  codex mcp add <server-name> --env VAR1=VALUE1 -- <stdio server-command>
  codex mcp list
  codex mcp --help
  codex mcp login <server-name>
  ```
- **STDIO 옵션:** `command`, `args`, `env`, `env_vars`, `cwd`, `experimental_environment`
- **Streamable HTTP 옵션:** `url`, `auth`, `bearer_token_env_var`, `http_headers`, `env_http_headers`
- **공통 옵션:** `startup_timeout_sec`, `tool_timeout_sec`, `enabled`, `required`, `enabled_tools`, `disabled_tools`, `default_tools_approval_mode`, `tools.<tool>.approval_mode`
- **최상위 옵션:** `mcp_oauth_callback_port`, `mcp_oauth_callback_url`
- TOML 예시 (원문 그대로):
  ```toml
  [mcp_servers.context7]
  command = "npx"
  args = ["-y", "@upstash/context7-mcp"]
  env_vars = ["LOCAL_TOKEN"]

  [mcp_servers.context7.env]
  MY_ENV_VAR = "MY_ENV_VALUE"

  [mcp_servers.figma]
  url = "https://mcp.figma.com/mcp"
  bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
  http_headers = { "X-Figma-Region" = "us-east-1" }

  [mcp_servers.chrome_devtools]
  url = "http://localhost:3000/mcp"
  enabled_tools = ["open", "screenshot"]
  default_tools_approval_mode = "prompt"
  ```
- 추천 MCP 서버: OpenAI Docs MCP(`https://developers.openai.com/mcp`), Context7, Figma(로컬/원격), Playwright, Chrome Developer Tools, Sentry, GitHub
- Claude Code 대응: `codex mcp add` ↔ `claude mcp add`, `[mcp_servers]` TOML ↔ `.mcp.json`. **Codex 고유:** `required = true`(초기화 실패 시 시작/재개 자체를 실패), `enabled_tools`/`disabled_tools` 도구 단위 allow/deny, `default_tools_approval_mode`(auto/prompt/writes/approve) — Claude Code는 MCP 도구 단위 승인 모드를 이 정도로 세분화하지 않는다.

### Record & Replay
- URL: https://learn.chatgpt.com/codex/extend/record-and-replay · 원문: `codex__extend__record-and-replay.md`
- **워크플로를 시연해 재사용 가능한 스킬로 바꾸는 기능.**
- 가용성: **macOS 전용**, 초기 가용성에서 **EEA·UK·스위스 제외**, **Computer Use가 사용 가능하고 활성화**되어야 함
- 절차: Plugins 열기 → **"Record a skill"** 선택 → 제안 프롬프트 검토·수정 → 녹화 권한 부여 → Mac에서 워크플로 시연 → 녹화 중지
- 생성 결과: 시스템이 동작을 관찰해 **언제 쓰는지·어떤 입력이 필요한지·어떤 단계인지·성공을 어떻게 검증하는지**를 설명하는 스킬을 만든다
- 재생: 새 채팅에서 스킬을 참조하고 가변 입력(파일·날짜 등)을 주면 Computer Use·브라우저 액션·플러그인으로 실행
- 사용 사례: 경비 처리, 주차 예약, 이슈 생성, 영상 게시, 리포트 다운로드
- 모범 사례: 시연은 **짧고 완결적으로**, 민감하지 않은 현실적 입력, 목표를 먼저 말하기, 이후 스킬을 다듬어 명명 규칙·판단 지점 같은 숨은 선호를 명시화
- Claude Code 대응: **대응물이 전혀 없는 Codex 고유 기능.** Claude Code 스킬은 사람이 마크다운으로 쓰지만, Record & Replay는 **GUI 조작 시연 → 스킬 자동 생성**이라는 역방향 저작 경로다.

### Hooks
- URL: https://learn.chatgpt.com/codex/hooks · 원문: `codex__hooks.md`
- 용도 (원문 그대로): 커스텀 로깅·분석 엔진으로 채팅 전송 / 팀 프롬프트를 스캔해 API 키 실수 붙여넣기 차단 / 채팅을 요약해 지속 메모리 자동 생성 / 턴 종료 시 커스텀 검증으로 표준 강제 / 특정 디렉터리에서 프롬프팅 커스터마이즈

**런타임 동작 (원문)**
- "Matching hooks from multiple files all run."
- "Multiple matching command hooks for the same event are launched concurrently, so one hook can't prevent another matching hook from starting."
- "Non-managed command hooks must be reviewed and trusted before they run."

**이벤트 실행 시점**
| When | Hooks |
|---|---|
| During a turn | `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `UserPromptSubmit`, `SubagentStop`, `Stop` |
| When a session or subagent starts | `SessionStart`, `SubagentStart` |
| When the main thread ends | `SessionEnd` (doesn't run for subagents) |

**탐색 위치**
- `hooks.json` 또는 `config.toml` 안의 인라인 `[hooks]` 테이블
- 실제로 유용한 4곳: `~/.codex/hooks.json` · `~/.codex/config.toml` · `<repo>/.codex/hooks.json` · `<repo>/.codex/config.toml`
- 설치된 플러그인도 매니페스트나 기본 `hooks/hooks.json`으로 번들 가능
- **중요:** "If more than one hook source exists, Codex loads all matching hooks. Higher-precedence config layers don't replace lower-precedence hooks." 한 레이어에 `hooks.json`과 인라인 `[hooks]`가 둘 다 있으면 **병합하고 시작 시 경고**한다. 레이어당 하나의 표현만 쓰는 것을 권장.
- 프로젝트 로컬 훅은 `.codex/` 레이어가 **trusted일 때만** 로드된다. untrusted 프로젝트에서도 사용자·시스템 훅은 로드된다.

**신뢰 검토 (Codex 고유)**
- "Before a non-managed command hook can run, Codex requires you to review and trust the exact hook definition. Codex records trust against the hook's current hash, so new or changed hooks are marked for review and skipped until trusted."
- `/hooks`로 소스 검사·신뢰·개별 비활성화. 시작 시 검토 필요하면 경고를 출력한다.
- 관리형 훅(system·MDM·cloud·`requirements.toml`)은 managed로 표시되고 정책상 신뢰되며 사용자 브라우저에서 비활성화할 수 없다.
- 일회성 자동화: **`--dangerously-bypass-hook-trust`**

**설정 구조 (JSON, 원문 그대로)**
```json
{
  "description": "Optional lifecycle hooks for this workspace.",
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/hooks/session_start.py",
            "statusMessage": "Loading session notes",
            "additionalContextLimit": 5000
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.codex/hooks/session_end.py",
            "timeout": 3
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py\"",
            "statusMessage": "Checking Bash command"
          }
        ]
      }
    ],
    "PermissionRequest": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/permission_request.py\"",
            "statusMessage": "Checking approval request"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/post_tool_use_review.py\"",
            "statusMessage": "Reviewing Bash output"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/user_prompt_submit_data_flywheel.py\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/stop_continue.py\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**필드 주의사항 (원문 그대로)**
- `description`은 `hooks.json`의 선택적 최상위 메타데이터. 어떤 훅이 도는지 바꾸지 않는다.
- `timeout`은 **초** 단위. 생략하면 대부분의 훅에 **`600`초**. **`SessionEnd`는 기본 `1`초이고 최대 `3`초까지 지원.**
- `statusMessage`는 선택.
- `additionalContextLimit`은 command 훅이 모델에 보낼 수 있는 `additionalContext` 양의 임계값.
- `commandWindows`는 Windows 전용 명령 오버라이드. TOML에서는 `command_windows` 또는 `commandWindows`.
- **`async` 옵션은 파싱되지만 비동기 command 훅은 아직 지원하지 않는다.**
- **오늘 실행되는 핸들러는 `type: "command"` 뿐이다. `prompt`와 `agent` 핸들러는 파싱되지만 건너뛴다.**
- 명령은 세션 `cwd`를 작업 디렉터리로 실행된다.
- repo-local 훅은 상대 경로(`.codex/hooks/...`) 대신 **git root 기준으로 해석**하라 — Codex가 하위 디렉터리에서 시작될 수 있다.

**동등한 인라인 TOML (원문 그대로)**
```toml
[[hooks.SessionStart]]
matcher = "^compact$"

[[hooks.SessionStart.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/session_start.py"'
additionalContextLimit = 5000

[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py"'
timeout = 30
statusMessage = "Checking Bash command"

[[hooks.PostToolUse]]
matcher = "^Bash$"

[[hooks.PostToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/post_tool_use_review.py"'
timeout = 30
statusMessage = "Reviewing Bash output"
```

**끄기**
```toml
[features]
hooks = false
```
`hooks`가 canonical key. **`codex_hooks`는 deprecated 별칭.** 관리자는 `requirements.toml`에 `[features].hooks = false`로 강제할 수 있다.

**관리형 훅 (`requirements.toml`, 원문 그대로)**
```toml
allow_managed_hooks_only = true

[features]
hooks = true

[hooks]
managed_dir = "/enterprise/hooks"
windows_managed_dir = 'C:\enterprise\hooks'

[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = "python3 /enterprise/hooks/pre_tool_use_policy.py"
command_windows = 'py -3 C:\enterprise\hooks\pre_tool_use_policy.py'
timeout = 30
statusMessage = "Checking managed Bash command"
```
- `managed_dir`는 macOS·Linux, `windows_managed_dir`는 Windows용.
- **Codex는 `managed_dir`의 스크립트를 배포하지 않는다** — 기업 도구가 별도로 설치·갱신해야 한다.
- `allow_managed_hooks_only = true`는 사용자·프로젝트·세션·플러그인 훅을 건너뛰고 관리형 훅만 로드한다.

**플러그인 번들 훅**
- 기본 탐색: 플러그인 루트의 `hooks/hooks.json`. `.codex-plugin/plugin.json`의 `hooks` 항목으로 오버라이드 가능 (`./`-prefixed 경로, 경로 배열, 인라인 hooks 객체, 또는 그 배열).
```json
{
  "name": "repo-policy",
  "hooks": "./hooks/hooks.json"
}
```
- 매니페스트 훅 경로는 플러그인 루트 기준으로 해석되며 **루트 밖으로 나갈 수 없다.**
- **환경 변수 (원문 그대로):**
  - `PLUGIN_ROOT` — "a Codex-specific extension that points to the installed plugin root."
  - `PLUGIN_DATA` — "a Codex-specific extension that points to the plugin's writable data directory."
  - **"Codex also sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for compatibility with existing plugin hooks."**
- 플러그인 설치·활성화가 자동으로 훅을 신뢰하지는 않는다. 검토·신뢰 전까지 건너뛴다.

**Matcher 패턴**
- `matcher`는 정규식 문자열. `"*"`, `""`, 또는 생략하면 해당 이벤트 전부에 매칭.

| Event | What `matcher` filters | Notes |
|---|---|---|
| `PermissionRequest` | tool name | `Bash`, `apply_patch`*, MCP tool names |
| `PostToolUse` | tool name | Tool coverage 참조 |
| `PostCompact` | compaction trigger | `manual` 또는 `auto` |
| `PreCompact` | compaction trigger | `manual` 또는 `auto` |
| `PreToolUse` | tool name | Tool coverage 참조 |
| `SessionEnd` | end reason | 현재 `other`만 |
| `SessionStart` | start source | `startup`, `resume`, `clear`, `compact` |
| `SubagentStart` | subagent type | 시작하는 서브에이전트에 따라 다름 |
| `SubagentStop` | subagent type | 중지하는 서브에이전트에 따라 다름 |
| `UserPromptSubmit` | **not supported** | 설정된 `matcher`는 무시됨 |
| `Stop` | **not supported** | 설정된 `matcher`는 무시됨 |

\* `apply_patch`는 `matcher` 값으로 `Edit` 또는 `Write`도 쓸 수 있다.

예시: `Bash` · `^apply_patch$` · `Edit|Write` · `mcp__filesystem__read_file` · `mcp__filesystem__.*` · `startup|resume|clear|compact` · `manual|auto`

**Tool coverage (원문 표 그대로)**
| Tool path | `PreToolUse` | `PostToolUse` | Notes |
|---|---|---|---|
| Shell commands | Yes | Yes | Match as `Bash`. |
| Unified exec (`exec_command`) | Yes | Yes | Match as `Bash`. A later `write_stdin` poll can deliver the original command's `PostToolUse` when that command finishes. |
| `apply_patch` | Yes | Yes | Match as `apply_patch`, `Edit`, or `Write`. |
| MCP tools | Yes | Yes | Match the MCP tool name, such as `mcp__filesystem__read_file`. |
| Other local function tools | Yes | Yes | Match the function tool name, such as `update_plan`. `spawn_agent` also matches `Agent`. |
| Hosted tools, such as `WebSearch` | No | No | These don't use the local function-tool hook path. |

> "Some specialized tool paths can opt out of the default hook path. Treat tool hooks as a useful guardrail, not a complete enforcement boundary."

**공통 입력 필드 (stdin JSON 1객체)**
| Field | Type | Meaning |
|---|---|---|
| `session_id` | `string` | Current Codex session id. Subagent hooks use the parent session id. |
| `transcript_path` | `string \| null` | Path to the session transcript file, if any |
| `cwd` | `string` | Working directory for the session |
| `hook_event_name` | `string` | Current hook event name |
| `model` | `string` | Codex-specific extension. Active model slug |

- `SessionStart`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `UserPromptSubmit`, `SubagentStart`, `SubagentStop`, `Stop`은 **`permission_mode`** 도 포함한다 — 값: `default`, `acceptEdits`, `plan`, `dontAsk`, `bypassPermissions`.
- 주의: "`transcript_path` points to a chat transcript for convenience, but the transcript format isn't a stable interface for hooks and may change over time."

**공통 출력 필드**
```json
{
  "continue": true,
  "stopReason": "optional",
  "systemMessage": "optional",
  "suppressOutput": false
}
```
| Field | Effect |
|---|---|
| `continue` | If `false`, marks that hook run as stopped |
| `stopReason` | Recorded as the reason for stopping |
| `systemMessage` | Surfaced as a warning in the UI or event stream |
| `suppressOutput` | Parsed today but not yet implemented |

- 출력 없이 exit `0`이면 성공으로 보고 계속 진행한다.
- `PreToolUse`·`PermissionRequest`는 `systemMessage`만 지원하고 `continue`·`stopReason`·`suppressOutput`은 미지원. 미지원 필드를 반환하면 해당 훅 실행을 실패로 표시하고 오류를 보고한 뒤 **툴 호출은 계속한다.**
- `PostToolUse`는 `systemMessage`, `continue: false`, `stopReason`을 지원하고 `suppressOutput`은 미지원.

**Large hook output (spilling)**
- 기본적으로 **모델이 보는 훅 출력 메시지 하나를 약 2,500 토큰**으로 제한한다.
- 초과하면 전문을 **`<temp_dir>/hook_outputs/<session_id>/<uuid>.txt`** 에 저장하고, 모델에는 head-and-tail 미리보기 + 저장 경로를 준다. 이 동작을 **spilling**이라 부른다. 파일 쓰기가 실패해도 모델은 잘린 미리보기를 받는다.
- 원문 경고: "Keep hook and plugin context concise. Context from multiple hooks and plugins adds up and can degrade model performance. Raising `additionalContextLimit` increases that risk. Avoid setting the limit to `0` unless the hook enforces a strict output cap; otherwise, a single hook can consume the entire context window."
```json
{
  "type": "command",
  "command": "python3 ~/.codex/hooks/session_start.py",
  "additionalContextLimit": 5000
}
```
- 생략하면 기본 **`2500`** 토큰 임계값. 양의 정수로 변경하거나 **`0`으로 두면 전체를 그대로 모델에 전달**한다. 각 핸들러를 독립 평가하며, additional context를 만들 수 없는 이벤트에서는 무시하고 설정 경고를 낸다.
- 이 설정은 `additionalContext`에만 적용된다. 툴 피드백과 continuation 프롬프트는 기본 제한을 유지한다.
- **"Because oversized output can be written to disk, avoid returning secrets or other sensitive data in hook output."**

**이벤트별 상세 (11종 전수)**

*SessionStart* — `matcher`는 `source`에 적용. 추가 입력: `source` (`startup`/`resume`/`clear`/`compact`). stdout 평문은 추가 developer context로 붙는다.
```json
{ "hookSpecificOutput": { "hookEventName": "SessionStart", "additionalContext": "Load the workspace conventions before editing." } }
```
> compaction 후: "`SessionStart` hooks that match `source: \"compact\"` run before the next model request." 턴 중간 자동 compaction에도 적용되며, 훅의 추가 컨텍스트를 **다음 사용자 턴이 아니라 즉시 continuation에 전달**한다. `continue: false`면 다음 모델 요청 없이 턴을 종료한다.

*SessionEnd* — 메인 스레드 종료 시 실행. 대화를 아카이브·삭제할 때, Codex가 정상 종료할 때, **또는 대화가 유휴 상태이고 어떤 연결 클라이언트에도 열려 있지 않은 채 30분이 지난 뒤**. **서브에이전트에는 실행되지 않는다.** 대화 전환이나 `thread/unsubscribe`는 즉시 세션을 끝내지 않는다. 추가 입력: `reason` (현재 항상 `other`). **자문(advisory)** — 출력이 Codex를 조종하거나 스레드를 열어두지 못한다.
```json
{
  "session_id": "thr_123",
  "transcript_path": "/workspace/.codex/rollout.jsonl",
  "cwd": "/workspace",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

*SubagentStart* — `matcher`는 `agent_type`. 추가 입력: `turn_id`, `agent_id`, `agent_type`, `permission_mode`. stdout 평문은 **서브에이전트용** 추가 developer context.
```json
{ "hookSpecificOutput": { "hookEventName": "SubagentStart", "additionalContext": "Review the repository test conventions first." } }
```
`continue: false`는 호환성을 위해 파싱되지만 **서브에이전트 시작을 막지 못한다.**

*PreToolUse* — 추가 입력: `turn_id`, `tool_name`, `tool_use_id`, `tool_input`. stdout 평문은 무시. 차단:
```json
{ "hookSpecificOutput": { "hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "Destructive command blocked by hook." } }
```
구형 shape도 허용:
```json
{ "decision": "block", "reason": "Destructive command blocked by hook." }
```
**exit code `2` + stderr에 사유**도 가능. 차단 없이 컨텍스트 추가:
```json
{ "hookSpecificOutput": { "hookEventName": "PreToolUse", "additionalContext": "The pending command touches generated files." } }
```
**툴 호출 재작성 (rewrite):**
```json
{ "hookSpecificOutput": { "hookEventName": "PreToolUse", "permissionDecision": "allow", "updatedInput": { "command": "echo rewritten" } } }
```
Bash·`apply_patch`는 `updatedInput`에 문자열 `command` 필드가 있어야 한다. MCP·기타 로컬 함수 툴은 `updatedInput`이 대체 인자 객체다. **`updatedInput`은 `permissionDecision: "allow"`와만 반환**하라. `permissionDecision: "ask"`, 레거시 `decision: "approve"`, `continue: false`, `stopReason`, `suppressOutput`은 파싱되나 미지원.

*PermissionRequest* — "runs when Codex is about to ask for approval, such as a shell escalation or managed-network approval." 승인이 필요 없는 명령에는 실행되지 않는다. 추가 입력: `turn_id`, `tool_name`, `tool_input`, `tool_input.description`.
```json
{ "hookSpecificOutput": { "hookEventName": "PermissionRequest", "decision": { "behavior": "allow" } } }
```
```json
{ "hookSpecificOutput": { "hookEventName": "PermissionRequest", "decision": { "behavior": "deny", "message": "Blocked by repository policy." } } }
```
- **"If multiple matching hooks return decisions, any `deny` wins."** `allow`면 승인 프롬프트 없이 진행. 아무 훅도 결정하지 않으면 정상 승인 흐름을 쓴다.
- `updatedInput`·`updatedPermissions`·`interrupt`는 반환하지 말 것 — 미래용으로 예약돼 있고 오늘은 fail closed다.

*PostToolUse* — 추가 입력: `turn_id`, `tool_name`, `tool_use_id`, `tool_input`, `tool_response`. Bash는 **비정상 종료(non-zero) 후에도 실행**된다. 이미 실행된 부수효과는 되돌릴 수 없다.
```json
{
  "decision": "block",
  "reason": "The Bash output needs review before continuing.",
  "hookSpecificOutput": { "hookEventName": "PostToolUse", "additionalContext": "The command updated generated files." }
}
```
> "For this event, `decision: \"block\"` doesn't undo the completed Bash command. Instead, Codex records the feedback, replaces the tool result with that feedback, and continues the model from the hook-provided message."
- `continue: false`면 원래 툴 결과의 정상 처리를 중단하고 피드백/중지 텍스트로 대체해 이어간다.
- `updatedMCPToolOutput`·`suppressOutput`은 파싱되나 미지원.

**code mode의 중첩 툴 호출 (원문 표)**
| Hook result | What code mode sees |
|---|---|
| `PreToolUse` blocks | The tool promise rejects before the tool runs. |
| `PreToolUse` returns `updatedInput` | The tool runs with the rewritten input and the promise resolves with that result. |
| `PostToolUse` returns `decision: "block"` or exits with code `2` | The tool runs, then the promise rejects with the hook reason. |
| `PostToolUse` returns `continue: false` | Codex uses the hook feedback for the model-visible result, but doesn't reject the nested tool promise. |

*PreCompact* / *PostCompact* — `matcher`는 `trigger`(`manual`/`auto`). 추가 입력: `turn_id`, `trigger`. stdout 평문 무시. 매칭 훅이 `continue: false`를 반환하면 `PreCompact`는 **compaction 전에 중단**, `PostCompact`는 **compaction 후에 중단**한다.

*UserPromptSubmit* — `matcher` 미사용. 추가 입력: `turn_id`, `prompt`. stdout 평문은 추가 developer context.
```json
{ "hookSpecificOutput": { "hookEventName": "UserPromptSubmit", "additionalContext": "Ask for a clearer reproduction before editing files." } }
```
차단:
```json
{ "decision": "block", "reason": "Ask for confirmation before doing that." }
```

*SubagentStop* — `matcher`는 `agent_type`. 추가 입력: `turn_id`, `agent_id`, `agent_type`, `agent_transcript_path`, `stop_hook_active`, `last_assistant_message`. **exit `0`일 때 stdout에 JSON을 요구한다. 평문 출력은 이 이벤트에 무효.**
```json
{ "decision": "block", "reason": "Run one more focused pass inside the subagent." }
```
매칭 훅 중 하나가 `continue: false`를 반환하면 다른 훅의 continuation 결정보다 우선한다.

*Stop* — `matcher` 미사용. 추가 입력: `turn_id`, `stop_hook_active`, `last_assistant_message`. **exit `0`일 때 stdout JSON 필수.**
```json
{ "decision": "block", "reason": "Run one more pass over the failing tests." }
```
> "For this event, `decision: \"block\"` doesn't reject the turn. Instead, it tells Codex to continue and automatically creates a new continuation prompt that acts as a new user prompt, using your `reason` as that prompt text."

**스키마:** 정확한 현재 wire format은 https://github.com/openai/codex/tree/main/codex-rs/hooks/schema/generated (단, `main` 브랜치 스키마에는 현재 릴리스에 없는 필드가 있을 수 있으므로 **문서 페이지를 릴리스 동작 기준으로 삼으라**고 명시).

- Claude Code 대응: **이름·구조가 놀랍도록 일치한다.** 동일 이벤트: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`, `PreCompact`. 동일 스키마 요소: `matcher` 그룹 → `hooks[]`, `type: "command"`, stdin JSON(`session_id`·`transcript_path`·`cwd`·`hook_event_name`), `hookSpecificOutput.additionalContext`, `permissionDecision`, `{"decision":"block","reason":...}`, exit code 2 + stderr 관례까지 동일. **결정적 증거:** Codex가 **`CLAUDE_PLUGIN_ROOT`·`CLAUDE_PLUGIN_DATA`를 호환용으로 설정**한다고 문서에 명시 — 기존 Claude 플러그인 훅과의 호환을 명시적으로 노린 설계다. **Codex 고유:** `PermissionRequest`·`PostCompact`·`SubagentStart` 이벤트 / `statusMessage`(UI 진행 표시) / `additionalContextLimit`과 **spilling**(2,500토큰 초과 시 디스크로) / `commandWindows` / **훅 신뢰 검토(해시 기반)와 `--dangerously-bypass-hook-trust`** / `allow_managed_hooks_only`. Claude Code에는 훅 신뢰 게이트가 없다 — 보안 비교 챕터의 핵심 소재.

### Build skills
- URL: https://learn.chatgpt.com/codex/build-skills · 원문: `codex__build-skills.md`
- 스킬은 **open agent skills standard**를 따라 지침·리소스·선택적 스크립트를 패키징한다.
- 디렉터리 구조 (원문 FileTree):
  ```
  my-skill/
  ├── SKILL.md              (Required: instructions + metadata)
  ├── scripts/              (Optional: executable code)
  ├── references/           (Optional: documentation)
  ├── assets/               (Optional: templates, resources)
  └── agents/
      └── openai.yaml       (Optional: appearance and dependencies)
  ```
- SKILL.md 프론트매터 (필수 2필드):
  ```yaml
  ---
  name: skill-name
  description: Explain exactly when this skill should and should not trigger.
  ---

  Skill instructions here.
  ```
- `agents/openai.yaml` (원문 그대로):
  ```yaml
  interface:
    display_name: "Optional user-facing name"
    short_description: "Optional user-facing description"
    icon_small: "./assets/small-logo.svg"
    icon_large: "./assets/large-logo.png"
    brand_color: "#3B82F6"
    default_prompt: "Optional surrounding prompt to use the skill with"

  policy:
    allow_implicit_invocation: false

  dependencies:
    tools:
      - type: "mcp"
        value: "openaiDeveloperDocs"
        description: "OpenAI Docs MCP server"
        transport: "streamable_http"
        url: "https://developers.openai.com/mcp"
  ```
- 호출 2방식: **Explicit** — ChatGPT는 `@`, Codex CLI는 `$`. **Implicit** — 과제가 description과 맞으면 자동 선택.
- 로드 경로 (Codex):
  ```
  $CWD/.agents/skills        (repo-specific)
  $REPO_ROOT/.agents/skills  (repo-wide)
  $HOME/.agents/skills       (user-level)
  /etc/codex/skills          (admin-level)
  ```
- 생성 도구: ChatGPT Work `@skill-creator`, Codex `$skill-creator`. 큐레이션 설치는 `$skill-installer`.
- 배포: "Bundle two or more skills together, or ship a skill alongside a connector, package them as a plugin"
- 모범 사례: 스킬 하나는 한 과제에 집중 / **스크립트보다 지침 선호** / 명시적 입출력과 함께 명령형 단계 / description에 맞춰 프롬프트 테스트
- 관련 설정 키: `skills.config`, `skills.config.<index>.path`, `skills.config.<index>.enabled`
- Claude Code 대응: **거의 동일한 표준**(`SKILL.md` + name/description frontmatter). 경로만 다르다 — Claude Code `.claude/skills/`, Codex `.agents/skills/`. **Codex 고유:** `agents/openai.yaml`의 `interface`(브랜드 색·아이콘·표시명)와 **`policy.allow_implicit_invocation`**, **`dependencies.tools`로 스킬이 필요로 하는 MCP 서버를 선언**(Claude Code 스킬은 도구 의존성을 선언하지 않는다), `/etc/codex/skills` 관리자 레벨 경로.

### Build plugins
- URL: https://learn.chatgpt.com/codex/build-plugins · 원문: `codex__build-plugins.md`
- 정의: "A plugin is an installable package that can include skills, an MCP server, or both. An MCP server can also return optional UI."
- **ChatGPT와 Codex는 하나의 유니버설 플러그인 디렉터리를 공유**한다. 공개 플러그인을 한 번 게시하면 두 제품의 지원 표면에서 같은 목록이 발견된다. 개발 중에는 **로컬 마켓플레이스**로 테스트한다.
- 판단 기준 (원문): "Start with a skill when you are still iterating on one personal workflow. Build a plugin when you want to share that workflow, package related skills, connect to an external service, or distribute a stable capability to a team."
- `@plugin-creator` / `$plugin-creator`:
  ```
  @plugin-creator Create a plugin named meeting-follow-up.
  Include a skill that turns meeting notes into decisions, owners, and next steps.
  Add it to a personal marketplace so I can test it locally.
  ```
- 생성 후 절차 (원문): 1) `.codex-plugin/plugin.json` 검토 2) `skills/` 아래 각 스킬 확인 3) 새로고침 후 로컬 마켓플레이스 소스에서 설치 4) 새 대화에서 대표 요청으로 테스트
- 최소 구조 (원문 그대로):
  ```
  meeting-follow-up/
  ├── .codex-plugin/
  │   └── plugin.json
  └── skills/
      └── meeting-follow-up/
          └── SKILL.md
  ```
  ```json
  {
    "name": "meeting-follow-up",
    "version": "1.0.0",
    "description": "Turn meeting notes into decisions and next steps",
    "skills": "./skills/"
  }
  ```
  ```markdown
  ---
  name: meeting-follow-up
  description: Extract decisions, owners, and next steps from meeting notes.
  ---

  Review the meeting notes. Return:

  1. Decisions
  2. Action items with owners
  3. Open questions
  ```
- 명명: 플러그인 이름은 **kebab case**로 안정적으로. 스킬 description은 적용 시점을 인지할 만큼 구체적으로.
- MCP 서버 포함 시: 먼저 서버를 빌드·테스트한 뒤 `@plugin-creator`에 등록된 연결 정보를 준다.
- 빌더 문서: https://developers.openai.com/plugins/ (concepts/plugins · build/skills · build/mcp-server · build/chatgpt-ui · build/plugins · deploy/connect-chatgpt · deploy/submission)
- 관련 설정 키: `plugins.<plugin>.mcp_servers.<server>.{enabled, enabled_tools, disabled_tools, default_tools_approval_mode, tools.<tool>.approval_mode}`, `features.remote_plugin`
- Claude Code 대응: **개념·구조가 거의 동형.** `.codex-plugin/plugin.json` ↔ `.claude-plugin/plugin.json`(동일한 name/version/description 필드), `skills/` 규약 동일, 로컬 마켓플레이스 → 공개 디렉터리 흐름 동일. **차이:** ChatGPT와 Codex가 **하나의 유니버설 디렉터리를 공유**하고, MCP 서버가 **선택적 UI를 반환**할 수 있다(Claude Code MCP에는 UI 반환 개념이 없음).

---

## 7. Windows

### ChatGPT desktop app for Windows
- URL: https://learn.chatgpt.com/codex/windows/windows-app · 원문: `codex__windows__windows-app.md`
- PowerShell·Windows 샌드박스·WSL2 통합을 네이티브 지원. 핵심 워크플로: worktrees, scheduled tasks, Git, 내장 브라우저, 파일 미리보기, 플러그인, 스킬.
- 설치: Microsoft Store 또는
  ```
  winget install --id 9PLM9XGG6VKS -s msstore
  ```
- 커스터마이징: Preferred editor(VS Code·Visual Studio 등) / Integrated terminal(PowerShell·Command Prompt·Git Bash·WSL) / Agent를 Windows 네이티브로 돌릴지 WSL2로 전환할지
- 권장 개발 도구: Git, Node.js, Python, .NET SDK, GitHub CLI — 모두 `winget` 설치 지원
- **WSL2 경로 성능:** 프로젝트는 `\\wsl$\` 경로로 접근 가능하나, 안정적 성능을 위해서는 **프로젝트를 Windows 파일시스템에 두고 WSL에서 `/mnt/<drive>/...` 로 접근**하라.
  > **⚠️ 대조 필요:** `/codex/windows/wsl` 페이지는 반대 권고("저장소를 Linux 홈 `~/code/`에 두고 `/mnt/c/…`는 피하라")를 한다. **두 페이지의 권고 방향이 다르므로 인용 시 반드시 어느 페이지 기준인지 밝힐 것.** (맥락 차이로 보인다 — windows-app은 "앱이 Windows 네이티브로 도는 경우", wsl은 "Codex를 WSL 안에서 도는 경우"를 전제한다.)
- Claude Code 대응: Claude Code도 Windows 네이티브/WSL 양쪽을 지원하나 **OS 네이티브 샌드박스(elevated/unelevated)는 없다.**

### Windows sandbox
- URL: https://learn.chatgpt.com/codex/windows/windows-sandbox · 원문: `codex__windows__windows-sandbox.md`
- 원문: "The app can run natively in PowerShell with a Windows sandbox instead of requiring WSL or a virtual machine."
- **2모드**
  | 모드 | 설명 |
  |---|---|
  | `elevated` | **선호되는 네이티브 Windows 샌드박스.** 전용 저권한 샌드박스 사용자, 파일시스템 권한 경계, 방화벽 규칙, 로컬 정책 변경 |
  | `unelevated` | **폴백.** 제한된 Windows 토큰으로 실행, ACL 기반 파일시스템 경계, 환경 레벨 오프라인 제어 |
  ```toml
  [windows]
  sandbox = "elevated" # or "unelevated"
  ```
- 엔터프라이즈 강제:
  ```toml
  [windows]
  allowed_sandbox_implementations = ["elevated"]
  ```
- 샌드박스 읽기 권한 부여: `/sandbox-add-read-dir C:\absolute\directory\path`
- **Windows 버전 지원**
  | 버전 | 지원 |
  |---|---|
  | Windows 11 | Recommended |
  | 최신 업데이트된 Windows 10 | Best effort |
  | 구버전 Windows 10 빌드 | Not recommended |
- 트러블슈팅 항목: 네이티브 샌드박스 설정 실패 / unelevated 폴백 / **Windows 오류 1385** / 폴더 권한 경고 / 네트워크 접근 문제 / 샌드박싱 깨짐 / IDE 확장 무응답
- 관련 키: `windows.sandbox`, `windows.sandbox_private_desktop`, `windows_wsl_setup_acknowledged`, `computer_use.windows.always_allowed_app_ids`
- 관련 명령: `/setup-default-sandbox`, `/sandbox-add-read-dir`
- Claude Code 대응: Windows 네이티브 샌드박스 개념 없음(macOS Seatbelt/Linux bubblewrap 기반은 있음). **elevated/unelevated 2단 폴백과 `allowed_sandbox_implementations` 엔터프라이즈 강제**는 Codex 고유.

### WSL
- URL: https://learn.chatgpt.com/codex/windows/wsl · 원문: `codex__windows__wsl.md`
- **WSL1 지원은 버전 0.114에서 종료.** Linux 샌드박스는 이제 **`bubblewrap`** 을 사용한다.
- VS Code 실행: WSL 터미널에서 `code .` → 초록 상태 바에 **"WSL: `<distro>`"** 표시 확인
- CLI 설치 (원문 그대로):
  ```
  wsl --install
  wsl
  curl -fsSL https://chatgpt.com/codex/install.sh | sh
  codex
  ```
- 모범 사례: 저장소를 **Linux 홈(`~/code/`)** 에 두고 Windows 마운트 경로(`/mnt/c/…`)는 피할 것(성능). Windows 탐색기에서는 `\\wsl$\Ubuntu\home\<user>`.
- 트러블슈팅: 저장소가 느림 → `/mnt/c` 회피, `wsl --update` / `codex` 바이너리 없음 → `which codex`
- 관련 설정: `chatgpt.runCodexInWindowsSubsystemForLinux`(IDE 확장, 기본 `false`), `windows_wsl_setup_acknowledged`
- Claude Code 대응: 설치 스크립트 `https://chatgpt.com/codex/install.sh` ↔ `https://claude.ai/install.sh`. Codex는 **WSL vs 네이티브 샌드박스를 명시적 선택지로 문서화**하고 IDE 확장 설정 키로 토글까지 노출한다.

---

## 8. 개발자 명령·설정 (Developer)

### Developer commands
- URL: https://learn.chatgpt.com/codex/developer-commands · 원문: `codex__developer-commands.md` + HTML `astro-island` 복원 표 29개
- 원문: "This page catalogs every documented Codex CLI command and flag."
- **⚠️ 수집 주의:** 이 페이지의 표 29개는 `.md` 판본에서 `<ConfigTable client:load options={globalFlagOptions} />` 형태의 **자리표시자로만 나온다.** 실제 데이터는 HTML의 `<astro-island component-export="ConfigTable" props="...">` JSON에 있다. 아래 표는 그 JSON을 디코드해 복원한 것 — **자리표시자 29개 → 복원 표 29개, 총 174행 (1:1 검증 완료).**
- 기본 원칙 (원문): "The CLI inherits most defaults from `~/.codex/config.toml`. Any `-c key=value` overrides you pass at the command line take precedence for that invocation."
- Maturity 라벨(Experimental·Beta·Stable) 해석은 https://learn.chatgpt.com/docs/feature-maturity 참조.

**안전 권고 (원문 그대로)**
- "Use `--sandbox workspace-write` for unattended local work that can stay inside the workspace, and avoid `--dangerously-bypass-approvals-and-sandbox` unless you are inside a dedicated sandbox VM."
- "When you need to grant Codex write access to more directories, prefer `--add-dir` rather than forcing `--sandbox danger-full-access`."
- "Pair `--json` with `--output-last-message` in CI to capture machine-readable progress and a final natural-language summary."

**대화형 단축키 (원문 그대로)**
- `@` 입력 → 워크스페이스 파일 검색 후 경로를 프롬프트에 추가
- **Up**/**Down** → 초안 히스토리 복원
- **Ctrl+R** → 프롬프트 히스토리 검색, **Enter**로 사용, **Esc**로 취소
- **Ctrl+O** 또는 `/copy` → 최근 완료된 Codex 출력 복사
- 줄 앞에 **`!`** → 현재 승인·샌드박스 설정 하에 로컬 셸 명령 실행
- Codex 작업 중 **Tab** → 다음 턴을 위한 후속 프롬프트·슬래시 명령·셸 명령 큐잉
- Codex 작업 중 **Enter** → 현재 턴에 새 지시 주입
- 빈 컴포저에서 **Esc 두 번** → 이전 사용자 메시지를 편집하고 **그 지점에서 채팅을 fork**
- **Ctrl+C** 또는 `/exit` → 세션 종료

**IDE 확장 명령 (원문 표 그대로)**
| Command | Default key binding | Description |
|---|---|---|
| `chatgpt.addToThread` | - | Add selected text range as context for the current chat |
| `chatgpt.addFileToThread` | - | Add the entire file as context for the current chat |
| `chatgpt.newChat` | macOS: `Cmd+N` / Windows·Linux: `Ctrl+N` | Create a new chat |
| `chatgpt.newCodexPanel` | - | Create a new Codex panel |
| `chatgpt.openCommandMenu` | - | Open the Codex command menu |
| `chatgpt.openSidebar` | - | Open the Codex sidebar panel |

키 바인딩 할당: Command Palette(**Cmd+Shift+P** / **Ctrl+Shift+P**) → **Preferences: Open Keyboard Shortcuts** → `Codex` 또는 명령 ID(예: `chatgpt.newChat`) 검색 → 연필 아이콘.

**IDE 확장 슬래시 명령 (앱 판본과 다르다 — 원문 표 그대로)**
| Slash command | Description |
|---|---|
| `/approve` | Approve one retry of a recent automatic-review denial, when automatic review is active. |
| `/cloud` | Run the chat in the cloud, when cloud execution is available. |
| `/cloud-environment` | Choose the cloud environment for the chat. |
| `/compact` | Compact the current chat's context. |
| `/fast` | Turn a catalog-provided Fast service tier on or off, when available. |
| `/feedback` | Open the feedback dialog to submit feedback and optionally include logs. |
| `/fork` | Copy a local chat into a new local chat. |
| `/goal` | Set a persistent goal for Codex to work toward. |
| `/ide-context` | Turn automatic IDE context on or off. |
| `/init` | Generate an `AGENTS.md` scaffold for the current project. |
| `/local` | Run the chat in your local workspace. |
| `/mcp` | Open MCP status to view connected servers. |
| `/memories` | Configure whether the chat can use or generate memories, when Memories is available. |
| `/model` | Choose the model for the current chat. |
| `/personality` | Choose how Codex responds, when the current model supports personalities. |
| `/plan` | Toggle plan mode for multi-step planning. |
| `/project` | Choose a project for new chats. |
| `/reasoning` | Choose the reasoning effort for the current chat. |
| `/review` | Start code review mode to review uncommitted changes or compare against a base branch. |
| `/side` | Start a temporary side chat without interrupting the main chat. |
| `/status` | Show the chat ID, context usage, and rate limits. |
| `/worktree` | Run the chat in a new Git worktree. |

**CLI TUI 내장 슬래시 명령 (원문 표 그대로 — 43개, 앱·IDE 판본보다 훨씬 많다)**
| Command | Purpose | When to use it |
|---|---|---|
| `/permissions` | Set what Codex can do without asking first. | Relax or tighten approval requirements mid-session, such as switching between Auto and Read Only. |
| `/ide` | Include open files, current selection, and other IDE context. | Pull editor context into the next prompt without re-explaining what's open in your IDE. |
| `/keymap` | Remap TUI keyboard shortcuts. | Inspect and persist custom shortcut bindings in `config.toml`. |
| `/vim` | Toggle Vim mode for the composer. | Switch between Vim normal/insert behavior and the default composer editing mode. |
| `/setup-default-sandbox` | Set up the elevated agent sandbox (Windows only). | Replace the degraded Windows sandbox after Codex offers the elevated setup. |
| `/sandbox-add-read-dir` | Grant sandbox read access to an extra directory (Windows only). | Unblock commands that need to read an absolute directory path outside the current readable roots. |
| `/agent`, `/subagents` | Switch the active agent thread. | Inspect or continue work in a spawned subagent thread. |
| `/apps` | Browse apps (connectors) and insert them into your prompt. | Attach an app as `$app-slug` before asking Codex to use it. |
| `/plugins` | Browse installed and discoverable plugins. | Inspect plugin tools, install suggested plugins, or manage plugin availability. |
| `/hooks` | View and manage lifecycle hooks. | Inspect configured hooks, trust new or changed hooks, or disable non-managed hooks before they run. |
| `/clear` | Clear the terminal and start a fresh chat. | Reset the visible UI and chat context together when you want a fresh start. |
| `/rename` | Rename the current chat. | Give a saved session a recognizable name without leaving the TUI. |
| `/archive` | Archive the current session and exit Codex. | Remove the current session from active session lists without deleting its transcript. |
| `/delete` | Permanently delete the current session and exit Codex. | Remove the transcript and descendant sessions when archiving isn't enough. |
| `/compact` | Summarize the visible chat to free tokens. | Use after long runs so Codex retains key points without blowing the context window. |
| `/copy` | Copy the latest completed Codex output. | Grab the latest finished response or plan text without manually selecting it. You can also press `Ctrl+O`. |
| `/diff` | Show the Git diff, including files Git isn't tracking yet. | Review Codex's edits before you commit or run tests. |
| `/exit` | Exit the CLI (same as `/quit`). | Alternative spelling; both commands exit the session. |
| `/experimental` | Toggle experimental features. | Enable options such as Network proxy or Prevent sleep while running. |
| `/approve` | Approve one retry of a recent auto review denial. | Retry a command or action that the auto reviewer denied. |
| `/memories` | Configure memory use and generation. | Turn memory injection or memory generation on or off without leaving the TUI. |
| `/skills` | Browse and use skills. | Improve task-specific behavior by selecting a relevant local skill. |
| `/import` | **Import Claude Code setup, project files, and recent chats.** | Migrate supported external-agent artifacts into Codex configuration and local files. |
| `/feedback` | Send logs to the Codex maintainers. | Report issues or share diagnostics with support. |
| `/init` | Generate an `AGENTS.md` scaffold in the current directory. | Capture persistent instructions for the repository or subdirectory you're working in. |
| `/logout` | Sign out of Codex. | Clear local credentials when using a shared machine. |
| `/mcp` | List configured Model Context Protocol (MCP) tools. | Check which external tools Codex can call during the session; add `verbose` for server details. |
| `/mention` | Attach a file to the chat. | Point Codex at specific files or folders you want it to inspect next. |
| `/model` | Choose the active model (and reasoning effort, when available). | Switch between models such as `gpt-5.6-luna` and `gpt-5.6-terra` before running a task. |
| `/fast` | Toggle a Fast service tier when the model catalog exposes one. | Turn the current model's Fast tier on or off and persist the selection. |
| `/plan` | Switch to plan mode and optionally send a prompt. | Ask Codex to propose an execution plan before implementation work starts. |
| `/goal` | Set, edit, pause, resume, view, or clear a task goal. | Give Codex a persistent target to track while a larger task runs. |
| `/personality` | Choose a communication style for responses. | Make Codex more concise, more explanatory, or more collaborative without changing your instructions. |
| `/ps` | Show background terminals and their recent output. | Check long-running commands without leaving the main transcript. |
| `/stop` | Stop all background terminals. | Cancel background terminal work started by the current session. |
| `/fork` | Fork the current chat into a new chat. | Branch the active session to explore a new approach without losing the current transcript. |
| `/app` | Continue the current session in the ChatGPT desktop app. | Move from the TUI to the desktop app on macOS or Windows. |
| `/side`, `/btw` | Start an ephemeral side chat. | Ask a focused follow-up without disrupting the main chat's transcript. |
| `/raw` | Toggle raw scrollback mode. | Make terminal selection and copying less formatted while reviewing long output. |
| `/resume` | Resume a saved chat from your session list. | Continue work from a previous CLI session without starting over. |
| `/new` | Start a new chat inside the same CLI session. | Reset the chat context without leaving the CLI when you want a fresh prompt in the same repo. |
| `/quit` | Exit the CLI. | Leave the session immediately. |
| `/review` | Ask Codex to review your working tree. | Run after Codex completes work or when you want a second set of eyes on local changes. |

> 문서 본문에는 위 표 외에 `/usage`(View account usage), `/debug-config`(Inspect config layers), `/statusline`(Configure footer items), `/title`(Configure terminal title items), `/theme`(Choose a syntax theme), `/pets`(Choose a terminal pet)의 개별 절도 존재한다.

**`/import` 상세 (Claude Code 사용자에게 가장 중요한 명령)**
1. `/import` 입력
2. 마이그레이션할 **Claude Code setup, project files, 또는 recent chats** 선택

> "Expected: Codex opens the external-agent import picker and imports the selected supported artifacts into Codex configuration and local files."
> "Run `/import` from a local TUI session. It's unavailable while a task is running, in remote sessions, and while connected to the local app-server daemon."

- Claude Code 대응 총괄:
  | Codex | Claude Code |
  |---|---|
  | `codex exec` | `claude -p` (headless) |
  | `codex resume` | `claude --resume` / `--continue` |
  | `codex doctor` | `claude doctor` |
  | `codex update` | `claude update` |
  | `codex mcp` / `codex mcp-server` | `claude mcp` / `claude mcp serve` |
  | `codex plugin` / `codex plugin marketplace` | `claude plugin` / `/plugin marketplace` |
  | `--add-dir` | `--add-dir` (동일) |
  | `--yolo` | `--dangerously-skip-permissions` |
  | `/compact`·`/clear`·`/init`·`/diff`·`/model`·`/vim`·`/mcp`·`/permissions`·`/resume`·`/review`·`/hooks` | 동일 이름 존재 |
  | `codex fork` / `/fork`, `/side`·`/btw`, `/raw`, `/ps`·`/stop`, `/goal`, `/personality`, `/app` | 대응물 없음 |
  | `codex sandbox` (샌드박스 안에서 임의 명령 실행) | 대응물 없음 |
  | `codex execpolicy` (규칙 파일 검증) | 대응물 없음 |
  | `codex debug models` / `debug prompt-input` | 대응물 없음 (모델 카탈로그·프롬프트 덤프) |
  | **`/import`** | **역방향 대응물 없음** — Codex만 Claude Code 설정을 가져온다 |

#### 복원한 명령·플래그 표 29개 (HTML astro-island에서 디코드, 총 174행)

**Global flags** (20행)

| Option | Type | Default | Description |
|---|---|---|---|
| `PROMPT` | string |  | Optional text instruction to start the session. Omit to launch the TUI without a pre-filled message. |
| `--image, -i` | path[,path...] |  | Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag. |
| `--model, -m` | string |  | Override the model set in configuration (for example `gpt-5.6-terra`). |
| `--oss` | boolean | false | Use a local open source model provider. Codex uses `--local-provider`, your configured `oss_provider`, or prompts you to choose between LM Studio and Ollama. |
| `--local-provider` | lmstudio \| ollama |  | Choose the local provider used with `--oss`, overriding `oss_provider` for this run. |
| `--profile, -p` | string |  | Layer `$CODEX_HOME/profile-name.config.toml` on top of the base user config. |
| `--sandbox, -s` | read-only \| workspace-write \| danger-full-access |  | Select the sandbox policy for model-generated shell commands. |
| `--ask-for-approval, -a` | untrusted \| on-request \| never |  | Control when Codex pauses for human approval before running a command. |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | boolean | false | Run every command without approvals or sandboxing. Only use inside an externally hardened environment. |
| `--dangerously-bypass-hook-trust` | boolean | false | Run enabled hooks without requiring persisted hook trust for this invocation. Intended only for automation that already vets hook sources. |
| `--cd, -C` | path |  | Set the working directory for the agent before it starts processing your request. |
| `--search` | boolean | false | Enable live web search (sets `web_search = "live"` instead of the default `"cached"`). |
| `--add-dir` | path |  | Grant additional directories write access alongside the main workspace. Repeat for multiple paths. |
| `--no-alt-screen` | boolean | false | Disable alternate screen mode for the TUI (overrides `tui.alternate_screen` for this run). |
| `--remote` | ws://host:port \| wss://host:port \| unix:// \| unix://PATH |  | Connect to a remote app-server endpoint over WebSocket or a Unix socket. Supported for `codex`, `codex resume`, `codex fork`, `codex archive`, `codex delete`, and `codex unarchive`; other subcommands reject remote mode. |
| `--remote-auth-token-env` | ENV_VAR |  | Read a bearer token from this environment variable and send it when connecting with `--remote`. Requires `--remote`; tokens are only sent over `wss://` URLs or local-only `ws://` URLs. |
| `--strict-config` | boolean | false | Error when `config.toml` contains fields this Codex version does not recognize. Supported by runtime commands such as `codex`, `exec`, `review`, `resume`, `fork`, `app-server`, `mcp-server`, and `exec-server`. |
| `--enable` | feature |  | Force-enable a feature flag (translates to `-c features.<name>=true`). Repeatable. |
| `--disable` | feature |  | Force-disable a feature flag (translates to `-c features.<name>=false`). Repeatable. |
| `--config, -c` | key=value |  | Override configuration values. Values parse as TOML if possible; otherwise the literal string is used. |

**Command overview** (28행)

| Option | Type | Description |
|---|---|---|
| `codex` | stable | Launch the terminal UI. Accepts the global flags above plus an optional prompt or image attachments. |
| `codex app-server` | experimental | Launch the Codex app server for local development or debugging over stdio, WebSocket, or a Unix socket. |
| `codex remote-control` | experimental | Run or manage remote control for the local app-server, or create a short-lived pairing code. |
| `codex app` | stable | Launch the ChatGPT desktop app on macOS or Windows. On macOS, Codex can open a workspace path; on Windows, Codex prints the path to open. |
| `codex debug app-server send-message-v2` | experimental | Debug app-server by sending a single V2 message through the built-in test client. |
| `codex debug models` | experimental | Print the raw model catalog Codex sees, including an option to inspect only the bundled catalog. |
| `codex debug prompt-input` | experimental | Render the model-visible prompt input list as JSON, optionally with a prompt and images. |
| `codex apply` | stable | Apply the latest diff generated by a Codex cloud chat to your local working tree. Alias: `codex a`. |
| `codex review` | stable | Run a non-interactive review of uncommitted changes, a base branch diff, a commit, or custom review instructions. |
| `codex archive` | stable | Archive a saved interactive session by session ID or session name. |
| `codex delete` | stable | Permanently delete a saved interactive session by session ID or session name. |
| `codex cloud` | experimental | Browse or execute Codex cloud chats from the terminal without opening the TUI. Alias: `codex cloud-tasks`. |
| `codex completion` | stable | Generate shell completion scripts for Bash, Zsh, Fish, or PowerShell. |
| `codex doctor` | stable | Generate a diagnostic report for local installation, config, auth, runtime, Git, terminal, app-server, and thread inventory issues. |
| `codex features` | stable | List feature flags and persistently enable or disable them in `config.toml`. |
| `codex exec` | stable | Run Codex non-interactively. Alias: `codex e`. Stream results to stdout or JSONL and optionally resume previous sessions. |
| `codex execpolicy` | experimental | Evaluate execpolicy rule files and see whether a command would be allowed, prompted, or blocked. |
| `codex login` | stable | Authenticate Codex using ChatGPT OAuth, device auth, an API key, or an access token piped over stdin. |
| `codex logout` | stable | Remove stored authentication credentials. |
| `codex mcp` | stable | Manage Model Context Protocol servers (list, add, remove, authenticate). |
| `codex plugin marketplace` | stable | Add, list, upgrade, or remove plugin marketplaces from Git or local sources. |
| `codex plugin` | stable | Install, list, and remove plugins from configured marketplace sources. |
| `codex mcp-server` | stable | Run Codex itself as an MCP server over stdio. Useful when another agent consumes Codex. |
| `codex resume` | stable | Continue a previous interactive session by ID or resume the most recent chat. |
| `codex fork` | stable | Fork a previous interactive session into a new chat, preserving the original transcript. |
| `codex sandbox` | stable | Run arbitrary commands inside Codex-provided macOS, Linux, or Windows sandboxes. |
| `codex update` | stable | Check for and apply a Codex CLI update when the installed release supports self-update. |
| `codex unarchive` | stable | Restore an archived interactive session by session ID or session name. |

**`codex app-server`** (10행)

| Option | Type | Default | Description |
|---|---|---|---|
| `--stdio` | boolean | false | Use stdio transport. Equivalent to `--listen stdio://` and mutually exclusive with `--listen`. |
| `--listen` | stdio:// \| ws://IP:PORT \| unix:// \| unix://PATH \| off | stdio:// | Transport listener URL. Use `stdio://` for JSONL, `ws://IP:PORT` for a TCP WebSocket endpoint, `unix://` for the default Unix socket, `unix://PATH` for a custom Unix socket, or `off` to disable the local transport. |
| `--ws-auth` | capability-token \| signed-bearer-token |  | Authentication mode for app-server WebSocket clients. If omitted, WebSocket auth is disabled; non-local listeners warn during startup. |
| `--ws-token-file` | absolute path |  | File containing the shared capability token. Use with `--ws-auth capability-token` unless you provide `--ws-token-sha256` instead. |
| `--ws-token-sha256` | hexadecimal SHA-256 digest |  | Expected SHA-256 digest for capability-token authentication. Use instead of `--ws-token-file` when the client token comes from another source. |
| `--ws-shared-secret-file` | absolute path |  | File containing the HMAC shared secret used to validate signed JWT bearer tokens. Required with `--ws-auth signed-bearer-token`. |
| `--ws-issuer` | string |  | Expected `iss` claim for signed bearer tokens. Requires `--ws-auth signed-bearer-token`. |
| `--ws-audience` | string |  | Expected `aud` claim for signed bearer tokens. Requires `--ws-auth signed-bearer-token`. |
| `--ws-max-clock-skew-seconds` | number | 30 | Clock skew allowance when validating signed bearer token `exp` and `nbf` claims. Requires `--ws-auth signed-bearer-token`. |
| `--analytics-default-enabled` | boolean | false | Defaults analytics to enabled for first-party app-server clients unless the user opts out in config. |

**`codex app`** (2행)

| Option | Type | Default | Description |
|---|---|---|---|
| `PATH` | path | . | Workspace path for the ChatGPT desktop app. On macOS, Codex opens this path; on Windows, Codex prints the path. |
| `--download-url` | url |  | Advanced override for the ChatGPT desktop app installer URL used during install. |

**`codex debug app-server send-message-v2`** (1행)

| Option | Type | Description |
|---|---|---|
| `USER_MESSAGE` | string | Message text sent to app-server through the built-in V2 test-client flow. |

**`codex debug models`** (1행)

| Option | Type | Default | Description |
|---|---|---|---|
| `--bundled` | boolean | false | Skip refresh and print only the model catalog bundled with the current Codex binary. |

**`codex debug prompt-input`** (2행)

| Option | Type | Description |
|---|---|---|
| `PROMPT` | string | Optional user prompt appended after the session context. |
| `--image, -i` | path[,path...] | Attach one or more images to the user prompt. Separate multiple paths with commas or repeat the flag. |

**`codex apply`** (1행)

| Option | Type | Description |
|---|---|---|
| `TASK_ID` | string | Identifier of the Codex cloud chat whose diff should be applied. |

**`codex review`** (6행)

| Option | Type | Default | Description |
|---|---|---|---|
| `PROMPT` | string \| - (read stdin) |  | Custom review instructions. Use `-` to read the instructions from stdin. |
| `--uncommitted` | boolean | false | Review staged, unstaged, and untracked changes. |
| `--base` | branch |  | Review changes against the specified base branch. |
| `--commit` | SHA |  | Review the changes introduced by the specified commit. |
| `--title` | string |  | Set the commit title shown in the review summary. Requires `--commit`. |
| `--strict-config` | boolean | false | Error when `config.toml` contains fields this Codex version does not recognize. |

**`codex archive` and `codex unarchive`** (3행)

| Option | Type | Description |
|---|---|---|
| `SESSION` | session ID \| session name | Saved session to archive or restore. Session IDs take precedence over session names. |
| `--remote` | ws://host:port \| wss://host:port \| unix:// \| unix://PATH | Connect to a remote app-server endpoint before changing archive state. |
| `--remote-auth-token-env` | ENV_VAR | Read a bearer token from this environment variable when `--remote` requires authentication. |

**`codex delete`** (4행)

| Option | Type | Default | Description |
|---|---|---|---|
| `SESSION` | session ID \| session name |  | Saved session to delete. Session IDs take precedence over session names. |
| `--force` | boolean | false | Delete without prompting. The session argument must be a UUID; names still require interactive confirmation. |
| `--remote` | ws://host:port \| wss://host:port \| unix:// \| unix://PATH |  | Connect to a remote app-server endpoint before deleting the session. |
| `--remote-auth-token-env` | ENV_VAR |  | Read a bearer token from this environment variable when `--remote` requires authentication. |

**`codex cloud`** (3행)

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Task prompt. If omitted, Codex prompts interactively for details. |
| `--env` | ENV_ID |  | Target Codex cloud environment identifier (required). Use `codex cloud` to list options. |
| `--attempts` | 1-4 | 1 | Number of assistant attempts (best-of-N) Codex cloud should run. |

**`codex cloud list`** (4행)

| Option | Type | Default | Description |
|---|---|---|---|
| `--env` | ENV_ID |  | Filter tasks by environment identifier. |
| `--limit` | 1-20 | 20 | Maximum number of tasks to return. |
| `--cursor` | string |  | Pagination cursor returned by a previous request. |
| `--json` | boolean | false | Emit machine-readable JSON instead of plain text. |

**`codex completion`** (1행)

| Option | Type | Default | Description |
|---|---|---|---|
| `SHELL` | bash \| zsh \| fish \| power-shell \| elvish | bash | Shell to generate completions for. Output prints to stdout. |

**`codex doctor`** (5행)

| Option | Type | Default | Description |
|---|---|---|---|
| `--json` | boolean | false | Emit a redacted machine-readable support report. |
| `--summary` | boolean | false | Show grouped check rows and the final count summary only. |
| `--all` | boolean | false | Expand long lists in the detailed human-readable report. |
| `--no-color` | boolean | false | Disable ANSI color in human-readable output. |
| `--ascii` | boolean | false | Use ASCII status labels and separators in human-readable output. |

**`codex features`** (3행)

| Option | Type | Description |
|---|---|---|
| `List subcommand` | codex features list | Show known feature flags, their maturity stage, and their effective state. |
| `Enable subcommand` | codex features enable <feature> | Persistently enable a feature flag in `$CODEX_HOME/config.toml`. |
| `Disable subcommand` | codex features disable <feature> | Persistently disable a feature flag in `$CODEX_HOME/config.toml`. |

**`codex exec` (표 1)** (21행)

| Option | Type | Default | Description |
|---|---|---|---|
| `PROMPT` | string \| - (read stdin) |  | Initial instruction for the task. Use `-` to pipe the prompt from stdin. |
| `--image, -i` | path[,path...] |  | Attach images to the first message. Repeatable; supports comma-separated lists. |
| `--model, -m` | string |  | Override the configured model for this run. |
| `--oss` | boolean | false | Use a local open source provider. Codex uses `--local-provider` or your configured `oss_provider`, and exits with an error if neither is set. |
| `--local-provider` | lmstudio \| ollama |  | Choose the local provider used with `--oss`, overriding `oss_provider` for this run. |
| `--sandbox, -s` | read-only \| workspace-write \| danger-full-access |  | Sandbox policy for model-generated commands. Defaults to configuration. |
| `--profile, -p` | string |  | Layer `$CODEX_HOME/profile-name.config.toml` on top of the base user config. |
| `--full-auto` | boolean | false | Deprecated compatibility flag. Prefer `--sandbox workspace-write`; Codex prints a warning when this flag is used. |
| `--dangerously-bypass-approvals-and-sandbox, --yolo` | boolean | false | Bypass approval prompts and sandboxing. Dangerous—only use inside an isolated runner. |
| `--dangerously-bypass-hook-trust` | boolean | false | Run enabled hooks without requiring persisted hook trust for this invocation. Intended only for automation that already vets hook sources. |
| `--cd, -C` | path |  | Set the workspace root before executing the task. |
| `--skip-git-repo-check` | boolean | false | Allow running outside a Git repository (useful for one-off directories). |
| `--ephemeral` | boolean | false | Run without persisting session rollout files to disk. |
| `--ignore-user-config` | boolean | false | Do not load `$CODEX_HOME/config.toml`. Authentication still uses `CODEX_HOME`. |
| `--ignore-rules` | boolean | false | Do not load user or project execpolicy `.rules` files for this run. |
| `--output-schema` | path |  | JSON Schema file describing the expected final response shape. Codex validates tool output against it. |
| `--color` | always \| never \| auto | auto | Control ANSI color in stdout. |
| `--json, --experimental-json` | boolean | false | Print newline-delimited JSON events instead of formatted text. |
| `--output-last-message, -o` | path |  | Write the assistant’s final message to a file. Useful for downstream scripting. |
| `Resume subcommand` | codex exec resume [SESSION_ID] |  | Resume an exec session by ID or add `--last` to continue the most recent session from the current working directory. Add `--all` to consider sessions from any directory. Accepts an optional follow-up prompt. |
| `-c, --config` | key=value |  | Inline configuration override for the non-interactive run (repeatable). |

**`codex exec` (표 2)** (5행)

| Option | Type | Default | Description |
|---|---|---|---|
| `SESSION_ID` | uuid \| session name |  | Resume the specified session. Omit and use `--last` to continue the most recent session. |
| `--last` | boolean | false | Resume the most recent chat from the current working directory. |
| `--all` | boolean | false | Include sessions outside the current working directory when selecting the most recent session. |
| `--image, -i` | path[,path...] |  | Attach one or more images to the follow-up prompt. Separate multiple paths with commas or repeat the flag. |
| `PROMPT` | string \| - (read stdin) |  | Optional follow-up instruction sent immediately after resuming. |

**`codex execpolicy`** (3행)

| Option | Type | Default | Description |
|---|---|---|---|
| `--rules, -r` | path (repeatable) |  | Path to an execpolicy rule file to evaluate. Provide multiple flags to combine rules across files. |
| `--pretty` | boolean | false | Pretty-print the JSON result. |
| `COMMAND...` | var-args |  | Command to be checked against the specified policies. |

**`codex login`** (4행)

| Option | Type | Description |
|---|---|---|
| `--with-api-key` | boolean | Read an API key from stdin (for example `printenv OPENAI_API_KEY \| codex login --with-api-key`). |
| `--with-access-token` | boolean | Read an access token from stdin (for example `printenv CODEX_ACCESS_TOKEN \| codex login --with-access-token`). |
| `--device-auth` | boolean | Use OAuth device code flow instead of launching a browser window. |
| `status subcommand` | codex login status | Print the active authentication mode and exit with 0 when logged in. |

**`codex mcp` (표 1)** (6행)

| Option | Type | Description |
|---|---|---|
| `list` | --json | List configured MCP servers. Add `--json` for machine-readable output. |
| `get <name>` | --json | Show a specific server configuration. `--json` prints the raw config entry. |
| `add <name>` | -- <command...> \| --url <value> | Register a server using a stdio launcher command or a streamable HTTP URL. Supports `--env KEY=VALUE` for stdio transports. |
| `remove <name>` |  | Delete a stored MCP server definition. |
| `login <name>` | --scopes scope1,scope2 | Start an OAuth login for a streamable HTTP server (servers that support OAuth only). |
| `logout <name>` |  | Remove stored OAuth credentials for a streamable HTTP server. |

**`codex mcp` (표 2)** (6행)

| Option | Type | Description |
|---|---|---|
| `COMMAND...` | stdio transport | Executable plus arguments to launch the MCP server. Provide after `--`. |
| `--env KEY=VALUE` | repeatable | Environment variable assignments applied when launching a stdio server. |
| `--url` | https://… | Register a streamable HTTP server instead of stdio. Mutually exclusive with `COMMAND...`. |
| `--bearer-token-env-var` | ENV_VAR | Environment variable whose value is sent as a bearer token when connecting to a streamable HTTP server. |
| `--oauth-client-id` | CLIENT_ID | OAuth client identifier for a streamable HTTP MCP server. Requires `--url`. |
| `--oauth-resource` | RESOURCE | OAuth resource parameter to include during login for a streamable HTTP MCP server. Requires `--url`. |

**`codex plugin`** (4행)

| Option | Type | Description |
|---|---|---|
| `add <plugin[@marketplace]>` | [--marketplace, -m NAME] [--json] | Install a plugin from a configured marketplace. Use `--marketplace` or `-m` when the plugin argument omits `@marketplace`. |
| `list` | [--marketplace, -m NAME] [--available --json] [--json] | List installed plugins. With `--json`, output has `installed` and `available` arrays; `--available` includes uninstalled marketplace plugins and requires `--json`. |
| `remove <plugin[@marketplace]>` | [--marketplace, -m NAME] [--json] | Remove an installed plugin from local config and cache. Use `--json` for automation-friendly output. |
| `marketplace` |  | Manage configured marketplace sources. See `codex plugin marketplace` below. |

**`codex plugin marketplace`** (4행)

| Option | Type | Description |
|---|---|---|
| `add <source>` | [--ref REF] [--sparse PATH] [--json] | Install a plugin marketplace from GitHub shorthand, a Git URL, an SSH URL, or a local marketplace root directory. `--sparse` is supported only for Git sources and can be repeated. |
| `list` | [--json] | Show plugin marketplaces Codex is currently considering and the root path for each marketplace. |
| `upgrade [marketplace-name]` | [--json] | Refresh one configured Git marketplace, or all configured Git marketplaces when no name is provided. |
| `remove <marketplace-name>` | [--json] | Remove a configured plugin marketplace. |

**`codex resume`** (4행)

| Option | Type | Default | Description |
|---|---|---|---|
| `SESSION_ID` | uuid \| session name |  | Resume the specified session. Omit and use `--last` to continue the most recent session. |
| `--last` | boolean | false | Skip the picker and resume the most recent chat from the current working directory. |
| `--all` | boolean | false | Include sessions outside the current working directory when selecting the most recent session. |
| `--include-non-interactive` | boolean | false | Include non-interactive sessions in the picker and `--last` selection. |

**`codex fork`** (3행)

| Option | Type | Default | Description |
|---|---|---|---|
| `SESSION_ID` | uuid |  | Fork the specified session. Omit and use `--last` to fork the most recent session. |
| `--last` | boolean | false | Skip the picker and fork the most recent chat automatically. |
| `--all` | boolean | false | Show sessions beyond the current working directory in the picker. |

**macOS seatbelt** (8행)

| Option | Type | Default | Description |
|---|---|---|---|
| `--profile, -p` | NAME |  | Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config. |
| `--permission-profile, -P` | NAME |  | Apply a named permissions profile from the active configuration stack. |
| `--cd, -C` | DIR |  | Working directory used for profile resolution and command execution. Requires `--permission-profile`. |
| `--include-managed-config` | boolean | false | Include managed requirements while resolving an explicit permissions profile. Requires `--permission-profile`. |
| `--allow-unix-socket` | path |  | Allow the sandboxed command to bind or connect Unix sockets rooted at this path. Repeat to allow multiple paths. |
| `--log-denials` | boolean | false | Capture macOS sandbox denials with `log stream` while the command runs and print them after exit. |
| `--config, -c` | key=value |  | Pass configuration overrides into the sandboxed run (repeatable). |
| `COMMAND...` | var-args |  | Shell command to execute under macOS Seatbelt. Everything after `--` is forwarded. |

**Linux Landlock** (6행)

| Option | Type | Default | Description |
|---|---|---|---|
| `--profile, -p` | NAME |  | Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config. |
| `--permission-profile, -P` | NAME |  | Apply a named permissions profile from the active configuration stack. |
| `--cd, -C` | DIR |  | Working directory used for profile resolution and command execution. Requires `--permission-profile`. |
| `--include-managed-config` | boolean | false | Include managed requirements while resolving an explicit permissions profile. Requires `--permission-profile`. |
| `--config, -c` | key=value |  | Configuration overrides applied before launching the sandbox (repeatable). |
| `COMMAND...` | var-args |  | Command to execute under Landlock + seccomp. Provide the executable after `--`. |

**Windows** (6행)

| Option | Type | Default | Description |
|---|---|---|---|
| `--profile, -p` | NAME |  | Layer `$CODEX_HOME/NAME.config.toml` on top of the base user config. |
| `--permission-profile, -P` | NAME |  | Apply a named permissions profile from the active configuration stack. |
| `--cd, -C` | DIR |  | Working directory used for profile resolution and command execution. Requires `--permission-profile`. |
| `--include-managed-config` | boolean | false | Include managed requirements while resolving an explicit permissions profile. Requires `--permission-profile`. |
| `--config, -c` | key=value |  | Configuration overrides applied before launching the sandbox (repeatable). |
| `COMMAND...` | var-args |  | Command to execute under the native Windows sandbox. Provide the executable after `--`. |
### Developer settings
- URL: https://learn.chatgpt.com/codex/developer-settings · 원문: `codex__developer-settings.md`
- 설정 영역: 프로젝트·터미널 동작(파일 열기 위치, 명령 출력 표시량, 터미널 탭 기본 위치) / 코드 리뷰(Git 설정에서 **inline** 또는 **detached**) / IDE 확장 동기화(데스크톱 앱과 활성 채팅·에디터 컨텍스트 공유) / Agent 구성(`config.toml`) / Git 설정(브랜치 명명 표준화, force push, 커밋 메시지·PR 설명 프롬프트) / 통합·MCP / 브라우저 개발자 모드

**IDE 확장 설정 표 (원문 그대로, 10개 전수)**
| Setting | Default | Description |
|---|---|---|
| `chatgpt.commentCodeLensEnabled` | `true` | Show CodeLens above `TODO` comments so Codex can address them. |
| `chatgpt.openOnStartup` | `false` | Focus the Codex sidebar when the extension finishes starting. |
| `chatgpt.followUpQueueMode` | `queue` | Choose message queuing behavior (`queue` or `steer`); legacy `interrupt` treated as `steer` |
| `chatgpt.composerEnterBehavior` | `enter` | Choose whether Enter always sends (`enter`), Cmd/Ctrl+Enter sends multiline prompts (`cmdIfMultiline`), or the modifier is always required (`cmdAlways`). |
| `chatgpt.reviewDelivery` | `inline` | Run `/review` in the current chat when possible (`inline`) or start a separate review chat (`detached`). |
| `chatgpt.localeOverride` | Auto | Set the preferred language for the Codex UI. Leave empty to detect it automatically. |
| `chatgpt.runCodexInWindowsSubsystemForLinux` | `false` | Windows only: Run Codex in WSL when WSL is available. |
| `chatgpt.cliExecutable` | Unset | Development only path setting for Codex CLI executable |
| `chat.fontSize` | Editor default | Control chat text in the Codex sidebar, including chat content and the composer. |
| `chat.editor.fontSize` | Editor default | Control code-rendered content in Codex chats, including code snippets and diffs. |

- 언급된 `config.toml` 키: `model`, `model_reasoning_effort`, `personality`, `[tui]` 하위 `vim_mode_default`·`raw_output_mode`
- 브라우저 개발자 모드 (원문): "Under **Developer mode**, turn on **Enable full CDP access** to let ChatGPT use the Chrome DevTools Protocol for performance profiling and deeper browser debugging."
- Claude Code 대응: `chatgpt.*` VS Code 설정 ↔ Claude Code VS Code 확장 설정. **`chatgpt.followUpQueueMode`(queue/steer)** 는 Claude Code의 "메시지 큐잉 vs 현재 실행 조정"과 같은 문제를 **명시적 설정 키로 노출**한다(데스크톱 앱 "Follow-up behavior" 설정과 짝). `Enable full CDP access` ↔ chrome-devtools MCP.

---

## 수집 검증 요약

| 항목 | 결과 |
|---|---|
| 지정 URL | 34 |
| 성공 | **34** |
| 실패 | **0** |
| 수집 방식 | `{경로}.md` 원문 markdown (curl) — 전 34건 HTTP 200 |
| 원문 보존 | `research/codex-docs-raw/` 34개 파일 (약 604 KB) |
| `ConfigTable` 자리표시자 총 개수 | **31** (config-reference 2 + developer-commands 29) |
| 복원한 표 개수 | **31** (config-reference 2 = 390행 / developer-commands 29 = 174행) |
| 복원 검증 | config-reference: 인라인 `key:` 390개 = 표 행 390개 ✅ / developer-commands: 자리표시자 29개 = astro-island 29개 = 복원 표 29개 ✅ |
| 그 외 32개 파일 | `options={변수}` 형태 외부참조 자리표시자 **없음** (`FileTree`·`ContentModeSwitch` 등은 데이터가 인라인) |

## 접근 실패 URL

**없음 (34/34 성공).**

## 수집 한계·주의 (인용 시 확인 필요)

| 항목 | 내용 |
|---|---|
| `/codex/artifacts-viewer` | 실제 페이지 제목은 **"Work with files"**. "Artifacts viewer"라는 제목은 문서상 존재하지 않는다 (원문 H1으로 확정) |
| `/codex/agent-configuration/speed` | 원문 전문이 1.8 KB로 매우 짧다. 모델별 비교 표나 Codex-Spark의 구체 배수 수치는 **문서에 없다** |
| reasoning effort 값 불일치 | config-sample·config-basic은 `minimal\|low\|medium\|high\|xhigh`, subagents는 여기에 `ultra`·`max` 추가. **어느 페이지 기준인지 명시할 것** |
| WSL 경로 성능 권고 충돌 | windows-app은 "Windows 파일시스템에 두고 `/mnt/`로 접근", wsl은 "Linux 홈 `~/code/`에 두고 `/mnt/c/` 회피". **전제(네이티브 실행 vs WSL 내부 실행)가 달라 보이나 문서가 명시하지 않는다** |
| `/codex/extend/mcp` | resources·prompts·sampling을 별도 설정 요소로 다루지 않는다 (문서에 없음) |
| `developer-commands` 표 | `.md` 판본에는 데이터가 없다. 본 문서의 표는 HTML astro-island에서 복원한 것 — 재검증 시 `.md`가 아니라 **HTML**을 받아야 한다 |
| hooks 스키마 | GitHub `main` 브랜치 스키마에는 현재 릴리스에 없는 필드가 있을 수 있다. 문서가 "Use this page as the release behavior reference"라고 명시 |

## 추가 발견 URL

`llms.txt` 색인 기준 전체 문서는 **134개**이며, 내 담당 34개를 뺀 **100개**가 미방문이다.

**그룹 B 주제와 직접 인접해 후속 수집 가치가 높은 것 (우선순위 순)**
- `/docs/permissions` — 베타 permission 프로필 (config-reference의 `permissions.<name>.*` 키 설명 원본)
- `/docs/permission-modes` — `permission_mode` 값(`default`/`acceptEdits`/`plan`/`dontAsk`/`bypassPermissions`)의 정의
- `/docs/agent-approvals-security` — sandbox·approvals, protected paths in writable roots, network access (config-reference가 반복 참조)
- `/docs/sandboxing`, `/docs/sandboxing/auto-review` — `[auto_review]` 정책의 원본
- `/docs/enterprise/managed-configuration` — `requirements.toml` admin-enforced requirements 상세
- `/docs/import` — `/import`(Claude Code 설정 가져오기)의 전용 문서
- `/docs/feature-maturity` — Experimental/Beta/Stable 라벨 정의
- `/docs/skills-and-plugins`, `/docs/plugins` — 스킬·플러그인 사용자 관점 문서
- `/docs/models` — 모델 카탈로그 (모델명·수치 대조용)
- `/docs/pricing` — 요금·크레딧 (Fast mode 배수 대조용)
- `/docs/personalize`, `/docs/notifications`, `/docs/pets`
- `/docs/config-schema.json` — **`config.toml` 공식 JSON 스키마** (설정 키 검증 1차 근거)
- `/codex/cloud/internet-access` — 클라우드 네트워크 경계

**그 외 미방문 (다른 그룹 담당으로 추정)**
administration · amazon-bedrock · app · app-server · auth · automations · browser · changelog · cli · cloud · code-review · codex-sdk · computer-use · cyber-safety · developers · enterprise/{access-tokens, admin-setup, analytics-api, apps-and-connectors, compliance-api, governance, groups-and-provisioning, roles-and-workspace-permissions, skills, windows-deployment, work-admin-faq, workspace-analytics, workspace-model-availability} · environments/{cloud-environment, git-worktrees, local-environment, modes} · features · features/{codex-micro, voice} · get-started-with-work · github-action · glossary · hipaa-configuration · ide · integrated-terminal · long-running-work · mcp-server · non-interactive-mode · open-source · projects · prompting · quickstart · remote-connections · resources · security · security-administration · security/{cli, cli/bulk-scans, cli/ci, cli/faq, cli/reference, faq, plugin, plugin/*, sdk, setup, threat-model} · sites · third-party/{github, linear, slack} · use-cases · use-cases/collections · use-chatgpt · videos · visualizations · web · whats-new

**문서 본문에서 참조된 외부 URL**
- https://developers.openai.com/plugins/ (concepts/plugins · build/skills · build/mcp-server · build/chatgpt-ui · build/plugins · deploy/connect-chatgpt · deploy/submission)
- https://developers.openai.com/mcp — OpenAI Docs MCP 서버 엔드포인트
- https://github.com/openai/codex/issues · /issues/new — 이슈 트래커
- https://github.com/openai/codex/tree/main/codex-rs/hooks/schema/generated — hooks wire format 스키마
- https://chatgpt.com/codex/install.sh — CLI 설치 스크립트
- https://research.trychroma.com/context-rot — subagents 문서가 인용하는 context rot 리서치
