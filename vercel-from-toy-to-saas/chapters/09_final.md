# 9장. 함정·대안·비상 탈출 — 의심하는 법

## 9.1 잘 쓰는 것과 떠날 수 있는 것은 다르다

여기까지 같이 왔다. 1장에서 새벽 두 시의 황홀함과 그 다음 한 시간의 막막함을 환기했고, 2장에서 추상화 지도를 그렸다. 3·4·5·6장은 토이부터 SaaS까지 단계마다 무엇을 켜고 무엇을 분리하는지 살폈고, 7장과 8장에서는 흩어진 비용·보안 메모를 한 자리에 모아 결판을 봤다. 그동안 이 책은 줄곧 "어떻게 잘 쓰는가"를 물었다.

이제 톤을 한 번 바꿔보자. 마지막 장은 비판하기 위한 장이 아니다. **잘 쓰는 능력과 떠날 수 있는 능력은 다른 능력이다**, 라는 한 문장에서 시작한다. 잘 쓰는 능력만 가진 개발자는 의외로 많다. 화려한 기능을 다 켤 줄 알고, 청구서가 좀 늘어도 어디서 새는지 찍어낼 수 있다. 그런데 "어느 날 Vercel을 떠나야 한다고 해보자"라는 가정 앞에서는 갑자기 막막해진다. 어디서부터 무엇을 어떻게 옮기는지, 무엇을 잃고 무엇을 살릴 수 있는지, 그 비용이 얼마인지, 1차 자료 없이 답할 수 있는 사람이 드물다.

떠날 수 있는 능력은 평소에 길러두는 것이지 떠나야 하는 날 갑자기 익히는 것이 아니다. 그래서 이 장의 제목은 "의심하는 법"이다. 비판이라는 단어보다는 거리두기라는 단어가 더 맞는다. 지금 잘 쓰고 있는 도구를 *조금 떨어진 자리에서* 다시 한번 보자. 어디까지가 진짜 종속이고, 어디는 그저 익숙해진 것뿐인가. 어떤 함정이 자주 발을 거는가. 다른 길은 어디 있고, 그 길의 풍경은 어떤가. 비상 탈출은 어떻게 평소의 손에 둘 수 있는가.

이 장을 다 읽고 나면, 1장에서 던진 네 번째 큰 질문 — "Vercel을 잘 쓰면서도 언제든 떠날 수 있는 능력은 어떻게 갖추는가" — 에 자기 언어로 답할 수 있게 될 것이다. 그 답이 모이면, 마지막 절에서 책의 첫 새벽으로 한번 더 돌아간다.

## 9.2 자주 빠지는 함정 — 한 페이지에 모아서

함정은 운영 의식의 거울이다. 어디서 자주 발이 걸리는지 보면, 자기가 어떤 추상화를 흐릿하게 두고 살았는지 그대로 드러난다. 단계 챕터를 지나오는 동안 일부는 이미 만났다. 이 절에서는 흩어진 함정을 한 자리에 모으고, 2장에서 미뤄뒀던 두 함정 — ISR `revalidate` 오해와 Edge Node API 제약 — 의 결판을 본다.

### 런타임 한도 — 25초·300초·800초·4.5MB

가장 먼저 외워둬야 하는 숫자가 몇 개 있다. Edge runtime은 25초 안에 응답을 시작해야 하고, 스트리밍은 최대 300초까지다. Node runtime은 Pro Fluid에서 max duration을 800초까지 늘릴 수 있다. 그리고 함수 응답·요청 body는 4.5MB가 한도다.[^limits] 이 네 숫자는 실수로 부딪치면 디버깅이 꽤 난감하다. 특히 4.5MB body 한도는 파일 업로드를 함수로 직접 받는 코드에서 자주 발이 걸린다. 큰 파일은 함수를 거치지 않고 클라이언트가 Blob 같은 외부 스토리지로 직접 업로드하게 두는 편이 낫다.

[^limits]: <https://vercel.com/docs/limits>, <https://vercel.com/docs/functions/limitations>

### Cold Start — 0이 되지는 않는다

Fluid compute가 cold start 영향을 크게 줄였다는 발표는 사실이다. 단일 인스턴스가 다중 요청을 동시에 처리하니, 새 인스턴스를 띄울 일이 줄어드는 게 당연하다. 그런데 0이 되는 것은 아니다. 학계 메타분석은 cold start가 first invocation의 50–90% latency를 차지한다고 본다.[^mahmoudi] Fluid는 이 비율을 낮추지만 없애지는 않는다. AI 에이전트처럼 첫 응답이 사용자에게 곧장 보이는 워크로드라면, "처음 한 번은 좀 느릴 수도 있다"는 사실을 UX에 반영하는 편이 낫다. 로딩 상태를 더 빨리 노출하거나, warm-up ping을 cron으로 한 번 돌리거나.

[^mahmoudi]: Mahmoudi et al., "A Systematic Review on Cold Start in Serverless Computing," ACM Computing Surveys 2024. <https://dl.acm.org/doi/abs/10.1145/3700875>

### Turborepo 캐시 invalidation — 잘못된 적중이 무섭다

