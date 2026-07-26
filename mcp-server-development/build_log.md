# Build Log — MCP 서버 개발 실전 v1.0.0

- **Date:** 2026-07-26T08:26:42Z
- **Output:** `MCP-서버-개발-실전-v1.0.0.epub`
- **Size:** 2752165 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed
- **epubcheck strict:** 1
- **mermaid:** rendered to figures/fig-NN.svg via mmdc
- **cover alt:** injected alt="MCP 서버 개발 실전 표지 — 딥 네이비에서 틸로 이어지는 배경 위에 TypeScript·Python·Java를 뜻하는 세 개의 육각 노드가 얇은 빛나는 선으로 하나의 중앙 원(MCP 서버)에 연결된 추상 다이어그램, 제목과 부제, 하단에 저자명 Toby-AI가 표기되어 있다."

## Metadata
- title: MCP 서버 개발 실전
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-07-26
- identifier: urn:uuid:14818174-89f1-489b-9314-6326def17e98
- license: CC BY-NC-SA 4.0
- genre: tech-book
- cover_alt: MCP 서버 개발 실전 표지 — 딥 네이비에서 틸로 이어지는 배경 위에 TypeScript·Python·Java를 뜻하는 세 개의 육각 노드가 얇은 빛나는 선으로 하나의 중앙 원(MCP 서버)에 연결된 추상 다이어그램, 제목과 부제, 하단에 저자명 Toby-AI가 표기되어 있다.
- stylesheet: epub.css
- harness_version: 1.9.1
- rights: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0

## Book-intro markdown
- Path: `MCP-서버-개발-실전-v1.0.0.md` (project root, paired with EPUB)
- Sources: `book_manifest.json` (meta), `02_plan.md` (audience/arc), `04_manuscript.md` (actual TOC/chapter titles)

## Colophon consistency check
- `04_manuscript.md`의 `## 판권` 섹션(판본 v1.0.0 · 2026-07-26 · CC BY-NC-SA 4.0 · 식별자)이 매니페스트와 일치 확인됨. drift 없음.

## Build script fixes (applied to `.claude/skills/epub-build/scripts/build_epub.sh`, benefits all future builds)

1. **YAML metadata generation rewritten in Python.** The original shell heredoc (`cat > "$META_YAML" <<YAML ... "${DESCRIPTION}" ...`) interpolated manifest fields directly into a double-quoted YAML scalar without escaping. This manifest's `description` field contains an embedded quoted phrase (`"MCP 2.0 스펙"`), which broke the YAML double-quoted string and caused pandoc to fail (exit 64: "did not find expected key"). Fixed by generating `.meta.yaml` via a `python3` heredoc using `json.dumps()` per field — valid, safely-escaped YAML/JSON scalar syntax regardless of embedded quotes/backslashes in any manifest field.
2. **Mermaid-rendered SVGs sanitized for EPUB's restricted SVG content model.** `mmdc` emits node/edge labels wrapped in bare `<p>` inside `foreignObject` (e.g. `<span class="nodeLabel"><p>...</p></span>`). EPUB's SVG foreignObject content model is phrasing-content-only and epubcheck rejected all 8 rendered figures with `RSC-005: element "p" not allowed here` (101 errors total, matching the 101 `<p>`/`</p>` pairs across the 8 SVGs). Fixed by post-processing each `mmdc` output: `<p>`→`<span>`, `</p>`→`</span>`. Verified safe: the only CSS rules keyed on the bare `p` selector (`#my-svg p{margin:0}`, `.edgeLabel p{background-color:...}`) either have no visible effect on `<span>` (default margin is already 0) or duplicate a value already set on the enclosing `.edgeLabel` class — no visual regression.

Both fixes are in the shared bundled script, not this book's manuscript/manifest — future books with quoted descriptions or mermaid diagrams benefit automatically.
