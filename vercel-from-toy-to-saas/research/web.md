# 웹 리서치: Vercel 입문서

수집 시점: 2026-05-06. 기준 시점이 명시되지 않은 가격·한도는 모두 2026년 봄 기준이며, 변동 가능성이 크다는 전제를 책 본문에 명시할 것.

## 자료 1: Fluid compute (공식 문서)
- 출처: https://vercel.com/docs/fluid-compute
- 핵심 주장: Fluid compute는 단일 함수 인스턴스가 다중 요청을 동시에 처리하는 새로운 실행 모델이다. 2025년 초부터 모든 신규 배포의 기본값.
- 인용: "Optimized concurrency: handle multiple invocations within a single function instance" / "Reduce compute costs by up to 85%"
- 관련 섹션: 1. 개념 / 4. 비용 / 6. 함정

## 자료 2: Introducing Fluid compute — Vercel 공식 블로그
- 출처: https://vercel.com/blog/introducing-fluid-compute
- 저자·날짜: Vercel, 2025
- 핵심 주장: AI 워크로드처럼 I/O 대기가 긴 함수에서 idle 자원을 회수해 cost-efficiency를 확보. CPU 시간 ms 단위로만 과금.
- 인용: "You are only billed during actual code execution and not during I/O operations"
- 관련 섹션: 1. 개념 / 4. 비용

## 자료 3: Vercel Functions Limits (공식)
- 출처: https://vercel.com/docs/functions/limitations
- 핵심 주장: Edge runtime은 filesystem 접근·`require()` 직접 호출·대부분 Node API를 지원하지 않음. Edge functions는 25초 이내 응답 시작·최대 300초 스트리밍.
- 관련 섹션: 1. 개념(런타임 차이) / 7. 함정

## 자료 4: Vercel Pricing 공식 페이지
- 출처: https://vercel.com/pricing
- 핵심 주장 (2026-05 기준):
  - Hobby: 무료, 비상업적 개인 용도. Fast Data Transfer 100GB, 함수 invocations 1M, Active CPU 4시간, Provisioned Memory 360 GB-hrs/월.
  - Pro: $20/seat/월, 1TB bandwidth, 10M edge requests, ~1,000 GB-hours 함수 메모리, 초과시 GB당 $0.15.
  - Enterprise: 커스텀 가격, 99.99% SLA, SCIM·Audit Log·Secure Compute.
  - 함수 과금 3축: invocations $0.60/M + CPU-hour $0.128 + memory $0.0106/GB-hour.
- 관련 섹션: 4. 비용

## 자료 5: Schematic — Vercel Pricing Plans and Hidden Costs (2026)
- 출처: https://schematichq.com/blog/vercel-pricing
- 핵심 주장: Vercel 청구서가 폭증하는 4대 원인 — image optimization, bandwidth overage, edge requests, 다수의 seat. 공식 페이지에 잘 안 보이는 add-on (Speed Insights $10/proj, Web Analytics $10/proj 25K events) 존재.
- 관련 섹션: 4. 비용 / 7. 함정

## 자료 6: Vercel Bill Shock — Medium (Ibrahim Ahmed)
- 출처: https://journeywithibrahim.medium.com/vercel-bill-shock-from-700-to-120-ec24ee9755c3
- 저자·날짜: Ibrahim Ahmed, 2026-01
- 핵심 주장: 한 클라이언트의 월청구서가 $20→$700 폭증. 원인: Next.js Image, 큰 JSON API 응답, ISR·SSR fetch가 모두 bandwidth로 청구. aggressive caching 도입 후 $120(83% 감소).
- 인용 가능한 구절: "no aggressive caching meant repeated fetches"
- 관련 섹션: 4. 비용 / 5. 보안·운영 / 7. 함정 / 8. 사례

## 자료 7: Cutting Vercel Costs by 80% — howdygo.com
- 출처: https://www.howdygo.com/blog/cutting-howdygos-vercel-costs-by-80-without-compromising-ux-or-dx
- 핵심 주장: caching 전략·이미지 외부 CDN 위탁·ISR 재검증 주기 조정 등으로 80% 절감. DX·UX 손상 없음.
- 관련 섹션: 4. 비용 / 5. 운영

