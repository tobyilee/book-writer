# 웹 리서치: GitHub·AWS·Cloudflare를 쓰는 개발자를 위한 CI/CD (+ AI 코딩 도구 시대의 팁)

- 장르: tech-book / 대상: 한국 실무 개발자
- 검색 시점: 2026-09-26 (모든 "기준" 표기는 이 날짜의 공개 문서·릴리스 기준)
- 인용 표기: 따옴표 안은 원문 발췌. 단, 수집 도구(WebFetch)가 본문을 추출·정리하는 과정을 거쳤으므로 **수치·버전·날짜는 fact-checker가 원 URL에서 한 번 더 대조**하길 권한다. 이하 "주의" 표시는 소스 간 충돌이나 2차 소스 의존 항목이다.

---

## 0. 빠른 참조: 주요 액션·도구 최신 버전 (GitHub Releases API, 2026-09-26 조회)

| 액션/도구 | 최신 태그 | 릴리스 일시(UTC) |
|---|---|---|
| aws-actions/configure-aws-credentials | v6.3.0 | 2026-09-15 |
| aws-actions/amazon-ecr-login | v2.1.7 | 2026-08-19 |
| aws-actions/amazon-ecs-deploy-task-definition | v2.6.3 | 2026-07-01 |
| cloudflare/wrangler-action | v4.1.3 | 2026-09-24 |
| wrangler (cloudflare/workers-sdk) | 4.141.0 | 2026-09-25 |
| anthropics/claude-code-action | v1.0.235 (floating `v1`) | 2026-09-25 |
| actions/checkout | v7.0.1 (v6.1.0도 병행 유지) | 2026-07-20 |
| actions/cache | v6.1.0 / v5.1.0 병행 | 2026-06-26 |
| actions/upload-artifact | v7.0.1 | 2026-04-10 |
| actions/attest | v4.2.2 | 2026-08-04 |
| hashicorp/setup-terraform | v4.0.1 | 2026-05-12 |
| step-security/harden-runner | v2.21.1 | 2026-08-30 |

- 조회 명령: `gh api "repos/{owner}/{repo}/releases?per_page=2"` — fact-checker가 재현 가능.
- 주의: 공식 문서 예제는 버전이 제각각이다 (Claude Code 문서·Cloudflare 문서 예제는 `actions/checkout@v6`, 최신은 v7). 본문 예제는 한 버전으로 통일하고 "2026년 9월 기준"을 명시할 것. wrangler는 거의 매일 마이너가 올라가므로 본문에선 "wrangler 4.x"로 적는 편이 안전하다.

---

## A. GitHub Actions 기초·고급 기능

### 자료 1: GitHub Actions: Early September 2026 updates (GitHub Changelog)
- 출처: https://github.blog/changelog/2026-09-03-github-actions-early-september-2026-updates/
- 저자·날짜: GitHub / 2026-09-03
- 신뢰성: 최상 (1차 공식 체인지로그)
- 기준: GitHub.com 2026-09 기준 (재사용 워크플로 job 컨텍스트는 GHES 미지원)
- 핵심 주장: 러너 버전 지원 종료일 조회 REST API, `GITHUB_TOKEN`의 `vulnerability-alerts` 권한(read/none) 신설, 재사용 워크플로가 자기 출처를 알 수 있는 `job.workflow_*` 컨텍스트 4종 추가.
- 인용 가능한 구절:
  > "`GET /actions/runners/deprecations/{version}` ... returning `runner_version`, `runtime_deprecates_at`, and `registration_deprecates_at`"
  > "Workflows now access read-only Dependabot alerts through a new `vulnerability-alerts` permission for `GITHUB_TOKEN`. This feature supports "read" and "none" values"
  > "`job.workflow_ref` ... `job.workflow_sha` ... `job.workflow_repository` ... `job.workflow_file_path`"
- 관련 섹션: 재사용 워크플로, 최소 권한(permissions), self-hosted 러너 운영

### 자료 2: New releases for GitHub Actions – November 2025 (재사용 워크플로 한도 상향)
- 출처: https://github.blog/changelog/2025-11-06-new-releases-for-github-actions-november-2025/
- 저자·날짜: GitHub / 2025-11-06
- 신뢰성: 최상
- 기준: GitHub.com 2025-11 기준
- 핵심 주장: 재사용 워크플로 중첩 한도 4→10단계, 한 실행에서 호출 가능한 워크플로 20→50개. M2 macOS 러너 GA. Copilot coding agent를 Actions 없이도 사용 가능.
- 인용 가능한 구절:
  > "You can now use up to 10 nested reusable workflows and call up to 50" (이전 한도 4, 20)
  > "You can now use GitHub Copilot coding agent without turning on GitHub Actions"
- 관련 섹션: reusable workflow vs composite action, 조직 단위 파이프라인 표준화

### 자료 3: GitHub Actions concurrency groups now allow larger queues
- 출처: https://github.blog/changelog/2026-05-07-github-actions-concurrency-groups-now-allow-larger-queues/
- 저자·날짜: GitHub / 2026-05-07
- 신뢰성: 최상
- 기준: GitHub.com 2026-05 기준
- 핵심 주장: 동시성 그룹이 대기 1개 제한에서 최대 100개 FIFO 대기로 확장. `queue: max`는 `cancel-in-progress: true`와 함께 쓸 수 없다.
- 인용 가능한 구절:
  > "a concurrency group could have one run in progress and one pending run. If another run entered the group, the pending run was canceled and replaced."
  > "you can configure concurrency groups to queue multiple pending runs and process them sequentially, with support for up to 100 queued jobs or workflow runs per concurrency group."
  ```yaml
  concurrency:
    group: my-group
    cancel-in-progress: false
    queue: max
  ```
- 관련 섹션: concurrency, 배포 직렬화(배포는 취소하지 말고 줄 세우기), PR 빌드는 cancel-in-progress

### 자료 4: GitHub Actions: Late March 2026 updates (환경의 deployment:false, 스케줄 타임존)
- 출처: https://github.blog/changelog/2026-03-19-github-actions-late-march-2026-updates/
- 저자·날짜: GitHub / 2026-03-19
- 신뢰성: 최상
- 핵심 주장: environment를 시크릿·변수 스코프 용도로만 쓰고 배포 레코드는 만들지 않는 `deployment: false` 옵션(커스텀 배포 보호 규칙과는 병용 불가). cron 스케줄에 IANA 타임존 지정 가능.
- 인용 가능한 구절:
  > "By setting `deployment: false` in your configuration, you can access environment features while avoiding unnecessary deployment records. However, this option is unavailable if you've implemented custom deployment protection rules."
  > "Users can specify a timezone field alongside cron expressions—for example, `timezone: "America/New_York"`"
- 관련 섹션: environments & protection rules, 스케줄 워크플로(한국 독자에겐 `Asia/Seoul` 예시)

### 자료 5: GitHub Actions: Early April / Early February 2026 updates
- 출처: https://github.blog/changelog/2026-04-02-github-actions-early-april-2026-updates/ , https://github.blog/changelog/2026-02-05-github-actions-early-february-2026-updates/
- 저자·날짜: GitHub / 2026-04-02, 2026-02-05
- 신뢰성: 최상
- 핵심 주장: (4월) OIDC 토큰에 저장소 custom properties를 클레임으로 넣는 기능 GA — 저장소별 신뢰 정책 대신 "환경 유형·팀·컴플라이언스 등급"으로 AWS 신뢰 정책을 묶을 수 있다. 서비스 컨테이너 entrypoint/command 오버라이드. (2월) allowed actions 설정을 Free·Team 포함 전 플랜으로 확대, Kubernetes 없이 쓰는 Go 기반 Runner Scale Set Client(퍼블릭 프리뷰), `windows-2025-vs2026` 이미지.
- 인용 가능한 구절:
  > "use repository custom properties as claims in your OIDC tokens to create more granular trust policies"
  > "define exactly which actions and reusable workflows run"
- 관련 섹션: OIDC 심화(조직 규모의 신뢰 정책), self-hosted 러너 오토스케일링

### 자료 6: Managing a merge queue (GitHub Docs)
- 출처: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue
- 저자·날짜: GitHub Docs / 상시 갱신 (2026-09 조회)
- 신뢰성: 최상
- 핵심 주장: 머지 큐를 쓰면 required check 워크플로에 `merge_group` 트리거를 반드시 추가해야 한다. 빌드 동시성·그룹 크기 1~100 설정 가능.
- 인용 가능한 구절:
  > "You **must** use the `merge_group` event to trigger your GitHub Actions workflow when a pull request is added to a merge queue."
  > "If your repository uses GitHub Actions to perform required checks on pull requests in your repository, you need to update the workflows to include the `merge_group` event as an additional trigger."
  > "Build concurrency: The maximum number of `merge_group` webhooks to dispatch (between `1` and `100`)"
  ```yaml
  on:
    pull_request:
    merge_group:
  ```