모노레포에서 Turborepo Remote Cache는 빌드 시간을 절반 이상 줄여준다. 이 절감 자체에 의심을 품을 일은 별로 없다. 진짜 함정은 invalidation key 설정이다. 환경 변수나 외부 파일 의존성이 키에 빠져 있으면, *내용이 바뀐 빌드인데 옛 캐시가 적중*해 잘못된 산출물이 production으로 나가는 사고가 가능하다. CI 캐시 디버깅이 헷갈릴 때는 `vercel build --debug`로 어떤 키가 어떻게 잡히는지부터 본다. 빌드가 빨라졌다고 좋아할 일이 아니라, 빨라진 만큼 검증의 책임이 늘었다고 생각하는 편이 낫다.

### ISR `revalidate` — 2장에서 미뤄뒀던 오해

`export const revalidate = 60` 한 줄을 보고 "60초마다 자동으로 재생성된다"라고 읽는 독자가 흔하다. 솔직히 영어 문장으로도 그렇게 읽힌다. 그런데 정확히는 **"60초가 지난 뒤 그 다음 요청이 들어오면 백그라운드에서 재생성하고, 그 요청은 일단 stale을 받는다"**이다.[^isr] 이 메커니즘의 뿌리는 1990년대로 거슬러 올라가는 RFC 5861의 `stale-while-revalidate`다.[^rfc5861] 즉, ISR은 Vercel의 발명품이라기보다 오래된 HTTP 의미론을 framework 레벨로 통합한 것이다.

[^isr]: <https://vercel.com/docs/incremental-static-regeneration>
[^rfc5861]: RFC 5861, "HTTP Cache-Control Extensions for Stale Content." <https://datatracker.ietf.org/doc/html/rfc5861>

이 사실은 두 가지를 바꾼다. 첫째, 60초 주기를 짧게 잡았다고 해서 트래픽이 없는 페이지가 자기 알아서 갱신되는 건 아니다. 요청이 와야 갱신이 일어난다. 둘째, 데이터 정합성이 즉시 필요한 자리 — 결제 직후 주문 페이지, 관리자가 방금 바꾼 콘텐츠 — 에서는 시간 기반 revalidate를 믿으면 안 된다. `revalidateTag`나 `revalidatePath`로 on-demand 갱신을 호출하는 편이 낫다. 시간은 보조 신호고, 이벤트가 주 신호다.

### Edge runtime의 Node API 제약 — pdfkit·sharp·bcrypt가 안 되는 이유

이것도 2장에서 미뤄뒀던 함정이다. Edge runtime은 글로벌 분산이 매력이지만 Node API의 거의 전부가 막혀 있다. filesystem 접근 불가, `require()` 직접 호출 불가, fetch·crypto.subtle·Web Streams 정도만 가능하다고 가정하고 시작하는 편이 안전하다.[^edge] 그래서 pdfkit으로 PDF를 만들거나, sharp로 이미지를 리사이즈하거나, bcrypt로 비밀번호를 해시하려는 라이브러리는 import 자체가 실패한다. AWS SDK v2도 같은 운명이다.

[^edge]: <https://vercel.com/docs/functions/limitations>

여기서 흔히 빠지는 함정은 *처음에는 fetch만 쓰던 함수에 어느 날 sharp 한 줄이 추가되면서* 빌드가 무너지는 시나리오다. "Edge runtime을 default로 둔 것" 자체가 후일의 발목을 잡는다. 무거운 처리가 들어올 가능성이 있는 라우트는 처음부터 Node runtime을 default로 두자. Edge는 진짜로 fetch와 헤더 조작만 쓰는 가벼운 라우트, 또는 글로벌 분산이 사용자 체감에 직결되는 자리에 한정하는 편이 낫다.

### 한 줄 요약

다섯 함정을 한 줄씩으로 정리하면 이렇다.

| 함정 | 한 줄 |
|------|------|
| 런타임 한도 | 25/300/800초·4.5MB body — 큰 파일은 외부 스토리지에 직접 |
| Cold Start | Fluid도 0이 되진 않는다 — 첫 응답 UX를 따로 챙기자 |
| Turborepo 캐시 | 빨라진 만큼 invalidation key 검증 책임이 늘었다 |
| ISR `revalidate` | 시간이 아니라 이벤트로 갱신을 트리거하는 편이 낫다 |
| Edge Node API | sharp·pdfkit·bcrypt는 import부터 막힌다 — Node runtime이 default |

함정을 외우려고 들지 말고, 함정이 어디에서 *왜* 생기는지 한 번 생각해보면 어떨까. 런타임 한도는 서버리스 격리의 본성에서, ISR 오해는 RFC 5861의 의미론에서, Edge 제약은 V8 isolate가 Node가 아니라는 사실에서 온다. 본성을 한 번 잡아두면 Vercel을 떠나서도 같은 직관이 따라붙는다. 그게 의심하는 법의 첫 번째 의미다.

## 9.3 Vendor Lock-in 논쟁 — 두 관점을 같이 들어보자

"Vercel을 쓰면 Next.js에 묶이고, Next.js를 쓰면 Vercel에 묶인다"는 말은 커뮤니티에서 꾸준히 도는 말이다. 이게 정말 lock-in인가? 그렇다면 어디까지가 lock-in이고 어디부터는 그저 익숙함인가? 이 질문에는 권위 있는 두 관점이 나란히 있다. 양쪽을 같이 들어두는 편이 낫다.