## 자료 8: DDoS Mitigation 공식 문서
- 출처: https://vercel.com/docs/vercel-firewall/ddos-mitigation
- 핵심 주장: Firewall이 차단한 트래픽은 청구되지 않음. 단, "automatic mitigation 발동 전" 처리된 요청은 청구됨. Attack Challenge Mode는 모든 플랜에서 무료.
- 관련 섹션: 5. 보안 / 4. 비용

## 자료 9: Attack Challenge Mode 공식 문서
- 출처: https://vercel.com/docs/vercel-firewall/attack-challenge-mode
- 핵심 주장: 챌린지로 차단된 요청은 사용량 미차감. 검색엔진·웹훅 화이트리스트 자동 적용. 장기 활성화해도 SEO 영향 없음.
- 관련 섹션: 5. 보안

## 자료 10: Web Application Firewall — Vercel 공식
- 출처: https://vercel.com/security/web-application-firewall
- 핵심 주장: Bot Protection Managed Ruleset, AI Bots Managed Ruleset, BotID, Custom WAF Rules. Pro 플랜 이상 일부 기능 유료.
- 관련 섹션: 3. 활용 기능 / 5. 보안

## 자료 11: Vercel April 2026 security incident — KB
- 출처: https://vercel.com/kb/bulletin/vercel-april-2026-security-incident
- 핵심 주장: Context.ai (Vercel 직원이 사용한 third-party AI tool)의 Lumma Stealer 감염 → Google Workspace OAuth → Vercel 직원 계정 → 내부 시스템 → non-sensitive 환경 변수 enumerate·decrypt. Sensitive 처리된 변수는 무사.
- 관련 섹션: 5. 보안 / 8. 사례·논쟁

## 자료 12: Trend Micro 분석 — Vercel Breach OAuth
- 출처: https://www.trendmicro.com/en_us/research/26/d/vercel-breach-oauth-supply-chain.html
- 핵심 주장: 공급망 공격 패턴, OAuth 토큰 위협 모델. Sensitive 라벨이 차이를 만든 결정적 요인.
- 관련 섹션: 5. 보안

## 자료 13: GitGuardian — Non-Sensitive Env Vars Need Investigation Too
- 출처: https://blog.gitguardian.com/vercel-april-2026-incident-non-sensitive-environment-variables-need-investigation-too/
- 핵심 주장: Sensitive로 표시되지 않은 변수도 자주 비밀을 담는다 (DB URL, API key, signing key). 모두 회전 권고.
- 관련 섹션: 5. 보안

## 자료 14: ShipSafer — Vercel Deployment Security
- 출처: https://www.shipsafer.ai/blog/vercel-deployment-security
- 핵심 주장: Preview에 production 시크릿을 재사용하면 모든 PR Preview가 production 폭발 반경. Sensitive flag, 환경별 분리, 회전 후 재배포 필수.
- 인용: "A rotating Vercel environment variable does not retroactively invalidate old deployments"
- 관련 섹션: 5. 보안 / 7. 함정

## 자료 15: Sensitive environment variables — 공식 문서
- 출처: https://vercel.com/docs/environment-variables/sensitive-environment-variables
- 핵심 주장: Sensitive 플래그가 켜진 변수는 dashboard·API에서 다시 읽을 수 없게 저장. 일반 변수는 decrypt 가능 형태로 보관.
- 관련 섹션: 5. 보안

## 자료 16: Deployment Protection 공식 문서
- 출처: https://vercel.com/docs/deployment-protection
- 핵심 주장: Preview/Production URL 접근 통제. SSO, Password, OPTIONS Allowlist 등 옵션. 무료 플랜은 제한.
- 관련 섹션: 5. 보안

