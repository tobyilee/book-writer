# Book Writer — 한국어 기술서 저술 하네스

주제·주요 내용·대상 독자만 주면 **리서치부터 EPUB 완성까지** 자동으로 굴러가는 Claude Code 기반 책 저술 시스템이다. 저자는 항상 `Toby-AI`로 고정되며, 모든 원고는 **토비 문체**(평어체 기반, 청유형 적극 활용, 수사적 질문, 감정적 공감)로 작성된다.

## 왜 이렇게 만들었나

책 한 권을 쓰는 작업은 성격이 전혀 다른 여섯 일을 하나로 묶는 일이다. 자료를 모으고, 구조를 잡고, 비판적으로 읽고, 글로 풀고, 톤을 지키고, 포장까지 해야 한다. 사람 혼자 하기엔 흐름이 자주 끊긴다. 이 하네스는 각 일을 **전문 에이전트**에게 맡기고, 사이사이의 왕복(저자↔리뷰어, 저술가↔스타일 가디언)을 **팀 모드**로 실시간 조율한다. 남은 건 주제 하나를 던지는 것뿐이다.

## 산출물 예시 — `llm-intro` 브랜치

- **책:** 『LLM 내부로 들어가기 — 백엔드 개발자를 위한 한 걸음씩 입문』 (약 290,000자, 서문 + 10장 + 부록 A/B/C)
- **EPUB:** [output/LLM-내부로-들어가기-v1.0.1.epub](output/LLM-내부로-들어가기-v1.0.1.epub) (357 KB, epubcheck 0 errors / 0 warnings)
- **중간 산출물:** [llm-intro/](llm-intro/) (리서치 → 플랜 v1·v2 → 리뷰 로그 → 14장 draft/review/final → 통합 원고 → 표지 → 매니페스트 → 빌드 로그)

이 한 권이 하네스의 종단 동작 증거다. 브랜치 `llm-intro`로 전환해 전체 워크플로우가 남긴 자국을 추적할 수 있다.

## 전체 흐름

```
주제 입력
   │
   ▼
┌────────────────────────────────────────────────────────┐
│ Phase 0. 컨텍스트 확인                                │
│   - {slug}/ 존재 여부, 부분 재실행 여부 판단          │
└────────────────────────────────────────────────────────┘
   │
   ▼
┌────────────────────────────────────────────────────────┐
│ Phase 1. 리서치 (팬아웃)                              │
│   research-lead                                        │
│     ├── web-researcher        ─ 병렬, 백그라운드       │
│     ├── paper-researcher      ─ 병렬, 백그라운드       │
│     └── community-researcher  ─ 병렬, 백그라운드       │
│   → research/web.md · papers.md · community.md         │
│   → 01_reference.md (종합)                             │
└────────────────────────────────────────────────────────┘
   │
   ▼
┌────────────────────────────────────────────────────────┐
│ Phase 2. 저술 계획 (단일)                             │
│   book-planner → 02_plan.md (v1)                       │
└────────────────────────────────────────────────────────┘
   │
   ▼
┌────────────────────────────────────────────────────────┐
│ Phase 3. 계획 리뷰 (팀 왕복)                          │
│   plan-reviewer ↔ book-planner (최대 2회)              │
│   → 02_plan.md (v2) + 03_review_log.md                 │
└────────────────────────────────────────────────────────┘
   │
   ▼
┌────────────────────────────────────────────────────────┐
│ Phase 4. 챕터 저술 (팀)                                │
│   chapter-writer × 3 (풀 방식, 파도별 병렬)            │
│     draft → style-guardian 리뷰 → revise → final       │
│   editor → 통합 04_manuscript.md + book_manifest.json  │
└────────────────────────────────────────────────────────┘
   │
   ▼
┌────────────────────────────────────────────────────────┐
│ Phase 5. 표지 + EPUB (팬아웃, 순서 의존)              │
│   cover-designer       ─ 병렬                          │
│   epub-builder (cover 대기 후) → output/*.epub         │
└────────────────────────────────────────────────────────┘
   │
   ▼
 사용자 피드백 → 특정 Phase만 재실행
```

## 에이전트 (11종)

전부 `model: opus`로 구동된다. 각자 좁고 깊은 역할 하나를 맡는다.

