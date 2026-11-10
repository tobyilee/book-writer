# 부록 B. 도구 명령 대응표와 버전 기준표 (2026-11-10 기준)

이 부록은 책 전체에서 쓴 도구의 판, 하네스별 호출 표기, 그리고 개념과 명령의 대응을 한곳에 모은 참조표다. 본문을 읽다가 "이 명령이 Codex에서는 뭐였지?" 하는 순간에 펼쳐 보면 된다.

먼저 주의할 점이 있다. 여기 적힌 값은 모두 2026년 11월 10일에 공식 저장소와 문서에서 읽은 것이다. Spec Kit과 OpenSpec은 이 책의 자료를 모으는 동안에도 하루 사이에 새 판을 냈다. 그러니 표를 그대로 믿기보다, 따라 하기 전에 아래 "공식 문서 위치"에서 현재 판을 확인하는 편이 낫다. 명령 이름이 바뀌어도 당황할 필요는 없다. 세 번째 표의 개념 열은 오래 남는다.

## 버전 기준표

| 도구 | 기준 판 / 날짜 | 라이선스 | 이 책에서 | 비고 |
|---|---|---|---|---|
| GitHub Spec Kit | v1.3.3 / 2026-11-09 | MIT | 4장, 9장 | 1.0.0은 2026-08-21 |
| OpenSpec | v1.17.0 / 2026-11-09 | MIT | 4장, 8장 | 2.0에서 `/opsx:*` 명령 파일 제거 예고 |
| Superpowers | v7.0.2 / 2026-11-03 | MIT | 5장, 10장 | v7.0.0(2026-10-10)에서 `brainstorming` 재작성 |
| cc-sdd | v3.1.0 / 2026-09-23 | MIT | 4장 | 마지막 푸시 2026-10-22 |
| mattpocock/skills | v1.3.2 / 2026-10-29 | MIT | 5장, 6장 | 마지막 푸시 2026-11-09 |
| BMAD Method | v6.12.4 안정판 / 2026-10-14 | MIT + 상표 | 4장 | v7은 미리보기 알파, 2026-11 중순 정식 출시 예정 |
| Kiro | 버전 번호 없음 (문서 접근 2026-11-10) | 독점 | 3장, 4장 | 정식 출시 2025-11-17 |
| Claude Code | 2.1.319 (로컬 설치본 `claude --version`) | - | 6장, 7장 외 | 문서에 버전 표기 없음 |

날짜는 각 판의 릴리스 날짜다. 별 수와 다운로드 수는 일부러 넣지 않았다. 5장에서 봤듯이 그 숫자들은 관심과 요청을 셀 뿐 쓰임을 세지 않는다. BMAD는 판에 특히 주의하자. 이 책이 다룬 `bmad-spec`과 `SPEC.md`는 안정판 v6.12의 것이고, v7 알파에는 다른 역할과 산출물이 나온다. Kiro는 버전 번호가 없어 문서를 읽은 날짜로만 기준을 남겼다. Kiro 문서는 대부분 갱신일 표기도 없으니, 다시 볼 때는 읽은 날짜를 직접 적어 두는 편이 낫다.

## 하네스별 호출 표기

같은 단계라도 하네스마다 부르는 표기가 다르다. 단계 자체는 같으니 표기만 바꿔 읽으면 된다. 본문은 Claude Code 표기를 기본으로 썼다.

| 도구 | Claude Code | Cursor | GitHub Copilot | Codex CLI |
|---|---|---|---|---|
| Spec Kit (문서 표기 `/speckit.specify`) | `/speckit-specify` | `/speckit-specify` | `/speckit-specify` | `$speckit-specify` |
| Spec Kit 설치 위치 | `.claude/skills/speckit-<command>/` | `.cursor/skills/speckit-<command>/` | `.github/skills/speckit-<command>/` | `.agents/skills/speckit-<command>/` |
| OpenSpec 명령 | `/opsx:propose` | `/opsx-propose` | `/opsx-propose` (IDE만) | `$openspec-propose` |
| OpenSpec 스킬 (2.0 이후 표준 후보) | `/openspec-propose` | 설치 위치 `.cursor/skills/openspec-*/`, 호출 표기는 문서에 없음 | 설치 위치 `.github/skills/openspec-*/`, 호출 표기는 문서에 없음 | `$openspec-propose` |
| Superpowers 설치 | `/plugin install superpowers@claude-plugins-official` | `/add-plugin superpowers` | `copilot plugin install superpowers@superpowers-marketplace` (CLI) | `/plugins`에서 검색 후 설치 |
| Superpowers 호출 | 자동 트리거, 직접 부를 때 `/brainstorming` | 자동 트리거 | 자동 트리거 | 자동 트리거 (직접 부르는 표기는 문서에 없음) |

