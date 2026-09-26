<!-- fact-check 메모(저술가): 집필 규율대로 이 장의 예제는 `@<full-commit-sha> # v{N}` 자리표시 형식을 쓴다. 주석의 메이저 버전(checkout v5, upload/download-artifact v4)은 레퍼런스 근거가 없는 저술가 추정값이므로 2026-09 기준으로 대조·교체 필요. 레퍼런스 밖 문법·동작(Dependabot `package-ecosystem: github-actions` 설정, `download-artifact`의 `run-id`/`github-token` 입력과 `actions: read` 권한, GITHUB_TOKEN이 잡 종료 시 만료된다는 점, 2025-12-08 이전 `pull_request_target`이 PR base 브랜치의 워크플로를 썼다는 설명)도 Docs 대조 대상. -->

# 11장. YAML 한 줄이 공격 표면이다 — GitHub Actions 보안

2025년 3월 14일. 여느 금요일처럼 PR이 올라오고, CI가 돈다. 체크는 초록이다. 누구도 워크플로 파일을 고치지 않았다. `uses: tj-actions/changed-files@v45`라는 한 줄은 어제와 글자 하나 다르지 않다.

그런데 그 한 줄이 가리키는 코드는 어제와 다르다. PR에서 바뀐 파일 목록을 뽑아 주던 이 인기 액션의 버전 태그들이 한꺼번에 다른 커밋을 가리키기 시작했다. v1부터 v45.0.7까지, 사람들이 "버전"이라고 믿고 적어 둔 태그 거의 전부다. 새로 가리키게 된 커밋은 파일 목록을 뽑는 대신 러너가 쥐고 있던 시크릿을 빌드 로그에 찍어 냈다. 공개 저장소의 빌드 로그는 누구나 읽을 수 있다. 수만 개 저장소가 이 액션을 쓰고 있었다.

아찔한 것은 이 모든 일이 아무 경보 없이 일어났다는 점이다. 워크플로는 성공했고, 테스트도 통과했다. 겉으로는 평소와 똑같은 하루였다.

## 그 주말에 무슨 일이 있었나

사건을 차분히 재구성해 보자. 먼저 공식 기관이 확인한 사실부터다. 미국 사이버보안·인프라보안청(CISA)은 2025년 3월 18일 경보를 냈고, GitHub Advisory는 이 취약점에 CVE-2025-30066을 붙였다. 확인된 내용은 이렇다.

- 2025년 3월 14일부터 15일 사이, 공격자가 `tj-actions/changed-files`의 v1부터 v45.0.7까지 태그를 악성 커밋으로 재지정했다.
- 악성 코드는 워크플로 로그를 통해 시크릿을 노출했다. Advisory의 제목이 요약하는 그대로다. "tj-actions changed-files through 45.0.7 allows remote attackers to discover secrets by reading actions logs."
- 영향받은 저장소는 2만 3천 개 이상으로 추정됐다(보안업체 추정치).
- 문제는 v46.0.1에서 해소됐다.
- CISA 경보는 `reviewdog/action-setup`의 침해를 같은 경보에서 함께 다뤘다.

여기서부터는 보도와 커뮤니티 분석의 영역이다. 공격의 발단은 이 저장소에 쓰기 권한을 가진 봇 계정의 개인 액세스 토큰(PAT)이 탈취된 것이었고, `reviewdog` 쪽 침해가 연쇄의 앞 단계였다는 분석이 나왔다. 국내 보도에서는 시크릿이 실제로 노출된 것으로 확인된 저장소를 최소 218개로 집계하기도 했다(사실 확인 필요). 악성 커밋이 만들어진 날짜를 3월 12일로 보는 분석도 있다. 이런 세부는 출처마다 조금씩 다르니, 이 책에서는 앞의 확정 사실 위에서만 교훈을 끌어내자.

사건 당일 Hacker News에는 이런 반응들이 올라왔다(커뮤니티 의견).

> "many people mistakenly assume that git tags are immutable"
>
> "People don't pin versions. Referencing a tag is not pinning a version, those can be updated"

