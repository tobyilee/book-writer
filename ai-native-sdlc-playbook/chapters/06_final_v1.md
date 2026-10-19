# 6장. 스킬과 빌드 훅 — 절차는 스킬로, 반드시는 훅으로

### 잘려 나간 줄의 정체

앞 장에서 CLAUDE.md를 줄였다. 잘려 나간 줄 가운데 "~할 때는 1, 2, 3 순서로"로 시작하는 것이 있었을 것이다. 그 줄은 사실이 아니라 절차다. "claims-api는 FastAPI다"는 읽는 순간 끝나는 정보지만, "엔드포인트를 만들 때는 인증을 확인하고, 스키마로 검증하고, 감사 이벤트를 남기고, PII 필드를 로그에서 빼라"는 네 단계짜리 일이다. 이런 줄이 CLAUDE.md에 있으면 매 세션 토큰을 쓰면서도, 엔드포인트와 무관한 세션에서는 아무 쓸모가 없다.

그렇다면 그 줄은 어디로 가야 할까? 질문을 조금 바꿔 보자. 세 번째로 같은 지시를 채팅창에 붙여 넣고 있다면, 그 지시는 어디에 살아야 할까? 공식 스킬 문서가 바로 답한다. "Create a skill when you keep pasting the same instructions, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact." 이유도 적혀 있다. "Unlike CLAUDE.md content, a skill's body loads only when it's used" — 스킬의 본문은 쓰일 때만 로드되므로 긴 참고 자료도 필요할 때까지는 거의 비용이 들지 않는다.

코스 레슨 6의 정의는 더 간결하다. 스킬은 "a folder containing a `SKILL.md` whose frontmatter says when it triggers and whose body says what to do" — `SKILL.md` 하나가 든 폴더이고, frontmatter가 언제 발동하는지를, 본문이 무엇을 할지를 말한다. 그리고 코스가 보는 스킬의 역할은 조직적이다.

> "Skills are how an organization makes its institutional knowledge operational. The instructions are explicit, version controlled, applied broadly, and updated centrally when policy changes. The rule of thumb: write a skill for institutional knowledge that must be applied consistently; don't write a skill for components that belong in `CLAUDE.md` or a prompt."
>
> 스킬은 조직이 제도적 지식을 작동하게 만드는 방법이다. 지시는 명시적이고, 버전 관리되고, 넓게 적용되며, 정책이 바뀌면 중앙에서 갱신된다. 경험칙은 이렇다 — 일관되게 적용되어야 하는 제도적 지식에는 스킬을 쓰고, CLAUDE.md나 프롬프트에 속하는 것에는 스킬을 쓰지 말라. (코스 레슨 6)

"제도적 지식(institutional knowledge)"이라는 말이 혼자 일하는 독자에게는 멀게 들릴 수 있다. 그런데 개인에게도 제도는 있다. 커밋 전에 꼭 돌리는 체크리스트, 새 엔드포인트를 열 때마다 확인하는 네 가지. 매번 머릿속에서 꺼내 다시 타이핑하는 그것이 개인의 제도다. 현장의 한 블로그가 제안한 테스트 문장도 쓸 만하다 — "이 프로젝트에서는…"으로 시작하는 생각이면 CLAUDE.md, 여러 CLAUDE.md에 같은 지시가 반복되면 스킬.

### 코스의 여섯 단계와 `secure-api-review`

코스의 실행 단계는 여섯이다. 하나씩 보자.

1. 오늘 일관되지 않게 지켜지는 지식 하나를 고른다. 보안 표준, API 설계 컨벤션, 브랜드 규칙 같은 것.
2. 그것을 스킬로 쓴다. 정책 소유자의 원본 문서에서 Claude의 도움을 받아 쓴다.
3. 리포의 `.claude/skills/<name>/`에 둔다. 조직 전체에는 플러그인으로.
4. 스킬이 발동하는지 테스트한다. "Ask Claude to do the relevant task in different ways and confirm the skill loads each time."
5. 정책이 바뀌면 스킬을 바꾸고 정책 소유자가 사인오프한다.
6. 엔지니어는 다음 세션에서 새 판본을 자동으로 받는다.

