# 그룹 E: 엔터프라이즈·관리·인증 (17 URL) — 검색 2026-08-02 기준

<!-- 검색 시점: 2026-08-02 기준 -->
<!-- 수집 방법: 각 페이지 경로에 `.md`를 붙이면 원문 markdown이 그대로 반환된다(예: https://learn.chatgpt.com/codex/auth.md). 아래 내용은 전부 그 원문 markdown에서 발췌·인용한 것이며 추측으로 채운 부분은 없다. -->
<!-- 성공 17 / 실패 0 -->

## 이 그룹을 읽는 법 (개인 개발자용 요약)

17개 페이지 중 개인 개발자에게 직접 쓸모 있는 것은 사실상 **3개**다.

| 등급 | 페이지 | 이유 |
|---|---|---|
| **높음** | `/codex/auth` | 로그인 방식·인증 파일 위치·재인증·헤드리스 로그인. 개인이 매일 만난다. |
| **중간** | `/codex/enterprise/managed-configuration` | `requirements.toml`은 관리자용이지만, "왜 내 설정이 무시되지?"를 설명하는 유일한 문서. 권한 프로필 예시가 개인에게도 교보재. |
| **중간** | `/codex/enterprise/workspace-model-availability` | **2026-08-31 GPT-5.4 은퇴** — 개인의 저장된 모델 설정도 영향받는다. |
| **중간** | `/codex/enterprise/windows-deployment` | Windows 개인 설치 경로(`winget`)가 여기에만 있다. |

나머지 13개는 조직 관리자 전용이다. 다만 문서 전체를 관통하는 개념 **"여섯 개의 통제 경계(six control boundaries)"** 는 개인에게도 개념적으로 유용하다 — "왜 워크스페이스에 접근되는데 GitHub 레포는 안 보이지?"의 답이 여기 있다.

---

### Administration (관리 개요)
- URL: https://learn.chatgpt.com/codex/administration
- 검색: 2026-08-02 기준
- 핵심 내용:
  - 이 페이지는 관리 영역의 랜딩(허브) 페이지다. 본문은 `<CodexDocsOverviewLanding>` 컴포넌트로 되어 있어 산문이 거의 없고 섹션·링크 목록이 전부다.
  - 설명(description) 원문: *"Set access and policy boundaries for ChatGPT, Codex developer tools, APIs, plugins, and connected systems."*
  - 인트로 원문(이 그룹 전체의 핵심 명제):
    > "Administration covers six related boundaries: ChatGPT workspace access; local runtime policy for covered capabilities in the ChatGPT desktop app, Codex CLI, and IDE extension; Codex cloud eligibility; Platform API access; plugin availability and connector permissions; and permissions in connected systems. Start with workspace identity and access, then apply the runtime and source-system controls required for each deployment."
- 섹션·링크 구성 (원문 그대로):

| 섹션 | 하위 페이지 | 설명(원문) |
|---|---|---|
| Getting started | Admin rollout guide (`/codex/enterprise/admin-setup`) | "Plan access, assign owners, configure controls, and verify the rollout." |
| Getting started | ChatGPT Work admin FAQ (`/codex/enterprise/work-admin-faq`) | "Review access, data, governance, usage, and incident controls for ChatGPT Work." |
| Identity and authentication | Authentication overview (`/codex/auth`) | "Compare sign-in methods, credential storage, and enforcement controls." |
| Identity and authentication | Access tokens (`/codex/enterprise/access-tokens`) | "Create and manage tokens for programmatic access." |
| Workspace access, policy, and models | Groups and provisioning (`/codex/enterprise/groups-and-provisioning`) | "Manage manual and SCIM groups, provisioning, and rollout cohorts." |
| Workspace access, policy, and models | Roles and workspace permissions (`/codex/enterprise/roles-and-workspace-permissions`) | "Use the canonical map of workspace, runtime, API, plugin, and source-system controls." |
| Workspace access, policy, and models | Managed configuration (`/codex/enterprise/managed-configuration`) | "Distribute managed settings where supported and enforce runtime requirements for covered capabilities in the ChatGPT desktop app, Codex CLI, and IDE extension." |
| Workspace access, policy, and models | HIPAA configuration (`/codex/hipaa-configuration`) | "Configure local runtime safeguards for workflows that may handle protected health information." |
| Workspace access, policy, and models | Workspace model availability (`/codex/enterprise/workspace-model-availability`) | "Separate model access for ChatGPT, Codex in the ChatGPT desktop app, Codex CLI, the IDE extension, Codex cloud, and the Platform API." |
| Plugin and connector controls | Plugin controls (`/codex/enterprise/apps-and-connectors`) | "Manage plugin availability, connector access and actions, and source-system permissions." |
| Plugin and connector controls | Skill controls (`/codex/enterprise/skills`) | "Compare ChatGPT workspace, local filesystem, and plugin skill controls." |
| Usage, governance, and compliance | Governance (`/codex/enterprise/governance`) | "Choose the right analytics, spend, and audit surface for each question." |
| Usage, governance, and compliance | Workspace analytics (`/codex/enterprise/workspace-analytics`) | "Review workspace-level ChatGPT adoption and Codex usage." |
| Usage, governance, and compliance | Analytics API (`/codex/enterprise/analytics-api`) | "Automate developer activity and code review reporting with the Codex Analytics API." |
| Usage, governance, and compliance | Compliance API and audit events (`/codex/enterprise/compliance-api`) | "Export activity records for audit and investigation workflows." |
| Deployment and model providers | Windows app deployment (`/codex/enterprise/windows-deployment`) | "Choose an installation and update path for managed Windows devices." |
| Deployment and model providers | Remote connections (`/codex/remote-connections`) | "Start and control work on connected computers." |
| Deployment and model providers | Amazon Bedrock (`/codex/amazon-bedrock`) | "Configure supported local clients to use models available through Bedrock." |

- 수치·플랜명·버전: 없음.
- 코드/설정 예시: 없음.
- 제약·주의사항: primary CTA는 `/codex/auth?surface=app`. 이 문서 사이트는 **surface 쿼리 파라미터**(`?surface=app|cli|ide|web`)로 내용이 갈린다 — 원문 markdown에 `<ContentModeSwitch group="codex-surface" ids="app,cli,ide">` 블록이 그대로 노출된다.
- **개인 개발자 관련성: 낮음** — 목차 페이지. 단 "six boundaries" 개념 문장은 인용 가치 있음.

---

### Admin rollout guide (관리자 롤아웃 가이드)
- URL: https://learn.chatgpt.com/codex/enterprise/admin-setup
- 검색: 2026-08-02 기준
- 핵심 내용: ChatGPT Enterprise 롤아웃을 8단계로 나눈 절차서. 다루는 경계는 6가지 — Workspace access / Local runtime policy(desktop app·CLI·IDE extension) / Codex cloud / Platform API access / Plugins and connector access / Permissions in connected systems.
- **핵심 용어 주의 (원문 인용):**
  > "In workspace settings, **Codex Local** is a grouping label for certain local access and access-token controls, not a separate product or client. The current **Allow members to use Codex Local** control covers local use in the ChatGPT desktop app, Codex CLI, and IDE extension."

- 8단계 (원문 제목 그대로):
  1. **Step 1: Assign owners and choose a rollout** — 소유자 지정 대상: Workspace access / Local runtime policy / Codex cloud / Connected systems / Reporting and compliance.
  2. **Step 2: Configure workspace access and identity** — 인용: *"Workspace access doesn't grant repository, file, or action access in a connected service."*
  3. **Step 3: Configure local runtime requirements** — `requirements.toml`을 "supported cloud, device, or system channel"로 배포.
  4. **Step 4: Standardize repository configuration** — `.codex` 또는 `.agents` 디렉터리.
  5. **Step 5: Configure Codex cloud** — 6개 하위 절차.
  6. **Step 6: Configure plugins and connected capabilities** — 4개 검토 항목.
  7. **Step 7: Set up governance and observability**
  8. **Step 8: Verify and maintain the rollout**

- 코드/설정 예시 (Step 3, 원문 그대로):
```toml
default_permissions = ":workspace"

[allowed_permission_profiles]
":read-only" = true
":workspace" = true
```
  Computer Use를 전 표면에서 끄는 예시:
```toml
[features]
browser_use = false
browser_use_full_cdp_access = false
browser_use_external = false
in_app_browser = false
computer_use = false
```

- Step 4 표 (원문 그대로):

| Type | Source | Use it to |
|---|---|---|
| Configuration | Config basics (`/codex/config-file/config-basic`) | Set repository defaults for supported local clients |
| Rules | Rules (`/codex/agent-configuration/rules`) | Control commands that require approval outside the sandbox |
| Skills | Build skills (`/codex/build-skills`) | Make repository workflows available to supported clients |

- Step 5 절차 (원문 그대로):
  1. Grant the intended audience Codex cloud access through supported workspace controls.
  2. Install and configure the supported source-system integration.
  3. Limit repository access in the source system to the repositories each audience needs.
  4. Configure cloud environments, secrets, and internet access for those repositories.
  5. Configure optional hosted workflows such as code review.
  6. Test with a representative user who has the intended workspace and repository permissions.

- Step 6 플러그인 가용 표면 (원문 인용, **중요**):
  > "Plugins are available with ChatGPT Work on the web, with ChatGPT Work and Codex in the ChatGPT desktop app, and through the Codex CLI plugin browser. They aren't available in Chat, the IDE extension, or mobile. ChatGPT and Codex share one universal public plugin directory; workspace controls determine which of those plugins members can access."

- Step 7 리포팅 표면 선택 (원문 그대로):
  - Workspace analytics — "interactive ChatGPT workspace analytics and Codex analytics"
  - Analytics API — "programmatic, aggregated reporting through the Codex Analytics API"
  - Compliance API — "audit and investigation records"
  - ChatGPT usage limits and spend controls — "when plan-dependent Codex activity consumes eligible ChatGPT workspace credits"

- 제약·주의사항:
  - 인용: *"Use permission profiles for supported local clients instead of building new deployments around legacy sandbox-mode restrictions."* — 즉 `sandbox_mode`는 레거시, `permission profiles`가 현행.
  - 인용: *"Repository configuration can supply defaults and reusable workflows. It can't grant workspace, model, Platform API, or connected-system access."*
  - 인용: *"Codex cloud respects the repository permissions and protections exposed by the connected source system. Workspace access doesn't bypass those controls."*
  - 인용: *"Don't build an integration from a copied contract in this guide."* — API 계약은 인증된 레퍼런스가 정전.
  - 보안 백서 링크: `https://trust.openai.com/?itemUid=382f924d-54f3-43a8-a9df-c39e6c959958&source=click` ("Codex security white paper")
- **개인 개발자 관련성: 낮음** — 조직 관리자 전용. 단 Step 4의 `.codex`/`.agents` 레포 설정 개념과 Step 3의 permission profile 예시는 개인도 이해해두면 좋다.

---

### ChatGPT Work admin FAQ
- URL: https://learn.chatgpt.com/codex/enterprise/work-admin-faq
- 검색: 2026-08-02 기준
- 핵심 내용: ChatGPT Work(= Codex 기술을 ChatGPT 안으로 가져온 장기·다단계 작업 모드)의 관리자 FAQ. 6개 대주제 — Core administrative controls / Access, data, systems, and user actions / Compliance / Observability / Governance / Usage and cost / Incident and revocation controls.

- **수치·날짜 (fact-check 원장, 원문 그대로):**
  - **"ChatGPT Work launched July 9, 2026."** (2026-07-09 출시)
  - Enterprise·Edu는 **2주 프리뷰(two-week preview)** 동안 웹·모바일 접근이 **기본 off**. 원문: *"For Enterprise and Edu, web and mobile access is off by default during a two-week preview. Admins can enable billable usage, and explicit opt-outs persist when the default changes."*
  - **Compliance Logs Platform 보존 기간: 30일.** 원문: *"The Compliance Logs Platform retains data for 30 days."*

- 역할·권한·플랜 (원문 그대로):
  - 내장 역할: **Owner, Admin, Member** — *"Built-in Owner, Admin, and Member roles determine who can administer the workspace. Custom roles and member RBAC separately control end-user access to ChatGPT Work, plugins, and other capabilities."*
  - 크레딧: *"ChatGPT Work and Codex share pricing, credits, and usage limits. Eligible Enterprise and Edu admins can set monthly per-user limits through a workspace default, group defaults, and individual overrides. Users can request increases when the workspace allows it. **Business follows a separate credit and spend-control model.**"*
  - 신원 기능(플랜·설정에 따라): SSO, domain verification, SCIM provisioning, user lifecycle management, identity-group synchronization. *"Users can enable account-level OpenAI MFA; enforce workspace-wide MFA through your identity provider."*

- 액션 카테고리 6종 (원문 그대로):
  - **Read:** Access, search, or summarize information from approved sources without changing the underlying data.
  - **Draft:** Prepare documents, email, reports, code, or other content for a person to review before use.
  - **Write:** Create, update, or delete records in connected systems, such as documents, tickets, repositories, or project-management tools.
  - **Share:** Send, publish, or otherwise make information available to more people, systems, or external destinations.
  - **Scheduled:** Start a task at a future time or on a recurring schedule without requiring a user to initiate each run.
  - **Execute:** Run code, shell commands, browser automation, or other tool-driven tasks that interact directly with external environments.

- 관찰 가능성 (원문 그대로, **중요한 한계**):
  - *"The Global Admin Console shows adoption and credit use by user, product, and model, including the ability to drill down across Chat, Work, and Codex usage. The Compliance API covers all user messages and responses across Chat, Work, and Codex."*
  - *"The Compliance Logs Platform provides user prompts and agent responses. **It doesn't track files, actions, or tool calls.**"*
  - OTel: *"Organizations using local Codex clients can opt in to OpenTelemetry exports for events such as API requests, errors, prompt metadata, tool-approval decisions, and tool results. Prompt contents are redacted unless `otel.log_user_prompt = true` is enabled as a separate explicit opt-in."*

- 거버넌스 3계층 (원문 그대로):
  - **ChatGPT Work access controls** determine who can use ChatGPT Work on each surface.
  - **Workspace Agent controls** determine who can build, publish, share, schedule, or configure reusable agents and shared connections.
  - **Codex managed configuration** governs covered local runtime behavior, including permissions, approvals, filesystem and network access, MCP servers, hooks, and command rules.
  - 인용: *"Managed configuration constrains supported runtime behavior. It doesn't grant workspace access, replace RBAC, or revoke a user's workspace access."*
  - 인용: *"Network requirements are experimental and should be tested on the client versions and operating systems in your deployment before broad use."*

- 사용량 한도·스펜드 컨트롤 (Enterprise·Edu 적격 워크스페이스, 원문 그대로):
  - Monitor credit consumption / Set a default monthly limit / Apply group-specific limits / Create user overrides / Review increase requests / Control overall workspace exposure(워크스페이스 크레딧 알림 + overage limit) / Export usage data(**unified Cost API**)
  - *"Users can view their own usage and, if enabled, request more credits, but they can't change assigned limits."*

- 회수(revocation) 경로 (원문 그대로):
  - Remove a user's workspace or group access. For SCIM-managed users, remove access at the identity provider; otherwise, a later synchronization can provision the user again.
  - Disable or restrict the relevant plugin or connector.
  - Revoke a shared connection, bot, or service account through its owning surface. Workspace owners and admins can separately revoke Codex workspace access tokens.
  - Remove a Workspace Agent from publication or delete it through its agent owner or workspace administrator.
  - Disable the relevant schedule or trigger.
  - For Codex access, separately revoke the relevant access token, repository connection, and cloud-environment access. **Managed configuration isn't an access-revocation mechanism.**

- "Additional resources for your teams" 표 (원문 그대로):

| Topic | Use this when explaining | Learn ChatGPT page |
|---|---|---|
| Workspace setup and RBAC | Who can use and administer Codex | Admin rollout guide (`/codex/enterprise/admin-setup`) |
| Authentication | How ChatGPT sign-in, API key sign-in, and workspace policy differ | Authentication (`/codex/auth`) |
| Approvals and sandboxing | How Codex controls file, command, network, and side-effecting tool actions | Agent approvals and security (`/codex/agent-approvals-security`) |
| Managed policy | How admins enforce Codex settings users can't override | Managed configuration (`/codex/enterprise/managed-configuration`) |
| Runtime environments | How Codex cloud setup, secrets, caches, and task phases work | Cloud environments (`/codex/environments/cloud-environment`) |
| Internet access | How Codex cloud domain allowlists and HTTP methods work | Agent internet access (`/codex/cloud/internet-access`) |
| Permissions | How filesystem, network, and deny-read controls work | Permissions (`/codex/permissions`) |
| Observability | How analytics, reporting, and compliance exports work | Governance (`/codex/enterprise/governance`) |
| Automation credentials | How access tokens are created, limited, revoked, and audited | Access tokens (`/codex/enterprise/access-tokens`) |

- 제약·주의사항: *"Coverage for data residency, inference residency, FedRAMP, HIPAA, or a Business Associate Agreement isn't universal."* / *"Local runs in the ChatGPT desktop app, CLI, and IDE execute on the user's machine with operating-system sandboxing and approval policies. Codex cloud runs chats in isolated OpenAI-managed environments."*
- **개인 개발자 관련성: 낮음** — 관리자 전용. 단 "로컬은 내 머신 OS 샌드박스, 클라우드는 OpenAI 격리 환경"이라는 대비 문장과 액션 6분류는 개인에게도 개념적으로 유용.

---

### Authentication (인증) ★ 개인 개발자 필독
- URL: https://learn.chatgpt.com/codex/auth
- 검색: 2026-08-02 기준
- 핵심 내용: ChatGPT 웹·데스크톱 앱·Codex CLI·IDE 확장의 로그인 방법 전부. 이 그룹에서 개인 개발자에게 가장 중요한 페이지다.

#### 1) 두 가지 로그인 방식 (원문 그대로)
> "Codex supports two ways to sign in when using OpenAI models:
> - Sign in with ChatGPT for subscription access
> - Sign in with an API key for usage-based access
>
> The ChatGPT desktop app, Codex CLI, and IDE extension support both sign-in methods for local work. **Codex cloud requires signing in with ChatGPT.**"

로그인 방식이 데이터 정책을 결정한다 (원문 그대로):
- *"When you sign in with ChatGPT, Codex usage follows your ChatGPT workspace permissions, role-based access control (RBAC), and ChatGPT Enterprise retention and residency settings."*
- *"With an API key, usage follows your API organization's retention and data-sharing settings instead."*

#### 2) 표면별 로그인 절차 (원문 그대로)

| 표면 | ChatGPT 로그인 | API 키 로그인 |
|---|---|---|
| ChatGPT web | "Open ChatGPT, sign in, and choose the workspace where you want to work. ChatGPT web keeps the authenticated session in your browser." | (해당 없음) |
| ChatGPT desktop app | 로그아웃 화면에서 **Continue to sign in** → 브라우저 플로우 | **Sign in another way** → 키 입력 → **Continue** |
| Codex CLI | `codex login` 실행 → 브라우저 플로우. *"This is the default authentication path when no valid session is available."* | `printenv OPENAI_API_KEY \| codex login --with-api-key` |
| IDE extension | **Sign in with ChatGPT** → 브라우저 플로우 | **Use API Key** → 키 입력 → **OK** |

CLI API 키 로그인 (원문 코드 그대로):
```shell
printenv OPENAI_API_KEY | codex login --with-api-key
```

#### 3) API 키 인증의 제약 (원문 그대로)
- *"OpenAI bills API key usage through your OpenAI Platform account at standard API rates."*
- *"API key authentication supports local Codex workflows, but some features that rely on ChatGPT workspace access or cloud services are limited or unavailable."*
- *"In Codex CLI and Codex in the ChatGPT desktop app, API key authentication includes access to supported OpenAI-curated plugins. Some plugins aren't available because their connection flows require unsupported OAuth capabilities."*
- *"When you sign in with an API key, Codex uses standard API pricing instead of included ChatGPT plan credits."*
- *"Use API key authentication for programmatic Codex CLI workflows, such as CI/CD jobs. Don't expose Codex execution in untrusted or public environments."*

#### 4) 인증 상태 확인 / 로그아웃 (원문 그대로)
- **Codex CLI:** `codex login status` → 활성 인증 방식 확인. `codex logout` → 현재 자격증명 삭제.
- **desktop app / IDE extension:** 프로필 메뉴에서 활성 계정·API 키 상태 확인, **Log out**.
- **ChatGPT web:** 프로필 메뉴 → **Log out**.

#### 5) 엔터프라이즈 access token (CLI)
```shell
printenv CODEX_ACCESS_TOKEN | codex login --with-access-token
```
> "In ChatGPT Enterprise workspaces, admins can grant the access token permission so permitted members can create Codex access tokens for trusted, non-interactive Codex local workflows. ... Access tokens are intended for trusted scripts, schedulers, and private CI runners. For general OpenAI API calls, continue to use Platform API keys."

#### 6) MFA — Codex 클라우드 (원문 그대로, **개인에게도 강제될 수 있음**)
- *"Codex cloud interacts directly with your codebase, so it needs stronger security than many other ChatGPT features. Enable multi-factor authentication (MFA)."*
- 소셜 로그인(Google, Microsoft, Apple) 사용 시: *"you aren't required to enable MFA on your ChatGPT account, but you can set it up with your social login provider."*
- SSO 사용 시: *"your organization's SSO administrator should enforce MFA for all users."*
- **이메일/비밀번호 로그인:** *"If you log in using an email and password, you must set up MFA on your account before accessing Codex cloud."*
- **혼합 로그인:** *"If your account supports more than one login method and one of them is email and password, you must set up MFA before accessing Codex, even if you sign in another way."*

#### 7) 로그인 캐시 위치 ★ (원문 그대로)
> "Codex caches login details locally in a plaintext file at **`~/.codex/auth.json`** or in your OS-specific credential store."
> "The CLI and extension share the same cached login details. If you log out from either one, you'll need to sign in again the next time you start the CLI or extension."
> "For sign in with ChatGPT sessions, Codex refreshes tokens automatically during use before they expire, so active sessions usually continue without requiring another browser login."

#### 8) 자격증명 저장소 설정 키 ★ (원문 그대로)
```toml
# file | keyring | auto
cli_auth_credentials_store = "keyring"
```
- `file` — stores credentials in `auth.json` under `CODEX_HOME` (defaults to `~/.codex`).
- `keyring` — stores credentials in your operating system credential store.
- `auto` — uses the OS credential store when available, otherwise falls back to `auth.json`.

경고 (원문): *"If you use file-based storage, treat `~/.codex/auth.json` like a password: it contains access tokens. Don't commit it, paste it into tickets, or share it in chat."*

#### 9) 로그인 방식·워크스페이스 강제 (관리 환경) — 설정 키 (원문 그대로)
```toml
# Only allow ChatGPT login or only allow API key login.
forced_login_method = "chatgpt" # or "api"

# When using ChatGPT login, restrict users to a specific workspace.
forced_chatgpt_workspace_id = "00000000-0000-0000-0000-000000000000"
```
> "If the active credentials don't match the configured restrictions, Codex logs the user out and exits."

#### 10) 로그인 진단 / 커스텀 CA (CLI, 원문 그대로)
- *"Direct `codex login` runs write a dedicated **`codex-login.log`** file under your configured log directory."*
- 커스텀 CA 번들:
```shell
export CODEX_CA_CERTIFICATE=/path/to/corporate-root-ca.pem
codex login
```
> "When `CODEX_CA_CERTIFICATE` is unset, Codex falls back to `SSL_CERT_FILE`. The same custom CA settings apply to login, normal HTTPS requests, and secure WebSocket connections."

#### 11) 헤드리스 로그인 ★ (원격·SSH 환경, 원문 그대로)
브라우저 로그인이 안 되는 경우 2가지: 원격/헤드리스 환경, 또는 localhost 콜백 차단.

**권장: Device code authentication (beta)**
1. Enable device code login in your ChatGPT security settings (personal account) or ChatGPT workspace permissions (workspace admin).
2. 인터랙티브 로그인 UI에서 **Sign in with Device Code** 선택, 또는 `codex login --device-auth` 실행.
3. Open the link in your browser, sign in, then enter the one-time code.

**폴백 1: auth 캐시 복사**
1. 브라우저 가능한 머신에서 `codex login` 실행.
2. `~/.codex/auth.json` 존재 확인.
3. 헤드리스 머신의 `~/.codex/auth.json`으로 복사.

```shell
ssh user@remote 'mkdir -p ~/.codex'
scp ~/.codex/auth.json user@remote:~/.codex/auth.json
```
`scp` 없이:
```shell
ssh user@remote 'mkdir -p ~/.codex && cat > ~/.codex/auth.json' < ~/.codex/auth.json
```
Docker 컨테이너로:
```shell
# Replace MY_CONTAINER with the name or ID of your container.
CONTAINER_HOME=$(docker exec MY_CONTAINER printenv HOME)
docker exec MY_CONTAINER mkdir -p "$CONTAINER_HOME/.codex"
docker cp ~/.codex/auth.json MY_CONTAINER:"$CONTAINER_HOME/.codex/auth.json"
```
주의 (원문): *"If your OS stores credentials in a credential store instead of `~/.codex/auth.json`, this method may not apply."*
CI/CD 심화는 `/codex/auth/ci-cd-auth` ("Maintain Codex account auth in CI/CD (advanced)") 참조. 원문: *"API keys are still the recommended default for automation."*

**폴백 2: localhost 콜백 SSH 포워딩** — 기본 포트 **`localhost:1455`**
```shell
ssh -L 1455:localhost:1455 user@remote
```
그 SSH 세션에서 `codex login` 실행 후 출력된 주소를 로컬 브라우저에서 연다.

#### 12) 대체 모델 프로바이더 인증 (원문 그대로)
커스텀 모델 프로바이더 정의 시 3가지 중 택1:
- **OpenAI authentication:** `requires_openai_auth = true` — ChatGPT 또는 API 키로 로그인. LLM 프록시 서버 경유 시 유용. *"When `requires_openai_auth = true`, Codex ignores `env_key`."*
- **Environment variable authentication:** `env_key = "<ENV_VARIABLE_NAME>"`
- **No authentication:** 둘 다 미설정 → 인증 불필요 프로바이더로 간주. *"This is useful for local models."*

- 수치·플랜명·버전: 로컬 콜백 포트 `1455` (2026-08 기준). Device code auth는 **beta**(2026-08 기준).
- **개인 개발자 관련성: 높음** — 이 페이지는 그룹 E에서 개인 독자에게 사실상 유일한 필독 페이지다. `~/.codex/auth.json`, `codex login/logout/login status`, `--with-api-key`, `--device-auth`, `cli_auth_credentials_store`, `CODEX_CA_CERTIFICATE`, SSH 포트포워딩 1455 전부 개인 워크플로에 그대로 쓰인다.

---

### Access tokens (액세스 토큰)
- URL: https://learn.chatgpt.com/codex/enterprise/access-tokens
- 검색: 2026-08-02 기준
- 핵심 내용: Codex access token = "ChatGPT workspace credentials scoped to Codex permissions". 신뢰된 비대화형 로컬 워크플로(Codex CLI, app-server 기반 자동화)를 ChatGPT 워크스페이스 신원으로 인증한다.

- **플랜 (원문 그대로):** *"Codex access tokens are currently supported for **ChatGPT Business and Enterprise** workspaces."*
  - (주: `/codex/auth` 페이지는 "In ChatGPT **Enterprise** workspaces, admins can grant the access token permission"이라고만 적어 두 페이지의 플랜 서술 범위가 다르다. 이 페이지가 더 구체적이다 — Business + Enterprise.)

- 생성 위치: ChatGPT admin console의 **Access tokens** 페이지 `https://chatgpt.com/admin/access-tokens`
- 원문: *"They're tied to the ChatGPT user who creates them and that user's workspace. The tokens act as agent identities for programmatic local workflows."*
- 선택 기준 (원문): *"If a Platform API key works for your automation, keep using API key auth. Use Codex access tokens when a trusted local workflow specifically needs ChatGPT workspace access, workspace-managed entitlements, or enterprise controls."*
- **혼동 주의 (원문):** *"Codex access tokens authenticate trusted local workflows through Codex CLI or an app-server client; they do not authenticate workspace agent trigger calls."* → Workspace Agents API는 별도 **Workspace Agent access token** 사용 (`/workspace-agents/authentication`).

- 사용 사례 (원문 그대로):
  - `codex exec` jobs that run from trusted automation.
  - Local scripts that need repeatable, non-interactive Codex CLI runs.
  - Trusted app-server-based automation.
  - Enterprise workflows where usage should be associated with a ChatGPT workspace user instead of an API organization key.

- 주요 리스크 5가지 (원문 그대로, 제목 볼드 포함):
  - **Leaked secrets:** anyone with the token can start local runs through Codex CLI or an app-server client as the token creator. Store tokens in a secret manager, keep them out of logs, and rotate them regularly.
  - **Runner trust:** public CI, forked pull requests, or shared machines can expose tokens to people outside your workspace. Use access tokens only on trusted runners.
  - **Shared identities:** one person's token reused across unrelated teams makes ownership and audit trails harder to interpret. Create tokens for a specific workflow owner.
  - **Stale credentials:** long-lived tokens can remain active after the workflow changes. Prefer time-limited tokens and revoke tokens that are no longer used.
  - **Wrong credential type:** Codex access tokens are for trusted local automation through Codex CLI or an app-server client. Use Workspace Agent access tokens to trigger published ChatGPT workspace agents, and use Platform API keys for general OpenAI API calls.

- 설정 항목 (원문 그대로):
  - `Workspace Settings > Permissions & roles` (`https://chatgpt.com/admin/settings`)
  - **Access tokens** 섹션 → **Allow users to create access tokens** 토글
  - **Codex Local** 섹션 → **Allow members to use Codex Local** (desktop app·CLI·IDE extension 로컬 사용 커버)
  - **Codex Local** 섹션 → **Access token expiration limit** — *"The limit applies to new access tokens. Existing tokens keep their current expiration."*

- 토큰 생성 절차 (원문 그대로):
  1. Go to Access tokens.
  2. Select **Create**.
  3. Enter a descriptive name, such as `release-ci` or `nightly-docs-check`.
  4. Choose an expiration. Prefer a finite expiration such as **7, 30, 60, or 90 days**. If you choose **No expiration**, rotate the token on a regular schedule.
  5. Select **Create**.
  6. Copy the generated access token immediately. **You can't view it again after you close the modal.**
  7. Store the token in your secret manager or CI secret store.

- **수치 (fact-check 원장):** *"The shortest custom expiration is **one day**."* / 권장 만료: 7·30·60·90일 / *"Revoked and expired tokens can't be used to start new authenticated runs."* (2026-08 기준)

- 코드 예시 (원문 그대로):
```shell
export CODEX_ACCESS_TOKEN="<access-token>"
codex exec --json "review this repository and summarize the top risks"
```
```shell
printf '%s' "$CODEX_ACCESS_TOKEN" | codex login --with-access-token
codex exec "summarize the last release diff"
```
> "`codex login --with-access-token` stores an agent identity credential in Codex CLI auth storage. If you prefer not to persist credentials on the machine, use the `CODEX_ACCESS_TOKEN` environment variable instead."
> "`codex app-server` can use the same credential through `CODEX_ACCESS_TOKEN` or a login created with `codex login --with-access-token`... For a remote WebSocket connection, configure a separate bearer or capability token as described in App server; **don't reuse the Codex access token as the transport token.**"

- 회전(rotate) 절차 (원문 그대로): 1) Create a replacement token. 2) Update the secret in the runner, scheduler, or secret manager. 3) Run a smoke test with the new token. 4) Revoke the old token from Access tokens.

