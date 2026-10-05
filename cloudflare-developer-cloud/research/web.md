# 웹 리서치: Cloudflare를 "나의 클라우드"로 — 앱·서비스 배포·운영 (tech-book)

- 슬러그: `cloudflare-developer-cloud`
- 대상 독자: Java·Kotlin·JS/TS·React·Next.js·Node.js 경험 개발자
- 검색 시점: **2026-10-03** (모든 항목 공통. 아래 "기준" 날짜는 각 문서 페이지의 `Last updated`/게시일)
- 수집 방법: developers.cloudflare.com 문서를 `index.md`(마크다운 원문)로 직접 수집, 공식 changelog RSS(1,306건) 전수 필터링, blog.cloudflare.com 태그 RSS(birthday-week·agents-week·developer-platform·developers·zero-trust·cloudflare-tunnel), GitHub 릴리스(`gh release list`)
- 인용 규칙: 따옴표 안은 원문 그대로(영어). 해설은 한국어. 버전·한도·가격은 "{제품} {날짜} 기준" 태그와 URL을 단다.
- 원장 용도: fact-checker는 이 파일의 인용·URL·날짜를 1차 대조 기준으로 쓴다. "[커뮤니티/3자 주장]"·"[추론]" 표기가 붙은 항목은 1차 문서로 확인되지 않은 것이다.

---

## 0. 먼저 알아둘 이벤트 명칭 정정

- 브리프는 "Developer Week (April 2026)"를 전제했지만, 블로그 태그 RSS 기준으로 **2026년에는 `developer-week` 태그 글이 없다**. 2026년 4월 중순 발표(Containers GA 4/13, VPC Networks·Mesh 4/14, Email Sending 공개 베타 4/16, Billable Usage 대시보드·Budget alerts 4/21)는 **"Agents Week 2026"** 태그로 묶여 있다(예: Mesh 글 태그 "Agents Week 2026", 2026-04-14). 2026-08-03~07에도 "Agents Week"가 한 번 더 열렸다(리뷰 글 2026-08-10).
  - 출처: https://blog.cloudflare.com/mesh/ (2026-04-14), https://blog.cloudflare.com/agents-week-review-august-2026/ (2026-08-10), 태그 RSS https://blog.cloudflare.com/tag/developer-week/rss/ (2026년 글 0건, 검색 시점 2026-10-03)
- **Birthday Week 2026**은 2026-09-28 ~ 10-02 (vinext 1.0, `cf` CLI, Containers 재구축, Observability 통합 가격, Protected Quick Tunnels, KV Instant 등).
  - 출처: https://blog.cloudflare.com/tag/birthday-week/rss/
- 본문에서 "2026년 Developer Week"라는 명칭은 쓰지 말 것. "2026년 4월 Agents Week"로 쓰는 것이 정확하다.

---

## 1. 신선도 변경 요약 (상태 변화 원장)

