# 5장. 개발자의 일상에 녹이기 — 코드 리뷰·ADR·TIL·회고

월요일 오전 10시, 스프린트 회의가 끝나고 PR 리뷰가 5건 쌓여 있다. 점심 전까지 두 개는 봐야 한다. 오후엔 신규 인증 모듈 ADR을 써야 하고, 4시엔 어제 발생한 결제 장애 회고가 잡혀 있다. 사이사이 슬랙 멘션, 신입에게 온 코드 질문, 사내 위키에 정리해둬야 할 안건들. 노트할 시간이 어디 있나.

이런 일정에서 "옵시디언을 켜고 30분 fleeting 캡처를 해봅시다"라는 말은 거의 농담이다. 4장에서 우리가 다룬 건 개인 학습 루틴이었다. 출근 전 아침, 점심 후, 퇴근 후 30분 — 비교적 한가한 시간을 잘 분배하는 이야기였다. 하지만 정작 회사 시간에는 이걸 어떻게 녹일 수 있을까? 그리고 더 중요한 질문 — 내가 회사 자료를 vault에 적어도 회사가 그걸 문제 삼지 않을까?

이 장은 그 두 질문에 답한다. 4장이 학습 루틴이었다면, 5장은 업무 산출물과의 결합이다. 코드 리뷰 중에 떠오른 패턴, ADR 작성, TIL 누적, 회의록과 일감, 온콜 회고, 오픈소스 기여 — 이 모두가 같은 vault 안에서 어떻게 흐를 수 있는지를 본다. 그리고 마지막 절(§5.8)에서 한국 IT 환경의 보안 정책 현실을 13항목 체크리스트로 마주한다. 금융권에 다니는 독자, 공공기관 협력사 개발자, 대기업 SI 인력 — 이런 분들이 "이 책 좋은데 우리 회사에선 못 쓰겠다"로 끝나지 않도록.

먼저 솔직한 고백 하나. 나도 처음 1년은 이걸 못했다. vault는 집에서만 켜고, 회사 일은 사내 위키와 Jira에만 적었다. 그러다 vault에 누적된 atomic note 몇 개가 회사 ADR 회의에서 결정적인 인용이 되는 경험을 한 후에야, "두 vault를 섞을 수 있구나"를 깨달았다. 그 깨달음을 어떻게 안전하게 시스템화하는지가 이 장의 본론이다.

## 5.1 코드 리뷰 노트 — 패턴은 N번 반복되면 노트가 된다

PR 리뷰는 개발자에게 가장 풍부한 학습의 순간이다. 동료가 작성한 코드를 읽으면서 "어, 이런 식으로도 되는구나", "이 패턴은 왜 여기서 안 좋은가", "지난주에 다른 PR에서 본 패턴이랑 비슷한데 결말이 달랐지" 같은 사고가 끊임없이 일어난다. 그런데 이 사고들이 어디로 가는가? 대부분은 PR 코멘트 한 줄로 휘발된다. PR이 머지되고 나면 그 사고도 같이 닫힌다.

이걸 vault에 흘려보내는 패턴이 있다. **PR 한 건당 fleeting 1~3개를 캡처하고, 같은 패턴이 N번(보통 3~5회) 반복되면 atomic permanent로 승격한다.**

리뷰 중에 떠오른 패턴을 그 자리에서 한 줄로 적는다. 옵시디언이 켜져 있다면 `Ctrl+N`으로 새 노트를 열어 한 줄을 적고 닫으면 된다. 켜져 있지 않다면 fleeting note 캡처 도구(3장 인서트 박스의 iOS Drafts나 Android 캡처 앱)에 한 줄 적는다. 형식은 신경 쓸 필요 없다. 이런 식이다.

```
2026-05-12 PR-1842 리뷰
- async 함수에서 try/finally로 락 해제 보장 — 우리 코드베이스에 비슷한 패턴 부재
- 에러 메시지에 사용자 ID 안 찍힘 — 트레이싱 어려움
```

이게 fleeting이다. 주간 리뷰 시간에 이 fleeting 더미를 다시 본다. 같은 패턴이 다른 PR에서도 나왔다면, 즉 N번 반복된 패턴이라면, atomic permanent로 승격한다.

```markdown
---
type: permanent
created: 2026-05-15
tags: [#permanent, #engineering/error-handling]
---

# async 컨텍스트에서 락 해제는 try/finally로 보장한다

Python·JavaScript·Kotlin의 async 함수에서 락을 획득한 후 await 포인트가 있으면, 예외가 던져지거나 task가 cancel될 때 락이 해제되지 않을 수 있다. try/finally로 감싸는 것이 가장 단순한 해결이고, with 구문(Python)·using 구문(C#)이 있다면 그쪽이 더 안전하다.

## 왜 흔한 실수인가
sync 코드에서는 함수 종료 시 스택이 정리되며 락이 해제되는 게 자연스러웠다. async에서는 await 포인트가 사실상 함수 종료점처럼 동작할 수 있어서 직관이 깨진다.

## 우리 코드베이스 적용
- [[PR-1842 리뷰 코멘트]]에서 처음 발견
- [[PR-1923 리뷰 코멘트]]에서 다시 발견
- [[PR-2104 리뷰 코멘트]]에서 또 발견 — atomic으로 승격 결정

## 관련 노트
- [[비동기 컨텍스트의 자원 관리]]
- [[락 획득 실패와 데드락의 구분]]
```

이렇게 만들어진 atomic note는 다음 코드 리뷰에서 인용된다. PR 코멘트에 "이 패턴은 [[async 컨텍스트에서 락 해제는 try/finally로 보장한다]]에 정리해둔 것과 같습니다"라고 쓸 수 있다(공개할 수 있는 vault라면). 사내 위키 링크로 변환해서 코멘트에 붙여도 된다. 시간이 지나면 같은 코드 리뷰 패턴을 매번 다시 설명하지 않아도 된다.

여기서 한 가지 짚자. **N번이 어디부터 N인가?** 너무 일찍 승격하면 vault에 어설픈 노트가 쌓인다. 너무 늦게 승격하면 여러 PR에서 같은 사고를 반복한다. 경험적으로는 3~5회가 좋다. 한 번은 우연, 두 번은 패턴의 실마리, 세 번은 진짜 패턴, 다섯 번이면 사내 표준이 될 만한 것. 본인의 코드베이스 사이즈와 PR 빈도에 따라 조정하자.

