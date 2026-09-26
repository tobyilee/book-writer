# GitHub·AWS·Cloudflare를 쓰는 개발자를 위한 CI/CD (+ AI 코딩 도구 시대의 팀 팁) 레퍼런스

- genre: tech-book / 대상: 한국 실무 개발자 / 슬러그: `cicd-github-aws-cloudflare`
- 합성 시점: 2026-09-26. 원천: `research/web.md`(웹, 자료 1~50), `research/papers.md`(논문 1~56), `research/community.md`(커뮤니티 패턴 1~12·휴리스틱 1~10·논쟁 A~G). 원천 파일은 fact-checker의 1차 대조 근거이므로 보존한다.
- **팩트체크 정정 (2026-09-26, `factcheck_log.md`가 이 문서보다 우선):** (1) Worker Previews가 자동 격리하는 것은 Durable Objects뿐이며 D1·KV·R2는 `previews` 블록에 별도 바인딩해야 한다. "Preview URLs"는 별칭 붙은 Version URL(`wrangler versions upload --preview-alias`)로 프로덕션 리소스를 친다. (2) Workers 버전에는 코드·정적 에셋·바인딩·호환성 설정이 포함되며, 바깥에 있는 것은 D1·KV의 데이터뿐이다. (3) P-47(Qodo 연구)의 22는 설문 응답 실무자 수이고 분석 규모는 3개 프로젝트·PR 4,335건이며 "Beko"라는 기업명은 초록에 없다. (4) GitHub OIDC immutable `sub` 클레임 변경은 실재한다 — GitHub Changelog 2026-04-23, 2026-07-15 이후 생성·이름 변경·이전된 저장소에 자동 적용.
- 출처 유형 태그: **[웹]** 공식 문서·체인지로그·회사 블로그·언론 / **[논문]** 동료 심사 논문(프리프린트는 [프리프린트], 산업 보고서는 [그레이]) / **[커뮤니티]** HN·Lobsters·GitHub Issues·GeekNews·velog 등 — 커뮤니티 주장은 모두 "개인 의견·검증 필요" 전제.
- 원천 참조 표기: `W-n` = web.md 자료 n, `P-n` = papers.md 논문/자료 n, `C-패턴n`/`C-휴n`/`C-논쟁X` = community.md.
- 수집 도구(WebFetch)가 본문을 추출·정리했으므로 영어 인용은 원문과 미세하게 다를 수 있다. 수치·버전·날짜는 원 URL에서 재대조할 것 (W 머리말).
- **"확인 필요"** = 출처 불분명·2차 소스 단독·익명 주장뿐. **"쓰지 말 것"** = 원천에 붙어 있던 경고를 그대로 옮긴 것.

---

## 0. 빠른 참조: 주요 액션·도구 최신 버전 (GitHub Releases API, 2026-09-26 조회) [웹] (W-0)

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

- 재현: `gh api "repos/{owner}/{repo}/releases?per_page=2"`.
- 주의(원천 경고): 공식 문서 예제의 버전이 제각각이다(Claude Code·Cloudflare 문서 예제는 `actions/checkout@v6`, 최신은 v7). 본문 예제는 한 버전으로 통일하고 "2026년 9월 기준"을 명시할 것. wrangler는 거의 매일 마이너가 올라가므로 본문에선 "wrangler 4.x"로 적는 편이 안전하다.

---

## 1. 개념과 정의

### 1.1 CI/CD와 그 효과에 대한 근거
- **CI의 정의(한국어 인용용):** "CI는 Continuous Integration의 약자로, 변경 사항에 대하여 자동으로 검증을 진행하고 성공했을 때에만 반영하는 것을 말합니다." — 토스 SLASH 23 (2023-10-12, GoCD 기반) [웹] (W-50)
- **CI는 속도와 품질의 교환이 아니다:** "Our main finding is that continuous integration improves the productivity of project teams, who can integrate more outside contributions, without an observable diminishment in code quality." — Vasilescu et al., ESEC/FSE 2015 (초록; 상관 기반 관측 연구라는 점을 덧붙일 것) [논문] (P-1)
- **CI는 민간요법이 아니라 데이터:** GitHub 프로젝트 34,544개·빌드 1,529,291건·설문 442명. "we show evidence that supports the claim that CI helps projects release more often" / "developers, tool builders, and researchers make decisions based on folklore instead of data." — Hilton et al., ASE 2016. "릴리스 빈도 약 2배" 같은 구체 수치는 초록에 없음 → **미확인** [논문] (P-2)
- **CI의 세 긴장 축:** "speed and certainty (Assurance), ... better access and information security (Security), ... more configuration options and greater ease of use (Flexibility)." — Hilton et al., ESEC/FSE 2017. 책 전체 설계 축 후보(빌드 시간 / 시크릿·OIDC / 재사용 워크플로) [논문] (P-3)
- **CI 극장:** Travis CI 1,270개 프로젝트. 약 60%(748개)가 드문 커밋, 커버리지 확인 가능 51개 평균 78%(Ruby 86%, Java 63%), "85% of the studied projects have at least one broken build that take more than four days to be fixed", 대부분은 "10분 규칙" 이내 빌드 — Felidre et al., ESEM 2019 (초록) [논문] (P-4)

### 1.2 DORA 지표
- Accelerate(2018)의 4대 지표(배포 빈도·변경 리드타임·변경 실패율·복구 시간), 속도와 안정성이 상충하지 않는다는 주장의 원전 — Forsgren, Humble, Kim. 정확한 정의 문구는 원서 확인 필요 [논문/단행본] (P-38)
- **현행(2024년부터) 5종:** 변경 리드타임·배포 빈도·실패 배포 복구 시간·변경 실패율·배포 재작업률 — dora.dev [웹] (W-46)
- 표기 원칙: Accelerate 4지표는 "원전", 본문 현행 정의는 dora.dev 5종으로.

### 1.3 GitHub Actions 핵심 개념 (현행 사양)
- **재사용 워크플로 한도:** "You can now use up to 10 nested reusable workflows and call up to 50" (이전 한도 4, 20) — 2025-11-06 [웹] (W-2)
- **재사용 워크플로 자기 출처 컨텍스트:** `job.workflow_ref`·`job.workflow_sha`·`job.workflow_repository`·`job.workflow_file_path` — 2026-09-03 (GHES 미지원) [웹] (W-1)
- **`GITHUB_TOKEN`의 `vulnerability-alerts` 권한:** "read"·"none" 값 — 2026-09-03 [웹] (W-1)
- **러너 버전 지원 종료 조회 API:** `GET /actions/runners/deprecations/{version}` → `runner_version`, `runtime_deprecates_at`, `registration_deprecates_at` — 2026-09-03 [웹] (W-1)
- **concurrency 큐:** 과거엔 "one run in progress and one pending run" — 새 run이 들어오면 pending이 취소·교체. 2026-05-07부터 그룹당 "up to 100 queued jobs or workflow runs" FIFO. `queue: max`는 `cancel-in-progress: true`와 함께 쓸 수 없다 [웹] (W-3)
  ```yaml
  concurrency:
    group: my-group
    cancel-in-progress: false
    queue: max
  ```
- **environment `deployment: false`:** 시크릿·변수 스코프 용도로만 쓰고 배포 레코드 미생성. "this option is unavailable if you've implemented custom deployment protection rules." — 2026-03-19 [웹] (W-4)
- **cron 타임존:** `timezone: "America/New_York"` 형태의 IANA 타임존 — 2026-03-19. 한국 독자용 예시는 `Asia/Seoul` [웹] (W-4)
- **OIDC custom properties 클레임 GA:** "use repository custom properties as claims in your OIDC tokens to create more granular trust policies" — 2026-04-02 [웹] (W-5)
- **allowed actions 설정 전 플랜 확대**(Free·Team 포함), Go 기반 Runner Scale Set Client(K8s 불필요, 퍼블릭 프리뷰), `windows-2025-vs2026` 이미지 — 2026-02-05 [웹] (W-5)
- **머지 큐:** "You **must** use the `merge_group` event to trigger your GitHub Actions workflow when a pull request is added to a merge queue." Build concurrency는 `1`~`100` [웹] (W-6)
  ```yaml
  on:
    pull_request:
    merge_group:
  ```
- **캐시 한도:** "All repositories will continue to receive access to 10 GB, which is provided at no additional cost." 초과분 종량 과금(Pro/Team/Enterprise), "cache size eviction limit (GB) and cache retention limit (days)" 엔터프라이즈→조직→저장소 캐스케이드 — 2025-11-20 [웹] (W-7)

### 1.4 공급망 보안 개념
- **4개 CI 보안 속성:** Admittance Control, Execution Control, Code Control, Access to Secrets — Koishybayev et al., USENIX Security 2022. 보안 챕터 뼈대로 재사용 가능 [논문] (P-14)
- **안전한 공급망 3속성:** 투명성(transparency)·유효성(validity)·분리(separation) — Okafor et al., SCORED '22. SLSA·서명·OIDC 단기 자격증명을 이 세 단어로 묶기 [논문] (P-21)
- **공격 지도:** 107개 공격 벡터, 94개 실사고, 33개 방어책, 전문가 17명·개발자 134명 검증 — Ladisa et al., IEEE S&P 2023 [논문] (P-20). 실제 악성 패키지 174개(2015-11~2019-11, npm·PyPI·RubyGems) — Ohm et al., DIMVA 2020 [논문] (P-19)
- **Sigstore:** OIDC 신원 기반 keyless 서명 + 투명성 로그. "From the effects of XCodeGhost to SolarWinds, hackers have identified that targeting weak points in the supply chain allows them to compromise high-value targets" — Newman et al., CCS 2022. SLSA 자체는 OpenSSF 명세(학술 논문 아님) [논문] (P-22)
- **Artifact attestation & SLSA:** 아티팩트 다이제스트를 in-toto 형식 SLSA provenance에 묶고 Sigstore 단기 인증서로 서명. "Artifact attestations by itself provides SLSA v1.0 Build Level 2." 재사용 워크플로로 빌드 지침을 저장소 밖에 두면 L3. v4부터 `attest-build-provenance`는 `actions/attest` 래퍼 — "new implementations should use actions/attest instead." 검증은 `gh attestation verify` [웹] (W-25)
- **Immutable releases GA (2025-10-28):** "Once you publish a release as immutable, its assets can't be added, modified, or deleted." / "Tags for new immutable releases are protected and can't be deleted or moved." 에셋별 서명된 release attestation 자동 생성 [웹] (W-19). 커뮤니티 반응: "Wait?! They weren't immutable before?" [커뮤니티] (C-휴2)

### 1.5 AI 코딩 에이전트 관련 용어 (표기 통일 필요)
- **Copilot coding agent → Copilot cloud agent:** 2025-09-25 GA 당시 명칭은 coding agent, 2026 문서상 "Copilot cloud agent"로 개칭 [웹] (W-42). 본문 용어 표기 결정 필요.
- **AGENTS.md:** "a simple, universal standard that gives AI coding agents a consistent source of project-specific guidance..." Linux Foundation AAIF(2025-12-09) 산하로 이관, "embraced by more than 60,000 open source projects and agent frameworks including Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules and VS Code". AWS·Anthropic·Cloudflare·Google·Microsoft·OpenAI 등 플래티넘 회원 [웹] (W-45)
- Copilot 에이전트가 읽는 지시 파일: 루트·중첩 AGENTS.md, `.github/copilot-instructions.md`, `.github/instructions/**.instructions.md`, `CLAUDE.md`, `GEMINI.md` — 2025-08-28 [웹] (W-45)
- **GitHub Agentic Workflows(gh-aw):** Markdown 지시 파일 기반 에이전트 워크플로. 1,248개(276 저장소) 분석 — 지시문 중앙값 556.5단어, 62.1% 코드 블록 포함, 4개월째에도 78.2% 갱신, "only 9.4% explicitly address prompt-injection defense." — Khelifi et al., 2026-09-23 게시 [프리프린트] (P-56). gh-aw 기능 현황은 웹 교차 확인 안 됨.

---

## 2. 핵심 관점들

### 2.1 워크플로는 멍청하게, 로직은 로컬에서 도는 스크립트로
- 커뮤니티 최다 동조 휴리스틱: "Don't have logic in your workflows. Workflows should be dumb and simple (KISS) and they should call your scripts." — 1a527dd5 / "No matter which CI you use, you're in for a bad time if you don't do this." — thiht (HN) [커뮤니티] (C-휴1)
- "An ideal action has 2 steps: (1) check out the code, (2) invoke a sane script that you can test locally." — iamcalledrob (HN, 2026-01-14 스레드) [커뮤니티] (C-패턴1)
- 변형: Makefile 얇은 래퍼, mise tasks, make+nix, 프로젝트 언어로 CI 구현, "only implement your logic in a tool that has a debugger" [커뮤니티] (C-휴1)
- 비용 논리로 같은 결론: "don't couple yourself to a specific product. If you do, you're gonna get screwed eventually. It happened with TravisCI, CircleCI, now it's happening with GitHub." — physicsguy [커뮤니티] (C-휴10)
- 반론은 4.1 참조.

### 2.2 보안의 세 규칙: 최소 권한, 신뢰 불가 입력은 env로, SHA 고정
- 교차 관찰(P 교차관찰 3): GHA 보안 문제는 기본값과 참조 방식에 몰려 있다 — 과권한(P-14, P-12), 신뢰 불가 입력 인젝션(P-15, P-55), 태그 참조(P-18, P-11) [논문]
- GitHub 공식 하드닝(Secure use reference) [웹] (W-15):
  - 스크립트 인젝션: "set the value of the expression to an intermediate environment variable"
  - "Pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release."
  - "set the default permission for the `GITHUB_TOKEN` to read access only for repository contents"
  - self-hosted runners "should almost never be used for public repositories"
  - 클라우드 인증은 OIDC, 워크플로 파일은 CODEOWNERS로 보호