## 자료 17: Vercel Storage overview & 마켓플레이스 변화
- 출처: https://vercel.com/docs/storage / https://vercel.com/blog/vercel-storage
- 핵심 주장: Vercel KV·Postgres가 sunset, Marketplace Storage로 대체 (Neon, Upstash 등 통합 빌링). Blob, Edge Config는 자체 운영. Edge Config는 1ms 미만 read p50.
- 관련 섹션: 3. 활용 기능

## 자료 18: Edge Config 공식
- 출처: https://github.com/vercel/storage/tree/main/packages/edge-config
- 핵심 주장: 글로벌 read-mostly 데이터 (피처 플래그·리다이렉트 룰·차단 IP). 99% read 10ms 이하.
- 관련 섹션: 3. 활용 기능

## 자료 19: Cron Jobs — 공식
- 출처: https://vercel.com/docs/cron-jobs , https://vercel.com/docs/cron-jobs/usage-and-pricing
- 핵심 주장: 모든 플랜 포함. Hobby는 일 1회 제한. 실행은 함수 quota에 차감.
- 관련 섹션: 3. 활용 기능 / 4. 비용

## 자료 20: Image Optimization 가격
- 출처: https://vercel.com/docs/image-optimization/limits-and-pricing
- 핵심 주장: 28,000 이미지 사례에서 월 $115 추가 — 기본 $20 구독 대비 7배. LLM 봇 크롤링 시 폭증.
- 관련 섹션: 4. 비용 / 7. 함정

## 자료 21: The Cost of Being Crawled — Hacker News
- 출처: https://news.ycombinator.com/item?id=43687431
- 핵심 주장: LLM 봇이 image API를 마구 호출 → 청구 폭증. robots.txt만으로 부족, WAF 차단 필요.
- 관련 섹션: 5. 보안 / 4. 비용

## 자료 22: Cloudflare Pages vs Netlify vs Vercel (2026) — DanubeData
- 출처: https://danubedata.ro/blog/cloudflare-pages-vs-netlify-vs-vercel-static-hosting-2026
- 핵심 주장: Cloudflare 300+ PoP, 글로벌 50ms 미만 TTFB. Vercel 2025 대비 비미국권 성능 개선. Cloudflare Pro $5 vs Vercel Pro $20.
- 관련 섹션: 7. 대안 비교

## 자료 23: Vercel: The anti-vendor-lock-in cloud — Vercel 블로그
- 출처: https://vercel.com/blog/vercel-the-anti-vendor-lock-in-cloud
- 핵심 주장: Vercel 측 반박. Next.js의 ~70%는 Vercel 외부에서 운영. Walmart, Nike, Claude.ai 사례.
- 관련 섹션: 8. 사례·논쟁

## 자료 24: Next.js Across Platforms: Adapters, OpenNext, and Our Commitments
- 출처: https://nextjs.org/blog/nextjs-across-platforms
- 핵심 주장: Next.js 16.2의 stable Adapter API. OpenNext·Netlify·Cloudflare·Amplify·Google과 공동 설계. 라우트·정적 자산·캐싱 룰·런타임 타깃의 typed/versioned description.
- 관련 섹션: 8. 사례·논쟁 / 7. 대안 비교

## 자료 25: OpenNext
- 출처: https://opennext.js.org/
- 핵심 주장: 2023년 AWS Lambda 어댑터로 시작한 오픈 프로젝트. 현재 Cloudflare/Netlify와 함께 Deployment Adapters Working Group 운영.
- 관련 섹션: 7. 대안 비교

## 자료 26: Self-Hosting Next.js: What You Gain (and Lose) — dev.to
- 출처: https://dev.to/rbobr/self-hosting-nextjs-what-you-gain-and-lose-vs-vercel-4g8c
- 핵심 주장: Image Optimization·Middleware·ISR·PPR이 self-host에서 best 또는 only로 작동. 셀프호스트 시 별도 인프라 구성 필요.
- 관련 섹션: 7. 대안 비교 / 8. 논쟁

