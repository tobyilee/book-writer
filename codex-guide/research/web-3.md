# 그룹 C: 개발자 도구·환경·SDK·통합 (21 URL) — 검색 2026-08-02 기준

<!-- 검색 시점: 2026-08-02 기준 -->
<!-- 수집자: web-researcher (그룹 C) / genre: tech-book / slug: codex-guide -->
<!-- 출처: OpenAI Codex 공식 문서 https://learn.chatgpt.com — 전부 신뢰성 "최상"(공식 1차 소스) -->
<!-- 보강: 2026-08-02 리서치 리드 지시 — `.md` 원문 수집법 적용. 21개 중 17개를 원문 markdown으로 재수집해 검증·보강 완료. 상세는 "§0 원문 재수집 보강" 참조 -->

## §0 원문 재수집 보강 (2026-08-02, 2차)

리서치 리드가 알려준 기법을 적용했다: **경로 끝에 `.md`를 붙이면 렌더링 전 원문 markdown이 손실 없이 나온다.**

```bash
curl -sSL https://learn.chatgpt.com/codex/codex-sdk.md
```

**결과: 21개 중 17개가 `.md`로 원문 회수 성공(HTTP 200).** 나머지 4개(`use-cases`, `use-cases/collections`, `resources`, `videos`)는 `.md`가 **404**를 반환한다 — 정적 문서가 아니라 **동적 목록(SPA) 페이지**이기 때문이다. 이 4개는 1차 WebFetch 수집 결과가 유일한 근거이며 그대로 유효하다(항목·URL·날짜는 렌더링된 목록에서 그대로 추출됨).

**문서 색인:** `https://learn.chatgpt.com/llms.txt`는 404다(SPA 셸 반환). 실제 작동하는 색인은 **`https://developers.openai.com/llms.txt`** (107KB)이며, Codex 전용 전문은 `https://developers.openai.com/codex/llms-full.txt`. `learn.chatgpt.com/codex/*`와 `developers.openai.com/codex/*`는 **같은 문서의 두 호스트**다(원문 내부 링크는 `/docs/...` 형태로 쓰여 있다). 색인에서 발견한 미방문 경로는 "추가 발견 URL"에 대폭 보강했다.

### 이 보강으로 바뀐 것

1. **`[구조화 추출]` → `[원문]` 승격**: 17개 페이지의 코드 블록·표·서술 문장이 모두 원문 대조되었다. 아래 각 페이지의 라벨을 갱신했고, 1차 수집에서 압축됐던 내용은 **§8 원문 복원 보강**에 페이지별로 추가했다.
2. **오류 1건 정정**: 1차 수집에서 `/codex/code-review`의 섹션 구조로 기록한 목록(`Before you start / Set up Codex code review / ...`)은 실제로는 **`/codex/third-party/github`의 구조**였다. WebFetch가 두 페이지를 혼동했다. 아래 code-review 항목을 정정했다.
3. **중대한 신규 발견**: app-server 문서에 **Claude Code → Codex 마이그레이션 경로가 프로토콜 수준으로 박혀 있다**(`externalAgentConfig/detect`·`import`, `"source": "claude-code"`). 1차 수집에서 메서드 이름만 잡히고 내용이 통째로 누락됐다. §8-2에 전문 수록.
4. **누락 섹션 2개 복원**: app-server의 **"Apps (connectors)"**와 **"Auth endpoints"**(10개 하위 절, 레이트리밋·토큰 사용량 포함) 전체가 1차 수집에서 빠져 있었다.

### 추출 충실도 라벨 (갱신)

- `[원문✓]` — **`.md` 원문으로 검증됨.** 코드 블록·표·인용문을 그대로 책에 실어도 안전.
- `[목록 추출]` — `.md`가 없는 동적 목록 페이지. 항목명·URL·날짜는 신뢰 가능, 개수는 단정 금지.

모든 페이지는 **공식 1차 소스**이므로 신뢰성 등급은 일괄 **최상**이다.
- 문서에 **발행일 표기가 없다.** 따라서 이 문서의 모든 사실은 **"2026-08-02 방문 기준"**으로만 고정된다. Codex는 빠르게 변하는 제품이므로, 챕터에 버전·모델명·수치를 쓸 때는 반드시 "2026년 8월 기준"을 병기하라.
- 이 문서에 없는 내용은 추측으로 채우지 않았다.

### 문서 전반에서 반복 확인된 모델명 (2026-08 기준)

여러 페이지에 걸쳐 일관되게 등장하는 모델 ID — Phase 4 fact-checker의 대조 원장:

| 모델 ID | 등장 페이지 |
|---|---|
| `gpt-5.6-terra` | codex-sdk, mcp-server, app-server |
| `gpt-5.6-sol` | app-server (`model/list` 응답 예시, `isDefault: true`), amazon-bedrock |
| `gpt-5.6-luna` | amazon-bedrock |
| `gpt-5.5` | amazon-bedrock |
| `gpt-5.4` | amazon-bedrock |
| `gpt-5` | mcp-server (Agents SDK 예제의 오케스트레이터 모델) |

Bedrock 경유 시에는 `openai.` 접두어가 붙는다 (`openai.gpt-5.6-terra` 등).

---

## 1. Developers (허브)

### Developers
- URL: https://learn.chatgpt.com/codex/developers
- 검색: 2026-08-02 기준
- 추출 충실도: `[원문]` (허브 페이지 — 카드 제목·설명·경로 전수)
- 핵심 내용: 개발자용 Codex 기능의 목차 페이지. 6개 그룹으로 나뉜다.
- 인용 가능한 구절 (인트로):
  > "Codex supports everyday code work and deeper integrations across local and cloud environments. Its developer workflows span code review, the integrated terminal, reusable skills and plugins, automation with the SDK and App Server, team tools, and reference material for each surface."
- 하위 카드 전수 (섹션 헤딩 그대로):

  **Development workflows**
  - Code review — "Review changes and work with development tools in ChatGPT." → `/codex/code-review`
  - Integrated terminal — "Work with development tools directly." → `/codex/integrated-terminal`

  **Extend and automate**
  - Build skills — "Package development workflows and run deterministic automation." → `/codex/build-skills`
  - Build plugins → `/codex/build-plugins`
  - Hooks → `/codex/hooks`

  **Environments**
  - Environments — "Choose where development work runs and how it is isolated." → `/codex/environments/modes`
  - Local environments → `/codex/environments/local-environment`
  - Cloud environment → `/codex/environments/cloud-environment`
  - Git worktrees → `/codex/environments/git-worktrees`

  **Build with Codex**
  - Codex SDK — "Add Codex to products and systems." → `/codex/codex-sdk`
  - App Server → `/codex/app-server`
  - MCP Server → `/codex/mcp-server`
  - GitHub Action → `/codex/github-action`
  - Non-interactive mode → `/codex/non-interactive-mode`

  **Third-party integrations**
  - GitHub — "Delegate and track work from GitHub." → `/codex/third-party/github`
  - Slack → `/codex/third-party/slack`
  - Linear → `/codex/third-party/linear`

  **Reference**
  - CLI customization → `/codex/cli-customization`
  - Developer commands → `/codex/developer-commands`
  - Developer settings → `/codex/developer-settings`
- 제약·주의사항: 이 허브의 6개 그룹 구조 자체가 **책 목차 설계의 1차 참조**가 된다. Codex 공식이 개발자 기능을 어떻게 분류하는지 보여준다.
- Claude Code 대응 관점 메모: 그룹 구성이 Claude Code 문서와 거의 1:1이다 — skills/plugins/hooks, 로컬·클라우드·worktree 환경, SDK/MCP/GitHub Action/비대화형 모드, 서드파티 통합. **두 제품이 같은 문제 공간을 같은 축으로 분해했다**는 사실 자체가 책의 좋은 프레임이다.

---

## 2. 개발 워크플로

### Code review
- URL: https://learn.chatgpt.com/codex/code-review
- 검색: 2026-08-02 기준
- 추출 충실도: `[원문✓]` (3차 `.md` 검증 완료 — §8-1에 원문 복원 보강)
- 핵심 내용: ChatGPT 데스크톱 앱·웹·IDE 확장에서 코드 변경을 리뷰하는 기능. `/review` 명령으로 시작하며, 리뷰 결과는 리뷰 페인에 인라인 코멘트로 표시된다. GitHub PR 리뷰도 같은 페인에서 처리한다.
- **⚠️ 1차 수집 오류 정정**: 여기 적었던 섹션 목록(`Before you start / Set up Codex code review / ...`)은 **이 페이지가 아니라 `/codex/third-party/github`의 구조**였다. WebFetch가 두 페이지를 혼동했다.
- **실제 섹션 헤딩(원문 검증)**: Start a review / Choose a review scope / Work with review results / Navigating the review pane / Inline comments for feedback / Pull request reviews / Staging and reverting files
- **중요한 구조적 사실**: 이 페이지는 `<ContentModeSwitch group="codex-surface" id="...">`로 **web / app / cli / ide 4개 표면별로 본문이 갈린다.** 같은 `/review`라도 표면마다 스코프 선택지와 설정 키가 다르다 — 책에서 "어느 표면 이야기인지"를 반드시 명시해야 한다.
- 명령·트리거·설정 키:
  - `/review` — 리뷰 시작 명령 (ChatGPT Work 또는 Codex 안에서)
  - `@codex review` — PR 코멘트로 리뷰 요청
  - `@codex review for security regressions` — 범위를 좁힌 리뷰 요청
  - `@codex fix the P1 issue` — 리뷰 후 수정 요청
  - 설정 토글: **Code review**, **Automatic reviews**
  - 분리형 리뷰 챗(detached review chat) 모드 — Settings에서 구성
  - `AGENTS.md` — 리포지토리별 리뷰 규칙 파일
  - `gh` (GitHub CLI) 인증 — PR 리뷰 전제 조건
- 리뷰 범위(scope) 선택지: base 브랜치 대비 리뷰 / 커밋되지 않은 변경 리뷰 / 특정 커밋 리뷰 / 커스텀 리뷰 지시. 리뷰 페인은 Git 상태(unstaged, staged, commit, branch, last turn changes)를 보여준다.
- 리뷰 페인 조작:
  - 파일명 클릭 → 에디터에서 열기
  - 파일 배경 클릭 → diff 펼치기/접기
  - Cmd+클릭(단일 라인) → 해당 라인을 에디터에서 열기
  - 인라인 코멘트로 라인 단위 피드백 남기기
- Git 액션 3단계 입도: **전체 diff / 파일 단위 / hunk 단위**로 stage·revert 가능.
- `AGENTS.md` 리뷰 규칙 예시 (문서에 제시된 형태):
```markdown
## Code Review Rules

### Experiment cohorts

- Do not filter treatment comparisons on post-exposure behavior, including conversion or retention.
  Safe path: build cohorts from assignment or exposure; report conversion as an outcome.
```
- 리뷰 규칙 작성 지침 (원문 표현):
  - "Focus on consequential, repository-specific behavior"
  - "State the safe path or exception"
  - "Keep rules scoped and durable" — 구현 세부가 아니라 **결과(outcome)**를 참조하게 쓰라는 뜻
  - "Leave mechanical checks in CI" — 기계적 검사는 CI/린터에 남겨라
- 수치·라벨: **P0 / P1** 우선순위 라벨로 고우선 이슈에 집중. `@codex fix the P1 issue` 형태로 후속 수정 지시 가능.
- 제약·주의사항: Codex cloud 설정 필요, 코드 리뷰 설정 접근 권한 필요, 트리거 문구가 정확해야 함. 자동 리뷰는 권한 매칭 필요. **코드 리뷰는 필수 승인(required approvals)을 대체하지 않으며, 테스트나 브랜치 보호를 대체하지도 않는다.**
- Claude Code 대응 관점 메모: `AGENTS.md`의 "Code Review Rules" 섹션 ↔ Claude Code의 `CLAUDE.md`. 두 제품 모두 **리포지토리 루트의 마크다운 파일이 에이전트 행동의 정전(canonical) 규약**이라는 동일한 설계를 택했다. 다만 Codex 문서는 "기계적 검사는 CI에 남기고, 규칙은 결과 중심·내구적으로 쓰라"는 규칙 작성 지침을 명시적으로 제공한다 — 이 부분이 책의 실무 팁으로 유용하다.

### Integrated terminal
- URL: https://learn.chatgpt.com/codex/integrated-terminal
- 검색: 2026-08-02 기준
- 추출 충실도: `[구조화 추출]` (2회 방문 병합)
- 핵심 내용: ChatGPT 데스크톱 앱 내장 터미널. **현재 프로젝트 또는 worktree에 스코프**되며 챗마다 별도로 존재한다. 우상단 터미널 아이콘 또는 단축키로 연다. ChatGPT가 터미널 출력을 읽을 수 있어, 실행 중인 개발 서버 상태 확인이나 실패한 빌드 참조가 대화 안에서 가능하다.
- 섹션: Run and validate your project / Create reusable actions / (단축키)
- 명령·단축키:

| 항목 | 값 | 설명 |
|---|---|---|
| 터미널 열기 | **Ctrl+`** (백틱) | 통합 터미널 열기 |
| 명령 팔레트 | **Cmd+K** | 앱 명령 팔레트를 연다 — **터미널을 지우지 않는다** |
| 터미널 지우기 | **Ctrl+L** | 터미널 clear |

- 문서에 예시로 등장하는 상용 명령: `git status`, `git pull --rebase`, `pnpm test` 또는 `npm test`, `pnpm run lint`
- 재사용 액션: 자주 쓰는 명령을 **로컬 환경(local environment)의 액션**으로 정의하면 데스크톱 앱에 단축 버튼으로 뜨고, 통합 터미널에서 실행된다. (→ local-environment 페이지와 연결)
- 제약·주의사항: ChatGPT 데스크톱 앱 전용 기능. Cmd+K가 터미널 clear가 **아니라는** 점이 명시적으로 언급된 것은 일반 터미널 관습과 다르기 때문 — 실무 함정.
- Claude Code 대응 관점 메모: Claude Code는 사용자의 기존 터미널 안에서 살지만, Codex 데스크톱 앱은 **터미널을 앱 안에 품는다**. 방향이 정반대다. "에이전트를 터미널에 넣을 것인가, 터미널을 에이전트에 넣을 것인가" — 책의 대비 축으로 쓸 만하다. (문서 근거: 이 페이지 + code-review 페이지의 통합 리뷰 페인)

---

## 3. 실행 환경 (Environments)

### Codex environments (모드 선택)
- URL: https://learn.chatgpt.com/codex/environments/modes
- 검색: 2026-08-02 기준
- 추출 충실도: `[원문]` (짧은 페이지 — 사실상 전문 회수)
- 핵심 내용: Codex 챗을 시작할 때 어디서 실행할지, 파일을 어떻게 격리할지 고르는 3지선다.
- 세 모드 (원문 문구):
  - **Local** — "work directly in your current project directory."
  - **Worktree** — "isolate changes in a Git worktree. Learn more."
  - **Cloud** — "run remotely in a configured cloud environment."
- 핵심 사실: **Local과 Worktree 챗은 둘 다 사용자 컴퓨터에서 실행된다.** Cloud만 원격 실행이다.
- 접근 경로: 데스크톱 앱에서 ChatGPT 드롭다운 → **Codex** 선택 → 새 챗 시작 시 환경 선택.
- 표: **비교표는 이 페이지에 없다.** (2026-08-02 기준 — 각 모드의 상세는 개별 페이지로 분기)
- 관련 링크: `/codex/environments/local-environment`, `/codex/environments/cloud-environment`, `/codex/environments/git-worktrees`, `/codex/prompting` (Concepts 섹션)
- Claude Code 대응 관점 메모: Claude Code의 실행 축(로컬 / worktree isolation / 원격 클라우드 에이전트)과 정확히 같은 3분할. **격리 수준을 챗 시작 시점의 1급 선택지로 노출**한다는 점이 Codex 데스크톱 앱의 특징이다.

### Local environments
- URL: https://learn.chatgpt.com/codex/environments/local-environment
- 검색: 2026-08-02 기준
- 추출 충실도: `[구조화 추출]` (2회 방문 병합)
- 핵심 내용: 프로젝트의 worktree 셋업 스크립트와 상용 액션을 정의하는 설정. **ChatGPT 데스크톱 앱 전용.** 설정은 데스크톱 앱의 설정 페인에서 하지만, 결과물은 프로젝트 루트의 `.codex` 폴더에 저장되어 **Git에 커밋해 팀과 공유할 수 있다.**
- 섹션 헤딩(순서): Local environments / Setup scripts / Actions / Use built-in Git tools
- 파일 경로·설정 키:
  - `.codex` — 프로젝트 루트의 설정 폴더. Git 리포지토리에 체크인 가능.
- **Setup scripts**: Codex가 새 worktree를 만들 때 자동 실행된다. 존재 이유(원문):
  > "your project might not be fully set up and might be missing dependencies or files that aren't checked into your repository."

  TypeScript 프로젝트 예시:
```
npm install
npm run build
```
  macOS / Windows / Linux 별로 기본값을 오버라이드하는 플랫폼별 스크립트를 따로 정의할 수 있다.
- **Actions**: 자주 쓰는 작업(개발 서버 시작, 테스트 실행 등)을 데스크톱 앱 상단 바에 단축으로 노출. **통합 터미널 안에서 실행된다.**

  Node.js "Run" 액션 예시:
```
npm start
```
  액션도 macOS/Windows/Linux 플랫폼별 스크립트 구성 가능.
- **내장 Git 도구** (앱을 떠나지 않고 가능한 작업 전수):
  - 현재 체크아웃의 변경사항을 diff 페인에서 보기
  - 변경사항에 인라인 코멘트 달기
  - 청크(chunk) 단위 stage 또는 revert
  - 파일 단위 stage 또는 revert
  - 커밋
  - 브랜치 푸시
  - 풀 리퀘스트 생성
- 제약·주의사항 (원문 취지):
  - "Local environments are available only in Codex in the ChatGPT desktop app"
  - worktree는 로컬 챗과 **다른 디렉터리**에서 실행되므로 셋업이 불완전할 수 있다 — 그래서 셋업 스크립트가 필요하다.
  - 여러 프로젝트가 한 리포에 있으면, **공유 `.codex` 폴더를 담고 있는 프로젝트 디렉터리를 열어야 한다.**
- Claude Code 대응 관점 메모: `.codex` 폴더를 리포에 커밋해 팀이 공유한다는 구조는 Claude Code의 `.claude/` 디렉터리(settings·skills·agents를 리포에 체크인)와 같은 발상이다. **"에이전트 설정을 코드처럼 버전 관리한다"**는 공통 원칙.

### Cloud environments
- URL: https://learn.chatgpt.com/codex/environments/cloud-environment
- 검색: 2026-08-02 기준
- 추출 충실도: `[구조화 추출]` (2회 방문 병합)
- 핵심 내용: Codex 클라우드 챗의 컨테이너 의존성·도구를 커스터마이즈하는 방법.
- 섹션 헤딩(순서): Cloud environments / How Codex cloud chats run / Default universal image / Environment variables and secrets / Automatic setup / Manual setup / Container caching / Internet access and network proxy
- **클라우드 챗 실행 절차 (순서대로)**:
  1. Codex가 컨테이너를 만들고, 지정된 브랜치/커밋 SHA에서 리포를 체크아웃한다.
  2. 셋업 스크립트를 실행한다. 캐시된 컨테이너를 재개하는 경우 선택적 **maintenance script**도 실행한다.
  3. 인터넷 접근 설정을 적용한다 (셋업 스크립트는 인터넷 접근 O, 에이전트 단계는 **기본 OFF**).
  4. 에이전트가 터미널 명령을 루프로 실행한다 — 코드 편집, 검사 실행, 작업 검증.
  5. `AGENTS.md`가 있으면 프로젝트별 린트·테스트 명령을 그것에서 읽는다.
  6. 답변과 파일 변경 diff를 보여준다. 사용자는 PR을 열거나 후속 질문을 할 수 있다.
- **Default universal image**: 흔한 언어·패키지가 사전 설치되어 있고, Python·Node.js 및 런타임의 **버전 핀(version pinning)** 가능. 레퍼런스는 GitHub의 `openai/codex-universal` 리포지토리.
- **환경 변수와 시크릿** (구분이 중요):

| 구분 | 유효 범위 | 암호화 |
|---|---|---|
| Environment variables | 챗 전체 기간 (셋업 + 에이전트 단계 모두) | 일반 |
| Secrets | **셋업 스크립트에서만** 사용 가능, 에이전트 단계 전에 제거됨 | 추가 암호화 적용 |

- **Automatic setup**: npm, yarn, pnpm, pip, pipenv, poetry 지원.
- **Manual setup**: 복잡한 셋업은 커스텀 Bash 스크립트. 문서의 예시:
```bash
# Install type checker
pip install pyright

