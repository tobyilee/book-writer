## 7장 (라운드 1)

### ❌ 정정
- PwC "Is Grep All You Need?" 단락: "2차 해설을 보면 … 원문을 대조하지 못했고 … 구체 수치는 `(사실 확인 필요)`로 남긴다" → 원문 대조 완료로 재서술. arXiv 2605.15184(2026-05-14, v1) 실재 확인, 저자 Sen·Kasturi·Lumer·Gulati·Subbiah, 소속 "PricewaterhouseCoopers, U.S." 명시; 인용구 "shifts the ceiling by roughly as much as swapping retrievers within a fixed harness" 원문 일치; 인라인 호출 10/10 grep 우세·파일 기록 호출 5/10 역전 원문 일치("inline grep exceeds inline vector for every harness–model pair" / "programmatic vector exceeds programmatic grep on five of ten harness–model pairs"). 신뢰구간 없음 확인. "하네스에서는"을 "호출 방식에서는"으로 — 논문은 인라인/파일을 하네스 속성이 아닌 tool-calling 방식으로 다룸. 표 불일치(76.7% vs 94.0%)는 LatentEval 해설의 지적이므로 수치는 싣지 않음 — 근거: arxiv.org/html/2605.15184, latenteval.ai 해설(W44), 원장 F7
- llmwiki MCP 도구 목록 "`read`, `search`, `lint`에 `create`·`edit`·`append`·`delete`까지 여덟 개" → `guide` 추가(일곱 개만 열거하고 여덟이라 셈) — 근거: 01_reference 6.3 [W8]
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — Taktile "2026년 7월·자기 보고", Contextual Retrieval "2024년 기준·Claude 3 세대", qmd "2026년 10월 11일 기준", Claude Code MCP 문서 "2026년 10월 열람", Crosley "일자 미확인"이 이미 명기됨)
### ✅ 확인 (요약)
- 수치 14건: Taktile 24쿼리·88항목·69.1초·0.47ms·K=3 약 1/5(자기 보고 명기) / IRCoT +21·+15 / Contextual Retrieval 35%·49%·67%(5.7→3.7→2.9→1.9) / LC vs RAG 13.1%·7.6%·65%·39%·−0.2~−2.2% / WUPHF recall@20 85%·clue.oz4e recall@5 93%(자기 보고 명기) / 우아한형제들 약 15% / qmd ★30.3k·900토큰·15%·300MB·640MB·1.1GB / Jim Liu 35페이지·40~50ms·500페이지 / bitsofchris 4,000+ — 01_reference 6.1·6.2, community.md와 일치
- 인용·귀속 13건: ReAct "a simple Wikipedia API" / IRCoT 원문 / gist "surprisingly well"·"~100 sources, ~hundreds of pages"·"reads the index first…" / rohitg00 "100-200 pages" / 클리앙 "별 부족함이 없었" / AI매터스 / jermolene·0xjaishy·clue.oz4e / Anthropic "glob and grep"·"just-in-time" / softwaredoug / Crosley / kurthong / mosfet1kg / 우아한형제들 2건 / Claude Code MCP 문서 4건 — 원문 발췌와 일치
- 식별자·버전 7건: arXiv 2212.10509(ACL 2023)·2210.03629(ICLR 2023)·2407.16833(EMNLP 2024 Industry)·2605.15184(웹 확인) / qmd MIT·Node 22+·Bun 1.0+·`npm install -g @tobilu/qmd` / `claude mcp add --transport http` 구문 — 일치
- 사용 금지 항목 F3·F9·F12·F19("500배"·"4명 중 1명") 부재 확인; gist 귀속 규모 수치는 "~100 sources" 외에 경험치로 구분 표기됨(F4·F39)
### 미해소
- (없음)

## 8장 (라운드 1)

