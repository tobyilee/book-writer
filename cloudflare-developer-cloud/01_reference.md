# Cloudflare를 "나의 클라우드"로 — 앱·서비스 배포·운영 레퍼런스

- 슬러그: `cloudflare-developer-cloud` · 장르: tech-book
- 대상 독자: Java·Kotlin·JS/TS·React·Next.js·Node.js 경험 개발자
- 합성 시점: 2026-10-03 (research-lead). 원천: `research/web.md`(웹, 1차 문서 중심), `research/community.md`(커뮤니티), `research/papers.md`(논문·표준). 원천 파일은 그대로 보존 — fact-checker의 1차 대조 근거다.
- 추가 갭 필: research-lead가 2026-10-03에 1차 출처(developers.cloudflare.com / cloudflare.com / blog.cloudflare.com)로 4개 공백을 직접 조회했다. 이 항목들은 `research/*.md`에 없으므로 **[갭필 2026-10-03]** 태그와 함께 원문 인용·URL·문서 날짜를 이 파일에 그대로 남겼다. fact-checker는 이 파일의 해당 인용을 대조 기준으로 쓴다.
- 출처 유형 태그: **[웹]** 1차 문서·공식 블로그·changelog·GitHub 릴리스 / **[웹-3자]** 개인·경쟁사 블로그 / **[커뮤니티]** HN·Reddit·GitHub 이슈·GeekNews 등(라벨 `[일화]`·`[이해관계자: 역할]`·`[문서화]`·"미러 경유" 원문 유지) / **[논문]** 논문·표준(확인 등급 `[원문]`·`[초록]`·`[요약]` 유지) / **[추론]** 원천 리서처의 추론 / **[편집 판단]** 집필 방침 제안.
- 신선도 규칙: 가격·한도·버전·상태는 "{제품} {날짜} 기준"을 붙인다. 날짜는 해당 문서의 `Last updated`(=dateModified) 또는 게시일이며, 검색 시점은 전 항목 2026-10-03.
- 인용 규칙: 따옴표 안 영어는 원문 그대로. 수치·기간·연도·인물 귀속은 원문 표현을 바꾸지 않았다. 원천의 "~라고 쓰지 말 것" 경고는 경고째 옮겼다(⚠ 표시).

---

## 0. 저술가 필독 — 명칭·상태 변경 (모든 장에 적용)

> 이 박스의 항목은 틀리면 책 전체의 신뢰를 깎는다. 본문·코드·그림 캡션·용어집 모두 아래 표기를 따른다.

| # | 틀린/낡은 표현 | 2026-10-03 기준 올바른 표현 | 근거 |
|---|---|---|---|
| 0-1 | "2026년 Developer Week" | **"2026년 4월 Agents Week"**(블로그 태그 "Agents Week 2026"). 2026-08-03~07에 Agents Week가 한 번 더 열림. Birthday Week 2026은 2026-09-28~10-02 | [웹] 태그 RSS `developer-week`에 2026년 글 0건(검색 시점 2026-10-03), https://blog.cloudflare.com/mesh/ (2026-04-14, 태그 "Agents Week 2026"), https://blog.cloudflare.com/agents-week-review-august-2026/ (2026-08-10). ⚠ web.md: "본문에서 "2026년 Developer Week"라는 명칭은 쓰지 말 것." |
| 0-2 | WARP Client / WARP Connector | **Cloudflare One Client** / **Cloudflare Mesh node**. 원문: "WARP Connector (now called a Cloudflare Mesh node) and WARP Client (now called Cloudflare One Client)" | [웹] https://blog.cloudflare.com/mesh/ (2026-04-14). 책 전체 통일: "WARP"는 구명칭으로 괄호 병기 [편집 판단, web.md 6-2] |
| 0-3 | Browser Rendering | **Browser Run** (문서 경로 `/browser-run/`) | [웹] https://developers.cloudflare.com/browser-run/pricing/ (2026-04-21 기준). 개명 시점은 2026-04 중순으로 **추정** — 개명 공지 원문 미확보(§7 원장 C-12) |
| 0-4 | Tunnel은 Cloudflare One(Zero Trust) 문서 하위 | **독립 제품 문서 `/tunnel/`**, 대시보드 경로 **Networking > Tunnels**. 사설망·VPN 대체 용도는 여전히 "Cloudflare One Tunnel documentation" | [웹] https://developers.cloudflare.com/tunnel/ (2026-09-11), Changelog 2026-02-20 tunnel-core-dashboard |
| 0-5 | "Next.js on Cloudflare = OpenNext" | **공식 권장 = vinext**. 원문: "Cloudflare recommends vinext as the default way to run Next.js applications on Cloudflare Workers." OpenNext는 "maintain an existing OpenNext application"용. **vinext 1.0.0 릴리스 2026-09-28**, 그러나 공식 가이드(2026-08-25)는 아직 "vinext is in beta" | [웹] https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/ (2026-08-25), https://github.com/cloudflare/vinext/releases/tag/vinext%401.0.0 (2026-09-28). 권장 표현: "vinext 1.0 출시(2026-09-28), 공식 가이드는 갱신 전 beta 표기" |
| 0-6 | 새 정적 사이트는 Pages로 | **새 프로젝트는 Workers**. Pages 문서 첫머리: "Start new projects with Workers." Pages는 계속 지원되나 투자는 Workers로 | [웹] https://developers.cloudflare.com/pages/ (2026-08-25) |
| 0-7 | Workers Sites | **폐기(deprecated)**. "Do not use Workers Sites for new projects." | [웹] https://developers.cloudflare.com/workers/configuration/sites/ (2026-04-23) |
| 0-8 | `@cloudflare/vitest-pool-workers` | **`@cloudflare/vitest-plugin`(v1)** | [웹] Changelog 2026-08-19 |
| 0-9 | `cloudflared proxy-dns` | 2026-02-02 이후 릴리스에서 **제거** → Cloudflare One Client·Mesh node로 이전 | [웹] Changelog 2025-11-11 |
| 0-10 | "Worker 크기 한도 3MB(Free)/10MB(Paid)" | **비압축 64 MiB, Free·Paid 동일** (2026-09-04 변경) | [웹] Changelog 2026-09-04. 구 수치를 쓴 OpenNext 트러블슈팅 문서·dev.to(2024) 글은 낡음 |
| 0-11 | "새 DO 네임스페이스를 KV 백엔드로" | 2026-07-09부터 **신규 네임스페이스는 SQLite 백엔드만** | [웹] Changelog 2026-07-09 |
| 0-12 | "Kotlin/Wasm stable" | **Beta** (kotlinlang.org 1차 표기) | [웹] https://kotlinlang.org/docs/wasm-overview.html (2026-09-01 수정). ⚠ 3자 요약의 "stable"을 따르지 말 것 |
| 0-13 | `nodejs_compat` 플래그는 필수 | compatibility date **`2026-08-04` 이상이면 기본 ON**(`nodejs_compat`·`nodejs_compat_v2`) | [웹] Changelog 2026-08-04 |
| 0-14 | 본문 기본 CLI | **Wrangler v4(GA)를 본문 기본**, `cf` CLI(2026-09-28 베타)는 전망 박스 | [편집 판단, web.md 10-2]. 단 vinext 1.0 init이 "default Cloudflare projects to cf"이므로 vinext 장에서는 `cf`가 나타남을 명시 |

---

## 1. 개념과 정의

### 1-1. 플랫폼 지도 (책의 출발 그림)
- **Workers**: 1급 지원 언어 JavaScript·TypeScript·Python·Rust. 원문 "Workers is a polyglot platform, and provides first-class support for the following programming languages: JavaScript, TypeScript, Python Workers, Rust" — [웹] Workers languages (2026-07-03 기준). 그 외 언어는 Wasm 경유("including C, C++, Kotlin, Go and more"). "Threading is not possible in Workers." "WASI support is experimental on Cloudflare Workers, with only some syscalls implemented." — [웹] WebAssembly 문서 (2026-04-23 기준)
- **Python Workers GA** 2026-09-21 — [웹] https://blog.cloudflare.com/python-workers-ga/ . WSGI(Django·Flask) 지원 2026-09-02, Python 3.14 2026-09-08, Python↔JS RPC 2026-08-03 (Changelog)
- **정적 자산 + Worker** 가 새 기본 웹 호스팅 단위(Pages 대체) — §0-6
- **저장소**: KV(최종 일관성 KV), D1(SQLite 기반 관계형, DB당 10 GB), Durable Objects(상태 있는 객체, SQLite 스토리지), R2(S3 호환 객체 저장, 이그레스 무료), Queues, Workflows, Hyperdrive(외부 Postgres/MySQL 풀링·캐시), Vectorize, Analytics Engine
- **컴퓨트 확장**: Containers(Workers Paid 전용, 2026-04-13 GA), Browser Run, Workers AI, AI Gateway
- **네트워크·보안**: Tunnel(`cloudflared`), Cloudflare One(Access·Gateway·Mesh), WAF, Rate Limiting, Turnstile, Cache(존 캐시·Workers Cache)
- Workers Paid는 도메인(존) 플랜과 별개: "Workers Paid plan is separate from any other Cloudflare plan (Free, Professional, Business) you may have." — [웹] Workers Pricing (2026-10-02 기준)

### 1-2. "2세대 서버리스"와 격리 스펙트럼 (학술 배경)
- 서버리스 정의·한계(상태·통신·콜드 스타트) — [논문] Jonas et al., "Cloud Programming Simplified: A Berkeley View on Serverless Computing", arXiv:1902.03383 (2019) [초록]. 인용: "represents an evolution that parallels the transition from assembly language to high-level programming languages."
- **microVM 칸** — [논문] Agache et al., "Firecracker", NSDI '20, pp. 419–434 [원문]. microVM당 메모리 오버헤드 5MB 미만, 애플리케이션 코드까지 부팅 125ms 미만, 호스트당 초당 최대 150개 microVM 생성. ⚠ 논문 인용 시 논문 표기 "5MB" 사용(프로젝트 사이트는 "<5 MiB"). 인용:
  > "Some language VMs (such as V8's isolates and the JVM's security managers) aim to run multiple workloads within a single process, an approach which introduces significant tradeoffs between functionality (and compatibility) and resistance to side channel attacks such as Spectre" (§2.1.2)
  > "Language-specific isolation techniques were not suitable for Lambda or Fargate, given our need to support arbitrary binaries." (§2.1.2)
  > "While the 125ms boot times offered by Firecracker are fast, they are not fast enough for the scale-up path of Lambda" (§4)
  - 참고: Cloudflare Containers도 Firecracker VM 위에서 동작함이 교차 테넌트 취약점 사후 분석에 설명돼 있다 — [웹] https://blog.cloudflare.com/containers-cross-tenant-vulnerability/ (2026-09-24, "Firecracker VM·dm-thin 구조 설명 포함" — web.md 요약 기반, 인용 전 원문 확인)
- **isolate 칸** — [논문] Schirmer et al., "New Kids: An Architecture and Performance Investigation of Second-Generation Serverless Platforms", arXiv:2604.15916 (v1 2026-04-17, v2 2026-08-14), ACM TOIT 게재 승인 [초록 + 본문 일부 요약]. 7개 플랫폼(AWS Lambda, Google Cloud Run Functions, OCI Functions, Cloudflare Workers, Deno Deploy, Fastly Compute, Fly.io), 3,800만 회 이상 호출 측정. 인용:
  > "While first-generation platforms are based on containerized, centralized execution, the new generation leverages lightweight isolates and edge deployment. This evolution reduces warm request latency from approximately 40ms to around 10ms and reduces cold starts to an afterthought, but limits the execution environment." (Abstract)
  - Workers 세부(SNI로 핸드셰이크 중 인스턴스 시작, LRU 축출, isolate당 128MB)는 **[요약] 등급** — 공식 문서와 교차 확인 후 사용.
- **왜 콜드 스타트가 문제인가** — [논문] Shahrad et al., "Serverless in the Wild", USENIX ATC '20 [원문]. "45% of the applications are invoked once per hour or less on average, and 81% of the applications are invoked once per minute or less on average." (§3) / "most functions are invoked very infrequently, but there is an 8-order-of-magnitude range of invocation frequencies." (Abstract) / 애플리케이션 20% 미만이 전체 호출의 99.6%. 사이드 프로젝트·사내 툴 독자에게 직결.
- **isolate는 안전한가** — [논문] Schwarzl, Borrello, Kogler, Varda, Schuster, Schwarz, Gruss, "Robust and Scalable Process Isolation Against Spectre in the Cloud", ESORICS 2022, DOI 10.1007/978-3-031-17146-8_9 [초록]. Cloudflare Workers에서 원격 Spectre 시연(누출 2 bit/min = arXiv 판 120 bit/h), DyPrIs 오탐률 0.61%. ⚠ 저자 순서는 ESORICS 출판본 우선(arXiv 판은 마지막 두 명 순서가 다름). 관련 포인터: Kenton Varda, "Spectre research with TU Graz", Cloudflare Blog, 2021-10-12 — 타이머 제한·멀티스레딩 차단(세부 문구는 교차 확인 권장).
- 대조 편집 제안: Firecracker의 "isolate는 Spectre 저항성과 트레이드오프" ↔ DyPrIs의 "통계적 보장 유지"를 한 박스에 병기 [편집 판단, papers.md].

### 1-3. Zero Trust의 정의와 계보
- [논문] NIST SP 800-207 (Rose, Borchert, Mitchell, Connelly, 2020년 8월), DOI 10.6028/NIST.SP.800-207 [초록]:
  > "Zero trust assumes there is no implicit trust granted to assets or user accounts based solely on their physical or network location (i.e., local area networks versus the internet) or based on asset ownership (enterprise or personally owned)."
  > "Authentication and authorization (both subject and device) are discrete functions performed before a session to an enterprise resource is established."
- [논문] Ward & Beyer, "BeyondCorp: A New Approach to Enterprise Security", ;login: Vol. 39 No. 6 (2014년 12월) [초록]: "We are removing the requirement for a privileged intranet and moving our corporate applications to the Internet." ⚠ 원칙 문장(접근은 네트워크 위치가 아닌 사용자·기기 자격으로 결정)은 원문 미확인 — NIST 문장으로 대신 인용.
- 매핑: Access 정책(누가·어떤 기기로·어떤 조건에서) + Cloudflare One Client(구 WARP) 기기 posture = NIST의 "subject and device" 인증. PDP/PEP 용어를 쓰려면 NIST 본문 재확인 필요.

### 1-4. Anycast와 엣지 캐시의 성질
- [논문] Calder et al., "Analyzing the Performance of an Anycast CDN", IMC '15 [초록]: "anycast usually performs well despite the lack of precise control but that it directs roughly 20% of clients to a suboptimal front-end."
- [논문] Koch et al., "Anycast In Context: A Tale of Two Systems", SIGCOMM 2021 [초록]: 루트 DNS 팽창 영향 사용자 >95%, Microsoft CDN은 35%. "We show that CDN anycast latency has little inflation due to extensive peering and engineering." ⚠ 저자 순서는 Crossref 반환 순서 — 인용 전 재확인.
- [논문] Maggs & Sitaraman, "Algorithmic Nuggets in Content Delivery", SIGCOMM CCR 45(3) 2015 [원문]: "On a typical CDN server cluster serving web traffic over two days, 74% of the roughly 400 million objects in cache were accessed only once and 90% were accessed less than four times."
- [논문] Yang et al., "FIFO queues are all you need for cache eviction", SOSP '23 [초록]: "most objects in skewed workloads will only be accessed once in a short window, so it is critical to evict them early (also called quick demotion)." ⚠ **"Cloudflare가 S3-FIFO를 쓴다"고 쓰지 말 것** (확인 안 됨).
- 커뮤니티 연결: 다모앙 일화 "요청이 LA로 라우팅되는 경우가 있었다"(§6) ↔ anycast 20% 비최적. 한국발 트래픽 PoP는 ISP 피어링에 좌우(검증 필요).

### 1-5. 엣지 데이터 일관성·상태 모델
- 최종 일관성 개념 — [논문] Bailis et al., "Probabilistically Bounded Staleness for Practical Partial Quorums", PVLDB 5(8) 2012 [초록]: "these configurations provide only basic eventual consistency guarantees, with no limit to the recency of data returned." ⚠ **PBS의 "수십 ms"는 데이터센터 내 Dynamo 계열 쿼럼 기준 — KV 전파 지연 수치로 쓰지 말 것.**
- KV 실측(1차): KV Instant 발표 블로그의 classic 모드 표 — p99 reads(cached) 160 ms, p99 reads(all) 287 ms, median·p95 write replication "< 1 s", **p99 write replication 4.38 s** ("Time to replicate across all required storage backends") — [웹][갭필 2026-10-03] https://blog.cloudflare.com/workers-kv-instant/ (Rob Sutter, 2026-10-01). 커뮤니티·문서 요약이 말하는 "전파 최대 60초"(dev.to Kuryzhev 2026-07-01, 검색 요약 경유)와는 **보완 관계**(전형값 vs 상한 서술)로 제시하고, 60초 상한 문구는 KV 공식 문서로 재확인할 것.
- Durable Objects 개념 계보 — [논문] Bernstein et al., "Orleans: Distributed Virtual Actors…", MSR-TR-2014-41 [초록]: "The actor model makes it natural to build a stateful middle tier and achieve the required performance." ⚠ **"Durable Objects는 Orleans에서 영감을 받았다"고 쓰지 말 것** — "유사한 모델"로만. Orleans 단일 스레드 보장 문구는 원문 미확인.
- 왜 SQLite인가 — [논문] Gaffney et al., "SQLite: Past, Present, and Future", PVLDB 15(12) 2022 [초록]: "SQLite has become the most widely deployed database engine in existence." 활성 SQLite DB 1조 개 초과 추정.
- 설계 철학(1차): "D1 is designed for horizontal scale out across multiple, smaller (10 GB) databases" — [웹/커뮤니티 문서화] https://developers.cloudflare.com/d1/platform/limits/

### 1-6. 표준 (규범 기준)
- RFC 9111 HTTP Caching (2022-06, STD 98) / RFC 9213 Targeted HTTP Cache Control(`CDN-Cache-Control`) / RFC 5861 `stale-while-revalidate`·`stale-if-error` — [논문/표준][초록]. ⚠ 벤더 구현과 RFC는 다를 수 있음 — Cloudflare 해석은 §3-8의 1차 문서로 대조(예: Cache API `cache.put`/`match`는 SWR·SIE 미지원).
- RFC 9000 QUIC / RFC 9114 HTTP/3 — 정의 1회 인용용.
- RFC 7519 JWT — Access JWT 검증 실습의 기준(서명·`aud`·`exp`).
- OAuth 2.1: draft-ietf-oauth-v2-1-16 (2026-09-03), **RFC 미발행 활성 초안** [요약] — "초안"임을 반드시 밝히고 출간 시 리비전 재확인(🕒).
- OpenID Connect Core 1.0 incorporating errata set 2 (2023-12-15) [초록].
- ECMA-429 "Minimum common web API" 1st edition (2025년 12월), WinterTC(TC55) [요약 — 인용 전 Ecma 페이지 확인]. "Workers 코드는 Node 코드가 아니라 Web 표준 API 코드"의 근거.

---

## 2. 가격·한도·과금 보호 — 책에서 가장 위험한 구역

> 모든 금액은 USD. 행마다 "{문서} {날짜} 기준". 이 구역의 수치는 2026-10-03 시점이며, 본문에 옮길 때 기준일을 함께 적는다.
> Workers Paid: "The Workers Paid plan includes Workers, Pages Functions, Workers KV, Hyperdrive, and Durable Objects usage for a minimum charge of $5 USD per month for an account." — [웹] Workers Pricing 2026-10-02 기준, https://developers.cloudflare.com/workers/platform/pricing/

### 2-1. 개발자 플랫폼(Workers 계열) [웹]

