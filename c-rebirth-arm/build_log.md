# Build Log — 다시, C v1.0.0

- **Date:** 2026-05-18T00:55:36Z
- **Output:** `다시,-C-v1.0.0.epub`
- **Size:** 359898 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed

## Metadata
- title: 다시, C
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-05-18
- license: CC BY-NC-SA 4.0
- harness_version: 1.2.0
- rights: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0

## 책 소개 markdown

- 경로: `../다시,-C-v1.0.0.md` (프로젝트 루트, EPUB 옆)
- 구성: logline · 책 설명(4문단) · 대상 독자(4 bullet) · 핵심 약속(9 bullet) · 차례(15장 + 부록 안내) · 저자 소개 · 책 정보
- 소스: book_manifest.json (메타), 02_plan.md (독자 여정·내러티브 아크·핵심 질문), 04_manuscript.md (실제 차례)

## 콜로폰 정합성 점검

- 매니페스트 license `CC BY-NC-SA 4.0` ↔ 본문 `## 판권` 일치
- 매니페스트 version `1.0.0` ↔ 본문 판본 `v1.0.0` 일치
- 매니페스트 pub_date `2026-05-18` ↔ 본문 발행일 `2026-05-18` 일치
- 매니페스트 harness_version `1.2.0` ↔ 본문 생성 도구 `book-writer 하네스 v1.2.0` 일치
- 매니페스트 identifier `urn:uuid:cff26257-706f-4c6f-9041-28d413530b31` ↔ 본문 식별자 일치
- OPF `<dc:rights>` `© 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0` 확인

## 검증

- EPUB 내부 구조: mimetype + META-INF/container.xml + EPUB/content.opf + 19 chapter xhtml + cover.xhtml + nav.xhtml + toc.ncx
- 콜로폰 챕터(ch019): `## 판권` 섹션이 EPUB 내부에 정상 임베드됨
- epubcheck: passed (no errors)