## 자료 27: Next.js Self-Hosting Guide 공식
- 출처: https://nextjs.org/docs/app/guides/self-hosting
- 핵심 주장: `output: "standalone"` 모드로 ~100-200MB Docker 이미지. 정적 자산은 CDN 권장.
- 관련 섹션: 7. 대안 비교

## 자료 28: Escape from Vercel — eastondev.com (2025-12)
- 출처: https://eastondev.com/blog/en/posts/dev/20251220-nextjs-docker-self-hosting/
- 핵심 주장: Vercel→Docker 셀프호스트 마이그레이션 실전 가이드. 다단계 Dockerfile, Nginx, GitHub Actions 자동화.
- 관련 섹션: 7. 대안 비교 / 3. 성장 단계

## 자료 29: PPR Platform Guide & ISR 공식
- 출처: https://nextjs.org/docs/app/guides/ppr-platform-guide / https://vercel.com/docs/incremental-static-regeneration
- 핵심 주장: PPR은 Next.js 15 stable, 16에서 cacheComponents flag 기본. Static shell + dynamic Suspense holes를 단일 응답에 통합.
- 관련 섹션: 1. 개념

## 자료 30: SSR vs SSG vs ISR vs PPR (2026)
- 출처: https://www.pkgpulse.com/blog/ssr-vs-ssg-vs-isr-vs-ppr-rendering-2026
- 핵심 주장: 렌더링 전략 비교. PPR은 sub-50ms TTFB + 부분 동적성을 동시 달성하는 첫 모델.
- 관련 섹션: 1. 개념

## 자료 31: Spend Management 공식
- 출처: https://vercel.com/docs/pricing/manage-and-optimize-usage
- 핵심 주장: Pro 팀은 임계값 알림·자동 일시정지·웹훅 트리거 가능.
- 관련 섹션: 4. 비용 / 5. 운영

## 자료 32: Vercel Compliance — 공식
- 출처: https://vercel.com/docs/security/compliance / https://vercel.com/blog/vercel-supports-hipaa-compliance
- 핵심 주장: SOC 2 Type 2, ISO/IEC 27001, PCI DSS, HIPAA, GDPR, EU-US DPF, ISO 27018, NIS 2, DORA. HIPAA는 Enterprise 한정 + Secure Compute.
- 관련 섹션: 5. 보안

## 자료 33: AI SDK Image Generation 공식
- 출처: https://vercel.com/docs/ai-gateway/capabilities/image-generation/ai-sdk
- 핵심 주장: AI Gateway가 OpenAI/Google/Black Forest Labs/Recraft 등 다수 모델을 단일 API로 라우팅. 인증·응답 포맷 자동.
- 관련 섹션: 3. 활용 기능

## 자료 34: AI Gateway Pricing (TrueFoundry)
- 출처: https://www.truefoundry.com/blog/understanding-vercel-ai-gateway-pricing
- 핵심 주장: 토큰 기반 모델 사용료 + Vercel 마진. 비용 구조 투명도가 낮다는 비판.
- 관련 섹션: 3. 활용 기능 / 4. 비용

## 자료 35: Edge Middleware Templates
- 출처: https://vercel.com/templates/edge-middleware
- 핵심 주장: Basic Auth·Bot Protection (Botd, DataDome)·A/B testing·feature flag rollout 등 표준 패턴 다수.
- 관련 섹션: 3. 활용 기능 / 5. 보안

## 자료 36: Vercel BotID — This Dot Labs
- 출처: https://www.thisdot.co/blog/vercel-botid-the-invisible-bot-protection-you-needed
- 핵심 주장: BotID는 클라이언트 fingerprint를 활용한 invisible bot detection. Middleware에 metadata 주입, rate limit·fraud detection에 활용.
- 관련 섹션: 3. 활용 기능 / 5. 보안

## 자료 37: Frameworks on Vercel (공식)
- 출처: https://vercel.com/docs/frameworks
- 핵심 주장: 35+ 프레임워크 first-class 지원 (Next.js, SvelteKit, Astro, Nuxt, Remix, Angular 등). 빌드·라우팅·이미지 최적화·env 표준화된 추상화.
- 관련 섹션: 1. 개념 / 2. 사용

