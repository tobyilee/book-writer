---
name: book-editing
description: Integrate all finished chapters into a single book-ready manuscript — polish chapter transitions, unify terminology, insert cross-chapter callbacks, and write front/back matter (preface, epilogue, references). Produce a manuscript + book_manifest.json for EPUB build. Use when chapters are individually complete and need to become a coherent book.
---

# Book Editing

완성된 챕터들을 한 권의 책으로 직조한다. 내용을 새로 쓰지 않고 흐름과 일관성을 다듬는다. 병렬로 쓴 챕터들을 처음으로 한꺼번에 보는 단계라서, 묶음 경계의 전환과 통권 단조로움은 여기서 잡는다.

## 절차

1. 모든 `{NN}_final.md`가 있는지 확인한다. 빠진 장은 `[미완성]` 주석과 함께 자리만 두고 보고한다.
2. 묶음 사이에서 갈린 것을 맞춘다 (아래 "장 간 정합").
3. 1장부터 순서대로 읽으며 전환부를 다듬는다 — 끝-시작 연결이 갑작스럽지 않은지, 여러 장이 같은 이음말로 끝나지 않는지.
4. 용어를 `02_plan.md`의 "용어 표기"에 맞춰 통일하고, 뒤 장이 앞 개념을 쓸 때 "앞서 3장에서 살펴봤듯이 ~" 같은 콜백을 자연스럽게 넣는다. 콜백의 장 번호는 실제 그 내용이 있는 장이어야 한다. 저술가가 써 둔 콜백과 예고("3장에서 봤듯이", "9장에서 다룬다")도 가리키는 장에 실제로 그 내용이 있는지 확인한다 — 저술가는 다른 묶음의 원고를 보지 못하고 썼다.
5. 통권 변주를 점검하고 고친다 (아래).
6. 부속 자료(서문·목차·에필로그·참고문헌·콜로폰)를 장르에 맞게 쓴다. practical 요리 계열이면 `profiles/practical/partials/conversion-tables.md`의 환산표를 부록에 복사한다.
7. `04_manuscript.md`로 합본하고, `book_manifest.json`을 쓰고, 빌드 안전 점검(아래)을 한 뒤 분량 리포트를 만든다.

## 장 간 정합

저술가들은 서로의 원고를 보지 못했고 fact-checker도 묶음별로 따로 봤다. 장 안에서는 맞지만 장 사이에서 어긋나는 것은 여기서만 잡힌다. 지금까지 수락 게이트가 가장 자주 막은 것이 이 부류다.

- **예제 정전.** `02_plan.md`의 "공유 정전"과 `integration_notes.md`(저술가들이 정전 밖에서 새로 정한 것의 목록)를 기준으로, 러닝 예제의 이름·경로·스키마·컬럼·시그니처·메시지 형태가 장마다 같은지 본다. 같은 것을 두 묶음이 다르게 정했으면 먼저 나온 장(또는 계획이 주 담당으로 정한 장)에 맞춘다. 뒤 장이 앞 장의 코드를 이어 쓰면 실제로 이어지는지(없는 컬럼, 중복 선언, 바뀐 권한) 대조한다.
- **사실 판정.** `factcheck_log.md`의 ❌ 정정·⚠️ 약화·`[원장 오류]` 항목마다 고치기 전 표현을 원고 전체에서 grep한다. 다른 묶음의 장에 같은 주장이 남아 있으면 같은 판정으로 맞춘다. 참고문헌·부록에도 적용한다.

값을 정전·판정에 맞추는 수정은 여기서 직접 한다. 맞추려면 절의 설계를 바꿔야 하는 충돌은 고치지 않고 `editor_notes.md`와 반환값에 올린다.

## 통권 변주 점검

장마다 (a) 오프닝 기법, (b) 클로징 형태, (c) 최다 반복 말버릇을 한 줄씩 표로 만든다.

```
| 장 | 오프닝 기법 | 클로징 형태 | 최다 반복 말버릇 |
|----|------------|------------|-----------------|
| 1  | 상황 가정   | 적용 과제   | ~해보자 (9)      |
| 2  | 실패 장면   | 다음 장 예고 | 그렇다면 (6)     |
```

인접 장의 같은 오프닝, '상황 가정' 오프닝이 전체의 1/3 초과(tech-book), 같은 클로징 공식의 반복, 책 전반에 과포화된 말버릇을 찾아 해당 문단을 고친다. 반복 횟수는 grep으로 센다. 표는 `editor_notes.md`에 남긴다 — 수락 게이트가 참고한다.

## 용어 통일 원칙

