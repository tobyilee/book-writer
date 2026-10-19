# 3장. 의도에서 명세까지 — `intent.md`와 `spec.md`

"설명란에는 대여섯줄 적어주고 땡이니, 그냥 이거 믿고 승인 해줘야 하나...?"

1장에서 병목이 옮겨 간 증거로 잠깐 꺼냈던 GeekNews 스레드의 한 줄이다. 같은 스레드에는 다른 각도의 댓글이 있다. 한 개발자는 리뷰어가 "왜 이렇게 했나?"라고 물으면 작성자가 AI에게 다시 물어 답을 붙여 넣는 구조를 꼬집었다 — 사람이 중개인 노릇만 한다는 것이다. 그리고 @tomskang은 이렇게 썼다. "어떤 flow 로 구현했는지, 다른 방법은 뭐가 있었고 왜 채택하지 않았는지, 왜 package.lock 이 바뀌어야 하는지. 전부 먼저 이야기해야하는것들 아닌가?"

이 댓글이 가리키는 것은 리뷰 속도가 아니다. 결정이 어디에 있느냐다. 그 PR을 만든 결정들 — 무엇이 문제였고, 어떤 결과를 원했고, 무엇은 건드리지 않기로 했고, 어떤 대안을 버렸는지 — 은 전부 어딘가에 있었다. 작성자와 Claude 사이의 대화 안에. 대화는 세션이 끝나면 사라지거나, 남아 있어도 리뷰어가 읽을 수 없는 곳에 있다. 리포에 남은 것은 diff와 대여섯 줄이다.

혼자 하는 프로젝트라면 이 문제가 없을까? 더 심하다. 석 달 뒤의 나는 그 세션을 열어 볼 수 없고, "왜 캐시를 60초로 했지?"라는 질문에 답할 사람이 없다. 그래서 다시 Claude에게 묻고, Claude는 코드만 보고 그럴듯한 이유를 지어낸다. 뒷맛이 찜찜한 장면이다. 코드를 치기 전에 두 파일을 써 두면 이 찜찜함은 사라진다. 코스의 플레이 1과 플레이 2가 그 두 파일이다.

### 플레이 1 — 의도를 `intent.md`로

코스 레슨 2의 "What changes" 표는 전통과 AI 네이티브를 이렇게 대비한다.

> "An idea passes through backlog entries, user stories, story points, and refinement meetings before anyone can act on it. Ownership transfers at each handoff, so what reaches engineering is several steps removed from what the originator meant." → "The originator brainstorms with Claude and writes the result down as `intent.md`, a proto-spec in the originator's own terms. The artifact contains what is wanted, why, and under which constraints."
>
> 아이디어는 백로그 항목, 유저 스토리, 스토리 포인트, 정제 회의를 거친 뒤에야 누군가 행동할 수 있다. 인수인계마다 소유권이 넘어가므로 엔지니어링에 도달한 것은 원래 제안자가 뜻한 것에서 몇 단계 떨어져 있다. → 제안자가 Claude와 브레인스토밍하고 결과를 자기 말로 쓴 프로토 스펙 `intent.md`에 적는다. 이 아티팩트는 무엇을 원하는지, 왜, 어떤 제약 아래서인지를 담는다. — 코스 레슨 2

개인에게 "인수인계마다 소유권이 넘어간다"는 말은 어떻게 번역될까? 인수인계 상대는 미래의 나와 Claude다. 머릿속의 의도가 프롬프트가 되고, 프롬프트가 대화가 되고, 대화가 코드가 되는 각 단계에서 조금씩 뜻이 빠진다. `intent.md`는 그 첫 단계에서 의도를 파일로 고정하는 장치다.

코스는 `intent.md`가 세 경로로 들어온다고 말한다. 사람이 아이디어를 떠올리거나, 티켓이 접수되거나, 알림으로 사고가 드러나거나. 세 번째 경로가 13장의 루프 복귀다. 어느 경로든 같은 다섯 단계를 거친다.