- **권한 모델 표 (원문 그대로 — 표 전체 보존):**

| Capability | Workspace owners and admins | Member with access token permission | Member without access token permission |
|---|---|---|---|
| Open Access tokens | Yes | Yes | No |
| Create access tokens | Yes, for their own ChatGPT workspace identity | Yes, for their own ChatGPT workspace identity | No |
| List access tokens | Workspace list, including who created each token | Only tokens they created | No |
| Revoke access tokens from the Access tokens page | Any token in the workspace | Only tokens they created | No page access |
| Grant or remove access token permission | Yes | No | No |
| Manage other local-client or Codex cloud settings | Yes, based on workspace admin permissions | No, unless separately granted | No |

> "In short: workspace owners and admins manage access at the workspace level. Members need the access token permission to create and manage their own tokens, but that permission grants neither admin rights nor access to other members' tokens."

- 트러블슈팅 (원문 그대로):
  - **The access tokens page returns 404 or forbidden** — *"Ask a workspace owner or admin to confirm that your role includes **Allow users to create access tokens**."*
  - **`codex login --with-access-token` fails** — *"Confirm that you copied the generated access token, not a browser session token or Platform API key. Also confirm that the token hasn't expired or been revoked."*
- **개인 개발자 관련성: 중간** — 개인 계정(Plus/Pro)에는 해당 없음(Business/Enterprise 전용). 다만 "CI에서 Codex를 어떻게 인증하나"라는 질문의 답이 여기 있고, 개인도 **Platform API 키가 기본 답**이라는 결론(*"If a Platform API key works for your automation, keep using API key auth."*)은 알아둘 가치가 있다.

