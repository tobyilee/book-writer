# 4장. 플랜 모드에서 시작한다 — 그리고 auto로 넘긴다

### 두 갈래 길

`spec.md`를 받았다. 앞 장에서 `intent/` 폴더에 `intent.md`와 `spec.md`를 커밋했고, R1부터 R4까지 번호가 붙은 요구사항과 세 개의 우려 사항(concern)이 그 안에 적혀 있다. 이제 세션을 열었다. 커서가 깜빡인다. 두 갈래 길이 있다.

첫 번째 길은 익숙하다. 명세를 붙여 넣고 "이대로 구현해 줘"라고 치는 것이다. Claude는 파일을 읽고, 엔드포인트를 만들고, 패널을 붙이고, 테스트를 쓴다. 십 분쯤 뒤 diff가 나온다. 빠르다. 그리고 그 diff를 처음 보는 순간, 우리는 그제야 "어떻게 만들 것인가"에 대한 결정을 한꺼번에 검토하게 된다. 캐시를 어디에 두었는지, 왜 라우트 파일을 둘로 나눴는지, 테스트가 네 가지 상태를 다 덮는지. 결정은 이미 코드가 되어 있고, 되돌리는 비용은 문서를 고치는 비용보다 훨씬 크다.

코스 레슨 4는 이 장면을 전통 쪽 칸에 이렇게 적는다.

> "An engineer reads the design and starts writing code. How the change will be made, down to which files and which tests, stays in the engineer's head or at best in a ticket comment. Nobody else can review it. The first thing a reviewer sees is the finished diff, and by then rework is slow."
>
> 엔지니어가 설계를 읽고 코드를 쓰기 시작한다. 어떤 파일을 어떤 테스트와 함께 바꿀지, 그 "어떻게"는 엔지니어의 머릿속에, 잘해야 티켓 댓글에 남는다. 아무도 그것을 리뷰할 수 없다. 리뷰어가 처음 보는 것은 완성된 diff이고, 그때는 이미 재작업이 느리다. (코스 레슨 4)

흥미로운 점은 이 문장이 사람이 코딩하던 시절을 묘사하고 있다는 것이다. 에이전트가 코드를 쓰는 지금은 어떨까? "엔지니어의 머릿속"이 "모델의 컨텍스트 윈도 안"으로 바뀌었을 뿐, 구조는 같다. 오히려 더 나빠진 면도 있다. 사람은 적어도 자기 머릿속의 계획을 알고 있었지만, 바로 코딩시킨 세션의 계획은 diff가 나오기 전까지 누구도 — 세션을 돌린 우리조차 — 본 적이 없다.

첫 번째 길의 장점은 빠르다는 것, 그리고 작은 변경에서는 그 빠름이 전부라는 것이다. 단점은 리뷰가 diff 위에서만 가능하고, 그 시점에는 방향을 바꾸는 비용이 가장 크다는 것이다. 1장에서 본 대로 병목이 빌드 밖으로 옮겨 갔다 — 그 말이 여기서 구체적인 모습을 띤다. 빌드는 십 분 걸렸는데 그 diff를 이해하고 되돌릴지 결정하는 데 한 시간이 걸린다면, 병목은 어디에 있는 걸까.

### 두 번째 길: 플랜을 받고, 심문하고, 커밋한다

두 번째 길은 같은 세션을 플랜 모드에서 연다. 코스 레슨 4의 AI 네이티브 쪽 칸은 이렇다.

> "Work starts with a written plan that Claude produces in plan mode, where it can read the codebase without changing anything. The engineer corrects the plan before code is written, and the approved version is committed as `plan.md` for later stages to check against."
>
> 작업은 Claude가 플랜 모드에서 만든 문서화된 계획으로 시작한다. 플랜 모드에서 Claude는 아무것도 바꾸지 않고 코드베이스를 읽을 수 있다. 엔지니어는 코드가 쓰이기 전에 계획을 고치고, 승인된 판본은 `plan.md`로 커밋되어 뒤 단계가 대조할 수 있게 된다. (코스 레슨 4)

코스는 이를 일곱 단계로 푼다. 하나씩 따라가 보자.

