# 웹 리서치: 개발 워크플로 전략 (Development Workflow Strategy)

- genre: tech-book / slug: dev-workflow-strategy
- 검색 시점: 2026-09-26 (모든 "현재 기준" 수치는 이 날짜의 공식 문서 기준)
- 인용 표기 규칙: 따옴표 안은 원문 발췌. 단, WebFetch 요약 모델을 거쳐 추출되었으므로 한두 단어 수준의 표기 차이는 있을 수 있다. 책에 인용문으로 그대로 옮길 문장은 fact-checker가 원문 URL로 한 번 더 대조할 것.
- 신뢰성 등급: 최상 = 공식 문서·체인지로그·원저자 원문·회사 엔지니어링 블로그 / 중 = 개인·커뮤니티 블로그, 벤더 블로그 / 하 = 2차 요약

---

## A. 브랜치 보호 · Rulesets · CODEOWNERS

## 자료 1: About protected branches (GitHub Docs)
- 출처: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- 저자·날짜: GitHub Docs, 상시 갱신 문서 (2026-09 조회 기준)
- 신뢰성: 최상
- 핵심 주장: 브랜치 보호 설정 항목 전체 목록과 required status check의 strict/loose 모드 차이를 정의한다.
- 인용 가능한 구절:
  > 설정 목록: "Require pull request reviews before merging," "Require status checks before merging," "Require conversation resolution before merging," "Require signed commits," "Require linear history," "Require merge queue," "Require deployments to succeed before merging," "Lock branch," "Do not allow bypassing the above settings," "Restrict who can push to matching branches," "Allow force pushes," "Allow deletions."
  > Strict: "The **Require branches to be up to date before merging** checkbox is checked." → "The branch **must** be up to date with the base branch before merging."
  > Loose: "The branch **does not** have to be up to date with the base branch before merging."
  > "Optionally, you can choose to dismiss stale pull request approvals when commits are pushed that affect the diff in the pull request."
  > "Enforcing a linear commit history prevents collaborators from pushing merge commits to the branch."
  > "Locking a branch will make the branch read-only and ensures that no commits can be made to the branch."
  > "You can enable this setting to apply the restrictions to admins and roles with the 'bypass branch protections' permission, too."
- 관련 섹션: 브랜치 보호 규칙 장, required status checks 장(strict 모드의 비용 → merge queue 도입 동기)

## 자료 2: About rulesets (GitHub Docs)
- 출처: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- 저자·날짜: GitHub Docs, 상시 갱신 (2026-09 조회)
- 신뢰성: 최상
- 핵심 주장: ruleset은 여러 개가 동시에 겹쳐 적용되며 가장 엄격한 규칙이 이긴다. 삭제 없이 enforcement 상태를 바꿀 수 있고, read 권한자 누구나 볼 수 있다.
- 인용 가능한 구절:
  > "A ruleset is a named list of rules that applies to a repository or to multiple repositories in an organization for customers on GitHub Team and GitHub Enterprise plans."
  > "You can have up to 75 rulesets per repository, and 75 organization-wide rulesets."
  > "Multiple rulesets can apply to the same branch at the same time, while only one branch protection rule applies."
  > "You can change a ruleset's enforcement status without deleting the ruleset."
  > "Anyone with read access to a repository can view its active rulesets."
  > "If the same rule is defined in different ways across the aggregated rulesets, the most restrictive version of the rule applies."
- 메모: 조회된 페이지 요약에서는 enforcement 상태로 Active/Disabled만 확인됨. "Evaluate" 모드는 자료 3(GA 체인지로그)에서 Enterprise Cloud 전용 "evaluation mode"로 확인. 본문에 Evaluate를 쓸 때는 플랜 제약을 병기할 것.
- 관련 섹션: Rulesets vs 브랜치 보호 비교

## 자료 3: Repository Rules — public beta(2023-04-17) / GA(2023-07-24) (GitHub Changelog)
- 출처: https://github.blog/changelog/2023-04-17-introducing-repository-rules-public-beta/ , https://github.blog/changelog/2023-07-24-repository-rules-are-generally-available/
- 저자·날짜: GitHub, 2023-04-17(베타) / 2023-07-24(GA)
- 신뢰성: 최상
- 핵심 주장: Repository rules는 "branch protections의 다음 진화"로 소개되어 2023-07-24 GA. 조직 단위 강제·evaluation mode는 Enterprise Cloud 기능.
- 인용 가능한 구절:
  > "Repository rules allow you to easily govern protections for branches and tags on your repositories."
  > (Enterprise Cloud) "evaluation mode to test rules before enforcing them."
- 버전 기준: 2023 기준 출시 연도. 플랜별 세부 기능은 2026-09 현재 Docs(자료 2)로 재확인.

## 자료 4: Required reviewer rule GA (GitHub Changelog, 2026-02-17)
- 출처: https://github.blog/changelog/2026-02-17-required-reviewer-rule-is-now-generally-available/
- 저자·날짜: GitHub, 2026-02-17 (2025-11 public preview → 2026-02 GA)
- 신뢰성: 최상
- 핵심 주장: ruleset에서 파일 경로 패턴별로 특정 팀의 승인 N개를 요구하는 규칙. CODEOWNERS를 대체하지 않고 보완한다. `!` 부정 패턴 지원(CODEOWNERS는 미지원 — 자료 5와 대비 포인트).
- 인용 가능한 구절:
  > "require a specific number of approvals from designated teams before merging into protected branches."
  > "CODEOWNERS files remain the best way to manage ownership, support individuals as reviewers, and request reviews even when not required."
- 관련 섹션: CODEOWNERS 장 말미 "최신 대안"

## 자료 5: About code owners (GitHub Docs)
- 출처: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- 저자·날짜: GitHub Docs, 2026-09 조회
- 신뢰성: 최상
- 핵심 주장: CODEOWNERS 위치 탐색 순서, "마지막 매칭 우선" 규칙, 3MB 제한, 쓰기 권한 필요, 지원되지 않는 gitignore 문법.
- 인용 가능한 구절:
  > "To use a CODEOWNERS file, create a new file called `CODEOWNERS` in the `.github/`, root, or `docs/` directory of the repository." (이 순서로 찾아 처음 찾은 것을 사용)
  > "Order is important; the last matching pattern takes the most precedence."
  > "CODEOWNERS files must be under 3 MB in size."
  > 코드 오너는 "must have write permissions for the repository."
  > 미지원: "Using `!` to negate a pattern", "Using `[ ]` to define a character range", `\`로 `#` 이스케이프
  > "an approval from *any* of the owners is sufficient to meet this requirement."
- 관련 섹션: CODEOWNERS 장 (함정: 마지막 매칭 우선, 팀 가시성·쓰기 권한)

---

## B. PR · 코드 리뷰 · 머지 방식

## 자료 6: About merge methods on GitHub (GitHub Docs)
- 출처: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github
- 저자·날짜: GitHub Docs, 2026-09 조회
- 신뢰성: 최상
- 핵심 주장: 세 머지 방식의 정의와, GitHub의 "Rebase and merge"가 로컬 `git rebase`와 다르게 항상 새 SHA·커미터 정보를 만든다는 함정.
- 인용 가능한 구절:
  > Merge commit: "All commits from the feature branch are added to the base branch in a merge commit. The pull request is merged using the `--no-ff` option."
  > Squash: "The pull request's commits are squashed into a single commit."
  > Rebase: "All commits from the topic branch (or head branch) are added onto the base branch individually without a merge commit."
  > "Always updates the committer information and creates new commit SHAs, whereas `git rebase` does not change the committer information when the rebase happens on top of an ancestor commit."
  > "The commits in the head branch are added to the base branch without commit signature verification."
