# 8장. 보안 — 시크릿·Preview·사고에서 살아남기

## 8.1 단계마다 흩어둔 보안 메모를 한자리에

여기까지 오면서 보안 이야기를 토막토막 흘려두었다. 한번 모아보자.

3장에서는 OAuth 키 한 줄을 dashboard에 붙여 넣으며 `Sensitive` 체크박스를 켰다. 그땐 그저 "켠다"였다. 4장에서는 의심스러우면 그냥 다 켜자고 규칙을 못 박았다. 결제 키든 webhook signing secret이든 가리지 말고. 5장에서는 트래픽이 흔들리기 시작할 때 WAF Managed Rulesets, BotID, Attack Challenge Mode를 *언제* 켜는지를 정했다. 어느 임계를 넘어가면 어떤 스위치를 올려야 하는지의 결정표였다.

이 메모들을 따로따로 두면 묘하게 찜찜하다. *왜* 그렇게 해야 하는지가 빠져 있기 때문이다. Sensitive 체크박스가 무엇이 다른지, 회전 한 번에 왜 모든 환경을 재배포해야 하는지, BotID가 어떤 메커니즘으로 봇을 잡아내는지 — 이 자리에서 한 번에 본다. 결정 뒤에 어떤 메커니즘과 어떤 사고가 깔려 있는지 본다.

이 장의 큰 질문은 하나다. 환경 변수, preview, 도메인, DDoS — 이 네 자리 가운데 어디가 가장 새기 쉽고, 무엇을 바꿔야 하는가? 하나씩 풀어보자.

## 8.2 환경 변수 두 종류 — 구조적 차이

Vercel dashboard의 환경 변수 입력란에는 별것 아닌 듯 보이는 체크박스 하나가 있다. `Sensitive`라는 이름이다. 처음 이 화면을 만난 사람은 거의 다 같은 질문을 한다. "이거 켜는 거랑 안 켜는 거랑 뭐가 다르지?"

흔히 하는 답은 "켜면 dashboard에서 다시 못 본다"이다. 맞는 말이지만, 그게 본질은 아니다. 다시 못 보는 건 결과이고, 그 뒤에 더 중요한 사실이 깔려 있다.

Sensitive를 끈 일반 환경 변수는 Vercel 내부에서 *복호화 가능한* 형태로 보관된다. 빌드 시점에 주입하고 dashboard에서 다시 읽기 위해, 어디엔가 키가 있고 그 키로 풀 수 있다. 반면 Sensitive를 켜면 다른 경로를 탄다. 한 번 저장된 뒤에는 dashboard로도, API로도, 그 어떤 사람의 손으로도 다시 평문으로 꺼내올 수 없다. 빌드 머신과 함수 런타임 안에서만 풀려서 환경 변수로 주입되고, 그 바깥에는 평문이 존재하지 않는다. 키 자체의 처리 경로가 다르다는 얘기다.[^1]

[^1]: <https://vercel.com/docs/environment-variables/sensitive-environment-variables>

여기까지만 들으면 "그럼 다 켜면 되네"라고 생각하기 쉽다. 정확하다. 사실 그게 4장에서 이미 정한 규칙이다. *의심 시 모두 켠다.* dashboard에서 다시 못 보는 게 단점처럼 느껴지지만, 그 불편이 실은 자산이다. 다시 못 본다는 건 다른 누구도 못 본다는 뜻이고, 그게 우리가 시크릿에서 원했던 바로 그 속성이기 때문이다.

그렇다면 무엇을 끄고 무엇을 켤 것인가. 기준을 한 줄로 정리해두자. **외부에 새는 즉시 누가 책임져야 할 만한 값이면 무조건 Sensitive다.** DB connection string, JWT signing key, 결제 webhook secret, third-party API key, Admin token. 반대로 노출돼도 사고가 안 나는 값 — 가령 `NEXT_PUBLIC_SITE_URL`처럼 어차피 브라우저로 가는 값 — 은 굳이 켤 이유가 없다.

