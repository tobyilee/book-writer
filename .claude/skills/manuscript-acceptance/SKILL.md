---
name: manuscript-acceptance
description: Whole-book acceptance gate run by a fresh-context reviewer before EPUB build (Phase 4.5). Cross-reads the integrated manuscript against the plan, research ledger, and logs, scans for forbidden leftover markers, checks terminology/voice/variation, cross-reference and promise integrity, and emits {slug}/05_acceptance.md with per-criterion PASS/BLOCK + owner-tagged fixes. Genre-agnostic; complements the per-chapter fact/continuity passes. Triggers on "수락 검수", "통권 검수", "manuscript acceptance", "최종 통과 게이트".
---

# Manuscript Acceptance

통합 원고(`04_manuscript.md`)가 Phase 5로 넘어가기 전 책 전체를 판정하는 게이트다. 원고를 만든 editor와 다른 새 컨텍스트가 수행한다. 챕터 단위 사실·연속성 패스를 다시 하지 않고, 잔여 미결과 통권 단위 문제만 본다. 기본 흐름에는 별도 스타일 검수가 없으므로 voice 이탈도 여기서 잡는다.

없는 로그가 대상인 기준(예: essay의 사실 로그)은 N/A PASS로 두고 이유를 한 줄 적는다.

## 수락 기준

| ID | 기준 | 확인 방법 | BLOCK 시 담당 |
|----|------|----------|--------------|
| (a) | 챕터 완비·분량 균형 | 플랜의 챕터 목록 ↔ 원고 `# N장` 헤딩 1:1 대조. `length_report.py`로 원고의 분량을 직접 재고 중앙값 대비 70% 미만·150% 초과 장, 계획 대비 ±20% 밖인 장을 본다 | 해당 장 `chapter-writer` |
| (b) | 미해소 마커 0건 | 아래 grep | 사용자 (빌드 중단) |
| (c) | 사실 미결 해소 | `factcheck_log.md`의 `미해소`. (tech-book) 참고문헌 항목의 식별자·확인 등급 라벨을 `research/*.md`와 표본 대조한다. 로그에서 정정·약화된 주장이 다른 장·부록·참고문헌에 옛 표현으로 남아 있는지, 같은 수치·버전이 장마다 다르게 쓰였는지 grep으로 본다 | `fact-checker` / 해결 불가면 사용자 (빌드 중단) |
| (d) | 용어·voice·변주 | 핵심 용어 표기 흔들림. 여러 장을 표본으로 활성 `style-checklist.md`에 비춰 voice 이탈(번역투, 강압 어조, 과포화 말버릇, 메타 선언 오프닝)을 본다. `editor_notes.md`의 변주 표를 참고해 오프닝·클로징이 같은 틀로 반복되는지 본다. 하네스 내부 역할·파일 이름("리서처", `research/…`)이 지면에 새지 않았는지 본다 | 한두 장이면 해당 장 `chapter-writer`, 통권 문제면 `editor`, 여러 장의 voice 이탈이면 `style-guardian` |
| (e) | 상호 참조·예제 정합 | "앞서 N장에서 ~" 류 콜백과 "N장에서 다룬다" 류 예고가 실제로 그 장의 내용을 가리키는지. 러닝 예제가 있으면 계획의 "공유 정전"을 기준으로 이름·경로·스키마·시그니처가 장마다 같은지, 뒤 장의 코드가 앞 장의 코드에서 실제로 이어지는지 표본 대조한다 | `editor` |
| (f) | 약속 이행 | 매니페스트 `description`과 계획의 독자 여정이 약속한 범위를 원고가 다루는지 | `editor`, 본질적 미달이면 사용자 |
| (g) | 부속 자료·구조 | 콜로폰(`## 판권`)과 장르별 부속 — tech-book: 서문·에필로그·참고문헌 / narrative: 작가의 말 / practical: 이 책 활용법·준비물 총정리 / essay: 머리말. 에필로그·부록·참고문헌이 `#` 헤딩인지(`##`면 마지막 장에 흡수된다), 모든 장에 `##` 절이 있는지(없으면 목차에 절이 실리지 않는다), 참고문헌이 공개 출처를 링크로 가리키는지 | `editor` |
| (h) | 연속성 (narrative) | `continuity_log.md`의 `미해소`, `story_bible.md` 복선 원장의 미회수 항목 | `chapter-writer` / 의도 확인은 사용자 |

