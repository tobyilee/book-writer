# Build Log — 시니어의 학습법 v1.0.0

- **Date:** 2026-05-04T10:47:20Z
- **Build script:** `/Users/tobylee/workspace/ai/book-writer/.claude/skills/epub-build/scripts/build_epub.sh ultimate-focus-super-learning`

## EPUB 산출물

- **Output:** `/Users/tobylee/workspace/ai/book-writer/시니어의-학습법-v1.0.0.epub`
- **Size:** 155,976 bytes (152 KB)
- **Pandoc exit code:** 0
- **File size check:** PASS (≥ 50KB)
- **epubcheck:** PASS (exit code 0, 경고 없음, `/Users/tobylee/.pyenv/shims/epubcheck`)

## 책 소개 markdown 산출물

- **Output:** `/Users/tobylee/workspace/ai/book-writer/시니어의-학습법-v1.0.0.md`
- **Size:** 7,559 bytes (약 3,931자)
- **Logline:** "5년차에 무너지기 시작한 학습 ROI를, 6개 레이어로 분해해 다시 작동하게 만든다."
- **구성:** 한 줄 logline → 메타 → 이 책은 무엇인가(4문단) → 누구를 위한 책인가(진입/출구 상태 + 신호 체크리스트) → 무엇을 얻게 되는가(6개 핵심 약속) → 차례(8개 챕터) → 저자 소개 → 책 정보
- **소스:** 02_plan.md(독자 여정·내러티브 아크), 04_manuscript.md(실제 1단계 헤딩), book_manifest.json(메타)

## 입력

- 통합 원고: `ultimate-focus-super-learning/04_manuscript.md` (1,057줄, 73,863자)
- 표지: `ultimate-focus-super-learning/cover.png` (1600×2560, 92KB)
- 매니페스트: `ultimate-focus-super-learning/book_manifest.json`

## Metadata

- **title:** 시니어의 학습법
- **subtitle:** FIT, PACER, RAIL로 다시 짜는 집중과 학습의 운영체제
- **author:** Toby-AI
- **language:** ko
- **version:** 1.0.0
- **pub_date:** 2026-05-04
- **identifier:** urn:uuid:82c4c88f-0cdc-42f0-b96e-275eeee0d036

## 챕터 구조 (manuscript H1 추출)

1. 프롤로그. 5년차 정체기의 풍경 — 왜 시니어일수록 학습이 더 어려워지는가
2. 1장. 집중력과 저항의 심리학 — 의지가 아니라 환경
3. 2장. 잘못된 학습 미신과 시스템의 재구축 — Enablers / Encoding / Retrieval
4. 3장. 지식을 지배하는 정보 구조화 기술 — PACER와 GRINDE
5. 4장. 초고속 스킬 습득과 한계 돌파 — RAIL과 정밀 연습
6. 5장. AI 시대의 생산성과 대체 불가한 뇌 — Cognitive Debt와 Bloom 상위 3단계
7. 6장. 상위 1%의 메타인지와 멘탈 모델 — 종이에 생각하기
8. 에필로그. 1년 후 자가 진단 체크리스트

## 노트

- 동일 버전(v1.0.0) 기존 산출물 없음 — 신규 빌드
- 결정적 빌드: build_epub.sh가 매니페스트의 identifier(UUID)를 그대로 사용
- 산출 정책: 프로젝트 루트에 EPUB과 책 소개 md를 같은 stem(`시니어의-학습법-v1.0.0`)으로 짝지어 공존