- 관련 섹션: required checks, merge queue, AI가 PR을 대량 생성할 때의 main 보호

### 자료 7: GitHub Actions cache size can now exceed 10 GB per repository
- 출처: https://github.blog/changelog/2025-11-20-github-actions-cache-size-can-now-exceed-10-gb-per-repository/
- 저자·날짜: GitHub / 2025-11-20
- 신뢰성: 최상
- 기준: 2025-11 기준
- 핵심 주장: 저장소당 10GB는 무료로 유지, 초과분은 종량 과금(Pro/Team/Enterprise). 캐시 크기 축출 한도와 보존 기간(일) 정책을 엔터프라이즈→조직→저장소로 캐스케이드 설정.
- 인용 가능한 구절:
  > "All repositories will continue to receive access to 10 GB, which is provided at no additional cost."
  > "cache size eviction limit (GB) and cache retention limit (days)"
- 관련 섹션: 캐싱 전략, 비용 최적화

---

## B. 러너·비용·속도

### 자료 8: GitHub Actions 2026 가격 변경 (GitHub Resources) + Actions runner pricing (Docs)
- 출처: https://github.com/resources/insights/2026-pricing-changes-for-github-actions (구 URL resources.github.com에서 308 리다이렉트), https://docs.github.com/en/billing/reference/actions-runner-pricing
- 저자·날짜: GitHub / 2025-12 발표, 2026-01-01 시행 (2026-09 조회)
- 신뢰성: 최상
- 기준: 2026-09 기준 가격
- 핵심 주장: 2026-01-01부터 GitHub-hosted 러너 가격 최대 39% 인하, 이 가격에 분당 $0.002 "Actions cloud platform charge"가 포함됨. self-hosted 러너에 같은 요금을 매기려던 계획(2026-03-01 시행 예정)은 **연기**. 현재 Linux 2-core x64 $0.006/분, arm64 2-core $0.005/분.
- 인용 가능한 구절:
  > "We're postponing the announced billing change for self-hosted GitHub Actions to take time to re-evaluate our approach."
  > "Linux 2-core (x64): $0.006 / Linux 2-core (arm64): $0.005 / Linux 4-core: $0.012 / Linux 8-core: $0.022 / Linux 16-core: $0.042 / Windows 2-core (x64): $0.010 / macOS 3-4 core: $0.062"
  > "Included minutes cannot be used for larger runners" / "The larger runners are not free for public repositories."
  > "96% of customers see no bill change"
- 주의: 2차 소스(samexpert.com 등)는 GitHub가 "missed the mark" 문구로 24~48시간 내 철회했다고 서술. 1차 페이지 문구는 "postponing". 본문엔 "연기"로 쓰고 재개 여부는 불확실로 둘 것.
- 관련 섹션: 러너 비용 최적화, self-hosted vs hosted 판단

### 자료 9: arm64 standard runners (public GA 2025-08, private 2026-01)
- 출처: https://github.blog/changelog/2025-08-07-arm64-hosted-runners-for-public-repositories-are-now-generally-available/ , https://github.blog/changelog/2026-01-29-arm64-standard-runners-are-now-available-in-private-repositories/
- 저자·날짜: GitHub / 2025-08-07, 2026-01-29
- 신뢰성: 최상
- 핵심 주장: Linux·Windows arm64 표준 러너가 퍼블릭(4 vCPU, 무료)에 이어 프라이빗(2 vCPU, 플랜 무료 분 차감)에서도 사용 가능. 라벨 `ubuntu-24.04-arm`, `ubuntu-22.04-arm`, `windows-11-arm`. Graviton(ECS/Lambda arm64)에 배포하는 팀은 에뮬레이션 없이 네이티브 빌드.
- 인용 가능한 구절:
  > "native multi-architecture builds without the overhead of virtualization or emulation."
  > "Private repositories: 2 vCPUs / Public repositories: 4 vCPUs"
- 관련 섹션: ARM 러너, 멀티아키텍처 이미지, 비용(arm64가 x64보다 분당 저렴)

### 자료 10: 쿠버네티스에게 Github Actions 설치에 대해 묻다 (버즈빌 기술블로그)
- 출처: https://tech.buzzvil.com/blog/쿠버네티스에게-github-actions-설치에-대해-묻다/
- 저자·날짜: Cade Seo (버즈빌 DevOps) / 2024-01-01
- 신뢰성: 최상 (회사 엔지니어링 블로그) — 단, 2024년 글이므로 ARC 버전은 구버전 정보일 수 있음
- 핵심 주장: 빌드 환경 통제와 워크플로별 리소스 최적화를 위해 ARC(Actions Runner Controller)로 self-hosted 러너를 운영. 커뮤니티 ARC 대신 GitHub 지원 ARC(Runner Scale Set)를 택한 이유.
- 인용 가능한 구절:
  > "빌드 환경에 대해 완전한 제어가 불가능합니다. 예를 들어 특정 운영체제 버전이나 도구를 사용하고 싶을 때가 있는데, 깃헙 호스팅을 선택하면 러너(Runner) 환경에서 제한된 행동밖에 하지 못합니다"
  > "각 러너 파드마다 워크플로 성격별로 최적화된 리소스를 할당해 비용 효율적으로 운영할 수 있습니다"
  > "커뮤니티 지원 ARC는 시간당 1,000개의 깃허브 API 개수 제한을 초과해 API 속도 제한 문제가 발생합니다"
  > "커뮤니티 지원 ARC가 레거시화 되었을 때의 마이그레이션 비용이 현재의 깃허브 지원 ARC의 부족한 기능으로 인한 운영 비용보다 더 크다고 생각했습니다"
- 관련 섹션: self-hosted 러너, 비용 최적화 (자료 8의 "self-hosted 과금 연기"와 함께 읽기)

### 자료 11: Github Actions 배포 시간 줄여볼까? (레몬베이스, GeekNews 소개)
- 출처: https://news.hada.io/topic?id=16313 (원문: https://blog.lemonbase.team/github-actions-배포-시간-줄여볼까-5725b92e36d9)
- 저자·날짜: 레몬베이스 팀 / GeekNews 게시 2024-08-14
- 신뢰성: 중 (GeekNews 요약 경유, 원문은 회사 블로그)
- 핵심 주장: 직렬 FE/BE 배포 병렬화, Docker 이미지 재사용으로 배포 시간 27분→12분(55% 감소). path-filter는 롤백 시 문제가 있어 워크플로 옵션으로 대체.
- 인용 가능한 구절:
  > "직렬로 배포되는 Frontend와 Backend 배포 작업을 병렬로 분리해 배포 시간을 27분에서 18분으로 단축"
  > "path-filter를 사용했으나, 롤백 시 문제되는 상황을 발견"
  > "Docker Image 재사용을 통해 배포 시간을 18분에서 15분으로 단축"
  > "배포 시간 55% 감소(27분 -> 12분)"
- 관련 섹션: 파이프라인 속도 최적화, 모노레포 path 필터의 함정(롤백)

### 자료 12: 모노레포에서 Github Actions 현명하게 사용하기 (F-Lab)
- 출처: https://f-lab.kr/blog/wise-use-of-github-actions-in-monorepo
- 저자·날짜: Tino (F-Lab 프론트엔드) / 2023-08-07
- 신뢰성: 중 (회사 블로그, 2023년 — 기법은 유효하나 액션 버전은 구버전일 수 있음)
- 핵심 주장: `dorny/paths-filter`로 변경된 프로젝트만 CI 실행, 프로젝트별 yml 분리로 실행 시간 절반.
- 인용 가능한 구절:
  > "CI 실행 시간과 시인성을 높이기 위해 각 프로젝트별로 yml 파일을 분리했습니다."
  > "이를 통해 기존 CI 실행 시간의 `절반` 수준으로 시간을 단축할 수 있었고"
  > "프로젝트별로 확인이 필요할 때만 CI가 실행되도록 구성하였고, 덕분에 개발자의 시간과 필요 없이 소모되는 금액을 줄일 수 있었습니다."
- 관련 섹션: 모노레포, required check와 path 필터 충돌(스킵된 체크가 required일 때) 설명의 도입 사례

---

## C. 보안: OIDC·최소 권한·공급망

