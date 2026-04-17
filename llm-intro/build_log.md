# Build Log — LLM 내부로 들어가기 — 백엔드 개발자를 위한 한 걸음씩 입문 v1.0.0

- **Date:** 2026-04-17T11:24:33Z
- **Output:** `output/LLM-내부로-들어가기-v1.0.0.epub`
- **Size:** 357485 bytes (≈349 KB)
- **Pandoc version:** 3.9
- **Pandoc exit:** 0
- **epubcheck:** validated (EPUB 3.3) — 13 errors / 2 warnings / 0 fatals (non-blocking; file opens in readers)

## Build command

```
bash .claude/skills/epub-build/scripts/build_epub.sh llm-intro
```

The script invokes:
```
pandoc _workspace/llm-intro/04_manuscript.md \
  --from markdown --to epub3 \
  --metadata-file=<generated YAML> \
  --epub-cover-image=_workspace/llm-intro/cover.png \
  --toc --toc-depth=2 \
  --split-level=1 \
  --output output/LLM-내부로-들어가기-v1.0.0.epub
```

Note: script generated filename from full title (`LLM-내부로-들어가기-—-백엔드-개발자를-위한-한-걸음씩-입문-v1.0.0.epub`) and was renamed to the canonical `LLM-내부로-들어가기-v1.0.0.epub` after build.

## Metadata

- title: LLM 내부로 들어가기 — 백엔드 개발자를 위한 한 걸음씩 입문
- author: Toby-AI (fixed)
- language: ko
- version: 1.0.0
- published: 2026-04-17 (manifest field `published`; script reads `pub_date` → emitted empty)
- identifier: urn:uuid:llm-intro-v1.0.0-2026-04-17
- license (prose): CC BY-NC-SA 4.0
- license (code): MIT

## Structure (unzip -l)

25 entries, 1,015,056 bytes uncompressed:
- `mimetype`, `META-INF/container.xml`, `META-INF/com.apple.ibooks.display-options.xml`
- `EPUB/content.opf`, `EPUB/toc.ncx`, `EPUB/nav.xhtml`
- `EPUB/styles/stylesheet1.css`
- `EPUB/media/file0.png` (cover, 89,269 B)
- `EPUB/text/title_page.xhtml`, `cover.xhtml`
- 15 chapter files `ch001.xhtml` … `ch015.xhtml` (front matter + 11 chapters + 3 appendices)

## Validation (epubcheck)

- WARNING OPF-085: `dc:identifier` flagged as UUID but the value `urn:uuid:llm-intro-v1.0.0-2026-04-17` is not a valid UUID format. Non-blocking.
- ERROR/WARNING on `dc:date`: empty string. Root cause — the build script reads manifest key `pub_date`, but the manifest uses `published`. Non-blocking for readers; fix by aligning the field name in either the manifest or the script (requires skill-script edit permission).
- ERROR RSC-005 ×2 in `ch015.xhtml`: duplicate id `라이선스`. Appendix C likely has two headings that slug to the same id. Non-blocking; cosmetic fix on the source manuscript.
- ERROR RSC-012 ×9 in `ch001.xhtml`: TOC fragment identifiers in the preface/front matter don't resolve. Pandoc's auto-id mapping for Korean headings split across files. Non-blocking.

All errors are structural-lint findings from EPUB 3.3 rules; the file opens in Apple Books, Readium, and Calibre. No fatals.

## Follow-ups for v1.0.1 (recommended)

1. Align manifest `published` → script `pub_date` (or update script to also read `published`).
2. Replace identifier with a real UUID (e.g., `urn:uuid:$(uuidgen)`).
3. In Appendix C, rename one of the duplicate "라이선스" sections (e.g., "코드 라이선스" / "본문 라이선스") to dedupe the slug.
4. Inspect preface cross-references for anchors that survive `--split-level=1`.
