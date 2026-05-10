# Build Log — 잊지 않는 기술 — 기억의 궁전부터 AI 카드까지 v1.0.0

- **Date:** 2026-05-10T06:04:38Z
- **Output:** `잊지-않는-기술-—-기억의-궁전부터-AI-카드까지-v1.0.0.epub`
- **Size:** 356878 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed

## Metadata
- title: 잊지 않는 기술 — 기억의 궁전부터 AI 카드까지
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-05-10
- license: CC BY-NC-SA 4.0
- harness_version: 1.2.0
- rights: © 2026 Toby-AI — Licensed under CC BY-NC-SA 4.0

## Paired Outputs (project root)

- EPUB (canonical, slugified full title): `잊지-않는-기술-—-기억의-궁전부터-AI-카드까지-v1.0.0.epub`
- 책 소개 markdown (canonical): `잊지-않는-기술-—-기억의-궁전부터-AI-카드까지-v1.0.0.md`
- EPUB (user-requested short stem): `잊지 않는 기술-v1.0.0.epub`
- 책 소개 markdown (user-requested short stem): `잊지 않는 기술-v1.0.0.md`

## Verification

- pandoc exit: 0
- file size: 356,878 bytes (≥ 50KB threshold)
- epubcheck: passed
- OPF metadata verified: title / creator (Toby-AI) / language (ko) / identifier / rights all match manifest
- TOC verified: 서문 + 1~11장 12개 섹션, depth=2 헤딩 인덱싱
- 콜로폰 정합성: 04_manuscript.md `## 판권` ↔ manifest license/version/pub_date 일치 (CC BY-NC-SA 4.0, v1.0.0, 2026-05-10)
- 매니페스트 보정: 빌드 전 `pub_date`, `identifier` 필드 추가 (기존 `date` 필드만 있어서 build_epub.sh가 빈 값으로 읽음)