그런데 이 기준이 사람마다 헷갈린다. "이건 좀 애매한데"라는 자리가 자주 나온다. 그럴 땐 켜자. 끄는 쪽으로 기우는 게 더 위험하다. 그리고 환경별로 분리하는 것도 잊지 말자. Production·Preview·Development는 각각 다른 값을 본다. 특히 DB와 결제와 Auth와 Admin — 이 네 자리는 환경 사이를 넘나들면 안 된다.[^2]

[^2]: <https://www.shipsafer.ai/blog/vercel-deployment-security>

## 8.3 2026년 4월의 사고 — Lumma Stealer가 Vercel까지 닿은 길

이 구분이 왜 중요한지를 한 번에 이해하게 만든 사건이 있다. 2026년 4월, Vercel 자체가 보안사고를 겪었다.[^3]

[^3]: <https://vercel.com/kb/bulletin/vercel-april-2026-security-incident>, <https://www.trendmicro.com/en_us/research/26/d/vercel-breach-oauth-supply-chain.html>, <https://blog.gitguardian.com/vercel-april-2026-incident-non-sensitive-environment-variables-need-investigation-too/>

상황을 따라가 보자. 어느 스타트업 — 사후 보고서에 Context.ai로 등장하는 회사 — 의 직원 한 명이 자기 PC에서 third-party AI tool을 받아 썼다. 그 도구의 어딘가에 Lumma Stealer가 묻어 있었다. Lumma Stealer는 잘 알려진 정보 탈취 악성 코드다. 브라우저 쿠키, 저장된 세션, 자격증명 캐시를 통째로 긁어 외부로 송출한다. 직원 PC가 감염된 순간, 그 사람이 로그인한 모든 SaaS의 세션이 사실상 공격자에게 넘어갔다.

이 가운데에는 Google Workspace 세션이 있었다. 공격자는 OAuth 토큰을 손에 넣었고, 그걸로 그 직원이 SSO로 연결해둔 다른 SaaS들에 접근할 수 있었다. 그 가운데 하나가 Vercel이었다.

여기까지는 Vercel의 잘못이라기보다 공급망의 잘못에 가깝다. 직원 PC → AI 도구 → OAuth → SSO → SaaS, 이 사슬 어디든 끊기지 않으면 일어날 수 있는 일이다. 진짜 무서운 건 그 다음이었다.

Vercel 내부에 들어간 공격자는 자기가 접근 가능한 프로젝트들의 환경 변수를 *조회*하기 시작했다. 그리고 non-sensitive로 분류된 변수들을 통째로 enumerate했다. 앞 절에서 본 그 구조 그대로다. non-sensitive 변수는 Vercel이 복호화할 수 있는 형태로 갖고 있다. 내부에 들어온 공격자에게도 — 적절한 권한만 있다면 — 마찬가지였다. 일부 데이터는 평문 형태로 손에 떨어졌다.

반면 Sensitive로 처리된 변수들은 무사했다. 공격자도 그 바깥에서는 풀 수 없는 형태였기 때문이다. dashboard로 다시 못 보는 그 불편이, 정확히 이 순간에 자산으로 환산됐다.

여기까지가 한 줄로 요약 가능한 사실이다. 이제 등골이 서늘해지는 부분으로 가자.

## 8.4 사고에서 배운 것 — non-sensitive에도 비밀이 산다

사고 직후, 보안 분석가들이 한목소리로 짚은 게 있다. "non-sensitive로 분류된 변수에도 사실 비밀이 자주 들어 있다."[^4]

[^4]: <https://blog.gitguardian.com/vercel-april-2026-incident-non-sensitive-environment-variables-need-investigation-too/>, 한국어 정리는 <https://news.hada.io/topic?id=28700>

생각해보자. 우리가 환경 변수를 처음 등록할 때 어떻게 하는가. `DATABASE_URL` 한 줄을 붙여 넣는다. 그 한 줄에는 호스트, 포트, 데이터베이스 이름, 사용자명, 그리고 비밀번호가 다 들어 있다. 비밀번호 한 토막 때문에 그 줄 전체가 시크릿이다. `NEXTAUTH_SECRET`도 마찬가지다. JWT signing에 쓰이는 값이라 노출되면 토큰을 위조당한다. webhook signing key, internal admin URL, OAuth client secret — 다 같다.

