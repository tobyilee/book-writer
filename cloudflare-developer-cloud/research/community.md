# 커뮤니티 리서치: Cloudflare를 내 앱·서비스의 클라우드로 쓰기

- 대상 독자: Java·Kotlin·JS/TS·React·Next.js·Node.js 경험 개발자
- genre: tech-book · 슬러그: `cloudflare-developer-cloud`
- 검색 시점: 2026-10-03 (모든 항목 공통 — 항목별로 "검색 시점 2026-10-03"을 반복 표기)
- 수집 범위: 2025-01 ~ 2026-10 우선. 그보다 오래된 글은 날짜와 "현재도 유효한가"를 함께 적었다.
- **라벨 규칙:** 이 문서의 모든 주장은 "커뮤니티 의견, 검증 필요"다. 문서화된 동작(공식 문서·체인지로그)은 `[문서화]`, 일화는 `[일화]`, 이해관계자 발언(Cloudflare 직원·경쟁사 창업자)은 `[이해관계자: 역할]`로 구분한다.
- Reddit은 직접 접근이 차단되어 미러(reddit.sentinel-team.org 스냅샷)나 2차 인용을 경유했다. 인용은 정식 `reddit.com` URL로 적고 "미러 스냅샷 경유"를 표시했다.
- HN 날짜·점수는 Algolia HN API(`hn.algolia.com/api/v1/items/{id}`)로 확인했다.

---

## 반복되는 고통·질문 (챕터 오프닝 소재)

### 패턴 1: "유료 플랜으로 올리는 순간 한도 없는 리스크를 진다" — 계정 단위 하드 지출 상한 부재와 요금 폭탄

빈도·강도 모두 1위. 2022년부터 2026년 9월까지 같은 불만이 끊기지 않는다. 금액 규모는 $48 → $4,868 → $34,895로 커졌다.

- **출현 예시:**
  - HN (thewillmoss, 2026-04-16, 31점) — https://news.ycombinator.com/item?id=47787042 · 검색 시점 2026-10-03 · `[일화]`
    > "My DO agent's onStart() handler called this.ctx.storage.setAlarm() on every wake-up without checking whether an alarm was already scheduled. Combined with 60+ preview Worker deployments each creating independent DO instances, this created a runaway self-health-check loop."
    > "April 4-5: peaked at ~930 billion row reads/day … April 15: $34,895 invoice due with no billing response yet"
    > "Cloudflare's Workers Usage Notifications only monitors CPU time. Not Durable Object row reads or writes. There is also no hard spending cap for DO operations available in the dashboard or Wrangler config. Nothing would have fired an alert during this runaway. I found out when the bill showed up."
    > "I'm a pre-launch sole proprietor who put all my personal savings into this startup. This bill would financially destroy me for usage that generated zero business value."
    - 결말(환불 여부)은 확인하지 못했다. 원문은 Agents Week 마케팅 시기에 이 공백이 방치됐다고 비판한다.
    - 댓글 jacobmei (2026-04-27): "CPU-time monitoring is a relic from before Workers grew DO/KV/D1 with their own metered ops, and per-binding spend caps would have caught this." https://news.ycombinator.com/item?id=47917107
  - 블로그 + Reddit (Nathan Schram, Little Bear Apps, 게시 2026-03-18 / 사건 2026-01) — https://littlebearapps.com/blog/d1-billing-disaster-circuit-breakers/ · 검색 시점 2026-10-03 · `[일화]`
    - D1 쓰기 48.3억 건. 원인은 버그 두 개(중복 제거 누락, `ON CONFLICT` 누락). $5/월 계정에 $4,868 청구, 하루 최대 $1,411.40.
    > "I don't have a billing department. I have a credit card and a vague hope that nothing goes catastrophically wrong."
    - 같은 사람의 r/CloudFlare 글(2026-02-18): "Support said my $4.8k billing dispute was on hold, but the automated system just suspended me anyway." — https://www.reddit.com/r/CloudFlare/comments/1r7skeq/ (원문 미열람, 블로그 인용 경유)
    - 결말: 18일 만에 $4,586.64 면제, 계정 복구. 이후 70%/90%/100% 단계별 자동 차단 서킷 브레이커를 직접 만들었다.
  - HN (woodylondon, 2026-04-16) — https://news.ycombinator.com/item?id=47795924 · 검색 시점 2026-10-03 · `[일화]`
    > "I would pay for Cloudflare Workers Paid ($5) in a heartbeat … The problem is that once you're on the paid plan, you're exposed to unlimited risk if your worker goes crazy due to a stupid code bug or if you're hacked. As a solo dev, it's a risk I simply cannot take; I could wake to a bankruptcy bill from Cloudflare."
    > "I am using Supabase at the moment, and see they have a hard cap now. and so does Vercel …"
  - HN (simonw, 2026-06-20, "Temporary Cloudflare accounts for AI agents" 249점 스레드) — https://news.ycombinator.com/item?id=48611258 · 검색 시점 2026-10-03
    > "Cloudflare still haven't shipped the most valuable possible feature for Cloudflare Workers though: hard billing caps. I want to set a cap of $100/month and know, for sure, that if something untoward happens my apps will all stop serving traffic rather than me getting hit with a bill for $1000s. The safest way to use Workers is on the free tier, which will shut off after 100,000 requests/day"
  - HN (mathoff, 2026-08-03, Billable Usage API 발표 스레드) — https://news.ycombinator.com/item?id=49158930 · 검색 시점 2026-10-03
    > "Translated: Close, but still not hard cost cap at Cloudflare."
  - HN Show HN "A usage circuit breaker for Cloudflare Workers" (ethan_zhao, 2026-03-10, 29점) — https://news.ycombinator.com/item?id=47322794 · 검색 시점 2026-10-03
    - 3mins.news 운영자. cron 트리거 10개 이상이 몇 분마다 도는 구조라 직접 사용량 차단기를 만들었다. 댓글 photobombastic: "Prevention over detection. Could be cool to set per-worker limits in addition to the global ones."
  - 블로그 helloacm (2022-08-25, **오래됨 — 지금도 유효**) — https://helloacm.com/cloudflare-unexpected-high-usage-of-api-requests-how-to-avoid-surprising-billing/ · 검색 시점 2026-10-03
    - 무료로 공개한 API가 한 달에 1억 634만 요청을 받아 $48가 청구됐다. 대응은 Bearer 인증, 레이트 리밋, 봇 차단, 결제 알림, 공개 API를 Free 플랜으로 내리기(하루 10만 요청에서 멈추고 과금되지 않음).
  - 한국: 다모앙 개발 게시판 (띠부씰, 2025-12-13) 댓글 — https://damoang.net/development/2488 · 검색 시점 2026-10-03 · `[일화]`
    - 사이트 관리자(SDK)가 Cloudflare 로깅을 실수로 켰다가 하루 50만 원 이상이 청구됐다는 경험을 댓글로 남겼다(요약 경유, 원문 문장 재확인 필요).

- **커뮤니티가 공유하는 진단:**
  1. 무료 플랜은 하루 한도에서 멈추는 사실상의 하드 캡이다. 유료로 올리면 그 브레이크가 사라진다(simonw, helloacm).
  2. 사용량 알림이 오랫동안 CPU time만 감시했고 DO·D1·KV 같은 저장소 연산은 감시하지 않았다(thewillmoss, jacobmei).
  3. 루프를 만드는 것은 대개 자기 코드다. alarm 재등록, 프리뷰 배포마다 생기는 DO 인스턴스, `ON CONFLICT` 누락, cron 남발.

