# 4장. 사이드 단계 — Pro로 올라가는 순간

토이로 굴리던 프로젝트에 첫 결제가 들어왔다고 해보자. 단돈 1,000원짜리 디지털 다운로드 한 건이 됐든, 후원 페이지에 박은 Stripe 위젯에서 첫 입금이 찍혔든 상관없다. 그 순간 머릿속에 작게 경보가 울리는 게 정상이다. "이거 이제 Hobby로 굴려도 되는 건가." 비슷한 신호는 또 있다. 회사 명함에 도메인 한 줄이 박혀버렸다. 친구가 같이 만들자며 합류 의사를 보냈다. cron이 한 번으로는 부족해서 새벽마다 두 번, 점심에 한 번, 저녁에 알림 한 번 — 이렇게 여러 번 돌리고 싶어졌다. 이 중 하나라도 해당된다면, Pro로 올라갈 시점이다.

Pro로 올라간다는 건 단순히 한도가 넓어진다는 뜻이 아니다. 더 정확히 말하면 **계정에 카드가 묶이고, 한도를 넘어가면 청구서가 늘어나기 시작하는 세계로 진입한다**는 뜻이다. 그래서 Pro 진입은 한도 확장이 아니라 **운영 의식의 시작점**이라고 보는 편이 낫다. 이번 장에서는 그 시작점에 무엇을 켜고, 무엇을 분리하고, 어떤 기능을 활용하면 사이드를 사이드답게 굴릴 수 있는지를 짚어보자.

## 4.1 Pro로 올라가는 4가지 트리거

토이 단계에서 Pro로 올라갈지 말지를 두고 망설인 적이 있을 것이다. "굳이 $20을 매달 내야 하나, Hobby로 좀 더 버텨도 되지 않을까." 이 망설임 자체는 건강하다. 다만 Pro로 올라갈 시점은 비용 감각이 아니라 **신호**로 정해야 한다. 신호가 없는데 미리 올리면 돈만 새고, 신호가 왔는데 미루면 ToS 위반이거나 운영이 답답해진다.

신호는 크게 네 가지다.

**첫째, 첫 결제다.** 단순히 후원 링크 한 줄을 박아둔 정도가 아니라, 실제로 결제가 들어오기 시작했다면 더 이상 비상업 용도가 아니다. Hobby 플랜의 ToS는 "비상업적·개인 용도"를 명시한다. AdSense 한 줄, Stripe 결제 위젯, Patreon 링크가 박힌 페이지는 이 경계를 흔든다. 외부에서 신고가 들어오거나 Vercel 내부 모니터링에 걸리면 강제 업그레이드 안내가 온다. 강제로 올리는 것보다 자기 손으로 올리는 편이 낫다.

**둘째, 회사 명함이 박힌 프로젝트다.** 부업이든 사이드 비즈니스든 이름 걸린 도메인이라면 그 무게가 다르다. 한밤중에 다운되면 친구한테 "내일 고칠게"가 안 통한다. 명함이 박히는 순간부터는 SLA 비슷한 무엇이 자기 머릿속에 생긴다. Pro의 자동 갱신·우선 빌드·기본 알림이 그 무게를 일부 받쳐준다.

**셋째, cron이 자주 필요해진다.** Hobby의 cron은 일 1회로 묶여 있다. 처음에는 새벽 3시에 한 번 돌리는 정도로 충분했지만, 어느 순간부터 외부 API를 5분 간격으로 폴링하고 싶고, 매시간 캐시를 갱신하고 싶고, 저녁마다 사용자에게 알림을 보내고 싶어진다. 이 욕구가 생긴다는 건 프로젝트가 단순한 정적 사이트에서 운영 도구로 진화했다는 뜻이다. 4장 후반에서 cron을 어떻게 다회로 굴리는지 자세히 다룬다.

**넷째, 팀원이 합류한다.** 친구 한 명이라도 같이 작업하기로 했다면 Pro의 팀 기능이 필요하다. Hobby는 기본적으로 1인 운영을 가정한다. seat당 $20이 더해지는 점은 부담이지만, 권한 분리·역할 관리·공동 배포 권한 없이 GitHub 토큰만으로 운영하면 사고 시 추적이 어려워진다.

