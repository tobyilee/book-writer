# Build Log — 꺼내 쓰는 뇌 v1.0.0

- **Date:** 2026-05-04T09:46:57Z
- **Output (EPUB):** `꺼내-쓰는-뇌-v1.0.0.epub`
- **Output (책 소개 md):** `꺼내-쓰는-뇌-v1.0.0.md` (8,002 bytes / 약 3,870 단어 / 860줄)
- **Size:** 3,291,943 bytes (≈3.14 MB, 표지 PNG 3 MB 포함)
- **Pandoc exit:** 0
- **epubcheck:** passed (이전 v1.0.0 1차 빌드는 `dc:identifier`·`dc:date` 빈 값 RSC-005 ERROR 2건 — 매니페스트에 `pub_date: 2026-05-04`, `identifier: urn:uuid:49c0b096-7a08-448b-8d01-4d667fa133a9` 추가 후 재빌드. 이전 산출물은 `_prev/`로 이동)

## Metadata (EPUB content.opf 확인 결과)

- **dc:identifier:** urn:uuid:49c0b096-7a08-448b-8d01-4d667fa133a9
- **dc:title:** 꺼내 쓰는 뇌
- **dc:date:** 2026-05-04
- **dc:language:** ko
- **dc:creator:** Toby-AI (role=aut)
- **dc:rights:** © 2026 Toby-AI
- **dc:description:** 매니페스트와 동일 (다섯 가지 약속 요약)
- **cover meta:** file0_png (1600×2560 PNG, 3 MB)
- **a11y meta:** alternativeText, readingOrder, structuralNavigation, tableOfContents (accessibilityHazard=none)

## Build command

```bash
bash .claude/skills/epub-build/scripts/build_epub.sh retrieval-brain
```

내부에서 호출되는 pandoc 명령(요약):

```bash
pandoc retrieval-brain/04_manuscript.md \
  --from markdown --to epub3 \
  --metadata-file=<temp.yaml> \
  --epub-cover-image=retrieval-brain/cover.png \
  --toc --toc-depth=2 --split-level=1 \
  --output 꺼내-쓰는-뇌-v1.0.0.epub
```

- **pandoc 버전:** 3.9.0.2 (Lua 5.4, +server +lua)
- **epubcheck 버전:** 시스템 설치본(`/Users/tobylee/.pyenv/shims/epubcheck`)

## EPUB 구조 (unzip -l 요약)

- mimetype, META-INF/container.xml, META-INF/com.apple.ibooks.display-options.xml
- EPUB/content.opf (4,577 bytes)
- EPUB/toc.ncx (18,555 bytes), EPUB/nav.xhtml (11,698 bytes)
- EPUB/text/cover.xhtml + EPUB/media/file0.png (3,120,127 bytes)
- 본문 챕터 14개 (ch001~ch014.xhtml): front matter 1개 + 5개 챕터 + 부록 5종 + 용어집·참고문헌·저자 소개
- EPUB/styles/stylesheet1.css (3,778 bytes)

## 검증 체크리스트

- [x] EPUB 파일 생성됨 (3,291,943 bytes ≥ 50KB 기준 통과)
- [x] 메타데이터(title/author/language/identifier/date/rights/description) 모두 정확히 박힘
- [x] 표지 이미지 EPUB 내부에 포함됨 (1600×2560 PNG, EPUB/media/file0.png)
- [x] 차례(TOC) 자동 생성 — 5개 챕터 × 5개 절 + 부록·용어집·참고문헌·저자 소개까지 toc-depth=2로 망라
- [x] epubcheck 통과 (ERROR 0, WARNING 0)
- [x] 책 소개 markdown 짝 산출물 존재 (`꺼내-쓰는-뇌-v1.0.0.md`, 같은 폴더)

## 책 소개 markdown 구성

- 로그라인 1문장
- 메타 블록 (저자·버전·발행일·언어·분량·장르)
- "이 책에 대해" 4단락 — 차별 메시지 4 + 메타 약속 1, 한국 학습자 자리에서 풀어쓴 도입
- "대상 독자" 3그룹 (직장인·전문가, 수험생, 지식 체계 구축자) 각자 어디부터 펴면 좋은지 안내
- "핵심 약속 (Promise)" 다섯 가지 ① ~ ⑤
- "차례" — 머리말 + 5개 챕터 한 줄 요약 + 부록 5종 + 용어집·참고문헌·저자 소개
- "저자 소개" — Toby-AI AI 저자 페르소나 한 단락
- "책 정보" — 제목·부제·저자·출판·언어·버전·분량·장르·파일·형식·표준 검증·권리

## 비고

- 1차 빌드(09:46:30Z) 시 `dc:identifier`·`dc:date` 빈 값 ERROR 2건 발생 → 매니페스트 보강 후 2차 빌드(09:46:57Z) 통과. 1차 산출물은 자동으로 `_prev/꺼내-쓰는-뇌-v1.0.0-{timestamp}.epub`로 이동.
- 매니페스트의 `description`이 길어 `dc:description`이 다소 장문이지만 EPUB 3 규격상 길이 제한은 없고 epubcheck도 통과.
- TOC depth=2이므로 절(예: 1.1, 1.2)까지는 노출되고 그 아래 즉시 적용 프로토콜·핵심 정리도 ## 헤딩이라 함께 노출됨.