| 제품 | Free 한도 | Paid 기본 포함량 | 초과 단가 | Free 초과 시 동작 | 기준·출처 |
|------|-----------|------------------|-----------|-------------------|-----------|
| Workers 요청 | 100,000/일 (00:00 UTC 리셋) | 1,000만/월 | +$0.30/100만 | **Error 1027** (라우트별 fail open/closed 선택) | Workers Pricing 2026-10-02, Limits 2026-09-05 |
| Workers CPU | 10 ms/호출 | 3,000만 CPU-ms/월 | +$0.02/100만 CPU-ms | Error 1102 "Worker exceeded resource limits" | 同上. Paid 호출당 최대 5분(기본 30초). Cron(≥1시간 간격) CPU 15분 / Queue consumer는 문서 불일치(§7 C-10) |
| Workers Duration | 과금 없음 | "No charge or limit for duration" | — | — | 同上 |
| `limits.cpu_ms` | — | 기본 30,000 → 최대 300,000 | — | 설정치 초과 시 종료 | Workers Pricing 2026-10-02 |
| `limits.subrequests` | 50/호출(외부), 1,000(내부 서비스) | 10,000/호출(기본), 최대 1,000만 | 서브리퀘스트 비과금 ("Cloudflare does not bill for subrequests you make from your Worker.") | — | Workers Pricing 2026-10-02, Changelog 2026-02-11 |
| Worker 크기 | 비압축 64 MiB | 비압축 64 MiB | — | — | Changelog 2026-09-04 |
| Worker 시작 시간 | 1초 | 1초 | — | — | Changelog 2025-10-10 (400 ms → 1초) |
| 정적 자산 | 무료·무제한 (버전당 파일 20,000개, 파일당 25 MiB) | 파일 100,000개 | **$0** ("Requests to static assets are free and unlimited") | `run_worker_first` 경로는 Worker 호출로 계산 → Free 초과 시 **429** | Static Assets Billing 2026-04-23, Limits 2026-09-05. 10만 파일은 Wrangler 4.34.0+ |
| Workers Cache (신규) | 별도 가격 없음 | — | **캐시 HIT도 표준 요청 단가** | — | "When caching is enabled, every request to your Worker is charged at the standard Workers request rate, including requests that are normally free: static asset requests and worker-to-worker invocations" (Workers Cache 2026-09-22) |
| Pages (신규 비권장) | 빌드 500/월, 동시 1빌드, 파일 20,000 | Pro 5,000 빌드 등 | Functions = Workers 과금 | Functions 요청은 Workers 할당량 차감 | Pages Limits 2026-09-05 |
| Workers KV | 읽기 100,000/일, 쓰기·삭제·list 각 1,000/일, 저장 1 GB | 읽기 1,000만/월, 쓰기·삭제·list 각 100만/월, 1 GB | 읽기 $0.50/100만, 쓰기·삭제·list $5.00/100만, 저장 $0.50/GB-월 | "If you exceed any one of these limits, further operations of that type will fail with an error." | Workers Pricing 2026-10-02, KV Limits 2026-04-21 |
| **KV Instant (private beta, 신규)** | 미공지 | 미공지 | 읽기(Class B) **$0.20 per million**, 쓰기·삭제·list(Class A) **$0.10 per operation**(100만 건당이 아님), 저장 **$100 per MB, per month** | — | [갭필 2026-10-03] blog 2026-10-01, §3-3 |
| D1 | 읽은 행 500만/일, 쓴 행 10만/일, 저장 5 GB(총), DB당 500 MB, DB 10개 | 읽은 행 250억/월, 쓴 행 5,000만/월, 5 GB | 읽기 $0.001/100만 행, 쓰기 $1.00/100만 행, 저장 $0.75/GB-월 | **2026-09-01부터 쿼리 실패**("Your account has exceeded D1's free tier daily row read limit...") + 이메일 | Workers Pricing 2026-10-02, D1 Limits 2026-04-21, Changelog 2026-09-01. Paid DB당 10 GB(상향 불가) |
| R2 | 10 GB-월, Class A 100만/월, Class B 1,000만/월 (Standard만) | (동일 구조) | Standard $0.015/GB-월, Class A $4.50/100만, Class B $0.36/100만. IA $0.01/GB-월, A $9.00, B $0.90, 조회 $0.01/GB | **무료 포함량 초과분은 과금(차단 아님)** — §2-4 [갭필] | R2 Pricing 2026-10-01. 이그레스 무료. "Cloudflare rounds up your usage to the next billing unit." |
| Durable Objects (SQLite) | 요청 100,000/일, Duration 13,000 GB-s/일, 읽은 행 500만/일, 쓴 행 10만/일, 저장 5 GB | 요청 100만/월, 40만 GB-s/월, 행 250억/5,000만, 5 GB-월 | 요청 $0.15/100만, Duration $12.50/100만 GB-s, 행 단가 D1과 동일, 저장 $0.20/GB-월 | Free는 SQLite 백엔드만 | Workers Pricing 2026-10-02. "Duration billing charges for the 128 MB of memory your Durable Object is allocated, regardless of actual usage." |
| Queues | 10,000 operations/일, 보존 24시간 고정 | 100만 operations/월, 보존 기본 4일·최대 14일 | $0.40/100만 operations | — | Workers Pricing 2026-10-02, Changelog 2026-02-04. "In most cases, it takes 3 operations to deliver a message: 1 write, 1 read, and 1 delete." 64 KB 단위로 1 op |
| Workflows | 요청 100,000/일(Workers와 공유), CPU 10 ms, 저장 1 GB-월, steps 3,000/일 | 요청 1,000만/월, CPU 3,000만 ms, 저장 1 GB-월, steps 50만/월 | 요청 $0.30/100만, CPU $0.02/100만 ms, 저장 $0.20/GB-월, steps $0.80/10만 | Free 저장 한도 도달 시 "will throw an error" | Workflows Pricing 2026-09-21. step·storage 과금은 "no earlier than August 10, 2026"(Changelog 2026-07-07) — 🕒 §9 |
| Cron Triggers | 계정당 5개 | 계정당 250개 | Workers 요청·CPU로 과금 | — | Workers Limits 2026-09-05 |
| Hyperdrive | 쿼리 100,000/일, 설정 10개, 원본 연결 ~20 | 쿼리 무제한, 설정 25개, 원본 연결 ~100 | 추가 요금 없음 | "further operations of that type will fail with an error" | Hyperdrive Pricing 2026-06-18, Limits 2026-06-09 |
| Workers AI | 10,000 Neurons/일 | 10,000 Neurons/일 | $0.011/1,000 Neurons | "further operations will fail with an error"; 일부 대형 모델(kimi-k2.6 등) Free는 403/5035 | Workers AI Pricing 2026-10-01, Changelog 2026-07-28 |
| AI Gateway | 핵심 기능 무료(분석·캐싱·레이트리밋) | — | 2026-09-24 이후 신규 로그는 Workers Logs 가격, Unified Billing 크레딧 5% 수수료 | spend limits(§2-3) | AI Gateway Pricing 2026-09-24 |
| Vectorize | 쿼리 3,000만 차원/월, 저장 500만 차원 | 쿼리 5,000만 차원/월, 저장 1,000만 차원 | 쿼리 $0.01/100만 차원, 저장 $0.05/1억 차원 | — | Vectorize Pricing 2026-04-21. 문서 내 불일치 §7 C-2 |
| Browser Run (구 Browser Rendering) | 브라우저 10분/일, 동시 3 | 10시간/월, 동시 10(월평균) | $0.09/시간, $2.00/추가 동시 브라우저 | — | Browser Run Pricing 2026-04-21 |
| Containers | **사용 불가** | 메모리 25 GiB-시간, vCPU 375분, 디스크 200 GB-시간 /월 | 메모리 $0.0000025/GiB-초, CPU $0.000020/vCPU-초(활성 사용분), 디스크 $0.00000007/GB-초. 이그레스: 북미·유럽 $0.025/GB(1 TB 포함), **오세아니아·한국·대만 $0.05/GB(500 GB 포함)**, 기타 $0.04/GB(500 GB) | — | Containers Pricing 2026-08-28. 앞단 Worker·DO 사용량 별도 과금 |
| Images | 고유 변환 5,000/월 | 5,000 포함 | 변환 $0.50/1,000, 저장 $5/10만 장, 전송 $1/10만 장 | **신규 변환 9422 에러, "You will not be charged for exceeding the limits in the Free plan."** | Images Pricing 2026-07-08 |
| Email Routing(수신) | 무제한 | 무제한 | — | — | Email Service Pricing 2026-06-09 |
| Email Sending(발신, 공개 베타) | 사용 불가(검증된 자기 주소로의 발송만 무료) | 3,000통/월 | $0.35/1,000통 | — | 同上 |
| Analytics Engine | 데이터포인트 100,000/일, 읽기 쿼리 10,000/일 | 1,000만 포인트/월, 100만 쿼리/월 | $0.25/100만 포인트, $1.00/100만 쿼리 | "Currently, you will not be billed for your use of Workers Analytics Engine." | AE Pricing 2026-04-23 |
| Workers Logs (현행, ~2026-11-30) | 20만 이벤트/일, 보존 3일 | 2,000만 이벤트/월, 보존 7일 | $0.60/100만 | — | Workers Pricing 2026-10-02 |
| Cloudflare Observability (2026-12-01~, Logs·Traces·Containers 로그 통합) | 수집 0.5 GB/일, 7일 보존 | 수집 50 GB/주기, 저장 12 GB-월/주기 | 수집 $0.25/GB, 저장 $0.10/GB-월 | **Free: 일 한도 도달 시 수집 중단**("Cloudflare stops ingesting new data when the account reaches its daily limit") / Paid: "Paid usage continues automatically after an allowance is exhausted." | Observability Pricing 2026-10-02 — 🕒 §9 |
| Workers Trace Events Logpush | 불가 | 1,000만 요청/월 | +$0.05/100만 | — | Workers Pricing 2026-10-02 |
| Logpush(일반, 전 플랜) | 내부 25 GB/월, 외부 25 GB/월, 변환 1 GB/월 | 同 | 내부 $0.03/GB, 외부 $0.10/GB, 변환 $0.04/GB | — | Changelog 2026-09-30 |
| Workers VPC | 오픈 베타 동안 무료(Workers 요금만) | — | — | — | Workers VPC Pricing 2026-09-16 — 🕒 §9 |
| Service bindings | — | 추가 요청 요금 없음(CPU는 합산) | — | — | "Requests made from your Worker to another worker via a Service Binding do not incur additional request fees." (Workers Pricing 2026-10-02) |

### 2-2. 보안·네트워크·캐시 [웹]

| 제품 | Free | 유료 | 비고·기준·출처 |
|------|------|------|----------------|
| Turnstile | 무료, 위젯 20개, "Unlimited challenges", 위젯당 호스트명 10개, 분석 7일 | Enterprise(문의) | Turnstile Plans 2026-08-14. "Turnstile can be used independently without requiring other Cloudflare services." |
| Cloudflare Tunnel | "Available on all plans" | — | Tunnel 2026-09-11. 터널당 replica 최대 25개(연결 100개) |
| Quick Tunnels | 계정 불필요, 무료 | — | "Each Quick Tunnel supports up to 200 in-flight requests. Additional requests return a 429 response." / "Quick Tunnels do not support Server-Sent Events (SSE)." (Quick Tunnels 2026-09-30) |
| **Zero Trust / Access 좌석** | **Free Plan "$0 forever", "Best for teams under 50 users", 사용량 행 "50 user limit"** | **Pay-as-you-go "$7 per user/month (paid annually)"**, "Best for teams over 50 users…", "No user limit" / Contract "Custom price per user/month (paid annually)" | [웹][갭필 2026-10-03] https://www.cloudflare.com/sase/products/access/ (페이지 날짜 표기 없음 → 검색 시점 2026-10-03). 좌석 소비 규칙: "A user consumes a seat when they perform an authentication event." (Seat management 2026-05-01). 상세 §3-6 |
| Access 계정 한도 | 앱 500, 서비스 토큰 50, IdP 50, 규칙당 이메일 1,000 | — | Account limits 2026-09-04 |
| WAF Free Managed Ruleset | 전 플랜, Free에 기본 배포 | Pro 이상 Cloudflare Managed Ruleset | "The Free Managed Ruleset is deployed by default on Free plans" |
| Rate Limiting rules (WAF) | **규칙 1개**, 기간 10초, 완화 10초, 필드 Path·Verified Bot, 카운팅 IP | Pro 2 / Business 5 / Ent 100 | 구버전(종량 과금)은 "no longer available" |
| Workers Rate Limiting 바인딩 | GA | — | `ratelimit` 바인딩, Changelog 2025-09-19 |
| Cache Rules | 10개 | Pro 25 / Business 50 / Ent 300 | Cache Rules 문서 |
| Tiered Cache / Smart Topology | Free 포함 | 同 | Generic Global·Regional·Custom 토폴로지는 Enterprise. Cloud region hint 전 플랜 무료 |
| Cache Reserve | 불가("A paid Cache Reserve plan is required.") | 저장 $0.015/GB-월, Class A $4.50/100만, Class B $0.36/100만 | "In most cases, a Cache Reserve miss will result in both one class A and one class B operation" / 2026-09-28부터 purge 시 Cache Reserve 콘텐츠도 강제 MISS |
| Request body 최대 (존 플랜) | 100 MB | Pro 100 MB / Business 200 MB / Ent 최대 5 GB | 초과 시 413. Workers Limits 2026-09-05 |
| CDN 캐시 객체 최대 | 512 MB | Ent 5 GB | 同上 |
| 계정 전용 고정 출구 IP | **없음(Enterprise 전용 제품)** | Smart Shield Advanced의 Dedicated CDN Egress IPs / Zero Trust Enterprise 애드온 dedicated egress IPs | [웹][갭필 2026-10-03] §3-9 |
| Analytics 보존 | 전 플랜 최소 30일 | — | Changelog 2026-10-02 |

### 2-3. 과금 보호 — 결론과 실제 장치

**결론: 2026-10-03 기준, Workers·Durable Objects·D1·R2 전체를 덮는 계정 단위 "하드 지출 상한(hard spending cap)"은 존재하지 않는다.**
- [웹] web.md: "계정 단위의 "하드 지출 상한(hard spending cap)"은 Cloudflare 1차 문서 어디에도 존재하지 않는다."
- [커뮤니티] community.md 결론(검색 시점 2026-10-03): "Workers·DO·D1·R2 전체를 덮는 계정 단위 하드 지출 상한은 여전히 없다. 알림(사후)과 차단(사전)은 다른 기능이다."
- 두 독립 리서치가 같은 결론. 책 표현 권장: "2026년 10월 현재, Cloudflare에는 계정 전체의 지출 상한을 거는 기능이 없다. 대신 아래 장치들을 겹쳐 쓴다." (출간 직전 재확인 §9)

실제 장치 (알림 ≠ 차단을 구분해 쓸 것):

1. **Budget alerts — 알림 전용 (Pay-as-you-go)**
   > "Budget alerts are informational only. They do not pause or cap usage. Your monthly invoice remains the authoritative source for billing." — Budget alerts 2026-05-29 기준, https://developers.cloudflare.com/billing/manage/budget-alerts/
   > "The alert is informational only. It does not cap your usage or impact your account in any way."
   > "Usage is processed once per day for the prior day's activity, so budget alerts fire the day after the threshold is reached rather than in real time."
   > "Budget alerts only consider spend on usage-based products. Recurring subscription fees, such as the Workers Paid plan fee or other monthly plan charges, are not included in the threshold calculation."
   — Changelog "Budget alerts now on by default", 게시 2026-07-20(URL 슬러그 2026-06-15, §7 C-14), https://developers.cloudflare.com/changelog/post/2026-06-15-budget-alerts-default-on/ — 적격 Pay-as-you-go 계정에 **$10 계정 단위 알림 자동 생성**, 다음 결제 주기부터 활성, 코호트 순차 적용, Enterprise 계약 제외.
   - Billable Usage 대시보드 + Budget alerts 도입: 2026-04-21 (Agents Week 2026 시기).