첫째, 제안자가 자기 말로 문제를 Claude에게 설명한다. 오늘 할 수 없는 것, 영향을 받는 사람, 더 나은 상태가 어떤 모습인지, 범위 밖은 무엇인지. 형식 언어는 필요 없다. 둘째, 아이디어가 구체해질 때까지 브레인스토밍한다. Claude는 분석가가 물을 질문을 던진다 — 범위, 사용자, 제약, 성공의 기준. 셋째, 결과를 조직의 템플릿으로 `intent.md`에 쓰게 한다. 코스는 이 템플릿을 스킬로 만들어 두라고 하고, 다섯 섹션을 제안한다: 문제, 제안하는 결과, 영향받는 사용자와 시스템, 제약, 미해결 질문. 넷째, 제안자가 Claude가 잘못 이해한 것을 고친다. 다섯째, 공유된 intent 홈에 커밋한다. 작성자와 타임스탬프가 기록에 합류하고, 제품 오너가 거기서 아이디어를 집어 든다.

관통 예제의 `intent.md`는 이렇다. 원문 그대로다.

```markdown
# Intent: claims status self-service
Author: J. Ortiz (claims operations). Status: draft.
## Problem
Customers phone the contact center to ask where their claim is.
Handlers spend roughly a third of call time on status-only queries.
## Proposed outcome
Customers see claim status, next step and expected date in the portal.
## Affected users and systems
Claims handlers, portal team, claims-core API.
## Constraints
No new PII in the portal session. Existing authentication only.
## Open questions
Do third-party loss adjusters need access too?
```

열세 줄이다. 작성자는 J. Ortiz, 클레임 운영 부서 사람이고 엔지니어가 아니다. 문제는 "고객이 클레임이 어디쯤 왔는지 묻느라 콜센터에 전화한다"이고, 근거로 "상담 시간의 대략 3분의 1이 상태 문의"라는 관찰이 붙어 있다. 원하는 결과는 포털에서 상태·다음 단계·예상 날짜를 보여 주는 것. 영향 범위에 `claims-core` API가 들어 있다 — 2장에서 본 초당 50 요청짜리 구형 시스템이다. 제약 두 줄이 이 체인에서 가장 오래 살아남는 문장이다. "포털 세션에 새 PII 없음. 기존 인증만." 이 두 줄은 `spec.md`의 제약 표로, 보안 스킬의 규칙으로, 훅의 검사로, 10장의 리뷰 발견으로 이어진다. 그리고 미해결 질문 하나 — 외부 손해사정인도 접근이 필요한가? 답을 모르면 모른다고 쓴다. 그 질문은 지워지지 않고 다음 파일로 넘어간다.

이 파일에 없는 것도 보자. 엔드포인트 이름이 없고, 캐시 전략이 없고, 어느 파일을 고칠지가 없다. 그것들은 다음 두 단계의 일이다. `intent.md`에 설계가 섞여 들어오기 시작하면 제안자의 말이 엔지니어의 말로 바뀌고, 그 순간 "원래 뭘 원했지?"가 다시 사라진다.

거버넌스는 간단하다. 코스의 말로 "증거는 커밋된 `intent.md`"다. 작성자, 타임스탬프, 전체 개정 이력이 intent 홈의 Git 이력에 남고, 제품 오너의 수락·거절은 머지 또는 리뷰 종료로 기록된다. 별도 승인 시스템이 없다. 커밋 자체가 증거다. 측정도 거기서 나온다. 첫 대화에서 커밋까지의 시간이 선행 지표(코스는 수 주짜리 요구사항 도출 주기가 몇 시간으로 줄기를 기대한다), 커밋된 intent 가운데 설계 단계로 넘어간 비율과 첫 `spec.md` 커밋 뒤에 `intent.md`가 고쳐진 횟수가 지연 지표다.

### 플레이 2 — 한 세션에서 요구사항과 설계

`intent.md`가 수락되면 다음은 명세다. 전통 SDLC에서 요구사항과 설계는 다른 팀이 맡는 다른 단계였다. 코스 레슨 3의 "What changes"는 그 분리를 이렇게 평한다.