이 네 가지 신호 중 두 개가 동시에 켜지면 거의 확정이다. 한 개만 켜져도 "다음 달 안에"라는 마음으로 준비하는 편이 낫다. 미루면 ToS 사고나 운영 사고 중 하나로 갚게 된다.

## 4.2 Pro 플랜 구조 한 장으로 보기

Pro로 올라가기 전에 무엇을 사는지 정리해보자. 가격표만 보면 숫자가 흩어져 있어서 첫눈에 잘 잡히지 않는다. 한 줄로 정리하면 이렇다.

> **Pro = $20/seat/월 + 1TB Bandwidth + 10M Edge Requests + ~1,000 GB-hours 함수 메모리**

여기서 핵심은 두 가지다. 하나는 **seat당 과금**이라는 점이고, 다른 하나는 **포함된 한도를 넘으면 종량제로 더해진다**는 점이다.

Seat당 과금은 팀이 커질수록 베이스라인이 빠르게 올라간다는 뜻이다. 혼자면 $20이지만 5명이면 $100이 시작점이다. 합류 시점에 이 숫자가 조용히 올라간다는 걸 인지하고 시작하는 편이 낫다.

포함 한도를 넘으면 종량제로 청구된다. 1TB Bandwidth를 넘으면 GB당 $0.15, 10M Edge Requests를 넘으면 1M당 $2, 함수 메모리는 GB-hour당 $0.0106. 숫자만 보면 작아 보이지만 폭증할 때는 한 번에 수백 달러가 더해진다. 이 폭증 메커니즘은 7장에서 손으로 계산해본다. 4장에서는 "어디서 이렇게 늘어날 수 있다"는 감각만 잡고 가자.

한도를 넘기 시작하는 시점이 사이드와 초기 스타트업의 경계다. 사이드 단계 동안에는 1TB 안에서 거의 다 처리된다. 페이지 평균 2~5MB로 잡으면 1TB는 한 달 20~50만 PV 정도다. 만 단위 사용자라면 사이드 안쪽이고, 몇 만에서 수십 만으로 넘어가기 시작하면 5장의 외부 보강 패턴을 미리 읽어두는 게 좋다.

## 4.3 만들자마자 켜야 할 것 — Spend Management

Pro 계정을 만들고 첫 배포까지 마쳤다고 해보자. 이제 한숨 돌리고 카페에 가서 커피 한 잔 마시고 싶어진다. 그 전에 한 가지만 켜고 가자. **Spend Management**다.

Spend Management는 한도를 넘어가면 알림을 보내고, 임계를 넘으면 자동으로 일시정지까지 시켜주는 가드레일이다. 그런데 디폴트가 OFF다. 이게 좀 당황스러운 부분이다. Pro로 올라가면 자동으로 켜져 있을 것 같지만, 명시적으로 켜지 않으면 한도를 넘어도 그저 청구서에 더해지기만 한다.

왜 디폴트 OFF인지에 대한 비판은 인터넷에 많다. 그 논쟁은 7장에서 다시 다룬다. 4장에서 기억해야 할 것은 단 하나다. **Pro로 올라가자마자 가장 먼저 켜야 하는 한 가지가 Spend Management다.** 임계 알림 설정·자동 일시정지 임계·웹훅 연동 같은 구체적 페이지는 7장의 "Spend Management 설정 한 페이지"에서 본격적으로 다룬다. 4장에서는 "왜 켜는가"만 명확히 해두자.

켜는 이유는 단순하다. 사이드 단계에서 가장 무서운 건 청구서 폭탄이 아니라 **눈치채지 못한 채 청구서가 쌓이는 것**이다. 바이럴 한 번, LLM 봇 크롤링 한 번, 잘못 설정한 cron 한 번이 며칠 동안 조용히 한도를 넘으면, 월말에 카드 명세서를 보고서야 알게 된다. Spend Management는 그 며칠을 줄여준다. 임계의 70%·90%·100%에서 알림이 오고, 100%를 넘으면 자동 일시정지까지 걸린다. 일시정지가 무서워서 안 켜는 사람이 있는데, 잘못 켜진 cron으로 며칠 만에 $500을 잃는 것보다 한 번 일시정지 걸리고 메일로 깨닫는 편이 낫다.

