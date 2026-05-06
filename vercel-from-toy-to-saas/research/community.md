# 커뮤니티 리서치: Vercel — 실무자의 목소리

수집 범위: Hacker News, Reddit r/nextjs·r/webdev, GitHub Discussions, GeekNews(news.hada.io), velog, OKKY, dev.to, Indie Hackers.

## 반복되는 고통·질문 (챕터 오프닝 소재)

### 패턴 1: "내 청구서가 갑자기 $700이 됐다"
- 출처: Vercel Bill Shock — Medium (https://journeywithibrahim.medium.com/vercel-bill-shock-from-700-to-120-ec24ee9755c3)
- 출처: Indie Hackers — Huge Vercel Costs and Rebrand to Feather (https://www.indiehackers.com/product/mdx-one/huge-vercel-costs-and-rebrand-to-feather--Myc071NF66jYxLB2yED)
- 출처: HN — "Ask HN: Why is Vercel so expensive?" (https://news.ycombinator.com/item?id=39898391)
- 핵심 패턴: $20 Pro로 시작 → 트래픽 한 번 튀거나 봇 크롤이 들어오면 수백 달러. Image Optimization, Bandwidth, Edge Requests 세 항목이 90% 원인.
- 책 활용: 챕터 4 "비용" 도입부의 정확한 공감 포인트.

### 패턴 2: "Vercel 무료 플랜으로 사이드 프로젝트 띄웠는데, 어느 순간 'commercial use' 경고가 떴다"
- 출처: HN 댓글 (https://news.ycombinator.com/item?id=41031912 — "Why are people paying so much for Vercel?")
- 출처: velog 입문 가이드들이 공통적으로 빠뜨리는 부분. Hobby = personal/non-commercial only.
- 핵심 패턴: AdSense 한 줄, Stripe 한 줄, Sponsorship 링크 → 즉시 ToS 위반. 강제 Pro 업그레이드.
- 책 활용: 챕터 3 "성장 단계 로드맵"의 토이→사이드 전환 시점에 트리거. "처음 1원이라도 받으면 Pro"가 정확한 룰.

### 패턴 3: "DDoS 한 번 맞고 청구서가 $20,000 나왔다"
- 출처: Next.js GitHub Discussion #41485 — "What to do in case of DDoS attack?" (https://github.com/vercel/next.js/discussions/41485)
- 출처: HN — "This is my worst nightmare as a bootstrapped founder" (https://news.ycombinator.com/item?id=39521028)
- 핵심 패턴: Vercel은 자동 mitigation 발동 전 처리된 요청을 청구. 사용자는 "내가 한 일이 아닌 트래픽으로 망한다"는 감각.
- 반박 측: Vercel은 firewall에 의해 차단된 트래픽은 청구하지 않는다고 명시. 차이는 "차단 직전까지 들어온 만큼".
- 책 활용: 챕터 5 "보안" 도입. Spend Management + Attack Challenge Mode + Cloudflare 앞단 등 가드레일이 왜 필수인지.

### 패턴 4: "Netlify가 단순 정적 사이트에 $104k 청구서를 보냈다"
- 출처: HN (https://news.ycombinator.com/item?id=39520776)
- 출처: GeekNews 한국어 정리 (https://news.hada.io/topic?id=13554)
- 핵심: Vercel만의 문제가 아니라 사용량 기반 PaaS 전체의 구조적 위험. Netlify는 결국 면제 처리. Vercel도 "legitimate mistake"는 forgive하는 정책 운영, 단 명시 SLA는 없음.
- 책 활용: 챕터 8 "사례·논쟁"의 전체 PaaS 시장 맥락.

### 패턴 5: "Vercel 외부에서 Next.js를 돌리니 ISR·Image·Middleware가 깨진다"
- 출처: HN (https://news.ycombinator.com/item?id=40627998 — "NextJS There is well-hidden vendor-lock")
- 출처: Reddit r/nextjs (다수 토론), Bring Your Own Next.js (https://richardkovacs.dev/blog/bring-your-own-nextjs)
- 핵심 패턴: 핵심 기능들이 사실상 Vercel-only로 설계됐다는 불만. OpenNext가 매워주지만 추격 형태.
- 반박 측: Vercel "70% of Next.js runs outside Vercel" (https://vercel.com/blog/vercel-the-anti-vendor-lock-in-cloud).
- 새 흐름: Next.js 16.2 stable Adapter API (Cloudflare/Netlify/Amplify/Google과 공동 설계). 의도적 portability 강화.
- 책 활용: 챕터 8 "사례·논쟁" 핵심 토픽. 양 진영을 그대로 병기.

### 패턴 6: "Edge Function에서 Node 라이브러리가 안 돈다"
- 출처: GitHub vercel/vercel discussion #4502, Vercel Functions Limits 공식
- 핵심 패턴: pdfkit, sharp, bcrypt, AWS SDK v2 같은 Node API 의존 라이브러리가 Edge runtime에서 import 자체 실패. 초보 개발자가 미들웨어에 그런 코드를 넣었다가 빌드 에러로 멈춤.
- 책 활용: 챕터 7 "함정". Edge=만능 아님, 가벼운 라우팅·인증·헤더 조작 전용.

### 패턴 7: "Hobby plan에서 cron이 하루 한 번밖에 안 돈다"
- 출처: Vercel Cron Jobs 공식 + HN/Reddit 흩어진 불만
- 핵심: 무료 사용자는 cron 표현이 자주 도는 형태이면 deploy 자체가 실패. 학습용 토이로 매분 cron을 돌릴 수 없음 → "다른 데로 옮기자"의 흔한 진입점.
- 책 활용: 챕터 3 "성장 단계 로드맵"에서 토이→사이드 전환 트리거.

### 패턴 8: "Preview에 production DB를 그대로 붙였다가 데이터가 날아갔다"
- 출처: ShipSafer 글, Reddit r/nextjs 다수 thread
- 핵심: 신입이 자주 빠지는 함정. Preview URL이 외부 노출되거나, PR brancher가 마이그레이션을 도는 사고.
- 책 활용: 챕터 5 "보안"의 워크인 시점. Sensitive 환경변수 + 환경 분리 룰을 강제하는 설계.

### 패턴 9: "Vercel breach (2026년 4월) 이후 모든 env var 회전했나?"
- 출처: GeekNews 한국어 (https://news.hada.io/topic?id=28699 / id=28700 / id=28768)
- 핵심: non-sensitive 변수 노출 가능성. Sensitive 플래그·변수 회전·재배포의 운영 룰이 갑자기 화제로 부상.
- 책 활용: 챕터 5 + 챕터 8.

## 실무 휴리스틱

- **이미지는 외부 CDN으로 빼자.** Cloudflare R2 + CDN, ImgIX, Bunny CDN 등을 이미지 라우트에만 위임 → Image Optimization 청구서 즉시 80% 감소. (출처: howdygo 케이스 스터디)
- **Spend Management부터 켜자.** Pro 만들자마자 임계 알림 + 자동 일시정지. 디폴트는 꺼져 있음. (출처: Vercel docs + HN 다수 권고)
- **Cloudflare를 앞에 둘 가치가 있다.** 도메인 → Cloudflare → Vercel. WAF 강화, DDoS 흡수, 캐시 적중 시 Vercel 전송량 제로. 단, Vercel 자체 ISR과 캐시 헤더 호환 주의. (출처: HN 다수, Schematic 글)
- **Sensitive 플래그는 의심 시 모두 켜라.** UI에서 다시 못 읽는 게 단점이 아니라 보안 자산. (출처: Vercel KB + GitGuardian)
- **`output: "standalone"` 만큼은 항상 익혀둬라.** 비상 탈출 옵션. Docker 이미지 100-200MB. (출처: Next.js docs + dev.to 가이드)
- **Turborepo Remote Cache는 모노레포에서 즉시 켜라.** 빌드 시간 50% 이상 절감 사례 흔함. (출처: Turborepo docs)
- **Edge Middleware에서는 fetch와 헤더 조작만 하라.** 무거운 로직은 Route Handler로 위임. (출처: 공식 + GitHub examples)

## 논쟁점

### 논쟁 A: "Vercel은 비싼가?"
- 관점 1 (비싸다): bandwidth $0.15/GB는 R2/Backblaze의 10-100배. 1TB 사용 시 외부 CDN 대비 명백한 premium. 트래픽 클수록 손해. (HN 다수, Schematic, servercompass)
- 관점 2 (가치가 있다): preview·git push deploy·Next.js 통합·자동 SSL·이미지 최적화 묶음. 인프라팀 1명 인건비 대비 저렴. 작은 팀에 맞다. (Vercel 공식, dev.to 우호 글, "anti-vendor-lock-in" 포스트)
- 책 입장: 양쪽 그대로 병기. 단계별 적정성을 챕터 3에서 결정.

### 논쟁 B: "Next.js는 Vercel 종속인가?"
- 관점 1 (사실상 종속): ISR·Image·Middleware·PPR이 Vercel에서 best/only. 다른 곳에서는 reduced fidelity. (dev.to, HN, eduardoboucas)
- 관점 2 (덜 종속): 70%가 외부에서 운영 중, Adapter API stable, OpenNext mature. (Vercel 공식, Cloudflare blog "vibe codes 94%")
- 책 입장: "기능 매트릭스"를 표로 보여주고 독자가 결정하게.

### 논쟁 C: "Cloudflare로 옮기면 더 나은가?"
- 관점 1 (Cloudflare 옹호): 글로벌 PoP·무제한 bandwidth·$5 Pro·Workers 더 빠름. (DanubeData, niobond)
- 관점 2 (Vercel 잔류): DX·preview·Next.js 통합·생태계. Cloudflare는 OpenNext 어댑터에 의존. (vibecoder, Vercel 공식)
- 변수: 2026 Cloudflare가 Pages에 Docker 컨테이너 지원 추가, Next.js 16.2 Adapter API stable로 격차 축소.

### 논쟁 D: "Edge가 정말 더 빠른가?"
- 관점 1 (Yes): TTFB 50ms 미만, 글로벌 사용자 대상.
- 관점 2 (조건부): DB가 한 region에 있으면 Edge가 그 region까지 round trip. 오히려 느림. Edge Config·Replication이 없으면 의미 약함.
- 학술 근거: 논문 4·5번 (placement-cost-latency triangle).

## 커뮤니티 발 팁 (학습 곡선)

- "처음에는 Vercel 기본값으로 시작해라. 최적화는 트래픽이 실제로 모인 후에." — r/nextjs 단골 답변
- "결제 등록 안 해도 Hobby는 무료다. 단 결제 등록 안 하면 한도 초과 시 정지된다." — 좋은 가드레일.
- "preview 도메인 https://*.vercel.app 은 검색 엔진에 잡힐 수 있다. robots.txt + Deployment Protection." — velog 다수
- "팀원 추가 시 Pro는 seat당 $20. 5명만 모여도 $100/월." — HN, Indie Hackers
- "Vercel Pro 시작 = 실수로 commercial 사용 신호. 회사 명함 박힌 프로젝트라면 처음부터 Pro." — 공통

## 한국 커뮤니티 별도 노트

- velog는 입문 가이드(배포 처음·환경변수·배포 실패 트러블슈팅)가 압도적 다수. 비용·보안 심층 토론은 빈약.
- OKKY는 "프리랜서 가이드"·"코딩 강의"가 주류. Vercel 비용 폭탄은 명시적 thread를 발견하지 못함.
- GeekNews(news.hada.io)는 영어권 토론을 한국어로 빠르게 전달. 2026 보안 사고와 Vercel 관련 주요 뉴스의 한국어 진입점.
- 코딩애플 포럼: "DB·서버·프론트 배포 월 15만원" 사례글(GAE 기반) — Vercel 직접 사례는 아니나, "갑자기 청구서 폭증"의 한국식 표현 패턴 참고.
- 결론: 한국 독자 대상이라면 영어권 사례를 한국어로 전달하면서 "이건 우리 동네에서도 벌어진다"는 신호로 코딩애플·GAE 사례를 짧게 곁들이는 구성이 효과적.

## 링크 모음 (전체)

- https://news.ycombinator.com/item?id=39898391 — Ask HN: Why is Vercel so expensive?
- https://news.ycombinator.com/item?id=41031912 — Ask HN: Why are people paying so much for Vercel?
- https://news.ycombinator.com/item?id=39521028 — Vercel DDoS 청구서 worst nightmare
- https://news.ycombinator.com/item?id=39520776 — Netlify $104k bill
- https://news.ycombinator.com/item?id=43687431 — Cost of Being Crawled (LLM bots + Image API)
- https://news.ycombinator.com/item?id=40627998 — Next.js vendor lock 논쟁
- https://news.ycombinator.com/item?id=47967508 — Vercel pricing page (recent)
- https://news.ycombinator.com/item?id=39932906 — Vercel Improved Infrastructure Pricing
- https://github.com/vercel/next.js/discussions/41485 — DDoS 대응 논의
- https://github.com/vercel/next.js/discussions/81448 — ISR in PPR
- https://github.com/vercel/vercel/discussions/4502 — function timeout config
- https://news.hada.io/topic?id=28700 — Vercel 내부 시스템 침해 (한국어)
- https://news.hada.io/topic?id=28768 — Vercel OAuth 공급망 공격 (한국어)
- https://news.hada.io/topic?id=28699 — Vercel 보안 침해 데이터 판매 주장 (한국어)
- https://news.hada.io/topic?id=13554 — Netlify $104k 청구서 (한국어)
- https://news.hada.io/topic?id=25869 — Vercel React Best Practices repo
- https://news.hada.io/topic?id=8052 — Edge Functions GA
- https://news.hada.io/topic?id=9430 — Vercel AI SDK 공개
- https://news.hada.io/topic?id=17884 — Vercel Grep 인수
- https://www.indiehackers.com/product/mdx-one/huge-vercel-costs-and-rebrand-to-feather--Myc071NF66jYxLB2yED
- https://journeywithibrahim.medium.com/vercel-bill-shock-from-700-to-120-ec24ee9755c3
- https://www.howdygo.com/blog/cutting-howdygos-vercel-costs-by-80-without-compromising-ux-or-dx
- https://eduardoboucas.com/posts/2025-03-25-you-should-know-this-before-choosing-nextjs/
- https://richardkovacs.dev/blog/bring-your-own-nextjs
- https://dev.to/rbobr/self-hosting-nextjs-what-you-gain-and-lose-vs-vercel-4g8c
- https://eastondev.com/blog/en/posts/dev/20251220-nextjs-docker-self-hosting/

## 수집 한계

- Discord 공개 로그·KakaoTalk 오픈채팅의 한국어 1차 사례는 접근 불가.
- Reddit thread 일부는 검색 결과로만 노출, 상세 댓글은 미수집.
- "Vercel 망함 이야기"의 일차 트윗·X 포스트는 검색 엔진에서 잘 잡히지 않음. WebSearch가 X·Threads에 약함.
- 한국 커뮤니티에서 비용 폭탄을 직접 다룬 글은 거의 없음 (대부분 영어권 사례 인용/번역).