그런데 우리는 이런 값들을 무심코 일반 환경 변수로 넣어왔다. "이건 그냥 connection string이지 시크릿이 아니지"라고 생각하면서. 4월 사고는 그 무심함의 비용을 보여줬다. non-sensitive로 분류한 순간, 우리는 그 값에 대해 "Vercel 인프라가 풀 수 있는 형태로 둬도 괜찮다"고 결정한 셈이다. 평소엔 괜찮다. 인프라가 뚫리지 않는 이상은. 그런데 인프라는 뚫린다.

여기서 우리가 가져갈 교훈은 두 가지다.

첫째, 환경 변수의 분류 기준을 다시 잡자. "DB connection이라서 시크릿이 아니다"가 아니라 **"안에 비밀번호가 한 토막이라도 있으면 시크릿이다"**가 맞다. 의심 시 모두 켠다는 4장의 규칙이 정답이었다는 게 이 사고로 검증된 셈이다. 이미 등록된 변수들도 한 번 훑어보자. `*_URL`, `*_SECRET`, `*_TOKEN`, `*_KEY`로 끝나는 이름들 가운데 Sensitive가 안 켜진 게 있다면 지금 켜자.

둘째, 회전이다. 사고가 났든 안 났든, 이미 평문으로 노출됐을 가능성이 있는 모든 시크릿은 새 값으로 바꿔야 한다. 단순히 dashboard에서 값을 갈아끼우는 걸로 끝이 아니다. 회전이 어떻게 끝나는지를 다음 절에서 보자.

## 8.5 회전이 끝나는 자리 — 모든 환경 재배포

시크릿을 갈아끼웠다고 안심하면 곤란하다. Vercel의 배포 모델 한 가지를 기억해두자. **각 배포는 그 시점의 환경 변수 값을 자기 안에 동결해서 보관한다.** 함수가 호출되면 그 동결된 값으로 돈다. dashboard에서 환경 변수를 새 값으로 바꿨다고 해서 *과거에 만들어진 배포*가 그 값을 새로 읽어오지 않는다.

이게 무슨 뜻인가. preview URL 하나가 이미 떠 있다고 해보자. 두 달 전에 누가 PR 올려서 만들어진 거다. 그 preview는 그때 그 환경 변수 — 즉, *옛날* DB credential — 을 그대로 들고 있다. 누가 그 URL을 알고 있다면, 그리고 옛 credential이 새지 않은 채 살아 있다면, 그 preview를 통해 옛 자격증명으로 계속 들어올 수 있다.

그래서 회전 절차의 마지막 단계는 항상 같다. **모든 환경에서 재배포한다.** Production, Preview, Development. preview의 경우 살아 있는 deployment 자체가 많다면, 옛 deployment를 정리하고 필요한 것만 새로 trigger한다.[^5]

[^5]: <https://www.shipsafer.ai/blog/vercel-deployment-security>

회전 절차를 한 번에 정리해두자.

1. 새 시크릿을 발급한다 (DB user 새로 파거나, signing key 새로 만들거나, OAuth client secret 회전).
2. Vercel dashboard에서 해당 환경 변수의 값을 새 값으로 갈아끼운다. Sensitive 플래그가 안 켜져 있다면 이번 기회에 켠다.
3. **Production을 재배포한다.** 단순히 last build 같은 걸로 redeploy하지 말고, fresh build를 돌리는 게 안전하다.
4. Preview·Development도 동일하게 처리한다. 살아 있는 PR preview들은 새 commit을 trigger하거나 deployment를 archive한다.
5. *옛 시크릿을 폐기*한다. DB user면 drop, OAuth면 revoke. 새 값이 잘 도는 걸 확인하고 끊는다.

3번이 빠지는 게 가장 흔한 실수다. 등골이 서늘하지 않은가. 갈아끼웠다고 끝낸 자리에 옛 값이 그대로 살아서 돌고 있는 셈이다. 회전은 *재배포가 끝나는 자리에서야* 끝난다. 잊지 말자.

## 8.6 Preview 환경의 폭발 반경 — 분리가 답이다

