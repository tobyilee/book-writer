# Build Log — 코드 밖에서 결정된다 v1.0.0

- **Date:** 2026-05-03T13:37:31Z
- **Output:** `코드-밖에서-결정된다-v1.0.0.epub`
- **Size:** 2276593 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed

## Metadata
- title: 코드 밖에서 결정된다
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-05-03
- identifier: urn:uuid:bd6a29ac-e52b-5cdd-ab13-7914d9037d85

## Companion Book Intro

- Path: `/Users/tobylee/workspace/ai/book-writer-3/.claude/worktrees/meta-skill-for-developer/코드-밖에서-결정된다-v1.0.0.md` (project root, alongside the EPUB)
- Sources used: `book_manifest.json` (meta), `02_plan.md` (audience/arc/chapter intent), `04_manuscript.md` (TOC verification, char count)

## Build History

1. **v1 build (23:34:39Z)** — pandoc exit 0, epubcheck FAILED with RSC-005 (empty `dc:identifier`, `dc:date`).
2. **v2 build (23:35:00Z)** — added `pub_date: "2026-05-03"`, `identifier: "urn:uuid:meta-skills-of-developers-v1.0.0"` to manifest. epubcheck passed but emitted OPF-085 warning ("not a valid UUID").
3. **v3 build (23:37:31Z, FINAL)** — replaced identifier with deterministic UUID5 `urn:uuid:bd6a29ac-e52b-5cdd-ab13-7914d9037d85` (uuid5 of `https://toby-ai.example/books/meta-skills-of-developers-v1.0.0`). epubcheck PASSED with zero errors and zero warnings.

Previous EPUBs preserved under `_prev/`:
- `코드-밖에서-결정된다-v1.0.0-20260503233458.epub` (v1)
- `코드-밖에서-결정된다-v1.0.0-20260503233729.epub` (v2)

## Structure Verification

- `04_manuscript.md`: 2,528 lines, 102,745 Hangul chars (~205K total chars).
- 1단계(`# `) headings: 16 (book title page + 15 manifest structure entries).
- pandoc `--split-level=1` produced 16 internal xhtml files: `ch001` is the title page (책 제목 + 부제 + 차례), `ch002`–`ch016` are the 15 manifest entries from 머리말 to 찾아보기 — matches `book_manifest.json` exactly.
- Cover (`cover.png`, 2,089,940 bytes) embedded as `EPUB/media/file0.png`; cover.xhtml present.
- Korean rendering verified by extracting `ch002`/`ch003`/`ch011`/`ch013`/`ch016` — h1 titles and first paragraphs render cleanly with no mojibake.

## Final Outputs

- EPUB: `/Users/tobylee/workspace/ai/book-writer-3/.claude/worktrees/meta-skill-for-developer/코드-밖에서-결정된다-v1.0.0.epub` (2,276,593 bytes)
- Book intro markdown: `/Users/tobylee/workspace/ai/book-writer-3/.claude/worktrees/meta-skill-for-developer/코드-밖에서-결정된다-v1.0.0.md` (8,428 bytes)
