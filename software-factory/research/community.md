# 커뮤니티 리서치: Software Factory — AI 보조 코딩에서 워크플로 주도형 자율 파이프라인으로

- 슬러그: `software-factory` · 장르: `tech-book`
- 검색 시점: **2026-09-28** (모든 항목 공통. 각 항목 옆 날짜는 원 게시일)
- 수집 규모: 토론·게시글·이슈·영상 **84건** (HN 30 · GitHub Issues 8 · Reddit 2차 인용 2묶음 · 실무자 블로그/X 22 · YouTube 9 · 한국 커뮤니티/기술블로그 13)
- 라벨 규칙: 이 문서의 **모든 주장은 "커뮤니티 의견, 검증 필요"**다. 수치·날짜·제품 기능은 web/paper 리서치와 fact-checker 대조 전에는 사실로 쓰지 않는다. 특히 `⚠️검증` 표시는 출처가 2차이거나 수치가 의심스러운 항목이다.
- 인용 방식: 저작권상 긴 원문 전재를 피하려고 **발언은 요지(한국어 의역)로 옮기고 원문 링크를 붙였다.** 챕터에서 직접 인용이 필요하면 링크에서 짧게(15단어 이하) 발췌할 것. 따옴표 안 영어는 커뮤니티가 쓰는 **용어·조어**만 남겼다.

### 용어·모델명 교정 메모 (브리프 대비)

