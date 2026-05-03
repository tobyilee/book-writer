# Build Log — JVM 출신을 위한 Rust v1.0.0

- **Date:** 2026-05-03T12:01:42Z
- **Output:** `JVM-출신을-위한-Rust-v1.0.0.epub`
- **Size:** 1026939 bytes
- **Pandoc exit:** 0
- **epubcheck:** passed

## Metadata
- title: JVM 출신을 위한 Rust
- author: Toby-AI
- language: ko
- version: 1.0.0
- pub_date: 2026-05-03
- identifier: urn:uuid:009bcde0-619c-432e-bb6d-47373c21edf6

## Companion artifacts

- 책 소개 markdown: `JVM-출신을-위한-Rust-v1.0.0.md` (project root, EPUB과 동일 폴더)

## Validation

- pandoc 3.9.0.2, EPUB 3 출력
- 파일 크기: 1,026,939 bytes (≥ 50KB OK)
- epubcheck: 0 fatal / 0 error / 0 warning (clean)
- 내부 구조: mimetype, META-INF/container.xml, EPUB/content.opf, EPUB/toc.ncx, EPUB/nav.xhtml, EPUB/text/cover.xhtml, ch001~chNNN.xhtml, EPUB/media/file0.png, EPUB/styles/stylesheet1.css

## Manuscript hardening (1차 빌드 → 재빌드)

코드 펜스 밖에서 백틱 없이 노출된 generic 타입 표기가 pandoc에 의해 raw HTML 태그로 흘러 XHTML 파서가 4건의 FATAL을 냈다. 다음 5곳을 백틱으로 감싸 수정:

- `## Vec<T>로 본 move의 의미` → `## \`Vec<T>\`로 본 move의 의미`
- `## Box<T> 살짝 — heap에 의도적으로 올리고 싶을 때` → `## \`Box<T>\` 살짝 …`
- 본문 *"같은 List<Greeter>가 아니므로"* → *"같은 \`List<Greeter>\`가 아니므로"*
- `## Arc<Mutex<T>> — 공유 가변 상태의 표준 표현형` → `## \`Arc<Mutex<T>>\` …`
- 부록 표 셀 `*State<T>*` → `\`State<T>\``

매니페스트에 빠져 있던 `pub_date`와 `identifier`(urn:uuid 형식) 키를 추가해 dc:date·dc:identifier 빈 값 ERROR도 해소.

이전 빌드 산출물은 `_prev/`에 보존됨.