### ❌ 정정
- Agent SDK 인증 인용 "Anthropic does not allow third party developers to offer claude.ai login…" → 원문 첫 구 "Unless previously approved, " 복원 — 생략하면 절대 금지로 읽혀 원문 뜻이 달라짐 — 근거: web.md 자료 26 [W26]
- Files API 단락의 구 베타 헤더 문자열 `files-api-2025-04-14` 삭제 → "구 자료에 나오는 베타 헤더는 더 이상 쓰지 않는다" — 원장 F12 사용 금지 항목(GA, 베타 헤더 불필요) — 근거: 01_reference 4.2 [W19]
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- Python·TS 코드 `claude-sonnet-5-5` 주석: `(사실 확인 필요)` 해소 → "2026년 10월 기준 공식 모델 ID" — 웹 확인: platform.claude.com/docs/en/models/overview 모델 표의 Claude API ID `claude-sonnet-5-5`(Sonnet 5.5) 일치; claude-api 스킬 모델 표(2026-10-06 캐시)와도 일치
- TS `cache_control: { type: "ephemeral", ttl: "1h" }` 주석: 마커 해소 → "2026년 10월 캐싱 문서 기준" — 웹 확인: Prompt caching 문서 예제 `"cache_control": {"type": "ephemeral", "ttl": "1h"}` 일치
### ✅ 확인 (요약)
- API 형태(Critical, 웹 2차): 인라인 텍스트 문서 `{type:"document", source:{type:"text", media_type:"text/plain", data}, title, citations:{enabled:true}}` — Citations 문서의 plain text 예제와 동일(마커 해소) / `char_location`·`cited_text`·`document_index`·`start_char_index` / `response.usage.cache_read_input_tokens` — 일치
- Agent SDK 옵션명(Critical, 웹 2차): `query(prompt=, options=)`·`ClaudeAgentOptions(allowed_tools=, agents=, hooks=)`·`AgentDefinition(description, prompt, tools, model="sonnet")`·`HookMatcher(matcher="Write|Edit", hooks=[...])`·훅 반환 `{"hookSpecificOutput": {"hookEventName", "permissionDecision": "deny", "permissionDecisionReason"}}`·`input_data["tool_input"].get("file_path")`·`"Agent"` 도구명 — code.claude.com agent-sdk/hooks·subagents 문서 예제와 일치
- 한도·버전 5건: `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`=3 / `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`=20 / `maxBudgetUsd`·`max_budget_usd`(TS v0.3.219·Py v0.2.127) / 패키지 0.2.x·0.3.x(F11) / 세션 경로 `~/.claude/projects/<encoded-cwd>/*.jsonl` — 문서·원장과 일치
- 캐싱 수치 9건(F10): 5분 기본·1시간 2배·쓰기 1.25배/2배·읽기 0.1배·Fable 5.1/Mythos 5.1 0.025배·Opus 5.5/Sonnet 5.5 0.05배·최소 512/1,024토큰 — 2026-10 Prompt caching 문서와 일치, "2026년 10월 11일 열람"·"가장 빨리 낡을 숫자" 명기됨
- Files API 3건: 500MB/1TB·"cannot be modified or renamed"·워크스페이스 공유 인용 / Memory tool 7건: `memory_20250818`·6개 명령·`/memories`·"client-side"·시스템 프롬프트 인용·경로 검증 인용 — [W19]·[W20]과 일치
- 인용·귀속 16건: Same Task More Tokens 0.92→0.68·500/3,000토큰 / NoLiMa 32K·11개 모델 / Context windows "Cached prompt prefixes…" / gist "good answers can be filed back…" / vellumkasane 3건 / orcosto-lab 9세션·2세션·인용 / bluewater8008·Fulkerson / 공식 비교표 3건(Agent SDK·Client SDK·Managed Agents) / "same as Claude Code" / 서브에이전트 인용 2건 / Claude Code memory "context, not enforced configuration"·PreToolUse / 우선순위 "deny > defer > ask > allow" / 세션 인용 4건 / "Claude Opus 5 delegates…" / alfadur 5~10배 / manavgup·ShootJackal / Citations 인용 4건 — 원장과 일치
- 사용 금지 항목 F3·F9("2026-03-13 1M GA" 날짜 미사용)·F19 부재 확인; F12는 위 정정으로 제거
### 미해소
- (없음)

## 9장 (라운드 1)

### ❌ 정정
- "git은 … 20년 가까이 풀어 온 도구" → "20년 넘게" — git 첫 릴리스 2005년, 2026년 기준 21년(일반 상식, 레퍼런스 외)
- "세 뷰어 모두 사내용으로 쓰려면 SSO 프록시 뒤에" → "웹으로 띄우는 뷰어는 어느 쪽이든" — 같은 소절의 세 번째 뷰어는 로컬 Obsidian clone이라 프록시 대상이 아님(문맥상 사실 오류)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- Quartz/Docusaurus SSO 프록시 단락(F17): `(사실 확인 필요)` 해소 — 웹 1차 확인: Cloudflare Access 공식 문서(developers.cloudflare.com, self-hosted public app) "adding Cloudflare Access as an authentication layer between the end user and your origin server" / oauth2-proxy 공식 문서(oauth2-proxy.github.io) "A reverse proxy and static file server that provides authentication using Providers (Google, GitHub, and others)". 범용 인증 계층이라는 사실은 1차 출처로 확정하고, Quartz·Docusaurus 전용 안내는 없다는 점을 "별도 확인" 문구로 유지. "2026년 10월 열람" 시점 명기
### ✅ 확인 (요약)
- 인용·귀속 22건: gist 첫날 질문 3건(geetansharora·MoserMichael·alinawab) / gist "Possibly with humans in the loop reviewing updates"·"The wiki is just a git repo…" / Stigmergy 5건("identity, visibility, concurrency, binary evidence, Slack, audit"·"Postgres is operational state…"·"Captured content is data, never instructions."·"Nobody approves a queue."·"No write waits for a human.") / psteinweber·xoai / llmwiki "The filesystem is the source of truth…"·`VaultFS`·"never modify your files" / bradwmorris·mpazik·YIING99 / najmuzzaman·rothnic·Zetaphor / Quartz v5.0.0 자기 소개·배포 대상·"Private Quartz Publish" / sails / vellumkasane CSV·"The wiki repo sat dirty…" / Jim Liu originals/·do-not-rewrite·log.md 운영 / dataviz1000 / Anthropic 장기 실행 하네스 3건("do too much at once"·"clean state"·`claude-progress.txt`) / aakarim / zedi PR #604 / ap0phasi·renan_warmling / Fontoura(소스 텍스트는 데이터) — 01_reference 4·8.5·8.6·12, community.md, web.md와 일치
- 수치·버전·식별자 11건: llmwiki ★1.7k·Apache-2.0·Python 3.11+·Node 20+·Docker / llmwiki 이슈 #93 2026-09-19 / Stigmergy 2026-08 / podcast-wiki launchd 6시간·wiki/ 쓰기 전용·git 금지·커밋은 스크립트 / Files API 워크스페이스 100개·"create a separate workspace for each tenant"·"Never accept `file_id` values…" / Memory tool 경로 검증 / `claude -p … --allowedTools "Edit,Bash(git commit *)" --permission-mode dontAsk`·`--output-format json` / 1시간 TTL 2배 / Anthropic 장기 실행 글 2025년 11월(2025-11-26) / 공식 best practices "2026년 10월 열람" — 일치
- 사용 금지 항목 F3·F9·F12·F19 부재 확인; 커뮤니티 수치는 이 장에 없음
### 미해소
- (없음)


