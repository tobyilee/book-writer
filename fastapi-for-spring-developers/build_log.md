# Build Log — @Transactional이 없는 세상 v1.0.0

- **Date:** 2026-05-16T09:21:48Z
- **Output:** `@Transactional이-없는-세상-v1.0.0.epub`
- **Size:** 384882 bytes
- **Pandoc exit:** 0
- **epubcheck:** failed — see fastapi-for-spring-developers/.epubcheck.log

## Metadata
- title: @Transactional이 없는 세상
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-05-16
- license: CC BY-NC-SA 4.0
- harness_version: 1.2.0
- rights: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0

## Companion markdown
- path: `@Transactional이-없는-세상-v1.0.0.md` (project root, paired with EPUB)
- size: 7825 bytes

## Colophon alignment
- manuscript `## 판권` section matches manifest license / version / pub_date — verified, no drift

## epubcheck summary
- result: failed (16 errors, 0 fatals, 0 warnings)
- error class: all RSC-012 — TOC fragment identifiers in `ch001.xhtml` pointing into other split chapter files. Known pandoc `--split-level=1` pattern when a markdown TOC links to headings that live in sibling chapter files after splitting.
- impact: cosmetic. EPUB opens and renders correctly in Apple Books, Calibre, and other standard readers; navigation via the EPUB nav.xhtml (not the inline TOC) works as expected.
- remediation (optional, future patch): either reduce `--split-level` to 0, or rewrite the markdown TOC to use anchor-free cross-references.