- 기준은 `02_plan.md`의 "용어 표기"다. 거기 없는 용어가 여러 표기(영문/한글, 축약/풀)로 흔들리면 가장 많이 쓰인 표기로 맞춘다
- 예외: 장르가 기술서면 "사용자"보다 "유저"가 자연스러울 때도 있음 — 문맥 우선
- 결정 불가능 → 서문에 "이 책에서는 {A}를 {B}로 표기한다" 정의

## 서문 작성 지침

- 왜 이 책을 썼는가 (문제의식)
- 이 책을 누가 읽으면 좋은가 (대상 독자)
- 어떻게 읽으면 좋은가 (순서·선택 독서 가이드)
- 감사의 말 (선택)
- 길이: 2~4페이지 분량

## 에필로그 작성 지침

- 여정을 짧게 돌아봄
- 책이 답하지 못한 질문들
- 다음 걸음에 대한 제안 (추천 도서·실천 과제)
- 길이: 1~2페이지

## 참고문헌

- 챕터에서 인용한 출처를 모아 단일 목록으로 정렬하고 중복을 없앤다. 정렬 방식(인용 순서 또는 저자 가나다순)은 하나로 통일한다.
- 형식: `저자. 제목. 발행처/URL, 날짜.`
- 서지 정보·식별자·확인 등급 라벨은 `research/*.md`와 `factcheck_log.md`에서 그대로 옮긴다. 원장에 없는 항목은 넣지 않는다.
- 독자가 찾아갈 수 있는 공개 출처만 적는다. `research/community.md`의 패턴 번호 같은 내부 작업 파일이나 공정 메모("확인 필요", "2차 보도")를 출처로 쓰지 않는다.
- URL은 `[제목](URL)`이나 `<URL>`로 적는다. 맨 URL은 EPUB에서 링크가 되지 않는다.
- 부록의 표·점검표도 본문·원장에 있는 사실만 옮긴다. 본문에서 약화·정정된 사실이 부록에 옛 값으로 남지 않게 한다.

## 빌드 안전 점검

합본한 뒤 EPUB 빌드를 깨거나 책 밖의 말이 지면에 새는 것을 grep으로 확인하고 고친다.

```bash
# 코드 밖 산문의 <한글…> — 변환기가 HTML 태그로 읽어 epubcheck가 실패한다. `\<…\>`나 코드 스팬으로 바꾼다
grep -nE "<[가-힣][^>]*>" {slug}/04_manuscript.md
# 하네스 내부 역할·파일 이름이 본문에 노출됐는지
grep -nE "리서처|fact-?checker|팩트체커|레퍼런스 문서|01_reference|research/|원장|오케스트레이터" {slug}/04_manuscript.md
# 절(##)이 하나도 없는 장 — EPUB 목차에 절이 실리지 않는다
awk '/^# [0-9]+장/{if(ch&&!n)print ch; ch=$0; n=0} /^## /{n++} END{if(ch&&!n)print ch}' {slug}/04_manuscript.md
```

첫 grep은 코드 블록 안의 일치도 보여주므로 산문에 있는 것만 고친다. 둘째 grep에서 주제상 정당한 쓰임(책이 리서치나 원장을 다루는 경우)은 그대로 둔다.

## 분량 균형 점검

글자 수는 눈대중이 아니라 스크립트로 센다:

```bash
python3 .claude/skills/book-editing/scripts/length_report.py {slug} > {slug}/length_report.md
```

스크립트는 `04_manuscript.md`가 있으면 그것을 `# N장` 헤딩으로 나눠 센다 — 실제로 출간되는 글이 기준이다(합본 전이거나 `--chapters`를 주면 `chapters/`의 장 파일을 센다). 표·코드·mermaid·`:::` 블록·인용·헤딩을 뺀 산문 글자 수(공백 포함)를 장별로 세고, 중앙값 대비 70% 미만이나 150% 초과인 장, `02_plan.md`의 예상 분량과 ±20% 넘게 어긋나는 장, 중앙값 아래로 떨어진 1장(첫인상을 만드는 장이다)을 표시한다. 의도적으로 짧은 장(막간 등)은 리포트 끝에 사유를 적어 예외로 둔다. 플래그된 장은 반환값에 올린다 — 확장·축약 여부는 수락 게이트와 오케스트레이터가 정한다.

## 출력 형식

`04_manuscript.md`:

