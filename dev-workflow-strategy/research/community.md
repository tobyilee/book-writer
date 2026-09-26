# 커뮤니티 리서치: 개발 워크플로 전략 (브랜치·PR·코드 리뷰·CI·GitHub Actions·Merge Queue)

> 검색 시점: 2026-09-26. 모든 인용은 **커뮤니티 의견, 검증 필요**. 인용문은 원문 그대로 두었다(영문은 원문, 괄호 안은 번역 요지).
> 수치·날짜 중 공식 발표가 있는 것은 [공식 대조 필요] 표시 — web.md 쪽 1차 소스(GitHub Blog·Changelog·CISA 등)와 fact-checker 대조 권장.
> HN 댓글 인용은 WebFetch 요약을 거쳐 추출된 것이라 문장 일부가 축약됐을 수 있다. 책에 직접 인용할 때는 원문 링크에서 한 번 더 확인할 것.

---

## 챕터 오프닝용 장면 (가장 생생한 것 우선)

### 장면 1: 머지 큐가 머지된 코드를 조용히 되돌린 날 (2026-04-23)
- 무슨 일: GitHub 머지 큐에서 squash 방식 + 머지 그룹에 PR 2개 이상일 때 잘못된 머지 커밋이 생성되어, 앞서 머지된 PR의 변경이 뒤 PR 머지로 **되돌려졌다**. 16:05~20:43 UTC. 원인은 미공개 기능용 새 머지 베이스 계산 경로가 feature flag 게이팅 누락으로 squash 머지 그룹에 적용된 것. merge/rebase 방식 그룹과 머지 큐 밖 PR은 영향 없음, 커밋 자체는 Git에 남아 데이터 손실은 없었다고 GitHub 설명. [공식 대조 필요]
  - GitHub 인시던트 스레드: https://github.com/orgs/community/discussions/193645
  - 영향 규모 수치가 출처마다 다름: 인시던트 요약 "658 repositories, 2,092 PRs"(초기 230 repo에서 상향), HN에서 인용된 Kyle Daigle 발언 "2,804 PRs out of over 4 million merged on April 23". [공식 대조 필요 — 수치 충돌]
- HN 스레드 "GitHub Merge Queue Silently Reverted Code" (2026-04): https://news.ycombinator.com/item?id=47881672
  - matthewbauer: "Merge Queue was silently reverting changesets in the merge queue."
  - MarkMarine: "4 people spent hours putting our repo back together at my company." (우리 회사는 4명이 몇 시간 동안 저장소를 복구했다)
  - EdwardDiego: "This has caused a morning of fun for our team, how do you break one of the most fundamental bits?"
  - LiquidityC: "This happened in complete silence and since the PR was just code refactor I would most likely never noticed." (리팩터링 PR이라 아마 영영 몰랐을 것)
  - Randalthorro: "Imagine you pay someone to save your family pictures but sometimes they save only half your data."
  - acid__: "This was a pain to clean up!"
  - classified: "How long will users put up with this before they finally leave?"
- 오프닝 활용: "머지 큐는 main이 깨지지 않게 하려고 도입했다. 그런데 그 머지 큐가 main을 조용히 망가뜨렸다면?" — 도구에 대한 신뢰와 '검증된 것과 머지된 것이 같은가'라는 머지 큐의 핵심 질문을 동시에 던질 수 있다.

### 장면 2: 태그를 믿었던 23,000개 저장소 — tj-actions/changed-files (2025-03)
- 무슨 일: 공격자가 봇의 PAT를 탈취해 tj-actions/changed-files의 **기존 버전 태그(v35, v44.5.1 등)를 전부 악성 커밋으로 재지정**. 워크플로가 러너 메모리에서 시크릿을 뽑아 빌드 로그에 출력 → 공개 저장소에서는 로그가 곧 유출. CVE-2025-30066 (CVSS 8.6). 약 23,000개 저장소 사용, 국내 보도 기준 최소 218개 저장소 시크릿 노출. SHA로 고정한 사용자는 영향 없음. 발단은 reviewdog/action-setup(CVE-2025-30154) 연쇄, Coinbase 표적 공격에서 확산되었다는 분석(Unit 42). [공식 대조 필요]
  - CISA 경보: https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction
  - 데일리시큐(국내 보도): https://www.dailysecu.com/news/articleView.html?idxno=164700
- HN "Tj-actions/changed-files GitHub Action Compromised – used by over 23K repos" (2025-03-14): https://news.ycombinator.com/item?id=43367987
  - rarkins (Renovate 메인테이너): "git tags are [not] immutable, especially if they are in semver format. Although it's rare for such tags to be changed, they are not immutable by design" (요약 과정에서 부정어가 흐려졌을 수 있음 — 원문 확인 필요)
  - srvaroa: "many people mistakenly assume that git tags are immutable"
  - remram: "People don't pin versions. Referencing a tag is not pinning a version, those can be updated"
  - mixologic: "All the version tags got relabeled to point to a compromised hash. Semver does nothing to help with this. your build should always use hashes and not version tags"
  - harrisi: "the way people run CI/CD is just listing a random repository on GitHub"
  - junon: "This is an insane default from GH."
