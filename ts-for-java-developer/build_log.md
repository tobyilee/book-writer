# Build Log — 왜 TypeScript는 이렇게 생겼는가 v1.0.0

- **Date:** 2026-05-04T10:36:09Z
- **Output:** `왜-TypeScript는-이렇게-생겼는가-v1.0.0.epub`
- **Size:** 590773 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed (errors: 0, fatals: 0)
- **책 소개 md:** `/Users/tobylee/workspace/ai/book-writer-3/.claude/worktrees/ts-for-java-developer/왜-TypeScript는-이렇게-생겼는가-v1.0.0.md`

## Metadata
- title: 왜 TypeScript는 이렇게 생겼는가
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-05-04

## 재빌드 노트 (이전 빌드 FATAL 해소)

이전 빌드에서 `ch011.xhtml:1376` 위치의 RSC-005/016 FATAL 오류 원인은 **7장 비동기 챕터의 헤딩 `### Awaited<T> 유틸리티 타입`**이었다 (사용자가 짚은 11장 JSX 코드 펜스 문제와는 별개의 잔여 이슈). pandoc은 마크다운 헤딩 안의 `<T>`를 raw inline HTML로 흘려보냈고, XHTML 파서가 닫히지 않은 `<T>` 태그로 해석해 FATAL을 냈다.

**수정:** 다음 두 파일의 헤딩을 `### \`Awaited<T>\` 유틸리티 타입`으로 백틱 감쌈.
- `04_manuscript.md:6278`
- `chapters/07_draft.md:1180`

재빌드 후 epubcheck passed (errors: 0, fatals: 0). LOW severity 잔여 경고도 없음.