> "Requirements and design are separate phases run by separate teams. Analysts formalize the idea into requirements, and designers then parse those back into a design. The separation exists for accountability, but it is slow and lossy." → "Both phases happen in a single prompted session. Claude takes `intent.md` and produces a requirements and design spec, constrained by the organization's skills, with areas of concern flagged."
>
> 요구사항과 설계는 별도 팀이 운영하는 별도 단계다. 분석가가 아이디어를 요구사항으로 형식화하고, 디자이너가 그것을 다시 설계로 해석한다. 분리는 책임 소재를 위해 존재하지만 느리고 손실이 크다. → 두 단계가 프롬프트 한 세션에서 일어난다. Claude가 `intent.md`를 받아 조직의 스킬을 제약으로 삼은 요구사항·설계 명세를 만들고, 우려 지점을 플래그한다. — 코스 레슨 3

여기서 중요한 역할 분담이 하나 있다. 코스는 "제품 오너는 그 명세를 리뷰하지만 쓰지는 않는다"고 말한다. 쓰는 것은 Claude다. 사람은 읽고, 고치고, 결정한다. 그리고 세션에는 조직의 스킬 — 브랜드, 보안, 컴플라이언스, UX 정책 — 이 로드되어 있어 명세가 그 정책들 안에서 쓰인다. 개인에게 이 스킬 묶음은 2장 번역 표대로 자기 프로젝트의 제약 스킬 한두 개, 없으면 CLAUDE.md의 Conventions 절이다.

#### 프롬프트의 마지막 문장

프롬프트는 길지 않다. 코스가 실제로 쓴 프롬프트 원문이다.

```text
Read the attached intent.md and produce a requirements and design spec for integrating it into our existing codebase. Apply the skills available to you so the plan conforms to our brand guidelines, security policies and UX standards. Document the spec fully as spec.md, ready to hand to the engineering team. Describe clearly any areas of concern, especially where you cannot satisfy contradicting policies.
```

마지막 문장을 기억해두자. "우려 지점을 분명히 기술하라, 특히 서로 충돌하는 정책을 만족시킬 수 없는 곳을." 이 한 문장이 플레이 2의 핵심이다. 모델은 기본적으로 질문하기보다 바로 만들기로 기울어 있다(뒤에서 근거를 본다). 충돌을 발견하면 조용히 한쪽을 골라 매끈한 문서를 내놓는다. 이 문장은 그 매끈함을 금지하고, 충돌을 사람 앞에 꺼내 놓게 한다.

결과물이 관통 예제의 `spec.md`다. 원문 그대로 싣는다.

```markdown
# Spec: claims status self-service
From: intent.md (J. Ortiz, claims operations). Status: ready for product owner review.
Skills applied: secure-api-review, brand-voice, portal-ux.

## Requirements
- R1. A signed-in customer sees status, next step and expected date for each open claim.
- R2. Status is one of four states: received, in review, approved, paid.
- R3. The response carries those three fields and nothing else.
- R4. What the customer sees is at most 60 seconds old.

## Design
- New endpoint GET /claims/{id}/status in claims-api, behind the gateway JWT.
- claims-api reads the claim from claims-core. The portal never calls claims-core.
- New StatusPanel on the portal claims page. It caches each answer for 60 seconds.

## How each constraint in the intent is met
| Constraint | Met by |
| :---- | :---- |
| No new PII in the portal session | R3. None of the three fields is tagged pii in the schema. |
| Existing authentication only | The gateway JWT. No new login, token or role. |

## Open questions from the intent
- Do third-party loss adjusters need access too? Not answered. Carried forward as concern 1.

## Areas of concern
1. Loss adjusters have no portal account. Giving them access breaks "existing
   authentication only", so they are left out of this spec. Owner: security.
2. The portal-ux skill says every status shows a date. The brand-voice skill says
   never to state a payment date as a commitment. I cannot satisfy both as written.
   Proposed label: "Estimated date". Owner: compliance.
3. claims-core allows 50 requests a second. The 60-second cache should keep the
   portal under that, but nobody has load tested it. Owner: claims-core team.
```

#### `spec.md`를 위에서부터 읽기

머리에 출처(`intent.md`, J. Ortiz)와 적용된 스킬 세 개가 적혀 있다. 어떤 정책 버전 아래에서 이 명세가 쓰였는지가 파일 자체에 남는다.