```markdown
# {책 제목}

## 저자
{author}

**판본:** v{version} · {pub_date}

---

## 판권

**{책 제목}**
**판본:** v{version}
**발행일:** {pub_date}
**저자:** {author}
**식별자:** {identifier}

### 라이선스

이 책은 **CC BY-NC-SA 4.0** 라이선스로 배포된다 — [Creative Commons 저작자표시-비영리-동일조건변경허락 4.0 국제](https://creativecommons.org/licenses/by-nc-sa/4.0/).

- **저작자 표시(BY):** 출처를 밝혀야 한다.
- **비상업적 이용(NC):** 상업적 목적으로 이용할 수 없다.
- **동일조건 변경허락(SA):** 변경·재배포 시 동일한 라이선스를 적용해야 한다.

매니페스트에 `license` 필드가 다른 값으로 명시되어 있으면 그 값으로 위 문장과 링크를 갈음한다. 어느 경우든 매니페스트 `license`의 정식 코드 문자열이 지면에 그대로 나와야 한다 — `epub-build`가 콜로폰과 매니페스트의 `license` 문자열 일치를 대조한다.

### 출처

이 책은 [book-writer](https://github.com/tobyilee/book-writer) 하네스 v{harness_version}로 자동 생성되었다.

---

## 서문
...

## 목차
- 1장. ...
- 2장. ...

---

# 1장. {제목}
(전환부 다듬어진 본문)

# 2장. ...

...

# 에필로그
...

# 부록 A. {제목}
...

# 참고문헌
...
```

장 뒤에 오는 에필로그·부록·참고문헌은 `#`로 쓴다. 빌드가 `#` 단위로 파일을 나누고 목차를 만들기 때문에, `##`로 쓰면 마지막 장의 절로 흡수돼 목차에서 그 장 아래에 매달린다. 책 제목 `#` 아래의 저자·판권·서문·목차는 앞부속 한 묶음이므로 `##` 그대로 둔다. 제목은 `02_plan.md`의 "확정 제목"을 쓴다.

`book_manifest.json`:

```json
{
  "title": "...",
  "subtitle": "...",
  "author": "Toby-AI",
  "language": "ko",
  "pub_date": "YYYY-MM-DD",
  "identifier": "urn:uuid:...",
  "description": "한 문단 소개",
  "cover_image": "cover.png",
  "cover_alt": "{title} 표지",
  "version": "1.0.0",
  "license": "CC BY-NC-SA 4.0",
  "genre": "tech-book",
  "delegation_mode": "production",
  "harness_version": "2.1.0",
  "rights": "© {year} {author} — Licensed under {license}"
}
```

`license`, `harness_version`, `rights`는 옵션 필드. 비우면 빌드 스크립트가 하네스 기본값(`CC BY-NC-SA 4.0` + 루트 `VERSION` + 자동 생성 rights)으로 채운다. `genre`는 오케스트레이터가 확정한 장르(`tech-book`/`narrative`/`practical`/`essay`)를 기록한다 — 재실행 시 활성 프로필을 결정적으로 재사용하는 출처다. 누락 시 `tech-book`. `delegation_mode`는 오케스트레이터가 Phase 0에서 확정한 위임 다이얼(`production`/`learning`)을 같은 취급으로 기록한다 — 재실행 시 학습 터치포인트를 결정적으로 재사용하는 출처다. 누락 시 `production` (`docs/learning-loop.md`).

`cover_alt`는 표지 이미지의 대체 텍스트로, 빌드 스크립트의 alt-text 주입이 이 값을 출처로 쓴다. 비우면 기본 패턴 `"{title} 표지"`를 적용한다.

**식별자(identifier) 발급 규칙:** `identifier`는 **신규 책일 때 한 번만** 생성한다 — `python3 -c "import uuid;print('urn:uuid:'+str(uuid.uuid4()))"`. 플레이스홀더 `"urn:uuid:..."`를 그대로 복사하지 않는다. 같은 책 재빌드 시 기존 `book_manifest.json`의 `identifier`를 **그대로 보존**하고 `version`만 올린다 (식별자는 책의 영구 ID — 재빌드마다 바뀌면 안 된다).

## 재편집 시

- 합본 뒤의 정본은 `04_manuscript.md`다. 부분 수정은 원고에서 직접 한다 — 장 파일에서 고쳐 다시 합치면 통합 때 다듬은 전환부·오프닝이 사라진다.
- 장이 통째로 다시 쓰였으면 → 원고의 그 장만 새 `{NN}_final.md`로 교체하고 앞뒤 전환부, 장 간 정합, 분량 리포트를 다시 본다.
- 서문·에필로그 개선 요청 → 해당 섹션만 다시 쓴다.
- 구조·내용 변경 제안은 `editor_notes.md`에 적는다.
