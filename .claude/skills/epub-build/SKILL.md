---
name: epub-build
description: Build a standards-compliant EPUB 3 file from a manuscript markdown, cover image, and book_manifest.json using the bundled pandoc-based script. Output is 책-제목-v{version}.epub with the manifest's author (defaults to Toby-AI), accompanied by a paired 책 소개 markdown ({책-제목}-v{version}.md) in the same folder. Use when converting the final book manuscript to EPUB, rebuilding after edits, or testing EPUB output.
---

# EPUB Build

통합 원고·표지·매니페스트를 입력받아 EPUB 3 파일을 생성하고, 같은 폴더에 책 소개 markdown을 함께 만든다. EPUB 변환은 결정적 빌드를 위해 `scripts/build_epub.sh` 스크립트에 위임하고, 책 소개 markdown은 `epub-builder` 에이전트가 매니페스트·계획·통합 원고를 읽어 직접 작성한다.

## 절차

1. **입력 검증** — 세 파일이 모두 존재하는지
   - `{slug}/04_manuscript.md`
   - `{slug}/cover.png`
   - `{slug}/book_manifest.json`
2. **매니페스트 필드 점검**
   - `title` 비어있지 않음
   - `author` 필드 존재 (기본값 `Toby-AI`, 사용자 지정 시 매니페스트 값을 그대로 사용)
   - `language` 존재 (`ko`)
   - `version` 존재 (예: `1.0.0`)
   - `identifier` (옵션) — 비어 있거나 플레이스홀더 `urn:uuid:...`이면 스크립트가 `urn:uuid:{uuid4}` 한 번 발급 후 매니페스트에 기록한다. **신간에 1회 발급되고 이후 재빌드에서 그대로 보존(불변)** — version/date만 바뀐다. `_prev`에 다른 식별자가 있으면 경고
   - `cover_alt` (옵션) — 표지 대체 텍스트. 비어 있으면 기본값 `{title} 표지`. 스크립트가 표지 xhtml에 실제 alt(또는 SVG 표지의 `role="img"`+`aria-label`+`<title>`)로 주입해 a11y 대체 텍스트 주장을 뒷받침한다
   - `license` (옵션) — 비어 있으면 하네스 기본값 `CC BY-NC-SA 4.0` 적용. 다른 라이선스를 쓰려면 명시 (`"CC BY 4.0"`, `"CC0"`, `"All rights reserved"` 등)
   - `harness_version` (옵션) — 비어 있으면 루트 `VERSION` 파일에서 자동 주입
   - `rights` (옵션) — 비어 있으면 `© {year} {author} — Licensed under {license}`로 자동 생성
3. **스크립트 실행** — `scripts/build_epub.sh {slug}`
4. **결과 검증**
   - 파일 존재, 크기 ≥ 50KB
   - `epubcheck` 실행 결과 점검 — **`epubcheck` 실패는 빌드 실패다(각주가 아님).** `EPUBCHECK_STRICT`(기본 켜짐 `1`)일 때 설치+실패면 빌드 로그를 쓴 뒤 종료 코드 `5`로 실패. `epubcheck`가 **미설치**면 EPUB은 검증되지 않은(UNVALIDATED) 상태로 산출되며 `brew install epubcheck` 안내를 stderr·빌드 로그에 남긴다 (`EPUBCHECK_STRICT=0`으로 실패를 경고로 강등 가능)
5. **책 소개 markdown 생성** — EPUB과 같은 폴더(프로젝트 루트)에 `{책-제목}-v{version}.md` 작성
   - 파일명 슬러그화 규칙은 EPUB과 동일 (공백→하이픈, 특수문자 제거)
   - 콘텐츠 템플릿·작성 원칙은 `epub-builder` 에이전트의 "책 소개 markdown" 섹션 참조
   - 소스: `book_manifest.json` (메타), `02_plan.md` (독자·아크), `04_manuscript.md` (실제 차례)
   - 같은 버전 파일이 이미 있으면 `_prev/`로 이동 후 신규 작성
6. **기록** — `{slug}/build_log.md`에 명령, 출력, 크기, 검증 결과, 책 소개 md 경로

## 스크립트 개요 (`scripts/build_epub.sh`)

pandoc을 이용해 원고와 메타데이터를 EPUB으로 변환한다. 요점:

```bash
pandoc {manuscript} \
  --from markdown \
  --to epub3 \
  --metadata-file={manifest_yaml} \
  --resource-path={slug} \
  --epub-cover-image={cover} \
  --css={styles/epub.css} \
  --toc --toc-depth=2 \
  --output {output_path}
```

매니페스트(JSON)를 YAML로 변환한 뒤 pandoc에 전달한다. `--resource-path={slug}`로 상대 이미지 경로(예: `figures/fig-NN.svg`)가 슬러그 디렉터리 기준으로 해석된다. 스크립트 전문은 `scripts/build_epub.sh` 참조.

## 스타일시트 (base 타이포그래피 + 구조화 블록, v1.8.0+)

