# 커뮤니티 리서치: GitHub·AWS·Cloudflare를 쓰는 개발자를 위한 CI/CD (+ AI 코딩 도구 시대의 팀 팁)

- 수집 시점: 2026-09-26
- 장르: tech-book / 슬러그: `cicd-github-aws-cloudflare`
- 주요 소스: Hacker News(Algolia API로 원문 댓글 직접 수집), Lobsters, GitHub Issues·Discussions, GeekNews, velog, Dev.to, 회사 기술 블로그(카카오엔터프라이즈 등)
- **라벨 규칙:** 이 문서의 모든 주장은 **커뮤니티 의견이며 검증이 필요하다**. 수치·날짜·버전은 web/fact-checker 단계에서 1차 소스와 대조해야 한다. 인용문은 원문 그대로 두었다(영문은 번역하지 않음. 저술 단계에서 번역·의역).

---

## 반복되는 고통·질문 (챕터 오프닝 소재)

### 패턴 1: "push → 기다림 → 빨간 X"의 피드백 루프 — CI YAML은 로컬에서 디버깅할 수 없다
여러 플랫폼에서 가장 많이, 가장 감정적으로 나오는 불만이다. "fix ci" 커밋이 줄줄이 쌓이는 경험.
- 출현 예시:
  - HN "I hate GitHub Actions with passion" (2026-01-14, https://news.ycombinator.com/item?id=46614558) — 글 인용을 받은 iamcalledrob: "The pain is real. I think everyone that's ever used GitHub actions has come to this conclusion. An ideal action has 2 steps: (1) check out the code, (2) invoke a sane script that you can test locally." (https://news.ycombinator.com/item?id=46615262)
  - 같은 스레드 btreecat: "If you can't run the same scripts locally (minus external hosted service/API) then how do you debug them w/o running the whole pipeline?" (https://news.ycombinator.com/item?id=46615347)
  - HN "The Pain That Is GitHub Actions" (2025-03, https://news.ycombinator.com/item?id=43419701) — deng: "testing/debugging pipelines becomes a nightmare", "Avoid YAML as much as possible, period."
  - Lobsters "GitHub Actions Is Slowly Killing Your Engineering Team" (2026-02, https://lobste.rs/s/hkqnro/github_actions_is_slowly_killing_your) — yorickpeterse: "there's no sensible way of testing (or even linting) GitHub's CI config locally." / Halkcyon: "I wish I could leave YAML forever and the programming languages that develop inside of it" / scraps: "you take a data structure language (xml, json, yaml, etc) and then put logic expressions in it"
  - 원글 Ian Duncan (2026-02-05, https://www.iankduncan.com/engineering/2026-02-05-github-actions-killing-your-team/) — 요약 보도: self-hosted runner를 써도 "fighting the expression syntax and the permissions model and the marketplace and the log viewer that crashes your browser". HN 토론 https://news.ycombinator.com/item?id=46900381
  - Dev.to 디버깅 가이드류 — "commit-push-wait-for-CI-fail" 사이클을 명시적 고통으로 지목 (https://dev.to/stelixx-insider/streamline-your-github-actions-workflow-with-act-4la7)
- 추정 원인 (커뮤니티가 공유하는 진단): 로직이 YAML+표현식에 박혀 있어 디버거·로컬 실행이 불가능. 플랫폼별 러너 이미지 차이로 "한 OS에서만 실패"가 생김 (g947o, https://news.ycombinator.com/item?id=46615402).

### 패턴 2: `act`는 "80%짜리" 로컬 대체재 — 복잡해지면 오히려 함정
- 출현 예시:
  - c0wb0yc0d3r: "I remember it NOT being a direct stand in locally. Like it covered 80% of use cases." (https://news.ycombinator.com/item?id=46615801)
  - figmert: "act is great, however, it has many shortcomings. Too often I've run into roadblocks... Simpler workflows work fine with it, but more complex workflows will be much harder. Don't put your logic in proprietary tooling. I have started writing all logic into mise tasks" (https://news.ycombinator.com/item?id=46615416)
  - xlii(원글 저자): "act is often mentioned as a drop-in replacement but I never got it to replicate GitHub actions environment." (https://news.ycombinator.com/item?id=46616510)
  - GitHub Issues: services 컨테이너(Postgres/MySQL) 네트워킹 실패 nektos/act#247 (https://github.com/nektos/act/issues/247), "act fails where GitHub CI succeeds" #2095 (https://github.com/nektos/act/issues/2095), 서드파티 액션 로컬 실패 #1750 (https://github.com/nektos/act/issues/1750)
  - 반대 목소리: Mattwmaster58 "It doesn't perfectly replicate the GH environment, but for my use case that doesn't matter and it's super nice to have." (https://news.ycombinator.com/item?id=46621914)
- 추정 원인: 기본 이미지가 GitHub 러너의 도구를 다 담지 않음, Linux 외 러너 불가, 멀티 컨테이너 네트워크 차이.
- 부수 팁(커뮤니티): 실패 러너에 SSH로 들어가기 — action-tmate는 종료 예정, upterm/action-upterm으로 대체 (figmert, https://news.ycombinator.com/item?id=46615436). "SSH into the machine after it fails" 기능이 내장돼야 한다는 요구 (palata, https://news.ycombinator.com/item?id=46616900).

### 패턴 3: 캐시가 빌드보다 느리다 / 캐시가 자꾸 식는다
- 출현 예시:
  - Blacksmith 블로그 HN 토론 "Reverse engineering GitHub Actions cache to make it fast" (2025-07, https://news.ycombinator.com/item?id=44658909) — 반론 bob1029: "I am struggling with justification for CI/CD pipelines that are so complex this kind of additional tooling becomes necessary."
  - GitHub Discussions: actions/cache restore가 느림 (https://github.com/orgs/community/discussions/25087), 모노레포 Nx 캐시 안전성 질문 (https://github.com/orgs/community/discussions/166480)
  - 벤더/블로그 계열 수치(검증 필요, 이해관계 있음): "~1.2 GB node_modules 캐시 복원 38초 vs warm npm ci 6초", "10 GB per-repo 캐시 한도로 eviction → warm 빌드가 cold로" (BuildPulse https://buildpulse.io/blog/github-actions-cache-optimization-benchmarks, Tenki https://tenki.cloud/blog/github-actions-cache-strategy)
  - self-hosted 러너에서 캐시가 퍼블릭 인터넷을 경유해 느리고 전송 비용 발생 (actuated https://actuated.com/blog/faster-self-hosted-cache; 한국 기술블로그 요약에도 동일 지적)
- 추정 원인: 캐시가 tarball → 원격 blob 저장소 왕복 구조. 캐시 키 설계 실패, 리포당 용량 한도.

### 패턴 4: GitHub Actions 자체의 신뢰성 — "또 죽었다"
- 출현 예시:
  - HN "GitHub Actions is shitting the bed again" (2026-03-05, https://news.ycombinator.com/item?id=47263825) — sidsud: "are they vibe coding their infra? lost count of how many incidents they've had in 2026 alone" / bracketfocus: "Sitting at 91% platform uptime over the last 90 days" (비공식 집계 사이트 인용, **검증 필요**) / yifanl: "Its a true marvel to barely have a single nine of uptime in 2026"
  - HN "GitHub Actions is the weakest link" (2026-04-28, https://news.ycombinator.com/item?id=47933257) — tomaytotomato: "Github actions is running like treacle now. Even when our company pays lots of money for cloud and private Github runners."
  - GeekNews "GitHub Actions가 다운됐음" (https://news.hada.io/topic?id=29908) — 한국 댓글은 거의 없고 HN 토론으로 연결됨
- 추정 원인(커뮤니티 추측, 근거 약함): Azure 이전, Copilot 리뷰 전면 도입으로 인한 부하, 누적된 기술 부채. **모두 추측이므로 책에서는 "개발자들이 이렇게 느꼈다"로만 사용.**
- 저술 활용: "CI 플랫폼 장애 시 배포를 어떻게 할 것인가(수동 배포 런북·대체 경로)"라는 챕터 소재.

### 패턴 5: 비용 — 분(minute) 요금과 self-hosted 러너 과금 소동
- 출현 예시:
  - GitHub가 2025-12-16 self-hosted 러너에도 분당 $0.002 "cloud platform charge"를 발표 → 반발 → 무기한 연기. GitHub Discussion #182186 (https://github.com/orgs/community/discussions/182186):
    - brtkwr: "Don't charge them the same per minute price as your own runners, that is just anti-competitive."
    - bhswilson: "We already pay for the control plane, to the tune of thousands of dollars."
    - eslym: "Many of us run self-hosted runners because we have idle hardware and we want to avoid burning through the plan's included minutes."
    - macintoshplus: "Charging for minutes on private runners is unacceptable for nonprofits."
  - HN "Pricing Changes for GitHub Actions" (819 댓글, https://news.ycombinator.com/item?id=46291156) — physicsguy: "There's always been this lesson with CI/CD - don't couple yourself to a specific product. If you do, you're gonna get screwed eventually. It happened with TravisCI, CircleCI, now it's happening with GitHub." / brightball: "I honestly don't have any issue paying the self-hosted runner fee."
  - HN self-hosted 경험: zackify "self hosted runner on bare metal with lxc containers for each runner. Cost savings are insane" (https://news.ycombinator.com/item?id=47732520); arusahni "our monthly bill is now flat because we pay for a server" 댓글에 과금 재개 가능성 경고 (https://news.ycombinator.com/item?id=48476246)
- **상충 정보(검증 필요):** 한국 블로그 youngju.dev(2026-03)는 "2026년 3월부터 self-hosted에도 $0.002 과금 시작"이라고 서술했으나, GitHub 공식 changelog·The Register·bex.co(2026-07)는 "연기/철회"로 보도. 1차 소스(https://github.blog/changelog/2025-12-16-coming-soon-simpler-pricing-and-a-better-experience-for-github-actions/, https://resources.github.com/actions/2026-pricing-changes-for-github-actions/)로 확인 필요. GitHub 호스티드 러너 가격 인하(보도상 최대 39%)도 수치 확인 필요.

### 패턴 6: AWS OIDC — "Not authorized to perform sts:AssumeRoleWithWebIdentity"
한국·해외 모두 가장 흔한 첫 배포 장벽. velog에 설정 튜토리얼이 대량 존재한다는 사실 자체가 신호.
- 출현 예시:
  - aws-actions/configure-aws-credentials Issues #318 (https://github.com/aws-actions/configure-aws-credentials/issues/318), #1137 (https://github.com/aws-actions/configure-aws-credentials/issues/1137), #1293 (https://github.com/aws-actions/configure-aws-credentials/issues/1293)
  - AWS re:Post 동일 질문 (https://www.repost.aws/questions/QUPqSGcz54SI-CTgAJ2jlHmg/issue-with-assuming-role-in-aws-using-github-actions-not-authorized-to-perform-sts-error)
  - velog: "[AWS] Github OIDC Provider 설정" (https://velog.io/@ninthsun91/AWS-Github-OIDC-Provider-%EC%84%A4%EC%A0%95), "github action과 ECS를 이용한 springboot 배포" (https://velog.io/@tngus3722/github-OIDC%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-ECR-upload)
- 추정 원인 (커뮤니티 진단): trust policy의 `sub`/`aud` 조건이 실제 토큰 클레임과 글자 단위로 불일치 — 특히 브랜치 push용으로 쓴 `sub`가 `pull_request`나 `environment:` 클레임과 안 맞는 경우, `aud`가 `sts.amazonaws.com`이 아닌 경우, `permissions: id-token: write` 누락. 디버깅 팁: actions-oidc-debugger로 디코딩된 JWT를 출력해 비교.
- **신선도 경고(검증 필요):** 한 블로그(decryptiondigest, https://www.decryptiondigest.com/blog/github-actions-oidc-aws-role-assumption-failures)는 "2026년 7월 이후 GitHub immutable subject claim에 옵트인한 리포는 기존 이름 기반 `sub` 조건으로 실패"라고 주장. GitHub 공식 changelog로 반드시 확인할 것.

### 패턴 7: ECS 배포가 "성공"으로 끝났는데 실제론 롤백됐다
- 출현 예시:
  - aws-actions/amazon-ecs-deploy-task-definition Issue #191 (https://github.com/aws-actions/amazon-ecs-deploy-task-definition/issues/191): "The GitHub action reports success in the case that the service stabilizes after a rollback is triggered by the circuit breaker" — 제안: 안정화 후 "the expected task revision is contained in the active deployment"인지 확인
  - aws/containers-roadmap #1488 "ECS Circuit Breaker doesn't rollback" (https://github.com/aws/containers-roadmap/issues/1488) — circuit breaker가 FAILED 상태에 머물고 롤백이 안 되는 사례; 단일 태스크 서비스는 실패 감지까지 약 100분이 걸린다는 보고(**검증 필요**)
  - 한국 사이드/학생 프로젝트 이슈들: "헬스체크 실패 시 이전 IMAGE_TAG로 되돌리고... 롤백까지 실패하면 명확히 실패" (https://github.com/B-TING/bu-ting-backend/issues/328), ":latest 대신 커밋 SHA로 이미지 태그 고정" (https://github.com/assistudy-toy/BE/issues/39)
- 추정 원인: "서비스 안정화 = 배포 성공"이라는 잘못된 가정, 헬스체크 경로·grace period 설정 미흡, 가변 이미지 태그.

### 패턴 8: Cloudflare Pages ↔ Workers 전환기의 혼란, wrangler 버전 이슈
- 출현 예시:
  - HN "Cloudflare recommends migrating from Pages to Workers" (2025-08-10, https://news.ycombinator.com/item?id=44853934) — merek: "I use AWS as a registrar, and I had to use Pages since Workers don't support 'Custom domains outside Cloudflare zones'... There's no way I can transfer the domain since I have subdomains tightly integrated with AWS services." (AWS DNS를 쓰는 팀에 직접 관련) / scottydelta: 리전 지정 불가로 Workers에서 Django로 이탈 — "Cloudflare provides it but only on enterprise plan."
  - Kenton Varda(Workers 테크 리드) 발언으로 전해지는 요지: "We are taking all the Pages-specific features and turning them into general Workers features" (2차 인용, https://cogley.jp/articles/cloudflare-pages-to-workers-migration — 원문 확인 필요)
  - cloudflare/workers-sdk #8851 "Problem with wrangler version 4 and deploying Pages" (https://github.com/cloudflare/workers-sdk/issues/8851) — 3.114.x는 되고 4.x는 실패(Vite 등이 만든 redirected config)
  - workers-sdk #10441 "Still having issues deploying worker via wrangler" (https://github.com/cloudflare/workers-sdk/issues/10441) — API 504 재시도 후 실패
  - Cloudflare Community: Pages→Workers 이전 시 "Missing entry-point to Worker script or to assets directory" (https://community.cloudflare.com/t/deploy-purely-static-from-github-moving-from-pages-to-workers/829966)
  - 한국 개인 리포 PR: `cloudflare/pages-action` 저장소 삭제로 "Unable to resolve action" → wrangler 직접 호출로 교체 (https://github.com/gooinsung/Leadpot/pull/14) — **액션 의존 자체가 리스크**라는 사례
  - wrangler 배포 시 `--branch=main` 누락하면 preview로 배포된다는 팁 (velog, https://velog.io/@milkskfk5677/Cloudflare-Pages)
  - willtemperley: "I've decided to ditch CF because Wrangler is deployed via NPM and I cannot bear NodeJS and Microsoft NPM anymore." (https://news.ycombinator.com/item?id=46461558)
- 추정 원인: 제품 통합기(Pages→Workers static assets), wrangler 메이저 버전 변경, 공식 액션 교체.

### 패턴 9: 공급망 — 태그는 움직인다 (tj-actions → Shai-Hulud → Mini Shai-Hulud)
- 출현 예시:
  - tj-actions/changed-files 침해(2025-03, CVE-2025-30066): Lobsters (https://lobste.rs/s/4ko499/popular_github_action_tj_actions_changed) — matklad: "It was obvious from day one that the lack of any kind of lock file in GHA is a giant vulnerability waiting to happen." / "always pin it by the hash...which is best effort only, as git hashes are not a security feature!" / alerque: "The projects most severely affected by this compromise were doing just this, and also running bots to bump the SHA commits... Hundreds of projects even auto-accept PRs bumping pinned hashes."
  - GeekNews "tj-actions/changed-files GitHub Action 해킹됨" (https://news.hada.io/topic?id=19770) — 한국 댓글은 dl57934 "어제 밤에 안되던데 지금은 또 되네요" 정도로 빈약, 논의는 HN 요약으로 대체됨
  - Coder가 피한 방법: "We achieve this by strictly pinning all GitHub Actions to specific commit hashes." (https://github.com/coder/coder/discussions/16993)
  - HN "GitHub Actions is the weakest link" (2026-04-28, https://news.ycombinator.com/item?id=47933257) — rmunn: 처음부터 SHA 고정, 동료는 "tags were secure enough" / maxloh: "GitHub Actions doesn't have a lock file, so your repo is still prone to transitive attacks" / koolba: "Even SHA pinning only lets you go one hop." / mmarian(반론): SHA 고정은 "lose vulnerability alerts, increase maintenance overhead" / AlecBG: "You can enforce at the org level to only allow actions pinned to hashes."
  - Shai-Hulud 사후 분석 (Trigger.dev, HN https://news.ycombinator.com/item?id=46262021) — "Running npm install is not negligence" 문장을 두고 격론
  - Mini Shai-Hulud(2026-05~): 감염된 GitHub Action이 2026-09-16 재활성화되어 다시 악성코드 실행 (보도: https://thehackernews.com/2026/09/compromised-github-actions-came-back.html) — **최신 사건, 날짜·범위 검증 필요**. 페이로드가 Claude Code·VS Code 훅을 리포에 커밋하고 Dependabot으로 위장한 워크플로를 주입한다는 보도(https://safedep.io/mini-shai-hulud-reinfection-github-repositories/)
- 추정 원인: 가변 태그, 락파일 부재, 전이 의존(composite action), CI에 과도한 시크릿, `CAP_SYS_PTRACE` 등 불필요 권한 (cyrnel, https://news.ycombinator.com/item?id=43925947).

### 패턴 10: AI 리뷰 봇 — 버그는 잡는데 소음이 더 크다
- 출현 예시:
  - HN "There is an AI code review bubble" (2026-01-26, https://news.ycombinator.com/item?id=46766961) — zmmmmm: "they do find critical bugs (from my retrospective analysis, maybe 80% of the time), but the signal to noise ratio is poor. It's really hard to get it not to tell you 20 highly speculative reasons why the code is problematic along with the one critical error." / jamesfinlayson: "a lovely loop of check against null rather than undefined, check against undefined rather than null etc." / storystarling: "I suspect the noise is largely an artifact of cost optimization. Most tools restrict the context to just the diff" / marginalia_nu: "a not insignificant part of the point of code reviews is to propagate understanding of the evolution of the code base among other team members." / greymalik: "Copilot has terrible signal noise. But Bugbot is incredible." (제품 평가는 사람마다 정반대)
  - Dev.to "Drowning in AI Code Review Noise" (https://dev.to/jet_xu/drowning-in-ai-code-review-noise-a-framework-to-measure-signal-vs-noise-304e)
  - velog 1인 개발자 CodeRabbit 도입기(2024-08): "도입이 쉬워서 5분만에 적용할 수 있었습니다", "혼자 개발하느라 놓쳤던 부분에 대해 도움을 받을 수 있겠다는 생각이 듭니다", 시(poem) 기능엔 "또 한편의 시가 나왔습니다 ㅋㅋㅋ" (https://velog.io/@heyday_xz/AI-%EC%BD%94%EB%93%9C%EB%A6%AC%EB%B7%B0-%EB%B6%99%EC%97%AC%EB%B3%B4%EA%B8%B0)
  - 한국 사례: W컨셉 프론트엔드 팀 Cursor 자동 리뷰 적용기 (https://medium.com/@wconceptTech/%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C-%ED%8C%80%EC%9D%B4-cursor-ai%EB%A1%9C-%EC%BD%94%EB%93%9C-%EB%A6%AC%EB%B7%B0%EB%A5%BC-%EC%9E%90%EB%8F%99%ED%99%94%ED%95%9C-%EC%A0%81%EC%9A%A9%EA%B8%B0-92990c6f1a87), "코드리뷰'조차' 이제 AI가 더 잘하나요?" (https://medium.com/@l2hyunwoo/%EC%BD%94%EB%93%9C%EB%A6%AC%EB%B7%B0-%EC%A1%B0%EC%B0%A8-%EC%9D%B4%EC%A0%9C-ai%EA%B0%80-%EB%8D%94-%EC%9E%98%ED%95%98%EB%82%98%EC%9A%94-9aa3ec4e8b15)
- 추정 원인: diff만 보는 컨텍스트, 기본값이 최대 민감도, "무엇이 nitpick인가"가 사람마다 질적으로 다름(Greptile 창업자 dakshgupta, https://news.ycombinator.com/item?id=46776408).

### 패턴 11: AI가 만든 PR 홍수와 리뷰 피로 — "코드가 리뷰보다 빨라졌다"
- 출현 예시:
  - GeekNews "코드는 다 읽을 수 없고, 코드 리뷰가 맡아온 책임은 사라지지 않는다" (https://news.hada.io/article/code-outruns-review): "사람이 코드를 읽고 검토할 수 있는 속도보다, 코드가 만들어지는 속도가 빨라진 것이 더 근본적인 변화" / "코드를 빨리 만들었다는 것은 일을 끝낸 것이 아니라, 그 코드가 작동한다는 증거를 만드는 단계로 일을 넘긴 것" / "AI 리뷰어를 붙이는 것만으로 좋은 리뷰 시스템이 만들어지지 않음"
  - GeekNews "AI 시대에 코드 리뷰에서 살아남는 방법은?" (https://news.hada.io/topic?id=33244) — koh3276: AI 코드는 자신감 있고 매끈해서 오히려 놓치기 쉬워 "이 함수를 깨뜨리려면 어떤 입력을 넣어야 하나"를 먼저 본다, 그럴듯한 존재하지 않는 API 호출을 자주 잡는다. (Lobsters 요약: 400줄 PR 상한, PR에 의도·근거·기각 대안 명시)
  - GeekNews "Git의 --author 플래그로 GitHub 저장소의 AI 봇 스팸을 막은 방법" (https://news.hada.io/topic?id=29642) — 한국 댓글: "GitHub가 이런 일이 가능하게 둔 게 문제임", "PR의 95% 이상이 거절되는 계정은 GitHub가 일시적으로 PR 생성을 막아야 할지도 모름", "작업 증명은 이메일에서 안 통했던 것처럼 여기서도 안 통함", 그리고 보안 지적 "저장소 기여자는 fork PR 실행의 승인 요구를 우회하는 등 더 높은 권한을 갖게 되므로, 이 방식에는 간과된 보안 영향이 있음"
  - HN "A standard protocol to handle and discard low-effort, AI-Generated pull requests" (2026-03, https://news.ycombinator.com/item?id=47267947) — danpalmer: AI로 만든 변경을 읽었지만 "I did not feel that I knew the codebase enough to be able to actually assess the correctness of the change" / zephyruslives: AI에게 더 물을수록 "fixed so many things to 'improve' the code that I completely lost all confidence in the change"
  - HN "Ask HN: Is anyone else sick of AI splattered code" (https://news.ycombinator.com/item?id=45278819) — nharada: "people aren't transparent about when they use AI" / Workaccount2: "You get shamed and dismissed for mentioning that you used AI, so naturally nobody mentions they used AI."
  - 오픈소스 측 보도: Jazzband 해산, curl 버그바운티 중단 등 (The New Stack https://thenewstack.io/ai-generated-code-crisis/ — **사실관계 검증 필요**), HN "PS3 Emulator Devs Politely Ask That People Stop Flooding It with AI PRs" (https://news.ycombinator.com/item?id=48089263)
- 추정 원인: 생성 비용≈0, 리뷰 비용 불변(보도상 PR당 30분+). 작성자가 설명 못 하는 PR.

### 패턴 12: CI 안의 AI 에이전트가 새 공격면이 되다
- 출현 예시:
  - Clinejection (2026-02): 이슈 제목 프롬프트 인젝션 → claude-code-action 트리아지 워크플로 → 캐시 포이즈닝 → 릴리스 토큰 탈취 → 약 4,000대 개발자 머신 감염 보도. HN (https://news.ycombinator.com/item?id=47263595) — yread: "configured the claude-code action with allowed_non_write_users: "*", meaning anyone with a GitHub account can trigger it... Has everyone lost their minds?" / Ukv: 워크플로는 `contents: read`라 안전하다고 주석까지 달았지만 캐시 경로로 뚫림 / hannob: "Clearly yes."
  - CodeRabbit RCE 공개 (2025-08, HN https://news.ycombinator.com/item?id=44953032) — PR 하나로 리뷰 봇 인프라 RCE, "write access on 1M repos" 주장. CodeRabbit 측 curuinor: "this RCE was reported and fixed in January... no customer data was affected" / progbits: "Someone could have taken the private github key and cloned your customers' private repos."
  - s1ngularity(Nx, 2025-08): 악성 패키지가 로컬 AI CLI를 `--dangerously-skip-permissions`/`--yolo`로 호출해 비밀을 수집 (보도 https://thehackernews.com/2025/08/malicious-nx-packages-in-s1ngularity.html, Nx 사후분석 https://nx.dev/blog/s1ngularity-postmortem)
- 추정 원인: 신뢰되지 않은 입력(이슈·PR 본문)이 도구 권한 있는 에이전트 프롬프트로 들어감. "읽기 전용"이어도 캐시·아티팩트 같은 옆길이 있음.

---

## 실무 휴리스틱

### 휴리스틱 1: 워크플로는 멍청하게, 로직은 로컬에서 도는 스크립트로
- 출처: https://news.ycombinator.com/item?id=46615411 (1a527dd5), https://news.ycombinator.com/item?id=46616526 (thiht)
- 원문:
  > "Don't have logic in your workflows. Workflows should be dumb and simple (KISS) and they should call your scripts. ... Having standalone scripts will allow you to develop/modify and test locally without having to get caught in a loop of hell." — 1a527dd5
  > "This is not even specific to GitHub Actions. The logic goes into the scripts, and the CI handles CI specific stuff (checkout, setup tooling, artifacts, cache...). No matter which CI you use, you're in for a bad time if you don't do this." — thiht
- 추천·동조 반응: 해당 스레드 최다 동조. 변형 — Makefile 얇은 래퍼(JanMa, HN 43419701), mise tasks(figmert, lucasew), make+nix(sebastien, Lobsters), 프로젝트 언어로 CI 구현(wheybags, Lobsters), "only implement your logic in a tool that has a debugger"(forrestthewoods).
- 반론: mlrtime "How do you orchrestate a full CI/CD pipeline where you need state? You just move that complex logic to another monolithic script with its own problems?" (https://news.ycombinator.com/item?id=46631469), 셸 vs 스크립팅 언어 논쟁(Storment33: "if you need anything more than shell that starts to become a smell").

### 휴리스틱 2: 액션은 SHA로 고정하고, 봇으로 갱신하되 자동 머지는 하지 마라
- 출처: https://github.com/coder/coder/discussions/16993, https://news.ycombinator.com/item?id=47936663 (arionmiles), https://lobste.rs/s/4ko499/
- 원문:
  > "I feel pretty happy we use ... Renovate at my current workplace which by default will raise PRs to change any tags for actions with the SHA instead. Then, even when it bumps the version in future PRs, it bumps the SHA (with a comment of which tag version it represents)" — arionmiles
- 추천·동조 반응: 도구 추천 다수 — pmw, frizbee, Renovate (https://news.ycombinator.com/item?id=43926389 스레드), 조직 수준 강제(AlecBG). 단 alerque의 경고(해시 bump PR 자동 수락 = 무의미)와 전이 의존(composite action) 한계가 꼭 따라붙음. GitHub Immutable Releases GA(2025-10, https://news.ycombinator.com/item?id=45772064) 반응: "Wait?! They weren't immutable before?"

### 휴리스틱 3: 배포 시크릿은 main(리뷰 후)에만, build/test 잡엔 시크릿 0
- 출처: Lobsters tj-actions 스레드 (https://lobste.rs/s/4ko499/)
- 원문:
  > "You can ensure your main branch (ie: post review) is the only one with deployment secrets, that workflows such as 'build/test' have no secrets at all" — insanitybit
  > "The production/release tokens should ideally not be on the same system as the ones doing regular CI." — ashishb
- 추천·동조 반응: GitHub Environments + OIDC `sub`를 `environment:prod`로 좁히는 방식과 자연스럽게 연결됨(저술 시 web 리서치로 보강). 필요 없는 권한(ptrace 등) 제거가 코드 감사보다 현실적이라는 cyrnel 의견(https://news.ycombinator.com/item?id=43925947).

### 휴리스틱 4: ECS 배포는 "안정화"가 아니라 "내가 올린 리비전이 active인가"로 판정
- 출처: https://github.com/aws-actions/amazon-ecs-deploy-task-definition/issues/191
- 원문:
  > "The GitHub action reports success in the case that the service stabilizes after a rollback is triggered by the circuit breaker"
- 추천·동조 반응: 한국 팀 이슈들에서 커밋 SHA 이미지 태그 + 헬스체크 실패 시 이전 태그 롤백 + 롤백 실패면 파이프라인 실패 패턴 반복 등장 (B-TING #328, assistudy-toy #39).

### 휴리스틱 5: AI 리뷰는 사람 리뷰의 "앞단 필터"로만 — 심각도 순으로 자기 평가하게
- 출처: https://news.ycombinator.com/item?id=46775638 (colechristensen), https://news.ycombinator.com/item?id=46772445 (thesurlydev)
- 원문:
  > "give it a number of things to list in order of severity and ... tell it to grade how serious of a problem it may be. The human reviewer can then look at the top ten list" — colechristensen
  > "I start with Claude Code reviewing a PR. Then I selectively choose what I want to bubble up to the actual review." — thesurlydev
  > "the top 3 or 4 are likely good ones to look deeper into." — furyofantares
- 추천·동조 반응: 한국 쪽도 "AI 리뷰는 맞춤법 검사 수준으로, 휴먼 리뷰는 AI가 놓치는 부분에" 식 결론이 반복됨. 반면 jjmarr: "all of my PRs go through Copilot before another human looks at it. It's almost always right." (https://news.ycombinator.com/item?id=46312740)

### 휴리스틱 6: 에이전트는 컨테이너 안에서, 푸시 권한 없이, 프로덕션과 단절
- 출처: HN "Ask HN: How are you LLM-coding in an established code base?" (https://news.ycombinator.com/item?id=46331367)
- 원문:
  > "We use claude code, running it inside a docker container... The docker container doesn't have git credentials, so claude code can see git history etc and do local git ops ... but not actually push anything without a review." — adzicg
- 추천·동조 반응: 테스트를 가드레일로(__mharrison__ "I use tests as guardrails"). 중요한 반론 avree: CLAUDE.md에 "프로덕션 연결 시 실행 금지"라고 쓴 것은 "doesn't 'prevent' Claude code from doing anything, what it does is insert these instructions into the context window" (https://news.ycombinator.com/item?id=46331909) — **지시문은 가드레일이 아니다, 권한이 가드레일이다**라는 책의 핵심 메시지 후보.

### 휴리스틱 7: CI 에이전트 워크플로 체크 — 누가 트리거할 수 있나, 어떤 도구를 주나, 캐시를 공유하나
- 출처: Clinejection HN 스레드 (https://news.ycombinator.com/item?id=47263595), CSA 연구노트 (https://labs.cloudsecurityalliance.org/research/csa-research-note-clinejection-prompt-injection-cicd-cache-p/)
- 원문:
  > "AI agent with full rights running on untrusted input in your repo?" — yread
- 추천·동조 반응: `allowed_non_write_users: "*"` 금지, Bash/WebFetch 등 도구 최소화, 트리아지용 워크플로와 릴리스 워크플로 간 캐시 키 분리. (구체 설정값은 공식 문서로 검증 필요)

### 휴리스틱 8: 모노레포는 path 필터만으론 부족 — affected graph + 불확실하면 fail-closed + main에서 전체 스위트
- 출처: https://news.ycombinator.com/item?id=49789947 (thedefaultman, 2026-09-21)
- 원문:
  > "In a monorepo, path filters alone are not enough. You want an affected graph (packages and tests), fail-closed when the graph is unsure, and a canary on main that still runs the full suite."
- 추천·동조 반응: 단일 발언(동조 확인 못 함). 원격 캐시(Nx) 안전성 질문은 GitHub Discussion #166480에 존재.

### 휴리스틱 9: 실제 의존성을 가진 PR별 프리뷰 환경은 초기 며칠 투자로 오래 간다
- 출처: https://news.ycombinator.com/item?id=44665560 (presentation)
- 원문:
  > "I invested a few days at the start of building my B2B SaaS company wherein on every deploy we automate branching our actual staging/production databases with Neon, spinning up a complete preview environment with all the real dependencies, applying all migrations to the real data, and running end to end tests on that environment. Once it was set up I almost never need to touch it"
- 추천·동조 반응: PR별 서브도메인 프리뷰를 어떻게 만드냐는 질문(hu3, https://news.ycombinator.com/item?id=45514891)이 여전히 올라옴 → 수요 확인. Cloudflare Workers/Pages의 브랜치 프리뷰, `wrangler deploy --temporary`(60분 임시 배포, simonw 체험 https://news.ycombinator.com/item?id=48610403 — **2026-06 신기능, 검증 필요**)가 소재.

### 휴리스틱 10: CI 벤더에 종속되지 마라 (가격은 오르기만 한다)
- 출처: https://news.ycombinator.com/item?id=46300269 (physicsguy)
- 원문: 패턴 5 인용 참조. 휴리스틱 1과 같은 결론(로직을 이식 가능한 스크립트로)에 비용 논리로 도달.

---

## 논쟁점

### 논쟁 A: GitHub Actions를 계속 쓸 것인가
- 관점 1: GHA는 "CI의 Internet Explorer", Buildkite 등으로 가야 한다 (Ian Duncan 글; gabrielgio "Buildkite is really good", https://news.ycombinator.com/item?id=46901094; pcthrowaway "My years using Concourse were a dream compared to the CI/CD pains")
  - 대표 발언: "Github Actions however, I'd say for someone coming from GitLab, is even worse to work with" — mschuster91 (HN 43419701)
- 관점 2: 도구 문제가 아니라 사용법 문제 — 스크립트로 빼면 어떤 CI든 괜찮다, 레포 옆에 있다는 통합성은 대체 불가
  - 대표 발언: "most CIs are fine if you just use them to bootstrap into your build system" — sebastien (Lobsters); 카카오엔터프라이즈 워크서버개발팀: 젠킨스 인스턴스 관리 부담에서 벗어나 "GitHub 페이지에서 바로 빌드 결과를 확인/실행"하는 점을 GHA만의 장점으로 꼽음 (https://tech.kakaoenterprise.com/180); GeekNews 요약 "GitHub의 대안은 있지만 대체재는 없다" (https://news.hada.io/topic?id=32104)

### 논쟁 B: CDK vs Terraform (vs OpenTofu/Pulumi/SAM)
- 관점 1: Terraform — 벤더 중립, plan/drift 도구가 성숙
  - 대표 발언: "Terraform, because the tooling around it is just much better for things like drift detection, showing planned changes, pipelines, etc." — superdeeda (HN 38268256, 2023 스레드지만 여전히 인용됨); "Terraform, when committed to git, provides organisational memory... And tfstate is hard" — sshine (https://news.ycombinator.com/item?id=48548439)
- 관점 2: CDK/CloudFormation — AWS 전용이면 진짜 언어의 추상화, 롤백이 조용함
  - 대표 발언: "CDK/CFN seems to work more reliably 'at scale' for commonly used stacks due to low drama rollbacks etc." — xyzzy123; "CDK is great if you are only using AWS but Documentation sucks." — mr_o47 (https://news.ycombinator.com/item?id=38268256)
- 관점 3: 둘 다 아님 — "SAM and vanilla CloudFormation are my choice" (mlhpdx); Pulumi 호평(here2learnstuff, https://news.ycombinator.com/item?id=46227231) vs "I have absolutely nothing good to say about Pulumi. Stay far, far away." (packetlost, https://news.ycombinator.com/item?id=46223255)
- 최신 변수: HashiCorp의 CDKTF 종료(HN "The future of Terraform CDK", 2025-12, https://news.ycombinator.com/item?id=46222165) → "We use OpenTofu it's pretty seamless" (smithcoin). BSL 라이선스 전환 이후 OpenTofu 선택지. **CDKTF deprecation 정확한 상태는 1차 소스 확인 필요.**
- 맥락 관점(danw1979, https://news.ycombinator.com/item?id=43238960): Terraform 불만은 대개 "someone managing inherently ephemeral infrastructure"의 시각 — 플랫폼 팀 관점과 앱 팀 관점이 다르다.

### 논쟁 C: SHA 고정은 충분한가, 과한가
- 관점 1: 필수. 태그는 움직인다 (Coder, rmunn, matklad)
- 관점 2: 불충분하거나 비용이 크다 — 전이 의존(koolba, maxloh, rileymichael), 취약점 알림 상실·유지보수 부담·Immutable Releases 보급 시 가치 0 (mmarian, https://news.ycombinator.com/item?id=47939129), 해시 bump 자동 머지하면 무의미(alerque)
- 관점 3: 코드 감사보다 권한 축소가 본질 (cyrnel)

### 논쟁 D: AI 리뷰 봇은 가치가 있나
- 관점 1: 있다 — 버그를 실제로 잡는다, 1인 개발·첫 필터로 유용 (zmmmmm의 80%, greymalik의 Bugbot 호평, jjmarr, velog 1인 개발자)
- 관점 2: 소음이 가치를 잡아먹고, 리뷰의 목적(지식 전파)을 지운다 (marginalia_nu, materialpoint "Most of the feedback is just sh*t"), 이해상충 — AI 리뷰 회사의 "AI 코드는 버그 1.7배" 보고서에 bogzz/jjmarr "Coderabbit is an LLM code review company so their incentives are the opposite. AI is terrible and you need more AI to review it." (https://news.ycombinator.com/item?id=46312740)
- 관점 3(보안): 리뷰 봇 자체가 공격면 — CodeRabbit RCE 스레드, vadepaysa "I cancelled my coderabbit paid subscription" (https://news.ycombinator.com/item?id=44955570)

### 논쟁 E: AI 사용을 PR에 밝혀야 하나 / AI 생성 코드를 받아야 하나
- 관점 1: 밝혀야 한다, 혹은 금지 — nharada; ardour.org "we've banned any and all LLM-generated code" (PaulDavisThe1st, https://news.ycombinator.com/item?id=46331080)
- 관점 2: 코드는 코드일 뿐 — "Code is code: it speaks for itself." (kstrauser, https://news.ycombinator.com/item?id=45279083); 밝히면 낙인찍혀서 아무도 안 밝힌다(Workaccount2)
- 관점 3: 작성자 책임 강화 — 변경을 이해하고 손으로 요약을 쓰라(strogonoff, https://news.ycombinator.com/item?id=47273408), "play with the code, try to break it, write more tests yourself"(lawn)

### 논쟁 F: self-hosted 러너 — 절감인가 부담인가
- 관점 1: 베어메탈/LXC로 "Cost savings are insane"(zackify), 월 고정비(arusahni), 한국 블로그들도 Spot·커스텀 이미지로 절감 보고 (채널톡 GitHub Actions 도입기, 버즈빌 K8s 러너 https://tech.buzzvil.com/blog/%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%EC%97%90%EA%B2%8C-github-actions-%EC%84%A4%EC%B9%98%EC%97%90-%EB%8C%80%ED%95%B4-%EB%AC%BB%EB%8B%A4/, 다나와 https://danawalab.github.io/common/2022/08/24/Self-Hosted-Runner.html)
- 관점 2: 운영·보안 부담(퍼블릭 리포의 self-hosted 러너 위험, 캐시 경로 문제), 그리고 GitHub가 언제든 과금할 수 있다는 플랫폼 리스크

### 논쟁 G: Cloudflare를 AWS 앞에 둘 것인가
- 관점 1: DNS/CDN/Workers를 앞단에 두는 조합은 흔하다 (sebst "cloudflare DNS in front of AWS infra", https://news.ycombinator.com/item?id=46862011)
- 관점 2: 비용·결합도 우려 — "AWS is still not part of the Bandwidth Alliance... if you put a 3rd party CDN in front of AWS you can still end up paying a lot more in egress fees" (sagiba, https://news.ycombinator.com/item?id=48334483, **검증 필요**); 장애 전파 — Cloudflare 2025-11-18 장애 사후분석 HN(916 댓글, https://news.ycombinator.com/item?id=45973709)에서 abalone: "Their bot management system is designed to push a configuration out to their entire network rapidly... it creates risk as compared to systems that roll out changes gradually." → **점진 배포(progressive rollout)** 교훈으로 연결 가능
- 관점 3: 외부 DNS(Route 53) 유지 시 Workers 커스텀 도메인 제약 (merek, 패턴 8)

---

## 수집 한계
- **미접근 플랫폼:** Reddit(r/devops, r/aws, r/github, r/CloudFlare, r/ExperiencedDevs)은 크롤러 차단으로 원문 수집 불가 — 검색 요약에 "Reddit에서도"라고 언급된 2차 인용만 있음, 직접 인용 없음. X·Mastodon·Discord/Slack 로그, OKKY(검색 결과에 원문 스레드 미노출), 커리어리, 네이버 카페도 원문 미확보. Stack Overflow 대신 GitHub Issues·AWS re:Post로 대체.
- **언어 편중:** 영어(HN·Lobsters·GitHub) 약 80%. 한국 소스는 GeekNews(댓글 수가 적고 대부분 HN 요약 GN⁺ 봇), velog 튜토리얼·도입기, 학생/사이드 프로젝트 GitHub 이슈, 카카오엔터프라이즈·채널톡·버즈빌·다나와 기술블로그 정도. 우아한형제들·토스의 CI/CD 관련 커뮤니티성 글은 이번 수집에서 확보하지 못함(web-researcher에 위임 권장). 한국 실무자의 "날것 감정" 인용이 부족 — 오프닝 소재는 영어 인용 번역 의존도가 높음.
- **주제 공백:** Lambda 배포 함정(콜드스타트·버전/별칭·SAM vs CDK 배포 실패)에 대한 커뮤니티 토론 원문을 못 찾음. flaky test 대응(재시도·격리) 토론도 HN에서 유의미한 스레드를 못 찾음 — 벤더 글 위주. 롤백 "무용담"은 ECS 이슈와 Cloudflare 장애 외 개인 서사가 부족.
- **신선도·검증 필요 항목(fact-checker 대조용):** GitHub self-hosted 러너 $0.002/분 과금 현재 상태(연기 vs 시행, 소스 간 상충), 호스티드 러너 가격 인하율, OIDC immutable `sub` 클레임 변경(2026-07 주장), Mini Shai-Hulud 액션 재활성화(2026-09-16), Clinejection 피해 규모(~4,000대), CDKTF 종료 상태, `wrangler deploy --temporary`, Cloudflare Pages→Workers 기능 동등성 주장(2026-03), GitHub 가용성 "91%"(비공식 집계).
- **익명성:** HN·Lobsters 발언자는 대부분 닉네임뿐 — 경험 주장(비용 절감률, 탐지 시간 등)은 개인 일화로만 취급할 것. 벤더 블로그(Blacksmith, Tenki, BuildPulse, CodeRabbit, Greptile) 수치는 이해관계가 있다.