## 자료 38: Custom Domains & SSL 공식
- 출처: https://vercel.com/docs/domains/working-with-domains , https://vercel.com/blog/automatic-ssl-with-vercel-lets-encrypt
- 핵심 주장: Let's Encrypt 와일드카드 자동 발급·갱신. 만료 14-30일 전 자동 갱신. 도메인은 자체 구매 시 자동 갱신, 외부 등록은 수동.
- 관련 섹션: 2. 사용

## 자료 39: Vercel CLI 공식 / Turborepo 가이드
- 출처: https://vercel.com/academy/production-monorepos , https://turborepo.dev/docs/guides/ci-vendors/github-actions
- 핵심 주장: `vercel deploy --prebuilt --token`으로 GitHub Actions 통합. Turborepo Remote Cache(`TURBO_TEAM`+토큰)로 모노레포 빌드 가속.
- 관련 섹션: 2. 사용

## 자료 40: Top 10 Vercel Alternatives — DigitalOcean
- 출처: https://www.digitalocean.com/resources/articles/vercel-alternatives
- 핵심 주장: AWS Amplify, Render, Fly.io, Cloudflare Pages, Netlify, Coolify, Railway, DigitalOcean App Platform, Sliplane, Northflank 등 비교.
- 관련 섹션: 7. 대안 비교

## 자료 41: Coolify vs CapRover vs Dokku — selfhostable.dev
- 출처: https://selfhostable.dev/blog/coolify-vs-caprover-vs-dokku/
- 핵심 주장: Coolify가 2026 셀프호스트 PaaS의 1순위. Docker Compose 전체 스택 배포 가능. Dokku는 minimalist 단일 서버, CapRover는 안정적이지만 개발 둔화.
- 관련 섹션: 7. 대안 비교

## 자료 42: AWS Amplify vs Vercel (agilesoftlabs)
- 출처: https://www.agilesoftlabs.com/blog/2026/01/aws-amplify-vs-vercel-2026-complete
- 핵심 주장: 스케일에서 Amplify 40% 저렴, 단 AWS 학습곡선. 인증·DB·API 통합 시 Amplify 유리. Vercel은 Next.js 중심 팀 우세.
- 관련 섹션: 7. 대안 비교

## 자료 43: 5 Vercel Alternatives — Qovery
- 출처: https://www.qovery.com/blog/vercel-alternatives
- 핵심 주장: cost·lock-in·frontend-only constraints가 이탈 동기. Vercel은 백엔드·DB·long-running 워크로드에 약하다는 시장 평가.
- 관련 섹션: 7. 대안 비교 / 8. 논쟁

## 자료 44: vercel/turborepo on Vercel (공식)
- 출처: https://vercel.com/solutions/turborepo
- 핵심 주장: Turborepo 자체가 Vercel 자산. Remote Cache·incremental build·affected workspace deploy.
- 관련 섹션: 2. 사용

## 자료 45: Limits — Vercel 공식
- 출처: https://vercel.com/docs/limits
- 핵심 주장: 함수 페이로드 4.5MB 응답·deployment build duration 45분(기본)·max function duration 800초(Pro fluid)·request body 4.5MB 등 한도 표.
- 관련 섹션: 7. 함정

## 수집 한계
- 한국어 일차 자료(velog, OKKY 등)에서 "비용 폭탄" 직접 사례 글은 찾지 못함. 대부분 입문 가이드와 환경변수·라우팅 트러블슈팅. 한국 커뮤니티의 비용 토론은 영어권 사례를 인용·번역하는 형태가 많음.
- Vercel KV/Postgres sunset의 정확한 일정은 마켓플레이스 안내문에 단편적으로만 노출. 마이그레이션 마감일 등은 공식 deprecation 문서 추가 확인 필요.
- AI Gateway 가격 구조의 마진율은 공식 자료에 없음 (제3자 분석에 의존).
