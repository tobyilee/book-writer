# 웹 리서치: AI 코딩 에이전트 신뢰 곡선 (Claude Code + Codex, Java/Spring + React/Next.js)

- 검색 시점: **2026-10-10**
- 장르: tech-book · 슬러그: agentic-dev-trust-curve
- 수집 원칙: 버전·수치·API는 공식 1차 소스(릴리스 노트·공식 문서·GitHub 저장소·npm/Maven 레지스트리) 우선. 2차 소스(블로그·기사)는 신뢰성 등급을 적고, 교차 확인 안 된 수치는 "미확인"으로 표시.
- 인용 표기: 영어 원문은 번역하지 않고 그대로 둔다(fact-checker 대조용). 한국어 자료는 원문 그대로.

---

## 0. 버전 기준표 (2026-10-10 조회)

책에서 버전을 언급할 때 아래 값을 "{버전}/2026-10 기준"으로 못 박는다. 레지스트리 직접 조회값은 최상 등급, 문서 페이지 표기값은 최상, 2차 소스는 중.

| 도구 | 최신 버전 | 조회 방법 | 비고 |
|---|---|---|---|
| Claude Code (`@anthropic-ai/claude-code`) | 2.1.296 | npm view, CHANGELOG.md(GitHub anthropics/claude-code) | 거의 매일 릴리스. 책에선 "2.1.x/2026-10 기준" 권장 |
| Codex CLI (`@openai/codex`) | 0.162.1 (rust-v0.162.1, 2026-10-09) | npm view, GitHub openai/codex releases | 0.163.0-alpha.5까지 공개(2026-10-10) |
| Codex 모델 | `gpt-6.1-sol`(2026-09-29), `gpt-6-astra`, `gpt-6-luna`, `gpt-6-sol`(2026-09-22) | learn.chatgpt.com/docs/models, changelog | **`gpt-5.5`는 2026-10-14 Codex에서 은퇴.** 사용자 프롬프트의 "GPT-5-Codex"는 구명칭(2025) |
| pstack (Cursor 플러그인) | 0.15.15 | github.com/cursor/plugins/pstack/.cursor-plugin/plugin.json | 2026-10-06 커밋 기준 |
| gstack (Garry Tan) | 릴리스 태그 없음 · ★135,748 | gh repo view garrytan/gstack | 2026-03-11 생성, 2026-10-09 push |
| Next.js | 16.4.0 | npm view | Next.js 16 메이저는 2025-10-21 |
| React / react-dom | 19.3.0 | npm view | React 19.2는 2025-10-01 |
| eslint-plugin-react-hooks | 7.1.1 | npm view | v6(2025-10)부터 flat config 기본 + 컴파일러 룰 |
| TypeScript | 7.0.2 | npm view | |
| ESLint | 10.12.0 | npm view | |
| Storybook | 10.6.1 | npm view | |
| `@playwright/mcp` | 0.0.83 | npm view | |
| `chrome-devtools-mcp` | 1.10.1 | npm view | |
| eslint-plugin-boundaries | 7.2.0 | npm view | |
| dependency-cruiser | 18.5.0 | npm view | |
| knip | 6.41.0 | npm view | |
| promptfoo | 0.124.1 | npm view | |
| danger (JS) | 14.0.7 | npm view | |
| Spring Boot | 4.1.1 (docs "Stable"), 4.1.0은 2026-06-10 GA | docs.spring.io 버전 선택기, spring.io 블로그 | 4.0.0 GA 2025-11-20. 3.5 OSS 지원 2026-06 종료(InfoQ, 중) |
| Spring Framework | 7.0.x (7.0 GA 2025-11-13) | spring.io 블로그 | |
| Spring Modulith | 2.1.1 (Stable), 2.2.0-M2 (Preview) | docs.spring.io/spring-modulith | 2.0 GA 2025-11-21 |
| ArchUnit | 1.5.1 (9/25), 1.5.0 (8/4, JUnit 6 지원) | GitHub TNG/ArchUnit releases | 릴리스 페이지에 연도 미표기(JUnit 6 지원으로 보아 2026 추정 — 미확인) |
| Java | 25 LTS (2025-09-16 GA) | InfoQ/Azul (중) | 다음 LTS는 27(2027-09 예정) |
| Error Prone | 2.50.0 (2026-06-10) | Maven Central 검색 API (중 — 인덱스 지연 의심, 아래 수집 한계 참조) | |

> **Maven Central 검색 API 주의:** `search.maven.org` 인덱스가 Spring Boot 최신을 3.5.3(2025-06)으로 돌려줘 명백히 낡아 있었다. Testcontainers·jqwik·NullAway·Checkstyle·Spotless·springdoc·REST Docs의 정확한 최신 버전은 **미확인**으로 남긴다(책에서 버전 명시 필요 시 fact-checker가 각 프로젝트 GitHub releases로 재확인).

---

## A. 1차 소스(사용자 지정) 핵심 주장 — 타임스탬프 원장

### A-0. 소스 자체에 대한 발견 (책 구성에 영향)

1. **두 영상은 같은 워크숍이다.** `2v40N037oJU`("How One AI Agent Manages 20+ GrokBot Agents", Get into AI, 2026-10-09 업로드)의 자막은 앞 약 54초의 짧은 인트로(Grok Bot 소개·"agents fix bugs while I sleep")만 다르고, `[00:00:54]`부터 `EWSUvEyFwjc`(Vision Sabbat, 2026-09-15)와 동일한 발화가 이어진다(끝까지 동일, 타임스탬프만 약 +1~2분 밀림). 영상 설명의 "/loop·/goal·Chief of Staff 에이전트로 20+ GrokBot 조율" 내용은 **자막 어디에도 없다.** 그 설명은 Grok Bot 제품 마케팅(VentureBeat: "Internally, a Chief of Staff Bot sits above specialist Bots")에서 가져온 것으로 보인다. → 책에서는 **첫 영상 하나만 1차 소스로 인용**하고, 두 번째는 재업로드로 처리한다.
2. **워크숍 녹화일은 2026-08-12(수)로 추정된다**(업로드 2026-09-15가 아님). 근거: (a) `[00:32:11]` "Grockbot … we just launched yesterday" — Grok Bot 베타 공개 2026-08-11(VentureBeat); (b) `[00:50:47]` "we actually announced Grock 4.6 today" — x.ai Grok 4.6 발표 2026-08-12; (c) `[00:05:06]` "this month we're only on the 12th". 따라서 "지난달 1,000 PR" = **2026년 7월**, "이번 달 12일 기준 ~800 PR" = **2026-08-01~12**.
3. **Lauren Tan의 소속**: 본인 발화 `[00:47:57]` "I work at a AI lab where we have unlimited tokens", `[00:51:18]` "cursor and SpaceX AI try to really optimize". GitHub 프로필(@poteto) bio: "Software Engineer @xai-org & @react compiler core team". pstack README(본인 작성): "i've worked with millions of lines of code at Meta, Netflix, and Cursor. i'm also on the react core team where i help build and maintain react compiler." Cursor는 2026-08-14부로 SpaceX에 인수 완료(Cursor 공식 블로그). → 정리 문서의 "Cursor 엔지니어, 前 Meta"는 맞지만 불완전. 책에서는 **"Cursor(2026-08 SpaceX/SpaceXAI에 인수) 소속 엔지니어, React Compiler 코어팀, 前 Meta·Netflix"**로 쓰는 것이 정확하다. "SpaceXAI 엔지니어"(채널 제목)도 틀리지 않다.
4. **고유명사 정식 표기**: 제품명은 **"Grok Bot"**(x.ai/bot, 두 단어). 플러그인은 **pstack**(소문자, "potato stack" — `[00:13:37]`~`[00:13:52]`에서 본인 확인). 아키텍처 코드명 **Dune**은 공개 문서 없음. 검증 스킬 **control-glass**는 pstack에 포함되지 않음(아래 B-2 참조).

### A-1. 핵심 주장 원문 (EWSUvEyFwjc 기준 타임스탬프)

