# 2장. 도구 생태계 — Claude Code와 Codex의 실체

금요일 오후, 팀 슬랙에 한 줄이 올라왔다고 해보자. "사내 표준 코딩 에이전트를 정해야 합니다. 후보는 Claude Code와 Codex CLI. 결정 권한은 당신에게." 후보가 무엇인지는 모두가 안다. 두 달쯤 써봤고 익숙한 쪽을 고르고 싶지만, 결정하는 순간부터 비용이 쌓인다. 구독, 라이선스, 온보딩 문서, 팀원의 근육기억, 그 위에 쌓일 훅과 서브에이전트와 스킬까지 — 한번 고르면 되돌리는 데 드는 비용이 선형이 아니다.

1장에서 하네스를 "복합 AI 시스템을 조립한 마구"로 정의했다. 마구를 어떤 금속으로 만들 것인가가 이제 질문이다. 기억해두자 — **도구는 실행 바이너리가 아니라 "어떤 방식으로 실패하게 할 것인가"의 선택이다.** Claude Code와 Codex는 같은 일을 다르게 실패한다. 어디서 멈추고, 어디서 폭주하고, 어디서 토큰을 태우는지가 다르다. 2장은 이 발산 지점을 해부한다. "컨텍스트가 99%다"라는 3장 주제는 미뤄두고, 우선 두 도구의 **내부 메커니즘**부터 들여다보자.

## Claude Code의 메커니즘 — 훅과 스킬로 결합된 통제 장치

Claude Code가 Codex와 본질적으로 다른 지점은 "**모델이 무엇을 하는가**"가 아니라 "**모델 주변에 무엇이 붙어 있는가**"다.