## 1장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — "X 포스트 2026-04-02 / gist 생성 2026-04-04", "별·포크 2026년 10월 11일 기준 5,000+", "2026년 10월 기준 100만 토큰"이 이미 시점 명기됨; F1 날짜 상충은 트윗/gist 구분 표기로 처리되어 있음)
### ✅ 확인 (요약)
- gist 인용 16건: "Humans abandon wikis…"·"The tedious part…bookkeeping"·"LLMs don't get bored…15 files"·Memex 1945 "who does the maintenance"·"intentionally abstract"·"optional and modular"·raw/wiki/schema 정의 3건·"A single source might touch 10-15 wiki pages"·"good answers can be filed back"·index.md "~100 sources, ~hundreds of pages"·log.md 접두사 `## [2026-04-02] ingest | Article Title`·`grep "^## \[" log.md | tail -5`·"The human's job is…"·"Obsidian is the IDE…"·"There's no accumulation"·"compiled once and then kept current"·"persistent, compounding artifact" — 01_reference 1.1~1.3 [W1] 원문 발췌와 일치
- 수치·날짜 7건: 본문 1,959단어 / HN 원 스레드 296점·댓글 95개(2026-04-04) / Show HN 40건 이상 / @_avichawla 2026-04-08 / Vannevar Bush 1945 / 100만 토큰 컨텍스트(W17, 2026-10-11 열람) — 01_reference 1.1·6.6과 일치
- 커뮤니티 귀속 5건: bluewater8008 "The LLM is the writer. You're the editor-in-chief."(gist 댓글) / qaadika "Learn how to learn…"(HN) / GeekNews 편집자 코멘트 / @_avichawla "But this pattern breaks…"·후속 "Karpathy liked this one!" / 당근 AI월드 2026(fnnews) — community.md와 일치
- 용어 메모 "gist는 backlink라는 말을 쓰지 않는다"(P-S1) 일치
- 사용 금지 항목 F3("100 articles/400,000 words")·F34(Threads 270만)·F42("surgically update")·Reddit 인용 부재 확인; gist 귀속 규모 수치는 "~100 sources, ~hundreds of pages"·"10-15 pages"만 사용(F4)
### 미해소
- (없음)

## 4장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- "여섯 달 동안 수십 개의 파생 구현이 나왔는데" → "여러 파생 구현이 나왔는데" — 레퍼런스(3.1절)는 파생 구현 6종만 열거, 개수 근거 없음
### 🕒 신선도
- (없음 — Astro-Han 별 수 "2026년 10월 11일 기준", 토스 하네스 "2026-02-26" 이미 명기)
### ✅ 확인 (요약)
- 디렉터리 구조 3건(Astro-Han README·HagaiHen·Taktile — 01_reference 3.1절), 토스 하네스 3계층·"가설" 자인(W38, 저자 토스페이먼츠 소속 research/web.md 자료 확인), @_avichawla 타입 엔티티(community.md)
- TL;DR·토큰 예산 수치 6건(YokoPunk·Jim Liu 50자/35개·bluewater8008 L0~L3·tomjwxf·AgriciDaniel 500) — 3.2절과 일치, 본문에 "자기 보고·통제 실험 아님" 명기됨(F33)
- 논문 4건: Dense X(arXiv 2312.06648, 11.2/58.5단어, Recall@20 +10.1 비지도 — 발표처 미기재, F29 준수), Qu 외(arXiv 2410.13070 인용문), Zep(arXiv 2501.13956 4타임스탬프·무효화 모델, "자체 평가라 수치 미인용" 명기, F28), Dhingra(TACL 2022 확인)
- 프런트매터 출처 4건(Fulkerson 인용문·Jim Liu schema.md 필드·토스 Topic 신뢰 상태 5종·우아한형제들 메타데이터), Glukhov 인용문, asakin·mfittko PR #48
- gist 귀속 수치는 "~100 sources, ~hundreds of pages"·"10~15 pages"만(F4 준수), index.md·log.md 정의와 grep 팁 원문 일치(web.md 자료 1), gist "inbound link" 용어(P-S1), 인라인 이미지 제약
- jermolene·Taktile 인덱스 오류·otomatty #604·aakarim — community.md와 일치
- 사용 금지 항목(F3·F8·F14·F15·F16·F18·F23) 부재 확인
### 미해소
- (없음)

## 5장 (라운드 1)