1. 플랜 모드로 세션을 시작한다.
2. `intent.md`와 `spec.md`를 건네고, 바뀌는 파일·작업 순서·그것을 증명하는 테스트를 담은 구현 계획을 요청한다.
3. 계획을 심문(interrogate)한다 — 이 변경이 무엇을 깨뜨릴 수 있는지, 어느 단계가 가장 위험한지, Claude가 선택하지 않은 다른 방법은 무엇이었는지.
4. "대화를 한 번도 본 적 없는 엔지니어가 계획만 보고 구현할 수 있을 때까지" 반복한다.
5. 승인된 계획을 `plan.md`로 커밋한다. 이 파일은 감사 추적에 합류하고, Deploy 단계의 PR 리뷰 플레이가 최종 diff를 이 파일과 대조한다.
6. 계획을 수락하고 구현을 맡긴다. "탄탄한 계획이면 구현은 종종 한 번에 끝난다(a single pass)."
7. 구현이 계획에서 벗어나면 같은 커밋에서 `plan.md`를 갱신한다. 둘의 동기화를 훅으로 강제하는 것도 고려한다.

여기서 3번과 4번이 이 플레이의 심장이다. 계획을 "받는" 것은 쉽다. 계획을 "심문하는" 것이 일이다. 무엇이 깨질 수 있나, 가장 위험한 단계는 어디인가, 선택하지 않은 대안은 무엇인가 — 이 세 질문은 코드 리뷰에서 우리가 diff를 보며 뒤늦게 던지던 질문을 코드가 없는 시점으로 당겨 온 것이다. 그리고 4번의 기준은 개인 개발자에게도 그대로 유효하다. "대화를 못 본 엔지니어"는 다음 주의 자기 자신이기 때문이다.

관통 예제의 `plan.md`를 원문 그대로 보자.

```markdown
# Plan: claims status self-service (from intent.md and spec.md)

## Files that change

portal/src/claims/StatusPanel.tsx (new), claims-api/routes/status.py, claims-api/tests/test_status.py

## Order of work

1. Add the status endpoint behind existing auth (R1, R2, R3).
2. Panel against the endpoint, with the 60-second cache (R1, R4).
3. Wire into the portal nav.

## Risks

The claims-core API rate-limits at 50 rps; the panel must cache (spec concern 3).

## Proof

test_status.py covers the four claim states (R2) and fails on any extra field (R3); screenshot matches the approved mock.
```

세 가지를 눈여겨보자. 첫째, 바뀌는 파일이 셋뿐이다. 패널 하나(신규), 라우트 하나, 테스트 하나. 영향 반경(blast radius)이 파일 이름으로 보인다. 둘째, 작업 순서의 각 단계가 괄호 안에 R1, R2 같은 번호를 달고 있다. 앞 장에서 `spec.md`에 번호를 붙인 이유가 여기서 회수된다. 코스의 설명을 빌리면 "R1 to R4 are the numbered requirements in `spec.md`, and concern 3 is a risk that `spec.md` flagged. Because the plan cites them, a reviewer can check the plan against the spec line by line." — 계획이 명세를 인용하기 때문에 리뷰어는 계획을 명세와 한 줄씩 대조할 수 있다. 셋째, Risks 절의 "50 rps"와 "concern 3"은 `spec.md`가 미검증으로 남겨 둔 claims-core의 속도 제한을 계획이 그대로 넘겨받은 것이다. 이 숫자는 책 뒤에서 계속 되돌아온다 — 다음 장 CLAUDE.md의 Architecture 절에서, 그리고 13장의 사고 기록에서. 값을 바꾸지 말고 그대로 기억해 두자.

Proof 절도 짚어 두자. "test_status.py covers the four claim states (R2) and fails on any extra field (R3)". 테스트가 무엇을 증명하는지를 요구사항 번호로 말한다. 승인 뒤 Claude가 쓴 테스트가 네 상태 중 셋만 덮고 있다면, 그것은 "테스트가 좀 부족하다"는 취향의 문제가 아니라 계획 위반이다. 리뷰 기준이 취향에서 문서로 옮겨 간다.

거버넌스 문단은 짧지만 개인에게도 중요하다. "Plan mode enforces this itself, since Claude cannot edit files until the engineer accepts the plan." — 설계 리뷰가 코드 생성 전에 일어나는 것을 플랜 모드가 스스로 강제한다, 엔지니어가 계획을 수락하기 전에는 Claude가 파일을 편집할 수 없으니. 코스는 루틴 변경은 엔지니어가, 조직이 고위험으로 분류한 것은 테크 리드나 아키텍트가 승인한다고 쓴다. 혼자 일하는 우리에게 아키텍트는 없다. 대신 "승인 버튼을 누르기 전에 계획을 직접 편집하는 손"이 그 자리를 맡는다. 어떻게 편집하는지는 바로 다음 절에서 본다.

