# 그룹 B: 기능·레퍼런스·설정·커스터마이징 (34 URL) — 검색 2026-08-02 기준

<!-- 검색 시점: 2026-08-02 기준 -->
<!-- 출처: OpenAI Codex 공식 문서 https://learn.chatgpt.com -->
<!-- 신뢰성: 전 항목 "최상" (공식 1차 문서). 버전·수치는 2026-08-02 문서 스냅샷 기준이며 빠르게 변할 수 있음 -->

> **원장 사용 안내 (fact-checker용):** 이 문서의 설정 키·명령어·수치는 모두 `learn.chatgpt.com` 공식 문서에서 직접 인용했다. 각 항목의 URL이 대조 기준이다. 문서에 없는 내용은 기록하지 않았다. 일부 페이지는 WebFetch 요약 과정에서 원문 문장이 축약되었을 수 있으며, 그런 경우 "원문 확인 권장" 표시를 남겼다.

---

## 1. 기능 확장 (Feature)

### Web search
- URL: https://learn.chatgpt.com/codex/web-search
- 검색: 2026-08-02 기준
- 핵심 내용: ChatGPT/Codex 전 표면(데스크톱 앱·웹·CLI·IDE 확장)에 내장된 웹 검색 도구. 로컬 Codex는 **기본적으로 캐시된 검색(cached)** 을 사용한다 — 임의 페이지를 라이브로 가져오는 대신 OpenAI가 관리하는 인덱스를 쓴다. 워크스페이스 설정으로 웹 검색 가용성이 제한될 수 있다.
- 명령·플래그·설정 키:
  - CLI 플래그: `--search` — 단일 실행에서 라이브 웹 검색을 켠다.
  - `config.toml` 키: `web_search` (값 4종)
    | 값 | 의미 (문서 원문 기반) |
    |---|---|
    | `"cached"` | **로컬 Codex 기본값.** "an OpenAI-maintained index instead of fetching arbitrary pages live, which lowers—but doesn't remove—prompt injection risk" |
    | `"indexed"` | 검색 인덱스가 요청을 게이트할 때만 외부 웹 접근 허용 |
    | `"live"` | 최신 정보가 필요할 때 임의 페이지를 라이브로 가져옴 (`--search`와 동일) |
    | `"disabled"` | 도구 비활성화 |
- 코드/설정 예시:
  ```
  codex --search "Summarize the latest release notes for this dependency"
  ```
- 제약·주의사항:
  - "All web results should be treated as untrusted input." — 웹 결과는 전부 신뢰할 수 없는 입력으로 취급하라 (프롬프트 인젝션).
  - 검색 활동은 트랜스크립트에 다른 도구 호출과 나란히 기록된다. `codex exec --json` 출력에는 `web_search` 항목으로 나타난다.
  - 클라우드 환경의 네트워크 경계는 별도 정책(`/codex/cloud/internet-access`)을 따른다.
  - **중요 상호작용:** `--yolo`(full access 샌드박스)를 쓰면 web search 기본값이 `live`로 바뀐다 (출처: config-sample 주석).
- Claude Code 대응 관점 메모: Claude Code의 WebSearch/WebFetch 도구와 대응. 다만 Codex는 "캐시 인덱스 기본 + 라이브는 옵트인"이라는 **보안 등급 다이얼**을 설정 키 하나(`web_search`)로 노출한다는 점이 구조적 차이다.

---

### Image generation
- URL: https://learn.chatgpt.com/codex/image-generation
- 검색: 2026-08-02 기준
- 핵심 내용: 앱 컴포저·웹 채팅·CLI 세션·확장 채팅에서 이미지를 생성·편집한다. 참조 이미지를 붙여 기존 이미지를 편집할 수 있다.
- 명령·플래그·설정 키:
  - `$imagegen` — 스킬을 명시적으로 호출. 원문: "Include `$imagegen` in your prompt to invoke the image generation skill explicitly."
  - CLI: `-i` / `--image` — 참조 이미지 첨부. 원문: "Attach an existing image with `-i` or `--image` when it should guide the result."
- 수치·모델명·버전 (**2026-08 문서 기준**):
  - 모델: **`gpt-image-2`** — 원문: "Built-in image generation uses `gpt-image-2`"
  - 사용량: "Image generations use included limits **3–5x faster on average** than similar turns without image generation" (품질·크기에 따라 다름)
  - "Image availability and usage limits in ChatGPT web depend on your plan and workspace settings."
- 코드/설정 예시: 페이지 본문에 코드 블록 없음 (플래그 표기만).
- 제약·주의사항: 일반 Codex 사용 한도에 포함된다. 실존 인물 묘사 시 참조 사진 제공 + 허가 확인 필요.
- 프롬프트 모범 사례(문서 요약): 1~3문장, 목적/대상, 주체와 동작, 배경·구도·시각 스타일, 프레이밍·조명·색·재질, 등장시키지 말 것에 대한 제약. 다중 참조는 콘텐츠용/스타일용 이미지를 분리. 텍스트 삽입은 따옴표 안에 정확한 문구 + 폰트 지정. 인포그래픽은 정보 위계를 서술하고 라벨은 짧게.
- Claude Code 대응 관점 메모: Claude Code에는 대응하는 내장 이미지 생성 도구가 없다(MCP/플러그인 경유). `$imagegen`의 `$` 접두어는 Codex의 **스킬 명시 호출 문법**으로, Claude Code의 Skill 도구 호출과 대응하는 개념.

---

### Image inputs
- URL: https://learn.chatgpt.com/codex/image-inputs
- 검색: 2026-08-02 기준
- 핵심 내용: 스크린샷·다이어그램·시각 참조를 프롬프트에 첨부. 에러 스크린샷, UI 디자인, 아키텍처 다이어그램, 기존 에셋처럼 **시각 컨텍스트에 의존하는 작업**에 쓴다.
- 명령·플래그: CLI `-i`, `--image` (쉼표 구분 다중 경로 또는 `--image` 반복)
- 코드/설정 예시:
  ```
  codex -i screenshot.png "Explain this error and suggest the smallest fix"
  codex --image before.png,after.png "Compare these states and list the regressions"
  ```
- 표면별 첨부 방법:
  | 표면 | 방법 |
  |---|---|
  | 데스크톱 앱 | Shift를 누른 채 컴포저로 이미지 드래그 |
  | 웹 | 컴포저에 첨부·붙여넣기·드래그 |
  | CLI | `-i` / `--image` |
  | Chrome 확장 | Shift를 누른 채 컴포저로 드래그 (에디터로 넘어가지 않게) |
- 제약·주의사항: PNG·JPEG 등 일반 이미지 포맷 지원. "don't rely on the image alone to communicate the task" — 이미지만으로 과제를 전달하지 말고 무엇을 검사하고 무엇을 원하는지 문장으로 쓸 것. 여러 장이면 각각을 지칭하고 비교 방법을 설명.
- 문서 예시 프롬프트(원문): "Compare this checkout screen with the design. Fix spacing and typography only; do not change behavior. Verify the result with a new screenshot."
- Claude Code 대응 관점 메모: Claude Code의 Read 도구 이미지 읽기 / 클립보드 붙여넣기와 대응. Codex는 CLI 진입 플래그(`-i`)로 초기 프롬프트에 이미지를 다는 경로를 표준화했다.

---

### Appshots
- URL: https://learn.chatgpt.com/codex/appshots
- 검색: 2026-08-02 기준
- 핵심 내용: **macOS 데스크톱 앱 전용.** 최전면 앱 창을 캡처해 ChatGPT에 컨텍스트로 넘긴다.
- 캡처 대상 2가지:
  1. 보이는 창의 이미지
  2. 그 창에서 얻을 수 있는 텍스트 — **화면 밖(off-screen) 텍스트 포함**(앱이 접근성 API로 노출하는 범위)
- 명령·단축키: **양쪽 Command 키를 동시에 누름** (커스텀 핫키 설정 가능)
- 동작 규칙 (수치 포함): 기본적으로 appshot은 **새 채팅**을 시작한다. 단 **60초 이내**에 어떤 채팅과 상호작용했다면 그 기존 대화에 추가된다.
- 필요 권한 (macOS):
  | 권한 | 용도 |
  |---|---|
  | Screen & System Audio Recording | 창 캡처 |
  | Accessibility | 최전면 창의 사용 가능 텍스트 읽기 |
- 제약·주의사항: macOS 데스크톱 앱에서만 동작. **CLI에서는 사용 불가.** 일부 앱(Google Docs, Gmail, Sheets, Slides)은 전체 문서 텍스트 없이 보이는 스크린샷만 제공할 수 있다.
- 사용 사례: API 레퍼런스 페이지를 보여주고 스크립트 생성 요청, 메일·캘린더 화면 공유, 디자인 도구·에러 메시지처럼 말로 설명하기보다 보여주는 게 쉬운 것.
- Claude Code 대응 관점 메모: Claude Code에 직접 대응 기능 없음. 가장 가까운 것은 claude-in-chrome MCP의 스크린샷 캡처지만 그건 브라우저 한정이고, Appshots는 **OS 레벨 최전면 창 + 접근성 텍스트**라는 점에서 범위가 더 넓다.

---

### Chrome extension
- URL: https://learn.chatgpt.com/codex/chrome-extension
- 검색: 2026-08-02 기준
- 핵심 내용: ChatGPT가 사용자의 Chrome 브라우저를 제어하도록 하는 확장. 이미 로그인된 사이트(LinkedIn, Salesforce, Gmail, 사내 도구)를 읽고 조작한다. 작업은 **Chrome 탭 그룹**으로 정리되어 실행된다. 아무 웹페이지 옆에 ChatGPT를 띄워 그 페이지 내용에 대해 묻거나, 그 컨텍스트 + 로컬 파일 + 연결된 앱으로 작업을 이어갈 수 있다.
- 설치: ChatGPT 데스크톱 앱의 **Plugins Directory**를 통해 설치 → Chrome 권한 프롬프트 승인 → 브라우저에서 ChatGPT 사이드 채팅 로드 확인.
- 웹사이트 접근 제어: 기본적으로 **새 도메인마다 사전 허가를 요청**한다. 선택지: 한 번만 허용 / 이 사이트에 대해 허용 / 모든 사이트에 대해 허용 / 거부.
- 제약·주의사항:
  - OpenAI는 Chrome 액션의 별도 기록을 남기지 않지만, 브라우저 활동이 채팅 컨텍스트에 들어가면(읽은 텍스트·스크린샷·요약) 저장된다.
  - Computer Use는 **Memories 설정을 존중**한다.
  - **브라우저 히스토리 접근은 민감하므로 요청마다 확인**이 필요하다.
  - Chrome 권한은 확장 기능을 가능하게 할 뿐, ChatGPT는 그 위에 자체 확인·설정·허용 목록·차단 목록을 적용한 뒤에야 사이트나 히스토리를 사용한다.
- Claude Code 대응 관점 메모: Claude Code의 `claude-in-chrome` MCP / Chrome DevTools MCP와 직접 대응. 도메인별 허용 정책 모델도 유사(사이트 레벨 권한). Codex 쪽은 이를 앱 설정(Blocked Websites)과 통합해 관리한다.

---

### Work with files (요청 경로 `/codex/artifacts-viewer`)
- URL: https://learn.chatgpt.com/codex/artifacts-viewer
- 검색: 2026-08-02 기준
- **주의:** 이 URL의 실제 페이지 제목은 **"Work with files"** 다. 리다이렉트가 아니라 해당 경로가 곧바로 "Work with files" 문서로 연결된다. (문서 재확인 결과 2회 모두 동일 — "Artifacts viewer"라는 제목은 문서상 확인되지 않음.)
- 핵심 내용: 문서·프레젠테이션·스프레드시트·PDF를 ChatGPT에서 만들고, 미리보고, 다듬는다. 미리보기·리뷰 도구는 표면마다 다르다.
- 표면별 기능:
  | 표면 | 기능 |
  |---|---|
  | 데스크톱 앱 | 채팅 옆에서 문서·프레젠테이션·스프레드시트·PDF 미리보기. 미리보기 켜면 생성 파일 자동 열림. `.html`·`.htm`은 **인터랙티브 HTML 미리보기**. 렌더된 미리보기 ↔ 소스 보기 전환. **주석(annotation)** 으로 파일 특정 부분에 집중 수정 요청 |
  | ChatGPT Work (웹) | 소스 파일 첨부 또는 문서 생성 요청, 채팅에서 리뷰, 다운로드, 표적 피드백으로 개정 |
  | Codex CLI | 작업 디렉터리에서 파일 생성·편집. **시각적 미리보기·주석 인터페이스 없음.** 출력 경로와 검증 결과를 보고 |
  | IDE 확장 | 워크스페이스 파일 생성·편집, 에디터에서 텍스트·코드 리뷰, 호환 뷰어로 문서 열기 |
- 워크플로 요점: 파일 생성 시 기대하는 시트·컬럼·차트·슬라이드·섹션과 검증 체크를 명시하면 정확도가 올라간다. 주석으로 특정 구간만 다시 요청하면 문서 전체를 다시 만들지 않아도 된다.
- Claude Code 대응 관점 메모: Claude Code의 Artifact 도구와 개념이 겹치지만 성격이 다르다 — Claude의 Artifact는 **공유 가능한 호스팅 페이지**, Codex의 이 기능은 **로컬 파일 생성 + 앱 내 미리보기·주석**이다. 파일 주석 기반 국소 수정은 Claude Code에 직접 대응물이 없다.

---

## 2. 레퍼런스 (Reference)