- 추가 HN 스레드: https://news.ycombinator.com/item?id=43368870 , https://news.ycombinator.com/item?id=43382055
- 오프닝 활용: `uses: tj-actions/changed-files@v45` 한 줄. 우리가 '버전'이라고 믿은 것이 사실은 언제든 옮겨 붙일 수 있는 포스트잇이었다.

### 장면 3: 셀프호스트 러너에 통행료를 매기겠다던 이틀 (2025-12-16~18)
- 무슨 일: GitHub이 2026-03-01부터 셀프호스트 러너 사용에 분당 $0.002 플랫폼 요금을 부과한다고 발표(동시에 호스트 러너 가격은 최대 39% 인하). 이틀 만에 "재검토를 위해 연기". 2026년 중반 기준 미시행, 재도입 일정 미발표. [공식 대조 필요]
  - GitHub Changelog: https://github.blog/changelog/2025-12-16-coming-soon-simpler-pricing-and-a-better-experience-for-github-actions/
- GitHub Community Discussion #182089 "Per minute charges for self hosted runners? Wtf?" (2025-12-16): https://github.com/orgs/community/discussions/182089
  - JC3: "Why are you going to charge per minute for self hosted runners? Those minutes are MY processing time"
  - alexkiro: "How can they justify per-minute charges when it's MY machine that runs it. If I have a crappy machine I need to pay GitHub more???"
  - eplightning: "Github-hosted runners are both insanely overpriced and underpowered."
  - Qix-: "Complete insult to those of us who have been here for over a decade who touted GH as a reputable service"
- HN "GitHub walks back plan to charge for self-hosted runners" (2025-12-17): https://news.ycombinator.com/item?id=46309821
  - ZuoCen_Liu: "The primary reason teams use self-hosted is not to save money, but for security (VPC access) and specialized hardware (GPUs/ARM)."
  - jjgreen: "Postponed, not abandoned."
- 관련 HN: https://news.ycombinator.com/item?id=46301772 , https://news.ycombinator.com/item?id=46291156
- 오프닝 활용: 러너 선택(호스트 vs 셀프호스트)이 순수 기술 결정이 아니라 비용·보안·벤더 의존 결정이라는 점.

### 장면 4: 3년째 열려 있는 "경로 필터 + 필수 체크" 이슈 (모노레포)
- GitHub Community Discussion #13690 (2022-03-28 개설, 👍101): https://github.com/orgs/community/discussions/13690
  - 증상: 워크플로에 `paths` 필터를 걸고 그 체크를 브랜치 보호의 필수 체크로 지정하면, 해당 경로를 안 건드린 PR은 체크가 영원히 "대기 중" → 머지 불가.
  - joegaudet (2022-11-03): "we've been asking for it for 3 years now, the only way to safely protect branches in this scenario is to run all checks always."
  - annabkr (2023-01-24): "Came here to add to the chorus of programmers asking for help with this sad trombone UX."
  - hankhsu1996 (2024-11-18): "Something as basic as skipping jobs based on file changes shouldn't require this level of convoluted hacking."
  - wAuner (2025-08-02): "Since 2022, this glaring issue has remained unresolved and unimplemented. This is not a feature request; it's a genuine problem."
  - joshuat (2026-08-10): "this is a feature I almost do not comprehend is missing and is routinely one of the reasons I look at moving us away from GH Actions."
- 동류: #26251 https://github.com/orgs/community/discussions/26251 , #44490 https://github.com/orgs/community/discussions/44490
- 커뮤니티 공유 우회책: 워크플로 수준 path 필터 대신 "detect-changes" 잡 하나에서 변경 경로를 계산하고 하위 잡이 `needs` + `if`로 스스로 스킵, 그리고 항상 도는 집계(ci_done) 잡 하나만 필수 체크로 지정. (skip된 잡은 success가 아니라는 점이 핵심 함정.)
- 오프닝 활용: 모노레포 CI 장의 첫 장면 — "안 건드린 서비스의 테스트 때문에 PR이 머지 버튼 앞에서 멈춘다."