지금 자기 프로젝트가 Pro 계정인데 아직 Spend Management를 켜지 않았다면, 이 장을 읽다 말고 켜고 와도 좋다. 정말이다.

## 4.4 시크릿 분리 — 환경별로 진짜로 나누자

토이 단계에서는 환경 변수가 거의 한 줄짜리였다. `DATABASE_URL`, 어쩌면 `OPENAI_API_KEY` 정도. 이걸 Production·Preview·Development 셋 다 같은 값으로 박아두고 굴리는 게 자연스러웠다.

사이드 단계로 올라오면 이 패턴이 슬슬 위험해진다. PR을 올릴 때마다 자동으로 만들어지는 preview 배포가 있다. 그 preview에서 production DB에 그대로 쓰기·읽기를 한다면, 잘못된 마이그레이션 한 번에 production 데이터가 폭발한다. preview가 검색엔진에 인덱싱이라도 되면 더 황당한 일이 벌어진다. PR 작업 중인 미완성 페이지가 검색 결과에 뜨고, 거기서 production 데이터 일부가 노출되는 식이다.

그래서 사이드 단계의 첫 가드레일은 이거다. **production 시크릿을 preview에 그대로 재사용하지 말자.**

Vercel은 환경 변수를 Production / Preview / Development 세 환경으로 나눠서 저장할 수 있게 해준다. 같은 키 이름이라도 환경별로 다른 값을 줄 수 있다. 이 분리는 그냥 옵션이 아니라 사이드 단계의 운영 룰이다.

| 변수 | Production | Preview | Development |
|------|-----------|---------|-------------|
| `DATABASE_URL` | prod DB | staging DB 또는 PR별 임시 DB | 로컬 SQLite/Docker |
| `STRIPE_SECRET_KEY` | live key | test key | test key |
| `OPENAI_API_KEY` | 운영용 키 + budget cap | 별도 키 + 더 낮은 budget | 개인 키 |
| `ADMIN_TOKEN` | 강한 시크릿 | preview 전용 토큰 | 개발용 |

이 표를 보면 "정말 다 나눠야 할까?"라는 의문이 들 수 있다. 답은 **DB·결제·Auth·Admin 네 가지는 무조건 나누고, 나머지는 상황 보고 결정**이다. DB는 데이터가 섞이면 복구가 어렵다. 결제는 test/live key를 헷갈리면 사고로 직결된다. Auth는 세션·쿠키 도메인이 섞이면 추적이 안 된다. Admin은 권한이 새면 가장 빨리 폭발한다.

로컬 개발에서는 `vercel env pull`을 쓰면 Vercel에 등록한 변수를 `.env.local`로 끌어올 수 있다.

```bash
# 프로젝트 루트에서
$ vercel link              # 한 번만, 로컬과 Vercel 프로젝트 연결
$ vercel env pull          # Development 환경 변수를 .env.local로
```

`.env.local`은 `.gitignore`에 들어가 있어야 한다. `vercel env pull`을 처음 돌려보면 `.env.local` 첫 줄에 "이 파일은 Vercel CLI가 생성했다"는 주석이 박힌다. 이 패턴을 잡아두면 새 팀원이 합류했을 때도 `vercel link → vercel env pull` 두 줄로 환경이 맞춰진다. README에 두 줄을 박아두는 편이 낫다.

## 4.5 Sensitive 플래그 — 의심 시 모두 켜자

환경 변수를 Vercel에 넣을 때 보면 옆에 작은 체크박스가 있다. **Sensitive**라는 플래그다. 이걸 켜두면 한 번 저장한 후에는 dashboard나 API에서 그 값을 다시 읽을 수 없게 된다. 빌드·런타임에서는 정상적으로 쓰이지만, 사람이 UI를 통해 다시 꺼내볼 수 없다는 뜻이다.