몇 가지를 덧붙인다. Spec Kit을 기존 저장소에 붙일 때는 `specify integration install claude`처럼 통합 키를 쓴다. Cursor의 통합 키는 `cursor-agent`, Copilot은 `copilot`, Codex는 `codex`다. 여러 에이전트를 함께 쓰는 팀은 `--integration none`을 고르기도 한다. OpenSpec은 Copilot CLI가 사용자 정의 프롬프트 파일을 지원하지 않아 IDE에서만 명령이 된다. Superpowers는 슬래시 명령 디렉터리가 없는 스킬 묶음이라 조건이 맞으면 스스로 켜진다. v7.0.1 릴리스 노트는 이름이나 `/brainstorming`으로 브레인스토밍을 요청하는 경우를 언급하지만, 하네스별 호출 표기는 적지 않는다. OpenSpec도 Cursor와 Copilot에 스킬을 설치하지만 스킬을 직접 부르는 표기는 문서에 없으니, 이 두 하네스에서는 위 줄의 `/opsx-propose` 명령을 쓰자. OpenSpec 스킬 폴더 이름이 명령 이름과 늘 같지는 않다는 점도 기억하자. v1.17.0 저장소에서 sync와 verify의 스킬 폴더는 `openspec-sync-specs`, `openspec-verify-change`다. 설치된 `.claude/skills/openspec-*/` 폴더 이름으로 확인하는 편이 확실하다.

## 개념에서 명령으로

명령은 바뀌어도 개념은 남는다. 도구 없이 하는 방법(6·7장)을 첫 열에 두고, 세 실습 도구에서 같은 개념을 맡는 명령이나 스킬을 나란히 놓았다.

| 개념 | 도구 없이 (6·7장) | OpenSpec (8장) | Spec Kit (9장) | Superpowers (10장) |
|---|---|---|---|---|
| 프로젝트 원칙 | 컨텍스트 파일(`CLAUDE.md`, `AGENTS.md`) | 헌법 같은 전용 장치는 약하다 (추론, `config.yaml`은 프로젝트 설정) | `/speckit-constitution` | 계획마다 Global Constraints |
| 변경 제안 | 인터뷰 프롬프트 | `/opsx:propose` → `proposal.md` | `/speckit-specify` → 기능 폴더 생성 | `brainstorming` |
| 요구 정의 | `SPEC.md` | 델타 스펙 `specs/<domain>/spec.md` | `spec.md` | 설계 문서 `docs/superpowers/specs/` |
| 명확화 | 인터뷰, 검사관 세션 | `/opsx:explore` (제안 전) | `/speckit-clarify` | `brainstorming`의 질문 |
| 계획 | 플랜 모드 | `design.md` (propose가 생성) | `/speckit-plan` | `writing-plans` |
| 태스크 | 계획 안 체크리스트 | `tasks.md` (propose가 생성) | `/speckit-tasks` | 계획의 Task N |
| 계획 수정 | `SPEC.md` 고치고 결정 기록 | `/opsx:update` | 커뮤니티 Spec Refine 확장 | 설계 문서와 계획을 고쳐 다시 승인 (추론) |
| 구현 | 새 세션에서 구현 | `/opsx:apply` | `/speckit-implement` | `subagent-driven-development` 또는 `executing-plans` |
| 정합성 점검 | 대화를 못 본 서브에이전트의 diff 대조 | `openspec validate --strict`, `/opsx:verify` (확장 프로필) | `/speckit-analyze` (읽기 전용), `/speckit-checklist` | `requesting-code-review`, `verification-before-completion` |
| 아카이브·수렴 | PR 본문에 수용 기준 남기기 | `/opsx:sync`, `/opsx:archive` | `/speckit-converge` (태스크 덧붙이기만) | `finishing-a-development-branch` |

마지막 두 줄은 특히 조심해서 읽자. "정합성 점검"과 "수렴"이라는 이름이 같아도 판정자는 다르다. `openspec validate`는 형식을 검사하는 프로그램이고, `/speckit-analyze`와 `/speckit-converge`는 같은 에이전트가 판정한다. 7장의 기준선대로 수용 테스트와 결정적 검사를 일한 에이전트 밖에 두는 일은 어느 도구를 쓰든 따로 해야 한다.

실습 장을 주지 않은 도구는 대표 명령만 적는다.

| 도구 | 대표 흐름 | 비고 |
|---|---|---|
| Kiro 스펙 | IDE의 Spec 또는 CLI `/spec new <name>` → `/spec run <name>` | 산출물 `.kiro/specs/<name>/`, 가벼운 경로는 퀵 스펙과 Plan 모드 |
| cc-sdd | `/kiro-discovery` → `/kiro-spec-init` → `/kiro-spec-requirements` → `/kiro-spec-design` → `/kiro-spec-tasks` → `/kiro-impl` | Codex는 `$kiro-*`, 한국어 산출물은 `--lang ko` |
| BMAD v6.12 | `npx bmad-method install` → `bmad-spec` → `bmad-build` | 모르면 `bmad-help` |
| mattpocock/skills | `/grill-me` 또는 `/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement` | 저장소마다 처음 한 번 `/setup-matt-pocock-skills` (흐름 조합은 추론) |