### 자료 13: Configuring OpenID Connect in Amazon Web Services (GitHub Docs)
- 출처: https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
- 저자·날짜: GitHub Docs / 상시 갱신 (2026-09 조회)
- 신뢰성: 최상
- 핵심 주장: 공급자 URL `https://token.actions.githubusercontent.com`, audience `sts.amazonaws.com`. 신뢰 정책의 `sub` 조건으로 저장소·브랜치·환경을 제한. 워크플로는 `id-token: write` 필요.
- 인용 가능한 구절:
  ```json
  "Condition": {
    "StringLike": { "token.actions.githubusercontent.com:sub": "repo:octo-org/octo-repo:*" },
    "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" }
  }
  ```
  > (문서 예제 워크플로는 `permissions: id-token: write, contents: read`와 SHA 고정된 `aws-actions/configure-aws-credentials@e3dd6a42...` 사용)
- 주의: 문서 예제의 `repo:octo-org/octo-repo:*`는 모든 브랜치·PR을 허용한다. 본문에선 `repo:org/repo:environment:production` 또는 `ref:refs/heads/main`으로 좁히는 예를 권장(자료 5의 custom properties 클레임도 대안).
- 관련 섹션: OIDC to AWS, 최소 권한 IAM

### 자료 14: aws-actions/configure-aws-credentials (README, v6.3.0)
- 출처: https://github.com/aws-actions/configure-aws-credentials
- 저자·날짜: AWS / v6.3.0 릴리스 2026-09-15
- 신뢰성: 최상
- 기준: v6.3.0 / 2026 기준
- 핵심 주장: OIDC 권장. `role-session-name` 기본값 "GitHubActions", `role-duration-seconds` 기본 3600(900~43200).
- 인용 가능한 구절:
  ```yaml
  permissions:
    id-token: write
  jobs:
    run_job_with_aws:
      runs-on: ubuntu-latest
      steps:
        - name: Configure AWS Credentials
          uses: aws-actions/configure-aws-credentials@v6.3.0
          with:
            role-to-assume: <Role ARN you created in step 2>
            aws-region: <AWS Region you want to use>
  ```
- 관련 섹션: OIDC 실습

### 자료 15: Secure use reference (GitHub Docs — 보안 하드닝)
- 출처: https://docs.github.com/en/actions/reference/security/secure-use
- 저자·날짜: GitHub Docs / 상시 갱신 (2026-09 조회)
- 신뢰성: 최상
- 핵심 주장: 스크립트 인젝션은 중간 환경변수로 막고, 서드파티 액션은 전체 SHA로 고정하고, `GITHUB_TOKEN` 기본 권한은 읽기 전용, 클라우드 인증은 OIDC, 워크플로 파일은 CODEOWNERS로 보호, 퍼블릭 저장소엔 self-hosted 러너 금지.
- 인용 가능한 구절:
  > "set the value of the expression to an intermediate environment variable"
  > "Pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release."
  > "set the default permission for the `GITHUB_TOKEN` to read access only for repository contents"
  > self-hosted runners "should almost never be used for public repositories"
- 관련 섹션: 보안 기본기 체크리스트 (AI 섹션의 프롬프트 인젝션과 같은 뿌리: "신뢰할 수 없는 입력")

### 자료 16: tj-actions/changed-files 침해 (CVE-2025-30066) — GitHub Advisory + CISA
- 출처: https://github.com/advisories/ghsa-mrrh-fwg8-r2c3 , https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction
- 저자·날짜: GitHub Advisory DB (게시 2025-03-15, 최종 갱신 2025-10-22), CISA (2025-03-18)
- 신뢰성: 최상
- 핵심 주장: 공격자가 v1~v45.0.7 태그를 악성 커밋으로 소급 변경. 러너 워커 프로세스 메모리에서 시크릿을 긁어 로그에 출력. 23,000개 이상 저장소 영향, v46.0.1에서 수정. 연쇄로 reviewdog/action-setup@v1(CVE-2025-30154)도 침해.
- 인용 가능한 구절:
  > "Attackers retroactively modified multiple version tags to reference a malicious commit, exposing CI/CD secrets in workflow logs."
  > "extracted secrets from the Runner Worker process memory and printed them in GitHub Actions logs, making them publicly accessible."
  > CVSS 3.1: 8.6 (High), 영향 기간 2025-03-14~15, 패치 v46.0.1
- 관련 섹션: SHA 고정의 이유(태그는 움직인다), 공급망 사고 사례

### 자료 17: [긴급] 깃허브 액션스 공급망 공격 발생…218개 저장소 비밀정보 유출돼 (데일리시큐)
- 출처: https://www.dailysecu.com/news/articleView.html?idxno=164700
- 저자·날짜: 길민권 기자 / 2025-03-23
- 신뢰성: 중 (국내 보안 전문 매체)
- 핵심 주장: 23,000개 저장소가 사용했으나 실제 비밀정보가 유출된 오픈소스 저장소는 최소 218개. 봇 PAT 유출이 시작점.
- 인용 가능한 구절:
  > "CI/CD 파이프라인의 러너에서 동작하는 워크플로우를 악용해 민감한 비밀정보(Secrets)를 레포지토리 콘솔 로그에 출력"
  > 권고: "Action 버전을 커밋 SHA로 고정 지정", "CI/CD 봇의 권한을 최소화하고 주기적으로 교체"
- 주의: "23,000개 영향"(사용 저장소 수)과 "218개 유출"(실제 유출 확인)은 다른 수치다. 본문에서 구분해 쓸 것.
- 관련 섹션: 공급망 사고 한국어 도입부

### 자료 18: GitHub Actions policy now supports blocking and SHA pinning actions
- 출처: https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/
- 저자·날짜: GitHub / 2025-08-15
- 신뢰성: 최상
- 핵심 주장: 조직/저장소 정책으로 SHA 미고정 액션 실행 거부, `!` 접두어로 특정 액션·버전 차단(차단 목록이 마지막에 평가되어 허용을 덮음).
- 인용 가능한 구절:
  > "The blocklist is evaluated last, overriding any other policy that would otherwise allow the action."
  > (SHA 고정 강제 시) 전체 커밋 SHA로 고정하지 않은 액션을 쓰는 워크플로는 실행이 거부된다.
- 관련 섹션: SHA 고정을 사람의 규율이 아니라 정책으로

### 자료 19: Immutable releases are now generally available
- 출처: https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/
- 저자·날짜: GitHub / 2025-10-28
- 신뢰성: 최상
- 핵심 주장: 불변 릴리스로 게시 후 에셋 추가·수정·삭제 불가, 태그 이동·삭제 불가, 에셋별 서명된 릴리스 attestation 자동 생성.
- 인용 가능한 구절:
  > "Once you publish a release as immutable, its assets can't be added, modified, or deleted." / "Tags for new immutable releases are protected and can't be deleted or moved."
- 관련 섹션: 자체 액션·라이브러리를 배포하는 쪽의 책임

### 자료 20: What's coming to our GitHub Actions 2026 security roadmap (GitHub Blog)
- 출처: https://github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/
- 저자·날짜: Greg Ose, Stephen Glass / 2026-03-26 (2026-03-30 갱신)
- 신뢰성: 최상 (단, **로드맵**이므로 출시 여부·시점은 미확정)
- 기준: 2026-03 발표 기준. 2026-09 현재 프리뷰 출시 여부는 이번 조사에서 확인하지 못함.
- 핵심 주장: 워크플로 `dependencies:` 잠금(직·간접 액션을 SHA+해시로 고정, go.sum 유사), ruleset 기반 실행 정책(누가·어떤 이벤트로 트리거 가능한지), scoped secrets(브랜치·환경·워크플로 경로에 바인딩, 쓰기 권한과 시크릿 관리 권한 분리), 러너 VM 밖에서 동작하는 L7 egress 방화벽, Actions Data Stream(S3/Azure로 실행 텔레메트리).
- 인용 가능한 구절:
  > "locks all direct and transitive dependencies with the commits SHA"
  > (egress 방화벽은) "outside the runner VM" ... "immutable even if an attacker gains root access"
  > "prohibit pull_request_target events entirely and only allow pull_request, ensuring workflows triggered by external contributions run without access to repository secrets or write permissions."
  > 일정: 잠금·정책·scoped secrets 퍼블릭 프리뷰 3~6개월, GA 6개월 / egress 방화벽 프리뷰 6~9개월
- 관련 섹션: "앞으로 바뀔 것" 박스, 신선도 경고 필요