`styles/epub.css`를 스크립트가 자동으로 임베드한다(스크립트 위치 기준 상대 경로). pandoc 3.x의 `--css`는 EPUB 기본 스타일시트를 **대체**하므로, 이 파일은 **기본 타이포그래피(표·코드·인용·헤딩·figure)** 와 **구조화 블록 클래스**(`meta`/`ingredients`/`steps`/`tip`/`warning`/`itinerary`, 태스크 리스트)를 함께 제공한다. 한글 본문 폰트 스택·모노스페이스 코드 폰트·다크 모드(`prefers-color-scheme: dark`) 대비까지 포함한다. 실용서(practical) 챕터는 블록 클래스를 pandoc fenced div(`::: meta` 등)로 작성한다(규약은 `profiles/practical/scaffolds.md`). CSS 파일이 없으면 스크립트는 `--css` 없이 진행한다(이 경우 기본 타이포그래피도 빠지므로 권장하지 않음).

## 식별자(identifier) 발급·보존

EPUB의 `urn:uuid:*` 식별자는 **신간에 1회 발급**되고 이후 재빌드에서 **그대로 보존된다(불변)** — 재빌드 때는 version/date만 바뀐다. 매니페스트의 `identifier`가 비어 있거나 플레이스홀더 `urn:uuid:...`이면 스크립트가 `urn:uuid:{uuid4}`를 발급해 매니페스트에 기록한다. 한 번 발급된 식별자는 수동으로 바꾸지 않는다. `_prev`에 다른 식별자가 있으면 경고를 출력한다.

## 그림(figure) — mermaid 사전 처리 (옵션)

구조·관계를 나타내는 그림은 본문에 ```` ```mermaid ```` fenced 블록 + `그림 N. {설명}` 캡션 줄로 작성한다(챕터별 N 번호). 빌드 시 `mmdc`가 설치되어 있으면 pandoc 전에 각 블록을 `{slug}/figures/fig-NN.svg`로 렌더하고 fence를 `![caption](figures/fig-NN.svg)`로 치환한다. `mmdc`가 없으면 fence를 그대로 두고(코드 블록으로 렌더) 경고만 남긴다 — **mmdc는 하드 의존성이 아니다**(옵션 epubcheck와 동일 패턴).

## 파일명 규칙

- `{책-제목}-v{version}.epub`
- 제목의 공백·유니코드 대시(U+2010–U+2015) 연속은 하나의 `-`로 축약
- 첫 번째 em-dash(`—`)나 콜론(`:`) 뒤의 부제는 잘라내고 **메인 제목만** 파일명에 사용
- Windows 금지 문자(`\ / : * ? " < > |`)는 제거
- 앞뒤 하이픈은 제거, 최대 60자로 제한
- 짝을 이루는 책 소개 `.md`의 stem은 EPUB과 **동일**해야 한다
- 예: `데이터베이스 인덱스 — 깊이 있는 안내` → `데이터베이스-인덱스-v1.0.0.epub`

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
- [ ] `epubcheck` 통과 — 실패는 빌드 실패(`EPUBCHECK_STRICT` 기본 켜짐 → 종료 코드 `5`). 미설치 시 EPUB은 검증되지 않음(`brew install epubcheck` 권장)
- [ ] 표지 alt 텍스트가 표지 xhtml에 실제로 들어갔는지 (`<img alt>` 또는 SVG `aria-label`/`<title>`)
- [ ] 재빌드 후에도 `identifier`(`urn:uuid:*`)가 직전 빌드와 동일한지
- [ ] 책 소개 md (`{책-제목}-v{version}.md`)가 EPUB 옆에 존재하고, 차례·저자·버전이 매니페스트와 일치
- [ ] `unzip -p {output} OEBPS/content.opf | grep -i rights` — `rights` 메타에 라이선스 문구 포함 (`Licensed under {license}` 또는 매니페스트의 명시값)
- [ ] `04_manuscript.md`의 `## 판권` 섹션이 매니페스트의 `license`/`version`/`pub_date`와 일치 (drift 시 editor 재호출)

## 실패 대응

| 상황 | 조치 |
|------|------|
| pandoc 미설치 | `brew install pandoc` 안내, 또는 Calibre `ebook-convert` 폴백 검토 |
| cover.png 누락 | cover-designer에 폴백 생성 요청, 메타만으로 빌드 후 경고 |
| 원고 내 비정상 유니코드·XML 문자 | 스크립트가 `iconv`로 정규화 시도, 실패 시 해당 구절 치환 |
| `epubcheck` 실패 | **빌드 실패**(각주 아님). 오류 로그(`.epubcheck.log`) 보존, `EPUBCHECK_STRICT` 기본 켜짐 → 종료 코드 `5`. 오류를 고쳐 재빌드. 부득이하게 산출만 필요하면 `EPUBCHECK_STRICT=0`으로 경고 강등 |
| `epubcheck` 미설치 | EPUB은 검증되지 않은(UNVALIDATED) 상태. stderr·빌드 로그에 `brew install epubcheck` 안내 |
| `mmdc` 미설치 | mermaid 다이어그램은 코드 fence로 남음(경고만). 그림이 필요하면 `npm i -g @mermaid-js/mermaid-cli` |
| 50KB 미만 산출물 | 챕터 변환 실패 의심 → 변환 단계별 디버깅 후 재빌드 |

## 재빌드 시

- 이전 결과를 `_prev/`로 이동
- 사용자가 매니페스트 일부만 수정한 경우 → 원고 재작업 없이 매니페스트만 갱신하고 재빌드 가능
