# 5장. CLAUDE.md — 읽고, 인정하고, 그러고는 무시한다

### 60분, 아홉 번의 교정

60분. 아홉 번의 교정. 400줄짜리 CLAUDE.md.

GitHub 이슈 #17530은 2026년 1월 11일에 열렸다. 보고자는 자기 CLAUDE.md가 약 400줄이고, Claude Code가 그 안의 명시적 지시를 "approximately 50% of sessions"에서 따르지 않는다고 썼다. 한 시간 동안 아홉 번 같은 것을 고쳐 줬다. 월 200달러 구독에 지시 준수율이 절반이라는 문장이 이슈 본문에 있다. 이슈는 3월 6일 "not planned"로 닫혔다. 보고자 스스로 내린 처방이 흥미롭다 — "CLAUDE.md를 150줄 아래로 유지하고, 참고 자료는 별도 파일로 분리하라."

이 장면이 낯설지 않다면, 아마 같은 일을 겪었을 것이다. 규칙을 적었다. Claude는 세션을 시작할 때 그 파일을 읽었다고 말한다. 심지어 "알겠습니다, 컨벤션을 따르겠습니다"라고 대답한다. 그러고는 다음 턴에 그 규칙을 어긴다. 읽고, 인정하고, 그러고는 무시한다. 찜찜하다. 그리고 어느 순간부터는 파일을 고치는 일 자체가 허무해진다.

이 고통은 한 사람의 것이 아니다. 같은 제목의 이슈가 GitHub에 열 건 넘게 쌓여 있고(2026-10 기준), 대부분은 봇이 "inactive"로 닫았다. #44246(2026-04-06)은 더 구체적이다. 무시된 지시 네 가지를 열거하는데 — "plan mode before non-trivial tasks", "end-to-end verification before declaring work complete", "checking documentation before guessing", "pausing to diagnose root cause after repeated failures" — 전부 이 책이 플레이로 다루는 것들이다. 보고자는 "This is not occasional drift"라고 썼다. 가끔의 흔들림을 넘어 일관된 퇴행이라는 것이다.

그렇다면 CLAUDE.md는 쓸모없는 파일일까? 그 질문에 답하려면 이 파일이 애초에 무엇인지부터 다시 봐야 한다. #34763(2026-03-15)의 보고자가 남긴 한 문장이 좋은 출발점이다. "CLAUDE.md startup instructions are just text in the context window. The model _can_ follow them, but it often doesn't." 컨텍스트 윈도 안의 텍스트일 뿐이다. 따를 수 있지만, 자주 따르지 않는다. 불평처럼 들리지만 사실은 정확한 사양 설명이다. 무엇을 기대할 수 있고 무엇은 기대할 수 없는지가 여기서 갈린다.

### 코스가 말하는 CLAUDE.md — 다섯 단계와 한 페이지

코스 레슨 5의 정의부터 보자.

> "`CLAUDE.md` gives Claude the context a new joiner would need, covering conventions, commands, architecture, and the mistakes the team sees most often. Knowledge that used to sit in people's heads and on wikis becomes a file the agent reads at the start of every session, maintained by the whole team and iterated on whenever a mistake is made."
>
> CLAUDE.md는 새로 합류한 사람이 필요로 할 컨텍스트 — 컨벤션, 명령, 아키텍처, 팀이 가장 자주 보는 실수 — 를 Claude에게 준다. 사람들의 머릿속과 위키에 있던 지식이 에이전트가 매 세션 시작 시 읽는 파일이 되고, 팀 전체가 유지하며 실수가 날 때마다 고친다. (코스 레슨 5)

"새로 합류한 사람(new joiner)"이라는 비유를 붙잡아 두자. 신입에게 첫날 주는 문서에 프레임워크 튜토리얼을 통째로 넣지는 않는다.

코스의 실행 단계는 다섯이다.

