# 개발 워크플로 전략 레퍼런스

- genre: tech-book / slug: dev-workflow-strategy
- 대상 독자: Git 기초를 아는 1~5년차 실무 개발자
- 합성 시점: 2026-09-26. 원천: `research/web.md`, `research/papers.md`, `research/community.md` (보존 — fact-checker 1차 대조 근거)
- 표기 규칙
  - 출처 유형 태그: **[웹]** 공식 문서·체인지로그·원저자 원문·회사/개인 블로그, **[논문]** 동료 심사 논문·프리프린트·단행본, **[커뮤니티]** HN·Lobsters·GitHub Community Discussions·GeekNews·국내 블로그 토론
  - 인용문(따옴표·`>`)은 원천 파일의 표현을 그대로 옮겼다. web·community 인용은 WebFetch 요약 모델을 거쳐 추출돼 한두 단어 차이가 있을 수 있으므로, 책에 인용문으로 옮길 문장은 원문 URL로 한 번 더 대조한다.
  - **⚠ 경고**: 원천 리서처가 붙인 "이렇게 쓰지 말 것 / 원문 대조 필요" 경고를 그대로 옮긴 것. **(확인 필요)**: 출처가 2차·요약·익명이거나 수치가 충돌하는 항목.
  - 커뮤니티 인용은 전부 "커뮤니티 의견, 검증 필요" 전제.

---

## 1. 개념과 정의

### 1.1 브랜치 보호 규칙 (Protected branches) [웹]
- 설정 항목 전체: "Require pull request reviews before merging," "Require status checks before merging," "Require conversation resolution before merging," "Require signed commits," "Require linear history," "Require merge queue," "Require deployments to succeed before merging," "Lock branch," "Do not allow bypassing the above settings," "Restrict who can push to matching branches," "Allow force pushes," "Allow deletions." (GitHub Docs, About protected branches, 2026-09 조회)
- required status check의 두 모드
  - Strict: "The **Require branches to be up to date before merging** checkbox is checked." → "The branch **must** be up to date with the base branch before merging."
  - Loose: "The branch **does not** have to be up to date with the base branch before merging."
  - 책 연결: strict 모드의 비용(매번 base 따라잡기 + 재검사)이 merge queue 도입 동기.
- "Optionally, you can choose to dismiss stale pull request approvals when commits are pushed that affect the diff in the pull request."
- "Enforcing a linear commit history prevents collaborators from pushing merge commits to the branch."
- "Locking a branch will make the branch read-only and ensures that no commits can be made to the branch."
- 관리자 포함 적용: "You can enable this setting to apply the restrictions to admins and roles with the 'bypass branch protections' permission, too."

### 1.2 Rulesets [웹]
- 정의: "A ruleset is a named list of rules that applies to a repository or to multiple repositories in an organization for customers on GitHub Team and GitHub Enterprise plans." (GitHub Docs, About rulesets, 2026-09 조회)
- 한도: "You can have up to 75 rulesets per repository, and 75 organization-wide rulesets."
- 브랜치 보호와의 차이: "Multiple rulesets can apply to the same branch at the same time, while only one branch protection rule applies."
- 겹칠 때: "If the same rule is defined in different ways across the aggregated rulesets, the most restrictive version of the rule applies."
- "You can change a ruleset's enforcement status without deleting the ruleset." / "Anyone with read access to a repository can view its active rulesets."
- 연혁: public beta 2023-04-17, GA 2023-07-24 ("branch protections의 다음 진화"로 소개). "Repository rules allow you to easily govern protections for branches and tags on your repositories." (GitHub Changelog)
- ⚠ 경고: 조회된 Docs 요약에서는 enforcement 상태가 Active/Disabled만 확인됨. "Evaluate" 모드는 GA 체인지로그에서 Enterprise Cloud 전용 "evaluation mode to test rules before enforcing them."으로 확인. 본문에 Evaluate를 쓸 때는 플랜 제약을 병기할 것.
- Required reviewer rule (GA 2026-02-17, 2025-11 public preview → 2026-02 GA): ruleset에서 파일 경로 패턴별로 "require a specific number of approvals from designated teams before merging into protected branches." `!` 부정 패턴 지원(CODEOWNERS는 미지원 — 대비 포인트). CODEOWNERS를 대체하지 않는다: "CODEOWNERS files remain the best way to manage ownership, support individuals as reviewers, and request reviews even when not required."

### 1.3 CODEOWNERS [웹]
- 위치: "To use a CODEOWNERS file, create a new file called `CODEOWNERS` in the `.github/`, root, or `docs/` directory of the repository." (이 순서로 찾아 처음 찾은 것을 사용)
- 우선순위: "Order is important; the last matching pattern takes the most precedence."
- 크기: "CODEOWNERS files must be under 3 MB in size."
- 코드 오너는 "must have write permissions for the repository."
- 미지원 문법: "Using `!` to negate a pattern", "Using `[ ]` to define a character range", `\`로 `#` 이스케이프
- 승인 요건: "an approval from *any* of the owners is sufficient to meet this requirement."
- 보안 연결: "If all your workflow files are stored `.github/workflows`, you can add this directory to the code owners list, so that any proposed changes to these files will first require approval from a designated reviewer." (Secure use reference)

### 1.4 머지 방식 세 가지 [웹]
- Merge commit: "All commits from the feature branch are added to the base branch in a merge commit. The pull request is merged using the `--no-ff` option."
- Squash: "The pull request's commits are squashed into a single commit."
- Rebase: "All commits from the topic branch (or head branch) are added onto the base branch individually without a merge commit."
- 함정: GitHub의 Rebase and merge는 "Always updates the committer information and creates new commit SHAs, whereas `git rebase` does not change the committer information when the rebase happens on top of an ancestor commit." / "The commits in the head branch are added to the base branch without commit signature verification." (GitHub Docs, About merge methods, 2026-09 조회)
- `--no-ff`의 원래 동기(Driessen 2010): "The `--no-ff` flag causes the merge to always create a new commit object, even if the merge could be performed with a fast-forward. This avoids losing information about the historical existence of a feature branch and groups together all commits that together added the feature."

### 1.5 Draft PR [웹]
- 2019-02-14 도입. Draft PR은 CODEOWNERS 리뷰 요청 알림을 억제하고 "Ready for review"로 표시하기 전까지 머지할 수 없다. ⚠ 경고: 2019 원문 문장은 요약 수준 — fact-checker 대조 필요.
- 2025-05-01부터 Free 플랜 private 저장소까지: "You can now create draft pull requests in any repository, public or private, completely free of charge"

### 1.6 Stacked PR / stacked diffs [웹]
- 정의(Graphite, 벤더): "Stacked diffs refer to a series of changes where each change depends on the previous one." Phabricator·Google Critique에서 유래한 관행.
- GitHub 네이티브 stacked PR — **public preview 2026-07-30**: "Stacked pull requests break large changes into small, reviewable pull requests. They're an ordered series of pull requests that each represent focused layers of your change."
  - 설치: `gh extension install github/gh-stack`. 웹·모바일·코딩 에이전트 지원.
  - "Merge the latest ready pull request to land it and every unmerged layer below it in one single operation. To land part of a stack, merge one or more lower layers—the pull requests above it stay open and automatically rebase and retarget."
  - "Merge queue support for stacked pull requests is rolling out progressively over the coming weeks."
  - ⚠ 경고: 빠르게 변하는 기능 — 집필 시점 GA 여부·merge queue 연동 상태 재확인 필요.
- Google small CLs의 stacking 정의: "Write one small CL, send it off for review, and then immediately start writing another CL based on the first CL."

### 1.7 브랜치 전략 정의 [웹]
- **Git Flow** (Vincent Driessen, 2010-01-05 원문)
  - master: "the main branch where the source code of `HEAD` always reflects a _production-ready_ state."
  - develop: "the main branch where the source code of `HEAD` always reflects a state with the latest delivered development changes for the next release."
- **GitHub Flow** (GitHub Docs, 2026-09 조회): "GitHub flow is a lightweight, branch-based workflow." 단계: Create a branch → Make changes → Create a pull request → Address review comments → Merge your pull request → Delete your branch. "After you merge your pull request, delete your branch. This indicates that the work on the branch is complete and prevents you or others from accidentally using old branches." — 배포 시점은 Docs에 명시 없음(§4 논쟁 참고).
- **GitLab Flow** (GitLab 토픽 페이지; 원문 2014-09-29 블로그, 당시 CEO Sid Sijbrandij 작성으로 알려짐 — 조회 페이지에 저자 표기 없음)
  - "teams practice feature branching, while also maintaining a separate production branch. Whenever the 'main' branch is ready to be deployed, users merge it into the production branch and release."
  - "Teams can add as many pre-production branches as needed — for example, from `main` to test, from test to acceptance, and from acceptance to production."
  - "Commits flow downstream to ensure that every line of code is tested in all environments." 여러 버전 유지가 필요하면 release 브랜치(v1, v2).
  - ⚠ 경고: 2014 원문의 "upstream first" 문장은 추출 못 함(현재 URL이 토픽 페이지로 대체). 인용 전 archive.org 확인.
- **Trunk-Based Development** (trunkbaseddevelopment.com, Paul Hammant 외)
  - "A source-control branching model, where developers collaborate on code in a single branch called 'trunk' and resist any pressure to create other long-lived development branches."
  - "Trunk-Based Development is a key enabler of Continuous Integration and by extension Continuous Delivery."
  - short-lived feature branch는 "for code-review and build checking (CI), but not artifact creation or publication, to happen before commits land in the trunk."
  - release branch: "Release branches that are cut from the trunk on a just-in-time basis, are 'hardened' before a release ... and those branches are deleted some time after release."
  - DORA 기준: "Each developer divides their own work into small batches and merges that work into trunk at least once (and potentially several times) a day." / "Have three or fewer active branches in the application's code repository." / "Merge branches to trunk at least once a day." / "Don't have code freezes and don't have integration phases."
- **OneFlow** (Adam Ruka; 페이지 표기 2017-04-30, 최초 게시는 2015년으로 알려짐 — **(확인 필요)**)
  - "OneFlow's basic premise is to have one eternal branch in your repository." / "OneFlow has been conceived as a simpler alternative to GitFlow."
  - "OneFlow's branching model is exactly as powerful as GitFlow's. There is not a single thing that can be done using GitFlow that can't be achieved (in a simpler way) with OneFlow."
  - "Once whatever process you use for releasing is finished, the tip of the branch is tagged with the version number."
- **Release Flow** (Microsoft Learn, ms.date 2022-07-18): 트렁크 기반 + 스프린트 단위 release branch. "Release branches never merge back to the main branch, so they might require *cherry-picking* important changes." / 핫픽스는 "The process always starts by making the change in `main` first." / "Fixing a bug in the release branch without bringing the change back to `main` would mean the bug would recur during the next deployment"
- **토픽 브랜치 vs 장기 브랜치** (Pro Git 2nd ed., 2014): "It's generally easier to think about them as work silos, where sets of commits graduate to a more stable silo when they're fully tested." / "A topic branch is a short-lived branch that you create and use for a single particular feature or related work. ... But in Git it's common to create, work on, merge, and delete branches several times a day."
- **Feature Toggles** (Pete Hodgson, martinfowler.com, 2017-10-09): 분류 Release / Experiment / Ops / Permissioning (수명·동적성 축). "Release Toggles allow incomplete and un-tested codepaths to be shipped to production as latent code which may never be turned on."

### 1.8 Merge Queue [웹]
- 정의: "A merge queue helps increase velocity by automating pull request merges into a busy branch and ensuring the branch is never broken by incompatible changes." (GitHub Docs, Managing a merge queue, 2026-09 조회)
- GA 문구: "ensuring each pull request queued for merging is tested with any other pull requests queued ahead of it." (Changelog 2023-07-12)
- 뿌리 — Not Rocket Science Rule (Graydon Hoare, 2014): "automatically maintain a repository of code that always passes all the tests" — ⚠ 2차 인용, Graydon 원문(403) 대조 필요.
- 동류 시스템: Uber SubmitQueue는 "solves the same problem as Github's 'merge queue' and GitLab's 'merge train' features." [웹] / GitLab은 같은 기능을 "merge trains"라 부르고 Premium 전용(커뮤니티 IshKebab 발언, **(확인 필요)**) [커뮤니티] / 계보: bors → GitHub merge queue·GitLab merge train(masklinn, HN 36707239) [커뮤니티]
- ⚠ 경고(papers): GitHub Merge Queue의 구현(임시 브랜치에 앞 PR을 누적해 테스트)은 SubmitQueue와 같지 않다. 개념의 계보로만 연결한다.

### 1.9 DORA 지표 [웹]
- 2026-01-05 갱신판 기준 **5개 지표**(throughput 3 + instability 2). MTTR은 Failed Deployment Recovery Time으로 대체.
  - Change Lead Time: "The amount of time it takes for a change to go from committed to version control to deployed in production."
  - Deployment Frequency: "The number of deployments over a given period or the time between deployments."
  - Failed Deployment Recovery Time: "The time it takes to recover from a deployment that fails and requires immediate intervention."
  - Change Fail Rate: "The ratio of deployments that require immediate intervention following a deployment."
  - Deployment Rework Rate: "The ratio of deployments that are unplanned but happen as a result of an incident in production."
- ⚠ 경고: 구 자료의 "4 key metrics / MTTR" 표기와 구분할 것. Accelerate(Forsgren·Humble·Kim, 2018, IT Revolution Press, ISBN 9781942788331)는 서지만 확인 — 본문 수치 미확인 [논문].

---

## 2. 핵심 관점들

### 2.1 코드 리뷰는 무엇을 위한 것인가 — "버그 그물"보다 "공동 이해"
- **결함 발견은 동기일 뿐, 실제 산출물은 개선·지식 전달** [논문] — Bacchelli & Bird 2013 (ICSE, Microsoft CodeFlow)
  - 코멘트 570개(200개 스레드) 분류: 코드 개선 165개(29%)가 최다, 결함은 78개(14%)로 9개 범주 중 4위. 결함 78개 중 65개가 로직 문제 (p.7, §V.A)
  - 결함 발견을 1순위 동기로 꼽은 개발자 383명(44%) (p.5). 설문 응답률 관리자 28%, 개발자 44% (p.4)
  - > "Review comments about defects are few, comprising one-eighth of the total in our sample, and mostly address 'micro' level and superficial concerns" (p.7, §V.B)
  - > "the most difficult thing when doing a code review is understanding the reason of the change" (인터뷰 인용, p.7, §VI.A) → PR 설명에 변경 이유를 써야 하는 근거
- **75:25 — 유지보수성 대 기능** [논문]
  - Mäntylä & Lassenius (TSE, 2009년 5월호; OpenAlex는 2008): "75 percent of defects found during the review do not affect the visible functionality of the software." (초록 기준)
  - Beller et al. 2014 (MSR): OSS 두 프로젝트, 리뷰 후 변경 1,400건 이상. 유지보수성:기능 = 75:25. 코멘트의 7~35%는 반영되지 않음, 변경의 10~22%는 명시적 코멘트 없이 일어남 (초록 기준)