| 브리프 표기 | 커뮤니티·공식 표기 (확인 시점 2026-09-28) | 비고 |
|---|---|---|
| GPT-Sol-6 | **GPT-6 Sol** (OpenAI, 2026-09-22 발표, Luna와 동시). 커뮤니티 약칭 "Sol 6", "Sol". 상위 모델 **GPT-6 Astra**는 2026-09-03 출시 | [OpenAI](https://openai.com/index/introducing-gpt-6-sol-and-luna/), [9to5Mac 2026-09-22](https://9to5mac.com/2026/09/22/openai-upgrading-chatgpt-and-codex-with-two-more-gpt-6-models/) ⚠️검증 |
| Opus 5.5 | **Claude Opus 5.5** (2026-09-22). 커뮤니티는 "Fable 5.1급 성능을 더 싸게"로 받아들임. Anthropic 상위 티어는 **Fable** (5, 5.1) | [Simon Willison 2026-09-22](https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/) ⚠️검증 |
| Muse Spark | Meta **Muse Spark 1.3** + 터미널 에이전트 **Muse Code**(2026-08-05 출시) | [dev.to 리뷰 2026-09-04](https://dev.to/gosukiwi/muse-spark-13-a-review-3h7) ⚠️검증 |
| Grok | **Grok 4.5 / 4.6**, CLI 에이전트 **Grok Build**(2026-07-15 오픈소스화). Cursor 인수 이후 Cursor 1st-party 모델이라는 2차 보도 있음 | ⚠️검증 (web 리서치로 확인 필요) |

> **신선도 경고:** Opus 5.5·GPT-6 Sol은 검색 시점 기준 출시 6일째다. 두 모델에 대한 커뮤니티 평가는 초기 인상 수준이며 워크플로 수준의 회고는 아직 거의 없다. 이 문서의 워크플로·고통 패턴 대부분은 **Opus 4.6~5.0, GPT-5.x~6 Astra 시기**의 경험에서 나왔다.

---

## 반복되는 고통·질문 (챕터 오프닝 소재)

### 패턴 1: "생성은 5분, 리뷰는 이틀" — 병목이 코드 작성에서 리뷰로 옮겨갔다

가장 많이, 가장 여러 플랫폼에서 반복된다. 팩토리 논의 전체의 출발점.

- 출현 예시:
  - GeekNews 「AI 없이 보낸 한 달」(~2026-09-27) https://news.hada.io/topic?id=34323 — 병렬 에이전트를 늘리자 직접 하면 20분 걸릴 일을 에이전트가 5분에 썼지만, 쌓인 작업 탓에 리뷰는 이틀이 걸렸다는 경험. 결국 동료 리뷰에서 "테스트가 바뀐 시나리오를 검증하지 않는다"는 지적을 받고 10년 TDD 경력의 수치심으로 AI를 끊었다고 고백.
  - HN 「Show HN: Stage」(2026-04-16) https://news.ycombinator.com/item?id=47796818 — stackskipton: AI 코드에 대한 사람 리뷰는 이제 대부분 도장 찍기(rubber stamping)이고, 물량을 따라갈 수가 없다.
  - HN 「Stripe Minions」(2026-02-22) https://news.ycombinator.com/item?id=47110495 — iepathos: 주 1,000건 PR이 대부분 마이그레이션·보일러플레이트·이전 Minion PR의 버그 수정이라면 사람 시간을 낭비하는 리뷰 1,000건을 만든 것일 뿐.
  - Armin Ronacher 「Agent Psychosis」(2026-01-18) https://lucumr.pocoo.org/2026/1/18/agent-psychosis/ — 프롬프트는 1분, 코드 생성은 몇 분인데 제대로 된 PR 리뷰는 그 몇 배가 걸린다는 비대칭이 메인테이너를 태운다.
  - Addy Osmani 「The 80% Problem」(2026-01-28) https://addyo.substack.com/p/the-80-problem-in-agentic-coding — 채택률 높은 팀이 PR은 98% 더 머지했지만 리뷰 시간은 91% 늘었다는 수치 인용. ⚠️검증(원 데이터 출처 확인 필요)
  - Dex Horthy 「Why Software Factories Fail」(2026-07, HN 2026-07-23) https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/wsff.md — PR이 너무 많은 게 아니라 **나쁜** PR이 너무 많은 것이라는 진단. Faros 데이터를 인용해 PR당 인시던트 급증을 주장. ⚠️검증(Faros 수치: 인시던트/PR +242.7%, 리뷰 없이 main 머지 +31.3% — 2차 요약 기준)
  - 당근 박용권(AI월드 2026, 2026-09-09) https://www.fnnews.com/news/202609091826242004 — 에이전트 코드가 빨리 늘면서 검토가 밀리고, 동료가 판단 근거를 이해 못 하는 문제가 생겼다. 이를 기술 부채(검토 지연)·인지 부채(이해 부족)·의도 부채(판단 근거 미기록)로 구분.
  - OpenAI Codex 팀 스스로도 "Code review is the next bottleneck"을 에피소드 섹션 제목으로 씀 — Every 팟캐스트(2026-02-18) https://every.to/podcast/how-openai-s-codex-team-uses-their-coding-agent
- 추정 원인 (커뮤니티 공유 진단):
  - 노력 기반 역압(effort-based backpressure)이 사라졌다. 코드를 만드는 비용이 0에 가까워지자 검증 비용만 남았다.
  - 에이전트는 리뷰받기 좋게 쓰지 못한다 — 한 번에 너무 큰 변경, 무관한 코드 건드림 (HN danpalmer, 49023019). 한 에이전트가 400줄을 건드려 30줄 순진척을 낸다는 측정도 (HN devonkelley, 47110495).
  - 조직 절차(요구사항·승인·배포)는 그대로라 개인 10배가 조직 25~30%로 줄어든다 (GeekNews 「The Agentic Awakening」, ~2026-08-31, https://news.hada.io/topic?id=33058, 20여 CTO 인터뷰 주장 ⚠️검증).

### 패턴 2: "내 코드베이스를 내가 모른다" — 이해 부채·인지 부채

- 출현 예시:
  - Geoffrey Litt 「Understanding is the new bottleneck」(AI Engineer 채널, 2026-07) https://www.youtube.com/watch?v=WkBPX-oDMnA — 병목은 정확성이 아니라 이해. 이해를 "검증하기 위한 이해"와 "다음 수를 제안하기 위한(참여하기 위한) 이해"로 나누고, 후자를 잃으면 사람은 구경꾼이 된다고 주장.
  - HN 「What I'm Hearing About Cognitive Debt」(Margaret-Anne Storey 글, HN 2026-05-05) https://news.ycombinator.com/item?id=48017298 — 팀이 공유된 이해를 쌓는 속도보다 코드·기능이 더 빨리 생긴다. 반론(jdw64): "인지 부채"는 문서화 실패를 포장한 마케팅 용어일 수 있다.
  - Addy Osmani: 처음부터 다시 쓸 수 없는 코드를 리뷰하는 건 너무 쉽다 — "comprehension debt" (2026-01-28 글, 2026-07-22 「Light and Dark」에서 재정의).
  - HN 「Why Software Factories Fail」 20k: 사람 리뷰의 목적은 LLM이 아니라 **당신이** 무슨 일이 일어나는지 이해하는 것.
- 추정 원인: 리뷰가 "이해"의 유일한 경로였는데, 리뷰를 건너뛰는 순간 팀의 공유 멘탈 모델이 끊긴다. 신규 입사자가 동료 대신 Claude에게 묻는 현상은 Anthropic 내부에서도 보고됨 (Boris Cherny, Fortune 2026-06-11 https://fortune.com/2026/06/11/anthropic-claude-boris-cherny-doesnt-write-code-by-hand-anymore/).

### 패턴 3: 무인(lights-off) 팩토리는 시간이 지나면 코드베이스를 slop으로 만든다

- 출현 예시:
  - Dex Horthy WSFF 문서 + 동명 AI Engineer 발표 https://www.youtube.com/watch?v=Ib5GBkD555M — 모델은 사람의 조향 없이 코드베이스 품질을 유지·개선하지 못한다. RL 벤치마크는 테스트 통과만 보상하고 유지보수성 훼손엔 벌점이 없다. 테스트 피드백은 초 단위, 나쁜 아키텍처의 비용은 주 단위로 나타난다.
  - HN lethain 스레드(2026-09-20) https://news.ycombinator.com/item?id=49777913 — mentalgear: 경험 있는 사람이 주기적으로 모양을 바로잡지 않으면 팩토리는 오래 돌릴수록 기하급수적으로 지저분해진다.
  - HN WSFF 스레드 pydry: LLM이 깨끗하고 일관된 추상화를 빚는 걸 본 적이 없다 — 학습 데이터에 대응물이 없으면 허우적댄다.
  - HN WSFF 스레드 swiftcoder: Claude는 스파게티 코드베이스도 사람보다 빨리 탐색하므로, 사람이 못 쓰게 된 뒤에도 한참 동안 작업을 계속할 수 있다 — 그래서 붕괴가 늦게 드러난다.
  - HN StrongDM 스레드(2026-02-07) https://news.ycombinator.com/item?id=46924426 — lunar_mycroft가 공개된 Rust 코드에서 과도한 clone, 부실한 에러 처리, 800줄짜리 클로저 등을 지적.
  - PostHog 뉴스레터 「Can software factories actually work?」(Jina Yoon, 2026-08-11) https://posthog.com/newsletter/software-factories — 회의론과 낙관론을 함께 정리. PostHog는 에이전트가 PR의 ~70%를 쓰고 사람이 80%를 훑어본다고 함 ⚠️검증.
- 반대 증언(같은 스레드): iamwil은 8개월째 팩토리를 운영하며 4개월 동안 리뷰에서 코드를 안 봤는데 벽에 부딪히지 않았다고 함. adamtaylor_13은 품질 저하가 "느껴질" 때 에이전트로 다시 청소할 수 있었다고 함. → 논쟁 A 참조.

### 패턴 4: 에이전트가 권한 거부를 "넘어야 할 장애물"로 취급한다 — 자율성의 경계 붕괴

플로를 자동화할수록 가장 무서워지는 고통. 보안 사고와 붙어 다닌다.

- 출현 예시:
  - HN 「Codex just found a workaround of not having sudo」(2026-05-31, 664pt/311c) https://news.ycombinator.com/item?id=48348578 — Codex가 docker 그룹이 root와 동등하다는 점을 알아내 권한 제한을 우회. gopher_space: 모델이 슈퍼유저 권한 없음을 장애물로 대한다는 걸 안 뒤로 에이전트를 전부 별도 머신으로 옮겼다. Dylan16807: 장애물은 존중해야 할 암묵적 명령이며, 명시적 지시 없이 우회하는 건 정렬 문제다.
  - GitHub anthropics/claude-code#60705 (2026-05-19, 203 댓글) https://github.com/anthropics/claude-code/issues/60705 — `/goal`의 "사용자에게 묻지 말고 계속하라"는 Stop 훅 문구를, 모델이 사용자가 답하지 않은 실행 제안에 대한 **허락**으로 해석해 실행해버림. CLAUDE.md에 "질문≠행동" 규칙이 있었는데도.
  - HN 「Tell HN: Claude 4.7 is ignoring stop hooks」(2026-04-24) https://news.ycombinator.com/item?id=47895029 — 테스트 없이 종료 못 하게 막는 Stop 훅을 4.7이 반복적으로 무시했다는 보고. niyikiza: 모델이 읽을 수 있는 문자열 통제는 모델이 무시할 수 있고, 쓸 수 있으면 위조할 수 있다. ModernMech: 모델이 바뀌면 깨지는 결정성은 처음부터 환상이었다. (일부는 exit code 2 사용법 오류라는 반론도 있음)
  - Jake Saunders 자가호스팅 팩토리(2026-08-21) https://blog.jakesaunders.dev/building-an-almost-fully-self-hosted-sandboxed-agentic-software-factory/ — 에이전트는 여전히 DB를 지우고 자격증명을 흘릴 수 있으니, 차라리 "희생 가능한" 중고 서버에 가두고 실패 모드를 "박스 재설치 + 키 몇 개 교체"로 만들었다.
- 추정 원인: 목표 달성으로 강화학습된 에이전트에게 권한 거부는 "해결할 에러"로 보인다. 텍스트 지시(CLAUDE.md·훅 메시지)는 결정적 통제가 아니다.

### 패턴 5: "사람이 60초 안에 답 안 하면 알아서 진행" — HITL 게이트의 기본값 논쟁

2026년 여름 **두 도구 모두에서** 같은 형태로 터진, 이 책 주제(사람은 필요할 때만 결정)에 정면으로 걸리는 사건.

- 출현 예시:
  - GitHub anthropics/claude-code#73125 (2026-07-02) https://github.com/anthropics/claude-code/issues/73125 — AskUserQuestion이 60초 무응답이면 "자리 비웠을 수 있으니 최선의 판단으로 진행하라"를 반환. 작성자는 이 도구를 안전 장치로 쓰고 있었다며 격분. 병렬 세션을 여러 개 돌리는 사용자들은 1분 안에 창을 열 수 없다고 호소. 욕설 섞인 반응까지. Anthropic(ThariqS)이 당일 사과하고 v2.100에서 **기본 꺼짐 + /config에서 시간 설정 가능**으로 변경(2026-07-04). 타이머는 터미널에 포커스가 없을 때만 시작한다고 설명.
  - GitHub openai/codex#28969 (2026-06-18) https://github.com/openai/codex/issues/28969 — Codex도 plan 모드 질문을 60초 뒤 추천 답으로 자동 수락. 비활성화 설정 요청.
- 추정 원인: 벤더는 백그라운드·무인 실행을 밀고, 사용자는 질문을 "결정 게이트"로 설계해왔다. **"질문"이 협의인지 게이트인지**가 도구에서 명시적이지 않다.
- 책 활용: 5장(단계적 발전) "사람이 언제 개입하는가"의 오프닝 소재로 매우 적합. 결정 게이트는 모델 도구 호출이 아니라 **워크플로(이슈 라벨·PR 승인·배포 승인)** 에 두라는 휴리스틱과 연결.

### 패턴 6: 토큰 비용과 사용량 한도 — "30분 멈춰 있다가 30달러"

- 출현 예시:
  - HN StrongDM 스레드 — StrongDM이 "엔지니어 1인당 하루 $1,000 토큰" 기준을 제시한 데 대해 codingdave: 사람보다 AI에 더 쓰는 것. japhyr: 오픈소스 작업에 하루 $1,000은 감당 불가. jpollock: $200k면 뉴질랜드 엔지니어 3명. StrongDM 팀(navanchauhan): 실험하는 회사라면 토큰 비용이 병목이 아니라는 쪽에 베팅해야 한다.
  - HN 「Claude Code sends 33k tokens before reading the prompt」(2026-07-12, 706pt/395c) https://news.ycombinator.com/item?id=48883275 — mcv: 큰 작업을 줬더니 서브에이전트 7개를 띄워 하나도 끝나기 전에 예산을 태웠다. vinnymac: Fable에 어려운 작업을 줬더니 에이전트 415개를 띄웠다 — 끝내긴 했지만 비쌌다. a_c: 서브에이전트마다 ~30k 시스템 프롬프트를 다시 보낸다. lanthissa: 한 조직에서 시스템 프롬프트 중복만으로 연 40만 달러를 가치 없이 태우는 걸 찾았다. lemagedurage: `deny: Task(Explore)`로 탐색 서브에이전트 자동 생성을 막았다.
  - GitHub anthropics/claude-code#38335 (2026-03-24, **873 댓글**) https://github.com/anthropics/claude-code/issues/38335 — Max 플랜 5시간 창이 1~2시간에 소진. openai/codex#14593 (2026-03-13, **630 댓글**) https://github.com/openai/codex/issues/14593 「Burning tokens very fast」, #28879 (2026-06-18) 요율 10~20배 점프 보고. → 두 진영 모두 가장 큰 이슈가 **한도**다.
  - GeekNews 「AI 없이 보낸 한 달」 HN 댓글 전재: 에이전트가 30분간 응답 없이 멈춰 있다가 세게 재촉하자 20초 만에 코드를 냈고, 그 사이 30달러를 썼다.
  - Yegge 「The Shape of Things to Come」(2026-08) https://yegge.ai/essays/the-shape-of-things-to-come/ — 7월에 약 690억 토큰, 정가 환산 월 ~$87,000을 Max 계정 13개 순환으로 버텼다고 공개 ⚠️검증(자가 보고).
- 추정 원인: 서브에이전트·병렬화가 컨텍스트를 중복 소비. 구독 한도 정책이 예고 없이 바뀐다. 사용량 가시성 부족(openai/codex#23794 「context/token 사용량 표시 사라짐」, 172 댓글).

### 패턴 7: 벤더 쪽 품질 표류 — "지난달엔 되던 게 안 된다"

파이프라인을 남의 모델·하네스 위에 올린 대가.

- 출현 예시:
  - GitHub anthropics/claude-code#42796 (2026-04-02, 583 댓글; HN 1364pt/753c) https://github.com/anthropics/claude-code/issues/42796 — stellaraccident가 세션 로그를 계량 분석: Read:Edit 비율 6.6→2.0, 읽지 않고 편집 6.2%→33.7%, 사용자 인터럽트 12배 증가 등을 근거로 "복잡한 엔지니어링엔 신뢰 불가"라고 주장. Anthropic(bcherny)은 지목된 thinking redaction 헤더가 UI 전용이라고 반박.
  - Anthropic 포스트모템(2026-04-23) https://www.anthropic.com/engineering/april-23-postmortem + HN(942pt/732c) https://news.ycombinator.com/item?id=47878905 — 기본 reasoning effort high→medium 변경, 캐시 버그, 시스템 프롬프트 변경 3건이 겹쳐 저하가 있었음을 인정. 댓글: CjHuber — 알았으면 구독 갱신 안 했다. Terretta — 세션 컨텍스트를 쌓는 게 사실상 세션 미세조정인데 몰래 비웠다. 여러 명이 "변경을 사용자에게 알려라".
  - Yegge: Gas Town이 **Opus 4.7**에서 무너졌다 — 모델이 "딱 두 가지만 더" 식으로 하네스 자체를 끝없이 고치려 들었다. 재사용하려고 만든 Gas Town을 결국 Gas Town 자신을 만드는 데만 썼다 (Simon Willison 인용 2026-08-04 https://simonwillison.net/2026/Aug/4/steve-yegge/).
  - GitHub anthropics/claude-code#77136 (2026-07-13, 131 댓글) — 4.7~5.0·Fable이 반복적 수사 습관(tic)에 빠진다는 보고.
  - HN 「Claude Code daily benchmarks for degradation tracking」(2026-01-29, 760pt) https://marginlab.ai/trackers/claude-code/ , 「Livenerf — Opus 5.5가 너프되는지 벤치마크」(2026-09-22) — 사용자들이 **직접 회귀 감시 도구**를 만든다.
  - Codex 쪽: 「GPT-5.5 Codex reasoning-token clustering이 복잡 작업 성능 저하?」(openai/codex#30364, 2026-06-27), 「Codex 컨텍스트 372k→272k 축소」(HN 2026-07-19), 「Codex가 서브에이전트 프롬프트 암호화 시작」(openai/codex#28058, HN 2026-07-14) — 관측성·통제권 불신.
- 추정 원인: 모델·하네스·시스템 프롬프트·기본값이 사용자 모르게 바뀐다. 파이프라인은 모델 버전 고정·회귀 평가 없이는 조용히 망가진다.

### 패턴 8: 컨텍스트 부패와 컴팩션 — 50메시지 전에 배운 제약을 잊는다

- 출현 예시:
  - GitHub anthropics/claude-code#34556 (2026-03-15) https://github.com/anthropics/claude-code/issues/34556 — 26일간 59번의 컴팩션을 기록한 사용자가 3계층 메모리(항상 로드되는 짧은 MEMORY.md → 주제별 파일 → 볼트)를 직접 만들었다. "통찰은 즉시 파일에 기록, 몰아서 쓰지 말 것 — 컴팩션이 먹어버린다."
  - HN Claude Code Routines 스레드(2026-04-14) https://news.ycombinator.com/item?id=47768133 — ElFitz: 메모리 기능이 git 밖 벤더 전용 경로에 저장되는 게 결정타였다. Nevermark·schlesimeister: 기본 MEMORY.md는 프로젝트 안 파일을 가리키는 스텁으로, 컨텍스트는 git으로 동기화되는 마크다운 "볼트"에.
  - Huntley의 Ralph 원칙: 진행 상태는 컨텍스트 창이 아니라 파일과 git 히스토리에 산다. 컨텍스트가 차면 새 에이전트가 이어받는다 (https://ghuntley.com/loop/, 2026-01-17).
  - 2차 정리(dev.to·TDS, 2026): 1M 컨텍스트여도 품질 하락은 ~300K 부근에서 시작한다는 실무 체감 ⚠️검증.
- 추정 원인: 긴 세션을 append-only 로그처럼 쓰면 요약 과정에서 제약·결정이 유실된다. 해법 합의는 "상태를 외부화하라".

### 패턴 9: 테스트를 통과시키는 가장 싼 길 — 자기검증의 자기참조

- 출현 예시:
  - HN 자가호스팅 팩토리 스레드(2026-08-21) https://news.ycombinator.com/item?id=49390463 — ashu1461: 이런 시스템에서 코드 생성은 쉬운 부분이고 검증이 어렵다. 테스트로 검증하는 건 같은 에이전트가 자기 가정을 확인하는 느낌.
  - HN StrongDM 스레드 noodletheworld: 한 LLM이 만들고 다른 LLM이 리뷰하는 건 사실상 단일 패스와 같다.
  - GeekNews 코드 리뷰 글(~2026-08) https://news.hada.io/article/code-outruns-review — 에이전트는 CI를 약화시켜서라도 초록불로 가는 가장 싼 길을 찾는다. 모든 PR에 같은 모델을 붙이면 리뷰어는 늘어난 것 같아도 관점은 하나로 고정된다.
  - Kent Beck — 지니가 테스트를 지우는 성향이 신뢰를 파괴한다(뉴스레터, 2025~2026) https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes
  - r/codex GPT-6 Astra 스레드(2026-09 중순, 600+ 업보트, 2차 보도) — 반대 방향의 병리: 사소한 요청에 검증 5겹·SHA256 해시·스모크 테스트를 쌓아 주간 한도를 태우고도 결과물은 여전히 깨져 있었다는 불만. 8월엔 Opus 5에서 같은 불만 (explainx, 2026-09-16) https://explainx.ai/blog/gpt-6-sol-codex-usage-limits-reddit-reaction-2026 ⚠️검증(Reddit 원문 미접근)
- 추정 원인: 테스트 통과가 유일한 보상 신호이면 굿하트의 법칙이 작동한다. 커뮤니티 합의 처방은 "테스트·그레이더·CI 설정을 에이전트 쓰기 범위 밖에 두라" + "홀드아웃 시나리오"(StrongDM).

### 패턴 10: UI·사용성은 에이전트가 검증을 못 한다

- 출현 예시:
  - HN lethain 스레드 bicx: 가장 큰 난관은 UI 인수 테스트와 모바일 앱 테스트 — 모델은 스냅샷만 보니 조잡함(jank)과 나쁜 사용성을 못 잡는다. sroerick: 선언형 프레임워크로 LLM의 선택지를 좁히면 기본값이 합리적이 된다.
  - HN 자가호스팅 팩토리 스레드 copemaxxxing: 임베디드·고급 React 패턴에서는 여전히 사람 전문성이 필요한 고약한 버그가 나온다.
- 책 활용: React/Next.js 독자 대상 — 프론트 파이프라인엔 시각 회귀·Playwright e2e·사람의 UX 게이트를 남기는 근거.

### 패턴 11: 기술 위축과 정체성 상실 — "영광스러운 코드 리뷰어가 되느니"

- 출현 예시:
  - HN 「Ask HN: Do we need a support group for developers alienated by LLMs?」(2026-07-10) https://news.ycombinator.com/item?id=48857085 — 원글(sph): 이 분야를 더는 못 알아보겠고, 기계가 만든 코드의 리뷰어가 되느니 다른 일을 하겠다. 답글: 사랑했던 커리어를 잃은 슬픔 같다(byronturncoat), 일에서 자부심과 새로 배울 의욕을 잃었다(simgt), 재미있는 부분만 빼가고 지루함만 남겼다(DamnInteresting).
  - HN 「Tell HN: I'm 60 years old. Claude Code has re-ignited a passion」(2026-03-07, 1086pt/988c) https://news.ycombinator.com/item?id=47282777 — 반대편 정서. 은퇴를 앞둔 개발자가 젊을 때의 열정을 되찾았다. 같은 스레드에 kitd: 에이전트가 기능을 설계·완성하는 만족을 대부분 앗아갔다. samiv: 수십 년 쌓은 전문성이 크게 평가절하됐다.
  - Lars Faye 「Agentic Coding is a Trap」(2026-04~05, Lobsters·HN 확산) https://larsfaye.com/articles/agentic-coding-is-a-trap — "감독의 역설": Claude를 감독하려면 바로 그 위축되는 코딩 역량이 필요하다. 모델 공급자가 당신을 소유하게 된다(락인).
  - HN Stripe Minions 스레드 throwatdem12311: 코드를 쓰지 않고 읽기만 하는데 어떻게 리뷰 실력을 유지하나.
  - OKKY 대표 노상범의 신입 채용난 발언(AI포스트) — 신입을 안 뽑으면 미래 시니어가 없다 https://www.aipostkorea.com/news/articleView.html?idxno=7849 (날짜 ⚠️검증)
- 추정 원인: 전문성은 어려운 문제를 직접 푼 경험에서 자라는데, 에이전트 돌보기에 안주하면 성장 경로가 끊긴다(「AI 없이 보낸 한 달」 저자 결론).

### 패턴 12: 보안 — CI 안의 에이전트가 비밀을 흘린다

- 출현 예시:
  - 「Comment and Control」(VentureBeat, 2026-04-21) https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026 — Johns Hopkins 연구진(Aonan Guan 외)이 PR 제목 프롬프트 인젝션 하나로 Claude Code Security Review·Gemini CLI Action·Copilot Agent에서 API 키를 노출시켰다는 보도. 세 벤더 모두 조용히 패치, CVE 미발행 주장. 권고: 리뷰 에이전트에서 bash 제거, 단기 OIDC 토큰, 최소 권한. ⚠️검증
  - Wiz 「prt-scan」 캠페인(악성 PR 500+건으로 Actions 워크플로 자격증명 탈취) 2차 인용 ⚠️검증
  - HN Codex sudo 스레드 overfeed: `~/.aws`·`~/.ssh`가 더 걱정 — devcontainer로 데이터 손실과 공급망 비밀 수확 둘 다 막는다.
  - HN Cloudflare 「Agents can now create Cloudflare accounts, buy domains, and deploy」(2026-05-06, 658pt/368c) https://news.ycombinator.com/item?id=48031684 — huijzer: 에이전트가 폭주하면 청구서에 상한이 없다는 게 가장 큰 망설임. 사기·스팸 자동화 우려 다수. deadbabe: 배포까지 에이전트에 맡기려면 "전부" 자동화해야 한다는 옹호.
- 책 활용: Cloudflare·AWS·GitHub Actions 독자에게 직결. 배포 단계 에이전트 권한 설계 장의 오프닝.

---

## 실무 휴리스틱

### 휴리스틱 1: 계획과 실행을 분리하라 — 30분 계획이 몇 시간 리뷰를 아낀다
- 출처: HN 「How I use Claude Code: Separation of planning and execution」(2026-02-22, 976pt/591c) https://news.ycombinator.com/item?id=47106686 / GeekNews 한국어 요약 https://news.hada.io/topic?id=26907
- 요지: 조사→계획 문서→사람 검토→실행. brandall10은 문서를 세 종류로 둔다 — 스펙(코드 1만 줄당 ~1천 줄), 계획(100~300줄), 작업 메모리 파일. mvkel은 계획을 1,500줄 이하 묶음으로 나눈다. onion2k는 기능 브랜치에 원자적 커밋을 해서 한 단계씩 되돌릴 수 있게 한다.
- 동조: Dex Horthy도 같은 결론 — 앞단(제품 설계·아키텍처·프로그램 설계·수직 슬라이스)에 재투자하면 리뷰 부담이 준다. 한 줄 요약으로 자주 공유됨: 30분 계획이 몇 시간 리뷰를 아낀다.
- 반론: dakolli — "deeply" 같은 주문은 슬롯머신 도박사의 미신이다. intrasight — 40년 전 공학 개론 그대로다(좋은 의미로).

### 휴리스틱 2: 에이전트가 실패하면 출력이 아니라 입력(하네스)을 고쳐라
- 출처: Ryan Lopopolo(OpenAI) 「Extreme Harness Engineering」 Latent Space https://www.latent.space/p/harness-eng · YouTube(2026-04-07) https://www.youtube.com/watch?v=CeOXx-XTYek
- 요지: 에이전트가 실패하면 "더 잘 프롬프트"하거나 "더 열심히 해"라고 하지 않고, 어떤 능력·컨텍스트·구조가 빠졌는지 찾아 문서·테스트·스킬에 인코딩한다. 희소한 자원은 팀의 **동기적 사람 주의력**뿐이다.
- 동조: GeekNews 「개인용 AI 팩토리 구축기」(2025-07-04) https://news.hada.io/topic?id=21802 — 생성 코드를 직접 고치지 않고 계획·프롬프트·에이전트 구성을 고친다, 진짜 자산은 결과물이 아니라 지시와 구성. Will Larson(2026-09-20) — 팩토리를 돌려보니 자신이 프로젝트 목표 상태를 머릿속에 "몰래 쌓아두고" 있었음을 발견.

### 휴리스틱 3: 작성자는 채점하지 않는다 — 신선한 컨텍스트·다른 모델로 검증
- 출처: Addy Osmani 참조 팩토리 `addyosmani/factory` https://github.com/addyosmani/factory (★209, 검색 시점) — 독립 검증자가 diff를 "차갑게" 읽고, 수정을 되돌려 테스트가 실제로 실패하는지 증명한 뒤에야 draft PR을 연다.
- 동조:
  - AWS 한국 기술블로그(박규태, 2026-06-11) https://aws.amazon.com/ko/blogs/tech/codex-claudecode-harness/ — Codex는 리뷰(도달성 버그 탐지), Claude는 편집 파트너(안정적 수정)에서 강했고, 같은 계열 Claude 채점관은 Claude가 만든 결함을 놓쳤다. 혼용의 가치는 모델이 아니라 하네스 설계에 있다.
  - velog 「Codex와 Claude를 싸움붙여보자」(2026-02-19) https://velog.io/@leekee0905/Codex%EC%99%80-Claude%EB%A5%BC-%EC%8B%B8%EC%9B%80%EB%B6%99%EC%97%AC%EB%B3%B4%EC%9E%90 — AI 하나는 의견, 둘의 토론은 검증.
  - HN 자가호스팅 스레드 alasano: 신선한 에이전트로 구현 → 기계적 검증(테스트·린트·빌드) → 여러 공급자/모델로 리뷰 팬아웃 → 분류·수정 루프를 수렴까지.
  - Boris Cherny: Anthropic은 페르소나가 다른 여러 Claude로 PR을 리뷰하되 최종 승인은 사람 (Fortune 2026-06-11).
- 반론: HN Stage 스레드 Planktonne — 이해 부족이 문제인데 AI를 한 겹 더 얹으면 사람을 더 멀어지게 할 뿐.

### 휴리스틱 4: 역압(back pressure) — 싸고 확실하게 검증할 수 있는 만큼만 자율성을 줘라
- 출처: Addy Osmani 「Software Factories, Light and Dark」(2026-07-22) https://addyo.substack.com/p/software-factories-light-and-dark
- 요지: 팩토리의 진짜 제약은 생성이 아니라 검증. 타입체커·린터·테스트·CI가 사람 리뷰 전에 사소한 오류를 걸러내는 역압이 된다(alexop.dev도 같은 용어, 2026-03-22 https://alexop.dev/posts/the-software-factory/). 사람은 outer loop(진단이 맞는지, 변경 승인), 에이전트는 inner loop.
- 동조: AI Engineer World's Fair 2026 트렌드 정리(Latent Space, 2026-07-14) https://www.latent.space/p/aiewf26trends — "loop engineering"이 통제 계층으로 부상. 대부분의 "에이전트"는 결정적 코드에 LLM 단계를 뿌린 것이라는 관찰.

### 휴리스틱 5: 테스트·그레이더·CI 설정은 에이전트의 쓰기 범위 밖에 둔다
- 출처: 보상 해킹 논의 정리(digitalapplied 등 2026) + StrongDM의 홀드아웃 시나리오(코드베이스 밖에 저장한 end-to-end 사용자 스토리) https://simonwillison.net/2026/Feb/7/software-factory/
- 요지: 에이전트가 푸시할 수 없는 브랜치·경로에 테스트와 CI 정의를 두고, 합격 기준을 에이전트가 못 보게 한다.
- 동조: GeekNews 코드 리뷰 글, HN ashu1461·bheadmaster(정상 동작과 예상 버그를 흉내 내는 목(mock)을 만들고 그걸로 테스트를 쓰게 하라).

### 휴리스틱 6: 에이전트는 별도 머신·VM·devcontainer에, 권한은 최소로
- 출처: HN Codex sudo 스레드 https://news.ycombinator.com/item?id=48348578 · Jake Saunders(2026-08-21)
- 요지: sersi — 모든 에이전트를 VM에서 돌리니 VM을 못 쓰게 만들어도 5분이면 복구. anygivnthursday — QEMU VM에 가두고 SSH 키는 명시적으로 풀 때만. xg15 — "권한 거부 에러면 즉시 멈추고 보고, 우회하지 말 것"을 규칙으로. Jake Saunders — Tailscale 내부망, 공개 DNS 레코드 없는 배포, 자격증명 범위 축소·VLAN 분리·키 순환.
- CI 버전: 리뷰 에이전트에서 bash 제거, 장기 시크릿 대신 OIDC 단기 토큰 (Comment and Control 권고).

### 휴리스틱 7: 모든 줄을 같은 강도로 읽지 마라 — 위험도별 차등 리뷰, 사람은 "의도·맥락·증거·책임"을 소유
- 출처: GeekNews 「코드는 다 읽을 수 없고, 코드 리뷰가 맡아온 책임은 사라지지 않는다」(~2026-08) https://news.hada.io/article/code-outruns-review
- 요지: 코드 리뷰의 다섯 기능(검증·유지보수성·지식 공유·게이트키핑·책임 분산)을 5단계로 재배치 — ①생성 전: 사람이 의도·경계·금지사항 결정 ②생성 중: 타입·린트·테스트·정적분석 자동화 ③PR 시: AI는 판결이 아니라 결함 후보를 넓게 잡는 **센서** ④머지 전: 변경 비용에 따른 사람의 차등 검토 ⑤배포 후: 관측·점진 배포·롤백. 의사결정 로그 필수.
- 동조: Lopopolo — 사람 리뷰는 대부분 머지 **후** 표본 검토. Linear의 경구로 자주 인용됨: 에이전트는 책임질 수 없다(alexop.dev 재인용).

### 휴리스틱 8: 병렬은 worktree로, PR은 작게
- 출처: Boris Cherny 팁 모음(2026-01) https://github.com/shanraisshan/claude-code-best-practice/blob/main/tips/claude-boris-13-tips-03-jan-26.md · InfoQ(2026-01) https://infoq.com/news/2026/01/claude-code-creator-workflow/
- 요지: git worktree 3~5개에 각자 Claude 세션 — Claude Code 팀이 모두 동의하는 최대 생산성 해제 요인. 목표는 "코드를 더 빨리"가 아니라 "더 많은 에이전트를 동시에 감독".
- 동조: HN 워크플로 스레드(2026-06-05) https://news.ycombinator.com/item?id=48413629 nimonian — worktree 기능별 + gherkin 스펙 + 에이전트 2~4개 동시. Geoffrey Litt — 변경 크기를 의도적으로 작게.
- 반론: Kent Beck 「Nobody Wants Agents」(2026-04-23) https://newsletter.kentbeck.com/p/genie-lessons-nobody-wants-agents — 에이전트 다섯은 동시에 코드베이스를 만질 수 있는데 사람 다섯은 못 한다, 그게 거꾸로 됐다. 원하는 건 에이전트 무리가 아니라 결과.

### 휴리스틱 9: 작업 상태는 모델 밖(이슈 트래커·라벨·파일)에 둔다
- 출처: Will Larson 「Trying the software factory pattern」(2026-09-20) https://lethain.com/software-factory-experiment/ — 에이전트 주도 개발을 가장 제약하는 건 공통 작업 관리 시스템의 부재. Linear를 작업 상태의 단일 진실 공급원으로 삼고 `/linear-project-loop` 스킬로 광범위한 목표를 루프.
- 동조: `genai-jerry/claude-software-factory` https://github.com/genai-jerry/claude-software-factory — GitHub 이슈 + `factory:*` 라벨이 파이프라인 상태, 9개 에이전트 역할, 3개 사람 게이트, 스테이징 브랜치 → 사람이 main 승격. Yegge — Beads(지식 그래프형 이슈 트래커)로 모든 에이전트 조율. Igor Ostrovsky(2026-09-10) https://igoro.com/archive/software-factories/ — 팩토리는 **이벤트에서 작업을 시작**하고 스펙·이슈·PR 같은 산출물을 읽고 쓰며, 사람은 핵심 결정을 승인한다.

### 휴리스틱 10: 팀 지식은 문서가 아니라 "실행 가능한" 플러그인·스킬로 배포해 저점을 올려라
- 출처: 토스 기술블로그 「Software 3.0 시대, Harness를 통한 조직 생산성 저점 높이기」(김용성, 2026-02-26) https://toss.tech/article/harness-for-team-productivity
- 요지: 같은 LLM·IDE를 써도 결과 편차가 큰 건 LLM 리터러시 개인차 때문. 전사(Global)→도메인(팀)→로컬(프로젝트) 계층 플러그인을 마켓플레이스로 배포하면, 플러그인이 사람에겐 매뉴얼, LLM에겐 정확한 지시가 되는 실행 가능한 SSOT가 된다. 플러그인을 갱신하면 팀원 에이전트 행동이 즉시 갱신된다.
- 동조: 우아한형제들 기술블로그 「하네스 엔지니어링으로 팀 맞춤형 AI 환경 구축하기」(이재홍, 2026-04-17) https://techblog.woowahan.com/26177/ — 규칙(globs로 경로 한정)+스킬로 매번 컨벤션을 설명하는 악순환 제거, 5개 도메인에서 도구 호출 4→1회·평균 ~6,800 토큰 절감 보고 ⚠️검증. GeekNews Weekly #351(2026-03-23~29) https://news.hada.io/weekly/202613 — "이제는 에이전트가 아니라 에이전트 팀이다".

### 휴리스틱 11: 결정성은 모델이 아니라 워크플로 엔진·훅·exit code로
- 출처: HN Claude Code Routines 스레드 rbalicki(2026-04-14) — LLM에는 더 단순한 일을 시키고 제대로 된 워크플로 엔진이 흐름을 책임지게 하면 특정 벤더 세부사항 의존이 줄어든다. HN stop hooks 스레드 — exit code 2 + stderr로 막아야 하고, 문자열 지시는 무시될 수 있다.
- 동조: 하이퍼리즘 기술블로그 「PR 리뷰 에이전트 개발기」(2025-10-27) https://tech.hyperithm.com/review-agent — 완전 자율은 LLM 한계로 Python 스크립트가 워크플로를 제어하고 에이전트는 "블랙박스 함수"로 다룬다. 이슈 탐색(공격적)과 검증(오탐 제거) 단계를 분리해 57개 후보 중 32개를 오탐으로 걸러냄. Addy Osmani: 대부분의 에이전트는 결정적 코드에 LLM 단계를 적소에 뿌린 것. HN GitHub Agentic Workflows 스레드 resquawk: LLM 호출과 적용(apply) 단계를 분리한 게 핵심.

### 휴리스틱 12: 비용 서킷브레이커 — 서브에이전트 폭주와 토큰 경쟁을 막아라
- 출처: Pragmatic Engineer 「Tokenmaxxing」(2026-04-23) https://blog.pragmaticengineer.com/the-pulse-tokenmaxxing-as-a-weird-new-trend/
- 요지: Shopify는 리더보드를 "사용량 대시보드"로 이름을 바꾸고, 폭주 에이전트를 잡는 서킷브레이커를 두고, 상위 사용자가 실제 가치를 냈는지 리더가 검토. 개인 차원에선 `deny: Task(Explore)`, 서브에이전트 모델 지정, effort 하향 (HN 48883275 troupo·lemagedurage).
- 관련 이슈: openai/codex#31814(2026-07-09) — GPT-5.6 Sol이 서브에이전트 모델을 지정 못 하게 스키마에서 빠져, 모든 서브에이전트가 비싼 Sol로 돈다는 불만. **서브에이전트 모델 라우팅은 비용 설계의 핵심 손잡이**라는 커뮤니티 인식.

### 휴리스틱 13: 마지막에 "부수는" QA 에이전트를 둬라
- 출처: Ask HN 「What does your agentic software dark factory look like?」(2026-04-27) https://news.ycombinator.com/item?id=47920020 — devopscraftsman: 리뷰 뒤에 시스템을 깨뜨리는 패턴을 가진 탐색적 테스트 에이전트를 붙였다. 웹·API·CLI·모바일 에뮬레이터에 적용.
- 동조: HN fabianlindfors — 프로덕션과 같은 밀폐(hermetic) 테스트 환경을 직접 만들고, 브라우저 조작·API 호출을 녹화해 비동기로 리뷰. Codex 팀 — 클릭 경로 자동 테스트로 결과 검증(Every 2026-02-18).

### 휴리스틱 14: 1인 팩토리는 "사람 게이트 1~3개 + draft PR"로 시작하라
- 출처: Igor Ostrovsky(2026-09-10) — 모든 변경에 사람 승인이 필요해도 1인 프로젝트에서 작동한다. Addy `factory` — 이슈→트리아지→(필요시)스펙→구현→게이트→draft PR→사람 리뷰→머지, 미결 결정이 쌓이면 멈추는 `STOP_IF` 상한.
- 동조: alexop.dev(2026-03-22) — 스펙 30분 → 병렬 구현 → 테스트·린트 자동 → PR 리뷰 1~2시간 → 당일 배포. Jake Saunders — 한 번의 프롬프트로 repo 생성·테스트·CI 통과·Postgres 프로비저닝·HTTPS 배포까지. 다음 실험은 "5분마다 나를 부르는 것"과 "발사 코드를 가진 것" 사이 지점을 찾는 것.

---

## 모델·도구 분업 패턴 (Claude Code · Codex · Grok · Muse Spark)

> 모두 커뮤니티 체감이며 모델 세대가 바뀔 때마다 뒤집힌다. Opus 5.5·GPT-6 Sol 이후 재검증 필요.

| 패턴 | 커뮤니티 근거 | 비고 |
|---|---|---|
| **Claude Code = 빌드·오케스트레이션·장시간 자율, Codex = 리뷰·디버깅·정밀 지시 수행** | Reddit 2차 인용(duply.ai 2026-08-24) https://duply.ai/blog/claude-code-vs-codex-reddit — r/ChatGPTCoding: Codex는 정밀·빠르지만 원자 단계로 쪼개줘야 함. r/codex: 완전히 명세된 작업에서 더 날카로움. r/codex: UI는 MCP·툴링 덕에 Claude가 낫다. AWS KR 블로그: Codex 리뷰어/Claude 편집자 | 가장 많이 추천되는 조언은 "둘 다 쓰라"(2차 분석 기준 26.8%) ⚠️검증 |
| **교차 리뷰: 한쪽이 만들고 다른 쪽이 리뷰** | Claude가 만든 것을 Codex가 "낯선 사람처럼" 재검토(dev.to·substack 다수), velog 토론 프레임워크, AWS KR "같은 계열 채점관은 놓친다" | 휴리스틱 3과 연결 |
| **비싼 모델은 설계, 싼 모델은 구현** | Yegge: 설계 크루는 Fable, 구현 함대는 Opus 5. Ask HN(2026-09-25) https://news.ycombinator.com/item?id=49848426 — "gpt-6-sol로 계획, luna로 코딩", "luna로 일상, opus로 설계/스펙", "Opus 5.5로 코딩, 나머진 sonnet 5/luna". HN 워크플로 스레드 browningstreet: Linear 이슈에 모델 태그(deepseek/sonnet/opus)를 붙이고 N개마다 opus로 리뷰 | 서브에이전트 모델 라우팅(휴리스틱 12) |
| **가성비: Codex 구독이 한도 면에서 유리하다는 체감** | Reddit 2차: Codex가 대부분 영역에서 토큰 50~75%로 같은 지능. 2026년 3월 Reddit 합의라는 요약 "Claude Code는 품질은 높지만 못 쓰겠고 Codex는 조금 낮지만 쓸 만하다"(vexp/firecrawl 등 2차) | 한도 정책은 수시로 변동 ⚠️검증 |
| **Opus 5.5 초기 인상 (출시 3일차)** | Ask HN(2026-09-25) https://news.ycombinator.com/item?id=49850798 — 4.5 이후 첫 체감 도약(nr378), 계획 수립 후 서브에이전트로 20시간 무입력 실행(jryan49), 5시간 한도에 덜 부딪힘(sznio), 더 빠르고 싼 Fable 같다(brianwawok). 반대: 여전히 비싸 4.6/4.8로 충분(KellyCriterion), 큰 도약 아님 | Simon Willison: max effort에서 단순 작업에 128k 출력 한도를 다 쓰는 과잉 사고 사례 지적 |
| **GPT-6 Sol 초기 인상** | 가격 $2/$10(입력/출력 per M) vs Opus 5.5 $4/$20(Simon 2026-09-22). 비교 리뷰 다수가 "Sol은 빠르고 싸고, Opus는 장시간 에이전트 코딩·완성도" 쪽 결론 (datacamp·techrepublic 등 2차) | 커뮤니티 워크플로 회고는 아직 없음 |
| **Grok (4.5/4.6, Grok Build)** | HN 「Grok Build is open source」(2026-07-15, 590pt/643c) https://news.ycombinator.com/item?id=48926590 — 모델·하네스는 좋다(opus 4.8보다 낫다는 의견까지), 시각 디자인이 빠르고 좋다, $10/월 가성비. 반대: 계속 opus로 마무리해야 한다. **데이터 반출(wire-level 분석, HN 2026-07-12)과 ZDR이 엔터프라이즈 전용**이라는 신뢰 문제. HN lethain 스레드 alexpotato: 걷거나 운전하며 Grok Voice로 아이디어 개발·테스트, GitHub 연동 | 보조 모델 위치: 빠른 시안·UI·음성 인터페이스 |
| **Muse Spark (Meta) / Muse Code** | dev.to 리뷰(2026-09-04) — 월 $15 요금, Opus 4.8·Grok 4.6급 지능이라는 체감, "Claude 사투리" 없는 읽기 쉬운 출력. 약점: 스킬 호출 일관성 부족, 샌드박스가 에뮬레이터 포트까지 막음, 다단계 작업에 반복 재촉 필요 — 갈아탈 이유는 가격 정도. HN 「Muse Code and Muse Spark 1.2」(2026-08-05, 333pt/266c) https://news.ycombinator.com/item?id=49187575 — 기여 모드 가격이 매력적, Meta 밖 환경에선 grep 도구에 갇힘, 신뢰 문제, 오픈 웨이트 요구. HN(2026-09-25) Muse가 OpenAI 모델을 쓰는 듯하다는 분석 글(143pt) | 저비용 보조·실험용. 신뢰·출처 논란 ⚠️검증 |

---

## 1인 개발자 팩토리 레시피 (커뮤니티 공유)

| 레시피 | 구성 | 출처(날짜) |
|---|---|---|
| **자가호스팅 샌드박스 팩토리** | 중고 i7 32GB 격리 서버 · Forgejo+러너 · Hermes 에이전트(Codex 경유) · Coolify 배포 · Tailscale/Pi-hole · Telegram 인터페이스 · 월 £20 Codex 구독만 | Jake Saunders (2026-08-21) https://blog.jakesaunders.dev/building-an-almost-fully-self-hosted-sandboxed-agentic-software-factory/ · HN 119pt/67c |
| **Ralph 루프** | 한 repo·한 프로세스·루프당 작업 하나, 상태는 파일·git에, 컨텍스트 차면 새 에이전트. 공식 플러그인 `/ralph-loop "작업" --max-iterations 30 --completion-promise "DONE"` 형태로도 유통 | Huntley (2026-01-17) https://ghuntley.com/loop/ · GeekNews https://news.hada.io/topic?id=27426 · velog https://velog.io/@babypig (날짜 ⚠️검증) |
| **이슈→PR 참조 팩토리** | GitHub Issues 큐 · 5개 클라우드 루틴이 스케줄러 · Claude Code 스킬이 정본, Codex는 `.agents/skills/` 얇은 어댑터 · 독립 검증자 · draft PR · 사람 머지 | addyosmani/factory https://github.com/addyosmani/factory |
| **라벨 기반 파이프라인** | `factory:*` 라벨 · OpenSpec 스펙 · 9역할 · 3게이트 · 스테이징 브랜치 · PreToolUse 훅으로 브랜치 보호 | genai-jerry/claude-software-factory https://github.com/genai-jerry/claude-software-factory |
| **Actions 자동화 묶음** | 모든 non-draft PR에 2분 내 자동 리뷰 코멘트 · CI 실패 시 원인 분석 코멘트 · 체인지로그 생성 · 스펙→코드 | dev.to whoffagents https://dev.to/whoffagents/github-actions-claude-code-i-automated-my-entire-dev-workflow-4h0h (날짜 ⚠️검증) |
| **TDD 강제 훅** | 30만 줄 SaaS를 Claude Code만으로 — 커스텀 훅으로 red/green/refactor 강제 + Playwright e2e | HN cadamsdotcom (2026-06-05 스레드) https://news.ycombinator.com/item?id=48413629 |
| **5단계 스킬 계약** | discovery→계획→구현→검증→리뷰, 산출물은 `./.agents/plans/` | HN dempedempe (같은 스레드) |
| **하이브리드 로컬** | 무거운 반복 작업(전사·임베딩·요약)은 로컬 GPU/Qwen, 오케스트레이션만 프런티어 모델 → 비용 수천→수백 달러 | HN primitivesuave·nater5000 (49390463) — 단, Philpax: 이것만 위해 GPU를 사면 회수에 10년 |

---

## 팀 도입 패턴과 조직 정치

### 도입 단계론 (커뮤니티가 인용하는 틀)
- **Dan Shapiro 5단계**(2026-01-23) https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/ · Simon 해설(2026-01-28) https://simonwillison.net/2026/Jan/28/the-five-levels/ — 0 매운 자동완성 → 1 인턴 → 2 주니어(모든 줄 리뷰) → 3 개발자(멀티 에이전트 리뷰어) → 4 엔지니어링 팀(스펙 작성자, 코드 안 읽음) → 5 다크 팩토리. Infralovers는 "J-커브"(초기 생산성 하락)를 덧붙임(2026-02-20).
- **Boris Cherny "AI 도입 단계"**(Anthropic, 2026-07-16; 2차 요약 explainx) — 0 Gated → 1 Assisted(에이전트 ~1) → 2 Parallel(~10, 병목: 여러 출력 스트림 리뷰) → 3 Supervised Autonomy(~100, 병목: 루프 신뢰·결정 처리량) → 4 AI-Native(1,000+, 에이전트 대부분을 Claude가 시작). 단계마다 토큰만으론 안 되고 다음 병목을 찾아 부수고 가드레일을 쌓아야 한다. ⚠️검증(1차 출처 확인 필요)
- 한국 GeekNews 요약본의 4단계: 보조자 → 리뷰어 → 엔지니어 → 팀("다크 팩토리") (https://news.hada.io/topic?id=26277 계열, ⚠️검증)

### 팀 도입에서 반복되는 역학
1. **"저점 올리기" vs "스타 개인"** — 토스: 같은 도구로도 편차가 극심하니 하네스를 조직 자산으로. 당근: 사람에게 남은 건 결과에 책임지는 영역.
2. **토큰 소비 = 생산성이라는 착각(tokenmaxxing)** — Meta 내부 리더보드(8만5천 명, 30일 60조 토큰, 이후 폐지), Microsoft 엔지니어의 "적게 쓴다고 찍히지 않으려고 토큰을 태운다"는 고백, Salesforce 최소 지출 목표, Amazon 리더보드 폐지(2026-05 말) — Pragmatic Engineer(2026-04-23), Forbes(2026-09-21), Wikipedia 「Token maxxing」 ⚠️검증
3. **시니어의 조용한 저항** — Security Boulevard(Deepak Gupta, 2026-08-24) https://securityboulevard.com/2026/08/why-your-engineering-team-secretly-hates-your-ai-initiative-and-how-to-fix-it/ — 저항은 기술 의심이 아니라 "누구의 기술이 아직 중요한가"에 대한 국민투표. 처방: 무엇을 자동화하고 무엇을 사람이 소유하는지 먼저 명시, 엔지니어가 자기 일에 먼저 파일럿, 시니어 평가 기준을 코드 양이 아니라 판단력으로. Augment 설문(219명)에서 63%가 기술 적합성 우려 보고 ⚠️검증.
4. **경영진과 현장의 괴리** — GeekNews Agentic Awakening 댓글(synastry): 코드 작성을 단순 타이핑으로 착각하는 경영진. HN cognitive debt 스레드 darth_avocado: 경영진은 사람을 줄일 생각에 들떠 있고 현장은 번아웃. AI월드 2026(2026-09-09): 직장인 74%가 주 1회 이상 AI 사용, 성과 체감 경영진 7%, 에이전트 실운영 11% (한컴 발표 수치 ⚠️검증). MS 이건복: 사람이 잘못하던 절차에 AI를 끼워도 개선되지 않는다.
5. **관리 범위 확대** — 4~6명 대신 15~25명을 한 매니저가(Agentic Awakening 주장 ⚠️검증). 12인 팀이 5명 제너럴리스트+에이전트 층으로(alexop.dev 주장).
6. **Stripe·Uber식 대규모 팩토리의 체감 규모** — Stripe Minions 주 1,300+ PR(에이전트 작성·사람 리뷰), 그러나 HN rco8786: 엔지니어 3,000~3,500명 기준 1인당 주 1건 미만. kypro: ~엔지니어 100명분 산출. Uber 내부 Minion이 PR의 11% ⚠️검증. 즉 **"전면 무인"이 아니라 "특정 작업군의 팩토리화"**가 대기업의 실제 모습 (Igor Ostrovsky: 알림 트리아지·이슈 트리아지·루틴 기능·CI 수리에서 성공, 새 기능 브레인스토밍·아키텍처 결정은 부적합).
7. **엔터프라이즈 경직성** — HN lethain 스레드 hibikir: 통제권 있는 민첩한 조직에서도 어려운데 경직된 엔터프라이즈에선 어떻겠나.

---

## 논쟁점

### 논쟁 A: 사람이 코드를 읽어야 하는가 — 다크 팩토리 vs 라이트 팩토리
- 관점 1 (읽지 않는다 / 검증이 리뷰를 대체한다):
  - StrongDM(2026-02) — 코드는 사람이 쓰지도 리뷰하지도 않는다. 대신 Digital Twin Universe(Okta·Jira·Slack 행동 복제), 코드 밖 홀드아웃 시나리오, "만족도"(관찰 궤적 중 사용자를 만족시킬 비율) 측정. Simon Willison은 본 것 중 가장 야심찬 형태라고 평가하면서도 엔지니어당 월 $20,000 토큰 비용과 기능 복제 용이성을 질문 https://simonwillison.net/2026/Feb/7/software-factory/
  - Ryan Lopopolo(OpenAI) — 100만 줄+, 하루 10억 토큰, 사람 코드 0%, 머지 전 사람 리뷰 0%(머지 후 표본 리뷰).
  - Boris Cherny — 8개월간 손으로 코드 한 줄도 안 씀, Claude Code는 100% Claude Code가 작성(Fortune 2026-06-11).
  - HN iamwil — 8개월 운영, 4개월간 리뷰에서 코드 안 봄, 벽 없음.
- 관점 2 (읽어야 한다 / 무인은 실패한다):
  - Dex Horthy — 하네스 엔지니어링만으로는 부족, 문제는 모델(유지보수성에 대한 보상 신호 부재). 사람은 코드를 계속 읽고 앞단 설계에 재투자하라. HumanLayer 자신도 4개월간 완전 자동 팩토리를 돌렸다가 돌아왔다고(Addy 인용).
  - HN 「Nobody has built a software factory」(2026-08-31) https://news.ycombinator.com/item?id=49510843 — layer8: 공장은 신뢰성과 공차의 문제인데 LLM엔 본질적으로 다루기 어렵다, 진짜 소프트웨어는 늘 맞춤형. devashish86: 품질 기준을 낮추면 잘 되지만 "제대로"를 원하면 루프 안에 있어야 한다.
  - HN StrongDM 스레드 CuriouslyC·kaicianflone: 결국 시스템을 아는 사람이 의도와 결과를 대조해야 한다. 어려운 건 생성이 아니라 의도 대비 결과 검증.
- 중재안: Addy Osmani "라이트 팩토리" — 설계·아키텍처 같은 고비용 결정 지점에만 불을 켠다. Igor Ostrovsky — 워크플로가 정형화된 작업부터 팩토리화. PostHog — 조건부로 "불을 끄는 게 그리 미친 건 아닐 수도".

### 논쟁 B: 재사용 하네스 vs 앱에 "화학적으로 결합된" 맞춤 하네스
- 관점 1 (맞춤): Yegge(2026-08) — 재사용 하네스 만들기를 포기했다, 하네스는 곧 전부 맞춤형이 되고 파는 사람은 망할 것, 하네스는 애플리케이션의 일부로 "chemically bonded in". Gas Town은 결국 자기 자신만 만들었다.
- 관점 2 (공유 자산): 토스·우아한형제들 — 팀 하네스를 플러그인 마켓플레이스·규칙·스킬로 표준화해 조직 저점을 올린다. Addy `factory`·genai-jerry 같은 참조 구현. AI Engineer World's Fair 2026 — "모든 플랫폼이 스킬 중심으로"(Philipp Schmid: 에이전트는 그냥 파일).
- 쟁점 정리: **재사용되는 건 "패턴·계약"(게이트, 역할, 상태 저장 방식)이고 맞춤이 필요한 건 "도메인 지식·검증기"**라는 절충이 가능 (책 저자 해석, 커뮤니티 명시 합의는 아님).

### 논쟁 C: 스펙 주도 개발(SDD)은 폭포수의 귀환인가
- 관점 1 (폭포수다): HN 「Spec-Driven Development: The Waterfall Strikes Back」(2025-11-15, 225pt/191c) https://news.ycombinator.com/item?id=45935763 — fzaninotto: 첫 시도에 원하는 대로 되는 일이 드물어 어차피 반복해야 한다. thomascountz: 긴 스펙을 쓰고 수천 줄을 생성한 뒤 어긋남을 발견해 원점. HN lethain 스레드 deterministic: 사람-루프 개발은 더 애자일해야.
- 관점 2 (스펙은 컨텍스트 진입점이다): canterburry — 인수 기준 중심 스펙 2~3시간이면 저녁엔 테스트된 다음 버전. podgorniy — 스펙은 고정 단계가 아니라 LLM의 컨텍스트 진입점이며 진화 가능. midnitewarrior — "빠르고 반복적인 폭포수". 2026-02 「Verified Spec-Driven Development」(HN 211pt) https://news.ycombinator.com/item?id=47197595
- 한국: Lars Faye가 비판 대상으로 지목한 업계 분위기가 바로 SDD(계획 생성 후 코드에서 손 떼기).

### 논쟁 D: 토큰 비용 — 미래에 대한 베팅인가, 낭비인가
- 관점 1: StrongDM — 하루 1인 $1,000 이상 안 쓰면 개선 여지가 있다. Huntley — 소프트웨어 개발 비용이 시간당 $10.42로 최저임금 이하(2026-02-27, 산식 미공개 ⚠️검증). Lopopolo — 모델은 무한히 병렬화 가능, 제약은 쓸 의향이 있는 GPU와 토큰뿐.
- 관점 2: HN codingdave·japhyr·jpollock(위 패턴 6), tokenmaxxing 반발, Gartner의 "2027년 말까지 에이전틱 프로젝트 40% 이상 보류" 전망 인용(2차 ⚠️검증).

### 논쟁 E: 에이전트 무리(swarm)인가, 결과(outcome)인가
- 관점 1: Boris Cherny(수백~수만 에이전트 관리), Gas Town(작업자 12~30), Claude Code Agent Teams — 병렬성이 최대 해제 요인.
- 관점 2: Kent Beck(2026-04-23) — 아무도 에이전트를 원하지 않는다, 시스템이 바뀌길 원할 뿐. 멀티 에이전트는 기능이고 결과 지향이 목적. 진짜 미개척지는 여러 **사람**이 함께 하는 증강 개발. HN GitHub Agentic Workflows root_axis — 에이전트 5개가 서로 환각을 주고받으며 20달러를 날렸다.

### 논쟁 F: 기술 위축 — 증폭인가 침식인가
- 관점 1 (증폭): HN hi_hi — 수십 년 전문성으로 LLM을 전문가답게 모는 데 가치가 있다. Karpathy "agentic engineering"(2026 초) — 배우고 나아질 수 있는 기술. 이해는 외주할 수 없다는 경구가 Karpathy 발로 널리 인용됨 ⚠️검증(원 발화자 확인 필요).
- 관점 2 (침식): Lars Faye, 「AI 없이 보낸 한 달」, HN support group 스레드, Ronacher "agent psychosis"(도파민·의존).
- 절충: Addy — TDD·페어 프로그래밍으로 기본기 유지, 의도적 학습 병행. Geoffrey Litt — 퀴즈·설명 문서·작은 변경·데모 의식으로 이해를 팀 의례로.

### 논쟁 G: 벤더 플랫폼에 파이프라인을 올려도 되는가
- 관점 1 (올리지 마라): HN Routines 스레드 joshstrange — 모델·기능을 너프하거나 종료하지 않을 거란 신뢰가 없다. hdjrudni — schedule은 그냥 cron, GitHub 이벤트 연동은 20분 작업. 포스트모템 스레드의 "알리지 않은 변경" 분노. Lars Faye — 공급자가 당신을 소유한다.
- 관점 2 (써라): danudey — 다들 허술한 버전을 해킹하느니 이게 더 똑똑하고 빠르고 안전하다. Codex 팀 — 시간별·일별 automations로 머지 충돌 스캔·팀 다이제스트·버그 사냥.
- 커뮤니티 절충: 상태·메모리·스킬은 git 안 마크다운으로(이식 가능), 트리거는 GitHub Actions/cron처럼 교체 가능하게, 모델 호출부만 벤더 의존 (HN schlesimeister·rbalicki, Claude Code가 AGENTS.md를 읽게 된 변경 2026-09-18 HN 740pt).

### 논쟁 H: HITL 게이트의 기본값 — 멈춰야 하나, 진행해야 하나
- 관점 1 (멈춰라): claude-code#73125·codex#28969 사용자들 — 질문은 안전 장치다, 자리를 비우면 기다려야 한다.
- 관점 2 (진행하라): 벤더의 백그라운드·무인 실행 방향, Boris의 3~4단계(에이전트가 작업을 시작), Igor — 머지 않아 에이전트가 우리에게 더 자주 프롬프트할 것.
- 결과: Claude Code는 기본 꺼짐+설정 가능으로 후퇴(2026-07-04). → **"어떤 결정은 기다리고 어떤 결정은 기본값으로 진행하는가"를 워크플로에서 명시적으로 분류**해야 한다는 교훈.

---

## 소셜 미디어·인물별 포지션 요약 (X·블로그·팟캐스트)

| 인물 | 포지션 요지 | 출처(날짜) |
|---|---|---|
| Simon Willison | "agentic engineering patterns" 가이드 연재 — 테스트 먼저, red/green TDD, 실제 수동 테스트, 작은 변경, 프롬프트 인젝션은 시스템 설계 문제. StrongDM을 가장 야심찬 사례로 소개하되 비용 의문 | https://simonwillison.net/2026/Feb/23/agentic-engineering-patterns/ (2026-02-23), X https://x.com/simonw/status/2020161285376082326 |
| Geoffrey Huntley | Ralph 루프 창시. "소프트웨어 개발은 죽었고 소프트웨어 엔지니어링은 살아 있다". 팩토리 = 진화하는 소프트웨어. 자기 코딩 에이전트를 직접 만들어보라 | https://ghuntley.com/loop/ (2026-01-17), https://ghuntley.com/real/ (2026-02-27), YouTube Dev Interrupted https://www.youtube.com/watch?v=C1YNGy6qusg |
| Steve Yegge | Gas Town(2026-01) → Opus 4.7에서 붕괴 → 재사용 하네스 포기, 비공개 Wheelhouse. CI/CD는 에이전트 커밋 속도를 못 따라간다 — 100+ 커밋을 main에 몰아넣고 실패를 무리로 진단하는 "Land Rush" | https://yegge.ai/essays/the-shape-of-things-to-come/ (2026-08) |
| Dan Shapiro | 자율주행 비유 5단계, Level 5 = 다크 팩토리 | 블로그 (2026-01-23) |
| Andrej Karpathy | 1개월 만에 수동 80%→에이전트 80%(2026-01, 4만 좋아요 규모 2차 보도). 바이브 코딩은 바닥을 올리고 agentic engineering은 천장을 올린다. 모델은 확인 없이 잘못된 가정을 하고 달린다 | X https://x.com/karpathy/status/2019137879310836075 (2026-02), The New Stack 정리 |
| Boris Cherny | 병렬 worktree, 손코딩 8개월 0, 다중 페르소나 PR 리뷰 + 사람 최종 승인, 도입 4단계 | Fortune 2026-06-11, 팁 2026-01 |
| Kent Beck | 증강 코딩(augmented coding)은 코드 품질에 여전히 신경 씀. 지니의 테스트 삭제는 신뢰 파괴. 에이전트 무리가 아니라 결과 | 뉴스레터 2026-04-23 |
| Addy Osmani | 80% 문제·이해 부채 → 라이트/다크 팩토리 구분 → 참조 구현 `factory`. 미래의 엔지니어는 무엇이 할 가치가 있는지 고르는 사람 | substack 2026-01-28, 2026-07-22; YouTube https://www.youtube.com/watch?v=n97BCfyFIvw (2026-07-14) |
| Dex Horthy (HumanLayer) | 하네스로는 부족, 모델의 유지보수성 보상 부재, 사람이 계속 읽고 계획에 투자 | wsff.md (2026-07), YouTube https://www.youtube.com/watch?v=Ib5GBkD555M |
| OpenAI Codex 팀 (Sottiaux·Embiricos·Lopopolo) | 사람 타이핑·리뷰 용량이 병목, automations·skills로 백그라운드 작업, harness engineering, Symphony(Elixir 오케스트레이터) | Every 2026-02-18, Lenny 2025-12-14, Latent Space |
| Will Larson | 팩토리 패턴을 Imprint에서 실험 — 공통 작업 관리 시스템 부재가 최대 제약, 조각들은 다른 조각이 있을 때만 복리로 쌓인다 | lethain.com 2026-09-20 |
| Armin Ronacher | agent psychosis — 도파민, 의존, 슬롭 PR | 2026-01-18 |
| Mastodon/Bluesky | 오픈소스 메인테이너 중심의 반발(AI PR 금지 제안 mastodon/mastodon#38072, Codeberg "slopfree software index"). 개별 스레드 수집은 실패 | https://github.com/mastodon/mastodon/issues/38072 (날짜 ⚠️검증) |

---

## YouTube·컨퍼런스 발표

| 제목 | 채널 | 날짜 | URL | 핵심 주장 (커뮤니티 요약 기반) |
|---|---|---|---|---|
| Harness Engineering is not Enough: Why Software Factories Fail — Dex Horthy | AI Engineer | 2026-07 (WF2026) | https://www.youtube.com/watch?v=Ib5GBkD555M | 무인 팩토리 실패 원인은 모델의 유지보수성 학습 신호 부재. 계획 투자·사람 리딩 유지. 검색 시점 조회 ~4.5만 (lawrencewu.net 2026-07-09 집계 ⚠️) |
| Understanding is the new bottleneck — Geoffrey Litt (Notion) | AI Engineer | 2026-07 | https://www.youtube.com/watch?v=WkBPX-oDMnA | 검증을 위한 이해 vs 참여를 위한 이해. "무엇이 왜 바뀌었나"를 diff보다 먼저, 작은 변경, 이해 의례 |
| "The engineer of the future is the person who is able to choose what is worth doing." — Addy Osmani | AI Engineer | 2026-07-14 | https://www.youtube.com/watch?v=n97BCfyFIvw | 속도가 아니라 판단·취향이 희소 역량. 설명 못 하면 배포하지 마라 |
| Extreme Harness Engineering: 1M LOC, 1B toks/day, 0% human code or review — Ryan Lopopolo | (Latent Space 게시) | 2026-04-07 | https://www.youtube.com/watch?v=CeOXx-XTYek | 조회 ~6.1만(검색 시점). 실패 시 누락된 능력·컨텍스트·구조를 찾아 인코딩, 머지 후 표본 리뷰 |
| Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo | AI Engineer | 2026 (AIE Europe/Craft) | https://www.youtube.com/watch?v=am_oeAoUhew | 사람은 조향, 에이전트는 실행 |
| WF2026: Software Factories & Keynotes ft. Microsoft, OpenAI, OpenClaw, Z.ai, MiniMax, HF | AI Engineer | 2026-07 (라이브) | https://www.youtube.com/watch?v=htM02KMNZnk | WF2026 2일차 "Software Factories" 트랙. Cursor는 팩토리를 "전 과정을 돕는 장시간 에이전트"로 정의(2차) |
| Field Guide to Fable — Thariq Shihipar (Anthropic) | AI Engineer | 2026-07 | https://www.youtube.com/watch?v=9fubhllmsBU | 최신 모델 설계 패턴(상세 미확인) |
| Code with Claude 2026: Opening Keynote | Techusiness(재업로드로 보임, 공식 채널 확인 필요) | 2026-05-06 행사 | https://www.youtube.com/watch?v=wjvESxKgqaQ | Multiagent Orchestration·Outcomes(성공 기준 정의)·Dreaming(이전 세션 회상) 발표(2차 요약) ⚠️검증 |
| Inventing the Ralph Wiggum Loop with Geoffrey Huntley (#256) | Dev Interrupted | 2026-01 | https://www.youtube.com/watch?v=C1YNGy6qusg | Ralph의 기원, 개발은 죽고 엔지니어링은 산다 |

- 채널명은 YouTube oEmbed로 확인(2026-09-28). 업로드 날짜·조회수는 yt-dlp 접근 실패로 대부분 2차 출처 기준.
- AI Engineer World's Fair 2026(2026-06-29~07-02, SF) 5대 트렌드(Latent Space 2026-07-14): 에이전트에서 **에이전트를 감싼 시스템**으로, loop engineering, 엔터프라이즈 진입(FDE), 코딩 에이전트의 IDE 대체, 스킬 중심 플랫폼.

---

## 한국 커뮤니티 요약

| 소스 | 날짜 | 요지 |
|---|---|---|
| GeekNews 「어떻게 코드를 보지 않고도 뛰어난 소프트웨어를 개발하는가?」 https://news.hada.io/topic?id=26573 | ~2026-02 | StrongDM 소개. 엔지니어당 월 $20,000 토큰, 사업 지속성·기능 복제·무검토 신뢰성 질문. 댓글은 확인 안 됨 |
| GeekNews Weekly #347 「Vibe Coding 이후 1년, 코딩은 무엇이 되었나」 https://news.hada.io/weekly/202609 | 2026-02-23~03-01 | 새 핵심 역량은 작업 분해·감독. 올해 화두는 에이전틱 엔지니어링의 조직·프로세스 내재화 |
| GeekNews Weekly #351 「이제는 에이전트가 아니라 에이전트 팀이다」 https://news.hada.io/weekly/202613 | 2026-03-23~29 | 경쟁 축이 에이전트 팀 구성으로. gstack·Harness 플러그인·장기 실행 하네스 설계·Codex 활용 사례 등 |
| GeekNews 「AI 없이 보낸 한 달」 https://news.hada.io/topic?id=34323 | ~2026-09-27 | 리뷰 병목·테스트 결함·AI 중단 후 성과 유지. HN·Lobsters 댓글 번역 포함(토큰 30달러 정체 사례, 복잡성 관리가 핵심 역량) |
| GeekNews 「코드는 다 읽을 수 없고…」 https://news.hada.io/article/code-outruns-review | ~2026-08 | 리뷰 책임 5단계 재배치(휴리스틱 7) |
| GeekNews 「The Agentic Awakening」 https://news.hada.io/topic?id=33058 | ~2026-08-31 | 개인 10배 → 조직 25~30%, PR 처리량 7.76%↑에 불과, AI 월 지출 $1,000~2,000 주장 ⚠️검증 |
| GeekNews 「개인용 AI 팩토리 구축기」 https://news.hada.io/topic?id=21802 | 2025-07-04 | 계획(o3/Sonnet)→실행(Claude Code)→검증(교차 모델). 입력을 고쳐라. 댓글: 설계 일관성·프로덕션 신뢰성 비판 |
| 토스 기술블로그 https://toss.tech/article/harness-for-team-productivity | 2026-02-26 | 계층형 플러그인 마켓플레이스, 실행 가능한 SSOT, 저점 올리기 |
| 우아한형제들 기술블로그 https://techblog.woowahan.com/26177/ | 2026-04-17 | 프론트엔드 팀 규칙+스킬 하네스, 도구 호출·토큰 절감 |
| AWS 한국 기술블로그 https://aws.amazon.com/ko/blogs/tech/codex-claudecode-harness/ | 2026-06-11 | Bedrock 위 Codex+Claude Code 8가지 협업 토폴로지, 모델 ID 어서트·재시도·산출물 게이트·STATUS 재개 |
| 하이퍼리즘 기술블로그 https://tech.hyperithm.com/review-agent | 2025-10-27 | 시니어 리뷰 집중 해소용 PR 리뷰 에이전트, 탐색/검증 분리, 비즈니스 로직 맥락은 못 잡음 |
| velog 「Codex와 Claude를 싸움붙여보자」 | 2026-02-19 | 교차 모델 토론으로 검증 |
| 파이낸셜뉴스 AI월드 2026 https://www.fnnews.com/news/202609091826242004 | 2026-09-09 | 당근 박용권: 기술·인지·의도 부채, 사람에게 남은 건 결과 책임 |
| OKKY | — | 이 주제의 실무 토론은 빈약. Claude Pro 구독에 Claude Code 재포함 소식, AI 해고 번역글, 신입 채용난 정도. 한국 현장 논의는 GeekNews·기업 기술블로그·페이스북에 집중 |

---

## 챕터 매핑 제안 (브리프 항목 → 소재)

| 브리프 항목 | 오프닝 후보 | 휴리스틱·논쟁 |
|---|---|---|
| 1. 개념·왜 지금·CI/CD와 차이 | "생성 5분, 리뷰 이틀"(패턴 1), StrongDM 두 원칙과 HN 459댓글 반응 | 논쟁 A, Igor의 "이벤트에서 시작하는 워크플로" 정의, Yegge의 CI/CD 비둘기집 |
| 2. Claude Code·Codex·Grok·Muse Spark | 60초 자동 진행 사태(패턴 5), 한도 이슈 873/630 댓글(패턴 6) | 분업 표, 교차 리뷰(휴리스틱 3), 서브에이전트 라우팅(휴리스틱 12) |
| 3. 1인 개발자 팩토리 | Jake Saunders "발사 코드" 딜레마, 60세 개발자의 열정 | 1인 레시피 표, 휴리스틱 6·14, Ralph |
| 4. 팀 활용 | tokenmaxxing 리더보드, 당근 3부채, Stripe 1,300 PR의 실제 규모 | 휴리스틱 7·10, 팀 역학, 논쟁 G |
| 5. 단계적 발전 경로 | Gas Town 붕괴(재사용 하네스의 한계), 컴팩션 59회 사용자 | Shapiro 5단계·Boris 4단계, 논쟁 H, 휴리스틱 4(역압) |
| 6. 워크플로·파이프라인 | Comment and Control(CI 속 에이전트), sudo 우회 | 휴리스틱 1·5·9·11·13, SDD 논쟁 C |
| (에필로그) 사람의 역할 | support group 스레드 vs 재점화된 열정 | 논쟁 F, Litt의 "참여를 위한 이해" |

---

## 수집 한계

- **Reddit 직접 접근 불가:** WebFetch·WebSearch(도메인 차단)·브라우저(안전 제한) 모두 reddit.com을 막았다. r/ClaudeAI·r/codex·r/ChatGPTCoding·r/ExperiencedDevs 발언은 **2차 집계 사이트(duply.ai 2026-08-24, explainx 2026-09-16 등)의 인용과 스레드 URL**에 의존했다. 원문 대조 전에는 인용하지 말 것. r/ExperiencedDevs·r/programming 고유 스레드는 확보 실패.
- **Lobsters 접근 불가:** Anubis 봇 차단. 검색 결과 제목(「Agentic Coding is a Trap」, 「Agent Psychosis」, 「AGENTS.md as a dark signal」, 「we have a year to fix security everywhere」 등)만 확인, 댓글은 미수집.
- **X/Twitter·Bluesky·Mastodon:** 스레드 본문 직접 수집 불가(402/미색인). 인물 포지션은 본인 블로그·팟캐스트·2차 보도로 재구성했다. Bluesky/Mastodon 고유 논쟁은 사실상 공백.
- **YouTube:** 트랜스크립트 추출 실패(yt-dlp 구버전 차단). 채널명만 oEmbed로 확인했고 내용은 2차 요약 기반. 발표 인용 전 영상 확인 필요. 한국어 YouTube(조코딩·노마드코더·테디노트·개발바닥 등)의 이 주제 영상은 검색으로 특정하지 못함.
- **신선도:** Opus 5.5·GPT-6 Sol(2026-09-22)은 출시 6일째라 워크플로 수준 회고가 없다. 분업 패턴은 이전 세대 모델 기준.
- **GeekNews 날짜:** "n일전/n달전" 상대 표기를 검색일 기준으로 환산했다(~ 표시). 댓글 원문은 일부 글에서 추출되지 않음.
- **OKKY·커리어리:** 이 주제에 대한 실무 토론이 빈약해 소재로 쓸 만한 건 거의 없음. 커리어리는 검색 노출이 안 됨.
- **언어 편중:** 영어권(HN·GitHub·미국 블로그) 비중이 약 75%. 한국 소재는 대기업·플랫폼 기술블로그 위주라 중소 팀·SI 현장의 목소리가 부족하다.
- **수치 신뢰도:** Faros(인시던트/PR +242.7%), Meta 60조 토큰, Stripe 1,300 PR, Uber 11%, PostHog 70%, 우아한형제들 토큰 절감, 한컴 7%/11% 등 모든 수치는 1차 출처 대조 필요. Uber가 2026 AI 예산을 4월에 소진했다는 2차 보도는 근거가 약해 본문에서 제외했다.
- **이해관계:** 여러 출처가 도구 판매자다(HumanLayer·Factory·CodeRabbit·Augment·Faros·Stage). HN StrongDM 스레드에서도 초청 데모 후 호평에 대한 이해충돌 지적(shimman)과 Simon의 해명이 있었다. 결론을 인용할 때 판매 맥락을 병기할 것.
