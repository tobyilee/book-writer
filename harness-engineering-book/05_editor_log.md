# 편집 로그 — 하네스 엔지니어링

- **편집 완료일:** 2026-04-20
- **편집자 역할:** editor 서브에이전트 (통합 편집자)
- **대상 산출물:** 13개 챕터 + 6개 부록 → `04_manuscript.md` 통합 + `book_manifest.json`

## 1. 챕터별 수정 사항

### 수정된 챕터 (용어·인용 형식 통일)

**`chapters/07_final.md`**
- `(GitHub issue #41866)` → `(GitHub Issue anthropic/claude-code#41866)` — 2장에서 확립된 인용 형식 `GitHub Issue anthropic/claude-code#NNNNN`과 통일.

**`chapters/10_final.md`**
- 섹션 제목 `## 롤백과 회복 — worktree, human gate, 그리고 #29684` → `## 롤백과 회복 — worktree, human gate, 그리고 anthropic/claude-code#29684`. 제목에서도 레포 프리픽스를 명시해 본문과 일관.

**`chapters/11_final.md`**
- Contrarian Signal 박스 내 `#29684 고아 커밋 버그` → `GitHub Issue anthropic/claude-code#29684 고아 커밋 버그`로 풀어 씀.
- 같은 박스의 `[§5.10, 확인 필요]` 마크업 → `(확인 필요, 단일 출처)`로 변경. `§5.10` 참조는 리서치 내부 인덱싱이라 독자에게 의미가 없고, 9장 각주 형식과 맞춤.

### 점검 후 수정하지 않기로 결정한 항목

- **`AGENTS.md` vs `CLAUDE.md` 표기:** 8개 `_final.md` 파일 전반에 걸쳐 백틱 인라인 코드(`` `AGENTS.md` `` / `` `CLAUDE.md` ``)로 이미 일관됨. 3장은 `AGENTS.md`를 주로 쓰고 나머지 장은 맥락에 따라 양쪽 모두를 사용하는데, 두 파일이 스펙상 서로 다른 층위이므로 통일이 아니라 **현재 유지가 정확**.
- **arXiv 인용 형식:** 모든 장이 `저자 et al. (연도), 제목, arXiv:XXXX.XXXXX` 형식을 이미 따름. 부록 D에서 정식 재정리.
- **확인 필요 태그:** 9장·11장에서 각주 형태로 정직하게 표기됨. 추가 개입 불필요.
- **`DB` / `데이터베이스` 혼용:** 3장(2건)·11장(2건) 모두 `DB`로 일관. 본문에 `데이터베이스` 표기는 없음.

## 2. 부록 집필 완료

6개 부록 모두 plan v2 스펙 준수하며 작성.

| 부록 | 경로 | 예상 분량 | 실제 문자수 | 상태 |
|---|---|---:|---:|---|
| A 용어집 | `appendices/A_glossary.md` | 2,500자 | 6,454자 | 완료 |
| B AGENTS.md 템플릿 5종 | `appendices/B_agents_md_templates.md` | 3,000자 | 7,949자 | 완료 |
| C 체크리스트 모음 | `appendices/C_checklists.md` | 2,500자 | 6,942자 | 완료 |
| D 참고문헌 | `appendices/D_references.md` | 3,000자 | 15,605자 | 완료 |
| E 캡스톤 워크북 | `appendices/E_capstone_workbook.md` | 4,000자 | 8,010자 | 완료 |
| F 팀 온보딩 키트 | `appendices/F_team_onboarding_kit.md` | 2,500자 | 9,753자 | 완료 |

부록 D는 plan 예상 분량 3,000자 대비 실제 15,605자로 확장됨. 학술 27편 + 1차 웹 자료 + 2차 해설 + GitHub Issues + 커뮤니티 토론 + 한국어 자료 + 단일 출처 별도 섹션까지 전부 통합하면서 자연스럽게 늘어남. 축약 시 실용성이 떨어져 확장본 유지 결정.