4번을 가볍게 넘기지 말자. 발동 조건이 frontmatter의 자연어 설명이라서, 요청이 늘 예상한 표현으로 들어오지는 않는다. "엔드포인트 하나 추가해 줘", "status 라우트 만들자", "API에 조회 기능 넣어" — 세 가지 말로 요청해 세 번 모두 로드되는지 보는 것이 테스트다. 이 테스트를 건너뛴 스킬은 있는지도 모른 채 조용히 잠들어 있다.

관통 예제의 스킬을 원문 그대로 보자. 파일 위치는 `.claude/skills/secure-api-review/SKILL.md`다.

```markdown
---
name: secure-api-review
description: Apply the API security standard. Use whenever creating or
  modifying an external-facing endpoint, reviewing API code, or
  generating an OpenAPI spec.
---
# Secure API review
When you create or change an API endpoint:
1. Authentication: every endpoint requires the gateway JWT;
   no anonymous routes outside /health.
2. Input validation: validate request bodies against the OpenAPI
   schema and reject unknown fields.
3. Audit: every state-changing endpoint emits an audit event with
   actor, action, entity and timestamp.
4. Data classification: fields tagged pii in the schema must never
   appear in logs or error messages.
Run scripts/check-endpoints.sh and include its output in your summary.
```

frontmatter의 `description`이 발동 조건이다. 외부 노출 엔드포인트를 만들거나 고칠 때, API 코드를 리뷰할 때, OpenAPI 스펙을 생성할 때. 본문은 네 규칙과 한 줄의 실행 지시다. 앞 장의 CLAUDE.md와 겹쳐 보자. Things Claude gets wrong에 "Do not log request or response bodies in claims-api; they can hold PII"가 있었다. 같은 정책이 여기서는 규칙 4 — "fields tagged pii in the schema must never appear in logs or error messages" — 로 적혀 있다. 하나는 회귀 제약으로 매 세션 상주하고, 하나는 엔드포인트를 건드릴 때만 로드되는 절차다. 중복이 아니라 층이 다르다. 마지막 줄이 가리키는 `scripts/check-endpoints.sh`는 곧 다시 나온다.

코스의 거버넌스 문단은 2장에서 통제 3층의 정전으로 이미 인용했다. 여기서 되새길 것은 한 문장이다. "The skill makes violations rare and the hook makes them close to impossible." 스킬은 위반을 드물게 하고, 훅은 거의 불가능하게 한다. 측정도 그 성격을 반영한다. 선행 지표는 정책 소유자가 변경을 승인한 때부터 갱신된 스킬이 머지되기까지의 시간, 지연 지표는 "그 정책을 인용하는 PR 리뷰 발견 건수"다.

### 현행 사양: 스킬

Claude Code 2.1.303 / 2026-10 기준으로 스킬이 사는 곳은 다섯이다 — 엔터프라이즈(관리형 설정 디렉터리), 개인 `~/.claude/skills/<skill-name>/SKILL.md`, 프로젝트 `.claude/skills/<skill-name>/SKILL.md`, 하위 디렉터리 `<subdir>/.claude/skills/<skill-name>/SKILL.md`, 플러그인 `<plugin>/skills/<skill-name>/SKILL.md`. "Where you save a skill decides which sessions load it" — 어디에 저장하느냐가 어느 세션이 로드하느냐를 정하고, 이름이 충돌하면 엔터프라이즈가 개인을, 개인이 프로젝트를 이긴다.

frontmatter 필드는 많지만(`name`, `description`, `when_to_use`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `paths`, `hooks` 등) 공식 문서는 분명히 말한다. "All fields are optional. Only `description` is recommended so Claude knows when to use the skill." 전부 선택이고, Claude가 언제 쓸지 알 수 있도록 `description`만 권장된다 — 코스의 `secure-api-review`가 그 모양이다. 함정이 둘 있다. 필드 이름은 하이픈까지 정확히 일치해야 하고, 모르는 필드는 오류 없이 조용히 무시된다. 그리고 스킬 목록에서 `description`과 `when_to_use`를 합친 텍스트가 1,536자에서 잘리므로 핵심 용례를 앞에 둔다. `disable-model-invocation: true`면 사람만, `user-invocable: false`면 Claude만 부를 수 있다 — 배포 절차처럼 사람이 시작해야 하는 스킬과 코드 작성 중 조용히 적용되는 스킬을 이 둘로 가른다.

