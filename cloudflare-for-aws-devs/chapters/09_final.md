# 9장. Next.js on Cloudflare — Workers Static Assets·OpenNext의 현실

AWS Amplify Hosting에 올려둔 Next.js 상점 프론트가 한 개 있다고 해보자. 토큰 한 줄 바꾸면 자동 배포되고, Lambda@Edge도 알아서 깔리고, 큰 사고 없이 1년쯤 잘 굴러갔다. 그런데 어느 날 사용자가 도쿄·서울·LA·암스테르담에 흩어져 있다는 사실이 문제로 떠오른다. 미주 사용자에게서 "장바구니 페이지가 답답하다"는 컴플레인이 들어온다. CloudFront 캐시 hit률은 나쁘지 않은데, SSR 페이지 한 번에 800ms를 넘는 일이 잦다. 한국 리전에 박힌 Lambda@Edge가 미국에서 콜드스타트할 때마다 사용자가 1초씩 기다린다. 옮겨야 할까? 어디로 옮겨야 할까?

7장에서 D1과 KV를 손에 쥐고, 8장에서 Durable Objects와 R2까지 들고 왔다. 백엔드 깊이로 두 챕터를 내달렸으니 이번 장은 호흡을 한 번 환기하자. 프론트 이야기다. Next.js 앱을 Cloudflare 위에 어떻게 올릴 것인가. 답이 한 줄로 정리되지 않는다는 사실부터 짚어둬야 한다 — 2025년 4월 이후로 Cloudflare의 프론트 호스팅은 *움직이고 있는 풍경*이기 때문이다.

이 장에서 손에 쥐고 가야 할 것은 세 가지다. 첫째, Pages가 Workers Static Assets로 흡수된 흐름을 이해한다. 둘째, `@opennextjs/cloudflare` 어댑터로 Next.js 14/15 앱을 어떻게 올리는지 단계별로 따라간다. 셋째, *어떤 Next.js 앱은 옮겨도 되고 어떤 앱은 미루는 게 옳은지* 의사결정선을 그린다. 5장에서 만든 결정 프레임을 프론트에 한 번 더 적용하는 셈이다.

자, Pages 이야기부터 살펴보자.

## Pages가 사라진 자리에 Workers Static Assets가 들어왔다

3년 전쯤 Cloudflare 프론트 호스팅을 처음 만난 사람이라면 Pages를 기억할 것이다. GitHub 리포만 연결하면 자동 빌드·자동 배포·Preview deploy까지 한 번에 되던 그 제품이다. Vercel·Netlify와 거의 같은 DX, 게다가 무료 트래픽 무제한이라는 매력. 한국 커뮤니티에서도 한동안 "Vercel 비싸면 Pages 써봐라"는 말이 자연스럽게 돌았다.

그런데 2025년 4월부터 분위기가 바뀐다. Cloudflare가 새 프론트 기능들을 Pages에 더 얹지 않고 *Workers Static Assets*라는 새 모델로 옮기기 시작한 것이다. 공식 문서의 톤도 달라진다. "Pages는 maintenance 모드, 신규 프로젝트는 Workers Static Assets로 시작하시오." 한국말로 옮기면 "Pages는 그대로 두지만 더 손은 안 댄다" 정도의 뜻이다.

이 흐름이 처음 들으면 살짝 찜찜하다. 프론트 호스팅을 두 번 갈아엎는 건가? 기존 Pages 사용자는 어떻게 되는 건가? 정직하게 말하면 — 기존 Pages는 당분간 멀쩡히 돈다. Cloudflare가 갑자기 끄지는 않는다. 하지만 새 프로젝트를 시작한다면 Pages를 고를 이유가 거의 없다. 두 가지 풍경이 동시에 지나가고 있다고 보면 된다.

그렇다면 Workers Static Assets가 무엇인지 한 줄로 정리하자. **Worker 코드 하나에 정적 자원(HTML·CSS·JS·이미지)을 묶어 한 배포 단위로 만드는 모델**이다. 정적 SPA·SSG라면 정적 자원만 있고, SSR이 필요하다면 Worker가 그걸 담당한다. 같은 `wrangler deploy`로 두 가지가 한 번에 올라간다. 정적과 동적이 한 배포 단위 안에 들어와 있는 모양이다.

3가지 옵션을 한 표로 비교하면 이렇다.

| 방식 | 권장도 | 한 줄 메모 |
|---|---|---|
| **Cloudflare Pages** | △ (legacy) | 2025년 4월 이후 maintenance. 기존 사용자는 그대로 두되, 새 프로젝트에는 권장 안 함. |
| **Workers Static Assets** | ◎ | 정적 SPA·SSG에 가장 자연스러운 자리. Worker SSR과 한 배포 단위. |
| **`@opennextjs/cloudflare`** | ◎ (Next.js 풀 기능) | 1.0-beta 시점에 Next 14/15 대부분이 동작. Edge Runtime은 미지원. |
| **Vercel** | (외부 옵션) | DX·기능 풀커버. 비용·벤더 종속이 단점. |

