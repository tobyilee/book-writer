# 4장. main을 지키는 약속을 코드로 적다 — 보호 규칙, 룰셋, CODEOWNERS, 머지 방식

브랜치 보호는 흔히 누군가를 막는 장치로 여겨진다. 신입이 실수로 `main`에 force push하지 못하게, 급한 선배가 리뷰 없이 머지하지 못하게 채우는 자물쇠 말이다. 그래서 보호 규칙을 켜자고 하면 "우리 팀은 서로 믿는데 굳이?"라는 반응이 돌아오기도 한다.

하지만 보호 규칙은 사실 팀이 합의한 흐름을 실행 가능한 형태로 적어 둔 문서에 가깝다. 2장과 3장에서 우리는 브랜치 전략을 골랐다. "`main`에는 PR로만 들어간다", "머지하려면 한 명 이상 승인해야 한다", "CI가 초록이어야 한다" 같은 약속도 함께 정했을 것이다. 이 약속을 위키 페이지에 적어 두면 어떻게 될까? 바쁜 금요일 오후에는 아무도 위키를 열지 않는다. 같은 약속을 저장소 설정에 적어 두면 다르다. 약속을 어기는 머지 버튼이 아예 눌리지 않는다.

이렇게 보면 보호 규칙을 켜는 일은 불신의 표현이 아니다. 우리가 무엇에 합의했는지를 모두가 볼 수 있는 곳에, 모두에게 똑같이 적용되는 형태로 남기는 일이다. 1장에서 워크플로를 전략으로 다루자고 했다. 전략이 문서로만 남아 있으면 금세 다시 습관으로 돌아간다. 이제 그 전략을 코드로 적는 법을 살펴보자.

## 보호 규칙이라는 메뉴판

GitHub의 브랜치 보호 규칙(branch protection rule)은 특정 브랜치 이름 패턴에 조건을 거는 기능이다. 2026년 9월 기준 GitHub Docs에 나오는 설정 항목은 다음과 같다.

| 설정 항목 | 무엇을 강제하는가 |
|---|---|
| Require pull request reviews before merging | 머지 전 리뷰 승인 필요 |
| Require status checks before merging | 지정한 CI 체크가 통과해야 머지 가능 |
| Require conversation resolution before merging | 리뷰 대화가 모두 해결돼야 머지 가능 |
| Require signed commits | 서명된 커밋만 허용 |
| Require linear history | 머지 커밋 push 금지 |
| Require merge queue | 머지 큐를 거쳐야 머지 가능 |
| Require deployments to succeed before merging | 지정한 배포 환경에 배포 성공 후 머지 |
| Lock branch | 브랜치를 읽기 전용으로 |
| Do not allow bypassing the above settings | 관리자도 위 규칙 적용 |
| Restrict who can push to matching branches | push 가능한 사람 제한 |
| Allow force pushes / Allow deletions | force push·삭제 허용 여부 |

메뉴판이 길다. 전부 켜고 싶은 유혹이 들지만, 항목마다 대가가 있으니 하나씩 이유를 따져 볼 필요가 있다.

리뷰 필수는 거의 모든 팀에 권할 만하다. 여기에 붙은 옵션 하나가 특히 중요하다. Docs의 설명을 보자. "Optionally, you can choose to dismiss stale pull request approvals when commits are pushed that affect the diff in the pull request." 승인을 받은 뒤에 변경을 더 push하면 기존 승인을 무효로 돌리는 옵션이다. 이 옵션이 꺼져 있으면 어떻게 될까? 오탈자 수정으로 승인을 받아 놓고, 그 뒤에 결제 로직을 통째로 바꿔 push해도 승인이 그대로 살아 있다. 리뷰어가 본 코드와 머지되는 코드가 달라지는 셈이다. 1장의 두 번째 축, 검증한 것을 머지하고 있느냐는 질문이 사람의 리뷰에서도 똑같이 등장한다.

대화 해결 필수는 리뷰 코멘트가 흐지부지 묻히는 것을 막는다. "나중에 고칠게요"라는 답만 달고 머지되는 PR이 많은 팀이라면 효과가 크다.