길이 규칙도 있다. "Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files." 이유는 비용이다. "Once a skill loads, its content stays in context across turns, so every line is a recurring token cost." 한 번 로드된 스킬은 이후 턴에도 컨텍스트에 남아, 매 줄이 반복되는 토큰 비용이 된다. CLAUDE.md보다는 싸지만 무료는 아니다.

> **구버전 주의**
> 코스(2026-08)는 "organization-level slash command"처럼 슬래시 커맨드를 스킬과 별개의 것으로 언급한다. 현행(2.1.303)에서는 커맨드가 스킬에 통합되었고(공식 문서는 통합된 버전을 따로 적지 않는다), 새로 만드는 것은 `SKILL.md`로 쓰라고 권한다. 이 책은 현행을 따라 "스킬"로만 부른다. 기존 커맨드 파일을 쓰고 있다면 그대로 동작하지만, 새 절차는 스킬 폴더로 만드는 편이 낫다.

경고 하나. 스킬은 스크립트 실행을 지시할 수 있고, ITWorld 코리아는 "스킬을 켜면 악성 코드가 실행될 수 있다"고 짚었다. 출처가 불분명한 스킬을 받아 쓰는 것은 출처가 불분명한 패키지를 설치하는 것과 같은 일이다.

### 빌드 훅: 권고 뒤의 결정론

여기까지 읽고 의문이 들었을 것이다. 스킬도 결국 텍스트인데, 앞 장의 CLAUDE.md처럼 무시되면? 코스는 그 질문을 레슨 6의 부속 절에서 받는다.

> "A skill is an advisory control, while a hook is the deterministic layer behind it. Most of Claude's actions are file edits and shell commands during implementation, so the build phase is where hooks can end up firing most often."
>
> 스킬은 권고적 통제이고, 훅은 그 뒤에 있는 결정론적 층이다. Claude의 행동 대부분은 구현 중의 파일 편집과 셸 명령이므로, 빌드 단계가 훅이 가장 자주 발동하게 되는 곳이다. (코스 레슨 6)

빌드 단계의 훅이 할 수 있는 일로 코스는 넷을 든다. 보호 경로의 편집 차단, 편집 뒤 포매터·린터 실행, 자격 증명이 diff에 들어가지 않게 하는 것, 그리고 "예외 없이 지켜져야 하는 정책을 가진 스킬을 뒤에서 받치는 것". 설계 원칙은 하나다 — "build-phase hooks should be fast and scoped to the file that changed. Heavier checks such as the full test suite belong at the commit or the PR." 훅은 매칭되는 행동마다 돌아가므로 빠르고 바뀐 파일에만 좁게 걸고, 전체 테스트 스위트 같은 무거운 검사는 커밋이나 PR에 둔다.

