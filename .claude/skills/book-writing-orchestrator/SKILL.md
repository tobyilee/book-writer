---
name: book-writing-orchestrator
description: Orchestrate a full book-writing workflow from topic to finished EPUB with cover image. Use when the user asks to "write a book", "draft a book", "author a book", "책 쓰기", "책 저술해줘", "책 만들어줘", "전자책 만들어줘", "EPUB 생성", provides a topic/audience/outline and asks to turn it into a book, or says "~에 대한 책을 써줘". Also triggers on follow-ups like "다시 저술", "계획 수정", "챕터 다시 써줘", "표지 바꿔", "책 업데이트", "특정 챕터 보완", "이전 책 개선", "리서치만 다시". Coordinates research, planning, review, chapter writing in Toby's style, style enforcement, editing, cover design, and EPUB assembly. Author is always Toby-AI.
---

# Book Writing Orchestrator

주제·주요 내용·대상 독자를 받아 Toby 스타일의 완성된 EPUB을 산출하는 전 과정을 조율한다. 각 Phase에서 전문 에이전트를 호출하고, 중간 산출물을 `{slug}/` 하위에 축적한 뒤 최종 EPUB을 프로젝트 루트에 만든다.

## 실행 모드

| Phase | 모드 | 왜 이렇게 |
|-------|------|----------|
| 1. 리서치 | 서브 에이전트(팬아웃) | 소스별 독립 수집 → 병렬화가 이득 |
| 2. 저술 계획 | 단일 서브 | 통합적 사고가 필요, 분할 이점 없음 |
| 3. 계획 리뷰 | 에이전트 팀(생성-검증 왕복) | 저자와 리뷰어의 토론이 품질을 높임 |
| 4. 챕터 저술 | **에이전트 팀** | 챕터 저술가 ↔ 스타일 가디언 ↔ 편집자 실시간 조율 |
| 5. 표지 + EPUB | 서브(병렬) | 독립 작업, 결과만 수집 |

## Phase 0: 컨텍스트 확인

워크플로우를 시작하기 전에 기존 산출물 존재 여부를 확인한다.

1. 사용자 입력에서 **주제, 주요 내용, 대상 독자**를 추출한다. 셋 중 하나라도 불명확하면 사용자에게 짧게 질문한다 (AskUserQuestion 사용).
2. 책 제목 후보(슬러그 포함)를 만든다. 예: `AI 시대의 개발자 철학` → 슬러그 `ai-developer-philosophy`.
3. `{slug}/`의 존재 여부를 확인한다.
   - **미존재** → 초기 실행, Phase 1부터 순차 실행
   - **존재 + 사용자가 부분 수정 요청** (예: "챕터 3만 다시", "계획만 수정") → 부분 재실행, 해당 Phase만 재호출
   - **존재 + 새 입력 제공** → 기존 `{slug}/`를 `{slug}_prev-{timestamp}/`로 이동 후 새 실행

## Phase 1: 리서치 (팬아웃)

**실행 모드:** 서브 에이전트 병렬 호출

`research-lead` 에이전트를 호출하고, 내부에서 `web-researcher`, `paper-researcher`, `community-researcher`를 `run_in_background: true`로 병렬 스폰한 뒤 결과를 종합하도록 지시한다.

**입력:** 주제, 주요 내용, 대상 독자
**출력:** `{slug}/01_reference.md` — 리서치 종합 문서 (섹션: 개념·정의, 주요 관점, 사례, 논쟁점, 참고문헌)

Agent 도구 호출 시 반드시 `model: "opus"`를 명시한다.

## Phase 2: 저술 계획

**실행 모드:** 단일 서브 에이전트

`book-planner` 에이전트를 호출한다.

**입력:** 주제, 주요 내용, 대상 독자, `{slug}/01_reference.md`
**출력:** `{slug}/02_plan.md` — 책 구조 설계 문서
- 책 제목 후보 3개
- 책 특성 (장르, 분량, 난이도, 독자 여정)
- 챕터 목록 (번호, 제목, 핵심 질문, 주요 내용, 예상 분량)
- 챕터 간 흐름(내러티브 아크)

## Phase 3: 계획 리뷰 (팀)

**실행 모드:** 에이전트 팀 (생성-검증 왕복)

`TeamCreate`로 `book-planner`와 `plan-reviewer`를 팀으로 구성한다. `plan-reviewer`가 계획을 비판적으로 읽고 `SendMessage`로 `book-planner`에게 피드백을 보낸다. `book-planner`는 피드백을 반영해 계획을 갱신한다. 합의에 도달하거나 최대 2회 왕복 후 팀을 해체한다.

**산출물:** `{slug}/02_plan.md` (갱신됨) + `{slug}/03_review_log.md` (리뷰 기록)

