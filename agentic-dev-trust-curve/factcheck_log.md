# 사실 검증 로그 — agentic-dev-trust-curve (tech-book, 검색 시점 2026-10-10)

## 01장 (라운드 1)

### ❌ 정정
- "같은 해 8월, Lauren Tan…은 … 워크숍을 이렇게 열었다" → "이듬해인 2026년 8월" — 근거: 01_reference §1-1 녹화일 2026-08-12 추정(업로드 09-15). METR이 2025-07이므로 "같은 해"는 2025로 읽혀 오류
- "이 사람은 다섯 달 뒤에 … 자동 머지" → "입사 다섯 달 만에" — 근거: 자막 [00:03:36] "over the past 5 months … ascend this trust curve", [00:04:53] "I joined five months ago". 오프닝 인용은 워크숍 당일 발화이므로 "뒤에"는 시점이 어긋남
### ⚠️ 약화·삭제
- METR "절반은 허용하고 절반은 금지" → "과업마다 AI 도구 허용 여부를 무작위로 배정" — papers.md 4-4는 246 과업 무작위 배정만 기술, 50:50 비율은 원장에 없음
- "손으로 그린 차트" → "직접 그린 차트" — 자막 [00:02:33]은 "not a very scientific chart"뿐, 수기 여부 근거 없음
### 🕒 신선도
- (없음 — Hashimoto 2026-02, METR 2025-07, "2026년 7월 기준 본인 보고" 등 시점 명기 확인)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 1건 해소: Peng 2023 과업 "JavaScript로 HTTP 서버 구현" — papers.md 4-1과 일치 → 마커 제거
- 수치 9건(METR 16명·246·−19%·사전 −24%·사후 −20%; Peng 55.8%; Cui 4,867명·+26.08%; Paradis 96명·약 21%·CI 넓음; Wang 17명; Vasconcelos 5연구·731명) — papers.md §1·§4, 01_reference §5-1과 일치
- 학술 귀속 4건(Lee & See 2004 *Human Factors*, Hoff & Bashir 2015 3층, Wang 2024 FAccT, Vasconcelos 2023) — 일치. Wang venue FAccT(CHI 아님) 확인
- 자막 인용 12건([00:00:44] 리뷰 시간, [00:02:33] 차트, [00:03:07]–[00:03:36] 1단계·병렬 불가, [00:03:52] 20 PR "그날 아침", [00:26:41]·[00:28:01] 건너뛰기 경고, [00:31:28] 인턴 자격증명, [00:06:10]·[00:06:29] 검증 정의·맞는/좋은 코드, [00:47:57]·[00:48:09]·[00:50:02]·[00:50:17] 토큰 Q&A, [00:47:12] 호스트 "2~3개") — 자막 원문과 대조 일치
- "4단계 번호는 호스트 요약·본인 동의"(C9), "PR 1,000개는 2026-07 본인 보고·외부 감사 없음"(C1), Hashimoto 6단계·인용(web.md 자료 46), 0단계 커뮤니티 반론(§6-7) — 계획의 저술 제약대로 한정어 유지 확인
### 미해소
- (없음)

## 02장 (라운드 1)