이제 스킬의 마지막 줄이 가리키던 스크립트가 돌아온다. 코스는 `secure-api-review`의 규칙 4를 받치는 훅을 보여 준다. 엔드포인트 파일은 `claims-api/routes/`에 살고, 그 폴더의 파일이 편집될 때마다 훅이 `scripts/check-endpoints.sh`를 돌린다. 이 스크립트는 OpenAPI 스키마에서 `pii`로 태그된 필드가 로그 호출이나 raise된 에러에 닿으면 실패한다. 훅은 `.claude/settings.json`에 등록한다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/api-policy.sh",
            "args": [] }
        ]
      }
    ]
  }
}
```

`PostToolUse`는 도구가 실행된 뒤에 발동하는 이벤트고, `matcher`의 `Edit|Write`는 그 두 도구에만 건다는 뜻이다. 빈 `args` 목록은 코스의 설명대로 "run the script directly instead of through a shell" — 셸을 거치지 않고 스크립트를 직접 실행하게 한다. 스크립트 자체는 이렇다.

```bash
#!/bin/bash
# Backs rule 4 of the secure-api-review skill with the same script the skill runs.
file=$(jq -r '.tool_input.file_path')
case "$file" in
  "$CLAUDE_PROJECT_DIR"/claims-api/routes/*.py) ;;
  *) exit 0 ;;  # not an endpoint
esac
cd "$CLAUDE_PROJECT_DIR" || exit 2
if ! found=$(scripts/check-endpoints.sh "${file#"$CLAUDE_PROJECT_DIR"/}"); then
  echo "secure-api-review rule 4: a pii field reaches a log or an error message." >&2
  echo "$found" >&2
  exit 2
fi
```

훅은 표준 입력으로 JSON을 받고, `jq`로 편집된 파일 경로를 꺼낸다. 경로가 `claims-api/routes/*.py`가 아니면 `exit 0`으로 조용히 빠진다 — "빠르고 좁게"의 구현이다. 엔드포인트 파일이면 스킬이 가리키던 바로 그 스크립트를 돌리고, 실패하면 `exit 2`로 끝난다. 사람이 읽는 규칙(스킬)과 기계가 확인하는 검사(훅)가 한 스크립트를 공유하므로 둘이 어긋날 수 없다.

`exit 2`의 의미를 정확히 알아 두자. "A hook that runs after an edit cannot undo it, so exit code 2 puts the script's message in front of Claude, which can then fix the line." 편집 뒤에 도는 훅은 편집을 되돌릴 수 없다. 그래서 `exit 2`는 메시지를 Claude 앞에 놓고 그 줄을 고치게 한다. 고객 이름을 로그에 남기는 편집 뒤 Claude가 보는 메시지는 이렇다.

```text
secure-api-review rule 4: a pii field reaches a log or an error message.
claims-api/routes/status.py:10: policy_holder_name
```

`policy_holder_name` — 이 필드 이름도 체인의 키다. 10장의 `REVIEW.md` Security 패스가 에러 경로에서 같은 필드를 찾아내고, 9장의 eval이 같은 스크립트를 호출한다.

그런데 구멍이 하나 있다. "An `Edit|Write` hook does not fire when a shell command rewrites the file." Claude가 `sed`나 리다이렉션으로 파일을 고치면 이 훅은 발동하지 않는다. 코스의 답은 같은 스크립트를 PR의 필수 체크로도 돌리는 것이다.

```yaml
name: API policy
on: pull_request
jobs:
  check-endpoints: # a required check in branch protection
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: scripts/check-endpoints.sh claims-api/routes/*.py
```

"The hook catches a violation at the edit, and the same check on the pull request catches anything that reached the branch another way." 훅은 편집 시점에서 잡고, PR 체크는 다른 경로로 브랜치에 도달한 것을 잡는다. 같은 스크립트가 세 곳에서 돈다 — 스킬이 시키는 자리, 훅, PR. 한 정책, 한 스크립트, 세 지점.

코스는 이 절을 한 가지 선 긋기로 끝낸다. "A hook that asks a human for approval belongs with the gates in Stage 5: Deploy, because an approval prompt during the build puts a person back on the critical path of all the sessions running in parallel." 빌드 중의 승인 프롬프트는 병렬로 도는 모든 세션의 크리티컬 패스에 사람을 다시 올려 놓는다. 그래서 빌드 훅은 묻지 않는다. 막거나, 고치게 하거나, 통과시킨다. 묻는 훅은 11장에서 만난다.

### 현행 사양: 훅, 빌드 단계에서 알아야 할 만큼만

훅의 전체 사양 — 이벤트 목록, `permissionDecision`, 설정 층의 우선순위 — 은 11장이 본진이다. 여기서는 빌드 훅을 하나 쓰는 데 필요한 만큼만 Claude Code 2.1.303 / 2026-10 기준으로 정리한다.

먼저 `exit 2`의 공식 의미. "Exit with code 2 to block the action." 그런데 바로 이어서 — `PreToolUse`의 도구 호출과 `UserPromptSubmit`의 프롬프트는 막지만 "has no blocking effect on `PostToolUse`, where it only shows stderr to Claude." 코스가 "편집 뒤의 훅은 되돌릴 수 없다"고 쓴 것과 같은 말이다. `PostToolUse`가 JSON으로 답할 수도 있다 — `decision`을 `"block"`으로 주면 `reason`이 도구 결과 옆에 붙고, 출력을 바꿔치기하려면 `updatedToolOutput`을 쓴다.

`matcher`는 `"*"`·`""`·생략이면 전부에 걸리고, 영숫자·`_`·`-`·공백·`,`·`|`만 들어 있으면 정확한 이름 또는 목록(`Edit|Write`)으로, 그 밖의 문자가 있으면 앵커 없는 자바스크립트 정규식으로 해석된다. `args` 필드가 있으면 `command`는 셸 없이 직접 스폰되고, `CLAUDE_PROJECT_DIR`는 세션이 시작된 프로젝트 루트다. 타임아웃은 대부분 기본 600초(`UserPromptSubmit`은 30초)이고, `"async": true`로 비동기로 돌릴 수 있지만 "Async hooks can't block or control Claude's behavior" — 비동기 훅은 막지 못한다.

입문자가 먼저 만들 훅 두 개는 공식 문서에 예가 있다. 포매터는 `PostToolUse`에 `Edit|Write`로 걸고 명령은 `jq -r '.tool_input.file_path' | xargs npx prettier --write`. 보호 파일은 `PreToolUse`에서 `.env`, `package-lock.json`, `.git/` 안의 경로를 보고 `exit 2`로 차단한다 — 이쪽은 `PreToolUse`이므로 정말로 막힌다.

이벤트는 30종이 넘고(`SessionStart`, `PreToolUse`, `PostToolUse`, `Stop`, `ConfigChange`, `WorktreeCreate` 등) 훅 타입도 command·http·mcp_tool·prompt·agent 다섯이지만, 이 책은 command 타입만 쓴다. 2.1.295에 추가된 `onFailure: "block"`은 시작하지 못하거나 타임아웃되거나 예상 밖 코드로 끝난 훅이 행동을 통과시키는 대신 막게 한다 — 훅이 실패하면 열리지 않고 닫힌다(fail-closed). 보안도 한 줄 — 훅은 사용자의 전체 권한으로 실행되므로 셸 변수는 항상 인용하고(`"$VAR"`), 경로의 `..`를 막고, `.env`·`.git/`·키 파일은 건너뛴다. 코스의 `api-policy.sh`가 모든 변수를 큰따옴표로 감싼 이유다. 그리고 공식 Best practices의 한 줄 — "Claude can write hooks for you." 훅을 처음 쓰는 독자에게 가장 빠른 길이다.

### 어디에 무엇을 — 그리고 왜 이 플레이인가

"스킬로 만들었으니 지켜지겠지"라고 생각하기 쉽다. 하지만 코스 자신이 스킬을 "a control, though an advisory one" — 통제이되 권고적인 통제 — 라고 불렀다. 이 장의 제목이 둘로 나뉜 이유다. 절차는 스킬로, 반드시는 훅으로.

세 층을 한 표로 정리해 보자. 코스의 3분법과 공식 문서의 기준, 현장의 경험칙을 저자가 한데 모았다.

| 줄의 성격 | 어디에 | 로드 시점 | 보장 수준 | 예 |
|---|---|---|---|---|
| 사실·회귀 제약 ("이 프로젝트에서는…") | CLAUDE.md | 매 세션 시작 | 권고 | "claims-core는 50 rps. 캐시하고 폴링하지 말 것" |
| 절차·체크리스트 (세 번째로 붙여 넣는 것) | 스킬 `SKILL.md` | 발동 시 | 권고 | 엔드포인트 생성 시 네 규칙 |
| 반드시 (예외 없이) | 훅 — 또는 린터·테스트 | 매칭되는 행동마다 | 결정론적 | `pii` 필드가 로그에 닿으면 `exit 2` |

현장은 이 분류를 고통으로 먼저 배웠다. HN의 한 사용자는 "No matter how many times I told it, it lints randomly" — 아무리 말해도 린트를 들쭉날쭉 돌린다고 썼고, HumanLayer의 글은 그 답을 한 문장으로 남겼다. "Never send an LLM to do a linter's job." 린터가 할 일을 LLM에게 보내지 말라.

한국 현장에서 가장 선명한 사례는 토스 테크의 글(2026-02)이다. 팀의 워크플로를 훅과 커맨드가 든 플러그인으로 배포하고 그것을 "실행 가능한 SSOT"라고 부른다. "플러그인 코드가 업데이트되면, 팀원들의 에이전트 행동 양식도 즉시 업데이트됩니다." 린터와 비교한 문장도 좋다. "기존의 린터(Linter)가 단순히 에러를 뱉고 차단했다면, 플러그인은 팀의 규율에 맞게 행동을 교정(Align)해주는 가이드 역할을 수행할 수 있습니다." `exit 2`가 메시지를 Claude 앞에 놓고 고치게 하는 것이 정확히 이 "교정"이다. GPTers의 한 후기는 개인 규모의 같은 경험이다 — "한 번 정해두니 다음부터는 안 알려줘도 에이전트가 알아서 지킵니다."

학술 근거는 셋이다. Galster 외(AIware 2026)의 2,853개 리포 연구에서 스킬과 서브에이전트를 채택한 리포는 소수였고, 채택된 스킬도 대부분 정적 지시였다. Vijayvergiya 외의 Google AutoCommenter(AIware '24)는 코딩 모범 사례를 LLM이 코드 리뷰에서 강제하는 시스템을 Google 규모로 배포한 선례다. 그리고 Grynets 외의 명세 주도 개발 벤치마크(2026, 아직 심사 전인 연구)에서는 보안 요구를 따로 명시하지 않은 기준선에서 보안 실패가 가장 많았고, 명세에 보안 층을 더할수록 줄었다. 보안 규칙이 어디엔가 적혀 있어야 하고 그 "어디"가 매번 프롬프트일 수 없다면, `secure-api-review` 같은 스킬이 그 자리다.

### 내 리포로 옮기기

`[개인 즉시]` 첫 스킬은 오늘 만들 수 있다. 최근 일주일 동안 채팅창에 세 번 이상 붙여 넣은 지시가 있는가? 그것을 `~/.claude/skills/<이름>/SKILL.md`로 옮긴다. frontmatter에는 `name`과 `description`만, 본문은 코스 예시처럼 번호 매긴 규칙으로. 그다음 같은 작업을 세 가지 다른 말로 요청해 세 번 모두 로드되는지 본다. 첫 훅도 둘로 시작하자. 포매터 `PostToolUse`(공식 prettier 예시를 자기 포매터로 바꾼다)와 `.env`·lock 파일을 지키는 `PreToolUse` `exit 2`. 테스트 파일을 지키는 훅은 8장에서 더한다. Claude에게 시켜도 되지만, 생성된 스크립트의 변수가 인용되어 있는지는 눈으로 확인하자.

`[팀 합의]` 팀의 스킬은 `.claude/skills/<name>/`에 커밋한다. 코스 6단계대로 팀원은 다음 세션에서 자동으로 받는다. 훅 설정 `.claude/settings.json`도 커밋한다. 토스처럼 플러그인으로 묶는 것은 2~10명 팀에서도 가능하지만 선택이다. 스킬 폴더의 변경은 PR로 받고, 코스 5단계의 "정책 소유자 사인오프"는 팀에서 그 영역을 가장 잘 아는 한 사람의 승인으로 번역한다.

`[조직 결정]` 플러그인 마켓플레이스로 조직 전체에 배포하는 층, 정책 소유자의 공식 사인오프, 엔터프라이즈 스킬 디렉터리가 있다. 조직 층이 없는 독자의 대체 경로는 리포 커밋과 PR 리뷰다.

측정은 코스의 지연 지표를 개인판으로 바꾼다. "그 정책을 인용하는 PR 리뷰 발견이 0을 향해 줄어드는가"는 `/code-review` 결과에서 같은 지적이 반복되는 횟수로 셀 수 있다. 스킬을 만든 뒤에도 같은 지적이 반복된다면 둘 중 하나다 — 스킬이 발동하지 않거나(4단계 테스트로 돌아간다), 발동했는데도 지켜지지 않는다. 후자라면 이 장이 할 말은 하나다. 스킬이 안 지켜질 때 화내지 말자. 그 규칙은 처음부터 훅이어야 했다.

### 이 장의 핵심

- 세 번째로 같은 지시를 붙여 넣고 있거나 CLAUDE.md의 한 절이 절차로 자랐다면 스킬이다(공식 기준). 본문은 발동 시에만 로드되고, 한 번 로드되면 턴마다 남는다.
- 스킬은 권고적 통제다. "스킬은 위반을 드물게, 훅은 거의 불가능하게"(코스 레슨 6). 예외 없이 지켜져야 하는 규칙은 스킬 뒤에 훅을 둔다.
- 빌드 훅은 빠르고 좁게. `PostToolUse` `exit 2`는 편집을 되돌리지 못하고 메시지를 Claude 앞에 놓아 고치게 한다. 셸로 고친 파일은 훅이 못 보므로 같은 스크립트를 PR 필수 체크로도 돌린다.
- 사람에게 묻는 훅은 Deploy의 게이트에 둔다. 훅의 전체 사양은 11장이 본진이다.