### 자료 21: Securely using pull_request_target (GitHub Docs) + actions/checkout v7 변경 (The Hacker News)
- 출처: https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target , https://thehackernews.com/2026/06/github-updates-actionscheckout-to-block.html
- 저자·날짜: GitHub Docs (2026-09 조회) / Ravie Lakshmanan, 2026-06-23
- 신뢰성: 최상 (Docs) / 중 (보안 뉴스)
- 기준: 2026-09 기준, 정책 강제일 2026-11-02
- 핵심 주장: 퍼블릭 저장소에서 `pull_request_target`을 막는 GitHub 기본 이벤트 정책이 현재 evaluate 모드, **2026-11-02 강제 예정**(프라이빗·내부 저장소 미적용). actions/checkout v7(2026-06-18, 지원 버전에 2026-07-16까지 백포트)은 `pull_request_target`·`workflow_run`에서 포크 PR 코드를 가져오기를 거부하며, `allow-unsafe-pr-checkout: true`로만 우회.
- 인용 가능한 구절:
  > "GitHub provides a default policy that blocks the `pull_request_target` event in public repositories."
  > "the checked-out code is only ever inspected as data and never executed." (`allow-unsafe-pr-checkout` 사용 조건)
  > (THN) "refuses to fetch fork pull request code in pull_request_target and workflow_run workflows"
- 주의: THN 기사는 Nx s1ngularity를 "March 2026"으로 적었으나 1차·다수 소스(자료 22)는 2025년 8월. 기사 오기이거나 Nx의 별도 사건일 수 있으므로 **본문에 THN 날짜를 쓰지 말 것**. PostHog(2025-11)·TanStack(2026-05) 사례도 THN 단독 출처라 교차 확인 필요.
- 관련 섹션: pwn request, 포크 PR 처리, 책 출간 직후 바뀌는 날짜(2026-11-02) 신선도 경고

### 자료 22: s1ngularity: Nx 공급망 공격 (Wiz Blog)
- 출처: https://www.wiz.io/blog/s1ngularity-supply-chain-attack
- 저자·날짜: Wiz Research / 2025-08-27 최초 게시, 2025-08-29 갱신
- 신뢰성: 최상 (보안 기업 리서치 블로그)
- 핵심 주장: 2025-08-21 추가된 워크플로의 PR 제목 미검증 + `pull_request_target` 권한으로 명령 인젝션 → npm 토큰 탈취 → 악성 Nx 패키지 게시. 페이로드는 설치된 AI CLI(Claude·Gemini·Q)를 동원해 시크릿을 수색 — "AI 도구를 무기화한 첫 공급망 공격"으로 보도됨.
- 인용 가능한 구절:
  > "An unsanitized pull-request title combined with pull_request_target permissions enabled command injection"
  > "over a thousand valid Github tokens, dozens of valid cloud credentials and NPM tokens, and roughly twenty thousand additional files were leaked."
  > "over 400 users/organizations impacted, and over 5500 repositories"
- 관련 섹션: 스크립트 인젝션 사례, AI 섹션 도입부(개발자 머신의 AI 에이전트도 공격 표면)

### 자료 23: GitHub Actions workflow security analysis with CodeQL is now generally available
- 출처: https://github.blog/changelog/2025-04-22-github-actions-workflow-security-analysis-with-codeql-is-now-generally-available/
- 저자·날짜: GitHub / 2025-04-22
- 신뢰성: 최상
- 핵심 주장: CodeQL이 워크플로 YAML 자체를 분석(권한 누락, 스크립트 인젝션 등). 기본 설정 저장소는 자동 활성화. 프리뷰 기간 158,000개 저장소에서 80만 건 이상 탐지, 약 15% 수정.
- 인용 가능한 구절:
  > "over 158,000 repositories" / "more than 800,000 potential vulnerabilities in Actions workflows" / "approximately 15% of these issues"
  > `actions/missing-workflow-permissions` — "one of the most frequent findings in Actions workflows"
- 관련 섹션: CodeQL, 워크플로 자체를 코드로 검사하기

### 자료 24: Dependabot 기본 쿨다운 (3일) 도입
- 출처: https://github.blog/changelog/2026-07-14-dependabot-version-updates-introduce-default-package-cooldown/ (배경: https://github.blog/changelog/2025-07-01-dependabot-supports-configuration-of-a-minimum-package-age/)
- 저자·날짜: GitHub / 2026-07-14 (쿨다운 옵션 자체는 2025-07-01 GA)
- 신뢰성: 최상
- 기준: 2026-07 기준 github.com
- 핵심 주장: 버전 업데이트 PR은 새 릴리스가 레지스트리에 3일 이상 머문 뒤에야 열린다. 보안 업데이트는 쿨다운 무시.
- 인용 가능한 구절:
  > "Dependabot now waits until a new release has been available on its registry for at least three days before opening a version update pull request."
- 주의: dependabot-core 이슈 #13078·#13691에 따르면 github-actions 생태계의 쿨다운은 태그 커밋 날짜 기준으로 계산되고, 릴리스가 잦은 액션은 업데이트가 영영 안 뜨는 문제가 보고됨(커뮤니티 리서처 영역과 겹침).
- 관련 섹션: Dependabot/Renovate로 SHA 고정 액션 갱신하기, 공급망 방어로서의 "기다리기"

### 자료 25: Artifact attestations와 SLSA Build Level 3 (GitHub Docs)
- 출처: https://docs.github.com/en/actions/concepts/security/artifact-attestations , https://docs.github.com/actions/security-guides/using-artifact-attestations-and-reusable-workflows-to-achieve-slsa-v1-build-level-3 , https://github.com/actions/attest-build-provenance
- 저자·날짜: GitHub Docs / 상시 갱신 (2026-09 조회), actions/attest v4.2.2 (2026-08-04)
- 신뢰성: 최상
- 핵심 주장: attestation은 아티팩트 다이제스트를 in-toto 형식 SLSA provenance에 묶고 Sigstore 단기 인증서로 서명. 단독으로 SLSA v1.0 Build L2, 재사용 워크플로로 빌드 지침을 저장소 밖에 두면 L3. v4부터 `attest-build-provenance`는 `actions/attest`의 래퍼 — 신규는 `actions/attest` 권장.
- 인용 가능한 구절:
  > "Artifact attestations by itself provides SLSA v1.0 Build Level 2."
  > "new implementations should use actions/attest instead."
- 관련 섹션: SLSA/provenance, ECR 이미지 서명·검증(`gh attestation verify`)

---

## D. AWS 배포 대상

### 자료 26: Amazon ECS built-in blue/green (2025-07) → linear/canary (2025-10) → NLB 지원 (2026-02)
- 출처: https://aws.amazon.com/about-aws/whats-new/2025/07/amazon-ecs-built-in-blue-green-deployments/ , https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-ecs-built-in-linear-canary-deployments , https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-ecs-nlb-linear-canary-deployments/
- 저자·날짜: AWS What's New / 2025-07-17, 2025-10-30, 2026-02
- 신뢰성: 최상
- 기준: 2026-09 기준
- 핵심 주장: ECS가 CodeDeploy 없이 자체 blue/green(ALB·NLB·Service Connect), Lambda 라이프사이클 훅, 베이크 기간 중 자동 롤백, CloudWatch 알람·circuit breaker 연동을 제공. 2025-10에 linear·canary 추가, 2026-02 NLB에도 확장.
- 인용 가능한 구절:
  > "these capabilities help make your software updates safer, allowing you to ship new capabilities faster."
  > (linear) 동일 비율 단계로 트래픽을 옮기며 단계별 bake time 설정 / (canary) 소량 트래픽 후 canary bake time 경과 시 나머지 전환
- 관련 섹션: ECS/Fargate 점진 배포, "CodeDeploy는 이제 필수가 아니다"

### 자료 27: Migrating from AWS CodeDeploy to Amazon ECS for blue/green deployments (AWS Containers Blog)
- 출처: https://aws.amazon.com/blogs/containers/migrating-from-aws-codedeploy-to-amazon-ecs-for-blue-green-deployments
- 저자·날짜: Mike Rizzo, Islam Mahgoub, Olly Pomeroy / 2025-09-16
- 신뢰성: 최상
- 기준: 2025-09 시점 — **이후 linear/canary가 추가되었으므로 일부 서술은 구버전 정보**
- 핵심 주장: CodeDeploy는 TaskSet, ECS는 ServiceRevision 모델. 대기 시간(wait time)은 ECS에선 훅으로 구현.
- 인용 가능한 구절:
  > "CodeDeploy uses a TaskSet, whereas Amazon ECS uses a ServiceRevision."
  > "As of this writing, ECS blue/green only supports all-at-once." ← 2025-10 이후 사실과 다름(자료 26)
  > "Where CodeDeploy supports a wait time option for testing a new deployment ... you need to use a hook to achieve this with ECS blue/green deployments."