### ❌ 정정
- "구글 독스는 … 마크다운 공식 내보내기 경로를 확인하지 못했다(사실 확인 필요). 당장은 노션으로 옮기거나 사람이 복사해 넣는 쪽으로 두자." → "구글 독스는 2024년 7월부터 공식으로 마크다운을 내보낸다. 파일 → 다운로드 → 마크다운(.md) / Drive API export MIME `text/markdown`(2026년 10월 열람 기준)" — 웹 2차: Google Workspace Updates 2024-07-16 "Import and export Markdown in Google Docs"(workspaceupdates.googleblog.com), Google Docs 고객센터 12014036, Drive API 내보내기 형식 표(developers.google.com/workspace/drive/api/guides/ref-export-formats — Documents 행 "Markdown text/markdown .md"). 레퍼런스 16.1의 미확인 항목 해소, 마커 제거
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- Google Docs 정정문에 "2026년 10월 열람 기준" 부착. Notion API 절은 이미 "2026년 10월 열람 기준" 명기
### ✅ 확인 (요약)
- Notion Markdown API(웹 2차, developers.notion.com/reference/retrieve-page-markdown): `GET /v1/pages/{page_id}/markdown`, `Notion-Version: 2026-03-11`, 응답 `object: page_markdown`·`markdown`·`truncated`(약 20,000블록 한도)·`unknown_block_ids`(최대 100개, 재조회 가능), 403(읽기 권한 없음)/404(없거나 접근 불가), SDK `notion.pages.retrieveMarkdown` — 전부 일치. `include_transcript`(F15) 미사용 확인
- slackdump: "마크다운 직접 출력은 확인되지 않았다"로 F16 준수. PDF 도구 4종 특성만 서술·비교 수치 없음(F18 준수). llmwiki LibreOffice·Mistral OCR(W8)
- 커뮤니티 수치 전부 자기 보고 명기(F33): bluewater8008·HagaiHen·vbarsoum(210/4,597/19.2·68파일·15.5만 단어·12M 토큰·10~15분)·julianoczkowski 5~15분·클리앙 20분+·프밍·Helleeni·grishasen·Ghelbur $0.05/$0.40~0.80·glaucobrito $0·Jim Liu $20·alfadur 5~10배·페이지 폭발(gist 10~15·xoai·AgriciDaniel 8~15·MetamusicX 38·Jim Liu 중앙값 9, 4~23) — 3.3·3.4절과 일치
- Karpathy "one at a time" 선호(W1 원문), gist ingest 흐름(1.3절), Anthropic 장기 실행 하네스 글(2025-11-26) 교훈 3건·claude-progress.txt(W21)
- @vellumkasane 기록 트리거 4종·do-not-record·인용문(2026-09-22), HagaiHen "Extend, don't create"/"Rewrite … don't append"/dream 패스, Ghelbur 2024 인용문, Taktile 소스 해시 계획·"매 답변 소스 재조회", Jwcjwc12·viberesearch
- STORM(arXiv 2402.14207, NAACL 2024 Main 확인 — 발표처 기재 허용), 25%/10%포인트, 새 실패 유형 2종; Casey Newton 문체 인용(W3); 토스 Topic 결정/미결 구분(W37)
- 사용 금지 항목(F3·F8·F14·F15·F16·F18·F23) 부재 확인
### 미해소
- (없음)

## 6장 (라운드 1)

### ❌ 정정
- "'You curate sources, the LLM writes the wiki'라는 gist의 문장" → gist 실제 문장 "You drop a new source into the raw collection and tell the LLM to process it."로 교체 — 인용된 문장은 gist 원문에 없음(원문은 "The human's job is to curate sources … The LLM's job is everything else."). 논지(gist가 사람을 "You"로 부름)는 유지
- "@vellumkasane … 차단하고(신규 추가만 허용)" → "(신규 추가와 append만 허용)" — 01_reference 5.4절 "신규 추가·append만 허용"
- "주석을 빼면 70줄 남짓이다. 200줄 예산의 3분의 1이다." → "60줄 남짓이다. 200줄 예산의 3분의 1이 안 된다." — 본문 산출물 직접 세기: 주석 제외 63줄(공백 포함)/52줄(공백 제외)
### ⚠️ 약화·삭제
- "같은 시기 Claude Code 공식 문서는 … 적고 있었다" → "Claude Code 공식 문서(2026년 10월 열람 기준)는 … 적고 있다" — 2026-04 시점의 문서 내용은 레퍼런스에 없음(열람 시점만 확인)
### 🕒 신선도
- 위 항목에 "2026년 10월 열람 기준" 부착. v2.1.277+/v2.1.283+·auto memory 200줄/25KB 절은 이미 "2026년 10월 열람 기준" 명기
### ✅ 확인 (요약)
- Claude Code memory 문서(웹 2차, code.claude.com/docs/en/memory): 새 컨텍스트·두 메커니즘, auto memory "first 200 lines or 25KB", "target under 200 lines", "context, not enforced configuration"·PreToolUse 훅, 모순 시 임의 선택, `@path` import 최대 4홉·컨텍스트 비용 미절감, 하위 디렉터리 온디맨드 로드, `.claude/rules/` 경로 스코프, AGENTS.md "v2.1.277 or later"·CLAUDE.md 없을 때만, `/doctor prompt-audit` "v2.1.283 or later"·점검 항목 3종, "facts Claude should hold in every session"·스킬/경로 규칙 이관 — 전부 원문 일치. "Would removing this…"·"over-specified… lost in the noise"·"Give Claude a check it can run"(best practices, W25)
- Agent Skills(웹 2차, anthropic.com/engineering/equipping-agents-…): SKILL.md 디렉터리, `name`·`description` 필수, 3단계 progressive disclosure, "effectively unbounded", Claude.ai·Claude Code·Agent SDK·Developer Platform 지원, 2025-10-16 발행·2025-12-18 오픈 표준 업데이트, 토큰·줄 상한 없음 — 본문의 "5,000토큰 상한은 공식 글에 없다" 서술과 일치(F14 준수)
- 이슈 #42796(2026-04-02, 댓글 583)을 공식 "200줄"과 함께 인용(F41 준수); arXiv 2602.11988 미인용(F8 준수); kwar13·criley2·Yuncun·justinzhang2039(2026-04-06) — community.md와 일치
- @vellumkasane(CRM·회계 앱 옆 위키 4곳, 2주 4건, "wish, not a rule", PreToolUse·Stop 훅 `git status --porcelain`), Ghelbur(2026-04-29, 마케팅 에이전시, 슬래시 커맨드 31·예약 에이전트 4, 1만 단어·`<think>`·파이썬 dict), Jim Liu "most important file", Karpathy "the key configuration file"·co-evolve(W1 원문), Fulkerson 훅 인용 2건, 토스 하네스 "기록→실행"(W38), Astro-Han `npx add-skill` 3스킬, LY ODW #5 "SE-0500"(발행일 미기재 유지, F20)
- Anthropic 컨텍스트 엔지니어링(2025-09-29) 고도·Goldilocks·가벼운 식별자·glob/grep·just-in-time·progressive disclosure(W14)
- 논문 5편: FreshLLMs(arXiv 2310.03214 — 발표처 미기재, F29; "모델 크기 무관"·"간결 지시가 환각 감소" papers.md 3-10 일치), WikiChat(arXiv 2305.14292, Findings of EMNLP 2023 확인, +3.9/+38.6/+51.0), Self-RAG(arXiv 2310.11511 — 발표처 미기재, 4토큰·인용문), CRAG(arXiv 2401.15884, 3분기), Resolving Knowledge Conflicts(arXiv 2310.00935, COLM 2024 확인, 인용문)
- Stigmergy·Fontoura "데이터" 원칙, LY 도구 메시지 주입(W40), 토스 Topic `insufficient_evidence`(W37), 페이지원 32명·원북(02_plan 정전)
- 사용 금지 항목(F3·F8·F14·F15·F16·F18·F23) 부재 확인
### 미해소
- (없음)