## 절차

1. 금지 마커를 grep한다. 한 건이라도 있으면 (b) BLOCK이며 줄 번호와 원문을 기록한다.
   ```bash
   grep -nE "\(사실 확인 필요\)|\[리서치 공백\]|\[미완성\]" {slug}/04_manuscript.md
   ```
2. 챕터 완비와 분량을 확인한다.
   ```bash
   grep -nE "^# [0-9]+장" {slug}/04_manuscript.md
   python3 .claude/skills/book-editing/scripts/length_report.py {slug}
   ```
3. 콜백·예고를 모아 가리키는 장이 맞는지 본다. 장 번호가 붙은 참조는 모두 대상이다.
   ```bash
   grep -nE "[0-9]+장(에서|의 |에 |으로|을 |를 |과 |와 |부터|까지)|부록 [A-Z]" {slug}/04_manuscript.md
   ```
   구조도 함께 본다 — 장 뒤 부속이 `#`인지, 절 없는 장이 있는지.
   ```bash
   grep -nE "^#{1,2} (에필로그|참고문헌|부록|작가의 말|맺음말)" {slug}/04_manuscript.md
   awk '/^# [0-9]+장/{if(ch&&!n)print ch; ch=$0; n=0} /^## /{n++} END{if(ch&&!n)print ch}' {slug}/04_manuscript.md
   ```
4. 로그의 잔여 미결을 본다.
   ```bash
   grep -nE "미해소" {slug}/factcheck_log.md {slug}/continuity_log.md 2>/dev/null
   ```
5. (c)의 참고문헌 표본 대조와 정정 잔존 grep, (d)의 voice·변주, (e)의 예제 정합, (f)(g)를 판정한다. 말버릇 반복 횟수는 grep으로 센다. grep은 대소문자·띄어쓰기 변형 때문에 오탐·누락이 나므로, 일치한 줄을 읽어 본 뒤 판정한다.
6. `05_acceptance.md`를 쓴다.

## 평결

- **ACCEPT** — 모든 기준 PASS.
- **BLOCK** — 하나 이상 BLOCK. 오케스트레이터가 조치를 담당자에게 한 번 보내고, 영향받은 기준만 재판정한다. 재판정 후에도 BLOCK이면 사용자가 판단한다. 담당자는 `04_manuscript.md`를 직접 고치므로(통합 뒤의 정본이다) 조치에는 원고의 줄 번호나 절 제목을 적는다.
- BLOCK까지는 아닌 발견은 "비차단 권고"로 따로 적는다. 오케스트레이터가 빌드 전에 editor에게 한 번에 넘길 수 있다.
- (b)(c)는 사용자가 명시적으로 승인하지 않는 한 PASS가 될 수 없다. 승인했으면 그 사실과 범위를 기록한다.

## 출력 형식

```markdown
# 수락 검수: {책 제목}

<!-- 검수: {날짜} · 라운드 {N} · manuscript-reviewer (fresh context) -->

## 기준 판정

| ID | 기준 | 판정 | 근거 |
|----|------|------|------|
| (a) | 챕터 완비·분량 균형 | PASS | 플랜 8장 = 원고 8장, 플래그 0 |
| (b) | 미해소 마커 0건 | PASS | grep 0건 |
| (c) | 사실 미결 해소 | PASS | 미해소 0건, 참고문헌 표본 6건 원장 일치 |
| (d) | 용어·voice·변주 | BLOCK | 4·5·6장 모두 '상황 가정' 오프닝, 6장 "기억해두자" 11회 |
| (e) | 상호 참조 무결성 | PASS | 콜백 6건 정합 |
| (f) | 약속 이행 | PASS | ... |
| (g) | 부속 자료 완비 | PASS | ... |
| (h) | 연속성 | N/A | tech-book |

## 평결

BLOCK

## 조치

| 기준 | 심각도 | 담당 | 조치 |
|------|--------|------|------|
| (d) | 중간 | chapter-writer 5장 | 오프닝을 '실패 장면'으로 교체 (계획 배정과 일치시킴) |
| (d) | 낮음 | chapter-writer 6장 | "기억해두자" 11회 → 4회 이하로, 나머지는 평어체 |

## 비차단 권고

- {기준} {위치} — {권고}
```

재검수면 새 라운드를 append하고, 이전 조치의 해소 여부를 먼저 적은 뒤 영향받은 기준만 다시 판정한다.