- **나중 제품 변경과의 관계 — "알림"과 "상한"을 구분할 것 (fact-checker 대조 필요):**
  - `[문서화]` Budget alerts 기본 활성화: 대상 Pay-as-you-go 계정에 계정 단위 $10 임계값을 기본으로 켰다. 체인지로그 원문은 "It does not cap your usage or impact your account in any way."라고 적고 있고, 사용량을 하루 한 번 처리하므로 알림이 하루 늦게 온다. https://developers.cloudflare.com/changelog/post/2026-06-15-budget-alerts-default-on/ · 검색 시점 2026-10-03
    - (fact-checker 대조 필요) URL 슬러그는 2026-06-15, 본문은 "2026-07-20께부터 코호트 롤아웃, 다음 청구 주기부터 적용"이라고 적었다.
  - `[문서화]` Billable Usage 대시보드·API (HN 발표 2026-08-03): https://blog.cloudflare.com/billable-usage-api/ — 비용을 보여 줄 뿐 상한은 아니다.
  - `[문서화]` **AI Gateway spend limits** (2026-06-05): 달러 기준 예산을 넘으면 요청을 막는 실제 차단 기능이다. 단 **AI Gateway 트래픽에만** 적용되고 계정 전체 상한이 아니다. https://developers.cloudflare.com/changelog/post/2026-06-05-spend-limits/ · 검색 시점 2026-10-03
  - **결론 (검색 시점 2026-10-03):** 커뮤니티 인식과 체인지로그를 대조하면 Workers·DO·D1·R2 전체를 덮는 계정 단위 하드 지출 상한은 여전히 없다. 알림(사후)과 차단(사전)은 다른 기능이다. 책에서는 이 차이를 분명히 다뤄야 한다.
  - (미검증 2차 인용) "RetainDB 사이드 프로젝트 81명 사용자, $36,000" 사례는 검색 스니펫에만 나오고 원문을 확인하지 못했다. 인용하지 말 것.

### 패턴 2: "인터넷의 20%가 한 회사에 묶여 있다" — 잇단 장애와 단일 벤더 리스크

- **출현 예시:**
  - HN "Cloudflare outage on November 18, 2025 post mortem" (2025-11-18, **1465점·916댓글**) — https://news.ycombinator.com/item?id=45973709 · 검색 시점 2026-10-03
    - ojosilva: "This is the multi-million dollar .unwrap() story. … that's what you get for an outage this big that had me tied up for half a day."
    - binarymax: "28M 500 errors/sec for several hours from a single provider. Must be a new record."
    - otterley: "Absent from this list are canary deployments and incremental or wave-based deployment of configuration files (which are often as dangerous as code changes)"
    - SerCe(긍정 쪽): "As always, kudos for releasing a post mortem in less than 24 hours after the outage"
  - HN "Cloudflare outage on December 5, 2025" (2025-12-05, 782점·566댓글) — https://news.ycombinator.com/item?id=46162656 · 검색 시점 2026-10-03
    - lionkor: "Cloudflare is now below 99.9% uptime, for anyone keeping track. I reckon my home PC is at least 99.9%."
    - flaminHotSpeedo: "Not only did they fail to apply the deployment safety 101 lesson of 'when in doubt, roll back' …"
  - HN "Cloudflare outage on February 20, 2026" (2026-02-21, 190점) — https://news.ycombinator.com/item?id=47103649 · 검색 시점 2026-10-03
    - atty: "it seems like Cloudflare has been having more network disruptions lately than they used to. … is that just recency bias?"
    - boarush: "businesses care more about SLAs and uptime than the incident report."
  - HN "Cloudflare R2 Outage (Sigh)" (2026-08-08) — https://news.ycombinator.com/item?id=49224478 · 검색 시점 2026-10-03
    - minraws: "I am a long time Cloudflare user, I have been moving more and more of my stuff to the platform. … Please don't make me have to figure out how to move services again, I am tired folks."
    - 반박 hnthrow10282910: "There was no data loss in this incident. … Personally long time R2 user and it's fantastic." (데이터 유실 여부는 두 주장이 엇갈림 — 검증 필요)
  - 한국 GeekNews "Cloudflare 2025년 11월 18일 장애 사후 분석" — https://news.hada.io/topic?id=24471 · 검색 시점 2026-10-03
    - princox: "Cloudflare가 안되어서 온갖 서비스가 중단되니 지옥이더군요.."
    - barca105: "CF정도되는 회사에서도 .unwrap()을 쓰네요 ㄷㄷ 저 코드가 어떻게 프로덕션에 적용된거지" / skageektp: "unwrap이 문제는 아닌거같은" / barca105: "근본적인 문제는 잘못된 쿼리죠."
    - t7vonn: "설정파일 관련 장애는 어디서든 나네요."
  - 한국 GeekNews "Cloudflare, 또다시 다운" (2025-12-05) — https://news.hada.io/topic?id=24848 · 검색 시점 2026-10-03
    - gpdir16: "대시보드와 API라고만 표시되어있는데 클로드, 클라우드플레어 웹사이트, 제 웹사이트, 다운디텍터 모두 접속이 안되었었습니다"
    - redmi: "Cloudflare에서 HTTP 트래픽 28%가 500 응답을 했다고 블로그에 올렸습니다"
- **추정 원인(커뮤니티 진단):** 전역 설정 배포에 단계적 롤아웃·카나리가 없다는 지적이 가장 많다. 11/18은 Bot Management feature file, 12/5는 WAF 규칙의 전역 설정, 2/20은 BYOIP API 버그로 원인은 매번 달랐지만 폭발 반경이 전역이었다는 점이 같다.
- **책 연결:** 이 장애 이야기는 무료로 시작해 모든 걸 한 벤더에 올리는 결정의 반대편을 보여 준다. 정적 폴백, 다중 DNS, 상태 페이지 의존 같은 대비책을 이끌어 낼 오프닝 소재로 쓸 수 있다.

### 패턴 3: Pages와 Workers 중 무엇을 써야 하나, Next.js는 왜 매 버전마다 깨지나 — 배포 경로의 혼란

- **출현 예시 (Pages → Workers):**
  - Reddit r/CloudFlare "Help me understand Workers vs Pages in Cloudflare (I'm confused!)" (u/Prasheel_Varma, 2026-03 무렵) — https://www.reddit.com/r/CloudFlare/comments/1s40651/ (미러 스냅샷 경유) · 검색 시점 2026-10-03
    - 최다 추천(28점) u/jekadotorg: "Cloudflare added backend functions to Pages and static hosting to Workers." 미래를 생각하면 Workers를 쓰라는 조언.
  - Reddit r/CloudFlare (u/BasteinOrbclaw09, 2026-03 무렵): Cloudflare는 "moving away from Pages"라며 Workers를 권함 — https://www.reddit.com/r/CloudFlare/comments/1s4bdml/ (미러 경유)
  - 블로그 Bryce Wray "From Pages to Workers (again)" (2025-05-27) — https://brycewray.com/posts/2025/05/pages-workers-again/ · 검색 시점 2026-10-03
    > "following it is no walk in the park."
    - Pages Functions를 단일 파일로 합쳐야 했고, CSP 헤더와 정적 자산 장기 캐시 전략을 다시 짜야 했다.
  - HN (aperture147, 2025-10-15) — https://news.ycombinator.com/item?id=45589265 · 검색 시점 2026-10-03
    > "Pages seems to be on the way out, leaving me with Workers Assets that are painful to migrate. Configs that worked in Wrangler 3 didn't carry over cleanly to Wrangler 4, and it feels like Wrangler 5 will introduce yet another interaction model."
  - `[문서화]` Cloudflare 공식 입장(Bryce Wray 인용): "Cloudflare Pages will continue to be supported, but, going forward, all of our investment, optimizations, and feature work will be dedicated to improving Workers."