# Install dependencies
poetry install --with test
pnpm install
```
- **Container caching** (수치 주의):
  - 캐시 지속: **최대 12시간** ("up to 12 hours") — 2026-08 기준
  - 스크립트나 변수가 바뀌면 캐시 자동 무효화
  - 캐시된 컨테이너 재개 시 maintenance script 실행
  - **Business / Enterprise**: "caches are shared across all users who have access" — 캐시가 워크스페이스 전체에 공유되므로, 무효화도 전체 사용자에게 영향
- **인터넷 접근과 네트워크 프록시**:
  - 셋업 단계: 인터넷 접근 있음
  - 에이전트 단계: **기본 OFF**, 설정으로 제한적/무제한 허용 가능
  - 모든 아웃바운드 트래픽은 **HTTP/HTTPS 프록시**를 거쳐야 한다 (보안·오남용 방지 목적)
- 관련 링크: `/codex/cloud/internet-access` (Agent internet access 상세)
- Claude Code 대응 관점 메모: "셋업 단계엔 인터넷, 에이전트 단계엔 기본 차단"이라는 **단계별 권한 분리(phase-scoped privilege)**는 Codex 클라우드 설계의 핵심이다. 시크릿을 에이전트 단계 전에 제거하는 것도 같은 원리 — **에이전트가 실행되는 순간의 권한 표면을 최소화**한다. Claude Code의 sandbox/permission 모델과 대조할 때 이 "단계"라는 축이 Codex 쪽의 고유한 발명이다.

### Worktrees (Git worktrees)
- URL: https://learn.chatgpt.com/codex/environments/git-worktrees
- 검색: 2026-08-02 기준
- 추출 충실도: `[구조화 추출]` (2회 방문 병합, FAQ는 원문 회수)
- 핵심 내용: 한 프로젝트에서 여러 챗을 동시에, 서로 방해 없이 돌리기 위한 Git worktree 활용. 리포지토리의 2차 체크아웃을 만들어 파일은 각자 갖되 Git 메타데이터(`.git`)는 공유한다.
- 섹션 헤딩(순서): Worktrees / What's a worktree / Terminology / Why use a worktree / Getting started / Working between Local and Worktree / Option 1: Working on the worktree / Option 2: Handing a chat off to Local / Advanced details / Codex-managed and permanent worktrees / How Codex manages worktrees for you / Copy ignored local files into managed worktrees / Branch limitations / Why this limitation exists / Worktree cleanup / Frequently asked questions
- **용어 정의 (원문)**:
  - **Local checkout**: "The repository that you created. Sometimes just referred to as **Local** in the ChatGPT desktop app."
  - **Worktree**: "A Git worktree that was created from your local checkout in the ChatGPT desktop app."
  - **Handoff**: "The flow that moves a chat between Local and Worktree. Codex handles the Git operations required to move your work safely between them."
- **왜 쓰는가 (3가지)**:
  1. Local 셋업을 건드리지 않고 병렬 작업
  2. 집중을 유지한 채 백그라운드 작업을 큐에 넣기
  3. 검사·테스트가 필요하면 챗을 Local로 옮기기
- **시작하기 (4단계, 원문)**:
  1. "Select 'Worktree' In the new chat view, select **Worktree** under the composer. Optionally, choose a local environment to run setup scripts for the worktree."
  2. "Select the starting branch Below the composer, choose the Git branch to base the worktree on. This can be your `main` / `master` branch, a feature branch, or your current branch with unstaged local changes."
  3. "Submit your prompt Submit your prompt, and Codex creates a Git worktree based on the branch you selected. By default, Codex works in a 'detached HEAD'."
  4. "Choose where to keep working When you're ready, you can either keep working directly on the worktree or hand the chat off to your local checkout."
- **두 갈래 작업 방식**:
  - **Option 1**: worktree에서만 작업하고 영구 브랜치를 만든다.
  - **Option 2**: 헤더의 **Hand off** 버튼으로 챗을 Local로 넘긴다.
- **경로·파일명·설정 키 (전수)**:

| 항목 | 값 | 의미 |
|---|---|---|
| worktree 기본 위치 | `$CODEX_HOME/worktrees` | Codex 관리 worktree가 생성되는 디렉터리 |
| 위치 변경 | **Settings > Worktrees > Worktree root** | 기본 위치 오버라이드 |
| 무시 파일 복사 목록 | `.worktreeinclude` | gitignore된 파일 중 worktree에 필요한 것을 나열 |
| 자동 복사 파일 | `AGENTS.override.md` | 로컬 관리 worktree에 자동 복사됨 |
| 공유 메타데이터 | `.git` | worktree 간 공유 |
| 브랜치 참조 형식 | `refs/heads/<name>` | |
| 예시 ignored 파일 | `.env`, `.env.local`, `config/secrets.json` | `.worktreeinclude`에 넣을 만한 것들 |

- **수치·한도**: **"Codex keeps your most recent 15 Codex-managed worktrees."** — 기본적으로 최근 15개 관리형 worktree만 보존 (2026-08 기준).
- **브랜치 제약 (실무 함정)**:
  - "Git only allows a branch to be checked out in one place at a time."
  - worktree에서 브랜치를 체크아웃하면 로컬 체크아웃에서는 **체크아웃할 수 없다.**
  - worktree에서 브랜치를 만들면 다른 worktree에서 체크아웃할 수 없다.
  - 실제 에러 메시지: `fatal: 'feature/a' is already used by worktree at '<WORKTREE_PATH>'`
- **`.worktreeinclude` 사용 규칙**:
  - Git이 의도적으로 무시하는 파일 중 worktree에 필요한 것을 나열한다.
  - "Don't list tracked files" — 추적되는 파일은 넣지 마라.
  - "Codex skips source symlinks and won't overwrite files that already exist in the new checkout."
  - "This behavior applies to local ChatGPT desktop app managed worktrees, not remote worktrees or Git worktrees you create yourself from the command line."
- **FAQ (질문 + 원문 답변)**:
  - Q: Can I control where worktrees are created?
    > "Yes. Codex creates managed worktrees under `$CODEX_HOME/worktrees` by default. To choose another location, open **Settings > Worktrees** and change **Worktree root**."
  - Q: Can I move a chat between Local and Worktree?
    > "Yes. Use **Hand off** in the chat header to move a chat between your local checkout and a worktree. Codex handles the Git operations needed to move the chat safely between environments. If you hand a chat back to a worktree later, Codex returns it to the same associated worktree."
  - Q: What happens to chats if a worktree is deleted?
    > "Chats can remain in your history even if the underlying worktree directory is deleted. For Codex-managed worktrees, Codex saves a snapshot before deleting the worktree and offers to restore it if you reopen the associated chat. Permanent worktrees are not automatically deleted when you archive their chats."
- 제약·주의사항: worktree는 **ChatGPT 데스크톱 앱 전용**이며, **Git 리포지토리에 속한 프로젝트에서만** 동작한다.
- Claude Code 대응 관점 메모: Claude Code의 `isolation: "worktree"` 서브에이전트 옵션과 정확히 같은 문제(병렬 에이전트가 같은 작업 트리를 밟는 문제)를 푼다. 다만 Codex는 여기에 **(a) 관리형 worktree의 자동 GC(15개 보존), (b) `.worktreeinclude`로 gitignore된 파일을 명시적으로 승계, (c) Local↔Worktree 양방향 handoff와 삭제 전 스냅샷** 세 겹의 운영 장치를 더 얹었다. `.worktreeinclude`는 "worktree를 만들면 `.env`가 없어서 빌드가 깨진다"는 아주 흔한 실패를 정면으로 겨냥한 설계다 — 책의 실무 챕터에서 강조할 지점.

---

## 4. Build with Codex (SDK·서버·자동화)

### Codex SDK
- URL: https://learn.chatgpt.com/codex/codex-sdk
- 검색: 2026-08-02 기준
- 추출 충실도: `[구조화 추출]` (2회 방문 병합, 코드 블록은 원문)
- 핵심 내용: TypeScript·Python 라이브러리로 **로컬 Codex 에이전트를 프로그래밍 방식으로 제어**한다.
- 섹션 헤딩(순서): Codex SDK / TypeScript library / Installation / Usage / Python library / Installation / Usage / Sandbox presets
- **언제 쓰는가 (문서가 든 4가지)**:
  - CI/CD 파이프라인에 Codex 통합
  - 복잡한 엔지니어링 작업에 Codex를 부리는 에이전트 구축
  - 사내 도구·워크플로에 Codex 임베드
  - 커스텀 애플리케이션에 Codex 편입
  - 원문: "Use for coding-focused Codex threads"
- **설치 명령 (원문 그대로)**:
```bash
npm install @openai/codex-sdk
```
```bash
pip install openai-codex
```
  프리릴리스 빌드: `pip install --pre openai-codex`
- **버전 요구사항 (2026-08 기준)**:
  - TypeScript: **Node.js 18 이상**
  - Python: **Python 3.10 이상**
- **TypeScript — 스레드 시작 및 실행**:
```typescript
import { Codex } from "@openai/codex-sdk";

const codex = new Codex();
const thread = codex.startThread();
const result = await thread.run(
  "Make a plan to diagnose and fix the CI failures"
);

console.log(result.finalResponse);
```
- **TypeScript — 스레드 이어가기 및 재개**:
```typescript
const result = await thread.run("Implement the plan");
console.log(result.finalResponse);

const threadId = "<thread-id>";
const thread2 = codex.resumeThread(threadId);
const result2 = await thread2.run("Pick up where you left off");
console.log(result2.finalResponse);
```
- **Python — 기본 사용 (컨텍스트 매니저)**:
```python
from openai_codex import Codex, Sandbox

with Codex() as codex:
    thread = codex.thread_start(
        model="gpt-5.6-terra",
        sandbox=Sandbox.workspace_write,
    )
    result = thread.run("Make a plan to diagnose and fix the CI failures")
    print(result.final_response)
```
- **Python — 비동기**:
```python
import asyncio

from openai_codex import AsyncCodex


async def main() -> None:
    async with AsyncCodex() as codex:
        thread = await codex.thread_start(model="gpt-5.6-terra")
        result = await thread.run("Implement the plan")
        print(result.final_response)


asyncio.run(main())
```
- **Python — 샌드박스 프리셋 (턴별 강등 패턴)**:
```python
from openai_codex import Codex, Sandbox

with Codex() as codex:
    thread = codex.thread_start(sandbox=Sandbox.workspace_write)
    thread.run("Make the requested change.")
    review = thread.run("Review the diff only.", sandbox=Sandbox.read_only)
```
- **API 시그니처 (문서에 나타난 범위)**:

| 언어 | 심볼 | 설명 |
|---|---|---|
| TS | `new Codex()` | 클라이언트 생성자 |
| TS | `codex.startThread()` | 새 스레드 |
| TS | `codex.resumeThread(threadId: string)` | 스레드 재개 |
| TS | `await thread.run(prompt: string)` | 턴 실행 |
| TS | `result.finalResponse` | 최종 응답 프로퍼티 |
| Py | `Codex()` | 컨텍스트 매니저 |
| Py | `codex.thread_start(model=..., sandbox=...)` | 새 스레드 |
| Py | `thread.run(prompt, sandbox=...)` | 턴 실행 |
| Py | `result.final_response` | 최종 응답 프로퍼티 |
| Py | `AsyncCodex()` | 비동기 컨텍스트 매니저 |
| Py | `CodexConfig(codex_bin=...)` | 특정 Codex 실행파일 지정 |

- **Sandbox 프리셋 (열거값 전수)**: `Sandbox.read_only`, `Sandbox.workspace_write`, `Sandbox.full_access`
- **주의사항 (원문)**:
  - 배포된 SDK 빌드에는 **핀 고정된 Codex CLI 런타임 의존성**이 포함된다.
  - "Pass `CodexConfig(codex_bin=...)` only when you intentionally want to run against a specific local Codex executable"
  - `run()`의 `sandbox` 인자는 **해당 턴과 이후 턴에 적용**된다.
  - "When you omit `sandbox=`, app-server uses its configured default" — 생략하면 app-server의 기본값을 따른다.
- Claude Code 대응 관점 메모: **Codex SDK ↔ Claude Agent SDK**의 정면 대응. 개념 매핑이 거의 1:1이다 — `startThread()/resumeThread()` ↔ 세션/재개, `sandbox` 프리셋 3단계 ↔ Claude Code의 permission mode. 특히 `Sandbox.workspace_write`로 쓰고 `Sandbox.read_only`로 리뷰하는 **턴 단위 권한 강등 패턴**은 문서가 명시적으로 예시로 든 것이라, 책에서 "권한은 세션 속성이 아니라 턴 속성"이라는 논지의 근거로 쓸 수 있다. SDK가 내부적으로 app-server 위에 얹혀 있다는 점("app-server uses its configured default")도 중요한 아키텍처 사실이다.

### Codex App Server
- URL: https://learn.chatgpt.com/codex/app-server
- 검색: 2026-08-02 기준
- 추출 충실도: `[구조화 추출]` (2회 방문, 2차에서 메서드·이벤트·JSON 스키마 대량 회수)
- 핵심 내용: Codex를 제품에 임베드하기 위한 **JSON-RPC 기반 프로토콜 서버**. SDK보다 한 층 아래의 표면이며, ChatGPT 데스크톱 앱·IDE 확장이 이 위에서 돈다. 구현은 Codex GitHub 리포지토리에 오픈소스로 공개되어 있다.
- 섹션 헤딩(순서, 62개 항목 — 원문 목차 전수):
  Codex App Server / Connect the CLI terminal UI / Protocol / Message schema / Getting started / Core primitives / Lifecycle overview / Initialization / Experimental API opt-in / API overview / Models / List models (`model/list`) / List experimental features (`experimentalFeature/list`) / Inspect an execution environment (experimental) / Threads / Start or resume a thread / Manage a thread goal / Read a stored thread (without resuming) / List thread turns / List threads (with pagination & filters) / Update stored thread metadata / Track thread status changes / List loaded threads / Unsubscribe from a loaded thread / Archive a thread / Delete a thread / Unarchive a thread / Trigger thread compaction / Run a thread shell command / Clean background terminals / Roll back recent turns / Turns / Sandbox read access (`ReadOnlyAccess`) / Start a turn / Inject items into a thread / Steer an active turn / Start a turn (invoke a skill) / Interrupt a turn / Review / Process execution / Command execution / Read admin requirements (`configRequirements/read`) / Windows sandbox setup (`windowsSandbox/setupStart`) / Filesystem / Events / Notification opt-out / Fuzzy file search events (experimental) / Warning events / Windows sandbox setup events / Turn events / Items / Item deltas / Errors / Approvals / Command execution approvals / File change approvals / `tool/requestUserInput` / Permission requests / MCP server elicitation requests / Dynamic tool calls (experimental) / MCP tool-call approvals (apps) / Skills

- **핵심 원시 개념 (원문 정의)**:
  - **Thread**: "A conversation between a user and the Codex agent. Threads contain turns."
  - **Turn**: "A single user request and the agent work that follows. Turns contain items and stream incremental updates."
  - **Item**: "A unit of input or output (user message, agent message, command runs, file change, tool call, and more)."

- **명령 (원문 그대로)**:
```bash
codex app-server --listen ws://127.0.0.1:4500
codex --remote ws://127.0.0.1:4500
export CODEX_REMOTE_TOKEN="$(cat "$HOME/.codex/app-server-token")"
codex --remote wss://remote-host:4500 --remote-auth-token-env CODEX_REMOTE_TOKEN
codex app-server generate-ts --out ./schemas
codex app-server generate-json-schema --out ./schemas
```

- **전송(transport) 옵션 전수**:

| 값 | 설명 |
|---|---|
| `stdio://` | **기본값.** 개행 구분 JSON (newline-delimited JSON) |
| `ws://IP:PORT` | WebSocket — **실험적·미지원(experimental and unsupported)** |
| `unix://` 또는 `unix://PATH` | Unix 소켓 (HTTP Upgrade 사용) |
| `off` | 로컬 전송 노출 안 함 |

- **WebSocket 인증 플래그**:
```bash
--ws-auth capability-token --ws-token-file /absolute/path
--ws-auth capability-token --ws-token-sha256 HEX
--ws-auth signed-bearer-token --ws-shared-secret-file /absolute/path
--ws-issuer <issuer> --ws-audience <audience> --ws-max-clock-skew-seconds <seconds>
```

- **메시지 스키마 (JSON-RPC 형태)**:
```json
{ "method": "thread/start", "id": 10, "params": { "model": "gpt-5.6-terra" } }
{ "id": 10, "result": { "thread": { "id": "thr_123" } } }
{ "id": 10, "error": { "code": 123, "message": "Something went wrong" } }
{ "method": "turn/started", "params": { "turn": { "id": "turn_456" } } }
```

- **Getting started — Node.js 클라이언트 전문**:
```typescript
import { spawn } from "node:child_process";
import readline from "node:readline";

const proc = spawn("codex", ["app-server"], {
  stdio: ["pipe", "pipe", "inherit"],
});
const rl = readline.createInterface({ input: proc.stdout });

const send = (message: unknown) => {
  proc.stdin.write(`${JSON.stringify(message)}\n`);
};

let threadId: string | null = null;

rl.on("line", (line) => {
  const msg = JSON.parse(line) as any;
  console.log("server:", msg);

  if (msg.id === 1 && msg.result?.thread?.id && !threadId) {
    threadId = msg.result.thread.id;
    send({
      method: "turn/start",
      id: 2,
      params: {
        threadId,
        input: [{ type: "text", text: "Summarize this repo." }],
      },
    });
  }
});

send({
  method: "initialize",
  id: 0,
  params: {
    clientInfo: {
      name: "my_product",
      title: "My Product",
      version: "0.1.0",
    },
  },
});
send({ method: "initialized", params: {} });
send({ method: "thread/start", id: 1, params: { model: "gpt-5.6-terra" } });
```

- **초기화 (필수 절차)**: 원문 —
  > "Clients must send a single `initialize` request per transport connection before invoking any other method on that connection, then acknowledge with an `initialized` notification."

```json
{
  "method": "initialize",
  "id": 0,
  "params": {
    "clientInfo": {
      "name": "codex_vscode",
      "title": "Codex VS Code Extension",
      "version": "0.1.0"
    }
  }
}
```

- **실험 API 옵트인 + 알림 옵트아웃**:
```json
{
  "method": "initialize",
  "id": 1,
  "params": {
    "clientInfo": { "name": "my_client", "title": "My Client", "version": "0.1.0" },
    "capabilities": {
      "experimentalApi": true,
      "optOutNotificationMethods": ["thread/started", "item/agentMessage/delta"]
    }
  }
}
```

- **API 메서드 전수 (문서 그룹 그대로)**:

  *Thread Management*: `thread/start`, `thread/resume`, `thread/fork`, `thread/read`, `thread/list`, `thread/turns/list`, `thread/items/list`, `thread/loaded/list`, `thread/name/set`, `thread/goal/set`, `thread/goal/get`, `thread/goal/clear`, `thread/metadata/update`, `thread/archive`, `thread/delete`, `thread/unsubscribe`, `thread/unarchive`, `thread/status/changed`, `thread/compact/start`, `thread/shellCommand`, `thread/backgroundTerminals/clean`, `thread/backgroundTerminals/list`, `thread/backgroundTerminals/terminate`, `thread/rollback`, `thread/inject_items`

  *Turn Management*: `turn/start`, `turn/steer`, `turn/interrupt`

  *Review*: `review/start`

  *Process & Command Execution*: `command/exec`, `command/exec/write`, `command/exec/resize`, `command/exec/terminate`, `process/spawn`, `process/writeStdin`, `process/resizePty`, `process/kill`

  *Models & Features*: `model/list`, `modelProvider/capabilities/read`, `experimentalFeature/list`, `experimentalFeature/enablement/set`

  *Environment & Configuration*: `environment/info`, `configRequirements/read`, `config/read`, `config/value/write`, `config/batchWrite`

  *Permissions & Profiles*: `permissionProfile/list`

  *Collaboration*: `collaborationMode/list`

  *Skills*: `skills/list`, `skills/extraRoots/set`, `skills/config/write`

  *Hooks*: `hooks/list`

  *Plugins & Marketplace*: `marketplace/add`, `marketplace/remove`, `marketplace/upgrade`, `plugin/list`, `plugin/read`, `plugin/install`, `plugin/uninstall`, `plugin/skill/read`

  *Apps*: `app/installed`, `app/list`, `app/read`

  *MCP Servers*: `config/mcpServer/reload`, `mcpServerStatus/list`, `mcpServer/resource/read`, `mcpServer/tool/call`, `mcpServer/oauth/login`

  *External Agents*: `externalAgentConfig/detect`, `externalAgentConfig/import`

  *Windows Sandbox*: `windowsSandbox/setupStart`

  *Feedback & Tools*: `feedback/upload`, `tool/requestUserInput`

  *Filesystem*: `fs/readFile`, `fs/writeFile`, `fs/createDirectory`, `fs/getMetadata`, `fs/readDirectory`, `fs/remove`, `fs/copy`, `fs/watch`, `fs/unwatch`

  *Session Initialization*: `initialize`, `initialized`