| 시각 | 주장 | 원문 인용 (자동 자막, 철자 보정 없음) |
|---|---|---|
| 00:00:00 | AI는 페어 프로그래머, 생각을 외주화하지 말라 | "the best use of you of AI is really as like a like a pair like someone you're pair programming with and not someone as not not a not a tool to just replace the act of writing code or worse outsourcing your thinking." |
| 00:00:44 | 리뷰·수정 시간이 더 든다 | "although when I use AI I save some time you know writing the code I actually find myself spending more time reviewing what the AI did and like correcting it." |
| 00:01:24 | 큰 주제 = 신뢰 | "the big theme for me as I've been using agents to write code … is how do you trust it?" |
| 00:01:52 | 백 번째 확신에 찬 오답 | "confidently stating that they found the smoking gun, uh, for the hundth time, uh, but it's actually not the real problem. You lose a lot of trust." |
| 00:02:04 | 매니저 비유(마이크로매니지먼트) | "if I'm an a manager … and I don't trust them then the mode of operation I'm going to be in is going to be like micromanagement" |
| 00:02:33 | 비과학적 차트 | "I drew this chart because uh it's It's not it's not a very scientific chart but like this is how I imagine myself and my journey" |
| 00:03:21 | 1개도 못 믿으면 100개 불가 | "you can't go to a 100 agents uh like spawn 100 agents when you don't even trust the output of one agent" |
| 00:03:36 | 5개월간 곡선을 오름 | "over the past 5 months I feel like I've really been able to uh like ascend this trust curve" |
| 00:03:52 | 자동 머지 + 20 PR | "I actually have my agents now um autoemerging PRs for me. … I woke up today and there were like 20 PRs landed and I just reviewed them on main like they were already landed and they were good." |
| 00:04:53 | 입사 5개월, 첫 달 비생산 | "I joined five months ago … my first month I was like not very productive" |
| 00:05:06 | 월 1,000 PR / 12일 ~800 | "last month I shipped a thousand PRs which is ridiculous. Uh, and then this month we're only on the 12th. I'm already at like almost 800 PRs landed." |
| 00:05:53 | 가장 중요한 스킬 = 검증 | "the most important skill that you should have in your toolbox when you work with agents is verification." |
| 00:06:10 | 검증의 정의 | "the ability for an agent to actually run the code uh or take CPU traces or heap snapshots or uh you know open an iOS simulator whatever you know however your application is exposed to your users. It can do the same thing" |
| 00:06:29 | 맞는 코드 vs 좋은 코드 | "it doesn't guarantee your agent writes good code uh but it allows them to at least write correct code uh which is a big a really big step forward for being able to trust your agents." |
| 00:08:48 | 사람이 검증자면 병목 | "development with an agent where you don't have a verification skill you are the verifier right you you're the bottleneck" |
| 00:09:13 | 병렬화 불가 | "you're constantly just in the loop and and being a bottleneck. So there's really no way to parallelize." |
| 00:09:26 | control-glass 스킬, Glass = Agents Window 코드명 | "the control glass skill is like one of the first skills I built uh for cursor. Uh and glass by the way is the code name for agents window" |
| 00:09:43 | CDP / iOS 시뮬레이터 | "you can teach your agent how to use like the Chrome DevTools protocol or through uh Apple has some utilities as well for running the simulator" |
| 00:10:17 | Feature Map | "this skill comes with this very unique feature called or not feature uh unique file called a feature map." |
| 00:11:33 | pstack의 create verification 스킬 | "in PAC, the plugin that I I've made, uh, if you search for PAC cursor on Google, you you'll find it. Uh, but there is a create verification skill in that plugin" (PAC = pstack 오인식) |
| 00:12:31 | "???" 수준 버그 리포트 | "someone just says question mark question mark question mark like what is this?" |
| 00:12:56 | Feature Map 내용 | "from the user point of view here's where to how do I get to it all the different keyboard shortcuts uh even like … the attributes that you use for selecting things through the CDP uh are all there." |
| 00:13:10 | maintain-verification 스킬 | "piece stack ships uh that create verification skill but also a maintain verification skill uh so you can keep this up to date." |
| 00:13:37–13:52 | pstack = potato stack, gstack 패러디 | "the P the P in P stack is like potato potato stack … Gary Tan who is the CEO of Y Combinator and he's come up with this plugin called GStack uh Gary Stack and uh funnily enough we share the last name. We have no relations." |
| 00:14:11 | 설계 의도 없음, 점진 축적 | "I honestly actually never set out to build PAC. Uh, it just started with a bunch of skills" |
| 00:14:27 | how 스킬의 유래 | "another skill like called how which I also noticed through like observing agents" |
| 00:15:07 | 툴 콜을 열어보니 코드를 안 읽음 | "when I looked at the actual tool calls, I noticed it wasn't actually reading the code that I thought should be affected. And that made me just extremely suspicious." |
| 00:15:33 | 5초 전 입사한 엔지니어 | "an engineer on your team who was a really good coder, no business context whatsoever … they onboarded you know like 5 seconds ago. Uh and so how do you actually teach that person to be effective?" |
| 00:16:01 | 스킬 = 마크다운, latent space | "skill being just you know it's just markdown right … some people on Twitter call it like you know pull the agent to a different latent space" |
| 00:16:47 | 실패 관찰 → 스킬 | "every time I saw that I just okay I'm just going to make that a skill right like stop hallucinating actually go and search up look up the code use a lot of sub agents uh and yeah stop guessing" |
| 00:17:35 | eval = 에이전트 단위 테스트 | "an eval is essentially like a way to uh well I think the mental model I have is like it's like a unit test for an agent." |
| 00:17:52 | 프레임워크 불필요 | "You don't need like a special framework for them." |
| 00:18:28 | Eval Playbook | "in Pstack, we ship uh under potato mode there's a playbook if you search for it called eval playbook." |
| 00:18:46 | 코디네이터 + 루브릭 + 서브에이전트 | "I spawn a lot of different sub agents. I have like my main coordinator agent uh come up with a rubric for uh what I want the skill to do." |
| 00:19:03 | 평가 중임을 숨긴 디렉터리명 | "it creates individual directories for them uh which are cleverly named to not let the sub agent know that it's being evaluated because uh agents can actually tell and when they do they change their behavior." |
| 00:19:37 | 모델 매트릭스 | "you can actually eval your skill across all sorts of different models." |
| 00:19:52 | 스킬 수정마다 eval | "Every time I I modify a skill, I will run one of these uh like the Ebal playbook" |
| 00:20:08 | 유지보수는 어렵다, taste | "maintaining skills is actually pretty hard. Uh it requires I think a lot of taste and observation. So you kind of need to be very good at being a backseat driver." |
| 00:20:46 | 툴 콜·thinking 블록을 읽어라 | "opening up the all the tool calls and like reading the code and reading all the to uh the agent behavior and their thinking blocks is a really great way to see where they they fail" |
| 00:21:15 | 검증자를 검증 | "I actually did the same process for verifying the verification skill" |
| 00:21:30 | 다른 모델 judge로 편향 교차검증 | "you can have a judge agent of a different model to uh kind of cross reference and make sure that the first model is not being biased" |
| 00:21:46 | /loop로 hill-climb | "you can use like /loop in cursor and you can say okay keep looping on this eval right until everything is 10 out of 10" |
| 00:22:48 | 헤드 셰프 비유 | "you're like a a chef in a restaurant. uh you know, you're the head chef. Uh you're not cooking all the food yourself anymore. … it's your job to really design the environment." |
| 00:23:52 | 로컬에서 시작 | "the best place to start is local because you can observe" |
| 00:24:34 | 클라우드 에이전트 올인 | "I have basically been kind of all in mostly all in on cloud agents because they're extremely powerful." |
| 00:25:02 | 팀·회사 전체 이득 | "It actually levels up your whole team uh and even your whole company" |
| 00:25:16 | Benny | "this agent we have called Benny, right? who who uh you know takes all of the bug reports that we get and it automatically goes off in the cloud … It runs cursor in its own computer and it uses the same control skills to interact with the application and try to reproduce the bug" |
| 00:25:46 | "이미 main에서 고쳐짐" | "the Benny actually reproduced the bug uh but it's already fixed on main." |
| 00:26:41 | 점프 금지 | "you don't want to jump to like I'm going to spawn hundred of thous or thousands of cloud agents right now because you're just going to waste a lot of tokens." |
| 00:27:06–27:38 | 호스트의 4단계 요약 | "start with verification … once we trust it locally, then we can start to think about scaling into the cloud … And then maybe the last step is like automerging the PRs … and then reviewing the one main" |
| 00:28:01 | 지름길 없음 | "there's really no shortcut for going from here to there because this is really about your personal level of trust in agents" |
| 00:28:30 | 나를 맹신하지 말라, 포크하라 | "I definitely would not encourage people to blindly trust me … take a look at PAC and kind of fork it make it your own" |
| 00:29:27 | 3번째 축: 리라이트 | "there's a third part to this … refactoring and rewriting." |
| 00:30:34 | 빅테크 문제 = 모두의 문제 | "a lot of big tech company problems are now everybody's problems." |
| 00:31:01 | human slop | "I often joke that like, you know, before AI slop, we had human slop." |
| 00:31:15 | 가장 못하는 엔지니어 기준 설계 | "you're catering to the … the least capable engineer on your team right you build you build frameworks you build conventions you build guard rails you know you restrict credentials so that you know your intern doesn't wipe your production database" |
| 00:31:58 | 그린필드 최대 리스크 | "green field applications especially are … the biggest risk in my opinion. Uh and also the greatest opportunity" |
| 00:32:11 | Grok Bot 전날 출시 | "Grockbot was spun up very very very quickly. … it's like our a new application we just launched yesterday." |
| 00:32:52 | organic architecture 트윗 | "I had this tweet recently uh where I said something about organic architecture." |
| 00:33:10 | 가장 편한 방법으로 해결 | "when you give them a task, they will just solve it in whatever method is the most convenient. And over time you get into this uh situation where you have a codebase that is spiraling out of control" |
| 00:33:40 | 강한 제약으로 시작 | "starting your codebase with uh like very strong constraints is very much needed" |
| 00:34:12 | 600+ PR 리팩터링 | "over 600 PRs I I I calculated yesterday uh when I refactored all of Grockbot to this new architecture" |
| 00:34:28 | 코드를 거의 안 봄 | "I've gotten to a point where I I don't really look I really don't look at the code anymore. … I spent a lot of tokens to get the codebase to this point" |
| 00:34:54 | PM·디자이너·GTM 기여 | "it also empowers you know designers and product managers and you know pe uh even GTM people to add features to Grockbot" |
| 00:35:06 | 에이전트가 귀찮음을 흡수 | "I have a ton of constraints and CI like it's actually very annoying to write code in in graph web but like agents absorb all of that annoyance" |
| 00:36:06 | Pretext 가상화 라이브러리 | "virtualization in grockbot and in uh cursor is actually powered by uh Pretext uh which is a sort of new library" (웹 미확인) |
| 00:36:22–36:57 | PR 크기 50~1,000, 하드 캡 없음 | "they can range anywhere from a few hundred lines or 50 lines to like a thousand … There's no hard cap." |
| 00:37:13 | git history = 컨텍스트 | "the git history is a very rich source of context. Uh, and I like the I like each PR to sort of atomically describe what that small piece of thing is doing" |
| 00:37:27 | 40,000줄 PR | "It's not in this 40,000 line PR where you who knows what landed in there." |
| 00:37:52 | Dune = 코드명 | "Dune is the is the sort of cheeky code code name for the architecture that we've built for Grockbot." |
| 00:38:09–38:24 | useEffect 금지 | "one of the biggest foot guns in react is use effect. Uh so in uh Dune and in graphbot we've banned use effect." |
| 00:38:24 | Dune = Electron용 Next.js | "you can kind of think of it as like Nex.js JS for uh electron apps and it's designed for agents to write" |
| 00:38:54 | 코드 주석 금지 | "I actually ban code comments as well … 99% of the time agents just write code comments that kind of describe some historical thing that is actually totally irrelevant to the code." |
| 00:39:09 | "Lauren said you should never do this" | "it will often say like, you know, oh, Lauren said you should never do this and it's now in in a code comment. … I just meant like your this PR sucks and you should change that part." |
| 00:39:34 | 못하는 건 전부 금지 | "we just ban everything everything you can imagine like the agents are bad at we ban." |
| 00:40:14 | 프로세스 격리 부실 | "we have very poor um isolation between processes. So like on you know on on Electron you have a renderer thread … but you also have like a main thread" |
| 00:40:43 | 16ms 프레임 예산 | "if you want like 60 fps you have to every frame that gets drawn has to be done in 16 milliseconds." |
| 00:41:37 | 임포트 경계 CI | "we literally have a directory called electron main electron renderer and we have a import uh CI guess where we actually check the dependency graph to make sure you're not accidentally importing code from one directory to another." |
| 00:41:54 | Bugbot, agents MD | "as well as bug bots uh which is our which cursors um like code review tool that runs on CI uh you know in our agents MD it's everywhere" |
| 00:42:13–42:27 | 아키텍처 = 최강 집행 | "if you have an architecture like this where it's extremely strict … that's like the strongest strongest level of enforcement because agents just love to copy existing patterns." |
| 00:42:41 | Dune의 명사: feature, entry points, transcript cards | "we have this these concepts called like a feature and we have entry points and transcript cards … these are all like like nouns I guess in in the framework" |
| 00:42:55 | 기능 = 디렉터리 하나 | "a feature is all in in a single directory as an example and so all of the code that contributes to that feature lives in one directory so it's all collocated" |
| 00:43:07 | 80% 캡슐화 | "for 80% of the work, it's mostly just very encapsulated there." |
| 00:43:20 | 가장 멍청한 에이전트용 | "it's like designed again for you know like the dumbest agent like you don't have to think" |
| 00:43:34 | shortest path = best path | "one of the key principles I have for this framework is like the shortest the shortest path is the best path. … they like to take shortcuts … So why not make that the best way to solve the problem?" |
| 00:44:03 | 오픈소스 안 함 | "this framework is really more of a collection of ideas and principles rather than something that will open source. Uh you can you can you know screenshot this I guess if you want and uh tell your agent to uh do some build build something like this for you too." |
| 00:44:32–44:50 | 레이어: 하드 vs 소프트 | "there's CI checks, we have a lot of lints for bad patterns that we observe. uh compiler diagnostics uh there's also rules and bugbot which are um I think like three four five are more soft right these two actually make make CI red" |
| 00:45:07 | 소프트만 있으면 쓰레기 | "if you only have rules and bug bar and skills and a style guide for your code, you will it's only a matter of time before your codebase looks like complete trash." |
| 00:45:36 | Rust 컴파일러 | "Rust is sort of making you know it's like getting super popular again. Uh because the compiler is so strict … as long as you make sure your agents don't write unsafe code blocks, uh you can more or less feel somewhat confident that if the code compiles, it's probably works" |
| 00:46:18 | 코드 리뷰 랜드 = 최악 | "the worst place to be in is if you are stuck in code review land where you actually enforce all of the constraints, the invariance in your codebase by literally the human person saying, you know, reading the code and like, okay, you should not do this" |
| 00:46:35 | 코멘트 = code smell | "Every time you have to do that, you should consider that as a code smell, like a anti- pattern and you should say, 'Okay, instead of me commenting on the PR, how do I turn this into a hard rule, right? How do I turn this into a lint rule? How do I turn this into a CI failure? Or how do I even categorically eliminate this problem uh entirely?'" |
| 00:47:12 | 호스트: 로컬 2~3개 단계 | "I'm definitely on like the uh you know, maybe a couple of parallel ones locally stage. So, like two to three locally, and I'm sure most people here are on the same." |
| 00:47:57 | AI 랩, 토큰 무제한 | "obviously you know I work at a AI lab where we have unlimited tokens. So uh I definitely cannot say that you know this is something everyone should do in the exact same way" |
| 00:48:22 | ROI 질문 | "I think to me it's a question of ROI. … yes, you spend a lot of money on tokens in the upfront stage" |
| 00:49:18 | 에이전트의 가치 = 불가능했던 일 | "agents are all about allowing you to do things that you couldn't do before. That's really to me like the value of agents … the thing I couldn't do before is like enforce this level of constraints in a codebase by myself" |
| 00:50:02 | 고용 vs 토큰 | "do you hire someone to do this or do you spend the tokens to set up a code base so that even the the most naive right the dumbest agents can do a good job" |
| 00:50:47–51:18 | Grok 4.6 당일 발표, 단가 | "we actually announced Grock 4.6 today. … I hopefully I'm not saying this incorrectly, but uh I believe the cost per token is the same as 4.5." (**본인도 hedging. x.ai 발표문은 4.5 대비 단가 비교를 명시하지 않음 → 미확인**) |
| 00:51:18 | Cursor와 SpaceX AI | "this is an area that cursor tries to cursor and SpaceX AI try to really optimize for like that heredto frontier of you know cost versus intelligence." |
| 00:53:22 | Grok Bot = 비개발자의 Cursor 모먼트 | "Grockbot is basically like the kusher moment for people who are not in tech in my opinion … It looks like iMessage." |
| 00:54:13 | PM이 고친 버그 → stamp | "they will just say oh here's a bug I fixed it can you look at it and then I'll go review it and actually it's just perfect. I'm like okay stamp." |
| 00:54:26 | Dune이 버티고 있다 | "that shows that you know the the Dune architecture is holding up right the all the the really strict constraints allow people who are not experts in engineering to contribute at a high level." |

