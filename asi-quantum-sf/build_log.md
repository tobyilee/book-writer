# Build Log — 결어긋남 v1.0.0

- **Date:** 2026-04-20T13:40:00Z
- **Output:** `/Users/tobylee/workspace/ai/book-writer/.claude/worktrees/sf/결어긋남-v1.0.0.epub`
- **Size:** 2,307,799 bytes (2.20 MB)
- **Pandoc exit:** 0
- **epubcheck:** passed with 1 warning (identifier UUID format)

## Metadata

- title: 결어긋남
- subtitle: Decoherence
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-04-20
- identifier: urn:uuid:kairos-decoherence-v1-20260420
- chapter_count: 15

## Build command

```bash
pandoc asi-quantum-sf/04_manuscript.md \
  --from markdown+smart \
  --to epub3 \
  --metadata-file=asi-quantum-sf/.meta.yaml \
  --epub-cover-image=asi-quantum-sf/cover.png \
  --toc --toc-depth=2 \
  --split-level=1 \
  --mathml \
  --output 결어긋남-v1.0.0.epub
```

## Structure (25 files in archive)

- mimetype, META-INF/container.xml, Apple iBooks display-options
- EPUB/content.opf (4.7 KB), EPUB/toc.ncx (34 KB), EPUB/nav.xhtml (21 KB)
- EPUB/text/cover.xhtml, title_page.xhtml
- EPUB/media/file0.png (cover, 2.05 MB, 1600×2560)
- EPUB/styles/stylesheet1.css (3.8 KB)
- 15 body XHTML files (`ch001.xhtml` ~ `ch015.xhtml`):
  프롤로그 + 1~13장 + 에필로그

## Rendering verification

에필로그 (`ch015.xhtml`) 스팟 체크:

- `<math>` 태그: **12쌍** (MathML 변환 성공 — `--mathml` 옵션 적용)
- `<pre>` 블록: **3개** (ASCII 회로 다이어그램 고정폭 보존)
- `<code>` 인라인: **19개**
- 그리스 문자: Φ×29, θ×10, α×4, β×7, γ×5 (UTF-8 보존)

코드 블록(5·9·10·11장 콘솔 출력)은 분리된 각 XHTML 파일에서 `<pre><code>` 구조로 pandoc이 변환. 섹션 구분자 `* * *`·`---`는 모두 `<hr>`로 일관 변환.

## TOC entries (nav.xhtml 기반)

pandoc `--toc-depth=2`로 다음 레벨까지 포함:

**Front matter**
- 결어긋남 / Decoherence / 헌정 / 서문 — 독자에게 / 목차 / 등장인물·주요 개념 / 주요 개념 약어

**Body (15장)**
- 프롤로그 — 어떤 측정은 되돌릴 수 없다
- 1장 — 평가자의 오후
- 2장 — 중첩의 월요일
- 3장 — 얽힘은 통신이 아니다 (6개 하위 섹션)
- 4장 — 훈련 분포의 바깥 (5개 하위 섹션)
- 5장 — 첫 대화, 기호로만 (6개 하위 섹션)
- 6장 — 결맞음이 유지되는 동안 (11개 하위 섹션)
- 7장 — 관측되지 않은 시간의 길이 (15개 하위 섹션)
- 8장 — Blindsight의 오후
- 9장 — 카이로스의 선택지
- 10장 — 제주로 가는 밤
- 11장 — 측정
- 12장 — 남은 자들 (9개 하위 섹션)
- 13장 — 파동함수가 돌아왔을 때 (14개 하위 섹션)
- 에필로그 — 부록: 카이로스의 마지막 회로 (7개 하위 섹션)

**Back matter**
- 작가의 말 / 참고문헌 / 저자 소개

**Landmarks**
- Title Page / Cover / Table of Contents

## Page estimate

본문·프론트·백 매터 합 283,757자 기준:
- ~157쪽 @ 1,800 cpp
- ~189쪽 @ 1,500 cpp

## Warnings

1. **epubcheck OPF-085**: `urn:uuid:kairos-decoherence-v1-20260420`은 엄격한 UUID 포맷이 아님. EPUB 규격상 경고일 뿐 readers는 정상 식별. 향후 필요시 `urn:uuid:` 뒤를 정규 UUIDv4로 교체 권장.

## Notes

- 매니페스트 파일명이 `05_book_manifest.json`이라 스킬 스크립트가 찾는 `book_manifest.json`과 이름이 달랐음. 빌드 시간 동안만 심볼릭 링크를 생성해 브릿지.
- 스킬 번들 스크립트의 기본 pandoc 호출에 `--mathml`이 빠져 있어, editor_notes의 수식 렌더링 요구를 충족하기 위해 동등한 커맨드로 직접 호출. 결과는 스크립트가 작성하는 log와 동일 포맷으로 수동 작성.