선형 이력 필수도 흥미롭다. Docs는 이렇게 설명한다. "Enforcing a linear commit history prevents collaborators from pushing merge commits to the branch." 이 옵션을 켜면 머지 커밋 방식은 쓸 수 없고, 스쿼시나 리베이스로만 들어올 수 있다. 머지 방식에 대한 팀의 선택을 강제하는 스위치인 셈이다. 머지 방식은 이 장 뒷부분에서 따로 살펴본다.

마지막으로 관리자 포함 여부다. "You can enable this setting to apply the restrictions to admins and roles with the 'bypass branch protections' permission, too." 이것을 켜지 않으면 관리자는 모든 규칙을 건너뛸 수 있다. 그리고 규칙을 건너뛰는 일은 대개 가장 급하고 가장 위험한 순간, 즉 장애 대응 중에 일어난다. 급할수록 검증을 건너뛰고 싶어지지만, 급할 때 들어간 검증 안 된 코드가 두 번째 장애를 부른다. 관리자까지 규칙에 포함하고, 정말 규칙을 풀어야 한다면 그 사실이 기록에 남게 하는 편이 낫다.

## strict와 loose — 머지 레이스를 막는 값

1장에서 잠깐 언급한 필수 체크는 이 메뉴판에서 가장 중요한 항목이다. CI가 돈다는 것과, CI가 통과해야만 머지할 수 있다는 것은 전혀 다른 이야기다. 체크를 필수로 지정하지 않으면 빨간 체크가 떠 있어도 머지 버튼은 눌린다.

필수 체크에는 두 가지 모드가 있다. Docs는 이렇게 구분한다. strict 모드는 "Require branches to be up to date before merging" 체크박스가 켜진 상태로, "The branch **must** be up to date with the base branch before merging." loose 모드는 그 체크박스가 꺼진 상태로, "The branch **does not** have to be up to date with the base branch before merging."

1장의 장면을 떠올려 보자. 두 번째 PR은 오전의 `main`을 기준으로 초록이었고, 그 상태로 오후의 `main`에 머지됐다. 이것이 loose 모드에서 일어나는 일이다. strict 모드였다면 어떻게 됐을까? 첫 번째 PR이 머지되는 순간 두 번째 PR은 "최신이 아님" 상태가 된다. 머지하려면 `main`을 받아서 체크를 다시 돌려야 하고, 그 과정에서 사라진 함수 이름 때문에 빌드가 실패한다. 머지 레이스는 `main`에 닿기 전에 PR 안에서 잡힌다.

그렇다면 항상 strict를 켜면 되지 않을까? 여기서 대가가 등장한다. strict 모드에서는 누군가 머지할 때마다 열려 있는 모든 PR이 낡은 상태가 된다. 각 작성자는 `main`을 따라잡고, CI를 처음부터 다시 돌리고, 그 사이 또 누가 머지하면 다시 따라잡아야 한다. PR이 하루에 몇 개인 팀에서는 문제 되지 않는다. 하지만 하루에 수십 개씩 머지되는 저장소라면, 개발자들은 "업데이트 버튼 누르고 CI 기다리기"를 반복하느라 오후를 다 쓴다. 게다가 CI가 20분씩 걸린다면? 번거로움을 넘어 머지 자체가 병목이 된다.

loose는 빠르지만 머지 레이스에 문을 열어 두고, strict는 안전하지만 트래픽이 늘수록 줄서기 비용이 커진다. 이 딜레마를 푸는 것이 1장에서 잠깐 소개한 머지 큐다. 머지 큐는 strict 모드의 따라잡기와 재검사를 사람 대신 큐가 차례로 처리한다. 이 이야기는 12장과 13장에서 이어진다. 지금은 팀 규모와 PR 트래픽을 보고 둘 중 하나를 의도적으로 고르자. 기본값을 그대로 두고 무엇이 켜져 있는지 모르는 상태가 가장 위험하다.

## 룰셋 — 겹쳐 쓰는 규칙