- 관련 섹션: CodeDeploy → ECS 네이티브 이관, 충돌 기록

### 자료 28: AWS App Runner 신규 고객 종료 + ECS Express Mode
- 출처: https://docs.aws.amazon.com/apprunner/latest/relnotes/relnotes.html , https://aws.amazon.com/about-aws/whats-new/2025/11/announcing-amazon-ecs-express-mode/ , https://aws.amazon.com/about-aws/whats-new/2026/09/amazon-ecs-express-mode-arm-architecture/
- 저자·날짜: AWS / App Runner 공지(2026-03-31 게시 추정, 2026-04-30 시행), ECS Express Mode 2025-11 발표, Graviton 지원 2026-09
- 신뢰성: 최상
- 기준: 2026-09 기준
- 핵심 주장: App Runner는 2026-04-30부터 신규 고객을 받지 않음(기존 고객 계속 사용, 신규 기능 없음). AWS는 대안으로 ECS Express Mode 권장 — 이미지 하나로 ECS 서비스·HTTPS 엔드포인트·오토스케일링을 만들고, 만든 리소스는 계정에 그대로 노출. 추가 요금 없음.
- 인용 가능한 구절:
  > "AWS App Runner will no longer be open to new customers starting April 30, 2026. If you would like to use App Runner, sign up prior to that date. Existing customers can continue to use the service as normal."
  > (Express Mode) "available now in all AWS Regions at no additional charge"
- 주의: 브리프가 App Runner를 배포 대상으로 나열했으나, 신규 독자에게는 사용 불가. 본문은 "App Runner → ECS Express Mode"로 대체 권장.
- 관련 섹션: AWS 배포 대상 선택표

### 자료 29: AWS Lambda now supports GitHub Actions (aws-actions/aws-lambda-deploy)
- 출처: https://aws.amazon.com/about-aws/whats-new/2025/08/aws-lambda-github-actions-function-deployment , https://github.com/aws-actions/aws-lambda-deploy , https://docs.aws.amazon.com/lambda/latest/dg/deploying-github-actions.html
- 저자·날짜: AWS / 2025-08-07
- 신뢰성: 최상
- 핵심 주장: 공식 Lambda 배포 액션 — zip·컨테이너 이미지 지원, 패키징 자동, OIDC 인증, 런타임·메모리·타임아웃·환경변수 선언적 설정, dry-run, 대용량은 S3 경유.
- 인용 가능한 구절:
  > "Starting today, the new GitHub action provides a simplified way to deploy changes to Lambda functions using declarative configuration."
- 관련 섹션: Lambda 배포 (SAM/CDK와의 역할 구분: 함수 코드만 vs 인프라 전체)

### 자료 30: Automate Terraform with GitHub Actions (HashiCorp Developer)
- 출처: https://developer.hashicorp.com/terraform/tutorials/automation/github-actions , https://github.com/hashicorp/setup-terraform
- 저자·날짜: HashiCorp / 튜토리얼 상시 갱신, setup-terraform v4.0.1 (2026-05-12)
- 신뢰성: 최상
- 핵심 주장: PR 커밋마다 speculative plan을 만들어 PR에 링크/코멘트, main 머지 시 apply. setup-terraform은 CLI 설치와 래퍼 출력 제공.
- 주의: PR 코멘트 65,535자 제한으로 큰 plan은 코멘트 실패 가능(2차 소스). plan 전문은 아티팩트/Step Summary로.
- 관련 섹션: IaC 파이프라인(plan-on-PR, apply-on-merge), CDK diff와 대조. CDK diff 전용 공식 AWS 가이드는 이번 조사에서 찾지 못함(서드파티 `cdk-diff-action` 다수).

---

## E. Cloudflare

### 자료 31: Migrate from Pages to Workers (Cloudflare Docs)
- 출처: https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/
- 저자·날짜: Cloudflare Docs / 2026-09 조회 (예제 `compatibility_date: "2026-09-25"`)
- 신뢰성: 최상
- 핵심 주장: 정적 사이트는 `pages_build_output_dir` → `assets.directory` 한 줄 변경. Workers는 SPA/404 처리를 명시(`not_found_handling`), 기본은 정적 에셋 우선(`run_worker_first`로 변경). Workers 쪽이 기능 폭이 넓다. 정적 에셋 요청은 무료.
- 인용 가능한 구절:
  > "Workers has a distinctly broader set of features available to it, (including Durable Objects, Cron Triggers, and more comprehensive Observability)."
  ```jsonc
  { "name": "my-worker", "compatibility_date": "2026-09-25", "assets": { "directory": "./dist/client/" } }
  ```
- 주의: "Pages가 deprecated되었다"는 2차 블로그 표현(vibecodingwithfred 등)은 공식 문구가 아니다. 공식 문서는 "merging"/마이그레이션 권장 수준으로 기술 — 본문에서 "폐지"라고 단정하지 말 것.
- 관련 섹션: Pages vs Workers static assets 수렴

### 자료 32: Worker Previews / Compare workflows (Cloudflare Docs)
- 출처: https://developers.cloudflare.com/workers/previews/ , https://developers.cloudflare.com/workers/previews/compare-workflows/ , https://developers.cloudflare.com/workers/configuration/previews/
- 저자·날짜: Cloudflare Docs / 2026-09 조회
- 신뢰성: 최상
- 기준: Wrangler 4.135.0+ (Worker Previews), wrangler-action의 `preview` 명령 예제는 4.136.3+
- 핵심 주장: `wrangler preview`가 브랜치별로 격리된 프로덕션 유사 환경을 같은 Worker 아래 만든다. Version URL(`wrangler versions upload`)은 **프로덕션 리소스를 쓰므로** 브랜치/PR 테스트에 쓰지 말라고 공식 문서가 명시. 대부분 바인딩은 Preview별 격리 사본이지만 Workflow 바인딩과 서비스 바인딩은 예외.
- 인용 가능한 구절:
  > "Previews give each branch an isolated, production-like environment under the same Worker"
  > "Do not use Version URLs for branch or pull request testing. Use Previews instead."
  > "Previews are the recommended way to test changes before production."
  > "Service bindings from a Preview call the bound Worker's production deployment."
  > "Worker Previews requires Wrangler 4.135.0 or later."
- 주의: 이 기능은 매우 최근(2026년 하반기)이고 2025-07의 "preview URLs"(`--preview-alias`, Wrangler 4.21.0+)와 이름이 겹친다. 신선도 경고 필수, 용어 표기 통일 필요(Preview URL vs Worker Previews vs Version URL).
- 관련 섹션: PR별 프리뷰 환경

### 자료 33: cloudflare/wrangler-action (README) + GitHub Actions 가이드 (Cloudflare Docs)
- 출처: https://github.com/cloudflare/wrangler-action , https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/
- 저자·날짜: Cloudflare / v4.1.3 (2026-09-24)
- 신뢰성: 최상
- 핵심 주장: `apiToken`·`accountId`만으로 배포. `wranglerVersion`으로 버전 고정. 출력 `deployment-url`, `gitHubToken` 전달 시 GitHub Deployments 생성(`deployments: write`). API 토큰은 "Edit Cloudflare Workers" 템플릿에서 시작.
- 인용 가능한 구절:
  ```yaml
  - uses: cloudflare/wrangler-action@v4
    with:
      apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
      accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
  ```
  > "command: preview --name pr-${{ github.event.pull_request.number }}" (Wrangler 4.136.3+)
  > "Never commit `CLOUDFLARE_API_TOKEN` to your repository."
- 주의: Cloudflare는 GitHub OIDC 페더레이션을 지원하지 않는 것으로 보임(이번 조사에서 공식 문서 발견 못 함) → AWS와 달리 장기 API 토큰을 시크릿으로 둘 수밖에 없다는 비대칭을 본문에서 다룰 가치가 있음. 확인 필요.
- 관련 섹션: Workers 배포 파이프라인