- 관련 섹션: 머지 방식 비교 장

## 자료 7: Google Engineering Practices — Small CLs
- 출처: https://google.github.io/eng-practices/review/developer/small-cls.html
- 저자·날짜: Google, 2019 공개(eng-practices 저장소), 상시 문서
- 신뢰성: 최상
- 핵심 주장: 작은 변경이 리뷰 속도·철저함·버그·롤백에서 유리하며, 100줄은 적당·1000줄은 과대. 분할 전략으로 stacking, 파일별, 수평/수직 분할 제시.
- 인용 가능한 구절:
  > "100 lines is usually a reasonable size for a CL, and 1000 lines is usually too large, but it's up to the judgment of your reviewer."
  > "A 200-line change in one file might be okay, but spread across 50 files it would usually be too large."
  > "It's easier for a reviewer to find five minutes several times to review small CLs than to set aside a 30 minute block to review one large CL."
  > Stacking: "Write one small CL, send it off for review, and then immediately start writing another CL based on the first CL."
- 관련 섹션: PR 크기 장, stacked PR 장 도입

## 자료 8: Stacked pull requests public preview (GitHub Changelog, 2026-07-30)
- 출처: https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/
- 저자·날짜: GitHub, 2026-07-30
- 신뢰성: 최상
- 핵심 주장: GitHub이 네이티브 stacked PR을 public preview로 출시. `gh-stack` CLI 확장, 웹·모바일·코딩 에이전트 지원. 상위 PR을 머지하면 아래 레이어까지 한 번에 랜딩, 하위만 머지하면 위 PR은 자동 rebase·retarget. merge queue 지원은 점진 롤아웃 중.
- 인용 가능한 구절:
  > "Stacked pull requests break large changes into small, reviewable pull requests. They're an ordered series of pull requests that each represent focused layers of your change."
  > 설치: `gh extension install github/gh-stack`
  > "Merge the latest ready pull request to land it and every unmerged layer below it in one single operation. To land part of a stack, merge one or more lower layers—the pull requests above it stay open and automatically rebase and retarget."
  > "Merge queue support for stacked pull requests is rolling out progressively over the coming weeks."
- 버전 기준: 2026-07 public preview 기준. **빠르게 변하는 기능 — 집필 시점 GA 여부·merge queue 연동 상태 재확인 필요.**
- 관련 섹션: stacked PR 장 (Graphite 등 서드파티와의 관계)

## 자료 9: Graphite — Stacked diffs guide
- 출처: https://graphite.com/guides/stacked-diffs (구 graphite.dev에서 리다이렉트)
- 저자·날짜: Greg Foster (Graphite), 날짜 표기 없음
- 신뢰성: 중 (벤더 콘텐츠)
- 핵심 주장: stacked diff의 정의와 이점, Phabricator·Google Critique에서 유래한 실무 관행.
- 인용 가능한 구절:
  > "Stacked diffs refer to a series of changes where each change depends on the previous one."
- 관련 섹션: stacked PR 장 역사

## 자료 10: Draft pull requests (GitHub, 2019-02-14 / 2025-05-01)
- 출처: https://github.blog/changelog/2019-02-14-draft-pull-requests/ , https://github.blog/news-insights/product-news/introducing-draft-pull-requests/ , https://github.blog/changelog/2025-05-01-draft-pull-requests-are-now-available-in-all-repositories/
- 저자·날짜: GitHub, 2019-02-14 도입 / 2025-05-01 무료 플랜 private 저장소 확대
- 신뢰성: 최상
- 핵심 주장: draft PR은 CODEOWNERS 리뷰 요청 알림을 억제하고 "Ready for review" 전까지 머지 불가. 2025-05부터 Free 플랜 private 저장소에서도 사용 가능.
- 인용 가능한 구절:
  > (2025) "You can now create draft pull requests in any repository, public or private, completely free of charge"
  > (2019, 요약) Draft PR은 CODEOWNERS 알림을 억제하고 "Ready for review"로 표시하기 전까지 머지할 수 없다. (원문 문장은 fact-checker 대조 필요)
- 관련 섹션: draft PR 절

## 자료 11: 효과적인 코드리뷰 / 코드리뷰 도입 사례 (국내)
- 출처:
  - 우아한테크세미나 "지속가능한 SW개발을 위한 코드리뷰" 다시보기 — https://techblog.woowahan.com/8159/ (백명석, 2022-04-19)
  - 카카오 "효과적인 코드리뷰를 위한 리뷰어의 자세" — https://tech.kakao.com/posts/498 (kay.gw, 2022)
  - 카카오 "카카오스토리 팀의 코드 리뷰 도입 사례" — https://tech.kakao.com/2016/02/04/code-review/ (2016-02-04)
- 신뢰성: 최상(회사 기술블로그)
- 핵심 주장: 우아한테크세미나 — 코드리뷰는 결함 발견뿐 아니라 상호 성장 수단이며, PR 작성 기법·리뷰 기법·리뷰 우선순위/응답 시간 규칙을 다룬다.
- 인용 가능한 구절:
  > "출시 전에 결함을 발견하는 것이 가장 중요한 목적이겠지만, 팀원들과 주고받는 피드백을 통해 상호 성장을 할 수 있는" (우아한테크세미나 소개문)
- 메모: 카카오 두 글은 본문이 JS 렌더라 추출 실패 — 제목·저자만 확보. 인용이 필요하면 브라우저로 재확인.
- 관련 섹션: 코드 리뷰 관행 장

## 자료 12: GitHub Actions로 개선하는 코드 리뷰 문화 (토스)
- 출처: https://toss.tech/article/25431
- 저자·날짜: 김성일(토스페이먼츠 Server Developer), 2024-02-07
- 신뢰성: 최상
- 핵심 주장: GitHub Actions로 리뷰어 랜덤 자동 할당 + 슬랙 DM 알림 + 평일 오후 2시 미리뷰 PR 리마인더(cron)를 구축. 평균 PR 리뷰 시간이 하루 내외로 단축, 리뷰 코멘트 수 평균 2배 이상.
- 인용 가능한 구절:
  > "리뷰어 목록에서 PR 생성자를 제외하고 랜덤으로 리뷰어를 선정"
  > "평일 오후 2시에 팀 채널로"
  > 성과(요약): 평균 PR 리뷰 시간 하루 내외, 코멘트 수 평균 2배 이상, 운영 이슈 대응 시간 전년 대비 약 90% 감소 — 수치는 원문 재확인 권장
- 관련 섹션: 코드 리뷰 장 사례 박스, GitHub Actions 장(schedule 트리거 예시)

---

## C. CI 검사 · 테스트 전략 · Flaky Test