1. 리포에서 `/init`을 실행한다. Claude가 발견한 것으로 출발점 CLAUDE.md를 만든다.
2. 생성된 파일을 "신입이 첫날 필요로 할 것"까지 깎아 낸다. 빌드·테스트·린트 명령, 중요한 컨벤션, Claude가 계속 틀리는 것들만 남긴다.
3. 리포 루트에 커밋한다. 변경은 코드처럼 리뷰된다.
4. 작업 규칙 하나 — "When Claude makes a mistake twice, the correction goes into `CLAUDE.md`." 두 번 틀리면 한 줄.
5. 한 페이지 아래로 유지한다. "Claude reads all of it at the start of a session and anything stale is taking up context for no benefit."

2번과 5번이 같은 말을 두 번 하고 있다. 생성한 것을 깎아라, 그리고 한 페이지 아래로. 코스는 CLAUDE.md를 채우는 플레이가 아니라 비우는 플레이로 설계했다. 그리고 4번이 채우는 유일한 경로다 — 관찰된 실수, 두 번.

관통 예제의 CLAUDE.md를 원문 그대로 보자. 보험사 포털 리포의 것이고, `claims-core`는 청구 데이터를 쥔 구형 내부 시스템, `intent/`는 변경별 계획 파일이 사는 폴더다.

```markdown
# Claims portal
## Commands
- Build: make build
- Test: make test (unit), make itest (integration, needs docker)
- Lint: make lint (runs in CI; fix before pushing)
- Run: make run (portal on :3000, claims-api on :8000)
## Conventions
- claims-api is Python 3.12 and FastAPI. portal is TypeScript and React.
- Every endpoint needs a test in claims-api/tests.
- Dates cross the API as ISO 8601, never as formatted text.
## Architecture
- portal/ is the customer site, claims-api/ is its backend, and
  intent/ holds the intent.md, spec.md and plan.md for each change.
- Only claims-api talks to claims-core. The portal never calls it.
- claims-core allows 50 requests a second. Cache reads; never poll it.
## Things Claude gets wrong
- Do not log request or response bodies in claims-api; they can hold PII.
- Do not bump dependency versions; the platform team owns them.
```

네 절이 각각 "신입 첫날 문서"의 네 종류다. Commands는 추측할 수 없는 것(`make itest`에 도커가 필요하다는 사실). Conventions는 기본값과 다른 규칙. Architecture는 이 리포에만 있는 결정 — "Only claims-api talks to claims-core. The portal never calls it." 그리고 앞 장 `plan.md`의 Risks 절에 있던 바로 그 숫자 — 50 rps — 가 여기서는 "claims-core allows 50 requests a second. Cache reads; never poll it."으로 적힌다. 마지막 절 Things Claude gets wrong은 4번 규칙으로 쌓인 줄들이다. "Do not log request or response bodies in claims-api; they can hold PII." 이 한 줄은 뒤에서 다시 만난다. 6장의 스킬 규칙 4가 같은 정책을 절차로 적고, 9장에서는 이 줄을 지웠을 때 무슨 일이 생기는지가 eval의 시나리오가 된다. 지금은 "두 번 틀려서 들어온 줄"로만 기억해 두자.

파일이 짧다. 스무 줄 미만이다. 그런데 이 안에 포털의 구조, 외부 시스템의 한계, 팀이 겪은 실수의 흔적이 전부 들어 있다.

거버넌스는 간단하다. 버전 관리되므로 에이전트가 따르는 지시가 리뷰·감사 가능하고, 변경은 Git 이력에 남고, 코드 오너가 PR에서 승인한다. 측정은 선행 지표로 "CLAUDE.md가 잡았어야 할 실수를 Claude가 반복하는 빈도", 지연 지표로 "새 팀원의 첫 머지 PR까지 걸린 시간"이다.

### 현행 사양: 컨텍스트이지, 강제되는 설정이 아니다

Claude Code 2.1.303 / 2026-10 기준 공식 메모리 문서에서 가장 중요한 문장은 이것이다.

> "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead. The more specific and concise your instructions, the more consistently Claude follows them."
>
> Claude는 이 파일들을 컨텍스트로 취급하며, 강제되는 설정으로 취급하지 않는다. Claude의 판단과 무관하게 행동을 막으려면 `PreToolUse` 훅을 쓰라. 지시가 구체적이고 간결할수록 Claude는 더 일관되게 따른다.