### 현행 사양: 플랜 모드, 그리고 승인 뒤의 auto 모드

코스는 플랜 모드를 가리키기만 하고 사양은 공식 문서에 맡겼다. Claude Code 2.1.303 / 2026-10 기준으로 정리하자. 이 부분은 빠르게 바뀌는 영역이니 공식 문서를 함께 열어 두는 편이 낫다.

플랜 모드의 정의는 공식 문서에서 이렇다. "Plan mode tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source." — 파일을 읽고, 탐색용 셸 명령을 돌리고, 계획을 쓰되 소스는 편집하지 않는다. 대화형 터미널에서 bypass 권한을 쓸 수 있는 경우를 빼면 계획을 승인하기 전까지 편집은 막혀 있다.

진입 경로는 셋이다. 세션 안에서 `Shift+Tab`을 누르거나, 한 번의 프롬프트 앞에 `/plan`을 붙이거나, 처음부터 `claude --permission-mode plan`으로 시작한다. 프로젝트 전체의 기본값으로 삼으려면 `.claude/settings.json`에 `defaultMode`를 `plan`으로 둔다. 현장에서는 `Shift+Tab`이 사고(thinking) 토글만 하는 것 같다는 보고도 있었다(인프런 Q&A). 단축키가 먹지 않으면 `/plan`을 쓰는 편이 확실하다.

계획이 나오면 승인 다이얼로그가 뜬다. 여기에 두 가지가 숨어 있다. 하나는 `Ctrl+G`다. "Press `Ctrl+G` to open the proposed plan in your default text editor and edit it directly before Claude proceeds." 계획을 기본 편집기에서 열어 직접 고친 뒤 진행시킬 수 있다. 코스의 "심문" 단계를 대화로만 하지 않고 손으로 할 수 있다는 뜻이다. 다른 하나는 승인 선택지의 문구다. "Yes, and use auto mode" — 그렇다, 그리고 auto 모드로 가라. "No, keep planning" — 아니다, 계속 계획하라.

여기서 auto 모드가 무엇인지 알아야 한다. 코스 레슨 4는 auto 모드를 부속 절에서 이렇게 소개한다.

> "Claude Code can also run in auto mode, where the engineer iterates on and approves the plan, and Claude then applies each change without a per-edit prompt. As the guardrails from the later plays mature (a tuned `CLAUDE.md`, skills that encode policy, hooks that block unsafe actions, and a test suite Claude can run), auto mode becomes the default for routine work: a tight `spec.md`, a small blast radius, and code the tests already cover."
>
> 엔지니어가 계획을 다듬어 승인하면 Claude가 편집마다 묻지 않고 변경을 적용한다. 뒤 플레이의 가드레일(다듬어진 CLAUDE.md, 정책을 담은 스킬, 위험한 행동을 막는 훅, Claude가 돌릴 수 있는 테스트 스위트)이 성숙하면 auto 모드가 루틴 작업의 기본이 된다 — 조밀한 `spec.md`, 작은 영향 반경, 테스트가 이미 덮는 코드. (코스 레슨 4)

"기본이 된다"는 코스의 미래형은 현행에서 현재형이 되었다. 공식 문서는 이렇게 쓴다. "With Claude Code v2.1.283 or later, auto mode is the built-in starting permission mode for interactive terminal and VS Code sessions." 2.1.283 이후 대화형 터미널과 VS Code 세션의 시작 권한 모드는 auto다. 작동 방식은 분류기다. "A separate classifier model reviews actions before they run, blocking anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content Claude read." 별도의 분류기 모델이 행동을 실행 전에 검토해, 요청 범위를 넘는 것, 모르는 인프라를 건드리는 것, Claude가 읽은 적대적 콘텐츠에 휘둘린 것으로 보이는 행동을 막는다. 명시적 `ask` 규칙은 그래도 질문을 띄운다. 폴백도 있다. 분류기가 행동을 세 번 연속 혹은 누적 스무 번 막으면 auto 모드가 멈추고 다시 묻기 시작한다.

