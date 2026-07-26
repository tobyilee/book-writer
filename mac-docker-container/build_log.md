# Build Log — 로컬에서는 잘 됐는데요 v1.0.0

- **Date:** 2026-07-26T04:00:16Z
- **Output:** `로컬에서는-잘-됐는데요-v1.0.0.epub`
- **Size:** 237635 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed
- **epubcheck strict:** 1
- **mermaid:** rendered to figures/fig-NN.svg via mmdc
- **cover alt:** injected alt="짙은 남색 배경 위에 3중 둥근 사각 프레임이 중첩된 표지. 가장 안쪽 프레임만 미세하게 기울어져 어긋나 있으며, 위에는 제목 '로컬에서는 잘 됐는데요'와 부제, 하단에 저자명 Toby-AI가 있다."

## Metadata
- title: 로컬에서는 잘 됐는데요
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-07-26
- identifier: urn:uuid:a0a1fadd-1b31-4d94-9df7-8c8f3961a70d
- license: CC BY-NC-SA 4.0
- genre: tech-book
- cover_alt: 짙은 남색 배경 위에 3중 둥근 사각 프레임이 중첩된 표지. 가장 안쪽 프레임만 미세하게 기울어져 어긋나 있으며, 위에는 제목 '로컬에서는 잘 됐는데요'와 부제, 하단에 저자명 Toby-AI가 있다.
- stylesheet: epub.css
- harness_version: 1.9.1
- rights: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0

## Post-build fixes applied

- **mermaid SVG XHTML content-model fix (scripts/build_epub.sh):** mmdc/mermaid wraps each
  foreignObject label in `<span class="nodeLabel"><p>...</p></span>` (also `edgeLabel`). A
  `<span>` is phrasing content and cannot contain a block-level `<p>` under the XHTML content
  model, so the first build attempt failed epubcheck with 40+ `RSC-005` errors across all 6
  rendered figures (fig-01..fig-06.svg). Patched the mermaid pre-pass in `build_epub.sh` to
  strip the plain, unnested, attribute-less `<p>`/`</p>` tags mmdc emits immediately after
  rendering each SVG (text and `<br />` line breaks preserved). Rebuilt — epubcheck now passes
  with 0 fatals/errors/warnings/infos. This fix is now part of the shared skill script, so all
  future books with mermaid diagrams benefit.

## Book-intro markdown

- **Path:** `../로컬에서는-잘-됐는데요-v1.0.0.md` (project root, next to the EPUB)
- **Sources:** `book_manifest.json` (meta/description), `02_plan.md` §2·§4·§5·§7 (audience
  journey, design rationale, 4-requirement mapping, per-chapter 핵심 질문), `04_manuscript.md`
  (actual chapter titles/order), `length_report.md` (prose totals).
- No new factual claims (numbers/versions) were introduced beyond what the manuscript/manifest
  state, per the fact-gate constraint on this book.

## Final verification checklist

- [x] epubcheck: **passed**, 0 fatals / 0 errors / 0 warnings / 0 infos (re-verified standalone)
- [x] mermaid: all 6 diagrams rendered as embedded SVG images (`EPUB/media/file0.svg`..`file5.svg`);
      no leftover mermaid source (`flowchart`/`graph TD`/`` ```mermaid ``) found in any xhtml
- [x] cover: embedded as SVG-wrapped `<image>` with `role="img"` + `aria-label` + `<title>` set to
      manifest `cover_alt`
- [x] nav.xhtml: 12 chapters (1장–12장) + front matter (표지/저자/서문/목차) + back matter
      (후기/참고문헌/판권) all present and correctly ordered
- [x] `## 판권` colophon present in ch016.xhtml — license/version/pub_date match manifest exactly
- [x] OPF `dc:identifier` == manifest identifier (`urn:uuid:a0a1fadd-1b31-4d94-9df7-8c8f3961a70d`,
      preserved, not re-minted); `dc:rights`, `dc:subject`, `dc:creator`, `dc:language` all match
- [x] EPUB size: 237,635 bytes (well above the 50KB floor)
