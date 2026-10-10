# Build Log — 에이전트를 믿어도 될까 v1.0.0

- **Date:** 2026-10-10T06:09:30Z
- **Output:** `에이전트를-믿어도-될까-v1.0.0.epub`
- **Size:** 1363048 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed
- **epubcheck strict:** 1
- **mermaid:** rendered to figures/fig-NN.svg via mmdc
- **images:** 8 local reference(s), all present
- **cover alt:** injected alt="짙은 남색 배경 위에 책 제목 '에이전트를 믿어도 될까'와 부제, 그 아래 지켜보기·자가 검증·클라우드·자동 머지 네 단계를 따라 오른쪽 위로 오르는 앰버색 신뢰 곡선과 단계마다 늘어나는 흰 점들"

## Metadata
- title: 에이전트를 믿어도 될까
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-10-10
- identifier: urn:uuid:4a461c29-ec12-47f9-8458-fb5c20fcb1e1
- license: CC BY-NC-SA 4.0
- genre: tech-book
- cover_alt: 짙은 남색 배경 위에 책 제목 '에이전트를 믿어도 될까'와 부제, 그 아래 지켜보기·자가 검증·클라우드·자동 머지 네 단계를 따라 오른쪽 위로 오르는 앰버색 신뢰 곡선과 단계마다 늘어나는 흰 점들
- stylesheet: epub.css
- harness_version: 2.0.0
- rights: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0

## 빌드 명령·검증 (epub-builder)
- command: `PATH=$HOME/.nvm/versions/node/v24.21.0/bin:$PATH .claude/skills/epub-build/scripts/build_epub.sh agentic-dev-trust-curve` (프로젝트 루트에서)
- mermaid: 8/8 렌더 (figures/fig-01..08.svg, puppeteer 브라우저 자동 탐지: /Applications/Google Chrome.app), `.mermaid_err` 비어 있음
- EPUB 내부: SVG 8 + cover PNG 1, 챕터 xhtml 13, cover alt = SVG role=img + aria-label + <title>
- OPF 대조: identifier·date·creator·rights(`Licensed under CC BY-NC-SA 4.0`)가 매니페스트·원고 `## 판권`과 일치 — drift 없음
- 책 소개: `에이전트를-믿어도-될까-v1.0.0.md` (프로젝트 루트, EPUB과 같은 stem)