## 5.2 ADR — Architecture Decision Record를 vault에 두는 이유

ADR은 아키텍처 결정을 문서로 남기는 관행이다. Michael Nygard가 2011년에 제안한 형식이 출발점이고, 이후 Matteo Paoli의 MADR(Markdown Architectural Decision Records) 같은 변형이 널리 쓰인다. 형식은 단순하다 — 결정의 맥락(Context), 결정의 내용(Decision), 결과(Consequences). 한 결정이 한 파일이고, 시간 순으로 번호를 부여한다.

대부분의 팀은 ADR을 코드 리포지터리 안에(`docs/adr/` 같은 폴더) 두거나 사내 위키에 둔다. 그것도 좋다. 하지만 vault 안에 같이 두면 두 가지 이점이 생긴다.

**첫째, 백링크로 결정의 진화를 추적할 수 있다.** ADR-007이 ADR-003을 supersede(대체)한다면, 단순히 본문에 "supersedes ADR-003"이라고 적는 것보다 `[[ADR-003 인증 모듈 선택]]`을 백링크로 거는 게 낫다. ADR-003 노트의 백링크 패널에 자동으로 ADR-007이 나타나서 "이 결정은 나중에 어떻게 되었는가"를 한눈에 본다. 사내 위키에서는 이 양방향성을 흉내 내려면 양쪽 문서를 다 수정해야 하지만, vault에서는 한 쪽만 걸면 자동이다.

**둘째, atomic permanent note와 결정이 연결된다.** ADR-007에서 "Postgres에서 RDS Aurora로 마이그레이션한다"고 결정했다면, 그 결정의 근거가 된 atomic note들 — `[[Aurora의 read replica는 더 빠른 failover를 제공한다]]`, `[[RDS의 storage autoscaling 한계]]`, `[[우리 워크로드의 read/write 비율은 80/20]]` — 을 그대로 인용할 수 있다. 6개월 후에 결정을 재검토할 때, 그때 어떤 사실에 기반해 결정했는지가 노트로 박제되어 있다. "그땐 왜 이렇게 결정했지?"가 사라진다.

ADR을 어떻게 자동화할지는 §5.3에서 Templater 스니펫으로 다룰 거다. 먼저 형식부터 정착시키자. MADR 0.4 기준 템플릿은 이렇다.

```markdown
---
type: adr
status: proposed
adr-id: 008
date: 2026-05-15
deciders: [tobylee, jane.kim, mark.lee]
tags: [#adr, #db, #migration]
---

# ADR-008: 결제 DB를 Aurora MySQL로 마이그레이션

## Context (배경)
현재 결제 트랜잭션은 단일 RDS PostgreSQL 인스턴스에서 처리되고 있다.
지난 분기 트래픽이 2.3배 증가하면서 read 쿼리가 write를 차단하는 사례가
주 1회 발생하고 있다. 또한 region failover에 5~7분이 소요된다.

## Decision (결정)
결제 DB를 RDS Aurora MySQL로 마이그레이션한다.
- read replica를 region별 2개씩 두어 read 부담 분산
- failover RTO 목표는 90초 이내
- 마이그레이션은 2026-Q3 내 완료

## Considered Options (검토한 대안)
1. Aurora MySQL — 채택
2. Aurora PostgreSQL — 호환성은 좋지만 read replica 증설 비용이 1.4배
3. 현재 Postgres 유지 + read replica 증설 — failover 문제 미해결

## Consequences (결과·영향)
- 긍정: failover 단축, read scale-out 용이
- 부정: PostgreSQL 고유 기능(JSONB 일부, 풀텍스트 검색) 마이그레이션 필요
- 부정: 팀 전체 MySQL 학습 곡선 약 2주

## 관련 노트
- [[Aurora의 read replica는 더 빠른 failover를 제공한다]]
- [[우리 워크로드의 read/write 비율은 80/20]]
- [[ADR-003 결제 DB 선택]] — 현 결정의 supersede 대상
```

이 형식을 매번 손으로 쓰면 번거롭다. 그래서 다음 절에서 Templater로 자동화한다.

## 5.3 Dataview·Templater 실전 — 5개의 동작하는 코드

Obsidian의 진짜 매력이 드러나는 지점이 여기다. 마크다운 파일에 메타데이터를 정형화해 놓으면, Dataview 플러그인이 그걸 SQL처럼 쿼리할 수 있다. Templater 플러그인은 새 노트를 만들 때 미리 정해둔 템플릿을 자동으로 채운다. 두 플러그인을 같이 쓰면 vault가 단순한 노트 더미에서 살아 있는 데이터베이스로 변한다.

실제로 동작하는 코드 5개를 같이 살펴보자. Templater 스니펫 2개, Dataview 쿼리 3개. 그대로 복사해서 본인 vault에 붙여 넣고, 폴더 경로만 본인 환경에 맞춰 수정하면 된다. 두 플러그인 설치는 Settings → Community Plugins → Browse에서 "Templater"와 "Dataview"를 검색해서 설치 → 활성화하면 된다.

### Templater 스니펫 1 — fleeting을 permanent로 변환

매주 리뷰 시간에 Inbox의 fleeting note 중 살릴 만한 걸 permanent로 승격한다. 이때 매번 frontmatter를 손으로 채우는 게 번거롭다. Templater 스니펫 하나로 자동화하자.

`templates/Permanent Note.md` 파일을 만들고 다음 내용을 넣는다.

```markdown
---
type: permanent
status: draft
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
tags: [#permanent]
source: <% tp.file.cursor(1) %>
---

# <% tp.file.title %>

## 한 줄 주장 (claim)
<% tp.file.cursor(2) %>

## 본문
<% tp.file.cursor(3) %>

## 관련 노트
- [[<% tp.file.cursor(4) %>]]

## 메타
- 원본 fleeting: <% tp.file.cursor(5) %>
```