### ❌ 정정
- "`acceptEdits`는 파일 편집은 자동 승인하고 명령 실행은 묻는다" → "파일 편집과 `mkdir`·`mv` 같은 흔한 파일 시스템 명령은 자동 승인하고, 그 밖의 명령 실행은 묻는다" — 근거: code.claude.com/docs/en/permission-modes(2026-10-10 조회) 표 "Reads, file edits, and common filesystem commands (`mkdir`, `touch`, `mv`, `cp`, etc.)" — 원장에 없어 웹 2차 확인(Critical: 권한 모드 동작)
- "`plan`은 읽기만 하고 계획을 세운다" → "파일을 읽고 탐색 명령을 돌려 계획을 세우되 소스는 고치지 않는다" — 근거: 같은 문서 "Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source" — 읽기만 한다는 서술은 부정확
- #15310 해석 "`read-only`로 돌렸다고 믿었는데 실제로는 쓰기가 되고 있었다면" → "설정보다 좁은 쪽으로 떨어졌지만, 요점은 설정한 정책이 무인 실행 경로에 전달되지 않았다는 것" — 근거: `gh api repos/openai/codex/issues/15310` 제목 "Desktop automations silently fall back to workspace-write sandbox regardless of app configuration", 본문: `danger-full-access` 설정인데 `workspace-write`로 시작. 폴백 방향이 원고와 반대(넓어진 게 아니라 좁아짐). community.md L188의 "read-only 폴백" 표기도 오기 — 원장 §3-3·community L102의 "workspace-write 폴백"이 맞음
- "Codex 설정을 저장소에 커밋" → "Codex의 `.codex/config.toml`을 저장소에 커밋" — 프로젝트 범위 설정 파일명 구체화(아래 ✅ 참조)
### ⚠️ 약화·삭제
- auto mode "연구 프리뷰 시절 '격리된 샌드박스에서만' 권고가 붙어 있었다" → "…붙어 있었다고 전해진다" — community.md L169 뉴스 2차 경유, 1차 문서 미확인
### 🕒 신선도
- (추가 없음 — "2.1.x/2026-10 기준", "0.16x/2026-10 기준" 꼬리표 이미 있음. `--bare` "향후 `-p` 기본값" 휘발성 문구는 공식 문서 인용 그대로)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 2건 해소: (1) `acceptEdits`·`plan` → 위 정정; (2) Codex `config.toml` 샌드박스 키 → learn.chatgpt.com/docs/config-file/config-reference(2026-10-10 조회): `sandbox_mode` = `read-only`|`workspace-write`|`danger-full-access`, `approval_policy` = `on-request`|`never`, "User-level configuration lives in `~/.codex/config.toml`", "You can also add project-scoped overrides in `.codex/config.toml` files", "Codex loads project-scoped config files only when you trust the project" → 키 이름 명시하고 마커 제거
- Claude Code 권한 모드 6종·`auto` 분류기 설명·2.1.283 기본화·`dontAsk`/`bypassPermissions` 용도 문구·"Deny rules block in every mode, including `bypassPermissions`" — web.md 자료 14 + 공식 문서 재확인 일치
- `--bare` 2건 인용(훅·MCP 실행, "will become the default for `-p`") — web.md L316–317 일치
- Codex `--sandbox` 3값·`-a` 2값·`--full-auto` deprecated·`--yolo` 경고 문구 — web.md 자료 22 일치
- GitHub 이슈 3건 메타(#15310 2026-03 open, #2847 2025-08, #51601 2026-10 117 댓글) — community.md L101–102·L188, 01_reference §3-3 일치
- 커뮤니티 인용 5건(HN 48348578 nialse·felixgallo 2026-05, HN 47923275 "demented" 2026-04, mtlynch 2026-10, GeekNews 35104) — community.md L49·L100·L103 일치
- 자막 [00:31:28] 브라운필드 가드레일 인용 — 일치
- `--worktree` 경로 `.claude/worktrees/<name>/`·`.worktreeinclude` `.env` 복사 — web.md 자료(워크트리) 일치
- 표(0·1단계 매핑) — 01_reference §4-4 일치
### 미해소
- (없음)

## 03장 (라운드 1)

### ❌ 정정
- Lulla 2026 "실행 시간을 28.64%" → "실행 시간 중앙값을 28.64%" — 근거: papers.md 7-2 "중앙값 실행 시간 −28.64%"
- "Codex는 AGENTS.md만 읽는다" → "Codex는 별도 설정이 없는 한 CLAUDE.md를 읽지 않는다" — 근거: web.md L468–469 Codex는 `AGENTS.override.md`·`AGENTS.md`·`project_doc_fallback_filenames`를 읽음("Filenames not on this list are ignored"). "AGENTS.md만"은 override 파일을 빠뜨리고, 논지(CLAUDE.md 미독)는 유지
### ⚠️ 약화·삭제
- "Lauren의 스킬 대부분이 이 목록에서 나왔다" → "Lauren의 스킬도 이런 관찰에서 나왔다" — 자막 [00:14:11] "it just started with a bunch of skills", [00:14:27] `how` 스킬 유래만 있음. "대부분" 비율 근거 없음
### 🕒 신선도
- (추가 없음 — "Spring Boot 4.1/2026-10 기준", "Next.js 16/2026-10 기준", "2.1.277" 시점 명기 확인)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 마커 없음
- 토비 라이브 인용 4건("최선의 스프링 개발자들…", Boot 3.5/Java 17~21 거부·Initializr 강제, "실패하는 테스트를 꼭 만들고", N+1 "기가 막힌다", "여러분이 바보가 됩니다") — community.md L116·L133·L266·L289 일치
- 자막 인용 6건([00:03:07] 1단계, [00:04:53] 첫 달, [00:20:08]·[00:20:46] 백시트 드라이버, [00:14:27]–[00:16:59] `how` 스킬, [00:36:22]–[00:37:27] PR 크기·git 히스토리·하드 캡 없음·"평균 모름") — 일치
- 커뮤니티 7건(HN summarity "simplest fix" 2026-04, AllegedAlec 2.5K줄 "No", phillipcarter·altern8, dev.to 200K "boundary narrowly"·3주차 이후 야간 자율 포기 루프, olsondv·petcat 주니어 논쟁, pstack README "the best spec is code") — community.md·web.md L183 일치
- 학술 3건(Bosu 2015 150만 건·파일 수↑ 유용 코멘트↓, Gloaguen ICLR 2026 성공률 불변·비용 20%+·개요 무용·비표준 관행 유용, Lulla 2026 10 저장소 124 PR·−16.58% 토큰) — papers.md 5-5·7-1·7-2 일치
- 도구 사실 5건(Spring Boot 4.0 모듈 분리·JSpecify·Java 25 지원 — web.md 자료 29; Next.js 15+ 비동기 request API — §4-3; Claude Code 2.1.277 AGENTS.md — web.md L435; Codex `project_doc_max_bytes` 32 KiB — web.md L470; 공식 문서 "context, not enforced configuration… PreToolUse hook" — web.md L439) — 일치
- Best practices CLAUDE.md 인용 3문장·토스 인용 — web.md L391–392·자료 50 일치
- GitHub #32650(2026-03-10, 100+ 세션 16건, 2,000단어, 인용 3문장)·#19471("✓ Rules loaded", "NOT a context length issue") — community.md L60·L76 일치
### 미해소
- (없음)

## 패턴 (1~3장 묶음)

- 1차 소스 이슈·문서의 **방향**을 요약문만 보고 뒤집어 쓰는 경향 — #15310은 "폴백"이라는 단어만 남고 어느 쪽으로 떨어졌는지가 반대로 서술됨. 이슈 번호가 인용될 때는 제목 한 줄을 원문에서 확인한다
- 도구 동작 설명을 기억으로 축약("읽기만", "편집만") — 권한 모드처럼 표로 정의된 사실은 문서 표의 열을 그대로 옮긴다
- 연도 상대 표현("같은 해", "다섯 달 뒤")이 앞 문장의 기준 연도와 어긋남 — 서로 다른 소스(METR 2025 / 워크숍 2026)를 한 단락에 붙일 때 절대 연도를 한 번은 박는다
- 비율·정도 부사("대부분", "절반", "손으로")가 원장에 없는 채로 붙음 — 자막·논문 요약에 없는 수식어는 뺀다
- research/community.md L188의 "#15310 read-only 폴백"은 같은 파일 L102·01_reference §3-3과 충돌하는 오기 — 후속 장에서 이 이슈를 인용할 때 주의

## 10장 (라운드 1)

### ❌ 정정
- Kim 2025 "기준선이 약 45%를 넘어야 조율의 이득이 나타났다" → "기준선이 약 45%를 넘으면 조율의 이득은 오히려 줄거나 사라졌다" — 근거: papers.md 6-2·01_reference §5-1 "단일 에이전트 기준선이 약 45%를 넘으면 조율 이득이 줄거나 음수". 방향이 반대로 서술됨
- dev.to 200K 모놀리스 "야간 실행이 무너진 것은 아침마다 diff 전체를 사람이 읽어야 했기 때문" → "본인들은 복잡한 사례의 실패율이 너무 높고 실패가 너무 미묘해서라고 적었다 — 커버리지 하락은 사흘 뒤에야 발견됐다" — 근거: 원문(dev.to, 2026-10-10 조회) "The failure rate on complex cases was too high and the failures were too subtle." 리뷰 부담은 원문이 든 이유가 아님(community.md L206 ③ "3일간 미발견"과 정합). 장의 논지(검증 레인이 사람을 못 대신함)는 유지
### ⚠️ 약화·삭제
- Agent teams "(2차 가이드의 약 7배 추정은 확인 필요)" → "(한 2차 가이드는 plan mode 대비 약 7배로 추정하지만, 공식 수치는 아니다)" — 01_reference §7-2 #18 미확인 항목. 본문에 "확인 필요"가 남지 않도록 닫고, 비교 기준(plan mode 대비, community.md L176)을 보강
### 🕒 신선도
- (추가 없음 — "2.1.x/2026-10 기준", "0.16x/2026-10 기준" 꼬리표 확인)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 마커 없음
- 자막 인용 9건([00:03:07]–[00:03:36] 백 개 불가, [00:26:41] 토큰 낭비, [00:28:01] 지름길 없음, [00:23:28]·[00:23:52]·[00:24:34] 로컬/클라우드 Q&A, [00:25:16]–[00:26:14] Benny·"이미 main에서 고쳐짐"·한 시간) — 자막 원문 일치
- 학술 3건(Brown 2024 SWE-bench Lite 15.9%→250회 56%·검증기 없는 수학 과제; Kim 2025 180 구성·17.2배·4.4배; Cemri 2025 1,600+ 트레이스·14종·3범주 "검증/종료") — papers.md 2-7·6-1·6-2 일치
- Claude Code 사실 7건(`--worktree` → `.claude/worktrees/<name>/`·`worktree-<name>`, `isolation: worktree`, `/batch` 5~30, 동시 20·깊이 3, `.worktreeinclude`, `--cloud`·`/autofix-pr`, Routines research preview·1시간·권한 모드 선택지 없음·Alert triage 초안 PR, Agent teams "significantly more tokens") — web.md 자료 12·16·17, 01_reference §3-2 일치
- Codex 사실 4건(서브에이전트 기본 활성, `.codex/agents/` TOML, `max_concurrent_threads_per_session`, 워크트리 격리 언급 없음; Codex Cloud 태스크별 워크스페이스; `codex cloud exec --attempts 1–4` experimental·`--env` 필요; 자동화 트리거) — web.md 자료 22·25·26 일치
- 커뮤니티·담론 5건(aakashx "isolated, scoped, and validated" 경고, Hashimoto "End-of-Day Agents", pstack 07-overnight, 200K 팀의 전환 루프 "이슈 1개 → 계획 승인 → 검증 스크립트 → diff 리뷰 → 머지", #19471 2026-01 압축 11회·#18720 2026-04 45분·`ACTIVE_CONTRACT.md`·AGENTS.md 자동 재독) — community.md L132·L206, 01_reference §3-5·§6-2 일치
- 모델명 본문 부재 확인
### 미해소
- (없음)

## 11장 (라운드 1)

### ❌ 정정
- 오프닝 "환경 변수 이름을 바꾸는 단순한 리팩터링을 에이전트에게 맡겼다 … 그리고 '다 했습니다'라고 보고했다" → "`replace_all`로 문자열 치환을 돌렸는데, 그 문자열이 상수 정의에도 들어 있었다 … 첫 번째 리뷰는 이것을 놓쳤고, 두 번째 리뷰 에이전트 라운드에서야 잡혔다" — 근거: HN 47661327 KaiLetov 원문(2026-10-10 조회) "Took a second round of review agents to catch it" / community.md L63 "상수 정의까지 바꿔". 과업 내용("환경 변수 이름 변경")과 완료 보고 장면은 원문에 없음
- Wataoka 뒤 "요약 과제에서 나온 결과이지" → "두 연구 모두 코드 리뷰에서 직접 측정된 결과는 아니지만(Panickssery의 실험은 요약 과제였다)" — 근거: papers.md 3-3(XSUM·CNN/DM 요약)은 Panickssery; 3-4 Wataoka는 과제 미기재. 귀속 위치 정정
### ⚠️ 약화·삭제
- Panickssery "그 관계가 선형이며 인과라는 것까지 확인했다" → "인과로 보는 설명이 단순한 교란 요인으로는 반박되지 않는다는 것까지 보였다" — 근거: arXiv 2404.13076 초록(2026-10-10 조회) "linear correlation … the causal explanation resists straightforward confounders"; papers.md 3-3 "인과 관계 시사". "확인"은 과장
### 🕒 신선도
- `(사실 확인 필요)` 해소 지점에 "0.16x/2026-10 기준" 꼬리표 추가. 그 외 "2.1.x·0.16x/2026-10 기준", "2026-10 기준"(플러그인 설치), "2026-03 공개, 2차 보도"(codex-plugin-cc) 확인
### ✅ 확인 (요약)
- `(사실 확인 필요)` 1건 해소: pre-push 훅의 `codex review --base main` 비대화형 실행 — learn.chatgpt.com/docs/developer-commands?surface=cli(2026-10-10 조회) "Run a non-interactive review of uncommitted changes, a base branch diff, a commit, or custom review instructions." → 비대화형은 확인. 출력 옵션(`-o`·`--json`·stdout 형식)은 `codex review`에 문서화되지 않음(`codex exec`에만 있음) → 스크립트는 확인된 플래그(`--base main`)만 유지하고, 파일 저장은 "셸 관례일 뿐, 자기 환경에서 돌려 보라"로 약화. 마커 제거
- `codex review` 플래그 3종(`--uncommitted`·`--base <branch>`·`--commit <SHA>`) — web.md 자료 22·공식 문서 일치
- 학술 3건(Huang ICLR 2024 외부 피드백 없는 자기 교정; Panickssery NeurIPS 2024 "자기 것" 라벨 효과; Wataoka 2024 perplexity; Parasuraman & Riley 1997 disuse) — papers.md 2-6·3-3·3-4·1-2 일치
- Osmani 인용 2건("한 모델의 복사본 넷은 청구서만 커진 리뷰어 하나", 4도구 146 PR 93.4% — "벤더 보고라 수치보다 방향" 한정어) — web.md 자료 48, 01_reference §9 (g) 등급과 일치
- 자막 [00:21:30] 다른 모델 judge 교차 — 일치
- GeekNews 29011 사실 6건(Claude 작성자/Codex 자문 리뷰어, slash command + pre-push 훅 같은 래퍼, 소규모 `codex review --base` vs 100파일+ `codex exec`+diff, "절대 차단하지 않는다"·`--no-verify` 유도, race condition·null 체크, CLAUDE.md/AGENTS.md 80% 겹침) — community.md L146, 01_reference §6-3 일치
- 병용 증언 4건(29576 gkhcdef 역할 대칭, HN petcat 리뷰어>구현자 — 모델명 생략 확인, ajh508 삼각 검증, 28538 14년차 vs 댓글 반론 C21 관점 병기) — 일치
- codex-plugin-cc 7건(공개일 2차 라벨, 설치 3줄, `/codex:review`·`adversarial-review`("questions the chosen implementation and design")·`rescue`·`transfer`, Stop 훅 긴 루프 경고 "(2차)") — web.md 자료 28, 01_reference §3-3 일치. Best practices "A reviewer prompted to find gaps will usually report some" — 자료 18 일치
- CLAUDE.md/AGENTS.md 상호 인식 7건(2.1.277, 기본 `claude-md-or-agents-md` CLAUDE.md 없을 때만, `/config`에서 `claude-md-and-agents-md`, Codex "Filenames not on this list are ignored", `project_doc_fallback_filenames = ["CLAUDE.md"]`, 디렉터리당 1파일·32 KiB, `@AGENTS.md` import, 심링크 Windows "(2차)") — web.md 자료 21·23, 01_reference §3-5 일치. `## Code Review Rules`·"포맷·린트는 CI에" — 자료 23·26 일치
- kavtsya #301 "두 모델이 일치한다고 정답 보장 안 됨", "왕좌" 담론 — community.md L160–161 일치
- 모델명 본문 부재 확인("부록 A의 표가 맡는다")
### 미해소
- (없음)

## 12장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (추가 없음 — "2026년 7월 기준 본인 보고", "2.1.x/2026-10 기준"(`total_cost_usd`), "dekita, 2026-10", "리서치 시점(2026-10)" 확인)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 마커 없음
- 월 PR 수 표기: "2026년 7월 기준 본인 보고로 약 1,000개(05:06), 이후 본인 발표 기준 2,000~2,500 — 외부 감사는 없다", "20개는 그날 아침(03:52)", "상당수는 gardening PR이라고 본인이 말했다" — 01_reference §1-2·§7-1 C1·02_plan 저술 제약과 정확히 일치
- 자막 인용 9건([00:03:52] 20 PR·"괜찮았다", [00:05:06] 1,000, [00:47:57]·[00:48:09]·[00:50:02]·[00:50:17] 토큰 Q&A, [00:54:13] PM stamp, [00:54:26] "Dune 아키텍처가 버티고 있다", [00:49:18]–[00:49:31] 에이전트의 가치·"몇 년", [00:28:59] 신뢰 정의) — 자막 원문 일치
- GitHub 이슈 2건(claude-code #16157 2026-01 1,499 댓글·제목 "Instantly hitting usage limits with Max subscription"·Saprissa 45분; codex #14593 2026-03 630 댓글 "Burning tokens very fast") — community.md L93–94 일치
- GitHub auto-merge/merge queue 3건("all required reviews and status checks pass", "must be enabled for the repository", `merge_group`) — web.md 자료 42 일치. 공식 Code Review "don't approve or block" — 자료 19 일치
- pstack autopilot 5건(소유 에이전트 자기 판정 머지 불가, 독립 검증자, 트렁크 리베이스 head CI 그린·push마다 재검증, 아침 히스토리 샘플링·revert·린트 추가, 시작점 autopilot-stack → autopilot-full, 위험 도메인 "답이 없다") — community.md L253 일치
- 반대 관점 4건(dekita "작고 범위 명확한 변경만"·"재작업 측정" + 벤더 보고 한정어, Osmani "머지를 누른 사람이 소유"·"센서", The Register "10개 중 1개만 적법", 에이전트 PR 차단 저장소) — 01_reference §6-6 A·B, 자료 48 일치
- 비용 계기판 4건(`claude -p --output-format json` → `total_cost_usd`; Code Review $15–25·20분(공식 문서 수치, "오탐 1%"는 미사용 확인); Verga 2024 패널·비용 1/7 이하; Agent teams "significantly more tokens") — web.md 자료 13·17·19, papers.md 3-5 일치. Lulla 2026 "실행 시간과 출력 토큰이 준다" — papers.md 7-2 일치(수치 미기재로 중앙값 쟁점 없음)
- 조직 5건(커뮤니티 가이드 마케팅 카피·컬러 토큰·"do not touch"·결제/권한/고객 데이터, 주니어 논쟁 양측, 토스 "CLAUDE.md를 자주 수정하고 있다면…"·하네스, LY "조직의 기준을 따르는 리뷰어", 대기업 회고 미발견) — 01_reference §6-6 C·D, §6-8, §9 일치
- 모델명 본문 부재 확인("최상급이 아닌 모델"은 자막 "not fable size"의 의역, 모델명 아님)
### 미해소
- (없음)

## 패턴 (10~12장)

- **논문 수치의 방향 뒤집힘** — Kim 2025의 "45% 임계값"이 "넘어야 이득"으로 서술됨(원문은 "넘으면 이득 감소"). 임계값·비율이 등장하면 어느 쪽이 좋아지는지를 원장 문장과 한 번 더 맞춘다
- **커뮤니티 장면의 서사 보강** — HN 사례에 과업 내용("환경 변수 이름 변경")과 대사("다 했습니다")가 덧붙고, dev.to 사례에 원문에 없는 인과("아침마다 diff를 읽어야 해서")가 붙음. 오프닝 장면은 원장의 짧은 발췌 범위 안에서만 쓰고, 이유·대사는 원문에 있는 것만 쓴다
- **"확인 필요"를 본문에 남기는 습관** — Agent teams 7배 항목이 괄호 안에 "확인 필요"로 남음. 2차 수치는 "공식 수치는 아니다" 같은 닫힌 한정어로 쓴다
- **인접한 두 논문의 조건 귀속** — Panickssery(요약 과제)의 조건이 Wataoka 문장 뒤에 붙음. 한정어는 해당 논문 바로 뒤에 둔다
- **"시사"를 "확인"으로 격상** — papers.md가 "인과 관계 시사"로 적은 것을 "인과라는 것까지 확인"으로. 원장 등급 어휘(시사/확인/추정)를 그대로 옮긴다
- 양호: 월 PR 수·4단계 주체·자막 타임스탬프·도구 버전 꼬리표·2차 라벨(codex-plugin-cc 공개일, 심링크 Windows, Osmani 93.4%, dekita 수치)·모델명 부재는 세 장 모두 저술 제약대로 지켜짐

## 07장 (라운드 1)

### ❌ 정정
- "3장에서 본 Java 쪽 실패 … 토비의 라이브 코딩에서 … 바로 그 장면이다" → "3장에서 신호로 적어 둔 Java 쪽 실패 … 장면이기도 하다" — 근거: 03_final.md에는 "목으로 바꾸겠다는 말"이 관찰 신호로만 나오고, 토비가 Mockito→`@SpringBootTest`+롤백으로 규칙을 바꾼 장면(community.md L116)은 없음. 교차 참조만 고치고 사실(토비 gist)은 유지
- "1페이지로 줄이라던 3장의 원칙" → "한 페이지로 줄이라던" — 03_final.md L59·L71 표기와 일치시킴
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (추가 없음 — "0.16x/2026-10 기준", "2.1.x/2026-10 기준", "2.1.295부터 … (2026-10 기준)" 꼬리표 확인)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 1건 해소: `/skill-doctor`가 짚어 주는 것 — code.claude.com/docs/en/skills(2026-10-10 조회) "Run `/skill-doctor` to see what each of your skills costs and how often it gets used … It flags skills in the listing that have never been invoked", "requires Claude Code v2.1.252 or later" → 컨텍스트 비용·호출 빈도·미호출 스킬 보고로 구체화하고 마커 제거
- 자막 인용 11건([00:15:20] 무력감, [00:15:33] 매니저 비유, [00:16:01] "just markdown", [00:16:17] latent space·다음 토큰, [00:17:52] 프레임워크 불필요, [00:14:11] 축적, [00:14:27]–[00:16:59] `how` 유래, [00:20:08] 백시트 드라이버, [00:28:30] 맹목 신뢰 반대, [00:28:46] "fork it make it your own", [00:28:59] "different standard for engineering") — 자막 원문 일치
- 도구 사실 9건(Codex `name`·`description` 필수, Claude Code `description`으로 로드 판단 — 공식 문서 "The `description` helps Claude decide when to load the skill automatically"; frontmatter `disable-model-invocation`·`allowed-tools`·`context: fork`·`hooks`; `.claude/skills/`·`.agents/skills/`(상위 디렉터리 탐색)·Agent Skills 표준; 본문 지연 로드; CLAUDE.md "context, not enforced configuration"; 훅 이벤트·exit 2·"advisory vs deterministic" 인용·"PreToolUse 훅을 쓰라"; 2.1.295 `onFailure: "block"`; Codex 이벤트 훅 미확인·`--sandbox`/`-a never`) — 01_reference §3-2·§3-3·§3-5, web.md 자료 9·11·18·24 일치
- 인용 5건(Best practices "delete it or convert it to a hook", HN blamestross positive phrasing, 토스 컴포넌트/매니페스트, 공식 "Seeing a skill trigger…", Vercel 56%(2026-01, 2차)) — web.md L391, community.md L78·L121, 01_reference §6-8 일치
- pstack 2026-05-23·MIT·URL·수록 스킬 4종, gstack `./setup --host codex`, control-glass 부재·`control-ui`/`control-cli`(cursor-team-kit) — 01_reference §2-2 일치. 계획 제약("pstack의 control-glass" 금지) 준수 확인
- 3장 교차 참조: "실패 3개"(03_final L71 "실패 세 개"), "✓ Rules loaded"(L67) 일치
### 미해소
- (없음)

## 08장 (라운드 1)

### ❌ 정정
- 오프닝 "80문항 중 66문항에서 판정이 뒤집혔다" → "80문항 중 66문항에서 뒤처지던 쪽이 이겼다" — 근거: papers.md 3-2 "순서만 바꿔 Vicuna-13B가 ChatGPT를 80문항 중 66문항 이기게 만들 수 있었다". 66건 전부가 '뒤집힌' 판정이라는 보장은 원문에 없음. 뒤따르는 문장의 중복 수식어("당시 평가에서 뒤처지던") 제거
- "요약 과업에서 관측된 결과라" (Wataoka 문장 뒤) → "Panickssery의 실험은 요약 과업이라" — 근거: papers.md 3-3 요약 과업(XSUM·CNN/DM)은 Panickssery; Wataoka 3-4는 과업 미기재
- "Claude Code 쪽 skill-creator 글" → "Anthropic의 skill-creator 글" — web.md 자료 20 출처 claude.com/blog
### ⚠️ 약화·삭제
- "두 선택지 모두 이 둘[다른 모델 judge·작업자 블라인드]을 만족" → A만 둘 다 갖추고 B는 judge 쪽 블라인드로 대신한다고 분리; "둘 다 블라인드이고" → "둘 다 judge를 블라인드로 둔다" — 근거: plugin-evals 공식 문서(2026-10-10 조회)는 격리 워크스페이스만 기술하고 작업 세션이 평가 사실을 모르는지는 말하지 않음. 블라인드 근거(web.md 자료 20 "They judge outputs without knowing which is which")는 judge 쪽
### 🕒 신선도
- (추가 없음 — "2.1.x/2026-10 기준", "2.1.269+, 2026-10 기준" 꼬리표 확인. 모델명 본문 부재 확인)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 1건 해소: `claude plugin eval` 대상 — code.claude.com/docs/en/plugin-evals(2026-10-10 조회) Requirements "A plugin directory with a `plugin.json` or `.claude-plugin/plugin.json` manifest, or a skills-directory plugin"; "For iterating on one skill inside a Claude Code conversation, the skill-creator plugin runs a similar comparison with its own `evals/evals.json` format" → 대상 조건을 구체화하고 skill-creator 대안을 병기, 마커 제거
- 학술 7건(Wang ACL 2024 66/80; Zheng NeurIPS 2023 편향 4종·위치 일관 60%↑ 1개 모델; Panickssery NeurIPS 2024 선형·인과·라벨; Wataoka 2024 perplexity; Needham 2025 61 데이터셋·1,000 프롬프트·AUC 0.83/0.92; van der Weij ICLR 2025 위험 역량 맥락 한정; Verga PoLL 비용 1/7 이하) — papers.md §3, 01_reference §5-1 일치. 계획 제약(sandbagging 일반화 금지) 준수
- SWE-bench Verified 1,699→93명→500(OpenAI 2024-08) — papers.md 2-1 일치
- 자막 인용 7건([00:18:28] "unit test your skills", [00:18:46]–[00:19:52] 파이프라인, [00:19:03] 디렉터리 이름, [00:21:30] 다른 모델 judge, [00:19:52] 수정마다 실행, [00:21:46]–[00:22:00] `/loop` 10/10, [00:21:15] verify the verifier) — 자막 원문 일치
- Claude Code 사실 8건(`/goal` fresh model·Stop 훅 래퍼·평가자 명령/파일 미접근; `/loop 20m /review-pr 1234`·최소 1분·7일 만료; 그레이더 6종·커스텀 없음; 기본 3회×with/without=6런; `--judge-model`; 임계값 미달 시 0이 아닌 종료 코드(exit 1); `file_exists` 권고; "`tool_used: Skill` … Δ … suspect the judge" 인용) — web.md 자료 15·20 + 공식 문서 재확인 일치
- Codex `/goal`·`/loop` 대응 미확인·`codex exec --json -o` 셸 루프 — 01_reference §3-5, 계획 제약 일치
- skill-creator 블로그(2026-03-03) 인용 — web.md 자료 20 일치
### 미해소
- (없음)

## 09장 (라운드 1)

### ❌ 정정
- "10년 뒤 Google은" → "10여 년 뒤" — Bacchelli & Bird 2013 → AutoCommenter 2024(papers.md 5-4·5-7)
- "Adapter 16개" → "Adapter·Bridge 16개" — 근거: community.md L206 "Adapter/Bridge 16개"
- NullAway "`-Werror`와 함께 쓰면 … 기본 심각도는 경고라서 `check(...)`로 올려야" → "기본 심각도는 경고라서 `check("NullAway", CheckSeverity.ERROR)`로 올리거나 `-Werror`를 함께 걸어야" — 두 수단이 각각 독립적으로 빌드를 깨뜨리므로 '함께 써야' 하는 관계가 아님
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (추가 없음 — "2.1/2026-10 기준"(Modulith), "Next.js 16 기준", "2026-10 기준, research preview"(Code Review) 꼬리표 확인)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 1건 해소: NullAway Gradle 구문 — uber/NullAway README(2026-10-10 조회): `import net.ltgt.gradle.errorprone.CheckSeverity` … `check("NullAway", CheckSeverity.ERROR)`; "sets NullAway issues to the error level (it's equivalent to the `-Xep:NullAway:ERROR` standard Error Prone argument); by default NullAway emits warnings"; "built as a plugin to Error Prone and can run on every single build of your code" → 구문·기본 경고 확인, 마커 제거. (README 최소 Error Prone 2.36.0 — web.md 자료 33의 "2.14.0"은 구버전 표기, 본문 미인용이라 영향 없음)
- 자막 인용 16건([00:46:18]·[00:46:35]–[00:47:02] 코드 리뷰 랜드·code smell, [00:42:13] 여러 층, [00:42:27] 가장 강한 집행·패턴 복사, [00:44:50] CI red·forget, [00:45:07] "only source of enforcement"·complete trash, [00:43:34] shortest path, [00:43:20] dumbest agent, [00:44:03] 비공개, [00:42:41] 명사 3종, [00:41:37] 임포트 경계, [00:31:01] human slop, [00:39:09] 박제 주석, [00:31:58]·[00:32:52]–[00:33:24] 그린필드, [00:29:27] 리라이트, [00:45:36] Rust, [00:22:48] 헤드 셰프) — 자막 원문 일치. Dune 세부는 자막 범위(feature/entry point/transcript card·금지 목록·임포트 경계)만 사용 — 계획 제약 준수
- 학술 5건(Bacchelli & Bird ICSE 2013; AutoCommenter 약 80만 건; Distefano CACM 2019 near-zero vs 70%+ — ⚠️ 2차(TechBeacon·InferFix) 명시 유지; Sadowski CACM 2018 FindBugs 3회 실패·오탐 불신; GitClear 2025 8배(2차 보도)) — papers.md §5, 01_reference §5-1·C19 일치
- 담론 4건(Willison 2026-08, Thoughtworks Radar 2026-04 "결정론적 품질 게이트"(요약), GeekNews GN#347, React 19.2 블로그 "most users just disable the lint rule") — web.md 자료 36·44·47·52 일치
- 도구 사실 9건(GitHub Code Review "don't approve or block your PR"; Modulith `verify()` 규칙 3종; ArchUnit `layeredArchitecture()`·네이밍; Spring 함정 목록 3종; boundaries `boundaries/dependencies`; dependency-cruiser·Xebia 2026-06 Ghost; knip; Next.js 16 `next build` 린트 미실행; `react-hooks/exhaustive-deps: error`+`no-restricted-syntax`) — 01_reference §3-2·§4-2·§4-3 일치
- 교차 참조: "5장의 트랜잭션 경계 변경"(05_draft L143), "5장의 `quickCheck`"(05_draft L43) 일치
### 미해소
- (없음)

## 패턴 (7~9장)

- **앞 장 교차 참조가 '그 장에 실제로 있는 것'보다 넓게 쓰임** — 7장의 "3장에서 본 토비 Mockito 장면"은 3장 final에 신호 한 줄로만 있음. 뒤 묶음을 쓸 때 "N장에서 본"은 그 장의 final을 열어 해당 문장이 있는지 확인한다. 9장의 "6장에서 확인한 셀렉터"는 06_final 부재로 미대조 — editor 확인 필요
- **한정어(hedge)가 엉뚱한 문장에 붙음** — 8장에서 "요약 과업" 한정이 Panickssery가 아니라 Wataoka 뒤에 옴. 논문 두 편을 연달아 쓸 때 한계 서술은 해당 논문 바로 뒤에 둔다
- **두 선택지를 '둘 다 만족'으로 묶는 대칭 서술** — 8장의 "둘 다 블라인드"는 A(작업자 블라인드)와 B(judge 블라인드)가 다른 뜻. 비교표형 서술에서 같은 단어가 양쪽에서 같은 뜻인지 본다
- **공식 문서 인용의 소속 표기 축약** — "Claude Code 쪽" 블로그(실제는 Anthropic claude.com)처럼 출처 조직을 제품명으로 뭉뚱그림. 레퍼런스의 출처 URL 도메인으로 확인한다
- **두 독립 수단을 '함께 써야' 관계로 묶음** — 9장 NullAway의 `CheckSeverity.ERROR`와 `-Werror`는 각각 단독으로 빌드를 깨뜨림. 설정 두 개를 나열할 때 and/or를 가린다
- 2차 검색 요약(web.md 자료 33 "Error Prone 2.14.0 이상")이 현행 README(2.36.0)와 어긋남 — 본문 미인용이라 무해했지만, 자료 33을 인용하는 장이 있으면 README로 재확인

## 04장 (라운드 1)

### ❌ 정정
- 오프닝 "143개 클래스 가운데 127개를 손댔고, 아침에 열어 본 PR은 깨끗했다. 에이전트는 '완료했습니다'라고 보고했고, 팀은 머지했다" → "네 모듈로 옮겨야 할 143개 클래스 가운데 127개를 첫 밤에 제대로 옮겼고, 아침에 엔지니어들이 diff를 리뷰했다. 테스트는 계속 초록이었다" — 근거: dev.to 원문(2026-10-10 조회) "We had 143 classes to relocate across the 4 modules." / "Claude Code did 127 of them correctly in the first overnight run." / "Engineers would review in the morning." 127은 '손댄 수'가 아니라 '맞게 옮긴 수'이고, '완료했습니다' 보고·PR·머지 장면은 원문에 없음(community.md L206 "143 클래스 중 127(89%) 첫 야간 실행에서 정상"과 정합)
- 본문 3곳의 "127개 클래스"(밤새 돌아간 / PR에 도장 / 리뷰 범위) → "143개 클래스" — 위 정정에 맞춰 작업량 수치를 통일. "PR에 도장을 찍은 팀" → "diff를 사흘 동안 다 읽어 내지 못한 팀"(원문 "We didn't catch this for 3 days")
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (추가 없음 — "2.1.x/2026-10 기준"(베스트 프랙티스·게이트 4단), "2.1.286(2026-09-30)", "2.1.139", "2.1.295(2026-10-08)", "2026-10 기준"(Codex `/goal` 대응 미확인) 꼬리표 확인)
### ✅ 확인 (요약)
- `(사실 확인 필요)` 마커 없음
- 자막 인용 6건([00:06:10] 검증 정의·iOS 시뮬레이터, [00:06:29] 맞는 코드/좋은 코드, [00:07:05]–[00:08:36] 첫 주·출시 1주 전·플레임 그래프 스크린샷·"confidently state … not the actual thing", [00:08:48]–[00:09:13] 로컬 빌드·콘솔 에러 복사·병목·"no way to parallelize") — 자막 원문 일치
- dev.to 200K 사실 7건(12년 금융 Spring Boot 모놀리스·8명·400줄 CLAUDE.md·68→61%·사흘·`@Transactional` 소실→부분 결제 실패 감사 로그·QA 발견·"find the exact edge of your success criteria and stop there"·"A human must review any transaction boundary change") — community.md L206 + 원문 일치
- 학술 5건(Huang ICLR 2024 외부 피드백 없는 자기 교정 악화; Self-Debug Chen ICLR 2024 단위 테스트 최대 +12%p·없으면 +2~3%p; Reflexion Shinn NeurIPS 2023 HumanEval 91% + 테스트 피드백 병기; Bansal CHI 2021 수용↑·정확도 불변; Vasconcelos 2023 5연구 731명·비용 대비 선택) — papers.md·01_reference §5-1 일치. "FAccT" 혼동 없음(Wang 미인용)
- Hashimoto "verify its work … fixes its own mistakes and prevents regressions"(web.md L710), VibeTDD 변명 인용·`shouldThrow→shouldNotThrow`(community.md L68) — 일치
- Claude Code 사실 9건(베스트 프랙티스 "check it can run"·"you become the verification loop"·"session you watch / walk away from"; `verify` 스킬 2.1.286 커밋 전·"show evidence rather than asserting success"; 게이트 4단; `/goal` 2.1.139 fresh 모델·명령/파일 미접근·`test/auth` 예시; Stop 훅 exit 2·`{"decision":"block","reason":"Test suite must pass before proceeding"}`; 2.1.295 `onFailure: "block"`; 검증 서브에이전트 "won't be biased"·"reviewer prompted to find gaps") — 01_reference §3-2 일치
- Codex 3건(`/goal` 공식 대응 미확인, `codex exec -s workspace-write -a never`, `codex exec resume --last`, `learn.chatgpt.com/docs`(구 developers.openai.com/codex)) — §3-3·§3-5 일치
- 용어 표기: "Lauren Tan(Cursor, React Compiler 코어팀)" 첫 등장·직함 없음, 모델명 본문 부재
### 미해소
- (없음)

## 05장 (라운드 1)

### ❌ 정정
- "여기도 Boot 4의 이름 변화가 있다. 의존성은 `spring-boot-testcontainers`·`testcontainers-junit-jupiter`·`testcontainers-postgresql`이고 … `org.testcontainers.postgresql.PostgreSQLContainer`" → "Boot 4.1이 가져오는 Testcontainers 2.x(2026-10 기준)에서는 …" — 근거: 스크래치 Gradle 캐시에 `org.testcontainers:testcontainers-postgresql:2.0.5`·`testcontainers-junit-jupiter:2.0.5`가 Boot 4.1.1 BOM으로 해석됨(버전 미명시). 아티팩트·패키지 개명의 주체는 Testcontainers 2.0이지 Spring Boot가 아님. 이름 자체는 initializr-tc 스크래치(Initializr 생성본)와 일치
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- "저술 시점에 …" 4곳(Boot 3 경로 컴파일 실패 / `quickCheck` 4초·통합 테스트 13초 / Modulith 위반 메시지 / NullAway 메시지) → "저자 실측(2026-10 기준)" 꼬리표로 교체. Boot 3 경로 실패는 실제 컴파일러 메시지(`package org.springframework.boot.test.autoconfigure.web.servlet does not exist`)를 명시
- `withReuse(true)` 문장에 Testcontainers 문서(2026-10 기준)의 "실험적 기능·CI 비권장" 한정 추가
### ✅ 확인 (요약)
- `(사실 확인 필요)` 1건 해소: `~/.testcontainers.properties`의 `testcontainers.reuse.enable=true` — java.testcontainers.org/features/reuse(2026-10-10 조회) "through user property file `~/.testcontainers.properties`, by adding `testcontainers.reuse.enable=true`", 환경 변수 `TESTCONTAINERS_REUSE_ENABLE=true` 병기, "still an experimental feature", "not suited for CI usage" → 확인·보강, 마커 제거
- 저자 실측 재현(스크래치 `scratchpad/spring-check`, 2026-10-10): (a) `build.gradle` = Boot 4.1.1·Java 25 toolchain·Gradle 9.7.1(wrapper)·`spring-boot-starter-webmvc-test`·`spring-boot-starter-data-jpa-test`·Modulith 2.1.1 ✓; 슬라이스 애노테이션 패키지는 4.1.1 jar 목록으로 확인(`org/springframework/boot/webmvc/test/autoconfigure/WebMvcTest.class`, `org/springframework/boot/data/jpa/test/autoconfigure/DataJpaTest.class`); Boot 3 경로로 바꿔 `compileTestJava` → "package … does not exist" 재현 ✓ (b) `@TestConfiguration(proxyBeanMethods=false)`·`@ServiceConnection`·`PostgreSQLContainer(DockerImageName.parse("postgres:17-alpine")).withReuse(true)`·`@SpringBootTest(RANDOM_PORT)`+`@Import`+JDK `HttpClient` — 스크래치 소스와 일치 (c) `net.ltgt.errorprone` 5.1.1·`error_prone_core` 2.50.0·`nullaway` 0.14.2 캐시 해석 ✓; `disableAllChecks`·`check('NullAway', CheckSeverity.ERROR)`·`-Werror` 설정 일치; `@Nullable` 반환 역참조 컴파일 → `error: [NullAway] dereferenced expression 'find(id)' is @Nullable` 재현 ✓; `./gradlew quickCheck --rerun-tasks` 4.45초(time) ✓; `OrderApiIT` JUnit XML `time="13.086"` ✓ (d) `order`→`billing.internal.BillingCalculator` 주입 → quickCheck XML "Module 'order' depends on non-exposed type com.example.demo.billing.internal.BillingCalculator within module 'billing'!" 재현 ✓. 스크래치는 원상 복구·컴파일 확인
- codenote 2026-01 수치 5건(3~5분·JVM/빈/Testcontainers·"대화가 멈춘다"·`@SpringBootTest` 5~15s·`@WebMvcTest` 0.3~0.8s·`@DataJpaTest` 0.5~1.5s, "단일 저자 측정" 한정) — community.md L202 일치. `gradle.properties` 4줄 — 스크래치 일치
- Spring Boot 4 모듈 분리·JSpecify 채택·"4.1/2026-10 기준" — 01_reference §4-1 일치. Modulith `verify()` 규칙 3종·`@ApplicationModule(allowedDependencies)`·"2.1/2026-10 기준"; ArchUnit `layeredArchitecture()`·네이밍·"1.5.x/2026-10 기준"(§4-1 1.5.1)·정량 효과 미주장 — §4-2·계획 제약 준수
- `create-verification-skill` "plain HTTP for services" — web.md 자료 2 일치
- 자막 [00:45:36]–[00:46:02] Rust·unsafe — 일치. 4장 교차 참조(Adapter·Bridge 16개·2주 뒤 프로덕션 버그·트랜잭션 경계 사람 리뷰) — §6-4 일치
- JavaGuide 2026-01 함정 4종("Resume does not exist: ID=35"·`REQUIRES_NEW` `this` 호출·JSON NPE·`XACK`) — community.md L207 일치. 토비 gist 인용 2건·`@PrePersist` — community.md L117·L208 일치. N+1·fetch join+Pageable — §4-2 ③ 일치
### 미해소
- (없음)

## 06장 (라운드 1)

### ❌ 정정
- "같은 글은 … 스크린샷으로는 안 보이는 실패(눌리지 않는 버튼, 두 번 나가는 요청, 콘솔의 에러)를 나눈다" → "스크린샷으로는 안 보이는 실패(콘솔의 에러, 버튼처럼 생겼지만 버튼이 아닌 요소)를 나눈다. 오프닝의 눌리지 않는 버튼과 비어 있는 네트워크 탭도 후자 쪽이다" — 근거: qaskills 원문(2026-10-10 조회)은 보이지 않는 실패로 콘솔 에러("A page can look perfect and still be broken")와 시맨틱(버튼 역할 div, "the one screenshots can never catch and the accessibility tree always can")만 들고, 눌리지 않는 버튼·중복 요청은 없음. 오프닝 장면은 저자 가상 예시이므로 출처 귀속만 분리
- ESLint 설정 코드 블록에 `languageOptions`(ecmaVersion·sourceType·`ecmaFeatures.jsx`) 4줄 추가 — 근거: "실제로 돌려 확인한 것"이라고 적은 설정은 스크래치 `eslint.config.mjs`이며, 거기엔 이 블록이 있음. 이것 없이는 기본 파서가 JSX를 읽지 못해 지면의 설정으로는 재현되지 않음
### ⚠️ 약화·삭제
- "그 기능이 UI 어디에 있는지 몰라서 아무 데나 클릭했다" → "눌러야 할 곳을 찾지 못했다" — 자막 [00:11:02] "I just try to click here. It wouldn't know how to get to things"는 Lauren이 직접 클릭해 보는 장면이지 에이전트의 무작위 클릭이 아님
### 🕒 신선도
- "실제로 돌려 확인한 것이다" → "(저자 실측, 2026-10 기준)" 꼬리표. 그 외 "2026-10 기준"(MCP 두 개), "Next.js 16(2026-10 기준)", "Storybook(10.x/2026-10 기준)" 확인
### ✅ 확인 (요약)
- `(사실 확인 필요)` 마커 없음
- 저자 실측 재현(스크래치 `scratchpad/eslint-check`, 2026-10-10): `node_modules` eslint 10.12.0·eslint-plugin-react-hooks 7.1.1 ✓; `npx eslint src` → `src/Bad.jsx` 5:3 `no-restricted-syntax`(useEffect)·7:6 `exhaustive-deps`·8:3 `no-restricted-syntax`(React.useEffect) 3 errors, `src/effects/Allowed.jsx` 통과 ✓ — 본문 서술("둘 다 error, `src/effects/` 통과")과 일치. 셀렉터 `CallExpression[callee.name='useEffect']`·`CallExpression[callee.property.name='useEffect']` 그대로 수록(01_reference §7-2 #19 해소)
- 자막 인용 7건([00:09:26] control-glass·"code itself is not super interesting", [00:10:34] "no idea what the agent's window was", [00:10:34] "left sidebar is laggy", [00:11:02] "completely useless", [00:12:02]–[00:12:31] Slack 채널·"???"+스크린샷 재현, [00:12:43]–[00:13:10] 지도 내용(서브 기능·진입 경로·단축키·DOM 속성), [00:13:10] `maintain-verification`, [00:38:09]–[00:38:24] foot gun·"in Dune and in Grok Bot we've banned use effect") — 자막 원문 일치
- qaskills 2026-08 "confidently declare success on a broken page" + 보이는 실패 목록 — community.md L64·L243·원문 일치. 토비 gist React effect 이중 발화→리마인더 이중 생성 — L208 일치
- pstack 사실 6건(control-glass 비공개·공개 대응물 `control-ui`(cursor-team-kit); `verification-skill-example` "Heavily fictionalized"·Atlas/Harbor Labs·"The shape is what matters"·H2 4종; "Each file answers, from the user's point of view: what the feature is, how to reach it, how to drive it with the harness, and what observable end state proves it works"; proof standards 3항; "A generated skill that was never executed is a draft, not a deliverable"; 위키 vs 스킬 토큰) — web.md 자료 2·4, 01_reference §2-2 일치. 계획 제약("pstack의 control-glass" 금지) 준수
- 도구 사실 8건(Playwright MCP 접근성 트리·`browser_snapshot` "better than screenshot"·도구 5종·`claude mcp add playwright npx @playwright/mcp@latest`·`codex mcp add`; Chrome DevTools MCP "control and inspect a live Chrome browser"·트레이스; Next.js 16 DevTools MCP 통합 로그·에러 자동 접근; stevekinney 스냅샷 토큰 "단일 저자 측정"·HN bughunter3000 "token burner"; Next.js 16 `next lint` 제거·"`next build` no longer runs linting"; `@next/eslint-plugin-next` Flat Config·ESLint v10; theroadtoenterprise 2026-05 1위 `useEffect`+`useState` 페칭·stale/Strict Mode 이중 요청/중복 제거 없음; React 19.2 "most users just disable the lint rule … can lead to bugs"; Storybook+Chromatic "UI Tests" required·"prevent accidental UI bugs from being merged") — 01_reference §4-1·§4-3·§6-5, web.md 자료 40·41 일치
- Next.js 15+ 비동기 request API(`cookies()` await) — §4-3 ③ 일치
### 미해소
- (없음)

## 패턴 (4~6장)

- **"저술 시점" 실측의 꼬리표 누락** — 4건 모두 재현됐지만 "저술 시점에"는 시점이 없는 표현. 저자 실측은 "저자 실측(2026-10 기준)"으로 통일하고, 재현 가능한 오류 메시지는 메시지 자체를 싣는다
- **지면의 코드와 실제로 돌린 코드의 차이** — 6장 ESLint 설정에서 `languageOptions`가 빠짐. "실제로 돌려 확인"이라고 쓰는 코드 블록은 스크래치 파일을 그대로 옮기고, 보기 좋게 줄인 부분이 재현성을 깨는지 본다
- **원장 숫자의 역할 바꿔치기** — 4장 "127개"가 '맞게 옮긴 수'에서 '손댄 수'로 바뀌고, 그 위에 PR·보고·머지 장면이 덧붙음(10~12장 패턴 "커뮤니티 장면의 서사 보강"과 같은 계열). 숫자가 세는 대상(전체/성공/실패)을 원문 한 문장으로 못 박는다
- **변경 주체의 오귀속** — 5장 Testcontainers 아티팩트 개명을 "Boot 4의 변화"로 씀. 버전 꼬리표가 붙는 사실은 어느 프로젝트의 릴리스가 바꿨는지를 분리한다
- **"같은 글"에 저자 가상 예시를 섞음** — 6장 qaskills 목록에 오프닝 장면(눌리지 않는 버튼·중복 요청)이 들어감. 출처 인용 목록과 저자 예시는 문장을 나눈다
- 양호: 자막 인용 13건·학술 5건·공식 문서 사실 17건·버전 꼬리표·계획 제약(control-glass 비공개·ArchUnit 정량 금지·모델명 부재·Codex 대응 미확인)은 세 장 모두 지켜짐. 7~9장 패턴의 "6장 셀렉터" 미대조는 06_final에 셀렉터가 실려 있어 해소