- 실증 근거:
  - "99.8% of workflows are overprivileged and have read-write access (instead of read-only) to the repository." 447,238개 워크플로(213,854 저장소). 23.7%가 pull_request로 트리거되며 저장소 코드 사용, 99.7% 저장소가 외부 액션 실행, 97%가 검증되지 않은 제작자 액션 최소 1개, 18%가 보안 업데이트 누락 액션 — USENIX Security 2022 [논문] (P-14). **신선도: "당시(2022)" 수치로 표기할 것.** 이후 GitHub가 신규 저장소 `GITHUB_TOKEN` 기본값을 읽기 전용으로 조정했다는 점은 원천에서 현행 기본값 확인 필요로 남음.
  - 컴플라이언스: 95개 Java 워크플로 30개 기준 — "overall compliance is 28%, dropping to 4% for permission controls; Security (26%) lags far behind Clarity (68%)." LLM 간 합의 Fleiss κ=0.28, 다단 판정으로 검증 노력 81% 절감 — EASE 2026 [논문] (P-12)
  - "Compliance gaps are widespread, especially in permissions, timeout configuration, and SHA pinning, while reusable workflows remain rare." 공통 파이프라인 접두어 39.5% — Abrokwah & Ghaleb 2025 [프리프린트] (P-11). **"SHA pinning 6.3% vs 태그 93.7%"는 초록에 없음 — 본문 사용 금지(확인 필요).**
  - `actions/missing-workflow-permissions` — "one of the most frequent findings in Actions workflows"; CodeQL 프리뷰 기간 "over 158,000 repositories" / "more than 800,000 potential vulnerabilities" / "approximately 15%" 수정 — 2025-04-22 GA [웹] (W-23)
  - ARGUS: 워크플로 2,778,483개·액션 31,725개 분석, 워크플로 4,307개·액션 80개에서 치명적 인젝션, 기존 기법 대비 7배 이상 탐지(USENIX 페이지·검색 요약 기준) — USENIX Security 2023 [논문] (P-15)
  - GHAST: 50개 프로젝트에서 "a total of 24,905 security issues" — SCORED '22 [논문] (P-16)
  - 9개 스캐너 비교: "these scanners implement fundamentally different analysis strategies, leading to major gaps..." — 2026 [프리프린트] (P-17) → "스캐너 하나 돌렸다고 안심하지 말 것"
- **"태그는 움직인다":** Software Heritage 3억 2,840만 저장소에서 1,020만 건 태그 변경, 18.9만 저장소 영향, Nixpkgs 교차 분석 32개 중 7개 실제 빌드 오류. "We therefore recommend that build systems and package managers pin dependencies to cryptographic commit hashes" — 2026 [논문] (P-18)
- **SHA 고정을 사람의 규율이 아니라 정책으로:** 조직/저장소 정책으로 SHA 미고정 액션 실행 거부, `!` 접두어로 차단. "The blocklist is evaluated last, overriding any other policy that would otherwise allow the action." — 2025-08-15 [웹] (W-18). "You can enforce at the org level to only allow actions pinned to hashes." — AlecBG [커뮤니티] (C-패턴9)
- **SHA 고정 갱신은 봇으로, 자동 머지는 금지:** Renovate가 태그를 SHA로 바꾸고 주석으로 버전 표기(arionmiles) / "Hundreds of projects even auto-accept PRs bumping pinned hashes." — alerque [커뮤니티] (C-휴2). 도구: pmw, frizbee, Renovate. (Renovate 공식 문서는 미수집)
- **Dependabot 기본 쿨다운(2026-07-14):** "Dependabot now waits until a new release has been available on its registry for at least three days before opening a version update pull request." 보안 업데이트는 쿨다운 무시. 옵션 자체는 2025-07-01 GA [웹] (W-24). 주의: dependabot-core #13078·#13691 — github-actions 생태계 쿨다운이 태그 커밋 날짜 기준으로 계산되어 릴리스 잦은 액션은 업데이트가 영영 안 뜨는 문제 보고 [커뮤니티성, 확인 필요] (W-24)

### 2.3 장기 자격증명 대신 OIDC — 그리고 Cloudflare의 비대칭
- AWS OIDC: 공급자 URL `https://token.actions.githubusercontent.com`, audience `sts.amazonaws.com`, 워크플로 `id-token: write` 필요 [웹] (W-13)
  ```json
  "Condition": {
    "StringLike": { "token.actions.githubusercontent.com:sub": "repo:octo-org/octo-repo:*" },
    "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" }
  }
  ```
  - 원천 경고: 문서 예제의 `repo:octo-org/octo-repo:*`는 모든 브랜치·PR을 허용한다. 본문에선 `repo:org/repo:environment:production` 또는 `ref:refs/heads/main`으로 좁히는 예를 권장(custom properties 클레임도 대안) (W-13)
- configure-aws-credentials v6.3.0: `role-session-name` 기본 "GitHubActions", `role-duration-seconds` 기본 3600(900~43200) [웹] (W-14)
- 장기 키가 새는 규모: "not only is secret leakage pervasive -affecting over 100,000 repositories -but that thousands of new, unique secrets are leaked every day." — Meli et al., NDSS 2019 [논문] (P-23). IaC 하드코딩 비밀: "a hard-coded secret can persist for as long as 98 months, with a median lifetime of 20 months." — ICSE 2019 (Puppet 등 당시 도구 중심, 일반화 주의) [논문] (P-36)
- **Cloudflare 측:** wrangler-action은 `apiToken`·`accountId`로 배포, "Never commit `CLOUDFLARE_API_TOKEN` to your repository." [웹] (W-33). **Cloudflare가 GitHub OIDC 페더레이션을 지원하는지 공식 문서 미발견 → 미지원 추정, 확인 필요.** AWS와 달리 장기 API 토큰을 시크릿으로 둘 수밖에 없다는 비대칭은 본문 소재 (W-33)
- 비대칭 완화책: Worker 단위 역할 4종(Metadata Read-Only, Content Read-Only, Editor, Admin), 계정 소유 API 토큰을 "Specified Workers"로 스코프 — "For an agent or CI/CD workflow, go to Manage Account > Account API Tokens and create an account-owned API token. Set the scope to Specified Workers". Editor: "Deploy and update capabilities without deletion permissions" — 2026-09-15 [웹] (W-34)
- **배포 시크릿은 main(리뷰 후)에만:** "You can ensure your main branch (ie: post review) is the only one with deployment secrets, that workflows such as 'build/test' have no secrets at all" — insanitybit / "The production/release tokens should ideally not be on the same system as the ones doing regular CI." — ashishb (Lobsters) [커뮤니티] (C-휴3) → Environments + OIDC `sub`를 environment로 좁히는 방식과 연결

### 2.4 배포 안전성: 점진 배포·자동 롤백·"성공"의 정의
- 대규모 사례: Azure Gandalf — 장애 신호와 롤아웃의 시공간 상관으로 나쁜 롤아웃을 광역 장애 전에 차단, 18개월 이상 운영, 데이터 플레인 정밀도 92.4%·재현율 100%, 컨트롤 플레인 94.9%·99.8% — NSDI 2020 [논문] (P-33). Facebook 설정 관리(매일 수천 건 설정 변경, 배포와 기능 공개 분리의 원형) — SOSP 2015 [논문] (P-32). Facebook·OANDA 지속적 배포 — ICSE 2016 SEIP(결과 수치 미확인) [논문] (P-31)
- 소규모 팀 버전: CloudWatch 알람 + ECS 네이티브 롤백, Workers gradual deployments (3.2·3.3 참조)
- 커뮤니티 교훈: Cloudflare 2025-11-18 장애 사후분석 HN(916 댓글) — "Their bot management system is designed to push a configuration out to their entire network rapidly... it creates risk as compared to systems that roll out changes gradually." — abalone [커뮤니티] (C-논쟁G)
- 배포 "성공"은 "내가 올린 리비전이 active인가"로 판정 (3.2, C-휴4)

### 2.5 AI는 증폭기 — 기본기가 더 중요해진다
- "AI doesn't fix a team; it amplifies what's already there." — 2025 DORA (Google Cloud Blog, 2025-09-24) / "AI's primary role is as an amplifier, magnifying an organization's existing strengths and weaknesses." (dora.dev) [웹/그레이] (W-46, P-40)
- DORA 2024(2024-10-23): "As AI adoption increased, it was accompanied by an estimated decrease in delivery throughput by 1.5% and an estimated reduction in delivery stability by 7.2%". "AI 도입 25% 증가 시"라는 조건은 2차 요약 기준, 블로그 인용문에서 미확인. 표본 "39,000명 이상"도 검색 요약 기준(공식 원문 미확인) [그레이] (P-39)
- DORA 2025: 약 5,000명("nearly 5,000 technology professionals"), AI 사용 90%, 80% 이상 생산성 향상 체감, 30%는 AI 생성 코드를 거의/전혀 신뢰 안 함. AI 도입이 처리량·제품 성과와 양(+)의 관계, "AI adoption does continue to have a negative relationship with software delivery stability". 90% 조직이 최소 하나의 플랫폼 보유. 7개 팀 아키타입, 7개 역량 DORA AI Capabilities Model — **7개 역량 항목명은 원문 미확보, 본문에 쓰려면 리포트 PDF 확인** [그레이/웹] (P-40, W-46)
- 교차 관찰(P 교차관찰 1): 같은 결론이 세 층에서 반복 — CI는 품질 손실 없이 처리량↑(P-1), DORA는 작은 배치·테스트가 성과를 가름(P-38~40), 에이전트 PR도 작고 CI를 통과해야 병합(P-50). 책의 척추 메시지 후보.
- "지시문은 가드레일이 아니다, 권한이 가드레일이다": CLAUDE.md에 "프로덕션 연결 시 실행 금지"라고 쓴 것은 "doesn't 'prevent' Claude code from doing anything, what it does is insert these instructions into the context window" — avree (HN) [커뮤니티] (C-휴6)
- "코드를 생성하는 비용이 0에 가까워질수록, 가치의 원천은 생성이 아니라 검증으로 이동한다" — Flowkater.io (2026-03-08, 개인 블로그) [웹] (W-49) / "코드를 빨리 만들었다는 것은 일을 끝낸 것이 아니라, 그 코드가 작동한다는 증거를 만드는 단계로 일을 넘긴 것" — GeekNews [커뮤니티] (C-패턴11)

---

## 3. 대표 사례 (플랫폼·배포 대상별)

### 3.1 러너·비용·속도

**가격(2026-09 기준) [웹] (W-8)**
- 2026-01-01부터 GitHub-hosted 러너 가격 최대 39% 인하, 이 가격에 분당 $0.002 "Actions cloud platform charge" 포함.
- "Linux 2-core (x64): $0.006 / Linux 2-core (arm64): $0.005 / Linux 4-core: $0.012 / Linux 8-core: $0.022 / Linux 16-core: $0.042 / Windows 2-core (x64): $0.010 / macOS 3-4 core: $0.062"
- "Included minutes cannot be used for larger runners" / "The larger runners are not free for public repositories." / "96% of customers see no bill change"
- self-hosted 과금: "We're postponing the announced billing change for self-hosted GitHub Actions to take time to re-evaluate our approach." (당초 2026-03-01 시행 예정) → 4.3 충돌 참조.
- 구 URL resources.github.com은 github.com/resources/insights/...로 308 리다이렉트.

**arm64 러너 [웹] (W-9)**
- 퍼블릭 GA 2025-08-07(4 vCPU, 무료), 프라이빗 2026-01-29(2 vCPU, 플랜 무료 분 차감). 라벨 `ubuntu-24.04-arm`, `ubuntu-22.04-arm`, `windows-11-arm`. "native multi-architecture builds without the overhead of virtualization or emulation." Graviton(ECS/Lambda arm64) 배포 팀에 유리.

**비용·자원 실증 [논문]**
- "CI/CD imposes significant costs, e.g., $504 per year for an average paid-tier repository." 자원의 91.2%가 테스트·빌드, 트리거 PR 50.7%·push 30.9%·스케줄 15.5%, 캐싱 채택 32.9%(유료 저장소), 비활성 저장소 스케줄 워크플로 중단만으로 1.1~31.6% 절감 — Bouzenia & Pradel, ICSE 2024. **신선도: 연구 시점 가격 기준, 현행 요금과 병기** (P-7)
- 워크플로 유지보수는 "hidden costs of automation" (P-8, 프리프린트). 49K+ 저장소·267K+ 변경·3.4M+ 파일 버전(2019-11~2025-08): 저장소당 워크플로 중앙값 3개, 워크플로 파일의 7.3%가 매주 변경, 변경의 약 3/4은 단일 변경. "We did not find any conclusive evidence of the effect of LLM coding tools..." — JSS 2026 (P-9)
- 캐싱 유지보수: 952개 저장소(도입 266·미도입 686), 워크플로 1,556개, 설정 변경 17,185건, 저장소당 평균 9.37회 캐시 관련 변경, 파라미터 수정은 사람·버전 업데이트는 봇 — 2026 [프리프린트] (P-13)
- 캐싱 상한 감각: Kotinos — 14,364건 빌드 중 87.9% 이상이 가속 대상, 가속 빌드의 74%가 2배 속도 — IEEE TSE 2022 (P-30)
- 테스트 선택 근거: "very few of our tests ever fail, but those that do are generally \"closer\" to the code they test", 최근 3명 넘는 개발자가 수정한 코드가 더 자주 깨짐 — Google, ICSE-SEIP 2017 (7번째 저자 Micco는 Crossref 미확인) (P-27)
- 빌드 시간과 깨짐: 588개 프로젝트·924,616건 — "actions to fix build breakages (e.g., retrying or waiting for build commands) not only increase build durations but also do not guarantee passing builds." 약 1/3 프로젝트가 시간·안정성 중 하나를 희생 — IEEE TSE 2023 (P-29). 긴 빌드 요인(Ghaleb 2019, EMSE)은 초록 조회 실패 (P-28)