- **출현 예시 (Next.js 어댑터 이탈과 버전 지연):**
  - Reddit r/nextjs "How are you guys deploying next16 on cloudflare" (2025-12-06 무렵) — https://www.reddit.com/r/nextjs/comments/1pex20t/ (미러 경유) · 검색 시점 2026-10-03
    - next-on-pages가 deprecated되면서 Next 16에서 함수당 빌드 산출물이 5~10KB에서 약 500KB로 커졌다. 답글 u/fredsq: OpenNext와 Workers로 가거나 "build with a better tool like react router or tanstack start". u/AdowTatep: 수정될 때까지 Next 15에 머문다.
  - GitHub opennextjs/opennextjs-cloudflare — 반응 수 상위 이슈 대부분이 "Next 새 버전 지원" 문제다 · 검색 시점 2026-10-03
    - #972 "Next16 support" (2025-11-04, 39댓글, closed) — https://github.com/opennextjs/opennextjs-cloudflare/issues/972
    - #1049 "Next.js 16.1.0 crashes on Cloudflare Workers (Error 1101): Cannot assign to read only property 'setImmediate'" (2025-12-19, closed 2026-01-16) — https://github.com/opennextjs/opennextjs-cloudflare/issues/1049 · ilyesm: "Downgrading to 16.0.10 fixed it immediately."
    - #1157 "Next.js 16.2.0 crashes … Unexpected loadManifest(/.next/server/prefetch-hints.json)" (2026-03-18, closed) — https://github.com/opennextjs/opennextjs-cloudflare/issues/1157
    - #653 "[BUG] Performance is unusably slow" (2025-05-08, 33댓글) — https://github.com/opennextjs/opennextjs-cloudflare/issues/653
      > "I have all the caching functionality enabled but ttfb still ranges from 1.2s to almost 3 seconds! … this makes this library almost completely un usable for almost all websites."
      - 메인테이너 conico974는 Next가 요청마다 무거운 NextServer를 로드하고, KV cold read도 영향을 준다고 설명했다. **이후 변화:** 2025-10 Cloudflare가 CPU 벤치마크 논란을 계기로 V8 GC 튜닝, OpenNext 스트림 버퍼 중복 제거 등을 반영했다(HN 45584281). 부분 해소로 보이지만 검증이 필요하다.
    - #1214 "esbuild fails resolving pg-cloudflare/dist/index.js (Hyperdrive + node-postgres)" (2026-04-20, **open**) — https://github.com/opennextjs/opennextjs-cloudflare/issues/1214 · 우회책은 `next build --webpack` 또는 `outputFileTracingIncludes`에 pg-cloudflare 추가. 2026-09-18에도 "Had same issue using next 16.3" 보고가 있다.
  - HN (orliesaurus, 2025-10-15): "its really annoying that nextjs has to be forked and/or patched to work on cloudflare." — https://news.ycombinator.com/item?id=45586624
- **vinext 등장과 반응:**
  - HN "How we rebuilt Next.js with AI in one week" (2026-02-24, 540점·236댓글) — https://news.ycombinator.com/item?id=47142156 · 검색 시점 2026-10-03
    - 기대(hungryhobbit): "Better performance is something the Next community has been begging for for years … I hope it succeeds and gets proven so I can use it at my company!"
    - 신중(thawab): "Nextjs had remote code execution vulnerabilities because of how they implemented react server side. I am not touching an AI version without waiting for a while."
    - 품질 의문(slopinthebag): "does it actually handle the edge cases or does it just pass the tests."
  - 보안 지적: "Vulnerabilities in Cloudflare's vinext disclosed by Vercel" (2026-02-26) https://news.ycombinator.com/item?id=47161827 , hacktron "Vibe-Hacking Cloudflare's Vibe-Coded Next.js Replacement" (2026-02-28) https://news.ycombinator.com/item?id=47191775 — `[이해관계자: Vercel CEO 측 공개]`
  - vinext 1.0 발표(2026-09-28): https://blog.cloudflare.com/vinext-nextjs-on-vite/ — 1.0 이후의 실사용 후기는 아직 거의 없다(HN 4점). [리서치 공백]
- **추정 원인:** OpenNext는 Next 빌드 산출물을 역설계하는 어댑터라서 Next 마이너 버전이 나올 때마다 깨진다. vinext는 이 구조적 문제를 해결하려는 시도지만 아직 검증 기간이 짧다.

### 패턴 4: D1, KV, Durable Objects 중 무엇을 쓰나 — 10GB 상한, 최종 일관성, 트랜잭션

- **출현 예시:**
  - HN Ask "Why people still use GCP and AWS?" (keeda, 2026-04-08) — https://news.ycombinator.com/item?id=47696317 · 검색 시점 2026-10-03
    > "The 10GB limit per DB is unsuitable for even trivial use-cases. I was going to use it for a new prototype … and I realized the DB limitations could quickly become a blocker even for a prototype."
    - grugdev42: "Because they don't offer the most basic service... virtual machines. Not everyone is making serverless JS web applications!"
  - HN "Journey to Optimize Cloudflare D1 Database Queries" (2025-04-03, 117점) — https://news.ycombinator.com/item?id=43572511 · 검색 시점 2026-10-03
    - fastball: "I evaluated D1 for a project a few months ago, and found that global performance was pretty terrible."
    - kpozin: "a transaction cannot span multiple D1 requests, so you can't select from the database, execute application logic, and then write to the database in an atomic way." 이 사람은 batch 첫 문장에서 일부러 JSON 파싱 오류를 내 나머지를 중단시키는 편법을 썼다.
    - piterrro: "The only real application I found so far are small projects where less than 5 tables are needed and no JOINs are required."
    - (2025-04 글이다. D1 read replication은 같은 달 공개됐으므로 글로벌 읽기 지연 불만이 일부 완화됐을 수 있다 — 검증 필요)
  - Dev.to "Cloudflare Workers Rate Limiting: 3 KV Mistakes We Made" (Oleksandr Kuryzhev, 2026-07-01) — https://dev.to/oleksandr_kuryzhev_42873f/cloudflare-workers-rate-limiting-3-kv-mistakes-we-made-4m9n · 검색 시점 2026-10-03
    - KV를 강한 일관성 저장소처럼 썼고(전파 최대 60초), 키당 초당 1회 쓰기 제한을 무시했고, API 키를 그대로 KV 키로 썼다.
    > "If your rate limiter can fail in a way that produces zero errors, you need a metric specifically watching for that — not just error rate."
    - 해결: 카운팅은 사용자당 DO 하나로 옮기고, KV는 느리게 바뀌는 설정에만 쓴다. 비용이 약 40% 줄었다고 한다.
  - GitHub workers-sdk #2733 "D1 Transaction support" (2023-02, 42댓글, 반응 1위, closed) — https://github.com/cloudflare/workers-sdk/issues/2733 — 트랜잭션 요구가 오래된 고통임을 보여 준다.
  - Reddit r/CloudFlare "I built a full AI-powered search engine using only Cloudflare free tier" (u/tcoder7, 2026-06 무렵) — https://www.reddit.com/r/CloudFlare/comments/1u085uo/ (미러 경유) · 검색 시점 2026-10-03
    - D1 대량 삽입은 `wrangler d1 execute`가 REST API보다 "~100× slower"라고 한다. KV 캐시 적중률 약 85%. Workers AI 하루 무료 5,000 neurons를 관리한 경험도 있다(수치는 문서와 대조 필요).
- **추정 원인:** 같은 문제를 푸는 저장소가 너무 많다. HN "Cloudflare's AI Psychosis" (2026-08-15, 120점) https://news.ycombinator.com/item?id=49310719 원문은 "Too many ways to do the same thing, none of them great"라고 쓴다. 반대로 hasyimibhar는 각각 한 줄로 정리할 수 있다고 반박했다 — https://news.ycombinator.com/item?id=49311320

### 패턴 5: Tunnel은 마법 같지만 ToS·TLS 종단·Zero Trust UX가 걸린다