Preview 이야기를 본격적으로 해보자. Vercel을 처음 쓸 때 가장 매력적이라고 느끼는 기능이 PR마다 자동으로 떠오르는 preview deployment다. PM도 디자이너도 링크 한 줄로 들어와서 직접 만져본다. CI에 사람 한 명 더 들어온 느낌이다.

그런데 이 매력의 뒷면에 폭발 반경이 있다. 정말 production 시크릿을 preview에 그대로 둘 건가? 한 번만 더 생각해보자.

나쁜 시나리오를 가정해보자. 어느 인턴이 첫 PR을 올린다. preview가 자동으로 뜬다. 그 인턴의 PR 코드 어딘가에 — 본인은 모르고 — `console.log(process.env.DATABASE_URL)`이 한 줄 들어가 있다. preview를 열면 콘솔에 production DB credential이 그대로 찍힌다. 또는 그 인턴이 디버그 목적으로 임시 endpoint를 하나 만들었다. `/api/debug-env`가 환경 변수 dump를 그대로 응답한다. preview URL이 어딘가에 캐시되거나 슬랙 검색에 걸리는 순간, 누구나 그 dump를 본다.

Production이라면 코드 리뷰에서 잡혔을 것들이 preview에서는 *환경 자체가 같으니까* 똑같이 폭발한다. PR마다 production 폭발 반경이 새로 생긴다는 얘기다.[^6]

[^6]: <https://www.shipsafer.ai/blog/vercel-deployment-security>

답은 두 가지다.

**첫째, preview에는 preview 전용 시크릿을 쓴다.** Production DB와는 다른 인스턴스. 같은 스키마를 가진 staging DB나, 적어도 별도 user/role로 권한이 좁혀진 자격증명. 결제도 마찬가지다. Stripe면 test mode key, sandbox webhook. OAuth면 별도 client. 이 분리만 해두면, 위 시나리오들이 일어나도 폭발 반경이 staging 안에 갇힌다.

**둘째, preview를 외부에서 못 들어오게 한다.** 다음 절에서 본다.

## 8.7 `*.vercel.app`이 검색에 걸리는 자리 — robots.txt와 Deployment Protection

`my-app-git-feature-branch.vercel.app` 같은 URL을 본 적이 있을 것이다. PR 단위로 자동 생성되는 preview의 표준 도메인이다. 이 URL은 추측이 어려워 보이지만, 사실 그렇게 안전하지 않다. 도메인 패턴이 워낙 규칙적이라서 자동 스캐너가 흔하게 잡아낸다. 한국어 커뮤니티에서도 자주 거론되는 위험이다.

게다가 preview에서 production 사이트로 어딘가 외부 링크가 새는 순간, 검색 엔진 봇이 따라 들어가 인덱싱하기 시작한다. 운이 나쁘면 며칠 뒤 자기 회사 staging 페이지가 Google 검색 결과에 떠 있다. *staging인 줄 모르고* 들어와서 결제까지 시도하는 사용자가 생긴다. 끔찍한 일이다.

방어는 두 층으로 친다. 한 층은 봇용, 한 층은 사람용이다.

**봇용 — robots.txt.** preview 환경에서는 서비스 전체에 `User-agent: * / Disallow: /`를 응답하도록 한다. 가장 단순하게는 빌드 시점에 환경 변수 `VERCEL_ENV`를 보고 preview면 차단 robots.txt를, production이면 정상 robots.txt를 내보내는 분기 한 줄이다. 메타 태그로 `<meta name="robots" content="noindex">`를 넣는 것도 같이 가져가면 든든하다. 이건 어디까지나 *예의 바른* 봇을 막는 장치다. 인덱싱은 막지만, 의도적으로 들어오는 사람은 못 막는다.

**사람용 — Deployment Protection.** Vercel은 preview deployment 앞에 인증 게이트를 세우는 기능을 제공한다. 옵션이 세 가지다.[^7]

[^7]: <https://vercel.com/docs/deployment-protection>

- **SSO Protection** — 팀에 속한 Vercel 계정으로 로그인해야 들어간다. 가장 빈틈이 적다. 다만 Pro 이상 플랜에서 제공된다. 무료 플랜은 옵션이 제한된다.
- **Password Protection** — preview마다 단일 비밀번호를 걸어둔다. 외부 베타 테스터·고객 데모처럼 SSO를 줄 수 없는 상대에게 쓴다.
- **Allowlist** — 특정 IP·이메일에서만 들어오게 한다. 회사 사무실 IP나 클라이언트사 IP를 화이트리스트로.