이 표를 보면서 처음 드는 물음은 이거다 — *내 Next.js 앱은 어디에 올려야 하나?* 답은 두 갈래다. 정적 사이트라면 Workers Static Assets만으로 충분하다. SSR·ISR·서버 컴포넌트가 들어간 풀 Next.js라면 그 위에 한 겹 더 — `@opennextjs/cloudflare` 어댑터가 필요하다. 이 어댑터 이야기는 잠시 뒤에 본격적으로 보자.

## OpenNext가 1.0-beta라는 한 줄에서 멈칫한다면

OpenNext라는 이름을 처음 들으면 무엇인지 짐작이 안 간다. "Next의 오픈?" 정도. 사실 이름 그대로다 — Vercel이 아닌 곳에서 Next.js를 돌리기 위한 *오픈 소스 어댑터*다. AWS Lambda용 OpenNext, Netlify용 OpenNext, 그리고 우리에게 중요한 *Cloudflare용* `@opennextjs/cloudflare`가 있다.

Cloudflare 공식 블로그가 2024년에 "Next.js를 Workers에 그대로 올리는 길이 열렸다"고 발표한 그날부터, OpenNext가 사실상 표준이 됐다. 2026년 5월 시점에서 `@opennextjs/cloudflare`는 1.0-beta 단계에 있다. *1.0-beta*라는 말을 듣는 순간 살짝 찜찜하다. production에 올려도 되는 건가? 정직한 답은 — *대부분의 Next 14/15 앱은 동작한다, 다만 몇 가지 자리에서 발이 걸린다*. 곧 그 발이 걸리는 자리들을 짚는다.

OpenNext for Cloudflare의 본질을 한 줄로 정리하면 이렇다. **Next.js 빌드 결과물(`.next/` 폴더)을 Workers가 이해할 수 있는 형태로 바꿔주는 어댑터**다. Vercel이 자체적으로 하는 일을 OpenNext가 오픈 소스로 풀어 놓은 셈이다. 빌드 시점에 Next의 서버 코드를 Worker용 번들로 변환하고, 정적 자원을 Workers Static Assets로 분리하고, ISR 캐시 어디에 둘지를 R2·KV로 매핑한다.

좋아진 점도 있다. Workers runtime에 crypto·dns·timers·tls·net 같은 핵심 Node 모듈이 native로 들어왔다. 예전엔 polyfill로 비비 꼬아야 했던 자리들이 지금은 Node처럼 그냥 돈다. `next start`로 띄우던 앱을 Workers에 올렸을 때 깨지는 면적이 1년 전보다 한 자릿수 줄었다.

그렇다면 한계는 뭔가. 다음 자리에서 발이 걸린다.

- **Edge Runtime 미지원** — Vercel에서 `export const runtime = 'edge'`로 표시한 라우트가 있다면, OpenNext on Cloudflare에서는 그게 자동으로 Edge runtime으로 안 돈다. Node runtime으로만 돈다. 이름이 헷갈리는데, *Cloudflare Workers 자체는 V8 isolate인데 OpenNext의 라우트 분류상 "Node runtime"으로 잡힌다*는 의미다. 결과적으로 Edge runtime 가정의 코드(Web API만 사용, Node API 금지)가 그대로 들어가지 않는 경우가 있다. Vercel용 코드를 그대로 옮기면 일부 라우트가 깨진다.
- **스크립트 크기 한도** — Workers Free 3MiB / Paid 10MiB. Sharp나 Prisma engine처럼 큰 의존성을 그대로 번들에 넣으면 한도에 걸린다. 이미지 최적화는 Cloudflare Images로 분리하고, Prisma를 쓰던 자리는 Drizzle이나 Kysely로 바꾸는 편이 낫다 (10장 Hyperdrive와 자연스럽게 연결되는 결정).
- **Windows 미완전 지원** — 빌드가 Windows에서 완전히 안 도는 자리가 있다. 팀에 Windows 사용자가 있다면 WSL2 또는 컨테이너 빌드를 권한다. (Mac·Linux는 문제 없다.)
- **`use cache` (composable caching)** — Next.js 15의 새 캐싱 디렉티브는 다음 메이저 릴리즈에 들어온다는 게 OpenNext 로드맵이다. 책 집필 시점에는 *예정* 단계.
- **ISR 일부 시나리오** — `revalidate`로 다시 빌드하는 ISR은 동작하지만, 글로벌 분산된 Workers PoP 사이의 ISR 캐시 전파에는 한 박자 시간차가 있다. 1초 안에 모든 PoP가 같은 페이지를 보여주리라 기대하면 어긋난다.