보호 규칙은 오래된 기능이다. GitHub는 2023년에 그 다음 단계로 룰셋(ruleset)을 내놓았다. 2023년 4월 17일 public beta, 7월 24일 GA였고, 체인지로그는 룰셋을 브랜치 보호의 다음 진화로 소개했다. Docs의 정의는 이렇다. "A ruleset is a named list of rules that applies to a repository or to multiple repositories in an organization for customers on GitHub Team and GitHub Enterprise plans." 이름이 붙은 규칙 묶음이고, 저장소 하나에도, 조직 안의 여러 저장소에도 걸 수 있다. 정의에 붙은 플랜 조건은 조직 단위 룰셋에 걸리는 말이다. 저장소 룰셋은 Free 플랜에서는 공개 저장소에만, Pro·Team·Enterprise Cloud에서는 비공개 저장소에도 쓸 수 있다(2026년 9월 GitHub Docs 기준). 플랜 조건은 바뀔 수 있으니 자기 플랜에서 무엇이 되는지 먼저 확인하자.

보호 규칙과 무엇이 다를까? 가장 큰 차이는 겹칠 수 있다는 점이다. "Multiple rulesets can apply to the same branch at the same time, while only one branch protection rule applies." 보호 규칙은 한 브랜치에 하나만 적용되지만, 룰셋은 여러 개가 동시에 걸린다. 조직 전체에 "모든 저장소의 `main`은 리뷰 1명 필수"라는 룰셋을 걸고, 결제 저장소에는 "서명된 커밋 필수" 룰셋을 하나 더 거는 식이다.

두 룰셋이 같은 규칙을 다르게 정하는 경우도 있다. 한쪽은 리뷰 1명, 다른 쪽은 2명을 요구하는 식이다. 답은 분명하다. "If the same rule is defined in different ways across the aggregated rulesets, the most restrictive version of the rule applies." 가장 엄격한 쪽이 이긴다. 그러니 조직 룰셋은 모두가 지킬 최소 기준으로, 저장소 룰셋은 그 위에 얹는 추가 기준으로 설계하면 된다.

운영 측면의 장점도 있다. 룰셋은 지우지 않고 켜고 끌 수 있다. "You can change a ruleset's enforcement status without deleting the ruleset." 장애 대응 중에 규칙을 잠시 풀어야 한다면, 규칙을 지웠다가 기억에 의존해 다시 만드는 대신 상태만 바꾸면 된다. 또 "Anyone with read access to a repository can view its active rulesets." 저장소를 읽을 수 있는 사람은 누구나 지금 어떤 규칙이 걸려 있는지 볼 수 있다. 약속을 모두가 볼 수 있는 곳에 적어 두자는 이 장의 생각과 잘 맞는다.

적용 전에 시험해 보는 방법도 있다. GA 체인지로그는 규칙을 강제하기 전에 시험하는 평가 모드(evaluation mode)를 소개하는데, 발표 당시 기준으로 Enterprise Cloud 전용이었다. 다른 플랜이라면 먼저 작은 저장소에 걸어 보고 넓히는 편이 현실적이다. 한도도 알아 두자. 저장소당 75개, 조직 전체 룰셋도 75개까지다(2026년 9월 기준). 이런 수치는 바뀔 수 있으니 Docs를 함께 확인하는 편이 좋다.

2026년 2월 17일에는 룰셋에 required reviewer rule이 GA로 추가됐다. 파일 경로 패턴별로 지정한 팀의 승인을 몇 개 이상 받아야 머지할 수 있게 하는 규칙이다. 경로 패턴에 `!`로 제외를 표현할 수 있다는 점이 눈에 띈다. 예를 들어 "`infra/` 아래는 플랫폼 팀 승인 필수, 단 `infra/docs/`는 제외" 같은 규칙을 쓸 수 있다. 그렇다면 이제 CODEOWNERS는 필요 없을까? GitHub는 선을 분명히 그었다. "CODEOWNERS files remain the best way to manage ownership, support individuals as reviewers, and request reviews even when not required." 강제는 룰셋이, 소유권 표시와 리뷰 요청은 CODEOWNERS가 맡는 식으로 역할을 나누면 된다.