### 장면 5: 매일 아침 9시, 슬랙에 쌓이는 PR 목록 (한국)
- SK DEVOCEAN "코드 리뷰 문화를 리뷰해 봐요 (PR Reminder Bot 개발 이야기)": https://devocean.sk.com/blog/techBoardDetail.do?ID=165255 (게시일 미확인)
  - "구성원이 많아지면서 PR이 쌓이는 속도가 점점 빨라지기 시작했습니다."
  - "매일 매일 쌓여가는 PR과 함께 몰려 오는 불안감"
  - "기능 개발이 바쁠 경우 자연스럽게 후순위로 밀리게 된다."
  - "변경 사항의 사이즈가 커서 리뷰하는 데 있어 확인해야 하는 범위가 크고 부담으로 다가온다."
  - 대응: PR 템플릿(요구사항·핵심 변경·리뷰 포인트), Pn 룰(우선순위 레이블), D-n 룰(리뷰 마감일), 평일 09시 슬랙 리마인더 봇.
- 코멘토 개발팀 "리뷰는 버릇이다: 코드 리뷰 문화 되살리기" (2024-10-15): https://developer.comento.kr/post/code-review-culture-24-10-15
  - "수많은 개발팀이 채용 공고에서 우리는 코드 리뷰 문화가 있다고 내세웁니다."
  - "그렇게 한 번 두 번 리뷰를 하지 않다 보면 어느새 리뷰되지 않는 코드가 더 많아지는 날이 찾아옵니다."
  - 대응: 전원 리뷰 참여, 업무일 1일 이내 리뷰, 배포와 리뷰 분리.
- 오프닝 활용: 채용 공고의 "코드 리뷰 문화 있음"과 실제 슬랙 채널의 간극.

---

## 반복되는 고통·질문

### 패턴 1: 큰 PR은 리뷰되지 않는다 — 방치되거나, 읽지 않고 승인되거나
- 출현 예시:
  - DEVOCEAN(한국): 위 장면 5 — "변경 사항의 사이즈가 커서 … 부담으로 다가온다."
  - Dev.to (Hasura 사례): https://dev.to/noriste/improving-hasuras-internal-pr-review-process-1ham — PR이 평균 7일 열려 있었고 일부는 171.3시간. (회사 블로그성 글, 검증 필요)
  - HN "The Theatre of Pull Requests and Code Review" (2025-09경, 416 댓글): https://news.ycombinator.com/item?id=45371283
    - nitwit005: "It's going to be cheaper to just have a chat with your coworker when a PR is confusing."
  - 한국 블로그 요지: "말투 문제로 보이는 갈등의 상당수는 사흘을 기다린 뒤 받은 지적이라서 크게 느껴지는 경우" — https://www.youngju.dev/blog/career/code-review-that-teaches (개인 블로그, 검증 필요)