### Commands (키보드 단축키 & 딥링크)
- URL: https://learn.chatgpt.com/codex/reference/commands
- 검색: 2026-08-02 기준
- 핵심 내용: **ChatGPT 데스크톱 앱의 명령·키보드 단축키 레퍼런스.** `/` 슬래시 명령은 별도 문서(Slash commands)로 분리되어 있다.
- 키보드 단축키 (원문 그대로):

  **General**
  | 액션 | 키 |
  |---|---|
  | Command menu | Cmd/Ctrl + Shift + P 또는 Cmd/Ctrl + K |
  | Settings | Cmd/Ctrl + , |
  | Keyboard shortcuts | Cmd/Ctrl + Shift + / |
  | Open folder | Cmd/Ctrl + O |
  | Navigate back | Cmd/Ctrl + [ |
  | Navigate forward | Cmd/Ctrl + ] |
  | Increase font size | Cmd/Ctrl + + |
  | Decrease font size | Cmd/Ctrl + - |
  | Toggle sidebar | Cmd/Ctrl + B |
  | Open review tab | Ctrl + Shift + G |
  | Toggle review panel | Cmd/Ctrl + Alt + B |
  | Toggle bottom panel | Cmd/Ctrl + J |
  | Toggle terminal | Ctrl + ` |
  | Clear terminal | Ctrl + L |

  **Chat**
  | 액션 | 키 |
  |---|---|
  | Quick chat | Cmd + Option + N (macOS) / Ctrl + Alt + N (Windows) |
  | New chat | Cmd/Ctrl + N 또는 Cmd/Ctrl + Shift + O |
  | Search chats | Cmd/Ctrl + G |
  | Find in chat | Cmd/Ctrl + F |
  | Previous chat | Cmd/Ctrl + Shift + [ |
  | Next chat | Cmd/Ctrl + Shift + ] |

  **Input**
  | 액션 | 키 |
  |---|---|
  | Dictation | Ctrl + Shift + D |

- 딥링크 (`codex://` URL 스킴) — 원문 그대로:
  ```
  codex://threads/new
  codex://new?<query>
  codex://threads/<thread-id>
  codex://settings
  codex://settings/connections/<connection-type>
  codex://settings/connections/ssh/add?name=<ssh-config-host>
  codex://skills
  codex://automations
  codex://plugins/install/<plugin-name>?marketplace=<marketplace-name>
  codex://plugins/<plugin-id>
  codex://plugins/<plugin-name>?marketplacePath=<absolute-marketplace-path>
  codex://pets/install?name=<pet-name>&imageUrl=<https-image-url>
  ```
- 검색 기능: 채팅 검색 `Cmd/Ctrl + G`(과거 대화 다시 열기), 채팅 내 찾기 `Cmd/Ctrl + F`(현재 채팅 안 텍스트).
- 커스터마이징: Settings > Keyboard Shortcuts에서 찾기·변경·초기화. **키스트로크 모드 검색** 지원(명령 이름 또는 키 조합으로 검색).
- Claude Code 대응 관점 메모: Claude Code의 `~/.claude/keybindings.json` 기반 키바인딩 커스터마이징과 대응. 다만 Codex는 GUI 앱이라 단축키 표면이 훨씬 넓고, `codex://` 딥링크 스킴은 Claude Code에 대응물이 없는 **앱 간 연동 진입점**이다.

---

### Slash commands (전수)
- URL: https://learn.chatgpt.com/codex/reference/slash-commands
- 검색: 2026-08-02 기준
- 핵심 내용: 컴포저에서 `/`를 입력해 채팅을 떠나지 않고 액션을 실행. **가용 명령은 환경과 접근 권한에 따라 달라진다.**
- 사용법 (원문): "1. In the chat composer, type `/`. 2. Select a command from the list, or keep typing to filter (for example, `/status`)."
- **`$` 접두어**: 컴포저에서 `$`를 입력해 스킬을 명시적으로 호출할 수 있다. 활성화된 스킬도 슬래시 명령 목록에 나타난다. **커스텀 프롬프트는 `/prompts:<name>` 형태로 나타난다.**
- 슬래시 명령 전체 표 (원문 그대로, 알파벳 순 24개):

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

- `/goal` 상세 (원문 기반): "A goal is a persistent objective that ChatGPT works toward until it finishes the task, pauses, or needs more input." 목표를 먼저 다듬으려면 `/plan`으로 시작한 뒤 `/goal`로 설정한다. 목표가 활성이면 컴포저 위에 진행 상황 행이 표시되고, 그 행의 버튼으로 일시정지·재개·목표 텍스트 편집·목표 해제를 할 수 있다(다시 슬래시 명령을 칠 필요 없음). 목표가 도는 동안에도 후속 메시지로 계속 방향을 조정할 수 있다.
- Claude Code 대응 관점 메모: `/compact`·`/model`·`/init`·`/review`·`/feedback`은 Claude Code에 동명 또는 동등 기능이 있다. Codex 고유: `/goal`(지속 목표), `/side`(임시 사이드 채팅), `/worktree`·`/fork`(워크트리 분기), `/cloud`·`/cloud-environment`(클라우드 실행), `/personality`, `/pet`. `/prompts:<name>` 커스텀 프롬프트는 Claude Code의 슬래시 커맨드(`.claude/commands/*.md`)와 대응.

---

### Settings (데스크톱 앱 설정)
- URL: https://learn.chatgpt.com/codex/reference/settings
- 검색: 2026-08-02 기준
- 핵심 내용: ChatGPT 데스크톱 앱의 환경설정 레퍼런스.
- 섹션과 설정 항목 (원문 영어 표기 유지):

  **General**
  - Require Cmd+Enter for multiline prompts (기본 Off) — 여러 줄 메시지 전송에 키 조합 요구
  - Prevent sleep while running (기본 Off) — "keep local chats continue while you step away"
  - Follow-up behavior (기본 Current run) — 새 메시지가 현재 실행을 조정할지, 다음 실행을 기다릴지

  **Profile**
  - Activity insights: lifetime tokens, peak tokens, streaks, longest task, token activity
  - Profile details (picture, display name, username), Profile card sharing
  - Codex invitations (Invite a friend / Invite a coworker)

  **Keyboard Shortcuts**
  - Commands review, custom bindings, reset defaults
  - 명령 이름 또는 키스트로크로 검색

  **Notifications**
  - Turn completion notifications timing (턴 완료 알림 시점)
  - App notification permission prompts

  **Appearance**
  - Base theme selection
  - Accent color / Background color / Foreground color
  - UI font / Code font
  - Custom theme sharing

  **Pets**
  - 내장 또는 커스텀 펫 선택
  - Pet overlay 제어 (`/pet`, Wake Pet, Tuck Away Pet)

  **Browser**
  - 번들 Browser 플러그인 설치
  - Chrome 확장 설정
  - Allowed/blocked websites 관리

  **Computer Use**
  - 데스크톱 앱 접근 권한 검토 및 관련 선호 설정

  **Personalization**
  - Default personality: **Friendly / Pragmatic / None**
  - Custom instructions — **개인 지침을 `AGENTS.md`에 반영한다**
  - Suggested Prompts (컨텍스트 인지형 후속 제안 토글)
  - Memories (과거 채팅의 컨텍스트를 이후 작업으로 이어감)

  **Archived Chats**
  - 보관된 채팅 목록(날짜·프로젝트 컨텍스트 표시), Unarchive로 복원

  **Keep a Chat Near Your Work**
  - Chat pop-out window (활성 채팅을 플로팅 창으로 분리)
  - Always on top (기본 Off)

- 연결되는 `config.toml` 키: Personality → `personality`, Memories → `[features] memories` + `[memories]` 테이블, Code font → TUI/리뷰 창 공통 폰트.
- Claude Code 대응 관점 메모: **"Custom instructions가 `AGENTS.md`를 업데이트한다"** 는 점이 핵심 대응 포인트 — Claude Code에서 `/memory` 편집이 `CLAUDE.md`를 고치는 것과 같은 구조다. 즉 GUI 설정과 파일 기반 지침이 하나로 수렴한다.

---

### Troubleshooting
- URL: https://learn.chatgpt.com/codex/reference/troubleshooting
- 검색: 2026-08-02 기준
- 핵심 내용: FAQ + 로그 위치 + 막힘 상태 복구 패턴.
- FAQ (원문 요지):
  | 증상 | 원인·해결 |
  |---|---|
  | Codex가 편집하지 않은 파일이 사이드 패널에 보임 | 프로젝트가 Git 저장소면 리뷰 패널이 **Git 상태** 기준으로 변경을 보여주기 때문. staged/unstaged 전환·브랜치 비교 가능. Codex의 최근 변경만 보려면 diff 창의 **"Last turn"** 뷰 사용 |
  | 사이드바에서 프로젝트 제거 | 프로젝트 이름 위에 마우스 올리고 점 3개 메뉴 → **Remove**. 복원은 "Add new project" 버튼 또는 **Cmd+O** |
  | 보관된 채팅 찾기 | Settings에 있음. Unarchive하면 원래 사이드바 위치로 복귀 |
  | 일부 채팅만 사이드바에 보임 | "Chats" 옆 필터 아이콘 → **Chronological** 선택. 그래도 없으면 Settings의 보관 채팅 확인 |
  | 워크트리에서 코드가 안 돌아감 | 워크트리는 기본적으로 **Git이 추적하는 파일만** 상속. 로컬 환경으로 셋업 스크립트를 돌리거나 **`.worktreeinclude`** 로 무시된 파일을 복사. 또는 일반 프로젝트에서 체크아웃 |
  | 팀원이 공유한 로컬 환경을 앱이 못 읽음 | 로컬 환경 설정이 **프로젝트 루트의 `.codex` 폴더**에 있어야 함. 모노레포면 `.codex` 폴더가 있는 디렉터리를 프로젝트로 열 것 |
  | Codex가 Apple Music 접근을 요청 | 일부 macOS 디렉터리는 사용자 승인 필요. 홈 디렉터리 접근이 필요하면 macOS가 승인을 요청함 |
  | 예약 작업이 워크트리를 너무 많이 만듦 | 필요 없는 예약 실행을 아카이브하고, 워크트리가 필요한 게 아니면 실행을 pin하지 말 것 |
  | 잘못된 대상 선택 후 프롬프트 복구 | 컴포저에서 **위 방향키** |
  | CLI에선 되는데 데스크톱 앱에선 안 되는 기능 | 표면마다 Codex 버전이 다를 수 있음. 버전 확인:<br>CLI: `codex --version`<br>데스크톱 앱: `/Applications/Codex.app/Contents/Resources/codex --version` |
- 로그·경로 (원문 그대로):
  | 대상 | 경로 |
  |---|---|
  | 앱 로그 (macOS) | `~/Library/Logs/com.openai.codex/YYYY/MM/DD` |
  | 세션 트랜스크립트 | `$CODEX_HOME/sessions` (기본 `~/.codex/sessions`) |
  | 보관된 세션 | `$CODEX_HOME/archived_sessions` (기본 `~/.codex/archived_sessions`) |