- **이벤트/알림 전수**:

  *Thread*: `thread/started`, `thread/archived`, `thread/unarchived`, `thread/closed`, `thread/status/changed`, `thread/name/updated`, `thread/goal/updated`, `thread/goal/cleared`, `thread/deleted`, `thread/tokenUsage/updated`

  *Turn*: `turn/started`, `turn/completed`, `turn/diff/updated`, `turn/plan/updated`

  *Item lifecycle*: `item/started`, `item/completed`

  *Item deltas*: `item/agentMessage/delta`, `item/plan/delta`, `item/reasoning/summaryTextDelta`, `item/reasoning/summaryPartAdded`, `item/reasoning/textDelta`, `item/commandExecution/outputDelta`, `item/fileChange/outputDelta` *(deprecated)*

  *Approval/Request*: `item/commandExecution/requestApproval`, `item/fileChange/requestApproval`, `item/permissions/requestApproval`, `item/tool/requestUserInput`, `item/tool/call`, `mcpServer/elicitation/request`

  *Process/Command*: `command/exec/outputDelta`, `process/outputDelta`, `process/exited`

  *MCP*: `mcpServer/startupStatus/updated`, `mcpServer/oauthLogin/completed`

  *Hook*: `hook/started`, `hook/completed`

  *Model*: `model/safetyBuffering/updated`, `model/rerouted`, `model/verification`

  *Filesystem*: `fs/changed`

  *Config & Feature*: `configWarning`, `warning`, `skills/changed`

  *Windows sandbox*: `windowsSandbox/setupCompleted`

  *Fuzzy search (experimental)*: `fuzzyFileSearch/sessionUpdated`, `fuzzyFileSearch/sessionCompleted`

  *Review mode*: `enteredReviewMode`, `exitedReviewMode`

  *General*: `serverRequest/resolved`

- **승인(approval) 결정값**:
  - 명령 실행 승인: `accept`, `acceptForSession`, `decline`, `cancel`, 그리고 execpolicy 수정 동반 승인:
```json
{ "acceptWithExecpolicyAmendment": { "execpolicy_amendment": ["cmd", "..."] } }
```
  - 파일 변경 승인: `accept`, `acceptForSession`, `decline`, `cancel`

- **Item 타입 전수 (예시 페이로드)**:
```json
{ "id": "item_1", "type": "userMessage", "content": [] }
{ "id": "item_2", "type": "agentMessage", "text": "...", "phase": "commentary" }
{ "id": "item_3", "type": "plan", "text": "..." }
{ "id": "item_4", "type": "reasoning", "summary": "...", "content": "..." }
{ "id": "item_5", "type": "commandExecution", "command": "npm test", "cwd": "/project", "status": "inProgress" }
{ "id": "item_6", "type": "fileChange", "changes": [{ "path": "file.txt", "kind": "create", "diff": "..." }], "status": "inProgress" }
{ "id": "item_7", "type": "mcpToolCall", "server": "myserver", "tool": "mytool", "status": "inProgress", "arguments": {}, "appContext": { "connectorId": "conn_123" } }
{ "id": "item_8", "type": "dynamicToolCall", "tool": "mytool", "arguments": {} }
{ "id": "item_9", "type": "collabToolCall", "tool": "mytool", "status": "inProgress" }
{ "id": "item_10", "type": "webSearch", "query": "...", "action": { "type": "search" } }
{ "id": "item_11", "type": "imageView", "path": "/tmp/image.png" }
{ "id": "item_12", "type": "enteredReviewMode", "review": "current changes" }
{ "id": "item_13", "type": "exitedReviewMode", "review": "Looks good" }
{ "id": "item_14", "type": "contextCompaction" }
```

- **턴 입력(input) 형식**:
```json
{ "type": "text", "text": "Explain this diff" }
{ "type": "image", "url": "https://.../design.png" }
{ "type": "localImage", "path": "/tmp/screenshot.png" }
```

- **샌드박스 정책 스키마**:
```json
{ "type": "readOnly", "access": { "type": "fullAccess" } }
```
```json
{
  "type": "workspaceWrite",
  "writableRoots": ["/Users/me/project"],
  "readOnlyAccess": {
    "type": "restricted",
    "includePlatformDefaults": true,
    "readableRoots": ["/Users/me/shared-read-only"]
  },
  "networkAccess": false
}
```

- **`turn/start` 전체 예시 (승인 정책·샌드박스·모델·effort·outputSchema 포함)**:
```json
{
  "method": "turn/start",
  "id": 30,
  "params": {
    "threadId": "thr_123",
    "input": [{ "type": "text", "text": "Run tests" }],
    "cwd": "/Users/me/project",
    "approvalPolicy": "unlessTrusted",
    "sandboxPolicy": {
      "type": "workspaceWrite",
      "writableRoots": ["/Users/me/project"],
      "networkAccess": true
    },
    "model": "gpt-5.6-terra",
    "effort": "medium",
    "summary": "concise",
    "personality": "friendly",
    "outputSchema": {
      "type": "object",
      "properties": { "answer": { "type": "string" } },
      "required": ["answer"],
      "additionalProperties": false
    }
  }
}
```

- **스킬 호출 턴 (`turn/start`에 skill 아이템 동봉)**:
```json
{
  "method": "turn/start",
  "id": 33,
  "params": {
    "threadId": "thr_123",
    "input": [
      { "type": "text", "text": "$skill-creator Add a new skill for triaging flaky CI and include step-by-step usage." },
      { "type": "skill", "name": "skill-creator", "path": "/Users/me/.codex/skills/skill-creator/SKILL.md" }
    ]
  }
}
```

- **`thread/goal/set` (장기 목표 원장)**:
```json
{
  "method": "thread/goal/set",
  "id": 13,
  "params": {
    "threadId": "thr_123",
    "objective": "Finish the migration and keep tests green",
    "status": "active",
    "tokenBudget": 40000
  }
}
```
  응답에는 `tokensUsed`, `timeUsedSeconds`가 포함된다.

- **`model/list` 응답 예시 (모델 메타데이터 구조)**:
```json
{
  "id": 6,
  "result": {
    "data": [
      {
        "id": "gpt-5.6-sol",
        "model": "gpt-5.6-sol",
        "displayName": "GPT-5.6-Sol",
        "hidden": false,
        "defaultReasoningEffort": "low",
        "supportedReasoningEfforts": [
          { "reasoningEffort": "low", "description": "Fast responses with lighter reasoning" }
        ],
        "inputModalities": ["text", "image"],
        "supportsPersonality": true,
        "isDefault": true
      }
    ],
    "nextCursor": null
  }
}
```

- **`configRequirements/read` (관리자 강제 정책 조회)**:
```json
{
  "id": 52,
  "result": {
    "requirements": {
      "allowedApprovalPolicies": ["onRequest", "unlessTrusted"],
      "allowedSandboxModes": ["readOnly", "workspaceWrite"],
      "featureRequirements": { "personality": true, "unified_exec": false },
      "network": {
        "enabled": true,
        "allowedDomains": ["api.openai.com"],
        "allowUnixSockets": ["/tmp/example.sock"],
        "dangerouslyAllowAllUnixSockets": false
      }
    }
  }
}
```

- **수치·제약·안정성 노트 (fact-check 원장)**:

| 항목 | 값/내용 |
|---|---|
| 목표(goal) objective 길이 | **비어 있지 않아야 하고 최대 4,000자** |
| 과부하 시 에러 | WebSocket 모드에서 요청 큐가 차면 JSON-RPC 에러 코드 **`-32001`**, 메시지 `"Server overloaded; retry later."` |
| 페이지네이션 미지원 | `historyMode: "paginated"`는 아직 미지원 — JSON-RPC 에러 **`-32601`** 반환 |
| 기본 `historyMode` | `"legacy"` |
| `inputModalities` 누락 시 | `["text", "image"]`로 간주 (하위 호환) |

- **주요 주의사항 (원문)**:
  - WebSocket 전송: "WebSocket transport is experimental and unsupported. Local listeners such as `ws://127.0.0.1:PORT` are appropriate for localhost and SSH port-forwarding workflows. Non-loopback WebSocket listeners currently allow unauthenticated connections by default during rollout, so configure WebSocket auth before exposing one remotely."
  - 실험 API 게이팅: "Some app-server methods and fields are intentionally gated behind `experimentalApi` capability. Omit `capabilities` (or set `experimentalApi` to `false`) to stay on the stable API surface, and the server rejects experimental methods/fields."
  - MCP 필수 서버: "If you mark an enabled MCP server as `required` in config and that server fails to initialize, `thread/start` and `thread/resume` fail instead of continuing without it."
  - 모델 전환 경고: "If you resume with a different model than the one recorded in the rollout, Codex emits a warning and applies a one-time model-switch instruction on the next turn."
  - 외부 샌드박스: "Use `sandboxPolicy.type = \"externalSandbox\"` if you already sandbox the server process and want Codex to skip its own sandbox enforcement."
  - 네트워크 승인 그룹화: "Codex groups concurrent network approval prompts by destination (`host`, protocol, and port)."
  - macOS 읽기 전용: "On macOS, `includePlatformDefaults: true` appends a curated platform-default Seatbelt policy for restricted-read sessions."
  - 플러그인 API 미성숙: `plugin/list`, `plugin/read`, `plugin/install`, `plugin/uninstall`에 대해 "Don't call this method from production clients yet"
- **Deprecated 목록**: `thread/rollback` (제거 예정), `item/fileChange/outputDelta` (레거시 호환용)
- **`experimentalApi: true`가 필요한 메서드·필드 전수**: `thread/turns/list`, `thread/items/list`, `thread/backgroundTerminals/clean`, `thread/backgroundTerminals/list`, `thread/backgroundTerminals/terminate`, `environment/info`, `process/*` 계열, `thread/list`의 필터 `parentThreadId`·`ancestorThreadId`, `thread/fork`의 `excludeTurns`, `item/permissions/requestApproval`의 `additionalPermissions`, `collaborationMode/list`, `experimentalFeature/list`, `experimentalFeature/enablement/set`, `thread/status/changed`
- Claude Code 대응 관점 메모: **여기가 그룹 C의 최대 수확이다.** App Server는 Claude Code에 정확히 대응하는 공개 표면이 흔치 않은 층 — Codex는 "제품에 임베드하기 위한 JSON-RPC 프로토콜"을 문서화된 1급 시민으로 노출했고, 실제로 VS Code 확장(`clientInfo.name: "codex_vscode"`)이 이 위에서 돈다. 책에서 다룰 만한 대비 축: (a) **Thread/Turn/Item 3층 모델**이 대화 상태를 어떻게 재현 가능하게 만드는가, (b) `approvalPolicy`·`sandboxPolicy`·`configRequirements/read`가 이루는 **3단 권한 체계**(사용자 선택 / 세션 정책 / 관리자 강제), (c) `experimentalApi` 옵트인으로 안정 API 표면을 명시 분리하는 버저닝 전략. 그리고 `externalAgentConfig/detect` / `externalAgentConfig/import` 메서드의 존재는 **다른 에이전트 도구의 설정을 감지·가져오는 경로**가 프로토콜에 박혀 있다는 뜻이다 — Claude Code 사용자의 마이그레이션 관점에서 반드시 확인해볼 지점. (단, 이 메서드들의 상세 동작은 이 페이지에 서술되어 있지 않으므로 추측 금지.)

### Running Codex as an MCP server
- URL: https://learn.chatgpt.com/codex/mcp-server
- 검색: 2026-08-02 기준
- 추출 충실도: `[원문]` — **이 페이지는 본문이 사실상 전문 회수되었다. 인용 안전.**
- 핵심 내용: Codex를 MCP 서버로 띄워 다른 MCP 클라이언트(예: OpenAI Agents SDK)에서 호출하는 방법 + Agents SDK로 다중 에이전트 워크플로를 짜는 가이드.
- 인용 가능한 구절:
  > "You can run Codex as an MCP server and connect it from other MCP clients (for example, an agent built with the OpenAI Agents SDK MCP integration)."
  > "Codex CLI can do far more than run ad-hoc tasks. By exposing the CLI as a Model Context Protocol (MCP) server and orchestrating it with the OpenAI Agents SDK, you can create deterministic, reviewable workflows that scale from a single agent to a complete software delivery pipeline."
- **명령**:
```bash
codex mcp-server
```
```bash
npx @modelcontextprotocol/inspector codex mcp-server
```
- **노출되는 도구는 정확히 2개**: `codex`(대화 시작), `codex-reply`(대화 이어가기). `tools/list` 요청으로 확인 가능.

- **`codex` 도구 파라미터 전수 (원문 표)**:

| Property | Type | Description |
|---|---|---|
| **`prompt`** (required) | `string` | The initial user prompt to start the Codex conversation. |
| `approval-policy` | `string` | Approval policy for shell commands generated by the model: `untrusted`, `on-request`, and `never`. |
| `base-instructions` | `string` | The set of instructions to use instead of the default ones. |
| `compact-prompt` | `string` | Prompt used when compacting the conversation. |
| `config` | `object` | Individual configuration settings that override what's in `$CODEX_HOME/config.toml`. |
| `cwd` | `string` | Working directory for the session. If relative, resolved against the server process's current directory. |
| `developer-instructions` | `string` | Developer instructions injected as a developer-role message. |
| `model` | `string` | Optional override for the model name (for example, `gpt-5.6-terra`). |
| `sandbox` | `string` | Sandbox mode: `read-only`, `workspace-write`, or `danger-full-access`. |

- **`codex-reply` 도구 파라미터 전수 (원문 표)**:

| Property | Type | Description |
|---|---|---|
| **`prompt`** (required) | string | The next user prompt to continue the Codex conversation. |
| **`threadId`** (required) | string | The ID of the thread to continue. |
| `conversationId` (deprecated) | string | Deprecated alias for `threadId` (kept for compatibility). |

  > "Use the `threadId` from `structuredContent.threadId` in the `tools/call` response. Approval prompts (exec/patch) also include `threadId` in their `params` payload."

- **응답 페이로드 예시 (원문)**:
```json
{
  "structuredContent": {
    "threadId": "019bbb20-bff6-7130-83aa-bf45ab33250e",
    "content": "`ls -lah` (or `ls -alh`) — long listing, includes dotfiles, human-readable sizes."
  },
  "content": [
    {
      "type": "text",
      "text": "`ls -lah` (or `ls -alh`) — long listing, includes dotfiles, human-readable sizes."
    }
  ]
}
```
  > "Note modern MCP clients generally report only `\"structuredContent\"` as the result of a tool call, if present, though the Codex MCP server also returns `\"content\"` for the benefit of older MCP clients."

- **전제 조건 (원문)**:
  - Codex CLI가 로컬에 설치되어 `codex` 명령이 사용 가능할 것
  - Python 3.10+ 와 `pip`
  - MCP Inspector 예제를 돌리려면 Node.js 18+
  - 로컬에 저장된 OpenAI API 키

- **환경 준비**:
```bash
mkdir codex-workflows
cd codex-workflows
printf "OPENAI_API_KEY=sk-..." > .env
```
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade openai openai-agents python-dotenv
```

- **MCP 서버 기동 (`codex_mcp.py`) — 최소 형태**:
```python
import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStdio


async def main() -> None:
    async with MCPServerStdio(
        name="Codex CLI",
        params={
            "command": "codex",
            "args": ["mcp-server"],
        },
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        print("Codex MCP server started.")
        # More logic coming in the next sections.
        return


if __name__ == "__main__":
    asyncio.run(main())
```
  실행: `python codex_mcp.py` → `Codex MCP server started.` 출력 후 종료.

- **단일 에이전트 워크플로 (Game Designer → Game Developer)** — 전문:
```python
import asyncio
import os

from dotenv import load_dotenv

from agents import Agent, Runner, set_default_openai_api
from agents.mcp import MCPServerStdio

load_dotenv(override=True)
set_default_openai_api(os.getenv("OPENAI_API_KEY"))


async def main() -> None:
    async with MCPServerStdio(
        name="Codex CLI",
        params={
            "command": "codex",
            "args": ["mcp-server"],
        },
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        developer_agent = Agent(
            name="Game Developer",
            instructions=(
                "You are an expert in building simple games using basic html + css + javascript with no dependencies. "
                "Save your work in a file called index.html in the current directory. "
                "Always call codex with \"approval-policy\": \"never\" and \"sandbox\": \"workspace-write\"."
            ),
            mcp_servers=[codex_mcp_server],
        )

        designer_agent = Agent(
            name="Game Designer",
            instructions=(
                "You are an indie game connoisseur. Come up with an idea for a single page html + css + javascript game that a developer could build in about 50 lines of code. "
                "Format your request as a 3 sentence design brief for a game developer and call the Game Developer coder with your idea."
            ),
            model="gpt-5",
            handoffs=[developer_agent],
        )

        await Runner.run(designer_agent, "Implement a fun new game!")


if __name__ == "__main__":
    asyncio.run(main())
```

- **다중 에이전트 워크플로 (`multi_agent_workflow.py`)**: Project Manager + Designer + Frontend Developer + Backend Developer + Tester 5역할. PM이 `REQUIREMENTS.md`·`TEST.md`·`AGENT_TASKS.md`를 만들고 파일 존재 여부로 핸드오프를 게이팅한다. 전문은 원문 참조(길다) — 핵심 발췌:
  - 모든 하위 에이전트 지시에 반복되는 문구:
    > "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."
  - PM의 게이팅 규칙 (원문):
    > "Do not advance to the next handoff until the required files for that step are present. If something is missing, request the owning agent to supply it and re-check."
    > "Do NOT respond with status updates. Just handoff to the next agent until the project is complete."
  - PM 모델 설정: `model="gpt-5"`, `model_settings=ModelSettings(reasoning=Reasoning(effort="medium"))`
  - 실행: `Runner.run(project_manager_agent, task_list, max_turns=30)`
  - import 목록: `from agents import (Agent, ModelSettings, Runner, WebSearchTool, set_default_openai_api)`, `from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX`, `from agents.mcp import MCPServerStdio`, `from openai.types.shared import Reasoning`
  - 예제 과제: "Bug Busters" — 20초 동안 움직이는 버그를 클릭해 점수를 얻는 단일 화면 게임, 선택적으로 백엔드에 점수 제출 + top-10 리더보드. 백엔드 엔드포인트: `GET /health`, `GET/POST /scores`. 제약: "No external database—memory storage is fine."
- **트레이싱**:
  > "Codex automatically records traces that capture every prompt, tool call, and hand-off."
  > "These traces make it straightforward to debug workflow hiccups, audit agent behavior, and measure performance over time without requiring extra instrumentation."
- 제약·주의사항: `client_session_timeout_seconds=360000`(=100시간)를 예제가 쓴다는 점에 주목 — 장기 실행 세션을 상정한 값이다. MCP 서버로서 Codex가 노출하는 파라미터는 **`config` 오브젝트를 통해 `$CODEX_HOME/config.toml`을 개별 오버라이드**할 수 있다.
- Claude Code 대응 관점 메모: **Codex MCP server ↔ Claude Code의 MCP 통합**이지만 방향이 반대다. Claude Code는 주로 MCP **클라이언트**로서 외부 도구를 붙이는 문서가 두꺼운데, 이 페이지는 Codex를 MCP **서버**로 노출해 남의 오케스트레이터(Agents SDK) 밑에 종속시키는 시나리오를 1급으로 다룬다. 즉 "Codex를 도구로 쓰는 에이전트"를 공식이 권장한다. 승인 정책 값 매핑도 대조 재료다 — MCP 도구 파라미터는 `untrusted`/`on-request`/`never`, 샌드박스는 `read-only`/`workspace-write`/`danger-full-access`인데, **App Server의 JSON-RPC에서는 camelCase(`unlessTrusted`, `onRequest`, `workspaceWrite`, `readOnly`)로 다르다.** 같은 개념의 표기가 표면마다 갈리는 것은 실무 함정이자 책에서 짚을 디테일이다.

### Codex GitHub Action
- URL: https://learn.chatgpt.com/codex/github-action
- 검색: 2026-08-02 기준
- 추출 충실도: `[구조화 추출]` (2회 방문 병합, YAML은 원문)
- 핵심 내용: `openai/codex-action@v1`. GitHub CI/CD 워크플로 안에서 Codex 작업을 자동화한다.
- 인용 가능한 구절 (동작 요약, 원문):
  > "installs the Codex CLI, starts the Responses API proxy when you provide an API key, and runs `codex exec` under the permissions you specify."
- 섹션 헤딩(순서): Codex GitHub Action / Prerequisites / Example workflow / Configure `codex exec` / Manage privileges / Capture outputs / Security checklist / Troubleshooting
- **용도**: PR 피드백 자동화(수동 CLI 관리 없이), CI 파이프라인에서 품질 게이트, 워크플로 파일에서 코드 리뷰·마이그레이션 같은 반복 작업 실행.
- **전제 조건**:
  - OpenAI API 키를 GitHub secret으로 저장
  - **Linux 또는 macOS 러너** — Windows는 `safety-strategy: unsafe`가 필요
  - 리포지토리 코드를 미리 체크아웃
  - `prompt` 파라미터 또는 커밋된 파일을 가리키는 `prompt-file`로 프롬프트 선택
- **전체 워크플로 예시 (원문 그대로)**:
```yaml
name: Codex pull request review
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  codex:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    outputs:
      final_message: ${{ steps.run_codex.outputs.final-message }}
    steps:
      - uses: actions/checkout@v5
        with:
          ref: refs/pull/${{ github.event.pull_request.number }}/merge
          fetch-depth: 0
          persist-credentials: false

      - name: Run Codex
        id: run_codex
        uses: openai/codex-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          prompt-file: .github/codex/prompts/review.md
          output-file: codex-output.md

  post_feedback:
    runs-on: ubuntu-latest
    needs: codex
    if: needs.codex.outputs.final_message != ''
    permissions:
      issues: write
      pull-requests: write
    steps:
      - name: Post Codex feedback
        uses: actions/github-script@v7
        with:
          github-token: ${{ github.token }}
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.pull_request.number,
              body: process.env.CODEX_FINAL_MESSAGE,
            });
        env:
          CODEX_FINAL_MESSAGE: ${{ needs.codex.outputs.final_message }}
