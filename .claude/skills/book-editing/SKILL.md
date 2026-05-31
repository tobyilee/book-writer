---
name: book-editing
description: Integrate all finished chapters into a single book-ready manuscript — polish chapter transitions, unify terminology, insert cross-chapter callbacks, and write front/back matter (preface, epilogue, references). Produce a manuscript + book_manifest.json for EPUB build. Use when chapters are individually complete and need to become a coherent book.
---

# Book Editing

완성된 챕터들을 **한 권의 책**으로 직조한다. 내용을 새로 쓰지 않고, 흐름과 일관성만 다듬는다.

## 절차

1. **확인** — 모든 `{NN}_final.md` 존재 여부
2. **순회 읽기** — 1장부터 마지막까지 순서대로
3. **전환부 점검** — 각 챕터 끝 단락과 다음 챕터 시작 단락의 연결 품질
4. **용어 통일** — 불일치 발견 시 한쪽으로 정렬 (기준은 `02_plan.md`의 용어 표기를 따름)
5. **콜백 삽입** — 뒤 챕터가 앞 개념을 언급할 때 자연스러운 참조 추가
6. **부속 자료 작성** — 서문, 에필로그, 참고문헌, (선택) 용어집. 장르에 맞춘다: narrative=작가의 말/헌사(참고문헌 보통 생략), practical="이 책 활용법"+준비물 총정리, essay=짧은 머리말, tech-book=현행 그대로
7. **통합** — `04_manuscript.md`로 합본 저장
8. **분량 균형 점검** — 챕터별 분량 편차 확인 (아래 "분량 균형 점검" 절차)
9. **매니페스트 생성** — `book_manifest.json` 작성
10. **스타일 점검 요청** — `style-guardian`에게 통합 원고 전체 변주 점검(책 단위 whole-book 점검)을 **반드시** 요청한다. 이 단계는 생략하지 않는다 — 최종 확정 전 책 전체의 문장·오프닝 변주가 한 번 더 검수되어야 한다

## 전환부 체크

- 끝-시작 연결이 갑작스럽지 않은가?
- 다음 장 예고가 너무 길거나 짧지 않은가?
- 같은 표현("다음 장에서는 ~를 살펴보자")이 모든 챕터 말미에 반복되는가?

## 용어 통일 원칙

- 한 용어의 여러 표기(영문/한글, 축약/풀)가 있으면 **가장 많이 쓰인 표기** 기준
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

- 챕터 각주를 모아 단일 목록으로 재정렬
- 중복 제거
- 정렬: 인용 순서 or 저자 가나다순 (한 방식 고수)
- 형식 통일: `저자. 제목. 발행처/URL, 날짜.`

## 분량 균형 점검

챕터 간 분량 편차가 크면 독서 리듬이 무너진다. 통합 후 다음을 점검한다.

1. **코드 제거 후 글자 수 계산** — 챕터별로 코드 블록(```` ``` ````로 둘러싸인 영역)을 제외한 본문 글자 수를 센다
2. **편차 플래그** — 중앙값(median) 대비 **70% 미만**이거나 **150% 초과**인 챕터를 표시한다. (`02_plan.md`에 챕터별 "예상 분량"이 있으면 그 값 대비 ±20%를 함께 기준으로 쓴다)
3. **오프닝 챕터 가드** — **1장(훅 챕터)이 중앙값 아래로 떨어지지 않게** 특별히 살핀다. 첫 장이 빈약하면 책의 첫인상이 죽는다
4. **리포트 작성** — `{slug}/length_report.md`에 챕터별 글자 수·중앙값·플래그를 기록한다
5. **조치 요청** — 플래그된 챕터는 해당 `chapter-writer`에게 표적 확장/축약을 요청하거나, 정당한 사유(예: 의도적으로 짧은 막간 장)가 있으면 `length_report.md`에 예외로 명시한다

`length_report.md` 예시:

```markdown
# 분량 균형 리포트

| 장 | 코드 제외 글자 수 | 중앙값 대비 | 예상 분량 대비 | 판정 |
|----|------------------|------------|---------------|------|
| 1장 | 8,200 | 96% | -4% | OK (훅 챕터, 중앙값 이상 확인) |
| 2장 | 5,100 | 60% | -35% | ⚠️ 축소됨 — 확장 요청 |
| 3장 | 13,400 | 158% | +30% | ⚠️ 비대 — 축약 또는 분할 검토 |

중앙값: 8,500자
조치: 2장 확장 요청, 3장 축약 요청.
```

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

이 책은 [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 라이선스로 배포된다.

- **저작자 표시(BY):** 출처를 밝힐 것.
- **비상업적 이용(NC):** 상업적 목적으로 이용할 수 없다.
- **동일조건 변경허락(SA):** 변경·재배포 시 동일한 라이선스를 적용해야 한다.

매니페스트에 `license` 필드가 다른 값으로 명시되어 있으면 그 값으로 위 문장과 링크를 갈음한다.

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

## 에필로그
...

## 참고문헌
...
```

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
  "harness_version": "1.8.0",
  "rights": "© {year} {author} — Licensed under {license}"
}
```

`license`, `harness_version`, `rights`는 옵션 필드. 비우면 빌드 스크립트가 하네스 기본값(`CC BY-NC-SA 4.0` + 루트 `VERSION` + 자동 생성 rights)으로 채운다. `genre`는 오케스트레이터가 확정한 장르(`tech-book`/`narrative`/`practical`/`essay`)를 기록한다 — 재실행 시 활성 프로필을 결정적으로 재사용하는 출처다. 누락 시 `tech-book`.

`cover_alt`는 표지 이미지의 대체 텍스트로, 빌드 스크립트의 alt-text 주입이 이 값을 출처로 쓴다. 비우면 기본 패턴 `"{title} 표지"`를 적용한다.

**식별자(identifier) 발급 규칙:** `identifier`는 **신규 책일 때 한 번만** 생성한다 — `python3 -c "import uuid;print('urn:uuid:'+str(uuid.uuid4()))"`. 플레이스홀더 `"urn:uuid:..."`를 그대로 복사하지 않는다. 같은 책 재빌드 시 기존 `book_manifest.json`의 `identifier`를 **그대로 보존**하고 `version`만 올린다 (식별자는 책의 영구 ID — 재빌드마다 바뀌면 안 된다).

## 재편집 시

- 일부 챕터만 갱신 → 해당 섹션만 교체 후 전체 재저장
- 서문·에필로그 개선 요청 → 해당 섹션만 다시 작성, 버전 증가
- 내용 변경 제안은 반드시 `editor_notes.md`에 기록 (직접 수정 금지)