3장에서는 이걸 그저 "켠다"로만 정해뒀다. 이 자리에서 결판을 내자. 원칙은 한 줄이다. **어떤 회사든 preview에는 SSO Protection을 기본으로 켠다.** 외부 공유가 필요한 deployment만 명시적으로 password 또는 allowlist로 풀어준다. SSO를 못 쓰는 무료 플랜이라면 password라도 켜두자. 아무 보호도 없는 preview를 그대로 운영하는 건 — 솔직히 — 폭발하기 딱 좋은 자세다.

## 8.8 도메인과 SSL — 자동화의 안전망과 사람이 챙길 자리

이번엔 도메인이다. 이 자리는 좀 다르다. 보안 사고의 단골이라기보다는, 자동화가 잘 돌아서 *조용히 망가질* 위험이 큰 자리다.

Vercel은 도메인을 붙이는 순간 Let's Encrypt를 자동으로 띄운다. 90일짜리 SSL 인증서를 만료 전에 알아서 갱신한다. 우리가 한 일이 없다. 그래서 잊고 산다. 그러다 어느 날 페이지가 SSL 경고를 띄우는 사고가 생긴다.[^8]

[^8]: <https://vercel.com/docs/domains/working-with-ssl>

이런 사고를 막기 위해 Vercel은 한 가지 안전망을 더 깔아뒀다. **만료 5일 전부터 백업 인증서를 미리 발급해 둔다.** 주 인증서 갱신이 어떤 이유로 실패해도 백업이 자동 fallback으로 들어간다. 다운타임을 거의 0에 가깝게 막는 장치다. 보통은 이걸로 충분하다.

그런데 자동화가 닿지 않는 두 자리가 있다. 사람이 챙겨야 한다.

**첫째, 외부 등록 도메인의 갱신.** Vercel이 SSL은 자동 갱신해도, 도메인 자체의 *등록 갱신*은 외부 registrar에 묶여 있다. Namecheap, GoDaddy, Gabia 어디든. 등록 갱신이 끊기면 SSL이 무슨 소용이 있나. 도메인이 만료된 자리에 어느 외부인이 그 도메인을 가로채서 사이트를 띄울 수도 있다. 끔찍한 시나리오다. registrar 쪽에 자동 갱신을 켜두자. 결제 카드 만료도 챙기자. 카드가 expired됐는데 자동 갱신이 시도되면 그대로 실패한다.

**둘째, custom SSL 인증서.** Let's Encrypt가 아니라 회사가 자체 발급한 SSL을 쓰는 경우가 있다. 엔터프라이즈 계약이 그러길 요구할 때가 있다. 이 경우엔 갱신이 사람의 손에 묶인다. 5일 전 백업도 자동으로 안 떨어진다. 만료일을 캘린더에 넣고, 갱신 절차의 책임자를 이름으로 정해두자. "그건 OO팀이 알아서 하겠지"라는 자세는 이 자리에서 가장 위험하다.

도메인은 한 번 망가지면 복구가 가장 까다로운 자산이다. 자동화가 잘 돌고 있을 때 더 의심하자.

## 8.9 WAF·BotID·Attack Challenge — 5장의 *언제* 뒤에 무엇이 도는가

5장에서는 임계 — 5분 동안 비정상 트래픽이 1만 RPS를 넘으면 어떤 스위치를 올린다 — 만 정했다. 이 자리에서 그 스위치들이 *어떤 메커니즘*인지 본다. 켤 때 무엇이 도는지 모르고 켜는 것보다, 알고 켜는 게 늘 낫다.

### 8.9.1 Vercel WAF — Managed Rulesets와 Custom Rules

Vercel WAF는 두 층으로 돈다. Managed Rulesets와 Custom Rules.[^9]

[^9]: <https://vercel.com/security/web-application-firewall>