요구사항은 넷이고 번호가 붙어 있다. 코스는 이유를 한 문장으로 말한다. "The requirements are numbered so the plan and the review can cite them." — 플랜과 리뷰가 인용할 수 있게 번호를 붙인다. 4장의 `plan.md`는 작업 순서마다 "R1", "R3"을 적고, 10장의 `REVIEW.md` 컴플라이언스 패스는 diff가 그 번호를 지켰는지 본다. 번호가 없으면 "요구사항을 지켰나"가 산문 대 산문의 흐릿한 대조가 된다. 번호가 있으면 R3을 지켰나, 깼나로 답이 갈린다.

R3을 눌러 보자. "응답은 그 세 필드만 담고 다른 것은 담지 않는다." 이 줄은 `intent.md`의 "새 PII 없음"이 요구사항으로 번역된 결과다. 아래 제약 표가 그 연결을 명시한다 — 세 필드 가운데 스키마에서 `pii`로 태그된 것은 없다. R4의 "최대 60초"는 설계의 "60초 캐시"와 짝이고, 그 60초는 다시 `claims-core`의 50 rps 제한에서 나왔다.

설계는 세 줄이다. 엔드포인트, 데이터 경로("포털은 절대 `claims-core`를 직접 부르지 않는다"), 프런트엔드 컴포넌트. 어느 파일을 고칠지는 여기에도 없다.

미해결 질문은 지워지지 않았다. "답하지 못함. 우려 1로 이월." 그리고 우려 지점 셋. 1번은 손해사정인 — 접근을 주면 "기존 인증만"이 깨지므로 이 명세에서는 제외하고, 결정은 보안 소유자에게 넘긴다. 2번이 이 파일에서 가장 흥미로운 줄이다. UX 스킬은 모든 상태에 날짜를 보이라 하고, 브랜드 스킬은 지급 날짜를 약속처럼 말하지 말라 한다. Claude는 "두 가지를 쓰인 대로 동시에 만족시킬 수 없다"고 쓰고 "예상 날짜"라는 라벨을 제안한 뒤 결정을 컴플라이언스에 넘겼다. 프롬프트의 마지막 문장이 바로 이 줄을 만들어 냈다. 3번은 50 rps 제한과 60초 캐시 — "아무도 부하 테스트를 하지 않았다"는 정직한 고백이고, 4장의 플랜이 이것을 위험 항목으로 받는다.

코스의 거버넌스 문단은 이 구조의 가치를 "정책 충돌이 몇 주 뒤 리뷰에서 발견되는 대신, 명세가 쓰이는 동안 살아 있는 정책이 읽히고 적용된다"로 요약한다. 명세, 그것을 만든 프롬프트, 그때 유효했던 스킬 버전이 전부 버전 관리에 남는다. 측정은 두 타임스탬프다. 같은 변경 건의 `intent.md` 커밋과 `spec.md` 커밋 사이의 시간이 선행 지표, 빌드가 시작된 뒤 — 첫 `plan.md` 커밋 뒤 — 에 `spec.md`가 다시 고쳐진 횟수가 지연 지표다. 요구사항 재작업을 git log가 직접 세어 준다.

### 현행 사양 — 템플릿은 스킬로, 인터뷰는 프롬프트로

코스가 가리키기만 한 공식 문서를 Claude Code 2.1.303 / 2026-10 기준으로 채워 보자.

코스는 `intent.md` 템플릿을 "기술 팀원이 설정하고 리드가 승인한 스킬"로, 플레이 2의 프롬프트를 "조직 수준 슬래시 커맨드"로 만들라고 한다. 현행 문서에서 둘은 같은 것이다. 커스텀 커맨드는 스킬로 통합되었고(자세한 사정은 6장), 새로 만드는 것은 `SKILL.md`로 쓰기를 권한다. 개인 스킬은 `~/.claude/skills/<name>/SKILL.md`, 프로젝트 스킬은 `.claude/skills/<name>/SKILL.md`다. 공식 Skills 문서가 스킬을 만들 시점을 이렇게 정의한다. "같은 지시, 체크리스트, 다단계 절차를 채팅에 계속 붙여 넣고 있을 때, 또는 CLAUDE.md의 한 절이 사실이 아니라 절차로 자라났을 때." intent 템플릿은 정확히 그 경우다.

