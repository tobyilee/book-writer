---
name: epub-build
description: Build a standards-compliant EPUB 3 file from a manuscript markdown, cover image, and book_manifest.json using the bundled pandoc-based script. Output is 책-제목-v{version}.epub with Toby-AI as author. Use when converting the final book manuscript to EPUB, rebuilding after edits, or testing EPUB output.
---

# EPUB Build

통합 원고·표지·매니페스트를 입력받아 EPUB 3 파일을 생성한다. 결정적 빌드를 위해 `scripts/build_epub.sh` 스크립트에 위임한다.

## 절차

1. **입력 검증** — 세 파일이 모두 존재하는지
   - `{slug}/04_manuscript.md`
   - `{slug}/cover.png`
   - `{slug}/book_manifest.json`
2. **매니페스트 필드 점검**
   - `title` 비어있지 않음
   - `author == "Toby-AI"` — 다르면 경고 후 교정
   - `language` 존재 (`ko`)
   - `version` 존재 (예: `1.0.0`)
3. **스크립트 실행** — `scripts/build_epub.sh {slug}`
4. **결과 검증**
   - 파일 존재, 크기 ≥ 50KB
   - `epubcheck` 설치되어 있으면 실행, 로그 저장
5. **기록** — `{slug}/build_log.md`에 명령, 출력, 크기, 검증 결과

## 스크립트 개요 (`scripts/build_epub.sh`)

pandoc을 이용해 원고와 메타데이터를 EPUB으로 변환한다. 요점:

```bash
pandoc {manuscript} \
  --from markdown \
  --to epub3 \
  --metadata-file={manifest_yaml} \
  --epub-cover-image={cover} \
  --toc --toc-depth=2 \
  --output {output_path}
```

매니페스트(JSON)를 YAML로 변환한 뒤 pandoc에 전달한다. 스크립트 전문은 `scripts/build_epub.sh` 참조.

## 파일명 규칙

- `{책-제목}-v{version}.epub`
- 제목의 공백은 `-`로 치환
- 특수문자(`/`, `?`, `:`, `*`)는 제거
- 예: `효과적인-SQL-쿼리-튜닝-v1.0.0.epub`

## 버전 관리

- 초기 빌드: `v1.0.0`
- 오탈자 수정: patch 증가 → `v1.0.1`
- 챕터 개정: minor 증가 → `v1.1.0`
- 구조 재편: major 증가 → `v2.0.0`
- 기존 파일을 덮어쓰지 말고 새 파일로 공존

## 검증 체크

- [ ] EPUB 파일 생성됨
- [ ] 파일 크기 ≥ 50KB
- [ ] `unzip -l`로 내부 구조 확인 가능
- [ ] 메타 조회: `pandoc -f epub -t plain --template=metadata.tpl` 등
- [ ] `epubcheck` 통과 (설치되어 있는 경우)

## 실패 대응

| 상황 | 조치 |
|------|------|
| pandoc 미설치 | `brew install pandoc` 안내, 또는 Calibre `ebook-convert` 폴백 검토 |
| cover.png 누락 | cover-designer에 폴백 생성 요청, 메타만으로 빌드 후 경고 |
| 원고 내 비정상 유니코드·XML 문자 | 스크립트가 `iconv`로 정규화 시도, 실패 시 해당 구절 치환 |
| `epubcheck` 실패 | 오류 로그 보존, 빌드는 완료 처리하되 사용자에 리포트 |
| 50KB 미만 산출물 | 챕터 변환 실패 의심 → 변환 단계별 디버깅 후 재빌드 |

## 재빌드 시

- 이전 결과를 `_prev/`로 이동
- 사용자가 매니페스트 일부만 수정한 경우 → 원고 재작업 없이 매니페스트만 갱신하고 재빌드 가능
