# 장르 프로필 레지스트리

하네스의 voice·스캐폴드·스타일 체크리스트는 더 이상 하나로 고정되지 않는다. 장르마다 한 벌씩 묶여 `profiles/{genre}/`에 산다. 오케스트레이터가 Phase 0에서 장르를 확정하면, 그 디렉토리가 Phase 2(계획)·4(저술·검수)의 입력으로 흘러간다.

## 프로필 목록

| genre | 디렉토리 | 적용 대상 | voice 한 줄 |
|-------|----------|----------|-------------|
| `tech-book` | `profiles/tech-book/` | IT·기술서·입문서·최신 기술 해설 (**기본값**) | Toby 문체 — 함께 생각하는 선배 개발자 |
| `narrative` | `profiles/narrative/` | 소설·서사·스토리 중심 논픽션 | 보여주는 산문 — 씬·시점·대사로 끌고 간다 |
| `practical` | `profiles/practical/` | 요리·여행·DIY·실용 가이드 | 명료한 안내자 — 따라 하면 되는 단계와 안전 |
| `essay` | `profiles/essay/` | 에세이·사색·주제 칼럼 | 사색하는 1인칭 — 일화에서 통찰로 |

장르 미지정·미감지 시 **`tech-book`이 기본값**이다 (하위호환: 기존 책·`toby-book-writing-style.md` 참조가 안 깨진다).

## 각 프로필의 구성

| 파일 | 역할 | 누가 읽나 |
|------|------|----------|
| `voice.md` | 문체·어조·표현 사전·금지 표현 | chapter-writer, chapter-writing 스킬 |
| `scaffolds.md` | 챕터/섹션 유형별 구조 템플릿 | chapter-writer, book-planner |
| `style-checklist.md` | 검수 체크리스트 (편차 항목) | style-guardian, style-review 스킬 |

## 자동 감지 규칙 (Phase 0)

오케스트레이터는 주제·주요 내용·대상 독자를 보고 아래 신호로 장르를 **추정**한 뒤, `AskUserQuestion`으로 사용자에게 **확인**한다(추정값을 첫 옵션·추천으로). 사용자가 틀렸다고 하면 교체한다.

| 신호 | 추정 장르 |
|------|----------|
| 코드·프레임워크·언어·아키텍처·"개발자/엔지니어" 대상 | `tech-book` |
| 인물·줄거리·"소설/이야기", 허구 세계관 | `narrative` |
| 레시피·여행지·"~하는 법"·도구·단계별 실습·여행/요리 | `practical` |
| 개인 경험·사색·"~에 대하여"·칼럼·주제 탐구(비실용·비허구) | `essay` |
| 신호가 약하거나 혼재 | `tech-book` (기본) 추천 + 사용자 확인 |

`최신 기술` 주제(빠르게 변하는 API·버전·릴리스 다수)는 `tech-book` 프로필을 쓰되, voice의 "신선도·사실 규율" 섹션과 style-checklist의 사실 항목이 강하게 작동한다.

## 매니페스트 기록

확정된 장르는 `book_manifest.json`의 `genre` 필드에 기록된다. 재실행 시 같은 프로필이 결정적으로 재사용된다 (사용자가 명시적으로 장르 변경을 요청하지 않는 한).

## 새 프로필 추가하기

1. `profiles/{new-genre}/`에 `voice.md`·`scaffolds.md`·`style-checklist.md` 작성
2. 위 "프로필 목록"과 "자동 감지 규칙" 표에 행 추가
3. `CLAUDE.md` 변경 이력에 기록