- 피드백·이슈: 컴포저에서 `/` 입력 → 피드백. 기존 세션을 피드백과 함께 공유하면 세션 ID가 생성된다. 이슈 보고는 https://github.com/openai/codex/issues (기존 이슈 확인 후 새 버그 리포트 작성).
- 막힘 상태 복구 패턴: (1) 승인 대기 중인지 확인 (2) 터미널에서 `git status` 실행 (3) 좁힌 프롬프트로 새 채팅 시작. 워크트리 생성 취소 후 프롬프트 분실 시 위 방향키로 복구.
- 터미널 이슈: 터미널이 멈춘 것 같으면 (1) 터미널 패널 닫기 (2) **Ctrl+`** 로 다시 열기 (3) `pwd` 또는 `git status` 실행. 현재 디렉터리·브랜치를 먼저 검증. 계속되면 활성 채팅 완료를 기다렸다 앱 재시작.
- 폰트: Settings의 **"Code font"** 에서 설정. 리뷰 창·터미널·코드 표시에 동일 폰트가 쓰인다.
- Claude Code 대응 관점 메모: `$CODEX_HOME/sessions` ↔ Claude Code의 `~/.claude/projects/*/[uuid].jsonl` 트랜스크립트. `.worktreeinclude`는 Claude Code에 대응물이 없는 **워크트리 파일 승계 제어** 장치 — 하네스에서 worktree isolation을 쓸 때 참고할 만한 개념.

---

## 3. 설정 (Configuration & Config File)

### Configuration (허브 페이지)
- URL: https://learn.chatgpt.com/codex/configuration
- 검색: 2026-08-02 기준
- 핵심 내용: 기본값 설정, 지속적 컨텍스트 추가, ChatGPT/Codex 개발 도구 커스터마이징의 진입 허브. "configuration shapes behavior across chats, repositories, and machines for both individuals and teams."
- 하위 구조:
  - **Personal settings:** General, Profile, Appearance, Voice, Configuration, Personalization, Keyboard shortcuts
  - **Integrations:** MCP servers, Browser
  - **Configuration options:** User config (`config.toml`), Approval policy(승인 요청 시점), Sandbox settings(명령 실행 시 허용 범위), Network access, Personality(Friendly 또는 Pragmatic)
  - **주요 주제 5가지:** 1) Customization 2) Config File 3) Agent Configuration 4) Extend ChatGPT and Codex 5) Windows
- Claude Code 대응 관점 메모: Codex는 설정 축을 **config.toml(머신·프로젝트 defaults) / AGENTS.md(프로젝트 지침) / rules(명령 허용 정책) / hooks(라이프사이클)** 로 4분할한다. Claude Code는 `settings.json`(권한·env·hooks) + `CLAUDE.md`(지침)의 2분할 — Codex 쪽 `rules`가 Claude Code `settings.json`의 permissions allow/deny 규칙에 해당한다.

---

### Config basics
- URL: https://learn.chatgpt.com/codex/config-file/config-basic
- 검색: 2026-08-02 기준
- 핵심 내용: 로컬 Codex 설정의 저장 위치와 우선순위, 자주 쓰는 옵션, feature flag 표.
- 설정 저장 위치:
  - 사용자 레벨: `~/.codex/config.toml`
  - 프로젝트 레벨: 저장소 안의 `.codex/config.toml`
- **우선순위 (원문, 높은 것부터):**
  1. CLI flags and `--config` overrides
  2. Project config files: `.codex/config.toml`, ordered from project root to current working directory (closest wins; trusted projects only)
  3. Profile files selected with `--profile profile-name` (`~/.codex/profile-name.config.toml`)
  4. User config: `~/.codex/config.toml`
  5. System config (if present): `/etc/codex/config.toml` on Unix
  6. Built-in defaults
- 주요 TOML 예시 (원문 그대로):
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
- **`[features]` 표 (원문 그대로 — 2026-08 기준):**

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

- 관리형 조직 제약 (원문): "On managed machines, your organization may also enforce constraints via `requirements.toml` (for example, disallowing `approval_policy = "never"` or `sandbox_mode = "danger-full-access"`)."
- 제약·주의사항: **신뢰되지 않은(untrusted) 프로젝트는 프로젝트 스코프 레이어를 건너뛴다.**
- Claude Code 대응 관점 메모: 우선순위 6단계는 Claude Code의 settings 계층(enterprise managed → CLI args → `.claude/settings.local.json` → `.claude/settings.json` → `~/.claude/settings.json`)과 구조적으로 대응. `requirements.toml` ↔ Claude Code의 managed settings(`/Library/Application Support/ClaudeCode/managed-settings.json`).

---

### Advanced configuration
- URL: https://learn.chatgpt.com/codex/config-file/config-advanced
- 검색: 2026-08-02 기준
- 핵심 내용: 고급 설정 20개 주제 — Profiles / One-off CLI Overrides / Config Locations / Project Config Files / Hooks / Custom Model Providers / Amazon Bedrock / OSS Mode / Azure Provider / Model Settings / Approval Policies & Sandbox / Shell Environment Policy / MCP Servers / Observability(OTel) / Notifications / History Persistence / Citations / Project Instructions / Desktop Options / TUI Options.
- 핵심 개념:
  - **Profiles**: 이름 붙인 설정 레이어. CLI에서 `--profile profile-name`으로 전환. 파일은 `$CODEX_HOME/{name}.config.toml`.
  - **One-off overrides**: `--model` 같은 플래그, 또는 `-c` / `--config key=value`.
  - **Config locations**: `CODEX_HOME`(기본 `~/.codex`)에 설정·인증·상태 저장.
  - **Project config**: 저장소의 `.codex/config.toml` — **프로젝트가 trusted일 때만 로드**.
  - **Hooks**: `hooks.json` 또는 인라인 `[hooks]` 테이블에서 로드.
- TOML 예시 (원문 그대로):

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

  **헤더 설정**
  ```toml
  [model_providers.example]
  http_headers = { "X-Example-Header" = "example-value" }
  env_http_headers = { "X-Example-Features" = "EXAMPLE_FEATURES" }
  ```

  **명령 기반 bearer token 인증**
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

  **Amazon Bedrock**
  ```toml
  model_provider = "amazon-bedrock"
  model = "<bedrock-model-id>"

  [model_providers.amazon-bedrock.aws]
  profile = "default"
  region = "eu-central-1"
  ```

  **OSS 모드**
  ```toml
  oss_provider = "ollama" # or "lmstudio"
  ```

  **Azure**
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

  **데이터 레지던시**
  ```toml
  model_provider = "openaidr"
  [model_providers.openaidr]
  name = "OpenAI Data Residency"
  base_url = "https://us.api.openai.com/v1"
  ```

  **모델 추론·컨텍스트**
  ```toml
  model_reasoning_summary = "none"
  model_verbosity = "low"
  model_supports_reasoning_summaries = true
  model_context_window = 128000
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

  **Granular 승인 정책**
  ```toml
  approval_policy = { granular = {
    sandbox_approval = true,
    rules = true,
    mcp_elicitations = true,
    request_permissions = false,
    skill_approval = false
  } }
  ```

  **Shell 환경 정책**
  ```toml
  [shell_environment_policy]
  inherit = "none"
  set = { PATH = "/usr/bin", MY_FLAG = "1" }
  ignore_default_excludes = false
  exclude = ["AWS_*", "AZURE_*"]
  include_only = ["PATH", "HOME"]
  ```

  **OpenTelemetry**
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

  **알림 / 분석 / 피드백 / 추론 표시**
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

  **히스토리 지속성**
  ```toml
  [history]
  persistence = "none"
  max_bytes = 104857600 # 100 MiB
  ```

  **파일 열기(citations)**
  ```toml
  file_opener = "vscode" # or cursor, windsurf, vscode-insiders, none
  ```

  **TUI 옵션**
  ```toml
  [tui]
  notifications = true
  notification_method = "auto"
  notification_condition = "unfocused"
  animations = true
  alternate_screen = "auto"
  show_tooltips = true
  ```

  **데스크톱 커스텀 파일 핸들러**
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
- 알림 이벤트: `agent-turn-complete` 등 외부 프로그램 트리거.
- Claude Code 대응 관점 메모: `notify` ↔ Claude Code의 Notification/Stop hook. `[shell_environment_policy]` ↔ Claude Code `settings.json`의 `env` (다만 Codex 쪽이 **상속·제외·화이트리스트**까지 세분화). `file_opener` citations ↔ Claude Code의 파일 경로 클릭 열기. `[otel]` ↔ Claude Code의 OTel 텔레메트리 환경 변수.

---

### Config reference (전체 키 원장)
- URL: https://learn.chatgpt.com/codex/config-file/config-reference
- 검색: 2026-08-02 기준
- **수집 한계 명시:** 이 페이지는 수백 항목의 대형 표다. 1차 시도에서 표 전체 축자 복제는 거부되었으나, 2·3차 시도로 **키 이름 전수 목록**과 **섹션별 대표 기본값**을 확보했다. 개별 키의 설명 원문은 이 문서에 없으므로, 특정 키의 정확한 문구가 필요하면 위 URL을 직접 참조할 것.
- **설정 키 전수 목록 (문서 표 순서 그대로, 2026-08-02 기준):**

```
agents
agents.<name>.config_file
agents.<name>.description
agents.default_subagent_model
agents.default_subagent_reasoning_effort
agents.enabled
agents.interrupt_message
agents.max_concurrent_threads_per_session
agents.max_threads
allow_login_shell
analytics.enabled
approval_policy
approval_policy.granular.mcp_elicitations
approval_policy.granular.request_permissions
approval_policy.granular.rules
approval_policy.granular.sandbox_approval
approval_policy.granular.skill_approval
approvals_reviewer
apps._default.approvals_reviewer
apps._default.default_tools_approval_mode
apps._default.destructive_enabled
apps._default.enabled
apps._default.open_world_enabled
apps.<id>.approvals_reviewer
apps.<id>.default_tools_approval_mode
apps.<id>.default_tools_enabled
apps.<id>.destructive_enabled
apps.<id>.enabled
apps.<id>.open_world_enabled
apps.<id>.tools.<tool>.approval_mode
apps.<id>.tools.<tool>.enabled
auto_review.policy
background_terminal_max_timeout
chatgpt_base_url
check_for_update_on_startup
cli_auth_credentials_store
compact_prompt
computer_use.windows.always_allowed_app_ids
default_permissions
desktop.custom_file_handlers.<id>
desktop.custom_file_handlers.<id>.args
desktop.custom_file_handlers.<id>.command
desktop.custom_file_handlers.<id>.icon
desktop.custom_file_handlers.<id>.input
desktop.custom_file_handlers.<id>.label
desktop.custom_file_handlers.<id>.supports_ssh
developer_instructions
disable_paste_burst
experimental_compact_prompt_file
experimental_use_unified_exec_tool
features.apps
features.code_mode.direct_only_tool_namespaces
features.code_mode.enabled
features.code_mode.excluded_tool_namespaces
features.enable_request_compression
features.fast_mode
features.goals
features.hooks
features.memories
features.multi_agent
features.network_proxy
features.network_proxy.allow_local_binding
features.network_proxy.allow_upstream_proxy
features.network_proxy.dangerously_allow_all_unix_sockets
features.network_proxy.dangerously_allow_non_loopback_proxy
features.network_proxy.domains
features.network_proxy.enable_socks5
features.network_proxy.enable_socks5_udp
features.network_proxy.enabled
features.network_proxy.proxy_url
features.network_proxy.socks_url
features.network_proxy.unix_sockets
features.personality
features.prevent_idle_sleep
features.remote_plugin
features.rollout_budget.enabled
features.rollout_budget.limit_tokens
features.rollout_budget.prefill_token_weight
features.rollout_budget.reminder_interval_tokens
features.rollout_budget.sampling_token_weight
features.shell_snapshot
features.shell_tool
features.skill_mcp_dependency_install
features.unified_exec
features.web_search
features.web_search_cached
features.web_search_request
feedback.enabled
file_opener
forced_chatgpt_workspace_id
forced_login_method
hide_agent_reasoning
history.max_bytes
history.persistence
hooks
hooks.<Event>
hooks.<Event>[].hooks
hooks.<Event>[].hooks[].additionalContextLimit
hooks.<Event>[].hooks[].commandWindows
instructions
log_dir
mcp_oauth_callback_port
mcp_oauth_callback_url
mcp_oauth_credentials_store
mcp_servers.<id>.args
mcp_servers.<id>.auth
mcp_servers.<id>.bearer_token_env_var
mcp_servers.<id>.command
mcp_servers.<id>.cwd
mcp_servers.<id>.default_tools_approval_mode
mcp_servers.<id>.disabled_tools
mcp_servers.<id>.enabled
mcp_servers.<id>.enabled_tools
mcp_servers.<id>.env
mcp_servers.<id>.env_http_headers
mcp_servers.<id>.env_vars
mcp_servers.<id>.experimental_environment
mcp_servers.<id>.http_headers
mcp_servers.<id>.oauth_resource
mcp_servers.<id>.required
mcp_servers.<id>.scopes
mcp_servers.<id>.startup_timeout_ms
mcp_servers.<id>.startup_timeout_sec
mcp_servers.<id>.tool_timeout_sec
mcp_servers.<id>.tools.<tool>.approval_mode
mcp_servers.<id>.url
memories.consolidation_model
memories.disable_on_external_context
memories.extract_model
memories.generate_memories
memories.max_raw_memories_for_consolidation
memories.max_rollout_age_days
memories.max_rollouts_per_startup
memories.max_unused_days
memories.min_rate_limit_remaining_percent
memories.min_rollout_idle_hours
memories.use_memories
model
model_auto_compact_token_limit
model_auto_compact_token_limit_scope
model_catalog_json
model_context_window
model_instructions_file
model_provider
model_providers.<id>
model_providers.<id>.auth
model_providers.<id>.auth.args
model_providers.<id>.auth.command
model_providers.<id>.auth.cwd
model_providers.<id>.auth.refresh_interval_ms
model_providers.<id>.auth.timeout_ms
model_providers.<id>.base_url
model_providers.<id>.env_http_headers
model_providers.<id>.env_key
model_providers.<id>.env_key_instructions
model_providers.<id>.experimental_bearer_token
model_providers.<id>.http_headers
model_providers.<id>.name
model_providers.<id>.query_params
model_providers.<id>.request_max_retries
model_providers.<id>.requires_openai_auth
model_providers.<id>.stream_idle_timeout_ms
model_providers.<id>.stream_max_retries
model_providers.<id>.supports_websockets
model_providers.<id>.wire_api
model_providers.amazon-bedrock.aws.profile
model_providers.amazon-bedrock.aws.region
model_reasoning_effort
model_reasoning_summary
model_supports_reasoning_summaries
model_verbosity
notice.hide_full_access_warning
notice.hide_gpt-5.1-codex-max_migration_prompt
notice.hide_gpt5_1_migration_prompt
notice.hide_rate_limit_model_nudge
notice.hide_world_writable_warning
notice.model_migrations
notify
openai_base_url
oss_provider
otel.environment
otel.exporter
otel.exporter.<id>.endpoint
otel.exporter.<id>.headers
otel.exporter.<id>.protocol
otel.exporter.<id>.tls.ca-certificate
otel.exporter.<id>.tls.client-certificate
otel.exporter.<id>.tls.client-private-key
otel.log_user_prompt
otel.metrics_exporter
otel.trace_exporter
otel.trace_exporter.<id>.endpoint
otel.trace_exporter.<id>.headers
otel.trace_exporter.<id>.protocol
otel.trace_exporter.<id>.tls.ca-certificate
otel.trace_exporter.<id>.tls.client-certificate
otel.trace_exporter.<id>.tls.client-private-key
permissions.<name>.description
permissions.<name>.extends
permissions.<name>.filesystem
permissions.<name>.filesystem.":workspace_roots".<subpath-or-glob>
permissions.<name>.filesystem.<path-or-glob>
permissions.<name>.filesystem.glob_scan_max_depth
permissions.<name>.network.allow_local_binding
permissions.<name>.network.allow_upstream_proxy
permissions.<name>.network.dangerously_allow_all_unix_sockets
permissions.<name>.network.dangerously_allow_non_loopback_proxy
permissions.<name>.network.domains
permissions.<name>.network.domains.<pattern>
permissions.<name>.network.enable_socks5
permissions.<name>.network.enable_socks5_udp
permissions.<name>.network.enabled
permissions.<name>.network.mode
permissions.<name>.network.proxy_url
permissions.<name>.network.socks_url
permissions.<name>.network.unix_sockets
permissions.<name>.network.unix_sockets.<path>
permissions.<name>.workspace_roots
permissions.<name>.workspace_roots.<path>
personality
plan_mode_reasoning_effort
plugins.<plugin>.mcp_servers.<server>.default_tools_approval_mode
plugins.<plugin>.mcp_servers.<server>.disabled_tools
plugins.<plugin>.mcp_servers.<server>.enabled
plugins.<plugin>.mcp_servers.<server>.enabled_tools
plugins.<plugin>.mcp_servers.<server>.tools.<tool>.approval_mode
project_doc_fallback_filenames
project_doc_max_bytes
project_root_markers
projects.<path>.trust_level
review_model
sandbox_mode
sandbox_workspace_write.exclude_slash_tmp
sandbox_workspace_write.exclude_tmpdir_env_var
sandbox_workspace_write.network_access
sandbox_workspace_write.writable_roots
service_tier
shell_environment_policy.exclude
shell_environment_policy.experimental_use_profile
shell_environment_policy.ignore_default_excludes
shell_environment_policy.include_only
shell_environment_policy.inherit
shell_environment_policy.set
show_raw_agent_reasoning
skills.config
skills.config.<index>.enabled
skills.config.<index>.path
sqlite_home
suppress_unstable_features_warning
tool_output_token_limit
tool_suggest.disabled_tools
tool_suggest.discoverables
tools.view_image
tools.web_search
tui
tui.alternate_screen
tui.animations
tui.keymap.<context>.<action>
tui.model_availability_nux.<model>
tui.notification_condition
tui.notification_method
tui.notifications
tui.raw_output_mode
tui.resume_cwd
tui.show_tooltips
tui.status_line
tui.terminal_title
tui.theme
tui.vim_mode_default
web_search
windows_wsl_setup_acknowledged
windows.sandbox
windows.sandbox_private_desktop
```

- **섹션별 대표 기본값·타입 (2차 확인분):**
  | 키 | 타입/값 | 기본값 |
  |---|---|---|
  | `sandbox_mode` | read-only \| workspace-write \| danger-full-access | `read-only` |
  | `sandbox_workspace_write.network_access` | boolean | `false` |
  | `sandbox_workspace_write.writable_roots` | array | `[]` |
  | `permissions.<name>.network.enabled` | boolean | `false` |
  | `features.multi_agent` | boolean | `true` |
  | `features.unified_exec` | boolean | `true` (Windows 제외) |
  | `features.network_proxy.enabled` | boolean | `false` |
  | `features.memories` | boolean | `false` |
  | `agents.enabled` | boolean | `true` |
  | `mcp_servers.<id>.startup_timeout_sec` | number | `10` |
  | `mcp_servers.<id>.tool_timeout_sec` | number | `60` |
  | `mcp_servers.<id>.default_tools_approval_mode` | auto \| prompt \| writes \| approve | — |
  | `tui.alternate_screen` | auto \| always \| never | `auto` |
  | `otel.exporter` | none \| otlp-http \| otlp-grpc | `none` |
  | `otel.metrics_exporter` | none \| statsig \| otlp-http \| otlp-grpc | `statsig` |
  | `otel.environment` | string | `dev` |
  | `model_reasoning_effort` | minimal \| low \| medium \| high \| xhigh | — |
  | `model_verbosity` | low \| medium \| high | — |
  | `apps._default.enabled` | boolean | `true` |
- Claude Code 대응 관점 메모: 이 키 목록 규모 자체가 관점거리다 — Codex는 **약 250개 설정 키**를 단일 `config.toml` 레퍼런스로 노출한다. Claude Code `settings.json`은 키 수가 훨씬 적고 권한 문법(`Bash(git:*)`)에 표현력을 몰아준다. `permissions.<name>.*` 네임드 프로필은 Claude Code에 대응물이 없는 **재사용 가능 권한 프로필** 개념.

---

### Environment variables (전수)
- URL: https://learn.chatgpt.com/codex/config-file/environment-variables
- 검색: 2026-08-02 기준
- **환경 변수 표 (원문 그대로, 9개 전수):**

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

- 관련 환경 변수(다른 페이지 출처): `VISUAL` / `EDITOR`(프롬프트 에디터, cli-customization), `PLUGIN_ROOT` / `PLUGIN_DATA`(플러그인 훅, hooks), `TMPDIR`(Chronicle 캡처 경로).
- Claude Code 대응 관점 메모: `CODEX_HOME` ↔ `CLAUDE_CONFIG_DIR`(기본 `~/.claude`). `CODEX_API_KEY` ↔ `ANTHROPIC_API_KEY`. `RUST_LOG` ↔ Claude Code의 `DEBUG`/`ANTHROPIC_LOG`. **`CODEX_NON_INTERACTIVE`·`CODEX_INSTALL_DIR`처럼 설치 스크립트 전용 변수를 공식 문서에 명시한 점**은 CI 자동화 관점에서 참고할 만하다.

---

### Sample config.toml (전문)
- URL: https://learn.chatgpt.com/codex/config-file/config-sample
- 검색: 2026-08-02 기준
- **이 페이지가 그룹 B 최대의 원장이다.** 아래는 문서의 샘플 TOML 전문(주석 포함, 원문 그대로).

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
# model_context_window = 128000                    # tokens; default: auto for model
# model_auto_compact_token_limit = 64000           # tokens; unset uses model defaults
# model_auto_compact_token_limit_scope = "total"   # total | body_after_prefix; default: total
# tool_output_token_limit = 12000                  # tokens stored per tool output
# model_catalog_json = "/absolute/path/to/models.json"  # optional startup-only model catalog override
# background_terminal_max_timeout = 300000         # ms; max empty write_stdin poll window (default 5m)
# log_dir = "/absolute/path/to/codex-logs"         # log directory; setting explicitly enables codex-tui.log; default: "$CODEX_HOME/log"
# sqlite_home = "/absolute/path/to/codex-state"    # optional SQLite-backed runtime state directory

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
#   sandbox_approval = true,
#   rules = true,
#   mcp_elicitations = true,
#   request_permissions = false,
#   skill_approval = false
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
#   :read-only | :workspace | :danger-full-access
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
# config_file = "./agents/reviewer.toml"   # relative to the config.toml that defines it

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
# Case-insensitive glob patterns to remove (e.g., "AWS**", "AZURE**"). Default: []
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
# "*.example.com" matches subdomains only; "**.example.com" matches the apex plus subdomains.
# "*" allows any public host that is not denied, so prefer scoped rules when possible.
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
# glob_scan_max_depth when using unbounded patterns such as `**`.
# [permissions.workspace.filesystem]
# glob_scan_max_depth = 3
# ":workspace_roots" = { "." = "write", "**/*.env" = "deny" }
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
# mode = "limited"  # limited | full
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
#   ["model-with-reasoning", "context-remaining", "current-dir"].
# Set to [] to hide the footer.
# status_line = ["model", "context-remaining", "git-branch"]
# Ordered list of terminal window/tab title item IDs. When unset, Codex uses:
#   ["spinner", "project"]. Set to [] to clear the title.
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
# disable_on_external_context = false  # legacy alias: no_memories_if_mcp_or_web_search

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
# enabled = true                          # optional; default true
# required = true                         # optional; fail startup/resume if this server cannot initialize
# command = "docs-server"                 # required
# args = ["--port", "4000"]               # optional
# env = { "API_KEY" = "value" }           # optional key/value pairs copied as-is
# env_vars = ["ANOTHER_SECRET"]           # optional: forward local parent env vars
# env_vars = ["LOCAL_TOKEN", { name = "REMOTE_TOKEN", source = "remote" }]
# cwd = "/path/to/server"                 # optional working directory override
# experimental_environment = "remote"     # experimental: run stdio via a remote executor
# startup_timeout_sec = 10.0              # optional; default 10.0 seconds
# # startup_timeout_ms = 10000            # optional alias for startup timeout (milliseconds)
# tool_timeout_sec = 60.0                 # optional; default 60.0 seconds
# enabled_tools = ["search", "summarize"] # optional allow-list
# disabled_tools = ["slow-tool"]          # optional deny-list (applied after allow-list)
# scopes = ["read:docs"]                  # optional OAuth scopes
# oauth_resource = "https://docs.example.com/"  # optional OAuth resource