두 번째 문장이 이 사건의 핵심을 찌른다. 우리는 `@v45`라고 적으면서 버전을 고정했다고 믿었다. 실제로는 "이 저장소 주인이 v45라고 부르기로 한 것이 무엇이든 그것을 실행하겠다"고 적은 것이었다.

## 태그는 약속일 뿐이다 — SHA 고정

왜 이렇게 쉽게 번졌을까? 세 가지가 겹쳤다.

첫째, Git 태그는 움직일 수 있다. 태그는 특정 커밋을 가리키는 이름표일 뿐이라, 저장소에 쓰기 권한이 있는 사람은 이름표를 다른 커밋에 옮겨 붙일 수 있다. 보통은 메인테이너가 `v4`를 최신 `v4.x`로 옮기는 편의 기능으로 쓰지만, 권한을 훔친 공격자도 똑같이 할 수 있다.

둘째, 서드파티 액션은 우리 잡 안에서, 우리 권한으로 돈다. 8장에서 스텝끼리는 같은 러너를 공유한다고 했다. 같은 잡에 시크릿을 쓰는 스텝이 있다면, 같은 잡의 다른 스텝도 그 러너 위에 있다. 파일 목록을 뽑는 작은 액션 하나가 배포 키와 한 방을 쓰고 있었던 셈이다.

셋째, 공개 저장소의 로그는 공개다. 시크릿을 외부 서버로 빼돌릴 필요도 없었다. 로그에 찍기만 하면 누구나 읽을 수 있었다.

그렇다면 첫 번째 고리를 어떻게 끊을까? GitHub의 Actions 보안 문서는 분명하게 답한다.

> "Pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release."

커밋 SHA는 커밋 내용에서 계산된 값이라, 같은 SHA가 다른 내용을 가리키게 만들려면 공격자가 SHA-1 충돌을 만들어 내야 한다. 문서의 표현으로는 "as they would need to generate a SHA-1 collision for a valid Git object payload." 실제로 tj-actions 사건에서 SHA로 고정해 둔 사용자는 영향을 받지 않았다. 태그가 어디로 옮겨지든, 그들의 워크플로는 원래의 커밋을 실행했다.

SHA로 고정하면 이렇게 된다.

```yaml
    steps:
      - uses: actions/checkout@<full-commit-sha> # v5
      - uses: some-org/some-action@<full-commit-sha> # v2.3.1
```

`<full-commit-sha>` 자리에는 40자리 커밋 해시 전체가 들어간다. 짧은 해시는 쓰지 않는다. 뒤에 주석으로 사람이 읽을 버전을 적어 두는 것이 관례다. 해시만 보고는 이것이 어느 버전인지 알 수 없기 때문이다.

물론 번거롭다. 액션이 업데이트될 때마다 해시를 찾아 바꿔야 한다면 아무도 오래 지키지 못한다. 그래서 SHA 고정은 자동 갱신과 짝을 이룬다. Dependabot이나 Renovate가 새 버전의 SHA로 갱신하는 PR을 올려 주게 하는 조합이 흔히 권장된다.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

이렇게 하면 해시 변경이 PR로 들어온다. 업데이트가 저장소 몰래 일어나는 것이 아니라, 리뷰와 CI를 거쳐 머지되는 변경이 된다. 태그 참조에서는 누군가 태그를 옮기는 순간 우리 CI가 바뀌었다. SHA 참조에서는 우리가 PR을 머지해야만 바뀐다. 통제권이 우리 쪽으로 돌아온다.

조직 차원의 장치도 생겼다. GitHub는 2025년 8월 15일 허용 액션 정책에 "full SHA로 고정한 액션만 허용"하는 옵션을 추가했다. 이 옵션을 켜면 SHA로 고정하지 않은 액션을 쓰는 워크플로는 실패한다. 같은 업데이트에서 `!owner/action` 형태로 특정 액션을 차단하는 기능도 들어왔다. tj-actions 사건에 대한 대응이다. 2025년 10월 28일에는 immutable releases가 정식 출시됐다. 이 기능을 켠 릴리스는 자산을 추가·수정·삭제할 수 없고, 태그를 삭제하거나 옮길 수 없으며, 서명된 증명(attestation)이 함께 발급된다. 다만 이 보호는 액션을 배포하는 쪽이 켜야 작동한다. 액션 생태계 전체에 이 불변성이 어떻게 적용되는지는 2026년 9월 기준으로 확인하지 못했으니 공식 문서를 함께 보자(사실 확인 필요). 소비자가 스스로 쥘 수 있는 통제는 여전히 SHA 고정이다.