### 관점 A — "사실상 종속이다"

Eduardo Bouças는 Next.js를 쓰기 전에 알아둘 것을 정리한 글에서, "Next.js는 Vercel이 만든 Build Output API를 자기 자신은 지원하지 않는다"라고 지적한다.[^edu] 같은 회사에서 만든 두 제품인데, 한쪽이 다른 쪽의 표준을 채택하지 않는 모양새다. 자기호스팅을 시도해본 dev.to의 분석에서도 비슷한 결이 잡힌다 — ISR, Image Optimization, Edge Middleware, PPR이 Vercel에서 best, 사실상 only로 작동하고, 다른 플랫폼으로 옮기면 reduced fidelity를 감수해야 한다는 평이다.[^rbobr]

[^edu]: <https://eduardoboucas.com/posts/2025-03-25-you-should-know-this-before-choosing-nextjs/>
[^rbobr]: <https://dev.to/rbobr/self-hosting-nextjs-what-you-gain-and-lose-vs-vercel-4g8c>

이 관점에서 보면, "Next.js를 쓴다"는 결정은 "Vercel을 첫 후보로 둔다"는 결정과 거의 같은 무게다. 다른 플랫폼에서 돌릴 수는 있지만, Vercel에서만큼 깔끔하지 않다. 그래서 종속이라는 단어가 자연스럽다.

### 관점 B — "70%가 외부에서 운영된다"

Vercel은 자기 블로그에서 정반대 입장을 낸다. "anti-vendor lock-in cloud"라는 제목의 글에서, "Next.js 애플리케이션의 약 70%가 Vercel 외부에서 운영된다"는 데이터를 인용한다.[^anti] Walmart.com, Nike.com, Claude.ai 같은 굵직한 사례가 self-host 또는 다른 플랫폼에서 Next.js를 돌리는 자리로 거론된다.

[^anti]: <https://vercel.com/blog/vercel-the-anti-vendor-lock-in-cloud>

흥미로운 변수는 Next.js 16.2의 stable Adapter API다. Cloudflare·Netlify·AWS Amplify·Google·OpenNext가 공동 설계에 참여했다고 발표됐다.[^adapter] Adapter API가 안정화되면 "Next.js의 모든 기능을 다 쓰는데 Vercel이 아닌 곳에서 돌아간다"는 시나리오가 점점 현실에 가까워진다. 이 흐름까지 보면, "사실상 종속"은 *어제까지의* 사실에 가깝다.

[^adapter]: <https://nextjs.org/blog/nextjs-across-platforms>

### 어느 쪽이 옳은가

둘 다 옳다, 라고 말하면 좀 회피하는 답 같지만 솔직히 그게 맞다. *Vercel-only 기능을 풀 셋으로 쓰는 자리*에서는 관점 A가 맞고, *Next.js 자체의 기본기와 보편적 기능만 쓰는 자리*에서는 관점 B가 맞다. 그래서 lock-in 논쟁의 진짜 질문은 "Next.js가 Vercel에 묶여 있는가"가 아니라 "내 프로젝트는 Vercel-only 기능을 어디까지 깊게 쓰고 있는가"가 된다.

이 질문을 자주 자기에게 던져보자. ISR을 정말로 풀 기능으로 의존하는가, 아니면 그냥 SSG와 SSR의 중간이 필요한가. Image Optimization이 핵심 가치인가, 아니면 외부 CDN으로 대체해도 되는가. PPR이 사용자 체감을 정말로 바꾸는가, 아니면 SSG로 충분한가. 답이 후자에 가까울수록 자기 프로젝트는 Vercel-friendly이지 Vercel-bound는 아니다. 떠날 수 있는 능력은 거기서부터 자란다.

## 9.4 대안 — 한 줄 매트릭스로 풍경 잡기

Vercel을 떠난다고 했을 때 어디로 갈 수 있는지, 그 풍경부터 한 번 훑어보자. 정확한 가격이나 깊은 비교는 책 한 권을 따로 써야 할 분량이다. 여기서는 *한 줄씩*만 본다. 한 줄로도 자기 프로젝트와 어느 후보가 결이 맞는지 윤곽이 잡힌다.

| 플랫폼 | 강점 | 약점 | 적합 시점 |
|--------|------|------|-----------|
| Vercel | DX 1위, Next.js 통합, preview, AI Gateway | bandwidth 비쌈, 청구 폭증 위험 | 초기·중간 단계 Next.js 팀 |
| Cloudflare Pages/Workers | 300+ PoP, 무제한 bandwidth, $5 Pro | DX 살짝 낮음, Next.js 풀 기능은 OpenNext 의존 | 글로벌 트래픽이 큰 사이트 |
| Netlify | DX 양호, 정적 사이트 강함 | 일반 목적 경쟁력 약화 | 정적 마케팅·docs |
| AWS Amplify | 인증·DB·API 통합, SOC 2/HIPAA | AWS 학습곡선 | AWS 생태계·풀스택 |
| Render | Heroku 후계자, 백그라운드 워커 | 글로벌 edge 약함 | 전통적 백엔드+프론트 |
| Fly.io | Docker + 글로벌 edge | 인프라 지식 필요 | low-latency 글로벌 서비스 |
| 자가호스팅 (Coolify·Dokku·CapRover) | 완전한 통제, 비용 예측 | 운영 부담 | 비용·컴플라이언스 압박 |

