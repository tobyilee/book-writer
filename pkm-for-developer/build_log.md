# Build Log — 수집을 지식으로 — 50대 개발자를 위한 PKM 다시 짜기 v1.0.0

- **Date:** 2026-05-10T06:48:05Z
- **Output (EPUB):** `수집을-지식으로-v1.0.0.epub` (프로젝트 루트)
- **Output (책 소개 md):** `수집을-지식으로-v1.0.0.md` (프로젝트 루트, EPUB과 같은 폴더)
- **Size:** 271017 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed (exit 0, no warnings)

## Metadata

- title: 수집을 지식으로 — 50대 개발자를 위한 PKM 다시 짜기
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-05-10
- identifier: pkm-for-developer-v1.0.0
- license: CC BY-NC-SA 4.0
- harness_version: 1.2.0
- rights: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0

## OPF 메타 검증

- `dc:identifier` = `pkm-for-developer-v1.0.0` ✓
- `dc:title` = 풀제목 ✓
- `dc:creator` = `Toby-AI` ✓
- `dc:date` = `2026-05-10` ✓
- `dc:language` = `ko` ✓
- `dc:rights` = `© 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0` ✓
- `dc:description` = 매니페스트 description ✓

## 정합성 점검

- 매니페스트 `license`/`version`/`date` ↔ 04_manuscript.md `## 판권` 섹션 일치 ✓
  - 라이선스: CC BY-NC-SA 4.0
  - 버전: v1.0.0
  - 발행일: 2026년 5월 10일
  - 식별자: pkm-for-developer-v1.0.0
  - 하네스: book-writers v1.2.0

## 파일명 처리

빌드 스크립트는 매니페스트의 `title`을 슬러그화해 풀제목 파일명을 만든다 — `수집을-지식으로-—-50대-개발자를-위한-PKM-다시-짜기-v1.0.0.epub`. 사용자 요청에 따라 짧은 stem `수집을-지식으로-v1.0.0.epub`으로 rename. EPUB 내부 메타(OPF의 `dc:title`)는 풀제목을 유지하므로 서지정보·콜로폰과 일관.

## 빌드 절차

1. 매니페스트 검증 → `identifier`, `pub_date` 필드 추가 (epubcheck `RSC-005` 회피용)
2. `bash .claude/skills/epub-build/scripts/build_epub.sh pkm-for-developer`
3. 산출물 rename: 풀제목 stem → 짧은 stem
4. epubcheck 재검증 (exit 0)
5. 책 소개 markdown 작성 (외부 독자용 — logline·대상 독자·핵심 약속·차례·저자 소개·책 정보)

## 변경 사항 (book_manifest.json)

- `pub_date: "2026-05-10"` 추가 (`date`와 동일, build_epub.sh의 `read_field pub_date` 호환)
- `identifier: "pkm-for-developer-v1.0.0"` 추가 (epubcheck 통과를 위한 dc:identifier)