### 자료 34: Grant teammates and agents access to specific Workers (Cloudflare Changelog)
- 출처: https://developers.cloudflare.com/changelog/post/2026-09-15-granular-worker-permissions/ , https://developers.cloudflare.com/fundamentals/api/get-started/create-token/
- 저자·날짜: Cloudflare / 2026-09-15
- 신뢰성: 최상
- 핵심 주장: Worker 단위 역할 4종(Metadata Read-Only, Content Read-Only, Editor, Admin). 계정 소유 API 토큰을 "Specified Workers"로 스코프 가능 — CI와 AI 에이전트에 특정 Worker만 배포 권한 부여.
- 인용 가능한 구절:
  > "View settings, metrics, logs, and traces without access to Worker code" (Metadata Read-Only)
  > Editor: "Deploy and update capabilities without deletion permissions"
  > (토큰) "For an agent or CI/CD workflow, go to Manage Account > Account API Tokens and create an account-owned API token. Set the scope to Specified Workers"
- 관련 섹션: Cloudflare API 토큰 최소 권한, AI 에이전트에 줄 권한

### 자료 35: Gradual deployments / Rollbacks (Cloudflare Workers Docs) + Workers Metrics 릴리스 주석
- 출처: https://developers.cloudflare.com/workers/versions-and-deployments/gradual-deployments/ , https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/ , https://developers.cloudflare.com/changelog/post/2026-09-25-release-flows-workers-metrics/
- 저자·날짜: Cloudflare Docs (2026-09 조회), Changelog 2026-09-25
- 신뢰성: 최상
- 핵심 주장: `wrangler versions upload` → `wrangler versions deploy`로 두 버전 간 트래픽 분할. 최근 100개 버전 내에서만 가능, 한 배포에 최대 2개 버전. `Cloudflare-Workers-Version-Key` 헤더로 버전 어피니티. 롤백은 코드만 되돌리고 바인딩·D1 데이터·시크릿은 되돌리지 않는다. 2026-09-25부터 Metrics 차트에 점진 배포 단계가 음영으로 표시.
- 인용 가능한 구절:
  > "You can only create a gradual deployment with the last 100 uploaded versions of your Worker."
  > "pin a user to a consistent version for the duration of the gradual deployment."
  > "Resources connected to your Worker will not be changed during a rollback."
  > "You can only roll back to the 100 most recently published versions."
  > "Gradual deployments appear as a single rollout with shading that intensifies as traffic shifts to the new version."
- 관련 섹션: progressive delivery/rollback (ECS canary와 나란히 비교), "롤백이 데이터를 되돌리지 않는다"

### 자료 36: D1 migrations apply (Cloudflare Docs)
- 출처: https://developers.cloudflare.com/workers/wrangler/commands/d1/ , https://developers.cloudflare.com/d1/reference/migrations/
- 저자·날짜: Cloudflare Docs / 2026-09 조회
- 신뢰성: 최상
- 핵심 주장: 비대화형(CI)에선 확인 단계 생략하되 백업은 남김. 실패한 마이그레이션은 롤백되고 이전 성공분은 유지. 적용 기록은 `d1_migrations` 테이블.
- 인용 가능한 구절:
  > "When running the apply command in a CI/CD environment or another non-interactive command line, the confirmation step will be skipped, but the backup will still be captured."
  > "If applying a migration results in an error, this migration will be rolled back, and the previous successful migration will remain applied."
- 주의: wrangler-action 이슈 #221("D1 migrations in CI fail silently") — CI에서 `--remote` 누락 시 로컬 DB에 적용되는 함정. 커뮤니티 리서처 쪽 교차 확인.
- 관련 섹션: D1/R2 마이그레이션, 스키마 변경은 확장-축소(expand/contract)로 (자료 35 롤백 한계와 연결)

### 자료 37: Protect your origin server (Cloudflare Docs)
- 출처: https://developers.cloudflare.com/fundamentals/security/protect-your-origin-server/
- 저자·날짜: Cloudflare Docs / 2026-09 조회
- 신뢰성: 최상
- 핵심 주장: AWS 오리진(ALB 등)을 Cloudflare 뒤에 둘 때의 보호 수단 계층 — Cloudflare Tunnel(공인 IP 불필요), 비밀 헤더/JWT 검증, Authenticated Origin Pulls(mTLS), Cloudflare IP 허용 목록.
- 인용 가능한 구절:
  > (Tunnel) "connects your resources to Cloudflare without a publicly routable IP address"
  > (AOP) "Requires Full or Full (strict) encryption modes"
  > (IP allowlist) "Vulnerable to IP spoofing"
- 주의: IP 허용 목록만으로는 "다른 Cloudflare 고객의 트래픽"도 통과한다는 지적(2차: javan.de). AWS 쪽은 Cloudflare CIDR을 customer-managed prefix list로 보안 그룹에 연결하는 방식이 일반적(2차 소스).
- 관련 섹션: 하이브리드 아키텍처(Cloudflare 앞단 + AWS 오리진)

---

## F. AI 코딩 도구와 CI/CD

### 자료 38: Claude Code GitHub Actions (Claude Code Docs)
- 출처: https://code.claude.com/docs/en/github-actions
- 저자·날짜: Anthropic / 2026-09 조회 (문서 내 버전 표기: Claude Code v2.1.229 이후 리뷰가 PR에 게시)
- 신뢰성: 최상
- 기준: claude-code-action v1 (최신 v1.0.235, 2026-09-25)
- 핵심 주장: `/install-github-app`으로 빠른 설정. `prompt` 없으면 `@claude` 멘션에 반응(interactive), 있으면 automation. 이슈/PR 이벤트는 트리거 사용자가 쓰기 권한 필요, 봇은 기본 거부. 장기 키 대신 워크로드 아이덴티티 페더레이션(GitHub OIDC ↔ Claude Console 서비스 계정) 가능, Bedrock/Vertex/Foundry도 OIDC. 기본 `GITHUB_TOKEN`으로 만든 커밋은 CI를 트리거하지 않는다.
- 인용 가능한 구절:
  > "on issue and pull request events, the triggering user must have write access to the repository."
  > "the Claude Code GitHub Action rejects a bot actor unless you list it in `allowed_bots`, which keeps bots from triggering Claude in a loop."
  > "To avoid storing a long-lived secret entirely, authenticate through workload identity federation, where the Claude Code GitHub Action exchanges the workflow's GitHub OpenID Connect (OIDC) token for Claude API access through a Claude Console service account."
  > "Create a `CLAUDE.md` file in your repository root to define code style guidelines, review criteria, project-specific rules, and preferred patterns."
  > "GitHub doesn't trigger workflows on commits made with the default `GITHUB_TOKEN`."
  > 비용 절감: "Set `--max-turns` in `claude_args` to limit iterations" / "Use GitHub's concurrency controls to limit parallel runs"
  > "On public repositories, GitHub withholds secrets from runs triggered by fork pull requests, so the review runs only on pull requests from branches in the same repository."
- 관련 섹션: 에이전트를 Actions에서 돌리기, AI 리뷰 봇, 비용 통제

### 자료 39: claude-code-action Security (docs/security.md)
- 출처: https://github.com/anthropics/claude-code-action/blob/main/docs/security.md
- 저자·날짜: Anthropic / 2026-09 조회
- 신뢰성: 최상
- 핵심 주장: 숨은 마크다운(HTML 주석·보이지 않는 문자 등) 프롬프트 인젝션 경고와 자동 정제 목록, `allowed_non_write_users`는 "RISKY", PAT 금지, `show_full_output` 기본 비활성(디버그 모드에선 자동 활성), 기본 설정에서 Claude는 PR을 스스로 만들지 않고 생성 링크만 제공.
- 인용 가능한 구절:
  > "**Beware of potential hidden markdown when tagging Claude on untrusted content.** ... The action sanitizes content by stripping HTML comments, invisible characters, markdown image alt text, hidden HTML attributes, and HTML entities, but new bypass techniques may emerge."
  > "**Do not use a personal access token** — a static token does not rotate between runs and could be partially or fully recovered over time via prompt injection."
  > "Full output is **automatically enabled** when GitHub Actions debug mode is active (when `ACTIONS_STEP_DEBUG` secret is set to `true`)."
  > "In its default configuration, **Claude does not create pull requests automatically** ... ensuring human oversight before any code is proposed for merging"
- 관련 섹션: 프롬프트 인젝션, 에이전트의 시크릿 노출, 사람 승인 지점

