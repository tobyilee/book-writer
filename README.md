# Book Writer — AI 책 저술 자동화 하네스

[![Version](https://img.shields.io/badge/harness-v2.1.0-blue.svg)](VERSION) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Books: CC BY-NC-SA 4.0](https://img.shields.io/badge/books-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

주제, 주요 내용, 대상 독자만 주면 리서치부터 EPUB 빌드까지 한 번에 수행하는 **에이전트 하네스**다. v1.3.0부터 **장르별 문체 프로필**을 지원한다 — 기술서(Toby 문체)·소설·실용서(요리/여행)·에세이. 장르는 자동 감지 후 확인하며, 기본값은 `tech-book`이다 (아래 [장르 프로필](#장르-프로필) 참고). 저자명은 기본값 `Toby-AI`에서 원하는 값으로 바꿀 수 있다 (아래 [저자명 변경](#저자명-변경) 참고).

- **Repo:** https://github.com/tobyilee/book-writer
- **하네스 버전:** `v2.1.0` (단일 출처: 프로젝트 루트 [`VERSION`](VERSION). 변경 이력은 [CLAUDE.md](CLAUDE.md#변경-이력) 참조)
- **라이선스:** 하네스 코드는 **MIT** ([`LICENSE`](LICENSE)). 산출되는 책 콘텐츠 기본값은 **CC BY-NC-SA 4.0** — `book_manifest.json`의 `license` 필드로 책별 오버라이드 가능
- **실행 환경:** [Claude Code](https://claude.com/claude-code) + Claude Agent SDK
- **저자 모델:** 모든 에이전트가 현재 세션의 모델 설정을 그대로 상속한다 (에이전트별 `model` 고정 없음)

> **버전 두 개를 헷갈리지 말자.** 위 *하네스 버전*(단일 출처 [`VERSION`](VERSION) 기준, 이 도구 자체)과 산출 파일명에 들어가는 `{책-제목}-v{version}.epub`의 `version`(*책 매니페스트의 책 버전*, 각 책의 판본)은 독립적으로 진화한다. 책 콜로폰(`## 판권`)은 두 버전을 모두 노출한다.

## 이 하네스가 하는 일

주제를 던지면 다음을 자동으로 수행한다.

1. **리서치** — 웹·논문·커뮤니티를 병렬로 뒤져 레퍼런스 문서 작성
2. **저술 계획** — 제목 후보, 책 특성, 챕터 목록과 내러티브 아크 설계
3. **계획 승인** — 설계 근거와 함께 계획을 보여주고 사용자 승인 (원하면 리뷰어 에이전트의 비판적 검토 1회)
4. **챕터 저술** — 저술가 최대 4명이 연속 챕터 묶음을 병렬로 저술하고, 묶음이 끝나는 대로 tech-book은 팩트체커(구체 주장 전반), practical은 팩트체커(안전·건강·법규 사실), narrative는 연속성 키퍼가 한 번 검수해 바로 정정
5. **편집** — 챕터 통합, 전환부·용어·통권 변주 다듬기, 서문·에필로그·참고문헌 작성
6. **수락 게이트** — 새 컨텍스트의 리뷰어가 책 전체를 한 번 판정 (미해소 마커·사실 오류가 남으면 빌드하지 않음)
7. **표지 + EPUB 빌드 + 책 소개** — 표지 이미지 생성, pandoc으로 EPUB 3 조립, 짝을 이루는 책 소개 markdown 작성

산출물은 프로젝트 루트에 두 파일이 짝으로 저장된다.

- `{책-제목}-v{version}.epub` — 본문 EPUB
- `{책-제목}-v{version}.md` — 외부 독자용 책 소개 (logline, 대상 독자, 핵심 약속, 차례, 저자 소개, 책 정보). 블로그·스토어·SNS에 바로 붙여 쓸 수 있도록 작성된다.

## 사전 준비

### 필수

| 도구 | 용도 | 설치 |
|------|------|------|
| [Claude Code](https://claude.com/claude-code) | 하네스 실행 환경 | 공식 설치 가이드 참조 |
| `pandoc` ≥ 3.0 | EPUB 생성 | `brew install pandoc` |
| `python3` ≥ 3.8 | 빌드 스크립트의 메타데이터 파싱 | macOS 기본 제공 |

### 선택 (있으면 더 좋음)

| 도구 | 용도 | 설치 |
|------|------|------|
| `epubcheck` | EPUB 표준 검증 | `brew install epubcheck` |
| `imagemagick` | 표지 이미지 폴백 생성 | `brew install imagemagick` |
| 이미지 생성 MCP/API | 표지 이미지 실제 생성 | 사용 환경에 따라 |

## 설치

```bash
git clone https://github.com/tobyilee/book-writer.git
cd book-writer
# 의존 도구가 없다면 위 '사전 준비' 설치
```

Claude Code를 이 디렉토리에서 실행하면 `.claude/agents/`, `.claude/skills/`, `CLAUDE.md`를 자동 인식한다.

## 빠른 시작

Claude Code 프롬프트에 주제·내용·대상 독자를 자연어로 입력하면 자동으로 `book-writing-orchestrator` 스킬이 발동한다.

```
주제: 효과적인 SQL 쿼리 튜닝
주요 내용: 실행 계획 읽기, 인덱스 설계, N+1 회피, 실전 사례
대상 독자: 백엔드 주니어 개발자 (SQL 기본은 아는 수준)
분량: 150페이지 정도
이 주제로 책 써줘.
```

오케스트레이터가 Phase 0부터 Phase 5까지 순차적으로 진행하며, 각 Phase에서 필요한 에이전트를 자동으로 호출한다. 중간에 계획이 나오면 사용자 승인을 요청하는 지점이 있다.

### 기대 산출물

```
{slug}/
├── research/                # Phase 1 원자료 (보존 — 재실행에도 유지)
│   ├── web.md
│   ├── papers.md
│   └── community.md
├── 01_reference.md          # 리서치 종합
├── 02_plan.md               # 저술 계획 (승인된 최종본)
├── 03_review_log.md         # 계획 리뷰 기록 (plan-reviewer를 요청했을 때만)
├── chapters/
│   ├── 01_draft.md / 01_final.md
│   ├── 02_draft.md / 02_final.md
│   └── ...
├── 04_manuscript.md         # 통합 원고
├── 05_acceptance.md         # 통권 수락 검수 판정 (Phase 4.5, manuscript-reviewer)
├── style_log.md             # 스타일 검수 로그 (style-guardian을 요청했을 때만)
├── factcheck_log.md         # 사실 검증 로그 (tech-book·practical, 단일 append-only)
├── story_bible.md           # 인물·관계·세계관·타임라인·복선 원장 (narrative만)
├── continuity_log.md        # 연속성 검수 로그 + 장별 페이싱 계측 (narrative만)
├── pacing_report.md         # 감정 곡선·씬 페이싱 리포트 (narrative만, 자문 전용)
├── editor_notes.md          # 편집 메모 + 통권 변주 표
├── length_report.md         # 분량 리포트 (length_report.py 실측)
├── book_manifest.json       # EPUB 메타데이터
├── cover.png                # 표지 이미지
├── cover_prompt.md          # 표지 프롬프트 기록
└── build_log.md             # 빌드 로그

{책-제목}-v1.0.0.epub        # 최종 산출물 (프로젝트 루트, 예시 — 책 매니페스트 버전)
{책-제목}-v1.0.0.md          # 책 소개 markdown (EPUB과 같은 폴더, 같은 stem)
```

## 워크플로우 상세

### Phase 1: 리서치 (팬아웃)

- 오케스트레이터가 장르에 맞는 리서처를 **병렬로** 띄운다 — tech-book은 `web-researcher`·`paper-researcher`·`community-researcher`, 그 밖의 장르는 웹·커뮤니티 (학술 근거가 중요하면 논문 추가)
- 각 리서처는 독립 소스에서 자료를 모아 `research/*.md`에 저장 (보존 — fact-checker의 대조 원장)
- `research-lead`가 결과를 합성해 `01_reference.md` 작성

### Phase 2: 저술 계획

- `book-planner`가 레퍼런스를 읽고 `02_plan.md` 작성 — 독자 여정에서 역산한 챕터 배치, 설계 근거(기각한 대안 2개 이상), 용어 표기, 챕터별 오프닝·클로징·스캐폴드 배정
- narrative면 `story_bible.md`도 함께 시드

### Phase 3: 계획 승인

- 오케스트레이터가 계획과 설계 근거를 보여주고 사용자 승인을 받는다 (학습 루프의 선판단 초대 포함)
- 비판적 검토를 원하면 `plan-reviewer`가 5축(커버리지, 흐름, 독자 적합도, 균형, 중복)으로 한 번 리뷰 → planner 반영

### Phase 4: 챕터 저술 (병렬 묶음 + 묶음별 검수)

- 저술을 시작할 때 `cover-designer`를 백그라운드로 띄운다 — 표지에 필요한 것은 계획 승인 시점에 다 정해져 있다
- 챕터를 연속 묶음(2~4장)으로 나눠 `chapter-writer` 최대 4명이 병렬 저술 (narrative는 1~3장 묶음을 순서대로, 묶음마다 검수 뒤 다음 묶음). 저술가는 활성 프로필의 `style-checklist.md`를 품질 기준으로 삼아 쓰고, 계획의 배정·용어 표기·공유 정전을 따르며, 예상 분량을 ±15% 목표로 삼는다. 정전 밖에서 새로 정한 것은 반환값으로 올리고 오케스트레이터가 `integration_notes.md`에 모은다
- 묶음이 끝나는 즉시 검수: (tech-book) `fact-checker`가 사실 주장을 `research/*.md` 원장과 대조해 정정·약화·삭제를 직접 반영 / (practical) `fact-checker`가 안전·건강·법규 사실(식품 안전 온도·보관·알레르겐·여행 법규)만 같은 방식으로 / (narrative) `continuity-keeper`가 `story_bible.md`와 대조해 모순을 고치고 bible 갱신, 장별 페이싱 계측 후 마지막에 `pacing_report.md`(자문 전용). 결과가 `{NN}_final.md`
- 검수자가 스스로 고칠 수 없는 항목만 `미해소`로 남기고, 오케스트레이터가 모아서 통합 전에 한 번에 사용자에게 묻는다
- `editor`가 `04_manuscript.md`로 통합 — 장 간 정합(묶음마다 갈린 예제 정전, 한 장에서만 정정된 사실), 묶음 경계 전환, 용어 통일, 통권 변주(반복되는 오프닝·클로징·말버릇) 교정, 서문·에필로그·참고문헌(원장 그대로)·콜로폰, `book_manifest.json`, `length_report.md`
- 로그는 역할별 단일 파일(`factcheck_log.md`·`continuity_log.md`)에 장마다 즉시 append (병렬 검수자가 동시에 쓰므로 셸 `>>`로만)
- 통합 뒤의 정본은 `04_manuscript.md` — 이후 수정은 원고에 직접 한다
- (practical 요리 계열) editor가 `profiles/practical/partials/conversion-tables.md`의 환산표를 부록에 싣는다

**왜 이 구조인가?** 현행 Opus 모델은 명확한 기준을 주면 스스로 점검하며 쓴다. 그래서 검수 왕복을 겹겹이 쌓는 대신, 저술가 자신이 알기 어려운 두 가지 — 자기가 쓴 사실의 오류, 다른 장과의 충돌 — 만 독립 검수로 잡고, 책 전체에서만 보이는 문제는 editor와 수락 게이트가 한 번씩 본다.

### Phase 4.5: 통권 수락 검수 (신선 컨텍스트 게이트)

- `manuscript-reviewer`가 `manuscript-acceptance` 스킬로 **editor와 분리된 새 컨텍스트**에서 통권을 판정한다 (원고를 만든 쪽이 스스로 승인하지 않음)
- 챕터 완비·분량, 금지 마커(`(사실 확인 필요)`·`[리서치 공백]`·`[미완성]`), 사실 미결과 참고문헌 원장 대조, 용어·voice·변주, 상호 참조, 약속 이행, 부속 자료, (narrative) 연속성
- 판정을 `05_acceptance.md`에 기록 — **ACCEPT**면 Phase 5로, **BLOCK**이면 담당자에게 조치를 한 번 보내고 재판정, 그래도 BLOCK이면 사용자 판단

### Phase 5: EPUB 빌드 + 책 소개

- 표지는 Phase 4에서 백그라운드로 띄운 `cover-designer`가 만든다 (MCP > API > ImageMagick 폴백 순). 아직 끝나지 않았으면 `epub-builder`가 cover-독립 준비(매니페스트 검증·콜로폰 맞춤·책 소개 초안)를 먼저 한다
- `epub-builder`가 `scripts/build_epub.sh`를 호출해 결정적 빌드 (번들 `styles/epub.css`를 자동 임베드 — 실용서 구조화 블록 스타일)
- `pandoc`으로 `04_manuscript.md` + `cover.png` + `book_manifest.json`을 EPUB 3로 변환
- `epubcheck` 설치 시 자동 검증 (`EPUBCHECK_STRICT` 기본 ON)
- EPUB 빌드 직후 `epub-builder`가 `02_plan.md`·`04_manuscript.md`·매니페스트를 읽어 **책 소개 markdown**(`{책-제목}-v{version}.md`)을 EPUB 옆에 작성

## 후속 작업

완성된 책에 수정 요청이 생기면 같은 오케스트레이터가 처리한다.

```
챕터 3 처음 부분이 너무 딱딱해. 다시 써줘.
```
→ 통합 원고(`04_manuscript.md`)의 해당 부분만 고치고 수락 게이트·재빌드. 장 전체를 다시 쓰는 요청이면 `03_draft_v1.md`로 백업한 뒤 저술·검수부터 다시 거친다.

```
표지를 좀 더 따뜻한 느낌으로 바꿔줘.
```
→ `cover-designer` 재호출(`cover_v1.png`로 백업) 후 `epub-builder`로 재빌드.

```
계획을 좀 더 입문자 친화적으로 다시 세워줘.
```
→ Phase 2~3 재실행. 기존 `02_plan.md`는 `02_plan_v1.md`로 백업.

재실행 시 책 버전은 **minor 증가** (`v1.0.0` → `v1.1.0`) 또는 사용자가 명시적으로 지정. 이때 바뀌는 건 **책 매니페스트 버전**이지 하네스 버전이 아니다. EPUB 식별자(`urn:uuid:*`)는 처음 1회만 민팅되고 재빌드에도 그대로 보존된다 — 버전·발행일만 갱신된다.

요청 유형별 정확한 재실행 범위(리서치 보강→Phase 1, 구성·차례 변경→Phase 2~3, 챕터 부분 수정→원고 직접 수정, 챕터 전체 재작성→Phase 4, 표지→cover-designer+재빌드, 메타·라이선스→epub-builder)는 오케스트레이터의 **재실행 매트릭스**(`book-writing-orchestrator/SKILL.md`)를 따른다. 장르는 `book_manifest.json`의 `genre`를 재사용한다(사용자가 변경을 명시하지 않는 한).

## 운영자 학습 루프

하네스는 에이전트 파이프라인만 설계하지 않는다 — **운영자(사람)의 판단력이 완전 위임으로 마모되지 않도록** 세 겹의 학습 루프를 함께 설계한다 (정전 스펙: [`docs/learning-loop.md`](docs/learning-loop.md)).

1. **흐름 안:** 계획 공개 직전 "어떤 챕터 흐름을 기대하시나요?" 한 줄 초대(선판단 후공개) + 계획에 "설계 근거"(기각한 대안 포함) 동봉 + 완료 보고의 설명 가능성 자문
2. **흐름 밖:** 완료 보고에 로그 기반 **직접 검수 표적** 제안 — factcheck/continuity/acceptance 로그가 지목한 취약 지점을 15~30분 크기로
3. **메타:** 위임 다이얼 — 프롬프트에 `모드: 학습`을 넣으면 `learning` 모드로 전환되어 첫 챕터 직접 읽기 권유·검수 표적 3개 등 학습 터치포인트가 늘어난다. 기본은 `production`(현행 동작 그대로)

모든 터치포인트는 **자문 전용·비블로킹**이다 — 응답하지 않아도 파이프라인은 멈추지 않는다.

## 커스터마이징

### 장르 프로필

v1.3.0부터 문체·구조·검수 기준은 장르별 프로필로 관리된다. 각 프로필은 `profiles/{genre}/`에 세 파일로 산다.

| genre | 적용 대상 | voice 한 줄 |
|-------|----------|-------------|
| `tech-book` (기본) | IT·기술서·최신 기술 해설 | Toby 문체 — 함께 생각하는 선배 개발자 (+ 신선도·사실 규율) |
| `narrative` | 소설·서사 | 보여주는 산문 — 씬·시점·대사로 끌고 간다 |
| `practical` | 요리·여행·DIY 실용서 | 명료한 안내자 — 따라 하면 되는 단계와 안전 |
| `essay` | 에세이·사색 | 사색하는 1인칭 — 일화에서 통찰로 |

- 각 프로필: `voice.md`(문체)·`scaffolds.md`(구조)·`style-checklist.md`(문체 품질 기준 — 저술가와 수락 게이트가 공유)
- 장르 선택: 오케스트레이터가 Phase 0에서 주제·대상으로 **자동 감지 후 확인**. 프롬프트에 `장르: {값}`을 넣으면 바로 지정된다. 신호가 약하면 `tech-book` 기본
- 선택 규칙·자동 감지 표는 [`profiles/_registry.md`](profiles/_registry.md)
- 확정 장르는 `book_manifest.json`의 `genre` 필드에 기록되어 재실행 시 결정적으로 재사용된다
- 확장 후속(장르별 fact-checker·구조화 EPUB·소설 연속성 추적)은 [`docs/harness-roadmap.md`](docs/harness-roadmap.md)

### 문체 조정

특정 장르의 톤을 바꾸려면 해당 `profiles/{genre}/voice.md`(와 `scaffolds.md`·`style-checklist.md`)를 수정한다. `tech-book`의 뿌리는 루트 `toby-book-writing-style.md`이며 하위호환을 위해 유지된다. 새 장르를 추가하려면 `profiles/{새장르}/`에 세 파일을 만들고 `profiles/_registry.md` 표에 행을 추가한다.

### 저자명 변경

저자 기본값은 `Toby-AI`다. 다른 저자로 쓰고 싶다면 두 방법 중 하나를 고른다.

**방법 1. 프롬프트에서 지정 (일회성, 권장)**

책 쓰기 요청에 `저자: {이름}` 한 줄을 추가한다. 오케스트레이터가 Phase 0에서 이 값을 캡처해 `book_manifest.json`과 표지 메타에 그대로 반영한다.

```
주제: 효과적인 SQL 쿼리 튜닝
저자: Jane Doe
대상 독자: 백엔드 주니어 개발자
이 주제로 책 써줘.
```

**방법 2. 기본값 자체를 교체 (반복 사용)**

모든 책에 새 기본 저자를 쓰려면 하네스 파일에 있는 `Toby-AI`를 일관되게 교체한다:

- `.claude/skills/book-writing-orchestrator/SKILL.md` — description과 Phase 0·Phase 5 메타데이터
- `.claude/agents/editor.md`, `.claude/skills/book-editing/SKILL.md` — `book_manifest.json` 템플릿의 `"author"` 기본값
- `.claude/agents/cover-designer.md`, `.claude/skills/cover-design/SKILL.md` — 표지 저자 표기 기본값
- `.claude/skills/epub-build/scripts/build_epub.sh` — 빈 매니페스트일 때의 fallback

`epub-builder`와 `build_epub.sh`는 매니페스트 값을 그대로 사용하므로, 매니페스트에 사용자 지정 저자가 들어 있으면 이 fallback은 발동하지 않는다.

### 에이전트·스킬 추가/수정

새로운 역할(예: `translator`)을 추가하려면:

1. `.claude/agents/translator.md` 생성 (핵심 역할, 작업 원칙, 프로토콜)
2. `.claude/skills/translate/SKILL.md` 생성 (description은 pushy하게)
3. 오케스트레이터(`book-writing-orchestrator/SKILL.md`)의 Phase 구성에 통합
4. `CLAUDE.md`의 변경 이력 테이블에 기록

## 디렉토리 구조

```
book-writer/
├── CLAUDE.md                        # 하네스 포인터 + 변경 이력 (새 세션 자동 로드)
├── README.md                        # 이 파일
├── VERSION                          # 하네스 버전 단일 출처
├── toby-book-writing-style.md       # tech-book 프로필의 뿌리 (하위호환)
├── profiles/                        # 장르별 문체 프로필 (v1.3.0+)
│   ├── _registry.md                 # 장르 목록 + 자동 감지 규칙
│   ├── tech-book/                   # voice.md / scaffolds.md / style-checklist.md
│   ├── narrative/                   # 〃
│   ├── practical/                   # 〃
│   └── essay/                       # 〃
├── docs/
│   ├── harness-roadmap.md           # 장르 확장 후속 백로그 (P2·P3·P4)
│   └── learning-loop.md             # 운영자 학습 루프 정전 스펙 (v1.9.0+)
├── .gitignore                       # .omc 등 툴 로컬 파일 제외 (책 산출물은 버전 관리 대상)
└── .claude/
    ├── agents/                      # 14개 에이전트 정의 (역할 카드 — 절차는 스킬이 단일 출처)
    │   ├── research-lead.md         # 리서치 합성
    │   ├── web-researcher.md
    │   ├── paper-researcher.md
    │   ├── community-researcher.md
    │   ├── book-planner.md
    │   ├── plan-reviewer.md         # 요청 시 계획 비판 1회
    │   ├── chapter-writer.md
    │   ├── style-guardian.md        # 요청 시 문체 점검
    │   ├── fact-checker.md          # tech-book 사실 검증 + practical 안전 사실 검증
    │   ├── continuity-keeper.md     # narrative 연속성 추적 (v1.7.0+)
    │   ├── editor.md
    │   ├── manuscript-reviewer.md   # 통권 수락 게이트 (Phase 4.5, v1.8.0+)
    │   ├── cover-designer.md
    │   └── epub-builder.md
    └── skills/                      # 오케스트레이터 + 14개 전문 스킬
        ├── book-writing-orchestrator/   # 최상위 워크플로우
        ├── research-coordination/
        ├── web-research/
        ├── paper-research/
        ├── community-research/
        ├── book-planning/
        ├── plan-review/
        ├── chapter-writing/
        ├── style-review/
        ├── fact-check/              # tech-book 사실 검증 (v1.4.0+)
        ├── continuity-check/        # narrative 연속성 검수 (v1.7.0+)
        ├── book-editing/
        │   └── scripts/length_report.py  # 장별 산문 분량 실측
        ├── manuscript-acceptance/   # 통권 수락 게이트 (Phase 4.5, v1.8.0+)
        ├── cover-design/
        └── epub-build/
            ├── scripts/
            │   └── build_epub.sh
            └── styles/
                └── epub.css        # 구조화 블록 스타일 (v1.5.0+)
```

## 데이터 전달 규칙

| 방식 | 용도 |
|------|------|
| 파일 기반 (`{slug}/`) | Phase 간 산출물 전달, 감사 추적 |
| 반환값 기반 | 각 에이전트가 산출물 경로·미해소 항목·사용자 판단 필요 사항을 짧게 보고 |

팀 도구(`TeamCreate`·`SendMessage`)는 쓰지 않는다. 에이전트 간 조율은 모두 파일로 한다.

파일명 컨벤션: Phase 주요 산출물은 `{NN}_{artifact}.md` (NN = Phase 번호). 챕터는 `chapters/{NN}_draft.md`·`{NN}_final.md` (NN = 챕터 번호). 로그·매니페스트·표지·리포트 등 부산물은 역할별 고정 파일명(`factcheck_log.md`·`continuity_log.md`·`book_manifest.json`·`length_report.md` 등)을 쓰며 샤딩하지 않는다.

## 트러블슈팅

### "pandoc: command not found"
```bash
brew install pandoc
```

### EPUB 크기가 50KB 미만으로 경고
원고가 너무 짧거나 챕터 변환 실패 가능성. `{slug}/build_log.md`와 `.pandoc_err`를 확인한다. 원고가 진짜 짧다면(샘플·테스트) 무시해도 된다.

### `epubcheck` 실패
EPUB은 생성되지만 표준 위반 사항이 있다. `{slug}/.epubcheck.log`를 읽고 문제 구절을 수정한다. 대부분 `<script>` 태그나 금지된 네임스페이스 같은 마크다운 소스 문제다.

### 챕터 초안이 Toby 문체와 달라 보임
`05_acceptance.md`의 (d) 판정을 먼저 본다. 해당 장을 지정해 "N장 문체 점검해줘"라고 하면 `style-guardian`이 한 번 다듬는다. 여러 책에서 같은 이탈이 반복되면 `profiles/tech-book/voice.md`·`style-checklist.md`의 해당 규칙이 모호한 것이니 구체적 예시를 보강하자.

### 표지 이미지 생성 실패
1. 이미지 생성 MCP/API가 연결되어 있지 않으면 ImageMagick 폴백 사용 → 단순 타이포그래피 표지가 생성됨
2. ImageMagick도 없으면 `brew install imagemagick` 후 재실행
3. 품질이 부족하면 `cover-designer`를 수동으로 재호출 요청

### "book-writing-orchestrator 스킬이 트리거되지 않음"
프롬프트에 "책 써줘", "저술", "EPUB" 같은 키워드가 있는지 확인한다. 단순 질문(예: "이 하네스가 뭐야?")에는 트리거되지 않는 게 정상이다. 억지로 발동시키려면 `/book-writing-orchestrator`를 직접 호출.

## 진화 규칙

하네스는 **정적 산출물이 아니라 진화하는 시스템**이다.

- 실행 완료 후 사용자 피드백이 있으면 해당 에이전트·스킬을 수정
- 변경은 `CLAUDE.md`의 변경 이력 테이블에 기록
- 같은 유형 피드백이 2회 이상 반복되면 구조적 수정 검토
- 브랜치 전략 권장: 실험은 `harness` 브랜치, 안정화되면 `main`으로 머지

## 라이선스

MIT License. 전문은 [LICENSE](LICENSE) 참조.

## 크레딧

- 저자: Toby-AI (AI 저자 페르소나)
- 하네스 설계: Toby Lee + Claude Opus 4.7