팀 해체 후 사용자에게 최종 계획을 제시하고 승인을 받는다. 사용자 피드백이 있으면 `book-planner`를 한 번 더 호출해 반영한다.

## Phase 4: 챕터 저술 (에이전트 팀)

**실행 모드:** 에이전트 팀 (핵심 Phase)

가장 중요한 Phase다. 팀 구성:

- `chapter-writer` × N (N = min(챕터 수, 3)) — 챕터별 저술
- `style-guardian` × 1 — 실시간 스타일 검수
- `editor` × 1 — 챕터 간 전환·일관성 관리

**절차:**

1. `TeamCreate`로 위 팀을 구성한다. 팀 이름: `book-writing-team`.
2. `TaskCreate`로 각 챕터를 task로 등록한다. task당 `chapter-writer` 1명을 할당한다.
3. 각 `chapter-writer`는 자기 챕터 초안을 쓰고 `{slug}/chapters/{NN}_draft.md`에 저장한 뒤 `SendMessage`로 `style-guardian`에게 리뷰를 요청한다.
4. `style-guardian`은 Toby 스타일 기준(평어체, 청유형, 수사적 질문, 공감 표현 등)으로 검수하고, 편차가 있으면 구체적 수정 제안을 작성해 `SendMessage`로 응답한다.
5. `chapter-writer`가 수정하고 `{NN}_final.md`로 저장한다.
6. 모든 챕터 완료 후 `editor`가 전환부를 점검하고 `{slug}/04_manuscript.md`에 통합 원고를 만든다.
7. 팀을 해체한다.

**챕터 수가 3개를 초과하면** chapter-writer를 챕터 수만큼 만들지 않고, 3명으로 시작해 각자 여러 챕터를 순차 처리한다(풀 방식). 너무 많은 팀원은 조율 오버헤드를 만든다.

**스타일 가이드:** `toby-book-writing-style.md`를 모든 chapter-writer가 참조한다. `chapter-writing` 스킬 내 `references/toby-style-guide.md`에 확장된 가이드가 있다.

## Phase 5: 표지 + EPUB 빌드 (팬아웃)

**실행 모드:** 서브 에이전트 병렬 호출

두 작업이 독립적이므로 병렬로 호출한다.

- `cover-designer` → 표지 이미지 생성, `{slug}/cover.png` 저장
- `epub-builder`는 cover가 준비된 후에 호출 (순서 의존) → `{책-제목}-v{version}.epub` 생성 (프로젝트 루트)

**EPUB 메타데이터:**
- 저자: `Toby-AI` (고정)
- 제목: Phase 2에서 확정된 책 제목
- 버전: 초기 실행 시 `1.0.0`, 재실행 시 사용자 요청에 따라 증가 (예: `1.1.0`)
- 언어: `ko`

## 에러 핸들링

| 시나리오 | 대응 |
|---------|------|
| 리서치 에이전트 하나가 실패 | 1회 재시도, 재실패 시 해당 섹션 누락 명시하고 진행 |
| 스타일 가디언과 챕터 저술가가 3회 왕복에도 합의 실패 | 저술가의 최종본을 채택하고 reviewlog에 기록 |
| 표지 생성 실패 | 플레이스홀더 이미지(검은 배경 + 제목 텍스트)로 대체, 사용자에게 알림 |
| EPUB 빌드 실패 | pandoc 에러 메시지 그대로 보고, 원고 마크다운은 보존 |

## 데이터 전달 프로토콜

| 전략 | 용도 |
|------|------|
| 파일 기반 (`{slug}/`) | 모든 Phase 간 산출물 전달, 감사 추적 |
| 메시지 기반 (SendMessage) | Phase 3·4의 팀 내 실시간 조율 |
| 태스크 기반 (TaskCreate) | Phase 4의 챕터 작업 할당 및 진행 추적 |
| 반환값 기반 | 서브 에이전트 모드(Phase 1·2·5)의 결과 수집 |

파일명 컨벤션: `{NN}_{artifact}.md` (NN은 Phase 번호 2자리).

## 실행 후 피드백

모든 Phase 완료 및 EPUB 산출 후:
1. 사용자에게 EPUB 경로와 요약 보고
2. "개선할 부분이 있나요?"를 짧게 물어본다 (강요하지 않음)
3. 피드백이 오면 Phase 7-2 매트릭스에 따라 해당 Phase만 재실행

## 테스트 시나리오

**정상 흐름:** 주제 "효과적인 SQL 쿼리 튜닝", 대상 "백엔드 주니어 개발자", 분량 "150페이지" → 리서치 → 5~7개 챕터 계획 → 리뷰 반영 → 챕터 저술 → EPUB 생성

**에러 흐름:** community-researcher가 timeout → 웹/논문 결과만으로 reference.md 작성, 리서치 범위 제한 명시 → 이후 Phase 정상 진행
