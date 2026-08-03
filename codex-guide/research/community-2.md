# Codex 커뮤니티 리서치 보충 — Reddit·한국어·클라우드 위임 (검색 2026-08-02 기준)

> **이 문서의 범위:** 선행 `community.md`(563줄, 출처 77개)가 명시한 3개 공백만 메운다. 선행 문서가 이미 확보한 GitHub 이슈(#11626, #12115, #28969, #28879, #24515)는 재조사하지 않았고, Reddit에서 그 주제의 *반응*이 잡힌 경우만 §5에 보강 인용으로 넣었다.
>
> **Reddit 접근: 성공.** JSON API(`search.json`)·`old.reddit.com`·redlib 미러·WebFetch는 전부 차단(403/302→로그인)됐지만 **Atom RSS 엔드포인트**(`/r/{sub}/search.rss`, `/r/{sub}/comments/{id}/.rss`)는 열려 있었다. 이 경로로 게시글 본문과 **상위 댓글 원문**을 직접 확보했다. 상세는 §7.
>
> **신선도 규칙:** 게시일 2026-02-02 이전 = `⏳ 오래됨`. **요금·한도 주장은 예외 없이 날짜를 병기**했다.
> **신뢰 등급:** `[출처 명확]` = 식별 가능 계정 + 재현 가능한 수치·로그·절차 / `[익명 주장·확인 필요]` = 익명 단일 진술 / `[2차·미검증]` = 원 출처를 직접 확인하지 못함.
>
> ⚠️ **진영 표기 규율:** 이 문서의 Reddit 인용에는 출신 서브레딧을 전부 적었다. r/codex는 Codex 진영, r/ClaudeAI는 Claude 진영이다. 선행 문서 §8-1의 편향 경고는 이번 1차 자료로 **강화됐다**(§5-7 참조).

---

## 1. Reddit 1차 자료 (전환 후기·비교 스레드)

### 1-1. 핵심 스레드 ①: "Claude Code에서 Codex로 넘어간 분들 — 뭐가 낫고 뭐가 나쁩니까?"

**출처:** /u/LandinoVanDisel, r/codex, **2026-03-17**, 댓글 85개
https://www.reddit.com/r/codex/comments/1rwjmqp/those_of_you_who_switched_from_claude_code_to/

선행 리서처가 GeekNews 번역 경유로만 가지고 있던 "전환 후기" 축의 **원문 스레드**다. 질문 자체가 전환자의 불안을 그대로 담고 있다.

- 질문 본문 (LandinoVanDisel):
  > "I love Claude Code but it's becoming unreliable with how regularly it goes down. Curious about the output from Codex, particularly with **code not written by Codex**. How well does it seem to understand existing code? What about releasing code with bugs? Does it seem to interpret instructions pretty well or do long instructions throw it off?"

**(a) 교차 리뷰의 비대칭 — 이 리서치에서 나온 가장 정직한 관찰** `[출처 명확 — 자기 반증 포함]`

- Ok_Economist3865(2026-03-17):
  > "Heavy CC user here, around 2 months ago, i started using codex as well. Just out of curiosity I started using gpt 5.2 xhigh to review opus 4.5/4.6 code against a small task. **Almost 90 percent of the time, I found critical issues.** After a month I got tired and realized that **there has to be something wrong with my prompts.** Visited anthropic official prompt engineering guideline for opus 4.5/4.6, improved my prompts. **Now 5.2xhigh review results into 25-40 percent issues, down from 90.** Then one day I tried the reverse, how about gpt 5.2xhigh codes and opus reviews but nope, **opus says no critical and high issues.**"
  - **책 활용 (강력):** 커뮤니티에 널리 퍼진 "Codex로 리뷰하면 Claude 코드에서 문제가 쏟아진다"는 서사가 **절반은 프롬프트 문제였다**는 자기 검증. 90% → 25~40%. 그리고 남은 비대칭(역방향은 안 잡힘)도 함께 기록돼 있다. 선행 문서 §2-1("코드 리뷰는 Codex"는 논쟁이 거의 없다)에 필요한 **유일한 정량적 단서이자 유일한 자기 반증**.

**(b) 훅(Hooks) — CC에서 넘어와 가장 먼저 비는 자리**

- tom_mathews(2026-03-17): "Totally agree on the hooks feature. **It is big feature that I miss from CC**"
- fredjutsu(2026-03-18): "**CC is unusable without hooks if you're doing professional work**"
- kknow(2026-03-18) — 잃는 것이 구체적으로 무엇인지: `[출처 명확 — 업무 맥락·수치 제시]`
  > "I automated my flow and use hooks to run **heavily restrictive linters or scripts which contain specific reviews**. After I run a flow that implements a feature I have to change code afterwards maybe **30% of the time** depending on the complexity of the task. I am using this flow on **enterprise level code** so we strictly enforce code rules, security reviews, code reviews etc. 30% is way down from like half a year ago now."
- Ok_Economist3865(2026-03-17): "P.s just checked **hooks released as experimental feature in recent update**." → 2026-03 중순 시점에 실험적 기능으로 출시. 선행 문서 §마찰 5(#21753 패리티 트래커, 2026-05-08)와 시간축이 맞물린다.
- Neither-Phone-7264(2026-03-27): "now mcp and skills :D" → 이 시기에 기능이 빠르게 붙고 있었음.

**(c) "정찰하는 장인" 서사에 대한 정면 반박** `[익명 주장·확인 필요 — 다만 코드베이스 성격을 특정]`

선행 문서 §2-2(AWS 한국 블로그)는 "Codex = 정찰 후 패치하는 장인 / Claude = 단일 패스 작성자"로 정리했다. 레거시 코드베이스에서는 정확히 뒤집힌다는 보고.

- imperfectlyAware(2026-04-24), macOS/Swift/레거시 Objective-C:
  > "It's the reverse for me and my code base (macOS, swift, legacy objective-c). **Codex is good at criticizing my code base, but when it actually implements stuff, it just follows its own nose, replicates existing functionality and ignores existing patterns.** My products use my own hand developed, interlocking frameworks and it just produces **GitHub tutorial code** instead. So instead of writing the right 10 lines of code to drive my frameworks, it comes back with **hundreds of lines that it shivs into the wrong places.** CC goes off and looks at how I have solved similar problems before, works out how those work, and comes back with 'good news! This is a small change, you've already done the hard work!'"
- 같은 사용자, 같은 날 — 선행 문서 §4 논쟁 D(rednb: "Claude가 허락 없이 너무 빨리 실행")의 **시간 역전**:
  > "It is starting to go off and **default to doing stuff when I'm still chatting** trying to find the right solution. **CC used to be terrible at that (let's code!), but has gotten more patient.**"
  - **책 활용:** "어느 쪽이 성급한가"조차 버전에 따라 자리를 바꾼다. 선행 문서의 판정 유보를 강화하는 1차 증거.

**(d) 지시 준수 — Codex 쪽에서도 회귀를 인정** `[익명 주장·확인 필요]`

- sebstaq(2026-03-17):
  > "In general I think it adheres better to instructions. **Though, it has regressed a bit in that area. It's not as strict in following agents.md and implementation plans anymore. Claude on the other hand has improved in those areas. So they've become more alike.** ... **Codex writes extremely defensive code. To an extent that it often is dangerous.** Also **struggles immensely with cutting away code.** Though, Claude has the same struggles. It's not as noticeable when you vibecode obviously. But at work, when I rather carefully look at each line of code."
- ImagiBooks(2026-03-18) — 양쪽 다 안 지킨다는 쪽:
  > "I have in my **CLAUDE.md and AGENTS.md** rules on fallbacks are NEVER allowed without the user approval, errors can NEVER be swallowed, I have react hooks rules. **Yet they are barely followed it's so exhausting.** ... So after it was done implementing a few complex frontend files I insisted to run the react hook audit skill. And **it found an average of 5 hooks per file not needed / problematic.**"

**(e) 영역별 강약 — r/codex 안에서도 프론트엔드는 Claude로 합의**

- Vanillalite34(2026-03-17): "Generally the back end code is better, I prefer the Codex App, and they are 1000 times more generous with tokens. **Claude dunks on Codex from on high with regards to front end UI/IX.**"
- mar_floof(2026-03-17): "Yeah, it's really not even fair. Comparing the two for front end work. If you need a simple crud hi codex can get you there, but **anything else and Claude Code just blows it away**"
- inteligenzia(2026-03-18) — 가장 구조적인 정리:
  > "GPT models are good at thinking through **small details it has context of**. ... **Claude is much more disagreeable and can zoom out.** I think that is quite valuable **but at conceptual phase. Not later.** You can do that with GPT too, but it requires you asking this question. However it's much harder to ask Claude connect small dots."
- binotboth(2026-03-26) — 한도 기반 스위칭 루틴: "Then my CC rate limit hits and **that's when I switch over to codex, but I deliberately scope individual issues for it to work on that have a small surface**"

---

### 1-2. 핵심 스레드 ②: "$200끼리 붙여서 Claude → Codex 전환"

**출처:** /u/Perfect-Series-2901, r/codex, **2026-04-29**, 댓글 74개
https://www.reddit.com/r/codex/comments/1sz7l0l/switch_from_claude_to_codex_both_200_tier/

⚠️ **강한 진영 편향 스레드.** OP 본인이 스레드 안에서 "마케팅 아니냐"는 비난을 받았다고 인정하며 비꼬는 답을 남긴다. 그럼에도 **Codex 옹호자 본인이 인정한 Codex의 약점**이 나와 인용 가치가 높다.

- **Codex 옹호자가 인정한 CLI 열세** — Perfect-Series-2901(OP 본인):
  > "I have to agree tho, **for the CLI tools, Claude is much much better then codex.** But all this doesn't really matter if the model is a smartass but does not deliver..."
  - **책 활용:** 선행 문서 §4 논쟁 D는 "Claude Code TUI가 버그가 많다"(tlonny)만 실었다. 반대 방향 증언이 **Codex 진영 한복판에서** 나왔다는 점이 균형을 잡아 준다.
- **추론 vs 지시 준수의 분업** — spencer_kw(2026-04~05):
  > "i run both. **claude infers what you want better, codex follows instructions better.** different strengths."
  - 반박 — lemawe: "What you describe is just an impression **because Claude is more talkative than Codex**, but Codex always implement better, even if the plan doesn't look as detailed as Claude's."
  - 재반박 — spencer_kw: "Claude can be **brutally wasteful but will more preventatively not do anything stupid**, where as **Codex just does what you want but doesn't always infer the risks** as thoroughly."
- **5시간 캡을 우회하려고 두 구독을 동시에 돌린 사례** — HouseCommercial8583 `[익명 주장·확인 필요 — 조건 일부 명시]`:
  > "I ran **two parallel subscriptions for Codex and Claude for a month so that I can beat the 5-hour cap.** I had more bugs to solve whenever I switched to Claude than when on a Codex session."
  > (후속) "When Claude is **hitting limit within 20 minutes** or so, I am going for **1.5 hours with Codex** just to achieve the same amount of work, **on the 5.4 Medium which is equivalent to Sonnet 4.6.**"
  - ⚠️ 게시일 2026-04-29 스레드, 정확한 댓글 시점은 2026-05~06 사이. **2026-06-16 급등 이전** 데이터로 취급할 것.
- **토큰 배수 체감(2026-04-29 기준)** — Perfect-Series-2901: "my number is about **200% or 250% (i.e. 100% to 150% more) on opus**" — 같은 작업에 Opus가 2~2.5배 토큰. `[익명 주장·조건 불명]`
- 2Norn(2026-04-29경): "**$100 codex feels better than $200 claude in terms of usage limits**, let that sink in." `[익명·체감]`
- wgaca2: "**Claude can fix ui issues that codex loops on for hours.** But anything else codex appears to be better"
- patriot2024: "**You can use Claude skills and subagents with Codex.**" — 마이그레이션 실무자 진술(구현 방법은 미제시, 확인 필요)

---

### 1-3. "한도 때문에 갈아탔다가 그날로 돌아온" 사례 — 챕터 오프닝 최상급 소재

**출처:** /u/maraluke, r/codex, **2026-04-10** `[익명 주장·확인 필요 — 다만 자기 모순을 그대로 노출]`
https://www.reddit.com/r/codex/comments/1shacwd/i_switched_from_claude_code_to_codex_due_to_much/

제목: "I switched from Claude Code to Codex due to much higher rate limit". 본문 전문:

> "I was hitting 5h limit all the time with claude but Codex never gave me limit warning and the auto compact was very smooth and the Codex app is really nice so I just stop using Claude Code all together. **And today I just melted my 5h limit with 3 prompts** (probably due to superpower and plan mode). **Guess what, I'm switching right back to Claude Code lol.**"

- **책 활용 (최상급):** 게시일이 **2026-04-10**이다. 선행 문서 §3-4(b)가 잡아낸 "2026-06-16 한도 급등" **두 달 전**에 이미 "Codex 한도는 무한하다"는 통념이 개인 단위에서 깨지고 있었다는 증거. 제목과 본문이 한 게시물 안에서 서로를 반박한다.
- 선행 문서 §4 논쟁 E의 "구독 유목민 피로"(skageektp)를 영어권에서 재현한 사례이기도 하다.

---

### 1-4. 전환자 본인이 정리한 "덜 다듬어진 느낌"의 정체

**출처:** /u/Glittering_Bid_7281, r/codex, **2026-04-24** `[익명 주장·확인 필요 — 도메인·도구 명시]`
https://www.reddit.com/r/codex/comments/1su27hw/i_recently_switched_from_claude_code_to_codex/

사회과학 연구자(R/STATA/Python, 대형 행정 데이터). **소프트웨어 엔지니어가 아닌 전환자**의 목소리라 희소하다.

> "i left claude code because token limits were starting to bind (**even on a 100$ plan**), and i am very happy with codex's relative performance in this regard. the way i use it, i will never run out of tokens: **even after a very intense session, i have used 10% of tokens**
> however, there are some aspects of codex that i don't love. some of these are merely stylistic (**i find it quite verbose and long-winded**) and others are substantive (**it makes some stupid mistakes, sometimes 'stupider' than what claude would make**)
> ... my sense is that **codex can be as good as claude, but is a bit rougher straight out of the box** (probably because OpenAI didn't invest in making it as user-friendly)"

- 날짜 필수: **2026-04-24** 기준 "$100 플랜에서 한도가 조이기 시작", "격한 세션에도 10%".

---

### 1-5. "모델 우열이 아니라 워크플로 문제다" — 프레임을 바꾼 스레드

**출처:** /u/TheBanq, r/codex, **2026-06-12** `[익명 주장·확인 필요]`
https://www.reddit.com/r/codex/comments/1u3q06l/the_real_difference_between_codex_claude_code/

> "Everybody is arguing about which model is 'better', while overlooking the most important thing: **Use-case and workflow!** ...
> - **Codex needs more guidance, but is much more (by far) efficient in terms of time & tokens.**
> - **Claude Code is much better at structuring itself and be given a more broad task.**
> ... If you want to let the AI run through your code and '**optimize everything**', very broad performance audit, then **Claude Code will be much better** at that. If you want to implement a **well thought out feature, with clear specs and implementation plan**, then **Codex will make much more sense**.
> ... **But If you have a lazy workflow and don't really like to plan a lot** (which you should btw), **then Claude Code will probably perform much better.**"

- **책 활용:** 선행 문서 §4 논쟁 A("협업이냐 위임이냐")를 한 단계 정밀화한다. 선택 기준이 **"당신이 명세를 얼마나 써 주느냐"**로 바뀐다. 이 문장은 챕터 결론부 소재로 쓸 만하다.

---

### 1-6. 역방향 전환 — Codex → Claude 재구독 후기 (균형용)

**출처:** /u/DaC2k26, r/codex, **2026-06-24** `[익명 주장·확인 필요 — r/codex 게시, 진영 편향 주의]`
https://www.reddit.com/r/codex/comments/1ue06me/i_resubbed_to_claude_code_and_realized_i_was/

> "after being away from Claude for about four months (basically since the Opus 4.6 era), I resubscribed today ... What surprised me most was that one of the prompts I use in my agentic workflow—a prompt that DeepSeek V4 Flash, MiniMax, Codex, and Composer have never failed to understand—**completely confused Opus.** Instead of executing the task, it responded with: '**There's nothing being asked here, so there's nothing to do.**' The prompt contained a link to a document with multiple clearly defined requests. Opus didn't even bother reading it."

---

### 1-7. r/ClaudeAI 쪽(반대 진영) 1차 자료 — 편향 교정용

**(a) 자체 코드베이스 벤치마크** — /u/sergeykarayev, r/ClaudeAI, **2026-02-06**
https://www.reddit.com/r/ClaudeAI/comments/1qxr7vs/gpt53_codex_vs_opus_46_we_benchmarked_both_on_our/
`[출처 명확 — 방법론 공개 / ⚠️ 이해충돌: 자사 제품 Superconductor 홍보 포함]`

> "our codebase is a Ruby on Rails codebase with Phlex components, Stimulus JS ... **We selected PRs from our repo that represent great engineering work. An AI infers the original spec from each PR (the coding agents never see the solution).** Each agent independently implements the spec. **Three separate LLM evaluators (Claude Opus 4.5, GPT 5.2, Gemini 3 Pro) grade each implementation** on correctness, completeness, and code quality — no single model's bias dominates.
> **GPT-5.3 Codex: ~0.70 quality score at under $1/ticket. Opus 4.6: ~0.61 quality score at ~$5/ticket.**"

- ⚠️ 인용 시 필수 표기: (1) **2026-02-06**, GPT-5.3 / Opus 4.6 세대 — 2026-08 기준 두 세대 이상 낡음. (2) 채점자가 LLM 3종. (3) 가격은 "GPT 5.2와 동일 API 가격 가정"이라는 저자 스스로의 단서 위에 있다. (4) 게시자는 벤치마크 제품 판매자.
- **그럼에도 인용 가치가 큰 이유:** 선행 문서 §8-3이 지적한 "동일 태스크·동일 조건 벤치마크가 없다"는 공백을, **방법론이 공개된 형태로** 메우는 유일한 자료다. Claude 서브레딧에 올라온 Codex 우세 결과라는 점도 편향 방향이 반대다.

**(b) 병렬 오케스트레이션 실전 레시피** — /u/99xAgency, r/ClaudeAI, **2026-04-24** `[익명 주장·확인 필요 — 절차는 구체적]`
https://www.reddit.com/r/ClaudeAI/comments/1su7r02/claude_codex_excellence/

> "I have a 20x Claude account and have been using Opus 4.7 exclusively for all code. I noticed **even after asking multiple times to do code review, Opus would still not get there 100%.** Here is what I did:
> - Installed Codex cli and ran it in a **Tmux session**
> - Claude created **PR for Codex to review**
> - Claude **pinged Codex via shell** so I can see the Codex thinking and approve any file permission
> - Claude set a **wake up window**
> - Codex reviewed and updated comments in PR. Claude woke up and validated the comments before editing code.
> **Surprisingly Claude missed a lot of things and it was worth having Codex do the review.**"

- 선행 문서 §노하우 5(교차 리뷰)의 **실행 형태를 처음으로 구체화**한 1차 자료. tmux + PR + wake-up window.

**(c) 원인 규명형 전환 후기** — /u/Joozio, r/ClaudeAI, **2026-04-23**
https://www.reddit.com/r/ClaudeAI/comments/1stfc4t/opus_47_made_me_resubscribe_to_codex_after_two/

> "I cancelled ChatGPT Pro in February. For two months Claude Max 20x was covering everything ... Last week I renewed Codex at $200/month on top of Claude. **Opus 4.7 is the reason.** Here is what I noticed in my own sessions after the April 17 launch:
> - The model **reads 6 files instead of 60** before editing
> - **Full-file rewrites replacing surgical edits**
> - More questions from the model, less committed work
> - Instructions I pre-specified in the prompt getting ignored
> **I spent a week assuming it was my setup.** Cleaned up my CLAUDE.md. Shortened my memory file. Tested my skills. **Nothing moved the needle.** ...
> The honest caveat I owe 4.7: **at max reasoning it comes back.** ... But **max burns usage 3-4x faster in my setup. Weekly ceiling hits Tuesday instead of Friday.** I am not paying for a more capable model, **I am paying more to reach the capability that used to be the default.**"

- **책 활용:** "내 설정이 문제인 줄 알고 일주일을 태웠다"는 전환자의 전형적 함정. 선행 문서 §마찰 3(오래된 불만은 이미 고쳐졌을 수 있다)의 **거울상** — "새로 생긴 문제를 내 탓으로 오진한다".
- ⚠️ **미검증 부분:** 같은 글은 "Stella Laurenzo(AMD AI 시니어 디렉터) 팀이 Claude Code 세션 6,852건 / 툴 콜 234,760건을 분석해 Read:Edit 비율이 6.6 → 2.0(-70%)으로 떨어졌다"는 GitHub 이슈를 인용한다. **원 이슈를 직접 확인하지 못했다.** `[2차·미검증 — 책에 쓰려면 원 이슈 URL 확보 후에만]`

**(d) 요금제 구조 변화의 기록** — /u/Coolpop52, r/ClaudeAI, **2026-04-21**
https://www.reddit.com/r/ClaudeAI/comments/1ss3asp/does_claudes_20_plan_no_longer_include_claude_code/
> "Was looking at buying the $20 Plan today (and wanting to switch/try my options from Codex), but **saw that Claude Code was not included.**"
- /u/Virtual-Economist127, r/ClaudeAI, **2026-06-23** https://www.reddit.com/r/ClaudeAI/comments/1ud388h/the_20_100_gap_is_pushing_solo_power_users_to/ : "Pro at $20/month doesn't cover my daily volume. ... But **Max at $100 is a 5x jump with no middle ground. So I split: $20 on Claude Pro + $20 on ChatGPT/Codex** to get through the day."
- **책 활용:** "왜 다들 둘 다 결제하는가"의 **가격표 층위 설명**. 선행 문서 §4 논쟁 E가 관찰만 했던 현상의 원인.

---

### 1-8. 최신 세대(Sol/Fable) 비교 — 지시 준수 논쟁이 또 뒤집힌 지점

**출처:** /u/vanbrosh, r/codex, **2026-07-10**, 댓글 31개
https://www.reddit.com/r/codex/comments/1usogxo/in_our_benchmark_the_20_codex_plan_with_sol_56/

제목 주장: "$20 Codex 플랜의 Sol 5.6이 $20 Claude Code 플랜의 Fable 5보다 평균 난이도 개발 태스크를 **2.2배** 더 완료했다."
⚠️ `[2차·이해충돌]` 게시자는 자체 에이전트를 개발하는 쪽이고, 벤치마크 구성(Terminal-Bench Hard 2.1, SciCode, ITBench-AA, APEX-Agents-AA, IFBench, AAII)은 본인이 밝혔지만 **2.2배 수치의 산출 절차는 공개되지 않았다. 이 수치는 책에 쓰지 말 것.**

정작 값진 건 댓글의 성격 규정과 **정면 충돌**이다.

- **관점 A** — NootropicDiary(2026-07-10):
  > "**Fable is like an unpredictable wild genius** that can have flashes of stunning intelligence, is super proactive but **can equally spawn 20 agents and waste a bunch of tokens**. **Sol is the dependable, precise, efficient workhorse** but it shows less creativity and follows things more rigidly. Now, I know, it sounds good following things rigidly, but **Fable thinking outside the box and suggesting directions I didn't prompt has actually proven very useful** to me."
- **관점 B** — xoStardustt(2026-07-11), 정확히 반대:
  > "i feel like it's actually the opposite, **Sol tends to go apeshit and refactor half my code without me prompting it to do so (and even with an agents.md that explicitly forbids cleanup/refactor if it's out of scope).** Fable and even opus are both much better at following instructions and finding relevant issues"
- **한도 관련(날짜 필수, 2026-07-11)**:
  - Historical_Bus_8041: "I just wish **Sol didn't seem to burn through tokens even faster than Fable.**"
  - runfence: "Claude monthly value doesn't scale x4 with x5 to x20 subscription. **Actual scale is ~x1.8.** The x4 difference is only for 5h limit." `[익명 주장·확인 필요 — 계산 근거 미제시]`

- **책 활용:** 선행 문서 §4 논쟁 B의 "판정 유보"가 **최신 세대에서도 유효**하다는 증거. 같은 스레드, 하루 차이, 정반대 진술.

---

### 1-9. 현장 노하우 모음글 (가장 신선)

**출처:** /u/Immediate_Honey_1185, r/codex, **2026-07-26** `[익명 주장·확인 필요 — 저장소 링크 제시]`
https://www.reddit.com/r/codex/comments/1v7cvw6/from_a_dev_who_tried_it_all_how_to_actually_get/

- "Don't use codex in the app, **use CLI**"
- "Don't use the default CLI (harness), use **oh my pi**" — https://github.com/can1357/oh-my-pi/
- "**Pair.** ... checking the slop with alternative LLMs was the best way to filter the cap out. ... Pair Codex + Kimi k3, Codex + Opus 5 (or Fable), Codex + GLM, any will do better. **Even 5.6 Sol + 5.5 can work, though if a model has completely different weights it's better imo.**" ← 선행 문서 §노하우 5(교차 리뷰: 다른 계열은 맹점이 다르다)의 커뮤니티 재확인
- "**Avoid building a monolith.** Split, keep code redundant, component-based, re-usable, and **keep resetting sessions** (/clear or whatever)."
- "**Don't work on prod. Don't give SSH access.**"

---

### 1-10. ⭐ 핵심 스레드 ③: "최근에 Claude에서 Codex로 옮긴 분?" — 전환 동기의 표본

**출처:** /u/alOOshXL, r/codex, **2026-05-12**, 댓글 91개
https://www.reddit.com/r/codex/comments/1tao42q/did_anyone_here_moved_from_claude_to_codex/

본문이 제목 한 줄뿐이라 **댓글 전체가 곧 자료**다. 전환 동기가 어디에 몰려 있는지 가장 잘 보여 준다. ⚠️ r/codex 게시 — 진영 편향 강함. 아래는 **반복 패턴**과 **소수 반대 의견**을 함께 옮긴 것이다.

**(a) 압도적 1순위 동기는 "지능"이 아니라 "한도"** `[익명 다수 집계 — 2026-05-12 기준]`

- someRandomGeek98: "**Main reason is usage limits**"
- TimelyCard9057: "I mean **we don't even get to the quality discussion if I just get blocked due to usage limits** after a few chats"
- Grouchy_Yellow_8414 — 품질은 Claude 손을 들어 주면서도 옮긴 사례:
  > "**I find claude is faster and often provides a higher quality of work in most coding tasks. But I use Codex because I can get further with my money** than with Claude which is quick to burn through your wallet."
- CalvinBuild: "Because **$20 claude sub can't complete a single solid prompt within usage limit.**"
- DROP_TABLE_IF_EXISTS — 컨텍스트 재적재 비용:
  > "Worst thing is when Pro plan's 5 hour limit runs out late at night, so you close the PC and **have to continue in the same chat next day and after the first prompt it consume 20% of that 5 hour window.**"
- alOOshXL(OP) — 마케팅 문구의 함정:
  > "They said '**we are 2x rate 5hr window limits**' and everyone mind blow up. **Not knowing that weekly limit is the same**"
- **책 활용:** 선행 문서 §3-4가 요금·한도를 "함정" 섹션에 넣었는데, 이 스레드는 **한도가 전환의 1차 동인 자체**임을 보여 준다. 2026-05-12라는 날짜를 반드시 붙일 것.

**(b) ⭐ 가장 정확한 성격 대조 — 한 문장으로 정리된 트레이드오프** `[익명 주장·확인 필요 — 다만 이 문서에서 가장 많이 재확인된 관찰]`

- PinEnvironmental6395(2026-05-12):
  > "GPT-5 is very good at doing what you say. **But if you don't tell it what you want it won't do it.** It's the **opposite tradeoff Claude makes** — it's good at figuring out what you want **but at the cost of doing things you didn't want it to do.** **You have to prompt gpt to be proactive and Claude to be non-destructive.**"
  - **책 활용 (최상급):** 마지막 한 줄이 이 책의 한 챕터를 통째로 요약한다. §1-5(TheBanq), §1-2(spencer_kw "claude infers better, codex follows better"), §1-8(Sol/Fable 논쟁)이 전부 이 축의 변주다. **선행 문서 §4 논쟁 A·B를 하나의 프레임으로 합치는 문장.**
- 같은 축의 다른 표현들:
  - someRandomGeek98: "**codex is more thorough, catches bugs that opus doesn't. but opus is way more creative.**"
  - Corv9tte: "OpenAI has been **utterly obsessed with token efficiency since GPT-5. It tries to read as little as possible, and that makes it unreliable** yeah. Yes, you can system prompt your way out of this and patch the blindspot at least somewhat. ... Feels like at least in the near future **coding harnesses are going to be more and more important** to extract more value from AI models." `[익명·인과는 추정]`
  - tuhdo: "**Better to follow or wait for your instructions, than outright disobey.**"
  - TySocal: "Opus is talking too much. It's like this annoying product manager who always wants to do meetings ... **GPT just gets shit done.**"

**(c) ⭐ 구체적 전환 마찰 사례 — 모노레포 안드로이드 빌드** `[익명 주장·확인 필요 — 상황·명령 특정]`

- Exerionx(2026-05-13), Claude Code Pro를 새로 시도한 Codex 사용자:
  > "I recently switched my repo to a **monorepo** and moved stuff around which **broke my Android mobile build with `pnpm expo run:build`**. I asked Claude I'm having build issues, '**please diagnose and fix**'. **Asked me to copy and paste the error, so I did. Fixed it. Then another error, repeat…** Codex was literally just '**My Android build command is broken pls fix**' and it **fixed every gradle issue until the build was successful — constantly iterating and checking each time.** Am I missing something here or is CC just like this? Was using 4.6"
  - **책 활용:** "조용히 알아서 끝까지 간다"(선행 §2-3 Naresh B A)의 **구체적 장면**. 반복 루프를 사람이 릴레이해 주느냐, 에이전트가 스스로 도느냐의 차이.

**(d) ⭐ 전환의 실제 경로는 "갈아타기"가 아니라 "리뷰부터 슬금슬금"**

- cl0wnb0x(2026-05-12) `[익명 주장·확인 필요 — 경로가 구체적]`:
  > "I've **slowly transitioned from cc to codex over the last couple weeks.** Heavy daily user of the max cc plan and **I never had usage limit issues with it.** What got me to make the full switch was anthropic models genuinely feel like they're getting worse with each new release. **Started using codex for reviews of cc work. Then as I got more familiar with codex cli I just kept using it more and more.**"
  - **책 활용 (강력):** 선행 문서 §2-1("코드 리뷰는 Codex")과 §4 논쟁 E("둘 다 쓴다")를 잇는 **전환 경로의 표준형**. 리뷰 → 익숙해짐 → 주력. 한도 때문이 아니라고 본인이 명시한 점도 귀하다(위 (a)의 반례).
- Hegemonikon138(2026-05-12): "using codex just feels.. **Refreshing. I'm finding using it has less friction then Claude but I'm leaning towards having Claude stick with high level planning and UI design.**"
- Intrepid_Travel_3274: "**Im still paying both**"

**(e) 모델이 아니라 앱/하네스가 결정했다는 소수 의견**

- Complex-Concern7890(2026-05-12) `[익명 주장·확인 필요 — 비교 대상 다수]`:
  > "I have been using both daily plus K2.6/GLM5.1. ... **I really can not say if GPT5.5 is better than Opus4.7 in my use cases** as the results seem to be good enough with both (even with K2.6 usually is good enough for me). **But what is definitely better for me is the codex app. It just feels good to use and that is the main reason why I seem to use codex more than claude nowadays.**"
- onlyrealcuzzo(2026-05-12): "Claude Code is great, but it's ***SLOW AS HELL***. The phone app is great, but **it constantly gets frozen** ... Codex is good enough and WAY faster, and it rarely gets frozen."
- **선행 문서 §4 논쟁 D 보강:** CLI/앱 품질에 대한 평가가 **양방향으로 갈린다**(§1-2의 "CLI는 Claude가 낫다"와 정면 대립). 진영이 아니라 **플랫폼(모바일 앱 vs 터미널)**에 따라 갈리는 것으로 보인다.

**(f) 반대 방향 소수 의견 (같은 스레드 안에서)**

- projohnz(2026-05-14): "**I actually switch from gpt to claude and i think the opposite, Codex thinks it knows better than you what you need**"
- GTHell(2026-05-12): "At this point of time, **both are equally top tier and can get job done**"
- bigrealaccount: "**Claude is great for a second opinion** on whatever you're writing because usually its reasoning is a bit better imo, but codex usage is just way better"

⚠️ **이 스레드의 편향 경고:** "Anthropic이 모델을 로보토미했다/사기다"류의 감정적 주장(Corv9tte, mrjbelfort, Specialist-Buffalo-8 등)이 다수다. **어느 것도 근거 제시가 없다.** 인용하려면 "r/codex의 정서"로만 다뤄야 하고, 사실 주장으로 옮기면 안 된다.

---

## 2. 한국어 후기

**결론부터: "Claude Code를 쓰다가 Codex로 옮겨서 이런 데서 넘어졌다"는 한국어 1차 전환 마찰 후기는 2026-08-02 기준 여전히 희소하다.** 선행 리서처의 판단(§8-3)은 **대체로 유지**되지만, **한 건의 중요한 예외**를 찾았다.

### 2-1. ✅ 예외: 중첩 AGENTS.md 마찰의 한국어 1차 증언

**출처:** 코유키1357, 디시인사이드 "특이점이 온다" 마이너 갤러리, **2026-04-28 18:53**, 조회 7,507 / 추천 11
제목: **"월 40만원 써가며 작성한 클로드와 코덱스 사용 후기(장문)"**
https://gall.dcinside.com/mgallery/board/view/?id=thesingularity&no=1149110
`[익명 주장·확인 필요 — 익명 갤러리, 다만 사용 환경·비용을 구체적으로 명시]`

사용 환경(본인 기술): 풀스택. 백엔드 10만 줄 이상 / 400개 파일, 프론트엔드 5만 줄 이상 / 600개 파일, 유니티 게임, 회계 업무. Claude Pro + GPT Plus 동시 구독, API 병행.

**핵심 인용 (원문 그대로):**
> "클로드의 경우 **rules라는 기능을 통해 반복 실수하는 부분을 rules로 작성하여 반복 작성하는 문제를 해결할수있어서**"
> "**코덱스의 경우 hook은 있는데 rules가 없어 각 폴더 루트마다 AGENTS.md를 작성해야하고 이로 인해 프롬프트 관리가 까다로워지는 문제가 있음**"
> "**GPT의 경우 코드를 전부 다 읽지 않고 수정하는 문제가 있어서 코드가 중복되는 문제가 발생함**"
> "API로 사용했을때 **질문 하나마다 2달러 안되게 비용이 들었음**"

- **책 활용 (최우선):** 선행 문서 §마찰 2(중첩 AGENTS.md 미로딩, GitHub #12115)를 **한국 개발자가 자기 말로 겪고 기록한 유일한 사례**다. "각 폴더 루트마다 AGENTS.md를 작성해야 한다"는 문장은 #12115의 leonardo-panseri 댓글("서브디렉토리에서 CLI를 열라는 건 대부분의 프로젝트에서 비현실적")과 **독립적으로 같은 지점에 도달**했다. 한국 독자 공감 포인트를 여기서 만들 수 있다.
- ⚠️ **용어 주의:** 글쓴이가 말한 "rules"는 Claude Code의 공식 기능명이 아니다(CC는 CLAUDE.md/메모리·설정 체계). Cursor의 Rules나 CC의 메모리 파일 계층을 통칭한 것으로 보인다. 인용 시 이 점을 밝히거나 원문 표현임을 명시할 것.
- ⚠️ **비용 수치:** "질문 하나당 2달러 미만"은 조건(모델·토큰·기간) 미기재. 날짜(2026-04-28)와 함께만 인용.

### 2-2. ✅ 한국어 클린룸 대조 실험

**출처:** Sean(@sean_kk), velog, **2026-02-13** `[출처 명확 — 절차·소요시간 명시 / 단일 태스크·주관 명시]`
"GPT Pro Codex vs Claude Code: 클린 환경에서 붙여본 지극히 주관적인 비교"
https://velog.io/@sean_kk/GPT-Pro-Codex-vs-Claude-Code-클린-환경에서-붙여본-솔직-비교-ebs0gvya

- 절차: 같은 프롬프트로 웹 게임 PRD.md 생성 → 빈 프로젝트에서 각각 구현.
- 결과: **Claude Code 9분 — 오류 없이 동작, 디자인 무난.** **Codex 26분 — 세련된 디자인, 그러나 오류 발생 + 게임 동작 불일치.**
- 교차 실험: Codex가 만든 PRD를 Claude에 주면 오류 없이 동작하되 디자인은 평범.
- 저자 결론: "문서/기획/요약 **Codex 우세**", "코드 안정성 **Claude Code 우세**", "디자인 감성 **Codex 압승**" → **"문서를 만들고 설계도를 그리는 단계는 Codex, 그 설계도를 실제 코드로 옮기는 단계는 Claude Code"**
- ⚠️ 단일 태스크(수박게임 클론) 1회 시행. 모델 세대 2026-02 기준. **일반화 금지.**
- **주목:** 이 결론은 §1-7(b)·선행 문서 §노하우 5의 "Claude 구현 → Codex 리뷰"와 **역방향**이다. 한국·글로벌 양쪽에서 분업 방향이 갈린다는 것 자체를 논쟁으로 병기할 만하다.

### 2-3. ✅ Codex 앱 한국어 1차 후기 (전환 마찰은 없음)

**출처:** 김유현(@jujini31), velog, **2026-02-09**
"최근 출시한 Codex 앱 직접 써봤습니다 — Automations·Skills·멀티 에이전트까지"
https://velog.io/@jujini31/codex-앱-사용-후기
`[출처 명확 — 실명 표기, 다만 비교·마찰 서술 없음]`
- Codex 앱(2026-02-02 출시)의 Automations / Skills / 멀티 에이전트 스레드 / Git 연동을 직접 사용한 기록.
- 유일한 마찰 언급: PR 양식이 팀 표준과 다름 → **"평소 작성하던 양식이랑은 많이 달라서 이런 부분을 Skills로 통일시키면 좋을 듯 합니다."**
- Claude Code 비교·클라우드 위임·MCP 설정은 다루지 않는다.

### 2-4. △ 날짜 미확인 / 오래된 한국어 자료 (인용 주의)

| 항목 | 상태 |
|---|---|
| blog.nwlee.com "내가 AGENTS.md를 작성하는 방법" — "Claude Code는 종종 사용량을 초과한 것과 다르게 Codex CLI는 ChatGPT Plus 요금제만으로도 토큰 사용량 초과 걱정 없이 충분하게 활용할 수 있었다" https://blog.nwlee.com/agents-md-guides-to-codex-cli | **게시일 추출 실패.** 한도 관련 진술이므로 **날짜 없이 인용 금지** |
| TILNOTE 설탕사과 "Codex CLI와 클로드 코드 비교 체험기" **2025-09-05** https://tilnote.io/en/pages/68bab2de1e08f5ca788b1c67 — "Codex CLI는 요청한 세부 조건대로 정확히 구현하지 않는 경향", "한국어 프롬프트에 대해 영어 답변 위주로 진행하며, 명령어 해석력이 클로드 코드보다 다소 부족할 때가 있음" | ⏳⏳ **11개월 전.** 모델 세대가 완전히 다름. **"한국어 응답" 이슈는 현행 재확인 없이 인용 금지** |
| dcinside 효도폰만수르 "4.7이후 개발자 체감이 점점 codex로 넘어오는중" **2026-05-17**, 조회 3,049 https://gall.dcinside.com/mgallery/board/view/?id=thesingularity&no=1187798 | **2차.** GeekNews 29576(같은 날)과 동일한 Reddit r/codex 원글의 한국어 릴레이로 보임. 선행 문서에 이미 있는 내용과 중복 |

### 2-5. ❌ 확인 결과 없음 (억지로 채우지 않음)

2026-08-02 검색 기준, 다음에서 **Codex 전환 마찰 1차 후기를 찾지 못했다.**

| 채널 | 결과 |
|---|---|
| **OKKY** | Claude Code 관련 Q&A는 존재(예: "클로드 코드 Pro 쓰시는 분들" https://okky.kr/questions/1545950, 약 2025-11). **Codex 전환·비교 스레드는 검색되지 않음** |
| **회사 기술블로그** (토스·카카오·우아한형제들·당근·라인·네이버 D2) | **0건.** 선행 문서가 확보한 AWS 한국 블로그(Kyutae Park, 2026-06-11)가 여전히 유일한 국내 기업 채널 자료 |
| **커리어리 / 요즘IT / 인프런 커뮤니티** | Codex 소개·비교 아티클은 있으나 **1차 전환 마찰 후기 없음**. 인프런 "클로드 코드 VS 코덱스 비교" https://www.inflearn.com/pages/codex-vs-claudecode 는 편집 콘텐츠 |
| **브런치** | 선행 문서의 kk2daddy(2026-03-14) 외 신규 없음 |

- **판정:** 한국 담론은 **dcinside 특이점갤 → GeekNews → velog/브런치/Threads** 순으로 몰려 있고, 성격은 **"소개·비교"**이지 **"전환 실패담"**이 아니다. 유일한 예외가 §2-1이다.
- **책 집필 함의:** 선행 문서 §8-3의 결론 유지 — **한국 독자용 전환 마찰 서사는 저자 경험으로 메워야 한다.** 다만 §2-1(중첩 AGENTS.md)과 §2-2(구현 안정성 vs 설계)는 "한국에서도 같은 데서 걸렸다"는 근거로 쓸 수 있다.
- ⚠️ **SEO 생성물 경고:** 검색 상위에 잡힌 `treesoop.com`, `litmers.com`, `blog.gridge.co.kr`, `we0.ai/ko`, `wikidocs.net/blog` 계열은 **1차 경험이 확인되지 않는 정리/번역/SEO성 콘텐츠**다. 커뮤니티 자료로 쓰지 말 것.

---

## 3. 클라우드 위임·장시간 작업 실사용기

선행 문서 §8-3이 "목표한 만큼 못 모았다"고 남긴 축. 아래가 이번에 확보한 전부이며, **여전히 "몇 시간짜리 작업을 통째로 맡긴" 상세 후기는 드물다.** 대신 **위임 모델 자체의 성립 조건과 실패 양상**이 잡혔다.

### 3-1. 카테고리 정의 — 이 축의 용어부터 잡아 주는 인용

- simonw(HN, **2026-02-10**) `[출처 명확 — 식별 가능 인물]` https://news.ycombinator.com/item?id=46956015
  > "I like the term '**asynchronous coding agent**', which I define as the category of coding agent which **runs in a container somewhere and files a PR when it's done.** OpenAI Codex Cloud, Claude Code for the web, Gemini Jules and I think Devin are four examples. ... One catch though is that **the asynchronous coding agents are getting less asynchronous.** Claude Code for the web lets you prompt it while it's running which makes it feel much more like regular Claude Code."
  - **책 활용:** "위임"이 카테고리 이름을 얻는 순간의 인용. 그리고 **위임 모델이 다시 협업 모델로 수렴 중**이라는 관찰은 선행 문서 §4 논쟁 A의 이분법에 유통기한을 붙인다.

### 3-2. 성공 사례 — "클라우드만 쓰면 한도를 안 맞는다"

- tcgv(HN, **2026-05-12**) `[익명 주장·확인 필요 — 조건 일부 명시]` https://news.ycombinator.com/item?id=48111615
  > "I'm using a **ChatGPT Plus subscription, and I only use Codex in the cloud**. With this setup, **I have never hit the usage limit.** On my most active days, **I integrate around a dozen fully reviewed and adjusted MRs into my codebase.**"
  - ⚠️ **2026-05-12 기준**. 선행 문서 §3-4(b)의 6/16 급등 **이전** 진술. 현행 확인 필수.
- big_toast(HN, **2026-02-19**) `[익명 주장·확인 필요]` https://news.ycombinator.com/item?id=47080982 — 위임이 성립하는 작업 형태에 대한 관찰:
  > "I started a **golang TUI** last summer with Codex Web/Cloud because **it felt more like a closed loop.** It was able to manage pretty well end to end. **Every additional complexity hop probably increases the attrition rate for successful development**, so TUIs end up the most frequent bean to bar currently possible for hobbyists. I really wanted an iOS app. ... Each additional hurdle (containers, packages, builds, testing, running, OSes, browser integration, computer use) feels like **upping the required power of the models.**"
  - **책 활용:** "클라우드에 뭘 맡길 수 있나"의 답 — **검증 루프가 컨테이너 안에서 닫히는 작업**. 이게 위임 가능성의 실질 기준이다.
- darkblitzrc(r/codex, **2026-05-18**) `[익명 주장·확인 필요 — 구체적 버그 서술]` https://www.reddit.com/r/codex/comments/1tgbb0n/codex_is_a_monster/
  > "I have a React Native app with expo ... when **compiling the app in the cloud to create a preview build**, there was a nasty **duplicate app intent bug** that was driving me insane. I wasted like 1 hour copying the xcode log into chatgpt so i could save some tokens but man that got me nowhere. The real breakthrough came when I said f- it lets use codex. It did not one shot it but the beauty is that **it could run an unsigned build and view exactly where it was failing** and it fixed it after a couple of tries."
  - 같은 원리: **에이전트가 스스로 빌드를 돌려 실패 지점을 볼 수 있을 때** 위임이 통한다.

### 3-3. 실패 양상 ① — 내 설정은 그대로인데 결과가 무너진다

- ModernMech(HN, **2026-07-26**) `[익명 주장·확인 필요 — 대조 조건 명시]` https://news.ycombinator.com/item?id=49057553
  > "the past month I had been **using Codex cloud and it was working great writing Rust modules.** Suddenly last week they made a few changes and **everything went to shit, couldn't get a single good result out of it. Same text box, same prompting, same model, totally different results because they changed the cloud tool's resource limits.** So whereas before my debugging time would have been spent in Rust docs looking up traits and such, these days **I feel more like an AI therapist trying to figure out why it's not feeling up to task on any particular day.**"
  - **책 활용 (강력):** 로컬 CLI와 클라우드 위임의 결정적 차이 — **클라우드는 실행 환경이 공급자 소유라, 내 쪽 변경 없이도 어제와 다른 도구가 된다.** 선행 문서 §3-4(b)(#28879, 로그로 입증된 한도 급등)의 **클라우드 판본**. "AI 심리상담사가 된 기분"은 그대로 인용할 만한 문장이다.
  - ⚠️ 날짜 필수: **2026-07-26** 기준 "지난주" = 2026-07 중순.

### 3-4. 실패 양상 ② — 위임 자체가 좁아진다는 반대 보고

- knuckleheads(HN, **2026-06-09**) `[익명 주장·확인 필요]` https://news.ycombinator.com/item?id=48464767
  > "I feel like **Codex made a big push to run everything on your laptop.** With Claude, I get **4 cpu's, a fair amount of ram and 30gb** for every one of my dumb ideas **for free in the cloud containers. Codex used to be similar, but last time I tried it just kept pushing me to run it locally on my laptop**, which I really did not want to do with 20 requests going at once. That's the main advantage for me at the moment."
  - **관점 대립 정리:** Codex를 "위임형", Claude Code를 "협업형"으로 보는 통념(선행 §4 논쟁 A)과 **정반대의 인프라 층 관찰**. 2026-06 시점 기준으로는 **클라우드 컨테이너 제공에서 Claude 쪽이 더 후했다**는 주장. `현행 확인 필요`

### 3-5. 위임할 것인가, 곁에 둘 것인가 — 관점 A / B

- **관점 A — 위임은 Codex, 곁에 두는 건 Claude:** sidgarimella(HN, **2026-02-05**) https://news.ycombinator.com/item?id=46906476
  > "Many are saying codex is more interactive but ironically I think **that very interactivity/determinism works best when using codex remotely as a cloud agent and in highly async cases.** Conversely **I find opus great locally**, where I can ram messages into it to try to lever its autonomy best (and interrupt/clean up)"
- **관점 B — 클라우드는 조종이 안 된다:** lawrencechen(HN, **2026-02-14**) https://news.ycombinator.com/item?id=47011986
  > "I also personally **prefer running agents locally instead of in the cloud.** For some reason, **it feels easier to steer Claude Code when it's running in my terminal vs steering something in the cloud.** ... Part of it is likely reliability and '**time to first token that AI responded that I can see**.'"
- **관점 C — 남의 클라우드 말고 내 VM:** vardalab(HN, **2026-02-02**) `[익명 주장·확인 필요]` https://news.ycombinator.com/item?id=46863453
  > "I like using Claude or Codex in **VM on top of the tmux**. ... I open a new tmux window for each issue/task big enough to warrant it, issue a prompt to **create a worktree and agents** and let them go to town. **I actually use claude and codex at the same time.** I still get observability because of tmux and **I can close my laptop and let them cook for a while in yolo mode since the VM is frequently backed up in proxmox pbs.** ... Same for cloud. **I want them to support my personal 'cloud' instead of laggy github mess.**"

### 3-6. 클라우드 위임의 보안 경계 — 문서화된 함정

- thewisenerd(HN, **2026-04-22**) `[출처 명확 — 공식 문서·외부 리서치 링크 제시]` https://news.ycombinator.com/item?id=47860452
  > "an 'mitm' tls proxy also gives you much better firewalling capabilities, not that firewalls aren't inherently leaky, **codex's a 'wildcard' based one; hence 'easy' to bypass.** github's list is slightly better but ymmv"
  - 근거 링크: Codex Cloud 인터넷 접근 문서 https://developers.openai.com/codex/cloud/internet-access , 우회 사례 https://embracethered.com/blog/posts/2025/chatgpt-codex-remo... (⏳ 2025년 글)
  - **선행 문서 §3-8(레포가 통째로 올라간 사건)의 짝.** 클라우드 위임은 **네트워크 허용 목록의 정밀도** 문제를 새로 만든다.

### 3-7. 클라우드 과금 정책의 궤적 — 벤더 측 1차 진술 (⏳ 전부 2025년, 배경용)

r/codex에 OpenAI 측 계정 **/u/embirico**가 남긴 공지들. **2026-08 기준 현행 정책이 아니다.** 다만 "클라우드 태스크 과금은 계속 흔들려 왔다"는 **역사 근거**로 가치가 있다. `[출처 명확 — 벤더 자기식별]`

| 날짜 | 진술 | URL |
|---|---|---|
| 2025-10-30 ⏳ | (사용자 보고) 사실상 무제한이던 웹 에이전트에 한도 도입, "**a cloud task will cost x5 credits compared to a local task**" — /u/roundshirt19 | https://www.reddit.com/r/codex/comments/1ok8tt9/ |
| 2025-11-02 ⏳ | (사용자 보고) 가격 페이지에서 "Cloud tasks: **Generous limits for a limited time**" 문구 삭제, 클라우드 쿼터가 로컬과 **같은 풀로 통합**됨. 아카이브 근거 제시 — /u/Available-Space-2919 | https://www.reddit.com/r/codex/comments/1omcgob/ |
| 2025-11-02 ⏳ | **벤더 인정:** "we had a bug where we **overcharged for cloud task usage by ~2-5x**" + "**cloud tasks consume limits slightly faster than local tasks per unit of work, because we have to run the VM** powering the cloud environment" | https://www.reddit.com/r/codex/comments/1om4uce/ |
| 2025-11-04 ⏳ | **벤더:** "When a **cloud task fails, it no longer counts against limits.**" | https://www.reddit.com/r/codex/comments/1onvn1a/ |
| 2025-11-21 ⏳ | **벤더:** "**30% reduction in usage consumption for Cloud tasks specifically.** Running multiple versions of a task (aka **Best of N**) on Codex Cloud is heavily discounted" | https://www.reddit.com/r/codex/comments/1p2k68g/ |

- **책 활용:** "클라우드 태스크는 로컬보다 비싸다 — VM을 돌려야 하니까"는 **벤더 본인 설명**이다. 위임 비용 구조를 설명할 때 이 한 줄이 가장 깔끔하다. 단 **2025-11 시점 발언**임을 반드시 병기.

### 3-8. 남은 공백

- **"몇 시간짜리 작업을 클라우드에 던지고 자리를 비웠다"는 서사 있는 후기는 여전히 못 찾았다.** 성공담은 대부분 **커밋 하나~MR 하나 크기**(tcgv의 "a dozen MRs", big_toast의 TUI)다.
- 선행 문서가 확보한 iBelieve(2026-03-27, "Max 20x인데도 하루 클라우드 스케줄 세션 3개") https://news.ycombinator.com/item?id=47539320 가 여전히 스케줄 위임 관련 유일한 정량 자료.
- **가설(검증 안 됨):** 위임 성공담이 짧은 이유는 §3-2의 big_toast 관찰대로 **검증 루프가 닫히는 크기를 넘어서면 성공률이 급락**하기 때문일 수 있다. 책에서 쓰려면 별도 근거가 필요하다.

---

## 4. MCP 마이그레이션 실전

선행 문서 §8-3은 "Codex 고유의 MCP 팁이 거의 안 나왔고, `.mcp.json` → `config.toml` 실전 마이그레이션 사례를 못 찾았다"고 남겼다. **이번에 실전 사례를 확보했다.**

### 4-1. 두 형식의 대응 — 등가 표현

- mksglu(HN, **2026-02-25**) `[출처 명확 — 실행 가능한 설정]` https://news.ycombinator.com/item?id=47148402
  > "Codex CLI: `codex mcp add context-mode -- npx -y context-mode`
  > Or in `~/.codex/config.toml`:
  > ```toml
  > [mcp_servers.context-mode]
  > command = "npx"
  > args = ["-y", "context-mode"]
  > ```"
- rurban(HN, **2026-03-29**) `[익명 주장·확인 필요]` https://news.ycombinator.com/item?id=47562916 — 마이그레이션의 경계선을 한 줄로:
  > "Regarding skills: **just symlink them.** Since opencode and codex share `.agents/skills` use that for the others also. **Just the hooks and mcp integrations are still proprietary. codex needs a config.toml setting**, but then you can use eg safe-chains everywhere."
  - **책 활용:** "무엇이 이식되고 무엇이 안 되는가"의 커뮤니티 요약. **스킬은 심볼릭 링크로 공유 가능, 훅과 MCP는 각자.**

### 4-2. ⭐ 마이그레이션의 진짜 함정 — MCP를 그대로 옮기면 컨텍스트를 먼저 잃는다

**출처:** /u/buildxjordan, r/codex, **2026-02-11** `[출처 명확 — 실측 수치·설정 위치 명시 / 단일 환경]`
https://www.reddit.com/r/codex/comments/1r22uk1/new_search_tool_is_amazing/

> "There is an experimental feature (for the cli) called '**search_tool**'. You can enable it in the config.toml by adding `search_tool = true` under the `features` section. This feature **eliminates all connected MCP servers and tools from getting injected into the initial prompt at conversation start.** Instead, it allows the model to **search for the required tool and progressively reveals applicable tools** on an as needed basis. For me, that translated into a huge context window reclaim. Admittedly I have **more MCPs than probably recommended (8)** and the initial system prompt + agents.md + mcp context resulted in **sessions starting with 90-91% context remaining. After enabling this feature that changed to 99% context remaining on each session start** which I noticed helped improve model focus on tasks. ... I did update the agents.md to mention this feature to ensure that a search for available MCP tools is done when needed."

- **책 활용 (최우선, 챕터 소재급):** Claude Code에서 MCP 서버 8개를 달고 쓰던 사람이 그대로 Codex로 옮기면, **세션이 시작부터 컨텍스트의 9~10%를 잃은 채 출발한다.** 그리고 그 사실이 화면 어디에도 안 나온다.
- 선행 문서 §3-7의 #18498("스킬/플러그인이 새 스레드 토큰을 부풀린다")과 **같은 병의 MCP 판본**이며, 이쪽은 **해결책과 실측치가 함께 있다.**
- ⚠️ 실험적 기능, **2026-02-11 기준**. 현행 플래그명·동작 재확인 필수.

### 4-3. ⭐ MCP 하나가 시스템을 무너뜨린 두 건 (원인 규명형)

**(a) 메모리 100GB 폭주 — 원인은 "선언되지 않은 MCP로의 폴백"**
/u/ChoasMaster777, r/codex, **2026-03-19** `[출처 명확 — 하드웨어·재현·해결책 명시 / 단일 보고]`
https://www.reddit.com/r/codex/comments/1rxu4ur/if_your_memory_goes_more_than_100gb_during_using/

> "I have experienced **memory keeps growing over more than 100GB** during using codex for multiple projects in the same time. I have tried: Commit files in time ... Kill other apps ... Yesterday I have to **force reboot my mac book pro (48GB, M4 Pro) 4 times.** Finally, I found the root cause: **when `code-index` mcp not available, codex fallback to `rg` during the initialization!** Then I updated my config.toml to
> ```toml
> [mcp_servers.code-index]
> type = "stdio"
> command = "uvx"
> args = ["code-index-mcp"]
> startup_timeout_sec = 60
> tool_timeout_sec = 120
> ```
> Added timeout..."

- **책 활용:** MCP 마이그레이션에서 **"설정이 틀린 것"이 아니라 "설정한 서버가 안 뜬 것"**이 훨씬 조용하고 훨씬 파괴적이다. `startup_timeout_sec`/`tool_timeout_sec`은 CC의 `.mcp.json`에 대응물이 없어 이식 시 빠지기 쉽다.
- 선행 문서 §3-2(macOS가 `rg`를 막는 #28190)와 묘하게 맞물린다 — 양쪽 다 `rg` 폴백 경로가 문제의 축이다.

**(b) 상주 MCP 서버 하나가 Sol을 3시간 멈추게 했다**
/u/tokovar, r/codex, **2026-07-13** `[출처 명확 — 진단 절차·수정 목록 공개 / 인과는 본인도 미확정]`
https://www.reddit.com/r/codex/comments/1uvigpf/is_anyone_elses_codex_gpt56_sol_suddenly/

제목: "Is anyone else's Codex GPT-5.6 SOL suddenly extremely slow? (**3 hours just to ask one clarification**)"

> "UPDATE — RESOLVED FOR ME. ... **I cannot prove one root cause, but my local configuration was clearly an important variable. I disabled the persistent GitNexus MCP server and kept GitNexus through short-lived CLI commands.** I also **removed unused MCPs/connectors**, disabled automatic Security Guidance/Superpowers behavior, **changed follow-ups from queue to steer**, and restarted Codex fully. ... **Codex using 1–1.5 GB RAM was stable and was not the problem by itself.** Other users may have different configurations, so **don't blindly disable the same things.**"

- 같은 글에 **읽기 전용 자가 진단 프롬프트**를 통째로 공개해 뒀다(원문 코드블록 참조). 요지: `~/.codex/config.toml`·AGENTS.md·훅·플러그인·MCP 서버·커넥터·세션 크기·컴팩션·모델/effort·프로세스 트리를 **바꾸지 말고 먼저 조사**시키고, "플러그인과 앱 커넥터는 별개 레이어로 취급", "이름만 언급된 도구와 실제 툴 콜을 구분", "RAM이나 프로세스 수만으로 원인을 단정하지 말 것".
- **책 활용 (강력):** 마이그레이션 트러블슈팅 챕터의 모범 사례. 본인이 **인과를 단정하지 않고**("cannot prove one root cause") **남에게 따라 하지 말라고 경고**하는 태도까지 인용 가치가 있다.
- ⚠️ **2026-07-13, GPT-5.6 Sol 기준.** 매우 신선하지만 그만큼 초기 버그일 가능성.

### 4-4. 플랫폼별 MCP 함정 (Windows·WSL)

- Prestigiouspite(r/codex, **2026-03-07**) `[익명 주장·확인 필요 — GitHub 이슈 존재 언급]` https://www.reddit.com/r/codex/comments/1rn14kz/i_have_run_out_of_patience_for_the_windows_errors/
  > "Then, you select **WSL in the settings, and the very first restart of the app leads to a fatal error.** ... On top of that, there's the issue where **the Windows config.toml is used for WSL, which results in MCP etc. not being configured correctly.**"
  - **선행 문서 §3-3 / GitHub #13762**(WSL 모드가 Windows `CODEX_HOME`을 씀)의 **사용자 측 체감 증언**이며, 그 결과가 **"MCP가 조용히 잘못 설정된다"**임을 명시한다. 선행 문서에 없던 연결고리.
- sublingualwart(r/codex, **2026-06-20**) `[출처 명확 — 재현 절차·에러 문자열]` https://www.reddit.com/r/codex/comments/1ub0j1f/
  > 재현: "Open Codex Desktop with `@chrome`, `@browser`, or `@computer-use` plugin enabled. Run any browser control task ... Observe the error: `**Mcp error: -32602: js: codex/sandbox-state-meta: missing field sandboxPolicy**` Run `codex features list` — see `js_repl removed false`. Run `codex features enable js_repl` — config.toml writes `js_repl = true`. **Restart Codex — js_repl reverts to false.**"
  - **설정이 재시작 때 되돌아간다**는 유형. 마이그레이션 중 "분명히 켰는데 안 켜져 있다"의 한 원인.
- ⏳ **오래된 Windows MCP 팁 (배경용, 현행 확인 필수):**
  - Own_Analyst_5457(2025-10-10) https://www.reddit.com/r/codex/comments/1o34w9o/ — Windows에서는 `command = "cmd"`, `args = ["/c","npx","-y",...]`, `env = { SystemRoot = "C:\\Windows" }` 래핑이 필요했다.
  - shaziyo(2025-11-24) https://www.reddit.com/r/codex/comments/1p59nsg/ — HTTP URL 방식 MCP는 `[features] rmcp_client = true`가 전제였다.
  - AppealSame4367(2025-09-24) https://www.reddit.com/r/codex/comments/1npeego/ — `MCP client for 'chrome-devtools' failed to start: request timed out`의 실제 원인은 Node 버전(20 → 22 필요). **"MCP 타임아웃"은 대개 MCP 문제가 아니다**는 교훈만 유효.

### 4-5. MCP를 비용 절감에 쓰는 패턴 (노하우)

**출처:** /u/petburiraja, r/codex, **2026-05-04** `[출처 명확 — 수치·저장소 공개 / 자기 저장소 홍보 성격 있음]`
https://www.reddit.com/r/codex/comments/1t3ffxe/agentsmd_trick_that_stopped_codex_from_doing_dumb/

> "Spent a Sunday auditing where my Codex tokens were actually going. Half the calls were stuff like 'rename these 12 fields', 'format this csv as markdown table' ... **gpt-5.5 doing janitor work at architect rates.**
> The fix that actually held: pair Codex with a cheap side model and **write the routing rule as a deny list. The deny-list framing matters. Saying 'use the cheap model for X' gets ignored a chunk of the time. Saying 'do NOT use Codex for: bulk reformatting, single-field extraction, classification you'll review anyway' sticks. Codex obeys negative rules better than positive suggestions**, at least for me.
> Setup is **an MCP server with one tool.** Codex calls it via the standard MCP config in `~/.codex/config.toml`. ...
> A week of real numbers from one project: **184 calls offloaded out of ~520 total**; worker side: **$0.34**; estimated avoided Codex spend: **somewhere between $5 and $9** depending on token mix.
> **What stays on Codex:** planning, code that ships, anything touching unfamiliar parts of the repo, anything where wrong output would slip through review."
> 저장소: https://github.com/arizen-dev/deepseek-mcp

- ⚠️ **선행 문서 §4 논쟁 B와 정면 충돌:** pmarreck(2025-12-01)와 toraway(2026-02-26)는 "AGENTS.md 강조 문법·부정 지시는 무용하다"고 했다. 여기서는 **"부정(deny) 지시가 긍정 제안보다 더 잘 먹힌다"**고 한다. **관점 A/B로 병기할 것.** 어느 쪽도 통제 실험이 아니다.
- 선행 문서 §마찰 6(서브에이전트 모델 라우팅 불가)의 **우회로**로도 읽힌다 — 모델 라우팅을 서브에이전트가 아니라 MCP 툴로 구현.

### 4-6. 전환 도구 — 대화 이력 이식

**출처:** /u/builderpepc, r/codex, **2026-06-01** `[출처 명확 — 오픈소스·본인 프로젝트]`
https://www.reddit.com/r/codex/comments/1ttnu8y/you_can_move_chats_between_codex_and_claude_code/ / https://github.com/builderpepc/agent-migrator

> "I found myself wanting to continue a project I had started in Cursor using Claude Code, but **couldn't import my conversations to pick up right where I left off.** ... So, I built a CLI that can **seamlessly migrate your chats between agents with one command.** ... **Currently supports Claude Code CLI, Codex CLI, Gemini CLI, and Cursor IDE.** ... **the hype cycles around which agent/model/harness is the best are shifting all the time.** agent-migrator lets you start your work with one agent, switch to another anytime, and switch back with zero friction."
> 설치: `uv tool install agent-migrator`

- ⚠️ 개인 취미 프로젝트(본인 표기), 미검증. 다만 **"세션 이력이 도구에 묶인다"는 마찰이 실재한다는 증거**로서 가치가 있다. 선행 문서 §마찰 8(설정 마이그레이션이 config를 덮어쓴 #24515)과 함께 "전환 도구 자체가 마찰 지점"이라는 챕터 축을 만들 수 있다.
- 관련: /u/siddhantparadox의 **Codex Manager**(config.toml·스킬·MCP 서버·레포별 설정을 GUI로 관리, 변경 시 diff 미리보기 + 백업 + 원자적 쓰기) — 2026-01-13 최초, 2026-02-03 v1.3.0. https://github.com/siddhantparadox/codexmanager

---

## 5. 선행 `community.md`를 보강/반박하는 항목

| # | 선행 문서 항목 | 이번 자료의 효과 | 근거 |
|---|---|---|---|
| 1 | §마찰 2 — 중첩 AGENTS.md (#12115) | **보강 (한국어 1차 증언 확보)** | 코유키1357, dcinside, 2026-04-28: "코덱스의 경우 hook은 있는데 rules가 없어 **각 폴더 루트마다 AGENTS.md를 작성해야하고** 이로 인해 프롬프트 관리가 까다로워지는 문제가 있음" (§2-1) |
| 2 | §마찰 5 — 훅 커버리지 (#21753, 2026-05-08) | **시간축 보강** | 2026-03-17 시점에 이미 "hooks released as experimental" (Ok_Economist3865). 그 전까지 "CC is unusable without hooks if you're doing professional work"(fredjutsu). 잃는 것의 구체적 형태 = 엔터프라이즈 린터·보안리뷰 게이트, 수동 수정률 30%(kknow) (§1-1b) |
| 3 | §2-1 — "코드 리뷰는 Codex"는 논쟁이 거의 없다 | **중요한 단서 추가 (부분 반박)** | Ok_Economist3865: 리뷰 지적률이 **프롬프트 개선만으로 90% → 25~40%**로 하락. "Codex 리뷰가 많이 잡는다"의 상당 부분이 프롬프트 품질 문제였다는 자기 검증. 다만 역방향 비대칭은 남음 (§1-1a) |
| 4 | §2-2 — Codex=정찰하는 장인 / Claude=단일 패스 (AWS 블로그, 2026-06-11) | **반박 (조건부)** | imperfectlyAware(2026-04-24, macOS/Swift/레거시 ObjC): 정확히 반대. "Codex ... **replicates existing functionality and ignores existing patterns** ... produces GitHub tutorial code". 코드베이스 성격(레거시·자체 프레임워크)이 변수 (§1-1c) |
| 5 | §4 논쟁 D — Claude가 허락 없이 너무 빨리 실행(rednb, 2026-04-26) | **시간 역전 기록** | imperfectlyAware(2026-04-24): "[Codex] is starting to go off and default to doing stuff when I'm still chatting ... **CC used to be terrible at that, but has gotten more patient.**" (§1-1c) |
| 6 | §4 논쟁 D — Claude Code TUI가 버그가 많다(tlonny) | **반대 방향 보강 (Codex 진영 자백)** | Perfect-Series-2901(r/codex OP, 2026-04-29): "**for the CLI tools, Claude is much much better then codex**". DJJonny(2026-02-13): "Codex feels a bit **clunkier** in terms of interface" (§1-2, §7 미확보) |
| 7 | §8-1 — Reddit 구조적 편향 경고 | **강화 (진영 자각이 스레드 표면에 드러남)** | Perfect-Series-2901이 "내 글이 OpenAI 마케팅이라는 비난을 받았다"며 비꼬는 답변을 남김. ThinCar6563: "seeing all the people on various anthropic/claude subreddits **cope** is quite hilarious ... **almost all of us here were once claude code users**". r/ClaudeAI 쪽 벤치마크(1qxr7vs)도 벤더 이해충돌 있음 |
| 8 | §3-4 — 요금·한도 (6/16 급등이 전환점) | **연대기 확장** | **2026-04-10** 이미 개인 단위 반전 존재: maraluke, "**melted my 5h limit with 3 prompts** ... switching right back to Claude Code" (§1-3). **2026-07-11** Sol 세대: "Sol ... **burn through tokens even faster than Fable**"(Historical_Bus_8041) (§1-8). → "Codex 한도 넉넉" 서사는 6/16 하루에 뒤집힌 게 아니라 **최소 4월부터 조건부**였다 |
| 9 | §4 논쟁 B — 지시 준수 판정 유보 | **유보 유지, 최신 세대에서도 재현** | 같은 스레드 하루 차이로 정반대: NootropicDiary(Sol=경직) vs xoStardustt("**Sol tends to go apeshit and refactor half my code ... even with an agents.md that explicitly forbids** cleanup/refactor") (§1-8) |
| 10 | §4 논쟁 B — "부정 지시·강조 문법 무용론"(pmarreck, toraway) | **반대 증언 추가 (병기 필요)** | petburiraja(2026-05-04): "**Codex obeys negative rules better than positive suggestions**" + 1주 실측(184/520 오프로드, $0.34 vs $5~9) (§4-5) |
| 11 | §8-3 — MCP 실전 마이그레이션 사례 없음 | **해소** | §4 전체. 특히 buildxjordan(MCP 8개 → 세션 시작 컨텍스트 90-91%, `search_tool=true`로 99% 회복), ChoasMaster777(MCP 미기동 → `rg` 폴백 → 메모리 100GB), tokovar(상주 MCP 서버가 Sol 3시간 지연) |
| 12 | §8-3 — 클라우드 위임 후기 부족 | **부분 해소** | §3. 다만 "몇 시간짜리 위임"은 여전히 공백. 확보된 성공 사례는 전부 **커밋~MR 한 개 크기** |
| 13 | §8-3 — 한국어 전환 마찰 1차 후기 없음 | **1건 확보, 나머지 확정 부재** | §2-1(dcinside 코유키1357)이 유일. OKKY·회사 기술블로그·커리어리·요즘IT는 **확인 결과 없음**(§2-5) |
| 14 | §3-3 / #13762 — WSL 모드 경로 문제 | **결과 명시로 보강** | Prestigiouspite(2026-03-07): "the Windows config.toml is used for WSL, which results in **MCP etc. not being configured correctly**" — 경로 문제가 MCP 오설정으로 이어진다는 인과 (§4-4) |
| 15 | (선행 문서에 없음) **신규 마찰: 리서치·서브에이전트 깊이** | **신규** | Mountain_Sundae_3270(r/codex, 2026-04-20): "With Claude Code, I used to ... tell it to use a **researcher agent** ... The output was usually detailed, careful ... With Codex, **the research side feels weaker** ... more eager to infer things" https://www.reddit.com/r/codex/comments/1sqk7xj/codex_for_research/ |
| 16 | (선행 문서에 없음) **신규: 세션 이력이 도구에 묶인다** | **신규** | builderpepc의 agent-migrator(2026-06-01) 존재 자체가 증거 (§4-6) |
| 17 | §4 논쟁 A / 논쟁 B 전체 | **두 논쟁을 하나로 합치는 프레임 확보** | PinEnvironmental6395(2026-05-12): "GPT-5 is very good at doing what you say. **But if you don't tell it what you want it won't do it.** It's the **opposite tradeoff Claude makes** — good at figuring out what you want **but at the cost of doing things you didn't want it to do. You have to prompt gpt to be proactive and Claude to be non-destructive.**" (§1-10b) |
| 18 | §2-1 / §4 논쟁 E — "코드 리뷰는 Codex" + "결국 둘 다 쓴다" | **전환 경로의 표준형 발견** | cl0wnb0x(2026-05-12): "**Started using codex for reviews of cc work. Then as I got more familiar with codex cli I just kept using it more and more.**" — 한도 문제는 없었다고 본인이 명시. 리뷰 → 익숙해짐 → 주력 (§1-10d) |
| 19 | §3-4 — 요금·한도가 "함정"인가 "동인"인가 | **위치 재조정 제안** | r/codex 1tao42q(2026-05-12) 댓글 다수의 1순위 전환 동기가 한도. Grouchy_Yellow_8414: "**품질은 Claude가 낫지만 돈으로 더 멀리 간다**". alOOshXL: "5시간 창만 2배, **주간 한도는 그대로**" (§1-10a) |
| 20 | §4 논쟁 A — 협업 vs 위임 이분법 | **유통기한 경고** | simonw(2026-02-10): "**the asynchronous coding agents are getting less asynchronous**" (§3-1). knuckleheads(2026-06-09): 인프라 층에서는 오히려 Claude 쪽이 클라우드 컨테이너를 더 후하게 준다는 반대 관찰 (§3-4) |

---

## 6. 신선도·신뢰도 원장

### 6-1. Reddit (이번에 **원문 직접 확보** — 전부 RSS 경유)

| 항목 | 서브 | 게시일 | 신선도 | URL | 등급 |
|---|---|---|---|---|---|
| **"Did anyone here moved from claude to codex recently? And why?" (댓글 91 — 전환 동기 표본)** | r/codex | **2026-05-12** | 신선 | https://www.reddit.com/r/codex/comments/1tao42q/ | 출처 명확(스레드) / **강한 진영 편향 — 근거 없는 감정 주장 다수** |
| ↳ PinEnvironmental6395 — "gpt는 능동적이 되라고, claude는 파괴적이 되지 말라고 프롬프트해야" | r/codex | 2026-05-12 | 신선 | 동상 `/olbf7zf/` | 익명이나 **이 문서 최다 재확인 관찰** |
| ↳ cl0wnb0x — 전환 경로: 리뷰부터 슬금슬금 (한도 문제 없었다고 명시) | r/codex | 2026-05-12 | 신선 | 동상 `/olb5on1/` | 익명·경로 구체 |
| ↳ Exerionx — 모노레포 안드로이드 빌드 반복 루프 대조 | r/codex | 2026-05-13 | 신선 | 동상 `/olix0vz/` | 익명·명령/상황 특정 |
| ↳ Grouchy_Yellow_8414 — "품질은 Claude가 낫지만 돈으로 더 멀리 간다" | r/codex | 2026-05-12 | 신선 | 동상 `/old6071/` | 익명·**자기 진영 불리 진술** |
| ↳ alOOshXL — "5시간 창만 2배, 주간 한도는 그대로" | r/codex | 2026-05-12 | 신선 | 동상 `/olarg59/` | 익명·**요금표 대조 필요** |
| "Those of you who switched from Claude Code to Codex" (댓글 85) | r/codex | 2026-03-17 | 신선 | https://www.reddit.com/r/codex/comments/1rwjmqp/ | 출처 명확(스레드) / 개별 댓글 익명 |
| ↳ Ok_Economist3865 — 리뷰 지적률 90%→25~40% | r/codex | 2026-03-17 | 신선 | 동상 `/ob0pnnu/` | **익명이나 자기 반증 포함 — 인용 가치 높음** |
| ↳ kknow — 훅으로 엔터프라이즈 게이트, 수동 수정 30% | r/codex | 2026-03-18 | 신선 | 동상 `/ob29m8v/` | 익명·업무 맥락 명시 |
| ↳ imperfectlyAware — 레거시 Swift에서 서사 역전 | r/codex | 2026-04-24 | 신선 | 동상 `/ohz5gl4/`, `/ohz62zp/` | 익명·코드베이스 특정 |
| ↳ sebstaq — Codex 지시 준수 회귀 + 과방어 코드 | r/codex | 2026-03-17 | 신선 | 동상 `/ob0nusu/` | 익명·확인 필요 |
| "switch from Claude to codex (both $200 tier)" (댓글 74) | r/codex | 2026-04-29 | 신선 | https://www.reddit.com/r/codex/comments/1sz7l0l/ | **강한 진영 편향 — OP 본인이 인정** |
| ↳ Perfect-Series-2901 — "CLI 도구는 Claude가 훨씬 낫다" | r/codex | 2026-04-29~ | 신선 | 동상 `/oj2km7z/` | 익명·**자기 진영 불리 진술** |
| ↳ HouseCommercial8583 — 두 구독 병행으로 5h 캡 우회 | r/codex | 2026-05~06 | 신선 | 동상 `/ojgvc7p/`, `/ojgz6ii/` | 익명·조건 일부 명시 |
| "I switched ... due to much higher rate limit" (제목/본문 자기모순) | r/codex | **2026-04-10** | 신선 | https://www.reddit.com/r/codex/comments/1shacwd/ | 익명·**한도 서술 시 날짜 필수** |
| "i recently switched from claude code to codex" (사회과학자) | r/codex | 2026-04-24 | 신선 | https://www.reddit.com/r/codex/comments/1su27hw/ | 익명·도메인 명시 |
| "The real difference between Codex & Claude Code" | r/codex | 2026-06-12 | 신선 | https://www.reddit.com/r/codex/comments/1u3q06l/ | 익명·확인 필요 |
| "I re-subbed to claude code, and realized I was spoiled by Codex" | r/codex | 2026-06-24 | 신선 | https://www.reddit.com/r/codex/comments/1ue06me/ | 익명·**r/codex 편향** |
| "In our benchmark ... 2.2x more tasks" (댓글 31) | r/codex | 2026-07-10 | 매우 신선 | https://www.reddit.com/r/codex/comments/1usogxo/ | **2.2x 수치는 인용 금지(방법론 미공개·이해충돌)**. 댓글은 인용 가치 있음 |
| "From a dev who tried it all" (노하우 모음) | r/codex | 2026-07-26 | 매우 신선 | https://www.reddit.com/r/codex/comments/1v7cvw6/ | 익명·저장소 링크 제시 |
| "Codex For Research?" (리서치 깊이 격차) | r/codex | 2026-04-20 | 신선 | https://www.reddit.com/r/codex/comments/1sqk7xj/ | 익명·확인 필요 |
| "Any tips to improve Codex UX? (Coming from Claude Code)" | r/codex | 2026-02-13 | 신선(경계) | https://www.reddit.com/r/codex/comments/1r3vbvl/ | 익명·확인 필요 |
| "New search tool is amazing!" (`search_tool=true`, 90-91%→99%) | r/codex | 2026-02-11 | 신선(경계) | https://www.reddit.com/r/codex/comments/1r22uk1/ | **출처 명확 — 실측·설정 위치** |
| "메모리 100GB — code-index MCP 폴백" | r/codex | 2026-03-19 | 신선 | https://www.reddit.com/r/codex/comments/1rxu4ur/ | **출처 명확 — 하드웨어·해결책** |
| "Sol 3시간 지연 — 상주 MCP 서버" | r/codex | 2026-07-13 | 매우 신선 | https://www.reddit.com/r/codex/comments/1uvigpf/ | **출처 명확 — 진단 절차 공개, 인과 미확정 자인** |
| "AGENTS.md deny-list + MCP 사이드 모델 라우팅" | r/codex | 2026-05-04 | 신선 | https://www.reddit.com/r/codex/comments/1t3ffxe/ | 출처 명확(수치·저장소) / 자기 홍보 성격 |
| "Windows 오류에 인내심이 바닥" (WSL config.toml → MCP 오설정) | r/codex | 2026-03-07 | 신선 | https://www.reddit.com/r/codex/comments/1rn14kz/ | 익명·이슈 존재 언급 |
| "Chrome 플러그인 MCP 에러 -32602 / js_repl 롤백" | r/codex | 2026-06-20 | 신선 | https://www.reddit.com/r/codex/comments/1ub0j1f/ | 출처 명확(재현·에러 문자열) |
| "Codex is a MONSTER" (클라우드 프리뷰 빌드 디버깅) | r/codex | 2026-05-18 | 신선 | https://www.reddit.com/r/codex/comments/1tgbb0n/ | 익명·사례 구체 |
| "You can move chats between Codex and Claude Code now!" | r/codex | 2026-06-01 | 신선 | https://www.reddit.com/r/codex/comments/1ttnu8y/ | 출처 명확(OSS)·본인 프로젝트 |
| Codex Manager (config.toml·MCP GUI 관리) | r/codex | 2026-01-13 / 02-03 | 경계선 | https://github.com/siddhantparadox/codexmanager | 출처 명확·본인 프로젝트 |
| "GPT-5.3 Codex vs Opus 4.6: 프로덕션 Rails 벤치마크" | **r/ClaudeAI** | 2026-02-06 | 신선(경계) | https://www.reddit.com/r/ClaudeAI/comments/1qxr7vs/ | **출처 명확(방법론) / ⚠️ 벤더 이해충돌·세대 낡음** |
| "Claude + Codex = Excellence" (tmux 교차 리뷰 절차) | **r/ClaudeAI** | 2026-04-24 | 신선 | https://www.reddit.com/r/ClaudeAI/comments/1su7r02/ | 익명·절차 구체 |
| "Opus 4.7 made me re-subscribe to Codex" | **r/ClaudeAI** | 2026-04-23 | 신선 | https://www.reddit.com/r/ClaudeAI/comments/1stfc4t/ | 익명 / **내부 인용 GitHub 이슈는 2차·미검증** |
| "The $20 → $100 gap is pushing solo power users to split spend" | **r/ClaudeAI** | 2026-06-23 | 신선 | https://www.reddit.com/r/ClaudeAI/comments/1ud388h/ | 익명·확인 필요 |
| "Does Claude's $20 Plan No Longer Include Claude Code?" | **r/ClaudeAI** | 2026-04-21 | 신선 | https://www.reddit.com/r/ClaudeAI/comments/1ss3asp/ | 익명(요금표 대조로 검증 가능) |
| 클라우드 과금 벤더 공지 3건 (/u/embirico) | r/codex | 2025-11-02 / 11-04 / 11-21 | ⏳ **오래됨** | 위 §3-7 표 | **출처 명확 — 벤더 자기식별. 배경용만** |
| 클라우드 한도 도입 사용자 보고 2건 | r/codex | 2025-10-30 / 11-02 | ⏳ **오래됨** | 위 §3-7 표 | 익명 / 아카이브 링크 있음 |
| Windows MCP 설정 팁 3건 | r/codex | 2025-09-24 ~ 11-24 | ⏳ **오래됨** | §4-4 | 익명·**현행 확인 필수** |
| "Codex CLI vs Claude Code (500k codebase)" | r/ChatGPTCoding | **2025-09-04** | ⏳⏳ 매우 오래됨 | https://www.reddit.com/r/ChatGPTCoding/comments/1n8c82u/ | 배경용만. GPT-5 세대 |
| "Setting up MCP in Codex is easy, don't let the TOML trip you up" | r/ChatGPTCoding | **2025-08-30** | ⏳⏳ 매우 오래됨 | https://www.reddit.com/r/ChatGPTCoding/comments/1n3y2vq/ | **인용 비권장** |

### 6-2. Hacker News (이번에 신규 확보 — 전부 Algolia API 직접 조회)

| 항목 | 게시일 | 신선도 | URL | 등급 |
|---|---|---|---|---|
| ModernMech — "같은 프롬프트, 같은 모델, 다른 결과: 클라우드 리소스 한도가 바뀌었다" | **2026-07-26** | 매우 신선 | https://news.ycombinator.com/item?id=49057553 | 익명·**대조 조건 명시**, 인용 가치 높음 |
| tcgv — Plus 구독 + 클라우드 전용, 한도 미도달, 하루 MR 12건 | **2026-05-12** | 신선 | https://news.ycombinator.com/item?id=48111615 | 익명·**6/16 이전 데이터** |
| knuckleheads — Codex는 로컬로 미는 중, Claude는 클라우드 컨테이너 제공 | **2026-06-09** | 신선 | https://news.ycombinator.com/item?id=48464767 | 익명·확인 필요 |
| thewisenerd — Codex 클라우드 네트워크 허용목록이 와일드카드라 우회 쉬움 | **2026-04-22** | 신선 | https://news.ycombinator.com/item?id=47860452 | 출처 명확(문서·리서치 링크) |
| big_toast — 클라우드 위임은 "닫힌 루프" 작업에서만 성립 | **2026-02-19** | 신선(경계) | https://news.ycombinator.com/item?id=47080982 | 익명·관찰 |
| lawrencechen — 클라우드는 조종이 어렵다, "화면에 보이는 첫 토큰까지의 시간" | **2026-02-14** | 신선(경계) | https://news.ycombinator.com/item?id=47011986 | 익명·확인 필요 |
| simonw — "asynchronous coding agent" 정의 + 비동기성 후퇴 | **2026-02-10** | 신선(경계) | https://news.ycombinator.com/item?id=46956015 | **출처 명확 — 식별 가능 인물** |
| sidgarimella — Codex는 원격 async에서, Opus는 로컬에서 | **2026-02-05** | 신선(경계) | https://news.ycombinator.com/item?id=46906476 | 익명·확인 필요 |
| vardalab — tmux + 개인 VM + worktree, "노트북 닫고 재우기" | **2026-02-02** | 신선(경계) | https://news.ycombinator.com/item?id=46863453 | 익명·확인 필요 |
| mksglu — `codex mcp add` ↔ `[mcp_servers.*]` 등가 표현 | **2026-02-25** | 신선 | https://news.ycombinator.com/item?id=47148402 | 출처 명확(실행 가능) |
| rurban — 스킬은 심볼릭 링크로, 훅·MCP는 각자 | **2026-03-29** | 신선 | https://news.ycombinator.com/item?id=47562916 | 익명·확인 필요 |

### 6-3. 한국어 (이번 신규)

| 항목 | 저자 | 게시일 | 지표 | URL | 등급 |
|---|---|---|---|---|---|
| **"월 40만원 써가며 작성한 클로드와 코덱스 사용 후기(장문)"** — 중첩 AGENTS.md 마찰 한국어 1차 증언 | 코유키1357 | **2026-04-28** | 조회 7,507 / 추천 11 | https://gall.dcinside.com/mgallery/board/view/?id=thesingularity&no=1149110 | **익명(갤러리)이나 환경·비용 구체. 이 리서치의 한국어 최대 수확** |
| "GPT Pro Codex vs Claude Code: 클린 환경에서 붙여본 지극히 주관적인 비교" | Sean(@sean_kk), velog | **2026-02-13** | — | https://velog.io/@sean_kk/GPT-Pro-Codex-vs-Claude-Code-클린-환경에서-붙여본-솔직-비교-ebs0gvya | 출처 명확(절차·소요시간) / **단일 태스크 1회** |
| "최근 출시한 Codex 앱 직접 써봤습니다" | 김유현(@jujini31), velog | **2026-02-09** | — | https://velog.io/@jujini31/codex-앱-사용-후기 | 출처 명확(실명) / 비교·마찰 서술 없음 |
| "4.7이후 개발자 체감이 점점 codex로 넘어오는중" | 효도폰만수르, dcinside | **2026-05-17** | 조회 3,049 / 댓글 7 | https://gall.dcinside.com/mgallery/board/view/?id=thesingularity&no=1187798 | **2차 — GeekNews 29576과 동일 원글 계열, 중복** |
| "내가 AGENTS.md를 작성하는 방법" | blog.nwlee.com | **날짜 미확인** | — | https://blog.nwlee.com/agents-md-guides-to-codex-cli | **한도 진술 포함 — 날짜 없이 인용 금지** |
| "Codex CLI와 클로드 코드 비교 체험기" | 설탕사과, TILNOTE | **2025-09-05** | — | https://tilnote.io/en/pages/68bab2de1e08f5ca788b1c67 | ⏳⏳ **11개월 — 현행 재확인 없이 인용 금지** |
| OKKY "클로드 코드 Pro 쓰시는 분들" | OKKY Q&A | 약 2025-11 | 답변 2 | https://okky.kr/questions/1545950 | **부재 증명용** — Codex 전환 언급 없음 |

### 6-4. 이번 리서치에서 **인용 금지**로 판정한 것

1. r/codex 1usogxo의 "**2.2배**" — 산출 절차 미공개 + 게시자 이해충돌.
2. Joozio 글이 인용한 "**Claude Code 세션 6,852건 / 툴 콜 234,760건, Read:Edit 6.6→2.0**" — **원 GitHub 이슈 미확인.** URL을 대지 못하는 상태.
3. TILNOTE(2025-09-05)의 "한국어 프롬프트에 영어 답변" — 세대 차이가 너무 크다.
4. `treesoop.com` / `litmers.com` / `blog.gridge.co.kr` / `we0.ai` / `wikidocs.net/blog` 계열 한국어 글 — 1차 경험 확인 불가한 정리·SEO성 콘텐츠.
5. Threads(qjc.ai) — 선행 문서 판정 유지. **게시일 여전히 미확인**, 이번에도 확보 실패.

---

## 7. 접근 실패 소스

### 7-1. Reddit — **부분 성공**, 방법과 한계를 기록

| 경로 | 결과 |
|---|---|
| `https://www.reddit.com/r/{sub}/search.json?...` | ❌ **HTTP 403** (UA 변경·`curl` UA 모두 실패) |
| `https://api.reddit.com/...` | ❌ **HTTP 403** |
| `https://old.reddit.com/...` | ❌ **302 → `/login/?reason=lor2`** |
| redlib 공개 미러(`redlib.catsarch.com`) | ❌ **HTTP 403** |
| `r.jina.ai` 프록시 | ❌ 200이나 본문 477바이트(빈 껍데기) |
| **WebFetch(`reddit.com`)** | ❌ "Claude Code is unable to fetch from www.reddit.com" |
| Firecrawl CLI | ❌ **미설치**(`firecrawl not found`, npm 전역 없음, `FIRECRAWL_*` 키 없음) |
| ✅ **`https://www.reddit.com/r/{sub}/search.rss?q=...&sort=top&t=year&limit=100`** | ✅ **200.** 게시글 제목·작성자·게시일·본문 전문(Atom `<content>`) |
| ✅ **`https://www.reddit.com/r/{sub}/comments/{id}/.rss?sort=top&limit=100`** | ✅ **200.** 댓글 작성자·`<updated>` 일시·본문·퍼머링크 |

- **한계 1 — 강한 레이트 리밋.** 6초 간격에서도 HTTP 429가 잦았고 22초 간격에서도 재시도가 필요했다. **댓글 원문은 4개 스레드만 확보**했다(1tao42q / 1rwjmqp / 1sz7l0l / 1usogxo). 미확보 스레드(본문은 확보, **댓글 미확보**):
  - `1u3q06l` "The real difference between Codex & Claude Code"(2026-06-12)
  - `1ue06me` "I re-subbed to claude code..."(2026-06-24)
  - `1su27hw` "i recently switched from claude code to codex"(2026-04-24)
  - `1shacwd` "I switched ... due to much higher rate limit"(2026-04-10)
  - `1r3vbvl` "Any tips to improve Codex UX? (Coming from Claude Code)"(2026-02-13) — **질문글이라 댓글이 전부다. 후속 1순위**
  - `1s1btfx` / `1ttnu8y`
- **한계 2 — RSS는 업보트/점수를 주지 않는다.** 이 문서의 Reddit 인용에는 **반응 수·점수가 없다.** 선행 문서의 GitHub 👍 수치처럼 "얼마나 많은 사람이 동의했는지"를 댈 수 없다. 책에서 "다수 의견"이라고 쓰려면 별도 근거가 필요하다.
- **한계 3 — 댓글은 `sort=top&limit=100` 기준 상위만.** 전체 댓글 트리가 아니다.
- **재현 방법 (후속 리서처용):** 표준 브라우저 UA + `Accept: application/atom+xml`, **요청 간 20초 이상**, 실패 시 지수 백오프. 인증·API 키 불필요.

### 7-2. 여전히 접근 못 한 소스

| 소스 | 상태 |
|---|---|
| **Reddit 개별 댓글 점수/업보트** | 접근 경로 없음(RSS 미제공). |
| **Lobsters** | 이번에도 미수행 — Reddit 확보에 예산을 몰았다. |
| **Discord / Slack 공개 채널** | 검색 경로 없음. 선행 문서와 동일. |
| **X / Mastodon** | 직접 수집 실패. Reddit 게시물이 인용한 X 링크 2건(`x.com/OmedVibeCodes/status/2080348655039500703`, `x.com/tszzl/status/2019591272315650234`)만 확보, **원문 미확인**. |
| **Threads (qjc.ai) 게시일** | 재시도했으나 **여전히 미확인**. |
| **GeekNews 신규 Codex 토픽 본문** | 선행 문서가 확보한 3건(28538·29011·29576) 외 신규 토픽을 특정하지 못했다. 검색 결과에 `news.hada.io/topic?id=27194`, `27761`, `21296`이 잡혔으나 **주제 확인 실패**. 후속 확인 대상. |
| **회사 기술블로그(국내)** | 검색 결과 0건 — 부재로 판정(§2-5). |

### 7-3. 후속 리서치 우선순위

1. **r/codex `1r3vbvl` 댓글**(2026-02-13, "Codex UX 개선 팁? CC에서 넘어옴") — 질문글이라 댓글이 전부고, 주제가 정확히 이 책의 "전환 직후 세팅" 챕터다.
2. **Joozio 인용 GitHub 이슈 원문**(Stella Laurenzo / AMD, Claude Code 세션 6,852건 분석) — 확보되면 §1-7(c)를 `[출처 명확]`으로 승격 가능.
3. **`search_tool = true`의 2026-08 현행 동작** — §4-2가 이 책에서 가장 실용적인 마이그레이션 팁인데 2026-02 실험 기능 기준이다.
4. **GeekNews 27194 / 27761 / 21296 본문 확인.**
5. **blog.nwlee.com 게시일 확보** — 한국어 한도 진술 인용 가능 여부가 여기 걸려 있다.