주의할 점 하나. 대화 중에 "푸시하지 마"나 "내가 리뷰할 때까지 배포하지 마"라고 말하면 분류기가 그 경계를 존중해, 기본 규칙이 허용하는 행동도 막는다. 편리하다. 그러나 공식 문서는 분명히 선을 긋는다. "Boundaries are not stored as rules. ... For a hard guarantee, add a deny rule instead." 경계는 규칙으로 저장되지 않는다. 하드 보장이 필요하면 `deny` 규칙을 쓰라. 이 한 문장이 2장의 통제 모델을 다시 말해 준다 — 말은 컨텍스트이고, 보장은 설정이다. 그 설정의 본진은 11장이다.

> **구버전 주의**
> 코스(2026-08)는 auto 모드를 "Claude Code can also run in auto mode"라고, 가드레일이 성숙한 뒤에 켜는 선택 기능처럼 쓴다. 현행(2.1.303)에서는 2.1.283부터 대화형 세션의 기본 시작 모드다. 또 헤드리스(비대화형, `claude -p`)의 시작 모드는 한 번 바뀌고 되돌아갔다 — 2.1.285(2026-09-29)에서 서드파티 제공자·텔레메트리가 꺼진 환경의 `-p`를 auto로 바꿨고, 2.1.302(2026-10-16)에서 그 환경과 신규 설치를 다시 `default`로 되돌렸다(체인지로그 기준. 권한 모드 문서 본문은 2.1.303 시점에도 아직 2.1.285 서술을 담고 있다). 이 책은 현행을 따른다. 대화형은 "플랜 → 승인 → auto"를 기본 흐름으로 보고, CI에서는 시작 모드를 플래그로 늘 명시한다(12장).

권한 모드를 표로 한 번에 보자. CLI의 `--permission-mode`가 받는 값은 `default`·`acceptEdits`·`plan`·`auto`·`dontAsk`·`bypassPermissions`, 그리고 `default`의 별칭 `manual`이다.

| 모드 | 묻지 않고 실행하는 것 (공식 문서 요지) | 어울리는 자리 |
|---|---|---|
| `default` | 읽기만 | 낯선 리포, 처음 한 바퀴 |
| `acceptEdits` | 읽기, 파일 편집, 흔한 파일시스템 명령 | 편집은 믿고 셸은 보고 싶을 때 |
| `plan` | 읽기, 그리고 auto가 가능한 환경에서는 분류기가 승인한 명령 | 계획 단계 |
| `auto` | 전부 — 단, 백그라운드에서 분류기의 안전 검사를 거친다. 명시적 `ask` 규칙은 여전히 질문 | 긴 작업, 승인된 계획의 구현 (현행 대화형 기본) |
| `dontAsk` | 작업 디렉터리 안 읽기와 사전 승인 도구 — 질문이 뜰 행동은 거부 | 잠긴 CI와 스크립트 |
| `bypassPermissions` | 전부 | 격리된 컨테이너·VM에서만 |

참고로 2.1.299에서 `PreToolUse` 훅이 허용한 쓰기 작업을 플랜 모드가 실행하던 문제가 고쳐졌다. "읽기만 한다"는 약속도 패치로 다듬어지는 중이니, 버전을 함께 적어 두는 것이다.

### 어느 쪽이 나을까 — 플랜 모드 사용 기준표

그렇다면 늘 플랜 모드로 열어야 할까? 공식 Best practices는 그렇게 말하지 않는다. "Plan mode is useful, but also adds overhead. ... If you could describe the diff in one sentence, skip the plan." 플랜 모드는 유용하지만 오버헤드도 더한다. diff를 한 문장으로 설명할 수 있으면 계획을 건너뛰어라. 같은 문서가 반대편 함정도 짚는다. "Letting Claude jump straight to coding can produce code that solves the wrong problem." 바로 코딩에 뛰어들면 엉뚱한 문제를 푸는 코드가 나올 수 있다.

현장의 기준도 모여 있다. 블로그들 사이의 합의(데이터는 아니다)는 "3파일 이상이면, 리팩터·스키마·보안이 걸리면, 한 문장으로 설명이 안 되면 플랜, 한 줄 수정은 건너뛰기"다. 공식 문구와 같은 방향이다. 둘을 합쳐 기준표를 만들어 보자. 이 표는 코스 원문에 없는 것으로, 공식 문구와 현장 합의를 저자가 한데 묶었다.