한 가지 비용을 기억해두자. 공식 문서는 "스킬이 로드되면 그 내용은 턴을 넘어 컨텍스트에 남으므로, 모든 줄이 반복되는 토큰 비용"이라고 쓰고, `SKILL.md`를 500줄 아래로 유지하라고 한다. intent 템플릿 스킬은 다섯 섹션의 제목과 각 섹션에 무엇을 쓰는지 한두 줄이면 충분하다. 길이가 템플릿을 좋게 만들지는 않는다.

개인에게는 공식 Best practices 문서의 인터뷰 패턴이 플레이 1·2를 한 번에 압축한 형태다. 문서가 제안하는 프롬프트의 골격은 이렇다.

> "I want to build [brief description]. Interview me in detail using the AskUserQuestion tool. ... Keep interviewing until we've covered everything, then write a complete spec to SPEC.md."
>
> [간단한 설명]을 만들고 싶다. AskUserQuestion 도구를 써서 나를 자세히 인터뷰하라. ... 모든 것을 다 다뤘다고 판단될 때까지 인터뷰를 계속한 뒤, 완전한 명세를 SPEC.md에 쓰라. — Claude Code 공식 Best practices

코스의 2단계("Claude가 분석가가 물을 질문을 던진다")를 도구 호출로 명시한 것이다. 같은 문서는 두 가지를 덧붙인다. "명세가 완성되면 새 세션을 열어 실행하라" — 그리고 "가장 유용한 명세는 자기 완결적이다. 관련 파일과 인터페이스를 이름 붙이고, 범위 밖을 말하고, 기능이 동작함을 증명하는 종단간 검증 단계로 끝난다." 관통 예제의 `spec.md`가 R1~R4와 설계 세 줄로 한 것이 그것이다.

Anthropic의 컨텍스트 엔지니어링 글(2025-09)은 이런 파일을 "구조화된 노트 작성"이라고 부른다. 컨텍스트는 한계 효용이 줄어드는 유한한 자원이니, 결론을 파일에 적고 새 컨텍스트가 그 파일을 읽게 하라는 것이다.

머지를 트리거로 쓰는 자동화 — intent가 머지되면 비대화형 잡이 스킬을 로드한 채 명세 패스를 돌려 `spec.md`를 PR로 올리는 것 — 는 코스의 2단계가 말하는 끝 상태다. 현행 사양에서는 GitHub Actions의 automation mode가 그 자리다. 워크플로가 `prompt` 입력을 주면 Claude는 멘션을 기다리지 않고 실행하고, 헤드리스 문서에 따르면 프롬프트 문자열에 `/skill-name`을 넣으면 실행 전에 스킬로 확장된다. 함정 하나. `--bare` 플래그는 CLAUDE.md·스킬·훅을 건너뛴다. 재현성이 필요한 eval(9장)에서는 장점이지만, 스킬을 제약으로 삼아야 하는 이 잡에서는 명세가 정책 없이 쓰이게 되니 넣지 말자. 배관 전체는 12장에서 다룬다. 소규모 팀은 수동 스킬 호출에서 멈춰도 충분하다.

### 왜 이 플레이인가 — 모호함은 좋은 모델을 더 세게 때린다

코드를 치기 전에 두 파일을 쓰는 것이 번거롭게 느껴질 수 있다. "프롬프트를 좀 더 길게 쓰면 되지 않나?" 그 생각부터 짚어 보자.

Yang 외(ASE 2026, 심사 통과)는 네 가지 유형의 모호함을 심은 함수 수준 과제 1,304개로 여러 LLM을 평가했다. 결과는 두 줄로 요약된다. 모호함은 평가한 모든 모델의 성능을 일관되게 떨어뜨렸고, 그 부정적 효과는 "가장 발전한 모델에서 가장 두드러졌다." 또 모델들은 같은 모호한 요구에 대해 "기능적으로 서로 다른 구현을 자주 만들어 냈고, 그 모호함을 스스로 식별하거나 해소하는 능력이 부족했다." 더 좋은 모델이 모호한 명세에 더 크게 당한다는 것은 직관에 어긋난다. 그런데 생각해 보면 그럴 법하다. 좋은 모델은 빈칸을 더 그럴듯하게 채운다. 그럴듯하게 채워진 빈칸은 사람 눈에 띄지 않는다.