- **Google은 리뷰를 가독성·유지보수성·교육 목적으로 도입** [논문] — Sadowski et al. 2018 (ICSE-SEIP): "Reviewing was introduced at Google to ensure code readability and maintainability." (p.5, Finding 1)
- **리뷰는 지식을 퍼뜨린다** [논문] — Rigby & Bird 2013 (ESEC/FSE): "Our knowledge sharing measure shows that conducting peer review increases the number of distinct files a developer knows about by 66% to 150% depending on the project." (초록)
- **리뷰 커버리지·참여도와 품질** [논문] — McIntosh et al. 2014 (MSR, Qt/VTK/ITK): "Low code review coverage and participation are estimated to produce components with up to two and five additional post-release defects respectively." (초록) → "리뷰 없는 머지 금지" 근거, 러버스탬프 = 참여도 부족
- 국내 관점 [웹]: 우아한테크세미나(백명석, 2022-04-19) "출시 전에 결함을 발견하는 것이 가장 중요한 목적이겠지만, 팀원들과 주고받는 피드백을 통해 상호 성장을 할 수 있는" (소개문)

### 2.2 PR 크기 — "작게"의 기준과 이유
- **Google 가이드** [웹] (eng-practices, 2019 공개)
  - "100 lines is usually a reasonable size for a CL, and 1000 lines is usually too large, but it's up to the judgment of your reviewer."
  - "A 200-line change in one file might be okay, but spread across 50 files it would usually be too large."
  - "It's easier for a reviewer to find five minutes several times to review small CLs than to set aside a 30 minute block to review one large CL."
- **Google 실측 기준점** [논문] — Sadowski et al. 2018 (p.6~7, §5, 변경 약 900만 건·2년 로그)
  - 첫 피드백까지 중앙값: 작은 변경 1시간 미만, 아주 큰 변경 약 5시간. 전체 리뷰 과정 중앙값 4시간 미만
  - 35% 이상이 파일 1개만 수정, 약 90%가 파일 10개 미만, 10% 이상이 코드 한 줄만 변경. 수정 줄 수 중앙값 24줄
  - 리뷰어 2명 이상인 변경은 25% 미만, 리뷰어 수 중앙값 1명. 80% 이상이 코멘트 해소를 최대 1회 반복
  - 개발자 1명이 주당 작성하는 변경 중앙값 약 3건, 리뷰 중앙값 4건. Critique 사용자 97% 만족 (p.7)
  - 비교(Rigby & Bird 2013 재인용): 승인까지 중앙값 AMD 17.5시간, Chrome OS 15.7시간, Microsoft 세 프로젝트 14.7/19.8/18.9시간
  - > "Code review at Google has converged to a process with markedly quicker reviews and smaller changes, compared to the other projects previously investigated. Moreover, one reviewer is often deemed as sufficient, compared to two in the other projects." (p.7, Finding 4)
  - ⚠ 경고(papers): Google의 monorepo·도구·가독성 인증 문화가 함께 있어서 나온 숫자라는 점을 같이 밝힌다.
- **큰 PR은 리뷰가 얕아진다** [논문] — Bosu, Greiler, Bird 2015 (MSR, Microsoft 코멘트 150만 개): "the more files that are in a change, the lower the proportion of comments in the code review that will be of value to the author of the change." 리뷰어 입사 첫해 유용 코멘트 비율 급상승 후 정체. (초록 기준)
- 크기-속도·효과 상충 연구는 §4.2.
- **커뮤니티 진단** [커뮤니티]: 큰 변경일수록 리뷰어 인지 부하 ↑ → "내일 볼게" 또는 대충 읽고 LGTM으로 양극화. 러버스탬프와 의무적 nitpick은 같은 뿌리 — 결정이 끝난 뒤, 평가하기엔 너무 큰 변경을 리뷰하기 때문(Dev.to "LGTM Culture"). SK DEVOCEAN: "변경 사항의 사이즈가 커서 리뷰하는 데 있어 확인해야 하는 범위가 크고 부담으로 다가온다."
- 국내 수치 [웹]: 맘시터(2022-08-05) PR은 대개 300줄 미만 — 요약 수치, **(확인 필요)**

### 2.3 리뷰 지연 — 병목은 사람의 주의와 "승인 후 머지 대기"
- **두 종류의 대기** [논문] — Kudrjavets et al. 2022b (MSR, Gerrit·Phabricator 약 50만 건): 제안→첫 응답, 승인→머지. 승인 후 머지 시간을 줄이면 Phabricator 리뷰가 29~63% 빨라질 수 있음. "Our analysis suggests that switching from manual to automatic merges can help increase code velocity." → auto-merge·merge queue 근거
- **Nudge (Microsoft)** [논문] — Maddila et al. (TOSEM, 2023; OpenAlex는 2022): 147개 저장소 무작위 시험, 기한 넘긴 PR 8,500건의 해결 시간 60% 감소, 알림의 73% 긍정 처리. 이후 8,000개 저장소로 확대, 1년간 알림 210,000건. (초록 기준)
- **Meta nudge — 꼬리가 체감을 결정** [논문] — Shan et al. 2022 (ESEC/FSE): 개발자 84.7%가 리뷰 체류 시간에 만족. 불만은 응답자 diff 리뷰 시간 75백분위, 즉 24시간을 넘기는 diff와 밀접. ⚠ 실험 결과 수치는 초록이 잘려 미확인.
- **리뷰 SLA** [커뮤니티]: 코멘토(2024-10-15) "업무일 1일 이내 리뷰", 전원 참여, 배포와 리뷰 분리. 해외에서도 "피드백 지연은 하루가 상한, 이상적으로 1시간"(steveberczuk substack). 국내 블로그 요지: "말투 문제로 보이는 갈등의 상당수는 사흘을 기다린 뒤 받은 지적이라서 크게 느껴지는 경우"(개인 블로그, 검증 필요)
- Dev.to Hasura 사례: PR 평균 7일, 일부 171.3시간 — 회사 블로그성 글, **(확인 필요)** [커뮤니티]

### 2.4 PR 수락·거절을 가르는 것
- Gousios et al. 2014 (ICSE, GHTorrent + 표본 291개 프로젝트) [논문]
  - 활성 저장소의 14%가 PR 사용 (p.6, 2012~2013 기준). ⚠ 경고: 2014년 GitHub 데이터이며 이후 PR 사용률은 크게 올랐다. **14%를 현재 수치로 쓰면 안 된다.**
  - 표본 PR의 84.73%가 결국 머지 (p.6). 80%가 3.7일, 90%가 10일, 95%가 26일 안에 머지, 30%는 1시간 안 (p.6)
  - 대부분 PR은 20줄 미만, 하루 안에 처리, 토론 평균 3개 코멘트 (p.7)
  - 머지 결정 최대 요인: PR이 최근 수정된 코드를 건드리는지 (p.8)
  - 거절 사유: 동시 수정(obsolete·conflict·superseded) 27%, 구현 오류 13%, 분산 개발 특성·소통 문제 53% (p.9)
  - > "only 13% of the contributions are rejected due to technical issues, which is the primary reason for code reviewing, while a total 53% are rejected for reasons having to do with the distributed nature of the pull request process (concurrent modifications) or the way projects handle communication of project goals and practices." (p.9, §8)
- Gousios et al. 2015 (ICSE): 통합자 749명 설문 — 품질 유지와 기여 우선순위 결정이 가장 어려움 [논문]
- Tsay, Dabbish, Herbsleb 2014 (ICSE): "Pull requests with many comments were much less likely to be accepted, moderated by the submitter's prior interaction in the project." 자리 잡은 프로젝트일수록 보수적 [논문]

### 2.5 CI의 효과 — 속도보다 "안심"과 "판단"
- Vasilescu et al. 2015 (ESEC/FSE, Travis CI 도입 프로젝트 246개) [논문]
  - 코어 개발자 머지 PR 수 +20.5%, 거절 PR -42.3%, 외부 기여자 거절 PR -26% (p.9)
  - 코어 개발자 보고 버그 +48% (저자 해석: 내부에서 버그를 더 찾게 됨). 외부 기여자 버그 보고 수 영향 없음
  - > "Our main finding is that continuous integration improves the productivity of project teams, who can integrate more outside contributions, without an observable diminishment in code quality."
- Hilton et al. 2016 (ASE, 프로젝트 34,544개, Travis 빌드 1,529,291건, 설문 442명·응답률 9.8%) [논문]
  - CI 사용 40%, 별 수 최상위 그룹 70%, 인기 낮을수록 23% (p.3~4)
  - 릴리스: CI 월 0.54회 vs 비CI 0.24회, 같은 프로젝트 도입 전 0.34회 (p.7). > "Projects that use CI release more than twice as often as those that do not use CI."
  - PR 수락 시간 중앙값: CI 정보 있으면 5.2시간, 없으면 6.8시간 → 1.6시간 빠름 (p.8)
  - 평균 빌드 시간 500초가 조금 안 됨 (p.7)
  - 안 쓰는 이유 1위 "팀원이 CI에 익숙하지 않음"(47.00%), 2위 "자동화 테스트가 없음"(44.12%) (Table 4). 쓰는 이유 1위 "빌드가 깨질 걱정이 줄어서"(87.71%), 2위 "버그를 더 일찍 잡아서"(79.61%) (Table 6)
  - > "CI is not widely perceived as helpful with debugging." (p.7)
  - ⚠ 경고: Travis CI 시대 데이터. 현재 GitHub Actions 환경과 수치가 다를 수 있다.
- Hilton et al. 2017 (ESEC/FSE): CI 트레이드오프 세 축 — Assurance(속도↔확실성), Security(접근성↔정보 보안), Flexibility(설정 옵션↔사용 편의) [논문] → PR 단계 vs 머지 후/야간 배치의 틀
- 상충 연구(Bernardo 2018/2023)는 §4.3.
- Zhao et al. 2017 (ASE): CI 도입 후 커밋·이슈·테스트 관행 적응이 이전 연구보다 미묘 (초록, 세부 수치 미수집) [논문]
- 서베이: Soares et al. 2022 (EMSE, 479편 중 실증 101편, 6주제), Shahin et al. 2017 (IEEE Access, 2004~2016 논문 69편, 접근법·도구 30개) [논문]

### 2.6 테스트 계층화 — PR은 빠르게, 머지 후는 넓게
- Microsoft (Release Flow) [웹]
  - "The first- and second-level test suites run around 60,000 tests in less than five minutes."
  - "Some teams have several hundred developers working constantly in a single repository, who can complete over 200 pull requests into the main branch per day."
  - "Currently, a product with 200+ pull requests might produce 300+ continuous integration builds per day, amounting to 500+ test runs every 24 hours."
- Mergify two-step CI (요지) [웹]: PR에는 lint·unit 등 가벼운 검사, 큐 진입 시에만 통합·E2E 등 비싼 검사.
- 대규모의 한계 — Memon et al. 2017 (ICSE-SEIP, Google TAP) [논문]
  - TAP은 하루 평균 13,000개 이상 프로젝트 통합·테스트, 빌드 80만 건, 테스트 실행 1억 5천만 건 (p.1)
  - 커밋 평균 초당 1건. 변경마다 따로 테스트는 비용 대비 효과 없어 약 45분(피크 시간)마다 "마일스톤"으로 묶어 실행 (p.1)
  - 영향 테스트 대상 550만 개 중 91.3%는 한 번도 실패하지 않음, 통과·실패 모두 겪은 것 2.07%, flaky 걸러 내면 실제 결함 발견 1.23% (p.4)
  - 여러 사람이 여러 번 수정한 단일 파일은 거의 100% 실패를 일으킴 (p.3)
- 선택 실행 — Machalica et al. 2019 (ICSE-SEIP, Meta Predictive Test Selection): 변경 테스트 인프라 비용 절반, 개별 테스트 실패의 95% 이상·결함 있는 변경의 99.9% 이상 보고 (초록 기준) [논문] → 일반 팀엔 경로 필터·영향 분석이 축소판

### 2.7 Flaky test
- **Google 블로그 수치** [웹] — John Micco 2016-05-27 / Jeff Listfield 2017-04-17
  - 요지(2차 인용): "about 1.5% of all test runs reporting a 'flaky' result", "almost 16% of our tests have some level of flakiness", "84% of the transitions we observe from pass to fail involve a flaky test". 2017 글: 테스트 크기(바이너리 크기)가 클수록 flaky 확률이 높다는 상관.
  - ⚠ 경고: 원문 본문(스크립트 렌더) 직접 추출 실패. **fact-checker가 브라우저로 원문 대조 필수 (사실 확인 필요).**
- **Luo et al. 2014** (FSE, Apache 51개 프로젝트, flaky 수정 커밋 201건) [논문]
  - 근본 원인 상위 3: Async Wait 45%(161건 중 74건), Concurrency 20%(32건), Test Order Dependency 12%(19건) (p.4~5)
  - 78%는 처음 작성될 때부터 flaky, 96%는 플랫폼 무관 (p.2). Async Wait flaky 중 54%는 waitFor로 수정 (p.2)
  - Google TAP 재인용: 하루 평균 테스트 실패 160만 건 중 7.3만 건(4.56%)이 flaky 때문. 실패 테스트를 같은 코드에 10번 다시 돌려 한 번이라도 통과하면 flaky로 분류 (p.1)
  - > "if a flaky test fails frequently, developers tend to ignore its failures and, thus, could miss real bugs." (p.1, §1)
  - ⚠ 경고(합성): Google 블로그의 1.5%(전체 실행 중 flaky 결과 비율)와 Luo의 4.56%(실패 중 flaky 비율)는 분모가 다른 수치다. 합치거나 한 문장에서 비교하지 말 것.