이 플래그를 처음 보면 살짝 찜찜하다. "값을 다시 못 읽으면 어떡해, 잃어버리면?" 그래서 잘 안 켜는 사람이 많다. 이게 함정이다.

2026년 4월 Vercel 보안 사고에서 노출된 게 정확히 이 **non-sensitive로 분류된** 환경 변수들이었다. Sensitive로 처리된 변수는 무사했다. non-sensitive 변수는 Vercel 내부에 decrypt 가능한 형태로 저장되기 때문에, 내부 침해가 일어나면 그대로 읽힐 수 있다. Sensitive로 켜두면 그 자리에 한 번 더 자물쇠가 걸린 것과 같다.

사고의 자세한 해부와 회전 절차는 8장에서 다룬다. 4장에서 정해야 할 룰은 단 한 줄이다. **의심 시 모두 켠다.** "이게 비밀일까 아닐까" 망설여진다면 켜라. UI에서 다시 못 읽는 게 단점이 아니라 보안 자산이다. 잃어버리면 새로 만들어서 다시 넣으면 된다. 그게 못 막을 사고보다 훨씬 가볍다.

켤 후보를 리스트로 정리하면:

- DB 연결 문자열 (URL에 비밀번호가 포함되니까)
- API 키 류 전부 (OpenAI, Stripe, SendGrid, Twilio, …)
- JWT signing secret, NextAuth `AUTH_SECRET`
- Webhook signing secret
- Admin·관리자 권한 토큰
- 외부 OAuth client secret

이 정도는 그냥 다 Sensitive로 켜는 편이 낫다. "Public 한 URL 하나만 non-sensitive로 두면 되겠다" 정도의 분류로 시작하자.

## 4.6 Edge Middleware — Basic Auth와 룰북

사이드 단계에서 자주 마주치는 상황이 있다. "이 페이지는 운영 중인데, 일단 친구들끼리만 쓰고 싶다." 또는 "특정 IP에서 비정상적인 요청이 와서 막고 싶다." 이걸 매번 페이지마다 처리하기엔 번거롭다.

Edge Middleware가 이런 역할을 맡는다. 모든 요청이 라우트 핸들러에 도달하기 전에 **엣지에서 한 번 가로채서** 인증·차단·리다이렉트·헤더 조작을 할 수 있다. PoP에서 처리되니 빠르고, Next.js 프로젝트라면 `middleware.ts` 한 파일로 시작할 수 있다.

가장 쉬운 패턴인 Basic Auth부터 보자.

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'

export function middleware(req: NextRequest) {
  const auth = req.headers.get('authorization')
  const expected = `Basic ${Buffer.from(
    `${process.env.BASIC_AUTH_USER}:${process.env.BASIC_AUTH_PASS}`
  ).toString('base64')}`

  if (auth !== expected) {
    return new NextResponse('Auth required', {
      status: 401,
      headers: { 'WWW-Authenticate': 'Basic realm="Secure"' },
    })
  }
  return NextResponse.next()
}