| 신호 | 바로 코딩 (선택지 A) | 플랜 → 승인 → auto (선택지 B) |
|---|---|---|
| diff를 한 문장으로 설명할 수 있나 | 있다 | 없다 |
| 바뀌는 파일 수 | 1~2개 | 3개 이상 |
| 변경의 성격 | 오타·한 줄 수정·메시지 변경 | 리팩터, 스키마, 인증·보안, 외부 시스템 연동 |
| 뒤 단계가 대조할 문서가 필요한가 | 아니다 | 그렇다 (`plan.md`가 리뷰와 eval의 입력) |
| 되돌리는 비용 | 커밋 하나 revert | 여러 파일에 걸친 설계 되돌리기 |

"플랜 모드가 항상 낫다"고 여기기 쉽다. 하지만 두 가지를 생각해 보자. 첫째, 한 줄 수정에 계획을 받으면 계획을 읽는 시간이 수정 시간보다 길다. 그 오버헤드가 쌓이면 사람은 플랜 모드 자체를 끄게 되고, 그러면 정말 필요한 변경에서도 건너뛰게 된다. 둘째, 플랜 모드의 가치는 계획을 "심문"할 때 생긴다. 심문 없이 "Yes"만 누르는 플랜 모드는 바로 코딩에 한 턴을 더한 것뿐이다. 반대로 "바로 코딩이 항상 빠르다"도 착각이다. 한 블로그의 표현을 빌리면 "You're paying one extra turn to avoid a twenty-turn rework" — 스무 턴의 재작업을 피하려고 한 턴을 내는 것이다.

코스에는 "Legacy systems and the source of truth"라는 부속 절이 있다. 조직에는 이미 Jira·ServiceNow·요구사항 도구·변경 위원회가 있으니, 마크다운 아티팩트와 그 시스템 가운데 "하나를 소스 오브 트루스로 지명하고 나머지는 사본이나 링크를 쥔다"는 원칙이다. 코스는 리포가 진실인 구성, 레거시 시스템이 진실이고 마크다운이 작업 사본인 구성, 그리고 모든 아티팩트에 레코드 ID를·모든 레코드에 커밋 SHA를 적는 "연결(linkage)을 최소 기준으로" 삼는 구성 셋을 든다. 혼자 혹은 열 명 안쪽의 팀이라면 고민할 것이 없다. 리포가 진실이다 — 코스도 이 구성을 "모든 기록이 한 도구에, 한 타임스탬프 권위 아래" 있는 가장 깔끔한 구성 중 하나로 평한다.

### 왜 이 플레이인가

계획을 먼저 쓰는 것이 왜 효과가 있는지, 느낌 말고 근거를 보자.

학술 쪽에서 가장 가까운 것은 Wang 외의 Plan-and-Solve 프롬프팅(ACL 2023)이다. 이 연구는 단계별 사고(Zero-shot CoT)가 실패하는 세 가지 — 계산 오류, 단계 누락, 의미 오해 — 가운데 단계 누락을 줄이기 위해 "먼저 계획을 세우고 계획대로 수행하라"는 지시를 넣었고, 열 개 데이터셋에서 일관되게 나은 결과를 얻었다. `plan.md`의 "Order of work" 절이 하는 일이 정확히 이것이다. 단계를 미리 적어 두면 빠뜨리기 어렵다. Erdogan 외의 Plan-and-Act(ICML 2025)는 계획자와 실행자를 분리해 웹 탐색 벤치마크에서 성능을 끌어올렸다. 단, 도메인이 웹 탐색이지 코딩은 아니다. 코드 작업에 그대로 옮겨 쓸 수치로 읽지는 말자.

현장 데이터는 Watanabe 외의 TOSEM 연구가 준다. GitHub 157개 오픈소스 프로젝트에서 Claude Code가 도운 PR 567개를 보았을 때 83.8%가 결국 머지되었고, 머지된 PR의 54.9%는 추가 수정 없이 통합되었다. 코스가 이 플레이의 선행 지표로 든 "첫 구현 패스에서 머지되는 비율"의 현장 기준값 후보가 여기 있다. 사람이 손을 댄 사유는 버그 수정, 문서, 그리고 "프로젝트 고유 표준 준수"였다. 마지막 사유는 다음 장의 CLAUDE.md가 왜 필요한지를 미리 말해 준다.

