
---

## 에필로그

1장을 열 때 우리 손에 있던 것은 빨간 빌드 로그 한 줄이었다. 사라진 `calculateFee`를 부르는 코드, 그리고 "제 PR은 초록이었는데요"라는 두 사람의 말. 열네 장을 지나오며 그 한 줄 뒤에 겹겹이 쌓인 결정들을 하나씩 들춰 봤다. 브랜치를 얼마나 오래 살려 두는지, 저장소 설정이 팀의 약속을 얼마나 정확히 적고 있는지, PR이 리뷰어가 한자리에서 이해할 수 있는 크기인지, 리뷰가 무엇을 위해 있는지, 필수 체크를 믿을 수 있는지, 그 체크를 돌리는 파이프라인이 빠르고 안전한지, 그리고 검사한 조합을 그대로 머지하고 있는지. 이 가운데 어느 하나도 혼자서 `main`을 지켜 주지 않았다. 여러 겹이 조금씩 확률을 줄일 뿐이었다.

### 이 책이 답하지 못한 것

솔직히 적어 두고 싶은 빈칸이 있다.

먼저 국내 팀의 이야기가 한쪽에 몰려 있다. 브랜치 전략과 코드 리뷰에서는 우아한형제들, 맘시터, 토스페이먼츠, SK DEVOCEAN, 코멘토 같은 국내 팀의 경험을 빌려 올 수 있었지만, 머지 큐와 Actions 보안, 룰셋을 다룬 8~13장은 해외 사례와 공식 문서에 기댈 수밖에 없었다. 한국 팀이 머지 큐를 들이며 무엇에 걸려 넘어졌는지는 아직 이 책이 들려주지 못한 이야기다.

머지 큐의 학문적 근거도 얇다. 이 책을 준비하며 찾은 자료 가운데 머지 큐를 직접 다룬 동료 심사 연구는 12장에서 계보로 소개한 Uber SubmitQueue 정도였고, 그마저 원문 대신 저자 발표 자료로 읽어야 했다. 나머지는 기업 블로그와 공식 문서, 커뮤니티 토론이다. 머지 큐가 팀의 리드 타임이나 변경 실패율을 얼마나 바꾸는지 여러 조직에 걸쳐 잰 연구가 나온다면, 13장의 도입 판단은 지금보다 훨씬 단단해질 것이다.

브랜치 전략을 두고도 비슷하다. 트렁크 기반 개발과 Git Flow를 같은 조건에서 직접 비교한 실증 연구는 찾지 못했다. 2장과 14장의 결정 기준이 원저자의 설명, 팀들의 전환 사례, 통합 빈도에 관한 연구를 엮어 추론한 것이라는 점을 기억해 주길 바란다.

그리고 가장 빠르게 움직이는 질문이 남아 있다. 14장 끝에서 방향만 적어 둔 AI 에이전트의 PR이다. 사람이 아닌 작성자가 동시에 수많은 PR을 연다면 리뷰는 어떤 모양이 되어야 할까. 두 축이 여전히 유효하리라는 데는 자신이 있지만, 그 위에 어떤 장치가 새로 필요해질지는 아직 누구도 확실히 말하지 못한다.

### 다음 걸음

책을 덮었다면 거창한 개편 계획 대신 작은 일 하나로 시작하자. 1장 끝에서 던진 질문, 우리 팀에서 브랜치가 `main`에서 갈라져 나와 다시 합쳐지기까지 며칠이 걸리는가를 이번 주 안에 숫자로 적어 보자. 최근 머지된 PR 스무 건쯤의 생성·첫 리뷰·승인·머지 시각을 나란히 적고, 4장 끝의 다섯 가지 설정 점검과 11장의 보안 점검표를 한 번씩 돌려 보는 것으로 충분하다. 그 숫자와 점검 결과가 14장에서 제안한 "싸고 효과가 큰 것부터" 순서의 첫 칸을 알려 줄 것이다.

