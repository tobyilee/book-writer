# factcheck_log — ai-native-sdlc-playbook (tech-book)

장별 판정은 끝나는 즉시 append. 라벨: ❌ 정정 / ⚠️ 약화·삭제 / 🕒 신선도 / ✅ 확인 / 미해소. 근거 번호는 `01_reference.md`·`research/*.md` 기준.

## 01장 (라운드 1)

### ❌ 정정
- "Anthropic은 2026년 7월 자사 보안 블로그에서" → "Anthropic의 Jason Clinton(Deputy CISO)은 2026년 7월 회사 블로그에 쓴 글에서" — 근거: web.md 자료 24 (claude.com/blog, 별도 '보안 블로그' 아님)
- "이 코스의 블로그판(claude.com, 2026-08-21)은 이렇게 시작한다" + 귀속 "코스 레슨 1" 불일치 → "코스 레슨 1은 이렇게 시작한다. 블로그판도 같은 문장으로 문을 연다" — 근거: primary/01_introduction.md·99_claude-com-blog.md 둘 다 같은 첫 문장
### ⚠️ 약화·삭제
- "리뷰의 상당 부분을 자동화해서 얻은 결과라는 것이 그 글의 요지다" → "그 글이 전하는 맥락이다" — 16%→54%의 인과를 글의 '요지'로 단정할 근거가 web.md 자료 24 요약에 없음(수치 나열 수준)
### 🕒 신선도
- (없음 — DORA 2024(2024-10-23)·2025(2025-09-23)·2026(2026-03) 연도 병기, METR "2025년 초 도구", Cui "Management Science 2026", "자가 보고"·"프리프린트" 표기 모두 초안에 이미 있음)
### ✅ 확인 (요약)
- 수치 18건: METR 16명/246과제/5년/24%/20%/19%/Cursor Pro·Claude 3.5·3.7 Sonnet(papers 논문 2 초록 일치), Peng 55.8%(논문 1), Cui 4,867명/26.08%/표준오차 10.3%/기업 3곳(논문 3 초록), Google 96명/약 21%/신뢰구간(논문 4 초록), Zhang·Jiang·Koziolek 11,097개/+5.3%(논문 37 초록), DORA 2024 +7.5/+3.4/+3.1/−1.5/−7.2/39%(web 자료 28), DORA 2025 약 5,000명/90%(자료 29), Anthropic 80%·16%→54%(자료 24, 자가 보고 표기 확인)
- 인용 7건: 코스 레슨 1 표 12셀 + "Humans remain accountable" 원문 글자 단위 일치(스크립트 대조); 블로그판 "three things become true" 3항 원문 일치; GeekNews 27700 @bus710 댓글 원문 일치(community P5); LY Tech-Verse 2026 인용 원문 일치(web 자료 38); Ziegler MAPS '22 요지 일치(논문 6); DORA 2026 Balancing 문구 4건 일치(자료 30); Google 저자 경고문 번역 일치
- 서지 7건: Becker·Rush·Barnes·Rein 2025 arXiv 프리프린트 / Peng 외 2023 arXiv / Cui 외 Management Science 2026 심사 통과 / Paradis 외 ICSE-SEIP 2025 / Ziegler 외 MAPS '22 / Zhang 외 2026 arXiv 프리프린트 / 코스 독자 "엔지니어링·플랫폼·보안 리드"·규제 대기업 — 레퍼런스 7.5·1.1과 일치. 참고문헌 #7(DORA 연도 병기) 요건 충족.
- 레퍼런스 8장 한계 저촉 없음(한국 대기업·망분리 단정 없음; 한국 사례는 GeekNews·LY만)
### 미해소
- (없음)

## 02장 (라운드 1)

### ❌ 정정
- ".md인 이유를 코스는 ~ 설명한다" → "코스 블로그판은" — 해당 문장은 코스 레슨에 없고 블로그판(primary/99)에만 있음
- "파일 열다섯 개쯤" ×2 → "파일 스무 개 안팎" — 레퍼런스 3.1 파일 체인 표를 세면 20개 이상(intent·spec·plan·CLAUDE.md·SKILL.md·api-policy.sh·Actions·verifier.md·eval JSON·agent-evals.yml·check.sh·log_bodies.py·REVIEW.md·settings.json·release-gate.sh·managed settings·.mcp.json·bands.yaml·탐지 스크립트·사고 intent.md·캐시 eval)
- "GeekNews 도입 스레드의 첫 댓글" → "2025년 4월 ~ 유일한 한국어 댓글" — community.md 196행(GeekNews 20430, 2025-04-20, @ehdns1133 "유일한 한국어 댓글")
- "`/cost`가 현재 세션의 사용량을 보여 준다" → "`/usage`(`/cost`는 그 별칭)가 세션 토큰 사용량·추정 비용·플랜 사용량 바를 보여 준다; Pro·Max 구독자에게 달러 금액은 청구와 무관" — 근거: code.claude.com/docs/en/commands ("`/cost` | Alias for `/usage`"), docs/en/costs ("Claude Max and Pro subscribers have usage included in their subscription, so the session cost figure isn't relevant for billing purposes"), 2026-10-19 웹 확인(web.md에 `/cost` 항목 없음)
### ⚠️ 약화·삭제
- 스킬 "길어도 평소에는 비용이 들지 않고" → "본문이 길어도 호출되기 전까지는 ~ (목록에는 설명 한 줄만 늘 올라 있다)" — web.md 자료 3: description+when_to_use가 스킬 목록으로 항상 컨텍스트에 있음(1,536자 절단)
### 🕒 신선도
- "사용량 창으로 제한된다. 일정 시간 창" → "2026-10 공식 문서 기준으로 5시간 단위로 도는 창과 주간 창" — docs/en/costs ("rolling five-hour window and a weekly window", "session limit"/"weekly limit")
- `/usage` 문장에 "Claude Code 2.1.303 기준" 부가
### ✅ 확인 (요약)
- 인용 5건: 블로그판 "reimagined process ~ loop" / "thread running through ~ audit trail" / 트리거 문장 / 코스 레슨 6 거버넌스 문단(원문 글자 단위 일치, 스크립트 대조) / 레슨 11 훅 정의 "a script that runs before Claude acts that can allow, ask, or block"
- 공식 사양 8건: "context, not enforced configuration"(web 자료 5), "deterministic control"(자료 2), 결정값 allow/ask/deny + defer(자료 1), `--output-format json`→`total_cost_usd`(자료 6), `--max-budget-usd` print 모드 전용(자료 7), `Ctrl+G` 플랜 편집(자료 8), SKILL.md frontmatter/본문 구분(레슨 6), OTel 집계(자료 16)
- 버전·모델 6건: 코스 2026-08·`requiredMinimumVersion "2.1.193"`, Claude Code 2.1.303(2026-10-18), 코스기 Opus 4.8·Sonnet 5·Fable 5, 현행 Fable 5.1(09-01)/Opus 5.5(09-22)/Sonnet 5.5(09-28)/Haiku 5.5(10-07), 전부 1M 컨텍스트 — web 자료 18·26 일치. "구버전 주의" 박스 서술 적합
- 관통 예제 4건: portal TS·React / claims-api Python 3.12·FastAPI / claims-core 50 rps / intent 폴더, 60초 캐시·CACHE_SECONDS 60→0 사고 — 레퍼런스 2장 머리·3.1 일치
- 표 3건: 세 태그 매트릭스(레퍼런스 6.1), 의존 그래프(1.6, "실선·점선은 문장 해석" 고지 있음), 권장 진입 순서(1.6 합성 제안, "코스 원문 아님" 고지 있음)
- 커뮤니티 3건: 서브에이전트 사용량 소진 [개인 체험](community 97행), brunch "Pro 부족·Max 권장"(255행), 2025-04 HN 작업당 비용(255행) — 모두 "검증 필요"로 표기됨
- 부수 관찰(담당 외, 7장 검수자 참고): docs/en/costs에 "Agent teams use approximately 7x more tokens than standard sessions when teammates run in plan mode"가 공식 문구로 있음 — 레퍼런스 4.1 #4("7x 인용 금지 또는 출처 재확인")의 출처가 확인된 셈. 조건(plan mode 팀원) 병기 필요
### 미해소
- (없음)

## 03장 (라운드 1)