| 에이전트 | 역할 | 주요 산출물 |
|---------|------|------------|
| **research-lead** | 리서치 3명 병렬 조율 + 종합 | `01_reference.md` |
| **web-researcher** | 블로그·기사·공식 문서 8~15건 수집 | `research/web.md` |
| **paper-researcher** | arXiv/Semantic Scholar 논문 3~10편 | `research/papers.md` |
| **community-researcher** | Reddit/HN/OKKY/velog 커뮤니티 10~20건 | `research/community.md` |
| **book-planner** | 제목 후보·챕터 구성·내러티브 아크 설계 | `02_plan.md` |
| **plan-reviewer** | 5축(커버리지·흐름·독자·균형·중복) 비판 | `03_review_log.md` |
| **chapter-writer** | 단일 챕터를 토비 문체로 초안 작성 | `chapters/NN_draft.md` |
| **style-guardian** | 챕터 스타일 검수 + 구체적 대체 문장 제안 | `chapters/NN_style_review.md` |
| **editor** | 챕터 통합·전환부·용어 통일·프론트/백 매터 | `04_manuscript.md`, `book_manifest.json` |
| **cover-designer** | 표지 이미지 + 재생성 스크립트 | `cover.png`, `make_cover.py` |
| **epub-builder** | pandoc 기반 EPUB 3 빌드 + 검증 | `output/*.epub`, `build_log.md` |

## 스킬 (12종)

에이전트가 필요할 때 호출하는 절차 묶음이다. 각 스킬은 자신을 언제 써야 하는지 `description`에 적어두어, 사용자가 직접 키워드로 불러내는 것도 가능하다.

| 스킬 | 언제 쓰나 |
|------|----------|
| **book-writing-orchestrator** | 전체 파이프라인 실행. "책 써줘"의 입구. |
| **research-coordination** | 리서치 3인방 병렬 조율. |
| **web-research / paper-research / community-research** | 개별 소스 수집. 부분 재실행 시 유용. |
| **book-planning** | 저술 계획 최초 작성 또는 리뷰 반영 개정. |
| **plan-review** | 계획 5축 비판. |
| **chapter-writing** | 단일 챕터를 토비 문체로 집필. 스타일 가이드를 안고 작동. |
| **style-review** | 챕터 초안의 스타일 편차 점검. 10개 항목 체크리스트. |
| **book-editing** | 챕터 통합과 내러티브 다듬기. |
| **cover-design** | 표지 콘셉트 3안 + 실제 이미지 생성. |
| **epub-build** | `scripts/build_epub.sh`로 결정적 EPUB 빌드. |

## 문체 계약 — 토비 스타일

[toby-book-writing-style.md](toby-book-writing-style.md)가 모든 챕터의 제약 조건이다. 핵심만:

- **평어체 기반** — `-다`, `-한다`가 디폴트. 딱딱하지 않게.
- **청유형 적극** — `-자`, `-보자`를 자주. "함께 걷는 화자" 정서가 책의 뼈대.
- **수사적 질문·상황 가정** — 독자가 자기 상황에 대입하게 만드는 장치.
- **감정적 공감 어휘** — `난감하다`, `찜찜하다`, `아찔하다` 등을 자연스럽게 배치.
- **지시적 어조 금지** — "~해야 한다" 대신 "~하는 편이 낫다".
- **메타 문장 금지** — "이번 장에서는 ~을 다룬다" 같은 자기 고지는 쓰지 않는다.
- **문체 3층 구획** — (1) 장 도입·전환·말미는 청유형, (2) 코드·수식·표 앞 1~2문단은 평어 서술, (3) 코드 주석·에러 해설·터미널 로그는 담담한 매뉴얼체. 실습 장에서 특히 중요.

`style-guardian`이 초안마다 이 계약을 점검한다. 조건부 통과(Critical 1~2건)가 가장 흔한 판정이고, `chapter-writer`가 리뷰를 반영해 `{NN}_final.md`로 승격시킨다.

## 사용법

```
# 기본 — 주제만 던지기
$ claude
> OOO에 대한 책을 써줘. 대상은 △△ 개발자야.

# 부분 재실행
> llm-intro의 4장만 다시 써줘
> 표지만 새로 만들어줘
> 리서치만 다시 해줘
```

오케스트레이터 스킬이 `{slug}/`의 존재 여부와 사용자 입력을 보고 Phase 전체 실행인지 부분 재실행인지 결정한다.

### 수동으로 Phase만 호출하고 싶다면

스킬 이름으로 직접 불러낼 수 있다:

```
> /research-coordination  "LLM 파인튜닝" 주제로 3인 병렬 리서치
> /book-planning           위 리서치를 바탕으로 계획 v1
> /plan-review             v1 계획을 5축으로 비판
> /chapter-writing         4장만 토비 문체로 집필
> /style-review            4장 draft 스타일 점검
> /book-editing            모든 final 통합
> /cover-design            표지 생성
> /epub-build              EPUB 산출
```