- **출현 예시:**
  - HN "Cloudflare Quick Tunnels" (2026-09-18, **844점·316댓글**) — https://news.ycombinator.com/item?id=49754785 · 검색 시점 2026-10-03
    - tombert: "officially you're not allowed to use them for streaming video, meaning I can't put it in front of my Jellyfin without breaking TOS."
    - TIPSIO: "Tried to first do this with Cloudflare Tunnels (because I love Cloudflare), but between the broken dashboard side of Zero Trust and nightmare of Warp… it was basically impossible to setup."
    - aliasxneo: "I just have low trust with them recently with how big they are getting."
    - noname120: Quick Tunnels는 5년 넘은 기능이라고 지적(web.archive 2021 근거). "There should at least be a [2021] in the title."
    - whizzter: "Don't all these free proxy services always fall prey to blacklists because scammers,etc abuse them until they're useless?"
  - HN "I finally understand Cloudflare Zero Trust tunnels" (2025-11-16, 311점) — https://news.ycombinator.com/item?id=45946865 · 검색 시점 2026-10-03
    - jchw: "it acts as a termination point for TLS, whereas Tailscale does not. … that's a pretty big privacy downgrade for tunneling from the Internet."
    - yegle: "Free Cloudflare account cannot be used to serve my Plex server. To me that's a no-go."
    - sylens: Immich 앞단에 썼는데 "Only issue is the 100MB upload size for videos." (Free 플랜 업로드 본문 한도 — 문서 대조 필요)
    - amluto: CNAME을 `{uuid}.cfargotunnel.com`으로 걸어 라우팅하는 구성을 두고 "It boggles my mind that Cloudflare ever considered this acceptable for production"
    - jorams: "You've also in the process converted your entire security model to Cloudflare's idea of 'Zero Trust' which involves 100% trusting Cloudflare."
  - Lemmy·셀프호스팅 커뮤니티의 ToS 해석 (검색 요약 경유, 날짜 미상) — 기술적으로는 위반이지만 개인 단위로 단속된 사례는 거의 없고, 대규모 불법 복제 대응용 조항이라는 견해가 많다. 예전 "비디오 스트리밍 금지" 조항은 이후 바뀌었다는 주장도 있다. `[일화, 공식 ToS 대조 필요]` (예: https://feddit.it/post/30874176/20695568)
  - 블로그 Nicolas Fränkel(Java Champion) "From Cloudflare zero-trust to Tailscale" (2026-01-11) — https://blog.frankel.ch/cloudflare-zero-trust-tailscale/ · 검색 시점 2026-10-03
    - 사용자 기기가 사설망 안에 없어서 서비스마다 공개 엔드포인트를 만들어야 했다. SSH가 어려웠고, TLS 인증서 투명성 로그 때문에 서브도메인과 홈서버가 노출됐다. "Migrating to Tailscale was a leap of faith, but I'm very happy I did it."
  - GitHub cloudflared #491 "grpc support" (2021-10 개설, **2026-09-30까지 open, 66댓글**) — https://github.com/cloudflare/cloudflared/issues/491 · 검색 시점 2026-10-03
    - owenhaynes (2026-09-29): "It would be good if this gRPC support could be completed as its been years in progress for proper support"
    - lmtr0 (2026-09-30): `--protocol http2 --http2-origin --no-tls-verify`에 HTTPS 애플리케이션, HTTP2 연결, Chunked Encoding 비활성화를 조합해 동작시켰다.
    - ShadiestGoat (2026-09-06): "DO NOT enable 'Match SNI To Host' option. This will cause the trailing issue"
    - Java·Spring의 gRPC 서비스를 Tunnel로 노출하려는 독자에게 직접 관련 있다. 별개로 2026-08 "Workers and Containers now support inbound TCP connections and gRPC" 발표가 있었다(https://news.ycombinator.com/item?id=49155579). Tunnel 경로와는 다르다.
  - GitHub cloudflared QUIC 연결 문제 (#1158 2024-01, #1379 2024-06 등) — "Failed to serve quic connection error='timeout: no recent network activity'" 보고가 2025-09 로그까지 이어진다. `[문서화]` UDP 7844가 막혀 있으면 HTTP/2로 폴백하며, 업그레이드로 해결되는 경우가 많다. https://github.com/cloudflare/cloudflared/issues/1379
  - 한국 다모앙 계열 경험담은 Tunnel이 아니라 Workers 속도 문제였다(패턴 7 참조).
- **실무 쪽 반응 요약:** 공개 웹앱 노출은 Tunnel과 Access가 편하다는 평이다(HN brownindian 2026-03-08: "Put Cloudflare Access in front of the tunnel, now you have a proper auth via Google or Github." https://news.ycombinator.com/item?id=47302010). 사설 접근(SSH, 동기화, 미디어)은 Tailscale 쪽으로 가는 흐름이 반복된다.

### 패턴 6: "무료·무제한은 공짜가 아니다" — 엔터프라이즈 영업 압박

- **출현 예시:**
  - HN "Why is Cloudflare Pages' bandwidth unlimited?" (2025-01-15, 607점·357댓글, **21개월 전 — 패턴은 계속 재확인됨**) — https://news.ycombinator.com/item?id=42712433 · 검색 시점 2026-10-03
    - neya: "It's not really free. One day, you get a call from their sales team saying 'you're straining our network'. I kid you not. We were on a business plan and still got this. … we were asked to upgrade to a $2000+ per month plan. From a $200/mo plan."
    - i_have_an_idea: "Unless you stay very small, you'll eventually get on the radar of the sales team and you'll realize the service is neither unlimited nor free."
    - 반대편 nichochar: "We're building our startup infra on cloudflare … it turned out to be an amazing decision... Generous free tiers, pricing scales very competitively"
    - simonw: 무료 티어는 DNS 이전이라는 가장 큰 온보딩 장벽을 미리 넘게 해 주는 퍼널이라는 해석.
    - 한국 GeekNews 동일 주제(2025-01-16): https://news.hada.io/topic?id=18754 — "일정 규모 이상이 되면 고가의 계약을 요구받을 수 있음" 우려 요약.
  - HN "Cloudflare took down our website" (2024-05-26, 1044점, **오래됨**) — https://news.ycombinator.com/item?id=40481808 / 원문 https://robindev.substack.com/p/cloudflare-took-down-our-website · 검색 시점 2026-10-03
    - Business 플랜($250/월)을 쓰던 회사가 "24시간 안에 $120k 엔터프라이즈 선결제"를 요구받았다고 주장한다. 원문 표현은 "It felt like extortion."
    - **맥락:** 이 회사는 온라인 카지노였고 지역별 미러 도메인을 돌려 쓰고 있었다(candiddevmike: "Sounds like OP is a casino and plays domain games … Recommend reading article carefully before reacting to the headline."). 일반 개발자 사례로 일반화하면 안 된다.
    - jrochkind1: "No, there is no limit. But based on your traffic, we require you to get an enterprise plan." 식의 대화가 반복된다는 전언.
- **추정 원인:** "unmetered"는 ToS상 대역폭 과금이 없다는 뜻이지, 트래픽 유형(대용량 비HTML, 비디오)이나 규모에 상관없이 계속 무료라는 보장이 아니다. 대상 독자(개인·소규모)에게 실제로 닥칠 확률은 낮지만 불안은 크다.

### 패턴 7: Workers 런타임 한계 — CPU·메모리·번들 크기·nodejs_compat·체감 속도

- **출현 예시:**
  - HN "Unpacking Cloudflare Workers CPU Performance Benchmarks" (2025-10-14, 317점) — https://news.ycombinator.com/item?id=45584281 · 검색 시점 2026-10-03
    - Theo Browne 벤치마크(Vercel Node 대비 최대 3.5배 느림)에 Cloudflare가 응답했다. 스케줄링 개선, V8 young generation 제약 제거, JSON.parse 패치 등을 반영. `[이해관계자: Cloudflare 블로그]`
    - nisten: "nextjs being 4 times slower latency wise than plain react or even vanilla js is pretty funny"
    - orliesaurus: "huge fan of CF, and if cloudflare had the attention to details that vercel has, there would be no vercel."
  - 한국 다모앙 "Cloudflare Workers 비용과 속도 경험기" (띠부씰, 2025-12-13) — https://damoang.net/development/2488 · 검색 시점 2026-10-03 · `[일화]`
    - 무료 플랜에서 응답이 1~2초였고 요청이 LA로 라우팅되는 경우가 있었다고 한다. 유료($5)와 Smart Placement 적용 후: "체감상 아주 조금, 한 10~20% 정도는 빨라진 느낌". Argo Smart Routing(도메인당 $5/월)을 더하자 "눈에 띄게 빨라졌고", 최종 월 $10. (한국발 트래픽이 어느 PoP로 가는지는 ISP 피어링에 좌우된다는 점을 검증할 것)
  - OpenNext 트러블슈팅 문서와 PR — "Your Worker exceeded the size limit of 3 MiB" (Free) · https://opennext.js.org/cloudflare/troubleshooting · 검색 시점 2026-10-03 · `[문서화]`
    - (fact-checker 대조 필요) 유료 Worker 크기 한도가 출처마다 다르다. 한쪽은 "10 MiB", 다른 쪽은 "1 MiB→3 MiB(무료), 10 MiB→15 MiB(유료)로 상향"이라고 쓴다. 현행 limits 문서로 확정해야 한다.
  - `[문서화]` Error 1102 "Worker exceeded resource limits". 메모리 128MB는 isolate 단위이고 동시 요청이 이를 공유한다. 유료 CPU 기본 30초, 최대 5분까지 설정 가능하다(검색 요약 경유 — 대조 필요). https://developers.cloudflare.com/workers/platform/limits/
  - `[문서화]` nodejs_compat — 2025-08 이후 `node:fs`가 기본 제공된다(compat date 2025-09-01 이상). body-parser, jsonwebtoken, knex, passport 같은 패키지가 로드 가능해졌다. https://developers.cloudflare.com/changelog/post/2025-08-15-nodejs-fs/ — 2024년 이전의 "npm 패키지가 안 돌아간다" 불만은 상당 부분 해소됐다. 대신 #1049처럼 프레임워크가 Node 내부를 건드리는 지점에서 새 문제가 생긴다.
  - Dev.to (eliasoliedev, 2026-01-10 무렵) "I asked devs to crash my app" — https://dev.to/eliasoliedev/i-asked-devs-to-crash-my-app-heres-what-happened-in-the-first-24h-ddos-billing-limits-error-30g9 · 검색 시점 2026-10-03
    - Reddit·TabNews·DEV.to 트래픽이 몰려 Workers 무료 할당량을 다 썼고, 사용자에게 Error 1101 계열 화면이 노출됐다. 같은 날 Railway 쪽은 하드 지출 한도가 걸려 서비스가 멈췄다.
    > "Sometimes the bottleneck isn't code, it's the budget configuration."
    - 패턴 1과 같은 동전의 반대 면이다. 무료 한도는 비용을 지켜 주지만 가용성을 희생시킨다.
  - Kotlin 쪽: kotlinlang Slack "has anyone built something on cloudflare workers with kotlin" — https://slack-chats.kotlinlang.org/t/12050046/has-anyone-built-something-on-cloudflare-workers-with-kotlin · (2023 무렵으로 추정, **오래됨**) · Kotlin/JS는 코루틴과 stdlib 초기화 때문에 요청당 100~200ms 지연이 더해진다는 보고(검색 요약 경유). Kotlin/Wasm이 나온 뒤에도 유효한지는 [리서치 공백].

### 패턴 8: Containers는 "드디어 아무 언어나"인가, 비싼 실험인가

- **출현 예시:**
  - HN "Offloading FFmpeg with Cloudflare" 스레드 (2026-03-14~15) — https://news.ycombinator.com/item?id=47320571 · 검색 시점 2026-10-03
    - rozenmd: "This is the perfect use of cloudflare containers. Rare, bursty workloads that fit around regular use of Workers. … not even noticeable in billing."
    - meerab: R2를 FUSE(tigrisfs)로 마운트한 FFmpeg 컨테이너를 운영 중이며, "files never hit the public internet."
    - detuks: "I would not suggest using cloudflare containers for ffmpeg. Feels like it is the nost expensive product they have."
  - HN (youngbum, walla.my, 2026-05-21) — https://news.ycombinator.com/item?id=48216483 · 검색 시점 2026-10-03 · (한국 팀으로 보임)
    > "We did also try to deploy them on Cloudflare infrastructure but… as you know, Cloudflare workers were not built for Hocuspocus. We also tried Cloudflare Containers, but they weren't as reliable as just spinning up a small VM. 1vCPU and 1GB RAM were enough to synchronize about 3,000 users."
  - HN (nickandbro, 2026-01-24): "I use cloudflare containers and it takes roughly 6-7 seconds to boot up using a very lightweight image." — https://news.ycombinator.com/item?id=46740520
  - 블로그 sliplane "Cloudflare Containers in 2026" (Jonas Scholz) — https://sliplane.io/blog/cloudflare-released-containers-everything-you-need-to-know · 검색 시점 2026-10-03 · `[이해관계자: 경쟁 PaaS 공동창업자]`
    - 베타 시절 콜드 스타트 2~3초, 슬립 후 디스크 초기화(ephemeral), linux/amd64 전용. 상시 가동 standard(4GiB) 인스턴스는 월 약 $82.44로 일반 PaaS보다 5~10배 비싸다는 계산.
  - HN "Why we're moving off Cloudflare Durable Objects" (Wire, 2026-07-09) — https://news.ycombinator.com/item?id=48846757 / 원문 https://usewire.io/engineering/why-were-moving-wire-off-cloudflare-durable-objects/ (2026-07-07)
    - 컨테이너 배치가 고정적이고(한 리전에서 만들어지면 계속 그 리전), 테넌트별 전용 용량과 셀프호스팅이 없다는 이유를 들었다. 단 "This is not a 'we left Cloudflare' post. … the API, the frontends, the control plane, and processing all still run on Workers."
    - 반론 PUSH_AX: "The thought of moving back to Fly after CF is completely absurd to me"
  - **이후 변화:** 2025-11 Containers 관련 체인지로그(NicoJuicy가 HN 46034982에서 언급), 2026-08 Containers 인바운드 TCP·gRPC 지원, 2026-09-30 "Cloudflare Containers, rebuilt to scale agent sandboxes"(https://news.ycombinator.com/item?id=49909470). 위 불만 일부는 낡았을 수 있다.
  - (fact-checker 대조 필요) 콜드 스타트 수치가 출처마다 다르다. 2~3초(sliplane, 베타), 6~7초(nickandbro, 2026-01), 200ms(검색 요약, 출처 불명). 현행 공식 수치로 확정해야 한다.

---

## 실무 휴리스틱

### 휴리스틱 1: 공개 API·실험은 Free 플랜 계정에 두고, 유료 계정에는 스스로 차단기를 만든다
- 출처: simonw (HN 2026-06-20) https://news.ycombinator.com/item?id=48611258 / helloacm (2022-08) / Little Bear Apps (2026-03-18) https://littlebearapps.com/blog/d1-billing-disaster-circuit-breakers/ · 검색 시점 2026-10-03
- 원문:
  > "The safest way to use Workers is on the free tier, which will shut off after 100,000 requests/day" — simonw
- 구현 패턴(Little Bear Apps): 기능별 예산, 프로젝트 합산, 전역 비상 정지의 3단 구조. 70% 경고, 90% 위험, 100%에서 자동 비활성화하고 KV TTL로 1시간 뒤 자동 해제한다. 탐지 지연은 약 30초.
- 동조: photobombastic "Prevention over detection" (HN 47323303), matrixgard "Per-service p95-vs-median alerts at hourly granularity would have flagged this inside 6 hours" (HN 47823007).

### 휴리스틱 2: DO alarm은 "이미 있는지" 확인하고 걸고, 프리뷰 환경에서는 DO 바인딩을 뺀다
- 출처: thewillmoss, HN 2026-04-16 https://news.ycombinator.com/item?id=47787042 · 검색 시점 2026-10-03
- 원문:
  > "Strip DO bindings from preview environments entirely - Deploy a budget monitor kill switch Worker - Add a circuit breaker that checks alarm state before scheduling"
  - 코드: `const existing = await this.ctx.storage.getAlarm(); if (!existing) await this.ctx.storage.setAlarm(Date.now() + 60_000)`
- 대안(jacobmei): 쓰기가 인바운드 요청에서만 일어나게 설계한다. edge cache의 `max-age=3600`을 자연 스로틀로 쓰면 KV 쓰기가 "keys × 24/일"로 묶인다. "No alarms means no self-triggering loop is even possible."

### 휴리스틱 3: 커스텀 도메인을 붙였으면 `workers.dev`를 끈다 — WAF를 우회하는 뒷문이다
- 출처: HN "GPT Bot Ignoring Robots.txt on my cloudflare worker" (white_viel, 2026-02-25) https://news.ycombinator.com/item?id=47153800 · 검색 시점 2026-10-03
- 원문:
  > "the bot was bypassing the route on the domain and using the worker.dev domain … interesting that GPT was accessing the worker directly to bypass the WAF rule son Cloudflare"
- 응답 kentonv `[이해관계자: Cloudflare Workers 리드 엔지니어]` (2026-02-25) https://news.ycombinator.com/item?id=47156303:
  > "workers.dev domains can be a liability sometimes … you can disable the workers.dev zone by putting `"workers_dev": false,` in wranlger.jsonc. You can also enable Cloudflare Access on your workers.dev zone to require login … But of course you have to remember to do those things..."
- 책 연결: 패턴 1(비용)과 보안 장이 만나는 지점이다. "WAF·레이트 리밋을 Worker 앞에 둔다"는 조언은 workers.dev를 닫아야 비로소 성립한다.

### 휴리스틱 4: KV는 느리게 바뀌는 설정용, 카운터·락은 Durable Objects로
- 출처: Kuryzhev, Dev.to 2026-07-01 https://dev.to/oleksandr_kuryzhev_42873f/cloudflare-workers-rate-limiting-3-kv-mistakes-we-made-4m9n · 검색 시점 2026-10-03
- 원문:
  > "A single busy API key gets hit from many edge locations near-simultaneously, which is exactly the scenario that makes the propagation delay...worse."
- 근거(문서화): KV 전파는 최대 60초이고, "없음" 결과도 캐시된다(검색 요약 경유, 문서 대조 필요).

### 휴리스틱 5: "큰 DB 하나"가 필요하면 Hyperdrive와 외부 Postgres를, 아니면 테넌트별 작은 SQLite 여러 개를
- 출처: kentonv `[이해관계자: Cloudflare Workers 리드 엔지니어]` HN 2026-04-08 https://news.ycombinator.com/item?id=47696640 · 검색 시점 2026-10-03
- 원문:
  > "The 10GB limit applies to one database, but the idea is you design your system to split data into many small databases, e.g. one per user, or even one per document. … If you really need a single big database, you can use Hyperdrive, which provides connection management and caching over plain old Postgres, MySQL, etc."
- Hyperdrive 연동 시 실무 주의(Neon/Supabase 문서·FAQ 경유, `[문서화]`): Neon serverless 드라이버는 WebSocket을 써서 Hyperdrive 풀을 우회하므로 TCP 드라이버(`pg`, postgres.js)를 쓴다. Supabase는 풀러 주소 대신 direct 연결 문자열을 써서 이중 풀링을 피한다. https://neon.com/blog/hyperdrive-neon-faq · https://neon.com/docs/guides/cloudflare-hyperdrive
- 커뮤니티 실사용 흔적: "Neon Postgres via Prisma + Hyperdrive" 스택(HN 47146087, 2026-02-25), Vithos 템플릿 "Hyperdrive + optional Neon PR previews"(HN 48435284, 2026-06-07). 깊은 후기는 적다.

### 휴리스틱 6: Stripe 웹훅은 원본 body를 `.text()`로 받아 `constructEventAsync`로 검증한다
- 출처: Hono 공식 예제 https://hono.dev/examples/stripe-webhook · Stripe 문서 https://docs.stripe.com/webhooks/signature.md · 검색 시점 2026-10-03 · `[문서화 위주 — 커뮤니티 일화는 수집 못함]`
- 요지: 프레임워크가 JSON을 먼저 파싱하면 서명 검증이 깨진다. Workers에서는 동기 `constructEvent` 대신 SubtleCrypto 기반 비동기 API를 쓴다. 서드파티 `@worker-tools/stripe-webhook`의 constructEvent가 헤더를 검증하지 않는 취약점 공지가 있다: https://advisories.gitlab.com/pkg/npm/@worker-tools/stripe-webhook

### 휴리스틱 7: 공개 노출은 Tunnel과 Access, 사설 접근은 Tailscale
- 출처: brownindian HN 2026-03-08 https://news.ycombinator.com/item?id=47302010 · itake HN 2026-04-13 https://news.ycombinator.com/item?id=47749343 · Fränkel 2026-01-11 · 검색 시점 2026-10-03
- 원문:
  > "ssh itake@ssh.domain.me -o ProxyCommand="cloudflared access ssh --hostname %h"" — itake
  > "Put Cloudflare Access in front of the tunnel, now you have a proper auth via Google or Github." — brownindian
- Show HN Minvoice (ddyy, 2026-07-15) https://news.ycombinator.com/item?id=48920389: Workers와 D1로 만든 송장 앱이다. 기본 비밀번호 로그인 대신 "I recommend switching to Cloudflare Access". 관리자 화면 보호용으로 Access를 권하는 흐름이다.
- `[문서화]` Access 다중 호스트명 앱의 로그인 루프: 호스트명이 5개를 넘으면 쿠키 체인 때문에 일부 브라우저에서 sign-in loop가 생길 수 있었다. 2026-08-03부터 앱별 "Eager redirect cookie" 설정으로 조정할 수 있다. https://developers.cloudflare.com/changelog/post/2026-08-03-eager-redirect-cookie-setting/

### 휴리스틱 8: Containers는 "가끔, 몰아서" 쓰는 작업용이다
- 출처: rozenmd·meerab (HN 2026-03-14~15) https://news.ycombinator.com/item?id=47382501 · 검색 시점 2026-10-03
- 원문:
  > "Rare, bursty workloads that fit around regular use of Workers." — rozenmd
- 반대 정황: 상시 가동 실시간 동기화 서버(Hocuspocus)는 작은 VM이 더 안정적이었다(youngbum). 상시 가동 비용 계산(sliplane, 경쟁사)도 같은 방향이다.

### 휴리스틱 9: 배포 후 이상하면 캐시 층부터 의심한다 (HTML·서비스워커·CDN)
- 출처: HN "Dropping Cloudflare for Bunny.net" 스레드 (Manchitsanan, 2026-04-07) https://news.ycombinator.com/item?id=47675953 · 검색 시점 2026-10-03
- 원문:
  > "CDN edge caching served stale HTML after a deploy, and the service worker cached the bad response. Took a CDN purge from the dashboard to fix. The debugging experience when things go wrong at the edge is painful, you're always guessing which cache layer is the problem."
- 같은 스레드 mhitza (Bunny 사용자): "Every time I purge the pull zone cache, I do it twice, cause once from my CI isn't enough." CDN 전반의 퍼지 신뢰 문제다.
- `[문서화·가이드]` HTML은 기본적으로 `cf-cache-status: DYNAMIC`이라 캐시되지 않는다. Page Rules는 deprecated되어 Cache Rules로 옮겨 가는 중이다(2024-07 이후 신규 Free 계정은 Page Rules 사용 불가, 2025 자동 이관 예정 — 문서 대조 필요). Page Rules 시절 "Cache Everything"이 Cache Rules에서는 "Eligible for cache"에 해당한다. https://eastondev.com/blog/en/posts/dev/20251201-cloudflare-cache-rules-guide/ (2025-12-01, 개인 블로그) · https://dev.classmethod.jp/articles/cloudflare-page-rules-deprecation-202406/
- 한계: 캐시 관련 날것의 커뮤니티 불만(Reddit·Community 포럼)은 직접 수집하지 못했다. Community 포럼 "[IMPORTANT] Page Rules Migration" 스레드(https://community.cloudflare.com/t/important-page-rules-migration/656021)는 403으로 막혔다. [리서치 공백]

### 휴리스틱 10: R2는 egress가 무료이지 읽기가 무료인 게 아니다
- 출처: WordPress.org 지원 포럼(검색 요약 경유, 날짜 미상) https://wordpress.org/support/?p=18757257 · HN rezonant (2024-02-11, **오래됨**) https://news.ycombinator.com/item?id=39334574 · 검색 시점 2026-10-03
- 원문:
  > "with AI crawlers slurping up content, a site with a few thousand photos and any amount of decent traffic might turn into an expensive mistake relatively quickly." (WordPress 포럼, 요약 경유)
  > "the egress costs are extreme compared to R2 (remember, R2 does charge per read/write though) but (B) storage is cheaper on S3." — rezonant
- Reddit r/CloudFlare (u/alwerr, 2026-03 무렵) "I was thrilled to use Cloudflare Pages+D1 until saw R2 need Credit Card" https://www.reddit.com/r/CloudFlare/comments/1s4bdml/ (미러 경유): 카드 등록 자체를 불안해해서 VPS로 돌아갔다. 답글은 "To avoid spammers.", "billing alerts exist" 등.

---

## 논쟁점

### 논쟁 A: 중앙집중은 인터넷을 더 약하게 만드는가
- 관점 1: 동질적인 거대 시스템은 전역 장애를 계속 낳는다.
  - 대표 발언: mixedbit (HN 2025-12-05) "Homogeneous systems like Cloudflare will continue to cause global outages. Rust won't help, people will always make mistakes, also in Rust." https://news.ycombinator.com/item?id=46168481
  - krick (HN 2025-11-24) "As if after the last time AWS failed … anybody stopped using AWS. As if anybody could viably stop using them." https://news.ycombinator.com/item?id=46030461
  - stroebs: "I love Cloudflare's products … but I can't advocate for using them in my professional job since we actually require distributed infrastructure that won't fail globally in random ways we can't control."
- 관점 2: 중앙화 서비스가 더 견고하고, 장애가 눈에 잘 띌 뿐이다.
  - 대표 발언: miki123211 (HN 2025-11-24) "Centralized services don't decrease redundancy. They're usually far more redundant than whatever homegrown solution you can come up with. The difference between centralized and homegrown is mostly psychological." https://news.ycombinator.com/item?id=46031974
  - vasco: "smaller providers usually have much more ongoing issues, that just happen to be 'chronic' vs 'acute' pains."
- 출처 스레드: "The Cloudflare outage might be a good thing" (2025-11-24, 276점) https://news.ycombinator.com/item?id=46029908 · 검색 시점 2026-10-03

### 논쟁 B: D1의 10GB는 결함인가 설계 철학인가
- 관점 1(결함): keeda "The 10GB limit per DB is unsuitable for even trivial use-cases." (HN 2026-04-08) / fastball "global performance was pretty terrible" (HN 2025-04-07)
- 관점 2(설계): kentonv `[이해관계자: Workers 리드]` "split data into many small databases, e.g. one per user, or even one per document … you can create an unlimited number of them." (HN 2026-04-08) / `[문서화]` "D1 is designed for horizontal scale out across multiple, smaller (10 GB) databases" https://developers.cloudflare.com/d1/platform/limits/
- 독자(Spring/JPA 사고방식)에게는 DB 하나에 스키마 하나라는 전제를 깨는 지점이라 장 하나를 들일 만하다.

### 논쟁 C: Cloudflare Tunnel 대 Tailscale(그리고 ngrok)
- 관점 1(Tunnel 지지): 포트를 열지 않고 TLS·도메인·인증(Access)까지 한 번에 해결한다. AnonyMD (HN 2026-04-08): "It's a magical invention that lets us host websites while keeping our server firewalls closed!" https://news.ycombinator.com/item?id=47686508
- 관점 2(Tailscale 지지): TLS 종단과 MITM 우려, P2P 부재, 벤더 종속. jchw·jorams·siwatanejo (HN 45946865), Fränkel 블로그.
- 관점 3(익명 터널 자체 비판): inconshreveable `[이해관계자: ngrok 창업자]` (HN 2026-09-18) "we removed anonymous usage of our product many years ago because it was far and away the largest source of abuse … anonymous, account-less tunneling services like this are net negative for the security of the internet" https://news.ycombinator.com/item?id=49759719
- 경쟁 홍보 주의: ghoshbishakh `[이해관계자: Pinggy 공동창업자]`. Pangolin(오픈소스 대안, Show HN 2025-07-10, 500점) https://news.ycombinator.com/item?id=44526015

### 논쟁 D: Containers는 쓸 만한가
- 긍정: rozenmd, meerab (간헐적·버스트 작업, R2 내부망 접근). NicoJuicy: "Cloudflare Containers is literally 'pay for usage', while AWS is pay for capacity." (HN 2025-11-24) https://news.ycombinator.com/item?id=46034982
- 부정: detuks("the most expensive product"), youngbum("weren't as reliable as just spinning up a small VM"), Wire(배치 경직성).

### 논쟁 E: vinext — Next.js 문제의 해답인가 위험한 AI 생성물인가
- 기대: hungryhobbit (HN 47143933). 성능 개선과 Vite 기반이라는 점.
- 경계: thawab(RSC RCE 전례), slopinthebag(엣지 케이스), tills13("The messaging is ignorant"), Vercel 측 취약점 공개(이해관계자).
- 한국: GeekNews에도 소개됐지만(https://news.hada.io/topic?id=26988 , 2026-02-25, 댓글 4개) 날것의 국문 논쟁은 확보하지 못했다.
- 메타 비판: acedTrex "God cloudflare's blog quality has fallen off a cliff … just llm slop" (HN 47143848). Quick Tunnels 랜딩 페이지에도 "vibe-coded"라는 비판이 반복됐다(rplnt, skhameneh).

### 논쟁 F: 무료 티어는 선의인가 미끼인가
- 선의·전략: simonw(DNS 온보딩 퍼널), Shakahs("most of the bandwidth is from peering, so it essentially costs them nothing"), Cloudflare 공식 "Cloudflare's commitment to free" https://blog.cloudflare.com/cloudflares-commitment-to-free/
- 미끼·리스크: neya, i_have_an_idea, sjoedev("Cloudflare is not profitable … enshittification"), kugelblitz (HN 2026-04-07) "I don't like free offerings, because what if they decide to charge someday?" https://news.ycombinator.com/item?id=47675778

---

## 커뮤니티 근거 강도별 패턴 순위 (계획자용)

| 순위 | 패턴 | 근거 강도 | 대표 출처 |
|---|---|---|---|
| 1 | 하드 지출 상한 부재와 요금 폭탄(DO·D1·Workers) | 매우 강함 — 2022~2026-09 지속, 금액 최대 $34,895 | HN 47787042, littlebearapps, HN 48611258, 49158930 |
| 2 | 잇단 장애와 단일 벤더 리스크 | 매우 강함 — 1465·782·190점 스레드, 한국 GeekNews | HN 45973709, 46162656, 47103649, GN 24471 |
| 3 | Pages→Workers 혼란과 Next.js 어댑터 버전 지연(vinext 포함) | 강함 — GitHub 이슈 반복, Reddit | OpenNext #972/#1049/#1157/#653/#1214, r/nextjs |
| 4 | D1/KV/DO 선택(10GB, 최종 일관성, 트랜잭션) | 강함 | HN 43572511, 47696317, Dev.to KV |
| 5 | Tunnel의 ToS·TLS 종단·Zero Trust UX와 Tailscale 비교 | 강함 — 844점·311점 스레드 | HN 49754785, 45946865, cloudflared #491 |
| 6 | "무료는 공짜가 아니다" 엔터프라이즈 압박 | 중간 — 고득점이지만 2024~2025-01 중심, 개인 독자에겐 확률 낮음 | HN 42712433, 40481808 |
| 7 | Workers 런타임 한계(CPU·번들·nodejs_compat·체감 속도) | 중간 — 일부는 2025 하반기 개선으로 해소 | HN 45584281, damoang 2488, OpenNext 문서 |
| 8 | Containers 성숙도·비용 | 중간 — 일화 다수, 제품 변화 빠름 | HN 47320571 스레드, 48216483, sliplane |
| (이하) | Access 무료 티어 관리자 보호, 캐시 오해, R2 읽기 비용, Stripe 웹훅 | 약함 — 문서·가이드 위주, 날것 불만 수집 부족 | 휴리스틱 7·9·10·6 |

---

## fact-checker 대조 필요 목록 (값 충돌·미확정)

1. Worker 스크립트 크기 한도: Free 3 MiB / Paid 10 MiB(OpenNext 문서) vs "Paid 15 MiB로 상향"(검색 요약). 현행 limits 문서로 확정할 것.
2. Containers 콜드 스타트: 2~3초(sliplane 베타), 6~7초(HN nickandbro 2026-01), 200ms(출처 불명 요약). 2026-09-30 "rebuilt" 발표 이후 수치 확인.
3. Budget alerts 기본 활성화 시점: 체인지로그 URL 2026-06-15 vs 본문 "2026-07-20께 코호트 롤아웃".
4. Workers 유료 CPU 기본 30초·최대 5분, 메모리 128MB(isolate 단위) — 검색 요약 경유.
5. Tunnel(Free) 업로드 100MB 한도 — HN sylens 일화.
6. Tunnel 비디오 스트리밍 ToS 조항의 현행 문구(바뀌었다는 주장이 있음).
7. Page Rules 일정: 2024-07 신규 Free 계정 차단, 2025 자동 이관.
8. D1 Free 500MB / Paid 10GB, read replication 공개 시점(2025-04).
9. Workers AI 무료 10,000 neurons/일(검색 요약) vs Reddit 일화 "5,000 neurons/day" — 출처 간 충돌.
10. thewillmoss의 $34,895 청구가 이후 면제되었는지(결말 미확인).
11. **[가장 중요] "검색 시점 2026-10-03 기준, Workers·DO·D1·R2 전체를 덮는 계정 단위 하드 지출 상한은 없다."** 이 주장 위에 여러 장이 올라가므로 다음 체인지로그로 재확인할 것: Budget alerts 기본 활성화(알림 전용) https://developers.cloudflare.com/changelog/post/2026-06-15-budget-alerts-default-on/ · Billable Usage API(가시성 전용) https://blog.cloudflare.com/billable-usage-api/ · AI Gateway spend limits(AI Gateway 한정 차단) https://developers.cloudflare.com/changelog/post/2026-06-05-spend-limits/ . 2026-08 이후 계정 단위 상한이 발표됐는지도 함께 확인한다.

---

## 수집 한계

- **수집 규모:** 토론·게시글 약 45건(HN 스레드 26개와 개별 댓글 다수, GitHub 이슈 9건, Reddit 5건(미러 경유), 블로그·Dev.to 8건, 한국 GeekNews 4건, 다모앙 1건).
- **미접근 플랫폼:**
  - Reddit 직접 접근 차단(rate limit). 미러 스냅샷과 2차 인용으로 5건만 확보했다. r/selfhosted·r/homelab·r/webdev의 원문 스레드는 거의 수집하지 못했다.
  - Cloudflare Community 포럼(community.cloudflare.com) 403. 포럼의 결제 분쟁·Access 설정 문제 원문이 비어 있다.
  - Cloudflare Discord, X/Mastodon 스레드, Lobsters는 검색하지 못했다(Lobsters는 R2 LaLiga 차단 건 링크 하나만 확인: https://lobste.rs/s/uetrpm/my_cloudflare_r2_has_been_blocked_from).
  - 한국: velog·OKKY·커리어리·회사 기술 블로그에서 Cloudflare 개발자 플랫폼 실사용기를 찾지 못했다(site 검색 결과 없음). wikidocs 304528(Tunnel 국문 글)은 403으로 원문을 확인하지 못해 인용하지 않았다. GeekNews는 장애 스레드 댓글만 날것으로 확보했다.
- **언어 편중:** 영어 HN 비중이 70% 이상이다. HN 사용자층(인프라 관심이 높고 대기업 비판 성향)의 편향이 있다.
- **[리서치 공백]**
  1. **Java/Kotlin/Spring 개발자의 Cloudflare 실사용기:** HN 댓글 검색("cloudflare tunnel spring boot")에서 0건이 나왔다. Spring Boot를 Tunnel 뒤에 두거나 Containers로 JVM을 올린 구체적 후기가 없다. 관련 단서는 Fränkel(Java Champion)의 Zero Trust→Tailscale 이주, cloudflared gRPC 이슈, Kotlin/JS 초기화 지연(2023 무렵) 정도다. 해당 장은 웹·공식 문서와 저자 실험으로 채워야 한다.
  2. **Hyperdrive + JDBC 없는 백엔드(Neon/Supabase/PlanetScale) 깊은 후기:** 템플릿 언급과 OpenNext 번들링 이슈만 있다. 지연·풀링 체감 후기가 부족하다.
  3. **Workers AI·Images·R2 operations 요금 폭탄 실사례:** 계산기와 우려 글만 있고 1인칭 사례는 확보하지 못했다.
  4. **Access/Zero Trust 무료 50석 실무 함정(IdP 설정, OTP, 서비스 토큰):** 날것의 불만은 TIPSIO("broken dashboard side of Zero Trust and nightmare of Warp") 하나뿐이다. 나머지는 문서다.
  5. **캐시 오해(HTML DYNAMIC, Cache Rules 이관)의 날것 불만:** 개인 블로그 가이드와 Manchitsanan 일화 하나뿐이다.
  6. **vinext 1.0(2026-09-28) 이후 실사용 후기:** 발표 직후라 거의 없다.
  7. **Stripe 웹훅 on Workers 실패담:** 문서와 예제만 있다.
  8. **하이브리드 AWS + Cloudflare 운영기:** 단편적 댓글뿐이다(red-iron-pine "I want diversity of providers").
- **교차 확인 권고:** 패턴 1의 제품 변경(Budget alerts, Billable Usage API, AI Gateway spend limits)과 패턴 7의 런타임 한계 수치는 web-researcher의 공식 문서·체인지로그로 반드시 교차 확인할 것.