**한국 회사 사례 [웹]**
- 레몬베이스: FE/BE 병렬화 "27분에서 18분", Docker 이미지 재사용 "18분에서 15분", 최종 "배포 시간 55% 감소(27분 -> 12분)". "path-filter를 사용했으나, 롤백 시 문제되는 상황을 발견" → 워크플로 옵션으로 대체 (GeekNews 2024-08-14 요약 경유, 신뢰성 중) (W-11)
- F-Lab: `dorny/paths-filter` + 프로젝트별 yml 분리로 "기존 CI 실행 시간의 `절반` 수준" (2023-08-07, 액션 버전 구버전 가능) (W-12)
- 버즈빌: GitHub 지원 ARC(Runner Scale Set)로 self-hosted 운영. "커뮤니티 지원 ARC는 시간당 1,000개의 깃허브 API 개수 제한을 초과해 API 속도 제한 문제가 발생합니다" (2024-01-01, ARC 정보 구버전 가능) (W-10)
- 카카오엔터프라이즈: 젠킨스 인스턴스 관리 부담에서 벗어나 "GitHub 페이지에서 바로 빌드 결과를 확인/실행"하는 점을 GHA 장점으로 [커뮤니티/회사 블로그] (C-논쟁A)

**캐시 고통 [커뮤니티] (C-패턴3)**
- 벤더 수치(이해관계 있음, 검증 필요): "~1.2 GB node_modules 캐시 복원 38초 vs warm npm ci 6초", "10 GB per-repo 캐시 한도로 eviction → warm 빌드가 cold로" (BuildPulse, Tenki)
- self-hosted 러너에서 캐시가 퍼블릭 인터넷을 경유해 느리고 전송 비용 발생 (actuated)

### 3.2 AWS 배포 대상

**ECS 네이티브 점진 배포 [웹] (W-26)**
- 2025-07-17 built-in blue/green(ALB·NLB·Service Connect), Lambda 라이프사이클 훅, 베이크 기간 중 자동 롤백, CloudWatch 알람·circuit breaker 연동 → 2025-10-30 linear·canary 추가 → 2026-02 NLB에도 linear/canary 확장. "CodeDeploy는 이제 필수가 아니다."
- linear: 동일 비율 단계로 트래픽 이동, 단계별 bake time / canary: 소량 트래픽 후 canary bake time 경과 시 나머지 전환.
- CodeDeploy→ECS 이관: "CodeDeploy uses a TaskSet, whereas Amazon ECS uses a ServiceRevision." / 대기 시간은 ECS에선 훅으로 구현 — AWS Containers Blog 2025-09-16 (W-27). **같은 글의 "As of this writing, ECS blue/green only supports all-at-once."는 2025-10 이후 사실과 다름 — 구버전 정보로 인용하지 말 것** (4.3 참조)

