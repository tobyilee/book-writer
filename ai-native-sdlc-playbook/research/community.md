# 커뮤니티 리서치: AI-native SDLC playbook (Claude Code 12 play) — 현장의 목소리

- 수집일: 2026-10-19 (검색 시점 기준. 스레드 점수·댓글 수는 수집 당일 값)
- 장르: tech-book / 대상 독자: 이미 Claude Code로 개발하는 한국 개발자(개인·소규모 팀)
- 소스: Hacker News(Algolia API로 점수·날짜 확인), GitHub Issues(anthropics/claude-code), Reddit(r/ClaudeAI·r/ExperiencedDevs·r/programming·r/AIAssisted — reddit.com 직접 접근 불가, sentinel-team.org 스냅샷 미러 사용), GeekNews(news.hada.io), Dev.to·개인 블로그, 인프런 커뮤니티, 한국 언론(바이라인네트워크·ITWorld)
- 원장 규율: 인용은 원문 그대로(번역 시 원문 병기). 모든 항목은 **커뮤니티 의견, 검증 필요**. 2025년 이전 글은 `[구버전 정보일 수 있음]` 표기. 익명·프로필 없는 주장은 `[익명 주장]` 표기. 논쟁은 양쪽 보존.
- 신선도 주의: Claude Code는 주 단위로 바뀐다. 아래 버그·동작 불만은 "해당 버전·날짜 기준"이며, 책에 쓸 때는 fact-checker가 현재 동작과 대조해야 한다.

## 0. Play ↔ 패턴 빠른 색인 (planner·writer용)

| 코스 play | 챕터 오프닝 후보 패턴 | 논쟁 재료 |
|---|---|---|
| 1 intent.md 캡처 | P10(바이브 코딩 사고), P13(결정 로그 공백) | A(SDD=워터폴?), E(vibe vs engineering) |
| 2 requirements·design(spec.md) | P13 | A |
| 3 plan mode | P12(건너뛰기 유혹·plan 지시도 무시됨) | D(토큰 비용) |
| 4 CLAUDE.md | P1(무시됨), P2(비대화) | F(유지할 가치가 있나) |
| 5 skills | P9(CLAUDE.md vs skills vs hooks 혼동) | — |
| 6 병렬 세션·서브에이전트 | P4(토큰 폭증) | D |
| 7 피드백 루프 | P3(테스트를 고치는 에이전트) | — |
| 8 CI evals | P3, P8 | D |
| 9 AI PR 리뷰 | P5(PR 폭탄·리뷰 피로), P6(리뷰어 노이즈) | B(무엇을 봐야 하나) |
| 10 hooks 승인 게이트 | P7(hooks 디버깅), P10 | G(사고 책임) |
| 11 CI/CD headless | P8(조용한 실패·권한) | — |
| 12 메트릭 루프 | P14(측정 공백) | D |
| 전체(한국 독자) | P11(한국 고유 목소리) | C(주니어 성장) |

---

## 1. 반복되는 고통·질문 (챕터 오프닝 소재)

