# 그룹 A: 기초·개념·제품 표면 (33 URL) — 검색 2026-08-02 기준

<!-- 검색 시점: 2026-08-02 기준 -->

## 수집 방법 메모 (재현·검증용)

- `https://learn.chatgpt.com/codex/{path}` 는 **308 리다이렉트로 `https://learn.chatgpt.com/docs/{path}` 로 이동**한다. 문서 사이트의 정전(canonical) 경로는 `/docs/`다.
- 모든 문서 페이지는 **URL 끝에 `.md`를 붙이면 원문 마크다운**을 반환한다 (`content-type: text/markdown`). 예: `https://learn.chatgpt.com/docs/quickstart.md`. 본 리서치는 요약 손실을 피하기 위해 전 페이지를 이 방식으로 수집했다.
- 문서 사이트가 스스로 안내하는 전체 색인: `https://learn.chatgpt.com/llms.txt` (1,787줄). 사이트맵: `https://learn.chatgpt.com/chatgpt-sitemap-0.xml` (246 URL, 그중 `/docs/` 125개).
- 페이지 상단마다 다음 안내문이 반복 삽입되어 있다 (원문 그대로):
  > For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

**신선도 경고:** 이 문서군은 2026년 7월 말까지의 릴리스를 반영한다. Codex/ChatGPT는 주 단위로 변하므로(창고 changelog 기준 2026년에만 70여 건), 모델명·요금·한도는 반드시 "2026-08-02 기준"으로 못 박아 서술할 것.

---

## 자료 1: Overview (Codex 랜딩)

- URL: https://learn.chatgpt.com/codex → `https://learn.chatgpt.com/docs`
- 검색: 2026-08-02 기준
- 신뢰성: 최상 (OpenAI 공식 1차 문서)
- 핵심 내용: 랜딩 페이지는 산문 본문이 사실상 없다. 마크다운 소스(`/docs/overview.md`)는 `<CodexOverviewLanding />` 컴포넌트 한 줄뿐이며, 실제 내용은 렌더링된 카드 UI다. 헤드라인은 "Start with a goal, idea, or task. ChatGPT can gather context, take action, and produce something useful." 좌측 사이드바 구조(New chat / Search / Scheduled tasks / Plugins / Sites / Pull requests, Pinned, Projects, Chats)와 "What should we build?" 진입 카드(코드 탐색·이해, 새 기능·앱·도구 제작, 코드 리뷰 및 변경 제안, 문제·버그 수정, 프로젝트 선택)를 노출한다.
- 명령·플래그·설정 키: 없음
- 수치·요금·모델명·버전: 랜딩의 "최근 소식" 카드가 GPT-5.6 3종(Sol / Terra / Luna)과 Codex Micro를 홍보 (2026년 7월 기준)
- 코드 예시 요지: 없음
- 제약·주의사항: **이 페이지는 인용 가치가 낮다.** 책의 1차 근거로 쓰지 말고, 아래 개별 문서를 근거로 삼을 것.
- 관련 섹션: 1장 도입부의 "Codex 제품 지도" 정도로만 활용
- Claude Code 대응 관점 메모: Claude Code에는 대응하는 GUI 랜딩이 없다 — 이것이 두 제품의 첫 번째 구조적 차이다 (Codex는 데스크톱 앱이 1급 표면, Claude Code는 CLI가 1급 표면).

---

## 자료 2: Quickstart

- URL: https://learn.chatgpt.com/codex/quickstart
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: ChatGPT를 쓸 표면을 고르고(데스크톱 앱 / 웹) 첫 메시지를 보내는 4단계 온보딩. 개발자가 터미널·에디터에서 쓰려면 Codex CLI 또는 Codex IDE 확장으로 안내한다.
  - **데스크톱 경로 4단계:** ① ChatGPT 데스크톱 앱 설치(Windows/macOS) → ② 앱 열고 ChatGPT 계정으로 로그인 → ③ ChatGPT가 작업할 위치 선택(채팅 시작, 프로젝트 생성, 폴더 열기 — "ChatGPT can read and modify files in the folder you choose") → ④ 첫 메시지 전송.
  - ④단계의 모드 선택 규칙 (원문 요지):
    - 리서치·분석·산출물(문서·프레젠테이션·스프레드시트·Sites) → **ChatGPT** 선택 후 컴포저 위 상단에서 **Work**로 전환
    - 코드베이스 컨텍스트와 개발자 도구가 필요한 소프트웨어 개발 → ChatGPT 드롭다운에서 **Codex** 선택
    - 가벼운 질문·잡담 → **ChatGPT** → 상단 스위처에서 **Chat**. Codex 안에서는 **New chat**에 마우스를 올린 뒤 오른쪽의 **Quick chat** 아이콘 선택
  - **웹 경로 4단계:** ① chatgpt.com 접속·로그인 → ② Chat 또는 Work 선택 → ③ 채팅 시작 또는 프로젝트 선택 → ④ 첫 메시지 전송
- 명령·플래그·설정 키: 없음(GUI 절차). 관련 링크로 `/docs/codex/cli`, `/docs/codex/ide`, `/docs/pricing#feature-availability`
- 수치·요금·모델명·버전: 없음
- 코드 예시 요지 (프롬프트 예시 — **원문 그대로**):
  - 데스크톱 "Prepare a decision":
    ```text
    Review the reports and notes in this project, compare the options, and create a one-page decision memo with a recommendation, risks, open questions, and source links.
    ```
  - 데스크톱 "Analyze spreadsheets":
    ```text
    Combine the spreadsheets in this folder, clean inconsistent records, identify the most important trends, and create a concise report with charts and plain-English takeaways.
    ```
  - 데스크톱 "Improve this app":
    ```text
    Inspect this app, identify one high-impact usability improvement, implement it, update the relevant tests, and verify the result on mobile and desktop.
    ```
  - 웹 "Make a decision":
    ```text
    Research whether I should [decision], compare the best options, explain the tradeoffs for my situation, and recommend one with citations.
    ```
  - 웹 "Daily briefing":
    ```text
    Every weekday at 8:00 a.m., review my connected calendar and recent messages, then send me a briefing with today’s priorities, meeting prep, replies I owe, and blockers.
    ```
  - 웹 "Plan an event":
    ```text
    Help me plan my event. Ask me about the occasion, guests, date, location, budget, and anything else you need. Then create a timeline, budget, invitation copy, and checklist, and publish a Site I can use to invite guests and collect RSVPs.
    ```
- 제약·주의사항: "You may also use Codex with an API key. **Some features might not be available**" — API 키 로그인 시 기능 제약이 있음을 명시(→ 자료 12 Pricing의 feature availability 표로 연결).
- 관련 섹션: 설치·첫 실행 장(章). 프롬프트 예시 6종은 "무엇을 시킬 수 있는가"의 구체 예시로 그대로 인용 가능.
- Claude Code 대응 관점 메모: Claude Code의 `npm i -g @anthropic-ai/claude-code` → `claude` 첫 실행에 해당. 다만 Codex는 **"작업 위치(폴더)를 GUI에서 고르는 단계"** 가 명시적 온보딩 스텝으로 존재한다는 점이 다르다 (Claude Code는 cwd가 암묵적).

---

## 자료 3: Use ChatGPT

- URL: https://learn.chatgpt.com/codex/use-chatgpt
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: **Chat / ChatGPT Work / Codex 3분법**이 이 문서군 전체의 개념 축이다.
  - 작업 흐름 4단계: ① 질문·아이디어·메모·파일·과제로 시작 → ② 설명·발전·초안·리서치·분석·창작을 요청 → ③ 필요한 컨텍스트와 도구(파일·웹 검색·프로젝트·플러그인) 추가 → ④ 결과 검토·방향 수정·변경 요청. "You don't need a perfect first prompt or special commands."
  - **모드 선택 표 (원문 그대로):**

    | Choose | When you want to | Examples |
    |---|---|---|
    | Chat | Work through something with ChatGPT | Ask a question, search the web, brainstorm, draft a message, compare options |
    | ChatGPT Work | Define an outcome and get a reviewable result | Create a deck, analyze files, draft a report, build a project plan |
    | Codex | Use developer tools and see technical details | Debug code, run tests, review a PR, implement a feature |

  - **Codex 안의 Quick chat 용도 (원문 목록):** 질문/웹 검색/주제 학습, 낯선 개념을 쉬운 말로 설명, 브레인스토밍, 메시지·개요·콘텐츠 초안, 톤·독자에 맞춘 리라이팅, 메모·텍스트·파일 요약, 선택지 비교·의사결정, 큰 작업 시작 전 요구사항 명확화.
  - **ChatGPT Work vs Codex 데스크톱 상세 비교표 (원문 그대로):**

    | Difference | ChatGPT in Desktop app | Codex in Desktop app |
    |---|---|---|
    | Where to start | Select **ChatGPT**, then switch to **Work** | Select **Codex** in the product selector |
    | Chats you see | See chats started with Chat on web and mobile, plus ChatGPT Work chats | Focus on Codex chats and development projects |
    | Quick chat | Not available | When available, access ChatGPT chats from web and mobile in Codex |
    | Technical detail | Hide technical details like Git or shell commands | See developer details, including diff and review views |
    | Agent communication | Prefers nontechnical language and finished outputs | Can include technical and implementation details |
    | Pull requests pane | Not available when using ChatGPT Work | Available when enabled |

  - 컨텍스트 투입 3수단: **프로젝트**(주제·목표·지속 업무 단위로 채팅·파일·지침 묶음), **파일 첨부**(문서·프레젠테이션·스프레드시트·PDF·이미지·데이터 익스포트 — 요약/비교, 패턴·불일치 발견, 추출·정제·재구성, 새 파일의 원재료), **플러그인**(Google Drive, SharePoint, Salesforce, Gong 등).
  - 결과 검증 체크리스트(원문): 중요 수치·이름·날짜·인용·주장 검증 / 생성 파일을 열어 모든 섹션·탭·슬라이드·페이지 확인 / 올바르고 최신인 원자료를 썼는지 확인 / 누락 정보와 근거 없는 가정 탐색 / 빗나갔으면 표적 수정 요청.
- 명령·플래그·설정 키: `@`(플러그인/스킬 멘션, ChatGPT 측), Quick chat 아이콘
- 수치·요금·모델명·버전: 없음
- 코드 예시 요지 (프롬프트 계단식 개선 3단 — 원문 그대로):
  - Start simple: `Help me plan a 30-minute team meeting about our new customer feedback process.`
  - Add context: `Help me plan a 30-minute team meeting about our new customer feedback process. The audience is a customer support team that hasn't seen the process before. Include five minutes for questions and end with clear next steps.`
  - Choose a format: `Create a 30-minute agenda for a customer support team that hasn't seen our new customer feedback process before. Include five minutes for questions, end with clear next steps, and format it so I can paste it into a calendar invitation.`
  - 후속 지시 예: “Make this shorter.” / “Give me three different approaches.” / “What assumptions are you making?” / “Ask me questions before you continue.”
  - **압박 검증(pressure-test) 질문 6종 (인용 가치 높음):** “What sources did you use for this?” / “Cite the source for each major claim.” / “What assumptions did you make?” / “What information were you unable to access?” / “What would change your recommendation?” / “Check this result against the original files.”
- 제약·주의사항: 원문 경고 — "Legal, financial, medical, security, and other high-stakes decisions require appropriate expert review. Use ChatGPT to support informed judgment, not replace it." 또한 "If ChatGPT couldn't access a source or complete part of the task, ask it to say so plainly. **An explicit gap is easier to address than a confident guess.**" (책의 "AI를 믿는 법" 절에 그대로 인용 가능)
- 관련 섹션: 2장 "Codex를 어떤 모드로 쓸 것인가" 핵심 근거. 압박 검증 질문 6종은 실무 팁 박스로.
- Claude Code 대응 관점 메모: Claude Code에는 Chat/Work/Codex 3분법이 없다 — 단일 에이전트 표면이다. Codex의 이 3분법은 **"비개발자용 산출물 모드(Work)"를 같은 엔진 위에 얹은 제품 전략**이며, Claude Code 사용자에게는 가장 낯선 개념. Quick chat ↔ Claude Code에는 대응 없음(별도 claude.ai 채팅).

---

## 자료 4: Get started with ChatGPT Work

- URL: https://learn.chatgpt.com/codex/get-started-with-work
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: ChatGPT Work = "실제 업무를 ChatGPT에 위임하는 방식". Chat은 답·설명·브레인스토밍·짧은 초안, Work는 명확한 산출물이 있는 과제(브리프·덱·분석·정기 업데이트·워크플로·검토용 파일).
  - Work가 쓸 수 있는 것: 파일, 플러그인, 승인된 도구 → 정보 검색, 완성 파일 생성, 워크플로 실행. 진행 상황을 따라가며 질문에 답하고, 방향을 바꾸고, 중요한 액션을 승인할 수 있다. **데스크톱 앱에서는 로컬 파일·앱·브라우저도 사용 가능.**
  - "If you have used Codex for non-coding work, you can stay in Codex or use ChatGPT Work instead." — 기존 Codex 사용자에게 강제 이전 없음.
  - **로컬 vs 클라우드 선택:** 데스크톱 컴포저의 **Work locally** 컨트롤. **Cloud**가 보이면 ⓐ 앱을 닫거나 컴퓨터를 꺼도 계속 실행되길 원할 때 ⓑ 웹·모바일에서 대화를 이어가고 싶을 때 선택. 로컬 파일·앱이 필요하면 **Work locally** 유지. 클라우드는 시간에 걸쳐 웹사이트를 조사·확인하는 예약 작업에도 유용(실행이 내 컴퓨터의 절전 여부에 의존하지 않음).
  - 첫 과제 3종: 프레젠테이션 생성 / 비교 스프레드시트 생성 / 정기 업데이트 설정.
  - **Work가 적합한 과제 조건 4가지 (원문):** 여러 소스·플러그인·도구·단계를 사용 / 수동으로 하면 의미 있는 시간이 드는 일 / 검토·편집·재사용할 산출물이 나오는 일 / 반복·모니터링·갱신이 필요한 일.
  - 더 나은 결과를 위해 알려줄 것: 원하는 결과, 사용할 소스·플러그인, 지켜야 할 제약, "좋은 결과"의 기준, 검토·승인을 위해 멈춰야 할 지점.
  - 플러그인: 좌측 사이드바 **Plugins** → 라이브러리 → 설치. 프롬프트에서 `@` + 플러그인 이름으로 특정 도구 지목. 연결 대상 예: Slack, Google Drive, SharePoint, email, calendars, CRM, project trackers.
  - **효율 원칙:** "Longer or more complex tasks may use more credits because ChatGPT is doing more on your behalf. **Focus on the value of the completed result, rather than the number of prompts.**" 유용한 경계 예: "use only these sources," "compare the top five options," "stop before sending anything."
  - 유스케이스 컬렉션 7종: productivity-and-collaboration, business-operations, data-science, finance, sales, life-sciences, education
- 명령·플래그·설정 키: `@{플러그인명}`, 컴포저 컨트롤 **Work locally** / **Cloud**
- 수치·요금·모델명·버전: 없음(크레딧 소모 언급만)
- 코드 예시 요지 (프롬프트 — 원문 그대로):
  - 프레젠테이션: `Review the attached source materials and create an eight-slide presentation for [audience]. Focus on the main themes, include supporting evidence, and flag anything that needs human review. Return a draft for my review.`
  - 비교 스프레드시트: `Create a spreadsheet comparing the options for [decision]. Use the attached notes and source materials. Include the most important criteria, score each option, flag risks or missing information, and add a summary tab with a recommendation and next steps.`
  - 정기 업데이트: `Every Monday morning, review new updates from @Slack and @Google Drive for [project]. Refresh the meeting agenda with decisions, blockers, owners, and open questions. Send me a draft before sharing it.`
  - **나쁜 프롬프트 vs 좋은 프롬프트 대비 (책에 그대로 쓸 만한 예시):**
    - Instead of: `Make me a presentation about our customer research.`
    - 좋은 예: `Review the attached interview notes and survey results. Create an eight-slide presentation for the product leadership meeting. Focus on the three most common customer problems, include supporting evidence, separate findings from recommendations, and flag any claims that are not well supported. Use @Google Drive for the source docs. Return a draft for my review before treating it as final.`
- 제약·주의사항: 빠른 질문·짧은 리라이팅·조언만 필요한 결정은 Work가 아니라 Chat을 쓰라고 명시.
- 관련 섹션: "위임의 단위를 어떻게 잡을 것인가" 절. 나쁜/좋은 프롬프트 대비는 프롬프팅 장의 핵심 예시.
- Claude Code 대응 관점 메모: Work locally/Cloud 토글 ↔ Claude Code에는 없음(로컬 전용). Codex의 Cloud는 Claude Code의 원격 실행/백그라운드 에이전트와 개념적으로 가깝지만, **"컴퓨터를 꺼도 계속 돈다"** 는 보장은 Claude Code에 없는 특성.

---

## 자료 5: Import from another agent

- URL: https://learn.chatgpt.com/codex/import
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: **이 책에서 가장 중요한 페이지 중 하나** — Claude Code 사용자를 Codex로 이주시키는 공식 경로다.
  - 다른 에이전트의 지침·설정·스킬·플러그인·프로젝트·최근 작업을 ChatGPT 데스크톱 앱으로 가져오는 임포트 플로우. "**Importing doesn't change or delete your existing agent setup.**" (기존 설정 비파괴)
  - **임포트 절차 5단계 (원문):** ① 데스크톱 앱에서 **Settings > Import** 열기 (Import 섹션이 아직 없으면 **General**에서 **Import other agent setup** 찾기) → ② **Import** 선택 → ③ 가져올 에이전트 선택 후 **Continue** → ④ **Select items to import**에서 항목 선택 후 **Continue** → ⑤ 완료 후 임포트된 프로젝트나 채팅 열어 작업 계속.
  - 동작 원리: 사용자 레벨 설정(내 머신의 파일)과 기존 프로젝트(선택한 저장소·폴더의 파일)를 모두 검사. ① 지원되는 설정·최근 작업 탐지 → ② 선택 항목 임포트 → ③ 기존 에이전트 설정은 그대로 둠 → ④ 임포트된 플러그인·커넥션이 추가 설정을 필요로 하는지 확인 → ⑤ 필요 시 상태 카드 표시.
  - **임포트 대응 표 (원문 그대로 — 책의 마이그레이션 장 핵심 자산):**

    | Imported item | Destination |
    |---|---|
    | Instruction files | [`AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
    | `settings.json` | [`config.toml`](https://learn.chatgpt.com/docs/config-file/config-basic) |
    | Skills | [Skills](https://learn.chatgpt.com/docs/build-skills) |
    | Plugins | Plugins |
    | Existing project folders | Projects using the same folders |
    | Chats from the last 30 days | ChatGPT chats |
    | MCP server configuration | [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp) |
    | Hooks | [Codex hooks](https://learn.chatgpt.com/docs/hooks) |
    | Slash commands | [Skills](https://learn.chatgpt.com/docs/build-skills) |
    | Subagents | [Codex agents](https://learn.chatgpt.com/docs/agent-configuration/subagents) |

  - **임포트 후 반드시 검토할 것 (원문 목록):** 임포트된 스킬·에이전트의 도구 제한/권한 / 커스텀 인증·헤더·환경 변수·트랜스포트를 쓰는 MCP 서버 설정(재로그인 필요할 수 있음) / 임포트 후 동작이 달라질 수 있는 훅 / 수동 후속 조치가 필요한 플러그인·마켓플레이스 / 인자·셸 보간·파일 경로 플레이스홀더에 의존하는 프롬프트 템플릿·커맨드형 프롬프트.
  - 완료 시 좌측 하단에 상태 카드가 뜨고, 주의가 필요한 항목이 있으면 **Finish**를 눌러 설정을 마친다.
- 명령·플래그·설정 키: `AGENTS.md`, `settings.json`, `config.toml`, Settings > Import, Settings > General > "Import other agent setup"
- 수치·요금·모델명·버전: **"Chats from the last 30 days"** (최근 30일 채팅만 임포트)
- 코드 예시 요지: 없음
- 제약·주의사항:
  - **지원 소스 에이전트로 Claude Code와 Claude Cowork가 명시됨** (changelog 2026-06-09 "Added **Import to Codex** flows for importing supported setup from **Claude Code and Claude Cowork**, including during onboarding.")
  - **"Standard Claude Chat data cannot be imported"** — 일반 Claude 채팅 데이터는 임포트 불가.
- 관련 섹션: **마이그레이션 장의 척추.** 매핑 표(10행)를 그대로 옮기고, 각 행마다 "Claude Code에서는 이랬는데 Codex에서는 이렇게 된다"를 붙이는 구성이 유효.
- Claude Code 대응 관점 메모: 완전 대응 — `CLAUDE.md` → `AGENTS.md`, `.claude/settings.json` → `config.toml`, `.claude/skills/` → Skills, `.mcp.json`/MCP 설정 → Codex MCP, `.claude/hooks` → Codex hooks, **슬래시 커맨드(`.claude/commands/`) → Skills로 흡수**(1:1 커맨드 개념이 없음), 서브에이전트(`.claude/agents/`) → Codex agents. 특히 "슬래시 커맨드가 스킬로 접히는" 부분은 두 제품의 확장 모델 차이를 보여주는 핵심 관찰.

---

## 자료 6: Prompting

- URL: https://learn.chatgpt.com/codex/prompting
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: 문서군에서 가장 분량이 큰 실무 가이드(약 23KB). 세 층으로 구성 — ① 프롬프팅 일반 원칙 ② Chat용 예시 ③ ChatGPT Work용 예시 ④ **Codex용 워크플로 8종**(개발자에게 가장 중요).
  - **프롬프트 4요소 (원문):** **Goal**(ChatGPT가 무엇을 해야 하나) / **Context**(어떤 정보·출처가 도움되나) / **Output**(어떤 형식·길이·상세도) / **Boundaries**(무엇이 변하면 안 되나, 무엇을 피하거나 행동 전에 확인해야 하나). "Use only the parts that help. You don't need to fill in every item or follow a required format."
  - 결과부터 서술: "Start with the result, not a detailed list of steps." 프로세스 자체가 중요할 때만 프로세스를 기술하고, 아니면 ChatGPT가 탐색·비교·접근법 조정을 하도록 여지를 남겨라.
  - 컨텍스트 추가 4수단: 파일 첨부(문서·스프레드시트·프레젠테이션·PDF), 이미지 인풋(스크린샷·다이어그램 — "Point out the area that matters instead of relying on the image alone"), 웹 검색, 프로젝트.
  - **경계(Boundaries) 예시 4종 (원문):** "Keep the approved dates and budget figures unchanged." / "Use only the supplied sources. Flag missing information instead of guessing." / "Keep recommendations within the stated budget." / "Prepare the message as a draft. Don't send it." → "Focus on the one or two boundaries that matter most."
  - **Steering vs Queuing (Codex 고유 개념, 인용 가치 높음):**
    - **Steer** — 메시지를 **현재 실행 중인 턴에 추가**. 방향 전환, 빠진 디테일 보충, 새 정보 공유에 사용.
    - **Queue** — 메시지를 **다음 턴을 위해 저장**. 현재 작업이 끝난 뒤 처리되어야 할 후속 작업에 사용.
    - 데스크톱 앱 기본값: **Settings > General > Follow-up behavior**. 대기 중 메시지는 컴포저 위에 표시되며 편집·재정렬·전송·삭제 가능. 기본값을 바꾸지 않고 한 번만 다른 동작을 쓰는 단축키도 해당 설정에 표시됨.
    - **Codex CLI:** Codex가 작업 중일 때 <kbd>Enter</kbd> = 현재 턴 steer, <kbd>Tab</kbd> = 다음 턴으로 queue.
  - **음성 받아쓰기:** 데스크톱 앱에서 컴포저가 보이는 상태로 <kbd>Ctrl</kbd>+<kbd>M</kbd>를 **누르고 있는 동안** 말하면 컴포저에 전사됨(전송 전 검토·편집 가능).
  - **Goal / Plan 모드:** 다단계 과제는 앱 컴포저에 `/plan`을 입력해 Codex가 조사 후 접근법을 제안하게 한다. Goal mode가 가능하면 계획 이후 `/goal`로 지속 목표를 설정.
  - **Codex 워크플로 8종** (각각 "언제 쓰나 / 단계 / 컨텍스트 노트 / 검증"의 4부 구조):
    1. **Explain a codebase** — 온보딩, 서비스 인수인계, 프로토콜·데이터 모델·요청 흐름 파악
    2. **Fix a bug** — 로컬에서 재현 가능한 실패 동작
    3. **Write a test** — 테스트 범위를 정확히 정의하고 싶을 때
    4. **Prototype from a screenshot** — 디자인 목업·스크린샷·UI 레퍼런스를 동작 프로토타입으로
    5. **Iterate on UI with live updates** — "design → tweak → refresh → tweak" 타이트 루프
    6. **Delegate refactor to the cloud** — 로컬 컨텍스트로 접근법 설계 후 긴 구현을 클라우드에 위임
    7. **Do a local code review** — 커밋·PR 전 second pair of eyes
    8. **Review a GitHub pull request** — 브랜치를 로컬로 당기지 않고 리뷰 피드백
  - 원문 Note: "**The IDE extension automatically includes your open files as context. In the CLI, mention paths explicitly, or attach files with `/mention` and `@` path autocomplete.**"
- 명령·플래그·설정 키 (원문 그대로):
  - `/plan`, `/goal`, `/review`, `/mention`, `@`(파일 경로 자동완성 및 플러그인 멘션), `$plan`(스킬 명시 호출)
  - `codex` (대화형 세션 시작)
  - `@codex review` (GitHub PR 코멘트로 리뷰 요청)
  - **Settings > General > Follow-up behavior** (steer/queue 기본값)
  - <kbd>Ctrl</kbd>+<kbd>M</kbd> (음성 받아쓰기), <kbd>Enter</kbd>(steer) / <kbd>Tab</kbd>(queue) — CLI
  - IDE 명령 팔레트: **"Add to Codex Thread"** (선택 영역을 컨텍스트로 추가)
- 수치·요금·모델명·버전: 없음
- 코드 예시 요지 (원문 그대로 — 대표 발췌):
  - 종합 프롬프트(4요소 총집합, 책의 모범 예시로 최적):
    ```text
    Prepare a one-page project status update for Monday's leadership meeting. Use
    the latest project plan in Drive and relevant decisions and updates from the
    project's Slack channel.

    Lead with the decisions leadership needs to make and the next steps. Summarize
    progress, risks, owners, and due dates. Keep approved dates and budget figures
    unchanged. Flag any conflicting or missing information, and don't send or
    publish anything.

    Before you finish, check that every next step has an owner and due date.
    ```
  - 버그 수정 프롬프트(재현 레시피 + 제약 — 이 책의 "좋은 버그 리포트" 예시로 최적):
    ```text
    Bug: Clicking "Save" on the settings screen sometimes shows "Saved" but doesn't persist the change.

    Repro:
    1) Start the app: npm run dev
    2) Go to /settings
    3) Toggle "Enable alerts"
    4) Click Save
    5) Refresh the page: the toggle resets

    Constraints:
    - Do not change the API shape.
    - Keep the fix minimal and add a regression test if feasible.

    Start by reproducing the bug locally, then propose a patch and run checks.
    ```
  - 코드베이스 설명(CLI): `I need to understand the protocol used by this service. Read @foo.ts @schema.ts and explain the schema and request/response flow. Focus on required vs optional fields and backward compatibility rules.`
  - 테스트 작성(CLI): `Add a test for the invert_list function in @transform.ts. Cover the happy path plus edge cases.`
  - 스크린샷 → 프로토타입(CLI, 이미지를 터미널에 드래그해 첨부):
    ```text
    Create a new dashboard based on this image.

    Constraints:
    - Use react, vite, and tailwind. Write the code in typescript.
    - Match spacing, typography, and layout as closely as possible.

    Outputs:
    - A new route/page that renders the UI
    - Any small components needed
    - README.md with instructions to run it locally
    ```
  - 리팩터 계획(`$plan` 스킬 명시 호출):
    ```text
    $plan

    We need to refactor the auth subsystem to:
    - split responsibilities (token parsing vs session loading vs permissions)
    - reduce circular imports
    - improve testability

    Constraints:
    - No user-visible behavior changes
    - Keep public APIs stable
    - Include a step-by-step migration plan
    ```
  - 로컬 리뷰: `/review` / 포커스 지정: `/review Focus on edge cases and security issues`
  - GitHub PR 리뷰: `@codex review` / `@codex review for security vulnerabilities and security concerns`
  - 검증 요청: `After the fix, run lint + the smallest relevant test suite. Report the commands and results.`
- 제약·주의사항:
  - "Codex runs local commands inside a [sandbox] that limits file and network access. If a task needs to cross that boundary, Codex follows your approval policy before continuing."
  - 클라우드 위임 시: "Tasks delegated to the cloud run in isolated environments. **Internet access is off during the agent phase unless you enable it for the environment.**"
  - UI 반복 작업 시 주의: "If you revert or change an edit, tell Codex so it doesn't overwrite your edit when it works on the next prompt."
  - GitHub PR 리뷰 사전 조건: 저장소에 Codex **Code review**를 활성화해야 함.
- 관련 섹션: 프롬프팅 장 전체 + 개발 워크플로 장(8종 워크플로를 그대로 장 구조로 써도 됨). 4요소(Goal/Context/Output/Boundaries)는 책 전체를 관통하는 프레임으로 채택 가능.
- Claude Code 대응 관점 메모: Steering/Queuing은 Claude Code에 **직접 대응 개념이 없다**(Claude Code는 실행 중 입력이 큐잉되는 단일 동작). Codex가 이를 명시적 2모드 + 단축키(Enter/Tab)로 노출한 것은 눈에 띄는 UX 차이. `/plan` ↔ Claude Code의 Plan mode, `/review` ↔ `/review` 스킬, `@` 파일 자동완성 ↔ `@` 파일 참조, `$plan` ↔ `/plan` 스킬 호출(Codex는 스킬 접두사가 `$`, ChatGPT 측은 `@`).

---

## 자료 7: Personalize ChatGPT

- URL: https://learn.chatgpt.com/codex/personalize
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: 개인화 4수단 — 성격(personality), 커스텀 지침, 메모리, Chronicle.
  - **성격:** **Settings > Personalization**에서 **Friendly**, **Pragmatic**, **None** 중 기본 성격 선택. "A personality changes how ChatGPT communicates; **it doesn't change what the model can do.**"
  - **커스텀 지침:** 채팅 전반에 적용할 선호(응답 스타일 등). "In Codex, these personal instructions are stored in your **global `AGENTS.md`** file." 프로젝트·저장소도 각자의 지침을 제공할 수 있음.
  - **메모리(Memories):** 이전 채팅의 유용한 컨텍스트를 이후 작업으로 이월. 안정적 선호, 반복 워크플로, 프로젝트 관례 등. **"Memories are separate from required project guidance. Keep instructions that must always apply in `AGENTS.md` or checked-in project documentation."** (반드시 적용돼야 하는 지침은 메모리가 아니라 AGENTS.md에)
  - **Chronicle:** 최근 **화면 컨텍스트**로 메모리를 보강하는 **opt-in 리서치 프리뷰**. **자격 요건: ChatGPT Pro 구독자, macOS 데스크톱 앱**, **Screen Recording**과 **Accessibility** 권한 필요. 활성화 전 프라이버시·보안·저장·레이트리밋 고려사항을 검토할 것. 언제든 일시중지·비활성화 가능.
- 명령·플래그·설정 키: **Settings > Personalization**, 전역 `AGENTS.md`, `codex://settings` (딥링크 스킴)
- 수치·요금·모델명·버전: Chronicle = ChatGPT **Pro** 전용, **macOS** 전용, 리서치 프리뷰 (2026-08-02 기준)
- 코드 예시 요지: 없음
- 제약·주의사항: Chronicle은 화면을 읽으므로 프라이버시 검토 필수. 성격 설정은 능력이 아니라 커뮤니케이션 방식만 바꾼다는 점 명시.
- 관련 섹션: 설정·개인화 장. "메모리 vs AGENTS.md" 구분은 실무자가 자주 혼동하는 지점이라 별도 박스 권장.
- Claude Code 대응 관점 메모: 전역 `AGENTS.md` ↔ `~/.claude/CLAUDE.md`, 프로젝트 `AGENTS.md` ↔ 프로젝트 `CLAUDE.md`. **Chronicle은 Claude Code에 대응 없음**(화면 관찰 기반 자동 메모리) — Codex 고유. Friendly/Pragmatic 성격 프리셋도 Claude Code에는 대응 없음(output style이 유사하지만 다름).

