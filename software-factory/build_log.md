# Build Log — 소프트웨어 팩토리 v1.0.0

- **Date:** 2026-09-28T04:14:57Z
- **Output:** `소프트웨어-팩토리-v1.0.0.epub`
- **Size:** 2635084 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed
- **epubcheck strict:** 1
- **mermaid:** rendered to figures/fig-NN.svg via mmdc
- **images:** 17 local reference(s), all present
- **cover alt:** injected alt="짙은 남색 바탕에 '소프트웨어 팩토리' 제목이 크게 적혀 있고, 아래에는 보조·협업·위임·승인·온콜 순으로 높아지는 공장 건물 다섯 동이 서 있다. 오른쪽으로 갈수록 불 켜진 창이 줄어들지만 마지막 건물에도 창 하나는 켜져 있다."

## Metadata
- title: 소프트웨어 팩토리
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-09-28
- identifier: urn:uuid:9cec6102-fd42-4f02-b97e-01816fc1395a
- license: CC BY-NC-SA 4.0
- genre: tech-book
- cover_alt: 짙은 남색 바탕에 '소프트웨어 팩토리' 제목이 크게 적혀 있고, 아래에는 보조·협업·위임·승인·온콜 순으로 높아지는 공장 건물 다섯 동이 서 있다. 오른쪽으로 갈수록 불 켜진 창이 줄어들지만 마지막 건물에도 창 하나는 켜져 있다.
- stylesheet: epub.css
- harness_version: 2.0.0
- rights: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0

## Build command

```bash
cd /Users/tobylee/workspace/ai/book-writer
rm -f 소프트웨어-팩토리-v1.0.0.epub   # unreleased v1.0.0, overwritten in place per coordinator (no _prev backup)
PATH="<scratchpad>/bin:$PATH" bash .claude/skills/epub-build/scripts/build_epub.sh software-factory
# <scratchpad>/bin/mmdc = wrapper: exec npx -y @mermaid-js/mermaid-cli@latest "$@"
# puppeteer browser auto-detected: /Applications/Google Chrome.app
```

- exit 0. `build_epub.sh` unchanged. `04_manuscript.md` used as-is (no re-assembly).
- **Rebuild 2 (2026-09-28T04:14:57Z)** after editor layout fixes: colophon hard breaks; figs 1/4/5/7/10/11/12 switched from `flowchart LR` to `flowchart TB`. Replaces the first build (04:05:45Z, 2,634,889 bytes). Same version and identifier.

## epub-builder checks

| Check | Result |
|---|---|
| Output exists, size ≥ 50KB | PASS — 2,635,084 bytes |
| epubcheck (strict) | PASS — EPUB 3.4 rules, 0 fatals / 0 errors / 0 warnings / 0 infos (`.epubcheck.log`) |
| mermaid pre-pass | PASS — 17 ```` ```mermaid ```` blocks → `figures/fig-01.svg`…`fig-17.svg`, 17 `<img>` in chapter XHTML, 0 mermaid code blocks left, no `<foreignObject>` |
| Image pre-flight | PASS — 17 local references, 0 MISSING |
| Cover alt | PASS — `cover.xhtml` `<svg role="img" aria-label="…">` + `<title>` carry manifest `cover_alt` |
| OPF metadata | PASS — dc:title 소프트웨어 팩토리 · dc:creator Toby-AI · dc:language ko · dc:date 2026-09-28 · dc:subject tech-book · dc:identifier urn:uuid:9cec6102-fd42-4f02-b97e-01816fc1395a (unchanged) |
| OPF rights | PASS — `© 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0` |
| Colophon (`## 판권`) vs manifest | PASS — license string `CC BY-NC-SA 4.0` (manifest empty → build default), version v1.0.0, pub_date 2026-09-28, identifier all match |
| Colophon line breaks | PASS — `ch001.xhtml`: title / 판본 / 발행일 / 저자 / 식별자 lines separated by `<br />` |

## Figure aspect ratios after LR → TB (w/h, from SVG viewBox)

| Figure | Before (LR) | After (TB) |
|---|---|---|
| fig-01 (1장 그림 1) | 6.0 | 0.73 (523×716) |
| fig-04 (4장 그림 1) | 7.4 | 0.37 (312×853) |
| fig-05 (5장 그림 1) | 4.7 | 0.57 (376×660) |
| fig-07 (7장 그림 1) | 9.1 | 0.29 (281×969) |
| fig-10 (9장 그림 1) | 5.5 | 0.74 (360×489) |
| fig-11 (10장 그림 1) | 10.7 | 0.35 (168×473) |
| fig-12 (11장 그림 1) | 12.9 | 0.37 (168×458) |

All seven were checked visually (headless Chrome): the flow is now vertical and the labels are legible.

## Remaining advisory (non-blocking, cosmetic — owner: editor)

- Long ASCII tokens still wrap mid-word in some node labels, e.g. `factory:approve|d` (fig-08, fig-09) and `claude-code-acti|on` (fig-03, fig-08).

## Book intro

- `/Users/tobylee/workspace/ai/book-writer/소프트웨어-팩토리-v1.0.0.md` (same stem as the EPUB). Unchanged by the rebuild: its facts (version, date, identifier, TOC, license, epubcheck pass, 17 figures) all still hold.