## 토큰은 필요한 만큼만

두 번째 고리는 권한이다. 8장에서 `permissions`를 파일에 적는 습관을 권했다. 이제 그 이유를 제대로 볼 차례다. GitHub 보안 문서는 이렇게 권한다.

> "It's good security practice to set the default permission for the `GITHUB_TOKEN` to read access only for repository contents. The permissions can then be increased, as required, for individual jobs within the workflow file."

이 권고가 왜 필요한지는 숫자가 말해 준다. Koishybayev와 동료들은 2022년 USENIX Security에서 저장소 213,854개의 워크플로 447,238개를 분석해 이렇게 보고했다. "99.8% of workflows are overprivileged and have read-write access (instead of read-only) to the repository." 같은 연구에서 저장소의 99.7%가 외부 액션을 실행했고, 97%는 검증되지 않은 제작자의 액션을 하나 이상 썼으며, 18%는 보안 업데이트가 빠진 액션을 실행하고 있었다.

다만 이 99.8%를 지금의 비율로 읽으면 안 된다. 연구 데이터는 GitHub가 2023년 2월 2일 기본 권한을 바꾸기 전의 것이다. 그날부터 새로 만드는 엔터프라이즈, 조직, 개인 저장소의 `GITHUB_TOKEN` 기본 권한은 읽기 전용이 됐다. 그런데 기존 조직과 저장소의 설정은 바뀌지 않았다. 2023년 2월 이전에 만든 조직이라면, 지금도 모든 워크플로가 기본으로 쓰기 권한 토큰을 들고 돌고 있을 수 있다. 오늘 할 수 있는 가장 싼 보안 점검은 조직 설정에서 워크플로 기본 권한이 무엇으로 되어 있는지 확인하는 일이다.

설정을 바꾸는 것과 별개로, 워크플로 파일 자체에 권한을 적어 두자.

```yaml
permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<full-commit-sha> # v5
      - run: make test

  release:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@<full-commit-sha> # v5
      - run: make release
```

테스트 잡은 읽기만 하고, 릴리스를 만드는 잡만 쓰기 권한을 받는다. 서드파티 액션이 침해되더라도 그 액션이 도는 잡의 토큰이 읽기 전용이라면, 공격자가 그 토큰으로 할 수 있는 일은 저장소를 읽는 데 그친다.

여기서 구분할 것이 하나 있다. `GITHUB_TOKEN`은 워크플로마다 새로 발급되고 잡이 끝나면 만료되는 짧은 토큰이다(사실 확인 필요). 정말 위험한 것은 우리가 저장소 시크릿에 넣어 둔 오래 사는 비밀들, 즉 개인 액세스 토큰, 클라우드 접근 키, 배포 키다. tj-actions 사건에서 로그로 새어 나간 것도 이런 시크릿이었다. 토큰 권한을 줄이는 일과 오래 사는 시크릿 자체를 줄이는 일은 함께 가야 한다. 10장의 OIDC가 그 두 번째 일이다.

사건의 발단으로 지목된 것이 봇 계정의 개인 액세스 토큰이었다는 분석도 곱씹어 볼 만하다. 사실이라면 공격자가 태그를 옮길 수 있었던 것은 누군가의 자동화가 저장소 쓰기 권한을 가진 오래 사는 토큰을 들고 있었기 때문이다. 이 교훈은 액션을 쓰는 쪽보다 만드는 쪽에 더 무겁다. 우리 팀이 사내외에 공유하는 액션이나 10장의 공용 워크플로 저장소를 운영한다면, 그 저장소에 쓰기 권한을 가진 토큰이 어디에 몇 개나 있는지부터 세어 보자. 편의를 위해 만들어 둔 토큰 하나가 그 액션을 쓰는 모든 저장소의 뒷문이 될 수 있다.