- Memon 2017: > "it is impossible to weed out all flaky tests" (p.2, §I) [논문]
- Parry et al. 2021 (TOSEM 서베이, 76편): 원인·비용·탐지·완화 4축. 초록은 개발자 59%가 월·주·일 단위로 flaky를 다룬다는 선행 설문 인용(원 설문 출처 미확인). 후속 Parry et al. 2022 (ICSE-SEIP, 응답 170건 + SO 스레드 38개): flaky를 자주 겪을수록 진짜 실패를 무시할 가능성↑, 원인 1위 인식은 setup/teardown [논문]
- Henderson et al. 2023 (ICST, Google Flake Aware Culprit Finding): flaky 잡음 속 범인 커밋을 베이즈 추론·잡음 있는 이진 탐색으로. 테스트 파손 13,000건 이상 평가 → 배치 머지의 범인 찾기 비용과 연결 [논문]
- **커뮤니티 목소리** [커뮤니티]
  - smarterclayton (HN 23493249, 2020-06): "once anyone anywhere thinks 'oh it's just flaky' they stop treating it like signal. Once they treat it like noise, it's very hard to unwind"
  - hinkley: "your one bad test is going to fail every week or two...now builds are failing 2x a day on average"
  - l0b0: "nobody even bothers checking whether it's a 'real' failure until it's failed a few times in a row"
  - HN 47024638 (2026-02경) 본문: "Every retry rule in your CI pipeline is a painkiller." / "Retries, quarantining, adding waits - these aren't fixes."
  - Canva CI 스레드(HN 42429601, 2024-12-18): dan_sbl flaky는 "should have been addressed first, not last."; nijave "flakey/slow/expensive CI is also an orange/red flag you're lacking in developer experience/productivity."
  - 머지 큐에서는 flaky 하나가 그룹 전체를 떨어뜨려 고통이 증폭(Discussion #168145) [오귀속 — 실제는 트리거 중복·상호 취소 (13장 fact-check 확인)]

### 2.8 GitHub Actions 상세 (전부 [웹], GitHub Docs 2026-09 조회 기준 — ⚠ 한도·플랜 수치는 자주 바뀜)
- **한도**
  - "Each job in a workflow can run for up to 6 hours of execution time." (GitHub-hosted)
  - 워크플로 런 최대 "35 days / workflow run"
  - "A job matrix can generate a maximum of 256 jobs per workflow run."
  - (self-hosted) "A job can be in the queue for 24 hours before it is automatically cancelled."
  - 동시 잡: Free 20 / Pro 40 / Team 60 / Enterprise 500 (larger runners 1,000)
  - "The rate limit for `GITHUB_TOKEN` is 1,000 requests per hour per repository" (Enterprise Cloud 15,000)
  - 저장 한도(저장소당): Free 500 MB artifacts / Pro 1 GB / Team 2 GB / Enterprise Cloud 50 GB, cache 10 GB
  - "The `branches`, `branches-ignore`, `tags`, and `tags-ignore` keywords accept glob patterns."
  - permissions 키: actions, artifact-metadata, attestations, checks, code-quality, contents, deployments, discussions, id-token, issues, packages, pages, pull-requests, security-events, statuses, vulnerability-alerts
- **트리거**
  - pull_request(fork): "With the exception of `GITHUB_TOKEN`, secrets are not passed to the runner when a workflow is triggered from a forked repository. The `GITHUB_TOKEN` has read-only permissions in pull requests from forked repositories."
  - pull_request_target: "Running untrusted code on the `pull_request_target` trigger may lead to security vulnerabilities. These vulnerabilities include cache poisoning and granting unintended access to write privileges or secrets."
  - merge_group: 활동 유형은 `checks_requested` 하나. "if your repository uses GitHub Actions to perform required checks on pull requests in your repository, you need to update the workflows to include the `merge_group` event as an additional trigger."
  - workflow_run: "The workflow started by the `workflow_run` event is able to access secrets and write tokens, even if the previous workflow was not."
  - schedule 예시: 토스의 평일 오후 2시 미리뷰 PR 리마인더(cron) (§3)
- **캐시**
  - "By default, the limit is 10 GB per repository, but this limit can be increased by enterprise owners, organization owners, or repository administrators." 10 GB 초과분 유료 확장 가능 — 최대치 "up to 10 TB"는 요약상 표현, **(확인 필요)**
  - "GitHub will remove any cache entries that have not been accessed in over 7 days."
  - 스코프: "Workflow runs can restore caches created in either the current branch or the default branch (usually `main`). If a workflow run is triggered for a pull request, it can also restore caches created in the base branch." / "Workflow runs cannot restore caches created for child branches or sibling branches."
  - 매칭 순서: key 정확 일치 → key 부분 일치 → restore-keys 순차 부분 일치
- **Artifacts**: 2025-01-30부터 upload/download-artifact v3 사용 불가("Starting January 30th, 2025, GitHub Actions customers will no longer be able to use v3 of actions/upload-artifact or actions/download-artifact."). v4 "uploads are significantly faster, upwards of 90% improvement in worst case scenarios." / "Each job in a workflow run now has a limit of 500 artifacts." (Changelog 2024-04-16, 검색 결과 발췌) ⚠ 경고: v4/2024 기준. **2026 현재 최신 메이저 버전(v5 이상 여부) 미확인 — 구버전 정보일 수 있음.**
- **재사용: reusable workflow vs composite action**
  - "For a workflow to be reusable, the values for `on` must include `workflow_call`"
  - "Workflows that call reusable workflows in the same organization or enterprise can use the `inherit` keyword to implicitly pass the secrets."
  - "Unlike when you are using actions within a workflow, you call reusable workflows directly within a job, and not from within job steps."
  - "You can connect a maximum of ten levels of workflows - that is, the top-level caller workflow and up to nine levels of reusable workflows." / "Loops in the workflow tree are not permitted."
  - 비교: reusable은 "Can contain multiple jobs", 러너 지정 가능, 스텝별 실시간 로깅 / composite는 "Run as a step within a job", "Logged as one step even if it contains multiple steps", "Can be nested to have up to 10 composite actions in one workflow", Marketplace 게시 가능
  - ⚠ 경고: 요약 모델이 composite를 "Cannot use secrets"로 옮겼으나 정확히는 secrets 컨텍스트를 직접 받지 못하고 inputs로 전달받아야 한다는 뜻 — 원문 대조 필요.
  - ⚠ 경고: 과거 Docs의 "워크플로 파일당 고유 reusable workflow 최대 N개"(20→50 변경 이력) 한도는 이번 조회에서 확인 못 함 — **수치 쓰지 말거나 재확인.**
- **Concurrency**
  - "When you limit concurrency, by default only one run can be pending in a concurrency group—any additional pending runs cancel the previous one."
  - 2026-05-07 Changelog: "`queue` property accepts the following values: `single` (default)...`max`: Up to 100 jobs or workflow runs can be `pending` in the concurrency group."
  - "The combination of `queue: max` and `cancel-in-progress: true` is not allowed and will result in a workflow validation error."
  - 예시: `group: ${{ github.head_ref || github.run_id }}` + `cancel-in-progress: true`
  - ⚠ 경고: queue 옵션은 2026-05 신기능. 구버전 자료("항상 1개 대기만 가능")와 충돌 주의.
- **Environments**
  - "You can list up to six users or teams as reviewers."
  - "users who initiate a deployment cannot approve the deployment job, even if they are a required reviewer." (prevent self-review)
  - Wait timer: "The time (in minutes) must be an integer between 1 and 43,200 (30 days)."
  - "A maximum of 6 deployment protection rules can be enabled on any environment at the same time."
  - "a job cannot access environment secrets until one of the required reviewers approves it."
  - 플랜: required reviewers·wait timer는 Free/Pro/Team에서는 public 저장소만.
- **OIDC**
  - "OpenID Connect allows your workflows to exchange short-lived tokens directly from your cloud provider." / "You won't need to duplicate your cloud credentials as long-lived GitHub secrets." / "With OIDC, your cloud provider issues a short-lived access token that is only valid for a single job, and then automatically expires."
  - subject 예: `repo:octo-org/octo-repo:environment:prod`, `repo:my-org/my-repo:ref:refs/heads/main`
  - ⚠ 경고: `permissions: id-token: write` 요구 문장은 직접 확보 못 함(permissions 목록에 id-token 존재). 클라우드별 how-to로 확인.
- **가격** (Changelog 2025-12-16 + 이후 연기 공지)
  - 2026-01-01 GitHub-hosted runner 가격 최대 39% 인하
  - self-hosted runner 분당 $0.002 플랫폼 요금(2026-03-01 예정)은 반발 후 연기: "We're postponing the announced billing change for self-hosted GitHub Actions to take time to re-evaluate our approach."
  - community: 이틀 만에 연기, "2026년 중반 기준 미시행, 재도입 일정 미발표" [커뮤니티, **(확인 필요)**]
  - ⚠ 경고: self-hosted 요금 재도입 여부 집필 시점 재확인.
- **실증 연구** [논문]
  - 채택률 — ⚠ 시점별로 다름, 섞지 말 것: Kinsman et al. 2021 (MSR) 저장소 416,266개 중 3,190개(0.7%) — **Actions 출시 초기(2020년 무렵) 수치, 현재 채택률로 쓰면 안 된다.** Wessel et al. 2023 (EMSE) 인기 저장소 5,000개 중 1,489개(약 30%). Decan et al. 2022 (ICSME) 약 68K개 저장소 중 43.9%. Golzadeh et al. 2022 (SANER) npm 저장소 91,810개 9년 추적 — Actions가 18개월이 안 돼 지배적 CI, Travis 감소.
  - Kinsman 2021: 사용 Action 708개 중 42개(5.93%)만 verified. > "After adopting GitHub Actions, on average, there are more rejected pull requests and fewer commits on merged pull requests." (p.8)
  - Wessel 2023: 도입 후 PR 거절 증가, 승인 PR은 대화↑·커밋↓, 거절 PR은 대화↓·커밋↑, 승인까지 시간 증가 → 필수 검사를 가려 설계
  - Bouzenia & Pradel 2024 (ICSE): 유료 저장소 평균 연 $504. 자원의 91.2%가 테스트·빌드. 트리거별 PR 50.7%, push 30.9%, 스케줄 15.5%. 캐시를 쓴 유료 저장소 32.9%. 비활성 저장소 스케줄 끄기만으로 실행 시간 1.1~31.6% 절감 가능
  - Valenzuela-Toledo et al. 2024 (SCAM, 약 200개 프로젝트): 워크플로도 유지보수해야 하는 코드("hidden costs of automation")
  - Rostami Mazrae et al. 2026 (arXiv:2602.14572, 게재 미확인): 저장소 49K개 이상, 워크플로 변경 267K개 이상, 파일 버전 3.4M개 이상(2019-11~2025-08). 저장소당 워크플로 파일 중앙값 3개, 7.3%가 매주 바뀜, 변경의 약 3/4은 단일 변경. LLM 도구 영향의 결정적 증거 없음
  - Saroar & Nayebi 2023 (EASE, 90명 설문): 60.87%가 YAML 작성이 어렵고 오류 나기 쉽다고 응답. 논문 시점 Marketplace Action 16,730개
- **커뮤니티 불만: 피드백 루프** [커뮤니티]
  - woodruffw (HN 46614558, 2026-01경): "the lack of a tight feedback loop. Pushing and waiting for completion on what's often a very simple failure mode is frustrating."
  - modeless: "It's insane to me that being able to run CI steps locally is not the first priority of every CI system."
  - danpalmer(act): "you have to make a lot of decisions to support Act. It in no way 'just works'"
  - yorickpeterse (Lobsters, 2026-02-05 Ian Duncan 글): "there's no sensible way of testing (or even linting) GitHub's CI config locally."
  - Riolku: "The back button in the GitHub Actions UI is a roulette wheel. You will land somewhere. It will not be where you wanted to go."
  - sebastien: "most CIs are fine if you just use them to bootstrap into your build system. I typically use make and nix or mise"
  - tracking1: "The less I rely on Github Actions environment the happier I am"
- **모노레포 경로 필터 + 필수 체크 함정** [커뮤니티] — Discussion #13690 (2022-03-28 개설, 👍101): `paths` 필터 워크플로를 필수 체크로 지정하면 해당 경로를 안 건드린 PR은 체크가 영원히 "대기 중" → 머지 불가. joegaudet (2022-11-03) "we've been asking for it for 3 years now, the only way to safely protect branches in this scenario is to run all checks always." / joshuat (2026-08-10) "...routinely one of the reasons I look at moving us away from GH Actions." 동류 #26251, #44490, #177835.
- **CI 대기와 캐시** [커뮤니티] — 뱅크샐러드(2022-08-29): "하나의 action이 3분이 걸린다면 20명의 동료들이 한 번씩만 사용한다고 하더라도 1시간이 허비될 수 있습니다", 의존성 설치 1분 8초 → 21초, 전체 CI 약 40초. 셀프호스트 러너 캐시 느림(Discussion #18549). 벤더 벤치마크 수치는 신뢰도 낮음.

### 2.9 GitHub Actions 보안 하드닝
- **Secure use reference 뼈대** [웹]
  - "Pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release."
  - "Pinning to a particular SHA helps mitigate the risk of a bad actor adding a backdoor to the action's repository, as they would need to generate a SHA-1 collision for a valid Git object payload."
  - "It's good security practice to set the default permission for the `GITHUB_TOKEN` to read access only for repository contents. The permissions can then be increased, as required, for individual jobs within the workflow file."
  - "For inline scripts, the preferred approach to handling untrusted input is to set the value of the expression to an intermediate environment variable."
  - "Workflows that use these triggers must not explicitly check out untrusted code, including from pull request forks or from repositories that are not under your control."
  - "Self-hosted runners should almost never be used for public repositories on GitHub, because any user can open pull requests against the repository and compromise the environment."
- **pwn request** [웹] — GitHub Security Lab, Jaroslav Lobačevski, 2021-08-03
  - "Workflows triggered via `pull_request_target` have write permission to the target repository. They also have access to target repository secrets."
  - "Combining `pull_request_target` workflow trigger with an explicit checkout of an untrusted PR is a dangerous practice that may lead to repository compromise."
  - "They may submit malicious changes to the existing build scripts like `make` or `powershell` files or redefine the build script in the `package.json` file."
  - 권장 패턴: "The workflow processing the PR should then store any results like code coverage or failed/passed tests in artifacts and exit. The following workflow then starts on `workflow_run` where it is granted write permission to the target repository."
- **pull_request_target 동작 변경** [웹] — 2025-11-07 공지, 2025-12-08 시행 (검색 결과 발췌, 원문 대조 권장)
  - "The workflow file and checkout commit will always be taken from the repository's default branch, regardless of the pull request's base branch."
  - "GITHUB_REF for pull_request_target will resolve to the default branch, and GITHUB_SHA will point to the latest commit on that branch."
  - "Historically, this behavior has led to the exploitation of outdated workflows that contained vulnerabilities in pull_request_target workflows that were presumed to be remediated since they were fixed in the default branch."
  - ⚠ 경고: 2025-12-08 이후 동작. 2021 Security Lab 등 이전 자료의 서술과 달라진 점 명시할 것.
- **GITHUB_TOKEN 기본 read-only** [웹] — Changelog 2023-02-02: 신규 엔터프라이즈·조직·개인 저장소의 기본 권한이 read-only로. 기존 것은 영향 없음 → 오래된 조직은 여전히 read/write일 수 있음(점검 포인트).
- **Actions policy — SHA 고정 강제·차단** [웹] — Changelog 2025-08-15: 허용 액션 정책에 full SHA 고정 강제 체크박스(고정 안 된 액션 쓰는 워크플로는 실패), `!owner/action` 접두로 특정 액션 차단. tj-actions 사건 대응.
- **Immutable releases GA** [웹] — Changelog 2025-10-28: 자산 추가·수정·삭제 불가, 태그 삭제·이동 불가, 서명된 attestation 발급. ⚠ "immutable actions"의 별도 출시 상태는 미확인.
- **정량 근거** [논문]
  - Koishybayev et al. 2022 (USENIX Security, 저장소 213,854개·워크플로 447,238개): > "Our analysis shows that 99.8% of workflows are overprivileged and have read-write access (instead of read-only) to the repository." 23.7%는 pull_request로 트리거되며 저장소 코드 사용. 저장소의 99.7%가 외부 Action 실행, 97%는 비verified 제작자 Action 하나 이상, 18%는 보안 업데이트 빠진 Action 실행. pull_request_target: 저장소 7,485개(3.5%), 워크플로 8,874개(1.9%) (p.9, Table 4)
    - ⚠ 경고(합성): 이 99.8%는 2022년 논문 수치로, 2023-02 기본 read-only 전환 이전 데이터다. 현재 비율로 쓰지 말 것.
  - ARGUS (Muralee et al. 2023, USENIX Security): 워크플로 2,778,483개·Action 31,725개 분석, 워크플로 4,307개·Action 80개에서 치명적 코드 주입 취약점. 기존 패턴 스캐너 대비 발견율 7배 이상. > "command injection vulnerabilities in the GitHub Actions ecosystem are not only pervasive but also require taint analysis to be detected." → `${{ github.event.pull_request.title }}`를 run에 바로 넣지 말고 환경 변수로
  - Benedetti et al. 2022 (SCORED, GHAST): 오픈소스 50개에서 보안 이슈 24,905건
- **커뮤니티: 공급망 불신** [커뮤니티] — cookiengineer (HN 43419701) "the GitHub Actions CVE from August 2024 was the final nail in the coffin". 2025 하반기 Shai Hulud v2·GhostAction 언급 **(확인 필요 — 1차 소스 미확보)**. 2026-06 Claude Code GitHub Action 결함으로 악성 이슈 하나가 저장소를 탈취할 수 있었다는 보도(The Hacker News) — AI 에이전트 액션의 프롬프트 인젝션이라는 새 표면 **(확인 필요)**

### 2.10 브랜치 전략 — 이론 축은 "통합 빈도"
- **Fowler** [웹] (Patterns for Managing Source Code Branches, 2020-05-28)
  - "Frequent integration increases the frequency of merges but reduces their complexity and risk."
  - "The smaller the integrations, the less likely they are to turn into an epic merge of misery and despair."
  - "Continuous Integration allows a team to get the benefits of high-frequency integration, while decoupling feature length from integration frequency."
  - "Release branches are a valuable tool when a team isn't able to keep their mainline in a healthy state."
  - "Environment branches are an example of using source branching as a poor man's modular architecture." (GitLab Flow 환경 브랜치 비판)
  - "Overall I much prefer to work on a team that uses Continuous Integration."
- **브랜치는 지연이라는 세금** [논문] — Bird & Zimmermann 2012 (FSE, Windows): 최대 문제로 꼽힌 것은 브랜치가 너무 많아 변경이 팀 사이를 오가는 데 오래 걸리는 것("branchmania"). > "By removing high-cost-low-benefit branches in Windows based on our what-if analysis, changes would each have saved 8.9 days of delay and only introduced 0.04 additional conflicts on average."
- **브랜치 구조 ↔ 조직 구조** [논문] — Shihab, Bird, Zimmermann 2012 (ESEM, Vista·Win7): > "misalignment of branching structure and organizational structure is associated with higher post-release failure rates."
- **머지 충돌** [논문]
  - Ghiotto et al. (TSE, 온라인 2018 / 권호 2020, Java 2,731개): > "it has been reported that as much as 10 to 20 percent of all merge attempts result in a merge conflict" — ⚠ 경고: 10~20%는 선행 연구에서 가져온 수치. **책에서는 "선행 연구에 따르면(Ghiotto et al. 재인용)"으로 쓴다.**
  - McKee et al. 2017 (ICSME): 실무자 10명 인터뷰 + 162명 설문 — 충돌 코드의 체감 복잡도에 따라 해결 시점·방법을 바꿈
  - Brun et al. 2011 (ESEC/FSE): 충돌 조기 감지 → 자주 통합해야 하는 근거
  - Xu et al. 2026 (arXiv:2607.04697, **동료 심사 미확인 프리프린트**): AIDev-pop(PR 33,596건, 저장소 2,807개). 시간이 정확히 겹치는 기준 저장소의 40.2%에 동시 열린 에이전트 PR 쌍. 3-way 머지 재현 시 텍스트 충돌률 다른 에이전트끼리 41.7%, 같은 에이전트끼리 19.8%.
- **Feature flag도 부채** [웹][논문]
  - Hodgson: "Savvy teams view the Feature Toggles in their codebase as inventory which comes with a carrying cost and seek to keep that inventory as low as possible."
  - Rahman et al. 2016 (MSR, Chrome 릴리스 39개·5년): 토글은 빠른 릴리스와 장기 기능 개발 병행을 가능하게 하지만 기술 부채·유지보수 부담
- Monorepo 1차 출처 후보: Potvin & Levenberg 2016 (CACM) — ⚠ 메타데이터만 확인, 본문 수치 인용 전 원문 대조.
- 트렁크 기반 vs GitFlow를 직접 비교한 실증 논문은 없음(§7).

### 2.11 Merge Queue — 작동 방식과 설정
- **왜 필요한가**: 각 PR은 초록인데 합치면 main이 빨개지는 "merge race". Shopify 2018: "Occasionally, master merges can go wrong. For example, two unrelated merges can affect one another, the introduction of a new flaky test, or even accidental merges of work in progress." [웹] / byroot (Lobsters 2026-07-27): "Merge Queues don't replace CI, they're mostly a solution to merge races on project with a high throughput." [커뮤니티]
- **GitHub 설정** [웹] (GitHub Docs, 2026-09 조회)
  - 워크플로 트리거: `on: pull_request: merge_group:`
  - Build concurrency: "The maximum number of `merge_group` webhooks to dispatch (between `1` and `100`), throttling the total amount of concurrent CI builds."
  - Merge limits: "Select the minimum and maximum number of pull requests to merge into the base branch at the same time (between `1` and `100`), and a timeout"
  - Status check timeout: "Choose how long the queue should wait for a response from CI before assuming that checks have failed."
  - "Only merge non-failing pull requests" — 그룹 내 앞 PR이 실패해도 마지막 PR이 통과하면 함께 머지할지 결정하는 토글
  - "If there are failed required status checks or conflicts with the base branch, the pull request will be removed from the queue."
  - "jumping to the top of a merge queue will cause a full rebuild of all in-progress pull requests." / "Jumping to the front of the queue is now only available to admins by default" (GA Changelog)
  - 서드파티 CI는 "gh-readonly-queue/{base_branch}" 접두 브랜치 push에 반응하도록 설정(임시 브랜치는 PR과 다른 SHA). merge_group 트리거가 없으면 "status checks will not be triggered when you add a pull request to a merge queue. The merge will fail as the required status check will not be reported." (검색 발췌)
  - 제거 사유: "Configured CI service is reporting test failures for a merge group," "Timed out awaiting a successful CI result," "User requesting a removal via the API or merge queue interface," "Branch protection failure that could not automatically be resolved."
  - ⚠ 경고: **기본값(예: build concurrency 5, 최소 그룹 1/최대 5, 대기 5분, 타임아웃 60분)은 공식 확인되지 않음 — 본문에 기본값을 쓰려면 UI/원문 재확인 필수.** 범위(1~100)만 확인된 사실.
- **가용 범위** [웹]: GA(2023-07-12) 시 Enterprise Cloud의 private/public 저장소 + 조직 소유의 모든 public 저장소. public beta 2023-02-08. ⚠ 경고: **2026-09 현재 Team 플랜 private 저장소 지원 여부는 공식 확인 못 함** — 커뮤니티 요청 토론(Discussion #201908)이 남아 있어 여전히 미지원으로 보이나 fact-checker 확인 필요.
- **배치와 실패 격리** [웹] — Mergify 문서
  - "If a batch fails, all subsequent batches are deemed to fail as well, are canceled and put back into the queue. The system splits the failed batch to isolate the problematic pull request."
  - "If a batch contains only one pull request and still fails, it is deemed to be the culprit and is removed from the queue."
  - `batch_max_wait_time`으로 배치가 찰 때까지 대기
- **투기 실행의 학술 원형 — Uber SubmitQueue** [논문] — Ananthanarayanan et al. 2019 (EuroSys). ⚠ **논문 PDF 원문 미확보(ACM 403)** — "슬라이드"는 저자 1차 자료, "TMP"는 The Morning Paper(2019-04-18) 2차 인용.
  - 구성: speculation tree(성공·충돌 확률 예측 후 가치 있는 빌드만 투기 실행), conflict analyzer(빌드 그래프로 독립 변경을 병렬 커밋), planner
  - 동시 변경 수가 늘면 충돌 확률 5%→40% (슬라이드 p.10). TMP는 "16개 동시 변경에서 40%"
  - 단순 직렬 큐는 하루 수천 건에서 확장 안 됨 (슬라이드 p.17). TMP: 하루 1,000건, 변경당 30분이면 마지막 변경 대기 20일 초과
  - 모두 투기 실행하면 변경 n개에 2^n개 빌드 (슬라이드 p.26)
  - 로지스틱 회귀, 수작업 특성 100개 이상, 예측 정확도 97% (슬라이드 p.36). 변경의 7.9%만 빌드 그래프 변경 (p.48)
  - 모두 투기 실행은 Oracle보다 최대 15배 느림, SubmitQueue P99 대기는 극단적 경합에서도 4배 수준, conflict analyzer는 Oracle 대기를 최대 50% 단축 (p.52, 56, 57)
  - 도입 전 iOS main은 일주일 표본에서 52%의 시간만 초록, 도입 후 1년 넘게 항상 초록 — **TMP 인용, 원문 페이지 미확인.** ⚠ 경고: fact-checker는 원문과 대조하거나 "Uber 보고에 따르면"으로 완화할 것.
  - 후속(블로그, 2023-08-31, BLRD): "After enabling BLRD in the SubmitQueue for Uber's Go monorepo in late May 2023, the P95 wait time of June is 74% less than that of April." [웹]
- **처리량 산식** [커뮤니티]: danlucraft (Discussion #14801, 2022-07-20) "queue with 8 PRs, that is going to take 2 hours to clear because our build takes 30 mins and the 2-build limit" → 빌드 시간 × 동시 빌드 한도 = 큐 처리량

---

## 3. 대표 사례

### 3.1 Merge Queue 도입 사례 [웹]
- **GitHub 자체** (Will Smythe, Lawrence Gripper, 2024-03-06)
  - 이전 "train" 방식: "A train was a special pull request that grouped together multiple pull requests (passengers)" — 최대 15개 PR 묶음, "wait 8+ hours after joining a train for it to ship, only for it to be removed due to a conflict"
  - "Over 500 engineers merge 2,500 pull requests into our large monorepo with merge queue" — ⚠ 경고: **기간 표현은 원문 대조 필요 — 월 단위로 알려짐.** "월 2,500건"으로 단정하지 말 것.
  - "30,000+ pull requests with their associated 4.5 million CI runs"
  - "The average wait time to ship a change has also been reduced by 33%"
  - 모놀리식 저장소에서 30개 이상 동시 배포 가능
  - "one of the best quality-of-life improvements to shipping changes that I've seen at GitHub!"
- **Block Inc.** (GA 블로그, Jon Graves): "We would routinely experience post-merge build failures in our monorepo several times a week and merge queue has practically eliminated all build failures in that category."
- **Shopify**
  - 2018 (Darren Worrall, 2018-06-08): Shipit 배포 도구에 merge queue 내장. "Over 90% of pull requests to Shopify's core application are using Shipit with the merge queue!"
  - 2019 v2 (Jack Li, 2019-11-14): "a 'predictive branch,' implemented as a git branch, onto which pull requests are merged, and CI is run." / "a batch size of 8 as a balance between throughput and risk" / 3개 배치 분량 동시 CI, flaky 대응 실패 허용 임계값, `/shipit --emergency` 긴급 머지. 1000+ 개발자, 일 약 400 커밋, 하루 40회 배포. 원칙: "Master must always be green (passing CI)", "Master must stay close to production", "Emergency merges must be fast"
  - Graphite 고객 사례(벤더, 날짜 미확인, URL `https://graphite.com/customer/shopify-merge-queu` 원문 그대로): Graphite Merge Queue로 대기 "hours to minutes" — **본문 미확인, (확인 필요)**
- **bors 종료** (2023-04-30): "As the primary maintainer, I officially declare Bors-NG to be feature frozen and deprecated. The public instance will remain running for awhile, but it will eventually start emitting warnings and be taken down." 종료 사유는 GitHub 네이티브 merge queue 공개. Rust 프로젝트의 자체 후속 bors 운영은 **(확인 필요)**
- 긍정 경험담 [커뮤니티]: elijahpotter (Lobsters, 2026-07-27) "the switch to merge queues was an enormous improvement in quality of life for both reviewers and PR authors."; zabil (HN 36707239, 2023-07-13) "We've been using this for a few months … for our mono repo. It's greatly improved the merge process."

### 3.2 머지 큐가 머지된 코드를 조용히 되돌린 날 (2026-04-23) [커뮤니티, 공식 대조 필요]
- GitHub 머지 큐에서 **squash 방식 + 머지 그룹에 PR 2개 이상**일 때 잘못된 머지 커밋이 생성되어, 앞서 머지된 PR의 변경이 뒤 PR 머지로 되돌려짐. 16:05~20:43 UTC.
- 원인(GitHub 설명): 미공개 기능용 새 머지 베이스 계산 경로가 feature flag 게이팅 누락으로 squash 머지 그룹에 적용됨. merge/rebase 방식 그룹과 머지 큐 밖 PR은 영향 없음. 커밋 자체는 Git에 남아 데이터 손실은 없었다고 GitHub 설명.
- 인시던트 스레드: https://github.com/orgs/community/discussions/193645
- ⚠ **영향 규모 수치 불일치 — 합치지 말 것**
  - 관점 A: 인시던트 요약 "658 repositories, 2,092 PRs" (초기 230 repo에서 상향)
  - 관점 B: HN에서 인용된 Kyle Daigle 발언 "2,804 PRs out of over 4 million merged on April 23"
  - 두 수치 모두 공식 1차 원문 미대조. 본문에서는 출처를 명시해 병기하거나, 수치 없이 서술할 것.
- HN "GitHub Merge Queue Silently Reverted Code" (item 47881672): matthewbauer "Merge Queue was silently reverting changesets in the merge queue." / MarkMarine "4 people spent hours putting our repo back together at my company." / LiquidityC "This happened in complete silence and since the PR was just code refactor I would most likely never noticed." / EdwardDiego "This has caused a morning of fun for our team, how do you break one of the most fundamental bits?"
- 책 연결: "검증된 것과 머지된 것이 같은가"라는 머지 큐의 핵심 질문. 머지 방식 선택(squash)이 도구 버그의 노출면까지 바꾼다는 사례.

### 3.3 tj-actions/changed-files 공급망 공격 (CVE-2025-30066)
- [웹] CISA 경보 2025-03-18 / GitHub Advisory: 2025-03-14~15 공격자가 v1~v45.0.7 태그를 악성 커밋으로 재지정, 워크플로 로그로 시크릿 유출. 23,000개 이상 저장소 영향(보안업체 추정), v46.0.1에서 해소. Advisory 제목: "tj-actions changed-files through 45.0.7 allows remote attackers to discover secrets by reading actions logs."
- [커뮤니티] 봇의 PAT 탈취가 발단, 기존 버전 태그(v35, v44.5.1 등)를 전부 재지정, 러너 메모리에서 시크릿을 뽑아 빌드 로그에 출력 → 공개 저장소에서는 로그가 곧 유출. CVSS 8.6. 국내 보도(데일리시큐) 기준 최소 218개 저장소 시크릿 노출. SHA 고정 사용자는 영향 없음. reviewdog/action-setup(CVE-2025-30154) 연쇄, Coinbase 표적 공격에서 확산이라는 분석(Unit 42). 악성 커밋 날짜 03-12설 있음. — **218개·CVSS 8.6·03-12설·Unit 42 분석은 (확인 필요)**
- HN 43367987 (2025-03-14): mixologic "All the version tags got relabeled to point to a compromised hash. Semver does nothing to help with this. your build should always use hashes and not version tags" / remram "People don't pin versions. Referencing a tag is not pinning a version, those can be updated" / srvaroa "many people mistakenly assume that git tags are immutable" / harrisi "the way people run CI/CD is just listing a random repository on GitHub"
- ⚠ 경고: rarkins(Renovate 메인테이너) 인용 "git tags are [not] immutable, especially if they are in semver format..."는 **요약 과정에서 부정어가 흐려졌을 수 있음 — 원문 확인 전 인용 금지.**
- 대응: 여러 프로젝트가 즉시 SHA 고정 PR(sysdiglabs/charts #2741, rust-lang/crates.io #10835). 이후 GitHub의 SHA 고정 강제 정책(2025-08-15)과 immutable releases(2025-10-28).

### 3.4 셀프호스트 러너 과금 발표와 이틀 만의 연기 (2025-12-16~18) [웹][커뮤니티]
- 발표·연기 사실은 §2.8 가격 참고.
- Discussion #182089: JC3 "Why are you going to charge per minute for self hosted runners? Those minutes are MY processing time" / eplightning "Github-hosted runners are both insanely overpriced and underpowered."
- HN 46309821 (2025-12-17): ZuoCen_Liu "The primary reason teams use self-hosted is not to save money, but for security (VPC access) and specialized hardware (GPUs/ARM)." / jjgreen "Postponed, not abandoned."
- 책 연결: 러너 선택은 비용·보안·벤더 의존 결정.

### 3.5 국내 사례 [웹]
- **토스페이먼츠** (김성일, 2024-02-07, "GitHub Actions로 개선하는 코드 리뷰 문화"): 리뷰어 랜덤 자동 할당("리뷰어 목록에서 PR 생성자를 제외하고 랜덤으로 리뷰어를 선정") + 슬랙 DM + "평일 오후 2시에 팀 채널로" 미리뷰 PR 리마인더(cron). 성과(요약): 평균 PR 리뷰 시간 하루 내외, 코멘트 수 평균 2배 이상, 운영 이슈 대응 시간 전년 대비 약 90% 감소 — ⚠ **수치는 원문 재확인 권장.**
- **SK DEVOCEAN** (PR Reminder Bot, 게시일 미확인) [커뮤니티]: "구성원이 많아지면서 PR이 쌓이는 속도가 점점 빨라지기 시작했습니다." / "기능 개발이 바쁠 경우 자연스럽게 후순위로 밀리게 된다." 대응: PR 템플릿(요구사항·핵심 변경·리뷰 포인트), Pn 룰(우선순위 레이블), D-n 룰(리뷰 마감일), 평일 09시 슬랙 리마인더 봇.
- **코멘토** (2024-10-15, "리뷰는 버릇이다") [커뮤니티]: "수많은 개발팀이 채용 공고에서 우리는 코드 리뷰 문화가 있다고 내세웁니다." / "그렇게 한 번 두 번 리뷰를 하지 않다 보면 어느새 리뷰되지 않는 코드가 더 많아지는 날이 찾아옵니다."
- **우아한형제들** (배민프론트개발팀 안드로이드 파트, 2017-10-30, "우린 Git-flow를 사용하고 있어요"): 2016-01 GitHub 이전 시 GitHub-flow로 시작, 팀이 2~3명→5명으로 늘고 현재 릴리스와 다음 릴리스 작업을 병렬로 하게 되며 2017-06 Git-flow로 전환. Upstream(공용)/Origin(개인 fork)/Local 3계층, squash·rebase로 선형 이력, PR 작성자가 직접 머지. 발췌: "2016년 1월에 Github로 소스코드를 이전하면서 Github-flow를 사용하기 시작했으나, 2017년 6월부터 Git-flow로 브랜치 전략을 바꾸게 되었습니다." — ⚠ 원문 대조 권장. (모바일 앱 = 명시적 버전 소프트웨어 → Driessen 2020 노트와 정합)
- **맘시터** (2022-08-05, "Git Flow에서 트렁크 기반 개발으로 나아가기"): 다중 장기 브랜치·잦은 충돌·드문 배포 문제로 TBD 전환. 작은 배포(주 단위 증분), feature toggle, 테스트 자동화로 보완. 하루 5회 이상 배포, PR 대개 300줄 미만 — ⚠ **요약 수치, 원문 대조 필요.**
- **뱅크샐러드** (2022-08-29): CI 캐시 최적화 (§2.8)
- 후보(본문 미확인): 카카오 "효과적인 코드리뷰를 위한 리뷰어의 자세"(kay.gw, 2022), "카카오스토리 팀의 코드 리뷰 도입 사례"(2016-02-04), 카카오엔터프라이즈 "GitHub Actions를 사용하는 이유"(aaron.m2, 2022) — JS 렌더로 본문 추출 실패, **인용 전 브라우저 확인.** 매스프레소 QANDA 프론트엔드 모노레포 TBD(날짜 미확인), 버즈빌 모노리포 가이드, 화해 "Git 브랜치 전략 수립을 위한 전문가의 조언들", AWS 권장 가이드(한국어) "Git 브랜칭 전략 선택".

### 3.6 Microsoft Release Flow [웹]
- 수치는 §2.6. PR 단계 빠른 테스트, 머지 후 긴 테스트 분리, release 브랜치는 main에 머지하지 않고 cherry-pick, 핫픽스는 main 먼저.

---

## 4. 논쟁점·상충 관점

### 4.1 Git Flow는 죽었나
- **원저자의 반성** [웹] (Driessen, 2020-03-05 Note of reflection)
  - "This model was conceived in 2010, now more than 10 years ago, and not very long after Git itself came into being. In those 10 years, git-flow (the branching model laid out in this article) has become hugely popular in many a software team to the point where people have started treating it like a standard of sorts — but unfortunately also as a dogma or panacea."
  - "Web apps are typically continuously delivered, not rolled back, and you don't have to support multiple versions of the software running in the wild."
  - "If your team is doing continuous delivery of software, I would suggest to adopt a much simpler workflow (like GitHub flow) instead of trying to shoehorn git-flow into your team."
  - "If, however, you are building software that is explicitly versioned, or if you need to support multiple versions of your software in the wild, then git-flow may still be as good of a fit to your team as it has been to people in the last 10 years."
  - "To conclude, always remember that panaceas don't exist. Consider your own context. Don't be hating. Decide for yourself."
  - ⚠ 경고: 노트는 2020년에 쓰였고 "10 years"는 2010→2020 기준이다. 2026년 시점 서술로 옮길 때 "10년"을 현재 경과 기간처럼 쓰지 말 것.
- **관점 A: 해롭다/불필요** [커뮤니티] — Adam Ruka "GitFlow considered harmful"(2015) → OneFlow. sytse (GitLab CEO, HN 9744059, 2015-06-19) "I agree that GitFlow is needlessly complex and that there should be one main branch." / simonw (HN 22485489, 2020-03-04) "Master should always be in a deployable state." / Lobsters(2020-03-05) bkircher "Every repo that is following gitflow comes with a mental overhead for me"; roshan "Your product almost certainly does not need this stuff"; skade "weakly defined enough to evolve into something I call 'X as practiced'"
- **관점 B: 맥락에 따라 유효** [커뮤니티] — SAI_Peregrinus (HN 22485489) "Our tests include power analysis testing...total testing takes about two weeks. Git-flow is bad if you have CD. Git-flow is great if you can't do that." / utahshex (Lobsters) "particularly useful when you have a dedicated testing team, who need a stable base to test on" / 우아한형제들의 GitHub-flow→Git-flow 전환(모바일) [웹]
- 국내 현장 [커뮤니티]: velog 등은 여전히 Git Flow를 기본값으로 소개하는 글 다수, 반면 맘시터처럼 TBD 전환기도 존재.
- 합성 관찰: 실제 분기점은 브랜치 모양이 아니라 "main의 임의 커밋을 안전하게 배포할 수 있는가"(CD 성숙도, 릴리스 승인 절차, 다중 버전 지원). 모바일·펌웨어·패키지처럼 명시적 릴리스 버전이 있으면 Git Flow 옹호가 강하다 — Driessen 노트와 일치.

### 4.2 PR 크기: 작으면 빠른가, 좋은가
- **관점 A: 작을수록 빠르고 좋다** — Google small CLs 가이드 [웹], Sadowski 2018의 Google 기준점(중앙값 24줄, 4시간 미만) [논문], Bosu 2015 "파일이 많을수록 유용한 코멘트 비율 하락" [논문]
- **관점 B: 크기와 머지 시간은 무관** [논문] — Kudrjavets, Nagappan, Rastogi 2022 (MSR, 10개 언어 100개 프로젝트 PR 845,316건 + Gerrit·Phabricator 401,790건): "Our study shows that pull request size and composition do not relate to time-to-merge." 삽입·삭제·수정 비율과 머지 시간 상관 rs = 0.18 / 0.06 / -0.14 (p.8)
- **관점 C: 쪼개면 잡음은 줄지만 결함 발견은 그대로** [논문] — di Biase et al. (arXiv:1805.10978, 2018; PeerJ CS 게재 추정, 게재지·DOI 미확인): 28명 통제 실험. 쪼개면 잘못 보고되는 이슈↓·맥락 탐색↑, 변경 이유 이해도와 찾은 결함 수에는 영향 없음
- 정리 방향(papers 제안): 작은 PR을 권하는 이유를 "빨리 머지된다"에 두지 말고 리뷰 품질(Bosu)과 되돌리기 쉬움에 둔다. "PR을 쪼개면 버그를 더 잡는다"는 과장 경계.
- ⚠ 경고: "한 번에 200~400 LOC"류 고전 수치는 SmartBear/Cisco 업계 보고로 학술 출처가 아니며 리서치에서 제외됨. 쓰려면 별도 출처 확보.

### 4.3 CI는 PR을 빠르게 하는가
- **관점 A: 빨라진다** — Hilton 2016: PR 수락 중앙값 1.6시간 빠름(5.2 vs 6.8시간), 릴리스 2배 이상 [논문]
- **관점 B: 빨라진다는 보장은 없다** — Bernardo et al. 2018 (MSR, 87개 프로젝트 PR 162,653건): CI 도입 후 머지된 PR을 더 빨리 전달한 프로젝트는 51.3%뿐. 도입 후 PR 제출 급증이 주요 원인. 2023 확장판(EMSE, 설문 450건): "adopting a CI service may not necessarily quicken the delivery of merge PRs. Instead, the pivotal benefit of a CI service is to improve the decision making on PR submissions" [논문]
- **관점 C: 자동화가 오히려 거절·대기를 늘린다** — Kinsman 2021, Wessel 2023 (GitHub Actions 도입 후 거절↑, 승인까지 시간↑) [논문]
- 정리: "CI는 빨라지게 하는 도구라기보다 판단을 돕는(그리고 안심을 사는, 87.71%) 도구."

### 4.4 리뷰어는 몇 명이어야 하나
- 관점 A: 2명이 최적 — Rigby & Bird 2013 (여러 조직에서 2명으로 수렴) [논문]
- 관점 B: 1명으로 충분 — Google, 리뷰어 중앙값 1명, 2명 이상은 25% 미만 (Sadowski 2018) [논문]
- 조직 맥락(도구·가독성 인증·monorepo)에 따른 선택지로 제시.

### 4.5 squash vs rebase vs merge commit [커뮤니티] (HN 38800454, 2023-12-29~31; HN 45371283)
- 관점 A: rebase는 좋지만 squash는 싫다 — JoshTriplett "I'm a big fan of the rebase workflow, but not of squashing. I wrote it as several separate commits for a _reason_: documenting each step, making each step revertible, separating refactors from semantic changes." / lolinder "Why not take the chance to tell the story _now_, so that future you can skip all the false starts and failed experiments?" / fillmore "I also read every commit message, and review PRs commit by commit"
- 관점 B: squash가 현실적 — herval "nobody reads intermediate commit messages one by one on a PR, period" / William_BB "PR is the atomic level of work. I'd argue PR-level history (i.e. squash) is often enough and is way cleaner." / cj "each single commit in master corresponds to a single PR. Makes it easy to revert PR but difficult to cherry pick." / bccdee "Github isn't designed to review and merge individual commits...The 'atomic commits' crowd are working against the grain of the tools we actually use."
- 관점 C: 이력 재작성 반대 — wandernotlost "It's like a huge portion of the industry is collectively engaging in a lie, so that our commit histories look prettier." / ponector "You run tests against each commit in the history that you're rebasing? I doubt it" / TheCleric: 연쇄 PR에서 squash하면 "the changes done in 1 are now present TWICE." (스택 PR과 squash 충돌)
- 절충: burntsushi "Why not use squash & merge when appropriate and rebase & merge otherwise?" / kdmccormick "The real answer to this whole debate is 'it depends' but for some reason that doesn't seem to satisfy people."
- 참고: Mitchell Hashimoto gist "Merge vs. Rebase vs. Squash" — 인용 전 원문 확인.
- 연결: 2026-04-23 머지 큐 사고는 squash 방식 그룹에서만 발생(§3.2). GitHub Rebase and merge는 로컬 rebase와 달리 항상 새 SHA·서명 검증 없음(§1.4).

### 4.6 코드 리뷰: 품질 게이트인가 연극인가 [커뮤니티]
- 관점 A: 의식(theatre)이 됐다 — HN 45371283 "The Theatre of Pull Requests and Code Review"(2025-09경, 416 댓글), nitwit005 "It's going to be cheaper to just have a chat with your coworker when a PR is confusing." GeekNews(TigerBeetle 글) 댓글: 설계 리뷰가 코드 리뷰 단계에서만 일어나 피드백이 늦다, RFC·사전 협의가 먼저. 대안: 페어 프로그래밍, 트렁크 + 사후 리뷰, 리뷰어가 직접 고쳐 머지하는 비동기 페어링.
- 관점 B: 대규모·분산 협업에선 필수 — jcalvinowels "It's clear you've never worked on a large open source project...in big distributed projects this stuff really matters." / illuminator83 "Messiness is usually not tolerated by maintainers of important projects"
- 학술 쪽 보강: McIntosh 2014(커버리지·참여도↓ → 결함↑) [논문]은 관점 B를, Bacchelli & Bird(결함 코멘트 1/8)는 "버그 그물로서의 리뷰" 기대를 낮추는 쪽을 지지 — 단 "리뷰는 무용"의 근거로 쓰면 안 된다(리뷰의 가치를 결함 외로 재정의하는 근거).
- 2026 새 축: AI 생성 PR. 한 보고서는 AI 고도 도입 조직에서 PR 크기 +51%, 리뷰 대기 중앙값 +441%, 무리뷰 머지 +31%를 주장 — ⚠ **출처 신뢰도 낮음(agentconn.com), 수치 인용 전 원 연구 확인 필수.** GitHub의 "PR kill switch" 검토 보도(2026-02, opensourceforu) **(확인 필요)**.

### 4.7 스택 PR은 필요한 추상인가 [커뮤니티]
- 찬성: adamwk (HN 47757495, 2026-04경) "It makes both reviewing and working on long-running feature projects so much nicer." / calebio "I miss the Phabricator review UI so much." / tazjin(Lobsters, 2023-12-06 Graphite 글) 스택이 "frustration levels"를 낮춘다
- 회의: jenadine "Git itself already has the concept of commit. Why put this 'stacked PR' abstraction on top of it?" / saagarjha "A unit of change is a commit. I have no idea why you'd think a PR is a unit of change." / Diana "commits go directly to main. No branch. No PR." / anordal: 문제는 GitHub이 커밋을 리뷰 단위로 보여주지 않는 것(Gerrit처럼) / crustacean: 벤더 마케팅 경계
- GeekNews(프리뷰 반응): 해결 안 된 문제가 많은 채 대상 확대, 스쿼시 머지 + 필수 리뷰 조합 시 재승인 요구, 스택 상태가 드롭다운에 미표시
- ⚠ HN 47757495의 "약 900점/528댓글"은 추출 수치 — 확인 필요.
- 진단: 리뷰 단위(PR)와 이력 단위(커밋)를 GitHub UI가 섞어 놓았다는 불만이 반복.

### 4.8 머지 큐는 필요한가, 비용만 두 배인가
- 관점 A: 트래픽 많은 main엔 필수 — byroot(§2.11), carlana (Lobsters) "you need to follow the not-rocket-science rule with agents or they will break main." [커뮤니티]; GitHub·Shopify·Block 사례 [웹]; Kudrjavets 2022b 자동 머지 근거 [논문]
- 관점 B: 비용·복잡도·신뢰 — cprecioso (HN 36707239) "the merge group needs to pass the same checks as the branch itself, making it doubly expensive"; jgoux (#14801) "the CI is running against the exact same code, it's unnecessary"; ploxiln "it was pretty flaky early on, got stuck, double commits, not configurable merge-group size ... but it's pretty good now"; 2026-04 사고 [커뮤니티]
- 완화책: two-step CI(Mergify) — PR엔 가벼운 검사, merge_group에서만 비싼 검사 [웹]
- 대체재: Mergify, Graphite, bors, Trunk 등 — 벤더 글이 많아 중립성 주의.

### 4.9 GitHub Actions에 머물 것인가 [커뮤니티]
- 관점 A: 떠나고 싶다 — YAML(tcoff91 "What kills me is when these things add like control flow constructs to YAML. Like just use an actual programming language!"; mmcnl "It's just YAML files with unlimited configuration options that have very limited documentation"; deng "Avoid YAML as much as possible, period."), 로컬 재현 불가, 가격 불신, 장애. habosa "GitHub Actions is the worst CI tool I've ever used (maybe tied with Jenkins)". 학술 보강: YAML 어려움 60.87%(Saroar 2023) [논문]
- 관점 B: 대안은 있어도 대체재는 없다 — 네트워크 효과, 무료 CI 인프라, 마켓플레이스. GeekNews 32104 댓글 "Microsoft는 무료 CI 실행기에 연간 약 1억 달러를 지출" — ⚠ **검증 필요.** Ghostty가 Actions 장애로 약 2시간 PR 리뷰를 못 했다는 사례 **(확인 필요)**.
- 절충: Actions는 트리거·오케스트레이션으로만, 빌드 로직은 이식 가능하게(§5).

### 4.10 GitHub Flow에서 배포는 언제인가 [웹]
- 관점 A (Microsoft): "an often overlooked part of GitHub Flow is that pull requests must deploy to production for testing before they can merge to the main branch."
- 관점 B (GitHub Docs): 단계 목록에 배포 시점 명시 없음(Create branch → … → Merge → Delete).
- 본문에서는 "Microsoft의 해석에 따르면"으로 귀속해 쓸 것.

### 4.11 flaky: 무관용 vs 재시도+격리 [커뮤니티]
- 관점 A: mdoms "I have a zero tolerance policy for flaky tests. In code bases where I have the authority, I immediately remove flaky tests" / "Every retry rule in your CI pipeline is a painkiller."
- 관점 B: 대규모에서는 재시도 + 자동 격리 + 소유 팀 통지가 현실적(HN 36513060 "Suppressing flaky tests is a little terrifying. Google would just retry them…"). Shopify도 flaky 대응 실패 허용 임계값 사용 [웹]. Memon 2017 "it is impossible to weed out all flaky tests" [논문]

---

## 5. 실무 적용 팁

1. **서드파티 액션은 full commit SHA로 고정** — 공식 근거 "currently the only way to use an action as an immutable release"(§2.9). tj-actions 사고에서 SHA 고정 사용자는 영향 없음. 업데이트 부담은 Dependabot/Renovate로 SHA를 갱신하는 조합이 흔히 권장 [커뮤니티]. 조직 차원에선 SHA 고정 강제 정책(2025-08-15) [웹].
2. **GITHUB_TOKEN 최소 권한** — 워크플로 기본 contents read, 잡 단위로 필요한 만큼만 상향. 2023-02 이전 생성 조직은 기본값 점검 [웹]. 근거 수치 99.8% 과도 권한(2022 논문, 전환 이전 데이터) [논문].
3. **pull_request_target에서 PR head 체크아웃 금지** — 쓰기가 필요하면 `pull_request`(무권한)→artifact→`workflow_run`(쓰기) 패턴. 2025-12-08 이후 pull_request_target은 항상 기본 브랜치의 워크플로·커밋 사용 [웹].
4. **신뢰할 수 없는 입력은 중간 환경 변수로** — `${{ github.event.pull_request.title }}`를 run에 직접 넣지 않기 [웹][논문 ARGUS].
5. **`.github/workflows`를 CODEOWNERS에 등록**, public 저장소에 self-hosted runner 쓰지 않기 [웹].
6. **클라우드 자격 증명은 OIDC로** — 장기 시크릿 대신 잡 단위 단기 토큰, subject에 environment/ref 제한 [웹]. (`id-token: write` 문장은 확인 필요)
7. **머지 큐 도입 체크리스트** [커뮤니티 역산 + 웹] — (1) 필수 체크를 최소 하나 지정("The issue was that we had no required status checks set. After setting one, it started to work." — #15254), (2) 필수 체크를 만드는 워크플로에 `merge_group` 트리거 추가(서드파티 CI는 `gh-readonly-queue/{base}/**`), (3) 빌드 시간 × 동시 빌드 한도 = 처리량 계산, (4) flaky 먼저 정리, (5) 막히면 큐 헤드 제거 → 큐 비우기 → 머지 큐 끄고 다시 켜기(GitHub 측 권장 복구). 2026년 사례: "the required merge-queue checks were never produced and the head entry hung in AWAITING_CHECKS, blocking ~23 PRs." Discussion #151100: 큐가 `merge_group`이 아닌 `pull_request` 이벤트 체크 결과로 판단한다는 보고 **(확인 필요)**. 큐 앞자리 점프는 진행 중 전체 재빌드를 부른다 [웹].
8. **two-step CI로 머지 큐 비용 절감** — PR엔 lint·unit, merge_group에서 통합·E2E [웹].
9. **모노레포: 워크플로 path 필터 대신 "변경 감지 잡 + 집계 필수 체크"** — detect-changes 잡에서 변경 경로 계산, 하위 잡은 `needs`+`if`로 스킵, 항상 도는 집계(ci_done) 잡 하나만 필수 체크. 함정: skip된 잡은 success가 아님, `actions/checkout` 기본 `fetch-depth: 1`이면 비교할 이전 커밋이 없음 [커뮤니티].
10. **CI YAML은 얇게, 빌드 로직은 로컬에서 도는 도구로**(make·just·nix·mise·Dagger) — push-and-wait 루프 끊기 [커뮤니티].
11. **캐시 스코프 이해** — PR 런은 현재·기본·base 브랜치 캐시만 복원, 형제·자식 브랜치 캐시는 못 씀, 7일 미접근 삭제, 저장소당 기본 10 GB [웹]. 캐시 쓴 유료 저장소는 32.9%뿐, 비활성 저장소 스케줄 끄기로 1.1~31.6% 절감 [논문].
12. **concurrency로 낡은 런 취소** — `group: ${{ github.head_ref || github.run_id }}` + `cancel-in-progress: true`. 배포 직렬화엔 2026-05 `queue: max`(최대 100 대기), 단 `cancel-in-progress: true`와 병용 불가 [웹].
13. **environments로 배포 게이트** — required reviewers(최대 6), prevent self-review, wait timer(1~43,200분), 승인 전 environment secrets 접근 불가. Free/Pro/Team은 public만 [웹].
14. **리뷰 SLA + 리마인더** — "업무일 1일 이내", 우선순위 레이블·마감일, 리마인더 봇(토스 평일 14시, DEVOCEAN 평일 09시). 학술 근거: Nudge 해결 시간 -60%, 불만은 p75(24시간) 꼬리에서 [웹][커뮤니티][논문].
15. **승인 후 머지 대기 제거** — auto-merge·merge queue. 29~63% 단축 가능성 [논문].
16. **PR 설명에 "왜"를 쓴다** — 리뷰에서 가장 어려운 일은 변경 이유 이해(Bacchelli & Bird) [논문]. 템플릿(요구사항·핵심 변경·리뷰 포인트) [커뮤니티].
17. **flaky는 신호를 지키는 문제** — 원인 절반 가까이가 Async Wait(45%): sleep 대신 조건 대기. 재시도는 진통제, 격리 시 소유 팀 통지 [논문][커뮤니티].
18. **feature flag는 재고** — 수명 짧게, 제거 계획과 함께 [웹][논문].
19. **브랜치는 짧게, 팀 경계에 맞게** — 브랜치 제거로 변경당 8.9일 지연 절감(+0.04 충돌), 구조 불일치 시 실패율↑ [논문]. TBD 기준: 하루 1회 이상 머지, 활성 브랜치 3개 이하 [웹].
20. **Rulesets로 이행 시** — 여러 ruleset이 겹치면 가장 엄격한 규칙 적용, 삭제 없이 비활성화 가능. 경로별 팀 승인은 required reviewer rule(2026-02 GA)로, 소유권·개인 리뷰어는 CODEOWNERS로 [웹].

---

## 6. 참고문헌

### 웹 — 공식 문서·체인지로그
- GitHub Docs. About protected branches. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches, 2026-09 조회.
- GitHub Docs. About rulesets. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets, 2026-09 조회.
- GitHub. Introducing repository rules (public beta). https://github.blog/changelog/2023-04-17-introducing-repository-rules-public-beta/, 2023-04-17.
- GitHub. Repository rules are generally available. https://github.blog/changelog/2023-07-24-repository-rules-are-generally-available/, 2023-07-24.
- GitHub. Required reviewer rule is now generally available. https://github.blog/changelog/2026-02-17-required-reviewer-rule-is-now-generally-available/, 2026-02-17.
- GitHub Docs. About code owners. https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners, 2026-09 조회.
- GitHub Docs. About merge methods on GitHub. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github, 2026-09 조회.
- GitHub. Stacked pull requests are now in public preview. https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/, 2026-07-30.
- GitHub. Draft pull requests. https://github.blog/changelog/2019-02-14-draft-pull-requests/, 2019-02-14; Introducing draft pull requests. https://github.blog/news-insights/product-news/introducing-draft-pull-requests/; Draft pull requests are now available in all repositories. https://github.blog/changelog/2025-05-01-draft-pull-requests-are-now-available-in-all-repositories/, 2025-05-01.
- GitHub Docs. Workflow syntax. https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax; Limits. https://docs.github.com/en/actions/reference/limits, 2026-09 조회.
- GitHub Docs. Events that trigger workflows. https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows, 2026-09 조회.
- GitHub Docs. Dependency caching reference. https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching, 2026-09 조회.
- GitHub. Deprecation notice: v3 of the artifact actions. https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/, 2024-04-16.
- GitHub Docs. Reuse workflows. https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows; Reusing workflow configurations. https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations, 2026-09 조회.
- GitHub Docs. Control the concurrency of workflows and jobs. https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency, 2026-09 조회.
- GitHub. GitHub Actions concurrency groups now allow larger queues. https://github.blog/changelog/2026-05-07-github-actions-concurrency-groups-now-allow-larger-queues/, 2026-05-07.
- GitHub Docs. Deployments and environments. https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments, 2026-09 조회.
- GitHub Docs. OpenID Connect. https://docs.github.com/en/actions/concepts/security/openid-connect, 2026-09 조회.
- GitHub. Coming soon: simpler pricing and a better experience for GitHub Actions. https://github.blog/changelog/2025-12-16-coming-soon-simpler-pricing-and-a-better-experience-for-github-actions/, 2025-12-16 (이후 연기 공지 추가); 2026 pricing changes for GitHub Actions. https://github.com/resources/insights/2026-pricing-changes-for-github-actions.
- GitHub Docs. Secure use reference. https://docs.github.com/en/actions/reference/security/secure-use, 2026-09 조회.
- Jaroslav Lobačevski. Keeping your GitHub Actions and workflows secure Part 1: Preventing pwn requests. GitHub Security Lab. https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/, 2021-08-03.
- GitHub. Actions pull_request_target and environment branch protections changes. https://github.blog/changelog/2025-11-07-actions-pull_request_target-and-environment-branch-protections-changes/, 2025-11-07 (2025-12-08 시행); Docs https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target.
- GitHub. GitHub Actions: updating the default GITHUB_TOKEN permissions to read-only. https://github.blog/changelog/2023-02-02-github-actions-updating-the-default-github_token-permissions-to-read-only/, 2023-02-02.
- GitHub. GitHub Actions policy now supports blocking and SHA pinning actions. https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/, 2025-08-15.
- CISA. Supply Chain Compromise of Third-Party tj-actions/changed-files (CVE-2025-30066) and reviewdog/action-setup. https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction, 2025-03-18; GitHub Advisory https://github.com/advisories/ghsa-mrrh-fwg8-r2c3.
- GitHub. Immutable releases are now generally available. https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/, 2025-10-28.
- GitHub Docs. GitHub flow. https://docs.github.com/en/get-started/using-github/github-flow, 2026-09 조회.
- GitHub Docs. Managing a merge queue. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue, 2026-09 조회.
- GitHub Docs. Merging a pull request with a merge queue. https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request-with-a-merge-queue, 2026-09 조회.
- GitHub. Pull request merge queue public beta. https://github.blog/changelog/2023-02-08-pull-request-merge-queue-public-beta/, 2023-02-08; Pull request merge queue is now generally available. https://github.blog/changelog/2023-07-12-pull-request-merge-queue-is-now-generally-available/, 2023-07-12.
- Dustin Yin. GitHub merge queue is generally available. GitHub Blog. https://github.blog/news-insights/product-news/github-merge-queue-is-generally-available/, 2023-07-12 (2024-04-25 갱신).
- Microsoft Learn. How Microsoft develops with DevOps. https://learn.microsoft.com/en-us/devops/develop/how-microsoft-develops-devops, ms.date 2022-07-18 (updated_at 2026-09-04).
- DORA. DORA's software delivery metrics. https://dora.dev/guides/dora-metrics/, 2026-01-05 갱신.
- DORA. Capabilities: Trunk-based development. https://dora.dev/capabilities/trunk-based-development/, 상시.
- DORA / Google Cloud. 2025 DORA Report — State of AI-assisted Software Development. https://dora.dev/dora-report-2025/, 2025(9월); PDF https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf.
- Mergify. Merge Queue docs (batches, parallel checks, two-step). https://docs.mergify.com/merge-queue/batches/, https://docs.mergify.com/merge-queue/parallel-checks/, https://docs.mergify.com/merge-queue/two-step/, 2026-09 조회.

### 웹 — 원저자·엔지니어링 블로그
- Google. Engineering Practices: Small CLs. https://google.github.io/eng-practices/review/developer/small-cls.html, 2019 공개.
- Greg Foster. Stacked diffs guide. Graphite. https://graphite.com/guides/stacked-diffs, 날짜 미표기.
- John Micco. Flaky Tests at Google and How We Mitigate Them. Google Testing Blog. https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html, 2016-05-27.
- Jeff Listfield. Where do our flaky tests come from? Google Testing Blog. https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html, 2017-04-17.
- Vincent Driessen. A successful Git branching model (+ Note of reflection). https://nvie.com/posts/a-successful-git-branching-model/, 2010-01-05 / 2020-03-05.
- GitLab. What is GitLab Flow. https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/; 원문 https://about.gitlab.com/blog/2014/09/29/gitlab-flow/, 2014-09-29.
- Paul Hammant 외. Trunk Based Development. https://trunkbaseddevelopment.com/, 상시.
- Martin Fowler. Patterns for Managing Source Code Branches. https://martinfowler.com/articles/branching-patterns.html, 2020-05-28.
- Adam Ruka. OneFlow – a Git branching model and workflow. https://www.endoflineblog.com/oneflow-a-git-branching-model-and-workflow, 페이지 표기 2017-04-30. / GitFlow considered harmful. https://www.endoflineblog.com/gitflow-considered-harmful, 2015.
- Pete Hodgson. Feature Toggles (aka Feature Flags). https://martinfowler.com/articles/feature-toggles.html, 2017-10-09.
- Scott Chacon, Ben Straub. Pro Git 2nd ed., Git Branching — Branching Workflows. https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows, 2014.
- Will Smythe, Lawrence Gripper. How GitHub uses merge queue to ship hundreds of changes every day. GitHub Blog. https://github.blog/engineering/engineering-principles/how-github-uses-merge-queue-to-ship-hundreds-of-changes-every-day/, 2024-03-06.
- Darren Worrall. Introducing the Merge Queue. Shopify Engineering. https://shopify.engineering/introducing-the-merge-queue, 2018-06-08.
- Jack Li. Successfully Merging the Work of 1000+ Developers. Shopify Engineering. https://shopify.engineering/successfully-merging-work-1000-developers, 2019-11-14.
- Zhongpeng Lin, Matthew Williams. Bypassing Large Diffs in SubmitQueue. Uber Blog. https://www.uber.com/blog/bypassing-large-diffs-in-submitqueue/, 2023-08-31. (논문 페이지 https://www.uber.com/blog/research/keeping-master-green-at-scale 조회 시 404)
- bors-ng. This Month in Bors #76. https://bors.tech/newsletter/2023/04/30/tmib-76/, 2023-04-30. Graydon Hoare. Not Rocket Science Rule. https://graydon2.dreamwidth.org/1597.html, 2014 (조회 403).
- Graphite. Shopify merge queue customer story. https://graphite.com/customer/shopify-merge-queu, 날짜 미확인.
- 백명석. 우아한테크세미나 "지속가능한 SW개발을 위한 코드리뷰". 우아한형제들 기술블로그. https://techblog.woowahan.com/8159/, 2022-04-19.
- kay.gw. 효과적인 코드리뷰를 위한 리뷰어의 자세. 카카오 기술블로그. https://tech.kakao.com/posts/498, 2022. (본문 미확인)
- 카카오. 카카오스토리 팀의 코드 리뷰 도입 사례. https://tech.kakao.com/2016/02/04/code-review/, 2016-02-04. (본문 미확인)
- 김성일. GitHub Actions로 개선하는 코드 리뷰 문화. 토스 기술블로그. https://toss.tech/article/25431, 2024-02-07.
- aaron.m2. 카카오엔터프라이즈가 GitHub Actions를 사용하는 이유. https://tech.kakao.com/posts/516, 2022. (본문 미확인)
- 우아한형제들 배민프론트개발팀 안드로이드 파트. 우린 Git-flow를 사용하고 있어요. https://techblog.woowahan.com/2553/, 2017-10-30.
- 맘시터(Mfort). Git Flow에서 트렁크 기반 개발으로 나아가기. https://tech.mfort.co.kr/blog/2022-08-05-trunk-based-development/, 2022-08-05.
- Hyunmin Woo. 프론트엔드 모노레포 TBD로 관리하기. 매스프레소. https://blog.mathpresso.com/프론트엔드-모노레포-tbd로-관리하기-af752314d30f, 날짜 미확인.
- 버즈빌. 모노리포 개발 가이드. https://tech.buzzvil.com/handbook/workingflow-in-monorepo.
- AWS 권장 가이드. Git 브랜칭 전략 선택. https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/choosing-git-branch-approach/.
- 뱅크샐러드. GitHub Action npm cache. https://blog.banksalad.com/tech/github-action-npm-cache/, 2022-08-29.
- 화해. Git 브랜치 전략 수립을 위한 전문가의 조언들. https://blog.hwahae.co.kr/all/tech/9507.

### 논문·단행본
- Bacchelli, A., Bird, C. Expectations, Outcomes, and Challenges of Modern Code Review. ICSE 2013, pp. 712-721. DOI 10.1109/ICSE.2013.6606617.
- Sadowski, C., Söderberg, E., Church, L., Sipko, M., Bacchelli, A. Modern Code Review: A Case Study at Google. ICSE-SEIP 2018, pp. 181-190. DOI 10.1145/3183519.3183525.
- Rigby, P. C., Bird, C. Convergent Contemporary Software Peer Review Practices. ESEC/FSE 2013, pp. 202-212. DOI 10.1145/2491411.2491444.
- Mäntylä, M. V., Lassenius, C. What Types of Defects Are Really Discovered in Code Reviews? IEEE TSE, pp. 430-448, 2009. DOI 10.1109/TSE.2008.71.
- Beller, M., Bacchelli, A., Zaidman, A., Juergens, E. Modern Code Reviews in Open-Source Projects: Which Problems Do They Fix? MSR 2014, pp. 202-211. DOI 10.1145/2597073.2597082.
- McIntosh, S., Kamei, Y., Adams, B., Hassan, A. E. The Impact of Code Review Coverage and Code Review Participation on Software Quality. MSR 2014, pp. 192-201. DOI 10.1145/2597073.2597076.
- Bosu, A., Greiler, M., Bird, C. Characteristics of Useful Code Reviews: An Empirical Study at Microsoft. MSR 2015, pp. 146-156. DOI 10.1109/MSR.2015.21.
- di Biase, M., Bruntink, M., van Deursen, A., Bacchelli, A. The Effects of Change Decomposition on Code Review — A Controlled Experiment. arXiv:1805.10978, 2018. (게재지·DOI 미확인)
- Kudrjavets, G., Nagappan, N., Rastogi, A. Do Small Code Changes Merge Faster? A Multi-Language Empirical Investigation. MSR 2022, pp. 537-548. DOI 10.1145/3524842.3528448.
- Kudrjavets, G., Kumar, A., Nagappan, N., Rastogi, A. Mining Code Review Data to Understand Waiting Times Between Acceptance and Merging. MSR 2022, pp. 579-590. DOI 10.1145/3524842.3528432.
- Maddila, C. et al. Nudge: Accelerating Overdue Pull Requests toward Completion. ACM TOSEM, pp. 1-30, 2023. DOI 10.1145/3544791.
- Shan, Q. et al. Using Nudges to Accelerate Code Reviews at Scale. ESEC/FSE 2022, pp. 472-482. DOI 10.1145/3540250.3549104.
- Badampudi, D., Unterkalmsteiner, M., Britto, R. Modern Code Reviews—Survey of Literature and Practice. ACM TOSEM, pp. 1-61, 2023. DOI 10.1145/3585004.
- Davila, N., Nunes, I. A systematic literature review and taxonomy of modern code review. JSS, 2021. DOI 10.1016/j.jss.2021.110951.
- Gousios, G., Pinzger, M., van Deursen, A. An Exploratory Study of the Pull-based Software Development Model. ICSE 2014, pp. 345-355. DOI 10.1145/2568225.2568260.
- Gousios, G., Zaidman, A., Storey, M.-A., van Deursen, A. Work Practices and Challenges in Pull-Based Development: The Integrator's Perspective. ICSE 2015, pp. 358-368. DOI 10.1109/ICSE.2015.55.
- Gousios, G., Storey, M.-A., Bacchelli, A. Work practices and challenges in pull-based development: the contributor's perspective. ICSE 2016, pp. 285-296. DOI 10.1145/2884781.2884826.
- Tsay, J., Dabbish, L., Herbsleb, J. Influence of Social and Technical Factors for Evaluating Contribution in GitHub. ICSE 2014, pp. 356-366. DOI 10.1145/2568225.2568315.
- Vasilescu, B., Yu, Y., Wang, H., Devanbu, P., Filkov, V. Quality and Productivity Outcomes Relating to Continuous Integration in GitHub. ESEC/FSE 2015, pp. 805-816. DOI 10.1145/2786805.2786850.
- Hilton, M., Tunnell, T., Huang, K., Marinov, D., Dig, D. Usage, Costs, and Benefits of Continuous Integration in Open-Source Projects. ASE 2016, pp. 426-437. DOI 10.1145/2970276.2970358.
- Hilton, M., Nelson, N., Tunnell, T., Marinov, D., Dig, D. Trade-offs in Continuous Integration: Assurance, Security, and Flexibility. ESEC/FSE 2017, pp. 197-207. DOI 10.1145/3106237.3106270.
- Bernardo, J. H., da Costa, D. A., Kulesza, U. Studying the Impact of Adopting Continuous Integration on the Delivery Time of Pull Requests. MSR 2018, pp. 131-141. DOI 10.1145/3196398.3196421.
- Bernardo, J. H., da Costa, D. A., Kulesza, U., Treude, C. The impact of a continuous integration service on the delivery time of merged pull requests. EMSE, 2023. DOI 10.1007/s10664-023-10327-6.
- Zhao, Y., Serebrenik, A., Zhou, Y., Filkov, V., Vasilescu, B. The Impact of Continuous Integration on Other Software Development Practices. ASE 2017, pp. 60-71. DOI 10.1109/ASE.2017.8115619.
- Soares, E., Sizilio, G., Santos, J., da Costa, D. A., Kulesza, U. The Effects of Continuous Integration on Software Development: A Systematic Literature Review. EMSE, 2022. DOI 10.1007/s10664-021-10114-1.
- Shahin, M., Babar, M. A., Zhu, L. Continuous Integration, Delivery and Deployment: A Systematic Review on Approaches, Tools, Challenges and Practices. IEEE Access, pp. 3909-3943, 2017. DOI 10.1109/ACCESS.2017.2685629.
- Luo, Q., Hariri, F., Eloussi, L., Marinov, D. An Empirical Analysis of Flaky Tests. FSE 2014, pp. 643-653. DOI 10.1145/2635868.2635920.
- Memon, A. et al. Taming Google-Scale Continuous Testing. ICSE-SEIP 2017, pp. 233-242. DOI 10.1109/ICSE-SEIP.2017.16.
- Parry, O., Kapfhammer, G. M., Hilton, M., McMinn, P. A Survey of Flaky Tests. ACM TOSEM, pp. 1-74, 2021. DOI 10.1145/3476105.
- Parry, O. et al. Surveying the developer experience of flaky tests. ICSE-SEIP 2022, pp. 253-262. DOI 10.1145/3510457.3513037.
- Eck, M., Palomba, F., Castelluccio, M., Bacchelli, A. Understanding flaky tests: the developer's perspective. ESEC/FSE 2019, pp. 830-840. DOI 10.1145/3338906.3338945.
- Machalica, M., Samylkin, A., Porth, M., Chandra, S. Predictive Test Selection. ICSE-SEIP 2019, pp. 91-100. DOI 10.1109/ICSE-SEIP.2019.00018.
- Henderson, T. A. D., Dorward, B., Nickell, E., Johnston, C., Kondareddy, A. Flake Aware Culprit Finding. ICST 2023, pp. 362-373. DOI 10.1109/ICST57152.2023.00041.
- Shihab, E., Bird, C., Zimmermann, T. The Effect of Branching Strategies on Software Quality. ESEM 2012, pp. 301-310. DOI 10.1145/2372251.2372305.
- Bird, C., Zimmermann, T. Assessing the Value of Branches with What-if Analysis. FSE 2012, pp. 1-11. DOI 10.1145/2393596.2393648.
- Ghiotto, G., Murta, L., Barros, M., van der Hoek, A. On the Nature of Merge Conflicts: A Study of 2,731 Open Source Java Projects Hosted by GitHub. IEEE TSE, pp. 892-915, 2020 (온라인 2018). DOI 10.1109/TSE.2018.2871083.
- McKee, S., Nelson, N., Sarma, A., Dig, D. Software Practitioner Perspectives on Merge Conflicts and Resolutions. ICSME 2017, pp. 467-478. DOI 10.1109/ICSME.2017.53.
- Brun, Y., Holmes, R., Ernst, M. D., Notkin, D. Proactive detection of collaboration conflicts. ESEC/FSE 2011, pp. 168-178. DOI 10.1145/2025113.2025139.
- Rahman, M. T., Querel, L.-P., Rigby, P. C., Adams, B. Feature Toggles: Practitioner Practices and a Case Study. MSR 2016, pp. 201-211. DOI 10.1145/2901739.2901745.
- Potvin, R., Levenberg, J. Why Google Stores Billions of Lines of Code in a Single Repository. CACM, pp. 78-87, 2016. DOI 10.1145/2854146.
- Xu, G., Subramanian, A., Karthik, N. AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates. arXiv:2607.04697, 2026. (동료 심사 미확인)
- Ananthanarayanan, S. et al. Keeping Master Green at Scale. EuroSys 2019, pp. 1-15. DOI 10.1145/3302424.3303970. (원문 미확보 — 저자 슬라이드 sundaram.io/slides/eurosys19.pdf, The Morning Paper blog.acolyer.org 2019-04-18)
- Kinsman, T., Wessel, M., Gerosa, M. A., Treude, C. How Do Software Developers Use GitHub Actions to Automate Their Workflows? MSR 2021, pp. 420-431. DOI 10.1109/MSR52588.2021.00054.
- Wessel, M., Vargovich, J., Gerosa, M. A., Treude, C. GitHub Actions: The Impact on the Pull Request Process. EMSE, 2023. DOI 10.1007/s10664-023-10369-w.
- Decan, A., Mens, T., Rostami Mazrae, P., Golzadeh, M. On the Use of GitHub Actions in Software Development Repositories. ICSME 2022, pp. 235-245. DOI 10.1109/ICSME55016.2022.00029.
- Golzadeh, M., Decan, A., Mens, T. On the rise and fall of CI services in GitHub. SANER 2022, pp. 662-672. DOI 10.1109/SANER53432.2022.00084.
- Decan, A., Mens, T., Onsori Delicheh, H. On the outdatedness of workflows in the GitHub Actions ecosystem. JSS, 2023. DOI 10.1016/j.jss.2023.111827.
- Bouzenia, I., Pradel, M. Resource Usage and Optimization Opportunities in Workflows of GitHub Actions. ICSE 2024. DOI 10.1145/3597503.3623303.
- Valenzuela-Toledo, P., Bergel, A., Kehrer, T., Nierstrasz, O. The Hidden Costs of Automation: An Empirical Study on GitHub Actions Workflow Maintenance. SCAM 2024. DOI 10.1109/SCAM63643.2024.00029 (arXiv:2409.02366).
- Rostami Mazrae, P., Decan, A., Mens, T., Wessel, M. An Empirical Study of the Evolution of GitHub Actions Workflows. arXiv:2602.14572, 2026.
- Saroar, S. G., Nayebi, M. Developers' Perception of GitHub Actions: A Survey Analysis. EASE 2023, pp. 121-130. DOI 10.1145/3593434.3593475.
- Koishybayev, I. et al. Characterizing the Security of GitHub CI Workflows. USENIX Security 2022. https://www.usenix.org/system/files/sec22-koishybayev.pdf (DOI 없음).
- Muralee, S. et al. ARGUS: A Framework for Staged Static Taint Analysis of GitHub Workflows and Actions. USENIX Security 2023. https://www.usenix.org/system/files/usenixsecurity23-muralee.pdf (DOI 없음).
- Benedetti, G., Verderame, L., Merlo, A. Automatic Security Assessment of GitHub Actions Workflows. SCORED '22, pp. 37-45. DOI 10.1145/3560835.3564554.
- Forsgren, N., Humble, J., Kim, G. Accelerate: The Science of Lean Software and DevOps. IT Revolution Press, 2018. ISBN 9781942788331.
- Forsgren, N., Humble, J. The Role of Continuous Delivery in IT and Organizational Performance. SSRN, 2015. DOI 10.2139/ssrn.2681909.

### 커뮤니티 (전부 커뮤니티 의견, 검증 필요)
- GitHub Community Discussion #193645 (머지 큐 squash 되돌림 인시던트), 2026-04. https://github.com/orgs/community/discussions/193645
- HN "GitHub Merge Queue Silently Reverted Code", 2026-04. https://news.ycombinator.com/item?id=47881672
- HN "Tj-actions/changed-files GitHub Action Compromised", 2025-03-14. https://news.ycombinator.com/item?id=43367987 (+ 43368870, 43382055)
- 데일리시큐. tj-actions 관련 보도. https://www.dailysecu.com/news/articleView.html?idxno=164700
- GitHub Community Discussion #182089, 2025-12-16. https://github.com/orgs/community/discussions/182089 ; HN 46309821 (2025-12-17), 46301772, 46291156
- GitHub Community Discussion #13690 (2022-03-28~), #26251, #44490, #177835 (path 필터 + 필수 체크)
- SK DEVOCEAN. 코드 리뷰 문화를 리뷰해 봐요 (PR Reminder Bot 개발 이야기). https://devocean.sk.com/blog/techBoardDetail.do?ID=165255, 게시일 미확인.
- 코멘토 개발팀. 리뷰는 버릇이다: 코드 리뷰 문화 되살리기. https://developer.comento.kr/post/code-review-culture-24-10-15, 2024-10-15.
- Dev.to. Improving Hasura's internal PR review process. https://dev.to/noriste/improving-hasuras-internal-pr-review-process-1ham ; LGTM Culture. https://dev.to/pyor/lgtm-culture-when-code-review-becomes-theatre-28k
- HN "The Theatre of Pull Requests and Code Review", 2025-09경. https://news.ycombinator.com/item?id=45371283
- youngju.dev. code-review-that-teaches. https://www.youngju.dev/blog/career/code-review-that-teaches (개인 블로그)
- agentconn.com. 10x PRs 1x reviewers. https://agentconn.com/blog/10x-prs-1x-reviewers-code-quality-bottleneck-gate-2026/ (신뢰도 낮음)
- OpenSourceForU. GitHub weighs pull request kill switch. https://www.opensourceforu.com/2026/02/github-weighs-pull-request-kill-switch-as-ai-slop-floods-open-source/, 2026-02.
- HN "GitHub Stacked PRs", 2026-04경. https://news.ycombinator.com/item?id=47757495 ; GeekNews https://news.hada.io/topic?id=32001 ; Lobsters https://lobste.rs/s/sda7hr/your_github_pull_request_workflow_is (2023-12-06)
- HN flaky 스레드: 23493249 (2020-06), 47024638 (2026-02경), 42429601 (2024-12-18), 36513060; Discussion #168145 [오귀속 — 실제는 트리거 중복·상호 취소 (13장 fact-check 확인)]
- HN "I hate GitHub Actions with passion", 2026-01경. https://news.ycombinator.com/item?id=46614558 ; Lobsters "GitHub Actions Is Slowly Killing Your Engineering Team" (Ian Duncan, 2026-02-05) https://lobste.rs/s/hkqnro/github_actions_is_slowly_killing_your ; HN 46909274 ; HN "The Pain That Is GitHub Actions" (2025-03-20) https://news.ycombinator.com/item?id=43419701
- GeekNews "GitHub의 대안은 있지만 대체재는 없다". https://news.hada.io/topic?id=32104 (2026년 중반 추정)
- velog. CI 빌드 시간 400% 개선하기. https://velog.io/@rhkrwngud445/CI-%EB%B9%8C%EB%93%9C-%EC%8B%9C%EA%B0%84-400-%EA%B0%9C%EC%84%A0%ED%95%98%EA%B8%B0-feat-Github-Action ; Discussion #18549
- GitHub Community Discussion #15254 (2022-04-20~), #151100, #14801 (2022-04-12~), #201908
- The Hacker News. Claude Code GitHub Action flaw. https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html, 2026-06.
- sysdiglabs/charts PR #2741; rust-lang/crates.io PR #10835.
- codewithkarani. Monorepo GitHub Actions path filters. https://www.codewithkarani.com/blog/monorepo-github-actions-path-filters-shared-code
- Steve Berczuk. Timely reviews. https://steveberczuk.substack.com/p/timely-reviews
- HN 9744059 (2015-06-19); HN 22485489 (2020-03-04); Lobsters https://lobste.rs/s/o76cit/please_stop_recommending_git_flow (2020-03-05); velog https://velog.io/@gmlstjq123/Git-Flow-VS-Github-Flow
- HN "The merge vs. rebase debate", 2023-12-29~31. https://news.ycombinator.com/item?id=38800454 ; Mitchell Hashimoto gist https://gist.github.com/mitchellh/319019b1b8aac9110fcfb1862e0c97fb ; GeekNews https://news.hada.io/topic?id=22651
- HN 36707239 (merge queue GA, 2023-07-13); Lobsters "Replace Your CI With a Merge Queue" https://lobste.rs/s/drtmhv/replace_your_ci_with_merge_queue (2026-07-27)

---

## 7. 리서치 한계

### 실패·미확보 원문
- **Uber SubmitQueue 논문(EuroSys 2019) 원문 미확보(ACM 403).** 수치는 저자 슬라이드와 The Morning Paper 2차 인용. 특히 "도입 전 iOS main이 초록이던 시간 52%"는 원문 페이지 미확인. Uber 블로그의 논문 페이지도 404.
- **Google flaky 수치(1.5% / 16% / 84%)는 2차 인용.** Google Testing Blog 2016·2017 본문이 스크립트 렌더라 원문 문장 추출 실패 — 브라우저 대조 필수.
- Graydon Hoare "Not Rocket Science Rule" 원문 403. GitLab Flow 2014 원문의 "upstream first" 문장 미확보. 카카오 기술블로그 두 글(posts/498, 516) 본문 미로딩. Graphite Shopify 고객 사례 본문 미확인.
- 초록만 본 논문(Rigby & Bird 원문 수치, Zhao 2017, Shan 2022 실험 결과, Eck 2019, Decan 2023 outdatedness, Potvin 2016)은 세부 수치 인용 전 원문 대조 필요.
- 2025 DORA Report 원문 PDF 문장 미추출(발표문·2차 요약 수준). Accelerate 본문 수치 미확인.

### 공식 미확인 수치·상태
- **GitHub merge queue 설정 기본값**(build concurrency·그룹 최소/최대·대기·타임아웃) 공식 미확인 — 범위(1~100)만 확인.
- **2026-09 현재 Team 플랜 private 저장소의 merge queue 지원 여부** 미확인.
- **2026-04-23 머지 큐 사고 규모 수치 불일치**: "658 repositories, 2,092 PRs"(인시던트 요약) vs "2,804 PRs out of over 4 million merged on April 23"(HN에서 인용된 Kyle Daigle 발언). 공식 원문 대조 전 어느 쪽도 단정 불가.
- GitHub 자체 merge queue의 "2,500 pull requests" 기간 단위(월로 알려짐) 미확인.
- reusable workflow 파일당 호출 한도, OIDC `id-token: write` 문장, artifact 액션 최신 메이저 버전, 캐시 확장 최대치("up to 10 TB"), stacked PR의 GA·merge queue 연동 상태, self-hosted 요금 재도입 여부, "immutable actions" 출시 상태.
- tj-actions 세부(218개 저장소·CVSS 8.6·03-12설·Unit 42 분석)는 보도·커뮤니티 기반.

### 상충해 결론을 내리지 않은 영역
- **리뷰 크기 연구 상충**: Google 가이드·Sadowski 2018·Bosu 2015(작을수록 좋다) vs Kudrjavets 2022(크기와 머지 시간 무관) vs di Biase 2018(쪼개도 결함 발견 수 동일). 업계 "200~400 LOC" 수치는 학술 출처가 아니라 제외.
- CI 속도 효과(Hilton 2016 vs Bernardo 2018/2023), 리뷰어 수(Rigby & Bird 2명 vs Google 1명).

### 커버리지 공백
- **Reddit 전면 차단**(검색·페치 불가) — r/git·r/devops·r/ExperiencedDevs 부재. 주니어~중간 연차의 일상 경험담이 약하다. OKKY·커리어리도 노출 거의 없음/페치 실패.
- **국내 자료 비중 낮음**: web 전체 약 20%(스킬 기준 60~70%에 미달). merge queue·Actions 보안·rulesets의 국내 회사 1차 사례 없음. 국내 사례는 코드 리뷰(토스·우아한·카카오·DEVOCEAN·코멘토)와 브랜치 전략(우아한·맘시터)에 편중. 한국 팀의 머지 큐 도입 경험담 미발견.
- Merge Queue를 직접 다룬 동료 심사 논문은 SubmitQueue뿐. Google TAP·Chromium CQ 같은 사례의 1차 자료 부족.
- 트렁크 기반 vs GitFlow를 직접 비교한 실증 논문 없음(브랜칭 연구는 Microsoft Windows 중심).
- 모노레포 CI는 GitHub Discussions 중심, Bazel/Nx/Turborepo 실사용 토론은 얕음.
- HN/Lobsters 댓글과 web 인용은 WebFetch 요약 경유 — 축약·부정어 누락 가능(특히 rarkins).
- 실패한 리서처: 없음(3종 모두 산출). 단, 각 리서처가 위 부분 실패를 보고함.

---

## 신선도 원장

검색 시점: 세 리서처 모두 2026-09-26. "2026-09 조회" = 상시 갱신 문서를 이 시점에 본 것.

| 소스 | 발행일 / 버전 시점 | 비고 |
|---|---|---|
| GitHub Docs — protected branches, rulesets, code owners, merge methods, GitHub flow | 상시 갱신, 2026-09 조회 | 플랜별 기능 변동 |
| Repository rules beta / GA | 2023-04-17 / 2023-07-24 | evaluation mode = Enterprise Cloud |
| Required reviewer rule GA | 2026-02-17 (preview 2025-11) | |
| Stacked PR public preview | 2026-07-30 | 빠르게 변함 — GA·merge queue 연동 재확인 |
| Draft PR 도입 / Free private 확대 | 2019-02-14 / 2025-05-01 | |
| Actions workflow syntax·limits·events·caching·reuse·environments·OIDC·secure use | 2026-09 조회 | 한도·플랜 수치 자주 변동 |
| Artifacts v3 deprecation | 2024-04-16 (v3 차단 2025-01-30) | 최신 메이저 미확인 |
| Concurrency `queue: max` | 2026-05-07 | 이전 자료와 충돌 |
| Actions 가격 변경 / self-hosted 요금 연기 | 2025-12-16 / 2025-12-17~18 | 재도입 여부 재확인 |
| pwn requests (Security Lab) | 2021-08-03 | 2025-12-08 변경 이전 서술 |
| pull_request_target 동작 변경 | 2025-11-07 공지 / 2025-12-08 시행 | |
| GITHUB_TOKEN read-only 기본값 | 2023-02-02 | 신규 대상만 |
| Actions policy SHA 고정 강제 | 2025-08-15 | |
| tj-actions CVE-2025-30066 / CISA | 2025-03-14~15 사건 / 2025-03-18 경보 | 악성 커밋 03-12설 |
| Immutable releases GA | 2025-10-28 | |
| Merge queue beta / GA / GA 블로그 갱신 | 2023-02-08 / 2023-07-12 / 2024-04-25 | Team private 지원 미확인 |
| GitHub merge queue 사내 사례 | 2024-03-06 | |
| 머지 큐 squash 되돌림 사고 | 2026-04-23 | 규모 수치 충돌 |
| Shopify merge queue | 2018-06-08 / 2019-11-14 | |
| Uber SubmitQueue 논문 / BLRD 블로그 | EuroSys 2019 / 2023-08-31 | 논문 원문 미확보 |
| bors-ng 종료 | 2023-04-30 | |
| Mergify docs | 2026-09 조회 | |
| Google small CLs | 2019 공개, 상시 | |
| Google Testing Blog flaky | 2016-05-27 / 2017-04-17 | 원문 미추출 |
| Microsoft Release Flow | ms.date 2022-07-18 (updated 2026-09-04) | |
| Driessen Git Flow / Note of reflection | 2010-01-05 / 2020-03-05 | "10 years"는 2020 기준 |
| GitLab Flow | 2014-09-29 원문, 토픽 페이지 상시 | |
| Trunk Based Development / DORA TBD capability | 상시 | |
| Fowler branching patterns | 2020-05-28 | |
| OneFlow | 페이지 2017-04-30 (최초 2015 추정) | |
| Feature Toggles (Hodgson) | 2017-10-09 | |
| Pro Git 2nd ed. | 2014 | |
| DORA metrics guide | 2026-01-05 갱신 | 5지표 |
| 2025 DORA Report | 2025-09 | 원문 미추출 |
| 우아한형제들 Git-flow | 2017-10-30 | |
| 맘시터 TBD | 2022-08-05 | |
| 토스 코드 리뷰 Actions | 2024-02-07 | |
| 우아한테크세미나 코드리뷰 | 2022-04-19 | |
| 카카오 코드리뷰 / 카카오스토리 / 카카오엔터프라이즈 Actions | 2022 / 2016-02-04 / 2022 | 본문 미확인 |
| 뱅크샐러드 CI 캐시 | 2022-08-29 | |
| 코멘토 리뷰 문화 | 2024-10-15 | |
| SK DEVOCEAN PR Reminder Bot | 게시일 미확인 | |
| 논문 — 코드 리뷰 | 2009~2023 | Sadowski 2018 Google 맥락 |
| 논문 — PR 모델 (Gousios 2014) | 2012~2013 데이터 | 14%는 현재 수치 아님 |
| 논문 — CI (Vasilescu 2015, Hilton 2016) | Travis CI 시대 | Actions 환경과 다를 수 있음 |
| 논문 — Actions 채택 (Kinsman 2021) | 2020년 무렵 데이터 | 0.7%는 현재 채택률 아님 |
| 논문 — Actions 보안 (Koishybayev 2022) | 2023-02 기본 read-only 전환 이전 | |
| 논문 — Rostami Mazrae 2026 / Xu 2026 | arXiv 2026, 게재 미확인 | 프리프린트 |
| 피인용수 | OpenAlex/Crossref, 2026-09-26 | Scholar보다 낮음 |
| 커뮤니티 스레드 | 2015-06 ~ 2026-08 (표 내 개별 날짜) | 전부 검증 필요 |