여기서 `tp.date.now()`는 현재 날짜를 자동으로 박는다. `tp.file.title`은 파일명을 제목으로 쓴다. `tp.file.cursor(N)`는 템플릿 적용 후 커서가 옮겨갈 위치를 표시한다. Tab 키로 다음 cursor 위치로 이동하면서 채워 가면 된다.

이 템플릿을 빠르게 호출하려면 핫키를 설정한다. Settings → Templater → Template Hotkeys → "Permanent Note" 추가 → 핫키를 `Ctrl+Alt+P`로 지정. 이제 새 빈 노트(`Ctrl+N`)를 열고 `Ctrl+Alt+P`를 누르면 위 템플릿이 자동으로 채워진다. fleeting → permanent 변환이 30초 안에 끝난다.

### Templater 스니펫 2 — ADR 자동 생성

ADR도 같은 방식으로 자동화한다. 단, ADR은 번호를 자동으로 부여해야 해서 좀 더 복잡하다. `templates/ADR.md` 파일을 만들고 다음을 넣는다.

```markdown
<%*
// ADR 폴더에서 다음 번호 계산
const adrFolder = "10_Permanent/ADR";
const files = app.vault.getMarkdownFiles()
  .filter(f => f.path.startsWith(adrFolder))
  .map(f => f.basename);
const numbers = files
  .map(name => {
    const match = name.match(/^ADR-(\d+)/);
    return match ? parseInt(match[1], 10) : 0;
  });
const nextNum = (numbers.length > 0 ? Math.max(...numbers) : 0) + 1;
const padded = String(nextNum).padStart(3, "0");

// 사용자에게 결정 제목 입력 받기
const title = await tp.system.prompt("ADR 제목 (예: 결제 DB 마이그레이션)");

// 새 파일명으로 이름 변경
const newName = `ADR-${padded} ${title}`;
await tp.file.rename(newName);
-%>
---
type: adr
status: proposed
adr-id: <% padded %>
date: <% tp.date.now("YYYY-MM-DD") %>
deciders: []
tags: [#adr]
---

# ADR-<% padded %>: <% title %>

## Context (배경)
<% tp.file.cursor(1) %>

## Decision (결정)
<% tp.file.cursor(2) %>

## Considered Options (검토한 대안)
1. <% tp.file.cursor(3) %>
2.
3.

## Consequences (결과·영향)
- 긍정:
- 부정:
- 위험:

## 관련 노트
- [[<% tp.file.cursor(4) %>]]
```

스니펫 첫 부분의 JavaScript가 핵심이다. `10_Permanent/ADR` 폴더를 스캔해서 가장 큰 ADR 번호를 찾고, 1을 더해 새 번호를 만든다. 그러고 사용자에게 제목을 받아 파일명을 `ADR-008 결제 DB 마이그레이션` 형식으로 바꾼다. frontmatter의 `adr-id`도 자동으로 채워진다.

핫키 `Ctrl+Alt+A`로 등록해두면, ADR 회의 중에도 즉석에서 새 결정 카드를 만들고 회의 내용을 바로 입력할 수 있다.

### Dataview 쿼리 1 — 고립된 노트 찾기

vault가 자라면서 가장 위험한 게 "고립된 노트"다. 만들어 놓고 백링크 한 번도 안 걸려서 시간이 지나면 사실상 사라진 노트들. 분기마다 한 번씩 이걸 찾아내서 연결을 보강하거나 폐기 결정을 내려야 한다.

빈 노트를 하나 만들고(`고립된 노트 점검.md`) 다음 코드 블록을 넣는다.

````markdown
# 지난 30일에 만든 백링크 0개 atomic note

```dataview
TABLE
  file.ctime AS "생성일",
  length(file.inlinks) AS "백링크 수",
  file.tags AS "태그"
FROM "10_Permanent"
WHERE
  type = "permanent"
  AND length(file.inlinks) = 0
  AND file.ctime >= date(today) - dur(30 days)
SORT file.ctime DESC
```
````

이 쿼리를 실행하면(자동으로 렌더링된다) 지난 30일에 `10_Permanent/` 폴더에 만들어진 노트 중 백링크가 0개인 것들이 표로 나온다. 분기 리뷰에서 이 표를 보고 결정을 내린다.

- **연결 보강 가능:** 다른 노트와 의미적으로 닿는 게 보이면 forward 링크 또는 백링크를 보강
- **수정 가능:** 제목이 너무 추상적이거나 모호해서 인용이 안 된 거면 제목을 명제 형식으로 다듬기
- **폐기 결정:** 만들 때는 의미 있어 보였지만 30일 지나도 다른 사고와 안 닿는 거면 archive 폴더로 이동

이 분기 리뷰가 vault 건강 관리의 핵심이다. 8장의 100일 KPI에서 다시 다루겠지만, 이걸 안 하면 vault가 쓰레기장으로 변하는 건 시간 문제다.

### Dataview 쿼리 2 — ADR 인덱스 자동 생성

ADR이 20개를 넘기면 손으로 인덱스 페이지를 관리하는 게 부담스러워진다. status별로 그룹핑한 인덱스를 자동으로 만들자.

`ADR Index.md` 파일에 다음을 넣는다.

````markdown
# ADR Index

## Accepted (적용 중)

```dataview
TABLE
  adr-id AS "ID",
  date AS "결정일",
  deciders AS "결정자"
FROM "10_Permanent/ADR"
WHERE
  type = "adr"
  AND status = "accepted"
SORT date DESC
```

## Proposed (제안 중)

```dataview
TABLE
  adr-id AS "ID",
  date AS "제안일",
  deciders AS "검토자"
FROM "10_Permanent/ADR"
WHERE
  type = "adr"
  AND status = "proposed"
SORT date DESC
```

## Superseded (대체됨)

```dataview
TABLE
  adr-id AS "ID",
  date AS "결정일",
  superseded-by AS "대체 ADR"
FROM "10_Permanent/ADR"
WHERE
  type = "adr"
  AND status = "superseded"
SORT date DESC
```

## Rejected (기각)

```dataview
TABLE
  adr-id AS "ID",
  date AS "검토일",
  reason AS "기각 사유"
FROM "10_Permanent/ADR"
WHERE
  type = "adr"
  AND status = "rejected"
SORT date DESC
```
````

