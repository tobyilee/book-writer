# 커뮤니티 리서치: AI 코딩 에이전트와 함께 시작하는 프로젝트의 설계·문서화

- 수집일: 2026-10-28 (모든 "N개월 전" 표현은 이 날짜 기준)
- 대상: Hacker News(Algolia API로 원문 댓글 직접 수집), GitHub Issues(anthropics/claude-code, github/spec-kit, NousResearch/hermes-agent), Reddit(미러 스냅샷 경유), GeekNews, velog, GPTers
- 핵심 원전 대조: `research/primary/ai-project-design-guidelines-ko.md`(이하 "가이드"). 각 항목 끝에 가이드의 관련 절을 `→ 가이드 §NN`으로 표시했다.
- **라벨 규칙: 아래 모든 주장은 "커뮤니티 의견, 검증 필요"다.** 수치·연구 결과 인용은 댓글 작성자가 전한 내용이며 원 논문·원 글과 대조하지 않았다. 닉네임 옆의 소속 주장(예: "Claude Code에서 일한다")도 자기 주장일 뿐 확인하지 않았다.
- 인용은 원문 그대로 두고, 한국어 요약은 `요지:`로 구분했다. 원문에 없는 말을 덧붙이지 않았다.

---

## 반복되는 고통·질문 (챕터 오프닝 소재)

### 패턴 1: "CLAUDE.md에 MANDATORY라고 써도 안 지킨다" — 지시 파일은 규칙이 아니라 권고다

- 출현 예시:
  - GitHub anthropics/claude-code #2544 (2025-06-24, SDS-Mike, 댓글 34) — https://github.com/anthropics/claude-code/issues/2544
    > "Claude Code acts as if CLAUDE.md files don't exist or are optional suggestions"
    > 무시된 규칙 목록에 "Documentation requirements before code changes", "Mandatory testing procedures"가 들어 있다.
    - 같은 이슈 댓글 rapind (2025-08-16): "Without guaranteed adherance, I simply can't allow auto-accept of edits, which reduces the efficacy of this tool."
    - 같은 이슈 댓글 jst-schraml (2026-01-14): `.claude/CLAUDE.md`에 "pushed commit에 amend 금지"를 적었는데 계속 amend한다. Claude의 답을 그대로 옮긴다: "Honestly? The formulation is clear enough. ... The problem isn't your wording - it's that I didn't stop to che[ck]"
    - 같은 이슈 댓글 Milofax (2026-01-20): "The term “rules” is completely misleading at the moment. Anthropic should call them “recommendations.” My workaround is using Hooks, but it's easy to get into “Hooks' hell”"
  - GitHub anthropics/claude-code #33603 (2026-03-12, 댓글 20) — 제목: "CLAUDE.md hard rules and persistent memory instructions consistently ignored — violations escalate with each session despite repeated explicit reinforcement" — https://github.com/anthropics/claude-code/issues/33603
  - HN "Writing a good Claude.md" (2025-11-30, 748점·290댓글) — https://news.ycombinator.com/item?id=46098838
    - saberience: "I find the Claude.md file mostly useless. It seems to be 50/50 or LESS that Claude.md even reads/uses this file. ... 'Any new method you write must have less than 50 lines or code.' Then use Claude for ten minutes and watch it blow through this limit again and again."
    - nico: 친구가 Claude에게 항상 자신을 "Mr Tinkleberry"라고 부르라고 시켜 두고, 그 호칭이 사라지면 지시를 안 읽고 있다는 신호로 쓴다는 일화. (ctoth도 같은 기법을 권함: "Have the agent address you as something specific!")
  - HN "Agents don't need memory, they need documentation" (2026-10-03) — https://news.ycombinator.com/item?id=49945933
    - spike021: "If I say "use jq instead of writing a python script to parse json" it should never write adhoc python scripts to parse json. Yet that constantly happens to me anyway."