**ECS 배포 "성공"의 함정 [커뮤니티] (C-패턴7, C-휴4)**
- "The GitHub action reports success in the case that the service stabilizes after a rollback is triggered by the circuit breaker" — amazon-ecs-deploy-task-definition #191. 제안: 안정화 후 "the expected task revision is contained in the active deployment"인지 확인.
- containers-roadmap #1488: circuit breaker가 FAILED에 머물고 롤백 안 되는 사례, 단일 태스크 서비스 실패 감지 약 100분 보고 — **검증 필요**.
- 한국 사이드 프로젝트 패턴: 커밋 SHA 이미지 태그(`:latest` 대신), 헬스체크 실패 시 이전 태그 롤백, 롤백 실패면 파이프라인 실패 (B-TING #328, assistudy-toy #39).

**App Runner → ECS Express Mode [웹] (W-28)**
- "AWS App Runner will no longer be open to new customers starting April 30, 2026. If you would like to use App Runner, sign up prior to that date. Existing customers can continue to use the service as normal." (공지 게시일 2026-03-31 추정, relnotes 배너만 확보)
- 대안 ECS Express Mode(2025-11 발표): 이미지 하나로 ECS 서비스·HTTPS 엔드포인트·오토스케일링, 리소스는 계정에 노출, "available now in all AWS Regions at no additional charge". Graviton 지원 2026-09.
- 원천 경고: 신규 독자는 App Runner를 쓸 수 없다. 본문은 "App Runner → ECS Express Mode"로 대체 권장.

**Lambda [웹] (W-29)**
- `aws-actions/aws-lambda-deploy`(2025-08-07): zip·컨테이너 이미지, 패키징 자동, OIDC, 런타임·메모리·타임아웃·환경변수 선언적 설정, dry-run, 대용량은 S3 경유. "Starting today, the new GitHub action provides a simplified way to deploy changes to Lambda functions using declarative configuration." SAM/CDK와의 구분(함수 코드만 vs 인프라 전체).

**IaC 파이프라인 [웹] (W-30)**
- Terraform: PR 커밋마다 speculative plan → PR 코멘트/링크, main 머지 시 apply. setup-terraform v4.0.1(2026-05-12).
- 주의: PR 코멘트 65,535자 제한으로 큰 plan 코멘트 실패 가능(2차 소스) → plan 전문은 아티팩트/Step Summary로.
- CDK diff-on-PR 공식 AWS 가이드는 이번 조사에서 발견 못 함(서드파티 `cdk-diff-action` 다수).
- IaC 결함 근거: 7가지 보안 스멜, 293개 저장소 15,232 스크립트에서 21,201건(하드코딩 비밀번호 1,326건), 버그 리포트 1,000건 중 응답 212·수정 수용 148 — ICSE 2019 [논문] (P-36). 8개 범주 결함 분류(OpenStack 1,448 커밋, 실무자 66명, 291 저장소 80,425 커밋) — ICSE 2020 [논문] (P-37). IaC 매핑 스터디(P-35, 세부 초록 미확인).

### 3.3 Cloudflare

**Pages → Workers static assets [웹] (W-31)**
- 정적 사이트는 `pages_build_output_dir` → `assets.directory` 한 줄 변경. SPA/404는 `not_found_handling` 명시, 기본은 정적 에셋 우선(`run_worker_first`로 변경). 정적 에셋 요청 무료.
- "Workers has a distinctly broader set of features available to it, (including Durable Objects, Cron Triggers, and more comprehensive Observability)."
  ```jsonc
  { "name": "my-worker", "compatibility_date": "2026-09-25", "assets": { "directory": "./dist/client/" } }
  ```
- 원천 경고: "Pages가 deprecated되었다"는 2차 블로그 표현(vibecodingwithfred 등). 공식은 "merging"/마이그레이션 권장 수준 — **본문에서 "폐지"라고 단정하지 말 것.**
- 전환기 혼란 [커뮤니티] (C-패턴8): HN "Cloudflare recommends migrating from Pages to Workers"(2025-08-10) — AWS를 레지스트라로 쓰는 merek은 Workers가 "Custom domains outside Cloudflare zones"를 지원하지 않아 Pages를 써야 했다(AWS DNS 팀에 직접 관련). 리전 지정은 enterprise plan만(scottydelta). Kenton Varda 발언으로 전해지는 "We are taking all the Pages-specific features and turning them into general Workers features"는 2차 인용 — **원문 확인 필요**. workers-sdk #8851(3.114.x는 되고 4.x 실패), #10441(API 504), "Missing entry-point to Worker script or to assets directory"(Cloudflare Community), `cloudflare/pages-action` 저장소 삭제로 "Unable to resolve action" → wrangler 직접 호출 교체(한국 개인 리포 PR) → **액션 의존 자체가 리스크**. `--branch=main` 누락 시 preview로 배포된다는 팁(velog).

**PR별 프리뷰: 용어 3종 [웹] (W-32)** — 본문 표기 통일 필수
- **Preview URLs** (2025-07, `--preview-alias`, Wrangler 4.21.0+)
- **Worker Previews** (`wrangler preview`, Wrangler 4.135.0+; wrangler-action의 `preview` 명령 예제는 4.136.3+): "Previews give each branch an isolated, production-like environment under the same Worker" / "Previews are the recommended way to test changes before production." 대부분 바인딩은 Preview별 격리 사본이지만 예외 — "Service bindings from a Preview call the bound Worker's production deployment." Workflow 바인딩도 예외. "Worker Previews requires Wrangler 4.135.0 or later."
- **Version URLs** (`wrangler versions upload`): 프로덕션 리소스를 쓴다. "Do not use Version URLs for branch or pull request testing. Use Previews instead."
- 신선도 경고: Worker Previews는 매우 최근(2026년 하반기) 기능.
- wrangler-action 예: `command: preview --name pr-${{ github.event.pull_request.number }}` (4.136.3+) (W-33)
- `wrangler deploy --temporary`(60분 임시 배포, simonw 체험, 2026-06 신기능) — **검증 필요** [커뮤니티] (C-휴9)
- 수요 근거: Neon DB 브랜칭 + 실제 의존성 프리뷰 환경 — "I invested a few days at the start... Once it was set up I almost never need to touch it" (HN) [커뮤니티] (C-휴9)

**wrangler-action [웹] (W-33)**
```yaml
- uses: cloudflare/wrangler-action@v4
  with:
    apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```
- `wranglerVersion`으로 버전 고정, 출력 `deployment-url`, `gitHubToken` 전달 시 GitHub Deployments 생성(`deployments: write`). 토큰은 "Edit Cloudflare Workers" 템플릿에서 시작.

**Gradual deployments·롤백 [웹] (W-35)**
- `wrangler versions upload` → `wrangler versions deploy`로 두 버전 간 트래픽 분할. "You can only create a gradual deployment with the last 100 uploaded versions of your Worker." 한 배포에 최대 2개 버전. `Cloudflare-Workers-Version-Key` 헤더로 "pin a user to a consistent version for the duration of the gradual deployment."
- 롤백: "Resources connected to your Worker will not be changed during a rollback." (바인딩·D1 데이터·시크릿 미복원) / "You can only roll back to the 100 most recently published versions."
- 2026-09-25 Changelog: "Gradual deployments appear as a single rollout with shading that intensifies as traffic shifts to the new version."
- ECS canary와 나란히 비교할 소재. 배경 원리는 P-32(설정 기반 점진 공개).

**D1 마이그레이션 [웹] (W-36)**
- "When running the apply command in a CI/CD environment or another non-interactive command line, the confirmation step will be skipped, but the backup will still be captured."
- "If applying a migration results in an error, this migration will be rolled back, and the previous successful migration will remain applied." 적용 기록은 `d1_migrations` 테이블.
- 함정: wrangler-action 이슈 #221("D1 migrations in CI fail silently") — CI에서 `--remote` 누락 시 로컬 DB에 적용 (커뮤니티 교차 확인 안 됨, 확인 필요)
- 롤백이 데이터를 되돌리지 않으므로 스키마 변경은 확장-축소(expand/contract)로.

**Cloudflare 앞단 + AWS 오리진 [웹] (W-37)**
- 보호 계층: Cloudflare Tunnel("connects your resources to Cloudflare without a publicly routable IP address"), 비밀 헤더/JWT 검증, Authenticated Origin Pulls(mTLS, "Requires Full or Full (strict) encryption modes"), Cloudflare IP 허용 목록("Vulnerable to IP spoofing").
- 주의(2차): IP 허용 목록만으론 "다른 Cloudflare 고객의 트래픽"도 통과(javan.de). AWS 쪽은 Cloudflare CIDR을 customer-managed prefix list로 보안 그룹에 연결하는 방식이 일반적(2차 소스).

### 3.4 공급망 사고 사례

**tj-actions/changed-files (CVE-2025-30066) [웹] (W-16, W-17)**
- "Attackers retroactively modified multiple version tags to reference a malicious commit, exposing CI/CD secrets in workflow logs." / "extracted secrets from the Runner Worker process memory and printed them in GitHub Actions logs, making them publicly accessible."
- v1~v45.0.7 태그 소급 변경, CVSS 3.1 8.6(High), 영향 기간 2025-03-14~15, 패치 v46.0.1. 연쇄로 reviewdog/action-setup@v1(CVE-2025-30154) 침해. Advisory 게시 2025-03-15(최종 갱신 2025-10-22), CISA 2025-03-18.
- **"23,000개 이상 저장소 영향"(사용 저장소 수)과 "최소 218개"(실제 비밀정보 유출 확인, 데일리시큐 2025-03-23)는 다른 지표 — 본문에서 구분해 쓸 것.** 시작점은 봇 PAT 유출(데일리시큐).
- 커뮤니티: "It was obvious from day one that the lack of any kind of lock file in GHA is a giant vulnerability waiting to happen." / "always pin it by the hash...which is best effort only, as git hashes are not a security feature!" — matklad (Lobsters). Coder: "We achieve this by strictly pinning all GitHub Actions to specific commit hashes." [커뮤니티] (C-패턴9)

**s1ngularity: Nx (2025-08) [웹] (W-22)**
- Wiz(2025-08-27 최초, 08-29 갱신): 2025-08-21 추가된 워크플로의 PR 제목 미검증 + `pull_request_target` — "An unsanitized pull-request title combined with pull_request_target permissions enabled command injection" → npm 토큰 탈취 → 악성 Nx 패키지. "over a thousand valid Github tokens, dozens of valid cloud credentials and NPM tokens, and roughly twenty thousand additional files were leaked." / "over 400 users/organizations impacted, and over 5500 repositories"
- 페이로드가 설치된 AI CLI(Claude·Gemini·Q)를 `--dangerously-skip-permissions`/`--yolo`로 호출해 시크릿 수색 — "AI 도구를 무기화한 첫 공급망 공격"으로 보도 (W-22, C-패턴12)
- **날짜 경고: THN(2026-06) 기사가 "March 2026"으로 적었으나 1차·다수 소스는 2025-08. 본문에 THN 날짜를 쓰지 말 것.**

**Shai-Hulud / Mini Shai-Hulud [커뮤니티] (C-패턴9)**
- Shai-Hulud 사후 분석(Trigger.dev) — "Running npm install is not negligence" 격론.
- Mini Shai-Hulud(2026-05~): 감염 액션이 2026-09-16 재활성화(THN 보도), 페이로드가 Claude Code·VS Code 훅을 리포에 커밋하고 Dependabot 위장 워크플로 주입(safedep 보도) — **최신 사건, 날짜·범위 검증 필요.**

**pull_request_target 대응 [웹] (W-21)**
- "GitHub provides a default policy that blocks the `pull_request_target` event in public repositories." 현재 evaluate 모드, **2026-11-02 강제 예정**(프라이빗·내부 저장소 미적용).
- actions/checkout v7(2026-06-18, 지원 버전에 2026-07-16까지 백포트): "refuses to fetch fork pull request code in pull_request_target and workflow_run workflows"(THN). 우회는 `allow-unsafe-pr-checkout: true`, 사용 조건 "the checked-out code is only ever inspected as data and never executed."
- PostHog(2025-11)·TanStack(2026-05) 사례는 THN 단독 출처 — **교차 확인 필요.**

### 3.5 AI 코딩 도구와 CI/CD

**Claude Code GitHub Actions [웹] (W-38, W-39)**
- `/install-github-app`으로 설정. `prompt` 없으면 `@claude` 멘션(interactive), 있으면 automation.
- "on issue and pull request events, the triggering user must have write access to the repository."
- "the Claude Code GitHub Action rejects a bot actor unless you list it in `allowed_bots`, which keeps bots from triggering Claude in a loop."
- 워크로드 아이덴티티 페더레이션: "...exchanges the workflow's GitHub OpenID Connect (OIDC) token for Claude API access through a Claude Console service account." Bedrock/Vertex/Foundry도 OIDC.
- "Create a `CLAUDE.md` file in your repository root to define code style guidelines, review criteria, project-specific rules, and preferred patterns."
- "GitHub doesn't trigger workflows on commits made with the default `GITHUB_TOKEN`."
- 비용: "Set `--max-turns` in `claude_args` to limit iterations" / "Use GitHub's concurrency controls to limit parallel runs"
- "On public repositories, GitHub withholds secrets from runs triggered by fork pull requests, so the review runs only on pull requests from branches in the same repository."
- 문서 내 표기: Claude Code v2.1.229 이후 리뷰가 PR에 게시.
- Security 문서: 숨은 마크다운 인젝션 경고 — "The action sanitizes content by stripping HTML comments, invisible characters, markdown image alt text, hidden HTML attributes, and HTML entities, but new bypass techniques may emerge." `allowed_non_write_users`는 "RISKY". "**Do not use a personal access token** — a static token does not rotate between runs and could be partially or fully recovered over time via prompt injection." "Full output is **automatically enabled** when GitHub Actions debug mode is active (when `ACTIONS_STEP_DEBUG` secret is set to `true`)." "In its default configuration, **Claude does not create pull requests automatically**"

**openai/codex-action [웹] (W-40)**
- 인젝션 벡터: PR 제목·본문(숨은 HTML 주석), 커밋 메시지, **AGENTS.md 같은 저장소 지시 파일**, 스크린샷.
- GitHub-hosted 러너의 비밀번호 없는 sudo 때문에 읽기 전용 샌드박스만으론 API 키가 procfs로 노출 가능 — "Be sure to use either `drop-sudo` or `unprivileged-user` to ensure it stays secret!"
- "Particularly if you run Codex with loose permissions, there are no guarantees what the state of the host is when the `openai/codex-action` completes." → 액션은 마지막 단계, 결과 게시는 별도 job.
- "Permission profiles constrain commands that Codex runs; they do not replace the action's `safety-strategy`."

**Copilot cloud agent (구 coding agent) [웹] (W-42, W-2)**
- 이슈 할당 → Actions 기반 환경에서 드래프트 PR. 쓰기 권한자만 할당, `copilot/` 브랜치에만 푸시, 방화벽으로 인터넷 제한.
- "By default, workflows are not triggered until Copilot cloud agent's code is reviewed and a user with write access to the repository clicks the **Approve and run workflows** button."
- "Copilot cloud agent cannot mark its pull requests as 'Ready for review' and cannot approve or merge a pull request."
- "Copilot cloud agent's commits are authored by Copilot, with the developer who assigned the issue or requested the change to the pull request marked as the co-author."
- 2025-11: "You can now use GitHub Copilot coding agent without turning on GitHub Actions" (W-2)
- 조직 방화벽 설정 2026-04-03 changelog. self-hosted 러너에서 돌리려면 방화벽을 꺼야 한다는 2차 보도(bex.co, 2026-07-28) — **교차 확인 필요.**

**AI 리뷰 도구 [웹]**
- Copilot code review 에이전트 구조 GA(2026-03-05): "...generally available for all users with Copilot Pro, Copilot Pro+, Copilot Business, and Copilot Enterprise." "60 million Copilot code reviews and counting". self-hosted 러너 조직은 1회 설정 필요 (W-43)
- Cursor Bugbot: `.cursor/BUGBOT.md` 계층 규칙("always includes the root `.cursor/BUGBOT.md` file and any additional files found while traversing upward from changed files."), Autofix는 Cloud Agent가 푸시. **함정:** "requiring the status alone does not block merges on findings because findings default to `neutral`." → 막으려면 fail-on-unresolved (W-44)
- CodeRabbit 공식 문서는 미수집.

**한국 AI 리뷰 도입 사례 [웹]**
- kt cloud(2026-08-20): GitHub Actions 대신 사내 VM poller + Claude Code, `.claude/architecture/architecture-rules.json` 규칙 기반. "리뷰 기준을 명확하게 정의하는 것" / "모든 PR이 동일한 기준으로 검증되기 때문에 리뷰어에 따른 품질 편차가 사라진다" / "시니어 리뷰어에게 집중되던 부담이 줄어든다" (W-47)
- 하이퍼리즘(2025-10-27): 코드 유출 우려로 SaaS 대신 Claude Agent SDK 자체 구축. 1단계 공격적 탐지 → 2단계 Evidence·Mitigation 수집, "57건 중 32건을 오탐으로 분류". "지금 방식은 에이전트라기 보다는 워크플로우에 가깝습니다" (W-48)
- W컨셉 Cursor 자동 리뷰 적용기, velog 1인 개발자 CodeRabbit 도입기("도입이 쉬워서 5분만에 적용할 수 있었습니다", "또 한편의 시가 나왔습니다 ㅋㅋㅋ") [커뮤니티] (C-패턴10)

**AI 생산성·품질 실증 [논문]** — 한 수치만 인용하면 오해를 낳는다(P 교차관찰 2)
- Copilot 통제 실험: 55.8% 빨리 완료(단일 그린필드 과제, GitHub 소속 저자 포함) — 2023 [프리프린트] (P-41)
- METR RCT: 숙련 OSS 개발자 16명, 과제 246개. "Surprisingly, we find that allowing AI actually increases completion time by 19%--AI tooling slowed developers down." 사전 24% 단축 예상, 사후에도 20% 단축 믿음 — 2025 [프리프린트] (P-42)
- Cursor 도입 DiD: 속도는 크게 오르나 일시적, 정적 분석 경고·복잡도 지속 증가, 누적 복잡도가 이후 속도를 떨어뜨림 — He et al., MSR 2026. **"첫 달 추가 라인 3~5배, 복잡도 약 41%·경고 약 30% 증가, 도입 806 vs 대조 1,380 저장소"는 web 검색 요약상 수치 — 본문 인용 전 논문 원문 대조 필요(미확인)** (P-43)
- 엔터프라이즈 2배 목표: 개발자 802명·PR 196,212건(2024-01~2026-04), 1인당 처리량 2026-04에 기준선 대비 2.09배. "per-reviewer load roughly doubled and automated review overtook human review, while merge and revert rates held steady." — 2026 [프리프린트] (P-44)
- 보안: Copilot 89개 시나리오 1,689개 프로그램 중 약 40% 취약 — IEEE S&P 2022 (2021 초기 Copilot 기준, 최신 모델 일반화 금지 🕒) (P-45). "Participants with access to an AI assistant were also more likely to believe they wrote secure code" — CCS 2023 (P-46)
- 자동 리뷰 실무: Beko 22개 저장소 Qodo PR-Agent(GPT-4 Turbo), 자동 코멘트 73.8% 해결 처리, PR 종료 시간 평균 5시간 52분 → 8시간 20분 증가 — ICSE 2025 SEIP (수치는 web 검색 요약 기준, 초록 재확인 권장) (P-47)

**에이전트 PR 실증 [논문]**
- AIDev 데이터셋: Codex·Devin·Copilot·Cursor·Claude Code 5개 에이전트 PR 45.6만여 건(6.1만 저장소, 4.7만 개발자), 에이전트 PR은 빠르지만 수락률 낮음 [프리프린트] (P-48)
- Claude Code PR 567개(157 프로젝트): 83.8% 병합, 그중 54.9%는 수정 없이 병합 [프리프린트] (P-49)
- 실패 PR 33k: "Not-merged PRs tend to involve larger code changes, touch more files, and often do not pass the project's CI/CD pipeline validation." 문서·CI·빌드 업데이트 과제 병합률 최고 — MSR 2026. **에이전트별 병합률(Codex 82.59% 등)은 초록에 없음 → 미확인** (P-50)
- 과제 유형이 지배 요인: 문서 82.1% vs 신기능 66.1%, 16%p 격차 — MSR 2026 Mining Challenge. 에이전트 간 순위는 시점 의존 🕒 (P-51)
- 보안 PR 1,293개(약 4%), 병합률 낮고 리뷰 김 — IST minor revision(게재 미확정) (P-52)
- 조기 채택: 2,361개 저장소·에이전트 PR 25,264건, 중앙값 저장소는 3개월에 1~2건, "한 명의 사람이 감독" 모델 지배적 — KDD 2026 Workshop (P-53)
- 워크플로 진화 연구는 LLM 도구 효과의 결정적 증거 없음 (P-9)

**AI 에이전트 워크플로 공격 [논문/웹/커뮤니티]**
- 간접 프롬프트 인젝션 원전: "LLM-Integrated Applications blur the line between data and instructions" — AISec '23 [논문] (P-54)
- Comment and Control(JAW): GitHub 워크플로 4,714개·n8n 템플릿 8개 탈취, Claude Code·Gemini CLI·Qwen CLI·Cursor CLI 공식 액션 포함 15개 액션, 책임 공개 — "An adversary may control and craft certain inputs, such as GitHub issue comments, to manipulate the LLM agent for unwanted actions, such as credential exfiltration and arbitrary command execution." — 2026 [프리프린트] (P-55)
- PromptPwnd(Aikido, 2025-12-04, 2026-03-17 갱신): "Untrusted user input → injected into prompts → AI agent executes privileged tools → secrets leaked or workflows manipulated." Gemini CLI·Claude Code Actions·Codex Actions·GitHub AI Inference 대상, 최소 5개 포춘 500 기업 영향. 권고: 도구 제한, 입력 정제, "Treat AI-generated output as untrusted code requiring validation" [웹, 벤더] (W-41)
  ```yaml
  ISSUE_TITLE: '${{ github.event.issue.title }}'
  ISSUE_BODY: '${{ github.event.issue.body }}'
  ```
- Clinejection(2026-02): 이슈 제목 인젝션 → claude-code-action 트리아지 워크플로 → 캐시 포이즈닝 → 릴리스 토큰 탈취 → 약 4,000대 개발자 머신 감염 보도(**피해 규모 검증 필요**). "configured the claude-code action with allowed_non_write_users: "*", meaning anyone with a GitHub account can trigger it... Has everyone lost their minds?" — yread. 워크플로는 `contents: read`였지만 캐시 경로로 뚫림(Ukv) [커뮤니티] (C-패턴12). CSA 연구노트 존재(C-휴7).
- CodeRabbit RCE(2025-08 공개): "write access on 1M repos" 주장, 회사 측 "this RCE was reported and fixed in January... no customer data was affected" [커뮤니티] (C-패턴12)
- 구조적 통찰: ARGUS(P-15)가 본 "신뢰할 수 없는 입력 → 실행" 문제의 새 판. 스크립트 인젝션(W-15)과 같은 뿌리.

---

## 4. 논쟁점·상충 관점

### 4.1 관점이 갈리는 주제 (병기)

**A. GitHub Actions를 계속 쓸 것인가** [커뮤니티] (C-논쟁A, C-패턴1·4)
- 관점 A: GHA는 떠나야 한다 — "CI의 Internet Explorer"(Ian Duncan, 2026-02-05), "fighting the expression syntax and the permissions model and the marketplace and the log viewer that crashes your browser", Buildkite·Concourse 호평. 신뢰성 불만: "Sitting at 91% platform uptime over the last 90 days"(**비공식 집계 인용, 검증 필요**), "lost count of how many incidents they've had in 2026 alone". 원인 추측(Azure 이전, Copilot 부하)은 **근거 약함 — "개발자들이 이렇게 느꼈다"로만 사용.**
- 관점 B: 도구가 아니라 사용법 문제 — "most CIs are fine if you just use them to bootstrap into your build system"(sebastien), 저장소 옆 통합성은 대체 불가, "GitHub의 대안은 있지만 대체재는 없다"(GeekNews 요약), 카카오엔터프라이즈 사례.
- 저술 활용: 플랫폼 장애 시 수동 배포 런북·대체 경로.

**B. 워크플로 로직을 스크립트로 뺄 것인가** [커뮤니티] (C-휴1)
- 관점 A: 뺀다(2.1).
- 관점 B: "How do you orchrestate a full CI/CD pipeline where you need state? You just move that complex logic to another monolithic script with its own problems?" — mlrtime. 셸 vs 스크립팅 언어 논쟁("if you need anything more than shell that starts to become a smell").
- 로컬 재현 도구 `act`: "covered 80% of use cases"(c0wb0yc0d3r), 복잡하면 함정(figmert), services 컨테이너 네트워킹 실패 nektos/act#247 등 vs "for my use case that doesn't matter and it's super nice to have"(Mattwmaster58). 디버깅: action-tmate 종료 예정 → upterm/action-upterm (C-패턴2)

**C. SHA 고정은 충분한가, 과한가** [커뮤니티+논문] (C-논쟁C)
- 관점 A: 필수 — 태그는 움직인다(P-18, W-16, Coder, rmunn, matklad).
- 관점 B: 불충분 — 전이 의존("Even SHA pinning only lets you go one hop." — koolba; "GitHub Actions doesn't have a lock file, so your repo is still prone to transitive attacks" — maxloh), 해시 bump 자동 머지하면 무의미(alerque).
- 관점 C: 비용 과다 — "lose vulnerability alerts, increase maintenance overhead", Immutable Releases 보급 시 가치 0(mmarian).
- 관점 D: 코드 감사보다 권한 축소가 본질(cyrnel; `CAP_SYS_PTRACE` 등 불필요 권한 제거).
- 미래 변수: GitHub 2026 보안 로드맵의 `dependencies:` 잠금("locks all direct and transitive dependencies with the commits SHA") — **로드맵일 뿐**(4.3).

**D. CDK vs Terraform (vs OpenTofu/Pulumi/SAM)** [커뮤니티] (C-논쟁B)
- 관점 A Terraform: "the tooling around it is just much better for things like drift detection, showing planned changes, pipelines"(superdeeda, 2023 스레드), "provides organisational memory... And tfstate is hard"(sshine)
- 관점 B CDK/CFN: "CDK/CFN seems to work more reliably 'at scale' for commonly used stacks due to low drama rollbacks etc."(xyzzy123), "CDK is great if you are only using AWS but Documentation sucks."(mr_o47)
- 관점 C 둘 다 아님: SAM·vanilla CloudFormation(mlhpdx), Pulumi 호평 vs "Stay far, far away."(packetlost), OpenTofu("pretty seamless", BSL 전환 이후 선택지)
- 맥락: Terraform 불만은 대개 "someone managing inherently ephemeral infrastructure"의 시각(danw1979) — 플랫폼 팀 vs 앱 팀.
- **CDKTF 종료:** HN "The future of Terraform CDK"(2025-12) 기반 — **정확한 상태는 1차 소스 확인 필요.**

**E. AI 리뷰 봇은 가치가 있나** [커뮤니티+논문]
- 관점 A 있다: "they do find critical bugs (from my retrospective analysis, maybe 80% of the time)"(zmmmmm), "Bugbot is incredible"(greymalik), "It's almost always right."(jjmarr), 1인 개발자·kt cloud·하이퍼리즘 사례, 자동 코멘트 73.8% 해결(P-47)
- 관점 B 소음이 가치를 잡아먹는다: "the signal to noise ratio is poor. It's really hard to get it not to tell you 20 highly speculative reasons..."(zmmmmm), "Copilot has terrible signal noise"(greymalik — 제품 평가는 사람마다 정반대), diff만 보는 컨텍스트(storystarling), 리뷰의 목적은 지식 전파(marginalia_nu), PR 종료 시간 증가(P-47), 하이퍼리즘 57건 중 32건 오탐(W-48)
- 관점 C 이해상충·공격면: "Coderabbit is an LLM code review company so their incentives are the opposite."(CodeRabbit "AI 코드는 버그 1.7배" 보고서에 대해), CodeRabbit RCE, 리뷰 봇 자체가 공격면
- 실무 합의점(휴리스틱 5): AI 리뷰는 사람 리뷰의 앞단 필터 — "give it a number of things to list in order of severity and ... tell it to grade how serious" / "the top 3 or 4 are likely good ones to look deeper into."

**F. AI 사용을 PR에 밝혀야 하나** [커뮤니티] (C-논쟁E)
- 관점 A 밝히거나 금지: "people aren't transparent about when they use AI"(nharada), ardour.org "we've banned any and all LLM-generated code"
- 관점 B 코드는 코드: "Code is code: it speaks for itself."(kstrauser), 밝히면 낙인찍혀 아무도 안 밝힌다(Workaccount2)
- 관점 C 작성자 책임 강화: 변경을 이해하고 손으로 요약(strogonoff), "play with the code, try to break it, write more tests yourself"(lawn)

**G. self-hosted 러너: 절감인가 부담인가** [커뮤니티+웹] (C-논쟁F)
- 관점 A: "Cost savings are insane"(zackify, 베어메탈 LXC), 월 고정비(arusahni), 버즈빌·채널톡·다나와 사례
- 관점 B: 운영·보안 부담(퍼블릭 리포 금지 W-15, 캐시 경로 문제), GitHub가 언제든 과금할 수 있는 플랫폼 리스크(W-8 연기 상태)
- 과금 소동 반응: "anti-competitive"(brtkwr), "We already pay for the control plane"(bhswilson), "unacceptable for nonprofits"(macintoshplus) vs "I honestly don't have any issue paying the self-hosted runner fee."(brightball)

**H. Cloudflare를 AWS 앞에 둘 것인가** [커뮤니티+웹] (C-논쟁G)
- 관점 A: 흔한 조합("cloudflare DNS in front of AWS infra")
- 관점 B: 비용·결합도 — "AWS is still not part of the Bandwidth Alliance... you can still end up paying a lot more in egress fees"(sagiba, **검증 필요**), 장애 전파(2025-11-18 사후분석)
- 관점 C: Route 53 유지 시 Workers 커스텀 도메인 제약(merek)

**I. AI의 생산성 효과 (측정 방식에 따라 부호가 바뀜)** [논문]
- +55.8%(P-41) / −19%(P-42) / 속도↑·복잡도 지속↑(P-43) / 처리량 2.09배·되돌림률 유지(P-44). 과제·숙련도·기간 차이. "체감 ≠ 측정" → DORA 지표로 재야 한다.
- DORA 2024 vs 2025: 처리량 관계 음→양, 안정성은 계속 음. 2025는 방법론·지표 구성이 바뀌었을 수 있어 직접 비교 시 주의(P 교차관찰 4).

### 4.2 AI PR 홍수와 리뷰 피로 (현상 기술)
- "사람이 코드를 읽고 검토할 수 있는 속도보다, 코드가 만들어지는 속도가 빨라진 것이 더 근본적인 변화" / "AI 리뷰어를 붙이는 것만으로 좋은 리뷰 시스템이 만들어지지 않음" — GeekNews [커뮤니티] (C-패턴11)
- AI 코드는 자신감 있고 매끈해 오히려 놓치기 쉽다, 존재하지 않는 API 호출을 자주 잡는다(koh3276). Lobsters 요약: 400줄 PR 상한, PR에 의도·근거·기각 대안 명시 [커뮤니티]
- "I did not feel that I knew the codebase enough to be able to actually assess the correctness of the change"(danpalmer) [커뮤니티]
- `--author` 플래그로 AI 봇 스팸 차단 사례와 보안 지적("저장소 기여자는 fork PR 실행의 승인 요구를 우회하는 등 더 높은 권한을 갖게 되므로...") [커뮤니티]
- 오픈소스 측 보도(Jazzband 해산, curl 버그바운티 중단, The New Stack) — **사실관계 검증 필요.** PR당 리뷰 30분+ "보도상" 수치 — 확인 필요.
- **"AI 도입률이 높은 팀은 PR을 98% 더 많이 머지하지만 리뷰 시간은 91% 늘어났다"** — Flowkater.io가 latent.space를 출처로 적었으나 원 조사는 Faros AI 보고서(2025)로 알려짐 — **본문 인용 시 원 출처 확인 필수** [웹, 2차 인용] (W-49). 400줄 결함 감지율은 SmartBear/Cisco 연구(고전 레퍼런스, 원천 미확인).
- 실증 뒷받침: 리뷰어 1인당 부하 약 2배(P-44).

### 4.3 사실 충돌·신선도 함정 (fact-checker 대조 기준)

| # | 항목 | 충돌 내용 | 채택 표기 |
|---|---|---|---|
| 1 | ECS blue/green 트래픽 전환 | AWS 블로그(2025-09-16) "As of this writing, ECS blue/green only supports all-at-once." vs What's New(2025-10-30) linear/canary 추가, 2026-02 NLB 확장 | 2026-09 기준 linear/canary 지원이 사실. "all-at-once만"은 구버전 — 쓰지 말 것 (W-26, W-27) |
| 2 | App Runner | 브리프에 배포 대상으로 나열 vs 2026-04-30부터 신규 고객 불가 | 신규 독자에겐 ECS Express Mode로 대체 안내 (W-28) |
| 3 | Nx s1ngularity 날짜 | THN(2026-06) "March 2026" vs Wiz 등 다수 2025-08(워크플로 추가 2025-08-21, Wiz 게시 2025-08-27) | 2025-08. THN 날짜 쓰지 말 것 (W-21, W-22) |
| 4 | tj-actions 피해 규모 | 23,000개(사용 저장소) vs 218개(유출 확인) | 서로 다른 지표 — 구분 표기 (W-16, W-17) |
| 5 | self-hosted 러너 과금 | 1차 "postponing"(연기) vs 2차 "24~48시간 내 철회"(samexpert, "missed the mark") vs 한국 블로그 youngju.dev(2026-03) "2026년 3월부터 과금 시작" vs The Register·bex.co(2026-07) "연기/철회" | "연기"로 쓰고 재개 여부는 불확실. "폐기 확정"·"시행 중" 모두 쓰지 말 것 (W-8, C-패턴5) |
| 6 | pull_request_target 기본 차단 | 현재 evaluate 모드, 2026-11-02 강제 예정 | 오늘(2026-09-26) 기준 "예정". 출간 시점에 따라 "시행"으로 바뀌는 항목 — 신선도 경고 필수 (W-21) |
| 7 | GitHub Actions 2026 보안 로드맵 | 2026-03-26 발표(03-30 갱신), 잠금·정책·scoped secrets 프리뷰 3~6개월·GA 6개월, egress 방화벽 프리뷰 6~9개월 | 2026-09 현재 출시 여부 미확인 — "로드맵"으로만 표기 (W-20) |
| 8 | Cloudflare Pages 상태 | 2차 블로그 "deprecated" vs 공식 "merging"/마이그레이션 권장 | "폐지"라고 단정하지 말 것 (W-31) |
| 9 | Cloudflare 프리뷰 용어 | Preview URLs(2025-07, `--preview-alias`, 4.21.0+) / Worker Previews(`wrangler preview`, 4.135.0+) / Version URLs(프로덕션 리소스) | 세 용어 구분 표기, PR 테스트엔 Worker Previews (W-32) |
| 10 | Copilot 에이전트 명칭 | 2025-09 GA "coding agent" vs 2026 문서 "cloud agent" | 본문 용어 표기 결정 필요(예: "Copilot cloud agent(구 coding agent)") (W-42) |
| 11 | Cloudflare의 GitHub OIDC 수용 | 공식 문서 미발견 | 미지원 추정 — 확인 필요. 단정 금지 (W-33) |
| 12 | OIDC `sub` 클레임 변경 | decryptiondigest 블로그 "2026년 7월 이후 immutable subject claim 옵트인 리포는 기존 이름 기반 `sub` 조건으로 실패" | GitHub 공식 changelog 미확인 — 확인 필요, 본문 단정 금지 (C-패턴6) |
| 13 | CDKTF 종료 | HN 스레드(2025-12) 기반 | 정확한 상태 1차 소스 확인 필요 (C-논쟁B) |
| 14 | 미확인 통계 | "98% 더 많은 PR / 91% 긴 리뷰"(원 출처 Faros AI 추정), Cursor 논문 "3~5배·41%·30%·806 vs 1,380", "SHA pinning 6.3%", 에이전트별 병합률(Codex 82.59%), Hilton "릴리스 2배", DORA 2024 "25% 증가" 조건·"39,000명", GHA 가용성 "91%", Clinejection "~4,000대" | 모두 원문 대조 전 본문 사용 금지 (W-49, P-43, P-11, P-50, P-2, P-39, C-패턴4·12) |
| 15 | Mini Shai-Hulud 재활성화(2026-09-16) | THN·safedep 보도 | 최신 사건 — 날짜·범위 검증 필요 (C-패턴9) |
| 16 | PostHog(2025-11)·TanStack(2026-05) pwn request 사례 | THN 단독 | 교차 확인 필요 (W-21) |
| 17 | `wrangler deploy --temporary` | simonw 체험(2026-06) | 공식 문서 미대조 — 검증 필요 (C-휴9) |
| 18 | Kenton Varda "Pages 기능을 Workers로" 발언 | 2차 인용(cogley.jp) | 원문 확인 필요 (C-패턴8) |
| 19 | Copilot cloud agent + self-hosted 러너 방화벽 | 2차 보도(bex.co, 2026-07-28) | 교차 확인 필요 (W-42) |
| 20 | Dependabot 쿨다운의 github-actions 계산 방식 | dependabot-core #13078·#13691 이슈 보고 | 커뮤니티 교차 확인 안 됨 (W-24) |
| 21 | D1 `--remote` 누락 함정 | wrangler-action #221 | 확인 필요 (W-36) |
| 22 | ECS 단일 태스크 실패 감지 약 100분 | containers-roadmap #1488 | 검증 필요 (C-패턴7) |
| 23 | 호스티드 러너 인하율 | 1차 "최대 39%" (W-8) vs 커뮤니티 "보도상 최대 39%, 확인 필요" | 1차 소스 확인됨 — "최대 39%" 채택 (W-8) |
| 24 | Workers 경로 필터 + 롤백 | 레몬베이스: path-filter가 롤백 시 문제 | 사례 인용만, 일반화 주의 (W-11) |

---

## 5. 실무 적용 팁

### 5.1 파이프라인 설계
- 워크플로는 checkout + 로컬에서 도는 스크립트 호출로(2.1). `act`는 80%짜리, 복잡하면 스크립트 쪽으로.
- 배포 concurrency는 취소하지 말고 줄 세우기(`cancel-in-progress: false`, `queue: max` — 100개 FIFO), PR 빌드는 `cancel-in-progress` (W-3)
- 머지 큐를 쓰면 required check 워크플로에 `merge_group` 트리거 필수 (W-6) — AI가 PR을 대량 생성할 때 main 보호
- 모노레포: path 필터 + 프로젝트별 yml(F-Lab, W-12). 단 "path filters alone are not enough. You want an affected graph (packages and tests), fail-closed when the graph is unsure, and a canary on main that still runs the full suite." — thedefaultman(HN, 2026-09-21, 단일 발언) [커뮤니티] (C-휴8). 스킵된 체크가 required일 때의 충돌 설명 필요(W-12 관련 섹션). path 필터는 롤백 시 함정(W-11).
- 재사용 워크플로로 조직 표준화 — 단 "Template을 수정하면 많은 Pipeline에 한 번에 적용되기 때문에 실수를 했을 때 영향이 굉장히 큽니다." 일부 파이프라인에서 먼저 검증, 파이프라인 변경에 CODEOWNERS (W-50)
- 캐싱: 효과는 크지만(P-30) 유지보수 비용이 있고(P-13), 10GB 한도·eviction(W-7, C-패턴3)을 고려한 키 설계.
- 비용: arm64 러너가 x64보다 분당 저렴($0.005 vs $0.006) + Graviton 네이티브 빌드(W-8, W-9). 비활성 저장소 스케줄 워크플로 중단(P-7). 스케줄은 `timezone: "Asia/Seoul"`(W-4).
- 플레이키 테스트: 재시도로 덮기 전에 격리. "A 95% confidence that a passing test case is not flaky on average would require 170 reruns."(P-26, PyPI 22,352 프로젝트·876,186 테스트, 플레이키 7,571개 중 59% 순서 의존·28% 인프라) / 개발자 59%가 월·주·일 단위로 겪음(P-25) / 원전 Luo 2014(P-24, 51개 프로젝트 201 커밋, 원인별 비율은 미확인). 재시도는 빌드를 늘리고 통과를 보장하지 않음(P-29).
- 워크플로 코드 리뷰 체크리스트 근거: 확정 워크플로 스멜 7개(후보 22개, 목록은 전문 미확인)(P-10), CodeQL 워크플로 분석(W-23).

### 5.2 보안 기본기 체크리스트
1. `permissions:` 블록 명시, `GITHUB_TOKEN` 기본 읽기 전용 (W-15, P-12, P-14)
2. `${{ github.event.* }}`를 `run:`에 직접 넣지 말고 env로 (W-15, P-15)
3. 서드파티 액션 전체 SHA 고정 + 조직 정책으로 강제 + Renovate/Dependabot으로 갱신하되 자동 머지 금지 (W-18, C-휴2)
4. 클라우드 인증은 OIDC, `sub`를 environment/branch로 좁힘 (W-13). OIDC 실패 1순위 원인 — `sub`/`aud` 글자 단위 불일치, `permissions: id-token: write` 누락. 디버깅은 actions-oidc-debugger로 디코딩된 JWT 비교 [커뮤니티] (C-패턴6)
5. build/test 잡엔 시크릿 0, 배포 시크릿은 main·environment에만 (C-휴3)
6. 퍼블릭 저장소엔 self-hosted 러너 금지 (W-15)
7. 포크 PR은 `pull_request`로, `pull_request_target`은 피하기, checkout v7의 기본 거부 유지 (W-21)
8. 워크플로 파일은 CODEOWNERS (W-15, W-50)
9. 스캐너는 여러 관점으로(하나로 안심 금지) (P-17). LLM 감사는 전문가 대체 불가(κ=0.28) (P-12)
10. 산출물 attestation (`actions/attest`) + 검증 (W-25)
11. step-security/harden-runner(v2.21.1)로 egress 통제 (W-0; 기능 상세는 원천에 없음)

### 5.3 배포 대상별 요령
- **ECS:** 네이티브 blue/green·linear·canary + CloudWatch 알람 롤백(W-26). 배포 성공 판정은 "내 리비전이 active인가"(C-휴4). 커밋 SHA 이미지 태그.
- **신규 컨테이너 앱:** App Runner 대신 ECS Express Mode (W-28)
- **Lambda:** `aws-actions/aws-lambda-deploy`로 함수 코드, 인프라 전체는 SAM/CDK (W-29). (Lambda 배포 함정 커뮤니티 원문은 미확보)
- **IaC:** plan-on-PR, apply-on-merge. 큰 plan은 아티팩트/Step Summary로 (W-30)
- **Workers:** wrangler 버전 고정(`wranglerVersion`), PR 프리뷰는 Worker Previews(Version URL 금지), 점진 배포는 versions upload/deploy, 롤백은 데이터를 되돌리지 않으므로 D1은 expand/contract (W-32, W-33, W-35, W-36)
- **Cloudflare 토큰:** 계정 소유 토큰 + Specified Workers 스코프 + Editor(삭제 권한 없음) (W-34)
- **Cloudflare 앞단 + AWS 오리진:** Tunnel 또는 AOP(mTLS). IP 허용 목록 단독은 취약 (W-37)
- **공식 액션 의존 리스크:** `cloudflare/pages-action` 저장소 삭제 사례 — wrangler 직접 호출이 대안 (C-패턴8)

### 5.4 AI 코딩 도구를 쓰는 팀
- **트리거 제한:** 쓰기 권한 사용자만(claude-code-action·codex-action 기본값), `allowed_non_write_users: "*"` 금지("RISKY"), 봇 루프는 `allowed_bots`로 명시 (W-38, W-39, W-40, C-휴7)
- **자격증명:** PAT 금지, OIDC 워크로드 아이덴티티 페더레이션 (W-38, W-39)
- **도구 최소화:** Bash/WebFetch 등 도구 제한, 이슈/PR 쓰기 금지, 트리아지 워크플로와 릴리스 워크플로 간 캐시 키 분리 — 구체 설정값은 공식 문서로 검증 필요 (C-휴7, W-41)
- **격리:** codex-action `drop-sudo`/`unprivileged-user`, 에이전트 job과 게시 job 분리, 액션은 마지막 단계 (W-40). 로컬 에이전트는 컨테이너 안에서 git 자격증명 없이 — "can see git history etc and do local git ops ... but not actually push anything without a review."(adzicg) (C-휴6)
- **디버그 모드 주의:** `ACTIONS_STEP_DEBUG=true`면 full output 자동 활성 (W-39)
- **지시 파일은 가드레일이 아니다:** CLAUDE.md·AGENTS.md는 컨텍스트 삽입일 뿐, 그리고 AGENTS.md 자체가 인젝션 벡터가 될 수 있다(역설) (C-휴6, W-40). 빌드·테스트 명령을 AGENTS.md에 적는 것은 CI 정의와 같은 일 (W-45)
- **사람 승인 지점 유지:** Copilot cloud agent는 "Approve and run workflows" 전 CI 미실행, 스스로 머지 불가 — branch protection·required checks가 그대로 적용 (W-42). Claude는 기본 설정에서 PR 자동 생성 안 함 (W-39)
- **`GITHUB_TOKEN` 커밋은 CI를 트리거하지 않는다** — 에이전트 커밋 후 CI를 돌리려면 GitHub App 토큰 등 필요 (W-38)
- **AI 리뷰를 required check로 걸 때:** Bugbot은 기본 `neutral` — fail-on-unresolved 설정 필요 (W-44)
- **AI 리뷰 노이즈 관리:** 심각도 순 상위 N개만 사람에게(C-휴5), 규칙 파일로 기준 명문화(kt cloud, `.cursor/BUGBOT.md`), Evidence/Mitigation 2단 판정(하이퍼리즘), diff가 아니라 스펙·의도 리뷰, 스위스 치즈 모델(W-49)
- **에이전트에게 맡길 일:** 과제 유형이 병합률을 좌우(문서 82.1% vs 신기능 66.1%, P-51), 작은 변경 + 초록 CI(P-50)
- **품질 게이트:** 정적 분석·복잡도 게이트(P-43), SAST·시크릿 스캔을 CI로 강제(P-46 과신 근거)
- **비용 통제:** `--max-turns`, concurrency로 병렬 실행 제한 (W-38)
- **측정:** 체감이 아니라 DORA 5지표로(P-42, W-46)

---

## 6. 참고문헌

### 6.1 웹 — 공식 문서·체인지로그 (GitHub)
- GitHub. GitHub Actions: Early September 2026 updates. https://github.blog/changelog/2026-09-03-github-actions-early-september-2026-updates/, 2026-09-03.
- GitHub. New releases for GitHub Actions – November 2025. https://github.blog/changelog/2025-11-06-new-releases-for-github-actions-november-2025/, 2025-11-06.
- GitHub. GitHub Actions concurrency groups now allow larger queues. https://github.blog/changelog/2026-05-07-github-actions-concurrency-groups-now-allow-larger-queues/, 2026-05-07.
- GitHub. GitHub Actions: Late March 2026 updates. https://github.blog/changelog/2026-03-19-github-actions-late-march-2026-updates/, 2026-03-19.
- GitHub. GitHub Actions: Early April 2026 updates. https://github.blog/changelog/2026-04-02-github-actions-early-april-2026-updates/, 2026-04-02.
- GitHub. GitHub Actions: Early February 2026 updates. https://github.blog/changelog/2026-02-05-github-actions-early-february-2026-updates/, 2026-02-05.
- GitHub Docs. Managing a merge queue. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue, 2026-09 조회.
- GitHub. GitHub Actions cache size can now exceed 10 GB per repository. https://github.blog/changelog/2025-11-20-github-actions-cache-size-can-now-exceed-10-gb-per-repository/, 2025-11-20.
- GitHub. 2026 pricing changes for GitHub Actions. https://github.com/resources/insights/2026-pricing-changes-for-github-actions, 2025-12 발표 / 2026-01-01 시행.
- GitHub Docs. Actions runner pricing. https://docs.github.com/en/billing/reference/actions-runner-pricing, 2026-09 조회.
- GitHub. Coming soon: simpler pricing and a better experience for GitHub Actions. https://github.blog/changelog/2025-12-16-coming-soon-simpler-pricing-and-a-better-experience-for-github-actions/, 2025-12-16. (C-패턴5 인용)
- GitHub. arm64 hosted runners for public repositories are now generally available. https://github.blog/changelog/2025-08-07-arm64-hosted-runners-for-public-repositories-are-now-generally-available/, 2025-08-07.
- GitHub. arm64 standard runners are now available in private repositories. https://github.blog/changelog/2026-01-29-arm64-standard-runners-are-now-available-in-private-repositories/, 2026-01-29.
- GitHub Docs. Configuring OpenID Connect in Amazon Web Services. https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services, 2026-09 조회.
- GitHub Docs. Secure use reference. https://docs.github.com/en/actions/reference/security/secure-use, 2026-09 조회.
- GitHub Docs. Securely using pull_request_target. https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target, 2026-09 조회.
- GitHub. GitHub Actions policy now supports blocking and SHA pinning actions. https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/, 2025-08-15.
- GitHub. Immutable releases are now generally available. https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/, 2025-10-28.
- Greg Ose, Stephen Glass. What's coming to our GitHub Actions 2026 security roadmap. https://github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/, 2026-03-26 (2026-03-30 갱신).
- GitHub. GitHub Actions workflow security analysis with CodeQL is now generally available. https://github.blog/changelog/2025-04-22-github-actions-workflow-security-analysis-with-codeql-is-now-generally-available/, 2025-04-22.
- GitHub. Dependabot version updates introduce default package cooldown. https://github.blog/changelog/2026-07-14-dependabot-version-updates-introduce-default-package-cooldown/, 2026-07-14. / Dependabot supports configuration of a minimum package age. https://github.blog/changelog/2025-07-01-dependabot-supports-configuration-of-a-minimum-package-age/, 2025-07-01.
- GitHub Docs. Artifact attestations. https://docs.github.com/en/actions/concepts/security/artifact-attestations ; Using artifact attestations and reusable workflows to achieve SLSA v1 Build Level 3. https://docs.github.com/actions/security-guides/using-artifact-attestations-and-reusable-workflows-to-achieve-slsa-v1-build-level-3 ; actions/attest-build-provenance. https://github.com/actions/attest-build-provenance, 2026-09 조회.
- GitHub Advisory Database. GHSA-mrrh-fwg8-r2c3 (CVE-2025-30066). https://github.com/advisories/ghsa-mrrh-fwg8-r2c3, 2025-03-15 게시 / 2025-10-22 갱신.
- GitHub. Copilot coding agent is now generally available. https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/, 2025-09-25.
- GitHub Docs. Risks and mitigations (Copilot cloud agent). https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations, 2026-09 조회.
- GitHub. Copilot code review now runs on an agentic architecture. https://github.blog/changelog/2026-03-05-copilot-code-review-now-runs-on-an-agentic-architecture/, 2026-03-05.
- GitHub. Copilot coding agent now supports AGENTS.md custom instructions. https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions/, 2025-08-28.

### 6.2 웹 — 공식 문서 (AWS·HashiCorp·Cloudflare·AI 벤더)
- AWS. aws-actions/configure-aws-credentials (README). https://github.com/aws-actions/configure-aws-credentials, v6.3.0 (2026-09-15).
- AWS What's New. Amazon ECS built-in blue/green deployments. https://aws.amazon.com/about-aws/whats-new/2025/07/amazon-ecs-built-in-blue-green-deployments/, 2025-07-17.
- AWS What's New. Amazon ECS built-in linear and canary deployments. https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-ecs-built-in-linear-canary-deployments, 2025-10-30.
- AWS What's New. Amazon ECS NLB linear/canary deployments. https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-ecs-nlb-linear-canary-deployments/, 2026-02.
- Mike Rizzo, Islam Mahgoub, Olly Pomeroy. Migrating from AWS CodeDeploy to Amazon ECS for blue/green deployments. AWS Containers Blog. https://aws.amazon.com/blogs/containers/migrating-from-aws-codedeploy-to-amazon-ecs-for-blue-green-deployments, 2025-09-16.
- AWS. App Runner release notes. https://docs.aws.amazon.com/apprunner/latest/relnotes/relnotes.html, 2026-04-30 시행 공지.
- AWS What's New. Announcing Amazon ECS Express Mode. https://aws.amazon.com/about-aws/whats-new/2025/11/announcing-amazon-ecs-express-mode/, 2025-11. / ECS Express Mode ARM architecture. https://aws.amazon.com/about-aws/whats-new/2026/09/amazon-ecs-express-mode-arm-architecture/, 2026-09.
- AWS. AWS Lambda now supports GitHub Actions. https://aws.amazon.com/about-aws/whats-new/2025/08/aws-lambda-github-actions-function-deployment, 2025-08-07. / aws-actions/aws-lambda-deploy. https://github.com/aws-actions/aws-lambda-deploy / https://docs.aws.amazon.com/lambda/latest/dg/deploying-github-actions.html.
- HashiCorp. Automate Terraform with GitHub Actions. https://developer.hashicorp.com/terraform/tutorials/automation/github-actions ; hashicorp/setup-terraform. https://github.com/hashicorp/setup-terraform, v4.0.1 (2026-05-12).
- Cloudflare Docs. Migrate from Pages to Workers. https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/, 2026-09 조회.
- Cloudflare Docs. Worker Previews / Compare workflows / Previews. https://developers.cloudflare.com/workers/previews/ , https://developers.cloudflare.com/workers/previews/compare-workflows/ , https://developers.cloudflare.com/workers/configuration/previews/, 2026-09 조회.
- Cloudflare. cloudflare/wrangler-action. https://github.com/cloudflare/wrangler-action, v4.1.3 (2026-09-24). / GitHub Actions (CI/CD). https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/.
- Cloudflare Changelog. Grant teammates and agents access to specific Workers. https://developers.cloudflare.com/changelog/post/2026-09-15-granular-worker-permissions/, 2026-09-15. / Create API token. https://developers.cloudflare.com/fundamentals/api/get-started/create-token/.
- Cloudflare Docs. Gradual deployments. https://developers.cloudflare.com/workers/versions-and-deployments/gradual-deployments/ ; Rollbacks. https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/ ; Changelog: Release flows in Workers Metrics. https://developers.cloudflare.com/changelog/post/2026-09-25-release-flows-workers-metrics/, 2026-09-25.
- Cloudflare Docs. D1 commands / Migrations. https://developers.cloudflare.com/workers/wrangler/commands/d1/ , https://developers.cloudflare.com/d1/reference/migrations/, 2026-09 조회.
- Cloudflare Docs. Protect your origin server. https://developers.cloudflare.com/fundamentals/security/protect-your-origin-server/, 2026-09 조회.
- Anthropic. Claude Code GitHub Actions. https://code.claude.com/docs/en/github-actions, 2026-09 조회.
- Anthropic. claude-code-action Security. https://github.com/anthropics/claude-code-action/blob/main/docs/security.md, 2026-09 조회.
- OpenAI. codex-action Security. https://github.com/openai/codex-action/blob/main/docs/security.md, 2026-09 조회.
- Cursor. Bugbot. https://cursor.com/docs/bugbot, 2026-09 조회.
- Linux Foundation. Linux Foundation announces the formation of the Agentic AI Foundation. https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation, 2025-12-09.
- Nathen Harvey, Derek DeBellis. Announcing the 2025 DORA Report. Google Cloud Blog. https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report, 2025-09-24. / DORA metrics. https://dora.dev/guides/dora-metrics/ ; https://dora.dev/insights/dora-metrics-history/.

### 6.3 웹 — 보안 리서치·언론
- CISA. Supply Chain Compromise of Third-Party tj-actions/changed-files (CVE-2025-30066) and reviewdog/action-setup. https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction, 2025-03-18.
- 길민권. [긴급] 깃허브 액션스 공급망 공격 발생…218개 저장소 비밀정보 유출돼. 데일리시큐. https://www.dailysecu.com/news/articleView.html?idxno=164700, 2025-03-23.
- Wiz Research. s1ngularity: supply chain attack. https://www.wiz.io/blog/s1ngularity-supply-chain-attack, 2025-08-27 (2025-08-29 갱신).
- Ravie Lakshmanan. GitHub updates actions/checkout to block... The Hacker News. https://thehackernews.com/2026/06/github-updates-actionscheckout-to-block.html, 2026-06-23. (s1ngularity 날짜 오기 — 날짜 인용 금지)
- Rein Daelman. PromptPwnd: Prompt Injection Vulnerabilities in GitHub Actions Using AI Agents. Aikido. https://www.aikido.dev/blog/promptpwnd-github-actions-ai-agents, 2025-12-04 (2026-03-17 갱신).
- The Hacker News. Malicious Nx packages in s1ngularity. https://thehackernews.com/2025/08/malicious-nx-packages-in-s1ngularity.html, 2025-08. / Nx. s1ngularity postmortem. https://nx.dev/blog/s1ngularity-postmortem. (C-패턴12)
- The Hacker News. Compromised GitHub Actions came back. https://thehackernews.com/2026/09/compromised-github-actions-came-back.html, 2026-09. / SafeDep. Mini Shai-Hulud reinfection. https://safedep.io/mini-shai-hulud-reinfection-github-repositories/. (검증 필요)
- CSA. Research note: Clinejection. https://labs.cloudsecurityalliance.org/research/csa-research-note-clinejection-prompt-injection-cicd-cache-p/. (C-휴7)

### 6.4 웹 — 한국 회사·개인 블로그
- Cade Seo. 쿠버네티스에게 Github Actions 설치에 대해 묻다. 버즈빌 기술블로그. https://tech.buzzvil.com/blog/쿠버네티스에게-github-actions-설치에-대해-묻다/, 2024-01-01.
- 레몬베이스 팀. Github Actions 배포 시간 줄여볼까? https://blog.lemonbase.team/github-actions-배포-시간-줄여볼까-5725b92e36d9 (GeekNews https://news.hada.io/topic?id=16313, 2024-08-14).
- Tino. 모노레포에서 Github Actions 현명하게 사용하기. F-Lab. https://f-lab.kr/blog/wise-use-of-github-actions-in-monorepo, 2023-08-07.
- 강민호. [AI활용] Claude 실무편 - kt cloud VM에서 PR 리뷰 자동화하기. kt cloud 기술블로그. https://tech.ktcloud.com/entry/2026-08-ktcloud-claude-pr-review-automation, 2026-08-20.
- Cheolwan Park. PR 리뷰 에이전트 개발기 feat. Claude Agent SDK. 하이퍼리즘 기술블로그. https://tech.hyperithm.com/review-agent, 2025-10-27.
- Tony Cho. AI 시대에 코드 리뷰, 어떻게 해야할까? Flowkater.io. https://flowkater.io/posts/2026-03-08-ai-code-review/, 2026-03-08.
- 김동석. 유연하고 안전하게 배포 Pipeline 운영하기 (SLASH 23). 토스. https://toss.tech/article/slash23-devops, 2023-10-12.
- 카카오엔터프라이즈 워크서버개발팀. https://tech.kakaoenterprise.com/180 (날짜 미기재). / 다나와. Self-Hosted Runner. https://danawalab.github.io/common/2022/08/24/Self-Hosted-Runner.html, 2022-08-24.

### 6.5 논문
- Vasilescu, B., Yu, Y., Wang, H., Devanbu, P., Filkov, V. Quality and productivity outcomes relating to continuous integration in GitHub. ESEC/FSE 2015. DOI 10.1145/2786805.2786850.
- Hilton, M., Tunnell, T., Huang, K., Marinov, D., Dig, D. Usage, costs, and benefits of continuous integration in open-source projects. ASE 2016. DOI 10.1145/2970276.2970358.
- Hilton, M., Nelson, N., Tunnell, T., Marinov, D., Dig, D. Trade-offs in continuous integration: assurance, security, and flexibility. ESEC/FSE 2017. DOI 10.1145/3106237.3106270.
- Felidre, W., Furtado, L., da Costa, D. A., Cartaxo, B., Pinto, G. Continuous Integration Theater. ESEM 2019. DOI 10.1109/esem.2019.8870152.
- Kinsman, T., Wessel, M., Gerosa, M. A., Treude, C. How Do Software Developers Use GitHub Actions to Automate Their Workflows? MSR 2021. DOI 10.1109/msr52588.2021.00054.
- Decan, A., Mens, T., Rostami Mazrae, P., Golzadeh, M. On the Use of GitHub Actions in Software Development Repositories. ICSME 2022. DOI 10.1109/icsme55016.2022.00029.
- Bouzenia, I., Pradel, M. Resource Usage and Optimization Opportunities in Workflows of GitHub Actions. ICSE 2024. DOI 10.1145/3597503.3623303.
- Valenzuela-Toledo, P., Bergel, A., Kehrer, T., Nierstrasz, O. The Hidden Costs of Automation. arXiv:2409.02366, 2024. [프리프린트]
- Rostami Mazrae, P., Decan, A., Mens, T., Wessel, M. An Empirical Study of the Evolution of GitHub Actions Workflows. JSS 236, 112824, 2026. DOI 10.1016/j.jss.2026.112824 / arXiv:2602.14572.
- Khatami, A., Willekens, C., Zaidman, A. Catching Smells in the Act: A GitHub Actions Workflow Investigation. SCAM 2024. DOI 10.1109/scam63643.2024.00015.
- Abrokwah, E., Ghaleb, T. A. An Empirical Study of Complexity, Heterogeneity, and Compliance of GitHub Actions Workflows. arXiv:2507.18062, 2025. [프리프린트]
- Abrokwah, E., Ghaleb, T. A. How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing. EASE 2026. arXiv:2605.02091.
- Hasan, K. A., Tian, Y., Hassan, S., Ding, S. H. H. How Developers Adopt, Use, and Evolve CI/CD Caching. arXiv:2604.13129, 2026. [프리프린트]
- Koishybayev, I. et al. Characterizing the Security of GitHub CI Workflows. USENIX Security 2022. https://www.usenix.org/conference/usenixsecurity22/presentation/koishybayev.
- Muralee, S. et al. ARGUS: A Framework for Staged Static Taint Analysis of GitHub Workflows and Actions. USENIX Security 2023. https://www.usenix.org/conference/usenixsecurity23/presentation/muralee.
- Benedetti, G., Verderame, L., Merlo, A. Automatic Security Assessment of GitHub Actions Workflows. SCORED '22. DOI 10.1145/3560835.3564554.
- Fares, M., Gamage, Y., Baudry, B. Unpacking Security Scanners for GitHub Actions Workflows. arXiv:2601.14455, 2026. [프리프린트]
- Rapaport, S., Pautet, L., Tardieu, S., Zacchiroli, S., Zimmermann, T. Mutating the "Immutable": A Large-Scale Study of Git Tag Alterations. ACM REP 2026. arXiv:2606.31354.
- Ohm, M., Plate, H., Sykosch, A., Meier, M. Backstabber's Knife Collection. DIMVA 2020. arXiv:2005.09535.
- Ladisa, P., Plate, H., Martinez, M., Barais, O. SoK: Taxonomy of Attacks on Open-Source Software Supply Chains. IEEE S&P 2023. DOI 10.1109/sp46215.2023.10179304.
- Okafor, C., Schorlemmer, T. R., Torres-Arias, S., Davis, J. C. SoK: Analysis of Software Supply Chain Security by Establishing Secure Design Properties. SCORED '22. DOI 10.1145/3560835.3564556.
- Newman, Z., Meyers, J. S., Torres-Arias, S. Sigstore: Software Signing for Everybody. ACM CCS 2022. DOI 10.1145/3548606.3560596.
- Meli, M., McNiece, M. R., Reaves, B. How Bad Can It Git? NDSS 2019. DOI 10.14722/ndss.2019.23418.
- Luo, Q., Hariri, F., Eloussi, L., Marinov, D. An empirical analysis of flaky tests. FSE 2014. DOI 10.1145/2635868.2635920.
- Parry, O., Kapfhammer, G. M., Hilton, M., McMinn, P. A Survey of Flaky Tests. ACM TOSEM 2021. DOI 10.1145/3476105.
- Gruber, M., Lukasczyk, S., Kroiß, F., Fraser, G. An Empirical Study of Flaky Tests in Python. ICST 2021. DOI 10.1109/ICST49551.2021.00026.
- Memon, A. et al. Taming Google-scale continuous testing. ICSE-SEIP 2017. DOI 10.1109/icse-seip.2017.16.
- Ghaleb, T. A., da Costa, D. A., Zou, Y. An empirical study of the long duration of continuous integration builds. EMSE 2019. DOI 10.1007/s10664-019-09695-9.
- Ghaleb, T. A., Hassan, S., Zou, Y. Studying the Interplay Between the Durations and Breakages of CI Builds. IEEE TSE 2023. DOI 10.1109/tse.2022.3222160.
- Gallaba, K., Ewart, J., Junqueira, Y., McIntosh, S. Accelerating Continuous Integration by Caching Environments and Inferring Dependencies. IEEE TSE 2022. DOI 10.1109/tse.2020.3048335.
- Savor, T. et al. Continuous deployment at Facebook and OANDA. ICSE 2016 Companion. DOI 10.1145/2889160.2889223.
- Tang, C. et al. Holistic configuration management at Facebook. SOSP 2015. DOI 10.1145/2815400.2815401.
- Li, Z. et al. Gandalf. NSDI 2020. https://www.usenix.org/conference/nsdi20/presentation/li.
- Schermann, G., Cito, J., Leitner, P., Zdun, U., Gall, H. C. We're doing it live. IST 2018. DOI 10.1016/j.infsof.2018.02.010.
- Rahman, A., Mahdavi-Hezaveh, R., Williams, L. A systematic mapping study of infrastructure as code research. IST 2019. DOI 10.1016/j.infsof.2018.12.004.
- Rahman, A., Parnin, C., Williams, L. The Seven Sins: Security Smells in Infrastructure as Code Scripts. ICSE 2019. DOI 10.1109/icse.2019.00033.
- Rahman, A., Farhana, E., Parnin, C., Williams, L. Gang of Eight. ICSE 2020. DOI 10.1145/3377811.3380409.
- Forsgren, N., Humble, J., Kim, G. Accelerate. IT Revolution, 2018. ISBN 9781942788331.
- DORA / Google Cloud. 2024 Accelerate State of DevOps Report. 2024-10-23. [그레이]
- DORA / Google Cloud. 2025 State of AI-assisted Software Development Report. 2025-09-24. [그레이]
- Peng, S., Kalliamvakou, E., Cihon, P., Demirer, M. The Impact of AI on Developer Productivity. arXiv:2302.06590, 2023. [프리프린트]
- Becker, J., Rush, N., Barnes, E., Rein, D. Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity. arXiv:2507.09089, 2025. [프리프린트]
- He, H., Miller, C., Agarwal, S., Kästner, C., Vasilescu, B. Speed at the Cost of Quality. MSR 2026. DOI 10.1145/3793302.3793349 / arXiv:2511.04427.
- He, H., Agarwal, S., Denisov-Blanch, Y., Azaletskiy, P., Koyejo, S., Vasilescu, B. AI Writes Faster Than Humans Can Review. arXiv:2607.01904, 2026. [프리프린트]
- Pearce, H. et al. Asleep at the Keyboard? IEEE S&P 2022. DOI 10.1109/sp46214.2022.9833571.
- Perry, N., Srivastava, M., Kumar, D., Boneh, D. Do Users Write More Insecure Code with AI Assistants? ACM CCS 2023. DOI 10.1145/3576915.3623157.
- Cihan, U. et al. Automated Code Review In Practice. ICSE 2025 SEIP. arXiv:2412.18531.
- Li, H., Zhang, H., Hassan, A. E. The Rise of AI Teammates in SE 3.0. arXiv:2507.15003, 2025. [프리프린트]
- Watanabe, M. et al. On the Use of Agentic Coding. arXiv:2509.14745, 2025. [프리프린트]
- Ehsani, R. et al. Where Do AI Coding Agents Fail? MSR 2026. arXiv:2601.15195.
- Pinna, G., Gong, J., Williams, D., Sarro, F. Comparing AI Coding Agents. MSR 2026 Mining Challenge. arXiv:2602.08915.
- Siddiq, M. L. et al. Security in the Age of AI Teammates. arXiv:2601.00477, 2026. [프리프린트]
- Raida, M. N., Hou, D. Early Adoption of Agentic Coding Tools by GitHub Projects. KDD 2026 Workshop. arXiv:2607.14037.
- Greshake, K. et al. Not What You've Signed Up For. AISec '23. DOI 10.1145/3605764.3623985.
- Fendley, N., Liu, Z., Guan, A., Zhong, J., Cao, Y. Comment and Control. arXiv:2605.11229, 2026. [프리프린트]
- Khelifi, J., Oukhay, I., Ouni, A., Sayagh, M., Saied, M. A. Specifying and Maintaining Agentic Workflows. arXiv:2609.27263, 2026-09-23. [프리프린트]

### 6.6 커뮤니티 (대표 스레드)
- HN. I hate GitHub Actions with passion. https://news.ycombinator.com/item?id=46614558, 2026-01-14.
- HN. The Pain That Is GitHub Actions. https://news.ycombinator.com/item?id=43419701, 2025-03.
- Ian Duncan. GitHub Actions Is Slowly Killing Your Engineering Team. https://www.iankduncan.com/engineering/2026-02-05-github-actions-killing-your-team/, 2026-02-05 (Lobsters https://lobste.rs/s/hkqnro/ , HN https://news.ycombinator.com/item?id=46900381).
- HN. GitHub Actions is shitting the bed again. https://news.ycombinator.com/item?id=47263825, 2026-03-05.
- HN. GitHub Actions is the weakest link. https://news.ycombinator.com/item?id=47933257, 2026-04-28.
- HN. Pricing Changes for GitHub Actions. https://news.ycombinator.com/item?id=46291156.
- GitHub Community Discussion #182186 (self-hosted 과금). https://github.com/orgs/community/discussions/182186.
- aws-actions/amazon-ecs-deploy-task-definition Issue #191. https://github.com/aws-actions/amazon-ecs-deploy-task-definition/issues/191.
- aws/containers-roadmap #1488. https://github.com/aws/containers-roadmap/issues/1488.
- configure-aws-credentials Issues #318, #1137, #1293.
- HN. Cloudflare recommends migrating from Pages to Workers. https://news.ycombinator.com/item?id=44853934, 2025-08-10.
- cloudflare/workers-sdk #8851, #10441.
- Lobsters. tj-actions/changed-files. https://lobste.rs/s/4ko499/ ; Coder discussion #16993.
- HN. There is an AI code review bubble. https://news.ycombinator.com/item?id=46766961, 2026-01-26.
- GeekNews. 코드는 다 읽을 수 없고... https://news.hada.io/article/code-outruns-review ; AI 시대에 코드 리뷰에서 살아남는 방법은? https://news.hada.io/topic?id=33244 ; --author 플래그로 AI 봇 스팸 차단 https://news.hada.io/topic?id=29642.
- HN. Clinejection. https://news.ycombinator.com/item?id=47263595, 2026-02.
- HN. CodeRabbit RCE. https://news.ycombinator.com/item?id=44953032, 2025-08.
- HN. Ask HN: How are you LLM-coding in an established code base? https://news.ycombinator.com/item?id=46331367.
- HN. The future of Terraform CDK. https://news.ycombinator.com/item?id=46222165, 2025-12.
- HN. Cloudflare 2025-11-18 outage postmortem. https://news.ycombinator.com/item?id=45973709.
- velog 튜토리얼·도입기 (OIDC, CodeRabbit, Cloudflare Pages) — URL은 community.md 패턴 6·8·10 참조.

---

## 7. 리서치 한계

- **실패한 리서처:** 없음 (web·paper·community 3종 모두 산출).
- **미접근 플랫폼(커뮤니티):** Reddit(r/devops, r/aws, r/github, r/CloudFlare, r/ExperiencedDevs) 크롤러 차단으로 원문 수집 불가 — 직접 인용 없음. X·Mastodon·Discord/Slack, OKKY, 커리어리, 네이버 카페 원문 미확보. Stack Overflow는 GitHub Issues·AWS re:Post로 대체.
- **한국 소스 빈약:** 웹 약 80%, 커뮤니티 약 80%가 영어. 한국 대형 테크 블로그(우아한형제들·카카오·네이버 D2·LINE·토스)에서 2025~2026년 GitHub Actions/OIDC/Cloudflare 실전 글 미확보. 토스 글은 GoCD 기반. GeekNews 댓글은 적고 대부분 HN 요약 봇. 오프닝의 "날것 감정" 인용은 영어 번역 의존도가 높다.
- **공식 문서 미확보:** Cloudflare의 GitHub OIDC 지원 여부, AWS 공식 CDK diff-on-PR 가이드, App Runner 공지 원문 페이지(relnotes 배너만), dora.dev 리포트 본문(7가지 AI 역량 항목명), CodeRabbit 공식 문서, Renovate 공식 문서, GitHub 2026 보안 로드맵 기능의 실제 프리뷰 출시 여부, OIDC immutable `sub` 클레임 변경 changelog, CDKTF 종료 1차 공지.
- **논문 접근 한계:** Semantic Scholar API 429 → Crossref·OpenAlex·arXiv로 대체(피인용수는 OpenAlex 기준, Google Scholar보다 낮음). ACM DL 전문 403 → 대부분 초록 기반. 원인별 비율(Luo 2014), Hilton 2016 "릴리스 2배", Cursor 논문 구체 수치, 에이전트별 병합률, 확정 워크플로 스멜 7개 목록, Ghaleb 2019·Schermann 2018 초록은 미확인. USENIX 논문(P-14·15·33)은 DOI 없음.
- **주제 공백:** AWS·Cloudflare 특정 배포를 다룬 동료 심사 실증 연구 없음. CI 로그/러너 경유 시크릿 유출(ArtiPACKED 등)은 산업 보고서만. SLSA 채택 효과 정량 연구 없음. 소규모 팀 대상 카나리/프로그레시브 딜리버리 정량 연구 없음. Terraform/CDK 등 현행 IaC 도구 결함 연구 미포함. Lambda 배포 함정(콜드스타트·버전/별칭·SAM vs CDK 실패) 커뮤니티 원문 없음. flaky test 대응 HN 스레드 없음(벤더 글 위주). 롤백 개인 서사 부족. step-security/harden-runner 기능 상세 미수집.
- **인용 정확도:** WebFetch 추출 과정을 거친 영어 인용은 원문과 미세하게 다를 수 있음. 커뮤니티 발언자는 대부분 닉네임 — 경험 주장은 개인 일화로만. 벤더 블로그(Blacksmith, Tenki, BuildPulse, CodeRabbit, Greptile, Aikido) 수치는 이해관계가 있다.
- **의도적 제외(웹):** 날짜 없는 SEO형 튜토리얼(oneuptime, vibecodingwithfred 등), 벤더 비교 마케팅 글(weavai 등).

---

## 신선도 원장 (소스별 발행일·버전 시점·검색 시점)

- 검색·조회 시점(전 원천 공통): **2026-09-26**. 액션 버전표는 GitHub Releases API 2026-09-26 조회.
- 합성 시점 기준 "예정" 항목: pull_request_target 기본 차단 강제 2026-11-02 / GitHub 2026 보안 로드맵(프리뷰 시점 미정).

| 원천 | 소스 | 발행/시점 | 버전·기준 |
|---|---|---|---|
| W-1 | GH Actions Early Sept 2026 updates | 2026-09-03 | GitHub.com 2026-09 (GHES 미지원) |
| W-2 | GH Actions Nov 2025 releases | 2025-11-06 | 2025-11 기준 |
| W-3 | concurrency 큐 확장 | 2026-05-07 | 2026-05 기준 |
| W-4 | Late March 2026 updates | 2026-03-19 | — |
| W-5 | Early April / Early Feb 2026 updates | 2026-04-02 / 2026-02-05 | — |
| W-6 | Merge queue Docs | 상시 갱신 | 2026-09 조회 |
| W-7 | 캐시 10GB 초과 | 2025-11-20 | 2025-11 기준 |
| W-8 | 2026 Actions 가격 | 2025-12 발표, 2026-01-01 시행 | 2026-09 기준 가격 |
| W-9 | arm64 러너 | 2025-08-07 / 2026-01-29 | — |
| W-10 | 버즈빌 ARC | 2024-01-01 | ARC 구버전 가능 |
| W-11 | 레몬베이스 | GeekNews 2024-08-14 | — |
| W-12 | F-Lab 모노레포 | 2023-08-07 | 액션 버전 구버전 가능 |
| W-13 | GitHub OIDC for AWS Docs | 상시 갱신 | 2026-09 조회 |
| W-14 | configure-aws-credentials | 2026-09-15 | v6.3.0 |
| W-15 | Secure use reference | 상시 갱신 | 2026-09 조회 |
| W-16 | tj-actions Advisory / CISA | 2025-03-15(갱신 2025-10-22) / 2025-03-18 | 패치 v46.0.1 |
| W-17 | 데일리시큐 | 2025-03-23 | — |
| W-18 | SHA pinning 정책 | 2025-08-15 | — |
| W-19 | Immutable releases GA | 2025-10-28 | — |
| W-20 | 2026 보안 로드맵 | 2026-03-26 (03-30 갱신) | 로드맵, 2026-09 출시 여부 미확인 |
| W-21 | pull_request_target Docs / THN | 2026-09 조회 / 2026-06-23 | checkout v7(2026-06-18), 강제일 2026-11-02 |
| W-22 | Wiz s1ngularity | 2025-08-27 (08-29 갱신) | — |
| W-23 | CodeQL 워크플로 분석 GA | 2025-04-22 | — |
| W-24 | Dependabot 기본 쿨다운 | 2026-07-14 (옵션 2025-07-01) | github.com 2026-07 기준 |
| W-25 | Artifact attestations | 상시 갱신 | actions/attest v4.2.2 (2026-08-04) |
| W-26 | ECS blue/green→linear/canary→NLB | 2025-07-17 / 2025-10-30 / 2026-02 | 2026-09 기준 |
| W-27 | CodeDeploy→ECS 이관 블로그 | 2025-09-16 | 2025-09 시점, 일부 구버전 |
| W-28 | App Runner 종료 / ECS Express Mode | 2026-04-30 시행(공지 2026-03-31 추정) / 2025-11 / Graviton 2026-09 | 2026-09 기준 |
| W-29 | Lambda GitHub Action | 2025-08-07 | — |
| W-30 | Terraform + GHA | 튜토리얼 상시 갱신 | setup-terraform v4.0.1 (2026-05-12) |
| W-31 | Pages→Workers 마이그레이션 | 2026-09 조회 | 예제 compatibility_date 2026-09-25 |
| W-32 | Worker Previews | 2026-09 조회 | Wrangler 4.135.0+ / 4.136.3+ / Preview URLs 4.21.0+(2025-07) |
| W-33 | wrangler-action | 2026-09-24 | v4.1.3 |
| W-34 | Granular Worker permissions | 2026-09-15 | — |
| W-35 | Gradual deployments / Rollbacks / Metrics | 2026-09 조회 / Changelog 2026-09-25 | — |
| W-36 | D1 migrations | 2026-09 조회 | — |
| W-37 | Protect origin | 2026-09 조회 | — |
| W-38 | Claude Code GitHub Actions | 2026-09 조회 | claude-code-action v1 (v1.0.235, 2026-09-25), Claude Code v2.1.229+ |
| W-39 | claude-code-action security.md | 2026-09 조회 | — |
| W-40 | codex-action security.md | 2026-09 조회 | — |
| W-41 | Aikido PromptPwnd | 2025-12-04 (2026-03-17 갱신) | — |
| W-42 | Copilot coding agent GA / cloud agent Docs | 2025-09-25 / 2026-09 조회 | 명칭 변경 |
| W-43 | Copilot code review agentic GA | 2026-03-05 | — |
| W-44 | Cursor Bugbot | 2026-09 조회 | — |
| W-45 | AGENTS.md 지원 / AAIF | 2025-08-28 / 2025-12-09 | — |
| W-46 | 2025 DORA / dora.dev | 2025-09-24 | 지표 5종(2024~) |
| W-47 | kt cloud | 2026-08-20 | — |
| W-48 | 하이퍼리즘 | 2025-10-27 | — |
| W-49 | Flowkater.io | 2026-03-08 | — |
| W-50 | 토스 SLASH 23 | 2023-10-12 | GoCD 기반 |
| P-1~56 | 논문 메타 | 각 논문 발표 연도(6.5 참조) | Crossref·OpenAlex·arXiv 2026-09-26 조회, 피인용수 OpenAlex 기준 |
| P-7 | Bouzenia & Pradel | ICSE 2024 | 연구 시점 가격 — 현행 요금과 병기 |
| P-14 | Koishybayev et al. | USENIX Sec 2022 | "당시" 수치 |
| P-45 | Pearce et al. | S&P 2022 | 2021 초기 Copilot 🕒 |
| P-39 / P-40 | DORA 2024 / 2025 | 2024-10-23 / 2025-09-24 | 방법론 변경 가능 |
| P-56 | gh-aw 연구 | 2026-09-23 게시 | 검색 3일 전 최신 |
| C 전체 | 커뮤니티 스레드 | 2023~2026-09-21 (개별 날짜는 6.6·원천 참조) | 2026-09-26 수집 |
| C-패턴9 | Mini Shai-Hulud 재활성화 | 2026-09-16 | 최신, 검증 필요 |
| C-휴9 | `wrangler deploy --temporary` | 2026-06 | 검증 필요 |
| C-패턴6 | OIDC immutable sub 주장 | "2026년 7월 이후" | 1차 미확인 |