하나 더. Shen과 Tamkin(Anthropic)의 연구 — 아직 심사 전인 연구다 — 는 AI를 쓰는 여섯 가지 상호작용 패턴 가운데 인지적으로 관여하는 세 가지가 학습을 보존한다고 보고한다. "AI-enhanced productivity is not a shortcut to competence" — 계획을 심문하는 행위는 그 관여형 패턴과 겹친다. 플랜 모드는 코드 품질만의 문제가 아니라, 우리가 자기 코드베이스를 계속 이해하고 있을 수 있는가의 문제이기도 하다.

마찰은 어디에 있을까? 흥미롭게도 "플랜 모드는 낭비다"라는 글은 찾기 어렵다. 건너뛰기의 유혹은 불만이 아니라 행동으로 나타난다. GitHub 이슈 #44246(2026-04)은 CLAUDE.md에 "plan mode before non-trivial tasks"를 적어 두어도 모델이 건너뛴다고 보고한다. 사람도 모델도 계획을 건너뛰고 싶어한다. 그래서 `defaultMode: plan`처럼 설정에 두는 것과, 계획이 나왔을 때 심문하는 습관을 몸에 붙이는 것이 함께 필요하다. 계획은 모델을 위한 문서이기도 하지만, 코드가 생기기 전에 사람이 개입할 수 있는 마지막 문서이기도 하다.

### 내 리포로 옮기기

`[개인 즉시]` 오늘 세션부터 바꿀 수 있는 것은 셋이다. 첫째, 계획이 뜨면 "Yes"를 누르기 전에 `Ctrl+G`로 열어 한 번 읽고, Risks 절에 빠진 것이 있으면 손으로 적어 넣는다. 둘째, 승인한 계획을 `intent/` 폴더에 `plan.md`로 커밋한다. `intent.md`·`spec.md` 옆에 두면 세 파일이 한 변경의 기록이 된다. 셋째, 구현이 계획에서 벗어나면 같은 커밋에서 `plan.md`를 고친다. 이것이 번거롭다면 그 번거로움이 신호다 — 계획이 틀렸거나 변경이 계획보다 커진 것이다. 코스가 권하는 훅 기반 동기화는 훅을 다루는 6장 뒤로 미뤄도 좋다. 그리고 위의 기준표를 자기 말로 다시 써 보자. 한 문장으로 설명되는 diff는 그냥 시키고, 세 파일을 넘으면 계획을 받는다.

`[팀 합의]` 팀이 있다면 `.claude/settings.json`에 `defaultMode: plan`을 두어 리포를 여는 모두가 계획부터 시작하게 할 수 있다. 단, `auto`와 `bypassPermissions`는 프로젝트 설정으로 켤 수 없다 — 사용자 설정이나 관리형 설정에서만 된다. 팀이 합의할 다른 하나는 `plan.md`의 커밋 위치와 파일명이다. 리뷰어가 PR을 열었을 때 어디를 보면 계획이 있는지 알아야 10장의 compliance 리뷰가 성립한다.

`[조직 결정]` 코스의 소스 오브 트루스 3구성과 "고위험 변경은 아키텍트 승인"은 Jira·ServiceNow·변경 위원회가 있는 조직의 이야기다. 그런 층이 없다면 리포가 진실이고 승인자는 자기 자신이다. 조직이 커져 외부 시스템이 생기면 "연결을 최소 기준으로"에서 시작하면 된다.

측정은 개인판으로 두 개만. 선행 지표는 코스의 "첫 구현 패스에서 머지되는 비율"을 그대로 쓴다. 개인 리포라면 PR을 열고 추가 커밋 없이 머지한 비율을 `git log`로 셀 수 있다. 54.9%가 현장 기준값 후보라는 점을 기억하면서, 자기 수치가 그보다 낮다면 계획이 느슨한지 심문이 느슨한지 들여다보자. 지연 지표는 코스의 "머지된 diff가 여전히 `plan.md`와 일치하는가"를 개인판으로 바꾼 "`plan.md` 갱신 없이 구현이 이탈한 횟수"다. 세는 방법은 간단하다. 머지 전에 `plan.md`의 Files that change 절과 실제 diff의 파일 목록을 한 번 나란히 보는 것.

플랜을 승인하고 auto로 넘겼다. 분류기가 행동을 걸러 주고, `plan.md`는 커밋되어 있다. 그런데 그 세션이 코드를 치기 전에 읽은 파일이 하나 더 있다. Claude가 매 세션 읽는 그 파일에는 무엇이 적혀 있어야 할까?