## 2장 (라운드 1)

### ❌ 정정
- NoLiMa 설계 서술 "질문과 정답 문장 사이에 글자 그대로 겹치는 어휘가 없도록 만들었다" → "겹치는 어휘를 최소화하도록 만들었다"(뒤 문장 "겹치지 않자" → "겹침을 걷어내자") — 근거: arXiv 2502.05167 초록 원문 "questions and needles have minimal lexical overlap"(웹 확인); papers.md 2-11 요약("어휘 중복을 최소화")과도 일치. "없도록"은 과장
- Lost in the Middle "중간(인덱스 9)" → "한가운데(스무 개 중 열 번째)" + "(GPT-3.5-Turbo 기준)" 추가, "읽어 낸 계산값" → "읽어 낸 값" — 근거: 논문 부록 G Table 6(ar5iv 확인) — "Index n"은 n+1번째 위치, 20문서 설정은 인덱스 0/4/9/14/19, GPT-3.5-Turbo 행 75.8/57.2/53.8/55.4/63.2. 수치는 표에 그대로 있는 값이지 계산값이 아님(원장 F26 "계산값" 표기는 "본문 문장이 아님"의 뜻으로 해석)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- LY Corporation 인용 "(글의 발행일이 페이지에 표시되어 있지 않다 — 사실 확인 필요)" → "(발행일 미표시, 2026년 10월 열람 기준)" — F20 해소: 페이지 직접 열람(2026-10-12)에도 발행일 없음(이미지 메타의 2026-01·03은 갱신 시각이라 발행일로 못 씀). 인용 문장 "GPT-4나 Llama-3.1 같은 모델에서도 … (32K~64K 토큰) …" 원문 일치
### ✅ 확인 (요약)
- NoLiMa 수치 6건: ICML 2025 / 32K에서 11개 모델 50% 미만 / GPT-4o 99.3%→69.7% / Llama 3.1 70B 표방 128K·유효 2K·32K 42.7% / 유효 길이 대부분 ≤2K·GPT-4o 8K — papers.md 2-11·arXiv 초록과 일치
- Context Rot 6건: Chroma 2025-07-14·Hong/Troynikov/Huber·비동료심사·arXiv ID 없음(F27 명기) / 18모델·8길이·11위치 / 인용 3건 / LongMemEval 306문항·~300 vs ~113K 토큰 — P-S2 일치
- 논문 수치·인용 18건: Lost in the Middle closed-book 56.1%·"more than 20 retrieved documents…"(TACL 2023) / Same Task More Tokens 500토큰·0.92→0.68(3,000)·인용(ACL 2024) / RULER 인용(COLM 2024) / Generative Agents 가중치 1·0.995·0.995^24≈0.89·임계치 150(UIST 2023 S2 표기 명시) / MemGPT 32.1→92.5·35.3→93.4·인용(2023 프리프린트) / A-MEM memory evolution 인용·"최대 약 93%"(F23 준수, NeurIPS 2025) / Zhang 서베이 writing·management·reading(2404.13501) / Editing LLMs reliability 99+·IKE 55.38·MEMIT 52.74·SERAC 20% 미만·인용(EMNLP 2023) / Ripple Effects 인용(TACL 2024) / 지식 편집 3분류(2401.01286) / Dhingra 인용(TACL 2022) / TemporalWiki 12분의 1(EMNLP 2022) / FreshLLMs 인용 2건(ACL 2024 Findings S2 표기 명시) — 01_reference 1.4·2.1·2.3, papers.md와 일치
- 공식 문서 5건: Anthropic 컨텍스트 엔지니어링 2025-09-29 정의·목표·attention budget·context rot / Claude API Context windows "more context isn't automatically better…"·"Cached prompt prefixes still occupy…"(2026-10-11 열람 명기) / 100만 토큰 기본(2026년 10월 기준 명기) / Contextual Retrieval 2024-09-19 "smaller than 200,000 tokens (about 500 pages…)"·"2024년 기준·Claude 3 세대" 명기(F13) — W14·W15·W16·W17 일치
- 커뮤니티 1건: HN lelanthran "What use is 10M context…" — community.md 일치
- 사용 금지·주의 항목: A-MEM "multi-hop 2배"(F23) 부재, 1M GA 날짜 "2026-03-13"(F9) 부재, 벤더 자체 평가 명시(F28 — Chroma "벤더 보고서·비동료심사"), 발표처 "S2 표기" 항목(Generative Agents·FreshLLMs)은 본문에 그 사실을 병기(F29)
### 미해소
- (없음)

## 3장 (라운드 1)