새 ADR을 만들 때마다 이 인덱스 페이지가 자동으로 갱신된다. 사내 위키에 ADR 인덱스를 동기화하고 싶다면, 이 페이지를 마크다운 그대로 export하면 된다. 인덱스를 손으로 갱신하느라 시간을 쓰는 일이 사라진다.

### Dataview 쿼리 3 — TIL을 블로그 후보로 모으기

한국 개발자에게 블로그는 곧 포트폴리오다. 그런데 매주 글감을 짜내려고 하면 머리가 백지가 된다. 평소 쌓아둔 TIL이 글감의 보고인데, 흩어져 있어서 안 보일 뿐이다. Dataview로 한 줄에 모으자.

`이번 주 블로그 후보.md`:

````markdown
# 이번 주 블로그 글 후보

지난 7일에 만든 TIL 또는 permanent 중에서 블로그 한 편으로 펼칠 만한 것들.

```dataview
LIST
  "✦ " + file.link + " (" +
  (length(file.outlinks) + length(file.inlinks)) + "개 연결, " +
  length(file.tasks) + "개 후속 액션)"
FROM "10_Permanent" OR "20_Reference/TIL"
WHERE
  (type = "permanent" OR type = "til")
  AND file.ctime >= date(today) - dur(7 days)
  AND length(file.outlinks) + length(file.inlinks) >= 2
SORT length(file.outlinks) + length(file.inlinks) DESC
```
```

이 쿼리는 지난 7일 동안 만든 노트 중 연결이 2개 이상인 것들을 연결 수 내림차순으로 정렬한다. 연결이 많은 노트일수록 풀어 쓰면 한 편의 글이 될 가능성이 높다는 휴리스틱이다. 매주 일요일 저녁에 이 페이지를 한 번 열어보는 습관만 들이면 — 블로그 글감 고갈은 사실상 사라진다.

### 다섯 코드의 진짜 가치

여기까지 다섯 개 코드를 봤다. Templater 2개, Dataview 3개. 이 코드들의 진짜 가치는 "옵시디언이 무엇이 될 수 있는가"의 시범에 있다. 기본 옵시디언은 마크다운 노트 더미에 양방향 링크를 붙인 도구다. 두 플러그인이 추가되면, vault가 살아 있는 데이터베이스이자 자동화된 작업 환경이 된다. 매번 손으로 했던 일들 — 새 ADR 번호 부여, 인덱스 갱신, 고립 노트 찾기, 글감 발굴 — 이 자동으로 일어난다.

단, 한 가지 경고. **이 자동화에 빠져서 노트 자체를 안 쓰는 함정이 있다.** Tinkering Trap이라는 거다. 새 Dataview 쿼리를 한 시간 동안 다듬고 나면 뿌듯한데, 정작 그 시간에 atomic note 한 장을 더 쓰는 게 가치는 더 높다. 자동화는 손이 아플 때만, 정말 반복이 보일 때만 추가하자. 8장에서 이 함정도 다시 다룬다.

## 5.4 TIL과 Permanent 폴더 분리 — 한국 개발자 문화에 맞춰

한국 개발자 커뮤니티에는 TIL(Today I Learned) 문화가 깊이 뿌리내려 있다. GitHub에 `til` 레포를 만들고 매일 한 줄씩 적는 사람들, velog에 "오늘 배운 것" 시리즈를 올리는 사람들. 이게 좋은 습관이다. 학습한 것을 한 번 더 손으로 옮기면서 정리되는 효과가 있고, 시간이 지나면 그 자체가 학습 이력의 증거가 된다.

그런데 TIL과 permanent note를 한 폴더에 섞으면 두 가지가 다 망가진다. 폴더 분리를 권한다.

```
20_Reference/
  TIL/
    2026-05-12.md
    2026-05-13.md
    2026-05-14.md
  literature/
    ...

10_Permanent/
  postgres-mvcc는-트랜잭션-id로-행-가시성을-결정한다.md
  vacuum은-죽은-튜플을-회수한다.md
  ...