이 연구의 두 번째 발견이 개인에게 바로 쓸 수 있는 진단법을 준다. 같은 요구로 여러 번 생성해 결과가 서로 다르면 그 요구는 모호하다. Mu 외의 ClarifyGPT(2023, arXiv 프리프린트 — 아직 심사 전인 연구)가 이 직관을 그대로 방법으로 만들었다. 모호함이 감지되면 명확화 질문을 던지게 했더니 GPT-4의 MBPP-sanitized Pass@1이 70.96%에서 80.80%로 올랐다. 숫자는 그 시점의 모델 것이지만 방향은 분명하다. 좋은 질문 한 번이 긴 프롬프트보다 낫다. Wu 외(2025, 프리프린트)는 기본 모델이 "질문하기"보다 "바로 생성"으로 치우쳐 있음을 보였다 — 플레이 2의 프롬프트가 "충돌을 기술하라"고 굳이 명령하는 이유다.

보안은 더 날카롭다. Grynets 외의 Specification-Driven Development Benchmark(2026, arXiv 프리프린트 — 아직 심사 전인 연구)는 숨긴 221개 블랙박스 API 테스트로 생성 코드를 평가했다. 보안 요구를 따로 명시하지 않은 기준선에서 주요 실패가 50건, ASVS를 넣으면 42건, 다층 보안 모델을 넣으면 36건이었다. 한 줄로 줄이면 — 스펙에 쓰지 않은 보안 요구는 생성되지 않는다. `spec.md`의 "No new PII" 제약 표와 보안 스킬이 왜 따로 있어야 하는지, 그리고 10장의 리뷰에 왜 보안 패스가 또 있어야 하는지가 여기서 나온다.

그러니 "프롬프트를 길게"라는 대안은 어떨까? 길이는 모호함을 줄이지 않는다. 구조가 줄인다. 다섯 섹션은 "제약"과 "미해결 질문" 칸을 비워 둔 채로 보여 주고, 번호 붙은 요구사항은 "다른 것은 담지 않는다"처럼 범위를 닫는 문장을 쓰게 만든다. 긴 프롬프트는 그 빈칸을 숨긴다.

이제 반론을 들어 보자. 2025년 11월 Hacker News에서 "Spec-Driven Development: The Waterfall Strikes Back"이라는 글이 수백 개의 댓글을 모았다. 한쪽은 단호하다. "나는 전문적으로 워터폴 개발을 했고, SDD는 정확히 워터폴이다." 명세가 "이해관계자의 머릿속에서 불변의 것으로 석회화된다"는 경험담도 있다. 다른 쪽은 반박한다. "워터폴은 이터레이션이 한 번이라는 뜻이다." 8시간 단위로 명세를 고치며 돈다는 사람은 "명세를 쓴다고 덜 애자일해진 적이 없다"고 했다. 그리고 한 고백 — "우리는 문제조차 잘 이해하지 못하는데 해법을 어떻게 명세하나."

코스의 답은 어느 쪽일까? 명세를 돌에 새기지 않는다는 것이다. 플레이 2의 측정 지표 자체가 "빌드 시작 뒤 `spec.md`가 고쳐진 횟수"다 — 고쳐질 것을 전제한다. 4장의 플랜 모드는 구현이 플랜에서 벗어나면 "같은 커밋에서 `plan.md`를 갱신하라"고 하고, 훅으로 동기화를 강제하는 것까지 고려한다. 명세는 한 번 쓰고 잊는 문서가 아니라 코드와 같은 커밋에서 함께 움직이는 파일이다.

재미있는 것은 한국 커뮤니티가 이 답을 스스로 찾아냈다는 점이다. 2026년 초 GeekNews에서 "2년간의 바이브코딩을 끝내고 다시 손으로 코드를 쓰기 시작했다"는 글이 올라왔을 때, 댓글은 명세로 모였다. 한 사람은 "명세깎는데 공들이는게 필요하죠"라며 추적성 관리를 말했고, 다른 사람은 "명세를 업데이트 하세요"라고 썼다. 그리고 @cosine20: "훅을 걸어서 구현이 완료되면 명세를 업데이트 할 수도 있고, 그게 아니어도 수동으로 명세 업데이트하는 command나 skill을 추가하면 되는데." intent→spec→훅. 코스를 읽지 않은 사람들이 같은 그림을 그렸다. 그만큼 자연스러운 흐름이라는 뜻으로 읽고 싶다.