이 다섯 가지 한계가 OpenNext가 "1.0-beta"인 이유다. 광고 없이 정직하게 말하면 — *production-ready*에 한 발 걸쳐 있는 상태. 무난한 e-commerce 프론트, 블로그, 대시보드, SaaS landing이라면 충분히 올릴 만하다. Edge runtime 가정이 깊게 박힌 앱이거나 Sharp 직접 호출이 필요한 미디어 앱이라면 잠시 미루는 편이 낫다.

## 따라해보자 — Next.js 14 상점 프론트를 올리기까지

말로만 풀면 멀리 있는 이야기처럼 들린다. `toby-shop`의 상점 프론트(Next.js 14)를 손가락으로 한 번 올려보자. 6장에서 만든 사용자 API와 7장에서 D1으로 옮긴 프로필 API가 이미 살아 있다고 가정하자. 이번 장의 목표는 그 위에 *Worker 한 개*를 더 띄우는 것이다 — Next.js 풀 기능이 도는 SSR Worker.

### 0단계 — 프로젝트 만들기

새 Next.js 앱을 만든다. 평범하다.

```bash
pnpm create next-app@latest toby-shop-web
# TypeScript: Yes
# App Router: Yes
# Tailwind: 취향대로
```

여기까지는 Vercel과 똑같다. 이제 Cloudflare용 어댑터를 붙이자.

### 1단계 — `@opennextjs/cloudflare` 추가

```bash
cd toby-shop-web
pnpm add -D @opennextjs/cloudflare wrangler
```

그리고 프로젝트 루트에 `open-next.config.ts`를 만든다. 사실 default config면 충분하다.

```ts
// open-next.config.ts
import { defineCloudflareConfig } from "@opennextjs/cloudflare";

export default defineCloudflareConfig({
  // ISR 캐시를 어디에 둘지: R2 또는 KV.
  // 지금은 default (작은 프로젝트면 KV, 큰 프로젝트면 R2 권장)
  incrementalCache: "kv",
});
```

`incrementalCache`가 처음 보는 옵션일 것이다. Next.js의 ISR은 빌드된 페이지를 어딘가에 캐시해 두고 일정 시간 뒤에 다시 빌드하는 모델이다. Vercel에서는 그 캐시가 Vercel KV에 들어가는데, OpenNext on Cloudflare에서는 *KV*냐 *R2*냐 우리가 정해야 한다. 작은 사이트라면 KV로도 충분하고, 캐시 페이지가 큰 e-commerce·미디어라면 R2가 비용 측면에서 낫다.

### 2단계 — `wrangler.toml`로 묶기

다음으로 `wrangler.toml`을 한 장 둔다. 이게 Workers Static Assets의 핵심 설정 파일이다.

```toml
# wrangler.toml
name = "toby-shop-web"
main = ".open-next/worker.js"
compatibility_date = "2026-04-01"
compatibility_flags = ["nodejs_compat"]

[assets]
directory = ".open-next/assets"
binding = "ASSETS"

[[kv_namespaces]]
binding = "NEXT_INC_CACHE_KV"
id = "your-kv-namespace-id"
```

한 줄씩 풀어 보자.

`main = ".open-next/worker.js"` — 빌드 결과물의 진입점. `pnpm opennextjs-cloudflare build`를 한 번 돌리면 `.open-next/` 폴더가 생기고 그 안에 worker.js가 떨어진다. 이 한 파일이 Next.js의 모든 SSR 엔트리를 흡수한 결과물이다.

`compatibility_flags = ["nodejs_compat"]` — Workers runtime에서 Node 호환 API를 켜는 플래그. OpenNext가 만들어내는 코드는 일부 Node API에 의존하므로 이 플래그가 필수다. (예전에는 polyfill 패키지를 더해야 했는데 지금은 native 호환이 들어와 깔끔해졌다.)

`[assets] directory = ".open-next/assets"` — 정적 자원이 들어 있는 디렉터리. Workers Static Assets가 이 폴더 안의 모든 파일을 CDN처럼 서빙한다. CSS·JS·이미지·`/_next/static/...` 모두 여기에 들어간다.

`[[kv_namespaces]]` — ISR 캐시용 KV 바인딩. 이름이 `NEXT_INC_CACHE_KV`로 정해져 있다는 점에 주의하자. OpenNext가 이 이름을 기대한다. KV namespace는 미리 만들어 둬야 한다 — `wrangler kv namespace create NEXT_INC_CACHE_KV`로 한 번에 만들 수 있고, 출력으로 나오는 ID를 위 `id` 자리에 넣는다.

### 3단계 — 빌드와 로컬 미리보기

이제 빌드한다.

```bash
pnpm opennextjs-cloudflare build
```