**Managed Rulesets**는 Vercel이 큐레이션한 차단 규칙 묶음이다. 대표적으로 `Bot` ruleset(알려진 악성 봇 차단), `AI Bot` ruleset(LLM 학습 크롤러 차단)이 있다. 한 번 토글로 켜면 그 안의 수백 가지 규칙이 한꺼번에 도는 식이다. 운영 부담이 거의 없다는 게 매력이다. 다만 *일반론적이라* 우리 서비스에 맞춤으로 도는 건 아니다.

**Custom Rules**는 우리가 직접 짜는 규칙이다. "이 path로 1분에 100번 넘게 오면 차단", "이 country에서 오는 POST는 challenge", "이 User-Agent는 그냥 deny" 같은 식이다. 5장에서 결정한 임계들이 보통 여기로 들어간다. 강력하지만 잘못 짜면 정상 트래픽을 자르니까 조심하자.

### 8.9.2 BotID — invisible fingerprint의 메커니즘

이름이 모호한데, 메커니즘은 명료하다. BotID는 들어오는 클라이언트가 사람인지 봇인지를 *눈에 안 보이는* 수많은 신호로 판별한다. 브라우저 fingerprint, 마우스 움직임, 타이핑 패턴, JS 실행 환경의 미묘한 차이 — 봇이 흉내 내기 어려운 신호들의 조합이다.

이 신호를 모은 결과는 score 또는 metadata 형태로 Edge Middleware에 주입된다. 우리는 그걸 받아 다음 결정을 한다. score가 높으면 그대로 통과, 낮으면 rate limit을 빡세게 걸거나, 아주 낮으면 challenge로 보내거나, fraud detection 시스템으로 신호를 보낸다. CAPTCHA를 띄우지 않고도 봇을 가려낸다는 점이 핵심이다.[^10]

[^10]: <https://www.thisdot.co/blog/vercel-botid-the-invisible-bot-protection-you-needed>

5장에서는 "사람 트래픽 비율이 의심스러우면 BotID를 켠다"고 정했다. 메커니즘을 이해하면 *어디에* 켤지가 명확해진다. 회원가입, 로그인, 결제 시작, 쿠폰 코드 사용 — 봇이 가장 노리는 자리다. 이런 endpoint를 묶어서 BotID를 적용하고, score를 middleware에서 읽어 행동을 분기하자.

### 8.9.3 Attack Challenge Mode — 비상 스위치

마지막은 비상시에 한 번에 켜는 큰 스위치다. Attack Challenge Mode를 켜면 모든 트래픽이 일단 challenge 페이지를 거친다. 정상 사용자는 몇 초 내로 통과하지만, 봇은 거의 다 떨어진다.[^11]

[^11]: <https://vercel.com/docs/vercel-firewall/attack-challenge-mode>

이게 무서운 건 SEO에 영향을 주지 않는다는 점이다. 검색 봇은 별도로 식별되어 차단 흐름에 잘못 휘말리지 않는다. 그리고 모든 플랜에서 무료다. 차단된 트래픽은 과금되지 않는다는 점도 중요하다 — 비용 폭탄을 피하는 안전망이기도 하다.

DDoS Mitigation도 비슷한 원칙으로 돈다. 차단된 트래픽은 과금되지 않는다. 다만 *mitigation이 발동되기 전*에 처리된 분은 청구된다. 그래서 임계를 너무 늦게 잡으면 mitigation이 켜지기 직전까지 청구서가 누적된다. 이 한 줄이 5장에서 임계를 *낮은 쪽으로 보수적으로* 잡아둬야 했던 이유다.[^12]

[^12]: <https://vercel.com/docs/vercel-firewall/ddos-mitigation>

추가로, 외부 CDN(예: Cloudflare)을 Vercel 앞단에 두는 패턴이 강력한 흡수층이 된다. 트래픽 규모가 큰 SaaS라면 한 번 검토할 만하다.

## 8.10 Edge Middleware의 자리 — 무거운 로직 금지

Edge Middleware 이야기를 한 번 더 짚자. 보안 관련해서 흔히 빠지는 함정이다.

Edge Middleware는 매력적인 도구다. 모든 요청 앞에 끼어들어 헤더를 바꾸고, redirect를 걸고, A/B 분기를 하고, 인증 토큰을 검증한다. 5장에서 본 BotID metadata도 여기서 받는다. 빠르고, 글로벌하고, 사용자 가까이에서 돈다.