- 커뮤니티가 공유하는 진단: 큰 변경일수록 리뷰어의 인지 부하가 커져 "내일 볼게" 또는 대충 읽고 LGTM으로 양극화. 러버스탬프와 의무적 nitpick은 같은 뿌리 — 결정이 이미 끝난 뒤, 평가하기엔 너무 큰 변경을 리뷰하기 때문(Dev.to "LGTM Culture": https://dev.to/pyor/lgtm-culture-when-code-review-becomes-theatre-28k).
- 2026년 변수 — AI 생성 PR: "PR이 커지고 아무도 읽지 않는다"는 글과 보고서가 급증. 한 보고서는 AI 고도 도입 조직에서 PR 크기 +51%, 리뷰 대기 중앙값 +441%, 무리뷰 머지 +31%를 주장(https://agentconn.com/blog/10x-prs-1x-reviewers-code-quality-bottleneck-gate-2026/ — 출처 신뢰도 낮음, 수치 인용 전 원 연구 확인 필수). GitHub이 AI slop PR 대응으로 "PR kill switch"를 검토한다는 보도(2026-02): https://www.opensourceforu.com/2026/02/github-weighs-pull-request-kill-switch-as-ai-slop-floods-open-source/

### 패턴 2: 스택 PR에 대한 오래된 갈증
- HN "GitHub Stacked PRs" (2026-04경, 약 900점/528댓글로 추출됨 — 수치 확인 필요): https://news.ycombinator.com/item?id=47757495
  - adamwk: "It makes both reviewing and working on long-running feature projects so much nicer."
  - calebio: "I miss the Phabricator review UI so much."
  - jenadine: "Git itself already has the concept of commit. Why put this 'stacked PR' abstraction on top of it?"
  - saagarjha: "A unit of change is a commit. I have no idea why you'd think a PR is a unit of change."
- GitHub Changelog: Stacked PR 공개 프리뷰 2026-07-30 https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/ [공식 대조 필요]
- GeekNews "GitHub Stacked PR 공개 프리뷰 시작": https://news.hada.io/topic?id=32001 — 우려: "해결되지 않은 문제가 많은 상태에서 대상을 확대", 스쿼시 머지 + 필수 리뷰 조합 시 재승인 요구, 스택 상태가 드롭다운에 표시되지 않음.
- Lobsters "Your GitHub pull request workflow is slowing everyone down" (2023-12-06, Graphite 글): https://lobste.rs/s/sda7hr/your_github_pull_request_workflow_is
  - 반응이 갈림: tazjin은 스택 워크플로가 실제로 "frustration levels"를 낮춘다고, Diana는 "commits go directly to main. No branch. No PR."(트렁크 기반)을, anordal은 문제는 GitHub이 커밋을 리뷰 단위로 보여주지 않는 것(Gerrit처럼)이라고 봄. crustacean은 벤더 마케팅이라고 경계.
- 진단: 리뷰 단위(PR)와 이력 단위(커밋)를 GitHub UI가 섞어 놓았다는 불만이 반복된다.

### 패턴 3: 플래키 테스트 — "그냥 재실행 눌러"가 문화가 되는 순간
- HN (2020-06, 인용 댓글 스레드): https://news.ycombinator.com/item?id=23493249
  - smarterclayton: "once anyone anywhere thinks 'oh it's just flaky' they stop treating it like signal. Once they treat it like noise, it's very hard to unwind"
  - mdoms: "I have a zero tolerance policy for flaky tests. In code bases where I have the authority, I immediately remove flaky tests"
  - hinkley: "your one bad test is going to fail every week or two...now builds are failing 2x a day on average"
  - l0b0: "nobody even bothers checking whether it's a 'real' failure until it's failed a few times in a row"
- HN "Flaky Tests Are Not a Testing Problem. They're a Feedback Loop You Broke" (2026-02경): https://news.ycombinator.com/item?id=47024638
  - 본문: "Every retry rule in your CI pipeline is a painkiller." / "Retries, quarantining, adding waits - these aren't fixes."
- HN "Faster continuous integration builds at Canva" (2024-12-18): https://news.ycombinator.com/item?id=42429601
  - dan_sbl: flaky 문제는 "should have been addressed first, not last."
  - nijave: "flakey/slow/expensive CI is also an orange/red flag you're lacking in developer experience/productivity."
  - maccard: "throwing more resources and money at the problem often shows significantly diminishing returns"
- 머지 큐와의 연결: 머지 큐에서는 플래키 하나가 그룹 전체를 떨어뜨리므로 고통이 증폭된다(Discussion #168145 "PR repeatedly removed from merge queue due to failed status checks": https://github.com/orgs/community/discussions/168145). [오귀속 — 실제는 트리거 중복·상호 취소 (13장 fact-check 확인)]

### 패턴 4: GitHub Actions의 피드백 루프 — push하고 기다리고, 또 push
- HN "I hate GitHub Actions with passion" (2026-01경): https://news.ycombinator.com/item?id=46614558
  - woodruffw: "the lack of a tight feedback loop. Pushing and waiting for completion on what's often a very simple failure mode is frustrating."
  - modeless: "It's insane to me that being able to run CI steps locally is not the first priority of every CI system."
  - danpalmer (act에 대해): "you have to make a lot of decisions to support Act. It in no way 'just works'"
  - mmcnl: "It's just YAML files with unlimited configuration options that have very limited documentation"
  - tracking1: "The less I rely on Github Actions environment the happier I am"
- Lobsters "GitHub Actions Is Slowly Killing Your Engineering Team" (2026-02-05, Ian Duncan): https://lobste.rs/s/hkqnro/github_actions_is_slowly_killing_your
  - yorickpeterse: "there's no sensible way of testing (or even linting) GitHub's CI config locally."
  - Riolku: "The back button in the GitHub Actions UI is a roulette wheel. You will land somewhere. It will not be where you wanted to go."
  - sebastien: "most CIs are fine if you just use them to bootstrap into your build system. I typically use make and nix or mise"
  - HN 동일 글 스레드: habosa "GitHub Actions is the worst CI tool I've ever used (maybe tied with Jenkins)" https://news.ycombinator.com/item?id=46909274 ; tcoff91 "What kills me is when these things add like control flow constructs to YAML. Like just use an actual programming language!"
- HN "The Pain That Is GitHub Actions" (2025-03-20): https://news.ycombinator.com/item?id=43419701
  - deng: "testing/debugging pipelines becomes a nightmare" / "Avoid YAML as much as possible, period."
- GeekNews "GitHub의 대안은 있지만 대체재는 없다" (2026년 중반 추정): https://news.hada.io/topic?id=32104 — Ghostty(Mitchell Hashimoto)가 Actions 장애로 약 2시간 PR 리뷰를 못 했다는 사례 언급.
- 커뮤니티 공유 휴리스틱: 워크플로 YAML은 얇게, 로직은 make/스크립트/nix 등 로컬에서 도는 빌드 시스템으로. (아래 휴리스틱 3)

### 패턴 5: CI 대기 시간과 캐시
- 뱅크샐러드 기술블로그 (2022-08-29): https://blog.banksalad.com/tech/github-action-npm-cache/
  - "action이 실행되고 이를 기다리는 시간은 지루하고 아깝습니다"
  - "하나의 action이 3분이 걸린다면 20명의 동료들이 한 번씩만 사용한다고 하더라도 1시간이 허비될 수 있습니다"
  - 의존성 설치 1분 8초 → 21초, 전체 CI 약 40초 (캐시·병렬화·변경분만 테스트).
- velog 사례들: "CI 빌드 시간 400% 개선하기" https://velog.io/@rhkrwngud445/CI-%EB%B9%8C%EB%93%9C-%EC%8B%9C%EA%B0%84-400-%EA%B0%9C%EC%84%A0%ED%95%98%EA%B8%B0-feat-Github-Action (15~19분 CI 사례 언급)
- 캐시의 함정(커뮤니티·벤더 글): 저장소당 캐시 10GB 한도, 셀프호스트 러너에서 캐시가 느리거나 멈춤(Discussion #18549 https://github.com/orgs/community/discussions/18549), 캐시 복원만으로 잡당 수십 초. 벤더 벤치마크 글이 많아 수치 신뢰도 낮음 — 검증 필요.

### 패턴 6: 머지 큐 설정 함정 — 큐가 "멈춘다"
- Discussion #15254 "Why does our Merge Queue get stuck?" (2022-04-20): https://github.com/orgs/community/discussions/15254
  - 원인 1: CI가 `gh-readonly-queue/{base}/**` 브랜치(또는 `merge_group` 이벤트)에서 트리거되지 않음 → 필수 체크가 영원히 대기.
  - 원인 2 (원 게시자): "The issue was that we had no required status checks set. After setting one, it started to work."
  - 2026년 댓글: "the required merge-queue checks were never produced and the head entry hung in AWAITING_CHECKS, blocking ~23 PRs."
  - GitHub 측 권장 복구: 큐 헤드 제거 → 큐 비우기 → 머지 큐 끄고 다시 켜기.
- Discussion #151100: 큐가 `merge_group` 이벤트가 아닌 `pull_request` 이벤트의 체크 결과를 보고 판단한다는 보고. https://github.com/orgs/community/discussions/151100
- Discussion #14801 "Merge Queue Feedback" (2022-04-12, 베타 시절): https://github.com/orgs/community/discussions/14801
  - danlucraft (2022-07-20): "queue with 8 PRs, that is going to take 2 hours to clear because our build takes 30 mins and the 2-build limit"
  - jgoux (2022-08-18): "the CI is running against the exact same code, it's unnecessary"
  - benjaminmurphy: 큐 헤드 PR이 통과했는데 "was waiting on the request _behind_ it, which feels like it should never happen"
- 진단: PR 단계 체크와 머지 그룹 단계 체크의 이중 실행(비용 2배), 워크플로 트리거 누락, 큐 내부 상태 불투명.

### 패턴 7: 공급망 불신 — 마켓플레이스 액션을 어디까지 믿나
- 위 장면 2(tj-actions) + HN 43419701의 cookiengineer: "the GitHub Actions CVE from August 2024 was the final nail in the coffin", 스크립트 인젝션 우려 "arbitrary data sources that are exposed as variables in the yaml files"
- 2025년 하반기에도 Shai Hulud v2, GhostAction 등 연쇄 사고가 언급됨(검증 필요 — web.md에서 1차 소스 확인).
- 2026-06: Claude Code GitHub Action 결함으로 악성 이슈 하나가 저장소를 탈취할 수 있었다는 보도(The Hacker News): https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html — AI 에이전트 액션의 프롬프트 인젝션이라는 새 표면. [공식 대조 필요]

---

## 실무 휴리스틱

### 휴리스틱 1: 서드파티 액션은 커밋 SHA로 고정하라
- 출처: HN 43367987 (2025-03-14)
- 원문:
  > "your build should always use hashes and not version tags" — mixologic
  > "Referencing a tag is not pinning a version, those can be updated" — remram
- 동조 반응: 사고 직후 여러 프로젝트가 즉시 SHA 고정 PR을 올림(예: sysdiglabs/charts #2741 https://github.com/sysdiglabs/charts/pull/2741 , rust-lang/crates.io #10835 https://github.com/rust-lang/crates.io/pull/10835). SHA 고정 사용자는 영향 없었다는 것이 보안 벤더 공통 결론. 단, SHA 고정은 업데이트 부담을 만들므로 Dependabot/Renovate로 SHA를 갱신하는 조합이 흔히 권장됨.

### 휴리스틱 2: 플래키 테스트는 즉시 격리·삭제, 재시도는 진통제
- 출처: HN 23493249, 47024638
- 원문:
  > "I have a zero tolerance policy for flaky tests." — mdoms
  > "Every retry rule in your CI pipeline is a painkiller." — 47024638 본문
- 반론: 대규모 조직에서는 재시도 + 자동 격리 + 소유 팀 통지가 현실적이라는 의견(HN "Suppressing flaky tests is a little terrifying. Google would just retry them…" https://news.ycombinator.com/item?id=36513060).

### 휴리스틱 3: CI YAML은 얇게, 빌드 로직은 로컬에서 도는 도구로
- 출처: Lobsters hkqnro, HN 46614558
- 원문:
  > "most CIs are fine if you just use them to bootstrap into your build system." — sebastien
  > "The less I rely on Github Actions environment the happier I am" — tracking1
- 동조: make·just·nix·mise·Dagger 등으로 로컬 재현성을 확보해 "push하고 기다리기" 루프를 끊는다는 경험담 다수.

### 휴리스틱 4: 모노레포에서는 워크플로 path 필터 대신 "변경 감지 잡 + 집계 필수 체크"
- 출처: Discussion #13690·#177835 https://github.com/orgs/community/discussions/177835 , 커뮤니티 블로그 https://www.codewithkarani.com/blog/monorepo-github-actions-path-filters-shared-code
- 요지: 워크플로 수준 path 필터는 공유 코드 의존 그래프를 모른다. 변경 감지를 한 번 하고 하위 잡이 `needs`/`if`로 스킵, 항상 실행되는 집계 잡만 필수 체크로. `actions/checkout`의 기본 `fetch-depth: 1`이면 비교할 이전 커밋이 없다는 함정도 반복 언급.

### 휴리스틱 5: 리뷰 SLA를 명시하라 — "업무일 1일 이내"
- 출처: 코멘토(2024-10-15), DEVOCEAN D-n 룰, 한국 블로그 다수
- 요지: 리뷰를 개인 선의가 아닌 팀 규칙으로. 리마인더 봇·우선순위 레이블·마감일 표시. 해외에서도 "피드백 지연은 하루가 상한, 이상적으로 1시간"이라는 글이 반복(https://steveberczuk.substack.com/p/timely-reviews).

### 휴리스틱 6: 머지 큐 도입 체크리스트 (커뮤니티 트러블슈팅에서 역산)
- 출처: Discussion #15254, #151100, #14801
- 요지: (1) 필수 체크를 최소 하나 지정, (2) 필수 체크를 만드는 워크플로에 `merge_group` 트리거 추가, (3) 빌드 시간 × 동시 빌드 한도 = 큐 처리량 계산, (4) 플래키 테스트를 먼저 정리, (5) 막히면 헤드 제거 → 큐 비우기 → 재활성화.
- 긍정 경험담: Lobsters elijahpotter "the switch to merge queues was an enormous improvement in quality of life for both reviewers and PR authors." (https://lobste.rs/s/drtmhv/replace_your_ci_with_merge_queue, 2026-07-27); HN zabil "We've been using this for a few months … for our mono repo. It's greatly improved the merge process." (https://news.ycombinator.com/item?id=36707239, 2023-07-13)

---

## 논쟁점

### 논쟁 A: Git Flow는 죽었나
- 배경: Vincent Driessen 원문(2010) 상단에 2020년 "Note of reflection" 추가 — 지속 배포되는 웹 앱은 자신이 염두에 둔 소프트웨어가 아니며, 그런 팀은 GitHub Flow 같은 더 단순한 흐름을 쓰라고 권함. https://nvie.com/posts/a-successful-git-branching-model/ [공식 대조 필요 — 원문 문구 확인]
- 관점 1: 죽었다 / 해롭다
  - Adam Ruka "GitFlow considered harmful"(2015) https://www.endoflineblog.com/gitflow-considered-harmful → OneFlow 제안. HN(2015-06-19): https://news.ycombinator.com/item?id=9744059 — sytse(GitLab CEO): "I agree that GitFlow is needlessly complex and that there should be one main branch."
  - HN "Please stop recommending Gitflow" (2020-03-04): https://news.ycombinator.com/item?id=22485489 — simonw: "Master should always be in a deployable state."
  - Lobsters 같은 글(2020-03-05): https://lobste.rs/s/o76cit/please_stop_recommending_git_flow — bkircher: "Every repo that is following gitflow comes with a mental overhead for me"; skade: "weakly defined enough to evolve into something I call 'X as practiced'"; roshan: "Your product almost certainly does not need this stuff"
- 관점 2: 맥락에 따라 여전히 유효
  - SAI_Peregrinus (HN 22485489): "Our tests include power analysis testing...total testing takes about two weeks. Git-flow is bad if you have CD. Git-flow is great if you can't do that."
  - utahshex (Lobsters): "particularly useful when you have a dedicated testing team, who need a stable base to test on"
  - belak (Lobsters): develop/master를 각각 다른 환경에 자동 배포하는 용도.
  - 한국 현장: 국내 블로그·velog에서는 여전히 Git Flow를 기본값으로 소개하는 글이 다수(예: https://velog.io/@gmlstjq123/Git-Flow-VS-Github-Flow), 반면 전환기도 존재 — 맘시터 "Git Flow에서 트렁크 기반 개발으로 나아가기"(2022-08-05) https://tech.mfort.co.kr/blog/2022-08-05-trunk-based-development/ , 화해 "Git 브랜치 전략 수립을 위한 전문가의 조언들" https://blog.hwahae.co.kr/all/tech/9507
- 관찰: 논쟁의 실제 분기점은 브랜치 모양이 아니라 "main의 임의 커밋을 안전하게 배포할 수 있는가"(CD 성숙도, 릴리스 승인 절차, 다중 버전 지원). 모바일·펌웨어·패키지 배포처럼 명시적 릴리스 버전이 있는 경우 Git Flow 옹호가 강하다.

### 논쟁 B: squash vs rebase vs merge commit
- HN "The merge vs. rebase debate" (2023-12-29~31): https://news.ycombinator.com/item?id=38800454
- 관점 1: rebase는 좋지만 squash는 싫다 (의미 있는 커밋 보존)
  - JoshTriplett: "I'm a big fan of the rebase workflow, but not of squashing. I wrote it as several separate commits for a _reason_: documenting each step, making each step revertible, separating refactors from semantic changes."
  - lolinder: "Why not take the chance to tell the story _now_, so that future you can skip all the false starts and failed experiments?"
  - HN 45371283 jonahx: "The atomic level of work should be a single, logically coherent change to the codebase"; fillmore: "I also read every commit message, and review PRs commit by commit"
- 관점 2: squash가 현실적 (PR = 단위)
  - herval (45371283): "nobody reads intermediate commit messages one by one on a PR, period" / "Just squash and merge, you have a single commit and it WORKS."
  - William_BB: "PR is the atomic level of work. I'd argue PR-level history (i.e. squash) is often enough and is way cleaner."
  - cj (38800454): "each single commit in master corresponds to a single PR. Makes it easy to revert PR but difficult to cherry pick."
  - bccdee: "Github isn't designed to review and merge individual commits...The 'atomic commits' crowd are working against the grain of the tools we actually use."
- 관점 3: merge commit / 이력 재작성 반대
  - wandernotlost: "It's like a huge portion of the industry is collectively engaging in a lie, so that our commit histories look prettier."
  - ponector: "You run tests against each commit in the history that you're rebasing? I doubt it"
  - TheCleric: 연쇄(serialized) PR에서 squash하면 "the changes done in 1 are now present TWICE." — 스택 PR과 squash의 충돌 지점.
- 절충: burntsushi: "Why not use squash & merge when appropriate and rebase & merge otherwise?"; kdmccormick: "The real answer to this whole debate is 'it depends' but for some reason that doesn't seem to satisfy people."
- 참고: Mitchell Hashimoto의 gist "Merge vs. Rebase vs. Squash" https://gist.github.com/mitchellh/319019b1b8aac9110fcfb1862e0c97fb (개인 선호 정리 — 인용 전 원문 확인)
- 책 연결점: 장면 1의 머지 큐 사고는 **squash 방식 머지 그룹에서만** 발생 — 머지 방식 선택이 도구 버그의 노출면까지 바꾼다는 구체 사례.

### 논쟁 C: 코드 리뷰는 품질 게이트인가, 연극인가
- 관점 1: 리뷰는 의식(theatre)이 되었다 — 러버스탬프, 의무적 nitpick, 설계 리뷰가 너무 늦게 일어남.
  - HN 45371283 (416 댓글), GeekNews "코드 리뷰는 더 나아질 수 있음"(TigerBeetle 글) https://news.hada.io/topic?id=22651 — 댓글: "설계 리뷰가 코드 리뷰 단계에서만 일어나 늦은 피드백 발생", RFC·사전 협의가 먼저라는 의견.
  - 대안: 페어 프로그래밍, 트렁크 기반 + 사후 리뷰, 리뷰어가 직접 고쳐 머지하는 비동기 페어링.
- 관점 2: 대규모·분산 협업에서는 리뷰와 깨끗한 이력이 필수.
  - jcalvinowels (45371283): "It's clear you've never worked on a large open source project...in big distributed projects this stuff really matters."
  - illuminator83: "Messiness is usually not tolerated by maintainers of important projects"
- 2026년 새 축: AI가 코드를 쓰는 속도 > 사람이 읽는 속도. "리뷰가 병목"이라는 인식이 확산, 리뷰 생략 머지 증가 보고(검증 필요).

### 논쟁 D: 머지 큐는 필요한가, 비용만 두 배인가
- 관점 1: 트래픽이 많은 main에서는 필수 — "not rocket science rule".
  - byroot (Lobsters 2026-07-27): "Merge Queues don't replace CI, they're mostly a solution to merge races on project with a high throughput."
  - carlana: "you need to follow the not-rocket-science rule with agents or they will break main." (AI 에이전트가 PR을 대량 생산하는 환경에서 재조명)
  - masklinn (HN 36707239): GitHub 머지 큐와 GitLab merge train 모두 bors의 계보.
- 관점 2: 비용과 복잡도, 신뢰 문제.
  - cprecioso (HN 36707239): "the merge group needs to pass the same checks as the branch itself, making it doubly expensive"
  - ploxiln: "it was pretty flaky early on, got stuck, double commits, not configurable merge-group size ... but it's pretty good now"
  - IshKebab: GitLab은 같은 기능을 "merge trains"라 부르고 Premium 전용.
  - 2026-04 사고 이후 "검증한 커밋과 실제 머지된 커밋이 같은가"라는 근본 질문(장면 1).
- 대체재 언급: Mergify, Graphite, bors, Trunk 등 서드파티 큐(벤더 글이 많아 중립성 주의).

### 논쟁 E: GitHub Actions에 머물 것인가
- 관점 1: 떠나고 싶다 — YAML, 로컬 재현 불가, 가격 정책 불신, 장애. Buildkite·Jenkins(Groovy)·GitLab CI·자체 러너 선호 발언 다수(HN 46909274, 43419701).
- 관점 2: 대안은 있어도 대체재는 없다 — 네트워크 효과, 무료 CI 인프라(GeekNews 32104 댓글: "Microsoft는 무료 CI 실행기에 연간 약 1억 달러를 지출" — 검증 필요), 마켓플레이스 생태계.
- 절충: Actions는 트리거·오케스트레이션으로만 쓰고 빌드 로직은 이식 가능하게(휴리스틱 3).

---

## 날짜·신선도 메타 (fact-checker 대조용)

| 사건·자료 | 날짜 | 비고 |
|---|---|---|
| Driessen Git Flow 원문 / Note of reflection | 2010-01 / 2020-03 | 원문 문구 확인 필요 |
| "GitFlow considered harmful" | 2015 | HN 2015-06-19 |
| "Please stop recommending Git Flow" | 2020-03-04~05 | HN·Lobsters |
| GitHub merge queue 베타 피드백 | 2022-04~ | Discussion #14801 |
| GitHub merge queue GA | 2023-07 (HN 2023-07-13, GeekNews 2023-07-15) | [공식 대조 필요] |
| tj-actions/changed-files 침해 | 2025-03-14~15 (악성 커밋 03-12설 있음) | CVE-2025-30066 |
| 셀프호스트 러너 과금 발표·연기 | 2025-12-16 / 12-17~18 | 2026-03-01 시행 예정이었음 |
| Ian Duncan "GitHub Actions Is Slowly Killing…" | 2026-02-05 | Lobsters |
| 머지 큐 squash 되돌림 사고 | 2026-04-23 | 영향 수치 출처별 상이 |
| Stacked PR 공개 프리뷰 | 2026-07-30 | Changelog |
| Lobsters "Replace Your CI With a Merge Queue" | 2026-07-27 | |

---

## 수집 한계
- 수집 건수: 토론·게시글 약 35건(HN 14, Lobsters 5, GitHub Community Discussions 7, GeekNews 4, 한국 기술블로그·velog 5 + 보도 보조).
- 미접근 플랫폼: **Reddit 전면 차단**(검색·페치 모두 불가) — r/git·r/devops·r/programming·r/ExperiencedDevs 목소리 부재. Lobsters와 HN으로 대체했으나 주니어~중간 연차의 "우리 팀은 이렇게 한다" 류 일상 경험담이 약하다. OKKY·커리어리는 검색 노출이 거의 없거나 페치 실패(커리어리 페이지 본문 미로드).
- 언어 편중: 영어권 HN/Lobsters가 과반. 한국 자료는 커뮤니티 토론보다 **회사 기술블로그·개인 블로그** 위주라 "날것의 댓글"이 부족. GeekNews는 댓글 원문을 거의 못 얻었고, 게시일이 상대 표기라 일부 추정.
- 인용 정확도: HN/Lobsters 댓글은 WebFetch 요약 모델을 거쳐 추출 — 일부 축약·부정어 누락 가능성(특히 rarkins 인용). 책에 쓰기 전 원문 링크 재확인 권장.
- 주제 공백: 한국 팀의 머지 큐 도입 경험담은 찾지 못함. 모노레포 CI는 GitHub Discussions 중심이고 Bazel/Nx/Turborepo 실사용 토론은 얕게만 확보.