### ❌ 정정
- intent.md "열네 줄이다" → "열세 줄이다" — primary/02 코드블록 실측 13줄
- @jjw9512151 인용 "명세 깎는 데 공들이는 게 필요하다"(띄어쓰기 교정된 간접 인용을 직접 인용 부호 안에 둠) → 원문 "명세깎는데 공들이는게 필요하죠" — community.md 200행
### ⚠️ 약화·삭제
- "명세에 보안 요구를 넣지 않은 기준선" → "보안 요구를 따로 명시하지 않은 기준선" — 논문 20 초록은 기준선의 보안 요구가 '암묵적·일반적'이라 함(전무 아님)
- "/skill-name 확장" 문장에 "헤드리스 문서에 따르면" 출처 한정 — 해당 문구는 web 자료 6(headless)이며 GitHub Actions 문서(자료 11) 문구가 아님
### 🕒 신선도
- (없음 — "Claude Code 2.1.303 / 2026-10 기준" 선언, ClarifyGPT "숫자는 그 시점의 모델 것" 고지, 프리프린트 표기 모두 초안에 있음)
### ✅ 확인 (요약)
- 코스 예시 파일 3건 글자 단위 일치(diff): `intent.md`(완전 동일), 프롬프트(완전 동일), `spec.md`(들여쓰기 복원만 차이 — 허용)
- 코스 인용 5건: 레슨 2·3 What changes 표 원문, "The requirements are numbered so the plan and the review can cite them.", 거버넌스·측정 문단 요지, 5단계·6단계·3경로·5섹션 — primary/02·03 일치. "코스 레슨 N" 귀속 정확
- 수치 9건: Orchid 1,304과제·4유형(논문 18), ClarifyGPT 70.96→80.80% MBPP-sanitized GPT-4(논문 17 초록 — 초록 원문 수치라 '원문 미대조' 아님), SDD 벤치마크 221테스트·50/42/36(논문 20 초록), Pinna 82.1%/66.1%(논문 35 초록), HN SDD 스레드 2025-11-15·191댓글("수백 개"), canterburry 8시간, SKILL.md 500줄, 1,536자(미인용)
- 서지 5건: Yang 외 ASE 2026 심사 통과 / Mu 외 2023 arXiv 프리프린트(FSE 2024 게재는 DOI 미확인이라 보수적 표기 유지) / Wu 외 2025 프리프린트 / Grynets 외 2026 프리프린트 / Pinna 외 MSR 2026 심사 통과 — 레퍼런스 7.5 일치. arXiv ID(2604.21505·2606.00167 등)는 본문에 미노출, 빌드일 이전 YYMM
- 공식 사양 7건: 커맨드→스킬 통합·SKILL.md 권장·경로 2종(web 자료 3), 스킬 생성 시점 정의·"stays in context"·500줄(자료 3), Best practices 인터뷰 프롬프트·"fresh session"·"self-contained"(자료 14), 컨텍스트 엔지니어링 2025-09(자료 21), Actions automation mode(자료 11), `--bare` 건너뛰기(자료 6), 플랜 모드 "update plan.md in the same commit ~ hook"(primary/04 47행)
- 커뮤니티 6건: GeekNews 27700 @bus710·@tomskang 원문 일치, gieseanw 요지, HN constantcrying·cushychicken·Fargren·canterburry·laserlight(모두 같은 SDD 스레드 — community 214·263~265행), GeekNews 26148 @goodnvin·@cosine20 원문 일치
### 미해소
- (없음)

## 08장 (라운드 1)

### ❌ 정정
- "DevEx 프레임워크(Forsgren 외, ACM Queue 2023)" → "DevEx 프레임워크(Noda 외, ACM Queue 2023)" — 근거: papers.md 논문 47 저자 순서 Abi Noda, Margaret-Anne Storey, Nicole Forsgren, Michaela Greiler (DOI 10.1145/3595878). Forsgren은 3저자.
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — 현행 사양 절에 "Claude Code 2.1.303 / 2026-10 기준" 이미 명시, #319는 "Claude 3.7 시기" 명시)
### ✅ 확인 (요약)
- 4.1 #8 Goodhart 귀속: 인용문 → Strathern 1997 *European Review* 5(3) "영국 대학 감사 제도", Goodhart는 1975(강연)/1984(재수록) 원리 제안자 — 01_reference 4.1·papers 논문 48과 일치.
- GitHub #319(2025-03-04, Claude 3.7 시기, "safe-tests"·"cheating on the test", @rben01 innerHTML, @MatiasPujado "You are right!" ×4, 2026-01-30 봇 종료) · #7074(2025-09-03) · #46940 · DoltHub Sehn 인용·"이틀·$100"(개인 체험으로 명시) · Replit 2025-07 "falsely claimed unit tests had passed" — community.md P3와 일치.
- Manheim & Garrabrant arXiv:1803.04585(프리프린트 표기 있음) 4변종·Adversarial·인용문 / EvalPlus Liu 외 NeurIPS 2023 80x·pass@k 19.3–28.9%·"test insufficiency can lead to mis-ranking" / DORA 2026 "robust test automation" 인용 / HN ijk "evaluation metric ≠ optimization metric" — papers 논문 12·48, web 자료 30, community와 일치.
- 코스 레슨 8 원문 인용 전부(What changes 표, Prerequisites "None", 7단계, verifier 구분, governance "evidence comes from the toolchain"·"PR's check run", 측정 2지표) — primary/08과 일치. "Verifying your work" 블록 8줄 토큰 단위 일치.
- 현행 사양: Best practices 인용 3건·게이트 4단계·"trust-then-verify gap"(자료 14), `/goal [condition|clear]`·`/verify`(자료 13), Stop 훅 `decision: block`·`reason` 필수·8회 연속 상한·`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`(자료 1), 2.1.286 `verify` 스킬 커밋 전 실행(자료 18), memory 문서 "context, not enforced configuration"(자료 5), Hooks guide 보호 파일 패턴 PreToolUse·exit 2·피드백 문구(자료 2) — 전부 web.md와 일치.
- `protect-tests.sh`+settings.json: 본문에 "코스 예시가 아니라 코스 7단계와 공식 패턴을 관통 예제 경로에 맞춰 저자가 적은 것" 명시 확인. 설정 키(`hooks.PreToolUse[].matcher "Edit|Write"`, `type: command`, `command`, `args: []`)·`${CLAUDE_PROJECT_DIR}`·stdin `tool_input.file_path`·`exit 2` 차단·stderr 전달 — 공식 hooks reference(web 자료 1: `args` 필드 정의, `CLAUDE_PROJECT_DIR`)·코스 레슨 6·11 설정 형식과 일치. `settings.local.json`(gitignored·개인) — 자료 9와 일치. "훅은 Edit|Write에만 걸려 셸 덮어쓰기는 못 잡는다" 한계 서술 확인.
### 미해소
- (없음)

## 09장 (라운드 1)

