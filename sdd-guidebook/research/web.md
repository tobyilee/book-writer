# 웹 리서치: 실습용 SDD 도구 사용 상세 (1차 출처 원장)

- 수집 시점: 2026-11-10 (모든 자료의 접근일은 2026-11-10)
- 역할: `research/sdd-report.md`(2026-11-09 검증)의 지형도를 다시 쓰지 않는다. 실습서가 필요로 하는 **정확한 설치 명령, 명령 목록, 생성 디렉터리, 문서 헤딩 구조, 실제 스펙 발췌**를 1차 출처에서 모은다.
- 출처 우선순위: 공식 저장소의 원본 파일(템플릿·SKILL.md·docs/*.md, GitHub API로 직접 읽음) > 공식 문서 사이트 > 공개 저장소의 실사용 스펙.
- 날짜 표기: "발행일"은 공식 문서에 날짜가 없으면 **해당 파일의 마지막 커밋 시각**(GitHub API)을 적는다. 버전은 모두 "{버전}/{날짜} 기준"으로 못 박는다.
- 저작권: Spec Kit, OpenSpec, cc-sdd, Superpowers, mattpocock/skills는 MIT 저장소다. 템플릿 헤딩 구조는 원문 그대로 옮기되, 긴 본문은 짧게 발췌한다. Kiro 문서·Anthropic 문서·라이선스 표기가 없는 저장소(shuk)는 짧은 발췌만 남긴다.
- 표기: **[보고서와 다름]** 은 `sdd-report.md`의 서술과 1차 출처가 어긋나는 지점이다. 마지막 절에 모아 둔다.

---

## 0. 한눈에 보는 버전 기준표 (2026-11-10 GitHub API 조회)

| 도구 | 최신 릴리스 | 릴리스 시각(UTC) | 마지막 푸시 | 비고 |
|---|---|---|---|---|
| GitHub Spec Kit | **v1.3.3** | 2026-11-09 20:40 | 2026-11-10 01:57 | 보고서 기준값은 v1.3.2(2026-11-06) |
| OpenSpec | **v1.17.0** | 2026-11-09 23:46 | 2026-11-09 23:47 | 보고서 기준값은 v1.16.1(2026-11-07) |
| cc-sdd | v3.1.0 | 2026-09-23 07:30 | 2026-10-22 | 보고서와 같음 |
| BMAD Method | v6.12.4 (안정) | 2026-10-14 21:19 | 2026-11-08 | v7은 main 브랜치의 미리보기 알파 |
| Superpowers | v7.0.2 | 2026-11-03 22:17 | 2026-11-03 | 보고서와 같음 |
| mattpocock/skills | v1.3.2 | 2026-10-29 10:27 | 2026-11-09 | 보고서와 같음 |
| Claude Code | 2.1.319 (로컬 설치본 `claude --version`) | - | - | 문서는 버전 표기 없음 |

> 빠르게 변하는 영역이다. 원고 확정 직전에 이 표를 다시 조회할 것을 권장한다. Spec Kit과 OpenSpec은 보고서 검증일 이후 하루 사이에 새 릴리스가 나왔다.

---

## 자료 1: GitHub Spec Kit — README (설치·최소 흐름)

- 출처: https://github.com/github/spec-kit (README.md), 한국어판 https://github.com/github/spec-kit/blob/main/README.ko.md
- 저자·날짜: GitHub. README.md 마지막 커밋 2026-11-04, README.ko.md 마지막 커밋 2026-11-04. v1.3.3/2026-11-09 기준.
- 신뢰성: 최상 (공식 저장소)
- 핵심 주장: Spec Kit은 이제 SDD 하나만이 아니라 "SDD, 버그 수정, 아이디어 평가, 직접 만든 프로세스" 네 진입점을 둔다. SDD는 코어에 있고 버그 수정·평가는 확장으로 설치한다. 명령은 터미널이 아니라 에이전트 채팅에서 하나씩 실행하고, 결과를 검토한 뒤 다음으로 넘어간다.
- 사전 요구: Python 3.11+, uv, 지원 에이전트 (Linux/macOS/Windows).

설치 (README 원문, v1.3.3 기준):

```bash
uv tool install specify-cli
specify init my-project --integration copilot
cd my-project
```

버전 고정 설치 (v1.3.3 릴리스 노트 원문):

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.3.3
specify init my-project
```

최소 SDD 흐름 (README 원문, Copilot 기본 스킬 표기):

```text
/speckit-constitution Create principles focused on code quality, testing, and maintainability.
/speckit-specify Build a photo organizer with albums grouped by date and a tile preview of each album.
/speckit-plan Use Vite with vanilla JavaScript. Keep images local and store metadata in SQLite.
/speckit-tasks
/speckit-implement
/speckit-converge
```

- 인용 가능한 구절:
  > "Repeat implement and converge until convergence reports `Converged`."
  > "These are independent entry points, not mandatory phases."
- 버그 수정 확장 (README 원문): `specify extension add bug` 후 `/speckit-bug-assess "..." slug=login-crash` → `/speckit-bug-fix slug=login-crash` → `/speckit-bug-test slug=login-crash`. 보고서는 `.specify/bugs/login-crash/`에 쌓이고 판정은 `verified`/`partial`/`failed`.
- 아이디어 평가 확장: `specify extension add assess` 후 `/speckit-assess-intake` → `-research` → `-define` → `-shape` → `-decide`. 산출물 `.specify/assessments/<slug>/`, 판정 `go`/`needs-clarification`/`kill`.
- 관련 섹션: 실습 장 "Spec Kit으로 기능 하나 만들기", 부록 설치표

## 자료 2: Spec Kit — 에이전트별 설치 위치와 호출 표기

- 출처: https://github.github.io/spec-kit/integrations/cli.html (Command Invocation 절), 저장소 원본 `docs/integrations/claude.md`, `codex.md`, `cursor-agent.md`, `copilot.md`
- 저자·날짜: GitHub. 접근 2026-11-10, v1.3.3 기준. 통합 목록 페이지는 통합 43개(`none`, `generic` 포함)를 싣는다.
- 신뢰성: 최상
- 핵심 주장: 단계는 모든 에이전트에서 같고 표기만 다르다. 공식 문서는 점 표기(`/speckit.specify`)를 쓰지만 실제 설치본은 하이픈 스킬(`/speckit-specify`)이나 `$` 스킬이다.

| 에이전트 | 통합 키 | 설치 위치 | 호출 예 |
|---|---|---|---|
| Claude Code | `claude` | `.claude/skills/speckit-<command>/SKILL.md` | `/speckit-specify` |
| Codex CLI | `codex` | `.agents/skills/speckit-<command>/SKILL.md` | `$speckit-specify` |
| Cursor | `cursor-agent` | `.cursor/skills/speckit-<command>/SKILL.md` | `/speckit-specify` |
| GitHub Copilot | `copilot` | `.github/skills/speckit-<command>/SKILL.md` | `/speckit-specify` |
| 문서 표기 | - | - | `/speckit.specify` |

- 기존 프로젝트에 붙일 때: `specify integration install claude` (docs/integrations/claude.md 원문).
- CLI 하위 명령 (cli.html 예시에서 확인): `specify init`, `specify check`, `specify integration list|search|info|install|uninstall|switch|use|upgrade|status|catalog`, `specify extension add`, `specify preset add`, `specify version`, `specify artifact list --json`.
- 컨텍스트 비용 옵션 (docs/integrations/claude.md 원문 요약): 기본값에서는 모든 Spec Kit 스킬이 모델 호출 가능이라 설명이 항상 컨텍스트에 들어간다. 아래 옵션을 주면 코어 스킬에 `disable-model-invocation: true`가 들어가 사용자가 직접 부를 때만 실행된다.

```bash
specify init my-project --integration claude --integration-options="--no-model-invocation"
```

- 인용 가능한 구절 (cli.html):
  > "Invoke Spec Kit's process steps inside your coding agent, not in the terminal."
- 관련 섹션: 하네스별 설치 부록, "스킬이 컨텍스트를 먹는다" 주의 박스

## 자료 3: Spec Kit — SDD 명령 레퍼런스 (9개 명령)

- 출처: https://github.github.io/spec-kit/reference/agentic-sdd.html , 원본 `templates/commands/*.md`
- 저자·날짜: GitHub. 접근 2026-11-10, v1.3.3 기준.
- 신뢰성: 최상

| 명령 | 공식 설명 (원문) | 쓰거나 읽는 파일 |
|---|---|---|
| `/speckit.constitution` | "Establish or update project principles" | `.specify/memory/constitution.md` |
| `/speckit.specify` | "Define requirements and user stories" | `specs/<NNN>-<short-name>/spec.md`, `checklists/requirements.md`, `.specify/feature.json` |
| `/speckit.clarify` | "Resolve ambiguity before planning (optional quality gate; formerly `/quizme`)" | `spec.md`에 `## Clarifications` → `### Session YYYY-MM-DD` 추가 |
| `/speckit.plan` | "Create the technical implementation plan" | `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/` |
| `/speckit.checklist` | "Generate requirements-quality checklists (optional quality gate)" | `checklists/*.md` |
| `/speckit.tasks` | "Break the plan into actionable tasks" | `tasks.md` |
| `/speckit.analyze` | "Check artifact consistency after tasks and before implementation (optional quality gate)" | 읽기 전용 |
| `/speckit.implement` | "Execute the tasks" | `tasks.md`를 읽고 코드 작성 |
| `/speckit.converge` | "Assess implementation against the artifacts and append remaining work" | `tasks.md`에 `## Phase N: Convergence`만 덧붙임 |

- 세부 규칙 (원문):
  - clarify: "Asks up to five targeted questions about underspecified areas of the current spec." (`templates/commands/clarify.md`: "Maximum of 5 total questions across the whole session.")
  - analyze: "**read-only**" / "never edits files."
  - converge: "append-only: it never edits or deletes code, and its only possible write is adding tasks to `tasks.md`."
- 기능 디렉터리 이름 규칙 (`templates/commands/specify.md` 원문 요약): 기본은 `specs/` 아래. `.specify/init-options.json`의 `feature_numbering`이 `"sequential"`이거나 없으면 `NNN` 세 자리 번호, `"timestamp"`면 `YYYYMMDD-HHMMSS`. 예 `003-user-auth`, `20260319-143022-user-auth`. 결정된 경로는 `.specify/feature.json`의 `"feature_directory"`에 저장해 다음 명령이 브랜치 이름 없이 찾게 한다.
  > "The spec directory name and the git branch name are independent — they may be the same but that is the user's choice"
- 브랜치 생성은 선택 기능이다. `before_specify` 훅이 있을 때만 git 브랜치를 만든다 (v0.10.0, 2026-06-09부터. 보고서 2.1절과 일치).
- 관련 섹션: Spec Kit 명령 한 장 요약표

## 자료 4: Spec Kit — 생성 문서 템플릿의 헤딩 구조 (실습용 골격)

- 출처: https://github.com/github/spec-kit/tree/main/templates
- 저자·날짜: GitHub(MIT). 파일별 마지막 커밋: `spec-template.md` 2026-05-12, `plan-template.md` 2026-07-10, `tasks-template.md` 2026-05-12, `constitution-template.md` 2026-02-09. v1.3.3 기준.
- 신뢰성: 최상

### 4-1. `constitution-template.md` → `.specify/memory/constitution.md`

```markdown
# [PROJECT_NAME] Constitution
## Core Principles
### [PRINCIPLE_1_NAME]        <!-- Example: I. Library-First -->
### [PRINCIPLE_2_NAME]        <!-- Example: II. CLI Interface -->
### [PRINCIPLE_3_NAME]        <!-- Example: III. Test-First (NON-NEGOTIABLE) -->
### [PRINCIPLE_4_NAME]        <!-- Example: IV. Integration Testing -->
### [PRINCIPLE_5_NAME]        <!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
## [SECTION_2_NAME]           <!-- Example: Additional Constraints, Security Requirements ... -->
## [SECTION_3_NAME]           <!-- Example: Development Workflow, Review Process, Quality Gates ... -->
## Governance
**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
```

- 템플릿 주석의 예시 문장 (원문): "TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced"
- 방법론 문서 `spec-driven.md`의 "The Nine Articles of Development"는 Article I(Library-First), II(CLI Interface Mandate), III(Test-First Imperative), IV~VI(프로젝트가 정의), VII~VIII(Simplicity, Anti-Abstraction), IX(Integration-First Testing)로 설명한다.
  > "Articles IV, V, and VI are intentionally defined by each project's constitution rather than prescribed by Spec Kit."
  - 정리: **템플릿 파일 자체는 원칙 칸 5개 + 추가 절 2개 + Governance** 구조다. "조항 9개"는 방법론 문서의 설명틀이고, 템플릿이 9개 칸을 만들지는 않는다. (보고서 2.1절 "조항 9개를 담습니다" 문장을 실습 장에서 쓸 때 이 구분을 붙일 것.)

### 4-2. `spec-template.md` → `specs/<feature>/spec.md`

```markdown
# Feature Specification: [FEATURE NAME]
**Feature Branch**: `[###-feature-name]`
**Created**: [DATE]
**Status**: Draft
**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*
### User Story 1 - [Brief Title] (Priority: P1)
**Why this priority**: ...
**Independent Test**: ...
**Acceptance Scenarios**:
1. **Given** [initial state], **When** [action], **Then** [expected outcome]
### User Story 2 - [Brief Title] (Priority: P2)
### User Story 3 - [Brief Title] (Priority: P3)
### Edge Cases

## Requirements *(mandatory)*
### Functional Requirements
- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
### Key Entities *(include if feature involves data)*

## Success Criteria *(mandatory)*
### Measurable Outcomes
- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]

## Assumptions
```

- 불명확 표시 규칙 (원문 예시):
  > "- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]"
- Success Criteria 주석 (원문): "These must be technology-agnostic and measurable."
- 실습 포인트: Spec Kit의 수용 기준은 EARS가 아니라 **Given/When/Then** 시나리오이고, 기능 요구사항은 RFC 2119식 `MUST` 문장(FR-번호)이다. Kiro(EARS)·OpenSpec(SHALL + GIVEN/WHEN/THEN)과 비교하는 표로 쓰기 좋다.

### 4-3. `plan-template.md` → `specs/<feature>/plan.md`

```markdown
# Implementation Plan: [FEATURE]
**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`
## Summary
## Technical Context
**Language/Version** / **Primary Dependencies** / **Storage** / **Testing** /
**Target Platform** / **Project Type** / **Performance Goals** / **Constraints** / **Scale/Scope**
## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*
## Project Structure
### Documentation (this feature)
### Source Code (repository root)
**Structure Decision**: ...
## Complexity Tracking
```

- 기능 폴더의 문서 배치 (템플릿 원문 트리):

```text
specs/[###-feature]/
├── plan.md              # This file (plan command output)
├── research.md          # Phase 0 output (plan command)
├── data-model.md        # Phase 1 output (plan command)
├── quickstart.md        # Phase 1 output (plan command)
├── contracts/           # Phase 1 output (plan command)
└── tasks.md             # Phase 2 output (tasks command - NOT created by plan)
```

- Technical Context 각 항목의 기본값은 "`or NEEDS CLARIFICATION`"이 붙은 자리 표시다. 모르는 값을 지어내지 말고 표시하라는 장치다.

### 4-4. `tasks-template.md` → `specs/<feature>/tasks.md`

```markdown
# Tasks: [FEATURE NAME]
**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
## Format: `[ID] [P?] [Story] Description`
## Path Conventions
## Phase 1: Setup (Shared Infrastructure)
## Phase 2: Foundational (Blocking Prerequisites)
## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP
### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️
### Implementation for User Story 1
**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently
## Phase 4: User Story 2 - [Title] (Priority: P2)
...
## Phase N: Polish & Cross-Cutting Concerns
```

- 태스크 줄 형식 (원문 예):
  > "- [ ] T012 [P] [US1] Create [Entity1] model in src/models/[entity1].py"
  - `[P]` = 병렬 가능(다른 파일, 의존 없음), `[US1]` = 사용자 스토리 번호, 정확한 파일 경로 포함.
- 테스트 정책 (원문): "Tests are OPTIONAL - only include them if explicitly requested in the feature specification." — 헌법의 Test-First 원칙과 함께 읽어야 하는 지점이다.
- converge가 덧붙이는 절: `## Phase N: Convergence` (`templates/commands/converge.md`).
- 관련 섹션: "Spec Kit 산출물 해부" 장, 부록 템플릿 모음

## 자료 5: Spec Kit — 방법론 문서 `spec-driven.md`의 예시 흐름

- 출처: https://github.com/github/spec-kit/blob/main/spec-driven.md
- 저자·날짜: GitHub(MIT). 접근 2026-11-10.
- 신뢰성: 최상(단, 일부 예시는 구버전 동작을 남김)
- 핵심 주장: 채팅 기능 예시에서 `/speckit.specify` → `/speckit.plan` → `/speckit.tasks`가 `specs/003-chat-system/` 아래 `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `tasks.md`를 만든다고 설명한다.
- 주의 (구버전 정보일 수 있음): 같은 예시가 "Creates branch "003-chat-system""이라고 적는다. 현재 `specify` 명령 템플릿은 브랜치 생성을 선택 훅으로 돌렸으므로, 이 문장은 v0.10.0(2026-06-09) 이전 동작이다. 원고에서 인용할 때 주석을 붙일 것.
- 관련 섹션: Spec Kit 역사·철학 박스

---

## 자료 6: Kiro — Specs 개요 (3문서 구조, IDE·CLI·Web 시작 방법)

- 출처: https://kiro.dev/docs/specs/ (원본 `https://kiro.dev/docs/specs.md`)
- 저자·날짜: AWS Kiro. 페이지 날짜 표기 없음. 접근 2026-11-10.
- 신뢰성: 최상 (공식 문서, 독점 제품)
- 핵심 주장: 모든 스펙은 `requirements.md`(또는 버그면 `bugfix.md`), `design.md`, `tasks.md` 세 파일을 `.kiro/specs/<name>/`에 만든다. 기능 표에서 Feature/Bugfix/Quick Spec·병렬 태스크 실행은 IDE·CLI·Web 모두 ✓, Analyze Requirements는 IDE·CLI ✓·Web —, 속성 기반 테스트(Correctness)는 IDE만 ✓.
- 시작 방법 (원문 요약):
  - IDE: Kiro 창의 **Specs** 아래 `+`를 누르거나 채팅 창에서 **Spec**을 고른다. Feature면 **Requirements-First** 또는 **Design-First**를 고른다. 각 단계 문서의 **Review** 버튼으로 Markdown Review를 열어 구절에 댓글을 단다.
  - CLI: `/spec new <name>`으로 시작 → 에이전트가 Spec 모드로 바뀌고 Feature/Bug/Quick Spec 중 무엇인지 묻는다 → 산출물은 `.kiro/specs/<name>/` → 단계마다 `Ctrl+X`로 문서를 읽고 줄 댓글 → `/spec run <name>`으로 전체 화면 태스크 실행, `/spec <name>`으로 재개.
  - Web: app.kiro.dev에서 저장소를 고르고 **Spec** 선택 → 완료되면 PR을 연다. 산출물은 **Download**로 `.md` 저장.
- 병렬 실행 (원문): "Waves execute sequentially; tasks within a wave execute concurrently."
- 관련 섹션: Kiro 실습 장 도입, IDE/CLI 비교 박스

## 자료 7: Kiro — Requirements-First 흐름과 EARS 예

- 출처: https://kiro.dev/docs/specs/feature-specs/requirements-first.md , 상위 페이지 https://kiro.dev/docs/specs/feature-specs/
- 저자·날짜: AWS Kiro. 상위 페이지 "Page updated: August 4, 2026". 하위 페이지 날짜 없음. 접근 2026-11-10.
- 신뢰성: 최상
- 흐름: Feature Spec 생성 → Requirements-First 선택 → `requirements.md` 생성·검토·확정("Confirm when requirements meet your needs") → `design.md` 생성·검토 → `tasks.md` 생성(선택 태스크 표시) → 개별 또는 전체 실행.
- `requirements.md`에 들어가는 것 (원문 목록): "User stories with clear acceptance criteria", "System behaviors in EARS format (WHEN...THE SYSTEM SHALL...)", "Functional requirements", "Edge cases and error handling".
- `design.md`에 들어가는 것 (원문 목록): "System architecture and components", "Sequence diagrams showing interactions", "Data models and interfaces", "Technology stack recommendations", "Error handling approach", "Testing strategy".
- `tasks.md`에 들어가는 것 (원문 목록): "Discrete, trackable tasks", "Clear descriptions and expected outcomes", "Dependencies between tasks", "Optional vs required tasks".
- EARS 예 (문서 예시, 짧은 발췌):

```markdown
WHEN a user submits valid registration data
THE SYSTEM SHALL create a new user account
```

- 문형 (feature-specs 페이지 원문): "WHEN [condition/event] THE SYSTEM SHALL [expected behavior]"
- 설계 우선 흐름 (https://kiro.dev/docs/specs/feature-specs/tech-design-first.md): Design-First를 고른 뒤 **High Level Design**(아키텍처 다이어그램, 컴포넌트, 비기능 속성) 또는 **Low Level Design**(의사코드, 인터페이스, 데이터 구조) 수준을 고른다. design.md 확정 후 요구사항을 역으로 도출한다.
- 관련 섹션: Kiro 실습 장 "요구사항 → 설계 → 태스크"

## 자료 8: Kiro — Bugfix Spec, Quick Spec, Plan 모드

- 출처: https://kiro.dev/docs/specs/bugfix-specs.md , https://kiro.dev/docs/specs/quick-spec.md , https://kiro.dev/docs/specs/plan.md
- 저자·날짜: AWS Kiro. 페이지 날짜 없음. 접근 2026-11-10.
- 신뢰성: 최상
- `bugfix.md` 세 절과 문형 (원문):
  - Current Behavior (Defect): "WHEN [condition] THEN the system [incorrect behavior]"
  - Expected Behavior (Correct): "WHEN [condition] THEN the system SHALL [correct behavior]"
  - Unchanged Behavior (Regression Prevention): "WHEN [condition] THEN the system SHALL CONTINUE TO [existing behavior]"
  - 버그 design.md는 근본 원인 분석, 수정 방식, 세 종류 속성(버그 재현·수정 확인·회귀 방지)을 담는다. 태스크는 속성 기반 테스트로 이 셋을 검증한다.
  - 문서가 권하는 버그 설명 예 (best-practices): "O'Brien" 같은 특수문자 이름에서 500 오류 → 정상 저장 → 이메일·비밀번호 검증 로직은 건드리지 말 것.
- Quick Spec: 시작할 때 범위·제약·경계 사례를 한 번에 묻고, 승인 관문 없이 세 문서를 차례로 만든다. 산출물 형식은 표준 스펙과 같다.
  > "Vibe mode is conversational and unstructured - there are no artifacts saved to `.kiro/specs/`."
- Plan 모드 (plan.md): 기능 표에서 **IDE ✓, CLI ✓**, Web·Mobile —. IDE는 "Let's build" 화면이나 에이전트 선택기에서 **Plan**. CLI는 `Shift+Tab` 또는 `/plan`, 프롬프트에 `[plan]` 표시. 계획은 대화 컨텍스트에만 있고 `.kiro/specs/`에 저장하지 않는다. 15~60분 구현 작업에 권한다(보고서와 일치).
  - **[보고서와 다름]** 보고서 4절 Kiro 표는 Plan 모드 CLI를 "확인 안 됨"으로 적었다. 현재 문서는 CLI 지원을 명시한다.
- 관련 섹션: "작업 크기에 맞는 Kiro 경로 고르기"

## 자료 9: Kiro — 스펙 반복·동기화 모범 사례

- 출처: https://kiro.dev/docs/specs/best-practices.md
- 저자·날짜: AWS Kiro. 날짜 없음. 접근 2026-11-10.
- 신뢰성: 최상
- 핵심 내용 (원문 요약):
  - 워크플로는 스펙을 만들 때 고르고 바꿀 수 없다. 바꾸려면 새 Feature Spec을 만든다.
  - 기존 요구사항 문서 가져오기: 파일을 저장소에 두고 스펙 채팅에서 `#foo-prfaq.md Generate a spec from it`.
  - 요구사항을 고친 뒤: 스펙 채팅에서 design.md 갱신을 요청 → `tasks.md`에서 **Sync Files** → 새 태스크 생성. 이미 구현된 태스크는 Sync Files나 "Check which tasks are already complete" 요청으로 완료 표시.
  - 바이브 세션에서 `Generate spec`이라고 하면 스펙 세션으로 넘어간다.
  - 채팅에서 `#spec`으로 스펙 세 파일 전체를 컨텍스트에 넣는다.
  - Analyze Requirements는 "minutes (not seconds)" 걸리며 작은 스펙은 건너뛰어도 된다.
  - 팀 공유: 스펙을 코드와 같은 저장소에 버전 관리. 여러 팀은 중앙 스펙 저장소 + git submodule.
- 관련 섹션: "스펙이 코드와 어긋날 때" 절

## 자료 10: Kiro 실사용 스펙 예 — `darko-mesaros/shuk` 의 `.kiro/specs/upload-only/`

- 출처: https://github.com/darko-mesaros/shuk/tree/main/.kiro/specs/upload-only (`requirements.md` 86줄, `design.md` 232줄, `tasks.md` 117줄)
- 저자·날짜: Darko Mesaros(공개 저장소, 라이선스 표기 없음 → 짧게만 발췌). requirements.md 마지막 커밋 2026-06-09. 접근 2026-11-10.
- 신뢰성: 중 (실사용 예. 공식 예시는 아님)
- 왜 중요한가: 공식 문서 예시(헤딩 + WHEN/SHALL 두 줄)보다 **2026년 Kiro가 실제로 생성하는 형식**을 보여 준다. 공식 문서에는 이 헤딩 구조가 없다.
- `requirements.md` 헤딩: `# Requirements Document` → `## Introduction` → `## Glossary` → `## Requirements` → `### Requirement 1: Upload-Only CLI Flag Definition` → `**User Story:** As a user, I want ..., so that ...` → `#### Acceptance Criteria` (번호 목록)
- 수용 기준 발췌 (2줄):

```markdown
1. THE CLI_Parser SHALL accept an optional `--upload-only` boolean flag that defaults to `false` when not provided.
3. WHEN the `--upload-only` flag is provided without a filename, THE CLI_Parser SHALL exit with a non-zero exit code and write an error message to stderr indicating that a filename is required.
```

  - 관찰: Glossary에서 정의한 컴포넌트 이름(`CLI_Parser`, `Upload_Engine`)을 EARS의 `<system name>` 자리에 쓴다. Ubiquitous(`THE ... SHALL`)와 Event-driven(`WHEN ..., THE ... SHALL`)이 섞인다.
- `design.md` 헤딩: Overview / Design Rationale / Architecture / Components and Interfaces / Data Models / **Correctness Properties** / Error Handling / Testing Strategy(Unit, Property-Based, Integration)
  - 속성 형식 발췌: "### Property 1: Upload-only flag parses correctly with any valid filename" → "*For any* valid filename string ..." → "**Validates: Requirements 1.2, 1.5**"
- `tasks.md` 형식:
  - `# Implementation Plan: ...` → `## Overview` → `## Tasks` → 계층 체크박스 `- [x] 1.` / `- [x] 1.1`
  - 선택 태스크 표시 `- [ ]*` (예: 속성 테스트 작성 태스크)
  - 추적 표기 `_Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_`, 속성 태스크는 `**Validates: Requirements 1.2, 1.5**`
  - 끝에 `## Task Dependency Graph` JSON(`"waves": [{ "id": 0, "tasks": ["1.1"] }, ...]`) — 공식 문서의 웨이브 병렬 실행과 대응
- 관련 섹션: "Kiro 산출물 실제로 읽어 보기" 실습. 원고에는 이 저장소를 링크하고 구조만 설명하는 편이 안전하다.

## 자료 11: Kiro — 스티어링과 설치

- 출처: https://kiro.dev/docs/steering/ , https://kiro.dev/docs/getting-started/installation.md
- 저자·날짜: AWS Kiro. 날짜 없음. 접근 2026-11-10.
- 신뢰성: 최상
- 스티어링: 작업 공간 `.kiro/steering/`(IDE·CLI·Web·Mobile), 전역 `~/.kiro/steering/`(IDE·CLI). 기본 파일 `product.md`(목적·사용자·기능), `tech.md`(스택·제약), `structure.md`(파일 구성·명명·import 패턴). 포함 모드는 YAML 머리말 `inclusion: always | fileMatch | manual | auto`. AGENTS.md도 읽지만 "do not support inclusion modes and are always included."
- 설치: IDE는 kiro.dev에서 설치 파일을 받는다. CLI는 macOS `brew install kiro-cli` 또는 `curl -fsSL https://cli.kiro.dev/install | bash` (Linux는 rpm/deb 패키지 경로도 있음).
- 관련 섹션: Kiro 실습 준비, 스티어링 = Spec Kit 헌법과 비교 박스

---

## 자료 12: EARS 원전 — Alistair Mavin

- 출처: https://alistairmavin.com/ears/
- 저자·날짜: Alistair Mavin. 페이지 저작권 표기 © 2026. EARS 최초 발표는 2009년(Rolls-Royce PLC에서 제트 엔진 제어 시스템의 감항 규정을 분석하며 개발). 원 논문: Mavin et al., "Easy Approach to Requirements Syntax (EARS)", RE'09 (2009). 접근 2026-11-10.
- 신뢰성: 최상 (원저자)
- 일반 문형 (원문): "While <optional pre-condition>, when <optional trigger>, the <system name> shall <system response>"

| 패턴 | 키워드 | 템플릿 (원문) | 예문 (원문) |
|---|---|---|---|
| Ubiquitous (항상) | 없음 | The <system name> shall <system response> | The mobile phone shall have a mass of less than XX grams. |
| State-driven (상태) | While | While <precondition(s)>, the <system name> shall <system response> | While there is no card in the ATM, the ATM shall display "insert card to begin". |
| Event-driven (사건) | When | When <trigger>, the <system name> shall <system response> | When "mute" is selected, the laptop shall suppress all audio output. |
| Optional feature (선택 기능) | Where | Where <feature is included>, the <system name> shall <system response> | Where the car has a sunroof, the car shall have a sunroof control panel on the driver door. |
| Unwanted behaviour (원치 않는 동작) | If / Then | If <trigger>, then the <system name> shall <system response> | If an invalid credit card number is entered, then the website shall display "please re-enter credit card details". |
| Complex (복합) | 조합 | While <precondition(s)>, When <trigger>, the <system name> shall <system response> | While the aircraft is on ground, when reverse thrust is commanded, the engine control system shall enable reverse thrust. |

- 도구별 변형 (위 원전과 비교해 원고에 쓸 것):
  - Kiro 문서: `WHEN ... THE SYSTEM SHALL ...` (대문자, 주어를 THE SYSTEM으로 고정). 실사용 예는 Glossary의 컴포넌트 이름을 주어로 쓴다(자료 10). 버그 스펙은 EARS에 없는 `SHALL CONTINUE TO`를 더한다(자료 8).
  - cc-sdd 템플릿: 원전 다섯 패턴을 그대로 쓰되 `When ...,` 대신 레거시 예시는 `WHEN ... THEN ... SHALL`도 섞인다(자료 18).
  - OpenSpec: EARS가 아니라 `The system SHALL ...` 한 문장 + GIVEN/WHEN/THEN 시나리오(자료 15).
  - Spec Kit: EARS가 아니라 `System MUST ...`(FR) + Given/When/Then(자료 4).
- 관련 섹션: "EARS로 수용 기준 쓰기" 절 (한국어 예문 작성 시 cc-sdd 규칙 참고: 키워드는 영어로 두고 변수 부분만 한국어)

---

## 자료 13: OpenSpec — 설치와 초기화 (v1.15.0 이후 기본 설치 변경)

- 출처: https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md , `docs/getting-started.md`, 릴리스 노트 https://github.com/Fission-AI/OpenSpec/releases
- 저자·날짜: Fission AI(MIT). v1.15.0 2026-10-24, v1.16.0 2026-10-30, v1.16.1 2026-11-07, v1.17.0 2026-11-09. 접근 2026-11-10.
- 신뢰성: 최상
- 기본 설치 = 독립 실행 파일 (Node.js 불필요, installation.md 원문):

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/scripts/binary/install.sh | sh
# Windows (PowerShell)
irm https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/scripts/binary/install.ps1 | iex
```

  - v1.16.0 릴리스 노트는 짧은 주소도 안내한다: `curl -fsSL https://openspec.dev/cli/install.sh | sh` (Windows `irm https://openspec.dev/cli/install.ps1 | iex`).
  - 설치 위치 `~/.local/bin`, `OPENSPEC_VERSION=v1.15.0`으로 버전 고정 가능.
- 패키지 관리자 경로 (Node.js **22.12.0 이상**, v1.16.0부터 breaking): `npm install -g @fission-ai/openspec@latest` (pnpm/bun/yarn 1.x도 가능)
  > v1.16.0 원문: "The standalone binary, the default install since v1.15.0, doesn't use Node"
- 다섯 줄 흐름 (getting-started.md 원문):

```text
TERMINAL   $ curl -fsSL https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/scripts/binary/install.sh | sh
TERMINAL   $ cd your-project && openspec init
AI CHAT      /opsx:explore                    (optional: think it through first)
AI CHAT      /opsx:propose add-dark-mode      (AI drafts the plan; you review it)
AI CHAT      /opsx:apply                      (AI builds it)
AI CHAT      /opsx:archive                    (specs updated, change filed away)
```

- `openspec init` 후 구조 (getting-started.md 원문 트리):

```text
openspec/
├── specs/              # Source of truth (your system's behavior)
│   └── <domain>/
│       └── spec.md
├── changes/            # Proposed updates (one folder per change)
│   └── <change-name>/
│       ├── proposal.md
│       ├── design.md
│       ├── tasks.md
│       └── specs/      # Delta specs (what's changing)
│           └── <domain>/
│               └── spec.md
└── config.yaml         # Project configuration (optional)
```

- 변경 폴더에는 선택 메타 파일 `.openspec.yaml`도 있다(`schema`, `created`, `skip_specs`, `retire_capabilities`, 사용자 `x-*` 키 — concepts.md).
- **2.0 예고 (v1.17.0, 2026-11-09)**: "command files (`/opsx:*`) go away in OpenSpec 2.0." 스킬은 남는다. 미리 바꾸려면 `openspec config set delivery skills && openspec update`. 계획은 이슈 #2022.
  - 실습서 영향: `/opsx:propose` 대신 스킬 표기(`/openspec-propose`)가 표준이 될 수 있다. 원고에서 두 표기를 함께 적을 것을 권장한다.
- 관련 섹션: OpenSpec 실습 장 준비

## 자료 14: OpenSpec — 슬래시 명령과 도구별 표기

- 출처: https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md , `docs/supported-tools.md`, `docs/cli.md`
- 저자·날짜: Fission AI(MIT). v1.17.0/2026-11-09 기준. 접근 2026-11-10.
- 신뢰성: 최상
- 기본 `core` 프로필 (원문 표):

| 명령 | 목적 |
|---|---|
| `/opsx:propose` | Create a change and generate planning artifacts in one step |
| `/opsx:explore` | Think through ideas before committing to a change |
| `/opsx:apply` | Implement tasks from the change |
| `/opsx:update` | Revise a change's planning artifacts and keep them coherent |
| `/opsx:sync` | Merge delta specs into main specs |
| `/opsx:archive` | Archive a completed change |

- 확장 프로필 (`openspec config profile`로 고른 뒤 `openspec update`): `/opsx:new`, `/opsx:continue`, `/opsx:ff`, `/opsx:verify`, `/opsx:bulk-archive`, `/opsx:onboard`.
- 기본 흐름 (getting-started.md): `/opsx:explore`(선택) → `/opsx:propose` → `/opsx:apply` → `/opsx:sync` → `/opsx:archive`. 확장 흐름: `/opsx:new` → `/opsx:ff` 또는 `/opsx:continue` → `/opsx:apply` → `/opsx:verify` → `/opsx:archive`.
- 도구별 표기 (commands.md 원문 표 요약):

| 명령 파일 형태 | 표기 | 예 |
|---|---|---|
| `.../commands/opsx/<id>.*` | `/opsx:propose` | Claude Code, Gemini CLI |
| `.../opsx-<id>.*` | `/opsx-propose` | Cursor, Devin Desktop, Copilot(IDE), Trae |
| 스킬만 | `/openspec-propose`, `/openspec-apply-change` | Zed Agent, 공유 `.agents` 등 |
| Codex CLI | `$openspec-propose` | Codex |

  - Claude Code 설치 위치: 스킬 `.claude/skills/openspec-*/SKILL.md`, 명령 `.claude/commands/opsx/<id>.md` (supported-tools.md).
  - Copilot CLI는 사용자 정의 프롬프트 파일을 지원하지 않아 IDE에서만 `/opsx-*`가 된다 (commands.md 주석).
- `/opsx:propose` 출력 예 (원문):

```text
You: /opsx:propose add-dark-mode

AI:  Created openspec/changes/add-dark-mode/
     ✓ proposal.md
     ✓ specs/ui/spec.md
     ✓ design.md
     ✓ tasks.md
     Ready for implementation. Run /opsx:apply.
```

- `/opsx:archive`가 하는 일 (원문 목록): 산출물 완료 확인 → 태스크 완료 확인(미완료면 경고만) → 델타 미동기화 시 동기화 제안 → `openspec/changes/archive/YYYY-MM-DD-<name>/`로 이동 → 감사 기록용으로 모든 산출물 보존.
  > "Archive won't block on incomplete tasks, but will warn"
- 레거시 명령: `/openspec:proposal`, `/openspec:apply`, `/openspec:archive` (아직 동작, OPSX 권장).
- CLI 명령 (cli.md 헤딩): `openspec init`, `update`, `list`, `view`, `show`, `validate`, `archive`, `new change`, `status`, `instructions`, `templates`, `schemas`, `schema init|fork|validate|which`, `config`, `store setup|register|...`, `feedback`, `completion`.
- 검증 규칙 변화 (릴리스 노트):
  - v1.16.0: `openspec validate`가 WHEN/GIVEN 단계나 THEN 단계가 없는 `Scenario:`를 경고, `--strict`면 실패.
  - v1.16.1: `## DEPRECATED Requirements`처럼 모르는 델타 절에 요구사항을 넣으면 `validate` 실패, `archive` 거부(전에는 경고 후 조용히 버림).
- 관련 섹션: OpenSpec 명령 한 장 요약표

## 자료 15: OpenSpec — 스펙·변경·델타 문서 형식

- 출처: https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md (마지막 커밋 2026-10-14), `docs/writing-specs.md`
- 저자·날짜: Fission AI(MIT). 접근 2026-11-10.
- 신뢰성: 최상
- 메인 스펙 형식 (`openspec/specs/<domain>/spec.md`, concepts.md 예시 발췌):

```markdown
# Auth Specification

## Purpose
Authentication and session management for the application.

## Requirements

### Requirement: User Authentication
The system SHALL issue a JWT token upon successful login.

#### Scenario: Valid credentials
- GIVEN a user with valid credentials
- WHEN the user submits login form
- THEN a JWT token is returned
- AND the user is redirected to dashboard
```

  - 요소 (원문 표): `## Purpose` = 도메인 개요, `### Requirement:` = 시스템이 가져야 할 동작, `#### Scenario:` = 그 동작의 구체 예, SHALL/MUST/SHOULD = RFC 2119 강도.
- `proposal.md` 헤딩 (concepts.md 예): `# Proposal: Add Dark Mode` → `## Intent` → `## Scope`(In scope / Out of scope) → `## Approach`
- `design.md` 헤딩 (concepts.md 예): `# Design: Add Dark Mode` → `## Technical Approach` → `## Architecture Decisions` → `### Decision: Context over Redux` … → `## Data Flow` → `## File Changes`
- `tasks.md` 형식 (concepts.md 예):

```markdown
# Tasks

## 1. Theme Infrastructure
- [ ] 1.1 Create ThemeContext with light/dark state
- [ ] 1.2 Add CSS custom properties for colors
```

  - 원문 모범 사례: 계층 번호(1.1, 1.2), 한 세션에 끝낼 크기, 태스크마다 검증 방법 명시, 테스트와 문서는 마지막 몰아치기 그룹이 아니라 각 그룹 안에.
- **델타 스펙** (`openspec/changes/<change>/specs/<domain>/spec.md`, concepts.md 예 발췌):

```markdown
# Delta for Auth

## ADDED Requirements

### Requirement: Two-Factor Authentication
The system MUST support TOTP-based two-factor authentication.

#### Scenario: 2FA enrollment
- GIVEN a user without 2FA enabled
- WHEN the user enables 2FA in settings
- THEN a QR code is displayed for authenticator app setup

## MODIFIED Requirements

### Requirement: Session Expiration
The system MUST expire sessions after 15 minutes of inactivity.
(Previously: 30 minutes)

## REMOVED Requirements

### Requirement: Remember Me
(Deprecated in favor of 2FA. Users should re-authenticate each session.)
```

- 아카이브 시 병합 규칙 (concepts.md 원문 표 요약):

| 절 | 의미 | 아카이브 때 |
|---|---|---|
| `## ADDED Requirements` | 새 동작 | 메인 스펙에 덧붙임 |
| `## MODIFIED Requirements` | 바뀐 동작 | 기존 요구사항을 **통째로** 교체 (전체 새 버전을 적어야 함) |
| `## REMOVED Requirements` | 없어질 동작 | 메인 스펙에서 삭제. 마지막 요구사항을 지우면 능력(capability)을 은퇴시키고 spec 파일을 지움 — 단 `.openspec.yaml`에 `retire_capabilities: true`가 있을 때만 |
| `## Purpose` | 새 능력의 목적 | 새 메인 스펙의 Purpose가 됨, 기존 스펙에서는 무시 |

  - `RENAMED` 절: `/opsx:sync` 설명이 "Parses ADDED/MODIFIED/REMOVED/RENAMED sections"라고 적는다(commands.md). concepts.md 표에는 없다. 문서 사이 불일치이므로 실습에서는 ADDED/MODIFIED/REMOVED 세 절만 가르치는 편이 안전하다.
- 좋은 요구사항 기준 (writing-specs.md 원문):
  > "One statement, one `SHALL`/`MUST`."
  > "The test for a requirement: *could a tester who's never seen the code tell whether it passed?*"
  > "A good change has one intent you can say in a sentence."
  - 체크리스트 6항 (원문): 요구사항마다 관찰 가능한 동작 하나, 구현 세부 없음, 요구사항마다 시나리오 하나 이상, 경계·오류 사례 시나리오, 델타 절 올바른 사용, 변경 하나 = 의도 하나.
- 관련 섹션: "OpenSpec으로 기존 코드 바꾸기" 실습, "MODIFIED는 전문을 다시 쓴다" 주의 박스

---

## 자료 16: cc-sdd — README (설치·플래그·흐름)

- 출처: https://github.com/gotalab/cc-sdd (README.md)
- 저자·날짜: gotalab(MIT). v3.1.0/2026-09-23 기준(마지막 푸시 2026-10-22). 접근 2026-11-10.
- 신뢰성: 최상
- 설치 (원문):

```bash
cd your-project
npx cc-sdd@latest                       # Claude Code Skills, 영어 문서 (기본)
npx cc-sdd@latest --codex-skills --lang ja
npx cc-sdd@latest --claude-skills --lang ko   # 한국어 (지원 언어 14개 중 ko 포함)
npx cc-sdd@latest --dry-run             # 적용 전 미리 보기
npx cc-sdd@latest --kiro-dir docs       # 스펙 폴더 위치 변경
```

  - 스킬 모드 플래그: `--claude-skills`, `--codex-skills`(안정), `--cursor-skills`, `--copilot-skills`, `--devin`, `--opencode-skills`, `--gemini-skills`, `--antigravity`(베타). 레거시 `/kiro:*` 명령 모드(`--claude`, `--cursor` 등)는 폐기 예정, `--codex`는 차단.
- 흐름 (원문 예):

```bash
/kiro-discovery Photo albums with upload, tagging, and sharing
/kiro-spec-init photo-albums
/kiro-spec-requirements photo-albums
/kiro-spec-design photo-albums
/kiro-spec-tasks photo-albums
/kiro-impl photo-albums
```

  - Codex는 `$kiro-*`, (구) Cascade는 `@kiro-*` 표기 (skill-reference.md).
- 상황별 경로 (원문 표 요약): 새 기능 = discovery → spec-init → requirements → design → tasks → impl / 기존 시스템 확장 = `kiro-steering` → discovery 또는 spec-init → (선택) `kiro-validate-gap` → design → tasks → impl / 큰 이니셔티브 = discovery → `kiro-spec-batch` / 스펙 없는 작은 변경 = discovery → 바로 구현.
- 인용 가능한 구절:
  > "Code remains the source of truth."
  > "Installing 17 skills does not verify that a host can run the full autonomous loop."
- 관련 섹션: "Claude Code에서 Kiro 방식 쓰기" 실습

## 자료 17: cc-sdd — 17개 스킬 목록과 역할

- 출처: https://github.com/gotalab/cc-sdd/blob/main/docs/guides/skill-reference.md , 스킬 디렉터리 `tools/cc-sdd/templates/agents/claude-code-skills/skills/`
- 저자·날짜: gotalab(MIT). 접근 2026-11-10, v3.1.0 기준.
- 신뢰성: 최상
- 설치되는 17개 스킬 (디렉터리 목록 그대로): `kiro-debug`, `kiro-discovery`, `kiro-impl`, `kiro-review`, `kiro-spec-batch`, `kiro-spec-design`, `kiro-spec-init`, `kiro-spec-quick`, `kiro-spec-requirements`, `kiro-spec-status`, `kiro-spec-tasks`, `kiro-steering-custom`, `kiro-steering`, `kiro-validate-design`, `kiro-validate-gap`, `kiro-validate-impl`, `kiro-verify-completion`

| 스킬 | 하는 일 (원문 요약) | 출력 |
|---|---|---|
| `/kiro-discovery` | 요청을 라우팅하고 범위를 다듬는다 | `brief.md`, 필요 시 `roadmap.md`, 다음 명령 제안 후 멈춤 |
| `/kiro-spec-batch` | 여러 스펙을 의존성 웨이브로 생성, 스펙 간 일관성 검토 | 여러 스펙 폴더 |
| `/kiro-impl` | 자율 모드(인자 없음, 반복당 태스크 1개, 구현자·리뷰어·디버거 새 컨텍스트) / 수동 모드(태스크 지정, 메인 컨텍스트 TDD + 리뷰 관문) | 코드, `tasks.md`의 `## Implementation Notes` |
| `/kiro-validate-impl` | 태스크 간 통합, 요구사항 커버리지, 설계 정합, 전체 테스트 증거 | `GO` / `NO-GO` / `MANUAL_VERIFY_REQUIRED` |
| `kiro-review` | 태스크 단위 적대적 리뷰 (스펙 준수, 경계, 기계 검증, RED 증거) | 판정 |
| `kiro-debug` | 근본 원인 우선 디버그 | `ROOT_CAUSE`, `CATEGORY`, `FIX_PLAN`, `NEXT_ACTION` |
| `kiro-verify-completion` | 성공 주장 전 새 증거 확인 | `VERIFIED` / `NOT_VERIFIED` / `MANUAL_VERIFY_REQUIRED` |
| `/kiro-steering`, `/kiro-steering-custom` | 프로젝트 기억(스티어링) 생성 | `.kiro/steering/*.md` |

- 관련 섹션: cc-sdd 명령표

## 자료 18: cc-sdd — 스펙 템플릿과 EARS 규칙, 실제 예

- 출처: `tools/cc-sdd/templates/shared/settings/templates/specs/`(`requirements.md`, `design.md`, `tasks.md`, `init.json`, `research.md`, `requirements-init.md`), `.../settings/rules/ears-format.md`, 예시 https://github.com/gotalab/cc-sdd/tree/main/.kiro/specs/photo-albums-en
- 저자·날짜: gotalab(MIT). 예시 폴더 마지막 커밋 2025-09-07(v3 이전 → **구버전 형식일 수 있음**, `_Boundary:_` 표기 없음). 템플릿은 v3.1.0 기준. 접근 2026-11-10.
- 신뢰성: 최상(템플릿) / 중(예시는 구버전)
- 생성 위치: `.kiro/specs/<feature>/` 아래 `requirements.md`, `design.md`, `tasks.md`, `spec.json`(+ discovery의 `brief.md`, `roadmap.md`). 사용자 정의는 `{{KIRO_DIR}}/settings/templates/`(문서 구조)와 `settings/rules/`(생성 원칙).
- `spec.json` 승인 상태 (init.json 원문 구조): `"phase": "initialized"`, `"approvals"` 아래 `requirements`/`design`/`tasks` 각각 `{"generated": false, "approved": false}`, `"ready_for_implementation": false`. — 단계 관문이 파일로 기록된다.
- `requirements.md` 템플릿 헤딩: `# Requirements Document` → `## Introduction` → `## Boundary Context (Optional)` → `## Requirements` → `### Requirement 1: {{REQUIREMENT_AREA_1}}` → `**Objective:** As a {{ROLE}}, I want {{CAPABILITY}}, so that {{BENEFIT}}` → `#### Acceptance Criteria`
  - 템플릿의 수용 기준 자리 (원문):

```markdown
1. When [event], the [system] shall [response/action]
2. If [trigger], then the [system] shall [response/action]
3. While [precondition], the [system] shall [response/action]
4. Where [feature is included], the [system] shall [response/action]
5. The [system] shall [response/action]
```

  - 템플릿 주석: 요구사항 제목은 숫자 ID만 허용("Requirement A" 금지).
- `design.md` 템플릿 주요 헤딩: Overview(Goals, Non-Goals) / **Boundary Commitments**(This Spec Owns, Out of Boundary, Allowed Dependencies, Revalidation Triggers) / Architecture / Technology Stack / **File Structure Plan**(Directory Structure, Modified Files) / System Flows / **Requirements Traceability** / Components and Interfaces(Service Interface, API Contract, Event Contract, Batch/Job Contract, State Management) / Data Models
  > "This section directly drives task `_Boundary:_` annotations and implementation Task Briefs."
- `tasks.md` 템플릿 (원문):

```markdown
- [ ] {{NUMBER}}.{{PARALLEL_MARK}} {{TASK_DESCRIPTION}}
  - _Boundary: {{COMPONENT_NAMES}}_ (Only for (P) tasks. Omit when scope is obvious.)
  - _Depends: {{TASK_IDS}}_ (Only for non-obvious cross-boundary dependencies. Most tasks omit this.)
  - _Requirements: {{REQUIREMENT_IDS}}_ (IDs only; do not add descriptions or parentheses.)
```

- EARS 규칙 파일의 다국어 지침 (ears-format.md 원문 요약): 트리거 키워드와 고정 구(`When`, `If`, `While`, `Where`, `The system shall`)는 **영어로 두고**, 변수 부분만 대상 언어로 쓴다. 주어는 구체 시스템 이름(예 "Checkout Service")을 쓴다. 복합형 `While [precondition], when [event], the [system] shall ...`도 허용.
  - 한국어 책에 바로 쓸 수 있는 규칙이다. 예: `When 사용자가 결제 버튼을 누르면, the Checkout Service shall 장바구니 내용을 검증한다` 같은 혼용 형식이 이 규칙의 결과다(예문은 본 리서처가 규칙에 맞춰 만든 것, 출처 문장 아님).
- 실제 예 (photo-albums-en/requirements.md 발췌, 구버전 표기):

```markdown
### Requirement 1: Album Management
**Objective:** As a user, I want to create and manage photo albums grouped by date, so that I can organize my photos chronologically and find them easily.

#### Acceptance Criteria

1. WHEN a user creates a new album THEN the Photo Album Application SHALL associate the album with a creation date
3. IF an album contains no photos THEN the Photo Album Application SHALL allow the user to delete the album
```

  - 같은 파일의 2번 요구사항에는 `WHILE dragging an album THE Photo Album Application SHALL ...`, `WHERE drag and drop is active THE ...`도 있다. 다섯 패턴이 한 문서에 다 나오는 좋은 교재다. 단 `WHEN ... THEN ... SHALL`은 현재 템플릿(`When ..., the ... shall`)과 다르다.
- 관련 섹션: "EARS를 한국어로 쓸 때" 박스, cc-sdd 실습

---

## 자료 19: BMAD Method — README (안정판과 v7 알파의 두 갈래)

- 출처: https://github.com/bmad-code-org/BMAD-METHOD (main 브랜치 README.md)
- 저자·날짜: BMad Code, LLC(MIT + 상표). 안정판 v6.12.4/2026-10-14, v7은 미리보기 알파(README: 출시 예정 2026-11 중순). 접근 2026-11-10.
- 신뢰성: 최상
- 안정판 v6.12 설치 (원문): Node.js 20.12+, Python 3.10+, uv 필요.

```bash
npx bmad-method install
# 헤드리스 CI 예 (docs/start/install-bmad.md, V6.12 브랜치)
npx bmad-method install --yes --modules bmm --tools claude-code
npx bmad-method install --list-tools
npx bmad-method@next install      # 프리릴리스
```

  - README: 설치 후 AI 도구에서 `bmad-build`로 바꿀 것을 말하고, 다음 단계를 모르면 `bmad-help`를 부른다. 설치 결과는 `_bmad/` 디렉터리.
- v7 미리보기 알파 설치 (원문):

```bash
npx skills add bmad-code-org/BMAD-METHOD --skill '*'
# Claude Code 안에서
/plugin marketplace add bmad-code-org/bmad-plugins
# Codex
codex plugin marketplace add bmad-code-org/bmad-plugins
```

  - v7은 `bmad` 허브 스킬에 `bmad setup`, `bmad status`를 요청한다. 산출물 기본 폴더 `_bmad-output`(main 브랜치 docs).
  > "Expect breaking changes between updates."
- 관련 섹션: BMAD 소개 장, "어느 판으로 실습할까" 결정 박스

## 자료 20: BMAD v6.12 — 스킬·에이전트 레퍼런스와 산출물

- 출처: https://github.com/bmad-code-org/BMAD-METHOD/blob/V6.12/docs/reference/skills-and-agents.md , `docs/plan/choose-a-planning-path.md`, `docs/plan/define-requirements-and-a-specification.md` (모두 **V6.12 브랜치**). 한국어 문서: `docs/ko-kr/` (V6.12 브랜치에 존재)
- 저자·날짜: BMad Code, LLC. v6.12.4 기준. 접근 2026-11-10.
- 신뢰성: 최상
- 스킬 설치 위치 (원문 표): Claude Code `.claude/skills/`, Cursor·Windsurf·Codex·Auggie·Amp 등 `.agents/skills/`, Cline `.cline/skills/`, Antigravity `.agent/skills/`.
- 에이전트 5종 (원문 표):

| 에이전트 | 스킬 ID | 메뉴 코드 |
|---|---|---|
| Analyst (Mary) | `bmad-agent-analyst` | `BP`, `MR`, `DR`, `TR`, `TS`, `CR`, `UV`, `CB`, `WB`, `PC` |
| Product Manager (John) | `bmad-agent-pm` | `PRD`, `CE`, `IR`, `CC` |
| Architect (Winston) | `bmad-agent-architect` | `CA`, `IR` |
| Developer (Amelia) | `bmad-agent-dev` | `BD`, `QA`, `CR`, `SP`, `ER` |
| UX Designer (Sally) | `bmad-agent-ux-designer` | `CU` |

- 코어 스킬 8개: `bmad-help`, `bmad-advanced-elicitation`, `bmad-review`, `bmad-customize`, `bmad-brainstorming`, `bmad-deep-recon`, `bmad-forge-idea`, `bmad-party-mode`.
- 방법 스킬과 산출물 (choose-a-planning-path.md 원문 표 요약):

| 스킬 | 산출물 |
|---|---|
| `bmad-product-brief` | `brief.md` + `addendum.md` |
| `bmad-prfaq` | `prfaq-<project>.md` |
| `bmad-prd` | `prd.md`, `addendum.md`, `.memlog.md` (validate는 HTML + `.md` 보고서) |
| `bmad-ux` | `DESIGN.md`, `EXPERIENCE.md`, `.memlog.md` |
| **`bmad-spec`** | **`SPEC.md`** + `specs/spec-<slug>/` 아래 부속 파일, 요청 시 `stories.yaml` |
| `bmad-architecture` | 기본 `ARCHITECTURE-SPINE.md` |
| `bmad-create-epics-and-stories` | 에픽 파일과 스토리 |
| `bmad-sprint-planning` | PASS/CONCERNS/FAIL + `sprint-status.yaml` |
| `bmad-build` / `bmad-build-auto` | 코드(리뷰·검증 포함) / 무인 루프 1회 |

- v6.12의 `SPEC.md` 다섯 필드 (define-requirements 원문):
  > "`SPEC.md` has five fields: Why, Capabilities (each with an intent and a success condition), Constraints, Non-goals, and Success signal."
  - "`bmad-spec` is the only writer of `SPEC.md`. Do not hand-edit it" — 고치려면 스킬을 다시 돌려 능력 ID를 유지한 채 갱신한다.
  - 입력 상한 (원문): "a few tens of thousands of tokens is the practical ceiling" (약 40쪽).
- 경로 고르기 (원문 요약): 의도가 잘 정의되었으면 `bmad-spec`에 넣고 Build. 한 세션 크기면 바로 `bmad-build`, 에픽 크기면 Story Breakdown(`stories.yaml`) 후 스토리마다 Build, 약 20세션 이상이면 프로젝트 경로. "You don't need BMad for an obvious, low-risk edit."
- 옛 스킬 이름(`bmad-create-prd`, `bmad-edit-prd`, `bmad-generate-project-context` 등)은 새 스킬로 넘겨 주는 포워더로 남아 있다.
- **[보고서와 다름]** 보고서 2.7절의 역할·산출물 표(PO Sofia, `prd-<slug>.md`, `tickets.toml`)는 **v7 알파(main 브랜치·docs.bmad-method.org)** 의 내용이다. `npx bmad-method install`로 설치되는 안정판 v6.12에는 Sofia(`bmad-agent-po`)와 `tickets.toml`이 없고, 대신 `bmad-spec`/`SPEC.md`/`stories.yaml`이 있다. 공식 문서 사이트는 버전 배너 없이 v7 내용을 보여 준다(2026-11-10 확인: 사이트의 choose-a-planning-path에 Sofia·`tickets.toml`은 있고 `bmad-spec`·`SPEC.md`는 없음). 실습 장은 판을 명시해야 한다.
- 관련 섹션: BMAD 실습 장, "문서 사이트와 설치본이 다를 때" 주의 박스

---

## 자료 21: Superpowers — README (설치·7단계 기본 흐름)

- 출처: https://github.com/obra/superpowers (README.md), 릴리스 노트 https://github.com/obra/superpowers/releases
- 저자·날짜: Jesse Vincent / Prime Radiant(MIT). v7.0.2/2026-11-03 기준(v7.0.0 2026-10-10에 brainstorming 재작성). 접근 2026-11-10.
- 신뢰성: 최상
- 설치 (원문):

```bash
# Claude Code — 공식 마켓플레이스
/plugin install superpowers@claude-plugins-official
# 또는 Superpowers 마켓플레이스
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
# Cursor Agent 채팅
/add-plugin superpowers
# Codex CLI: /plugins 에서 superpowers 검색 후 Install Plugin
# Gemini CLI
gemini extensions install https://github.com/obra/superpowers
# GitHub Copilot CLI
copilot plugin marketplace add obra/superpowers-marketplace
copilot plugin install superpowers@superpowers-marketplace
```

- 슬래시 명령이 아니라 **자동 트리거 스킬**이다. 저장소에 `commands/` 디렉터리가 없다(2026-11-10 확인). 사용자가 `/brainstorming`처럼 스킬 이름으로 직접 부를 수도 있다(v7.0.1 릴리스 노트).
- 기본 흐름 (README "The Basic Workflow" 원문 요약):
  1. `brainstorming` — 만들기 전에 발동. 질문으로 의도와 이유를 끌어내고 이해한 바를 되읽어 준다. 작은 변경은 채팅에서 합의, 프로젝트는 설계 문서.
  2. `using-git-worktrees` — 설계 승인 뒤. 새 브랜치 격리 작업 공간, 깨끗한 테스트 기준선 확인.
  3. `writing-plans` — 2~5분 단위 태스크로 분해.
  4. `subagent-driven-development`(태스크마다 새 서브에이전트 + 리뷰, 가장 철저) 또는 `executing-plans`(현재 세션에서 인라인, 마지막에 브랜치 전체 리뷰 1회, 가장 저렴).
  5. `test-driven-development` — RED-GREEN-REFACTOR. 테스트 전에 쓴 코드는 지운다.
  6. `requesting-code-review` — 태스크 사이, 심각도별 보고, Critical은 진행을 막음.
  7. `finishing-a-development-branch` — 테스트 확인, merge/PR/keep/discard 선택, worktree 정리.
  > "**The agent checks for relevant skills before any task.** Mandatory workflows, not suggestions."
- 전체 스킬 (skills/ 디렉터리): `brainstorming`, `diagnosing-superpowers`, `dispatching-parallel-agents`, `executing-plans`, `finishing-a-development-branch`, `receiving-code-review`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `test-driven-development`, `using-git-worktrees`, `using-superpowers`, `verification-before-completion`, `writing-plans`, `writing-skills` (15개)
- 관련 섹션: Superpowers 실습 장

## 자료 22: Superpowers — 설계 문서와 구현 계획의 저장 위치·형식 (SKILL.md 원문)

- 출처: https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md , https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md (마지막 커밋 2026-09-25)
- 저자·날짜: Jesse Vincent(MIT). v7.0.2 기준. 접근 2026-11-10.
- 신뢰성: 최상
- 저장 위치 (원문):
  - 설계: `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`, committed. (사용자 선호가 우선)
  - 계획: `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- 설계 문서가 다룰 것 (brainstorming 원문 목록): intent and the why / goals, non-goals, anti-goals / constraints / approaches / the parts of the how they decided / what's left to the builder. 프로젝트 규모면 새 서브에이전트가 빌더 입장에서 읽는 **Builder check**를 거친다(v7.0.0에서 spec-document reviewer를 대체).
- 계획 문서 머리말 (writing-plans 원문 구조):

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. ...

**Goal:** [One sentence describing what this builds]
**Architecture:** [2-3 sentences about approach]
**Tech Stack:** [Key technologies/libraries]
**Spec:** [path to the spec/design doc this plan implements ...]

## Global Constraints
## Review Focus
```

- 태스크 구조 (writing-plans 원문 골격):

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [...]
- Produces: [...]

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run test to verify it fails**   (Run: `pytest ...` / Expected: FAIL ...)
- [ ] **Step 3: Implement `function(input: InputType) -> ResultType` in `exact/path/to/file.py`**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit**
```

- 코드 단계의 기준 (writing-plans 원문): "the exact signature (name, parameters, return type), the file it lives in, and the specific values the spec pins. The implementer writes the body."
  - **[보고서와 다름]** 보고서 3.2절은 README를 따라 "태스크마다 정확한 파일 경로, **완성 코드**, 검증 단계"라고 적었다. README 문구는 아직 "complete code"지만, 실제 `writing-plans` SKILL.md(2026-09-25)는 시그니처·파일·값만 주고 본문은 구현자가 쓰며, 코드 블록은 시그니처와 테스트로 정해지지 않는 알고리즘에만 둔다고 한다. 저장소 안에서 README와 스킬이 어긋난다. 실습 장은 SKILL.md를 기준으로 삼을 것.
- v7.0.2 brainstorming 변화 (릴리스 노트 원문 요약): 답이 결과를 바꿀 때만 묻는다. 이유를 말하지 않았으면 그것부터 묻는다. 선택지가 있으면 추천과 함께 보여 준다. 블라인드 채점 테스트에서 불필요한 질문이 41개(7.0.1)에서 23개로 줄었다(제조사 측정).
- 관련 섹션: "Superpowers가 남기는 문서 읽기" 실습

---

## 자료 23: mattpocock/skills — README (설치·스킬 목록)

- 출처: https://github.com/mattpocock/skills (README.md)
- 저자·날짜: Matt Pocock(MIT). v1.3.2/2026-10-29 기준(마지막 푸시 2026-11-09). 접근 2026-11-10.
- 신뢰성: 최상
- 설치 (원문, 에이전트마다 하나만 — 둘 다 설치하면 스킬이 두 번 보임):

```bash
# Claude Code (자동 업데이트)
claude plugin install mattpocock-skills@claude-plugins-official
# Codex
codex plugin marketplace add mattpocock/skills
codex plugin add mattpocock-skills@mattpocock
# GitHub Copilot (CLI, VS Code)
copilot plugin marketplace add mattpocock/skills
copilot plugin install mattpocock-skills@mattpocock
# Gemini CLI (수동 업데이트)
gemini skills install https://github.com/mattpocock/skills.git --path skills/engineering
gemini skills install https://github.com/mattpocock/skills.git --path skills/productivity
# 그 밖의 에이전트 / 편집 가능한 사본
npx skills@latest add mattpocock/skills -a <agent>   # cursor, opencode, devin, windsurf, amp, pi
```

- 설치 직후 저장소마다 한 번 `/setup-matt-pocock-skills`: 이슈 트래커(GitHub, GitLab, 로컬 파일 등), 트리아지 라벨, 문서 저장 위치를 묻는다.
- 스킬 분류 (README "Reference" 원문 요약): **사용자 호출**(직접 입력해야 실행, 오케스트레이션 담당)과 **모델 호출**(에이전트가 알아서 고를 수 있는 규율). 사용자 호출 스킬은 모델 호출 스킬을 부를 수 있지만 다른 사용자 호출 스킬은 부르지 않는다.
  - Engineering 사용자 호출: `ask-matt`, `grill-with-docs`, `triage`, `improve-codebase-architecture`, `setup-matt-pocock-skills`, `to-spec`, `to-tickets`, `implement`, `implement-spec`, `wayfinder`, `retro`
  - Engineering 모델 호출: `prototype`, `diagnosing-bugs`, `research`, `tdd`, `domain-modeling`, `codebase-design`, `code-review`, `pr`, `wizard`
  - Productivity 사용자 호출: `grill-me`, `handoff`, `teach`, `to-questionnaire`, `wait-what` / 모델 호출: `grilling`, `writing-for-agents`
- 공유 언어 파일 이름은 `GLOSSARY.md`다(README: 예시 링크의 `CONTEXT.md`는 이름 변경 전 커밋이라고 명시).
- 인용 가능한 구절:
  > "Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process."
- 관련 섹션: "프레임워크 없이 스킬만으로" 장

## 자료 24: mattpocock/skills — `/grill-me` 와 `/to-spec` 의 실제 내용

- 출처: https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md (마지막 커밋 2026-08-19), https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md
- 저자·날짜: Matt Pocock(MIT). 접근 2026-11-10.
- 신뢰성: 최상
- `grill-me` SKILL.md는 머리말 `disable-model-invocation: true`와 한 줄 본문("Call the Skill tool with "grilling".")뿐이다. 실제 인터뷰 규율은 모델 호출 스킬 `grilling`에 있다.
- `to-spec` 머리말: `disable-model-invocation: true`, 설명 "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed."
- `to-spec` 절차 (원문 요약): (1) 저장소 탐색, 용어집 어휘 사용, ADR 존중 → (2) 기능을 테스트할 **이음매(seam)** 를 스케치하고 사용자와 확인(가장 높은 곳, 가능하면 하나) → (3) 템플릿으로 스펙을 쓰고 이슈 트래커에 올리며 `ready-for-agent` 라벨.
  - 정리: 보고서 3.3절이 지적한 "소개문(모듈을 먼저 묻는다) vs 스킬 목록(인터뷰 없음)" 차이는 SKILL.md로 풀린다. 인터뷰는 하지 않지만 **테스트 이음매 하나는 사용자에게 확인**한다.
- `to-spec` 스펙 템플릿 헤딩 (원문):

```markdown
## Problem Statement
## Solution
## User Stories
1. As an <actor>, I want a <feature>, so that <benefit>
## Implementation Decisions
## Testing Decisions
## Out of Scope
## Further Notes
```

  - 원문 지침: User Stories는 "A LONG, numbered list", Implementation Decisions에는 "Do NOT include specific file paths or code snippets. They may end up being outdated very quickly." (프로토타입이 만든 상태 기계·스키마 같은 결정은 예외)
- 실습 흐름 제안 (도구 문서 조합, 추론): `/grill-with-docs`로 인터뷰 + `GLOSSARY.md`/ADR 갱신 → `/to-spec`으로 이슈 등록 → `/to-tickets`로 블로킹 관계가 있는 티켓 분해 → `/implement` 또는 `/implement-spec`.
- 관련 섹션: "인터뷰로 스펙 끌어내기" 실습

---

## 자료 25: Anthropic — Claude Code 모범 사례의 "인터뷰 → SPEC.md → 새 세션"

- 출처: https://code.claude.com/docs/en/best-practices (원본 `.md`)
- 저자·날짜: Anthropic. 페이지 날짜 없음. 접근 2026-11-10 (문서는 기본 모델을 Opus 5.5로 서술 — 2026-11 시점 문서).
- 신뢰성: 최상 (제조사 공식 문서)
- 핵심 주장: 원하는 것을 아직 모르면 프롬프트를 다듬지 말고 Claude에게 인터뷰를 시키고, 결과를 `SPEC.md`로 남긴 뒤 **새 세션**에서 구현하고, 같은 파일로 리뷰한다. 프레임워크 없는 SDD의 1차 근거다.
- 인터뷰 프롬프트 (원문 예):

```text
I want to add rate limiting to the public API but haven't thought it through yet. Interview me until you could write the spec, then write it to SPEC.md.
```

- 짧은 인용 (원문):
  > "Once `SPEC.md` exists, start a fresh session to build from it"
  - 이어지는 설명: 새 세션은 깨끗한 컨텍스트와 글로 적힌 완료 정의로 시작한다. 같은 파일을 나중에 리뷰어에게 가리킨다. Claude는 사용자별 대 키별 제한, 초과 요청 처리, 범위 밖 항목 같은 객관식 질문을 한다.
- 스펙 기준 리뷰 프롬프트 (원문 예):

```text
use a subagent to review the rate limiter diff against SPEC.md, check every requirement is implemented and the listed edge cases have tests, report gaps that affect correctness and skip style
```

  - 원문 주의: `skip style`을 빼지 말 것. 문제를 찾으라는 리뷰어는 늘 무언가를 찾고, 그걸 다 고치면 불필요한 추상화와 일어날 수 없는 경우의 테스트가 생긴다.
- 함께 쓰는 지침 (같은 문서): CLAUDE.md는 짧게(검증 명령, 오해하기 쉬운 코드, 저장소에 없는 결정, 두 번 고친 것). 리뷰는 대화를 못 본 새 서브에이전트(`/code-review`)로. 완료 주장에는 증거(실행한 명령과 출력)를 요구. `/verify`로 앱을 빌드·실행해 확인.
- 관련 섹션: "도구 없이 SDD 하기" 장의 뼈대

## 자료 26: Anthropic — Claude Code 플랜 모드 상세

- 출처: https://code.claude.com/docs/en/permission-modes (§ Analyze before you edit with plan mode), https://code.claude.com/docs/en/common-workflows (§ Plan before editing), https://code.claude.com/docs/en/settings-reference (`plansDirectory`, `showClearContextOnPlanAccept`)
- 저자·날짜: Anthropic. 날짜 없음. 접근 2026-11-10. 로컬 설치본 Claude Code 2.1.319.
- 신뢰성: 최상
- 진입 (원문 요약): `Shift+Tab`으로 모드 순환(`default` → `acceptEdits` → `plan`, auto에서 시작하면 첫 누름이 default), **또는 한 프롬프트 앞에 `/plan`**, 또는 `claude --permission-mode plan`. 상태 표시줄 `⏸ plan mode on`. 다시 `Shift+Tab`이면 승인 없이 나간다.
- 계획 중 동작: 파일을 읽고 탐색용 셸 명령을 실행하고 계획을 쓰지만 소스는 고치지 않는다. 셸 명령은 auto 모드 사용 가능 + `useAutoModeDuringPlan`(기본 켜짐)이면 분류기가 판정, 아니면 읽기 전용 목록 밖 명령은 승인을 묻는다.
- 승인 선택지 (원문): **Yes, and use auto mode**(auto 불가면 **Yes, auto-accept edits**) / **Yes, manually approve edits** / **No, keep planning**. `Ctrl+G`로 계획을 텍스트 편집기에서 직접 고친다.
- `showClearContextOnPlanAccept`를 켜면 첫 선택지 **Yes, clear context and …**가 생겨 계획을 승인하고 대화 컨텍스트를 비운 채 **계획만으로** 구현을 시작한다(자료 25의 "새 세션"을 한 세션 안에서 하는 방법).
- 계획 파일 위치 (settings-reference 원문 요약): 기본값은 `~/.claude/plans`. `plansDirectory`(예 `"./plans"`)로 프로젝트 루트 기준 경로를 정할 수 있다. 루트 밖 경로나 macOS·Linux에서 백슬래시가 든 경로는 무시되고 `~/.claude/plans`로 간다.
- 기본 모드로: `.claude/settings.json`에 `defaultMode: "plan"`. VS Code 확장은 사용자 설정 `claudeCode.initialPermissionMode: "plan"`.
- **[보고서와 다름]** 보고서 4절 비교표는 Claude Code 플랜 모드의 기본 위치를 "세션 안", 진입을 "`--permission-mode plan`, Shift+Tab"으로 적었다. 실제로는 계획이 **파일로** `~/.claude/plans`에 저장되고, `plansDirectory`로 저장소 안에 둘 수 있으며, `/plan` 접두 진입도 있다. "저장소에 기본 저장 = 아니오"는 맞다.
- 관련 섹션: "플랜 모드를 가장 작은 SDD로 쓰기" 실습

## 자료 27: 다른 하네스의 네이티브 플랜 모드 (짧게)

- 출처와 날짜 (모두 접근 2026-11-10):
  - Cursor: https://cursor.com/docs/agent/plan-mode (날짜 없음)
  - VS Code Copilot: https://code.visualstudio.com/docs/agents/run/planning (바닥글 날짜 2026-11-04)
  - Codex CLI: https://developers.openai.com/codex/cli/slash-commands (원본 `.md`, 날짜 없음)
- 신뢰성: 최상 (각 제조사 문서)

| 하네스 | 진입 | 동작 | 계획 저장 | 출처 |
|---|---|---|---|---|
| Cursor | 채팅 입력에서 `Shift+Tab`으로 Plan Mode, 또는 모드 선택기 | 명확화 질문 → 코드베이스 조사 → 편집 가능한 계획 → 버튼으로 build | 기본 홈 디렉터리, **Save to workspace**로 작업 공간에 저장 | Cursor 문서 |
| VS Code Copilot | `/plan` + 원하는 결과·제약·검증 방법, 또는 Local에서 에이전트 목록의 **Plan** | 구현 단계, 관련 파일, 검증 단계 | Local: 세션 메모리 `/memories/session/plan.md`(프로젝트 파일 아님). Copilot 하네스: 문서에 위치 없음, 사본 저장 후 새 세션에 첨부 | VS Code 문서 |
| Codex CLI | `/plan` (선택적으로 인라인 프롬프트, 이미지·붙여넣기 가능) | "Ask Codex to propose an execution plan before implementation work starts." 작업 중에는 `/plan` 사용 불가 | 공식 페이지에 없음 | Codex 문서 |

- 인계 선택지: VS Code Copilot 하네스는 Implement Plan / Approve Plan Only / Implement with Autopilot / Reject, Local은 Start Implementation과 "Continue in" 목적지, Open in Editor(편집 가능한 무제 사본).
- Codex 플랜 모드의 모드 개수·승인 후 흐름·`Shift+Tab` 지원은 커뮤니티 글(deepakness.com, codex.danielvaughan.com 등)에만 있고 서로 다르다. 공식 문서로 확인한 것은 `/plan` 명령뿐이다.
- **[보고서와 다름]** 보고서 4절 Codex 항목은 "이 보고서가 출처로 등록한 Codex 문서는 플랜 모드를 다루지 않습니다"라며 비교표에서 Codex를 뺐다. 공식 Codex CLI 슬래시 명령 문서에 `/plan`("Switch to plan mode and optionally send a prompt.")이 있다.
- 관련 섹션: 하네스별 플랜 모드 비교 박스

---

## 보고서(sdd-report.md)와 1차 출처가 어긋나는 지점 모음

| # | 보고서 위치 | 보고서 서술 | 1차 출처 (2026-11-10) | 판정 |
|---|---|---|---|---|
| 1 | 4절 매트릭스 OpenSpec 설치 | `npm install -g @fission-ai/openspec@latest` 후 `openspec init` | v1.15.0(2026-10-24)부터 기본 설치는 독립 실행 파일 `curl -fsSL .../scripts/binary/install.sh \| sh`. npm은 대안이며 v1.16.0부터 Node.js 22.12.0+ 필요 | 낡음 |
| 2 | 2.6절 OpenSpec 단계 | 4단계(explore, propose, apply, archive), 확장에 new·continue·ff·verify·bulk-archive·onboard | 기본 `core` 프로필은 6개(propose, explore, apply, **update**, **sync**, archive) | 불완전 |
| 3 | 2.6절 OpenSpec 명령 표기 | `/opsx:*` 명령 중심 | v1.17.0(2026-11-09): `/opsx:*` 명령 파일은 2.0에서 사라지고 스킬만 남는다고 공지 | 곧 낡음 |
| 4 | 2.6절·4절 버전 | OpenSpec v1.16.1, Spec Kit v1.3.2 | OpenSpec v1.17.0(2026-11-09), Spec Kit v1.3.3(2026-11-09) | 검증일 이후 갱신 |
| 5 | 2.7절 BMAD 역할·산출물 | PO Sofia, `prd-<slug>.md`, `tickets.toml`, PM 계획 문서 11개 | 이 내용은 v7 알파(main·문서 사이트). 안정판 v6.12(`npx bmad-method install`)는 에이전트 5종(Sofia 없음), `bmad-spec` → `SPEC.md` + `stories.yaml`, `prd.md` | 판 혼동 |
| 6 | 3.2절 Superpowers 계획 | 태스크마다 정확한 파일 경로, **완성 코드**, 검증 단계 | `writing-plans` SKILL.md(2026-09-25): 시그니처·파일·값만, 본문은 구현자가 씀. README 문구만 "complete code"로 남음 | 저장소 내부 불일치, 스킬 기준으로 고칠 것 |
| 7 | 4절 Claude Code 플랜 모드 | 진입 `--permission-mode plan`, Shift+Tab / 위치 "세션 안" | `/plan` 접두 진입 추가. 계획은 `~/.claude/plans`에 파일로 저장, `plansDirectory`로 저장소 안 지정 가능. `showClearContextOnPlanAccept`로 컨텍스트 비우고 구현 | 불완전 |
| 8 | 4절 Codex | Codex 문서는 플랜 모드를 다루지 않음, 비교표에 Codex 행 없음 | 공식 Codex CLI 슬래시 명령 문서에 `/plan` 있음 | 낡음 또는 누락 |
| 9 | 4절 Kiro 표면표 | Plan 모드 CLI "확인 안 됨" | Kiro Plan 문서 표: IDE ✓, CLI ✓(`Shift+Tab`, `/plan`) | 낡음 |
| 10 | 2.2절 Kiro 실행 | (CLI 스펙 명령 언급 없음) | Kiro CLI: `/spec new <name>`, `/spec run <name>`, `/spec <name>`, 단계마다 `Ctrl+X` 리뷰 | 누락(실습에 필요) |
| 11 | 2.1절 Spec Kit 헌법 | `memory/constitution.md`는 Test-First 같은 **조항 9개**를 담는다 | 템플릿은 원칙 칸 5개 + 절 2개 + Governance. "9개 조항"은 `spec-driven.md`의 설명틀이며 IV~VI는 프로젝트가 정의 | 표현 보정 필요 |
| 12 | 2.1절 Spec Kit 경로 | `memory/constitution.md` | 실제 경로는 `.specify/memory/constitution.md` | 경로 보정 |
| 13 | 3.3절 mattpocock `/to-spec` | 소개문(모듈을 먼저 묻는다)과 목록(인터뷰 없음)이 다르다 | SKILL.md: 인터뷰는 안 하지만 테스트 이음매는 사용자에게 확인. 소개문과 목록 모두 부분적으로 맞음 | 해소 |

문서끼리 어긋나는 지점 (보고서와 무관, 원고에서 주의):
- Spec Kit `spec-driven.md` 예시는 아직 "Creates branch 003-chat-system"이라고 적지만 현재 `specify` 명령은 브랜치를 선택 훅으로만 만든다.
- OpenSpec `commands.md`의 `/opsx:sync` 설명은 RENAMED 절을 언급하지만 `concepts.md` 델타 표에는 없다.
- Kiro Specs 개요 표는 Analyze Requirements Web을 "—"로 둔다(보고서도 이 불일치를 이미 기록함).
- BMAD 문서 사이트(docs.bmad-method.org)는 버전 배너 없이 v7 알파 내용을 보여 준다. 안정판 문서는 GitHub `V6.12` 브랜치의 `docs/`에 있다.

---

## 한국어 자료

이 주제의 실습 정보는 영어 1차 출처가 압도적이다. 한국어로 바로 쓸 수 있는 **공식** 자료는 아래뿐이다.
- Spec Kit 한국어 README: https://github.com/github/spec-kit/blob/main/README.ko.md (2026-11-04 커밋, 영어판과 같은 날 갱신, 명령 예시 동일)
- BMAD 한국어 문서: https://github.com/bmad-code-org/BMAD-METHOD/tree/V6.12/docs/ko-kr (안정판 v6.12 브랜치)
- cc-sdd 한국어 산출물: `npx cc-sdd@latest --lang ko` (지원 언어 14개에 ko 포함)
- 한국어 블로그 사용기는 검색에서 1건(mjoo1106.tistory.com, OpenSpec) 정도로 얕았다. 커뮤니티 리서처 영역이므로 여기서는 수집하지 않았다.

---

## 수집 한계

- 접근 실패·미확인: Kiro 문서 페이지 대부분에 갱신일 표기가 없다(feature-specs 상위 페이지만 2026-08-04). Kiro가 생성하는 `requirements.md`/`design.md`/`tasks.md`의 **공식 헤딩 템플릿**은 문서에 없어 공개 저장소(shuk) 실사용 예로 대신했다. Codex 플랜 모드의 승인 흐름은 공식 문서에서 확인하지 못했다(`/plan` 존재만 확인). Cursor 플랜의 정확한 기본 경로(홈 디렉터리 아래 어디인지)는 문서에 없다.
- 의도적으로 제외: 커뮤니티 후기·벤치마크·비교 글(커뮤니티 리서처 영역), 논문(논문 리서처 영역), 보고서가 이미 다룬 지형도·채택 지표.
- 원고 확정 전 재확인 권장: Spec Kit·OpenSpec 릴리스(하루 단위로 바뀜), BMAD v7 정식 출시(README 예정 2026-11 중순)와 그에 따른 설치 명령·산출물 변경, OpenSpec 2.0의 명령 파일 제거.