## pwn request — pull_request_target의 함정

세 번째 고리는 트리거다. 8장에서 이름만 소개하고 넘어간 `pull_request_target`을 이제 열어 볼 차례다.

외부 기여를 받는 오픈소스 저장소를 운영한다고 해보자. fork에서 온 PR에 "테스트 커버리지 요약"을 코멘트로 달아 주고 싶다. 그런데 8장에서 봤듯 fork PR의 `pull_request` 워크플로는 읽기 전용 토큰으로 돌아 코멘트를 달 수 없다. 그때 눈에 들어오는 것이 `pull_request_target`이다. 이 트리거는 fork PR에서도 대상 저장소의 권한으로 돈다. GitHub Security Lab의 2021년 글은 그 성질을 이렇게 적는다.

> "Workflows triggered via `pull_request_target` have write permission to the target repository. They also have access to target repository secrets."

여기에 PR의 코드를 체크아웃해 빌드하는 스텝을 더하면 어떻게 될까?

```yaml
# 위험한 패턴 — 이렇게 쓰지 말자
name: Coverage comment
on: pull_request_target
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<full-commit-sha> # v5
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: npm ci && npm test
```

이 워크플로는 쓰기 토큰과 시크릿을 쥔 채로, 아무나 올릴 수 있는 PR의 코드를 실행한다. 공격자는 테스트 코드를 고칠 필요도 없다. Security Lab의 설명대로 "They may submit malicious changes to the existing build scripts like `make` or `powershell` files or redefine the build script in the `package.json` file." `npm test`가 부르는 스크립트 하나만 바꾸면 된다. 이런 공격을 "pwn request"라고 부른다. Security Lab의 결론은 단호하다. "Combining `pull_request_target` workflow trigger with an explicit checkout of an untrusted PR is a dangerous practice that may lead to repository compromise." Koishybayev의 연구에서 `pull_request_target`을 쓰는 저장소는 7,485개(3.5%)였다. 드문 트리거지만, 쓰는 곳에서는 치명적이다.

그렇다면 fork PR에 코멘트를 달고 싶은 요구는 포기해야 할까? 안전한 패턴이 있다. 신뢰할 수 없는 코드를 실행하는 일과 쓰기 권한이 필요한 일을 두 워크플로로 나누는 것이다. 첫 워크플로는 권한 없는 `pull_request`로 PR 코드를 빌드하고 테스트한 뒤, 결과를 아티팩트로 남기고 끝난다. 두 번째 워크플로가 `workflow_run`으로 이어받아 결과를 읽고 코멘트를 단다. Security Lab이 권하는 구조 그대로다.

```yaml
# .github/workflows/pr-build.yml — 신뢰할 수 없는 코드를 권한 없이 실행
name: PR Build
on:
  pull_request:
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<full-commit-sha> # v5
      - run: npm ci && npm run coverage:summary
      - env:
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: echo "$PR_NUMBER" > coverage/pr-number.txt
      - uses: actions/upload-artifact@<full-commit-sha> # v4
        with:
          name: coverage
          path: coverage/
```

```yaml
# .github/workflows/pr-comment.yml — 결과만 읽고 쓰기 작업을 한다
name: PR Comment
on:
  workflow_run:
    workflows: [PR Build]
    types: [completed]
permissions:
  contents: read
  actions: read
  pull-requests: write
jobs:
  comment:
    if: github.event.workflow_run.conclusion == 'success'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@<full-commit-sha> # v4
        with:
          name: coverage
          run-id: ${{ github.event.workflow_run.id }}
          github-token: ${{ github.token }}
      - name: 커버리지 요약을 코멘트로 남기기
        env:
          GH_TOKEN: ${{ github.token }}
          REPO: ${{ github.repository }}
        run: |
          pr="$(cat pr-number.txt)"
          case "$pr" in
            ''|*[!0-9]*) echo "PR 번호 형식이 아니다"; exit 1 ;;
          esac
          gh pr comment "$pr" --repo "$REPO" --body-file summary.md
```

