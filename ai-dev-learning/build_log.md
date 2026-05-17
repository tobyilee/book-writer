# Build Log — 바이브 너머의 엔지니어 v1.0.0

- **Date:** 2026-05-17T04:36:38Z
- **Output:** `바이브-너머의-엔지니어-v1.0.0.epub`
- **Size:** 2820370 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed

## Metadata
- title: 바이브 너머의 엔지니어
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-05-17
- license: CC BY-NC-SA 4.0
- harness_version: 1.2.0
- rights: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0

## Companion Files

- **책 소개 markdown:** `바이브-너머의-엔지니어-v1.0.0.md` (외부 독자용 — 블로그·스토어·SNS 공유 카피)

## Verification

- **EPUB 파일:** `바이브-너머의-엔지니어-v1.0.0.epub` — 2,820,370 bytes (2.82 MB)
- **표지 임베드:** `EPUB/media/file0.png` (2,699,338 bytes, `properties="cover-image"`)
- **OPF 메타:**
  - `dc:identifier` = `urn:uuid:beyond-the-vibe-v1.0.0`
  - `dc:title` = 바이브 너머의 엔지니어
  - `dc:creator` = Toby-AI (role=aut)
  - `dc:date` = 2026-05-17
  - `dc:language` = ko
  - `dc:rights` = © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0
- **콜로폰 정합성:** manuscript의 `## 판권` 섹션이 매니페스트의 license/version/pub_date/identifier/harness_version과 일치
- **epubcheck:** passed (1 warning — OPF-085, slug-style identifier flagged as non-RFC4122 UUID; not a spec violation, no distribution impact)
- **빌드 명령:** `bash .claude/skills/epub-build/scripts/build_epub.sh ai-dev-learning` (pandoc 3.9.0.2, epub3 target, `--toc --toc-depth=2 --split-level=1`)