---

## 자료 8: Skills & Plugins

- URL: https://learn.chatgpt.com/codex/skills-and-plugins
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: 확장 모델의 정의 페이지.
  - **정의 (원문 그대로):**
    - "A **skill** packages instructions and supporting resources for a specific task or workflow."
    - "A **plugin** is an installable bundle that can include skills, connectors, or both. Connectors are backed by **Model Context Protocol (MCP)** servers and can optionally include custom ChatGPT UI."
  - 스킬 구성 3요소: ① ChatGPT/Codex가 언제 적용할지 인식하게 하는 **name과 description** ② 프로세스와 기대 결과를 정의하는 **워크플로 지침** ③ 템플릿·예시·브랜드 가이드·스키마·연결된 도구 등 **보조 리소스**.
  - **호출 문법 차이 (중요):** "ChatGPT supports **`@` mentions**, while Codex supports **`$` mentions** for skills."
  - **스킬 제작 4단계 (원문):** ① 반복하는 하나의 과제를 고른다(시작 재료와 완성 결과를 메모) → ② 워크플로를 서술한다 — **ChatGPT에서는 `@skill-creator`, Codex에서는 `$skill-creator`** 로 시작. 목표·따를 단계·기대 형식·항상 포함/배제할 것을 설명하고 템플릿이나 좋은 예시를 추가 → ③ 초안 검토·시험(현실적인 요청으로 테스트, 단계 누락이나 형식 이탈 시 개선) → ④ 설치·재사용(워크스페이스 설정이 허용하면 팀과 공유).
  - 플러그인: ChatGPT와 Codex가 **하나의 universal plugin directory**를 공유. 설치 후 과제를 직접 서술하거나, 해당 표면의 호출 문법으로 플러그인·번들 스킬을 명시 선택.
  - **스킬 vs 플러그인 선택 기준 (원문):** "Use a **skill** when you need reusable instructions for a focused task. Use a **plugin** when you want an installable package that can combine instructions with connected services or other tools."
  - **Record & Replay:** 워크플로를 시연하면 그것을 재사용 가능한 스킬로 변환.
  - 좋은 첫 스킬 예: 주간 업데이트, 캠페인 브리프, 미팅 후속 조치 — "any task where the steps and format should stay consistent."
- 명령·플래그·설정 키: `@skill-creator` (ChatGPT), `$skill-creator` (Codex), `@{skill}` / `${skill}`
- 수치·요금·모델명·버전: 없음
- 코드 예시 요지: 없음
- 제약·주의사항: 플러그인 가용성은 플랜·워크스페이스 설정·플러그인 자체에 따라 다름.
- 관련 섹션: 확장·자동화 장의 개념 정의. **`@` vs `$` 문법 차이는 Claude Code 사용자가 가장 먼저 헷갈릴 지점**이므로 초반에 명시.
- Claude Code 대응 관점 메모: Skill ↔ Claude Code Skill (거의 동일 개념: name+description으로 자동 트리거, 보조 리소스 번들). Plugin ↔ Claude Code Plugin (스킬·MCP·훅·에이전트 번들 — 구조가 매우 유사). `@skill-creator`/`$skill-creator` ↔ Claude Code의 `skill-creator` 스킬. **핵심 차이: Codex는 스킬 호출 접두사가 표면별로 다르다(`@`/`$`)**; Claude Code는 `/`로 통일.

---

## 자료 9: Permissions (Permission modes)

- URL: https://learn.chatgpt.com/codex/permission-modes
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: 권한 모델의 개념 페이지(상세는 `/codex/sandboxing`, `/codex/permissions`로 분기).
  - 권한은 ChatGPT(데스크톱 앱)와 Codex(CLI·IDE)가 **로컬 액션(파일 편집, 명령 실행, 인터넷 사용)** 을 어떻게 다룰지 통제한다. "The mode you choose sets the boundary for what ChatGPT can do on its own and what needs review."
  - **권장 기본값:** "For most work, start with **Ask for approval**. It lets ChatGPT work within the current workspace and pauses before reaching beyond that boundary."
  - **3개 모드 (원문 명칭):**
    - **Ask for approval** — 항상 사용 가능(기본)
    - **Approve for me** — 설정에서는 **Auto-review**로 표기
    - **Full access**
  - **모드 활성화:** 데스크톱 앱 첫 사용 시 앱 설정에서 모드를 켜야 한다. **Settings > General**의 **Permissions**에서 켠다. "Enabling a mode makes it available in the menu; **it doesn't select the mode or change an existing chat.**"
  - **작동 원리 — 두 통제 장치가 함께 동작 (원문, 이 책의 핵심 개념):**
    - "The **sandbox** defines which files and network resources ChatGPT can access."
    - "**Approvals** determine when ChatGPT pauses before an action or sends the request to automatic review."
    - **"Changing who reviews a request doesn't expand the sandbox.** For example, **Approve for me** keeps the same workspace boundary as **Ask for approval**; it sends requests to cross that boundary to automatic review."
  - 접근 위치: 데스크톱 앱·IDE 확장에서는 컴포저 아래 권한 컨트롤. **CLI에서는 `/permissions` 입력.**
- 명령·플래그·설정 키: `/permissions` (CLI), **Settings > General > Permissions**
- 수치·요금·모델명·버전: 없음
- 코드 예시 요지: 없음
- 제약·주의사항: "The available modes can depend on your local configuration and your organization's requirements. **A mode that isn't allowed appears disabled.**" (조직 정책이 모드를 막을 수 있음)
- 관련 섹션: 보안·권한 장의 도입부. "샌드박스 ≠ 승인" 분리는 반드시 도식(mermaid)으로.
- Claude Code 대응 관점 메모: **Ask for approval** ↔ Claude Code 기본 권한 프롬프트, **Approve for me / Auto-review** ↔ Claude Code에 **직접 대응 없음**(모델이 승인 요청을 심사하는 별도 리뷰어 개념은 Codex 고유), **Full access** ↔ `--dangerously-skip-permissions`. `/permissions` 명령어 이름은 **양쪽이 동일**하다 — 좋은 대비 소재.

---

## 자료 10: What's new (주간 다이제스트)

- URL: https://learn.chatgpt.com/codex/whats-new
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "This weekly digest highlights ChatGPT and Codex features that can change how you work." 버전별 전 항목은 changelog로 안내. **2026년 2월~7월의 제품 진화 서사가 압축돼 있어, 책의 "Codex는 어떻게 여기까지 왔나" 장의 1차 근거로 최적.**
  - **2026-07-20~24:** ChatGPT Voice(GPT-Live 기반) — Chat·Work·Codex에서 음성으로 작업 조율. macOS에서 "Take a look at this"로 appshot 공유(**Screen context** 켠 경우). Plus·Pro·Business·Edu·Enterprise 플랜, 데스크톱 앱 + Remote on iOS. / 로컬 프로젝트 **다중 폴더** 지원 — primary 폴더가 새 채팅·Git 작업·`AGENTS.md`/skills/`config.toml` 자동 탐색을 담당, secondary 폴더는 파일 검색·읽기·편집만.
  - **2026-07-13~17:** 데스크톱에서 Work 대화와 Projects 통합 — 클라우드 Work 대화는 웹·모바일·데스크톱 동기화, 로컬 Work 대화는 컴퓨터에 유지. Codex는 개발 워크플로용 전용 뷰와 별도 히스토리 유지. / **7월 15일 Codex Micro 출시**(OpenAI × Work Louder, 한정 생산). / **GPT-5.6 Sol·Terra·Luna가 Amazon Bedrock에서 GA** — 내장 `amazon-bedrock` 프로바이더를 Bedrock API 키 또는 AWS SDK 자격증명 체인으로 사용(데스크톱 앱의 Work·Codex, Codex CLI, IDE 확장, Codex SDK). / ChatGPT for iOS **1.2026.188**에 Codex 태스크 인라인 시각화 추가.
  - **2026-07-06~10:** ChatGPT Work 본격 도입 — 파일·플러그인에서 컨텍스트를 모으고, 워크플로 전반에 액션을 취하고, 검토 가능한 문서·프레젠테이션·스프레드시트·Sites 생성. **GPT-5.6 기반**, 목표를 단계로 쪼개 **몇 시간 동안** 작업 가능. / GPT-5.6 3종 소개 — "The default **Power** setting uses **Sol with medium reasoning**." / **7월 9일: Codex 앱이 ChatGPT 데스크톱 앱으로 병합**(macOS·Windows). diff 인라인 편집, 사이드 패널 PR 리뷰, GPT-5.6 기반 더 빠른 Computer Use, 멀티 저장소 프로젝트. "The updated desktop app is available **globally on every ChatGPT plan, including Free**."
  - **2026-06-15~19:** **Record & Replay** — macOS에서 워크플로를 시연해 재사용 스킬로 변환. **초기 가용성에서 EEA·영국·스위스 제외, Computer Use 필요.** / **Chat handoff** — 로컬 컴퓨터와 연결된 원격 호스트 간에 채팅과 Git 상태 이동. / iOS Remote에 워크스페이스 파일 브라우저·디렉터리 피커·diff 접기/펼치기·채팅별/교차 MCP 승인 선택 추가. / **Computer Use, Chrome 확장, Memories, Chronicle이 EEA·영국·스위스로 롤아웃 시작 — 단 해당 지역에서 Memories는 기본 꺼짐**, Chronicle은 macOS ChatGPT Pro 구독자용 opt-in 리서치 프리뷰.
  - **2026-06-08~12:** **Browser Developer mode** — Chrome DevTools Protocol 접근으로 네트워크 트래픽·콘솔 출력·런타임 에러·페이지 상태 검사. **Settings > Browser**의 **Developer mode**에서 **Enable full CDP access**. "**Browser use is also up to twice as fast** because CDP and DOM snapshot optimizations reduce browser round trips." / 다른 코딩 에이전트 설정 임포트 플로우 + `/init` 추가. / iOS Remote에서 브랜치 선택·worktree 생성·환경 셋업 스크립트 실행·goal 관리·인라인 리뷰 코멘트.
  - **2026-06-01~05:** **Sites** — ChatGPT가 웹사이트·대시보드·사내 도구·웹앱·게임을 생성·저장·배포·검사, **OpenAI가 호스팅**. / **Amazon Bedrock으로 Codex 사용** 가능. / iOS Remote에 인앱 잠금·후속 동작 설정·diff 줄바꿈·Windows SSH 연결.
  - **2026-05-25~29:** Computer use가 **Windows 데스크톱 앱** 지원 — Computer Use 플러그인 설치 필요, Windows에서는 활성 데스크톱을 쓰며 작업 중 전경을 점유. Remote 연결도 Windows 지원. / iOS Remote에 Spotlight·Shortcuts 진입점, 아카이브 채팅 탐색, `/side`.
  - **2026-05-18~22:** **Appshots** — **양쪽 Command 키를 누르면** 최전면 앱 창의 스크린샷과 가용 텍스트를 Codex로 전송. / **Goal mode가 experimental 딱지를 뗌** — Codex 앱·IDE 확장·CLI에서 "objectives that can take **hours or days**". / **Locked use** — Mac 잠금 후에도 승인된 computer-use 작업 계속. / ChatGPT Business 워크스페이스가 재사용 가능한 플러그인 번들을 멤버와 공유 가능.
  - **2026-05-11~15:** ChatGPT 모바일 앱의 **Remote**가 ChatGPT 데스크톱 앱 실행 중인 Mac에 연결 — "your projects, files, credentials, plugins, skills, and configuration remain available." / **Hooks가 GA**(에이전트 생명주기 핵심 지점에서 커스텀 명령 실행). / ChatGPT Enterprise 관리자가 **Codex access tokens** 활성화 가능(신뢰된 스크립트·스케줄러·프라이빗 CI 러너용).
  - **2026-05-04~08:** **Chrome 확장** — 브라우저를 점유하지 않고 백그라운드에서 탭 전반 병렬 작업. / 받아쓰기 정리 + 이름·파일 경로·코드 심볼용 **커스텀 사전**.
  - **2026-04-20~24:** **GPT-5.5**가 대부분 작업의 권장 모델로 Codex에 도착. / **내장 브라우저에서 Computer Use** — 로컬 개발 서버·파일 기반 페이지를 클릭해 이슈 재현·수정 검증. / **automatic approval review** — 액션 실행 전 리뷰 상태와 리스크 표시.
  - **2026-04-13~17:** 내장 브라우저에 라이브 프리뷰·페이지 코멘트 추가, Computer Use로 macOS 앱 조작. / **Standalone chats**(프로젝트 폴더를 고르지 않고 시작), 채팅 내 예약 작업, PR 컨텍스트, 풍부한 파일 프리뷰, **Memories**.
  - **2026-04-06~10:** 리뷰 경험 — 접이식 인라인 코멘트, 인라인/분리 리뷰 모드, Git·소스 컨텍스트 개선. PR 활동·코멘트·푸시 선택이 앱 안으로 이동.
  - **2026-03-23~27:** **Plugins 출시** — 스킬·커넥터·MCP 서버의 설치형 번들.
  - **2026-03-16~20:** 이전 메시지에서 채팅 **fork** 가능. 초안 작성 중 모델·추론 명령 사용 가능, 활성 스킬이 `@` 메뉴에 노출, **GPT-5.4 mini** 등장(가벼운 작업·서브에이전트용).
  - **2026-03-09~13:** 예약 작업이 로컬 또는 worktree에서 명시적 모델·추론 레벨로 실행. 재사용 템플릿·커스텀 테마. / Codex가 현재 채팅의 **integrated terminal** 출력을 직접 읽음.
  - **2026-03-02~06:** **Codex 앱 Windows 네이티브 출시** — 네이티브 PowerShell·샌드박스 지원, worktree·예약 작업·스킬. WSL도 계속 지원. / **Local ↔ Worktree handoff**. / **GPT-5.4** 도착.
  - **2026-02-09~13:** **GPT-5.3-Codex-Spark** 리서치 프리뷰(실시간 코딩 반복용 초저지연 모델). 채팅 fork, 플로팅 always-on-top 채팅 창.
  - **2026-02-02~06:** **Codex 앱 macOS 출시** — 병렬 프로젝트 채팅, 내장 Git 리뷰, worktree, 스킬, 예약 작업, 음성 받아쓰기. / **Mid-turn steering**과 이미지 외 파일 첨부 — 이후 steering/queuing의 토대.
- 명령·플래그·설정 키: `/init`, `/side`, `amazon-bedrock` 프로바이더, **Settings > Browser > Developer mode > Enable full CDP access**, 양쪽 Command 키(Appshot)
- 수치·요금·모델명·버전 (**fact-check 원장**): GPT-5.6(Sol/Terra/Luna), GPT-5.5, GPT-5.4, GPT-5.4 mini, GPT-5.3-Codex-Spark, GPT-Live / ChatGPT for iOS 1.2026.188 / "up to twice as fast" 브라우저 / "hours or days" Goal mode / 2026-07-09 Codex 앱→ChatGPT 데스크톱 앱 병합 / 2026-07-15 Codex Micro 출시
- 코드 예시 요지 (원문 프롬프트):
  - `Open the Launch project, review its files and recent conversations, and continue the launch plan from the latest Work conversation.`
  - `Create a launch brief from the attached research and campaign template. Show me the plan and flag missing information before you build the final document, then adapt the approved brief into assets for three markets.`
  - `Use @Browser to reproduce the slow checkout. Inspect the network timing and console errors, fix the cause, and verify the result.`
  - `Build a responsive launch dashboard from this project with Sites. Validate it at mobile and desktop sizes, then save a version for review. Do not deploy it until I approve the saved version.`
  - `Use @Computer to open the Windows app, reproduce the export failure, save a diagnostic file, and summarize the exact steps that trigger the problem.`
  - `Use this appshot as the visual reference. Match the selected screen in the app, then open a preview and compare spacing, typography, and color.`
  - `Compare the open product pages, collect the plan limits in a table, cite each source tab, and flag any differences that need a manual check.`
  - `Use @Browser to open the local app, reproduce the checkout failure, fix it, and verify the flow end to end.`
  - `Every weekday, inspect changes from the last 24 hours, find one likely regression, fix it in a worktree, run the smallest relevant tests, and report the evidence.`
- 제약·주의사항: 지역 제한이 반복 등장 — **EEA·영국·스위스**에서 Record & Replay 초기 제외, Computer Use/Chrome 확장/Memories/Chronicle은 6월에야 롤아웃, 해당 지역 Memories 기본 꺼짐. 한국은 명시적 언급 없음(=일반 가용 지역으로 추정되나 **문서에 명시 없음, 추정 금지**).
- 관련 섹션: "Codex 연대기" 장 전체. 각 월별 항목을 그대로 타임라인으로.
- Claude Code 대응 관점 메모: 2026년 상반기 Codex의 진화 방향이 뚜렷하다 — **터미널 도구 → 데스크톱 앱 → GUI·브라우저·컴퓨터 조작·음성·전용 하드웨어**로 확장. Claude Code는 같은 기간 CLI/SDK 중심을 유지했다는 점이 대비 축이 된다.

---

## 자료 11: Models  ★ 모델명 단일 출처(single source of truth)

- URL: https://learn.chatgpt.com/codex/models
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: **이 책의 모델 관련 fact-check 원장.** 다른 페이지(overview, CLI 레퍼런스, codex-for-oss 등)에 모델명 표기 흔들림이 있으므로 **이 페이지를 정전으로 삼는다.**

  ### 표면별 모델 선택 방법 (원문)
  | 표면 | 방법 |
  |---|---|
  | ChatGPT 데스크톱 앱 | 컴포저 아래 모델·추론 컨트롤 |
  | ChatGPT 웹 (ChatGPT Work) | 컴포저 아래 모델·추론 컨트롤 |
  | Codex CLI | 대화형 세션에서 `/model`, 또는 실행 시 `--model` (별칭 `-m`) |
  | Codex IDE 확장 | 컴포저 아래 모델 스위처 |

  ### 권장 모델 3종 — 원문 `ModelDetails` 데이터 전수
  | 모델 ID | 표시명 | 설명(원문) | Capability | Speed |
  |---|---|---|---|---|
  | `gpt-5.6-sol` | **5.6 Sol** | "Flagship GPT-5.6 model with the strongest capability for complex coding, computer use, research, and cybersecurity." | ★5 | ⚡2 |
  | `gpt-5.6-terra` | **5.6 Terra** | "Balanced GPT-5.6 model for everyday work, with performance competitive with GPT-5.5 at a lower cost." | ★4 | ⚡3 |
  | `gpt-5.6-luna` | **5.6 Luna** | "Fast and affordable GPT-5.6 model that delivers strong capability at the lowest cost in the family." | ★3 | ⚡4 |
  | `gpt-5.3-codex-spark` | **5.3 Codex Spark** | "Text-only research preview model optimized for near-instant, real-time coding iteration. **Available to ChatGPT Pro users.**" | ★2 | ⚡5 |

  ### 권장 모델 표면별 가용성 (원문 데이터 그대로)
  | 모델 | 데스크톱 앱 | ChatGPT 웹 | Codex CLI | IDE 확장 | **Codex cloud** | ChatGPT Credits | API Access |
  |---|---|---|---|---|---|---|---|
  | `gpt-5.6-sol` | ✅ | ✅ | ✅ | ✅ | **✅** | ✅ | ✅ |
  | `gpt-5.6-terra` | ✅ | ✅ | ✅ | ✅ | **❌** | ✅ | ✅ |
  | `gpt-5.6-luna` | ✅ | ✅ | ✅ | ✅ | **❌** | ✅ | ✅ |
  | `gpt-5.3-codex-spark` | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |

  > **주목할 사실:** GPT-5.6 3종 중 **Codex cloud에서 쓸 수 있는 것은 Sol 뿐**이다. 그리고 원문은 별도로 "Currently, you can't change the default model for Codex cloud chats."라고 못 박는다 — 클라우드는 모델 선택이 불가하다.

  ### 기타 모델 (ToggleSection "View other models") — 원문 데이터 전수
  | 모델 | 표시명 | 설명(원문) | Capability | Speed | cloud |
  |---|---|---|---|---|---|
  | `gpt-5.5` | 5.5 | "Previous-generation frontier model for complex coding, computer use, knowledge work, and research workflows." | ★4 | ⚡3 | ❌ |
  | `gpt-5.4` | 5.4 | "Frontier model for professional work with strong coding, reasoning, tool use, and agentic workflow capabilities." | ★3 | ⚡3 | ❌ |
  | `gpt-5.4-mini` | 5.4 Mini | "Fast, efficient mini model for responsive coding tasks and subagents." | ★2 | ⚡4 | ❌ |

  (위 3종 모두 데스크톱 앱·웹·CLI·IDE·Credits·API = ✅, cloud만 ❌)

  ### Sol / Terra / Luna 선택 기준 (원문 그대로 — 인용 가치 최상)
  - "Codex offers three GPT-5.6 models: **Sol** for detail and polish, **Terra** as the everyday workhorse, and **Luna** for clear, repeatable work. **If you are unsure, start with Sol.**"
  - **Sol, for complex, open-ended work.** 모호하거나 어렵거나 가치가 큰 과제 — 복잡한 코드 변경, 심층 리서치, 완성도 높은 문서. 좁은 과제에는 "done"의 정의를 줘서 초점을 유지시켜라.
  - **Terra, the pragmatic all-rounder.** Sol의 깊이가 필요 없는 일상 업무. "It is a natural starting point for work you previously gave **GPT-5.5**."
  - **Luna, for clear, repeatable tasks.** 좋은 결과가 무엇인지 이미 아는 구체적·대량 과제 — 추출, 분류, 변환, 구조화 요약.

  ### 추론 강도(reasoning effort)
  - "Use the **lowest** reasoning effort that produces the result you need."
  - **Light**(데스크톱 앱·웹 Work·IDE 확장) 또는 **Low**(CLI) — 빠르고 범위가 명확한 과제
  - **Medium** — 속도와 깊이의 균형, 계획이 더 필요한 과제
  - **High**, **Extra High** — 여러 단계·소스·트레이드오프가 있는 어려운 작업
  - **중요 경고(원문):** "**There is no exact mapping from GPT-5.5 reasoning efforts to GPT-5.6.** Try a familiar task at a lower setting and adjust based on the result."

  ### Max와 Ultra
  - **Max**: 선택한 모델이 **하나의 과제**에 더 오래 추론하게 한다. 가장 어려운 문제, 속도·사용량보다 깊이가 중요할 때. "If you don't see Max in your options, you'll have to enable it in your app settings."
  - **Ultra**: **서브에이전트를 사용**해 복잡한 과제의 각 부분을 병렬 처리. 작업을 의미 있는 조각으로 나눌 수 있을 때 선택. "**Most tasks do not need Max or Ultra.**"
  - Ultra가 데스크톱 앱 모델 슬라이더에 없으면: **Settings > Configuration** → **Ultra in model picker slider** 켜기.
  - 기본값(원문): "Start with the default **Power** setting, which uses **`gpt-5.6-sol` with medium reasoning**. Move toward **Smarter** for deeper reasoning or **Faster** for faster, lower-cost work. Open **Advanced** when you want `gpt-5.6-luna` or a specific model, reasoning effort, or speed."

  ### 폐기·은퇴 (★ fact-check 핵심)
  - **"The `gpt-5.4` and `gpt-5.4-mini` models retire from Codex with ChatGPT sign-in on August 31, 2026."**
    - 대체: `gpt-5.4` → **`gpt-5.6-terra`**, `gpt-5.4-mini` → **`gpt-5.6-luna`**
    - 갱신 대상(원문): workspace defaults, saved model settings, managed configurations, custom agents, and scheduled tasks
    - **"The OpenAI API and Codex authenticated with your own API key aren't affected."**
  - **`gpt-5.2`와 `gpt-5.3-codex`는 ChatGPT 로그인 시 Codex에서 이미 폐기(deprecated)됨.** 스크립트·설정 파일·`codex exec --model` 명령을 갱신할 것.