두 번째 워크플로는 PR의 코드를 체크아웃하지도, 실행하지도 않는다. 아티팩트로 받은 파일은 공격자가 조작했을 수 있는 데이터로 다룬다. 그래서 PR 번호가 숫자인지 확인하고, 요약 파일은 실행하지 않고 코멘트 본문으로만 쓴다. 8장에서 `workflow_run`이 시크릿과 쓰기 토큰을 가진다고 했던 성질이 여기서는 정확히 필요한 곳에만 쓰인다.

`pull_request_target`에는 최근 달라진 점도 있다. GitHub는 2025년 11월 7일 공지하고 12월 8일부터 동작을 바꿨다. "The workflow file and checkout commit will always be taken from the repository's default branch, regardless of the pull request's base branch." `GITHUB_REF`는 기본 브랜치를, `GITHUB_SHA`는 그 브랜치의 최신 커밋을 가리킨다. 이전에는 PR의 base 브랜치에 있는 워크플로가 쓰였기 때문에(사실 확인 필요), 기본 브랜치에서는 이미 고친 취약한 워크플로가 오래된 릴리스 브랜치에 남아 공격 통로가 되곤 했다. GitHub의 설명대로 "Historically, this behavior has led to the exploitation of outdated workflows that contained vulnerabilities in pull_request_target workflows that were presumed to be remediated since they were fixed in the default branch." 2021년 Security Lab 글을 포함해 2025년 12월 이전 자료는 이전 동작을 기준으로 설명하고 있으니 읽을 때 주의하자. 달라지지 않은 것도 있다. `pull_request_target`에서 PR의 코드를 명시적으로 체크아웃해 실행하는 것은 여전히 위험하다. GitHub 보안 문서의 말 그대로 "Workflows that use these triggers must not explicitly check out untrusted code."

## 스크립트 인젝션 — PR 제목이 명령이 될 때

네 번째 고리는 문자열이다. PR 제목이 팀의 규칙(`feat:`, `fix:` 같은 접두어)을 지키는지 검사하는 워크플로를 만든다고 해보자. 처음 떠오르는 모양은 이렇다.

```yaml
# 위험한 패턴 — 이렇게 쓰지 말자
      - name: PR 제목 검사
        run: |
          title="${{ github.event.pull_request.title }}"
          echo "$title" | grep -qE '^(feat|fix|docs):'
```

무엇이 문제일까? 8장에서 짚었듯 `${{ }}` 표현식은 셸이 실행되기 전에 문자열로 치환된다. 셸이 받는 것은 변수가 아니라 제목이 그대로 박혀 들어간 스크립트다. 누군가 제목에 따옴표를 닫고 그 뒤에 명령을 이어 붙이면, 그 명령이 우리 러너에서 실행된다. PR 제목은 아무나 정할 수 있는 입력이다. 이 워크플로가 시크릿이나 쓰기 권한을 가진 맥락에서 돈다면 결과는 앞의 pwn request와 다르지 않다.

해법은 간단하다. GitHub 보안 문서의 권고대로 "the preferred approach to handling untrusted input is to set the value of the expression to an intermediate environment variable."

```yaml
      - name: PR 제목 검사
        env:
          TITLE: ${{ github.event.pull_request.title }}
        run: |
          echo "$TITLE" | grep -qE '^(feat|fix|docs):'
```

이제 제목은 스크립트의 일부가 아니라 환경 변수의 값으로 셸에 전달된다. 셸은 `$TITLE`을 데이터로만 다룬다. 따옴표로 감싸 쓰는 것도 잊지 말자. 이 장과 앞 장들의 예제가 저장소 이름이나 PR 번호처럼 위험해 보이지 않는 값까지 `env`로 거쳐 넘긴 것은 이 습관을 몸에 붙이기 위해서다.