### A-2. 정리 문서(trust-curve-page.txt)와 자막 대조에서 발견한 주의점

- 정리 문서의 숫자(5개월·~1,000·~800·20·600+·16ms·50~1,000줄·주석 0)는 모두 자막에서 확인됨. 단 "월 1,000 PR"의 달은 2026-07, "12일 기준 800"은 2026-08-12(A-0 참조).
- "Grok 4.6: 4.5와 동일 단가"는 Lauren 본인이 "I believe … hopefully I'm not saying this incorrectly"로 말함. 책에서는 "Lauren의 발언"으로 한정하고 단정하지 말 것.
- 정리 문서의 "Agents Window … 내부 코드명 Glass"·"Benny"·"Feature Map"·"how 스킬"은 자막과 일치. "Pretext" 라이브러리는 웹에서 미확인.
- 정리 문서 "pstack: … create-verification, maintain-verification, how, Eval Playbook 포함"은 현재 공개 pstack과 일치(B-2). 단 **control-glass는 pstack에 없고** `control-ui`/`control-cli`가 `cursor-team-kit` 플러그인에 있음(pstack README "not shipped here").
- 정리 문서 "신뢰 곡선 4단계"는 호스트(Colin)의 중간 정리 `[00:27:06]`를 Lauren이 "Yeah, exactly"로 승인한 것. Lauren이 직접 단계 번호를 붙인 건 아님 — 책에서 "Lauren이 그린 곡선을 호스트가 4단계로 요약, 본인 동의"로 쓰는 것이 정확.

---

## B. Lauren Tan · pstack · Grok Bot · gstack

### 자료 1: pstack 공식 저장소 (cursor/plugins/pstack)
- 출처: https://github.com/cursor/plugins/tree/main/pstack (README, `.cursor-plugin/plugin.json`, `skills/*/SKILL.md`, `skills/poteto-mode/playbooks/*.md`) — `gh api`로 직접 조회
- 저자·날짜: Lauren Tan(커밋 작성자 "lauren"). **첫 커밋 "Add pstack plugin" 2026-05-23**, 최신 커밋 2026-10-06 ("feat(pstack): drop Sol, default to Opus xhigh and Grok (#511)"). plugin.json `version: 0.15.15`, MIT.
- 신뢰성: 최상
- 핵심 주장: 23개 플레이북 + 24개 원칙 스킬 + 다수 워크플로 스킬. 진입점은 `/poteto-mode`. 모델 역할 분담은 `/setup-pstack`. "fearless parallelism"이 신뢰 곡선 논리와 동일.
- 인용 가능한 구절 (README 원문, 모두 소문자):
  > "i've worked with millions of lines of code at Meta, Netflix, and Cursor. i'm also on the react core team where i help build and maintain react compiler."
  > "there's a growing sense that ai writes too much slop code. i agree. i don't want to ship like a team of twenty slop artists. throughput without quality is not a goal i aspire to. if you want to go fast, go deep first."
  > "**pstack gives you fearless parallelism.** when you can go deep on one agent and trust it to write good, verifiable code, you can truly parallelize with confidence."
  > "out of the box the mode splits work by model strength: code delegates (feature, refactoring, bug fix, perf, hillclimb) go to grok, while the hardest changes, prose, and judgment go to opus 5.5. the default panel is opus 5.5 / grok."
  > "[`/poteto-mode`] works extremely well with cursor's `/loop` command. you can make cursor work for many hours without sacrificing rigor."
  > "why are there no planning skills? cursor already has a great plan mode which works great with pstack. but personally, i don't believe in planning. the best spec is code."
  > "a few things `poteto-mode` references but doesn't bundle: `/deslop` … `control-cli` (for CLIs and TUIs) and `control-ui` (for browser, Electron, web) ship in `cursor-team-kit` too."
  > "pstack also ships a dormant benny automation pack. benny triages slack issue reports, then reproduces and fixes confirmed bugs with real ui evidence."
  - `/correct` 스킬 설명 (집행 레이어 승격의 코드화): "you keep correcting agents for the same mistakes. mines history for mistake classes, fixes each at the highest level that works (architecture, then types, lint, and ci, then tests, with docs last), and keeps a table pairing each rule with what enforces it."
  - 원칙 `encode-lessons-in-structure`: "Encode the rule as a lint, metadata flag, runtime check, or script instead of more text."
  - 원칙 `prove-it-works`: "Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'"
  - 원칙 `test-behavior-not-implementation`: "If the test would still pass when every imported function returns undefined, rewrite the assertion or delete the test."
- 관련 섹션: 2장(검증)·3장(스킬+eval)·4장(아키텍처/집행 레이어)·"pstack을 포크하라" 부록. **주의:** 2차 소스(mindpattern "early September 2026", redreamality "open-sourced in May")가 공개 시점을 다르게 적음 — GitHub 커밋 기준 **2026-05-23이 정전**.

### 자료 2: pstack `create-verification-skill` SKILL.md (Feature Map의 공식 정의)
- 출처: https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md
- 날짜: 2026-10-06 기준 main
- 신뢰성: 최상
- 핵심 주장: 프로젝트 로컬 `verify-<app>` 스킬을 생성 — Launch/Doctor/Drive/Evidence/Cleanup/Helpers 섹션 + `features/README.md` 피처 맵. "A generated skill that was never executed is a draft, not a deliverable."
- 인용:
  > "Every serious project needs a scripted way to drive the real app and prove behavior: launch it, exercise a feature the way a user would, and capture evidence."
  > "**Drive:** how can an agent interact with it programmatically? Existing harnesses first — Playwright/Cypress specs, expect scripts, PTY helpers, curl-able endpoints, a debug port. Only then pick a generic recipe: browser/CDP for web and Electron, a tmux/PTY harness for CLI/TUI, plain HTTP for services."
  > "Each file answers, from the user's point of view: what the feature is, how to reach it, how to drive it with the harness, and what observable end state proves it works. The four H2s are `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`."
  > "State the proof standards: exercise the real user path, not internal setters or test-only endpoints; capture the action and the resulting state, not just the final screen; verify side effects (files written, rows inserted, messages sent) alongside what's visible"
- 관련 섹션: 검증 챕터의 "Feature Map 작성법" — Java/Spring(`plain HTTP for services`)·Next.js(`browser/CDP`)에 그대로 매핑 가능.

### 자료 3: pstack `eval` 플레이북 (블라인드 eval 설계)
- 출처: https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md
- 신뢰성: 최상
- 인용:
  > "No `eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `compare`, `benchmark`, `candidate`, or `arena` in any directory, file, or prompt the candidate sees."
  > "The judge can know it's judging but sees outputs by sanitized label only, never by model name."
  > "Spawn one blinded judge on a different model family"
  > "Verify the chain from transcripts, not self-report. … Grade chain-following from the files it really read plus the shape of the code, never from the candidate's own claims."
  > "Read every candidate output yourself end to end. Compare to the judge's verdict. Disagreement means a model is biased or the rubric is ambiguous."
- 관련 섹션: 스킬+eval 챕터 — 워크숍 `[00:19:03]` "cleverly named" 디렉터리의 구체 규칙.

### 자료 4: poteto/verification-skill-example (Feature Map 예시 저장소)
- 출처: https://github.com/poteto/verification-skill-example — 2026-07-30 push, ★137
- 신뢰성: 최상(본인 공개)
- 인용:
  > "Heavily fictionalized example of a project-local verification skill + behavior-level feature map for a large desktop app. Nothing here is a real product. 'Atlas' / 'Harbor Labs' / `control-atlas` are made up. The shape is what matters."
  > "A wiki is great for humans. Agents pay for every token they reread. A skill + feature map is: Scoped … Actionable … Sweepable … Maintained as code."
  > "This sample is sized like a large app: ~30 feature files across account/chrome, left rail/sessions, prompt/replies, layout, source control, app panes …"
- 관련 섹션: 검증 챕터 — Cursor Agents Window(Glass) 피처 맵의 익명화 버전으로 볼 수 있음.

### 자료 5: Cursor 공식 블로그 "Cursor is now a part of SpaceX"
- 출처: https://cursor.com/blog/joining-spacex — 2026-08-14, Cursor Team
- 신뢰성: 최상
- 인용:
  > "Cursor has officially been acquired by SpaceX."
  > "This completes the acquisition process that started in April."
  > "Grok 4.6, which we released Wednesday, provides an early look at what we can now build together."
- 부가(중, TechCrunch 2026-06-16 / Bloomberg 2026-08-14 / Wikipedia): 2026-04-21 인수 옵션 계약 → 2026-06-16 $60B 전액 주식 인수 행사 → 2026-08-14 완료. xAI는 2026-02 SpaceX에 인수, 2026-07 "SpaceXAI"로 개명.
- 관련 섹션: 서문/저자 소개 — Lauren의 소속 설명.

### 자료 6: VentureBeat — Grok Bot 출시
- 출처: https://venturebeat.com/orchestration/spacexais-grok-bot-turns-agents-into-persistent-digital-coworkers-that-can-operate-your-apps-for-120-per-month — 2026-08-11, Carl Franzen
- 신뢰성: 중(기술 매체)
- 핵심: Grok Bot 베타 2026-08-11. 각 Bot은 자기 클라우드 컴퓨터에서 24/7. 가격: Cursor Premium Teams $120/seat/월, Cursor Ultra $200/월, SuperGrok Heavy($300) 포함. 플랫폼 macOS·Windows·Linux·iOS.
- 인용:
  > "Bots are AI teammates that do real work for you." (SpaceXAI 발표 인용)
  > "Internally, a Chief of Staff Bot sits above specialist Bots (inbox, recruiting, expenses, operations, bug fixes)." (기사 서술)
- 관련 섹션: 클라우드 에이전트 챕터 — Benny 패턴의 제품화. 공식 x.ai/bot 페이지는 403으로 미열람(미확인 항목).