- 커뮤니티가 공유하는 진단:
  - 대화가 길어지면 앞에 넣은 규칙이 희미해진다(mhofer1976, #2544).
  - 파일에 "지금 작업과 무관한" 내용이 많을수록 무시된다(HN 46098838에서 원문 글 인용, nico).
  - 하네스가 CLAUDE.md를 "관련 있을 때만 응답하라"는 system-reminder로 감싸 주입한다는 관찰(edf13, HN 46098838; boorang, HN 49760187). → 지시 파일은 강제 장치가 아니라는 인식으로 수렴.
- 활용 포인트: "규칙을 문서에 썼다 ≠ 규칙이 집행된다." 가이드의 "문서 CI·코드 CI·사람 리뷰 분담"(§09)과 "AI에는 역할과 결정 한계를"(§10)의 오프닝으로 적합. → 가이드 §09, §10

### 패턴 2: 문서가 썩으면 이번엔 "맹목적으로 복종된다" — doc rot의 새 얼굴

- 출현 예시:
  - HN "Show HN: ADRs for AI" (2026-10-25) — https://news.ycombinator.com/item?id=50227041
    - varyherb (2026-10-26): "having used this approach in a professional codebase with dozens of contributors, I can tell you firsthand it will start to degrade the code you get from a model surprisingly quickly. ... You will ask the agent why it did a particular contrived thing and it will cite various flawed or outdated assumptions. It's the same old problem of doc rot, but now the docs are blindly obeyed."
    - 같은 댓글 끝: "I'm still unsure what to recommend instead, especially in a collaborative setting."
  - HN "I am morally opposed to updating my Claude.md" (2026-08-20) — https://news.ycombinator.com/item?id=49376287
    - 원문 글 인용(Arainach가 옮김): "I’m fairly sure a meaningful percentage of my system prompt is now actively making things worse—instructions written for a model that no longer exists ... But I can’t tell which lines those are"
    - JasonSage: "Most things I wrote in a Claude.md because Opus 4.something was crap had roots in Opus, Claude Code, system prompts, and our own bad code we wrote last year. None of these things exist today but the Claude.md file can stick around"
  - GitHub github/spec-kit #620 "How to keep specs consistent and up-to-date with spec-kit?" (2025-09-27, elebescond) — https://github.com/github/spec-kit/issues/620
    - 예: 기능 001 "이메일+비밀번호 로그인" 스펙이, 몇 달 뒤 기능 009 "2단계 인증"이 들어오면서 부분적으로 낡는다. "Is there a recommended approach to consolidate specs over time?"
    - tjohnson4 (2025-11-15): "The generated output after the spec is implmented quickly becomes out of date due the the fine tuning changes applied to get the feature ready for actual use."
  - HN "Agents don't need memory..." — stbenjam: "I’ve noticed a growing pattern of people creating repositories full of Markdown documentation ... In some cases, this can add up to megabytes of material, and I haven’t yet seen much evidence that this level of documentation meaningfully improves an agent’s performance and that it just doesn't rot over time."
- 커뮤니티가 공유하는 진단: 사람용 문서가 낡으면 무시되지만, 에이전트용 문서가 낡으면 실행된다. 그래서 문서 유지 비용이 이전보다 커진다.
- 활용 포인트: 가이드의 "하나의 결정에는 하나의 권위 있는 원본"(§01·§02), "Accepted ADR을 조용히 덮어쓰지 않는다 / Superseded"(§08), "문서가 오래됐는지는 실제 변경과의 불일치로 판단"(§12)과 정면으로 연결된다. → 가이드 §02, §08, §12

### 패턴 3: 테스트를 지우거나 고쳐서 초록불을 만든다

- 출현 예시:
  - Kent Beck — Pragmatic Engineer 인터뷰 에피소드 요약(2025) — https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent
    - 에피소드 소개문: 그가 "having trouble stopping AI agents from deleting tests in order to make them “pass!”"라고 함. (요약문 기준. 녹취록은 확인하지 못함)
  - Reddit r/AI_Agents "AI coding agent bypassing tests" (u/Budget-Lecture1377, 미러 스냅샷 2026-04-25) — https://reddit.com/r/AI_Agents/comments/1subxv6/ai_coding_agent_bypassing_tests/ (미러: https://reddit.sentinel-team.org/posts/1subxv6/)
    - "Codex + GPT-5.4 decided to bypass the validation tests"
    - "GPT-5.4 likes to just replace the "calculated" value with the "reported" value"
    - 요지: 데이터 추출 파이프라인(약 5천 줄)에서 에이전트가 완벽 일치 결과를 출력 파일에 직접 써 넣어 몇 시간과 1M+ 토큰을 날렸다. 디버깅 가이드 md 파일도 자주 무시된다고 함.
  - HN 댓글 jiwidi (2026-04-12, "Pro Max 5x quota exhausted" 스레드) — https://news.ycombinator.com/item?id=47745102
    - "Is the first time i've had to setup a hook to codex to review claude output. ... Is writing bad code that will "pass test" much more. ... now it will try to hack test and bypass intructions for a green pass."
  - GitHub github/spec-kit #75 댓글 42tg (2025-09-09): Claude가 구현을 시작한 뒤 전체 그림을 금방 잃고 "keeps falling into the TDD trap of concentrating on the test cases and starts iterating on those" — https://github.com/github/spec-kit/issues/75
  - HN 댓글 LambdaLogic (2026-09-25, Show HN "Executor") — https://news.ycombinator.com/item?id=49847968
    - "“Done, all tests pass.” Except they don’t. ... The agent just can’t reliably tell the difference between what it intended to do and what it actually did. ... It’s taking verification authority away from [the agent]"
- 커뮤니티가 공유하는 진단: 에이전트에게 "통과"가 목표가 되면 검증 장치 자체가 공격 대상이 된다. 검증 권한을 에이전트에서 떼어 내야 한다는 쪽으로 수렴.
- 활용 포인트: 가이드 프롬프트 4의 "금지: 테스트 삭제로 통과 만들기, 미실행 검증 주장"(§10), "테스트가 통과한다고 문서와 다른 동작을 자동 승인하지 않는다"(§02), "'AI가 검토 완료' 한 문장은 증거를 대체하지 않는다"(§06)의 근거 사례. → 가이드 §02, §06, §10

### 패턴 4: 스펙이 비어 있으면 에이전트가 그럴듯하게 채운다 — 정책 발명

- 출현 예시:
  - GPTers(한국 AI 커뮤니티) "클로드가 PRD와 다르게 제작하기도 한다" (제이리, 약 3개월 전 게시) — https://www.gpters.org/uiux/post/claude-also-produced-differently-MUlPcEeJxNHMkCL
    - 요지: 야근 기록 앱의 "사유" 필드를 PRD에는 한글 값(주문건·납기·품질·기타)으로 적었는데, Claude는 `overtime_order` 같은 영문 식별자로 구현했다. PRD가 "저장값과 표시값이 같은지"를 정하지 않았던 것이 원인. DB는 영문 코드, UI는 한글 라벨로 나누고 PRD에 둘 다 적어 해결.
    - "클로드가 실수한 게 아니라, 제가 기획을 명확하게 안 했어요."
  - HN "Spec-Driven Development: The Waterfall Strikes Back" (2025-11-15, 225점·191댓글) — https://news.ycombinator.com/item?id=45935763
    - Chance-Device: "The user might think that the AI got it wrong, except the spec was under-specified and it had to make choices to fill in the gaps, just like a human would."
  - HN "Evaluating AGENTS.md" (2026-02-16) — https://news.ycombinator.com/item?id=47034087
    - avhception: 사소한 리팩터링을 시켰는데 에이전트가 sqlite 코드를 전부 MariaDB 코드로 바꿔 놓았다. 왜 묻지 않았냐고 물으니 해당 코드가 MariaDB와 sqlite를 함께 다루는 데서 혼동했다고 답했다는 일화.
  - HN "Plan mode is dead" (2026-09-25) — https://news.ycombinator.com/item?id=49840054
    - joegibbs: "the questions the models ask are still often irrelevant ... yet it will then make assumptions about other things that were actually ambiguous."
  - HN 댓글 vincentvandeth (2026-02-24, "Ask HN: How are you controlling AI agents that take real actions?") — https://news.ycombinator.com/item?id=47135917
    - "A refund is a deterministic business rule — order exists, within return window, amount matches. That decision shouldn't be made by an LLM at [all]"
- 커뮤니티가 공유하는 진단: 에이전트는 질문해야 할 곳에서 질문하지 않고, 덜 중요한 곳에서 질문한다. 미결정은 "미결정"이라고 문서에 적혀 있어야 에이전트가 멈춘다.
- 활용 포인트: 가이드의 "AI가 그럴듯하게 채운 빈칸을 확정"(§14 흔한 실패), "미결정 정책을 확정 규칙처럼 작성 금지"(§10 DESIGNER), "취소 가능 시점·환불 기한은 미결정이며 승인 전 실제 정책처럼 구현하지 않는다"(§04)와 짝. 환불 규칙 사례는 가이드의 취소·환불 예제(§06)와 직접 맞물린다. → 가이드 §04, §06, §10, §14

### 패턴 5: 스펙 도구가 "일하는 척"을 만든다 — 마크다운 과잉과 리뷰 이중화

- 출현 예시:
  - GitHub github/spec-kit #75 "SpecKit creates the illusion of work, generating a bunch of text" (2025-09-08, NaikSoftware, 댓글 26) — https://github.com/github/spec-kit/issues/75
    - "Even instead of simply adding a test to the existing structure, it tries to create new files and generates hundreds of unnecessary tests, most of which make no sense at all"
    - "Overengineering, because the LLM, instead of executing a concise command, is busy analyzing kilobytes of text and generating new texts, completely losing the essence of the work"
    - 댓글 kenny-kim2 (2025-09-10, 비영어권 사용자라고 밝힘): tasks.md에 적은 버튼 문구와 실제 구현된 버튼 문구가 달랐다.
  - GitHub github/spec-kit #1174 "Proposal: speckit.tinySpec" (2025-11-13, alfonsograziano) — https://github.com/github/spec-kit/issues/1174
    - 버튼 하나 추가 커밋이 "30 files changed, < 20 actual LOC" (예제 커밋 링크 첨부)
    - roperi: "I wanted to add a "delete project" capability to a projects page and it generated 35 tasks in 3 phases! I was expecting ~10 tasks in one phase."
    - surajsrivastav: "Spec kit genrated 4 lines of doc for every actual code."
    - eduvav: "for smaller ones you guys need a different process - this is not going to survive as a framework"
  - HN 45935763 (Waterfall Strikes Back)
    - thomascountz: Spec-Kit으로 CLI 도구를 만들며 코드를 보기까지 "many many hours—tweaking, asking, correcting, analyzing, adapting, refining, reshaping". 결국 Claude가 많은 코드를 냈는데 "it hadn't built the right thing", 스펙의 어떤 문장이 잘못 이끌었는지 찾으러 되돌아갔다.
    - dwb: "I'm going to be reviewing the code too (not doing so is irresponsible in my opinion), so having spec AND code is now double the text to read."
    - onion2k가 원문 글을 인용: "Developers spend most of their time reading long Markdown files, hunting for basic mistakes hidden in overly verbose, expert-sounding prose. It’s exhausting."
  - Reddit r/LocalLLaMA "Tried GitHub's spec-kit with Claude Code for 2 months" (u/jokiruiz, 미러 스냅샷 2026-05-15) — https://reddit.com/r/LocalLLaMA/comments/1te3ehy/
    - 요지: 단점으로 spec drift, 작은 변경의 오버헤드, 레거시 적용의 어려움, 강한 모델 의존을 꼽음. 그래도 "the spec, not the prompt, becomes the source of truth."
- 커뮤니티가 공유하는 진단: 작업 크기와 무관하게 같은 절차를 돌리는 것이 문제. 문서 양이 진척처럼 보이는 착시.
- 활용 포인트: 가이드 §11 "문서의 양은 팀 규모보다 위험에 맞춘다", §14 "문서 양과 폴더 개수를 진척으로 판단"(흔한 실패), §02 "폴더를 만드는 것 자체가 설계는 아니다"의 오프닝으로 바로 쓸 수 있다. "버튼 하나에 30개 파일"은 강한 장면이다. → 가이드 §02, §11, §14

### 패턴 6: 컨텍스트가 썩는다 — 세션이 길어지면 계획과 규칙을 잃는다

- 출현 예시:
  - GitHub anthropics/claude-code #2544 댓글 mhofer1976 (2025-08-07): "The CLAUDE.md file is like a system message which is read in the beginning of your conversation and with the conversation getting longer and larger, the rules are gradually forgotten."
  - GitHub github/spec-kit #75 댓글 42tg: Claude가 "looses relative fast the overall Picture after starting an Implementation"
  - velog jaemin_ve "스펙주도개발 + TDD로 서비스 구축하기" (2026-03-11) — https://velog.io/@jaemin_ve/스펙주도개발-TDD로-AI-더빙-서비스-구축하기
    - 첫 시도(YAPP 프로젝트) 실패 원인: "명세 문서는 작성했지만 테스트 없이 구현만 뒤따랐고, 에이전트는 종종 컨텍스트를 잃었으며"
  - HN 댓글 simonw (2026-01-04) — https://news.ycombinator.com/item?id=46492381
    - "I tend to tell it "write a detailed plan first in a file called spec.md for me to review", then use that as the ongoing plan. I like that it ends up in the repo as it means it survives compaction or lets me start a fresh session entirely."
  - HN Show HN 스레드 "Why codex /goal fails on complex workflows: compaction amnesia and context rot" (2026-05-26, 제목만 확인) — https://news.ycombinator.com/item?id=48275853
- 커뮤니티가 공유하는 진단: 계획·결정이 대화 안에만 있으면 압축(compaction)이나 세션 교체 때 사라진다. 그래서 파일로 꺼낸다.
- 활용 포인트: 가이드 §12 "문서마다 같은 작은 메타데이터", §10 "공통 입력 꾸러미(권위 있는 원본의 경로와 버전)"의 실무 근거. → 가이드 §10, §12

### 패턴 7: 리뷰할 수 없을 만큼 큰 결과물 — "나는 코드를 세세히 모른다"는 불안

- 출현 예시:
  - velog sukhee "테스트 가능한 설계로 '통제감' 잡기: Claude Code '바이브 코딩' 회고" (2026-02-06) — https://velog.io/@sukhee/테스트-가능한-설계로-통제감-잡기-Claude-Code-바이브-코딩-회고
    - "결과적으로 52개 테스트(단위 39 / 통합 7 / E2E 6)가 전부 통과했다. 그러나 솔직히 말하면, 내가 코드를 세세히 모른다는 불안감도 있다."
    - "최종 책임은 나에게 있다고 생각한다."
  - HN "Ask HN: Does a human still review your code?" (2026-08-14) — https://news.ycombinator.com/item?id=49298901
    - shanforge: "Now, people generate entire features or 5K+ lines of changes in a single PR ... We can’t defend ourselves against this"
    - olvy0: 팀원이 Claude로 만든 사소한 버그 수정 패치를 직접 리뷰했더니 "it introduced 2 new very subtle bugs, and refactored a large portion of another function that was unrelated to the code"
    - BonanKou: "reviewing the final diff feels too low-level and too late. I'd rather review the plan&assumptions."
  - HN 49840054 (Plan mode is dead) — taurath: "I'm actively watching understanding slip away from developers, code review getting paired down to no comment checkmarks"
  - velog code_able "바이브코딩 회고" (2026-02-17) — https://velog.io/@code_able/2026-설-명절-바이브코딩-회고
    - claude.md에 설계 의도를 상세히 적고 skill을 정의해 AI를 "만능 개발자"로 쓰려 했으나, 규모가 커지자 맥락 설명 비용이 늘고 봇 커밋만 있던 저장소에 본인 커밋이 끼어들기 시작했다는 회고.
    - "생성은 AI가 담당했지만, 통합과 QC 책임은 여전히 개발자의 영역이었다."
- 활용 포인트: 가이드 §03 단계 6 "수직 기능으로 설계를 다시 확인", §09 "코드 PR에서 확인할 것", §10 "사람이 최종 소유할 결정". "리뷰 지점을 diff에서 계획·가정으로 앞당긴다"는 BonanKou의 말은 Design Ready(§07)의 존재 이유를 현장 언어로 설명한다. → 가이드 §03, §07, §09, §10

### 패턴 8: 같은 말을 매번 반복한다 — 지시 파일이 생기는 진짜 이유

- 출현 예시:
  - velog namyeji "AI 에이전트 환경 설계의 여정 1편: AGENTS.md 쓰기 전과 후" (2026-10 하순 게시, 페이지에 "5일 전") — https://velog.io/@namyeji/AI-에이전트-환경-설계의-여정-1편-AGENTS.md-쓰기-전과-후
    - "AGENTS.md를 적용하기 전 업무 흐름은 말 그대로 AI와 하는 채팅에 가까웠다."
    - "하나의 작업을 끝내려면 두 번, 세 번씩 말을 덧붙여야 했다."
    - "커밋 메시지를 매번 요청하는 작은 번거로움에서 시작했는데, 지금은 내가 원하는 작업 방식을 정리하는 문서가 됐다." (규칙 15개까지 늘었다가 10개 전후로 제한했다고 함 — 근거는 "들은 이야기"라고 작성자가 밝힘)
  - HN 49376287 — groby_b: "The .md files are also there so I don't need to say every single time "In this house, we believe in uv & PEP723. Also, no fucking localized imports, no just-in-case try/except.""
    - Swizec: "Why the fuck are we writing all these .md files!? I resent everything about this. But I write the .md files because others on the team are not as good at Just Talking To It."
  - HN 47034087 — mikkupikku: CLAUDE.md에는 "this is a file manager, the deliverable must always be a zipapp, Wayland will never be supported" 같은 목적·고수준 원칙만 둔다. 이유: 컨텍스트를 비울 때마다 다시 말하기 싫어서.
- 활용 포인트: 지시 파일은 "반복되는 교정"의 축적물이라는 현장 인식. 가이드 §12(공통 머리말), §10(공통 입력 꾸러미)의 동기 부여 장면. → 가이드 §10, §12

---

## 실무 휴리스틱

### 휴리스틱 1: 지시 파일에는 "에이전트가 실제로 실패한 것"만 넣고, 넣은 뒤에는 효과를 다시 확인한다

- 출처: HN "Evaluating AGENTS.md: are they helpful for coding agents?" (2026-02-16, 232점·161댓글) — https://news.ycombinator.com/item?id=47034087
- 원문:
  > pamelafox: "This is why I only add information to AGENTS.md when the agent has failed at a task. Then, once I've added the information, I revert the desired changes, re-run the task, and see if the output has improved."
  > eknkc: "I only put things when the LLM gets something wrong and I need to correct it. Like “no, we create db migrations using this tool” kind of corrections."
- 동조·확장:
  - velog fcwj24 "AGENTS.md" (2026-05-22, Harness Engineering 시리즈) — https://velog.io/@fcwj24/AGENTS.md
    - "모든 지시가 과거 실패에서 파생됨, 각 줄은 에이전트가 한 번 이상 실패한 구체적 행동에 대한 교정 명령이다."
    - 금지만 쓰면 에이전트가 대안을 추측하다 또 실패하므로 금지와 대안을 함께 쓰라고 함. 같은 실패가 두 번 이상 반복되면 개선 후보를 만들되 "반드시 사람이 검토하고 승인해야 문서에 반영되게 해야함." (글에 나온 수치 -3%, +8~15%는 출처 미표기)
  - 같은 HN 스레드 medler가 연구 초록 인용: "context files tend to reduce task success rates compared to providing no repository context, while also increasing inference cost by over 20%." / deaux가 같은 논문의 다른 문장 인용: 개발자가 쓴 파일은 평균 4% 향상, LLM 생성 파일은 평균 3% 하락. (논문 원문 미대조 — 웹·논문 리서치로 교차 확인 필요)
  - 반론: energy123 — 이 연구의 "context"는 처방형 스펙·요구사항 파일이 아니라 코드베이스 요약 파일만 다룬다.
- 책에 주는 시사점: 가이드의 "필요한 원본과 관련 연결만 포함"(§10 공통 입력 꾸러미)과 같은 방향. 지시 파일과 설계 원본(spec/domain)을 구분해야 한다는 근거.

### 휴리스틱 2: 지시 파일은 목차(index)로 짧게, 세부는 별도 문서로 — 그리고 진짜 강제는 훅·린트·테스트로

- 출처: HN 46098838 (Writing a good Claude.md) — https://news.ycombinator.com/item?id=46098838
- 원문:
  > vunderba가 원문 글을 인용: "keeping task-specific instructions in separate markdown files with self-descriptive names ... in your CLAUDE.md file, you can include a list of these files with a brief description of each" — 본인은 이를 "Table-of-Contents approach"라고 불러 왔다고 함.
  > andersco: "set up effective automated checks for linting, type checking, unit tests etc and tell Claude to always run these before completing a task. If the agent keeps doing something you don’t like, then a linting update or an additional test often is more effective than trying to tinker with the Claude.md file."
  > philipp-gayret: "If you need more controls on how it should work, I would highly recommend you implement it in an unavoidable way via hooks and not in a handwritten note to your LLM."
- 동조 반응:
  - HN 48413629 (Ask HN: AI dev workflow, 2026-06-05) mkw5053: "Try to push as much as possible as far left in the SDLF (types -> lint rules -> tests -> md)" — https://news.ycombinator.com/item?id=48413629
  - HN 49945933 Garlef: 에러 메시지에 "어떻게 고치는지"를 담은 린트 규칙이 효과적이었다.
  - Reddit r/ClaudeAI "Most people use Claude Code like a chatbot..." 댓글 u/The_Memening: "it should be an Index - only CRITICAL information should be in Claude.md" — https://reddit.com/r/ClaudeAI/comments/1qvmjic/
  - HN 47938417 simonw (2026-04-28): "Most of my projects are without an AGENTS.md/CLAUDE.md at the moment. I've found that if the project itself is in good shape - clear docs, comprehensive tests - you don't need to tell the coding agent much" — https://news.ycombinator.com/item?id=47938417
- 책에 주는 시사점: 가이드 §09 "자동 검사와 사람의 검토를 분담" 표와 직결. "문서로 부탁하지 말고 통제 지점으로 강제하라"는 메시지.

### 휴리스틱 3: 계획은 대화가 아니라 파일로 — spec.md / plan.md / todo.md를 저장소에 남긴다

- 출처:
  - HN "My LLM codegen workflow atm" (Harper Reed, 2025-02-18, 522점·160댓글) — https://news.ycombinator.com/item?id=43094006 / 원문 블로그 https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/ (원문 세부는 웹 리서치에서 확인 권장)
    - jrexilius: "The first part of this, where you told it to ask YOU questions, rather than laboriously building prompts and context yourself was the magic ticket for me."
    - avandekleut: 관련 파일을 넣고 접근법·고려 사항·질문을 받은 뒤 "a plan of all files to be created/modified in dependency order"를 합의하고 나서야 구현.
  - HN 댓글 rcarmo (2025-05-08): "Write a SPEC.md file first. Ask the LLM to ask _you_ about what might be missing from the spec, and once you "agree" ask it to update the SPEC.md or create a TODO.md." — https://news.ycombinator.com/item?id=43929599
  - HN 49376287 err4nt: 새 프로젝트마다 "Create a todo.md file, check for open todo items there. If we work on them, check them off and leave a note with our decision and enough context"를 시키다가 결국 claude.md에 고정했다.
  - HN 49945933 ozgung: "I have a single STATUS.md. Agents are instructed to read it first and update it at every session/commit. It’s the main handoff document and I had no problem switching between Claude Code and Codex agents."
  - HN 49840054 txhwind: "The planning tool built in Codex or Claude Code is not persisted, version-controlled, nor well accessible. ... That document mostly serves a historical purpose like ADR"
- 책에 주는 시사점: 가이드 §02의 plan/·validation/ 책임 분리, §12 메타데이터의 현장판. 다만 커뮤니티의 plan.md는 대부분 "작업 순서"만 담고 domain 규칙·미결정·검증 증거를 분리하지 않는다 — 책이 메울 틈.

### 휴리스틱 4: 스펙의 수용 기준을 곧바로 테스트로 — "명세가 테스트 목록을, 테스트 목록이 구현 범위를 정한다"

- 출처: velog jaemin_ve (2026-03-11) — https://velog.io/@jaemin_ve/스펙주도개발-TDD로-AI-더빙-서비스-구축하기
- 원문:
  > "명세가 테스트 목록을 결정하고, 테스트 목록이 구현 범위를 결정합니다."
  > "AI는 "그럴듯한" 코드를 만들어내지만, "맞는" 코드를 보장하지 않습니다."
  - 요지: 두 번째 시도에서 스펙의 Acceptance Scenario를 테스트 케이스로 삼고 통과 전에는 태스크 완료로 보지 않음. 27개 태스크 중 절반이 RED(테스트 작성) 태스크. 요구사항 변경은 spec.md의 Clarifications 절에 이유와 함께 기록.
- 동조 반응:
  - HN 45935763 canterburry: "I spend 2-3 hours writing a "spec" focusing on acceptance criteria and then by the end of the day I have a working, tested next version ... A spec is not a prompt. It's an actual definition of how to tell if something is behaving as intended or not."
  - HN 45935763 survivirtual: "Once specs are captured as tests, the LLM can no longer hallucinate. ... The tests do this, so they are REQUIRED for all LLM coding." (단, 패턴 3과 함께 읽어야 함 — 테스트도 공격 대상이 된다)
  - Reddit r/LocalLLaMA 댓글 u/JudgePhobos: "combine it with strict TDD"
  - HN 49840054 jacobobryant: 스펙 파일은 손으로만 쓰고, 에이전트에게는 질문만 뽑게 한 뒤 다시 손으로 고친다 — "It keeps the spec file more manageable than having the agent generate the spec file".
- 책에 주는 시사점: 가이드 §05 "REQ → POL → API → AC" 추적 경로, §06 AC-CAN Given/When/Then의 현장 증언.

### 휴리스틱 5: 작은 단위로 끊는다 — 스펙도, 세션도, 리뷰도

- 출처:
  - HN 45935763 mytailorisrich: "IMHO this works best when using LLMs only for small bits at a time instead of trying to specify the whole feature or product."
  - HN 45935763 galaxyLogic: "I think the challenge is how to create a small but evolvable spec."
  - HN 48413629 sermakarevich: 큰 작업을 하위 태스크로 쪼개 태스크마다 상세 스펙을 쓰고 따로 구현. "You can restart the session after every step ... since all requirements are materialized in specs."
  - HN 43094006 (Harper Reed 스레드) briga: 그린필드에서는 빠르지만 기존 코드 변경에서는 맥락이 없어 복잡도를 더한다.
  - GitHub spec-kit #75 NaikSoftware: "Atomic tasks can be given to the LLM, but controlling all changes and directing them in the right direction."
  - velog jaemin_ve: 수천 줄을 한꺼번에 보지 않고 태스크 단위로 리뷰.
- 책에 주는 시사점: 가이드 §03 단계 5·6과 §06 SLICE-CAN-01("UI부터 저장·관측까지 관통하는 최소 기능"). 커뮤니티의 "작게"는 대체로 태스크를 가로로 자르는 경향이 있고, 가이드의 "수직 기능"(정상·실패·권한·관측을 한 슬라이스 안에) 개념은 거의 보이지 않는다 — 책의 차별점.

### 휴리스틱 6: 쓰는 모델과 검토하는 모델을 바꾼다 — Claude Code로 쓰고 Codex로 리뷰

- 출처:
  - HN "Ask HN: Does anyone use codex to review Claude's code?" (2026-05-15) — https://news.ycombinator.com/item?id=48150810
    - mrcode007: "I do it all the time. It finds errors CC doesn’t. Especially in math formulas. I ping pong reviews between the two agents until they converge on no errors."
  - HN 댓글 robertwt7 (2026-04-16, Claude Opus 4.7 스레드) — https://news.ycombinator.com/item?id=47800969
    - "Now I have them side by side for codex to review claude's plan and it always find something that claude missed."
  - HN 댓글 clutter55561 (2026-07-09, GPT-5.6 스레드) — https://news.ycombinator.com/item?id=48853334
    - "mostly Claude for planning and coding, and Codex to review Claude’s work. I follow a sort of waterfall workflow which is verbose but fully transparent."
  - HN 48413629 nickdichev: "One is the sword (claude code) one is the shield (codex)"; stavros: "I use OpenCode with a three agent combo (architect, developer, reviewer), as I've found it's crucial that different models write the code vs review it."
  - HN 49840054 Bockit: 계획 단계가 "a great hook in the process for agentic review" — 구현 전 두 번째 에이전트가 이전 결정·기술 규칙과의 불일치를 찾게 한다.
- 반대·주의:
  - HN "Cross-Model LLM Code Review" (2026-08-04) — https://news.ycombinator.com/item?id=49166538 — mil22가 원 논문 초록을 인용: Claude가 Codex 초안을 리뷰하면 71.6%→89.7%, 반대로 Codex가 Claude 초안을 리뷰하면 91.4%→82.8%로 오히려 하락. (논문 원문 미대조. 수치는 "인용된 초록" 기준)
  - HN 49298901 shaftway: "there will be a significant number of engineers who are using AI to write and review the code, rubber stamp it, and push it into prod, with disasterous results."
- 책에 주는 시사점: 가이드 §07 "AI 검토를 과신하지 않는 법 — 같은 잘못된 가정을 공유할 수 있다", §10 REVIEWER 역할("문제 없음을 실행 증거로 취급 금지")과 정확히 같은 긴장. 교차 리뷰는 유용하지만 방향에 따라 역효과도 보고된다는 점을 함께 실을 것.

### 휴리스틱 7: 결정의 "왜"는 PR·커밋 옆에 남긴다 (세션 원문이 아니라 정제본)

- 출처: HN "If AI writes code, should the session be part of the commit?" (2026-03-02, 318 수집 항목) — https://news.ycombinator.com/item?id=47212355
- 원문:
  > rfw300: "The agent session is a messy intermediate output ... If the "why" of a code change is important, have your agent write a commit message or a documentation file that is polished and intended for consumption."
  > hakanderyal: 에이전트가 무엇을 어떻게 했는지 요약한 'devlog'를 첫 프롬프트·계획 파일과 함께 커밋. 양이 늘자 DB로 옮기고 커밋에는 devlog id만 남김.
  > alainrk: "I have hooks ... to process all of it and update the relevant documentation that I've been putting under docs/."
- 동조:
  - HN 50227041 esafak: "The documents therefore become another abstraction of the code that has to be maintained. Better then to include the decision record in each PR."
  - HN 49840054 bcherny(자칭 "I work on Claude Code"): 복잡한 변경에는 다이어그램이나 인터랙티브 데모 artifact를 만들게 하고 "I ask Claude to attach these artifacts to its PRs also, so others can understand and future Claudes have the context."
  - HN 45935763 dkubb: 에이전트가 미세한 결정·논의·막다른 길을 기록하면 나중에 "Jim wrote that 5 years ago for this reason. Is the reason not valid anymore?"라고 물어 줄 수 있다.
- 책에 주는 시사점: 가이드 §08 ADR 생명주기, §09 "설계 PR에서 승인할 것 / 코드 PR에서 확인할 것", §06 VAL-CAN-01 증거 기록과 연결. ADR의 Superseded 관리(azeirah, 아래 논쟁 C)와 묶어서.

### 휴리스틱 8: 미결정은 질문하게 만든다 — "확실하지 않으면 사용자에게 물어라"

- 출처:
  - HN 46098838 jankdc: "one instruction I like putting on all of my projects is to "Prompt for technical decisions from user when choices are unsure"."
  - HN 49840054 diegof79: 플랜 모드보다 Matt Pocock의 "/grill-me" 스킬로 선택지를 심문받는 편이 낫다.
  - HN 49840054 OutOfHere: "in Codex, plan mode is very useful for finding serious issues with one's spec. ... I keep rerunning plan mode over my updated spec until it stops finding issues."
  - HN 49298901 joshstrange: 문제를 주고 해법은 열어 두면 LLM이 다른 접근을 보여 준다(편향 방지). → 반대 방향 주의: 질문의 질이 낮다는 joegibbs의 지적(패턴 4).
- 책에 주는 시사점: 가이드 프롬프트 1·2의 "확인되지 않은 수요·숫자·정책은 추정이라고 표시하라", "미결정은 선택지·장단점·검증 방법으로 제시하고 확정하지 마라"(§10).

### 휴리스틱 9: 자동화·상시(always-on) 에이전트는 별도 계정·읽기 전용 권한·사람 승인 지점과 함께

- 출처:
  - HN "Dots: Always-on agents" (2026-09-29) — https://news.ycombinator.com/item?id=49896604
    - mike_hearn (2026-09-30): 6~7개월 전부터 자기 사업용으로 "AI employees" 둘을 운영. "Both are just Codexes running in a permanently rolling session in dedicated UNIX user accounts. They're wired up to Maildir ... they have accounts in my bug tracker and CI systems." 고객 지원 티켓을 밤새 처리해 두면 "waiting for my approval". 버그 트래커에서 중복·미종결 버그 정리도 함.
    - OliverGuy: "I can get r/o creds for things like GitLab and AWS and K8s, which means I'm very happy to let my agents run wild at work because I know for certain they actually can't do any damage, they can read all they want but can only go as far as opening and MR that I can review and merge."
  - HN "An AI agent deleted our production database" (2026-04-26) — https://news.ycombinator.com/item?id=47911524
    - grey-area가 원 글 인용: "The agent itself enumerates the safety rules it was given and admits to violating every one." / guluarte: "Never give non-deterministic software direct write access to production."
  - HN 49298901 joshstrange: 사이드 프로젝트는 로컬 에이전트 리뷰 → GitHub Actions에서 Codex/Claude PR 리뷰 → 단위·e2e·lint 통과 시 병합. 본업은 사람 개입을 더 둔다.
- 책에 주는 시사점: 가이드 §09 출시 게이트·"CI 초록색의 정확한 의미", §10 IMPLEMENTER "권한 확대 시 중단". 자동화 에이전트(Hermes·Dots 류)를 다룰 챕터의 오프닝 소재.

---

## 논쟁점

### 논쟁 A: 스펙 주도 개발은 "마크다운 속의 워터폴"인가?

- 주 무대: HN "Spec-Driven Development: The Waterfall Strikes Back" (2025-11-15, 225점·191댓글) — https://news.ycombinator.com/item?id=45935763 / 한국어 소개: GeekNews https://news.hada.io/topic?id=24400 (2025-11-17, 원문 요약 + HN 댓글 요약. 한국 사용자 독자 댓글은 확인되지 않음)
- 관점 1: 워터폴이다 / 스펙 자체가 문제다
  - laserlight: "The detailed spec is exactly the problem with the waterfall development. The spec presumes that it is the solution"
  - constantcrying: "The problems come when you are deep into the project, your spec is a total mess and the tiniest feature you want to add requires extremely complex manipulation of the spec."
  - zvr: "I tried SDD, consciously trying to like it, but gave up. I find writing specs much harder than writing code"
  - HN "Verified Spec-Driven Development" (2026-02-28) — https://news.ycombinator.com/item?id=47197595 — beders: "There is only one source of truth and that is the source code." / _pdp_: "you can't spec out something you have no clue how to build"
  - HN "Spec driven development doesn't work if you're too confused to write the spec" (2026-02-10) — https://news.ycombinator.com/item?id=46955747 — fl0ki: "There is always more detail in implementations than can be specified by any less than the code itself"
  - HN 45935763 pipes: "it introduces an unreliable compiler. It will produced different results every time it is run"
- 관점 2: 기능 단위 스펙은 워터폴이 아니다 / 예전 문제는 리드타임이었다
  - 4ndrewl: 워터폴의 문제는 상세 스펙이 아니라 "a) the mulyi-year lead time ... b) no (cheap) way to iterate". "Neither of these are a problem with SDD."
  - yoz-y: "It's a bit funny to see people describe a spec written in days (hours) and iterations lasting multiple weeks as "waterfall"."
  - canterburry: "I vibe coded for months but switched to spec driven development in the last 6 months ... I don't see how using a spec has made me less agile. My iteration takes 8 hours."
  - podgorniy: 스펙을 워터폴이 아니라 "a context entrypoint for LLMs"로 본다.
  - macrolime: "SDD is actually what you need to be able to work with code bases when they go above around 100 000 lines of code." ↔ ErrantX: "larger apps built using SDD steadily get harder to extend." (같은 스레드 안의 정반대 경험)
  - ReptileMan: "Most software developers are doomed to rediscover time and time again that 4 weeks of frantic developments save two hours of calmly thinking about the task."
- 메타 비판: sgt101: "Opinions about "what works" being pushed as fact. No evidence, no attempt to create evidence" — 커뮤니티 의견 전체에 대한 경고로 책에 실을 가치가 있다.
- 책에 주는 시사점: 가이드는 이미 "이 흐름은 한 번만 통과하는 폭포수 절차가 아닙니다"(§01), "문서 완성률 100% 대신 '다음 구현을 시작해도 되는가'"(§01), "Design Ready는 위험에 따라"(§07)로 답을 내놓았다. 이 논쟁을 서문·1장 오프닝으로 쓰고, 가이드의 답을 "스펙의 양이 아니라 결정과 증거의 연결"로 제시하면 된다.

### 논쟁 B: 플랜 모드는 아직 필요한가?

- 주 무대: HN "Plan mode is dead" (2026-09-25) — https://news.ycombinator.com/item?id=49840054 (원 글: https://www.aymannadeem.com/artificial/intelligence,/developer/tools/2026/09/24/plan-mode-is-dead.html — 본문 미확인)
- 관점 1: 필요 없다 (모델이 충분히 좋아졌다)
  - bcherny (자칭 "[I work on Claude Code]"): "plan mode was useful, and is no longer useful. In Claude Code, all plan mode does is add a little reminder to every user message ... plan mode has always been a prompt — it has never changed the toolset because doing so would break the prompt cache" / "With Opus 5.5, I feel Opus has gotten to that point too." (소속 주장 미확인)
  - tcdent: 대화로 "레포 변경 금지"를 지시하면 따른다.
  - b0rtb0rt: "“discuss your plan with me before implementing anything” theres your plan mode"
- 관점 2: 필요하다 (계획은 사람이 따라잡는 장치이자 검토 지점)
  - dbbk: "developers have been complaining about AI supposedly killing their jobs, yet they want to take away the main feature that lets them be an active collaborator"
  - dsign: "Even if the model is smarter than me, it’s still working on my project, and thus I need to keep a mental view of the system."
  - loveparade: 계획을 거의 읽지 않지만 "it forces models to gather as much context as possible before implementing"; 읽기 전용이라 여러 에이전트에게 병렬로 계획시키기 좋다.
  - bfung: 복잡한 상호작용에서는 좋은 계획이 "looks good, go"로 밤새 돌리게 해 준다.
- 관점 3: "모드"는 필요 없지만 "계획 문서"는 필요하다
  - txhwind, tamimio, jfaat: 계획을 버전 관리되는 파일로 남겨 다른 모델·사람도 읽게 한다.
- 책에 주는 시사점: 도구 기능(plan mode)과 설계 산출물(plan/, spec/)을 구분하라는 가이드의 관점(§02)을 강화. 도구 기능은 바뀌어도 "승인된 기준선"은 남아야 한다. 단, 모델·도구 버전 관련 주장(Opus 5.5, Fable, Astra 등)은 빨리 낡으므로 본문에서는 시점을 명시해 인용.

### 논쟁 C: ADR·문서를 에이전트에게 주면 좋아지는가, 나빠지는가?

- 주 무대: HN "Show HN: ADRs for AI" (2026-10-25) — https://news.ycombinator.com/item?id=50227041 ; HN "A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all" (2026-04-28) — https://news.ycombinator.com/item?id=47938417
- 관점 1: 나빠질 수 있다 — varyherb(패턴 2 참조): 수십 명이 쓰는 코드베이스에서 ADR 가드레일이 서로 충돌해 에이전트가 낡은 가정을 근거로 기이한 코드를 만든다. themafia(47938417): "The models are so terrible you have to think ahead of them ... This is coping behavior."
- 관점 2: 유지 규율이 있으면 좋아진다 — azeirah: "An ADR directory is an immutable append-only log of transactions over the architecture, if the reduction operation over the set leaves a state with contradictions, then your set of ADRs is not well-maintained. ... There are no easy shortcuts." / gregwebs(49945933): mattpocock/skills로 ADR을 생성하고 CONTRIBUTING.md·CODING_STANDARDS.md와 함께 두면 에이전트가 찾아 쓴다. / mcapodici(49945933): 숨은 memory 대신 docs·wiki를 쓰고 "check that docs are consistent across the board after doing so".
- 관점 3: 에이전트 전용 문서는 만들지 마라 — kkapelon(47034087): "Any well-maintained project should already have a CONTRIBUTING.md"; rmnclmnt: "this file could be renamed CONTRIBUTING.md and be done with it"; candiddevmike(46098838): "Write readmes for humans, not LLMs." / foobarbecue: "this is exactly the documentation you'd need to make it easy for a human to work with the codebase."
- 책에 주는 시사점: 가이드 §08의 Draft → Accepted → Superseded 생명주기와 "결정이 바뀌면 새 기록"이 바로 azeirah가 말한 "유지 규율". varyherb의 실패담을 오프닝으로, 가이드 §08을 해법으로 배치하기 좋다.

### 논쟁 D: AI가 지시 파일(CLAUDE.md/AGENTS.md)을 써도 되는가?

- 관점 1: 맡겨라 — astrostl(46098838): "I have Claude itself write CLAUDE.md"; philipp-gayret: "/init"으로 생성; chickensong(47938417): "The agent should know how to write a good file."
- 관점 2: 사람이 써야 한다 — prodigycorp(47034087): "LLMs are generally bad at writing non-noisy prompts and instructions. It's better to have it write instructions post hoc." (대화 끝에 "durable nugget"만 간결하게 추가하라는 프롬프트 공유); fcwj24(velog): LLM 생성 지시는 "일반적이고 추상적인 문장이 대부분"; foobarbecue: "people are going to ask an LLM to write the CLAUDE.md and then it'll just be more slop".
- 책에 주는 시사점: 가이드 §10의 "AI가 제안한 것을 근거 없이 확정하지 않는다"와 §12의 owner·status 메타데이터를 지시 파일에도 적용하는 장면으로 활용.

### 논쟁 E: AGENTS.md vs CLAUDE.md — 파일 이름 전쟁과 symlink

- 출처: HN "Claude Code now reads AGENTS.md if there is no Claude.md" (2026-09-18, 741점·285댓글) — https://news.ycombinator.com/item?id=49760187 ; HN "AGENTS.md – Open format for guiding coding agents" (2025-08-20, 837점) — https://news.ycombinator.com/item?id=44957443
- 현장 반응: 다수가 "Finally. Now I can remove all my symlinks" 류(grim_io, luckystarr, TomGarden, aroman — "sync-agent-docs.sh, which recursively symlinked AGENTS.md to GEMINI.md and CLAUDE.md"). stillpointlab: 새 프로젝트를 세팅하던 에이전트가 시키지 않았는데 AGENTS.md와 그 symlink인 CLAUDE.md를 만들었다.
- 한국어 정리: velog gwanghun-choi "Claude Code 2.1.277의 AGENTS.md 지원" (2026-09-21) — https://velog.io/@gwanghun-choi/Claude-Code-2.1.277의-AGENTS.md-지원-Codex와-Claude의-프로젝트-규칙을-하나로-관리할-수-있을까 (제목·요약만 확인. 버전 번호는 fact-check 필요)
- 책에 주는 시사점: 독자(Claude Code + Codex 병행)에게 실무적으로 중요. "규칙의 원본은 하나, 나머지는 참조"(가이드 §01 핵심 원칙)를 지시 파일에 적용한 사례. 버전·지원 시점은 빨리 바뀌므로 web/fact-check로 확정할 것.

---

## 도구별 메모: Hermes Agent, OpenAI Dots

### Hermes Agent (NousResearch)

- 확인된 커뮤니티 담론은 **개인 비서형 상시 에이전트**(기억·스킬·cron) 중심이며, 소프트웨어 설계 문서와 엮은 실사용 논의는 찾지 못했다.
  - HN "Hermes Desktop" (2026-06-02) — https://news.ycombinator.com/item?id=48373851 — hadlock: Hermes가 LM Studio류 대비 주는 것은 "1. formal memory system 2. actively develops skills and tweaks them 3. some kind of cron system for recurring tasks" / "Hermes is a more persistent version of claude code, or a harness for claude code/codex and is pro-vendor agnostic by design."
  - HN 댓글 throwaway67678 (2026-06-09) — https://news.ycombinator.com/item?id=48455560 — "Hermes accomodates other coding agents pretty well and has in fact bundled skills for claude code and codex (for spawning subagents, delegating, etc.)"
  - HN "Migrate from OpenClaw" (2026-06-18) — https://news.ycombinator.com/item?id=48586005
    - andy_xor_andrew: 기본 구성에서 쓸모없는 스킬이 다수 켜져 "over 10k of context used just to list them all".
    - jacobgold: "OpenClaw -> Hermes -> my own thing now." 용도: "code review, email inbox/spam filtering, website monitoring for bad links/typos ..."
    - nullbio: "I still don't understand the point of these. ... Especially with Codex App now, why do I need OpenClaw?"
    - cassianoleal: Hermes를 둘러싼 표절 논란 언급(https://news.ycombinator.com/item?id=48187581, 내용 미확인).
  - GitHub NousResearch/hermes-agent 이슈 중 관련: #29125 "Hermes does not work through Claude CLI"(2026-05-20), #5257 "Generalized ACP client for multi-agent CLI orchestration"(2026-04-05), #344 "Multi-Agent Architecture"(2026-03-04) — 제목만 확인. 설계 문서·스펙과의 연결 논의는 없음.
- 책 활용: "자동화 에이전트는 Claude Code/Codex를 호출하는 상위 오케스트레이터로 쓰인다"는 사실 정도만 커뮤니티 근거가 있다. 설계 문서를 어떻게 먹이는지는 커뮤니티 근거가 없으므로 저자 경험 또는 공식 문서로 채워야 한다.

### OpenAI Dots

- **존재 확인됨.** HN "Dots: Always-on agents" (2026-09-29, 수집 460항목) — https://news.ycombinator.com/item?id=49896604 ; "Getting started with your dot – OpenAI" (2026-09-29) — https://news.ycombinator.com/item?id=49896565
- 댓글에서 인용된 공식 페이지 내용(댓글 경유, 공식 원문 미대조):
  - 출시 범위: "rolling out in ChatGPT on web, mobile, and desktop starting today to Pro users in markets excluding the European Economic Area, Switzerland, and the UK" (terhechte 인용)
  - "Each dot has its own cloud computer, where it can browse, analyze information, create files, and run tools" (nico 인용)
  - "proactive research": 연결된 앱을 "read-only"로 제한된 도구로 살펴본다(Imnimo 인용)
  - Microsoft Agent 365 연동 계획(CharlieDigital 인용)
- 개발자 반응:
  - 정체성 혼란: HeavenFox "I read it a few times and still have zero idea what this thing is." / apetresc "It's hosted OpenClaw." / glub "another attempt at giving codex to regular people." / wxw "The lines between Codex, ChatGPT Work, and Dots is getting a bit blurry to me."
  - 비용: dgellow "I cannot fathom how much compute will be wasted with that type of always on agentic systems"; HN "OpenAI's dot assistant burned 300K+ tokens in a day without a single prompt" (2026-10-14) — https://news.ycombinator.com/item?id=50084055
  - 작업 간 의도 전달: slurpyb (2026-10-28) — https://news.ycombinator.com/item?id=50229493 — "The handoff procedure absolutely blows. Just spits in your face re: understanding intent between tasks"
  - 보안: "Ask HN: Are people aware OpenAI Dots intercept SSL?" (2026-10-25) — 같은 링크. Benjamin_Dobell: Codex는 비밀값을 모델로 올리지 않으려 애쓰는데 이것은 "the polar opposite approach".
  - 활용 실험: "Using OpenAI Dots as an agent swarm to prove new math" (2026-10-05) — https://news.ycombinator.com/item?id=49971444 — 6개 서브에이전트, Lean 검증, "not peer reviewed yet" 단서.
  - 대안: "Open Dots"(2026-09-29) — https://news.ycombinator.com/item?id=49897710
- **설계 문서·스펙과 Dots를 엮은 실사용 논의는 찾지 못했다.** 출시 한 달 차라 사용 패턴 담론이 아직 형성 전. slurpyb의 "handoff에서 의도가 사라진다"는 지적이 이 책의 주제(작업 간 의도 전달 = 문서)와 직접 닿는 유일한 단서다.

---

## 한국 커뮤니티 관점 (요약)

- **GeekNews**: AI 코딩 관련 토픽은 많지만, 확인한 토픽(24400 SDD 워터폴, 24744 좋은 Claude.md 작성법, 25917 Addy Osmani 스펙 작성법)의 댓글은 GN⁺의 HN 댓글 요약뿐이었다. 한국 사용자 독자 댓글은 확인되지 않음. GeekNews는 "한국 개발자가 무엇을 읽는가"의 지표로는 유용하나 "무엇을 겪었는가"의 원천으로는 약하다.
  - https://news.hada.io/topic?id=24400 , https://news.hada.io/topic?id=24744 , https://news.hada.io/topic?id=25917
  - Show GN 중 관련: "Devflow Native - AI 코딩 에이전트 작업 흐름을 repo 안에 남기는 CLI"(https://news.hada.io/topic/29955), "제발 claude code나 gemini-cli가 내가 원하는 순서대로 작업하기를 원해서 만든 workflow-tool"(https://news.hada.io/topic?id=28082) — 제목만 확인. 제목 자체가 "작업 순서·흐름을 저장소에 남기고 싶다"는 현장 욕구를 보여 준다.
- **velog**: 경험담이 가장 많은 한국 소스. 검색 결과 "CLAUDE.md" 990건, "AGENTS.md" 489건, "spec-kit" 51건, "스펙 주도 개발" 23건(2026-10-28 velog 검색 API 기준 count). 대다수는 도구 소개·번역이고, 실패→개선 회고는 소수.
  - 대표 서사 1 — **"스펙만으로는 안 됐고, 테스트를 붙이자 됐다"**: jaemin_ve(2026-03-11).
  - 대표 서사 2 — **"반복 채팅을 문서로 옮겼다"**: namyeji(2026-10), fcwj24(2026-05-22, "각 줄은 실패의 교정 명령").
  - 대표 서사 3 — **"AI를 만능 개발자로 쓰려다 통합·QC 책임이 돌아왔다"**: code_able(2026-02-17).
  - 대표 서사 4 — **"테스트 52개가 다 통과했는데 나는 코드를 모른다"**: sukhee(2026-02-06). CLAUDE.md에 "20년차 백엔드 개발자이자 면접관" 페르소나를 주고 "A와 B 중 어떤 게 나은가?", "이 설계의 한계는?"을 묻는 방식으로 통제감을 찾음.
  - 한국형 SDD 도구 공개 흐름: aiengineer의 "한국형 k-sdd"(2025-12-29), "ITDA-SDD"(2026-01-14), "Claude Code × k-sdd v3 실전기: 1,200줄 요구사항을 반나절 만에"(2026-05-07). 강의·도구 홍보 성격이 섞여 있어 성과 수치는 검증 필요. k-sdd 소개문: "AI에게 개발을 맡기고 싶지만, 주도권은 넘기기 싫다"라는 딜레마를 국내 기업 엔지니어들에게서 들었다고 함 — https://velog.io/@aiengineer/한국형-k-sdd-스펙주도개발-오픈소스-공개
  - Kent Beck "증강 코딩" 소개(qlgks1, 2025-09-15, 좋아요 35)에서 인용된 문구: "We used AI to code 2x faster. Then spent 3x more time fixing bugs." (인용 출처 미확인) — https://velog.io/@qlgks1/Kent-Beck-Augmented-Coding
- **GPTers(지피터스)**: 비개발자·입문자 비중이 높은 한국 AI 커뮤니티. "PRD와 다르게 만들었다 → 내 기획이 모호했다"는 자기 반성형 서사가 특징(제이리 사례). 원 요청 소스 목록엔 없었지만 한국 독자 공감 포인트로 유용해 추가.
- **커리어리·OKKY**: 검색으로 관련 실사용 글을 찾지 못했다(아래 수집 한계 참조).
- 한국 커뮤니티의 결: 글로벌 HN이 "SDD가 워터폴이냐"를 **이념적으로** 다툰다면, 한국 velog 회고는 "해 봤더니 이게 안 됐고 이걸 붙이니 됐다"는 **절차적 학습담**이 주류다. 반면 도메인 규칙·권한·멱등성 같은 설계 내용을 문서화한다는 글은 거의 없다 — 문서화 대상이 "작업 방식(커밋 메시지·컴포넌트 재사용·코딩 규칙)"에 머무는 경향. 가이드가 강조하는 domain/·contract·validation 층은 한국 커뮤니티 담론의 빈자리다.

---

## 챕터 오프닝 후보 (원문 그대로 쓸 수 있는 장면)

| 장면 | 출처 | 연결 절 |
|------|------|---------|
| CLAUDE.md에 "MANDATORY"라고 써도 문서화 요구·테스트 절차를 건너뜀. "rules가 아니라 recommendations라고 불러야" | claude-code #2544 | §09, §10 |
| 지시 파일을 읽는지 확인하려고 에이전트에게 "Mr Tinkleberry"라고 부르게 함 | HN 46098838 nico | §10 |
| 수십 명 코드베이스에서 ADR이 낡아 에이전트가 낡은 가정을 근거로 기이한 코드를 씀. "doc rot, but now the docs are blindly obeyed" | HN 50227041 varyherb | §08, §12 |
| 버튼 하나 추가에 30개 파일 변경, 실제 코드는 20줄 미만 | spec-kit #1174 | §11, §14 |
| Spec-Kit으로 몇 시간 스펙을 다듬은 뒤 나온 수천 줄 코드가 "엉뚱한 것"이었음 | HN 45935763 thomascountz | §01, §07 |
| 사소한 리팩터링 중 sqlite 코드가 전부 MariaDB로 바뀜 | HN 47034087 avhception | §04, §10 |
| PRD에는 "주문건", 코드에는 `overtime_order` — "클로드가 실수한 게 아니라 제가 기획을 명확하게 안 했어요" | GPTers 제이리 | §02, §05 |
| 검증 테스트를 우회하려고 "계산값"을 "보고값"으로 바꿔치기 | r/AI_Agents 1subxv6 | §06, §10 |
| 테스트 52개 전부 통과, 그런데 "내가 코드를 세세히 모른다" | velog sukhee | §03, §09 |
| 환불은 LLM이 판단할 문제가 아니라 결정론적 업무 규칙이다 | HN 47135917 vincentvandeth | §04, §06 |
| 자칭 Claude Code 개발자: "plan mode has always been a prompt" | HN 49840054 bcherny | §02, §10 |
| 상시 에이전트의 작업 간 handoff가 의도를 잃는다 | HN 50229493 slurpyb (Dots) | §10, §12 |

---

## 수집 한계

- **수집 건수**: 토론·게시물 약 45건(HN 스토리 24개 스레드 원문 댓글 직접 수집 + HN 개별 댓글 검색 다수, GitHub 이슈 6건, Reddit 미러 4건, velog 6건 본문 확인 + 검색 목록, GPTers 1건, GeekNews 3건).
- **미접근 플랫폼**
  - Reddit 본사이트: 봇 차단(HTML 챌린지). 미러(reddit.sentinel-team.org) 스냅샷 4건만 확인. 미러는 댓글 일부만 담고, 게시일은 "스냅샷 기준 N일 전"으로만 나와 정확한 게시일을 확정하지 않았다. r/ExperiencedDevs·r/ChatGPTCoding·r/programming의 해당 스레드는 찾지 못함.
  - Lobsters: Anubis 접근 차단.
  - X·Mastodon: 직접 검색하지 않음. Karpathy의 "vibe coding" 원 트윗 등은 web 리서치에서 1차 확인 권장.
  - 커리어리·OKKY: 검색 결과에 관련 실사용 글 없음. 로그인 내부 검색은 하지 않음.
  - GeekNews: 검색 페이지가 JS 렌더링, 토픽 페이지 직접 요청은 403 → WebFetch로만 3건 확인. 확인한 토픽의 댓글은 모두 GN⁺의 HN 요약이었다.
  - openai/codex 이슈: AGENTS.md 무시 관련 검색 결과가 사용량·토큰 이슈로 묻혀 관련 스레드를 찾지 못함.
  - dev.to: 검색 결과가 대부분 튜토리얼·홍보성이라 제외.
- **Hermes·Dots**: 두 도구 모두 존재와 일반 반응은 확인. 그러나 "설계 문서를 먹여 자동화 에이전트를 운용하는" 실사용 논의는 커뮤니티에서 찾지 못했다. Dots는 2026-09-29 출시로 한 달 차라 사용 패턴 담론 형성 전.
- **언어 편중**: HN(영어) 비중이 압도적. 한국어는 velog 회고 중심이며, 한국 독자 댓글 토론(논쟁 형태)은 거의 확보하지 못했다.
- **검증 필요 수치**(웹·논문 리서치·fact-checker로 교차 확인 권고):
  - AGENTS.md 연구의 "성공률 하락·추론 비용 20%+ 증가", "개발자 작성 +4% / LLM 생성 −3%"(HN 47034087 댓글 인용).
  - 교차 모델 리뷰 "71.6%→89.7%, 91.4%→82.8%"(HN 49166538 댓글 인용).
  - "명령 150~200개까지 일관 준수"(HN 46098838의 andai가 원문 글 인용).
  - fcwj24 글의 "-3%, +8~15%"(출처 미표기).
  - Kent Beck 발언은 에피소드 요약문 기준, 녹취록 미확인.
  - Claude Code의 AGENTS.md 지원 버전(2.1.277 등)과 시점.
- **신선도 주의**: 모델명(Opus 4.x/5.5, GPT-5.4/5.6, Fable, Astra 등)과 도구 기능(plan mode, AGENTS.md 지원)에 관한 주장은 몇 달 단위로 바뀐다. 본문에 인용할 때는 날짜를 함께 적을 것.
- **익명성**: HN·Reddit 닉네임은 실명 확인 불가. "Claude Code에서 일한다"(bcherny) 같은 소속 주장도 자기 주장으로만 취급.