---

### Groups and provisioning (그룹과 프로비저닝)
- URL: https://learn.chatgpt.com/codex/enterprise/groups-and-provisioning
- 검색: 2026-08-02 기준
- 핵심 내용: 그룹은 ChatGPT 워크스페이스 접근을 조직하고 커스텀 역할을 실을 수 있다. 그룹 멤버십은 로컬 런타임 정책·연결 시스템 권한과 별개다.

- **멤버십 소스 표 (원문 그대로):**

| Group type | Membership source | When it applies |
|---|---|---|
| Manually managed | ChatGPT workspace administration | The group is small, temporary, or not managed through directory sync |
| Identity-provider managed | Your identity provider through SCIM | Membership should follow the organization's directory and member-removal process |

> "Manual and identity-provider-managed groups can coexist. For synchronized groups, the identity provider is the membership source; later provisioning updates can overwrite workspace-side changes. The Help Center owns current SCIM behavior, supported attributes, and setup steps."

- 접근 경계 (원문 그대로, **중요**):
  > "SCIM provisions workspace membership and group assignments. **It doesn't grant permissions in GitHub, Google Drive, Slack, or another connected system.** It also doesn't replace local runtime requirements or Platform API organization access."
  > "Workspace RBAC and local runtime requirements are separate control systems. A group can be relevant to both, but **don't infer a managed-requirements matching or precedence rule from workspace group order.**"

- 현행 절차 소스 (원문 링크 그대로):
  - Manage members, seat types, roles, and access — `https://help.openai.com/en/articles/8266401-managing-members-seat-types-roles-and-access-in-chatgpt-enterprise`
  - Manage groups — `https://help.openai.com/en/articles/9083985-group-permissions-in-gpts`
  - SCIM integration FAQ — `https://help.openai.com/en/articles/10011769-openai-platform-scim-integration-faq`
  - Manage workspace settings — `https://help.openai.com/en/articles/8411955`
- 수치·플랜명·버전: 없음.
- 제약·주의사항: 이 페이지는 절차를 담지 않고 Help Center로 위임한다. *"Workspace administration details can change."*
- **개인 개발자 관련성: 낮음** — 순수 조직 관리자 영역.

---

### Roles and workspace permissions (역할과 워크스페이스 권한) ★ 개념적 정전
- URL: https://learn.chatgpt.com/codex/enterprise/roles-and-workspace-permissions
- 검색: 2026-08-02 기준
- 핵심 내용: **이 그룹 전체의 정전(canonical) 지도.** 관리는 6개 통제 경계에 걸치며, 한 경계에서 접근을 허용해도 다른 경계 접근이 생기지 않는다.

- **용어 경고 (원문 그대로):**
  > "In workspace settings, **Codex Local** is a grouping label for certain local access and access-token controls, not a separate product or client. Individual controls in the group can have different scopes. The current **Allow members to use Codex Local** workspace permission covers local use in the ChatGPT desktop app, Codex CLI, and IDE extension. Managed configuration is a separate layer that constrains supported runtime behavior for covered capabilities in those clients. Features and effective requirements can differ by client and version."

- **6개 통제 경계 표 (원문 그대로 — 표 전체 보존):**

| Boundary | What it controls | What it doesn't control | Current source |
|---|---|---|---|
| ChatGPT workspace | Membership, seats, built-in administration roles, and role-based access to supported workspace features | Local agent permissions, Platform API organization access, or permissions in a connected service | ChatGPT workspace access (help.openai.com/…/8266401…) and RBAC (help.openai.com/…/11750701-rbac) |
| Local clients | Runtime behavior for covered capabilities in the ChatGPT desktop app, Codex CLI, and IDE extension, including approvals, filesystem and network access, permission profiles, and allowed integrations | A ChatGPT seat, feature or model entitlement, or access to external data | Managed configuration (`/codex/enterprise/managed-configuration`) and Permissions (`/codex/permissions`) |
| Codex cloud | Eligibility to use hosted Codex workflows and the cloud environments made available to the user | Local runtime policy or the repository permissions granted by a source system | Cloud environments (`/codex/environments/cloud-environment`) |
| Platform API | Organization and project membership, API keys, model access, usage, and billing for API-authenticated work | ChatGPT workspace membership, local-client access, or Codex cloud access | OpenAI API Platform (`https://platform.openai.com/docs/overview`) |
| Plugins | Plugin availability and installation, bundled skills, connector access, and supported connector actions | Authorization in the connected service or broader local and cloud runtime permissions | Plugin controls (`/codex/enterprise/apps-and-connectors`) |
| Connected systems | Which repositories, files, messages, and actions the authenticated account can access in the source system | ChatGPT workspace, plugin, Codex cloud, or Platform API entitlement | The connected service's administration and access controls |

