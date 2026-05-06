# Vercel 입문서 — 종합 레퍼런스

대상 독자: JS/TS·React/Next.js 경험은 있지만 실무 깊이가 얕고 Vercel은 처음 또는 거의 처음인 개발자.
범위: 토이 프로젝트 → 사이드 → 초기 스타트업 → 본격 SaaS로 성장하는 과정에서 Vercel을 어떻게 활용·조정하는지.
기준 시점: 2026-05. 가격·한도·기능 가용성은 변동성이 크다는 점을 본문에서 매번 환기할 것.
출처 표기 규칙: 각 주장에 대표 URL 1개를 inline으로 단다. 같은 주장이 여러 소스에 있으면 가장 권위 있는 일차 자료(공식 문서 > 저자 명확한 분석 > 커뮤니티) 하나만 인용한다.

---

## 1. 개념·정의

### 1.1 Vercel이라는 제품의 정체
- Vercel은 Frontend Cloud를 표방한다. Git push 한 번으로 빌드·배포·CDN·SSL·프리뷰·서버리스 함수까지 묶어 제공하는 매니지드 PaaS다. ([Frameworks on Vercel](https://vercel.com/docs/frameworks))
- 35+ 프레임워크에 대해 "first-class" 어댑션을 가진다. 빌드 명령·라우팅·이미지 최적화·env 주입을 표준 추상화로 감싼다. Next.js는 Vercel이 직접 메인테인하므로 가장 깊게 통합된다. ([Frameworks on Vercel](https://vercel.com/docs/frameworks))

### 1.2 엣지 네트워크와 PoP
- Vercel은 자체 글로벌 PoP에 정적 자산·CDN 캐시·Edge Functions를 분산한다. 2025 대비 2026년에는 비미국권 TTFB가 개선됐다. ([DanubeData 비교 2026](https://danubedata.ro/blog/cloudflare-pages-vs-netlify-vs-vercel-static-hosting-2026))
- 단, PoP 수만 보면 Cloudflare(300+)가 더 많다. 글로벌 사용자 분포에 따라 차이가 발생한다. (같은 출처)

### 1.3 빌드 파이프라인
- Git 연결 시 push마다 자동 빌드 → preview URL 생성 → main merge 시 production. ([Vercel Academy: Production Monorepos](https://vercel.com/academy/production-monorepos))
- 모노레포에서는 Turborepo Remote Cache로 affected workspace만 빌드 가능. ([Turborepo on Vercel](https://vercel.com/solutions/turborepo))

### 1.4 함수 런타임 — Node vs Edge vs Fluid
- **Node runtime**: Node API 전체 사용 가능, region pinning 가능. 데이터 변환·파일 처리·외부 SDK 호출 적합.
- **Edge runtime**: 글로벌 분산. filesystem 접근 불가, `require()` 직접 호출 불가, 대부분 Node API 미지원. 25초 안에 응답 시작, 최대 300초 스트리밍. ([Vercel Functions Limits](https://vercel.com/docs/functions/limitations))
- **Fluid compute** (2025 신설, 2026년 신규 배포 기본값): 단일 인스턴스가 다중 요청을 동시 처리. Bytecode 최적화·pre-warming으로 cold start 영향 완화. CPU 시간 ms 단위로만 과금하며 I/O 대기 시간은 무료. ([Fluid compute 공식](https://vercel.com/docs/fluid-compute), [Introducing Fluid compute](https://vercel.com/blog/introducing-fluid-compute))
- Fluid는 Vercel이 새로 발명한 기술이 아니라, 학계가 분류한 caching + application-level optimization 접근의 제품화에 가깝다. ([Mahmoudi et al. 2024, ACM Computing Surveys](https://dl.acm.org/doi/abs/10.1145/3700875))

### 1.5 렌더링 전략 — SSG / SSR / ISR / PPR
- **SSG**: 빌드 타임 정적 생성. 가장 싸고 가장 빠름.
- **SSR**: 요청 시 매번 렌더. 동적이지만 함수 비용 ↑.
- **ISR (Incremental Static Regeneration)**: revalidate 주기로 재생성. 본질은 RFC 5861의 stale-while-revalidate를 framework 레벨로 통합한 것이다. ([RFC 5861](https://datatracker.ietf.org/doc/html/rfc5861))
- **PPR (Partial Prerendering)**: Next.js 15 stable, 16의 cacheComponents flag 기본값. 정적 shell + dynamic Suspense holes를 단일 응답에 결합. 50ms 미만 TTFB와 부분 동적성을 동시에 달성하는 첫 모델이라는 평. ([PPR Platform Guide](https://nextjs.org/docs/app/guides/ppr-platform-guide), [PkgPulse 비교 2026](https://www.pkgpulse.com/blog/ssr-vs-ssg-vs-isr-vs-ppr-rendering-2026))

### 1.6 Preview Deployments
- 모든 PR/branch에 고유 URL이 생성된다. 디자인 리뷰·QA·스테이크홀더 데모에 즉시 활용 가능. 단, preview에 production 시크릿을 재사용하면 모든 PR이 production-급 폭발 반경을 갖는다. ([ShipSafer 분석](https://www.shipsafer.ai/blog/vercel-deployment-security))

---

## 2. 사용·기능

### 2.1 배포 방식 — CLI / Git 연동 / API
- 가장 흔한 패턴: GitHub/GitLab/Bitbucket 연결 후 push마다 자동.
- CLI 패턴: `vercel deploy --prebuilt --token=$VERCEL_TOKEN`. production은 `--prod` 추가. GitHub Actions에서 monorepo 부분 배포에 활용. ([Turborepo CI 가이드](https://turborepo.dev/docs/guides/ci-vendors/github-actions), [Vercel Academy GitHub Actions](https://vercel.com/academy/production-monorepos/github-actions))

### 2.2 도메인·SSL
- Let's Encrypt 와일드카드 인증서 자동 발급·갱신. 만료 14-30일 전 자동 갱신. ([Automatic SSL with Vercel and Let's Encrypt](https://vercel.com/blog/automatic-ssl-with-vercel-lets-encrypt))
- Vercel에서 산 도메인은 자동 갱신. 외부 등록 도메인은 수동 갱신. ([Working with Domains](https://vercel.com/docs/domains/working-with-domains))
- 커스텀 SSL 업로드 시 5일 전부터 백업으로 자동 발급 인증서가 다운타임을 막는다. (같은 출처)

### 2.3 환경 변수와 Secrets
- 환경별(Development/Preview/Production) 분리 가능. `Sensitive` 플래그를 켜면 dashboard·API에서 다시 못 읽는 형태로 저장된다. ([Sensitive environment variables](https://vercel.com/docs/environment-variables/sensitive-environment-variables))
- 일반 변수는 decrypt 가능 형태로 보관 — 2026년 4월 보안사고에서 노출된 것이 정확히 이쪽이다. ([Vercel April 2026 incident](https://vercel.com/kb/bulletin/vercel-april-2026-security-incident))
- 환경 변수 회전은 과거 배포에 자동 반영되지 않는다. 회전 후 모든 환경에서 재배포가 필수. ([ShipSafer](https://www.shipsafer.ai/blog/vercel-deployment-security))

### 2.4 팀·역할·권한
- Pro부터 seat당 $20/월 과금. 5명만 모여도 $100/월 베이스라인. ([Vercel Pricing](https://vercel.com/pricing))
- Enterprise는 SCIM·SSO·Audit Log·Secure Compute 포함. ([Vercel Compliance](https://vercel.com/docs/security/compliance))

### 2.5 Vercel CLI
- 로컬 개발 (`vercel dev`), 환경 동기화 (`vercel env pull`), 배포 (`vercel`), 프로젝트 링크 (`vercel link`)가 일상 워크플로의 기본. ([Vercel CLI 문서](https://vercel.com/docs))

### 2.6 Monorepo 지원
- 공식 통합: Turborepo. Remote Cache (`TURBO_TEAM` 변수 + 토큰)로 빌드 시간 50%+ 절감 사례 다수. ([Turborepo on Vercel](https://vercel.com/solutions/turborepo))

### 2.7 외부 CI 통합 (GitHub Actions 등)
- Build & Deploy 분리 패턴: Actions에서 빌드/테스트 → `vercel deploy --prebuilt`로 업로드만 위임. ([Vercel Academy](https://vercel.com/academy/production-monorepos/github-actions))

### 2.8 활용 기능 카탈로그
- **Edge Middleware**: 인증·A/B testing·feature flag rollout·리다이렉트·헤더 조작·봇 차단. 무거운 로직은 Route Handler로 위임 권장. ([Edge Middleware Templates](https://vercel.com/templates/edge-middleware))
- **Cron Jobs**: 모든 플랜 포함. Hobby는 일 1회 제한. 함수 quota에 차감. ([Cron Jobs](https://vercel.com/docs/cron-jobs))
- **Storage 마켓플레이스**: 자체 KV·Postgres가 sunset되고 Marketplace Storage로 통합 (Neon, Upstash 등 통합 빌링). Blob과 Edge Config는 Vercel 자체 운영. ([Vercel Storage overview](https://vercel.com/docs/storage), [Introducing storage on Vercel](https://vercel.com/blog/vercel-storage))
- **Edge Config**: read-mostly 글로벌 데이터 (피처 플래그·리다이렉트 룰·차단 IP). p50 1ms 미만, 99% read 10ms 이하. ([Edge Config 패키지](https://github.com/vercel/storage/tree/main/packages/edge-config))
- **Speed Insights**: 프로젝트당 $10/월 add-on. Core Web Vitals 실시간 모니터링. ([Schematic Pricing 2026](https://schematichq.com/blog/vercel-pricing))
- **Web Analytics**: 프로젝트당 $10/월, 월 25K 이벤트. 초과 시 1K당 $0.25. (같은 출처)
- **Image Optimization**: Next.js `<Image>` 컴포넌트와 통합. on-the-fly 변환·반응형. 가격은 변환된 이미지 수와 source bandwidth로 산정. 28K 이미지 사례 월 $115 추가. ([Image Optimization 가격](https://vercel.com/docs/image-optimization/limits-and-pricing))
- **Vercel Firewall / WAF**: Bot Protection Managed Ruleset, AI Bots Managed Ruleset, BotID(invisible bot detection), Custom WAF Rules. ([Web Application Firewall](https://vercel.com/security/web-application-firewall), [Vercel BotID 분석](https://www.thisdot.co/blog/vercel-botid-the-invisible-bot-protection-you-needed))
- **Vercel AI SDK·AI Gateway**: 다수 모델(OpenAI, Google Imagen, Black Forest Labs Flux, Recraft 등)을 단일 API로 라우팅. 인증·응답 포맷 자동. 가격은 토큰 기반 + Vercel 마진(투명도 비판 있음). ([AI SDK Image Generation](https://vercel.com/docs/ai-gateway/capabilities/image-generation/ai-sdk), [TrueFoundry 분석](https://www.truefoundry.com/blog/understanding-vercel-ai-gateway-pricing))
- **OG Image Generation**: Next.js의 `ImageResponse` API와 Vercel 엣지에서 동적 OG 이미지 생성 (Vercel 자료 공식 추가 확인 필요).

---

## 3. 성장 단계별 활용 (토이 → 사이드 → 초기 스타트업 → 본격 SaaS)

### 3.1 토이 프로젝트 (Hobby)
- 플랜: Hobby (무료). 비상업적·개인 용도 한정. ([Vercel Hobby Plan](https://vercel.com/docs/plans/hobby))
- 자원 한도(2026-05): Fast Data Transfer 100GB / 함수 invocations 1M / Active CPU 4시간 / Provisioned Memory 360 GB-hrs/월. (같은 출처)
- 켜야 할 것: Git 연동 자동 배포, 기본 도메인, Sensitive env 플래그, robots.txt + Deployment Protection(preview 노출 차단).
- 주의: AdSense, Stripe 결제, Sponsorship 링크 한 줄만 들어가도 ToS 위반 신호 → Pro 강제 업그레이드. ([HN Ask: Why are people paying so much for Vercel?](https://news.ycombinator.com/item?id=41031912))
- Cron 한도(일 1회)가 답답하면 사이드 단계로 이동 신호다. ([Cron Jobs](https://vercel.com/docs/cron-jobs))

### 3.2 사이드 프로젝트 (Pro 진입)
- 트리거: 첫 결제(1원이라도) / 회사 명함이 박힌 프로젝트 / cron이 자주 필요 / 팀원 합류.
- 플랜: Pro $20/seat/월. 1TB bandwidth, 10M edge requests, ~1,000 GB-hours 함수 메모리 포함. ([Vercel Pricing](https://vercel.com/pricing))
- 즉시 켜야 할 가드레일: Spend Management(임계 알림 + 자동 일시정지). 디폴트 OFF다. ([Manage and Optimize Usage](https://vercel.com/docs/pricing/manage-and-optimize-usage))
- 권장 운영:
  - Sensitive 플래그 의심 시 모두 켜기. ([GitGuardian 분석](https://blog.gitguardian.com/vercel-april-2026-incident-non-sensitive-environment-variables-need-investigation-too/))
  - Preview에 production 시크릿 재사용 금지 — 환경별 분리.
  - Web Analytics·Speed Insights는 필요할 때만. 매 프로젝트 $10씩 더해진다.

### 3.3 초기 스타트업 (Pro + 외부 보강)
- 트래픽이 한 자리수 만 명/월을 넘기 시작하면 비용 곡선이 꺾인다. ([Vercel Bill Shock 사례](https://journeywithibrahim.medium.com/vercel-bill-shock-from-700-to-120-ec24ee9755c3))
- 외부 보강 패턴:
  - **이미지를 외부 CDN으로 분리**: Cloudflare R2 + CDN, ImgIX, Bunny CDN. Image Optimization 비용 80%+ 절감 사례. ([Cutting Vercel Costs by 80%](https://www.howdygo.com/blog/cutting-howdygos-vercel-costs-by-80-without-compromising-ux-or-dx))
  - **Cloudflare 앞단**: 도메인 → Cloudflare → Vercel. WAF/DDoS 흡수, 캐시 적중 시 Vercel 전송량 0. 단, Vercel 자체 ISR과 캐시 헤더 호환에 주의. ([Schematic 분석](https://schematichq.com/blog/vercel-pricing))
  - **DB는 Vercel 마켓플레이스 또는 외부**: Neon, Upstash, Supabase, PlanetScale 등. 자체 KV/Postgres는 sunset. ([Vercel Storage overview](https://vercel.com/docs/storage))
  - **Edge Config**로 변하지 않는 메타데이터·차단 룰·feature flag 분리.
- 보안 기본: WAF Custom Rules, BotID, Attack Challenge Mode 활성화 룰북.

### 3.4 본격 SaaS (Pro 한도 초과 또는 Enterprise 검토)
- 신호: bandwidth 5TB+ / 함수 GB-hours 수천 / 팀원 10명+ / SOC 2·HIPAA·GDPR 컴플라이언스 요구 / 99.99% SLA 필요.
- Enterprise 추가 가치: 커스텀 한도·가격, SCIM, Audit Log, Secure Compute(HIPAA에 필수), 24/7 지원. ([Vercel Compliance](https://vercel.com/docs/security/compliance))
- 검토할 분기점:
  - 비용이 인프라 엔지니어 풀타임 1명 인건비를 넘는가? → 셀프호스트 또는 멀티 호스트 검토.
  - 데이터 주권 요구가 있는가 (EU·HIPAA)? → Secure Compute 또는 자체 인프라.
  - Next.js의 모든 Vercel-only 기능을 다 쓰는가? → 셀프호스트 시 손실 평가 필요. ([Self-Hosting Next.js: What You Gain (and Lose)](https://dev.to/rbobr/self-hosting-nextjs-what-you-gain-and-lose-vs-vercel-4g8c))
- 비상 탈출 옵션을 항상 손에 두기: `next.config.js`의 `output: "standalone"` 빌드를 평소에 익혀둔다. Docker 이미지 100-200MB. ([Next.js Self-Hosting Guide](https://nextjs.org/docs/app/guides/self-hosting))

---

## 4. 비용

### 4.1 플랜 구조 (기준 시점 2026-05)
| 플랜 | 베이스 | 핵심 포함 | 비고 |
|------|--------|----------|------|
| Hobby | 무료 | Fast Data Transfer 100GB, invocations 1M, Active CPU 4h, Provisioned Memory 360 GB-hrs | 비상업·개인 용도 한정 |
| Pro | $20/seat/월 | Bandwidth 1TB, Edge Requests 10M, 함수 메모리 ~1,000 GB-hrs | 초과 시 GB당 $0.15 |
| Enterprise | 커스텀 | 99.99% SLA, SCIM, Audit Log, Secure Compute, HIPAA | 영업 컨택 |
출처: [Vercel Pricing](https://vercel.com/pricing), [Schematic Pricing 2026](https://schematichq.com/blog/vercel-pricing).

### 4.2 함수 과금 3축 (Pro)
- Invocations: $0.60 / 1M
- CPU-hour (Active CPU): $0.128
- Memory: $0.0106 / GB-hour
출처: [Schematic Pricing 2026](https://schematichq.com/blog/vercel-pricing).
- Fluid compute는 I/O 대기 동안 과금되지 않으므로, AI 에이전트처럼 외부 API 호출이 긴 함수에서 효과가 크다. ([Introducing Fluid compute](https://vercel.com/blog/introducing-fluid-compute))

### 4.3 자주 폭증하는 항목
1. **Bandwidth**: 1TB는 빠르게 소진된다. 페이지 평균 2-5MB → 1TB는 20-50만 PV/월 수준. 바이럴 한 번이면 하루에 다 쓴다. 초과 시 GB당 $0.15. ([Schematic 2026](https://schematichq.com/blog/vercel-pricing), [Flexprice 2026](https://flexprice.io/blog/vercel-pricing-breakdown))
2. **Image Optimization**: 28K 이미지 사례 월 $115 추가, 기본 $20 구독 대비 7배. LLM 봇 크롤링 시 더 폭증. ([Image Optimization 가격](https://vercel.com/docs/image-optimization/limits-and-pricing), [HN: Cost of Being Crawled](https://news.ycombinator.com/item?id=43687431))
3. **Edge Requests**: 10M 초과 시 1M당 $2.
4. **Seat 수**: Pro에서 팀원 1명마다 $20.
5. **Add-on**: Speed Insights $10/proj, Web Analytics $10/proj/25K 이벤트.

### 4.4 비용 폭탄 사례
- $20 → $700 (Image, JSON API 응답, ISR/SSR fetch가 모두 bandwidth로 계상). aggressive caching 도입 후 $120(83% 감소). ([Vercel Bill Shock](https://journeywithibrahim.medium.com/vercel-bill-shock-from-700-to-120-ec24ee9755c3))
- DDoS 한 번에 $20,000 청구된 사례 보고. Vercel은 "차단된 트래픽은 미과금"이지만 mitigation 발동 직전까지의 트래픽은 청구된다. ([HN Worst Nightmare](https://news.ycombinator.com/item?id=39521028), [DDoS Mitigation 공식](https://vercel.com/docs/vercel-firewall/ddos-mitigation))
- Netlify $104k 청구서 사건은 결국 면제 처리됐고, Vercel도 "legitimate mistake"는 forgive 정책을 운영하지만 명시 SLA는 없다. ([HN $104k bill](https://news.ycombinator.com/item?id=39520776))

### 4.5 가드레일
- **Spend Management**: 임계 알림 + 자동 일시정지 + 웹훅. Pro에서 만들자마자 켤 것. ([공식](https://vercel.com/docs/pricing/manage-and-optimize-usage))
- **Attack Challenge Mode**: 모든 플랜에서 무료. 챌린지 차단 트래픽은 미과금. ([공식](https://vercel.com/docs/vercel-firewall/attack-challenge-mode))
- **Cloudflare 앞단**: WAF 강화 + 캐시 적중 시 Vercel bandwidth 0.
- **이미지 외부 CDN 위탁**: 가장 큰 단일 절감 항목.
- **결제 카드 등록 안 하기 (Hobby)**: 한도 초과 시 자동 정지된다. 토이에서는 일부러 등록 안 두는 것도 가드레일.

### 4.6 모니터링
- 대시보드 Usage 탭, Spend Management 임계, 자체 OpenTelemetry 연동(Enterprise).
- 함수별·라우트별 사용량 분해는 공식 대시보드에 점진적 개선 중.

---

## 5. 보안

### 5.1 환경 변수와 비밀
- Sensitive 플래그를 의심 시 모두 켠다. UI에서 다시 못 읽는 게 단점이 아니라 보안 자산이다. ([Sensitive env vars](https://vercel.com/docs/environment-variables/sensitive-environment-variables))
- 회전 후에는 모든 환경에서 재배포 필수 — 과거 배포는 옛 값을 그대로 쓴다. ([ShipSafer](https://www.shipsafer.ai/blog/vercel-deployment-security))
- Production/Preview/Development 시크릿은 항상 분리. 특히 DB·결제·Auth·Admin.

### 5.2 Preview 환경 노출 위험
- `*.vercel.app` preview URL은 검색 엔진에 잡힐 수 있다. robots.txt + Deployment Protection 필수. (커뮤니티 공통 권고)
- Deployment Protection: SSO, Password, Allowlist 등. 무료 플랜은 옵션 제한. ([Deployment Protection 공식](https://vercel.com/docs/deployment-protection))

### 5.3 Edge Middleware로 인증·봇 차단
- Basic Auth 패턴, Bot Protection (Botd, DataDome), JWT 검증, Rate limit 등 표준 템플릿 다수. ([Edge Middleware Templates](https://vercel.com/templates/edge-middleware))
- 무거운 로직은 절대 Edge Middleware에 넣지 말 것 — fetch/헤더 조작 전용. (커뮤니티 공통)

### 5.4 Firewall / WAF
- Managed Rulesets (Bot, AI Bot), BotID, Custom WAF Rules. ([Web Application Firewall](https://vercel.com/security/web-application-firewall))
- BotID는 invisible fingerprint 기반, Middleware에 metadata 주입 → rate limit, fraud detection에 활용. ([This Dot Labs 분석](https://www.thisdot.co/blog/vercel-botid-the-invisible-bot-protection-you-needed))

### 5.5 DDoS 대응
- Attack Challenge Mode: 모든 플랜 무료, SEO 영향 없음, 챌린지 차단 트래픽 미과금. ([공식](https://vercel.com/docs/vercel-firewall/attack-challenge-mode))
- DDoS Mitigation: 차단 트래픽 미과금, 단 mitigation 발동 전 처리분은 청구. ([공식](https://vercel.com/docs/vercel-firewall/ddos-mitigation))
- 외부 CDN(Cloudflare) 앞단 배치는 강력한 추가 흡수층.

### 5.6 도메인·SSL
- Let's Encrypt 자동 발급/갱신. 외부 등록 도메인은 갱신 수동. 커스텀 SSL은 5일 전부터 백업 발급으로 다운타임 방지. ([공식](https://vercel.com/docs/domains/working-with-ssl))

### 5.7 컴플라이언스
- SOC 2 Type 2, ISO/IEC 27001, PCI DSS, HIPAA(Enterprise + Secure Compute), GDPR, EU-US DPF, ISO 27018, NIS 2, DORA 등. ([Vercel Compliance](https://vercel.com/docs/security/compliance), [HIPAA 지원 발표](https://vercel.com/blog/vercel-supports-hipaa-compliance))

### 5.8 2026년 4월 보안사고 사례
- Context.ai(직원이 사용한 third-party AI tool)의 Lumma Stealer 감염 → Google Workspace OAuth → Vercel 직원 계정 → 내부 시스템 → non-sensitive 환경 변수 enumerate·decrypt. Sensitive 처리된 변수는 무사. ([Vercel KB Bulletin](https://vercel.com/kb/bulletin/vercel-april-2026-security-incident), [Trend Micro 분석](https://www.trendmicro.com/en_us/research/26/d/vercel-breach-oauth-supply-chain.html))
- 교훈: non-sensitive로 분류된 변수도 자주 비밀을 담는다(DB URL, signing key 등). 회전 + 재배포가 정답. ([GitGuardian 분석](https://blog.gitguardian.com/vercel-april-2026-incident-non-sensitive-environment-variables-need-investigation-too/), [GeekNews 한국어](https://news.hada.io/topic?id=28700))

---

## 6. 함정·주의사항

### 6.1 런타임 한도 (Vercel Functions Limits)
- Edge: 25초 안에 응답 시작, 최대 300초 스트리밍. filesystem·`require()`·대부분 Node API 미지원.
- Node (Pro Fluid): max duration 800초까지 가능. ([Limits 공식](https://vercel.com/docs/limits))
- 함수 응답·요청 body 4.5MB 한도, deployment build duration 기본 45분. (같은 출처)

### 6.2 Cold Start
- Fluid compute로 영향 85% 절감 주장이지만 0이 되지는 않는다. 학계 연구는 cold start가 first invocation의 50-90% latency를 차지한다고 본다. ([ACM Computing Surveys 2024](https://dl.acm.org/doi/abs/10.1145/3700875))
- Edge runtime은 cold start가 더 짧지만 Node API 제약이 큰 trade-off.

### 6.3 빌드 캐시 함정
- Turborepo Remote Cache의 invalidation key를 잘못 설정하면 잘못된 캐시 적중 → 운영 사고. CI 캐시 디버깅이 필요할 때 `vercel build --debug`.

### 6.4 ISR revalidate 오해
- `revalidate = 60`은 "60초마다 재생성"이 아니라 "60초 지난 뒤 다음 요청부터 백그라운드 재생성". 첫 요청은 stale. ([ISR 공식](https://vercel.com/docs/incremental-static-regeneration))
- 데이터 정합성이 즉시 필요하면 `revalidateTag`/`revalidatePath` on-demand 호출.

### 6.5 Edge Runtime의 Node API 제약
- pdfkit, sharp, bcrypt, AWS SDK v2 같이 Node API에 깊이 의존하는 라이브러리는 import 자체 실패. ([Vercel Functions Limits](https://vercel.com/docs/functions/limitations), GitHub vercel/vercel #4502)
- Edge에서는 fetch·crypto.subtle·Web Streams만 가능하다고 가정하고 시작.

### 6.6 Vendor Lock-in (관점별 정리)
- "사실상 종속" 관점: ISR·Image·Middleware·PPR이 Vercel에서 best/only로 작동. ([dev.to 자기호스팅](https://dev.to/rbobr/self-hosting-nextjs-what-you-gain-and-lose-vs-vercel-4g8c), [eduardoboucas 분석](https://eduardoboucas.com/posts/2025-03-25-you-should-know-this-before-choosing-nextjs/))
- "덜 종속" 관점: Next.js의 ~70%가 Vercel 외부에서 운영. Walmart, Nike, Claude.ai 사례. Adapter API stable, OpenNext 성숙. ([Vercel anti-lock-in 블로그](https://vercel.com/blog/vercel-the-anti-vendor-lock-in-cloud), [Next.js Across Platforms](https://nextjs.org/blog/nextjs-across-platforms))
- 결정적 변수: Next.js 16.2의 stable Adapter API (Cloudflare/Netlify/Amplify/Google/OpenNext 공동 설계).

### 6.7 청구서 폭탄
- Image Optimization, Bandwidth, Edge Requests, Seat 수, Add-on이 폭증의 주범. 가드레일 없이 운영하지 말 것. (위 4.4·4.5 참조)

### 6.8 Preview 사고
- production DB credential을 preview에도 주면 PR마다 prod 폭발 반경. ([ShipSafer](https://www.shipsafer.ai/blog/vercel-deployment-security))
- preview 도메인이 검색 엔진에 인덱싱될 위험. (커뮤니티 공통)

### 6.9 Hobby의 비상업 ToS
- AdSense·Stripe·후원 링크 한 줄로도 위반 신호. 정식 사이드 시작 시점에 Pro 전환이 안전하다. ([HN](https://news.ycombinator.com/item?id=41031912))

---

## 7. 대안 비교

### 7.1 한 줄 매트릭스 (2026-05)
| 플랫폼 | 강점 | 약점 | 적합 시점 |
|--------|------|------|-----------|
| Vercel | DX 1위, Next.js 통합, preview, AI Gateway | bandwidth 비쌈, 청구 폭증 위험 | 초기·중간 단계 Next.js 팀 |
| Cloudflare Pages/Workers | 300+ PoP, 무제한 bandwidth, $5 Pro | DX 약간 낮음, Next.js는 OpenNext 어댑터 의존 | 글로벌·트래픽 큰 사이트 |
| Netlify | DX 양호, 정적 사이트 강함 | 일반 목적 경쟁력 약화 | 정적 마케팅·docs |
| AWS Amplify | 인증·DB·API 통합, SOC 2/HIPAA | AWS 학습곡선 | AWS 생태계·풀스택 |
| Render | Heroku 대체, 풀스택, 백그라운드 워커 | edge 글로벌 네트워크 약함 | 전통적 백엔드+프론트 |
| Fly.io | Docker + 글로벌 edge | 인프라 지식 필요 | low-latency 글로벌 서비스 |
| 자가 호스팅 (Coolify/Dokku/CapRover) | 완전한 통제, 비용 예측 | 운영 부담 | 비용·컴플라이언스 압박 |
| Next.js Standalone (Docker) | Vercel 기능 일부 손실, 100-200MB 이미지 | 직접 구성 필요 | 비상 탈출·자가 호스팅 |
출처: [DigitalOcean 비교](https://www.digitalocean.com/resources/articles/vercel-alternatives), [Qovery](https://www.qovery.com/blog/vercel-alternatives), [DanubeData 2026](https://danubedata.ro/blog/cloudflare-pages-vs-netlify-vs-vercel-static-hosting-2026), [agilesoftlabs Amplify vs Vercel](https://www.agilesoftlabs.com/blog/2026/01/aws-amplify-vs-vercel-2026-complete), [selfhostable.dev](https://selfhostable.dev/blog/coolify-vs-caprover-vs-dokku/), [Next.js Self-Hosting](https://nextjs.org/docs/app/guides/self-hosting).

### 7.2 Cloudflare Pages/Workers
- 글로벌 50ms 미만 TTFB 일관성. ([DanubeData](https://danubedata.ro/blog/cloudflare-pages-vs-netlify-vs-vercel-static-hosting-2026))
- 2026년 Pages에 Docker 컨테이너 지원, OpenNext for Cloudflare 성숙. ([Cloudflare blog](https://blog.cloudflare.com/vinext/))
- 가격: Pro $5(Vercel $20 대비 1/4). bandwidth 무제한.
- 약점: Next.js 풀 기능을 OpenNext 어댑터에 의존, 새 기능은 약간 지연.

### 7.3 Netlify
- DX는 Vercel과 비슷, 정적 사이트에 강함. 일반 목적 경쟁력은 약화. ([DanubeData](https://danubedata.ro/blog/cloudflare-pages-vs-netlify-vs-vercel-static-hosting-2026))
- $104k 청구서 사례로 사용량 기반 PaaS의 구조적 위험 노출. ([HN](https://news.ycombinator.com/item?id=39520776))

### 7.4 AWS Amplify
- 풀스택(인증·DB·API·CI/CD) 통합. 스케일에서 40% 저렴 추정. AWS 지식 필요. ([agilesoftlabs](https://www.agilesoftlabs.com/blog/2026/01/aws-amplify-vs-vercel-2026-complete))
- HIPAA, SOC 2 등 규제 환경에서 강점.

### 7.5 Render
- Heroku의 정신적 후계자. 데이터베이스·백그라운드 워커·크론·persistent disk. Next.js만 보면 Vercel/Cloudflare가 우세. ([DigitalOcean](https://www.digitalocean.com/resources/articles/vercel-alternatives))

### 7.6 Fly.io
- Docker 컨테이너 글로벌 배포. 직접 region 통제. low-latency 게임·실시간 서비스에 적합. 인프라 지식 필요. ([DigitalOcean](https://www.digitalocean.com/resources/articles/vercel-alternatives), [Northflank Fly alts](https://northflank.com/blog/flyio-alternatives))

### 7.7 자가 호스팅 (Coolify · Dokku · CapRover · Dokploy)
- Coolify: 2026 셀프호스트 PaaS의 1순위. Docker Compose 전체 스택 가능. UI 우수. ([selfhostable.dev](https://selfhostable.dev/blog/coolify-vs-caprover-vs-dokku/))
- Dokku: 단일 서버 미니멀, CLI 친화. ($5 VPS도 가능)
- CapRover: 안정적이지만 개발 둔화 추세.
- 비용: VPS $5-20/월로 Vercel Pro 한도 대부분 커버 가능.

### 7.8 Next.js 셀프호스트 (Standalone)
- `output: "standalone"` → 100-200MB Docker 이미지. 정적 자산은 외부 CDN 권장. ([Next.js Self-Hosting Guide](https://nextjs.org/docs/app/guides/self-hosting))
- Image Optimization·ISR·Middleware는 self-host에서 reduced fidelity. OpenNext가 격차 축소. ([OpenNext](https://opennext.js.org/), [eastondev 마이그레이션 가이드](https://eastondev.com/blog/en/posts/dev/20251220-nextjs-docker-self-hosting/))

### 7.9 결정 휴리스틱
- "Next.js의 모든 기능을 즉시 쓰고 싶다 + 시간이 돈이다" → Vercel.
- "트래픽이 글로벌, bandwidth가 큰 비중" → Cloudflare.
- "AWS에 이미 있고 통합 풀스택이 필요" → Amplify.
- "비용 예측 가능성·완전 통제" → 자가 호스팅 + Coolify.
- "비상 탈출 능력은 누구나 갖춰야 한다" → 평소에 standalone 빌드를 익혀두기.

---

## 8. 사례·논쟁

### 8.1 청구서 폭탄 사례
- $20 → $700 → $120 (caching 도입). ([Vercel Bill Shock](https://journeywithibrahim.medium.com/vercel-bill-shock-from-700-to-120-ec24ee9755c3))
- Indie Hackers — Huge Vercel Costs and Rebrand to Feather. ([Indie Hackers](https://www.indiehackers.com/product/mdx-one/huge-vercel-costs-and-rebrand-to-feather--Myc071NF66jYxLB2yED))
- HN Worst Nightmare — DDoS 청구서. ([HN](https://news.ycombinator.com/item?id=39521028))
- LLM 봇 크롤링 + Image API → 청구 폭증. ([HN: Cost of Being Crawled](https://news.ycombinator.com/item?id=43687431))
- 같은 카테고리: Netlify $104k 청구서 사건. ([HN](https://news.ycombinator.com/item?id=39520776), [GeekNews 한국어](https://news.hada.io/topic?id=13554))
- 절감 사례: howdygo 80% 절감. ([howdygo](https://www.howdygo.com/blog/cutting-howdygos-vercel-costs-by-80-without-compromising-ux-or-dx))

### 8.2 Next.js Vendor Lock-in 논쟁
- 관점 A (사실상 종속):
  - "Next.js doesn't support the Build Output API that Vercel created" — eduardoboucas. ([링크](https://eduardoboucas.com/posts/2025-03-25-you-should-know-this-before-choosing-nextjs/))
  - HN 다수, dev.to 자기호스팅 분석.
- 관점 B (덜 종속):
  - Vercel: "70% of Next.js applications run outside of Vercel". ([anti-lock-in 블로그](https://vercel.com/blog/vercel-the-anti-vendor-lock-in-cloud))
  - Walmart.com, Nike.com, Claude.ai 등 self-host 운영 사례.
- 새 흐름:
  - Next.js 16.2 stable Adapter API (Cloudflare·Netlify·Amplify·Google·OpenNext 공동 설계). ([Next.js Across Platforms](https://nextjs.org/blog/nextjs-across-platforms))
  - Cloudflare blog "vibe codes 94%" — AI로 1주만에 Next.js를 Workers에 포팅. ([Cloudflare blog](https://blog.cloudflare.com/vinext/))

### 8.3 보안 사고 — 2026년 4월 Vercel Breach
- 공급망 공격: Context.ai 직원 PC 감염 → OAuth → Vercel 내부. non-sensitive env var 노출 가능성. Sensitive 처리분은 보호됨. ([Vercel KB](https://vercel.com/kb/bulletin/vercel-april-2026-security-incident), [Trend Micro](https://www.trendmicro.com/en_us/research/26/d/vercel-breach-oauth-supply-chain.html), [GitGuardian](https://blog.gitguardian.com/vercel-april-2026-incident-non-sensitive-environment-variables-need-investigation-too/))
- 한국어 정리: GeekNews 다수 thread. ([id=28700](https://news.hada.io/topic?id=28700), [id=28768](https://news.hada.io/topic?id=28768), [id=28699](https://news.hada.io/topic?id=28699))

### 8.4 Edge가 정말 빠른가 (조건부 논쟁)
- Yes 측: TTFB 50ms 미만, 글로벌 사용자 균질.
- 조건부 측: DB가 한 region에 있으면 Edge가 그 region까지 round trip → 오히려 느림. Edge Config·Replication이 없으면 의미 약함.
- 학술 근거: placement-cost-latency triangle. ([Cassel et al. 2025](https://arxiv.org/html/2502.15775v1)), short-request에서는 cloud serverless 우위, 1초+ 처리에서 edge 우위 ([Pinto et al. 2023](https://journalofcloudcomputing.springeropen.com/articles/10.1186/s13677-023-00485-9)).

### 8.5 한국 커뮤니티 신호
- velog: 입문 가이드(배포·환경변수·라우팅 트러블슈팅) 압도적. 비용·보안 심층 토론은 빈약. ([대표 입문 글](https://velog.io/@lovelys0731/Vercel%EB%A1%9C-React-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%EB%A5%BC-%EB%B0%B0%ED%8F%AC%ED%95%B4-%EB%B3%B4%EC%9E%90-1-Vercel-%EB%B0%B0%ED%8F%AC-%EA%B8%B0%EB%B3%B8))
- OKKY: Vercel 비용 폭탄 직접 thread는 발견 못 함.
- GeekNews: 영어권 토론을 한국어로 빠르게 전달. 보안사고·AI SDK·Edge Functions GA 등 주요 뉴스의 한국어 진입점. ([Edge Functions GA](https://news.hada.io/topic?id=8052), [AI SDK 공개](https://news.hada.io/topic?id=9430), [Grep 인수](https://news.hada.io/topic?id=17884), [React Best Practices repo](https://news.hada.io/topic?id=25869))

### 8.6 학술 맥락 (책의 깊이를 더하는 백그라운드)
- Cold start systematic review — 100여 편 메타분석. ([Mahmoudi et al. 2024](https://dl.acm.org/doi/abs/10.1145/3700875))
- Serverless edge taxonomy. ([Cassel et al. 2025](https://arxiv.org/html/2502.15775v1))
- Edge-cloud dynamic placement. ([Aslanpour et al. 2020](https://arxiv.org/pdf/2003.01310))
- Latency·resource analysis. ([Pinto et al. 2023](https://journalofcloudcomputing.springeropen.com/articles/10.1186/s13677-023-00485-9))
- Green vs Fast (cold start vs idle carbon). ([arXiv 2602.23935](https://arxiv.org/abs/2602.23935))
- Firecracker microVM (NSDI '20) — Lambda·Fargate 기반 인프라. (Agache et al. 2020)
- RFC 5861 — stale-while-revalidate, ISR/PPR의 뿌리. ([RFC](https://datatracker.ietf.org/doc/html/rfc5861))

---

## 9. 참고문헌 (URL 모음)

### 공식 문서·공지
- https://vercel.com/pricing
- https://vercel.com/docs/plans/hobby
- https://vercel.com/docs/fluid-compute
- https://vercel.com/blog/introducing-fluid-compute
- https://vercel.com/docs/functions
- https://vercel.com/docs/functions/limitations
- https://vercel.com/docs/limits
- https://vercel.com/docs/functions/configuring-functions/duration
- https://vercel.com/docs/incremental-static-regeneration
- https://nextjs.org/docs/app/guides/ppr-platform-guide
- https://nextjs.org/docs/app/guides/incremental-static-regeneration
- https://nextjs.org/docs/app/guides/self-hosting
- https://nextjs.org/blog/nextjs-across-platforms
- https://vercel.com/docs/frameworks
- https://vercel.com/docs/storage
- https://vercel.com/blog/vercel-storage
- https://github.com/vercel/storage/tree/main/packages/edge-config
- https://vercel.com/docs/cron-jobs
- https://vercel.com/docs/cron-jobs/usage-and-pricing
- https://vercel.com/docs/image-optimization
- https://vercel.com/docs/image-optimization/limits-and-pricing
- https://vercel.com/docs/image-optimization/managing-image-optimization-costs
- https://vercel.com/security/web-application-firewall
- https://vercel.com/docs/vercel-firewall
- https://vercel.com/docs/vercel-firewall/attack-challenge-mode
- https://vercel.com/docs/vercel-firewall/ddos-mitigation
- https://vercel.com/docs/vercel-firewall/vercel-waf
- https://vercel.com/docs/environment-variables
- https://vercel.com/docs/environment-variables/sensitive-environment-variables
- https://vercel.com/docs/deployments/environments
- https://vercel.com/docs/deployment-protection
- https://vercel.com/docs/security
- https://vercel.com/docs/security/compliance
- https://vercel.com/blog/vercel-supports-hipaa-compliance
- https://vercel.com/kb/guide/is-vercel-soc-2-compliant
- https://vercel.com/kb/bulletin/vercel-april-2026-security-incident
- https://vercel.com/blog/automatic-ssl-with-vercel-lets-encrypt
- https://vercel.com/docs/domains/working-with-domains
- https://vercel.com/docs/domains/working-with-ssl
- https://vercel.com/docs/pricing/manage-and-optimize-usage
- https://vercel.com/solutions/turborepo
- https://vercel.com/academy/production-monorepos
- https://vercel.com/academy/production-monorepos/github-actions
- https://turborepo.dev/docs/guides/ci-vendors/github-actions
- https://vercel.com/docs/ai-gateway/capabilities
- https://vercel.com/docs/ai-gateway/capabilities/image-generation/ai-sdk
- https://vercel.com/templates/edge-middleware
- https://vercel.com/blog/vercel-the-anti-vendor-lock-in-cloud
- https://vercel.com/blog/introducing-the-vercel-waf

### 산업 분석·블로그
- https://schematichq.com/blog/vercel-pricing
- https://flexprice.io/blog/vercel-pricing-breakdown
- https://kuberns.com/blogs/vercel-pricing/
- https://temps.sh/blog/vercel-pricing-complete-guide-2026
- https://journeywithibrahim.medium.com/vercel-bill-shock-from-700-to-120-ec24ee9755c3
- https://www.howdygo.com/blog/cutting-howdygos-vercel-costs-by-80-without-compromising-ux-or-dx
- https://eduardoboucas.com/posts/2025-03-25-you-should-know-this-before-choosing-nextjs/
- https://richardkovacs.dev/blog/bring-your-own-nextjs
- https://dev.to/rbobr/self-hosting-nextjs-what-you-gain-and-lose-vs-vercel-4g8c
- https://eastondev.com/blog/en/posts/dev/20251220-nextjs-docker-self-hosting/
- https://opennext.js.org/
- https://blog.cloudflare.com/vinext/
- https://danubedata.ro/blog/cloudflare-pages-vs-netlify-vs-vercel-static-hosting-2026
- https://www.codebrand.us/blog/vercel-vs-netlify-vs-cloudflare-2026/
- https://niobond.com/vercel-vs-netlify-vs-cloudflare/
- https://www.digitalocean.com/resources/articles/vercel-alternatives
- https://www.qovery.com/blog/vercel-alternatives
- https://www.agilesoftlabs.com/blog/2026/01/aws-amplify-vs-vercel-2026-complete
- https://selfhostable.dev/blog/coolify-vs-caprover-vs-dokku/
- https://lumadock.com/tutorials/coolify-alternatives
- https://northflank.com/blog/best-vercel-alternatives-for-scalable-deployments
- https://northflank.com/blog/flyio-alternatives
- https://www.thisdot.co/blog/vercel-botid-the-invisible-bot-protection-you-needed
- https://www.shipsafer.ai/blog/vercel-deployment-security
- https://aishipsafe.com/blog/are-vercel-environment-variables-secure
- https://blog.gitguardian.com/vercel-april-2026-incident-non-sensitive-environment-variables-need-investigation-too/
- https://www.trendmicro.com/en_us/research/26/d/vercel-breach-oauth-supply-chain.html
- https://www.truefoundry.com/blog/understanding-vercel-ai-gateway-pricing
- https://www.pkgpulse.com/blog/ssr-vs-ssg-vs-isr-vs-ppr-rendering-2026

### 커뮤니티
- https://news.ycombinator.com/item?id=39898391
- https://news.ycombinator.com/item?id=41031912
- https://news.ycombinator.com/item?id=39521028
- https://news.ycombinator.com/item?id=39520776
- https://news.ycombinator.com/item?id=43687431
- https://news.ycombinator.com/item?id=40627998
- https://news.ycombinator.com/item?id=47967508
- https://news.ycombinator.com/item?id=39932906
- https://news.ycombinator.com/item?id=29691934
- https://github.com/vercel/next.js/discussions/41485
- https://github.com/vercel/next.js/discussions/81448
- https://github.com/vercel/vercel/discussions/4502
- https://github.com/vercel/examples/tree/main/edge-middleware/bot-protection-botd
- https://www.indiehackers.com/product/mdx-one/huge-vercel-costs-and-rebrand-to-feather--Myc071NF66jYxLB2yED
- https://news.hada.io/topic?id=28700
- https://news.hada.io/topic?id=28768
- https://news.hada.io/topic?id=28699
- https://news.hada.io/topic?id=13554
- https://news.hada.io/topic?id=8052
- https://news.hada.io/topic?id=9430
- https://news.hada.io/topic?id=17884
- https://news.hada.io/topic?id=25869
- https://velog.io/@lovelys0731/Vercel%EB%A1%9C-React-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%EB%A5%BC-%EB%B0%B0%ED%8F%AC%ED%95%B4-%EB%B3%B4%EC%9E%90-1-Vercel-%EB%B0%B0%ED%8F%AC-%EA%B8%B0%EB%B3%B8
- https://velog.io/@hoeun0723

### 학술
- https://arxiv.org/abs/2310.08437 (Cold Start Systematic Review)
- https://dl.acm.org/doi/abs/10.1145/3700875 (ACM Computing Surveys 게재본)
- https://arxiv.org/html/2502.15775v1 (Serverless Edge Taxonomy)
- https://arxiv.org/pdf/2003.01310 (Edge-Cloud Placement)
- https://journalofcloudcomputing.springeropen.com/articles/10.1186/s13677-023-00485-9 (Edge Analytics)
- https://arxiv.org/abs/2602.23935 (Green or Fast)
- https://datatracker.ietf.org/doc/html/rfc5861 (stale-while-revalidate)

---

## 10. 리서치 한계

- 한국어 1차 자료의 비용·보안 심층 토론은 빈약. velog/OKKY는 입문 가이드 위주, 비용 폭탄·보안 사고는 GeekNews를 통한 영어권 인용이 대부분. 책에서 "한국 동네 사례"가 필요하다면 코딩애플 GAE 15만원 사례처럼 인접 사례를 곁들이는 구성이 현실적.
- Vercel 자체를 분석한 peer-reviewed 학술 논문은 거의 없다. 인접 분야(cold start, edge serverless, FaaS placement) 논문을 매핑해 이론 백본으로 사용했다.
- PPR/ISR의 정량 성능 비교 학술 논문은 부재. 책은 Vercel/Cloudflare 자체 벤치마크를 인용하되 "공급자 자체 데이터"임을 명시 권장.
- AI Gateway 가격 마진율은 공식 자료에 없고 제3자 분석에 의존. 인용 시 "추정"임을 표기.
- Vercel KV/Postgres sunset의 정확한 마이그레이션 마감일은 마켓플레이스 안내문에 단편적으로만 노출. 책 출판 직전 한 번 더 확인 필요.
- Discord 공개 로그·KakaoTalk 오픈채팅·X/Threads 일차 트윗은 검색 도구 한계로 미수집. 한국 개발자 일차 목소리 추가 발굴 시 보강 가능.
- AI Gateway·Fluid compute·PPR은 2025-2026에 빠르게 변화 중. 가격·기본값·기능 가용성은 책 출판 시점에 한 번 더 검증해야 한다.