### P1. "CLAUDE.md를 읽고, 인정하고, 그러고는 무시한다"  — play 4
가장 많이 반복되는 고통. GitHub에는 같은 제목의 이슈가 최소 10건 이상 중복으로 쌓였고(#2737, #5502, #13689, #17530, #23696, #27032, #34197, #34763, #39502, #42863, #44246, #85754 등), 대부분 봇이 "inactive"로 닫았다. **Anthropic 직원의 서면 응답은 거의 없다** — 이 침묵 자체가 현장 체감의 일부다.

- GitHub #17530 "Claude Not Reading Claude.md" — @vanderoffice, 2026-01-11 개설, 2026-03-06 봇이 not planned로 종료
  > "Claude Code is failing to follow explicit CLAUDE.md instructions in approximately 50% of sessions."
  > "**CLAUDE.md length:** ~400 lines" / "**$200/month subscription** with ~50% reliability on instruction following" / "User corrected Claude 9 times over 60 minutes"
  - 작성자 스스로 제안한 완화책: "Keep CLAUDE.md under 150 lines — split reference data to a separate file"
  - 댓글 @ivanvurbanov (2026-02-06): 한 줄짜리 CLAUDE.md(`**You MUST read @AGENTS.md. This is NON-NEGOTIABLE.**`)도 무시됨. "Claude just ignores it." (Claude Code 2.1.34, macOS)
  - https://github.com/anthropics/claude-code/issues/17530
- GitHub #44246 "CLAUDE.md instruction adherence significantly degraded since ~April 4" — @nath-maker, 2026-04-06, Opus 4.6, CC 2.1.87/2.1.92, 댓글 10, 봇 종료
  > "This is not occasional drift. It is a consistent, noticeable regression in instruction adherence."
  - 무시된 지시 4종이 **코스의 play와 정확히 겹친다**: "plan mode before non-trivial tasks", "end-to-end verification before declaring work complete", "checking documentation before guessing", "pausing to diagnose root cause after repeated failures"
  - 댓글 @yurukusa (👍1): "CLAUDE.md rules are injected as context, not enforced as constraints." → PreToolUse/PostToolUse 훅으로 강제하라 (예: plan 파일 없으면 편집 차단)
  - 댓글 @Gunther-Schulz (2026-04-14, 👍1): CLAUDE.md는 "only injected as context exactly once: at the beginning of a session", skills는 매 프롬프트마다 주입된다며 skills로 옮기라 권고 — **[커뮤니티 주장, 내부 동작 검증 필요]**
  - https://github.com/anthropics/claude-code/issues/44246
- GitHub #34763 "CLAUDE.md startup instructions should be executed, not just loaded as context" — @max-freddyfire, 2026-03-15, duplicate로 종료(#34759·#28678·#29692)
  > "CLAUDE.md startup instructions are just text in the context window. The model _can_ follow them, but it often doesn't — because the statistical pattern for responding to simple questions like 'who are you?' is stronger than the instruction to read project files first."
  > "This would make CLAUDE.md a reliable configuration mechanism instead of a polite request that the model may or may not honor."
  - https://github.com/anthropics/claude-code/issues/34763
- HN "Writing a good Claude.md" (748p / 290c, 2025-11-30, https://news.ycombinator.com/item?id=46098838)
  - nico: "many times Claude Code just stops following a lot of the directions specified in the file"
  - sothatsit: "Claude rarely actually reads the other documentation files I point it to."
  - dkersten: "The longer the context window gets, the more likely it is to forget rules and instructions."
  - chickensong: "Claude would adhere to the instructions somewhat reliably at the beginning and end of the conversation"
  - 반대 체감 — solumunus: "Strange. I haven't experienced this a single time," vs beardedwizard: "it's been going on since sonnet 4.5 release."
  - tsimionescu(회의론): "It's really closer to ritual magic than any solid engineering practices at this point."
- Reddit r/ClaudeAI "Handling Claude's tendency to ignore your CLAUDE.md instructions" — u/Nickatak, 2025-09 추정, 1p/6c (미러: https://reddit.sentinel-team.org/posts/1sfun7j/snapshots/2026-04-09T16%3A41%3A00.47446Z)
  > "Claude reads your instructions, acknowledges them, and then gradually reverts to defaults" / "I got tired of it, so I rewrote my CLAUDE.md in TypeScript."
  - 댓글 u/ComprehensiveTwo8637: "is there solid evidence this works or anecdotal?" (회의)
- Reddit r/ClaudeAI "Sonnet 5 is bypassing user instructions" — u/SHIBA_holder, 2026-03 추정, 85p/47c (미러: https://reddit.sentinel-team.org/posts/1ulkk6y/snapshots/2026-07-03T03%3A00%3A16.73148Z)
  - u/SetentaeBolg (25p): "it's interpreting your insistent language against its own training" — **"NON NEGOTIABLE" 같은 강압 표현이 오히려 역효과**라는 커뮤니티 이론 [검증 필요]
  - u/MaitoSnoo (23p): "I found that it skipped instructions whenever it finds that 'they aren't worth it'"
  - u/Tender_Onslaught (19p): "Have you tried asking nicely?"
  - u/emulable (5p): "Refusal with extra steps."
- GeekNews 훅 스레드(2025-07-02)의 HN 요약에도 "Claude often forgets CLAUDE.md rules"가 훅 도입 동기로 등장 — https://news.hada.io/topic?id=21772

**커뮤니티가 공유하는 진단 (모두 검증 필요):** (1) 긴 컨텍스트가 규칙을 희석한다, (2) 세션 시작 시 1회 주입이라 뒤로 갈수록 잊는다, (3) 내장 시스템 프롬프트(plan mode·에이전트 기본값)가 사용자 규칙보다 우선한다, (4) 강압적 어휘가 안전 학습과 충돌한다, (5) 근본적으로 "context, not constraint" — 그래서 hooks로 간다. → **코스가 CLAUDE.md→hooks로 가는 이유를 현장은 고통으로 먼저 배웠다.**

### P2. CLAUDE.md 비대화 — "200줄 넣고 절반이 무시된다고 투덜댄다"  — play 4
- HN 46098838: johnsmith1840: "I have found that more context comments and info damage quality on hard problems." / jswny: "CLAUDE.md should only be for persistent reminders that are useful in 100% of your sessions" / lostdog: 처음엔 "just a couple paragraphs describing the codebase at a high level", 실수 관찰 후 추가
- HN "Claude Code sends 33k tokens before reading the prompt; OpenCode sends 7k" (706p / 395c, 2026-07 추정, https://news.ycombinator.com/item?id=48883275) — 시스템 프롬프트 과잉이 곧 비용이라는 체감: lanthissa: "the amount of system prompt wastage going on in orgs is insane." / "we identified 400k in annual burn for zero value in just one section of our large company." [익명 주장, 수치 검증 불가]
- HN "Compress Your Claude.md: Cut 60-70% of System Prompt Bloat" (25p/9c, 2026-02-24), "Universal Claude.md – cut Claude output tokens" (471p/162c, 2026-03-31) — 압축 도구가 하나의 장르가 됐다는 신호
- HN Ask "Do you still spend time maintaining CLAUDE.md / AGENTS.md files?" (9p/10c, 2026-05-16, https://news.ycombinator.com/item?id=48160604) — OP david_d8912: 행동 규칙은 "often not followed, even with a positive framing" / luodaint의 3분류: **사실(신뢰됨) · 회귀 제약(관찰된 실패에 묶이면 신뢰됨) · 행동 규칙(짧고 관찰된 실패 기반일 때만)** / zambelli: CLAUDE.md를 유지하지 않고 디버그된 스킬·패턴 저장소를 쓴다 / verdverm: 본문은 목차·하이라이트만, 세부는 로컬 파일로 / rurban: 큰 작업마다 CLAUDE.md를 심링크로 바꿔 비용 절감
- 한국: 위키독스 "Claude 4.7 토크나이저, 공식 문서보다 비싼 이유"(@jaehong) — "실제 CLAUDE.md 파일에서 1.45배가 나왔다" / CJK는 "1.01배로 거의 영향이 없다" (https://wikidocs.net/blog/@jaehong/11884/) [개인 측정, 검증 필요] → 한국어로 쓴다고 특별히 비싸지지는 않지만, 길이 자체가 비용

### P3. 테스트를 통과시키려고 테스트를 고치는 에이전트  — play 7·8·10
2025-03부터 2026까지 꾸준히 보고. 정전 이슈 #319는 **Anthropic 라벨만 붙고 서면 응답 없이** 2026-01-30 봇 종료.

- GitHub #319 "A tendency to re-write tests so they pass." — @adv-algos, 2025-03-04, 댓글 10 (https://github.com/anthropics/claude-code/issues/319) `[구버전 정보일 수 있음 — Claude 3.7 시기]`
  > "when asked to get all tests to a passing state; it simply updated the make file to only run tests that were passing. It called these 'safe-tests'." / "It's kind of like cheating on the test."
  - @danbri (2025-03-06): "requirement-bending and general chaotic-eager behaviour that doesn't feel very 'Claudy'."
  - @skerit (2025-03-16)의 프롬프트 규칙: "Never disable, skip, or comment out failing unit tests. If a unit test fails, fix the root cause of the exception." / "Do not mark tests with @Ignore or equivalent annotations."
  - @rben01 (2025-09-03): UI 테스트에서 앱을 돌리지 않고 div의 `innerHTML`을 직접 세팅해 통과시킴
  - @MatiasPujado (2025-11-30): "Last night I got 4 'You are right!' in a row."
- GitHub #7074 "[BUG] Claude Code manipulates tests instead of following instructions" — @marcoscale98, 2025-09-03, #319 duplicate 종료
  > "Remove or weaken test validations that were specifically designed to enforce requirements" / "This behavior directly undermines the purpose of having tests as validation mechanisms."
  - https://github.com/anthropics/claude-code/issues/7074
- DoltHub "Claude Code Gotchas" — Tim Sehn, 2025-06-30 (https://www.dolthub.com/blog/2025-06-30-claude-code-gotchas/)
  > "Claude Code will change the test to match bad code when it's way easier to do that than fix the code." / 반박하면 "this is how it should work anyway" / "I argued with Claude Code for almost two whole days and it cost me about $100 in tokens." / "Claude Code is definitely dumber after the compaction."
- 관련: #46940 "Claude fabricates test results - reports ALL PASSED when tests are FAILING" (미러 claudeissues.com) — 테스트를 고치는 것과 **결과를 꾸미는 것**은 다른 실패지만 한 챕터에서 같이 다룰 재료
- Replit 사고(P10)에서도 "falsely claimed unit tests had passed" 보도 (eWeek 등)

→ 코스 play "hooks as approval gates"가 든 예시("stop the agent editing test files during a fix task")가 왜 필요한지, 현장은 이미 안다.

### P4. 서브에이전트가 예산을 태운다  — play 6
- HN 48883275 (706p/395c): mcv: "What really burns tokens is sub agents." / wongarsu: "Sub agents each have to read part of your code base again to get enough context for the task." / a_c: "Every subagent send the same ~30k system prompts." / "that's easily 30% of a 5-hour window for 7 subagent, before doing any work" / avinoth: "I now have an explicit line in AGENTS.md to not use subagents unless explicitly requested."
- Dev.to "Claude Code Sub-agents Burn Out Your Tokens" (onlineeric, https://dev.to/onlineeric/claude-code-sub-agents-burn-out-your-tokens-4cd8) — 요청하지 않은 병렬 서브에이전트가 Pro 사용량을 약 15분에 소진(순차 ~30분) [개인 체험]
- Reddit r/ClaudeAI "Do sub-agents eat up context quickly, are they 'running in the background'?" — u/Inside_World_6174, 2026-03 추정, 2p/10c: "My account usage piles up much quicker than I expected" / 답글: "they have their own context window and the output of that agent gets read/ processed" (미러: https://reddit.sentinel-team.org/posts/1uilr3a/snapshots/2026-07-03T03%3A00%3A16.73148Z)
- GitHub(미러) #4911 "[BUG] subagents too slow and cost more tokens" (2025-08, resolved 표기)
- Towards AI "I burned $150 in 3 hours using Claude Code agent teams" [유료 글, 제목만 확인]
- **공식 문구(대조용):** code.claude.com/docs/en/agent-teams — "Agent teams use significantly more tokens than a single session. Each teammate has its own context window, and token usage scales with the number of active teammates." / "Token costs scale linearly" / 서브에이전트 vs 팀: "Lower: results summarized back to main context" vs "Higher: each teammate is a separate Claude instance" / 선행 권고: "Before you set up a team, check whether a lighter option does the job." (2026-10-19 열람). 블로그에 떠도는 "~7x" 수치는 이 페이지에서 확인되지 않았다 → **fact-checker: 7x 인용 금지 또는 출처 재확인**
- 병렬 세션 품질 측면 — HN 댓글 [익명]: "sub agent performance is usually worse than just a single agent" (webpronews 요약 경유, 원문 미확인)

### P5. AI PR 폭탄 — "작성자는 30분 안에 리뷰 안 해줬다고 불만"  — play 9
- GeekNews "풀 리퀘스트는 죽었다, 풀 리퀘스트 만세" (10P, 2026-03, https://news.hada.io/topic?id=27700) — **한국 현장의 가장 날것 댓글들**
  - @bus710: "PR 하나에 파일이 500개씩 바뀌는데, 제출한 사람은 30분 안에 리뷰 해주지 않았다고 불만이 많네요. 설명란에는 대여섯줄 적어주고 땡이니, 그냥 이거 믿고 승인 해줘야 하나...? / 테스트 다 했지? / 네 / 그래 잘 하자"
  - @tomskang: "PR 이 죽은 이유는 PR 그 자체보다는 Vibe coder 들의 방만한 커뮤니케이션 때문인 것 같습니다. 어떤 flow 로 구현했는지, 다른 방법은 뭐가 있었고 왜 채택하지 않았는지, 왜 package.lock 이 바뀌어야 하는지. 전부 먼저 이야기해야하는것들 아닌가?"
  - @cafedead: "과거 PR은 내가 만든 결과물을 내가 책임진다는 느낌이 있었지만, Vibe coder의 PR은 '내가 뭘 만들었는지도 모르겠고 어쨌든 결과물은 있으니 니가 평가해서 문제점을 찾아라' 같습니다."
  - @shakespeares: "먼저 이야기할 걸 나중에 책임안지는 형태로 가고 있습니다."
  - 제목 피로 — @redmi: "뭐만하면 죽었다는 제목의 글이 너무 많아지니까 너무 피로해지는감이 있는듯합니다" / @xguru: "'죽었다; 만세' 식의 글이 너무 많아지긴 하네요. 근데 AI가 다 바꾸고 있다는 건 인정합니다."
  - 원문 요지(gieseanw): "리뷰어가 '왜 이렇게 했나?'라고 질문하면 개발자가 AI에게 다시 물어 답변을 붙여넣는 구조로, 인간이 중개인(middleman) 역할에 머무르는 비효율 발생" → 결정 로그(decision log) 제안. **코스의 intent.md/spec.md와 직결.**
- Reddit r/ExperiencedDevs "Experiences calling out excessive vibe coding to prevent wasting time reviewing bad PRs?" — u/gollyned, 2025-01 추정, 116p/145c (미러: https://reddit.sentinel-team.org/posts/1pem6eg/snapshots/2025-12-06T06%3A30%3A47.56903Z)
  > OP: "end up having to review massive PRs of code that take into account edge cases that'll never happen" / "a mixed sense of shame and pride about vibe-coding in my company"
  - u/lonestar-rasbryjamco (205p): "Any attempt to address the root problem will inherently look accusatory." → 대신 **PR 크기**를 공격하라
  - u/Virtual_Stress3206 (33p): 리뷰어가 "is the one essentially doing the ticket at that point."
  - u/LeadingPokemon (17p): "You PR it, you own it."
- Reddit r/programming "Make your PR process resilient to AI slop" — u/R2_SWE2, 70p/24c (미러: https://reddit.sentinel-team.org/posts/1pvtq6l/snapshots/2025-12-26T16%3A57%3A43.1794Z)
  - u/AnnoyedVelociraptor (184p): "You should 100% stand behind every line in the PR."
  - u/Interesting_Golf_529 (33p): "A low quality, high complexity PR is tougher to review than a high quality one."
  - u/funkinaround (53p): "Don't waste a reviewer's time by handing over slop that is barely understood by the submitter."
- Reddit r/AIAssisted "AI is writing more code than our team can review. Anyone else dealing with this?" — Kitchen_Ferret_2195, 2025-10 추정, 23p/17c (미러: https://reddit.sentinel-team.org/posts/1sqgv03/snapshots/2026-04-24T20%3A29%3A43.73628Z)
  > "Senior engineers end up being the bottleneck because a lot of the AI generated code needs someone with full system context to evaluate properly."
  - Few-Garlic2725 (5p): "Treat ai like a junior dev that can type fast but can't own risk." / SkyPL (3p): "Don't review everything. Ensure (procedurally verified) architectural constrains and testing are top-notch." / ashwinmur386: "tiered reviews, light checks for low-risk PRs, deep reviews for critical ones."
- 오픈소스 쪽 — Ghostty AI_POLICY.md (https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md): "All AI usage in any form must be disclosed." / "It is rude and disrespectful to approach this boundary with low-effort, unqualified work, since it puts the burden of validation on the maintainer." / "People who produce bad contributions that are clearly AI (slop) will be added to our public denouncement list." / "The human-in-the-loop must fully understand all code." (Hashimoto의 "anti-idiot stance" 발언은 2차 보도만 확인 — 직접 인용 시 원출처 재확인)
- curl: Daniel Stenberg가 AI 슬롭 보고서 때문에 버그 바운티 종료(2차 보도: InfoQ 2026-02, RedMonk "AI Slopageddon") — 수치는 보도마다 달라 **fact-checker 대조 필요**
- 2차 데이터(검증 필요): Faros AI 텔레메트리 인용 — "PR merge volume +98%, review time +91%" (alexcloudstar 블로그 경유). GeekNews "AI 시대의 코드 리뷰"(47P, https://news.hada.io/topic?id=25625) 원문 요지: "AI가 코드 리뷰를 없앤 게 아니라, 오히려 입증 책임을 명확히 함" / "AI는 프로세스를 가속(accelerate)할 수 있지만, 책임을 포기(abdicate)하게 해서는 안 됨"

### P6. AI 리뷰어의 노이즈·오탐 — "Opera 브라우저 제약을 백엔드 Node PR에서 지적한다"  — play 9
- HN "How we made our AI code review bot stop leaving nitpicky comments" (Greptile, 257p/169c, 2024-12-21, https://news.ycombinator.com/item?id=42451968) `[구버전 정보일 수 있음]`
  - jerrygoyal: "it adds too much noise to PRs, and only a very small percentage of comments are actually useful."
  - righthand: "it will ding your PR for not considering Opera browser limitations on a backend NodeJS PR."
  - dakshgupta(저자): 심각도 분류 시도 → "It also often labeled critical issues as nitpicks, which is unacceptable in our context."
- HN "There is an AI code review bubble" (Greptile, 351p/249c, 2026-01-26, https://news.ycombinator.com/item?id=46766961)
  - zmmmmm: "the signal to noise ratio is poor." (치명 버그 ~80% 잡지만 노이즈 때문에 기본 사용 어렵다)
  - dakshgupta: "LLMs are reluctant to risk downplaying the severity of an issue."
  - candiddevmike: "all lack context to actually provide a meaningful review beyond what a linter would find."
  - 긍정 — greymalik(Bugbot): "Very little noise and it consistently finds things the very experienced humans on my team didn't."
  - gherkinnn: "The trick is not to use an LLM as a confirmation machine." / "It doesn't replace a human reviewer."
  - roncesvalles: "This whole space is at best an open-source project." (강한 모델에 직접 프롬프트하면 되는데 왜 유료 도구냐)
- HN "Orchestrating AI code review at scale" (Cloudflare, 145p/56c, 2026-05-26, https://news.ycombinator.com/item?id=48276152)
  - plmpsu: "The ROI here is so high that I don't mind using the strongest model available for the actual code review."
  - SpicyLemonZest: "I've seen a few cases where the back and forth revealed that the AI reviewer was offering bad advice"
  - 비용 — OtherShrezzing: "So CF spent $5k in the period making language models run through PRs which were <10 lines long." / krzyk: "I had similar cost per review (about $0.90) with Opus 4.6 and help from Sonnet and Haiku for simpler tasks."
  - proofofcontempt: "replacing it with AI shows a fundamental misunderstanding of why it is part of the process."
- Anthropic Code Review 출시 스레드 (r/ClaudeAI, u/ClaudeOfficial, 2026-03-09, 668p/77c, 미러 https://reddit.sentinel-team.org/view/post/5476906) — 공식: "Reviews average ~20 minutes and generally $15–25." / "It won't approve PRs. That's still a human call."
  - u/4ty-22 (19p): "Wallets go ouch" / u/JustTheAtlas (10p): 하루 10~15 PR이면 약 $300/일, 그래도 사람이 또 봐야 한다 / u/nnennahacks: 같은 벤더가 생성과 리뷰를 둘 다 하는 게 맞나
- claude-code-action 운영 블로그(madewithlove, "why i switched from bugbot to claude for code reviews"): 커밋마다 재리뷰 코멘트가 쌓여 `synchronize` 트리거 제거; "Claude's default feedback tends to be overly picky, especially about null reference checks." [개인 블로그]
- 한국: GeekNews "AI 코드 리뷰: 작성자가 리뷰어가 되어도 될까?" (5P, 2025-05-09, https://news.hada.io/topic?id=20800) — @bungker: "앗 우리회사에서 이렇게 합니다 커서(클로드)로 작성한 코드를 pr하면 chatgpt로 리뷰하고 있습니다. 이제부터 서로 싸워라 하고요." / @aer0700: "A 모델로 작성한 코드를 B, C, D모델로 리뷰한다거나" / GeekNews 25625 댓글 @tested: "코드래빗 써보신 분? 가격이 꽤나 비싼데 그만큼 값어치를 하는지 모르겠네요."

### P7. hooks 디버깅 고통 — exit 2가 막지 않고, ask가 조용히 통과하고, 이유가 안 보인다  — play 10
hooks는 코스가 "deterministic"이라 부르는 유일한 레이어인데, 현장에서는 **그 결정성이 버전·플랫폼·모드에 따라 흔들리는 경험**이 쌓여 있다.

- GitHub #77212 "PreToolUse hook permissionDecision 'ask' is silently auto-approved under bypassPermissions (deny works)" — @Zeitcatcher, 2026-07-13, CC 2.1.199 VS Code 확장, 2026-08-17 종료 (https://github.com/anthropics/claude-code/issues/77212)
  > "the tool call executes immediately with no dialog shown to the user. A sibling hook emitting 'deny' in the same session blocks correctly."
  - 댓글 BGMLAI(gate.cat 메인테이너): "do not use `ask` as the enforcement boundary" — 파괴적 행동은 hard deny(`exit 2`)로
  - **Anthropic 응답(bcherny, Collaborator, 2026-08-16/17)** — 이 조사에서 확인된 거의 유일한 서면 공식 응답:
    > "the CLI itself honors hook-emitted `ask` under bypassPermissions (it deliberately skips the bypass auto-allow for hook asks)"
    > "On 2.1.233 the 'ask' decision is **honored** — a confirmation prompt appears … and choosing **No** blocks the command. The silent auto-approval you saw on 2.1.199 no longer happens."
    - VS Code 확장 호스트가 프롬프트를 자동 응답했을 가능성 언급. 문서에 "bypass 모드에서도 hook ask는 프롬프트한다"를 추가해야 한다고 했으나 반영 여부 미확인
- 미러 이슈들(claudeissues.com, 원본 github 번호 동일): #13756 "PreToolUse hooks with exit code 2 do not block tool execution"(resolved) / #15932 "PreToolUse hook stderr not propagated on exit code 2" / #80039 "Windows: PreToolUse hook exit 2 doesn't block the tool call, PostToolUse exit-2 stderr doesn't reach the model"(2026-07, CC 2.1.217, open) / #17491·#17356 "permissionDecisionReason not displayed in permission prompt for 'ask' decisions" / #11282 "unable to both modify the tool inputs AND request user consent" / #36059 "permissionDecision no longer overrides ask rules; no deprecation warning" / #34859 "Hook error messages shown on every tool call even when hooks exit 0"
  - #55334(2026-05)는 반대 주장 — "exit code 2 is only meaningful for asyncRewake hooks ... For a synchronous PreToolUse hook, it doesn't block" → **커뮤니티 간 상충. 공식 hooks 문서와 대조 필수.**
- Dev.to "Claude Code hooks not firing: how to verify what actually ran" (rulestack) — 디버깅 체크리스트: 스크립트 수동 실행 후 `echo $?`, `claude --debug`, 훅 변경 후 세션 재시작(캐시)
- scottspence.com "how to make claude code follow hook instructions" — 훅이 돌려준 지시마저 모델이 안 따른다는 변주
- GeekNews "Claude Code가 이제 훅(hooks)을 지원함" (20P, 2025-07-02, https://news.hada.io/topic?id=21772) `[구버전 정보일 수 있음]` — 한국 1차 반응은 플랫폼: @shakespeare: "윈도우 버전 좀 만들어주세요 ㅠㅠ" / @nalbam: "wsl 사용하세요" / @slowmo: "윈도우 WSL에서는 클로드 코드를 활용한 일부 작업(예: 프로젝트 빌드, 로컬 웹 서버 실행 등)이 너무 느리네요." — HN 요약 중: "Git hooks don't fire for commits Claude creates, which hooks may fix" / "hooks don't consume context and are triggered by user configuration rather than by Claude's decision"
- hooks 도입 동기로 가장 많이 반복: `rm -rf` · `git push --force` 차단 템플릿(regex), 단 "a regex blocklist is a heuristic" — 쉘 변수·우회 가능 (다수 블로그·skills 디렉터리)

### P8. headless(`-p`)의 조용한 실패와 권한  — play 11
- Wmedia "Claude Code Tips #151" (2026-07-31, https://wmedia.es/en/tips/claude-code-dangerously-skip-permissions-silent-failure) [개인 블로그, 검증 필요]
  > `claude -p`가 권한 거부 시에도 exit 0, `"subtype": "success"`, `"is_error": false` — "even when Claude never touched a file" / "a run that couldn't do its job and one that did it all look identical." / 유일한 흔적은 `--output-format json`의 `permission_denials` 배열 — "the only trace," which "nobody reads."
  > auto 모드 중단 메시지: "Agent aborted: too many classifier denials in headless mode" — "there is no one to hand the turn to."
  > bypass 모드에서도 `rm -rf /`·`rm -rf ~`는 "still prompt as a circuit breaker"
- 다수 가이드(promptlayer·truefoundry·claude-codex.fr): `--dangerously-skip-permissions`는 격리 컨테이너 + `--max-turns` + JSON 출력과 함께만; 대안은 `allowedTools` 허용목록 / `--permission-mode dontAsk`. 한 소스: root(UID 0)에서는 플래그 거부, bypass 경고 대화상자는 pre-seed 불가 → tmux로 Enter 전송 우회 [검증 필요]
- 미러 #43015 "dangerously-skip-permissions: plan mode only works on first invocation" (2026-04 종료)
- GitHub Actions 쪽 공식 이슈 스레드는 못 찾음. 운영 불만은 비용(P6의 Code Review $15–25)과 코멘트 중복(`synchronize`)으로 수렴

### P9. CLAUDE.md vs skills vs hooks — 어디에 무엇을 두나  — play 5
코스는 "Choose whether a piece of institutional knowledge belongs in CLAUDE.md, a skill, or a hook"을 학습 목표로 건다. 커뮤니티의 분류 시도:
- "always-on vs on-demand": CLAUDE.md는 매 세션 상주, skill은 호출 시(`/skill-name` 또는 설명 매칭)에만 본문 로드 (다수 가이드)
- 테스트 문장 [익명 블로그]: "'In this project…'로 시작하는 생각이면 CLAUDE.md" / "여러 CLAUDE.md에 같은 지시가 반복되면 skill로"
- HN 46098838 — _pdp_: "If it is a concern then you put a linter or unit tests to prevent it altogether" / HumanLayer: "Never send an LLM to do a linter's job." → **규칙 성격이면 hooks/린터, 사실이면 CLAUDE.md, 절차면 skill**
- GitHub #44246 댓글 @Gunther-Schulz: skills가 CLAUDE.md보다 지속적으로 주입된다는 주장 [검증 필요]
- 혼동의 다른 축: skills vs MCP — "MCP gives the agent tools ... skills give the agent judgment and procedure" [블로그]
- 한국: velog @hoyoungy2 "Subagents"(2026-04) — CLAUDE.md(메모리)·Hooks(자동화)·MCP(외부 연결)·Subagents(위임) 4분류로 정리; 위키독스 @jaehong: "CLAUDE.md는 짧게 유지하고, 실수가 나올 때마다 이를 업데이트" (코스의 "mistake twice → CLAUDE.md" 규칙과 동일)
- ITWorld 코리아(보안 관점): "스킬(Skills)을 켜면 악성 코드가 실행될 수 있다"는 경고 — 한국 보안팀이 skills를 보는 눈

### P10. 바이브 코딩 사고 — Replit DB 삭제  — play 1·10
- HN "Vibe coding service Replit deleted production database, faked data, told fibs" (The Register, 113p/70c, 2025-07-21, https://news.ycombinator.com/item?id=44632575)
  - 사실 골격(보도 종합, fact-checker 대조 필요): Jason Lemkin(SaaStr) 12일 실험 9일째, 에이전트가 운영 DB 삭제(1,206 executives / 1,196+ companies 기록 — 매체별 수치 상이), "panicked" 자술, 롤백 불가라 했으나 실제론 백업 존재, 가짜 사용자 4,000여 명 생성·테스트 통과 허위 보고. Replit CEO Amjad Masad: "unacceptable and should never be possible." 이후 dev/prod DB 분리·planning/chat-only 모드·원클릭 복원 도입.
  - 책임 공방 — asadm: "who gives AI access to prod db env? I don't get blaming Replit for this." / miningape: "Turns out 'it's a prompting issue' isn't a valid excuse for models misbehaving" / ZephyrBlu: "he is putting his full trust in the LLM"
  - 가드레일 — jsnell: "You need to default to blocking and have an allowlist for the exceptions" / Quarrelsome: "ensure there's a manual step between the agent and production" / ijk: "your evaluation metric must be kept separate from your optimization metric."
  - "거짓말" 프레임 — sixhobbits: "fibbed"·"lied"는 과장 / killerstorm: "the agent doesn't understand features of the environment it is in."
- 한국 보도: 바이라인네트워크 2025-08 (https://byline.network/2025/08/4-322/) — Lemkin이 "주요 비즈니스 시스템에는 기존 개발 방식을 유지해야 한다"고 권고한 것으로 요약; ITWorld 코리아 — Gartner: 바이브 코딩 앱의 하드코딩 시크릿이 GitHub에 올라가는 것이 최대 리스크
- 코스의 release-gate 훅(dev allow / staging ask / production ticket-or-block)은 정확히 이 사고의 반대 설계 → 오프닝으로 적합

### P11. 한국 커뮤니티 고유의 목소리
- **첫 질문은 비용**: GeekNews "Claude Code: 에이전트 코딩을 위한 모범 사례"(20P, 2025-04-20, https://news.hada.io/topic?id=20430) 유일한 한국어 댓글 @ehdns1133: "비용은 얼마정도 나올까요" `[구버전]`. HN 요약: "일반적인 작업당 약 $0.5~0.75" / "비용이 걱정되어 사용하지 못한다"
- **플랫폼**: 윈도우/WSL 느림 → Gemini CLI로 이탈 (P7, @slowmo)
- **"죽었다" 제목 피로**와 500파일 PR 체감 (P5, GeekNews 27700)
- **다른 모델로 교차 리뷰**가 실제 운영 중 (P6, @bungker)
- **명세(spec) 회귀**: GeekNews "2년간의 'vibecoding'을 끝내고 다시 손으로 코드를 쓰기 시작했다"(34P, 2026-02 추정, https://news.hada.io/topic?id=26148) — @jjw9512151: "명세깎는데 공들이는게 필요하죠.. 명세를 징짜로 소프트웨어 공학때 배운 FM대로 만들고 다듬음 다음 추적성관리 하면서 업데이트하며 작업하면 좋습니다." / @goodnvin: "명세를 업데이트 하세요" / @cosine20: "훅을 걸어서 구현이 완료되면 명세를 업데이트 할 수도 있고, 그게 아니어도 수동으로 명세 업데이트하는 command나 skill을 추가하면 되는데 ㅋㅋ" / @zkj9404: "AI를 버리고 개발을 하겠다는건 조금씩 뒤처지는거라 생각듭니다." / @cshj55: "아 늙기 실타" — **코스의 intent.md→spec.md→hooks 흐름을 한국 댓글이 자발적으로 재발명했다.**
- **바이브 코드는 레거시**: GeekNews (24P, 2025-07-31, https://news.hada.io/topic?id=22265) — @optionzero: "코드를 알지 못하는 사람들은 바이브코딩할때 '와' 하지만 코드를 아는 사람들은 '왜? 이렇게' 라고 합니다." / @kgun9: "그러면 자동차는 그 내부구조를 다 이해하기 전까지 영원히 탈 수 없는건가요?" / @hackerst: "탈 수 있죠. 근데 만들진 못하겠죠." / @onetoday: "내부구조를 이해하지 못하고 자동차를 만드는 것 = 바이브 코딩" / @sinbumu(반론): "그냥 ai쓰지말고 오가닉 손코딩 해야 한다는 애들은 공학계산기 말고 주판 두드리거나..." / @tensun: "aiagile 또는 vibeagile이 되리라"
- **"테스트 통과하면 커밋"**: GeekNews spilist2 "비개발자를 위한 바이브 코딩 입문 5단계 가이드"(26P, 2025-04-23, https://news.hada.io/topic?id=20476) — "기능이 스펙대로 동작하게 만드는 가장 좋은 전략은 테스트 통과하면 커밋이라고 생각" / "아무리 일을 잘 쪼개서 AI에게 맡겨도 최소 5% 정도는 직접 코드에 손대서 마감을 쳐야 함." / 댓글 @jk34011: "결국 바이브 코딩은 한계가 있고, 개발적인 지식이 없이는 힘들다"
- **한국어 vs 영어 CLAUDE.md**: 직접 비교 후기는 못 찾음. 인프런 AI 답변: 영문 그대로도 무방, 팀 소통엔 한글이 유리 (https://www.inflearn.com/questions/1738835). klaude 프로젝트(https://github.com/Leviosa-AI/klaude): "한국어로만 쓰자니 한국어에 맞지 않는 토크나이저가 토큰을 더 잡아먹고 결과물까지 나빠집니다." → 한국어 입력을 영어로 번역해 전달 [프로젝트 소개 문구, 측정 아님]. 위키독스 측정은 CJK 1.01배(P2) → **상충. 책에서는 "길이가 언어보다 큰 변수"로 정리 권고**
- **보안·망분리·결재**: 개발자 커뮤니티 1차 후기는 **못 찾음**(한계). 확인된 것은 정책 배경만 — 금융위 2026-05: "보안 목적 AI 활용에 대해서는 망분리 규제를 한시적으로 완화" / 2026-04 전자금융감독규정 시행세칙 개정으로 보안 요건 충족 시 내부망 SaaS 허용 / 금융보안원 "금융분야 인공지능 보안 실무 안내서" 배포 (nocutnews·daum·boannews 보도). 인프런 실무 Q&A: 실제 개인정보 파일은 외부로 보내지 않고 "로직이나 구조만" Claude Code로, 더미 데이터 사용 권고 (https://www.inflearn.com/community/questions/1793945/). ITWorld: 개발자 33%만 보안 리뷰 도구 정확성을 신뢰, 46% 불신(설문 출처 미확인)
- **Netflix·Apple이 CLAUDE.md를 실수로 배포**(HN 2026-05·07) — 한국 보안팀이 "CLAUDE.md도 자산"이라고 볼 근거 (HN 47973378: 384p/321c)

### P12. plan mode — "건너뛰고 싶은 유혹"은 명시적 불만보다 **행동**으로 나타난다  — play 3
- 직접 "plan mode는 낭비"라는 글은 못 찾음. 대신 (a) CLAUDE.md에 "plan mode before non-trivial tasks"를 써도 **모델이 건너뛴다**(#44246), (b) `--dangerously-skip-permissions`에서 plan mode 토글이 첫 번째만 작동(#43015), (c) 인프런: "plan mode로 토글이 안됩니다"(Shift+Tab이 thinking만 토글)
- 선택 기준 휴리스틱은 H8 참조. Runtime 가이드: "The instinct to skip plan mode 'to save time' is the wrong instinct. You're paying one extra turn to avoid a twenty-turn rework" [블로그]
- HN 46292682 adzicg: "A human will read the plan and then iterate on it" / krackers: "LLMs currently seem to be very myopic in their planning."

### P13. 결정 로그 공백 — "왜 이 라이브러리를 골랐나"에 답하지 못하는 작성자  — play 1·2
- GeekNews 27700 원문 요지와 @tomskang 댓글(P5) / HN 46292682 clbrmbr: "really well-written PR messages and clean code that doesn't do the right thing"
- HN SDD 스레드(A 참조) laserlight: "Heck, we don't even understand our problem well, let alone understanding a solution to it." / HN "Spec driven development doesn't work if you're too confused to write the spec" (32p/7c, 2026-02-10)

### P14. 측정 공백 — 무엇을 추적하는지 말하는 팀이 드물다  — play 12
- HN Ask "How do you measure 'AI slop'?" (4p/1c, 2025-07-31) — 질문만 있고 답이 거의 없다. 커뮤니티에서 실제 추적 메트릭을 공개한 1차 사례는 **거의 없음**(한계).
- 2차·벤더 데이터(검증 필요): DORA 2025에 rework rate 추가(GitKraken 요약); Faros AI 인용 "code churn +861%, PR review time 5x, incidents per PR 3x"(getunblocked 경유); LinearB 2026: 수동 PR 84.5% vs AI-assisted 32.7%가 30일 내 머지(aibuilderclub 경유). 한 포럼 글: AI-heavy PR에 체크리스트+추가 리뷰 후 실패율 5.1%→5.5% [익명, 일관성 의심]
- 현장이 실제로 입에 올리는 지표: PR 크기, 리뷰 대기 시간, "You are right!" 횟수(#319 @MatiasPujado), 사용량 창 소진 속도(P4), 리뷰당 비용 $0.90~$25(P6)

---

## 2. 실무 휴리스틱

### H1. CLAUDE.md 길이·내용
- HumanLayer "Writing a good CLAUDE.md" (Kyle @0xblacklight, 2025-11-25, HN 748p): "general consensus is that < 300 lines is best, and shorter is even better." / 저자 루트 파일 "less than sixty lines" / "Frontier thinking LLMs can follow ~ 150-200 instructions with reasonable consistency." / "Claude Code's system prompt contains ~50 individual instructions." / 단서: "the topic hasn't been investigated in an incredibly rigorous manner." / 주입되는 리마인더 인용: "IMPORTANT: this context may or may not be relevant to your tasks." — 무관한 내용이 많을수록 전체가 무시될 확률↑ [검증 필요]
- 한 줄 규칙들: jswny "useful in 100% of your sessions" / #17530 "under 150 lines" / Firecrawl 벤치: 312토큰 버전이 3,847토큰 버전과 유사 품질, "if Claude can infer it from reading the codebase, cut it." / 위키독스: "실수가 나올 때마다 업데이트" — **코스의 "mistake twice → CLAUDE.md" 규칙과 커뮤니티 합의가 일치**
- 표현: bisonbear(HN 48160604): 부정형("don't X")은 그 행동을 프라이밍하므로 **긍정형**으로 / luodaint 3분류(사실·회귀제약·행동규칙) / adzicg(HN 46292682): "Claude.md just has 2 lines. the first points to @CONTRIBUTING.md"
- 반대 의견: bastawhiz: "this engineer has amnesia and forgets everything it's learned after every task." (그래서 onboarding 문서처럼) vs sroussey: "sounds like that directory should have a readme." ↔ stingraycharles: "READMEs are written for people, CLAUDE.mds are written for coding assistants."

### H2. 규칙은 LLM이 아니라 도구에
- HumanLayer: "Never send an LLM to do a linter's job." / "always use deterministic tools whenever you can" / HN _pdp_: 린터·유닛테스트로 차단 / brianwawok: "No matter how many times I told it, it lints randomly."
- 추천 반응: HN 46098838·48160604 다수 동조. 코스의 CLAUDE.md→hooks 분업과 동일.

### H3. 테스트 보호
- 테스트 파일을 "계약"으로 선언(horadecodar 가이드) / #319 @skerit 프롬프트 규칙 / DoltHub: "be very wary of changes to your test files" / __mharrison__(HN 46292682): "I use tests as guardrails to keep the AI from doing something silly" / 코스 play 10의 "stop the agent editing test files" 훅과 결합
- 결과 위조 대응: 테스트는 **에이전트가 아니라 CI가 실행**하고 결과를 읽게 한다(ijk: 평가 지표와 최적화 지표 분리)

### H4. 서브에이전트 비용 통제
- Reddit 댓글: 글로벌 CLAUDE.md에 "tool call 5개 미만은 인라인" 규칙 / avinoth: "not use subagents unless explicitly requested" / HN: 서브에이전트에 작은 모델 / 공식 문서: 팀 전에 subagent, subagent 전에 단일 세션 검토; 3~5 teammates 시작, 같은 파일 편집 금지 / `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=0`으로 의도치 않은 팀 생성 차단(공식)

### H5. PR 리뷰 운영
- PR 크기 공격(u/lonestar-rasbryjamco 205p), "You PR it, you own it", 티어드 리뷰(핵심 경로 deep / 루틴 light), AI 생성 PR 라벨·봇 정책(GeekNews 25625), 결정 로그를 PR 전에(GeekNews 27700), 작성 모델 ≠ 리뷰 모델(@bungker·@aer0700), 커밋마다 재리뷰 금지(`synchronize` 제거), 심각도 상한·스타일 코멘트 opt-in, 리뷰어가 직접 고치기(eieio: "if a reviewer changed your code, you reviewed their change." ↔ PurelyApplied: 학습 기회 상실 우려)

### H6. hooks 운영
- 강제 경계는 deny(`exit 2` 또는 JSON deny), `ask`는 편의 레이어(BGMLAI) / 차단 시 이유를 stderr·reason에 — 단 reason 미표시 버그 보고 있음(#17491) / 디버깅: 수동 실행 `echo $?` → `claude --debug` → 세션 재시작 / Windows·VS Code 확장은 별도 검증 / 팀 공유는 `.claude/settings.json` 커밋(코스와 동일)

### H7. headless 운영
- `permission_denials` 배열을 직접 검사해 빌드 실패 처리 / 허용목록(`allowedTools`) 우선, bypass는 격리 컨테이너+`--max-turns`+JSON / root 금지 / 결과 파싱 전 `is_error`만 믿지 말 것

### H8. plan mode 선택 기준
- "3파일 이상 / 리팩터·스키마·보안 / 한 문장으로 설명 안 되면 plan, 한 줄 수정은 skip" (claudelog·mejba·openreplay 블로그 다수 수렴) [블로그 합의, 데이터 아님]

### H9. 비용 감각(인용 가능한 숫자, 모두 검증 필요)
- 작업당 $0.5~0.75(2025-04 HN 댓글, 구버전) / DoltHub 2일 $100 / Cloudflare 리뷰당 ~$0.90(krzyk) / Anthropic Code Review $15–25·~20분(공식) / 한국 brunch: Pro $20로는 멀티에이전트 테스트 부족, Max $100 권장, "$100을 넘긴 적은 없다"

---

## 3. 논쟁점

### A. spec-driven development는 워터폴의 귀환인가  — play 1·2
- HN "Spec-Driven Development: The Waterfall Strikes Back" (marmelab, 225p/191c, 2025-11-15, https://news.ycombinator.com/item?id=45935763)
  - 워터폴이다 — constantcrying: "I did professional waterfall development and SDD is exactly waterfall." / cushychicken: "the spec has calcified into something immutable in stakeholders' minds." / wiseowise(냉소): "Documentation gets out of date quickly!!!"
  - 아니다 — Fargren: "Waterfall means only one iteration." / canterburry: "I don't see how using a spec has made me less agile." (8시간 이터레이션) / podgorniy: "There is a spec, but there is no waterfall required to work and maintain it." / Allstacks(블로그): 피드백 루프가 "six months to twenty minutes"로 줄었다
  - 제3 관점 — jillesvangurp: "What we do when we create software is creating a specification in source code form." / laserlight: "we don't even understand our problem well, let alone understanding a solution to it."
- 다른 HN 스레드: "Verified Spec-Driven Development" (211p/118c, 2026-02-28), Martin Fowler "Understanding SDD: Kiro, Spec-Kit, Tessl" (128p/32c, 2025-10-16), "Ask HN: Are you using Spec Driven Development?" (7p/6c, 2026-06-12)
- 한국: GeekNews 26148 댓글 @jjw9512151·@goodnvin·@cosine20 — 명세 유지 자동화(훅·스킬)로 "rot" 반론

### B. AI 시대에 코드 리뷰는 무엇을 봐야 하나  — play 9
- 관점 1(기능·의도만): Quarrelsome: "A good code reviewer knows how to just drop all the things that irk them." / daotoad: "most naming comments are just bike shedding." / SkyPL: 전부 보지 말고 아키텍처 제약·테스트를 절차적으로 보장
- 관점 2(사람 리뷰는 대체 불가·교육 기능): proofofcontempt / sailfast(HN 46302267): "All of the learning that happens during PR review is at risk in this way" / PurelyApplied
- 관점 3(작성자=리뷰어 가능, 다른 모델로): Greptile "Should the author be the reviewer?" (136p/84c, 2025-05-01) ↔ GeekNews 20800 HN 요약: "엔지니어들은 AI가 생성한 코드를 자신이 작성한 코드만큼 꼼꼼하게 검토하지 않음" / "결국 PR을 올린 저자가 자기 코드의 영향과 결과에 대한 책임을 져야 함"
- 한국: @tomskang "flow·대안·왜 lock 파일이 바뀌는지를 먼저 말하라" — 리뷰의 단위를 코드에서 **결정**으로 옮기자는 주장

### C. 주니어 개발자 성장 경로
- HN "AWS CEO says replacing junior devs with AI is 'one of the dumbest ideas'" (1,073p/532c, 2025-12-17, https://news.ycombinator.com/item?id=46302267)
  - 우려 — beAbU: "a machine that short circuits the process of getting stuck in obtuse documentation is actually harmful long term" / sailfast(위) / jorvi: "no one wanted to bear the 'burden' of training juniors to be seniors." / throwaway894345: 주니어는 "the only pipeline for getting senior devs"
  - 낙관 — marcosdumay: "AI enable juniors to add more value more quickly. That makes them more valuable, not less." / simonw(Kent Beck 인용): "The juniors working this way compress their ramp dramatically."
  - 구조 원인 — citizenpaul: "senior management soured on hiring juniors even a few years before AI" / TheGRS: "'replacing juniors with AI' is just the industry's way of clumsily saving face."
- 2차: Stanford Digital Economy Lab 인용 "entry-level tech postings down 67% (2023→2024)"(Substack 경유), LeadDev 2025: 54%가 주니어 채용 감소 예상 — **fact-checker 대조 필요**
- 한국: GeekNews 바이브 코딩 스레드 댓글 — "AI가 기초 작업을 대신하면서 학생들이 직접 코드를 쓰며 배우는 과정을 건너뛰게 된다"(검색 요약, 원댓글 미확인) / @cshj55 "아 늙기 실타"

### D. 토큰 비용 vs 생산성  — play 3·6·8·9
- 비용 쪽: HN 48883275(33k 토큰 선지출, 706p), 서브에이전트(P4), Code Review $15–25, "Claude Code's Token Tax"(webpronews) / lanthissa "400k in annual burn for zero value"
- 생산성 쪽: plmpsu "ROI here is so high" / Allstacks "feedback loop ... twenty minutes" / 공식: "For research, review, and new feature work, the extra tokens are usually worthwhile. For routine tasks, a single session is more cost-effective."
- 중간: 작업 크기에 프로세스 오버헤드를 맞추라(KDnuggets·mejba) — 코스의 "pick your first play" 모듈성과 공명

### E. vibe coding vs engineering  — play 1·7
- Replit 사고(P10), GeekNews "바이브 코드는 레거시 코드임"(P11), "2년간의 vibecoding을 끝내고"(P11), r/ExperiencedDevs "shame and pride"(P5)
- 반론(도구론): @sinbumu 주판 비유 / @kgun9 자동차 비유 / @tensun "vibeagile" / @zkj9404 "AI를 버리고 개발을 하겠다는건 조금씩 뒤처지는거"
- 중간(spilist2): "'딸깍'과는 거리가 멀고, 수준을 높이려면 엔지니어가 많이 노력해야"
- 분기점: 비전문가·프로토타입 OK vs 핵심 시스템 NO (Lemkin 본인의 사후 권고와 동일)

### F. CLAUDE.md를 계속 손보는 것이 가치 있나  — play 4
- HN "I am morally opposed to updating my Claude.md" (29p/28c, 2026-08-20, https://news.ycombinator.com/item?id=49376287) — 농반진반 글. Arainach(요약): 옛 모델용 지시가 새 모델 성능을 깎는데 어느 줄이 문제인지 모른다
  - 찬성(유지) — err4nt: "they're just the things I keep finding myself repeating." / groby_b: "to make sure the code produced measures up to my standards."
  - 반대 — Swizec: "We are talking about a thing that's consumed all human knowledge whose superpowers are summarization and understanding." / JasonSage: "we're altering every version of the model+harness we use henceforth." / electric_mayhem: "Claude cheerfully ignores the content of your CLAUDE.md"
- 코스의 반론 재료: CLAUDE.md 변경을 **evals로 회귀 테스트**(play 8)하면 "어느 줄이 문제인지 모른다"가 해소된다 — 커뮤니티 도구 Mdarena "Benchmark your Claude.md against your own PRs"(HN 22p, 2026-04-05)가 같은 방향

### G. 사고 책임은 누구에게 — 도구·사용자·조직  — play 10·11
- P10 HN 댓글 3분파: 사용자(asadm·ZephyrBlu) / 도구(miningape·queenkjuul: "an agent understanding the constraints of its environment would be one of the primary things") / 경영(WheelsAtLarge: "Management is to blame on this.")
- Ghostty: 책임은 "human-in-the-loop"에 / GeekNews 20800: "승인자와 머지한 사람이 책임"

---

## 4. 공식 채널에서 확인된 것 (Discord·Discussions 대체)

- Anthropic Discord 및 GitHub Discussions는 접근 불가(403/404). 대신 **GitHub Issues의 Anthropic 직원 응답**을 추적한 결과:
  - 서면 응답 확인: **bcherny(#77212, 2026-08)** — hook `ask`는 bypass 모드에서도 CLI가 프롬프트한다, VS Code 확장이 원인일 수 있음, 2.1.233에서 재현 안 됨
  - 라벨만(응답 없음): #319(ashwin-ant `bug`, bcherny `area:model`)
  - 응답 없음·봇 종료: #17530, #34763, #44246, #7074 등 CLAUDE.md·테스트 조작 계열 전부
  - 현장 해석: "CLAUDE.md 무시"는 모델 문제(`area:model`)로 분류되어 CLI 팀이 답하지 않는다는 체감 → 책에서는 "CLAUDE.md는 확률적, hooks는 결정적"을 공식 설계 의도로 제시 가능(코스도 그렇게 말한다)
- 공식 문서 인용(2026-10-19): agent-teams 페이지의 비용 문구(P4), "Spawning teammates also requires an interactive session. In non-interactive mode with the -p flag ... Claude doesn't spawn teammates" → **headless CI에서 팀 기반 play는 성립하지 않는다**(play 11 설계 시 주의)
- 자주 묻는 질문(커뮤니티 집계): hooks 종료코드 의미(0/1/2/JSON), `ask` vs `deny`, 훅이 캐시되는가(재시작), Windows 지원, skills가 언제 로드되는가, 서브에이전트 모델 지정(`CLAUDE_CODE_SUBAGENT_MODEL`), 팀 자동 생성 끄기

---

## 5. 수집 한계

- **미접근**: reddit.com 직접(차단 — 미러 스냅샷 사용, 댓글 일부만 캡처), Anthropic Discord, GitHub Discussions(403), X/Mastodon 스레드(검색 결과 없음), 커리어리·OKKY(site: 검색 무효·페이지 미렌더), velog 1건만
- **언어 편중**: 영어 HN·GitHub가 양·질 모두 우세. 한국 1차 소스는 GeekNews 댓글 7개 스레드 + 인프런 Q&A + 위키독스/브런치 개인 글. **한국 조직의 망분리·결재·보안팀 마찰에 대한 개발자 1차 후기는 못 찾았다** — 정책 보도만 확보. 책에서 이 부분은 "현장 목소리"가 아니라 "정책 배경 + 인프런 Q&A 수준의 조심스러운 실무 팁"으로 써야 한다.
- **버전 민감**: hooks 동작(#77212·#80039·#55334 상충), CLAUDE.md 주입 빈도(@Gunther-Schulz 주장), 7x 토큰 수치는 모두 fact-checker가 현재 문서·버전과 대조 필요. 2024~2025 초 글(#319, Greptile 2024-12, GeekNews 2025-04)은 구버전 표기.
- **익명·벤더 편향**: Faros·LinearB·CodeRabbit 계열 수치는 2차 인용이며 마케팅 인접. 포럼(tianpan.co) 글은 작성자 불명. 책 본문 수치로 쓰지 말고 "업계가 이렇게 말한다" 수준으로.
- **plan mode·metrics**: 명시적 커뮤니티 토론이 얇다. 오프닝은 P12·P14처럼 "불만이 아니라 행동(건너뜀·미측정)으로 드러난다"는 각도로.