- **인용 가능한 핵심 구절 (원문 그대로):**
  > "A request must pass every boundary that applies to it. For example, workspace access can make a plugin available, but the connected service still decides which data the signed-in account can read. A local permission profile can restrict a run in a supported local client, but it can't grant a workspace feature or model."

- 워크스페이스 접근 배정 (원문 그대로):
  > "ChatGPT workspace administration separates product access from administrative authority. **The workspace plan and a member's seat determine which product surfaces are available. Built-in workspace roles determine who can administer the workspace. Role-based access control (RBAC) determines which supported features members can use.**"
  > "Administrators can assign custom roles through groups, and a member can receive access from more than one group."

- 로컬 런타임 정책 (원문 그대로):
  > "Local runtime policy constrains covered capabilities in the ChatGPT desktop app, Codex CLI, and IDE extension. Cloud-managed requirements additionally depend on supported ChatGPT sign-in and plan eligibility. Permission profiles and managed requirements can constrain commands, filesystem access, network access, approvals, and other local runtime behavior. **They don't change the user's seat, workspace role, model entitlement, or permissions in an external system.**"
  > "Users can select a built-in or custom permission profile when local policy allows it."

- 수치·플랜명·버전: 구체 수치 없음. 역할·시트 목록은 의도적으로 Help Center에 위임 — *"Because available seats, roles, and permissions change with product and plan updates, use the Help Center for the current permission list and setup procedure."*
- **개인 개발자 관련성: 중간** — 6경계 표 자체는 관리자용이지만, "왜 Codex가 내 GitHub 레포에 접근 못하지?", "왜 관리자가 켜줬는데 모델이 안 보이지?" 같은 개인의 혼란을 설명하는 유일한 개념 지도다. 책의 개념 장에서 인용 가치 높음.

---

### Managed configuration (관리형 구성) ★ 설정 키 밀집
- URL: https://learn.chatgpt.com/codex/enterprise/managed-configuration
- 검색: 2026-08-02 기준
- 핵심 내용: 관리자가 로컬 클라이언트(desktop app·CLI·IDE extension) 런타임 동작을 통제하는 두 방식 — **Requirements**(사용자가 못 덮음)와 **Managed defaults**(시작값, 세션 중 변경 가능).

> "**Requirements**: admin-enforced constraints that users can't override."
> "**Managed defaults**: starting values applied when a supported client launches. Users can still change settings during a run; the client reapplies managed defaults the next time it starts."

#### A. Requirements (`requirements.toml`)

제약 대상 (원문 그대로): *"approval policy, approvals reviewer, automatic review policy, sandbox mode, permission profiles, web search mode, managed hooks, which MCP servers users can enable, and which user-configured plugin marketplace sources they can add, install from, or refresh"*

> "When resolving configuration (for example from `config.toml`, profile files, or CLI config overrides), if a value conflicts with an enforced rule, the local client falls back to a compatible value and notifies the user. If you configure an `mcp_servers` allowlist, the client enables an MCP server only when both its name and identity match an approved entry; otherwise, the client disables it."

**버전 (fact-check 원장):**
> "For **Codex 0.138.0 or later**, prefer permission profiles with `allowed_permission_profiles` and managed `default_permissions`. Use `allowed_sandbox_modes` only for legacy deployments that still configure `sandbox_mode`."
> "Permission-profile allowlists require **Codex 0.138.0 or later**. **Codex 0.137.0 and earlier ignore** `allowed_permission_profiles` and managed `default_permissions`."
(0.138.0 / 2026-08 기준)

**위치와 우선순위 (낮은 것 → 높은 것, 원문 그대로):**
1. System `requirements.toml` (`/etc/codex/requirements.toml` on Unix systems, including Linux and macOS, or `%ProgramData%\OpenAI\Codex\requirements.toml` on Windows).
2. Enterprise-managed requirements delivered in the cloud config bundle.
3. Legacy `managed_config.toml` fields that the local client reinterprets as requirements.
4. macOS managed preferences (MDM) delivered through `com.openai.codex:requirements_toml_base64`.

> "Higher-precedence layers override ordinary scalar and list values from lower layers. Tables merge by key, while requirements such as rules, hooks, and filesystem restrictions have field-specific composition behavior."
> 하위호환: *"supported local clients reinterpret the legacy `approval_policy`, `approvals_reviewer`, and `sandbox_mode` fields as requirements."*

**클라우드 관리형 requirements** — 관리 콘솔: `https://chatgpt.com/codex/settings/managed-configs`
예시 (원문 그대로):
```toml
enforce_residency = "us"
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]

[rules]
prefix_rules = [
  { pattern = [{ any_of = ["bash", "sh", "zsh"] }], decision = "prompt", justification = "Require explicit approval for shell entry points" },
]
```
적용 메커니즘 (원문): *"the client first checks for a valid, identity-matched cache entry. If no valid entry is available, the client fetches the applicable bundle with retries and writes a signed cache entry on success. If the request fails or times out and no valid cache is available, the cloud config bundle load returns an error rather than silently starting without the cloud-managed requirements layer."*

**기본 차단 예시 (`--yolo` 차단, 원문 그대로):**
```toml
allowed_approval_policies = ["untrusted", "on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```
> "This example blocks `--ask-for-approval never` and `--sandbox danger-full-access` (including `--yolo`)."

**개별 설정 키 (원문 그대로):**

| 키 | 값 예시 | 효과 |
|---|---|---|
| `allow_appshots` | `false` | Appshots 비활성. app-server의 `configRequirements/read`는 `allowAppshots`로 동일 제약 수신. 생략/`null`이면 비활성 아님. |
| `allow_remote_control` | `false` | device remote control 비활성. **SSH remote connections는 비활성화하지 않음.** |
| `allowed_permission_profiles` | 테이블 | 존재 시 "the complete list of allowed profiles" — `true`만 허용, 생략·`false`는 거부(미래 빌트인 포함). |
| `default_permissions` | `":workspace"` 등 | 기본 프로필. 생략 시 *"the local runtime defaults to `:workspace` only when both `:workspace` and `:read-only` are explicitly allowed."* |
| `allowed_web_search_modes` | `["cached"]` | `"disabled"`는 암묵 허용. `[]`면 `"disabled"`만 허용. `["cached"]`는 `danger-full-access` 세션에서도 라이브 웹검색 차단. |
| `allowed_approval_policies` | `["on-request"]` | 승인 정책 제한 |
| `allowed_approvals_reviewers` | `["auto_review"]` / `["user"]` | 자동 리뷰 요구 또는 수동 승인 허용 |
| `guardian_policy_config` | 문자열(멀티라인) | 자동 리뷰 정책의 테넌트 고유 섹션 교체. *"Managed `guardian_policy_config` takes precedence over local `[auto_review].policy`."* |
| `allow_managed_hooks_only` | `true` | user·project·session·plugin 훅 건너뛰고 managed 훅만 로드 |
| `features.plugins` | `false` | 플러그인 끄기. *"This setting also applies when users sign in to Codex with an API key."* |
| `[marketplaces] restrict_to_allowed_sources` | `true` | 사용자 구성 마켓플레이스 소스 제한 |
| `[computer_use] allow_locked_computer_use` | `false` | macOS 잠금 상태 Computer Use 차단 (Computer Use를 켜는 건 아님) |

**빌트인 권한 프로필 이름:** `:read-only`, `:workspace`, `:danger-full-access` (앞의 `:`가 예약 접두사). 커스텀 이름 규칙 (원문): *"Custom names can't start with `:` or use the reserved `filesystem` name."*

권한 프로필 예시 3종 (원문 그대로):
```toml
# 표준 프로필 허용 (full access 제외)
default_permissions = ":workspace"

[allowed_permission_profiles]
":read-only" = true
":workspace" = true
# ":danger-full-access" is omitted, so it is denied.
```
```toml
# 관리형 최소권한 기본값
default_permissions = "acme_review_only"

[allowed_permission_profiles]
":read-only" = true
":workspace" = true
acme_review_only = true
# ":danger-full-access" is intentionally omitted, so it is denied.

[permissions.acme_review_only]
description = "Review code without modifying the workspace."
extends = ":read-only"
```
```toml
# 엔터프라이즈 정의 프로필만 허용
default_permissions = "acme_workspace"

[allowed_permission_profiles]
acme_workspace = true

[permissions.acme_workspace]
description = "Workspace access with sensitive files denied."
extends = ":workspace"

[permissions.acme_workspace.filesystem]
glob_scan_max_depth = 3

[permissions.acme_workspace.filesystem.":workspace_roots"]
"**/*.env" = "deny"
```
> "The custom profile can extend `:workspace` even though users can't select the built-in `:workspace` profile directly."
> "Permission allowlists combine by profile name. Because cloud requirements have higher precedence than system requirements, cloud requirements can use `false` to turn off a profile allowed by the system file."

**호스트별 샌드박스 오버라이드 (원문 그대로):**
```toml
allowed_sandbox_modes = ["read-only"]

[[remote_sandbox_config]]
hostname_patterns = ["*.devbox.example.com", "runner-??.ci.example.com"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```
> "Host-specific entries currently override `allowed_sandbox_modes` only." / *"Matching is case-insensitive; `*` matches any sequence of characters, and `?` matches one character."* / *"The first matching `[[remote_sandbox_config]]` entry wins within the same requirements source."* / **"Host name matching is for policy selection only; don't treat it as authenticated device proof."**

**네트워크 접근 requirements — 실험적 (원문 경고 그대로):**
> "`[experimental_network]` is experimental and may change. Do not enable these requirements broadly across an enterprise deployment without validating them on the local client versions and operating systems your users run. **Windows support is still limited**; avoid applying this policy to Windows users unless you have tested it in your environment."
```toml
experimental_network.enabled = true
experimental_network.allowed_domains = [
  "api.openai.com",
  "*.example.com",
]
experimental_network.denied_domains = [
  "blocked.example.com",
  "*.exfil.example.com",
]
```
> "Use `experimental_network.managed_allowed_domains_only = true` only when you also define administrator-owned `allowed_domains` and want that allowlist to be exclusive."

**피처 플래그 핀 (원문 그대로):**
```toml
[features]
personality = true
unified_exec = false

# Disable surface-specific features when needed.
browser_use = false
browser_use_full_cdp_access = false
browser_use_external = false
in_app_browser = false
computer_use = false
```
각 키 의미 (원문 그대로):
- `in_app_browser = false` disables the built-in browser pane.
- `browser_use = false` disables Computer Use in browsers and Browser Agent availability.
- `browser_use_full_cdp_access = false` disables full CDP access in the local runtime, including Browser Developer mode, and prevents the ChatGPT desktop app from enabling the corresponding setting.
- `browser_use_external = false` disables external Browser Use.
- `computer_use = false` disables Computer Use, Record & Replay, and related install or setup flows.

**deny-read 강제 (원문 그대로):**
```toml
[permissions.filesystem]
deny_read = [
  # values can be absolute paths...
  "/**/*.env",
  # ...or relative to $HOME/%USERPROFILE% using `~`.
  "~/.ssh",
  # But relative paths starting with `./` are not allowed.
]
```
> "When deny-read requirements are present, the local runtime rejects full-access permissions and keeps local execution in a read-only or workspace sandbox so it can enforce them. **On native Windows, managed `deny_read` applies to direct file tools; shell subprocess reads don't use this sandbox rule.**"

**관리형 훅 (원문 그대로):**
```toml
allow_managed_hooks_only = true

[features]
hooks = true

[hooks]
managed_dir = "/enterprise/hooks"
windows_managed_dir = 'C:\enterprise\hooks'

[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = "python3 /enterprise/hooks/pre_tool_use_policy.py"
command_windows = 'py -3 C:\enterprise\hooks\pre_tool_use_policy.py'
timeout = 30
statusMessage = "Checking managed Bash command"
```
> "The local runtime enforces the hook configuration from `requirements.toml`, but **it doesn't distribute the scripts in `managed_dir`.** Deliver those scripts with your MDM or device-management solution."

**커맨드 규칙 (원문 그대로):**
> "Unlike `.rules`, requirements rules must specify `decision`, and that decision must be `"prompt"` or `"forbidden"` (**not `"allow"`**)."
```toml
[rules]
prefix_rules = [
  { pattern = [{ token = "rm" }], decision = "forbidden", justification = "Use git clean -fd instead." },
  { pattern = [{ token = "git" }, { any_of = ["push", "commit"] }], decision = "prompt", justification = "Require review before mutating history." },
]
```