## CODEOWNERS — 누가 봐야 하는가

CODEOWNERS는 "이 경로의 코드는 누가 책임지는가"를 적는 파일이다. 파일을 두면 해당 경로를 건드리는 PR에 코드 오너가 자동으로 리뷰어로 요청된다. 리뷰 필수 설정에서 코드 오너의 리뷰를 요구하도록 켜면, 오너의 승인이 머지 조건이 된다.

파일 위치는 세 곳 중 하나다. "create a new file called `CODEOWNERS` in the `.github/`, root, or `docs/` directory of the repository." GitHub는 이 순서로 찾아서 처음 발견한 파일을 쓴다. 한 저장소에 여러 개를 두면 헷갈리니 하나만, 되도록 `.github/`에 두자.

```text
# .github/CODEOWNERS
*                    @acme/backend
/web/                @acme/frontend
/payments/           @acme/payments
/payments/docs/      @acme/tech-writers
/.github/workflows/  @acme/platform
```

이 파일을 읽을 때 기억할 규칙이 하나 있다. "Order is important; the last matching pattern takes the most precedence." 위에서 아래로 읽다가 마지막으로 일치한 줄이 이긴다. 위 예에서 `/payments/docs/guide.md`는 `*`, `/payments/`, `/payments/docs/`에 모두 일치하지만, 마지막 줄인 `@acme/tech-writers`가 오너가 된다. 그래서 넓은 패턴을 위에, 좁은 패턴을 아래에 두는 게 기본 모양이다. 순서를 거꾸로 쓰면 `*`가 맨 아래에서 모든 규칙을 덮어 버리는 난감한 일이 생긴다.

쓸 수 없는 문법도 있다. Docs는 `!`로 패턴을 제외하는 것, `[ ]`로 문자 범위를 지정하는 것, `\`로 `#`을 이스케이프하는 것을 지원하지 않는다고 적어 둔다. 앞에서 본 required reviewer rule이 `!` 제외를 지원한다는 점과 대비된다. 제외 규칙이 필요하다면 룰셋 쪽이 맞는 도구다. 그 밖에 파일 크기는 3MB 미만이어야 하고, 코드 오너는 저장소 쓰기 권한이 있어야 한다.

마지막으로 자주 놓치는 규칙이다. 한 경로에 오너가 여럿일 때다. "an approval from *any* of the owners is sufficient to meet this requirement." 오너 중 아무나 한 명만 승인해도 요건이 충족된다. `/payments/ @alice @bob`이라고 적어도 둘 중 한 명의 승인이면 충분하다. 둘 다의 승인이 꼭 필요하다면 CODEOWNERS만으로는 부족하고, 룰셋의 required reviewer rule이나 승인 인원 설정과 조합해야 한다.

예시의 마지막 줄 `/.github/workflows/`에도 이유가 있다. 워크플로 파일은 CI가 어떤 권한으로 무엇을 실행할지 정한다. 이 경로를 누구나 고칠 수 있다면 보호 규칙의 필수 체크 자체를 우회하는 PR이 가능해진다. 그래서 GitHub의 보안 가이드도 이 디렉터리를 코드 오너 목록에 넣으라고 권한다. 왜 이것이 공격 표면이 되는지는 11장에서 자세히 다룬다.

## 머지 커밋, 스쿼시, 리베이스 — 이력에 무엇을 남길까

보호 규칙을 모두 통과한 PR은 이제 머지된다. 그런데 어떤 방식으로? GitHub는 세 가지를 제공한다. 머지 커밋(Create a merge commit), 스쿼시 머지(Squash and merge), 리베이스 머지(Rebase and merge)다. 저장소 설정에서 허용할 방식을 고를 수 있다.