먼저 **메모리 파일 `CLAUDE.md`**. 프로젝트 루트에서 홈까지 상향 트래버스하며 발견되는 모든 `CLAUDE.md`를 **병합**한다. 덮어쓰기가 아니라 누적이다. 모노레포에서 여러 레이어가 동시에 반영되면 어느 규칙이 살아남았는지 추적하기 난감하다. 공식 권장은 60줄 이하, 커뮤니티 실무 합의는 200줄 이하(HN #44957443). 이 숫자가 기분 때문이 아니라 **컨텍스트 오염을 억제하기 위한 경제학**임은 3장에서 본격적으로 다룬다.

다음 **서브에이전트**. `.claude/agents/<name>.md`에 YAML 프런트매터로 선언하며 필수는 `name`·`description`. 선택 필드 `tools`·`model`·`permissionMode`·`mcpServers`·`hooks`·`skills`·`isolation` 중 `tools`를 생략하면 부모 에이전트의 툴 집합을 **상속**한다. 서브에이전트마다 허용 툴을 다시 적는 건 번거롭고 휴먼 에러의 온상이니, 이 상속이 실무에서 가장 쓸모 있다.

그중 `isolation: worktree`를 짚어두자. 서브에이전트를 깃 워크트리 안에서 실행시켜 부모의 파일시스템과 **물리적으로 격리**한다. 다중 에이전트가 같은 파일을 동시에 쓰는 난감한 사태를 — 그걸 디버깅해야 하는 끔찍한 시간을 — 차단한다.

세 번째, **Skills와 Slash commands의 관계**. v2.1부터 같은 `/slash-command` 인터페이스로 통합됐다. 이름이 비슷해 혼동되지만 역할이 다르다. Slash command는 사용자가 직접 부르는 **단일 파일**짜리 프롬프트 레시피, Skill은 모델이 자동 호출하는 **다중 파일** 번들이며 프런트매터로 `disable-model-invocation`·`user-invocable`·`allowed-tools`를 세밀하게 통제한다. Slash는 "사람이 이 순서로 해달라"의 템플릿, Skill은 "상황이 이러면 알아서 꺼내 쓰라"의 위임. 같은 입구를 공유하되 결정권이 다른 쪽에 있다. v2.1.73에서 `/output-style`은 deprecated됐다 — 버전 의존 기능임을 기억해두자.

네 번째, Claude Code를 "통제 가능한 도구"로 만드는 결정적 장치 — **훅(hooks)**. v2.1 기준 **27종**. 세 그룹으로 묶으면 툴 호출 주변(`PreToolUse`·`PostToolUse`·`PostToolUseFailure`·`PermissionRequest`·`PermissionDenied`), 세션 수명 주기(`SessionStart`·`UserPromptSubmit`·`Stop`·`SessionEnd`·`Notification`), 서브에이전트·태스크·파일시스템 이벤트군(`SubagentStart/Stop`·`TaskCreated/Completed`·`FileChanged`·`WorktreeCreate/Remove`·`PreCompact/PostCompact`·`ConfigChange`·`CwdChanged`·`Elicitation` 등).

훅의 강제력이 중요하다. 공식 문서 인용 — *"A hook that returns permissionDecision: 'deny' blocks the tool even in bypassPermissions mode or with --dangerously-skip-permissions."* (Hooks guide, 접속 2026-04-20). 즉 훅은 `--dangerously-skip-permissions`를 뚫고도 유효한 **유일한 강제 게이트**다. "이것만은 절대 못 한다"를 박아두고 싶다면 프롬프트로 설득하지 말고 훅으로 끊어내는 편이 낫다.

다섯 번째, **MCP 명명 규약**. 툴 이름은 `mcp__<server>__<tool>` 꼴로 고정된다. 덕분에 권한 설정이 글롭 매칭으로 깔끔해진다 — `mcp__github__*` 한 줄이면 GitHub MCP 서버 전체가 한꺼번에 통제된다. 기본 설정에서 `WebSearch`와 `WebFetch`는 비활성 — 프롬프트 인젝션 표면을 줄이기 위한 합리적 기본값이다.

끝으로 **설정 스코프 우선순위**. User → Project committed → Project local → Managed policy. Managed policy는 기업 관리자가 잠그는 상자이며 **최우선**. 평가 순서는 deny → ask → allow, 첫 매치가 승. 프로젝트의 `deny`가 유저의 `allow`를 이긴다. 이 순서를 몰라서 "왜 내 allow가 안 먹죠"라는 질문이 포럼에 매일 올라온다. 좁은 쪽과 강한 쪽이 이긴다 — 외워두자.

## Codex CLI의 메커니즘 — OS가 강제하는 경계

Codex의 설계 철학은 공식 문서 한 문장으로 요약된다. *"Sandbox enforces technical boundaries; approval enforces interaction boundaries."* (Codex Security, 접속 2026-04-20). 두 레이어가 **독립적으로** 작동한다. 샌드박스는 OS가 강제하는 물리 경계, approval은 사람이 끼어드는 상호작용 경계. 한쪽을 뚫어도 다른 쪽이 남는다.

**샌드박스 3모드**. `workspace-write`가 기본값 — 워크스페이스 내 읽기·쓰기가 자유롭되 `.git`, `.agents`, `.codex` 세 디렉터리는 쓰기 가능 모드에서도 read-only를 유지한다. 에이전트가 실수로든 고의로든 `.git`을 조작하지 못하게 막는 장치다. `read-only`는 말 그대로 읽기만. `danger-full-access`는 모든 보호 제거 — 공식 권장이 아니며, 써야 한다면 컨테이너 안에서만 쓰라는 게 실무 합의다.

**Approval policy 4종**. `on-request`가 인터랙티브 기본값 — 샌드박스 경계·네트워크 이탈 시 질의. `never`는 질의 차단으로 비인터랙티브·CI 전용. `untrusted`는 안전한 read는 자동 승인·state-mutating은 질의. `granular`는 범주별 선택. 기본 `on-request`로 대화형 개발을 하다가 CI용으로 `never` + `read-only`를 조합하는 구성이 자주 보인다. 반드시 기억할 플래그 하나 — `--dangerously-bypass-approvals-and-sandbox`. 이름이 이렇게 긴 이유는 짐작할 만하다(실수 타이핑 방지). 켜면 샌드박스도 approval도 모두 제거된다. 찜찜한 느낌이 들어야 정상이다.

그리고 결정적 차이. **OS-enforced 샌드박스**. macOS는 Seatbelt(sandbox-exec), Linux는 Landlock 계열 LSM을 쓴다. Claude Code의 경계는 훅과 권한 규칙 — 즉 **에이전트 프로세스 내부**의 소프트 경계다. Codex의 경계는 OS 커널이 강제하는 **프로세스 바깥**의 하드 경계다. 하드 경계는 한번 켜두면 모델 프롬프트가 아무리 구슬러도 깨지지 않는다. 대신 설정이 까다롭고, 특히 macOS Seatbelt는 에러 메시지가 불친절해 디버깅이 초난감한 경우가 있다. `AGENTS.md`는 세션 시작 시 1회 로드되며, 조회 순서와 "가장 가까운 것이 이긴다" 규칙은 3장에서 다룬다.

## 발산 지점 — 두 도구를 나란히

메커니즘을 따로 훑었으니 한 표에 놓고 비교해보자.

| 축 | Claude Code (v2.1, 2026-04) | Codex CLI (2026-04) |
|---|---|---|
| 샌드박스 | 약함 — 훅·권한 규칙(프로세스 내부) | **강함** — OS-enforced Seatbelt/Landlock(외부) |
| 자율성 | supervised — plan mode + 훅 중단 지점 | unsupervised — full-auto 1~30분 비동기 |
| 토큰 기본값 | Extended thinking **on** | thinking **off** |
| 토큰 소비 실측 | Codex 대비 **약 4×** (Builder.io Figma→Code, 6.2M vs 1.5M, N=1 한계) | 기준점 |
| 장시간 세션 drift | 2시간+ 세션에서 초기 결정 망각, 재주입 필요 | `AGENTS.md` 1회 로딩, 재주입 수단 빈약 |
| 훅 | 27종, `permissionDecision:'deny'` 강제력 | 제한적, approval policy로 대체 |

출처: Claude Code docs, Codex docs, thoughts.jock.pl "AI Coding Harness Agents 2026", builder.io "Codex vs Claude Code"(접속 2026-04-20).

**샌드박스 강도**가 갈리는 이유는 설계 철학이 다르기 때문이다. Claude Code는 "훅과 권한으로 통제 가능하다", Codex는 "모델은 잘못할 수 있으니 OS로 막자". 전자는 감시자가 옆에 있을 때 강하고, 후자는 없을 때 안전하다. 이것이 **자율성 축**에 연결된다. Claude Code는 plan mode와 훅 중단이 자연스럽고, Codex는 1~30분짜리 비동기 태스크를 후방에 돌리는 패턴이 공식 가이드에 녹아 있다. 혼자 두고 회의에 다녀와도 OS 샌드박스가 받쳐준다. **장시간 세션 drift**는 양쪽 모두의 취약지대이되 완화 수단이 다르다 — Claude Code는 `CLAUDE.md`와 slash command로 재주입, Codex는 세션을 짧게 끊는 편이 낫다.

그리고 **토큰 4×**. 이 숫자는 입에 올리기 좋지만 맥락을 뺀 채 인용하면 오해를 부른다.

> **Contrarian Signal — 토큰 4× 갭의 진짜 원인**
>
> "Claude Code가 Codex보다 토큰을 4배 쓴다"의 출처는 Builder.io Figma→Code 벤치 1건(6.2M vs 1.5M). **이 4×는 "더 똑똑해서 더 많이 생각하기 때문"이 아니다.** 원인은 단순하다 — Claude Code는 **extended thinking이 기본 on**이고 Codex는 기본 off다. Extended thinking은 내부 추론 트레이스를 생성하며 이 출력 토큰이 과금된다.
>
> `MAX_THINKING_TOKENS=8000` 상한을 걸거나 `/effort low`로 낮추면 토큰 소비가 급감한다. velog @justn-hyeok의 진단대로 `CLAUDE_CODE_EFFORT_LEVEL=high`와 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`을 뒤집으면 도구의 "성격" 자체가 달라진다. 4×는 **도구의 본성이 아니라 기본값의 산물**이다.
>
> 벤치 자체의 한계도 기억해두자. N=1, Figma→Code는 UI 변환 편향이 강하다. 리팩토링·마이그레이션 같은 반복형 태스크에서는 갭이 좁혀진다는 사례 보고가 잇따른다. "4×"는 슬로건이 되기 좋지만 슬로건은 설계 결정의 근거가 못 된다. 자기 태스크 분포로 직접 재보는 편이 낫다.

## 그 밖의 도구들은 어느 자리에 서는가

CLI 2파전으로 보이지만 실제 팀은 IDE·플러그인을 섞어 쓴다. 포지셔닝만 짧게 정리해두자.

**Cursor**는 IDE 중심이다. 규칙은 `.cursor/rules/*.mdc`(메타데이터+본문 MDC 포맷)로 관리하며 path glob로 스코프를 나눈다. 프런트엔드·디자인 시스템에 잘 맞는다. 한 가지 주의 — MCP 도구가 40개를 넘으면 **조용히 truncate**된다(silent cap). 이 사례는 3장에서 컨텍스트 오염 반증으로 다시 등장한다. 이미 팀에 깔려 있다면 이탈 비용이 크니 굳이 옮길 이유가 없다.

**Aider**는 오픈소스 CLI다. `CONVENTIONS.md`를 `--read`로 자동 주입하고, **Architect/Editor 모드**로 강한 모델이 설계·빠른 모델이 편집하는 이원화가 특징이다. Auto-commit 기본 on으로 롤백 포인트가 자연스럽게 쌓인다. 온프레미스·오프라인·규제 산업에서 Claude Code·Codex가 원천 차단될 때 **사실상 유일한 선택지**다.

**Cline**은 VS Code 플러그인이다. **Focus Chain**(6 메시지마다 todo 재주입)·`new_task`(50% 초과 시 핸드오프)·Memory Bank 패턴을 내장하며 "Cline 50% 규칙"의 원천 — 3장 중심 소재다. **Continue/Windsurf**는 `.windsurfrules` 같은 경량 규칙 파일을 쓰는 플러그인·IDE 변형군.

언제 무엇을? **IDE 통합 우선이면 Cursor**, **OSS·온프레 강제면 Aider**, **VS Code 안에서 끝내면 Cline**, **훅·서브에이전트·관측성이면 Claude Code**, **OS-sandbox·비동기 자율성이면 Codex**.

## 도구 선택 의사결정 플로우차트

```
               ┌─ 분기 0 ─┐
               │ OSS/온프레│
               │ 강제?    │
               └────┬────┘
            Yes ────┼──── No
            ▼              ▼
        [Aider]      ┌─ 분기 1 ─┐
                     │Cursor/VSC│
                     │딥인티드? │
                     └────┬────┘
                  Yes ────┼──── No
                  ▼              ▼
           [Cursor/Cline]   ┌─ 분기 2 ─┐
                            │훅·서브에 │
                            │이전트?   │
                            └────┬────┘
                         Yes ────┼──── No
                         ▼              ▼
                  [Claude Code]    ┌─ 분기 3 ─┐
                                   │OS-sandbox│
                                   │·비동기?  │
                                   └────┬────┘
                                Yes ────┼──── No
                                ▼              ▼
                          [Codex CLI]    [Claude Code 기본]
```

**분기의 순서**가 핵심이다. 첫 분기점은 기능이 아니라 거버넌스·라이선스 제약, 두 번째는 기존 툴체인 이탈 비용, 그다음이 기능·자율성. 현실에서 결정을 좌우하는 건 기능이 아니라 그 앞의 제약이다. 거꾸로 쓰지 말자.

## GitHub Issue #42796 — 공식 changelog보다 이슈가 먼저 말한다

2026년 2월, Claude Code 커뮤니티에 "뭔가 이상하다"는 신호가 올라왔다. 공식 changelog엔 별일 없다. 그런데 파워 유저 `stellaraccident`가 GitHub Issue anthropic/claude-code#42796에 **측정된 수치**를 얹는다 — edit당 file read 70% 감소, 17일간 premature stop 173건(이전 0), 사용자 인터럽트 12배, 전체 파일 rewrite 비중 2배. Anthropic 스태프가 보고의 유효성을 인정한다.

여기서 배울 건 **운영 지능(operational intelligence)이 공식 changelog가 아니라 GitHub issue에 먼저 쌓인다**는 것이다. 벤더 문서는 릴리스 노트의 시차만큼 뒤진다. 도구를 고른다는 건 이슈 트래커를 **주간으로 훑을 팀 루틴**을 함께 고르는 일이며 — Claude Code면 `anthropics/claude-code` 이슈, Codex면 OpenAI 공지·포럼 — 공짜가 아니다.

## 실습과 체크포인트

메커니즘을 머리로만 정리하는 건 난감하다. 두 번의 실습으로 감각을 붙이자.

**실습 1 `[본격 2시간]` — 동일 이슈, 두 도구 병렬 해결**
- 필요 도구: 본인 레포, Claude Code v2.1+, Codex CLI 최신 안정판, 스톱워치, 단위테스트 스위트.
- 절차: 백로그에서 중간 난이도 이슈 1개를 고른다(2시간 내 완결 가능한 것). 같은 이슈를 `feat/claude-attempt` 브랜치에서 Claude Code로, `feat/codex-attempt`에서 Codex CLI로 각각 해결한다. 두 세션 모두 기본값을 건드리지 않는다 — 첫 측정을 왜곡하지 않기 위해서.
- 기록할 수치: (1) `git diff --stat` 라인, (2) 세션 토큰(Claude는 `/cost`, Codex는 세션 로그), (3) 벽시계 시간, (4) 테스트 통과 여부, (5) 사람이 개입한 횟수.
- 산출물: `decisions/tool-choice.md`에 5개 수치 + 주관적 후기 3줄 + 재현 주의점 2줄을 커밋.
- 주의: 1회 실행으로 결론 내지 말자. Kapoor et al. (2024, arXiv:2407.01502) "AI Agents That Matter"는 현 agent 벤치들이 비용 분포를 가린 채 단일 숫자로 성능을 주장한다고 비판한다 — 우리의 1회 측정도 같은 함정에 빠지기 쉽다.

**실습 2 `[읽기 15분]` — `MAX_THINKING_TOKENS` 시연**
- 필요 도구: Claude Code, 짧은 태스크 1개(예: "README.md 목차 정비").
- 절차: 같은 태스크를 (a) 기본값, (b) `MAX_THINKING_TOKENS=8000` 환경변수 지정 상태에서 각 1회 실행. 직후 `/cost`로 세션 토큰을 확인·비교한다. 정책화·팀 표준화는 10장(거버넌스)에서 다룰 테니 여기선 **감각만** 확인하면 된다.
- 산출물: `decisions/tool-choice.md` 말미에 "thinking cap 감각" 항목 3줄 메모.
- 주의: 이 실습은 도구 선택을 뒤집기 위한 게 아니라 "4× 갭의 원인은 기본값"이라는 Contrarian Signal을 **몸으로 확인**하기 위한 것이다.

**체크포인트 두 가지.** 첫째, **도구 선택 근거 1페이지**. 어느 분기점에서 왜 어느 쪽을 택했는지, 거버넌스·툴체인·기능·자율성 4축에 각 1~2줄로 정당화한다. "그냥 써봤더니 좋았다"가 아니라 분기점을 명시해야 6개월 뒤 재검토가 가능하다. 둘째, **월 토큰 예산 추정치**. 팀 인원 × 1인당 일일 세션 수 × 세션당 평균 토큰(실습 1 수치) × 주당 개발일 × 4주. 엉성해도 숫자가 있어야 예산이다.

2장은 두 도구의 내부 장치를 풀어헤쳤다 — `CLAUDE.md` 상향 병합, 서브에이전트 `isolation: worktree`, 27종 훅과 `permissionDecision:'deny'` 강제력, MCP 명명, 설정 스코프. 반대편엔 샌드박스 3모드·approval 4종·OS-enforced Seatbelt/Landlock. 발산 지점 표로 토큰 4× 갭의 진짜 원인을 분리했고, Cursor·Aider·Cline·Continue의 자리를 잡은 뒤 의사결정을 4단 플로우차트로 정리했다.

그런데 이 모든 설명이 성립하려면 **컨텍스트가 제대로 관리된다**는 전제가 필요하다. 60줄 권장은 왜 나왔는가? "가장 가까운 `AGENTS.md`가 이긴다"는 조율 규칙은 어떻게 설계하는가? 200k 윈도우인데 왜 100k부터 품질이 꺾이는가? 3장 "컨텍스트가 99%다"의 질문들이다. 도구를 골랐다면 이제 도구의 **입력**을 설계할 차례다.

---

### 학술 레퍼런스

- Kapoor, S., et al. (Princeton, 2024). AI Agents That Matter. arXiv:2407.01502. https://arxiv.org/abs/2407.01502 — 현 agent 벤치가 비용 분포를 가린 채 단일 숫자로 성능을 주장한다는 비판. 2장에서는 Builder.io 4× 측정을 과잉 일반화하지 말라는 근거로 인용.

### 1차 자료

- [Anthropic, Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide) (접속 2026-04-20)
- [Anthropic, Claude Code Memory](https://code.claude.com/docs/en/memory) (접속 2026-04-20)
- [Anthropic, Claude Code Sub-agents](https://code.claude.com/docs/en/sub-agents) (접속 2026-04-20)
- [Anthropic, Claude Code Skills](https://code.claude.com/docs/en/skills) (접속 2026-04-20)
- [Anthropic, Claude Code Settings](https://code.claude.com/docs/en/settings) (접속 2026-04-20)
- [Anthropic, Claude Code Sandboxing](https://code.claude.com/docs/en/sandboxing) (접속 2026-04-20)
- [OpenAI, Codex AGENTS.md Guide](https://developers.openai.com/codex/guides/agents-md) (접속 2026-04-20)
- [OpenAI, Codex Agent Approvals & Security](https://developers.openai.com/codex/agent-approvals-security) (접속 2026-04-20)
- [OpenAI, Codex Security](https://developers.openai.com/codex/security) (접속 2026-04-20)

### 2차 자료 / 벤치

- [Builder.io, "Codex vs Claude Code"](https://www.builder.io/blog/codex-vs-claude-code) — Figma→Code 벤치 6.2M vs 1.5M. N=1 한계 명시.
- [thoughts.jock.pl, "AI Coding Harness Agents 2026"](https://thoughts.jock.pl/p/ai-coding-harness-agents-2026)
- [velog @justn-hyeok, "Claude Code adaptive thinking 끄기"](https://velog.io/@justn-hyeok/off-claude-code-adaptive-thinking) — `CLAUDE_CODE_EFFORT_LEVEL`·`CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` 환경변수 우회의 한국어 1차 진단.

### 운영 지능

- GitHub Issue anthropic/claude-code#42796 — Feb 2026 regression. https://github.com/anthropics/claude-code/issues/42796
- GitHub Issue anthropic/claude-code#38335 — Max plan 세션 한도 소진. https://github.com/anthropics/claude-code/issues/38335
- GitHub Issue anthropic/claude-code#10065 — 단일 프롬프트 주간 한도 10% 소비. https://github.com/anthropics/claude-code/issues/10065