## 자료 13: Flaky Tests at Google and How We Mitigate Them / Where do our flaky tests come from?
- 출처: https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html (John Micco, 2016-05-27) ; https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html (Jeff Listfield, 2017-04-17)
- 신뢰성: 최상 (단, 본문이 스크립트 렌더라 원문 문장 직접 추출 실패)
- 핵심 주장: 테스트 실행의 약 1.5%가 flaky 결과, 전체 테스트의 약 16%가 어느 정도 flaky, post-submit에서 pass→fail 전이의 약 84%가 flaky 테스트 관련(수치 출처는 2016 Micco 글로 널리 인용). 2017 글은 테스트 크기(바이너리 크기)가 클수록 flaky 확률이 높다는 상관을 보고.
- 인용 가능한 구절: 원문 직접 추출 실패. 2차 인용 기반 요지 — "about 1.5% of all test runs reporting a 'flaky' result", "almost 16% of our tests have some level of flakiness", "84% of the transitions we observe from pass to fail involve a flaky test". **fact-checker가 브라우저로 원문 대조 필수 (사실 확인 필요).**
- 관련 섹션: flaky test 장, merge queue 실패 처리

## 자료 14: Microsoft — How Microsoft develops with DevOps (Release Flow)
- 출처: https://learn.microsoft.com/en-us/devops/develop/how-microsoft-develops-devops
- 저자·날짜: Microsoft Learn, ms.date 2022-07-18 (페이지 updated_at 2026-09-04)
- 신뢰성: 최상
- 핵심 주장: 트렁크 기반 + 스프린트 단위 release branch("Release Flow"). PR 단계는 빠른 테스트, 머지 후 긴 테스트로 분리. 핫픽스는 반드시 main 먼저, 그다음 release 브랜치로 cherry-pick. release 브랜치는 main에 다시 머지하지 않는다.
- 인용 가능한 구절:
  > "The first- and second-level test suites run around 60,000 tests in less than five minutes."
  > "Some teams have several hundred developers working constantly in a single repository, who can complete over 200 pull requests into the main branch per day."
  > "Release branches never merge back to the main branch, so they might require *cherry-picking* important changes."
  > "The process always starts by making the change in `main` first."
  > "Fixing a bug in the release branch without bringing the change back to `main` would mean the bug would recur during the next deployment"
  > "Currently, a product with 200+ pull requests might produce 300+ continuous integration builds per day, amounting to 500+ test runs every 24 hours."
  > "an often overlooked part of GitHub Flow is that pull requests must deploy to production for testing before they can merge to the main branch."
- 관련 섹션: 테스트 전략(PR 빠른 검사 vs 머지 후 검사), release branch 장, 브랜치 전략 비교

---

## D. GitHub Actions 상세

## 자료 15: Workflow syntax / Limits (GitHub Docs)
- 출처: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax , https://docs.github.com/en/actions/reference/limits
- 저자·날짜: GitHub Docs, 2026-09 조회
- 신뢰성: 최상
- 핵심 주장: 수치 한도의 1차 출처.
- 인용 가능한 구절:
  > "Each job in a workflow can run for up to 6 hours of execution time." (GitHub-hosted)
  > 워크플로 런 최대 "35 days / workflow run"
  > "A job matrix can generate a maximum of 256 jobs per workflow run."
  > (self-hosted) "A job can be in the queue for 24 hours before it is automatically cancelled."
  > 동시 잡: Free 20 / Pro 40 / Team 60 / Enterprise 500 (larger runners 1,000)
  > "The rate limit for `GITHUB_TOKEN` is 1,000 requests per hour per repository" (Enterprise Cloud 15,000)
  > 저장 한도(저장소당): Free 500 MB artifacts / Pro 1 GB / Team 2 GB / Enterprise Cloud 50 GB, cache 10 GB
  > "The `branches`, `branches-ignore`, `tags`, and `tags-ignore` keywords accept glob patterns."
  > permissions 키: actions, artifact-metadata, attestations, checks, code-quality, contents, deployments, discussions, id-token, issues, packages, pages, pull-requests, security-events, statuses, vulnerability-alerts
- 버전 기준: 2026-09 Docs 기준. 한도·플랜 수치는 자주 바뀜.

## 자료 16: Events that trigger workflows (GitHub Docs)
- 출처: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- 저자·날짜: GitHub Docs, 2026-09 조회
- 신뢰성: 최상
- 인용 가능한 구절:
  > (pull_request, fork) "With the exception of `GITHUB_TOKEN`, secrets are not passed to the runner when a workflow is triggered from a forked repository. The `GITHUB_TOKEN` has read-only permissions in pull requests from forked repositories."
  > (pull_request_target) "Running untrusted code on the `pull_request_target` trigger may lead to security vulnerabilities. These vulnerabilities include cache poisoning and granting unintended access to write privileges or secrets."
  > (merge_group) 활동 유형은 `checks_requested` 하나. "if your repository uses GitHub Actions to perform required checks on pull requests in your repository, you need to update the workflows to include the `merge_group` event as an additional trigger."
  > (workflow_run) "The workflow started by the `workflow_run` event is able to access secrets and write tokens, even if the previous workflow was not."
- 관련 섹션: 트리거 절, 보안 하드닝 절

## 자료 17: Dependency caching reference (GitHub Docs)
- 출처: https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching
- 저자·날짜: GitHub Docs, 2026-09 조회
- 신뢰성: 최상
- 인용 가능한 구절:
  > "By default, the limit is 10 GB per repository, but this limit can be increased by enterprise owners, organization owners, or repository administrators."
  > "GitHub will remove any cache entries that have not been accessed in over 7 days."
  > "Workflow runs can restore caches created in either the current branch or the default branch (usually `main`). If a workflow run is triggered for a pull request, it can also restore caches created in the base branch."
  > "Workflow runs cannot restore caches created for child branches or sibling branches."
  > 매칭 순서: key 정확 일치 → key 부분 일치 → restore-keys 순차 부분 일치
- 메모: 10 GB 초과분 유료 확장 가능(최대치는 요약상 "up to 10 TB" — 원문 대조 필요). 빠르게 변하는 영역.
- 관련 섹션: 캐시 절 (브랜치 스코프 함정)

## 자료 18: Artifacts v3 deprecation (GitHub Changelog, 2024-04-16)
- 출처: https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/
- 저자·날짜: GitHub, 2024-04-16
- 신뢰성: 최상
- 핵심 주장: 2025-01-30부터 upload/download-artifact v3 사용 불가. v4는 백엔드 재설계로 업로드가 최악 사례에서 최대 90% 이상 빨라짐, 잡당 artifact 500개 한도.
- 인용 가능한 구절(검색 결과 발췌, 원문 대조 권장):
  > "Starting January 30th, 2025, GitHub Actions customers will no longer be able to use v3 of actions/upload-artifact or actions/download-artifact."
  > "uploads are significantly faster, upwards of 90% improvement in worst case scenarios."
  > "Each job in a workflow run now has a limit of 500 artifacts."
- 버전 기준: v4/2024 기준. **2026 현재 최신 메이저 버전(v5 이상 여부)은 미확인 — 구버전 정보일 수 있음.**
- 관련 섹션: artifacts 절

## 자료 19: Reusing workflows / Reusable vs composite (GitHub Docs)
- 출처: https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows , https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations
- 저자·날짜: GitHub Docs, 2026-09 조회
- 신뢰성: 최상
- 인용 가능한 구절:
  > "For a workflow to be reusable, the values for `on` must include `workflow_call`"
  > "Workflows that call reusable workflows in the same organization or enterprise can use the `inherit` keyword to implicitly pass the secrets."
  > "Unlike when you are using actions within a workflow, you call reusable workflows directly within a job, and not from within job steps."
  > "You can connect a maximum of ten levels of workflows - that is, the top-level caller workflow and up to nine levels of reusable workflows."
  > "Loops in the workflow tree are not permitted."
  > 비교: reusable은 "Can contain multiple jobs", 러너 지정 가능, 스텝별 실시간 로깅 / composite는 "Run as a step within a job", "Logged as one step even if it contains multiple steps", "Can be nested to have up to 10 composite actions in one workflow", Marketplace 게시 가능