### ❌ 정정
- "Retrieval as Reasoning" 단락(F5 해소): "아직 2차 자료다 … GeekNews의 소개 글에 따르면 … (사실 확인 필요) … 이 책은 논문 원문을 대조하지 못했고" → 원문 대조 완료로 재서술. arXiv 2605.25480 실재 확인(Ming·Li·Wu·Que, v1 2026-05-25, cs.CL, 제목 "Retrieval as Reasoning: Self-Evolving Agent-Native Retrieval via LLM-Wiki"). 초록 "compiles documents into structured Wiki pages with bidirectional links"·"by 2.0-8.1 F1 points"(HotpotQA·MuSiQue·2WikiMultiHopQA, 대조군 HippoRAG 2·LightRAG·GraphRAG) 일치. ablation(§5.3 Table 3) 위키 구조 제거 −0.061/−0.070/−0.067, 점진적 순회(progressive traversal) 제거 −0.117/−0.138/−0.122 → GN 요약의 −6.1/−7.0/−6.7·−11.7/−13.8/−12.2(F1 포인트)와 일치. "페이지 순회" → "검색·읽기·링크 따라가기를 반복하는 점진적 순회"로 논문 용어에 맞춤. 비교군이 BM25·Dense RAG·RAPTOR·GraphRAG·LightRAG·HippoRAG 2이며 튜닝된 agentic RAG 아님 확인 — 근거: arxiv.org/abs·html/2605.25480(웹 확인), 원장 F5
- "한 사전등록식 비교 … '약 21배 더 많은 토큰'(2차 인용, 사실 확인 필요)"(F6 해소) → 출처 특정: Cochran, "Single-Round Vector RAG vs an LLM-Compiled Wiki: A Preregistered Comparison on a Small Multi-Domain Research Corpus", arXiv 2605.18490(v1 2026-05-18, v3 2026-10-02). 초록 "spent about 21 times more LLM tokens per query"·"scored much better at connecting findings across papers" 일치. 규모(논문 24편·질문 13개)를 본문에 병기 — 근거: arxiv.org/abs/2605.18490(웹 확인)
- "HN에서 xguru는 약 2,500 항목을 400페이지로" → "GeekNews에서 xguru는" — 근거: community.md "GeekNews 28208 xguru — Farzapedia(약 2,500 항목 → 400페이지)"(xguru는 GeekNews 운영자, HN 댓글 아님)
- Karpathy 귀속 인용 "compile once, keep current" → gist 원문 "The knowledge is compiled once and then kept current." — 근거: web.md [W1] 원문 발췌(앞의 것은 community.md의 요약 구절이라 따옴표 안에 Karpathy 말로 둘 수 없음)
### ⚠️ 약화·삭제
- 구영수(clue.oz4e) "수개월 운영 끝에" → "2026년 8월, 운영 끝에" — community.md에 운영 기간 근거 없음(댓글 일자 08-10·08-21만 있음)
### 🕒 신선도
- (없음 — Taktile "2026년 7월 13일·자기 보고", 클리앙 "2026-04-26·자기 보고", 윤기석 "2026-06-24", LC vs RAG "2024년 모델 기준", Contextual Retrieval "2024년 기준"이 이미 명기됨; 2026년 논문 두 편은 "프리프린트" 시점 병기)
### ✅ 확인 (요약)
- 논문 수치·인용 14건: GraphRAG "RAG fails on global questions…"·"9x-43x"·comprehensiveness 72~83%·LLM-as-judge·directness는 벡터 RAG 우세·281분·약 100만 토큰(2024 프리프린트) / RAPTOR "18.5% to 57%"·QuALITY 82.6 vs 62.3(ICLR 2024 S2 표기 명시) / Mem0 약 2%·벤더 자체 평가 명시(ECAI 2025 S2 표기, F28) / HippoRAG "10-30 times cheaper and 6-13 times faster"(NeurIPS 2024) / LC vs RAG 인용·7.6%·13.1%·3.6%·Self-Route 65%·39%·실패 유형 4범주+기타(F25, EMNLP 2024 Industry) / Search-R1 "20~41%(버전에 따라)"(F24, 2025 프리프린트) — 01_reference 2.2, papers.md 1-5·1-7·1-8·1-10·2-7·2-12와 일치
- 커뮤니티 귀속 19건: kenforthewin·devmor·mememememememo·panarky·darkhanakh(HN) / visakadev(gist) / dishant0406(Dev.to) / jdthedisciple·Marekai·a-a-k / Casey Newton "to make sure nothing I was about to say was hallucinated"(2026-08-18) / Fontoura "메커니즘"·전체 트랜스크립트 / Imanari "kicking the can…"·"regurgitate 2nd-order information" / devnullbrain·gojomo·ChrisGreenHeur / GeekNews HN 요약 "새로운 형태의 기술 부채"(W4) / 윤기석 2026-06-24 인용 / 구영수 "지도로 강등"·recall@5 93%(자기 보고 명기) / VentureBeat "bypasses RAG" 프레임 / gist "optional and modular"·qmd 추천 — community.md·01_reference 2.4·12절과 일치
- 실사용 수치(자기 보고 명기, F33) 3건: Taktile 9분 40초·$2.50 → 1분 19초·$0.98(86%·61%, 2026-07-13) / 클리앙 카일라스 2026-04-26·500+ 메모·20분 넘게·인용 2건 / xguru 2,500 항목·400페이지 — 일치
- 사용 금지 항목 F3·F9·F23·F34·Reddit 인용 부재 확인; 자기 보고 수치는 모두 문장 안에 "자기 보고" 라벨 있음
### 미해소
- (없음)

## 10장 (라운드 1)

