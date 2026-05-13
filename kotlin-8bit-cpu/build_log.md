# Build Log — 코드로 짓는 CPU v1.0.0

- **Date:** 2026-05-13T01:30:15Z
- **Output:** `코드로-짓는-CPU-v1.0.0.epub`
- **Size:** 1147313 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed

## Metadata
- title: 코드로 짓는 CPU
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-05-13
- license: CC BY-NC-SA 4.0
- harness_version: 1.2.0
- rights: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0

## Companion artifact

- **책 소개 markdown:** `코드로-짓는-CPU-v1.0.0.md` (프로젝트 루트, EPUB 옆)

## Verification

- [x] EPUB 파일 생성 (1,147,313 bytes, ≥ 50KB)
- [x] EPUB 내부 구조 정상 (`mimetype`, `META-INF/`, `EPUB/content.opf`, 22 챕터 xhtml, 표지 PNG 869 KB 포함, 총 32 파일)
- [x] 표지가 `EPUB/text/cover.xhtml`로 첫 페이지에 배치됨 (`<reference type="cover">`)
- [x] 차례 자동 생성 (`EPUB/nav.xhtml` 24 KB, `EPUB/toc.ncx` 40 KB, toc-depth=2, split-level=1)
- [x] OPF에 `<dc:rights>© 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0</dc:rights>` 정상 노출
- [x] 본문 `## 판권` 섹션이 매니페스트의 license/version/pub_date/harness_version과 일치 (drift 없음)
- [x] epubcheck 3.3 통과 — 0 errors / 1 warning (`OPF-085`: UUID 형식 경고, 동작 영향 없음)
- [x] 책 소개 md가 EPUB과 같은 폴더에 존재하고 차례·저자·버전이 매니페스트와 일치

## 빌드 노트

- 첫 시도는 매니페스트 `description` 필드 안의 `\"정확도\"`(JSON 디코딩 후 실제 `"` 문자)가 pandoc 메타 YAML의 더블쿼트 안에서 충돌해 exit 64로 실패.
- 매니페스트 description의 `"정확도"`를 한국어 인용부호 `‘정확도’`로 교체한 뒤 재빌드 성공. 콜로폰/차례/본문 의미와 무관한 안전 수정.