- 메모: 요약 모델이 composite를 "Cannot use secrets"로 옮겼는데, 정확히는 composite action이 secrets 컨텍스트를 직접 받지 못하고 inputs로 전달받아야 한다는 뜻 — 본문 서술 시 fact-checker 원문 대조 필요.
- 메모2: 과거 Docs에는 "워크플로 파일당 고유 reusable workflow 최대 N개"(20→50으로 변경 이력) 한도가 있었으나 이번 조회에서 확인 못 함 — 수치 쓰지 말거나 재확인.
- 관련 섹션: reusable workflows / composite actions 절

## 자료 20: Control the concurrency of workflows and jobs (GitHub Docs) + 대기열 확장 (Changelog 2026-05-07)
- 출처: https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency , https://github.blog/changelog/2026-05-07-github-actions-concurrency-groups-now-allow-larger-queues/
- 저자·날짜: GitHub Docs(2026-09 조회), Changelog 2026-05-07
- 신뢰성: 최상
- 핵심 주장: 기본은 그룹당 실행 1 + 대기 1이고 새 대기가 오면 기존 대기가 취소된다. 2026-05부터 `queue: max`로 최대 100개 대기 가능(순차 실행). `queue: max`와 `cancel-in-progress: true` 조합은 검증 오류.
- 인용 가능한 구절:
  > "When you limit concurrency, by default only one run can be pending in a concurrency group—any additional pending runs cancel the previous one."
  > "`queue` property accepts the following values: `single` (default)...`max`: Up to 100 jobs or workflow runs can be `pending` in the concurrency group."
  > "The combination of `queue: max` and `cancel-in-progress: true` is not allowed and will result in a workflow validation error."
  > 예시:
  > ```yaml
  > concurrency:
  >   group: ${{ github.head_ref || github.run_id }}
  >   cancel-in-progress: true
  > ```
- 버전 기준: queue 옵션은 2026-05 기준 신기능. 구버전 자료(“항상 1개 대기만 가능”)와 충돌 주의.
- 관련 섹션: concurrency 절, 배포 직렬화

## 자료 21: Deployments and environments (GitHub Docs)
- 출처: https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
- 저자·날짜: GitHub Docs, 2026-09 조회
- 신뢰성: 최상
- 인용 가능한 구절:
  > "You can list up to six users or teams as reviewers."
  > "users who initiate a deployment cannot approve the deployment job, even if they are a required reviewer." (prevent self-review 옵션)
  > Wait timer: "The time (in minutes) must be an integer between 1 and 43,200 (30 days)."
  > "A maximum of 6 deployment protection rules can be enabled on any environment at the same time."
  > "a job cannot access environment secrets until one of the required reviewers approves it."
  > 플랜: required reviewers·wait timer는 Free/Pro/Team에서는 public 저장소만.
- 관련 섹션: environments·secrets 절

## 자료 22: OpenID Connect (GitHub Docs)
- 출처: https://docs.github.com/en/actions/concepts/security/openid-connect
- 저자·날짜: GitHub Docs, 2026-09 조회
- 신뢰성: 최상
- 인용 가능한 구절:
  > "OpenID Connect allows your workflows to exchange short-lived tokens directly from your cloud provider."
  > "You won't need to duplicate your cloud credentials as long-lived GitHub secrets."
  > "With OIDC, your cloud provider issues a short-lived access token that is only valid for a single job, and then automatically expires."
  > subject 예: `repo:octo-org/octo-repo:environment:prod`, `repo:my-org/my-repo:ref:refs/heads/main`
- 메모: `permissions: id-token: write` 요구 사항은 이번 조회 페이지에서 직접 문장 확보 못 함(자료 15 permissions 목록에 id-token 존재). 클라우드별 how-to 페이지(예: AWS 구성 가이드)로 fact-checker 확인.
- 관련 섹션: OIDC 절

## 자료 23: GitHub Actions 가격 변경 (Changelog 2025-12-16, 이후 업데이트)
- 출처: https://github.blog/changelog/2025-12-16-coming-soon-simpler-pricing-and-a-better-experience-for-github-actions/ , https://github.com/resources/insights/2026-pricing-changes-for-github-actions
- 저자·날짜: GitHub, 2025-12-16 (이후 연기 공지 추가)
- 신뢰성: 최상
- 핵심 주장: 2026-01-01 GitHub-hosted runner 가격 최대 39% 인하. self-hosted runner에 분당 $0.002 플랫폼 요금(2026-03-01 예정)은 반발 후 연기.
- 인용 가능한 구절:
  > "We're postponing the announced billing change for self-hosted GitHub Actions to take time to re-evaluate our approach."
- 버전 기준: 2026-09 검색 시점. self-hosted 요금 재도입 여부 재확인 필요.
- 관련 섹션: 러너 선택·비용 박스(선택)

## 자료 24: 국내 GitHub Actions 운영 사례
- 출처: 카카오엔터프라이즈 "카카오엔터프라이즈가 GitHub Actions를 사용하는 이유" — https://tech.kakao.com/posts/516 (aaron.m2, 2022)
- 신뢰성: 최상(회사 블로그) — 단, 본문 추출 실패로 제목·저자만 확보
- 관련 섹션: GitHub Actions 장 도입부 사례 후보 (본문 인용 전 브라우저 확인 필요)

---

## E. GitHub Actions 보안 하드닝

## 자료 25: Secure use reference (GitHub Docs, Security hardening)
- 출처: https://docs.github.com/en/actions/reference/security/secure-use
- 저자·날짜: GitHub Docs, 2026-09 조회
- 신뢰성: 최상
- 인용 가능한 구절:
  > "Pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release."
  > "Pinning to a particular SHA helps mitigate the risk of a bad actor adding a backdoor to the action's repository, as they would need to generate a SHA-1 collision for a valid Git object payload."
  > "It's good security practice to set the default permission for the `GITHUB_TOKEN` to read access only for repository contents. The permissions can then be increased, as required, for individual jobs within the workflow file."
  > "For inline scripts, the preferred approach to handling untrusted input is to set the value of the expression to an intermediate environment variable."
  > "Workflows that use these triggers must not explicitly check out untrusted code, including from pull request forks or from repositories that are not under your control."
  > "Self-hosted runners should almost never be used for public repositories on GitHub, because any user can open pull requests against the repository and compromise the environment."
  > "If all your workflow files are stored `.github/workflows`, you can add this directory to the code owners list, so that any proposed changes to these files will first require approval from a designated reviewer."
- 관련 섹션: 보안 하드닝 절 전체의 뼈대

## 자료 26: Keeping your GitHub Actions and workflows secure Part 1: Preventing pwn requests (GitHub Security Lab)
- 출처: https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/
- 저자·날짜: Jaroslav Lobačevski, 2021-08-03
- 신뢰성: 최상
- 핵심 주장: `pull_request_target` + 신뢰할 수 없는 PR head 체크아웃 = 저장소 탈취 위험. 권장 패턴은 권한 없는 `pull_request` 워크플로가 결과를 artifact로 남기고, `workflow_run` 워크플로가 쓰기 권한으로 후처리.
- 인용 가능한 구절:
  > "Workflows triggered via `pull_request_target` have write permission to the target repository. They also have access to target repository secrets."
  > "Combining `pull_request_target` workflow trigger with an explicit checkout of an untrusted PR is a dangerous practice that may lead to repository compromise."
  > "They may submit malicious changes to the existing build scripts like `make` or `powershell` files or redefine the build script in the `package.json` file."
  > "The workflow processing the PR should then store any results like code coverage or failed/passed tests in artifacts and exit. The following workflow then starts on `workflow_run` where it is granted write permission to the target repository."