## 원고 확정 뒤 바뀔 수 있는 것

아래 항목은 이 책이 나온 뒤에 달라질 가능성이 높다. 본문과 다르게 동작하면 먼저 여기를 의심하자. 다시 확인할 때는 순서를 정해 두면 덜 번거롭다. 릴리스 노트에서 현재 판과 breaking 표시를 먼저 보고, 그다음 명령 문서에서 이 부록의 두 번째 표가 아직 맞는지 보고, 마지막으로 하네스 설정 문서에서 키 이름이 그대로인지 본다. 판이 바뀌었는데 개념 표의 칸이 그대로라면 본문의 흐름은 대부분 그대로 쓸 수 있다.

| 항목 | 지금 (2026-11-10) | 확인할 곳 |
|---|---|---|
| OpenSpec 2.0 | `/opsx:*` 명령 파일이 사라지고 스킬만 남는다고 예고. 미리 옮기려면 `openspec config set delivery skills && openspec update` | OpenSpec 릴리스 노트, 이슈 #2022 |
| BMAD v7 | main 브랜치 미리보기 알파. 설치가 `npx skills add bmad-code-org/BMAD-METHOD --skill '*'` 같은 스킬 방식으로 바뀌고 산출물 폴더가 `_bmad-output`. 원문 경고 "Expect breaking changes between updates." | BMAD README. 문서 사이트는 버전 배너 없이 v7 알파를 보여 주므로 안정판은 `V6.12` 브랜치 `docs/` |
| Claude Code 플랜 모드 설정 키 | `plansDirectory`, `showClearContextOnPlanAccept`, `useAutoModeDuringPlan`, `defaultMode: "plan"`, VS Code `claudeCode.initialPermissionMode` | Claude Code permission modes, settings 문서 |
| Spec Kit 릴리스 | 하루 단위로 새 판이 나온다. 버전을 고정하려면 `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.3.3` | Spec Kit 릴리스 노트 |
| Spec Kit 미채택 제안 | 연번 밀림(#4065), 비슷한 문구로 같은 동작이 두 줄로 사는 문제(#4164)의 제안이 미채택 | Spec Kit 이슈 |
| OpenSpec 문서 불일치 | `/opsx:sync` 설명은 RENAMED 절을 언급하지만 개념 문서의 델타 표에는 없다. 이 책은 ADDED/MODIFIED/REMOVED만 썼다 | OpenSpec `commands.md`, `concepts.md` |
| OpenSpec `/opsx:update` | 원인이 구현인지 스펙인지 먼저 판정하는 `/opsx:repair` 제안(#821)은 2026년 8월 "not planned"로 닫히고 토론 게시판으로 옮겨졌다. `/opsx:update`는 계획 산출물만 고치고 코드는 고치지 않는다 | OpenSpec 이슈 #821, `commands.md` |
| Spec Kit 방법론 문서 | `spec-driven.md` 예시는 아직 브랜치를 자동으로 만든다고 적지만, v0.10.0부터 브랜치는 선택 훅으로만 만든다 | Spec Kit `spec-driven.md` |
| Superpowers 문서 불일치 | README는 계획에 "complete code"를 준다고 적지만 `writing-plans` 스킬은 시그니처·파일·값만 준다. 이 책은 스킬을 따랐다 | Superpowers `skills/writing-plans/SKILL.md` |

## 공식 문서 위치

| 도구 | 위치 |
|---|---|
| Spec Kit | https://github.com/github/spec-kit (한국어 README.ko.md), https://github.github.io/spec-kit/ |
| OpenSpec | https://github.com/Fission-AI/OpenSpec (`docs/`), 릴리스 https://github.com/Fission-AI/OpenSpec/releases |
| Superpowers | https://github.com/obra/superpowers |
| cc-sdd | https://github.com/gotalab/cc-sdd |
| mattpocock/skills | https://github.com/mattpocock/skills |
| BMAD Method | https://github.com/bmad-code-org/BMAD-METHOD (안정판 문서는 `V6.12` 브랜치 `docs/`, 한국어 `docs/ko-kr/`) |
| Kiro | https://kiro.dev/docs/specs/ |
| Claude Code | https://code.claude.com/docs/en/permission-modes , https://code.claude.com/docs/en/best-practices |
| Cursor Plan Mode | https://cursor.com/docs/agent/plan-mode |
| VS Code Copilot 계획 | https://code.visualstudio.com/docs/agents/run/planning |
| Codex CLI 슬래시 명령 | https://developers.openai.com/codex/cli/slash-commands |

표를 다시 조회할 때는 버전 번호만 보지 말고 날짜도 함께 적어 두자. "{버전}/{날짜} 기준"으로 남긴 기록이 있어야 나중에 무엇이 바뀌었는지 알 수 있다.