이 한 줄이 무엇을 하는가. `next build`를 먼저 돌리고, 그 결과물을 OpenNext가 Workers용 번들로 다시 변환한다. 처음 돌리면 30초~1분쯤 걸린다. `.open-next/`라는 폴더가 새로 생긴다.

로컬에서 한 번 미리 보자.

```bash
pnpm wrangler dev
```

`localhost:8787` 정도에 사이트가 뜬다. `wrangler dev`는 production runtime을 그대로 재현하므로 (workerd 위에서 도므로) 로컬에서 잘 돌면 production에서도 거의 그대로 돈다고 봐도 좋다. 4장에서 살펴봤던 *workerd local mode*의 신뢰가 여기서 빛난다.

### 4단계 — 배포

```bash
pnpm opennextjs-cloudflare deploy
```

또는 `wrangler deploy`. 1~2분 안에 `toby-shop-web.<sub>.workers.dev` 도메인에 사이트가 올라온다. 7장에서 만든 사용자 API가 같은 계정에 있으면 같은 KV·D1 namespace를 공유할 수도 있다. 모노레포라면 더 자연스럽다 — `apps/web`이 `wrangler.toml` 한 장을 가지고, `apps/api`도 자기 `wrangler.toml`을 가지고, 둘이 같은 D1을 본다. 4장에서 권장했던 모노레포 구조가 이 자리에서 자연스럽게 동작한다.

여기까지 따라왔다면 Next.js 14 앱 한 개가 Cloudflare 글로벌 PoP에 깔린 셈이다. 한국에서 접속하면 도쿄 PoP, LA에서 접속하면 LA PoP. SSR이 가까운 PoP에서 돌고, 정적 자원은 같은 PoP의 Workers Static Assets에서 나간다.

### 5단계 — Preview deploy 구성하기

여기서 Vercel 사용자라면 한 가지가 빠진 것을 눈치챈다 — *PR마다 자동으로 뜨는 preview URL.* Vercel에서는 GitHub PR을 열면 30초 만에 preview 환경이 깔리는 그 마법이 OpenNext on Cloudflare에서는 직접 구성해야 한다. 처음 보면 살짝 번거롭지만 GitHub Actions 한 장으로 풀린다.

```yaml
# .github/workflows/preview.yml
name: Preview Deploy
on: pull_request

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: pnpm install --frozen-lockfile
      - run: pnpm opennextjs-cloudflare build
      - name: Deploy preview
        run: |
          pnpm wrangler deploy \
            --name toby-shop-web-pr-${{ github.event.number }} \
            --compatibility-date 2026-04-01
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CF_API_TOKEN }}
```

PR이 열릴 때마다 `toby-shop-web-pr-123.<sub>.workers.dev` 같은 URL이 뜬다. 매끄럽지는 않지만 동작은 한다. `wrangler` versions API를 쓰면 더 정교한 staging deploy도 가능한데, 여기까지 들어가면 호흡 환기가 아니라 본격 DevOps 챕터가 되니 부록 A의 wrangler 치트시트로 미루자.

기억해두자 — *OpenNext의 매끈하지 않은 자리는 거의 다 직접 구성으로 풀린다.* Vercel만큼 즉각적이지 않지만, 한 번 GitHub Actions를 잘 짜두면 그 다음부터는 자동이다.

## 라우트별 runtime 선택 — 무엇을 어디서 돌릴까

Next.js 14/15에는 라우트마다 runtime을 지정하는 두 줄이 있다. App Router 기준으로 라우트 파일 상단에 다음을 적는다.

```ts
// app/api/health/route.ts
export const runtime = "nodejs"; // 또는 "edge"
```

Vercel에서는 이 한 줄이 굵직한 결정이다 — `edge`로 하면 Vercel Edge runtime에서, `nodejs`로 하면 AWS Lambda Node runtime에서 돈다. OpenNext on Cloudflare에서는 어떻게 동작할까. 정직하게 말하면 — *현 시점(2026년 5월)에서는 Edge runtime export가 미지원*이라 모두 Workers의 Node-호환 모드(`nodejs_compat`)에서 돈다. `edge`로 표시한 라우트가 있어도 Node 모드로 돈다.

이게 좋은 면도 있고 헷갈리는 면도 있다. 좋은 면은 — Vercel용 Edge runtime으로 못 옮겼던 라우트들이 *그냥 다 잘 돈다*. Edge에서는 못 쓰던 Node API들이 들어가 있어도 Workers의 `nodejs_compat`이 받아준다. 헷갈리는 면은 — `runtime = "edge"`라는 표시 자체가 OpenNext on Cloudflare에서는 *의미가 없다*는 점이다. 코드에 그렇게 적혀 있어도 실제 실행 환경은 Workers V8 isolate 위의 Node-호환 모드다. 이 차이를 모르고 "Edge runtime이니까 빠르겠지"라고 가정하면 어긋난다.