# --- Example: Streamable HTTP transport ---
# [mcp_servers.github]
# enabled = true                          # optional; default true
# required = true                         # optional; fail startup/resume if this server cannot initialize
# url = "https://github-mcp.example.com/mcp"    # required
# bearer_token_env_var = "GITHUB_TOKEN"   # optional; Authorization: Bearer <token>
# http_headers = { "X-Example" = "value" }      # optional static headers
# env_http_headers = { "X-Auth" = "AUTH_ENV" }  # optional headers populated from env vars
# startup_timeout_sec = 10.0              # optional
# tool_timeout_sec = 60.0                 # optional
# enabled_tools = ["list_issues"]         # optional allow-list
# disabled_tools = ["delete_issue"]       # optional deny-list
# scopes = ["repo"]                       # optional OAuth scopes

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
# base_url = "https://us.api.openai.com/v1"       # example with 'us' domain prefix
# wire_api = "responses"                          # only supported value
# # requires_openai_auth = true                   # use only for providers backed by OpenAI auth
# # request_max_retries = 4                       # default 4; max 100
# # stream_max_retries = 5                        # default 5; max 100
# # stream_idle_timeout_ms = 300000               # default 300_000 (5m)
# # supports_websockets = true                    # optional
# # experimental_bearer_token = "sk-example"      # optional dev-only direct bearer token
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
# approvals_reviewer = "user"              # user | auto_review
# default_tools_approval_mode = "auto"     # auto | prompt | writes | approve
#
# [apps.google_drive]
# enabled = false
# destructive_enabled = false              # block destructive-hint tools for this app
# default_tools_enabled = true
# approvals_reviewer = "auto_review"
# default_tools_approval_mode = "prompt"   # auto | prompt | writes | approve
#
# [apps.google_drive.tools."files/delete"]
# enabled = false
# approval_mode = "approve"

# Optional tool suggestion allowlist for connectors or plugins Codex can offer to install.
# [tool_suggest]
# discoverables = [
#   { type = "connector", id = "gmail" },
#   { type = "plugin", id = "figma@openai-curated" },
# ]
# disabled_tools = [
#   { type = "plugin", id = "slack@openai-curated" },
#   { type = "connector", id = "connector_googlecalendar" },
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
# service_tier = "fast"                 # or another supported service tier id
# oss_provider = "ollama"
# model_reasoning_effort = "medium"
# plan_mode_reasoning_effort = "high"
# model_reasoning_summary = "auto"
# model_verbosity = "medium"
# personality = "pragmatic"             # or "friendly" or "none"
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
# trust_level = "trusted"   # or "untrusted"

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
# protocol = "binary"   # "binary" | "json"
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

- **이 샘플에서 뽑아낼 핵심 수치·기본값 (2026-08 기준):**
  | 항목 | 값 |
  |---|---|
  | 권장 기본 모델 | `gpt-5.6` |
  | 서브에이전트 예시 모델 | `gpt-5.6-terra` |
  | `approval_policy` 기본 | `on-request` |
  | `sandbox_mode` 기본 | `read-only` |
  | `web_search` 기본 | `cached` (단, `--yolo` 등 full access 시 `live`) |
  | `project_doc_max_bytes` 기본 | `32768` (32 KiB) |
  | `project_root_markers` 기본 | `[".git"]` |
  | `file_opener` 기본 | `vscode` |
  | `history.persistence` 기본 | `save-all` |
  | `cli_auth_credentials_store` 기본 | `file` |
  | `mcp_oauth_credentials_store` 기본 | `auto` |
  | MCP `startup_timeout_sec` 기본 | `10.0`초 |
  | MCP `tool_timeout_sec` 기본 | `60.0`초 |
  | `background_terminal_max_timeout` 기본 | 300000 ms (5분) |
  | `request_max_retries` 기본 | 4 (최대 100) |
  | `stream_max_retries` 기본 | 5 (최대 100) |
  | `stream_idle_timeout_ms` 기본 | 300000 (5분) |
  | `otel.metrics_exporter` 기본 | `statsig` |
  | `windows.sandbox` 샘플값 | `unelevated` |
  | 내장 provider ID (예약) | `openai`, `ollama`, `lmstudio`, `amazon-bedrock` |
  | 내장 permissions 프로필 | `:read-only`, `:workspace`, `:danger-full-access` |
  | 기본 상태라인 항목 | `["model-with-reasoning", "context-remaining", "current-dir"]` |
  | 기본 터미널 타이틀 항목 | `["spinner", "project"]` |
- Claude Code 대응 관점 메모: `project_doc_max_bytes = 32768`은 Claude Code가 `CLAUDE.md`를 무제한 로드하는 것과 대비되는 **명시적 지침 예산**이다. `[projects."<path>"].trust_level`은 Claude Code의 프로젝트 신뢰 프롬프트("Do you trust the files in this folder?")를 파일로 고정하는 형태. `[features.rollout_budget]`(토큰 예산 + 리마인더)은 Claude Code에 대응물이 없는 **에이전트 토큰 예산 추적** 기능.

---

## 4. 커스터마이징 (Customization)

### Customization (개요)
- URL: https://learn.chatgpt.com/codex/customization/overview
- 검색: 2026-08-02 기준
- 핵심 내용: Codex 커스터마이징을 보완적 5개 레이어로 정리한다.
  1. **Project guidance (AGENTS.md)** — 저장소와 함께 다니는 지속 지침. 빌드 명령, 리뷰 기대치, 저장소 관례.
  2. **Memories** — 이전 작업에서 학습된 컨텍스트. 로컬에 지속.
  3. **Skills** — 재사용 가능한 워크플로·도메인 전문성을 반복 가능한 프로세스로 패키징.
  4. **MCP** — GitHub, Linear, Figma 같은 외부 도구·공유 시스템과 통합.
  5. **Subagents** — 집중 작업을 전담 에이전트에 위임.
- 경로:
  - Skills: `~/.agents/skills` (글로벌) / `.agents/skills` (저장소별)
  - Global AGENTS.md: `~/.codex/`
- **AGENTS.md를 갱신해야 할 신호 (원문 요지):** 에이전트가 같은 실수를 반복할 때, 문서를 너무 많이 읽을 때, 같은 피드백을 반복해서 줄 때.
- **권장 도입 순서 (원문 요지):** AGENTS.md 규칙 확립 → 스킬 설치·작성 → 외부 시스템 연결(MCP) → 마지막으로 서브에이전트 위임.
- Claude Code 대응 관점 메모: 5레이어가 Claude Code와 거의 1:1 대응한다 — AGENTS.md ↔ CLAUDE.md, Memories ↔ (Claude Code에는 유사 기능 없음/`#` 메모리 추가), Skills ↔ Skills(`.claude/skills`), MCP ↔ MCP, Subagents ↔ Subagents(`.claude/agents/*.md`). **도입 순서 권고("지침 먼저, 서브에이전트 마지막")** 는 하네스 설계에도 그대로 적용되는 원칙.

---

### Memories
- URL: https://learn.chatgpt.com/codex/customization/memories
- 검색: 2026-08-02 기준
- 핵심 내용: ChatGPT와 Codex가 여러 세션에 걸쳐 유용한 컨텍스트를 유지한다. **ChatGPT 웹은 ChatGPT memory를, 로컬 Codex 클라이언트는 별도의 로컬 메모리 저장소를 독립된 제어로 유지한다.**
- 명령·설정:
  - 데스크톱 앱: `/memories` 명령 또는 **Settings > Personalization**
  - CLI·IDE 확장: 대화형 세션에서 `/memories`
- 저장 경로: `~/.codex/memories/` (또는 커스텀 `CODEX_HOME`) — 요약(summaries), 지속 항목(durable entries), 최근 입력(recent inputs), 근거(supporting evidence)를 담는다.
- 활성화:
  ```toml
  [features]
  memories = true
  ```
  또는 **Settings > Personalization**
- **메모리 설정 키 (config-reference 대조 포함, 전수):**
  | 키 | 설명 |
  |---|---|
  | `memories.generate_memories` | 새로 만들어진 채팅을 메모리 생성 입력으로 저장할지 제어 |
  | `memories.use_memories` | 기존 메모리를 이후 세션에 주입할지 제어 |
  | `memories.disable_on_external_context` | `true`면 외부 컨텍스트(MCP 도구·웹 검색)를 쓴 채팅을 메모리 생성에서 제외. 레거시 별칭: `no_memories_if_mcp_or_web_search` |
  | `memories.min_rate_limit_remaining_percent` | 메모리 생성을 시작하기 위한 최소 잔여 레이트리밋 비율 |
  | `memories.extract_model` | 채팅별 메모리 추출에 쓸 모델 오버라이드 |
  | `memories.consolidation_model` | 전역 메모리 통합에 쓸 모델 오버라이드 |
  | `memories.max_raw_memories_for_consolidation` | (config-reference 목록에 존재) |
  | `memories.max_rollout_age_days` | (config-reference 목록에 존재) |
  | `memories.max_rollouts_per_startup` | (config-reference 목록에 존재) |
  | `memories.max_unused_days` | (config-reference 목록에 존재) |
  | `memories.min_rollout_idle_hours` | (config-reference 목록에 존재) |