```
- **액션 입력(inputs) 전수**:

| Input | 설명 | 비고 |
|---|---|---|
| `prompt` | 인라인 작업 지시 | `prompt` 또는 `prompt-file` 중 하나 선택 |
| `prompt-file` | 마크다운/텍스트 파일의 리포지토리 경로 | `prompt` 또는 `prompt-file` 중 하나 선택 |
| `codex-args` | 추가 CLI 플래그 | JSON 배열 또는 셸 문자열 형식 |
| `model` | Codex 에이전트 모델 설정 | 비우면 기본값 |
| `effort` | Codex 에이전트 reasoning effort | 비우면 기본값 |
| `sandbox` | 샌드박스 모드 | `workspace-write`, `read-only`, `danger-full-access` |
| `output-file` | 최종 메시지를 디스크에 저장 | 아티팩트·diff 용도 |
| `codex-version` | 고정할 CLI 릴리스 | 비우면 최신 |
| `codex-home` | 공유 Codex 홈 디렉터리 | 스텝 간 설정 재사용 |
| `safety-strategy` | 권한 통제 방식 | **기본값 `drop-sudo`** |
| `unprivileged-user` | 특정 사용자 계정으로 실행 | `codex-user`와 함께 사용 |
| `read-only` | 파일·네트워크 변경 제한 | **단독으로는 시크릿을 보호하지 못함** |
| `allow-users` | 워크플로 트리거 가능 사용자 제한 | 명시적 신뢰 계정 |
| `allow-bots` | 봇 트리거 제한 | 추가 신뢰 계정 목록 |
| `openai-api-key` | API 인증 | Responses API 프록시에 필요 |

- **액션 출력(outputs)**: `final-message` — Codex 실행의 마지막 메시지
- **`safety-strategy` 값 전수**:
  1. **`drop-sudo`** (기본값) — Codex 실행 전에 `sudo`를 제거한다. **잡(job)당 되돌릴 수 없다(irreversible per job).** 메모리 내 시크릿을 보호한다.
  2. **`unsafe`** — Windows 러너에 필요
  3. **`unprivileged-user`** — 지정한 계정으로 Codex 실행
- **시크릿·환경 변수**: `${{ secrets.OPENAI_API_KEY }}`, `CODEX_FINAL_MESSAGE`
- **버전 핀**: `openai/codex-action@v1`, `actions/checkout@v5`, `actions/github-script@v7` (2026-08 기준)
- **보안 체크리스트 (원문 인용)**:
  1. "Limit who can start the workflow. Prefer trusted events or explicit approvals instead of allowing everyone to run Codex against your repository."
  2. "Sanitize prompt inputs from pull requests, commit messages, or issue bodies"
  3. "Protect your `OPENAI_API_KEY` by keeping `safety-strategy` on `drop-sudo`"
  4. "Never leave the action in `unsafe` mode on multi-tenant runners"
  5. "Run Codex as the last step in a job so later steps don't inherit state changes"
  6. "Rotate keys immediately if you suspect proxy logs exposed secrets"
- 관련 리포: https://github.com/openai/codex-action, 보안 문서 https://github.com/openai/codex-action/blob/main/docs/security.md
- Claude Code 대응 관점 메모: **Codex GitHub Action ↔ Claude Code GitHub Action**. 설계 차이가 뚜렷하다 — Codex 액션은 API 키를 셸 스텝에 노출하지 않기 위해 **Responses API 프록시를 액션이 직접 띄우고**, `drop-sudo`를 기본 안전 전략으로 삼는다. 그리고 예시 워크플로가 **잡을 둘로 쪼개** Codex 잡에는 `contents: read`만 주고, 쓰기 권한이 필요한 코멘트 작성은 `OPENAI_API_KEY` 없는 별도 잡(`post_feedback`)으로 넘긴다. 이 **"권한과 크레덴셜을 잡 경계로 분리"** 패턴은 non-interactive-mode 페이지의 auto-fix 예제와도 일치한다 — Codex 문서 전반을 관통하는 보안 원칙이며, 책의 CI 챕터에서 핵심 교훈으로 삼을 만하다.

### Non-interactive mode (`codex exec`)
- URL: https://learn.chatgpt.com/codex/non-interactive-mode
- 검색: 2026-08-02 기준
- 추출 충실도: `[원문]` — **본문 전문 회수. 인용 안전.**
- 핵심 내용: 대화형 TUI 없이 스크립트·CI에서 Codex를 돌리는 모드. 진입점은 `codex exec`.
- 인용 가능한 구절:
  > "Non-interactive mode lets you run Codex from scripts (for example, continuous integration (CI) jobs) without opening the interactive TUI. You invoke it with `codex exec`."
- 섹션: When to use `codex exec` / Basic usage / Permissions and safety / Make output machine-readable / Create structured outputs with a schema / Authenticate in automation / Resume a non-interactive session / Git repository required / Common automation patterns / Advanced stdin piping
- **언제 쓰는가 (원문 4개 불릿)**:
  > "Run as part of a pipeline (CI, pre-merge checks, scheduled jobs)."
  > "Produce output you can pipe into other tools (for example, to generate release notes or summaries)."
  > "Fit naturally into CLI workflows that chain command output into Codex and pass Codex output to other tools."
  > "Run with explicit, pre-set sandbox and approval settings."
- **기본 사용법**:
```bash
codex exec "summarize the repository structure and list the top 5 risky areas"
```
  **스트림 규약 (중요)**:
  > "While `codex exec` runs, Codex streams progress to `stderr` and prints only the final agent message to `stdout`."
```bash
codex exec "generate release notes for the last 10 commits" | tee release-notes.md
```
```bash
codex exec --ephemeral "triage this repository and suggest next steps"
```
  stdin 동작:
  > "If stdin is piped and you also provide a prompt argument, Codex treats the prompt as the instruction and the piped content as additional context."
```bash
curl -s https://jsonplaceholder.typicode.com/comments \
  | codex exec "format the top 20 items into a markdown table" \
  > table.md
```
- **권한과 안전 (플래그 전수)**:

| 플래그 | 의미 |
|---|---|
| (기본값) | **read-only 샌드박스에서 실행** |
| `--sandbox workspace-write` | 편집 허용 |
| `--sandbox danger-full-access` | 광범위 접근 허용 |
| `--full-auto` | **deprecated 호환 플래그. 경고를 출력한다.** 새 스크립트에서는 `--sandbox workspace-write`를 명시적으로 쓸 것 |
| `--ephemeral` | 세션 rollout 파일을 디스크에 남기지 않음 |
| `--ignore-user-config` | `$CODEX_HOME/config.toml`을 로드하지 않음 |
| `--ignore-rules` | 사용자·프로젝트 execpolicy `.rules` 파일 건너뜀 |
| `--json` | stdout을 JSON Lines 스트림으로 |
| `-o <path>` / `--output-last-message <path>` | 최종 메시지를 파일로 (stdout에도 여전히 출력) |
| `--output-schema <path>` | JSON Schema를 만족하는 최종 응답 요청 |
| `--skip-git-repo-check` | Git 리포 검사 우회 |

  > "Use `danger-full-access` only in a controlled environment (for example, an isolated CI runner or container)."
  > "If you configure an enabled MCP server with `required = true` and it fails to initialize, `codex exec` exits with an error instead of continuing without that server."
- **기계 판독 가능 출력**:
```bash
codex exec --json "summarize the repo structure" | jq
```
  이벤트 타입: `thread.started`, `turn.started`, `turn.completed`, `turn.failed`, `item.*`, `error`
  아이템 타입: agent messages, reasoning, command executions, file changes, MCP tool calls, web searches, plan updates
  샘플 JSONL 스트림 (원문):
```json
{"type":"thread.started","thread_id":"0199a213-81c0-7800-8aa1-bbab2a035a53"}
{"type":"turn.started"}
{"type":"item.started","item":{"id":"item_1","type":"command_execution","command":"bash -lc ls","status":"in_progress"}}
{"type":"item.completed","item":{"id":"item_3","type":"agent_message","text":"Repo contains docs, sdk, and examples directories."}}
{"type":"turn.completed","usage":{"input_tokens":24763,"cached_input_tokens":24448,"output_tokens":122,"reasoning_output_tokens":0}}
```
  ※ **주의**: `--json` 이벤트는 점 표기(`thread.started`)이고, App Server JSON-RPC 이벤트는 슬래시 표기(`thread/started`)다. 서로 다른 표면이다.
- **구조화 출력 (스키마)**:
  `schema.json`:
```json
{
  "type": "object",
  "properties": {
    "project_name": { "type": "string" },
    "programming_languages": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["project_name", "programming_languages"],
  "additionalProperties": false
}
```
```bash
codex exec "Extract project metadata" \
  --output-schema ./schema.json \
  -o ./project-metadata.json
```
  최종 출력 예시:
```json
{
  "project_name": "Codex CLI",
  "programming_languages": ["Rust", "TypeScript", "Shell"]
}
```
  ※ 이 예시는 **Codex CLI 자체가 Rust·TypeScript·Shell로 작성되어 있음**을 시사하지만, 문서상 어디까지나 예시 출력이다 — 사실 주장으로 인용하지 말 것.
- **자동화 인증**:
  - 기본적으로 저장된 CLI 인증을 재사용한다.
  - GitHub Actions에서는 CLI를 직접 설치·인증하지 말고 **Codex GitHub Action을 쓸 것**을 권장.
  - **경고 (원문)**:
    > "Do not set `OPENAI_API_KEY` or `CODEX_API_KEY` as a job-level environment variable in workflows that check out or run repository-controlled code. Build scripts, tests, dependency lifecycle hooks, or a compromised action in the same job can read those environment variables."
  - 단일 호출에만 키를 붙이는 패턴:
```bash
CODEX_API_KEY=<api-key> codex exec --json "triage open bug reports"
```
  - **"`CODEX_API_KEY` is only supported in `codex exec`."**
  - ChatGPT 관리 인증을 CI에서 쓰는 고급 경로: `~/.codex/auth.json`
    > "Treat `~/.codex/auth.json` like a password: it contains access tokens. Don't commit it, paste it into tickets, or share it in chat."
    > "Do not use this workflow for public or open-source repositories."
    상세: `/codex/auth/ci-cd-auth`
- **세션 재개**:
```bash
codex exec "review the change for race conditions"
codex exec resume --last "fix the race conditions you found"
```
  특정 세션 지정: `codex exec resume <SESSION_ID>`
- **Git 리포지토리 필수**:
  > "Codex requires commands to run inside a Git repository to prevent destructive changes. Override this check with `codex exec --skip-git-repo-check` if you're sure the environment is safe."
- **자동화 패턴 — CI 실패 자동 수정 워크플로 (전문, 원문 YAML)**:
```yaml
name: Codex auto-fix on CI failure

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

jobs:
  generate_fix:
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest
    permissions:
      contents: read
    outputs:
      has_patch: ${{ steps.diff.outputs.has_patch }}
    steps:
      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.workflow_run.head_sha }}
          fetch-depth: 0
          persist-credentials: false

      - uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install dependencies
        run: |
          if [ -f package-lock.json ]; then npm ci; fi

      - name: Run Codex
        uses: openai/codex-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          prompt: |
            The CI workflow "${{ github.event.workflow_run.name }}" failed for commit
            ${{ github.event.workflow_run.head_sha }}.

            Run `npm test --silent` to reproduce the failure. Identify the minimal
            change needed to make the tests pass, implement only that change, and
            run `npm test --silent` again.

            Do not refactor unrelated files.

      - name: Create patch artifact
        id: diff
        run: |
          git add -N .
          git diff --binary HEAD > codex.patch
          if [ -s codex.patch ]; then
            echo "has_patch=true" >> "$GITHUB_OUTPUT"
          else
            echo "has_patch=false" >> "$GITHUB_OUTPUT"
          fi

      - name: Upload patch artifact
        if: steps.diff.outputs.has_patch == 'true'
        uses: actions/upload-artifact@v4
        with:
          name: codex-fix-patch
          path: codex.patch
          if-no-files-found: error

  open_pr:
    runs-on: ubuntu-latest
    needs: generate_fix
    if: needs.generate_fix.outputs.has_patch == 'true'
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v5
        with:
          ref: ${{ github.event.workflow_run.head_sha }}
          fetch-depth: 0

      - uses: actions/download-artifact@v4
        with:
          name: codex-fix-patch

      - name: Apply Codex patch
        run: git apply --index codex.patch

      - name: Open pull request
        env:
          GH_TOKEN: ${{ github.token }}
          FAILED_HEAD_BRANCH: ${{ github.event.workflow_run.head_branch }}
          FAILED_HEAD_SHA: ${{ github.event.workflow_run.head_sha }}
          RUN_ID: ${{ github.event.workflow_run.run_id }}
        run: |
          branch="codex/auto-fix-$RUN_ID"

          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git switch -c "$branch"
          git commit -m "Auto-fix failing CI via Codex"
          git push origin "$branch"

          {
            echo "Codex generated this patch after CI failed for \`$FAILED_HEAD_SHA\`."
            echo
            echo "Review the changes before merging."
          } > pr-body.md

          gh pr create \
            --base "$FAILED_HEAD_BRANCH" \
            --head "$branch" \
            --title "Auto-fix failing CI via Codex" \
            --body-file pr-body.md
```
  설계 의도 (원문):
  > "The Codex job below has only `contents: read`. After Codex runs, it only serializes the diff as an artifact. The `open_pr` job receives repository write permissions, but it does not receive `OPENAI_API_KEY`."
- **고급 stdin 파이핑 — 두 모드**:
  1. **prompt + stdin**: 지시는 직접 쓰고, 파이프된 출력은 컨텍스트로.
```bash
npm test 2>&1 \
  | codex exec "summarize the failing tests and propose the smallest likely fix" \
  | tee test-summary.md
```
```bash
tail -n 200 app.log \
  | codex exec "identify the likely root cause, cite the most important errors, and suggest the next three debugging steps" \
  > log-triage.md
```
```bash
curl -vv https://api.example.com/health 2>&1 \
  | codex exec "explain the TLS or HTTP failure and suggest the most likely fix" \
  > tls-debug.md
```
```bash
gh run view 123456 --log \
  | codex exec "write a concise Slack-ready update on the CI failure, including the likely cause and next step" \
  | pbcopy
```
```bash
gh run view 123456 --log \
  | codex exec "summarize the failure in 5 bullets for the pull request thread" \
  | gh pr comment 789 --body-file -
```
  2. **`codex exec -`**: stdin 전체가 프롬프트.
```bash
cat prompt.txt | codex exec -
```
```bash
printf "Summarize this error log in 3 bullets:\n\n%s\n" "$(tail -n 200 app.log)" \
  | codex exec -
```
```bash
generate_prompt.sh | codex exec - --json > result.jsonl
```
- 관련 링크: 플래그 상세는 `/codex/developer-commands?surface=cli#cli-codex-exec`
- Claude Code 대응 관점 메모: **`codex exec` ↔ `claude -p`**의 정면 대응이며, 이 페이지가 그룹 C에서 실무 인용 가치가 가장 높다. 대조 포인트: (a) **stderr=진행, stdout=최종 메시지**라는 스트림 분리 규약이 명문화되어 있다; (b) `--json` JSONL 이벤트 스트림 + `--output-schema` JSON Schema 강제 — 구조화 출력을 두 층(이벤트/최종 응답)으로 제공한다; (c) **Git 리포 밖에서는 기본적으로 거부**하고 `--skip-git-repo-check`로만 우회 — 파괴적 변경 방지 장치를 CLI 진입점에 박아뒀다; (d) `--full-auto`를 deprecate하고 명시적 `--sandbox` 플래그로 유도 — "편의 플래그가 권한을 숨기면 안 된다"는 방향성; (e) `CODEX_API_KEY`를 `codex exec`에서만 지원하고 잡 레벨 env var 사용을 명시적으로 금지 — 자동화의 키 노출 표면을 좁힌다. 다섯 가지 모두 책에서 "비대화형 에이전트를 안전하게 파이프라인에 넣는 법"의 교재로 쓸 수 있다.

---

## 5. 서드파티 통합

### Codex code review in GitHub
- URL: https://learn.chatgpt.com/codex/third-party/github
- 검색: 2026-08-02 기준
- 추출 충실도: `[구조화 추출]` (2회 방문 병합)
- 핵심 내용: GitHub PR에 대한 자동 코드 리뷰. `/codex/code-review` 페이지와 내용이 상당 부분 겹친다(같은 기능의 GitHub 표면).
- **전제 조건**: 리포지토리에 Codex cloud 설정, Codex 코드 리뷰 설정 접근 권한, (선택) 커스텀 가이드용 `AGENTS.md`.
- **트리거**:
  - PR에 `@codex review` 코멘트 → 리뷰 요청
  - **자동 리뷰(Automatic reviews)** 활성화 → 모든 새 PR을 자동 리뷰
  - `@codex fix the P1 issue` → 리뷰 후 수정 요청
  - 그 외 `@codex` 지시 → PR 컨텍스트를 가진 클라우드 챗 시작
- **리뷰 커스터마이즈**: `AGENTS.md`의 "Code Review Rules" 섹션. 문서 권장 —
  > 규칙은 "consequential, repository-specific behavior"에 집중하고, CI/린팅에 맡길 기계적 검사는 배제하라.

  효과적인 규칙의 3요소:
  - 코드베이스에 특유한 구체적 제약이나 위험 패턴을 서술한다
  - 안전한 대안이나 예외를 제시한다
  - 구현 세부가 아닌 **결과(outcome)**를 참조해 내구성을 갖게 한다