출처는 DigitalOcean·Qovery·DanubeData·agilesoftlabs·selfhostable.dev의 2026년 비교 자료를 기준으로 했다.[^alt-sources] 가격과 기능은 빠르게 변하니, 결정 직전에 직접 한 번 더 검증하는 편이 낫다.

[^alt-sources]: <https://www.digitalocean.com/resources/articles/vercel-alternatives>, <https://www.qovery.com/blog/vercel-alternatives>, <https://danubedata.ro/blog/cloudflare-pages-vs-netlify-vs-vercel-static-hosting-2026>, <https://www.agilesoftlabs.com/blog/2026/01/aws-amplify-vs-vercel-2026-complete>, <https://selfhostable.dev/blog/coolify-vs-caprover-vs-dokku/>

표를 자세히 들여다볼 필요는 없다. 풍경만 잡자. 이 풍경에서 두 가지가 보이면 충분하다. 첫째, 후보가 적지 않다. 둘째, 후보마다 강점과 약점이 *대칭적으로* 갈린다. Vercel이 일등인 자리가 있고 꼴찌인 자리가 있다. Cloudflare가 일등인 자리가 있고, Render가 일등인 자리가 있다. 자기 프로젝트가 어떤 자리에 서 있는지를 보고 후보를 뽑는 거지, "최고의 플랫폼"을 찾으려고 들면 영영 답이 안 나온다.

### 결정 휴리스틱 — 네 줄로 좁히기

매트릭스를 다 외울 필요는 없다. 네 줄로 좁혀도 거의 답이 나온다.

- 글로벌 트래픽이 큰 비중이고 bandwidth가 부담이다 → **Cloudflare**
- 이미 AWS 생태계 안에 살고 있고 풀스택 통합이 필요하다 → **AWS Amplify**
- 비용 예측 가능성과 완전한 통제가 무엇보다 중요하다 → **자가호스팅 + Coolify**
- Next.js의 모든 기능을 즉시 쓰고 싶고 시간이 돈이다 → **Vercel**

이 네 줄 중 하나에 자기 프로젝트가 깔끔하게 들어맞으면, 후보는 거의 정해진 셈이다. 두 줄에 걸쳐 있다면 그 둘을 단계 단위로 다시 한 번 따져보자. 예컨대 초기 SaaS는 Vercel로 가다가 트래픽이 글로벌하게 커지면 Cloudflare 앞단을 붙이는 길이 있다(이건 5장에서 이미 봤다). "전부 또는 전무"가 아니라 *섞어 쓰는* 전술이 의외로 자주 답이 된다.

## 9.5 Next.js 16.2 stable Adapter API가 바꾼 풍경

위에서 잠깐 언급한 Next.js 16.2의 Adapter API는 따로 한 절을 둘 만큼 풍경을 바꾼다. 좀 차분히 짚어보자.

지금까지 Next.js를 다른 플랫폼에서 돌리려면 각 플랫폼이 *각자* 어댑터를 만들어야 했다. Cloudflare는 OpenNext for Cloudflare를, Netlify는 자기 플러그인을, Amplify는 자기 SSR 통합을. 각자 만든 어댑터는 새 Next.js 기능이 나올 때마다 따라가야 했고, 그 사이에 reduced fidelity가 발생했다. ISR이 동작하긴 하지만 fidelity가 떨어진다거나, Middleware의 일부 동작이 다르다거나.

Next.js 16.2에서 Adapter API가 stable로 올라가면서, **Cloudflare·Netlify·Amplify·Google·OpenNext가 공동 설계에 참여한 단일 인터페이스**가 생겼다.[^adapter2] 한쪽이 어댑터를 따라잡는 게 아니라, 양쪽이 같은 약속 위에서 만나는 모양이 됐다. Vercel은 자기 블로그에서 이 변화를 anti-lock-in의 핵심 증거로 인용한다.[^anti2]

[^adapter2]: <https://nextjs.org/blog/nextjs-across-platforms>
[^anti2]: <https://vercel.com/blog/vercel-the-anti-vendor-lock-in-cloud>

이게 의미하는 바를 한 문단으로 정리해보자. Adapter API stable 이후의 세계에서는 "Next.js를 다른 플랫폼에서 돌리는 것"이 점점 *예외 사례*가 아니라 *정상 사례*로 정착한다. 새 기능이 Vercel에서 먼저 작동하더라도, Adapter API 위에서 다른 플랫폼이 따라잡는 시간 차가 줄어든다. Cloudflare가 자기 블로그에서 "AI로 1주만에 Next.js를 Workers에 포팅했다"라고 발표한 사례도 같은 맥락 위에 있다.[^vinext] 어댑터가 표준화되니, 마이그레이션의 인지적 부담 자체가 낮아지는 흐름이다.

[^vinext]: <https://blog.cloudflare.com/vinext/>

Adapter API stable이 의미하는 또 하나는 *OpenNext의 위상 변화*다.

## 9.6 OpenNext의 위치와 한계