- 동작 특성: 메모리는 채팅 종료 직후가 아니라 **백그라운드 모드에서 갱신**된다. 잔여 레이트리밋 비율이 설정 임계값 아래로 떨어지면 메모리 생성을 건너뛴다.
- **핵심 인용 (원문):** "Keep required team guidance in `AGENTS.md` or checked-in documentation. Treat memories as a helpful recall layer, not as the only source for rules that must always apply."
- Claude Code 대응 관점 메모: 위 인용이 **Codex 문서의 가장 실용적인 설계 원칙 중 하나**다 — "반드시 지켜야 할 규칙은 파일(AGENTS.md)에, 메모리는 회상 보조층에". Claude Code에서 CLAUDE.md와 대화 컨텍스트를 나누는 기준으로 그대로 인용 가능. `features.memories = false`가 기본값(Experimental)인 점도 주목.

---

### Chronicle
- URL: https://learn.chatgpt.com/codex/customization/chronicle
- 검색: 2026-08-02 기준
- 핵심 내용: **ChatGPT Pro 구독자 대상 macOS 전용 opt-in 리서치 프리뷰.** 최근 화면 컨텍스트를 Codex 메모리에 편입해, 매번 상황을 다시 설명하지 않아도 되게 한다. 관련 소스를 식별하고 사용자의 도구·워크플로를 학습하는 데 도움을 준다.
- 요구 조건:
  - ChatGPT **Pro** 구독
  - macOS 기기
  - **Settings > Personalization**에서 Memories 활성화
  - macOS **Screen Recording**과 **Accessibility** 권한
- 경로 (원문 그대로):
  | 대상 | 경로 | 보존 |
  |---|---|---|
  | 화면 캡처 임시 저장 | `$TMPDIR/chronicle/screen_recording/` | **6시간 후 삭제** |
  | 생성된 메모리 | `~/.codex/memories_extensions/chronicle/` | 암호화되지 않은 마크다운 파일 |
- **핵심 인용 (원문):**
  - 레이트리밋: "Chronicle works by running sandboxed agents in the background to generate memories from captured screen images. These agents currently consume rate limits quickly."
  - 보안: "Using Chronicle increases risk to prompt injection attacks from screen content."
- 데이터 처리: 스크린샷은 메모리 생성을 위해 서버 측에서 처리되지만, 법적 요구가 없는 한 OpenAI가 보관하지 않으며 모델 학습에 쓰이지 않는다.
- 제어: 메뉴 바 아이콘으로 일시정지·재개, Settings에서 완전 비활성화. 채팅 세션별 메모리 사용 제어도 가능.
- Claude Code 대응 관점 메모: Claude Code에 대응물 없음. Appshots(수동 1회 캡처)와 대비되는 **상시 화면 관찰형 메모리**로, "에이전트가 개발자의 작업 환경을 지속 관측한다"는 방향의 가장 공격적인 사례. 프롬프트 인젝션 리스크를 문서가 명시적으로 경고한다는 점이 인용 가치가 높다.

---

### CLI customization
- URL: https://learn.chatgpt.com/codex/cli-customization
- 검색: 2026-08-02 기준
- 핵심 내용: Codex 터미널 인터페이스·에디터·자동완성·단축키 커스터마이징.
- **구문 강조·테마:**
  - TUI는 마크다운 펜스 코드 블록과 파일 diff를 구문 강조한다.
  - `/theme` — 테마 피커를 열어 미리보고 선택을 `$CODEX_HOME/config.toml`의 `tui.theme`에 저장.
  - 커스텀 테마: `.tmTheme` 파일을 **`$CODEX_HOME/themes`** 에 두면 피커에서 선택 가능.
- **셸 자동완성:** Bash, Z shell, Fish, PowerShell 지원.
  ```
  eval "$(codex completion zsh)"
  ```
  `command not found: compdef` 오류 시:
  ```
  autoload -Uz compinit && compinit
  eval "$(codex completion zsh)"
  ```
  셸 재시작 후 `codex` + Tab으로 확인.
- **프롬프트 에디터:** 긴 프롬프트는 컴포저에서 **Ctrl+G** 를 눌러 `VISUAL` 환경 변수(미설정 시 `EDITOR`)로 지정된 에디터를 연다. 저장하고 닫으면 텍스트가 컴포저로 돌아온다.
- 관련 설정 키: `tui.theme`, `tui.keymap.<context>.<action>`, `tui.status_line`, `tui.terminal_title`, `tui.vim_mode_default`, `tui.raw_output_mode`, `tui.alternate_screen`
- Claude Code 대응 관점 메모: `codex completion zsh` ↔ Claude Code에는 셸 자동완성 명령이 표준 문서화돼 있지 않음. `Ctrl+G` 외부 에디터 ↔ Claude Code의 `Ctrl+O`/외부 에디터 열기. `$CODEX_HOME/themes` .tmTheme 지원은 Claude Code의 테마(내장 프리셋)보다 확장성이 크다.

---

## 5. 에이전트 구성 (Agent Configuration)

### Custom instructions with AGENTS.md
- URL: https://learn.chatgpt.com/codex/agent-configuration/agents-md
- 검색: 2026-08-02 기준
- 핵심 내용: Codex가 `AGENTS.md` 파일을 읽어 프로젝트에 커스텀 지침·컨텍스트를 적용하는 방식.
- **탐색·우선순위 (원문 그대로 인용):**
  > "Discovery follows this precedence order:
  > 1. **Global scope:** In your Codex home directory (defaults to `~/.codex`), Codex reads `AGENTS.override.md` if it exists. Otherwise, Codex reads `AGENTS.md`.
  > 2. **Project scope:** Starting at the project root, Codex walks down to your current working directory, checking for `AGENTS.override.md`, then `AGENTS.md` in each directory.
  > 3. **Merge order:** Codex concatenates files from the root down. Files closer to your current directory override earlier guidance because they appear later in the combined prompt."
- **`AGENTS.override.md` 동작 (원문 인용):**
  > "Use `~/.codex/AGENTS.override.md` when you need a temporary global override without deleting the base file. Remove the override to restore the shared guidance."
- 예시 코드 블록 (원문 그대로):

  **전역 지침**
  ```markdown
  # ~/.codex/AGENTS.md

  ## Working agreements

  - Always run `npm test` after modifying JavaScript files.
  - Prefer `pnpm` when installing dependencies.
  - Ask for confirmation before adding new production dependencies.
  ```

  **프로젝트 수준**
  ```markdown
  # AGENTS.md

  ## Repository expectations

  - Run `npm run lint` before opening a pull request.
  - Document public utilities in `docs/` when you change behavior.
  ```

  **중첩 디렉터리 오버라이드**
  ```markdown
  # services/payments/AGENTS.override.md

  ## Payments service rules

  - Use `make test-payments` instead of `npm test`.
  - Never rotate API keys without notifying the security channel.
  ```
- **전역 지침 생성:**
  ```
  mkdir -p ~/.codex
  ```
- **코드 리뷰 규칙:** 해당 `AGENTS.md`에 `## Code Review Rules` 섹션을 넣으면 GitHub 코드 리뷰 자동화의 체크로 쓰인다.
- **폴백 파일명 커스터마이즈** (`~/.codex/config.toml`):
  ```toml
  project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
  project_doc_max_bytes = 65536
  ```
- **검증:**
  ```
  codex --ask-for-approval never "Summarize current instructions"
  ```
  → 파일들이 올바른 우선순위로 로드됐는지 확인.
- **트러블슈팅:** `AGENTS.override.md` 존재 여부 확인, 내용이 비어 있지 않은지 확인, 설정 문법 확인, Codex 재시작으로 지침 체인 재구성.
- Claude Code 대응 관점 메모: **이 페이지가 그룹 B에서 Claude Code 대응이 가장 직접적이다.** `AGENTS.md` ↔ `CLAUDE.md`, `AGENTS.override.md` ↔ `CLAUDE.local.md`(사용 중단됨)/`~/.claude/CLAUDE.md`. 디렉터리 하향 탐색 + 가까운 파일이 나중에 붙어 우선한다는 병합 규칙도 Claude Code와 동일한 발상. 차이: Codex는 **`project_doc_max_bytes`로 지침 바이트 예산을 강제**하고 **`project_doc_fallback_filenames`로 파일명 자체를 커스터마이즈**할 수 있다(Claude Code는 `CLAUDE.md` 고정). `## Code Review Rules` 섹션 규약도 Codex 고유.

---

### Subagents
- URL: https://learn.chatgpt.com/codex/agent-configuration/subagents
- 검색: 2026-08-02 기준
- 핵심 내용 (원문): "ChatGPT Work and Codex can run subagent workflows by spawning specialized agents in parallel and then collecting their results in one response."
- **왜 도움이 되는가:** 서브에이전트는 **context pollution**과 **context rot**을 해결한다 — 잡음이 많은 중간 작업을 메인 스레드 밖으로 옮겨, 주 에이전트가 요구사항과 결정에 집중하게 한다.
- **커스텀 에이전트 정의 파일 위치:**
  - `~/.codex/agents/` (개인)
  - `.codex/agents/` (프로젝트 스코프)
  - 파일 형식: **TOML**
- **필드:**
  | 필드 | 필수 | 설명 |
  |---|---|---|
  | `name` | 필수 | 스폰 시 쓰는 에이전트 식별자 |
  | `description` | 필수 | 언제 이 에이전트를 쓸지에 대한 사람 대상 안내 |
  | `developer_instructions` | 필수 | 핵심 행동 지침 |
  | `model` | 선택 | 모델 지정 |
  | `model_reasoning_effort` | 선택 | 추론 강도 |
  | `sandbox_mode` | 선택 | 샌드박스 정책 |
  | `mcp_servers` | 선택 | MCP 서버 |
  | `skills.config` | 선택 | 스킬 설정 |
- **모델 선택 (2026-08 기준):**
  | 모델 | 용도 |
  |---|---|
  | `gpt-5.6` | 가장 까다로운 작업 |
  | `gpt-5.6-terra` | 속도 중심 작업 |
  | `gpt-5.6-luna` | 빠르고 범위가 좁은 작업 |
  | `gpt-5.3-codex-spark` | (예시 파일에서 사용) 빠른 실시간 코딩 |
- **Reasoning effort 레벨 (서브에이전트 문서 기준):** `ultra`, `max`, `xhigh`, `high`, `medium`, `low`
  > **⚠️ 대조 필요:** config-sample과 config-basic은 `model_reasoning_effort`의 값을 `minimal | low | medium | high | xhigh`로 표기한다. 서브에이전트 문서만 `ultra`·`max`를 추가로 언급한다 — fact-checker는 두 페이지를 함께 대조할 것.
- **전역 `[agents]` 설정 키:**
  | 키 | 타입 | 설명 |
  |---|---|---|
  | `agents.enabled` | boolean | 멀티에이전트 도구 활성/비활성 (기본 true) |
  | `agents.max_concurrent_threads_per_session` | number | 동시 스폰 스레드 상한 (주 스레드 제외) |
  | `agents.default_subagent_model` | string | 스폰되는 에이전트의 기본 모델 |
  | `agents.default_subagent_reasoning_effort` | string | 스폰되는 에이전트의 기본 추론 강도 |
  | `agents.interrupt_message` | boolean | 에이전트 턴 중단 시 모델이 볼 수 있는 메시지 기록 (기본 true) |
  | `agents.<name>.description` | string | 에이전트 설명 |
  | `agents.<name>.config_file` | string | 에이전트 정의 파일 경로 (정의한 config.toml 기준 상대 경로) |
  | `agents.max_threads` | number | (config-reference 목록에 존재) |