### 자료 40: openai/codex-action Security (docs/security.md)
- 출처: https://github.com/openai/codex-action/blob/main/docs/security.md
- 저자·날짜: OpenAI / 2026-09 조회
- 신뢰성: 최상
- 핵심 주장: 기본은 쓰기 권한 사용자만 실행. 인젝션 벡터로 PR 제목·본문(숨은 HTML 주석), 커밋 메시지, **AGENTS.md 같은 저장소 지시 파일**, 스크린샷을 명시. GitHub-hosted 러너의 비밀번호 없는 sudo 때문에 읽기 전용 샌드박스만으론 API 키가 procfs로 노출될 수 있어 `drop-sudo`(기본) 또는 `unprivileged-user` 필수. 액션은 마지막 단계로 두고 결과는 별도 job으로 넘겨라.
- 인용 가능한 구절:
  > "Be sure to use either `drop-sudo` or `unprivileged-user` to ensure it stays secret!"
  > "Particularly if you run Codex with loose permissions, there are no guarantees what the state of the host is when the `openai/codex-action` completes."
  > "Permission profiles constrain commands that Codex runs; they do not replace the action's `safety-strategy`."
- 관련 섹션: 에이전트 러너 격리, "에이전트 job과 게시 job 분리" 패턴, AGENTS.md가 공격 표면이 되는 역설

### 자료 41: PromptPwnd — Prompt Injection Vulnerabilities in GitHub Actions Using AI Agents (Aikido)
- 출처: https://www.aikido.dev/blog/promptpwnd-github-actions-ai-agents
- 저자·날짜: Rein Daelman / 2025-12-04 (2026-03-17 갱신)
- 신뢰성: 중~최상 (보안 기업 리서치, 벤더 블로그)
- 핵심 주장: 이슈 제목·본문을 그대로 프롬프트에 넣는 AI 워크플로가 권한 있는 도구를 실행해 시크릿을 유출. Gemini CLI, Claude Code Actions, Codex Actions, GitHub AI Inference 통합이 대상. 최소 5개 포춘 500 기업 영향 확인.
- 인용 가능한 구절:
  > "Untrusted user input → injected into prompts → AI agent executes privileged tools → secrets leaked or workflows manipulated."
  ```yaml
  ISSUE_TITLE: '${{ github.event.issue.title }}'
  ISSUE_BODY: '${{ github.event.issue.body }}'
  ```
  > 권고: 에이전트 도구 제한(이슈/PR 쓰기 금지), 입력 정제, "Treat AI-generated output as untrusted code requiring validation"
- 관련 섹션: 이슈/PR 텍스트로 트리거되는 에이전트 워크플로의 위험 (자료 15 스크립트 인젝션과 같은 구조임을 보여주기)

### 자료 42: Copilot coding agent GA + Risks and mitigations (GitHub)
- 출처: https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/ , https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations
- 저자·날짜: GitHub / 2025-09-25 GA, Docs 2026-09 조회 (문서상 명칭이 "Copilot cloud agent"로 바뀜)
- 신뢰성: 최상
- 핵심 주장: 이슈를 할당하면 Actions 기반 환경에서 드래프트 PR 생성. 쓰기 권한자만 할당 가능, `copilot/` 브랜치에만 푸시, 사람의 "Approve and run workflows" 전에는 CI가 돌지 않음, 방화벽으로 인터넷 제한, 커밋은 Copilot 작성·요청자 공동저자, 스스로 Ready for review/승인/머지 불가.
- 인용 가능한 구절:
  > "By default, workflows are not triggered until Copilot cloud agent's code is reviewed and a user with write access to the repository clicks the **Approve and run workflows** button."
  > "Copilot cloud agent cannot mark its pull requests as 'Ready for review' and cannot approve or merge a pull request."
  > "Copilot cloud agent's commits are authored by Copilot, with the developer who assigned the issue or requested the change to the pull request marked as the co-author."
- 주의: 명칭 변경(coding agent → cloud agent) — 본문 용어 표기 결정 필요. 조직 방화벽 설정은 2026-04-03 changelog, self-hosted 러너에서 돌리려면 방화벽을 꺼야 한다는 2차 보도(bex.co, 2026-07-28)는 교차 확인 필요.
- 관련 섹션: 에이전트가 PR을 만드는 팀의 가드레일 (branch protection·required checks가 그대로 적용된다는 점)

### 자료 43: Copilot code review now runs on an agentic architecture (GA)
- 출처: https://github.blog/changelog/2026-03-05-copilot-code-review-now-runs-on-an-agentic-architecture/
- 저자·날짜: GitHub / 2026-03-05
- 신뢰성: 최상
- 핵심 주장: Copilot 코드 리뷰가 도구 호출로 저장소 맥락을 수집하는 에이전트 구조로 전환, Pro/Pro+/Business/Enterprise GA. Actions 위에서 돌며 self-hosted 러너 조직은 1회 설정 필요. 누적 6천만 건 리뷰.
- 인용 가능한 구절:
  > "Copilot code review now runs on an agentic tool-calling architecture and is generally available for all users with Copilot Pro, Copilot Pro+, Copilot Business, and Copilot Enterprise."
  > "60 million Copilot code reviews and counting"
- 관련 섹션: AI 리뷰 봇 비교 (Copilot / Claude / CodeRabbit / Bugbot)

### 자료 44: Cursor Bugbot (Cursor Docs)
- 출처: https://cursor.com/docs/bugbot
- 저자·날짜: Cursor / 2026-09 조회
- 신뢰성: 최상 (벤더 공식 문서)
- 핵심 주장: `.cursor/BUGBOT.md` 계층 규칙, Autofix는 Cloud Agent가 새 브랜치 또는 기존 브랜치에 수정 푸시. "Cursor Bugbot" 체크는 기본 `neutral`이라 required로 걸어도 머지를 막지 않음 — 막으려면 fail-on-unresolved 설정.
- 인용 가능한 구절:
  > "requiring the status alone does not block merges on findings because findings default to `neutral`."
  > (규칙 파일) "always includes the root `.cursor/BUGBOT.md` file and any additional files found while traversing upward from changed files."
- 관련 섹션: AI 리뷰를 required check로 만들 때의 함정

### 자료 45: Copilot coding agent now supports AGENTS.md + Linux Foundation AAIF 설립
- 출처: https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions/ , https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
- 저자·날짜: GitHub / 2025-08-28, Linux Foundation / 2025-12-09
- 신뢰성: 최상
- 핵심 주장: Copilot 에이전트가 루트·중첩 AGENTS.md와 함께 `.github/copilot-instructions.md`, `.github/instructions/**.instructions.md`, `CLAUDE.md`, `GEMINI.md`를 읽는다. AGENTS.md는 AAIF(Linux Foundation) 산하로 이관, 6만 개 이상 프로젝트 채택. AWS·Anthropic·Cloudflare·Google·Microsoft·OpenAI 등이 플래티넘 회원.
- 인용 가능한 구절:
  > "With custom instructions, you can guide Copilot on how to understand your project as well as how to build, test, and validate its changes."
  > (AGENTS.md) "a simple, universal standard that gives AI coding agents a consistent source of project-specific guidance needed to operate reliably across different repositories and toolchains"
  > "embraced by more than 60,000 open source projects and agent frameworks including Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules and VS Code"
- 관련 섹션: AGENTS.md/CLAUDE.md 관례 — "빌드·테스트 명령을 적어 두는 것이 CI 정의와 같은 일"

### 자료 46: Announcing the 2025 DORA Report (Google Cloud Blog) + DORA 지표 5종
- 출처: https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report , https://dora.dev/guides/dora-metrics/ , https://dora.dev/insights/dora-metrics-history/
- 저자·날짜: Nathen Harvey, Derek DeBellis / 2025-09-24
- 신뢰성: 최상
- 핵심 주장: 응답자 약 5,000명. AI 사용 90%, 생산성 향상 체감 80%+, AI 생성 코드 불신(거의/전혀 신뢰 안 함) 30%. AI는 처리량(throughput)과 양의 관계, 안정성과는 여전히 음의 관계. 90%의 조직이 최소 하나의 내부 플랫폼 보유. 지표는 2024년부터 5종(변경 리드타임·배포 빈도·실패 배포 복구 시간·변경 실패율·배포 재작업률).
- 인용 가능한 구절:
  > "AI doesn't fix a team; it amplifies what's already there."
  > "AI's primary role is as an amplifier, magnifying an organization's existing strengths and weaknesses." (dora.dev)
- 주의: "7가지 AI 역량 모델"의 항목명은 이번 수집에서 원문 확보 실패 — 본문에 쓰려면 리포트 PDF에서 확인.
- 관련 섹션: DORA 지표, AI 섹션의 결론("빠른 피드백 루프와 자동화 테스트가 AI의 증폭 방향을 정한다")