### ❌ 정정
- Karpathy 귀속 "surgically update only affected pages"(F42, `(사실 확인 필요)` 주석) → gist 원문의 수집 정의 "updates relevant entity and concept pages across the wiki"(한 소스가 10~15 페이지를 건드린다) — 근거: gist raw(https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw) 전문 대조에서 "surgical/surgically/affected pages" 미출현. community.md §논쟁 E의 "Karpathy 원문의" 귀속은 오류 — 날조 인용 1건 제거, 주석 닫음
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — Fontoura 2026-10, Abby_101 2026-04, Jim Liu 2026-05, Ghelbur 2026-04, Theo James 2026-04, vellumkasane 2026-09, llmwiki #93 2026-09, Glukhov "발행일 미표시" 명기, Jim Liu $0.40 "Opus 1M 컨텍스트 기준·자기 보고" 명기됨)
### ✅ 확인 (요약)
- 논문 인용·수치 9건: ClashEval "overriding their own correct prior knowledge" / Chameleon·Sloth(ICLR 2024 Spotlight) "coherent and convincing"·"a strong confirmation bias"·3.7%→99.8%·Llama2-7B 92.4% / RAGTruth GPT-4 13.7%(F26, "Table 3 계산값이지 논문 문장 아님" 본문 명기) / SemDeDup(학습 데이터 맥락·수치 미이식 명기, F31) / Wang 외 arXiv 2310.00935(COLM 2024) "identifying the existence… struggle to determine the specific conflicting knowledge" / Dhingra "Many facts come with an expiration date" / TemporalWiki 1/12 — papers.md 3-2·3-3·3-4·3-8·3-9·3-12·4-6, 01_reference 8.1·8.2와 일치
- gist 1차 인용 3건: "ingest sources one at a time and stay involved" / "Possibly with humans in the loop reviewing updates" / 수집당 10~15페이지(F4) — gist raw 대조 일치
- 커뮤니티 귀속 인용·수치 34건: Abby_101·Jwcjwc12·Fontoura(2026-10-06)·Glukhov(검토 주기 표·위험 등급·체크리스트·"lie quietly"·"vague compromise")·Jim Liu(6개월·3개월 차 고아·aliases 유실·"Contradictions are assets"·24 링크·<$0.40·15분/20분/격주)·Ghelbur(31 커맨드·4 에이전트·50~100 소스·"accumulated faster"·헤지·24시간)·Theo James(2주·3주·"Missing 5 percent")·vellumkasane(4곳·150줄·5항목·CI nonzero)·Fulkerson(23/11·LOG.md 90일·"bookkeeping")·llmwiki lint·podcast-wiki(`tools/lint_wiki.py`·`/lint-wiki`·`/dream`·launchd 6시간)·markdownlint/lychee/mdlint/wiki-lint·Covenant0028·ChrisGreenHeur·HagaiHen "Never silently overwrite"·Taktile 2건·saadn92·Fontoura "ripe page"·techwithhari PR 규칙·anuramat `// SLOP`·Stigmergy 3건·SOLAR_FIELDS·bluewater8008·jurajskuska·simsla·saberience·Ask HN 2026-07 댓글 0·daydreamblend·Medium 2차 인용(F37, 본문에 "원문 미확인" 명기)·alfadur·jermolene·dataviz1000 — community.md·web.md·01_reference 8절·12절과 일치. 자기 보고 수치는 모두 문장 안에 라벨 있음(F33)
- 러닝 예시 정전: 가격 페이지 경로·`valid_from/to`·`review_after: 2026-03-30`·32명·1시간 캐시 TTL — 02_plan·04/08/09_final과 일치
- 사용 금지 항목 F3·F9·F19·F23·F34·F36(Reddit) 부재 확인
### 미해소
- (없음)

## 11장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- "구영수(clue.oz4e)가 몇 달간의 운영기를 올리며" → "2026년 8월 운영기를 올리며" — community.md에 운영 기간 근거 없음(댓글 일자 08-10·08-21만). 3장 판정과 동일 처리
### 🕒 신선도
- (없음 — Anthropic 평가 글 "2026년 1월", Verifiability "2023년 초 상용 시스템 기준"(F30), ShootJackal "2026년 10월" 명기됨)
### ✅ 확인 (요약)
- 공식 문서 인용 8건: Anthropic evals(2026-01-09) eval·task·trial·grader 정의·capability/regression·"20-50 simple tasks"·pass@k/pass^k·"Eval saturation" / Citations API "guaranteed to contain valid pointers to the provided documents" — web.md [W22]·[W18]과 일치
- 논문 인용·수치 10건: LongMemEval(ICLR 2025) 5능력·"a 30% accuracy drop" / RAGAS "without having to rely on ground truth human annotations" / ARES(NAACL 2024) "only a few hundred human annotations" / ALCE(EMNLP 2023) citation recall·precision·"50% of the time" / Verifiability 51.5%·74.5%(F30 라벨) / RAGTruth 탐지기 F1 78.7% vs 63.4% / CRAG Correct·Incorrect·Ambiguous(6장 final과 정합) — papers.md 4-1~4-7·2-6과 일치
- 커뮤니티·국내 10건: clue.oz4e "10개 전부"(08-10) / ShootJackal "trusting what it tells you later"(2026-10-01)·VERIFIED 위조·"a check with no model in it…" / manavgup "hallucinates 404s" / Stigmergy "pure code"·Recall@5 1.00·정직성 1.00·15문항(자기 보고 명기) / techwithhari 9페이지·3/10→7/10(자기 평가 명기) / WUPHF OP 500 아티팩트·50 쿼리·recall@20 85%(자기 보고 명기) / Taktile 24쿼리 / 우아한형제들 Langfuse·G-Eval·수치 미공개 / 토스 Topic `insufficient_evidence` "실패가 아니에요"·"0.87" 예시값(F21) — community.md·web.md [W37]·[W39]와 일치
- 러닝 예시 정전: 골든셋 씨앗 6문항(8장 final 문구 그대로)·"일본 진출 pending"·"39,000원" — 02_plan·08_final·writer_handoffs와 일치
- 사용 금지 항목 F3·F9·F19·F23·F34·F36 부재 확인
### 미해소
- (없음)

## 12장 (라운드 1)