이것이 드문 실수라면 좋겠지만 현실은 그렇지 않다. Muralee와 동료들이 2023년 USENIX Security에 발표한 ARGUS 연구는 워크플로 2,778,483개와 액션 31,725개를 분석해, 워크플로 4,307개와 액션 80개에서 치명적인 코드 주입 취약점을 찾아냈다. 이 도구는 기존 패턴 기반 스캐너보다 7배 이상 많은 취약점을 발견했다. 연구진의 결론은 이렇다.

> "command injection vulnerabilities in the GitHub Actions ecosystem are not only pervasive but also require taint analysis to be detected."

패턴 검사만으로는 다 잡기 어렵다는 뜻이다. PR 제목만의 문제도 아니다. PR 본문, 브랜치 이름, 커밋 메시지, 이슈 제목과 코멘트처럼 외부인이 정할 수 있는 값은 모두 같은 규칙으로 다루자. `${{ }}` 안에 `github.event`로 시작하는 값이 `run`에 직접 들어가 있다면, 일단 의심하고 보는 편이 낫다.

## 공격자의 눈으로 워크플로 점검하기

네 고리를 지나왔다. 태그, 권한, 트리거, 문자열. 이 사례들이 알려 주는 원리는 하나로 모인다. 워크플로는 코드를 실행하는 시스템이고, 누가 그 코드를 정할 수 있는지와 그 코드가 무엇을 쥐고 도는지가 곧 공격 표면이다. 몇 가지 방어선을 더 보태자.

먼저 워크플로 파일 자체를 지키자. 4장에서 다룬 CODEOWNERS에 워크플로 디렉터리를 올려, 이 디렉터리를 바꾸는 PR은 플랫폼 팀이나 보안 담당의 리뷰를 거치게 한다.

```text
/.github/workflows/  @my-org/platform-team
/.github/actions/    @my-org/platform-team
```

보호 규칙에서 코드 오너 리뷰를 필수로 켜 두어야 이 한 줄이 실제 문이 된다. 권한과 트리거를 바꾸는 변경은 기능 코드와 다른 눈으로 봐야 한다.

다음은 셀프호스트 러너다. GitHub 보안 문서는 이렇게 적는다. "Self-hosted runners should almost never be used for public repositories on GitHub, because any user can open pull requests against the repository and compromise the environment." GitHub 호스트 러너는 잡마다 깨끗한 기계에서 시작하고 끝나면 사라지지만, 셀프호스트 러너는 한 번 오염되면 다음 잡에도 그 흔적이 남을 수 있다. 9장에서 러너를 고를 때 공개 저장소라면 셀프호스트를 피하자고 한 이유가 이것이다.

새로운 표면도 생기고 있다. 이슈나 PR 내용을 읽고 스스로 코드를 고치거나 코멘트를 다는 AI 에이전트 액션이 늘면서, 이슈 본문 자체가 에이전트를 조종하는 입력이 되는 프롬프트 인젝션 사례가 보도되고 있다(보도 수준, 사실 확인 필요). 원리는 스크립트 인젝션과 같다. 외부인이 정한 텍스트가 권한을 가진 실행자에게 명령으로 해석되는 것이다. 이런 액션을 들일 때는 어떤 권한과 시크릿을 쥐여 주는지부터 따져 보자.

이 모든 것을 자기 저장소에 대입해 볼 수 있게 점검표로 모으면 다음과 같다.

| 점검할 질문 | 확인할 곳 |
|---|---|
| 서드파티 액션을 full commit SHA로 고정했는가? 갱신은 자동화했는가? | 워크플로의 `uses:`, `dependabot.yml`, 조직의 액션 정책 |
| `GITHUB_TOKEN` 기본 권한이 읽기 전용인가? 워크플로에 `permissions`를 적었는가? | 조직·저장소 Actions 설정, 워크플로 상단 |
| `pull_request_target`에서 PR 코드를 체크아웃하는 곳이 있는가? | `on: pull_request_target`이 있는 워크플로 |
| `${{ github.event... }}`가 `run`에 직접 들어간 곳이 있는가? | 모든 `run:` 블록 |
| 오래 사는 클라우드 키가 저장소 시크릿에 남아 있는가? | 저장소·조직 시크릿 목록, OIDC 전환 여부(10장) |
| 워크플로 디렉터리가 CODEOWNERS로 보호되는가? | `CODEOWNERS`, 보호 규칙의 코드 오너 리뷰 |
| 공개 저장소에 셀프호스트 러너가 붙어 있는가? | 저장소·조직 러너 설정 |