export const config = { matcher: ['/((?!_next|favicon.ico).*)'] }
```

`BASIC_AUTH_USER`·`BASIC_AUTH_PASS`는 Sensitive로 켜두자. matcher에서 `_next` 같은 정적 자산을 제외하지 않으면 빌드 산출물 로딩까지 인증이 걸려서 페이지가 깨진다. 처음 도입할 때 자주 빠지는 함정이니 기억해두자.

비슷한 패턴으로 IP rate limit, 특정 국가 차단, A/B 분기, www → apex 리다이렉트 같은 룰을 짤 수 있다. Vercel 공식 템플릿에도 표준 예제가 여럿 있다.

다만 Edge Middleware에 **무거운 로직을 넣으면 안 된다**. 모든 요청마다 실행되는 자리이기 때문에, DB 쿼리나 LLM 호출 같은 걸 넣으면 트래픽이 늘 때 비용이 폭발하고 응답이 느려진다. fetch·헤더 조작·간단한 토큰 검증 정도가 적정선이다. 무거운 로직 금지가 왜 *원칙*이 되는지, 미들웨어 폭주 사례가 어떻게 청구서로 돌아오는지는 8장에서 메커니즘과 함께 다룬다. 4장에서는 룰북만 잡아두자.

> **Edge Middleware 룰북 (사이드 단계)**
> - Basic Auth, JWT 검증, 헤더 주입, 리다이렉트, 간단한 rate limit — OK
> - DB 쿼리, LLM 호출, 외부 API에 5xx 의존하는 로직 — 금지
> - matcher로 `_next/`·정적 자산 제외 — 필수
> - 시크릿은 Sensitive 플래그 ON — 필수

## 4.7 Web Analytics·Speed Insights는 *정말* 필요할 때만

Pro로 올라오면 Vercel 대시보드에 작게 뜨는 두 가지 add-on이 있다. **Web Analytics**와 **Speed Insights**다. 클릭 한 번으로 켜진다는 친절한 안내까지 붙어 있다. 그래서 일단 켜두는 사람이 많다.

이게 사이드 단계에서 조용히 새는 비용 중 하나다. 두 add-on은 각각 **프로젝트당** $10/월이다. 프로젝트가 두 개면 $40, 다섯 개면 $100이 거기서 더해진다. Web Analytics는 월 25K 이벤트까지 포함이고 그 다음 1K당 $0.25가 더 더해진다.

질문을 다시 던져보자. **이 add-on이 정말 필요한가?**

- 외부 무료 분석 도구(Plausible, Umami, GA4)가 이미 붙어 있나? 그렇다면 Web Analytics는 중복일 가능성이 높다.
- Speed Insights를 켜면 보겠다는 결심이 있나? Core Web Vitals 수치를 매주 들여다볼 게 아니라면, 켜두기만 한 채 잊혀진다.
- 이 프로젝트가 비즈니스 의사결정에 분석 데이터를 쓰나? 사이드 단계라면 보통 아직 아니다.

켜는 시점은 **명함이 박힌 메인 프로덕트 한 개**부터다. 사이드의 모든 프로젝트에 켜둘 필요는 없다. 토이 단계에서 굴리던 부 프로젝트들에 무심코 켜두면 한 달에 $30~50이 묻혀서 빠져나간다. 자기 프로젝트 리스트를 한 번 훑어보고, "이 프로젝트는 분석이 정말 필요한가"를 한 번씩 물어보고 켜는 편이 낫다.

## 4.8 Cron Jobs를 다회로 굴려보자

이제 사이드 단계의 진짜 활용 영역으로 가자. **Cron Jobs**다.

Hobby 단계에서는 cron이 일 1회로 묶여 있어서 답답했다. Pro로 올라오면 빈도 제한이 풀린다(공식 한도는 변동될 수 있으니 콘솔에서 매번 확인하자). 그러면 갑자기 손이 자유로워진다. 그 자유 안에서 사이드 단계 사람들이 실제로 cron을 어떻게 쓰는지 네 가지 패턴을 살펴보자.

**패턴 1 — Scheduled DB 정리.** 만료된 세션 토큰, 임시 업로드 파일, 30일 지난 게스트 데이터를 새벽에 한 번씩 비운다.

```typescript
// app/api/cron/cleanup/route.ts
import { db } from '@/lib/db'

export async function GET(req: Request) {
  if (req.headers.get('authorization') !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response('Unauthorized', { status: 401 })
  }
  await db.session.deleteMany({ where: { expiresAt: { lt: new Date() } } })
  return Response.json({ ok: true })
}
```

```json
// vercel.json
{ "crons": [{ "path": "/api/cron/cleanup", "schedule": "0 3 * * *" }] }
```

`CRON_SECRET`은 Sensitive로 두고, Vercel cron에서 자동으로 실어 보내는 헤더로 인증한다. 이 한 줄짜리 인증을 빼먹으면 누구나 GET으로 DB 정리를 트리거할 수 있다. 잊지 말자.

**패턴 2 — 외부 API 폴링.** 환율, 주가, GitHub 이벤트, 공공데이터 — 자기 서비스에 띄울 외부 데이터를 5분·30분·1시간 간격으로 미리 받아둔다. 사용자가 페이지에 들어왔을 때 외부 API에 매번 직접 부르면 응답도 느리고 rate limit도 무섭다. cron으로 미리 받아 KV·Edge Config에 캐싱해두면 페이지는 캐시만 읽고 끝낸다.

**패턴 3 — ISR `revalidatePath` 트리거.** Next.js의 ISR은 "60초 지난 다음 요청부터 재생성"이라는 lazy 모델이다. 그런데 어떤 페이지는 데이터가 바뀌었을 때 *즉시* 갱신되길 원한다. 이때 cron으로 정기적으로 `revalidatePath`/`revalidateTag`를 호출하면 페이지를 강제로 신선하게 유지할 수 있다.

```typescript
// app/api/cron/refresh-blog/route.ts
import { revalidatePath } from 'next/cache'

