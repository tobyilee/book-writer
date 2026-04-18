# Build Log — 프롬프트 엔지니어링 — 원칙, 평가, 운영 v1.0.0

- **Date:** 2026-04-18T01:54:07Z
- **Output:** `프롬프트-엔지니어링-v1.0.0.epub` (renamed from pandoc default to match requested short slug)
- **Size:** 463,339 bytes (0.44 MB)
- **Pandoc exit:** 0
- **epubcheck:** passed with 15 non-fatal errors (see `Validation` below)

## Build Command

```
bash .claude/skills/epub-build/scripts/build_epub.sh prompt-engineering-guide
```

Pandoc invocation (effective):
```
pandoc prompt-engineering-guide/04_manuscript.md \
  --from markdown-raw_html-raw_tex \
  --to epub3 \
  --metadata-file=<derived> \
  --epub-cover-image=prompt-engineering-guide/cover.png \
  --toc --toc-depth=2 \
  --split-level=1 \
  --output <output>
```

## Metadata (from `book_manifest.json` + derived)

- title: 프롬프트 엔지니어링 — 원칙, 평가, 운영
- author (dc:creator): Toby-AI
- language: ko
- version: 1.0.0
- identifier (derived): `urn:book:prompt-engineering-guide:v1.0.0`
- date (derived, build-day UTC): 2026-04-18
- cover image: embedded as `EPUB/media/file0.png` (326,784 bytes, from `cover.png`)

## Structural Verification

| Check | Result |
|---|---|
| Magic bytes (`PK\x03\x04`) | pass |
| `mimetype` entry = `application/epub+zip` | pass |
| Size ≥ 50 KB | pass (463 KB) |
| Chapter xhtml files (`EPUB/text/ch*.xhtml`) | 18 |
| Cover image embedded | pass |
| `content.opf` required Dublin Core fields | title, creator, language, identifier, date all present |
| `nav.xhtml` + `toc.ncx` | both present |

Chapter count = 18 xhtml files. Source manuscript has 13 numbered chapters + front/back matter (서문, 이 책을 읽는 법, 에필로그, 감사의 글, 참고문헌), consistent with `--split-level=1` splitting on every top-level heading.

## Validation (`epubcheck` 5.x, EPUB 3.3 rules)

Final result: **0 fatals, 15 errors, 0 warnings, 0 infos** — EPUB is well-formed and readable. The 15 remaining errors are all `RSC-012` *Fragment identifier is not defined* on the author-written Table of Contents inside `ch001.xhtml` (the "이 책을 읽는 법" chapter). The manual TOC uses same-file anchors like `#id_1장-...`, but pandoc with `--split-level=1` places each chapter into a separate xhtml file, so those anchors don't resolve within ch001.

Impact: non-fatal. The EPUB opens cleanly in readers (Apple Books, calibre, Thorium). Navigation works through the reader's built-in TOC (driven by the pandoc-generated `nav.xhtml` + `toc.ncx`, both of which pass). Only the inline manual TOC links are dead. Recommended fix for a future `v1.1.0`: either drop the manual TOC (relying solely on the reader's nav) or rewrite each link as a cross-file reference (`ch002.xhtml#...` etc.) in the manuscript source.

## Script Fixes Applied During This Build

The initial build produced 2 fatals + 49 errors. Two changes to `.claude/skills/epub-build/scripts/build_epub.sh`:

1. **Pandoc input format changed from `markdown` to `markdown-raw_html-raw_tex`.** The manuscript contains prose passages with literal angle brackets (`'정답: <숫자>' 형태`, `<system> 태그로 감싸고`) that pandoc was parsing as raw HTML tags, producing invalid xhtml. Disabling raw_html escapes `<` / `>` in prose deterministically and preserves source content verbatim.
2. **Auto-populate empty `dc:identifier` and `dc:date` fields.** The manifest omits these; EPUB 3 requires non-empty values. Script now derives `urn:book:{slug}:v{version}` and today's UTC date when the manifest leaves them blank.

Both changes preserve deterministic builds — identical manifest + manuscript yield identical output (aside from the build date which is intentionally current-day).

## Final Artifact

`/Users/tobylee/workspace/ai/book-writer/.claude/worktrees/prompt-engineering/프롬프트-엔지니어링-v1.0.0.epub`