문제는 이 자리에 너무 많은 걸 넣고 싶은 유혹이 든다는 점이다. "어차피 모든 요청이 여기 지나가니까, 인증 검사도 여기서, DB 조회도 여기서, 권한 체크도 여기서…" 한 번에 다 처리하고 싶어진다. 난감해진다.

기억해두자. **Edge Middleware는 fetch와 헤더 조작 전용이다.** 그 이상은 들어가면 안 된다.[^13]

[^13]: <https://vercel.com/templates/edge-middleware>

이유가 두 가지다. 첫째는 런타임 제약이다. Edge Runtime은 Node API 대부분이 안 돈다. `fs`, `crypto.createHmac` 같은 흔한 것조차 import 자체가 실패한다. JWT 라이브러리 가운데 Web Crypto만 쓰는 것들은 통과하지만, 그렇지 않은 라이브러리는 그냥 죽는다. 둘째는 cold start와 비용이다. 모든 요청에 무거운 로직이 끼면 latency도 늘고 invocation 비용도 누적된다. 7장에서 본 청구서 폭탄 패턴 가운데 하나다.

원칙을 한 줄로 잡아두자. *Edge Middleware는 길목, Route Handler는 사무실.* 길목에서는 출입증 확인(JWT 서명 검증), 방향 전환(redirect), 표시(헤더 추가)만 한다. DB 조회·복잡한 권한 트리 평가·이메일 발송 같은 사무실 일은 Route Handler로 보낸다. 이 분리가 무너지면 5장에서 켜둔 보안 장치들이 오히려 서비스 자체를 느리게 만드는 역효과를 낸다.

## 8.11 컴플라이언스가 비기술 결정에 들어오는 두 자리

여기까지는 우리가 *직접* 손대는 보안이었다. 컴플라이언스는 결이 다르다. 우리가 손대는 게 아니라, *외부가* 우리에게 요구하는 보안이다. 비기술 의사결정에 — 영업, 계약, 플랜 선택에 — 보안이 끼어드는 자리다. 이 책의 독자가 마주칠 가장 흔한 두 시나리오를 보자.[^14]

[^14]: <https://vercel.com/docs/security/compliance>, <https://vercel.com/blog/vercel-supports-hipaa-compliance>

### 8.11.1 시나리오 (a) — B2B 엔터프라이즈 계약과 보안 questionnaire

스타트업이 첫 엔터프라이즈 고객을 잡았다고 해보자. 계약서가 오기 직전에 보안팀에서 questionnaire 한 장이 날아든다. 100여 줄의 체크리스트다. 그 안에 거의 반드시 들어 있는 두 줄.

> "귀사의 인프라 제공자는 SOC 2 Type 2 인증을 보유하고 있는가?"
>
> "귀사의 인프라 제공자는 ISO/IEC 27001 인증을 보유하고 있는가?"

이 두 줄에 "Yes"라고 답할 수 있어야 계약이 다음 단계로 간다. 답할 수 없으면 거기서 끊긴다.

다행히 Vercel은 두 인증을 모두 보유한다. SOC 2 Type 2, ISO 27001, PCI DSS, GDPR, EU-US DPF, ISO 27018, NIS 2, DORA 등 일반적인 B2B 요구는 거의 다 커버된다. 우리가 할 일은 두 가지다. **첫째, Vercel Trust Center에서 해당 보고서를 받아 questionnaire에 첨부한다.** **둘째, 우리 자체의 운영 — 직원 PC 보안, 접근 통제, 사고 대응 절차 — 도 같이 정리해둔다.** 인프라가 SOC 2여도 우리가 구멍이면 계약은 흔들린다.

이 시나리오에서 Vercel 플랜을 바꿀 필요까지는 없다. Pro로 충분하다. 다만 SSO Protection이 자유롭게 쓰이는 Pro 이상이라는 점, 그리고 dedicated support가 필요해지는 시점이 Enterprise라는 점은 기억해두자.

### 8.11.2 시나리오 (b) — 의료 SaaS와 HIPAA·Secure Compute