#17530의 고통에 대한 공식 답이 사실 여기 있다. 그 파일은 원래 보장을 약속한 적이 없다. 보장은 훅의 일이고(11장), CLAUDE.md의 일은 "더 자주 맞게 행동하도록" 컨텍스트를 주는 것이다.

위치는 네 계층이다. 관리형 정책 파일(macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`, Linux/WSL `/etc/claude-code/CLAUDE.md`, Windows `C:\Program Files\ClaudeCode\CLAUDE.md`), 사용자 `~/.claude/CLAUDE.md`, 프로젝트 `./CLAUDE.md` 또는 `./.claude/CLAUDE.md`, 로컬 `./CLAUDE.local.md`(`.gitignore`에 넣는다). 작업 디렉터리 위쪽의 파일은 시작 시 로드되고, 하위 디렉터리의 파일은 그 디렉터리를 건드릴 때 로드된다. 중요한 한 줄 — "All discovered files are concatenated into context rather than overriding each other." 발견된 파일은 서로 덮어쓰지 않고 이어 붙는다. 두 파일의 규칙이 충돌하면? 공식 답은 "Claude may pick one arbitrarily" — 임의로 하나를 고를 수 있다. 계층을 쓸수록 모순을 점검할 일이 늘어난다.

로드 빈도에 대해서는 공식 문서가 "loaded at launch"라고만 쓴다. 커뮤니티에는 "세션 시작 시 정확히 한 번만 주입되고 이후에는 다시 주입되지 않는다"는 주장이 있지만(#44246 댓글), 내부 동작은 검증되지 않았다. 이 책은 "세션 시작 시 로드된다"까지만 말한다.

크기 기준도 공식 문서에 있다. "Size: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." 파일당 200줄 아래를 목표로. 길어질수록 컨텍스트를 더 쓰고 준수율은 떨어진다. 코스의 "한 페이지"가 공식 수치로는 200줄인 셈이다. 현장 수치는 더 작다 — HumanLayer의 글은 "300줄 아래가 일반 합의"라며 자기 루트 파일은 60줄 아래라 했고, #17530 보고자는 150줄을 제안했다. 방향은 하나다. 이 책은 공식 200줄을 기준으로 삼는다.

Best practices 문서는 줄마다 던질 질문 하나를 준다. "For each line, ask: *Would removing this cause Claude to make mistakes?* If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" 이 줄을 지우면 Claude가 실수를 하게 될까? 아니라면 지워라. 부푼 파일은 정작 중요한 지시를 무시하게 만든다. 같은 문서의 포함·제외 표를 옮기면 이렇다.

| 넣는다 | 뺀다 |
|---|---|
| Claude가 추측할 수 없는 Bash 명령 | 코드를 읽으면 알 수 있는 것 |
| 기본값과 다른 코드 스타일 규칙 | 언어의 표준 컨벤션 |
| 테스트 지시와 선호하는 테스트 러너 | 상세 API 문서(링크로 대신) |
| 리포 에티켓(브랜치 이름, PR 규약) | 자주 바뀌는 정보 |
| 이 프로젝트 고유의 아키텍처 결정 | 긴 설명·튜토리얼 |
| 개발 환경의 유별난 점 | 파일별 설명 |
| 흔한 함정 | "깨끗한 코드를 쓰라" 같은 자명한 것 |

### 현행 사양: 임포트, 규칙 파일, 메모리, 그리고 강조 한 줄

몇 가지 기능을 더 짚어 두자. `@path/to/import` 문법으로 다른 파일을 끌어올 수 있고 깊이는 네 홉까지다. 단, 공식 문서는 분명히 말한다. 임포트는 긴 파일을 정리하는 데 도움이 되지만 컨텍스트 비용은 줄이지 않는다 — 임포트된 파일도 시작 시 로드되기 때문이다. 경로를 임포트하지 않고 언급만 하려면 백틱으로 감싼다. `.claude/rules/` 디렉터리의 규칙 파일은 frontmatter `paths:`의 글롭에 맞는 파일을 다룰 때만 로드된다 — 이 책은 정의만 소개한다(리서치에서 확인된 현장 사례가 없었다). `/init`은 CLAUDE.md가 이미 있으면 덮어쓰지 않고 개선을 제안하고, Claude가 스스로 쓰는 auto memory는 매 세션 첫 200줄 또는 25KB까지 로드되며 `/memory`로 편집하거나 끈다 — 공식 문서는 두 파일을 "누가 쓰는가"로 가른다. CLAUDE.md는 사람이, auto memory는 Claude가. 2.1.277부터는 작업 디렉터리와 그 위에 CLAUDE.md가 하나도 없을 때만 `AGENTS.md`를 읽는다.

강조에 대한 지침도 있다. "If Claude keeps skipping one instruction, add emphasis such as 'IMPORTANT' to that line alone. If you emphasize many lines, none of them stands out." IMPORTANT는 한 줄에만. 여러 줄을 강조하면 아무것도 두드러지지 않는다.

마지막으로, 스킬 문서가 CLAUDE.md에 대해 하는 말 하나. "when a section of CLAUDE.md has grown into a procedure rather than a fact" — CLAUDE.md의 한 절이 사실에서 절차로 자라났을 때 그 절은 스킬로 옮긴다. 스킬의 본문은 쓰일 때만 로드되기 때문이다. 이 기준을 뒤의 체크리스트에서 쓴다.

### 잘못된 대안: 더 길게, 더 세게

규칙이 무시되면 사람은 두 가지 반응을 한다. 더 많이 적거나, 더 세게 적는다. 둘 다 현장에서 실패 보고가 있다.

더 길게 적는 쪽부터. HN의 한 사용자는 CLAUDE.md를 "100%의 세션에서 쓸모 있는 지속적 리마인더"에만 쓰라고 했다. 공식 문서의 "부푼 파일은 정작 중요한 지시를 무시하게 만든다"와 같은 말이다. 400줄의 #17530이 바로 그 경우였을 가능성이 높다. 규칙이 안 지켜져서 줄을 더하고, 줄이 늘어 더 안 지켜지는 순환이다.

더 세게 적는 쪽은 어떨까. 이슈 #17530의 한 댓글(2026-02-06)은 한 줄짜리 CLAUDE.md도 무시되었다고 보고한다. 그 한 줄은 `**You MUST read @AGENTS.md. This is NON-NEGOTIABLE.**`이었다. Reddit에는 강압적 어휘가 오히려 역효과를 낸다는 이론이 있다 — "it's interpreting your insistent language against its own training" — 커뮤니티 이론이고 검증된 것은 아니다. 공식 지침은 더 소박하다. IMPORTANT는 한 줄에만. 부정형("don't X")보다 긍정형으로 쓰라는 HN의 조언도 있는데, 역시 현장 관찰이지 데이터는 아니다.

한국어로 쓸까 영어로 쓸까도 자주 묻는 질문이다. 한국어와 영어의 토큰 비용을 직접 나란히 측정한 자료는 리서치에서 찾지 못했다. 가까운 것은 한 위키독스 저자의 개인 측정(2026-04)이다 — Opus 4.7의 새 토크나이저가 영어·코드 위주의 실제 CLAUDE.md에서는 구 토크나이저 대비 1.45배 토큰을 만들었고, CJK 텍스트에서는 1.01배로 거의 변화가 없었다는 것이다. 토크나이저 변경이 한국어에 불리하게 작용하지는 않았다는 뜻이지, 한국어가 영어보다 싸다는 뜻은 아니다. 공식 수치로 확인되는 것은 하나뿐이다. Sonnet 5의 새 토크나이저는 같은 텍스트에 약 30% 더 많은 토큰을 만든다 — 언어를 따로 구분하지 않은 수치다. 그러니 공식적으로 확인되는 변수는 길이다. 200줄 아래로 유지한다면 한국어로 써도 좋고, 팀 소통에는 한국어가 유리하다.

그리고 근본적인 반론이 하나 있다. 2026년 8월 HN에 "I am morally opposed to updating my Claude.md"라는 글이 올랐다. 인간 지식을 전부 소화한 모델에게 왜 내가 지시를 적어 줘야 하나, 옛 모델용으로 적은 지시가 새 모델의 성능을 깎는데 어느 줄이 문제인지 알 수도 없다 — 이런 논지다. 반대편은 "결국 내가 반복해서 말하게 되는 것들"이라서 적는다고 답한다. "어느 줄이 문제인지 모른다"에 대한 답은 CLAUDE.md의 변경을 코드처럼 회귀 테스트하는 것이고, 그것이 9장의 주제다. 여기서는 양쪽이 공유하는 한 가지만 챙기자. 관찰된 실수에 묶이지 않은 줄은 가치가 불확실하다.

### 올바른 대안: 감사 체크리스트 — 사실, 회귀 제약, 행동 규칙

그렇다면 어떻게 줄여야 할까? HN Ask(2026-05)의 한 댓글이 쓸 만한 분류를 남겼다. CLAUDE.md의 줄은 세 종류다. 사실(fact) — "claims-api는 Python 3.12와 FastAPI다" 같은 것으로, 모델이 신뢰한다. 회귀 제약(regression constraint) — "요청 바디를 로그에 남기지 마라"처럼 관찰된 실패에 묶인 것으로, 그 실패와 함께 적혀 있을 때 신뢰된다. 행동 규칙(behavioral rule) — "항상 X 전에 Y를 하라" 같은 것으로, 짧고 관찰된 실패에 기반할 때만 효과가 있다. 코스 예시에 대보면 Commands·Conventions·Architecture는 거의 사실이고, Things Claude gets wrong은 회귀 제약이다. 행동 규칙은 거의 없다. 그 파일이 스무 줄 미만으로 끝나는 이유다.

이 분류와 공식 한 줄 테스트를 합쳐 체크리스트를 만들어 보자. 저자의 구성이고, 재료는 모두 위에서 본 것이다.

1. **한 줄 테스트.** 줄마다 묻는다 — 이 줄을 지우면 Claude가 실수할까? 아니라면 지운다. 코드를 읽으면 알 수 있는 것, 언어 표준, 튜토리얼이 여기서 떨어진다.
2. **분류.** 남은 줄에 사실·회귀 제약·행동 규칙 라벨을 붙인다.
3. **회귀 제약에는 실패를 붙인다.** "두 번 틀렸다"는 기록이 없는 제약은 추측이다. 기록이 있으면 짧게 덧붙인다 — 코스 예시의 "they can hold PII"가 그 역할이다.
4. **행동 규칙은 의심한다.** "~할 때는 1, 2, 3 순서로"처럼 절차가 된 줄은 이 파일에 머물 이유가 없다. 따로 적어 둔다 — 갈 곳이 있다. "절대 ~하지 마라"처럼 반드시 지켜져야 하는 줄도 이 파일로는 보장되지 않는다. 역시 따로 적어 둔다(11장에서 훅으로 간다).
5. **강조는 한 줄.** IMPORTANT가 둘 이상이면 하나로 줄인다.
6. **모순 점검.** `~/.claude/CLAUDE.md`와 프로젝트 파일이 이어 붙는다는 것을 기억하고, 두 파일에 서로 다른 말이 있는지 본다.
7. **200줄.** 넘으면 1번으로 돌아간다.

왜 이렇게까지 해야 할까? 이 파일이 실제로 어떻게 쓰이는지를 본 연구가 있다. Santos 외(AGENT 2026, ICSE 워크숍)는 공개 Claude Code 프로젝트의 설정 파일 328개를 분석했는데, 에이전트가 따라야 할 아키텍처를 명시하는 경향이 두드러졌다 — 코스 예시의 Architecture 절 그대로다. Galster 외(AIware 2026)는 GitHub 리포 2,853개를 보았다. 컨텍스트 파일이 지배적이고 흔히 유일한 메커니즘이었으며, 스킬이나 서브에이전트 같은 고급 메커니즘을 쓰는 리포는 소수였다. 두 연구를 겹쳐 읽으면 그림이 나온다. 대부분은 CLAUDE.md 하나로 모든 것을 하려 하고, 그래서 파일이 부풀고, 그래서 #17530이 생긴다. 이 책의 독자는 그 파일을 비우고 절차와 강제를 다른 층으로 옮기는, 아직은 소수에 속하는 쪽이다.

토스 테크의 글(2026-02)은 "차이는 단 하나, 작업 전에 컨텍스트를 설계했느냐의 여부입니다"라고 쓰고, 그 결과를 "문서 관리의 패러다임이 '기록'에서 '실행'으로 바뀌는 셈입니다"라고 요약한다. CLAUDE.md는 읽히기 위해 쓰는 문서가 아니라 실행되기 위해 쓰는 문서다. 실행되지 않는 줄은 기록이고, 기록은 위키에 두면 된다.

### 내 리포로 옮기기

`[개인 즉시]` 오늘 할 일은 코스의 다섯 단계 그대로다. CLAUDE.md가 없으면 `/init`으로 만들고, 있으면 `/init`을 다시 돌려 제안을 받는다. 그다음 위의 체크리스트로 줄인다. 200줄을 목표로 하되 더 짧아도 괜찮다 — 코스 예시는 스무 줄 미만이다. 리포와 무관한 개인 규칙(커밋 메시지 형식 같은 것)은 `~/.claude/CLAUDE.md`로 보낸다. 그리고 기대치를 조정한다. 이 파일은 확률을 올리는 파일이다. 어긴다고 화를 내기보다 "두 번 틀렸나?"를 묻고, 두 번째라면 한 줄을 더한다. 그 한 줄이 절차나 "반드시"라면 이 파일 말고 다른 곳에 적어 둔다.

`[팀 합의]` 팀이 있다면 루트 CLAUDE.md를 커밋하고, 개인 취향은 `CLAUDE.local.md`로 분리해 `.gitignore`에 넣는다. CLAUDE.md 변경은 PR로 받는다 — 팀이 두 명이라도. 에이전트의 행동을 바꾸는 파일이라면 코드와 같은 리뷰를 받는 편이 낫다. Netflix와 Apple이 CLAUDE.md를 실수로 배포에 포함시킨 일이 HN에 오른 적이 있다(2026-05·07). 이 파일도 자산이다.

`[조직 결정]` 머신 전체에 적용되고 개인 설정으로 제외할 수 없는 관리형 CLAUDE.md가 있다. 공식 분업 표는 "도구·명령·경로 차단은 관리형 설정의 `permissions.deny`로, 코드 스타일·품질 지침은 관리형 CLAUDE.md로"라고 나눈다. 조직 층이 없는 독자에게 대체 경로는 `~/.claude/CLAUDE.md`와 팀 리포의 루트 파일이다.

측정은 git에서 셀 수 있다. 선행 지표는 코스의 "CLAUDE.md가 잡았어야 할 실수의 반복"인데, 개인판은 `git log -- CLAUDE.md`다. 같은 주제의 줄이 두 번 이상 고쳐졌다면 그 줄은 CLAUDE.md로는 해결되지 않는 것이다 — 절차거나 강제다. 지연 지표인 "새 팀원의 첫 머지 PR까지 시간"은 소규모 팀에서만 의미가 있고, 혼자라면 "새 머신에서 리포를 클론해 첫 커밋까지 걸린 시간"으로 대신해도 된다.

지금 자기 CLAUDE.md를 열어 체크리스트를 돌려 보자. 잘려 나간 줄 가운데 "~할 때는 먼저 ~하고, 그다음 ~"으로 시작하는 줄이 있다면 버리지 말고 따로 적어 두자. 그 줄에는 갈 곳이 있다.

### 이 장의 핵심

- CLAUDE.md는 컨텍스트다(공식 문서: "context, not enforced configuration"). 세션 시작 시 로드되어 행동의 확률을 바꾸지만, "반드시"를 보장하지 못한다 — 보장은 훅의 일이다.
- 비우는 플레이다. 코스의 "한 페이지", 공식의 "200줄", 현장의 "짧을수록 좋다"가 같은 방향을 가리킨다. 채우는 유일한 경로는 "두 번 틀리면 한 줄".
- 줄마다 한 줄 테스트(이 줄을 지우면 실수가 생기나?)를 던지고, 남은 줄을 사실·회귀 제약·행동 규칙으로 분류한다. 절차가 된 줄은 스킬로, 반드시인 줄은 훅으로 옮긴다.
- 더 길게·더 세게 쓰는 것은 현장에서 실패했다. IMPORTANT는 한 줄에만, 그리고 확인된 변수는 언어가 아니라 길이다.