### ❌ 정정
- `(사실 확인 필요)` 마커 해소(4.1 #6, `claude -p` exit code vs `is_error`/`permission_denials`): 두 진술을 "어느 쪽이 맞는지 확인 필요"로 둔 문단 → 공식 헤드리스 문서(code.claude.com/docs/en/headless, 2026-10-19 웹 확인)로 판정. 문서는 (a) "exits with code 0 on success and a non-zero code when the run fails … When a failure happens inside the run, such as missing authentication"이라 하고, (b) 권한 거부는 "the final result message lists them in `permission_denials`"로 별도 서술하며 실행 실패로 집계한다고 쓰지 않음. → "실행 실패"와 "권한 거부로 일을 못 함"은 다른 범주, 두 진술은 모순 아님으로 재서술. Wmedia 블로그는 "검증되지 않은 개인 관찰"로 약화해 유지. `permission_denials` 검사 권고는 "필드 자체는 공식 문서에 있다"로 근거 격상. final에 마커 0개.
- 같은 이유로 적용 절의 "커뮤니티 보고 기반이라 검증이 필요하지만" → "필드 자체는 공식 문서에 있고".
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- "2026년 한 해에만 … 모델 여덟 개를 냈다" → "(릴리스 노트 기준)" 부가 — web 자료 26 릴리스 노트 8건(Opus 4.7 04-16 · 4.8 05-28 · Fable 5 06-09 · Sonnet 5 06-30 · Fable 5.1 09-01 · Opus 5.5 09-22 · Sonnet 5.5 09-28 · Haiku 5.5 10-07)과 일치하나 "모델 개수"는 집계 기준에 따라 달라질 수 있어 기준 명시.
### ✅ 확인 (요약)
- 코스 예시 파일 4종 원문 일치(공백 정규화 후 토큰·순서 단위 대조, primary/09): `status-no-pii-in-logs.json`(`from: 9d04e7a`, `may_change` 2폴더, checks 5개 순서·이름 "no pii in logs" 포함), `agent-evals.yml` 35줄(들여쓰기 복원만, `Bash(make test)`·`fetch-depth: 0`·`cron '0 2 * * *'`·`/tmp/evals` 복사·worktree), `check.sh` 40줄, `log_bodies.py` 22줄, 정상/실패 출력 2블록.
- 코스 레슨 9 원문 인용 전부(정의·live suite·offline cadence·Prerequisites·Infrastructure·5단계·eval 출처 설명·루프 설명·`--bare` 굵은 경고·check.sh/log_bodies 설명·실패 시나리오·결말) — primary/09와 일치. 블로그판(2026-08-21) 초기 워크플로 묘사(`paths`에 `evals/**` 없음, 격리 없음, `./evals/check.sh`) — primary/99 610~652행과 일치.
- `--bare` 구버전 주의 박스: 코스(2026-08) 서술·2.1.286 변경 인용·"recommended … will become the default for `-p`" — web 자료 6·18, 레퍼런스 5장 표와 일치(헤드리스 문서 웹 재확인에서도 동일 문구).
- 현행 플래그·키 전부 레퍼런스에 존재: `--output-format json`+`total_cost_usd`, `--allowedTools` 접두 매칭 경고 원문, `--max-turns`·`--max-budget-usd`(print 전용), `claude setup-token`→`CLAUDE_CODE_OAUTH_TOKEN`(Pro/Max/Team/Enterprise), `--settings '{"disableAllHooks": true}'`·신뢰 경고 원문, `ANTHROPIC_API_KEY` — web 자료 6·7·11. 레퍼런스에 없는 플래그·설정 키 없음.
- Anthropic "Demystifying evals"(2026-01-09) 인용 4건·pass@k/pass^k 정의·"Deterministic graders are natural" — web 자료 22 일치.
- 학술: SWE-bench Jimenez 외 ICLR 2024 2,294·12리포 / Terminal-Bench Merrill 외 ICLR 2026 3요소 / SWE-Bench+ Aleithan 외 arXiv:2410.06992(프리프린트 표기) 32.67%·31.08%·94%+·12.47→3.97% / SWE-bench Verified 2024-08 500개 / Kapoor 외 TMLR holdout 인용 / Zheng 외 NeurIPS 2023 3편향 / Wang 외 ACL 2024 66/80 — papers 논문 7·8·9·11·13·14·15 초록 원문과 일치. 표의 3결함↔3장치 대응은 레퍼런스 2.8 합성과 일치.
- 커뮤니티: HN Arainach(49376287)·Mdarena — community 295·298행 일치.
- 레퍼런스 8장 한계 준수: 개인 eval 예시(`fix-keeps-tests`)에 "코스 포맷을 저자가 개인 리포 규모로 축소한 구성 예시 — 실제 리포 아님" 명시 확인; "5~10개"에 "이 책의 합성 제안" 명시 확인.
### 미해소
- (없음)

## 10장 (라운드 1)

### ❌ 정정
- "열네 줄, 네 절이다" / "위의 열네 줄을 `CLAUDE.md`로" → "열세 줄" ×2 — REVIEW.md 코스 원문은 13줄(primary/10 대조, 토큰 단위 일치).
- Greptile 인용 귀속: dakshgupta "LLM은 문제의 심각도를 낮게 보는 위험을 꺼린다"는 2024-12 스레드가 아니라 2026-01-26 "AI 코드 리뷰 버블" 스레드의 발언(community.md P6). 2024-12 스레드의 dakshgupta 발언은 "치명적 문제를 nitpick으로 분류하는 일도 잦았다". 두 인용을 각자의 스레드로 재배치.
- 구버전 주의 박스 "코스 집필기의 명령 체계에서는 `/review`가 별도 명령이었다" → "코스 예시가 요구하는 최소 버전(2.1.193)에서는 `/review`가 별도 명령이었다" — 별칭 전환은 v2.1.223(web 자료 13); 코스의 `requiredMinimumVersion: "2.1.193"` < 2.1.223이므로 버전 기준으로 정확히 서술(레퍼런스 5장 주석: `/review`는 코스 레슨 본문에 직접 등장하지 않음).
- `(사실 확인 필요)` 마커 해소(4.1 #12 curl 바운티): 웹 확인(The Register 2026-01-21, The New Stack, heise, BleepingComputer, LWN — Daniel Stenberg의 2026-01-21 GitHub 커밋·Mastodon 공지 보도) → "curl 프로젝트는 2026년 1월, AI 생성 보고의 폭증을 이유로 버그 바운티 종료를 공지했다 — 부실한 보고를 보낼 유인을 없애려는 조치였다. 보고 건수는 보도마다 달라 숫자는 적지 않는다." 수치 없이 사실만. final에 마커 0개.
### ⚠️ 약화·삭제
- Cihan 외 PR 종료 시간 증가의 원인 서술 "리뷰어가 읽을 것이 많아졌고 … 오갔기 때문이다"(단정) → "…시간이 붙었다고 보는 것이 자연스럽다"(해석) — 초록에 원인 분석 수치 없음(papers 논문 30).
- 관리형 Code Review "가장 손이 안 가고 **가장 비싸며**" → "가장 손이 안 가고" — 경로 간 비용 비교 근거는 커뮤니티 수치($0.90, 검증 필요)뿐이라 최상급 삭제.
- Fu 외 "GitHub의 Copilot 생성 스니펫 733개" → "GitHub 프로젝트에 올라간 Copilot 등 AI 어시스턴트 생성 스니펫 733개" — 논문 27은 Copilot·CodeWhisperer·Codeium 스니펫 포함.
### 🕒 신선도
- (없음 — 네 가지 길 표와 현행 사양 절에 "Claude Code 2.1.303 / 2026-10 기준" 명시, 구버전 주의 박스에 코스 2026-08 명시, 플랜 조건 "바뀔 수 있다" 고지 있음)
### ✅ 확인 (요약)
- Cihan 외 ICSE-SEIP 2025(arXiv:2412.18531, 심사 통과): 4,335 PR·1,568 자동 리뷰·73.8% 해결·5h52m→8h20m — papers 논문 30 초록 원문 일치.
- 4.1 #9 관리형 Code Review 라벨: 현행 "research preview" 없음·Team/Enterprise, `/code-review` 모든 플랜, 서비스 vs `/code-review` 별개 도구·읽는 파일 인용 원문, REVIEW.md 베이스 브랜치 규칙, Find/Verify/Rank/Post, 심각도 3종 정의, neutral·"never concludes as a failure", `bughunter-severity` JSON `{"nit":1,"normal":2,"pre_existing":0}`·`normal`=Important, `@claude review`/`always`·write 권한 — web 자료 12 일치. check run 표(Important 2·Nit 1)와 집계 예시값 일치.
- 공식 비용 문구 "리뷰는 평균 약 20분, 대개 $15–25"·"PR을 승인하지 않는다" — r/ClaudeAI u/ClaudeOfficial 2026-03-09(community P6) 원문 범위 내. 커뮤니티 비용(Cloudflare $5k·10줄 PR)은 수치 없이 서술, "커뮤니티 비용 수치는 전부 검증이 필요" 고지 확인.
- claude-code-action v1: `/install-github-app`(github.com 전용·admin), 시크릿 2종·플랜 4종·`claude setup-token`, prompt 유무 모드, `code-review@claude-code-plugins`·`/code-review:code-review --comment`·`--comment` 없으면 미게시, write·human actor·`allowed_bots`, 드래프트/닫힌/기존 코멘트 건너뛰기, 포크 PR 시크릿, `--max-turns`·타임아웃·동시성 — web 자료 11 일치.
- 로컬 명령: `/code-review`·`--fix`·`/code-review high 1234`·`/review` 별칭(v2.1.223)·`/code-review ultra`·`/security-review`·2.1.288 `--max-findings <n>|all`·헤드리스 `gh pr diff … --append-system-prompt` 예 — web 자료 13·18·6 일치. Anthropic 보안 SDLC(2026-07-21) "hard code review gate in CI" — 자료 24 일치.
- 코스 레슨 10 원문 인용(What changes 표·"gives and receives"·6단계·check run 표·"first finding exists only because…"·governance·측정) — primary/10 일치. REVIEW.md 13줄 토큰 단위 일치. `plan.md` 위험 항목 "50 rps; the panel must cache (spec concern 3)" — 레퍼런스 3.1 일치.
- 커뮤니티: GeekNews 27700 @cafedead 원문, r/ExperiencedDevs lonestar-rasbryjamco(205p 최다)·LeadingPokemon·ashwinmur386 티어드, Ghostty AI_POLICY.md 2문장, HN jerrygoyal·zmmmmm·greymalik·plmpsu·OtherShrezzing, GeekNews 20800(2025-05) @bungker, madewithlove `synchronize`(개인 블로그 표기), @tomskang, sailfast — community.md P5·P6·논쟁 B 일치.
- 학술: Bacchelli & Bird ICSE 2013(수치 없이 결론 방향만 — 레퍼런스 "초록 미확보" 지침 준수) / Xia & Miller arXiv:2607.09902(2026-07, 빌드일 이전, 프리프린트 표기) 182리포·10%p→~6% / Fu 외 TOSEM 2025 733·55.5% / Perry 외 CCS 2023 인용 — papers 논문 43·36·27·28 일치.
### 미해소
- (없음)


## 04장 (라운드 1)

### ❌ 정정
- 권한 모드 표 `auto` 행(저술가 구성) "분류기가 통과시킨 행동 — 명시적 `ask` 규칙은 여전히 질문 / 승인된 계획의 구현" → 공식 표 행으로 교체: "전부 — 단, 백그라운드에서 분류기의 안전 검사를 거친다. 명시적 `ask` 규칙은 여전히 질문 / 긴 작업, 승인된 계획의 구현(현행 대화형 기본)" — 근거: code.claude.com/docs/en/permission-modes 모드 표 `auto` 행 "Everything, with background safety checks | Long tasks, reducing prompt fatigue" + auto 절 "Explicit ask rules still force a prompt" (2026-10-19 웹 확인; 레퍼런스 2.3 표에는 auto 행 없음)
- 구버전 박스 "`-p` 시작 모드는 2.1.285에서 2.1.302 사이에 몇 차례 오갔다" → "한 번 바뀌고 되돌아갔다 — 2.1.285(09-29) 서드파티·텔레메트리 off의 `-p`를 auto로, 2.1.302(10-16) 그 환경과 신규 설치를 다시 `default`로" — 근거: 체인지로그 2.1.285·2.1.302 원문(web 자료 18 + 웹 재확인). 2.1.286~2.1.301 사이에 `-p` 시작 모드 변경 항목 없음(체인지로그 2.1.285~2.1.303 전수 확인). 부수 관찰: permission-modes 문서 본문의 `-p` 행은 2.1.303 시점에도 "auto with v2.1.285 or later"로 남아 있어 체인지로그와 어긋남 — 책은 날짜가 명시된 체인지로그를 따르고 박스에 그 사실을 병기
- 인용 "AI-enhanced productivity is not a shortcut to competence." → 원문은 "...competence and AI assistance should be..."로 이어지는 문장이라 마침표 제거(단편 인용 표시) — papers 논문 42 초록
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — "Claude Code 2.1.303 / 2026-10 기준" 선언, 코스 2026-08 병기, 2.1.283·2.1.299 버전 병기 모두 초안에 있음)
### ✅ 확인 (요약)
- 코스 레슨 4 원문 인용 전부(What changes 양쪽 칸·7단계·"R1 to R4 ~ line by line"·거버넌스 "Plan mode enforces this itself ~"·auto mode 부속 절·레거시 3구성) — primary/04와 글자 단위 일치(스크립트 대조 36건 중 35건 일치, 1건은 위 마침표만). `plan.md` 19줄 토큰 단위 일치
- 공식 사양 11건: 플랜 모드 정의·bypass 예외·`Shift+Tab`/`/plan`/`--permission-mode plan`·`defaultMode: plan`·`Ctrl+G`·"Yes, and use auto mode"/"No, keep planning"·v2.1.283 auto 기본·분류기 정의·3회 연속/20회 누적 폴백·"Boundaries are not stored as rules ~ deny rule"·`--permission-mode` 7값(`manual` 별칭)·`plan` 행 "classifier-approved commands when auto mode is available"·`auto`/`bypassPermissions`는 프로젝트 설정 불가 — web 자료 7·8 + permission-modes 웹 재확인 일치. 2.1.299 플랜 모드 쓰기 수정 — 체인지로그 원문 일치
- Best practices 3건("adds overhead ~ one sentence, skip the plan", "jump straight to coding ~ wrong problem") — web 자료 14. H8 블로그 합의는 "데이터는 아니다" 고지 확인. "You're paying one extra turn ~" 블로그 인용 — community P12
- 학술 4건: Wang 외 Plan-and-Solve ACL 2023(3실패·10데이터셋), Erdogan 외 Plan-and-Act ICML 2025(웹 탐색 도메인 명시 확인), Watanabe 외 TOSEM 157/567/83.8%/54.9%·수정 사유 3종, Shen & Tamkin 프리프린트 표기·6패턴 중 3 — papers 21·22·33·42 일치
- 커뮤니티 3건: #44246(2026-04) "plan mode before non-trivial tasks" — gh api로 이슈 본문 원문 확인(2026-04-06 개설); HN adzicg "A human will read the plan and then iterate on it"; 인프런 Shift+Tab — community P12 일치
- 레퍼런스에 없는 플래그·설정 키 없음
### 미해소
- (없음)

## 05장 (라운드 1)

### ❌ 정정
- "한 위키독스 저자가 자기 CLAUDE.md로 측정해 보니 한국어가 영어의 1.45배 토큰이었고, CJK 전반으로는 1.01배로 거의 차이가 없었다" → 수치의 비교 대상이 다름. 원문(wikidocs.net/blog/@jaehong/11884, "Claude 4.7 토크나이저, 공식 문서보다 비싼 이유", 2026-04-18)은 **Opus 4.7 새 토크나이저 vs 구 토크나이저** 비율: 영어·코드 위주 실제 CLAUDE.md 1.45배(공식 가이드 1.0~1.35배 초과), CJK 텍스트 1.01배(거의 변화 없음). 한국어 대 영어 비교가 아님 → "토크나이저 변경이 한국어에 불리하게 작용하지 않았다는 뜻이지, 한국어가 영어보다 싸다는 뜻은 아니다"로 재서술하고, "한국어·영어 직접 비교 자료는 리서치에서 찾지 못했다"(community P11 "직접 비교 후기는 못 찾음")를 명시. 레퍼런스 4.1 #5의 "CJK 1.01배 [개인 측정]" 요약 자체가 비교 대상을 생략한 것이었음 — 직접 접근은 403, WebSearch 결과의 원문 발췌로 확인
- 같은 문단 "Sonnet 5의 새 토크나이저는 ~ 약 30% 더 많은 토큰 — 언어와 무관하게" → "언어를 따로 구분하지 않은 수치다" — 릴리스 노트 원문은 "approximately 30% more tokens for the same text"(web 자료 26)이며 언어 독립성을 명시하지 않음. 결론 "길이가 언어보다 큰 변수다" → "공식적으로 확인되는 변수는 언어가 아니라 길이다"(핵심 bullet도 동일 방향으로 수정)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- "같은 제목의 이슈가 GitHub에 최소 열 건 넘게" → "(2026-10 기준)" 부가 — community P1 집계 12건(#2737~#85754), 수집 시점 기준 집계라 시점 명기
### ✅ 확인 (요약)
- GitHub 이슈 2건 gh api 원문 확인: #17530 "Claude Not Reading Claude.md" @vanderoffice 2026-01-11 개설, 2026-03-06 closed not_planned; 본문 "approximately 50% of sessions"·"~400 lines"·"$200/month subscription with ~50% reliability"·"9 times over 60 minutes"·"under 150 lines" 일치; 댓글 @ivanvurbanov 2026-02-06(한 줄 NON-NEGOTIABLE) 일치. #44246 @nath-maker 2026-04-06 개설(2026-05-31 종료); 본문 무시 지시 4종·"This is not occasional drift. It is a consistent, noticeable regression" 일치; 댓글 @Gunther-Schulz 2026-04-14("exactly once") 일치 — 본문은 "커뮤니티 주장, 검증되지 않았다"로 표기 유지(4.1 #3 준수: "세션 시작 시 로드된다"까지만). #34763(2026-03-15) 인용 원문 — community P1 일치
- 코스 레슨 5 원문 인용 전부(정의·5단계·거버넌스·측정) — primary/05 일치. `CLAUDE.md` 예시 18줄 토큰 단위 일치(들여쓰기 복원만) → "스무 줄 미만" 실측 확인
- 공식 메모리 문서 12건: "context, not enforced configuration ~ PreToolUse hook", 4계층 경로(macOS/Linux·WSL/Windows·User·Project 2경로·Local gitignore), "loaded at launch"/하위 디렉터리 on demand, "concatenated ~ rather than overriding", "may pick one arbitrarily", "target under 200 lines", `@import` 4홉·컨텍스트 비용 미감소·백틱 회피, `.claude/rules/` `paths:`, `/init` 비덮어쓰기, auto memory 200줄/25KB·`/memory`·"Who writes it", AGENTS.md v2.1.277+, Managed CLAUDE.md 분업 표 — web 자료 5·13 일치. Best practices 포함/제외 표 14항·한 줄 테스트·IMPORTANT 한 줄 — web 자료 14 일치. 스킬 문서 "grown into a procedure rather than a fact" — 자료 3 일치
- 커뮤니티: HumanLayer "< 300 lines"·"less than sixty lines", HN jswny "100% of your sessions", Reddit u/SetentaeBolg "insistent language"(검증 필요 표기 확인), HN bisonbear 긍정형, HN 49376287 "morally opposed"(2026-08-20) 양측 논지, HN 48160604 luodaint 3분류(2026-05-16), Netflix·Apple HN(2026-05·07), klaude 프로젝트 문구(측정 아님 표기 확인), 토스 테크 2문장 — community P1·P2·H1·F·P11, web 자료 36 일치
- 학술: Santos 외 AGENT 2026(ICSE 워크숍) 328개·아키텍처 경향, Galster 외 AIware 2026 2,853개·"few repositories adopt ~ Skills and Subagents" — papers 24·25 일치
### 미해소
- (없음)

## 06장 (라운드 1)

### ❌ 정정
- (없음)
### ⚠️ 약화·삭제
- "Grynets 외 ~ 스펙에 적지 않은 보안 요구는 생성 코드에 나타나지 않았다" → "보안 요구를 따로 명시하지 않은 기준선에서 보안 실패가 가장 많았고, 명세에 보안 층을 더할수록 줄었다" — 논문 20 초록은 기준선의 보안 요구가 '암묵적·일반적'이고 modal failure가 50→42→36으로 감소했다고 함(전무 아님). 03장 검수 판정과 정합
- 구버전 박스 "커맨드가 스킬에 통합되었고" → "(공식 문서는 통합된 버전을 따로 적지 않는다)" 병기 — 스킬 문서 안내문("Custom commands have been merged into skills")에 버전 없음, 체인지로그 2.1.285~2.1.303 범위·웹 검색에서도 통합 버전 미확인 → 버전 병기 요청은 불가, 미기재 사실을 명시
- 인용 "Unlike CLAUDE.md content, a skill's body loads only when it's used." → 원문이 ", so long reference material ~"로 이어져 마침표 제거(단편 인용)
### 🕒 신선도
- (없음 — 두 "현행 사양" 절에 "Claude Code 2.1.303 / 2026-10 기준" 명시, 박스에 코스 2026-08 명시, 2.1.295 버전 병기 있음)
### ✅ 확인 (요약)
- 코스 예시 파일 5종 토큰 단위 일치(primary/06): `SKILL.md` 17줄, `settings.json` 14줄, `api-policy.sh` 13줄, 메시지 출력 2줄(`claims-api/routes/status.py:10: policy_holder_name`), Actions YAML 8줄(들여쓰기 복원만). `scripts/check-endpoints.sh`·`.claude/hooks/api-policy.sh` 경로 일치
- 코스 레슨 6 원문 인용 전부(정의·6단계·거버넌스 "advisory ~ close to impossible"·측정 2지표·훅 부속 절 4용도·"fast and scoped"·"cannot undo it, so exit code 2"·"does not fire when a shell command rewrites"·"The hook catches ~ another way"·"belongs with the gates in Stage 5") — 글자 단위 일치(43건 중 42건, 1건 마침표). "organization-level slash command" — primary/03 41행에 실재
- 공식 스킬 사양 9건: 위치 5곳·"Where you save a skill decides"·충돌 우선순위·frontmatter 필드명 9개(모두 공식 표에 존재)·"All fields are optional. Only `description` is recommended"·하이픈 정확 일치·조용한 무시·1,536자·`disable-model-invocation`/`user-invocable` 의미·500줄·"stays in context across turns"·"Create a skill when ~" — web 자료 3 + 스킬 문서 웹 재확인 일치
- 공식 훅 사양 12건: exit 2 정의·PostToolUse 비차단(stderr만)·`decision: "block"`+`reason`·`updatedToolOutput`·matcher 문법(`"*"`/`""`/영숫자 목록/비앵커 JS 정규식)·`args` 직접 스폰·`CLAUDE_PROJECT_DIR`·600초/30초·`async` 비차단·이벤트 30종+·타입 5종·2.1.295 `onFailure: "block"`(체인지로그 웹 재확인)·"full user permissions"·모범 사례 4항·prettier/보호 파일 예시·"Claude can write hooks for you"·"hooks are deterministic" — web 자료 1·2·14·18 일치. 본문 이벤트명 6개(`SessionStart`·`PreToolUse`·`PostToolUse`·`Stop`·`ConfigChange`·`WorktreeCreate`) 모두 레퍼런스에 존재
- 커뮤니티·한국: 익명 블로그 테스트 문장(P9), ITWorld 스킬 악성 코드 경고, HN brianwawok, HumanLayer "Never send an LLM to do a linter's job", 토스 테크 3문장(2026-02-26), GPTers "한 번 정해두니" — community P9·H2, web 자료 36·40 일치
- 학술: Galster 외 "대부분 정적 지시", Vijayvergiya 외 AutoCommenter AIware '24 Google 규모 — papers 25·31 일치
### 미해소
- (없음)

## 07장 (라운드 1)

### ❌ 정정
- 4.1 #4 "7x" 해소: "블로그에는 구체적인 배수가 떠돌지만 공식 페이지에서 확인되지 않으므로 이 책은 인용하지 않는다" → 공식 비용 문서(https://code.claude.com/docs/en/costs, "Manage agent team costs" 절, 2026-10-19 웹 확인)에 "Agent teams use approximately 7x more tokens than standard sessions when teammates run in plan mode, because each teammate maintains its own context window and runs as a separate Claude instance"가 있음 → 조건(에이전트 팀·팀원이 플랜 모드일 때) 병기한 조건부 인용으로 정정. 서브에이전트 배수는 여전히 공식 문서에 없음을 명시. 네 선택지 표의 에이전트 팀 비용 칸에도 "(팀원이 플랜 모드일 때 약 7배, 공식)" 부가. 1~3장 검수자 전달 사항과 일치
- "의도치 않은 팀 생성을 막으려면 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=0`을 둔다" → "에이전트 팀은 실험 기능이고 기본으로 꺼져 있다(`=1`로 켠다). 켠 뒤 요청하지 않은 팀이 만들어지면 같은 변수를 `0`으로 되돌린다" — agent-teams 문서 경고문 "Agent teams are experimental and disabled by default. Enable them by setting CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1" + 트러블슈팅 "=0" 절(웹 확인). 초안은 기본 켜짐처럼 읽힐 여지가 있었음
- "내장 서브에이전트는 셋이다" → "Explore·Plan·General-purpose 셋이 중심이다(그 밖에 보조용 몇 개가 더 있다)" — sub-agents 문서는 세 주요 내장 외에 `claude`·`statusline-setup`·`claude-code-guide`를 추가로 열거(웹 확인)
- `/cost` ×2 → `/usage`(`/cost`는 별칭) — commands 문서 "`/cost` | Alias for `/usage`"(웹 확인; 02장 판정과 정합)
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — 두 "현행 사양" 절에 "Claude Code 2.1.303 / 2026-10 기준" 명시)
### ✅ 확인 (요약)
- 코스 레슨 7 원문 인용 전부(도입 "One engineer can drive ~", 병렬 세션·서브에이전트 정의, "knows nothing about the others ~ only thing they share", What changes 양쪽 칸, 4단계, 거버넌스, 인프라 "permission settings tuned ~", 측정 2지표) — primary/07 일치(34건 중 33건 글자 단위, 1건은 문장 중간 절단 마침표 — 허용). `verifier.md` 8줄 토큰 단위 일치(frontmatter 빈 줄 정리 고지 있음)
- 워크트리 공식 사양 12건: `--worktree`/`-w`·`<repo>/.claude/worktrees/<name>`·이름 자동 생성·`#<number>`/PR URL·브랜치 `worktree-<name>`·베이스 `"fresh"`/`"head"`·`.gitignore`·`.worktreeinclude`·정리 3규칙(`-p` 미정리 포함)·격리 검사(Edit/Write/NotebookEdit·git 리다이렉트)·`${CLAUDE_PROJECT_DIR}` stays put/`cwd` follows·"don't ask again"→메인 `settings.local.json` — web 자료 7·10 일치
- 서브에이전트 공식 사양: 발견 순서 5단계, `name`·`description`만 필수, `tools` 생략 시 전체 상속, `model` 값(`sonnet`·`opus`·`haiku`·`fable`·전체 ID·`inherit`), `permissionMode`, `maxTurns`(부분 완료 표시), `skills`(전문 주입), `memory`, `isolation: worktree`(변경 없으면 자동 정리), "fresh, isolated context window ~", "only this system prompt plus basic environment details", 호출 3방식 — sub-agents 문서 웹 재확인 일치. `/batch` "5 to 30 independent units ~ isolated worktree" — commands 문서 웹 확인 일치
- 에이전트 팀 공식 문구: "significantly more tokens ~ scales with the number of active teammates", "Token costs scale linearly", "Before you set up a team, check whether a lighter option does the job", `-p`에서 팀원 미생성, "For research, review, and new feature work ~ routine tasks, a single session" — agent-teams 문서 웹 재확인 일치
- Best practices: Writer/Reviewer "fresh context ~ biased", 적대적 리뷰 경고 원문, `-p` 팬아웃 `--permission-mode dontAsk` — web 자료 14 일치. `--output-format json`·`total_cost_usd` — 자료 6. `CLAUDE_CODE_ENABLE_TELEMETRY=1`·기본 off·리포 `.claude/settings.json`으로 불가 — 자료 16 "a repository can't use them to turn telemetry on" 일치. `permissions.allow` — 자료 9
- 커뮤니티: HN 48883275 mcv·wongarsu 인용, Dev.to 15분/30분 [개인 체험] 표기, H4 3항("5개 미만 인라인"·명시 요청 시만·작은 모델), GPTers PM 1+6 "역할이 섞이고" — community P4·H4, web 자료 40 일치
- 학술: Kapoor 외 TMLR(비용도 메트릭), Mozannar 외 CHI 2024(비율 수치 미인용 고지 있음), METR — papers 15·5·2 일치
- 그림 1(mermaid) 경로·브랜치명(`.claude/worktrees/feature-auth`·`worktree-feature-auth`)은 공식 규칙과 정합. 표 "서브에이전트 CI(`-p`) 가능"은 공식 문서에 반대 서술 없음(팀만 `-p` 제외)
### 미해소
- (없음)

## 11장 (라운드 1)

### ❌ 정정
- 출처 표기 2건: "레퍼런스의 합성 추정이고" → "이 책의 추정이고" / "커뮤니티의 반복되는 호소를 레퍼런스는 한 줄로 요약한다" → "…호소는 한 줄로 요약된다" — 독자에게 보이지 않는 내부 리서치 산출물(`01_reference.md`)을 출처처럼 인용한 표현 제거. 사실 내용은 그대로(블로그판→코스판 변화 추정은 01_reference 2.10 합성 추정; P7 요약은 community.md P7 제목)
### ⚠️ 약화·삭제
- Replit 사고 후속 조치 "Replit은 이후 … 도입했다" → "보도에 따르면 Replit은 … 도입했다(사고의 세부는 보도 종합이고…)" — 4.1 #11: 1차(Lemkin 원 게시물·Replit 공식) 재확인 전이라 골격만 쓰되 보도 귀속 명시. 수치(1,206/1,196+/4,000여)는 초안에 이미 없음 확인
- "인프런 Q&A에서 반복되는 권고" → "인프런 Q&A에서 확인한 권고" — community.md P11에 해당 권고 출처는 Q&A 1건(questions/1793945)
### 🕒 신선도
- "2.1.233 이상에서 `ask`는 작동한다" → "2.1.233 이상에서는 `bypassPermissions` 모드에서도 훅의 `ask`가 작동한다" — 4.1 #2 판정의 조건(bypass 모드)을 명시. 근거: community.md P7 bcherny 2026-08-16/17 응답
- "#80039 … 아직 열려 있고" → "이 책의 조사 시점(2026-10)에도 열려 있고" — 이슈 상태는 휘발성
### ✅ 확인 (요약)
- 코스 예시 코드 4블록 토큰 단위 일치(스크립트 대조, primary/11): settings.json 14줄, `release-gate.sh` 32줄(비공백), 출력 JSON 2개(4f2c9e1·CHG-·`^[0-9a-f]{7,40}$`·change.example.com), 관리형 설정 JSON 34줄(`requiredMinimumVersion: "2.1.193"` 포함) — 들여쓰기 복원 외 무변경
- 4.1 #1 `exit 2`: 본문이 공식 hooks 문서(2026-10-19 웹 재확인 — "PreToolUse | Yes | Blocks the tool call", "PostToolUse | No | Shows stderr to Claude")를 우선하고 #13756(resolved)·#80039(Windows, 2.1.217)·#55334(2026-05)를 플랫폼·버전 한정 결함으로 서술, "직접 깨뜨려 보라" 권고 — 지시대로. 8장 한계("Windows 네이티브 훅·샌드박스 동작 검증된 가이드 없음")에 걸리는 단정 없음
- 4.1 #2 `ask`·bypass: #77212(2026-07-13, CC 2.1.199, VS Code 확장) / bcherny "On 2.1.233 … honored" — community.md P7 원문 일치. H6 "강제는 deny, ask는 편의" 서술 일치
- 현행 사양(web 자료 1·2·8·9·15·16, v2.1.303): `permissionDecision` 4값 정의·우선순위 `deny` > `defer` > `ask` > `allow`·reason 독자(ask→사용자/deny→Claude/allow·defer→디버그 로그)·"Deny and ask rules are still evaluated", 종료 코드 0/1/2 문구, `updatedInput` 2.1.300 검증, 매처 문법(영숫자·`_`·`-`·공백·`,`·`|` / MCP `.*` 필수), `args` 필드 셸 미경유, 설정 위치 7행(플러그인 "When plugin is enabled" — 웹 재확인)·우선순위 5층·"Nothing in your own settings files or `--settings` overrides a managed key"·`permissions.allow` 병합·규칙 문법·스키마 URL·`/status`·`/permissions`(자료 13), "Deny rules block in every mode, including `bypassPermissions`", 샌드박스(셸 명령만·macOS/Linux/WSL2·Windows unsandboxed·도메인 목록 빈 상태·기본 off·`/sandbox`·`failIfUnavailable`·개인용 `--settings` 한 줄), OTel `tool_decision(source="hook")`·기본 off·리포 설정 불가, `disableBypassPermissionsMode` 등 managed-only 키 개인 무효 — 전부 일치. 레퍼런스에 없는 플래그·설정 키·훅 이벤트명 없음
- 구버전 주의 박스: 코스(2026-08) 3값/"스크립트"/2.1.193 ↔ 현행 `defer`·훅 5종(command/http/mcp_tool/prompt/agent)·2.1.303 — 5장 표 일치
- 코스 레슨 11 인용 전부(훅 정의·Deploy 배치 이유·4단계·`args` 설명·`change-ticket`·"no way to write to the records it reads"·비대화형 `ask` 거부·`GITHUB_REF` 한계·reason 독자·거버넌스·관리형 키 설명 8항·측정 2지표) — primary/11 일치. 블로그판 `production-gate.sh` "열 줄짜리"(primary/99 757행 실측 10줄)·`Bash` 매처·`RELEASE_APPROVAL`·`exit 2`·2026-08-21 일치
- 학술: Parasuraman & Manzey 2010 *Human Factors*(논문 40, 초록 원문 2문장) / Parasuraman & Riley 1997 disuse(논문 39, 분류 틀만) / Bainbridge 1983 *Automatica* "Ironies of Automation" p.775 인용(논문 38) / Lee 외 CHI 2025 319명·936건·자기 보고(논문 41) — papers.md 일치
- 한국 보안 문단: 정책 배경(2026-04 시행세칙 개정·2026-05 망분리 한시 완화)+"1차 후기는 확보하지 못했다" 고지+인프런 권고 — 8장 한계 지침("현장 목소리로 쓰지 말 것") 준수. 토스 정세훈 인용 원문 일치(web 자료 37). "root UID 0 거부"는 이 장에 없음(12장에서 "현장 보고로는" 표기)
- 분량·문체·`<!-- -->` 주석 무변경
### 미해소
- (없음)

## 12장 (라운드 1)

### ❌ 정정
- 4.1 #6 `claude -p` exit code: 오프닝 "공식 문서는 실행이 실패하면 0이 아닌 종료 코드를 돌려준다고 적으니, 사실 여부는 검증이 필요하다" + 적용 절 "레퍼런스는 이 마지막 권고를 '확인 필요'로 표시하면서도…" → 9장 final과 같은 판정으로 통일: 공식 헤드리스 문서(2026-10)는 '실행 실패'(인증 누락 등)의 비0 종료와 권한 거부의 `permission_denials` 목록 기재를 별도 서술 — 두 진술은 모순 아님. Wmedia는 "검증되지 않은 개인 관찰" 유지, `permission_denials` 검사 권고는 "필드 자체는 공식 문서에 있다"로 근거 격상. 내부 산출물 '레퍼런스' 인용 표현 제거. 근거: web.md 자료 6, factcheck_log `## 09장` 판정, 09_final.md 244행
- "Bainbridge의 1983년 논문이 70년 가까이 된 답" → "40년 넘은 답" — 1983→2026 = 43년(01_reference 2.11의 "70년 전 근거"도 같은 오류, 레퍼런스 표기 오류를 본문에서 바로잡음)
- "`-p`의 기본 권한 모드는 최근 두 달 사이에 왕복했다" → "2026년 9월 말과 10월 중순 사이에" — 2.1.285(2026-09-29) → 2.1.302(2026-10-16), 약 2.5주(web 자료 18)
### ⚠️ 약화·삭제
- "auto 모드의 분류기가 연속으로 거부를 내면 세션이 중단된다" ×2(본문·핵심) → "중단될 수 있다 / 중단으로 이어질 수 있고" — 근거가 Wmedia 블로그 메시지 하나(community P8 [검증 필요]); 공식 문서(web 자료 8)는 대화형 폴백(3회 연속/20회 누적 시 프롬프트 재개)만 기술
- Agent SDK 인증 "Anthropic은 서드파티 개발자가 … 허용하지 않는다" → "사전 승인 없이는 … 허용하지 않는다" — 원문 "Unless previously approved"(web 자료 17)
### 🕒 신선도
- (없음 — "Claude Code 2.1.303 / 2026-10 기준" 선언, `--permission-prompts none` 2.1.259+, `--restricted` 2.1.248+, `--bare` 2.1.286, "빠르게 바뀌고 있다" 고지, DORA "2026-10-19 확인", Wmedia "2026년 7월" 모두 초안에 있음)
### ✅ 확인 (요약)
- 코스 예시 3블록 토큰 단위 일치(primary/12): 트리아지 YAML 6줄(`if: failure()`·`out/build.log`·`triage.md`), `.mcp.json` 19줄(`type: http`·3 URL·`${DEPLOY_*_TOKEN}`), 스테이징 YAML 11줄(`${{ github.sha }}`·"over 1%"·`--allowedTools` 3툴·`--permission-mode dontAsk`·`release-notes.md`) — 들여쓰기 복원 외 무변경. 도구 표(release/status/rollback, "five minutes", 5xx)·3티어 표(Dev/Staging/Production 4열) 원문 일치
- `prod-gate.sh`: 본문에 "저자 구성 예시" 명시 확인. 훅 이벤트명 `PreToolUse`, JSON 키 `hookSpecificOutput`·`hookEventName`·`permissionDecision`·`permissionDecisionReason`, stdin `tool_input.command`, `exit 0`+JSON — 공식 hooks reference(web 자료 1·2)와 일치. 문자열 매칭 우회 가능성 정직 고지 확인
- 코스 레슨 12 인용 전부(What changes 표·Prerequisites·Infrastructure·6단계·"names the server and the tool, not the tool's arguments"·`dontAsk` 설명·fail-closed 문단·`allowManagedHooksOnly`·거버넌스 3통제·"agent's own identity"·측정 2지표) — primary/12 일치. 환경별 3티어는 코스 귀속 ✓
- 현행 플래그·키(web 자료 6·7·8·11·17·18): `dontAsk` 정의 원문, `--permission-prompts none`, 2.1.285/2.1.302 왕복 원문, `--allowedTools`("Tools that execute without prompting") vs `--tools` vs `--disallowedTools`(`"Edit"`/`"*"`/`"mcp__*"`), `--max-turns`·`--max-budget-usd`(print 전용)·`--json-schema`·`--append-system-prompt`·교체 플래그 지침 원문·`--restricted` 원문, `--bare`("recommended … will become the default", 2.1.286 MCP 명시), Agent SDK Python/TypeScript·서브프로세스 `-p --output-format json`, GitHub Actions `use_bedrock`/`use_vertex`/`use_foundry` OIDC, agent-teams "-p … doesn't spawn teammates" — 전부 일치. 레퍼런스에 없는 플래그·키 없음
- DORA 5지표 정의 5건 번역·"MTTR → Failed Deployment Recovery Time"·"original four keys → current five-metric model" — web 자료 27 + dora.dev 가이드 웹 재확인(2026-10-19) 일치. *Accelerate*(2018) 설문 기반 상관 연구 고지 — 자료 45 지침 일치
- 커뮤니티·업계: Wmedia #151 2026-07-31 인용 3건("subtype"/"is_error"/"Agent aborted…")·H7 세 줄·root UID 0 "현장 보고로는" 표기(community P8 [검증 필요]) / codex-action@v1 `sandbox` 3값·`safety-strategy` `drop-sudo`(web 자료 34) — 일치
- 학술: Xia & Miller 2026 프리프린트 10%p→약 6%(논문 36) / Writing effective tools 2025-09-11 인용 2건(자료 20) / Bainbridge 1983 요지(논문 38) — 일치
- 분량·문체 무변경
### 미해소
- (없음)

## 13장 (라운드 1)

### ❌ 정정
- 출처 표기 2건: "(레퍼런스의 논문 리서처가 확인했다)" → 수학 근거 직접 명시 "정규분포 단측 꼬리 확률(약 0.159·0.0228·0.00135)의 역수를 반올림한 값" (1/0.1587≈6.3, 1/0.02275≈44.0, 1/0.00135≈740.7 — 검산 일치) / "웹 리서처가 … 확인했고 논문 리서처는 2차 자료로만 봤다" → dora.dev 가이드 정의 문장 직접 인용 + "2026-10-19 확인" — 독자에게 보이지 않는 내부 리서치 과정을 출처로 쓴 표현 제거. 4.1 #13: dora.dev 가이드 웹 재확인(2026-10-19) — Instability 아래 "Deployment rework rate: The ratio of deployments that are unplanned but happen as a result of an incident in production." 존재, "shifting from the original four keys to the current five-metric model" 문구 확인 → 1차 출처 채택 확정
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — OTel 구버전 주의 박스에 "코스(2026-08)"/"현행(2.1.303)" 병기, Claude Tag "(2026-06-23)", Building effective agents "2024년 12월", Anthropic 보안 SDLC "2026년 7월" 모두 초안에 있음. 이 장은 DORA 연차 보고서 수치를 쓰지 않아 2024/2025/2026 연도 병기 대상 없음)
### ✅ 확인 (요약)
- 코스 예시 5블록 토큰 단위 일치(primary/13): 탐지 출력 JSON(1.9/0.2/0.02), `bands.yaml` 9줄(`Read,Grep,Bash(gh run view *)`·`runbook:rollback-deploy`), Python 27줄(비공백; `MIN_SIGMA = 0.01`·`len(baseline) < 24`·규칙 5개 순서·`round(…, 4)`), 사고 `intent.md` 16줄(4f2c9e1·13:52·14:00·14:02·14:04·8c41d07·60→0·50 rps·R4), eval JSON 12줄(`4f2c9e1~1`·`grep -Eq 'CACHE_SECONDS = [1-9]'`) — 들여쓰기 복원 외 무변경. 산술 검산: 3σ 선 0.2+3×0.02=0.26 ✓, 탐지→복구 14:00→14:04 4분 ✓. "33줄"은 코스 자기 서술로 귀속됨(캡처 블록은 공백 포함 31줄 — 캡처 시 공백 줄 손실 가능, 코스 귀속 표기라 그대로 둠)
- 4.1 #8 Goodhart: 인용문 → Marilyn Strathern 1997 *European Review*, Goodhart는 "영국 통화 정책을 다룬 글(1984년 출판)"의 원리 제안자(1975 강연 재수록) — papers 논문 48 서지 일치. Manheim & Garrabrant 4변종·프리프린트 표기·Adversarial 변종 — 일치
- 컨트롤 밴드: 코스 정의·1/6·1/44·1/740·720회/하루 4·월 16·월 1·Western Electric 1956 "4 of 5 above 1σ / 8 in a row above mean" — primary/13 일치. Shewhart 1930 *Bell System Technical Journal*·Western Electric 핸드북 1956 — 자료 49 서지 일치. 코스 7단계·"detection stays entirely deterministic"·"drift rule counts as 2σ"·거버넌스·측정 2지표·Examples 3건·Claude Tag 절 인용 — 원문 일치
- Claude Tag: "첫 대응자" 묘사를 코스 서술로 귀속 + 발표 페이지(2026-06-23) 내용(Team/Enterprise 베타·Opus 4.8·채널별 도구·토큰 한도·작업 로그)·"사고 채널 시나리오는 직접 등장하지 않는다" — web 자료 25 주의 사항 그대로. Pro/Max 해당 없음·대안(webhook→`claude -p`, Routines) — 01_reference 2.12 일치
- OTel 구버전 박스: 기본 off·`CLAUDE_CODE_ENABLE_TELEMETRY=1`·`OTEL_METRICS_EXPORTER=otlp`·리포 설정 불가·`claude_code.session.count`·`tool_decision(source="hook")`·개인 대체 `total_cost_usd` — web 자료 16·5장 표 일치. `SessionStart` 평문 stdout 인용 — 자료 1 일치
- 학술·측정: SPACE Forsgren 외 *CACM* 2021·5차원·"적어도 세 차원"(web 자료 31, GitHub Blog 경유 — 원문 403이라 2차 인용임을 인지, 레퍼런스 채택 유지) / Li 외 2025 프리프린트 456,000+ PR·5에이전트·"accepted less frequently"(논문 34) / Kapoor 외 TMLR(논문 15) / METR 20%·19%(논문 2) / Ziegler MAPS '22(논문 6) / Building effective agents 2024-12-19 "workflow" 정의(자료 19) / Anthropic 보안 SDLC 2026-07-21 트리아지 에이전트 3권한(자료 24) — 일치
- 커뮤니티 P14: "1차 사례 거의 없음"·벤더 수치 미사용·현장 지표 5종("You are right!" 횟수 등) — community.md 일치. 코스 레슨 14 맺음말 번역 — primary/14 일치. 리소스 순서 재배열은 "개인이라면"으로 이 책 제안임이 드러남(코스 귀속 아님)
- 레퍼런스에 없는 플래그·설정 키·훅 이벤트명 없음. 분량·문체 무변경
### 미해소
- (없음)