더 깊이 읽고 싶다면 이 책이 여러 번 기대 선 원전으로 가 보길 권한다. Martin Fowler의 "Patterns for Managing Source Code Branches"는 통합 빈도라는 축을 가장 넓게 펼쳐 보이는 글이다. Vincent Driessen이 2020년에 Git Flow 원문 위에 덧붙인 반성 노트는 짧지만, 전략을 고르는 태도에 대해 이 책 전체보다 간결하게 말한다. Google의 엔지니어링 실무 가이드 가운데 small CLs 편은 5장의 출발점이었고, GitHub Security Lab의 pwn request 글은 11장의 뼈대가 됐다. 측정 쪽으로는 DORA의 지표 가이드가 있다. 모두 참고문헌에 주소를 적어 두었다.

마지막으로, 이 책의 "2026년 9월 기준"들은 시간이 지나면 하나씩 낡을 것이다. 그때 이 책에서 남기를 바라는 것은 숫자가 아니라 질문 두 개다. 우리는 얼마나 자주 합치는가. 우리가 검증한 것이 정말 머지된 것인가.

## 참고문헌

본문에서 인용하거나 근거로 삼은 자료다. 서지 정보와 확인 등급 표기는 이 책의 리서치 원장(`01_reference.md`, `research/*.md`)과 사실 확인 기록(`factcheck_log.md`)에 적힌 그대로 옮겼다. 유형별로 묶고, 각 묶음 안에서는 원장의 순서를 따랐다. "2026-09 조회"는 상시 갱신되는 문서를 2026년 9월에 확인했다는 뜻이다.

### 공식 문서·체인지로그

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
- Mergify. Merge Queue docs (batches, parallel checks, two-step). https://docs.mergify.com/merge-queue/batches/, https://docs.mergify.com/merge-queue/parallel-checks/, https://docs.mergify.com/merge-queue/two-step/, 2026-09 조회.

### 사실 확인 과정에서 대조한 자료

`factcheck_log.md`에 근거로 기록된 자료다. 원장에 적힌 만큼의 서지 정보만 옮겼다.

