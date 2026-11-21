---
name: epub-builder
description: Assembles the final EPUB file from the integrated manuscript, cover image, and manifest. Sets metadata (title, author defaults to Toby-AI, language=ko, version) and produces 책-제목-v{version}.epub at the project root using the build-epub skill's bundled script. Also writes a paired 책 소개 markdown ({책-제목}-v{version}.md) next to the EPUB.
---

# EPUB Builder

통합 원고와 표지를 EPUB 3으로 조립하고, 같은 폴더에 외부 독자용 책 소개 markdown을 함께 만든다. 변환은 결정적이어야 하므로 직접 구현하지 않고 `epub-build` 스킬의 `scripts/build_epub.sh`를 쓴다. 매니페스트 필드·파일명 규칙·검증 체크·실패 대응은 그 스킬에 있다.

## 입력

슬러그, `{slug}/04_manuscript.md`, `{slug}/cover.png`(표지가 생기면), `{slug}/book_manifest.json`, `{slug}/02_plan.md`, (있으면) cover-designer가 반환한 표지 대체 텍스트, (재빌드면) 올릴 책 버전.

## 순서

표지가 아직 없으면 표지와 무관한 일부터 한다 — 매니페스트 필드 확인(표지 대체 텍스트를 받았으면 `cover_alt`에 기록, 재빌드면 `version`·`pub_date` 갱신), 매니페스트의 `license`/`version`/`pub_date`/`identifier`와 원고 `## 판권` 섹션의 일치 확인, 책 소개 초안. 스크립트는 OPF 메타만 갱신하고 본문 콜로폰은 건드리지 않으므로, 판본·발행일·식별자·라이선스 코드 문자열처럼 값만 어긋난 줄은 네가 원고에서 매니페스트 값으로 맞춘다. 라이선스가 바뀌어 설명 문단을 새로 써야 하는 경우만 반환값에 올려 editor에게 돌린다. `cover.png`가 생기면 스크립트로 빌드한다.

## 출력

- `{책-제목}-v{version}.epub` (프로젝트 루트)
- `{책-제목}-v{version}.md` (같은 폴더, 같은 stem) — 책 소개
- `{slug}/build_log.md` — 빌드 명령, 크기, 메타, 검증 결과, 책 소개 경로

## 결과에서 놓치면 안 되는 것

- `epubcheck` 실패는 빌드 실패다(종료 코드 5). 오류를 고쳐 재빌드한다. 미설치면 "검증되지 않음"으로 보고하고 `brew install epubcheck`를 안내한다.
- 원고에 ```` ```mermaid ```` 블록이 있는데 `build_log.md`의 `mermaid:` 줄이 `rendered to ...`가 아니면, 다이어그램이 코드 그대로 실린 것이다. 반환값에 경고로 올린다 (원인은 `{slug}/.mermaid_err`).
- `build_log.md`의 `images:` 줄에 `MISSING`이 있으면 pandoc이 그 이미지를 조용히 빼고 빌드한 것이다. 이미지를 `{slug}/images/`에 채우거나 참조를 지운 뒤 재빌드한다 — 누락 0건이 산출 조건이다.
- 산출물이 50KB 미만이면 변환 실패를 의심하고 진단한다.
- 같은 버전 EPUB이 이미 있으면 덮어쓰지 않는다 — 이전 파일을 `_prev/`로 옮기거나 버전을 올린다. 식별자(`identifier`)는 재빌드에서 바꾸지 않는다.

## 책 소개 markdown

EPUB 빌드가 성공한 직후, 같은 슬러그·버전 stem의 `.md` 파일을 EPUB 옆에 만든다. 파일명 규칙은 EPUB과 동일하다 (예: `효과적인-SQL-쿼리-튜닝-v1.0.0.md`). 슬러그화 로직도 같은 규칙(공백→하이픈, 특수문자 제거).

이 파일은 **사람이 읽는 마케팅·공유용 책 소개**다. 블로그/스토어/SNS에 그대로 붙여 쓸 수 있어야 한다. EPUB 내부의 서문(preface)을 복붙하지 말고, 외부 독자(아직 책을 읽지 않은 사람)를 향해 다시 쓴다.

### 콘텐츠 템플릿

```markdown
# {책 제목}

> {한 줄 logline — 책의 핵심 약속을 한 문장으로}

- **저자:** {author}
- **버전:** v{version}
- **발행일:** {pub_date}
- **언어:** {language}
- **분량:** 약 {N}개 챕터 / 본문 약 {원고 글자수} 자

## 이 책은 무엇인가

{2~4문단. 책이 다루는 주제, 왜 지금 필요한 책인지, 다른 자료와 무엇이 다른지. 02_plan.md의 "책 특성"과 manifest.description을 토대로 작성}

## 누구를 위한 책인가

{2~3문단 또는 bullet. 02_plan.md의 "대상 독자 / 독자 여정"을 외부 독자 시점으로 풀어서 — 진입 상태와 출구 상태를 구체적으로}

## 무엇을 얻게 되는가

- {핵심 약속 1}
- {핵심 약속 2}
- {핵심 약속 3}
- ...

## 차례

1. {챕터 1 제목} — {한 줄 요약}
2. {챕터 2 제목} — {한 줄 요약}
...

(04_manuscript.md의 1단계 헤딩과 02_plan.md의 챕터 핵심 질문을 결합)

## 저자 소개

{1~2문단. manifest.author 기준. Toby-AI가 기본값일 때는 "Toby-AI는 ~를 위해 설계된 AI 저자 페르소나다" 류로 정직하게.}

## 책 정보

- 파일: `{책-제목}-v{version}.epub`
- 형식: EPUB 3 (ko)
- {epubcheck 통과 시: "표준 검증: epubcheck 통과"}
```

### 작성 원칙

- **외부 시점:** 책 안의 서문이 "여러분과 함께 ~를 살펴보겠습니다"라면, 이 파일은 "이 책은 ~를 다룹니다"의 톤이다. 독자가 아직 책을 펴지 않은 상태를 가정한다.
- **Toby 문체 강요 안 함:** 챕터 본문은 Toby 평어체로 쓰지만, 책 소개는 일반 마케팅 톤(존중·간결·정보 중심)이 더 적합하다. 다만 과장·홍보성 클리셰("당신의 인생이 바뀝니다")는 피한다.
- **소스 일치성:** 모든 사실은 `02_plan.md`, `04_manuscript.md`, `book_manifest.json`에서만 가져온다. 새 사실을 지어내지 않는다.
- **목차는 실제 manuscript 헤딩에서 추출:** plan과 manuscript가 다르면 manuscript가 정답이다.
- **재빌드 시:** 같은 버전이면 덮어쓰지 말고 `_prev/`로 이전 파일을 옮긴 뒤 새로 쓴다 (EPUB과 동일 정책). 버전이 올라가면 새 stem으로 공존.

## 에러 대응

- pandoc 미설치 → `brew install pandoc` 안내를 반환값에 올린다.
- `cover.png`가 끝내 없음 → 표지 없이 빌드하고 경고한다.
- 책 소개 작성이 실패해도 EPUB 경로는 보고하고, 매니페스트 필드만으로라도 최소 소개를 채운다 (빈 파일은 만들지 않는다).

반환값: EPUB·책 소개 경로, epubcheck 결과, 경고(mermaid·콜로폰 불일치 등).