**MCP 서버 허용목록 (원문 그대로):**
```toml
[mcp_servers.docs]
identity = { command = "codex-mcp" }

[mcp_servers.remote]
identity = { url = "https://example.com/mcp" }
```
```toml
[mcp_servers.internal.identity]
command = { executable = "/usr/local/bin/codex-mcp", args = [
  { match = "exact", value = "serve" },
  { match = "prefix", value = "--workspace=" },
] }
```
> "The string form of `identity.command` matches only the configured `command`. It doesn't inspect `args`, `cwd`, `env`, or `env_vars`."
> "Argument and URL rules support `exact`, `prefix`, and full-value `regex` matching."
> "Plugin-bundled MCP servers use the same identity shapes under `plugins.<plugin>.mcp_servers.<server>`."
> "**If `mcp_servers` is present but empty, the local client disables all MCP servers.**"

**마켓플레이스 소스 제한 (원문 그대로):**
```toml
[marketplaces]
restrict_to_allowed_sources = true

[marketplaces.allowed_sources.company_plugins]
source = "git"
url = "https://github.com/example/company-plugins.git"
ref = "main"

[marketplaces.allowed_sources.internal_git]
source = "host_pattern"
host_pattern = '^git\.example\.com$'

[marketplaces.allowed_sources.local_plugins]
source = "local"
path = "/opt/company/codex-plugins"
```
> "These requirements reject unmatched marketplace add, plugin install, and configured Git marketplace refresh operations for user-configured sources. Codex-managed OpenAI marketplaces remain available when their source and reserved name match. **The requirements don't filter already configured user marketplaces or their plugins at runtime.**"
> "These source restrictions apply only where a local client supports plugin marketplace operations: ChatGPT Work and Codex in the desktop app, and Codex CLI. They don't add plugins to Chat, the IDE extension, or mobile."

#### B. Managed defaults (`managed_config.toml`)

> "Managed defaults merge on top of a user's local `config.toml` and take precedence over any CLI `--config` overrides, setting the starting values when a supported local client launches."

**★ 모델 은퇴 경고 (fact-check 원장, 원문 그대로):**
> "If a managed default, macOS MDM profile, or saved configuration pins `gpt-5.4` or `gpt-5.4-mini` for users signed in with ChatGPT, update it **before August 31, 2026**. Replace `gpt-5.4` with **`gpt-5.6-terra`** and `gpt-5.4-mini` with **`gpt-5.6-luna`**. The OpenAI API and Codex authenticated with your own API key aren't affected."