2. **Billable Usage 대시보드 / 제품 사이드바 위젯 — 가시성** — "The data comes from the same system that generates your monthly invoice, so the figures match your bill." (Changelog 2026-04-21) / 위젯은 "aligns to your billing cycle (or the current day on Free plans)" (Changelog 2026-06-04)
3. **Billable Usage API — 가시성(프로그래밍)** — "Today, usage and cost data are updated daily while we work towards providing more real time data." (blog 2026-08-03, https://blog.cloudflare.com/billable-usage-api/ , FOCUS 호환 컬럼). [추론] 자체 킬 스위치(Cron Worker가 API 폴링 → 라우트 해제·Worker 비활성화)의 유일한 공식 훅이지만 **하루 지연이라 실시간 차단 불가**, Cloudflare가 이 패턴을 문서화한 것은 아님. 커뮤니티 반응: "Translated: Close, but still not hard cost cap at Cloudflare." (HN mathoff, 2026-08-03, https://news.ycombinator.com/item?id=49158930)
4. **Usage-based billing notifications (제품별, Pro 이상 존)** — "The email notifications are for informational purposes only." (Usage-based billing 2026-05-29)
5. **Threshold billing — 상한이 아니라 중간 정산** — "When your combined usage charges across all usage-based products reach a certain level during a billing cycle, Cloudflare generates a mid-cycle invoice and charges your payment method on file." / "The threshold is automatically set by Cloudflare and cannot be modified." (Threshold billing 2026-06-16)
6. **Worker 단위 기술적 상한 — 실질적 비용 브레이크**
   - `limits.cpu_ms`: "To prevent accidental runaway bills or denial-of-wallet attacks, configure the maximum amount of CPU time that can be used per invocation" (Workers Pricing 2026-10-02). 기본 30,000 → 최대 300,000
   - `limits.subrequests`: "To protect against runaway code or unexpected costs, you can also set a lower limit for both subrequests and CPU usage." (Changelog 2026-02-11, 예시 `"subrequests": 10, "cpu_ms": 1000`)
   - 레거시 Bundled 모델에서 이관된 Worker는 50 ms CPU 한도 자동 부여 (Workers Pricing)
   - DO: WebSocket Hibernation으로 유휴 Duration 과금 중지 — "billing pauses while the Durable Object is hibernated" (Optimize costs 2026-05-04)
   - Workflows: `default_retention`으로 보존 기간 단축 → 저장 과금 절감
   - ⚠ 이 상한들은 **호출 단위**다. 호출 횟수 자체(루프·DDoS성 트래픽)는 막지 못하므로 아래 7·8과 겹쳐야 한다 [편집 판단].
7. **Free 플랜 = "청구 대신 에러" (제품별, 문서 확인분)** — Workers 1027 / KV·Hyperdrive·Workers AI "fail with an error" / D1 2026-09-01부터 실패+이메일 / Images 9422 + "You will not be charged" / Observability(2026-12-01~) 수집 중단 / 정적 자산 `run_worker_first` 429. 커뮤니티 휴리스틱: "The safest way to use Workers is on the free tier, which will shut off after 100,000 requests/day" (simonw, HN 2026-06-20, https://news.ycombinator.com/item?id=48611258).
   - ⚠ **예외: R2는 이 목록에 들지 않는다** — 무료 포함량 초과분은 과금된다(§2-4).
   - 대가: 무료 한도는 비용을 지키지만 가용성을 희생 — dev.to eliasoliedev(2026-01-10 무렵)의 앱이 트래픽 폭주로 무료 할당량을 소진해 사용자에게 Error 1101 계열 화면이 노출됨(같은 날 Railway는 하드 지출 한도로 정지). "Sometimes the bottleneck isn't code, it's the budget configuration." [커뮤니티]
8. **AI Gateway spend limits — 실제 차단, 단 AI Gateway 한정** — 달러 예산 초과 시 요청 차단. **AI Gateway 트래픽에만 적용, 계정 전체 상한 아님.** [커뮤니티 `[문서화]`] https://developers.cloudflare.com/changelog/post/2026-06-05-spend-limits/ (2026-06-05)
9. **WAF·Rate Limiting을 Worker 앞에** — Free 존도 Rate limiting rule 1개(10초 기간)·Free Managed Ruleset 기본 배포, Workers `ratelimit` 바인딩 GA(2025-09-19). ⚠ **커스텀 도메인 사용 시 `workers.dev`를 꺼야 성립** — `workers.dev`로 들어오면 존 WAF를 우회한다(HN white_viel 2026-02-25, kentonv 답변 "you can disable the workers.dev zone by putting `"workers_dev": false,` in wranlger.jsonc" — 원문 오타 'wranlger' 그대로, https://news.ycombinator.com/item?id=47156303). 대안: 2026-08-14부터 Worker 단위/계정 전체 Access 보호("Make all Workers private by default…").
10. **커뮤니티 자작 서킷 브레이커** — Little Bear Apps: 기능별 예산·프로젝트 합산·전역 비상 정지 3단, 70%/90%/100%에서 단계적 경고·자동 비활성화, KV TTL로 1시간 뒤 자동 해제, 탐지 지연 약 30초 (https://littlebearapps.com/blog/d1-billing-disaster-circuit-breakers/ , 2026-03-18) [커뮤니티 `[일화]`]. Show HN "A usage circuit breaker for Cloudflare Workers"(ethan_zhao, 2026-03-10, https://news.ycombinator.com/item?id=47322794).

### 2-4. R2: Free 범위를 넘으면 차단이 아니라 과금 [갭필 2026-10-03]
- [웹] R2 Get started (dateModified 2026-04-21), https://developers.cloudflare.com/r2/get-started/ :
  > "You need a Cloudflare account with an R2 subscription."
  > "Complete the checkout flow to add an R2 subscription to your account."
  > "R2 is free to get started with included free monthly usage. You are billed for your usage on a monthly basis."
- [웹] R2 Pricing (Last updated 2026-10-01), https://developers.cloudflare.com/r2/pricing/ — 청구 예시 표가 "Usage | Free Tier | Billable Quantity | Price" 구조로, 무료 포함량을 뺀 나머지를 과금한다(예: 1,000 GB-months 사용 → Free Tier 10 GB-months → Billable 990 GB-months → $14.85). "The free tier only applies to Standard storage, and does not apply to Infrequent Access storage."
- 부수 사실(1차): "Will I be charged for unauthorized requests to my R2 bucket? No. You are not charged for operations when the caller does not have permission to make the request (HTTP 401 `Unauthorized` response status code)." / 삭제류(`DeleteObject`, `DeleteBucket`, `AbortMultipartUpload`)는 무료 연산.
- 판정: **[1차 문서 2건 종합] R2는 "무료 포함량 + 종량 과금" 구조이며 Free 범위 초과 시 차단하지 않고 과금한다.** 잔여 공백: "차단하지 않는다"를 문자 그대로 적은 문장은 없다 — 책 권장 표현: "R2는 결제수단을 등록한 구독 위에서 동작하고, 매달 무료 포함량을 넘는 사용분은 그대로 청구된다(R2 문서 2026-10 기준)."
- 커뮤니티 맥락: 카드 등록 자체에 대한 불안 — Reddit u/alwerr "I was thrilled to use Cloudflare Pages+D1 until saw R2 need Credit Card" (2026-03 무렵, 미러 경유); 한국어 후기 "무료 한도가 있어도 R2를 활성화하려면 Dashboard에서 R2 구독 Checkout 절차를 완료해야 합니다. 계정 상태에 따라 결제수단 등록을 요구할 수 있어" (잡가이버, 2026-08-07, https://jab-guyver.co.kr/7280) [웹-3자].

### 2-5. "깜짝 청구서" 함정 목록 (책에서 경고할 것)
문서화된 함정 [웹]:
1. **Workers Cache를 켜면** 평소 무료인 정적 자산 요청·Worker 간 호출까지 요청 단가로 과금 (Workers Cache 2026-09-22)
2. "Since Cloudflare Workers runs before the Cloudflare cache, the caching of a request still incurs costs." (Workers Pricing Fine Print)
3. DO Duration은 실제 사용과 무관하게 128 MB 기준, `accept()`한 WebSocket은 연결 내내 Duration 과금 → Hibernation API 사용
4. Queues: 배치·재시도마다 메시지별 operation 과금, 64 KB 초과 메시지는 여러 op
5. D1: 인덱스 없는 풀 스캔은 반환 행이 적어도 스캔한 행 전부가 "rows read"
6. R2: 단위 올림 — "If you have performed one million and one operations, you will be billed for two million operations." + Free 초과분 과금(§2-4)
7. Containers 이그레스: 한국 $0.05/GB로 북미·유럽($0.025/GB)의 2배, 포함량도 500 GB vs 1 TB
8. Free/Pro/Business의 Tunnel 공개 호스트명으로 대용량 비디오 서빙은 약관상 유료 서비스 필요: "On Free, Pro, and Business plans, the service-specific terms require you to use a specific paid service to serve video and other large files." (Cloudflare One Tunnels FAQ, https://developers.cloudflare.com/cloudflare-one/faq/cloudflare-tunnels-faq/)
9. Paid 계정 Observability(2026-12-01~): "Paid usage continues automatically after an allowance is exhausted."
10. **KV Instant(private beta)**: 쓰기·삭제·list가 **$0.10 per operation**, 저장 **$100 per MB, per month** — classic KV 감각(100만 건당 $5)으로 쓰면 수만 배 비싸다. 용도는 드물게 바뀌는 설정·플래그 [갭필 2026-10-03, §3-3]
11. Budget alerts는 하루 늦게 오고, Workers Paid 월 기본료는 임계치 계산에서 빠진다

커뮤니티 실사례 [커뮤니티 `[일화]`, 금액 원문 그대로]:
- **$34,895** — HN thewillmoss(2026-04-16, 31점, https://news.ycombinator.com/item?id=47787042): DO `onStart()`가 깨어날 때마다 alarm 존재 확인 없이 `setAlarm()` + 60개 이상의 preview Worker 배포가 각자 DO 인스턴스 생성 → 자기 헬스체크 루프. "April 4-5: peaked at ~930 billion row reads/day … April 15: $34,895 invoice due with no billing response yet". "Cloudflare's Workers Usage Notifications only monitors CPU time. Not Durable Object row reads or writes." ⚠ **환불·면제 결말 미확인** — "면제받았다"고 쓰지 말 것.
- **$4,868** — Little Bear Apps(Nathan Schram, 게시 2026-03-18, 사건 2026-01): D1 쓰기 48.3억 건, 버그 두 개(중복 제거 누락, `ON CONFLICT` 누락), $5/월 계정, 하루 최대 $1,411.40. 결말: 18일 만에 $4,586.64 면제, 계정 복구. 분쟁 보류 중 자동 정지됐다는 r/CloudFlare 글(2026-02-18, 원문 미열람·블로그 인용 경유).
- **$48** — helloacm(2022-08-25, 오래됨 — 지금도 유효): 공개 API 월 1억 634만 요청.
- 한국 — 다모앙(2025-12-13) 댓글: 로깅을 실수로 켰다가 하루 50만 원 이상 청구 (요약 경유, **원문 문장 재확인 필요**).
- ⚠ "RetainDB 사이드 프로젝트 81명 사용자, $36,000" 사례는 검색 스니펫뿐 — **인용하지 말 것.**
- 커뮤니티 공유 진단: (1) Free는 사실상의 하드캡, 유료로 올리면 브레이크가 사라진다 (2) 사용량 알림이 오래 CPU time만 감시 (3) 루프의 원인은 대개 자기 코드(alarm 재등록, 프리뷰마다 DO, `ON CONFLICT` 누락, cron 남발).

---

## 3. 핵심 내용 — 커버리지 순서별

### 3-1. 간단한 웹사이트 (정적 사이트 → SPA)
- **새 사이트는 Workers + 정적 자산.** Pages 신규 비권장(§0-6), Workers Sites 폐기(§0-7). [웹]
- 정적 자산 무료·무제한: "Requests to static assets are free and unlimited" (Static Assets Billing 2026-04-23). React SPA: "`assets.not_found_handling` is set to `single-page-application`, which means that routes that are handled by your React SPA do not go to the Worker, and are thus free." (React 가이드) [웹]
- `@cloudflare/vite-plugin` (2026-09-30 기준): "Your Worker code runs inside workerd, matching the production behavior" / "Official support for TanStack Start and React Router v8 with server-side rendering" / "Produces standard Build Output for `cf build` and `cf deploy`". 2025-12-08 Changelog: "Wrangler config is optional when using Vite plugin". [웹]
- C3: "`npm create cloudflare`, powered by the `create-cloudflare` package" (최신 create-cloudflare 2.73.2, 2026-10-02). `wrangler deploy` 자동 구성 GA — "Starting with Wrangler **4.68.0**, running `wrangler deploy` automatically configures your project by detecting your framework, installing required adapters, and deploying it" (Changelog 2026-02-25). [웹]
- 기존 Pages 사용자 박스 — 마이그레이션 가이드: "Like Pages, requests for static assets on Workers are free, and Pages Functions invocations are charged at the same rate as Workers, so you can expect a similar cost structure" / "Unlike Pages, Workers has a distinctly broader set of features available to it, (including Durable Objects, Cron Triggers, and more comprehensive Observability)." `functions/` → `npx wrangler pages functions build --outdir=./dist/worker/`. [웹] https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/
  - 현장 반응: "following it is no walk in the park." (Bryce Wray, 2025-05-27) — Pages Functions 단일 파일화, CSP 헤더·장기 캐시 재설계. "Configs that worked in Wrangler 3 didn't carry over cleanly to Wrangler 4" (HN aperture147, 2025-10-15). Cloudflare 공식 입장(Bryce Wray 인용): "Cloudflare Pages will continue to be supported, but, going forward, all of our investment, optimizations, and feature work will be dedicated to improving Workers." [커뮤니티]
- 한국어 현장 근거: "도메인만 구입하고 Cloudflare 무료 플랜을 활용하면 호스팅비 없이 DB가 연결된 개인 홈페이지나 소형 블로그를 운영할 수 있습니다." (잡가이버 2026-08-07, 수치는 공식 문서와 일치 확인) [웹-3자]
- 무료 정적 자산을 지키는 주의: Workers Cache를 켜면 정적 자산도 과금(§2-5 #1). `run_worker_first` 경로는 Worker 호출로 계산.

### 3-2. 웹 서비스·앱 (Next.js·React·Node.js·Hono·Python)
**Next.js**
- 공식 권장 = vinext (§0-5). 원문: "vinext gives you two starting points: scaffold a new Workers-ready app with `create-vinext-app`, or add vinext to an existing Next.js 16 app with a single non-destructive `vinext init` (your existing `next dev` keeps working)." / "vinext is a Vite plugin that reimplements the Next.js API surface." / "vinext is in beta. Before adopting it for an existing production application, run the compatibility check from your project directory" (`npx vinext check`) — [웹] 가이드 2026-08-25
- OpenNext 페이지: "Cloudflare recommends vinext instead of OpenNext for new Next.js applications on Cloudflare Workers. Use this guide to maintain an existing OpenNext application. Migrate to vinext when compatibility allows." [웹] 2026-08-25
- 기능표: vinext(2026-08-25 문서) App Router·Pages Router·RSC·Server Actions·SSR·SSG/static export·ISR·middleware/`proxy.ts` 지원, `next/*` "Mostly supported", Image optimization "Partially supported". OpenNext: `"use cache"`(Composable Caching)·PPR "Supported"(Next.js 실험 기능), "Node.js in Middleware — Not yet supported". [웹]
- vinext 1.0 발표(James Anderson, Matt "TK" Taylor, 2026-09-28, https://blog.cloudflare.com/vinext-nextjs-on-vite/):
  > "When we launched Vinext in February, it was the result of an audacious week-long AI-driven experiment"
  > "Vinext lets you take any Next.js application, whether it was built for the Pages or App Router, and make it portable to be deployed to any web platform, including the Cloudflare Workers free plan, Netlify, or AWS Lambda."
  > "Our test compatibility has risen to more than 99%, excluding cache components."
  > "Vinext today has limited support for the "use cache" directive that drives Cache Components"
  > "We also run the Next.js end-to-end test suite against Vinext nightly"
  - 1.0.0 릴리스 노트: "Init: default Cloudflare projects to cf", "replace deploy prerendering with cache warming", "rename cdnAdapter to workersCacheCdnAdapter"
  - [편집 판단] `"use cache"`에 의존하는 앱은 당분간 OpenNext 유지가 합리적일 수 있음
- 보안(Changelog 2026-05-07): "Patched versions are available for React (`react-server-dom-webpack`, `react-server-dom-parcel`, and `react-server-dom-turbopack` `19.0.6`, `19.1.7`, and `19.2.6`) and Next.js (`15.5.16` and `16.2.5`)." / "Vinext's latest release is not vulnerable to any of the disclosed CVEs." / "Several of the disclosed vulnerabilities are not possible to block in WAF. We strongly recommend updating your applications so they are not purely reliant on WAF mitigations." [웹] → "WAF는 패치를 대체하지 않는다"
- 커뮤니티 고통(OpenNext 버전 지연) [커뮤니티]: #972 "Next16 support"(2025-11-04, 39댓글, closed), #1049 Next.js 16.1.0 Error 1101 `setImmediate`(2025-12-19 → closed 2026-01-16, "Downgrading to 16.0.10 fixed it immediately."), #1157 16.2.0 `prefetch-hints.json`(2026-03-18, closed), #653 "Performance is unusably slow" TTFB 1.2~3초(2025-05-08, 33댓글; 2025-10 CPU 벤치 논란 후 V8 GC 튜닝·스트림 버퍼 중복 제거 반영 — 부분 해소, 검증 필요), **#1214 Hyperdrive + node-postgres `pg-cloudflare` 해석 실패(2026-04-20, open; 2026-09-18에도 "Had same issue using next 16.3")** — 우회: `next build --webpack` 또는 `outputFileTracingIncludes`에 pg-cloudflare 추가. next-on-pages deprecated 후 Next 16에서 함수당 산출물 5~10KB → 약 500KB(r/nextjs 2025-12-06 무렵, 미러 경유). "its really annoying that nextjs has to be forked and/or patched to work on cloudflare." (HN orliesaurus, 2025-10-15)
- vinext 반응 [커뮤니티]: HN "How we rebuilt Next.js with AI in one week"(2026-02-24, 540점·236댓글) — 기대(hungryhobbit) / 신중(thawab: "I am not touching an AI version without waiting for a while.") / 품질 의문(slopinthebag: "does it actually handle the edge cases or does it just pass the tests."). 보안 지적: "Vulnerabilities in Cloudflare's vinext disclosed by Vercel"(2026-02-26), hacktron "Vibe-Hacking…"(2026-02-28) `[이해관계자: Vercel 측 공개]`. **1.0(2026-09-28) 이후 실사용 후기는 거의 없음(HN 4점)** [리서치 공백].

**Node.js 호환**
- "For compatibility dates of `2026-08-04` or later, Workers enables both `nodejs_compat` and `nodejs_compat_v2` by default." / "For compatibility dates from `2024-09-23` through `2026-08-03`, add the `nodejs_compat` compatibility flag" / "npm packages that depend on these APIs will work without additional configuration." / 일부 모듈은 "As polyfill shim implementations that Wrangler adds to your Worker's code, allowing it to import the module, but calling API methods will throw errors." / 끄기: `"compatibility_flags": ["no_nodejs_compat", "no_nodejs_compat_v2"]` — [웹] Node.js 문서 2026-08-12
- `node:fs` 기본 제공(2025-08, compat date 2025-09-01 이상) → body-parser, jsonwebtoken, knex, passport 로드 가능 — [커뮤니티 `[문서화]`] https://developers.cloudflare.com/changelog/post/2025-08-15-nodejs-fs/ . 2024년 이전 "npm 패키지가 안 돈다" 불만은 상당 부분 해소, 대신 프레임워크가 Node 내부를 건드리는 지점에서 새 문제(#1049).
- 모듈 레지스트리 재작성 — https://blog.cloudflare.com/workers-module-registry-nodejs/ (2026-09-09) [웹]

**런타임 한도·성능**
- Error 1102, 메모리 128MB는 isolate 단위로 동시 요청이 공유, Paid CPU 기본 30초·최대 5분 — 커뮤니티 요약값이 1차(Workers Pricing 2026-10-02)와 일치. 동시 연결: "Each Worker invocation can have up to six connections simultaneously waiting for response headers." / "Once response headers arrive for a connection, it no longer counts toward the six-connection limit." (Changelog 2026-04-09 완화) [웹]
- "Using global `fetch()` to call another Worker on the same zone without service bindings fails." (Workers Limits) [웹]
- 성능 논쟁: Theo Browne 벤치(Vercel Node 대비 최대 3.5배 느림)에 Cloudflare가 응답(스케줄링 개선, V8 young generation 제약 제거, JSON.parse 패치) — HN 45584281(2025-10-14, 317점) `[이해관계자: Cloudflare 블로그]`. nisten: "nextjs being 4 times slower latency wise than plain react or even vanilla js is pretty funny" [커뮤니티]
- 다모앙(띠부씰, 2025-12-13, https://damoang.net/development/2488): 무료에서 1~2초, LA 라우팅 사례, 유료+Smart Placement로 "체감상 아주 조금, 한 10~20% 정도는 빨라진 느낌", Argo Smart Routing(도메인당 $5/월) 추가 시 "눈에 띄게 빨라졌고", 최종 월 $10 [커뮤니티 `[일화]`]. Smart Placement: "Smart Placement is available on all Workers plans." / "Smart Placement may take up to 15 minutes to analyze your Worker after deployment." [웹]
- Placement Hints(2026-01-22): `"placement": { "region": "aws:us-east-1" }`, "Placement hints support Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure region identifiers." [웹]

**Hono / Python** — Hono 가이드 https://developers.cloudflare.com/workers/framework-guides/web-apps/more-web-frameworks/hono/ , Python Workers GA(2026-09-21). [웹]

### 3-3. 데이터·상태 (D1·KV·KV Instant·DO·Queues·Workflows)
**D1**
- 한도는 §2-1. 2026-09-01부터 Free 일일 한도 실제 강제(쿼리 실패 + 이메일). Paid DB당 10 GB(상향 불가). [웹]
- 트랜잭션 한계: "a transaction cannot span multiple D1 requests, so you can't select from the database, execute application logic, and then write to the database in an atomic way." (HN kpozin, 2025-04) — batch 첫 문장에 일부러 JSON 파싱 오류를 내 나머지를 중단시키는 편법. GitHub workers-sdk #2733 "D1 Transaction support"(2023-02, 42댓글, 반응 1위, closed). [커뮤니티]
- "I evaluated D1 for a project a few months ago, and found that global performance was pretty terrible."(fastball, 2025-04) — D1 read replication이 같은 달 공개돼 일부 완화됐을 수 있음(검증 필요). "The only real application I found so far are small projects where less than 5 tables are needed and no JOINs are required."(piterrro) [커뮤니티]
- 대량 삽입: `wrangler d1 execute`가 REST API보다 "~100× slower"(r/CloudFlare u/tcoder7, 2026-06 무렵, 미러 경유) [커뮤니티 `[일화]`]
- ⚠ 호출당 쿼리 수 문서 불일치(§7 C-11).

**KV (classic)**
- 최종 일관성, 키당 초당 1회 쓰기. 커뮤니티 실패담(Kuryzhev, dev.to 2026-07-01): KV를 강한 일관성 저장소처럼 씀(전파 최대 60초), 키당 쓰기 제한 무시, API 키를 그대로 KV 키로 → 카운팅은 사용자당 DO로, KV는 느리게 바뀌는 설정에만 → 비용 약 40% 감소(본인 주장). "If your rate limiter can fail in a way that produces zero errors, you need a metric specifically watching for that — not just error rate." [커뮤니티]
- "없음" 결과도 캐시된다(검색 요약 경유, 문서 대조 필요).

**KV Instant — 2026-10-01 발표, private beta** [웹][갭필 2026-10-03]
- 출처: Rob Sutter, "Introducing Workers KV Instant — powered by Quicksilver", Cloudflare Blog, 2026-10-01 (Birthday Week), https://blog.cloudflare.com/workers-kv-instant/
- 무엇이 바뀌었나: **기존 KV를 바꾼 것이 아니라 새 "모드"가 추가됐다.** "Today, we're introducing Workers KV Instant, a new mode for Workers KV that pushes your changes globally for instant availability without cold read penalties." / "KV Instant mode provides the same API as Workers KV, but powers it using Quicksilver." Cloudflare 내부 KV(Quicksilver v2)를 처음 고객에게 개방.
- 성능 원문: "KV Instant offers read latency that is over 100 times faster than classic mode, with reads resolving in under two milliseconds even at the 99th percentile of response time (p99), and 95th percentile (p95) times measured in microseconds. Writes are pushed to the edge over 20 times faster, with 99% of all writes replicating in around 250ms."
  - 블로그 표: Instant — p99 reads(all) 1.62 ms, median write replication 107 ms, p95 181ms, p99 256 ms (각주 "Time to replicate to all edge locations (over 300 as of publication)"). Classic — p99 reads(cached) 160 ms, p99 reads(all) 287 ms, median·p95 "< 1 s", p99 4.38 s (각주 "Time to replicate across all required storage backends", "We do not have sub-second fidelity for replication lag in classic mode").
- 용도: "It's not for every type of data, but, for infrequently updated application configuration data — the same thing we use Quicksilver for ourselves — KV Instant shines." / "If you need to store large amounts of data, or update it frequently, Workers KV continues to be a great fit."
- 사용법·차이: "You must specify KV Instant mode when creating a KV namespace." (`"mode": "instant"`), 메타데이터 미지원, `list`는 페이지네이션 없이 전부 반환.
- 한도: "Each key can be up to 300 bytes, and values can be any size that does not cause the namespace to exceed one megabyte in total size. KV Instant namespaces can contain up to 10,000 key value pairs of any type." / "KV Instant also restricts write frequency to one write per namespace per second." (classic은 키당 초당 1회)
- 가격: Class B(reads) "$0.20 per million"(classic $0.50 대비 "60% less"), Class A(put·delete·list) "**$0.10 per operation**", Storage "**$100 per MB, per month**". "Each list request counts as one Class A operation, regardless of how many keys are returned". 여러 키를 한 번의 get으로 요청해도 키당 Class B 1회.
- 상태: "KV Instant is launching today in private beta." GA 일정 미공지.
- 책 권장 표현: "2026년 10월 Cloudflare는 KV에 'Instant' 모드(비공개 베타)를 추가했다. 기존(classic) KV의 최종 일관성 동작은 그대로이며, Instant는 1 MB·1만 키 이하의 드물게 바뀌는 설정용이다." classic KV 일관성 설명(§1-5, §5 휴리스틱 4)은 유지.

**Durable Objects**
- 신규 네임스페이스 SQLite 전용(2026-07-09). SQLite-backed DO 스토리지 과금: 공지 2025-12-12, "target date of January 7, 2026", Free는 과금 없음 — **실제 개시 확정 공지 미확인**(§7 C-5, 🕒 §9). [웹]
- 128 MB Duration 과금, Hibernation 권장(§2-5). alarm 루프 함정과 처방: §5 휴리스틱 2.

**Queues** — Free 포함(2026-02-04, 일 10,000 ops), 메시지당 대개 3 ops. HTTP pull 소비자(외부 JVM 워커가 소비 가능): "HTTP Pull consumers require an API token with the `com.cloudflare.api.account.queues_read` and `com.cloudflare.api.account.queues_write` permissions." 요청 예 `{ "visibility_timeout_ms": 10000, "batch_size": 2 }`, `visibilityTimeout` 최대 12시간. 2026: Email Sending 이벤트 구독(2026-07-15), Workers Builds 이벤트 구독(2026-01-09). [웹]

**Workflows** — step 과금 "no earlier than August 10, 2026"(Changelog 2026-07-07), 보존 기간·스크립트 크기 문서 불일치(§7 C-3·C-4). [웹]

**선택 가이드(논쟁 B 연결)** — kentonv `[이해관계자: Cloudflare Workers 리드 엔지니어]`(HN 2026-04-08, https://news.ycombinator.com/item?id=47696640): "The 10GB limit applies to one database, but the idea is you design your system to split data into many small databases, e.g. one per user, or even one per document. … If you really need a single big database, you can use Hyperdrive, which provides connection management and caching over plain old Postgres, MySQL, etc." 반대: keeda "The 10GB limit per DB is unsuitable for even trivial use-cases." HN "Cloudflare's AI Psychosis"(2026-08-15, 120점) 원문 "Too many ways to do the same thing, none of them great" ↔ hasyimibhar(각각 한 줄로 정리 가능). [커뮤니티] → Spring/JPA 독자의 "DB 하나에 스키마 하나" 전제를 깨는 장으로 다룰 가치.

### 3-4. JVM(Java/Kotlin/Spring Boot) 백엔드는 어디에 두나
- **Workers에는 JVM이 없다.** 1급 언어 JS/TS/Python/Rust, 나머지는 Wasm(단일 스레드, WASI 실험적). Kotlin/Wasm은 **Beta**: "Although Kotlin/Wasm is still in Beta, Compose Multiplatform running on Kotlin/Wasm already shows encouraging performance traits." / "Kotlin/Wasm uses the WebAssembly System Interface (WASI) for backend applications." (kotlinlang.org 2026-09-01) [웹] → [추론] Kotlin 백엔드를 Workers로 옮기는 것은 현실적 주력 경로가 아님.
- TeaVM 실험(Gregory Mitchell, dev.to 2024-08-31) [웹-3자, 2년 경과]: "It uses TeaVM to compile Java into WebAssembly usable by the Cloudflare Workers runtime." / "`java.util.concurrent` and other threading operations are not included and will result in a compilation error." ⚠ 글의 "3 MiB after gzip" 크기 제한은 2026-09-04 폐지된 구정보.
- Kotlin/JS: 코루틴·stdlib 초기화로 요청당 100~200ms 지연 보고(kotlinlang Slack, 2023 무렵 추정, 오래됨, 검색 요약 경유). Kotlin/Wasm 이후 유효성은 [리서치 공백]. [커뮤니티]
- **Cloudflare Containers — Spring Boot의 현실적 착지점** [웹] (문서 2026-09-30, FAQ 2026-10-02, GA 2026-04-13, Workers Paid 전용):
  > "Run code written in any programming language, built for any runtime, as part of apps built on Workers."
  > "Your container image must be able to run on the `linux/amd64` architecture, but aside from that, has few limitations."
  > "Container cold starts can often be in the 1-3 second range, but this is dependent on image size and code execution time, among other factors."
  > "Is built-in autoscaling for stateless applications available? Not today, though Cloudflare plans to add built-in autoscaling in a future release."
  > "Memory and disk usage are based on the *provisioned resources* for the instance type you select, while CPU usage is based on *active usage* only."
  - 인스턴스 타입(2026-09-30): lite 1/16 vCPU·256 MiB·2 GB / basic 1/4·1 GiB·4 GB / standard-1 1/2·4 GiB·8 GB / standard-2 1·6 GiB·12 GB / standard-3 2·8 GiB·16 GB / standard-4 4·12 GiB·20 GB. 커스텀 vCPU 1~4, 메모리 최대 12 GiB, "Minimum 3 GiB memory per vCPU". 계정 동시 한도 메모리 6 TiB·vCPU 1,500·디스크 30 TB, 이미지 저장 50 GB.
  - 인스턴스마다 Durable Object가 붙고 Worker 코드가 수명주기 제어, `getRandom` 헬퍼로 무상태 분산.
  - 2026 변화: Docker Hub 이미지(2026-03-24), Google Artifact Registry(2026-07-01), SSH(2026-03-12, 2026-05-12부터 기본 ON), `exec()`(2026-06-18), R2 FUSE 마운트(2025-11-21), 스냅샷(2026-09-30), `durable_object` 스케줄링 정책 + "starts Containers more than 6x faster"(blog 2026-09-30, https://blog.cloudflare.com/faster-agent-sandboxes/). CPU 과금 활성 사용량 기준(2025-11-21).
  - [추론] Spring Boot 적합성: 공식 문서에 "Spring Boot" 언급 없음. JVM 힙 고려 시 `standard-1`(4 GiB) 이상 무난, 콜드 스타트는 sleep 타임아웃 정책 + CRaC/GraalVM 네이티브 이미지 검토, 상시 가동 월 비용은 메모리 프로비저닝분이 지배 — **저자가 계산 예시로 검증할 것.**
  - 보안 이력: 2026-09-04 보고된 교차 테넌트 잔여 디스크 블록 노출 — 수정 완료, 악용 증거 없음. "a customer with a Workers Paid account could recover residual disk blocks previously used by Containers on the same host" (blog 2026-09-24)
  - 커뮤니티 [커뮤니티]: 긍정 — rozenmd "This is the perfect use of cloudflare containers. Rare, bursty workloads that fit around regular use of Workers. … not even noticeable in billing."(HN 2026-03-14~15), meerab(R2 FUSE + FFmpeg, "files never hit the public internet."), NicoJuicy "Cloudflare Containers is literally 'pay for usage', while AWS is pay for capacity."(2025-11-24). 부정 — detuks "Feels like it is the nost expensive product they have."(원문 오타 그대로), youngbum(walla.my, 2026-05-21) "We also tried Cloudflare Containers, but they weren't as reliable as just spinning up a small VM. 1vCPU and 1GB RAM were enough to synchronize about 3,000 users.", Wire(2026-07-07) 배치 경직성 — 단 "This is not a 'we left Cloudflare' post. … the API, the frontends, the control plane, and processing all still run on Workers." 경쟁 PaaS sliplane `[이해관계자: 경쟁 PaaS 공동창업자]`: 상시 standard(4GiB) 월 약 $82.44, 일반 PaaS의 5~10배.
  - ⚠ 콜드 스타트 수치 충돌 — §7 C-16.
- **인바운드 TCP·gRPC (private beta)** — "connect(socket) — a new handler in the Workers runtime that lets your Worker directly accept an inbound TCP socket provided by Spectrum" / "Full-duplex, bidirectional gRPC from Cloudflare Containers — forward the socket from your Worker to your gRPC server running in a container" / "We're introducing this in private beta" (blog 2026-08-03, Mar Witek·Thomas Rubini) [웹] → 전망으로만.
- **JVM을 Cloudflare 밖에 두는 정석** [웹]:
  1. Tunnel로 VPS·홈서버·타 클라우드의 Spring Boot 공개 — "Map public hostnames to local services (for example, `app.example.com` to `http://localhost:8080`)." / "Traffic flows through Cloudflare's network to your origin, with full CDN and security applied."
  2. Workers VPC로 Worker → 사설 Spring API — "Workers VPC allows you to connect your Workers to your private APIs, services, and databases in external clouds (AWS, Azure, GCP, on-premise, and others) that are not accessible from the public Internet." / "While in beta, Workers VPC is available for free to all Workers plans."
  3. Placement Hints로 기존 클라우드 리전 옆에서 Worker 실행
  4. Hyperdrive로 Spring Boot와 Worker가 같은 Postgres/MySQL 공유
  5. Queues HTTP pull로 JVM 워커가 Cloudflare 큐 소비
  6. R2를 AWS SDK for Java v2로(§3-9)
- [리서치 공백] Spring Boot를 Tunnel 뒤에 두거나 Containers로 JVM을 올린 구체적 실사용기 0건(HN 검색 "cloudflare tunnel spring boot" 0건). 단서: Fränkel(Java Champion)의 Zero Trust→Tailscale 이주, cloudflared gRPC 이슈 #491. → 저자 실험으로 채울 장.

### 3-5. 그 밖의 서비스 (메일·AI·브라우저·이미지)
- **Email Service** = Email Routing(수신, 무제한 무료) + Email Sending(발신, 2026-04-16 공개 베타, Workers Paid 3,000통/월 포함). "Send transactional emails directly from Workers (`env.EMAIL.send()`) or the REST API". SMTP(2026-06-08 베타): `smtp.mx.cloudflare.net:465`, 사용자명 `api_token`, 비밀번호 = "Email Sending: Edit" 권한 API 토큰 → [추론] Spring Boot `JavaMailSender`로도 발송 가능(SMTP 표준). "New accounts start with a conservative daily quota and scale up over time based on your sending behavior". 메시지 최대 5 MiB(첨부 포함), 수신자 50명/통, 라우팅 규칙 200개/도메인(Limits 2026-09-25). Wrangler로 라우팅 규칙(2026-09-04). [웹]
- **Workers AI** — 10,000 Neurons/일, 일부 대형 모델 Free 차단(403/5035, 2026-07-28). ⚠ 모델별 단가는 교체가 잦아 본문에는 Neuron 단가만 권장(web.md 방침). Reddit 일화의 "5,000 neurons/day"와 충돌 — §7 C-19. [웹]
- **AI Gateway** — 핵심 기능 무료, spend limits는 AI Gateway 한정 차단(§2-3 #8). DLP: "Accounts without a Zero Trust subscription have access to two predefined DLP profiles: Financial Information and Social / Insurance / National Identifier Numbers." [웹]
- **Browser Run(구 Browser Rendering)** — 가격 §2-1. Wrangler 세션 관리 changelog 2026-04-14. [웹]
- **Images** — 초과 시 9422, Free 과금 없음. [웹]
- **Analytics Engine** — 현재 미과금, 과금 개시 미정(§7 C-6). [웹]
- **Turnstile** — §3-7.

### 3-6. Cloudflare One (Zero Trust) — 1인·소규모 팀이 쓸 수 있는 것
**좌석·플랜** [웹][갭필 2026-10-03 — web.md의 [3자 주장]을 1차로 해소]
- https://www.cloudflare.com/sase/products/access/ (Cloudflare 공식 Access 제품 페이지, 페이지 날짜 표기 없음, 검색 시점 2026-10-03) 원문:
  > "Free Plan $0 forever Best for teams under 50 users or enterprise proof-of-concept tests."
  > "Pay-as-you-go $7 per user/month (paid annually) Best for teams over 50 users solving narrow SSE use cases and that do not require enterprise support services."
  > "Contract Plan Custom price per user/month (paid annually) Best for organizations building toward a full-featured SSE or SASE deployment…"
  > 사용량 행(Free / Pay-as-you-go / Contract 3열): "50 user limit" / "No user limit" / "No user limit"
  - ⚠ "$7"에는 **"(paid annually)"** 조건이 붙어 있다 — "월 $7"로만 쓰지 말고 "연간 결제 기준 사용자당 월 $7"로 쓸 것. 월 단위 결제 단가는 미확인.
  - ⚠ `www.cloudflare.com/plans/zero-trust-services/`는 클라이언트 렌더링으로 원문 추출 실패(web.md·갭필 모두) — 인용은 위 Access 제품 페이지로.
- 역사적 근거(원문 raw 확인): "On Tuesday, we announced a new free plan which provides many of the features of Cloudflare One, including DNS filtering, Zero Trust access, and a management dashboard - for up to 50 users at no cost." / "With our new Teams free plan, up to 50 seats of Access are available at no cost." — https://blog.cloudflare.com/zero-trust-week-setting-up-cloudflare-one-as-a-small-business/ (2020-10-15) [웹][갭필]. 2020년 이후 50석 구조 유지.
- Mesh 한정 문구(별개 제품): "50 nodes and 50 users free. Your whole team and your whole staging environment on one private network, included with every Cloudflare account." / "Get started Cloudflare Mesh: Head to Networking > Mesh in the Cloudflare dashboard. Free for up to 50 nodes and 50 users." (blog/mesh 2026-04-14). ⚠ Mesh 문구를 Access 좌석의 근거로 쓰지 말 것 — Access는 위 제품 페이지를 근거로.
- 좌석 소비 규칙(Seat management 2026-05-01): "Cloudflare One subscriptions consist of seats that active users in your account consume. Active users are added to Cloudflare One through any authentication event." / "A user who authenticates will hold their seat until you remove the user from your account. By default, inactive users will not be automatically removed". 서비스 토큰은 좌석 비소비 대안. 이 페이지에는 좌석 수·가격 문구가 없음을 갭필에서 재확인.

**명칭·구조 변경** — §0-2(Cloudflare One Client, Mesh node), §0-4(Tunnel 문서 분리), §0-9(proxy-dns 제거).

**Access 운영 한도·신기능** [웹] (Account limits 2026-09-04): 앱 500, 규칙당 이메일 1,000, IdP 50, 서비스 토큰 50, Gateway DNS/HTTP/Network 정책 각 500, 리스트 100(Standard 항목당 1,000). Require Access protection(2026-01-22): "When enabled, traffic to any hostname that does not have a matching Access application is automatically blocked." / "This deny-by-default approach prevents accidental exposure of internal resources to the public Internet." Managed OAuth(2026-03-20), Independent MFA(2026-04-15). Eager redirect cookie(2026-08-03 — 호스트명 5개 초과 다중 호스트 앱의 sign-in loop 대응, [커뮤니티 `[문서화]`]).

**신규 조직 기본값 변화** [웹]: 기본 로그인 = Cloudflare IdP(2026-06-18, 이전 OTP) — "When you create a new Zero Trust organization, Cloudflare automatically configures the Cloudflare identity provider as your default login method." / strict service token 인증 — 2026-10-05 이후 생성 조직은 기본 ON·끌 수 없음(§3-7).

**Tunnel 호스트명 라우팅(사설)** — "You can now route private traffic to Cloudflare Tunnel based on a hostname or domain, moving beyond the limitations of IP-based routing. This new capability is **free for all Cloudflare One customers**." (Changelog 2025-09-18). "Hostname routing is now generally available"(2026-08-11 — RSS 제목만 확인, changelog 본문 404). [웹]

**유료 경계** [웹]: "Remote browser isolation is available as an add-on to Zero Trust Pay-as-you-go and Enterprise plans." Zero Trust dedicated egress IPs: "Only available as an add-on to Zero Trust Enterprise plans." [갭필, §3-9]. CASB·Gateway Free 세부(로그 보존 등) [리서치 공백].

**현장 반응** [커뮤니티]: "between the broken dashboard side of Zero Trust and nightmare of Warp… it was basically impossible to setup."(TIPSIO, HN 2026-09-18) — Zero Trust UX 날것 불만은 이것 하나뿐. 관리자 화면 보호용 Access 권장 흐름(Show HN Minvoice 2026-07-15: "I recommend switching to Cloudflare Access").

### 3-7. 인증·보안
**Access JWT 검증 (오리진이 Spring/Node일 때)** [웹] (2026-05-06 기준, https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/validating-json/)
> "When Cloudflare sends a request to your origin, the request will include an application token as a `Cf-Access-Jwt-Assertion` request header."
> "We recommend validating the `Cf-Access-Jwt-Assertion` header instead of the `CF_Authorization` cookie, since the cookie is not guaranteed to be passed."
> "The public key for the signing key pair is located at `https://<your-team-name>.cloudflareaccess.com/cdn-cgi/access/certs`"
> "By default, Access rotates the signing key every 6 weeks. ... Previous keys remain valid for 7 days after rotation"
- 공식 예제 언어: Go·Python·JavaScript(Node.js). **Java/Kotlin(Spring Security) 공식 예제 없음** [리서치 공백] → 책은 JWKS 기반 Spring Security Resource Server(또는 JJWT) 예제를 **저자 작성 예제임을 명시**해 제시. 검증 항목 근거: RFC 7519(서명·`aud`·`exp`), 키 회전 6주·이전 키 7일 유효 → JWKS 캐시 갱신 설계.

**Workers에서 Access — `ctx.access`** [웹] (2026-08-18 기준, https://developers.cloudflare.com/workers/configuration/cloudflare-access/ , blog 2026-08-14)
> "the Worker can read the signed-in user's identity — including email, groups, device posture, and more identity fields — through `ctx.access`. No extra configuration or JWT parsing is required."
> "`ctx.access` is `undefined` if Access did not authenticate the request."
> "Cloudflare Access does not propagate `ctx.access` through Service Binding HTTP requests or remote procedure call (RPC) invocations."
> "Workers with Static Assets execute behind an internal router Worker. Access still protects the application and its assets. However, the router does not pass `ctx.access` to the user Worker."
> (Changelog 2026-08-14) "Make all Workers private by default, so every existing and newly created Worker requires sign-in before anyone can reach it."
- 구 방식(Changelog 2025-10-03): "To fully secure your application, it is important that you validate the JWT that Cloudflare Access adds to the `Cf-Access-Jwt-Assertion` header on the incoming request." (jose 패키지 예제)
- 로컬 테스트: `wrangler.jsonc`의 `"access": { "dev": { "aud": "my-app", "identity": {...} } }`

**서비스 토큰(머신 간)** [웹]
- 헤더 `CF-Access-Client-Id` / `CF-Access-Client-Secret`. 단일 헤더 대안 `Authorization: {"cf-access-client-id": "...", "cf-access-client-secret": "..."}` — "useful for authenticating SaaS services that only support sending one custom header"
- strict 모드(Changelog 2026-10-02): "If authentication or authorization fails, Access always returns `401` or `403` instead of redirecting the client to the login page with `302`." / "Only Service Auth policies can authorize the request." / "Zero Trust organizations created on or after October 5, 2026 have strict service token authentication turned on by default and cannot turn it off."
- 계정당 50개. rotation grace period·일시 비활성(2026-08-25), 비활성 토큰 자동 관리(2026-09-22), 스캔 가능한 시크릿 형식(2026-08-26).

**IdP 연동** [웹] (2026-06-19 기준): Cloudflare IdP 기본(신규 조직), "You can also send a one-time PIN (OTP) to approved email addresses. No configuration needed", "If they support OIDC or OAuth, select the generic OIDC", "Cloudflare One supports social identity providers that do not require administrator accounts, open source providers, and corporate providers." Terraform `cloudflare_zero_trust_access_identity_provider`. Auth0/Clerk 전용 가이드 미확인 → generic OIDC로 [추론]. 표준 기준: OIDC Core 1.0, OAuth 2.1 초안(§1-6).

**Turnstile** [웹] (Plans 2026-08-14, Spin GA 2026-08-10)
> "Turnstile setup has two parts: embed the widget in your frontend, then call siteverify from your backend. Without the second part, the widget appears on the page but does not protect the request."
> "The Turnstile dashboard flags existing widgets with no matching siteverify traffic."
- Free: "Up to 20 widgets", "Unlimited challenges", "10 hostnames per widget". 다른 Cloudflare 서비스 없이 독립 사용 가능.

**WAF·Rate Limiting(무료 범위)** [웹]: "Cloudflare Free Managed Ruleset: Available on all Cloudflare plans. Provides protection against high-impact and widely exploited vulnerabilities." Rate limiting rule Free 1개(10초 기간·10초 완화, 필드 Path·Verified Bot). Workers 바인딩: "The `ratelimit` binding is now stable and recommended for all production workloads." (2025-09-19)
- ⚠ `workers.dev` 뒷문 — §2-3 #9, §5 휴리스틱 3.
- "WAF는 패치를 대체하지 않는다" — §3-2 React/Next.js CVE.

**mTLS / API Shield** [웹]: "Each zone allows up to **100 active client certificates** by default." / "BYOCA certificates: Available on Enterprise accounts." / API Shield "Enterprise-only paid add-on" / "Anyone can set up Mutual TLS with a Cloudflare-managed certificate authority." / "New RFC 9440 mTLS certificate fields in Workers" (Changelog 2026-03-27). → API Shield는 개인 개발자 범위 밖.

**DDoS가 내 일인가** [논문] Jonker et al., "Millions of Targets Under Attack", IMC '17 [초록]: 2년간 활성 /24 네트워크의 약 3분의 1이 최소 1회 공격, .com/.net/.org 웹사이트 약 3%가 일평균 공격 연루. ⚠ 공격 건수 "약 2,100만 건"은 보도자료 수준 [요약] — 원문 확인 전 인용 금지. 2017년 데이터임을 밝힐 것.

**보안 관점의 반론** [커뮤니티]: Tunnel은 TLS 종단점 — jchw "it acts as a termination point for TLS, whereas Tailscale does not. … that's a pretty big privacy downgrade"; jorams "You've also in the process converted your entire security model to Cloudflare's idea of 'Zero Trust' which involves 100% trusting Cloudflare." (HN 45946865, 2025-11-16). 인증서 투명성 로그로 서브도메인·홈서버 노출(Fränkel 2026-01-11).

### 3-8. 캐싱
**세 가지 캐시 경로 — 어느 것을 쓸 것인가** [웹]

| 경로 | 핵심 성질 | 원문 |
|---|---|---|
| **Workers Cache** (신규, `"cache": {"enabled": true}`) | Worker 실행 없이 캐시 응답, 존 캐시 설정 미적용, RFC 9111 `Cache-Control` 준수, 기본 tiered, 요청 병합, `ctx.cache.purge({ tags: [...] })` | "Workers Cache lets Cloudflare return cached HTTP responses from your Worker without executing your Worker code." / "No zone configuration for caching applies to Workers Caching." / "Workers Caching is **tiered by default**." / "Cloudflare runs your Worker **once** and serves the resulting response to every waiting request." **⚠ 켜면 HIT·정적 자산까지 요청 과금** (2026-09-22) |
| **Cache API** (`caches.default`) | 데이터센터 로컬, tiered 불가, 요청 병합 없음 | "the Cache API does not collapse concurrent requests, so a burst of traffic to a fresh URL invokes your Worker once per request." / "the contents of the cache do not replicate outside of the originating data center." / "The `cache.put` method is not compatible with tiered caching." / "The `stale-while-revalidate` and `stale-if-error` directives are not supported when using the `cache.put` or `cache.match` methods." |
| **`fetch()`의 `cf` 옵션** (미들웨어형 Worker) | 오리진 응답을 존 캐시에 | "For requests where Workers are behaving as middleware (that is, Workers are sending a subrequest via `fetch`) it is recommended to use `fetch`." 옵션 `cacheEverything`, `cacheKey`, `cacheTags`, `cacheTtl`, `cacheTtlByStatus`(예: `{ "200-299": 86400 }`), 2026-06-28부터 `cf.vary` |

- Smart Placement와의 관계: "The cache is always consulted before Smart Placement is considered."
- "Since Cloudflare Workers runs before the Cloudflare cache, the caching of a request still incurs costs." (Workers Pricing Fine Print)

**존 캐시** [웹]: Cache Rules Free 10개. Tiered Cache·Smart Topology Free 포함(Generic Global·Regional·Custom은 Enterprise). "Cloud region hints are available on all plan types (Free, Pro, Business, and Enterprise) at no additional cost." Cache Response Rules(2026-03-24): "Cache Response Rules let you modify `Cache-Control` directives, manage cache tags, and strip headers like `Set-Cookie` from origin responses *before* they reach Cloudflare's cache." Vary 지원(2026-07-02), Smart Tiered Cache for public cloud(2026-04-17). Cache Reserve 유료(§2-2). Pingora가 캐시 구동(Changelog 2026-05-04).

**갱신·무효화·퍼지** [웹]
- "Cloudflare's `stale-while-revalidate` support is now fully asynchronous." / "This change is live for all Free, Pro, and Business zones." (2026-02-26)
- invalidate(2026-09-28): "Invalidation marks matching content as stale. On the next request, Cloudflare revalidates the content with your origin. If your origin responds with `304 Not Modified`, Cloudflare reuses the cached content" — `POST /zones/$ZONE_ID/invalidate_cache`
- 퍼지: Free도 URL·Hostname·Tag·Prefix·Purge Everything 모두 가능. Free 요청 한도 "5 requests per minute"(호스트명·태그·프리픽스·전체), 단일 URL 800 URLs/초.

**커뮤니티 현장** [커뮤니티]
- "CDN edge caching served stale HTML after a deploy, and the service worker cached the bad response. Took a CDN purge from the dashboard to fix. The debugging experience when things go wrong at the edge is painful, you're always guessing which cache layer is the problem." (HN Manchitsanan, 2026-04-07, https://news.ycombinator.com/item?id=47675953)
- HTML은 기본 `cf-cache-status: DYNAMIC`. Page Rules deprecated → Cache Rules("Cache Everything" ↔ "Eligible for cache") — 개인 블로그 가이드(eastondev 2025-12-01, classmethod) 근거, 일정(2024-07 신규 Free 계정 차단, 2025 자동 이관)은 **문서 대조 필요**(§7 C-21).

**학술 근거 연결**: one-hit-wonder 74%(Maggs & Sitaraman) → 캐시 키를 쿼리스트링 등으로 쪼갤수록 HIT율이 떨어진다, Tiered Cache·Cache Reserve가 필요한 이유. RFC 9213 `CDN-Cache-Control`로 "브라우저엔 짧게, 엣지엔 길게", RFC 5861 `stale-if-error`로 오리진 장애 버티기 — 단 Cloudflare 지원 범위는 위 1차 문서로 대조.

### 3-9. Cloudflare 밖 서비스와의 통합 전략
**Hyperdrive — 외부 Postgres/MySQL** [웹]
> "Hyperdrive supports any Postgres or MySQL database, including those hosted on AWS, Google Cloud, Azure, Neon and PlanetScale. Hyperdrive also supports Postgres-compatible databases like CockroachDB and Timescale."
> (Neon) "you should use a driver like node-postgres (pg) or Postgres.js to connect directly to the underlying database instead of the Neon serverless driver."
> (MySQL GA 2026-08-07) "You can connect using your existing drivers, ORMs, and query builders ... MySQL support is available at the same pricing as Postgres." — `mysql2`는 `disableEval: true` 필수
> (PlanetScale 2026-06-18) "PlanetScale usage appears on your Cloudflare invoice each billing period as a dollar total at PlanetScale's standard pricing."
> (사설 DB 2026-04-29) "You can now connect Hyperdrive to a private database through a Workers VPC service. This is the recommended way to connect Hyperdrive to a private database that is not exposed to the public Internet."
- 한도: 쿼리 최대 60초, 캐시 응답 50 MB, 원본 연결 Free ~20 / Paid ~100. STABLE 함수 비캐시(2026-02-23), 로컬 dev 원격 DB(2025-12-04).
- 커뮤니티 `[문서화]`: Neon serverless 드라이버는 WebSocket이라 Hyperdrive 풀 우회 → TCP 드라이버. **Supabase는 풀러 주소 대신 direct 연결 문자열로 이중 풀링 회피** (https://neon.com/blog/hyperdrive-neon-faq , https://neon.com/docs/guides/cloudflare-hyperdrive — Supabase 쪽 근거는 Neon/Supabase 문서·FAQ 경유, Cloudflare 1차 Supabase 페이지 미확인). OpenNext #1214 번들링 이슈(§3-2). 실사용 흔적: "Neon Postgres via Prisma + Hyperdrive"(HN 47146087), Vithos 템플릿(HN 48435284) — 깊은 후기 적음.

**R2 — S3 호환 API를 기존 AWS SDK로** [웹]
> "When using the S3 API, the region for an R2 bucket is `auto`. For compatibility with tools that do not allow you to specify a region, an empty value and `us-east-1` will alias to the `auto` region."
> (Java v2, 2026-04-21) "You must set `chunkedEncodingEnabled(false)` in the `S3Configuration` when building your client. The AWS SDK for Java v2 uses chunked transfer encoding by default for `putObject` requests, which causes a signature mismatch error (HTTP 403) with R2"
- 엔드포인트 `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`, `.pathStyleAccessEnabled(true)`, `.region(Region.of("auto"))`
- 비용 팁: "Use presigned URLs for direct client access instead of proxying through Workers" (Optimize costs 2026-05-04)
- 2026: Sippy가 Azure Blob·S3 호환 지원(2026-07-24), `us` jurisdiction(2026-08-17), Local Uploads 오픈 베타(2026-02-03)
- ⚠ "R2는 egress가 무료이지 읽기가 무료인 게 아니다" — rezonant(HN 2024-02-11, 오래됨) "(remember, R2 does charge per read/write though)"; WordPress 포럼(요약 경유, 날짜 미상) AI 크롤러로 인한 사진 사이트 비용 우려 [커뮤니티]. Free 초과분 과금(§2-4).

**Queues HTTP pull / Service bindings** [웹] — §3-3. Service bindings: "Service bindings provide the separation of concerns that microservice or service-oriented architectures provide, without configuration pain, performance overhead or need to learn RPC protocols." 추가 요청 요금 없음.

**외부 API 호출과 출구(egress) IP — IP 화이트리스트를 요구하는 PG·사내 API** [웹][갭필 2026-10-03로 부분 해소]
- 계정 전용 고정 출구 IP는 **Enterprise 제품**이다:
  - Smart Shield (Dedicated CDN Egress IPs), dateModified 2026-04-16, https://developers.cloudflare.com/smart-shield/configuration/dedicated-egress-ips/ : "Enterprise customers can leverage dedicated egress IPs for layer 7 WAF and CDN services, as well as Spectrum. The egress IPs are reserved exclusively for your account so that you can increase your origin security by only allowing traffic from a small list of IP addresses." Protect your origin(2026-10-02)은 Smart Shield Advanced 전용 egress IP를 "Availability: Enterprise-only"로 표기.
  - Workers와의 관계, dateModified 2026-05-07, https://developers.cloudflare.com/smart-shield/configuration/dedicated-egress-ips/other-products/ : "`fetch()` requests that access services on your origin will use Dedicated CDN Egress IP addresses." / "Workers subrequests — requests from one Worker to another — are expected to use different IPs." / "For `connect()` requests - which create outbound TCP connections from Workers - Dedicated CDN Egress IPs are **not** used." / "If you are interested in any of these solutions, contact your account team."
  - Zero Trust(Gateway) dedicated egress IPs, dateModified 2026-09-04, https://developers.cloudflare.com/cloudflare-one/traffic-policies/egress-policies/dedicated-egress-ips/ : "Only available as an add-on to Zero Trust Enterprise plans." 그 외 트래픽은 "default shared IPs".
- 비Enterprise에서 문서화된 우회책:
  - **Tunnel 호스트명 라우팅**: "Precise Egress Control: Route traffic for public hostnames (e.g., `bank.example.com`) through a specific Tunnel to enforce a dedicated source IP, solving the IP allowlist problem for third-party services." (Changelog 2025-09-18, Cloudflare One 전 고객 무료) — 고정 IP를 가진 자기 서버(`cloudflared` 설치 지점)에서 나가게 하는 방식.
  - **Gateway egress for Workers**(Changelog 2026-06-05): "Workers using a VPC Network binding with `network_id: "cf1:network"` now egress to public Internet destinations through Cloudflare Gateway." — 단 Gateway의 전용 IP는 Enterprise 애드온이므로, 비Enterprise에서는 기본 공유 IP로 나간다 [추론: 위 두 1차 문장의 조합].
- 잔여 [리서치 공백]: "Workers 기본 `fetch()`의 출구 IP는 고정되지 않는다/공유 IP다"를 **직접** 명시한 1차 문장은 확보하지 못했다. 책 권장 표현: "계정 전용 고정 출구 IP는 Cloudflare에서 Enterprise 제품(Smart Shield·Zero Trust 애드온)이다. 그 밖의 플랜에서 IP 화이트리스트가 필요하면, 고정 IP를 가진 자기 서버를 Tunnel로 연결해 그 서버를 거쳐 나가게 한다."

**Email(외부 메일 대체)** — §3-5.

**Stripe·웹훅** [커뮤니티 `[문서화 위주]`]: 원본 body를 `.text()`로 받아 `constructEventAsync`(SubtleCrypto 기반 비동기)로 검증 — 프레임워크가 JSON을 먼저 파싱하면 서명 검증이 깨진다. Hono 공식 예제 https://hono.dev/examples/stripe-webhook , Stripe 문서 https://docs.stripe.com/webhooks/signature.md . ⚠ 서드파티 `@worker-tools/stripe-webhook`의 constructEvent가 헤더를 검증하지 않는 취약점 공지(https://advisories.gitlab.com/pkg/npm/@worker-tools/stripe-webhook). 로컬 수신 테스트: Protected Quick Tunnel("Protected Quick Tunnels let you share a local development server, webhook receiver, or demo", Changelog 2026-10-02). Cloudflare 1차 Stripe 전용 가이드 [리서치 공백].

**IaC·CI/CD** [웹]
- Terraform provider **v5.27.0** (2026-10-03). 2025-10-09부터 정적 자산 포함 풀스택 Worker·Workflows를 Terraform으로 배포 가능.
- Pulumi: "Use TypeScript, JavaScript, Python, Go, .Net, Java, or YAML to write Pulumi programs." → Java 개발자는 Pulumi Java SDK로 IaC 가능.
- GitHub Actions: `uses: cloudflare/wrangler-action@v4`(문서 예시), 최신 v4.1.3(2026-09-24), 토큰 템플릿 "Edit Cloudflare Workers".
- Workers Builds: GitHub·GitLab·Artifacts 연결, 기본 Node.js 24.18.0(2026-07-30), Deploy Hooks(2026-04-01), 대체된 대기 빌드 건너뛰기(2026-07-24), PR별 Worker Previews(2026-09-22).

**하이브리드 운영 관점** [커뮤니티]: 깊은 AWS+Cloudflare 운영기는 없음(red-iron-pine "I want diversity of providers" 수준). 단일 벤더 리스크(§4 논쟁 A, §6 패턴 2)가 통합 전략 장의 오프닝 소재.

### 3-10. Cloudflare Tunnel (`cloudflared`)
**개요·무료·HA** [웹] (Tunnel 2026-09-11, https://developers.cloudflare.com/tunnel/)
> "Available on all plans"
> "Instead of exposing a public IP, you install a lightweight daemon called `cloudflared` on your server."
> "Each tunnel maintains four long-lived connections to two Cloudflare data centers for built-in redundancy."
> "A replica is an additional `cloudflared` instance that points to the same tunnel. Each replica creates four new connections ... You can run up to 25 replicas (100 connections) per tunnel. Traffic routes to the geographically closest replica."
> "This documentation covers Cloudflare Tunnel use cases for public applications. For VPN replacement, private network access, and network traffic filtering, refer to the Cloudflare One Tunnel documentation."

**원격 관리(권장) vs 로컬 관리** [웹] (2026-09-11 / get-started 2026-09-30)
> "Cloudflare recommends creating a remotely-managed tunnel for most use cases. Remotely-managed tunnels store their configuration on Cloudflare, which allows you to manage the tunnel from any machine using the dashboard, API, or Terraform."
> "Locally-managed tunnels are intended for specific scenarios such as local development, testing, or legacy configurations."
> "A remotely-managed tunnel only requires a token to run. Anyone with the token can run the tunnel."
- 원격: 대시보드 **Networking > Tunnels > Create Tunnel**, 또는 API `POST /accounts/$ACCOUNT_ID/cfd_tunnel` + `"config_src": "cloudflare"`, 라우트 "Published application"
- 로컬: `cloudflared tunnel login` → `cloudflared tunnel create <NAME>` → `~/.cloudflared/config.yml`(`credentials-file: /root/.cloudflared/<Tunnel-UUID>.json`, ingress) → `cloudflared tunnel route dns <UUID or NAME> <hostname>` → `cloudflared tunnel run <UUID or NAME>`

**운영** [웹]
- Linux 서비스: `sudo cloudflared service install` → `systemctl start cloudflared`; 원격 관리는 `ExecStart=/usr/local/bin/cloudflared tunnel ... run --token <TOKEN VALUE>`
- 토큰: `--token` ↔ `TUNNEL_TOKEN`, `--token-file <PATH>` ↔ `TUNNEL_TOKEN_FILE`
- Docker `cloudflare/cloudflared`. Kubernetes 예시 `replicas: 2`, `cloudflared tunnel --no-autoupdate --loglevel info --metrics 0.0.0.0:2000 run`
> "We do not recommend using `cloudflared` in autoscaling setups because downscaling (removing replicas) will break existing user connections to that replica. Additionally, `cloudflared` does not load balance across replicas; replicas are strictly for high availability."
> "Instances of `cloudflared` do not automatically update on Windows."
> "Cloudflare supports versions of `cloudflared` that are within one year of the most recent release."
- 문서 간 미묘한 차이: "Traffic routes to the geographically closest replica" ↔ "does not load balance across replicas" — 양립. 책 표현: **"replica는 HA용이지 LB용이 아니다."**
- 연결 사전 점검(2026-05-27): "Starting with `cloudflared` version 2026.5.2, Cloudflare Tunnel automates the entire connectivity pre-checks workflow directly inside the binary." / "Transport connectivity — outbound `UDP (QUIC)` and `TCP (HTTP/2)` on port `7844`." / "If DNS is unresolvable, or **both** UDP and TCP fail on port 7844, `cloudflared` exits early with the failure" → 사내 방화벽 7844 아웃바운드 허용. QUIC 타임아웃 이슈(#1158, #1379)는 UDP 7844 차단 시 HTTP/2 폴백·업그레이드로 해결되는 경우가 많음 [커뮤니티 `[문서화]`].
- 폐기·변경: `proxy-dns` 제거(2026-02-02~), 2027년 32-bit Windows·Intel macOS 빌드 중단(공지 2026-09-18), 최신 2026.9.3(2026-09-24).

**Quick Tunnels + 보호 모드** [웹] (2026-09-30, Changelog·blog 2026-10-02)
> "Quick Tunnels create a temporary `trycloudflare.com` URL for a local service. You do not need a Cloudflare account or domain."
> "Quick Tunnels are for testing and development. For production, create a Cloudflare Tunnel."
> "Each Quick Tunnel supports up to 200 in-flight requests. Additional requests return a `429` response." / "Quick Tunnels do not support Server-Sent Events (SSE)."
> "Use the new `--allowed-mail` flag in `cloudflared` to require visitors to authenticate with a one-time PIN sent to their email" — 예: `cloudflared tunnel --url http://localhost:8080 --allowed-mail '*@example.com'`
- HN "Cloudflare Quick Tunnels"(2026-09-18, 844점·316댓글): Quick Tunnels는 5년 넘은 기능이라는 지적(noname120, web.archive 2021 근거) → ⚠ **Quick Tunnels 자체를 "신기능"으로 쓰지 말 것. 신기능은 2026-10-02 Protected Quick Tunnels(`--allowed-mail`).** ngrok 창업자 `[이해관계자]`의 익명 터널 비판(§4 논쟁 C).

**Wrangler·Vite 통합** [웹] (2026-03-19, 2026-05-18): "`wrangler tunnel quick-start` — Start a free, temporary tunnel without an account using Quick Tunnels." / "Wrangler handles downloading and managing the cloudflared binary automatically." / "To start a tunnel, press `t` in Wrangler or `t + Enter` in Vite while your dev server is running." 명령: create/list/info/delete/run/quick-start.

**SSH·Access 연계** [커뮤니티]: `ssh itake@ssh.domain.me -o ProxyCommand="cloudflared access ssh --hostname %h"`(itake, HN 2026-04-13); "Put Cloudflare Access in front of the tunnel, now you have a proper auth via Google or Github."(brownindian, HN 2026-03-08).

**걸림돌** [커뮤니티]
- ToS·대용량 미디어: "officially you're not allowed to use them for streaming video, meaning I can't put it in front of my Jellyfin without breaking TOS."(tombert), "Free Cloudflare account cannot be used to serve my Plex server."(yegle) ↔ 1차 FAQ 문구(§2-5 #8). Lemmy 등의 "개인 단속 사례 거의 없음·조항이 바뀌었다" 주장은 `[일화, 공식 ToS 대조 필요]` — 책은 1차 FAQ 문구만 인용.
- 업로드 100MB: sylens(Immich) "Only issue is the 100MB upload size for videos." ↔ 1차: Free 존 request body 최대 100 MB(초과 413) — 일치.
- gRPC: cloudflared #491 "grpc support"(2021-10 개설, 2026-09-30까지 open, 66댓글). 우회(lmtr0, 2026-09-30): `--protocol http2 --http2-origin --no-tls-verify` + HTTPS 앱·HTTP2·Chunked Encoding 비활성화. ShadiestGoat(2026-09-06): "DO NOT enable 'Match SNI To Host' option. This will cause the trailing issue". Spring gRPC 독자에 직결. Workers/Containers 인바운드 gRPC(private beta)는 다른 경로.
- 구성 비판: amluto — CNAME `{uuid}.cfargotunnel.com` 라우팅 "It boggles my mind that Cloudflare ever considered this acceptable for production"

### 3-11. 도구 체인·관측성
**Wrangler v4** [웹]: "Cloudflare recommends using `wrangler.jsonc` for new projects, and some newer Wrangler features will only be available to projects using a JSON config file." / "Wrangler is installed locally into each of your projects." / "We support running the Wrangler CLI with the Current, Active, and Maintenance versions of Node.js." 2026 신규: 인증 프로필(2026-07-02), OS 키체인 저장(2026-06-03), 디바이스 플로 로그인(2026-08-04), `secrets` 필수 선언(2026-03-25), `wrangler types --check`(2026-01-12), KV·R2·D1 자동 프로비저닝(2025-10-24). Remote bindings GA(2025-09-16): "add `"remote" : true` to each binding that you want to rely on a remote resource running on Cloudflare". Local Explorer(2026-04-13). 최소 버전: 정적 자산 10만 파일 4.34.0+, 자동 구성 4.68.0+, Worker Previews 4.135.0+.

**`cf` CLI (베타, 2026-09-28)** [웹] https://developers.cloudflare.com/cf/ , 한국어판 https://blog.cloudflare.com/ko-kr/cloudflare-cf-cli-launch/
> "Wrangler is the CLI for Workers projects configured with `wrangler.jsonc` or `wrangler.toml`. `cf` covers the public Cloudflare API and uses `cloudflare.config.ts` for Workers projects."
> "Before you run `cf dev`, `cf build`, or `cf deploy` in a Wrangler project, convert it with `cf migrate`."
> "Wrangler only provides commands for around 280 operations, and Cloudflare offers thousands."
> "In March 2026, agents were responsible for a quarter of Wrangler use ... Last week, agent usage reached 48%."
- Changelog 표현: Cloudflare API 전체 2,900+ 명령 + Workers 개발·배포. [편집 판단] Wrangler 본문, `cf` 전망 박스(§0-14).
- 커뮤니티 불안: "it feels like Wrangler 5 will introduce yet another interaction model."(aperture147, 2025-10-15)

**테스트** [웹]: "Version 1 of the Workers Vitest integration is published as `@cloudflare/vitest-plugin`. The package was formerly named `@cloudflare/vitest-pool-workers`." / "To migrate automatically, run: `npx @cloudflare/codemods vitest:pool-workers-to-vitest-plugin`" / "For outbound request mocks in Workers tests, use the `@msw/cloudflare` integration." Miniflare v5(2026-09-08, `cf` CLI 대비 구성 형식 변경, breaking): "Most projects should use those tools instead of depending on Miniflare directly, and Miniflare v5 will not require any action." ⚠ GitHub상 Miniflare 5.x는 alpha 프리릴리스(예: `miniflare@5.20261001.0-alpha`, 2026-10-01) — 직접 의존 금지.

**Worker Previews** [웹] (blog 2026-09-22, Yomna Shousha 외): "Each Git branch gets a production-like place to run, with its own code, configuration, URL, observability, and state." / "Deploy an isolated Preview with npx wrangler preview" (Wrangler 4.135.0+) / "For Durable Objects and Containers, Cloudflare automatically provisions separate namespaces, storage, apps, and instances for every Preview." ⚠ 비용 연결: $34,895 사례는 60개 이상의 preview 배포가 각자 DO 인스턴스를 만든 것이 원인의 일부(§2-5) → "프리뷰 환경에서 DO 바인딩을 뺀다"(휴리스틱 2).

**관측성** [웹]: `"observability": { "enabled": true }`. "Workers tracing follows OpenTelemetry (OTel) standards" / "You can also set `persist: false` to export traces to your destination without persisting them in the Cloudflare dashboard." / `head_sampling_rate` 기본 1. "We're launching Cloudflare Traces in open beta, giving you a request-level view of supported security rules, transformations, cache decisions, routing, Workers, and origin handling." (blog 2026-10-02). 커스텀 스팬 `startActiveSpan()`(2026-07-28), RPC 세션 스팬 자동(2026-09-17), 로컬 트레이싱(2026-08-04), 메모리 메트릭(2026-06-30), Custom Dashboards에 로그·트레이스(2026-10-02). 가격 전환 2026-12-01(§2-1, 🕒 §9). Logpush 전 플랜(2026-09-30). Analytics 전 플랜 최소 30일 보존(2026-10-02).

---

## 4. 논쟁점·상충 관점 (합치지 말고 병기)

### 논쟁 A: 중앙집중은 인터넷을 더 약하게 만드는가 [커뮤니티]
- 관점 A(약하게 만든다): mixedbit "Homogeneous systems like Cloudflare will continue to cause global outages. Rust won't help, people will always make mistakes, also in Rust."(HN 2025-12-05) / stroebs "I can't advocate for using them in my professional job since we actually require distributed infrastructure that won't fail globally in random ways we can't control." / krick "As if anybody could viably stop using them."
- 관점 B(더 견고하다, 눈에 띌 뿐): miki123211 "Centralized services don't decrease redundancy. They're usually far more redundant than whatever homegrown solution you can come up with. The difference between centralized and homegrown is mostly psychological."(HN 2025-11-24) / vasco "smaller providers usually have much more ongoing issues, that just happen to be 'chronic' vs 'acute' pains."
- 출처 스레드: "The Cloudflare outage might be a good thing"(2025-11-24, 276점) https://news.ycombinator.com/item?id=46029908
- 사실 배경(§6 패턴 2): 2025-11-18(Bot Management feature file), 2025-12-05(WAF 규칙 전역 설정), 2026-02-20(BYOIP API 버그), 2026-08-08 R2 장애.

### 논쟁 B: D1의 10GB는 결함인가 설계 철학인가
- 관점 A(결함): keeda "The 10GB limit per DB is unsuitable for even trivial use-cases."(HN 2026-04-08) / fastball "global performance was pretty terrible"(HN 2025-04) [커뮤니티]
- 관점 B(설계): kentonv `[이해관계자: Workers 리드]` "split data into many small databases … you can create an unlimited number of them."(HN 2026-04-08) / [웹] "D1 is designed for horizontal scale out across multiple, smaller (10 GB) databases"
- 학술 배경: SQLite의 임베디드 단일 파일 성격(Gaffney et al. 2022).

### 논쟁 C: Cloudflare Tunnel 대 Tailscale(그리고 ngrok)
- 관점 A(Tunnel): 포트를 열지 않고 TLS·도메인·인증(Access)까지 한 번에. AnonyMD "It's a magical invention that lets us host websites while keeping our server firewalls closed!"(HN 2026-04-08)
- 관점 B(Tailscale): TLS 종단·MITM 우려, P2P 부재, 벤더 종속 — jchw·jorams·siwatanejo(HN 45946865), Fränkel "Migrating to Tailscale was a leap of faith, but I'm very happy I did it."(2026-01-11)
- 관점 C(익명 터널 자체 비판): inconshreveable `[이해관계자: ngrok 창업자]` "we removed anonymous usage of our product many years ago because it was far and away the largest source of abuse … anonymous, account-less tunneling services like this are net negative for the security of the internet"(HN 2026-09-18). whizzter "Don't all these free proxy services always fall prey to blacklists…"
- 경쟁 홍보 주의: ghoshbishakh `[이해관계자: Pinggy 공동창업자]`, Pangolin(오픈소스 대안, Show HN 2025-07-10, 500점).
- 현장 합의(휴리스틱 7): 공개 노출은 Tunnel+Access, 사설 접근(SSH·동기화·미디어)은 Tailscale.

### 논쟁 D: Containers는 쓸 만한가 — §3-4 커뮤니티 항목(긍정 rozenmd·meerab·NicoJuicy / 부정 detuks·youngbum·Wire). 공식 입장은 "1-3 second range" 콜드 스타트, 내장 오토스케일링 없음.

### 논쟁 E: vinext — Next.js 문제의 해답인가 위험한 AI 생성물인가
- 기대: hungryhobbit(HN 47143933), 성능·Vite 기반.
- 경계: thawab(RSC RCE 전례), slopinthebag(엣지 케이스), tills13("The messaging is ignorant"), Vercel 측 취약점 공개 `[이해관계자]`.
- Cloudflare 측: 1.0에서 테스트 호환성 "more than 99%, excluding cache components", Next.js e2e 테스트 nightly 실행, 2026-05 CVE에 "Vinext's latest release is not vulnerable".
- 메타 비판: acedTrex "God cloudflare's blog quality has fallen off a cliff … just llm slop"(HN 47143848), Quick Tunnels 랜딩 "vibe-coded" 비판(rplnt, skhameneh). 한국 GeekNews 소개(2026-02-25, 댓글 4개) — 국문 논쟁 미확보.

### 논쟁 F: 무료 티어는 선의인가 미끼인가
- 관점 A(전략적 선의): simonw(DNS 온보딩 퍼널), Shakahs("most of the bandwidth is from peering, so it essentially costs them nothing"), 공식 "Cloudflare's commitment to free" https://blog.cloudflare.com/cloudflares-commitment-to-free/ , nichochar "Generous free tiers, pricing scales very competitively"
- 관점 B(미끼·리스크): neya "One day, you get a call from their sales team saying 'you're straining our network'. … we were asked to upgrade to a $2000+ per month plan. From a $200/mo plan."(HN 2025-01-15, 607점), i_have_an_idea, sjoedev("enshittification"), kugelblitz "I don't like free offerings, because what if they decide to charge someday?"(HN 2026-04-07)
- ⚠ "$120k 엔터프라이즈 선결제" 사례(robindev, 2024-05-26)는 **온라인 카지노가 지역별 미러 도메인을 돌리던 맥락** — 일반 개발자 사례로 일반화하지 말 것(candiddevmike 지적). 원문 표현 "It felt like extortion."
- 추정 원인: "unmetered"는 대역폭 과금이 없다는 뜻이지 트래픽 유형(대용량 비HTML·비디오)·규모와 무관한 영구 무료 보장이 아님. 대상 독자에게 닥칠 확률은 낮지만 불안은 큼.

### 논쟁 G: 지출 보호 — 알림이면 충분한가, 하드캡이 필요한가
- 관점 A(현행 장치로 충분): Budget alerts 기본 $10·Billable Usage API·`limits.*`·AI Gateway spend limits로 겹겹 방어 [웹]
- 관점 B(하드캡 필요): simonw "I want to set a cap of $100/month and know, for sure, that if something untoward happens my apps will all stop serving traffic", woodylondon "once you're on the paid plan, you're exposed to unlimited risk", jacobmei "per-binding spend caps would have caught this", mathoff "Close, but still not hard cost cap" [커뮤니티]. 경쟁사 비교: woodylondon "I am using Supabase at the moment, and see they have a hard cap now. and so does Vercel …"(이용자 주장, 타사 기능은 미검증).

---

## 5. 실무 적용 팁 (현장 노하우 + 문서 근거)

### 휴리스틱 (커뮤니티 출처 → 문서 근거)
1. **공개 API·실험은 Free 계정에, 유료 계정에는 차단기를 직접 만든다.** "The safest way to use Workers is on the free tier, which will shut off after 100,000 requests/day" (simonw). 구현: Little Bear Apps 3단 서킷 브레이커(70/90/100%, KV TTL 1시간 자동 해제, 탐지 ~30초). "Prevention over detection"(photobombastic, HN 47323303), "Per-service p95-vs-median alerts at hourly granularity would have flagged this inside 6 hours"(matrixgard, HN 47823007). 문서 근거: §2-3.
2. **DO alarm은 "이미 있는지" 확인하고 건다, 프리뷰에서는 DO 바인딩을 뺀다.** "Strip DO bindings from preview environments entirely - Deploy a budget monitor kill switch Worker - Add a circuit breaker that checks alarm state before scheduling"(thewillmoss). 코드: `const existing = await this.ctx.storage.getAlarm(); if (!existing) await this.ctx.storage.setAlarm(Date.now() + 60_000)`. 대안(jacobmei): 쓰기를 인바운드 요청에서만, edge cache `max-age=3600`을 자연 스로틀로 → KV 쓰기 "keys × 24/일", "No alarms means no self-triggering loop is even possible."
3. **커스텀 도메인을 붙였으면 `workers.dev`를 끈다** — WAF 우회 뒷문. "the bot was bypassing the route on the domain and using the worker.dev domain"(white_viel, HN 2026-02-25) / kentonv: `"workers_dev": false` 또는 workers.dev에 Access, "But of course you have to remember to do those things..."
4. **KV는 느리게 바뀌는 설정용, 카운터·락은 Durable Objects로.** "A single busy API key gets hit from many edge locations near-simultaneously, which is exactly the scenario that makes the propagation delay...worse."(Kuryzhev). 레이트 리밋은 Workers `ratelimit` 바인딩(GA)도 선택지. 극히 작은 전역 설정·플래그는 KV Instant(private beta, §3-3)가 새 선택지.
5. **"큰 DB 하나"가 필요하면 Hyperdrive + 외부 Postgres, 아니면 테넌트별 작은 SQLite 여러 개**(kentonv). Neon은 TCP 드라이버, Supabase는 direct 연결 문자열.
6. **Stripe 웹훅은 원본 body `.text()` + `constructEventAsync`.** §3-9.
7. **공개 노출은 Tunnel + Access, 사설 접근은 Tailscale.** §3-10, 논쟁 C.
8. **Containers는 "가끔, 몰아서" 쓰는 작업용.** "Rare, bursty workloads that fit around regular use of Workers."(rozenmd). 상시 실시간 서버는 작은 VM이 더 안정적이었다는 반대 정황(youngbum).
9. **배포 후 이상하면 캐시 층부터 의심** (HTML·서비스워커·CDN). Manchitsanan 일화, mhitza "Every time I purge the pull zone cache, I do it twice". 문서 도구: invalidate API, 퍼지 한도(Free 5회/분).
10. **R2는 egress가 무료이지 읽기가 무료가 아니다** + Free 초과분은 과금(§2-4). presigned URL로 Worker 경유 비용 절감.

### 무료 티어 극대화 체크리스트 [편집 판단, 근거는 §2]
- 정적 자산은 무료·무제한 → SPA는 `not_found_handling: single-page-application`으로 Worker 호출을 피한다. Workers Cache는 켜지 않는다(켜면 과금).
- Free에 머무르면 대부분 "청구 대신 에러"(Workers 1027, KV·Hyperdrive·Workers AI 에러, D1 실패, Images 9422, Observability 수집 중단). **R2는 예외(과금).**
- Queues가 Free 포함(일 10,000 ops), Cron 5개, Hyperdrive 쿼리 10만/일, Turnstile 무제한, Tunnel 무료, Access 50명까지 $0.
- Free에서 불가: Containers, Email Sending(자기 주소 외), 일부 대형 Workers AI 모델, Cache Reserve, Workers Trace Events Logpush.
- 비용 대비 가용성 트레이드오프를 독자에게 명시(Error 1101 화면 노출 사례).

### 유료 전환 시 안전장치 체크리스트 [편집 판단, 근거는 §2-3·§2-5]
1. `limits.cpu_ms`·`limits.subrequests`를 Worker마다 보수적으로 설정
2. Budget alert 임계치를 기본 $10에서 자기 예산에 맞게 추가 설정(알림 전용·하루 지연임을 이해)
3. Billable Usage API 폴링 Cron Worker로 자체 킬 스위치(하루 지연 감안) + 기능별 자체 카운터(커뮤니티 서킷 브레이커)
4. WAF Rate limiting rule·`ratelimit` 바인딩을 Worker 앞에, `workers.dev` 끄기
5. DO: Hibernation, alarm 중복 등록 방지, 프리뷰 환경에서 DO 바인딩 제거
6. D1: 인덱스 점검(풀 스캔 = rows read), `ON CONFLICT`
7. AI 호출은 AI Gateway spend limits 경유
8. 실험·공개 API는 별도 Free 계정으로 분리(휴리스틱 1)
9. 청구 분쟁 대비: Little Bear Apps는 18일 만에 $4,586.64 면제됐으나 그 사이 자동 정지를 겪음 — "면제를 기대하지 말고 사전 차단"으로 서술

---

## 6. 대표 사례 — 커뮤니티 고통 순위와 챕터 오프닝 매핑

> 순위는 community.md "근거 강도별 패턴 순위" 그대로. 챕터명은 계획 전이라 주제명으로 제안한다 [편집 판단].

| 순위 | 고통 패턴 | 근거 강도 | 대표 출처 | 오프닝 후보 챕터 | 오프닝 소재(한 줄) |
|---|---|---|---|---|---|
| 1 | 하드 지출 상한 부재와 요금 폭탄(DO·D1·Workers) | 매우 강함 — 2022~2026-09 지속, 최대 $34,895 | HN 47787042, littlebearapps, HN 48611258, 49158930 | 과금 보호·안전한 유료 사용 장 / 무료 티어 극대화 장 / DO 장 | "아침에 일어나 보니 $34,895 청구서가 와 있었다"(결말 미확인 명시) 또는 "$5 계정에 $4,868"(18일 뒤 $4,586.64 면제) |
| 2 | 잇단 장애와 단일 벤더 리스크 | 매우 강함 — 1465·782·190점 스레드, GeekNews | HN 45973709(2025-11-18, 1465점·916댓글), 46162656, 47103649, GN 24471 | 외부 서비스 통합 전략 장 / 운영·관측성 장 | "28M 500 errors/sec for several hours from a single provider."(binarymax) / GeekNews "Cloudflare가 안되어서 온갖 서비스가 중단되니 지옥이더군요.." |
| 3 | Pages→Workers 혼란과 Next.js 어댑터 버전 지연(vinext 포함) | 강함 | OpenNext #972/#1049/#1157/#653/#1214, r/nextjs | 첫 배포(정적 사이트) 장 / Next.js 장 | r/CloudFlare "Help me understand Workers vs Pages in Cloudflare (I'm confused!)" / "Downgrading to 16.0.10 fixed it immediately." |
| 4 | D1/KV/DO 선택(10GB, 최종 일관성, 트랜잭션) | 강함 | HN 43572511, 47696317, Dev.to KV | 데이터 저장소 선택 장 | 레이트 리미터가 "zero errors"로 조용히 실패한 KV 사례 |
| 5 | Tunnel의 ToS·TLS 종단·Zero Trust UX, Tailscale 비교 | 강함 — 844점·311점 | HN 49754785, 45946865, cloudflared #491 | Tunnel 장 / Cloudflare One 장 | Jellyfin·Plex를 Tunnel 뒤에 두려다 ToS에 걸리는 장면, 4년째 열린 gRPC 이슈 |
| 6 | "무료는 공짜가 아니다" 엔터프라이즈 압박 | 중간 — 2024~2025-01 중심, 개인 독자 확률 낮음 | HN 42712433, 40481808 | 무료 티어 극대화 장의 박스 / 맺음말 | neya의 "$200/mo → $2000+" (카지노 사례는 맥락 주의) |
| 7 | Workers 런타임 한계(CPU·번들·nodejs_compat·체감 속도) | 중간 — 일부 2025 하반기 개선으로 해소 | HN 45584281, damoang 2488, OpenNext 문서 | Workers 기초 장 / 성능·Placement 장 | 다모앙 "요청이 LA로" → Smart Placement·Argo 실험기 |
| 8 | Containers 성숙도·비용 | 중간 — 일화 다수, 제품 변화 빠름 | HN 47320571, 48216483, sliplane | JVM 백엔드·Containers 장 | "작은 VM이 더 안정적이었다"(walla.my) vs "not even noticeable in billing" |
| (약함) | Access 관리자 보호, 캐시 오해, R2 읽기 비용, Stripe 웹훅 | 문서·가이드 위주 | 휴리스틱 7·9·10·6 | 인증·보안 장 / 캐싱 장 / 외부 통합 장 | `workers.dev` 우회 GPT 봇(white_viel), 배포 후 stale HTML(Manchitsanan) |

장애 사후 분석 인용(패턴 2 보강, [커뮤니티]): ojosilva "This is the multi-million dollar .unwrap() story." / otterley "Absent from this list are canary deployments and incremental or wave-based deployment of configuration files" / lionkor "Cloudflare is now below 99.9% uptime, for anyone keeping track."(2025-12-05) / SerCe(긍정) "kudos for releasing a post mortem in less than 24 hours" / GeekNews barca105 "CF정도되는 회사에서도 .unwrap()을 쓰네요" ↔ "근본적인 문제는 잘못된 쿼리죠." / redmi "Cloudflare에서 HTTP 트래픽 28%가 500 응답을 했다고 블로그에 올렸습니다" / R2 장애(2026-08-08) minraws "Please don't make me have to figure out how to move services again, I am tired folks." ↔ hnthrow10282910 "There was no data loss in this incident."(데이터 유실 여부 엇갈림 — §7 C-24).

---

## 7. 충돌·미확인 원장 (fact-checker 대조 기준)

> 형식: 충돌 내용 → 근거 → **책 권장 표현**. 🕒 = 출간 직전 재확인(§9와 연동).

| # | 항목 | 충돌·미확인 내용 | 근거 | 책 권장 표현 |
|---|---|---|---|---|
| C-1 | vinext 상태 🕒 | 가이드(2026-08-25) "vinext is in beta" ↔ vinext 1.0.0(2026-09-28) | web §12-1 | "vinext는 2026년 9월 28일 1.0이 나왔다. 다만 Cloudflare 공식 가이드는 (2026-10 기준) 아직 beta로 표기한다." |
| C-2 | Vectorize Free 가용성 | Workers Pricing "Vectorize is currently only available on the Workers paid plan" ↔ 같은 페이지·Vectorize Pricing의 Free 컬럼 | web §12-2 | Free 사용을 단정하지 말고 "Vectorize Pricing 문서에는 Free 포함량이 있으나 Workers 가격 문서는 유료 전용으로 적고 있다(2026-10 기준)" 또는 Paid 기준으로만 설명 |
| C-3 | Workflows 스크립트 크기 | Workflows Limits(2026-09-21) "3MB/10MB" ↔ Workers Limits·Changelog 64 MiB | web §12-3 | 64 MiB(Workers 공통, 2026-09-04 변경)를 쓰고 Workflows 페이지는 갱신 누락으로 간주 |
| C-4 | Workflows 기본 보존 | Pricing "30 days on the Paid plan" ↔ Changelog 2026-09-10 "Default instance retention for new Workflows on Workers Paid is seven days" | web §12-4 | 최신 changelog(2026-09-10) "신규 Workflow는 7일"을 쓰고, `default_retention`으로 조정 가능하다고 일반화 |
| C-5 | DO SQLite 스토리지 과금 개시 🕒 | 공지 2025-12-12 "target date of January 7, 2026" — Pricing 문서는 아직 미래형, 개시 확정 공지 미확인 | web §12-5 | "2026년 1월부터 과금하겠다고 예고됐다(목표일 2026-01-07). Free는 과금 없음." — 실제 개시 여부는 출간 전 확인 |
| C-6 | Analytics Engine 과금 | "Currently, you will not be billed" (2026-04-23), 개시 시점 미정 | web §12-6 | "2026-10 현재 과금하지 않는다고 문서에 적혀 있으나 가격표는 공개돼 있다" |
| C-7 | Tunnel replica 라우팅 | "routes to the geographically closest replica" ↔ "does not load balance across replicas" | web §12-7 | "replica는 HA용이지 LB용이 아니다(가까운 replica로 가지만 부하 분산 목적이 아님)" |
| C-8 | Kotlin/Wasm | 3자 "stable" ↔ kotlinlang.org "Beta" | web §12-8 | "Beta" |
| C-9 | 이벤트명 | 2026년 4월 = "Agents Week 2026" | web §12-9 | §0-1 |
| C-10 | Queue consumer CPU | Workers Pricing "Max of 15 minutes of CPU time per Cron Trigger or Queue Consumer invocation" ↔ Queues Limits "Consumer CPU time: Configurable to 5 minutes" + "Consumer duration (wall clock time) 15 minutes"; Workers Limits는 Cron만 15분 | web §12-10 | 보수적으로 "Queue consumer는 CPU 5분(설정)·벽시계 15분" + 출간 전 재확인 |
| C-11 | D1 호출당 쿼리 수 | D1 Limits(2026-04-21) "1000 (Workers Paid) / 50 (Free)" ↔ 서브리퀘스트 Paid 기본 10,000(최대 1,000만), 내부 서비스 Free 1,000(2026-02-11) | web §12-11 | 구체 수치를 피하고 "호출당 서브리퀘스트 한도를 따른다(2026-02 상향)"로 쓰거나, 수치를 쓸 경우 Workers Limits 기준 + 출처 명시 |
| C-12 | Browser Run 개명 시점 | 공지 원문 미확보, 2026-04 중순 추정 | web §12-12 | "2026년 Browser Rendering에서 Browser Run으로 이름이 바뀌었다" — 월 단위 단정 금지 |
| C-13 | Worker 크기 한도 | OpenNext 문서 Free 3 MiB / Paid 10 MiB ↔ 검색 요약 "Paid 15 MiB로 상향" ↔ 1차 changelog 64 MiB | community 대조 1, web §1 #12 | "2026-09-04부터 비압축 64 MiB(Free·Paid 동일)". 3/10/15 MiB는 낡은 값 |
| C-14 | Budget alerts 기본 활성화 시점 | URL 슬러그 2026-06-15 ↔ 게시·롤아웃 2026-07-20, 다음 청구 주기부터·코호트 순차 | community 대조 3, web §1 #17 | "2026년 7월부터 적격 Pay-as-you-go 계정에 $10 알림이 기본으로 켜지기 시작했다(순차 적용)" |
| C-15 | Workers CPU·메모리(검색 요약 경유) | 유료 CPU 기본 30초·최대 5분, 128MB isolate | community 대조 4 | **해소**: 1차(Workers Pricing 2026-10-02)와 일치 — 1차 출처로 인용 |
| C-16 | Containers 콜드 스타트 | 2~3초(sliplane, 베타) / 6~7초(HN nickandbro 2026-01-24) / 200ms(출처 불명) ↔ 공식 "often be in the 1-3 second range" + 2026-09-30 "more than 6x faster" | community 대조 2, web 3-4 | 공식 문구만 인용("이미지 크기 등에 따라 대개 1~3초"), "6배 빨라졌다"는 블로그 주장으로 출처 표기. 200ms는 쓰지 말 것 |
| C-17 | Tunnel 업로드 100MB | HN sylens 일화 | community 대조 5 | **해소**: Free 존 request body 최대 100 MB(초과 413, Workers Limits 2026-09-05)로 인용 |
| C-18 | Tunnel 비디오 ToS 현행 문구 | 커뮤니티 "조항이 바뀌었다" 주장 | community 대조 6 | 1차 FAQ 문구만 인용: "On Free, Pro, and Business plans, the service-specific terms require you to use a specific paid service to serve video and other large files." 단속 여부 언급 금지 |
| C-19 | Workers AI 무료 Neurons | 1차 10,000/일 ↔ Reddit 일화 5,000 | community 대조 9 | 10,000 Neurons/일(Workers AI Pricing 2026-10-01) |
| C-20 | $34,895 결말 | 면제 여부 미확인 | community 대조 10 | "청구서가 나왔다"까지만. 면제·환불 언급 금지 |
| C-21 | Page Rules 일정 | 2024-07 신규 Free 계정 차단, 2025 자동 이관 — 개인 블로그 근거 | community 대조 7 | "Page Rules는 Cache Rules 등 Rules 제품으로 대체되는 중(deprecated)"까지만. 날짜는 1차 확인 후 |
| C-22 | D1 Free 500MB / Paid 10GB, read replication 2025-04 | 검색 요약 | community 대조 8 | 한도는 1차(D1 Limits 2026-04-21: DB당 Free 500 MB·Paid 10 GB)로 인용. read replication 공개 시점은 "2025년"까지만 |
| C-23 | **계정 단위 하드캡 없음** 🕒 | 책 여러 장의 전제 | web §2-3, community 대조 11 | "2026년 10월 현재 계정 전체 지출 상한 기능은 없다" + 출간 직전 changelog 재확인 |
| C-24 | R2 장애(2026-08-08) 데이터 유실 | minraws(불만) ↔ hnthrow10282910 "There was no data loss in this incident." | community 패턴 2 | 유실 여부 단정 금지. 장애가 있었다는 사실만 |
| C-25 | KV 전파 "최대 60초" | dev.to·검색 요약 경유 ↔ KV Instant 블로그 classic p99 write replication 4.38 s | community 휴리스틱 4, 갭필 | "classic KV는 최종 일관성이라 변경이 전 세계에 반영되기까지 시간이 걸린다(공식 문서 기준 최대 수십 초 — 재확인)" + 블로그 실측(p99 4.38초)을 "전형값"으로 병기. PBS 수치 혼용 금지 |
| C-26 | RetainDB $36,000 | 검색 스니펫뿐 | community 패턴 1 | **인용 금지** |
| C-27 | 다모앙 "하루 50만 원 이상" | 요약 경유 | community 패턴 1 | 원문 재확인 전에는 쓰지 않거나 "한국 커뮤니티에도 로깅 설정 실수로 큰 청구를 받았다는 경험담이 있다"로 일반화 |
| C-28 | New Kids의 Workers 세부(SNI 프리워밍, LRU, 128MB) | [요약] 등급 | papers 논문 5 | Abstract 문장만 직접 인용, 세부는 공식 문서로 |
| C-29 | BeyondCorp 원칙 문장 | 원문 미확인 | papers 논문 6 | Abstract 두 문장만, 원칙은 NIST로 |
| C-30 | DDoS "약 2,100만 건" | 보도자료 [요약] | papers 논문 15 | 인용 금지. "/24의 약 1/3, 웹사이트 약 3%"만 |
| C-31 | ECMA-429 세부 | [요약] | papers 표준 6 | "2025년 12월 1판" 정도로, 인용 전 Ecma 페이지 확인 |
| C-32 | OAuth 2.1 리비전 🕒 | draft-16(2026-09-03), RFC 미발행 | papers 표준 4 | "초안(draft)"임을 명시 |
| C-33 | 저자 순서 | Schwarzl et al.(ESORICS vs arXiv), Koch et al.(Crossref 순서) | papers 논문 4·11 | ESORICS 출판본 순서 / Koch는 ACM 출판본 확인 |
| C-34 | 계보·채택 주장 | "Cloudflare가 S3-FIFO 사용", "DO는 Orleans에서 영감" | papers 논문 9·13 | **둘 다 쓰지 말 것.** "유사한 모델"·"엣지 캐시 연구의 일반 결과"로만 |
| C-35 | Zero Trust 가격 표기 | "$7 per user/month (paid annually)" — 월 결제 단가 미확인 | 갭필 | "연간 결제 기준 사용자당 월 $7(2026-10 기준)" |
| C-36 | Workers 기본 egress IP | 직접 명시 문장 없음 | 갭필 | §3-9 권장 표현 |
| C-37 | R2 Free 초과 = 과금 | "차단하지 않는다"는 문자 그대로의 문장은 없음(종합 판정) | 갭필 | §2-4 권장 표현 |
| C-38 | Firecracker 단위 | 논문 "5MB" ↔ 사이트 "5 MiB" | papers 논문 2 | 논문 인용 시 "5MB" |
| C-39 | Quick Tunnels "신기능" 오인 | 2021년부터 존재(noname120) | community 패턴 5 | 신기능은 Protected Quick Tunnels(2026-10-02)뿐 |

---

## 8. 도구 버전 표 (2026-10-02 기준, GitHub Releases, 검색 시점 2026-10-03)

| 도구 | 최신 버전 | 릴리스 일시(UTC) | 비고 | 출처 |
|------|-----------|------------------|------|------|
| `wrangler` | **4.147.0** | 2026-10-02 | 메이저는 여전히 v4. 최소 요구: 정적 자산 10만 파일 4.34.0+, 자동 구성 4.68.0+, Worker Previews 4.135.0+ | https://github.com/cloudflare/workers-sdk/releases |
| `@cloudflare/vite-plugin` | **1.62.5** | 2026-10-02 | | 同上 |
| `@cloudflare/vitest-plugin` | **1.3.6** | 2026-10-02 | 구 `@cloudflare/vitest-pool-workers` | 同上 |
| `create-cloudflare` (C3) | **2.73.2** | 2026-10-02 | | web.md 10-3 |
| `miniflare` | 5.x **alpha 프리릴리스** (예: `5.20261001.0-alpha`, 2026-10-01) | — | 직접 의존 금지(공식 권고) | 同上 |
| `cloudflared` | **2026.9.3** | 2026-09-24 | 2026.5.2+ 연결 사전 점검 내장. 1년 이내 버전만 지원 | https://github.com/cloudflare/cloudflared/releases |
| `@opennextjs/cloudflare` | **1.20.8** | 2026-10-02 | 기존 앱 유지보수 경로 | https://github.com/opennextjs/opennextjs-cloudflare/releases |
| `vinext` / `@vinext/cloudflare` | **1.0.1** (1.0.0은 2026-09-28) | 2026-10-01 | 가이드는 beta 표기(C-1) | https://github.com/cloudflare/vinext/releases |
| `cloudflare/wrangler-action` | **v4.1.3** (v4.0.0은 2026-05-12) | 2026-09-24 | 문서 예시 `@v4` | https://github.com/cloudflare/wrangler-action/releases |
| Terraform provider `cloudflare` | **v5.27.0** | 2026-10-03 | | https://github.com/cloudflare/terraform-provider-cloudflare/releases |
| `cf` CLI | 베타(2026-09-28 출시) | — | 버전 번호 미수집 | https://developers.cloudflare.com/cf/ |
| Workers Builds 기본 Node.js | 24.18.0 | 2026-07-30 | | Changelog |
| compatibility date 기준선 | `2026-08-04`+ → `nodejs_compat` 기본 ON | — | | Changelog 2026-08-04 |

---

## 9. 출간 직전 재확인 항목 🕒 (본문에는 반드시 날짜를 붙여 서술)

| 항목 | 현재 상태(2026-10-03) | 본문 서술 방식 |
|---|---|---|
| DO SQLite 스토리지 과금 개시 | 공지 2025-12-12, 목표일 2026-01-07, 확정 공지 미확인 | "2026년 1월부터 과금 예정으로 공지됐다(목표일 2026-01-07)" |
| Cloudflare Observability 가격 전환 | 2026-12-01부터 통합 가격(공지 2026-10-02) | "2026년 12월 1일부터 …로 바뀐다(2026-10 공지)" — 출간이 12월 이후면 현재형으로 전환 |
| Workflows step·storage 과금 | "no earlier than August 10, 2026"(2026-07-07) | "2026년 8월 10일 이후 과금 개시로 예고" — 실제 개시 확인 |
| vinext 가이드 beta 표기 | 1.0 출시, 가이드 beta | C-1 |
| `cf` CLI 베타 | 2026-09-28 베타 | "2026년 9월 베타로 공개" — GA 여부 확인 |
| Workers VPC 베타(무료) | 오픈 베타, 베타 동안 무료 | "베타 기간(2026-10 현재) 무료" — GA·과금 개시 확인 |
| KV Instant private beta | 2026-10-01 | 가격·한도 변경 가능성 |
| 인바운드 TCP·gRPC private beta | 2026-08-03 | 전망으로만 |
| Email Sending 공개 베타 | 2026-04-16 | GA 여부 |
| Cloudflare Traces 오픈 베타 | 2026-10-02 | GA 여부 |
| Access strict service token 기본 ON | 2026-10-05 이후 생성 조직 | 날짜 그대로 |
| 계정 단위 하드캡 부재 | 없음 | C-23 |
| Analytics Engine 미과금 | "Currently, you will not be billed" | C-6 |
| OAuth 2.1 | draft-16 | C-32 |
| `cloudflared` 32-bit Windows·Intel macOS 빌드 폐기 | 2027년 예정 | 날짜 그대로 |
| 도구 버전 표 전체 | 2026-10-02 기준 | §8 갱신 |

---

## 10. 참고문헌

### 10-1. 1차 문서·공식 블로그 (웹)
> developers.cloudflare.com 페이지는 본문 각 항목에 URL과 문서 날짜를 붙였다. 아래는 주요 출처의 대표 목록이며 전수 목록은 `research/web.md`.
- Cloudflare. Workers Pricing. https://developers.cloudflare.com/workers/platform/pricing/ , 2026-10-02.
- Cloudflare. Workers Limits. https://developers.cloudflare.com/workers/platform/limits/ , 2026-09-05.
- Cloudflare. Workers Cache. https://developers.cloudflare.com/workers/cache/ , 2026-09-22.
- Cloudflare. Static Assets — Billing and limitations. https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/ , 2026-04-23.
- Cloudflare. Next.js framework guide. https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/ , 2026-08-25.
- Cloudflare. R2 Pricing. https://developers.cloudflare.com/r2/pricing/ , 2026-10-01.
- Cloudflare. R2 Get started. https://developers.cloudflare.com/r2/get-started/ , 2026-04-21. [갭필]
- Cloudflare. Budget alerts. https://developers.cloudflare.com/billing/manage/budget-alerts/ , 2026-05-29.
- Cloudflare. Changelog: Budget alerts now on by default. https://developers.cloudflare.com/changelog/post/2026-06-15-budget-alerts-default-on/ , 2026-07-20.
- Cloudflare. Changelog: AI Gateway spend limits. https://developers.cloudflare.com/changelog/post/2026-06-05-spend-limits/ , 2026-06-05.
- Cloudflare. Threshold billing. https://developers.cloudflare.com/billing/threshold-billing/ , 2026-06-16.
- Cloudflare. Observability Pricing. https://developers.cloudflare.com/observability/pricing/ , 2026-10-02.
- Cloudflare. Containers (overview·limits·FAQ·pricing). https://developers.cloudflare.com/containers/ , 2026-09-30 / FAQ 2026-10-02 / Pricing 2026-08-28.
- Cloudflare. Cloudflare Tunnel. https://developers.cloudflare.com/tunnel/ , 2026-09-11.
- Cloudflare. Quick Tunnels. https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/ , 2026-09-30.
- Cloudflare. Cloudflare One Tunnels FAQ. https://developers.cloudflare.com/cloudflare-one/faq/cloudflare-tunnels-faq/ , 검색 시점 2026-10-03.
- Cloudflare. Validate Access JWT. https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/validating-json/ , 2026-05-06.
- Cloudflare. Workers — Cloudflare Access. https://developers.cloudflare.com/workers/configuration/cloudflare-access/ , 2026-08-18.
- Cloudflare. Seat management. https://developers.cloudflare.com/cloudflare-one/team-and-resources/users/seat-management/ , 2026-05-01.
- Cloudflare. Cloudflare One account limits. https://developers.cloudflare.com/cloudflare-one/account-limits/ , 2026-09-04.
- Cloudflare. Cloudflare Access product page (plans). https://www.cloudflare.com/sase/products/access/ , 날짜 표기 없음(검색 시점 2026-10-03). [갭필]
- Cloudflare. Smart Shield — Dedicated egress IPs. https://developers.cloudflare.com/smart-shield/configuration/dedicated-egress-ips/ , 2026-04-16. [갭필]
- Cloudflare. Smart Shield — Use with other Cloudflare products. https://developers.cloudflare.com/smart-shield/configuration/dedicated-egress-ips/other-products/ , 2026-05-07. [갭필]
- Cloudflare. Cloudflare One — Dedicated egress IPs. https://developers.cloudflare.com/cloudflare-one/traffic-policies/egress-policies/dedicated-egress-ips/ , 2026-09-04. [갭필]
- Cloudflare. Protect your origin server. https://developers.cloudflare.com/fundamentals/security/protect-your-origin-server/ , 2026-10-02. [갭필]
- Cloudflare. Hyperdrive. https://developers.cloudflare.com/hyperdrive/ ; Pricing 2026-06-18, Limits 2026-06-09.
- Cloudflare. R2 — AWS SDK for Java. https://developers.cloudflare.com/r2/examples/aws/aws-sdk-java/ , 2026-04-21.
- Cloudflare. Workers Vitest integration. https://developers.cloudflare.com/workers/testing/vitest-integration/ , 2026-08-20.
- Cloudflare. cf CLI. https://developers.cloudflare.com/cf/ , 2026-09-28.
- Cloudflare Blog. Mesh (Agents Week 2026). https://blog.cloudflare.com/mesh/ , 2026-04-14.
- Cloudflare Blog. Billable Usage API. https://blog.cloudflare.com/billable-usage-api/ , 2026-08-03.
- James Anderson, Matt "TK" Taylor. Vinext 1.0. https://blog.cloudflare.com/vinext-nextjs-on-vite/ , 2026-09-28.
- Rob Sutter. Introducing Workers KV Instant — powered by Quicksilver. https://blog.cloudflare.com/workers-kv-instant/ , 2026-10-01. [갭필]
- Cloudflare Blog. How small businesses can start using Cloudflare One today. https://blog.cloudflare.com/zero-trust-week-setting-up-cloudflare-one-as-a-small-business/ , 2020-10-15. [갭필]
- Mar Witek, Thomas Rubini. gRPC & inbound TCP for Workers. https://blog.cloudflare.com/grpc-workers/ , 2026-08-03.
- Cloudflare Blog. Containers cross-tenant vulnerability. https://blog.cloudflare.com/containers-cross-tenant-vulnerability/ , 2026-09-24.
- Cloudflare Blog. Faster agent sandboxes (Containers rebuilt). https://blog.cloudflare.com/faster-agent-sandboxes/ , 2026-09-30.
- Cloudflare Blog. Protected Quick Tunnels. https://blog.cloudflare.com/protected-quick-tunnels/ , 2026-10-02.
- Yomna Shousha 외. Worker Previews. https://blog.cloudflare.com/worker-previews/ , 2026-09-22.
- Cloudflare Blog. One observability platform. https://blog.cloudflare.com/one-observability-platform/ , 2026-10-02.
- Cloudflare Blog. Python Workers GA. https://blog.cloudflare.com/python-workers-ga/ , 2026-09-21.
- Cloudflare Blog. cf CLI launch. https://blog.cloudflare.com/cloudflare-cf-cli-launch/ , 2026-09-28 (한국어판 https://blog.cloudflare.com/ko-kr/cloudflare-cf-cli-launch/).
- Kenton Varda. Spectre research with TU Graz. https://blog.cloudflare.com/spectre-research-with-tu-graz/ , 2021-10-12.
- JetBrains. Kotlin/Wasm overview. https://kotlinlang.org/docs/wasm-overview.html , 2026-09-01.
- 한국어판 공식 블로그(검색 시점 2026-10-03 HTTP 200): cf CLI, Mesh, Billable Usage API, Agents Week 리뷰, Workers VPC(원문 2025-11-05). 한국어판 없음: vinext 1.0, Worker Previews, Protected Quick Tunnels, Workers protected by Access, Observability, Containers 재구축, Python Workers GA, gRPC.

### 10-2. 3자 웹
- Gregory Mitchell. Java on Cloudflare Workers. https://dev.to/gmitch215/java-on-cloudflare-workers-2njh , 2024-08-31.
- 잡가이버. (Workers + D1 개인 홈페이지). https://jab-guyver.co.kr/7280 , 2026-08-07.
- Nathan Schram (Little Bear Apps). D1 billing disaster & circuit breakers. https://littlebearapps.com/blog/d1-billing-disaster-circuit-breakers/ , 2026-03-18.
- Bryce Wray. From Pages to Workers (again). https://brycewray.com/posts/2025/05/pages-workers-again/ , 2025-05-27.
- Nicolas Fränkel. From Cloudflare zero-trust to Tailscale. https://blog.frankel.ch/cloudflare-zero-trust-tailscale/ , 2026-01-11.
- Oleksandr Kuryzhev. Cloudflare Workers Rate Limiting: 3 KV Mistakes We Made. https://dev.to/oleksandr_kuryzhev_42873f/cloudflare-workers-rate-limiting-3-kv-mistakes-we-made-4m9n , 2026-07-01.
- Jonas Scholz (sliplane, 이해관계자). Cloudflare Containers in 2026. https://sliplane.io/blog/cloudflare-released-containers-everything-you-need-to-know .
- Wire. Why we're moving Wire off Cloudflare Durable Objects. https://usewire.io/engineering/why-were-moving-wire-off-cloudflare-durable-objects/ , 2026-07-07.
- helloacm. Unexpected high usage of API requests. https://helloacm.com/cloudflare-unexpected-high-usage-of-api-requests-how-to-avoid-surprising-billing/ , 2022-08-25.
- robindev. Cloudflare took down our website. https://robindev.substack.com/p/cloudflare-took-down-our-website , 2024-05.
- Hono. Stripe webhook example. https://hono.dev/examples/stripe-webhook ; Stripe. Webhook signatures. https://docs.stripe.com/webhooks/signature.md ; Neon. Hyperdrive FAQ. https://neon.com/blog/hyperdrive-neon-faq .

### 10-3. 커뮤니티 (주요 스레드; 전수 목록은 `research/community.md`)
- HN 47787042 ($34,895, 2026-04-16) · 48611258 (simonw, 2026-06-20) · 49158930 (Billable Usage API, 2026-08-03) · 47322794 (circuit breaker, 2026-03-10) · 45973709 (2025-11-18 장애, 1465점) · 46162656 (2025-12-05 장애) · 47103649 (2026-02-20 장애) · 49224478 (R2 장애, 2026-08-08) · 49754785 (Quick Tunnels, 844점, 2026-09-18) · 45946865 (Zero Trust tunnels, 2025-11-16) · 47142156 (vinext, 2026-02-24) · 45584281 (CPU 벤치, 2025-10-14) · 47696317/47696640 (D1 10GB, 2026-04-08) · 47153800/47156303 (workers.dev, 2026-02-25) · 42712433 (Pages 대역폭, 2025-01-15) · 40481808 (2024-05-26) · 46029908 (중앙집중 논쟁, 2025-11-24)
- GitHub: opennextjs-cloudflare #972 · #1049 · #1157 · #653 · #1214; cloudflared #491 · #1158 · #1379; workers-sdk #2733
- GeekNews 24471 · 24848 · 18754 · 26988; 다모앙 development/2488
- Reddit(미러 스냅샷 경유): r/CloudFlare 1s40651 · 1s4bdml · 1r7skeq(원문 미열람) · 1u085uo; r/nextjs 1pex20t

### 10-4. 논문·표준 (확인 등급 유지)
- Jonas, E. et al. Cloud Programming Simplified: A Berkeley View on Serverless Computing. arXiv:1902.03383, 2019. [초록]
- Agache, A. et al. Firecracker: Lightweight Virtualization for Serverless Applications. NSDI '20, pp. 419–434, 2020. https://www.usenix.org/conference/nsdi20/presentation/agache [원문]
- Shahrad, M. et al. Serverless in the Wild. USENIX ATC '20. arXiv:2003.03423. [원문]
- Schwarzl, M., Borrello, P., Kogler, A., Varda, K., Schuster, T., Schwarz, M., Gruss, D. Robust and Scalable Process Isolation Against Spectre in the Cloud. ESORICS 2022, LNCS 13555, pp. 167–186. DOI 10.1007/978-3-031-17146-8_9. [초록]
- Schirmer, T. et al. New Kids: An Architecture and Performance Investigation of Second-Generation Serverless Platforms. arXiv:2604.15916, 2026 (ACM TOIT 게재 승인). [초록 + 일부 요약]
- Ward, R., Beyer, B. BeyondCorp: A New Approach to Enterprise Security. ;login: 39(6), pp. 6–11, 2014-12. [초록]
- Rose, S., Borchert, O., Mitchell, S., Connelly, S. Zero Trust Architecture. NIST SP 800-207, 2020-08. DOI 10.6028/NIST.SP.800-207. [초록]
- Maggs, B. M., Sitaraman, R. K. Algorithmic Nuggets in Content Delivery. ACM SIGCOMM CCR 45(3), pp. 52–66, 2015. DOI 10.1145/2805789.2805800. [원문]
- Yang, J. et al. FIFO queues are all you need for cache eviction. SOSP '23, pp. 130–149. DOI 10.1145/3600006.3613147. [초록]
- Calder, M. et al. Analyzing the Performance of an Anycast CDN. IMC '15, pp. 531–537. DOI 10.1145/2815675.2815717. [초록]
- Koch, T. et al. Anycast In Context: A Tale of Two Systems. SIGCOMM 2021, pp. 398–417. DOI 10.1145/3452296.3472891. [초록]
- Bailis, P. et al. Probabilistically Bounded Staleness for Practical Partial Quorums. PVLDB 5(8), pp. 776–787, 2012. arXiv:1204.6082. [초록]
- Bernstein, P. A. et al. Orleans: Distributed Virtual Actors for Programmability and Scalability. MSR-TR-2014-41, 2014. [초록] (관련: Bykov et al., SoCC '11, DOI 10.1145/2038916.2038932)
- Gaffney, K. P. et al. SQLite: Past, Present, and Future. PVLDB 15(12), pp. 3535–3547, 2022. DOI 10.14778/3554821.3554842. [초록]
- Jonker, M. et al. Millions of Targets Under Attack. IMC '17, pp. 100–113. DOI 10.1145/3131365.3131383. [초록]
- RFC 9111 (DOI 10.17487/RFC9111), RFC 9213 (10.17487/RFC9213), RFC 5861, RFC 9000, RFC 9114, RFC 7519 (10.17487/RFC7519). [초록]
- Hardt, D., Parecki, A., Lodderstedt, T. The OAuth 2.1 Authorization Framework. draft-ietf-oauth-v2-1-16, 2026-09-03 (Internet-Draft). [요약]
- Sakimura, N. et al. OpenID Connect Core 1.0 incorporating errata set 2. OpenID Foundation, 2023-12-15. [초록]
- Ecma International. ECMA-429 Minimum common web API, 1st edition, 2025-12. [요약]
- 검토 후 제외(papers.md): Wang et al. "Peeking Behind the Curtains of Serverless Platforms"(ATC '18), Shillaker & Pietzuch "Faasm"(ATC '20), Gillman et al. "Protecting Websites from Attack with Secure Delivery Networks"(IEEE Computer 2015), Bailis & Ghodsi "Eventual Consistency Today"(ACM Queue 2013).

---

## 11. 리서치 한계

**갭필로 해소된 것 (2026-10-03, research-lead)**
- (a) Zero Trust 좌석: Free 50명 한도·$0, Pay-as-you-go "$7 per user/month (paid annually)" — Access 제품 페이지 1차 확인(§3-6). 잔여: 월 결제 단가, 플랜 페이지(zero-trust-services) 원문.
- (b) R2 Free 초과 시: 과금(차단 아님) — get-started·pricing 2건 종합(§2-4). 잔여: "차단하지 않는다"는 문자 그대로의 문장 없음.
- (c) KV Instant: classic KV를 바꾼 것이 아니라 새 모드(private beta), 성능·가격·한도 원문 확보(§3-3). 잔여: classic KV의 "최대 60초" 문구 1차 재확인(C-25), KV Instant의 Free 포함량.
- (d) Workers 고정 egress IP: 계정 전용 IP는 Enterprise 제품임을 1차 확인, Workers `fetch()`/`connect()`와의 관계 확인(§3-9). 잔여: 기본 egress가 공유·비고정임을 직접 적은 문장.

**남은 [리서치 공백]**
1. **Java/Kotlin(Spring Security) Access JWT 검증 공식 예제 없음** → 책은 JJWT 또는 Spring Security Resource Server(JWKS: `https://<team>.cloudflareaccess.com/cdn-cgi/access/certs`, `aud` 검증) 예제를 **저자 작성 예제로 명시**해 제시하고, 키 회전(6주, 이전 키 7일 유효)을 반영한다.
2. **Spring Boot on Tunnel / JVM on Containers 실사용기 0건**(커뮤니티) → 저자 실험·비용 계산 예시로 채운다. Containers 상시 가동 비용은 공식 단가로 직접 계산해 검증.
3. Kotlin/Wasm 이후 Kotlin on Workers 지연 실측 없음(2023년 Kotlin/JS 보고만).
4. Hyperdrive의 Supabase·AWS RDS 개별 Cloudflare 1차 가이드 미정독(Supabase 권고는 Neon/Supabase 문서 경유).
5. Stripe/웹훅 Cloudflare 1차 전용 가이드 없음(Hono·Stripe 문서로 대체).
6. CASB 무료 범위, Gateway Free 기능 세부(로그 보존 등) 미확인.
7. Clerk/Auth0 ↔ Access 전용 가이드 미확인(generic OIDC 추정).
8. DO SQLite 스토리지 과금 실제 개시 확정 공지 미확인.
9. vinext 1.0 이후 실사용 후기 거의 없음.
10. 캐시 오해·Page Rules 이관의 1차 일정, Community 포럼 원문(403) 미확보.
11. Workers AI·Images·R2 operations 요금 폭탄 1인칭 사례 없음.
12. 하이브리드 AWS+Cloudflare 깊은 운영기 없음.
13. 컨퍼런스 발표(Cloudflare Connect 2026 등) 미수집.
14. 한국어 실사용기 빈약: velog·OKKY·커리어리·기업 기술 블로그에서 Cloudflare 개발자 플랫폼 실사용기 미발견. wikidocs 304528(Tunnel 국문) 403. 국문 근거는 GeekNews 장애 댓글·다모앙 1건·잡가이버 1건.
15. 학술: Workers isolate 콜드 스타트·메모리 독립 측정 논문은 New Kids 외 없음, DO·D1·R2 자체 논문 없음, KV 전파 지연 학술 측정 없음, Turnstile·봇 관리 학술 근거 미수집.

**접근 실패·편향**
- 실패한 리서처: 없음(3종 모두 산출). 
- 접근 실패: cloudflare.com/plans/zero-trust-services/(클라이언트 렌더링), changelog `2026-08-11-hostname-routing-ga-…`(404, 제목만), Reddit 직접 접근(미러 5건만), community.cloudflare.com(403), Discord·X·Mastodon·Lobsters 미검색(Lobsters는 R2 LaLiga 차단 링크 1건: https://lobste.rs/s/uetrpm/my_cloudflare_r2_has_been_blocked_from), ACM DL(403), BeyondCorp PDF 추출 실패.
- 편향: 커뮤니티 자료의 70% 이상이 영어 HN(인프라 관심·대기업 비판 성향). 이해관계자 발언(Cloudflare 직원 kentonv, Vercel, ngrok, Pinggy, sliplane)은 라벨 유지.
- 의도적 제외(web.md): 12개월 이상 지난 튜토리얼의 가격·한도·버전, Workers AI 모델별 단가 전체 표.

---

## 신선도 원장 (소스별 문서 날짜 · 검색 시점)

> 검색 시점은 전 항목 **2026-10-03**. 날짜 = 문서 `Last updated`/dateModified 또는 게시일.

**공식 문서 (developers.cloudflare.com)**
- Workers Pricing — 2026-10-02
- Workers Limits — 2026-09-05
- Workers Cache — 2026-09-22
- Static Assets Billing — 2026-04-23
- Workers languages — 2026-07-03 / WebAssembly — 2026-04-23
- Node.js compatibility — 2026-08-12
- Next.js 가이드·OpenNext 가이드 — 2026-08-25
- Pages 개요 — 2026-08-25 / Pages Limits — 2026-09-05
- Workers Sites — 2026-04-23
- Vite plugin — 2026-09-30
- Local development — 2026-08-20 / Vitest integration — 2026-08-20
- Workers Logs·Traces — 2026-10-02 / Real-time logs — 2026-06-25
- Workers — Cloudflare Access — 2026-08-18
- KV Limits — 2026-04-21
- D1 Limits — 2026-04-21
- R2 Pricing — 2026-10-01 [갭필 재확인]
- R2 Get started — 2026-04-21 [갭필]
- R2 AWS SDK for Java — 2026-04-21
- Optimize costs — 2026-05-04
- Workflows Pricing·Limits — 2026-09-21
- Queues Limits — 2026-04-21
- Hyperdrive Pricing — 2026-06-18 / Limits — 2026-06-09
- Workers AI Pricing — 2026-10-01
- AI Gateway Pricing — 2026-09-24
- Vectorize Pricing — 2026-04-21
- Browser Run Pricing — 2026-04-21
- Containers 개요·Limits — 2026-09-30 / FAQ — 2026-10-02 / Pricing — 2026-08-28
- Images Pricing — 2026-07-08
- Email Service Pricing — 2026-06-09 / Limits — 2026-09-25
- Analytics Engine Pricing — 2026-04-23
- Observability Pricing — 2026-10-02
- Workers VPC Pricing — 2026-09-16 / Workers VPC 개요 — 2026-09-18
- Budget alerts — 2026-05-29 / Usage-based billing — 2026-05-29 / Threshold billing — 2026-06-16
- Turnstile Plans — 2026-08-14
- Tunnel 개요·로컬 관리·run parameters·Kubernetes·downloads — 2026-09-11 / Tunnel get-started·Quick Tunnels — 2026-09-30
- Cloudflare One Tunnels FAQ — 날짜 미기록
- Access JWT 검증 — 2026-05-06
- IdP 연동 — 2026-06-19
- Seat management — 2026-05-01 [갭필 재확인]
- Cloudflare One account limits — 2026-09-04
- Remote browser isolation — 2026-09-30
- SSL client certificates — 2026-09-08 / API Shield — 2026-08-19
- Smart Shield dedicated egress IPs — 2026-04-16 [갭필]
- Smart Shield other products — 2026-05-07 [갭필]
- Cloudflare One dedicated egress IPs — 2026-09-04 [갭필]
- Protect your origin server — 2026-10-02 [갭필]
- CI/CD Builds — 2026-10-01 / GitHub Actions — 2026-09-18

**Changelog (게시일)** — 2025-09-16(remote bindings GA), 2025-09-18(Tunnel 호스트명 라우팅), 2025-09-19(ratelimit GA), 2025-10-03(Access JWT 구방식), 2025-10-10(시작 시간 1초), 2025-11-11(proxy-dns 제거 공지), 2025-11-21(Containers CPU 과금), 2025-12-08(Vite plugin 설정 선택), 2025-12-12(DO SQLite 과금 공지), 2026-01-22(Placement Hints·Require Access), 2026-02-04(Queues Free), 2026-02-11(subrequests), 2026-02-20(Tunnel 대시보드), 2026-02-25(autoconfig GA), 2026-02-26(async SWR), 2026-03-19(wrangler tunnel), 2026-03-24(Cache Response Rules), 2026-04-13(Containers GA), 2026-04-16(Email Sending 베타), 2026-04-21(Billable Usage 대시보드·Budget alerts), 2026-04-29(Hyperdrive VPC), 2026-05-07(React/Next.js CVE), 2026-05-27(cloudflared 사전 점검), 2026-06-05(AI Gateway spend limits·Gateway egress for Workers), 2026-06-18(Cloudflare IdP 기본), 2026-07-07(Workflows 과금), 2026-07-09(DO SQLite 전용), 2026-07-20(Budget alerts 기본 ON, 슬러그 2026-06-15), 2026-07-28(Workers AI Free 차단 모델), 2026-07-30(Builds Node 24.18.0), 2026-08-04(nodejs_compat 기본), 2026-08-07(Hyperdrive MySQL GA), 2026-08-10(Turnstile Spin GA), 2026-08-14(Workers Access), 2026-08-19(vitest-plugin), 2026-09-01(D1 Free 강제), 2026-09-04(Worker 64 MiB), 2026-09-08(Miniflare v5), 2026-09-10(Workflows 보존 7일), 2026-09-18(cloudflared 아키텍처 폐기), 2026-09-22(Worker Previews), 2026-09-28(cf CLI·cache invalidation), 2026-09-30(Logpush 전 플랜), 2026-10-02(Protected Quick Tunnels·strict service token·30일 Analytics)

**공식 블로그** — mesh 2026-04-14 · billable-usage-api 2026-08-03 · grpc-workers 2026-08-03 · agents-week-review-august-2026 2026-08-10 · workers-protected-by-access 2026-08-14 · workers-module-registry-nodejs 2026-09-09 · python-workers-ga 2026-09-21 · worker-previews 2026-09-22 · containers-cross-tenant-vulnerability 2026-09-24 · vinext-nextjs-on-vite 2026-09-28 · cloudflare-cf-cli-launch 2026-09-28 · faster-agent-sandboxes 2026-09-30 · workers-kv-instant 2026-10-01 [갭필] · one-observability-platform·cloudflare-tracing·protected-quick-tunnels 2026-10-02 · zero-trust-week small business 2020-10-15 [갭필] · spectre-research-with-tu-graz 2021-10-12 · workers-vpc-open-beta 2025-11-05

**마케팅 페이지** — cloudflare.com/sase/products/access/ — 날짜 표기 없음, 검색 시점 2026-10-03 [갭필]

**GitHub 릴리스** — §8 표(2026-09-24 ~ 2026-10-03)

**3자 웹** — kotlinlang.org 2026-09-01 · dev.to gmitch215 2024-08-31 · 잡가이버 2026-08-07 · Little Bear Apps 2026-03-18 · Bryce Wray 2025-05-27 · Fränkel 2026-01-11 · Kuryzhev 2026-07-01 · Wire 2026-07-07 · helloacm 2022-08-25(오래됨) · robindev 2024-05(오래됨) · sliplane(날짜 미기록) · eastondev 2025-12-01

**커뮤니티** — 수집 범위 2025-01 ~ 2026-10 우선, 개별 날짜는 §2-5·§3·§4·§6 각 항목에 표기. 오래된 항목(2022·2023·2024)은 "오래됨" 표시 유지.

**논문·표준** — 2012~2026 (§10-4 연도). 최신: New Kids v2 2026-08-14, OAuth 2.1 draft-16 2026-09-03. 피인용수는 Semantic Scholar/Crossref 2026-10-03 조회.