## 14장 (라운드 1)

### ❌ 정정
- "`.github/workflows/`의 네 파일명은 이 책의 제안이다" → "`api-policy.yml`·`release.yml`·`bands.yml`은 이 책의 제안 … `agent-evals.yml`과 나머지 경로는 코스 예시 파일에 적힌 그대로" — primary/09 66행에 `.github/workflows/agent-evals.yml` 경로가 코스 원문으로 명시됨(`name: Agent evals`도 원문). 역방향 오귀속(코스 것을 책 제안으로)이지만 사실 정정
- "2장에서 소개한 `/cost`" → "`/usage`(별칭 `/cost`)" — 02_final.md 166행(공식 commands 문서: `/cost`는 `/usage` 별칭)과 통일
### ⚠️ 약화·삭제
- (없음)
### 🕒 신선도
- (없음 — "Claude Code 2.1.303 / 2026-10 기준" 재선언, 정책 배경 연월(2026-04·05) 명시 있음)
### ✅ 확인 (요약)
- 파일 트리(레퍼런스 3장 사례 체인 표 정전 + primary 대조): `CLAUDE.md`(5장, "Verifying your work" 블록 8장)·`REVIEW.md`(10장)·`bands.yaml`·`.mcp.json`·`intent.md`(J. Ortiz)·`spec.md`(R1~R4)·`plan.md`·`.claude/settings.json`(6장 PostToolUse+11장 PreToolUse)·`.claude/hooks/api-policy.sh`·`release-gate.sh`·`.claude/skills/secure-api-review/SKILL.md`·`.claude/agents/verifier.md`·`scripts/check-endpoints.sh`(primary/06 63·91·122·144행, primary/09 61행 — 훅·PR 체크·eval 공용 ✓)·`evals/status-no-pii-in-logs.json`·`evals/status-panel-keeps-its-cache.json`·`evals/check.sh`·`evals/log_bodies.py`(primary/09 46·113·162행)·`portal/src/claims/StatusPanel.tsx`·`claims-api/routes/status.py`·`claims-api/tests/test_status.py`(primary/04 60행) — 전부 코스 경로와 일치. 제안 경로(`intent/` 하위 폴더명·워크플로 3파일)는 코스 귀속 없이 "이 책의 제안"으로 표기됨 ✓
- 파일 연결 표 12행 — 레퍼런스 3.1 "다른 파일과의 연결" 열과 일치(REVIEW.md "관리형 Code Review만 읽음" = 3.5 "서비스만 읽음")
- 코스 레슨 14 인용·귀속: "사람은 판단이 필요한 모든 결정에 책임을 진다"(레슨 1 "Humans remain accountable for every decision that requires judgment", 01장 로그에서 원문 일치 확인) / "The loop keeps running. Human judgement stays above it." — primary/99 981행 원문 글자 단위 일치, **블로그판** 귀속 정확(코스판 레슨 14에는 없음 — 1.7 표·primary/14 대조)
- 최소 측정 세트 다섯(DORA 3: 배포 빈도·변경 리드타임·변경 실패율 + 비용 `total_cost_usd`/사용량 창 + 자기 보고 1) — 레퍼런스 6.1 Play 12 개인 열·2.12 적용 포인트·13장 final과 일치. 보조 2개(첫 패스 머지율·diff 읽기 체감)는 이 책 제안으로 읽힘
- 30일 표 수치: CLAUDE.md 200줄(공식, 4.3), eval 5개("코스 20~50개에서 줄인 수" 고지 — 4.3 합성 제안), 훅 3개·워크트리 2개(6.1), "선행 조건 없는 플레이 여섯 가운데 셋 — CLAUDE.md·피드백 루프·훅" — 1.6 6개 목록(Play 1·3·4·5·7·10)에 Play 4·7·10 포함 ✓. 순서는 "이 책의 합성 제안이고 코스 원문의 순서가 아니다" 고지 ✓
- 공식 Best practices 실패 패턴 5종·"두 번 넘게 교정하면 `/clear`"("more than twice", web 자료 14) — 일치. METR 20%/19%(논문 2), 훅 결정값 4개, `dontAsk` — 앞 장 final과 일치
- 한국 독자 문단: Windows 네이티브 샌드박스 미지원·훅 보고 상이→WSL2 권고(8장 한계 범위 내), 한국어 CLAUDE.md "길이가 언어보다 크다"(4.1 #5), 망분리 "정책 배경(2026년 4월 시행세칙 개정, 5월 망분리 한시 완화)까지만"+"로직이나 구조만, 더미 데이터" — 8장 한계 지침 준수. 한국 기업 사례 언급 없음(토스·LY 외 기업 없음 ✓)
- `<!-- editor: 파일 트리를 1~13장 실제 산출과 대조 -->` 주석 유지. 분량·문체 무변경
### 미해소
- (없음)