export async function GET(req: Request) {
  if (req.headers.get('authorization') !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response('Unauthorized', { status: 401 })
  }
  revalidatePath('/blog')
  revalidatePath('/sitemap.xml')
  return Response.json({ ok: true })
}
```

ISR의 `revalidate = 60` 같은 표기가 흔히 오해를 부르는데, 이 오해 자체는 9장에서 짚는다. 4장에서는 cron으로 강제 재생성을 트리거하는 패턴이 가능하다는 점만 잡아두자.

**패턴 4 — 알림 발송.** 매일 아침 사용자 디지스트, 매주 월요일 운영자 리포트, 결제 실패 retry — 이런 시간 기반 알림은 cron의 가장 자연스러운 사용처다. 외부 메일·Slack·Discord 웹훅으로 한 줄 보내고 끝낸다.

여기서 한 가지 잊지 말아야 할 사실이 있다. **Cron Jobs의 매 실행은 함수 invocation 한 번을 차지한다.** 다시 말해 함수 quota에 그대로 차감된다. 5분 간격 cron이면 한 달 8,640번이고, 1분 간격이면 43,200번이다. 무료 1M invocation 한도 안에서는 여유가 있지만, cron이 실행 안에서 다시 외부 API를 폴링하고 DB 쿼리를 돌리면 CPU-hour와 메모리 GB-hour까지 쌓인다. cron을 "0원에 도는 자동화"로 착각하지 말고, **함수 호출이 시간표에 따라 도는 것**으로 인식하는 편이 낫다. 빈도와 실행 시간이 곱해진다는 감각만 잡고 시작하자.

## 4.9 OG Image — 공유될 때 다르게 보이기

사이드 단계에서 자주 빼먹는 일이 있다. **OG 이미지**다. 트위터·페이스북·슬랙에 자기 사이트 링크를 붙였을 때 미리보기 카드가 어떻게 뜨는지 본 적이 있을 것이다. 어떤 사이트는 잘 디자인된 이미지에 제목까지 박혀서 뜨고, 어떤 사이트는 작은 파비콘 하나 또는 그냥 빈 카드로 뜬다. 이 차이가 클릭률에 그대로 영향을 준다.

토이 단계에서는 정적 이미지 한 장을 `public/og.png`로 박아두는 정도로 충분했다. 사이드 단계로 오면 페이지마다, 글마다, 사용자마다 다른 OG 이미지가 필요해진다. "토비의 블로그"보다 "Vercel 사이드 단계 — 4가지 트리거 - 토비의 블로그"가 박힌 이미지가 클릭을 부른다.

매번 디자이너가 이미지를 만들어줄 수는 없으니, 동적으로 OG 이미지를 생성해야 한다. Next.js의 `ImageResponse` API와 Vercel 엣지가 이걸 빠르게 끝내준다.

```typescript
// app/blog/[slug]/opengraph-image.tsx
import { ImageResponse } from 'next/og'

