# 리서치 종합: Claude Code 하네스 엔지니어링

> 본 문서는 5–10명 팀의 테크리드/시니어/플랫폼 엔지니어를 위한 책 "Claude Code를 활용한 Harness Engineering"의 토대 자료다. 입문 콘텐츠는 의도적으로 배제하고, **팀 단위 운영·설계·거버넌스**에 무게중심을 둔다. 인용 옆 [W#] = 웹, [P#] = 논문, [C#] = 커뮤니티.

---

## 1. 개념 및 정의

### 1.1 Harness Engineering — 정의 비교

여러 출처가 "**Agent = Model + Harness**"라는 동일한 등식을 반복한다. 즉 모델 자체를 제외한 **모든 것**(루프, 도구, 컨텍스트 관리, 메모리, 가드레일, 추적)이 하네스다 [W2, W7, W8]. Anthropic 자체도 "Claude는 자신의 하네스에 맞춰 사후 학습(post-trained)되었다"고 인정한다 [W1, W2].

세 가지 외연을 구분해 쓰는 것이 유용하다:

| 용어 | 범위 | 시점 | 주된 관심사 |
|---|---|---|---|
| Prompt Engineering | 한 번의 입력 | 호출 시점 | 모델이 받을 한 문장의 품질 |
| Context Engineering | 컨텍스트 윈도 | 세션 단위 | "모델이 무엇을 보는가" 관리 |
| Harness Engineering | 모델 외 모든 것 | 시스템 단위 | 도구·권한·메모리·관측·오케스트레이션 |
| Scaffolding | 첫 호출 *전* 구성 | 부팅 시점 | 시스템 프롬프트, 도구 스키마, 서브에이전트 등록 |

(Adnan Masood, Avi Chawla, Madplay 정리 [W6, W17, W19, W21])
> "Prompt engineering is a subset of context engineering. Context engineering is a subset of harness engineering. Each layer builds on the one before it." [W17]

Martin Fowler는 같은 개념을 **사이버네틱 모델**(피드포워드/피드백)로 재정의한다 [W4]:
- **Guides (피드포워드):** 행동 *전* 안내 — 시스템 프롬프트, 코드 검색, 스킬, 문서
- **Sensors (피드백):** 행동 *후* 관찰 — 린터, 테스트, 리뷰 에이전트
- 사람은 그 사이에서 하네스를 진화시키는 **steerer** 역할

대안 프레이밍: Avi Chawla는 OODA(Observe-Orient-Decide-Act) 루프 중 LLM이 실제로 강한 부분은 Decide뿐이고 나머지 셋은 하네스의 영역이라고 본다 [W20].

### 1.2 왜 지금 Harness가 중요한가

- **Skill Issue 가설** (HumanLayer): "더 좋은 모델(GPT-6)을 기다리는 것은 핵심을 빗나간다. 모델이 좋아질수록 새 문제에서 새로운 방식으로 실패한다." [W1]
- **모델은 자신의 하네스에 과적합된다.** Opus 4.6은 Claude Code 안에서 Terminal-Bench 33위, 다른 하네스에선 5위 [W1]. 동일 Opus 모델이 Claude Code에선 77%, Cursor에선 93% (Matt Mayer 독립 테스트) — **하네스 한 끗 차이로 16%p 격차** [W23].
- **수렴 명제(convergence thesis):** "최상위 코딩 에이전트들은 모델이 다르더라도 서로 닮아간다. 차별점이 모델에서 하네스로 옮겨가고 있기 때문이다." [W7]
- **98.4% 하네스 가설 (논문):** Liu et al.이 Claude Code TypeScript 소스를 분석한 결과 "프로덕션 에이전트 코드의 98.4%는 운영 인프라이고 1.6%만이 AI 의사결정 로직"이다 [P1, W26].

### 1.3 한 줄 요약

> "하네스 엔지니어링이란, AI 코딩 에이전트를 팀의 일관된 생산성 도구로 길들이기 위해, Command·Hook·Subagent·Skill·CLAUDE.md·settings.json·MCP를 의도적으로 설계·공유·진화시키는 메타-엔지니어링 활동이다."

---

## 2. Claude Code 빌딩블록과 팀 활용 패턴

### 2.1 7개 빌딩블록 한눈 비교

| 블록 | 목적 | 팀 공유 방식 | 강도 |
|---|---|---|---|
| **CLAUDE.md** | 프로젝트 상시 컨텍스트 | git에 체크인 | 권고적 (~80% 준수) [W14] |
| **settings.json** | 권한/훅/환경 설정 | `.claude/settings.json` git 체크인 | 강제적 |
| **Hooks** | 라이프사이클 결정적 자동화 | settings.json에 정의 | 강제적 (100% 실행) [W14] |
| **Slash Commands** | 자주 쓰는 작업 단축 | `.claude/commands/` 또는 `.claude/skills/` | 호출 시 실행 |
| **Skills** | 점진적 공개 가능한 도메인 지식 | `.claude/skills/` git 체크인 | 필요할 때 자동 로드 [W12, W27] |
| **Subagents** | 컨텍스트 격리·전문화 | `.claude/agents/` git 체크인 | 호출 시 격리 실행 |
| **MCP** | 외부 시스템 게이트웨이 | `.mcp.json` git 체크인 | 보안·인증 경계 |

### 2.2 12개 핵심 하네스 패턴 (Generative Programmer가 leak 분석한 결과 [W23])

**메모리/컨텍스트:**
1. **Persistent Instruction File** — 매 세션 자동 로드되는 CLAUDE.md
2. **Scoped Context Assembly** — 조직/사용자/프로젝트/하위디렉토리 계층적 로딩
3. **Tiered Memory** — 200줄 인덱스 + 주제별 파일 + 전체 트랜스크립트 검색
4. **Dream Consolidation** — 유휴 시간 메모리 정리 (autoDream 8단계)
5. **Progressive Context Compaction** — HISTORY_SNIP / Microcompact / CONTEXT_COLLAPSE / Autocompact 4단계 압축

**워크플로/오케스트레이션:**
6. **Explore-Plan-Act Loop** — 권한이 단계별로 늘어나는 3단계 루프
7. **Context-Isolated Subagents** — 리서치 에이전트는 편집 불가, 플래닝 에이전트는 실행 불가
8. **Fork-Join Parallelism** — git worktree 병렬 + 캐시 컨텍스트 재사용

**도구/권한:**
9. **Progressive Tool Expansion** — 기본 20개 미만, 필요 시 활성화
10. **Command Risk Classification** — ML 분류기로 위험도 판정 후 자동 승인/차단
11. **Single-Purpose Tool Design** — FileReadTool, FileEditTool 등 좁은 스코프

**자동화:**
12. **Deterministic Lifecycle Hooks** — 25+ 훅 포인트, 프롬프트 밖에서 실행

### 2.3 팀 공유 운용 원칙

- **계층적 settings 병합:** Managed(조직) > Project > User > Personal. 배열 값은 모든 스코프에서 합쳐진다 [W4-실제로는 W1-blakecrosley 등].
- **`.claude/settings.json` = 팀, `.claude/settings.local.json` = 개인** — gitignore에 두 번째만 [W4].
- **CLAUDE.md vs Hook 결정 규칙:** "CLAUDE.md is the suggestion, Hooks is the requirement" — 매 번 반드시 해야 할 것은 hook으로 [C2-팁38].
- **Linter 작업은 hook으로, 도메인 지식은 CLAUDE.md로:** "LLM은 linter보다 비싸다. Hook으로 결정성 확보하면 instruction budget을 사람만이 가르칠 수 있는 것에 쓸 수 있다." [W4]
- **Skills 지정 위치:** Project skills는 `.claude/skills/` (팀 공유), 글로벌은 `~/.claude/skills/`. Skill은 Claude.ai/Code/API 모두에서 같은 정의로 동작 [W27].
- **Plugin Marketplace로 패키징해 사내 배포:** Team/Enterprise 플랜에서는 사설 GitHub repo를 marketplace로 두고 자동 설치 가능 [W28].

### 2.4 Subagent vs Skill — 언제 어느 것을 쓰나

커뮤니티의 대표 분기 기준 [W24, C3]:

- **Skill = "WHAT to do"** — 도메인 지식·절차의 점진적 공개. 메타데이터만 시스템 프롬프트에 노출, 본문은 매칭 시 로드 [W27].
- **Subagent = "WHO does it"** — 컨텍스트 격리가 필요할 때. 메인 컨텍스트를 깨끗이 유지하기 위함.

Shrivu Shankar는 **반대 입장**도 제시한다: "커스텀 서브에이전트는 brittle한 해법이다. 메인 에이전트에게 컨텍스트(CLAUDE.md)를 주고 자체 Task() 기능으로 위임시키는 것이 낫다." [W30] → **논쟁점**(섹션 8 참조).

---

## 3. 핵심 운영 주제

### 3.1 안전과 권한

#### 3.1.1 7-mode 권한 시스템 + ML 분류기

Claude Code는 7가지 권한 모드를 ML 분류기와 결합해 명령 위험도를 자동 판단한다 [P1, W26]. PreToolUse hook이 **유일하게 차단할 수 있는 훅**이며, exit code 2를 리턴해야 실제로 차단된다 [W14].

#### 3.1.2 위험 명령 차단 패턴

```
PreToolUse → matcher: "Bash"
           → 정규식 검사: rm -rf, git push --force, DROP TABLE …
           → 매칭 시 exit 2 → 차단
```

`rm -rf`, `git push --force`, `drop table` 패턴은 거의 모든 가이드가 공통으로 차단 대상으로 든다 [W14, C2-팁40, W7].

#### 3.1.3 Permission 계층

- `/permissions`로 신뢰 명령어 화이트리스트 등록 (반복 승인 프롬프트 제거) [C2-팁33]
- `/sandbox`로 OS 수준 격리: 쓰기는 프로젝트 한정, 네트워크는 화이트리스트 도메인만 [C2-팁34]
- "인증·결제·데이터 뮤테이션은 *반드시* 사람 검토" — 자동화 테스트가 모든 것을 잡지 못한다 [C2-팁42]

#### 3.1.4 Prompt Injection — 실제 사고

> 한 보안 연구자가 PR 제목에 악의적 지시를 넣어 PR을 열자, **Claude Code Security Review GitHub Action이 자기 API 키를 코멘트로 게시**했다. Anthropic은 이를 CVSS 9.4 Critical로 분류했고, 시스템 카드는 이미 "이 액션은 prompt injection에 hardened되지 않았다"고 명시하고 있었다 [W15].

논문의 분류: 코딩 에이전트 prompt injection의 근본 원인은 **LLM이 instruction과 data를 신뢰성 있게 구분하지 못한다는 것** [P2: arXiv 2601.17548].

방어 권고:
- **Meta의 "Rule of Two":** 에이전트가 (1) 신뢰 못하는 입력 처리, (2) 민감 데이터 접근, (3) 강력한 능력 — 셋 중 둘 이상을 동시에 갖지 말 것 [P3: arXiv 2510.05244]
- **CaMeL 프레임워크:** 제어 흐름과 자연어 입력을 형식적으로 분리 [W15-OWASP]
- GitHub Action 보안 강화: `permissions:` 키로 GITHUB_TOKEN 스코프 제한, environment protection rule, first-time-contributor 게이트 [W15]

#### 3.1.5 시크릿 보호 — Gateway 패턴

Kong AI Gateway 가이드가 정리한 **무거버넌스 롤아웃의 4대 위험** [W11]:
1. 비용 폭주
2. 민감 데이터(소스코드·API키·설정) 무방비 송신
3. 감사 추적 부재 (규제 산업)
4. 그림자 AI 확산 — 팀별 다른 보안 관행

Gateway 도입 효과:
- 개발자 개인이 API 키 보유하지 않음 (`ANTHROPIC_BASE_URL=http://localhost:8000/anything claude` [W11])
- 팀 단위 토큰 쿼터, PII 살균, 세맨틱 가드레일
- Kong File Log plugin으로 모든 요청·응답 메타데이터 캡처

### 3.2 워크플로 자동화 — PR·테스트·배포·시큐리티 게이트

#### 3.2.1 PR 게이트로서 GHA + Claude

Anthropic 공식 `claude-code-action`과 `claude-code-security-review`가 표준 출발점 [W31]:
- 변경 파일에 대해 prompt injection, SQL injection, XSS, auth bypass, OWASP Top 10 검사
- diff-aware 스캔, 인라인 코멘트, 패턴 매칭이 아닌 의미 이해
- 비용: PR당 $0.04 — 하루 20 PR이면 월 $24 (개발자 1시간 미만) [W31]

타이밍 옵션: PR 오픈 시 1회 vs 매 push마다 — 후자는 자동 resolve도 됨 [W31].

#### 3.2.2 PR 정책 변화 사례

Shrivu Shankar는 **"인간 prompter가 없는 PR(고객 요청 → 자동 처리)은 최소 2명 승인"**으로 정책을 정했다고 보고 [W30]. AI가 만든 PR을 어떻게 검토할지에 대한 거버넌스 질문이 새로 생긴다.

#### 3.2.3 PostToolUse Hook으로 자동 포매팅

```
matcher: "Edit|Write"
command: "prettier --write $file || true"
```
- 모델 출력 품질에 의존하지 않고 결정적 normalize
- `||true`로 실패가 에이전트를 차단하지 않게 [C2-팁39]

#### 3.2.4 Pre-commit 게이트 — Block-at-submit 전략

Shankar의 핵심 주장: **"plan 도중에 막으면 에이전트가 혼란/좌절한다. 끝까지 일하게 하고 commit 단계에서 결과만 검사하라."** [W30]
- `Bash(git commit)` 래핑 → `/tmp/agent-pre-commit-pass` 파일이 있을 때만 통과
- 이 파일은 테스트 통과 시에만 생성 → 자동 fix 루프 강제

#### 3.2.5 PR-from-anywhere 패턴

Slack/Jira/CloudWatch alert에서 트리거 → Claude Code SDK로 분기 → 테스트된 PR 반환. 회사 전체 GHA 로그를 정기적으로 분석해 자주 막히는 지점을 CLAUDE.md/CLI에 반영 [W30]:
> "Query logs since 5 days ago; identify what agents got stuck on; fix issues; submit PR."

### 3.3 멀티 에이전트 오케스트레이션

#### 3.3.1 Generator-Verifier (Generator-Critic) 패턴

학계와 실무 모두 같은 결론으로 수렴: **생성과 검증을 같은 에이전트에 맡기지 말라.** [W3, W22, P4]

- AgentForge (arXiv 2604.13120): Planner / Coder / Tester / Debugger / Critic 5개 + 듀얼 메모리 → SWE-bench Lite 40.0%, 단일 에이전트 대비 +26~28pt [P4]
- Multi-agent decision support: 단일 에이전트 1.7% 대비 100% actionable 추천률 (80배 / 140배 향상) [W22]

#### 3.3.2 Reflexion 계보 (학계)

- **ReAct** (Yao 2023): Reason-Act-Observe loop의 표준
- **Reflexion** (Shinn et al., arXiv 2303.11366): 실패 후 verbal self-reflection → episodic memory에 저장 → 다음 시도에 condition. 그래디언트 업데이트 없는 "verbal RL" [P5]
- **Voyager** (Wang et al.): automatic curriculum + iterative prompting + skill library — Minecraft에서 평생학습 시연. **Skill 개념의 학술적 원형** [P6]
- 후속: Self-Refine, CRITIC, Chain-of-Verification — 모두 같은 generate→critique→refine 루프의 변형 [P7: arXiv 2509.02547 survey]

#### 3.3.3 Anthropic의 장기 작업 패턴 — Initializer + Coder 분리

[W2: "Effective harnesses for long-running agents"] 핵심:

장시간 에이전트의 두 실패 모드:
1. **Over-ambition** — 한 번에 앱 전체 만들기 시도 → 컨텍스트 소진 → 미완성
2. **Premature completion** — 다음 인스턴스가 "이미 끝났네"로 오판

해법은 **두 가지 다른 프롬프트**:
- **Initializer Agent (1회)** — `init.sh`, `claude-progress.txt`, JSON feature list, 첫 git commit 만들기
- **Coding Agent (반복)** — 진행 파일·git 로그 읽고 → 1개 feature 골라 → 깨끗한 상태로 commit
> "Inspiration for these practices came from knowing what effective software engineers do every day." [W2]

테스트 강제 문구 예시:
> "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality." [W2]

#### 3.3.4 Fork-Join: git worktree 병렬

`claude --worktree feature-auth` → 격리 디렉토리 + 전용 브랜치 + 독립 파일 시스템. 3~5개 동시 실행 권장 [C2-팁15, W26].

> "버그 보고서 9시 → 4개 탭 병렬 작업 (버그 수정·PR 리뷰·changelog·배경 조사) 9:20 → 11시까지 PR 자동 생성 → 11:30에 사람이 최종 리뷰" — 한 한국 개발자가 GeekNews에 공유한 오전 2시간 사례 [C1]

서브에이전트도 worktree 격리 가능: `isolation: worktree` 프론트매터 [C2-팁35].

#### 3.3.5 Agent Teams (실험적 기능)

`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 활성화 시 팀 리더가 팀원에게 작업 분배. 같은 파일 수정 시 충돌 회피 [C2-팁20]. **단점: 표준 세션의 약 7배 토큰 소비** (각 teammate가 자기 컨텍스트 윈도와 별도 인스턴스를 유지하기 때문) [W18].

### 3.4 관측가능성과 비용 통제

#### 3.4.1 OpenTelemetry 공식 지원

`CLAUDE_CODE_ENABLE_TELEMETRY=1` + 적어도 하나의 exporter 설정 → 3개 시그널 독립 export [W18]:
- traces (W3C trace context 자동 propagation)
- metrics
- events

서브에이전트가 Task tool로 spawn 되면 `llm_request`/`tool` span이 부모 `claude_code.tool` span 아래에 nest되어 **전체 위임 체인이 한 trace로 보인다** [W18].

호환 백엔드: SigNoz, Dynatrace, Grafana Cloud, Honeycomb, Datadog, Sentry, Logfire (claudia wrapper 사용 시) [W18].

#### 3.4.2 비용 실데이터

- **엔터프라이즈 평균:** $13/개발자/active day, $150–250/월 (90%는 active day당 $30 미만) [W13]
- **Latent Space 인터뷰:** Cursor $20/월 vs Claude Code 평균 $6/일 (≈ $180/월) [W32]
- **Agent Teams는 ~7배:** 각 팀원이 별도 인스턴스 [W18]
- **2명 팀이 월 $400으로 대규모 팀 산출물 달성** — 한국 개발자 인용 [C1]

#### 3.4.3 비용 절감 전략

- `MAX_THINKING_TOKENS=8000`로 thinking 예산 축소, 또는 `/effort low` [W13]
- "ultrathink" 키워드는 어려운 문제에만 [C2-팁7]
- 프롬프트 캐싱 적극 활용 — Bifrost 같은 게이트웨이가 캐시 효율 별도 측정 [W13]
- Branch8의 사례: token budget script + 캐싱으로 **70% 비용 절감** [W13]
- `/clear`는 무료, 컴팩션은 비싸고 노이즈 — 무관한 작업 사이엔 무조건 `/clear` [C2-팁12, W30]

#### 3.4.4 거버넌스 캡 (gateway 패턴)

Bifrost / Kong / Maxim 공통 패턴 [W13]:
- 개발자별 일일 한도, 팀별 월 예산, 조직 전체 캡 (각각 독립 작동)
- 예산 소진 시 자동 차단 (인보이스 닿기 전)
- Prometheus 메트릭, OTLP, Datadog 커넥터로 통합

### 3.5 도메인 지식의 코드화

#### 3.5.1 CLAUDE.md 디시플린

Addy Osmani의 가이드 [W7]:
- **60줄 미만 유지** — pilot's checklist이지 style guide가 아니다
- 모든 룰은 **과거의 실제 실패에서 유래**해야 한다
- "Litmus test for every line: 이 줄 없으면 Claude가 실수할까?" — 약 150~200줄이 한도 [C2-팁29]

Shankar의 추가 원칙 [W30]:
- 문서의 *내용*을 박지 말고 *언제·왜* 읽으라고 알리기: "For complex usage or if you encounter FooBarError, see path/to/docs.md"
- 부정형보다 대안: "Never use --foo-bar" 대신 "Prefer --baz-qux"
- "30%+ 엔지니어가 쓰는 도구만 문서화" — token budget 배분
- Monorepo 기준 baseline ~20k 토큰, 작업용으로 ~180k 남김

#### 3.5.2 Self-Updating CLAUDE.md

Claude가 실수하면 즉석에서: **"CLAUDE.md를 업데이트해서 이 실수가 반복되지 않게 해."** Claude가 자체 룰을 작성 → 다음 세션부터 자동 준수 [C2-팁30]. 살아있는 문서 패턴.

#### 3.5.3 Conditional Rules

`.claude/rules/` 디렉토리 + frontmatter `paths:` 패턴 → 특정 파일 패턴에서만 로드 [C2-팁31]. CLAUDE.md를 가볍게 유지하면서 도메인별 깊이 확보.

#### 3.5.4 Skill로 절차적 지식 패키징

Anthropic 공식 정의 [W27]:
> "Building a skill for an agent is like putting together an onboarding guide for a new hire."

3-tier progressive disclosure:
1. **메타데이터:** SKILL.md frontmatter만 시스템 프롬프트에 (수십 토큰)
2. **본문:** 매칭 시 SKILL.md 전체 로드
3. **번들:** 필요 시 보조 파일 로드

> "Cambrian explosion in Skills" — Simon Willison: "Claude Skills are awesome, maybe a bigger deal than MCP." [W25]

Skill의 호환성: Codex CLI, Gemini CLI 등 다른 도구도 같은 폴더를 가리킬 수 있다 [W25].

#### 3.5.5 The Ratchet Pattern (Osmani)

> "Each agent mistake becomes a permanent constraint. When an agent ships commented-out tests, add a rule; add a pre-commit hook; flag it in the reviewer subagent." [W7]

**팀 암묵지 → 명시화의 단방향 톱니바퀴**가 하네스의 본질.

---

## 4. 팀 도입과 거버넌스

### 4.1 시니어/주니어 격차 — 양면

**가속 측:** "더 많이 알수록 AI가 더 가속한다. 덜 알수록 AI가 더 묻는다(buries you)." [W33]
- AI 코딩 도구의 26~55% 생산성 향상은 **검토할 수 있는 능력**에 의존 [W33]
- 시니어는 3배 빨라진다. 그렇다면 회사가 같은 수의 주니어를 뽑아야 하나? — 미국 주니어 채용 30% 감소(2022 대비) [W33]

**위험 측:**
- 코딩 에이전트는 서브한 이슈(불필요한 추상화, 중복 로직, 일관성 없는 네이밍, 엣지 케이스 누락)를 잘 못 본다 [W33]
- "96%의 개발자가 AI 코드를 완전히 신뢰하지 않지만, 실제로 검증하는 비율은 48%" — **검증 격차** [W33]
- 시니어가 *자기 코드 보듯* 검토하면 놓치고, *유능한 동료의 코드처럼* 검토하면 잡는다 [W33]

GeekNews 6주차 후기: **"경험 많은 주니어+ 급 페어 프로그래머"** — Claude Code는 시니어 감독이 필요한 빠른 주니어 [C4].
> "주니어 개발자가 이해도 없이 PR 올리는 사례가 늘었다." [C4]

### 4.2 변화관리 — Toss/올리브영 패턴

[W34: CIO 한국] 사례:
- **Toss:** 톱다운 도입 대신 **AI Evangelist 모델** — 약 10명을 evangelist로 지명, 본업 + AI 전파. Slack에 누적된 conversational 데이터를 AI 온보딩에 활용.
- **올리브영:** 단일 벤더 락인 회피, 개발자 1인당 AI 예산 → 도구 자율 선택. 사내 표준 점수화 코드리뷰 시스템을 **"코치"로 포지셔닝**(평가자 아님)해 감정적 마찰 감소.
- 공통: experimentation culture, empowerment with budgets, **psychological safety enabling failure discussion** 세 가지를 성공 요인으로 꼽음.

### 4.3 IMWEB 인프라팀 사례 (한국)

GeekNews에 정리된 5명 팀 사례 [C5]:
- **읽기/쓰기 권한 명확 분리, 승인 정책 철저, 한 번에 하나씩 검증**으로 보수적 접근
- 결과: 팀 전체 자발적 사용, "새벽 3시에 안 깨도 된다", **생산성 10배 평가**
- 마이그레이션·리팩토링·기술 부채 해소를 6주 내 병행 완료 [C6]

### 4.4 5인 팀처럼 운영하기 — GeekNews 패턴 [C1]

병렬 인스턴스 + 사람은 **"오케스트라 지휘자"** 역할:
- `/issues` → GitHub 이슈 자동 생성
- `/work` → 이슈 기반 개발 + PR 생성
- `/review` → PR 리뷰·개선
- 사람: UX/코드 스타일 최종 검토 (11:30 회의)

### 4.5 HCI/SE 학계 — 채택 연구 정리

- **경험 수준이 채택률은 예측하지 않으나, 멘탈 모델은 결정한다** [P8: arXiv 2504.13903]
  - 시니어: AI를 "주니어 동료" 또는 "콘텐츠 생성기"로
  - 주니어: AI를 "선생님"으로
- **자기보고 생산성 vs 측정 생산성 격차:** 개발자는 일관되게 큰 향상을 보고하지만, 실측은 더 modest [P9: arXiv 2503.06195 systematic review]
- **PR에 AI 흔적 남기기 거부감:** 일부 응답자는 "PR에 AI 코드처럼 보이면 평가에 부정적"으로 우려. 조직 리더가 **"AI 사용은 받아들여진다"는 문화**를 만들어야 한다 [P10: ACM 3706599.3706670 enterprise study]
- Anthropic + Toss + 올리브영 한국 라운드테이블 공통 결론: **"무엇을 더 만들까?"가 아니라 "어떤 일이 사라져도 되는가?"** [W34]

### 4.6 Plugin Marketplace — 사내 표준 배포

Team/Enterprise 플랜은 사설 marketplace 가능 [W28]:
- 조직 marketplace는 private/internal repo만 (public 금지)
- per-user provisioning, auto-install
- 팀원이 프로젝트 폴더 trust 시 자동 설치 prompt

---

## 5. 사례 연구

### 5.1 Anthropic 내부

[W29: Anthropic 공식 블로그]:
- **Security Engineering:** 스택 트레이스 + 문서를 Claude에 공급 → control flow 추적. **10–15분 → 3배 빠름.** TDD: pseudocode 요청 → 테스트 작성 → 주기적 체크인. 익숙하지 않은 언어(Rust)로 테스트 번역.
- **Growth Marketing:** CSV 수백 광고 → 두 서브에이전트가 식별/생성 → "수 시간 카피 페이스트 → 배치당 0.5초". Figma 플러그인으로 100개 변형 자동 생성.
- **Data Infrastructure (Kubernetes 장애):** 대시보드 스크린샷 공급 → Claude가 GCP UI 메뉴별로 안내 → pod IP 고갈 식별 → 정확한 명령어 제공. **20분 절약.**
- **Legal:** "phone tree" 라우팅 시스템 프로토타입 — 비개발팀의 첫 자체 도구.

핵심 패턴: "성공적인 팀은 Claude Code를 **code generator가 아니라 thought partner로** 다룬다." [W29]

### 5.2 Notion (Geoffrey Litt)

"Code like a surgeon" 모델 [W26-Litt]:
- 주된 high-leverage 디자인·코딩에 집중
- 부차적 작업(코드베이스 가이드, 탐색 spike, 일상적 TS 수정, 문서)은 백그라운드 에이전트 위임
- malleable software 비전: "AI + local-first가 사용자 agency를 확장한다."

### 5.3 Deriv — 자동 보안 코드 리뷰

[W31: Deriv blog] PR마다 Claude Code GHA가 보안 검토. 인라인 코멘트로 OWASP Top 10 + prompt injection까지 커버.

### 5.4 6주 후기 (GeekNews) [C6]

- React Native 수백 컴포넌트 마이그레이션, RedwoodJS 교체, Jest→Vitest, Node 22 업그레이드 — 모두 6주 안에 병행 완료
- PR/commit 수치는 modest하게 늘었지만 **"주관적 속도와 유연성이 극적으로 향상"**
- "코딩계의 사진술 도입기" — 표현 방식의 패러다임 전환
- "설계/품질/최종 컨트롤은 인간 엔지니어가 담당" — 거버넌스 원칙

### 5.5 Sendbird

엔지니어 인용 [W34]: "에이전트 코딩은 신입이 시니어를 대체하는 도구가 아니라, 시니어가 경험을 더 빠르고 넓게 활용하도록 돕는 도구다."

---

## 6. 안티패턴과 실패담

### 6.1 컨텍스트 측

| 안티패턴 | 증상 | 출처 |
|---|---|---|
| **Auto-compaction 신뢰** | 중요 결정·아키텍처 사라짐 | W30 |
| **`/compact` 남용** | 불투명·에러 발생 → "Document & Clear"로 대체 | W30 |
| **CLAUDE.md 비대화** | 200줄 넘으면 중요 줄 희석 | C2-팁29 |
| **`@`-import로 거대 문서 박기** | 컨텍스트 폭증 | W30 |
| **컨텍스트 마지막 20% 사용** | 멀티파일 작업에서 워킹 메모리 부족 | W36 |
| **연구·플래닝·편집 한 세션** | "Context contamination" — 셋 다 저하 | W36 |

### 6.2 도구 측

- **MCP 서버를 "혹시 모르니" 미리 다 설치** — 도구 설명만으로 컨텍스트 폭증 [W1]
- **MCP를 API 추상화로 오용:** "MCP의 일은 추상화가 아니라 auth/network/security 경계 관리, 그 외엔 비켜라." Shankar는 Jira·AWS·GitHub MCP를 simple CLI로 교체, Playwright만 유지 [W30]
- **LLM-생성 agentfile** — 성능 ~20% 저하 [W1]
- **5분+ 전체 테스트 매 세션 실행** — 작은 부분집합으로 [W1]

### 6.3 자동화 측

- **Plan 도중 차단**: 에이전트가 혼란/좌절. Block-at-submit으로 [W30]
- **Hook이 비결정적/느림** — PostToolUse는 idempotent해야 [W14]
- **인증·결제·DB 변경 자동 머지** — 항상 사람 검토 [C2-팁42]

### 6.4 사람 측

- **AI slop PR**: AI가 만든 코드는 시각 검사 통과 → "intent 공유 없으면 리뷰는 패턴 매칭으로 전락" [W15-AI slop]
- **GitHub의 PR kill switch 검토** (HN 토론): 너무 많은 AI slop이 메인테이너를 매장 [W15]
- **검증 격차 96/48%:** 신뢰 안 한다고 말하면서 검증은 안 함 [W33]
- **Slopsquatting:** AI가 자주 환각하는 패키지명을 공격자가 미리 등록 → 무방비로 install [W15]

### 6.5 비용 측

- **Agent Teams 7× 토큰** — 비용 인지 없이 도입 시 폭주 [W18]
- **개인 한도만으로 충분치 않다** — 게이트웨이 없이는 팀 단위 capping 불가 [W13]
- **Cursor와 Claude Code 동시 결제** — 20% 사용자 trap [W23]

### 6.6 거버넌스 측

- **Cursor + Claude + Codex + Aider 동시 도입** — "shadow AI proliferation": 팀별 다른 보안 관행, 통합 enforcement 불가 [W11]
- **CLAUDE.md를 LLM에게 자동생성** — 성능 저하 [W1]
- **Skill 73%가 60/100 미만 (커뮤니티 214개 audit, 2026)** [W24]
- "Claude still loves to ignore [the skill]" — 호출 신뢰성 이슈 누적 [W24]

---

## 7. 생태계 비교와 미래 전망

### 7.1 도구별 운영상 차이 — 2026 시점 [W23]

| 도구 | 강점 | 약점 | 팀 거버넌스 |
|---|---|---|---|
| **Claude Code** | 멀티스텝 자율, 1M 컨텍스트, SWE-bench 80.8% | 2시간+ 컨텍스트 손실, 토큰 3–4× | Agent Teams, CLAUDE.md, Plugin marketplace, GHA |
| **Codex CLI** | GPT-5.4 코드 품질, 클라우드 컨테이너 | step 3-4 후 일관성 손실, "cold" 느낌 | ChatGPT 구독 통합, AGENTS.md |
| **Cursor** | 최고의 supervised IDE, Composer, Agent Tabs | 무인 자율 작업 부적합 | $40/user/월, Cloud Agents, Design Mode |
| **Aider** | git-first 커밋, 4.2× 토큰 효율, BYOM | pair programmer일 뿐, 오케스트레이터 아님 | open source, 감사추적 우수 |
| **OpenCode** | 75+ 프로바이더 한 인터페이스 | 영구 프로젝트 컨텍스트 부재 | 멀티 프로바이더 |
| **Pi (Anthropic)** | primitives-first, RPC mode | Claude Max 구독 미적용 → 별도 청구 | 커스텀 하네스 빌딩에 적합 |

### 7.2 가격 구조 (10인 팀 기준)

- Cursor Teams: $40/user/월 → **$400/월**
- Claude Code Premium seat: $125/user/월 → **$1,250/월**
- Aider: $0 (모델 비용만)
[W23]

### 7.3 벤치마크 진화

- **SWE-bench Verified:** 정형화된 GitHub issue. Claude Code 80.8%, GPT-5.4 Codex 56.8% (Pro에서) [W23, P11]
- **SWE-Bench Pro (arXiv 2509.16941):** 41 repos × 1,865 problems. enterprise-급 long-horizon 문제. SWE-bench의 contamination 우회 [P11]
- **Terminal-Bench 2.0:** 에이전트 작업에 더 적합. Claude Code 92.1%, Codex CLI 77.3% [W23]
- **AgentBench (Liu et al. 2308.03688):** 8개 환경 [P12]
- **SWE-EVO (arXiv 2512.18470):** software evolution 시나리오 [P13]

### 7.4 1–2년 변화 시그널

- **Anthropic Managed Agents** (2026.04 출시): runtime 분리. 컨테이너 제공 + $0.08/session-hour. Claude.ai/Code/API 동일 skill 호환 [W26-managed]
- **Claude Cowork:** 비-터미널 사용자용 VM 기반 Claude Code. Anthropic이 코딩 외 업무(영수증·경비) 사용을 발견하고 만든 것 [W32]
- **MCP가 모든 도구의 lingua franca로 굳어가고 있다** (Cursor, Codex CLI, Gemini CLI 모두 채택) [W25]
- **Skill 표준화:** Anthropic 외 도구도 같은 skill 폴더 가리킴 [W25]
- **하네스 격차가 모델 격차보다 커지는 중:** "Top coding agents look more like each other than their underlying models do." [W7]
- **Dive into Claude Code 논문:** 모델이 수렴하는 시점에 **결정성 있는 엔지니어링 하네스가 신뢰성의 결정적 차별점**이 된다는 학술적 정리 [P1]

---

## 8. 논쟁점

> 책의 긴장감을 만드는 자원. 한쪽 입장만 옹호하지 말고 **양쪽을 병기**한다.

### 8.1 Subagent vs 메인 Agent + Task

| 관점 A: Subagent 분할 | 관점 B: 메인에 위임 |
|---|---|
| 컨텍스트 격리, 전문화 prompt, 권한 분리 [W14, C2-팁35] | "brittle한 해법, 인간이 정의한 rigid workflow 강제. CLAUDE.md만 잘 쓰면 메인이 자체 Task()로 더 동적 위임" — Shankar [W30] |
| Anthropic 공식 권장 ("subagents in Claude Code") | "Claude Code is so intelligent it rarely summons subagents anyway" — 호출 신뢰성 비판 [W24] |
| 명확한 책임 분리, 팀 SOP화 가능 | 토큰 7× 소비, 대부분 케이스 과잉 |

### 8.2 Hook 강제 어디까지

| 관점 A: 결정적 Hook 적극 | 관점 B: Block-at-submit만 |
|---|---|
| "100% 준수 vs CLAUDE.md 80%" — 매 번 반드시 해야 할 것은 hook [C2-팁38] | "Plan 도중 막으면 에이전트 좌절 — 끝까지 일하게 하고 commit에서 결과만 검사" [W30] |
| 시큐리티·포매팅·formatter는 deterministic이 옳다 | 과한 hook은 에이전트의 self-correction 능력 망친다 |

### 8.3 자동 머지 vs 수동 게이트

| 관점 A: 야간 자율 머지 | 관점 B: 항상 사람 게이트 |
|---|---|
| Pi/Claude Code 등 야간 자율 작업 가능 [W23] | "인증·결제·데이터 변경은 사람" [C2-팁42] |
| Anthropic Growth Marketing 자동화 사례 [W29] | 96/48% 검증 격차, slopsquatting, prompt injection 사고 [W15, W33] |
| TASKS.md 기반 멀티 에이전트 협업 [W26] | "AI slop PR로 메인테이너 매장" [W15] |

### 8.4 CLAUDE.md 자동생성 vs 수동작성

| 관점 A: `/init`로 자동생성 후 절반 줄이기 | 관점 B: 처음부터 수동 |
|---|---|
| 빠르게 토대 [C2-팁28] | "LLM-생성 agentfile은 성능 ~20% 저하" — ETH Zurich 검증 [W1] |
| | "60줄 미만, 인간이 작성, 모든 룰은 실제 실패에서 유래" [W7] |

### 8.5 더 좋은 모델 기다리기 vs 하네스 투자

| 관점 A: 모델이 곧 다 푼다 | 관점 B: Skill Issue 가설 |
|---|---|
| 모델 capability가 선형 향상 중 | "더 좋은 모델은 새 문제에서 새로 실패한다" [W1] |
| Claude Code/Cursor/Codex 컨버전스 → 모델이 차별화 요소 | "모델이 수렴할수록 하네스가 차별점" [W7, P1] |

### 8.6 시니어/주니어 격차 — 가속인가 양극화인가

| 관점 A: 시니어 가속 | 관점 B: 주니어 위협 |
|---|---|
| Sendbird "시니어 경험 활용 도구" [W34] | "주니어 채용 30% 감소" [W33] |
| GeekNews "experienced junior+ pair" — 시니어가 지휘 [C4] | "코드 이해 없이 PR 올리는 주니어 늘어남" [C4] |
| 시니어가 더 많은 책임 가져 1팀 효과 가능 | 시니어 검증 부담 폭증, skill atrophy 위험 |

### 8.7 도구 다중화 vs 단일 표준

| 관점 A: 단계별 다른 도구 | 관점 B: 단일 표준 |
|---|---|
| "Claude Code는 플래닝, Cursor는 구현, Codex는 자동 테스트" — 분업 [W23] | 올리브영 패턴: 표준 강요 회피하나, IMWEB은 단일 표준으로 보수 운영 [C5, W34] |
| | "shadow AI proliferation" — 통합 거버넌스 불가 [W11] |

### 8.8 MCP의 역할

| 관점 A: 도구 추상화 | 관점 B: 보안 게이트웨이 |
|---|---|
| 일관된 인터페이스로 통합 | "MCP의 일은 auth/network/security 경계, 추상화 아님" — Shankar [W30] |
| Skill < MCP | "Claude Skills는 MCP보다 큰 일" — Willison [W25] |

---

## 9. 리서치 한계 / 커버하지 못한 영역

- **개별 팀의 정량 ROI 데이터 부족:** "10× 향상", "26~55% 향상" 등은 자기보고 또는 case study. RCT 수준 증거는 거의 없다 [P9].
- **한국 대기업 공식 사례 빈약:** 토스/올리브영은 라운드테이블 단편, IMWEB은 Medium 글로 확인하려 했으나 원문 접근 실패 (404). 우아한형제들·카카오·네이버는 책/뉴스 단편적 언급만.
- **장기(6개월+) 운영 로그 분석 연구:** 대부분 4~12주 내 단기 보고. 장기 staying power, 하네스 evolution 데이터 부재.
- **비용 게이트웨이 제품의 객관적 비교:** Kong, Bifrost, Maxim 등 자사 마케팅 자료 위주.
- **실패 사례 (조직 차원):** Prompt injection 1건 외, 큰 사고 공개 사례 적음. 조직이 도입 실패해 롤백한 사례는 거의 없음 (보고 인센티브 부재 가능).
- **Claude Code의 비-영어/한국어 코드베이스 운용:** 다국어 환경에서의 행동 차이 자료 빈약.
- **법률·규제:** EU AI Act, 한국 AI 기본법, 산업별 규제(금융·헬스) 하의 코딩 에이전트 운영 가이드라인 자료 빈약.

---

## 10. 참고문헌

### 웹 (W)

- [W1] Skill Issue: Harness Engineering for Coding Agents — HumanLayer Blog. https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents (접근일 2026-04-26)
- [W2] Effective harnesses for long-running agents — Anthropic Engineering. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents (접근일 2026-04-26)
- [W3] Developer's guide to multi-agent patterns in ADK — Google Developers Blog. https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/
- [W4] Harness engineering for coding agent users — Martin Fowler (Birgitta Böckeler 외). https://martinfowler.com/articles/harness-engineering.html
- [W5] Anthropic Best Practices for Agentic Coding. https://www.anthropic.com/engineering/claude-code-best-practices (관련: code.claude.com/docs/en/best-practices)
- [W6] Beyond Prompts and Context: Harness Engineering for AI Agents — MadPlay. https://madplay.github.io/en/post/harness-engineering
- [W7] AddyOsmani.com — Agent Harness Engineering. https://addyosmani.com/blog/agent-harness-engineering/
- [W8] The Anatomy of an Agent Harness — Avi Chawla. https://blog.dailydoseofds.com/p/the-anatomy-of-an-agent-harness
- [W9] What is an agent harness? — Parallel Web Systems. https://parallel.ai/articles/what-is-an-agent-harness
- [W10] Awesome Harness Engineering. https://github.com/ai-boost/awesome-harness-engineering
- [W11] Governing Claude Code: Secure Agent Harness Rollouts with Kong AI Gateway. https://konghq.com/blog/engineering/claude-code-governance-with-an-ai-gateway
- [W12] Claude Code: Hooks, Subagents, and Skills — Complete Guide (ofox.ai). https://ofox.ai/blog/claude-code-hooks-subagents-skills-complete-guide-2026/
- [W13] Manage costs effectively — Claude Code Docs. https://code.claude.com/docs/en/costs · Best Ways to Monitor Claude Code Token Usage and Costs in 2026 — DEV. https://dev.to/kuldeep_paul/best-ways-to-monitor-claude-code-token-usage-and-costs-in-2026-5j3 · Branch8: How We Cut Claude Code Costs 70%. https://branch8.com/posts/claude-code-token-limits-cost-optimization-apac-teams
- [W14] Hooks reference — Claude Code Docs. https://code.claude.com/docs/en/hooks · How to Use Claude Code Hooks to Prevent Data Deletion (Zenn). https://zenn.dev/tmasuyama1114/articles/claude_code_hooks_guard_bash_command
- [W15] Three AI coding agents leaked secrets through a single prompt injection — VentureBeat. https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026 · AI slop PRs are ruining code review — DEV. https://dev.to/adioof/ai-slop-prs-are-ruining-code-review-for-everyone-56ip · GitHub Ponders Kill Switch for Pull Requests to Stop AI Slop (HN). https://news.ycombinator.com/item?id=46884471 · OWASP Prompt Injection. https://owasp.org/www-community/attacks/PromptInjection
- [W16] (deprecated, merged into W11)
- [W17] Agent Harness Engineering — The Rise of the AI Control Plane (Adnan Masood). https://medium.com/@adnanmasood/agent-harness-engineering-the-rise-of-the-ai-control-plane-938ead884b1d
- [W18] Observability with OpenTelemetry — Claude Agent SDK Docs. https://code.claude.com/docs/en/agent-sdk/observability · SigNoz Claude Code Monitoring. https://signoz.io/blog/claude-code-monitoring-with-opentelemetry/ · ColeMurray/claude-code-otel. https://github.com/ColeMurray/claude-code-otel · TechNickAI/claude_telemetry. https://github.com/TechNickAI/claude_telemetry
- [W19] AI Agent Harness, 3 Principles for Context Engineering (Hugo Bowne-Anderson). https://hugobowne.substack.com/p/ai-agent-harness-3-principles-for
- [W20] (Avi Chawla) Anatomy of an Agent Harness — see W8.
- [W21] Agentic Harness Engineering: LLMs as the New OS — Decoding AI. https://www.decodingai.com/p/agentic-harness-engineering
- [W22] Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support — arXiv 2511.15755. https://arxiv.org/abs/2511.15755
- [W23] Claude Code vs Codex CLI vs Aider vs OpenCode vs Pi vs Cursor — thoughts.jock.pl. https://thoughts.jock.pl/p/ai-coding-harness-agents-2026 · Builder.io: Claude Code vs Cursor. https://www.builder.io/blog/cursor-vs-claude-code · 2026 Guide to Coding CLI Tools — Tembo. https://www.tembo.io/blog/coding-cli-tools-comparison
- [W24] Claude Skills vs Subagent — eesel AI. https://www.eesel.ai/blog/skills-vs-subagent · Stop Adding New Claude Skills. https://buildtolaunch.substack.com/p/claude-skills-not-working-fix · Skills explained — Anthropic. https://claude.com/blog/skills-explained
- [W25] Claude Skills are awesome, maybe a bigger deal than MCP — Simon Willison. https://simonwillison.net/2025/Oct/16/claude-skills/
- [W26] Dive into Claude Code: The Design Space (arXiv 2604.14228). https://arxiv.org/abs/2604.14228 · Anthropic Managed Agents — InfoQ. https://www.infoq.com/news/2026/04/anthropic-managed-agents/ · Geoffrey Litt. https://www.geoffreylitt.com/ · Litt "Code like a surgeon" (Oct 2025).
- [W27] Equipping agents for the real world with Agent Skills — Anthropic Engineering. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills · Agent Skills overview — platform.claude.com. https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview · Skill authoring best practices. https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- [W28] Create and distribute a plugin marketplace — Claude Code Docs. https://code.claude.com/docs/en/plugin-marketplaces · Cowork and plugins for teams across the enterprise. https://claude.com/blog/cowork-plugins-across-enterprise · Building a Private Claude Code Plugin Marketplace (Dominic Böttger). https://dominic-boettger.com/blog/claude-code-private-plugin-marketplace-guide/
- [W29] How Anthropic teams use Claude Code — Anthropic blog. https://claude.com/blog/how-anthropic-teams-use-claude-code · PDF: https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf
- [W30] How I Use Every Claude Code Feature — Shrivu Shankar. https://blog.sshh.io/p/how-i-use-every-claude-code-feature
- [W31] anthropics/claude-code-security-review GitHub Action. https://github.com/anthropics/claude-code-security-review · anthropics/claude-code-action. https://github.com/anthropics/claude-code-action · Code Review docs. https://code.claude.com/docs/en/code-review · Automate security reviews — Anthropic blog. https://claude.com/blog/automate-security-reviews-with-claude-code · Deriv automated security code reviews. https://derivai.substack.com/p/automated-security-code-reviews-claude-code-github-actions
- [W32] Claude Code: Anthropic's Agent in Your Terminal — Latent Space (Cat Wu, Boris Cherny). https://www.latent.space/p/claude-code · Why Anthropic Thinks AI Should Have Its Own Computer — Felix Rieseberg of Claude Cowork. https://www.latent.space/p/felix-anthropic
- [W33] Can Claude Code Replace a Junior Developer? I Tested It. — DEV. https://dev.to/themachinepulse/can-claude-code-replace-a-junior-developer-i-tested-it-f5i · The Secret Life of Claude Code: The Senior Developer's New Role. https://www.tech-reader.blog/2026/04/the-secret-life-of-claude-code-senior.html · Claude Code Just Made Junior Developers Obsolete (And Senior Devs 10x Faster). https://medium.com/@anyapi.ai/claude-code-just-made-junior-developers-obsolete-and-senior-devs-10x-faster-9f71f3c79b93
- [W34] 개발자 AI 지원, 어디까지 왔나 — CIO Korea (Anthropic·Toss·올리브영 라운드테이블). https://www.cio.com/article/4111488/...
- [W35] Karpathy 2025 LLM Year in Review. https://karpathy.bearblog.dev/year-in-review-2025/ · Karpathy LLM Wiki gist. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f · Closing the Loop: Coding Agents, Telemetry — Arize. https://arize.com/blog/closing-the-loop-coding-agents-telemetry-and-the-path-to-self-improving-software/
- [W36] Claude Code Context Window: Optimize Your Token Usage. https://claudefa.st/blog/guide/mechanics/context-management · You're Using Claude Code Wrong. https://diamantai.substack.com/p/youre-using-claude-code-wrong-and · Practical Lessons From the Claude Code Leak — Generative Programmer. https://generativeprogrammer.com/p/practical-lessons-from-the-claude

### 논문 (P)

- [P1] Liu J, Zhao X, Shang X, Shen Z. *Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems.* arXiv:2604.14228 (2026.04). https://arxiv.org/abs/2604.14228
- [P2] *Prompt Injection Attacks on Agentic Coding Assistants: A Systematic Analysis of Vulnerabilities in Skills, Tools, and Protocol Ecosystems.* arXiv:2601.17548 (2026.01). https://arxiv.org/abs/2601.17548
- [P3] *Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?* arXiv:2510.05244 (2025.10). https://arxiv.org/abs/2510.05244
- [P4] *AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering.* arXiv:2604.13120 (2026). https://arxiv.org/abs/2604.13120
- [P5] Shinn N et al. *Reflexion: Language Agents with Verbal Reinforcement Learning.* arXiv:2303.11366 (NeurIPS 2023). https://arxiv.org/abs/2303.11366
- [P6] Wang G et al. *Voyager: An Open-Ended Embodied Agent with Large Language Models.* (Minecraft skill library). https://voyager.minedojo.org/
- [P7] *The Landscape of Agentic Reinforcement Learning for LLMs: A Survey.* arXiv:2509.02547 (2025). https://arxiv.org/abs/2509.02547
- [P8] Ferdowsi M et al. *From Teacher to Colleague: How Coding Experience Shapes Developer Perceptions of AI Tools.* arXiv:2504.13903 (2025.04). https://arxiv.org/abs/2504.13903
- [P9] *Human-AI Experience in Integrated Development Environments: A Systematic Literature Review.* arXiv:2503.06195 (2025). https://arxiv.org/abs/2503.06195
- [P10] *Examining the Use and Impact of an AI Code Assistant on Developer Productivity and Experience in the Enterprise.* CHI 2025 Extended Abstracts. https://dl.acm.org/doi/10.1145/3706599.3706670
- [P11] *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* arXiv:2509.16941 (2025.09, v2 2025.11). https://arxiv.org/abs/2509.16941
- [P12] Liu X et al. *AgentBench: Evaluating LLMs as Agents.* arXiv:2308.03688 (2023). https://arxiv.org/abs/2308.03688
- [P13] *SWE-EVO: Benchmarking Coding Agents in Long-Horizon Software Evolution Scenarios.* arXiv:2512.18470 (2026). https://arxiv.org/abs/2512.18470
- [P14] *A Survey on Code Generation with LLM-based Agents.* arXiv:2508.00083 (2025). https://arxiv.org/abs/2508.00083
- [P15] *Architectural Design Decisions in AI Agent Harnesses.* arXiv:2604.18071 (2026). https://arxiv.org/html/2604.18071v1
- [P16] *The Design Space of LLM-Based AI Coding Assistants: An Analysis of 90 Systems.* (UCSD/VLHCC 2025). https://lau.ucsd.edu/pubs/2025_analysis-of-90-genai-coding-tools_VLHCC.pdf
- [P17] *Rethinking Software Development Considering Collaboration with AI Assistants.* ICSE 2025 Companion. https://dl.acm.org/doi/10.1109/ICSE-Companion66252.2025.00045
- [P18] *Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response.* arXiv:2511.15755 (2025). https://arxiv.org/abs/2511.15755
- [P19] AgenticSE Workshop @ ASE 2025. https://agenticse.github.io/

### 커뮤니티 (C)

- [C1] Claude Code로 5명 팀처럼 개발하는 법 — GeekNews. https://news.hada.io/topic?id=22716
- [C2] 일상적으로 사용하는 Claude Code 팁과 모범 사례 50가지 — GeekNews. https://news.hada.io/topic?id=27677
- [C3] Reddit r/ClaudeAI subagent/skill 논의 (간접) — eesel·Verdent·Towards Data Science 정리 [W24]
- [C4] (laply 외) Claude Code 사용기 — velog. https://velog.io/@laply/Claude-Code-%EC%82%AC%EC%9A%A9%EA%B8%B0
- [C5] AI와 함께하는 DevOps: Claude Code로 생산성 10배 높이기 — Yonghyun Kim, Medium (IMWEB 인프라팀, 원문 404로 GeekNews 단편 인용). https://medium.com/@baramboys0615/...
- [C6] Claude Code 6주 사용기 — GeekNews. https://news.hada.io/topic?id=22375 · Claude Code 2주 사용 후기. https://news.hada.io/topic?id=22053
- [C7] Claude로 코드리뷰 경험 개선하기 — velog. https://velog.io/@kwonhl0211/Claude로-코드리뷰-경험-개선하기
- [C8] [Anthropic] Anthropic팀은 어떻게 Claude Code를 사용하는가? — velog. https://velog.io/@euisuk-chung/Anthropic-Claude-Code-케이스-스터디
- [C9] How I'm Productive with Claude Code — Hacker News. https://news.ycombinator.com/item?id=47494890
- [C10] Effective harnesses for long-running agents — Hacker News discussion. https://news.ycombinator.com/item?id=46081704
- [C11] Claude Code introduces specialized sub-agents — Hacker News. https://news.ycombinator.com/item?id=44686726
- [C12] A Guide to Claude Code 2.0 and getting better at using coding agents — sankalp's blog. https://sankalp.bearblog.dev/my-experience-with-claude-code-20-and-how-to-get-better-at-using-coding-agents/
- [C13] [실제 경험] Claude Code와 Cursor: 일주일 사용 후 알게 된 진짜 비용 효율 — velog (takuya). https://velog.io/@takuya/실제-경험-Claude-Code와-Cursor-일주일-사용-후-알게-된-진짜-비용-효율
- [C14] Claude Code 마스터하기: AI 시대 API 개발 효율화 테크닉 34선 — velog. https://velog.io/@takuya/ai-api-workflow-claude-code-efficiency-tips
- [C15] Awesome Claude Code Subagents — VoltAgent. https://github.com/VoltAgent/awesome-claude-code-subagents
- [C16] Awesome Claude Skills — travisvn. https://github.com/travisvn/awesome-claude-skills