- **수정 반영**: Codex는 PR 컨텍스트로 클라우드 챗을 시작하고, 권한이 있으면 **브랜치에 수정을 직접 푸시**할 수 있다.
- **우선순위**: P0·P1 이슈를 강조해 리뷰를 고우선 관심사에 집중시킨다.
- 제약·주의사항: Codex cloud 필요. 코드 리뷰가 필수 승인·테스트·브랜치 보호를 대체하지 않는다.
- Claude Code 대응 관점 메모: `@codex review` PR 코멘트 트리거 ↔ Claude Code GitHub Action의 `@claude` 멘션 패턴. 차이는 Codex 쪽이 **`AGENTS.md`의 전용 섹션**을 리뷰 규칙의 공식 주입 경로로 문서화했다는 점, 그리고 **P0/P1 우선순위 라벨**을 리뷰 출력 규약으로 못 박았다는 점이다.

### Use Codex in Slack
- URL: https://learn.chatgpt.com/codex/third-party/slack
- 검색: 2026-08-02 기준
- 추출 충실도: `[원문]` — **본문 전문 회수. 인용 안전.**
- 핵심 내용: Slack 채널·스레드에서 `@Codex`를 멘션하면 클라우드 챗을 만들고 결과를 회신한다.
- 인용 가능한 구절:
  > "Use Codex in Slack to kick off coding work from Slack channels and threads. Mention `@Codex` with a prompt, and Codex creates a cloud chat and replies with the results."