- 관련 섹션: pull_request_target 위험 절 (고전 레퍼런스)

## 자료 27: pull_request_target · environment 브랜치 보호 변경 (GitHub Changelog, 2025-11-07)
- 출처: https://github.blog/changelog/2025-11-07-actions-pull_request_target-and-environment-branch-protections-changes/ ; 관련 Docs https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target
- 저자·날짜: GitHub, 2025-11-07 공지, 2025-12-08 시행
- 신뢰성: 최상 (검색 결과 발췌 — 원문 대조 권장)
- 핵심 주장: `pull_request_target`은 PR의 base 브랜치와 무관하게 항상 기본 브랜치의 워크플로 파일·커밋을 사용. 이전에는 오래된 base 브랜치의 취약한 워크플로가 실행되는 악용이 있었음.
- 인용 가능한 구절(발췌):
  > "The workflow file and checkout commit will always be taken from the repository's default branch, regardless of the pull request's base branch."
  > "GITHUB_REF for pull_request_target will resolve to the default branch, and GITHUB_SHA will point to the latest commit on that branch."
  > "Historically, this behavior has led to the exploitation of outdated workflows that contained vulnerabilities in pull_request_target workflows that were presumed to be remediated since they were fixed in the default branch."
- 버전 기준: 2025-12-08 이후 동작. 이전 자료(2021 Security Lab 등)의 서술과 달라진 점 명시할 것.

## 자료 28: GITHUB_TOKEN 기본 권한 read-only 전환 (GitHub Changelog, 2023-02-02)
- 출처: https://github.blog/changelog/2023-02-02-github-actions-updating-the-default-github_token-permissions-to-read-only/
- 저자·날짜: GitHub, 2023-02-02
- 신뢰성: 최상 (검색 결과 발췌)
- 핵심 주장: 신규 엔터프라이즈·조직·개인 저장소의 GITHUB_TOKEN 기본 권한이 read-only로. 기존 것은 영향 없음(그래서 오래된 조직은 여전히 read/write일 수 있음 — 점검 포인트).
- 관련 섹션: GITHUB_TOKEN 권한 절

## 자료 29: Actions policy — 액션 차단·SHA 고정 강제 (GitHub Changelog, 2025-08-15)
- 출처: https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/
- 저자·날짜: GitHub, 2025-08-15
- 신뢰성: 최상 (검색 결과 발췌)
- 핵심 주장: 허용 액션 정책에 "full SHA 고정 강제" 체크박스 추가 — 고정되지 않은 액션을 쓰는 워크플로는 실패. `!owner/action` 접두로 특정 액션 차단 가능. tj-actions 사건(자료 30)에 대한 대응.
- 관련 섹션: 액션 SHA 고정 절

## 자료 30: tj-actions/changed-files 공급망 공격 (CVE-2025-30066) — CISA 경보
- 출처: https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction ; https://github.com/advisories/ghsa-mrrh-fwg8-r2c3
- 저자·날짜: CISA 2025-03-18 / GitHub Advisory
- 신뢰성: 최상
- 핵심 주장: 2025-03-14~15 공격자가 v1~v45.0.7 태그를 악성 커밋으로 재지정, 워크플로 로그로 시크릿 유출. 23,000개 이상 저장소 영향(보안업체 추정), v46.0.1에서 해소. 태그 참조의 가변성을 보여주는 대표 사례 — SHA 고정 근거.
- 인용 가능한 구절: "tj-actions changed-files through 45.0.7 allows remote attackers to discover secrets by reading actions logs." (GitHub Advisory 제목)
- 관련 섹션: 보안 하드닝 장 오프닝 사례

## 자료 31: Immutable releases GA (GitHub Changelog, 2025-10-28)
- 출처: https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/
- 저자·날짜: GitHub, 2025-10-28
- 신뢰성: 최상 (검색 결과 발췌)
- 핵심 주장: 불변 릴리스로 게시하면 자산 추가·수정·삭제 불가, 태그 삭제·이동 불가, 서명된 attestation 발급. 액션 배포자 측 대응책.
- 버전 기준: 2025-10 GA. "immutable actions"의 별도 출시 상태는 미확인.
- 관련 섹션: SHA 고정 절의 "앞으로" 박스

---

## F. 브랜치 전략 비교

## 자료 32: A successful Git branching model + Note of reflection (Vincent Driessen, nvie.com)
- 출처: https://nvie.com/posts/a-successful-git-branching-model/
- 저자·날짜: Vincent Driessen, 2010-01-05 원문 / 2020-03-05 반성 노트
- 신뢰성: 최상 (원저자 원문, 고전)
- 인용 가능한 구절:
  > (2020 노트) "This model was conceived in 2010, now more than 10 years ago, and not very long after Git itself came into being. In those 10 years, git-flow (the branching model laid out in this article) has become hugely popular in many a software team to the point where people have started treating it like a standard of sorts — but unfortunately also as a dogma or panacea."
  > "Web apps are typically continuously delivered, not rolled back, and you don't have to support multiple versions of the software running in the wild."
  > "If your team is doing continuous delivery of software, I would suggest to adopt a much simpler workflow (like GitHub flow) instead of trying to shoehorn git-flow into your team."
  > "If, however, you are building software that is explicitly versioned, or if you need to support multiple versions of your software in the wild, then git-flow may still be as good of a fit to your team as it has been to people in the last 10 years."
  > "To conclude, always remember that panaceas don't exist. Consider your own context. Don't be hating. Decide for yourself."
  > master: "the main branch where the source code of `HEAD` always reflects a _production-ready_ state."
  > develop: "the main branch where the source code of `HEAD` always reflects a state with the latest delivered development changes for the next release."
  > "The `--no-ff` flag causes the merge to always create a new commit object, even if the merge could be performed with a fast-forward. This avoids losing information about the historical existence of a feature branch and groups together all commits that together added the feature."
- 관련 섹션: Git Flow 절, 전략 선택 기준

## 자료 33: GitHub flow (GitHub Docs)
- 출처: https://docs.github.com/en/get-started/using-github/github-flow
- 저자·날짜: GitHub Docs, 2026-09 조회
- 신뢰성: 최상
- 인용 가능한 구절:
  > "GitHub flow is a lightweight, branch-based workflow."
  > 단계: Create a branch → Make changes → Create a pull request → Address review comments → Merge your pull request → Delete your branch
  > "After you merge your pull request, delete your branch. This indicates that the work on the branch is complete and prevents you or others from accidentally using old branches."
- 관련 섹션: GitHub Flow 절 (배포 시점은 Docs에 명시 없음 — Microsoft 자료 14의 "PR을 먼저 배포" 서술과 대조 포인트)