export const runtime = 'edge'
export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default async function OGImage({ params }: { params: { slug: string } }) {
  const post = await getPostMeta(params.slug)

  return new ImageResponse(
    (
      <div
        style={{
          height: '100%',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          padding: 80,
          background: '#0b0b10',
          color: '#fff',
          fontSize: 64,
          fontWeight: 700,
        }}
      >
        <div style={{ opacity: 0.6, fontSize: 28 }}>토비의 블로그</div>
        <div style={{ marginTop: 24 }}>{post.title}</div>
      </div>
    ),
    size,
  )
}
```

Next.js 13 이상의 App Router에서는 라우트 폴더 안에 `opengraph-image.tsx`를 두면 된다. 빌드 후에는 `/blog/{slug}/opengraph-image`로 동적으로 생성된 이미지가 뜨고, 메타 태그도 자동으로 박힌다. 함수는 엣지에서 돌고, JSX로 그린 화면을 PNG로 내려준다. 글마다 따로 디자인 작업을 하지 않아도 자동으로 차별화된 카드가 만들어진다.

이걸 사이드 단계에 넣어두면 SEO·공유 양쪽에서 차이가 난다. 이미지 하나에 들이는 손이 적은데, 공유될 때 받는 인상은 분명히 달라진다. 이 단계의 가성비 좋은 한 수다.

## 4.10 사이드 단계의 비용·보안 미니 점검표

사이드 단계까지 정리한 내용을 한 장으로 압축하면 이렇다.

**비용 미니 점검표**

- Spend Management ON — 임계 알림 70/90/100% (자세한 설정은 7장)
- Web Analytics·Speed Insights는 메인 프로덕트 한 개에만
- Cron 빈도와 실행 시간을 한 번 손으로 곱해보기
- Image Optimization 기본값 그대로 — 폭증하면 5장으로
- 한 달 청구서를 첫 달·셋째 달에 한 번씩 직접 열어보기

**보안 미니 점검표**

- 환경 변수 Production / Preview / Development 분리 (DB·결제·Auth·Admin은 무조건)
- Sensitive 플래그 — 의심 시 모두 ON
- `.env.local`은 `.gitignore`에 (당연하지만 새 팀원 합류 시 한 번 더 확인)
- Edge Middleware로 Basic Auth 또는 IP rate limit
- preview에서 production DB 절대 재사용 금지

이 두 표가 손에 익을 때까지 사이드 단계가 이어진다. 익숙해지면 다음 단계로 넘어갈 준비가 된다.

## 4.11 다음 단계로 넘어가는 신호

사이드 단계에서 초기 스타트업 단계로 넘어가는 신호는 어디에 있을까. 가장 명확한 신호 두 가지를 짚어두자.

**첫째, 트래픽이 만 단위를 안정적으로 넘기 시작한다.** 어느 글이 공유돼서 하루만 1만 PV를 찍은 게 아니라, 평일 평균이 만 단위에 들어오는 상태. 이때부터 1TB Bandwidth 한도가 흔들리기 시작한다. 페이지 무게에 따라 다르지만, 평균 3MB 페이지 기준으로 월 30만 PV가 1TB 근처다. 한 번 넘기 시작하면 다음 달, 그다음 달 곡선이 급해지는 일이 잦다.

**둘째, 청구서에 'Image Optimization'이 잡히기 시작한다.** Image API는 사이드 단계에서는 거의 무료처럼 쓰이다가, 트래픽이 만을 넘기 시작하면 가장 빠르게 폭증하는 단일 항목이다. LLM 봇이 사이트를 크롤링하기 시작하면 더 빨라진다. 이 청구서가 처음 보이면 5장의 외부 CDN 분리 패턴을 미리 읽어두는 편이 낫다.

이 외에도 신호는 더 있다 — DB 연결 한도가 답답해지기 시작한다, 팀원이 5명을 넘는다, 컴플라이언스 질문지가 처음 메일로 들어온다. 어느 신호든 두 개가 겹치면 다음 장이 자기 단계다.

5장은 한도가 처음 흔들릴 때, 비용 곡선이 어떻게 꺾이고 어떻게 펴는지를 본다. 이미지를 외부 CDN으로 분리하고, 도메인 앞에 Cloudflare를 놓고, AI 기능을 어떻게 빠르게 붙이는지까지 — 사이드의 가드레일 위에 외부 보강과 운영 깊이를 더하는 단계다. 사이드를 잘 굴리고 있다면 그대로 따라오자.