- **설치 3단계 (원문)**:
  1. Codex 클라우드 챗 셋업. **Plus, Pro, Business, Enterprise, Edu 플랜 필요** + 연결된 GitHub 계정 + 최소 1개 환경.
  2. Codex 설정(https://chatgpt.com/codex/settings/connectors)에서 워크스페이스에 Slack 앱 설치. 워크스페이스 정책에 따라 관리자 승인이 필요할 수 있다.
  3. 채널에 `@Codex` 추가.
- **사용 흐름**:
  1. 채널이나 스레드에서 `@Codex` 멘션 + 프롬프트. "Codex can reference earlier messages in the thread, so you often don't need to restate context."
  2. (선택) 환경이나 리포지토리 지정 — 예: `@Codex fix the above in openai/codex`
  3. Codex가 👀 리액션을 달고 챗 링크로 답한다. 완료되면 결과와, 설정에 따라 스레드 내 답변을 게시한다.
- **환경·리포 선택 규칙 (원문)**:
  > "Codex reviews the environments you have access to and selects the one that best matches your request. If the request is ambiguous, it falls back to the environment you used most recently."
  > "The chat runs against the default branch of the first repository listed in that environment's repo map. Update the repo map in Codex if you need a different default or more repositories."
  > "If no suitable environment or repository is available, Codex will reply in Slack with instructions on how to fix the issue before retrying."
- **Enterprise 데이터 통제**: 기본적으로 Codex는 스레드에 답변을 올리며 여기에 실행 환경의 정보가 포함될 수 있다. Enterprise 관리자는 ChatGPT 워크스페이스 설정에서 **"Allow Codex Slack app to post answers on task completion"**을 해제할 수 있고, 그러면 Codex는 **챗 링크만** 회신한다.
- **데이터 처리**: "When you mention `@Codex`, Codex receives your message and thread history to understand your request and create a chat."
  > "Codex uses large language models that can make mistakes. Always review answers and diffs."
- **트러블슈팅 (원문 4항목)**:
  - Missing connections: Slack/GitHub 연결을 확인 못 하면 재연결 링크로 답한다.
  - Unexpected environment choice: 스레드에 원하는 환경을 답글로 쓴 뒤(예: `Please run this in openai/openai (applied)`) 다시 `@Codex` 멘션.
  - Long or complex threads: 최신 메시지에 핵심을 요약해 스레드 깊숙이 묻힌 맥락 누락을 막아라.
  - Workspace posting: 일부 Enterprise 워크스페이스는 최종 답변 게시를 제한한다 — 그 경우 챗 링크로 진행 상황을 본다.
- Claude Code 대응 관점 메모: Slack 멘션 → 클라우드 챗 생성 → 스레드 회신은 Claude의 Slack 통합과 같은 형태다. Codex 고유 디테일은 **"환경(environment)"이라는 1급 개념이 라우팅 단위**라는 점 — 프롬프트만으로 어느 환경/리포에서 돌지가 결정되고, 애매하면 "가장 최근 쓴 환경"으로 폴백한다. 이 암묵적 라우팅은 편리하지만 예측 불가능성을 낳으며, 문서가 트러블슈팅 항목("Unexpected environment choice")으로 이를 인정한다.

### Use Codex in Linear
- URL: https://learn.chatgpt.com/codex/third-party/linear
- 검색: 2026-08-02 기준
- 추출 충실도: `[원문]` — **본문 전문 회수. 인용 안전.**
- 핵심 내용: Linear 이슈에서 작업을 위임한다. 이슈를 Codex에 **assign**하거나 코멘트에서 `@Codex` 멘션하면 클라우드 챗이 생성되고 진행 상황·결과가 이슈에 회신된다.
- 인용 가능한 구절:
  > "Use Codex in Linear to delegate work from issues. Assign an issue to Codex or mention `@Codex` in a comment, and Codex creates a cloud chat and replies with progress and results."
- **플랜 요건**: 유료 플랜에서 사용 가능. Enterprise는 워크스페이스 관리자가 (a) 워크스페이스 설정에서 Codex 클라우드 챗을 켜고, (b) 커넥터 설정에서 Codex for Linear를 활성화해야 한다.
- **설치 3단계**:
  1. GitHub를 Codex에 연결하고 작업 대상 리포의 환경을 만들어 Codex 클라우드 챗을 셋업.
  2. Codex 설정에서 워크스페이스용 Codex for Linear 설치.
  3. Linear 이슈의 코멘트 스레드에서 `@Codex`를 멘션해 Linear 계정 연결.
- **두 가지 위임 방식**:
  - **이슈 assign**: 팀원에게 배정하듯 Codex에 배정. Codex가 작업을 시작하고 이슈에 업데이트를 올린다.
  - **`@Codex` 멘션**: 코멘트 스레드에서 위임하거나 질문. 답변 후 같은 스레드에 후속 댓글을 달면 같은 챗이 이어진다.
  - 리포 고정: `@Codex fix this in openai/codex`
- **진행 추적**: 이슈의 **Activity**에서 진행 업데이트 확인, 챗 링크로 상세 추적. 완료 시 요약 + 완료된 챗 링크를 올려 PR을 만들 수 있게 한다.
- **환경·리포 선택 규칙 (원문)**:
  > "Linear suggests a repository based on the issue context. Codex selects the environment that best matches that suggestion. If the request is ambiguous, it falls back to the environment you used most recently."
  > "The chat runs against the default branch of the first repository listed in that environment's repo map."
- **트리아지 규칙으로 자동 배정 (4단계)**:
  1. Linear에서 **Settings**로 이동
  2. **Your teams** 아래 팀 선택
  3. 워크플로 설정에서 **Triage**를 열고 켠다
  4. **Triage rules**에서 규칙을 만들고 **Delegate > Codex** 선택 (원하는 다른 속성도 설정)

  > "Linear assigns new issues that enter triage to Codex automatically. When you use triage rules, Codex runs chats using the account of the issue creator."

  ※ **중요한 실행 주체 규칙**: 트리아지 규칙을 쓰면 Codex는 **이슈 작성자의 계정**으로 챗을 실행한다.
- **로컬 작업용 Linear 연결 (MCP)**: 데스크톱 앱·CLI·IDE 확장에서 로컬로 Linear 이슈에 접근하려면 Linear MCP 서버를 설정한다. **IDE 확장이든 CLI든 설정은 동일**(같은 config를 공유).
  - CLI (권장):
```bash
codex mcp add linear --url https://mcp.linear.app/mcp
```
    → Linear 계정 로그인 프롬프트가 뜬다.
  - 수동 설정: `~/.codex/config.toml`을 열고 추가
```toml
[mcp_servers.linear]
url = "https://mcp.linear.app/mcp"
```
    그 후 `codex mcp login linear` 실행.
- **트러블슈팅 (원문)**:
  - Missing connections: Linear 연결을 확인 못 하면 이슈에 계정 연결 링크로 답한다.
  - Unexpected environment choice: 스레드에 원하는 환경을 답글로 (예: `@Codex please run this in openai/codex`)
  - Wrong part of the code: 이슈에 컨텍스트를 더하거나 `@Codex` 코멘트에 명시적 지시를 준다.
- Claude Code 대응 관점 메모: **`codex mcp add <name> --url <url>` / `codex mcp login <name>` / `~/.codex/config.toml`의 `[mcp_servers.*]` TOML 블록**은 Claude Code의 `claude mcp add` + `.mcp.json` 대응이다. 형식이 다르다(TOML vs JSON)는 점, 그리고 Codex가 OAuth 로그인을 `codex mcp login`이라는 별도 서브커맨드로 노출한다는 점이 대조 포인트. 또 "트리아지 규칙 사용 시 이슈 작성자 계정으로 실행"은 **에이전트 자동화의 감사 추적(누구 권한으로 돌았나) 문제**를 공식이 명시적으로 정의한 드문 사례다.

---

## 6. 원격 접속 및 대체 모델 백엔드

### Remote connections
- URL: https://learn.chatgpt.com/codex/remote-connections
- 검색: 2026-08-02 기준
- 추출 충실도: `[원문]` — **본문 전문 회수. 인용 안전.**
- 핵심 내용: 다른 기기·머신에서 돌고 있는 작업에 접속한다. ChatGPT 모바일 앱의 **Remote**로 연결된 Mac/Windows의 ChatGPT·Codex 챗을 조작하거나, 다른 데스크톱 기기에서 이어받거나, SSH 호스트의 프로젝트에 앱을 연결한다.
- 인용 가능한 구절:
  > "Remote access uses the connected host's projects, chats, files, credentials, permissions, plugins, Computer Use, browser setup, and local tools."
  > "A secure relay layer keeps trusted machines reachable across your authorized ChatGPT devices without exposing them directly to the public internet."
- 섹션: Remote connections / What you can do remotely / Before you set up Remote / Set up Remote / Choose what to connect / What comes from the connected host / Pick up work from another device / Connect to an SSH host / Hand off a chat between hosts / Authentication and network exposure / Troubleshooting / See also
- **원격으로 가능한 일 (원문 6개 불릿)**:
  - 호스트의 프로젝트에서 새 챗 시작, 기존 챗 이어가기
  - 후속 지시 전송, 질문 응답, 진행 중 작업 조종(steer)
  - 명령 및 기타 동작 승인
  - 출력·diff·테스트 결과·터미널 출력·스크린샷 검토
  - 작업 완료 또는 주의 필요 시 알림 수신
  - 연결된 호스트와 챗 간 전환
- **전제 조건**: 사용할 ChatGPT 계정·워크스페이스의 Codex 접근 권한 / 최신 ChatGPT 모바일 앱(iOS·Android) / 깨어 있고 온라인이며 같은 계정·워크스페이스로 로그인된 최신 데스크톱 앱(macOS·Windows) / 필요한 MFA·SSO·패스키 설정.
  - **"Mobile setup starts from the app; you can't set it up from the Codex CLI or IDE extension."**
  - 워크스페이스를 통해 Codex를 쓰면 관리자가 **Remote Control 접근을 먼저 활성화**해야 할 수 있다.
- **날짜 기준 (수치 — fact-check 대상)**:
  > "Existing connections used since June 8, 2026, remain paired. If you haven't used an existing connection since June 8, 2026, update both apps and pair the devices again."
- **셋업 4단계**:
  1. **Start Remote setup.** 호스트에서 앱을 열고 사이드바의 **Set up Remote** 선택.
  2. **Scan the QR code.** 폰으로 QR 스캔.
  3. **Finish setup in ChatGPT.** 같은 계정·워크스페이스 확인 후 MFA·SSO·패스키 절차 완료. 성공하면 호스트가 폰의 Remote에 나타난다.
  4. **Review host settings.** 호스트 앱의 **Settings > Connections**에서 연결 기기 관리. 컴퓨터 깨어 있게 유지, Computer Use 활성화, Chrome 확장 설치 여부도 여기서.
  - QR 코드는 **그 폰과 그 호스트를 페어링**한다. 조작하려는 모든 폰·데스크톱을 모든 호스트와 각각 페어링해야 한다.
- **무엇을 연결할 것인가 (3가지 선택지)**:
  - **내 노트북/데스크톱**: 이미 ChatGPT를 쓰는 기기. 잠들거나 네트워크가 끊기거나 앱을 닫으면 원격 접근이 멈춘다.
    - Mac 노트북: **뚜껑을 열고 전원 연결** 상태면 원격 접근 유지 가능. 뚜껑을 닫으려면 **외부 디스플레이도 연결**해야 한다. **Sleep을 선택하면 여전히 원격 접근이 멈춘다.**
    - Windows 호스트: Computer Use를 쓰는 작업에서는 **세션을 잠금 해제 상태로** 유지해야 한다. "Computer Use on Windows runs in the foreground, so remote control is best for starting or checking work while you dedicate the host desktop to the task."
  - **전용 상시 가동 컴퓨터**: 장시간 작업용. 프로젝트·크레덴셜·MCP 서버·스킬·도구를 그 머신에 설치한다.
  - **원격 개발 환경(SSH 호스트)**: 프로젝트가 이미 원격에 있을 때. 데스크톱 앱 호스트를 그 환경에 먼저 연결하고, 폰은 여전히 같은 호스트에 붙는다.
- **연결된 호스트가 제공하는 것 (원문)**:
  - 리포지토리 파일·로컬 문서는 연결된 호스트에서 온다
  - 셸 명령은 그 호스트 또는 원격 환경에서 실행된다
  - MCP 서버·스킬·브라우저 접근·Computer Use는 그 호스트 설정에서 온다
  - 로그인된 웹사이트·데스크톱 앱은 호스트가 접근 가능할 때만 쓸 수 있다
  - **"The sandboxing settings, security controls, and action approvals still apply to the connected session."**
- **SSH 호스트 연결 (4단계, 원문 코드 포함)**:
  1. SSH config에 호스트를 추가해 Codex가 자동 발견하게 한다:
```
Host devbox
  HostName devbox.example.com
  User you
  IdentityFile ~/.ssh/id_ed25519
```
     > "Codex reads concrete host aliases from `~/.ssh/config`, resolves them with OpenSSH, and ignores pattern-only hosts."
  2. 앱이 도는 머신에서 SSH가 되는지 확인:
```bash
ssh devbox
```
  3. 원격 호스트에 Codex를 설치·인증한다. "The app starts the remote Codex app server through SSH, using the remote user's login shell. Make sure the `codex` command is available on the remote host's `PATH` in that shell."
  4. 앱에서 **Settings > Connections**를 열어 SSH 호스트를 추가·활성화하고 원격 프로젝트 폴더를 고른다.
  - 보안 기대치: "trusted keys, least-privilege accounts, and no unauthenticated public listeners."
- **호스트 간 챗 핸드오프**:
  - 핸드오프는 기존 챗과 **Git 상태**를 로컬 컴퓨터와 원격 호스트 사이에서 옮긴다.
  - 사전 조건: 목적지 호스트를 연결하고, **같은 Git 리포지토리의 프로젝트를 그 호스트에도 저장**해둬야 한다. 리포의 하위 디렉터리라면 양쪽에 같은 하위 디렉터리를 저장한다. "Codex only shows destinations with a matching saved project."
  - 절차: 챗을 연다 → 챗 푸터에서 현재 실행 위치 선택 → 목적지 호스트 선택(로컬로 되돌릴 땐 **This computer**) → 목적지와 브랜치 확인 후 **Hand off**.
  - "Codex creates or reuses a worktree on the destination host, transfers the chat and Git state, and switches the chat to that host. If the chat is running, handoff interrupts the current response before transferring it."
  - **제약**: "Codex can't hand off the chat making the request, and handoff to a Codex cloud environment isn't supported."
- **인증·네트워크 노출**:
  > "Remote connections use SSH to start and manage the remote Codex app server. Don't expose app-server transports directly on a shared or public network."
  > "If you need to reach a remote machine outside your current network, use a VPN or mesh networking tool instead of exposing the app server directly to the internet."
- **트러블슈팅 (5항목, 요지)**: 폰에 호스트가 안 보임 / 재로그인 후 Remote Control이 꺼짐(로그아웃은 Remote Control을 끄지만 페어링은 지우지 않는다 — 다시 켜면 복구) / 승인 요청이 안 뜸 / 원격 세션 끊김 / 인증이 셋업을 막음.
- Claude Code 대응 관점 메모: 이 페이지는 **App Server 페이지의 `codex --remote ws://...`와 짝을 이룬다** — Remote는 결국 "SSH로 원격 Codex app server를 띄우고 붙는 것"이다(문서가 명시). Claude Code에는 이에 정확히 대응하는 모바일 원격 조종 표면이 없다. 책의 관점: OpenAI는 **에이전트를 "어디서 도는 프로세스"로 보고, 조종석(phone/desktop)과 실행 호스트를 분리**했다. 그리고 "sandboxing·security controls·approvals는 원격 세션에도 그대로 적용된다"고 못 박아, 원격이 권한 우회 경로가 되지 않게 했다. **June 8, 2026** 페어링 기준일은 fact-checker가 확인할 구체 수치.

### Use ChatGPT Work and Codex with Amazon Bedrock
- URL: https://learn.chatgpt.com/codex/amazon-bedrock
- 검색: 2026-08-02 기준
- 추출 충실도: `[구조화 추출]` (2회 방문 병합)
- 핵심 내용: 로컬 ChatGPT Work·Codex가 OpenAI 호스팅 인프라 대신 **Amazon Bedrock을 통해 OpenAI 모델을 쓰도록** 설정한다.
- 인용 가능한 구절:
  > "The local client sends model requests to Amazon Bedrock, and Bedrock provides an OpenAI-compatible Responses API implementation."
- 섹션 헤딩(순서): Use ChatGPT Work and Codex with Amazon Bedrock / How it works / Before you start / Configure the provider / Authentication options / Option 1: Bedrock API key / Option 2: AWS SDK credentials / Shared AWS configuration files / Environment variables / AWS Management Console credentials / AWS SSO or a named profile / Federated identity / Desktop app and IDE extension / Verify setup / Supported models / Feature availability / Troubleshooting / Support boundaries
- **전제 조건**: Bedrock에서 지원 OpenAI 모델 접근 권한 / 선택 모델이 제공되는 AWS 리전 / **Amazon Bedrock Mantle 경로**에 대한 인증 구성.
- **설정 (`~/.codex/config.toml`)**:
```toml
model_provider = "amazon-bedrock"
```
- **인증 옵션 1 — Bedrock API 키**:
```bash
export AWS_BEARER_TOKEN_BEDROCK=<your-bedrock-api-key>
export AWS_REGION=us-east-2
```
- **인증 옵션 2 — AWS SDK 크레덴셜**: 표준 AWS 크레덴셜 소스 사용 — 공유 config 파일, 환경 변수, AWS Management Console, SSO, 페더레이티드 아이덴티티.
```bash
export AWS_ACCESS_KEY_ID=<your-access-key-id>
export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
export AWS_SESSION_TOKEN=<your-session-token>
```
- **데스크톱 앱·IDE 확장 (중요 함정)**: 이들은 셸 환경 변수를 상속하지 않을 수 있으므로 **`~/.codex/.env`에 값을 넣어야 한다.**
```bash
# ~/.codex/.env
export AWS_BEARER_TOKEN_BEDROCK=<your-bedrock-api-key>
export AWS_REGION=us-east-2
```
- **환경 변수 전수**:

| 변수 | 예시 값 |
|---|---|
| `AWS_BEARER_TOKEN_BEDROCK` | `<your-bedrock-api-key>` |
| `AWS_REGION` | `us-east-2` |
| `AWS_ACCESS_KEY_ID` | `<your-access-key-id>` |
| `AWS_SECRET_ACCESS_KEY` | `<your-secret-access-key>` |
| `AWS_SESSION_TOKEN` | `<your-session-token>` |
| `AWS_PROFILE` | `codex-bedrock` |

- **지원 모델 ID (원문 그대로, 2026-08 기준)**:
  - `openai.gpt-5.6-sol`
  - `openai.gpt-5.6-terra`
  - `openai.gpt-5.6-luna`
  - `openai.gpt-5.5`
  - `openai.gpt-5.4`

  "Model availability varies by AWS Region."
- **리전**: 문서는 "supported commercial AWS Regions"를 일반적으로 언급하고 예시로 `us-east-2`를 든다. 명시적 제외:
  > "Local ChatGPT Work and Codex surfaces don't support Bedrock Mantle endpoints in AWS GovCloud Regions."
- **IAM/권한**: 선택한 Bedrock 모델에 접근할 권한이 AWS 아이덴티티에 있어야 한다. Bedrock API 키 또는 AWS IAM 크레덴셜 필요.
- **사용 불가 기능 (전수 — 이 목록이 이 페이지의 핵심 가치)**:
  > "Hosted ChatGPT Work on the web, Codex cloud, and features that depend on OpenAI-hosted cloud services, hosted tools, or cloud-managed discovery aren't currently available."
  > "Fast Mode isn't available with Amazon Bedrock. Fast Mode uses priority processing, and the initial Amazon Bedrock offering supports on-demand inference only."

  개별 항목: 이미지 생성·편집 / 음성 받아쓰기 / 웹 검색 / 모바일 원격 조종 / 플러그인 공유 / 커넥터 / Chronicle / **Codex 클라우드 챗** / Sites / **GitHub 이슈·PR 위임** / **GitHub 코드 리뷰** / **Slack 클라우드 통합** / **Linear 클라우드 통합** / SAML SSO·MFA·워크스페이스 사용자 관리 / 클라우드 관리 config 정책 / ChatGPT 워크스페이스 RBAC / SCIM·EKM·도메인 검증 / 엔터프라이즈 보존·거주 통제 / 분석 대시보드 / Analytics API / Compliance API·감사 로그 / 연결된 리포지토리에 대한 Codex Security
- **부분 제한**: 브라우저 Computer Use, Chrome과 함께 쓰기, Computer Use 일반, Memories — 리전 제한. 로컬 플러그인 번들은 "when their capabilities do not require ChatGPT authentication"인 경우에만 지원. "OpenAI-curated plugin discovery and features that depend on connectors or cloud-hosted sharing aren't available."
- **트러블슈팅 체크리스트 (6항목)**: 모델 ID 정확 일치 / 모델이 제공되는 AWS 리전 지정 / 크레덴셜 유효·미만료 / AWS 아이덴티티의 모델 접근 권한 / `AWS_BEARER_TOKEN_BEDROCK`이 만료·오설정 키가 아닌지 / 데스크톱·IDE는 `~/.codex/.env`에 변수 존재
- **지원 경계 (원문)**:
  - OpenAI Support 담당: "ChatGPT Work and Codex client setup, configuration, local CLI behavior, desktop app behavior, IDE extension behavior, and the local product experience."
  - AWS·고객 담당: "AWS credentials, IAM permissions, Bedrock model access, quotas, billing, regional availability, Bedrock request failures, AWS service logs, or Bedrock service behavior."
- Claude Code 대응 관점 메모: **Codex + Amazon Bedrock ↔ Claude Code + Amazon Bedrock**. 두 제품 모두 같은 클라우드 마켓플레이스 경로를 지원하지만, 이 페이지의 진짜 가치는 **"모델 백엔드를 갈아끼우면 무엇이 사라지는가"의 완전한 목록**이다. Bedrock으로 가면 Codex 클라우드·GitHub·Slack·Linear 통합이 전부 죽는다 — 즉 그룹 C에서 다룬 기능의 상당수가 **OpenAI 호스팅 클라우드에 종속**돼 있다는 뜻이다. 이 사실은 "규제 산업에서 Bedrock으로 Codex를 쓰려는 팀"에게 결정적인 트레이드오프이며, 책에서 반드시 표로 제시할 내용이다. `model_provider = "amazon-bedrock"` 한 줄로 provider를 바꾸는 config 구조도 Claude Code의 `ANTHROPIC_BEDROCK_BASE_URL`/`CLAUDE_CODE_USE_BEDROCK` 방식과 대조된다.

---

## 7. 리소스·목록 페이지

### Use cases (목록)
- URL: https://learn.chatgpt.com/codex/use-cases
- 검색: 2026-08-02 기준
- 추출 충실도: `[구조화 추출]` — 항목·경로는 원문, 순서·중복은 렌더링 그대로
- 핵심 내용: 12개 컬렉션 + 3개 featured + 100건 이상의 개별 유스케이스 카드. **책의 실무 예시 소재 광맥.**
- **Featured (3건)**:
  - Get your email to inbox zero → `/codex/use-cases/manage-your-inbox` (Automation, Integrations) — "Clear the backlog, draft replies in your voice, and stay on top of new email"
  - Use your computer with ChatGPT → `/codex/use-cases/use-your-computer-with-codex` (Knowledge Work, Workflow) — "Let ChatGPT click, type, and navigate apps on your macOS or Windows computer"
  - Follow a goal → `/codex/use-cases/follow-goals` (Engineering, Automation) — "Give Codex a durable objective for long-running work"
- **엔지니어링·개발 관련 유스케이스 (이 책에 직접 쓸 만한 것 선별, 경로 포함)**:
  - Audit dependency incidents → `/codex/use-cases/dependency-incident-audits` (Engineering, Quality)
  - Automate bug triage → `/codex/use-cases/automation-bug-triage` (Automation, Quality)
  - Add evals to your AI application → `/codex/use-cases/ai-app-evals` (Evaluation, Quality)
  - Bring your app to ChatGPT → `/codex/use-cases/chatgpt-apps` (Integrations, Code)
  - Build and deploy internal apps → `/codex/use-cases/build-and-deploy-internal-apps` (Front-end, Integrations)
  - Build for iOS → `/codex/use-cases/native-ios-apps` (iOS, Code)
  - Build for macOS → `/codex/use-cases/native-macos-apps` (macOS, Code)
  - Build React Native apps with Expo → `/codex/use-cases/react-native-expo-apps` (Mobile, Engineering)
  - Build responsive front-end designs → `/codex/use-cases/frontend-designs` (Front-end, Design)
  - Browser-based games → `/codex/use-cases/browser-games` (Engineering, Code)
  - Code migrations → `/codex/use-cases/code-migrations` (Engineering, Code)
  - **Create a CLI Codex can use → `/codex/use-cases/agent-friendly-clis` (Engineering, Code)**
  - Debug in iOS simulator → `/codex/use-cases/ios-simulator-bug-debugging` (iOS, Code)
  - Deep security scan → `/codex/use-cases/deep-security-scan` (Engineering, Quality)
  - Deploy an app or website → `/codex/use-cases/deploy-app-or-website` (Front-end, Integrations)
  - Figma designs to code → `/codex/use-cases/figma-designs-to-code` (Front-end, Design)
  - Get from idea to proof of concept → `/codex/use-cases/idea-to-proof-of-concept` (Front-end, Engineering)
  - Iterate on difficult problems → `/codex/use-cases/iterate-on-difficult-problems` (Engineering, Analysis)
  - **Kick off coding tasks from Slack → `/codex/use-cases/slack-coding-tasks` (Integrations, Workflow)**
  - Make granular UI changes → `/codex/use-cases/make-granular-ui-changes` (Front-end, Design)
  - QA your app with Computer Use → `/codex/use-cases/qa-your-app-with-computer-use` (Automation, Quality)
  - Refactor SwiftUI screens → `/codex/use-cases/ios-swiftui-view-refactor` (iOS, Code)
  - Refactor your codebase → `/codex/use-cases/refactor-your-codebase` (Engineering, Code)
  - Remediate a vulnerability backlog → `/codex/use-cases/remediate-vulnerability-backlog` (Engineering, Quality)
  - **Reusable Codex skills / Save workflows as skills → `/codex/use-cases/reusable-codex-skills` (Engineering, Workflow)**
  - **Review GitHub pull requests → `/codex/use-cases/github-code-reviews` (Integrations, Workflow)**
  - Scan code changes for security → `/codex/use-cases/scan-code-changes-for-security` (Engineering, Quality)
  - **Understand large codebases → `/codex/use-cases/codebase-onboarding` (Engineering, Analysis)**
  - Upgrade your API integration → `/codex/use-cases/api-integration-migrations` (Evaluation, Engineering)
  - **Run verified operations → `/codex/use-cases/verified-operations-workflows` (Automation, Integrations)**
  - Add iOS app intents → `/codex/use-cases/ios-app-intents`; Add Mac telemetry → `/codex/use-cases/macos-telemetry-logs`; Adopt liquid glass → `/codex/use-cases/ios-liquid-glass`; Build a Mac app shell → `/codex/use-cases/macos-sidebar-detail-inspector`
- **비엔지니어링 유스케이스 (Data/Finance/Sales/Education/Sciences/Knowledge Work — 존재 자체가 논지)**: Analyze datasets and ship reports, Analyze product feedback across tools, Analyze KPI root causes, Annotate scRNA-seq data, Budget vs. actuals review, Build a Dashboard that stays up to date, Cash flow forecast, Clean and prepare messy data, Clean and review a financial model, Consolidate spreadsheets, Create or revise a slide deck, Dashboard builder and monitoring workflow, Diagnose a stalled deal, Discover protein folding models, Draft PRDs from internal context, Event launch playbooks, Initiative off-track brief, Learn a new concept, Manage your inbox, Measure business impact, Meeting prep briefs, Model a DCF valuation, Model strategic scenarios and tradeoffs, Monthly business review narrative, New hire onboarding, Prepare a committee packet, Prepare a leadership reporting pack, Prioritize accounts, Prioritize drug targets, Prioritize Slack action items, Project teammate, Refresh a forecast and plan, Refresh a strategic account plan, Scope an analytics request, Set up a work chief of staff (`/codex/use-cases/daily-work-brief`), Synthesize research evidence, Track bills/subscriptions/spending, Track job applications, Turn meetings into follow-ups (`/codex/use-cases/zoom-meeting-follow-ups`), Turn research into a decision memo, Turn user stories into UI mocks, Validate bulk RNA-seq inputs, Weekly work summary — 그리고 Education 계열 다수(Audit course section consistency, Build a unit plan from source files, Build an exam study system, Build an interactive lesson resource, Build a classroom materials pack, Build a lesson deck, Build a student website, Calibrate assessments, Organize a lesson or unit folder, Organize a semester workspace, Refresh course materials, Revise a lesson package, Run a student club project, Track course engagement).
- 제약·주의사항: 목록에 **중복 렌더링**이 있다(예: Forecast cash flow / Cash flow forecast가 같은 경로 `/codex/use-cases/cash-flow-forecast`, Prepare a business review / Monthly business review narrative도 동일 경로). 카드 개수를 수치로 인용하지 말 것 — "100건 이상"처럼 안전하게 쓰거나 아예 세지 말 것. 컬렉션 목록도 이 페이지에서는 12개인데 "Eight thematic collections"라는 표기와 실제 12개 나열이 어긋나 보였다. **컬렉션 수는 collections 페이지(아래) 기준 12개를 신뢰하라.**
- Claude Code 대응 관점 메모: 유스케이스의 **다수가 코딩이 아니다** — Finance, Sales, Education, Life Sciences가 각각 독립 컬렉션이다. "Codex"라는 이름이 코딩 도구를 가리키던 시절과 달리, 2026-08 기준 문서는 이것을 **범용 업무 에이전트**로 포지셔닝한다. Claude Code가 여전히 "코딩 에이전트" 정체성을 유지하는 것과 대비되는 전략적 차이이며, 책의 도입부나 결론에서 쓸 만한 관측이다. `agent-friendly-clis`("Create a CLI Codex can use")는 특히 흥미롭다 — **에이전트가 쓰기 좋은 CLI를 설계하는 법**이라는 역방향 관점.

### Collections (목록)
- URL: https://learn.chatgpt.com/codex/use-cases/collections
- 검색: 2026-08-02 기준
- 추출 충실도: `[원문]` — 12개 전수, 설명 문구 원문
- 핵심 내용: 워크플로를 실용적 순서로 묶은 가이드 컬렉션 12개.
- 전수:

| # | 컬렉션 | 설명 (원문) | 경로 |
|---|---|---|---|
| 1 | Productivity & Collaboration | "Coordinate work across plugins, data, and teams" | `/codex/use-cases/collections/productivity-and-collaboration` |
| 2 | Business Operations | "Turn initiative context and metrics into decision-ready work" | `/codex/use-cases/collections/business-operations` |
| 3 | Data Science | "Turn questions, dashboards, and raw data into review-ready analysis" | `/codex/use-cases/collections/data-science` |
| 4 | Web Development | "Build responsive UI from designs and prompts" | `/codex/use-cases/collections/web-development` |
| 5 | Game Development | "Prototype loops, UI, and gameplay faster" | `/codex/use-cases/collections/game-development` |
| 6 | Native Development | "Build and debug iOS and macOS apps" | `/codex/use-cases/collections/native-development` |
| 7 | Production Systems | "Navigate, refactor, and review real codebases" | `/codex/use-cases/collections/production-systems` |
| 8 | Security | "Assess code, review changes, and remediate security findings" | `/codex/use-cases/collections/security` |
| 9 | Finance | "Build, review, and report from financial models and operating data" | `/codex/use-cases/collections/finance` |
| 10 | Sales | "Turn account context and deal signals into pipeline actions" | `/codex/use-cases/collections/sales` |
| 11 | Life Sciences | "Use GPT-Rosalind to accelerate scientific research and drug discovery" | `/codex/use-cases/collections/life-sciences` |
| 12 | Education | "Turn teaching, learning, and academic work into review-ready artifacts" | `/codex/use-cases/collections/education` |

- 주목: **Life Sciences 설명에 "GPT-Rosalind"라는 별도 모델·제품명이 등장**한다. 이 문서 전체에서 이 이름은 여기서만 나온다 — 책에서 언급하려면 별도 확인이 필요하다(추측 금지).
- Claude Code 대응 관점 메모: "Production Systems"("Navigate, refactor, and review real codebases")가 개발자에게 가장 직접적인 컬렉션이다. 컬렉션 8·9·10·12(Security/Finance/Sales/Education)의 존재는 위 use-cases 관측을 뒷받침한다.

### Resources (목록)
- URL: https://learn.chatgpt.com/codex/resources
- 검색: 2026-08-02 기준
- 추출 충실도: `[원문]` — 항목·URL·날짜 전수
- 핵심 내용: 최신 영상 + 블로그 글 + 지원/커뮤니티 링크 허브.
- **Latest videos (6건)**:

| 제목 | 카테고리 | 날짜 | URL |
|---|---|---|---|
| Codex for Solutions Engineers: Making AI Tangible for Customers | Solutions Engineering | 2026-07-01 | https://www.youtube.com/watch?v=08hgAtg-P_8 |
| Builders Unscripted: Ep. 4 - Pietro Schirano | Builders Unscripted | 2026-06-26 | https://www.youtube.com/watch?v=SPC_yCe1cUw |
| Record & Replay in Codex | Skills | 2026-06-18 | https://www.youtube.com/watch?v=ZK3JhU73W18 |
| Build and test iOS apps without leaving Codex | Plugins | 2026-06-15 | https://www.youtube.com/watch?v=u9zLlcsCDiQ |
| Codex as a Solutions Engineering Partner | Solutions Engineering | 2026-06-15 | https://www.youtube.com/watch?v=_jNbM8pV9oI |
| Analyze earnings and update your investment thesis with Codex | Finance | 2026-06-12 | https://www.youtube.com/watch?v=Rlju1Z9e110 |

- **Blog posts (3건) — 인용 가치 높음**:

| 제목 | 날짜 | 경로 | 설명 (원문) |
|---|---|---|---|
| Mastering remote engineering work from your phone | 2026-06-23 | `/blog/mastering-codex-remote-for-engineering` | "Use Remote in the ChatGPT mobile app to start, steer, review, and organize engineering work." |
| Using skills to accelerate OSS maintenance | 2026-03-09 | `/blog/skills-agents-sdk` | "Using skills and GitHub Actions to optimize Codex workflows in the OpenAI Agents SDK repos." |
| Run long horizon tasks with Codex | 2026-02-23 | `/blog/run-long-horizon-tasks-with-codex` | — |

- **지원·커뮤니티**: Help center https://help.openai.com/en/ / Developer forum https://community.openai.com/ / OpenAI Academy https://openai.com/academy/ / Status page https://status.openai.com/
- Claude Code 대응 관점 메모: 블로그 3건이 **책의 사례 챕터에 그대로 쓸 수 있는 1차 소스**다. 특히 "Using skills to accelerate OSS maintenance"는 OpenAI 스스로가 Agents SDK 리포 유지보수에 Codex 스킬 + GitHub Actions를 쓴 자기 사례다 — 도그푸딩 근거. "Run long horizon tasks with Codex"는 App Server의 `thread/goal/set`(objective + tokenBudget)과 use-cases의 "Follow a goal"과 한 묶음으로 읽힌다. **이 세 개가 "장기 실행 작업"이라는 하나의 제품 서사를 이룬다.** (단, 세 블로그의 본문은 이번 그룹 C 범위 밖 — 필요하면 별도 수집.)

### Videos (목록)
- URL: https://learn.chatgpt.com/codex/videos
- 검색: 2026-08-02 기준
- 추출 충실도: `[원문]` — 52건 전수, 섹션 구분·날짜·카테고리 포함
- 인트로: "Learn how to use Codex with demos, walkthroughs, and talks"
- **New in ChatGPT and Codex**: Record & Replay in Codex (Skills, 2026-06-18, ZK3JhU73W18) / Debug web apps with browser use in Codex (Browser use, 2026-06-11, bhgYFRZLyKI) / Windows Computer Use and mobile access for Codex (Computer use, 2026-05-29, MPIAB-8VmCo) / Introducing Appshots in Codex (Appshots, 2026-05-21, QKYbGCvNpFo) / Computer use in Codex (Computer use, 2026-05-12, D_FCYsshMI4) / Codex can now use Chrome directly on macOS and Windows (Browser use, 2026-05-08, b6Mxcv1pyBU)
- **Apps and Prototyping**: Build and test iOS apps without leaving Codex (Plugins, 2026-06-15, u9zLlcsCDiQ) / Introducing Sites in Codex (Sites, 2026-06-05, VRvC5smyzso) / Build and share interactive prototypes in Codex (Product design, 2026-06-04, _9ImjmzAyus) / Build and share apps in Codex (Sites, 2026-06-02, 5UlRL_ImvQ0) / Introducing ChatGPT for Excel and Google Sheets (Apps, 2026-05-06, sfkyiXvlYL0)
- **Plugins and Workflows**: Run long tasks in Codex using goals (Goals, 2026-05-21, rgh0hMYPcd0) / Share Codex plugins with your team (Plugins, 2026-05-21, msSa0tc2TbU)
- **Finance and Business**: Codex for Solutions Engineers (2026-07-01, 08hgAtg-P_8) / Codex as a Solutions Engineering Partner (2026-06-15, _jNbM8pV9oI) / Analyze earnings and update your investment thesis (Finance, 2026-06-12, Rlju1Z9e110) / Build sales account strategies and outreach with Codex (Sales, 2026-06-11, 4YkOAYNZVOQ) / Codex for Finance: Faster Reports, Dashboards, and Decisions (Finance, 2026-06-09, IEYU-CgLo3E) / Codex for Sales Teams (Sales, 2026-06-04, U2C55LC0ZLM) / Prep for sales meetings faster with Codex (Sales, 2026-05-05, y5hogSW2mqU)
- **Creative and Technical Workflows**: Codex for Creatives: Riff, Design, Ship (Creative, 2026-06-11, K6wxZOqD-HY) / Creating black hole simulations with Codex (Science, 2026-06-11, 4XSI4SClBMA) / Create campaign concepts and assets with Codex (Creative, 2026-06-10, 2ey7znf8SI0) / Codex for data science (Data science, 2026-06-09, Lvk_VZOppIY)
- **Builders Unscripted**: Ep. 4 Pietro Schirano (2026-06-26, SPC_yCe1cUw) / Ep. 3 Matias Castello, Product Lead at Alchemy (2026-05-29, 8QKqENa_eQQ) / Ep. 2 Ashe Magalhaes, Founder of Hearth AI (2026-04-10, flweA_I-VKE) / **Ep. 1 Peter Steinberger, Creator of OpenClaw (2026-02-24, 9jgcT0Fqt7U)**
- **All videos (기타)**: Codex for Everyday Work: AI Agents Beyond Coding (Productivity, 2026-05-14, DLP9CagE3dU) / Bring your work into Codex in a few clicks (데스크톱 앱, 2026-05-01, flvZ6jEj3VU) / Creating an agent (Workspace Agents, 2026-04-22, Vimeo 1179656803) / Testing your agent (Workspace Agents, 2026-04-22, Vimeo 1180606828) / What is an agent? (Workspace Agents, 2026-04-22, Vimeo 1177399057) / Codex for (almost) everything (데스크톱 앱, 2026-04-16, Lm7-yFZ5fZQ) / Image Generation (2026-04-10, Vimeo 1165684590) / Writing with ChatGPT (2026-04-10, Vimeo 1167522582) / **Build Hour: API & Codex (Talk or demo, Build Hour, 2026-03-10, rhsSqr0jdFw)** / **The Codex app is now on Windows (2026-03-05, 8hNcRChDrNk)** / Codex checks its work for you (2026-02-11, dHCNpcNyoFM) / How PMs use the Codex app (Product management, 2026-02-09, 6OiE0jIY93c) / Multitasking with the Codex app (2026-02-06, 9ohXlkbXiM4) / How designers prototype using the Codex app (Design, 2026-02-04, P7HXxl14dCA) / Automate tasks with the Codex app (Scheduled tasks, 2026-02-03, xHnlzAPD9QI) / **Introducing the Codex app (2026-02-02, HFM3se4lNiw)** / **Codex in JetBrains IDEs (IDE, 2026-01-22, 1XkVsE9-ZK4)** / Codex code review (Code review, 2025-11-04, HwbSWVg5Ln4) / Build beautiful frontends with OpenAI Codex (Frontend, 2025-10-27, fK_bm84N7bs) / OpenAI Codex in your code editor (IDE, 2025-10-17, sd21Igx4HtA) / **Using OpenAI Codex CLI with GPT-5-Codex (CLI, 2025-10-14, iqNzfK4_meQ)** / Shipping with Codex (Talk or demo, DevDay, 2025-10-08, Gr41tYOzE20) / Sora, ImageGen, and Codex: The Next Wave of Creative Production (2025-10-08, 70ush8Vknx8) / **Codex intro (Talk or demo, Introduction, 2025-05-16, hhdpnbfH6NU)**
- **연표로서의 가치 (수치 주의 — 날짜는 영상 게시일이지 기능 출시일이 아니다)**: 2025-05-16 Codex intro → 2025-10 DevDay·CLI·IDE → 2026-01 JetBrains → **2026-02-02 데스크톱 앱 출시** → 2026-03-05 Windows → 2026-05 Computer Use·Chrome → 2026-06 Sites·prototypes·Record & Replay. 책의 "Codex는 어떻게 여기까지 왔나" 챕터의 뼈대로 쓸 수 있다.
- Claude Code 대응 관점 메모: **Builders Unscripted Ep. 1의 게스트가 "Peter Steinberger, Creator of OpenClaw"**라는 점이 눈에 띈다 — OpenAI 공식 채널이 서드파티 에이전트 도구 제작자를 첫 화 게스트로 세웠다. 또 "Codex for Everyday Work: AI Agents Beyond Coding"이라는 제목 자체가 use-cases 페이지에서 관측한 포지셔닝 확장을 압축한다.

---

## §8 원문 복원 보강 (`.md` 2차 수집분)

1차 WebFetch가 압축·누락한 내용을 원문에서 복원했다. **아래는 전부 `.md` 원문 검증본이므로 그대로 인용 가능하다.**

### §8-1. Code review — 표면별 분기 전문

**표면 공통 인용구:**
> "Codex reports prioritized findings without changing your working tree."

**표면별 차이 (원문):**

| 표면 | `/review` 동작 | 스코프 선택지 |
|---|---|---|
| **web** (ChatGPT Work) | 코드를 업로드하거나 설치된 source 플러그인으로 접근시킨다. 프롬프트에 PR·브랜치·커밋·파일·리뷰 기준을 명시. | 프롬프트로 지정 |
| **app** (데스크톱) | 컴포저에 `/review` 입력 → **Review against a base branch** 또는 **Review uncommitted changes** | 리뷰 페인 뷰로 전환 (아래) |
| **cli** | `/review` 입력 → CLI 리뷰 프리셋. "Codex starts a dedicated reviewer that reads the selected diff" | 4종 (아래) |
| **ide** | 컴포저에 `/review` | 2종: base branch 대비 / uncommitted |

**CLI 스코프 4종 (원문)**:
> - **Review against a base branch** finds the merge base and reviews your branch diff.
> - **Review uncommitted changes** includes staged, unstaged, and untracked files.
> - **Review a commit** reviews the exact change set for a selected commit.
> - **Custom review instructions** focuses the review on criteria you provide.

**리뷰 페인 뷰 (app) — 기본값 포함**:
> "By default, the review pane shows **Unstaged** changes. Use **Staged** for the Git index, **Commit** for a selected commit, **Branch** for the diff against your base branch, or **Last turn** for the most recent assistant turn."

> "The review pane reflects the state of your Git repository, not just what Codex edited. It includes changes made by Codex, changes you made yourself, and any other uncommitted changes in the repository."

**분리형 리뷰 설정 — 표면별 설정 키 (1차 수집에서 누락)**:

| 표면 | 설정 위치·키 |
|---|---|
| app | **Settings > General > Code review** → **Detached** 선택 |
| cli | `config.toml`의 **`review_model`** — 현재 세션과 다른 모델로 리뷰하고 싶을 때 |
| ide | **`chatgpt.reviewDelivery`** 를 `detached` 로 |

**인라인 코멘트 절차 (원문 5단계)**:
> 1. Open the review pane.
> 2. Hover over the line you want to comment on.
> 3. Select the **+** button that appears.
> 4. Write your feedback and submit it.
> 5. After you finish leaving feedback, send a message back to the chat.

> "Codex treats inline comments as review guidance. After leaving comments, send a follow-up message that makes your intent explicit, for example, “Address the inline comments and keep the scope minimal.”"

**PR 리뷰 전제 (원문)**:
> "Install the GitHub CLI (`gh`) and authenticate it with `gh auth login` so Codex can load pull request context, review comments, and changed files. If `gh` is missing or unauthenticated, pull request details may not appear in the sidebar or review pane."

**stage/revert 3단 입도 (원문)**:
> - **Entire diff**: Use the action buttons in the review header, such as **Stage all** or **Revert all**.
> - **Per file**: Stage, unstage, or revert an individual file.
> - **Per hunk**: Stage, unstage, or revert a single hunk.

> "Git can represent both staged and unstaged changes in the same file. When that happens, the pane can show the same file in both views. That's normal Git behavior."

**제약 (원문)**: "The review pane requires a project inside a Git repository. If your project isn't a Git repository yet, the app prompts you to create one." / IDE에서는 "The `/review` command appears only when the open project is inside a Git repository."

---

### §8-2. App Server — Claude Code 마이그레이션 경로 (⭐ 최대 발견, 1차 수집 전면 누락)

app-server 문서의 `### Detect and import external agent config` 절 전문. **이 책의 핵심 소재다** — OpenAI가 Claude Code 사용자의 이주 경로를 프로토콜 수준에서 구현해뒀다는 1차 증거.

> "Use `externalAgentConfig/detect` to discover external-agent artifacts that can be migrated, then pass the selected entries to `externalAgentConfig/import`."

**감지(detect) 요청·응답 — 원문 그대로**:
```json
{ "method": "externalAgentConfig/detect", "id": 63, "params": {
  "includeHome": true,
  "cwds": ["/Users/me/project"]
} }
{ "id": 63, "result": {
  "items": [
    {
      "itemType": "AGENTS_MD",
      "description": "Import /Users/me/project/CLAUDE.md to /Users/me/project/AGENTS.md.",
      "cwd": "/Users/me/project"
    },
    {
      "itemType": "SKILLS",
      "description": "Copy skill folders from /Users/me/.claude/skills to /Users/me/.agents/skills.",
      "cwd": null
    }
  ]
} }
```

**가져오기(import) — `source: "claude-code"`**:
```json
{ "method": "externalAgentConfig/import", "id": 64, "params": {
  "migrationItems": [
    {
      "itemType": "AGENTS_MD",
      "description": "Import /Users/me/project/CLAUDE.md to /Users/me/project/AGENTS.md.",
      "cwd": "/Users/me/project"
    }
  ],
  "source": "claude-code"
} }
{ "id": 64, "result": { "importId": "8ae96ff3-3425-4f4c-8772-b6fd61502868" } }
```

> "The optional top-level `source` import parameter labels the product that produced the selected migration items."

**진행·완료 알림**: `externalAgentConfig/import/progress` (항목 타입 완료 시), `externalAgentConfig/import/completed` (동기·백그라운드 임포트 전부 끝난 뒤). 둘 다 응답의 `importId`와 타입별 `successes`/`failures`를 담은 `itemTypeResults`를 포함한다. 이력 조회는 `externalAgentConfig/import/readHistories`.

**마이그레이션 가능한 `itemType` 전수 (원문)**:
> "Supported `itemType` values are `AGENTS_MD`, `CONFIG`, `SKILLS`, `PLUGINS`, `MCP_SERVER_CONFIG`, `SUBAGENTS`, `HOOKS`, `COMMANDS`, and `SESSIONS`."

즉 **CLAUDE.md·설정·스킬·플러그인·MCP 서버 설정·서브에이전트·훅·커맨드·세션** 9종이 이전 대상이다.

**중복 방지 규칙 (원문)**:
> "Detection returns only items that still have work to do. For example, Codex skips AGENTS migration when `AGENTS.md` already exists and is non-empty, and skill imports don't overwrite existing skill directories."

**Claude Code 플러그인 마켓플레이스 추론 (원문 — 매우 구체적)**:
> "When detecting plugins from `.claude/settings.json`, Codex reads configured marketplace sources from `extraKnownMarketplaces`. If `enabledPlugins` contains plugins from `claude-plugins-official` but the marketplace source is missing, Codex infers `anthropics/claude-plugins-official` as the source."

**책 활용 관점**: 이 한 절이 "Codex vs Claude Code" 비교 챕터의 척추가 될 수 있다. 개념 대응표가 OpenAI 자신의 손으로 작성돼 있다 — `CLAUDE.md ↔ AGENTS.md`, `~/.claude/skills ↔ ~/.agents/skills`, `.claude/settings.json ↔ Codex config`, 그리고 subagents·hooks·commands·MCP 설정이 1:1로 대응한다는 사실. **추측이 아니라 문서에 박힌 매핑이다.** 별도 문서 `/codex/import` ("Import from another agent")가 색인에 존재하므로 후속 수집 1순위.

---

### §8-3. App Server — 1차 수집에서 통째로 빠진 섹션 2개

`.md` 원문의 실제 헤딩 구조(라인 번호 기준)를 확인한 결과, 1차 수집이 잡은 62개 항목 뒤에 **두 개의 큰 섹션이 더 있었다**:

**(a) `## Apps (connectors)`** — 하위에 `### Config RPC examples for app settings`, `### Detect and import external agent config`(위 §8-2)

**(b) `## Auth endpoints`** — 하위 10개 절 전수:
> `### Authentication modes` / `### API overview` / `### 1) Check auth state` / `### 2) Log in with an API key` / `### 3) Log in with ChatGPT (browser flow)` / `### 3b) Log in with ChatGPT (device-code flow)` / `### 3c) Log in with externally managed ChatGPT tokens (`chatgptAuthTokens`)` / `### 4) Cancel a ChatGPT login` / `### 5) Logout` / `### 6) Rate limits (ChatGPT)` / `### 7) Token usage (ChatGPT)` / `### 8) Earned rate-limit resets (ChatGPT)` / `### 9) Notify a workspace owner about a limit` / `### 10) Workspace messages (ChatGPT)`

원문 설명:
> "The JSON-RPC auth/account surface exposes request/response methods plus server-initiated notifications (no `id`). Use these to determine auth state, start or cancel logins, logout, inspect ChatGPT rate limits, and notify workspace owners about depleted credits or usage limits."

**주목**: 레이트리밋·토큰 사용량·"earned rate-limit resets"·워크스페이스 소유자 알림이 **프로토콜 1급 시민**이다. 즉 Codex를 임베드하는 제품은 사용량 한도를 직접 조회·표시할 수 있다. 이 절의 상세 스키마는 이번 범위에서 수집하지 않았다 — **사용량·요금 챕터를 쓴다면 재방문 필수**(`app-server.md` 1858행 이하).

**1차 수집 수치 전량 재검증 완료** (원문 라인 확인):
- JSON-RPC `-32001` + `"Server overloaded; retry later."` ✓ (원문 84–85행) — 추가로 "Clients should retry with an exponentially..." 백오프 권고 존재
- `-32601` (paginated 미지원) ✓ (503행)
- goal objective **"non-empty and at most 4,000 characters"** ✓ (569행)

---

### §8-4. Cloud environments — 실무 함정 3건 (1차 수집 누락)

**⚠️ 함정 1 — 셋업 스크립트의 `export`는 에이전트에 전달되지 않는다 (원문)**:
> "Setup scripts run in a separate Bash session from the agent, so commands like `export` do not persist into the agent phase. To persist environment variables, add them to `~/.bashrc` or configure them in environment settings."

이건 클라우드 환경에서 가장 흔한 실패 원인이다. 반드시 책에 실을 것.

**함정 2 — 캐시 무효화 트리거와 수동 리셋 (원문)**:
> "Codex automatically invalidates the cache if you change the setup script, maintenance script, environment variables, or secrets. If your repo changes in a way that makes the cached state incompatible, select **Reset cache** on the environment page."

**함정 3 — 캐시 생성/재개 시 동작이 다르다 (원문)**:
> 캐시될 때: "Codex clones the repository and checks out the default branch. Codex runs the setup script and caches the resulting container state."
> 캐시 재개 시: "Codex checks out the branch specified for the chat. Codex runs the maintenance script (optional). This is useful when the setup script ran on an older commit and dependencies need to be updated."

**추가 사실**:
- 환경 설정 URL: `https://chatgpt.com/codex/settings/environments`
- 이미지 이름은 **`universal`** ("The Codex agent runs in a default container image called `universal`")
- 버전 핀 UI: 환경 설정에서 **Set package versions** 선택 → Python·Node.js 및 기타 런타임 고정
- `openai/codex-universal`은 "a reference Dockerfile and an image that can be pulled and tested locally" — **로컬에서 당겨 테스트 가능**
- 시크릿 암호화 정밀 표현: "stored with an additional layer of encryption and are only decrypted for task execution"

---

### §8-5. Worktrees — 원문 복원분

**시작 커밋 규칙 (1차 누락, 원문)**:
> "Codex creates worktrees in `$CODEX_HOME/worktrees`. The starting commit is the `HEAD` commit of the branch selected when you start your chat. If you chose a branch with local changes, Codex applies the uncommitted changes to the worktree as well. The worktree isn't checked out as a branch. It's in a detached HEAD state. This lets Codex create several worktrees without polluting your branches."

**`.worktreeinclude` 실제 예시 파일 (원문 코드블록)**:
```text
# .worktreeinclude
.env
.env.local
config/secrets.json
```
> "Codex only copies ignored files that match `.worktreeinclude`; it doesn't copy other local files that Git doesn't track. Don't list tracked files."
> "Codex automatically copies an ignored `AGENTS.override.md` into local managed worktrees, so you don't need to list it in `.worktreeinclude`."

**Handoff와 gitignore의 상호작용 (1차 누락, 중요)**:
> "Since Handoff uses Git operations, any files that are part of your `.gitignore` file won't move with the chat unless Codex copies them into a local managed worktree with `.worktreeinclude`."

**worktree 정리 규칙 — 삭제되지 않는 조건 / 삭제되는 조건 (1차 누락, 원문)**:
> Codex-managed worktrees **won't** be deleted automatically if:
> - A pinned chat is tied to it
> - The chat is still in progress
> - The worktree is a permanent worktree
>
> Codex-managed worktrees **are** deleted automatically when:
> - You archive the associated chat
> - Codex needs to delete older worktrees to stay within your configured limit

> "By default, Codex keeps your most recent 15 Codex-managed worktrees. You can change this limit or turn off automatic deletion in settings if you prefer to manage disk usage yourself."
> "Before deleting a Codex-managed worktree, Codex saves a snapshot of the work on it. If you open a chat after its worktree was deleted, you'll see the option to restore it."

이유 설명 (원문, 디스크 관점): "Worktrees can take up a lot of disk space. Each one has its own set of repository files, dependencies, build caches, etc."

**브랜치 제약의 근본 원인 — Git 내부 설명 (1차 누락, 원문 전문)**:
> "Git prevents the same branch from being checked out in more than one worktree at a time because a branch represents a single mutable reference (`refs/heads/<name>`) whose meaning is "the current checked-out state" of a working tree.
> When a branch is checked out, Git treats its HEAD as owned by that worktree and expects operations like commits, resets, rebases, and merges to advance that reference in a well-defined, serialized way. Allowing multiple worktrees to simultaneously check out the same branch would create ambiguity and race conditions around which worktree's operations update the branch reference, potentially leading to lost commits, inconsistent indexes, or unclear conflict resolution.
> By enforcing a one-branch-per-worktree rule, Git guarantees that each branch has a single authoritative working copy, while still allowing other worktrees to safely reference the same commits via detached HEADs or separate branches."

**해결 지침 (원문)**: "If you plan on checking out the branch locally, use Handoff to move the chat into Local instead of trying to keep the same branch checked out in both places at once." / UI 버튼명은 **Create branch here**.

---

### §8-6. Codex SDK — 원문 복원분 (아키텍처 사실 포함)

**⭐ 아키텍처 사실 (1차 누락, 원문)**:
> "The Python SDK controls the local Codex app-server over JSON-RPC."

즉 **SDK는 app-server 위의 얇은 래퍼다.** 앞서 추론으로 적었던 것이 원문으로 확인됐다.

**SDK 선택 기준 (원문 — 결정 규칙으로 인용 가치 높음)**:
> "Use the Codex SDK for coding-focused Codex threads. If Codex is one specialist inside a broader orchestrated workflow, run Codex CLI as an MCP server and orchestrate it with the Agents SDK."

**베타 상태와 설치 규칙 정정 (1차 수집이 부정확했음, 원문)**:
> "While the Python SDK is in beta, `pip install openai-codex` selects the latest published beta build. After a stable SDK release exists, use `pip install --pre openai-codex` to opt in to newer prerelease builds."

→ 즉 `--pre`는 **지금 필요한 게 아니라 안정판 출시 이후**에 프리릴리스를 원할 때 쓴다. 1차 기록("프리릴리스 빌드: `pip install --pre openai-codex`")은 시점 조건이 빠져 오해 소지가 있었다. **2026-08 기준 Python SDK는 베타다.**

**샌드박스 프리셋 설명 (원문 그대로)**:
> - `Sandbox.read_only`: Read files without allowing writes.
> - `Sandbox.workspace_write`: Read files and write inside the workspace and configured writable roots.
> - `Sandbox.full_access`: Run without filesystem access restrictions.

> "When you omit `sandbox=`, app-server uses its configured default. A sandbox passed to `run(...)` or `turn(...)` applies to that turn and later turns on the thread."

**공식 리포 경로 (1차 누락)**:
- TypeScript: https://github.com/openai/codex/tree/main/sdk/typescript
- Python: https://github.com/openai/codex/tree/main/sdk/python

**별도 SDK 존재 (1차 누락)**: 베타 접근 권한이 있고 "repository or change scans with structured security findings and coverage"가 필요하면 **Codex Security TypeScript SDK** (`/codex/security/sdk`)를 쓰라고 안내한다.

**⚠️ 주의**: `.md` 원문의 TypeScript 첫 예제는 코드 펜스 안 `import` 줄이 비어 있다(렌더링 파이프라인 이슈로 보임). 1차 WebFetch 렌더본에는 `import { Codex } from "@openai/codex-sdk";`가 있었다. **책에 실을 때는 import 줄을 포함하되, 이 한 줄만은 실제 SDK로 재확인할 것.**

---

### §8-7. GitHub Action — 원문 복원분

**`codex-args` 실제 예시 (1차 누락, 원문)**:
> "`codex-args`: Extra CLI flags. Provide a JSON array (for example `["--ephemeral"]`) or a shell string (`--profile ci`) to configure sessions, profiles, or MCP settings."

**프롬프트 보관 관례 (원문)**: "Consider storing prompts in `.github/codex/prompts/`."

**`allow-users` 기본 동작 (1차 누락 — 중요)**:
> "`allow-users` and `allow-bots` restrict who can trigger the workflow. **By default only users with write access can run the action**; list extra trusted accounts explicitly or leave the field empty for the default behavior."

**`read-only`의 한계 (원문)**:
> "`read-only` keeps Codex from changing files or using the network, but it still runs with elevated privileges. Don't rely on `read-only` alone to protect secrets."

**구조화 출력 경로 (1차 누락)**:
> "When you need structured data, pass `--output-schema` through `codex-args` to enforce a JSON shape."

**프롬프트 인젝션 경고 정밀 표현 (원문)**:
> "Sanitize prompt inputs from pull requests, commit messages, or issue bodies to avoid prompt injection. **Review HTML comments or hidden text** before feeding it to Codex."

**Troubleshooting 절 전문 (1차 수집 전면 누락)**:
> - **You set both prompt and prompt-file**: Remove the duplicate input so you provide exactly one source.
> - **responses-api-proxy didn't write server info**: Confirm the API key is present and valid; the proxy starts only when you provide `openai-api-key`.
> - **Expected `sudo` removal, but `sudo` succeeded**: Ensure no earlier step restored `sudo` and that the runner OS is Linux or macOS. Re-run with a fresh job.
> - **Permission errors after `drop-sudo`**: Grant write access before the action runs (for example with `chmod -R g+rwX "$GITHUB_WORKSPACE"` or by using the unprivileged-user pattern).
> - **Unauthorized trigger blocked**: Adjust `allow-users` or `allow-bots` inputs if you need to permit service accounts beyond the default write collaborators.

**참고 예제 링크 (1차 누락)**: `unprivileged-user` 실사용 예 — https://github.com/openai/codex-action/blob/main/examples/unprivileged-user.yml

---

### §8-8. GitHub 통합 — 원문 복원분

**설정 URL 정확값 (1차 누락)**: `https://chatgpt.com/codex/settings/code-review`

**AGENTS.md 계층 적용 규칙 (1차 누락 — 실무 핵심, 원문)**:
> "Codex searches your repository for `AGENTS.md` files and follows the applicable code review rules. Add a `## Code Review Rules` section to the file closest to the code the rules govern. Use `###` headings to group related checks when helpful."
> "Put repository-wide rules in the root `AGENTS.md` and service-specific rules in a nested file, such as `services/experiment_reporting/AGENTS.md`. Codex applies the root and more-specific guidance that covers each changed file, so unrelated changes don't have to carry service-specific context."

**규칙 작성 착수 지침 (원문)**: "Start with two or three concise rules that encode checks reviewers often explain."

**규칙 4원칙 — 원문 전문 (1차에서 제목만 잡혔음)**:
> - **Focus on consequential, repository-specific behavior.** Describe the compatibility constraint, data boundary, or unsafe side effect to flag and why it matters.
> - **State the safe path or exception.** Give Codex enough context to distinguish a real issue from expected behavior.
> - **Keep rules scoped and durable.** Prefer outcomes over function names that can change, and place guidance near the code it governs.
> - **Leave mechanical checks in CI.** Keep formatting, lint, and other deterministic checks out of review rules.

**반복 개선 루프 (원문)**: "Open a representative pull request and request a review with `@codex review`. Refine the rules based on the findings and feedback you see, and narrow or remove guidance that produces noise."

**P0/P1 정확한 표현 (원문)**: "In GitHub, Codex flags only P0 and P1 issues so review comments stay focused on high-priority risks." — **GitHub 표면에 한정된 규칙**이다.

**추가 트리거 예시 (1차 누락)**: `@codex fix the CI failures` (review 이외의 지시는 PR을 컨텍스트로 클라우드 챗 시작)

**Troubleshoot 절 (1차 누락)**: Code review 토글 확인 / 리포에 Codex cloud 설정 확인 / **정확한 트리거 `@codex review` 사용** / 자동 리뷰는 Automatic reviews 활성 + PR 이벤트가 리뷰 트리거 설정과 일치하는지 확인.

**참고 영상**: 이 페이지에 "Codex code review walkthrough" 영상 임베드 (`HwbSWVg5Ln4` — videos 목록의 2025-11-04 "Codex code review"와 동일).

---

### §8-9. Local environments / Integrated terminal / Modes — 원문 복원분

**Local environments**:
- 설정 페인은 **`codex://settings`** 커스텀 URL 스킴으로 열린다 (1차 누락)
- 셋업 스크립트 실행 시점 정밀화: "Setup scripts run automatically when Codex creates a new worktree **at the start of a new chat**."
- 액션 식별: "To identify your actions, choose an icon associated with each action." (아이콘 지정 가능 — 1차 누락)
- 액션 vs 터미널 사용 구분 (원문): "Actions are helpful to keep you from typing common actions like triggering a build for your project or starting a development server. For one-off quick debugging you can use the integrated terminal directly."
- Git 도구의 한계 (원문, 1차 누락): "Use the integrated terminal for Git operations that aren't exposed in the app. To isolate concurrent changes from your local checkout, start the task in a worktree."

**Integrated terminal** — 1차 수집 내용이 원문과 일치함(✓). 보강 표현:
> "Each chat in the ChatGPT desktop app includes a terminal scoped to its current project or worktree."
> "Use the terminal to validate changes, run scripts, and perform Git operations without switching apps. ChatGPT can read the current terminal output, so it can check a running development server or refer to a failed build while it works with you."

**Modes** — 1차 수집 내용이 원문과 완전히 일치함(✓). 페이지 전문이 979바이트로 매우 짧으며, **비교표가 없다는 관찰도 확정.** 진입 경로 원문: "In the ChatGPT desktop app, open the ChatGPT dropdown and select **Codex**."

---

### §8-10. Amazon Bedrock / Remote connections / Slack / Linear / MCP server — 검증 결과

**전부 1차 수집 내용이 원문과 일치함(✓).** 재검증된 항목:
- Bedrock 지원 모델 5종 ID 정확 일치 (`openai.gpt-5.6-sol` / `-terra` / `-luna` / `openai.gpt-5.5` / `openai.gpt-5.4`) ✓
- "Amazon Bedrock **Mantle** path" 표현 및 GovCloud 미지원 문장 ✓
- `AWS_REGION=us-east-2` 예시 ✓
- Remote connections의 **June 8, 2026** 페어링 기준일 — 원문에 3회 등장 ✓
- non-interactive-mode의 `CODEX_API_KEY`·`--ephemeral`·`--skip-git-repo-check`·`--full-auto` deprecated 서술 전부 ✓ (원문 385행 분량, 1차 수집이 이미 전문에 가까웠음)
- Slack·Linear 페이지는 1차에서 이미 `[원문]` 등급이었고 재검증에서 차이 없음 ✓
- mcp-server의 `codex`/`codex-reply` 도구 파라미터 표 2개, Agents SDK 예제 코드 전부 일치 ✓

---

## 접근 실패 URL

**1차(WebFetch): 21/21 전수 성공, 실패 0건.**
**2차(`.md` 원문): 17/21 성공, 4건은 `.md` 미제공(404).**

| URL | `.md` 결과 | 판정 |
|---|---|---|
| `/codex/use-cases` | 404 | 동적 목록 페이지 — `.md` 소스 없음. WebFetch 결과가 유일 근거이며 유효 |
| `/codex/use-cases/collections` | 404 | 동일 |
| `/codex/resources` | 404 | 동일 |
| `/codex/videos` | 404 | 동일 |

`developers.openai.com/codex/{use-cases,resources,videos}.md`도 동일하게 404였다. 두 호스트 모두 이 4개는 정적 markdown을 제공하지 않는다 — **접근 실패가 아니라 구조적 부재**다.

**따라서 재방문 권장 목록은 §0 보강으로 대부분 해소되었다.** 남은 재방문 대상은 아래 두 건뿐:

| 대상 | 사유 |
|---|---|
| `app-server.md` 1858행 이하 (`## Auth endpoints` 10개 절) | 레이트리밋·토큰 사용량·워크스페이스 알림 스키마 미수집. **사용량/요금 챕터를 쓸 경우 필수** |
| `app-server.md` 1503행 이하 (`## Apps (connectors)`) | 커넥터 설정 RPC 예시 미수집 |

다만 다음은 "성공했으나 추출 충실도가 낮아 재방문 권장" 목록이다:

| URL | 사유 |
|---|---|
| https://learn.chatgpt.com/codex/environments/modes | 페이지 자체가 매우 짧아 추가 정보 없음 — 재방문 불필요하나, 비교표가 없다는 사실만 재확인 |
| https://learn.chatgpt.com/codex/code-review | 리뷰 페인 조작·트러블슈팅 섹션의 문장 단위 인용이 필요하면 재방문 |
| https://learn.chatgpt.com/codex/github-action | "Configure `codex exec`", "Capture outputs", "Troubleshooting" 섹션 본문이 요약됨 — 챕터에서 깊게 다루면 재방문 |
| https://learn.chatgpt.com/codex/environments/cloud-environment | maintenance script 예시와 인터넷 접근 세부 설정값이 회수되지 않음 — `/codex/cloud/internet-access` 함께 재방문 |
| https://learn.chatgpt.com/codex/codex-sdk | 페이지가 실제로 짧을 가능성이 높으나, TS 쪽 옵션 표가 있었다면 누락 가능 |

---

## 추가 발견 URL

과제 목록에 없었으나 (a) 그룹 C 페이지들의 링크와 (b) **공식 색인 `https://developers.openai.com/llms.txt`**에서 발견된 URL. **본문은 수집하지 않았고 목록만 남긴다.**

> **호스트 주의:** `learn.chatgpt.com/codex/{path}` 와 `developers.openai.com/codex/{path}` 는 같은 문서다. 어느 쪽이든 끝에 `.md`를 붙이면 원문이 나온다. 원문 내부 링크는 `/docs/{path}` 형태로 쓰여 있으니 혼동 말 것.

### ⭐ 공식 색인에서 발견한 미방문 `/codex/*` 경로 (우선순위별)

**1순위 — 이 책의 Claude Code 비교·이주 챕터에 직결:**
- `/codex/import` — **"Import from another agent"** (§8-2의 `externalAgentConfig` UI 대응 문서)
- `/codex/agent-configuration/agents-md` — Custom instructions with AGENTS.md
- `/codex/agent-configuration/subagents` — Subagents
- `/codex/agent-configuration/rules` — Rules
- `/codex/hooks` — Hooks
- `/codex/build-skills` · `/codex/build-plugins` · `/codex/skills-and-plugins` · `/codex/plugins`
- `/codex/extend/mcp` — Model Context Protocol
- `/codex/extend/record-and-replay` — Record & Replay
- `/codex/permission-modes` · `/codex/permissions` — Permissions (동명이 두 경로)
- `/codex/sandboxing` — Sandbox / `/codex/sandboxing/auto-review` — Auto-review
- `/codex/agent-approvals-security` — Agent approvals & security

**2순위 — 설정·명령 레퍼런스 (책의 레퍼런스 부록용):**
- `/codex/config-file/config-basic` · `config-advanced` · `config-reference` · `config-sample` · `environment-variables`
- `/codex/configuration` · `/codex/cli-customization` · `/codex/custom-prompts`
- `/codex/cli` (Codex CLI) · `/codex/cli/reference` (Command line options) · `/codex/cli/slash-commands`
- `/codex/ide` · `/codex/ide/commands` · `/codex/ide/settings` · `/codex/ide/slash-commands`
- `/codex/app` · `/codex/app/commands` · `/codex/app/settings` · `/codex/app/windows`
- `/codex/reference/troubleshooting` · `/codex/glossary` · `/codex/feature-maturity`

**3순위 — 기능·개념:**
- `/codex/overview` · `/codex/quickstart` · `/codex/features` · `/codex/models` · `/codex/pricing` · `/codex/whats-new`
- `/codex/prompting` · `/codex/learn/best-practices` · `/codex/long-running-work` · `/codex/projects`
- `/codex/cloud` · `/codex/cloud/internet-access` · `/codex/web` · `/codex/auth`
- `/codex/computer-use` · `/codex/browser` · `/codex/chrome-extension` · `/codex/appshots` · `/codex/sites` · `/codex/visualizations` · `/codex/artifacts-viewer`
- `/codex/automations` (Scheduled tasks) · `/codex/notifications` · `/codex/web-search` · `/codex/image-generation` · `/codex/image-inputs`
- `/codex/customization/overview` · `/codex/customization/memories` · `/codex/customization/chronicle`
- `/codex/features/codex-micro` · `/codex/features/voice` · `/codex/agent-configuration/speed`
- `/codex/windows/windows-app` · `/codex/windows/windows-sandbox` · `/codex/windows/wsl`
- `/codex/pets` (!)

**4순위 — Codex Security 제품군 (별도 제품, 범위 밖이나 존재는 기록):**
- `/codex/security` · `/codex/security/setup` · `/codex/security/faq` · `/codex/security/sdk` · `/codex/security/threat-model`
- `/codex/security/cli` · `/codex/security/cli/reference` · `/codex/security/cli/faq` · `/codex/security/cli/ci` · `/codex/security/cli/bulk-scans`
- `/codex/security/plugin` · `/codex/security/plugin/{scans,deep-scans,code-changes,fix-findings,export-findings,triage-backlog,vulnerability-reports,security-hardening,workbench,changelog}`
- `/codex/cyber-safety`

**5순위 — 엔터프라이즈·거버넌스:**
- `/codex/administration` · `/codex/security-administration` · `/codex/get-started-with-work` · `/codex/use-chatgpt` · `/codex/personalize`
- `/codex/enterprise/{admin-setup,access-tokens,analytics-api,compliance-api,governance,groups-and-provisioning,managed-configuration,roles-and-workspace-permissions,skills,apps-and-connectors,usage-limits,windows-deployment,work-admin-faq,workspace-analytics,workspace-model-availability}`
- `/codex/open-source` · `/codex/community/codex-for-oss` · `/codex/guides/build-ai-native-engineering-team`

**색인·전문 덤프 (수집 도구로 유용):**
- `https://developers.openai.com/llms.txt` — 전체 문서 색인 (107KB, 작동 확인)
- `https://developers.openai.com/codex/llms.txt` — Codex 색인
- `https://developers.openai.com/codex/llms-full.txt` — **Codex 전 문서 전문 덤프** (후속 리서치에 강력 추천)
- ⚠️ `https://learn.chatgpt.com/llms.txt` 는 **404**다 (문서 본문이 이 URL을 안내하지만 실제로는 SPA 셸 반환)

### Codex 문서 내부 (learn.chatgpt.com)
- `/codex/build-skills` — 스킬 작성 (developers 허브)
- `/codex/build-plugins` — 플러그인 작성 (developers 허브)
- `/codex/hooks` — 훅 (developers 허브)
- `/codex/cli-customization` — CLI 커스터마이즈 (developers 허브 Reference)
- `/codex/developer-commands` — 개발자 명령 레퍼런스 (developers 허브 / non-interactive-mode에서 `?surface=cli#cli-codex-exec` 앵커로 참조)
- `/codex/developer-settings` — 개발자 설정 (developers 허브)
- `/codex/cloud` — Codex 클라우드 챗 (slack·linear에서 참조)
- `/codex/cloud/internet-access` — 에이전트 인터넷 접근 (cloud-environment에서 참조) **← 우선 재방문 후보**
- `/codex/auth/ci-cd-auth` — CI/CD에서 Codex 계정 인증 유지 (고급) (non-interactive-mode에서 참조) **← 우선 재방문 후보**
- `/codex/agent-approvals-security` — 보안 문서 (slack·linear에서 참조) **← 우선 재방문 후보**
- `/codex/prompting` — Concepts 섹션 (modes에서 참조)

### 블로그 (learn.chatgpt.com/blog)
- `/blog/mastering-codex-remote-for-engineering` (2026-06-23)
- `/blog/skills-agents-sdk` (2026-03-09)
- `/blog/run-long-horizon-tasks-with-codex` (2026-02-23)

### 유스케이스 (전체는 위 use-cases 섹션 참조 — 우선 후보만)
- `/codex/use-cases/follow-goals` — Follow a goal (Featured, 장기 목표)
- `/codex/use-cases/agent-friendly-clis` — Create a CLI Codex can use
- `/codex/use-cases/reusable-codex-skills` — Reusable Codex skills
- `/codex/use-cases/codebase-onboarding` — Understand large codebases
- `/codex/use-cases/github-code-reviews` — Review GitHub pull requests
- `/codex/use-cases/slack-coding-tasks` — Kick off coding tasks from Slack
- `/codex/use-cases/verified-operations-workflows` — Run verified operations
- `/codex/use-cases/code-migrations` — Code migrations
- `/codex/use-cases/refactor-your-codebase` — Refactor your codebase
- 컬렉션 12개: `/codex/use-cases/collections/{productivity-and-collaboration | business-operations | data-science | web-development | game-development | native-development | production-systems | security | finance | sales | life-sciences | education}`

### 외부 (GitHub·기타)
- https://github.com/openai/codex-action — GitHub Action 리포
- https://github.com/openai/codex-action/blob/main/docs/security.md — 액션 보안 체크리스트
- `openai/codex-universal` (GitHub) — 클라우드 기본 유니버설 이미지 레퍼런스
- Codex GitHub 리포지토리 — App Server 오픈소스 구현 (app-server 페이지가 언급, 정확한 URL은 미회수)
- https://mcp.linear.app/mcp — Linear MCP 엔드포인트
- https://chatgpt.com/codex/settings/connectors — Codex 커넥터 설정
- https://chatgpt.com/admin/settings — ChatGPT 워크스페이스 관리자 설정
- https://chatgpt.com/pricing — 플랜·가격
- https://help.openai.com/en/ · https://community.openai.com/ · https://openai.com/academy/ · https://status.openai.com/
- 영상 52건의 YouTube·Vimeo URL (위 videos 섹션에 전수 기재)

---

## 수집 한계 (fact-checker 전달 사항)

1. **발행일 부재.** learn.chatgpt.com의 문서 페이지에는 발행일·최종수정일 표기가 없다. 이 문서의 모든 사실은 **2026-08-02 방문 기준**으로만 유효하다. 챕터에서 버전·수치를 쓸 때는 "2026년 8월 기준"을 반드시 병기하라.
2. **추출 방식 — 2차 보강으로 해소됨.** 1차 WebFetch는 이 사이트를 요약하는 경향이 있었으나, 2차에서 `.md` 원문 수집(§0)으로 **17/21 페이지를 원문 검증**했다. 나머지 4개(동적 목록 페이지)는 항목명·URL·날짜만 인용하고 개수는 단정하지 않는다.
   - **인용 안전:** `[원문✓]` 라벨이 붙은 페이지의 모든 코드 블록·표·따옴표 문장.
   - **인용 시 주의:** §8-6에 적은 Codex SDK의 TypeScript `import` 한 줄(원문 코드펜스에서 누락되어 있음).
   - 1차 수집분 중 **오류 1건**(code-review 섹션 구조)을 정정했다. 같은 유형의 혼동이 더 있을 가능성은 낮지만, 페이지 구조를 논거로 삼을 때는 §8을 우선하라.
3. **수치 인용 시 주의 목록**:
   - "최근 15개 worktree 보존" (git-worktrees)
   - "캐시 최대 12시간" (cloud-environment)
   - "goal objective 최대 4,000자" (app-server)
   - "June 8, 2026 페어링 기준일" (remote-connections)
   - JSON-RPC 에러 코드 `-32001`, `-32601` (app-server)
   - 유스케이스 카드 개수 — **중복 렌더링이 있으므로 개수를 단정하지 말 것**
4. **의도적으로 수집하지 않은 것**: 이 그룹 범위 밖인 하위 링크의 본문(위 "추가 발견 URL"). 블로그 3건과 `/codex/cloud/internet-access`·`/codex/auth/ci-cd-auth`·`/codex/agent-approvals-security`는 책의 보안·자동화 챕터가 깊어지면 별도 수집이 필요하다.
5. **표기 불일치 경고 (책에서 반드시 짚을 것)**: 같은 개념이 표면마다 표기가 다르다.
   - 승인 정책: MCP 도구 `untrusted`/`on-request`/`never` ↔ App Server `unlessTrusted`/`onRequest`/`never`
   - 샌드박스: CLI·MCP `read-only`/`workspace-write`/`danger-full-access` ↔ App Server `readOnly`/`workspaceWrite` ↔ Python SDK `Sandbox.read_only`/`Sandbox.workspace_write`/`Sandbox.full_access`
   - 이벤트: `codex exec --json`은 점 표기(`thread.started`) ↔ App Server는 슬래시 표기(`thread/started`)
   이는 추측이 아니라 각 페이지 원문 대조로 확인된 사실이다.