다른 부록도 plan 예상 분량을 상회하나, 분량보다 **본문 cross-ref 정합성**을 우선해 유지.

## 3. 통합 원고 생성 결과

- **파일:** `04_manuscript.md`
- **구성:** 표지 메타 + 작가의 말 + 목차 → 서문~12장 → 부록 A~F
- **장 경계:** 각 섹션 앞에 `---` (h1 헤더는 각 챕터 원본의 것을 그대로 유지, EPUB 빌더가 인식)
- **총 문자수:** 약 306,000자 (공백 포함) / 본문 순 글자 기준 약 115,000~120,000자 (plan 예산 +5,000자 근처)

챕터 원문은 **임의 재해석하지 않음**. 전환부와 인용 형식만 손봄. 이 결정은 plan의 "챕터 독립성 유지" 지시와 editor 스킬 원칙("저술가의 목소리 존중, 전체 윤문을 새로 하지 않는다")을 따른 것.

## 4. 발견한 불일치와 해결 내역

| # | 발견 | 해결 |
|---|---|---|
| 1 | `GitHub issue #41866` (7장) vs `GitHub Issue anthropic/claude-code#42796` (2장) 프리픽스 유무 | 7장을 2장 형식으로 맞춤. |
| 2 | 10장 섹션 제목이 `#29684`만 단독 표기 | 섹션 제목과 본문 모두 레포 프리픽스 명시. |
| 3 | 11장 Contrarian 박스에서 `[§5.10, 확인 필요]` 내부 인덱스 참조 | 독자 친화적 `(확인 필요, 단일 출처)`로 변경. |

## 5. 버려진 결정

- **전체 용어 사전 pass를 통한 한영 혼용 통일 제안:** 에디터 지침상 "내용 변경 금지, 표현만"이므로 본문 전면 리터치는 범위 밖. 대신 부록 A 용어집에서 6개 주제 그룹으로 묶어 독자가 단일 entry point로 쓸 수 있게 함.
- **9장·11장의 "확인 필요" 각주를 통합 편집자가 재검증:** 원 리서치에서 단일 출처로 태깅된 내용은 editor가 재검증할 자료가 아님. 저자의 태깅을 존중하고 부록 D §7에 별도 섹션으로 모아 투명성만 추가 확보.

## 6. EPUB 빌더에 전달할 메타

`book_manifest.json`에 다음 필드를 채움:
- `title`: "하네스 엔지니어링"
- `subtitle`: "Claude Code와 Codex로 에이전트를 프로덕션에 태우는 법"
- `author`: "Toby-AI"
- `language`: "ko"
- `pub_date`: "2026-04-20"
- `identifier`: `urn:uuid:7e3c5f2a-8b4d-4a19-b7a2-harness-eng-v1`
- `version`: "1.0.0"
- `manuscript`: "04_manuscript.md"
- `cover_image`: "cover.png" (별도 cover-design 에이전트가 생성 예정)
- `description`: 한 문단 소개 포함
- `keywords`: 10개

## 7. 체크포인트

- [x] 13개 챕터 일관성 점검 및 필요 수정 적용 완료
- [x] 부록 A~F 6개 파일 저장
- [x] 04_manuscript.md 저장 (통합 원고)
- [x] book_manifest.json 저장
- [x] 05_editor_log.md 저장

## 8. 다음 단계에 필요한 것

- **cover-design 에이전트**: `cover.png` 생성 (1600×2560, plan §A 후보 1의 "담백한 전문서적" 톤)
- **style-guardian**: 통합 원고 최종 스타일 점검 요청 가능하지만, 이번 세션에서는 편집자 개입을 최소화했으므로 필수는 아님
- **epub-build 스킬**: `04_manuscript.md` + `book_manifest.json` + `cover.png`로 `하네스 엔지니어링-v1.0.0.epub` 빌드