다른 결의 시나리오다. 의료·헬스케어 도메인의 SaaS는 시작부터 컴플라이언스가 결정 사항이다. 미국에서 환자 정보(PHI)를 다루는 순간 HIPAA가 적용된다. 한국 의료 도메인이라도, 미국 시장 진출을 검토하는 즉시 HIPAA 호환이 화두가 된다.

Vercel은 HIPAA를 지원한다. 다만 두 조건이 있다.

**첫째, Enterprise 플랜이어야 한다.** Pro에서는 HIPAA BAA를 체결할 수 없다.

**둘째, Secure Compute를 켜야 한다.** Secure Compute는 함수가 isolated network 환경에서 도는 모드다. 일반 Vercel 함수가 공유 인프라에서 도는 것과 달리, dedicated network 안에서 격리되어 PHI를 처리하는 데 필요한 격리 수준을 만족한다.

이게 의미하는 바는 명확하다. 의료 SaaS의 시작은 *Pro에서 잠깐 시작했다가 Enterprise로 옮긴다*가 아니라 *처음부터 Enterprise·Secure Compute를 전제한다*가 맞다. 비용 구조가 6장의 SaaS 단계와 비슷한 결이지만, 임계가 다르다. 컴플라이언스가 임계를 *위에서 끌어내리는* 셈이다.

이 두 시나리오에서 보듯, 컴플라이언스는 기술 결정이라기보다 사업 결정에 가깝다. 첫 엔터프라이즈 고객을 잡기 직전, 의료·금융 도메인 진출을 검토하는 시점, M&A 실사를 받는 시점 — 이런 자리에서 questionnaire와 BAA가 화두로 들어온다. 미리 준비하지 않으면 그 자리에서 막힌다. 잊지 말자.

## 8.12 마무리 — 의심 시 모두 켜고, 회전이 끝나는 자리까지 가자

8장을 한 줄로 묶어보자. **의심 시 모두 켜고, 환경을 분리하고, 회전은 재배포까지가 끝이다.**

세부적으로 가져갈 메모는 다섯 줄이다.

1. **환경 변수** — Sensitive를 의심 시 모두 켠다. non-sensitive에도 비밀이 산다는 사실을 4월 사고가 가르쳐줬다. `*_URL`, `*_SECRET`, `*_TOKEN`, `*_KEY` 패턴을 한 번 훑자.
2. **회전** — 값을 갈아끼우는 게 끝이 아니다. Production·Preview·Development *모두* 재배포한 자리에서 끝난다. 옛 시크릿 폐기까지가 한 묶음이다.
3. **Preview** — production 시크릿을 절대 재사용하지 않는다. SSO Protection을 기본으로 켜고, robots.txt로 봇을 막는다. PR마다 폭발 반경을 새로 만들지 말자.
4. **도메인·SSL** — Let's Encrypt 자동 갱신과 5일 전 백업이 안전망이다. 사람이 챙겨야 할 자리는 두 곳, 외부 registrar의 등록 갱신과 custom SSL의 만료 관리.
5. **WAF·BotID·Edge** — 5장의 *언제 켜는가* 뒤에는 Managed Rulesets, invisible fingerprint, challenge mode가 돈다. Edge Middleware는 fetch와 헤더 전용으로 좁혀두자.

그리고 컴플라이언스 두 자리 — B2B 첫 엔터프라이즈 계약(SOC 2 Type 2/ISO 27001), 의료 SaaS(HIPAA + Secure Compute, Enterprise 전용) — 는 비기술 결정이 보안에 묶이는 순간이다. 그 자리에서 당황하지 않도록 미리 알고 있자.

다음 9장에서는 결이 또 바뀐다. 8장까지 우리가 *Vercel을 잘 쓰는 법*을 봤다면, 9장에서는 *Vercel을 의심하는 법*을 본다. 자주 빠지는 함정, 잘 알려진 한도, vendor lock-in 논쟁의 두 관점, 그리고 — 정말 떠나야 할 때를 대비해서 — 비상 탈출 경로의 카탈로그까지. 잘 쓰면서도 언제든 떠날 수 있는 능력을 갖추는 게 마지막 장의 약속이다.