| 방식 | GitHub Docs의 설명 | `main`에 남는 것 |
|---|---|---|
| 머지 커밋 | "All commits from the feature branch are added to the base branch in a merge commit. The pull request is merged using the `--no-ff` option." | 브랜치의 모든 커밋 + 머지 커밋 |
| 스쿼시 머지 | "The pull request's commits are squashed into a single commit." | PR당 커밋 하나 |
| 리베이스 머지 | "All commits from the topic branch (or head branch) are added onto the base branch individually without a merge commit." | 브랜치의 커밋들이 한 줄로 |

머지 커밋의 `--no-ff`에는 2장에서 본 Git Flow의 동기가 그대로 담겨 있다. 기능 브랜치가 존재했다는 사실과, 어떤 커밋들이 하나의 기능을 이뤘는지를 이력에 남기겠다는 것이다. 대신 이력은 갈래가 많은 그래프가 된다.

리베이스 머지에는 알아 둘 함정이 있다. 로컬에서 `git rebase`를 하는 것과 GitHub의 리베이스 머지는 같지 않다. Docs에 따르면 GitHub의 리베이스 머지는 "Always updates the committer information and creates new commit SHAs"이고, "The commits in the head branch are added to the base branch without commit signature verification." 항상 새 SHA가 만들어지니 PR 브랜치에서 본 커밋 해시와 `main`의 커밋 해시가 달라진다. 서명 검증도 거치지 않는다. 커밋 서명을 중요하게 여기는 팀이라면 놓치기 쉬운 부분이다.

어느 방식이 옳을까? 개발자 커뮤니티에서 이 논쟁은 끝나지 않는다. 한쪽은 커밋 하나하나에 이야기를 담자고 말한다. Hacker News의 한 개발자는 스쿼시를 싫어하는 이유를 이렇게 썼다. "I wrote it as several separate commits for a _reason_: documenting each step, making each step revertible, separating refactors from semantic changes." 반대쪽은 PR이 곧 작업 단위라고 본다. "PR is the atomic level of work. I'd argue PR-level history (i.e. squash) is often enough and is way cleaner." 스쿼시를 하면 `main`의 커밋 하나가 PR 하나와 대응해서 PR 단위로 되돌리기는 쉽지만, 그 안의 일부만 체리픽하기는 어려워진다는 지적도 있다. 결국 한 개발자의 말처럼 "The real answer to this whole debate is 'it depends'"다.

무엇에 달려 있을까? 세 가지 질문으로 정리할 수 있다. 첫째, 팀원들이 PR 안의 커밋을 하나하나 다듬는가? 커밋마다 의미 있는 메시지와 독립적인 변경을 담는 문화라면 리베이스 머지가 그 노력을 살린다. 대부분의 커밋이 "fix", "리뷰 반영" 같은 중간 기록이라면 스쿼시가 이력을 깨끗하게 지킨다. 둘째, 되돌리기는 어떤 단위로 하는가? PR 단위로 되돌리는 일이 많다면 스쿼시가 편하다. 셋째, 브랜치의 존재 자체를 기록해야 하는가? Git Flow처럼 릴리스 브랜치를 합치는 흐름이라면 머지 커밋이 자연스럽다.

한 가지 방식만 고집할 필요도 없다. 커뮤니티에서도 "Why not use squash & merge when appropriate and rebase & merge otherwise?"라는 절충안이 나온다. 다만 PR마다 작성자가 기분대로 고르게 두면 이력이 뒤죽박죽이 된다. 팀 합의로 기본 방식을 정하고, 설정에서 허용 방식을 그에 맞게 좁혀 두자.

머지 방식의 영향은 이력의 모양에서 끝나지 않는다. 5장에서 볼 스택 PR은 스쿼시와 부딪히는 지점이 있고, 12장에서는 스쿼시 방식의 머지 그룹에서만 발생한 머지 큐 사고를 만난다. 머지 방식이 도구 버그에 노출되는 범위까지 바꿀 수 있다는 이야기다.

## 두 가지 설정 예시

지금까지 본 항목을 묶어 두 팀의 설정을 그려 보자. 하나는 다섯 명이 웹 서비스를 연속 배포하는 팀, 다른 하나는 금융처럼 감사와 규제를 받는 팀이다.