그래서 권하는 모양은 단순하다. *runtime 표시를 안 적거나 `nodejs`로 통일한다.* OpenNext 가이드의 default가 그렇다. 라우트별 차이는 따로 두지 말고, 무거운 의존성이 들어가는 라우트만 별도 Worker로 분리하는 식으로 가는 편이 낫다.

여기서 한 단계 더 들어가면, ISR과 SSR의 선택 기준이 헷갈릴 수 있다. 한 표로 정리하자.

| 페이지 종류 | 권장 모양 | Cloudflare 위에서 |
|---|---|---|
| 정적 콘텐츠 (랜딩·about) | SSG | 빌드 시점에 HTML 생성, Workers Static Assets에서 그대로 서빙 |
| 자주 바뀌는 콘텐츠 (블로그·뉴스) | ISR | revalidate 주기 설정. 캐시는 KV 또는 R2 (`incrementalCache` 옵션) |
| 사용자별 콘텐츠 (대시보드·장바구니) | SSR | 매 요청마다 Worker가 SSR. 빠른 PoP에서 돌아 Vercel 대비 콜드스타트 이점 |
| 검색·필터 (DB 쿼리 무거움) | SSR + Hyperdrive | DB는 그대로 두고 Hyperdrive로 가속 (10장에서 본격) |
| 이미지 처리 | Cloudflare Images | next/image 대신 분리 (다음 절) |

이 표가 본문 14장 마이그레이션 시퀀스의 프론트 부분 베이스다. 5장에서 그렸던 결정 워크시트의 "정적 콘텐츠"·"사용자 facing CRUD" 칸이 이 자리에서 구체적으로 풀린다.

ISR 동작을 한 번 손가락으로 그려 보자. `app/products/[id]/page.tsx`에 `export const revalidate = 60`이라고 적었다고 해보자. 무엇이 일어나는가?

1. 첫 사용자(서울)가 `/products/123`을 부른다 — Worker가 SSR로 페이지를 만들고, 결과를 KV(`NEXT_INC_CACHE_KV`)에 저장한 뒤 사용자에게 응답한다.
2. 60초 안에 두 번째 사용자(서울)가 같은 페이지를 부른다 — Worker가 KV에서 캐시된 페이지를 꺼내 즉시 응답한다. SSR 안 돈다.
3. 60초가 지난 뒤 세 번째 사용자가 부른다 — Worker가 stale 페이지를 일단 응답하고, 백그라운드로 새 페이지를 빌드해 KV에 갱신한다 (stale-while-revalidate 모델).
4. 그런데 LA 사용자가 같은 시점에 `/products/123`을 부르면? KV는 글로벌 분산이라 *대체로* 같은 캐시를 보지만, 60초 정도 전파 시간차가 있을 수 있다. *이 시간차가 위에서 짚었던 한계 한 줄이다.*

이 모양이 머리에 들어오면 ISR을 어디에 쓸지 감이 잡힌다. 1초 단위 신선도가 중요한 페이지(주식 시세·실시간 재고)는 ISR로 풀지 말자. 1분~1시간 단위 신선도면 충분한 페이지(상품 상세·블로그 글·카탈로그)에 ISR이 빛난다. *Cloudflare의 ISR은 "거의 정적인 페이지를 거의 즉시 응답하는" 자리에서 가장 잘 어울린다.*

## 이미지 최적화 — `next/image` vs Cloudflare Images

Next.js의 `next/image`는 Vercel 위에서 한 줄로 끝나는 마법이다. 컴포넌트만 쓰면 알아서 리사이즈·WebP 변환·lazy loading이 다 된다. Cloudflare 위에서는 어떻게 다룰까.

선택지가 두 개다.

**선택지 1. `next/image` 그대로 쓰기.** OpenNext가 Workers 위에서 Next.js의 이미지 최적화 엔드포인트를 돌리도록 어댑터해 둔다. 다만 큰 함정이 있다 — `next/image`의 내부는 Sharp 라이브러리를 쓴다. Sharp는 native binary 의존성이 깊어서 Workers 스크립트 크기 한도(Free 3MiB / Paid 10MiB)를 곧잘 넘긴다. 작은 사이트라면 안 걸리지만, 이미지 종류가 많은 e-commerce에서는 빌드 단계에서 한도 초과로 거부되는 일이 잦다. 정직하게 말하면 — *2026년 5월 시점에서는 권하지 않는다.*

**선택지 2. Cloudflare Images로 분리하기.** 이쪽이 권장 패턴이다. Cloudflare Images는 별도 제품으로, 5,000 transforms/월 무료, 이후 $0.50/1,000의 가격이다. 이미지 자체는 R2 버킷이나 외부 origin(예: 기존 S3)에 두고, 변환만 Cloudflare Images에 맡긴다. 코드는 이렇게 된다.