OpenNext는 Next.js를 Vercel 외부에서 돌리기 위한 오픈 소스 어댑터 프로젝트다. Cloudflare, AWS, Netlify 등 여러 환경을 타겟으로 한다.[^opennext] Adapter API stable 흐름에서 OpenNext는 더 이상 "비공식 우회로"가 아니라, Next.js 공식 생태계의 한 축에 가까워졌다.

[^opennext]: <https://opennext.js.org/>

OpenNext가 선물하는 것은 분명하다. `output: "standalone"`보다 한 단계 더 나아가, ISR이나 Middleware 같은 기능을 다른 플랫폼에서 *비교적 충실하게* 돌릴 수 있게 해준다. Cloudflare for Next.js 어댑터가 OpenNext 위에 올라가 있고, AWS Lambda 타겟도 성숙해 있다.

다만 OpenNext에도 한계는 있다. Image Optimization, ISR, Middleware 셋은 여전히 "reduced fidelity"라는 단서가 붙는다.[^selfhost] Image Optimization은 Vercel의 on-the-fly 변환이 가지는 정확한 캐싱 동작과 1:1 대응이 어렵고, ISR도 캐시 백엔드에 따라 동작이 살짝 달라질 수 있다. Middleware는 Edge Middleware 특유의 메타데이터 주입(BotID 같은) 동작이 환경에 따라 빠질 수 있다.

[^selfhost]: <https://nextjs.org/docs/app/guides/self-hosting>

이 한계를 어떻게 받아들이는 편이 좋을까. "OpenNext로 가면 몇 가지를 잃는다"가 아니라 "OpenNext는 *내가 정말 풀 기능으로 의존하는 게 무엇인지* 다시 묻게 해주는 도구"라고 보는 편이 낫다. 막상 옮겨보면, 풀 기능으로 의존하는 게 별로 없는 프로젝트가 많다. 의존이 깊은 자리에서만 fidelity 격차가 아프고, 그 외의 자리에서는 충분하다. 이 진단을 평소에 한 번 해두는 것 자체가 떠날 수 있는 능력의 절반이다.

## 9.7 Edge가 정말 빠른가 — 조건부 논쟁

"Edge runtime은 빠르다." 이 말은 마케팅 카피에서 자주 본다. 사실인가? 이걸 둘로 나눠 보자.

### 조건이 맞으면 빠르다

정적 자산, 짧은 처리, 데이터가 edge 캐시에 있는 시나리오 — 여기서는 Edge가 분명히 빠르다. TTFB 50ms 미만이 글로벌하게 균질하게 나온다는 보고가 흔하다.[^danube] 사용자가 어디 있든 가까운 PoP에서 응답이 나가니, 한 region에 묶인 서버보다 latency가 안정적이다.

[^danube]: <https://danubedata.ro/blog/cloudflare-pages-vs-netlify-vs-vercel-static-hosting-2026>

### 조건이 어긋나면 더 느릴 수도 있다

문제는 데이터베이스다. DB가 한 region에 있는데 함수가 글로벌 edge에 분산되면, 사용자 가까운 edge에서 멀리 있는 DB까지 round trip을 한 번씩 한다. PoP가 사용자에게 1ms로 가까워도, DB까지 100ms 걸리면 *합계*는 한 region에 모아둔 것보다 *느려질 수도* 있다.

이건 직관에 약간 반하는 결과다. 학술적으로 이 현상은 **placement-cost-latency triangle**로 정리된다.[^cassel] 캐시·연산·데이터를 어디에 두느냐의 삼각관계에서, 한 꼭짓점을 가깝게 만들면 다른 꼭짓점이 멀어진다는 본성이 있다. Pinto 외(2023)의 실측 분석은 흥미로운 경향을 추가로 보여준다 — *짧은 요청*에서는 cloud serverless가 우위, *1초 이상이 걸리는 처리*에서는 edge가 우위라는 것이다.[^pinto] 짧은 처리에서는 cold start와 데이터 round trip의 영향이 상대적으로 크게 잡혀, edge의 latency 이점이 가려진다.

[^cassel]: Cassel et al., "A Taxonomy for Serverless Computing at the Edge," arXiv 2025. <https://arxiv.org/html/2502.15775v1>
[^pinto]: Pinto et al., "Latency and Resource Consumption Analysis at the Edge," Journal of Cloud Computing 2023. <https://journalofcloudcomputing.springeropen.com/articles/10.1186/s13677-023-00485-9>

### 자기 프로젝트의 답

그러니 "Edge로 옮기면 빨라진다"라는 가정은 *조건 점검 없이* 받아들이지 않는 편이 낫다. 자기 프로젝트의 데이터가 어디 있는지, 함수의 처리가 짧은지 긴지, 사용자 분포가 글로벌인지 한 region에 몰려 있는지 — 이 세 가지를 한 번 그려보자. 데이터가 한 region에 있고 사용자도 한 region에 몰려 있다면 Edge runtime이 손해일 수 있다. 데이터가 Edge Config나 글로벌 KV에 분산되어 있고 사용자도 글로벌하다면 Edge가 빛난다. 둘 사이의 회색 지대가 가장 흔하고, 거기서는 실측 한 번이 추정 열 번보다 낫다.

## 9.8 비상 탈출 빌드 — 평소에 손에 두기

여기서 잠시 손을 움직여보자. 이 책에서 가장 묵직한 한 줄이 될지도 모르는 명령이다.