일곱 가지를 한 번에 다 고치려 들면 지친다. 어디서부터 시작할까? 비용은 적고 효과는 큰 것부터 가자. 조직의 기본 토큰 권한을 읽기 전용으로 바꾸는 것은 설정 하나로 모든 워크플로의 기본 피해 범위를 줄인다. 그다음 저장소 전체에서 `pull_request_target`과 `run:` 안의 `github.event` 표현식을 검색해 보자. 검색 몇 번으로 가장 위험한 곳이 드러난다. SHA 고정은 Dependabot 설정을 먼저 넣고 나서 시작하면 한 번에 모든 참조를 바꾸는 PR을 받을 수 있고, 저장소들이 준비되면 조직 정책으로 강제한다. 오래 사는 시크릿을 OIDC로 옮기는 일은 시간이 걸리니 운영 배포부터 하나씩 옮긴다. 이 점검을 분기에 한 번쯤 반복하는 습관을 들이면, 워크플로가 늘어나는 속도를 방어선이 따라잡을 수 있다.

## 다시 그 금요일로

2025년 3월 14일로 돌아가 보자. 같은 액션을 쓰던 두 저장소가 있다.

첫 번째 저장소의 워크플로에는 `@v45`가 적혀 있다. 태그가 옮겨지는 순간 이 저장소의 CI는 악성 커밋을 실행한다. 토큰은 쓰기 권한을 쥐고 있고, 저장소 시크릿에는 1년 전에 발급한 클라우드 접근 키가 들어 있다. 로그에 찍힌 키는 누군가 폐기할 때까지 유효하다. 이 팀의 월요일은 키를 교체하고, 어디에 쓰였는지 추적하고, 무엇이 새어 나갔는지 확인하는 데 통째로 들어간다.

두 번째 저장소의 워크플로에는 40자리 SHA와 `# v45` 주석이 적혀 있다. 태그가 어디로 옮겨지든 이 저장소는 원래 커밋을 실행한다. 악성 코드는 애초에 이 저장소의 러너에 도달하지 못한다. 설령 다른 경로로 뚫렸다고 해도, 이 잡의 토큰은 읽기 전용이고, 클라우드 자격 증명은 OIDC로 받은 잡 한 번짜리 토큰이다. 새어 나가더라도 쓸 수 있는 시간은 길어야 잡 하나가 도는 동안이다. 이 팀은 월요일 아침 뉴스를 읽고 Dependabot이 올린 v46.0.1 갱신 PR을 리뷰하면 된다.

두 저장소의 차이는 거창한 보안 제품이 아니었다. `uses:` 한 줄의 참조 방식, `permissions:` 두 줄, 그리고 시크릿 대신 OIDC를 고른 배포 설정이었다. YAML 한 줄이 공격 표면이라면, 방어선도 YAML 한 줄에서 시작한다.

### 이 장의 핵심

- 태그는 움직일 수 있다. 서드파티 액션은 full commit SHA로 고정하고, Dependabot이나 Renovate로 갱신을 PR로 받는다.
- `GITHUB_TOKEN`의 기본 권한은 읽기 전용으로 두고 필요한 잡에서만 올린다. 2023년 2월 이전에 만든 조직은 기본값부터 점검한다.
- `pull_request_target`에서 PR 코드를 체크아웃해 실행하지 않는다. 쓰기가 필요하면 `pull_request` → 아티팩트 → `workflow_run`으로 나누고, 아티팩트는 데이터로만 다룬다.
- PR 제목·본문·브랜치 이름 같은 외부 입력은 `run`에 직접 넣지 말고 중간 환경 변수를 거친다.
- 워크플로 디렉터리는 CODEOWNERS로 지키고, 공개 저장소에는 셀프호스트 러너를 붙이지 않으며, 오래 사는 시크릿은 OIDC로 줄인다.