| # | 변경 | 날짜 | 1차 출처 |
|---|------|------|----------|
| 1 | **Next.js 공식 권장 경로가 OpenNext → vinext로 바뀜.** 문서: "Cloudflare recommends vinext as the default way to run Next.js applications on Cloudflare Workers." OpenNext는 "You maintain an existing OpenNext application that cannot yet migrate to vinext because of a compatibility gap"일 때로 격하. vinext 1.0 릴리스 2026-09-28 | 문서 2026-08-25 갱신 / 1.0 2026-09-28 | https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/ , https://blog.cloudflare.com/vinext-nextjs-on-vite/ , https://github.com/cloudflare/vinext/releases/tag/vinext%401.0.0 |
| 2 | **Pages는 신규 비권장.** Pages 문서 첫머리: "Are you sure you want to use Pages? ... It is Cloudflare's primary platform for building applications. Start new projects with Workers." | 2026-08-25 갱신 | https://developers.cloudflare.com/pages/ |
| 3 | **Workers Sites 폐기(deprecated).** "It has been deprecated in Wrangler v4, and the Cloudflare Vite plugin does not support Workers Sites. Do not use Workers Sites for new projects." | 2026-04-23 갱신 | https://developers.cloudflare.com/workers/configuration/sites/ |
| 4 | **Containers GA** (Workers Paid 전용). "Containers and Sandbox SDK are now generally available on the Workers Paid plan." | 2026-04-13 | https://developers.cloudflare.com/changelog/post/2026-04-13-containers-sandbox-ga/ |
| 5 | **Containers CPU 과금이 '활성 사용량' 기준으로 변경** | 2025-11-21 | https://developers.cloudflare.com/changelog/post/2025-11-21-new-cpu-pricing/ |
| 6 | **Queues가 Workers Free에 포함** (일 10,000 operations) | 2026-02-04 | https://developers.cloudflare.com/changelog/post/2026-02-04-queues-free-plan/ |
| 7 | **D1 Free 일일 한도 실제 강제 시작** (초과 시 쿼리 실패) | 2026-09-01 | https://developers.cloudflare.com/changelog/post/2026-09-01-d1-free-tier-limit-enforcement/ |
| 8 | **Durable Objects: 신규 네임스페이스는 SQLite 백엔드만** 생성 가능 | 2026-07-09 | https://developers.cloudflare.com/changelog/post/2026-07-09-restrict-new-kv-backed-namespaces/ |
| 9 | **SQLite-backed DO 스토리지 과금 시작** (목표일 2026-01-07, Free는 과금 없음) | 공지 2025-12-12 | https://developers.cloudflare.com/changelog/post/2025-12-12-durable-objects-sqlite-storage-billing/ |
| 10 | **Workflows에 step 과금 추가** (step·storage 과금은 "no earlier than August 10, 2026") | 2026-07-07 | https://developers.cloudflare.com/changelog/post/2026-07-07-workflows-billing-updates/ |
| 11 | **`nodejs_compat` 기본 활성화** — compatibility date `2026-08-04` 이상이면 플래그 없이 Node.js API 사용 가능 | 2026-08-04 | https://developers.cloudflare.com/changelog/post/2026-08-04-nodejs-compat-default/ |
| 12 | **Worker 크기 한도: 압축 3MB/10MB 제한 폐지 → 비압축 64 MiB (Free·Paid 동일)** | 2026-09-04 | https://developers.cloudflare.com/changelog/post/2026-09-04-increased-worker-size-limit/ |
| 13 | **서브리퀘스트 1,000 상한 폐지** → Paid 기본 10,000, `limits.subrequests`로 최대 1,000만까지. Free는 외부 50 / 내부 1,000 유지 | 2026-02-11 | https://developers.cloudflare.com/changelog/post/2026-02-11-subrequests-limit/ |
| 14 | **Worker 시작 시간 한도 400 ms → 1초** | 2025-10-10 | https://developers.cloudflare.com/changelog/post/2025-10-10-increased-startup-time/ |
| 15 | **Workers Cache(Worker 앞단 캐시) 신설** — `"cache": {"enabled": true}`. 켜면 정적 자산 요청까지 유료 요청으로 계산됨(과금 함정) | 문서 2026-09-22 갱신 | https://developers.cloudflare.com/workers/cache/ |
| 16 | **Billable Usage 대시보드 + Budget alerts** 도입 (Pay-as-you-go) | 2026-04-21 | https://developers.cloudflare.com/changelog/post/2026-04-13-billable-usage-dashboard-and-budget-alerts/ |
| 17 | **$10 Budget alert 기본 생성** (적격 Pay-as-you-go 계정, 정보성 알림, 상한 아님) | 2026-07-20 | https://developers.cloudflare.com/changelog/post/2026-06-15-budget-alerts-default-on/ |
| 18 | **Billable Usage API** (일 단위 갱신, FOCUS 호환 컬럼) | 2026-08-03 | https://blog.cloudflare.com/billable-usage-api/ |
| 19 | **Workers Logs → "Cloudflare Observability" 통합 가격** (2026-12-01부터) | 공지 2026-10-02 | https://developers.cloudflare.com/observability/pricing/ , https://blog.cloudflare.com/one-observability-platform/ |
| 20 | **Logpush 전 플랜 제공(사용량 기반 가격)** | 2026-09-30 | https://developers.cloudflare.com/changelog/post/2026-09-30-logpush-usage-based-pricing/ |
| 21 | **`@cloudflare/vitest-pool-workers` → `@cloudflare/vitest-plugin`(v1)로 이름 변경** | 2026-08-19 | https://developers.cloudflare.com/changelog/post/2026-08-19-vitest-plugin/ |
| 22 | **Miniflare v5** (`cf` CLI 대비 구성 형식 변경, breaking) | 2026-09-08 | https://developers.cloudflare.com/changelog/post/2026-09-08-miniflare-v5/ |
| 23 | **Cloudflare CLI `cf` 베타** (Cloudflare API 전체 2,900+ 명령 + Workers 개발·배포) | 2026-09-28 | https://developers.cloudflare.com/changelog/post/2026-09-28-cloudflare-cli-beta/ |
| 24 | **Worker Previews** (PR마다 격리된 프리뷰, Wrangler 4.135.0+ `wrangler preview`) | 2026-09-22 | https://developers.cloudflare.com/changelog/post/2026-09-22-worker-previews/ |
| 25 | **`wrangler deploy` 자동 구성 GA** (설정 파일 없이 프레임워크 감지, Wrangler 4.68.0+) | 2026-02-25 | https://developers.cloudflare.com/changelog/post/2026-02-25-wrangler-autoconfig-ga/ |
| 26 | **Python Workers GA** | 2026-09-21 | https://blog.cloudflare.com/python-workers-ga/ |
| 27 | **Tunnel 문서가 Cloudflare One 하위에서 독립 제품 `/tunnel/`로 분리**, 대시보드 경로 **Networking > Tunnels** | 문서 2026-09-11~30 갱신 | https://developers.cloudflare.com/tunnel/ , https://developers.cloudflare.com/changelog/post/2026-02-20-tunnel-core-dashboard/ |
| 28 | **`wrangler tunnel` 명령** (create/list/info/delete/run/quick-start) | 2026-03-19 | https://developers.cloudflare.com/changelog/post/2026-03-19-wrangler-tunnel-commands/ |
| 29 | **Protected Quick Tunnels** (`--allowed-mail`로 이메일 OTP 보호) | 2026-10-02 | https://developers.cloudflare.com/changelog/post/2026-10-02-protected-quick-tunnels/ |
| 30 | **`cloudflared proxy-dns` 제거** (2026-02-02 이후 릴리스) | 공지 2025-11-11 | https://developers.cloudflare.com/changelog/post/2025-11-11-cloudflared-proxy-dns/ |
| 31 | **`cloudflared` 32-bit Windows·Intel macOS 빌드 2027년 폐기 예정** | 공지 2026-09-18 | https://developers.cloudflare.com/changelog/post/2026-09-18-cloudflared-architecture-deprecation/ |
| 32 | **Access: strict service token 인증** — 2026-10-05 이후 생성 조직은 기본 ON(끌 수 없음) | 2026-10-02 | https://developers.cloudflare.com/changelog/post/2026-10-02-strict-service-token-authentication/ |
| 33 | **신규 Zero Trust 조직의 기본 로그인 = Cloudflare IdP** (이전 OTP) | 2026-06-18 | https://developers.cloudflare.com/changelog/post/2026-06-18-cloudflare-idp-default/ |
| 34 | **Workers 단위/계정 전체 Access 보호** (모든 Worker 기본 비공개 옵션) | 2026-08-14 | https://developers.cloudflare.com/changelog/post/2026-08-14-workers-access/ |
| 35 | **WARP Client → "Cloudflare One Client", WARP Connector → "Cloudflare Mesh node"로 개명** | 2026-04-14 | https://blog.cloudflare.com/mesh/ |
| 36 | **Browser Rendering → "Browser Run"으로 개명** (문서 경로 `/browser-run/`) | 개명 시점은 2026-04 중순 changelog 표기로 추정(§12 #12), 가격 문서 2026-04-21 갱신 | https://developers.cloudflare.com/browser-run/pricing/ |
| 37 | **Hyperdrive MySQL GA** | 2026-08-07 | https://developers.cloudflare.com/changelog/post/2026-08-07-hyperdrive-mysql-ga/ |
| 38 | **Hyperdrive ↔ 사설 DB: Workers VPC 경유가 권장 경로** | 2026-04-29 | https://developers.cloudflare.com/changelog/post/2026-04-29-hyperdrive-vpc-private-databases/ |
| 39 | **Email Sending 공개 베타** (Email Routing과 합쳐 "Cloudflare Email Service") | 2026-04-16 | https://developers.cloudflare.com/changelog/post/2026-04-16-email-sending-public-beta/ |
| 40 | **Turnstile Spin GA** (대시보드·Wrangler·AI 에이전트로 siteverify까지 배선) | 2026-08-10 | https://developers.cloudflare.com/changelog/post/2026-08-10-turnstile-spin-ga/ |
| 41 | **Workers AI 일부 대형 모델 Free 차단(403/5035)** | 2026-07-28 | https://developers.cloudflare.com/changelog/post/2026-07-28-models-require-workers-paid/ |
| 42 | **비동기 stale-while-revalidate** (Free·Pro·Business 전면 적용) | 2026-02-26 | https://developers.cloudflare.com/changelog/post/2026-02-26-async-stale-while-revalidate/ |
| 43 | **Cache Response Rules**(응답 단계 캐시 규칙), **invalidate(무효화) API** | 2026-03-24 / 2026-09-28 | https://developers.cloudflare.com/changelog/post/2026-03-24-cache-response-rules/ , https://developers.cloudflare.com/changelog/post/2026-09-28-cache-invalidation/ |
| 44 | **Placement Hints** (`placement.region = "aws:us-east-1"` 등) | 2026-01-22 | https://developers.cloudflare.com/changelog/post/2026-01-22-explicit-placement-hints/ |
| 45 | **Remote bindings GA** (로컬 dev에서 실제 D1·R2·KV 연결) | 2025-09-16 | https://developers.cloudflare.com/changelog/post/2025-09-16-remote-bindings-ga/ |
| 46 | **Workers Rate Limiting 바인딩 GA** | 2025-09-19 | https://developers.cloudflare.com/changelog/post/2025-09-19-ratelimit-workers-ga/ |
| 47 | **Workers·Containers 인바운드 TCP(`connect()` 핸들러)·gRPC — private beta** | 2026-08-03 | https://blog.cloudflare.com/grpc-workers/ |
| 48 | **Workers VPC (VPC Services/Networks) — 오픈 베타, 베타 기간 무료** | 2025-11-05 / 2026-04-14 | https://developers.cloudflare.com/workers-vpc/platform/pricing/ |
| 49 | **Analytics: 전 플랜 최소 30일 보존** | 2026-10-02 | https://developers.cloudflare.com/changelog/post/2026-10-02-30-days-analytics-on-every-plan/ |
| 50 | **Workers Builds 기본 Node.js 24.18.0** | 2026-07-30 | https://developers.cloudflare.com/changelog/post/2026-07-30-workers-builds-nodejs-24/ |

### 도구 최신 버전 (GitHub Releases, 검색 시점 2026-10-03)

| 도구 | 최신 버전 | 릴리스 일시(UTC) | 출처 |
|------|-----------|------------------|------|
| `wrangler` | **4.147.0** | 2026-10-02 | https://github.com/cloudflare/workers-sdk/releases |
| `@cloudflare/vite-plugin` | **1.62.5** | 2026-10-02 | 同上 |
| `@cloudflare/vitest-plugin` | **1.3.6** | 2026-10-02 | 同上 |
| `cloudflared` | **2026.9.3** | 2026-09-24 | https://github.com/cloudflare/cloudflared/releases |
| `@opennextjs/cloudflare` | **1.20.8** | 2026-10-02 | https://github.com/opennextjs/opennextjs-cloudflare/releases |
| `vinext` / `@vinext/cloudflare` | **1.0.1** (1.0.0은 2026-09-28) | 2026-10-01 | https://github.com/cloudflare/vinext/releases |
| `cloudflare/wrangler-action` | **v4.1.3** (v4.0.0은 2026-05-12) | 2026-09-24 | https://github.com/cloudflare/wrangler-action/releases |

- 주의: Wrangler 메이저는 여전히 **v4**(4.x)다. 문서 곳곳의 최소 버전 요구: 정적 자산 10만 파일은 "version 4.34.0 or higher", 자동 구성은 "4.68.0", Worker Previews는 "4.135.0 or later".

---

## 2. 가격·한도·과금 보호 표 (필수 섹션)

> 모든 금액은 USD. "기준" 날짜는 해당 문서의 `Last updated`. Workers Paid는 **계정당 월 최소 $5**: "The Workers Paid plan includes Workers, Pages Functions, Workers KV, Hyperdrive, and Durable Objects usage for a minimum charge of $5 USD per month for an account." (Workers Pricing 2026-10-02 기준, https://developers.cloudflare.com/workers/platform/pricing/)
> Workers Paid는 도메인 플랜(Free/Pro/Business)과 별개: "Workers Paid plan is separate from any other Cloudflare plan (Free, Professional, Business) you may have." (同上)

### 2-1. 개발자 플랫폼(Workers 계열)

| 제품 | Free 한도 | Paid 기본 포함량 | 초과 단가 | Free 초과 시 동작 | 기준·출처 |
|------|-----------|------------------|-----------|-------------------|-----------|
| **Workers 요청** | 100,000/일 (00:00 UTC 리셋) | 1,000만/월 | +$0.30/100만 | **Error 1027** (라우트별 fail open/closed 선택) | Workers Pricing 2026-10-02, Limits 2026-09-05 기준. https://developers.cloudflare.com/workers/platform/pricing/ , https://developers.cloudflare.com/workers/platform/limits/ |
| **Workers CPU** | 10 ms/호출 | 3,000만 CPU-ms/월 | +$0.02/100만 CPU-ms | 초과 시 Error 1102 "Worker exceeded resource limits" | 同上. Paid 호출당 최대 5분(기본 30초). Cron(≥1시간 간격) CPU 15분 / Queue consumer: CPU 5분(설정 가능)·벽시계 15분 — 문서 불일치, §12 #10 |
| **Workers Duration** | 과금 없음 | "No charge or limit for duration" | — | — | 同上 |
| **CPU 상한 설정 `limits.cpu_ms`** | — | 기본 30,000 → 최대 300,000 | — | 설정치 초과 시 종료 | "To prevent accidental runaway bills or denial-of-wallet attacks, configure the maximum amount of CPU time that can be used per invocation" (Workers Pricing 2026-10-02 기준) |
| **서브리퀘스트 `limits.subrequests`** | 50/호출(외부), 1,000(내부 서비스) | 10,000/호출(기본), 최대 1,000만 | 서브리퀘스트 자체는 비과금 | — | "Cloudflare does not bill for subrequests you make from your Worker." (Workers Pricing 2026-10-02), Changelog 2026-02-11 |
| **Workers 정적 자산** | 무료·무제한 (Worker 버전당 파일 20,000개, 파일당 25 MiB) | 파일 100,000개 | **$0** ("Requests to static assets are free and unlimited") | `run_worker_first` 경로는 Worker 호출로 계산 → Free 초과 시 **429** | Static Assets Billing 2026-04-23, Limits 2026-09-05 기준. https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/ |
| **Workers Cache (신규)** | 별도 가격 없음 | — | 캐시 HIT도 표준 요청 단가 | — | "When caching is enabled, every request to your Worker is charged at the standard Workers request rate, including requests that are normally free: static asset requests and worker-to-worker invocations" (Workers Cache 2026-09-22 기준) |
| **Pages** | 빌드 500/월, 동시 1빌드, 파일 20,000 | Pro 5,000 빌드 등 | Pages Functions = Workers 과금 | Functions 요청은 Workers 할당량 차감 | Pages Limits 2026-09-05 기준. https://developers.cloudflare.com/pages/platform/limits/ — **상태: 신규 비권장(§1 #2)** |
| **Workers KV** | 읽기 100,000/일, 쓰기·삭제·list 각 1,000/일, 저장 1 GB | 읽기 1,000만/월, 쓰기·삭제·list 각 100만/월, 1 GB | 읽기 $0.50/100만, 쓰기·삭제·list $5.00/100만, 저장 $0.50/GB-월 | "If you exceed any one of these limits, further operations of that type will fail with an error." | Workers Pricing 2026-10-02, KV Limits 2026-04-21 기준 |
| **D1** | 읽은 행 500만/일, 쓴 행 10만/일, 저장 5 GB(총), DB당 500 MB, DB 10개 | 읽은 행 250억/월, 쓴 행 5,000만/월, 5 GB | 읽기 $0.001/100만 행, 쓰기 $1.00/100만 행, 저장 $0.75/GB-월 | **2026-09-01부터 쿼리 실패**("Your account has exceeded D1's free tier daily row read limit...") + 이메일 알림 | Workers Pricing 2026-10-02, D1 Limits 2026-04-21, Changelog 2026-09-01. Paid DB당 10 GB(상향 불가) |
| **R2** | 10 GB-월, Class A 100만/월, Class B 1,000만/월 (Standard 스토리지만) | (Free 포함량과 동일 구조) | Standard $0.015/GB-월, Class A $4.50/100만, Class B $0.36/100만. IA: $0.01/GB-월, A $9.00, B $0.90, 조회 $0.01/GB | 이그레스 무료 / R2는 Workers Paid와 별개로 "R2 subscription"(체크아웃) 필요 — "You need a Cloudflare account with an R2 subscription." (R2 Get started). 무료 포함량 초과분은 위 단가로 과금되는 구조로 읽히나, Free 초과 시 차단 여부를 명시한 문구는 미확인 [리서치 공백] | R2 Pricing 2026-10-01 기준. https://developers.cloudflare.com/r2/pricing/ — "Cloudflare rounds up your usage to the next billing unit." |
| **Durable Objects (SQLite)** | 요청 100,000/일, Duration 13,000 GB-s/일, 읽은 행 500만/일, 쓴 행 10만/일, 저장 5 GB | 요청 100만/월, 40만 GB-s/월, 행 250억/5,000만, 5 GB-월 | 요청 $0.15/100만, Duration $12.50/100만 GB-s, 행 단가 D1과 동일, 저장 $0.20/GB-월 | Free는 **SQLite 백엔드만** 사용 가능 | Workers Pricing 2026-10-02 기준. "Duration billing charges for the 128 MB of memory your Durable Object is allocated, regardless of actual usage." |
| **Queues** | 10,000 operations/일, 보존 24시간 고정 | 100만 operations/월, 보존 기본 4일·최대 14일 | $0.40/100만 operations | — | Workers Pricing 2026-10-02, Changelog 2026-02-04. "In most cases, it takes 3 operations to deliver a message: 1 write, 1 read, and 1 delete." 64 KB 단위로 1 op |
| **Workflows** | 요청 100,000/일(Workers와 공유), CPU 10 ms, 저장 1 GB-월, steps 3,000/일 | 요청 1,000만/월, CPU 3,000만 ms, 저장 1 GB-월, steps 50만/월 | 요청 $0.30/100만, CPU $0.02/100만 ms, 저장 $0.20/GB-월, steps $0.80/10만 | Free 저장 한도 도달 시 "will throw an error" | Workflows Pricing 2026-09-21 기준. https://developers.cloudflare.com/workflows/reference/pricing/ |
| **Cron Triggers** | 계정당 5개 | 계정당 250개 | 별도 요금 없음(Workers 요청·CPU로 과금) | — | Workers Limits 2026-09-05 기준 |
| **Hyperdrive** | 쿼리 100,000/일, 설정 10개, 원본 연결 ~20 | 쿼리 무제한, 설정 25개, 원본 연결 ~100 | 추가 요금 없음(풀링·캐시 포함) | "further operations of that type will fail with an error" | Hyperdrive Pricing 2026-06-18, Limits 2026-06-09 기준 |
| **Workers AI** | 10,000 Neurons/일 | 10,000 Neurons/일 | $0.011/1,000 Neurons | "further operations will fail with an error"; 일부 모델(kimi-k2.6 등) Free는 403/5035 | Workers AI Pricing 2026-10-01 기준 |
| **AI Gateway** | 핵심 기능 무료(분석·캐싱·레이트리밋) | — | 신규(2026-09-24 이후) 로그는 Workers Logs 가격, Unified Billing 크레딧 5% 수수료 | — | AI Gateway Pricing 2026-09-24 기준 |
| **Vectorize** | 쿼리 3,000만 차원/월, 저장 500만 차원 | 쿼리 5,000만 차원/월, 저장 1,000만 차원 | 쿼리 $0.01/100만 차원, 저장 $0.05/1억 차원 | — | Vectorize Pricing 2026-04-21 기준. ※ Workers Pricing 페이지에 "Vectorize is currently only available on the Workers paid plan" 문구가 Free 컬럼 표와 공존(문서 내 불일치) |
| **Browser Run (구 Browser Rendering)** | 브라우저 10분/일, 동시 3 | 10시간/월, 동시 10(월평균) | $0.09/시간, $2.00/추가 동시 브라우저 | — | Browser Run Pricing 2026-04-21 기준. https://developers.cloudflare.com/browser-run/pricing/ |
| **Containers** | **사용 불가**(N/A) | 메모리 25 GiB-시간, vCPU 375분, 디스크 200 GB-시간 /월 | 메모리 $0.0000025/GiB-초, CPU $0.000020/vCPU-초(활성 사용분), 디스크 $0.00000007/GB-초. 이그레스: 북미·유럽 $0.025/GB(1 TB 포함), **오세아니아·한국·대만 $0.05/GB(500 GB 포함)**, 기타 $0.04/GB(500 GB) | — | Containers Pricing 2026-08-28 기준. https://developers.cloudflare.com/containers/platform/pricing/ ※ 컨테이너 앞단 Worker·DO 사용량도 별도 과금 |
| **Images** | 고유 변환 5,000/월 | 5,000 포함 | 변환 $0.50/1,000, 저장 $5/10만 장, 전송 $1/10만 장 | **신규 변환은 9422 에러, "You will not be charged for exceeding the limits in the Free plan."** | Images Pricing 2026-07-08 기준 |
| **Email Routing (수신)** | 무제한 | 무제한 | — | — | Email Service Pricing 2026-06-09 기준 |
| **Email Sending (발신, 공개 베타)** | 사용 불가(검증된 자기 주소로의 발송만 무료) | 3,000통/월 | $0.35/1,000통 | — | 同上. https://developers.cloudflare.com/email-service/platform/pricing/ |
| **Analytics Engine** | 데이터포인트 100,000/일, 읽기 쿼리 10,000/일 | 1,000만 포인트/월, 100만 쿼리/월 | $0.25/100만 포인트, $1.00/100만 쿼리 | "Currently, you will not be billed for your use of Workers Analytics Engine." | AE Pricing 2026-04-23 기준 |
| **Workers Logs (현행, ~2026-11-30)** | 20만 이벤트/일, 보존 3일 | 2,000만 이벤트/월, 보존 7일 | $0.60/100만 | — | Workers Pricing 2026-10-02 기준 |
| **Cloudflare Observability (2026-12-01~, Workers Logs·Traces·Containers 로그 등 통합)** | 수집 0.5 GB/일, 7일 보존 | 수집 50 GB/주기, 저장 12 GB-월/주기 | 수집 $0.25/GB, 저장 $0.10/GB-월 | **Free는 일 한도 도달 시 수집 중단**("Cloudflare stops ingesting new data when the account reaches its daily limit") / Paid는 "Paid usage continues automatically after an allowance is exhausted." | Observability Pricing 2026-10-02 기준. https://developers.cloudflare.com/observability/pricing/ |
| **Workers Trace Events Logpush** | 불가 | 1,000만 요청/월 | +$0.05/100만 | — | Workers Pricing 2026-10-02 기준 |
| **Logpush (일반, 전 플랜)** | 내부 내보내기 25 GB/월, 외부 25 GB/월, 변환 1 GB/월 | 同 | 내부 $0.03/GB, 외부 $0.10/GB, 변환 $0.04/GB | — | Changelog 2026-09-30 |
| **Workers VPC** | 오픈 베타 동안 무료(Workers 요금만) | — | — | — | Workers VPC Pricing 2026-09-16 기준 |
| **Service bindings** | — | 추가 요청 요금 없음(CPU는 합산) | — | — | "Requests made from your Worker to another worker via a Service Binding do not incur additional request fees." (Workers Pricing 2026-10-02) |

### 2-2. 보안·네트워크·캐시

| 제품 | Free | 유료 | 비고·기준·출처 |
|------|------|------|----------------|
| **Turnstile** | 무료, 위젯 20개, "Unlimited challenges", 위젯당 호스트명 10개, 분석 7일 | Enterprise(문의) | Turnstile Plans 2026-08-14 기준. "Turnstile can be used independently without requiring other Cloudflare services." https://developers.cloudflare.com/turnstile/plans/ |
| **Cloudflare Tunnel** | "Available on all plans" (무료) | — | Tunnel 2026-09-11 기준. 터널당 replica 최대 25개(연결 100개). https://developers.cloudflare.com/tunnel/ , https://developers.cloudflare.com/tunnel/configuration/ |
| **Quick Tunnels** | 계정 불필요, 무료 | — | 제약: "Each Quick Tunnel supports up to 200 in-flight requests. Additional requests return a 429 response." / "Quick Tunnels do not support Server-Sent Events (SSE)." (Quick Tunnels 2026-09-30 기준) |
| **Zero Trust / Access 좌석** | **[커뮤니티/3자 주장] 50 users 무료** — 공식 플랜 페이지(https://www.cloudflare.com/plans/zero-trust-services/)는 JS 렌더링으로 원문 미확보. 1차 근거로 확인된 것은 Mesh 한정 문구: "50 nodes and 50 users free" (blog/mesh, 2026-04-14) | Pay-as-you-go 좌석당 과금 [3자 자료: $7/user/월 — 미확인] | 좌석 소비 규칙(1차): "A user consumes a seat when they perform an authentication event." 서비스 토큰은 좌석을 소비하지 않는 대안으로 안내. Seat management 2026-05-01 기준 |
| **Access 계정 한도** | 앱 500, 서비스 토큰 50, IdP 50, 규칙당 이메일 1,000 | — | Account limits 2026-09-04 기준. https://developers.cloudflare.com/cloudflare-one/account-limits/ |
| **WAF – Free Managed Ruleset** | 전 플랜 제공, Free 플랜에 기본 배포 | Pro 이상: Cloudflare Managed Ruleset | "The Free Managed Ruleset is deployed by default on Free plans" (WAF Get started), WAF Managed Rules 문서. https://developers.cloudflare.com/waf/managed-rules/ |
| **Rate Limiting rules (WAF)** | **규칙 1개**, 기간 10초, 완화 10초, 필드: Path·Verified Bot, 카운팅: IP | Pro 2개 / Business 5개 / Ent 100개 | 신 버전은 별도 종량 과금 언급 없음. 구버전(종량 과금)은 "no longer available" (Rate limiting rules 문서). https://developers.cloudflare.com/waf/rate-limiting-rules/ |
| **Workers Rate Limiting 바인딩** | — | GA | `ratelimit` 바인딩. Changelog 2025-09-19 |
| **Cache Rules** | 10개 | Pro 25 / Business 50 / Ent 300 | Cache Rules 문서. https://developers.cloudflare.com/cache/how-to/cache-rules/ |
| **Tiered Cache / Smart Topology** | Free 포함 "Yes" | 同 | Generic Global·Regional·Custom 토폴로지는 Enterprise 전용. Cloud region hint는 전 플랜 무료. https://developers.cloudflare.com/cache/how-to/tiered-cache/ |
| **Cache Reserve** | 불가("A paid Cache Reserve plan is required.") | 저장 $0.015/GB-월, Class A(쓰기) $4.50/100만, Class B(읽기) $0.36/100만 | "In most cases, a Cache Reserve miss will result in both one class A and one class B operation" / 2026-09-28부터 purge 시 Cache Reserve 콘텐츠도 강제 MISS. https://developers.cloudflare.com/cache/advanced-configuration/cache-reserve/ |
| **Request body 최대 크기 (zone 플랜)** | 100 MB | Pro 100 MB / Business 200 MB / Ent 최대 5 GB(셀프서비스) | 초과 시 413. Workers Limits 2026-09-05 기준 |
| **CDN 캐시 객체 최대 크기** | 512 MB | Ent 5 GB | 同上 |

### 2-3. 과금 보호 장치 — 문서로 확인된 것 vs 아닌 것

**결론(문서 기준): 계정 단위의 "하드 지출 상한(hard spending cap)"은 Cloudflare 1차 문서 어디에도 존재하지 않는다.** 대신 아래 장치들을 조합한다.

1. **Budget alerts (Pay-as-you-go 전용)** — 이메일 알림일 뿐 상한이 아니다.
   > "Budget alerts are informational only. They do not pause or cap usage. Your monthly invoice remains the authoritative source for billing."
   — Budget alerts, 2026-05-29 기준, https://developers.cloudflare.com/billing/manage/budget-alerts/
   > "The alert is informational only. It does not cap your usage or impact your account in any way."
   > "Usage is processed once per day for the prior day's activity, so budget alerts fire the day after the threshold is reached rather than in real time."
   > "Budget alerts only consider spend on usage-based products. Recurring subscription fees, such as the Workers Paid plan fee or other monthly plan charges, are not included in the threshold calculation."
   — Changelog "Budget alerts now on by default", 2026-07-20, https://developers.cloudflare.com/changelog/post/2026-06-15-budget-alerts-default-on/ (적격 계정에 **$10 계정 단위 알림 자동 생성**, 다음 결제 주기부터 활성, 코호트 순차 적용, Enterprise 계약 제외)
2. **Billable Usage 대시보드 / 제품 사이드바 위젯** — 청구서와 같은 데이터, 일 단위. "The data comes from the same system that generates your monthly invoice, so the figures match your bill." (Changelog 2026-04-21) / 위젯은 "aligns to your billing cycle (or the current day on Free plans)" (Changelog 2026-06-04)
3. **Billable Usage API** — 프로그래밍 방식 비용 조회. "Today, usage and cost data are updated daily while we work towards providing more real time data." (blog, 2026-08-03, https://blog.cloudflare.com/billable-usage-api/) → **[추론]** 자체 "킬 스위치"(예: Cron Worker가 API를 폴링해 임계치 초과 시 라우트 해제·Worker 비활성화)를 만들 수 있는 유일한 공식 훅이지만, 데이터가 하루 지연되므로 실시간 차단은 불가. Cloudflare가 이 패턴을 문서화한 것은 아니다.
4. **Usage-based billing notifications (제품별)** — "If you are on a Professional plan or higher, you can monitor the usage of individual Cloudflare add-ons by turning on email notifications." / "The email notifications are for informational purposes only." (Usage-based billing 2026-05-29 기준, https://developers.cloudflare.com/billing/understand/usage-based-billing/)
5. **Threshold billing** — 상한이 아니라 **중간 정산 청구**다. "When your combined usage charges across all usage-based products reach a certain level during a billing cycle, Cloudflare generates a mid-cycle invoice and charges your payment method on file." / "The threshold is automatically set by Cloudflare and cannot be modified." (Threshold billing 2026-06-16 기준, https://developers.cloudflare.com/billing/threshold-billing/)
6. **Worker 단위 기술적 상한** (실질적인 '비용 브레이크')
   - `limits.cpu_ms` — "To prevent accidental runaway bills or denial-of-wallet attacks, configure the maximum amount of CPU time that can be used per invocation" (Workers Pricing 2026-10-02)
   - `limits.subrequests` — "To protect against runaway code or unexpected costs, you can also set a lower limit for both subrequests and CPU usage." (Changelog 2026-02-11, 예시 `"subrequests": 10, "cpu_ms": 1000`)
   - 레거시 Bundled 모델에서 이관된 Worker에는 50 ms CPU 한도가 자동 부여됨 (Workers Pricing 2026-10-02)
   - Durable Objects: WebSocket Hibernation API로 유휴 시 Duration 과금 중지 ("billing pauses while the Durable Object is hibernated", Optimize costs 2026-05-04)
   - Workflows: `default_retention`으로 상태 보존 기간 단축 → 저장 과금 절감 (Workflows Pricing 2026-09-21)
7. **Free 플랜에 머무르면 "청구 대신 에러"** — 문서로 확인된 제품별 동작:
   - Workers: 100,000/일 초과 → Error 1027 (라우트 fail open/closed) — Workers Limits
   - KV·Hyperdrive·Workers AI: "further operations ... will fail with an error" — 각 Pricing
   - D1: 2026-09-01부터 실패 + 이메일 — Changelog
   - Images: 9422 에러, "You will not be charged" — Images Pricing
   - Observability(2026-12-01~): Free는 수집 중단 — Observability Pricing
   - 정적 자산 `run_worker_first`: 429 — Static Assets Billing
   - **[추론]** 따라서 "절대 과금되지 않아야 하는 사이드 프로젝트"는 Workers Free에 두는 것이 사실상 유일한 하드 캡이다. 단, R2는 결제수단 등록 후 종량제로 작동하므로 Free 범위 초과 시 동작이 '차단'인지 '과금'인지 1차 문서에서 명시 문구를 확인하지 못했다 [리서치 공백].
8. **문서화된 "깜짝 청구서" 포인트 (책에서 경고할 것)**
   - Workers Cache를 켜면 평소 무료인 정적 자산 요청·Worker 간 호출까지 요청 단가로 과금 (Workers Cache 2026-09-22, Workers Pricing 각주 4)
   - "Since Cloudflare Workers runs before the Cloudflare cache, the caching of a request still incurs costs." (Workers Pricing Fine Print)
   - DO Duration은 실제 사용과 무관하게 128 MB 기준, `accept()`한 WebSocket은 연결 내내 Duration 과금 (Workers Pricing)
   - Queues: 배치·재시도마다 메시지별 operation 과금, 64 KB 초과 메시지는 여러 op (Workers Pricing)
   - D1: 인덱스 없는 풀 스캔은 반환 행이 적어도 스캔 행 전부 "rows read" (Workers Pricing D1 정의 1)
   - R2: 단위 올림 — "If you have performed one million and one operations, you will be billed for two million operations." (R2 Pricing)
   - Containers 이그레스: 한국 리전 $0.05/GB로 북미·유럽의 2배 (Containers Pricing)
   - Free/Pro/Business의 Tunnel 공개 호스트명으로 대용량 비디오 서빙은 약관상 유료 서비스 필요: "On Free, Pro, and Business plans, the service-specific terms require you to use a specific paid service to serve video and other large files." (Cloudflare One Tunnels FAQ, https://developers.cloudflare.com/cloudflare-one/faq/cloudflare-tunnels-faq/)
   - Paid 계정 Observability: "Paid usage continues automatically after an allowance is exhausted." (2026-12-01~)
9. **[커뮤니티 주장 — 1차 미확인]** "Cloudflare에 하드캡이 없어 DDoS성 트래픽으로 청구서가 커졌다"류의 사례는 이 파일의 범위 밖(커뮤니티 리서처 담당). 본 파일은 1차 문서 기준으로 "하드캡 없음"만 확정한다.

---

## 3. 독자 맞춤 갭 ① — JVM(Java/Kotlin/Spring Boot) 백엔드는 어디에 두나

### 자료 3-1: Workers 언어 지원 — JVM 없음
- 출처: https://developers.cloudflare.com/workers/languages/ (2026-07-03 기준), https://developers.cloudflare.com/workers/runtime-apis/webassembly/ (2026-04-23 기준)
- 신뢰성: 최상(공식 문서)
- 핵심: 1급 지원 언어는 JavaScript·TypeScript·Python·Rust. 그 외는 Wasm 경유. Wasm은 단일 스레드이며 WASI는 실험적.
- 인용:
  > "Workers is a polyglot platform, and provides first-class support for the following programming languages: JavaScript, TypeScript, Python Workers, Rust"
  > "Workers also supports WebAssembly ... This allows you to write Workers using programming language beyond the languages listed above, including C, C++, Kotlin, Go and more."
  > "Threading is not possible in Workers. Each Worker runs in a single thread, and the Web Worker API is not supported."
  > "WASI support is experimental on Cloudflare Workers, with only some syscalls implemented."
  > "In general, Workers supports the same set of features that are available in Google Chrome."
- 관련 섹션: "왜 Workers에 Spring Boot를 못 올리나" 도입부

### 자료 3-2: Kotlin/Wasm 현황 (JetBrains 1차)
- 출처: https://kotlinlang.org/docs/wasm-overview.html (페이지 수정 2026-09-01, 검색 시점 2026-10-03)
- 신뢰성: 최상(언어 공식 문서)
- 핵심: Kotlin/Wasm은 **Beta**. 백엔드는 Wasm-WASI 타깃 사용. Workers의 WASI 지원이 실험적이므로 Kotlin 백엔드를 Workers로 옮기는 것은 현실적 주력 경로가 아니다 **[추론]**.
- 인용:
  > "Although Kotlin/Wasm is still in Beta, Compose Multiplatform running on Kotlin/Wasm already shows encouraging performance traits."
  > "Kotlin/Wasm uses the WebAssembly System Interface (WASI) for backend applications."
- 주의: 일부 2026년 3자 요약은 "Kotlin/Wasm stable"이라 하나 1차 문서는 Beta로 표기 — 1차를 따른다.

### 자료 3-3: Java → Wasm(TeaVM) on Workers 실험 (구버전 정보일 수 있음)
- 출처: https://dev.to/gmitch215/java-on-cloudflare-workers-2njh — Gregory Mitchell, 2024-08-31
- 신뢰성: 중(개인 블로그, 2년 경과)
- 핵심: TeaVM 기반 "bytebox"로 Java를 Wasm으로 컴파일해 Workers에서 실행. 스레드·동적 클래스 로딩 불가, Spring 같은 프레임워크는 대상 아님.
- 인용:
  > "It uses TeaVM to compile Java into WebAssembly usable by the Cloudflare Workers runtime."
  > "`java.util.concurrent` and other threading operations are not included and will result in a compilation error."
- 주의: 글이 언급하는 "3 MiB after gzip" 크기 제한은 **2026-09-04에 폐지**(현재 비압축 64 MiB) — 구버전 정보.

### 자료 3-4: Cloudflare Containers — Spring Boot의 현실적 착지점
- 출처: https://developers.cloudflare.com/containers/ (2026-09-30), https://developers.cloudflare.com/containers/platform/limits/ (2026-09-30), https://developers.cloudflare.com/containers/faq/ (2026-10-02), https://developers.cloudflare.com/containers/get-started/ , Changelog 2026-04-13(GA)
- 신뢰성: 최상
- 핵심: Workers Paid 전용·GA. 컨테이너 인스턴스마다 Durable Object가 붙고 Worker 코드가 수명주기를 제어. 이미지 요건은 `linux/amd64`. 콜드 스타트 1~3초. 내장 오토스케일링 없음(`getRandom` 헬퍼로 무상태 분산).
- 인용:
  > "Run code written in any programming language, built for any runtime, as part of apps built on Workers."
  > "Your container image must be able to run on the `linux/amd64` architecture, but aside from that, has few limitations."
  > "Container cold starts can often be in the 1-3 second range, but this is dependent on image size and code execution time, among other factors."
  > "Is built-in autoscaling for stateless applications available? Not today, though Cloudflare plans to add built-in autoscaling in a future release."
  > "Memory and disk usage are based on the *provisioned resources* for the instance type you select, while CPU usage is based on *active usage* only."
- 인스턴스 타입(2026-09-30 기준): lite 1/16 vCPU·256 MiB·2 GB / basic 1/4·1 GiB·4 GB / standard-1 1/2·4 GiB·8 GB / standard-2 1·6 GiB·12 GB / standard-3 2·8 GiB·16 GB / standard-4 4·12 GiB·20 GB. 커스텀: vCPU 1~4, 메모리 최대 12 GiB, "Minimum 3 GiB memory per vCPU". 계정 동시 한도: 메모리 6 TiB·vCPU 1,500·디스크 30 TB, 이미지 저장 50 GB.
- 2026 변화: Docker Hub 이미지(2026-03-24), Google Artifact Registry(2026-07-01), SSH(2026-03-12, 2026-05-12부터 기본 ON), `exec()`(2026-06-18), R2 FUSE 마운트(2025-11-21), 스냅샷(2026-09-30), `durable_object` 스케줄링 정책으로 런타임 이미지·인스턴스 선택 + "starts Containers more than 6x faster"(blog 2026-09-30, https://blog.cloudflare.com/faster-agent-sandboxes/).
- **[추론] Spring Boot 적합성**: 공식 문서에 "Spring Boot" 언급은 없다. 문서화된 사실(임의 언어 이미지, linux/amd64, 1~3초 콜드 스타트, 메모리는 프로비저닝 기준 과금)로부터 추론하면, JVM 힙을 고려해 `standard-1`(4 GiB) 이상이 무난하고, 콜드 스타트를 줄이려면 sleep 타임아웃 정책과 CRaC/GraalVM 네이티브 이미지 같은 JVM 측 최적화를 검토해야 한다. 상시 가동 시 월 비용은 메모리 프로비저닝분이 지배적이다 — 저자가 계산 예시로 검증할 것.
- 보안 이력: 2026-09-04 보고된 Containers 교차 테넌트 잔여 디스크 블록 노출 취약점 — 수정 완료, 악용 증거 없음. "a customer with a Workers Paid account could recover residual disk blocks previously used by Containers on the same host" (blog 2026-09-24, https://blog.cloudflare.com/containers-cross-tenant-vulnerability/)
- 관련 섹션: JVM 백엔드 장, 비용 장

### 자료 3-5: 인바운드 TCP·gRPC (private beta)
- 출처: https://blog.cloudflare.com/grpc-workers/ (2026-08-03, Mar Witek·Thomas Rubini)
- 신뢰성: 최상(공식 블로그) — 단 private beta
- 인용:
  > "connect(socket) — a new handler in the Workers runtime that lets your Worker directly accept an inbound TCP socket provided by Spectrum"
  > "Full-duplex, bidirectional gRPC from Cloudflare Containers — forward the socket from your Worker to your gRPC server running in a container"
  > "We're introducing this in private beta"
- 관련 섹션: Spring gRPC 서비스 이전 시나리오(전망으로만 언급)

### 자료 3-6: JVM을 Cloudflare 밖에 두는 정석 — Tunnel·Workers VPC·Hyperdrive·Placement
- 출처: https://developers.cloudflare.com/tunnel/ (2026-09-11), https://developers.cloudflare.com/workers-vpc/ (2026-09-18), https://developers.cloudflare.com/hyperdrive/ , Changelog 2026-04-29, 2026-01-22
- 신뢰성: 최상
- 핵심 패턴:
  1. **Tunnel로 VPS·홈서버·타 클라우드의 Spring Boot를 공개** — "Map public hostnames to local services (for example, `app.example.com` to `http://localhost:8080`)." / "Traffic flows through Cloudflare's network to your origin, with full CDN and security applied."
  2. **Workers VPC로 Worker → 사설 Spring API 호출** — "Workers VPC allows you to connect your Workers to your private APIs, services, and databases in external clouds (AWS, Azure, GCP, on-premise, and others) that are not accessible from the public Internet." / "While in beta, Workers VPC is available for free to all Workers plans."
  3. **Placement Hints로 Worker를 기존 클라우드 리전 옆에서 실행** — `"placement": { "region": "aws:us-east-1" }` / "Placement hints support Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure region identifiers."
  4. **Hyperdrive로 외부 Postgres/MySQL 공유** — §8 참조.
- 관련 섹션: 하이브리드 아키텍처 장

---

## 4. 독자 맞춤 갭 ② — Next.js·React·Node.js on Cloudflare

### 자료 4-1: Next.js 공식 권장 = vinext (OpenNext는 유지보수 경로)
- 출처: https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/ (2026-08-25 기준), https://developers.cloudflare.com/workers/framework-guides/web-apps/opennext/ (2026-08-25 기준)
- 신뢰성: 최상
- 인용:
  > "Cloudflare recommends vinext as the default way to run Next.js applications on Cloudflare Workers. vinext gives you two starting points: scaffold a new Workers-ready app with `create-vinext-app`, or add vinext to an existing Next.js 16 app with a single non-destructive `vinext init` (your existing `next dev` keeps working)."
  > "vinext is a Vite plugin that reimplements the Next.js API surface."
  > "vinext is in beta. Before adopting it for an existing production application, run the compatibility check from your project directory" (`npx vinext check`)
  > (OpenNext 페이지) "Cloudflare recommends vinext instead of OpenNext for new Next.js applications on Cloudflare Workers. Use this guide to maintain an existing OpenNext application. Migrate to vinext when compatibility allows."
- 기능표(vinext, 2026-08-25 문서): App Router·Pages Router·RSC·Server Actions·SSR·SSG/static export·ISR·middleware/`proxy.ts` 지원, `next/*` "Mostly supported", Image optimization "Partially supported".
- OpenNext 기능표: `"use cache"`(Composable Caching)·PPR "Supported"(Next.js 실험 기능), "Node.js in Middleware — Not yet supported".
- **문서 간 불일치 주의**: 문서(2026-08-25)는 vinext를 "beta"라 하지만 **vinext 1.0.0이 2026-09-28 릴리스**됨. 책에서는 "1.0 출시(2026-09-28), 공식 가이드는 갱신 전 beta 표기"로 쓰는 것이 안전.
- 관련 섹션: Next.js 장

### 자료 4-2: Vinext 1.0 발표 (Birthday Week 2026)
- 출처: https://blog.cloudflare.com/vinext-nextjs-on-vite/ — James Anderson, Matt "TK" Taylor, 2026-09-28
- 신뢰성: 최상
- 인용:
  > "When we launched Vinext in February, it was the result of an audacious week-long AI-driven experiment"
  > "Vinext lets you take any Next.js application, whether it was built for the Pages or App Router, and make it portable to be deployed to any web platform, including the Cloudflare Workers free plan, Netlify, or AWS Lambda."
  > "Our test compatibility has risen to more than 99%, excluding cache components."
  > "Vinext today has limited support for the "use cache" directive that drives Cache Components"
  > "We also run the Next.js end-to-end test suite against Vinext nightly"
- GitHub 1.0.0 릴리스 노트: "Init: default Cloudflare projects to cf", "replace deploy prerendering with cache warming", "rename cdnAdapter to workersCacheCdnAdapter" (https://github.com/cloudflare/vinext/releases/tag/vinext%401.0.0, 2026-09-28)
- 관련 섹션: Next.js 장 — `"use cache"`에 의존하는 앱이면 당분간 OpenNext 유지가 합리적일 수 있다는 판단 근거

### 자료 4-3: React/Next.js 보안 이슈와 어댑터 대응
- 출처: https://developers.cloudflare.com/changelog/post/2026-05-06-react-nextjs-vulnerabilities/ (2026-05-07)
- 신뢰성: 최상
- 인용:
  > "Patched versions are available for React (`react-server-dom-webpack`, `react-server-dom-parcel`, and `react-server-dom-turbopack` `19.0.6`, `19.1.7`, and `19.2.6`) and Next.js (`15.5.16` and `16.2.5`)."
  > "Vinext's latest release is not vulnerable to any of the disclosed CVEs."
  > "Several of the disclosed vulnerabilities are not possible to block in WAF. We strongly recommend updating your applications so they are not purely reliant on WAF mitigations."
- 관련 섹션: 보안 장 — "WAF는 패치를 대체하지 않는다"

### 자료 4-4: React SPA / Vite — `@cloudflare/vite-plugin`
- 출처: https://developers.cloudflare.com/workers/vite-plugin/ (2026-09-30), https://developers.cloudflare.com/workers/framework-guides/web-apps/react/
- 신뢰성: 최상
- 인용:
  > "Your Worker code runs inside workerd, matching the production behavior"
  > "Official support for TanStack Start and React Router v8 with server-side rendering"
  > "Produces standard Build Output for `cf build` and `cf deploy`"
  > (React 가이드) "`assets.not_found_handling` is set to `single-page-application`, which means that routes that are handled by your React SPA do not go to the Worker, and are thus free."
- 2025-12-08 Changelog: "Wrangler config is optional when using Vite plugin"
- 관련 섹션: 첫 배포(정적 사이트 → SPA) 장

### 자료 4-5: Node.js 호환 — 2026-08-04부터 기본 ON
- 출처: https://developers.cloudflare.com/workers/runtime-apis/nodejs/ (2026-08-12 기준), Changelog 2026-08-04
- 신뢰성: 최상
- 인용:
  > "For compatibility dates of `2026-08-04` or later, Workers enables both `nodejs_compat` and `nodejs_compat_v2` by default."
  > "For compatibility dates from `2024-09-23` through `2026-08-03`, add the `nodejs_compat` compatibility flag"
  > "npm packages that depend on these APIs will work without additional configuration." (`node:crypto`, `node:buffer`, `node:stream`, `node:net`, `node:dns`, `node:fs`, `node:http` 등)
  > "As polyfill shim implementations that Wrangler adds to your Worker's code, allowing it to import the module, but calling API methods will throw errors."
  > 끄기: `"compatibility_flags": ["no_nodejs_compat", "no_nodejs_compat_v2"]`
- 관련: 모듈 레지스트리 재작성 (blog 2026-09-09, https://blog.cloudflare.com/workers-module-registry-nodejs/)

### 자료 4-6: Hono / Python Workers GA
- 출처: https://developers.cloudflare.com/workers/framework-guides/web-apps/more-web-frameworks/hono/ , https://blog.cloudflare.com/python-workers-ga/ (2026-09-21), Changelog 2026-09-02 "Python Workers now support WSGI web frameworks like Django and Flask", 2026-09-08 "Python 3.14 for Python Workers", 2026-08-03 "Python and JavaScript Workers can now call each other via RPC"
- 신뢰성: 최상
- 관련 섹션: API 서버 장(Hono), 언어 선택 부록

### 자료 4-7: Pages → Workers 마이그레이션
- 출처: https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/
- 신뢰성: 최상
- 인용:
  > "Like Pages, requests for static assets on Workers are free, and Pages Functions invocations are charged at the same rate as Workers, so you can expect a similar cost structure"
  > "Unlike Pages, Workers has a distinctly broader set of features available to it, (including Durable Objects, Cron Triggers, and more comprehensive Observability)."
  > `functions/` 폴더는 `npx wrangler pages functions build --outdir=./dist/worker/`로 단일 Worker로 컴파일
- 관련 섹션: 기존 Pages 사용자용 박스

---

## 5. 독자 맞춤 갭 ③ — 인증·보안

### 자료 5-1: Access JWT 검증 (`Cf-Access-Jwt-Assertion`)
- 출처: https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/validating-json/ (2026-05-06 기준)
- 신뢰성: 최상
- 인용:
  > "When Cloudflare sends a request to your origin, the request will include an application token as a `Cf-Access-Jwt-Assertion` request header."
  > "We recommend validating the `Cf-Access-Jwt-Assertion` header instead of the `CF_Authorization` cookie, since the cookie is not guaranteed to be passed."
  > "The public key for the signing key pair is located at `https://<your-team-name>.cloudflareaccess.com/cdn-cgi/access/certs`"
  > "By default, Access rotates the signing key every 6 weeks. ... Previous keys remain valid for 7 days after rotation"
- 공식 예제 언어: Go·Python·JavaScript(Node.js) — **Java/Kotlin(Spring Security) 예제는 공식 페이지에 없음** → 저자가 JWKS 기반 Spring Security Resource Server 설정 예시를 직접 작성해야 함 [리서치 공백: 1차 Java 예제 없음].
- 관련 섹션: Spring Boot 앞에 Access 붙이기

### 자료 5-2: Workers에서 Access — `ctx.access` (JWT 파싱 불필요)
- 출처: https://developers.cloudflare.com/workers/configuration/cloudflare-access/ (2026-08-18 기준), Changelog 2026-08-14, 2025-10-03, blog https://blog.cloudflare.com/workers-protected-by-access/ (2026-08-14)
- 신뢰성: 최상
- 인용:
  > "the Worker can read the signed-in user's identity — including email, groups, device posture, and more identity fields — through `ctx.access`. No extra configuration or JWT parsing is required."
  > "`ctx.access` is `undefined` if Access did not authenticate the request."
  > "Cloudflare Access does not propagate `ctx.access` through Service Binding HTTP requests or remote procedure call (RPC) invocations."
  > "Workers with Static Assets execute behind an internal router Worker. Access still protects the application and its assets. However, the router does not pass `ctx.access` to the user Worker."
  > (Changelog 2026-08-14) "Make all Workers private by default, so every existing and newly created Worker requires sign-in before anyone can reach it."
  > (Changelog 2025-10-03, 구 방식) "To fully secure your application, it is important that you validate the JWT that Cloudflare Access adds to the `Cf-Access-Jwt-Assertion` header on the incoming request." (jose 패키지 예제)
- 로컬 테스트: `wrangler.jsonc`의 `"access": { "dev": { "aud": "my-app", "identity": {...} } }`
- 관련 섹션: 사내 도구/관리자 페이지 보호

### 자료 5-3: 서비스 토큰 (머신 간 인증)
- 출처: https://developers.cloudflare.com/cloudflare-one/access-controls/service-credentials/service-tokens/ , Changelog 2026-10-02(strict), 2026-08-25(rotation grace period·일시 비활성), 2026-09-22(비활성 토큰 자동 관리), 2026-08-26(스캔 가능한 시크릿 형식)
- 신뢰성: 최상
- 인용:
  > 헤더: `CF-Access-Client-Id: <CLIENT_ID>` / `CF-Access-Client-Secret: <CLIENT_SECRET>`
  > 단일 헤더 대안: `Authorization: {"cf-access-client-id": "...", "cf-access-client-secret": "..."}` — "useful for authenticating SaaS services that only support sending one custom header"
  > (strict) "If authentication or authorization fails, Access always returns `401` or `403` instead of redirecting the client to the login page with `302`." / "Only Service Auth policies can authorize the request." / "Zero Trust organizations created on or after October 5, 2026 have strict service token authentication turned on by default and cannot turn it off."
- 계정 한도: 서비스 토큰 50개 (Account limits 2026-09-04). 좌석 절약: Seat management 문서가 서비스 토큰을 좌석 비소비 대안으로 안내.
- 관련 섹션: CI·백엔드 간 호출 보호

### 자료 5-4: IdP 연동 (Google·GitHub·Okta·OIDC)
- 출처: https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/ (2026-06-19 기준), Changelog 2026-06-18
- 신뢰성: 최상
- 인용:
  > "When you create a new Zero Trust organization, Cloudflare automatically configures the Cloudflare identity provider as your default login method."
  > "You can also send a one-time PIN (OTP) to approved email addresses. No configuration needed"
  > "If they support OIDC or OAuth, select the generic OIDC"
  > "Cloudflare One supports social identity providers that do not require administrator accounts, open source providers, and corporate providers."
- Auth0/Clerk: 전용 페이지 대신 generic OIDC 경로 **[추론: 1차 문서에서 Clerk 전용 가이드 미확인]**
- Terraform 리소스: `cloudflare_zero_trust_access_identity_provider`
- 관련 섹션: 팀 로그인 설계

### 자료 5-5: Turnstile (봇 방지, 무료)
- 출처: https://developers.cloudflare.com/turnstile/plans/ (2026-08-14), Changelog 2026-08-10 (Spin GA)
- 신뢰성: 최상
- 인용:
  > "Turnstile setup has two parts: embed the widget in your frontend, then call siteverify from your backend. Without the second part, the widget appears on the page but does not protect the request."
  > "The Turnstile dashboard flags existing widgets with no matching siteverify traffic."
  > (Plans) Free: "Up to 20 widgets", "Unlimited challenges", "10 hostnames per widget"
- 관련 섹션: 가입·로그인 폼 보호

### 자료 5-6: mTLS / API Shield
- 출처: https://developers.cloudflare.com/ssl/client-certificates/ (2026-09-08), https://developers.cloudflare.com/api-shield/ (2026-08-19)
- 신뢰성: 최상
- 인용:
  > "Each zone allows up to **100 active client certificates** by default."
  > "BYOCA certificates: Available on Enterprise accounts."
  > (API Shield) "Enterprise-only paid add-on" / "Anyone can set up Mutual TLS with a Cloudflare-managed certificate authority."
  > Workers 필드: "New RFC 9440 mTLS certificate fields in Workers" (Changelog 2026-03-27)
- 관련 섹션: 모바일·IoT 클라이언트 인증, "API Shield는 개인 개발자 범위 밖"

### 자료 5-7: WAF·Rate Limiting (무료 범위)
- 출처: https://developers.cloudflare.com/waf/managed-rules/ , https://developers.cloudflare.com/waf/get-started/ , https://developers.cloudflare.com/waf/rate-limiting-rules/ , https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/
- 신뢰성: 최상
- 인용:
  > "Cloudflare Free Managed Ruleset: Available on all Cloudflare plans. Provides protection against high-impact and widely exploited vulnerabilities."
  > "Users on the Free plan have access to the Cloudflare Free Managed Ruleset, a subset of the Cloudflare Managed Ruleset. The Free Managed Ruleset is deployed by default on Free plans"
  > Rate limiting rules Free: 규칙 1개, 카운팅 기간 10초, 완화 10초, 표현식 필드 "Path, Verified Bot"
  > (Workers 바인딩 GA, 2025-09-19) "The `ratelimit` binding is now stable and recommended for all production workloads."
- 관련 섹션: 무료 플랜 보안 기본값

---

## 6. 독자 맞춤 갭 ④ — Cloudflare One(Zero Trust): 1인·소규모 팀이 무료로 쓸 수 있는 것

### 자료 6-1: 좌석 모델과 무료 좌석 수
- 출처: https://developers.cloudflare.com/cloudflare-one/team-and-resources/users/seat-management/ (2026-05-01 기준), https://blog.cloudflare.com/mesh/ (2026-04-14), 플랜 페이지 https://www.cloudflare.com/plans/zero-trust-services/ (JS 렌더링, 본문 미확보)
- 신뢰성: 좌석 규칙=최상 / 무료 50명=**[커뮤니티/3자 주장]**(costbench.com 등 2026 3자 집계) + Mesh 한정 1차 문구
- 인용:
  > "Cloudflare One subscriptions consist of seats that active users in your account consume. Active users are added to Cloudflare One through any authentication event."
  > "A user who authenticates will hold their seat until you remove the user from your account. By default, inactive users will not be automatically removed"
  > (Mesh 블로그) "50 nodes and 50 users free. Your whole team and your whole staging environment on one private network, included with every Cloudflare account."
- 주의: Mesh 문구는 Mesh(사설 네트워킹)에 대한 것이므로 Access/Gateway 전체의 무료 좌석 수로 일반화하지 말 것. 책에서 "50명 무료"를 쓰려면 저자가 대시보드(Zero Trust > Settings > Cloudflare One plan)에서 직접 확인 필요.
- 관련 섹션: Zero Trust 장 도입

### 자료 6-2: 2026 명칭 변경 — Cloudflare One Client, Mesh
- 출처: https://blog.cloudflare.com/mesh/ (2026-04-14, Agents Week 2026)
- 신뢰성: 최상
- 인용:
  > "WARP Connector (now called a Cloudflare Mesh node) and WARP Client (now called Cloudflare One Client)"
  > "Get started Cloudflare Mesh: Head to Networking > Mesh in the Cloudflare dashboard. Free for up to 50 nodes and 50 users."
- 관련 섹션: 용어 표기(책 전체 통일: "WARP"는 구명칭으로 괄호 병기)

### 자료 6-3: 유료 애드온 경계 — Browser Isolation, DLP
- 출처: https://developers.cloudflare.com/cloudflare-one/remote-browser-isolation/ (2026-09-30 기준), https://developers.cloudflare.com/ai-gateway/reference/pricing/ (2026-09-24 기준)
- 신뢰성: 최상
- 인용:
  > "Remote browser isolation is available as an add-on to Zero Trust Pay-as-you-go and Enterprise plans."
  > (AI Gateway DLP) "Accounts without a Zero Trust subscription have access to two predefined DLP profiles: Financial Information and Social / Insurance / National Identifier Numbers."
- CASB 무료 범위: [리서치 공백] — 1차 문서에서 Free 플랜 CASB 통합 수 한도 미확인
- 관련 섹션: "무료로 되는 것/안 되는 것" 표

### 자료 6-4: Access 운영 한도와 신규 기능 (2026)
- 출처: https://developers.cloudflare.com/cloudflare-one/account-limits/ (2026-09-04), Changelog 2026-01-22 (Require Access protection), 2026-03-20 (Managed OAuth), 2026-04-15 (Independent MFA)
- 신뢰성: 최상
- 인용:
  > (Require Access protection) "When enabled, traffic to any hostname that does not have a matching Access application is automatically blocked." / "This deny-by-default approach prevents accidental exposure of internal resources to the public Internet."
- 한도: 앱 500, 규칙당 이메일 1,000, IdP 50, 서비스 토큰 50, Gateway DNS/HTTP/Network 정책 각 500, 리스트 100(Standard 항목당 1,000)
- 관련 섹션: "실수로 내부 도구를 공개하지 않기"

### 자료 6-5: Tunnel 호스트명 라우팅(사설) — 전 Cloudflare One 무료
- 출처: https://developers.cloudflare.com/changelog/post/2025-09-18-tunnel-hostname-routing/ (2025-09-18), blog https://blog.cloudflare.com/tunnel-hostname-routing/
- 신뢰성: 최상
- 인용:
  > "You can now route private traffic to Cloudflare Tunnel based on a hostname or domain, moving beyond the limitations of IP-based routing. This new capability is **free for all Cloudflare One customers**."
  > "Precise Egress Control: Route traffic for public hostnames (e.g., `bank.example.com`) through a specific Tunnel to enforce a dedicated source IP, solving the IP allowlist problem for third-party services."
- 관련 섹션: 사설 네트워크 접근, 고정 출구 IP가 필요한 외부 API 연동(§9)

---

## 7. 독자 맞춤 갭 ⑤ — Cloudflare Tunnel (`cloudflared`)

### 자료 7-1: 제품 개요·무료·HA
- 출처: https://developers.cloudflare.com/tunnel/ (2026-09-11), https://developers.cloudflare.com/tunnel/configuration/ (검색 시점 2026-10-03)
- 신뢰성: 최상
- 인용:
  > "Available on all plans"
  > "Instead of exposing a public IP, you install a lightweight daemon called `cloudflared` on your server."
  > "Each tunnel maintains four long-lived connections to two Cloudflare data centers for built-in redundancy."
  > "A replica is an additional `cloudflared` instance that points to the same tunnel. Each replica creates four new connections ... You can run up to 25 replicas (100 connections) per tunnel. Traffic routes to the geographically closest replica."
  > "This documentation covers Cloudflare Tunnel use cases for public applications. For VPN replacement, private network access, and network traffic filtering, refer to the Cloudflare One Tunnel documentation."
- 관련 섹션: Tunnel 장 개요

### 자료 7-2: 원격 관리(권장) vs 로컬 관리
- 출처: https://developers.cloudflare.com/tunnel/features/locally-managed-tunnels/ (2026-09-11), https://developers.cloudflare.com/tunnel/get-started/ (2026-09-30), https://developers.cloudflare.com/tunnel/reference/tunnel-tokens/
- 신뢰성: 최상
- 인용:
  > "Cloudflare recommends creating a remotely-managed tunnel for most use cases. Remotely-managed tunnels store their configuration on Cloudflare, which allows you to manage the tunnel from any machine using the dashboard, API, or Terraform."
  > "Locally-managed tunnels are intended for specific scenarios such as local development, testing, or legacy configurations."
  > "A remotely-managed tunnel only requires a token to run. Anyone with the token can run the tunnel."
- 원격 관리 생성: 대시보드 **Networking > Tunnels > Create Tunnel**, 또는 API `POST /accounts/$ACCOUNT_ID/cfd_tunnel` + `"config_src": "cloudflare"`, 라우트 종류 "Published application"(공개 호스트명 → 로컬 서비스 URL)
- 로컬 관리 흐름: `cloudflared tunnel login` → `cloudflared tunnel create <NAME>` → `~/.cloudflared/config.yml`(`credentials-file: /root/.cloudflared/<Tunnel-UUID>.json`, ingress 규칙) → `cloudflared tunnel route dns <UUID or NAME> <hostname>` → `cloudflared tunnel run <UUID or NAME>`
- 관련 섹션: Tunnel 장 실습

### 자료 7-3: 서비스·Docker·Kubernetes 운영
- 출처: https://developers.cloudflare.com/tunnel/features/locally-managed-tunnels/as-a-service/linux/ , https://developers.cloudflare.com/tunnel/reference/run-parameters/ (2026-09-11), https://developers.cloudflare.com/tunnel/guides/kubernetes/ (2026-09-11), https://developers.cloudflare.com/tunnel/downloads/ (2026-09-11)
- 신뢰성: 최상
- 인용·사실:
  - Linux 서비스: `sudo cloudflared service install` → `systemctl start cloudflared`; 원격 관리는 `ExecStart=/usr/local/bin/cloudflared tunnel ... run --token <TOKEN VALUE>`
  - 토큰 환경변수: `cloudflared tunnel run --token <TUNNEL_TOKEN>` ↔ `TUNNEL_TOKEN`, `--token-file <PATH>` ↔ `TUNNEL_TOKEN_FILE`
  - Docker: "A Docker image of `cloudflared` is available on DockerHub" (`cloudflare/cloudflared`)
  - Kubernetes 예시: `replicas: 2`, `image: cloudflare/cloudflared:latest`, 명령 `cloudflared tunnel --no-autoupdate --loglevel info --metrics 0.0.0.0:2000 run`
  > "We do not recommend using `cloudflared` in autoscaling setups because downscaling (removing replicas) will break existing user connections to that replica. Additionally, `cloudflared` does not load balance across replicas; replicas are strictly for high availability."
  - Windows: "Instances of `cloudflared` do not automatically update on Windows."
  - 지원 정책: "Cloudflare supports versions of `cloudflared` that are within one year of the most recent release."
- **문서 간 미묘한 차이**: Configuration 페이지 "Traffic routes to the geographically closest replica" vs Kubernetes 페이지 "does not load balance across replicas; replicas are strictly for high availability" — 두 문장은 양립(가까운 replica로 라우팅되지만 부하분산 목적은 아님). 책에서는 "HA용이지 LB용이 아니다"로 정리.
- 관련 섹션: 운영(HA·업데이트) 절

### 자료 7-4: 연결 사전 점검(2026.5.2+)·방화벽
- 출처: https://developers.cloudflare.com/changelog/post/2026-05-27-cloudflared-connectivity-prechecks/ (2026-05-27)
- 신뢰성: 최상
- 인용:
  > "Starting with `cloudflared` version 2026.5.2, Cloudflare Tunnel automates the entire connectivity pre-checks workflow directly inside the binary."
  > "Transport connectivity — outbound `UDP (QUIC)` and `TCP (HTTP/2)` on port `7844`."
  > "If DNS is unresolvable, or **both** UDP and TCP fail on port 7844, `cloudflared` exits early with the failure"
- 관련 섹션: 트러블슈팅 박스(사내 방화벽에서 7844 아웃바운드 허용)

### 자료 7-5: Quick Tunnels (trycloudflare) + 보호 모드
- 출처: https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/ (2026-09-30), Changelog 2026-10-02, blog https://blog.cloudflare.com/protected-quick-tunnels/ (2026-10-02)
- 신뢰성: 최상
- 인용:
  > "Quick Tunnels create a temporary `trycloudflare.com` URL for a local service. You do not need a Cloudflare account or domain."
  > "Quick Tunnels are for testing and development. For production, create a Cloudflare Tunnel."
  > "Each Quick Tunnel supports up to 200 in-flight requests. Additional requests return a `429` response." / "Quick Tunnels do not support Server-Sent Events (SSE)."
  > "Use the new `--allowed-mail` flag in `cloudflared` to require visitors to authenticate with a one-time PIN sent to their email" — 예: `cloudflared tunnel --url http://localhost:8080 --allowed-mail '*@example.com'`
- 관련 섹션: 웹훅 로컬 테스트, 데모 공유

### 자료 7-6: Wrangler·Vite와의 통합
- 출처: Changelog 2026-03-19 (`wrangler tunnel`), 2026-05-18 (로컬 dev 터널)
- 신뢰성: 최상
- 인용:
  > "`wrangler tunnel quick-start` — Start a free, temporary tunnel without an account using Quick Tunnels."
  > "Wrangler handles downloading and managing the cloudflared binary automatically."
  > "To start a tunnel, press `t` in Wrangler or `t + Enter` in Vite while your dev server is running."
- 관련 섹션: 로컬 개발 장

### 자료 7-7: 폐기·변경 사항
- `proxy-dns` 제거(2026-02-02~): "the `cloudflared proxy-dns` command will be removed from all new `cloudflared` releases" → WARP(현 Cloudflare One Client)·WARP Connector(현 Mesh node)로 이전 (Changelog 2025-11-11)
- 2027년 32-bit Windows·Intel macOS 빌드 중단 (Changelog 2026-09-18)
- 최신 릴리스: 2026.9.3 (2026-09-24, GitHub)

---

## 8. 독자 맞춤 갭 ⑥ — 캐싱

### 자료 8-1: 세 가지 캐시 경로 — Workers Cache / Cache API / fetch(`cf`)
- 출처: https://developers.cloudflare.com/workers/cache/ (2026-09-22), https://developers.cloudflare.com/workers/runtime-apis/cache/ , https://developers.cloudflare.com/workers/reference/how-the-cache-works/ , https://developers.cloudflare.com/workers/runtime-apis/request/
- 신뢰성: 최상
- 인용:
  > (Workers Cache) "Workers Cache lets Cloudflare return cached HTTP responses from your Worker without executing your Worker code."
  > "No zone configuration for caching applies to Workers Caching." (Cache Rules·Page Rules 등 미적용) / "You set `Cache-Control` headers on your responses, and Cloudflare honors them per RFC 9111."
  > "Workers Caching is **tiered by default**." / 요청 병합: "Cloudflare runs your Worker **once** and serves the resulting response to every waiting request."
  > "the Cache API does not collapse concurrent requests, so a burst of traffic to a fresh URL invokes your Worker once per request."
  > 활성화: `"cache": { "enabled": true }`, 퍼지: `ctx.cache.purge({ tags: ["blog-posts"] })`
  > (Cache API) "the contents of the cache do not replicate outside of the originating data center." / "The `cache.put` method is not compatible with tiered caching." / "The `stale-while-revalidate` and `stale-if-error` directives are not supported when using the `cache.put` or `cache.match` methods."
  > (How the cache works) "For requests where Workers are behaving as middleware (that is, Workers are sending a subrequest via `fetch`) it is recommended to use `fetch`."
  > `fetch()`의 `cf` 옵션: `cacheEverything`, `cacheKey`, `cacheTags`, `cacheTtl`, `cacheTtlByStatus`(예: `{ "200-299": 86400 }`); 2026-06-28부터 `cf.vary` 지원
- **과금 함정**: Workers Cache 활성화 시 HIT도 요청 과금, 정적 자산 무료 혜택 상실 (§2-3 #8)
- 관련 섹션: 캐싱 장 — "어느 캐시를 쓸 것인가" 의사결정 표

### 자료 8-2: 존 캐시 — Cache Rules·Cache Response Rules·Tiered Cache·Cache Reserve
- 출처: https://developers.cloudflare.com/cache/how-to/cache-rules/ , https://developers.cloudflare.com/cache/how-to/tiered-cache/ , https://developers.cloudflare.com/cache/advanced-configuration/cache-reserve/ , Changelog 2026-03-24, 2026-07-02(Vary), 2026-04-17(Smart Tiered Cache for public cloud)
- 신뢰성: 최상
- 핵심: Cache Rules Free 10개. Tiered Cache·Smart Topology Free 포함. Cache Reserve는 유료(R2 단가와 동일 구조). Cache Response Rules로 오리진 응답의 `Cache-Control`·`Set-Cookie` 등을 캐시 전에 수정.
- 인용:
  > "Cache Response Rules let you modify `Cache-Control` directives, manage cache tags, and strip headers like `Set-Cookie` from origin responses *before* they reach Cloudflare's cache."
  > "Cloud region hints are available on all plan types (Free, Pro, Business, and Enterprise) at no additional cost."
- 관련 섹션: Spring Boot/Next.js 오리진 앞 캐싱

### 자료 8-3: stale-while-revalidate (비동기) / 무효화 / 퍼지 한도
- 출처: Changelog 2026-02-26, 2026-09-28; https://developers.cloudflare.com/cache/how-to/purge-cache/ ; https://developers.cloudflare.com/cache/concepts/revalidation/
- 신뢰성: 최상
- 인용:
  > "Cloudflare's `stale-while-revalidate` support is now fully asynchronous." / "This change is live for all Free, Pro, and Business zones."
  > (invalidate) "Invalidation marks matching content as stale. On the next request, Cloudflare revalidates the content with your origin. If your origin responds with `304 Not Modified`, Cloudflare reuses the cached content" — 엔드포인트 `POST /zones/$ZONE_ID/invalidate_cache`
  > 퍼지: Free도 URL·Hostname·Tag·Prefix·Purge Everything 모두 가능. 요청 한도 Free "5 requests per minute"(호스트명·태그·프리픽스·전체), 단일 URL 800 URLs/초.
- 관련 섹션: 배포 후 캐시 갱신 전략

### 자료 8-4: Smart Placement / Placement Hints
- 출처: https://developers.cloudflare.com/workers/configuration/placement/ , Changelog 2026-01-22
- 신뢰성: 최상
- 인용:
  > "Smart Placement is available on all Workers plans."
  > "Smart Placement may take up to 15 minutes to analyze your Worker after deployment."
  > (Workers Cache와의 관계) "The cache is always consulted before Smart Placement is considered."
- 관련 섹션: 원격 DB와 가까이 실행하기

---

## 9. 독자 맞춤 갭 ⑦ — Cloudflare 밖 서비스와의 통합

### 자료 9-1: Hyperdrive — Neon·Supabase·PlanetScale·RDS
- 출처: https://developers.cloudflare.com/hyperdrive/ , https://developers.cloudflare.com/hyperdrive/examples/connect-to-postgres/postgres-database-providers/neon/ , Changelog 2026-08-07(MySQL GA), 2026-06-18(PlanetScale 통합 과금), 2026-04-29(VPC), 2026-02-23(STABLE 함수 비캐시), 2025-12-04(로컬 dev 원격 DB)
- 신뢰성: 최상
- 인용:
  > "Hyperdrive supports any Postgres or MySQL database, including those hosted on AWS, Google Cloud, Azure, Neon and PlanetScale. Hyperdrive also supports Postgres-compatible databases like CockroachDB and Timescale."
  > (Neon) "you should use a driver like node-postgres (pg) or Postgres.js to connect directly to the underlying database instead of the Neon serverless driver."
  > (MySQL GA) "You can connect using your existing drivers, ORMs, and query builders ... MySQL support is available at the same pricing as Postgres." — `mysql2` 사용 시 `disableEval: true` 필수
  > (PlanetScale) "PlanetScale usage appears on your Cloudflare invoice each billing period as a dollar total at PlanetScale's standard pricing."
  > (사설 DB) "You can now connect Hyperdrive to a private database through a Workers VPC service. This is the recommended way to connect Hyperdrive to a private database that is not exposed to the public Internet."
- 한도: 쿼리 최대 60초, 캐시 응답 50 MB, 원본 연결 Free ~20 / Paid ~100 (Hyperdrive Limits 2026-06-09)
- Supabase 전용 가이드: [리서치 공백 — 이번 수집에서 개별 페이지 미확인. Hyperdrive 공급자 목록 페이지에서 확인 필요]
- 관련 섹션: 기존 Postgres 재사용 장 (Spring Boot와 Worker가 같은 DB 공유)

### 자료 9-2: R2 — S3 호환 API를 기존 AWS SDK(Java/JS)로
- 출처: https://developers.cloudflare.com/r2/api/s3/api/ , https://developers.cloudflare.com/r2/examples/aws/aws-sdk-java/ (2026-04-21 기준), https://developers.cloudflare.com/r2/examples/aws/aws-sdk-js-v3/
- 신뢰성: 최상
- 인용:
  > "When using the S3 API, the region for an R2 bucket is `auto`. For compatibility with tools that do not allow you to specify a region, an empty value and `us-east-1` will alias to the `auto` region."
  > (Java v2) "You must set `chunkedEncodingEnabled(false)` in the `S3Configuration` when building your client. The AWS SDK for Java v2 uses chunked transfer encoding by default for `putObject` requests, which causes a signature mismatch error (HTTP 403) with R2"
  > 엔드포인트: `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`, `.pathStyleAccessEnabled(true)`, `.region(Region.of("auto"))`
  > (R2 시작) "You need a Cloudflare account with an R2 subscription. ... Complete the checkout flow to add an R2 subscription to your account." (https://developers.cloudflare.com/r2/get-started/)
- 비용 팁(1차): "Use presigned URLs for direct client access instead of proxying through Workers" (Optimize costs 2026-05-04)
- 2026 변화: Sippy가 Azure Blob·S3 호환 스토리지 지원(2026-07-24), R2 `us` jurisdiction(2026-08-17), Local Uploads 오픈 베타(2026-02-03)
- 관련 섹션: Spring Boot에서 R2 쓰기(AWS SDK for Java v2 그대로)

### 자료 9-3: Queues — 외부 소비자(HTTP pull)
- 출처: https://developers.cloudflare.com/queues/configuration/pull-consumers/
- 신뢰성: 최상
- 인용:
  > "HTTP Pull consumers require an API token with the `com.cloudflare.api.account.queues_read` and `com.cloudflare.api.account.queues_write` permissions."
  > 요청 예: `--data '{ "visibility_timeout_ms": 10000, "batch_size": 2 }'`, `visibilityTimeout` 최대 12시간 (Queues Limits)
- 2026: Email Sending 이벤트를 Queues로 구독(2026-07-15), Workers Builds 이벤트 구독(2026-01-09)
- 관련 섹션: JVM 워커가 Cloudflare Queue를 소비하는 하이브리드 패턴

### 자료 9-4: Service bindings·RPC (Worker 간)
- 출처: https://developers.cloudflare.com/workers/runtime-apis/bindings/service-bindings/ , Workers Pricing
- 신뢰성: 최상
- 인용:
  > "Service bindings provide the separation of concerns that microservice or service-oriented architectures provide, without configuration pain, performance overhead or need to learn RPC protocols."
  > "Using global `fetch()` to call another Worker on the same zone without service bindings fails." (Workers Limits)
- 관련 섹션: Worker 분할 설계

### 자료 9-5: 외부 API 호출과 출구(egress) IP
- 출처: Workers Limits(서브리퀘스트·동시 연결), Changelog 2026-04-09(동시 연결 완화), 2025-09-18(Tunnel 호스트명 라우팅), 2026-06-05(Gateway egress for Workers)
- 신뢰성: 최상
- 인용:
  > "Each Worker invocation can have up to six connections simultaneously waiting for response headers." / "Once response headers arrive for a connection, it no longer counts toward the six-connection limit."
  > (Gateway egress) "Workers using a VPC Network binding with `network_id: "cf1:network"` now egress to public Internet destinations through Cloudflare Gateway."
  > (Tunnel) "Route traffic for public hostnames ... through a specific Tunnel to enforce a dedicated source IP, solving the IP allowlist problem for third-party services."
- [리서치 공백] Workers 기본 fetch의 고정 출구 IP 제공 여부: 1차 문서에서 "Workers에 고정 egress IP가 있다/없다"를 직접 명시한 문장을 이번 수집에서 확보하지 못함. 위 두 경로(Tunnel 호스트명 라우팅, Gateway egress)가 문서화된 우회책.
- 관련 섹션: 결제 PG·사내 API가 IP 화이트리스트를 요구할 때

### 자료 9-6: Email (수신 라우팅 + 발신)
- 출처: https://developers.cloudflare.com/email-service/ , Pricing(2026-06-09), Limits(2026-09-25), Changelog 2026-04-16, 2026-06-08(SMTP 베타), 2026-09-04(Wrangler로 라우팅 규칙)
- 신뢰성: 최상
- 인용:
  > "Send transactional emails directly from Workers (`env.EMAIL.send()`) or the REST API"
  > SMTP: `smtp.mx.cloudflare.net:465`, 사용자명 `api_token`, 비밀번호 = "Email Sending: Edit" 권한 API 토큰 → **Spring Boot의 `JavaMailSender`로도 발송 가능 [추론: SMTP 표준이므로]**
  > "New accounts start with a conservative daily quota and scale up over time based on your sending behavior"
  > 메시지 최대 5 MiB(첨부 포함), 수신자 50명/통, 라우팅 규칙 200개/도메인
- 관련 섹션: 가입 확인·매직 링크 메일

### 자료 9-7: IaC·CI/CD
- 출처: https://developers.cloudflare.com/terraform/ , https://developers.cloudflare.com/pulumi/ , https://developers.cloudflare.com/workers/ci-cd/builds/ (2026-10-01), https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/ (2026-09-18), GitHub releases
- 신뢰성: 최상
- 사실:
  - Terraform provider 최신 **v5.27.0** (2026-10-03, https://github.com/cloudflare/terraform-provider-cloudflare/releases). 2025-10-09부터 정적 자산 포함 풀스택 Worker·Workflows를 Terraform으로 배포 가능(Changelog).
  - Pulumi: "Use TypeScript, JavaScript, Python, Go, .Net, Java, or YAML to write Pulumi programs." → **Java 개발자는 Pulumi Java SDK로 IaC 가능**
  - GitHub Actions: `uses: cloudflare/wrangler-action@v4` (문서 예시), 최신 v4.1.3 (2026-09-24). 토큰 템플릿 "Edit Cloudflare Workers"
  - Workers Builds: GitHub·GitLab·Artifacts 저장소 연결, 기본 Node.js 24.18.0 (2026-07-30), Deploy Hooks (2026-04-01), 대체된 대기 빌드 건너뛰기 (2026-07-24), PR별 Worker Previews (2026-09-22)
- 관련 섹션: 배포 자동화 장

### 자료 9-8: Stripe·웹훅
- [리서치 공백] Cloudflare 1차 문서의 Stripe 전용 가이드는 이번 수집 범위에서 확인하지 못함. 문서화된 관련 사실만: Quick Tunnel로 로컬 웹훅 수신 테스트("Protected Quick Tunnels let you share a local development server, webhook receiver, or demo", Changelog 2026-10-02), `node:crypto` 기본 제공(2026-08-04~)으로 Stripe Node SDK 서명 검증 가능성 **[추론]**.

---

## 10. 독자 맞춤 갭 ⑧ — 도구 체인

### 자료 10-1: Wrangler v4 / `wrangler.jsonc` 권장
- 출처: https://developers.cloudflare.com/workers/wrangler/configuration/ , https://developers.cloudflare.com/workers/wrangler/install-and-update/
- 신뢰성: 최상
- 인용:
  > "Cloudflare recommends using `wrangler.jsonc` for new projects, and some newer Wrangler features will only be available to projects using a JSON config file."
  > "Wrangler is installed locally into each of your projects."
  > "We support running the Wrangler CLI with the Current, Active, and Maintenance versions of Node.js."
- 2026 신규: 인증 프로필(2026-07-02), OS 키체인 저장(2026-06-03), 디바이스 플로 로그인(2026-08-04), `secrets` 필수 선언(2026-03-25), `wrangler types --check`(2026-01-12), KV·R2·D1 자동 프로비저닝(2025-10-24)
- 최신: wrangler **4.147.0** (2026-10-02)

### 자료 10-2: `cf` CLI 베타 — Wrangler의 후속 후보
- 출처: https://developers.cloudflare.com/cf/ , https://blog.cloudflare.com/cloudflare-cf-cli-launch/ (2026-09-28), 한국어판 https://blog.cloudflare.com/ko-kr/cloudflare-cf-cli-launch/
- 신뢰성: 최상
- 인용:
  > "Wrangler is the CLI for Workers projects configured with `wrangler.jsonc` or `wrangler.toml`. `cf` covers the public Cloudflare API and uses `cloudflare.config.ts` for Workers projects."
  > "Before you run `cf dev`, `cf build`, or `cf deploy` in a Wrangler project, convert it with `cf migrate`."
  > "Wrangler only provides commands for around 280 operations, and Cloudflare offers thousands."
  > "In March 2026, agents were responsible for a quarter of Wrangler use ... Last week, agent usage reached 48%."
- 주의: vinext 1.0 init이 "default Cloudflare projects to cf". 책 집필 시점(2026-10)에는 **Wrangler(GA)를 본문 기본, `cf`(베타)를 전망 박스**로 다루는 것이 안전 **[편집 판단]**.

### 자료 10-3: C3 / 자동 구성 / 로컬 개발
- 출처: https://developers.cloudflare.com/pages/get-started/c3/ , Changelog 2026-02-25(autoconfig GA), https://developers.cloudflare.com/workers/local-development/ (2026-08-20), Changelog 2025-09-16(remote bindings GA), 2026-04-13(Local Explorer)
- 인용:
  > "Cloudflare provides a CLI command for creating new Workers and Pages projects — `npm create cloudflare`, powered by the `create-cloudflare` package" (최신 create-cloudflare 2.73.2, 2026-10-02)
  > "Starting with Wrangler **4.68.0**, running `wrangler deploy` automatically configures your project by detecting your framework, installing required adapters, and deploying it"
  > (remote bindings) "add `"remote" : true` to each binding that you want to rely on a remote resource running on Cloudflare"

### 자료 10-4: 테스트 — `@cloudflare/vitest-plugin` / Miniflare v5
- 출처: https://developers.cloudflare.com/workers/testing/vitest-integration/ (2026-08-20), Changelog 2026-08-19, 2026-09-08
- 인용:
  > "Version 1 of the Workers Vitest integration is published as `@cloudflare/vitest-plugin`. The package was formerly named `@cloudflare/vitest-pool-workers`."
  > "To migrate automatically, run: `npx @cloudflare/codemods vitest:pool-workers-to-vitest-plugin`"
  > "For outbound request mocks in Workers tests, use the `@msw/cloudflare` integration."
  > (Miniflare v5) "Most projects should use those tools instead of depending on Miniflare directly, and Miniflare v5 will not require any action."
- 주의: GitHub 릴리스상 Miniflare 5.x는 **alpha 프리릴리스**(예: `miniflare@5.20261001.0-alpha`, 2026-10-01). 직접 의존 금지가 공식 권고.

### 자료 10-5: 관측성 — Workers Logs·Traces·Tail·Issues
- 출처: https://developers.cloudflare.com/workers/observability/logs/workers-logs/ (2026-10-02), https://developers.cloudflare.com/workers/observability/traces/ (2026-10-02), https://developers.cloudflare.com/workers/observability/logs/real-time-logs/ (2026-06-25), blog https://blog.cloudflare.com/one-observability-platform/ (2026-10-02), https://blog.cloudflare.com/cloudflare-tracing/ (2026-10-02)
- 인용:
  > (Traces) "Workers tracing follows OpenTelemetry (OTel) standards" / "You can also set `persist: false` to export traces to your destination without persisting them in the Cloudflare dashboard." / `head_sampling_rate` 기본 1
  > (Observability 블로그) "We're launching Cloudflare Traces in open beta, giving you a request-level view of supported security rules, transformations, cache decisions, routing, Workers, and origin handling."
  > 설정: `"observability": { "enabled": true }`
- 2026: 커스텀 스팬 `startActiveSpan()`(2026-07-28), RPC 세션 스팬 자동(2026-09-17), 로컬 트레이싱(2026-08-04), 메모리 사용량 메트릭(2026-06-30), Custom Dashboards에 로그·트레이스(2026-10-02)
- 관련 섹션: 운영 장 + §2 Observability 가격 전환(2026-12-01)

### 자료 10-6: Worker Previews
- 출처: https://blog.cloudflare.com/worker-previews/ (2026-09-22, Yomna Shousha 외), https://developers.cloudflare.com/workers/previews/
- 인용:
  > "Each Git branch gets a production-like place to run, with its own code, configuration, URL, observability, and state."
  > "Deploy an isolated Preview with npx wrangler preview" (Wrangler 4.135.0+)
  > "For Durable Objects and Containers, Cloudflare automatically provisions separate namespaces, storage, apps, and instances for every Preview."

---

## 11. 엔지니어링 블로그·한국어 자료

### 자료 11-1: Cloudflare 블로그 한국어판 (1차, 한국어)
- 확인된 한국어판(HTTP 200, 검색 시점 2026-10-03):
  - 『전체 Cloudflare API를 위한 에이전틱 CLI, cf를 소개합니다』 https://blog.cloudflare.com/ko-kr/cloudflare-cf-cli-launch/ (원문 2026-09-28)
  - 『모두를 위한 안전한 사설 네트워킹: 사용자, 노드, 에이전트, Workers — Cloudflare Mesh 소개』 https://blog.cloudflare.com/ko-kr/mesh/ (원문 2026-04-14)
  - 『Cloudflare Billable Usage API(과금 사용량 API) 소개: Cloudflare 비용을 프로그래밍 방식으로 확인』 https://blog.cloudflare.com/ko-kr/billable-usage-api/ (원문 2026-08-03)
  - 『Agents Week에서 출시한 모든 것』 https://blog.cloudflare.com/ko-kr/agents-week-review-august-2026/ (원문 2026-08-10)
  - 『Workers VPC 서비스가 전 세계 어디에서나 지역 사설 네트워크에 연결하는 방법』 https://blog.cloudflare.com/ko-kr/workers-vpc-open-beta/ (원문 2025-11-05)
- 한국어판 없음(404): vinext 1.0, Worker Previews, Protected Quick Tunnels, Workers protected by Access, Observability 8대 업데이트, Containers 재구축, Python Workers GA, gRPC
- 신뢰성: 최상(공식 번역)
- 관련 섹션: 한국 독자용 "더 읽을거리"

### 자료 11-2: 한국어 실무 후기 — Workers + D1 개인 홈페이지
- 출처: https://jab-guyver.co.kr/7280 — 잡가이버, 2026-08-07
- 신뢰성: 중(개인 블로그, 수치는 공식 문서와 일치 확인)
- 인용(원문 한국어):
  > "도메인만 구입하고 Cloudflare 무료 플랜을 활용하면 호스팅비 없이 DB가 연결된 개인 홈페이지나 소형 블로그를 운영할 수 있습니다."
  > "무료 한도가 있어도 R2를 활성화하려면 Dashboard에서 R2 구독 Checkout 절차를 완료해야 합니다. 계정 상태에 따라 결제수단 등록을 요구할 수 있어"
  > "Containers는 무료 플랜 기능이 아닙니다. Workers Paid 플랜에서만 사용할 수 있으며"
- 관련 섹션: "무료로 시작하기" 장의 현장 사례 / R2 결제수단 요구(1차: "You need a Cloudflare account with an R2 subscription")

### 자료 11-3: Cloudflare 엔지니어링 블로그(내부 구조) — 책의 "왜" 설명용
- Pingora가 캐시를 구동: Changelog 2026-05-04 "Pingora now powers Cloudflare's cache"
- 모듈 레지스트리 재작성(Node.js 호환): https://blog.cloudflare.com/workers-module-registry-nodejs/ (2026-09-09)
- Containers 교차 테넌트 취약점 사후 분석: https://blog.cloudflare.com/containers-cross-tenant-vulnerability/ (2026-09-24) — Firecracker VM·dm-thin 구조 설명 포함
- Containers 재구축(스케줄링 정책·스냅샷): https://blog.cloudflare.com/faster-agent-sandboxes/ (2026-09-30)
- KV Instant(Quicksilver 기반): https://blog.cloudflare.com/workers-kv-instant/ (2026-10-01) — 본문 미정독 [리서치 공백: KV 최종 일관성 변화 여부 확인 필요]

---

## 12. 문서 내 불일치·주의 목록 (fact-checker용)

1. **vinext 상태**: 가이드(2026-08-25) "vinext is in beta" ↔ GitHub vinext 1.0.0(2026-09-28)·블로그 "Vinext 1.0".
2. **Vectorize Free 가용성**: Workers Pricing "Vectorize is currently only available on the Workers paid plan" ↔ 같은 페이지·Vectorize Pricing의 Free 컬럼(3,000만 쿼리 차원/월).
3. **Workflows 스크립트 크기**: Workflows Limits(2026-09-21) "3MB/10MB max script size" ↔ Workers Limits(2026-09-05)·Changelog(2026-09-04) 64 MiB. Workflows 페이지가 갱신 누락으로 보임.
4. **Workflows 기본 보존 기간**: Workflows Pricing "30 days on the Paid plan" ↔ Changelog 2026-09-10 "Default instance retention for new Workflows on Workers Paid is seven days".
5. **Durable Objects SQLite 스토리지 과금 문구**: Workers Pricing이 아직 "will be enabled in January 2026, with a target date of January 7, 2026"라는 미래형 문구를 유지(2026-10 시점엔 과거). 실제 개시일 확정 공지는 이번 수집에서 미확인.
6. **Analytics Engine**: "Currently, you will not be billed" (2026-04-23) — 과금 개시 시점 미정.
7. **Tunnel replica 라우팅**: §7-3 참조.
8. **Kotlin/Wasm**: 3자 요약 "stable" ↔ kotlinlang.org "Beta".
9. **이벤트명**: 2026년 4월은 "Agents Week 2026"(Developer Week 아님).
10. **Queue consumer CPU 상한**: Workers Pricing(2026-10-02) "Max of 15 minutes of CPU time per Cron Trigger or Queue Consumer invocation" ↔ Queues Limits(2026-04-21) "Consumer CPU time: Configurable to 5 minutes" + "Consumer duration (wall clock time) 15 minutes". Workers Limits(2026-09-05) CPU 표는 Cron만 15분으로 기재. 본문은 "CPU 5분(설정)·벽시계 15분"으로 보수적으로 쓰고 출간 전 재확인.
11. **D1 호출당 쿼리 수**: D1 Limits(2026-04-21) "Queries per Worker invocation ... 1000 (Workers Paid) / 50 (Free)" ↔ Workers Limits(2026-09-05)·Changelog 2026-02-11 서브리퀘스트 Paid 기본 10,000(최대 1,000만), 내부 서비스 Free 1,000. D1 페이지가 2026-02 상향을 반영하지 않은 것으로 보임.
12. **Browser Run 개명 시점**: 문서 경로 `/browser-run/`와 changelog 태그 "Browser Run"(2026-04-14 "Manage Browser Rendering sessions with Wrangler CLI"부터 확인)으로 2026-04 중순 개명으로 추정. 개명 공지 원문은 미확보.

---

## 수집 한계

- **수집 건수**: 1차 문서 페이지 약 140개(developers.cloudflare.com `index.md`), changelog 게시물 57건 정독(+RSS 1,306건 제목 필터), Cloudflare 블로그 19편, GitHub 릴리스 8개 저장소, 3자 자료 3건(dev.to·kotlinlang.org·한국어 개인 블로그 1건).
- **[리서치 공백]**
  1. Zero Trust 무료 좌석 수(50명) — 공식 플랜 페이지가 JS 렌더링이라 원문 미확보. 1차 근거는 Mesh 한정 "50 nodes and 50 users free"뿐. Pay-as-you-go 좌석 단가($7/user 3자 주장)도 미확인.
  2. R2: Free 범위 초과 시 차단인지 과금인지 명시 문구 미확인(1차는 "R2 subscription" 필요만 명시).
  3. Workers 기본 egress 고정 IP 유무에 대한 직접 문장 미확보.
  4. Access JWT 검증의 Java/Kotlin(Spring Security) 공식 예제 없음.
  5. CASB 무료 범위, Gateway Free 기능 세부(로그 보존 등) 미확인.
  6. Hyperdrive Supabase·AWS RDS 개별 가이드 미정독.
  7. Stripe/웹훅 전용 1차 가이드 미확인.
  8. DO SQLite 스토리지 과금의 실제 개시일 확정 공지 미확인.
  9. KV Instant(2026-10-01) 본문 미정독 — KV 일관성 모델 변경 여부.
  10. Clerk/Auth0와 Access 연동 전용 가이드(1차) 미확인 — generic OIDC로 추정.
  11. 컨퍼런스 발표(Cloudflare Connect 2026 등) 자료는 수집하지 못함.
- **접근 실패**: https://www.cloudflare.com/plans/zero-trust-services/ (클라이언트 렌더링), `changelog/post/2026-08-11-hostname-routing-ga-public-initial-resolved/`(404 — 제목만 RSS로 확인: "Hostname routing is now generally available"), 블로그 태그 페이지 페이지네이션(HTML 렌더링).
- **의도적으로 제외**: 12개월 이상 지난 튜토리얼의 가격·한도·버전 주장(구버전 위험), 커뮤니티 토론(Reddit·HN·OKKY 등 — community-researcher 담당), 논문(paper-researcher 담당), Workers AI 모델별 단가 전체 표(모델 교체가 잦아 본문에는 Neuron 단가만 권장).
- **신선도 경고**: 이 파일의 가격·한도는 2026-10-03 시점. 특히 (a) Observability 가격 2026-12-01 전환, (b) Workflows step 과금 개시, (c) vinext 문서 갱신, (d) `cf` CLI 베타→GA, (e) Workers VPC 베타→GA(과금 개시) 다섯 가지는 출간 직전 재확인 필요.