```js
// next.config.js
module.exports = {
  output: "standalone",
};
```

`output: "standalone"`은 Next.js가 "최소한의 파일만 모은 self-contained 번들"을 만들도록 시키는 옵션이다. 실행에 필요한 최소 의존성만 추출하니, Docker 이미지가 보통 100–200MB 안에 들어간다.[^standalone] 그 다음은 흔한 두세 줄의 Dockerfile이고, 어디든 — Render, Fly.io, AWS, Coolify 위의 자기 VPS — 올릴 수 있다.

[^standalone]: <https://nextjs.org/docs/app/guides/self-hosting>

이 빌드는 평소에 손에 두는 편이 낫다. 왜냐하면 "비상 탈출이 필요한 날"은 보통 평정심이 가장 부족한 날이기 때문이다. 청구서가 폭발했거나, ToS 분쟁이 생겼거나, 보안 사고가 막 터진 직후거나. 그 자리에서 Dockerfile을 처음 짜고, 환경 변수 마이그레이션 스크립트를 처음 만들고, ISR 캐시 백엔드를 어떻게 옮길지 처음 고민하기 시작하면 — 솔직히 막막하다. 혼자서는 한 주가 그냥 간다.

그래서 분기에 한 번씩, 또는 새 큰 기능을 production에 띄울 때 한 번씩, `output: "standalone"`으로 빌드를 돌려보고 로컬 Docker로 한번 띄워보자. ISR이 어떻게 동작하는지, Image Optimization이 어떤 fidelity로 작동하는지, Middleware가 어떻게 따라오는지 — 한 번씩 눈으로 본다. 이걸 *드릴*이라고 부르고 싶다. 비상 대응 훈련이다. 평소에 익숙해진 손은 비상시에 떨지 않는다.

이 드릴이 주는 부가 효과가 하나 더 있다. 자기 프로젝트가 *진짜로* Vercel-only 기능에 얼마나 의존하는지를 매번 체크하게 된다. 어느 분기 빌드는 거의 무탈하게 standalone으로 돈다. 어느 분기 빌드는 ISR 백엔드를 못 찾아 stuck된다. 그 차이가 "내 프로젝트가 그 사이에 어디로 흘러갔는지"를 정직하게 보여준다.

## 9.9 학술 백본 한 페이지 — 직관을 일반화하기

이 책은 입문서지만, 입문자에게도 학술 한 페이지는 필요하다. 왜냐하면 학술적 근거는 *Vercel을 떠나도 따라오는 직관*이 되기 때문이다. 이 절에서는 책 곳곳에서 잠시 인용했던 논문들을 한 자리에 모아본다.

**Mahmoudi 외 (2024) — Cold Start 메타분석.** 100여 편의 cold start 연구를 메타분석한 ACM Computing Surveys 논문이다.[^mahmoudi2] 이 논문이 정리한 두 가지 진실이 책 전체에 깔려 있다. 첫째, cold start는 first invocation의 50–90% latency를 차지한다 — 그래서 0이 되지는 않는다는 사실이 무겁다. 둘째, cold start 완화 기법은 caching, application-level optimization, hardware-level optimization 셋으로 분류되며, Fluid compute는 그중 첫 두 갈래의 제품화에 가깝다. Fluid가 "Vercel만의 마법"이 아니라 *오래된 직관의 잘 만든 구현*이라는 시선이, 이 직관을 다른 플랫폼으로 옮길 때도 따라오게 만든다.

[^mahmoudi2]: <https://dl.acm.org/doi/abs/10.1145/3700875>

**RFC 5861 — `stale-while-revalidate`.** ISR과 PPR이 발명품이 아니라는 말을 위에서 했다. 그 뿌리가 RFC 5861이다.[^rfc] HTTP 캐싱 의미론에 stale-while-revalidate라는 directive가 들어간 것이 2010년이다. ISR은 이 directive를 framework 레벨로 통합한 것이고, PPR은 한 응답 *안*에서 stale shell과 fresh holes를 결합한 것이다. 직관 자체는 HTTP 캐싱을 깊게 이해한 사람이 다음 단계로 자연스럽게 도달한 자리에 있다.

[^rfc]: <https://datatracker.ietf.org/doc/html/rfc5861>

**Firecracker microVM — NSDI '20.** Vercel 함수의 *바닥*에는 AWS Lambda가 있고, Lambda의 바닥에는 Firecracker microVM이 있다. NSDI '20에서 발표된 Agache 외의 논문은 이 microVM이 어떻게 가벼운 격리와 빠른 부팅을 동시에 달성하는지 설명한다. 함수 한도(25/300/800초·4.5MB body)의 본성이 microVM의 격리 모델에서 오는 거라는 점을 한 번 잡아두면, *왜 그 한도가 그렇게 생겼는지*가 갑자기 자연스러워진다. 이건 Vercel 문서를 외워서 얻는 직관이 아니다.

이 한 페이지가 직접 자기 일에 쓰일 일은 적을지도 모른다. 그러나 직관의 *밑변*을 깔아두는 효과가 크다. 누군가 "Vercel은 어떻게 그렇게 잘 돌아가요?"라고 물었을 때, "잘 만들어서요"가 아니라 "이런 오래된 시스템 연구의 잘 정착된 결과예요"라고 답할 수 있다면, 그 사람은 더 이상 마법에 매혹되지 않는다. 의심하는 법은 거기서 한 단계 깊어진다.