## 산출 경로 규약

각 책은 리포지토리 루트에 자기 슬러그 폴더를 하나 갖는다. EPUB은 공통 `output/` 디렉터리로 모인다.

```
{slug}/                            (예: llm-intro/)
├── research/
│   ├── web.md
│   ├── papers.md
│   ├── community.md
│   └── supplementary_gap*.md     (2차 리서치 — 필요 시)
├── 01_reference.md               (리서치 종합)
├── 02_plan_v1.md · 02_plan.md    (계획 v1 스냅샷 + 최신)
├── 03_review_log.md              (계획 리뷰 로그)
├── chapters/
│   ├── 00_draft.md · 00_style_review.md · 00_final.md
│   ├── 01_draft.md · 01_style_review.md · 01_final.md
│   └── ... (각 장마다 3종 세트)
├── 04_manuscript.md              (통합 원고)
├── book_manifest.json            (EPUB 빌드용 매니페스트)
├── cover.png · cover_thumb.png · make_cover.py · cover_prompt.md
├── style_log.md                  (전 챕터 스타일 리뷰 요약)
└── build_log.md                  (EPUB 빌드 기록 + 개선 내역)

output/
└── {책-제목}-v{version}.epub
```

각 책 폴더와 `output/`은 기본적으로 리포지토리에 트래킹된다. 실험적·비공개 책은 `.gitignore`에 해당 슬러그를 추가해 제외할 수 있다.

## EPUB 빌드 세부

- **도구:** pandoc 3.x + epubcheck (선택)
- **스크립트:** `.claude/skills/epub-build/scripts/build_epub.sh {slug}`
- **메타데이터:**
  - 제목: 매니페스트의 `title`
  - 저자: **`Toby-AI` 고정** (다른 값이면 경고)
  - 언어: `ko`
  - 식별자: 매니페스트의 `identifier` (실제 UUID 권장: `urn:uuid:...`)
  - 발행일: 매니페스트의 `pub_date`
- **산출 파일명:** `{제목-슬러그}-v{version}.epub`

빌드 후 `epubcheck`가 있으면 자동 검증한다. `0 fatals / 0 errors / 0 warnings`가 목표. v1.0.0에서 13개 non-blocking 오류를 본 뒤 v1.0.1에서 clean으로 만드는 과정이 [llm-intro/build_log.md](llm-intro/build_log.md)에 남아 있다.

## 설계 결정

| 선택 | 이유 |
|------|------|
| 리서치 3인방 팬아웃 | 소스별 독립 수집이라 병렬이 이득 |
| 계획 단계는 단일 에이전트 | 통합적 사고가 필요, 분할이 독 |
| 계획 리뷰는 팀 왕복 | 저자↔리뷰어 토론이 품질을 높임 |
| 챕터 저술은 3풀 병렬 + 스타일 가디언 | 조율 오버헤드와 처리량의 균형 |
| 모든 중간 산출물은 파일 | 재실행·감사 추적·토큰 효율 |
| 저자 `Toby-AI` 고정 | 다중 저자 관리 불필요, 톤 일관성 확보 |

## 필요한 도구

- Claude Code (`claude` CLI) — Opus 모델 접근 권장
- pandoc 3.x (`brew install pandoc`)
- Pillow (표지 생성 — `pip install pillow` 또는 `uv pip install pillow`)
- epubcheck (선택, 검증용 — `brew install epubcheck`)

## 알려진 제약

- **한국어 인쇄·조판 수준은 아직 아님** — EPUB 내부 CSS는 pandoc 기본. 시각 디자인 개선 여지 남음.
- **이미지 생성은 Pillow 기반 타이포 위주** — AI 이미지 모델 연동은 옵션 (cyberpunk 취향을 피하려 기본 비활성).
- **빌드 스크립트 경로 가정** — `.claude/skills/epub-build/scripts/build_epub.sh`는 아직 `_workspace/{slug}/` 경로를 읽도록 되어 있다. 책 폴더를 루트 슬러그로 쓰는 현재 규약에 맞추려면 스크립트에서 경로 prefix를 옵션화하거나 루트 `{slug}/`를 `_workspace/{slug}/`로 심볼릭 링크해 두고 돌리면 된다. 차기 스크립트 개선 항목.

## 라이선스

코드: MIT. 산출된 책의 본문·표지는 각 책의 매니페스트에 명시된 라이선스를 따른다 (기본값 CC BY-NC-SA 4.0).

---

저자: **Toby-AI** (수천 개발자의 공개 기록이 뭉친 화자)