```

왜 분리해야 하는가? **TIL은 학습 기록이고, Permanent는 자기 주장이기 때문이다.** 두 층위가 다르다.

TIL은 "오늘 이걸 배웠다"의 시간 순 기록이다. 형식은 자유롭고, 다음 날 보면 어색해도 괜찮다. 학습의 흐름을 남기는 게 목적이지, 영구 보관이 목적이 아니다. 6개월 후의 본인이 그 TIL을 다시 안 봐도 무방하다.

Permanent는 "내가 이렇게 주장한다"의 영구 노트다. 시간이 지나도 갱신되며, 1년 후에도 다른 노트가 인용한다. 형식이 정형화돼야 하고, atomic이어야 하고, 제목이 안정적인 인터페이스여야 한다.

두 층위를 한 폴더에 섞으면 — TIL의 자유로움이 permanent의 정형성을 침범하거나, permanent의 부담이 TIL의 자유로움을 짓눌러서 매일 적는 습관이 무너진다. 폴더로 분리하면 둘이 각자 자기 모드로 살 수 있다.

흐름은 이렇게 잡는다. **TIL은 매일 적는다. 그 중 일부가 주간 리뷰에서 permanent로 승격된다.**

월요일 TIL: "Postgres에서 `EXPLAIN ANALYZE`의 BUFFERS 옵션이 캐시 히트 정보를 보여준다는 걸 알았다. 인덱스 효과 분석할 때 유용."

토요일 주간 리뷰: 이번 주 TIL을 한 번 훑어본다. "EXPLAIN ANALYZE BUFFERS"가 단순한 한 줄 학습이 아니라 "쿼리 성능 진단의 핵심 도구"라는 걸 깨닫는다. permanent로 승격한다 — `[[EXPLAIN ANALYZE의 BUFFERS는 인덱스 효율을 진단한다]]`. 본문에 자기 언어로 정리하고, 관련 atomic 노트(`[[Postgres 쿼리 플래너의 비용 모델]]`, `[[shared_buffers와 효과적 사용법]]`)와 링크 건다.

승격 비율은 보통 10~20% 정도다. 한 주에 TIL이 7개라면 그 중 1~2개가 permanent로 자란다. 나머지는 TIL 폴더에 남아 학습 이력으로 남는다. 둘 다 vault에 있고, 둘 다 가치가 있다 — 다만 다른 종류의 가치다.

## 5.5 회의록·일감 관리 — 송요창 패턴 응용

회의록을 vault에 두는 것이 합리적인가? 보통은 사내 위키나 Notion에 두지 않나? 합리적인지는 두 조건에 달렸다 — (1) 회의 결정과 연결되는 atomic 노트가 vault에 있고, (2) 회의록이 일감과 연결되어 추적되는가.

송요창의 Medium 글에서 본 패턴이 한국 개발자 문화에 잘 맞아서 약간 변형해서 쓰고 있다. 핵심은 이모지로 메타데이터를 표시하고 백링크로 일감을 추적하는 것이다.

회의록 템플릿:

```markdown
---
type: meeting
date: 2026-05-15
attendees: [tobylee, jane.kim, mark.lee]
tags: [#meeting, #team-platform]
---

# 2026-05-15 플랫폼 팀 위클리

## 안건
1. ADR-008 결제 DB 마이그레이션 검토
2. Q3 OKR 초안 공유
3. 신규 인증 모듈 설계 리뷰

## 논의

### 1. ADR-008 검토
[[ADR-008 결제 DB 마이그레이션]]
- 마이그레이션 RTO 90초 → 120초로 완화 (jane 의견)
- 결정: 다음 주 PoC 후 최종 결정
- 🏃 (in-progress) PoC 환경 구축 — @mark — 📅 2026-05-22

### 2. Q3 OKR
[[Q3 2026 OKR]]
- 핵심 목표: 결제 시스템 가용성 99.95%
- 🏃 OKR 문서 초안 작성 — @tobylee — 📅 2026-05-20

### 3. 인증 모듈
[[ADR-009 인증 모듈 — JWT vs Session]]
- 결정 보류: 보안팀과 추가 협의 필요
- 📅 다음 주 화요일 보안팀 합석
```

이모지 메타데이터의 의미를 약속해두면 된다.

- 🏃 (in-progress) — 진행 중인 액션
- 📅 (due) — 마감일
- ✅ (done) — 완료
- ❌ (blocked) — 막힘
- 🔥 (urgent) — 긴급
- @사람 — 담당자

이 회의록이 [[ADR-008]], [[Q3 2026 OKR]], [[ADR-009]] 같은 atomic 노트들과 백링크로 연결된다. 일주일 후 ADR-008을 열면 백링크 패널에 5월 15일 회의록이 자동으로 보인다. "이 결정에 대해 우리가 언제, 어떤 맥락에서 합의했는가"가 한 번에 추적된다.

일감 관리는 여기서 한 단계 더 갈 수 있다. Dataview로 "이번 주 내가 담당인 모든 액션"을 한 페이지에 모은다.

````markdown
# 이번 주 내 액션

```dataview
TASK
FROM "30_Daily" OR "20_Reference/Meetings"
WHERE
  contains(text, "@tobylee")
  AND !completed
  AND file.ctime >= date(today) - dur(14 days)
SORT file.ctime DESC
```
```

이 페이지를 데일리 노트의 상단에 embed해 두면 매일 아침 그날 해야 할 일이 자동으로 떠오른다. Jira나 Linear 같은 정식 일감 시스템을 대체하는 건 아니지만, "회의에서 떨어진 액션을 잊지 않고 처리하는" 정도까진 충분히 커버된다.

## 5.6 온콜·장애 회고 — 5 Whys를 atomic으로 분해한다

장애 회고는 정직성과 학습 가치가 함께 있는 자리다. 그런데 보통 회고 문서는 한 사건에 한 문서로 끝나서, 다음 사건에서 "지난번에 비슷한 문제 있었지?"를 떠올려도 그 문서를 통째로 다시 읽어야 한다. atomic으로 분해하면 다음 장애에서 즉시 인용 가능한 학습 단위가 된다.

5 Whys 루트 분석을 atomic으로 분해하는 패턴을 보자.

**원본 회고 (사내 위키 양식):**

```
2026-05-10 결제 시스템 장애 회고

증상: 14:32~15:18 결제 API 응답 지연 (p99 > 30초)
영향: 약 2,400건의 결제 실패, 매출 영향 추정 ~3,000만원
근본 원인 (5 Whys):
- Why 1: 결제 API가 DB 응답 대기로 타임아웃
- Why 2: DB connection pool 고갈
- Why 3: 한 long-running 쿼리가 100개 connection 점유
- Why 4: 캠페인 페이지가 결제 이력을 LEFT JOIN으로 조회
- Why 5: 캠페인 출시 전 쿼리 리뷰 누락 + 부하 테스트 미실시

조치:
- 단기: 캠페인 쿼리에 인덱스 추가 + statement_timeout 5초 적용
- 중기: 결제 이력 read replica 분리
- 장기: 캠페인 페이지의 결제 이력 노출 방식 재설계
```

이 회고를 vault에 그대로 둔다. 그리고 이 회고에서 atomic 노트 4~5개를 분해해 낸다.

```
[[캠페인 페이지의 LEFT JOIN은 long-running 쿼리를 유발한다]]
  - 우리 코드베이스에 비슷한 패턴이 있는지 점검 필요
  - 관련: [[N+1 vs LEFT JOIN의 trade-off]]

[[statement_timeout은 connection pool 고갈을 사후 차단한다]]
  - 모든 결제 관련 DB session에 5초 default 적용
  - 관련: [[connection pool 사이징 휴리스틱]]

[[부하 테스트 누락이 캠페인 장애의 빈번한 원인이다]]
  - 우리 사례: 2025-08, 2025-12, 2026-05 — 3회 반복
  - 관련: [[캠페인 출시 체크리스트]]

[[5 Whys는 4단계 이상이면 시스템 차원 결함을 가리킨다]]
  - 이번 사례에서 Why 5는 프로세스 결함 (코드 결함이 아닌)
```

이 atomic 노트들이 다음 장애 회고에서 인용된다. 다음 장애의 5 Whys 분석 중 "어, 이거 [[부하 테스트 누락이 캠페인 장애의 빈번한 원인이다]]랑 같은 거 아냐?"가 자연스럽게 떠오른다. 백링크 패널을 열면 "이 패턴이 과거에 어떤 회고들에서 나왔는지"가 한눈에 보인다. 같은 실수를 4번째로 반복하기 전에 멈출 수 있다.

이게 회사 차원의 학습 시스템이 된다. 단, 한 가지 — **회고 문서에 사람 비난이 들어가면 vault에 보관할 가치가 사라진다.** 회고는 시스템과 프로세스의 학습이지 사람 책임 추궁이 아니다. blameless postmortem 원칙을 지키고, atomic 노트도 그 톤으로 적는다.

## 5.7 오픈소스 기여 — 라이브러리 internals를 노트로 박제

오픈소스에 기여하기 위해 어떤 라이브러리의 internals를 파고든 경험이 있는가? 그 시간이 보통 어떻게 흐르는가? 한 주 동안 코드를 깊이 읽고, 이해하고, PR을 만들고, 머지된다. 그러면 — 그 한 주의 학습이 어디로 가는가? 대부분은 PR이 머지된 순간 머릿속에서 휘발된다. 6개월 후에 같은 라이브러리를 다시 만지면 처음부터 다시 읽어야 한다.

이걸 atomic 노트로 박제하면 다음 기여가 훨씬 빠르다.

예를 들어 한 주 동안 Python의 asyncio 라이브러리 내부를 읽었다고 해보자. 그러면 PR 작업 중에 다음 같은 atomic 노트가 자연스럽게 생긴다.

- `[[asyncio의 EventLoop는 selector 기반의 단일 스레드다]]`
- `[[asyncio.Future와 concurrent.futures.Future는 다른 클래스다]]`
- `[[asyncio.gather의 return_exceptions=False는 첫 예외에서 다른 task를 cancel한다]]`
- `[[asyncio.shield는 task cancel을 막지만 wait은 막지 않는다]]`

이 노트들이 PR 작업 동안 만들어진다. PR이 머지되면, 노트는 vault에 남는다. 6개월 후에 asyncio 관련 다른 이슈를 토론할 때, 이 노트들을 인용할 수 있다. "이 동작은 [[asyncio.shield는 task cancel을 막지만 wait은 막지 않는다]]에 정리해둔 것과 일치합니다" — 같은 코멘트로 토론에 참여할 수 있다.

내가 처음 이걸 의식적으로 시도한 게 한 라이브러리의 connection pool 부분을 읽을 때였다. 그때 atomic 노트 8장을 남겼는데, 1년 후에 회사 코드베이스에서 connection pool 관련 장애가 났을 때 그 8장이 그대로 인용 가능했다. 그 라이브러리를 다시 읽지 않고도 회고와 ADR을 빠르게 쓸 수 있었다. 그 한 주의 학습이 1년 후에 다시 살아난 거다.

오픈소스 기여 자체가 학습이지만, 그걸 atomic으로 박제하지 않으면 학습이 사고의 자산이 되지 않는다. 그냥 PR 한 건의 기록으로만 남는다. 그게 아쉽다.

## 5.8 회사 vault vs 개인 vault — 보안·프라이버시 (한국 IT 환경)

자, 이 장의 가장 어려운 절에 도착했다. 지금까지 다룬 모든 패턴이 멋져 보여도, 회사 보안 정책 앞에서 한 줄에 무너질 수 있다. 한국 IT 환경에는 외부 클라우드 사용 금지, MDM 강제, 외부 저장소 접근 모니터링 같은 정책이 흔하다. 특히 금융권, 공공기관, 일부 대기업 SI는 사실상 모든 외부 동기화가 차단된다. 이런 환경에서 옵시디언과 vault 워크플로우를 어떻게 운영할 수 있을까?

한 가지 원칙부터 시작하자. **회사 vault와 개인 vault는 명확히 분리한다.** 같은 옵시디언 앱에서 vault를 두 개 운영하면 된다(`Open another vault` 메뉴로 전환). 한 vault에 회사 자료와 개인 자료를 섞는 순간 보안과 프라이버시 양쪽이 다 위험해진다.

### 회사 자료를 vault에 적어도 되는 경계

판단 기준은 단순하다. **재현 가능한 일반 패턴은 OK, 식별 가능한 데이터·키는 NO.**

OK인 것:
- "캠페인 페이지의 LEFT JOIN이 long-running 쿼리를 유발한다" — 일반 패턴
- "JWT refresh token은 HttpOnly 쿠키에 저장한다" — 보안 모범 사례
- "Aurora MySQL의 read replica 사용 시 binlog 지연을 모니터해야 한다" — 도구 사용법
- "ADR-008 결제 DB 마이그레이션의 결정 근거" — 회사 결정이지만 기술적 본질만 적은 경우

NO인 것:
- 실제 고객 데이터, 거래 데이터, 사용자 ID
- API 키, 토큰, 비밀번호, 자격 증명
- 회사 내부 시스템 IP, 호스트명, 포트
- 미공개 매출, 손익, 사용자 수 같은 경영 정보
- 보안 취약점 — 회사 내부에 보고 → 패치 → 그 후에야 일반화된 형태로 적기

이 경계가 모호한 영역이 있다. 예를 들어 ADR에 "Aurora MySQL로 마이그레이션한다"는 결정을 적는 게 OK인가? 회사가 어떤 DB를 쓰는지가 기밀이라면 NO고, 일반적으로 공개해도 무방한 정보라면 OK다. 본인이 모호하다고 느끼면 NO 쪽으로 보수적으로 판단하자. 한 번 vault에 들어간 정보는 회수가 어렵다.

### GitHub Private 저장소가 "안전"한가

3장에서 권장한 GitHub Private + Obsidian Git 조합이 회사 vault에는 적합한가? 이게 회사 정책에 따라 갈린다.

**일반 IT 기업 (스타트업, 중견 IT, 대형 IT):** 보통 외부 GitHub Private 사용은 허용된다. 회사 정책에 명시된 게 없다면 IT/보안 부서에 한 번 확인하는 게 좋다. "개인 학습 노트를 GitHub Private에 보관해도 되나요"라고 단순한 질문으로 시작하자.

**금융권 (은행, 증권, 보험, 카드사):** 외부 Git 자체가 금지되는 경우가 많다. 금융보안원 가이드라인과 각 사 보안 정책에 따라 외부 Git 접근 자체가 막혀 있을 수 있다. 회사 PC에서 GitHub.com 접속 자체가 차단된 환경도 흔하다. 이런 곳에서는 회사 vault를 GitHub Private에 동기화하는 게 정책 위반이다.

**공공기관 협력사·국방 관련:** 보안 등급에 따라 외부 클라우드 일체 금지인 경우가 많다. 망 분리(internet 망과 업무 망 분리)가 적용된 환경이 대부분이라 외부 동기화 자체가 물리적으로 불가능하다.

**대기업 SI (삼성SDS, LG CNS, SK C&C 등):** 고객사에 따라 다르다. 본인이 파견 나간 고객사가 금융권이면 그 회사 정책을 따라야 한다.

회사 vault를 GitHub Private에 올렸다가 나중에 정책 위반으로 적발되면 — 단순한 견책으로 끝날 수도 있고 인사 조치가 따라올 수도 있다. 안전하게 가려면 IT/보안 부서에 사전에 한 번 묻자. "이런 형태의 노트 동기화가 정책에 부합하는지" 한 줄 메일이면 된다.

### 회사 vault의 로컬 전용 운영

외부 동기화가 안 되는 환경에서는 어떻게 vault를 운영할까? 몇 가지 옵션이 있다.

**(1) 회사 PC 단일 운영.** 가장 단순하다. 회사 PC에 옵시디언만 깔고 동기화 없이 운영한다. PC가 망가지면 자료가 다 날아간다는 위험이 있다. 회사가 사내 백업 시스템을 운영한다면 그 백업 폴더에 vault를 두면 OK.

**(2) 사내 NAS 또는 사내 Git.** 회사 내부에 NAS나 GitLab/Gitea 같은 사내 Git 서버가 있다면, 그쪽에 동기화한다. 회사 정책으로 봤을 때 사내 자원이라 외부 동기화 금지에 해당하지 않는다. NAS에 vault 폴더 두면 옵시디언이 그대로 읽고 쓴다.

**(3) iCloud Drive 회사 계정.** 회사가 Apple Business나 Google Workspace 회사 계정을 제공하고 그게 정책상 허용된 클라우드라면, 그 안에 vault를 둔다. 개인 iCloud나 개인 Google Drive와는 다르다. 회사 계정이 회사 IT 관리 하에 있고 정책상 허용된 클라우드라는 게 핵심이다.

**(4) 회사 PC + 개인 PC 이원 운영.** 회사 자료는 회사 PC에서만, 개인 학습은 개인 PC에서. 두 vault를 절대 섞지 않는다. 가장 보수적이지만 가장 안전하다. 한국 금융권·공공 환경에서는 사실상 이게 표준이다.

### 퇴사 시 vault 처리

퇴사할 때 vault를 어떻게 가져갈 것인가? 이게 단순한 데이터 이전 문제가 아니라 법적·윤리적 문제다.

원칙: **회사 자료는 두고 가고, 일반화된 학습 노트만 가져간다.**

회사 자료를 그대로 가져가는 건 보통 비밀유지의무(NDA) 위반이다. 입사 시 서명한 NDA의 범위 안에 들어간다. 회사 ADR, 회사 회의록, 회사 일감 — 이런 건 vault에 있더라도 퇴사 시 삭제하거나 회사에 인계해야 한다.

하지만 그 자료에서 학습한 일반 패턴 — `[[캠페인 페이지의 LEFT JOIN은 long-running 쿼리를 유발한다]]` 같은 atomic 노트 — 은 사고 자산이다. 이건 가져가도 무방하다(법적으로는 회사마다 다를 수 있으니 중요한 결정 전에는 확인). 단, 그 노트에 회사 시스템명·내부 정보가 박혀 있다면 다 지우고 가져간다.

이걸 자동화하려면 폴더 구조부터 분리한다.

```
work-vault/
  10_Permanent/         # 일반화된 atomic 노트 (퇴사 시 가져감)
  11_Company-Specific/  # 회사 시스템·결정·고객 정보 (퇴사 시 삭제)
  20_Reference/
    Meetings/           # 회사 회의록 (삭제)
    TIL/                # 학습 기록 (가져감)
  30_Daily/             # 데일리 노트 (개별 검토)
```

`11_Company-Specific/` 같은 폴더에 회사 종속 자료를 명시적으로 분리해 두면, 퇴사 시 처리가 자동화된다. 폴더 통째로 회사에 인계하거나 삭제하면 된다.

`30_Daily/`는 개별 검토가 필요하다. 보통 데일리 노트에는 회사 일과 개인 학습이 섞여 있다. 1년치 데일리 노트를 다시 읽으며 회사 정보만 지우는 건 현실적이지 않다. 그래서 처음부터 데일리 노트에는 회사 종속 정보를 적지 않는 습관이 좋다. 회사 일은 `11_Company-Specific/Daily/`에, 학습은 `30_Daily/`에. 이런 분리가 처음엔 번거롭지만 1년 후 퇴사 결정에서 빛을 본다.

### AI에 vault 노출 시 (NotebookLM·Claude Desktop)

6장에서 다룰 AI 통합 패턴 중 — vault를 NotebookLM에 업로드하거나 Claude Desktop이 MCP로 vault를 직접 읽게 하는 시나리오 — 가 있다. 이게 회사 vault와 만나면 새로운 보안 인터페이스가 발생한다.

**NotebookLM에 회사 vault 업로드:** 절대 NO. NotebookLM은 Google 서버에 데이터를 업로드한다. 회사 자료가 외부 클라우드에 올라가는 게 사실상 모든 보안 정책에 위반된다. 개인 vault는 OK, 회사 vault는 절대 NO.

**Claude Desktop + MCP로 회사 vault 접근:** Claude Desktop이 MCP로 vault 파일을 읽는다는 건, 그 내용이 Claude API로 전송된다는 뜻이다. 즉 Anthropic 서버에 회사 자료가 올라간다. 회사 정책이 외부 LLM API 사용을 허용한다면 OK, 금지하면 NO. 회사가 자체 LLM 인프라(예: 사내 호스팅된 LLaMA, 사내 Azure OpenAI)를 운영한다면 그쪽으로 라우팅하는 옵션을 검토하자.

**Claude Code + 회사 코드베이스:** Claude Code가 vault에서 코드 컨텍스트를 가져온다는 건, vault의 회사 정보가 Claude API로 전송된다는 뜻이다. Cursor·Copilot도 같은 이슈가 있다. 회사가 이런 도구 사용을 명시적으로 허용했는지 확인 필수.

원칙은 단순하다. **외부 LLM에 회사 자료가 어떻게든 전송될 수 있다면, 그 사용은 회사 IT/보안 부서의 명시적 허가가 필요하다.** 묵시적 허용이나 본인의 판단에 맡기지 말고 명시적으로 묻자.

### 한국 IT 보안 정책 13항목 자가 진단

본인 회사의 보안 환경이 어디쯤 있는지 한 번 점검해보자. 13개 항목에 ✅/❌ 체크하면서 본인 회사의 vault 운영 정책을 자기 손으로 결정한다.

**[A] 외부 동기화 가능성**
1. ☐ 회사 PC에서 GitHub.com 접속이 가능한가?
2. ☐ 회사 PC에서 GitHub Private 저장소 push/pull이 허용되는가?
3. ☐ 회사 PC에서 iCloud Drive·Google Drive·Dropbox 같은 외부 클라우드 동기화가 허용되는가?
4. ☐ 회사 정책에 "외부 저장소에 회사 자료 보관 금지" 같은 명시 조항이 있는가? (있으면 ❌)

**[B] 망 분리·접근 통제**
5. ☐ 인터넷 망과 업무 망이 분리되어 있는가? (분리되어 있으면 외부 동기화 사실상 불가)
6. ☐ MDM(모바일 기기 관리) 정책이 적용되어 있는가? (있으면 회사 PC 행위가 모니터링됨)
7. ☐ DLP(데이터 손실 방지) 솔루션이 깔려 있는가? (회사 키워드 포함 파일이 외부 전송 시 차단)

**[C] AI/LLM 도구 사용**
8. ☐ ChatGPT·Claude 같은 외부 LLM 사용이 명시적으로 허용되는가?
9. ☐ Cursor·Copilot 같은 AI 코딩 도구 사용이 허용되는가?
10. ☐ 회사가 자체 LLM 인프라를 제공하는가? (사내 호스팅 LLM이 있으면 그쪽으로 라우팅)

**[D] 개인 자료 분리**
11. ☐ 회사 PC에서 개인 학습용 vault를 별도로 운영할 수 있는가? (회사 자료와 분리하여)
12. ☐ 퇴사 시 개인 자료(학습 노트, 일반화된 atomic 노트)를 가져갈 수 있는 정책이 있는가?
13. ☐ 회사 vault와 개인 vault를 명확히 분리해 운영하고 있는가?

**판정 기준:**
- **9개 이상 ✅:** 일반 IT 기업 환경. GitHub Private 동기화, 외부 LLM 사용, 개인-회사 분리 vault 운영이 모두 가능. 이 책의 모든 패턴을 활용 가능.
- **5~8개 ✅:** 보안 강화 IT 환경. 외부 동기화는 가능하지만 회사 자료에 대한 보수적 운영 필요. 회사 vault는 일반 패턴만, 식별 정보는 절대 금지.
- **5개 미만 ✅:** 금융·공공·국방 같은 고보안 환경. 회사 vault는 로컬 전용 또는 사내 NAS 운영. 외부 LLM 사용 금지. 개인 학습은 개인 PC에서만. 옵시디언 자체는 깔 수 있어도 동기화·AI 통합은 거의 다 봉인된다.

본인 환경이 어느 칸에 있는지 보고, 이 장에서 다룬 패턴 중 어떤 걸 적용할지 결정하자. 5개 미만이라도 회사 PC 로컬에서 옵시디언으로 노트하는 것까진 보통 가능하다. 동기화와 AI 통합만 빠진다. 그것만으로도 가치가 충분하다 — 사고를 외장하는 것 자체가 목적이지, 클라우드 동기화가 목적이 아니다.

## 마무리

이 장이 길었다. 그만큼 개발자 일상의 부피가 컸기 때문이다. 코드 리뷰, ADR, TIL, 회의록, 일감, 회고, 오픈소스 기여 — 그리고 이 모두가 회사 보안 정책과 어떻게 공존할지. 한 장에 다 들어갔다.

다 흡수할 필요는 없다. 본인 일상에서 가장 가까운 한두 패턴부터 시작하자. PR 리뷰 자주 하면 §5.1, ADR 쓸 일 많으면 §5.2, 한국 개발자 문화에 맞춰 TIL 매일 쓰는 사람이면 §5.4부터. 한 패턴이 자리잡으면 다음 패턴이 자연스럽게 따라온다.

그리고 §5.8의 보안 13항목 체크리스트는 한 번은 자기 회사 환경에 적용해보자. 이게 막연한 두려움("회사가 노트를 보면 어쩌지?")을 구체적 판단("우리 회사는 9개 ✅니까 GitHub Private은 OK, 외부 LLM은 IT 부서 한 번 확인 필요")으로 바꿔 준다. 막연한 두려움이 가장 행동을 막는다. 구체적 판단이 행동을 만든다.

다음 장은 AI와의 분업이다. Claude·NotebookLM·Smart Connections·Claude Code 같은 도구들이 vault와 어떻게 만나야 사고가 죽지 않는지를 본다. 그 장은 5장의 §5.8을 전제로 깔고 간다 — 어떤 자료를 어떤 AI에 노출시켜도 되는지의 보안 인터페이스가 다음 장의 출발점이다.

당장 오늘 저녁에 할 한 가지를 골라보자. PR 리뷰하면서 fleeting 1개 적기, Templater 스니펫 1개 vault에 깔기, 또는 보안 13항목 체크리스트로 본인 회사 환경 점검하기. 한 가지면 충분하다. 5장 24페이지를 다 읽고 아무것도 안 하는 것보다, 한 가지를 시작하는 게 100배 가치 있다.