## 9.10 그래도 Vercel이 빛나는 자리

여기까지 왔으니, 의심하는 일은 충분히 한 셈이다. 비판으로만 닫지 않으려면 한 절을 따로 두어야 한다. **Vercel이 정말로 빛나는 자리**가 어디인지, 같은 거리감으로 한번 보자.

### Claude.ai를 운영하는 자리

Anthropic의 Claude.ai는 Vercel 자체 사례 인용에 자주 등장한다.[^anti3] 흥미로운 사실은 *Anthropic이 Vercel을 안 쓸 능력이 없어서가 아니라는* 점이다. 수십 명의 인프라 엔지니어가 있는 회사가 Vercel을 선택했다는 건, 적어도 *어떤 자리*에서는 자기 인프라를 직접 굴리는 것보다 Vercel이 합리적이라는 신호로 읽힌다. 그 자리가 어디인지 한 번 짚어보면, 빠른 frontend iteration, preview-driven QA, 글로벌 분산 — 흔히 인프라 팀이 "직접 만들면 한 분기는 가져갈" 자리들이다.

[^anti3]: <https://vercel.com/blog/vercel-the-anti-vendor-lock-in-cloud>

### AI Gateway가 한 줄로 해결하는 것

5장에서 이미 다뤘지만 한 번 더 짚자. AI Gateway는 OpenAI, Google Imagen, Black Forest Labs Flux, Recraft 같은 다수 모델을 *단일 API*로 라우팅한다.[^aigw] 인증·응답 포맷·재시도·로깅이 한 번에 묶인다. 이걸 직접 짜본 사람은 안다 — provider별 SDK 차이, response 포맷 차이, rate limit 차이를 손으로 흡수하는 데 들어가는 시간이 얼마나 끔찍한지. AI Gateway가 그 시간을 *한 줄*로 줄인다. 가격 마진의 투명도에 비판이 있고 그 비판은 정당하지만, DX의 합리성이 사라지는 건 아니다.

[^aigw]: <https://vercel.com/docs/ai-gateway/capabilities/image-generation/ai-sdk>

### PPR — 50ms 미만 TTFB와 부분 동적성

PPR (Partial Prerendering)은 Next.js 15에서 stable, Next.js 16에서 cacheComponents flag의 기본값으로 들어온 렌더링 전략이다.[^ppr] 정적 shell을 미리 렌더하고, 동적 부분만 Suspense holes로 남겨, 한 응답에 둘을 결합한다. 이 모델의 의의는 한 줄로 요약된다 — **50ms 미만 TTFB와 부분 동적성을 동시에 달성하는 첫 모델**이라는 평. SSG의 속도와 SSR의 동적성을 한 응답에서 합치는 시도다.

[^ppr]: <https://nextjs.org/docs/app/guides/ppr-platform-guide>

PPR은 다른 플랫폼에서도 도전 중이지만, *가장 먼저, 가장 깊이* 통합된 자리는 Vercel이다. RFC 5861의 의미론을 framework 레벨로 한 번 통합한 것이 ISR이라면, PPR은 그 의미론을 *한 응답 안*으로 한 번 더 끌어들인 자리에 있다. 입문자 입장에서 PPR을 직접 쓸 일은 아직 적을지도 모르지만, "이런 자리에서 Vercel이 한 발 앞서간다"는 사실 자체는 인정해두는 편이 정직하다.

### 균형 — 비판도 옹호도, 거리감 안에서

이 절을 두는 이유는 비판에 대칭으로 옹호 한 토막을 두기 위함이 아니다. **거리감이라는 단어를 양쪽 모두에 적용하기 위함**이다. 비판도 거리감 안에서, 옹호도 거리감 안에서. Vercel을 *마법처럼* 칭송하는 자리에서도, *부도덕한 lock-in*으로 묘사하는 자리에서도 거리를 두자. 두 시선 모두 자기 프로젝트의 의사결정에는 별로 도움이 안 된다. 도움이 되는 건 자기 프로젝트의 단계와 자리를 잡고, 그 위에서 Vercel이 *지금* 빛나는지 *지금* 부담스러운지를 차분히 가늠하는 일이다.

## 9.11 기준 시점 환기 — 이 책의 내용은 변한다

마지막 절로 가기 전에 한 단락을 비워둔다. 1장에서도 같은 약속을 했지만, 마지막 장에서 한 번 더 짚는 게 무겁지 않다.

이 책의 **기준 시점은 2026년 5월**이다. Vercel의 가격, 한도, 기본값, 새 기능, 사고 사례 — 어느 하나도 그대로 멈춰 있지 않다. 책이 출간되는 시점, 그리고 독자가 이 책을 펼치는 시점에 어떤 항목은 이미 바뀌었을 것이다. 그래서 책 곳곳에서 *공식 문서 URL*을 1차 출처로 함께 적어뒀다. 결정 직전에는 그 URL을 한 번 더 클릭해보는 편이 낫다. 책이 답하는 것은 *방법론*과 *직관*이고, 책이 답할 수 없는 것은 *지금 이 순간의 가격*이다.