- GitHub Docs. Automatically merging a pull request. 2026-09 조회.
- GitHub Docs. Managing rulesets for a repository (managing-rulesets). 2026-09 조회.
- GitHub Docs. Available rules for rulesets (enterprise-cloud@latest). 2026-09 조회.
- GitHub Docs. Metadata syntax for GitHub Actions. 2026-09 조회.
- GitHub Docs. Automatic token authentication (GITHUB_TOKEN). 2026-09 조회.
- GitHub Docs. Using conditions to control job execution; About status checks. 2026-09 조회.
- GitHub. Immutable subject claims for GitHub Actions OIDC tokens. GitHub Changelog, 2026-04-23 (2026-06-10 editor's note).
- Vlad Fedorov. An update on GitHub availability. GitHub Blog, 2026-04-28.
- GitHub. actions/checkout v7.0.1 (2026-07-20), actions/setup-node v7.0.0 (2026-07-14), actions/cache v6.1.0 (2026-06-26), actions/upload-artifact v7.0.1 (2026-04-10), actions/download-artifact v8.0.1 (2026-03-11). GitHub 릴리스, 2026-09-26 조회.
- GitLab Docs. Merge trains. https://docs.gitlab.com/ci/pipelines/merge_trains, 2026-09 조회.
- Trunk Based Development. Branch for release. https://trunkbaseddevelopment.com/branch-for-release/, 상시.
- BleepingComputer, The Hacker News. tj-actions/changed-files 관련 보도 (Endor Labs 추산 218개 저장소, CVE-2025-30154 경유 PAT 획득 분석).

### 원저자·엔지니어링 블로그

- Google. Engineering Practices: Small CLs. https://google.github.io/eng-practices/review/developer/small-cls.html, 2019 공개.
- John Micco. Flaky Tests at Google and How We Mitigate Them. Google Testing Blog. https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html, 2016-05-27.
- Vincent Driessen. A successful Git branching model (+ Note of reflection). https://nvie.com/posts/a-successful-git-branching-model/, 2010-01-05 / 2020-03-05.
- GitLab. What is GitLab Flow. https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/; 원문 https://about.gitlab.com/blog/2014/09/29/gitlab-flow/, 2014-09-29.
- Paul Hammant 외. Trunk Based Development. https://trunkbaseddevelopment.com/, 상시.
- Martin Fowler. Patterns for Managing Source Code Branches. https://martinfowler.com/articles/branching-patterns.html, 2020-05-28.
- Adam Ruka. OneFlow – a Git branching model and workflow. https://www.endoflineblog.com/oneflow-a-git-branching-model-and-workflow, 페이지 표기 2017-04-30. / GitFlow considered harmful. https://www.endoflineblog.com/gitflow-considered-harmful, 2015.
- Pete Hodgson. Feature Toggles (aka Feature Flags). https://martinfowler.com/articles/feature-toggles.html, 2017-10-09.
- Will Smythe, Lawrence Gripper. How GitHub uses merge queue to ship hundreds of changes every day. GitHub Blog. https://github.blog/engineering/engineering-principles/how-github-uses-merge-queue-to-ship-hundreds-of-changes-every-day/, 2024-03-06.
- Darren Worrall. Introducing the Merge Queue. Shopify Engineering. https://shopify.engineering/introducing-the-merge-queue, 2018-06-08.
- Jack Li. Successfully Merging the Work of 1000+ Developers. Shopify Engineering. https://shopify.engineering/successfully-merging-work-1000-developers, 2019-11-14.
- bors-ng. This Month in Bors #76. https://bors.tech/newsletter/2023/04/30/tmib-76/, 2023-04-30. Graydon Hoare. Not Rocket Science Rule. https://graydon2.dreamwidth.org/1597.html, 2014 (조회 403).
- 백명석. 우아한테크세미나 "지속가능한 SW개발을 위한 코드리뷰". 우아한형제들 기술블로그. https://techblog.woowahan.com/8159/, 2022-04-19.
- 김성일. GitHub Actions로 개선하는 코드 리뷰 문화. 토스 기술블로그. https://toss.tech/article/25431, 2024-02-07.
- 우아한형제들 배민프론트개발팀 안드로이드 파트. 우린 Git-flow를 사용하고 있어요. https://techblog.woowahan.com/2553/, 2017-10-30.
- 맘시터(Mfort). Git Flow에서 트렁크 기반 개발으로 나아가기. https://tech.mfort.co.kr/blog/2022-08-05-trunk-based-development/, 2022-08-05.
- 뱅크샐러드. GitHub Action npm cache. https://blog.banksalad.com/tech/github-action-npm-cache/, 2022-08-29.

### 논문·연구

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
- Gousios, G., Pinzger, M., van Deursen, A. An Exploratory Study of the Pull-based Software Development Model. ICSE 2014, pp. 345-355. DOI 10.1145/2568225.2568260.
- Gousios, G., Zaidman, A., Storey, M.-A., van Deursen, A. Work Practices and Challenges in Pull-Based Development: The Integrator's Perspective. ICSE 2015, pp. 358-368. DOI 10.1109/ICSE.2015.55.
- Tsay, J., Dabbish, L., Herbsleb, J. Influence of Social and Technical Factors for Evaluating Contribution in GitHub. ICSE 2014, pp. 356-366. DOI 10.1145/2568225.2568315.
- Vasilescu, B., Yu, Y., Wang, H., Devanbu, P., Filkov, V. Quality and Productivity Outcomes Relating to Continuous Integration in GitHub. ESEC/FSE 2015, pp. 805-816. DOI 10.1145/2786805.2786850.
- Hilton, M., Tunnell, T., Huang, K., Marinov, D., Dig, D. Usage, Costs, and Benefits of Continuous Integration in Open-Source Projects. ASE 2016, pp. 426-437. DOI 10.1145/2970276.2970358.
- Hilton, M., Nelson, N., Tunnell, T., Marinov, D., Dig, D. Trade-offs in Continuous Integration: Assurance, Security, and Flexibility. ESEC/FSE 2017, pp. 197-207. DOI 10.1145/3106237.3106270.
- Bernardo, J. H., da Costa, D. A., Kulesza, U. Studying the Impact of Adopting Continuous Integration on the Delivery Time of Pull Requests. MSR 2018, pp. 131-141. DOI 10.1145/3196398.3196421.
- Bernardo, J. H., da Costa, D. A., Kulesza, U., Treude, C. The impact of a continuous integration service on the delivery time of merged pull requests. EMSE, 2023. DOI 10.1007/s10664-023-10327-6.
- Luo, Q., Hariri, F., Eloussi, L., Marinov, D. An Empirical Analysis of Flaky Tests. FSE 2014, pp. 643-653. DOI 10.1145/2635868.2635920.
- Memon, A. et al. Taming Google-Scale Continuous Testing. ICSE-SEIP 2017, pp. 233-242. DOI 10.1109/ICSE-SEIP.2017.16.
- Parry, O. et al. Surveying the developer experience of flaky tests. ICSE-SEIP 2022, pp. 253-262. DOI 10.1145/3510457.3513037.
- Machalica, M., Samylkin, A., Porth, M., Chandra, S. Predictive Test Selection. ICSE-SEIP 2019, pp. 91-100. DOI 10.1109/ICSE-SEIP.2019.00018.
- Henderson, T. A. D., Dorward, B., Nickell, E., Johnston, C., Kondareddy, A. Flake Aware Culprit Finding. ICST 2023, pp. 362-373. DOI 10.1109/ICST57152.2023.00041.
- Shihab, E., Bird, C., Zimmermann, T. The Effect of Branching Strategies on Software Quality. ESEM 2012, pp. 301-310. DOI 10.1145/2372251.2372305.
- Bird, C., Zimmermann, T. Assessing the Value of Branches with What-if Analysis. FSE 2012, pp. 1-11. DOI 10.1145/2393596.2393648.
- Ghiotto, G., Murta, L., Barros, M., van der Hoek, A. On the Nature of Merge Conflicts: A Study of 2,731 Open Source Java Projects Hosted by GitHub. IEEE TSE, pp. 892-915, 2020 (온라인 2018). DOI 10.1109/TSE.2018.2871083.
- Rahman, M. T., Querel, L.-P., Rigby, P. C., Adams, B. Feature Toggles: Practitioner Practices and a Case Study. MSR 2016, pp. 201-211. DOI 10.1145/2901739.2901745.
- Xu, G., Subramanian, A., Karthik, N. AI Agent Pull Requests on GitHub: Frequency, Structure, and Merge Conflict Rates. arXiv:2607.04697, 2026. (동료 심사 미확인)
- Ananthanarayanan, S. et al. Keeping Master Green at Scale. EuroSys 2019, pp. 1-15. DOI 10.1145/3302424.3303970. (원문 미확보 — 저자 슬라이드 sundaram.io/slides/eurosys19.pdf, The Morning Paper blog.acolyer.org 2019-04-18)
- Kinsman, T., Wessel, M., Gerosa, M. A., Treude, C. How Do Software Developers Use GitHub Actions to Automate Their Workflows? MSR 2021, pp. 420-431. DOI 10.1109/MSR52588.2021.00054.
- Wessel, M., Vargovich, J., Gerosa, M. A., Treude, C. GitHub Actions: The Impact on the Pull Request Process. EMSE, 2023. DOI 10.1007/s10664-023-10369-w.
- Bouzenia, I., Pradel, M. Resource Usage and Optimization Opportunities in Workflows of GitHub Actions. ICSE 2024. DOI 10.1145/3597503.3623303.
- Valenzuela-Toledo, P., Bergel, A., Kehrer, T., Nierstrasz, O. The Hidden Costs of Automation: An Empirical Study on GitHub Actions Workflow Maintenance. SCAM 2024. DOI 10.1109/SCAM63643.2024.00029 (arXiv:2409.02366).
- Rostami Mazrae, P., Decan, A., Mens, T., Wessel, M. An Empirical Study of the Evolution of GitHub Actions Workflows. arXiv:2602.14572, 2026. (저널 게재 미확인)
- Saroar, S. G., Nayebi, M. Developers' Perception of GitHub Actions: A Survey Analysis. EASE 2023, pp. 121-130. DOI 10.1145/3593434.3593475.
- Koishybayev, I. et al. Characterizing the Security of GitHub CI Workflows. USENIX Security 2022. https://www.usenix.org/system/files/sec22-koishybayev.pdf (DOI 없음).
- Muralee, S. et al. ARGUS: A Framework for Staged Static Taint Analysis of GitHub Workflows and Actions. USENIX Security 2023. https://www.usenix.org/system/files/usenixsecurity23-muralee.pdf (DOI 없음).

### 커뮤니티 (전부 커뮤니티 의견, 검증 필요)

- GitHub Community Discussion #193645 (머지 큐 squash 되돌림 인시던트), 2026-04. https://github.com/orgs/community/discussions/193645
- HN "GitHub Merge Queue Silently Reverted Code", 2026-04. https://news.ycombinator.com/item?id=47881672
- HN "Tj-actions/changed-files GitHub Action Compromised", 2025-03-14. https://news.ycombinator.com/item?id=43367987 (+ 43368870, 43382055)
- 데일리시큐. tj-actions 관련 보도. https://www.dailysecu.com/news/articleView.html?idxno=164700
- GitHub Community Discussion #182089, 2025-12-16. https://github.com/orgs/community/discussions/182089 ; HN 46309821 (2025-12-17), 46301772, 46291156
- GitHub Community Discussion #13690 (2022-03-28~), #26251, #44490, #177835 (path 필터 + 필수 체크)
- SK DEVOCEAN. 코드 리뷰 문화를 리뷰해 봐요 (PR Reminder Bot 개발 이야기). https://devocean.sk.com/blog/techBoardDetail.do?ID=165255, 게시일 미확인.
- 코멘토 개발팀. 리뷰는 버릇이다: 코드 리뷰 문화 되살리기. https://developer.comento.kr/post/code-review-culture-24-10-15, 2024-10-15.
- HN "The Theatre of Pull Requests and Code Review", 2025-09경. https://news.ycombinator.com/item?id=45371283
- youngju.dev. code-review-that-teaches. https://www.youngju.dev/blog/career/code-review-that-teaches (개인 블로그)
- HN "GitHub Stacked PRs", 2026-04경. https://news.ycombinator.com/item?id=47757495 ; GeekNews https://news.hada.io/topic?id=32001 ; Lobsters https://lobste.rs/s/sda7hr/your_github_pull_request_workflow_is (2023-12-06)
- HN flaky 스레드: 23493249 (2020-06), 47024638 (2026-02경), 42429601 (2024-12-18), 36513060
- HN "I hate GitHub Actions with passion", 2026-01경. https://news.ycombinator.com/item?id=46614558 ; Lobsters "GitHub Actions Is Slowly Killing Your Engineering Team" (Ian Duncan, 2026-02-05) https://lobste.rs/s/hkqnro/github_actions_is_slowly_killing_your ; HN 46909274 ; HN "The Pain That Is GitHub Actions" (2025-03-20) https://news.ycombinator.com/item?id=43419701
- velog. CI 빌드 시간 400% 개선하기. https://velog.io/@rhkrwngud445/CI-%EB%B9%8C%EB%93%9C-%EC%8B%9C%EA%B0%84-400-%EA%B0%9C%EC%84%A0%ED%95%98%EA%B8%B0-feat-Github-Action ; Discussion #18549
- GitHub Community Discussion #15254 (2022-04-20~), #151100, #14801 (2022-04-12~), #201908, #168145 (머지 큐 트리거 중복·상호 취소) https://github.com/orgs/community/discussions/168145
- The Hacker News. Claude Code GitHub Action flaw. https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html, 2026-06.
- Steve Berczuk. Timely reviews. https://steveberczuk.substack.com/p/timely-reviews
- HN 9744059 (2015-06-19); HN 22485489 (2020-03-04); Lobsters https://lobste.rs/s/o76cit/please_stop_recommending_git_flow (2020-03-05); velog https://velog.io/@gmlstjq123/Git-Flow-VS-Github-Flow
- HN "The merge vs. rebase debate", 2023-12-29~31. https://news.ycombinator.com/item?id=38800454 ; Mitchell Hashimoto gist https://gist.github.com/mitchellh/319019b1b8aac9110fcfb1862e0c97fb ; GeekNews https://news.hada.io/topic?id=22651
- HN 36707239 (merge queue GA, 2023-07-13); Lobsters "Replace Your CI With a Merge Queue" https://lobste.rs/s/drtmhv/replace_your_ci_with_merge_queue (2026-07-27)
