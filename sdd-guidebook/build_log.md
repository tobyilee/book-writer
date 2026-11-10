# Build Log — AI 에이전트와 함께하는 스펙 주도 개발 v1.0.0

- **Date:** 2026-11-10T05:38:33Z
- **Output:** `AI-에이전트와-함께하는-스펙-주도-개발-v1.0.0.epub`
- **Size:** 2305099 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed
- **epubcheck strict:** 1
- **mermaid:** rendered to figures/fig-NN.svg via mmdc
- **images:** 18 local reference(s), all present
- **cover alt:** injected alt="어두운 청색 블루프린트 격자 위에 스펙 문서의 요구사항 줄이 앰버색 선을 따라 코드 줄로 이어지는 그림과 제목 '스펙 주도 개발'"

## Metadata
- title: AI 에이전트와 함께하는 스펙 주도 개발
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-11-10
- identifier: urn:uuid:35706d4e-d35e-49da-bea9-cddd79ade8a6
- license: CC BY-NC-SA 4.0
- genre: tech-book
- cover_alt: 어두운 청색 블루프린트 격자 위에 스펙 문서의 요구사항 줄이 앰버색 선을 따라 코드 줄로 이어지는 그림과 제목 '스펙 주도 개발'
- stylesheet: epub.css
- harness_version: 2.0.0
- rights: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0

## Build history and verification (epub-builder)

- **Command:** `bash .claude/skills/epub-build/scripts/build_epub.sh sdd-guidebook` (from project root)
- **Attempt 1: FAILED (epubcheck, exit 5).** 1 fatal / 6 errors:
  `FATAL(RSC-016): .../EPUB/text/ch004.xhtml(100,189): Fatal Error while parsing file: Attribute name "사전조건" associated with an element type "선택적" must be followed by the ' = ' character.`
  The 6 `RSC-012 Fragment identifier is not defined` errors (toc.ncx, nav.xhtml) came from the same broken file.
  Cause: in `04_manuscript.md` line 445 (3장, EARS 일반형), pandoc parsed the placeholders `<선택적 사전조건>`, `<선택적 트리거>`, `<시스템 이름>`, `<시스템 응답>` as raw HTML tags.
  Fix: escaped them as `\<…\>` on that line only. The displayed text is unchanged; the EPUB now shows `While <선택적 사전조건>, when <선택적 트리거>, the <시스템 이름> shall <시스템 응답>.`
  The failed EPUB was moved to `_prev/AI-에이전트와-함께하는-스펙-주도-개발-v1.0.0.failed-epubcheck.epub`.
- **Attempt 2: PASSED.** epubcheck (EPUB 3.4 rules): `No errors or warnings detected. Messages: 0 fatals / 0 errors / 0 warnings / 0 infos`
- **Size:** 2,305,099 bytes
- **Mermaid:** 18 fenced blocks in manuscript → 18 SVGs (`figures/fig-01..18.svg`). No fence left as code in the EPUB, no `syntax error` SVG, no `<foreignObject>`.
  - timeline: fig-04 (4장), fig-18 (12장). Both render with real labels.
  - quadrantChart: fig-06 (5장). Renders with axis and quadrant labels.
- **Images:** 18 local references, all present (no MISSING)
- **OPF:** identifier `urn:uuid:35706d4e-d35e-49da-bea9-cddd79ade8a6` (preserved), dc:date 2026-11-10, dc:subject tech-book, dc:rights `© 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0`
- **Colophon (`## 판권`) vs manifest:** matches. Version v1.0.0, 발행일 2026-11-10, license `CC BY-NC-SA 4.0`, identifier, and harness v2.0.0 are all the same.
- **Cover alt:** injected from `cover_alt`
- **책 소개:** `AI-에이전트와-함께하는-스펙-주도-개발-v1.0.0.md` (project root, same stem as EPUB)