마지막으로 Pinna 외(MSR 2026, 심사 통과)의 관찰 하나. 에이전트 PR의 수락률을 가르는 가장 큰 변수는 과제 유형이었다 — 문서 작업은 82.1%, 새 기능은 66.1%로, 도구 사이의 차이보다 컸다. `intent.md`를 쓸 때 "영향받는 사용자와 시스템" 칸이 길어진다면, 그 변경은 영향 반경(blast radius)이 크다는 신호다. 첫 intent는 그 칸이 짧은 것으로 고르는 편이 낫다.

### 내 리포로 옮기기

조직의 플레이 1·2를 자기 리포로 가져오면 이렇게 된다.

`[개인 즉시]` — 리포 루트에 `intent/` 폴더를 만든다. 코스도 단일 제품에는 리포 안 폴더가 가장 단순한 intent 홈이라고 말한다. 변경 건마다 하위 폴더 하나, 그 안에 `intent.md`와 `spec.md`. 템플릿은 `~/.claude/skills/intent/SKILL.md`로 — 다섯 섹션 제목과 각 섹션의 한 줄 설명, 그리고 "답을 모르는 질문은 Open questions에 남겨라"는 지시 하나. 명세용 제약 스킬은 한두 개면 된다(API 응답 규약, 개인정보 처리 규칙). 없으면 CLAUDE.md의 Conventions 절이 대역이니 억지로 만들지 말자. 프롬프트는 코스 원문 그대로, 마지막 문장은 빼지 않는다. `spec.md`가 끝나면 세션을 닫고 새 세션에서 구현에 들어간다. 제품 오너는 미래의 나이므로, `intent.md`는 쓴 날 커밋하지 말고 다음 날 다시 읽고 커밋하자.

`[팀 합의]` — PR 설명란의 템플릿을 intent의 다섯 섹션으로 바꾼다. 문제, 제안하는 결과, 영향받는 사용자와 시스템, 제약, 미해결 질문. 이 장을 열었던 "설명란에 대여섯 줄"에 대한 가장 싼 답이고, `.github/PULL_REQUEST_TEMPLATE.md` 한 파일이면 된다. intent가 머지되면 `spec.md` PR을 자동으로 올리는 Actions 잡은 가능하지만, API 비용과 `--bare` 함정이 있으니 팀이 수동 스킬 호출에 익숙해진 뒤에 결정하자.

`[조직 결정]` — 코스가 전제하는 것들이 있다. 엔지니어가 아닌 사람의 Claude 접근, Git을 모르는 제안자를 대신해 커밋해 주는 GitHub 커넥터, 여러 리포에 걸친 전용 intent 리포, Claude Design 목업에서 코드로 내보내는 흐름, 우려 지점을 정책 소유자에게 라우팅하는 체계. 이 층이 있다는 것만 알아 두자. 대체 경로는 위 두 묶음이고, 그것으로 체인은 끊기지 않는다.

측정은 두 타임스탬프다. `intent/` 폴더의 커밋 이력에서 `intent.md`와 `spec.md`의 커밋 시각 차이를 읽는다 — 아이디어가 명세가 되는 데 걸린 시간이다. 그리고 첫 `plan.md` 커밋 뒤에 `spec.md`가 고쳐진 횟수를 센다. 이 수가 크면 명세가 모호했다는 신호이고, 0이면 명세를 고치지 않고 코드만 고쳤다는 뜻일 수도 있으니 두 쪽을 다 의심하자.

코스는 플레이 2의 마지막 단계를 이렇게 적었다. 제품 오너가 명세와 intent를 빌드로 넘길지 결정하고, "명세를 수락하는 것이 빌드 단계의 플랜 모드 플레이를 시작한다." 이제 `intent/` 폴더에 두 파일이 있다. 다음에 할 일은 그 둘을 들고 세션을 여는 것이다.

`intent.md`는 미래의 나에게 보내는 첫 커밋이고, `spec.md`는 그 편지에 Claude가 쓴 답장이다.