```tsx
// app/products/[id]/page.tsx
import Image from "next/image";

const cfLoader = ({ src, width, quality }: any) => {
  const params = `width=${width},quality=${quality || 75},format=auto`;
  return `https://imagedelivery.net/your-account-hash/${src}/${params}`;
};

export default function Product({ params }: any) {
  return (
    <Image
      loader={cfLoader}
      src="product-123-hero"
      width={1200}
      height={800}
      alt="Hero"
    />
  );
}
```

`next/image`의 컴포넌트 인터페이스는 그대로 살리되, `loader`만 Cloudflare Images로 바꾸는 모양이다. Next의 React 컴포넌트 DX를 잃지 않으면서 이미지 처리를 Workers 번들 바깥으로 빼낸 셈이다. 스크립트 크기 한도에 걸릴 일이 없고, transform 비용도 Vercel Image Optimization 대비 큰 폭 저렴하다.

기억해두자 — Next.js를 Cloudflare에 올린다면 이미지는 처음부터 Cloudflare Images로 분리하는 편이 낫다. 시작할 때 이 결정을 미뤘다가 나중에 바꾸면, 이미 깔린 이미지의 URL 패턴을 다 갈아엎어야 한다. 끔찍한 일이다.

한 가지 더. 이미지 자체를 어디에 둘지도 함께 정하자. 세 가지 패턴이 있다.

- **Cloudflare Images에 직접 업로드** — 가장 단순. 5,000장까지 무료 storage 포함. 작은 사이트.
- **R2에 두고 Cloudflare Images로 변환** — storage는 R2(egress free), transform만 Cloudflare Images. 이미지 종류가 많은 e-commerce에 가장 합리적인 모양.
- **기존 S3에 두고 Cloudflare Images로 변환** — 이미지가 이미 S3에 있다면 그대로 두고 transform 레이어만 Cloudflare로. 마이그레이션 비용을 한 자릿수 가볍게 만든다. 하이브리드 패턴의 자연스러운 자리.

세 번째 패턴이 이 책 전체의 권장 모양과 가장 잘 맞는다. *S3는 그대로, 컴퓨트 한 겹만 Cloudflare로.* 10장에서 RDS를 두고 Hyperdrive로 가속하는 그림과 같은 멘탈이다.

## AWS Amplify·Vercel과의 비용·DX 비교

매핑 표만으로는 결정이 안 선다. 비용과 DX를 함께 봐야 한다. 한 표로 정리하자.

| 기준 | AWS Amplify Hosting | Vercel | Cloudflare (Workers Static Assets + OpenNext) |
|---|---|---|---|
| **DX (배포·롤백)** | GitHub 연결, preview deploy, 매끈한 편 | *최강*. preview·rollback·analytics 한 화면 | wrangler 기반, GitHub Actions 연동. preview는 직접 구성 |
| **글로벌 지연** | CloudFront + Lambda@Edge. 일부 PoP에서 콜드스타트 큼 | Edge Network 글로벌, 콜드스타트 작음 | Workers 글로벌 PoP, 콜드스타트 < 5ms |
| **비용 (트래픽)** | egress 청구가 주범 | 무료 tier 후 빠르게 가파름. team plan부터 의무 | egress free, Workers 요청 단가 저렴 |
| **이미지 최적화** | 별도 구성 (CloudFront + Lambda) | Vercel Image Optimization 비싼 편 | Cloudflare Images 저렴 |
| **Edge runtime 호환성** | 부분 지원 (Lambda@Edge) | 100% 지원 (네이티브) | 미지원 (Node mode로만) |
| **벤더 종속** | AWS 전반에 깊이 통합 | Vercel 고유 API 다수 | Workers 고유 binding API 일부 |
| **2025 outage 영향** | AWS region outage 시 영향 | Vercel infra outage 영향 | Cloudflare outage 시 영향 (13장에서 다룸) |

이 표만 보면 Cloudflare가 압도적으로 보일 수 있는데, 정직하게 균형을 잡자. **Vercel의 DX는 여전히 강하다.** Cloudflare 어댑터로 옮기면 preview deploy를 직접 구성해야 하고, 빌드 로그·배포 history UI도 Vercel만큼 매끈하지 않다. 작은 팀에서 *DX의 시간 절약*이 비용보다 중요하다면 Vercel이 합리적인 선택이다. 한국 Next.js 개발자 사이에서 잘 알려진 velopert(veltrends) 사례가 그 한 모양이다 — 처음 Cloudflare Pages에 올렸다가 SSR·Node 호환성 문제로 Vercel로 회귀했다. 그 결정이 틀렸다고 말하기 어렵다. 1인 개발자 + 빠른 출시 + DX 우선이라는 입력에서 Vercel은 합리적이다.

반대로 Baselime 사례처럼 *글로벌 분포 + spike-y 트래픽 + 비용 민감*한 입력이라면 Cloudflare로 옮기는 동기가 매우 분명해진다. 5장의 5축 결정 트리가 프론트에서도 그대로 작동한다 — 요청 패턴·일관성·글로벌성·런타임 의존·컴플라이언스. 다섯 축이 다 초록불인 Next.js 앱이라면 OpenNext on Cloudflare가 잘 어울리고, 한 축이라도 빨간불이면 Vercel을 유지하는 편이 낫다.

기억해두자 — *Vercel을 떠나는 것이 목표가 아니다.* 5장에서 강조했던 그 한 줄이 9장에서도 유효하다. 자기 앱에 올바른 자리를 내주는 것이 목표다.

## Vinext — "곧 등장할 또 하나"라는 풍경

OpenNext가 사실상 표준이 된 자리에서, Cloudflare가 직접 만드는 또 하나의 라인이 보이기 시작했다. *Vinext*다. 이름은 Vite + Next의 합성어 같고, 실제로도 Vite 플러그인 형태로 Next.js 호환을 제공하는 어댑터다. GitHub의 `cloudflare/vinext` 리포에서 진행 상황을 추적할 수 있다.

이 풍경은 정직하게 *불확실성*을 안고 있다. 책 집필 시점(2026년 5월)에서는 실험적 라인이고, OpenNext와 별개로 굴러간다. *책 집필 시점에 사실 확인 필요*라는 면책을 한 줄 박아둔다 — 이 책이 출간되고 1년 뒤에 Vinext가 OpenNext를 대체할지, 아니면 두 라인이 공존할지, 아니면 조용히 사라질지 지금은 알 수 없다.

그렇다면 우리가 어떻게 해야 할까. 두 가지 권장사항이다.

첫째, **새 프로젝트는 OpenNext로 시작한다.** 1.0-beta라는 라벨이 붙어 있어도 사실상 표준이고 사례도 많다. 안전하다.

둘째, **Vinext의 진행 상황은 분기마다 한 번 살핀다.** Cloudflare 공식 블로그·OpenNext 뉴스·GitHub 리포 README. 이 셋이 Vinext의 위상이 바뀔 때 가장 먼저 신호를 준다. 만약 Cloudflare가 Vinext를 1순위로 밀기 시작하고 OpenNext 어댑터의 유지보수가 줄어드는 신호가 보이면, 그때 옮길 결정을 한다.

이 풍경 자체가 Cloudflare 생태계의 변동성을 보여준다. 부록 E에서 "책 이후 추적 가이드"를 별도로 둔 이유다 — Cloudflare는 분기마다 풍경이 바뀐다. Vinext만이 아니다. Workers Containers GPU·Vectorize hybrid search·Dynamic Workers 같은 영역도 마찬가지다. 한 번 책에 박아둔 가이드를 1년이 지나도 그대로 믿으면 위험하다. *분기마다 한 번씩 공식 페이지를 다시 보자.*

## 어떤 Next.js 앱은 옮기지 말자

5장의 결정 프레임을 프론트에 한 번 더 적용해 보자. 다음 자리에서는 Cloudflare로 옮기지 않는 게 정직한 답이다.

- **Edge runtime 가정이 깊은 앱.** 코드 곳곳에 `runtime = "edge"`가 박혀 있고, Web API만 쓰도록 다듬은 라우트가 절반 이상이라면, OpenNext on Cloudflare에서 그 가정이 깨진다. Vercel을 유지하자.
- **Sharp 또는 큰 native binary 의존성이 핵심.** 이미지 처리·PDF 생성·headless Chrome을 직접 호출해야 하는 앱. 스크립트 크기 한도와 native binary 제약에서 곧 막힌다. 이쪽은 별도 ECS/Lambda task로 분리하거나 Cloudflare Images 같은 외부 제품으로 빼자.
- **DX 우선 + 작은 팀.** 1~2인 팀이고 *시간이 가장 비싼 자원*이라면 Vercel의 매끈함이 비용을 정당화한다. velopert 사례의 결정이 그 자리다.
- **`use cache` (Next.js 15) 깊이 의존.** OpenNext의 `use cache` 지원이 다음 메이저 릴리즈 예정이므로, 이 디렉티브를 적극 쓰는 앱은 잠시 미루자.
- **Windows 전용 빌드 환경.** Mac·Linux로 옮길 의향이 없다면 OpenNext의 빌드가 매끄럽지 않다.

반대로 다음 자리는 옮길 만하다.

- **글로벌 사용자 분포 + e-commerce / SaaS 대시보드.** 이게 OpenNext on Cloudflare의 sweet spot이다.
- **이미 R2·KV·D1을 쓰고 있는 백엔드와 한 단위로 묶고 싶은 앱.** 같은 binding을 공유해서 데이터·세션을 깔끔하게 나눠 갖는다.
- **Vercel 비용이 가파르게 올라간 앱.** 트래픽 큰 사이트라면 Cloudflare로 옮겼을 때 절감 폭이 한 자릿수 차이가 날 수 있다.
- **DX보다 글로벌 분포·비용이 우선인 앱.** 엔지니어링 시간이 절약되는 자리.

이 결정도 5장의 워크시트처럼 *지금 당장*이 아니라 *권장*이다. Vercel에 잘 굴러가는 프론트를 굳이 옮길 필요가 없다. 비용·지연·운영 부담이 한 축이라도 점점 무거워질 때, OpenNext on Cloudflare가 옵션 한 자리에 들어가 있으면 그때 옮기면 된다. *옮기지 않는 결정도 정직한 결정이다.*

## OpenNext가 무너지는 자리

이 책이 광고서가 아니라는 약속을 9장에서도 지키자. OpenNext on Cloudflare가 무너지는 자리들을 한 번 더 짚어둔다.

- **Edge Runtime 미지원.** Vercel용 코드 그대로 옮기면 일부 라우트가 깨지거나 의도와 다르게 Node 모드로 돈다. 운영 환경에서 동작이 다르면 디버깅이 까다롭다.
- **스크립트 크기 한도.** Sharp·Prisma engine·headless Chrome 같은 큰 의존성은 빌드 단계에서 거부된다. 빠른 워크어라운드가 없는 자리.
- **Windows 빌드 미지원.** 팀 일부가 Windows라면 WSL2 또는 컨테이너 빌드 강제. 매끈하지 않다.
- **`use cache` 미지원 (현 시점).** Next.js 15의 새 캐싱 모델을 적극 쓰는 앱은 잠시 미뤄야 한다.
- **ISR PoP 전파 시간차.** 글로벌 분산된 PoP 사이의 ISR 캐시 전파에 시간차가 있다. "1초 안에 모두 같은 페이지"를 기대하면 어긋난다.
- **Preview deploy DX.** Vercel만큼 매끈한 preview deploy를 직접 구성해야 한다. GitHub Actions + wrangler로 풀 수는 있지만 즉시 되는 모양은 아니다.
- **Vinext와의 미래 관계.** OpenNext의 향후 위상이 Vinext의 진행에 따라 흔들릴 가능성이 있다. 1년 뒤 책 가이드가 *그대로* 유효할지 사실상 보장 못 한다.
- **빌드 실패 디버깅.** OpenNext 빌드 에러 메시지가 처음 보면 의미가 잘 안 잡힌다. 부록 F에 자주 보이는 7가지 에러를 별도로 정리해 두었다 — 처음 막히면 거기를 펼쳐 보자.

이 무너지는 자리들을 알고도 옮길 만한가? 충분히 그렇다. 다만 *알고 옮기는* 것이지 *모르고 옮기는* 것이 아니다. 그 차이가 6개월 뒤 회귀 사례를 만드는지 안 만드는지를 가른다.

## 마무리

Next.js를 Cloudflare에 올리는 길을 9장에서 한 번 짚어 봤다. Pages가 Workers Static Assets로 흡수된 흐름, `@opennextjs/cloudflare` 어댑터로 Next 14/15를 올리는 단계별 명령, 라우트별 runtime 선택의 함정, 이미지 최적화는 Cloudflare Images로 분리하는 권장 패턴, AWS Amplify·Vercel과의 DX·비용 비교, 그리고 Vinext라는 곧 등장할 풍경. 호흡 환기 챕터답게 따라 하기 친화적으로 풀었지만, 결정 자체는 결코 가볍지 않다.

이 한 장으로 우리는 한 가지 그림을 손에 쥐었다. **Workers + Hono로 만든 백엔드 API 옆에, OpenNext로 빌드된 Next.js 프론트가 같은 Cloudflare 계정 안에서 한 단위로 묶여 돈다.** `toby-shop`은 이제 Worker 한 개(API), Worker 한 개(채팅 DO), Web 한 개(Next.js 상점)로 구성된다. 같은 D1·KV·R2를 공유한다. 이 모양이 4장 매핑 카탈로그에서 약속했던 모노레포 구조의 자연스러운 결과다.

물론 9장의 이 그림에도 큰 한계가 하나 있다. *우리는 아직 RDS를 만지지 못했다.* `toby-shop`의 주문 도메인은 여전히 Aurora Postgres 같은 곳에 있을 가능성이 높고, 그걸 옮기는 일은 위험이 크다. 옮기지 않고도 edge에서 빠르게 쓸 길이 있다면 어떻겠는가? 다음 장에서 그 답을 손에 쥔다. **10장 — Hyperdrive로 RDS를 그대로 살려두기**. 점진 마이그레이션의 가장 risk-low한 첫 발걸음을 다음 페이지에서 살펴보자.
