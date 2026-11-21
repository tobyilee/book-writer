---
name: book-writing-orchestrator
description: Orchestrate a full book-writing workflow from topic to finished EPUB with cover image. Use when the user asks to "write a book", "draft a book", "author a book", "책 쓰기", "책 저술해줘", "책 만들어줘", "전자책 만들어줘", "EPUB 생성", provides a topic/audience/outline and asks to turn it into a book, or says "~에 대한 책을 써줘". Also triggers on follow-ups like "다시 저술", "계획 수정", "챕터 다시 써줘", "표지 바꿔", "책 업데이트", "특정 챕터 보완", "이전 책 개선", "리서치만 다시". Coordinates research, planning, chapter writing in the active genre voice (auto-detected; defaults to tech-book = Toby's style), fact/continuity checks, editing, cover design, and EPUB assembly. Author defaults to Toby-AI (overridable via user prompt — include "저자: {이름}").
---

# Book Writing Orchestrator

주제·주요 내용·대상 독자를 받아 완성된 EPUB을 산출한다. 각 Phase에서 전문 에이전트를 호출하고, 중간 산출물을 `{slug}/`에 쌓은 뒤 최종 EPUB과 책 소개 markdown을 프로젝트 루트에 만든다.

## 흐름 한눈에

| Phase | 누가 | 산출물 |
|-------|------|--------|
| 0. 컨텍스트 | 오케스트레이터 | 장르·저자·라이선스·슬러그·위임 모드 확정 |
| 1. 리서치 | 리서처 2~3명 병렬 → `research-lead`(합성) | `research/*.md`, `01_reference.md` |
| 2. 계획 | `book-planner` | `02_plan.md` (+ narrative면 `story_bible.md` 시드) |
| 3. 계획 승인 | 사용자 | 승인된 `02_plan.md` (확정 제목 기록) |
| 4. 저술 | `chapter-writer` 최대 4명 병렬 → 묶음별 `fact-checker`/`continuity-keeper` → `editor` (`cover-designer`는 이때 백그라운드로 시작) | `chapters/*`, `integration_notes.md`, `04_manuscript.md`, `book_manifest.json`, `cover.png`, (narrative) `pacing_report.md` |
| 4.5. 수락 게이트 | `manuscript-reviewer` (신선 컨텍스트) | `05_acceptance.md` |
| 5. EPUB | `epub-builder` | `{책-제목}-v{version}.epub`·`.md` |

독립 검수는 두 곳에만 둔다 — 챕터 묶음마다 한 번의 사실/연속성 패스, 그리고 통권 수락 게이트 한 번. 저술가는 활성 프로필의 체크리스트를 자기 품질 기준으로 삼아 쓰므로 별도의 스타일 왕복 검수는 기본 흐름에 없다(요청 시 `style-guardian`을 쓴다).

## 서브에이전트 운용

- 에이전트는 `Agent` 도구로 호출하고, 서로 독립인 호출(리서처들, 저술가들)은 한 메시지에 모아 병렬로 띄운다. 팀 도구(`TeamCreate`·`SendMessage`)에 의존하지 않는다 — 모든 조율은 `{slug}/`의 파일과 반환값으로 한다.
- 첫 브리프에 필요한 것을 다 담는다: `genre`, 슬러그, 담당 범위(챕터 번호 등), 읽을 파일 경로, 쓸 파일 경로, 저자·라이선스처럼 이 Phase에 필요한 사용자 지정값. 파일 내용을 프롬프트에 붙여넣지 말고 경로를 준다.
- 각 에이전트에게 반환값은 짧게 요청한다 — 쓴 파일 경로, 미해소 항목, 사용자 판단이 필요한 것. 반환된 결과를 오케스트레이터가 다시 검증하거나 다시 쓰지 않는다.
- 모델은 지정하지 않는다. 모든 에이전트가 현재 세션의 모델 설정을 그대로 상속한다 (frontmatter에도 `model`을 두지 않는다).
- 에이전트가 중단되면 이미 쓴 파일(로그는 챕터마다 즉시 append된다)을 확인하고, 남은 범위만 담아 다시 호출한다.

## Phase 0: 컨텍스트 확인

1. 사용자 입력에서 주제·주요 내용·대상 독자를 뽑는다. 하나라도 불명확하면 `AskUserQuestion`으로 짧게 묻는다. `저자: {이름}`이 있으면 그 값, 없으면 `Toby-AI`. `라이선스: {값}`이 있으면 그 값, 없으면 매니페스트 `license`를 비워 빌드 스크립트 기본값(`CC BY-NC-SA 4.0`)을 쓴다.
2. 장르를 정한다. `장르: {값}`이 있으면 그대로 쓴다. 없으면 `profiles/_registry.md`의 감지 규칙으로 추정하고, 신호가 분명하면 알리고 진행하며, 애매하면 `AskUserQuestion`으로 추정값을 첫 옵션으로 제시해 확인받는다.
3. 위임 모드를 정한다. `모드: 학습`이나 "이 주제를 공부하려고" 같은 명확한 학습 신호가 있으면 `learning`, 없으면 묻지 않고 `production`. 어차피 질문할 일이 있으면 거기에 함께 묻는다 (`docs/learning-loop.md`).
4. 이전 책의 교훈을 모은다. 책마다 자기 브랜치에서 산출되므로 교훈 레코드도 그 브랜치에 커밋돼 있다 — 작업 트리의 파일만 읽으면 다른 책의 교훈이 보이지 않는다. 아래 스크립트가 전 브랜치의 `book-lessons.md`를 모아 같은 장르의 최근 레코드를 출력한다. 그중 이번 책에 해당하는 것을 골라 리서처·planner·writer 브리프에 참고 메모로 넣는다. 레코드가 없으면 건너뛴다.
   ```bash
   python3 .claude/skills/book-writing-orchestrator/scripts/collect_lessons.py --genre {genre} --limit 5
   ```
5. 사용자가 1차 자료(보고서·강의 자료·문서·영상 자막 등)를 줬으면 `{slug}/research/primary/`에 저장한다. 리서처에게는 "이 자료는 다시 수집하지 말고, 자료가 비워 둔 곳과 발행 뒤 바뀐 사실을 채워라"로 브리프한다. 1차 자료는 fact-checker의 대조 근거로도 쓰인다.
6. 제목 후보와 슬러그를 만든다 (예: `AI 시대의 개발자 철학` → `ai-developer-philosophy`). `{slug}/`가 없으면 새 실행, 있고 부분 수정 요청이면 재실행 매트릭스를 따르고, 있는데 완전히 새 입력이면 기존 폴더를 `{slug}_prev-{timestamp}/`로 옮긴 뒤 새로 시작한다. 재실행에서는 `book_manifest.json`의 `genre`·`delegation_mode`를 그대로 쓴다.

## Phase 1: 리서치

장르에 맞는 리서처를 한 메시지에서 병렬로 띄운다. 각자 `{slug}/research/`에 자기 파일을 쓴다.

| genre | 리서처 |
|-------|--------|
| `tech-book` | `web-researcher`, `paper-researcher`, `community-researcher` |
| `essay` | `web-researcher`, `community-researcher` (학술 근거가 중요한 주제면 `paper-researcher` 추가) |
| `practical`·`narrative` | `web-researcher`, `community-researcher` |

실습·도구 중심 `tech-book`이면 web-researcher 브리프에 "예제에 쓸 도구·액션의 최신 버전과 핵심 설정·API 시그니처 표"를 필수 산출로 적는다 — 이 표가 없으면 저술가가 코드 블록마다 추정하거나 확인 마커를 달게 된다.

모두 끝나면 `research-lead`를 호출해 `research/*.md`(와 `research/primary/`)를 `{slug}/01_reference.md`로 합성한다. `research/*.md`는 합성 후에도 보존한다 — `fact-checker`의 1차 대조 근거다. 리서처 하나가 실패하면 한 번 다시 띄우고, 또 실패하면 그 소스 없이 진행하며 레퍼런스의 "리서치 한계"에 적는다.

## Phase 2: 저술 계획

`book-planner`에게 `genre`, 주제·주요 내용·대상 독자, `01_reference.md`, 활성 `profiles/{genre}/scaffolds.md`, (있으면) 교훈 메모를 준다. 산출물은 `{slug}/02_plan.md` — 제목 후보 3개, 책 특성, 내러티브 아크, 설계 근거(기각한 대안 2개 이상), 용어 표기, 공유 정전(여러 장이 함께 쓰는 러닝 예제·아키텍처 불변식), 챕터 목록, 챕터별 전제·인계와 오프닝·클로징·스캐폴드 배정. `narrative`면 planner가 `{slug}/story_bible.md`도 시드한다.

## Phase 3: 계획 승인

사용자에게 계획을 보여주고 승인을 받는다. 보여주기 직전, 운영자에게 "이 주제·독자라면 어떤 챕터 흐름을 기대하시나요? (한두 줄, 건너뛰어도 됩니다)"를 초대한다 — `learning`에서는 별도 단계로, `production`에서는 승인 요청에 한 줄로 붙인다. 스케치가 오면 계획과 갈라진 지점을 짚어준다. 계획 제시에는 `02_plan.md`의 설계 근거를 포함한다. 피드백이 있으면 `book-planner`를 한 번 더 호출해 반영한다. 승인되면 사용자가 고른 제목(따로 말이 없으면 추천안)을 `02_plan.md`의 "제목 후보" 아래에 `**확정 제목:** {제목} — {부제}`로 적는다. editor·cover-designer가 이 줄을 읽는다.

사용자가 계획의 비판적 검토를 원하면 그때 `plan-reviewer`를 한 번 호출해 `03_review_log.md`를 받고, planner가 반영한다.

## Phase 4: 저술

**표지.** 저술을 시작할 때 `cover-designer`를 백그라운드로 띄운다(`{slug}/cover.png`). 표지에 필요한 것(확정 제목·주제 분위기·대상 독자·저자)은 계획 승인 시점에 다 정해져 있으므로, 원고를 기다릴 이유가 없다.

**저술.** 챕터를 연속된 묶음으로 나눠 `chapter-writer`에게 맡긴다 — 한 명이 2~4장, 최대 4명, 한 메시지에서 병렬로. 연속 묶음이어야 저술가가 자기 묶음 안의 전환을 직접 다듬을 수 있다. 묶음마다 끝나는 시점에 검수를 붙이려면 `run_in_background: true`로 띄워 완료 알림을 하나씩 받는다. 브리프에는 담당 장 번호, `02_plan.md`, `01_reference.md`, 활성 프로필(`voice.md`·`scaffolds.md`·`style-checklist.md`), 교훈 메모를 준다.

`narrative`는 병렬로 쓰지 않는다. 1~3장 묶음을 순서대로 맡기고, 묶음마다 continuity-keeper의 검수가 끝난 뒤 다음 묶음을 띄운다. 다음 묶음의 브리프에는 갱신된 `story_bible.md`와 앞 장들의 `{NN}_final.md`를 준다 — 앞 장의 문장과 새로 생긴 정전을 보지 못하면 서사가 갈라진다.

**묶음 사이의 결정 모으기.** 병렬 저술가들은 서로의 원고를 보지 못한다. 저술가의 반환값에는 계획의 공유 정전에 없어서 스스로 정한 것(예제의 파일 경로·클래스 이름·스키마·메시지 형태 등)과 다른 묶음이 알아야 할 것이 올라온다. 이를 받는 대로 `{slug}/integration_notes.md`에 묶음별로 옮겨 적고, 통합 때 editor에게 준다. 이 파일은 오케스트레이터만 쓴다.

저술가는 검수자가 있는 장르(`tech-book`·`practical`·`narrative`)에서는 `chapters/{NN}_draft.md`를, 없는 장르(`essay`)에서는 바로 `chapters/{NN}_final.md`를 쓴다.

**묶음별 검수 (파이프라인).** 저술가 하나가 끝나는 즉시 그 묶음의 검수자를 띄운다 — 다른 묶음을 기다리지 않는다. 묶음이 3장 이상이면 fact-checker를 2장 단위로 나눠 병렬로 띄운다. 웹 확인이 많은 4장 묶음을 한 검수자에게 주면 도중에 멈추는 일이 잦았다.
- `tech-book` → `fact-checker`: 구체 사실 주장과 `(사실 확인 필요)` 주석을 `01_reference.md`·`research/*.md`와 대조하고, 정정·약화·삭제를 draft에 직접 반영해 `{NN}_final.md`로 저장한다. `factcheck_log.md`에 장별로 기록한다.
- `practical` → `fact-checker`: 안전·건강·법규 사실만 본다 — 식품 안전 온도·보관 기간·알레르겐·응급 대처·여행 법규, "~해도 안전하다"류 단정. 틀리면 독자가 실제로 다치는 영역이라서다. 맛·취향·팁은 대상이 아니다.
- `narrative` → `continuity-keeper`: `story_bible.md`와 대조해 모순을 직접 고치고 `{NN}_final.md`로 저장하며, 새 정전을 bible에 반영한다. 저술가가 묶음을 끝낼 때마다 이어서 검수하고, 장마다 긴장도·지배 감정·씬 수·아크 위치를 한 줄 계측한다. 마지막 장을 마치면 `pacing_report.md`(감정 곡선·씬 페이싱, 자문 전용)를 만든다 — editor가 참고할 뿐 BLOCK 사유가 아니다.

검수자가 스스로 고칠 수 없는 항목(고치면 장의 논지가 무너지는 사실 오류, 저자 의도를 알아야 하는 설정 충돌)만 로그에 `미해소`로 남기고 반환값에 올린다. 오케스트레이터는 이를 모아 두었다가 모든 묶음의 검수가 끝난 뒤, editor를 부르기 전에 한 번에 사용자에게 묻는다. narrative에서 다음 묶음의 저술을 막는 설정 충돌만 바로 묻는다.

**통합.** 모든 `{NN}_final.md`가 모이면 `editor`를 호출한다(`integration_notes.md`가 있으면 함께 준다). editor는 묶음 사이에서 갈린 예제 정전과 사실 판정을 맞추고, 전환부·용어·콜백을 다듬고, 통권 변주(오프닝·클로징·말버릇이 여러 장에 같은 틀로 반복되는지)를 바로잡고, 서문·에필로그·참고문헌·콜로폰(`## 판권`)을 쓰고, `04_manuscript.md`·`book_manifest.json`·`length_report.md`를 만든다. `practical` 요리 계열이면 `profiles/practical/partials/conversion-tables.md`의 환산표를 부록에 싣고, `narrative`면 `pacing_report.md`를 참고해 평탄한 긴장 구간·돌출 씬을 손볼지 정한다. 매니페스트에는 `genre`, `delegation_mode`, 저자, (지정됐으면) 라이선스, 루트 `VERSION`의 `harness_version`을 넣는다.

`learning` 모드에서는 첫 `{NN}_final.md`가 나오면 운영자에게 알리고 `style-checklist.md`와 함께 직접 읽어보길 권한다. 저술은 멈추지 않는다.

## Phase 4.5: 통권 수락 게이트

`manuscript-reviewer`를 새 컨텍스트로 호출한다 — 원고를 만든 editor가 스스로 승인하지 않게 하기 위해서다. 입력은 `04_manuscript.md`, `02_plan.md`, `book_manifest.json`, `length_report.md`, `editor_notes.md`, 존재하는 로그(`factcheck_log.md`·`continuity_log.md`), (narrative) `story_bible.md`, (tech-book) `research/*.md`, 활성 `style-checklist.md`. 산출물은 `05_acceptance.md`. 기본 흐름에 별도 스타일 검수가 없으므로 voice 이탈도 이 게이트가 본다 — 여러 장에 걸친 이탈이면 해당 장들에 `style-guardian`을 한 번 보낸다.

- **ACCEPT** → Phase 5.
- **BLOCK** → 판정문의 조치를 담당자(해당 장 `chapter-writer`·`fact-checker`·`editor`·`style-guardian`)에게 한 번 보낸 뒤, 영향받은 기준만 다시 판정받는다. 그래도 BLOCK이면 빌드하지 않고 사용자에게 판단을 구한다.
- 통합 뒤의 정본은 `04_manuscript.md`다. 조치를 받은 담당자는 원고의 해당 부분을 직접 고친다(`{NN}_final.md`는 통합 전 스냅샷으로 남는다). editor가 통합하면서 다듬은 전환부·오프닝이 원고에만 있어서, 장 파일을 고쳐 다시 합치면 그 수정이 사라지기 때문이다. 장을 통째로 다시 써야 하는 조치만 `{NN}_draft.md`부터 다시 거친 뒤(저술 → 검수) editor가 원고의 그 장을 교체하고 앞뒤 전환부를 다시 다듬는다.
- 미해소 마커(`(사실 확인 필요)`·`[리서치 공백]`·`[미완성]`)나 미해소 사실 오류가 남은 원고는 사용자가 명시적으로 승인하지 않는 한 빌드하지 않는다. 틀린 사실이 담긴 책이 조용히 나가는 것이 이 하네스에서 가장 비싼 실패다.

## Phase 5: EPUB

`epub-builder`를 호출한다. 표지는 Phase 4에서 띄운 `cover-designer`가 이미 만들었을 것이다 — 아직 끝나지 않았으면 epub-builder가 매니페스트·콜로폰 정합성 확인과 책 소개 초안처럼 표지와 무관한 일을 먼저 하고, `cover.png`가 생긴 뒤 빌드한다. cover-designer가 반환한 표지 대체 텍스트가 있으면 epub-builder 브리프에 넣는다(매니페스트 `cover_alt`에 기록된다). 산출물은 프로젝트 루트의 `{책-제목}-v{version}.epub`과 같은 stem의 책 소개 `{책-제목}-v{version}.md`.

EPUB 메타데이터: 저자(기본 `Toby-AI`), Phase 2에서 확정된 제목, 버전(첫 실행 `1.0.0`, 재실행 시 증가), 언어 `ko`, 라이선스(기본 `CC BY-NC-SA 4.0`), `genre`, `harness_version`. epub-builder가 mermaid 미렌더나 epubcheck 문제를 보고하면 그대로 사용자에게 전한다.

## 완료 보고

1. EPUB 경로, 책 소개 md 경로, 짧은 요약, `02_plan.md` 설계 근거 요약.
2. 설명 가능성 자문 한 줄: "이 책의 핵심 논지를 남에게 한 문단으로 설명할 수 있는가? 막히는 지점이 직접 읽을 지점이다."
3. 직접 검수 표적 제안 — `production`은 1개, `learning`은 3개, 각 15~30분 크기. 로그에서 고른다: `factcheck_log.md`에서 약화·삭제가 몰린 장, `continuity_log.md`의 미해소, `05_acceptance.md`에서 아슬하게 통과한 기준. 수행을 강요하거나 추적하지 않는다.
4. 교훈 한 레코드를 프로젝트 루트의 `book-lessons.md`에 append한다(책 브랜치에 책과 함께 커밋되고, 다음 책의 Phase 0이 `collect_lessons.py`로 읽는다). 수집 스크립트가 헤딩의 날짜와 본문의 장르로 고르므로 아래 형식을 지킨다.
   ```markdown
   ## {YYYY-MM-DD} — {책 제목} ({slug})
   - genre: {genre} · harness v{harness_version} · delegation_mode: {mode} · 챕터 수: {N}
   - 반복된 사실/연속성 이슈: {...}
   - 수락 게이트 BLOCK 사유: {...}
   - 분량 준수도: {실측/계획}
   - 다음 책에 주는 메모: {하네스·브리프에서 바꿀 것}
   ```
5. "개선할 부분이 있나요?"를 짧게 묻는다.

학습 루프 터치포인트는 모두 자문이며 응답이 없으면 그대로 진행한다. 새 대기 지점을 만들지 않는다.

## 재실행 매트릭스

후속 요청은 해당 Phase만 다시 돌린다. 덮어쓸 산출물은 `{name}_v{N}.{ext}`로 백업한다. 장르·식별자(`urn:uuid:*`)는 유지하고 책 버전과 발행일만 올린다 — 올릴 폭(오탈자 patch·챕터 개정 minor·구조 재편 major)은 오케스트레이터가 정해 epub-builder 브리프에 적고, epub-builder가 매니페스트와 콜로폰의 판본·발행일을 함께 갱신한다. EPUB에 들어가는 것이 바뀌면 항상 epub-builder로 다시 빌드한다.

| 요청 | 재실행 범위 |
|------|------------|
| 리서치 보강 | Phase 1 (해당 리서처 + `research-lead` 합성) |
| 구성·차례 변경 | Phase 2~3 |
| 특정 챕터 부분 수정 | `chapter-writer`가 `04_manuscript.md`의 해당 부분을 고침 → (사실이 바뀌었으면) `fact-checker`가 바뀐 부분만 확인 → 4.5 → 재빌드 |
| 특정 챕터 전체 재작성 | Phase 4 해당 장(`{NN}_draft.md`부터 저술 → 검수) → editor가 원고의 그 장을 교체 → 4.5 → 재빌드 |
| 표지 변경 | `cover-designer` → `epub-builder` 재빌드 |
| 메타데이터·라이선스 변경 | `epub-builder`만 (라이선스 설명 문단을 새로 써야 하면 editor) |
| 문체 점검 요청 | `style-guardian`을 지정 장에 한 번 → 재빌드 |
| 페이싱 분석 요청 (narrative) | `continuity-keeper`로 `pacing_report.md`만 재산출 |

## 에러 대응

| 상황 | 대응 |
|------|------|
| 저술가가 `[리서치 공백]`으로 장이 계획 분량의 절반 아래로 줄었다고 보고 | 해당 주제로 리서처를 한 번 보강 호출하고 `research-lead`가 레퍼런스에 합친 뒤 그 장만 다시 쓴다 |
| 레퍼런스가 빈약해 fact-checker가 핵심 주장을 확인하지 못함 | 확인 못 한 주장은 약화·삭제하고, 핵심 주장이라 그럴 수 없으면 사용자에게 알린다 |
| narrative 계획이 인물·설정을 충분히 정하지 않음 | continuity-keeper가 1장 final에서 캐논을 뽑아 bible을 채운다 |
| 저술가가 계획 분량을 크게 넘겨 씀 (목표의 +15% 초과) | 통합 전에 그 저술가에게 줄일 장과 목표 글자 수를 적어 한 번 되돌린다. editor가 통합하면서 압축하면 저술가의 문장이 깎인다 |
| 표지 생성 실패 | ImageMagick 타이포 표지로 대체하고 알린다 |
| EPUB 빌드 실패 | 에러 메시지를 그대로 보고하고 원고는 보존한다 |

## 파일 규칙

Phase 산출물은 `{NN}_{artifact}.md`(NN = Phase 번호), 챕터는 `chapters/{NN}_draft.md`·`{NN}_final.md`(NN = 챕터 번호). 로그는 역할별 단일 파일(`factcheck_log.md`·`continuity_log.md`)에 `## {NN}장` 섹션으로 append하고, 한 장의 판정이 끝날 때마다 바로 쓴다 — 중단돼도 끝낸 판정은 남는다. 여러 검수자가 같은 로그에 동시에 쓰므로 append는 셸의 `>>`(`cat >> {slug}/factcheck_log.md <<'EOF'`)로만 한다. 파일을 읽어서 통째로 다시 쓰면 그 사이 다른 검수자가 쓴 섹션이 지워진다.