### ❌ 정정
- "Same Task, More Tokens가 500토큰을 넘으며 정확도가 0.92에서 0.68로 떨어진다" → "500토큰을 넘으면서 떨어지기 시작해 3,000토큰에서 0.92가 0.68이 된다" — 근거: papers.md 2-9(0.68은 3,000토큰 값), 2장 final 문구와 정합
- "가장 가까운 2026년 논문 셋(…)은 2차 요약만 확보했다" → 둘(arXiv 2605.25480·2605.15184)은 arXiv 원문 확인·동료심사 전 프리프린트, 자동 생성 AGENTS.md(arXiv 2602.11988)만 HN 2차 인용 — 근거: writer_handoffs.md fact-checker 메모(3장·7장에서 1차 대조 완료), F8
- Karpathy 인용 "You're in charge of sourcing, exploration, and asking the right questions. The LLM's job is everything else." → 두 문장을 별개 인용으로 분리 — 근거: gist raw 대조, 두 문장은 서로 다른 단락(web.md [W1] 발췌 29행·63행)이라 한 따옴표 안에 연속 인용으로 둘 수 없음
### ⚠️ 약화·삭제
- 사례 대조표 "clue.oz4e (PyTorchKR, 수개월)" → "(PyTorchKR, 2026-08)" — 01_reference §11 표는 "수개월"이나 그 원천(community.md 댓글)에 운영 기간 근거 없음. 3장·11장 판정과 통일(§11 표와의 의도적 불일치 — editor 참고)
### 🕒 신선도
- (없음 — 사례 대조표 전 행에 시점 명기, "리서치 시점(2026년 10월)" 명기)
### ✅ 확인 (요약)
- 사례 대조표 12행 vs 01_reference §11: Taktile(2026-07, 9m40s·$2.50 → 1m19s·$0.98) / Newton(2026-08, 1,440+) / Jim Liu(6개월, 2026-05, 15분·20분·<$0.40) / Ghelbur(2026-04, 31·4, $0.40~0.80·24시간) / vellumkasane(2026-09, 4곳·150줄·2주 4건) / techwithhari(2026-05, 9페이지·$35→~$0·3/10→7/10) / HagaiHen(2026-10, 60회→69) / orcosto-lab(2026-09, 9세션 중 2) / 카일라스(2026-04, 500+·20분+·"대부분 유사") / Theo James(2026-04) / llmwiki #93·#47 370파일·#52 — 이름·스택·수치 일치(clue.oz4e 시점 표기만 위 ⚠️)
- 인용 5건: @keane42443 "Now what?"(X, 2026-05-07) / alinawab "What's the failure mode? Where does it start fighting you?"(gist 2026-04-04, 답글 없음) / 당근 AI월드 2026 "판단의 결과뿐 아니라 이유와 근거를…" / Karpathy "There's no accumulation."(1장 final과 정합) / Stigmergy identity·visibility·concurrency·audit(9장 final과 정합) — community.md·web.md와 일치
- 결정 목록·전체 그림: 디렉터리·프런트매터 필드·가격/결정 페이지 경로·300건 전후 BM25·"토스 하네스 저자 스스로 가설" — writer_handoffs·02_plan·04/07/09_final·[W38]과 일치. 4주 계획의 기준값은 저술가 설계값(handoffs 명기)으로 검증 대상 아님
- 국내 참조점 4건(토스 Topic·토스페이먼츠·우아한형제들·LY)·"국내 사내 도입 후기 부재" — 01_reference 11.1·16.1과 일치
- 사용 금지 항목 F3·F9·F19·F23·F34·F36 부재 확인
### 미해소
- (없음)

## 7장 (라운드 2)

수락 게이트 (c) 재검수 — 대상: clue.oz4e 운영 기간 표현.

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- "PyTorchKR의 clue.oz4e는 몇 달의 자체 구현 끝에 위키를 …" → "PyTorchKR의 clue.oz4e는 2026년 8월 운영기에서 자체 구현 끝에 위키를 …" — community.md에 운영 기간 근거 없음(댓글 일자 2026-08-10·08-21만, §사례표의 "수개월"은 원천 댓글에 근거가 없는 합성 표기). 3·11·12장 판정과 통일. "자기 보고, 통제군 없음" 라벨 유지
### 🕒 신선도
- (없음)
### ✅ 확인 (요약)
- 12개 `*_final.md` 전수 grep: "몇 달"·"수개월"·"몇달"이 clue.oz4e 또는 다른 커뮤니티 구현자에게 붙은 잔여 사례 없음(Jim Liu "6개월"은 원문 명시 기간이라 대상 아님)
### 미해소
- (없음)

## 2·4·10장 (라운드 2)

수락 게이트 관찰 — 대상: Dhingra 외 연도 2021/2022 혼재.

### ❌ 정정
- (없음 — 두 연도 모두 참. arXiv 2106.15110 v1 2021-06-29, TACL 2022 vol.10 pp.257–273. arxiv.org/abs/2106.15110 직접 확인, 01_reference [P3-8]과 일치)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- 표기 통일 "Dhingra 외(2021, TACL 2022)": 2장 본문 "Dhingra 외(arXiv 2106.15110, TACL 2022)" → "Dhingra 외(2021, arXiv 2106.15110; TACL 2022)"(첫 언급이라 arXiv ID 유지) / 2장 표 "Dhingra 외(arXiv 2106.15110)" → "Dhingra 외(2021, TACL 2022)" / 4장 "Dhingra 외(TACL 2022)" → "Dhingra 외(2021, TACL 2022)" / 10장 "Dhingra 외(2021)" → "Dhingra 외(2021, TACL 2022)". 3장 표의 연도 없는 "Dhingra"는 같은 셀의 "FreshLLMs"와 형식이 같아 그대로 둠
### ✅ 확인 (요약)
- 인용문 "Many facts come with an expiration date, from the name of the President to the basketball team Lebron James plays for." — 01_reference 인용 23·[P3-8]과 일치
### 미해소
- (없음)