가격·기능·기본값은 변한다. 변하지 않는 건 자기 프로젝트의 단계를 진단하고, 켜야 할 가드레일을 켜고, 떠날 수 있는 능력을 평소에 손에 두는 *습관*이다. 책이 남기고 싶은 건 그쪽이다.

## 9.12 닫는 글: 다시 그 새벽으로 — 같은 한 줄, 다른 무게

다시 새벽 두 시로 돌아가 보자.

며칠을 붙들고 있던 사이드 프로젝트가 드디어 로컬에서 돌아간다. 커피는 식었고 책상은 어지럽다. 이 정도면 됐다. 한번 띄워나 보자, 싶어 터미널에 한 줄을 친다.

```
$ vercel deploy
```

5분도 채 지나지 않아 `https://my-thing-xxxxxx.vercel.app` 같은 URL 한 줄이 떨어진다. 클릭한다. 켜진다. SSL 자물쇠도 이미 박혀 있다.

같은 한 줄이다. 그런데 이번에는 그 한 줄 뒤에 보이는 풍경이 다르다.

이 명령이 어떤 결정을 *대신* 내려주는지 안다. 빌드 컨테이너의 region, 어디까지 캐시가 깔리는지, SSL을 누구에게 발급받는지, preview URL이 어떻게 만들어지는지 — 다 결정이 *내려진* 거지 결정이 *없는* 게 아니라는 것을 안다. 그 결정들은 Frontend Cloud라는 한 단어 뒤에 매니지드 PaaS의 모양으로 묶여 있다. Git push 한 번에 빌드·배포·CDN·SSL·preview·서버리스 함수가 한꺼번에 따라온다. 2장에서 그렸던 추상화 지도가 이제 머릿속에 한 장으로 자리잡혀 있다.

그 다음 한 시간도 다르다.

OAuth 키를 어디 둘지 망설이지 않는다. Sensitive 플래그를 켜야 할 자리는 켜고, non-sensitive로 둘 자리는 둔다. 8장에서 배운 사고 해부가 그 결정을 가볍게 만들어준다. 도메인을 붙일 때는 외부 등록 도메인의 갱신을 누가 챙길지 같이 생각한다. cron을 켤 때는 함수 quota를 차감한다는 비용 함의가 한 번 깜빡 떠오른다. Pricing 페이지를 봐도 GB-hour라는 단어가 무섭지 않다. 함수 과금 3축이 손에 잡혀 있고, 7장에서 손계산을 한 번 해봤다.

토이라면 결제 카드를 *일부러* 등록하지 않는 가드레일을 둔다. 사이드라면 만들자마자 Spend Management를 켠다. 스타트업이면 이미지를 외부 CDN으로 분리하고 Cloudflare 앞단을 한 번 더 진지하게 본다. SaaS면 함수 런타임 3종 중 어디에 어느 라우트를 둘지를 결정하고, 비용이 인프라 엔지니어 인건비를 넘는 자리부터 셀프호스트를 검토한다. 단계가 다르면 *지금* 켜야 할 것이 다르다 — 이 직관이 책 전체에 깔려 있다.

그리고 이번 새벽에는 *떠날 수 있는 능력*도 같이 손에 있다. `output: "standalone"` 빌드를 분기에 한 번씩 돌려본다. OpenNext의 한계를 안다. Adapter API stable이 풍경을 어떻게 바꿨는지를 안다. 다른 후보가 어디 있는지, 어느 자리에서 누가 빛나는지를 한 줄로 떠올릴 수 있다.

같은 `vercel deploy` 한 줄이다. 5분 뒤에 같은 URL이 떨어지고, 같은 자물쇠가 박힌다. 그런데 그 한 줄 뒤에 4단계의 척추가, 과금의 3축이, 시크릿의 두 종류가, 탈출의 옵션이 함께 보인다. 황홀함이 사라진 게 아니다. 막막함이 사라진 거다.

1장에서는 이 명령이 *황홀하다*고 적었다. 9장에 와서 다시 보면, 이 명령은 여전히 황홀하다. 다만 황홀함의 결이 좀 다르다. 처음에는 *한 줄이 인터넷에 사이트를 띄웠다*는 사실이 황홀했다면, 이번에는 *그 한 줄 뒤에 어떤 결정이 어떻게 묶여 있는지를 다 알면서도 그 한 줄을 그대로 칠 수 있다*는 사실이 황홀하다. 도구를 마법으로 보지 않으면서, 동시에 도구의 잘 만든 결을 인정하는 자리. 입문자가 운영자로 한 단계 올라선 자리다.

이 책은 거기까지 같이 왔다. 그 다음의 한 줄, 그 다음의 한 단계는 독자의 새벽에 맡긴다. 자기 프로젝트의 단계가 바뀌면 가드레일을 다시 켜고, 청구서가 흔들리면 7장으로 돌아오고, 보안 뉴스가 들리면 8장의 절차를 한 번 더 점검하고, 어느 날 떠나야 한다고 해보자, 라는 가정이 진심이 되면 9장의 standalone 드릴을 평소에 두자. 그 사이사이에 황홀함이 한 번씩 다시 와도 좋다. 이번에는 막막함 없이 와도 좋다.

좋은 새벽 되자.