## 자료 34: GitLab Flow (GitLab)
- 출처: https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/ ; 원문 https://about.gitlab.com/blog/2014/09/29/gitlab-flow/ (2014-09-29, 당시 CEO Sid Sijbrandij 작성으로 알려짐 — 조회 페이지에 저자 표기 없음)
- 신뢰성: 최상(공식) / 원문 날짜는 URL 기준
- 핵심 주장: main + production(환경) 브랜치. 커밋은 downstream으로만 흐른다(main→pre-production→production). 여러 버전 유지가 필요하면 release 브랜치(v1, v2).
- 인용 가능한 구절:
  > "teams practice feature branching, while also maintaining a separate production branch. Whenever the 'main' branch is ready to be deployed, users merge it into the production branch and release."
  > "Teams can add as many pre-production branches as needed — for example, from `main` to test, from test to acceptance, and from acceptance to production."
  > "Commits flow downstream to ensure that every line of code is tested in all environments."
- 메모: 2014 원문의 "upstream first" 문장은 이번 조회에서 추출 못 함(현재 URL이 토픽 페이지 내용으로 대체됨). 인용 전 archive.org 확인 권장.
- 관련 섹션: GitLab Flow 절

## 자료 35: Trunk Based Development (trunkbaseddevelopment.com)
- 출처: https://trunkbaseddevelopment.com/
- 저자·날짜: Paul Hammant 외, 상시 갱신 사이트
- 신뢰성: 최상 (사실상 표준 레퍼런스)
- 인용 가능한 구절:
  > "A source-control branching model, where developers collaborate on code in a single branch called 'trunk' and resist any pressure to create other long-lived development branches."
  > "Trunk-Based Development is a key enabler of Continuous Integration and by extension Continuous Delivery."
  > short-lived feature branch는 "for code-review and build checking (CI), but not artifact creation or publication, to happen before commits land in the trunk."
  > release branch: "Release branches that are cut from the trunk on a just-in-time basis, are 'hardened' before a release ... and those branches are deleted some time after release."
- 관련 섹션: TBD 절, release branch 절

## 자료 36: DORA capability — Trunk-based development
- 출처: https://dora.dev/capabilities/trunk-based-development/
- 저자·날짜: DORA (Google Cloud), 상시 문서
- 신뢰성: 최상
- 인용 가능한 구절:
  > "Each developer divides their own work into small batches and merges that work into trunk at least once (and potentially several times) a day."
  > "Have three or fewer active branches in the application's code repository."
  > "Merge branches to trunk at least once a day."
  > "Don't have code freezes and don't have integration phases."
- 관련 섹션: TBD 절, DORA 연결

## 자료 37: Patterns for Managing Source Code Branches (Martin Fowler)
- 출처: https://martinfowler.com/articles/branching-patterns.html
- 저자·날짜: Martin Fowler, 2020-05-28 (연재 완결일)
- 신뢰성: 최상
- 인용 가능한 구절:
  > "Frequent integration increases the frequency of merges but reduces their complexity and risk."
  > "The smaller the integrations, the less likely they are to turn into an epic merge of misery and despair."
  > "Continuous Integration allows a team to get the benefits of high-frequency integration, while decoupling feature length from integration frequency."
  > "Release branches are a valuable tool when a team isn't able to keep their mainline in a healthy state."
  > "Environment branches are an example of using source branching as a poor man's modular architecture."
  > "Overall I much prefer to work on a team that uses Continuous Integration."
- 관련 섹션: 브랜치 전략 비교 장의 이론 축(통합 빈도), GitLab Flow 환경 브랜치 비판

## 자료 38: OneFlow – a Git branching model and workflow (Adam Ruka)
- 출처: https://www.endoflineblog.com/oneflow-a-git-branching-model-and-workflow
- 저자·날짜: Adam Ruka. 페이지 표기 2017-04-30 (최초 게시는 2015년으로 알려짐 — fact-checker 확인)
- 신뢰성: 최상 (원저자)
- 인용 가능한 구절:
  > "OneFlow's basic premise is to have one eternal branch in your repository."
  > "OneFlow has been conceived as a simpler alternative to GitFlow."
  > "OneFlow's branching model is exactly as powerful as GitFlow's. There is not a single thing that can be done using GitFlow that can't be achieved (in a simpler way) with OneFlow."
  > "Once whatever process you use for releasing is finished, the tip of the branch is tagged with the version number."
- 관련 섹션: OneFlow 절

## 자료 39: Feature Toggles (aka Feature Flags) (Pete Hodgson, martinfowler.com)
- 출처: https://martinfowler.com/articles/feature-toggles.html
- 저자·날짜: Pete Hodgson, 2017-10-09
- 신뢰성: 최상
- 인용 가능한 구절:
  > "Release Toggles allow incomplete and un-tested codepaths to be shipped to production as latent code which may never be turned on."
  > "Savvy teams view the Feature Toggles in their codebase as inventory which comes with a carrying cost and seek to keep that inventory as low as possible."
  > 분류: Release / Experiment / Ops / Permissioning — 수명·동적성 축
- 관련 섹션: feature flag 절 (TBD의 전제 조건)

## 자료 40: Git Branching — Branching Workflows (Pro Git, git-scm.com)
- 출처: https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows
- 저자·날짜: Scott Chacon·Ben Straub, Pro Git 2nd ed. (2014)
- 신뢰성: 최상 (고전)
- 인용 가능한 구절:
  > "It's generally easier to think about them as work silos, where sets of commits graduate to a more stable silo when they're fully tested."
  > "A topic branch is a short-lived branch that you create and use for a single particular feature or related work. ... But in Git it's common to create, work on, merge, and delete branches several times a day."
- 관련 섹션: 브랜치 전략 장 도입(장기 브랜치 vs 토픽 브랜치)

## 자료 41: 우린 Git-flow를 사용하고 있어요 (우아한형제들)
- 출처: https://techblog.woowahan.com/2553/ (구 https://woowabros.github.io/experience/2017/10/30/baemin-mobile-git-branch-strategy.html)
- 저자·날짜: 우아한형제들 배민프론트개발팀 안드로이드 파트, 2017-10-30
- 신뢰성: 최상
- 핵심 주장: 2016-01 GitHub 이전 시 GitHub-flow로 시작, 팀이 2~3명→5명으로 늘고 현재 릴리스와 다음 릴리스 작업을 병렬로 하게 되며 2017-06 Git-flow로 전환. Upstream(공용)/Origin(개인 fork)/Local 3계층, 커밋 squash·rebase로 선형 이력, PR 작성자가 직접 머지.
- 인용 가능한 구절: 원문 문장 직접 추출은 요약 수준 — 검색 결과 발췌: "2016년 1월에 Github로 소스코드를 이전하면서 Github-flow를 사용하기 시작했으나, 2017년 6월부터 Git-flow로 브랜치 전략을 바꾸게 되었습니다." (원문 대조 권장)
- 관련 섹션: Git Flow 절 국내 사례 (모바일 앱 = 명시적 버전 소프트웨어 → Driessen 2020 노트와 정합)

## 자료 42: Git Flow에서 트렁크 기반 개발으로 나아가기 (맘시터)
- 출처: https://tech.mfort.co.kr/blog/2022-08-05-trunk-based-development/
- 저자·날짜: 맘시터(Mfort) 기술블로그, 2022-08-05
- 신뢰성: 최상(회사 블로그, 스타트업)
- 핵심 주장: Git Flow의 다중 장기 브랜치·잦은 충돌·드문 배포 문제로 TBD 전환. 작은 배포(주 단위 증분), feature toggle, 테스트 자동화를 보완책으로 사용. 하루 5회 이상 배포, PR은 대개 300줄 미만(요약 수치 — 원문 대조 필요).
- 관련 섹션: TBD 전환 국내 사례