**우선순위 (위가 아래를 덮음, 원문 그대로):**
- Managed preferences (macOS MDM; highest precedence)
- `managed_config.toml` (system/managed file)
- `config.toml` (user's base configuration)

> "CLI `--config key=value` overrides apply to the base, but managed layers override them. This means each run starts from the managed defaults even if you provide local flags."
> "Cloud-managed requirements affect the requirements layer (not managed defaults)."

**위치 (원문 그대로):**
- Linux/macOS (Unix): `/etc/codex/managed_config.toml`
- Windows/non-Unix: `~/.codex/managed_config.toml`
> "If the file is missing, the local runtime skips the managed layer."

**macOS MDM (원문 그대로):**
- Preference domain: `com.openai.codex`
- Keys: `config_toml_base64` (managed defaults), `requirements_toml_base64` (requirements)
> "For managed defaults (`config_toml_base64`), managed preferences have the highest precedence. For requirements (`requirements_toml_base64`), precedence follows the cloud-managed requirements order described above."

MDM 배포 워크플로 4단계 — 도구 예시 원문 그대로: `Jamf Pro`, `Fleet`, `Kandji`.
1. Build the managed payload TOML and encode it with `base64` (no wrapping).
2. Drop the string into your MDM profile under the `com.openai.codex` domain at `config_toml_base64` or `requirements_toml_base64`.
3. Push the profile, then ask users to restart the supported local client and confirm the startup config summary reflects the managed values.
4. When revoking or changing policy, update the managed payload; the client reads the refreshed preference the next time it launches.

**예시 `managed_config.toml` (원문 그대로):**
```toml
# Set conservative defaults
approval_policy = "on-request"
sandbox_mode    = "workspace-write"

[sandbox_workspace_write]
network_access = false             # keep network disabled unless explicitly allowed

[otel]
environment = "prod"
exporter = "otlp-http"            # point at your collector
log_user_prompt = false            # keep prompts redacted
# exporter details live under exporter tables; see Monitoring and telemetry above
```

**권장 가드레일 (원문 그대로):**
- Prefer `workspace-write` with approvals for most users; reserve full access for controlled containers.
- Keep `network_access = false` unless your security review allows a collector or domains required by your workflows.
- Use managed configuration to pin OTel settings (exporter, environment), but keep `log_user_prompt = false` unless your policy explicitly allows storing prompt contents.
- Periodically audit diffs between local `config.toml` and managed policy to catch drift; managed layers should win over local flags and files.

- **개인 개발자 관련성: 중간** — 배포는 관리자 몫이지만 (1) 권한 프로필 이름(`:read-only`/`:workspace`/`:danger-full-access`), (2) `--yolo`가 무엇을 의미하는지(`--ask-for-approval never` + `--sandbox danger-full-access`), (3) 회사 노트북에서 내 `config.toml`이 무시되는 이유, (4) **GPT-5.4 은퇴일** — 넷 다 개인에게 직접 영향.

---

### HIPAA configuration guide for Codex Local
- URL: https://learn.chatgpt.com/codex/hipaa-configuration
- 검색: 2026-08-02 기준
- 핵심 내용: PHI(protected health information)를 다룰 수 있는 워크플로를 위한 Codex Local 구성 가이드. **Codex Local = the ChatGPT desktop app, Codex IDE extension, and Codex CLI**(사용자 컴퓨터에서 실행).

- **가장 중요한 단일 문장 (원문 그대로, 볼드도 원문):**
  > "**The BAA doesn't cover Codex cloud. Don't use Codex cloud with PHI.**"

- 적용 대상 플랜/제품 (원문 그대로): *"If you use **ChatGPT for Healthcare, ChatGPT for Clinicians, or a Regulated workspace** and have an applicable OpenAI Business Associate Agreement (BAA), OpenAI handles PHI it receives from Codex Local consistent with the BAA."*
- **수치 (fact-check 원장):** *"For usage authenticated through ChatGPT, OpenAI keeps audit records for **up to 30 days** so you can retrieve them through the Compliance API."* / *"OpenAI doesn't train on ChatGPT Enterprise data or Codex Local data."*
- 면책 (원문): *"This guide isn't legal advice."*

- 공동 책임 (원문 그대로): *"ChatGPT Enterprise stores inputs and outputs in the OpenAI cloud. Your users' workstations keep inputs and outputs from Codex Local."*
- 고객 책임 범위 (원문): *"You are responsible for securely configuring local workstations, source repositories, local retention, local MCP servers, Browser Use and Computer Use activity, desktop apps, and third-party services such as Google Drive or GitHub that Codex can access."*
- 서드파티 경고 (원문): *"**OpenAI's BAA doesn't make another vendor a HIPAA-compliant destination.**"*

- OpenAI 보안 프로그램 4축 (원문 볼드 그대로): **Enterprise Risk Management** / **Secure development and CI/CD safeguards** / **OpenAI's vulnerability management program** / **Data protection controls**

- 활성화 절차 (원문): *"Contact your OpenAI Account Director to enable Codex HIPAA support for the workspace."*
- RBAC 페이지: `https://chatgpt.com/admin/permissions` / 커넥터 설정: `https://chatgpt.com/admin/ca` / 정책 페이지: `https://chatgpt.com/codex/settings/policies`

- **requirements 적용 순서 (이 페이지 서술, 원문 그대로 — 주의: managed-configuration 페이지의 순서 서술과 표현이 다르다):**
  > "Codex applies requirements layers in this order: cloud-managed requirements, macOS MDM requirements, and system `requirements.toml`. **Earlier requirements take precedence for any field they set.**"
  - ⚠️ **대조 필요:** `/codex/enterprise/managed-configuration`은 "1. System → 2. Cloud → 3. legacy managed_config → 4. macOS MDM" 순으로 "lower to higher precedence"라고 적는다. 두 페이지가 같은 결론(cloud/MDM이 system보다 강함)을 다른 방향으로 서술하되, cloud와 MDM 사이 상대 순서 표현이 상충한다. **fact-checker는 이 지점을 반드시 확인할 것.**
- 사용자 설정 위치 (원문): *"Local workstations store user-level configuration at `~/.codex/config.toml`. **The CLI and IDE extension share the same configuration layers.**"*
- Managed defaults의 역할 (원문): *"Use managed defaults for standardization, not strict compliance enforcement. ... If a setting must be non-bypassable for PHI workflows, put it in requirements instead."*
- Managed defaults 우선순위 (원문): *"For managed defaults, macOS MDM managed preferences have the highest precedence, followed by system `managed_config.toml` and then the user's local `config.toml`."*

- **PHI 워크플로 설정 표 (원문 그대로 — 표 전체 보존):**

| Control | Setting | Explanation |
|---|---|---|
| Sign-in method | ChatGPT sign-in for workspace-governed PHI workflows; API key sign-in only for approved API BAA workflows. | Determines whether ChatGPT workspace controls or API organization controls apply. |
| Workspace pinning | `forced_login_method = "chatgpt"` / `forced_chatgpt_workspace_id = "<workspace-id>"` | Keeps PHI workflows inside the approved workspace when admins require ChatGPT sign-in. |
| Approval policy | `allowed_approval_policies = ["on-request", "untrusted"]` | Keeps Codex from running higher-risk actions without review. |
| Approval reviewer | `allowed_approvals_reviewers = ["user"]` | Requires the user, not an automatic reviewer, to approve actions that cross the sandbox boundary. |
| Permission profiles | `default_permissions = ":workspace"` / Allow only `:read-only` and `:workspace`. | Prevents full-device access while allowing read-only or workspace-limited work. |
| Web search | `allowed_web_search_modes = ["cached"]` | Limits search to cached results or disables it. Live web access requires an approved configuration. |
| Browser and computer-use features | Set `computer_use`, `browser_use`, `browser_use_full_cdp_access`, and `in_app_browser` to `false`. | Reduces the chance that users copy PHI into websites or desktop apps. |
| MCP servers | Leave `[mcp_servers]` empty by default; allowlist only exact, approved servers. | Disables local MCP services by default. Add only approved servers or connectors. |
| Local history and plugins | Set `[history] persistence = "none"` when required. Enable plugins or connectors only for approved groups. | Addresses local transcript retention and third-party BAA review. |

- **Starter `requirements.toml` (원문 그대로):**
> "Permission-profile allowlists require **Codex 0.138.0 or later**. Deploy this example only after every managed client runs a supported version."
```toml
# Starter requirements.toml for Codex Local use with PHI.
# Review and adapt this policy before rollout.

allowed_approval_policies = ["on-request", "untrusted"]
allowed_approvals_reviewers = ["user"]
allowed_web_search_modes = ["cached"]

default_permissions = ":workspace"

[allowed_permission_profiles]
":read-only" = true
":workspace" = true

[features]
computer_use = false
browser_use = false
browser_use_full_cdp_access = false
in_app_browser = false

[mcp_servers]
# None allowed by default.
```
> "OpenAI provides ChatGPT Enterprise and Regulated workspaces with a starter configuration ... find this starter configuration on the Codex Policies page and override it for specific RBAC groups."

- **예시 1: Google Drive 플러그인 (원문 그대로)** — *"Codex uses the `apps` configuration key for connector settings."*
```toml
# Example config.toml change for a group approved to use
# the Google Drive connector with PHI, after legal and security review.

[features]
apps = true

[apps.google_drive]
enabled = true
destructive_enabled = false
default_tools_enabled = true
default_tools_approval_mode = "prompt"

[apps.google_drive.tools."files/delete"]
enabled = false
```

- **예시 2: 로컬 GitHub 사용 (원문 그대로)**
```toml
# Example requirements.toml addition for local GitHub use.
# This doesn't enable Codex cloud. It keeps repository actions reviewable.

[rules]
prefix_rules = [
  { pattern = [{ token = "git" }, { any_of = ["push", "commit"] }], decision = "prompt", justification = "Require review before changing repository history." },
  { pattern = [{ token = "gh" }], decision = "prompt", justification = "Require review before using GitHub CLI." },
]
```

- **선택: 검증된 GitHub MCP 서버 (원문 그대로)**
```toml
# Optional: allow a vetted GitHub MCP server.
# Use the exact approved server identity for your environment.

# requirements.toml
[mcp_servers.github]
identity = { url = "https://github-mcp.example.com/mcp" }

# config.toml
[mcp_servers.github]
url = "https://github-mcp.example.com/mcp"
enabled = true
default_tools_approval_mode = "prompt"
enabled_tools = ["<approved-read-tools>", "<approved-pr-tools>"]
```

- **실무 롤아웃 7단계 (원문 제목 그대로):**
  1. **Select the approved sign-in path.**
  2. **Confirm the BAA with OpenAI.**
  3. **Enable Codex Local and define RBAC groups.** — 예시 그룹명 원문: `Codex Admin`, `Codex Users`, `Codex PHI Users`.
  4. **Deploy admin-enforced `requirements.toml` and managed defaults.**
  5. **Train users on approvals and sandbox boundaries.**
  6. **Review third-party plugins before PHI use.**
  7. **Track, review, and refresh the deployment.**

- 참고 링크 (원문): ChatGPT Healthcare and Regulated Workspace functionality (help.openai.com/…/20001069), ChatGPT for Clinicians (…/20001202), BAA for OpenAI API services (…/8660679), Codex white paper (`https://app.safebase.io/portal?itemUid=382f924d-54f3-43a8-a9df-c39e6c959958&source=search`)
- **개인 개발자 관련성: 낮음** — 의료 규제 환경 전용. 단 (a) Starter `requirements.toml`은 "보수적 기본 설정"의 훌륭한 참고 템플릿이고, (b) `[history] persistence = "none"`은 개인의 프라이버시 설정으로도 유효하며, (c) "BAA는 Codex cloud를 커버하지 않는다"는 로컬/클라우드 경계를 가장 선명하게 보여주는 문장이다.

---

### Workspace model availability (워크스페이스 모델 가용성) ★ 모델 은퇴 정보
- URL: https://learn.chatgpt.com/codex/enterprise/workspace-model-availability
- 검색: 2026-08-02 기준
- 핵심 내용: *"Model availability depends on the product surface and authentication boundary. A ChatGPT workspace model setting isn't a universal model switch for Codex in the ChatGPT desktop app, Codex CLI, IDE extension, Codex cloud, or Platform API."*

- **모델 경계 표 (원문 그대로 — 표 전체 보존):**

| Product or authentication boundary | Model access follows | Current source |
|---|---|---|
| ChatGPT workspace | The workspace plan, member access, workspace settings, and supported role permissions | ChatGPT Enterprise and Edu models and limits (`https://help.openai.com/en/articles/11165333-chatgpt-enterprise-models-limits`) |
| Codex in the ChatGPT desktop app, Codex CLI, and IDE extension with ChatGPT sign-in | Models supported by the specific client and the access available to the signed-in ChatGPT identity | Codex models (`/codex/models`) and current workspace guidance |
| Codex cloud | Models supported by hosted Codex workflows and the access available to the signed-in ChatGPT identity | Codex models (`/codex/models`) and Codex cloud (`/codex/cloud`) |
| Codex in the ChatGPT desktop app, Codex CLI, and IDE extension with API-key authentication | The OpenAI API organization and project associated with the key | Authentication (`/codex/auth`) and the OpenAI API Platform |

- **★ GPT-5.4 은퇴 (fact-check 원장 — 이 그룹에서 가장 중요한 수치·날짜, 원문 그대로):**
  > "On **August 31, 2026**, GPT-5.4 and GPT-5.4 mini retire from Codex for users signed in with ChatGPT. Update affected workspace defaults, saved model settings, managed configurations, custom agents, and scheduled tasks before then:
  > - Replace `gpt-5.4` with **`gpt-5.6-terra`** (GPT-5.6 Terra).
  > - Replace `gpt-5.4-mini` with **`gpt-5.6-luna`** (GPT-5.6 Luna).
  >
  > **The OpenAI API and Codex authenticated with your own API key aren't affected.**"
  - 모델 ID (2026-08-02 기준): `gpt-5.4`, `gpt-5.4-mini` (은퇴 예정) → `gpt-5.6-terra`, `gpt-5.6-luna` (대체). 표시명: GPT-5.6 Terra, GPT-5.6 Luna.
  - 상세: `/codex/models#deprecated-codex-models`

- 접근과 런타임 권한 분리 (원문 그대로):
  > "Model access determines whether a model is available to the authenticated user on a supported surface. Local permission profiles and managed requirements determine what an agent can do after a local run starts... **A permission profile can't grant model access. Model access also can't weaken the sandbox, approval policy, network controls, or source-system permissions that apply to a run.**"

- 모델 접근 트러블슈팅 (원문 그대로):
  - Confirm the product surface and sign-in method.
  - Confirm the ChatGPT workspace or Platform API organization and project.
  - Review the current access controls for that authentication boundary.
  - Check whether the selected local client or Codex cloud supports the model.

- 현행 소스 (원문 링크): ChatGPT Enterprise and Edu models and limits / Manage workspace settings / Role-based access control / Codex models / **Codex feature availability by plan (`/codex/pricing#feature-availability`)** / Authentication
- 제약·주의사항 (원문): *"Don't copy a model catalog or assume that a ChatGPT model-picker setting has the same effect for Codex in the ChatGPT desktop app, Codex CLI, IDE extension, Codex cloud, and the API Platform."*
- **개인 개발자 관련성: 중간** — 은퇴 날짜와 대체 모델 ID는 개인의 저장된 모델 설정·커스텀 에이전트·예약 작업에도 그대로 적용된다(ChatGPT 로그인 사용자 한정). API 키 사용자는 영향 없음.

---

### Plugin controls (플러그인 통제)
- URL: https://learn.chatgpt.com/codex/enterprise/apps-and-connectors
- 검색: 2026-08-02 기준
- 핵심 내용: *"A plugin extends ChatGPT and Codex by packaging skills and optional connectors so teams can distribute workflows and knowledge. The products share one universal plugin directory, while admins control availability and installation for their workspace."*

- **가용 표면 (원문 그대로, 반복 확인됨):**
  > "Plugins are available with ChatGPT Work on the web, and with ChatGPT Work and Codex in the ChatGPT desktop app, and through the Codex CLI plugin browser. Availability on those surfaces doesn't make plugins available in **Chat, the IDE extension, or mobile**."

- **역량 체인 표 (원문 그대로 — 표 전체 보존):**

| Layer | What it determines | Where to manage it |
|---|---|---|
| Plugin availability and installation | Whether the plugin bundle is available to the user | Workspace settings (`https://chatgpt.com/admin/settings`) for supported web and desktop surfaces; the CLI plugin browser for CLI |
| Bundled skills | Which reusable instructions the installed plugin contributes | The plugin package and Skill controls (`/codex/enterprise/skills`) |
| Connector access | Whether users can use a connector-backed capability | Workspace apps (`https://chatgpt.com/admin/ca`) and Permissions & roles (`https://chatgpt.com/admin/settings`) |
| Connector actions and permissions | Which actions users can run and when ChatGPT asks before using the connector | The connector's Action control and App permissions in Workspace apps (`https://chatgpt.com/admin/ca`) |
| Source-system authorization | Which external data and actions the authenticated identity can access | The connected service and its identity provider |
| Runtime permissions | What an agent can do after it receives data or a tool | The runtime, sandbox, and approval controls for the active surface |

- 커넥터 통제 항목 (원문 그대로):
  - Enable reviewed connectors and assign access by workspace role.
  - For connectors that support Action control, allow read-only actions or an approved custom set, including how the workspace handles newly added actions.
  - Set App permissions that determine when ChatGPT asks before using a connector.
  - Keep access within the scopes and permissions granted by each connected service and authenticated user.

- 시작 플러그인 선택 (원문 그대로): *"For a broad initial rollout, consider plugin categories teams use every day: email, calendar, and file or document systems such as **Google Drive or Notion**."* / 디렉터리: `https://chatgpt.com/apps`
  > "**Start with read actions.** Enable write actions only after reviewing the plugin's owner, each connector's requested scopes, data access, external effects, and recovery path."

- 데이터 흐름·보안 (원문 그대로):
  > "For non-synced connector use, ChatGPT processes data from Chat and deep research transiently and doesn't index it. Connectors with sync index selected connected content in advance. This indexing distinction doesn't replace normal chat-retention controls; **chats that use plugins remain available through the Compliance API.**"
  > "OpenAI's current connector guidance also documents encryption in transit and at rest, per-user authorization, role and action controls, restricted network access for chats that use plugins, and **no model training on information accessed through plugins for Business, Enterprise, and Edu customers.**"
- 플랜명: **Business, Enterprise, Edu** (플러그인 접근 정보에 대한 모델 학습 없음 — 이 3개 플랜 명시).
- MCP: *"Custom MCP servers expose these operations as tools through Model Context Protocol (MCP)."* / 로컬 MCP 구성은 `/codex/extend/mcp`.
- **개인 개발자 관련성: 낮음** — 관리자 통제 설명. 단 "플러그인은 Chat/IDE 확장/모바일에서 안 된다"와 "CLI는 자체 plugin browser로 설치한다"는 개인에게도 실용 정보.

---

### Skill controls (스킬 통제)
- URL: https://learn.chatgpt.com/codex/enterprise/skills
- 검색: 2026-08-02 기준
- 핵심 내용: *"Skills are reusable workflows made from instructions and supporting resources."* ChatGPT 워크스페이스 Skill / 로컬 파일시스템 skill / 플러그인이 패키징한 skill — 셋은 생명주기와 접근 통제가 별개다.

- **배포 모델 표 (원문 그대로 — 표 전체 보존):**

| Distribution model | Use it for | Administration boundary |
|---|---|---|
| ChatGPT workspace Skill | Sharing or installing an approved workflow through supported ChatGPT workspace features | ChatGPT workspace skill permissions and lifecycle controls |
| Local filesystem skill | Loading an installed workflow from a repository, user, administrator, or bundled system location | Filesystem distribution, local client configuration, and runtime permissions |
| Plugin | Packaging one or more skills with optional connectors, MCP servers, hooks, and presentation metadata | Plugin availability and installation, plus the separate controls for every bundled capability |

- 인용 가능한 구절 (원문 그대로):
  > "ChatGPT workspace skill distribution, local filesystem skill installation, and surface-specific plugin installation are separate paths. **Moving a skill doesn't transfer ChatGPT workspace ownership, sharing, role assignments, plugin installation state, or connector authorization.**"
  > "ChatGPT workspace controls don't install local filesystem skills or plugins. Filesystem distribution doesn't assign ChatGPT workspace ownership or roles. **Plugin installation doesn't grant access to a connector, MCP server, or connected service.** Configure each capability through the control surface that owns it."
  > "Those supported surfaces draw public plugins from **one universal directory shared by ChatGPT and Codex**."

- 소유 문서 (원문 링크): Build skills (`/codex/build-skills` — 파일시스템 위치·저작), Skills in ChatGPT (`https://help.openai.com/en/articles/20001066-skills-in-chatgpt` — 현행 워크스페이스 절차), Build plugins (`https://developers.openai.com/plugins/build/plugins` — 패키징)
- 수치·플랜명·버전: 없음.
- **개인 개발자 관련성: 중간** — 로컬 파일시스템 skill은 개인이 직접 쓰는 기능이다. 이 페이지 자체는 관리 경계만 다루므로, 실제 저작법은 `/codex/build-skills`(그룹 외)에 있다. **로컬 skill 로딩 출처 4종("a repository, user, administrator, or bundled system location")** 은 개인에게 유용한 사실.

---

### Governance (거버넌스)
- URL: https://learn.chatgpt.com/codex/enterprise/governance
- 검색: 2026-08-02 기준
- 핵심 내용: Codex 활동의 거버넌스는 인터랙티브 분석·프로그래매틱 리포팅·ChatGPT 사용 통제·감사 기록 4개 표면에 걸친다. 질문에 맞는 표면을 고르라는 라우팅 페이지.

- **표면 선택 표 (원문 그대로 — 표 전체 보존):**

| If you need to | Start with |
|---|---|
| Understand adoption across ChatGPT | Workspace analytics (`/codex/enterprise/workspace-analytics`) |
| Review Codex adoption and activity interactively | Codex analytics (`#analytics-dashboard`) |
| Load aggregated Codex reporting into another system | Analytics API (`/codex/enterprise/analytics-api`) |
| Export records for audit or investigation | Compliance API (`/codex/enterprise/compliance-api`) |
| Review plan-dependent ChatGPT workspace credit controls | ChatGPT usage limits and spend controls (`/codex/enterprise/usage-limits`) |

- 관리 콘솔 URL (원문 그대로):
  - Workspace analytics — `https://chatgpt.com/admin/usage`
  - Codex Analytics API reference (인증 필요) — `https://chatgpt.com/codex/cloud/settings/apireference`
  - Admin API reference (인증 필요) — `https://chatgpt.com/admin/api-reference`
  - Compliance Platform guide — `https://help.openai.com/en/articles/9261474-compliance-api-for-chatgpt-enterprise-edu-and-chatgpt-for-teachers`

- 예시 (원문): *"use workspace analytics for a quick adoption check, the Analytics API to load aggregated Codex reporting into a business intelligence system, and the Compliance API to send auditable records to a SIEM or electronic discovery workflow."*
- 사용 통제 (원문 그대로): *"Depending on the plan, eligible Codex activity can consume ChatGPT workspace credits, and exhausted limits can pause access to eligible features. **These controls don't set a universal Codex limit or govern Platform API billing.**"*
- 제약·주의사항 (원문): *"Don't build a durable reporting contract from dashboard labels or downloaded report fields; those can change as the product evolves."*
- 수치·엔드포인트: **구체 엔드포인트는 이 페이지에 없다.** 문서가 의도적으로 인증된 API 레퍼런스에 위임한다 — *"The authenticated API reference owns access requirements, routes, schemas, fields, reporting windows, and pagination."*
- **개인 개발자 관련성: 낮음** — 조직 리포팅 전용.

---

### Workspace analytics (워크스페이스 분석)
- URL: https://learn.chatgpt.com/codex/enterprise/workspace-analytics
- 검색: 2026-08-02 기준
- 핵심 내용: 4개 리포팅 표면의 용도와 계약 소유자를 구분한다.

- **리포팅 표면 표 (원문 그대로 — 표 전체 보존):**

| Surface | Use it for | Contract owner |
|---|---|---|
| ChatGPT workspace analytics | Interactive, workspace-wide adoption and engagement reporting | Workspace analytics Help Center guidance (`https://help.openai.com/en/articles/10875114`) |
| Codex analytics | Interactive reporting focused on Codex adoption and activity | The authenticated Codex analytics dashboard (`https://admin.openai.com/analytics/codex`) |
| Analytics API | Programmatic, aggregated Codex reporting | The authenticated Codex Analytics API reference (`https://chatgpt.com/codex/cloud/settings/apireference`) |
| Compliance API | Audit, security, legal, and investigation records | The authenticated Admin API reference (`https://chatgpt.com/admin/api-reference`) |

- 인용 가능한 구절 (원문 그대로):
  > "Treat downloaded reports as identifiable organizational data. Apply the organization's access, storage, and retention policy instead of assuming that an export has the same privacy characteristics as an aggregated dashboard."
  > "Use it for interactive exploration, **not as a stable schema contract.** Dashboard categories, fields, filters, and export formats can change independently of this page."

- 데이터 해석 경계 (원문 그대로):
  - ChatGPT workspace analytics and Codex analytics cover different product scopes.
  - Aggregated analytics and audit records serve different purposes and have separate contracts.
  - Analytics describes activity; it doesn't grant access or change runtime permissions.
  - ChatGPT usage limits and spend controls are a separate, plan-dependent workspace boundary.
- 수치·엔드포인트: 없음 (모두 Help Center·인증 대시보드에 위임).
- **개인 개발자 관련성: 낮음.**

---

### Analytics API
- URL: https://learn.chatgpt.com/codex/enterprise/analytics-api
- 검색: 2026-08-02 기준
- 핵심 내용: *"The Codex Analytics API provides aggregated Codex usage and activity metrics for a ChatGPT workspace."*
- **API 엔드포인트 (중요 — 이 페이지에는 구체 엔드포인트가 없다):**
  > "The authenticated **Codex Analytics API reference** (`https://chatgpt.com/codex/cloud/settings/apireference`) is the source of truth for current access requirements, routes, request and response schemas, metrics, time semantics, and pagination."
  > "The authenticated reference owns current key provisioning, scope requirements, routes, schemas, fields, time semantics, and pagination behavior. **This page doesn't duplicate that contract.**"
  - ⚠️ 즉 라우트·스키마는 **공개 문서에 존재하지 않으며**, 인증된 워크스페이스 레퍼런스에서만 확인 가능. 책에 엔드포인트를 적을 수 없다.

- 사용 시점 (원문 그대로):
  - Automate recurring Codex reporting.
  - Join aggregated Codex metrics with internal organizational data.
  - Build a controlled reporting layer for approved audiences.
  - Avoid coupling an integration to an interactive dashboard.

- **인증 경계 (원문 그대로 — 중요한 비대칭):**
  > "Analytics API results are scoped to a ChatGPT workspace, but requests authenticate with a **Platform organization API key**. The key's organization must match the organization associated with the workspace."

- 제약 (원문): *"It's not a raw audit-log interface. Use the Compliance API when the workflow requires auditable activity records."*
- 수치·플랜명·버전: 없음.
- **개인 개발자 관련성: 낮음** — 조직 리포팅 전용. 단 "워크스페이스 스코프 + Platform 조직 API 키"라는 혼합 인증 모델은 개념적으로 흥미로운 사실.

---

### Compliance API and audit events
- URL: https://learn.chatgpt.com/codex/enterprise/compliance-api
- 검색: 2026-08-02 기준
- 핵심 내용: 보안·법무·거버넌스·조사 워크플로용 감사 가능 기록. *"Use analytics, not compliance records, to measure adoption and trends."*
- **API 엔드포인트 (이 페이지에도 구체 엔드포인트 없음):**
  > "The authenticated **Admin API reference** (`https://chatgpt.com/admin/api-reference`) is the source of truth for current access requirements, event coverage, routes, schemas, filters, retention, and request behavior."
  > "The authenticated reference owns the current routes, event coverage, schemas, filters, retention behavior, permission requirements, and request mechanics. **This page doesn't duplicate that contract.**"
  - 개요·통합 패턴: Compliance Platform guide — `https://help.openai.com/en/articles/9261474-compliance-api-for-chatgpt-enterprise-edu-and-chatgpt-for-teachers`

- 사용 시점 (원문 그대로):
  - Export supported records into an audit or investigation system.
  - Apply organizational retention and legal-hold processes.
  - Correlate Codex activity with other security or identity data.
  - Support approved security, legal, or governance investigations.

- Get started 4단계 (원문 그대로):
  1. Open the Admin API reference and confirm that your administrator role can access the compliance resources you need.
  2. **Use the append-only compliance log stream** for ongoing collection. Check the authenticated reference for the currently supported resources and retrieval patterns.
  3. Test ingestion into a non-production security information and event management (**SIEM**) system or data lake. The Compliance Platform guide links to the current API documentation and **quickstart notebook**.
  4. Schedule continuous collection and apply your organization's access, retention, and legal-hold controls to exported records. **Don't assume the source retention window replaces your organization's retention policy.**

- 제약 (원문): *"It's not a productivity dashboard. **Don't use it to infer code quality or individual performance.**"*
- 관련 수치 (다른 페이지 교차): Compliance Logs Platform 보존 **30일** (`work-admin-faq`), ChatGPT 인증 사용 감사 기록 **최대 30일** (`hipaa-configuration`).
- **개인 개발자 관련성: 낮음** — 조직 보안팀 전용.

---

### Deploy the Windows app (Windows 앱 배포)
- URL: https://learn.chatgpt.com/codex/enterprise/windows-deployment
- 검색: 2026-08-02 기준
- 핵심 내용: ChatGPT 데스크톱 앱의 Windows 설치·배포 경로 3가지. *"The app is Store-signed, but users don't need to open the Microsoft Store to install or update it."*

- **1) 사용자 자가 설치 (개인 개발자에게 직접 해당):**
  - 웹 인스톨러: `https://get.microsoft.com/installer/download/9PLM9XGG6VKS?cid=website_cta_psi`
  - 커맨드라인 (원문 코드 그대로):