- 명령·플래그·설정 키 (원문 그대로):
  - `/model` (CLI 대화형 세션에서 모델·추론 강도 전환)
  - `codex --model gpt-5.6` / 별칭 `-m`
  - `codex exec -m gpt-5.6 "Review the current changes"`
  - `config.toml`의 모델 지정:
    ```toml
    model = "gpt-5.6"
    ```
  - **Settings > Configuration > Ultra in model picker slider**
- 수치·요금·모델명·버전 (**2026-08-02 기준, fact-check 원장**):
  - 현행 권장: `gpt-5.6-sol` / `gpt-5.6-terra` / `gpt-5.6-luna`
  - Pro 전용 리서치 프리뷰: `gpt-5.3-codex-spark`
  - 구세대: `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`
  - 폐기 완료: `gpt-5.2`, `gpt-5.3-codex`
  - **은퇴 예정일: 2026년 8월 31일** (`gpt-5.4`, `gpt-5.4-mini`, ChatGPT 로그인 한정)
- 코드 예시 요지: 위 명령·설정 키 참조
- 제약·주의사항:
  - "You can also point Codex at **any model and provider that supports either the Chat Completions or Responses APIs**."
  - **경고(원문):** "**Support for the Chat Completions API is deprecated and will be removed in future releases of Codex.**" (→ Responses API로 이행 필요)
  - "The ChatGPT desktop app, Codex CLI, and IDE extension use the **same `config.toml`** configuration file."
  - Codex cloud는 기본 모델 변경 불가.
- **표기 불일치 판정 (리서치 리드 질의 응답):**
  - `/codex/models`(본 페이지) = `gpt-5.6-sol` / `gpt-5.6-terra` / `gpt-5.6-luna` — **소문자 하이픈 ID가 정전**
  - `/codex/automations` 삽화 캡션의 `5.6 Sol Extended`, 권한 데모의 `5.6 Sol Extended` = **UI 표시 문자열**(모델 ID 아님). 본문의 티어 명칭은 Light/Medium/High/Extra High + Max/Ultra이므로 **"Extended"는 문서 본문에 정의된 티어명이 아니다** — 삽화 전용 문자열로 취급하고 책에 티어명으로 옮기지 말 것.
  - 은퇴 정보 정합성: `/codex/models`(2026-08-31) ↔ `/codex/changelog` 2026-07-31 항목(2026-08-31) ↔ `/codex/automations`(2026-08-31) **3곳 모두 일치**. `/codex/whats-new`에는 은퇴 언급 **없음**(누락이지 모순은 아님).
- 관련 섹션: 모델 선택 장 전체. Sol/Terra/Luna 3분법과 Max/Ultra는 별도 절.
- Claude Code 대응 관점 메모: Sol/Terra/Luna ↔ Opus/Sonnet/Haiku 3티어 구조와 정확히 대응하는 발상. 추론 강도(Light~Extra High) ↔ Claude Code의 thinking budget. **Ultra(서브에이전트 병렬) ↔ Claude Code의 Agent 툴 병렬 실행** — 다만 Codex는 이를 *모델 슬라이더의 한 단계*로 노출하는 반면, Claude Code는 *에이전트 호출*로 노출한다. `/model` 명령어 이름은 양쪽 동일. `config.toml`의 `model = "..."` ↔ `settings.json`의 `model`.

---

## 자료 12: Pricing  ★ 개인 요금제 한도의 유일한 1차 소스

- URL: https://learn.chatgpt.com/codex/pricing
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- **리서치 리드 질의 응답: 이 페이지에는 구체 수치가 있다.** 사용량 한도 표(플랜 5종 × 모델 6종)와 크레딧 요율표(모델 8종 × 토큰 3종)가 **인라인 HTML `<table>`로 완전히 포함**돼 있다. 자리표시자 아님. (`/codex/enterprise/usage-limits`가 수치 없이 위임한다는 동료 보고와 정합)

  ### 대전제 (원문, 페이지 최상단 배너)
  > "**ChatGPT Work and Codex share usage.** ChatGPT Work usage inside ChatGPT uses the same pricing, credits, and usage limits as Codex."

  ### 개인 요금제
  | 플랜 | 가격 | 부제(원문) |
  |---|---|---|
  | **Free** | **$0** /month | "Explore Codex capabilities on quick coding tasks." |
  | **Go** | **$8** /month | "Use Codex for lightweight coding tasks." |
  | **Plus** | **$20** /month | "Power a few focused coding sessions each week." |
  | **Pro** | **From $100** /month | "Choose 5x or 20x higher rate limits than Plus." |
  | **API Key** | (토큰 종량제) | "Great for automation in shared environments like CI." |

  - **Plus 포함 사항(원문):** 웹·CLI·IDE 확장·iOS의 Codex / 자동 코드 리뷰·Slack 연동 등 클라우드 기반 통합 / GPT-5.6 모델 패밀리(Sol, Terra, Luna) / 가볍거나 대량인 작업에 더 높은 한도를 주는 GPT-5.6 Luna / ChatGPT credits로 유연한 사용량 확장 / Plus 플랜의 기타 ChatGPT 기능
  - **Pro 포함 사항(원문, Plus의 모든 것 +):** GPT-5.3-Codex-Spark(리서치 프리뷰) 접근 / **Plus 대비 5배 또는 20배 많은 Codex 사용량** / **$200/month 티어에서 ChatGPT Voice 무제한**(단 태스크는 여전히 Codex 사용량 예산 차감) / Pro 플랜의 기타 ChatGPT 기능
  - **API Key(원문):** CLI·SDK·IDE 확장의 Codex / **클라우드 기반 기능 없음**(GitHub 코드 리뷰, Slack 등) / 모델 가용성은 키가 접근 가능한 API 모델을 따름 / Codex가 쓴 토큰만큼만 과금

  ### 비즈니스/엔터프라이즈 요금제
  | 플랜 | 가격 | 비고 |
  |---|---|---|
  | **Business** | **$20** / user / month* | *2인 이상, 연간 결제 기준. **월간 결제 시 사용자당 월 $25.** |
  | **Enterprise & Edu** | 영업 문의 | Business의 모든 것 + 추가 |

  - **Business(원문):** 데스크톱·모바일 앱에서 ChatGPT와 Codex 접근 / **클라우드 채팅을 더 빠르게 실행하는 더 큰 가상 머신** / ChatGPT credits로 사용량 확장 / SAML SSO·MFA 등 필수 관리 기능을 갖춘 안전한 전용 워크스페이스 / **기본적으로 비즈니스 데이터로 학습하지 않음**
  - **Enterprise & Edu(원문):** 우선 요청 처리 / SCIM, EKM, 사용자 분석, 도메인 검증, RBAC 등 엔터프라이즈급 보안·통제 / Compliance API를 통한 감사 로그·사용량 모니터링 / 데이터 보존·데이터 레지던시 통제

  ### 사용량 한도 표 — **로컬 메시지 / 5시간** (원문 수치 전수)
  | 모델 | Plus | Pro 5x | Pro 20x | Business | API Key |
  |---|---|---|---|---|---|
  | GPT-5.6 Sol | **10-100** | **50-500** | **200-2,000** | **10-100** | Usage-based |
  | GPT-5.6 Terra | **25-200** | **125-1,000** | **500-4,000** | **25-200** | Usage-based |
  | GPT-5.6 Luna | **250-2,000** | **1,250-10,000** | **5,000-40,000** | **250-2,000** | Usage-based |
  | GPT-5.5 | **15-80** | **75-400** | **300-1600** | **15-80** | Usage-based |
  | GPT-5.4 | **20-100** | **100-500** | **400-2000** | **20-100** | Usage-based |
  | GPT-5.4 mini | **60-350** | **300-1750** | **1200-7000** | **60-350** | Usage-based |

  - **Cloud chats / 5h 열과 Code Reviews / 5h 열은 전 플랜·전 모델이 "Not available"로 표기돼 있다** (원문 그대로. 표의 현재 상태를 그대로 기록 — 해석·보정 금지).
  - **각주 (원문 그대로):**
    - "*The usage limits for local messages and cloud chats share a **five-hour window**. Additional weekly limits may apply."
    - "For Enterprise/Edu users with flexible pricing, there are no fixed rate limits - usage scales with credits"
    - "Enterprise and Edu plans without flexible pricing have the same per-seat usage limits as Plus for most features"
  - **Business 한도 = Plus 한도와 동일 수치**라는 점이 표에서 확인된다.

  ### 크레딧 요율표 — **100만 토큰당 크레딧** (원문 수치 전수)
  | 모델 | Input Tokens | Cached input tokens | Output Tokens |
  |---|---|---|---|
  | GPT-5.6 Sol | **125 credits** | **12.5 credits** | **750 credits** |
  | GPT-5.6 Terra | **50 credits** | **5 credits** | **300 credits** |
  | GPT-5.6 Luna | **5 credits** | **0.5 credits** | **30 credits** |
  | GPT-5.5 | **125 credits** | **12.50 credits** | **750 credits** |
  | GPT-5.4 | **62.50 credits** | **6.250 credits** | **375 credits** |
  | GPT-5.4 mini | **18.75 credits** | **1.875 credits** | **113 credits** |
  | GPT-5.3-Codex-Spark | research preview | research preview | research preview |
  | GPT-Image-2 (image) | **200 credits** | **50 credits** | **750 credits** |
  | GPT-Image-2 (text) | **125 credits** | **31.25 credits** | **250 credits** |

  - **표 각주(원문):** "**GPT-5.6 usage averages 5-40 credits per message.**" / "Fast mode consumes credits at a higher rate for supported models."
  - 파생 사실: Sol : Terra : Luna 입력 토큰 크레딧 비 = **125 : 50 : 5 = 25 : 10 : 1**. 출력은 **750 : 300 : 30 = 25 : 10 : 1**. 캐시 입력은 정가의 **1/10**.

  ### ChatGPT Voice 한도 (데스크톱)
  - "ChatGPT Voice on desktop uses a **separate, plan-dependent allowance measured in rolling five-hour windows.** Tasks started through Voice use your existing Codex usage budget."
  - **아키텍처(원문):** "ChatGPT Voice in Desktop uses a **duplex model: GPT-Live manages the live conversation, while GPT-5.6 Terra starts and coordinates tasks in the app.**"
  - **플랜별 음성 허용량 (원문 수치):**
    | 플랜 | 허용량 |
    |---|---|
    | **Plus** | 약 **15–30분** |
    | **Pro 5x ($100/month)** | 약 **1–2.5시간** |
    | **Pro 20x ($200/month)** | **무제한** |
    | **Business** | 약 **45분** |
    | **Enterprise / Edu (legacy)** | 약 **45분** |
  - "Unlimited voice access **doesn't** make Codex tasks unlimited."
  - **크레딧 기반/종량 과금 워크스페이스(Business·Edu·Enterprise): Desktop voice는 분당 약 6 크레딧.**
  - **"ChatGPT Voice in Desktop is not available via API Key currently."**

  ### 기타 수치·규칙
  - **이미지 생성:** 로컬 메시지·클라우드 채팅과 **동일한 일반 사용량 한도**에 계산됨. 이미지 생성이 없는 유사 턴 대비 **평균 3~5배 빠르게** 포함 한도를 소진(이미지 품질·크기에 따라 다름). 포함 한도 소진 후에는 크레딧 차감. **Free 플랜에서는 이미지 생성 불가.** API 키 사용 시에는 ChatGPT 포함 한도가 아니라 API 요금 적용.
  - **한도 초과 시:** "If you reach your usage limits during an active turn, **the agent will be able to continue working on that turn**, subject to fair use limits." Plus·Pro는 추가 크레딧 구매 가능(플랜 업그레이드 불필요). flexible pricing의 Business·Edu·Enterprise는 워크스페이스 크레딧 추가 구매 가능. 모든 사용자는 API 키로 추가 로컬 채팅 실행 가능(표준 API 요금).
  - **한도 확인:** 사용량 대시보드 `https://chatgpt.com/codex/settings/usage`. **Codex CLI 세션 중에는 `/status`.**
  - **Code Review 사용량의 정의(원문):** "Code Review usage applies **only when Codex runs reviews through GitHub**—for example, when you tag `@Codex` for review in a pull request or enable automatic reviews on your repository. **Reviews run locally or outside of GitHub count toward your general usage limits.**"
  - **다른 기능과의 한도 공유:** "Usage limits are shared with other agentic features once pricing for those features is effective. This currently includes **ChatGPT for Excel** on Plus and Pro."
  - **Spark 별도 한도:** "GPT-5.3-Codex-Spark is in research preview for ChatGPT Pro users only, and **isn't available in the API at launch**. Because it runs on **specialized low-latency hardware**, usage is governed by a **separate usage limit that may adjust based on demand**."
  - **Sites 비용:** "Sites is **included with eligible ChatGPT plans during public beta.**"

  ### 사용량 절약 팁 6종 (원문 그대로 — 실무 박스로 최적)
  1. **Control the size of your prompts.** 지시는 정확하게 하되 불필요한 컨텍스트는 제거
  2. **Limit source material.** 관련 파일만 제공하고 가능하면 소스나 기간을 좁힐 것
  3. **Match the output to the need.** 독자·형식·길이를 정의하고 필수 작업과 선택적 개선을 분리
  4. **Reduce the size of your AGENTS.md.** 큰 프로젝트라면 **저장소 안에 AGENTS.md를 중첩(nesting)** 해 주입되는 컨텍스트 양을 통제
  5. **Limit the number of MCP servers you use.** "Every MCP server adds more context to your messages and uses more of your limit. **Disable MCP servers when you don't need them.**"
  6. **Switch to a smaller model for routine tasks.** GPT-5.6 Terra나 Luna로 전환하면 로컬 메시지 한도를 늘릴 수 있음

  ### 초대(referral) 프로그램
  - 프로필 메뉴(앱 좌하단)에서 **Invite a friend**(개인 플랜) / **Invite a coworker**(Business 워크스페이스).
  - **"From June 11 through June 24, 2026, eligible Plus and Pro users can invite up to three friends."** 수신자가 첫 Codex 메시지를 보내면 양쪽 모두 **banked rate-limit reset**을 받음. **Banked rate-limit resets are usable for 30 days after they're granted.**
  - **"Referrals aren't currently available for ChatGPT Enterprise."**

  ### 기능 가용성 매트릭스 (원문 `CodexPlanFeatureMatrix` 데이터 — 주요 항목 발췌; 범례 ✅=available, ⛔=unavailable, △=limited)
  | 기능 | Plus | Pro | Business | Enterprise/Edu | API Key |
  |---|---|---|---|---|---|
  | Codex cloud | ✅ | ✅ | ✅ | ✅ | ⛔ |
  | ChatGPT Work on the web | ✅ | ✅ | ✅ | ✅ | ⛔ |
  | ChatGPT 데스크톱 앱(로컬 채팅) | ✅ | ✅ | ✅ | ✅ | ✅ |
  | Codex CLI / IDE 확장 | ✅ | ✅ | ✅ | ✅ | ✅ |
  | Codex SDK, `codex exec`, 스크립팅 | ✅ | ✅ | ✅ | ✅ | ✅ |
  | **Codex access tokens**(신뢰된 자동화) | ⛔ | ⛔ | ✅ | ✅ | ⛔ |
  | ChatGPT for Excel | ✅ | ✅ | ✅ | ✅ | ⛔ |
  | GPT-5.6 / Fast mode / 웹 검색 | ✅ | ✅ | ✅ | ✅ | ✅ |
  | **Codex-Spark 리서치 프리뷰** | ⛔ | **✅** | ⛔ | ⛔ | ⛔ |
  | 이미지 생성·편집 | ✅ | ✅ | ✅ | ✅ | ✅ |
  | 음성 받아쓰기 / **ChatGPT Voice** | ✅ | ✅ | ✅ | ✅ | ⛔ |
  | `/review` 로컬 코드 리뷰 / Auto-review / 샌드박스·권한 통제 | ✅ | ✅ | ✅ | ✅ | ✅ |
  | 예약 작업 / worktree·Git 도구 / 로컬 환경 | ✅ | ✅ | ✅ | ✅ | ✅ |
  | **Appshots** | ✅ | ✅ | ✅ | **⛔** | ✅ |
  | 내장 브라우저 프리뷰·코멘트 | ✅ | ✅ | ✅ | ✅ | ✅ |
  | 브라우저 Computer Use / Chrome 제어 / **Computer Use**(지역 제한) / **Record & Replay**(지역 제한) | △ | △ | △ | △ | △ |
  | SSH 원격 연결 | ✅ | ✅ | ✅ | ✅ | ✅ |
  | 모바일 원격 제어 / ChatGPT 웹 브라우저 | ✅ | ✅ | ✅ | ✅ | ⛔ |
  | `AGENTS.md` 커스텀 지침 / Skills / MCP / 서브에이전트·커스텀 에이전트 | ✅ | ✅ | ✅ | ✅ | ✅ |
  | **Plugins** | ✅ | ✅ | ✅ | ✅ | **△**(일부 1st-party 플러그인 불가) |
  | 플러그인 공유 / Connectors | ✅ | ✅ | ✅ | ✅ | ⛔ |
  | **Memories** | △ | △ | △ | △ | △ |
  | **Chronicle** | ⛔ | **△** | ⛔ | ⛔ | ⛔ |
  | 클라우드 채팅·환경·인터넷 통제 | ✅ | ✅ | ✅ | ✅ | ⛔ |
  | **Sites** | **⛔** | **⛔** | **✅** | **✅** | ⛔ |
  | GitHub `@codex` 위임 / GitHub PR 리뷰 / Slack / Linear | ✅ | ✅ | ✅ | ✅ | ⛔ |
  | SAML SSO·MFA·워크스페이스 관리 | ⛔ | ⛔ | ✅ | ✅ | ⛔ |
  | `requirements.toml` 관리 설정 | ✅ | ✅ | ✅ | ✅ | ✅ |
  | 클라우드 관리 설정 정책 | ⛔ | ⛔ | ✅ | ✅ | ⛔ |
  | **RBAC·커스텀 역할 / SCIM·EKM·도메인 검증 / 보존·레지던시 / 분석 대시보드 / 분석 API / Compliance API·감사 로그 / Codex Security** | ⛔ | ⛔ | ⛔ | **✅** | ⛔ |
  | API·비즈니스 데이터 기본 미학습 | ⛔ | ⛔ | ✅ | ✅ | ✅ |

  - 각주: "\* Feature is currently limited to only specific regions." / "† Some first party plugins are not available."
- 명령·플래그·설정 키: `/status` (CLI에서 잔여 한도 확인), `@Codex`(GitHub PR 리뷰 태그), 사용량 대시보드 `chatgpt.com/codex/settings/usage`
- 수치·요금·모델명·버전: **위 표 전체가 원장.** 반드시 "2026-08-02 기준"으로 못 박아 인용할 것.
- 코드 예시 요지: 없음
- 제약·주의사항:
  - 원문 경고: "Tasks that look similar can consume different amounts of your allowance. **Model choice, context, reasoning, tool use, retrieval, and caching all affect usage, so prompt length alone isn't a reliable estimate.**" (책에서 "요금 계산 공식"을 제시하려는 유혹을 막는 근거)
  - "A small subset of Enterprise customers should continue using the **legacy rate card**."
  - Speed 설정(Fast mode)은 모든 해당 모델의 크레딧 소모를 증가시킴.
- 관련 섹션: 요금·사용량 장 전체. 사용량 절약 팁 6종은 실무 체크리스트로.
- Claude Code 대응 관점 메모: 크레딧 단위 노출은 Codex 고유(Claude Code는 플랜 한도/API 과금이 이원화). **"AGENTS.md를 중첩해 컨텍스트 주입량을 줄여라"** 는 조언은 CLAUDE.md 중첩과 정확히 동형 — 좋은 대비 소재. "MCP 서버를 안 쓸 때 꺼라"도 Claude Code 실무와 동일한 교훈.

---

## 자료 13: Glossary