## 자료 43: 기타 국내 참고 (중)
- 프론트엔드 모노레포 TBD로 관리하기 (매스프레소 QANDA, Hyunmin Woo) — https://blog.mathpresso.com/프론트엔드-모노레포-tbd로-관리하기-af752314d30f — feature flag·다크런칭·QA 흐름. 날짜 미확인.
- 모노리포 개발 가이드 (버즈빌) — https://tech.buzzvil.com/handbook/workingflow-in-monorepo
- AWS 권장 가이드(한국어) "Git 브랜칭 전략 선택" — https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/choosing-git-branch-approach/ (트렁크·GitHub Flow·Gitflow 장단점 한국어 공식 문서)
- 신뢰성: 중~최상. 본문 미확인, 후보 목록.

---

## G. Merge Queue와 대안

## 자료 44: Managing a merge queue (GitHub Docs)
- 출처: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue
- 저자·날짜: GitHub Docs, 2026-09 조회
- 신뢰성: 최상
- 인용 가능한 구절:
  > "A merge queue helps increase velocity by automating pull request merges into a busy branch and ensuring the branch is never broken by incompatible changes."
  > ```yaml
  > on:
  >   pull_request:
  >   merge_group:
  > ```
  > Build concurrency: "The maximum number of `merge_group` webhooks to dispatch (between `1` and `100`), throttling the total amount of concurrent CI builds."
  > Merge limits: "Select the minimum and maximum number of pull requests to merge into the base branch at the same time (between `1` and `100`), and a timeout"
  > Status check timeout: "Choose how long the queue should wait for a response from CI before assuming that checks have failed."
  > "Only merge non-failing pull requests" — 그룹 내 앞 PR이 실패해도 마지막 PR이 통과하면 함께 머지할지 결정하는 토글
  > "If there are failed required status checks or conflicts with the base branch, the pull request will be removed from the queue."
  > "jumping to the top of a merge queue will cause a full rebuild of all in-progress pull requests."
  > (검색 발췌) 서드파티 CI는 "gh-readonly-queue/{base_branch}" 접두 브랜치 push에 반응하도록 설정해야 하며, 이 임시 브랜치는 PR과 다른 SHA를 가진다. merge_group 트리거가 없으면 "status checks will not be triggered when you add a pull request to a merge queue. The merge will fail as the required status check will not be reported."
- 메모: 기본값(예: build concurrency 5, 최소 그룹 1/최대 5, 대기 5분, 타임아웃 60분)은 이번 조회에서 확인되지 않음 — 본문에 기본값 쓰려면 UI/원문 재확인 필수.
- 관련 섹션: Merge Queue 설정 옵션 절

## 자료 45: Merging a pull request with a merge queue (GitHub Docs)
- 출처: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request-with-a-merge-queue
- 저자·날짜: GitHub Docs, 2026-09 조회
- 신뢰성: 최상
- 인용 가능한 구절:
  > "A pull request can be removed from the merge queue if it no longer meets merge requirements or if a queue check fails."
  > 제거 사유: "Configured CI service is reporting test failures for a merge group," "Timed out awaiting a successful CI result," "User requesting a removal via the API or merge queue interface," "Branch protection failure that could not automatically be resolved."
- 관련 섹션: 실패 처리 절

## 자료 46: Pull request merge queue GA (Changelog 2023-07-12) + 블로그
- 출처: https://github.blog/changelog/2023-07-12-pull-request-merge-queue-is-now-generally-available/ ; https://github.blog/news-insights/product-news/github-merge-queue-is-generally-available/ ; 베타 https://github.blog/changelog/2023-02-08-pull-request-merge-queue-public-beta/
- 저자·날짜: GitHub / 블로그 Dustin Yin, 2023-07-12 (블로그 2024-04-25 갱신), public beta 2023-02-08
- 신뢰성: 최상
- 핵심 주장: GA 시 가용 범위는 Enterprise Cloud의 private/public 저장소 + 조직 소유의 모든 public 저장소. 큐 앞자리 점프는 기본적으로 admin만.
- 인용 가능한 구절:
  > "ensuring each pull request queued for merging is tested with any other pull requests queued ahead of it."
  > "Jumping to the front of the queue is now only available to admins by default"
  > (Block Inc., Jon Graves) "We would routinely experience post-merge build failures in our monorepo several times a week and merge queue has practically eliminated all build failures in that category."