```powershell
winget install --id 9PLM9XGG6VKS -s msstore
```
  - 원문: *"Microsoft Store components may appear during installation or updates, but users don't need to browse the Store themselves."*

- **2) 엔터프라이즈 관리 도구 배포:**
  - Microsoft Intune 또는 호환 MDM/소프트웨어 배포 플랫폼
  - Store 앱 검색어: **"ChatGPT from OpenAI"**
  - **Store product ID: `9PLM9XGG6VKS`**
  - 참고 문서 (원문 링크 그대로): Enterprise deployment guide / Intune deployment guide / MECM deployment guide (모두 1drv.ms 단축 링크), Add Microsoft Store apps to Microsoft Intune (`https://learn.microsoft.com/en-us/intune/app-management/deployment/add-microsoft-store`)

- **3) Microsoft 배포 서비스 없이 설치 — MSIX 직접 다운로드 (원문 표 그대로):**

| Device architecture | Package |
|---|---|
| x64 | ChatGPT-x64.msix (`https://persistent.oaistatic.com/codex-app-prod/ChatGPT-x64.msix`) |
| Arm64 | ChatGPT-arm64.msix (`https://persistent.oaistatic.com/codex-app-prod/ChatGPT-arm64.msix`) |

  - 오프라인 라이선스 파일: `ChatGPT-License.xml` — `https://persistent.oaistatic.com/codex-app-prod/ChatGPT-License.xml`
  - 원문: *"These stable links point to the latest published Store-signed package for each architecture."*
  - 자동 업데이트 (원문): *"After the initial installation, devices that can reach **`persistent.oaistatic.com`** can install updates automatically, so you don't need to redeploy newer packages through your management tool."*
  - 이 경로의 특성 (원문 그대로):
    - Supports initial installation in restricted environments.
    - Supports x64 and Arm64 devices.
    - **Doesn't provide a standalone MSI or non-Store EXE.**

- 관련: ChatGPT desktop app for Windows (`/codex/windows/windows-app`)
- **개인 개발자 관련성: 중간** — Windows 개인 사용자에게 `winget install --id 9PLM9XGG6VKS -s msstore` 한 줄은 즉시 유용하다. 나머지(Intune·MECM·MSIX)는 IT 관리자용.

---

## 그룹 E 종합 — 이 그룹에서 건진 것

### 1) 개념적 척추: "여섯 개의 통제 경계"
`/codex/enterprise/roles-and-workspace-permissions`의 6경계 표(ChatGPT workspace / Local clients / Codex cloud / Platform API / Plugins / Connected systems)가 그룹 E 전체를 관통한다. 인용 최적 문장:
> "A request must pass every boundary that applies to it."

이 프레임은 개인 개발자에게도 "왜 로그인은 됐는데 이게 안 되지?"의 진단 체크리스트가 된다.

### 2) fact-check 원장에 올릴 수치·날짜·버전 (2026-08-02 기준)

| 항목 | 값 | 출처 URL |
|---|---|---|
| ChatGPT Work 출시일 | **July 9, 2026** | `/codex/enterprise/work-admin-faq` |
| ChatGPT Work Enterprise·Edu 프리뷰 | **2주(two-week), 웹·모바일 기본 off** | `/codex/enterprise/work-admin-faq` |
| Compliance Logs Platform 보존 | **30일** | `/codex/enterprise/work-admin-faq` |
| ChatGPT 인증 사용 감사 기록 보존 | **최대 30일** | `/codex/hipaa-configuration` |
| GPT-5.4 / GPT-5.4 mini 은퇴일 | **August 31, 2026** (ChatGPT 로그인 사용자 한정) | `/codex/enterprise/workspace-model-availability` |
| 대체 모델 ID | `gpt-5.4` → **`gpt-5.6-terra`**, `gpt-5.4-mini` → **`gpt-5.6-luna`** | `/codex/enterprise/workspace-model-availability`, `/codex/enterprise/managed-configuration` |
| 권한 프로필 허용목록 최소 버전 | **Codex 0.138.0 이상** (0.137.0 이하는 무시) | `/codex/enterprise/managed-configuration`, `/codex/hipaa-configuration` |
| access token 최단 커스텀 만료 | **1일** | `/codex/enterprise/access-tokens` |
| access token 권장 만료 | **7 / 30 / 60 / 90일** | `/codex/enterprise/access-tokens` |
| access token 지원 플랜 | **ChatGPT Business, Enterprise** | `/codex/enterprise/access-tokens` |
| CLI 로그인 콜백 포트 | **localhost:1455** | `/codex/auth` |
| Windows Store product ID | **`9PLM9XGG6VKS`** | `/codex/enterprise/windows-deployment` |
| 플러그인 미지원 표면 | **Chat, IDE extension, mobile** | admin-setup / apps-and-connectors / skills (3곳 일치) |
| 플러그인 학습 미사용 플랜 | **Business, Enterprise, Edu** | `/codex/enterprise/apps-and-connectors` |