- URL: https://learn.chatgpt.com/codex/glossary
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: 앱·CLI·IDE 확장·클라우드·SDK·연동 전반의 **용어 사전 약 100항목**. 각 항목은 `key`(용어), `appliesTo`(적용 표면), `description`(정의), `href`(상세 링크)를 갖는다. **책의 용어 통일 기준으로 삼기에 최적** — 특히 한국어 번역어 결정 시 원문 정의를 근거로 삼을 것.

  ### 핵심 개념 (원문 정의 그대로)
  | 용어 | 적용 표면 | 정의 |
  |---|---|---|
  | **Agent** | 데스크톱 앱, CLI, IDE, Cloud | "The Codex agent that reasons over context, uses tools, and completes a task." |
  | **Codex** | 데스크톱 앱, CLI, IDE, Web, Cloud, SDK | "OpenAI's coding agent for software development tasks." |
  | **ChatGPT Work** | 데스크톱 앱, Web | "The agent in ChatGPT for research, analysis, and creating documents, presentations, spreadsheets, and other finished work." |
  | **Chat** | 전 표면 | "A saved space for exchanging messages with ChatGPT or Codex, including shared context, results, and actions. **Quick chat starts a ChatGPT chat from Codex.**" |
  | **Conversation** | 전 표면 | "The ongoing exchange of messages and shared context between a person and ChatGPT or Codex within a chat." |
  | **Task** | 전 표면 | "A defined outcome ChatGPT or Codex works toward, such as fixing a bug, creating a document, or researching a topic." |
  | **Turn** | 전 표면 | "One exchange in a chat, usually a user prompt plus the agent's response and actions." |
  | **Thread** | App-server, SDK | "A **technical object** in Codex app-server APIs that contains turns and stored conversation history." |
  | **Project** | 데스크톱 앱 | "A group of related chats and shared sources, or a local folder used for file-based work." |
  | **Context** | 데스크톱 앱, CLI, IDE, Cloud, SDK | "Information Codex can use while working, such as files, prior messages, tool output, and instructions." |
  | **Context window** | 전 표면 | "The maximum amount of information the model can consider at once." |
  | **Compaction** | 전 표면 | "Summarizing older context so long-running work can continue." |
  | **Plan** | 전 표면 | "Codex's proposed or tracked steps for completing a task." |
  | **Prompt** | 전 표면 | "A question, instruction, or goal sent to ChatGPT or Codex." |

  ### 설정·확장
  | 용어 | 정의 |
  |---|---|
  | **AGENTS.md** | "Repository or user guidance file that gives Codex persistent instructions." |
  | **config.toml** | "Local Codex configuration files." |
  | **requirements.toml** | "Admin-enforced requirements file for managed Codex setups." (Enterprise) |
  | **Profile** | "Named configuration preset for Codex." (CLI, IDE) |
  | **Skill** | "Reusable workflow package with instructions and optional scripts or references." |
  | **Skill invocation** | "Explicit or implicit activation of a skill." |
  | **Progressive disclosure** | "Loading skill details only when needed to preserve context." |
  | **Plugin** | "An installable bundle of capabilities, such as skills, connectors, and tools, distributed through the **universal directory shared by ChatGPT and Codex**." |
  | **Plugin manifest** | "Plugin metadata file that identifies a plugin and points to bundled skills, connector mappings, MCP servers, hooks, and metadata." |
  | **Connector** | "A component of a plugin that connects ChatGPT or Codex to data and actions in an external service." |
  | **MCP** | "**Model Context Protocol**, a standard for connecting Codex to external tools and context." |
  | **MCP server / MCP tool / MCP resource** | 각각 "External tool or context provider exposed through MCP." / "Action exposed by an MCP server that Codex can call during a task." / "Readable context exposed by an MCP server for Codex to inspect." |
  | **STDIO MCP server** | "MCP server launched as a local process by a configured command and arguments." |
  | **Streamable HTTP MCP server** | "MCP server reached over HTTP, optionally with bearer token or OAuth authentication." |
  | **Hook** | "A lifecycle handler that runs when a Codex event matches, such as tool use, permission requests, or when a turn stops." |
  | **Hook event** | "Lifecycle point where configured hook handlers can run." |
  | **Subagent** | "Specialized child agent spawned to work on part of a task." |
  | **Subagent workflow** | "Workflow where Codex runs delegated agents in parallel and combines their results." |
  | **Custom agent** | "User-defined agent role with its own instructions and settings." |
  | **Slash command** | "Command entered with a leading slash to control or inspect a **Codex CLI** session." (CLI 한정으로 정의됨) |
  | **Memories** | "**Locally stored** context Codex can reuse across sessions." |
  | **Chronicle** | "Opt-in feature that builds memories from recent screen context." |

  ### 권한·샌드박스 (책의 보안 장 용어 기준)
  | 용어 | 정의 |
  |---|---|
  | **Action** | "An operation performed by a person, ChatGPT, or Codex, such as editing a file, running a command, or using a connected service." |
  | **Approval policy** | "Rules for when Codex must ask before taking an action." |
  | **Approval request** | "Codex asking to allow a restricted action." |
  | **Automatic approval review** | "**Model-based review** of eligible approval requests before they proceed." |
  | **Sandbox** | "Enforced boundary limiting what Codex commands can access or modify." |
  | **Sandbox mode** | "Configuration that defines Codex's filesystem and network limits." |
  | **Sandbox preset** | "SDK shorthand for common sandbox policies such as read-only, workspace-write, or full access." |
  | **Read-only mode** | "Mode where Codex can inspect but not modify without approval." |
  | **Full access** | "Mode where Codex runs without normal sandbox restrictions." |
  | **Writable roots** | "Directories Codex is allowed to modify." |
  | **Permission profile** | "Named **least-privilege** policy that combines filesystem and network rules for local command execution." |
  | **Filesystem permission** | "Permission profile rule that grants or denies read and write access to paths." |
  | **Deny-read rule** | "Filesystem permission rule that prevents Codex from reading sensitive paths or glob matches." |
  | **Rules** | "Policies that allow, prompt for, or deny command prefixes or permission exceptions." |
  | **Prefix rule** | "Command-rule pattern that allows, prompts for, or forbids matching command prefixes." |
  | **Network access / Network policy** | "Permission for commands or environments to reach the internet." / "Domain-based allow and deny rules that constrain sandboxed outbound network traffic." |

  ### Git·리뷰
  | 용어 | 정의 |
  |---|---|
  | **Git worktree** | "A second checkout of the same repository for parallel branch work." |
  | **Codex-managed worktree** | "A temporary worktree Codex creates and manages for a chat." |
  | **Permanent worktree** | "A long-lived worktree kept as its own project." |
  | **Worktree** | "Mode where Codex isolates changes in a separate Git worktree." |
  | **Handoff** | "Moving a chat and its work between Local and Worktree." |
  | **Diff / Hunk / Inline comment** | "Set of Git file changes shown for inspection, comments, staging, or reverting." / "Contiguous section of a diff that can be staged, unstaged, or reverted independently." / "Line-specific feedback attached to a diff." |
  | **Review pane** | "Desktop app view for inspecting diffs, comments, and Git changes." |
  | **Pull request review** | "Codex review of changes or feedback on a pull request." |

  ### 클라우드·환경
  | 용어 | 정의 |
  |---|---|
  | **Cloud** | "Mode where Codex works remotely in an **OpenAI-managed** environment." |
  | **Cloud environment / Cloud chat** | "Configured container setup used for Codex cloud chats." / "A Codex chat that runs remotely in a cloud environment." |
  | **Universal image** | "Default Codex cloud container image with common tools preinstalled." |
  | **Container cache / Maintenance script** | "Saved cloud container state reused to speed up future cloud chats." / "Optional script run when a cached cloud container resumes." |
  | **Setup script** | "Script run before the agent starts to install dependencies or prepare tools." |
  | **Secret** | "Encrypted value **available to setup scripts but removed before the agent phase**." |
  | **Environment variable** | "Runtime configuration value available during task execution." |
  | **Domain allowlist** | "Set of domains Codex cloud can reach when agent internet access is enabled." |
  | **Environment (local)** | "Desktop app configuration that tells Codex how to set up worktrees for a project." |
  | **Local / Local chat** | "Mode where Codex works on the user's computer." / "A ChatGPT or Codex chat that runs on the user's machine." |

  ### 실행·자동화
  | 용어 | 정의 |
  |---|---|
  | **Scheduled task** | "A prompt ChatGPT runs at a future time or on a recurring schedule, with its own settings and run history." |
  | **Scheduled run** | "One execution of a scheduled task, including its status and any resulting findings." |
  | **Standalone scheduled task** | "Scheduled task whose runs each start a new chat and report findings in Triage." |
  | **Scheduled task in a chat** | "A scheduled task that uses an existing chat's context and returns each run's results to that chat." |
  | **Heartbeat** | "A recurring scheduled task that returns ChatGPT to the same chat." |
  | **Schedule / Finding** | "The timing rule for a scheduled task." / "A notable result or issue surfaced by a scheduled task." |
  | **codex exec** | "CLI command for running Codex **non-interactively** from scripts or CI." |
  | **Non-interactive mode** | "CLI mode for running Codex from scripts or CI." |
  | **Ephemeral session** | "Non-interactive run that **skips saving session state** after it completes." |
  | **Output schema** | "**JSON Schema** passed to `codex exec` to constrain the final response." |
  | **Fast mode** | "Speed setting that makes supported models respond faster **at a higher credit cost**." (CLI, IDE) |
  | **Reasoning effort** | "Setting that controls how much reasoning budget a model uses." |
  | **Live web search / Web search cache** | "Real-time web lookup for current information." / "**Pre-indexed** search results Codex can use without live browsing." |

  ### 표면·인프라
  | 용어 | 정의 |
  |---|---|
  | **Codex app-server** | "**Local JSON-RPC server** for embedding Codex threads, turns, approvals, history, and streamed events in custom clients." |
  | **Codex SDK** | "Programmatic interface for building Codex-powered workflows or integrations." |
  | **Thread fork** | "New thread branched from the stored history of an existing thread." |
  | **Remote connection / Connected host** | "Connection that lets you access ChatGPT or Codex chats on another device through a connected host." / "Computer or development environment that provides files, tools, and shell access for ChatGPT or Codex chats opened through Remote." |
  | **Appshot** | "Snapshot of the frontmost app window sent to a ChatGPT or Codex chat." |
  | **Computer Use** | "Desktop capability that lets ChatGPT interact with other applications through the UI." |
  | **Computer Use in the browser** | "Capability that lets ChatGPT operate the built-in browser directly." |
  | **ChatGPT sign-in / API key sign-in / Auth cache** | "Authentication using a ChatGPT account and workspace permissions." / "Authentication using an OpenAI API key." / "Locally stored login credentials reused by Codex." |

  ### 엔터프라이즈
  | 용어 | 정의 |
  |---|---|
  | **Managed configuration** | "Organization-controlled Codex defaults and restrictions." |
  | **RBAC** | "Role-based access control for workspace permissions." |
  | **MDM** | "Mobile device management tooling for distributing device profiles and managed Codex settings." |
  | **Analytics dashboard** | "Admin hub for ChatGPT workspace adoption and Codex-focused reporting." |
  | **Compliance API** | "API for exporting supported ChatGPT workspace records and audit metadata." |
- 명령·플래그·설정 키: 위 표의 `AGENTS.md`, `config.toml`, `requirements.toml`, `codex exec`
- 수치·요금·모델명·버전: 없음
- 코드 예시 요지: 없음
- 제약·주의사항: 용어 사전의 링크 경로는 `/codex/...` 형태로 기재돼 있으나 실제로는 `/docs/...`로 리다이렉트된다.
- 관련 섹션: 책 말미 용어집(부록). 본문 번역어 통일의 기준.
- Claude Code 대응 관점 메모: 용어가 겹치는 것이 많다(Skill, Plugin, MCP, Hook, Subagent, Sandbox, Context window, Compaction). **결정적 차이는 "Task/Chat/Thread/Turn"의 4층 구분** — Codex는 Thread를 "app-server API의 기술 객체"로 따로 정의해 사용자 개념(Chat)과 분리했다. Claude Code에는 이 분리가 없다. 또 **Slash command를 "CLI 세션 전용"으로 정의**한 점이 Claude Code(전 표면 슬래시 커맨드)와 다르다.

---

## 자료 14: ChatGPT desktop app

- URL: https://learn.chatgpt.com/codex/app
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: 데스크톱 앱 = "Your command center for complex work". 병렬 프로젝트 실행, 파일 작업, 컴퓨터 사용, 장기 작업 유지를 하나의 데스크톱 워크스페이스에서.
  - **왜 데스크톱 앱인가 (원문 3항):**
    - "**Keep every chat in view:** Move between projects and long-running work without losing context."
    - "**Create and inspect real outputs:** Open documents, spreadsheets, images, and other files in the same workspace."
    - "**Work across your tools:** Use the browser, desktop apps, and plugins, or schedule a task inside a chat."
  - **시작 4단계:** ① `https://chatgpt.com/download/` 에서 Windows/macOS용 다운로드 → ② 앱 열고 ChatGPT 계정 로그인 → ③ 작업 위치 선택(채팅/프로젝트/폴더) → ④ 첫 메시지. ChatGPT 또는 Codex 선택; ChatGPT에서는 컴포저 위 토글로 Chat/Work 선택, Codex에서는 New chat으로 시작, 가벼운 질문은 New chat에 마우스 올려 Quick chat 아이콘.
  - **앱으로 할 수 있는 일 (use-case 링크 5종, 원문):** 하루를 집중 업무 브리프로 시작(`/use-cases/daily-work-brief` — 캘린더·메시지·이메일·프로젝트 컨텍스트 전반의 우선순위 검토) / 파일 분석 및 인터랙티브 시각화 생성(`/use-cases/analyze-data-export`) / 흩어진 컨텍스트를 완성된 PRD로(`/use-cases/draft-prds-from-sources`) / 지저분한 데이터 정제(`/use-cases/clean-messy-data` — "Turn a messy CSV or spreadsheet into a clean copy **without changing the original**") / 피드백을 액션으로(`/use-cases/feedback-synthesis`)
  - **데스크톱 앱을 쓸 때 (원문 4항):** 여러 프로젝트를 조율할 때 / 파일을 만들고 검토할 때 / 브라우저와 컴퓨터를 쓸 때 / 반복 작업을 예약할 때
- 명령·플래그·설정 키: 없음(GUI). 다운로드 URL `https://chatgpt.com/download/`
- 수치·요금·모델명·버전: 없음. (단 `/codex/whats-new` 기준 데스크톱 앱은 **Free 포함 전 플랜에 전역 제공**)
- 코드 예시 요지: 없음
- 제약·주의사항: Windows와 macOS만 지원(Linux 언급 없음).
- 관련 섹션: 제품 표면 비교 장. Claude Code 사용자에게 "왜 GUI 앱이 필요한가"를 설득하는 근거 3항.
- Claude Code 대응 관점 메모: **Claude Code에는 대응하는 1급 데스크톱 앱이 없다.** 이것이 두 제품의 가장 큰 표면 차이. "파일 산출물을 같은 워크스페이스에서 열어 검토한다"는 것은 CLI로는 불가능한 경험.

---

## 자료 15: ChatGPT on the web

- URL: https://learn.chatgpt.com/codex/web
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: 웹 표면 = "Research, analyze, and create in your browser". Chat과 ChatGPT Work를 포함.
  - **왜 웹인가 (원문 3항):** 명확한 과제로 시작(목표와 컨텍스트를 주고 후속 메시지로 다듬기) / 파일과 도구 사용(파일·프로젝트·플러그인) / 공유 가능한 파일 생성(문서·프레젠테이션·스프레드시트 등)
  - **시작 4단계:** ① chatgpt.com 로그인 → ② **Work** 선택(리서치·분석·문서·스프레드시트·프레젠테이션·Sites·다단계 과제) 또는 **Chat**(답변·대화) → ③ 채팅 시작 또는 프로젝트 선택 → ④ 첫 메시지
  - **웹에서 할 수 있는 것 (원문 4항):**
    - Chat/Work 선택 — "Use Chat to explore a question or shape an idea. Switch to Work when you have a clear outcome and want ChatGPT to plan, gather context, and carry a larger task through to a reviewable result."
    - 모델·추론 선택 — "Select a model and reasoning level from the composer. Start with the default effort, then increase it when a task needs deeper planning, analysis, or **a larger multi-agent run**."
    - 도구·반복 워크플로 투입 — 플러그인 설치(Google Drive, GitHub, Slack), 스킬 추가
    - 완성 파일 생성·개선 — 문서·프레젠테이션·스프레드시트·PDF 생성, 채팅에서 검토, 표적 수정 요청, 완성 시 다운로드
  - **웹을 쓸 때 (원문 4항):** 다단계 과제를 완수해야 할 때 / 더 깊은 추론이 필요할 때 / 작업이 내 도구·컨텍스트에 의존할 때 / 검토·공유할 파일이 필요할 때
- 명령·플래그·설정 키: 없음
- 수치·요금·모델명·버전: 없음
- 코드 예시 요지: 없음
- 제약·주의사항: 웹에는 로컬 폴더 접근이 없다(→ `/codex/projects`의 "A ChatGPT project doesn't provide direct access to a folder on your computer" 와 정합).
- 관련 섹션: 제품 표면 비교 장.
- Claude Code 대응 관점 메모: Claude Code에 웹 표면 대응 없음. "multi-agent run"이라는 표현이 Ultra(서브에이전트)를 가리킨다는 점은 자료 11과 교차 확인됨.

---

## 자료 16: Codex CLI  ★ 개발자 핵심

- URL: https://learn.chatgpt.com/codex/cli → 실제 `https://learn.chatgpt.com/docs/codex/cli`
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "Inspect, edit, and run code from your terminal."
  - **왜 CLI인가 (원문 3항):** 로컬 저장소 대상 작업(파일 검사, 편집, 내 머신에 이미 설치된 도구 실행) / 통제 유지(모델·추론 강도·권한·명령 선택) / 스크립트·CI와 조합("Use Codex interactively or call `codex exec` from repeatable workflows and pipelines")

  ### 설치 방법 4종 (원문 명령 그대로)
  | 방법 | 설치 | 업데이트 |
  |---|---|---|
  | **macOS/Linux 독립 설치 프로그램** | `curl -fsSL https://chatgpt.com/codex/install.sh \| sh` | `curl -fsSL https://chatgpt.com/codex/install.sh \| sh` (동일) |
  | **Windows 독립 설치 프로그램** | `powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 \| iex"` | (동일) |
  | **npm** | `npm install -g @openai/codex` | `npm install -g @openai/codex` (동일) |
  | **Homebrew** | `brew install --cask codex` | `brew upgrade --cask codex` |

  - **첫 실행:** 프로젝트 디렉터리에서 `codex` 실행. 최초 실행 시 **Sign in with ChatGPT** 또는 다른 로그인 방식 선택.
  - **첫 과제 예시:** `Tell me about this project`
  - **원문 권고:** "**Create Git checkpoints before and after a task so you can revert changes.**"

  ### CLI 기능 지도 (원문 — 명령별 정리, 책의 CLI 장 구조로 그대로 쓸 수 있음)
  | 명령/기능 | 설명(원문 요지) |
  |---|---|
  | `codex resume` | "**Return to a saved chat** — Reopen a recent chat from the current repository, or search across local chats when you need to return to older work." |
  | `codex --image` | "**Bring visual context into the prompt** — Pass an error screenshot, architecture diagram, or design reference with the first prompt, or paste an image into the interactive composer." |
  | `subagents` | "**Split up a larger investigation** — Ask Codex to delegate focused work to specialized agents, then bring their findings back into the main terminal session." |
  | `codex --search` | "**Search for current context** — Switch a run to live web search when a task depends on current releases, documentation, or external behavior. **Search activity stays visible in the transcript.**" |
  | `codex cloud` | "**Move work to Codex cloud** — Browse active and completed chats, submit work to a configured environment, and apply the result to your local repository from the terminal." |
  | `codex mcp` | "**Connect external tools with MCP** — Add local or remote MCP servers, authenticate when needed, and **inspect the tools available to the current session before Codex uses them.**" |
  | `/permissions` | "**Set the boundaries for each run** — Choose when Codex can edit files or run commands without asking, and **inspect the active sandbox and writable roots** before you continue." |
  | `codex completion` | "**Fit Codex to your terminal** — Generate completions for your shell, choose a syntax theme, and open longer prompts in the editor configured by **VISUAL or EDITOR**." |

  ### CLI로 할 수 있는 일 (원문 3항)
  - **터미널에 코딩 루프를 유지:** 저장소에서 Codex를 시작해 낯선 코드 탐색, 변경 계획, 파일 편집, 로컬 개발 도구 실행. 활성 턴을 steer하고, 명령과 diff를 나타나는 대로 검사하고, 후속 작업을 같은 세션에 유지.
  - **스킬과 플러그인 사용:** 반복 지침을 스킬로 패키징하고, 플러그인으로 팀 도구·데이터에 CLI를 떠나지 않고 연결.
  - **출하 전 변경 리뷰:** "Run a dedicated review against uncommitted changes, a commit, or a base branch. Codex reports prioritized findings **without modifying your working tree**, so you can address risks before you commit or open a pull request."

  ### CLI를 쓸 때 (원문 4항)
  터미널에서 일할 때 / 스크립팅·CI가 필요할 때 / 로컬 코드 리뷰를 원할 때 / 클라우드로 작업을 넘기고 싶을 때
- 명령·플래그·설정 키 (원문 그대로): `codex`, `codex exec`, `codex resume`, `codex cloud`, `codex mcp`, `codex completion`, `--image`, `--search`, `--cd <directory>` / `-C`(자료 23 참조), `--model` / `-m`(자료 11), `/permissions`, `/model`, `/review`, `/new`, `/resume`, `/plugins`, `/pets`, `/pet`, `/goal`, `/plan`, `/status`, `/mention`, `/side`, `/init`, 환경 변수 `VISUAL`, `EDITOR`
- 수치·요금·모델명·버전: 패키지명 `@openai/codex` (npm), Homebrew cask 이름 `codex`
- 코드 예시 요지: 위 설치 명령 4종 + `Tell me about this project`
- 제약·주의사항: 브라우저(내장), Computer Use, 예약 작업 관리 UI, 시각화 렌더링, Plugins의 일부는 **CLI에서 불가**(각 해당 자료 참조). CLI는 ChatGPT Projects 뷰를 노출하지 않는다.
- 관련 섹션: CLI 장 전체. 설치 표와 기능 지도 표를 그대로 사용.
- Claude Code 대응 관점 메모: 대응이 가장 촘촘한 영역.
  - `codex` ↔ `claude` / `codex exec` ↔ `claude -p` (비대화형)
  - `codex resume` ↔ `claude --resume` / `--continue`
  - `codex mcp` ↔ `claude mcp`
  - `codex completion` ↔ `claude` 셸 완성
  - `/permissions` ↔ `/permissions` (**이름 동일**)
  - `/model` ↔ `/model` (**이름 동일**)
  - `/review` ↔ `/review` (**이름 동일**)
  - `codex --search` ↔ Claude Code의 WebSearch 도구 (Codex는 **런 단위 플래그**로 전환하는 반면 Claude Code는 툴 권한으로 관리 — 설계 차이)
  - `codex cloud` ↔ Claude Code에 직접 대응 없음
  - **설치 경로가 4종(curl/PowerShell/npm/Homebrew)이라는 점**이 npm 중심의 Claude Code와 대비된다.

---

## 자료 17: Codex IDE extension

- URL: https://learn.chatgpt.com/codex/ide → 실제 `https://learn.chatgpt.com/docs/codex/ide`
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "Build with the context already in your editor."
  - **왜 IDE 확장인가 (원문 3항):**
    - "**Use the context already open:** Reference open files, selected code, and recent chats directly from the composer. Codex starts with the code you are already looking at, so you spend less time restating the problem."
    - "**Review changes beside your code:** Read the summary, inspect a focused diff, and follow up in the same chat. Keep only the changes you want while the source and rationale stay visible together."
    - "**Delegate when the task grows:** Keep quick iterations local, or connect Codex web when a task needs more time and room."
  - **지원 IDE와 설치 경로 (원문 그대로):**
    | IDE | 설치 |
    |---|---|
    | Visual Studio Code | `vscode:extension/openai.chatgpt` |
    | Cursor | `cursor:extension/openai.chatgpt` |
    | Windsurf | `windsurf:extension/openai.chatgpt` |
    | VS Code Insiders | Marketplace `itemName=openai.chatgpt` |
    | **Xcode** | Apple 문서 "setting-up-coding-intelligence" (**자체 통합**) |
    | **JetBrains IDEs** | JetBrains 문서 "codex-agent" (**자체 통합**) |
    - 원문: "VS Code and compatible editors use the Codex extension; **Xcode and JetBrains IDEs provide their own integrations.**"
  - **Codex 열기:** VS Code/Cursor/Windsurf → Codex 아이콘 선택. 안 보이면 명령 팔레트에서 **Codex: Open Codex Sidebar**. **Xcode** → 코딩 어시스턴트를 열고 새 채팅 시작 후 에이전트로 Codex 선택. **JetBrains** → AI Chat을 열고 Codex 선택.
  - 첫 채팅: 코드베이스 설명, 표적 변경, 디버깅 요청. "Create Git checkpoints before and after a task so you can revert changes."
  - **IDE에서 할 수 있는 것:** 이미 열린 컨텍스트 사용(열린 파일·선택 영역·최근 채팅을 컴포저에 추가) / 코드 옆에서 변경 리뷰("Review a concise summary and the changed lines **without an extra navigation pane**") / 커지면 위임(로컬 빠른 반복 vs Codex web 위임)
  - **IDE 확장을 쓸 때:** 표적 편집을 할 때 / 낯선 코드를 익힐 때 / 제자리에서 변경을 리뷰할 때 / 더 큰 작업을 위임할 때
- 명령·플래그·설정 키: 명령 팔레트 **Codex: Open Codex Sidebar**, **Add to Codex Thread**(자료 6), 확장 ID `openai.chatgpt`
- 수치·요금·모델명·버전: 확장 marketplace item name = `openai.chatgpt` (Codex 전용 ID가 아니라 **ChatGPT 확장으로 통합**돼 있음 — 주목할 사실)
- 코드 예시 요지: 없음
- 제약·주의사항: **플러그인은 IDE 확장에서 사용 불가**(자료 33), **내장 브라우저 사용 불가**(자료 30), 예약 작업 관리 UI 없음(자료 25), Pets 없음(자료 28), 시각화 렌더링 미지원(자료 24), 별도 알림 컨트롤 없음(자료 27). IDE 확장은 ChatGPT Projects 뷰를 노출하지 않는다.
- 관련 섹션: IDE 장. 표면별 기능 차이표(위 "제약"을 모아 한 표로)는 이 책의 고유 가치가 될 수 있다.
- Claude Code 대응 관점 메모: Claude Code의 VS Code/JetBrains 확장과 대응. **결정적 차이: Codex IDE 확장은 "열린 파일을 자동으로 컨텍스트에 포함"** 한다고 명시(자료 6의 Note). Claude Code는 명시적 참조가 기본. 또 Codex는 **Xcode 공식 통합**이 있다 — Claude Code에는 없는 표면.

---

## 자료 18: Codex cloud

- URL: https://learn.chatgpt.com/codex/cloud
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "Run coding tasks in parallel cloud environments." 격리된 클라우드 환경에서 작업을 병렬 실행하고, 웹·GitHub·Linear·Slack에서 작업을 시작.
  - **왜 클라우드인가 (원문 3항):**
    - "**Run work in parallel:** Give longer tasks dedicated environments and let them continue while you work on something else."
    - "**Reproduce the environment:** Configure the dependencies, tools, variables, and setup steps each repository needs."
    - "**Review before you merge:** Inspect the summary and diff, request a follow-up, or open a pull request when the result is ready."
  - **설정 5단계 (원문):** ① `https://chatgpt.com/codex` 접속·로그인 → ② **GitHub 연결**(프롬프트가 뜨면 계정 연결 후 Codex가 접근할 저장소 선택) → ③ **환경 생성**(`https://chatgpt.com/codex/settings/environments`에서 저장소용 환경 생성, 필요한 의존성·도구·환경 변수·시크릿 구성) → ④ 첫 과제 시작(환경 선택 후 원하는 결과 서술; 작업 로그를 보거나 백그라운드로 실행) → ⑤ 결과 검토(요약·diff 검토 후 후속 변경 요청 또는 PR 열기)
  - **클라우드로 할 수 있는 것:** 여러 과제 위임(병렬 시작 후 검토 가능해지는 대로 복귀) / 재현 가능한 환경 구축 / 통합에서 위임("Start work in Codex cloud from **GitHub pull requests, Linear issues, or Slack channels and threads**")
  - **클라우드를 쓸 때 (원문 4항):** 작업이 백그라운드에서 돌아야 할 때 / 여러 시도를 비교하고 싶을 때(로컬 머신을 묶어두지 않고 병렬 실행) / 작업이 GitHub·Linear·Slack에서 시작될 때 / 개발 머신에서 떨어져 있을 때
- 명령·플래그·설정 키: `codex cloud`(CLI에서 사용, 자료 16), 환경 설정 URL `chatgpt.com/codex/settings/environments`
- 수치·요금·모델명·버전: **클라우드에서 사용 가능한 모델은 `gpt-5.6-sol` 뿐**(자료 11 교차 확인). **"Currently, you can't change the default model for Codex cloud chats."**
- 코드 예시 요지: 없음
- 제약·주의사항:
  - **인터넷 접근이 기본 차단:** "Tasks delegated to the cloud run in isolated environments. **Internet access is off during the agent phase unless you enable it for the environment.**" (자료 6에서 교차 확인)
  - **시크릿 처리:** 용어집 정의 — "Encrypted value **available to setup scripts but removed before the agent phase.**" (셋업 단계에서만 접근 가능, 에이전트 단계에서는 제거)
  - **API 키 로그인 시 클라우드 사용 불가**(자료 12 기능 매트릭스: Codex cloud = API Key ⛔)
  - GitHub 연결이 사실상 전제 조건.
- 관련 섹션: 클라우드·위임 장. 시크릿의 "셋업 단계 후 제거" 설계는 보안 장의 좋은 소재.
- Claude Code 대응 관점 메모: Claude Code에 **직접 대응하는 관리형 클라우드 실행 환경이 없다**(remote worktree/원격 에이전트는 있으나 OpenAI 관리형 컨테이너와는 다름). GitHub/Linear/Slack에서 이슈·PR로 작업을 촉발하는 패턴은 Claude Code의 GitHub Action과 개념적으로 유사하나, Codex는 이를 **제품 내장 통합**으로 제공.

---

## 자료 19: ChatGPT & Codex changelog  ★ 릴리스 원장