- 버전 기준: 2023 GA 기준. **2026-09 현재 Team 플랜 private 저장소 지원 여부는 공식 확인 못 함** — 커뮤니티 요청 토론(https://github.com/orgs/community/discussions/201908)이 남아 있어 여전히 미지원으로 보이나 fact-checker 확인 필요.

## 자료 47: How GitHub uses merge queue to ship hundreds of changes every day (GitHub Blog)
- 출처: https://github.blog/engineering/engineering-principles/how-github-uses-merge-queue-to-ship-hundreds-of-changes-every-day/
- 저자·날짜: Will Smythe, Lawrence Gripper, 2024-03-06
- 신뢰성: 최상
- 핵심 주장: 이전의 "train" 방식(최대 15개 PR 묶음, 충돌 시 8시간+ 대기 후 탈락)을 merge queue로 대체. 모놀리식 저장소에서 30개 이상 동시 배포 가능, 평균 대기 33% 감소.
- 인용 가능한 구절:
  > "A train was a special pull request that grouped together multiple pull requests (passengers)"
  > "wait 8+ hours after joining a train for it to ship, only for it to be removed due to a conflict"
  > "Over 500 engineers merge 2,500 pull requests into our large monorepo with merge queue" (기간 표현은 원문 대조 필요 — 월 단위로 알려짐)
  > "30,000+ pull requests with their associated 4.5 million CI runs"
  > "The average wait time to ship a change has also been reduced by 33%"
  > "one of the best quality-of-life improvements to shipping changes that I've seen at GitHub!"
- 관련 섹션: Merge Queue 장 오프닝 사례

## 자료 48: Shopify — Introducing the Merge Queue (2018) / Successfully Merging the Work of 1000+ Developers (2019)
- 출처: https://shopify.engineering/introducing-the-merge-queue (Darren Worrall, 2018-06-08) ; https://shopify.engineering/successfully-merging-work-1000-developers (Jack Li, 2019-11-14)
- 신뢰성: 최상
- 핵심 주장: 2018 — Shipit 배포 도구에 merge queue 내장, 코어 앱 PR의 90% 이상이 사용. 2019 v2 — "predictive branch"에 PR을 병합해 CI, 배치 크기 8, 3개 배치 분량을 동시 CI, flaky 대응으로 실패 허용 임계값, `/shipit --emergency`로 긴급 머지. 1000+ 개발자, 일 약 400 커밋, 하루 40회 배포.
- 인용 가능한 구절:
  > (2018) "Occasionally, master merges can go wrong. For example, two unrelated merges can affect one another, the introduction of a new flaky test, or even accidental merges of work in progress."
  > (2018) "Over 90% of pull requests to Shopify's core application are using Shipit with the merge queue!"
  > (2019) "a batch size of 8 as a balance between throughput and risk"
  > (2019) "a 'predictive branch,' implemented as a git branch, onto which pull requests are merged, and CI is run."
  > (2019) 원칙: "Master must always be green (passing CI)", "Master must stay close to production", "Emergency merges must be fast"
- 관련 섹션: Merge Queue 역사·배치 크기 설계

## 자료 49: Uber SubmitQueue — Keeping Master Green at Scale / Bypassing Large Diffs in SubmitQueue
- 출처: 논문 페이지 https://www.uber.com/blog/research/keeping-master-green-at-scale (조회 시 404) ; 블로그 https://www.uber.com/blog/bypassing-large-diffs-in-submitqueue/ (Zhongpeng Lin, Matthew Williams, 2023-08-31)
- 신뢰성: 최상
- 핵심 주장: SubmitQueue는 GitHub merge queue·GitLab merge train과 같은 문제를 푸는 시스템. 대형 diff가 뒤 변경을 막는 문제를 BLRD로 해결해 Go 모노레포 P95 대기시간 74% 감소. (원 논문은 EuroSys 2019 — paper-researcher 영역)
- 인용 가능한 구절:
  > "solves the same problem as Github's 'merge queue' and GitLab's 'merge train' features."
  > "After enabling BLRD in the SubmitQueue for Uber's Go monorepo in late May 2023, the P95 wait time of June is 74% less than that of April."
- 관련 섹션: Merge Queue 대규모 사례, 투기적 실행(speculation) 개념

## 자료 50: Mergify Merge Queue docs (batches, parallel/speculative checks, two-step CI)
- 출처: https://docs.mergify.com/merge-queue/batches/ , https://docs.mergify.com/merge-queue/parallel-checks/ , https://docs.mergify.com/merge-queue/two-step/
- 저자·날짜: Mergify 공식 문서, 2026-09 조회
- 신뢰성: 최상(해당 제품 1차 문서) / 마케팅 수치는 중
- 인용 가능한 구절:
  > "If a batch fails, all subsequent batches are deemed to fail as well, are canceled and put back into the queue. The system splits the failed batch to isolate the problematic pull request."
  > "If a batch contains only one pull request and still fails, it is deemed to be the culprit and is removed from the queue."
  > `batch_max_wait_time`로 배치가 찰 때까지 대기
  > (two-step CI, 요지) PR에는 lint·unit 등 가벼운 검사, 큐 진입 시에만 통합·E2E 등 비싼 검사
- 관련 섹션: 대안 비교, CI 비용 설계(PR 검사 vs merge_group 검사 분리)

## 자료 51: bors — Not Rocket Science Rule과 bors-ng 종료
- 출처: https://bors.tech/newsletter/2023/04/30/tmib-76/ ; Graydon Hoare 원문 https://graydon2.dreamwidth.org/1597.html (조회 403)
- 저자·날짜: bors-ng 메인테이너, 2023-04-30 / Graydon Hoare 2014
- 신뢰성: 최상(원 프로젝트)
- 인용 가능한 구절:
  > "As the primary maintainer, I officially declare Bors-NG to be feature frozen and deprecated. The public instance will remain running for awhile, but it will eventually start emitting warnings and be taken down."
  > Not Rocket Science Rule(2차 인용): "automatically maintain a repository of code that always passes all the tests" — Graydon 원문 대조 필요
- 메모: 종료 사유는 GitHub 네이티브 merge queue의 공개. Rust 프로젝트는 자체 후속 bors를 운영(별도 확인 필요).
- 관련 섹션: Merge Queue 역사

## 자료 52: Graphite Merge Queue — Shopify 사례 (벤더)
- 출처: https://graphite.com/customer/shopify-merge-queu (URL 원문 그대로)
- 저자·날짜: Graphite, 날짜 미확인
- 신뢰성: 중(벤더 고객 사례)
- 핵심 주장(제목): Shopify가 Graphite Merge Queue로 대기를 "hours to minutes"로 줄였다는 사례. stacked PR 인지형 큐.
- 관련 섹션: 대안 비교 (본문 미확인 — 인용 전 확인)

---

## H. DORA 지표

## 자료 53: DORA's software delivery metrics (dora.dev)
- 출처: https://dora.dev/guides/dora-metrics/
- 저자·날짜: DORA, "Last updated: January 5, 2026"
- 신뢰성: 최상
- 핵심 주장: 기존 4 key metrics에서 5개 지표로 진화. throughput 3개 + instability 2개. MTTR은 Failed Deployment Recovery Time으로 대체.
- 인용 가능한 구절:
  > Change Lead Time: "The amount of time it takes for a change to go from committed to version control to deployed in production."
  > Deployment Frequency: "The number of deployments over a given period or the time between deployments."
  > Failed Deployment Recovery Time: "The time it takes to recover from a deployment that fails and requires immediate intervention."
  > Change Fail Rate: "The ratio of deployments that require immediate intervention following a deployment."
  > Deployment Rework Rate: "The ratio of deployments that are unplanned but happen as a result of an incident in production."
- 버전 기준: 2026-01 갱신판 기준 5지표. 구 자료의 "4 key metrics / MTTR" 표기와 구분할 것.
- 관련 섹션: DORA 장, 워크플로 선택의 측정 근거

## 자료 54: 2025 DORA Report — State of AI-assisted Software Development
- 출처: https://dora.dev/dora-report-2025/ ; Google Cloud 발표 https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
- 저자·날짜: DORA/Google Cloud, 2025 (9월 발간)
- 신뢰성: 최상 (단, 이번엔 발표문·2차 요약 수준 추출)
- 핵심 주장: AI는 "증폭기". AI 도입률 90%. AI 역량 모델 7개 중 "Strong version control practices"와 "Working in small batches" 포함. AI 도입은 throughput 상승과 함께 instability도 증가.
- 인용 가능한 구절: 원문 PDF 문장 미추출 — 인용 시 https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf 대조 필요 (사실 확인 필요)
- 관련 섹션: 에필로그/DORA 장 — "AI 시대에 작은 배치와 버전 관리 규율이 더 중요해진다"

---

## 수집 한계
- 접근 실패한 자료: Google Testing Blog 2016·2017 flaky 글 본문(스크립트 렌더) — 1.5%/16%/84% 수치는 2차 인용만 확보, 원문 대조 필수. 카카오 기술블로그 두 글(posts/498, posts/516) 본문 미로딩. Uber "Keeping Master Green at Scale" 블로그 페이지 404(논문 자체는 paper-researcher 영역). Graydon Hoare "Not Rocket Science Rule" 원문 403. GitLab Flow 2014 원문은 현재 토픽 페이지 내용으로 대체되어 "upstream first" 원문 문장 미확보.
- 미확인 수치: GitHub merge queue 설정 기본값(concurrency·그룹 크기·wait·timeout), 2026 현재 Team 플랜 private 저장소 merge queue 지원 여부, reusable workflow 파일당 호출 한도, OIDC `id-token: write` 문장, artifact 액션 최신 메이저 버전.
- 국내 자료 비중: 전체 약 20%로 스킬 기준(60~70%)에 못 미침. merge queue·Actions 보안·rulesets에 대한 국내 회사 기술블로그 1차 사례를 찾지 못함(토스·카카오·우아한형제들 모두 해당 주제 글 미발견). 국내 사례는 코드 리뷰(토스·우아한·카카오)와 브랜치 전략(우아한·맘시터)에 편중.
- 의도적으로 제외: Reddit/HN/GeekNews 토론(community-researcher 담당), EuroSys·ICSE 논문(paper-researcher 담당), 출처 불명 나열형 블로그·벤더 SEO 글(Mergify 블로그 수치 등은 문서만 채택).
- 추출 방식 한계: WebFetch 요약 모델 경유라 인용문이 원문과 미세하게 다를 수 있음. 책에 직접 인용할 문장은 fact-checker가 URL 원문으로 대조할 것.