### 자료 47: [AI활용] Claude 실무편 - kt cloud VM에서 PR 리뷰 자동화하기 (kt cloud 기술블로그)
- 출처: https://tech.ktcloud.com/entry/2026-08-ktcloud-claude-pr-review-automation
- 저자·날짜: 강민호 (kt cloud FE개발팀) / 2026-08-20
- 신뢰성: 최상 (회사 엔지니어링 블로그)
- 핵심 주장: GitHub Actions 대신 사내 VM에서 poller로 PR을 수집하고 Claude Code가 `.claude/architecture/architecture-rules.json` 규칙 기반으로 리뷰. 핵심은 "기준"의 명문화.
- 인용 가능한 구절:
  > "PR Review Bot은 단순한 스크립트가 아니라, 여러 구성 요소가 결합된 하나의 실행 시스템"
  > "리뷰 기준을 명확하게 정의하는 것"
  > "모든 PR이 동일한 기준으로 검증되기 때문에 리뷰어에 따른 품질 편차가 사라진다"
  > "시니어 리뷰어에게 집중되던 부담이 줄어든다"
- 관련 섹션: 한국 팀의 AI 리뷰 도입 사례, 러너 밖에서 돌리는 선택지

### 자료 48: PR 리뷰 에이전트 개발기 feat. Claude Agent SDK (하이퍼리즘 기술블로그)
- 출처: https://tech.hyperithm.com/review-agent
- 저자·날짜: Cheolwan Park (Hyperithm) / 2025-10-27
- 신뢰성: 최상 (회사 엔지니어링 블로그)
- 핵심 주장: 코드 유출 우려로 상용 SaaS 대신 자체 구축. 1단계 공격적 이슈 탐지 → 2단계 근거(Evidence)·반증(Mitigation) 수집으로 오탐 걸러냄. 57건 중 32건을 오탐으로 분류.
- 인용 가능한 구절:
  > "코드가 유출되어 라자루스 같은 해킹 그룹이 취약점을 발견한다면, 암호화폐를 취급하는 하이퍼리즘 같은 회사는 치명적인 피해를 입을 수 있습니다"
  > "이슈별로 Evidence(이슈가 실제 문제인 근거)와 Mitigation(이슈가 오탐일 수 있는 근거)을 모두 수집합니다"
  > "틀린 것, 빠진 것을 찾아내는 1차 리뷰 프로세스 역할은 충분히 수행"
  > "지금 방식은 에이전트라기 보다는 워크플로우에 가깝습니다"
- 관련 섹션: AI 리뷰의 노이즈(오탐) 관리, 보안 민감 조직의 선택

### 자료 49: AI 시대에 코드 리뷰, 어떻게 해야할까? (Flowkater.io)
- 출처: https://flowkater.io/posts/2026-03-08-ai-code-review/
- 저자·날짜: Tony Cho / 2026-03-08
- 신뢰성: 중 (개인 블로그, 인용 수치는 2차 인용)
- 핵심 주장: AI로 PR 수는 늘었지만 리뷰가 병목. diff가 아니라 스펙·의도를 리뷰하고, AI 리뷰+자동 테스트+사람의 의도 검증을 스위스 치즈처럼 겹쳐라.
- 인용 가능한 구절:
  > "AI 도입률이 높은 팀은 PR을 98% 더 많이 머지하지만 리뷰 시간은 91% 늘어났다"
  > "코드를 생성하는 비용이 0에 가까워질수록, 가치의 원천은 생성이 아니라 검증으로 이동한다"
  > "diff가 아니라 스펙을 리뷰하라. 구문이 아니라 맥락을 리뷰하라"
  > "스위스 치즈 모델처럼 불완전한 필터를 겹겹이 쌓아 구멍이 정렬되지 않도록"
- 주의: 98%/91% 수치는 블로그가 latent.space를 출처로 적었으나 원 조사는 Faros AI 보고서(2025)로 알려져 있음 — 본문 인용 시 원 출처 확인 필수. 400줄 결함 감지율은 SmartBear/Cisco 연구(고전 레퍼런스).
- 관련 섹션: AI 시대 리뷰 전략, "테스트가 곧 명세"

### 자료 50: 유연하고 안전하게 배포 Pipeline 운영하기 (토스 SLASH 23)
- 출처: https://toss.tech/article/slash23-devops
- 저자·날짜: 김동석 (토스뱅크 DevOps) / 2023-10-12
- 신뢰성: 최상 (회사 엔지니어링 블로그) — 도구는 GoCD 기반이라 GitHub Actions 직접 사례는 아님. 원칙 인용용 고전 레퍼런스
- 핵심 주장: 파이프라인 템플릿 변경은 영향 반경이 크므로 일부 파이프라인에서 먼저 검증. Pipeline as Code + 템플릿 + CI로 파이프라인 자체를 테스트.
- 인용 가능한 구절:
  > "CI는 Continuous Integration의 약자로, 변경 사항에 대하여 자동으로 검증을 진행하고 성공했을 때에만 반영하는 것을 말합니다."
  > "Template을 수정하면 많은 Pipeline에 한 번에 적용되기 때문에 실수를 했을 때 영향이 굉장히 큽니다."
  > "Pipeline 설정 파일 내용이 바뀌었다면 한 번 확인해 봐야 합니다."
- 관련 섹션: 재사용 워크플로를 조직 표준으로 만들 때의 위험(자료 2와 연결), 파이프라인 변경에 CODEOWNERS

---

## 소스 간 충돌·주의 요약 (fact-checker용)

1. **ECS blue/green 트래픽 전환**: AWS 블로그(2025-09-16) "all-at-once만 지원" vs What's New(2025-10-30) linear/canary 추가 → 2026-09 기준으로는 linear/canary 지원이 사실.
2. **Nx s1ngularity 날짜**: THN(2026-06) "March 2026" vs Wiz 등 다수 "2025-08-26~27" → 2025-08이 정설.
3. **tj-actions 피해 규모**: 23,000개(사용 저장소) vs 218개(유출 확인) — 서로 다른 지표.
4. **self-hosted 러너 과금**: "연기"(1차) — 폐기 확정이라는 2차 서술은 과장.
5. **Cloudflare Pages "deprecated"**: 2차 블로그 표현. 공식은 마이그레이션 가이드와 "merging" 수준.
6. **Copilot coding agent ↔ cloud agent 명칭**: 2026 문서에서 cloud agent로 개칭. 본문 표기 통일 필요.
7. **Cloudflare 프리뷰 용어 3종**: Preview URLs(2025-07, `--preview-alias`) / Worker Previews(`wrangler preview`, 4.135.0+) / Version URLs(프로덕션 리소스 사용).
8. **pull_request_target 기본 차단 정책 강제일 2026-11-02**: 책 출간 시점에 따라 "예정"→"시행"으로 바뀌는 항목.
9. **GitHub Actions 2026 보안 로드맵**: 발표(2026-03) 기준 프리뷰 3~6개월 — 2026-09 현재 출시 여부 미확인. "로드맵"으로만 표기.

## 수집 한계
- 수집 건수: 50건(URL 약 70개, 다수 항목이 1차 소스 묶음).
- 언어 비율: 한국어 자료 9건(자료 10·11·12·17·47·48·49·50 및 일부) — 대상 독자가 한국이지만 버전·API·수치는 1차 영문 공식 소스 우선 원칙 때문에 영어 비중이 약 80%. 한국 대형 테크 블로그(우아한형제들·카카오·네이버 D2·LINE)에서 2025~2026년 GitHub Actions/OIDC/Cloudflare 실전 글은 찾지 못함. 토스 글은 GoCD 기반.
- 접근 실패·미확보: dora.dev 리포트 본문(7가지 AI 역량 항목명), CodeRabbit 공식 문서(이번 회차 미수집 — 커뮤니티/보강 필요), AWS 공식 CDK diff-on-PR 가이드(발견 못 함), Cloudflare의 GitHub OIDC 지원 여부(공식 문서 미발견 → 미지원으로 추정, 확인 필요), App Runner 공지 원문 페이지(relnotes 배너만 확보), Renovate 공식 문서(미수집), GitHub Actions 2026 보안 로드맵 기능의 실제 프리뷰 출시 여부.
- 인용 방식 한계: WebFetch가 본문을 추출·정리하므로 영어 인용 일부는 원문과 미세하게 다를 수 있다. 수치·날짜·버전은 URL에서 재대조 권장.
- 의도적 제외: 날짜 없는 SEO형 튜토리얼(oneuptime, vibecodingwithfred 등은 참고만 하고 본 목록에서 제외), 벤더 비교 마케팅 글(weavai 등), 논문(arXiv GitInject 등은 paper-researcher 영역), Reddit/HN 토론(community-researcher 영역).