### 3) 개인 개발자가 실제로 쓰는 명령·경로·키 (전부 `/codex/auth` 출처)
```
codex login                              # ChatGPT 브라우저 로그인
printenv OPENAI_API_KEY | codex login --with-api-key
printenv CODEX_ACCESS_TOKEN | codex login --with-access-token
codex login --device-auth                # 헤드리스 (beta)
codex login status                       # 현재 인증 방식 확인
codex logout                             # 자격증명 삭제
```
- 캐시 파일: `~/.codex/auth.json` (또는 OS 자격증명 저장소)
- `CODEX_HOME` 기본값: `~/.codex`
- 로그인 로그: `codex-login.log` (설정된 로그 디렉터리 하위)
- 설정 키: `cli_auth_credentials_store = "file" | "keyring" | "auto"`
- 환경 변수: `OPENAI_API_KEY`, `CODEX_ACCESS_TOKEN`, `CODEX_CA_CERTIFICATE`(미설정 시 `SSL_CERT_FILE` 폴백)
- SSH 포워딩: `ssh -L 1455:localhost:1455 user@remote`

### 4) fact-checker가 반드시 대조할 상충 지점 ⚠️
- **requirements 우선순위 서술 불일치:** `/codex/enterprise/managed-configuration`은 "1. System → 2. Cloud → 3. legacy → 4. macOS MDM"을 "lower to higher precedence"로 적고, `/codex/hipaa-configuration`은 "cloud-managed → macOS MDM → system `requirements.toml`" 순으로 적으며 "**Earlier** requirements take precedence"라 한다. 두 서술 모두 "system이 가장 약함"에는 동의하나, cloud와 MDM의 상대 순서 표현이 다르다. 책에 우선순위를 적는다면 **managed-configuration 페이지를 정전으로 삼고** hipaa 페이지 서술은 인용하지 말 것.
- **access token 플랜 범위 불일치:** `/codex/enterprise/access-tokens`는 "ChatGPT **Business and Enterprise**", `/codex/auth`는 "In ChatGPT **Enterprise** workspaces"라고만 적는다. 전용 페이지(access-tokens)가 더 구체적이므로 그쪽을 채택.

### 5) 수집 한계 (문서에 없어서 못 적는 것)
- **Analytics API·Compliance API의 실제 엔드포인트·스키마·필드는 공개 문서에 존재하지 않는다.** 두 페이지 모두 명시적으로 "This page doesn't duplicate that contract"라며 인증된 레퍼런스(`chatgpt.com/codex/cloud/settings/apireference`, `chatgpt.com/admin/api-reference`)로 위임한다. 책에 엔드포인트를 쓰려면 별도 확보가 필요하며, **추측으로 채우면 안 된다.**
- **역할·시트·권한의 구체 목록**도 마찬가지다. `roles-and-workspace-permissions`가 "use the Help Center for the current permission list"라고 명시적으로 위임한다. 그룹 E 문서만으로는 "Owner / Admin / Member" 3개 내장 역할(work-admin-faq 출처) 외에 확정할 수 있는 역할명이 없다.
- 플랜별 기능 가용성 매트릭스(Plus/Pro/Business/Enterprise/Edu)는 이 그룹이 아니라 `/codex/pricing#feature-availability`에 있다 — **그룹 E 범위 밖. 다른 리서처가 커버해야 한다.**

---

## 접근 실패 URL

**없음.** 17개 URL 전부 HTTP 200으로 원문 markdown(`{경로}.md`) 취득 성공.

| # | URL | 상태 | 원문 크기 |
|---|---|---|---|
| 1 | https://learn.chatgpt.com/codex/administration | 200 | 7,006 B |
| 2 | https://learn.chatgpt.com/codex/enterprise/admin-setup | 200 | 11,048 B |
| 3 | https://learn.chatgpt.com/codex/enterprise/work-admin-faq | 200 | 26,012 B |
| 4 | https://learn.chatgpt.com/codex/auth | 200 | 15,024 B |
| 5 | https://learn.chatgpt.com/codex/enterprise/access-tokens | 200 | 11,914 B |
| 6 | https://learn.chatgpt.com/codex/enterprise/groups-and-provisioning | 200 | 3,071 B |
| 7 | https://learn.chatgpt.com/codex/enterprise/roles-and-workspace-permissions | 200 | 8,039 B |
| 8 | https://learn.chatgpt.com/codex/enterprise/managed-configuration | 200 | 27,556 B |
| 9 | https://learn.chatgpt.com/codex/hipaa-configuration | 200 | 20,887 B |
| 10 | https://learn.chatgpt.com/codex/enterprise/workspace-model-availability | 200 | 5,393 B |
| 11 | https://learn.chatgpt.com/codex/enterprise/apps-and-connectors | 200 | 7,492 B |
| 12 | https://learn.chatgpt.com/codex/enterprise/skills | 200 | 3,561 B |
| 13 | https://learn.chatgpt.com/codex/enterprise/governance | 200 | 5,620 B |
| 14 | https://learn.chatgpt.com/codex/enterprise/workspace-analytics | 200 | 3,564 B |
| 15 | https://learn.chatgpt.com/codex/enterprise/analytics-api | 200 | 1,797 B |
| 16 | https://learn.chatgpt.com/codex/enterprise/compliance-api | 200 | 3,467 B |
| 17 | https://learn.chatgpt.com/codex/enterprise/windows-deployment | 200 | 3,453 B |

---

## 추가 발견 URL

### ⚡ 수집 방법 발견 (다른 리서처에게 공유 권장)
- **`https://learn.chatgpt.com/llms.txt`** — 전체 문서 색인. 모든 페이지 상단에 안내된다.
- **모든 문서 페이지는 경로에 `.md`를 붙이면 원문 markdown을 그대로 반환한다.** 예: `https://learn.chatgpt.com/codex/auth.md`. WebFetch의 요약 손실 없이 표·코드블록·설정 키를 전문 그대로 얻을 수 있다. `curl -sSL "{url}.md"` 로 직접 받는 게 가장 확실하다.
- 문서 사이트는 `?surface=app|cli|ide|web` 쿼리로 내용이 갈린다. `.md` 원문에는 `<ContentModeSwitch group="codex-surface" ids="...">` 블록이 그대로 남아 어느 표면 전용 내용인지 식별 가능하다.

### learn.chatgpt.com 내 링크 (그룹 E 목록에 없음 — 다른 그룹 담당자용)
- `/codex/permissions` — 권한 프로필 동작 (managed-configuration이 계속 참조)
- `/codex/agent-approvals-security` (+ `#network-isolation`, `#monitoring-and-telemetry`)
- `/codex/config-file/config-reference` (+ `#requirementstoml` — **requirements.toml 정식 스키마**)
- `/codex/config-file/config-basic` (+ `#feature-flags`, `#web-search-mode`)
- `/codex/config-file/config-advanced` (+ `#profiles`, `#custom-model-providers`)
- `/codex/config-file/environment-variables` (+ `#authentication-and-network`)
- `/codex/enterprise/usage-limits` — ChatGPT usage limits and spend controls (그룹 E 목록 누락, 거버넌스와 직결)
- `/codex/pricing` (+ `#feature-availability` — **플랜별 기능 가용성 매트릭스**)
- `/codex/models` (+ `#deprecated-codex-models` — 모델 은퇴 상세)
- `/codex/plugins` (+ `#api-key-availability`)
- `/codex/skills-and-plugins`, `/codex/build-skills`
- `/codex/agent-configuration/rules`
- `/codex/extend/mcp` (+ `?surface=cli`)
- `/codex/environments/cloud-environment`, `/codex/cloud`, `/codex/cloud/internet-access`
- `/codex/third-party/github`
- `/codex/non-interactive-mode`
- `/codex/auth/ci-cd-auth` — "Maintain Codex account auth in CI/CD (advanced)"
- `/codex/app-server`
- `/codex/remote-connections` (+ `#pick-up-work-from-another-device`)
- `/codex/amazon-bedrock`
- `/codex/computer-use` (+ `#locked-use`)
- `/codex/windows/windows-app`
- `/codex/security-administration`, `/codex/features`, `/codex/configuration`, `/codex/developers`, `/codex/resources`, `/codex/use-cases`
- `/workspace-agents/authentication` — Workspace Agent access tokens (Codex access token과 **다른 자격증명**)
- `/plugins`, `/workspace-agents`

### 인증 필요 관리 콘솔 (URL만 기록, 접근 불가)
- `https://chatgpt.com/admin/access-tokens` — Access tokens
- `https://chatgpt.com/admin/settings` — Workspace Settings > Permissions & roles
- `https://chatgpt.com/admin/permissions` — 권한·역할 (HIPAA 가이드가 참조)
- `https://chatgpt.com/admin/ca` — Workspace apps (커넥터 설정)
- `https://chatgpt.com/admin/usage` — Workspace analytics
- `https://chatgpt.com/admin/api-reference` — **Admin API reference (Compliance API 정전)**
- `https://chatgpt.com/codex/settings/managed-configs` — 클라우드 관리형 requirements
- `https://chatgpt.com/codex/settings/policies` — Policies (starter requirements.toml 위치)
- `https://chatgpt.com/codex/cloud/settings/apireference` — **Codex Analytics API reference (정전)**
- `https://admin.openai.com/analytics/codex` — Codex analytics dashboard
- `https://chatgpt.com/apps` — Plugins Directory

### 외부 문서 (Help Center·백서)
- `https://help.openai.com/en/articles/8266401-managing-members-seat-types-roles-and-access-in-chatgpt-enterprise` — 멤버·시트·역할 (역할 목록의 실제 정전)
- `https://help.openai.com/en/articles/11750701-rbac` — RBAC
- `https://help.openai.com/en/articles/9083985-group-permissions-in-gpts` — 그룹 관리
- `https://help.openai.com/en/articles/10011769-openai-platform-scim-integration-faq` — SCIM
- `https://help.openai.com/en/articles/8411955` — 워크스페이스 설정
- `https://help.openai.com/en/articles/11165333-chatgpt-enterprise-models-limits` — Enterprise·Edu 모델·한도
- `https://help.openai.com/en/articles/10875114` — Workspace analytics
- `https://help.openai.com/en/articles/9261474-compliance-api-for-chatgpt-enterprise-edu-and-chatgpt-for-teachers` — Compliance Platform 가이드
- `https://help.openai.com/en/articles/11509118` — Admin controls, security, and compliance in apps
- `https://help.openai.com/en/articles/11487775` — Apps in ChatGPT
- `https://help.openai.com/en/articles/10847137` — Apps with sync
- `https://help.openai.com/en/articles/12289294-admin-portal` — Global Admin Console
- `https://help.openai.com/en/articles/8983778-chat-and-file-retention-policies-in-chatgpt` — 채팅·파일 보존 정책
- `https://help.openai.com/en/articles/8983130-...` — 비즈니스 데이터 미학습
- `https://help.openai.com/en/articles/9903489-data-residency-and-inference-residency-for-chatgpt`
- `https://help.openai.com/en/articles/20001001-manage-usage-limits-and-overages-in-chatgpt-enterprise-and-edu`
- `https://help.openai.com/en/articles/20001066-skills-in-chatgpt`
- `https://help.openai.com/en/articles/20001069-chatgpt-healthcare-and-regulated-workspace-functionality`
- `https://help.openai.com/en/articles/20001202-chatgpt-for-clinicians`
- `https://help.openai.com/en/articles/8660679-how-can-i-get-a-business-associate-agreement-baa-with-openai`
- `https://trust.openai.com/?itemUid=382f924d-54f3-43a8-a9df-c39e6c959958&source=click` — **Codex security white paper**
- `https://app.safebase.io/portal?itemUid=382f924d-54f3-43a8-a9df-c39e6c959958&source=search` — Codex white paper (동일 itemUid, 다른 포털)
- `https://cdn.openai.com/business-guides-and-resources/app-security-whitepaper.pdf` — App security white paper
- `https://developers.openai.com/plugins/build/plugins` — Build plugins
- `https://platform.openai.com/api-keys`, `https://platform.openai.com/docs/overview`, `https://openai.com/api/pricing/`
- `https://learn.microsoft.com/en-us/intune/app-management/deployment/add-microsoft-store`
- `https://get.microsoft.com/installer/download/9PLM9XGG6VKS?cid=website_cta_psi`
- `https://persistent.oaistatic.com/codex-app-prod/ChatGPT-x64.msix` / `ChatGPT-arm64.msix` / `ChatGPT-License.xml`
- 워크스루 영상: `https://vimeo.com/1207482321/d1286e4467` (RBAC), `https://vimeo.com/1207484127/0f2029dd01` (spend controls)