- URL: https://learn.chatgpt.com/codex/changelog
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- **수집 주의:** 이 페이지는 **`.md` 버전이 404**다(컴포넌트 기반). 본 리서치는 HTML을 받아 `<main>` 텍스트를 추출했다. 재현 시 동일 방식 필요.
- 핵심 내용: 부제 "Latest updates to ChatGPT and Codex". 필터 탭: **All updates / General / ChatGPT desktop app / Remote / Codex CLI**. 월별 내비게이션: **July 2026 → May 2025** (2025-05 ~ 2026-07, 총 **95개 항목**).

  ### 전체 항목 색인 (날짜 | 제목 — 전수, 원문 그대로)
  **2026년 7월 (9건)**
  - 2026-07-31 | GPT-5.4 and GPT-5.4 mini retire from Codex on August 31
  - 2026-07-30 | Browser upgrades, multi-repository review, and image editing **26.727**
  - 2026-07-29 | Sign in with ChatGPT (beta)
  - 2026-07-27 | ChatGPT for iOS **1.2026.202**
  - 2026-07-23 | ChatGPT Voice and multi-folder projects **26.715**
  - 2026-07-20 | ChatGPT for iOS **1.2026.195**
  - 2026-07-13 | ChatGPT for iOS **1.2026.188**
  - 2026-07-09 | **Codex joins the ChatGPT desktop app 26.707**
  - 2026-07-06 | ChatGPT for iOS **1.2026.181**

  **2026년 6월 (12건)**
  - 2026-06-25 | **Codex Remote reaches general availability**
  - 2026-06-22 | ChatGPT for iOS 1.2026.167
  - 2026-06-18 | Record & Replay and remote task handoff **26.616**
  - 2026-06-16 | More Codex features in the EEA, UK, and Switzerland
  - 2026-06-15 | ChatGPT for iOS 1.2026.160
  - 2026-06-11 | Usage resets and Browser Developer mode **26.609**
  - 2026-06-09 | Codex app **26.608**
  - 2026-06-09 | ChatGPT for iOS 1.2026.153
  - 2026-06-04 | Codex app updates **26.602**
  - 2026-06-02 | **Build and deploy websites with Sites**
  - 2026-06-02 | ChatGPT for iOS 1.2026.146
  - 2026-06-01 | **Use Codex with Amazon Bedrock** / Terminal placement controls **26.601**

  **2026년 5월 (11건)**
  - 2026-05-29 | Computer use and mobile access on Windows **26.527**
  - 2026-05-26 | **GPT-5.3-Codex and GPT-5.2 deprecated**
  - 2026-05-25 | ChatGPT for iOS 1.2026.139
  - 2026-05-21 | **Appshots, goal mode, and more 26.519**
  - 2026-05-18 | ChatGPT for iOS 1.2026.132
  - 2026-05-14 | **Work with Codex from anywhere**
  - 2026-05-11 | Expanded Auto-review documentation
  - 2026-05-08 | Codex app **26.506**
  - 2026-05-07 | **Codex for Chrome**
  - 2026-05-06 | Codex analytics governance docs update
  - 2026-05-05 | **Create Codex access tokens** / Codex app **26.429**

  **2026년 4월 (8건)**
  - 2026-04-24 | Codex app 26.423
  - 2026-04-23 | **GPT-5.5 and Codex app updates**
  - 2026-04-20 | Codex app 26.417
  - 2026-04-16 | **Codex can now help with more of your work 26.415**
  - 2026-04-12 | Codex app 26.410
  - 2026-04-10 | Codex app 26.409
  - 2026-04-09 | Codex app 26.406
  - 2026-04-07 | Codex model availability update
  - 2026-04-01 | Codex app 26.325, 26.331, 26.401

  **2026년 3월 (12건)**
  - 2026-03-25 | **Build and install plugins in Codex** / Codex app 26.324
  - 2026-03-24 | Codex app 26.323
  - 2026-03-20 | Codex app 26.320
  - 2026-03-19 | Codex app 26.318, 26.319
  - 2026-03-18 | Codex app 26.317
  - 2026-03-17 | **Introducing GPT-5.4 mini in Codex**
  - 2026-03-16 | Codex app 26.313
  - 2026-03-12 | Codex app 26.312
  - 2026-03-11 | Codex app 26.311
  - 2026-03-05 | **Introducing GPT-5.4 in Codex** / Codex app 26.305
  - 2026-03-04 | Codex app 26.304
  - 2026-03-03 | Codex app 26.303

  **2026년 2월 (12건)**
  - 2026-02-28 | Codex app 26.228
  - 2026-02-27 | Codex app 26.227
  - 2026-02-26 | Codex app 26.226
  - 2026-02-17 | Codex app 26.217
  - 2026-02-12 | **Introducing GPT-5.3-Codex-Spark** / Codex app 26.212
  - 2026-02-10 | Codex app 26.210
  - 2026-02-09 | GPT-5.3-Codex in Cursor and VS Code
  - 2026-02-08 | Codex app 26.208
  - 2026-02-06 | Codex app 26.206
  - 2026-02-05 | **Introducing GPT-5.3-Codex** / Codex app 26.205
  - 2026-02-04 | Codex app 26.204
  - 2026-02-03 | Codex app 26.203
  - 2026-02-02 | **Introducing the Codex app**

  **2026년 1월 (4건)**
  - 2026-01-28 | **Web search is now enabled by default**
  - 2026-01-23 | Team Config for shared configuration
  - 2026-01-22 | **Custom prompts deprecated**
  - 2026-01-14 | GPT-5.2-Codex API availability

  **2025년 (27건)**
  - 2025-12-19 | **Agent skills in Codex**
  - 2025-12-18 | **Introducing GPT-5.2-Codex**
  - 2025-12-04 | **Introducing Codex for Linear**
  - 2025-11-24 | Usage and credits fixes
  - 2025-11-18 | **Introducing GPT-5.1-Codex-Max**
  - 2025-11-13 | **Introducing GPT-5.1-Codex and GPT-5.1-Codex-Mini**
  - 2025-11-07 | Introducing GPT-5-Codex-Mini
  - 2025-11-06 | GPT-5-Codex model update
  - 2025-10-30 | **Credits on ChatGPT Pro and Plus**
  - 2025-10-22 | **Tag @Codex on GitHub Issues and PRs**
  - 2025-10-06 | **Codex is now GA**
  - 2025-09-23 | GPT-5-Codex in the API
  - 2025-09-15 | **Introducing GPT-5-Codex**
  - 2025-08-27 | Late August update
  - 2025-08-21 | Mid August update
  - 2025-06-13 | Best of N
  - 2025-06-03 | June update
  - 2025-05-22 | Reworked environment page
  - 2025-05-19 | **Codex in the ChatGPT iOS app**

  ### 대표 항목 상세 (원문 인용)
  - **2026-07-31 GPT-5.4 은퇴 공지:** "On August 31, 2026, GPT-5.4 and GPT-5.4 mini will no longer be available in Codex for users signed in with ChatGPT. GPT-5.4 and GPT-5.4 mini will remain available on the OpenAI API and Codex sessions authenticated with an API key." 대체: `gpt-5.4`→`gpt-5.6-terra`, `gpt-5.4-mini`→`gpt-5.6-luna`. 갱신 대상: workspace defaults, saved model settings, managed configurations, custom agents, scheduled tasks.
  - **2026-07-30 (26.727):** 내장 브라우저 주소창에서 방문 기록 재방문·Google 검색 / Settings에서 방문 기록 관리 + 작업 시 ChatGPT가 기록 검색 허용 / Chrome 확장으로 열린 탭 멘션·하이라이트 텍스트를 사이드 채팅에 / **Chrome 확장에서 YouTube 영상에 질문** / 웹페이지 우클릭 **Ask ChatGPT** / **멀티 저장소 프로젝트의 저장소별 변경 라인 확인 + Review로 교차 diff 검사** / 생성 이미지 확대 뷰어(**Focused view**/**Canvas view**), 이미지 간 코멘트, 표적 편집 / 사이드바 **Activity view** 추가(<kbd>Cmd/Ctrl</kbd>+<kbd>Opt</kbd>+<kbd>U</kbd>) / 브라우저 설정이 지원 브라우저만 표시 / 긴 패키지 경로에서 Windows 설치 신뢰성 개선
  - **2026-07-29 Sign in with ChatGPT (beta):** 선별 플러그인·파트너 사이트에서 롤아웃 시작 — **Airtable, GitLab, HubSpot, Notion, Supabase, Vercel**. "When you sign in, the partner receives **only your name, email address, and profile picture**, if available. You must still review and approve each plugin's requested access as a separate step."
  - **2026-07-09 (26.707) Codex가 ChatGPT 데스크톱 앱에 합류:** macOS·Windows. 기존 Codex 앱 사용자는 평소처럼 업데이트하며 프로젝트·설정·워크플로 유지. Codex를 기본 뷰로 지정 가능, macOS에서는 Codex 앱 아이콘 유지 가능. 신규: 앱에서 Markdown·코드 직접 편집 + 인라인 주석 + 선택 콘텐츠 수정 요청 / **PR Chat**으로 GitHub PR 리뷰(인라인 리뷰 피드백 전송, 제안 패치 검사·편집·수락·거부) / 게시된 Sites에 **커스텀 도메인** 연결. 개선: **GPT-5.6으로 Computer Use 고속화**, 태스크·서브에이전트 활동 추적 개선, 플러그인 관리를 Settings로 이동, **Full access와 Ultra 조합 시 경고 다이얼로그 추가**.
  - **2026-06-25 Codex Remote GA:** ChatGPT 모바일 앱에서 연결된 Mac·Windows 호스트의 작업 시작·계속·진행 확인·승인. "Remote Control now uses **authenticated one-to-one QR pairing** between each iOS or Android device and each host." **"Connections used since June 8, 2026, remain paired; older inactive connections need to pair again."** 신규 **DigitalOcean 플러그인**(Droplet 프로비저닝, SSH 접근 구성, Codex App에 원격 워크스페이스로 연결).
  - **2026-06-11 (26.609):** **Plus·Pro 대상 rate-limit reset banking** 도입(출시 시 무료 1회 + 초대로 추가 획득). **Browser Developer mode**(CDP 접근). **`/init` 명령**을 앱 컴포저에 추가(Codex CLI와 동일한 초기화 워크플로로 프로젝트 지침 생성). macOS Dock 아이콘 커스터마이즈(라이트/다크 Codex 변형). **EEA·영국·스위스 외 Enterprise 사용자에게 Computer Use 추가.** **Windows용 Computer Use 앱별 접근 통제 설정 지원.** 명령 메뉴에 **Unread chats** 섹션. **"Made Browser use up to 2x faster through CDP and DOM snapshot optimizations."** <kbd>Cmd</kbd>+<kbd>Enter</kbd> / <kbd>Ctrl</kbd>+<kbd>Enter</kbd>를 커스텀 승인 피드백 제출 단축키로 추가.
  - **2026-06-09 (26.608):** **"Added Import to Codex flows for importing supported setup from Claude Code and Claude Cowork, including during onboarding."** (← 자료 5의 근거) 플러그인 화면 개편(탭 분리, 마켓플레이스·카테고리 필터, 키보드 내비게이션). Settings 검색 확장(Git, pets 포함).
- 명령·플래그·설정 키: `/init`, <kbd>Cmd/Ctrl</kbd>+<kbd>Opt</kbd>+<kbd>U</kbd>(Activity view), <kbd>Cmd/Ctrl</kbd>+<kbd>Enter</kbd>(승인 피드백 제출)
- 수치·요금·모델명·버전 (**버전 원장**): 데스크톱 앱 버전은 `26.YMM` 형식(예: 26.727 = 2026-07-27 빌드로 추정되나 **문서에 명시 없음 — 추정 금지**). iOS는 `1.2026.NNN` 형식. 최신 확인 버전: 데스크톱 **26.727**(2026-07-30), iOS **1.2026.202**(2026-07-27).
- 코드 예시 요지: 없음
- 제약·주의사항: 이 페이지는 **책의 신선도 관리 기준점**이다. 출간 시점에 재확인 필요. `.md` 미제공.
- 관련 섹션: "Codex 연대기" 장의 정밀 근거. 자료 10(What's new)이 서사, 이것이 원장.
- Claude Code 대응 관점 메모: **2025-10-06 "Codex is now GA"** 가 기준점 — Codex는 2025년 하반기 GA 이후 약 10개월 만에 데스크톱 앱·클라우드·브라우저·Computer Use·음성·전용 키보드까지 확장했다. 이 속도 자체가 책의 서사 축이 될 수 있다.

---

## 자료 20: Feature Maturity

- URL: https://learn.chatgpt.com/codex/feature-maturity
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: 이 페이지는 **성숙도 등급의 정의만** 담는다(전체 1.7KB). 도입문: "Some ChatGPT and Codex features ship behind a maturity label so you can understand how reliable each one is, what might change, and what level of support to expect."

  ### 성숙도 4등급 (원문 표 전체)
  | Maturity | What it means | Guidance |
  |---|---|---|
  | **Under development** | Not ready for use. | Don't use. |
  | **Experimental** | Unstable and OpenAI may remove or change it. | Use at your own risk. |
  | **Beta** | Ready for broad testing; complete in most respects, but some aspects may change based on user feedback. | OK for most evaluation and pilots; expect small changes. |
  | **Stable** | Fully supported, documented, and ready for broad use; behavior and configuration remain consistent over time. | Safe for production use; removals typically go through a deprecation process. |
- 명령·플래그·설정 키: 없음
- 수치·요금·모델명·버전: 없음
- 코드 예시 요지: 없음
- 제약·주의사항 / **리서치 리드 질의 응답:** **기능별 성숙도 등급을 나열한 목록은 이 페이지에 없고, 그룹 A의 어느 페이지에도 없다.** 등급은 각 기능 문서에 **인라인 문구**로 붙는다. 그룹 A에서 확인된 실제 라벨 부착 사례:
  - `gpt-5.3-codex-spark` = **research preview** (자료 11, 12)
  - **Chronicle** = "opt-in **research preview**" (자료 7)
  - **Visualizations** = "The Visualizations **preview** is rolling out" (자료 24)
  - **Sites** = "included with eligible ChatGPT plans during **public beta**" (자료 12)
  - **Sign in with ChatGPT** = **beta** (자료 19)
  - **Goal mode** = 2026-05 릴리스에서 **experimental 딱지를 뗌**(자료 10) — 즉 그 이전에는 Experimental이었다
  - **Hooks** = 2026-05 릴리스에서 **GA 도달**(자료 10)
  - 주의: 문서가 실제로 쓰는 라벨("research preview", "public beta", "preview")과 이 표의 4등급명("Experimental", "Beta")이 **정확히 일치하지는 않는다.** 책에서 "Codex는 4단계 성숙도 체계를 쓴다"고 단정하면 과잉 일반화가 된다 — "4등급을 정의하되 실제 표기는 혼용된다"로 서술할 것.
- 관련 섹션: "무엇을 프로덕션에 써도 되는가" 절. 위 인라인 라벨 사례 목록은 이 책의 고유 정리 가치가 있다.
- Claude Code 대응 관점 메모: Claude Code에는 공개된 성숙도 등급 체계 문서가 없다. Codex가 이를 명문화한 것은 엔터프라이즈 도입을 의식한 설계로 읽힌다.

---

## 자료 21: Open Source

- URL: https://learn.chatgpt.com/codex/open-source
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "OpenAI develops key parts of Codex in the open. That work lives on GitHub so you can follow progress, report issues, and contribute improvements."

  ### 오픈소스 구성요소 표 (원문 그대로 — 이 책의 "무엇이 열려 있나" 근거)
  | Component | Where to find | Notes |
  |---|---|---|
  | **Codex CLI** | `openai/codex` | "The primary home for Codex open-source development" |
  | **Codex SDK** | `openai/codex/codex-sdk` (실제 경로 `github.com/openai/codex/tree/main/sdk`) | "SDK sources live in the Codex repo" |
  | **Codex App Server** | `openai/codex/codex-rs/app-server` | "App-server sources live in the Codex repo" |
  | **Skills** | `openai/skills` | "Reusable skills that extend ChatGPT and Codex" |
  | **IDE extension** | — | **"Not open source"** |
  | **Codex cloud** | — | **"Not open source"** |
  | **Universal cloud environment** | `openai/codex-universal` | "Base environment used by Codex cloud" |

  > **주목:** app-server 경로가 `codex-rs/`인 점에서 **Codex 코어가 Rust로 구현**돼 있음이 드러난다(문서가 명시적으로 "Rust"라고 말하지는 않으므로, 책에서는 "경로명이 `codex-rs`"라는 사실까지만 기술하고 언어를 단정하려면 별도 확인 필요).

  - **이슈·기능 요청 창구:** 버그 리포트·기능 요청 → `github.com/openai/codex/issues` / 토론 포럼 → `github.com/openai/codex/discussions`
  - **원문 권고:** "When you file an issue, include **which component you are using (CLI, SDK, IDE extension, Codex cloud) and the version** where possible."
  - **Codex for OSS 프로그램:** "If you maintain a widely used open-source project or want to nominate maintainers stewarding important projects, you can also apply to the **Codex for OSS program** for **API credits, ChatGPT Pro with Codex, and selective access to Codex Security**." (신청: `developers.openai.com/community/codex-for-oss`)
- 명령·플래그·설정 키: 없음
- 수치·요금·모델명·버전: 저장소명 `openai/codex`, `openai/skills`, `openai/codex-universal`
- 코드 예시 요지: 없음
- 제약·주의사항: **IDE 확장과 Codex cloud는 오픈소스가 아니다** — 책에서 "Codex는 오픈소스다"라고 뭉뚱그리면 사실 오류가 된다. CLI/SDK/app-server/skills/universal image만 공개.
- 관련 섹션: "Codex 생태계" 장. 개방/폐쇄 경계표는 Claude Code와의 비교에 유용.
- Claude Code 대응 관점 메모: Claude Code CLI는 **비공개 소스**(npm 배포 바이너리)인 반면 **Codex CLI는 오픈소스**다 — 이것은 두 제품의 가장 실질적인 철학 차이 중 하나이며, 책에서 반드시 다뤄야 할 대비점. 반대로 Claude Code의 Agent SDK는 공개돼 있고, Codex SDK도 공개돼 있어 SDK 층은 대칭.

---

## 자료 22: Features (기능 색인)

- URL: https://learn.chatgpt.com/codex/features
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: 기능 허브 페이지. 본문은 `<CodexDocsOverviewLanding>` 컴포넌트의 props로 구성돼 있으며, **그 props에 전체 기능 분류 트리가 담겨 있다**(자리표시자 아님). 도입문: "ChatGPT brings projects and long-running chats together with web browsing, files, images, and plugins. Commands, settings, and troubleshooting references round out these workflows, from choosing the right workflow to giving each chat the context and tools it needs."

  ### 분류 1 — Workflows ("Ways to organize, delegate, and review work.")
  | 기능 | 설명(원문) | 경로 |
  |---|---|---|
  | Projects and chats | "Keep related chats, context, and work together." | `/codex/projects` |
  | **Sites** | "Create, save, and publish interactive websites and apps in ChatGPT." | `/codex/sites` |
  | Visualizations | "Turn ideas and information into interactive visual explanations." | `/codex/visualizations` |
  | Scheduled tasks | "Schedule recurring work and review completed results." | `/codex/automations` |
  | Long-running work | "Let ChatGPT continue working while you step away." | `/codex/long-running-work` |
  | Notifications | "Choose how ChatGPT tells you when work needs attention." | `/codex/notifications` |
  | Pets | "Choose an animated companion and follow chat activity." | `/codex/pets` |
  | Codex Micro | "Monitor and control ChatGPT chats from a Work Louder keyboard." | `/codex/features/codex-micro` |

  ### 분류 2 — Capabilities ("Tools ChatGPT can use to understand, create, and take action.")
  | 기능 | 설명(원문) | 경로 |
  |---|---|---|
  | Browser | "Let ChatGPT browse websites and take action while you stay in control." | `/codex/browser` |
  | Computer use | "Let ChatGPT interact with apps through the visual interface." | `/codex/computer-use` |
  | ChatGPT Voice | "Try voice in Chat, Work, and Codex in the ChatGPT desktop app." | `/codex/features/voice` |
  | Plugins | "Install reusable workflows, connected tools, and shared context." | `/codex/plugins` |
  | **Web search** | "Find current information and bring sources into a task." | `/codex/web-search` |
  | **Image generation** | "Create and edit images as part of your work." | `/codex/image-generation` |
  | **Image inputs** | "Use screenshots and images as context for ChatGPT." | `/codex/image-inputs` |
  | **Appshots** | "Capture app state for visual inspection and debugging." | `/codex/appshots` |
  | **Chrome extension** | "Share browser context with ChatGPT from Chrome." | `/codex/chrome-extension` |
  | **Work with files** | "Create, preview, and refine documents and other generated files." | `/codex/artifacts-viewer` |

  ### 분류 3 — Reference ("Find commands and settings for the ChatGPT desktop app.")
  | 문서 | 설명(원문) | 경로 |
  |---|---|---|
  | **Commands** | "Use app commands, keyboard shortcuts, and deep links." | `/codex/reference/commands` |
  | **Slash commands** | "Use shortcuts for common interactive actions." | `/codex/reference/slash-commands` |
  | **Settings** | "Configure ChatGPT desktop app preferences." | `/codex/reference/settings` |
  | **Troubleshooting** | "Resolve common issues in the ChatGPT desktop app." | `/codex/reference/troubleshooting` |
- 명령·플래그·설정 키: 없음
- 수치·요금·모델명·버전: 없음
- 코드 예시 요지: 없음
- 제약·주의사항: 이 표에서 **그룹 A 33개 목록에 없는 문서 9개**가 드러난다 — Sites, Web search, Image generation, Image inputs, Appshots, Chrome extension, Work with files(artifacts-viewer), Commands, Slash commands, Settings, Troubleshooting. 아래 "추가 발견 URL"에 반영.
- 관련 섹션: 책의 전체 목차 설계 근거. **이 3분류(Workflows / Capabilities / Reference)를 책의 부(部) 구조로 차용하는 것을 권장.**
- Claude Code 대응 관점 메모: Codex의 "Capabilities" 목록은 Claude Code의 도구 목록(Bash, Read, Edit, WebSearch, WebFetch…)에 대응하지만, **Codex 쪽은 사용자 관점 기능명**(Browser, Computer use, Appshots)으로, Claude Code는 **에이전트 관점 도구명**으로 노출한다. 같은 것을 다른 층위에서 이름 붙인 셈 — 좋은 분석 소재.

---

## 자료 23: Projects and chats

- URL: https://learn.chatgpt.com/codex/projects
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: **표면별로 "프로젝트"의 의미가 다르다** — 이 페이지는 `ContentModeSwitch`로 app/web/cli/ide 4버전을 병기한다. 책에서 반드시 구분해 서술해야 할 지점.

  ### 표면별 프로젝트 정의 (원문)
  | 표면 | 프로젝트란 |
  |---|---|
  | **데스크톱 앱** | **Projects** 뷰에 **ChatGPT 프로젝트**와 **로컬 프로젝트**(내 컴퓨터 폴더에 연결)가 함께 있다. |
  | **웹** | 관련 채팅·파일·지침·소스를 묶는 단위. Chat과 ChatGPT Work 채팅이 같은 프로젝트에 들어갈 수 있다. 각 프로젝트에 **Chats** 섹션과 **Sources** 섹션. **"A ChatGPT project doesn't provide direct access to a folder on your computer, so upload or connect the sources you want ChatGPT to use."** |
  | **CLI** | "Codex CLI treats **the directory where you start it** as the project for the chat." `codex`를 원하는 디렉터리에서 실행하거나 **`--cd <directory>` (`-C`)** 로 명시. **"The CLI doesn't expose the ChatGPT Projects view."** |
  | **IDE 확장** | "The IDE extension treats the **folder or workspace open in your IDE** as the local project. In a **multi-root workspace, select the workspace root** for the chat." Projects 뷰 미노출. |

  - **프로젝트를 만들 때 vs 안 만들 때 (원문, 공통):** "Create a project when work will **continue over time, produce more than one output, or depend on the same files and sources.** Start a chat without a project when the work is **self-contained** and doesn't need shared project context."
  - **작업 단위 원칙(원문):** "Start a separate chat for **each distinct outcome** so its messages and results stay focused while the project keeps related work organized."

  ### 정리 기능 (데스크톱/웹)
  - **Pin a project** — 사이드바 상단 고정 / **Pin a chat** — 자주 돌아가는 채팅 고정
  - **Rename a chat** — 결과를 서술하는 짧은 제목. 원문 예: "Q3 launch brief", "Checkout accessibility review"
  - **Search projects** — Projects 뷰에서. **데스크톱: <kbd>Cmd</kbd>/<kbd>Ctrl</kbd>+<kbd>G</kbd>로 과거 채팅 검색 / 웹: <kbd>Cmd</kbd>/<kbd>Ctrl</kbd>+<kbd>K</kbd>** ("when you remember a phrase or **branch name** but not the title")
  - **Archive a chat** — 데스크톱은 프로젝트 메뉴의 **Archive chats**로 일괄 아카이브 가능
  - **원문 주의:** "**Pinning doesn't add context or change what ChatGPT can access.** It only changes where the project or chat appears in the sidebar."
  - 아카이브 복원: **데스크톱 = Settings > Archived chats** / **웹 = Settings > Data Controls > Archived chats** (경로가 다름)

  ### 로컬 프로젝트와 다중 폴더 (데스크톱 전용) — 2026-07-23 추가 기능
  - 프로젝트에 폴더가 반드시 필요하지는 않으나 필요에 따라 붙일 수 있다. 프로젝트 메뉴 → **Edit project** → **Add folder**로 여러 폴더 부착. "ChatGPT can read and change files in **every attached folder**."
  - 기본 작업 디렉터리 변경: 폴더를 가리키고 **Make primary**.
  - **primary 폴더의 특권 (원문, 중요):** "New chats start in the primary folder. Codex also uses that folder for **Git operations and automatic discovery of `AGENTS.md`, skills, and `config.toml`.** Secondary folders remain available for file search, reading, and editing, but **Codex doesn't automatically discover those project files from secondary folders.**"
  - 다중 폴더를 쓸 때: 관련 작업이 다른 곳에 있을 때(앱과 문서, 웹사이트와 백엔드). 무관한 작업이나 각 채팅이 저장소의 한 부분만 접근해야 할 때는 별도 프로젝트를 만들 것. **"Remote projects currently support one folder."**
  - Git 리뷰·PR·worktree 액션은 **primary 저장소**를 대상으로 한다. worktree에서 채팅을 시작해도 다른 폴더는 부착 상태를 유지.
  - **원문 경계 선언:** "Projects and worktrees organize work, but **the sandbox enforces what local commands can read, change, or access over the network.**"

  ### Quick chat (데스크톱 전용)
  - "Quick chat opens an **ordinary ChatGPT chat**. ChatGPT chats **don't appear in the Codex sidebar**, which contains your Codex chats and projects."
  - 열기: **New chat**에 마우스를 올려 오른쪽 **Quick chat** 아이콘, 또는 **<kbd>Cmd</kbd>+<kbd>Option</kbd>+<kbd>N</kbd>(macOS) / <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>N</kbd>(Windows)**. New chat에서 기존 ChatGPT 채팅을 열어 Codex 채팅에 추가할 수도 있다.

  ### CLI에서의 채팅 운영
  - `/new` — 결과 단위로 별도 채팅 시작 / `/resume`(Codex 실행 중) 또는 `codex resume` — 저장된 채팅 이어가기
  - **원문:** "The chat keeps its transcript and **recorded working directory**, while Codex reads files from the **current working tree**. Keep durable project guidance in `AGENTS.md` or checked-in documentation so it is available to future chats."

  ### 컨텍스트·도구 투입 (표면별 차이)
  | 표면 | 가능한 것 |
  |---|---|
  | 데스크톱 앱 | 파일·이미지 첨부 / **플러그인** / **MCP** 서버 / **메모리** |
  | CLI | 이미지 인풋 / **플러그인** / **MCP** 서버 / **메모리** |
  | IDE 확장 | 열린 파일·선택 코드 참조 / **MCP** 서버 / 연결된 Codex 호스트의 **메모리** (**플러그인 없음**) |
  | 웹 | 프로젝트 **Sources** 섹션에 파일·연결 소스 / 채팅에 파일·이미지 첨부 / **ChatGPT Work에서 플러그인** / **메모리** (**MCP 없음**) |
- 명령·플래그·설정 키: `--cd <directory>` / `-C`, `/new`, `/resume`, `codex resume`, <kbd>Cmd/Ctrl</kbd>+<kbd>G</kbd>(데스크톱 채팅 검색), <kbd>Cmd/Ctrl</kbd>+<kbd>K</kbd>(웹 채팅 검색), <kbd>Cmd</kbd>+<kbd>Option</kbd>+<kbd>N</kbd> / <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>N</kbd>(Quick chat), **Edit project / Add folder / Make primary**, **Settings > Archived chats**, **Settings > Data Controls > Archived chats**
- 수치·요금·모델명·버전: 없음. (다중 폴더는 2026-07-23 릴리스 26.715에서 도입 — 자료 19 교차 확인)
- 코드 예시 요지: 없음
- 제약·주의사항: **secondary 폴더에서는 `AGENTS.md`·skills·`config.toml`이 자동 탐색되지 않는다** — 다중 폴더 프로젝트의 가장 흔한 함정. 원격 프로젝트는 폴더 1개만 지원.
- 관련 섹션: 프로젝트 구성 장. 표면별 정의 4분할 표는 반드시 포함.
- Claude Code 대응 관점 메모: **CLI의 "시작 디렉터리 = 프로젝트"는 Claude Code와 정확히 동일한 모델**이다. Codex가 추가한 것은 그 위에 얹은 **GUI 프로젝트 개념(다중 폴더 + primary/secondary)**. Claude Code의 다중 디렉터리(`--add-dir`)와 유사하나, **Codex는 primary만 `AGENTS.md`를 자동 탐색**한다는 비대칭이 있다(Claude Code는 추가 디렉터리의 CLAUDE.md도 로드). `--cd`/`-C` ↔ Claude Code에는 대응 플래그 없음(cwd로 처리).

---

## 자료 24: Visualizations

- URL: https://learn.chatgpt.com/codex/visualizations
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "Visualizations turn questions, ideas, and information into **charts, maps, diagrams, calculators, simulations, and interactive explanations** you can explore in a ChatGPT chat."
  - **호출:** 컴포저에서 `@` 입력 → `Visualize` 타이핑 → **Plugins** 아래 **Visualize** 선택. 컴포저가 요청 앞에 **Visualize** 태그를 붙인다. 웹에서는 `@Visualize`를 직접 타이핑해 제안을 선택해도 된다. 플러그인 설명은 **"Create visualizations and interactive tools"**.

  ### 가용성 표 (원문 그대로)
  | Surface | Current availability |
  |---|---|
  | ChatGPT on the web | Available to supported accounts in Chat and ChatGPT Work |
  | ChatGPT desktop app | Rolling out in preview |
  | ChatGPT mobile apps | Rolling out to eligible accounts; composer controls can differ by app version |
  | **Codex CLI and IDE extension** | **Visualization rendering isn't supported** |

  - **원문:** "The **Visualize** suggestion is the reliable sign that the preview is enabled for your account. During the rollout, availability can differ across accounts, workspaces, and app versions, **even on the same plan.**"
  - **형식 선택 원칙 (원문 — "Ask for the smallest format that fits the job"):**
    - 라벨된 관계나 프로세스 → **다이어그램**
    - 이름 붙은 수치 데이터와 비교 → **차트/플롯**
    - 지리 정보 → **지도**
    - 입력·시간·움직임·공간 관계가 변해야 할 때 → **인터랙티브 시각화**
    - 공유 가능한 URL·권한·영속 데이터가 있는 지속 호스팅 앱이 필요할 때 → **Site**
  - **후속 개선 제안 (원문 목록):** 컨트롤·필터·비교·주석 추가/제거 / 원본 데이터·단위·라벨·가정 수정 / 집계·비닝·샘플링으로 느린 결과 단순화 / 간결한 텍스트 요약과 데이터 표 추가 / 모든 컨트롤을 키보드 접근 가능하게 하고 가시적 포커스 상태 추가 / 색뿐 아니라 라벨·패턴 사용, 반복 모션 제거 / 호스팅·재방문이 필요하면 Site로 전환
  - **중요 경고(원문):** "**A follow-up can create a replacement visualization instead of editing the original result in place. Review the new version before relying on it.**"
  - **공유·재사용:** 채팅의 표준 **Share** 액션 사용. **"Review the entire shared chat first, including its source data and earlier messages."** 그리고 결정적 성질 — "**A visualization is generally a snapshot of the information available when ChatGPT created it, not a live dashboard that stays synchronized with a connected source.**"
  - **접근성:** 생성된 시각화는 시맨틱 컨트롤·가시적 포커스·읽기 쉬운 대비·감소된 모션을 지향하지만 **결과가 들쭉날쭉할 수 있다.** 공유 전 확인하고, 텍스트 요약·데이터 표 추가, 축·단위 라벨링, 색 의존 회피, 키보드 동작을 요청할 것.
  - **실패 복구:** "Visualizations can take **a minute or longer** to generate." 비어 있거나 없으면 응답 완료를 기다리고 채팅을 **한 번** 새로고침 후 재시도. 그래도 실패하면: 더 작고 단순한 시각화 요청 / 큰 데이터셋은 집계·비닝·샘플링하거나 정밀도 축소 / 동작하지 않는 생성 컨트롤·라이브러리 제거 / 중요 값·지리 경계·소스 가정 검증 / 차트·다이어그램·표·Site로 대체 요청
  - 예시 갤러리: "These examples reproduce three visualizations from the **GPT-5.6 launch page**" — 스피로그래프(기하 조절 가능), 파동 간섭 실험실(이동 가능한 프로브), 토크나이저 설명기(편집 가능한 텍스트와 토큰화 단계)
- 명령·플래그·설정 키: `@Visualize`
- 수치·요금·모델명·버전: GPT-5.6 런치 페이지 참조. 생성 시간 "a minute or longer".
- 코드 예시 요지 (원문 프롬프트):
  ```text
  @Visualize how supply and demand determine a market price. Let me shift each curve, mark the equilibrium, and explain how price and quantity change.
  ```
- 제약·주의사항: **CLI·IDE 확장에서 렌더링 불가.** 프리뷰 롤아웃 중이라 같은 플랜에서도 계정별 차이. 스냅샷이지 라이브 대시보드가 아님. 데이터 취급 판단 원문: "Only include sensitive information when your organization permits it, and review the full chat before you share it."
- 관련 섹션: 산출물·시각화 장. "가장 작은 형식을 요청하라" 원칙과 실패 복구 절차는 실무 박스로.
- Claude Code 대응 관점 메모: Claude Code의 **Artifact 퍼블리싱**과 목적이 유사하나 성격이 다르다 — Codex Visualizations는 **채팅 내 인터랙티브 결과**, Claude Code Artifact는 **호스팅되는 페이지**. Codex에서 "호스팅이 필요하면 Site로 전환하라"고 안내하는 것이 Claude Code Artifact에 더 가까운 대응이다.

---

## 자료 25: Scheduled tasks (Automations)

- URL: https://learn.chatgpt.com/codex/automations
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: 반복 작업을 백그라운드로 예약. 활성·일시중지·완료 작업과 최근 실행을 **Scheduled** 뷰에서 검토. "You can combine scheduled tasks with **skills** for more complex work."

  ### 표면별 지원 (원문)
  | 표면 | 지원 |
  |---|---|
  | 데스크톱 앱 | 로컬 프로젝트와 연동, **프로젝트 디렉터리 또는 격리된 worktree**에서 실행. "Keep the computer on and the app running when a scheduled task needs local files." |
  | 웹 | 워크스페이스에 활성화된 경우 Chat 또는 ChatGPT Work에서 생성, **Scheduled**에서 실행 관리. 업로드 컨텍스트·연결 도구 사용 가능하나 **내 컴퓨터 폴더에서 직접 작업 불가.** |
  | **CLI** | **"Codex CLI doesn't provide the Scheduled management interface."** 프롬프트·스킬·스크립트를 준비·테스트하는 데는 도움됨. |
  | **IDE 확장** | **관리 인터페이스 없음.** 프롬프트·스킬·워크스페이스 변경 준비·테스트에는 활용 가능. |

  - **두 종류의 예약 작업 (이 페이지의 핵심 개념):**
    - **Standalone scheduled task** — "start a new chat for each scheduled run and report results in **Scheduled**." 각 실행이 독립적이어야 하거나, 하나의 예약 작업이 **여러 프로젝트에 걸쳐** 실행돼야 할 때.
    - **Scheduled task inside a chat** — "uses the chat's existing context instead of starting from a new prompt each time." 용어집에서는 이를 **Heartbeat**로도 부른다.
  - **채팅 내 예약이 맞는 경우 (원문 목록):** 장시간 작업이 끝날 때까지 확인 / Slack·GitHub 등 연결 소스를 폴링하되 결과가 같은 채팅에 남아야 할 때 / 고정 주기로 리뷰 루프를 계속하도록 상기 / 플러그인을 쓰는 스킬 주도 워크플로(PR 상태 확인 후 새 피드백 처리) / 진행 중인 리서치·트리아지 채팅을 컨텍스트 손실 없이 계속
  - 채팅 내 예약은 **분 단위 간격**(활발한 후속 루프용)과 **일간·주간** 일정 모두 가능.
  - **원문 권고:** "When you schedule a task inside a chat, **make the prompt durable.** It should describe what ChatGPT should do on each scheduled run, **how to decide whether there is anything important to report**, and **when to stop or ask you for input.**"
  - **커스텀 일정 — RFC 5545 RRULE:** "For an advanced schedule, edit its **RFC 5545 recurrence rule (RRULE)**, such as `RRULE:FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=9;BYMINUTE=0`."
  - **Scheduled 뷰 = 인박스:** "The **Scheduled** view acts as your inbox. Scheduled task runs with **findings** appear there, and an **unread indicator** shows when a run needs your attention." 필터: **All / Active / Paused**.
  - **로컬 vs worktree 실행 (Git 저장소):** 둘 다 백그라운드 실행. "**Worktrees keep changes from scheduled tasks separate from unfinished local work**, while running in your local project **can modify files you are still working on.**" 버전 관리되지 않는 프로젝트에서는 프로젝트 디렉터리에서 직접 실행. 같은 예약 작업을 여러 프로젝트에서 실행 가능.
  - **worktree 정리 (원문 주의):** "If you choose worktrees for Git repositories, **frequent schedules can create many worktrees over time.** Archive scheduled runs you no longer need, and **avoid pinning runs unless you intend to keep their worktrees.**"
  - 모델·추론 강도는 기본값으로 두거나 명시적으로 선택 가능.
  - **ChatGPT에게 예약 작업 생성·수정을 시킬 수 있다:** 작업 내용·일정·각 실행이 현재 채팅으로 돌아올지 새 채팅을 시작할지를 서술하면 ChatGPT가 프롬프트 초안 작성, 목적지 선택, 범위·주기 변경 시 갱신까지 한다. **스킬도 예약 작업을 생성·수정할 수 있다.**
  - **테스트 원칙:** 예약 전 일반 채팅에서 프롬프트를 수동 테스트해 ① 프롬프트가 명확하고 범위가 맞는지 ② 선택/기본 모델·추론 강도·도구가 기대대로 동작하는지 ③ 결과가 검토 가능한지 확인. 실행 시작 후 처음 몇 개 출력을 검토해 프롬프트·주기 조정.
  - 데스크톱 앱에서는 예약 작업 프롬프트에서 **`$skill-name`** 으로 스킬을 명시 트리거 가능.

  ### 권한·보안 모델 (★ 중요)
  - **"Scheduled tasks run unattended and use your default sandbox settings."** "Start with the narrowest access that lets the task succeed, and grant network or broader file access only when required."
  - 샌드박스 모드별 결과 (원문):
    - **read-only** — 파일 수정·네트워크 접근·컴퓨터 앱 사용이 필요한 툴 콜은 **실패**. workspace write로 올릴 것을 고려.
    - **workspace-write** — 워크스페이스 밖 파일 수정·네트워크 접근·컴퓨터 앱 사용이 필요하면 **실패**. **rules**로 샌드박스 밖 실행 명령을 선별 허용 가능.
    - **full access** — "background scheduled tasks carry **elevated risk**, as ChatGPT may change files, run commands, and access network **without asking**." workspace write로 낮추고 rules로 full access 명령을 선별 정의할 것을 권고.
  - **승인 정책:** "Scheduled tasks use **`approval_policy = "never"`** when your organization policy allows it. **If admin requirements disallow `approval_policy = "never"`, scheduled tasks fall back to the approval behavior of your selected permission mode.**"
  - 관리 환경에서는 관리자가 `requirements.toml`로 제한 가능(예: `approval_policy = "never"` 불허, 허용 샌드박스 모드 제약).
- 명령·플래그·설정 키: `$skill-name`, `approval_policy = "never"`, `requirements.toml`, RRULE 문자열, 샌드박스 모드 `read-only` / `workspace-write` / `full access`
- 수치·요금·모델명·버전: **원문 경고 그대로:** "If a scheduled task uses **`gpt-5.4` or `gpt-5.4-mini`** with ChatGPT sign-in, update it before those models retire on **August 31, 2026**. Replace `gpt-5.4` with `gpt-5.6-terra` and `gpt-5.4-mini` with `gpt-5.6-luna`." (자료 11·19와 3중 정합 확인)
- 코드 예시 요지 (원문 그대로 — 셋 다 인용 가치 높음):
  - **스킬 자동 개선 예약 작업:**
    ```markdown
    Scan all of the `~/.codex/sessions` files from the past day and if there have been any issues using particular skills, update the skills to be more helpful. Personal skills only, no repo skills.

    If there's anything we've been doing often and struggle with that we should save as a skill to speed up future work, let's do it.

    Definitely don't feel like you need to update any- only if there's a good reason!

    Let me know if you make any.
    ```
    (→ `~/.codex/sessions` 경로가 드러난다. Claude Code의 `~/.claude/projects/*/`에 대응)
  - **프로젝트 일일 브리핑 예약 작업:** `origin/master`/`origin/main`의 최근 24시간 커밋으로 워크스트림별 exec 브리핑 생성. 형식 규약(H1 워크스트림 섹션, 부제 이탤릭, 수평선), 내용 요구(PR 링크 인라인 `[#123](...)`, **커밋 해시와 "Key commits" 섹션 금지**), 범위 규칙(현재 cwd 내 변경만, 최근 24시간만, PR 제목·설명은 `gh`로 조회 가능).
  - **자기 버그 수정 스킬 `recent-code-bugfix`** — 프론트매터 포함 전문이 문서에 제시돼 있다:
    ```markdown
    ---
    name: recent-code-bugfix
    description: Find and fix a bug introduced by the current author within the last week in the current working directory. Use when a user wants a proactive bugfix from their recent changes, when the prompt is empty, or when asked to triage/fix issues caused by their recent commits. Root cause must map directly to the author's own changes.
    ---
    ```
    5단계 워크플로: ① 최근 변경 범위 확정(`git config user.name`/`user.email`로 작성자 판별, `git log --since=1.week --author=<author>`) → ② 최근 변경에 결부된 구체적 실패 발견 → ③ 최소 수정 구현 → ④ 검증(가장 작은 검증 단계 선호) → ⑤ 보고(근본 원인이 작성자의 최근 변경과 어떻게 연결되는지 명시)
    - 이후 예약 작업: `Check my commits from the last 24h and submit a $recent-code-bugfix.`
- 제약·주의사항: **CLI·IDE에 관리 UI 없음.** 데스크톱 로컬 예약 작업은 컴퓨터가 켜져 있고 앱이 실행 중이어야 하며 프로젝트가 디스크에 존재해야 함. 웹 예약 작업은 실행 간 로컬 폴더·worktree를 유지하지 않음.
- 관련 섹션: 자동화 장 전체. **스킬 프론트매터 전문은 "스킬 작성법" 장의 실제 예제로 그대로 사용 가능.**
- Claude Code 대응 관점 메모: Claude Code의 `/schedule`(cloud routines)·`/loop`과 개념 대응. **결정적 차이: Codex는 "채팅 내 예약(Heartbeat)"이라는 컨텍스트 보존형 반복을 별도 개념으로 제공**한다 — Claude Code의 `/loop`이 프롬프트를 재실행하는 것과 달리, Codex는 기존 대화 맥락으로 돌아온다. `~/.codex/sessions` ↔ `~/.claude/projects/`. `approval_policy = "never"` ↔ `--dangerously-skip-permissions`의 예약 실행판.

---

## 자료 26: Long-running work (Goal mode)

- URL: https://learn.chatgpt.com/codex/long-running-work
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "For work that may take many steps, give ChatGPT a **clear outcome, constraints, and definition of done.** Keep related work in the same chat so ChatGPT can use the same context to choose the next step and decide when the work is complete."
  - **`/goal` — Goal mode:** 데스크톱 앱, Codex CLI, IDE 확장에서 `/goal` 입력. **"The goal text becomes both the first prompt and the completion criteria for the task."** 데스크톱에서는 컴포저 위에 진행 상황 행이 나타나 **일시중지·재개·편집·삭제** 가능.
  - **`/plan` 선행:** "If the outcome is still unclear, start with `/plan`. Ask ChatGPT to **interview you**, identify constraints, and turn the result into a goal with **measurable success criteria**. Then start the refined goal with `/goal`."
  - **"done"의 정의 — 3요소 표 (원문 그대로):**
    | Goal element | What to include |
    |---|---|
    | **Outcome** | Describe the result you want, not only the activity ChatGPT should perform. |
    | **Constraints** | Name required tools, boundaries, compatibility needs, or approaches to avoid. |
    | **Verification** | Add tests, measurements, or review criteria that prove the work is complete. |
  - **웹은 Goal mode가 없다:** "For hosted long-running work in ChatGPT web, use **ChatGPT Work** and put the outcome, constraints, and review criteria **directly in your prompt.**" 같은 채팅에서 컨텍스트 추가·제약 변경·상태 확인. 독립 실행 가능한 작업은 별도 채팅으로. **"avoid giving two tasks write access to the same connected source."**
  - **실행 중 조종:** 데스크톱에서는 goal 진행 행으로 일시중지·재개·편집·삭제. goal 실행 중에도 후속 메시지 전송 가능. **"Use a side chat when you want a status recap or an explanation without interrupting the main chat."** **"Pause the goal before you expect to lose connectivity, then resume it when you're ready."** CLI·IDE에서는 같은 세션/채팅에서 후속 메시지로 조종하고 상태 요약을 요청.
  - **권한 불변 (★ 중요, 원문):** "**Starting a goal doesn't grant ChatGPT broader access.** It keeps the same sandbox and approval policy and pauses when it needs a decision. With **automatic approval reviews**, a separate reviewer can evaluate eligible requests **without expanding those boundaries.**"
  - **병렬 실행:** "Each chat keeps its own context, messages, results, and goal. Run chats concurrently, but **avoid letting two chats change the same files.** Use **worktrees** to give parallel coding chats separate checkouts."
  - **로컬 장시간 작업 팁 (데스크톱):** 설정에서 **Prevent sleep while running**을 켜 Mac이 깨어 있게 할 것. **Pets** 또는 시스템 알림으로 입력 필요/검토 준비 상태 확인.
- 명령·플래그·설정 키: `/goal`, `/plan`, **Prevent sleep while running**(설정)
- 수치·요금·모델명·버전: 없음. (자료 10 기준 Goal mode는 2026-05에 experimental 해제, "objectives that can take **hours or days**")
- 코드 예시 요지 (원문 goal 예시 — 3요소가 모두 든 모범 사례):
  ```text
  Migrate this codebase from JavaScript to TypeScript. Preserve existing behavior,
  compile in strict mode without explicit `any` types, and make the full test suite pass.
  ```
  (Outcome = TS 마이그레이션 / Constraints = 기존 동작 보존, strict mode, 명시적 `any` 금지 / Verification = 전체 테스트 통과)
- 제약·주의사항: **웹에는 `/goal`이 없다**(ChatGPT Work + 프롬프트로 대체). 두 채팅이 같은 파일을 바꾸게 하지 말 것.
- 관련 섹션: 장시간 작업 장. 3요소 표와 TS 마이그레이션 예시는 핵심 교보재.
- Claude Code 대응 관점 메모: `/plan` ↔ Claude Code Plan mode(**이름·기능 모두 유사**). **`/goal`은 Claude Code에 대응 없음** — "목표 텍스트가 곧 완료 기준이 되고, 에이전트가 스스로 완료를 판정한다"는 개념은 Codex 고유. Claude Code에서 이에 가장 가까운 것은 `/loop`이나, 자기 완료 판정 기제는 없다. "Prevent sleep while running" 같은 데스크톱 앱 수준 배려도 CLI에는 없는 것.

---

## 자료 27: Notifications

- URL: https://learn.chatgpt.com/codex/notifications
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "Notifications let you know when work needs attention. **Their controls and delivery channels vary by surface.**"
  - **데스크톱 앱:** **Settings**에서 턴 완료 알림을 **never / only while ChatGPT is in the background / always** 중 선택. **권한 알림**과 **질문 알림**은 별도 토글. OS가 ChatGPT 데스크톱 앱에 알림 권한을 요청할 수 있음.
    - 추가 수단으로 **플로팅 Pet** — 채팅이 **Running / Needs input / Ready / Blocked** 중 어느 상태인지 표시(자료 28).
  - **웹:** **Settings > Notifications**에서 계정에 가용한 알림 카테고리·채널 관리. 카테고리·계정에 따라 **push, email, SMS** 채널 가능. 작업 알림 설정의 **Manage tasks**로 **Scheduled** 열기.
  - **CLI:** 터미널·외부 알림은 **고급 설정 가이드의 Notifications 절**(`/codex/config-file/config-advanced#notifications`) 참조. "You can choose when the TUI emits a notification and **whether Codex runs an external program when a turn completes.**"
  - **IDE 확장:** **"The IDE extension doesn't provide separate notification controls."** 활동을 따라가려면 채팅을 열어 둘 것. 턴 완료 시 외부 프로그램을 실행하려면 **연결된 Codex 호스트에서 `notify`를 설정**.
- 명령·플래그·설정 키: `notify`(config), **Settings > Notifications**(웹), **Manage tasks**
- 수치·요금·모델명·버전: 없음
- 코드 예시 요지: 없음
- 제약·주의사항: IDE 확장에는 알림 컨트롤이 없다.
- 관련 섹션: 장시간 작업/알림 절. 표면별 차이 4분할.
- Claude Code 대응 관점 메모: `notify`(턴 완료 시 외부 프로그램 실행) ↔ Claude Code의 **Stop 훅**과 정확히 대응하는 기능. 웹의 push/email/SMS 채널은 Claude Code에 대응 없음.

---

## 자료 28: Pets

- URL: https://learn.chatgpt.com/codex/pets
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "Pets are **optional animated companions** for following work. Where a pet appears and what it shows depend on the interface you use. **Choosing a pet changes its appearance, not how ChatGPT completes tasks.**"

  ### 데스크톱 앱 — 플로팅 펫
  - **선택·깨우기:** ① 앱 하단 프로필 메뉴에서 **Pets** 선택(또는 **Settings > Pets**) → ② 내장 또는 커스텀 펫 선택 → ③ **`/pet`** 입력하거나 커맨드 메뉴에서 **Wake Pet** 선택
  - 숨기기: **Settings > Pets** 또는 커맨드 메뉴의 **Tuck Away Pet**, 또는 `/pet` 재입력. 선택과 위치는 앱 재실행 후에도 유지. 커스텀 펫 선택 시 **Profile** 뷰에도 나타남.
  - **펫 상태 표 (원문 그대로):**
    | Status | Meaning |
    |---|---|
    | **Running** | A chat is actively working. |
    | **Needs input** | A chat needs your approval, answer, or another decision. |
    | **Ready** | A chat has completed and has unread activity. |
    | **Blocked** | A chat failed or encountered a system error. |
  - **우선순위(원문):** "When more than one chat has activity, the pet prioritizes chats that **need input**, followed by **blocked**, **ready**, and **running** chats." 활동 트레이를 열어 채팅 선택. 펫을 선택하면 ChatGPT로 복귀. **"The activity tray is separate from system notifications."**
  - **Computer Use 연동 (macOS):** "the Computer Use picture-in-picture window can **attach to an awake pet**. Move the pet, and the window follows."
  - **커스텀 펫 만들기:** ① **Settings > Pets** → **Create your own pet** → ② 앱이 번들 **`hatch-pet` 스킬**을 설치하고 스킬을 리로드한 뒤 새 채팅을 연다 → ③ 원하는 펫을 서술하고 프롬프트 전송 → ④ 작업 완료 후 **Settings > Pets**로 돌아가 **Refresh** 선택 후 새 펫 선택
    - **"Custom pets created in the desktop app are stored locally on your computer. They don't automatically sync to ChatGPT web."**
  - **모션 감소:** "Pets respect your operating system's reduced motion setting. When reduced motion is enabled, the pet uses a **still frame** instead of sprite animation."

  ### 웹
  - **Settings > Personalization > Pet > Select pet**에서 내장 펫 또는 **Default**(펫 없음) 선택. 웹 펫은 **지원되는 ChatGPT Work 채팅 안에** 나타난다. **"It doesn't provide the desktop app's floating overlay, activity tray, or `/pet` command."**
  - **커스텀 펫 업로드:** **Upload pet**으로 커스텀 **스프라이트 시트** 추가. **파일 요건: 투명 PNG 또는 WebP, 정확히 1536 × 1872 픽셀, 20 MiB 이하.** 같은 설정에서 편집·다운로드·새로고침·삭제 가능.

  ### CLI
  - `/pets` 또는 `/pet` — 펫 선택기 열기 / `/pets <name>` — 펫 직접 선택 / **`/pets off`** — 터미널 펫 비활성화
  - 선택기에는 내장 펫과 컴퓨터에 설치된 호환 커스텀 펫이 포함. 터미널 펫은 **현재 CLI 세션의 활동만** 보고하며 Running/Needs input/Ready/Blocked 상태를 쓰되 **데스크톱의 다중 채팅 활동 트레이는 제공하지 않는다.**
  - **요구 사항(원문):** "Terminal pets require **iTerm2 3.6 or later**, or a terminal with **Kitty graphics or Sixel support**. They are **unavailable inside tmux and Zellij.**"

  ### IDE 확장
  - **"The Codex IDE extension doesn't provide a pet picker or floating pet overlay."** 데스크톱 앱이나 CLI를 쓸 것.
- 명령·플래그·설정 키: `/pet`, `/pets`, `/pets <name>`, `/pets off`, **Wake Pet**, **Tuck Away Pet**, **Settings > Pets**, **Settings > Personalization > Pet > Select pet**, `hatch-pet` 스킬
- 수치·요금·모델명·버전: 스프라이트 시트 **1536 × 1872 px, ≤20 MiB, 투명 PNG/WebP** / **iTerm2 3.6+**, Kitty graphics, Sixel / tmux·Zellij 불가
- 코드 예시 요지: 없음
- 제약·주의사항: 커스텀 펫은 로컬 저장이라 웹과 동기화되지 않음. tmux/Zellij 사용자는 터미널 펫 불가(한국 개발자 상당수가 해당).
- 관련 섹션: "장시간 작업을 어떻게 지켜보는가" 절의 가벼운 코너. 상태 4종(Running/Needs input/Ready/Blocked)은 알림·Codex Micro와 공통 어휘라 한 번만 정의하고 재사용할 것.
- Claude Code 대응 관점 메모: **Claude Code에 완전히 대응 없음.** 순수한 제품 개성(playfulness) 요소. 다만 그 밑에 깔린 **"에이전트 상태를 항상 보이게 한다"** 는 문제의식은 Claude Code의 터미널 상태줄/StatusLine과 통한다. 책에서 "장난처럼 보이지만 실은 상태 가시성 설계"라는 해석을 붙일 만하다.

---

## 자료 29: Codex Micro (하드웨어)

- URL: https://learn.chatgpt.com/codex/features/codex-micro
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "Codex Micro is a **limited-run collaboration between Codex and Work Louder.**" ChatGPT 데스크톱 앱과 연동해 채팅 확인, 채팅 간 이동, 음성 입력, 공통 액션·스킬 실행을 키보드에서 수행. (2026-07-15 출시 — 자료 10)
  - **설정 5단계:** ① ChatGPT 데스크톱 앱 열기 → ② 후면 버튼을 한 번 눌러 전원 켜기 → ③ USB-C 케이블 연결 또는 Bluetooth 페어링 후 ChatGPT가 감지하면 나타나는 설정 따르기 → ④ **macOS에서 Input Monitoring 허용** → ⑤ **Settings > Codex Micro**에서 Agent Keys가 무엇을 따르거나 실행할지 선택, Command Keys·아날로그 스틱·다이얼 커스터마이즈, 조명·음성 컨트롤 조정
  - 기본적으로 **다이얼을 잠시 길게 누르면** 설정이 열린다. ChatGPT 하단 계정명 옆 Micro 아이콘으로도 가능. 커스텀 다이얼 할당이 길게 누르기 단축키를 대체할 수 있음.
  - **"Work Louder Input isn't required for the ChatGPT integration."** 다른 앱용 컨트롤 커스터마이즈나 레이어 추가에만 사용.
  - **Bluetooth 페어링:** 채널 **3개** 제공. ① 후면 버튼 한 번 눌러 전원 → ② 좌하단 가장자리 터치 컨트롤을 **3초** 길게 누르면 하단 조명이 **파랑** → ③ 터치 컨트롤을 탭해 채널 1·2·3 선택(빠르게 깜빡이면 페어링 준비) → ④ 컴퓨터 Bluetooth 설정에서 연결 → ⑤ 채널 조명이 **solid**가 되면 완료
    - **"The connection selector closes after five seconds without input."** USB-C로 전환하려면 연결 선택기를 열고 하단 조명이 **흰색**이 될 때까지 터치 컨트롤 탭. **"Connecting a USB-C cable while the Micro is still in Bluetooth mode charges it but doesn't switch it to the wired connection."**

  ### Agent Keys (6개, 반투명)
  - 각 키가 채팅 하나를 따르고 상태에 따라 발광. **한 번 누르면** ChatGPT를 전면으로 가져오지 않고 그 채팅으로 전환. **350밀리초 안에 두 번 누르면** 채팅 전환 + ChatGPT 창을 전면으로. 첫 번째 누름으로 포커스하려면 **Focus ChatGPT with a single tap** 켜기.
  - **상태 조명 표 (원문 그대로):**
    | Light | Status | Meaning |
    |---|---|---|
    | White | Idle | The chat is idle. |
    | Blue | Thinking | ChatGPT is working. |
    | Green | Complete | The chat completed with an unread update. |
    | Amber | Requires input | ChatGPT needs your approval or response. |
    | Red | Error | Something went wrong. |
    | Off | No assigned chat | The key doesn't follow a chat. |
  - 선택된 채팅의 키는 자기 상태 색으로 **맥동(pulse)** 한다.
  - **Agent keys 배치 모드 4종:** **Most recent chats**(고정 여부 무관 최근 갱신 6개, 기본값) / **Pinned chats**(**Pinned**의 앞 6개) / **Priority chats**(입력 대기 → 미읽음 → 활성 순) / **Custom assignments**(각 키에 채팅·단축키·물리 키 동작·활성 스킬 할당; 미할당 키를 누르면 새 채팅이 열리고 시작 시 그 키에 배정됨)

  ### Command Keys (6개, 기본 레이아웃 — 원문 표)
  | Key | Default action |
  |---|---|
  | **Fast** | Turn Fast mode on or off. |
  | **Approve** | Approve the current request. |
  | **Decline** | Decline the current request. |
  | **Fork** | Continue the current chat in a new chat. |
  | **Mic** | Start push-to-talk. |
  | **Codex** | Send the message in the composer. |
  - **Mic 키:** 컴퓨터 마이크를 사용한다(**"Codex Micro doesn't have a microphone of its own."**). 기본은 **Push to talk**(누르고 있는 동안 말하고 떼면 정지). 핸즈프리는 **350밀리초 안에 두 번 눌러** 녹음 유지, 다시 누르면 정지.
    - 조명 피드백: 녹음 중 **sea-green** 빛이 키보드를 돌고, 처리 중에는 **움직이는 흰빛**, 프롬프트 준비 완료 시 **solid 흰색**. Codex 키를 눌러 전송.
    - **Microphone key** 아래 **Voice Chat**이 있으면 선택해 Mic 키로 Voice Chat 시작/마이크 토글, 길게 눌러 종료. **Use separate microphone keys**를 켜면 넓은 Mic 키 아래 두 스위치를 독립 매핑.
  - 리매핑: 설정의 **Layout** 프리뷰에서 Command Key 선택 후 키캡과 동작 지정. 가능한 동작 — 브라우저·터미널 열기, 채팅 관리, 변경 리뷰, Git·PR 액션 실행, 파일·사진 첨부, 플러그인·예약 작업 열기, **추론 강도 변경**, 활성 스킬 실행, 기타 단축키 할당. **"If you choose a keycap that's already used somewhere else, ChatGPT swaps the two instead of using one keycap twice."** 리매핑 후 물리 키캡도 교체할 것. **Reset layout**은 Agent Key 모드와 커스텀 채팅 할당은 건드리지 않고 Command Key·아날로그 스틱 기본값만 복원.

  ### 아날로그 스틱 (기본 매핑 — 원문 표)
  | Direction | Default action |
  |---|---|
  | Up | Turn Plan mode on or off. |
  | Right | Go forward in app history. |
  | Down | Show or hide the sidebar. |
  | Left | Go back in app history. |
  - 자유롭게 움직이며 중심에서 충분히 밀면 4방향 액션으로 변환. 각 방향에 임의의 ChatGPT 데스크톱 명령이나 활성 스킬 할당 가능.

  ### 다이얼 (모드 4종 — 원문 표)
  | Mode | Behavior |
  |---|---|
  | **Composer navigation** (기본) | Move through composer controls and select the focused control. |
  | **Reasoning only** | Adjust reasoning effort and open its slider or advanced options. |
  | **Conversation scrolling** | Scroll the active chat; press the dial to jump to the latest message. |
  | **Custom assignments** | Assign an action or skill to the left turn, right turn, press, and long press. |
  - 컴포저 컨트롤이나 메뉴가 열려 있으면 **다이얼 바로 오른쪽 Agent Key가 빨갛게** 켜진다 — 그 키를 눌러 취소. 다이얼 길게 누르기는 **Custom assignments를 제외한 모든 모드**에서 설정을 연다(Custom assignments에서는 길게 누르기에 할당된 액션 실행).

  ### 조명·배터리·레이어
  - **Brightness** 조절, **Auto-dim** 간격을 **30초~1시간** 중 선택 또는 끄기. Micro를 쓰거나 Agent Key 상태가 바뀌면 다시 켜진다. **기본값: 3분 후 소등.**
  - Micro가 배터리 상태를 보고하면 설정과 사이드바 Micro 아이콘 옆에서 확인 가능.
  - **"ChatGPT uses layer 1."** Work Louder Input으로 다른 앱용 **최대 5개 레이어**를 추가 설정 가능.

  ### 문제 해결
  - **macOS Input Monitoring 수정:** ① **System Settings > Privacy & Security > Input Monitoring** → ② 목록에 있으면 ChatGPT 접근 켜기, 없으면 Applications에서 **ChatGPT**를 드래그하거나 **Add (+)** 로 추가 → ③ ChatGPT 종료·재실행 후 layer 1에서 Micro를 감지하는지 확인
  - **연결 간섭:** ChatGPT는 Micro를 감지했으나 연결 실패·통신 유실 시 자동 재시도. 계속되면 재연결하고 키보드 유틸리티·보안 도구가 접근을 막는지 확인. **"On macOS, Work Louder notes that **Karabiner** and **Logitech Options+** can interfere with Micro communication when those apps have Input Monitoring permission."** 테스트하려면 해당 유틸리티를 종료하거나 Input Monitoring 접근을 일시 해제 후 재연결. 관리되는 컴퓨터라면 IT 관리자에게 기기 규칙 확인 요청.
  - 지원: Work Louder 설정 가이드 `worklouder.cc/openai-micro-setup`, 이메일 `hello@worklouder.cc`
  - **구매:** OpenAI Supply Co (`openai.com/supply/co-lab/work-louder/`). 데스크톱 앱은 **Creator Micro 2**(`worklouder.cc/creator-micro-2`, Work Louder 직판)도 지원.
- 명령·플래그·설정 키: **Settings > Codex Micro**, **Focus ChatGPT with a single tap**, **Use separate microphone keys**, **Reset layout**, **System Settings > Privacy & Security > Input Monitoring**
- 수치·요금·모델명·버전: Bluetooth 채널 **3개** / 페어링 길게 누르기 **3초** / 연결 선택기 자동 닫힘 **5초** / 더블탭 판정 **350ms** / Agent Keys **6개**, Command Keys **6개** / Auto-dim **30초~1시간**, 기본 **3분** / ChatGPT는 **layer 1**, 추가 **최대 5 레이어** / 가격 정보는 **문서에 없음**
- 코드 예시 요지: 없음
- 제약·주의사항: **한정 생산(limited-run)**. 자체 마이크 없음. Karabiner·Logitech Options+ 간섭 알려짐.
- 관련 섹션: "Codex의 확장 표면" 장의 마지막 절, 또는 컬럼(칼럼) 소재. 책 전체 분량 대비 과대 서술 주의 — 대부분의 독자는 구매하지 않는다.
- Claude Code 대응 관점 메모: **Claude Code에 완전히 대응 없음** — 전용 하드웨어 컨트롤 서피스는 Codex 고유. 다만 그 기능 목록(승인/거부, Fork, Fast 토글, 추론 강도 조절, Plan 모드 토글)은 **Claude Code에서 모두 키보드·슬래시 커맨드로 존재하는 동작**이다. 즉 Micro는 새 기능이 아니라 **기존 동작의 물리적 바인딩**이라는 점이 관찰의 핵심.

---

## 자료 30: Browser

- URL: https://learn.chatgpt.com/codex/browser
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: **표면에 따라 완전히 다른 두 브라우저**를 설명한다 — 데스크톱의 **내장 브라우저**와 웹의 **클라우드 운영 브라우저**.
  - 공통 정의: "Browser lets ChatGPT open websites, gather current information, and take action while you stay in control."
  - **최상위 경고 (원문, 책의 보안 장 필수 인용):** "**Treat page content as untrusted context.** Review the site and proposed action before sharing sensitive information or allowing ChatGPT to act."
  - **CLI·IDE에서는 사용 불가:** "Browser isn't available in Codex CLI or the Codex IDE extension. Open the ChatGPT desktop app to use the built-in browser."

  ### 데스크톱 — 내장 브라우저
  - 채팅 안에서 사용자와 ChatGPT가 웹사이트·로컬 웹앱을 **공유된 시야**로 본다. 페이지 미리보기, 시각적 피드백 남기기, ChatGPT가 대신 사이트와 상호작용.
  - **별도 프로필:** "The built-in browser uses a **browser profile that is separate from your regular browser.** It doesn't automatically share your existing tabs or browser session. You can sign in directly when a task requires an account." 관리: **Settings > Browser**.
  - **다운로드:** 기본은 시스템 Downloads 폴더. **Settings > Browser**에서 다른 위치 선택, 시스템 기본으로 리셋, 또는 **Ask where to save downloads** 켜기.
  - 기존 Chrome 탭이나 정규 Chrome 프로필이 필요하면 **Chrome 확장**을 쓸 것.
  - **열기:** 툴바에서, URL 클릭으로, 수동 내비게이션으로, 또는 **<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>B</kbd>(macOS) / <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>B</kbd>(Windows)**.

  #### Computer Use in the browser
  - ChatGPT Work 또는 Codex가 내장 브라우저를 직접 조작 — 페이지 열기, 클릭, 타이핑, 렌더링 상태 검사, 스크린샷, 페이지에서 결과 검증.
  - **설정:** ChatGPT 선택 후 스위처에서 Work 켜기 또는 Codex 선택 → **Plugins Directory**에서 **Browser** 설치 → 작업에서 브라우저 사용을 요청하거나 **`@Browser`** 로 직접 참조.
  - **권한:** "ChatGPT asks before it uses a website **unless you have already allowed that site.**" 허용·차단 사이트는 **Settings > Browser**에서 관리. "ChatGPT also asks for confirmation before **sensitive actions such as submitting information, making a purchase, changing permissions, or deleting data.**" **"ChatGPT can't automate file uploads in the built-in browser."**
  - **원문 경고:** "**Instructions on a page can be misleading or malicious.** A website permission lets ChatGPT interact with that site; **it doesn't make the site's content trustworthy or approve every action.**"

  #### 페이지 미리보기 5단계 (원문)
  ① 통합 터미널 또는 로컬 환경 액션으로 앱의 개발 서버 시작 → ② URL 클릭 또는 수동 내비게이션으로 로컬 라우트·파일 기반 페이지·공개 페이지 열기 → ③ 렌더링 상태를 **코드 diff와 나란히** 검토 → ④ 변경이 필요한 요소·영역에 **브라우저 코멘트** 남기기 → ⑤ ChatGPT에게 코멘트 처리를 요청하고 범위를 좁게 유지

  #### 페이지 코멘트(Annotation)
  ① **Annotation mode** 켜기 → ② 요소 클릭 또는 드래그로 영역 선택 → ③ 코멘트 작성·저장 → ④ 채팅에서 코멘트 처리를 요청
  - **Styling feedback:** 섹션에 주석을 추가할 때 텍스트 입력 옆 **Adjust**를 선택하면 폰트·텍스트·간격·색 등 값을 바꾸고 페이지에서 결과를 미리 본 뒤 더 명확한 대상으로 주석을 보낼 수 있다.
  - **브라우저 작업 범위 유지 원칙 (원문):** 페이지·라우트·URL 이름 대기 / 관심 있는 상태(loading, empty, error, success) 명시 / 변경이 필요한 정확한 요소·영역에 코멘트 / ChatGPT 완료 후 페이지 재검토 / 로컬 페이지를 열기 전에 개발 서버를 시작하거나 확인하도록 요청

  #### Developer mode (CDP)
  - Chrome과 내장 브라우저의 Computer Use와 함께 동작. **Chrome DevTools Protocol(CDP)** 에 통제된 접근을 부여 — JavaScript 프로파일링, 콘솔 출력·네트워크 트래픽 검사, DOM·적용 스타일 조사, 라이브 브라우저 이슈 진단.
  - **활성화:** **Settings > Browser**(딥링크 `codex://settings/browser-use`)의 **Developer mode**에서 **Enable full CDP access** 켜기.
  - **관리자 차단:** "Admins can set **`browser_use_full_cdp_access = false`** under **`[features]`** in **`requirements.toml`** to disable full CDP access and prevent users from enabling the corresponding setting."
  - **경고(원문):** "**Full CDP access can expose sensitive browser internals.** ChatGPT asks for **explicit approval** before it uses full CDP to inspect a website."
  - **호출:** 내장 브라우저는 **`@Browser`**, Chrome에서 Developer mode를 쓰려면 Chrome 확장을 설정하고 **`@Chrome`** 호출.

  ### 웹 — 클라우드 운영 브라우저
  - ChatGPT Work on the web에서 ChatGPT가 **클라우드에서 운영되는 브라우저**로 공개 웹사이트를 조사·상호작용. "It runs separately from the browser on your device, so you can delegate web tasks **without giving ChatGPT access to your open tabs or personal browser history.**"
  - **시작 4단계:** ① **ChatGPT** 선택 → 스위처에서 **Work** 전환 → 원하는 결과 서술(관련 웹사이트·제약 포함) → ② ChatGPT가 웹사이트를 필요로 하면 사이트 접근 요청을 검토 후 허용 → ③ 채팅에서 브라우저 진행 상황 확인, **Cloud browser**를 열어 페이지 스크린샷과 리플레이 검사 → ④ 정보를 쓰기 전에 결과와 출처 검토
  - **웹사이트 권한 3단계(원문):** ChatGPT 설정의 **Cloud browser**에서 관리. **Always ask** / **Auto approve** / **Always allow** 중 선택하고 개별 사이트를 허용·차단. **"Auto approve lets ChatGPT approve requests after its risk checks; Always allow removes that review step for website access. Use the least-permissive setting that works for your task."**
  - "The permission applies to the **site shown in the request**, so **check the hostname** before allowing it." / "**A website permission doesn't approve every action.** ChatGPT may ask separately for permission before performing consequential actions."
  - **브라우저 데이터:** 클라우드 브라우저는 쿠키·브라우저 데이터를 기기와 분리 보관. 클라우드 브라우저 데이터를 지워도 기기 쿠키는 지워지지 않는다. 쿠키 제거는 ChatGPT 설정 **Cloud browser** → **Browser data** → **Clear all**. **"Don't rely on open pages or browser history being available in a later chat."**
  - **한계 (원문 목록):**
    - "The browser supports **public, signed-out websites.** It **can't sign in to an account**, ask for credentials, or use the signed-in session from your browser."
    - "Some sites **block automated browsers or require a CAPTCHA.**"
    - "The browser is separate from the browser on your device. It can't use your **open tabs, extensions, saved passwords, or local browser history.**"
    - "Availability can depend on your plan, workspace settings, and rollout. **It is available in all regions on paid plans other than Free and Go.** **Enterprise admins must enable it for their workspace.**"
    - "During rollout, the browser might not appear immediately even when your plan supports it."
- 명령·플래그·설정 키: `@Browser`, `@Chrome`, <kbd>Cmd/Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>B</kbd>, **Annotation mode**, **Adjust**, **Settings > Browser**, `codex://settings/browser-use`, `browser_use_full_cdp_access = false` under `[features]` in `requirements.toml`, **Cloud browser > Browser data > Clear all**
- 수치·요금·모델명·버전: 클라우드 브라우저는 **Free·Go를 제외한 유료 플랜의 전 지역**에서 사용 가능(2026-08-02 기준). 자료 10 기준 브라우저 사용 속도 **최대 2배** 개선(2026-06).
- 코드 예시 요지 (원문 그대로):
  - `Use the browser to open http://localhost:3000/settings, reproduce the layout bug, and fix only the overflowing controls.`
  - `I left comments on the pricing page in the built-in browser. Address the mobile layout issues and keep the card structure unchanged.`
  - 코멘트 예시: `This button overflows on mobile. Keep the label on one line if it fits, otherwise wrap it without changing the card height.` / `This tooltip covers the data point under the cursor. Reposition the tooltip so it stays inside the chart bounds.`
  - Developer mode: `This app is slow. Use @Browser to capture a performance trace and inspect network traffic, then identify the bottleneck.`
  - 클라우드 브라우저: `Compare the publicly listed prices and cancellation terms for these three venues. Return a table with links to each source and flag anything that needs a phone call to confirm.`
- 제약·주의사항: 내장 브라우저는 **파일 업로드 자동화 불가**. 클라우드 브라우저는 **로그인 불가**. CLI·IDE 미지원.
- 관련 섹션: 브라우저 장. **"페이지 내용은 신뢰할 수 없는 컨텍스트"** 원칙은 프롬프트 인젝션 절의 핵심 인용.
- Claude Code 대응 관점 메모: Claude Code의 **Claude in Chrome**(브라우저 확장)과 **chrome-devtools MCP**가 대응. 내장 브라우저 ↔ Claude Code에는 대응 없음(항상 사용자 Chrome을 조작). **CDP 접근을 관리자가 `requirements.toml`로 차단할 수 있다**는 점은 Claude Code의 관리형 설정(managed settings)에 대응하는 발상. 주석(annotation) 기반 시각 피드백은 Codex 고유의 강점.

---

## 자료 31: Computer Use

- URL: https://learn.chatgpt.com/codex/computer-use
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "With Computer Use, ChatGPT can **see and operate graphical user interfaces** on macOS or Windows."
  - **가용성 (최상단 원문):** "**In supported regions**, Computer Use in the ChatGPT desktop app is available on **macOS and Windows** with **ChatGPT Work and Codex**. Install the **Computer Use plugin**. On macOS, grant **Screen Recording and Accessibility** permissions when prompted."
  - **언제 쓰나:** 커맨드라인 도구나 구조화된 통합으로 부족한 작업 — 데스크톱 앱 확인, 브라우저 사용, 앱 설정 변경, 플러그인으로 제공되지 않는 데이터 소스 작업, GUI에서만 발생하는 버그 재현.
  - **원문 경고:** "Because Computer Use can affect app and system state **outside your project workspace**, use it for **scoped tasks** and review permission prompts before continuing."
  - **설정:** ChatGPT 선택 후 Work 전환 또는 Codex 선택 → **Plugins > Computer Use** → 필요 시 **Install plugin** → **Enable** 표시되면 선택 → **Computer Use 서버와 스킬 토글 켜기** → **Try now**. 이후 **Settings > Computer use**에서 앱 접근 검토. 연결된 브라우저 컨트롤에는 **Manage** 액션이 표시되고, 향후 작업에 승인한 앱은 **Always-allowed apps** 섹션에 나타남.
  - **macOS 권한 2종 (원문):** **Screen Recording** — "so ChatGPT can see the target app." / **Accessibility** — "so ChatGGPT can click, type, and navigate."
  - **좋은 사용처 (원문 목록):** ChatGPT가 만들고 있는 macOS 앱·Windows 앱·iOS 시뮬레이터 플로우·기타 데스크톱 앱 테스트 / 웹 브라우저가 필요한 작업 / GUI에서만 나타나는 버그 재현 / UI 클릭이 필요한 앱 설정 변경 / 플러그인으로 접근 불가한 앱·데이터 소스의 정보 검사 / **macOS에서는 다른 일을 하면서 백그라운드로 범위가 좁은 작업 실행** / 여러 앱에 걸친 워크플로 실행
  - **로컬 웹앱은 내장 브라우저 우선:** "For web apps you are building locally, use the **built-in browser first.**"
  - **Windows 전경 사용 (원문, 중요):** "On Windows, Computer Use runs on the **active desktop**. It **can't operate in the background** while you keep using the same Windows session, so expect ChatGPT to **move the pointer, type, and take over the foreground** while the task runs."
    - 자리를 비운 채 계속하려면: Windows 기기를 잠금 해제·인터넷 연결 상태로 유지하고, 휴대폰에서 **remote control**로 진행 확인·후속 지시, 또는 **Windows 가상 머신 안에서 ChatGPT 데스크톱 앱을 실행**해 Computer Use가 주 데스크톱 대신 VM을 점유하게 한다.
  - **작업 시작:** 프롬프트에서 **`@Computer`** 또는 **`@AppName`** 을 멘션하거나 Computer Use를 쓰라고 요청. 조작할 정확한 앱·창·플로를 서술.
  - "If the target app exposes a **dedicated plugin or MCP server, prefer that structured integration** for data access and repeatable operations. Choose Computer Use when ChatGPT needs to **inspect or operate the app visually.**"

  ### 권한과 승인
  - "System permissions for Computer Use are **separate from** app approvals in ChatGPT." macOS의 Screen Recording·Accessibility는 보고 조작하게 하고, 앱 승인은 어떤 앱을 허용할지 정한다. **"File reads, file edits, and shell commands still follow the sandbox and approval settings for the task."**
  - 작업 중 ChatGPT는 컴퓨터의 앱을 쓰기 전에 권한을 묻는다. **Always allow**를 선택하면 이후 묻지 않는다. 데스크톱 앱 설정의 **Computer Use** 섹션에서 목록 제거 가능.
  - 문제 시: macOS는 **System Settings > Privacy & Security**에서 **Codex Computer Use**에 대한 **Screen Recording**·**Accessibility** 확인. Windows는 대상 앱이 활성 데스크톱 세션에 보이는지 확인.

  #### Windows 앱 정책 설정 (원문 코드)
  - Windows에서는 지속적 앱 결정을 **`$CODEX_HOME/config.toml`** 에 저장:
    ```toml
    [computer_use.windows]
    always_allowed_app_ids = ["mspaint.exe"]
    ```
  - "Use the app identifier that Windows Computer Use reports, such as an **executable name** for a desktop app or an **app user model ID** for a packaged app." 목록에 없는 앱은 프롬프트가 뜬다. 저장된 결정 취소는 **Settings > Computer Use > Always allow**에서 제거.
  - **"This table stores local Computer Use decisions. It's separate from the admin-enforced `requirements.toml`, where administrators can disable Computer Use with `[features].computer_use = false`."**
  - "Older **`$CODEX_HOME/computer-use/config.toml`** allow-list entries are **migrated** into the current setting; its **`denied` list isn't part of the current policy schema.**"

  ### Locked use (macOS 전용)
  - "Locked use is for macOS. On Windows, Computer Use works in the foreground."
  - Mac이 잠긴 후에도 Computer Use를 쓰게 하되 **명시적으로 켜야** 한다. 연결된 기기에서 시작한 작업이 Mac 잠금 후 데스크톱 앱을 써야 할 때 사용.
  - **"When you enable locked use, ChatGPT installs an Apple authorization plug-in that participates in the macOS unlock flow."**
  - **"Locked use is intentionally narrow. It's not a general-purpose remote-unlock path for your Mac, and it doesn't let other apps or local processes unlock the computer."**
  - 사용법: ① 앱의 **Settings > Computer Use** → ② locked use 활성화 → ③ Mac 화면이 잠긴 뒤 연결된 기기에서 Computer Use를 쓰는 작업 시작
  - 동작: 잠금 후 작업이 Computer Use로 앱에 접근하면 ChatGPT가 **로컬 사용을 차단하고 잠금 화면 보호를 유지한 채** Mac을 일시적으로 잠금 해제한다. 해제 전 그 시도가 **활성·신뢰된 Computer Use 턴을 위한 것인지** 확인하고, 그 짧은 창 밖에서는 잠금 해제를 거부하고 수동 해제를 요청한다.
  - **안전장치 4종 (원문):** 인가 창은 **수명이 짧고** 현재 잠금 해제 시도에 한정된다 / 자동 해제는 **활성 Computer Use 턴 동안 ChatGPT에만** 가능하다 / **ChatGPT가 임시 해제 동안 모든 디스플레이를 가린다** / **로컬 키보드·포인터 입력이 감지되면 Mac을 다시 잠그고** 수동 해제 전까지 자동 해제를 중단한다

  ### 안전 지침 (원문 — 보안 장 필수)
  - "ChatGPT can view screen content, take screenshots, and interact with **windows, menus, keyboard input, and clipboard state** in the target app. **Treat visible app content, browser pages, screenshots, and files opened in the target app as context ChatGPT may process while the task runs.**"
  - 원칙: 한 번에 하나의 명확한 대상 앱·플로만 / 언제든 작업 중지·컴퓨터 회수 가능 / 필요 없는 민감 앱은 닫아 둘 것 / **Windows에서는 전경 입력을 점유하므로 보조 기기·VM을 쓰거나 작업을 멈출 것** / 비밀정보가 필요한 작업은 각 단계를 승인할 수 있을 때만 / 앱 권한 프롬프트를 검토 후 허용 / **Always allow는 자동 사용을 신뢰하는 앱에만** / 계정·보안·프라이버시·네트워크·결제·자격증명 관련 설정에는 자리를 지킬 것 / 잘못된 창과 상호작용하기 시작하면 작업 취소
  - **브라우저 사용 시 경고(원문):** "If ChatGPT uses your browser, it can interact with pages **where you're already signed in.** Review website actions as if you were taking them yourself: web pages can contain malicious or misleading content, and **sites may treat approved clicks, form submissions, and signed-in actions as coming from your account.** To keep using your browser while ChatGPT works, ask ChatGPT to use a different browser."
  - **불가 사항(원문):** "The feature **can't automate terminal apps or ChatGPT itself**, since automating them could **bypass ChatGPT security policies.** It also **can't authenticate as an administrator or approve security and privacy permission prompts** on your computer."
  - "Changes made through desktop apps **may not appear in the review pane until they're saved to disk and tracked by the project.**"
- 명령·플래그·설정 키: `@Computer`, `@AppName`, `@Chrome`, `$CODEX_HOME/config.toml`, `[computer_use.windows]` / `always_allowed_app_ids`, `[features].computer_use = false`(requirements.toml), **Settings > Computer use**, **Always-allowed apps**, **System Settings > Privacy & Security**
- 수치·요금·모델명·버전: 자료 19 기준 **2026-07-09부터 GPT-5.6으로 Computer Use 고속화**. 자료 10 기준 Windows 지원은 2026-05, EEA·영국·스위스는 2026-06 롤아웃.
- 코드 예시 요지 (원문 그대로):
  - `Open the app with Computer Use, reproduce the onboarding bug, and fix the smallest code path that causes it. After each change, run the same UI flow again.`
  - `Open @Chrome and verify the checkout page still works after the latest changes.`
- 제약·주의사항: **지역 제한 있음**(자료 12 기능 매트릭스에서 전 플랜 △=limited, footnote "region"). 터미널 앱과 ChatGPT 자신은 자동화 불가. 관리자 권한 인증·보안 프롬프트 승인 불가.
- 관련 섹션: Computer Use 장 + 보안 장. Locked use의 안전장치 4종은 "AI에 컴퓨터를 맡긴다는 것"의 좋은 사례 연구.
- Claude Code 대응 관점 메모: Claude Code에 **GUI 조작 대응 없음**(Claude in Chrome은 브라우저 한정). Computer Use는 Codex가 "코딩 에이전트"를 넘어 "컴퓨터 에이전트"로 확장한 지점이며, 이 책의 핵심 차별 서사가 될 수 있다. `$CODEX_HOME` ↔ `CLAUDE_CONFIG_DIR`. `requirements.toml`의 `[features]` 차단 ↔ Claude Code managed settings의 permission deny.

---

## 자료 32: ChatGPT Voice

- URL: https://learn.chatgpt.com/codex/features/voice
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "**Powered by GPT-Live**, ChatGPT Voice lets you talk through ideas and coordinate tasks in **Chat, Work, and Codex** in the ChatGPT desktop app. Start work, check progress, or change direction without switching back to typing."
  - **가용성 (원문):** ChatGPT 데스크톱 앱에서 **Plus, Pro, Business, Edu, Enterprise** 플랜. **"Enterprise and Edu availability begins with a two-week early-access period before the feature becomes available by default."** **Remote on iOS**를 통해서도 사용 가능(휴대폰을 데스크톱 호스트와 페어링한 후). 롤아웃 상태와 워크스페이스 설정에 따라 다름.
  - **시작 4단계:** ① 데스크톱 앱에서 **새로 비어 있는 채팅이나 태스크** 열기 → ② 메시지를 보내기 **전에** **Start new voice chat** 선택 → ③ 최초 실행 시 마이크 접근 허용, 음성 선택, macOS에서는 화면 컨텍스트 검토 → ④ 말하기 시작. 끝나면 **End** 선택.
  - **핵심 제약(원문):** "**A chat or task must begin in voice mode to use ChatGPT Voice.** Chats or tasks that start in another mode offer **voice dictation** instead." 이전 음성 채팅을 재개하려면 열고 **Start voice chat** 선택.
  - 단축키: **Settings > Voice > Voice chat hotkey**.
  - **대화:** "ChatGPT Voice supports **natural turn-taking**. You can **interrupt** ChatGPT during a response, ask a follow-up, or change direction. If ChatGPT starts work, keep talking to check progress or steer the task."
  - **위임·조율:** "ChatGPT Voice can **start separate threads** for longer tasks, **check existing threads**, and **send follow-up instructions.** It brings progress, blockers, and results back to your voice conversation so you can keep talking while work continues."
    - 원문 예시: "Review today's launch brief and summarize decisions that need approval." / "Start a Codex task to run the tests and investigate anything that doesn't pass." / "Check active tasks and summarize anything blocking progress."
  - **권한:** "ChatGPT Voice follows the **same permissions** as the tasks it directs in Chat, Work, and Codex in the ChatGPT desktop app."
  - **Screen context (macOS):** **Settings > Voice**에서 **Screen context**를 켜고 "Take a look at this."라고 말하면 ChatGPT가 최전면 창의 **appshot**을 찍어 컨텍스트로 사용. **"Your organization can disable this capability."**
    - **주의(원문):** "An appshot can include the window's image and **accessible text, including content outside the visible scroll area.**" macOS가 **Screen & System Audio Recording**과 **Accessibility** 권한을 요청할 수 있음. **"Avoid sharing windows that contain sensitive information, including text outside the visible scroll area."**
  - **Voice vs 음성 받아쓰기:** "Use ChatGPT Voice for a **live conversation**. Use **voice dictation** when you only want to **turn speech into prompt text before sending it.**"
  - **한계·문제 해결:** **"Only one voice chat can be active across the ChatGPT desktop app at a time."** 음성 대화는 **롤링 5시간 창**으로 측정되는 별도의 플랜 의존 허용량을 쓴다. **"Tasks started through Voice continue to use your Codex usage budget."** 어느 한도에 도달하면 알림. 음성 채팅을 시작할 수 없으면 플랜·롤아웃·워크스페이스 가용성 확인 → 마이크 권한과 다른 앱 창에서 음성 채팅이 이미 활성인지 확인. 화면 컨텍스트가 안 되면 **Settings > Voice**, Appshots 권한, 조직 제한 확인.
- 명령·플래그·설정 키: **Start new voice chat**, **Start voice chat**, **End**, **Settings > Voice**, **Voice chat hotkey**, **Screen context**
- 수치·요금·모델명·버전 (**자료 12와 교차 확인**):
  - 엔진: **GPT-Live**(라이브 대화) + **GPT-5.6 Terra**(앱 내 태스크 시작·조율) — **duplex model**
  - 허용량: **Plus 약 15–30분 / Pro 5x($100) 약 1–2.5시간 / Pro 20x($200) 무제한 / Business 약 45분 / Enterprise·Edu(legacy) 약 45분**, 모두 **롤링 5시간 창** 기준
  - 크레딧 기반 워크스페이스: **분당 약 6 크레딧**
  - **API Key로는 사용 불가**
  - Enterprise·Edu는 **2주 얼리 액세스** 후 기본 제공
- 코드 예시 요지: 위 음성 명령 예시 3종
- 제약·주의사항: 한 번에 하나의 음성 채팅만. 채팅을 반드시 음성 모드로 **시작**해야 함(중간 전환 불가). 무제한 음성이 무제한 태스크를 뜻하지 않음.
- 관련 섹션: 음성 장. duplex 모델(GPT-Live + Terra) 구조는 기술적으로 흥미로운 디테일.
- Claude Code 대응 관점 메모: **Claude Code에 대응 없음.** 다만 "음성으로 여러 스레드를 조율한다"는 개념은 Claude Code의 병렬 에이전트 관리와 문제의식이 같다 — Codex는 이를 **음성 인터페이스**로, Claude Code는 **텍스트 오케스트레이션**으로 푼다.

---

## 자료 33: Plugins

- URL: https://learn.chatgpt.com/codex/plugins
- 검색: 2026-08-02 기준
- 신뢰성: 최상
- 핵심 내용: "Plugins bundle capabilities into reusable workflows in ChatGPT and Codex. They can include **skills, connectors, or both.** Both products use **one universal plugin directory.**"
  - **표면별 가용성 (원문, 중요):** "Plugins are available with **ChatGPT Work on the web** and with **ChatGPT Work or Codex in the ChatGPT desktop app.** **Codex CLI** also has a plugin browser for Codex environments. **Plugins aren't available in Chat, the IDE extension, or mobile.**"
  - **플러그인 구성 6종 (원문 정의 그대로):**
    - **Skills:** "reusable instructions for specific kinds of work. ChatGPT and Codex can load them when needed so they follow the right steps and use the right references or helper scripts for a task."
    - **Connectors:** "connections to tools like GitHub, Slack, or Google Drive... **Connectors expose tools and can optionally include custom UI.**"
    - **MCP servers:** "services that give ChatGPT and Codex access to more tools or shared information, often from systems outside your local project. **They're also the services behind connectors.** They define tools, enforce auth, return structured data, and perform actions against external systems."
    - **Browser extensions:** "browser capabilities that a plugin needs for its workflow."
    - **Hooks:** "commands that run at configured lifecycle points. **Review and trust plugin hooks before you enable them.**"
    - **Scheduled task templates:** "reusable starting points for recurring tasks where scheduled tasks are available."
  - 예시 플러그인(원문): **Codex Security**(승인된 코드를 스캔하고 그럴듯한 취약점 발견을 확인), **Gmail**, **Google Drive**(Drive·Docs·Sheets·Slides 전반), **Slack**(채널 요약, 답장 초안)
  - **Plugins Directory 탭 구성 (원문):** **OpenAI**(OpenAI가 만든 플러그인) / **{워크스페이스 이름}**(워크스페이스 제공) / **Personal**(개인 마켓플레이스 — **Created by me**, **Shared with me** 섹션 포함). 별도 **Installed** 행으로 설치된 플러그인 검토.
  - **설치 4단계:** ① 검색·탐색 후 상세 열기 → ② **플러스 버튼**으로 설치 → ③ 커넥터가 필요하면 프롬프트에 따라 연결(**"Some plugins ask you to authenticate during install. Others wait until the first time you use them."**) → ④ 설치 후 **새 채팅을 시작**하고 플러그인 사용을 요청
  - **사용 2방식:** **과제를 직접 서술**("Summarize unread Gmail threads from today", "Pull the latest launch notes from Google Drive") — ChatGPT가 알맞은 설치 도구를 고르게 할 때 / **특정 플러그인 선택** — `@`를 입력해 플러그인이나 번들 스킬을 명시 호출
  - **CLI 플러그인 브라우저:**
    ```text
    codex
    /plugins
    ```
    - "The CLI plugin browser **groups plugins by marketplace.** Use the marketplace tabs to switch sources, open a plugin to inspect details, install or uninstall marketplace entries, and press <kbd>Space</kbd> on an installed plugin to **turn it on or off.**"
  - **API 키 가용성 (원문):** "If you sign in to Codex with an OpenAI API key, you can browse, install, and manage **supported OpenAI-curated plugins** in Codex CLI and Codex in the ChatGPT desktop app. **Some plugins aren't available with API key authentication because their connection flows require unsupported OAuth capabilities.**" 사용량은 Platform Usage 페이지에서 검토.
  - **권한·데이터 공유:**
    - 웹: ChatGPT Work 채팅은 그 채팅에 가용한 워크스페이스 권한·도구를 쓴다. **"Connectors still require their own sign-in and access."**
    - 데스크톱·CLI: "When a plugin capability runs through a Codex host, **the host's sandbox and approval policy applies.** Connections to external services use **that service's own authentication and access controls.**"
    - 공통: 번들 스킬은 **설치 후 새 채팅/CLI 세션을 시작해야** 사용 가능 / 커넥터가 포함되면 설정 중이나 최초 사용 시 설치·로그인 요구 / MCP 서버가 포함되면 추가 설정·인증이 필요할 수 있음 / **"When ChatGPT sends data through a bundled connector, that service's terms and privacy policy apply."**
  - **제거:** 지원되는 플러그인 브라우저에서 열고 **Uninstall plugin** 선택(가능한 경우). **"Workspace-installed or default plugins may not offer that action; your workspace administrator controls them instead."** **"Uninstalling a plugin removes the plugin bundle from that ChatGPT or Codex environment, but bundled connectors stay connected until you manage them in ChatGPT."**
  - 배포: 마켓플레이스 소스(프로젝트·팀용 repo 마켓플레이스 등)로 게시해 공유.
  - 플러그인 가이드: **Record & Replay**("Show ChatGPT a workflow once and turn it into a reusable skill."), **Codex Security plugin**("Scan authorized code, confirm findings, and prepare reviewed fixes.")
- 명령·플래그·설정 키: `/plugins`(CLI), `@`(플러그인·스킬 명시 호출), <kbd>Space</kbd>(CLI 브라우저에서 활성 토글), **Uninstall plugin**
- 수치·요금·모델명·버전: 자료 12 기준 Plugins는 Plus·Pro·Business·Enterprise ✅, **API Key는 △**(일부 1st-party 플러그인 불가). Plugins 출시 = 2026-03-25(자료 19).
- 코드 예시 요지: 위 `codex` → `/plugins`
- 제약·주의사항: **Chat, IDE 확장, 모바일에서 사용 불가.** 훅은 신뢰 검토 후 활성화할 것. 플러그인 제거해도 번들 커넥터는 연결 유지.
- 관련 섹션: 확장 장. **6종 구성요소 정의는 Claude Code 플러그인과 1:1 비교표로 만들기 좋다.**
- Claude Code 대응 관점 메모: Claude Code Plugin과 구성이 거의 동형이다 — skills / MCP servers / hooks / (subagents). **Codex에만 있는 것: Connectors**(MCP 위에 얹은 인증·UI 계층), **Browser extensions**, **Scheduled task templates**. **Claude Code에만 있는 것: 슬래시 커맨드, 서브에이전트를 플러그인 구성요소로 직접 노출.** `/plugins` 명령어 이름은 **양쪽 동일**. "마켓플레이스별 그룹핑"도 Claude Code의 plugin marketplace와 동형.

---

## 접근 실패 URL

지시된 33개 URL 중 **31개는 `.md` 원문으로 손실 없이 수집**했고, 나머지 2개는 `.md`가 제공되지 않아 **대체 경로로 내용을 확보**했다. **완전 실패(내용 미확보)는 0건이다.**

| # | URL | 증상 | 대응 | 최종 상태 |
|---|---|---|---|---|
| 1 | `https://learn.chatgpt.com/codex` | `/docs`로 리다이렉트 후 `/docs/overview.md`는 **200이지만 본문이 `<CodexOverviewLanding />` 컴포넌트 한 줄**(219바이트). `/docs/index.md`·`/docs/codex.md`는 404 | 렌더링된 HTML에서 카드·사이드바 텍스트 확인 | **부분 확보** — 자료 1. 산문 본문이 애초에 없는 랜딩 페이지이므로 누락된 정보 없음 |
| 2 | `https://learn.chatgpt.com/codex/changelog` | `/docs/changelog`로 리다이렉트되나 **`.md`가 404**(`/docs/codex/changelog.md`, `/docs/releases.md`도 404) | HTML(432KB)을 받아 `<main>` 텍스트 추출(72KB) | **완전 확보** — 자료 19. 95개 항목 전수 색인 + 주요 항목 원문 |

### 자리표시자(placeholder) 점검 결과
리서치 리드 지시에 따라 그룹 A 전 파일을 `ConfigTable` / `astro-island` 자리표시자 잔존 여부로 점검했다.

- **`ConfigTable` 발견: 0건. `astro-island` 잔존: 0건.** 그룹 A는 `astro-island` props 디코딩이 **불필요**하다.
- 표 데이터는 세 형태로 `.md` 안에 **실제로 들어 있다**:
  - **인라인 HTML `<table>`** — `codex__pricing.md`에 6개(플랜별 사용량 한도 5개 + 크레딧 요율표 1개). 수치 전부 존재.
  - **마크다운 파이프 표** — `codex__feature-maturity.md`(성숙도 4등급) 등
  - **JSX props 안의 데이터 리터럴** — `codex__models.md`의 `<ModelDetails data={{...}}/>`, `codex__pricing.md`의 `<CodexPlanFeatureMatrix data={{...}}/>`, `codex__glossary.md`의 `<GlossaryTable options={[...]}/>`. **자리표시자가 아니라 데이터가 그대로 들어 있으며, 본 문서에 표로 복원 완료.**
- **유일한 실질 손실:** `/codex/permission-modes`의 `<PermissionModeSelectorDemo client:load />` 는 props가 비어 있고 데이터가 컴포넌트 코드 안에 있다. HTML 서버 렌더링에서 회수한 것:
  - 4개 모드명 전부: **Ask for approval / Approve for me / Full access / Custom (config.toml)**
  - 각 모드의 컴포저 메뉴 설명문(자료 9에 반영)
  - **`Ask for approval` 모드의 설정 3종만** 회수: `Sandbox = workspace-write`, `Approvals policy = on-request`, `Reviewer = user`
  - **미회수:** `Approve for me` / `Full access` / `Custom` 모드의 Sandbox·Approvals policy·Reviewer 값. JS 청크 6개를 받아 검색했으나 발견하지 못했다. **추측하지 않고 공백으로 남긴다.** → **그룹 B 담당의 `/codex/sandboxing`·`/codex/permissions`에서 보완 필요.**

### 리서치 리드 질의에 대한 확정 답변
1. **`/codex/pricing`에 수치가 있는가 → 있다.** 플랜 가격 6종, 플랜×모델 사용량 한도 표 5탭(각 6모델 × 3열), 크레딧 요율표 9행 × 3열, 음성 허용량 5플랜, 기능 가용성 매트릭스 7섹션이 모두 원문에 존재하며 본 문서에 전수 전사했다. 범위 값(`10-100` 등)은 범위 그대로 보존했다.
2. **`/codex/feature-maturity`에 기능별 등급 목록이 있는가 → 없다.** 4등급 정의 표만 존재(전체 1.7KB). 기능별 라벨은 각 기능 문서에 인라인 문구로 흩어져 있으며, 그룹 A에서 확인된 7개 사례를 자료 20에 정리했다. **문서가 정의한 4등급명과 실제 사용 라벨("research preview", "public beta", "preview")이 일치하지 않는다는 점**을 함께 기록했다.
3. **모델명 불일치 → `/codex/models`를 정전으로 확정.** `gpt-5.6-sol`/`gpt-5.6-terra`/`gpt-5.6-luna`가 정식 ID이며, `5.6 Sol Extended`는 삽화 속 UI 문자열로 본문에 정의된 티어명이 아니다(자료 11에 판정 기록).
4. **GPT-5.4 은퇴(2026-08-31) 정합성 → 3중 일치.** `/codex/models`, `/codex/changelog`(2026-07-31 항목), `/codex/automations` 모두 동일 날짜·동일 대체 모델을 명시한다. `/codex/whats-new`에만 언급이 없으나 이는 **모순이 아니라 누락**이다.

---

## 추가 발견 URL

지시된 33개 목록에 없으면서 `/docs/` 사이트맵(125개) 또는 수집한 문서 본문의 링크에서 발견된 경로다. **방문은 하지 않았고 목록만 남긴다.** (사이트맵 전체 246 URL 중 `/docs/` 125개 기준, 33개 목록과 차집합 93개 + 본문 링크에서만 발견된 5개 = **98개**)

### 사이트맵에 있으나 미지정 (93개)

**에이전트 설정·확장**
`/codex/agent-configuration/agents-md` · `/codex/agent-configuration/rules` · `/codex/agent-configuration/speed` · `/codex/agent-configuration/subagents` · `/codex/build-skills` · `/codex/build-plugins` · `/codex/extend/mcp` · `/codex/extend/record-and-replay` · `/codex/hooks` · `/codex/custom-prompts` · `/codex/mcp-server`

**설정 파일**
`/codex/config-file/config-basic` · `/codex/config-file/config-advanced` · `/codex/config-file/config-reference` · `/codex/config-file/config-sample` · `/codex/config-file/environment-variables` · `/codex/configuration` · `/codex/cli-customization`

**권한·샌드박스·보안**
`/codex/agent-approvals-security` · `/codex/sandboxing` · `/codex/sandboxing/auto-review` · `/codex/permissions` · `/codex/security-administration` · `/codex/cyber-safety` · `/codex/security` · `/codex/security/setup` · `/codex/security/faq` · `/codex/security/threat-model` · `/codex/security/sdk` · `/codex/security/cli` · `/codex/security/cli/bulk-scans` · `/codex/security/cli/ci` · `/codex/security/cli/faq` · `/codex/security/cli/reference` · `/codex/security/plugin` · `/codex/security/plugin/changelog` · `/codex/security/plugin/code-changes` · `/codex/security/plugin/deep-scans` · `/codex/security/plugin/export-findings` · `/codex/security/plugin/fix-findings` · `/codex/security/plugin/scans` · `/codex/security/plugin/security-hardening` · `/codex/security/plugin/triage-backlog` · `/codex/security/plugin/vulnerability-reports` · `/codex/security/plugin/workbench`

**환경·실행**
`/codex/environments/modes` · `/codex/environments/local-environment` · `/codex/environments/cloud-environment` · `/codex/environments/git-worktrees` · `/codex/cloud/internet-access` · `/codex/integrated-terminal` · `/codex/non-interactive-mode` · `/codex/remote-connections`

**기능(자료 22의 Features 색인에 등장)**
`/codex/sites` · `/codex/web-search` · `/codex/image-generation` · `/codex/image-inputs` · `/codex/appshots` · `/codex/chrome-extension` · `/codex/artifacts-viewer`(Work with files) · `/codex/code-review` · `/codex/visualizations`(지정됨) · `/codex/customization/overview` · `/codex/customization/memories` · `/codex/customization/chronicle`

**SDK·통합·플랫폼**
`/codex/codex-sdk` · `/codex/app-server` · `/codex/github-action` · `/codex/third-party/github` · `/codex/third-party/linear` · `/codex/third-party/slack` · `/codex/amazon-bedrock` · `/codex/auth` · `/codex/developers` · `/codex/administration`

**Windows**
`/codex/windows/windows-app` · `/codex/windows/windows-sandbox` · `/codex/windows/wsl`

**엔터프라이즈 (15개)**
`/codex/enterprise/access-tokens` · `/codex/enterprise/admin-setup` · `/codex/enterprise/analytics-api` · `/codex/enterprise/apps-and-connectors` · `/codex/enterprise/compliance-api` · `/codex/enterprise/governance` · `/codex/enterprise/groups-and-provisioning` · `/codex/enterprise/managed-configuration` · `/codex/enterprise/roles-and-workspace-permissions` · `/codex/enterprise/skills` · `/codex/enterprise/usage-limits` · `/codex/enterprise/windows-deployment` · `/codex/enterprise/work-admin-faq` · `/codex/enterprise/workspace-analytics` · `/codex/enterprise/workspace-model-availability`

**기타**
`/codex/reference/troubleshooting`

### 본문 링크에서만 발견 (사이트맵 미등재, 5개)
`/codex/developer-commands` · `/codex/developer-settings` · `/codex/reference/commands` · `/codex/reference/slash-commands` · `/codex/reference/settings`

> **주의:** 뒤 3개는 자료 22의 Features 색인이 명시적으로 가리키는 문서인데 사이트맵에 없다. 존재 여부를 실제 요청으로 확인해야 한다. `/codex/developer-commands?surface=cli`·`?surface=ide`는 CLI/IDE 명령 레퍼런스로 여러 문서가 참조하므로 **책의 CLI 장에 필수적**이다.

### `/docs/` 밖의 참조 경로 (별도 섹션 구조)
- `https://learn.chatgpt.com/use-cases` 및 개별 유스케이스(`/use-cases/daily-work-brief`, `/use-cases/analyze-data-export`, `/use-cases/draft-prds-from-sources`, `/use-cases/clean-messy-data`, `/use-cases/feedback-synthesis`, `/use-cases/make-granular-ui-changes`, `/use-cases/scan-code-changes-for-security` 등 — 사이트맵 246개 중 `/docs/` 125개를 뺀 121개 대부분이 여기)
- `https://learn.chatgpt.com/guides/best-practices` (CLI·IDE 문서가 "Read the best practices"로 링크)
- `https://learn.chatgpt.com/llms.txt` (전체 문서 색인, 1,787줄)
- 외부: `https://developers.openai.com/plugins/build/plugins` · `/plugins/build/mcp-server` · `/plugins/build/chatgpt-ui` · `/plugins/deploy/submission` · `/community/codex-for-oss` · `https://openai.com/academy/skills/` · `https://academy.openai.com/home/courses/ai-foundations-juzjs`

---

## 수집 한계 및 후속 과제

1. **`/codex/permission-modes`의 모드별 설정값 3/4 미확보.** `Ask for approval` 외 3개 모드의 Sandbox·Approvals policy·Reviewer 값은 클라이언트 컴포넌트 내부에 있어 회수하지 못했다. **추측으로 채우지 않았다.** → 그룹 B의 `/codex/sandboxing`, `/codex/permissions`, `/codex/agent-approvals-security`에서 확보해야 한다.
2. **`/codex/changelog`는 `.md`가 없다.** HTML 추출본에 의존하므로 서식·강조가 일부 손실됐다. 95개 항목의 날짜·제목은 전수 확보했으나, **본문 상세는 2026년 6~7월 위주로만 전사**했다. 2025년 항목의 본문 상세가 필요하면 재추출이 필요하다.
3. **한국 지역 가용성은 문서에 명시가 없다.** 지역 제한 언급은 EEA·영국·스위스에 대해서만 반복 등장한다. "한국에서는 쓸 수 있다/없다"를 문서 근거로 단정할 수 없다 — 책에서 서술하려면 별도 확인이 필요하며, **현 시점에서는 "공식 문서에 한국 관련 명시 없음"이 유일하게 확정 가능한 진술**이다.
4. **데스크톱 앱 버전 체계(`26.727` 등)의 의미가 문서에 정의돼 있지 않다.** 날짜 기반으로 보이나 확인된 바 없어 추정을 기록하지 않았다.
5. **Codex CLI 슬래시 커맨드 전체 목록은 그룹 A에 없다.** 본 문서에서 확인된 것은 여러 페이지에 흩어진 `/permissions` `/model` `/review` `/new` `/resume` `/plugins` `/pets` `/pet` `/goal` `/plan` `/status` `/mention` `/side` `/init` 14종이다. 정식 전수 목록은 `/codex/developer-commands?surface=cli`에 있을 것으로 보이며 **미방문**이다.
6. **Sites, Web search, Image generation, Appshots, Chrome extension, artifacts-viewer**는 자료 22의 기능 색인에서 존재가 확인됐으나 그룹 A 지정 범위 밖이라 본문을 수집하지 않았다. 책의 기능 커버리지를 위해 다른 그룹의 수집 결과와 합류해야 한다.