- 코드/설정 예시 (원문 그대로):
  ```toml
  [agents]
  max_concurrent_threads_per_session = 8
  ```
  **pr-explorer.toml:**
  ```toml
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
  (`reviewer.toml`, `docs-researcher.toml`도 같은 구조에 설정만 다름)
- **문서 제공 예시 프롬프트 (원문 그대로):**
  > "Review this branch against main. Have pr_explorer map the affected code paths, reviewer find real risks, and docs_researcher verify the framework APIs that the patch relies on."

  > "Investigate why the settings modal fails to save. Have browser_debugger reproduce it, code_mapper trace the responsible code path, and ui_fixer implement the smallest fix once the failure mode is clear."
- 제공 예시 구성 2종: **PR 리뷰** (explorer / reviewer / docs researcher 3개 에이전트), **프론트엔드 디버깅** (code mapper / browser debugger / UI fixer).
- Claude Code 대응 관점 메모: **Claude Code 서브에이전트와 가장 직접 대응되는 페이지.** 차이가 명확하다 — Claude Code는 `.claude/agents/*.md`에 **YAML frontmatter + 마크다운 본문**, Codex는 `.codex/agents/*.toml`에 **순수 TOML + `developer_instructions` 멀티라인 문자열**. `name`/`description`/`model`은 1:1 대응(Claude Code의 `tools` 필드 ↔ Codex의 `mcp_servers`/`skills.config`/`sandbox_mode`). `agents.max_concurrent_threads_per_session` ↔ Claude Code에는 명시적 동시 서브에이전트 상한 설정이 없음. **"context pollution / context rot"** 이라는 용어 정의는 인용 가치가 높다.

---

### Speed (Fast mode & Codex-Spark)
- URL: https://learn.chatgpt.com/codex/agent-configuration/speed
- 검색: 2026-08-02 기준
- 핵심 내용: 속도 향상 두 가지 경로 — **Fast mode**(서비스 티어 조정)와 **Codex-Spark**(별도 모델).
- **Fast mode (2026-08 기준 수치, 원문 인용):**
  - "Codex offers the ability to increase the speed of the model for increased credit consumption."
  - 속도: "increases supported model speed by **1.5x**"
  - 지원 모델: **GPT-5.6, GPT-5.5, GPT-5.4**
  - 크레딧 소모: "GPT-5.6 and GPT-5.5 consume credits at **2.5x** the Standard rate; GPT-5.4 consumes credits at **2x** the Standard rate"
  - API 관련: "API usage employs token pricing rather than credit multipliers; API Priority processing costs **2x** the Standard API token rate for GPT-5.6"
- 명령·설정 키:
  - CLI/슬래시: `/fast on`, `/fast off`, `/fast status`
  - config.toml: `service_tier = "fast"` + `[features].fast_mode = true`
- 가용 표면: ChatGPT 데스크톱, Codex CLI, IDE 확장.
- **Codex-Spark:** `GPT-5.3-Codex-Spark`는 모드 조정이 아니라 **실시간 코딩 작업에 최적화된 별개의 더 빠른 모델**이다. 리서치 프리뷰 기간 동안 **ChatGPT Pro 구독자 한정**이며 **별도 사용 한도**를 가진다.
- **수집 한계:** 2차 요청에서도 모델별 상세 비교 표나 Codex-Spark의 구체적 배수 수치는 페이지에서 확인되지 않았다. 위 수치가 문서에 명시된 전부다.
- Claude Code 대응 관점 메모: Claude Code에 서비스 티어 다이얼(`/fast`)은 없다. 가장 가까운 것은 모델 선택(Opus/Sonnet/Haiku)과 reasoning effort. **"속도를 크레딧으로 산다"** 는 명시적 트레이드오프를 UI 명령으로 노출한 점이 설계 관점의 대비 포인트.

---

### Rules (execpolicy)
- URL: https://learn.chatgpt.com/codex/agent-configuration/rules
- 검색: 2026-08-02 기준
- 핵심 내용: **Codex가 샌드박스 밖에서 실행할 수 있는 명령을 제어하는 규칙 시스템.**
- 규칙 파일 위치: 활성 설정 계층 옆의 `rules/` 폴더에 `.rules` 파일. 예: **`~/.codex/rules/default.rules`**
- 규칙 언어: **Starlark** (Python 유사 문법)
- **`prefix_rule()` 필드:**
  | 필드 | 필수 | 설명 |
  |---|---|---|
  | `pattern` | 필수 | 명령어 접두사를 정의하는 비어 있지 않은 리스트 |
  | `decision` | 선택 | `"allow"`(기본값) / `"prompt"` / `"forbidden"` |
  | `justification` | 선택 | 규칙의 이유 |
  | `match` | 선택 | 규칙 검증용 매칭 예제 명령 |
  | `not_match` | 선택 | 규칙 검증용 비매칭 예제 명령 |
- **`decision` 값 의미:**
  | 값 | 동작 |
  |---|---|
  | `allow` | 샌드박스 외부에서 프롬프트 없이 실행 |
  | `prompt` | 일치하는 호출마다 실행 전 프롬프트 |
  | `forbidden` | 프롬프트 없이 요청 차단 |
- 코드/설정 예시 (원문 그대로):
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
- **셸 래퍼 처리:** `bash -lc`, `bash -c` 같은 셸 래퍼에서 —
  - **안전한 경우**: `&&`, `||`, `;`, `|`로 연결된 명령을 **분리해서 각각 평가**
  - **복잡한 경우**: 리다이렉션, 변수 치환 등이 있으면 **전체를 하나의 명령으로 취급**
- **규칙 테스트 명령 (원문 그대로):**
  ```bash
  codex execpolicy check --pretty \
    --rules ~/.codex/rules/default.rules \
    -- gh pr view 7888 --json title,body,comments
  ```
  이 명령은 규칙이 특정 명령에 어떻게 적용되는지 보여주는 JSON 출력을 만든다.
- 관련 설정 키: `approval_policy.granular.rules` (granular 승인 정책에서 rules 카테고리 제어)
- Claude Code 대응 관점 메모: **Claude Code `settings.json`의 `permissions.allow` / `permissions.deny` / `permissions.ask`와 직접 대응.** Claude Code는 `Bash(gh pr view:*)` 같은 문자열 패턴, Codex는 Starlark 함수 호출로 접두사 리스트를 쓴다. Codex 쪽 강점: (1) `justification` 필드로 **규칙에 이유를 문서화**, (2) `match`/`not_match`로 **규칙 자체를 테스트**, (3) `codex execpolicy check`로 **규칙을 CI에서 검증** 가능. Claude Code에는 규칙 단위 테스트 하네스가 없다 — 책의 비교 챕터에서 강조할 만한 차이.

---

## 6. 확장 (Extend)

### Model Context Protocol (MCP)
- URL: https://learn.chatgpt.com/codex/extend/mcp
- 검색: 2026-08-02 기준
- 핵심 내용: Codex를 MCP 서버에 연결해 서드파티 도구·문서에 접근하게 한다.
- **지원 기능 3범주 (원문):**
  1. "STDIO servers": 로컬 프로세스, 환경 변수 지원
  2. "Streamable HTTP servers": 원격 접근, bearer token 및 OAuth 인증
  3. "Server instructions": 초기화 시 읽는 도구 간 공통 안내
- **표면별 설정 방법:**
  | 표면 | 방법 |
  |---|---|
  | ChatGPT 데스크톱 앱 | Settings → MCP servers → Add server → STDIO 또는 Streamable HTTP 전송 선택 → 재시작 |
  | Codex CLI | `codex mcp add <server-name> -- <command>` (환경 변수는 `--env` 플래그) |
  | IDE 확장 | 기어 메뉴 → MCP servers → Add server → 확장 재시작 |
- **CLI 명령 (원문 그대로):**
  ```
  codex mcp add <server-name> --env VAR1=VALUE1 -- <stdio server-command>
  codex mcp list
  codex mcp --help
  codex mcp login <server-name>
  ```
- **STDIO 서버 설정 옵션:** `command`, `args`, `env`, `env_vars`, `cwd`, `experimental_environment`
- **Streamable HTTP 서버 설정 옵션:** `url`, `auth`, `bearer_token_env_var`, `http_headers`, `env_http_headers`
- **공통 옵션:** `startup_timeout_sec`, `tool_timeout_sec`, `enabled`, `required`, `enabled_tools`, `disabled_tools`, `default_tools_approval_mode`, `tools.<tool>.approval_mode`
- **최상위 설정 옵션:** `mcp_oauth_callback_port`, `mcp_oauth_callback_url`
- 코드/설정 예시 (원문 그대로):
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
- **추천 MCP 서버 (문서 목록):** OpenAI Docs MCP, Context7, Figma(로컬/원격), Playwright, Chrome Developer Tools, Sentry, GitHub MCP server
- 수집 한계: 문서는 tools와 서버 기능 위주이며, resources·prompts·sampling을 별도 설정 요소로 상세히 다루지는 않는다.
- Claude Code 대응 관점 메모: `codex mcp add` ↔ `claude mcp add`, `codex mcp list` ↔ `claude mcp list`, `.mcp.json` ↔ `[mcp_servers]` TOML 테이블. **Codex 고유:** `required = true`(초기화 실패 시 시작/재개 자체를 실패시킴), `enabled_tools`/`disabled_tools` 도구 단위 allow/deny, `default_tools_approval_mode`(auto/prompt/writes/approve) — Claude Code는 MCP 도구 단위 승인 모드를 이 정도로 세분화하지 않는다.

---

### Record & Replay
- URL: https://learn.chatgpt.com/codex/extend/record-and-replay
- 검색: 2026-08-02 기준
- 핵심 내용: **워크플로를 시연해 재사용 가능한 스킬로 바꾸는 기능.** macOS 전용.
- 요구 조건·가용성:
  - **macOS 전용**
  - 초기 가용성에서 **EEA, UK, 스위스 제외**
  - **Computer Use가 사용 가능하고 활성화**되어 있어야 함
- 사용 절차:
  1. ChatGPT 또는 Codex에서 Plugins 열기
  2. 메뉴에서 **"Record a skill"** 선택
  3. 제안된 프롬프트 검토·수정
  4. 녹화 권한 부여
  5. Mac에서 워크플로 시연
  6. 완료 시 녹화 중지
- 생성 결과: 시스템이 동작을 관찰해 **언제 이 스킬을 쓰는지, 어떤 입력이 필요한지, 어떤 단계를 거치는지, 성공을 어떻게 검증하는지**를 설명하는 스킬을 만든다.
- 재생: 새 채팅에서 생성된 스킬을 참조하고 가변 입력(파일·날짜 등)을 제공하면, Computer Use·브라우저 액션·플러그인 등 사용 가능한 도구로 워크플로를 실행한다.
- 사용 사례: 경비 처리, 주차 예약, 이슈 생성, 영상 게시, 리포트 다운로드.
- 모범 사례: 시연은 **짧고 완결적으로**, 민감하지 않은 현실적 입력 사용, 목표를 먼저 말하기, 이후 스킬을 다듬어 명명 규칙·판단 지점 같은 숨은 선호를 명시화.
- Claude Code 대응 관점 메모: **Claude Code에 대응물이 전혀 없는 Codex 고유 기능.** Claude Code의 스킬은 사람이 마크다운으로 작성하지만, Record & Replay는 **GUI 조작 시연 → 스킬 자동 생성**이라는 역방향 저작 경로다. "스킬을 쓰는 게 아니라 스킬을 만드는 법"을 다루는 챕터의 핵심 대비 소재.

---

### Build skills
- URL: https://learn.chatgpt.com/codex/build-skills
- 검색: 2026-08-02 기준
- 핵심 내용: ChatGPT와 Codex를 과제별 역량으로 확장하는 스킬 작성·배포. 스킬은 **open agent skills standard**를 따라 지침·리소스·선택적 스크립트를 패키징한다.
- **디렉터리 구조 (원문 그대로):**
  ```
  my-skill/
  ├── SKILL.md              (Required: instructions + metadata)
  ├── scripts/              (Optional: executable code)
  ├── references/           (Optional: documentation)
  ├── assets/               (Optional: templates, resources)
  └── agents/
      └── openai.yaml       (Optional: appearance and dependencies)
  ```
- **SKILL.md 프론트매터 (필수 2필드):**
  ```yaml
  ---
  name: skill-name
  description: Explain exactly when this skill should and should not trigger.
  ---

  Skill instructions here.
  ```
- **`agents/openai.yaml` (원문 그대로):**
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
- **호출 방식 2가지:**
  1. **Explicit invocation:** ChatGPT는 `@`, Codex CLI는 `$` 로 스킬 선택
  2. **Implicit invocation:** 과제가 description과 맞으면 시스템이 자동 선택
- **스킬 로드 경로 (Codex, 우선순위 순):**
  ```
  $CWD/.agents/skills        (repo-specific)
  $REPO_ROOT/.agents/skills  (repo-wide)
  $HOME/.agents/skills       (user-level)
  /etc/codex/skills          (admin-level)
  ```
- **스킬 생성 도구:** ChatGPT Work `@skill-creator`, Codex `$skill-creator`. 큐레이션된 스킬 설치는 `$skill-installer`.
- **배포:** 재사용 배포는 폴더 단독이 아니라 **플러그인으로 패키징**. 원문: "Bundle two or more skills together, or ship a skill alongside a connector, package them as a plugin"
- **모범 사례:** 스킬 하나는 하나의 과제에 집중 / 스크립트보다 지침 선호 / 명시적 입출력과 함께 명령형 단계로 작성 / 스킬 description에 맞춰 프롬프트를 테스트.
- 관련 설정 키: `skills.config`, `skills.config.<index>.path`, `skills.config.<index>.enabled` (삭제하지 않고 특정 스킬만 비활성화)
- Claude Code 대응 관점 메모: **Claude Code Skills와 거의 동일한 표준(`SKILL.md` + name/description frontmatter).** 차이가 명확하다 — Claude Code는 `.claude/skills/`, Codex는 `.agents/skills/`(open agent skills standard 경로). Codex 고유: (1) `agents/openai.yaml`의 **`interface`(브랜드 색·아이콘·표시명)와 `policy.allow_implicit_invocation`**, (2) `dependencies.tools`로 **스킬이 필요로 하는 MCP 서버를 선언** — Claude Code 스킬은 도구 의존성을 선언하지 않는다. (3) `/etc/codex/skills` 관리자 레벨 경로. `$` 명시 호출 ↔ Claude Code의 Skill 도구 호출.

---

### Build plugins
- URL: https://learn.chatgpt.com/codex/build-plugins
- 검색: 2026-08-02 기준
- 핵심 내용: "A plugin is an installable package that can include skills, an MCP server, or both. An MCP server can also return optional UI."
- **디렉터리 통합 (원문 요지):** ChatGPT와 Codex는 **하나의 유니버설 플러그인 디렉터리를 공유**한다. 공개 플러그인을 한 번 게시하면 두 제품의 지원 표면 모두에서 같은 목록이 발견된다. 개발 중에는 **로컬 마켓플레이스**로 패키지를 테스트한 뒤 유니버설 디렉터리에 제출한다.
- **스킬 vs 플러그인 판단 기준 (원문):** "Start with a skill when you are still iterating on one personal workflow. Build a plugin when you want to share that workflow, package related skills, connect to an external service, or distribute a stable capability to a team."
- **`@plugin-creator` 사용 (ChatGPT Work) / `$plugin-creator` (Codex):**
  ```
  @plugin-creator Create a plugin named meeting-follow-up.
  Include a skill that turns meeting notes into decisions, owners, and next steps.
  Add it to a personal marketplace so I can test it locally.
  ```
  스킬이 필요한 `.codex-plugin/plugin.json` 매니페스트를 만들고, 플러그인 폴더를 구성하며, 로컬 마켓플레이스에 등록할 수 있다.
- **생성 후 절차 (원문 그대로):**
  1. Review `.codex-plugin/plugin.json`.
  2. Check each bundled skill under `skills/`.
  3. Refresh ChatGPT or Codex and install the plugin from its local marketplace source.
  4. Test the plugin in a new conversation with representative requests.
- **수동 생성 — 최소 구조 (원문 그대로):**
  ```
  meeting-follow-up/
  ├── .codex-plugin/
  │   └── plugin.json
  └── skills/
      └── meeting-follow-up/
          └── SKILL.md
  ```
- **`.codex-plugin/plugin.json` (원문 그대로):**
  ```json
  {
    "name": "meeting-follow-up",
    "version": "1.0.0",
    "description": "Turn meeting notes into decisions and next steps",
    "skills": "./skills/"
  }
  ```
- **`skills/meeting-follow-up/SKILL.md` (원문 그대로):**
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
- **명명 규칙:** 플러그인 이름은 **kebab case**로 안정적으로. 스킬 description은 ChatGPT/Codex가 워크플로 적용 시점을 인지할 만큼 구체적으로.
- **MCP 서버 포함 시:** 먼저 그 서버를 빌드·테스트한 뒤 `@plugin-creator`에 등록된 연결 정보를 준다. 전체 MCP 서버 워크플로는 https://developers.openai.com/plugins/build/mcp-server 참조.
- **빌더 문서 링크 (원문 그대로):**
  - Plugin architecture — https://developers.openai.com/plugins/concepts/plugins
  - Building skills — https://developers.openai.com/plugins/build/skills
  - Building an MCP server — https://developers.openai.com/plugins/build/mcp-server
  - Adding optional UI — https://developers.openai.com/plugins/build/chatgpt-ui
  - Packaging a plugin — https://developers.openai.com/plugins/build/plugins
  - Testing a plugin — https://developers.openai.com/plugins/deploy/connect-chatgpt
  - Submitting and publishing — https://developers.openai.com/plugins/deploy/submission
- 관련 설정 키: `plugins.<plugin>.mcp_servers.<server>.enabled` / `.enabled_tools` / `.disabled_tools` / `.default_tools_approval_mode` / `.tools.<tool>.approval_mode`, `features.remote_plugin`
- Claude Code 대응 관점 메모: **Claude Code 플러그인과 개념·구조가 거의 동형이다** — `.codex-plugin/plugin.json` ↔ `.claude-plugin/plugin.json`(동일한 name/version/description 필드), `skills/` 디렉터리 규약도 동일, 로컬 마켓플레이스 → 공개 디렉터리 흐름도 동일. 차이: Codex는 **ChatGPT와 Codex가 하나의 유니버설 디렉터리를 공유**하고, MCP 서버가 **선택적 UI를 반환**할 수 있다(Claude Code MCP는 UI 반환 개념이 없음).

---

### Hooks
- URL: https://learn.chatgpt.com/codex/hooks
- 검색: 2026-08-02 기준
- 핵심 내용: 훅은 에이전틱 루프에 스크립트를 주입하는 확장성 프레임워크. 커스텀 로깅, 프롬프트 스캔, 메모리 요약, 검증 체크, 컨텍스트 커스터마이징에 쓴다.
- 핵심 특성:
  - **매칭되는 훅 여러 개가 동시에(concurrently) 실행**된다.
  - **관리형(managed)이 아닌 command 훅은 실행 전 신뢰 검토(trust review)가 필요**하다.
  - 훅은 대화 라이프사이클의 특정 지점에서 실행된다.
- **훅 이벤트 (전 11종):**
  - **턴 중:** `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `UserPromptSubmit`, `SubagentStop`, `Stop`
  - **세션 라이프사이클:** `SessionStart`, `SessionEnd`, `SubagentStart`
- **설정 위치 (원문):**
  ```
  ~/.codex/hooks.json  또는  ~/.codex/config.toml
  <repo>/.codex/hooks.json  또는  <repo>/.codex/config.toml
  (그리고) 활성화된 플러그인에 번들된 플러그인 매니페스트
  ```
- **구조:** 이벤트 → matcher 그룹 → 핸들러
  ```json
  {
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
      ]
    }
  }
  ```
- **핵심 필드:**
  | 필드 | 설명 |
  |---|---|
  | `type` | `"command"` |
  | `command` | 실행할 명령 |
  | `timeout` | 초 단위. **기본 600**. **단 `SessionEnd`는 1초** |
  | `statusMessage` | UI 피드백용 선택 문자열 |
  | `additionalContextLimit` | 디스크로 흘려보내기 전 토큰 임계값 |
  | `commandWindows` | Windows 전용 명령 오버라이드 |
  | `matcher` | 이벤트별 매칭 대상 (아래 표) |
- **공통 입력 (모든 훅이 JSON stdin으로 받음):** `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `permission_mode`
- **공통 출력 JSON 필드:**
  | 필드 | 타입 | 설명 |
  |---|---|---|
  | `continue` | boolean | `false`면 처리 중단 |
  | `stopReason` | string | 기록되는 종료 사유 |
  | `systemMessage` | string | UI 경고 |
  | `suppressOutput` | boolean | 파싱되지만 아직 구현되지 않음 |
- **이벤트별 상세 (원문 기반 전수):**

  | 이벤트 | matcher 대상 | 추가 입력 필드 | 출력 |
  |---|---|---|---|
  | `SessionStart` | `source` (startup, resume, clear, compact) | `source` | `hookSpecificOutput.additionalContext` |
  | `SessionEnd` | `reason` (현재 `"other"`만) | `reason` | 자문(advisory)만, 공통 출력 필드 |
  | `SubagentStart` | `agent_type` | `turn_id`, `agent_id`, `agent_type` | `hookSpecificOutput.additionalContext` |
  | `PreToolUse` | `tool_name` (Bash, apply_patch, MCP tools) | `turn_id`, `tool_name`, `tool_use_id`, `tool_input` | `permissionDecision`(deny/allow), `permissionDecisionReason`, `updatedInput` / 레거시 `{"decision":"block","reason":...}` |
  | `PermissionRequest` | `tool_name` (Bash, apply_patch, MCP names) | `turn_id`, `tool_name`, `tool_input`, `tool_input.description` | `hookSpecificOutput.decision.behavior`(allow/deny) + `.message` |
  | `PostToolUse` | `tool_name` | `turn_id`, `tool_name`, `tool_use_id`, `tool_input`, `tool_response` | `decision: "block"` + `reason`, `hookSpecificOutput.additionalContext` |
  | `PreCompact` | `trigger` (manual, auto) | `turn_id`, `trigger` | 공통 출력 필드 |
  | `PostCompact` | `trigger` (manual, auto) | `turn_id`, `trigger` | 공통 출력 필드 |
  | `UserPromptSubmit` | **matcher 미지원** | `turn_id`, `prompt` | `hookSpecificOutput.additionalContext` 또는 `{"decision":"block","reason":...}` |
  | `SubagentStop` | `agent_type` | `turn_id`, `agent_id`, `agent_type`, `agent_transcript_path`, `stop_hook_active`, `last_assistant_message` | `{"decision":"block","reason":...}` |
  | `Stop` | **matcher 미지원** | `turn_id`, `stop_hook_active`, `last_assistant_message` | `{"decision":"block","reason":...}` |

- **출력 JSON 예시 (원문 그대로):**
  ```json
  {
    "hookSpecificOutput": {
      "hookEventName": "SessionStart",
      "additionalContext": "string"
    }
  }
  ```
  ```json
  {
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny|allow",
      "permissionDecisionReason": "string",
      "updatedInput": {"command": "string"}
    }
  }
  ```
  ```json
  {
    "hookSpecificOutput": {
      "hookEventName": "PermissionRequest",
      "decision": {
        "behavior": "allow|deny",
        "message": "string"
      }
    }
  }
  ```
  ```json
  {
    "decision": "block",
    "reason": "string",
    "hookSpecificOutput": {
      "hookEventName": "PostToolUse",
      "additionalContext": "string"
    }
  }
  ```
  ```json
  {
    "hookSpecificOutput": {
      "hookEventName": "UserPromptSubmit",
      "additionalContext": "string"
    }
  }
  ```
- **신뢰·관리:** 관리형이 아닌 훅은 `/hooks` 명령으로 명시적 신뢰 검토를 거쳐야 한다. `requirements.toml`에서 온 관리형 훅은 엔터프라이즈가 제어하며 자동으로 신뢰된다. 일회성 자동화를 위해 검토를 우회하려면 **`--dangerously-bypass-hook-trust`**.
- **비활성화:** `config.toml`에 `[features] hooks = false`
- **플러그인 번들 훅:** 플러그인은 `hooks/hooks.json`을 정의하거나 `.codex-plugin/plugin.json`의 `hooks` 항목으로 오버라이드할 수 있다. 명령은 **`PLUGIN_ROOT`** 와 **`PLUGIN_DATA`** 환경 변수를 받는다.
- Claude Code 대응 관점 메모: **Claude Code hooks와 이름·구조가 놀랍도록 일치한다.** 동일 이벤트: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`, `PreCompact`. 동일 스키마 요소: `matcher` 그룹 → `hooks[]` 배열, `type: "command"`, JSON stdin(`session_id`, `transcript_path`, `cwd`, `hook_event_name`), `hookSpecificOutput.additionalContext`, `permissionDecision`, `{"decision":"block","reason":...}`. **Codex 고유:** `PermissionRequest`, `PostCompact`, `SubagentStart` 이벤트 / `statusMessage`(UI 진행 표시) / `additionalContextLimit`(토큰 임계 넘으면 디스크로) / `commandWindows`(Windows 명령 분기) / **훅 신뢰 검토(trust review) 절차와 `--dangerously-bypass-hook-trust`**. Claude Code에는 훅 신뢰 게이트가 없다 — 보안 비교 챕터의 핵심 소재.

---

## 7. Windows

### ChatGPT desktop app for Windows
- URL: https://learn.chatgpt.com/codex/windows/windows-app
- 검색: 2026-08-02 기준
- 핵심 내용: 프로젝트 관리·병렬 채팅·결과 검토를 위한 Windows 데스크톱 앱. PowerShell, Windows 샌드박스, WSL2 통합을 네이티브로 지원한다.
- 주요 기능: PowerShell에서 실행 시 **Windows 샌드박스 네이티브 지원**, 사이드바 프로젝트 관리, 통합 터미널(PowerShell / Command Prompt / Git Bash / WSL), 핵심 워크플로(worktrees, scheduled tasks, Git, browser, file previews, plugins, skills), 승인 기반 샌드박싱.
- 설치 (원문 그대로):
  ```
  winget install --id 9PLM9XGG6VKS -s msstore
  ```
  또는 Microsoft Store.
- 커스터마이징: Preferred editor(VS Code, Visual Studio 등), Integrated terminal 선택, Agent를 Windows 네이티브로 실행할지 WSL2로 전환할지 선택.
- **WSL2 통합 주의사항 (성능):** 프로젝트는 `\\wsl$\` 경로에서 접근할 수 있으나, **안정적 성능을 위해서는 프로젝트를 Windows 파일시스템에 두고 WSL에서 `/mnt/<drive>/...` 로 접근**하라 (WSL 파일시스템에서 직접 여는 것보다 낫다).
  > **⚠️ 대조 필요:** `/codex/windows/wsl` 페이지는 반대 권고("Store repositories in Linux home directory `~/code/` rather than Windows-mounted paths `/mnt/c/…` for better performance")를 한다. 두 페이지의 권고가 방향이 다르므로 fact-checker는 원문을 직접 대조할 것.
- 권장 개발 도구: Git, Node.js, Python, .NET SDK, GitHub CLI — 모두 `winget`으로 설치 가능.
- Claude Code 대응 관점 메모: Claude Code도 Windows에서 네이티브/WSL 양쪽을 지원하지만, **Codex처럼 OS 네이티브 샌드박스(elevated/unelevated)를 갖추지는 않았다.** 이 차이가 Windows 챕터의 핵심.

---

### Windows sandbox
- URL: https://learn.chatgpt.com/codex/windows/windows-sandbox
- 검색: 2026-08-02 기준
- 핵심 내용: Windows에서 Codex를 네이티브 데스크톱 앱·CLI·IDE 확장으로 쓸 때의 샌드박스. "The app can run natively in PowerShell with a Windows sandbox instead of requiring WSL or a virtual machine." — 경계 지어진 파일시스템·네트워크 권한을 강제하면서도 Windows 네이티브 워크플로를 유지한다.
- **샌드박스 2모드:**
  | 모드 | 설명 |
  |---|---|
  | `elevated` | **선호되는 네이티브 Windows 샌드박스.** 전용 저권한 샌드박스 사용자, 파일시스템 권한 경계, 방화벽 규칙, 로컬 정책 변경을 사용 |
  | `unelevated` | **폴백.** 제한된 Windows 토큰으로 명령 실행, ACL 기반 파일시스템 경계, 환경 레벨 오프라인 제어 |
- 설정 (원문 그대로):
  ```toml
  [windows]
  sandbox = "elevated" # or "unelevated"
  ```
- 엔터프라이즈 설정 (원문 그대로):
  ```toml
  [windows]
  allowed_sandbox_implementations = ["elevated"]
  ```
- 샌드박스 읽기 권한 부여 (원문 그대로):
  ```
  /sandbox-add-read-dir C:\absolute\directory\path
  ```
- **Windows 버전 지원:**
  | 버전 | 지원 |
  |---|---|
  | Windows 11 | 권장 (Recommended) |
  | 최신 상태로 업데이트된 Windows 10 | 최선 노력 (Best effort) |
  | 구버전 Windows 10 빌드 | 권장하지 않음 (Not recommended) |
- 트러블슈팅 항목: 네이티브 샌드박스 설정 실패, unelevated 샌드박스로 폴백, **Windows 오류 1385**, 폴더 권한 경고, 네트워크 접근 문제, 샌드박싱 깨짐, IDE 확장 무응답.
- 관련 설정 키: `windows.sandbox`, `windows.sandbox_private_desktop`, `windows_wsl_setup_acknowledged`, `computer_use.windows.always_allowed_app_ids`
- 관련 슬래시 명령: `/setup-default-sandbox`(elevated Windows 샌드박스 설정), `/sandbox-add-read-dir`
- Claude Code 대응 관점 메모: Claude Code에는 Windows 네이티브 샌드박스 개념이 없다(macOS Seatbelt/Linux bubblewrap 기반 샌드박스는 있음). **elevated/unelevated 2단 폴백과 `allowed_sandbox_implementations` 엔터프라이즈 강제**는 Codex 고유.

---

### WSL
- URL: https://learn.chatgpt.com/codex/windows/wsl
- 검색: 2026-08-02 기준
- 핵심 내용: WSL에서 Codex를 실행·문제 해결하는 방법.
- **WSL2 vs WSL1:** "Run Codex inside the Linux environment instead of using the native Windows sandbox." **WSL1 지원은 버전 0.114에서 종료**되었고, Linux 샌드박스는 이제 **`bubblewrap`** 을 사용한다.
  > 버전 정보: **Codex 0.114 / 2026 기준** — WSL1 지원 종료.
- **WSL에서 VS Code 실행:**
  - 전제: WSL이 설치된 Windows + WSL 확장이 설치된 VS Code
  - 명령: WSL 터미널에서 `code .`
  - 확인: 초록색 상태 바에 **"WSL: <distro>"** 표시
- **CLI 설치 (원문 그대로):**
  ```
  wsl --install
  wsl
  curl -fsSL https://chatgpt.com/codex/install.sh | sh
  codex
  ```
- **모범 사례:** 저장소를 **Linux 홈 디렉터리(`~/code/`)** 에 두고, Windows 마운트 경로(`/mnt/c/…`)는 피할 것 — 성능 때문. Windows 탐색기에서 WSL 파일 접근은 `\\wsl$\Ubuntu\home\<user>`.
- **트러블슈팅:**
  - 저장소가 느림 → `/mnt/c` 회피, `wsl --update`로 WSL 갱신
  - `codex` 바이너리 없음 → `which codex`로 확인
- 관련 설정: `chatgpt.runCodexInWindowsSubsystemForLinux` (IDE 확장 설정, 기본 `false`), `windows_wsl_setup_acknowledged`
- Claude Code 대응 관점 메모: Claude Code도 WSL 설치 경로가 있으나(`curl ... | bash`), Codex는 **WSL vs 네이티브 샌드박스를 명시적 선택지로 문서화**하고 IDE 확장 설정 키로 토글까지 노출한다. 설치 스크립트 URL(`https://chatgpt.com/codex/install.sh`) ↔ Claude Code의 `https://claude.ai/install.sh`.

---

## 8. 개발자 명령·설정 (Developer)

### Developer commands (CLI 전수)
- URL: https://learn.chatgpt.com/codex/developer-commands
- 검색: 2026-08-02 기준
- 핵심 내용: Codex CLI 명령, 전역 플래그, 터미널 UI 내 슬래시 명령의 종합 레퍼런스.
- **전역 플래그 (원문 그대로, 15개 전수):**

  | Flag | Type | Purpose |
  |---|---|---|
  | `--add-dir` | path | "Grant additional directories write access alongside the main workspace" |
  | `--ask-for-approval, -a` | untrusted \| on-request \| never | Control approval timing before command execution |
  | `--cd, -C` | path | Set working directory for the agent |
  | `--config, -c` | key=value | "Override configuration values" |
  | `--dangerously-bypass-approvals-and-sandbox, --yolo` | boolean | Run without approvals or sandboxing (dangerous) |
  | `--disable` | feature | Force-disable a feature flag |
  | `--enable` | feature | Force-enable a feature flag |
  | `--image, -i` | path | "Attach one or more image files to the initial prompt" |
  | `--local-provider` | lmstudio \| ollama | Choose local provider for OSS models |
  | `--model, -m` | string | Override configured model |
  | `--oss` | boolean | "Use a local open source model provider" |
  | `--profile, -p` | string | Layer additional config file |
  | `--remote` | ws://host:port \| wss://host:port | Connect to remote app-server endpoint |
  | `--sandbox, -s` | read-only \| workspace-write \| danger-full-access | Select sandbox policy |
  | `--search` | boolean | Enable live web search |

- **CLI 명령 (원문 그대로, 성숙도 라벨 포함, 27개 전수):**

  | Command | Maturity | Description |
  |---|---|---|
  | `codex` | Stable | "Launch the terminal UI" with optional prompt or image attachments |
  | `codex app` | Stable | "Launch the ChatGPT desktop app on macOS or Windows" |
  | `codex app-server` | Experimental | "Launch the Codex app server for local development or debugging" |
  | `codex apply` | Stable | "Apply the latest diff generated by a Codex cloud chat to your local working tree" |
  | `codex archive` | Stable | "Archive a saved interactive session by session ID or session name" |
  | `codex cloud` | Experimental | "Browse or execute Codex cloud chats from the terminal" |
  | `codex completion` | Stable | "Generate shell completion scripts for Bash, Zsh, Fish, or PowerShell" |
  | `codex debug app-server send-message-v2` | Experimental | Debug app-server with built-in test client |
  | `codex debug models` | Experimental | "Print the raw model catalog Codex sees" |
  | `codex debug prompt-input` | Experimental | "Render the model-visible prompt input list as JSON" |
  | `codex delete` | Stable | "Permanently delete a saved interactive session" |
  | `codex doctor` | Stable | "Generate a diagnostic report for local installation, config, auth, runtime, Git, terminal" |
  | `codex exec` | Stable | "Run Codex non-interactively" with JSONL output option |
  | `codex execpolicy` | Experimental | Evaluate execpolicy rule files for command authorization |
  | `codex features` | Stable | "List feature flags and persistently enable or disable them" |
  | `codex fork` | Stable | "Fork a previous interactive session into a new chat" |
  | `codex login` | Stable | "Authenticate Codex using ChatGPT OAuth, device auth, an API key, or an access token" |
  | `codex logout` | Stable | "Remove stored authentication credentials" |
  | `codex mcp` | Stable | "Manage Model Context Protocol servers" (list, add, remove, authenticate) |
  | `codex mcp-server` | Stable | "Run Codex itself as an MCP server over stdio" |
  | `codex plugin` | Stable | "Install, list, and remove plugins from configured marketplace sources" |
  | `codex plugin marketplace` | Stable | "Add, list, upgrade, or remove plugin marketplaces" |
  | `codex remote-control` | Experimental | "Run or manage remote control for the local app-server" |
  | `codex resume` | Stable | "Continue a previous interactive session by ID or resume the most recent chat" |
  | `codex review` | Stable | "Run a non-interactive review of uncommitted changes" |
  | `codex sandbox` | Stable | "Run arbitrary commands inside Codex-provided macOS, Linux, or Windows sandboxes" |
  | `codex unarchive` | Stable | "Restore an archived interactive session" |
  | `codex update` | Stable | "Check for and apply a Codex CLI update" |

- **내장 슬래시 명령 (TUI, 원문 그대로 — reference/slash-commands와 목록이 다르다):**

  | Command | Purpose |
  |---|---|
  | `/permissions` | Set what Codex can do without asking first |
  | `/ide` | "Include open files, current selection, and other IDE context" |
  | `/keymap` | Remap TUI keyboard shortcuts |
  | `/vim` | Toggle Vim mode for the composer |
  | `/setup-default-sandbox` | Set up elevated Windows sandbox |
  | `/sandbox-add-read-dir` | Grant sandbox read access to extra directory |
  | `/agent`, `/subagents` | Switch the active agent thread |
  | `/apps` | "Browse apps (connectors) and insert them into your prompt" |
  | `/plugins` | "Browse installed and discoverable plugins" |
  | `/hooks` | "View and manage lifecycle hooks" |
  | `/clear` | "Clear the terminal and start a fresh chat" |
  | `/rename` | Rename the current chat |
  | `/archive` | "Archive the current session and exit Codex" |
  | `/delete` | "Permanently delete the current session and exit Codex" |
  | `/compact` | "Summarize the visible chat to free tokens" |
  | `/copy` | "Copy the latest completed Codex output" |
  | `/diff` | "Show the Git diff, including files Git isn't tracking yet" |
  | `/exit` | "Exit the CLI (same as /quit)" |
  | `/experimental` | Toggle experimental features |
  | `/approve` | Approve one retry of a recent auto review denial |
  | `/memories` | Configure memory use and generation |
  | `/skills` | "Browse and use skills" |
  | `/import` | Import Claude Code setup and configuration |
  | `/feedback` | "Send logs to the Codex maintainers" |
  | `/init` | Generate an AGENTS.md scaffold |
  | `/logout` | Sign out of Codex |
  | `/mcp` | "List configured Model Context Protocol (MCP) tools" |
  | `/mention` | Attach a file to the chat |
  | `/model` | Choose the active model |
  | `/fast` | Toggle Fast service tier |
  | `/plan` | "Switch to plan mode and optionally send a prompt" |
  | `/goal` | "Set, edit, pause, resume, view, or clear a task goal" |
  | `/personality` | "Choose a communication style for responses" |
  | `/ps` | Check background terminals |

- **사용 권고 (원문 요지):**
  - 워크스페이스 안에서만 작업하는 로컬 작업엔 `--sandbox workspace-write` 사용
  - 디렉터리 접근이 필요하면 `--sandbox danger-full-access`보다 **`--add-dir` 선호**
  - CI 워크플로에선 `--json`과 `--output-last-message`를 함께 사용
- **⭐ 결정적 발견 — `/import`:** "Import Claude Code setup and configuration" — **Codex CLI에 Claude Code 설정을 가져오는 전용 슬래시 명령이 내장되어 있다.** 이 책의 "Claude Code 사용자를 위한 Codex 안내" 관점에서 가장 직접적인 근거 자료.
- Claude Code 대응 관점 메모:
  | Codex | Claude Code |
  |---|---|
  | `codex exec` | `claude -p` (headless) |
  | `codex resume` | `claude --resume` / `--continue` |
  | `codex doctor` | `claude doctor` |
  | `codex update` | `claude update` |
  | `codex mcp` | `claude mcp` |
  | `codex mcp-server` | `claude mcp serve` |
  | `codex plugin` / `codex plugin marketplace` | `claude plugin` / `/plugin marketplace` |
  | `codex login` / `codex logout` | `/login` / `/logout` |
  | `--add-dir` | `--add-dir` (동일) |
  | `--yolo` | `--dangerously-skip-permissions` |
  | `--model, -m` | `--model` |
  | `/compact`, `/clear`, `/init`, `/diff`, `/model`, `/vim`, `/mcp`, `/permissions` | 동일 이름 존재 |
  | `codex fork` / `/fork` | Claude Code에 대응물 없음 |
  | `codex sandbox` | Claude Code에 독립 샌드박스 실행 명령 없음 |
  | `codex execpolicy` | 대응물 없음 (permissions는 있으나 CLI 검증 도구 없음) |
  | `codex debug models` / `debug prompt-input` | 대응물 없음 (모델 카탈로그·프롬프트 덤프) |
  | `/import` | **Codex → Claude Code 방향의 대응물 없음** |

---

### Developer settings
- URL: https://learn.chatgpt.com/codex/developer-settings
- 검색: 2026-08-02 기준
- 핵심 내용: ChatGPT·Codex 클라이언트의 개발 설정.
- 설정 영역:
  - **프로젝트·터미널 동작:** 파일 열기 위치, 명령 출력 표시량, 터미널 탭 기본 위치
  - **코드 리뷰:** Git 설정에서 리뷰 배달 방식을 **inline** 또는 **detached** 선택
  - **IDE 확장 동기화:** 데스크톱 앱과 IDE 확장이 활성 채팅·에디터 컨텍스트 공유
  - **Agent 구성:** `config.toml`로 고급 옵션 편집
  - **Git 설정:** 브랜치 명명 표준화, force push 설정, 커밋 메시지·PR 설명 프롬프트 구성
  - **통합·MCP:** MCP를 통한 외부 도구 연결
  - **브라우저 개발자 모드:** Chrome DevTools Protocol 활성화
- **IDE 확장 설정 표 (원문 그대로, 10개 전수):**

  | Setting | Default | Description |
  |---|---|---|
  | `chatgpt.commentCodeLensEnabled` | `true` | "Show CodeLens above `TODO` comments so Codex can address them." |
  | `chatgpt.openOnStartup` | `false` | "Focus the Codex sidebar when the extension finishes starting." |
  | `chatgpt.followUpQueueMode` | `queue` | Choose message queuing behavior (`queue` or `steer`); legacy `interrupt` treated as `steer` |
  | `chatgpt.composerEnterBehavior` | `enter` | "Choose whether Enter always sends (`enter`), Cmd/Ctrl+Enter sends multiline prompts (`cmdIfMultiline`), or the modifier is always required (`cmdAlways`)." |
  | `chatgpt.reviewDelivery` | `inline` | "Run `/review` in the current chat when possible (`inline`) or start a separate review chat (`detached`)." |
  | `chatgpt.localeOverride` | Auto | "Set the preferred language for the Codex UI. Leave empty to detect it automatically." |
  | `chatgpt.runCodexInWindowsSubsystemForLinux` | `false` | "Windows only: Run Codex in WSL when WSL is available." |
  | `chatgpt.cliExecutable` | Unset | Development only path setting for Codex CLI executable |
  | `chat.fontSize` | Editor default | "Control chat text in the Codex sidebar, including chat content and the composer." |
  | `chat.editor.fontSize` | Editor default | "Control code-rendered content in Codex chats, including code snippets and diffs." |

- 언급된 `config.toml` 키: `model`, `model_reasoning_effort`, `personality`, `[tui]` 하위의 `vim_mode_default`·`raw_output_mode`
- **브라우저 개발자 모드 (원문 인용):** "Under **Developer mode**, turn on **Enable full CDP access** to let ChatGPT use the Chrome DevTools Protocol for performance profiling and deeper browser debugging."
- Claude Code 대응 관점 메모: `chatgpt.*` VS Code 설정 ↔ Claude Code VS Code 확장의 `claude-code.*` 설정. `chatgpt.followUpQueueMode`(queue/steer)는 Claude Code의 "메시지 큐잉 vs 현재 실행 조정"과 같은 문제를 다루는데, Codex는 이를 **명시적 설정 키**로 노출한다(데스크톱 앱의 "Follow-up behavior" 설정과 짝). `Enable full CDP access` ↔ Claude Code의 chrome-devtools MCP.

---

## 접근 실패 URL

**없음.** 지정된 34개 URL 전부에 접근해 내용을 확보했다 (성공 34 / 실패 0).

다만 다음 항목은 **부분 수집**이므로 인용 시 원문 재확인을 권한다:

| URL | 한계 |
|---|---|
| `/codex/config-file/config-reference` | 표 전체 축자 복제는 확보하지 못했다. **설정 키 이름 약 250개는 전수 확보**했고 섹션별 대표 기본값은 2차 확보. 개별 키의 설명 문구가 필요하면 원문 직접 확인 필요 |
| `/codex/agent-configuration/speed` | 문서에 표 형식의 모델별 비교나 Codex-Spark 배수 수치가 없음이 2회 확인됨. 확보된 수치가 문서에 명시된 전부 |
| `/codex/artifacts-viewer` | 접근은 성공했으나 페이지 제목이 **"Work with files"** 로, 요청서의 "artifacts-viewer"라는 명칭과 다름 (2회 확인, 리다이렉트 아님) |
| `/codex/extend/mcp` | resources·prompts·sampling을 별도 설정 요소로 다루지 않아 해당 항목은 문서에 없음 |

---

## 추가 발견 URL

문서 목록에 없었으나 본문에서 참조된 URL·경로 (목록만, 미방문):

**learn.chatgpt.com 내부**
- `/codex/plugins` — Use plugins (플러그인 탐색·설치·활성화·제거)
- `/codex/cloud/internet-access` — 클라우드 환경 네트워크 경계 정책
- Managed configuration / admin-enforced requirements (`requirements.toml`) 관련 페이지 — config-basic·hooks에서 참조
- Codex pricing 페이지 — image-generation에서 참조
- Skills & Plugins 페이지 — slash-commands에서 참조
- Image generation API guide / Image generation gallery — image-generation에서 참조

**developers.openai.com (플러그인 빌더 문서)**
- https://developers.openai.com/plugins/
- https://developers.openai.com/plugins/concepts/plugins
- https://developers.openai.com/plugins/build/skills
- https://developers.openai.com/plugins/build/mcp-server
- https://developers.openai.com/plugins/build/chatgpt-ui
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/connect-chatgpt
- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/mcp — OpenAI Docs MCP 서버 엔드포인트

**외부**
- https://github.com/openai/codex/issues — 이슈 트래커
- https://github.com/openai/codex/issues/new — 새 버그 리포트
- https://chatgpt.com/codex/install.sh — CLI 설치 스크립트