| 항목 | 소규모 웹 팀 (5명) | 규제 있는 팀 |
|---|---|---|
| 적용 수단 | 저장소 보호 규칙 또는 룰셋 하나 | 조직 룰셋(최소 기준) + 저장소 룰셋(추가 기준) |
| 리뷰 승인 | 1명 | 2명 + 코드 오너 승인 |
| 경로별 승인 | CODEOWNERS로 리뷰 요청만 | required reviewer rule로 결제·인프라 경로에 담당 팀 승인 강제 |
| stale 승인 무효화 | 켬 | 켬 |
| 대화 해결 필수 | 켬 | 켬 |
| 필수 체크 | lint·단위 테스트·빌드, strict 켬 | 같은 체크 + 보안 검사, strict 또는 머지 큐 |
| 서명된 커밋 | 선택 | 켬 (리베이스 머지의 서명 검증 누락 주의) |
| 선형 이력 | 켬 (스쿼시만 허용) | 팀 합의에 따라 |
| 관리자 포함 | 켬 | 켬 |
| force push·삭제 | 금지 | 금지 |

소규모 팀의 설정에서 핵심은 가벼움이다. 리뷰 한 명과 빠른 필수 체크, 그리고 스쿼시로 통일한 이력이면 충분하다. PR 트래픽이 적으니 strict 모드의 따라잡기 비용도 크지 않다. 규제 있는 팀은 누가 무엇을 승인했는지를 나중에 증명할 수 있어야 한다. 그래서 조직 룰셋으로 모든 저장소에 최소 기준을 강제하고, 민감한 경로에는 담당 팀의 승인을 규칙으로 못 박는다. 두 설정 모두 관리자 포함을 켠 것은 우연이 아니다. 규칙은 모두에게 똑같이 적용될 때 약속이 된다.

## 지금 설정 화면을 열어 보자

이 장을 덮기 전에 자기 저장소의 설정 화면을 직접 열어 보자. 다섯 가지만 확인하면 된다.

첫째, `main`에 보호 규칙이나 룰셋이 실제로 걸려 있는가? 그리고 관리자도 예외 없이 적용되는가?

둘째, CI 체크가 "돌기만" 하는가, "필수"로 지정돼 있는가? 필수라면 strict와 loose 중 무엇인지, 그리고 그 선택을 의도해서 했는지 확인하자.

셋째, 승인 후 새 커밋이 올라오면 기존 승인이 무효가 되는가?

넷째, CODEOWNERS 파일이 있는가? 있다면 넓은 패턴이 위에, 좁은 패턴이 아래에 있는가? `.github/workflows/`에 오너가 지정돼 있는가?

다섯째, 저장소에서 허용한 머지 방식이 팀이 합의한 방식과 같은가?

다섯 개 중 몇 개에 바로 답할 수 있었는가? 답하지 못한 항목이 있다면, 그 항목이 지금 팀의 약속이 문서에만 남아 있는 곳이다.

## 이 장의 핵심

- 브랜치 보호 규칙과 룰셋은 팀이 합의한 흐름을 누구나 볼 수 있고 누구에게나 똑같이 적용되는 형태로 적어 둔 문서다. 관리자까지 포함해야 약속이 된다.
- 필수 체크의 strict 모드는 머지 레이스를 PR 안에서 잡아내지만, PR 트래픽이 늘수록 따라잡기와 재검사 비용이 커진다. 이 비용이 머지 큐의 동기다.
- 룰셋은 여러 개가 겹쳐 적용되고 가장 엄격한 규칙이 이긴다. 조직 룰셋은 최소 기준, 저장소 룰셋은 추가 기준으로 설계한다.
- CODEOWNERS는 마지막으로 일치한 패턴이 이기고, 오너 중 한 명의 승인으로 충족된다. 강제와 제외 패턴은 룰셋의 required reviewer rule이 맡는다.
- 머지 방식은 커밋을 다듬는 문화, 되돌리기 단위, 브랜치 이력 보존 필요에 따라 고르고, 저장소 설정으로 허용 방식을 좁혀 둔다.