### 자료 7: gstack (garrytan/gstack)
- 출처: https://github.com/garrytan/gstack — 생성 2026-03-11, ★135,748(2026-10-10), MIT. 설명: "Use Garry Tan's exact Claude Code setup: 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA"
- 신뢰성: 최상
- 인용(README):
  > "gstack is how I do it. It turns Claude Code into a virtual engineering team — a CEO who rethinks the product, an eng manager who locks architecture, a designer who catches AI slop, a reviewer who finds production bugs, a QA lead who opens a real browser, a security officer who runs OWASP + STRIDE audits, and a release engineer who ships the PR."
  > "Fork it. Improve it. Make it yours."
  > "gstack runs on more agents than Claude. … `./setup --host auto`      # or: `./setup --host codex`"
  > 설치: "git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup"
- 관련 섹션: pstack 소개 시 패러디 원본 설명. Claude Code·Codex 양쪽 지원 사례.

### 자료 8: redreamality 블로그 — Lauren Tan 후속 발표 정리 (2차)
- 출처: https://redreamality.com/blog/lauren-tan-poteto-trust-before-parallel/ — 2026-10-05, Remy
- 신뢰성: 중(개인 블로그, 그러나 출처 링크 명시)
- 핵심: Lauren의 X 게시물 2026-09-21(https://x.com/poteto/status/2102050467505430555 — 직접 열람 실패, 402)과 "Cursor Compile London → Grok @Bot Galaxy 라이브스트림" 38분 발표를 요약. "last month I shipped 2,500 PRs to production"(X 글 요지), 발표에서는 "약 2,000". Lauren의 공개 프로필: "working on Grok Bot and Cursor at SpaceXAI, while also on the React Compiler core team." Cursor 합류 2026-04, Meta 퇴사 2026-03 중순. "Dune has no public page." 블로그 자체 서술: "it's not an assembly line stamping out copies, and a person is still responsible for what goes out to the table."(Michelin kitchen 비유 — 블로그 표현이지 직접 인용 아님).
- 관련 섹션: 숫자의 시간순 — 7월 ~1,000 → 8월 ~2,500(또는 2,000). 책에서는 "자체 보고"로 한정.

---

## C. Claude Code 공식 문서 (code.claude.com/docs, 2.1.296/2026-10 기준)

### 자료 9: Skills
- 출처: https://code.claude.com/docs/en/skills
- 신뢰성: 최상
- 핵심: `.claude/skills/<name>/SKILL.md`; frontmatter `description`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `effort`, `context: fork`, `agent`, `hooks`. Agent Skills 오픈 표준 준수. 스킬 테스트는 "fresh session"에서 on/off 베이스라인 비교.
- 인용:
  > "Unlike CLAUDE.md content, a skill's body loads only when it's used, so long reference material costs almost nothing until you need it."
  > "Seeing a skill trigger tells you Claude found it, not that it did what you intended. To know a skill is working, measure separately whether Claude invokes it on the prompts it should, and whether the output matches what you expect when it does."
  > "A fresh session matters because leftover context from authoring the skill will mask gaps in the written instructions."
  > "Skills follow the Agent Skills open standard."
  - 버전 노트: v2.1.286부터 "Claude runs `verify` or `simplify` skills before commits"; v2.1.252 `/skill-doctor`.
- 관련 섹션: 스킬 챕터 — Cursor 스킬과 1:1 대응. Codex도 같은 표준(자료 23).

### 자료 10: Subagents
- 출처: https://code.claude.com/docs/en/sub-agents
- 신뢰성: 최상
- 핵심: `.claude/agents/*.md`; frontmatter `tools`, `disallowedTools`, `model`(sonnet/opus/haiku/fable/inherit), `permissionMode`, `isolation: worktree`, `hooks`, `memory`, `background`, `maxTurns`, `skills`. 동시 20개 제한, 깊이 3단.
- 인용:
  > "Set to `worktree` to run the subagent in a temporary git worktree, giving it an isolated copy of the repository branched by default from your default branch rather than the parent session's `HEAD`. The worktree is automatically cleaned up if the subagent makes no changes."
  > "By default, when 20 subagents are running in a session, spawning another with the Agent tool fails with `Concurrent subagent limit reached`."
  > "Each subagent starts with a fresh, isolated context window."
  > "Claude Code ignores a field it doesn't recognize without reporting an error."
- 관련 섹션: eval 코디네이터/judge 구현(서브에이전트 N개 격리) · 병렬 저술.

### 자료 11: Hooks
- 출처: https://code.claude.com/docs/en/hooks
- 신뢰성: 최상
- 핵심: 이벤트 `PreToolUse`·`PostToolUse`·`Stop`·`SubagentStop`·`UserPromptSubmit`·`SessionStart`·`WorktreeCreate`·`TeammateIdle`·`TaskCompleted` 등. 핸들러 5종: `command`, `http`, `mcp_tool`, `prompt`, `agent`(experimental). **exit 2 = 차단**. v2.1.295 `onFailure: "block"`.
- 인용:
  > "Exit with code 2 to block the action. On events that can block, Claude Code stops the action."
  > PreToolUse: "Blocks the tool call" / Stop: "Prevents Claude from stopping, continues the conversation" / PostToolUse: "Shows stderr to Claude; the tool already ran"
  > "Exit 2 blocks even when your hook prints JSON."
  > "If your hook is meant to enforce a policy, use `exit 2`."
  - Stop 예시: `{ "decision": "block", "reason": "Test suite must pass before proceeding" }`
  - CHANGELOG 2.1.295: "Added `onFailure: \"block\"` for command and HTTP hooks: a hook that can't start, times out, or exits with an unexpected code blocks the action instead of letting it through"
- 관련 섹션: 집행 레이어 챕터 — "소프트(CLAUDE.md) vs 하드(hook)"의 Claude Code 버전. 베스트 프랙티스 문서도 "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens."(자료 18)

### 자료 12: Worktrees (`--worktree`, EnterWorktree, isolation)
- 출처: https://code.claude.com/docs/en/worktrees ; CHANGELOG(`--worktree` 2.1.49, `isolation: worktree` 2.1.50, `ExitWorktree` 2.1.72)
- 신뢰성: 최상
- 인용:
  > "Pass `--worktree` or `-w` with a name to create an isolated worktree and start Claude in it. By default, the worktree is created under `.claude/worktrees/<name>/` at your repository root, on a new branch named `worktree-<name>`"
  > "You can also ask Claude to 'work in a worktree' during a session, and it creates one with the `EnterWorktree` tool."
  > "`worktree.baseRef` … `\"fresh\"` (default): branch from the repository's default branch on the remote … `\"head\"`: branch from your current local `HEAD`"
  > "To carry gitignored files such as `.env` into every new worktree automatically, add a `.worktreeinclude` file."
  > 격리 집행 4가지: "File edits … Command working directory … Git redirects … Command shape" — "Claude Code blocks a Bash or Monitor command when it can't verify from the command text that any git the command runs stays inside the worktree."
  > `--worktree "#1234"`로 PR에서 분기.
- 관련 섹션: 병렬화 챕터(로컬 1~3 → N). 사용자 환경이 바로 이 worktree(`.claude/worktrees/trust-curve`)임.

### 자료 13: 비대화형 모드(`claude -p`) 및 Agent SDK
- 출처: https://code.claude.com/docs/en/headless
- 신뢰성: 최상
- 인용:
  > "claude -p \"Find and fix the bug in auth.py\" --allowedTools \"Read,Edit,Bash\""
  > "`--bare` is the recommended mode for scripted and SDK calls, and will become the default for `-p` in a future release."
  > "Without `--bare`, a `-p` session runs the hooks in a project's `.claude/settings.json` and connects the servers in its `.mcp.json`, even in a folder you've never trusted."
  > `--output-format json|stream-json`, `--json-schema`로 구조화 출력; "With `--output-format json`, the response payload includes `total_cost_usd`"
  > CI 린터 예: `"lint:claude": "git diff main | claude -p \"you are a typo linter. …\""`
  > `--permission-prompts none` (v2.1.259+): "Pass `--permission-prompts none` when nobody is available to answer permission prompts"
  > "Fail CI when a plugin or MCP server doesn't load" — `system/init`의 `plugin_errors`, `mcp_server_errors`.
- 관련 섹션: 검증 자동화·CI 챕터 — Codex `codex exec`와 대조.

### 자료 14: 권한 모드 (auto mode·dontAsk·bypass)
- 출처: https://code.claude.com/docs/en/permission-modes ; https://code.claude.com/docs/en/permissions
- 신뢰성: 최상
- 핵심: 모드 6종 `default`(Manual)·`acceptEdits`·`plan`·`auto`·`dontAsk`·`bypassPermissions`. **v2.1.283부터 auto mode가 대화형 터미널·VS Code의 기본 시작 모드.** auto mode = 분류기 모델이 행동을 검토.
- 인용:
  > "With Claude Code v2.1.283 or later, auto mode is the built-in starting permission mode for interactive terminal and VS Code sessions."
  > "Auto mode lets Claude execute without routine permission prompts. A separate classifier model reviews actions before they run, blocking anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content Claude read."
  > 표: `dontAsk` — "Reads and pre-approved tools; anything that would prompt is denied | Locked-down CI and scripts"; `bypassPermissions` — "Everything | Isolated containers and VMs only"
  > CI 예: `claude -p "run the test suite" --permission-mode dontAsk --allowedTools "Bash(npm test)" "Read"`
  > "Deny rules block in every mode, including `bypassPermissions`."
- 관련 섹션: 신뢰 단계별 권한 설정 매핑(1단계 Manual → 2단계 acceptEdits/allowlist → 3단계 auto → 4단계 dontAsk/CI).

### 자료 15: `/loop`(스케줄 태스크)와 `/goal`
- 출처: https://code.claude.com/docs/en/scheduled-tasks ; https://code.claude.com/docs/en/goal ; CHANGELOG(`/loop` 2.1.71, `/goal` 2.1.139)
- 신뢰성: 최상
- 인용(/loop):
  > "`/loop 5m check the deploy` | Your prompt runs on a fixed schedule" / "`/loop check the deploy` | Your prompt runs at an interval Claude chooses" / "`/loop` | The built-in maintenance prompt runs, or your `loop.md` if one exists"
  > "You can also pass a skill as the prompt, for example `/loop 20m /review-pr 1234`"
  > 기본 유지보수 프롬프트: "continue any unfinished work … tend to the current branch's pull request: review comments, failed CI runs, merge conflicts … run cleanup passes"
  > "Recurring tasks automatically expire 7 days after creation."
  > 비교표: Cloud(Routines) 최소 1시간 / Desktop 1분 / `/loop` 1분.
- 인용(/goal):
  > "The `/goal` command sets a completion condition and Claude keeps working toward it without you prompting each step. After each turn, a model checks whether the condition holds."
  > "`/goal` adds a separate evaluator that checks your condition after every turn, so completion is decided by a fresh model rather than the one doing the work."
  > "`/goal` is a wrapper around a session-scoped prompt-based Stop hook."
  > 예: `/goal all tests in test/auth pass and the lint step is clean`
  > "The evaluator … doesn't run commands or read files independently, so write the condition as something Claude's own output can demonstrate."
- 관련 섹션: hill-climbing(워크숍 `[00:21:46]` Cursor `/loop`)의 Claude Code 대응: `/loop`(시간 기반) + `/goal`(조건 기반). **Cursor `/loop` 공식 문서는 미확인**(pstack README가 "cursor's `/loop` command"를 언급하므로 존재는 확실).

### 자료 16: 클라우드 세션 / Routines / Auto-fix PR
- 출처: https://code.claude.com/docs/en/claude-code-on-the-web ; https://code.claude.com/docs/en/routines
- 신뢰성: 최상
- 인용(클라우드):
  > "A cloud session is a Claude Code session that runs on cloud infrastructure instead of on your machine. … The session keeps running after you close your laptop"
  > "claude --cloud \"Fix the authentication bug in src/auth/login.ts\""
  > "each `--cloud` command creates its own cloud session that runs independently."
  > "Plan locally, execute in the cloud"
  > Auto-fix: "Claude can watch a pull request and automatically respond to CI failures and review comments. … when a check fails or a reviewer leaves a comment, Claude investigates and pushes a fix if one is clear." / `/autofix-pr`
  > "Cloud sessions are available on Pro, Max, and Team plans, and for Enterprise users with premium seats"
- 인용(Routines, research preview):
  > "Define routines that run on a schedule, trigger on API calls, or react to GitHub events from cloud infrastructure."
  > "**Alert triage.** Your monitoring tool calls the routine's API endpoint when an error threshold is crossed … opens a draft pull request with a proposed fix"
  > GitHub 트리거 이벤트: "Pull request | A PR is opened, closed, assigned, labeled, synchronized, or otherwise updated" / "Release"
  > "Routines run autonomously as full Claude Code cloud sessions: there is no permission-mode picker"
  > "The minimum interval is one hour"
- 관련 섹션: 3단계(클라우드 에이전트가 신호를 집어 PR) — Benny 패턴을 Routines(API 트리거 + Slack 커넥터)로 재현하는 레시피.

### 자료 17: Agent teams(experimental)·Workflow·`/batch`·agent view
- 출처: https://code.claude.com/docs/en/agent-teams ; CHANGELOG(agent teams 2.1.32 research preview, `/batch` 2.1.63, Workflow tool ≤2.1.152)
- 신뢰성: 최상
- 인용:
  > "Agent teams are experimental and disabled by default. Enable them by setting `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`"
  > "Agent teams add coordination overhead and use significantly more tokens than a single session."
  > "Start with 3-5 teammates for most workflows."
  > 품질 게이트 훅: "`TaskCompleted`: runs when a task is being marked complete. Exit with code 2 to prevent completion and send feedback."
  > best-practices: "Run `/batch <instruction>` to have Claude split the change across 5 to 30 subagents. Each subagent works in its own worktree."
  > best-practices: "Agent view: research preview. Run `claude agents` to dispatch sessions that keep running in the background and watch them from one screen"
- 관련 섹션: 병렬 규모 챕터 — "subagents(결과만) vs teams(토론)" 구분. 책은 신뢰 단계상 subagents + worktree를 기본으로 권하고 teams는 선택으로.

### 자료 18: Best practices (검증·CLAUDE.md·훅·Writer/Reviewer)
- 출처: https://code.claude.com/docs/en/best-practices (구 anthropic.com/engineering/claude-code-best-practices에서 308 리다이렉트)
- 신뢰성: 최상
- 인용:
  > "Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from."
  > "Claude stops when the work looks done. Without a check it can run, 'looks done' is the only signal available, and you become the verification loop: every mistake waits for you to notice it."
  > 게이트 강도 4단: "In one prompt … Across a session: set the check as a `/goal` condition … As a deterministic gate: a Stop hook … By a second opinion: a verification subagent"
  > "Have Claude show evidence rather than asserting success: the test output, the command it ran and what it returned, or a screenshot of the result."
  > CLAUDE.md: "For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"
  > "If Claude already does something correctly without the instruction, delete it or convert it to a hook."
  > "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens."
  > Writer/Reviewer: "A fresh context improves code review since Claude won't be biased toward code it just wrote."
  > "The trust-then-verify gap. Claude produces a plausible-looking implementation that doesn't handle edge cases. Fix: Always provide verification (tests, scripts, screenshots). If you can't verify it, don't ship it."
  > 어드버서리얼 리뷰 경고: "A reviewer prompted to find gaps will usually report some, even when the work is sound"
- 관련 섹션: 검증 챕터 서두 — Anthropic 공식 문서가 Lauren의 "사람이 검증자면 병목" 논지와 동일한 문장("you become the verification loop")을 씀.

### 자료 19: Code Review(GitHub, research preview)와 `/code-review`·ultrareview
- 출처: https://code.claude.com/docs/en/code-review ; CHANGELOG(`/ultrareview` 2.1.111, `/simplify`→`/code-review` 2.1.147)
- 신뢰성: 최상
- 인용:
  > "Code Review is in research preview, available for Team and Enterprise subscriptions."
  > "A fleet of specialized agents examine the code changes in the context of your full codebase … then a verification step checks candidates against actual code behavior to filter out false positives."
  > "Findings are tagged by severity and don't approve or block your PR"
  > "The check run always completes with a neutral conclusion so it never blocks merging through branch protection rules. If you want to gate merges on Code Review findings, read the severity breakdown from the check run output in your own CI."
  > `gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID --jq '.output.text | split("bughunter-severity: ")[1] | split(" -->")[0] | fromjson'` → `{"normal": 2, "nit": 1, "pre_existing": 0}`
  > "Each review averages $15-25 in cost" / "completing in 20 minutes on average"
  > `REVIEW.md`: "Verification bar: require evidence before a class of finding is posted. For example, 'behavior claims need a `file:line` citation in the source, not an inference from naming'"
  > 트리거 `@claude review` / `@claude review always`
- 관련 섹션: 자동 머지 챕터 — 소프트 레이어(리뷰 봇)가 "차단하지 않음"을 공식이 명시 → 하드 게이트는 CI 스크립트로 직접 만들어야 함.

### 자료 20: Plugins·`claude plugin eval`·skill-creator
- 출처: https://code.claude.com/docs/en/plugins ; https://code.claude.com/docs/en/plugin-evals (v2.1.269+) ; https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills (2026-03-03)
- 신뢰성: 최상
- 인용(plugin eval):
  > "Each case is a realistic prompt plus one or more graders. A grader is a pass/fail check on what Claude produced, such as a regex over the reply, whether a particular tool was called, or a rubric that a second model judges the reply against."
  > "each case runs three times by default."
  > "Each case runs three times with your plugin and three times without it, so one case is six runs." (with-arm / without-arm)
  > 그레이더 6종: `regex`, `tool_used`, `tool_order`, `file_exists`, `llm`, `baseline`. "There are no custom-code graders."
  > "Pass `--judge-model sonnet` or a full model ID to choose the judge yourself."
  > "exits non-zero below a threshold so you can gate CI on it."
  > "If a case's `tool_used: Skill` grader passes but `Δ` is negative, suspect the judge before the plugin."
  > "To check that a build or test passed inside the run, have the prompt ask Claude to run it and write the outcome to a file, grade that file, and assert the command ran with a `tool_used` grader whose `input_match` names the command."
- 인용(skill-creator 블로그 2026-03-03):
  > "As models and the infrastructure around them evolve, a skill that worked well last month might behave differently today."
  > "Either way, testing turns a skill that _seems_ to work into one you _know_ works."
  > "They judge outputs without knowing which is which, so you can tell whether a change actually helped."
- 관련 섹션: 스킬+eval 챕터 — pstack eval 플레이북(자료 3)과 비교: 둘 다 블라인드 judge, 다른 모델 judge. Claude Code는 ablation(with/without)이 기본.

### 자료 21: AGENTS.md 지원 (Claude Code 측)
- 출처: https://code.claude.com/docs/en/memory ; CHANGELOG 2.1.277
- 신뢰성: 최상
- 인용:
  > CHANGELOG 2.1.277: "Added AGENTS.md support: in a project with no CLAUDE.md, Claude Code reads AGENTS.md instead; change it under 'Project instructions' in `/config`"
  > "By default, Claude reads `AGENTS.md` only when you have no `CLAUDE.md` in your working directory or above it."
  > 설정값: `claude-md-or-agents-md`(기본) / `claude-md-and-agents-md` / `claude-md` / `managed-only` — `pluginConfigs."cc-plugin-agents-md@builtin".options.instructionFiles`
  > "Not read: `AGENTS.local.md`, `AGENTS.override.md`, or anything under a `.agents/` directory"
  > "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead."
- 관련 섹션: Claude Code + Codex 병용 챕터 — 공유 파일 전략(아래 D 요약).

---

## D. OpenAI Codex 공식 문서 (0.162.1/2026-10 기준)

> **문서 위치 변경:** `developers.openai.com/codex/*`는 2026-10 현재 `learn.chatgpt.com/docs/*`로 308 리다이렉트된다("ChatGPT Work" 브랜딩). 책의 링크는 learn.chatgpt.com으로 적되 "구 developers.openai.com/codex"를 병기.

### 자료 22: Codex CLI 명령 레퍼런스 (`codex exec`, sandbox, approval, review, cloud)
- 출처: https://learn.chatgpt.com/docs/developer-commands?surface=cli
- 신뢰성: 최상
- 인용:
  > `codex exec`(alias `codex e`, Stable): 비대화형. `--json` NDJSON 이벤트, `-o` 최종 메시지 파일, `--output-schema`, `--ephemeral`, `--skip-git-repo-check`, `--ignore-rules`. `codex exec resume [SESSION_ID]`, `--last`.
  > `--sandback`/`-s`: `read-only`, `workspace-write`, `danger-full-access`
  > `--ask-for-approval`/`-a`: `on-request`, `never`
  > `--full-auto`: "Prefer `--sandbox workspace-write`; Codex prints a warning when this flag is used." (deprecated)
  > `--yolo` = `--dangerously-bypass-approvals-and-sandbox`: "Dangerous—only use inside an isolated runner."
  > `codex review`: `--uncommitted` | `--base <branch>` | `--commit <SHA>` | 커스텀 PROMPT
  > `codex cloud exec` (Experimental): "requires `--env`, and `--attempts` accepts 1–4." (= best-of-N)
  > `codex mcp add|get|list|login|logout|remove` — 설정은 `~/.codex/config.toml`
  > "The `codex mcp-server` command and standalone `codex-mcp-server` binary have been removed. Use the Codex app server instead."
- 관련 섹션: Codex를 검증/리뷰 레인으로 쓰는 레시피(`codex exec --sandbox workspace-write -a never` + `codex review --base main`).

### 자료 23: Codex AGENTS.md 규칙
- 출처: https://learn.chatgpt.com/docs/agent-configuration/agents-md.md (구 developers.openai.com/codex/guides/agents-md)
- 신뢰성: 최상
- 인용:
  > 전역: `~/.codex/AGENTS.override.md` → `AGENTS.md`; "Codex uses only the first non-empty file at this level."
  > 프로젝트: 루트→cwd 순서로 각 디렉터리에서 `AGENTS.override.md`, `AGENTS.md`, 그다음 `project_doc_fallback_filenames`. "Codex includes at most one file per directory."
  > "Filenames not on this list are ignored for instruction discovery." (**CLAUDE.md 언급 없음** — 읽게 하려면 `project_doc_fallback_filenames = ["CLAUDE.md"]`를 사용자가 설정해야 함)
  > `project_doc_max_bytes` 기본 32 KiB
  > "Files closer to your current directory override earlier guidance because they appear later in the combined prompt."
  > 권장: 루트에 "lint requirements before a pull request" 같은 팀 규범; `## Code Review Rules` 섹션 — "leave formatting and lint checks to CI."
- 관련 섹션: 병용 챕터 — **공유 전략 요약(공식 문서 2종 교차):** (1) `AGENTS.md`만 두면 Claude Code 2.1.277+가 자동으로 읽고 Codex도 읽는다. (2) Claude 전용 내용이 필요하면 `CLAUDE.md` 첫 줄에 `@AGENTS.md` import. (3) Codex에서 CLAUDE.md를 읽게 하는 건 fallback 설정이 필요. 심링크는 Windows에서 권한 문제(2차 소스 gist, 중).

### 자료 24: Codex Skills
- 출처: https://learn.chatgpt.com/docs/build-skills (구 /codex/skills)
- 신뢰성: 최상
- 인용:
  > "Use agent skills to extend ChatGPT and Codex with task-specific capabilities."
  > 위치: Repository `$CWD/.agents/skills` (+ 상위 디렉터리 `.agents/skills` up to `$REPO_ROOT`), User `$HOME/.agents/skills`, Admin `/etc/codex/skills`, System(번들).
  > "The `SKILL.md` file must include `name` and `description`."
  > 오픈 표준: agentskills.io/specification
  > 호출: CLI/IDE에서 `/skills` 또는 `$`; 암시적 호출은 `description` 매칭.
  > 번들 스킬: Skill Creator, Skill Installer, ExecPlan, GitHub Fix CI, Linear, OpenAI Docs, Yeet, Atlas Control.
- 관련 섹션: 스킬 챕터 — **같은 SKILL.md를 `.claude/skills/`와 `.agents/skills/`에 두면 양쪽에서 동작**(Agent Skills 표준). pstack 미러(backnotprop/pstack)가 `npx skills add`로 Claude Code·Codex·Cursor에 동시 설치하는 사례.

### 자료 25: Codex Subagents
- 출처: https://learn.chatgpt.com/docs/agent-configuration/subagents.md (구 /codex/subagents)
- 신뢰성: 최상
- 인용:
  > "Current Codex releases enable subagent workflows by default." (`agents.enabled` 기본 `true`)
  > "When many agents are running, Codex waits until all requested results are available, then returns a consolidated response."
  > 커스텀 에이전트: `~/.codex/agents/` 또는 `.codex/agents/`의 TOML 파일; 필수 `name`, `description`, `developer_instructions`.
  > 병렬 상한: `[agents] max_concurrent_threads_per_session = 8` 예시; "If unset, Codex chooses the default." (구 alias `agents.max_threads`)
  > 서브에이전트는 "inherit your current sandbox policy"; `sandbox_mode` 개별 오버라이드 가능.
  > CLI `/agent`로 스레드 전환.
  > worktree 격리 언급 없음.
- 2차(중, codex.danielvaughan.com): 서브에이전트 GA v0.115.0(2026-03 중순) 주장 — 공식 날짜 미확인.
- 관련 섹션: Claude subagents(자료 10)와 대조표.

### 자료 26: Codex Cloud + GitHub 코드 리뷰
- 출처: https://learn.chatgpt.com/docs/cloud ; https://learn.chatgpt.com/docs/third-party/github.md ; https://learn.chatgpt.com/docs/code-review
- 신뢰성: 최상
- 인용:
  > Cloud: "Each task has its own workspace and can keep working while your computer is asleep." / "commit or open a pull request when you're ready."
  > GitHub: "In a pull request comment, mention `@codex review`." / "Codex flags only P0 and P1 issues so review comments stay focused on high-priority risks."
  > "Codex searches your repository for `AGENTS.md` files and follows the applicable code review rules." (`## Code Review Rules` 섹션)
  > 자동 리뷰: "turn on **Automatic review** under **Review code**."
  > 후속: `@codex fix the P1 issue` → 클라우드 태스크가 브랜치에 수정 푸시
  > "Cloud review doesn't require you to create or manage a cloud environment."
- 관련 섹션: 역할 분담 — "Claude Code가 구현, Codex가 리뷰(또는 그 반대)". Codex는 리뷰 규칙을 AGENTS.md에서, Claude Code Review는 REVIEW.md/CLAUDE.md에서 읽는다는 차이.

### 자료 27: Codex 모델·체인지로그
- 출처: https://learn.chatgpt.com/docs/models ; https://learn.chatgpt.com/docs/changelog ; GitHub openai/codex releases
- 신뢰성: 최상
- 인용:
  > "Astra (`gpt-6-astra`): Our most capable model for complex work across code, apps, and research." / "6.1 Sol (`gpt-6.1-sol`): Near-Astra performance for complex work at a lower cost than Astra." / "6 Luna (`gpt-6-luna`): Our most efficient model for focused, high-volume tasks."
  > "On October 14, 2026, GPT-5.5 will retire from ChatGPT, ChatGPT Work, and Codex on all plans."
  > 은퇴: GPT-5.3-Codex-Spark(2026-09-14), gpt-5.4/5.4-mini(2026-08-31)
  > changelog 2026-09-29 "GPT-6.1 Sol in Codex and ChatGPT Work"; 2026-10-08 "GPT-6.1 Sol Ultrafast"
  > GitHub: rust-v0.162.1 2026-10-09 ("Fixed startup failures caused by differences between a running background server's feature settings and CLI defaults")
- 관련 섹션: 모델 선택 — 책은 모델명을 본문에 박지 말고 "2026-10 기준 표"로 분리할 것(은퇴 주기 1~2개월).

### 자료 28: OpenAI 공식 "Codex plugin for Claude Code"
- 출처: https://github.com/openai/codex-plugin-cc (README) — 공개 2026-03-31(Gigazine 보도, 중)
- 신뢰성: 최상(README)·중(날짜)
- 인용:
  > "Use Codex from inside Claude Code for code reviews or to delegate tasks to Codex."
  > "`/codex:review` for a normal read-only Codex review" / "`/codex:adversarial-review` for a steerable challenge review" / "`/codex:rescue`, `/codex:transfer`, `/codex:status`, `/codex:result`, and `/codex:cancel`"
  > 설치: `/plugin marketplace add openai/codex-plugin-cc` → `/plugin install codex@openai-codex` → `/codex:setup`
  > "Runs a **steerable** review that questions the chosen implementation and design."
- 관련 섹션: 병용 챕터의 핵심 레시피 — Claude Code 세션 안에서 Codex를 "다른 모델 judge"로 호출(워크숍 `[00:21:30]`의 편향 교차검증을 두 벤더로 구현).

---

## E. Java/Spring 집행 레이어

### 자료 29: Spring Boot 4.0.0 / 4.1.0 릴리스
- 출처: https://spring.io/blog/2025/11/20/spring-boot-4-0-0-available-now/ (Phil Webb, 2025-11-20) ; https://spring.io/blog/2026/06/10/spring-boot-4/ (Andy Wilkinson, 2026-06-10, 검색 결과 기반) ; https://spring.io/blog/2025/11/13/spring-framework-7-0-general-availability/
- 신뢰성: 최상
- 인용:
  > "This release is the beginning of a new Spring Boot generation providing solid foundations for coming years." (4.0.0)
  > 4.0 핵심: "The Spring Boot codebase has been split into separate modules" / "Null-safety improvements across the portfolio use JSpecify" / "Java 25 is supported, and Java 17 compatibility is kept" / "API Versioning and HTTP Service Clients"
  > 4.1.0(2026-06-10): Spring gRPC 지원, Jackson 설정 속성 갱신, HTTP Client SSRF 완화, OpenTelemetry 관측성 갱신 (검색 요약, 중)
- 2차(중, InfoQ 2025-11): "The team strongly recommends upgrading to Spring Boot 3.5 first and resolving all deprecation warnings before attempting the 4.0 migration." / Spring Boot 3.5 무료 지원 2026-06까지.
- 관련 섹션: Java 독자 환경 설정 — "Spring Boot 4.x + Java 25/2026 기준".

### 자료 30: Spring Modulith `verify()`
- 출처: https://docs.spring.io/spring-modulith/reference/verification.html (2.1.1 Stable)
- 신뢰성: 최상
- 인용:
  > `ApplicationModules.of(Application.class).verify();`
  > "No cycles on the application module level — the dependencies between modules have to form a directed acyclic graph."
  > "Efferent module access via API packages only — all references to types that reside in application module internal packages are rejected."
  > "Explicitly allowed application module dependencies only (optional) — an application module can optionally define allowed dependencies via `@ApplicationModule(allowedDependencies = …)`."
  > "`ApplicationModules.verify()` throws an exception in case of any architectural violation being detected. You can access the violations … by instead calling `ApplicationModules.detectViolations()`."
  > "Spring Modulith optionally integrates with the jMolecules ArchUnit library and, if present, automatically triggers its Domain-Driven Design and architectural verification rules"
- 관련 섹션: 아키텍처 챕터 — Dune의 "electron-main ↔ renderer 임포트 경계 CI"의 Java 대응물 1순위(테스트 한 줄로 모듈 경계 = CI 빨간불).

### 자료 31: ArchUnit 릴리스
- 출처: https://github.com/TNG/ArchUnit/releases
- 신뢰성: 최상
- 핵심: 1.5.1(9/25, 버그픽스: "`java.lang.IO` is included in standard stream access") · 1.5.0(8/4: "Adds JUnit 6 support (`archunit-junit6`), sealed-class info on `JavaClass`") · 1.4.2(4/18). 1.5.0은 "Supports Java 27 (class file major version 71). Build and tests run on JDK 25."
- 관련 섹션: 레이어 규칙(`layeredArchitecture()`, `noClasses().that()…should().dependOnClassesThat()`) 예시. 연도는 페이지 미표기(미확인, 2026 추정).

### 자료 32: Spring Boot Testcontainers `@ServiceConnection`
- 출처: https://docs.spring.io/spring-boot/reference/testing/testcontainers.html (4.1.1)
- 신뢰성: 최상
- 인용:
  > "Thanks to @ServiceConnection, the above configuration allows Neo4j-related beans in the application to communicate with Neo4j running inside the Testcontainers-managed Docker container. This is done by automatically defining a Neo4jConnectionDetails bean … overriding any connection-related configuration properties."
  > "You'll need to add the spring-boot-testcontainers module as a test dependency in order to use service connections with Testcontainers."
  > 코드: `@Testcontainers @SpringBootTest class MyIntegrationTests { @Container @ServiceConnection static Neo4jContainer neo4j = new Neo4jContainer("neo4j:5"); … }`
- 관련 섹션: 검증 챕터 — 에이전트가 "앱을 실제로 띄워" 검증하는 Java 측 수단(개발 시간 서비스 `SpringApplication.from(...).with(...)`는 별도 페이지 `features/dev-services.html` — 미열람).

### 자료 33: Error Prone / NullAway
- 출처: https://github.com/uber/NullAway (README, 검색 요약) ; Maven Central(2.50.0, 2026-06-10, 중)
- 신뢰성: 중
- 인용(검색 요약 기반, 원문 확인 권장):
  > NullAway "is built as a plugin to Error Prone and can run on every single build of your code." / "requires that you build your code with Error Prone, version 2.14.0 or higher."
  > Gradle: `check("NullAway", CheckSeverity.ERROR)` — 기본은 경고이므로 ERROR로 올려야 CI가 빨개짐.
  > 기존 코드베이스: Error Prone 전체 체크를 끄고 NullAway만 켜서 시작하라는 가이드(2026, 중).
- 관련 섹션: 집행 레이어 "컴파일러를 엄격하게" — Rust borrow checker 비유의 Java 버전(`-Werror` + Error Prone + NullAway + JSpecify). **`-Werror`·Checkstyle·Spotless·jqwik·REST Docs·springdoc의 2026 최신 버전은 미확인.**

### 자료 34: Java 25 LTS
- 출처: https://www.infoq.com/news/2025/09/java25-released ; https://www.azul.com/blog/a-java-champions-guide-to-jdk-25-features/
- 신뢰성: 중(기술 매체)
- 핵심: JDK 25 GA 2025-09-16, JDK 21 이후 첫 LTS. 18 JEP. JEP 506 Scoped Values(final), JEP 505 Structured Concurrency(5th preview), JEP 512 Compact Source Files, JEP 513 Flexible Constructor Bodies, JEP 519 Compact Object Headers.
- 관련 섹션: 환경 기준 명시용.

---

## F. React/Next.js 집행 레이어

### 자료 35: Next.js 16 릴리스
- 출처: https://nextjs.org/blog/next-16 — 2025-10-21, Jimmy Lai·Josh Story·Sebastian Markbåge·Tim Neutkens
- 신뢰성: 최상
- 인용:
  > "Turbopack has reached stability for both development and production builds, and is now the default bundler for all new Next.js projects."
  > "Cache Components are a new set of features designed to make caching in Next.js both more explicit, and more flexible. They center around the new `\"use cache\"` directive"
  > "Unlike the implicit caching found in previous versions of the App Router, caching with Cache Components is entirely opt-in."
  > "Next.js 16 introduces **Next.js DevTools MCP**, a Model Context Protocol integration for AI-assisted debugging … Unified logs: Browser and server logs without switching contexts … Automatic error access: Detailed stack traces without manual copying"
  > "`proxy.ts` replaces `middleware.ts` and makes the app's network boundary explicit."
  > "Built-in support for the React Compiler is now stable in Next.js 16 following the React Compiler's 1.0 release."
  > 제거: "`next lint` command | Use Biome or ESLint directly; `next build` no longer runs linting."
  > "`@next/eslint-plugin-next` default | Now defaults to ESLint Flat Config format, aligning with ESLint v10"
  > "Node.js 20.9+ | Minimum version now 20.9.0 (LTS)"
  > 기여자 목록에 `@poteto` 포함(React Compiler 코어팀 — Lauren).
- 관련 섹션: 프런트 환경 기준 + 검증 수단(DevTools MCP). **`next build`가 린트를 안 돌리므로 CI에 ESLint 단계를 명시적으로 넣어야 함** — 집행 레이어 설계 포인트.

### 자료 36: React 19.2
- 출처: https://react.dev/blog/2025/10/01/react-19-2 — 2025-10-01, The React Team
- 신뢰성: 최상
- 인용:
  > `<Activity />`: "`hidden`: hides children, unmounts effects, and defers updates"
  > `useEffectEvent`: "**Effect Events should _not_ be declared in the dependency array**."
  > "You don't need to wrap everything in `useEffectEvent`, or to use it just to silence the lint error, as this can lead to bugs."
  > "To solve this, most users just disable the lint rule and exclude the dependency. But that can lead to bugs since the linter can no longer help you keep the dependencies up to date"
  > "`eslint-plugin-react-hooks` v6 uses flat config by default in the `recommended` preset and adds opt-in React Compiler-powered rules."
- 관련 섹션: "useEffect 금지"(Dune) 논의 — 공식 React도 `exhaustive-deps` 끄기를 경계. 책의 레시피: `react-hooks/exhaustive-deps: error` + `no-restricted-syntax`로 `useEffect` 호출 자체를 금지하거나 허용 디렉터리만 예외.

### 자료 37: ESLint `no-restricted-syntax` (useEffect 금지 구현 수단)
- 출처: https://eslint.org/docs/latest/rules/no-restricted-syntax
- 신뢰성: 최상
- 인용:
  > "This rule disallows specified (that is, user-defined) syntax."
  > 옵션 예: `{ "selector": "CallExpression[callee.name='setTimeout'][arguments.length!=2]", "message": "setTimeout must always be invoked with two arguments." }`
- 관련 섹션: 레시피 — `{ "selector": "CallExpression[callee.name='useEffect']", "message": "..." }` (책에서 작성 시 실제 동작 확인 필요; ESLint 10.12.0/2026-10 기준).

### 자료 38: eslint-plugin-boundaries / dependency-cruiser / knip
- 출처: https://github.com/javierbrea/eslint-plugin-boundaries ; https://xebia.com/blog/taking-frontend-architecture-serious-with-dependency-cruiser/ (2026-06) ; https://knip.dev
- 신뢰성: 최상(저장소)·중(Xebia)
- 핵심(검색 요약): boundaries — "maintain clean architecture by enforcing boundaries between different parts of your codebase", 핵심 룰 `boundaries/dependencies`. dependency-cruiser — 해석된 모듈 그래프에서 import 허용/금지 집행 + 시각화(Ghost 사례: ESLint 룰이 놓친 ESM import를 잡음). knip — 미사용 코드·의존성·설정 탐지(v6 모노레포 지원).
- 관련 섹션: Dune "import 경계 CI"의 Next.js 대응: 파일 단위 즉시 피드백(boundaries) + CI 그래프 검사(dependency-cruiser) + 죽은 코드 제거(knip).

### 자료 39: Chrome DevTools MCP
- 출처: https://github.com/ChromeDevTools/chrome-devtools-mcp (1.10.1)
- 신뢰성: 최상
- 인용:
  > "lets your coding agent (such as Antigravity, Claude, Cursor or Copilot) control and inspect a live Chrome browser."
  > 설정: `"command": "npx", "args": ["-y", "chrome-devtools-mcp@latest"]`
  > 성능: "to record traces and extract actionable performance insights."
  > 요구: Node.js LTS, Chrome current stable.
- 관련 섹션: 검증 챕터 — Lauren의 control-glass(CDP 직접 제어)를 **직접 만들 필요 없이** MCP로 대체하는 경로. 트레이스·콘솔·네트워크를 에이전트가 읽는다.

### 자료 40: Playwright MCP
- 출처: https://github.com/microsoft/playwright-mcp (0.0.83)
- 신뢰성: 최상
- 인용:
  > "A Model Context Protocol (MCP) server that provides browser automation capabilities using Playwright."
  > "Uses Playwright's accessibility tree, not pixel-based input" / "No vision models needed, operates purely on structured data"
  > Claude Code 설치: `claude mcp add playwright npx @playwright/mcp@latest`
  > 도구: `browser_snapshot`("better than screenshot"), `browser_navigate`, `browser_click`, `browser_type`, `browser_evaluate`, `browser_fill_form`, `browser_wait_for`, `browser_network_requests`
- 관련 섹션: 검증 — "행동은 Playwright, 진단은 DevTools MCP" 분업(2차 블로그 공통 패턴).

### 자료 41: Storybook 비주얼 테스트
- 출처: https://storybook.js.org/docs/writing-tests/visual-testing (Storybook 10.6)
- 신뢰성: 최상
- 핵심: Chromatic 애드온(`npx storybook@latest add @chromatic-com/storybook`)으로 스토리별 스냅샷 vs 베이스라인 픽셀 비교; PR에 "UI Tests" 체크 → "make it required in your Git provider" to "prevent accidental UI bugs from being merged." Vitest 애드온과 통합.
- 관련 섹션: 하드 게이트 목록(프런트) — 시각 회귀를 required check로.

### 자료 42: GitHub Auto-merge / Merge queue / `gh pr merge --auto`
- 출처: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request ; https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue ; `gh pr merge --help`(로컬 gh)
- 신뢰성: 최상
- 인용:
  > "Auto-merge merges a pull request automatically after all required reviews and status checks pass."
  > "Before you use auto-merge, it must be enabled for the repository."
  > "Auto-merge is disabled if someone without write permissions pushes new changes to the head branch"
  > Merge queue: "A merge queue helps increase velocity by automating pull request merges into a busy branch." / "You must use the `merge_group` event to trigger your GitHub Actions workflow."
  > `gh pr merge --help`: "--auto  Automatically merge only after necessary requirements are met" / "If required checks have passed, the pull request will be added to the merge queue."
- 관련 섹션: 4단계(자동 머지) — Lauren의 "agents autoemerging PRs"를 GitHub 기능으로 구현: required checks(ArchUnit/Modulith/ESLint/boundaries/Playwright) + auto-merge + merge queue.

---

## G. 에이전트 평가(eval) 도구

### 자료 43: promptfoo / Braintrust (2차 비교)
- 출처: https://www.braintrust.dev/articles/braintrust-vs-promptfoo ; 검색 요약
- 신뢰성: 중(벤더 블로그·비교 사이트)
- 핵심: promptfoo = CLI/YAML, 로컬·CI 실행(0.124.1/2026-10). **OpenAI가 2026-03-09 promptfoo 인수 발표, 오픈소스 유지**(2차, 미확인). Braintrust = 호스팅, LLM-as-judge 스코어러·트레이스·CI 게이트. LLM-as-judge 편향: "length, confidence, position and self-preference bias".
- 관련 섹션: eval 챕터 보조 — 책의 주축은 pstack eval 플레이북 + `claude plugin eval`이고, 범용 도구는 각주.

### 자료 44: Thoughtworks Technology Radar Vol. 34 (2026-04)
- 출처: https://www.thoughtworks.com/en-us/radar (테마 "Putting coding agents on a leash")
- 신뢰성: 최상
- 인용:
  > "humans are increasingly being tempted to step out of the loop."
  > "controls that guide agents' behavior before code is generated and provide feedback afterwards to enable self-correction."
  > "Feedforward controls anticipate what the agent needs to increase the likelihood of a correct first attempt." (예: Agent Skills, Superpowers, GitHub Spec-Kit, OpenSpec)
  > 피드백 측: 결정론적 품질 게이트(뮤테이션 테스트·퍼징·코드 품질 분석)를 에이전트 워크플로 안에서 실행해 "failures are fixed before human review"(요약)
  > 다른 테마: "codebase cognitive debt" / "This is not nostalgia, but a necessary counterweight to the speed at which AI tools can generate complexity."
- 관련 섹션: 집행 레이어 피라미드를 업계 용어(feedforward/feedback)로 뒷받침. 뮤테이션 테스트(`cargo-mutants` 언급; Java는 PIT — 미조사)를 "검증자를 검증"의 수단으로.

---

## H. 담론 (verification is the bottleneck 류)

### 자료 45: OpenAI "Harness engineering: leveraging Codex in an agent-first world"
- 출처: https://openai.com/index/harness-engineering/ — 2026-02-11, Ryan Lopopolo (**원문 403으로 직접 열람 실패**; 요약은 https://rywalker.com/research/openai-harness 및 Martin Fowler 분석 경유, 중)
- 신뢰성: 중(2차 경유) — 원문 재확인 필요
- 핵심(2차 요약): 2025-08부터 약 5개월, 3→7명 팀, 손으로 쓴 코드 0, ~1,500 merged PR(≈3.5 PR/엔지니어/일), ~100만 줄. AGENTS.md는 `docs/`를 가리키는 목차. 커스텀 린터·구조 테스트로 레이어 아키텍처 집행, 주기적 "garbage collection" 패스, 에이전트 간 리뷰.
- 인용(2차가 전한 유일한 직접 문장):
  > "Our most difficult challenges now center on designing environments, feedback loops, and control systems."
- 관련 섹션: Lauren의 "환경을 설계하라"(헤드 셰프)와 동일 결론을 Codex 팀이 독립적으로 도달 — 두 벤더 교차 근거.

### 자료 46: Mitchell Hashimoto "My AI Adoption Journey"
- 출처: https://mitchellh.com/writing/my-ai-adoption-journey — 2026-02-05
- 신뢰성: 최상(저자 블로그)
- 6단계: "Step 1: Drop the Chatbot / Step 2: Reproduce Your Own Work / Step 3: End-of-Day Agents / Step 4: Outsource the Slam Dunks / Step 5: Engineer the Harness / Step 6: Always Have an Agent Running"
- 인용:
  > "If you give an agent a way to verify its work, it more often than not fixes its own mistakes and prevents regressions."
  > "anytime you find an agent makes a mistake, you take the time to engineer a solution" / "give the agent fast, high quality tools to automatically tell it when it is wrong."
  > "forced myself to reproduce all my manual commits with agentic ones."
  > "block out the last 30 minutes of every day to kick off one or more agents."
  > "it was my job as a human to be in control of when I interrupt the agent, not the other way around."
- 관련 섹션: 신뢰 곡선의 "개인 버전" — 6단계가 Lauren의 4단계와 겹침(Step 2 = 로컬 관찰, Step 5 = 집행 레이어, Step 6 = 상시 에이전트). 한국어 번역 요약: GeekNews(discuss.pytorch.kr 미러).

### 자료 47: Simon Willison "More than just code review"
- 출처: https://simonwillison.net/2026/Aug/22/more-than-just-code-review/ — 2026-08-22
- 신뢰성: 최상
- 인용:
  > "The key skill required to make productive use of coding agents is being able to confidently instruct them" (… and then confidently verify that those changes have been applied in the correct way — 검색 요약이 전한 후반부)
  > "Sometimes this involves reviewing every line of code they have written, but there are other ways to achieve that goal."
  > "Eyeballing every line of code has never been the most effective way to validate a change to a piece of software."
- 관련 섹션: "코드 리뷰 랜드는 최악"(`[00:46:18]`)의 외부 지지 발언.

### 자료 48: Addy Osmani "Agentic Code Review"
- 출처: https://www.oreilly.com/radar/agentic-code-review/ — 2026-06-26 (addyosmani.com 재게재)
- 신뢰성: 최상(저자)·수치는 인용된 벤더 연구(중)
- 인용:
  > "The bottleneck didn't disappear; it moved to verification, and review is where that bill comes due."
  > "Four copies of one model is a single reviewer with a larger invoice."
  > "The loop can be both very sure and very wrong, with no human left to tell the difference."
  > "A model can't be paged and can't be held responsible for what it shipped, so whoever clicks merge owns it."
  > "'No users' is permission to defer review. It isn't permission to skip verification."
  > AI 리뷰는 "as a sensor, not a verdict."
- 인용 수치(저자가 인용한 벤더 연구; 책에서는 출처 한정 필수): Faros AI(22,000 devs, 2026-03) code churn +861%, incidents/PR +242.7%, 리뷰 시간 +441.5%; CodeRabbit(470 OSS PR, 2025-12) AI 공저 변경 이슈 ≈1.7×; GitClear "around 4x the raw output" vs 실제 생산성 ≈12%; Anthropic Code Review 오탐 <1%; 4개 도구 실험(146 PR, 679 findings) "93.4% were caught by exactly one of the four tools."
- 관련 섹션: "다른 모델 judge" 논거(93.4% 단일 도구 포착 → 교차 리뷰 필요) + "코드 리뷰 코멘트는 code smell"의 통계적 배경.

### 자료 49: Anthropic "Building effective agents"
- 출처: https://www.anthropic.com/engineering/building-effective-agents — 2024-12-19, Erik Schluntz·Barry Zhang (고전 레퍼런스)
- 신뢰성: 최상
- 인용:
  > 워크플로 vs 에이전트: workflows = "LLMs and tools are orchestrated through predefined code paths"; agents = LLMs "dynamically direct their own processes and tool usage."
  > 에이전트는 "gain 'ground truth' from the environment at each step"
  > "Code solutions are verifiable through automated tests." / "iterate on solutions using test results as feedback."
  > "human review remains crucial"
  > Evaluator-optimizer: "one LLM call generates a response while another provides evaluation and feedback in a loop."
- 관련 섹션: 이론적 뿌리 — Lauren의 "검증이 루프를 닫는다"(`[00:06:29]` "that's the thing that really closes the loop")와 "ground truth from the environment".

---

## I. 한국어 자료

### 자료 50: 토스 기술블로그 "소프트웨어 3.0 시대를 맞이하며"
- 출처: https://toss.tech/article/44539 — 2026-01-26, 김용성(토스페이먼츠 Node.js Developer)
- 신뢰성: 최상(회사 엔지니어링 블로그)
- 핵심: Claude Code를 "하네스"로 보고 Slash Commands=컨트롤러, Sub-agents=서비스 레이어, Skills=단일 책임 컴포넌트, MCP=어댑터, CLAUDE.md=`package.json` 같은 매니페스트로 매핑. HITL 질문은 "되돌릴 수 없거나 위험하거나 애매한 결정"에만.
- 인용:
  > "CLAUDE.md를 자주 수정하고 있다면, 그 내용은 거기 있으면 안 되는 것일 가능성이 높습니다."
  > "에이전트가 환경을 자동 감지하되, 애매한 부분은 질문합니다."
  > "지침을 작성한 뒤, Claude에게 \"이 워크플로우를 실행하면 어떤 파일들을 읽게 될 것 같아?\"라고 물어보세요."
  > `/setup → 감지된 환경: TypeScript + React, pnpm`
- 관련 섹션: 스킬 챕터 한국 독자용 도입부 — CLAUDE.md에 "안정적 원칙만" 두라는 조언이 Anthropic best practices와 일치.

### 자료 51: LY Corporation(라인) 기술블로그 "Claude Code Action: 조직 전반의 코드 품질을 지키는 AI 코드 리뷰 플랫폼화"
- 출처: https://techblog.lycorp.co.jp/ko/building-ai-code-review-platform-with-claude-code-action — 이동원(LINE NEXT DevOps). 발행일 본문 미표기(검색 메타 약 2026-02 추정, 측정 기간 2025-12 중순~2026-01 초)
- 신뢰성: 최상
- 핵심: Claude Code Action을 caller(서비스 리포)/executor(중앙 리포) 구조로 플랫폼화. 공통 프롬프트 `common/{analysis_type}.yml` + 서비스별 `{service_name}/code-review.yml` 병합. GitHub App 단기 토큰, 사내 프록시 → AWS Bedrock Claude. **약 1개월간 32개 리포, 344회 AI 리뷰.** DORA 대시보드에 호출 수·수행 시간·성공률 포함.
- 인용:
  > "리뷰 기준과 실행 로직은 중앙에서 통제하고 각 서비스 리포지터리에는 '호출'만 남기는 구조를 만든다."
  > "이 시스템에서 Claude Code는 자유롭게 말하는 AI가 아니라 조직의 기준을 따르는 리뷰어로 작동합니다."
  > "표준화는 끝이 아니라 시작입니다."
- 교훈: 공식 Action이 포크 PR 미처리 → `refs/pull/<번호>/head` fetch로 우회; 사용자 입력이 출력 형식을 바꾸는 문제 → 시스템 형식을 상위 지시로 고정.
- 관련 섹션: 소프트 레이어(리뷰 봇)의 조직 도입 사례 — 한국 독자용. 단, 이건 "리뷰"이지 "하드 게이트"가 아님을 책에서 구분.

### 자료 52: GeekNews 위클리 GN#347 "Vibe Coding 이후 1년, 코딩은 무엇이 되었나"
- 출처: https://news.hada.io/weekly/202609 — 2026-02-23~03-01 기간
- 신뢰성: 중(뉴스레터 요약)
- 인용:
  > "코드 품질 검증의 중심을 라인별 리뷰에서 스펙·테스트·자동 검증 인프라로 옮기자는 것"
  > "품질 판단과 책임은 인간 개발자에게 남아 있습니다"
  > "반복된 실패가 생길 때는 문서를 늘리기보다 코드베이스 자체를 수정하는 것이 바람직합니다"
  > "적절히 작업을 분해하고 감독하는 능력 자체가 새로운 핵심 역량으로 떠오르고 있습니다"
- 관련 섹션: 한국 커뮤니티 담론이 같은 결론(문서보다 코드베이스/집행 레이어를 고쳐라)에 도달했다는 근거. 챕터 오프닝 소재.

### 자료 53: 보안뉴스 — 한국 Claude Code 이용 현황 (참고)
- 출처: https://m.boannews.com/html/detail.html?idx=139926 (2025-10, 검색 요약)
- 신뢰성: 중
- 핵심(요약): "한국에서는 지난 4개월 동안 클로드 코드의 월간 활성 이용자 수(MAU)가 6배 증가", "한국 소프트웨어 엔지니어가 전 세계에서 클로드 코드를 가장 많이 이용한 사용자 1위". 2025-10 기준이라 구버전 정보일 수 있음.
- 관련 섹션: 서문 — 왜 한국 독자인가.

---

## J. 미확인 항목 (추측하지 않음)

1. **Lauren Tan의 정식 직함** — "Principal Engineer"(GitHub 미러 설명), "senior engineer"(KuCoin 기사), "heads GrokBot"(기사) 등 2차 소스가 제각각. 확인된 것: GitHub bio "Software Engineer @xai-org & @react compiler core team", 본인 발화 "I work at a AI lab", pstack README "at Cursor". 책에서는 직함 없이 "Cursor(SpaceXAI) 엔지니어, React Compiler 코어팀"으로.
2. **Lauren의 X 게시물(2026-09-21) 원문** — x.com 402로 미열람. "2,500 PRs" 숫자는 2차(redreamality) 경유.
3. **"organic architecture" 트윗 원문** — 검색 불가.
4. **Grok 4.6이 4.5와 동일 단가인지** — x.ai 발표문은 "$2/M input, $6/M output"만 명시, 4.5 비교 없음. Lauren 본인도 hedging.
5. **Grok Bot 공식 페이지(x.ai/bot) 원문** — 403. 가격·플랫폼은 VentureBeat(중) 기준. "Chief of Staff"가 기본 기능인지 사용자 구성 예시인지 불명.
6. **Dune 아키텍처** — 공개 문서 없음(본인 발화로 확정: 오픈소스 안 함).
7. **Pretext 가상화 라이브러리** — 웹 미확인.
8. **Cursor `/loop` 공식 문서** — 미발견(pstack README와 워크숍 발화로 존재는 확실).
9. **Cursor 랜딩 "pstack: the skills behind 10,000 agent runs"(cursor.com/lp-team/lauren)** — 모든 로케일 URL이 가격 페이지로 리다이렉트. "10,000 runs/week" 수치는 검색 스니펫 경유(중).
10. **OpenAI harness engineering 원문** — 403. 수치(1,500 PR, 3→7명)는 2차 경유.
11. **Codex 서브에이전트 GA 시점·기본 동시 스레드 수** — 공식 문서가 "Codex chooses the default"라고만 함.
12. **OpenAI codex-plugin-cc 공개일** — Gigazine 2026-03-31 보도 기준(gh 메타 조회 실패).
13. **OpenAI의 promptfoo 인수(2026-03-09)** — 비교 사이트 경유.
14. **ArchUnit 릴리스 연도**(페이지 미표기), **Testcontainers·jqwik·NullAway·Checkstyle·Spotless·springdoc·REST Docs 최신 버전**(Maven 검색 인덱스 낡음).
15. **우아한형제들·카카오·네이버 D2의 AI 코딩 에이전트 도입 글** — 3회 검색에서 미발견. 한국 회사 블로그는 토스·LY Corp만 확보.
16. **Addy Osmani가 인용한 Faros/CodeRabbit/GitClear 수치의 원 보고서** — 미열람.
17. **Thoughtworks Radar "deterministic quality gates" 정확한 문구** — 요약만 확보(테마 원문 일부 인용 확보).

## K. 수집 한계

- 접근 실패: openai.com/index/harness-engineering(403), x.ai/bot(403), x.com 게시물(402), cursor.com/lp-team/lauren(가격 페이지로 리다이렉트), github.com/poteto/pstack(존재하지 않음 — 정전은 cursor/plugins/pstack), learn.chatgpt.com/docs/agents-md 구 경로(404 → agent-configuration/agents-md.md로 대체).
- 의도적으로 제외: 출처 불명 나열형 "Top 10" 블로그, 날짜 없는 번역 요약 사이트(youtubesummary 등), 거래소 뉴스(KuCoin/HTX)의 Lauren 기사. 커뮤니티 토론(Reddit/HN/GeekNews 댓글)과 논문은 다른 리서처 담당이라 수집하지 않음(GN#347은 뉴스레터로 분류해 포함).
- 자막 한계: 자동 생성 영어 자막이라 고유명사(PAC/pstack, Grockbot/Grok Bot, Gary/Garry)가 흔들림. 인용은 자막 원문 그대로 두고 이 문서 A-0에서 정식 표기를 못 박음.
- 시간 민감도: Claude Code는 거의 매일, Codex CLI는 주 2~3회 릴리스. 모델명(gpt-5.5 은퇴 2026-10-14)은 출간 시점에 재확인 필수. 본문엔 버전을 박지 말고 0절 표로 분리하는 편집 방침을 권고.
