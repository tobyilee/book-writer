# Build Log — 리액트, 상태와 경계 v1.0.0

- **Date:** 2026-04-26T22:00:00Z
- **Output:** `리액트-상태와-경계-v1.0.0.epub` (project root)
- **Size:** 499232 bytes (~487 KB)
- **Pandoc exit:** 0
- **epubcheck:** passed (EPUB 3.3, 0 fatals / 0 errors / 0 warnings / 0 infos)

## Tooling

- pandoc 3.9.0.2 (Homebrew)
- epubcheck (Homebrew)

## Build commands

Initial run via the bundled `epub-build` skill:

```
bash .claude/skills/epub-build/scripts/build_epub.sh react-state-escape-hatches
```

The first build emitted empty `dc:identifier`, `dc:date`, and `dc:description`
elements (the manifest uses `publication_date`/`publisher`, while the script
reads `pub_date`/`identifier`/`description`), so epubcheck reported 3 errors
and 1 warning. The output was also named `리액트,-상태와-경계-v1.0.0.epub`
(comma preserved from the title), which differs from the spec-required
filename.

Rebuild with explicit metadata YAML (deterministic UUID via uuid5 of
`toby-ai/react-state-escape-hatches/v1.0.0`):

```
pandoc react-state-escape-hatches/04_manuscript.md \
  --from markdown \
  --to epub3 \
  --metadata-file=react-state-escape-hatches/.meta.yaml \
  --epub-cover-image=react-state-escape-hatches/cover.png \
  --toc --toc-depth=2 \
  --split-level=1 \
  --output "리액트-상태와-경계-v1.0.0.epub"
```

Metadata YAML supplied:

```
title: "리액트, 상태와 경계"
subtitle: "흔들리지 않는 멘탈 모델로 다시 쓰는 React"
author: "Toby-AI"
lang: "ko"
date: "2026-04-26"
identifier: urn:uuid:bce1be37-4e6f-56df-a2c2-93f1bbeaabb5
description: 리액트의 상태와 사이드 이펙트를 흔들리지 않는 멘탈 모델로 다시 쓰는 중급 개발자 안내서.
publisher: "self-published"
rights: "© 2026 Toby-AI"
```

## Metadata in EPUB

- title: 리액트, 상태와 경계
- subtitle: 흔들리지 않는 멘탈 모델로 다시 쓰는 React
- author (creator): Toby-AI
- language: ko
- version (book): 1.0.0
- date: 2026-04-26
- identifier: urn:uuid:bce1be37-4e6f-56df-a2c2-93f1bbeaabb5
- publisher: self-published

## Structure

- 34 entries inside the EPUB ZIP (mimetype, container, OPF, NCX, nav, cover, 24 chapter XHTMLs, stylesheet, cover image)
- Chapter splits at level 1 → one XHTML per top-level chapter (서문, 0–15장, 닫는 글, 부록 A–C)
- Cover: `react-state-escape-hatches/cover.png` (1600×2560 PNG, 174 KB) embedded as EPUB cover image
- Table of contents: 2 levels deep (`--toc-depth=2`)

## Validation

- File exists: yes
- Size ≥ 50 KB: yes (499232 bytes)
- `unzip -l` structure check: passed
- epubcheck (EPUB 3.3): **passed** — 0 errors / 0 warnings

## Warnings / issues

- Initial run produced an EPUB with the same name plus a comma
  (`리액트,-상태와-경계-v1.0.0.epub`) which has been removed in favor of
  the comma-stripped final filename.
- The skill script `scripts/build_epub.sh` reads metadata keys
  `pub_date` / `identifier` / `description`, but the manifest uses
  `publication_date` / `publisher` and lacks identifier/description. A
  follow-up improvement would be to align the script with the manifest
  schema (or extend the manifest) so the default build is epubcheck-clean
  without manual override.
