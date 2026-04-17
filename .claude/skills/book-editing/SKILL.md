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
6. **부속 자료 작성** — 서문, 에필로그, 참고문헌, (선택) 용어집
7. **통합** — `04_manuscript.md`로 합본 저장
8. **매니페스트 생성** — `book_manifest.json` 작성
9. **스타일 점검 요청** — 필요 시 `style-guardian`에게 전체 훑기

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

## 출력 형식

`04_manuscript.md`:

```markdown
# {책 제목}

**저자:** Toby-AI
**버전:** {version}
**발행일:** {date}

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
  "version": "1.0.0"
}
```

## 재편집 시

- 일부 챕터만 갱신 → 해당 섹션만 교체 후 전체 재저장
- 서문·에필로그 개선 요청 → 해당 섹션만 다시 작성, 버전 증가
- 내용 변경 제안은 반드시 `editor_notes.md`에 기록 (직접 수정 금지)
