# AWS 개발자를 위한 Cloudflare 본격 활용 가이드

**부제:** Workers·D1·R2부터 OpenNext·AI Gateway까지, 멘탈 모델을 다시 그리는 길잡이
**저자:** Toby-AI
**버전:** 1.0.0
**발행일:** 2026-05-05

---

## 서문

AWS에 익숙한 우리가 처음 Cloudflare 문서를 펼치면 묘한 위화감이 든다. 단어는 익숙하다. 서버리스, 함수, 객체 저장소, 데이터베이스, CDN. 그런데 표면 한 겹 아래로 내려가면 가정이 통째로 다른 풍경이 펼쳐진다. 리전이 없고, 컨테이너가 없고, 콜드스타트가 5ms 미만이고, S3 호환인데 egress가 무료라고 한다. "이거, 정말 production에서 굴러가는 게 맞나?" 한 번쯤 의심해 봤을 것이다. 그렇다고 외면하기에는 옆자리 동료가 슬랙에 OpenNext 후기를 자꾸 던지고, Hacker News 상단에는 Workers 이름이 자주 박힌다. 쳐다는 봐야겠는데, 어디서부터 봐야 할지 손에 잡히지 않는다.

이 책은 그 자리에 손을 내미는 책이다. *Cloudflare를 도입하자*고 권하는 책이 아니라, *자기 시스템에 Cloudflare가 들어올 자리가 있는지를 정직하게 결정하도록 돕는* 책이다. 두 자세는 다르다. 도입이라는 단어에는 새 제품을 안에 들이는 그림이 박혀 있다. 자리를 내준다는 단어에는 우리 아키텍처에 어울리는 한 자리에 한 손님이 들어오는 그림이 박혀 있다. 첫 번째는 광고고, 두 번째는 약속이다. 우리는 14장 내내 두 번째 자세를 흔들리지 않게 잡고 갈 것이다.

흐름은 단순하다. **왜** Cloudflare가 또 하나의 클라우드가 아닌지로 시작해(1장), 익숙한 멘탈 모델을 어디서 흔들어야 하는지를 짚고(2장), Mac에서 5분 만에 첫 Worker를 글로벌 PoP에 올린다(3장). 그러고 나서 AWS와 Cloudflare를 매핑하는 카탈로그를 펼치되 그 표가 거짓말이 되는 다섯 자리를 미리 표시해 두고(4장), "내 워크로드 중 무엇을 옮길 것인가"의 결정 도구를 손에 쥔다(5장). 6장부터 12장까지가 본격 실무다. Hono로 백엔드 골격을 다시 그리고, KV·D1·Durable Objects·R2로 데이터 자리를 채우고, OpenNext로 Next.js를 올리고, Hyperdrive로 RDS를 살려둔 채 컴퓨트만 글로벌로 흩뿌리고, Zero Trust로 보안 모델을 다시 그리고, Workflows·Queues·AI Gateway로 비동기·LLM 영역을 메운다. 그리고 13장에서 *운영과 정직한 한계*를 정면으로 마주하고, 14장에서 Strangler Fig 8단계로 모든 것을 시퀀스로 묶는다.

책 전체에 누적 실습 프로젝트 하나가 깔린다. **`toby-shop`이다.** 3장에서 한 줄짜리 Hello Worker로 시작해, 6장에서 Hono 라우팅·인증·미들웨어가 붙고, 7장에서 D1·KV로 사용자·세션이 들어오고, 8장에서 Durable Objects로 채팅방과 재고 동시성이 들어오고, 9장에서 Next.js 상점 프론트가 얹히고, 10장에서 Aurora Postgres가 Hyperdrive로 연결되고, 11장에서 어드민이 Access·Tunnel로 보호되고, 12장에서 결제 후 영수증 Workflow와 RAG 챗봇까지 자란다. 한 권을 다 읽고 나면, 손에 한 사이클이 굴러가는 작은 시스템이 남는다.

이 책이 약속하지 않는 것도 분명히 적어 두자. **이 책은 광고서가 아니다.** 모든 챕터에 *무너지는 자리* 박스가 들어 있다. Workers의 CPU time 한도가 어디서 발에 걸리는지, KV의 60초 전파 지연이 어디서 회귀가 되는지, Durable Objects가 어디까지 깊은 lock-in인지, 2025년 11/18·12/5 outage가 어떤 교훈을 남겼는지를 정직하게 짚는다. 광고는 다른 책이 하면 된다. 우리가 여기서 약속하는 것은 결정의 정직함뿐이다.

대상 독자는 *Spring·Java·Lambda·Step Functions·DynamoDB·CloudFront에 익숙한 백엔드 개발자*다. JavaScript/TypeScript에 알레르기가 없되 능숙하지 않아도 좋다. AWS 운영을 5년 이상 해봤고, 한 번쯤 "이거 다른 길도 있지 않나" 의심해 본 사람을 위한 책이다. 한 챕터에 한 시간씩, 14주를 들이면 손끝의 감각으로 자기 답을 손에 쥐게 된다. 처음부터 차례대로 읽는 것을 권하지만, 4장 매핑 카탈로그와 5장 결정 프레임은 어느 단계에서든 다시 펼쳐 볼 수 있는 빠른 참조용으로도 잘 작동한다. 부록 A부터 F까지는 책을 덮은 다음에도 계속 손에 들고 다닐 만한 한 장짜리 도구들이다.

이 책의 시간 도장은 2026년 5월이다. Cloudflare는 빠르게 변하는 영역이라, 어떤 페이지의 가격표나 베타 상태는 우리가 책장을 펼치는 그 순간에는 이미 다음 단계로 넘어가 있을 수 있다. 그래도 *멘탈 모델*은 잘 변하지 않는다. 우리가 잡으려는 것은 가격표가 아니라 가정이다. 가정이 손에 잡히면, 가격표가 바뀌어도 결정이 흔들리지 않는다.

자, 함께 시작해 보자. 첫 장을 펼치면 도쿄에서 280ms가 돌아오는 월요일 아침의 풍경부터 만난다.

---

## 차례

**서문**

**1부. 가정을 다시 그린다**
- 1장. 왜 또 하나의 클라우드가 아닌가 — Edge-first의 시대
- 2장. 멘탈 모델을 다시 그리자 — V8 Isolate가 바꾸는 가정
- 3장. 첫 Worker를 띄우자 — Mac에서 5분 만에 글로벌 배포

**2부. 지도와 나침반**
- 4장. AWS ↔ Cloudflare 매핑 카탈로그 — 1:1 표가 거짓말이 되는 지점들
- 5장. 옮길까 말까 — Cloudflare로 가야 할 워크로드 판별법

**3부. 본격 실무**
- 6장. Workers 본격 사용법 — Spring 멘탈을 Hono로 다시 그리자
- 7장. 데이터 1 — KV와 D1, 워크로드 패턴으로 골라 쓰기
- 8장. 데이터 2 — Durable Objects와 R2, 그리고 Cache API
- 9장. Next.js on Cloudflare — Workers Static Assets·OpenNext의 현실
- 10장. Hyperdrive로 RDS를 그대로 살려두기 — 가장 risk-low한 첫 발걸음
- 11장. 보안과 Zero Trust — Access·Tunnel·WAF·Turnstile·Auth.js
- 12장. AI·Workflows·Queues — Step Functions·SQS·`@Scheduled` 너머

**4부. 운영과 결정**
- 13장. 운영과 정직한 한계 — 비용·관측·outage·lock-in
- 14장. 마이그레이션 전략 — Strangler Fig 8단계로 어떻게 옮기는가

**후기**

**부록**
- A. Wrangler CLI 치트시트
- B. 진단 카드
- C. 비용 시뮬레이터 워크시트
- D. Python Workers 노트
- E. AWS ↔ Cloudflare 빠른 참조
- F. 트러블슈팅 + 2025 outage 타임라인

**참고자료**

---


## 1장. 왜 또 하나의 클라우드가 아닌가 — Edge-first의 시대

월요일 아침, 도쿄에 있는 사용자가 우리 API를 부르면 280ms가 돌아온다. 캘리포니아 본사 사무실에서는 60ms다. 같은 코드, 같은 데이터인데 5배 가까이 차이가 난다. CloudFront를 앞에 깔아도 첫 요청의 지연은 거의 줄지 않는다. 왜 그럴까?

이 책을 펼친 우리는 이미 답의 절반을 알고 있다. 코드가 us-east-1에 있기 때문이다. TLS 핸드셰이크와 DB 연결을 합치면 태평양을 건너는 라운드트립만 일고여덟 번이다. 그렇다면 코드를 도쿄에 두면 어떨까? 그게 그렇게 단순할 리 없다. 도쿄에 EC2를 한 대 더 띄우면 데이터는 어디서 오나, 세션은 어디서 공유하나, 비용은 두 배가 되지 않나. 시드니, 프랑크푸르트, 상파울루까지 사용자가 늘어나면 또 어떻게 할 것인가. 우리가 지난 10년 동안 익혀온 멘탈 모델 안에서는 모든 답이 또 다른 운영 부담으로 돌아온다. 리전을 더 늘리고, VPC를 더 그리고, 데이터 동기화를 더 짜야 한다.

Cloudflare는 이 질문을 다른 자리에서 다시 묻는다. "코드가 모든 곳에 있다면 어떨까?" 처음 들으면 마케팅 카피처럼 들린다. 하지만 그게 진짜로 가능하다면, 우리가 지난 10년 동안 짊어온 가정 — 리전을 고른다, VPC를 그린다, ALB 뒤에 Auto Scaling Group을 세운다 — 의 절반이 흔들린다. 함께 살펴보자. 이 책의 첫 페이지가 우리에게 약속하는 것이 바로 그것이다.

### "Cloudflare는 더 싼 Lambda다"라는 첫 인상

AWS를 오래 써온 개발자가 Cloudflare 문서를 처음 펼치면 가장 먼저 떠올리는 한 줄이 있다. "그러니까, 더 싼 Lambda네." Workers는 코드를 돌리니까 Lambda 같고, R2는 객체를 저장하니까 S3 같고, D1은 SQL을 받으니까 RDS 같다는 식이다. 표를 한 장 그리면 깔끔하게 정리된다. 그렇게 1:1로 매핑해 놓고 비용 계산기를 돌려보면 결론은 늘 비슷하다. "어, 정말 싸네. 그런데 우리 시스템을 진짜로 옮기면 깨질 것 같은데."

이 1:1 매핑이 바로 함정이다. 함정인 이유는 가격이 틀려서가 아니라, **두 플랫폼이 서로 다른 가정 위에 서 있기 때문**이다. AWS는 "리전 안에서 모든 것이 끝난다"는 가정 위에 쌓아 올렸다. 한 리전을 고르고, 그 안에 VPC를 그리고, 서브넷을 자른다. Lambda는 그 리전의 컨테이너를 띄워 함수를 돌리고, DynamoDB는 그 리전의 테이블에 쓰고, S3는 그 리전의 버킷에 올린다. 글로벌하게 만들고 싶으면 CloudFront를 앞에 두거나 Global Table을 켜면 된다. 그러나 본질은 "어떤 리전에 살 것인가"의 결정이 가장 먼저 온다.

Cloudflare는 그 가정을 출발선부터 다르게 잡는다. **코드는 모든 PoP에 동시에 배포된다.** 사용자가 도쿄에 있든 상파울루에 있든 가장 가까운 데이터센터에서 같은 코드가 응답한다. 리전은 고르는 게 아니라 사라진 자리다. 데이터의 위치는 리전이 아니라 jurisdiction(EU·UK 같은 법적 단위) 또는 location hint(D1·DO에서)로 표현한다. 코드와 데이터의 위치가 분리되고, 둘 다 사용자의 위치에 따라 동적으로 라우팅된다. 멘탈 모델 자체가 다르다.

그래서 1:1 매핑은 표면만 닮은 도구를 짝지어 놓고 안심하게 만든다. Lambda↔Workers는 둘 다 함수형 서버리스라서 옆에 두면 비슷해 보인다. 하지만 Lambda는 컨테이너(Firecracker microVM)를 띄우는 모델이고, Workers는 V8 isolate라는 더 가벼운 격리 위에서 돈다. 콜드스타트가 5ms 미만으로 떨어지는 대신 임의 바이너리·full Node API·OS syscall은 포기한다. 같은 "서버리스"라는 단어 아래에 다른 행성이 있다. 그 차이를 모르고 옮기면, Spring Boot 위에 올린 거대한 의존성 덩어리를 그대로 들고 가서 1MB 한도(또는 Paid 10MB)에 부딪혀 황당해진다. 끔찍한 일이다.

DynamoDB↔KV는 더 위험한 매핑이다. 둘 다 key-value니까 같다고 치면, 어느 날 production에서 secondary index로 쿼리하던 코드가 통째로 안 도는 광경을 보게 된다. KV는 secondary index가 없다. 범위 쿼리도 없다. eventually consistent라서 쓰고 나서 60초까지 다른 PoP에서는 옛 값이 보일 수 있다. Liftosaur라는 서비스가 Workers + KV로 시작했다가 DynamoDB로 회귀한 사례가 있는데, 가장 큰 이유 중 하나가 바로 이 KV의 한계였다. 1:1 매핑 표만 보고 옮긴 사람들의 공통된 후일담이다.

그렇다면 어떻게 해야 할까? 답은 단순하다. 매핑 표를 버리는 게 아니라, **매핑이 거짓말을 하는 경계선을 미리 알고 보는 것**이다. Lambda↔Workers는 "둘 다 서버리스"가 아니라 "둘 다 사용자 코드를 실행하지만, 컨테이너냐 isolate냐의 격리 모델이 다르다"로 읽어야 한다. DynamoDB는 KV로 매핑되는 게 아니라, **사용 패턴별로** KV·D1·Durable Objects 셋 중 하나로 갈라진다. read-heavy 세션·플래그라면 KV, 관계형 SQL이라면 D1, 강한 일관성·per-entity 상태라면 DO다. 하나의 익숙한 이름이 셋으로 갈라진다는 사실이 처음에는 번거롭게 느껴진다. 하지만 그게 정확한 그림이다.

그래서 이 책의 첫 약속은 이것이다. **Cloudflare를 "또 하나의 클라우드"로 보지 말자.** 그러면 가격 비교만 하다가 본질을 놓친다. 대신 "AWS와 가정이 다른 edge-first 플랫폼"으로 보자. 그 자리에서 보면, 어떤 워크로드는 옮기는 게 합리적이고 어떤 워크로드는 옮기지 않는 게 합리적이라는 결정이 또렷해진다.

### Edge-first가 정확히 무엇을 뜻하는가

"edge-first"라는 단어는 Cloudflare 블로그·문서에 거의 모든 페이지에 나오는 표현이다. 그런데 정확히 뭘 의미하는 걸까? 한 번 짚고 가자.

AWS의 멘탈에서 "edge"는 부속물이다. 사용자에게 가까운 곳에 캐시 한 겹을 더 두는 것이 CloudFront다. 코드를 약간 돌리고 싶으면 CloudFront Functions나 Lambda@Edge를 얹는다. 본체는 여전히 리전 안에 있다. EC2도, RDS도, DynamoDB도, ALB도 모두 한 리전에 있고, edge는 그 앞에 깔린 얇은 레이어다. 사용자에게 빠르게 보이고 싶을 때 옵션으로 켜는 기능에 가깝다.

Cloudflare는 거꾸로다. **edge가 본체이고, origin이 옵션이다.** 우리가 작성한 Worker 코드는 처음부터 330개 넘는 PoP에 동시 배포된다. 도쿄 사용자가 부르면 도쿄에서, 프랑크푸르트 사용자가 부르면 프랑크푸르트에서 응답한다. 어느 PoP에 살까를 정하는 일이 없다. 모든 PoP에 산다. 그게 edge-first의 첫 번째 의미다.

두 번째 의미는 더 미묘하다. 같은 코드가 모든 곳에 있다면, 그 코드 안에서 "리전"이라는 단어는 더 이상 변수가 아니다. AWS에서는 거의 모든 SDK 클라이언트 생성자에 region 파라미터가 들어간다. Workers에서 KV·R2·D1·DO를 호출할 때는 그런 게 없다. 우리는 그저 `env.MY_KV.get(...)`이라고 쓴다. 어디 있는 데이터인지는 런타임이 라우팅한다. 리전이 사라진 자리에 PoP·Bindings·Compatibility Date가 들어선다. 이 세 단어가 Cloudflare의 새로운 좌표계다.

세 번째, 그리고 가장 강력한 의미는 가격 모델이다. Lambda는 메모리·실행 시간(GB-s) × 요청 수로 과금한다. 외부 API를 호출하고 응답을 기다리는 동안에도 메모리는 lock되고 비용은 흐른다. Workers Standard는 다르다. **CPU time × 요청 수**로 과금한다. 외부 API·DB 응답을 기다리는 시간은 과금되지 않는다. AI 호출처럼 LLM 응답을 5초씩 기다리는 워크로드라면, 같은 양의 일에 비용 차이가 한 자릿수가 아니라 두 자릿수까지 벌어진다. 이건 단순한 가격표 차이가 아니라 "어떤 워크로드가 자연스럽게 흘러가는가"가 다르다는 뜻이다. 워크플로 오케스트레이션, AI 게이트웨이, 외부 API 프록시 같은 I/O 대기 위주 워크로드는 Workers 가격 모델 위에서 살이 붙는다.

자, 이쯤에서 한 번 멈춰보자. 여기까지 읽고 "그래서 AWS 버리라는 거야?"라는 의문이 들었다면, 그건 자연스러운 반응이다. 하지만 이 책의 답은 정반대다. **AWS를 버리지 말자.** 우리가 10년 가까이 쌓아 올린 시스템은 그 자리에서 충분히 잘 돌아간다. RDS의 강한 일관성, Step Functions의 풍부한 통합, ECS의 거대한 컨테이너 워크로드 — 이런 자리는 그대로 두는 편이 낫다. Cloudflare는 그 옆에 자기 자리를 가지고 들어와야 한다. 어디에 들어와야 하는가가 이 책 전체의 질문이다.

### 두 번의 outage가 가르쳐준 것

2025년 11월 18일, 그리고 같은 해 12월 5일. Cloudflare는 두 차례의 큰 글로벌 장애를 겪었다. 11월 18일의 사건은 특히 인상적이었는데, Bot Management 설정 파일이 ClickHouse 권한 변경 때문에 두 배 크기가 되어 proxy가 panic을 일으켰다. Workers KV, Turnstile, Dashboard까지 줄줄이 영향을 받았고 11:20부터 17:06 UTC까지 부분 또는 전체 장애가 이어졌다. Hacker News에서는 한동안 토론이 끊이지 않았다.

이 사건들을 어떻게 받아들여야 할까. 한쪽에서는 "단일 벤더에 너무 많은 트래픽이 집중되어 있다"고 경고한다. 다른 쪽에서는 "AWS도 us-east-1 장애가 나면 인터넷 절반이 멈춘다"고 반박한다. 둘 다 일리 있다. 어느 한쪽 말이 정답은 아니다.

이 책이 제안하는 자세는 조금 다르다. **"Cloudflare를 쓸까 말까"가 아니라 "어디까지 의존할까"의 질문으로 옮기자.** 단일 벤더에 모든 critical path를 거는 일은 어떤 벤더라도 위험하다. 그게 Cloudflare든, AWS든, GCP든. 그래서 우리가 던져야 할 질문은 다음과 같다.

DNS는 Cloudflare로 가더라도 secondary DNS를 다른 곳에 두면 어떨까. 핵심 데이터는 R2에 두더라도 AWS S3에 백업 sink를 하나 더 운영하면 어떨까. 결제 같은 critical path는 Workers와 Lambda 두 군데에 동시에 두고 dual-running하면 어떨까. Rebal AI라는 회사가 정확히 이 패턴을 운영하고 있다. 비용이 두 배 들지만 한쪽이 죽어도 서비스가 멈추지 않는다.

여기서 우리는 정직해야 한다. Cloudflare 블로그를 읽으면 자주 "single vendor lock-in은 없다"는 말이 나온다. Workers 코드 자체는 Web standards 기반이라 이론적으로는 portable하다. 하지만 Bindings, Durable Objects, D1, KV의 API는 Cloudflare 고유다. 옮기려면 추상화 레이어를 한 겹 두거나 코드를 다시 짜야 한다. **feature-level lock-in은 명백히 존재한다.** 이걸 인정하지 않고 "Cloudflare는 lock-in이 없습니다"라고 말하는 책이 있다면, 그건 광고지 책이 아니다.

이 책은 광고가 아니다. 13장에서 outage 케이스를 더 깊이 다루고, 부록 F에 두 번의 사건의 상세 타임라인을 정리해두었다. 도입을 권유하면서 위험을 숨기지 않는다는 약속을 지키기 위해서다.

### 세 가지 명시적 약속, 그리고 그 한계

마케팅 카피를 걷어내고 보면, Cloudflare가 AWS 개발자에게 명시적으로 약속하는 것이 셋 있다. 이 셋을 머릿속에 박아두는 것만으로도 결정의 90%가 또렷해진다. 함께 살펴보자.

**첫째, egress가 무료다.** R2의 객체 다운로드, Workers의 응답 트래픽, 모두 outbound 비용을 받지 않는다. S3 Standard에서 30TB를 한 달 동안 다운로드하면 약 $2,700이 나온다. 같은 양을 R2에서 받으면 storage 비용 외에는 0이다. 미디어, 백업, AI 모델 가중치, 로그 export처럼 outbound가 큰 워크로드일수록 절감 폭이 커진다. Baselime이라는 회사는 AWS에서 Cloudflare로 옮긴 뒤 일 $790짜리 비용이 $25로 떨어졌다고 공식 블로그에 썼다. 95% 절감이다.

여기서 정직해야 할 한계가 있다. egress가 무료지만 **Class A operations(쓰기·list)와 Class B operations(읽기)는 과금**된다. 요청 수가 매우 많은 워크로드(예: 작은 객체를 초당 수천 번 읽는 패턴)에서는 결국 비용이 누적된다. 그리고 AWS에서 R2로 한 번 큰 데이터를 옮길 때, 그 inbound는 AWS의 egress로 잡힌다. 마이그레이션 첫 달 청구서가 깜짝 놀랄 만큼 클 수 있다. 옮길 가치가 있어도, 옮기는 그 한 번의 비용은 잊지 말자.

**둘째, 콜드스타트가 5ms 미만이다.** Lambda는 함수마다 컨테이너(Firecracker microVM)를 띄운다. JVM이 무거우면 첫 호출에 수 초가 걸리기도 한다. Java/Spring 위에서 Lambda를 돌려본 사람이라면 이 고통을 안다. SnapStart, Provisioned Concurrency, GraalVM Native — 콜드스타트를 줄이려는 온갖 우회 기법들이 그래서 생겼다. Workers는 V8 isolate 위에서 돌기 때문에 그런 우회가 필요 없다. isolate는 OS 프로세스가 아니라 한 V8 안의 격리된 실행 컨텍스트다. 새 isolate를 만드는 데 5ms가 채 걸리지 않는다.

이것의 대가는 분명하다. **임의 바이너리·full Node API·OS syscall이 안 된다.** FFmpeg를 직접 호출하고 싶다? 안 된다. Sharp 같은 native binding은 그대로 못 쓴다(Cloudflare Images로 우회). JVM 전체를 올리고 싶다? 당연히 안 된다. 멀티스레딩? 안 된다. `Date.now()`는 스크립트 실행 중에 고정값을 반환한다(Spectre 방어 정책의 일부). 이 제약을 받아들일 수 있는 워크로드와 그렇지 않은 워크로드의 경계선을 구분하는 게 결정의 출발점이다.

**셋째, DDoS 방어와 SSL이 기본 포함이다.** Cloudflare는 도메인을 한 번 옮기면 무료 플랜에서도 무제한 대역폭, DDoS 방어, SSL 인증서, WAF의 일부, Bot Management의 일부가 그냥 따라온다. 한국 개발자 커뮤니티에서 자주 회자되는 "DDoS 청구서 폭탄" 같은 걱정이 없다. AWS Shield Standard도 기본이긴 하지만, 트래픽이 폭주하는 동안 그 트래픽이 그대로 EC2·Lambda·CloudFront 비용으로 잡힌다. Cloudflare에서는 그 트래픽이 origin에 닿기 전에 흡수된다.

여기에도 한계는 있다. WAF의 enterprise rule, Bot Management의 모든 기능, API Shield 같은 것은 유료다. 작은 서비스라면 무료 플랜만으로 충분하지만, 큰 서비스가 되면 결국 Pro·Business·Enterprise 플랜의 가격을 봐야 한다. 그래도 같은 보호 수준을 AWS WAF + Shield Advanced + 자체 운영으로 짜는 비용보다는 저렴한 경우가 많다.

이 셋을 한 줄씩 머릿속에 두고 가자. egress 무료, 콜드스타트 5ms 미만, 보호 기본 포함. 결정의 첫 단추다.

### 이 책이 다루지 않는 것

기술서를 펼치면 다 다룬다고 약속하는 책일수록 막상 필요한 부분에서 입을 다문다. 그래서 이 책은 처음부터 **다루지 않는 것**을 분명히 밝히는 편이 낫다.

먼저, **GPU 추론**이다. Cloudflare Workers AI가 자체 GPU 인프라 위에서 LLM·임베딩·이미지 모델을 돌리지만, 카탈로그에 없는 모델을 직접 GPU에서 돌리는 영역은 이 책의 범위 밖이다. 그런 워크로드는 ECS/Fargate + EC2 GPU 또는 Bedrock에 남기는 편이 낫다. 이 책에서는 12장에서 Workers AI와 AI Gateway를 다룰 때 "어떤 워크로드를 Workers AI로, 어떤 워크로드를 Bedrock에 남길지"의 의사결정선만 그린다.

다음, **Spring Batch와 같은 거대 배치**다. JPA로 관계 그래프를 깊게 타고 트랜잭션 안에서 수만 row를 돌리는 워크로드는 Workers의 CPU time 한도와 isolate 모델에 자연스럽게 맞지 않는다. 이런 워크로드는 ECS에 남기는 게 맞다. 5장의 결정 프레임에서 "절대 옮기면 안 되는 워크로드"로 다시 등장한다.

**복잡한 PrivateLink·VPC peering 위주 아키텍처**도 이 책의 범위 밖이다. Cloudflare Tunnel + Cloudflare One으로 대체할 수 있는 시나리오는 11장에서 다루지만, 수십 개의 VPC가 PrivateLink로 얽혀 있는 enterprise 토폴로지는 단순히 이전 대상이 아니다. 그런 환경에서는 Cloudflare가 사용자 facing 경로(API, CDN, 인증)에만 들어오고, 사설망 자체는 AWS에 남는 하이브리드가 자연스럽다.

마지막으로 **Python Workers**다. 2024년부터 베타로 제공되고 있고 점점 안정화되고 있지만, 2026년 5월 시점의 production 권장 패스는 여전히 TypeScript/JavaScript다. 부록 D에 한 페이지짜리 안내를 두긴 했지만, 본문은 TS Workers 중심이다. Python으로 데이터 파이프라인을 운영하는 분들에게는 미안한 일이지만, 책 한 권의 깊이를 유지하기 위한 선택이다.

이 네 가지를 의도적으로 제외한 자리에 우리가 다루는 것은 분명하다. **AWS Spring/Node 백엔드를 운영하는 개발자가, 자기 시스템에 Cloudflare를 어디까지 어떻게 끼워 넣을지 결정하고 실행하는 데 필요한 모든 것.** 그게 이 책의 약속이다.

### 이 책을 펼친 우리는 누구인가

이 책의 첫 페이지를 펼친 사람은 대체로 다음 셋 중 하나다.

하나는 **해외 사용자 지연으로 고민하는 개발자**다. us-east-1에 핵심 시스템을 두고 운영하는데, 한국·일본·유럽 사용자가 늘어나면서 p95 응답시간 SLO를 못 맞추기 시작한다. CloudFront를 깔아도 동적 API의 첫 요청은 여전히 길다. 리전을 늘리면 데이터 동기화·운영 부담이 함께 늘어난다. 이런 자리에서 Cloudflare의 edge-first 모델이 가장 또렷한 답이 된다.

둘은 **egress 비용으로 고민하는 개발자**다. S3에서 미디어를 직접 서빙하거나, 백업을 다른 클라우드로 보내거나, AI 학습 데이터를 자주 다운로드하는 워크로드. 매달 청구서를 받아 보면 트래픽 비용이 슬금슬금 올라가는데 줄일 길이 없다. R2의 egress free가 정확히 이 자리에 들어온다. 옮기는 첫 달의 inbound 청구서를 감수할 의지만 있으면, 그 다음부터는 압도적이다.

셋은 **운영 부담을 줄이고 싶은 개발자**다. ALB, Auto Scaling Group, RDS Multi-AZ, ElastiCache, 이 모두를 운영하는 부담이 점점 무거워진다. 새 기능을 짜는 시간보다 운영을 챙기는 시간이 늘어나면 어딘가가 잘못된 신호다. Workers에 옮길 수 있는 부분은 옮기고, 옮길 수 없는 부분은 RDS를 그대로 두되 Hyperdrive로 edge에서 살리는 하이브리드 패턴을 그릴 수 있다. 운영 면적이 줄어든다.

이 셋 중 하나라도 우리 이야기처럼 들렸다면, 이 책은 우리에게 쓰여졌다. 단, 한 가지 전제가 있다. **AWS와 Spring/Node 백엔드 경력**이다. 이 책은 클라우드 입문서가 아니다. Lambda를 짜본 적 있고, DynamoDB와 RDS의 차이를 안다는 정도의 바닥은 깔려 있다고 본다. JS/TS는 기초만 있어도 따라올 수 있도록 단계별 설명을 두었지만, 백엔드 경험 자체는 전제다.

반대로 이 책이 우리를 위한 책이 아닌 경우도 있다. Cloudflare를 처음 듣는 사람, 서버리스가 처음인 사람, 자바스크립트 자체가 낯선 사람은 이 책 전에 더 가벼운 입문서를 거치는 편이 낫다. AWS를 거의 안 써본 사람도 마찬가지다. 이 책의 모든 챕터는 "AWS의 그것"과 "Cloudflare의 그것"을 비교하면서 진행되기 때문이다. 비교 대상이 비어 있으면 챕터의 절반이 허공에서 들린다.

### 책의 나침반 — 14장의 지도

이 책은 한 직선이 아니라 활처럼 휘는 곡선을 그린다. 호기심에서 시작해, 멘탈 모델의 혼란을 한 번 거치고, 첫 성공의 안도감을 잡고, 지도를 펼쳐 보고, 결정의 도구를 손에 쥔 다음, 본격적으로 데이터·프론트·보안·AI·운영의 깊이로 들어간다. 마지막에는 "내 시스템을 어떻게 옮길 것인가"의 답을 자기 손으로 그릴 수 있게 된다.

지금 1장에서 우리는 호기심의 자리에 있다. "또 하나의 클라우드가 아니라면 무엇인가?" 다음 장은 그 답의 핵심으로 들어간다. **V8 isolate가 무엇이고, 리전이 사라진 자리에 무엇이 들어서며, Bindings와 Compatibility Date가 왜 새로운 좌표계인가.** Lambda 컨테이너 모델로 Workers를 이해하려는 시도가 깨지는 자리다. 의도된 혼란이 한 번 지나간다.

3장에서는 손끝의 성취가 머리의 혼란을 진정시킨다. Mac에서 Wrangler를 깔고, 5분 안에 Hello World를 글로벌 PoP에 배포해본다. 도쿄·LA·런던에서 같은 응답이 즉시 떨어지는 광경을 직접 본 뒤에는 멘탈 모델이 달라진다.

4장은 지도다. AWS의 익숙한 이름들 — Lambda, S3, DynamoDB, CloudFront, Step Functions, Bedrock — 이 Cloudflare의 어느 자리에 어떻게 자리 잡는지 카탈로그를 펼친다. 동시에 1:1 매핑이 깨지는 다섯 가지 패턴을 분명히 표시해 둔다. 5장에서는 그 매핑 위에서 "그래서 내 워크로드 중 무엇을 옮길 것인가"의 결정 프레임을 손에 쥔다.

6장부터 12장은 본격적인 실무 영역이다. Hono로 라우팅·미들웨어·DI를 다시 그리고(6장), KV·D1·DO·R2를 워크로드 패턴별로 골라 쓰고(7·8장), Next.js를 OpenNext로 옮기고(9장), Hyperdrive로 RDS를 그대로 살리고(10장), Cloudflare Access·Tunnel로 보안을 다시 짜고(11장), Workflows·Queues·Cron·AI Gateway·Workers AI로 비동기·AI 영역을 채운다(12장). 각 챕터는 누적 실습 프로젝트 `toby-shop` 위에서 한 겹씩 쌓인다. 깃 브랜치로 체크포인트가 남기 때문에 어디서든 다시 뛰어들 수 있다.

13장은 정직한 위험이다. 비용 모델의 함정, observability 공백, 2025년 outage의 교훈, vendor lock-in. 이 책이 광고가 아님을 가장 분명히 드러내는 챕터다. 14장은 결단이다. 5장에서 "무엇을 옮길 것인가"를 결정했다면, 14장은 "어떻게 옮길 것인가"의 8단계 시퀀스다. Strangler Fig 패턴으로, 아무것도 부수지 않고 점진적으로 옮기는 길.

마지막 페이지를 덮을 때쯤이면 우리는 한 가지 답을 손에 쥐고 있을 것이다. **내 시스템에 Cloudflare가 어디까지 들어와도 좋은가.** 그 답을 자기 손으로 쓰기 위한 도구 일습이 이 책이다.

### 누적 실습 프로젝트 — `toby-shop` 한 줄 소개

기술서가 추상적인 개념만 늘어놓으면 책장을 덮을 때쯤 머릿속에 남는 게 별로 없다. 그래서 이 책은 한 도메인의 작은 e-commerce SaaS — `toby-shop` — 을 누적 실습 프로젝트로 두었다. 3장에서 빈 Worker로 시작해 6장에서 Hono 라우팅·인증·KV 세션이 붙고, 7장에서 D1 + Drizzle로 사용자 프로필이 생기고, 8장에서 고객지원 채팅방(Durable Objects + WebSocket)이 분기되고, 9장에서 Next.js 상점 프론트가 추가되고, 10장에서 RDS + Hyperdrive로 주문 도메인이 살아나고, 11장에서 소셜 로그인과 어드민 보안이 더해지고, 12장에서 결제 후 영수증 Workflow와 RAG 챗봇이 얹힌다. 13장에서 Logpush + 외부 APM이 운영 레이어로 깔린다.

각 챕터 끝에는 깃 브랜치(`ch3-hello`, `ch6-data` 같은) 체크포인트가 있다. 처음부터 따라올 수도 있고, 7장이나 9장 같은 특정 챕터부터 뛰어들 수도 있다. 누적되는 곳은 누적되고, 분기되는 곳은 분기된다. 분기된 워크북(1·2·4·5·14장의 결정 워크시트)은 자기 시스템에 그대로 적용해볼 수 있는 형태로 만들어두었다.

### 무너지는 자리 — 1장이 약속하지 못하는 것

이 책의 모든 기술 챕터 끝에는 "무너지는 자리" 박스를 둔다. 1장에도 둔다. 광고로 보이지 않게 하는 가장 단순한 약속이다.

이 1장의 한계는 분명하다. 첫째, **Cloudflare는 빠르게 변한다.** 2026년 5월 시점의 사실들이 책이 출간된 뒤 6개월 안에 일부 바뀔 수 있다. Workers Containers의 인스턴스 한도, OpenNext 어댑터의 호환성, Vinext의 안정화 정도, Vectorize의 hybrid search 지원 — 이런 영역은 분기마다 공식 페이지를 다시 봐야 한다. 부록 E에 추적 가이드를 두었으니 참고하자.

둘째, **이 책은 enterprise PrivateLink·HIPAA·KISA 강한 region lock 같은 영역을 다루지 않는다.** 그런 환경에서 Cloudflare가 들어올 자리는 매우 좁아진다. 사용자 facing 경로 일부와 DDoS 보호 정도가 현실적인 한계일 수 있다. 그 영역의 더 깊은 답은 이 책이 줄 수 있는 것 너머에 있다.

셋째, **2025년 outage는 다시 일어날 수 있다.** Cloudflare의 엔지니어링 신뢰도와 별개로, 단일 벤더에 critical path를 거는 일은 본질적으로 위험을 동반한다. 13장에서 회피 전략을 다루지만, 그 회피 전략을 모두 갖추는 데도 비용과 운영 부담이 따른다. 한 줄로 정리하면, "Cloudflare를 도입한다"가 아니라 "Cloudflare에 자기 시스템의 일부 자리를 내준다"는 자세가 정직하다.

### 마무리

다음 장에서는 Lambda 컨테이너 모델로 Workers를 이해하려는 시도가 깨지는 자리를 살펴보자. V8 isolate가 정확히 무엇이고, 콜드스타트 5ms 미만의 대가로 무엇을 포기하는지, 리전이 사라진 자리에 PoP·Bindings·Compatibility Date가 어떻게 들어서는지. 우리가 익혀온 가정 중 일부를 한 번 흔들어볼 차례다. 잠시 불편하겠지만, 그 흔들림이 지나가야 3장의 첫 배포가 손에 잡힌다.

기억해두자. **Cloudflare는 또 하나의 클라우드가 아니다. 가정이 다른 edge-first 플랫폼이다.** 이 한 줄이 책 전체를 통과하는 나침반이다.

---


## 2장. 멘탈 모델을 다시 그리자 — V8 Isolate가 바꾸는 가정

Lambda 함수를 Java로 짠 적이 있는 우리는 어느 월요일 아침의 풍경을 잘 안다. 사용자가 처음 호출한 함수가 응답까지 3초 가까이 걸린다. CloudWatch 로그를 열어 보면 `INIT_DURATION: 2400 ms`라는 줄이 박혀 있다. JVM이 깨어나서 클래스를 로드하고 Spring 컨텍스트를 짜는 데만 2초가 넘게 갔다는 뜻이다. 두 번째 호출부터는 200ms로 떨어진다. 이른바 콜드스타트다. SnapStart를 켜고, Provisioned Concurrency를 사두고, GraalVM Native Image까지 만져본 사람이라면 이 풍경이 더 친숙할 것이다. 콜드스타트와의 싸움은 지난 10년간 서버리스 개발자의 숙제였다.

자, 그런데 누군가 우리에게 와서 이렇게 말한다고 해보자. "Workers는 콜드스타트가 5ms 미만이다." 처음 들으면 마케팅 카피처럼 들린다. JVM 워밍업도 없고, 컨테이너 부팅도 없고, 그냥 5ms? 어떻게 그게 가능할까? 그리고 더 중요한 질문, **그 대가로 우리는 무엇을 포기해야 할까?** 공짜로 받는 성능은 거의 없다. 우리가 익혀온 가정 중 어떤 것을 흔들어야 그 5ms가 손에 들어오는지, 함께 들여다보자.

이 장은 의도된 혼란의 자리다. 1장에서 "또 하나의 클라우드가 아니다"라는 말을 들었다면, 2장은 그 말이 정확히 무엇을 뜻하는지 멘탈 모델 단위로 풀어내는 곳이다. V8 isolate, 사라진 리전, Bindings, Compatibility Date 그리고 "I/O 대기는 과금되지 않는다"는 가격 모델 — 이 다섯 기둥을 세우고 나면 3장의 첫 배포가 손에 잡힌다.

### V8 Isolate — 같은 "서버리스"라는 단어 아래의 다른 행성

먼저 Lambda가 어떻게 도는지 한 줄로 다시 정리해보자. AWS는 함수마다 Firecracker라는 microVM을 띄운다. microVM은 KVM 위에 올린 가벼운 가상머신인데, 가볍다고 해도 OS 커널·파일시스템·네트워크 스택 같은 것들이 들어 있다. 그 위에서 Node나 JVM 같은 런타임이 켜지고, 그 안에 우리 함수 코드가 로드된다. 그러니까 한 요청을 처리하기 위해 우리는 사실상 작은 운영체제 한 대를 부팅하고 있는 셈이다. Firecracker가 부팅 자체는 100ms 안에 끝낸다고는 해도, 그 위에 올라가는 JVM이 켜지고 Spring 컨텍스트가 만들어지는 데 또 2초가 더 걸린다. 콜드스타트의 비용은 거기서 나온다.

Workers는 이 모델을 통째로 갈아엎는다. 핵심은 **V8 isolate**라는 개념이다. V8은 우리가 잘 아는 그 V8 — Chrome 브라우저 안에서 자바스크립트를 돌리는 엔진이다. 한 V8 프로세스 안에는 여러 개의 isolate를 동시에 띄울 수 있다. isolate 하나하나는 자기만의 힙과 GC를 가지지만, OS 프로세스를 새로 띄우는 게 아니라 같은 프로세스 안에 격리된 실행 컨텍스트로 존재한다. 브라우저로 비유하면, 같은 Chrome 안에서 여러 탭이 각자 격리되어 도는 것과 비슷하다. 새 탭을 여는 데 새 OS를 부팅할 필요가 없는 것과 같은 이치다.

그래서 새 isolate를 만드는 비용이 microVM 부팅에 비해 비교가 안 되게 싸다. 5ms 미만이라는 숫자가 거기서 나온다. 더 인상적인 점이 있는데, **isolate는 첫 요청이 들어오기 전까지 만들어지지도 않는다.** 사용자가 도쿄에서 우리 Worker를 처음 호출하면, 그 순간 도쿄 PoP에 isolate가 만들어진다. 같은 PoP에 두 번째 요청이 들어오면 같은 isolate가 재사용된다. 트래픽이 없으면 isolate는 자연스럽게 사라진다. Lambda의 컨테이너 풀처럼 따로 워밍업을 신경 쓸 필요가 없다.

여기서 자연스럽게 던져야 할 질문이 있다. **그렇다면 그 대가는 무엇인가?** 공짜는 없다고 했다. 가장 큰 대가는 *임의 바이너리·full Node API·OS syscall이 안 된다*는 점이다. V8은 자바스크립트(와 WebAssembly) 엔진이지 OS가 아니다. 그래서 FFmpeg를 직접 호출하고 싶다면 막힌다. Sharp 같은 native binding은 그대로 쓸 수 없다. 멀티스레딩? 안 된다. JVM을 통째로 올리고 싶다? 당연히 안 된다. 우리가 Spring 위에서 당연하게 누리던 라이브러리 생태계의 절반은 이 자리에서 닫힌다. 처음에는 끔찍한 일처럼 느껴진다. 평생 써온 도구함의 절반을 놓고 가야 하니까.

그런데 한 발짝 떨어져 보면 그림이 다르다. Workers의 자리는 **API 게이트웨이·인증·라우팅·캐시·외부 API 프록시·간단한 데이터 변환** 같은 워크로드다. 이런 곳에서는 FFmpeg도 JVM도 필요 없다. 필요한 것은 짧은 응답시간과 글로벌 분산이고, 그건 V8 isolate 모델이 가장 잘 해주는 일이다. 무거운 워크로드 — 미디어 변환, 거대 배치, GPU 추론 — 는 ECS나 Bedrock에 그대로 두면 된다. 도구함의 절반을 놓고 가는 게 아니라, 같은 도구함을 워크로드별로 두 군데에 나눠 두는 셈이다. 5장에서 이 결정의 프레임을 본격적으로 다룬다. 지금은 "isolate에 맞는 일과 맞지 않는 일이 있다"는 감각만 가져가자.

#### Spectre 방어와 멈춘 시계

V8 isolate에는 또 한 가지 미묘한 제약이 있다. 같은 isolate 안에 우리 코드가 다른 사람의 코드와 함께 사는 모델이라서, 이론적으로 Spectre 같은 side channel 공격이 가능해진다. 캐시·브랜치 예측 같은 CPU 마이크로아키텍처를 통해 같은 프로세스 안의 다른 메모리를 추론해내는 공격이다. Cloudflare는 여기에 대해 여러 겹의 방어를 깔아두었다.

가장 눈에 띄는 방어가 **시간 측정 차단**이다. 보통 자바스크립트에서 `Date.now()`나 `performance.now()`를 부르면 마이크로초 단위까지 시간이 흐른다. Spectre 공격은 그 미세한 시간 차이를 측정해 캐시 hit/miss를 추론한다. 그래서 Workers 안에서는 **`Date.now()`가 스크립트 실행 중에 사실상 고정된 값을 반환한다.** 정확히 말하면 마지막 I/O가 일어난 시점의 시간을 반환한다. 처음 이 사실을 알게 되면 찜찜하다. "벤치마크는 어떻게 돌리지?", "지연 시간은 어떻게 측정하지?" 하는 질문이 자연스럽게 따라붙는다.

답은 단순하다. *벤치마크는 Worker 안이 아니라 바깥에서 측정한다.* Cloudflare 대시보드의 Workers Analytics, `wrangler tail`로 들어오는 로그, 외부 APM(Sentry, Baselime, Datadog)으로 보낸 trace 이벤트가 실제 측정 지점이다. Worker 코드 안에서 ms 단위의 지연을 재서 의사결정에 쓰던 패턴이 있다면 다시 짜는 편이 낫다. 다행히 그런 패턴은 흔하지 않다.

또 하나의 방어는 **멀티스레딩 차단**이다. SharedArrayBuffer를 써서 정밀한 타이머를 만드는 우회로가 막혀 있다. 한 isolate 안에서 우리 코드는 사실상 단일 스레드로 돈다. CPU bound 작업을 병렬로 돌리고 싶다면 Workflows로 나누거나, 여러 Worker로 나누는 게 자연스러운 길이다.

그리고 한 가지 더, V8 보안 패치를 Cloudflare는 Chrome stable보다 먼저 production에 푼다. 새 CVE가 떴을 때 Chrome 사용자보다 Workers 사용자가 더 빨리 보호받는다는 뜻이다. 빠른 보안 대응이라는 점에서는 분명한 장점이다. 다만 양면이 있다. Chrome stable에서 검증되기 전의 패치가 production에 들어간다는 점은 일부 엔지니어 사이에서 양가적으로 평가된다. 빠른 패치인가, 검증 안 된 패치인가. 정답은 없고, *Cloudflare는 빠른 보안 쪽을 택했다*는 사실만 알아두면 된다.

> **무너지는 자리 — V8 Isolate가 안 맞는 자리**
> JVM 전체를 올리고 싶을 때, 임의 바이너리(FFmpeg, ImageMagick CLI)를 직접 호출해야 할 때, OS syscall에 의존하는 라이브러리(예: 로컬 파일 캐시·shared memory·POSIX 시그널)를 그대로 옮기려 할 때, 멀티스레딩으로 CPU를 갈아 넣어야 할 때 — 이런 워크로드는 isolate 모델에 맞지 않는다. 옮기지 말자. ECS·Fargate·Bedrock에 남기는 편이 정직하다.

### 사라진 리전, 들어선 좌표계

다음 가정을 흔들 차례다. AWS에서 새 프로젝트를 시작할 때 우리가 거의 무의식적으로 가장 먼저 하는 일이 있다. **리전을 고른다.** us-east-1로 갈지, ap-northeast-2로 갈지, 아니면 둘 다 쓸지. 그 결정 위에 VPC를 그리고, 서브넷을 자르고, Security Group을 짠다. 데이터도 그 리전에 산다. RDS는 그 리전의 인스턴스고, DynamoDB는 그 리전의 테이블이고, S3 버킷은 그 리전의 storage class다. 글로벌하게 만들고 싶다면 CloudFront를 앞에 깔거나 DynamoDB Global Table을 켜거나 S3 Cross-Region Replication을 건다. 어쨌든 출발점은 "어떤 리전에 살 것인가"의 결정이다.

Workers에는 이 결정 자체가 없다. 우리가 `wrangler deploy`를 한 번 누르면 코드는 330개 넘는 PoP에 동시에 배포된다. 도쿄 사용자가 부르면 도쿄에서, 프랑크푸르트 사용자가 부르면 프랑크푸르트에서 응답이 떨어진다. Worker 코드 안에서 `region` 같은 변수는 등장하지 않는다. AWS SDK 클라이언트를 만들 때 거의 모든 생성자에 들어가던 `region` 파라미터가, KV·R2·D1·DO 호출에서는 사라져 있다. 우리는 그저 `env.MY_KV.get(...)`이라고 쓴다. 데이터가 어디 있는지는 런타임이 라우팅한다.

처음에는 이게 편안하지 않다. 10년 동안 "리전을 정하고 시작하라"고 배운 사람한테 "리전이 없습니다"는 메시지는 어딘가 불안하다. *그럼 데이터 주권은 어떻게 챙기지? GDPR 같은 규제는?* 자연스러운 의문이다. 답은, 리전이 사라진 자리에 다른 좌표계가 들어섰다는 것이다. 셋만 기억해두자.

**첫째, PoP다.** PoP(Point of Presence)는 Cloudflare가 전 세계에 깔아둔 데이터센터 한 곳을 가리킨다. 코드 입장에서 PoP는 신경 쓰는 단위가 아니다. 어느 PoP에 도는지는 사용자에게 가장 가까운 곳을 런타임이 알아서 정한다. 그저 "내 코드는 모든 PoP에 산다"고 알아두면 된다.

**둘째, Jurisdiction이다.** GDPR을 비롯한 데이터 주권 규제 때문에, "이 데이터는 EU 안에서만 처리되어야 한다" 같은 요구가 있을 수 있다. Cloudflare에서는 D1·DO 같은 stateful 자원을 만들 때 `jurisdiction: "eu"` 같은 옵션으로 그 자원이 사는 영역을 EU 또는 UK로 묶을 수 있다. 한국·일본 같은 단일국 jurisdiction은 아직 별도로 제공되지는 않지만, jurisdiction이라는 추상이 리전의 자리를 일부 대체한다고 보면 된다.

**셋째, location hint다.** D1과 Durable Objects를 만들 때 "이 데이터의 첫 위치를 어디로 잡을지" 힌트를 줄 수 있다. 예를 들어 한국 사용자 위주의 워크로드라면 D1을 `apac` 힌트로 만들고, DO 인스턴스를 만들 때 `locationHint: "apac"`을 준다. 어디까지나 힌트라서 Cloudflare가 적절히 조정하지만, "사용자가 가장 많은 곳에 데이터를 가까이 두고 싶다"는 의지를 표현하는 도구다.

리전이 사라진 자리에 PoP·Jurisdiction·location hint가 들어섰다. 같은 좌표계가 아니라 *다른* 좌표계다. 1:1로 옮길 수 있는 것이 아니라 멘탈 자체를 새로 짜야 한다. 처음에는 번거롭게 느껴지지만, 한 번 익숙해지면 "리전마다 인프라를 복제한다"는 부담이 사라진 자리가 꽤 가볍다.

### Bindings — IAM Role과 SDK Client를 한 추상으로

이제 좀 다른 질문으로 옮겨가보자. AWS에서 Lambda가 S3 버킷을 읽으려면 무엇이 필요한가? 적어도 두 가지가 필요하다. **하나는 IAM role**이다. 그 Lambda 실행 역할에 `s3:GetObject` 권한이 붙어 있어야 한다. **다른 하나는 SDK client**다. 함수 코드 안에서 `new S3Client({ region: "..." })`처럼 클라이언트를 만들고 거기에 자격 증명이 흘러들어가야 한다. 이 둘이 따로 노는 점은 AWS를 오래 써본 사람이라면 익숙하다. IAM 정책은 콘솔이나 IaC에서 짜고, 클라이언트는 코드에서 만들고, 둘이 맞물려야 한다.

Cloudflare는 이 둘을 **Bindings**라는 한 추상으로 묶는다. `wrangler.jsonc`에 이렇게 적는다고 해보자.

```jsonc
{
  "name": "toby-shop-api",
  "main": "src/index.ts",
  "compatibility_date": "2026-05-01",
  "kv_namespaces": [
    { "binding": "SESSIONS", "id": "abc123..." }
  ],
  "r2_buckets": [
    { "binding": "ATTACHMENTS", "bucket_name": "toby-shop-files" }
  ],
  "d1_databases": [
    { "binding": "DB", "database_name": "toby-shop", "database_id": "..." }
  ]
}
```

이 한 덩어리가 의미하는 바를 풀어보자. `SESSIONS`라는 이름의 KV namespace가 있고, `ATTACHMENTS`라는 이름의 R2 bucket이 있고, `DB`라는 이름의 D1 database가 있다. 그런데 *어디에 권한 정책이 있나?* 없다. 아니, 정확히 말하면 **이 선언 자체가 권한 정책**이다. wrangler.jsonc에 binding을 적는다는 행위는 "이 Worker가 이 자원에 접근할 수 있다"고 선언하는 것과 같다. IAM의 별도 정책 문서가 없다.

코드에서는 이 binding이 그대로 함수 인자로 흘러들어온다.

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    // env.SESSIONS는 KV namespace 핸들
    const sessionId = getCookie(request, "sid");
    const user = await env.SESSIONS.get(sessionId, "json");

    // env.DB는 D1 database 핸들
    const profile = await env.DB
      .prepare("SELECT * FROM profiles WHERE user_id = ?")
      .bind(user.id)
      .first();

    return Response.json(profile);
  }
};
```

`env.SESSIONS`도, `env.DB`도 클라이언트를 직접 만들지 않았다. 자격 증명을 코드에 박지도 않았다. 그저 binding 이름을 통해 핸들이 함수 인자로 들어와 있다. **이게 IAM role과 SDK client 두 역할이 한 추상으로 합쳐졌다는 뜻이다.**

Spring 개발자라면 이 모양이 어딘가 익숙할 것이다. `@Autowired`로 의존성을 주입받는 그 모양이다. Spring에서 `UserRepository`를 컨트롤러 안에 주입할 때, 우리는 그 객체를 `new`로 만들지도 않고 데이터베이스 자격 증명을 코드에 넣지도 않는다. 컨테이너가 만들어서 넣어준다. Workers의 Bindings는 비슷한 사고방식의 더 가벼운 버전이다. *런타임이 의존성을 주입해주는 모델*이라고 보면 멘탈 매핑이 자연스럽다.

```java
// Spring — 의존성 주입
@RestController
class UserController {
    private final UserRepository repo;
    UserController(UserRepository repo) { this.repo = repo; }
    // ...
}
```

```typescript
// Workers — Bindings
async function fetch(req: Request, env: Env) {
  // env.DB가 사실상 주입된 의존성이다
  const repo = createUserRepo(env.DB);
  // ...
}
```

차이는 있다. Spring은 컴파일 타임에 의존 그래프를 짜고, Workers는 런타임에 환경 객체로 받는다. Spring은 임의 클래스를 빈으로 등록할 수 있고, Workers는 Cloudflare가 정의한 자원만 binding으로 잡을 수 있다. 그래도 "사용 측은 만들지 않고 받는다"는 본질이 같다는 점이 핵심이다. 처음에 Workers를 보고 "DI가 없네, 어떻게 테스트하지?" 하고 난감해하는 분이 있다면, 이 매핑을 떠올려보자.

테스트는 어떻게 하나? 좋은 질문이다. Spring에서는 모킹된 빈을 컨테이너에 넣었다. Workers에서는 `getBindingsProxy()`라는 헬퍼나 `@cloudflare/vitest-pool-workers`라는 도구로 같은 일을 한다. 테스트 코드에서 가짜 KV·D1·R2 핸들을 만들고, fetch 함수에 env 객체로 넣어 호출하는 식이다. 본격적인 코드 예시는 6장에서 다룬다. 지금은 "Bindings는 DI고, 모킹할 수 있다"는 사실만 알아두자.

Bindings의 또 한 가지 좋은 점은 **타입 안전성**이다. `wrangler types` 명령을 한 번 돌리면 `Env` 인터페이스가 자동 생성된다. wrangler.jsonc에 `SESSIONS`라는 KV가 있다면 `Env.SESSIONS: KVNamespace` 타입이 만들어진다. 오타를 내거나 없는 binding을 쓰면 컴파일 단계에서 잡힌다. AWS SDK의 string 기반 ARN이나 환경변수 폭주에 비하면 훨씬 깔끔하다. 익숙해지면 돌아가기 어렵다.

> **무너지는 자리 — Bindings의 한계**
> Bindings는 깔끔하지만 IAM의 정교한 정책 언어 — 조건부 접근, resource-level 권한, 시간대별 정책, MFA 강제 같은 — 와는 표현력이 다르다. "이 Worker는 이 KV의 read만 가능하고 write는 불가" 같은 fine-grained 정책을 binding 자체에 표현할 직접적 방법이 없다. 그런 정책이 필요하면 Worker를 둘로 나누거나, 코드 레벨에서 권한 체크를 직접 하거나, Cloudflare Access와 WAF 규칙을 조합하는 우회로를 잡아야 한다. 11장에서 더 자세히 다룬다.

### Compatibility Date — 시간이 박혀 있는 런타임

다음 기둥이다. AWS에서 Lambda 함수를 만들 때 우리는 런타임을 고른다. `nodejs20.x`, `java17`, `python3.12`. 시간이 지나면 AWS가 새 런타임을 내고, 옛 런타임의 EOL 날짜를 공지한다. Lambda 콘솔이나 IaC에서 우리가 직접 새 런타임으로 마이그레이션해줘야 한다. 안 그러면 어느 날 콘솔에 빨간 경고가 뜨고, 결국 강제로 마이그레이션 당한다.

Workers는 좀 다르다. 가장 헷갈리는 단어 중 하나가 `compatibility_date`다. wrangler.jsonc 위에 보면 `"compatibility_date": "2026-05-01"` 같은 줄이 들어 있다. 처음 보면 "이건 언제 만들어진 Worker라는 표시인가?" 싶다. 절반은 맞고 절반은 아니다.

정확하게 말하면, **이 날짜는 우리 Worker가 어느 시점의 런타임 동작을 따라갈지 못 박는 표시다.** Cloudflare는 workerd라는 런타임을 매주처럼 업데이트한다. 새 표준 API가 추가되고, 옛 API의 동작이 다듬어지고, 가끔은 미묘한 동작 변경도 있다. 만약 모든 Worker가 항상 최신 런타임 동작을 따라간다면, 우리가 6개월 전에 짠 Worker가 어느 날 갑자기 다른 동작을 보일 수 있다. 끔찍한 일이다.

`compatibility_date`는 그래서 일종의 시간 잠금 장치다. `2026-05-01`로 박아두면, 그 시점 기준의 런타임 동작이 우리 Worker에 적용된다. 시간이 흘러 Cloudflare가 어떤 동작을 바꿔도 우리 Worker는 옛 동작을 그대로 받는다. *우리가 직접 날짜를 올리기 전까지는.* AWS Lambda의 강제 EOL과 비교하면 마음이 편안해지는 모델이다. 능동적으로 올리지 않으면 옛날 그대로다.

물론 영원히 안 올릴 수는 없다. 보안 패치는 날짜와 무관하게 적용되고, 너무 오래된 동작은 어느 시점에 sunset된다. 그래도 Lambda처럼 "3개월 안에 마이그레이션 안 하면 함수가 안 돕니다" 같은 강압은 없다. 우리가 분기에 한 번 정도 검토해서 올리는 패턴이 자연스럽다.

`compatibility_flags`라는 짝궁 옵션도 있다. 특정 동작 하나만 켜고 끄고 싶을 때 쓴다. 예를 들어 "Node.js 호환 레이어 켜기" 같은 플래그를 개별로 활성화할 수 있다. 굳이 compatibility_date를 통째로 올리지 않고도 새 동작 하나만 시험해볼 수 있는 길이다.

```jsonc
{
  "compatibility_date": "2026-05-01",
  "compatibility_flags": ["nodejs_compat"]
}
```

Spring 개발자라면 어떻게 비유할까. Spring Boot의 버전 선택과 비슷하지만 결이 다르다. Spring Boot는 보통 한 버전을 고르고, 마이너 버전을 올릴 때 마이그레이션 가이드를 본다. Workers는 *런타임은 항상 최신*인데, 우리 코드에 **"이 시점의 동작을 봐달라"** 는 라벨을 붙이는 모양이다. 라벨을 올리는 것도 우리고, 라벨을 안 올려서 옛 동작을 받는 것도 우리다. 통제권이 우리 쪽에 있다.

새 Worker를 만들 때 한 가지만 기억해두자. **`pnpm create cloudflare`로 프로젝트를 만들면 그 시점의 최신 날짜로 자동 채워진다.** 우리가 신경 쓸 일은 분기마다 한 번씩 "지금 날짜로 올려도 되나" 점검하는 정도다. 변경사항은 Cloudflare 공식 문서의 "Compatibility Dates" 페이지에 깔끔하게 정리돼 있다. 부록 E에 추적 가이드를 두었다.

### "I/O 대기는 과금되지 않는다" — 가격이 멘탈을 다시 그린다

지금까지가 런타임 모델이었다면, 이제 그 위에 얹힌 가격 모델을 보자. 이 한 줄이 우리의 멘탈 모델을 어디까지 흔드는지 살펴보면 흥미롭다.

먼저 Lambda의 모델이다. Lambda는 두 가지로 과금한다. 하나는 요청 수, 다른 하나는 **메모리 × 실행 시간**이다. 1024MB 메모리 함수가 3초 동안 돌면 3 GB-s가 과금된다. 외부 API를 호출하고 5초 동안 응답을 기다린다고 해도, 그 5초 동안 Lambda는 메모리를 잡고 있고 *과금 시계는 그대로 돌아간다.* 이걸 알게 된 뒤로 많은 사람이 "Lambda 안에서는 외부 API 응답을 오래 기다리지 마라"는 운영 수칙을 갖게 됐다. 길게 기다려야 하는 작업은 Step Functions로 빼서 비동기로 만들고, Step Functions는 또 state transition 단위로 과금된다.

Workers Standard는 다르다. **CPU time × 요청 수**로 과금한다. 외부 API를 호출하고 5초를 기다리는 동안, 그 5초는 *과금되지 않는다.* CPU가 돌고 있는 시간만 잡는다. 외부 API 응답이 도착해 다시 우리 코드가 실행되는 그 짧은 순간만 비용이다. 이 한 줄이 멘탈 모델 전체를 흔든다.

상상해보자. 우리가 LLM 응답을 5초 동안 기다리는 워크로드를 운영한다고 해보자. Lambda 위에서는 5초 × 메모리만큼 비용이 흐른다. Workers 위에서는 우리 코드가 실제로 도는 몇십 ms 동안만 비용이 잡힌다. 같은 양의 일에 비용 차이가 한 자릿수가 아니라 두 자릿수까지 벌어질 수 있다. AI 게이트웨이, 외부 API 프록시, 워크플로 오케스트레이션 — 이런 I/O 대기 위주 워크로드는 Workers의 가격 모델 위에서 자연스럽게 살이 붙는다.

그렇다면 어떤 워크로드가 어디에 자연스러운가? 한 줄로 정리하면 **"I/O가 많고 CPU가 적은 일은 Workers, CPU를 많이 쓰는 무거운 일은 Lambda나 ECS"** 다. 외부 API 통합, 라우팅, 인증 검증, 캐시 hit 응답, 가벼운 데이터 변환 — Workers의 영역이다. 무거운 데이터 처리, 이미지 변환, 큰 SQL 분석 쿼리 — 다른 곳에 두는 편이 낫다.

이 가격 모델이 가져오는 부수 효과가 또 있다. **Workflows라는 durable execution 엔진이 Step Functions와 본질적으로 다른 비용 모양을 갖는다.** Step Functions는 state transition 단위로 과금되기 때문에 long-poll이나 사용자 승인 같은 외부 대기가 비용에 그대로 잡힌다. Workflows는 코드가 `step.sleep(...)`이나 `step.waitForEvent(...)`로 며칠을 자더라도 그 동안 비용이 흐르지 않는다. 우리가 Spring `@Async`로 짜오던 비동기 패턴, Step Functions로 짜오던 multi-step 워크플로 — 이런 영역의 비용 곡선이 다시 그려진다. 자세한 코드는 12장에서 본격적으로 살펴보자.

여기서도 정직해야 한다. **무료가 아니라는 점이다.** I/O 대기 시간은 과금되지 않지만, 요청 수와 CPU time은 과금된다. 요청이 매우 많은 워크로드(초당 수만 건)에서는 결국 비용이 누적된다. 그리고 Workers Paid 플랜은 월 $5짜리 기본료가 있다. 작은 사이드 프로젝트에 Free 플랜으로 충분한 경우가 많지만, production은 Paid가 권장된다. 비용 시뮬레이션은 부록 C에 워크시트로 두었다.

### Spring 개발자의 다섯 가지 멘탈 — 어떻게 다시 그릴까

V8 isolate, 사라진 리전, Bindings, Compatibility Date, I/O 과금. 네 기둥에 가격 모델까지 얹었다. 이 새 좌표계 위에서 Spring 개발자가 익숙하게 누리던 다섯 가지 멘탈 — 요청-응답, 미들웨어, DI, 트랜잭션, `@Scheduled` — 가 어떻게 다시 그려질지 미리 그림만 그려두자. 본격적인 코드는 6장과 12장에서 쓴다.

**첫째, 요청-응답이다.** Spring에서는 `@RestController`와 `@GetMapping`이 우리의 진입점이었다. Workers는 더 단순하다. `fetch(request, env, ctx)` 함수 하나가 전부다. request 객체는 Web standards의 그 Request이고, response도 Web standards의 그 Response다. 가벼운 라우팅이 필요하면 Hono를 얹는다. Hono는 Express에 가까운 라우팅·미들웨어 모델을 가져오기 때문에, Express를 써본 사람한테는 즉각 친숙하고, Spring만 써온 사람한테도 30분이면 적응된다.

**둘째, 미들웨어다.** Spring의 `SecurityFilterChain`, `Interceptor`, `Filter` — 이 자리는 Hono의 `app.use()` 체인이 정확히 채운다. 인증·rate limit·캐시·로깅을 미들웨어 체인으로 엮는 모델이 같다. 다른 점은 Hono의 미들웨어가 함수 한 개로 표현되어 가벼운다는 점, 그리고 V8 isolate 위에서 도니까 시작 비용이 거의 없다는 점이다.

**셋째, DI다.** 앞 절에서 봤듯이 Bindings가 Spring의 `@Autowired` 자리에 들어선다. 차이는 컨테이너가 우리가 정의한 임의 클래스를 빈으로 등록해주지는 않는다는 점이다. 그래서 Repository 같은 도메인 객체는 함수형으로 짜거나 작은 클래스로 직접 만들어 인자로 넘기는 패턴이 많다. 처음에는 "Spring 컨테이너가 그립다"는 마음이 들 수 있는데, 막상 짜보면 의외로 가볍고 명료해진다.

**넷째, 트랜잭션이다.** 이 자리는 Spring 개발자가 가장 헷갈려하는 곳이다. `@Transactional`을 메소드에 붙이면 트랜잭션이 자동 propagation되던 마법은 Workers 안에 없다. D1은 statement 또는 batch 단위 트랜잭션을 지원하지만 분산 propagation이 없고, Durable Objects는 그 storage 안에서 강한 일관성을 보장한다. "트랜잭션 코디네이터가 필요하다"고 느끼면 보통 Durable Objects를 그 자리에 둔다. 사용자별 카운터, 재고, 예약 — 이런 워크로드가 그렇다. 자세한 멘탈 매핑은 7·8장에서 본격적으로 다룬다.

**다섯째, `@Scheduled`다.** Spring Batch, `@Scheduled`로 짜오던 정기 작업은 Workers에서 **Cron Triggers**가 맡는다. wrangler.jsonc에 cron 표현식 한 줄을 적으면, 그 시간마다 우리 Worker의 `scheduled` 핸들러가 호출된다. 무거운 배치는 ECS에 그대로 두고, 매시 정각의 health check나 매일 새벽의 보고서 발송 같은 가벼운 정기 작업이 자연스러운 자리다. 12장에서 본격적으로 짜본다.

다섯 가지 멘탈을 한 페이지 표로 정리하면 이렇게 된다.

| Spring 멘탈 | Workers의 자리 |
|---|---|
| `@RestController` + `@GetMapping` | `fetch(request, env, ctx)` + Hono 라우팅 |
| `SecurityFilterChain` / `Interceptor` | Hono `app.use()` 미들웨어 체인 |
| `@Autowired` / DI 컨테이너 | Bindings (env 객체) + 함수형 또는 작은 팩토리 |
| `@Transactional` 자동 propagation | D1 statement·batch 또는 Durable Objects (per-entity) |
| `@Scheduled` / Spring Batch (가벼운 부분) | Cron Triggers + Workflows |

이 표는 한 페이지 요약이다. 본격적인 코드는 6장(Hono·미들웨어·DI), 7·8장(데이터·트랜잭션), 12장(Workflows·Cron)에서 쓴다.

### 무너지는 자리 — V8 Isolate 모델이 정직하게 안 되는 것들

이 장의 마지막 박스다. 이 책의 모든 기술 챕터 끝에는 "무너지는 자리" 박스를 둔다. 광고가 아님을 가장 단순하게 보여주는 약속이다. V8 isolate 모델이 정직하게 안 되는 자리를 한 번에 모아보자.

- **임의 바이너리 실행 불가.** FFmpeg을 직접 부르고 싶은가? 안 된다. 미디어 변환은 Cloudflare Images나 별도 ECS·Lambda 워커에 맡기자.
- **full Node API의 일부 부재.** `nodejs_compat` 플래그로 상당 부분 채워졌지만, `child_process`·`cluster`·일부 native fs API는 여전히 안 된다. Sharp 같은 native binding은 그대로 못 쓴다.
- **OS syscall 불가.** POSIX 시그널, raw socket, shared memory — 다 막혀 있다. 이런 게 필요한 워크로드는 isolate에 맞지 않는다.
- **멀티스레딩 불가.** SharedArrayBuffer로 정밀 타이머 만드는 패턴이 막혀 있고, Worker 내부에서 CPU 병렬 처리가 안 된다. 병렬이 필요하면 Workflows로 step을 나누거나 여러 Worker로 fan-out하자.
- **스크립트 크기 한도.** Free 플랜 1MiB, Paid 10MiB. Spring Boot fat jar 같은 거대한 의존성 덩어리는 들어갈 자리가 없다. 큰 의존성을 줄이거나 핵심만 옮기는 편이 낫다.
- **`Date.now()`가 사실상 멈춰 있다.** Spectre 방어 정책이다. 코드 안에서 정밀 타이밍을 재서 의사결정에 쓰는 패턴은 다시 짜야 한다.

이 한계를 받아들일 수 있는 워크로드와 그렇지 않은 워크로드를 구분하는 게 5장 결정 프레임의 출발선이다. 지금은 한계 자체를 정직하게 알고 가자.

### 마무리

자, 정리해보자. 우리는 V8 isolate라는 더 가벼운 격리 모델을 살펴봤고, 그 대가로 무엇을 포기해야 하는지 짚었다. 리전이 사라진 자리에 PoP·Jurisdiction·location hint라는 다른 좌표계가 들어섰다. Bindings는 IAM role과 SDK client 두 역할을 한 추상으로 묶었고, Spring의 `@Autowired`와 사고방식이 가깝다. Compatibility Date는 런타임 안정성을 우리 손으로 잡는 시간 잠금 장치고, "I/O 대기는 과금되지 않는다"는 가격 모델은 우리가 어떤 워크로드를 어디에 둘지의 결정을 다시 그린다. Spring 개발자의 다섯 가지 멘탈 — 요청-응답, 미들웨어, DI, 트랜잭션, `@Scheduled` — 는 사라지는 게 아니라 다른 자리에 다시 그려진다.

기억해두자. **Workers는 더 가벼운 Lambda가 아니라, 가정이 다른 런타임이다.** 컨테이너가 isolate로 바뀌고, 리전이 PoP로 바뀌고, IAM이 Bindings로 바뀌고, 메모리·시간 과금이 CPU 시간 과금으로 바뀐다. 한 자리만 다르면 비교가 가능한데, 네 자리가 동시에 다르니 멘탈 모델을 통째로 다시 그릴 필요가 있다. 불편하지만 정직한 진단이다.

다음 장에서는 이 새 좌표계 위에서 우리 손으로 첫 Worker를 띄워보자. Mac에서 Wrangler를 깔고, 5분 안에 Hello World가 글로벌 PoP에 배포되어 도쿄·LA·런던에서 같은 응답이 즉시 떨어지는 광경을 직접 본다. 머리의 혼란이 손끝의 성취로 진정되는 자리다. 함께 넘어가보자.

---


## 3장. 첫 Worker를 띄우자 — Mac에서 5분 만에 글로벌 배포

월요일 아침이라고 해보자. 커피 한 잔을 옆에 두고 빈 디렉토리 하나를 새로 열었다. 2장에서 V8 isolate 이야기를 한참 듣고 나서, 머릿속에는 "그래서 이게 정말 5ms 안에 뜬다고?"라는 의심이 한 줄 남았다. 표를 아무리 들여다봐도 손에 잡히지 않는다. 그 의심을 풀 길은 하나뿐이다. **직접 한 번 띄워보는 것이다.**

이번 장의 약속은 단순하다. Mac에서 명령어 몇 줄로 `Hello, edge`라고 답하는 Worker 한 개를 도쿄·LA·런던 PoP에 동시에 올린다. 그 다음 `wrangler tail`로 로그가 떨어지는 광경을 본다. 처음부터 끝까지 다해도 5분 남짓이다. 길어야 10분. 한번 함께 해보자.

### 도구 준비 — Homebrew로 Node와 pnpm만

먼저 도구다. 익숙한 도구일수록 가볍게 가는 편이 낫다. 우리에게 필요한 건 셋뿐이다. **Node 22 이상, pnpm, 그리고 Wrangler.** 이 중 Node와 pnpm은 Homebrew로 한 번에 깐다.

```bash
brew install node@22 pnpm
node --version   # v22.x.x
pnpm --version   # 9.x 이상
```

여기서 한 가지 함정이 있다. Wrangler 자체도 Homebrew에 비슷한 이름의 패키지가 있는데, 그건 비공식이다. Cloudflare 공식 문서가 권장하는 방법은 **프로젝트 단위로 pnpm devDependency에 넣는 것**이다. 글로벌 설치(`npm i -g wrangler`)도 가능하긴 한데, 프로젝트마다 다른 버전을 요구할 때 머리가 아파진다. 어떤 프로젝트는 wrangler 3.x를 요구하고 어떤 프로젝트는 4.x를 쓰는데, 글로벌은 한 버전밖에 없다. 난감해진다. 그래서 처음부터 프로젝트 안에 가두는 편이 깔끔하다.

```bash
# 글로벌 설치 — 권장하지 않는다
npm i -g wrangler

# 프로젝트 단위 설치 — 권장
pnpm add -D wrangler@latest
```

왜 이렇게 강조하느냐. 이건 단순한 취향 문제가 아니다. Cloudflare Workers는 빠르게 변하는 플랫폼이다. wrangler 버전마다 지원하는 바인딩, 명령어 옵션, `wrangler.toml` 필드가 바뀐다. 팀에서 한 명은 4.10에서 동작하는데 다른 한 명은 3.80에 머물러 있다면, 같은 `pnpm dev` 명령에 대해 결과가 달라진다. CI에서는 또 다른 버전이 돈다. 이쯤 되면 디버깅이 아니라 점성술이 된다. 끔찍한 일이다.

프로젝트의 lockfile에 wrangler 버전이 박혀 있으면 이 모든 혼란이 사라진다. `pnpm install` 한 번이면 모든 환경에서 같은 버전이 깔린다. 그러니 처음부터 그렇게 가자.

### `wrangler login` — OAuth 한 번이면 끝

도구가 깔렸으면 Cloudflare 계정과 묶어야 한다. AWS의 IAM access key를 처음 만들 때의 그 의식 — `aws configure`, access key 입력, region 입력, 출력 포맷 입력 — 같은 게 있을 것 같지만 없다. Cloudflare는 OAuth 흐름이다.

```bash
pnpm dlx wrangler login
```

명령을 치면 브라우저가 열리고 Cloudflare 대시보드 로그인 페이지로 간다. 이미 로그인되어 있으면 권한 승인 화면이 뜬다. "Allow"를 누르면 끝이다. 터미널에 다시 돌아오면 `Successfully logged in.`이라는 한 줄이 떨어져 있다. AWS의 access key·secret key 페어를 어디에 둘지 고민하는 시간보다 짧다.

토큰은 어디에 저장될까. 홈 디렉토리의 Wrangler 설정 폴더에 들어간다. macOS에서는 대체로 `~/.config/.wrangler/` 또는 `~/.wrangler/config/` 경로에 OAuth 토큰이 저장된다(버전에 따라 위치가 살짝 달라진다). 토큰을 직접 들여다볼 일은 거의 없지만, "이 토큰이 어디 있는지 모르고 쓰는 건 찜찜하다"는 마음이 든다면 한 번 확인해보자.

```bash
ls ~/.config/.wrangler/ 2>/dev/null || ls ~/.wrangler/config/ 2>/dev/null
```

CI에서는 OAuth가 안 통한다. 대신 `CLOUDFLARE_API_TOKEN` 환경변수를 쓴다. 대시보드 → My Profile → API Tokens에서 `Edit Cloudflare Workers` 템플릿으로 토큰을 발급받아 GitHub Actions의 secret에 넣어두면 된다. 로컬은 OAuth, CI는 API token — 이 분리를 처음부터 머릿속에 박아두자. 나중에 권한 문제로 헤매는 시간이 줄어든다.

### 첫 프로젝트 — `pnpm create cloudflare`

이제 본론이다. 빈 디렉토리에서 시작하는 게 아니라, Cloudflare가 제공하는 템플릿 생성기로 한 번에 셋업하자. AWS의 `sam init`이나 `cdk init`과 비슷하지만 훨씬 가볍다.

```bash
pnpm create cloudflare@latest hello-edge
```

또는 npm을 더 좋아한다면 같은 일을 하는 명령이 있다.

```bash
npm create cloudflare@latest hello-edge
```

명령을 치면 인터랙티브 프롬프트가 줄줄이 나온다. 하나씩 보자.

- **What would you like to start with?** → `Hello World example`을 고르자. 가장 단순한 시작점이다. Hono 같은 프레임워크 템플릿도 있지만, 그건 6장에서 다룬다. 지금은 빈 캔버스가 낫다.
- **Which template would you like to use?** → `Worker only`. Static Assets·Workers + Pages 같은 옵션은 9장에서 다룬다.
- **Which language do you want to use?** → `TypeScript`. 이 책은 TS로 간다.
- **Do you want to use git for version control?** → `Yes`.
- **Do you want to deploy your application?** → 일단 `No`. 코드를 한 번 들여다본 다음 손으로 배포하는 편이 감을 잡기에 낫다.

생성이 끝나면 `hello-edge/` 디렉토리가 만들어져 있다. 들어가서 구조를 살펴보자.

```bash
cd hello-edge
ls
```

대체로 이런 모습이다.

```
hello-edge/
├── node_modules/
├── src/
│   └── index.ts
├── package.json
├── pnpm-lock.yaml
├── tsconfig.json
├── wrangler.jsonc        # 또는 wrangler.toml
└── worker-configuration.d.ts
```

`src/index.ts`를 열어보면 정말 단순하다.

```ts
export default {
  async fetch(request, env, ctx): Promise<Response> {
    return new Response('Hello World!');
  },
} satisfies ExportedHandler<Env>;
```

이 한 덩어리가 Worker의 본질이다. Lambda 핸들러처럼 보이지만 입력이 다르다. `request`는 Web Fetch API의 `Request` 객체 그대로다. `env`는 Bindings(나중에 KV·D1·R2가 들어올 자리). `ctx`는 `waitUntil`·`passThroughOnException` 같은 실행 컨텍스트. **AWS SDK가 끼어들 자리가 없다.** 표준 Web API와 Bindings 두 가지로 모든 것이 끝난다. 이게 2장에서 말한 "리전이 사라진 자리에 Bindings가 들어선다"의 첫 인상이다.

`wrangler.jsonc`도 한 번 보자.

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "hello-edge",
  "main": "src/index.ts",
  "compatibility_date": "2025-04-01",
  "observability": {
    "enabled": true
  }
}
```

세 줄이 핵심이다. `name`은 Worker 식별자이자 `<name>.<account>.workers.dev` URL의 일부가 된다. `main`은 엔트리 파일. `compatibility_date`는 2장에서 다룬 그 좌표계 — 이 날짜의 런타임 동작으로 고정된다는 뜻이다. Lambda runtime 버전과 비슷하지만 더 세밀하다. `observability.enabled`는 대시보드의 Logs 탭에서 실시간 로그를 볼 수 있게 해주는 스위치다. 켜둔 채로 가자.

### "Hello, edge"로 한 줄 고치기

기본 템플릿이 `Hello World!`라고 답하는데, 이건 너무 평범하다. 우리가 *edge*에서 도는 코드라는 걸 직접 느끼려면 이 자리에 어디서 응답이 떨어졌는지 표시해주는 게 낫다. Cloudflare는 매 요청에 어느 PoP에서 응답했는지를 `request.cf.colo` 같은 메타데이터로 담아준다. 이걸 응답 본문에 같이 넣어보자.

`src/index.ts`를 이렇게 고친다.

```ts
export default {
  async fetch(request, env, ctx): Promise<Response> {
    const colo = (request.cf as any)?.colo ?? 'unknown';
    const country = (request.cf as any)?.country ?? 'unknown';
    return new Response(
      `Hello, edge! served from ${colo} (${country})\n`,
      { headers: { 'content-type': 'text/plain; charset=utf-8' } }
    );
  },
} satisfies ExportedHandler<Env>;
```

`request.cf`는 Workers 런타임이 끼워주는 메타데이터 묶음이다. `colo`는 응답을 처리한 데이터센터의 IATA 공항 코드(예: `NRT`는 도쿄 나리타, `LAX`는 LA, `LHR`은 런던 히드로). `country`는 사용자의 국가 코드. 이 한 줄이 글로벌 배포의 첫 증거가 된다.

### `wrangler dev` — 로컬에서 production을 그대로

배포에 앞서 로컬에서 한 번 띄워보자.

```bash
pnpm dev
```

`package.json`의 `dev` 스크립트가 `wrangler dev`를 부른다. 잠시 기다리면 이런 화면이 뜬다.

```
⛅️ wrangler 4.x.x
-------------------
Your worker has access to the following bindings:
- (none)
[wrangler:info] Ready on http://localhost:8787
```

브라우저에서 `http://localhost:8787`을 열거나, 다른 터미널에서 `curl`을 날려보자.

```bash
curl http://localhost:8787
# Hello, edge! served from unknown (unknown)
```

응답이 떨어진다. 그런데 `colo`와 `country`가 `unknown`으로 나온다. 왜일까? **로컬 모드에서는 Cloudflare edge가 끼어주는 메타데이터가 없기 때문이다.** `wrangler dev`는 기본적으로 `workerd`라는 production과 같은 V8 런타임을 우리 Mac에 띄워서 isolate를 시뮬레이션한다. 정확한 isolate 동작은 그대로 재현하지만, "어느 PoP에서 도는가" 같은 글로벌 메타데이터는 진짜 PoP에서만 채워진다.

이 메타데이터까지 보고 싶다면 `--remote` 플래그를 쓰면 된다.

```bash
pnpm dlx wrangler dev --remote
```

이렇게 하면 코드는 우리 Mac에서 편집하지만 실행은 Cloudflare edge에서 일어난다. 로컬에서 시뮬레이션이 어려운 일부 기능(특정 Zone 기능, 일부 cf 메타데이터)을 테스트할 때 유용하다. 다만 매번 edge로 왕복하므로 핫 리로드 속도가 느리다. 평소에는 로컬 모드, 가끔 검증할 때 `--remote` — 이렇게 두 모드를 오가는 편이 낫다.

자, 이제 마음에 든다. 배포해보자.

### `wrangler deploy` — 한 줄로 글로벌 배포

```bash
pnpm dlx wrangler deploy
```

또는 `package.json`에 `deploy` 스크립트가 잡혀 있으면 `pnpm deploy`로도 된다. 명령을 치면 이런 출력이 줄줄이 떨어진다.

```
Total Upload: 0.42 KiB / gzip: 0.30 KiB
Worker Startup Time: 4 ms
Uploaded hello-edge (1.85 sec)
Deployed hello-edge triggers (0.81 sec)
  https://hello-edge.<your-account>.workers.dev
Current Version ID: 01234567-89ab-...
```

**2초 남짓이다.** 이 한 줄에 충분히 음미할 거리가 있다. `Worker Startup Time: 4 ms` — 우리 Worker의 콜드스타트가 4ms라는 뜻이다. Lambda에서 JVM 띄우는 데 보통 2~3초 걸리던 그 시간을 떠올려보자. SnapStart로 줄여도 100ms 단위였다. Workers는 그 자리에서 단순히 한 자릿수다. 그리고 `Deployed hello-edge triggers` — 이 한 줄이 떨어진 순간, 우리 코드는 이미 330개 넘는 PoP에 동시 배포되어 있다. CDN의 invalidation을 기다릴 필요가 없다. 이건 가장자리 얘기가 아니라 본체 얘기다.

URL을 받아 브라우저에서 열거나 `curl`을 한 번 쳐보자.

```bash
curl https://hello-edge.<your-account>.workers.dev
# Hello, edge! served from ICN (KR)
```

서울에서 응답이 떨어졌다(ICN은 인천공항 코드). 한국에서 접속했으니 가장 가까운 PoP가 골랐다. 이게 edge-first의 첫 손맛이다.

### 도쿄·LA·런던에서 정말로 도는지 확인하기

같은 Worker가 다른 대륙에서도 잘 도는지 직접 검증해보자. 가장 단순한 방법은 응답 헤더의 `cf-ray`를 보는 것이다. `cf-ray`는 매 요청에 Cloudflare가 붙이는 식별자인데, 끝부분 세 글자가 응답한 PoP의 공항 코드다.

```bash
curl -v https://hello-edge.<your-account>.workers.dev 2>&1 | grep -i cf-ray
# < cf-ray: 8a1b2c3d4e5f6789-ICN
```

여기서는 `ICN`이 떨어졌다. 우리 머신이 한국이니 당연하다. 그렇다면 다른 나라에서 들어오는 척하려면 어떻게 할까? 가장 손쉬운 길은 외부 검증 도구를 쓰는 것이다.

- **무료 글로벌 ping/HTTP 체크 서비스**(검색하면 여럿 있다)에 우리 Worker URL을 넣어보면, 도쿄·LA·런던·시드니에서 실제로 호출했을 때의 응답 시간과 헤더를 보여준다.
- 또는 VPN을 일본·미국·유럽 끝점으로 바꿔가며 같은 `curl`을 반복해도 된다.

실측이 번거롭다면 응답 본문에 우리가 넣어둔 `colo`만 봐도 충분하다. 일본 VPN으로 들어오면 `NRT` 또는 `KIX`(오사카), 미국 서부 VPN이면 `LAX` 또는 `SFO`, 영국이면 `LHR`이 떨어진다. **같은 코드, 같은 URL, 다른 PoP.** AWS에서 같은 일을 하려면 us-east-1, ap-northeast-1, eu-west-1 세 군데에 Lambda를 따로 배포하고 Route 53 latency-based routing을 걸어야 한다. 시간으로 따지면 한나절이다. Workers는 한 줄로 끝났다.

### `wrangler tail`로 실시간 로그 보기

배포가 됐으니 운영 감각도 한 번 잡자. CloudWatch Logs에 익숙한 사람이라면 "그래서 로그는 어디서 보지?"가 다음 의문일 것이다. 로컬에서는 `wrangler dev`의 콘솔에 그대로 떨어졌다. 배포된 Worker의 로그는 어떻게 볼까?

가장 손쉬운 방법은 `wrangler tail`이다.

```bash
pnpm dlx wrangler tail hello-edge
```

명령을 치면 그 자리에서 스트리밍이 시작된다. 다른 터미널에서 `curl`을 몇 번 던져보자.

```bash
curl https://hello-edge.<your-account>.workers.dev
curl https://hello-edge.<your-account>.workers.dev
```

`tail` 쪽 터미널에 요청 한 건씩 떨어지는 광경이 뜬다. 응답 코드, URL, `colo`, `country`까지. `console.log`를 코드에 넣어두면 그 출력도 그대로 따라온다. CloudWatch에 5~10초 지연으로 도착하는 로그를 기다리던 시간을 생각하면, 이건 거의 즉각이다.

```ts
console.log('request received', { colo, country, path: new URL(request.url).pathname });
```

이 한 줄을 넣고 다시 배포하면(`pnpm dlx wrangler deploy`), `wrangler tail`에 구조화된 로그가 떨어진다. 디버깅의 첫 도구다.

물론 `tail`은 사람이 보는 도구다. 운영 환경에서는 로그를 어딘가에 영속시켜야 한다. 그건 13장 운영 챕터에서 Workers Logpush로 R2·외부 APM에 보내는 패턴을 다룬다. 지금은 "실시간으로 일단 보인다"는 감각만 챙기자.

대시보드에서도 같은 일을 할 수 있다. Cloudflare 대시보드 → Workers & Pages → `hello-edge` → Logs 탭에 들어가면 `wrangler tail`과 같은 스트림이 브라우저에서 흐른다. 그 옆 Metrics 탭에서는 요청 수, CPU time, error rate, 응답 시간 분포가 시각화된다. CloudWatch의 통합 대시보드에 비하면 단출하지만, **첫 운영 감각을 잡는 데는 충분하다**. 더 깊은 관측은 외부 APM(Sentry·Baselime·Axiom·Datadog)으로 보내는 패턴이 표준이다 — 이것도 13장에서 다룬다.

### 이 기술이 무너지는 자리

처음 배포까지 한 사이클을 도는 동안 모든 게 매끄럽게 흘러갔다면, 그건 운이 좋았던 거다. 실제로는 다음 다섯 자리에서 자주 발이 걸린다. 미리 알아두자.

**첫째, `workers.dev` 도메인은 검색 엔진에서 페널티를 받는다.** `<name>.<account>.workers.dev`로 영원히 살 생각은 하지 말자. 개발·테스트용으로는 더없이 편하지만, 일반 사용자에게 노출하는 production URL이라면 custom domain을 붙여야 한다. Cloudflare에 도메인을 옮겨두었다면 대시보드에서 Routes 또는 Custom Domain을 한 번 눌러주면 끝이다. DNS 전파가 보통 몇 분 안에 끝나지만, 가끔 30분 넘게 걸리는 경우가 있어 답답할 수 있다. 찜찜하다면 `dig` 또는 `nslookup`으로 확인하면서 가자. workers.dev에 production 트래픽을 그대로 두는 건 나중에 SEO 문제를 한 번 만나야 깨닫는 종류의 실수다. 처음부터 피하는 편이 낫다.

**둘째, 무료 plan의 일일 한도는 100,000 요청이다.** Workers Free에는 100k req/일·CPU 10ms/요청 한도가 있다. 친구들 몇 명이 호기심에 눌러보는 정도라면 차고 넘치지만, 한 번 입소문을 타거나 봇이 무차별 호출하면 하루 안에 한도에 도달한다. 한도를 넘으면 그 날의 나머지 요청은 1015 에러로 거절된다. production에 가까워졌다면 Workers Paid($5/월)로 올라가자. 1천만 요청까지 포함이고 추가 사용량은 100만 req당 $0.30이다. 이쯤 가격이면 EC2 t3.nano 한 대 값이다. 망설일 자리가 아니다.

**셋째, npm 패키지 중 Node API 깊이 의존하는 것은 V8 isolate에서 안 돈다.** `node:fs`로 파일 시스템에 쓰는 라이브러리, `child_process`로 외부 프로세스 부르는 라이브러리, native binding을 가진 라이브러리(Sharp, bcrypt 같은) — 이런 건 그대로 못 쓴다. 일부 Node API는 `compatibility_flags`에 `nodejs_compat`을 켜면 동작한다. `wrangler.jsonc`에 한 줄 추가하면 된다.

```jsonc
{
  "compatibility_flags": ["nodejs_compat"]
}
```

이렇게 켜두면 `node:buffer`, `node:crypto`, `node:url`, `node:stream` 같은 자주 쓰는 모듈이 polyfill로 들어온다. 그래도 `node:fs`처럼 디스크 I/O를 요구하는 모듈은 여전히 안 된다. 이건 polyfill로 해결할 일이 아니라 isolate 모델 자체의 경계다. 기존 Node 백엔드를 그대로 옮기려고 하면 이 자리에서 발이 걸린다. 어떤 의존성이 안 도는지 미리 한 번 점검하는 편이 낫다(2장의 "Workers에서 절대 못 하는 것 7가지" 점검표가 그 자리다).

**넷째, route 충돌이다.** 같은 zone에 여러 Worker가 있고 route가 겹치면, Cloudflare는 가장 구체적인 패턴 하나만 활성화한다. `*.example.com/*`에 Worker A가 잡혀 있는데 `api.example.com/*`에 Worker B를 새로 잡으면, `api.example.com`의 트래픽은 B로 간다. 익숙해지기 전에는 "왜 이 요청이 저 Worker로 가지?"라며 30분 동안 디버깅하게 된다. 대시보드의 Routes 탭에서 현재 활성 route 목록을 한눈에 볼 수 있으니, 새 Worker를 붙이기 전에 한 번 들여다보자.

**다섯째, `compatibility_date`를 그대로 두면 새 기능이 안 들어온다.** 템플릿이 만들어 준 날짜는 그 시점의 런타임 동작으로 고정된다. 6개월 뒤 Cloudflare가 멋진 새 API를 발표해도, 우리 Worker의 `compatibility_date`가 옛날 그대로면 새 API가 안 보인다. 고치는 건 한 줄이지만, 한 번 올리고 나면 동작 변화가 있을 수 있으니 staging에서 한 번 돌리고 가는 편이 낫다. 분기마다 한 번씩 날짜를 갱신하는 습관을 들이자. 광고가 아니라 실무 권유다.

이 다섯 자리만 넘기면, 첫 배포부터 실서비스로 가는 길이 꽤 매끄럽다.

### 정리 — 손끝의 성취가 머리의 혼란을 진정시킨다

1장에서 우리는 "Cloudflare는 또 하나의 클라우드가 아니다"라는 말 한 줄을 받았다. 2장에서는 V8 isolate·리전 부재·Bindings·Compatibility Date라는 새 좌표계를 머리로 한 번 그려봤다. 표를 봐도 그림이 도식적이고, 손에 잡히지 않았을 것이다.

이 장에서 우리는 그 좌표계 위에 첫 점을 찍었다. **Mac에서 wrangler를 깔고, 한 줄짜리 코드를 짜고, 한 명령으로 글로벌 배포까지.** 5분 안에 한 사이클이 돌았다. 도쿄·LA·런던에서 같은 응답이 떨어지는 광경을 직접 봤고, `wrangler tail`에 로그가 즉시 흐르는 감각을 손에 쥐었다. 머리의 혼란이 한 번 진정됐다면, 이 챕터의 일은 다 한 셈이다.

다음 4장에서는 이 감각 위에 지도를 펼친다. Lambda·S3·DynamoDB·CloudFront·Step Functions — AWS의 익숙한 이름들이 Cloudflare의 어느 자리에 어떻게 자리 잡는지 카탈로그를 본격적으로 그려본다. 동시에 1:1 매핑이 거짓말이 되는 다섯 가지 패턴도 미리 표시해둔다. 4장이 지도라면, 5장은 그 지도 위에서 "그래서 내 워크로드 중 무엇을 옮길 것인가"의 결정 도구가 된다. 그 두 장이 지나면, 6장부터는 본격 실무다.

**지금 이 순간 우리 손에는 Worker 도메인 하나가 있다.** `https://hello-edge.<account>.workers.dev`. 이 작은 한 줄짜리 Worker가 누적 실습 프로젝트 `toby-shop`의 시드다. 6장에서 라우팅·미들웨어·인증이 붙고, 7장에서 D1과 Drizzle이 들어오고, 12장에서는 결제 후 영수증 Workflow와 RAG 챗봇까지 얹는다. 한 줄에서 시작해 한 권의 책 분량으로 자라간다. 그 첫 줄을 우리 손으로 깐 것이다. 자, 다음 장으로 넘어가보자.

---


## 4장. AWS ↔ Cloudflare 매핑 카탈로그 — 1:1 표가 거짓말이 되는 지점들

팀 회의실에 모여 화이트보드 앞에 서 있다고 해보자. 누군가가 마커를 들고 표를 그리기 시작한다. 왼쪽에는 AWS, 오른쪽에는 Cloudflare. Lambda 옆에 Workers를 적고, S3 옆에 R2를 적고, DynamoDB 옆에 KV를 적는다. 그리고는 자신 있게 한 줄을 덧붙인다. "그러니까, DynamoDB는 Cloudflare에서 KV로 쓰면 되는 거죠?"

이 장면이 낯설지 않다면, 그건 우리 모두가 한 번쯤 같은 표를 그려봤기 때문이다. 그리고 그 표를 들고 한 달쯤 마이그레이션을 해본 사람이라면, 표 어딘가에서 자기 코드가 발이 걸려 넘어지는 광경을 본 적이 있을 것이다. 1:1 매핑은 정직한 도구처럼 보이지만, 실제로는 가장 위험한 종류의 지도다. 두 플랫폼의 표면이 비슷하게 생긴 자리에 동그라미를 그려 놓고, 그 안쪽 가정이 다르다는 사실을 표가 가려버리기 때문이다.

이 장에서는 매핑 표를 펼친다. 컴퓨트, 스토리지·DB, 네트워크·CDN·DNS, 보안, 메시징·이벤트, AI 여섯 카테고리다. 그런데 표만 그리고 끝내지 않는다. 각 행 끝에 "1:1로 보면 안 되는 이유"를 한두 줄씩 박아 둔다. 그 한두 줄이 사실 이 장의 본문이다. 표는 지도이고, 한두 줄짜리 주석은 그 지도의 위험 표시다. 위험 표시 없는 지도는 친절한 척하는 함정이다.

자, 한 카테고리씩 살펴보자.

### 카테고리 1. 컴퓨트 — 같은 "서버리스"라는 단어 아래의 다른 행성

먼저 컴퓨트다. AWS 개발자가 Cloudflare를 처음 마주칠 때 가장 먼저 그리는 표가 이 자리에 있다. Lambda는 Workers, Lambda@Edge도 Workers, ECS·Fargate는 Workers Containers, Step Functions는 Workflows. 네 줄짜리 깔끔한 표다. 그런데 이 네 줄 모두에서 1:1 매핑이 거짓말을 한다. 종류가 조금씩 다른 거짓말이다.

| AWS | Cloudflare | 1:1로 보면 안 되는 이유 |
|---|---|---|
| **Lambda** | **Workers** | Lambda는 Firecracker microVM(컨테이너 모델), Workers는 V8 isolate. 콜드스타트 5ms vs 200ms~수초. 임의 바이너리·full Node API·OS syscall 불가. 가격 모델이 GB-s vs CPU-time이라 I/O 대기 비용이 정반대로 잡힌다. |
| **Lambda@Edge** | **Workers** | Lambda@Edge는 CloudFront 트리거에 묶이고 동남아·남미에서 400~600ms 콜드스타트가 보고된다. Workers는 모든 PoP에서 글로벌 균일 5ms 미만. "둘 다 edge"라는 단어로 묶지 말자. |
| **ECS / Fargate** | **Workers Containers** | Workers Containers는 인스턴스당 0.5 vCPU / 4 GiB RAM 한도(2026 5월 기준). 더 큰 워크로드는 ECS가 그대로 우위. GPU·VPC peering 깊은 워크로드는 옮기지 말자. |
| **Step Functions** | **Workflows** | Step Functions는 ASL DSL + state transition 단위 과금, Workflows는 코드(`step.do`/`step.sleep`) + CPU time만 과금. AWS 200+ 액션 통합이라는 ecosystem 종속을 옮기는 건 단순한 일이 아니다. |

표는 4줄이지만, 짚고 갈 자리가 더 있다. 함께 살펴보자.

Lambda↔Workers를 한 줄에 묶는 가장 흔한 실수는 "둘 다 함수형 서버리스니까 비슷하다"는 인식이다. 같은 단어, 다른 행성이다. Lambda는 함수마다 Firecracker microVM 컨테이너를 띄운다. JVM이 무거우면 첫 호출에 수 초가 걸리고, SnapStart·Provisioned Concurrency·GraalVM Native가 그 고통을 우회하기 위해 태어났다. Workers는 한 V8 프로세스 안에서 isolate를 켠다. OS 프로세스를 새로 만들지 않으니 5ms 미만으로 떨어진다. 그 대가는 분명하다. 임의 바이너리 spawn 안 되고, full Node API 안 되고, OS syscall 안 되고, 멀티스레딩 안 되고, 1MB(Free)·10MB(Paid) 스크립트 한도가 있다. Spring Boot 전체 컨텍스트를 Lambda에 올려서 돌리던 사람이 그대로 Workers로 옮기려 들면, 첫 빌드부터 무너진다. Lambda layers로 의존성을 분리하던 패턴이 Workers에는 없다. *모델 자체가 다르다.*

가격 모델 차이는 더 흥미롭다. Lambda는 GB-s × 요청 수다. 외부 API를 호출하고 응답을 5초 기다리는 동안에도 메모리는 lock되고 비용은 흐른다. Workers Standard는 CPU time × 요청 수다. **외부 API·DB 응답을 기다리는 동안에는 과금되지 않는다.** AI 호출처럼 LLM 응답을 5~10초씩 기다리는 워크로드라면, 같은 일에 대한 비용이 한 자릿수가 아니라 두 자릿수로 벌어진다. 1:1 매핑 표는 "둘 다 서버리스"로 묶지만, 가격 모델 자체가 어떤 워크로드를 환영하고 어떤 워크로드를 거절하는지가 정반대다. AI 게이트웨이·외부 API 프록시·orchestration 같은 I/O 대기 위주 코드는 Workers 위에서 살이 붙고, CPU 무거운 batch나 거대한 의존성 덩어리는 Lambda 위에서 살이 붙는다.

Lambda@Edge↔Workers는 더 단순한 거짓말이다. "둘 다 edge에서 도는 함수"로 묶이지만, 본질적으로 Lambda@Edge는 *CloudFront에 묶인 트리거*다. CloudFront 이벤트 — viewer request, viewer response, origin request, origin response — 에 한정해서 호출되고, 콜드스타트는 PoP에 따라 들쭉날쭉하다. Rebal AI의 6개월 production 보고서에 따르면 동남아·남미 PoP에서 400~600ms 콜드스타트가 측정됐다. Workers는 모든 PoP에서 글로벌 균일하다. 한 줄로 매핑하면 이 사실이 표에서 사라진다.

ECS·Fargate↔Workers Containers는 매핑이 가장 어색한 자리다. Cloudflare가 2024~2025년에 Containers를 발표하면서 "ECS의 자리"를 부분적으로 가져왔지만, 2026년 5월 기준 인스턴스당 0.5 vCPU / 4 GiB RAM이 한도다. 데이터 처리 batch·머신러닝 추론·VPC 깊이 연동된 마이크로서비스는 ECS·Fargate가 그대로 우위다. *옮기지 말자.* 옮기는 게 자연스러운 자리는 작은 컨테이너로 풀리는 사이드카·작은 서비스·실험적 워크로드 정도다. Cloudflare 공식 표가 "ECS와 동등"이라고 말하는 게 아니다. 글로벌 PoP에 ~10초 안에 배포된다는 운영 속도 차이가 실제 가치다.

Step Functions↔Workflows는 가격 모델 차이가 가장 또렷한 자리다. Step Functions는 state transition 단위로 과금된다. 외부 승인을 한 시간 기다리는 long-poll, 사람이 결재를 누를 때까지의 대기 — 그 모든 transition이 청구서에 잡힌다. Workflows는 *실행 중인 CPU 시간만* 과금하고, sleep·외부 API 대기는 $0이다. 30일짜리 trial 만료 알림 워크플로를 만든다고 해보자. Step Functions로 짜면 30일짜리 sleep state가 비용에 잡히고, Workflows로 짜면 그 30일은 0원이다. 한편 Step Functions의 200+ AWS 서비스 통합(IAM·S3·SNS·EventBridge에 한 줄짜리 task로 연결되는 것들)은 Workflows에 같은 형태로 없다. 옮기는 자리에 따라 무엇을 잃고 무엇을 얻는지가 정반대로 갈린다.

이 카테고리의 한 줄 요약. *"같은 서버리스"라는 단어로 묶지 말자.* 격리 모델이 다르고, 가격 모델이 다르고, 통합 ecosystem이 다르다. 표 한 줄로는 가려지지 않는 차이다.

### 카테고리 2. 스토리지·DB — DynamoDB 한 줄 매핑은 거짓말이다

다음은 스토리지·DB다. 이 카테고리가 매핑의 함정이 가장 깊게 파인 자리다. 특히 DynamoDB. 이 한 이름을 어떻게 다루느냐로 마이그레이션의 성공과 실패가 6개월쯤 뒤에 갈린다.

| AWS | Cloudflare | 1:1로 보면 안 되는 이유 |
|---|---|---|
| **S3** | **R2** | API는 거의 호환(PUT/GET/multipart/presigned). egress free가 결정타. 단, Lifecycle policy·Glacier·Object Lock 일부 부재. AWS→R2 inbound 첫 마이그레이션 청구서는 AWS egress로 잡힌다. |
| **DynamoDB** | **KV / D1 / Durable Objects 중 선택** | 한 줄 매핑은 거짓말. read-heavy·세션·플래그면 KV, 관계형·SQL 쿼리면 D1, 강한 일관성·per-entity·트랜잭셔널이면 DO. **사용 패턴별로 갈라진다.** |
| **DynamoDB (transactional)** | **Durable Objects** | 재고·예약·턴 게임처럼 race condition 방어가 필요한 자리. DO는 actor 모델로 single-threaded처럼 직렬화된 처리를 보장한다. |
| **DynamoDB (read-heavy + 글로벌)** | **KV** | eventually consistent (최대 60초 전파), per-key 1 write/s, **secondary index 없음, range query 없음**. Liftosaur가 회귀한 결정적 이유. |
| **RDS / Aurora** | **D1 (작은 규모) / Hyperdrive (기존 DB 그대로)** | D1은 SQLite at edge, 1 DB 10GB 한도, sustained write 500~2k/s. Hyperdrive는 DB가 아니라 connection pool + 쿼리 캐시 — 이름의 함정. |
| **ElastiCache (Redis)** | **Cache API + KV / DO + Upstash Redis** | ElastiCache는 TCP 기반이라 Workers에서 직접 못 쓴다. REST 기반 Redis(Upstash 같은)만 edge에서 사용 가능. |
| **OpenSearch (vector)** | **Vectorize** | 글로벌 분산, 인덱스당 5M vector. **hybrid search 미지원**(2026 기준). 큰 규모·hybrid search는 OpenSearch 유지. |

자, 이 표 위에서 가장 무거운 한 줄은 두 번째다. *DynamoDB ↔ KV 한 줄 매핑은 거짓말이다.* 이 거짓말을 믿고 production 시스템을 옮긴 사람이 어떤 일을 겪는지, Liftosaur 사례로 잠시 따라가 보자.

Liftosaur는 운동 트래킹 앱을 만드는 1인 개발자의 서비스였다. 처음에 Workers + KV 위에 시스템을 올렸다. 사용자 데이터를 KV에 키-값으로 저장하고, 글로벌 분산·낮은 가격·콜드스타트 없는 응답이라는 약속에 끌렸다. 그런데 6개월쯤 운영하다 보니 슬슬 코드가 비비 꼬이기 시작했다. 사용자 별로 운동 기록을 조회하려면 secondary index가 필요한데, KV에는 그게 없다. 단일 키 lookup만 된다. 어쩔 수 없이 별도 인덱스 키를 직접 관리하기 시작했고, 그게 곧 두 개의 데이터 소스를 동기화하는 코드로 번졌다. 게다가 이미지 처리에 Sharp 같은 Node native 라이브러리가 필요했는데, Workers에서 동작하지 않았다. 1MB 스크립트 한도(당시 기준)에 걸려 의존성을 넣을 수도 없었다. 결국 Liftosaur는 Lambda + DynamoDB로 회귀했다. *정직한 후퇴*다. KV는 잘못된 도구가 아니었다. *이 워크로드에 맞지 않는 도구*였을 뿐이다.

이 사례가 가르쳐주는 건 단순하다. DynamoDB라는 한 이름이 실제로는 셋의 자리에 갈라져 있다. **read-heavy + 글로벌 + eventually consistent OK**라면 KV가 자연스럽다. 세션·feature flag·API key·configuration이 그 자리다. **관계형 + SQL 쿼리 + JOIN/CTE/트랜잭션**이 필요하다면 D1이다. SQLite 기반이라 1 DB 10GB·sustained write 2k/s 한도가 있지만, 작은~중간 규모 서비스의 사용자 프로필·게시물·주문에는 충분하다. **per-entity 강한 일관성 + 직렬화된 처리 + 트랜잭셔널**이 필요하면 Durable Objects다. 재고 차감, 좌석 예약, 게임 턴, 채팅방 메시지 순서 — 이런 자리는 DO 외에는 답이 없다. DynamoDB의 transactional API로 짜던 코드가 정확히 여기에 자리를 잡는다.

S3↔R2는 매핑이 가장 솔직한 자리다. API가 거의 호환된다. `aws-sdk` 클라이언트의 endpoint만 R2로 바꾸면 PUT/GET/multipart/presigned URL이 그대로 동작한다. 그리고 egress가 무료다. S3 Standard는 storage가 GB당 약 $0.023, egress가 GB당 약 $0.09다. R2는 storage가 GB당 약 $0.015, egress 0이다. 30TB를 한 달 동안 다운로드하면 S3에서는 $2,700이 나오고 R2에서는 $0이다. Baselime이 AWS에서 Cloudflare로 옮긴 뒤 일 비용이 $790에서 $25로 떨어진 사례에서 가장 큰 절감 항목이 정확히 이 egress였다. *그렇다면 모두 옮기면 되는 것 아닌가?* 아쉽게도 한 줄 매핑이 가리는 함정이 셋 있다. 첫째, Lifecycle policy·Glacier·Object Lock 같은 enterprise 기능이 일부 부재하다. 컴플라이언스로 Object Lock이 강제된다면 옮기지 말자. 둘째, Class A operations(쓰기·list)와 Class B operations(읽기)는 과금된다. 작은 객체를 초당 수천 번 읽는 워크로드는 결국 비용이 누적된다. 셋째, AWS에서 R2로 처음 데이터를 보내는 inbound는 *AWS의 egress로 잡힌다.* 30TB를 옮기면 마이그레이션 첫 달에 $2,700짜리 청구서가 한 번 더 온다. 이걸 알고 옮기는 것과 모르고 옮기는 것의 마음 고생은 두 자릿수가 다르다.

RDS·Aurora↔D1·Hyperdrive는 두 갈래로 갈라지는 매핑이다. D1은 *대안*이고 Hyperdrive는 *그대로 살리는 길*이다. D1은 SQLite at edge다. JOIN·CTE·트랜잭션 다 된다. 1 DB 10GB·sustained write 500~2k/s가 한도다. 작은 서비스의 사용자 프로필이나 작은 부속 도메인은 충분히 D1으로 옮길 수 있다. 반면 거대한 Aurora 클러스터를 한 번에 D1로 옮기려고 들면, write throughput에서 무너진다. *옮기지 말자.* 그 자리에 들어오는 도구가 Hyperdrive다. 이름이 함정인데, 이건 DB가 아니라 *connection pool + 쿼리 캐시*다. Workers는 V8 isolate라 TCP 직접 연결이 어렵다. TCP handshake 1 round-trip + TLS 3 + DB auth 3 = 7 round-trip이 매 요청마다 태평양을 건너야 하면 응답시간이 무너진다. Hyperdrive가 그 7 round-trip을 글로벌 풀에서 흡수한다. AWS RDS·Aurora에 publicly accessible 옵션 + Security Group 설정으로 그대로 붙일 수 있다. *DB는 AWS, 컴퓨트는 Cloudflare* 라는 하이브리드 패턴의 가장 risk-low한 첫 발걸음이 이 도구다. 10장에서 본격 다룬다.

ElastiCache↔Cache API + KV + DO 조합은 어색한 자리다. ElastiCache는 TCP 기반 Redis다. Workers는 TCP 직접 연결이 어렵기 때문에 ElastiCache를 직접 못 쓴다. 그래서 Cache API(요청 단위 ephemeral KV), KV(글로벌 eventual), DO(per-key strong)를 워크로드 패턴별로 조합한다. REST 기반 Redis인 Upstash 같은 3rd party 서비스라면 Workers에서 그대로 사용할 수 있다. *Redis 멘탈을 그대로 옮기려고 하면 자리가 안 보인다.* 캐싱이 무엇을 위한 캐싱인가를 다시 묻는 게 정직한 길이다.

OpenSearch k-NN·pgvector↔Vectorize는 표 한 줄에 가릴 수 없는 한계가 있다. Vectorize는 글로벌 분산되어 있고 인덱스당 5M vector를 지원한다. 그런데 2026년 5월 기준 **hybrid search(벡터 + full-text 결합)를 지원하지 않는다.** RAG 챗봇에서 키워드 + 의미 검색을 함께 돌리는 패턴이 표준이 된 시대에 이건 큰 한계다. 단순 의미 유사도 검색만 필요하다면 Vectorize가 자연스럽지만, hybrid search가 필요한 자리에는 OpenSearch나 pgvector를 그대로 두는 편이 낫다. *지금* 옮기지 말고, hybrid search 지원이 들어온 다음에 다시 보자.

이 카테고리의 한 줄 요약. *DynamoDB는 셋으로 갈라지고, S3는 솔직하지만 첫 청구서가 깜짝 놀랄 만하고, RDS는 옮기지 않고도 Hyperdrive로 살린다.* 매핑 표는 이 셋을 모두 한 줄로 말하지 못한다.

### 카테고리 3. 네트워크·CDN·DNS — 본체와 부속의 자리가 뒤집힌다

세 번째 카테고리다. 네트워크·CDN·DNS는 매핑이 표면적으로는 가장 자연스러워 보이는 자리다. CloudFront ↔ Cloudflare CDN, Route 53 ↔ Cloudflare DNS, ALB ↔ Workers Routes. 세 줄짜리 깔끔한 표다. 그런데 깊이 들여다보면 *본체와 부속*의 자리가 뒤집혀 있다.

| AWS | Cloudflare | 1:1로 보면 안 되는 이유 |
|---|---|---|
| **CloudFront** | **Cloudflare CDN (기본 포함)** | Cloudflare는 모든 PoP가 풀스택(컴퓨트·캐시·WAF). CloudFront는 캐시 + 제한된 함수, 무거운 컴퓨트는 Lambda@Edge 별도. Purge 속도 ~150ms vs 10~15분. Cloudflare 무료 plan이 무제한 대역폭·DDoS 방어·SSL 포함. |
| **Route 53** | **Cloudflare DNS** | Lookup ~11~13ms vs ~20ms. Cloudflare DNS 도메인당 무료 vs Route 53 hosted zone $0.50/월 + 쿼리 과금. 다만 weighted/geo/failover 같은 정교한 라우팅은 Route 53가 더 풍부. |
| **ELB / ALB** | **Workers Routes / Custom Domains** | "둘 다 트래픽을 라우팅"한다고 묶으면 안 된다. ALB는 VPC 안의 EC2·ECS task로 분배, Workers Routes는 URL 패턴 → Worker 매핑. 사설망 격리 모델이 정반대. |
| **API Gateway** | **Workers Routes + Hono (또는 itty-router)** | API Gateway에 해당하는 별도 제품이 없다. URL·custom domain은 Workers Routes로, 미들웨어·라우팅·검증은 코드(Hono)로 짠다. AI 트래픽이라면 별도로 AI Gateway가 자리를 잡는다. |

CloudFront↔Cloudflare CDN을 한 줄로 묶는 건 표면만 닮았다. 본질은 정반대다. AWS의 멘탈에서 *edge는 부속물*이다. 본체는 리전 안에 있다. EC2·RDS·DynamoDB가 한 리전에 있고, 그 앞에 CloudFront 캐시 한 겹을 더 깐다. CloudFront PoP는 캐시 + 제한된 함수만 제공하고, 무거운 컴퓨트는 Lambda@Edge라는 별도 제품으로 분리되어 있다. Cloudflare는 거꾸로다. *모든 PoP가 풀스택이다.* 같은 PoP에서 CDN 캐시도 돌고, Workers 컴퓨트도 돌고, WAF도 돌고, KV·R2 캐시도 들어간다. 한 사용자가 도쿄에서 요청을 보내면, 도쿄 PoP에서 캐시 확인 → Worker 실행 → KV 조회 → 응답까지 한 자리에서 끝난다. *본체와 부속이 뒤집혀 있다.* CloudFront에 익숙한 사람이 Cloudflare를 "더 빠른 CDN" 정도로 보기 시작하면, 이 뒤집힘이 표에서 사라진다.

Purge 속도 차이도 흥미롭다. Cloudflare는 글로벌 purge에 ~150ms가 걸린다. CloudFront는 10~15분이다. 100배 차이다. 정적 자산을 자주 갱신하는 워크로드(예: 잘못 올린 이미지를 빠르게 교체해야 하는 e-commerce)에서는 운영 감각 자체가 다르다. 잘못된 자산을 올렸을 때 "Cloudflare에서는 즉시 교체된다"와 "CloudFront에서는 15분 기다린다"는 incident response의 호흡 자체를 바꾼다.

Route 53↔Cloudflare DNS는 매핑이 가장 솔직한 자리다. 둘 다 권위 DNS 서버다. Cloudflare가 lookup 평균 ~11~13ms, Route 53가 ~20ms 정도로 측정되곤 한다. 가격 모델은 Cloudflare가 도메인당 기본 무료이고, Route 53가 hosted zone $0.50/월 + 쿼리 과금이다. 작은~중간 서비스라면 Cloudflare DNS가 거의 항상 더 저렴하고 더 빠르다. 다만 한 줄 매핑이 가리는 자리가 있다. **weighted routing, geolocation routing, failover routing** 같은 정교한 트래픽 분배는 Route 53가 여전히 더 풍부하다. 단순한 A 레코드 + CNAME 조합이라면 Cloudflare DNS로 옮기는 게 무위험이지만, 복잡한 라우팅 규칙이 있다면 *옮기기 전에 Cloudflare DNS의 Load Balancer 기능과 정확히 매핑되는지* 확인하자.

ALB↔Workers Routes·Custom Domains는 매핑 시도 자체가 어색하다. ALB는 VPC 안의 EC2·ECS task로 트래픽을 분배하는 도구다. Target Group, Health Check, Sticky Session, Path-based routing — 사설망 격리 모델 위에 얹혀 있다. Workers Routes는 *URL 패턴 → Worker 매핑*이다. 사설망 같은 게 없다. 글로벌 PoP에 떠 있는 Worker 코드에 "이 URL로 들어온 요청은 너에게 보낸다"고 약속하는 라우팅 테이블이다. 이름은 비슷해 보이지만 본질이 정반대다. ALB를 그대로 매핑하려는 시도 자체가 함정이다. 정확한 그림은 이렇다. *ALB의 자리는 사라진다.* 글로벌 PoP에 코드가 떠 있는 모델에서는 "어느 인스턴스로 분배할지"의 결정이 더 이상 필요하지 않다. PoP가 사용자에게 가장 가까운 곳에서 알아서 응답한다. ALB가 풀던 문제가 다른 자리에서 사라진 셈이다.

API Gateway↔Workers Routes + Hono는 매핑이 둘로 갈라지는 자리다. API Gateway에 해당하는 *별도 제품*이 Cloudflare에는 없다. URL 패턴·custom domain은 Workers Routes로, 미들웨어·라우팅·검증·인증·rate limit은 *코드 안에서* 짠다. Hono 같은 프레임워크가 그 코드의 자리를 채운다. 이건 일을 잃은 게 아니라 *일이 코드 쪽으로 옮겨온 것*이다. API Gateway의 Authorizer를 한 클릭으로 붙이던 사람에게는 처음엔 번거롭게 느껴진다. 그러나 코드로 짜는 미들웨어는 IaC와 자연스럽게 어울리고, 테스트·디버깅이 훨씬 쉬워진다. 6장에서 본격적으로 다룬다.

이 카테고리의 한 줄 요약. *본체와 부속의 자리가 뒤집혀 있고, ALB의 자리는 아예 사라지며, API Gateway는 코드로 옮겨온다.* 이름만 매핑하면 가려지는 사실이다.

### 카테고리 4. 보안 — IAM의 자리는 셋으로 흩어진다

네 번째는 보안이다. 이 카테고리에서 매핑이 가장 거짓말을 하는 자리는 IAM이다. Cloudflare에는 IAM에 정확히 1:1로 매핑되는 단일 제품이 없다. *그 자리가 셋으로 흩어진다.*

| AWS | Cloudflare | 1:1로 보면 안 되는 이유 |
|---|---|---|
| **IAM (사용자·서비스 인증)** | **(1:1 등가 없음) — Bindings + Cloudflare Access + WAF rule 조합** | IAM의 정교한 정책 언어에 직접 등가물이 없다. Worker 간 권한은 코드 레벨 Bindings, 사람·디바이스 액세스는 Access, 트래픽 단 권한은 WAF. 셋의 조합으로 다시 짜야 한다. |
| **Cognito** | **Cloudflare Access + 외부 IdP / Auth.js · Lucia · Clerk** | Access는 SaaS·앱 SSO에 강함. 일반 사용자 회원가입·소셜 로그인은 Workers 위에 Auth.js / Lucia / Clerk 같은 라이브러리를 얹는 패턴. |
| **AWS Verified Access** | **Cloudflare Access** | 둘 다 ZTNA. Access는 OIDC/SAML 다양 IdP, 브라우저 기반 SSH/VNC 같은 개발자 친화 기능. |
| **Secrets Manager / Parameter Store** | **Workers Secrets / Secrets Store / `.dev.vars`** | 로컬은 `.dev.vars` (gitignore), 배포 secret은 `wrangler secret put`. 2025년 발표된 Secrets Store는 account-level 중앙 관리. |
| **WAF** | **Cloudflare WAF + Bot Management + Turnstile + API Shield** | 한 단일 제품이 아니라 묶음. Turnstile은 invisible challenge라 일반 사용자에게 CAPTCHA UI 안 보임. |
| **Site-to-Site VPN / PrivateLink** | **Cloudflare Tunnel (cloudflared) / Cloudflare One** | cloudflared는 사설망 안에서 outbound-only tunnel. PrivateLink 같은 cross-VPC private endpoint와는 모델이 다르다. 정확한 1:1은 없다. |

IAM↔(1:1 등가 없음)을 처음 보면 당황스럽다. AWS에서 IAM은 거의 모든 권한 결정의 중심이다. 사용자 권한, 서비스 간 권한, 리소스 단위 권한, 조건부 권한 — 한 정책 언어로 모두 표현된다. Cloudflare에는 그런 단일 정책 언어가 없다. *대신 셋으로 흩어진다.*

첫째, **Worker 간 또는 Worker → 리소스 권한**은 Bindings에 표현된다. `wrangler.toml`에 `[[kv_namespaces]] binding = "SESSIONS"` 같은 줄을 적으면, 그 Worker는 그 KV에 접근할 수 있다. 코드에서 `env.SESSIONS.get(...)`로 호출한다. IAM role + SDK client가 분리되어 있는 AWS 모델과 달리, 권한과 클라이언트가 한 핸들에 합쳐져 있다. 직관적이지만, IAM의 정교한 조건부 권한(예: "이 사용자는 오전 9시~오후 6시에만 이 버킷에 쓸 수 있다")을 표현할 도구가 부족하다. 그런 정교한 룰은 Worker 코드 안에서 직접 짜야 한다. 둘째, **사람·디바이스 액세스**는 Cloudflare Access가 맡는다. SaaS·자체 앱 앞단에 SSO·device posture·OIDC/SAML IdP를 얹는다. AWS Verified Access의 자리다. 셋째, **트래픽 단 권한**은 WAF rule이 맡는다. "이 IP 대역만 접근 허용", "이 User-Agent 차단" 같은 룰이 트래픽이 origin에 닿기 전에 적용된다. 이 셋을 합쳐야 IAM의 자리가 채워진다. *한 단일 제품으로 옮기려는 시도가 실패한다.* 옮기는 게 아니라, 다시 짜는 일이다.

Cognito↔Access + Auth.js·Lucia·Clerk도 매핑이 갈라진다. Cognito는 AWS의 사용자 관리 + 소셜 로그인 + JWT 발급을 한 제품에 묶어둔다. Cloudflare에서는 두 자리로 나뉜다. *enterprise SSO·SaaS 앞단 보호*는 Access가, *일반 사용자 회원가입·소셜 로그인*은 Workers + Auth.js / Lucia / Clerk 조합이 맡는다. Auth.js는 Next.js + OpenNext 환경에서 가장 무난하고, Lucia는 Workers·Edge 친화적인 minimal auth 라이브러리, Clerk은 SaaS형으로 빠르게 도입 가능하지만 사용자 수에 비례한 비용이 든다. *어느 자리에 무엇을 두느냐*가 결정 항목이지, 단일 매핑이 아니다.

Secrets Manager↔Workers Secrets는 매핑이 가장 솔직한 자리다. 로컬에서는 `.dev.vars` 파일에 적고 gitignore한다. 배포 시에는 `wrangler secret put MY_SECRET`로 Cloudflare 쪽에 등록한다. 등록된 값은 대시보드에서도 보이지 않는다. 다중 환경은 `wrangler secret put --env staging`처럼 환경 분리로 관리한다. 2025년 발표된 **Cloudflare Secrets Store**는 account-level 중앙 관리 도구라서, 여러 Worker에서 동일 secret을 참조해야 할 때 자리를 잡는다. AWS Secrets Manager의 *자동 로테이션*은 Workers Secrets에 단일 제품으로 같은 형태가 없다. 로테이션이 핵심 보안 모델이라면 옮기기 전에 한 번 더 점검하자.

WAF↔Cloudflare WAF + Bot Management + Turnstile + API Shield는 한 줄이 한 제품을 가리키지 않는 자리다. Cloudflare 보안 스택은 *상품 묶음*이다. 트래픽 단 룰은 WAF, 봇 탐지·차단은 Bot Management, 사람 검증은 Turnstile, API 스키마 검증·mTLS는 API Shield. 이 넷이 한 무대 위에서 협력한다. **Turnstile**은 흥미로운 자리다. CAPTCHA UI를 일반 사용자에게 보여주지 않는 invisible challenge다. 사용자는 자기가 검증되고 있는지도 모른 채 통과되거나 차단된다. AWS WAF의 reCAPTCHA-style 통합과 다른 사용자 경험을 만든다. 보안 팀과 UX 팀의 사이가 좋아지는 도구다.

Site-to-Site VPN·PrivateLink↔Cloudflare Tunnel은 매핑이 정확하지 않은 자리다. cloudflared는 사설망 안에서 *outbound-only* tunnel을 Cloudflare로 연다. EC2 private subnet 안에 cloudflared를 띄우면, 외부에 그 subnet을 노출하지 않고도 Cloudflare를 거쳐 안전하게 접근할 수 있다. 단방향 outbound라 사설망 자체의 보안 모델이 깨지지 않는다. 다만 *AWS PrivateLink 같은 cross-VPC private endpoint*와는 모델이 다르다. PrivateLink는 양방향 사설 endpoint이고, cloudflared는 outbound-only tunnel이다. PrivateLink 위에 마이크로서비스 메시를 얹어 운영하는 enterprise 시스템을 cloudflared로 통째로 옮기려는 건 무리한 시도다. 11장에서 본격적으로 다룬다.

이 카테고리의 한 줄 요약. *IAM의 자리는 셋으로 흩어지고, Cognito는 둘로 갈라지며, PrivateLink의 자리는 아예 다른 모델이다.* 보안은 매핑이 아니라 다시 짜는 일이다.

### 카테고리 5. 메시징·이벤트 — SQS는 자연스럽고 EventBridge는 어색하다

다섯 번째 카테고리다. 비동기·이벤트·스케줄. 이 자리에서 매핑은 SQS↔Queues가 가장 자연스럽고, EventBridge↔(약함)이 가장 어색하다.

| AWS | Cloudflare | 1:1로 보면 안 되는 이유 |
|---|---|---|
| **SQS** | **Queues** | at-least-once, 메시지 본문 <128KB, 기본 보존 4일, batch·DLQ·retry 지원. Worker consumer는 push 기반. egress 비용 없음. 매핑이 가장 솔직한 자리. |
| **SNS** | **Pub/Sub (베타) / Workers + DO 직접 fan-out** | 1:N pub/sub의 단순한 케이스는 가능하지만, SNS의 다양한 subscriber 타입(SMS·email·SQS·HTTP·Lambda)은 Cloudflare 단일 제품으로 매핑되지 않는다. Workers·DO·Queues 조합으로 직접 짜야 한다. |
| **EventBridge / EventBridge Scheduler** | **Cron Triggers + Workflows / Workers + DO** | EventBridge의 패턴 매칭·rule 기반 sophisticated routing이 약함. Cron Triggers는 단순 cron, Workflows는 durable execution. EventBridge 수준의 통합 ecosystem 부재. |
| **Step Functions** | **Workflows** | (위 컴퓨트 카테고리 재인용) 가격 모델 — state transition vs CPU time — 이 정반대. AWS 200+ 액션 통합 부재. |

SQS↔Queues는 매핑이 가장 솔직한 자리다. 둘 다 at-least-once, batch 소비, 재시도, dead-letter queue 지원. Cloudflare Queues는 메시지 본문 128KB 제한, 기본 보존 4일이다. Worker consumer는 push 기반이라 SQS의 long-polling 패턴 대신 자동으로 호출된다. egress 비용이 없는 것도 큰 차이다. SQS에서 cross-region 메시지를 보내면 그 자체가 비용에 잡히는데, Queues는 그렇지 않다. 매핑이 자연스러운 자리답게 함정도 적다. *옮길 만한 자리에서는 옮기는 게 자연스럽다.*

SNS↔(약함)은 매핑이 어색해진다. SNS는 1:N pub/sub의 강력한 추상이다. Subscriber 타입이 SMS, email, SQS, HTTP, Lambda 등으로 다양하다. Cloudflare에는 SNS에 정확히 매핑되는 단일 제품이 없다. **Pub/Sub**이 베타로 있긴 하지만 2026년 5월 기준 일반 권장 패턴은 아니다. SNS의 자리는 *Workers + Durable Objects + Queues 조합*으로 직접 짠다. 한 fan-out endpoint를 Worker로 두고, subscriber 목록을 DO에 보관하고, 각 subscriber에 비동기로 메시지를 보내는 패턴이다. 일이 코드 쪽으로 옮겨오는 셈이다. 단순 fan-out에는 충분하지만, *SNS의 풍부한 통합 ecosystem*을 그대로 옮기려는 시도는 자연스럽지 않다.

EventBridge·EventBridge Scheduler↔Cron Triggers + Workflows는 매핑이 가장 깨지는 자리 중 하나다. EventBridge는 *패턴 매칭 + rule 기반 라우팅*이 본질이다. "S3 ObjectCreated 이벤트가 들어오면 Lambda A에, 그 중 .pdf인 것만 Lambda B에 보낸다" 같은 sophisticated routing이 한 룰로 표현된다. Cloudflare에는 이 자리에 정확히 매핑되는 단일 제품이 없다. **Cron Triggers**는 단순 cron이다. wrangler.toml에 `crons = ["0 * * * *"]`처럼 적으면 매시 정각에 Worker가 호출된다. Spring `@Scheduled`의 자리에 자연스럽다. **Workflows**는 durable execution이다. Step Functions의 자리에 자연스럽다. 둘 다 EventBridge가 아니다. EventBridge의 *event bus + rule 기반 fan-out*이 필요하다면, Workers + DO + Queues로 직접 짜거나, 그 부분만 AWS에 남기는 하이브리드가 정직한 길이다. *옮길 수 있는 자리만 옮기자.*

Step Functions↔Workflows는 위에서 이미 다뤘지만 한 번 더 짚는다. 가격 모델 차이가 결정적이다. Step Functions는 state transition 단위 과금이라 long-poll·승인 대기·trial 만료 같은 *대기 위주 워크플로*에서 비용이 누적된다. Workflows는 CPU time × 요청 수만 과금하고 sleep·외부 대기는 0이다. 30일 trial 만료 알림 같은 워크플로를 Workflows로 짜면 그 30일은 *공짜로 기다린다.* 반대로 Step Functions의 200+ AWS 서비스 통합 — IAM, S3, SNS, EventBridge에 한 줄짜리 task로 연결되는 것들 — 은 Workflows에 같은 형태로 없다. Workflows는 코드(`step.do(...)`, `step.sleep(...)`)로 짠다. 통합 ecosystem이 풍부한 Step Functions 자산을 그대로 옮기는 건 단순한 일이 아니다.

이 카테고리의 한 줄 요약. *SQS는 옮기고, SNS·EventBridge의 자리는 직접 짜거나 AWS에 남긴다.* 비동기 영역은 매핑이 갈라지는 정도가 가장 큰 자리다.

### 카테고리 6. AI — Bedrock과 Workers AI는 같은 자리가 아니다

마지막 카테고리. AI다. 이 자리에서 흥미로운 매핑은 셋이다. Bedrock↔Workers AI, OpenSearch k-NN·pgvector↔Vectorize, 그리고 **AWS 등가물이 없는 AI Gateway**.

| AWS | Cloudflare | 1:1로 보면 안 되는 이유 |
|---|---|---|
| **Bedrock** | **Workers AI** | Workers AI는 Cloudflare GPU 인프라 위 edge inference, Neuron 단위 과금. Bedrock은 region 내 inference, 모델 카탈로그·enterprise feature 풍부. *latency-critical edge*는 Workers AI, *VPC 격리·Knowledge Bases·enterprise*는 Bedrock. 한 자리에 가두지 말자. |
| **OpenSearch k-NN / pgvector** | **Vectorize** | 글로벌 분산, 인덱스당 5M vector. **hybrid search 미지원**(2026 기준). 큰 규모·hybrid search는 OpenSearch 유지. pgvector를 쓰는 자리라면 Hyperdrive로 그대로 살리는 길도 있다. |
| **(AWS 등가물 없음)** | **AI Gateway** | 70+ 모델 / 12+ provider 단일 endpoint, 캐싱(최대 90% 지연 감소), rate limit, retries, model fallback, 비용·토큰 분석. AWS에는 정확한 단일 등가물이 없다 — *자체 구축이 일반적*. |

Bedrock↔Workers AI는 매핑이 한 줄로는 가둬지지 않는 자리다. 둘 다 LLM inference 서비스라는 표면은 닮았지만, *어디서 도는가*가 정반대다. Workers AI는 Cloudflare의 GPU 인프라 위에서 edge inference를 한다. 사용자에게 가까운 PoP에서 모델이 응답한다. Llama 3.1, Stable Diffusion XL 같은 카탈로그 모델을 빠르게 호출할 수 있고, Neuron 단위로 과금된다($0.011 / 1k Neurons + 일 10k Neurons 무료). Bedrock은 region 안에서 inference를 한다. 모델 카탈로그가 풍부하고(Anthropic, Cohere, Mistral, Titan), enterprise 기능(VPC endpoint, Model evaluation, Knowledge Bases)이 두텁다. *latency-critical edge 호출이라면 Workers AI*, *VPC 격리·Knowledge Bases·enterprise feature가 핵심이라면 Bedrock*. 한 자리에 가둘 수 없는 매핑이다. 12장에서 본격적으로 다룬다.

OpenSearch k-NN·pgvector↔Vectorize는 위 카테고리 2에서 한 번 다뤘다. 다시 강조하면, **2026년 5월 기준 hybrid search 미지원**이 결정적 한계다. RAG 챗봇에서 키워드 + 의미 검색을 함께 돌리는 패턴이 표준이라면, Vectorize 단독으로는 부족하다. OpenSearch를 그대로 두거나, pgvector + Hyperdrive로 Postgres 안에서 벡터 검색을 살리는 길이 있다. *지금 옮기지 말자, hybrid search가 들어온 다음에 다시 보자.*

AI Gateway는 매핑 표에서 가장 흥미로운 자리다. **AWS에 정확한 등가물이 없다.** AI Gateway는 70+ 모델 / 12+ provider를 단일 endpoint로 묶고, 캐싱(동일 요청 글로벌 캐시 → 최대 90% 지연 감소), rate limit, retries, model fallback, 비용·토큰 분석을 한 제품으로 제공한다. AWS에서 같은 일을 하려면 자체 게이트웨이를 짜거나, Portkey 같은 3rd party를 붙이거나, Bedrock 앞에 직접 프록시를 두어야 한다. *자체 구축이 일반적*이다. 그래서 AWS 시스템에서 가장 risk-low하게 Cloudflare를 끼워 넣는 자리 중 하나가 정확히 이 AI Gateway다. **Bedrock 모델은 그대로 두고, AI Gateway만 앞단에 두는 패턴**이 가능하다. 모델 호출은 AWS에서 그대로 끝나지만, 캐싱·관측·비용 분석은 Cloudflare 쪽에서 무료 또는 저렴하게 얻는다. 14장 8단계 마이그레이션 시퀀스의 마지막 단계가 정확히 이 모양이다.

이 카테고리의 한 줄 요약. *Bedrock과 Workers AI는 한 자리가 아니고, Vectorize는 hybrid search가 들어온 다음 보고, AI Gateway는 AWS에 등가물이 없으니 가장 자연스러운 첫 진입점이다.* AI 영역은 매핑이 가장 빠르게 변하는 자리이기도 하다. 부록 E에 추적 가이드를 두었다.

### 1:1 표가 거짓말이 되는 5가지 패턴

여섯 카테고리를 다 펼쳐 본 뒤, 한 발 물러나서 패턴을 보자. 매핑 표가 거짓말이 되는 자리는 다섯 가지 패턴으로 정리된다. 자기 시스템에 매핑을 적용할 때, 이 다섯 패턴을 점검표처럼 써보자.

**패턴 1. 한 이름이 셋으로 갈라진다.** 가장 위험한 패턴이다. DynamoDB가 KV·D1·DO 셋으로 갈라지는 자리. 한 줄 매핑은 셋 중 하나를 임의로 선택해서 표에 박아 넣는다. 자기 워크로드의 사용 패턴이 그 선택과 맞지 않으면 6개월 뒤 회귀 사례가 된다. *사용 패턴별로 갈라서 보자.*

**패턴 2. 같은 단어, 다른 모델.** Lambda↔Workers, Step Functions↔Workflows에서 일어난다. "둘 다 서버리스", "둘 다 orchestration" 같은 단어로 묶이지만 격리 모델·가격 모델·실행 모델이 정반대다. Lambda 컨테이너 모델로 Workers를 이해하려는 시도가 깨지는 자리이고, Step Functions ASL을 Workflows로 그대로 옮기려는 시도가 무거워지는 자리다. *단어가 아니라 모델을 보자.*

**패턴 3. 옮기지 않고 그대로 살리는 길이 있다.** RDS·Aurora↔Hyperdrive가 정확히 이 패턴이다. D1으로 옮기는 게 매핑 표의 답처럼 보이지만, 실제로는 RDS를 그대로 두고 Hyperdrive를 앞단에 두는 게 가장 risk-low한 길이다. *옮기는 것만 답이 아니다, 그대로 살리는 길도 답이다.* 14장 마이그레이션 시퀀스의 핵심 멘탈이기도 하다.

**패턴 4. AWS에 한 단일 등가물이 있고, Cloudflare에는 셋으로 흩어진다.** IAM이 그렇다. Bindings + Access + WAF rule 셋의 조합으로 다시 짜야 한다. CloudWatch도 비슷하다. AWS에서는 한 단일 제품인데, Cloudflare에서는 Workers Logs + Workers Analytics + Logpush + 외부 APM 조합이 표준이다. *한 제품을 찾지 말고, 조합을 보자.*

**패턴 5. AWS 리전 모델 vs Cloudflare 글로벌 모델.** 이건 가장 깊은 자리에서 일어나는 매핑 거짓말이다. ALB의 자리가 사라지고, "어느 리전에 살까"의 결정이 사라지고, "데이터 jurisdiction은 어디인가"가 새로 등장한다. AWS 리전 모델 위에 익숙해진 멘탈을 글로벌 모델로 바꾸는 일이라, 매핑 표 한 줄로는 표현되지 않는다. 1장과 2장에서 이 차이를 다뤘다.

이 다섯 패턴 중 하나라도 자기 매핑에 걸린다면, *멈춰서 한 번 더 보자.* 한 줄 매핑이 답을 가리키는 게 아니라, 답을 가리고 있는 신호다.

### "1:1 표가 거짓말이 되는 자리" — 매핑 카탈로그의 한계

이 장의 마지막은 정직한 한계로 닫자. 매핑 카탈로그를 펼친 뒤에도 표가 답하지 못하는 자리가 셋 있다.

첫째, **빠르게 변하는 영역**이다. Cloudflare는 분기마다 제품이 추가·변경된다. 2025년 4월에 Pages가 maintenance 모드로 들어가고 Workers Static Assets가 본체가 되었다. 2025년 11월에 Workflows가 GA되었다. 2026년 4월에 Dynamic Workers가 open beta에 들어갔다. Vectorize의 hybrid search 지원, Workers Containers의 GPU·대용량 RAM, Vinext의 안정화 — 이런 영역은 책 출간 후 6개월 안에 바뀔 가능성이 높다. *분기마다 공식 페이지를 다시 보자.* 부록 E에 추적 가이드를 두었다.

둘째, **enterprise 기능 부재**다. AWS의 enterprise 기능 — Glacier·Object Lock·VPC PrivateLink·정교한 IAM policy 언어·복잡한 Route 53 라우팅·Step Functions의 200+ 통합 — 의 일부는 Cloudflare에 같은 형태로 없다. enterprise 컴플라이언스가 강하게 요구되는 워크로드라면, 매핑 표가 답을 가리고 있을 수 있다.

셋째, **일부 SDK 호환성 한계**다. R2는 S3 호환 API라고 하지만 100% 호환은 아니다. Lifecycle policy·Object Lock 같은 기능이 일부 부재하다. AWS SDK의 모든 메서드가 그대로 동작하는 건 아니다. 옮기기 전에 *자기 코드가 실제로 사용하는 메서드 목록*을 확인하는 게 정직한 절차다. 책 한 권으로 모든 SDK 호환성을 확인할 수 없다. 자기 시스템의 코드 베이스 위에서 한 번 점검하자.

매핑 카탈로그는 *지도*이지 *결정*이 아니다. 지도를 본 뒤 어디로 갈지를 정하는 일은 자기 시스템 위에서 자기 손으로 해야 한다. 그 결정 도구가 다음 장에 있다.

### 마무리

자, 매핑 카탈로그를 한 번 펼쳐 봤다. 컴퓨트·스토리지·네트워크·보안·메시징·AI 여섯 카테고리에서 1:1 매핑이 거짓말이 되는 다섯 가지 패턴을 보았다. 한 이름이 셋으로 갈라지는 자리, 같은 단어 아래 다른 모델이 있는 자리, 옮기지 않고 그대로 살리는 길이 있는 자리, 한 단일 등가물이 셋으로 흩어지는 자리, 리전 모델과 글로벌 모델이 부딪히는 자리. 이 다섯을 머릿속에 두고 자기 시스템 위에 매핑을 그리면, 6개월 뒤 회귀 사례가 되는 길을 적어도 한 번은 미리 피할 수 있다.

그런데 매핑 표를 다 본 뒤에 가장 먼저 드는 감정은 시원함이 아니라 막막함이다. *그래서 내 워크로드 중 무엇을 옮길 것인가?* 매핑은 길을 가리켜 주지만 어디로 갈지를 정해주지는 않는다. 옮길 자리와 남길 자리를 구분하는 결정 프레임이 없는 채로 매핑만 들고 뛰어들면, 거의 반드시 한 축에서 빨간불이 켜진 워크로드를 옮기려고 코드를 비비 꼬게 된다.

다음 장에서는 그 결정 프레임을 손에 쥔다. **5축 결정 트리, 자가 진단 18문항, 9패턴 워크로드 결정 매트릭스, 의사결정 워크시트**. 자기 시스템의 컴포넌트 8~12개를 표 한 장에 채워 넣어 "Move now / Move later / 보류 / Don't move"로 분류하는 도구다. 매핑 카탈로그가 *지도*라면, 5장의 결정 프레임은 *나침반*이다. 둘이 한 쌍이다.

기억해두자. **1:1 매핑 표는 친절한 척하는 함정이다.** 표 한 줄 한 줄 끝에 "1:1로 보면 안 되는 이유"가 함께 적혀 있을 때만 정직한 지도가 된다. 그 지도를 들고 함께 다음 장으로 넘어가 보자.

---


## 5장. 옮길까 말까 — Cloudflare로 가야 할 워크로드 판별법

월요일 오전, 팀 회의실에 모여 있다고 해보자. 누군가가 화이트보드 앞에 서서 묻는다. "그래서, 우리 시스템에서 Cloudflare로 옮겨야 할 게 뭐죠?" 4장에서 우리는 AWS의 모든 서비스가 Cloudflare 어느 자리에 어떻게 매핑되는지 카탈로그를 손에 쥐었다. 그런데 그 표를 다 본 직후 가장 먼저 드는 감정은 무엇인가. 시원함이 아니라 막막함이다. 매핑은 알겠는데, 정작 "내 워크로드 중 무엇을" 옮길 것인가는 표가 답해주지 않는다.

매핑 표는 지도다. 지도는 길을 가리켜 주지만 어디로 갈지를 정해주지는 않는다. 옮겨야 할 워크로드와 옮기면 안 되는 워크로드를 구분하지 못한 채 카탈로그만 보고 의사결정을 시작하면, 6개월 뒤에 우리는 KV에 secondary index를 흉내내려고 코드를 비비 꼬고 있거나, 30초짜리 PDF 생성 batch가 Workers CPU time 한도에 걸려서 매주 슬랙 알림을 받고 있을 것이다. 둘 다 끔찍한 일이다. 옮길 자리와 남길 자리를 구분하는 결정 프레임이 없는 채로 매핑만 들고 뛰어들면 거의 반드시 그렇게 된다.

이 장에서 손에 쥐고 가야 할 것은 한 가지다. 자기 시스템 위에 들고 가서 "이건 옮긴다, 이건 남긴다, 이건 나중"으로 한 번 분류해 주는 결정 프레임. 이 책 전체의 약속 — *Cloudflare를 도입하지 말고, 자기 아키텍처에 올바른 자리를 내주자* — 가 가장 무거워지는 챕터다. 14장에서 "어떻게 옮길 것인가"의 시퀀스를 그릴 텐데, 그 8단계 로드맵은 지금 이 챕터에서 만든 결정 워크시트 위에서만 의미가 있다. 5장은 *무엇을*, 14장은 *어떻게*. 둘은 짝이다.

자, 5축 결정 트리부터 살펴보자.

### 5축 결정 트리 — 한 워크로드를 다섯 번 묻는다

워크로드 하나를 두고 "Cloudflare로 옮길까 말까"를 결정하려면, 다섯 가지 축에서 각각 답을 가져야 한다. 한 축에서 명백한 거부 신호가 나오면 그 워크로드는 거기서 멈춰야 한다. 다섯 축이 모두 초록불일 때만 안전하게 옮길 수 있다.

#### 축 1. 요청 패턴 — spike-y인가 steady인가, 글로벌인가 단일 리전인가

먼저 가장 뚜렷한 축이다. 요청이 어떤 모습으로 들어오는가. 평소엔 잠잠하다가 가끔 폭주하는 spike-y 워크로드인가, 아니면 24시간 거의 일정한 부하의 steady 워크로드인가. 그리고 사용자가 어디에 있는가 — 서울 한 곳에 모여 있는가, 아니면 도쿄·싱가포르·암스테르담·상파울루에 흩어져 있는가.

spike-y + 글로벌이면 Workers의 가격·콜드스타트 모델이 가장 빛난다. 무료 plan에서도 일 10만 요청까지 받을 수 있고, 5ms 미만 콜드스타트 덕에 갑자기 트래픽이 들어와도 첫 요청자가 기다리지 않는다. 한 청원수 사이트가 무료 Workers 한도 안에서 트래픽 스파이크를 받아낸 한국 커뮤니티 사례를 떠올려도 좋다.

steady + 단일 리전이면 이야기가 다르다. 사용자가 한국에만 있고 부하가 일정하다면, 가격 모델 측면에서 Cloudflare가 압도적이지 않다. EC2 reserved instance나 Lambda provisioned concurrency가 더 저렴할 수도 있다. 그렇다면 굳이 옮길 이유가 없다. *지금 잘 돌고 있는 시스템을 옮길 이유가 없다는 결론도 충분히 정직한 답이다.*

#### 축 2. 데이터 일관성 — eventually consistent로 충분한가

두 번째 축. 이 워크로드의 데이터는 얼마나 강한 일관성을 요구하는가. 세 갈래로 나눠보자.

- **eventually consistent로 충분** — 세션 토큰, feature flag, 사용자 설정, 캐시. KV가 빛난다. 60초 정도 늦게 전파돼도 사용자가 눈치채지 못하는 데이터.
- **strong consistency 필요** — 사용자 프로필, 주문 내역, 게시물. D1 또는 Hyperdrive 너머의 Postgres가 자리를 잡는다.
- **transactional 일관성 필요** — 재고 차감, 좌석 예약, 게임 턴, 채팅방 메시지 순서. Durable Objects의 자리. actor 모델로 한 인스턴스가 직렬화된 처리를 보장.

여기서 중요한 함정 하나. DynamoDB를 쓰던 워크로드를 한 줄에 KV로 매핑하면 거의 반드시 사고가 난다. DynamoDB에는 secondary index가 있고 GSI로 다른 키 조합으로 조회할 수 있는데, KV는 단일 키 lookup만 된다. 검색·정렬·범위 쿼리가 필요한 순간 KV는 거기서 무너진다. 4장의 매핑 표가 "DynamoDB ↔ KV/D1/DO 중 선택"이라고 갈라 놨던 이유가 이것이다. *DynamoDB 한 줄 매핑은 거짓말이다.* 일관성 축에서 한 번 더 검증해야 한다.

#### 축 3. 글로벌성 — 사용자 지리·지연 SLO·데이터 jurisdiction

세 번째 축은 위치의 정치학이다. 사용자가 어디에 있고, 지연 SLO가 얼마이며, 데이터를 어느 관할에 두어야 하는가.

해외 사용자 비중이 높은데 p95 응답이 800ms를 넘는다면, edge로 옮길 동기가 분명하다. CloudFront + Lambda@Edge 조합이 일부 PoP에서 400~600ms 콜드스타트를 보였다는 Rebal AI의 보고를 떠올려 보면, Workers의 글로벌 균일 5ms 콜드스타트는 명백한 무기다.

반대로, 한국 데이터 주권을 강하게 요구하는 워크로드 — KISA 가이드를 따라야 하는 금융·의료 데이터 — 라면 Cloudflare의 글로벌 분산 자체가 컴플라이언스 위반이 될 수 있다. EU jurisdiction이나 D1 location hint로 일부 제어가 가능하지만, "한국 데이터는 한국 리전 안에서만"을 법적으로 증명해야 한다면 D1·KV의 글로벌 분산 모델은 맞지 않는다. *남기는 게 정답이다.*

#### 축 4. 패키지·런타임 의존 — V8 isolate 안에서 살아남을 수 있는가

네 번째 축이 가장 기술적이고 가장 거짓말 안 한다. 이 코드가 V8 isolate 안에서 도는가, 도는 척만 하는가. 2장에서 살펴봤듯 Workers는 V8 isolate 위에서 돌고, 그래서 빠르고 그래서 제약된다. 다음 항목 중 하나라도 깊이 의존한다면, 옮기는 건 잠시 미루는 편이 낫다.

- 임의 바이너리 실행 (FFmpeg을 직접 spawn해서 영상 처리)
- full Node.js API (특히 fs, child_process, worker_threads)
- OS syscall 의존 (로컬 디스크 캐시, /tmp에 큰 파일 쓰기)
- 무거운 JVM 라이브러리 (Spring Boot 전체 컨텍스트, Hibernate JPA, Spring Batch)
- 30초+ 장기 동기 batch (Workers CPU time 한도와 별개로 architecturally 잘못된 모양)
- 1MB(Free)·10MB(Paid) 스크립트 크기를 넘기는 의존성 (Prisma engine, Sharp, headless Chrome)

Liftosaur가 Workers를 떠나 Lambda로 회귀한 이유 중 하나가 정확히 이것이었다. 이미지 처리에 필요한 Node 라이브러리가 Workers에서 동작하지 않았고, 1MB 스크립트 한도에 걸려 의존성을 넣을 수가 없었다. Lambda layers로 의존성을 분리할 수 있는 Lambda와는 모델 자체가 다르다. *솔직한 사례를 뒤에서 더 자세히 보자.*

#### 축 5. 컴플라이언스·격리 — VPC·PrivateLink·강한 region lock

마지막 축. 네트워크 격리·컴플라이언스 요구가 얼마나 강한가. 다음과 같은 조건이 있다면 Cloudflare가 답이 아닐 가능성이 높다.

- 시스템이 VPC 안에서만 동작해야 하고 외부에 노출 자체가 금지된다.
- AWS PrivateLink로 cross-VPC private endpoint를 사용 중이고, 그게 핵심 보안 모델이다.
- HIPAA·PCI-DSS·KISA 가이드 같은 규제로 단일 region 안에서만 데이터·연산이 일어나야 한다.
- 정교한 IAM policy로 리소스별 권한을 행 단위로 제어하고 있고, 이걸 Bindings + Access policy 조합으로 다시 짜는 게 위험 부담이 너무 크다.

물론 Cloudflare One·Tunnel·Access 스택으로 ZTNA 모델은 다시 짤 수 있다. 11장에서 본격적으로 다룬다. 다만 *완전 격리된 사설망 위에서만 도는 시스템*을 굳이 Cloudflare로 끌어내야 할 이유는 보통 없다. 11장 cloudflared로 일부만 외부 접근 가능하게 만드는 패턴 정도면 충분하다.

자, 5축이 끝났다. 다섯 축에서 모두 초록불이 켜진 워크로드가 옮길 만한 후보다. 한 축이라도 빨간불이면 멈춰서 한 번 더 생각하자.

### 절대 옮기면 안 되는 워크로드

5축으로 충분히 거를 수 있지만, 명시적으로 못 박아 두는 편이 낫다. 다음 워크로드는 2026년 5월 시점 Cloudflare 플랫폼으로 옮기지 말자. 옮기는 순간 거의 반드시 후회한다.

**1. 대용량 GPU 추론 워크로드.** Workers AI에 올라와 있는 모델(Llama 3.1, Stable Diffusion XL 등) 외에는 GPU 추론을 직접 돌릴 수 없다. fine-tuned 모델·custom model을 GPU로 돌려야 한다면 Bedrock·SageMaker·자체 EC2 G/P 인스턴스가 자리를 지킨다.

**2. JVM 무거운 라이브러리 의존 코드.** Spring Boot 전체 컨텍스트를 띄워야 하는 모놀리스, Hibernate + JPA + Spring Batch가 핵심인 도메인 코드는 옮기지 말자. Spring Boot 4 + GraalVM native image + Workers Containers 조합이 미래에 가능해질지 모르지만, 2026년 5월 기준 실무 사례가 미디엄 글 한 편 수준이다. 책 집필 시점에는 *권장 패턴이라고 단언하기 어렵다.*

**3. 강한 region lock 워크로드.** 한국 데이터는 한국에만, 유럽 데이터는 유럽에만 — 법적·정책적으로 강제되는 시스템. D1 location hint가 일부 도움을 주지만, 글로벌 PoP에 코드가 동시에 떠 있는 모델 자체가 region lock 가정과 충돌한다.

**4. OS syscall에 깊이 의존하는 워크로드.** FFmpeg·ImageMagick·headless Chrome을 직접 호출하는 미디어 처리, /tmp에 임시 파일을 쓰면서 stream 처리하는 batch, 로컬 SQLite를 디스크에 두고 쓰는 코드. Workers 안에서는 이 가정이 모두 깨진다.

**5. 30초+ 장기 동기 batch.** 보고서 생성, 대용량 ETL, 전체 데이터 reprocess. Workers의 CPU time 한도(기본 30초, plan에 따라 더 유연)와 별개로, *architecturally* 잘못된 자리다. 이런 작업은 ECS/Fargate batch task나 Step Functions·Workflows의 step으로 쪼개야 한다.

**6. 복잡한 PrivateLink·VPC peering 위주 워크로드.** AWS 내부 사설망 안에서 마이크로서비스끼리 PrivateLink로 통신하는 구조. cross-VPC 격리·service mesh가 핵심 보안 모델이라면, 그 자리를 Cloudflare가 부드럽게 차지하지 못한다.

이 여섯 가지를 만난다면 *옮기지 말자.* 14장에서 다시 강조하지만, 책의 핵심 약속은 "올바른 자리를 내준다"이지 "전부 옮긴다"가 아니다. 옮기지 않는 결정도 정직한 결정이다.

### 자가 진단 체크리스트

5축 결정 트리를 받았으니, 이제 자기 시스템에 직접 들고 가서 점수를 매겨보자. 각 항목에 Yes/No로 답한다. Yes 하나당 점수를 더하거나 빼면, "Move now / Move later / Don't move" 세 갈래 결과가 나온다.

다음은 18개 항목 — 5축을 자기 워크로드 위에 풀어 놓은 형태다.

**요청 패턴 (3문항, 각 +2점)**
1. 현재 Lambda 평균 콜드스타트가 200ms 이상인가?
2. 해외 사용자(아시아·미주·유럽)가 전체 트래픽의 30% 이상인가?
3. 일일 트래픽이 spike-y한 편인가 (peak/avg 비율 5배 이상)?

**비용 (3문항, 각 +2점)**
4. egress 비용이 월 청구의 30% 이상인가?
5. CloudFront + Lambda@Edge에서 PoP 캐시 hit율이 50% 미만인가?
6. CloudWatch + X-Ray 비용이 월 $500을 넘는가?

**일관성 (3문항)**
7. 이 워크로드의 핵심 데이터에 secondary index 또는 range query가 필요한가? (Yes면 -3점, KV는 답이 아니므로)
8. 트랜잭션 격리 수준이 serializable이어야 하는 시나리오가 있는가? (Yes면 +1점, DO 후보)
9. 사용자 세션·feature flag·설정값처럼 eventually consistent로 충분한 데이터가 있는가? (Yes면 +1점, KV 후보)

**런타임 의존 (4문항)**
10. 핵심 코드가 임의 바이너리(FFmpeg·ImageMagick 등)를 spawn하는가? (Yes면 -3점)
11. Node.js의 fs·child_process·worker_threads에 깊이 의존하는가? (Yes면 -3점)
12. JVM 위 Spring Boot 전체 컨텍스트가 한 함수 단위로 떠야 하는가? (Yes면 -3점)
13. 의존성 패키지 합산 크기가 10MB를 넘는가? (Yes면 -2점)

**컴플라이언스·격리 (3문항)**
14. KISA 가이드·HIPAA·PCI 같은 규제로 데이터 region이 강제되는가? (Yes면 -3점)
15. AWS PrivateLink·VPC peering이 핵심 보안 모델인가? (Yes면 -2점)
16. IAM policy로 리소스별 권한을 정교하게 관리하고 있고, 그게 핵심 운영 모델인가? (Yes면 -1점)

**운영 부담 (2문항)**
17. SAM/CDK·CloudFormation 운영에 매주 1시간 이상 쓰고 있는가? (Yes면 +1점)
18. DDoS·WAF 청구서 폭탄을 한 번이라도 경험했거나 두려워하는가? (Yes면 +1점)

총점을 계산해보자.

- **+10점 이상** → Move now. 5축 다 통과한 셈, 옮길 동기와 적합도 모두 높다.
- **+3 ~ +9점** → Move later. 옮길 만한 자리지만, 보강이 필요한 항목(예: 일부 의존성 분리)이 있다. 14장 8단계 시퀀스 중 risk-low 단계부터 점진적으로.
- **-3 ~ +2점** → 보류. 현재 시스템과 Cloudflare 적합도 사이가 모호하다. 한 워크로드를 더 잘게 쪼개서 다시 점수 매겨보자. 일부만 옮길 수 있을지도 모른다.
- **-3점 이하** → Don't move. 위에서 본 "절대 옮기면 안 되는 워크로드"에 한 발 걸친 상태. 무리해서 옮기면 6개월 뒤 회귀 사례가 된다.

이 체크리스트는 부록 C의 비용 시뮬레이션과 짝이다. 점수가 +10이 나왔어도 비용 시뮬레이션에서 절감액이 미미하면 시급도가 낮은 것이고, 반대로 점수가 +5밖에 안 나왔어도 egress가 월 청구의 절반을 차지하는 R2 후보 버킷이 있다면 그것 한 항목만 분리해서 먼저 옮길 수 있다.

### 9패턴 워크로드 결정 매트릭스

체크리스트로 한 워크로드를 점수 내봤다면, 이번엔 워크로드 *유형*별로 미리 정해진 권장 행동을 매트릭스로 보자. 자기 시스템 안에 다음 9패턴이 어떻게 분포돼 있는지 확인하면, 어디부터 손댈지 한눈에 정리된다.

| 패턴 | 권장 행동 | 자리 잡는 Cloudflare 제품 |
|---|---|---|
| **정적 자산 (CSS·JS·이미지)** | Move now | R2 + Cloudflare CDN, 또는 Workers Static Assets |
| **API gateway 앞단** | Move now | Workers Routes + Hono (4·6장) |
| **read-heavy 캐시 / 세션** | Move now | KV (7장 본격) |
| **사용자 facing CRUD API** | Move later | Workers + D1/Drizzle 또는 Hyperdrive (7·10장) |
| **write-heavy DB (2k+ TPS)** | Don't move | RDS·Aurora 유지 + Hyperdrive 앞단 (10장) |
| **long-running orchestration** | Move now (조각 단위) | Workflows로 step 분리 (12장) |
| **WebSocket 채팅·실시간 협업** | Move now | Durable Objects + WebSocket Hibernation (8장) |
| **미디어 storage (egress 큰 버킷)** | Move now | R2 (egress free, 8장) |
| **인증 게이트웨이 / 어드민 노출** | Move now | Cloudflare Access + Tunnel (11장) |

이 표는 본문 14장 8단계 시퀀스의 압축판이기도 하다. 위에서 아래로 읽으면, *risk-low → risk-mid* 순서다. 정적 자산·API 앞단·세션 KV는 거의 무위험으로 옮길 수 있고, 사용자 CRUD는 D1/Hyperdrive 선택 결단이 필요하며, write-heavy DB는 옮기지 말고 Hyperdrive 앞에만 두자.

한 가지 주의. 매트릭스는 *기본값*이지 *법칙*이 아니다. 자기 시스템의 비즈니스 제약 — 예를 들어 "어드민은 한국에서만 접근"이나 "결제는 PG사 지정 region 통해서만" — 이 우선한다. 표는 기본값을 빨리 채우는 도구로만 쓰자.

### 의사결정 워크시트 — toby-shop을 예로

이제 종이를 한 장 꺼내 보자. 이 책의 누적 실습 프로젝트 `toby-shop`(작은 e-commerce SaaS)에 결정 워크시트를 적용해 보자. 부록 C의 빈 양식을 자기 시스템에 옮기기 전에, `toby-shop`을 가지고 한 번 호흡을 맞춰 보는 것이다.

`toby-shop`의 가상 컴포넌트 8개를 가져와 보자.

| # | 컴포넌트 | 5축 요약 | 점수 | 결정 |
|---|---|---|---|---|
| 1 | 상품 카탈로그 정적 페이지 (이미지·CSS·JS) | spike-y, 글로벌, eventually consistent OK, 의존성 가벼움 | +9 | **Move now** → Workers Static Assets + R2 |
| 2 | 상품 검색 API (read-heavy, 캐시 가능) | spike-y, 글로벌, eventually OK, secondary index 불필요 | +8 | **Move now** → Workers + KV 캐시 |
| 3 | 사용자 세션 (로그인 토큰 저장) | per-key 1 write/s 충분, 글로벌 분산 OK | +7 | **Move now** → KV |
| 4 | 사용자 프로필·주소 CRUD | strong consistency, SQL 쿼리 필요 | +4 | **Move later** → D1 + Drizzle 또는 Hyperdrive |
| 5 | 주문 처리 (재고 차감, 결제 연동) | transactional, 분산 lock 필요, write-heavy 가능 | -1 | **보류** → DO + Hyperdrive 검토 |
| 6 | 결제 후 영수증 발송 (orchestration) | step 단위 분리 가능, 외부 API 대기 큼 | +6 | **Move now** → Workflows |
| 7 | 고객지원 채팅 (WebSocket) | 실시간 + 강한 일관성 + per-room 격리 | +8 | **Move now** → Durable Objects |
| 8 | 월간 매출 보고서 batch (1시간+) | 30초+ 장기 동기, JVM 라이브러리 의존 | -5 | **Don't move** → ECS/Fargate 유지 |

8개 중 5개가 Move now, 1개가 Move later, 1개가 보류, 1개가 Don't move. 이 분포가 현실적이다. *모두 옮기지도 않고, 아무것도 안 옮기지도 않는다.* 하이브리드가 최종 형태일 가능성이 가장 높다는 14장의 메시지를 미리 만나는 셈이다.

자기 시스템에 적용할 때는 이렇게 해보자. 8~12개 핵심 컴포넌트를 골라 표 한 장에 채워 넣는다. 점수는 위 자가 진단 체크리스트로 매긴다. 결정란에 Move now / later / 보류 / Don't move를 적는다. *이 한 장이 14장 마이그레이션 로드맵의 베이스가 된다.* 이 워크시트 없이 14장으로 넘어가면 어디부터 손댈지 알 수 없게 된다.

부록 C에 빈 양식과 "내 워크로드 비용 추정" 칸이 있다. 결정 워크시트와 비용 시뮬레이션 두 장을 같이 채우면, 시급도와 적합도를 동시에 본 그림이 된다. 적합도는 높지만 절감액이 적은 워크로드는 낮은 우선순위. 적합도와 절감액 둘 다 높은 워크로드부터 14장 1단계로 옮긴다.

### 양 끝의 사례 — Baselime와 Liftosaur

결정 프레임을 손에 쥐었으니, 결정의 양쪽 끝에서 어떤 일이 벌어지는지 두 사례를 마주해 보자. *광고가 아니라는 약속*을 위해 둘 다 정직하게 들여다본다.

#### Baselime — 5축 다 초록불이었던 사례

Baselime는 observability 도구를 만드는 작은 팀이었다. 3명·3개월 미만으로 AWS Lambda + ECS 스택을 Workers로 풀 마이그레이션했고, 정규 가격 적용 시 일 비용이 $790에서 $25로 떨어졌다 — 95% 절감. AWS Lambda 비용만 따로 보면 -85%였다.

왜 잘 풀렸을까. Baselime의 워크로드를 5축에 넣어 보면 답이 보인다.

- 요청 패턴 — 글로벌 사용자, spike-y 트래픽 (체크).
- 일관성 — observability 데이터는 eventually consistent로 대부분 충분 (체크).
- 글로벌성 — 사용자 분포가 넓고 지연에 민감 (체크).
- 런타임 — Node 위에서 도는 stateless API. JVM·OS syscall 없음 (체크).
- 컴플라이언스 — VPC 격리 강제 없음, region lock 없음 (체크).

다섯 축이 모두 초록불이었다. *옮기지 않는 게 더 이상한 시스템*이었던 셈이다.

#### Liftosaur — 5축에서 빨간불이 두 개 켜진 사례

반대편에 Liftosaur가 있다. 운동 트래킹 앱을 만드는 1인 개발자가 처음에는 Workers + KV 위에 시스템을 올렸다가, 결국 Lambda + DynamoDB로 회귀한 사례다. 회귀 사유를 5축에 매핑해 보자.

- 일관성 — secondary index가 필요했다. KV는 단일 키 lookup만 된다. *빨간불.*
- 런타임 — 이미지 처리에 필요한 Node 라이브러리가 Workers에서 동작 안 했다. 1MB 스크립트 한도(Liftosaur가 옮긴 시점 기준)에 걸려 의존성을 넣을 수가 없었다. *빨간불.*

5축에서 빨간불이 두 개 켜진 워크로드를 끝까지 옮기려고 하면 코드가 비비 꼬인다. Liftosaur의 회귀는 실패가 아니다 — *정직한 후퇴*다. 5축으로 미리 점수를 매겼다면 처음부터 KV가 답이 아니라는 걸 알았을 것이다. KV 대신 D1로 갔거나, 아니면 처음부터 옮기지 않았거나. 둘 다 합리적이다.

이 두 사례는 결정 프레임의 양쪽 끝을 보여준다. *옮길 만한 워크로드는 5축이 다 초록불이고, 옮기면 안 되는 워크로드는 한두 축이 빨간불이다.* 이 단순한 진실을 무시하면 둘 중 하나가 된다 — Baselime의 95% 절감을 놓치거나, Liftosaur의 6개월 회귀 비용을 떠안거나.

### 결정 프레임의 권장형 적용 — "지금 당장이 아니라"

자, 이 모든 점수와 매트릭스를 손에 쥐었다고 해도 한 가지를 잊지 말자. *결정 프레임은 지시가 아니라 권유다.* 점수가 +10점이라고 해서 다음 주에 옮기지 않으면 안 되는 게 아니다.

오히려 추천하는 흐름은 이렇다. 결정 워크시트로 한 번 분류한다. Move now 항목 중 가장 risk-low한 한 개를 골라 14장 1단계로 옮긴다. 한 달 운영해 본다. 비용·p95·error rate가 예상대로 움직였다면 다음 항목으로. 그렇지 않으면 멈춰서 5축을 다시 점검한다.

너무 빨리 옮기는 것보다 천천히 옮기는 편이 낫다. *Cloudflare를 도입하는 게 목표가 아니라, 자기 아키텍처에 올바른 자리를 내주는 게 목표다.* 한 번에 5개 컴포넌트를 옮기는 팀과, 6개월에 걸쳐 한 개씩 옮기는 팀이 있다면, 후자가 거의 항상 더 안정적인 운영을 만든다. Strangler Fig 패턴의 본질은 "옛 나무를 베지 않고 새 나무가 옛 나무를 감싸 자라게 한다"이다. 14장에서 8단계로 풀어낼 그 패턴의 베이스가 5장의 결정 워크시트다.

다섯 축, 18문항 자가 진단, 9패턴 매트릭스, 결정 워크시트 한 장. 이 네 도구를 들고 자기 시스템 위에 한 번 올려 보자. 한 시간이면 충분하다. 그 한 장이 6장부터 12장까지의 본격 기술 챕터를 *내 시스템에 붙여서 읽게* 만들어 줄 것이다.

### 이 결정 프레임이 무너지는 자리

이 장의 마지막은 정직한 한계로 닫자. 5축 결정 트리는 만능이 아니다. 다음 자리에서는 무너지거나 거짓 안심을 줄 수 있다.

- 비즈니스 제약이 기술 점수보다 우선할 때. 점수가 +12점이어도 "어드민은 한국 EC2에서만 도는 게 정책"이면 옮기지 않는 게 맞다. 5축은 기술 적합도이지 정책 결정이 아니다.
- 트래픽 형상이 6개월 후에 크게 바뀔 가능성이 있을 때. 지금은 단일 region steady지만 곧 글로벌 spike-y가 된다면, 점수가 낮아도 미리 옮길 만한 후보일 수 있다. 미래를 점수에 반영하지 못한다.
- "보류" 결과가 나온 워크로드는 결정 프레임이 답을 회피하는 자리다. 더 잘게 쪼개서 다시 점수 내거나, 5축 외의 추가 정보(예: 팀 역량·운영 경험)를 손에 쥐고 결정해야 한다.
- 점수가 +5점인 워크로드 두 개를 묶어 한 번에 옮기는 게 점수가 +10점인 워크로드 하나를 옮기는 것보다 위험할 수 있다. 점수는 워크로드 *각각*에 대한 신호이지 묶음 마이그레이션 위험을 반영하지 않는다.
- 2025년 outage 같은 단일 벤더 의존 위험은 점수에 거의 반영 안 된다. 13장에서 본격적으로 다루지만, 점수가 +12점이어도 "이 워크로드까지 Cloudflare에 두면 critical path가 단일 벤더에 너무 쏠린다"는 운영적 판단은 별도로 해야 한다.

다음 장에서는 결정 워크시트에서 "Move now"로 표시된 항목들을 본격적으로 옮기기 시작한다. Spring 멘탈을 Hono로 다시 그리는 챕터, Workers 본격 사용법을 살펴보자.

---


## 6장. Workers 본격 사용법 — Spring 멘탈을 Hono로 다시 그리자

처음 Worker를 띄운 다음 날 아침을 떠올려 보자. 3장에서 `wrangler deploy` 한 번에 글로벌 PoP에 코드가 깔리는 순간을 손끝으로 느꼈고, 5장에서 자기 시스템 컴포넌트 8개를 결정 워크시트에 채워 "이건 Move now"라고 표시했다. 그래서 다음 한 시간 안에 그 첫 컴포넌트를 옮기려고 IDE를 연다. 그런데 빈 화면 앞에 앉으면 이상한 일이 생긴다. *분명 익숙한 자리인데 손이 어디로 가야 할지 모르겠다.*

`@RestController`는 어디에 적나. `@Component`로 주입하던 `UserService`는 어디에 둬야 하나. `SecurityFilterChain`을 매개로 인증·인가를 한 줄에 그리던 그 익숙한 빈 등록은 누가 대신 해주나. 5축 결정 트리는 손에 쥐었는데, 정작 한 라우트에 인증·로깅·에러 처리·DB 조회를 어떻게 늘어놓을지 빈 `index.ts` 한 장이 답을 안 해준다.

이 장에서 손에 쥐고 가야 할 건 그 빈 화면을 채우는 다섯 도구다. 라우팅, 미들웨어, 의존성 주입, 시크릿·환경 분리, 테스트. Spring 개발자가 이미 갖고 있는 다섯 도구를 Workers + Hono 환경에서 *어떤 모양으로 다시 그릴지* 한 번에 풀어 보자. 단, 한 가지 약속을 먼저 하자 — Spring을 잊으라고 하지 않는다. *익숙한 자리에 다른 도구를 끼워 맞춰 보는 것뿐*이다. JPA의 `@Transactional`이 KV·D1·DO에서 어떻게 다시 짜이는지는 7장으로 미루고, 여기서는 한 Worker 안의 골격을 끝까지 깔아 보자.

자, 첫 도구부터 살펴보자.

### fetch(request, env, ctx) — Workers의 본질 진입점

Workers 코드의 진짜 출발점은 한 함수다. `export default { fetch(request, env, ctx) { ... } }`. 이게 전부다. `request`는 표준 Web `Request`, `env`는 `wrangler.toml`이 주입한 바인딩 객체, `ctx`는 `ctx.waitUntil()`로 응답 후 작업을 등록할 수 있는 컨텍스트다. Spring Boot가 `DispatcherServlet`을 띄우고 그 위에 `@RestController`를 얹는 것과 비교하면, *Workers는 컨테이너 자체가 없다*. 컨테이너 없이 한 함수가 요청을 받아 응답을 만든다. 이게 5ms 콜드스타트의 비밀이다. 띄울 게 없으니 띄우는 시간도 없다.

이 본질을 잊지 말자. 이 책 내내 Hono를 쓸 텐데, Hono는 `fetch(request, env, ctx)` 위에 라우팅·미들웨어 한 겹을 얹은 *얇은 라이브러리*일 뿐이다. Spring처럼 풀스택 프레임워크가 아니다. 모든 게 결국 `fetch` 한 함수로 수렴한다는 사실을 기억해두자. 이상한 동작을 디버깅할 때 이 본질로 한 번 내려가 보면 보통 답이 나온다.

```ts
// 가장 본질적인 형태
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return new Response("hello edge");
  },
};
```

이 위에 라우팅을 얹으면 우리가 손에 익은 모양이 나타난다. 그게 Hono다.

### Hono — Express에 가까운 라우팅 DSL

Hono는 일본 개발자 Yusuke Wada가 만든 작은 웹 프레임워크다. Cloudflare Workers·Bun·Deno·Node 어디서든 도는데, 출발점이 Workers였던 만큼 V8 isolate 환경에서 가장 자연스럽다. Express를 써본 사람이라면 30초 만에 손에 붙는다. 5장 결정 워크시트의 2번 항목 *상품 검색 API* 를 한번 옮겨보자.

```ts
// apps/api/src/index.ts
import { Hono } from "hono";

type Bindings = {
  CACHE: KVNamespace;
  DB: D1Database;
  JWT_SECRET: string;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get("/", (c) => c.text("toby-shop API"));

app.get("/products/:id", async (c) => {
  const id = c.req.param("id");
  // 캐시 먼저
  const cached = await c.env.CACHE.get(`product:${id}`, "json");
  if (cached) return c.json(cached);

  // 캐시 미스 → D1
  const row = await c.env.DB
    .prepare("SELECT * FROM products WHERE id = ?")
    .bind(id)
    .first();
  if (!row) return c.notFound();

  c.executionCtx.waitUntil(
    c.env.CACHE.put(`product:${id}`, JSON.stringify(row), { expirationTtl: 300 })
  );
  return c.json(row);
});

export default app;
```

아주 짧지만 이 안에 6개의 작은 결정이 들어 있다. `Hono<{ Bindings }>`로 타입 파라미터를 넘기면 `c.env.CACHE` 같은 접근에 자동완성이 붙는다. `c.req.param("id")`는 path param. `c.env.CACHE.get(...)`은 KV 호출. `c.executionCtx.waitUntil(...)`은 응답을 보낸 뒤 백그라운드로 캐시 쓰기를 마무리하라는 약속 — Lambda의 `context.callbackWaitsForEmptyEventLoop = false`와 비슷한 의도다. 이 한 화면이 *Hono의 거의 전부*다.

Spring MVC와 한 화면씩 마주 놓아 보자.

```java
// Spring Boot — 같은 기능
@RestController
@RequestMapping("/products")
class ProductController {
    private final ProductRepository repo;
    private final CacheManager cache;

    ProductController(ProductRepository repo, CacheManager cache) {
        this.repo = repo;
        this.cache = cache;
    }

    @GetMapping("/{id}")
    @Cacheable(value = "products", key = "#id")
    public Product get(@PathVariable Long id) {
        return repo.findById(id).orElseThrow();
    }
}
```

같은 일을 Spring은 두 어노테이션(`@GetMapping`, `@Cacheable`)으로, Hono는 미들웨어 체인이나 명시적 KV 호출로 표현한다. 문법의 우열은 아니다. 다만 Hono 쪽은 *마법이 적다.* `@Cacheable`이 어떻게 동작하는지 디버깅하려면 Spring AOP·CGLIB·Caffeine을 쪼개야 하지만, Hono의 `c.env.CACHE.get`은 호출 한 줄이라 추적할 게 없다. Spring 개발자에겐 이게 처음엔 *허전하게* 느껴지고, 한 달쯤 지나면 *솔직하게* 느껴진다. 마법이 줄어든 만큼 책임이 늘어난 것 — 그 트레이드오프를 이 장 끝까지 같이 받아들이자.

#### 타입 안전한 path / query / body

Hono의 좋은 자리 하나는 validator다. `@hono/zod-validator`를 얹으면 query·body가 컴파일 타임에 잡힌다.

```ts
import { z } from "zod";
import { zValidator } from "@hono/zod-validator";

app.post(
  "/products",
  zValidator("json", z.object({
    name: z.string().min(1),
    price: z.number().int().nonnegative(),
  })),
  async (c) => {
    const body = c.req.valid("json"); // 타입이 좁혀진 채로
    const result = await c.env.DB
      .prepare("INSERT INTO products (name, price) VALUES (?, ?)")
      .bind(body.name, body.price)
      .run();
    return c.json({ id: result.meta.last_row_id }, 201);
  },
);
```

Spring의 `@RequestBody @Valid CreateProductDto dto` + `@NotBlank` 어노테이션 묶음과 같은 자리다. Hono의 zValidator 쪽이 *코드로 명시적*인 게 다르다. 어떤 검증이 어떤 라우트에 어떻게 붙었는지 그 자리에 다 적혀 있다. Spring처럼 어노테이션이 자동으로 해석되는 마법은 없지만, 그 자리에 적혀 있다는 명시성이 운영에서 의외로 큰 장점이 된다. *어디서 무엇이 검증되는지 한 화면에서 보인다.*

### 미들웨어 체인 — SecurityFilterChain을 다시 그리자

Spring Boot에서 인증·로깅·CORS·rate limit을 어떻게 묶는가. `SecurityFilterChain` 빈 한 개에 `HttpSecurity` 빌더로 필터를 줄 세우고, `HandlerInterceptor`로 횡단 관심사를 끼워 넣고, `@RestControllerAdvice`로 예외를 한 자리에 모은다. 세 도구가 세 자리에 흩어져 있다. 한 신참이 들어오면 *이게 어디서 어떻게 호출되는지* 추적하는 데 며칠이 걸린다.

Hono의 미들웨어는 한 자리에 줄 세운다. `app.use()` 한 줄로 끝이다. Express를 써본 사람이라면 정확히 그 모양이고, 안 써본 사람이라도 *함수가 함수를 호출한다*는 가장 단순한 흐름이라 한 화면에 다 보인다.

```ts
import { Hono } from "hono";
import { logger } from "hono/logger";
import { cors } from "hono/cors";
import { jwt } from "hono/jwt";
import type { Context, Next } from "hono";

type Bindings = {
  CACHE: KVNamespace;
  DB: D1Database;
  JWT_SECRET: string;
  RATE_LIMIT: KVNamespace;
};
type Variables = { userId: string };

const app = new Hono<{ Bindings: Bindings; Variables: Variables }>();

// 1. 전역: 로깅 + CORS
app.use("*", logger());
app.use("*", cors({ origin: ["https://toby-shop.com"], credentials: true }));

// 2. /api/* 에만: rate limit
app.use("/api/*", async (c, next) => {
  const ip = c.req.header("CF-Connecting-IP") ?? "unknown";
  const key = `rl:${ip}`;
  const count = parseInt((await c.env.RATE_LIMIT.get(key)) ?? "0", 10);
  if (count > 100) return c.json({ error: "rate limited" }, 429);
  c.executionCtx.waitUntil(
    c.env.RATE_LIMIT.put(key, String(count + 1), { expirationTtl: 60 }),
  );
  await next();
});

// 3. /api/admin/* 에만: JWT 검증
app.use("/api/admin/*", async (c, next) => {
  const middleware = jwt({ secret: c.env.JWT_SECRET });
  return middleware(c, next);
});

// 4. /api/admin/* 에만: 인가 (관리자 권한)
app.use("/api/admin/*", async (c, next) => {
  const payload = c.get("jwtPayload") as { role?: string };
  if (payload.role !== "admin") return c.json({ error: "forbidden" }, 403);
  c.set("userId", (payload as { sub: string }).sub);
  await next();
});

// 5. 라우트
app.get("/api/admin/orders", async (c) => {
  const userId = c.get("userId");
  // ... D1 쿼리
  return c.json({ ok: true, by: userId });
});

// 6. 에러 핸들러 — @RestControllerAdvice 자리
app.onError((err, c) => {
  console.error(err);
  return c.json({ error: "internal" }, 500);
});

app.notFound((c) => c.json({ error: "not found" }, 404));

export default app;
```

이 한 파일이 Spring의 `SecurityFilterChain` + `HandlerInterceptor` + `@RestControllerAdvice` + `Filter` 네 자리에 흩어져 있던 모든 횡단 관심사를 *한 자리에 줄 세운 것*이다. 위에서 아래로 읽으면 라이프사이클이 그대로 흐른다. 매칭된 미들웨어들이 순서대로 실행되고, `next()` 호출 후 코드는 응답이 만들어진 뒤에 실행된다 (Express의 onion 모델 그대로). 이게 처음엔 어색하지만, 사흘이면 손에 붙는다.

Spring `HandlerInterceptor`와 짧게 마주 놓아 보자.

```java
// Spring — 인증 인터셉터
@Component
class AuthInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
        String token = req.getHeader("Authorization");
        if (!isValid(token)) {
            res.setStatus(401);
            return false;
        }
        req.setAttribute("userId", parseUser(token));
        return true;
    }
}

// 등록은 별도 자리
@Configuration
class WebConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new AuthInterceptor()).addPathPatterns("/api/admin/**");
    }
}
```

기능은 정확히 같다. 다만 Spring 쪽은 *인터셉터 클래스 한 개 + 등록 클래스 한 개* 두 자리에 흩어진다. Hono는 한 자리. 어느 쪽이 더 좋다 나쁘다가 아니다 — 큰 팀, 다층 권한, 메서드 단위 보안이 필요한 시스템에는 Spring 모델이 더 안전하다. 작은 API, 빠른 추적, 단일 파일 가독성을 원하는 시스템에는 Hono 모델이 더 *솔직하다*. 5장의 결정 프레임을 한 번 더 떠올리자 — 모든 워크로드가 Workers로 옮겨가는 게 아니다. Spring의 `SecurityFilterChain`이 빛나는 어드민·금융 도메인은 Spring에 두고, edge에서 가벼운 게이트웨이만 Workers + Hono로 까는 *하이브리드*가 흔한 답이다.

#### 미들웨어 우선순위 — 위에서 아래로 읽힌다

기억해두자. Hono는 `app.use(path, handler)`를 *등록 순서대로* 실행한다. 그래서 글로벌 로깅·CORS는 가장 위에, 경로별 인증은 그 아래, 라우트 핸들러는 맨 아래에 두는 게 자연스럽다. Spring의 `Filter` order 어노테이션처럼 숫자를 넣어 우선순위를 비틀지 말자. *위에서 아래로 읽히는 코드*가 가장 디버깅하기 쉽다는 사실은 Workers에서도 변함이 없다.

### DI를 다시 그리자 — c.set/c.get과 Bindings, 그리고 정직한 권유

Spring 개발자가 Workers에서 가장 허전해하는 한 자리. *DI 컨테이너가 없다.* `@Component`도, `@Autowired`도, `ApplicationContext`도 없다. 그렇다면 어떻게 의존성을 주입할까. 답은 세 갈래다. *솔직하게 무엇이 권유할 만한지*부터 짚어 보자.

#### 갈래 1. Bindings — 런타임이 주입해주는 의존성

가장 먼저, 그리고 *가장 권유할 만한* 자리. `wrangler.toml`에 적은 KV·D1·R2·Queue·Service binding은 사실상 런타임 DI다. 코드에서 `c.env.DB.prepare(...)`로 쓰는 그 `DB`는 `wrangler.toml`이 주입한 D1 핸들이다. Spring의 `@Autowired DataSource`와 *기능적으로 같은 자리*다.

```toml
# wrangler.toml
[[d1_databases]]
binding = "DB"
database_name = "toby-shop"
database_id = "xxxx"

[[kv_namespaces]]
binding = "CACHE"
id = "yyyy"
```

```ts
// 코드는 그냥 c.env.DB / c.env.CACHE 를 쓰면 된다
app.get("/users/:id", async (c) => {
  const row = await c.env.DB.prepare("SELECT * FROM users WHERE id = ?").bind(c.req.param("id")).first();
  return row ? c.json(row) : c.notFound();
});
```

이 자리는 *권유할 필요도 없다.* Workers에서는 이게 기본이고, `wrangler types`가 자동 생성한 `Env` 인터페이스 덕분에 타입까지 안전하다. 처음엔 이걸 DI로 부르기 어색하지만, 한 번 익숙해지면 Spring의 IoC 컨테이너보다 *오히려 더 명확한 의존성 표현*이라는 의견에 동의하는 자신을 발견하게 된다. 무엇이 어디에 주입되는지 `wrangler.toml` 한 파일에 다 적혀 있다.

#### 갈래 2. c.set / c.get — 요청 단위 컨텍스트 주입

미들웨어 체인 예제에서 이미 본 패턴이다. 인증 미들웨어가 `c.set("userId", ...)`로 값을 꽂으면, 라우트 핸들러가 `c.get("userId")`로 꺼낸다. Spring의 `RequestContextHolder`나 ThreadLocal과 비슷한 자리다. *요청 단위 의존성*을 표현하는 깔끔한 방법이고, Hono의 타입 시스템(`Variables` 제네릭)이 자동완성까지 받쳐준다.

이 자리도 *권유할 만하다.* 다만 한 함정이 있다. `c.set`에 비즈니스 로직을 너무 많이 꽂으면 라우트 핸들러가 어디서 무엇이 들어왔는지 추적하기 어려워진다. Spring의 ThreadLocal 남용과 똑같은 함정이다. *userId·tenantId·tracerId처럼 진짜 횡단적인 값*만 꽂고, 비즈니스 객체는 함수 인자로 명시적으로 넘기는 편이 낫다.

#### 갈래 3. 함수형 DI — 가장 솔직하고 가장 가벼운 패턴

서비스 클래스를 함수로 풀어 헤치고, 의존성을 첫 번째 인자로 명시적으로 받는다. 이게 사실상 *Workers에서 가장 권유할 만한 패턴*이다.

```ts
// packages/shared/src/users.ts
import type { D1Database } from "@cloudflare/workers-types";

export async function getUser(db: D1Database, id: string) {
  return db.prepare("SELECT * FROM users WHERE id = ?").bind(id).first();
}

export async function createUser(db: D1Database, input: { name: string; email: string }) {
  const result = await db
    .prepare("INSERT INTO users (name, email) VALUES (?, ?)")
    .bind(input.name, input.email)
    .run();
  return result.meta.last_row_id;
}
```

```ts
// apps/api/src/routes/users.ts
import { Hono } from "hono";
import { getUser, createUser } from "@toby-shop/shared/users";

const users = new Hono<{ Bindings: Bindings }>();

users.get("/:id", async (c) => {
  const row = await getUser(c.env.DB, c.req.param("id"));
  return row ? c.json(row) : c.notFound();
});

export default users;
```

`UserService` 클래스도, `@Component`도 없다. 그냥 함수 + 명시적 의존성. 테스트 시에는 `getUser(mockDb, "1")`처럼 mock을 그대로 넘기면 된다. Spring 개발자에겐 *너무 단순해 보이는 게 함정*이다. 큰 시스템에서도 정말 이걸로 충분한가 묻고 싶어진다. 솔직히 답하자면, *Workers 한 개에 들어가는 정도의 도메인이라면 충분하다.* Workers는 코드 크기 한도(Free 3MiB / Paid 10MiB)가 있어서 한 Worker에 너무 많은 도메인을 묶을 수 없고, 그래서 *Spring Boot 모놀리스급 복잡도가 한 Worker에 들어올 일 자체가 드물다.* 도메인이 정말 커지면 Worker를 쪼개고 Service Bindings로 잇는다 (다음 챕터들에서 다룬다).

#### 갈래 4. awilix·tsyringe 같은 가벼운 컨테이너 — 권유하지 않는다

awilix, tsyringe, InversifyJS 같은 TypeScript DI 컨테이너를 Workers에 얹으면 어떨까. 가능은 하다. 다만 *권유하지 않는다.* 이유 셋.

첫째, Workers는 한 isolate가 여러 요청을 처리한다. 컨테이너가 글로벌 싱글톤이 되면 한 요청의 의존성 상태가 다음 요청에 새는 함정이 생긴다. Spring처럼 RequestScope·SessionScope·SingletonScope를 분리해주는 인프라가 컨테이너 안에 없다. 직접 깔아야 한다.

둘째, Workers의 코드 크기 한도. awilix만 해도 10~30KB 수준이지만 reflect-metadata + tsyringe 조합은 더 무겁다. 큰 의존성에 비해 얻는 게 함수형 DI보다 분명하지 않다.

셋째, *팀 신참이 입사 첫 주에 코드를 읽을 때*. 함수형 DI는 import 한 줄만 따라가면 끝이지만, 컨테이너 등록은 별도 파일·별도 토큰을 추적해야 한다. Spring에서 이미 익숙하지만, Workers의 작은 도메인에 굳이 그 복잡도를 끌어올 이유가 빈약하다.

그래서 권유: *Bindings + c.set/get + 함수형 DI 셋이면 충분하다.* 이 셋으로 안 풀리는 자리가 생기면 그 자리는 보통 "이 도메인은 한 Worker에 너무 많이 들어왔다"는 신호다. Worker를 쪼개라는 신호로 받아들이자. *DI 컨테이너의 부재가 처음엔 결핍 같다가, 나중엔 안내판처럼 보인다.*

### 환경변수와 시크릿 — `.dev.vars`, `wrangler secret put`, `c.env`

다음으로 Spring의 `application-{profile}.yml` + Spring Cloud Config + AWS Secrets Manager 자리. Workers에서는 세 레이어가 한결 단순해진다.

**로컬 개발용은 `.dev.vars`** — gitignore 필수. `.env`와 동시에 쓰지 말자. `.dev.vars`가 있으면 `wrangler dev`가 그걸 읽고 `.env`는 무시한다.

```bash
# .dev.vars (gitignore 됨)
JWT_SECRET=local-only-do-not-deploy
DATABASE_URL=postgresql://localhost/toby_shop_dev
```

**배포 환경의 시크릿은 `wrangler secret put`** — 대시보드에서 값은 다시 안 보인다.

```bash
$ wrangler secret put JWT_SECRET
? Enter a secret value: ********
✨ Success! Uploaded secret JWT_SECRET

$ wrangler secret put JWT_SECRET --env production
```

**일반 환경변수는 `wrangler.toml`의 `vars`** — 코드 저장소에 그대로 들어가도 안전한 값. 로그 레벨, feature flag, 외부 API URL 같은 비기밀 값.

```toml
[env.production]
vars = { LOG_LEVEL = "info", IMAGE_CDN = "https://images.toby-shop.com" }

[env.staging]
vars = { LOG_LEVEL = "debug", IMAGE_CDN = "https://staging-images.toby-shop.com" }
```

코드에서는 모두 `c.env`로 동일하게 접근한다. 시크릿이든 vars든 `wrangler types`가 만들어 준 `Env` 타입으로 오타가 잡힌다.

```ts
app.get("/protected", (c) => {
  const secret = c.env.JWT_SECRET;       // wrangler secret으로 등록
  const logLevel = c.env.LOG_LEVEL;      // [env.*].vars 로 등록
  // ...
});
```

기억해두자. *`.dev.vars`를 절대 git에 올리지 말자.* 한 번 올라가면 history에서 지우는 데 며칠을 쓴다. `.gitignore`에 `.dev.vars`를 처음 프로젝트 만들 때 적어두는 습관을 들이자.

여러 Worker에서 같은 시크릿을 공유해야 한다면 2025년에 발표된 **Cloudflare Secrets Store**(account-level 중앙 관리)를 쓸 수 있다. 다만 새 프로젝트에서는 우선 `wrangler secret put`으로 시작하고, 시크릿 공유가 정말 늘어나는 시점에 Secrets Store로 옮기자. *지금 당장 권유하기엔 아직 새로운 자리*다.

### wrangler.toml의 `[env.*]` — `application-{profile}.yml`을 다시 그리자

Spring 개발자가 환경 분리에 쓰는 `application-prod.yml` / `application-staging.yml` 자리. Workers에서는 `wrangler.toml`의 `[env.production]` / `[env.staging]` 블록이 그 역할이다.

```toml
name = "toby-shop-api"
main = "src/index.ts"
compatibility_date = "2025-04-01"
compatibility_flags = ["nodejs_compat"]

# 기본(개발) 환경 바인딩
[[kv_namespaces]]
binding = "CACHE"
id = "dev-kv-id"

[[d1_databases]]
binding = "DB"
database_name = "toby-shop-dev"
database_id = "dev-db-id"

# Staging
[env.staging]
name = "toby-shop-api-staging"
vars = { LOG_LEVEL = "debug" }

[[env.staging.kv_namespaces]]
binding = "CACHE"
id = "staging-kv-id"

[[env.staging.d1_databases]]
binding = "DB"
database_name = "toby-shop-staging"
database_id = "staging-db-id"

# Production
[env.production]
name = "toby-shop-api"
vars = { LOG_LEVEL = "info" }

[[env.production.kv_namespaces]]
binding = "CACHE"
id = "prod-kv-id"

[[env.production.d1_databases]]
binding = "DB"
database_name = "toby-shop-prod"
database_id = "prod-db-id"
```

배포는 환경별로 한 명령씩.

```bash
$ wrangler deploy --env staging
$ wrangler deploy --env production

$ wrangler secret put JWT_SECRET --env staging
$ wrangler secret put JWT_SECRET --env production

$ wrangler tail --env production    # 라이브 로그
```

Spring의 `--spring.profiles.active=production` 자리에 `--env production`이 들어선다. 한 가지 다른 점이 있다 — Spring은 한 jar가 profile만 바꿔 여러 환경에 도는데, Workers는 환경별로 *별도 Worker가 배포된다.* `[env.production]` 블록은 사실상 새 Worker(`toby-shop-api-staging`)를 만든다. 같은 코드, 다른 바인딩·다른 시크릿·다른 이름. 처음엔 *이게 환경 분리가 맞나* 싶지만, 환경 사이 간섭이 원천적으로 막힌다는 점에서 *오히려 더 안전한 분리*다.

흔한 함정 하나. preview 환경을 만들고 싶을 때다. PR마다 임시 URL을 띄우려면 `wrangler versions upload --env preview` 같은 패턴을 쓰는데, 이건 14장에서 마이그레이션 시 다시 다룬다. 일단 6장에서는 `staging` / `production` 둘이면 충분하다.

### 테스트 — vitest + miniflare로 단위·통합

Spring의 `@SpringBootTest`는 컨텍스트 전체를 띄워 통합 테스트를 한다. 비싸고 느리지만, 진짜 빈을 그대로 검증할 수 있다는 안정감이 크다. Workers에서는 어떻게 그 안정감을 손에 쥐어야 할까.

답은 두 갈래. *단위 테스트는 vitest 그대로*, *통합 테스트는 `@cloudflare/vitest-pool-workers` 위에서 miniflare가 띄운 가짜 Workers 환경*. miniflare는 workerd(production과 같은 V8 isolate 런타임)를 로컬에서 그대로 실행한다. 즉 production과 같은 환경에서 KV·D1·R2까지 SQLite 시뮬레이션으로 돌릴 수 있다.

설치는 한 번에.

```bash
$ pnpm add -D vitest @cloudflare/vitest-pool-workers
```

```ts
// vitest.config.ts
import { defineWorkersConfig } from "@cloudflare/vitest-pool-workers/config";

export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: "./wrangler.toml" },
      },
    },
  },
});
```

이 위에 통합 테스트 한 토막을 써보자. 5장 워크시트의 2번 항목 *상품 검색 API* 를 검증한다.

```ts
// apps/api/test/products.test.ts
import { env, createExecutionContext, waitOnExecutionContext } from "cloudflare:test";
import { describe, it, expect, beforeEach } from "vitest";
import app from "../src/index";

describe("GET /products/:id", () => {
  beforeEach(async () => {
    // D1 스키마 시드
    await env.DB.exec(`
      CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price INTEGER NOT NULL
      );
    `);
    await env.DB.prepare("DELETE FROM products").run();
    await env.DB.prepare("INSERT INTO products (id, name, price) VALUES (1, 'edge book', 25000)").run();
  });

  it("D1에서 가져온 상품을 반환한다", async () => {
    const ctx = createExecutionContext();
    const res = await app.fetch(new Request("http://x/products/1"), env, ctx);
    await waitOnExecutionContext(ctx);
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ id: 1, name: "edge book", price: 25000 });
  });

  it("두 번째 요청은 KV 캐시에서 응답한다", async () => {
    const ctx = createExecutionContext();
    await app.fetch(new Request("http://x/products/1"), env, ctx);
    await waitOnExecutionContext(ctx); // 캐시 쓰기 완료 대기

    // 캐시 hit 확인
    const cached = await env.CACHE.get("product:1", "json");
    expect(cached).toMatchObject({ id: 1, name: "edge book" });
  });

  it("없는 상품은 404", async () => {
    const ctx = createExecutionContext();
    const res = await app.fetch(new Request("http://x/products/999"), env, ctx);
    await waitOnExecutionContext(ctx);
    expect(res.status).toBe(404);
  });
});
```

이 테스트가 도는 모습은 Spring의 `@SpringBootTest`와 다르고도 같다. *다른 점*은 컨텍스트를 띄우는 비용이 거의 없다는 것 — miniflare가 in-memory로 D1·KV를 돌리니까 한 테스트가 수십 ms 안에 끝난다. *같은 점*은 production과 같은 런타임에서 같은 바인딩으로 돌린다는 것. workerd가 production V8 isolate를 그대로 재현하므로, "테스트는 통과했는데 production에서 깨지는" 흔한 함정이 크게 줄어든다.

순수 함수 테스트는 vitest 기본 모드로 돌리자. miniflare를 띄울 필요가 없다.

```ts
// packages/shared/test/users.test.ts (Workers pool 안 씀)
import { describe, it, expect } from "vitest";
import { getUser } from "../src/users";

describe("getUser", () => {
  it("D1 mock으로 단위 테스트", async () => {
    const mockDb = {
      prepare: () => ({
        bind: () => ({
          first: async () => ({ id: 1, name: "alice" }),
        }),
      }),
    } as unknown as D1Database;

    const user = await getUser(mockDb, "1");
    expect(user).toEqual({ id: 1, name: "alice" });
  });
});
```

함수형 DI 패턴이 여기서 빛난다. mock을 그대로 인자로 넘기면 끝. Spring의 `@MockBean`이 자동으로 빈을 갈아 끼워주는 마법은 없지만, *어떤 mock이 어디 들어갔는지가 한 화면에 보이는 명시성*이 그 자리에 들어선다.

**테스트 권유 지점**: 단위 테스트는 빠른 피드백용으로 매번 돌리고, miniflare 통합 테스트는 PR 단위 CI에서 돌리자. Spring의 `@SpringBootTest`는 한 번 띄울 때 5~30초가 걸려 PR마다 돌리기 부담스럽지만, *miniflare는 cold start가 1초 안*이라 PR마다 마음 편히 돌릴 수 있다. 이게 Workers의 작은 자랑이다.

### 짧은 KV 세션 실습 — 다음 장으로 넘어가기 전에

여기까지 라우팅·미들웨어·DI·시크릿·테스트까지 5도구를 깔았다. 마지막 한 토막으로 KV에 세션을 저장해보고 7장으로 넘기자. 5장 워크시트의 3번 항목 *사용자 세션* 이다.

```ts
// apps/api/src/routes/auth.ts
import { Hono } from "hono";
import { setCookie, getCookie, deleteCookie } from "hono/cookie";

type Bindings = { SESSIONS: KVNamespace; JWT_SECRET: string };
type Variables = { userId: string };

const auth = new Hono<{ Bindings: Bindings; Variables: Variables }>();

auth.post("/login", async (c) => {
  const { email, password } = await c.req.json<{ email: string; password: string }>();
  // 인증 로직 (실제로는 D1 + bcrypt)
  if (email !== "demo@toby-shop.com" || password !== "demo") {
    return c.json({ error: "invalid" }, 401);
  }

  const sessionId = crypto.randomUUID();
  const userId = "user-1";

  // 1시간짜리 세션 — KV의 sweet spot
  await c.env.SESSIONS.put(
    `session:${sessionId}`,
    JSON.stringify({ userId, createdAt: Date.now() }),
    { expirationTtl: 3600 },
  );

  setCookie(c, "session", sessionId, {
    httpOnly: true,
    secure: true,
    sameSite: "Lax",
    maxAge: 3600,
  });

  return c.json({ ok: true });
});

// 인증 미들웨어 — KV에서 세션 조회
auth.use("/me", async (c, next) => {
  const sessionId = getCookie(c, "session");
  if (!sessionId) return c.json({ error: "unauthenticated" }, 401);

  const raw = await c.env.SESSIONS.get(`session:${sessionId}`);
  if (!raw) return c.json({ error: "expired" }, 401);

  const session = JSON.parse(raw) as { userId: string };
  c.set("userId", session.userId);
  await next();
});

auth.get("/me", (c) => c.json({ userId: c.get("userId") }));

auth.post("/logout", async (c) => {
  const sessionId = getCookie(c, "session");
  if (sessionId) await c.env.SESSIONS.delete(`session:${sessionId}`);
  deleteCookie(c, "session");
  return c.json({ ok: true });
});

export default auth;
```

이게 Spring Security의 `HttpSessionRepository` + `SessionAuthenticationFilter`가 차지하던 자리다. KV는 이런 *eventually consistent + read-heavy + 짧은 TTL* 워크로드의 sweet spot이다. 60초 정도의 전파 지연이 세션에는 문제가 안 된다 — 사용자가 로그인하자마자 다른 PoP로 옮겨가서 세션이 보이지 않을 확률이 그렇게 높지 않고, 보였다 안 보였다 하는 건 1분 안에 수렴한다.

*다만* — 세션 같은 데이터가 *strong consistency*를 요구하는 시스템이라면 KV는 답이 아니다. 여기서 한 박자 멈추자. 다음 장 7장에서 KV의 *무너지는 자리*와 D1의 자리를 본격적으로 다룬다. 일단 6장의 KV 세션은 "워밍업"이라고 이해하자.

### 코드 품질 도구 — 짧게 한 자리

마무리 전에 코드 품질 한 단락. Workers + Hono 프로젝트에 권유할 만한 셋.

- **`wrangler types`** — `worker-configuration.d.ts`를 자동 생성. `Env` 타입과 compat date 기반 runtime types가 들어와서 IDE 자동완성이 산다. `package.json`의 prebuild 스크립트에 `wrangler types`를 걸어두자.
- **Biome 또는 ESLint + Prettier** — Biome이 더 빠르고 설정이 한 파일이지만, 팀에 이미 ESLint config가 있으면 굳이 갈아엎지 말자.
- **TypeScript strict 모드** — `tsconfig.json`에 `"strict": true`. `c.env.DB`의 타입이 strict일 때 더 정확히 좁혀진다.

모노레포 구조는 reference §4.7 그대로 권유한다.

```
apps/
  api/             # Workers + Hono (이번 장의 결과물)
  web/             # Next.js (9장에서 추가)
  worker-jobs/     # Cron + Workflows (12장에서 추가)
packages/
  shared/          # 도메인 함수 (오늘의 함수형 DI 베이스)
  db/              # Drizzle 스키마 (다음 장에서 추가)
```

각 앱마다 `wrangler.toml` 분리, 공통 binding은 같은 namespace 공유. *지금 6장 단계에서는 `apps/api` 한 개와 `packages/shared` 한 개로 시작*하면 충분하다. 다음 장에서 `packages/db`가 들어온다.

### 이 기술이 무너지는 자리

이 장의 마지막은 정직한 한계로 닫자. Hono + Workers가 빛나는 자리가 분명하지만, *무너지는 자리*도 정직하게 적어야 6장이 광고가 아닌 게 된다.

- **거대한 npm 생태계 대비 작은 미들웨어 풀.** Spring Boot의 starter 생태계가 수천 개라면, Hono의 공식·인기 미들웨어는 수십 개 수준이다. JWT·CORS·logger·basic auth·timing·secure-headers 같은 기본은 다 있지만, *Spring Cloud Gateway 같은 깊이 있는 게이트웨이 미들웨어, Resilience4j 수준의 circuit breaker·bulkhead 라이브러리는 부재*하다. 이런 기능이 핵심이면 직접 짜거나 외부 SaaS(예: AI Gateway는 LLM 트래픽 한정)에 맡겨야 한다.
- **AOP 부재.** Spring의 `@Cacheable`·`@Transactional`·`@Retry` 같은 메서드 단위 cross-cutting concern을 미들웨어 레이어로 풀어 놓으면 라우트 단위까지는 깔끔하지만, *서비스 함수 안의 한 메서드만 캐시*하고 싶을 때는 Hono로 표현이 안 된다. 함수 호출 자리에 명시적으로 `withCache(fn)` 같은 wrapper를 끼워야 한다. 처음엔 번거롭지만 한 달 지나면 *명시성이 살아 있는 코드*에 정이 든다.
- **DI 컨테이너의 안전망 부재.** awilix·tsyringe로 풀 수 있지만 위에서 권유하지 않은 이유가 그대로. 의존성 그래프가 100개를 넘는 도메인은 컨테이너의 lifecycle·scope 관리 없이는 직접 짜기 어렵다. 그런 도메인은 *Workers 한 개에 넣지 말자.* 5장 결정 프레임을 다시 펼쳐 — 이 도메인은 Spring 모놀리스에 두는 게 맞을 가능성이 높다.
- **테스트의 상한.** miniflare가 production V8 isolate를 그대로 재현하지만, Cloudflare Network 측 동작(예: 일부 Zone 기능, AI Gateway 일부 동작)은 시뮬레이션 안 된다. `wrangler dev --remote`로 production edge에 띄워 통합 테스트를 한 번 더 돌려야 하는 자리가 있다.
- **에러 추적의 공백.** `app.onError`로 한 자리에 모을 수는 있지만, Spring Boot Actuator + Sentry + Micrometer가 한 묶음으로 주는 metric·trace·log 통합은 아직 부재하다. Sentry는 됐지만 metric·tracing은 외부 APM(Datadog·Baselime)을 직접 붙여야 한다. 13장에서 다시 다룬다.

이 다섯 자리에서 무너진다는 사실을 손에 쥔 채로 6장의 도구들을 쓰자. 모든 워크로드를 Workers + Hono로 밀어넣지 말고, 5장 워크시트가 *Move now*로 표시한 자리부터 차분히 옮기자. *지금 잘 돌고 있는 Spring Boot를 부수러 가는 게 아니다.*

### 마무리 — 7장 KV·D1로 가기 전에

빈 화면 앞에 앉았던 한 시간 전을 떠올려 보자. `@RestController`도 없고 `@Component`도 없고 `application-prod.yml`도 없는데 어디서부터 시작해야 할지 막막했던 그 자리. 지금은 손에 다섯 도구가 있다. `fetch(req, env, ctx)`라는 본질, Hono의 라우팅·미들웨어 체인, Bindings + c.set/get + 함수형 DI 셋, `.dev.vars`·`wrangler secret put`·`[env.*]`의 시크릿·환경 분리, vitest + miniflare의 테스트.

5장 워크시트로 결정한 *Move now* 항목 중 가장 risk-low한 한 개를 골라, 이 6장의 골격 위에 사흘쯤 깔아 보자. 사용자 검색 API든, 정적 자산 게이트웨이든, 인증 미들웨어든 좋다. 한 번 깔아 본 코드 위에 다음 장의 데이터 레이어가 얹힌다.

7장 *데이터 1 — KV와 D1, 워크로드 패턴으로 골라 쓰기*에서는 오늘 잠깐 만난 KV를 *어디까지 믿어도 되는지*, eventually consistent의 60초 전파가 무엇을 허용하고 무엇을 금지하는지, 그리고 SQL이 필요한 자리에 D1 + Drizzle을 어떻게 끼워 넣는지를 본격적으로 다룬다. 6장이 *골격*이었다면 7장은 그 골격에 *데이터의 살을 붙이는 장*이다. 사용자 CRUD에 D1을 추가하고, 세션은 KV로 분리하고, `drizzle-kit migrate`로 스키마를 첫 번째로 돌려보자.

자, 다음 장을 펴자.

---


## 7장. 데이터 1 — KV와 D1, 워크로드 패턴으로 골라 쓰기

DynamoDB로 세션을 굴리고 있었다고 해보자. on-demand 청구서가 매달 우편처럼 꼬박꼬박 도착하고, GSI를 두어 사용자 ID와 만료 시각으로 동시에 조회하고 있다. 어느 날 팀에서 누군가 묻는다. "이거, 그냥 Cloudflare KV로 옮기면 같은 게 되지 않아요?" 솔깃하다. KV는 글로벌 분산이고, 무료 plan에서도 꽤 넉넉하고, 4장의 매핑 표에서도 분명히 "DynamoDB ↔ KV"라는 줄을 봤다. 옮기면 안 될까?

그런데 잠깐. 4장에서 우리는 그 줄에 작은 가시 하나를 박아 두었다. *DynamoDB 한 줄 매핑은 거짓말이다.* DynamoDB로 하던 일이 사용자 패턴에 따라 KV로도, D1으로도, Durable Objects로도 갈라진다고 분명히 적었다. 그리고 5장에서 우리는 5축 결정 트리를 세웠다 — 일관성·런타임·글로벌성·요청 패턴·컴플라이언스. 그 두 도구를 손에 쥔 채로 이 장에 들어왔다.

자, 그렇다면 이번 장에서 풀어야 할 질문은 무엇인가. *KV와 D1을 어디서부터 어디까지 믿어야 하는가.* 어떤 워크로드를 KV에 맡기면 나중에 후회하지 않고, 어떤 워크로드를 D1에 얹으면 production을 견디는가. 두 제품의 본질을 이해하지 못하면 6개월 뒤에 우리는 KV 위에 secondary index를 흉내내려고 코드를 비비 꼬고 있거나, D1 한 DB가 10GB 한도에 부딪쳐 야간에 sharding 전략을 그리고 있을 것이다. 둘 다 끔찍한 일이다.

이 장에서는 KV와 D1을 워크로드 패턴별로 어디에 어떻게 자리 잡게 할지, 그리고 둘 중 어느 쪽에도 답이 아닐 때 무엇을 해야 하는지를 정리해 보자. 6장에서 만든 사용자 API 한 벌은 이미 KV에 세션을 두고 있다. 이 장에서는 그 위에 D1과 Drizzle을 얹어 사용자 프로필을 진화시켜 보겠다.

### KV — 본질부터 다시 그리자

KV의 본질은 한 줄로 요약할 수 있다. *글로벌 분산 key-value 저장소, 그리고 eventually consistent.* 마지막 부분이 핵심이다. 우리가 한 PoP에서 값을 쓰면, 다른 PoP에서 그 값을 읽을 수 있게 되기까지 *최대 60초*가 걸린다. 평균은 훨씬 짧지만 SLA로 약속되는 숫자는 60초다.

DynamoDB도 eventually consistent 모드가 기본이라 비슷해 보일 수 있다. 그런데 DynamoDB는 옵션으로 strongly consistent read를 켤 수 있고, 같은 region 안에서는 거의 즉시 일관성이 보장된다. KV는 다르다. *strongly consistent 모드 자체가 없다.* 글로벌 분산이 KV의 정체성이고, 그 대가로 일관성을 늦췄다.

여기에 또 하나의 제약이 붙는다. **per-key 1 write/s.** 한 키에 1초에 한 번 이상 쓰면 그 너머의 쓰기는 거부되거나 마지막 것만 살아남는다. 카운터를 KV에 두면 안 된다는 뜻이다. 서로 다른 사용자의 세션을 각자의 키에 저장하는 건 괜찮지만, "전체 활성 사용자 수"를 한 키에 담아 매 요청마다 증가시키려고 하면 KV는 거기서 무너진다.

마지막 제약이 가장 무겁다. **secondary index도, range query도 없다.** 키 하나로 값 하나를 꺼낸다. 그게 전부다. `list()`로 prefix 기반 나열은 되지만, "30일 이내에 만료되는 세션을 모두 찾아라" 같은 쿼리는 못 한다. DynamoDB의 GSI를 기대하고 옮기면 거의 반드시 사고가 난다.

#### KV가 빛나는 자리

이런 제약을 받아들이고도 KV가 빛나는 자리는 분명하다. 5장의 결정 매트릭스에서 *Move now*로 묶였던 패턴들 — *read-heavy, eventually consistent로 충분, 단일 키 lookup* — 의 자리다.

- **세션 토큰.** 사용자가 로그인하면 토큰을 KV에 쓴다. 60초 후에 다른 PoP에서도 그 토큰이 보인다. 세션을 60초 안에 같은 토큰으로 두 번 검증하는 시나리오는 거의 없다.
- **Feature flag.** 어드민이 토글을 켜면 60초 후에 모든 PoP에서 그 변경이 반영된다. 광고 캠페인이나 베타 기능 노출에 충분하다.
- **API key·configuration.** 외부 API 키, 라우팅 설정, A/B 테스트 그룹. 자주 바뀌지 않고, 바뀌어도 1분 정도 늦게 적용돼도 무방한 데이터.
- **사용자 설정.** 다크 모드, 언어 선택, 알림 토글 같은 것. 사용자가 바꾼 직후에 다른 디바이스에서 1분 늦게 보이는 건 보통 문제가 안 된다.
- **읽기 캐시.** 외부 API 응답을 5분 TTL로 캐시. 한국 사용자가 일본 PoP을 거치든 미국 PoP을 거치든 거의 같은 캐시 적중률을 본다.

이 다섯 자리는 KV가 가장 안전하게 자리 잡는 곳이다. 6장에서 만든 사용자 API의 세션 저장소는 KV 그대로 두자. 7장이 끝나도 거기는 KV다.

#### KV가 무너지는 자리

반대로, 다음 자리에서는 KV가 무너지거나 거짓 약속을 한다. 무너진다는 건 동작 안 한다는 뜻이 아니다. *동작은 하지만 production에서 사고로 이어진다*는 뜻이다.

- **검색·정렬·범위 쿼리가 필요한 자리.** secondary index가 없으니 "활성 사용자 목록을 가입일 순서로" 같은 쿼리는 못 한다. 한 키에 JSON 배열로 다 담아 두고 매번 전체를 읽어 메모리에서 필터링하면 잠깐은 돌지만 데이터가 커지면 끝이다.
- **빈번한 쓰기.** per-key 1 write/s 한도. 카운터·실시간 통계·재고 차감은 KV의 자리가 아니다. 이건 D1 또는 Durable Objects의 영역이다.
- **transactional 일관성이 필요한 자리.** 좌석 예약, 재고 차감, 게임 턴. KV는 atomic compare-and-swap도 트랜잭션도 없다. 두 사용자가 같은 좌석을 동시에 예약하면 둘 다 성공한다.
- **strong consistency가 필요한 자리.** 결제 후 즉시 잔액을 읽어야 하는 시나리오. KV에 잔액을 두고 결제 후 잔액을 읽으면 60초 동안은 옛날 값이 보일 수 있다.

이 네 가지 중 하나라도 해당된다면 KV는 답이 아니다. *솔직히 다른 자리를 찾자.*

#### Liftosaur — 정직한 회귀

KV 이야기를 광고처럼 들리지 않게 하려면 한 사례를 마주봐야 한다. 운동 트래킹 앱 *Liftosaur*는 1인 개발자가 만든 서비스인데, 처음에는 Workers + KV 위에 시스템을 올렸다가 결국 Lambda + DynamoDB로 회귀했다. 회귀 사유를 본인이 블로그에 정직하게 남겼다. 그 글을 읽으면 KV가 무너지는 자리가 한 화면에 펼쳐진다.

- **secondary index 부재.** 운동 데이터는 사용자 ID로도 조회하고, 운동 종류로도 조회하고, 날짜 범위로도 조회해야 한다. KV에서는 이 세 가지가 다 단일 키 lookup으로 안 풀린다. DynamoDB라면 GSI 두세 개로 끝나는 일이다.
- **range query 부재.** "최근 7일간의 운동 기록"을 가져오려면 매번 전체를 스캔해야 한다.
- **KV 백업 어려움.** KV는 점진적 백업·복원 도구가 약하다. DynamoDB의 PITR(point-in-time recovery)이나 export to S3에 비교하면 운영적 안전망이 얇다.
- **Node 라이브러리 부재.** 이미지 처리에 필요한 일부 Node 라이브러리가 Workers에서 동작하지 않았고, 1MB 스크립트 한도(당시 기준)에 걸려 의존성을 넣을 수가 없었다. *이건 KV 문제는 아니지만, Workers 위에 워크로드 전체를 올린다는 결정의 일부였다.*

이 네 가지가 모여 결국 Lambda + DynamoDB로 돌아갔다. 본인이 블로그에서 강조한 결론은 분명하다 — *KV를 DynamoDB의 대체재로 보지 말라.* 사용 패턴이 secondary index나 range query에 의존한다면, KV가 아니라 DynamoDB나 D1로 가야 한다.

이 사례를 어떻게 받아들이면 좋을까. 두 가지로 나눠 보자. 첫째, *5축 결정 트리를 미리 돌렸다면 옮기지 않았을 것이다.* 일관성 축에서 secondary index 필요성이 보였을 테고, 런타임 축에서 1MB 한도와 Node 라이브러리 부재가 빨간불을 켰을 것이다. 둘째, *옮긴 뒤 회귀하는 것도 정직한 결정이다.* 6개월 운영해 보고 무너지는 자리를 확인했다면, 자존심을 굽히고 후퇴할 줄 아는 게 더 큰 용기다.

이 책의 핵심 약속을 한 번 더 떠올려 보자 — *Cloudflare를 도입하지 말고, 자기 아키텍처에 올바른 자리를 내주자.* Liftosaur는 KV가 자기 워크로드의 올바른 자리가 아니었다는 걸 운영 비용을 치르고 배웠다. 우리는 그 학습을 빌릴 수 있다.

#### KV 코드 한 사이클

본질을 봤으니 손으로 한 번 만져 보자. 6장의 사용자 API에 KV 세션 저장소가 이미 있다고 가정하자. `wrangler.toml`에 KV 바인딩을 선언하고, Hono 미들웨어에서 토큰을 읽고 쓰는 한 사이클이다.

먼저 `wrangler.toml`.

```toml
name = "toby-shop-api"
main = "src/index.ts"
compatibility_date = "2026-04-01"

[[kv_namespaces]]
binding = "SESSIONS"
id = "your-kv-namespace-id"
preview_id = "your-preview-id"
```

`binding = "SESSIONS"`가 핵심이다. 이 한 줄이 코드 안에서 `env.SESSIONS`로 들어오는 핸들이 된다. 4장에서 살펴봤듯 Bindings는 Spring의 `@Autowired`와 IAM role을 한 추상으로 묶은 것이다. 별도의 SDK 클라이언트도, IAM 정책도 없다.

이제 Hono 핸들러.

```ts
import { Hono } from "hono";

type Bindings = { SESSIONS: KVNamespace };

const app = new Hono<{ Bindings: Bindings }>();

// 로그인 — 세션 토큰 발급
app.post("/auth/login", async (c) => {
  const { userId } = await c.req.json<{ userId: string }>();
  const token = crypto.randomUUID();
  await c.env.SESSIONS.put(
    `session:${token}`,
    JSON.stringify({ userId, createdAt: Date.now() }),
    { expirationTtl: 60 * 60 * 24 * 7 }, // 7일 TTL
  );
  return c.json({ token });
});

// 세션 검증 미들웨어
app.use("/me/*", async (c, next) => {
  const token = c.req.header("authorization")?.replace("Bearer ", "");
  if (!token) return c.text("unauthorized", 401);
  const raw = await c.env.SESSIONS.get(`session:${token}`);
  if (!raw) return c.text("expired", 401);
  c.set("session", JSON.parse(raw));
  await next();
});

app.get("/me", async (c) => c.json(c.get("session")));

export default app;
```

세 가지를 짚어 두자. 첫째, `expirationTtl`. KV는 키마다 TTL을 줄 수 있다. 7일 후에는 자동으로 사라진다. DynamoDB의 TTL과 똑같은 모델인데, KV에서는 옵션 한 줄로 끝난다. 둘째, `put`/`get`/`list`라는 단순한 API. SQL도, 인덱스도, 트랜잭션도 없다. *그래서 빠르고, 그래서 제약된다.* 셋째, `put` 직후 다른 PoP에서 `get`을 부르면 60초 동안은 못 찾을 수 있다는 사실. 같은 PoP에서 같은 사용자가 같은 요청을 보내는 시나리오는 보통 문제가 안 되지만, 다중 region·다중 디바이스에서는 이걸 잊지 말자.

`list()`로 prefix 기반 나열도 가능하다.

```ts
const result = await c.env.SESSIONS.list({ prefix: "session:" });
for (const key of result.keys) {
  // key.name, key.expiration
}
```

다만 이걸 매 요청마다 부르면 비용이 무섭게 올라간다. KV의 `list`는 고운 검색이 아니라 *prefix scan*이다. 쓰임을 가려야 한다.

자, KV는 여기까지. 이제 D1으로 넘어가자.

### D1 — SQLite at edge, 그리고 그 한계

D1의 본질은 한 마디로 *SQLite를 글로벌 edge에 펼친 것*이다. SQL 쿼리, JOIN, CTE, 트랜잭션, prepared statement 전부 된다. 기존 RDS Postgres에 익숙한 개발자라면 손에 익은 도구를 거의 그대로 들 수 있다.

다만 두 가지 제약이 있다.

**첫째, 1 DB 최대 10GB.** 작은 SaaS의 사용자 데이터, 게시물, 주문 내역에는 충분하지만, 대규모 로그·이벤트 스트림을 D1에 다 담겠다는 발상은 위험하다. 한도에 가까워지면 sharding 전략을 미리 그려야 하는데, sharding을 하느니 처음부터 Postgres + Hyperdrive(10장)로 가는 편이 낫다.

**둘째, sustained write 500~2k/s.** D1의 read replica는 자동으로 글로벌 PoP에 분산되지만, write는 primary 한 곳에서 받는다. 초당 수천 건 이상의 쓰기가 지속되는 워크로드 — 게임 텔레메트리, IoT 센서 데이터, 실시간 분석 — 는 D1의 자리가 아니다. *이건 D1을 비난하는 게 아니다. 모델이 그렇게 설계된 것이다.* 비교를 위해 다른 SQLite 계열인 Turso는 1~5k/s, 본격 RDB인 PostgreSQL/MySQL은 10k~50k/s 수준이다.

이 두 한도 안에 들어오는 워크로드라면 D1은 Workers와 가장 자연스럽게 짝이 맞는 데이터 저장소다. Workers Paid plan에는 일 250억 row read, 5천만 row write, 5GB storage가 기본 포함된다. 작은 SaaS 한 개를 다 운영하고도 비용 청구서가 거의 안 보일 수준이다.

#### D1이 빛나는 자리, 무너지는 자리

5장의 결정 매트릭스에서 *사용자 facing CRUD API*가 *Move later*로 묶였던 걸 떠올려 보자. D1이 바로 그 자리의 첫 번째 후보다.

- **빛나는 자리.** 사용자 프로필·주소·권한, 상품 카탈로그 메타데이터, 주문 내역(write 부담이 크지 않은 작은 이커머스), 블로그 게시물, 댓글, 작은 SaaS의 거의 모든 관계형 데이터.
- **무너지는 자리.** 초당 수천 건 이상의 쓰�기가 들어오는 워크로드(IoT, 게임 telemetry), 한 DB가 10GB를 명백히 넘을 데이터(대규모 분석 로그), cross-region 트랜잭션이 필요한 워크로드, 강한 region lock이 필요한 워크로드.

마지막 두 가지는 KV에도 해당되는 함정이다. *KV·D1 모두 cross-region 트랜잭션을 지원하지 않는다.* 한국 D1과 유럽 D1을 한 트랜잭션 안에서 다루는 건 불가능하다. 그게 필요하다면 Durable Objects(8장) 또는 외부 분산 DB로 가야 한다.

#### RDS Postgres에 익숙한 개발자의 시각에서

RDS를 5년 굴려 본 개발자가 D1을 만나면 무엇이 같고 무엇이 다른가. 한 페이지로 정리해 보자.

| 측면 | RDS Postgres | D1 |
|---|---|---|
| **쿼리 언어** | PostgreSQL 방언 | SQLite 방언 (대부분 호환, JSON·CTE 지원) |
| **트랜잭션** | full ACID, savepoint, 분산 트랜잭션 가능 | statement-level transaction, batch transaction |
| **인덱스** | B-tree, hash, GIN, GiST, partial, expression | B-tree, partial, expression (SQLite 표준) |
| **read replica** | 명시적 설정·관리 필요 | 자동 글로벌 분산 |
| **백업** | snapshot + PITR (보통 35일) | 자동 + Time Travel (point-in-time recovery 30일) |
| **연결 모델** | TCP 직접, connection pool 직접 관리(HikariCP) | Workers 바인딩, 풀 관리 불필요 |
| **확장** | vertical (인스턴스 크기) + horizontal (replica) | DB 단위 자동 (단, 1 DB 10GB 한도) |
| **스키마 마이그레이션** | Flyway, Liquibase | wrangler d1 migrations + Drizzle Kit |
| **운영 부담** | 패치·업그레이드·VPC·SG | 거의 없음 |

가장 인상적인 차이는 *연결 모델*이다. Spring + JPA + HikariCP를 운영해 본 사람이라면 connection pool size 튜닝, idle timeout, max lifetime 같은 파라미터들과 씨름한 기억이 있을 것이다. D1에서는 그 모든 게 사라진다. `env.DB.prepare(...)`라고 부르면 그만이다. 풀도, 타임아웃도, 인증도 Workers 런타임이 알아서 한다. *이게 자유롭게 느껴지면 좋고, 통제권을 잃은 듯해 찜찜하면 그것도 정상이다.* 두 감정 모두 합당하다.

#### D1 + Drizzle 코드 한 사이클

이제 6장의 사용자 API 위에 D1 + Drizzle을 얹어 보자. 세션은 KV 그대로 두고, 사용자 프로필을 D1에 담는 진화다. Drizzle은 TypeScript 친화적인 ORM 겸 query builder인데, JPA 같은 무거운 마법 없이 SQL과 1:1로 맵핑된다는 점이 깔끔하다.

`wrangler.toml`에 D1 바인딩을 추가하자.

```toml
[[d1_databases]]
binding = "DB"
database_name = "toby-shop"
database_id = "your-d1-database-id"
migrations_dir = "drizzle/migrations"
```

스키마 파일.

```ts
// packages/db/schema.ts
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const users = sqliteTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  displayName: text("display_name").notNull(),
  createdAt: integer("created_at", { mode: "timestamp" }).notNull(),
});

export const profiles = sqliteTable("profiles", {
  userId: text("user_id")
    .primaryKey()
    .references(() => users.id),
  bio: text("bio"),
  avatarUrl: text("avatar_url"),
  language: text("language").default("ko"),
});
```

마이그레이션 워크플로우는 Drizzle Kit이 알아서 한다.

```bash
# 스키마 변경 → SQL 마이그레이션 파일 생성
pnpm drizzle-kit generate

# wrangler가 D1에 적용
pnpm wrangler d1 migrations apply toby-shop --remote
```

`drizzle-kit generate`는 스키마 변경을 감지해 `drizzle/migrations/0001_xxx.sql` 같은 파일을 만든다. 그 파일을 `wrangler d1 migrations apply`가 D1에 적용한다. *Flyway·Liquibase에 익숙하다면 거의 같은 멘탈 모델이다 — 형상 변경이 SQL 파일로 떨어지고, 그 파일들이 순서대로 적용된다.* 한 가지 다른 점은 `--local` 플래그로 로컬 SQLite에 먼저 적용해 보고 production에 적용할 수 있다는 것. `wrangler dev --local`이 D1을 로컬 SQLite로 시뮬레이션해 주기 때문에, 로컬에서 마이그레이션 결과를 확인하고 production으로 넘어가는 흐름이 자연스럽다.

이제 Hono 라우터에 사용자 프로필 엔드포인트를 추가하자.

```ts
import { Hono } from "hono";
import { drizzle } from "drizzle-orm/d1";
import { eq } from "drizzle-orm";
import { users, profiles } from "@toby-shop/db/schema";

type Bindings = {
  DB: D1Database;
  SESSIONS: KVNamespace;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get("/users/:id", async (c) => {
  const db = drizzle(c.env.DB);
  const id = c.req.param("id");

  const result = await db
    .select({
      id: users.id,
      email: users.email,
      displayName: users.displayName,
      bio: profiles.bio,
      avatarUrl: profiles.avatarUrl,
    })
    .from(users)
    .leftJoin(profiles, eq(profiles.userId, users.id))
    .where(eq(users.id, id))
    .get();

  if (!result) return c.notFound();
  return c.json(result);
});

app.put("/me/profile", async (c) => {
  const db = drizzle(c.env.DB);
  const session = c.get("session"); // KV 미들웨어에서 주입
  const body = await c.req.json<{ bio?: string; language?: string }>();

  await db
    .insert(profiles)
    .values({ userId: session.userId, ...body })
    .onConflictDoUpdate({
      target: profiles.userId,
      set: body,
    });

  return c.json({ ok: true });
});
```

세 가지를 짚어 두자. 첫째, `drizzle(c.env.DB)`로 D1 바인딩을 Drizzle 인스턴스로 감싼다. 그 인스턴스가 SQL 쿼리를 타입 안전하게 만든다. 둘째, `leftJoin`이 자연스럽게 되고 결과는 `result` 객체에 그대로 들어온다. JPA의 `@OneToOne`·`@ManyToOne` 같은 어노테이션 없이 SQL과 1:1로 매핑된다. 셋째, `onConflictDoUpdate`는 SQLite의 `INSERT ... ON CONFLICT DO UPDATE`. PostgreSQL에서 익숙한 upsert 패턴이 그대로 통한다.

JPA의 `@Transactional` 같은 자동 propagation은 없다. D1에서 트랜잭션을 쓰려면 `db.batch([...])`로 여러 statement를 한 묶음으로 보낸다.

```ts
await db.batch([
  db.insert(users).values({ id, email, displayName, createdAt: new Date() }),
  db.insert(profiles).values({ userId: id, language: "ko" }),
]);
```

이 batch는 atomic하다. 둘 다 성공하거나 둘 다 실패한다. *Spring의 `@Transactional`처럼 메서드 경계에서 자동으로 시작·커밋되는 게 아니라, 코드에서 명시적으로 묶는다.* 처음엔 번거롭게 느껴질 수 있다. 그런데 한두 주 쓰다 보면, 트랜잭션 경계가 코드에 그대로 보이는 게 오히려 명료하다. JPA의 `LazyInitializationException` 같은 함정이 없다.

#### Read replica와 Time Travel

D1에는 RDS 운영 경험이 있는 개발자에게 인상적인 두 가지 기본 장치가 있다.

**Read replica는 자동이다.** Workers가 어느 PoP에서 깨어나든 그 PoP에 가장 가까운 D1 read replica에서 읽어 온다. RDS에서 read replica를 한국·일본·유럽에 띄우고, 애플리케이션에서 어느 replica로 보낼지 라우팅하던 일을 D1은 알아서 한다. *그 대신 write는 primary 한 곳으로 모인다.* 이게 sustained write 한도의 이유이기도 하다.

**Time Travel.** D1은 30일 전까지의 어느 시점으로든 데이터베이스를 복원할 수 있다. RDS의 PITR과 멘탈 모델이 같다. 누군가 실수로 `DELETE FROM users` 한 줄을 production에 날렸다면, `wrangler d1 time-travel restore`로 5분 전 상태로 되돌릴 수 있다. 별도 백업 설정도, 비용 추가도 없다. *이게 production을 다루는 안심의 핵심이다.* 운영 경험이 쌓일수록 이 한 줄이 얼마나 무거운 약속인지 알게 된다.

다만 한 가지 주의. Time Travel은 한 D1 인스턴스 안의 시간 복원이다. *cross-region 일관성이나 cross-DB 트랜잭션을 보장하지 않는다.* 두 D1 DB를 같은 시점으로 같이 되돌리려면 별도 코디네이션이 필요하다.

### KV vs D1 의사결정 표 — 다섯 축으로 갈라보자

여기까지 두 제품의 본질을 봤다. 이제 자기 워크로드를 어느 쪽에 둘지 결정하는 표를 한 장 만들어 두자. 5축 결정 트리를 KV·D1 사이의 비교로 좁힌 형태다.

| 축 | KV에 두자 | D1에 두자 |
|---|---|---|
| **데이터 형상** | 단일 키 lookup이면 충분한 평탄한 데이터 (세션, flag, 설정) | 관계형, JOIN 필요, 다중 인덱스 (사용자, 주문, 상품) |
| **쿼리 패턴** | 키 → 값, 또는 prefix scan | SQL JOIN, 정렬, 범위, GROUP BY, 집계 |
| **일관성 요구** | eventually consistent (≤60초 늦어도 OK) | strong consistency, statement-level transaction |
| **쓰기 빈도** | per-key 1 write/s 이내, key 수는 무제한 | 전체 sustained 500~2k/s 이내 |
| **데이터 크기** | 키당 25MB까지, 총 namespace 무제한 | 1 DB 10GB 한도 |

이 표를 한 워크로드 위에 올려 보고 다섯 축이 모두 한 쪽으로 기울면 거기가 답이다. 만약 *데이터 형상은 KV인데 쿼리 패턴은 D1*처럼 축이 갈라진다면, 잠깐 멈춰서 생각하자. 보통은 워크로드를 더 잘게 쪼개야 답이 나온다. 예를 들어 "사용자 프로필"이 한 덩어리로 보였는데, 사실은 *세션 토큰(KV) + 프로필 마스터(D1)*로 갈라야 자연스럽다.

5장에서 만든 결정 워크시트를 다시 펼쳐서 KV·D1 컴포넌트들을 이 다섯 축 위에 한 번 더 점검해 보자. 한 시간이면 충분하다. 그 한 번의 점검이 6개월 뒤의 회귀 비용을 절반 이상 줄여 준다.

### 둘 다 답이 아닐 때 — 정직한 한계

여기까지 KV가 빛나는 자리와 D1이 빛나는 자리를 봤다. 그런데 5장 결정 트리가 그랬듯, 이 장의 의무도 정직성이다. *KV·D1 모두 답이 아닌 워크로드*가 분명히 있고, 그땐 무엇을 해야 하는가.

**1. 빈번한 쓰기 + 강한 일관성이 동시에 필요한 자리.** 재고 차감, 좌석 예약, 게임 점수판. KV는 일관성이 약하고 D1은 sustained write가 약하다. 이건 *Durable Objects(8장)*의 자리다. actor 모델로 한 객체가 직렬화된 처리를 보장한다.

**2. 초당 수천 건 이상의 sustained write가 필요한 자리.** 로그 ingestion, 텔레메트리, 이벤트 스트림. D1의 500~2k/s를 넘어선다. 이건 *RDS·Aurora 그대로 두고 Hyperdrive(10장)로 앞에 두는 패턴*이 답이다. 또는 외부 ClickHouse·Snowflake로.

**3. 한 DB가 10GB를 명백히 넘을 데이터.** 대규모 분석, 장기 이력. D1은 한도에 가까워진다. 이것도 *Hyperdrive 너머의 Postgres* 또는 분석 전용 DB가 답이다.

**4. cross-region 트랜잭션이 필요한 자리.** 한국과 유럽의 데이터를 한 트랜잭션 안에서 다뤄야 한다면 KV·D1 모두 답이 아니다. *외부 분산 DB(CockroachDB, Spanner) 또는 사가 패턴*으로 풀어야 한다.

**5. 강한 region lock이 요구되는 자리.** 한국 데이터는 한국에만 둬야 하는 컴플라이언스 워크로드. D1 location hint가 일부 도움이 되지만, 글로벌 분산 자체가 모델의 정체성이라 완전한 region lock은 어렵다. 이건 *AWS RDS in ap-northeast-2를 그대로 유지하고 Hyperdrive로 앞에만 두는 패턴*이 가장 깔끔하다.

다섯 가지 모두 *Cloudflare를 쓰지 말라*는 결론이 아니다. *컴퓨트는 Workers, 데이터는 RDS — 하이브리드*가 거의 항상 가능하다는 게 이 책의 핵심 메시지다. 14장에서 이 패턴을 8단계 시퀀스로 풀어낼 텐데, 그 시퀀스의 데이터 부분이 바로 이런 결정의 연속이다. *옮길 데이터와 남길 데이터를 가른다.*

### 이 기술이 무너지는 자리

이 장의 마지막은 정직한 한계로 닫자. KV·D1·둘의 조합이 무너지거나 거짓 안심을 주는 자리들을 한 화면에 모아 두자.

- **KV의 secondary index 부재.** 가장 자주 만나는 함정이다. DynamoDB GSI를 기대하고 옮기면 거의 반드시 사고가 난다. Liftosaur 사례가 그 증거다. 단일 키 lookup으로 풀 수 없는 쿼리가 보인다면 KV는 답이 아니다.
- **KV의 60초 전파.** 같은 사용자가 한 PoP에서 쓰고 다른 PoP에서 1분 안에 읽는 시나리오라면 옛 값을 볼 수 있다. 멀티 디바이스·멀티 region 사용자가 많은 워크로드에서는 이 함정을 잊지 말자.
- **KV의 per-key 1 write/s.** 카운터·실시간 통계는 KV의 자리가 아니다. Durable Objects로 가자.
- **D1의 10GB 한도.** 작은 SaaS에는 충분하지만, 데이터가 크게 자랄 가능성이 있다면 처음부터 Postgres + Hyperdrive로 시작하는 편이 낫다. 10GB에 가까워진 다음 옮기는 건 거의 항상 야간작업이 된다.
- **D1의 sustained write 500~2k/s.** spike-y 트래픽은 견디지만 sustained 부담은 못 견딘다. write-heavy 워크로드는 RDS·Aurora를 그대로 두고 Hyperdrive로 앞에 두자.
- **둘 다 cross-region 트랜잭션 없음.** 한 트랜잭션이 두 region 데이터를 동시에 다뤄야 한다면 KV·D1 모두 답이 아니다.
- **KV·D1 사이의 트랜잭션 없음.** "세션은 KV, 사용자는 D1"이라는 자연스러운 분리가 한 가지 함정을 함께 가져온다 — *둘을 한 번에 일관되게 갱신하는 트랜잭션이 없다.* 보통은 D1을 source of truth로 삼고 KV를 캐시로 쓰는 패턴이 안전하다.
- **백업·DR의 운영 안전망.** D1의 Time Travel은 30일 PITR이라 든든하지만, KV의 백업·복원은 도구가 약하다. KV에 의존하는 핵심 데이터는 별도 백업 sink(R2 export 등)를 운영적으로 마련해 두자.

이 여덟 가지를 외워 두자. 외운다는 건 모든 케이스에서 거부하라는 뜻이 아니다. *시스템 설계 회의에서 이 여덟 가지가 적용되는지 한 번씩 점검하라*는 뜻이다. 점검 한 번이 6개월 뒤의 회귀를 막는다.

### 마무리 — 다음 장으로

자, 이번 장에서 우리는 무엇을 손에 쥐었나. KV의 본질과 한계, D1의 본질과 한계, 둘 사이의 5축 의사결정 표, 그리고 둘 다 답이 아닐 때 어디로 가야 하는지의 지도. 6장에서 만든 사용자 API는 이제 *세션은 KV, 사용자·프로필은 D1 + Drizzle*로 진화했다. 마이그레이션 한 사이클까지 손으로 돌아봤다. 깃 브랜치로 `ch7-data` 체크포인트를 남겨 두자.

그런데 우리가 아직 만나지 못한 자리가 둘 있다. *빈번한 쓰기 + 강한 일관성*과 *큰 파일·미디어*다. KV·D1 둘 다 답이 아니라고 위에서 미뤄 둔 자리들이다. 다음 장에서 그 두 자리를 채울 두 제품을 만난다 — *Durable Objects*와 *R2*다.

Durable Objects는 actor 모델로 한 객체에 한 인스턴스를 보장하는 묘한 도구다. 채팅방, 재고, 좌석 예약, 실시간 협업 문서가 그 자리다. WebSocket Hibernation API라는 비용 모델을 뒤집는 한 수도 함께 만난다. R2는 S3 호환의 글로벌 객체 저장소인데, *egress free*라는 한 줄이 미디어 워크로드의 청구서를 어떻게 다시 쓰는지 보게 된다.

8장에서는 `toby-shop`에 고객지원 채팅방 Worker를 한 개 더 띄우고, 채팅 메시지는 DO storage에, 첨부 파일은 R2 presigned URL로 받는 한 사이클을 손으로 만들어 보자. 자, 다음 장으로 가보자.

---


## 8장. 데이터 2 — Durable Objects와 R2, 그리고 Cache API

재고가 정확히 1개 남은 상품이 있다고 해보자. 블랙 프라이데이 자정에 그 한 상품을 노리고 있던 두 사용자가 있다. 둘이 거의 동시에 결제 버튼을 누른다. 한 명은 서울 PoP에서, 다른 한 명은 도쿄 PoP에서. 두 요청이 0.3초 차이로 백엔드에 도착한다. 그 0.3초 사이에 무슨 일이 벌어져야 옳을까. 한 명은 결제 성공, 다른 한 명은 "재고 없음" 안내. 절대로 두 명 모두 성공하면 안 된다. *재고가 -1이 되는 순간 회사 슬랙에 사장의 호통이 떨어진다.*

이 문제를 어떻게 푸는가. Spring 개발자라면 익숙한 답이 있다. `@Transactional`로 묶고 데이터베이스에 `SELECT ... FOR UPDATE` 락을 건다. 또는 Redis에 분산 락(Redisson)을 건다. 또는 RabbitMQ로 직렬화 큐를 만든다. 어느 길로 가든 핵심은 하나다. *동일 자원에 대한 쓰기를 한 줄로 세운다.* 한 줄로 세우는 사람이 어디에 있는지 — 그것이 DB냐, Redis냐, 큐 시스템이냐 — 가 다를 뿐이다.

그런데 7장에서 우리가 손에 쥔 도구는 KV와 D1뿐이다. KV는 eventually consistent니까 -1 사고가 정확히 그 60초 전파 창에서 터진다. D1은 SQL 트랜잭션이 되긴 하지만 글로벌 PoP에서 동시에 들어오는 race condition을 대놓고 직렬화하기에는 모양이 매끄럽지 않다. 그렇다면 무엇이 필요한가. *전역에서 단 하나뿐인, 그 자원을 위한 전용 서버가 필요하다.* 한 줄로 세우는 사람을 데이터베이스 안에 두지 말고, 자원 자체에 박아 두는 발상이다. 재고 자원에는 재고를 위한 단일 actor가, 채팅방에는 그 방을 위한 단일 actor가, 사용자 세션에는 사용자 본인을 위한 단일 actor가.

이게 Durable Objects다. AWS에 정확한 등가물이 없다. 굳이 한 줄로 매핑하면 *DynamoDB + Lambda + ElastiCache를 한 추상으로 묶은 것* 정도지만, 정확하지 않다. 4장에서 이미 이야기했다 — DynamoDB의 한 줄 매핑은 거짓말이다. 8장은 그 거짓말의 정직한 답을 손에 쥐는 챕터다. Durable Objects로 강한 일관성·실시간 협업·WebSocket을 다시 그리고, R2로 미디어 storage의 egress 청구서를 내려놓고, Cache API로 요청 단위 캐시를 손에 쥔다.

자, Durable Objects부터 살펴보자.

### Durable Objects — Actor 모델로 다시 생각하기

#### "객체"가 글로벌에서 단 하나뿐이라는 발상

Durable Objects를 처음 만나면 이름부터 헷갈린다. "Durable"이라니, 영속 저장소인가? "Object"라니, S3 같은 거? 둘 다 살짝 맞고 살짝 틀리다. 본질을 한 줄로 적으면 이렇다.

> **Durable Object는 ID로 지칭되는 단일 인스턴스다. 전역에서 그 ID에 대해 인스턴스는 정확히 하나만 존재하고, 한 곳의 PoP에 고정 위치를 갖고, 자체 영속 스토리지를 갖는다.**

세 단어가 핵심이다. **단일·고정·영속**.

단일이라는 말은 무엇을 뜻하는가. `room-12345`라는 채팅방 ID가 있다고 해보자. 서울에서 누가 메시지를 보내든, 도쿄에서 누가 보내든, 상파울루에서 누가 보내든, 그 메시지는 결국 *같은 인스턴스*에 도달한다. 인스턴스가 여러 PoP에 복제돼 있는 게 아니다. 한 PoP에 진짜로 한 개만 있다. 그래서 그 인스턴스 안에서 코드를 쓰는 동안에는 마치 single-threaded JavaScript처럼 동작한다. *race condition이 없다.* 두 요청이 동시에 들어오면 한 요청이 먼저 처리되고 다른 요청은 대기열에 줄을 선다. 마음 편한 일이다.

고정이라는 말도 중요하다. 한 번 인스턴스가 만들어진 PoP에서, 그 인스턴스는 그 자리를 지킨다. `idFromName('room-12345')`로 처음 깨운 사용자가 도쿄에 있었다면 그 채팅방 인스턴스는 도쿄 PoP에 자리를 잡는다. 그 뒤에 서울 사용자가 같은 방에 들어오면, 서울에서 도쿄까지 한 hop을 더 가는 셈이다. 글로벌 분산이 아니라 *지역 고정*이다. KV의 글로벌 균등 분산과는 정반대 모델이다. location hint로 어느 대륙에 둘지 일부 제어할 수 있지만, 본질은 *한 자원에는 한 자리*다.

영속이라는 말은 인스턴스 안에 자체 스토리지가 들어 있다는 뜻이다. `state.storage.put('inventory', 99)` 한 줄로 영속 저장된다. SQLite 백엔드 위에 트랜잭션·serializable 격리 수준까지 보장된다. D1처럼 별도의 DB 바인딩을 부를 필요가 없다 — 객체 안에 내장돼 있다. 그래서 재고 차감 같은 transactional 워크로드가 한 객체 안에서 깔끔하게 닫힌다. 락을 따로 걸 필요도, 분산 트랜잭션을 짤 필요도 없다.

이 셋을 묶으면 무엇이 보이는가. *Erlang의 actor가 보인다.* Akka, Orleans, Elixir GenServer를 알고 있다면 거의 같은 자리다. 메시지를 받아 자기 상태를 일관되게 갱신하는 actor 한 개가 자원 하나에 매달려 있는 것이다. Spring 개발자에게는 멀게 느껴질 수 있는데, 가장 가까운 비유를 찾자면 이렇다 — *`@Transactional`을 데이터베이스에 거는 게 아니라 자원 그 자체에 거는 모델이다.* 데이터베이스 락 경합을 만들 필요가 없다. 자원 안에 락이 이미 있다.

#### 가장 단순한 DO — 카운터 한 개부터

말로만 풀면 손끝이 가렵다. 가장 단순한 DO를 손으로 한 번 만들어 보자. 카운터 한 개. 호출할 때마다 1씩 증가하고, 현재 값을 돌려준다. 두 요청이 동시에 들어와도 절대로 같은 값을 반환하지 않는다.

```typescript
// src/counter.ts
import { DurableObject } from 'cloudflare:workers';

export class Counter extends DurableObject {
  async increment(): Promise<number> {
    const current = (await this.ctx.storage.get<number>('count')) ?? 0;
    const next = current + 1;
    await this.ctx.storage.put('count', next);
    return next;
  }

  async value(): Promise<number> {
    return (await this.ctx.storage.get<number>('count')) ?? 0;
  }
}
```

이게 전부다. `DurableObject`를 상속하고, 메서드 두 개를 둔다. `this.ctx.storage`가 영속 스토리지의 핸들이다. `get`·`put`은 자동으로 트랜잭션 단위로 묶인다. 한 메서드 호출 안에서 일어난 모든 storage 연산은 atomic하다. *`SELECT FOR UPDATE`가 자동으로 걸려 있는 셈이다.*

그러면 이 객체를 Worker에서 어떻게 부르는가. Worker 진입점은 평소처럼 `fetch`이고, 그 안에서 DO를 namespace로 받아 ID로 인스턴스를 깨운다.

```typescript
// src/index.ts
export { Counter } from './counter';

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);
    const name = url.searchParams.get('name') ?? 'default';

    const id = env.COUNTER.idFromName(name);
    const stub = env.COUNTER.get(id);

    if (url.pathname === '/inc') {
      const v = await stub.increment();
      return Response.json({ value: v });
    }
    if (url.pathname === '/val') {
      const v = await stub.value();
      return Response.json({ value: v });
    }
    return new Response('not found', { status: 404 });
  },
} satisfies ExportedHandler<Env>;
```

`wrangler.toml`에는 한 묶음의 선언이 들어간다.

```toml
name = "toby-shop-do"
main = "src/index.ts"
compatibility_date = "2026-04-01"

[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"

[[migrations]]
tag = "v1"
new_sqlite_classes = ["Counter"]
```

`[[migrations]]` 항목이 처음 보면 낯설다. 2장에서 살짝 짚고 넘어왔지만 여기서 다시 짚자. DO는 클래스가 곧 데이터다. 클래스를 추가하거나 이름을 바꾸면 명시적인 migration tag로 그 변경을 선언해야 한다. 안 그러면 *배포 자체가 거부된다.* 처음에는 번거롭다 싶지만, 이 강제가 운영에서 큰 사고를 막아 준다. 내가 모르는 사이에 데이터가 매여 있는 클래스가 사라지는 일을 시스템이 거부해 준다.

이걸 배포하고 한 번 두드려 보자.

```
$ wrangler deploy
$ curl 'https://toby-shop-do.<sub>.workers.dev/inc?name=room-1'
{"value":1}
$ curl 'https://toby-shop-do.<sub>.workers.dev/inc?name=room-1'
{"value":2}
$ curl 'https://toby-shop-do.<sub>.workers.dev/inc?name=room-2'
{"value":1}
```

`name`을 바꾸면 다른 인스턴스다. 같은 `name`은 글로벌에서 단 하나뿐이다. *서울에서 두 번, 도쿄에서 한 번 누르든 정확히 한 줄로 직렬화된다.* 이 작은 카운터가 재고 차감의 본질을 그대로 담고 있다.

#### Spring `@Transactional` + Redis 락의 자리를 DO가 가져가는 방식

Spring 멘탈로 같은 일을 짠다고 해보자. 재고 차감 코드는 어떻게 생겼는가.

```java
// Spring 멘탈
@Service
public class InventoryService {
    @Autowired private InventoryRepository repo;
    @Autowired private RedissonClient redisson;

    @Transactional
    public boolean reserve(String sku) {
        RLock lock = redisson.getLock("inventory:" + sku);
        if (!lock.tryLock(0, 5, TimeUnit.SECONDS)) return false;
        try {
            Inventory inv = repo.findBySku(sku).orElseThrow();
            if (inv.getStock() < 1) return false;
            inv.setStock(inv.getStock() - 1);
            repo.save(inv);
            return true;
        } finally {
            lock.unlock();
        }
    }
}
```

세 가지가 보인다. (1) Redisson 분산 락으로 같은 SKU에 대한 동시 호출을 직렬화한다. (2) `@Transactional`로 DB read·write를 트랜잭션 안에 묶는다. (3) `tryLock` 타임아웃·예외 처리를 손으로 챙긴다. *마음을 졸이는 일이다.* Redis가 죽으면 어떻게 되는가. 락 키가 expire 안 되면? 트랜잭션 격리 수준이 잘못 설정돼 있으면? 운영 중에 정말로 -1 사고가 한 번이라도 터지면 그날 새벽이 길어진다.

같은 일을 DO로 짜면 이렇다.

```typescript
export class Inventory extends DurableObject {
  async reserve(): Promise<{ ok: boolean; remaining: number }> {
    const stock = (await this.ctx.storage.get<number>('stock')) ?? 0;
    if (stock < 1) return { ok: false, remaining: 0 };
    await this.ctx.storage.put('stock', stock - 1);
    return { ok: true, remaining: stock - 1 };
  }
}
```

여기에는 락 코드가 없다. 트랜잭션 어노테이션도 없다. *그래도 race condition이 없다.* 인스턴스가 글로벌에서 단 하나라서, 두 요청이 동시에 들어와도 한 요청이 먼저 끝난 뒤에야 다음 요청의 코드가 실행된다. storage `get`·`put`은 그 호출 안에서 atomic하다. 사장의 호통을 부를 -1 사고가 architecture 단에서 차단된다.

물론 공짜는 없다. 두 줄을 적어 두자.

- DO는 *하나*만 있어서 안전하지만, 그 하나에 트래픽이 몰리면 한 줄에 줄을 서야 한다. 한 인스턴스의 처리량이 곧 그 자원의 처리량이다. 그래서 핫한 SKU 하나가 초당 1만 reserve를 받아야 한다면 DO의 단일 인스턴스 모델로는 무리다. 그때는 자원을 쪼갠다 — `inventory-{sku}-{shard0~9}` 같은 식으로 1차 샤딩을 두든지, write-heavy 영역은 Hyperdrive 너머의 Postgres에 두는 편이 낫다. 5장의 결정 프레임이 여기서 다시 등장한다.
- DO는 한 PoP에 고정 위치를 갖는다. `idFromName('inventory-sku-1')`을 도쿄 사용자가 처음 깨우면 도쿄에 자리잡는다. 그 뒤에 미국 사용자가 같은 SKU를 찌르면 도쿄까지 한 hop을 가야 한다. *정상이다.* 그래서 멀티테넌트 SaaS의 per-tenant DO는 location hint로 그 테넌트의 주 사용 지역에 배치하는 게 좋다.

자, 카운터를 손에 쥐었으니 이제 채팅방으로 가보자. 그리고 그 김에 *DO의 가격 모델을 뒤집은 한 수* — WebSocket Hibernation을 만나자.

#### WebSocket Hibernation — 영속 연결의 비용 모델을 뒤집는 한 수

채팅방을 운영해 본 사람은 알 것이다. WebSocket 연결 1만 개를 한 서버가 들고 있으면, 그 서버 메모리는 하루 종일 떠 있어야 한다. AWS에서는 ECS Fargate 한 컨테이너가 24시간 떠 있고, 사용자가 메시지를 안 보내고 가만히 있어도 메모리·CPU 청구서가 계속 적힌다. 진짜로 메시지가 오가는 시간은 전체의 1%도 안 되는데 *나머지 99%의 시간에도 비용이 적힌다.* 찜찜하다.

DO에 WebSocket을 그냥 얹어도 같은 문제가 일어난다. 클라이언트가 `WebSocket` 연결을 유지하는 동안 그 DO 인스턴스는 메모리에 떠 있어야 하고, GB-s 과금이 계속 잡힌다. 그래서 Cloudflare가 WebSocket Hibernation API를 따로 만들었다. 본질은 한 줄이다.

> **연결은 살아 있되, DO 인스턴스는 메시지 사이의 휴면기에 메모리에서 내려간다. 메시지가 도착하면 DO가 깨어나 핸들러를 실행한다. 그 깨어 있는 시간만 과금된다.**

WebSocket 표준 위에 위장된 마술이 한 겹 들어 있다. 클라이언트는 연결이 정상으로 살아 있다고 본다. 서버는 메시지가 도착할 때만 메모리를 차지한다. 1만 명이 채팅방에 가만히 있는 시간 동안에는 *과금이 멈춘다.* 영속 연결의 비용 모델이 처음으로 정직해졌다.

이걸 코드로 보면 차이가 분명하다. 일반 WebSocket DO와 Hibernation API의 결정적 차이는 *연결 상태를 메서드 인자로 받는다*는 점이다. 인스턴스 변수에 보관하면 sleep 동안 그게 사라지니까.

```typescript
import { DurableObject } from 'cloudflare:workers';

export class ChatRoom extends DurableObject {
  async fetch(request: Request): Promise<Response> {
    if (request.headers.get('Upgrade') !== 'websocket') {
      return new Response('expected websocket', { status: 426 });
    }

    const pair = new WebSocketPair();
    const [client, server] = [pair[0], pair[1]];

    // Hibernation API — DO가 잠들어도 연결은 유지된다.
    this.ctx.acceptWebSocket(server);

    return new Response(null, { status: 101, webSocket: client });
  }

  async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer): Promise<void> {
    if (typeof message !== 'string') return;
    const text = message.slice(0, 2000);

    // 영속 저장 — 마지막 50개 메시지를 보관해 늦게 들어온 사람도 문맥을 본다.
    const recent = (await this.ctx.storage.get<string[]>('recent')) ?? [];
    recent.push(text);
    if (recent.length > 50) recent.shift();
    await this.ctx.storage.put('recent', recent);

    // 같은 방에 연결된 모든 클라이언트에 브로드캐스트.
    for (const peer of this.ctx.getWebSockets()) {
      try {
        peer.send(text);
      } catch {
        // 보낼 수 없는 소켓은 닫혀 있다 — 무시하자.
      }
    }
  }

  async webSocketClose(ws: WebSocket, code: number, reason: string, wasClean: boolean): Promise<void> {
    try { ws.close(code, reason); } catch {}
  }
}
```

세 가지가 눈에 띈다. (1) `this.ctx.acceptWebSocket(server)` — 이 한 줄이 일반 `server.accept()`와 갈라지는 지점이다. Hibernation 모드를 켜는 스위치다. (2) 메시지 핸들러가 `webSocketMessage`라는 *메서드*다. 클로저로 잡지 않는다. DO가 sleep에서 깨어나면 이 메서드가 호출된다. 인스턴스 변수는 사라져 있을 수 있어서, 필요한 상태는 모두 storage에 두거나 메시지에 실어야 한다. (3) `this.ctx.getWebSockets()`로 현재 살아 있는 소켓 목록을 받는다. 인스턴스 변수에 손으로 모아 두지 않아도 된다. *플랫폼이 기억해 준다.*

그리고 진입점.

```typescript
export { ChatRoom } from './chat-room';

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);
    const room = url.searchParams.get('room') ?? 'lobby';

    const id = env.CHAT.idFromName(`room:${room}`);
    const stub = env.CHAT.get(id);

    return stub.fetch(req);
  },
} satisfies ExportedHandler<Env>;
```

```toml
[[durable_objects.bindings]]
name = "CHAT"
class_name = "ChatRoom"

[[migrations]]
tag = "v1"
new_sqlite_classes = ["ChatRoom"]
```

이걸 띄우고 브라우저 콘솔에서 `new WebSocket('wss://.../?room=cs-001')` 두 개를 두 탭에 열어 보자. 한쪽에서 보낸 메시지가 다른 쪽에 즉시 도착한다. 그 둘이 잠시 메시지를 안 보내는 동안에는, 가격표상 *과금이 멈춰 있다.* 1시간 동안 두 사용자가 가만히 있었다면 그 1시간은 거의 공짜다.

이게 어떤 변화를 만드는가. 고객지원 채팅방을 ECS에 띄워 1만 동시 연결을 유지하는 비용과, DO + Hibernation으로 같은 1만 연결을 유지하는 비용을 비교해 보자. 후자는 *실제로 메시지를 주고받는 시간만* 비용이 잡힌다. 야간·주말 idle 트래픽이 그대로 청구서에서 빠진다. 한국 SaaS의 고객지원 채팅처럼 idle 비율이 90%를 넘는 워크로드에서는 비용 모델 자체가 다르다.

물론 정직해지자. 전송 메시지 수는 여전히 과금된다. 메시지가 폭주하는 라이브 스트림 채팅(분당 수만 건)이라면 *별로 매력적이지 않을 수 있다.* Hibernation은 *대기 시간이 긴* 워크로드에 빛난다. 5장의 결정 프레임을 다시 들고 와서, 트래픽 형상이 idle-heavy인지 burst-heavy인지부터 본다.

#### `[[migrations]]`라는 안전장치 — 무심코 넘기면 안 되는 한 줄

DO를 운영하다 보면 한 번은 마주치는 실수가 있다. 클래스 이름을 바꾸거나 새 DO 클래스를 추가하면서 `[[migrations]]` 태그를 깜빡한다. 그 상태로 `wrangler deploy`를 누르면 *배포가 그냥 거부된다.* 처음 보면 짜증스럽지만, 이 거부가 큰 사고를 막아 준다.

DO에서 클래스는 곧 데이터다. 클래스 이름을 바꾸면 그 이름으로 매여 있던 영속 데이터가 *고아*가 될 수 있다. 그래서 Cloudflare는 강제로 명시적인 결정을 요구한다 — "이 클래스 이름이 바뀌었습니다, 기존 데이터는 새 클래스에 매달려 있다고 봐도 됩니까?", "이 클래스를 추가했고 SQLite 백엔드를 씁니다, 맞습니까?" 같은 식으로.

```toml
[[migrations]]
tag = "v1"
new_sqlite_classes = ["Counter"]

[[migrations]]
tag = "v2"
new_sqlite_classes = ["ChatRoom"]

[[migrations]]
tag = "v3"
renamed_classes = [{ from = "ChatRoom", to = "SupportRoom" }]
```

태그는 누적이다. v1·v2·v3가 순서대로 적용된다. 한 번 적용된 태그를 바꾸면 안 된다. 운영하면서 가장 많이 보는 에러 메시지가 "tag X already applied"인데, 이 메시지를 만나면 새 태그를 추가하는 게 답이지 기존 태그를 수정하는 게 답이 아니다. *기억해두자.* `[[migrations]]`는 번거로워도 선물이다.

자, DO 이야기는 여기까지. 이제 큰 파일이 머무는 자리, R2로 가보자.

### R2 — egress free라는 한 줄이 바꾸는 풍경

#### S3에 익숙한 손이 R2를 만났을 때

R2를 가장 빠르게 이해하는 길은 한 줄이다. *S3 호환 API에 egress free를 더한 것.* 이게 핵심이고, 거의 전부다. AWS S3로 코드를 짜본 사람이라면 R2의 SDK 사용법은 별다른 학습이 필요 없다. `aws-sdk`의 endpoint만 R2로 바꾸면 거의 그대로 동작한다.

```typescript
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

// R2도 같은 SDK를 쓴다. endpoint와 region만 다르다.
const r2 = new S3Client({
  region: 'auto',
  endpoint: `https://${env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: env.R2_ACCESS_KEY_ID,
    secretAccessKey: env.R2_SECRET_ACCESS_KEY,
  },
});

// 업로드 — S3 코드와 동일.
await r2.send(
  new PutObjectCommand({
    Bucket: 'toby-shop-attachments',
    Key: `chat/${roomId}/${crypto.randomUUID()}.jpg`,
    Body: imageBytes,
    ContentType: 'image/jpeg',
  }),
);

// presigned URL — 이것도 S3와 동일. 클라이언트 직접 업로드용.
const presignedUrl = await getSignedUrl(
  r2,
  new PutObjectCommand({
    Bucket: 'toby-shop-attachments',
    Key: `chat/${roomId}/${crypto.randomUUID()}.jpg`,
    ContentType: 'image/jpeg',
  }),
  { expiresIn: 600 }, // 10분
);
```

S3로 짜본 코드라면 한 줄도 다르지 않다. 그래서 *마이그레이션 부담이 가장 낮은 자리*가 보통 R2다. 14장의 8단계 시퀀스에서 데이터 영역의 첫 줄에 R2가 오는 이유가 이것이다. SDK 호환·도구 호환(rclone·s3cmd·Mountpoint 등 거의 모두 동작)·동작 의미가 거의 같다.

Worker 안에서는 SDK 없이 더 매끄럽게 부르는 길도 있다. R2 binding을 wrangler.toml에 선언하면, env 안에 type-safe한 R2 핸들이 들어온다.

```toml
[[r2_buckets]]
binding = "ATTACHMENTS"
bucket_name = "toby-shop-attachments"
```

```typescript
// Worker 안에서 — SDK 없이.
const obj = await env.ATTACHMENTS.get(key);
if (obj === null) return new Response('not found', { status: 404 });

return new Response(obj.body, {
  headers: { 'content-type': obj.httpMetadata?.contentType ?? 'application/octet-stream' },
});

// 업로드.
await env.ATTACHMENTS.put(key, request.body, {
  httpMetadata: { contentType: request.headers.get('content-type') ?? undefined },
});
```

binding 방식은 IAM key 회전·SDK 의존성·credential 노출이 없다. *2장에서 살펴본 Bindings의 위력이 R2에서도 그대로다.* 외부에서 부르는 게 필요한 경우(예: 다른 클라우드의 batch가 R2에 쓰는 경우)에는 SDK + S3 endpoint, 자기 Worker 안에서 부르는 경우에는 binding이 권장 패턴이다. 두 길을 자기 워크로드에 맞게 골라 쓰자.

#### egress free가 진짜 의미를 갖는 자리

R2의 결정타는 가격이다. 본문 표지 한 줄이 "egress free"인 게 마케팅 카피가 아니라 실제 청구서의 차이를 만든다. 미디어 스트리밍·대형 백업·LLM 학습 데이터셋처럼 *outbound 트래픽이 큰 워크로드*에서 90~99% 절감 사례가 흔하다. 한 번 숫자로 그려 보자.

가상 시나리오 — 사용자 업로드 미디어를 매월 30TB 다운로드(egress)하는 서비스. 50TB까지 넘어가는 시나리오로 잡고, AWS S3와 R2를 비교한다 (2026년 5월 시점 표준 단가 기준).

| 항목 | AWS S3 Standard | R2 |
|---|---|---|
| Storage 50TB·월 | $1,150 (~$0.023/GB) | $750 (~$0.015/GB) |
| Egress 50TB·월 | $4,500 (~$0.09/GB) | **$0** |
| Class A operations(쓰기) | 별도 (요청 수 따라) | 별도 ($4.50/M) |
| Class B operations(읽기) | 별도 | 별도 ($0.36/M) |
| **월 합계 (단순 추정)** | **약 $5,650+** | **약 $750+** |

90% 가까운 절감이 한 줄에서 나온다. 미디어를 많이 내보내는 서비스라면 *옮기지 않는 게 더 이상한* 자리다. 5장에서 이 워크로드 패턴이 "Move now"로 분류된 이유가 여기에 있다.

물론 한 줄로 다 말하면 거짓말이다. egress free의 *정직한 한계*도 적어두자.

- Class A·Class B operations은 과금된다. 100TB를 쌓더라도 그것을 read하는 GET 요청 수가 한 번에 수억 건이라면 Class B 청구가 누적된다. 작은 객체를 매우 많이 read하는 패턴(예: 매 요청마다 1KB tile 50개를 가져오는 지도 서비스)에서는 절감 효과가 줄어든다.
- 처음 옮길 때 *AWS의 inbound가 아니라 AWS의 outbound가 청구된다.* S3 → R2로 50TB를 동기화하는 한 번의 작업에 AWS 측 egress $4,500이 한꺼번에 청구된다. 매월의 장기 절감을 위한 일회성 비용이지만, 모르고 시작하면 *깜짝 놀란다.* 미리 재무팀에 알려 두는 편이 낫다.
- multipart upload, presigned URL, lifecycle 일부, S3 API 거의 다 호환되지만 완전 호환은 아니다. 특히 *Object Lock, Glacier, S3 Intelligent-Tiering, Lifecycle policy의 일부 고급 동작*은 부재 또는 제한이 있다. compliance 목적의 immutable storage(WORM)가 핵심 요구라면 R2를 그대로 받아쓰지 못할 수 있다.
- 강한 region lock 워크로드에서는 R2의 글로벌 분산이 정책과 충돌한다. 한국 데이터를 한국 안에서만 보관해야 한다면 jurisdiction 옵션과 조합으로도 완전한 해결이 어렵다. 5장의 컴플라이언스 축에서 빨간불이 켜지는 자리.

이 한계를 알고 옮기면 된다. *모든 S3를 옮기라는 말이 아니다.* egress가 큰 버킷부터, enterprise 기능에 매여 있지 않은 자산부터, 점진적으로 옮긴다. 14장의 8단계에서 데이터 이전의 첫 줄에 항상 "egress 큰 버킷부터"가 적혀 있는 게 우연이 아니다.

#### multipart·presigned·외부 origin — 실무 패턴

채팅방 이야기로 다시 돌아오자. 사용자가 큰 이미지(예: 8MB 스크린샷)를 첨부 파일로 올리면 어떻게 받는가. 두 가지 길이 있다.

**첫째, 클라이언트가 Worker로 보내고 Worker가 R2에 쓴다.** 단순하지만 Worker의 요청 본문 크기 한도(plan에 따라 다르지만 대체로 100MB 수준)와 CPU time 한도를 의식해야 한다. 작은 파일에는 깔끔한 선택.

```typescript
// /upload — 작은 첨부 (~10MB 미만)
app.post('/upload', async (c) => {
  const roomId = c.req.query('room');
  const key = `chat/${roomId}/${crypto.randomUUID()}`;
  await c.env.ATTACHMENTS.put(key, c.req.raw.body, {
    httpMetadata: { contentType: c.req.header('content-type') },
  });
  return c.json({ key });
});
```

**둘째, presigned URL을 발급해 클라이언트가 R2에 직접 PUT한다.** 큰 파일에 적합한 표준 패턴. Worker는 토큰 발급만 한다 — 본문이 흐르지 않는다.

```typescript
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

app.post('/presign', async (c) => {
  const r2 = new S3Client({
    region: 'auto',
    endpoint: `https://${c.env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
    credentials: {
      accessKeyId: c.env.R2_ACCESS_KEY_ID,
      secretAccessKey: c.env.R2_SECRET_ACCESS_KEY,
    },
  });

  const roomId = c.req.query('room');
  const key = `chat/${roomId}/${crypto.randomUUID()}`;

  const url = await getSignedUrl(
    r2,
    new PutObjectCommand({
      Bucket: 'toby-shop-attachments',
      Key: key,
      ContentType: c.req.query('type') ?? 'application/octet-stream',
    }),
    { expiresIn: 600 },
  );

  return c.json({ url, key });
});
```

큰 파일·다량 업로드에는 multipart upload도 그대로 쓸 수 있다. R2 binding은 multipart API를 직접 노출한다.

```typescript
// 큰 파일 multipart — Worker binding 방식.
const upload = await env.ATTACHMENTS.createMultipartUpload(key);
const part1 = await upload.uploadPart(1, chunk1);
const part2 = await upload.uploadPart(2, chunk2);
await upload.complete([part1, part2]);
```

세 길 중 자기 워크로드에 맞는 자리를 고르자. 작은 첨부는 binding 직접 PUT, 큰 미디어는 presigned로 클라이언트 직접 업로드, 분할이 필요하면 multipart. 채팅방 첨부 같은 시나리오에서는 *5MB 미만은 직접, 그 이상은 presigned*가 흔한 분기점이다.

자, R2까지 손에 쥐었으니 마지막 한 조각이 남았다. 요청 단위 캐시, Cache API.

### Cache API — CloudFront behavior가 코드로 들어왔다고 생각하자

#### Cache API가 채우는 자리

Cache API는 Workers 안에서 직접 캐시를 조작하는 표준 인터페이스다. CloudFront의 behavior 설정이 *대시보드에서 yaml로 적는 일*이라면, Cache API는 *Worker 코드 안에서 한 줄로 적는 일*이다. 자유도가 다르다.

```typescript
const cache = caches.default;

// 캐시 hit 시도.
const cached = await cache.match(request);
if (cached) return cached;

// 미스면 origin에서 가져와서 캐시에 넣는다.
const upstream = await fetch(originUrl);
const response = new Response(upstream.body, upstream);
response.headers.set('cache-control', 'public, max-age=300');
await cache.put(request, response.clone());
return response;
```

`caches.default`가 한 PoP에 있는 ephemeral 캐시 핸들이다. `match`로 hit를 시도하고, 미스면 `put`으로 채운다. 응답의 `Cache-Control` 헤더가 TTL을 결정한다. CloudFront에서 behavior에 TTL을 박는 것과 같은 일을 코드로 한다.

CloudFront와 결정적으로 다른 한 가지가 있다. *분기 로직을 마음껏 짤 수 있다.* 사용자 plan에 따라 다른 캐시 키를 쓴다거나, 특정 헤더가 있을 때만 캐싱을 우회한다거나, 응답 본문을 일부 변형해서 캐시에 넣는다거나. CloudFront에서 Lambda@Edge로 풀던 자리가 Worker 안에 자연스럽게 들어와 있다. 4장에서 살펴본 *Lambda@Edge가 Workers에 사실상 흡수됐다*는 매핑의 본문이 여기에 보인다.

#### TTL·Vary·purge — 운영의 세 줄

Cache API를 운영에서 다룰 때 짚어야 할 세 가지가 있다.

**TTL은 응답 헤더로.** `Cache-Control: public, max-age=300` 한 줄이 5분 캐시를 만든다. 응답마다 다른 TTL을 동적으로 잡을 수 있다. CloudFront의 behavior 단위 일괄 설정이 *유연한 코드 단위 결정*이 된다. 다만 너무 짧은 TTL(예: 10초)은 cache thrash를 일으켜 origin 요청이 거의 안 줄어들 수 있다. *짚어두자.*

**Vary는 캐시 키 분기.** `Vary: Accept-Encoding`은 익숙하지만, 사용자별 캐시·plan별 캐시를 짜려면 캐시 키 자체를 손으로 만드는 편이 낫다. `cache.match(request)` 대신 `cache.match(new Request('https://cache.local/' + customKey))` 식으로 가짜 URL을 키로 쓴다. 헤더 기반 분기보다 명시적이고 디버깅하기 쉽다.

**Purge는 Cache API 자체로는 거의 못 한다.** Cache API의 TTL이 끝나야 자동으로 빠지거나, Cloudflare 대시보드/API의 cache purge로 일괄 비운다. *세밀한 single-key purge는 거의 손에 잡히지 않는다.* 이게 가장 큰 한계다. 빈번하게 invalidate해야 하는 데이터라면 Cache API보다 KV가 더 잘 맞을 수 있다 — KV는 명시적 delete가 있다.

#### Cache API가 빛나는 자리, 무너지는 자리

빛나는 자리부터 적자. *외부 API 응답의 짧은 캐시*가 가장 자연스럽다. 환율·날씨·검색 결과처럼 5분 정도 stale해도 되는 데이터를 origin에 매번 부르지 말고 PoP 단위로 받아 둔다. Worker가 PoP에서 응답하니까 cache hit는 PoP-local에서 끝난다 — 사용자가 도쿄에 있으면 도쿄 PoP의 캐시에서 미리 굳어 있던 응답이 즉시 떠난다.

무너지는 자리도 분명하다.

- *PoP-local* 캐시다. 글로벌 균등 캐시가 아니다. 도쿄 PoP에서 한 번 hit가 들어왔다고 서울 PoP의 캐시가 따라 채워지지 않는다. 글로벌 일관성이 필요한 캐시에는 KV가 맞다.
- TTL이 끝나면 자동 expire이지만 *그 사이에 데이터를 비우는 단일 키 purge*가 약하다. invalidate-heavy 워크로드에는 안 맞다.
- 응답 크기가 큰 자산(수십 MB의 비디오 chunk)은 Cache API가 처리하긴 하지만, 그런 패턴이라면 *Cloudflare CDN 자체*에 맡기는 편이 낫다. CDN 단의 캐시는 더 큰 캐시 풀을 가진다.

요약하면 Cache API는 *작은 응답·짧은 TTL·요청 단위 분기 로직*에 잘 맞고, *글로벌 일관 캐시·세밀한 invalidate·큰 자산*에는 다른 도구로 가는 편이 낫다. KV는 글로벌 일관·invalidate에, R2는 큰 자산에, CDN은 정적 자산 캐시에. 각자의 자리가 있다.

### 의사결정 플로차트(완성판) — 6갈래로 정리한다

7장 끝에서 KV·D1까지 그렸던 의사결정 플로차트를 8장 여기서 6갈래로 닫자. 자기 워크로드의 데이터 형상을 보고 한 번에 어디로 갈지 묻는 짧은 질문 묶음이다.

```
시작: 이 데이터의 형상은?
│
├─ 1) 큰 파일·미디어·백업 (객체 storage)
│      → R2 (egress free + S3 호환)
│
├─ 2) 짧은 응답을 PoP-local 캐시 (요청 단위 ephemeral)
│      → Cache API (TTL 짧음, invalidate 적음)
│
├─ 3) read-heavy + 글로벌 일관 + eventual OK
│      세션·플래그·API key·설정
│      → KV (60초 전파, per-key 1 write/s OK)
│
├─ 4) SQL 쿼리·관계형·moderate write
│      사용자·주문·게시글
│      → D1 + Drizzle (10GB 한도, sustained write 500~2k/s)
│
├─ 5) transactional·serializable·per-entity 격리
│      재고·예약·턴 게임·채팅방·실시간 협업·rate limit
│      → Durable Objects (+ WebSocket Hibernation)
│
└─ 6) write-heavy(2k+ TPS) + 기존 RDS/Aurora 살리기
       → Hyperdrive (10장)
```

`toby-shop` 시나리오에 대입해 보자. 상품 카탈로그 → R2(이미지) + Cache API(검색 응답 단기 캐시). 사용자 세션 → KV. 주문 도메인 → 5장에서 보류로 분류한 자리, DO + Hyperdrive 후보. 고객지원 채팅 → DO + WebSocket Hibernation. 첨부 파일 → R2. *이 6갈래가 자기 시스템 안에 한 줄씩 자리 잡는다.*

### 실습 — `toby-shop` 고객지원 채팅방 한 사이클

이번 챕터의 누적 산출물은 분명하다. `toby-shop`에 새 Worker 한 개를 분기로 추가한다. 고객지원 채팅방. WebSocket Hibernation으로 연결을 받고, 메시지는 DO storage에 쌓고, 첨부는 R2 presigned URL로 받는다.

```
toby-shop/
├── apps/
│   ├── api/                  # 6·7장에서 만든 Worker 1
│   └── support-chat/         # 8장 신규 — Worker 2
│       ├── src/
│       │   ├── index.ts
│       │   ├── chat-room.ts
│       │   └── presign.ts
│       └── wrangler.toml
└── packages/...
```

핵심 진입점.

```typescript
// apps/support-chat/src/index.ts
import { Hono } from 'hono';
import { presignAttachment } from './presign';
export { ChatRoom } from './chat-room';

type Env = {
  CHAT: DurableObjectNamespace;
  ATTACHMENTS: R2Bucket;
  R2_ACCOUNT_ID: string;
  R2_ACCESS_KEY_ID: string;
  R2_SECRET_ACCESS_KEY: string;
};

const app = new Hono<{ Bindings: Env }>();

// WebSocket — 한 방 한 인스턴스.
app.get('/ws', async (c) => {
  const room = c.req.query('room') ?? 'lobby';
  const id = c.env.CHAT.idFromName(`room:${room}`);
  const stub = c.env.CHAT.get(id);
  return stub.fetch(c.req.raw);
});

// 첨부 — presigned URL 발급.
app.post('/attach', async (c) => {
  const room = c.req.query('room') ?? 'lobby';
  const type = c.req.query('type') ?? 'application/octet-stream';
  const { url, key } = await presignAttachment(c.env, room, type);
  return c.json({ url, key });
});

// 첨부 다운로드 — Worker가 R2 binding으로 직접 응답.
app.get('/attach/:key{.+}', async (c) => {
  const obj = await c.env.ATTACHMENTS.get(c.req.param('key'));
  if (obj === null) return c.notFound();

  const headers = new Headers();
  obj.writeHttpMetadata(headers);
  headers.set('cache-control', 'public, max-age=86400, immutable');
  return new Response(obj.body, { headers });
});

export default app;
```

이 한 사이클이 동작하면 8장의 누적 결과가 손에 남는다. 6·7장의 사용자 API는 그대로 두고, 옆에 채팅 Worker가 새로 분기로 자리 잡는다. 같은 모노레포·같은 도메인의 다른 path. 두 Worker가 다른 모양의 데이터를 다룬다 — 하나는 D1 + KV의 사용자 도메인, 하나는 DO + R2의 실시간 도메인. *5장에서 그렸던 결정 매트릭스가 코드로 닫히는 순간이다.*

### 이 기술이 무너지는 자리

광고가 아니라는 약속을 8장에서도 지키자. DO·R2·Cache API 각자가 무너지는 자리를 정직하게 적는다.

- **DO의 lock-in 위험.** Workers 코드 자체는 Web standards로 portable하지만 *Durable Objects API와 storage·migration 모델은 Cloudflare 고유다.* DO 위에 채팅·재고·실시간 협업을 깊게 쌓을수록 다른 클라우드로 옮기기가 어려워진다. 같은 actor 모델을 AWS에서 흉내내려면 ECS + DynamoDB + ElastiCache 조합이 필요한데, *코드 모양이 다르다.* 13장에서 본격적으로 다루지만, DO 의존이 깊은 워크로드는 그 자체로 vendor lock-in의 깊이가 깊다는 사실을 알고 가자.
- **DO의 단일 인스턴스 모델은 처리량의 자연스러운 상한이다.** 한 자원에 초당 1만 write가 들어와야 한다면 단일 DO로는 무리다. 1차 샤딩(`{name}-{shardN}`)이나 write-heavy는 Hyperdrive 너머의 Postgres로 보내는 분기가 필요하다. *모든 strong consistency가 DO에 들어가야 하는 게 아니다.*
- **R2의 enterprise 기능 부재.** Object Lock(WORM), 일부 Lifecycle 동작, S3 Intelligent-Tiering, 일부 Glacier 전환 기능이 부재 또는 제한이다. compliance·archival 요구가 강한 자산은 S3에 남기는 편이 낫다. R2를 *primary 미디어·backup·LLM 데이터셋*에 쓰고, 강한 immutability가 필요한 부분은 S3와 병행하는 패턴이 가장 안전하다.
- **R2 inbound는 AWS egress다.** 처음 옮길 때 한 번 큰 청구서를 받는다. 점진적으로 옮기거나, 옮기는 시점을 회계 분기에 맞춰 두자. *모르고 옮기면 깜짝 놀란다.*
- **Cache API는 PoP-local이고 invalidate가 약하다.** 글로벌 일관 캐시가 필요하면 KV로 가고, 세밀한 single-key purge가 필요하면 KV·D1을 쓰는 편이 낫다. Cache API는 *짧은 TTL·요청 단위 분기*에 빛나는 도구다.
- **WebSocket Hibernation의 비용 모델은 "메시지가 적게 오가는 idle 시간이 긴" 워크로드에 최적이다.** 분당 수만 건이 폭주하는 라이브 스트림 채팅에서는 메시지 수 과금이 누적돼 절감 효과가 줄어든다. 트래픽 형상부터 본다.
- **DO migrations는 강제다.** 익숙해지면 자연스럽지만, 처음에는 짜증을 부른다. 클래스 이름을 함부로 바꾸지 말고, 새 클래스를 추가할 때마다 새 태그를 붙이는 습관을 들이자.

이 일곱 줄이 8장의 정직한 마무리다. *DO·R2·Cache API 모두 만능이 아니다.* 5장의 결정 프레임을 다시 들고 와, 자기 워크로드 위에 한 번 더 올려 보자.

### 다음 장 예고

데이터 두 챕터로 백엔드 깊이에 들어왔으니 한 번 호흡을 환기할 차례다. 9장에서는 프론트로 점프한다. Pages가 maintenance 모드가 된 지금, 새 Next.js 앱은 어디에 배포해야 하는가. OpenNext on Cloudflare가 어디까지 production을 견디는가. velopert(veltrends)가 Pages → Vercel로 회귀한 솔직한 사례를 옆에 두고, *모든 Next.js 앱이 이전 대상은 아니다*라는 정직한 의사결정선을 그려 본다. `toby-shop`의 상점 프론트(SSR + 이미지 최적화 + ISR 한 페이지)를 Workers Static Assets에 올려 7장 사용자 API와 8장 채팅 Worker 둘 다와 연동되는 그림을 손에 쥐자.

자, 다음 장에서 만나자.

---


## 9장. Next.js on Cloudflare — Workers Static Assets·OpenNext의 현실

AWS Amplify Hosting에 올려둔 Next.js 상점 프론트가 한 개 있다고 해보자. 토큰 한 줄 바꾸면 자동 배포되고, Lambda@Edge도 알아서 깔리고, 큰 사고 없이 1년쯤 잘 굴러갔다. 그런데 어느 날 사용자가 도쿄·서울·LA·암스테르담에 흩어져 있다는 사실이 문제로 떠오른다. 미주 사용자에게서 "장바구니 페이지가 답답하다"는 컴플레인이 들어온다. CloudFront 캐시 hit률은 나쁘지 않은데, SSR 페이지 한 번에 800ms를 넘는 일이 잦다. 한국 리전에 박힌 Lambda@Edge가 미국에서 콜드스타트할 때마다 사용자가 1초씩 기다린다. 옮겨야 할까? 어디로 옮겨야 할까?

7장에서 D1과 KV를 손에 쥐고, 8장에서 Durable Objects와 R2까지 들고 왔다. 백엔드 깊이로 두 챕터를 내달렸으니 이번 장은 호흡을 한 번 환기하자. 프론트 이야기다. Next.js 앱을 Cloudflare 위에 어떻게 올릴 것인가. 답이 한 줄로 정리되지 않는다는 사실부터 짚어둬야 한다 — 2025년 4월 이후로 Cloudflare의 프론트 호스팅은 *움직이고 있는 풍경*이기 때문이다.

이 장에서 손에 쥐고 가야 할 것은 세 가지다. 첫째, Pages가 Workers Static Assets로 흡수된 흐름을 이해한다. 둘째, `@opennextjs/cloudflare` 어댑터로 Next.js 14/15 앱을 어떻게 올리는지 단계별로 따라간다. 셋째, *어떤 Next.js 앱은 옮겨도 되고 어떤 앱은 미루는 게 옳은지* 의사결정선을 그린다. 5장에서 만든 결정 프레임을 프론트에 한 번 더 적용하는 셈이다.

자, Pages 이야기부터 살펴보자.

### Pages가 사라진 자리에 Workers Static Assets가 들어왔다

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

### OpenNext가 1.0-beta라는 한 줄에서 멈칫한다면

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

### 따라해보자 — Next.js 14 상점 프론트를 올리기까지

말로만 풀면 멀리 있는 이야기처럼 들린다. `toby-shop`의 상점 프론트(Next.js 14)를 손가락으로 한 번 올려보자. 6장에서 만든 사용자 API와 7장에서 D1으로 옮긴 프로필 API가 이미 살아 있다고 가정하자. 이번 장의 목표는 그 위에 *Worker 한 개*를 더 띄우는 것이다 — Next.js 풀 기능이 도는 SSR Worker.

#### 0단계 — 프로젝트 만들기

새 Next.js 앱을 만든다. 평범하다.

```bash
pnpm create next-app@latest toby-shop-web
# TypeScript: Yes
# App Router: Yes
# Tailwind: 취향대로
```

여기까지는 Vercel과 똑같다. 이제 Cloudflare용 어댑터를 붙이자.

#### 1단계 — `@opennextjs/cloudflare` 추가

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

#### 2단계 — `wrangler.toml`로 묶기

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

#### 3단계 — 빌드와 로컬 미리보기

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

#### 4단계 — 배포

```bash
pnpm opennextjs-cloudflare deploy
```

또는 `wrangler deploy`. 1~2분 안에 `toby-shop-web.<sub>.workers.dev` 도메인에 사이트가 올라온다. 7장에서 만든 사용자 API가 같은 계정에 있으면 같은 KV·D1 namespace를 공유할 수도 있다. 모노레포라면 더 자연스럽다 — `apps/web`이 `wrangler.toml` 한 장을 가지고, `apps/api`도 자기 `wrangler.toml`을 가지고, 둘이 같은 D1을 본다. 4장에서 권장했던 모노레포 구조가 이 자리에서 자연스럽게 동작한다.

여기까지 따라왔다면 Next.js 14 앱 한 개가 Cloudflare 글로벌 PoP에 깔린 셈이다. 한국에서 접속하면 도쿄 PoP, LA에서 접속하면 LA PoP. SSR이 가까운 PoP에서 돌고, 정적 자원은 같은 PoP의 Workers Static Assets에서 나간다.

#### 5단계 — Preview deploy 구성하기

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

### 라우트별 runtime 선택 — 무엇을 어디서 돌릴까

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

### 이미지 최적화 — `next/image` vs Cloudflare Images

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

### AWS Amplify·Vercel과의 비용·DX 비교

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

### Vinext — "곧 등장할 또 하나"라는 풍경

OpenNext가 사실상 표준이 된 자리에서, Cloudflare가 직접 만드는 또 하나의 라인이 보이기 시작했다. *Vinext*다. 이름은 Vite + Next의 합성어 같고, 실제로도 Vite 플러그인 형태로 Next.js 호환을 제공하는 어댑터다. GitHub의 `cloudflare/vinext` 리포에서 진행 상황을 추적할 수 있다.

이 풍경은 정직하게 *불확실성*을 안고 있다. 책 집필 시점(2026년 5월)에서는 실험적 라인이고, OpenNext와 별개로 굴러간다. *책 집필 시점에 사실 확인 필요*라는 면책을 한 줄 박아둔다 — 이 책이 출간되고 1년 뒤에 Vinext가 OpenNext를 대체할지, 아니면 두 라인이 공존할지, 아니면 조용히 사라질지 지금은 알 수 없다.

그렇다면 우리가 어떻게 해야 할까. 두 가지 권장사항이다.

첫째, **새 프로젝트는 OpenNext로 시작한다.** 1.0-beta라는 라벨이 붙어 있어도 사실상 표준이고 사례도 많다. 안전하다.

둘째, **Vinext의 진행 상황은 분기마다 한 번 살핀다.** Cloudflare 공식 블로그·OpenNext 뉴스·GitHub 리포 README. 이 셋이 Vinext의 위상이 바뀔 때 가장 먼저 신호를 준다. 만약 Cloudflare가 Vinext를 1순위로 밀기 시작하고 OpenNext 어댑터의 유지보수가 줄어드는 신호가 보이면, 그때 옮길 결정을 한다.

이 풍경 자체가 Cloudflare 생태계의 변동성을 보여준다. 부록 E에서 "책 이후 추적 가이드"를 별도로 둔 이유다 — Cloudflare는 분기마다 풍경이 바뀐다. Vinext만이 아니다. Workers Containers GPU·Vectorize hybrid search·Dynamic Workers 같은 영역도 마찬가지다. 한 번 책에 박아둔 가이드를 1년이 지나도 그대로 믿으면 위험하다. *분기마다 한 번씩 공식 페이지를 다시 보자.*

### 어떤 Next.js 앱은 옮기지 말자

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

### OpenNext가 무너지는 자리

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

### 마무리

Next.js를 Cloudflare에 올리는 길을 9장에서 한 번 짚어 봤다. Pages가 Workers Static Assets로 흡수된 흐름, `@opennextjs/cloudflare` 어댑터로 Next 14/15를 올리는 단계별 명령, 라우트별 runtime 선택의 함정, 이미지 최적화는 Cloudflare Images로 분리하는 권장 패턴, AWS Amplify·Vercel과의 DX·비용 비교, 그리고 Vinext라는 곧 등장할 풍경. 호흡 환기 챕터답게 따라 하기 친화적으로 풀었지만, 결정 자체는 결코 가볍지 않다.

이 한 장으로 우리는 한 가지 그림을 손에 쥐었다. **Workers + Hono로 만든 백엔드 API 옆에, OpenNext로 빌드된 Next.js 프론트가 같은 Cloudflare 계정 안에서 한 단위로 묶여 돈다.** `toby-shop`은 이제 Worker 한 개(API), Worker 한 개(채팅 DO), Web 한 개(Next.js 상점)로 구성된다. 같은 D1·KV·R2를 공유한다. 이 모양이 4장 매핑 카탈로그에서 약속했던 모노레포 구조의 자연스러운 결과다.

물론 9장의 이 그림에도 큰 한계가 하나 있다. *우리는 아직 RDS를 만지지 못했다.* `toby-shop`의 주문 도메인은 여전히 Aurora Postgres 같은 곳에 있을 가능성이 높고, 그걸 옮기는 일은 위험이 크다. 옮기지 않고도 edge에서 빠르게 쓸 길이 있다면 어떻겠는가? 다음 장에서 그 답을 손에 쥔다. **10장 — Hyperdrive로 RDS를 그대로 살려두기**. 점진 마이그레이션의 가장 risk-low한 첫 발걸음을 다음 페이지에서 살펴보자.

---


## 10장. Hyperdrive로 RDS를 그대로 살려두기 — 가장 risk-low한 첫 발걸음

회사에 이런 RDS 한 대가 있다고 해보자. Aurora Postgres, 도쿄 리전, 안에는 5년 치 주문 데이터가 들어 있다. 마이그레이션도 한두 번 했고, 인덱스는 손때가 묻을 대로 묻었으며, 야심한 새벽에 한 번씩 backup snapshot을 떠두는 쿠론 잡까지 정성스럽게 굴러간다. 누구도 이 DB를 옮기자고 말하지 않는다. 옮기자고 말하는 사람이 있다면, 옮기는 작업의 무게를 모르거나 모른 척하는 쪽이다.

그런데 이 위에 얹힌 Spring Boot API의 해외 사용자들이 점점 불편을 호소한다. 동남아·남미·유럽 어디에서 들어와도 응답이 답답하게 느껴진다. p95가 800ms를 넘는다. CloudFront만으로는 동적 API의 지연이 풀리지 않는다. 그럼 Lambda@Edge로? 그쪽은 콜드스타트가 더 끔찍하다는 보고가 도쿄 외 리전에서 올라온다. 그렇다면 어떻게 해야 할까.

DB는 그대로 둔다. 그건 협상 불가다. 옮길 것은 컴퓨트 한 겹뿐이다. RDS는 도쿄에 그대로 있는 채로, 사용자에게 가까운 PoP에서 도는 코드가 RDS를 빠르게 부를 수만 있으면 된다. 이 한 줄짜리 요구가 지금부터 풀어볼 문제다. 그리고 그 답이 Hyperdrive다.

### 7번의 round-trip이 글로벌에서 어떻게 누적되는가

먼저 왜 이 문제가 어려운지부터 짚고 가자. Workers에서 RDS로 곧장 TCP 연결을 여는 그림을 떠올려 보자. 사실 이 그림 자체가 처음부터 막힌다. Workers는 V8 isolate 위에서 도는 런타임이고, 임의 TCP socket을 여는 자유는 제한돼 있다. 그러면 우리가 알던 `pg`나 `mysql2` 라이브러리는 어떻게 도는가? Cloudflare는 Workers 안에서 외부 DB로의 TCP 연결을 자체 게이트웨이를 거쳐 흘려보낸다. 즉 Workers 코드는 표준 라이브러리를 쓰는 것처럼 보이지만, 실제로는 Cloudflare 인프라 한 겹을 거쳐 DB에 닿는다.

여기까지는 그래도 풀리는 그림이다. 진짜 문제는 그다음부터다. Postgres 한 번 부르려면 무엇이 일어나는지 따져보자.

- TCP handshake — 1 round-trip
- TLS handshake — 3 round-trip
- DB authentication (SCRAM-SHA-256 같은 방식) — 3 round-trip

다 합치면 7번이다. 한 번의 SQL 쿼리를 던지기 위해 미리 7번의 왕복을 해야 한다. 같은 리전이라면 이 비용이 작다. PoP와 RDS가 옆방에 있으면 7번을 다 합쳐도 수 ms 안쪽이다.

그렇다면 글로벌에서는 어떨까. 상파울루 PoP에서 도쿄 RDS까지 한 번 왕복이 250ms라고 해보자. 7번이면 1.75초다. 이걸 매 요청마다 쌓는다. 사용자가 페이지 하나를 띄우는 동안 API가 세 번 호출된다면, 5초가 그냥 핸드셰이크에 사라진다. 실제 SQL이 도는 시간은 그 안에 묻혀 보이지도 않는다. 끔찍한 일이다.

그렇다면 어떻게 해야 할까. 답은 이미 RDS Proxy나 PgBouncer 같은 도구가 알려준 적이 있다. **연결을 미리 맺어두고, 풀로 묶고, 요청이 오면 풀에서 하나 꺼내준다.** 다만 그 풀이 글로벌에 깔려 있어야 한다. 상파울루 사용자는 상파울루 근처 풀에서 꺼내고, 시드니 사용자는 시드니 근처 풀에서 꺼내야 한다. 그게 Hyperdrive다.

### Hyperdrive는 DB가 아니다 — 이름의 함정부터 풀자

처음 Hyperdrive라는 이름을 들으면 새로운 DB 제품처럼 들린다. D1 옆에 또 하나 있는 데이터베이스인가 하는 의심이 든다. 그렇지 않다. Hyperdrive는 DB가 아니라 **글로벌 connection pool + 쿼리 캐시**다. DB는 여전히 우리가 가진 RDS·Aurora·Neon·Supabase 그대로다.

기억해두자. Hyperdrive는 우리 RDS 앞에 글로벌하게 깔려 있는 한 겹의 도우미다. 이 한 겹이 무엇을 해주는가.

첫째, 7번의 round-trip을 흡수한다. Hyperdrive는 우리 DB와 미리 연결을 맺어두고 풀에 쥐고 있다. Worker가 SQL을 던지면, Hyperdrive는 풀에서 이미 인증이 끝난 연결 하나를 꺼내 그걸로 쿼리를 보낸다. Worker 입장에서는 핸드셰이크가 사실상 0번이 된 셈이다.

둘째, 쿼리 결과를 일정 조건에서 캐시한다. SELECT 쿼리, 같은 SQL · 같은 파라미터 · TTL 안쪽이라면 같은 결과를 PoP 가까이에서 돌려준다. CDN이 정적 자산을 캐시하는 모델을 SQL 응답에 적용한 것이다. 단 이 캐시는 강한 일관성이 필요한 쿼리에는 위험하다 — 그래서 끄거나, TTL을 짧게 두거나, 캐시 안 할 쿼리를 따로 표시하는 식으로 조절해야 한다.

셋째, **transaction mode**로 동작한다. 한 트랜잭션 동안에는 단일 연결을 점유했다가, COMMIT 또는 ROLLBACK이 끝나면 풀로 반환한다. 이 동작이 무엇을 의미하는지가 뒤에서 한 번 더 등장한다. 일단 머리에 새겨두자 — Hyperdrive는 트랜잭션 단위로 연결을 빌려주고 거두어들인다.

이걸 Spring 개발자의 익숙한 그림으로 바꾸면 한 페이지로 정리된다.

#### JDBC HikariCP ↔ Hyperdrive — Spring 개발자의 다리

Spring Boot 위에서 JDBC를 써본 사람이라면 HikariCP를 모를 수 없다. `application.yml` 어딘가에 `maximum-pool-size: 20` 같은 한 줄이 박혀 있고, 트랜잭션이 시작되면 풀에서 connection을 빌려와 `@Transactional` 메서드 끝까지 가지고 있다가 COMMIT 후 풀로 반환한다. 한 JVM 안에 풀이 하나 있고, 그 풀이 RDS와 미리 연결을 맺어둔 형태다.

Hyperdrive는 이 모델을 **글로벌**로 확장한 것이다. 한 JVM이 아니라 Cloudflare PoP들이 함께 풀을 운영한다. Worker가 트랜잭션을 시작하면, 가까운 PoP의 Hyperdrive가 미리 맺어둔 연결 하나를 빌려준다. 트랜잭션이 끝나면 다시 풀로 돌아간다. JDBC URL이 바뀐 셈이다 — `jdbc:postgresql://aurora.aws...`가 `postgresql://hyperdrive.cloudflare...`로 옮겨갔을 뿐, 그 너머의 DB는 그대로다.

다른 점도 있다. HikariCP는 한 JVM 안의 풀이라 JVM이 죽으면 풀도 같이 사라진다. Hyperdrive의 풀은 우리 코드가 아닌 Cloudflare 쪽에서 관리한다. 그래서 Worker 한 인스턴스가 죽고 살고는 풀과 무관하다. 이 구조는 우리가 Worker를 글로벌에 흩뿌려도 DB의 max_connections를 폭파시키지 않게 막아준다. JVM 100개를 띄우면 connection 2,000개가 RDS로 향하지만, Worker isolate 100,000개가 떠도 RDS로 가는 실제 연결은 Hyperdrive 풀 크기에 묶인다. 이건 작은 차이가 아니다 — RDS 운영자에게 가장 끔찍한 그림(connection storm)이 자연스럽게 차단되는 셈이다.

물론 다른 점도 있다. `@Transactional(propagation = REQUIRES_NEW)` 같은 정교한 propagation 모델은 Hyperdrive에 등가물이 없다. 트랜잭션 경계는 우리가 SQL 레벨에서 BEGIN·COMMIT으로 직접 그어야 한다. Drizzle이나 Kysely 같은 라이브러리가 그 경계를 함수로 감싸 비슷한 DX를 주긴 하지만, Spring의 AOP 마법은 없다. 기억해두자 — 트랜잭션 경계는 명시적이다.

### 가장 risk-low한 첫 발걸음

이 책 14장에서 다룰 마이그레이션 8단계 중, 컴퓨트를 옮기는 단계가 사실은 가장 까다롭다. 코드의 런타임이 바뀌는 일이라 호환성 문제가 깊은 자리에서 튀어나온다. 그런데 Hyperdrive는 그 여정을 한 단계 가볍게 만든다. 어떻게? **데이터는 그대로 두고, 컴퓨트만 가져오기 때문이다.**

이 그림이 왜 안전한지 따져보자.

먼저 데이터가 움직이지 않는다. 옮기지 않은 데이터는 깨질 일이 없다. RDS의 백업·복제·모니터링·DBA 운영 절차가 그대로 돈다. 사고가 나도 기존 절차로 복구된다. 옮기는 일에 비하면 위험이 한 자릿수 낮다.

다음으로 롤백이 단순하다. Hyperdrive 바인딩을 통한 호출이 마음에 안 들면, Worker의 connection string을 RDS 직접 호출로 바꾸기만 하면 된다. 데이터는 한 번도 움직이지 않았다. RDS는 여전히 거기에 있다. 롤백이 "DNS 한 번 바꾸기" 수준의 무게다.

또 하나, 실측 효과가 빠르게 나온다. 7번의 round-trip이 흡수되는 구조이기 때문에, 해외 사용자의 p95 응답시간이 거의 즉시 줄어든다. 도쿄 RDS · 상파울루 사용자 시나리오에서 글자 그대로 800ms대 응답이 200~300ms대로 떨어지는 사례가 보고된다 (정확한 절감폭은 워크로드와 PoP 위치에 따라 다르므로 직접 측정해 보는 편이 낫다). 비용 측면에서도, 2025년 가격 정책 변경 이후 무료 plan에서도 Hyperdrive를 쓸 수 있게 됐다. 도입 비용이 사실상 0이다.

이 셋을 함께 보면, Hyperdrive 도입은 점진 마이그레이션의 **첫 발걸음**으로 가장 잘 어울린다. 위험은 낮고, 효과는 빠르고, 롤백은 쉽다. 이 책이 권하는 하이브리드 패턴 — DB는 AWS, 컴퓨트는 Cloudflare — 의 핵심 도구가 바로 이것이다.

### 손으로 한 번 붙여보자 — Aurora Postgres + Hyperdrive

말로만 풀면 멀리 있는 이야기처럼 들린다. 손가락을 한 번 움직여 보자. 가상의 시나리오를 가정한다.

상황 — `toby-shop`이라는 e-commerce SaaS가 있다. 주문 도메인은 Aurora Postgres에 들어 있다. 우리는 이 RDS를 그대로 두고, Workers에서 주문을 조회하는 API 한 개만 edge에서 빠르게 띄우고 싶다.

#### 0단계 — RDS 쪽 준비

먼저 점검할 것이 두 가지 있다.

첫째, RDS가 Cloudflare에서 닿을 수 있어야 한다. 가장 단순한 방법은 publicly accessible 옵션을 켜고 Security Group의 inbound 5432를 Cloudflare egress IP 범위에서 허용하는 것이다. 정확한 IP 목록은 Cloudflare 공식 문서에 정리돼 있다 — 그대로 복사해 SG에 넣자. 이 방식이 찜찜하다면 두 번째 방법이 있다 — Cloudflare Tunnel(`cloudflared`)을 EC2 한 대에 띄워 RDS로 가는 길을 outbound-only로 여는 것이다. 11장에서 이 패턴을 본격 다룬다. 일단 지금은 publicly accessible + IP 화이트리스트로 진행하자.

둘째, SSL 연결이다. RDS는 기본적으로 SSL을 요구한다. Hyperdrive 설정에서 SSL 모드를 켜주면 된다. 인증서까지 검증하고 싶다면 RDS의 CA 번들을 Hyperdrive에 등록할 수 있다 (운영 환경에서는 검증하는 편이 낫다).

#### 1단계 — Hyperdrive 만들기

`wrangler` 한 줄이면 된다.

```bash
wrangler hyperdrive create toby-shop-orders \
  --connection-string="postgresql://USER:PASS@orders.cluster-xxx.ap-northeast-1.rds.amazonaws.com:5432/orders?sslmode=require"
```

응답으로 Hyperdrive 인스턴스의 ID가 나온다. 이 ID를 `wrangler.toml`(또는 `wrangler.jsonc`)에 바인딩으로 적어준다.

```toml
name = "toby-shop-orders-api"
main = "src/index.ts"
compatibility_date = "2026-04-01"

[[hyperdrive]]
binding = "ORDERS_DB"
id = "your-hyperdrive-id-here"
```

이 한 줄이 끝이다. 이제 Worker 코드 안에서 `env.ORDERS_DB.connectionString` 같은 형태로 connection string이 주입된다. Spring 개발자의 머릿속으로 옮겨 말하면 — `application.yml`에 `spring.datasource.url`을 적은 것과 같다. 다른 점은, 이 connection string이 RDS로 직접 가지 않고 Hyperdrive를 거쳐 RDS로 흐른다는 것뿐이다.

기억해두자 — connection string에는 production credential이 들어 있다. `wrangler secret`으로 관리하거나, Hyperdrive 자체가 제공하는 credential 보호 모드를 쓰는 편이 낫다. 평문으로 `wrangler.toml`에 박는 일은 끔찍한 일이다.

#### 2단계 — Hono + postgres-js로 코드 짜기

Workers에서 Postgres를 부를 때 가장 무난한 라이브러리가 `postgres`(postgres-js)다. Drizzle을 같이 쓰면 타입 안전성까지 챙긴다. 코드는 이렇다.

```ts
import { Hono } from "hono";
import postgres from "postgres";
import { drizzle } from "drizzle-orm/postgres-js";
import { orders } from "./schema";

type Bindings = {
  ORDERS_DB: Hyperdrive;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get("/orders/:id", async (c) => {
  const sql = postgres(c.env.ORDERS_DB.connectionString, {
    max: 5,
    fetch_types: false,
  });
  const db = drizzle(sql);

  const id = Number(c.req.param("id"));
  const result = await db
    .select()
    .from(orders)
    .where(orders.id.eq(id))
    .limit(1);

  c.executionCtx.waitUntil(sql.end());

  if (result.length === 0) return c.notFound();
  return c.json(result[0]);
});

export default app;
```

코드 한 줄씩 살펴보자.

`postgres(c.env.ORDERS_DB.connectionString, ...)` — Hyperdrive의 connection string을 그대로 postgres-js에 넘긴다. 라이브러리 입장에서는 그냥 Postgres 한 대다. Hyperdrive를 쓰는지 RDS를 직접 쓰는지 코드는 알지 못한다. 이게 좋은 신호다 — 표준 인터페이스 뒤에 Hyperdrive가 숨어 있어 lock-in이 얇다.

`max: 5` — postgres-js가 한 isolate 안에서 들고 있는 connection 수의 상한이다. Hyperdrive 너머의 풀과 별개다. Workers 한 isolate는 짧게 살았다 죽기 때문에, 내부 풀을 크게 들고 있을 이유가 없다.

`c.executionCtx.waitUntil(sql.end())` — Worker는 응답을 보낸 뒤에도 ctx 안에서 비동기 정리 작업을 끝낼 수 있다. connection 정리를 응답 이후로 미루면 사용자 응답 시간이 영향을 받지 않는다. JVM 세계에는 없는 멘탈 모델이라 처음 보면 낯설지만, 익숙해지면 무척 쓸모 있다.

이제 `wrangler dev --remote`로 한 번 돌려보자. 첫 요청은 Hyperdrive 풀을 채우는 비용이 살짝 보이지만, 두 번째 요청부터는 응답이 즉각 돌아온다. `wrangler tail`로 로그를 보면 SQL 한 번에 ms 단위 응답이 박히는 걸 볼 수 있다.

#### 3단계 — Drizzle 마이그레이션을 어떻게 굴릴까

여기서 한 가지 결정이 필요하다. Drizzle 스키마와 마이그레이션을 어디서 굴릴 것인가? 두 가지 패턴이 있다.

첫째, 마이그레이션은 기존 Spring Boot/Flyway/Liquibase에서 그대로 굴리고, Drizzle은 읽기·타입 정의 용도로만 쓰는 패턴. 이게 가장 안전하다. 마이그레이션의 책임자가 한 곳이라 충돌이 없다.

둘째, Drizzle Kit으로 마이그레이션을 직접 굴리는 패턴. 새로 만든 도메인 또는 작은 서비스에서 쓸 만하다. 다만 기존 Flyway 이력과 충돌할 수 있으므로, 두 도구가 같은 테이블에 손대지 않도록 영역을 갈라두자.

권장은 첫 번째다. 기존 마이그레이션 파이프라인은 그대로 두고, Workers는 읽기·쓰기를 표준 SQL로 한다. 왜? 마이그레이션은 옮기지 않을 때 가장 안전하니까. 컴퓨트 한 겹만 이동시키는 게 우리의 약속이었음을 다시 떠올리자.

### 호환성 한 번 더 — 어디까지가 기존 그대로인가

Hyperdrive가 표준 Postgres·MySQL을 그대로 흘려보낸다고 해도, 모든 동작이 1:1로 같지는 않다. 이 자리는 정직하게 짚고 넘어가야 한다. 광고서가 아니라 실무 가이드를 읽고 있다는 약속이니까.

**Postgres 호환성** — postgres-js, node-postgres(pg), Drizzle, Kysely 모두 잘 돈다. Aurora·RDS·Neon·Supabase 어디든 endpoint만 Hyperdrive로 바꾸면 된다. 이게 책 전체에서 가장 매끄러운 호환성 사례 중 하나다.

**MySQL 호환성** — `mysql2`가 표준 선택이다. PlanetScale은 자체 HTTP 프로토콜을 쓰는 별개 옵션이라 Hyperdrive와는 결이 다르다. PlanetScale 자체는 그 자체로 글로벌 가속이 있으므로 Hyperdrive 앞에 굳이 두지 않아도 된다.

**prepared statement** — 여기는 주의가 필요하다. Hyperdrive의 transaction mode 풀에서는 connection이 트랜잭션 단위로 회수되기 때문에, 한 connection에 prepared statement를 캐시해 두는 전통적 패턴이 그대로 작동하지 않을 수 있다. 라이브러리에 따라 매 트랜잭션마다 prepared statement를 다시 등록하거나, `prepare: false` 같은 옵션을 명시해야 한다. 처음 도입할 때 이 한 가지 때문에 지연이 미묘하게 들쭉날쭉하면 prepare 동작부터 의심하자.

**LISTEN/NOTIFY · long-running cursor** — Postgres의 LISTEN/NOTIFY 같은 영속 연결 기반 기능은 transaction-scoped 풀과 어울리지 않는다. 이런 워크로드는 별도 채널(예: 전용 worker가 직접 RDS에 붙어 NOTIFY를 듣고, Cloudflare Queue로 흘려보내는 식)로 분리하는 편이 낫다. 마찬가지로 거대한 결과셋을 cursor로 스트리밍하는 패턴도 풀 모델과 충돌한다. 짧고 여러 번이 Hyperdrive의 sweet spot이다.

**Connection limit** — RDS에 max_connections라는 한도가 있다는 사실을 다시 떠올리자. Hyperdrive 풀 크기는 우리가 정할 수 있고, 그 풀이 RDS로 향하는 실제 연결 수의 상한을 결정한다. RDS 인스턴스가 db.t3.medium처럼 작다면 max_connections가 100 안쪽이다. Hyperdrive 풀 크기를 그 안에서 잡아야 한다. 같은 RDS를 다른 서비스(Spring Boot, EC2 batch 등)와 공유하고 있다면, 각자의 풀 크기를 합쳐서 RDS의 max_connections를 넘지 않도록 운영팀과 미리 합의하자.

**쓰기 일관성** — 가장 중요한 한 줄이다. **쓰기 일관성을 보장하는 책임은 여전히 DB에 있다.** Hyperdrive는 connection 가속기이지 데이터 일관성 보장 레이어가 아니다. SERIALIZABLE 트랜잭션이 필요하면 SQL에 그렇게 쓰자. SELECT ... FOR UPDATE가 필요하면 그렇게 쓰자. Hyperdrive가 무언가를 자동으로 더 강하게 만들거나 약하게 만들지 않는다.

### 쿼리 캐시는 양날의 검이다

Hyperdrive의 쿼리 캐시 이야기로 잠시 돌아가자. 같은 SELECT가 짧은 시간 안에 반복되면, Hyperdrive는 두 번째부터 PoP 가까이에서 캐시된 결과를 돌려준다. 응답이 ms 단위로 떨어진다. 이건 매력적인 그림이다.

그런데 이 캐시는 우리가 평소 머릿속에 그리는 "DB가 항상 가장 최신"이라는 가정을 살짝 흔든다. 데이터가 방금 INSERT됐는데 다른 PoP에서 SELECT하면 잠깐 옛 결과가 보일 수 있다. TTL이 짧아도 0은 아니다.

그렇다면 어떻게 해야 할까? 두 갈래로 정리하자.

첫째, **읽기 일관성이 강해야 하는 쿼리는 캐시를 끈다.** Hyperdrive 설정에서 쿼리 캐시 자체를 비활성화하거나, 라이브러리 레벨에서 cache hint를 disable한다. 결제 직후 잔액 조회, 권한 체크 같은 자리가 여기 해당한다.

둘째, **읽기 일관성이 느슨해도 괜찮은 쿼리는 캐시를 켠다.** 카탈로그 목록, 인기 상품 톱10, 카테고리 트리 같은 자리. 이쪽은 1초 정도 옛 결과여도 사용자는 알아채지 못한다. 캐시 hit이 되는 쿼리에서 Hyperdrive의 진가가 가장 잘 드러난다.

이 결정을 SQL 한 줄 단위로 내려야 한다는 점이 처음에는 번거롭게 느껴진다. 그러나 다시 생각해보면, CDN 캐시 정책을 URL 단위로 내리는 일과 비슷하다. 정적 자산은 1년 캐시, API 응답은 0초 캐시, 카탈로그는 1분 캐시. 그 멘탈을 SQL에도 옮겨오면 된다. 익숙해지면 자연스럽다.

### Aurora·Supabase·Neon·PlanetScale — 어디든 붙는다

Hyperdrive의 사용처가 RDS만이 아니라는 점도 짚어두자. 표준 Postgres·MySQL을 노출하는 모든 서비스가 후보다.

**Aurora Postgres / Aurora MySQL** — RDS와 같은 방식으로 붙는다. Aurora의 read replica를 별도 endpoint로 둔다면, write용 Hyperdrive와 read용 Hyperdrive를 따로 만들어 코드에서 분기할 수도 있다.

**Supabase** — Supabase는 사실상 매니지드 Postgres + Auth + Storage 묶음이다. Postgres 부분은 Hyperdrive와 완벽히 어울린다. Workers + Hyperdrive + Supabase Postgres 조합은 풀스택 SaaS의 가장 가벼운 시작점 중 하나다.

**Neon** — serverless Postgres. scale-to-zero가 기본이라 hobby·MVP에 잘 맞는다. Neon + Hyperdrive 조합은 글로벌 분산 + 비용 절감 두 마리 토끼를 얻는 자리다. 다만 Neon 자체가 콜드스타트가 있다는 점은 기억해두자 — 첫 쿼리는 살짝 느릴 수 있다.

**PlanetScale** — 앞서 짚었듯, PlanetScale은 자체 HTTP 프로토콜을 통해 직접 edge에서 호출하는 경로가 따로 있다. Hyperdrive 없이도 글로벌 가속이 들어 있는 셈이다. 굳이 Hyperdrive를 거칠 이유가 적다.

이쯤에서 한 가지 분명히 해두자. **D1 vs Hyperdrive는 경쟁 관계가 아니다.** D1은 새 SQL DB를 Cloudflare 안에 두는 선택이고, Hyperdrive는 기존 Postgres·MySQL을 그대로 쓰는 선택이다. 새 프로젝트, 워크로드가 SQLite로 충분하고 Workers 안에 닫혀 있다면 D1이 좋은 선택이다. 기존 RDS·Aurora가 있고 그걸 옮길 의도가 없다면 Hyperdrive다. 둘 중 하나가 우월한 게 아니라, 결정의 입력이 다르다.

### 점진 이전의 첫 걸음으로 — 무엇을 옮기고 무엇을 남길까

이 챕터의 그림 하나를 다시 그려보자. 아래는 가장 현실적인 하이브리드 패턴이다.

```
[해외 사용자] → [Cloudflare PoP의 Workers] → [Hyperdrive] → [도쿄 Aurora]
                                              ↓
                                       (글로벌 connection pool)
                                              ↓
                              [기존 Spring Boot ECS도 같은 Aurora를 본다]
```

이 그림에서 무엇이 안 움직였는지 보자. Aurora가 안 움직였다. Spring Boot ECS가 안 움직였다. 마이그레이션·백업·DBA 절차가 안 움직였다. 움직인 것은 단 하나 — Workers라는 컴퓨트 한 겹이 글로벌 PoP에 새로 깔렸다는 점뿐이다.

이 한 겹의 이득이 충분히 크다면, 계속 이 그림으로 머물러도 된다. 굳이 다 옮길 필요가 없다. 14장에서 다시 강조하지만, 하이브리드는 임시 상태가 아니다. 많은 회사에서 하이브리드가 **최종 형태**다.

어디서 다음 걸음을 내딛을지는 사용 패턴이 결정한다. KV로 옮길 만한 세션 데이터가 있는가? R2로 옮길 만한 큰 미디어 자산이 있는가? Workflows로 옮길 만한 Step Functions orchestration이 있는가? 이 결정들은 5장에서 그렸던 결정 매트릭스를 다시 펼쳐 보면 된다. Hyperdrive는 그 매트릭스에서 "옮기지 않는다"라는 칸을 두려움 없이 선택하게 해주는 도구다.

### 무너지는 자리 — Hyperdrive가 못 풀어주는 것

이 책이 광고서가 아닌 이상, 이 도구가 어디서 무너지는지도 함께 짚어야 한다.

- **쓰기 일관성**은 여전히 DB의 책임이다. Hyperdrive는 SELECT를 빠르게 해주지만, 동시 쓰기의 충돌을 자동으로 풀어주지는 않는다. SERIALIZABLE이 필요하면 명시적으로 쓰자.
- **prepared statement·LISTEN/NOTIFY·long cursor** 같은 connection-bound 기능은 transaction-mode 풀과 어울리지 않는다. 매번 다시 prepare하거나, 별도 채널로 분리해야 한다.
- **DB 자체의 max_connections**가 풀 크기의 상한이다. RDS 인스턴스가 작으면 풀도 작게 잡아야 하고, 같은 DB를 공유하는 다른 서비스와 합산해서 한도를 넘지 않게 운영팀과 합의해야 한다.
- **쿼리 캐시는 양날의 검**이다. 한쪽 페이지의 응답을 ms 단위로 떨어뜨리지만, 잘못 켜면 stale 데이터가 사용자 눈에 들어온다. SQL 한 줄 단위로 캐시 정책을 내릴 각오가 필요하다.
- **VPC 깊이 격리**가 필요한 환경에는 publicly accessible RDS가 부담스러울 수 있다. 그런 경우엔 Cloudflare Tunnel을 써서 사설망 안쪽에서 outbound-only로 RDS를 노출하는 패턴을 쓰는 편이 낫다 — 이게 다음 장의 주제와 자연스럽게 맞물린다.

### 마무리

Hyperdrive를 손에 넣은 우리에게는 한 가지 새로운 선택지가 생겼다. **데이터를 옮기지 않고도 컴퓨트만 글로벌로 흩뿌릴 수 있다.** 이 한 줄짜리 가능성이 점진 마이그레이션 전체의 무게를 한 자릿수 가볍게 만든다. 7번의 round-trip이 흡수되고, 트랜잭션 모델은 익숙한 그대로 유지되며, 롤백은 connection string 한 줄 바꾸는 일이다.

물론 모든 자리가 매끄럽지는 않다. prepared statement, LISTEN/NOTIFY, 쓰기 일관성, max_connections 같은 DB 운영의 익숙한 함정들은 그대로 따라온다. 그래서 Hyperdrive는 기존 RDS·Aurora·Postgres를 잘 알고 있는 팀에게 가장 잘 어울린다. 모르고 도입하는 도구가 아니라, 알고 도입을 늦췄던 팀이 손쉽게 한 걸음을 내딛을 때 쓰는 도구다.

다음 장에서는 RDS를 publicly accessible로 두기가 찜찜한 자리에서 무엇을 할지를 살펴보자. Cloudflare Tunnel과 Access·WAF·Turnstile이 어떻게 묶여 "VPC 없는 세계의 보안 모델"을 만드는지가 다음 페이지에서 펼쳐진다.

---


## 11장. 보안과 Zero Trust — Access·Tunnel·WAF·Turnstile·Auth.js

VPC와 Security Group, NACL과 IAM 정책으로 그어둔 경계가 익숙한 우리에게 "경계가 없다"는 말은 처음에 끔찍하게 들린다. 우리는 사설망 안쪽을 안전한 거실, 바깥쪽을 위험한 길거리로 그려두는 데 익숙하다. EC2는 거실 안에 있어야 하고, ALB만이 길거리에 발을 내놓는다. 누군가 "EC2를 outbound-only로만 노출해 보세요"라고 말하면, 평생 IP 화이트리스트로 살아온 백엔드 개발자의 머릿속에서는 빨간불이 들어온다. 그게 Spring `SecurityFilterChain`을 한 줄씩 짜며 익혀온 직감이다.

그런데 잠시 멈춰 생각해 보자. 우리가 그어둔 그 경계는 정말 안전한 경계였던가? VPN을 한 번 뚫고 들어온 사용자는 그 안에서 어디든 갈 수 있었다. SG를 한 번 잘못 열면 RDS가 인터넷 전체에 노출됐다. 사내망 안쪽이라는 이유로 인증 없이 도는 어드민 페이지가 한두 개씩은 있었다. "안쪽이니까 안전하다"는 가정이 사실은 가장 무른 가정이었던 셈이다.

Zero Trust는 이 가정을 처음부터 거꾸로 뒤집는다. **경계로 신뢰를 만들지 말고, identity로 신뢰를 만들자.** 어떤 네트워크에서 들어오든, 사용자·디바이스가 누구인지·무엇인지를 매 요청마다 묻자. IP로 신뢰하는 게 아니라 사람으로 신뢰하자. 이 한 줄이 Cloudflare Access·Tunnel·WAF·Turnstile·API Shield가 한 묶음으로 엮이는 출발점이다.

이번 장에서는 IAM의 정교한 정책 언어를 잃은 자리에 무엇을 어떻게 다시 세울지, EC2 사설 서브넷을 외부에 노출하지 않고도 어떻게 Cloudflare로 안전하게 끌어올지, 그리고 일반 사용자 인증은 Auth.js·Lucia·Clerk·자체 JWT 중 무엇을 골라 얹을지를 차례로 살펴보자. 마지막엔 사내 Grafana를 한 번에 노출해보는 작은 워크스루로 손에 익히자.

#### Spring SecurityContext에 익숙한 사람을 위한 다리

본격적인 도구 이야기로 들어가기 전, Spring 개발자가 머릿속에 들고 있는 그림 한 장을 먼저 옮겨두자. Spring Security를 한 번이라도 깊이 짜본 사람이라면 `SecurityFilterChain` → `AuthenticationManager` → `SecurityContextHolder`라는 흐름이 머리에 박혀 있을 것이다. 요청이 들어오면 필터 체인이 한 줄씩 검사하고, 인증이 끝난 사용자는 `Authentication` 객체로 컨텍스트에 박힌다. 이후 어디에서든 `@PreAuthorize`나 `SecurityContextHolder.getContext()`로 그 사용자를 꺼내 쓴다.

Cloudflare로 옮기면 이 흐름이 분해된다. `SecurityFilterChain`의 역할이 한 곳에 모이지 않고 여러 자리에 흩어진다 — Cloudflare 엣지에서 도는 WAF·Bot·Access 한 단, Worker 안에서 도는 Hono 미들웨어 한 단, 그리고 origin에서 한 번 더 검증하는 한 단. 처음엔 이 흩어짐이 어색하다. "한 곳에서 다 잡는 게 깔끔하지 않나?"라는 의심이 든다.

그렇지만 다시 생각해 보자. Spring의 한 곳 모음이 깔끔해 보였던 건 같은 JVM·같은 프로세스 안에서 도는 신뢰 모델이 깔려 있어서였다. 분산된 엣지·다중 PoP·여러 Worker가 한 도메인을 처리하는 그림에서는 한 곳에 모으는 게 오히려 위험하다. 엣지에서 거를 수 있는 건 엣지에서 거르고(거기서 막으면 origin이 안 부른다 = 비용·지연 절감), Worker가 봐야 할 건 Worker가 보고, origin이 신뢰의 마지막 보루로 한 번 더 검증한다. 같은 책임을 세 단에 나눠 두는 그림이다.

기억해두자 — Cloudflare 세계의 보안은 한 줄짜리 `SecurityFilterChain`이 아니라, **여러 단의 점진적 거름망**이다. 처음엔 흩어져 보이지만, 익숙해지면 각 단의 책임이 또렷해 디버깅이 쉬워진다.

### 경계 대신 identity — Cloudflare Access

먼저 Cloudflare Access부터 살펴보자. 한 줄로 줄이면 이렇다 — **모든 앱 앞단에 SSO 게이트를 한 겹 두는 도구.** AWS 세계에서 가까운 그림을 그린다면 IAM Identity Center + Verified Access의 조합이다. Verified Access는 ZTNA(Zero Trust Network Access)를 표방하며 네트워크 단의 VPN을 identity 기반으로 갈아치우는 제품이고, Identity Center는 SSO·사용자·그룹을 관리한다. Cloudflare Access는 이 두 자리를 한 제품에서 다룬다.

작동 그림은 간단하다. `admin.toby-shop.com` 같은 서브도메인 앞에 Access 정책을 건다. 사용자가 그 도메인을 열면, 자기 회사 SSO(Google Workspace·Okta·Azure AD·GitHub·OIDC·SAML 어떤 IdP든)로 로그인하라는 페이지가 먼저 뜬다. 로그인이 성공하면 Access가 짧은 수명의 JWT를 쿠키에 박아주고, 그 쿠키를 들고 들어오는 요청만 뒤쪽 origin에 도달한다. 이때 origin은 EC2일 수도, Workers일 수도, 사내 Jenkins일 수도 있다. Access는 그 앞에 무엇이 있든 신경 쓰지 않는다 — 자기 일은 사람이 누군지 묻는 것뿐이다.

여기까지 보면 "그게 뭐 대단한가, ALB + Cognito로도 비슷하게 한다"고 말할 수 있다. 그런데 한 꺼풀 더 들어가 보면 차이가 보인다.

첫째, **device posture**다. 회사 노트북에만 발급된 디바이스 인증서가 있는 기기, OS가 최신 패치된 기기, 디스크 암호화가 켜진 기기에서만 들어오게 하는 정책을 한 줄로 건다. AWS Verified Access도 비슷한 그림을 그릴 수 있지만 설정의 무게가 다르다. Cloudflare Access에서는 Zero Trust 대시보드에서 체크박스 몇 개로 끝난다.

둘째, **앱 단위 정책**이다. IAM처럼 service·resource·action을 거대한 정책 문서로 묶지 않고, 한 도메인·한 경로마다 "이 그룹의 사람들만 들어올 수 있다"라고 끊어 표현한다. 정책 언어로서의 표현력은 IAM보다 좁지만, 실무에서 실제로 쓰는 패턴 — 어드민 페이지는 admin 그룹만, 스테이징은 dev 그룹만, 외부 협력사는 vendor 그룹만 — 을 한눈에 짜기엔 오히려 가볍다.

셋째, **브라우저 기반 SSH·VNC·RDP**다. Access 뒤쪽의 EC2에 SSH를 붙는데, 클라이언트는 그냥 브라우저 한 장이다. SSH 키를 노트북마다 뿌리고 관리하던 절차가, "Access로 로그인하면 브라우저 안에서 터미널이 열린다"로 바뀐다. 처음 보면 "이게 진짜 보안이 되나?" 싶지만, 실제로는 SSH 키 분실·노트북 도난 같은 사고를 한 단계 줄여준다. Cloudflare가 사용자별로 짧은 수명 인증서를 자동 발급해 EC2 OpenSSH에 꽂는 구조라, 키가 사용자 손에 영구히 남지 않는다.

기억해두자. Cloudflare Access의 본질은 한 줄이다 — **모든 트래픽 앞에 identity 한 겹을 둔다.** IP 화이트리스트를 더 정교하게 만드는 게 아니라, 아예 IP 자체를 신뢰의 기준으로 쓰지 않는 그림이다.

#### IAM의 빈자리, 어떻게 다시 채울까

Spring 세계에서 `SecurityFilterChain`은 모든 요청 앞단에서 인증·인가를 잡아준다. AWS 세계에서는 IAM이 그 자리에 있다. Cloudflare로 넘어오면 그 정교한 정책 언어가 한 번에 사라진 자리에 약간의 공허함이 남는다. "그래서 Worker A는 R2 bucket B에 어떤 권한으로 닿는 거지?" 같은 질문이 생긴다.

답은 세 줄로 갈라진다.

- **Worker ↔ 리소스 권한**은 `wrangler.toml`의 Bindings로 표현한다. Worker가 어떤 KV·D1·R2·Queue·DO에 닿을 수 있는지가 코드 옆에 선언으로 박힌다. IAM role의 Resource·Action을 Bindings 한 줄이 흡수한 셈이다. 정책 문서가 아니라 코드 옆 설정 파일이라 짧고 또렷하다.
- **사람·디바이스 ↔ 앱 권한**은 Cloudflare Access 정책으로 표현한다. 이쪽은 IAM Identity Center + Verified Access의 자리.
- **외부 클라이언트 ↔ API 권한**은 WAF 룰·API Shield·mTLS로 표현한다. IAM의 service-to-service 권한 영역.

세 자리가 한 제품으로 묶이지 않는다는 게 처음엔 흩어져 보인다. 그렇지만 다시 생각해 보면, IAM도 사실 한 제품이라기보다 여러 컨셉을 한 정책 언어 아래 묶어둔 것이었다. Cloudflare는 그 묶음을 풀어 컨셉별로 다른 도구에 나눠 담은 셈이다. 익숙해지면 각자의 책임이 명확해 디버깅이 오히려 쉬워진다.

### Cloudflare Tunnel — outbound-only로 사설망 끌어오기

이제 EC2 이야기를 해보자. 10장에서 우리는 RDS를 publicly accessible로 두고 SG에 Cloudflare egress IP를 화이트리스트했다. 동작은 한다. 그런데 찜찜하다. RDS가 인터넷에 노출돼 있다는 사실 자체가 보안팀의 잠을 줄인다.

다른 길은 없을까? 있다. **Cloudflare Tunnel**이다. 이름이 생경하지만, 동작은 단순하다. 사설망 안쪽 어딘가에 `cloudflared`라는 작은 데몬을 한 대 띄운다. 이 데몬은 사설망 안쪽에서 Cloudflare 엣지로 outbound 연결을 연다 — 들어오는 포트는 하나도 열지 않는다. Cloudflare는 그 outbound 연결을 잡아두고, 외부에서 들어오는 요청을 그 연결을 타고 사설망 안쪽으로 흘려보낸다.

이걸 그림으로 보면 한 줄이다.

```
[외부 사용자] → [Cloudflare 엣지] ↘
                                  ↓ (outbound-only tunnel)
                        [사설망 안쪽 cloudflared] → [RDS / EC2 서비스]
```

사설망 입장에서는 inbound 포트가 0개다. SG는 0/0에 대해 인바운드를 모두 닫아도 된다. 외부에서 RDS로 직접 닿는 길은 없다. 그런데도 Cloudflare 엣지에서 들어오는 정당한 요청은 사설망 안쪽 RDS로 이어진다. AWS 세계의 Site-to-Site VPN이나 PrivateLink가 풀어주던 문제를, outbound-only 모델로 더 가볍게 푼 셈이다.

처음 들으면 "outbound가 양방향으로 동작하나?" 싶다. 그렇다 — TCP를 outbound로 한 번 열어두면 그 위로 양방향 데이터가 흐른다. WebSocket이나 SSH의 reverse port forwarding을 쓴 사람이라면 익숙한 그림이다. Cloudflare Tunnel은 이 패턴을 production-grade로 다듬어 둔 것이다.

#### 손가락으로 한 번 띄워 보자

말로만 풀면 멀리 있는 이야기 같다. 손가락을 움직여 보자. EC2 한 대에서 사내 Grafana(`localhost:3000`)를 외부에 노출하는 시나리오를 가정한다.

```bash
# EC2 안에서, cloudflared 설치 (Amazon Linux 기준)
curl -L --output cloudflared.rpm \
  https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.rpm
sudo rpm -ivh cloudflared.rpm

# Cloudflare 계정에 로그인 (브라우저로 OAuth)
cloudflared tunnel login

# 새 터널 만들기
cloudflared tunnel create toby-grafana
# → Tunnel 이름과 ID, credentials 파일 경로 출력

# 터널을 도메인에 매핑
cloudflared tunnel route dns toby-grafana grafana.toby-shop.com

# config.yml 작성
cat > ~/.cloudflared/config.yml <<'YAML'
tunnel: toby-grafana
credentials-file: /home/ec2-user/.cloudflared/<UUID>.json
ingress:
  - hostname: grafana.toby-shop.com
    service: http://localhost:3000
  - service: http_status:404
YAML

# systemd 서비스로 띄우기
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

이 한 사이클이면 EC2 SG에서 80·443·3000 어떤 포트도 열지 않은 채로, `https://grafana.toby-shop.com`이 외부에서 동작한다. cloudflared가 EC2 안쪽에서 Cloudflare 엣지로 outbound 연결을 유지하고, Cloudflare가 그 연결을 타고 사용자 요청을 흘려보낸다.

이 자리에 Cloudflare Access를 한 줄 더 얹으면 — 그러니까 같은 도메인에 Access 정책을 걸면 — Grafana 앞에 SSO 게이트가 자동으로 끼어든다. Google Workspace 로그인을 통과한 사람만 Grafana로 들어가고, 들어가는 즉시 Grafana는 자기 인증 없이도 사용자가 누군지 헤더로 받을 수 있다 (`Cf-Access-Authenticated-User-Email` 같은 헤더). 사내 어드민 도구의 인증을 Access로 한 곳에 모아두면, Grafana·Jenkins·Argo·Kibana 어떤 도구든 자기 SSO 통합을 따로 하지 않아도 된다.

기억해두자 — `cloudflared`는 **데몬**이다. EC2가 죽으면 그 EC2의 터널도 같이 죽는다. Production에서는 한 터널을 여러 cloudflared replica가 함께 들고 있게 띄워야 한다 (같은 터널 ID를 여러 EC2에 띄우면 자동으로 부하 분산이 된다). 이건 ALB의 가용성을 직접 짊어지는 그림과 비슷하다 — 가볍지만 운영자의 책임이 늘어난 셈이다.

### WAF·Bot Management·Turnstile — 한 묶음으로 보자

Tunnel과 Access가 "들여보낼 사람"을 다룬다면, WAF·Bot Management·Turnstile은 "들이지 말아야 할 트래픽"을 다룬다. 이쪽은 Cloudflare 보안 스택의 가장 익숙한 얼굴 — DDoS 막아주는 그 회사라는 인상의 출처다.

세 도구가 어떻게 다른지부터 풀어보자.

**WAF**는 OWASP Top 10 같은 잘 알려진 공격 패턴을 룰셋으로 잡아준다. SQL injection, XSS, RCE 시도를 패턴 매칭으로 거른다. Cloudflare는 Managed Ruleset(Cloudflare가 직접 관리)·OWASP Ruleset·Custom Rule 세 단을 제공한다. 우리가 직접 룰을 짠다면 Custom Rule 쪽이다 — "특정 경로로 들어오는 PUT 요청은 차단하라" 같은 식으로 표현 언어를 써서 한 줄씩 쌓는다.

**Bot Management**는 패턴 매칭이 아닌 **신호 기반**이다. JA3 fingerprint, TLS 특성, 요청 간격, behavior pattern 등 수십 가지 신호를 모아 사람·legitimate bot·악성 bot을 구분해 점수로 매긴다. 점수가 임계치 아래면 차단·challenge·로그만 남기고 통과 같은 행동을 룰로 건다. 이 영역은 머신러닝 기반이라 우리가 룰을 직접 짜기보다는 점수를 활용해 정책을 쓰는 쪽이다.

**Turnstile**은 클라이언트 사이드의 신호를 한 번 더 잡는 위젯이다. CAPTCHA를 대체하는 자리에 들어간다. 흥미로운 점은 — 일반 사용자에게는 **invisible challenge**라 UI가 거의 보이지 않는다는 것이다. 봇 의심이 강한 경우에만 사용자에게 한 번 클릭을 요청하거나 추가 검증을 한다. reCAPTCHA에 길들여진 사용자에게는 거의 마찰이 없다. 회원가입·로그인·비밀번호 재설정 같은 form 앞에 자주 얹는다.

세 도구를 한 묶음으로 보면 이렇다. WAF는 알려진 패턴, Bot Management는 행동 신호, Turnstile은 클라이언트 신호. 같은 적을 세 각도에서 보는 셈이다. Cloudflare 공식 가이드는 셋을 함께 쓰는 통합 패턴을 권한다 — 통과시킬지 막을지 결정할 때 세 점수를 함께 본다.

#### Workers에서 Turnstile 한 줄 검증

Turnstile 위젯을 form에 붙이면 클라이언트는 토큰 한 장을 받는다. 이 토큰을 서버가 한 번 검증해야 의미가 있다. Workers에서는 한 줄짜리 fetch면 끝난다.

```ts
import { Hono } from "hono";

const app = new Hono<{ Bindings: { TURNSTILE_SECRET: string } }>();

app.post("/signup", async (c) => {
  const body = await c.req.parseBody();
  const token = body["cf-turnstile-response"] as string;

  const verify = await fetch(
    "https://challenges.cloudflare.com/turnstile/v0/siteverify",
    {
      method: "POST",
      body: new URLSearchParams({
        secret: c.env.TURNSTILE_SECRET,
        response: token,
        remoteip: c.req.header("CF-Connecting-IP") ?? "",
      }),
    },
  );
  const result = (await verify.json()) as { success: boolean };

  if (!result.success) {
    return c.json({ error: "verification failed" }, 403);
  }

  // 정상 회원가입 흐름...
  return c.json({ ok: true });
});

export default app;
```

`CF-Connecting-IP` 헤더는 Cloudflare가 자동으로 박아주는 진짜 클라이언트 IP다. ALB의 `X-Forwarded-For`와 비슷한 자리지만, Cloudflare 엣지가 위변조를 막아준다는 점이 다르다. 기억해두자 — `X-Forwarded-For`는 우리가 한 번 더 검증해야 할 헤더고, `CF-Connecting-IP`는 신뢰해도 되는 헤더다.

### mTLS와 API Shield — B2B API의 정직한 신뢰

지금까지의 도구는 사용자·브라우저를 다뤘다. 그렇다면 서버 ↔ 서버는 어떤가? 우리 API를 외부 회사 시스템이 호출한다면? IP 화이트리스트로 막던 그 자리는 Cloudflare에서 무엇으로 채울까?

답은 **mTLS**다. 클라이언트도 서버도 서로의 인증서를 검증하는 양방향 TLS. 한쪽 방향만 인증하던 보통 HTTPS와 달리, 서버도 클라이언트가 가진 인증서를 검증해 "이 클라이언트는 우리가 사전에 발급한 인증서를 가진 신뢰 가능한 상대다"를 확인한다.

Cloudflare에서 이걸 거는 자리가 **API Shield**다. API Shield는 mTLS 외에도 schema validation(우리 OpenAPI 명세에 안 맞는 요청을 거르는 것)·sequence rules(API 호출 순서가 정상인지 검증)·sensitive data detection 같은 도구를 묶어 둔다. 외부 파트너에게 API를 여는 자리, 모바일 앱이 우리 백엔드에 붙는 자리, 내부 서비스 간 통신을 한 단 더 단단히 묶는 자리에서 쓴다.

설정의 큰 틀은 이렇다. Cloudflare에 우리 자체 CA를 등록하고, 그 CA로 클라이언트 인증서를 발급해 파트너에게 준다. Cloudflare 룰에서 "이 도메인·이 경로로 들어오는 요청은 우리 CA로 발급된 클라이언트 인증서가 있어야 통과시킨다"를 한 줄 건다. 통과한 요청에는 인증서 정보가 헤더로 박혀 origin에 전달된다. origin Worker는 그 헤더로 "어느 파트너의 요청인가"를 확인한다.

기억해두자 — mTLS는 사용자 인증이 아니라 **클라이언트 시스템 인증**이다. 사람을 식별하지 않는다. B2B API·모바일 앱·내부 서비스 간처럼 클라이언트가 시스템인 자리에서 쓴다. 사람 인증과는 결이 다르다는 점을 흐리지 말자.

#### 사례 — 공개 API에 mTLS·WAF·Turnstile 한 줄로

`toby-shop`이 외부 파트너에게 주문 조회 API를 열었다고 해보자. 요구사항은 셋이다 — 파트너 시스템 외에는 못 부르게, 알려진 공격 패턴은 엣지에서 거르게, 사람 흉내 내는 봇은 별도 신호로 한 번 더 잡게.

세 도구를 차곡차곡 쌓아 본다.

**1단 — WAF 룰 한 줄.** `partners.toby-shop.com/orders`로 들어오는 요청은 GET·POST만 허용하고, body에 SQL injection·XSS 패턴이 보이면 차단. Cloudflare Managed Ruleset과 OWASP Ruleset을 켜고, Custom Rule 한 줄을 더 얹는다 — "이 경로의 PUT·DELETE 요청은 무조건 block".

**2단 — API Shield mTLS.** 파트너 회사마다 우리 CA로 발급한 클라이언트 인증서를 한 장씩 준다. Cloudflare 룰에 "이 도메인으로 들어오는 요청은 우리 CA 인증서가 있어야 통과"를 한 줄 건다. 인증서 없는 요청은 엣지에서 403으로 끊긴다 — origin Worker는 이 요청을 보지도 못한다.

**3단 — Turnstile은 form 위에만.** 이 API는 시스템 ↔ 시스템이라 Turnstile은 안 붙인다. 다만 같은 도메인의 파트너 셀프서비스 화면(예: 신규 파트너 가입 form, API key 발급 화면) 앞에는 Turnstile을 한 줄 얹는다. 사람의 form 제출과 봇의 form 제출을 구분하는 자리다.

origin Worker는 이렇게 짤 수 있다.

```ts
import { Hono } from "hono";

const app = new Hono();

app.use("/orders/*", async (c, next) => {
  // mTLS로 검증된 클라이언트 인증서 정보가 헤더로 박혀 있다
  const certHeader = c.req.header("Cf-Client-Cert-Spki");
  const partnerId = c.req.header("Cf-Client-Cert-Subject-DN");

  if (!certHeader || !partnerId) {
    return c.json({ error: "client cert required" }, 401);
  }

  // 파트너별 권한 분기
  c.set("partnerId", partnerId);
  await next();
});

app.get("/orders/:id", async (c) => {
  const partnerId = c.get("partnerId");
  // partnerId 기반으로 그 파트너가 볼 수 있는 주문만 반환
  return c.json({ id: c.req.param("id"), partnerId });
});

export default app;
```

`Cf-Client-Cert-*` 헤더는 Cloudflare가 mTLS 검증 후 박아주는 헤더다. origin은 이 헤더를 신뢰해 파트너를 식별한다. 단 — origin이 Cloudflare를 거치지 않은 요청을 받지 않게 막는 건 우리 책임이다 (origin SG에서 Cloudflare IP만 허용하거나, origin이 들어오는 토큰을 한 번 더 검증). 안 그러면 누군가 origin 직접 IP를 알아내 헤더를 위조해 들어올 수 있다.

이 세 단을 함께 켜두면, 파트너 API의 보안은 거의 자동이 된다. 우리가 직접 짜는 건 partner-별 권한 로직 한 줄뿐이다. ALB + WAF + Lambda Authorizer + Cognito + KMS의 조합으로 같은 그림을 그리려고 했던 사람이라면, 이 단순함이 살짝 어이없게 느껴질 수 있다. 그게 정상이다.

### Workers + Auth.js·Lucia·Clerk — 일반 사용자 인증

이제 화제를 바꿔 일반 사용자 회원가입·소셜 로그인·세션 관리로 넘어가 보자. 이쪽은 Access의 영역이 아니라 — Access는 SSO 게이트로 앱 앞단에 두는 것 — 우리 앱 안쪽에서 Auth.js·Lucia·Clerk·자체 구현으로 직접 짜는 영역이다.

네 갈래를 비교해 보자.

**Auth.js (NextAuth)** — Next.js 생태계에서 가장 무난한 선택. OAuth provider 50개 이상이 기본으로 들어 있고, OpenNext on Cloudflare 환경에서도 잘 돈다. session storage를 D1 또는 KV에 둘 수 있다. Drizzle 어댑터까지 짝으로 쓰면 7장에서 그렸던 D1 + Drizzle 그림과 자연스럽게 이어진다.

**Lucia** — Workers·Edge에 친화적인 minimal auth 라이브러리. "magic" 적은 코드로 명시적인 흐름을 짠다. Auth.js가 너무 큰 추상으로 느껴지는 사람, refresh token rotation·session invalidation 같은 동작을 손에 쥐고 짜고 싶은 사람에게 잘 맞는다. DB는 D1 또는 Hyperdrive 너머의 Postgres 어디든.

**Clerk** — SaaS형 인증 서비스. 회원가입·로그인·MFA·비밀번호 재설정·이메일 확인 같은 모든 흐름을 Clerk에 위임한다. UI 컴포넌트도 함께 제공된다. 도입 속도가 가장 빠르지만, 사용자 수에 비례해 비용이 든다. MVP·짧은 사이클로 출시해야 하는 자리에서 쓸 만하다.

**자체 구현 (Hono + JWT + KV)** — 가장 가벼운 길. Hono 미들웨어 한 줄로 JWT 검증, KV에 세션 저장, OAuth 콜백은 직접 짜기. 의존성이 적고 코드를 손에 쥐고 있다는 안도감이 있다. 다만 refresh token rotation, session revoke, OAuth 50개 provider 호환 같은 디테일을 모두 직접 책임진다.

어떤 걸 고를까? 정답은 없지만 가이드는 이렇다.

- 새 SaaS · MVP · 짧은 사이클이라면 **Clerk**
- Next.js 위에 평범한 소셜 로그인이라면 **Auth.js**
- Workers 단독 · 코드 정밀 제어가 필요하면 **Lucia**
- 인증 흐름이 단순하고 의존성을 줄이고 싶으면 **Hono + JWT + KV**

5장의 결정 프레임 표현으로 옮기면 — Clerk은 "Move now·운영 부담 최소", Auth.js는 "표준 패턴 그대로", Lucia는 "edge-native 가벼움", 자체는 "lock-in 회피"가 각각의 sweet spot이다.

#### Auth.js + D1 + Workers — 코드 한 토막

가장 흔한 그림인 Auth.js + D1 + Google 로그인을 코드로 그려 보자. OpenNext 위가 아니라 순수 Workers + Hono 환경이다.

```ts
// src/auth.ts — Auth.js v5 코어 설정
import { Auth } from "@auth/core";
import Google from "@auth/core/providers/google";
import { D1Adapter } from "@auth/d1-adapter";

type Env = {
  AUTH_SECRET: string;
  GOOGLE_CLIENT_ID: string;
  GOOGLE_CLIENT_SECRET: string;
  DB: D1Database;
};

export function authHandler(req: Request, env: Env) {
  return Auth(req, {
    adapter: D1Adapter(env.DB),
    secret: env.AUTH_SECRET,
    providers: [
      Google({
        clientId: env.GOOGLE_CLIENT_ID,
        clientSecret: env.GOOGLE_CLIENT_SECRET,
      }),
    ],
    session: { strategy: "database" },
    trustHost: true,
  });
}
```

Hono 라우터에 붙이는 자리는 한 줄이다.

```ts
// src/index.ts
import { Hono } from "hono";
import { authHandler } from "./auth";

const app = new Hono<{ Bindings: Env }>();

// /auth/* 모든 요청을 Auth.js에 위임 — signin, callback, signout, session 등
app.all("/auth/*", (c) => authHandler(c.req.raw, c.env));

// 보호된 라우트 — 세션이 없으면 401
app.get("/me", async (c) => {
  const sessionRes = await fetch(
    new URL("/auth/session", c.req.url),
    { headers: c.req.raw.headers },
  );
  const session = (await sessionRes.json()) as { user?: { email: string } };
  if (!session.user) return c.json({ error: "unauthenticated" }, 401);
  return c.json({ email: session.user.email });
});

export default app;
```

`wrangler.toml`에는 D1 바인딩과 secret 세 개를 적어준다.

```toml
name = "toby-shop-auth"
main = "src/index.ts"
compatibility_date = "2026-04-01"

[[d1_databases]]
binding = "DB"
database_name = "toby-shop"
database_id = "your-d1-id"

# AUTH_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET은
# wrangler secret put 으로 등록
```

```bash
wrangler secret put AUTH_SECRET
wrangler secret put GOOGLE_CLIENT_ID
wrangler secret put GOOGLE_CLIENT_SECRET
```

이 한 사이클이면 Google 소셜 로그인이 동작한다. 사용자가 `/auth/signin/google`로 들어가면 Google OAuth로 보내지고, 콜백이 돌아오면 Auth.js가 D1에 사용자·계정·세션을 기록한다. 세션은 쿠키로 클라이언트에 박히고, 우리는 `/auth/session` 엔드포인트로 현재 세션을 언제든 조회할 수 있다.

세션을 KV에 두고 싶다면 `D1Adapter` 자리에 KV 어댑터로 바꾸면 된다. 7장에서 본 KV vs D1 결정과 결이 같다 — 세션은 read-heavy + eventually consistent로 충분하니 KV가 잘 맞는 자리다. 다만 Auth.js의 표준 KV 어댑터는 별도 패키지를 골라야 하고, 일부는 커뮤니티 메인테인이다. 시작은 D1 어댑터로 안정적으로, 트래픽이 늘면 세션만 KV로 분리하는 흐름이 무난하다.

#### KV 세션의 일관성 — 60초의 의미

KV에 세션을 둘 때 한 번 짚어둘 게 있다. KV는 eventually consistent이고 전파에 최대 60초가 걸린다. 사용자가 로그아웃을 누르고 KV의 세션 키를 지웠다고 해도, 다른 PoP에서는 잠깐 옛 세션이 보일 수 있다는 뜻이다. 이게 무엇을 의미하는지 두 갈래로 정리하자.

**보통 로그인·로그아웃 흐름에서는 문제 없다.** 사용자가 한 PoP에서 로그인하고, 같은 사용자가 같은 디바이스로 같은 PoP 근처에서 다시 들어오는 게 보통이다. 같은 PoP의 KV는 즉시 일관된다. 글로벌 전파 60초가 보이는 자리는 다른 PoP에서 들어오는 매우 드문 케이스다.

**중요한 보안 이벤트에서는 한 단 더.** 비밀번호 변경 직후·다른 디바이스 강제 로그아웃·세션 revoke 같은 자리에서는 KV의 60초 전파가 위험할 수 있다. 이 자리에는 D1에 "revoked sessions" 테이블 한 장을 두고, 미들웨어가 세션 검증 시 D1을 한 번 더 보게 짠다. read는 D1로 한 번 더 가지만, security-critical 동작은 즉시 일관성을 보장한다. KV의 빠름과 D1의 일관성을 한 자리에 섞는 패턴이다.

기억해두자 — KV·D1·DO 중 어느 한 도구로 세션을 다 풀려고 하지 말자. 세션의 read와 revoke는 일관성 요구가 다르다. **빠른 read는 KV, 즉시 revoke는 D1**으로 갈라두는 편이 낫다.

#### 사례 — Workers + Auth.js로 Google 로그인 + KV 세션 한 사이클

위 그림을 그대로 손가락에 옮겨 보자. `toby-shop` 사용자가 Google로 로그인하고, 세션은 KV에서 빠르게 읽고, 로그아웃은 D1의 revocation 테이블에 한 줄을 박아 즉시 무효화하는 그림이다.

```ts
// src/middleware/session.ts
import type { MiddlewareHandler } from "hono";

type Env = {
  SESSIONS: KVNamespace;
  DB: D1Database;
};

export const sessionMiddleware: MiddlewareHandler<{ Bindings: Env }> = async (
  c,
  next,
) => {
  const sessionToken = c.req.header("Cookie")
    ?.match(/session=([^;]+)/)?.[1];

  if (!sessionToken) {
    c.set("user", null);
    return next();
  }

  // 1단 — KV에서 세션 읽기 (빠름, eventually consistent)
  const session = await c.env.SESSIONS.get(sessionToken, "json") as
    | { userId: string; email: string; expiresAt: number }
    | null;

  if (!session || session.expiresAt < Date.now()) {
    c.set("user", null);
    return next();
  }

  // 2단 — D1에서 revoke 여부 확인 (강한 일관성)
  const revoked = await c.env.DB.prepare(
    "SELECT 1 FROM revoked_sessions WHERE token = ? LIMIT 1",
  )
    .bind(sessionToken)
    .first();

  if (revoked) {
    // KV에서도 지워둔다 (eventual cleanup)
    c.executionCtx.waitUntil(c.env.SESSIONS.delete(sessionToken));
    c.set("user", null);
    return next();
  }

  c.set("user", { id: session.userId, email: session.email });
  await next();
};
```

로그인 콜백 자리는 Auth.js에 위임하되, 세션 발급 후 KV에 한 줄 박는 hook을 한 단 추가한다.

```ts
// src/auth.ts (events hook)
events: {
  signIn: async ({ user, env }) => {
    const token = crypto.randomUUID();
    const expiresAt = Date.now() + 30 * 24 * 60 * 60 * 1000; // 30일
    await env.SESSIONS.put(
      token,
      JSON.stringify({ userId: user.id, email: user.email, expiresAt }),
      { expirationTtl: 30 * 24 * 60 * 60 },
    );
    // 쿠키 박는 자리는 Auth.js 또는 직접 Set-Cookie로
  },
  signOut: async ({ token, env }) => {
    // KV에서도 지우고, D1에도 revocation 박기
    await env.SESSIONS.delete(token);
    await env.DB.prepare(
      "INSERT INTO revoked_sessions (token, revoked_at) VALUES (?, ?)",
    )
      .bind(token, Date.now())
      .run();
  },
},
```

이 한 사이클이면 사용자 로그인 흐름은 KV의 빠름을, 로그아웃·revoke는 D1의 강한 일관성을 함께 누린다. Spring 개발자의 익숙한 그림으로 옮기면 — Spring Session + Redis(빠른 세션) + DB(audit log) 조합과 비슷한 자리에 있다. 다만 우리는 두 도구가 한 wrangler.toml 안에 바인딩으로 묶여 있어 운영의 무게가 가볍다.

여기에 11장 앞부분의 도구를 한 줄씩 더 얹어 보자. 로그인 form 앞에는 Turnstile 한 단(브루트포스 봇 차단), 회원가입에는 WAF rate limit 한 단(같은 IP에서 분당 10회 이상 가입 시도 차단), 그리고 어드민 페이지는 Access 한 단으로 한 번 더 막는다. 그러면 사용자 인증 한 묶음이 — Cloudflare 엣지의 WAF·Turnstile·Access · Worker 안의 Hono 미들웨어 · KV·D1의 데이터 단 — 세 층으로 쌓이고, 각 층의 책임이 또렷이 갈라진다. Spring `SecurityFilterChain` 한 줄에 모든 걸 모으던 그림과는 결이 다르지만, 분산 환경에서는 이 갈라짐이 더 안정적이다.

### 사례 — 사내 Grafana를 한 번에 노출

이번 장의 도구들을 한 그림으로 묶어 보자. `toby-shop` 운영팀이 사내 Grafana를 외부에서 쓰고 싶어 한다. 요구사항은 셋이다.

1. EC2의 어떤 포트도 외부에 열지 말 것
2. 회사 Google Workspace 계정으로만 들어갈 수 있을 것
3. 회사 발급 노트북에서만 들어갈 수 있을 것

전통적인 AWS 패턴이라면 — VPN 한 번 깔고, ALB에 Cognito Authorizer 붙이고, 회사 노트북 인증을 Cognito 위에 또 한 겹 짜는 — 이 세 줄을 풀어내는 데 며칠이 걸린다. Cloudflare 한 묶음으로는 한나절이면 된다. 절차를 그려 보자.

**1단계 — Cloudflare Tunnel로 EC2 노출.** EC2에 cloudflared 데몬을 띄우고 `localhost:3000`(Grafana)을 `grafana.toby-shop.com`에 매핑한다. 앞서 본 명령어 그대로다. 이 시점에 EC2의 SG는 inbound 0/0을 모두 닫아도 된다.

**2단계 — Cloudflare Access 정책 부착.** Zero Trust 대시보드에서 `grafana.toby-shop.com`에 Access 애플리케이션을 만든다. Identity provider는 Google Workspace로 추가하고 (OIDC client ID·secret 한 번 입력), 정책은 "이메일 도메인이 `@toby-shop.com`인 사용자만 통과"로 한 줄 건다.

**3단계 — Device posture 추가.** 같은 정책에 device posture 조건을 한 줄 더 건다 — "디바이스 인증서가 발급된 노트북만 통과". 회사가 발급한 노트북에는 mTLS 클라이언트 인증서를 미리 깔아 두는 식이다. 또는 더 단순한 길로, WARP 클라이언트가 동작 중이고 회사 zone에 enroll된 디바이스만 통과로 잡을 수도 있다.

**4단계 — Grafana 인증 위임.** Grafana는 자기 인증 화면을 끄고, Access가 박아 주는 `Cf-Access-Authenticated-User-Email` 헤더를 신뢰해 사용자를 식별하도록 설정한다 (Grafana의 `auth.proxy` 모드). Access의 JWT signature를 한 번 더 검증하면 더 안전하다 — Cloudflare 공식 JWKS endpoint에서 키를 받아 Grafana가 직접 검증할 수 있다.

이 네 단계로 끝이다. 결과 — 외부에서 `grafana.toby-shop.com`을 열면 회사 Google 로그인 → device posture 검사 → Access JWT 발급 → Grafana 도착이라는 흐름이 자동으로 돈다. EC2의 어떤 포트도 외부에 열지 않은 채로. SG는 깨끗하고, 보안팀은 잠을 더 잔다.

같은 패턴으로 Jenkins·Argo·Kibana·내부 어드민 페이지를 한 도메인씩 더해 가면 된다. `cloudflared` config의 `ingress` 항목에 한 줄씩 늘리고, Access 애플리케이션에 한 개씩 등록하기. SSO 통합을 도구마다 따로 짜던 세계와는 무게가 다르다.

### 무너지는 자리 — Zero Trust도 만능은 아니다

이 책이 광고서가 아닌 이상 한 번 더 정직하게 짚고 가자. 위에서 푼 그림들이 어디서 무너지는가.

**Access는 enterprise IdP에 깊이 의존한다.** Google Workspace·Okta·Azure AD 같은 IdP가 살아 있어야 동작한다. IdP가 죽으면 Access 뒤의 모든 앱이 같이 죽는다. 회사가 IdP 한 곳에 묶이는 셈이라, IdP 자체의 가용성이 critical path가 된다. 이건 AWS Identity Center에 묶이는 그림과 비슷한 무게다 — 단일 의존을 받아들이는 결단이 필요하다.

**Tunnel은 cloudflared 데몬의 운영 부담을 새로 만든다.** ALB가 알아서 풀어주던 가용성·헬스체크·로깅을 우리가 cloudflared replica로 짊어진다. 한 EC2에만 cloudflared를 띄우면 그 EC2가 죽는 순간 터널이 끊긴다. Production에서는 최소 두 대 이상에 같은 터널 ID로 cloudflared를 띄워야 하고, 그 데몬의 헬스·로그·버전 업그레이드를 운영 절차에 포함해야 한다. 무료라고 해서 운영비가 0인 건 아니다.

**Bot Management와 Turnstile은 일부 정교한 봇을 못 잡는다.** 사람이 쓰는 도구를 흉내 내거나, residential proxy를 거쳐 사람처럼 행동하는 봇은 점수가 사람 가까이 나온다. 결제 abuse·credential stuffing 같은 자리에서는 Cloudflare 한 단에 모두 맡기지 말고, 우리 application logic에 rate limit·abuse detection 한 단을 더 넣는 편이 낫다. "Cloudflare가 막아줄 거야"라는 가정은 위험하다.

**mTLS는 인증서 운영의 책임을 가져온다.** 발급·rotation·revocation을 우리가 직접 짊어진다. 한 파트너의 인증서가 만료되면 그 순간 그 파트너의 통신이 끊긴다. 만료 알림과 자동 rotation 절차를 미리 깔아두지 않으면, 6개월 뒤 새벽 알림이 울린다. 끔찍한 일이다.

**IAM의 정교한 정책 언어는 정말 등가물이 없다.** 우리가 IAM의 condition·NotAction·resource ARN 패턴 같은 정밀한 표현에 익숙하다면, Cloudflare의 Bindings + Access policy + WAF rule 조합은 처음에 거칠게 느껴질 수 있다. 표현력의 한계다. 정교한 권한 그래프를 그리는 자리는 Cloudflare 단독이 어렵다 — 외부 IAM 시스템(Okta·Auth0·OPA·자체 권한 서비스)을 한 단 더 두는 편이 낫다.

**Access의 JWT 검증을 origin에서 안 하면 우회 위험이 있다.** Cloudflare 엣지를 거치지 않고 origin에 직접 닿는 경로가 한 줄이라도 있다면 — 누군가 origin IP를 알아내거나, DNS를 우회한다면 — Access가 무용지물이 된다. origin이 들어오는 JWT를 직접 검증하거나, origin이 Cloudflare 엣지에서 온 트래픽만 받도록 mTLS·Cloudflare-only IP 화이트리스트를 origin SG에 한 단 더 두는 게 안전하다.

이 한계들이 도구를 못 쓰게 만드는 건 아니다. 다만 "Cloudflare 켰으니 안전하다"는 단순한 가정으로 잠을 너무 깊이 자지는 말자는 이야기다. Zero Trust의 핵심은 "어디서도 신뢰를 가정하지 말 것" 아닌가. 도구 자체에도 그 원칙을 적용해 보자.

### 마무리

이번 장에서 우리는 IAM·Cognito·Verified Access·Site-to-Site VPN의 자리를 Cloudflare One 스택이 어떻게 다시 채우는지 살펴봤다. 핵심은 한 줄이다 — **경계가 아니라 identity로 신뢰를 만든다.** Access는 사람·디바이스를 매 요청마다 묻고, Tunnel은 사설망을 outbound-only로 끌어오며, WAF·Bot Management·Turnstile은 들이지 말아야 할 트래픽을 세 각도에서 거른다. mTLS와 API Shield는 시스템 ↔ 시스템 신뢰를, Auth.js·Lucia·Clerk·자체 JWT는 일반 사용자 인증을 채운다.

10장의 Hyperdrive와 자연스럽게 짝을 이룬다는 점도 다시 짚어두자. 10장에서 우리는 RDS를 publicly accessible로 두는 그림을 그렸지만, 그게 찜찜하다면 11장의 Cloudflare Tunnel로 사설망 안쪽에서 outbound-only로 RDS를 노출할 수 있다. 두 장을 함께 읽으면, "DB는 AWS, 컴퓨트는 Cloudflare" 하이브리드 패턴이 보안 측면에서도 닫힌 그림이 된다.

기억해두자. Zero Trust는 도구가 아니라 멘탈 모델이다. Access·Tunnel·WAF·Turnstile·mTLS는 그 멘탈을 구현하는 도구일 뿐, 도구를 켜는 것만으로 Zero Trust가 완성되지는 않는다. "어디서도 신뢰를 가정하지 말 것"이라는 한 줄을 우리 시스템 곳곳에 적용해 보자 — 그게 이번 장의 진짜 약속이다.

다음 장에서는 시야를 또 한 번 넓혀, AI·Workflows·Queues·Cron Triggers로 비동기·orchestration·스케줄·LLM 영역을 살펴보자. Step Functions와 SQS, `@Scheduled`와 Bedrock의 빈자리에 Cloudflare가 무엇을 어떻게 들여놓는지가 다음 페이지에서 펼쳐진다.

---


## 12장. AI·Workflows·Queues — Step Functions·SQS·`@Scheduled` 너머

이런 상황을 한번 가정해보자. 결제가 끝나면 영수증 PDF를 만들고, 그 PDF를 R2에 올린 뒤 사용자에게 이메일로 보내고, 30분 뒤 후속 안내 메일을 한 번 더 보내는 sequence를 짜야 한다. 익숙한 답은 Step Functions다. ASL JSON 한 덩어리를 그리고, Lambda를 다섯 개 묶고, IAM role 다섯 개를 따로 관리하고, CDK 스택에 얹는다. 코드와 워크플로 정의가 두 곳에 분리돼 있어 디버깅할 때마다 두 화면을 번갈아 봐야 한다. 그러다 누군가 옆에서 묻는다. "근데 그 30분 sleep 동안에도 state transition이 돈으로 잡히지?" 한 달 청구서를 떠올리면 살짝 찜찜하다.

그 찜찜함을 한 번 풀어보자. 같은 sequence를 이번에는 Workers 위에서 짠다고 해보자. 코드 한 파일에 step을 줄줄이 적고, 30분 sleep은 비용 0으로 처리되고, 영수증 발송은 Queue로 분리하고, 매시 정각에 도는 health check는 cron 한 줄로 붙는다. AI Gateway 한 겹을 끼워 OpenAI에 먼저 던져보고 실패하면 Workers AI로 fallback한다. 이 그림이 실제로 가능한지, 가능하다면 어디까지 production에 견디는지가 이 장의 주제다.

이 장은 다섯 파트로 길게 간다. Workflows로 Step Functions의 자리를 다시 채우고, Queues로 SQS의 자리를, Cron Triggers로 Spring `@Scheduled`·EventBridge Scheduler의 자리를 채운다. 그 위에 Workers AI·Vectorize·AI Gateway라는 세 도구를 더 얹어, 작은 RAG 챗봇과 fallback 체인까지 한 사이클을 그린다. 분량이 길지만, 각 파트가 독립적으로 읽혀도 된다. 호흡을 한 번씩 끊으며 따라오자.

---

### Part 1. Workflows — Step Functions를 코드로 다시 그리기

#### Step Functions 한 달 청구서를 떠올려 보자

먼저 ASL의 무게부터 짚고 가자. Step Functions로 상태 머신을 짜본 사람이라면 알 것이다. 한 step씩 JSON으로 정의하고, Choice·Parallel·Map·Wait를 조합하고, ResultPath로 입출력을 넘긴다. 표현력은 풍부하다. 그런데 가격 모델이 한 번 거슬린다. **state transition 단위로 과금**된다. Standard workflow는 1,000 transition당 $0.025. 그래서 long-poll, 30분 대기, 사람이 승인할 때까지 기다리는 step도 시간이 길어질수록 비용에 잡힌다 — 정확히는 "transition 횟수"에 잡히지만, 워크플로가 길고 step이 많을수록 그 횟수가 누적된다.

여기에 ASL의 또 한 가지 무게가 있다. 코드와 정의가 분리된다. Lambda 함수 다섯 개의 코드는 TypeScript로 짰는데, 이걸 묶는 워크플로는 별도 JSON에 들어 있다. 디버깅하다 보면 머리가 두 화면을 왔다 갔다 한다. 로컬에서 step 하나를 돌려보려면 Lambda 단위로 돌리거나, AWS Toolkit에서 시뮬레이션하거나, 결국엔 stage에 배포해 놓고 콘솔에서 입력 JSON을 던진다. 익숙해지면 쓸 만하지만, 익숙해지는 데까지의 거리가 멀다.

**Cloudflare Workflows는 이 두 가지 무게를 다른 방식으로 푼다.** 코드와 정의를 한 곳에 둔다. 그리고 외부 대기 시간은 비용에 잡지 않는다. 하나씩 살펴보자.

#### Durable execution이 무엇인가

Workflows를 이해하려면 한 단어를 먼저 짚어야 한다. **durable execution**. 우리말로 "영속 실행" 정도가 된다. 무슨 뜻인가? 워크플로 인스턴스가 실행 도중 어딘가에서 죽어도, 다시 살아나서 **다음 step부터** 이어 돌릴 수 있다는 뜻이다. 마지막으로 끝낸 step의 결과는 영속 저장소에 적혀 있고, 새 인스턴스는 그 결과를 읽어 다음 step으로 넘어간다.

Step Functions가 이미 같은 일을 한다. Temporal·AWS Durable Functions·Inngest 같은 도구들도 같은 카테고리다. Workflows는 이 패턴을 Cloudflare 식으로 — V8 isolate 위에서 — 재구현한 것이다. 차이는 **인터페이스**에 있다. ASL JSON 대신 TypeScript 코드 한 파일이다.

```ts
import { WorkflowEntrypoint, WorkflowEvent, WorkflowStep } from "cloudflare:workers";

type Params = { orderId: string; email: string };

export class ReceiptWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    const { orderId, email } = event.payload;

    const order = await step.do("verify-order", async () => {
      return await this.env.DB.prepare("SELECT * FROM orders WHERE id = ?")
        .bind(orderId).first();
    });

    const pdfUrl = await step.do("render-receipt-pdf", async () => {
      const pdf = await renderReceiptPdf(order);
      const key = `receipts/${orderId}.pdf`;
      await this.env.R2.put(key, pdf);
      return `https://files.toby-shop.example/${key}`;
    });

    await step.do("send-receipt-email", async () => {
      await this.env.MAIL_QUEUE.send({ to: email, kind: "receipt", url: pdfUrl });
    });

    await step.sleep("wait-30-minutes", "30 minutes");

    await step.do("send-followup-email", async () => {
      await this.env.MAIL_QUEUE.send({ to: email, kind: "followup", orderId });
    });
  }
}
```

코드를 한 줄씩 살펴보자. `step.do(name, async () => { ... })` — 이 한 묶음이 한 step이다. 이름과 동작 함수를 같이 넘긴다. 함수가 끝나고 반환된 값은 영속 저장소에 적힌다. 인스턴스가 도중에 죽어도, 다시 살아날 때 이 step은 적힌 결과를 그대로 읽고 다음으로 넘어간다. 즉 **`step.do` 안의 코드는 멱등(idempotent)이거나, 이미 끝난 step은 다시 실행되지 않는다는 가정 위에 짜야 한다.** 기억해두자 — 한 step 안에서 같은 부수효과를 두 번 만들면 안 된다. 결제·이메일·외부 API 호출 같은 위험한 부수효과는 step 단위로 깔끔히 떨어뜨리자.

`step.sleep("wait-30-minutes", "30 minutes")` — 이게 이번 장의 주연 중 하나다. 30분을 기다린다. 그 30분 동안 워커가 살아 있을까? 그렇지 않다. 인스턴스는 잠들어 있다가, 30분 뒤에 다음 step부터 다시 살아난다. **그 30분 동안 CPU는 0이고, 비용도 0에 가깝다.** Step Functions였다면 state transition이 누적되는 자리에서 Workflows는 가격이 사실상 사라진다. long-poll·승인 대기·후속 알림 같은 시나리오가 많을수록 가격 격차가 커진다.

`step.waitForEvent` 같은 API도 있다 — 외부에서 특정 이벤트가 도착할 때까지 기다리는 step이다. 사람이 승인할 때까지, webhook이 도착할 때까지, 또 다른 워크로드가 신호를 보낼 때까지 기다린다. 이 자리도 마찬가지로 비용 0이다.

#### Step Functions ↔ Workflows 한 페이지 매핑

머리에 그림 하나로 박아두자.

| 개념 | Step Functions | Workflows |
|---|---|---|
| 정의 형식 | ASL JSON | TypeScript 코드 |
| step 정의 | `Task` state | `step.do(name, fn)` |
| 분기 | `Choice` state | 그냥 `if` |
| 병렬 | `Parallel` state | `Promise.all([step.do(...), step.do(...)])` |
| 반복 | `Map` state | `for` 루프 + `step.do` |
| 대기 | `Wait` state | `step.sleep("...", "30 minutes")` |
| 외부 이벤트 | Task token | `step.waitForEvent` |
| 과금 | state transition 수 | 실행 중 CPU time만 |

ASL의 표현력 중 한 가지가 사라졌다는 점은 짚어야 한다. **AWS 서비스 통합**이다. Step Functions에는 200+ AWS 서비스 액션이 ASL 안에서 직접 호출 가능한 형태로 들어 있다. SNS publish, S3 putObject, DynamoDB UpdateItem 같은 호출을 Lambda 없이 한 줄로 적을 수 있다. Workflows에는 그런 통합이 없다 — 외부 호출은 step 안에서 SDK·fetch로 직접 적는다. 코드 한 줄이 늘어난다고 보면 된다. 다만 Bindings가 빛나는 자리이기도 하다. R2·D1·KV·Queue·Service binding이 `this.env.X`로 그대로 쓰이니, "AWS 서비스 통합 200개"는 없어도 Cloudflare 안에서의 통합은 매끄럽다.

#### Workflows를 어떻게 시작하나

`wrangler.toml`에 한 묶음 적어주면 된다.

```toml
name = "toby-shop-jobs"
main = "src/index.ts"
compatibility_date = "2026-04-01"

[[workflows]]
name = "receipt-workflow"
binding = "RECEIPT"
class_name = "ReceiptWorkflow"
```

이제 다른 Worker에서 이 워크플로를 시작하려면 한 줄이다.

```ts
const instance = await env.RECEIPT.create({
  params: { orderId: "ord-1234", email: "user@example.com" },
});
console.log("workflow id:", instance.id);
```

대시보드에 가면 인스턴스 목록·각 step의 상태·실패 step의 stack trace가 보인다. 실패한 step은 자동 재시도된다 — backoff 정책도 step 단위로 설정 가능하다. 어떤 step에서 retry exhaust가 나면 인스턴스 자체가 멈추고, 우리가 이어서 처리할 수 있는 상태로 남는다.

retry 정책을 한 step에 붙이려면 두 번째 인자로 옵션 객체를 넘기면 된다.

```ts
await step.do(
  "send-receipt-email",
  {
    retries: { limit: 5, delay: "10 seconds", backoff: "exponential" },
    timeout: "1 minute",
  },
  async () => {
    await this.env.MAIL_QUEUE.send({ to: email, kind: "receipt", url: pdfUrl });
  }
);
```

이 옵션이 Step Functions의 `Retry` 필드와 1:1로 대응한다. 차이는 — 한 곳에 코드와 retry 정책이 함께 있다는 것뿐이다. 디버깅할 때 두 화면을 왔다 갔다 하지 않아도 된다.

#### 가격 모델 비교 — 30분 sleep이 왜 게임 체인저인가

이 자리에서 한 번 숫자로 짚자. 위 영수증 sequence를 한 달에 100,000건 처리한다고 해보자. 한 sequence에 step 5개, 그 중 한 개가 30분 sleep이다.

**Step Functions Standard 가정.** 한 sequence가 약 8번의 state transition을 만든다(Task entry/exit, Wait entry/exit 포함). 100,000건 × 8 transition = 800,000 transition. 1,000 transition당 $0.025로 계산하면 월 $20 정도. 작아 보이는가? 그러면 sequence를 길게 만들고, sleep을 늘리고, 재시도를 늘려보자. transition은 그만큼 누적된다. 그리고 sleep 동안 state는 영속 저장소에 머물러 있다 — Step Functions는 그 저장 자체에 또 비용을 잡지는 않지만, 같은 state machine이 동시에 수만 개 떠 있는 시나리오에서는 운영 한도를 신경 써야 한다.

**Workflows 가정.** 한 sequence의 실제 CPU 시간은 sleep을 빼면 수백 ms 안쪽이다. CPU time × 요청 수 모델이라 — sleep 30분은 비용에 잡히지 않는다. 같은 100,000건이라도 청구서는 일반 Workers 호출 100,000건 + step storage 비용 일부에 가깝다. 정확한 단가는 공식 페이지에서 확인해야 하지만, **체감으로 한 자릿수 낮은 자리**에 있다.

이 가격 격차가 sleep이 길고 재시도가 많은 워크로드에서 폭이 가장 크다. 인간 승인 대기 30분, webhook 도착 대기 1시간, 후속 알림 24시간 같은 sequence라면 Workflows의 가격 모델이 분명한 우위를 잡는다. 반대로 sleep 없이 빠르게 끝나는 짧은 sequence라면 격차가 작다 — 그쪽은 가격보다 "코드와 정의가 한 곳에 있다"는 멘탈 모델 이득이 더 크다.

#### 무너지는 자리 — Workflows의 한계

이 책이 광고서가 아닌 이상, 무너지는 자리도 함께 짚자.

- **AWS 서비스 통합 자체가 깊은 워크플로**는 옮기는 비용이 만만치 않다. ASL의 `arn:aws:states:::dynamodb:updateItem.waitForTaskToken` 같은 깊은 통합 시나리오는 Workflows에서 그대로 옮길 등가물이 없다. Step Functions에 묶인 이력이 길수록 옮기는 일이 부담스럽다.
- **거대한 batch**는 부적합이다. Workflows는 짧은 multi-step orchestration에 어울린다. 30분짜리 ETL을 한 step에 욱여넣는 일은 잘못된 자리다. 그쪽은 ECS/Fargate 또는 Spring Batch가 그대로 더 잘 푼다 (5장 결정 프레임을 다시 펼쳐 보자).
- **lock-in**도 정직하게. Workflows의 `step.do`·`step.sleep` API는 Cloudflare 고유다. Temporal로 옮긴다면 비슷한 멘탈이지만 코드는 다시 짜야 한다. 다만 "ASL JSON에 lock-in되는 것"과 "TypeScript 함수에 lock-in되는 것"의 무게는 다르다. 코드는 결국 함수다 — 옮기기는 어렵지만, 구조 자체는 portable한 모양으로 남는다.

---

### Part 2. Queues — SQS의 자리를 채우다

#### 큐는 왜 필요한가, 다시 한 번

이런 자리를 떠올려 보자. 우리가 방금 짠 `ReceiptWorkflow`의 `send-receipt-email` step. 이메일 발송은 외부 SMTP 또는 Resend·SendGrid 같은 외부 API를 부른다. 잠깐 외부 API가 흔들리면? 워크플로의 step.do가 실패하고, 자동 retry된다. 그래도 안 되면 워크플로 인스턴스가 그 자리에서 멈춘다. 이메일 한 통 때문에 결제 후 sequence 전체가 멈추는 그림은 살짝 끔찍하다.

그래서 옛날부터 답이 정해져 있었다. 메일은 **큐**에 넣고, 큐에서 따로 도는 consumer가 하나씩 빼서 발송한다. SQS를 써본 사람이라면 익숙한 그림이다. producer는 메시지를 던지고, consumer는 polling 또는 push로 받아 처리한다. 처리 실패하면 retry, 그래도 안 되면 dead-letter queue로 격리.

Cloudflare Queues는 이 모델을 그대로 옮겨온 도구다. 다만 Cloudflare 식으로 한 겹 가볍다. 어떻게 가볍냐면 — **producer와 consumer가 둘 다 Worker**다. polling을 우리가 짤 필요가 없다. SQS 콘솔에서 "이 큐를 trigger로 묶어 Lambda를 호출"하던 단계가 Queues에서는 wrangler 설정 한 줄로 끝난다.

#### Producer와 consumer 한 사이클

producer Worker는 한 줄이면 된다.

```ts
await env.MAIL_QUEUE.send({
  to: "user@example.com",
  kind: "receipt",
  url: "https://files.toby-shop.example/receipts/ord-1234.pdf",
});
```

`env.MAIL_QUEUE`는 `wrangler.toml`에 producer binding으로 적어둔 이름이다.

```toml
[[queues.producers]]
binding = "MAIL_QUEUE"
queue = "mail-outbound"
```

consumer Worker는 별도 모듈이다. 같은 큐를 consumer로 등록한다.

```toml
[[queues.consumers]]
queue = "mail-outbound"
max_batch_size = 25
max_batch_timeout = 5
max_retries = 3
dead_letter_queue = "mail-dlq"
```

코드는 이런 모양이다.

```ts
export default {
  async queue(batch: MessageBatch<MailJob>, env: Env): Promise<void> {
    for (const msg of batch.messages) {
      try {
        await sendMail(msg.body, env);
        msg.ack();
      } catch (err) {
        msg.retry({ delaySeconds: 30 });
      }
    }
  },
};
```

코드 한 줄씩 살펴보자. `batch.messages`는 한 번에 여러 메시지를 받아 처리할 수 있는 묶음이다. `max_batch_size: 25`이면 최대 25건을 한 호출에서 다룬다 — Worker invocation 비용이 한 번으로 묶이니, 처리량이 높을수록 단가가 떨어진다. `msg.ack()`는 성공 처리, `msg.retry({ delaySeconds: 30 })`은 30초 뒤 다시 시도. `max_retries`만큼 실패하면 자동으로 dead-letter queue(`mail-dlq`)로 넘어간다.

DLQ 자체도 또 하나의 Queue다. 따로 consumer를 붙여 슬랙 알림·운영자 inbox로 흘려보내거나, 정해진 주기로 다시 꺼내 재처리할 수 있다.

#### SQS와 비교 — 어디가 같고 어디가 다른가

| 기준 | SQS | Cloudflare Queues |
|---|---|---|
| 메시지 본문 한도 | 256KB (SQS Standard) | 128KB |
| 보존 기간 | 최대 14일 | 기본 4일 |
| ordering | 기본 X (FIFO 큐 별도) | 기본 X, partial ordering 옵션 |
| 가격 | 요청 수 + payload | 작업 수 (operation) |
| consumer | Lambda trigger 또는 polling | Worker queue handler |
| egress | AWS 안에서는 무료, 밖으로 나가면 비용 | 무료 |
| dead-letter queue | 지원 | 지원 |
| retry/visibility timeout | 지원 | 지원 |

Queues 가격 감각을 한 줄로 잡자면 — 쓰기·읽기·삭제를 합친 "operation" 단위 과금이고, 무료 plan 한도 안에서 hobby·MVP에 충분하다. 정확한 단가 표는 공식 페이지에서 확인하자 (Cloudflare는 가격 모델이 자주 미세 조정된다).

본문 한도가 SQS보다 작다는 점은 한 번 짚어야 한다. 128KB. 큰 payload는 R2에 올리고, Queue에는 R2 key만 던지는 패턴으로 풀면 된다. 사실 SQS도 256KB를 넘으면 같은 패턴(S3에 본문 저장 + 메시지에 key 포함)을 써왔다. 한도 차이가 멘탈을 크게 흔들지는 않는다.

그리고 한 가지 더 — **strict global ordering은 보장하지 않는다.** Queues는 partial ordering 옵션을 제공하지만, "전 세계에서 보낸 순서대로 정확히"를 약속하지 않는다. 결제 처리·은행 거래 같은 strong ordering이 진짜 필요한 자리라면 SQS FIFO가 더 정직한 선택이고, 더 깊이 가면 Durable Objects 안에 큐를 직접 그리는 패턴이 있다 (8장에서 다룬 actor 모델 기억하자). 일반적인 작업 큐 — 이메일·이미지 변환·webhook fan-out — 에는 Queues의 ordering 모델로 충분하다.

#### Batch consume와 throughput 한 번 더

batch 사이즈를 어떻게 잡을지가 한 번 더 짚을 자리다. `max_batch_size: 25`가 기본 권장에 가깝다. 한 번 호출에서 25건을 처리하면 Worker invocation 비용이 25분의 1로 떨어진다. SMTP 호출 같은 외부 의존이 있는 작업이라면 한 batch 안에서 `Promise.allSettled`로 동시에 던지는 패턴이 자연스럽다.

```ts
async queue(batch: MessageBatch<MailJob>, env: Env) {
  const results = await Promise.allSettled(
    batch.messages.map((msg) => sendMail(msg.body, env))
  );

  results.forEach((r, i) => {
    const msg = batch.messages[i];
    if (r.status === "fulfilled") {
      msg.ack();
    } else {
      msg.retry({ delaySeconds: 30 });
    }
  });
}
```

`max_batch_timeout: 5` — 큐에 메시지가 25건이 차지 않더라도 5초가 지나면 그 시점까지 모인 메시지를 묶어 호출한다. throughput이 작은 자리에서 latency가 너무 길어지지 않게 잡는 안전장치다.

DLQ로 빠진 메시지를 어떻게 다룰지도 한 번 정해두자. 흔한 패턴 두 가지다.

첫째, **DLQ도 또 하나의 consumer를 붙여 슬랙·이메일로 알림 + 운영자 대시보드에 적기**. 사람이 한 번 보고 손으로 재시도할지 폐기할지 정한다. 결제·이메일 같은 자리에 어울린다.

둘째, **DLQ에서 정해진 주기로 다시 메인 큐로 복귀**. cron trigger가 매시 정각에 DLQ를 비우며 메인 큐로 다시 던지는 패턴. 일시적 외부 장애가 풀리고 나서 자동으로 따라잡는 자리에 어울린다.

어느 쪽이든 — DLQ를 만들어 두고 끝이 아니라 **DLQ 자체에도 후속 절차가 있어야 한다**. DLQ에 메시지가 쌓이는데 아무도 안 보는 상황은 끔찍한 일이다. 그건 큐를 안 쓰는 것보다 더 위험하다.

#### Workflow와 Queue를 같이 쓰면

이 자리에서 한 가지 분명히 해두자. **Workflows와 Queues는 경쟁이 아니라 짝꿍이다.** Workflows는 "이 sequence를 한 멘탈로 추적하고 싶다"는 자리에 어울린다. Queues는 "이 작업 단위를 fire-and-forget으로 떠넘기고 싶다"는 자리에 어울린다. 결제 sequence 자체는 Workflow로 그리고, 그 안에서 이메일 발송이라는 외부 의존이 강한 한 부분만 Queue로 떼어내는 그림이 가장 깔끔하다.

이 그림을 정리하면 우리의 영수증 sequence는 이렇게 흐른다.

```
[결제 webhook] → ReceiptWorkflow.create()
                     │
                     ├─ verify-order (D1 SELECT)
                     ├─ render-receipt-pdf (R2 put)
                     ├─ send-receipt-email → MAIL_QUEUE.send()
                     │                            │
                     │                            └─ MailWorker (consumer, retry, DLQ)
                     ├─ sleep 30 minutes (비용 0)
                     └─ send-followup-email → MAIL_QUEUE.send()
```

Workflow가 큰 흐름을 영속적으로 잡고, Queue가 외부 의존이 깊은 한 작업의 retry·DLQ를 책임진다. 각자 잘하는 자리에 둔다.

#### 무너지는 자리 — Queues의 한계

- **strict global ordering** 미보장. 진짜로 순서가 중요한 워크로드는 SQS FIFO 또는 DO 안의 큐 패턴으로 가는 편이 낫다.
- **본문 128KB 한도**. R2 + key 패턴으로 우회 가능하지만, 한 번 짚어두자.
- **per-queue throughput 한도**가 있다. 초당 수천 건 수준에서는 충분하지만, 초당 수십만 건이 필요한 워크로드라면 Cloudflare 영업과 한도 상향을 협의하거나, 큐를 분할 운영하는 패턴이 필요하다.
- **producer/consumer가 같은 Cloudflare 안**이라는 가정. AWS Lambda를 그대로 두고 그 Lambda가 Cloudflare Queue를 consume하려면 Workers 한 겹을 더 둬야 한다 (HTTP pull API도 있지만, 그쪽은 polling 모델로 회귀한다).

---

### Part 3. Cron Triggers — `@Scheduled`의 자리

#### 매시 정각에 도는 코드 한 줄

이런 그림을 가정해보자. 매시 정각에 외부 health check를 한 번 돌고, 5xx가 일정 비율을 넘으면 슬랙으로 알림을 쏘는 작은 작업. Spring을 써왔다면 손이 자연스럽게 `@Scheduled(cron = "0 0 * * * *")` 한 줄로 간다. AWS에서는 EventBridge Scheduler에 Lambda를 묶거나, EventBridge rule을 cron 표현식으로 잡아 Lambda를 trigger한다.

Cloudflare에서는 이 자리를 **Cron Triggers**가 받는다. `wrangler.toml`에 한 묶음 적어주면 된다.

```toml
[triggers]
crons = ["0 * * * *", "*/15 * * * *"]
```

cron 표현식 두 개. 첫 번째는 매시 정각, 두 번째는 15분마다. 이 한 줄이 EventBridge rule + IAM role + Lambda permission + ARN 문자열을 한꺼번에 대신한다.

코드 쪽은 Worker의 `scheduled` handler에 적는다.

```ts
export default {
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
    if (event.cron === "0 * * * *") {
      ctx.waitUntil(runHealthChecks(env));
    } else if (event.cron === "*/15 * * * *") {
      ctx.waitUntil(syncFeed(env));
    }
  },

  async fetch(request: Request, env: Env) {
    return new Response("ok");
  },
};
```

`event.cron`이 어떤 trigger가 발화했는지 알려준다. `ctx.waitUntil(...)`은 응답 후에도 비동기 작업을 끝까지 마치도록 하는 한 줄 — 9장·10장에서 이미 만났다. 한 Worker가 여러 cron을 갖되 분기 처리를 한 곳에서 하는 패턴이 깔끔하다.

#### `@Scheduled` ↔ Cron Trigger 매핑

| 개념 | Spring `@Scheduled` | EventBridge Scheduler | Cron Trigger |
|---|---|---|---|
| 정의 위치 | 코드 어노테이션 | IaC + 콘솔 | `wrangler.toml` |
| cron 형식 | Spring cron (6필드) | UNIX cron (5/6필드) | UNIX cron (5필드) |
| 실행 환경 | JVM 안 | Lambda invocation | Worker invocation |
| 다중 schedule | 메서드마다 | rule마다 | 한 Worker에 N개 |
| 분기 | 메서드별 자동 | rule input으로 | `event.cron` 분기 |
| timezone | JVM TZ | timezone 옵션 | UTC 기본 |

기억해둘 한 가지 — **Cron Trigger의 cron 표현식은 UTC 기준**이다. 한국 시각으로 매일 오전 9시에 도는 보고서를 짜고 싶다면 `0 0 * * *` (UTC 0시 = KST 9시) 식으로 변환해 적자. 익숙해지면 자연스럽지만, 처음에는 한 번 헷갈린다.

또 하나 — 단일 invocation에 CPU time 한도가 적용된다. 보고서 한 통 돌리는 정도라면 충분하지만, 큰 batch ETL을 cron 한 방에 욱여넣는 일은 적합하지 않다. 그쪽은 Workflows로 step을 쪼개거나, ECS Fargate에 두는 편이 낫다.

#### 실습 — 매시 health check + Queue 알림

위 코드를 한 사이클로 묶어보자. 매시 정각에 외부 endpoint 5개를 health check하고, 실패가 있으면 `ALERT_QUEUE`로 흘려보낸다. consumer는 슬랙·이메일 등으로 fan-out한다.

```ts
async function runHealthChecks(env: Env) {
  const targets = [
    "https://api.toby-shop.example/health",
    "https://admin.toby-shop.example/health",
    // ...
  ];

  const results = await Promise.allSettled(
    targets.map((url) => fetch(url, { signal: AbortSignal.timeout(5000) }))
  );

  const failures = results
    .map((r, i) => ({ url: targets[i], result: r }))
    .filter(({ result }) => result.status === "rejected" || (result.value as Response).status >= 500);

  if (failures.length > 0) {
    await env.ALERT_QUEUE.send({
      kind: "health-check-failure",
      failures: failures.map((f) => f.url),
      timestamp: new Date().toISOString(),
    });
  }
}
```

이 작은 함수 한 묶음이 Spring의 `@Scheduled` + RestTemplate + `@Async` 알림 발송을 사실상 다 흡수한다. JVM도 띄우지 않고, 서버도 켜둘 필요가 없다. Worker가 매시 정각에 깨어나서 5초 내외로 도는 한 사이클이다.

#### 무너지는 자리 — Cron Trigger의 한계

- **timezone**이 UTC 기본이다. 한국 시각으로 오전 9시 같은 표현을 쓰려면 우리가 변환해야 한다 (EventBridge Scheduler에는 timezone 옵션이 있어 이쪽이 살짝 편하다).
- **CPU time 한도**가 적용된다. 큰 batch ETL은 적합하지 않다 — Workflows로 쪼개거나 ECS에 두자.
- **재시도 모델이 Queue·Workflow보다 가볍다.** 한 invocation이 실패해도 다음 cron까지 재시도가 자동으로 일어나지는 않는다. 중요한 작업이라면 cron handler 안에서 Queue·Workflow를 trigger하고, 그쪽에 retry를 맡기는 편이 낫다.
- **execution log**가 짧다. Workers Logs·Logpush로 따로 흘려보내야 한 달 전 cron이 돌았는지 안 돌았는지를 추적할 수 있다.

---

### Part 4. Workers AI — Bedrock 옆자리

#### Edge inference라는 한 줄짜리 약속

세 개의 도구(Workflows·Queues·Cron)로 비동기·orchestration·스케줄의 빈자리를 채웠다. 이제 살짝 결이 다른 영역으로 넘어가자. AI다.

Workers AI는 이 책에서 가장 신영역이고, 가장 빠르게 변하는 자리다. 한 줄로 그 본질을 잡자면 — **Cloudflare GPU 인프라 위에서 LLM·임베딩·이미지 모델을 edge에서 부른다.** Bedrock과 비슷한 카탈로그를 갖되, Cloudflare PoP 가까이에서 inference가 실행된다는 점이 다르다.

코드는 한 줄이다.

```ts
const response = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", {
  messages: [
    { role: "system", content: "You answer concisely." },
    { role: "user", content: "Explain edge computing in one sentence." },
  ],
});
```

`env.AI`는 Workers AI binding이다. `wrangler.toml`에 한 줄.

```toml
[ai]
binding = "AI"
```

이 binding 한 줄이 Bedrock의 IAM role + endpoint + boto3 init + region 설정을 다 흡수한다. 모델 ID(`@cf/meta/llama-3.1-8b-instruct`)만 넘기면 된다. 카탈로그에는 Llama 계열, Mistral, Stable Diffusion, BGE 임베딩 등이 있다. 모델 카탈로그는 자주 추가되고 가끔 사라지기도 하니, 정확한 목록은 공식 페이지를 확인하자.

#### Bedrock vs Workers AI — 의사결정 표

| 기준 | Bedrock | Workers AI |
|---|---|---|
| 위치 | AWS region 내 | Cloudflare PoP edge |
| 모델 카탈로그 | Anthropic Claude, Cohere, Mistral, Titan, Llama, Nova 등 풍부 | Llama, Mistral, BGE, SDXL 등 (카탈로그 좁음) |
| 과금 단위 | 토큰 단위 (모델별) + 일부 캐시 할인 | Neuron 단위 ($0.011/1k Neurons, 일 10k 무료) |
| latency | region 내 호출, 사용자 위치에 따라 RTT 누적 | edge 가까이, 글로벌 균일 |
| Enterprise feature | VPC endpoint, Knowledge Bases, Model evaluation, Guardrails | 가벼움. AI Gateway가 일부 보완 |
| Anthropic Claude | 직접 호출 가능 | 직접 호출은 없음 (AI Gateway로 우회) |
| 통합 | AWS 안에서 IAM·VPC·CloudWatch 매끄러움 | Bindings로 R2·D1·Vectorize·Queue와 매끄러움 |

선택 기준을 한 줄로 잡자면 — **latency-critical edge 호출과 간편함은 Workers AI**, **컴플라이언스·VPC 격리·풍부한 enterprise feature는 Bedrock**이다. Anthropic Claude 같은 특정 모델을 production에서 써야 한다면, Bedrock이 그대로 정답이고, Workers AI가 닿지 못하는 자리다 (AI Gateway를 한 겹 끼워 우회는 가능하다 — 다음 파트에서 본다).

#### Neuron 단위 과금 한 번 더

가격 모델이 Bedrock과 다르다는 점은 짚고 가야 한다. Bedrock은 모델별로 입력 토큰 단가·출력 토큰 단가가 다르다. Workers AI는 **Neuron**이라는 단위로 추상화돼 있다. Llama 3.1 8B의 1k 토큰이 몇 Neuron인지는 모델별 환산 표가 공식 페이지에 있다 (정확한 수치는 자주 갱신되므로 직접 확인하자).

이 Neuron 추상화가 좋은 점은 — **모델을 바꿔도 가격 멘탈이 한 단위로 잡힌다.** 단점은 모델별 진짜 비용 비교가 한 번 더 환산을 거쳐야 보인다는 것. hobby·MVP에서는 일 10k Neurons 무료 한도가 꽤 후하다. 작은 RAG 챗봇 정도라면 무료 한도 안에서 충분히 굴러간다.

#### 무너지는 자리 — Workers AI의 한계

- **모델 라인업이 Bedrock보다 좁다.** Anthropic Claude·Cohere Command 같은 자리는 Workers AI에는 없다 (2026년 5월 기준). 이런 모델이 production 핵심이라면 Bedrock 또는 직접 OpenAI·Anthropic 호출 + AI Gateway 조합이 더 정직하다.
- **enterprise feature가 가볍다.** VPC endpoint, Knowledge Bases, Guardrails 같은 자리는 Bedrock 쪽이 두텁다.
- **GPU 단위 큰 모델은 부적합**할 수 있다. 70B+ 대형 모델·custom fine-tuned 모델 위주라면 Workers AI보다는 SageMaker·Bedrock 쪽이 맞다.
- **카탈로그 자체가 빠르게 변한다.** 작년에 있던 모델이 사라지거나, 같은 모델의 endpoint 이름이 바뀌기도 한다. production에서는 한 번 모델을 고정한 뒤 변경 시 회귀 테스트를 한 번 돌려야 한다.

이 한계를 인정하고 보면, Workers AI는 "모든 AI 호출을 여기서 다 한다"가 아니라 "edge 가까이에서 빠른 응답이 필요한 작은 작업을 가볍게 굴린다" 자리에 가장 잘 맞다. 임베딩 생성·간단한 분류·짧은 응답 생성 — 이쪽이 sweet spot이다. 큰 LLM 호출은 다음 파트의 AI Gateway를 통해 외부 모델로 흘려보내는 패턴이 더 현실적이다.

#### Streaming 응답 한 번 더

LLM 호출에서 한 가지 더 짚고 가자. **streaming 응답**이다. 사용자가 챗봇에 질문을 던지면, 응답이 한 번에 떨어지기보다 토큰 단위로 흘러내리는 편이 체감이 좋다. Workers AI는 이 패턴을 표준 `ReadableStream`으로 그대로 받쳐준다.

```ts
const stream = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", {
  messages: [{ role: "user", content: question }],
  stream: true,
});

return new Response(stream, {
  headers: { "content-type": "text/event-stream" },
});
```

`stream: true` 한 줄이 전부다. 반환되는 값이 `ReadableStream`이라 그대로 Response에 얹어 SSE(Server-Sent Events)로 흘려보낼 수 있다. Worker는 이 stream이 끝날 때까지 살아 있되, CPU 시간은 토큰을 가공하는 짧은 순간만 잡힌다. 외부 모델 응답을 기다리는 시간은 — 이미 익숙해졌듯이 — 비용 0이다.

같은 일을 Lambda에서 하려면 Function URL의 streaming 모드를 켜고 별도 응답 형식을 맞춰야 한다. Workers는 Web standards 그대로다. fetch handler 안에서 stream을 반환하면 끝. 이 작은 차이가 챗봇·코파일럿·코드 어시스턴트 같은 자리에서 코드 한 페이지를 줄여준다.

---

### Part 5. Vectorize + AI Gateway — fallback 체인까지

#### Vectorize — 글로벌 벡터 검색

작은 RAG 챗봇을 짠다고 해보자. 자기 회사 문서 1,000개를 임베딩해 벡터 DB에 저장하고, 사용자 질문이 들어오면 가까운 문서 5개를 찾아 LLM에 함께 던진다. 익숙한 그림이다. 벡터 DB 자리에 OpenSearch k-NN을 써도 되고, RDS에 pgvector를 얹어도 되고, Pinecone·Weaviate 같은 SaaS를 써도 된다. AWS에서는 최근에는 Knowledge Bases for Bedrock이 OpenSearch Serverless를 뒤에 두고 같은 일을 한 번 더 추상화한다 — 다만 region 단위 운영, IAM·VPC endpoint 한 줄, 그리고 매니지드 비용이 한 겹씩 따라온다.

Cloudflare에서는 이 자리를 **Vectorize**가 받는다. 한 줄로 잡자면 — **글로벌 분산 벡터 DB**다. 인덱스를 하나 만들고, 임베딩을 upsert하고, 쿼리 벡터로 nearest neighbor를 부른다. Workers·AI Gateway와 binding 하나로 매끄럽게 묶인다.

```ts
// 임베딩 저장
const embedding = await env.AI.run("@cf/baai/bge-small-en-v1.5", {
  text: ["edge computing reduces latency"],
});

await env.VECTORIZE.upsert([
  {
    id: "doc-1",
    values: embedding.data[0],
    metadata: { source: "intro.md", chunk: 0 },
  },
]);

// 검색
const queryEmbedding = await env.AI.run("@cf/baai/bge-small-en-v1.5", {
  text: ["how does edge work"],
});

const matches = await env.VECTORIZE.query(queryEmbedding.data[0], {
  topK: 5,
  returnMetadata: true,
});
```

`env.AI`로 임베딩을 만들고, `env.VECTORIZE`에 저장·검색한다. 두 binding이 Cloudflare 안에서 한 호흡으로 묶인다. 같은 일을 AWS에서 하려면 Bedrock embedding API → OpenSearch ingest → IAM role 두 개 → VPC endpoint 같은 세팅이 필요하다. Cloudflare 식으로는 binding 두 줄이다.

한도 한 번 짚자. 인덱스당 5M vector, 계정당 50k namespace까지 (2026 5월 기준). hobby·MVP에 충분한 규모이고, 중급 production까지는 무난히 견딘다. **다만 hybrid search(keyword + vector)는 미지원**이다. 큰 검색 시스템·복잡한 BM25+vector 결합이 필요한 자리라면 OpenSearch를 그대로 두는 편이 낫다.

다른 옵션과 비교 표 한 번 그려두자.

| 기준 | Vectorize | pgvector (RDS·Neon) | OpenSearch k-NN |
|---|---|---|---|
| 위치 | edge 글로벌 분산 | 기존 Postgres 안 | 별도 클러스터 |
| 운영 부담 | 매니지드, binding 한 줄 | 기존 RDS 운영에 흡수 | 별도 클러스터 운영 |
| Workers 통합 | binding 즉시 | Hyperdrive 경유 | HTTP fetch |
| 트랜잭션 | 없음 | RDB 트랜잭션 안에서 함께 | 없음 |
| 한도 | 5M vec/index | DB 단일 스케일 | 클러스터 스케일 |
| Hybrid search | 미지원 | extension 조합 가능 | 기본 지원 |

선택은 자기 워크로드를 펼쳐 보면 답이 나온다. **이미 RDS를 쓰고 vector도 RDB 트랜잭션에 묶이길 원한다면 pgvector**, **이미 OpenSearch에 full-text가 있고 vector를 한 번 더 얹는 거라면 OpenSearch**, **새 RAG·검색 시스템을 글로벌하게 가볍게 깐다면 Vectorize**. 5장의 결정 매트릭스를 한 번 더 펼쳐 자기 자리를 찾자.

#### AI Gateway — AWS에 정확한 등가물이 없는 자리

이제 이 장에서 가장 흥미로운 도구로 가자. **AI Gateway**다. AWS에 정확한 등가물이 없다. Bedrock도, SageMaker도 같은 자리를 채우지 않는다. 직접 구축하거나, Portkey 같은 외부 SaaS를 쓰는 게 일반적이었다.

AI Gateway가 무엇인가. 한 줄로 — **LLM 요청을 가로채는 프록시**다. 70+ 모델, 12+ provider(OpenAI, Anthropic, Google, Cohere, Workers AI, Bedrock 등)를 단일 endpoint로 묶는다. 그 위에 다음을 얹는다.

- **캐싱**. 같은 prompt에 같은 응답이 짧은 시간 안에 반복되면 캐시 hit. 최대 90% 지연 감소·비용 절감.
- **rate limit**. provider별·앱별·사용자별로 제한.
- **retries**. 일시적 장애 시 자동 재시도.
- **fallback**. OpenAI가 죽으면 Anthropic으로, 둘 다 죽으면 Workers AI로.
- **observability**. 토큰 수·비용·latency를 한 대시보드에서.

이 다섯 가지가 한 제품에 묶여 있다는 점이 핵심이다. 자체 구축하면 다섯 개 인프라를 따로 운영해야 한다.

#### OpenAI → Anthropic → Workers AI fallback 체인

코드로 한 번 그려보자. AI Gateway endpoint를 하나 만들고, OpenAI 호환 SDK로 호출하면 된다. 호출 URL만 AI Gateway로 바꾸면, 그 뒤로는 우리가 설정한 라우팅·fallback이 자동으로 적용된다.

```ts
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: env.OPENAI_API_KEY,
  baseURL: `https://gateway.ai.cloudflare.com/v1/${env.CF_ACCOUNT_ID}/${env.GATEWAY_NAME}/openai`,
});

const response = await client.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [{ role: "user", content: question }],
});
```

`baseURL`을 AI Gateway로 바꿔준 게 사실상 전부다. 우리 코드는 OpenAI를 부르는 평범한 SDK 호출. 그 뒤로 Cloudflare가 다음을 한다.

1. **캐시 확인**. 같은 prompt·같은 모델·TTL 안쪽이면 캐시된 응답을 즉시 돌려준다.
2. **OpenAI 호출 시도**. 성공하면 응답 + 토큰 사용량을 대시보드에 적는다.
3. **실패 시 fallback**. AI Gateway에 fallback rule을 설정해두면, OpenAI 5xx·timeout이 발생했을 때 Anthropic 같은 다른 provider로 자동 재시도한다.
4. **마지막 fallback**. Anthropic도 죽으면 Workers AI Llama 모델로 — 카탈로그가 좁아도 "응답이 없는 것보다는 낫다"는 자리에 어울린다.

fallback rule은 AI Gateway 콘솔이나 API로 정의한다. "primary는 OpenAI, secondary는 Anthropic, tertiary는 Workers AI" 식으로 체인을 짜둔다. 우리 코드는 한 곳만 부른다 — `client.chat.completions.create`. 라우팅은 인프라가 한다.

캐싱도 한 번 더 짚자. AI Gateway의 캐시는 prompt 전체를 key로 잡되, 우리가 cache key를 직접 지정할 수도 있다 — 사용자별 응답이 섞이지 않게 user id를 cache key에 포함하는 패턴이 흔하다. 같은 시스템 prompt + 같은 사용자 질문 + 동일 사용자 → 캐시 hit. TTL은 우리가 정한다. FAQ 같이 응답이 거의 변하지 않는 자리에서 캐시 hit률이 가장 높다 — Cloudflare 자료에 따르면 동일 요청 90%까지 지연 감소가 가능하고, 그만큼 토큰 비용도 깎인다.

rate limit도 한 묶음 짚자. provider별·사용자별·앱별로 분당 호출 수·일당 토큰 수를 잡을 수 있다. 사용자가 우리 챗봇을 악용해 OpenAI 청구서를 폭발시키는 시나리오가 한 번 떠오르면 — 끔찍하다 — 이 한 줄이 중요해진다. 자체 구축이라면 Redis + 토큰 버킷을 직접 짜야 하는 자리가 콘솔에서 한 번에 잡힌다.

이 그림이 왜 정직한가. 한 provider에 lock-in되지 않는다는 뜻이다. OpenAI 가격이 오르면 baseURL은 그대로 둔 채 라우팅을 Anthropic 우선으로 바꾸면 된다. 코드는 손대지 않는다. AWS에서 같은 일을 하려면 자체 게이트웨이를 짜거나, Portkey 같은 외부 SaaS를 한 겹 더 두는 식이다. AI Gateway는 그 한 겹을 Cloudflare 인프라가 직접 제공한다는 점에서 자리가 다르다.

#### Bedrock 앞에 AI Gateway를 두는 패턴

한 가지 더. AI Gateway는 **Bedrock도 provider로** 받는다. AWS에 모델이 묶여 있어 옮길 수 없는 회사도, AI Gateway를 앞단에 두면 캐싱·관측·rate limit·fallback의 이득은 그대로 얻는다.

```
[Worker] → [AI Gateway] → [Bedrock (Anthropic Claude)]
                       ↘ [OpenAI (fallback)]
                       ↘ [Workers AI (last resort)]
```

이 그림이 14장에서 강조하는 하이브리드 패턴 중 하나다. AWS 안의 모델은 그대로 두고, Cloudflare는 그 앞의 게이트웨이만 채운다. lock-in이 얇아지고, 옮길 자유는 늘어난다.

#### 작은 RAG 챗봇 한 사이클

이 장의 모든 도구를 한 줄에 꿰어보자.

1. **문서 임베딩 ingest** (Workflow): R2의 마크다운 문서를 chunk로 쪼개고, 각 chunk를 Workers AI 임베딩 모델로 변환해 Vectorize에 upsert. 한 번에 1,000건이면 step.do로 100개씩 10번 나눠 묶는다.
2. **사용자 질문 처리** (HTTP Worker): 질문을 받으면 임베딩하고 Vectorize에서 top-5 chunk를 찾는다.
3. **LLM 호출** (AI Gateway 경유): top-5 chunk를 context로 넣어 OpenAI에 질문. AI Gateway가 캐시·fallback·관측을 처리한다.
4. **응답 캐시 hit 시** 같은 질문 두 번째에는 ms 단위로 답이 돌아온다 — 90% 비용 절감의 자리가 여기다.
5. **저빈도 분석 작업**은 cron trigger로 매일 새벽 한 번 돌려, "어제 가장 많이 물은 질문 톱10"을 D1에 적어둔다.

이 한 사이클이 우리 누적 프로젝트 `toby-shop`의 어드민 옆에 작은 RAG 챗봇으로 붙는다. Workflow·Queue·Cron·Workers AI·Vectorize·AI Gateway가 한 사이클에 다 등장한다.

#### 무너지는 자리 — Vectorize + AI Gateway의 한계

- **Vectorize는 hybrid search 미지원** (2026 기준). BM25 + vector를 함께 써야 하는 검색 시스템이라면 OpenSearch가 더 정직하다.
- **AI Gateway는 신생 영역**이다. provider 추가·rule 문법·대시보드 UI가 자주 변한다. production에서 핵심 경로로 의존한다면, fallback 자체의 fallback도 떠올려두자 — AI Gateway가 잠깐 흔들릴 때 우리 시스템이 어떻게 보일지.
- **캐시 일관성**. AI Gateway 캐시는 LLM 응답을 그대로 캐싱한다. 사용자별·세션별 응답이 섞이지 않게 cache key 설계를 한 번 짚어야 한다 (잘못하면 다른 사용자의 응답이 보일 수 있다 — 끔찍한 일이다).
- **provider별 차이**가 fallback에서 드러난다. OpenAI와 Anthropic은 응답 형식이 다르다. fallback이 일어났을 때 client 코드가 모든 provider 형식을 처리할 수 있어야 한다 — AI Gateway가 어느 정도 정규화를 해주지만, 완벽하지는 않다.

---

### 실습 정리 — 이 장의 결과물

이 장에서 손가락으로 만든 것들을 한 자리에 모으자. `toby-shop` 누적 프로젝트의 12장 체크포인트(`ch12-async-ai`)에 다음이 더해진다.

- **결제 후 영수증 발송 Workflow** — 주문 검증 → 영수증 PDF 렌더 → R2 저장 → 이메일 Queue push → 30분 sleep → 후속 안내 메일. `step.sleep`이 비용 0이라 sequence를 늘려도 한 달 청구서가 흔들리지 않는다.
- **Mail Queue + Dead-letter Queue** — Workflow에서 떼어낸 이메일 발송이 별도 Worker consumer로 돌고, 외부 SMTP 흔들림을 retry·DLQ로 흡수한다.
- **매시 health check Cron + Alert Queue** — `[triggers] crons` 한 줄로 매시 정각에 외부 endpoint 5개를 점검하고 실패를 슬랙으로 fan-out.
- **작은 RAG 챗봇** — Vectorize에 회사 문서 임베딩, AI Gateway 경유 OpenAI → Anthropic → Workers AI fallback 체인. 같은 질문 두 번째에는 캐시 hit으로 응답이 즉각 돌아온다.

이 네 가지가 어드민 옆에 한 사이클로 묶여 있다. `wrangler tail`로 로그를 보면 Workflow 인스턴스가 step별로 진행되는 모습, Queue consumer가 batch로 처리하는 모습, cron 발화 로그, AI Gateway의 cache hit 로그가 함께 흐른다.

### 마무리

이 장이 길었다. 다섯 도구를 한 호흡에 다뤘으니 그럴 수밖에 없다. 한 번에 다 외울 필요는 없다 — 자기 시스템에 어떤 자리가 있는지를 5장의 결정 매트릭스 위에서 다시 펼쳐 보자. Step Functions가 무겁게 느껴졌던 자리에는 Workflows를 떠올리고, SQS 옆자리에는 Queues, `@Scheduled`·EventBridge Scheduler 자리에는 Cron Trigger, Bedrock 옆이나 앞에는 Workers AI·AI Gateway가 들어설 자리가 있다.

기억해두자 — 이 다섯 도구는 따로따로 빛나지 않는다. **함께 묶일 때** 가장 잘 빛난다. Workflow가 큰 흐름을 잡고, Queue가 외부 의존을 흡수하고, Cron이 정기 작업을 켜고, AI Gateway가 LLM 호출을 정돈한다. 한 도구만 도입하면 "또 하나의 SaaS 호출"처럼 보이지만, 다섯이 binding으로 매끄럽게 묶이면 한 멘탈로 잡히는 sequence가 된다.

물론 모든 자리가 매끄럽지는 않다. Workflows는 AWS 서비스 통합 깊은 워크플로를 옮기는 데 부담이 있고, Queues는 strict global ordering을 약속하지 않으며, Workers AI는 모델 라인업이 좁고, AI Gateway는 신생 영역이라 자주 변한다. 이 한계들을 인정하고 자기 자리에 맞을지 가늠하는 일이 5장 결정 프레임의 또 한 번의 적용이다.

다음 장에서는 이 모든 도구를 production에서 굴리는 일의 정직한 무게를 다룬다. **운영과 정직한 한계**다. 비용 모델의 함정, observability 공백, 2025년 두 차례의 outage가 가르쳐 준 것, vendor lock-in을 어떻게 안고 갈지. 이 책이 광고서가 아님을 가장 분명히 드러내는 장이 다음 페이지에서 펼쳐진다.

---


## 13장. 운영과 정직한 한계 — 비용·관측·outage·lock-in

Cloudflare로 옮긴 지 석 달째, 청구서가 도착했다고 해보자. 마이그레이션 발표 자리에서 우리가 약속한 숫자가 있다. "월 비용 60% 절감, p95 응답시간 200ms 단축." 청구서를 열어보니 줄어들긴 했다. 그런데 예상한 만큼은 아니다. 어디선가 한 줄씩 새고 있다. R2 storage 옆에 Class A operations이라는 항목이 처음 보는 숫자로 찍혀 있다. Workers 요청 수는 전월 대비 두 배가 넘는다. 코드를 바꾼 적이 없는데 왜 그럴까. 청구서를 한참 들여다봐도 어디서 새는지 잘 안 보여서 찜찜하다. 슬랙으로 물어보는 사이 Hacker News 첫 페이지에 빨간 글씨가 떠 있다. "Cloudflare global outage." 이번 분기만 두 번째다. 옆 자리 동료가 묻는다. "이거, 옮긴 거 잘한 결정 맞아?" 답하기가 난감하다.

이 자리에서 우리는 정직해야 한다. 책의 앞 12장에서 우리는 Workers의 콜드스타트, R2의 egress free, Hyperdrive의 round-trip 흡수 같은 약속을 살펴봤다. 약속은 진짜다. 하지만 약속이 진짜라는 사실과, 그 약속이 우리 워크로드에서 우리가 기대한 모양으로 작동한다는 사실은 다른 이야기다. 이 책이 Cloudflare 광고가 아니라는 사실을 가장 분명히 드러내야 하는 자리가 바로 이 장이다. 함께 살펴보자. 비용이 어디서 새는지, 관측이 어디서 비는지, 장애가 났을 때 우리가 어디까지 흔들릴 수 있는지, 그리고 한번 들여놓은 Cloudflare를 다시 빼낼 때 어떤 자리에서 발이 묶이는지.

### "I/O 대기 무료"라는 약속이 깨지는 자리

먼저 가격이다. Workers Standard의 가격 모델은 한 줄로 요약된다. **CPU time × 요청 수, I/O 대기는 무료.** Lambda가 메모리·실행 시간(GB-s) × 요청 수로 과금하면서 외부 API 응답을 기다리는 동안에도 비용이 흐르는 것과 정반대다. AI Gateway를 거쳐 LLM을 호출하고 5초씩 응답을 기다리는 워크로드, S3에서 큰 객체를 읽어 변환 없이 그대로 흘려보내는 프록시 워크로드, 외부 결제 게이트웨이의 webhook을 기다리는 워크플로 — 이런 자리에서는 비용 차이가 자릿수 단위로 벌어진다.

Baselime이 공식 블로그에 쓴 사례가 자주 인용된다. AWS Lambda + ECS 위에 돌던 시스템을 3명이 3개월 안에 Workers로 풀 마이그레이션했더니 일 비용이 $790에서 $25로 떨어졌다. 95% 절감이다. 인상적인 숫자다. 그런데 이 숫자를 우리 시스템에 그대로 갖다 붙이려고 하면 첫 번째 함정이 나타난다. **Baselime의 워크로드는 정확히 Workers 가격 모델이 빛나는 형태였다.** 외부 데이터를 받아 가볍게 가공해 다시 외부로 보내는 옵저버빌리티 백엔드. CPU 무거운 연산은 거의 없고, 거의 모든 시간이 I/O 대기다. Workers 가격 모델은 이런 워크로드를 위해 설계됐다고 봐도 과언이 아니다.

우리 워크로드가 그 모양이 아니라면 어떨까? 예컨대 무거운 JSON parsing, 큰 zod 스키마 검증, 이미지 메타데이터 추출, 암호화 연산 위주의 워크로드라면. 이런 자리에서는 CPU time이 그대로 잡히고, "I/O 대기 무료"의 이점이 거의 적용되지 않는다. Workers의 단가가 Lambda보다 저렴할 수는 있어도 "95% 절감" 같은 숫자는 절대 안 나온다. 운이 나쁘면 별 차이가 없거나, 요청 수가 매우 많은 워크로드(예: 작은 이미지를 초당 수천 번 transform)에서는 Workers 쪽이 미세하게 더 비쌀 수도 있다.

한 가지 더 짚어두자. **Workers 가격 모델은 "외부 API 대기는 무료"인 대신 동시 연결 수에는 한도가 있다.** 한 isolate가 동시에 열 수 있는 outbound 연결은 6개로 제한된다. 평소에는 신경 쓸 일이 없지만, 한 요청 안에서 외부 API를 8개·10개씩 fan-out하는 패턴(예: 한 사용자 요청에 여러 microservice를 한꺼번에 호출하는 BFF 패턴)에서는 이 한도가 곧 응답 시간으로 잡힌다. 7번째 연결은 6번째가 끝날 때까지 큐에 줄을 선다. Lambda에서는 이런 한도가 메모리 단위로 훨씬 느슨하다. 이걸 모르고 옮기면 "왜 같은 코드인데 Workers에서 두 배 느리지?"라는 의문이 한참 풀리지 않아 번거롭다.

또 하나의 함정은 Workers의 **CPU time 한도 자체**다. Workers Standard는 한 요청당 30초의 CPU time까지 허용한다(실제 wall clock은 더 길어도 된다). 30초 안에 끝나는 워크로드라면 충분하지만, 한 요청 안에서 큰 데이터를 정렬하거나 복잡한 검색을 돌리는 워크로드라면 이 한도에 부딪힌다. AWS Lambda는 메모리 단위로 15분까지 허용하기 때문에 한도 감각 자체가 다르다. 이런 자리는 12장의 Workflows로 분해하거나, 아예 ECS에 남기는 편이 낫다.

그렇다면 결정의 첫 단추는 무엇일까. **우리 워크로드의 시간 중 몇 퍼센트가 I/O 대기인지 한 번 측정해보자.** Lambda에서 X-Ray로, ECS에서 APM으로 측정할 수 있다. 80% 이상이 I/O 대기라면 Workers 가격 모델은 우리 편이다. 50% 안팎이라면 비용은 비슷하거나 약간 절감되는 수준이다. 30% 미만, 즉 CPU bound 워크로드라면 비용보다는 글로벌 분산·콜드스타트 같은 다른 이점에서 가치를 찾아야 한다. "egress free 때문에 옮긴다"가 의사결정의 시작점이 되면 이 측정 단계가 통째로 빠지는 경우가 많다. 청구서를 받기 전까지는 모른다. 받고 나면 늦다.

### R2 egress free의 얇은 진실

가격에서 가장 화려한 약속은 R2의 egress free다. S3 Standard에서 30TB를 한 달 동안 다운로드하면 약 $2,700이 나온다. 같은 양을 R2에서 받으면 storage 비용 외에는 0이다. 미디어 스트리밍, 백업 다운로드, AI 모델 가중치 배포처럼 outbound가 큰 워크로드에서는 절감 폭이 90~99%에 이르는 사례가 흔하다. 책 1장에서도 같은 약속을 적었다. 이 약속은 진짜다. 하지만 진짜 약속과 현장에서 우리가 받는 청구서 사이에는 세 가지 함정이 있다.

첫째, **R2는 egress가 free일 뿐 storage와 operations은 free가 아니다.** 2026년 5월 기준 가격으로 storage가 GB당 월 $0.015, Class A operations(쓰기·list·multipart) 100만 건당 $4.50, Class B operations(읽기·head) 100만 건당 $0.36이다. 이 단가만 보면 S3보다 저렴해 보이지만, 작은 객체를 매우 많이 읽고 쓰는 패턴에서는 operations 비용이 한 달에 storage 비용을 넘어서기도 한다. 100만 건당 몇 달러가 별것 아닌 것 같지만, 1초에 1,000건 read가 한 달이면 26억 건이 넘는다. 갑자기 청구서에 $1,000짜리 줄이 하나 더 생긴다. 미디어 한 덩어리를 통째로 받는 워크로드와, 작은 메타데이터 객체를 초당 수천 번 읽는 워크로드는 같은 R2라도 비용 모양이 완전히 다르다.

둘째, **inbound는 free이지만 inbound를 일으키는 쪽의 egress는 그대로 잡힌다.** 마이그레이션 첫 달, S3에서 30TB를 R2로 옮긴다고 해보자. R2 입장에서는 inbound 0원이지만 AWS 입장에서는 그게 30TB의 egress다. CloudFront를 통하면 약 $2,500 안팎, 직접 S3에서 받으면 더 비싸다. 옮긴 다음 달부터는 절감되지만, 옮기는 그 한 달의 청구서가 깜짝 놀랄 만큼 커질 수 있다. 이건 함정이라기보다는 회계의 문제다. 옮길 가치가 충분히 있는 결정이라도 의사결정 라인에서 "첫 달 청구서가 평소보다 $2,500 더 나옵니다"라는 한 줄을 빼먹으면 신뢰가 흔들린다. 미리 말해두는 편이 낫다.

셋째, **R2가 흡수하지 못하는 enterprise 기능들이 있다.** Lifecycle policy의 일부, Glacier 같은 cold storage tier, Object Lock, S3 Inventory, Replication의 일부 — 이런 기능에 의존하던 워크로드는 R2로 옮긴 직후가 아니라 한두 달 뒤 운영 자동화 스크립트가 깨지는 형태로 문제가 드러난다. 옮기기 전에 우리 S3 버킷에 어떤 기능이 켜져 있는지 한 번 점검하자. AWS 콘솔에서 "Properties" 탭과 "Management" 탭을 한 번씩 둘러보는 것만으로도 미리 발견되는 함정이 많다.

한 가지 시뮬레이션을 해보자. 월 30TB outbound, 200만 객체, 객체당 평균 read 5회·write 0.2회인 미디어 서빙 워크로드를 가정한다. S3 Standard에서는 storage $1,380 + egress $2,700 + 작은 ops 비용 = 약 $4,100/월. 같은 워크로드를 R2로 옮기면 storage $900 + egress $0 + Class A ops($1) + Class B ops($3.6) = 약 $905/월. 단순 비교로 78% 절감이다. 이게 정직한 R2의 강점이다. 하지만 같은 30TB가 작은 객체(예: 1KB 메타데이터)를 1억 건씩 read하는 패턴이라면? Class B ops만 100M × $0.36/M = $36/월. 별것 아닌 것 같지만 객체가 매우 많고 자주 읽히는 패턴에서는 ops 비용이 storage 비용을 추월하기도 한다. 우리 워크로드의 객체 크기 분포와 read/write 빈도를 한 번 측정하자. R2 절감폭은 미디어처럼 큰 객체일수록 압도적이고, 작은 객체 다량 패턴일수록 평범해진다.

### KV·D1·DO·Workflows·Queues — 가격 모양의 한 표

R2와 Workers는 익숙한 가격 모델 비교가 가능하지만, KV·D1·Durable Objects·Workflows·Queues는 AWS에 그대로 매핑되는 등가물이 없어서 가격 모양이 머릿속에 잘 안 그려진다. 한 표로 정리해두자. 외울 필요는 없고, 결정할 때 한 번 펼쳐보면 된다.

| 제품 | 과금 차원 | 무료 한도 | 핵심 함정 |
|---|---|---|---|
| **Workers Standard** | CPU time + 요청 수, I/O 대기 무료 | 일 100k 요청 (free plan) | CPU bound 워크로드는 절감폭 작음 |
| **R2** | storage + Class A/B operations, egress free | 10GB storage, 작은 ops 한도 | 작은 객체 다량 read·write 시 ops 비용 누적 |
| **KV** | read/write/delete 단위 + storage | 일 100k read, 1k write | per-key 1 write/s 한도, 요청 수가 곧 비용 |
| **D1** | rows read/written + storage | 일 5M rows read, 100k written | sustained write 500~2k/s 한도, 큰 쿼리는 read 카운트 폭증 |
| **Durable Objects** | requests + duration + storage | paid only | hibernation 켜지 않으면 long-lived 연결이 통째로 비용 |
| **Workflows** | 실행 중 CPU time만 (sleep·외부 대기 무료) | paid 한도 | 비용 모델은 강력하지만 instance 수 자체가 늘어나면 storage 누적 |
| **Queues** | 메시지 단위 (write·read·retry) | 일 100k operations | DLQ로 무한 retry 돌면 비용 폭주 |
| **Hyperdrive** | 무료 (paid plan 필요) | — | DB 자체 비용은 그대로, 캐시 hit률에 따라 효과 차이 큼 |

이 표를 처음 받아 들면 "AWS보다 단순하네"라는 인상을 받을 수 있다. 그런데 함정은 단순함의 뒷면에 있다. AWS는 거의 모든 항목에 자세한 단가표가 있고 Cost Explorer로 시간 단위 추적이 된다. Cloudflare는 단가가 단순한 대신 **항목별 추적의 깊이가 얕다.** 어떤 Workers route가 비용을 일으키는지, 어떤 D1 쿼리가 read를 폭증시키는지를 한눈에 보기가 의외로 쉽지 않다. 대시보드의 Analytics는 대개 합산값을 보여주고, 항목별 분해는 Logpush로 외부 sink에 넣어 직접 분석해야 한다. 이게 다음 절의 주제다.

### 같은 트래픽, 두 청구서 — 한 시뮬레이션

가격을 추상적으로만 다루면 결정에 별 도움이 안 된다. 한 가상 시나리오를 세워 두 청구서를 나란히 놓아보자. 1장과 14장에서도 비슷한 시나리오를 등장시키지만, 여기서는 비용 항목을 한 줄씩 풀어 보는 게 목적이다.

**가정.** 월간 활성 사용자 50만 명 규모의 SaaS. AWS 위에 돌고 있다.
- 월 1억 건의 API 요청 (스파이크 시 초당 5,000)
- API 평균 wall clock 200ms, 그중 CPU 30ms·I/O 대기 170ms
- DynamoDB read 월 5억 건·write 월 2,000만 건 (사용자 세션 + 메타데이터)
- S3에 저장된 사용자 미디어 20TB, 월 30TB outbound
- CloudFront 통한 전 세계 사용자
- CloudWatch Logs·Metrics 월 약 $600
- 월 총 비용 약 $9,000

**AWS 위에서 청구서 분해.**
| 항목 | 월 비용 |
|---|---|
| Lambda (1억 요청 × 평균 200ms × 512MB) | ~$2,400 |
| API Gateway (1억 요청) | ~$350 |
| DynamoDB on-demand | ~$1,200 |
| S3 storage (20TB) | ~$460 |
| S3 + CloudFront egress (30TB) | ~$2,700 |
| CloudWatch | ~$600 |
| 데이터 전송·기타 | ~$1,290 |
| **합계** | **~$9,000** |

**Cloudflare로 옮긴 시나리오.** API는 Workers + Hono로, 세션은 KV, 메타데이터는 D1, 미디어는 R2. CloudFront는 Cloudflare CDN으로 흡수. 외부 APM은 Sentry Team plan 월 $80을 도입.

| 항목 | 월 비용 |
|---|---|
| Workers (1억 요청 × 평균 30ms CPU) | ~$700 |
| KV (5억 read + 2,000만 write) | ~$200 |
| D1 (메타데이터) | ~$50 |
| R2 storage (20TB) + ops | ~$320 |
| R2 egress (30TB) | $0 |
| Cloudflare CDN | 무료 (Pro plan $20 포함) |
| Logpush + Sentry | ~$130 |
| **합계** | **~$1,420** |

이 시나리오에서 절감폭은 약 84%다. **그런데 이 숫자에는 한 줄로 잡히지 않는 비용이 빠져 있다.** 마이그레이션 자체의 인건비, S3 → R2 첫 inbound 전송 비용($2,500 안팎의 일회성), Workers 코드를 다시 짜는 시간(API당 평균 1~3일), 외부 APM 학습 비용, Cloudflare 운영 노하우를 쌓는 시간. 이런 비용을 다 더하면 첫 6개월 동안은 절감폭이 거의 없거나 오히려 마이너스일 수 있다. 6개월이 지난 다음부터 진짜 절감이 시작된다. **그래서 Cloudflare 마이그레이션은 분기 단위 의사결정이 아니라 연 단위 의사결정이다.**

또 하나 짚자. 위 시나리오는 **워크로드가 Workers 가격 모델에 맞을 때**의 그림이다. CPU bound 워크로드, 또는 작은 객체를 매우 많이 read하는 워크로드, 또는 한 요청에 많은 fan-out이 일어나는 워크로드라면 절감폭이 30~50% 수준으로 떨어질 수도 있다. 이 책의 표를 그대로 우리 시스템에 갖다 붙이지 말자. 우리 시스템의 항목별 측정이 우선이다. AWS Cost Explorer에서 한 달 비용을 항목별로 뽑고, 위 시뮬레이션 표의 자리에 우리 숫자를 넣어보자. 이게 가장 정직한 결정의 출발점이다.

### CloudWatch에 익숙한 눈으로 보면 빠진 것들

Cloudflare로 옮기고 한 달쯤 지나면 운영하는 사람의 손이 자꾸 비는 듯한 묘한 감각이 든다. CloudWatch에서 익숙하게 누르던 자리들이 비어 있다. 메트릭은 어디서 보지, alarm은 어떻게 거는 거지, 분산 트레이스는 어디에 있지. 처음에는 "내가 아직 못 찾은 거겠지" 싶다. 그러다 곧 깨닫는다. **CloudWatch처럼 한 제품으로 흡수된 옵저버빌리티가 Cloudflare에는 없다.** 이건 대놓고 인정해야 할 한계다.

Cloudflare가 제공하는 옵저버빌리티는 대략 네 조각이다.

**Workers Analytics**는 대시보드에 들어가면 가장 먼저 보이는 화면이다. 요청 수, 에러율, CPU time 분포, status code 분포 — 합산값은 모두 여기 있다. 시각화도 깔끔하다. 한 가지 단점은 항목별 분해가 얕다는 점이다. "어느 route가 5xx를 내고 있는지"까지는 보이지만, "그 5xx의 stack trace는 무엇인지"는 다른 도구가 필요하다. CloudWatch Logs Insights에서 한 줄 쿼리로 끝났던 일을 두세 도구에 걸쳐 풀어야 하니 처음엔 번거롭다.

**`wrangler tail`**은 실시간 로그 tail이다. CloudWatch Logs Insights의 실시간 부분과 비슷하다. 개발 중이거나 incident response 시 1차 도구로 강력하다. 단, 영속이 안 된다. 터미널을 닫으면 끝이다. "어제 새벽 3시의 그 에러"를 다시 보고 싶으면 못 본다.

**Tail Workers**는 한 Worker에 또 다른 Worker를 붙여 모든 요청·응답을 가공해 내보내는 메커니즘이다. dynamic sampling을 여기서 처리할 수 있다. 모든 요청을 다 내보내면 Logpush 비용이 너무 커지니까, 에러만 100% 샘플, 정상은 1%만 샘플 — 이런 정책을 Tail Worker 코드 안에서 정한다. CloudWatch에서 "log group의 retention과 filter pattern을 켠다"의 자리를 코드 한 덩어리가 대신한다. 자유도가 높은 대신 우리가 코드를 책임진다.

**Logpush**는 모든 옵저버빌리티의 종착지에 가깝다. Workers Logs, HTTP request logs, Firewall events 같은 데이터를 R2·S3·Datadog·New Relic·Splunk 같은 외부 sink로 push한다. 100만 요청당 약 $0.05의 단순한 비용 모델이다. **이게 사실상 Cloudflare 옵저버빌리티의 표준 패턴이다.** Cloudflare 자체에서 검색·alerting을 하는 게 아니라, Logpush로 외부 APM에 보낸 다음 거기서 한다.

여기서 정직한 권장은 이렇다. **Cloudflare를 쓴다는 결정은 외부 APM을 쓴다는 결정과 묶여 있다.** Datadog, New Relic, Honeycomb, Sentry, Baselime, Axiom — 어느 하나는 나란히 쓰는 편이 낫다. CloudWatch 한 제품의 자리를 Cloudflare 자체 도구만으로 채우려고 하면 어딘가에서 손이 빈다. Sentry는 에러 추적이 강하고, Honeycomb은 high-cardinality 트레이스가 강하고, Datadog은 풀스택을 다 잡아준다. 우리 팀이 이미 쓰던 APM이 있다면 그걸 Logpush sink로 그대로 잇는 편이 가장 부드럽다. 새로 도입한다면 작은 팀에는 Sentry, 트레이스 위주라면 Baselime이나 Axiom이 가성비가 좋다.

한 가지 자주 빠뜨리는 것이 있다. **외부 APM 비용을 Cloudflare 절감폭에서 차감하고 결정해야 한다.** Cloudflare로 옮겨 월 $3,000이 절감됐는데 Datadog Pro plan을 새로 들이면서 $1,200이 추가됐다면, 실질 절감은 $1,800이다. CloudWatch 비용이 사라진 자리를 외부 APM이 일부 채우는 형태로 봐야 한다. 트래픽 규모와 호스트 수에 따라 외부 APM 비용도 만만치 않다. 도입 전에 한 번 견적을 받아보자.

Sentry나 Baselime 같은 작은 APM을 Logpush sink로 잇는 코드는 의외로 간단하다. Cloudflare 대시보드에서 Logpush job을 만들고, destination에 외부 sink의 HTTPS endpoint를 적고, 어떤 dataset을 어떤 필터로 보낼지 정한다. 5분이면 끝난다. 그 다음에 Tail Worker로 sampling을 정교하게 다듬는다. 이 두 자리가 우리 옵저버빌리티 파이프라인의 척추가 된다.

마지막으로, **alarm·notification은 누구의 자리인가.** CloudWatch는 alarm·SNS·Lambda를 한 줄로 잇는 통합이 자연스럽다. Cloudflare는 Notifications라는 자체 알림 시스템이 있긴 하지만, 우리가 짠 운영 룰을 한 줄로 옮기기에는 부족할 수 있다. 결국 외부 APM의 alerting을 쓰거나, Workers 안에 자체 alerting 로직을 짜서 Slack/PagerDuty webhook을 부르는 형태가 흔하다. 이것도 코드의 책임이 된다는 사실을 받아들이자. CloudWatch에서 클릭 몇 번으로 끝나던 일이 코드 한 덩어리가 된다. 자유도가 높은 만큼 책임도 우리가 진다.

여기서 한 가지 더 짚자. **분산 트레이스는 Cloudflare 자체로는 부족하다.** Workers Trace Events라는 게 있긴 하지만 X-Ray만큼 깊지 않다. Worker가 다른 Worker를 부르고, 그 Worker가 D1과 R2를 부르고, 그 사이 Workflows가 끼어 있는 시스템을 한 화면에서 보고 싶다면 OpenTelemetry instrumentation을 코드에 직접 넣고 외부 APM에 보내는 게 표준이다. CloudWatch의 X-Ray 통합처럼 자동으로 그려지는 풀패키지는 아직 없다. "그래도 옮길 만한가?"의 답은 "외부 APM 비용을 추가로 감수할 수 있는가?"의 답과 같다.

### 2025년 11월 18일, 그리고 12월 5일

이제 가장 무거운 자리다. 2025년 한 해 동안 Cloudflare는 두 차례의 큰 글로벌 장애를 겪었다. 11월 18일과 12월 5일. 1장에서 한 단락으로 짚었지만, 이 책의 정직성을 위해서는 한 번 더 깊이 들여다봐야 한다.

**11월 18일 사건은 Bot Management 설정 파일이 발단이었다.** Cloudflare 내부에서 ClickHouse의 권한 설정을 변경했는데, 그 변경이 Bot Management가 사용하는 설정 파일의 크기를 두 배로 부풀렸다. 문제는 그 파일을 읽는 proxy가 크기 가정 위에 짜여 있었다는 점이다. 두 배가 된 파일이 들어오자 proxy가 panic을 일으켰다. Workers KV, Turnstile, 그리고 Cloudflare Dashboard 자체까지 줄줄이 영향을 받았다. 11:20 UTC부터 17:06 UTC까지 약 6시간 동안 부분 또는 전체 장애가 이어졌다. Cloudflare 공식 사후 분석은 블로그에 매우 상세히 공개되어 있다. 어느 정도냐 하면, "방어 코드 한 줄이 있었다면 막았을 사고"라는 점을 회사가 스스로 인정하고 적었을 정도다.

12월 5일은 다른 종류의 사건이었다. Hacker News에서는 두 사건이 그해 가장 토론이 많이 붙은 인프라 사건으로 기록되었다. 같은 분기에 두 번이라는 점이 사람들에게 가장 인상적이었다.

이 사건들에서 우리가 무엇을 배워야 할까. 단순히 "Cloudflare는 신뢰할 수 없다"고 결론짓는 건 게으른 반응이다. AWS도 us-east-1 장애가 나면 인터넷 절반이 멈춘다. GCP도 작년 큰 장애를 겪었다. 어떤 단일 클라우드도 SLA 100%를 약속하지 못한다. 그래서 우리가 던져야 할 질문은 다른 자리에서 시작한다.

**"Cloudflare를 쓸까 말까"가 아니라 "어디까지 의존할까"의 질문으로 옮기자.** 1장에서 한 약속을 여기서 다시 펼친다. critical path의 어느 자리까지 단일 벤더에 맡길 것인가. 결제, 로그인, 핵심 데이터 read — 이 세 자리는 어떤 벤더에 묶여 있어도 회피 전략이 필요하다.

회피 전략은 대체로 셋이다.

**첫째, Multi-CDN.** Cloudflare 한 곳에 DNS·CDN·WAF를 모두 맡기는 대신, 한 자리는 다른 사업자에게 둔다. AWS Route 53 health check + Cloudflare CDN + 보조 CDN(Akamai·Fastly)을 두고, Route 53 weighted routing으로 한쪽이 죽으면 다른 쪽으로 흘려보낸다. 운영 부담이 두 배 가깝게 늘어난다. WAF 룰을 두 군데에 동기화해야 하고, 캐시 무효화 명령도 두 군데에 보내야 한다. 작은 팀에는 권하지 않는다. 큰 트래픽을 받는 서비스라면 고려할 가치가 있다.

**둘째, DNS failover.** DNS는 Cloudflare로 가더라도 secondary DNS provider를 다른 곳에 둔다. NS1, AWS Route 53, Google Cloud DNS 같은 곳이 흔한 선택이다. Cloudflare DNS API의 secondary DNS 기능을 켜면 비교적 부드럽게 구성할 수 있다. DNS는 계층의 가장 위에 있어서 여기가 살아 있으면 다른 자리의 회피가 작동한다.

**셋째, dual-running.** 핵심 critical path를 Workers와 Lambda 양쪽에 동시에 둔다. Rebal AI라는 회사가 이 패턴을 운영한다는 사례가 자주 인용된다. 비용은 두 배 가깝다. 하지만 한쪽이 죽어도 서비스가 멈추지 않는다. 결제 같이 돈이 직접 걸린 경로에는 합리적이고, 단순 조회 API에는 과하다. 우리 시스템의 어느 경로가 진짜 critical인지 한 번 솎아내고, 그 자리에만 dual-running을 적용하는 편이 낫다.

여기서 더 정직한 한 줄을 적자. **이 책은 다음 outage가 언제 어떻게 날지 예측할 수 없다.** 11월 18일의 사건도, 12월 5일의 사건도 사후에야 패턴이 보인다. 우리가 사전에 할 수 있는 일은 critical path를 솎아내고 회피 전략을 미리 그려 두는 것까지다. 그 이상은 운에 맡기는 것에 가깝다. 정직한 운영자의 자세는 그것을 인정하는 데서 시작한다.

한 가지 더 짚을 자리가 있다. **Cloudflare의 사후 분석은 업계 평균보다 훨씬 자세하다.** 11월 18일 사건 블로그 포스트를 한 번 읽어보면 알 수 있다. 어느 시점에 어느 코드 경로가 어떻게 panic했는지, 왜 방어 코드가 없었는지, 어떤 모니터링이 작동하지 않았는지 — 이 정도까지 공개하는 회사는 AWS·GCP를 포함해도 흔치 않다. 이 점은 신뢰의 한 자락이 된다. "장애가 나도 되도록 빨리, 자세히, 정직하게 적는 회사"인지 아닌지는 oncall을 운영해본 사람에게는 결정적인 신호다. Cloudflare는 이 점에서는 모범적이다. 그래도 6시간짜리 장애가 분기에 두 번이라는 사실 자체는 별개의 이야기다. 두 사실을 같은 저울 위에 올려두고 우리 critical path를 들여다보자.

### "no lock-in"이라는 마케팅과 lock-in이라는 현실

Cloudflare 공식 문서와 블로그에는 "no vendor lock-in"이라는 표현이 자주 나온다. Workers 코드는 Web standards 기반이라 fetch·Request·Response 같은 표준 API를 쓴다. 이론적으로는 다른 edge runtime에 옮길 수 있다. Deno Deploy, Vercel Edge Runtime, AWS Lambda@Edge — 표준 API만 쓴 코드는 대체로 옮겨진다.

여기까지는 진짜다. 하지만 그 다음 한 줄이 더 진짜다. **Bindings·Durable Objects·D1·KV·Workflows·Queues의 API는 Cloudflare 고유다.** 이걸 쓴 코드는 옮길 수 없다. 정확히 말하면, 옮기려면 추상화 레이어를 한 겹 더 두거나 그 부분을 통째로 다시 짜야 한다. Hacker News의 한 토론(HN 29356036)에서 누군가 정확하게 표현했다. "Cloudflare는 'no lock-in'을 강조하지만 feature-level lock-in은 명백하다." 이 말이 옳다.

그렇다면 결정 프레임을 lock-in 축으로 한 번 다시 보자. 5장에서 옮길 자리·남길 자리를 결정할 때 우리가 썼던 5축에 한 축을 추가하는 거다. **이 컴포넌트가 Cloudflare 고유 API에 얼마나 깊이 박힐까?**

| Cloudflare 자리 | lock-in 깊이 | 표준 인터페이스 뒤에 둘 수 있나 |
|---|---|---|
| **Workers (코드)** | 얕음 | Web standards만 쓰면 portable |
| **R2 (storage)** | 얕음 | S3 호환 API. `aws-sdk` 그대로, endpoint만 바꿈 |
| **Hyperdrive (앞단)** | 얕음 | 뒤에 Postgres가 그대로. Hyperdrive 빼도 DB는 살아있음 |
| **KV** | 중간 | API는 단순. 추상화 한 겹으로 Redis·DynamoDB·다른 KV로 옮길 여지 |
| **D1** | 중간 | SQLite 호환. SQL 자체는 portable, 하지만 D1 client API는 Cloudflare 고유 |
| **Workflows** | 깊음 | step.do/sleep API는 Cloudflare 고유. 옮기려면 통째로 재작성 |
| **Queues** | 중간 | producer/consumer 패턴은 SQS·RabbitMQ로 옮길 수 있음. 단 retry 정책은 다시 |
| **Durable Objects** | 매우 깊음 | actor 모델 + 강한 일관성을 다른 곳에서 그대로 재현하기 어려움 |
| **AI Gateway** | 얕음 | 그냥 HTTP proxy. 빼도 Bedrock·OpenAI 직접 호출로 복원됨 |

이 표가 무엇을 말하는가. **lock-in의 깊이는 자리마다 다르다.** R2와 Hyperdrive는 빠져나가기 쉬운 자리다. R2는 endpoint만 S3로 돌리면 된다. Hyperdrive는 빼면 그냥 Postgres에 직접 붙는 코드로 돌아간다. AI Gateway는 빼면 model provider에 직접 호출하는 코드로 돌아간다. 이런 자리는 lock-in을 거의 걱정하지 않아도 된다.

반면 Durable Objects와 Workflows는 한 번 깊이 박히면 빠져나가기가 매우 어렵다. actor 모델 + per-entity 일관성 + 고정 위치 같은 본질적 특성을 다른 클라우드에서 한 제품으로 그대로 받쳐주는 곳이 사실상 없다. 옮기려면 Erlang/Elixir 클러스터를 직접 운영하거나, AWS에서 ECS + ElastiCache + 자체 라우팅 레이어로 actor 모델을 처음부터 짜야 한다. 이건 며칠이 아니라 몇 달의 일이다.

그렇다면 어떻게 해야 할까. 답은 단순하다. **lock-in이 깊은 자리에는 그 깊이를 감수해야 할 만큼의 가치가 있는 워크로드만 보낸다.** 채팅방, 실시간 협업 문서, per-user rate limiter — 이런 자리에서 Durable Objects의 가치가 압도적이라면 lock-in을 감수하는 게 합리적이다. 일반 CRUD를 Durable Objects에 박는 건 lock-in을 무료로 깊게 만드는 결정이다. 그러지 말자.

lock-in이 얕은 자리에는 부담 없이 들어가도 된다. R2, AI Gateway, Hyperdrive — 이 셋은 "Cloudflare를 시도해본다"는 결정의 진입점으로 가장 좋다. 빼기 쉬우니까 들이기도 쉽다. 1장에서 한 약속을 여기서 다시 적는다. "Cloudflare를 도입한다"가 아니라 "Cloudflare에 자리를 내준다." 자리는 lock-in의 깊이에 따라 다르게 내주자. 모든 자리를 다 내줄 필요도 없고, 모든 자리를 다 막을 필요도 없다.

### V8 패치 정책 — 빠른 보안의 양면

Cloudflare 운영에서 의외로 자주 토론되는 자리가 V8 패치 정책이다. **Cloudflare는 V8의 보안 패치를 Chrome stable 채널보다 먼저 production에 배포한다.** 보안 취약점이 발견되면 Chrome 사용자보다 Workers 사용자가 먼저 패치된 V8 위에서 코드를 돌리게 된다.

이게 어떤 의미인지 두 방향에서 봐야 한다.

**한 방향에서 보면 강점이다.** Spectre 같은 사이드채널 공격, V8 엔진의 zero-day가 보고된 직후 가장 빠르게 production에 패치가 도달한다. 우리 코드가 multi-tenant 환경에서 다른 고객의 코드와 같은 isolate pool 위에서 돈다는 사실을 떠올리면, 이 빠른 패치는 결정적이다. AWS Lambda는 microVM 격리라서 V8 단일 취약점에 좀 더 둔감하지만, Workers는 V8 단일 취약점이 곧 격리 모델 자체를 흔드는 일이 될 수 있다. 그래서 Cloudflare는 V8 보안에 매우 공격적으로 빠르게 움직인다. 이걸 못 마땅하게 볼 이유는 없다.

**다른 방향에서 보면 양날의 검이다.** Chrome stable에서 며칠 또는 몇 주 더 검증된 패치와, 패치되자마자 production에 들어간 패치는 안정성 면에서 다르다. Hacker News의 한 토론(HN 46458963)에서 정확히 이 자리가 논쟁이 됐다. 어떤 개발자는 "더 빠른 보안이 좋다"고 했고, 어떤 개발자는 "검증되지 않은 패치가 production에 먼저 들어오는 게 무섭다"고 했다. 둘 다 일리 있다.

여기서 정직한 한 줄을 적자. **어떤 워크로드는 한 박자 늦은 버전이 필요할 수 있다.** 결제·금융·의료처럼 안정성 SLA가 보안 SLA만큼 중요한 자리, 또는 V8 자체에 의존하는 매우 정교한 코드(예: 특정 정수 연산 동작에 의존하는 가상 머신)를 돌리는 자리. 이런 자리는 Workers 위에 올리는 게 자연스럽지 않을 수 있다. 대부분의 일반 웹 워크로드는 빠른 보안이 더 좋다. 하지만 모든 워크로드가 그런 건 아니라는 사실을 인정하는 게 정직함이다.

### "이 기술이 무너지는 자리" — 운영과 정직성 편

> **이 챕터 자체가 무너지는 자리.** 이 장은 의도적으로 정직한 한계를 다루지만, 그 정직함에도 한계가 있다.
>
> 첫째, **다음 outage는 예측할 수 없다.** 11월 18일과 12월 5일의 사건이 마지막이라는 보장이 없다. AWS·GCP도 마찬가지다. 우리가 할 수 있는 일은 critical path를 솎아내고 회피 전략을 미리 그려 두는 것까지다.
>
> 둘째, **가격 모델은 변동성이 크다.** 이 책의 표는 2026년 5월 기준이다. R2의 Class A/B operations 단가, KV의 free tier 한도, Workers AI의 Neuron 단가 — 이런 숫자는 분기 단위로 바뀐다. 결정 시점에 공식 페이지를 한 번씩 다시 확인하는 편이 낫다. 부록 E에 추적 가이드가 있다.
>
> 셋째, **lock-in의 깊이는 주관적이다.** 한 팀에는 깊은 lock-in이고, 다른 팀에는 그게 그렇게 깊지 않다. 추상화 레이어 한 겹을 짤 수 있는 팀과 그렇지 못한 팀의 결정이 같을 수 없다. 표는 평균값에 가깝다. 우리 팀의 코드 베이스, 마이그레이션 경험, 운영 인력에 따라 한 칸씩 위 또는 아래로 옮겨 읽자.
>
> 넷째, **이 책 자체에 시간 도장이 찍혀 있다.** 책이 출간된 시점과 우리가 이 페이지를 읽는 시점 사이에 어쩌면 1년이 흘렀을 수 있다. Workers Containers의 GPU 지원, Vectorize hybrid search, Vinext의 production 진입 — 이 책 출간 후 자리가 바뀌었을 영역이 있다. 부록 E의 추적 채널을 한번씩 점검하자.

### 운영 체크리스트 한 페이지

이 장에서 다룬 정직한 한계들을 운영 체크리스트로 압축해두자. 배포 전·배포 후·incident response·정기 점검 네 자리다.

**배포 전.**
- 우리 워크로드의 I/O 대기 비율을 한 번 측정했나
- R2로 옮길 버킷에 Lifecycle·Object Lock·Replication 같은 enterprise 기능이 켜져 있는지 확인했나
- Cloudflare 고유 API(DO·Workflows)를 쓰는 자리에 lock-in 가치가 충분한지 한 번 검토했나
- 외부 APM(Sentry·Datadog 등)을 Logpush sink로 잇는 코드를 같은 PR에 포함했나

**배포 후.**
- Workers Analytics 대시보드에 alarm·notification 규칙을 켰나
- Tail Worker로 dynamic sampling을 설정했나 (모든 요청 100% 샘플은 비싸다)
- 첫 한 주 청구서를 매일 한 번씩 들여다봤나
- DNS는 secondary provider에 동기화되어 있나

**Incident response.**
- `wrangler tail`을 즉시 띄울 수 있는 명령을 README에 적어두었나
- Cloudflare Status 페이지를 oncall 봇 알림에 묶어두었나
- critical path의 회피 전략(Multi-CDN·Lambda fallback)이 plan A와 plan B로 분리되어 있나
- 사후 분석을 우리 팀 위키에 적어두는 템플릿이 있나

**정기 점검 (분기).**
- Cloudflare 가격 페이지를 한 번 다시 봤나
- 우리 시스템에서 lock-in이 깊어지는 자리가 새로 생겼는지 확인했나
- 외부 APM 비용이 Cloudflare 비용 절감폭을 잠식하고 있지는 않은지 비교했나
- Compatibility Date를 한 번 점검했나 (너무 오래 묵으면 deprecated API 경고)

이 네 자리만 정기적으로 돌려도 운영의 8할은 잡힌다. 나머지 2할은 운과 경험의 영역이다.

### 마무리

이 장에서 우리는 가장 무거운 자리를 살펴봤다. Workers Standard의 가격 모델이 어디서 약속을 지키고 어디서 약속이 얇아지는지, R2 egress free의 진짜 의미와 Class A/B operations·inbound 청구서의 함정, CloudWatch에 익숙한 눈으로 보면 빠진 옵저버빌리티 조각들과 외부 APM이 사실상 표준 패턴이라는 사실, 2025년 두 차례 outage가 가르쳐준 "어디까지 의존할까"의 질문, lock-in의 깊이가 자리마다 다르다는 사실, 그리고 V8 보안 패치 정책의 양면성. 이 장 어디에도 "그래도 Cloudflare가 최고다"라는 결론은 없다. 광고는 다른 책이 하면 된다.

이 책의 자세를 한 줄로 다시 적자. **Cloudflare는 또 하나의 클라우드가 아니라 자리를 잘 골라 내주면 강점이 큰 edge-first 플랫폼이다. 그리고 운영자는 그 강점과 함께 한계도 함께 짊어진다.** 이 자세에서 출발하면 결정이 훨씬 쉬워진다. R2·AI Gateway·Hyperdrive처럼 lock-in이 얕은 자리는 부담 없이 들이고, Durable Objects·Workflows처럼 깊은 자리는 그 깊이만큼 가치가 있을 때만 들이고, critical path는 어떤 벤더에 묶여 있어도 회피 전략을 그려 두자. 청구서는 매월 한 번 들여다보고, 옵저버빌리티는 외부 APM과 함께 짠다.

기억해두자. 이 책은 Cloudflare로 옮기라고 권하는 책이 아니라, **자기 시스템에 Cloudflare가 들어올 자리를 정직하게 결정하도록 돕는 책**이다. 13장은 그 결정의 가장 무거운 무게추다.

다음 14장에서는 이 무게추를 손에 든 채로 마지막 한 걸음을 내딛는다. 5장에서 "무엇을 옮길 것인가"를 결정했고, 6장부터 12장까지 "어떻게 옮길 것인가"의 구체적 도구들을 살펴봤고, 13장에서 "옮긴 다음 어떻게 살 것인가"의 정직한 그림을 그렸다. 14장은 이 모든 것을 시퀀스로 묶는다. **Strangler Fig 패턴 8단계로, AWS 위에 쌓아 올린 시스템을 부수지 않고 Cloudflare를 어디에서부터 어떻게 끼워 넣을 것인가.** 책의 마지막 약속을 함께 살펴보자.

---


## 14장. 마이그레이션 전략 — Strangler Fig 8단계로 어떻게 옮기는가

월요일 오전, 팀 회의실에 모여 있다고 해보자. 누군가가 화이트보드 앞에 서서 안건을 한 줄 적어 둔다. *"Cloudflare 본격 도입을 검토합시다."* 13장까지 함께 따라온 우리는 어떤 표정이어야 할까. 환영해야 할까, 한 발 물러서야 할까. 5장에서 결정 워크시트를 한 장 채웠고, 6~12장에서 자리마다의 도구를 익혔고, 13장에서 outage와 lock-in의 정직한 위험까지 마주했다. 그런데도 회의실에서 막상 "그래서 뭘부터 옮기죠?"라는 질문이 떨어지면, 답이 손에 잘 잡히지 않는다.

이유는 단순하다. *무엇을* 옮길 것인가는 결정했지만, *어떤 순서로* 옮길 것인가가 비어 있기 때문이다. 한꺼번에 다 옮기겠다고 하면 첫째 주에 데이터·컴퓨트·DNS가 동시에 흔들려 사고가 난다. 가장 먼저 옮기고 싶은 부분(예: 비싼 S3 egress)을 덜컥 손대면 그 앞 단의 라우팅·인증·관측이 따라오지 못해 또 사고가 난다. 마이그레이션은 *순서가 모든 것*이다. 한 번에 너무 많은 것이 흔들리지 않게, 옛 시스템을 부수지 않은 채, 새 시스템이 옛 시스템을 한 겹씩 감싸 자라게 하는 패턴 — 그게 Strangler Fig다.

이 장에서 손에 쥐고 가야 할 것은 한 가지다. 5장의 결정 워크시트 위에 얹을 수 있는 8단계 시퀀스. 각 단계마다 "무엇을 옮기는가, 위험은 어느 정도인가, 깨졌을 때 어떻게 되돌리는가, 어떻게 검증하는가, 얼마나 걸리는가"를 한 표에 담는다. 그러고 나서 하이브리드가 왜 종착점이 될 가능성이 높은지, 흔한 함정 네 가지가 어떤 모습으로 찾아오는지, Java/Spring 백엔드라는 무거운 자산을 어떻게 다뤄야 하는지를 차례로 살펴보자. 책의 마지막 장이니, 결단을 권유하되 강요하지 않는 자세로 함께 가자.

자, Strangler Fig의 본질부터 한 번 짚고 시작하자.

### Strangler Fig — 옛 나무를 베지 않는다

이름이 조금 무섭다. 교살무화과. 동남아 열대우림의 이 나무는 다른 나무 위에 씨앗이 떨어지면, 가지에서부터 뿌리를 아래로 내려 본래의 나무를 한 겹씩 감싸며 자란다. 옛 나무가 안에서 천천히 사라지고, 바깥 형태는 새 나무가 차지한다. 마틴 파울러가 이 그림을 소프트웨어 마이그레이션에 가져왔다.

핵심은 단순하다. **옛 시스템을 베지 않는다.** 새 시스템이 옛 시스템을 한 겹씩 감싸며 자라게 한다. 어느 시점에서는 옛 시스템과 새 시스템이 동시에 살아 있다. 그 동시 운영 기간이 안전 장치다. 새 시스템이 깨지면 옛 시스템으로 트래픽을 되돌리면 된다. 데이터가 한쪽에서만 살아 있으면 그 한쪽이 진실이다. 옛 시스템이 점점 줄어들다 어느 날 마지막 호출이 사라지면, 그제서야 옛 시스템을 끈다.

이 패턴이 Cloudflare 도입에 잘 어울리는 이유가 두 가지 있다. 첫째, **Cloudflare는 AWS 앞단에 자연스럽게 끼어들 수 있다.** DNS·CDN·WAF·Tunnel·Workers는 모두 origin을 그대로 둔 채 그 앞에 한 겹을 더 두는 구조다. 옛 시스템(AWS) 위에 새 잎(Cloudflare)을 한 장씩 얹는 그림이 자연스럽다. 둘째, **하이브리드가 임시 상태가 아니다.** 많은 시스템에서 마이그레이션의 종착점이 "전부 옮긴 상태"가 아니라 "AWS와 Cloudflare가 각자의 자리를 가진 상태"다. Strangler Fig는 그 종착점에서 멈춰도 자연스럽게 안정적이다. *전부 옮기지 않는다*가 답인 경우가 많다는 정직한 메시지를 14장 안쪽에서 한 번 더 강조하겠다.

이제 8단계로 들어가자. 단계마다 *위험도 / 롤백 / 검증 / 예상 소요 기간*을 함께 묶어서 본다.

### 8단계 — 가장 안전한 순서

순서를 한 줄로 요약하면 이렇다. **가장 옅은 레이어부터, 가장 깊은 레이어 순으로**. DNS는 가장 옅고, 데이터는 가장 깊다. 위험이 낮은 단계가 앞에, 깊은 단계가 뒤에 온다.

#### 1단계 — DNS 이전 (Risk: Low)

가장 먼저 옮기는 것은 도메인의 권한 있는 네임서버다. Route 53(또는 가비아·Namecheap 등)에 있는 DNS 레코드를 Cloudflare DNS로 옮긴다. 옮긴다고 해서 트래픽 자체가 Cloudflare를 거치는 건 아니다. **proxy 옵션을 off**(회색 구름)로 둔 채 DNS 레코드만 그대로 복사하면, 사용자 → 우리 origin 경로는 한 자도 바뀌지 않는다. 단지 도메인의 이름이 어디서 풀리는지가 달라질 뿐이다.

| 항목 | 내용 |
|---|---|
| **무엇을** | 권한 네임서버를 Cloudflare로. proxy off로 그대로 origin 가리키기 |
| **위험도** | Low. 트래픽 경로 변화 없음 |
| **롤백** | 도메인 등록기관에서 네임서버를 다시 Route 53으로. 24~48시간 |
| **검증** | `dig @1.1.1.1 example.com`으로 NS·A 레코드 확인. 외부 헬스체크 도구로 글로벌 응답 확인 |
| **예상 기간** | 1~3일 (TTL 전파) |

여기서 한 가지 잊지 말자. DNS 이전은 *DNS만* 이전한다. proxy on(주황 구름)으로 켜는 일은 다음 단계의 일이다. 한꺼번에 둘을 다 켜면 캐시·헤더·쿠키 동작이 한 번에 바뀌어 무엇이 깨졌는지 분간이 안 된다. *한 번에 한 손가락씩.* 이게 8단계 전체를 관통하는 자세다.

13장에서 다뤘던 single vendor 의존 위험도 이 단계에서 한 번 떠올리자. 운영팀이 신중하다면 secondary DNS를 다른 벤더(Route 53나 NS1 같은)에 운영해 둘 수 있다. Cloudflare DNS API로 두 곳을 동시에 갱신하는 식이다. 첫 단계에서 secondary DNS까지 갖추면, 8단계 전체의 안전 마진이 한 단계 더 두꺼워진다.

#### 2단계 — CDN/WAF (Risk: Low)

DNS가 안정적으로 자리 잡았다면, 이제 proxy를 켤 차례다. 회색 구름을 주황으로 바꾼다. 사용자 → Cloudflare PoP → origin 경로가 만들어진다. 이 한 번의 클릭으로 DDoS 방어, 무료 SSL, 기본 WAF, Bot Management 일부가 따라온다.

| 항목 | 내용 |
|---|---|
| **무엇을** | proxy on. Cloudflare CDN을 origin 앞에 둠. 정적 자산 캐시·기본 WAF 룰 적용 |
| **위험도** | Low~Mid. 캐시·헤더 동작 변화. CloudFront와 동시 운영 시 충돌 가능 |
| **롤백** | proxy off로 되돌리기. 클릭 한 번. 5분 내 복구 |
| **검증** | `curl -I` 응답 헤더에 `cf-ray`·`cf-cache-status` 확인. cache hit 비율 추적 |
| **예상 기간** | 1~2주 (캐시 룰 검증 포함) |

여기서 두 가지 흔한 함정이 있다. 하나는 CloudFront와의 *이중 캐시*다. CloudFront를 그대로 두고 그 앞에 Cloudflare를 얹으면, 같은 응답을 두 곳에서 캐시한다. 무효화가 한쪽에서만 일어나면 stale이 끔찍한 모양으로 사용자에게 도달한다. 권장은 CloudFront를 *점진 제거*하는 그림이다. 새 도메인은 Cloudflare CDN으로 바로, 기존 도메인은 CloudFront 앞에 Cloudflare를 두되 캐시 TTL을 한쪽으로 몰아준다.

다른 하나는 **쿠키·인증 헤더**다. Cloudflare가 무심코 캐시한 응답에 Set-Cookie가 섞이면, 다른 사용자에게 옛 사용자의 세션이 흘러간다. 끔찍한 일이다. 인증 경로는 cache bypass를 명시적으로 켜자. Page Rules 또는 Cache Rules에서 `Cookie: session=*`이 있는 요청은 캐시 안 함, `Authorization` 헤더가 있는 요청도 캐시 안 함 — 이런 룰을 미리 박아 두자.

WAF는 처음에는 기본 룰만 켜는 편이 낫다. 너무 많은 룰을 한꺼번에 켜면 정상 트래픽이 막혀 false positive가 잔뜩 쌓인다. 일주일 정도 *log only* 모드로 돌려 보고, 정말 막아야 할 패턴이 무엇인지 확인한 뒤 *block* 모드로 바꾸는 흐름이 안전하다.

#### 3단계 — Tunnel로 사설망을 끌어오기 (Risk: Low)

세 번째 단계는 약간 의외로 들릴 수 있다. 컴퓨트도 데이터도 옮기기 전에 *사설망 노출 모델*을 먼저 다시 짠다. 왜 이게 앞에 오는가? 다음 4·5·6단계에서 컴퓨트를 옮기기 시작하면, edge에서 도는 새 코드가 우리 origin(EC2·RDS·내부 API)에 닿아야 한다. 그때 origin이 publicly accessible로 노출돼 있지 않은 채로 안전하게 닿을 수 있어야 한다. Cloudflare Tunnel이 그 자리를 채운다.

| 항목 | 내용 |
|---|---|
| **무엇을** | EC2·on-prem에 cloudflared 데몬을 띄워 outbound-only로 Cloudflare에 연결. ALB의 public 노출 줄이기 |
| **위험도** | Low. 기존 ALB 제거 전까지는 양쪽 동시 운영 가능 |
| **롤백** | cloudflared 종료, ALB로 트래픽 되돌리기. 분 단위 |
| **검증** | tunnel 상태 dashboard 확인. 내부 API 응답 정상성 확인 |
| **예상 기간** | 3~5일 |

cloudflared는 우리 사설망 안쪽에서 *바깥으로* 나가는 연결만 연다. inbound 포트를 열 필요가 없다. 기억해두자 — Cloudflare 쪽으로 outbound로 나간 한 가닥의 터널 안에서, 외부 사용자의 요청이 거꾸로 흘러 들어온다. SG inbound 22·80·443을 다 막아도 동작한다. 11장에서 본격적으로 다룬 패턴 그대로다.

이 단계가 끝나면 origin은 *공식적으로 public IP를 가질 필요가 없어진다*. 다만 갑자기 ALB를 다 내리지는 말자. ALB는 내부망용으로 남기거나, 또는 이중 운영하다가 다음 단계 끝에서 제거하는 편이 안전하다. 그리고 RDS도 마찬가지다 — publicly accessible로 두기 찜찜한 RDS는 Tunnel을 거쳐 Hyperdrive에서 닿게 할 수 있다(10장 끝에서 예고했던 패턴이다).

#### 4단계 — Edge 로직 이전 (Risk: Mid)

네 번째 단계부터는 컴퓨트의 영역이다. 가장 옅은 컴퓨트 — *edge 로직* — 부터 시작하자. CloudFront Functions, Lambda@Edge, viewer request·viewer response·origin request·origin response 어디에 있든 헤더 조작, 리다이렉트, A/B 테스트, 인증 토큰 검증 같은 짧은 코드. 이 자리는 Workers가 자기 집처럼 들어맞는다.

| 항목 | 내용 |
|---|---|
| **무엇을** | CloudFront Functions / Lambda@Edge에 있던 짧은 로직 → Workers로 |
| **위험도** | Mid. 런타임 차이(Node API 가용 범위), 헤더 정규화 미묘한 차이 |
| **롤백** | Workers Routes에서 해당 라우트 제거하면 즉시 CloudFront 경로 복원 |
| **검증** | shadow mirroring(`fetch()`로 두 경로 같이 호출 후 응답 비교) 권장. Workers Analytics + CloudWatch 양쪽 확인 |
| **예상 기간** | 2~3주 (개별 함수 단위) |

여기서 한 가지 권장 패턴이 있다. *shadow mode* 운영이다. Workers를 새로 띄우되, 첫 며칠은 production 트래픽의 응답을 사용자에게 *반환하지 않고* 비교만 한다. 같은 요청을 Lambda@Edge와 Workers에 동시에 보내고, 응답이 byte-for-byte 같은지 일치율을 본다. 일치율이 99.5% 이상에서 안정되면 그제서야 트래픽을 Workers로 옮긴다. 처음에는 1%, 다음 날 5%, 10%, 50%, 100%. 한 번에 100%로 옮기면 미묘한 차이가 사용자 경험에 그대로 닿는다.

코드 모양으로 보면 이렇다. Lambda@Edge 코드를 Workers로 옮기는 가장 단순한 패턴이다.

```ts
// 옛 Lambda@Edge (viewer-request)
export const handler = async (event) => {
  const request = event.Records[0].cf.request;
  if (!request.headers.cookie) {
    return { status: '302', headers: { location: [{ value: '/login' }] } };
  }
  return request;
};

// 새 Workers (route: example.com/admin/*)
export default {
  async fetch(request: Request) {
    const cookie = request.headers.get('cookie');
    if (!cookie) return Response.redirect('https://example.com/login', 302);
    return fetch(request); // origin으로 그대로 흘림
  },
};
```

`event.Records[0].cf.request`라는 AWS 고유 객체 모델이 표준 `Request`로 바뀐다. 이건 lock-in이 옅어지는 신호다 — Workers의 fetch handler는 Web Standards Request/Response를 그대로 쓰기 때문에, 다른 edge 런타임으로 옮길 때도 코드의 본체는 거의 그대로다.

#### 5단계 — API Gateway → Workers Routes (Risk: Mid)

다섯 번째 단계는 API 라우팅 레이어다. AWS에서 API Gateway가 자리하는 영역. 라우트 정의, 미들웨어(인증·rate limit·logging·CORS), 백엔드 호출 분배 — 이 모두를 Workers Routes + Hono 조합으로 다시 그린다.

| 항목 | 내용 |
|---|---|
| **무엇을** | API Gateway의 라우팅·미들웨어 → Workers Routes + Hono |
| **위험도** | Mid. 라우트 매칭 룰 미묘한 차이. CORS·인증 헤더 처리 |
| **롤백** | Workers Routes 제거 → API Gateway endpoint로 트래픽 복귀 |
| **검증** | 카나리 배포(1% → 100%). 4xx/5xx 비율, p95 비교 |
| **예상 기간** | 3~6주 (라우트 수에 비례) |

이 단계의 함정은 *전부 한 번에 옮기려는 욕심*이다. API Gateway에 라우트가 200개 있다고 200개를 한꺼번에 옮기지 말자. 일감이 가벼운 stateless 라우트(예: `/healthz`, `/version`, 정적 리다이렉트) 5~10개를 먼저 옮기고 일주일 운영해 본다. 4xx·5xx·p95가 정상이면 다음 묶음으로. 한 번에 한 도메인씩, 한 번에 한 묶음씩. 권장 흐름은 이렇다.

```
주차 1: /healthz, /version, /robots.txt 같은 무상태 응답
주차 2: GET 위주 read API 한 묶음
주차 3: 인증 필요한 GET 한 묶음
주차 4: POST·PUT·DELETE write API 한 묶음
주차 5+: 외부 webhook 수신 같은 보조 라우트
```

이 단계가 끝나면 API Gateway의 라우트 비중이 줄어든다. 어느 시점에 0이 되면 API Gateway 자체를 끄거나, 일부는 남겨 둔 채로 운영한다. 후자가 더 흔하다. *전부 옮기지 않는 게 답*이라는 메시지를 다시 떠올리자.

#### 6단계 — Stateless Lambda → Workers (Risk: Mid)

여섯 번째는 *stateless Lambda*의 자리다. 의존성이 가벼운 Node Lambda — Sharp 같은 native binding 없고, 무거운 SDK 없고, 30초 안에 끝나는 함수들. 이 그룹은 Workers로 옮길 수 있다. 옮길 수 *없는* Lambda(Java JVM, Python ML, Sharp 의존, 5분짜리 배치)는 그대로 둔다. 5장의 결정 워크시트가 여기서 정확히 답을 준다.

| 항목 | 내용 |
|---|---|
| **무엇을** | 의존성 가벼운 stateless Node Lambda → Workers. 무거운 Lambda는 유지 |
| **위험도** | Mid. Node API 호환성, 1~10MB 스크립트 한도, V8 isolate 제약 |
| **롤백** | API Gateway·이벤트 소스를 Lambda ARN으로 되돌림 |
| **검증** | Workers Analytics의 error rate, p95. CloudWatch와 동시 확인 |
| **예상 기간** | 4~8주 (함수 수에 비례) |

여기서 한 가지 정직한 한계를 짚자. **`@aws-sdk/client-*`를 그대로 import하면 스크립트 크기가 폭발할 수 있다.** AWS SDK v3는 트리쉐이킹이 잘 돼 있긴 하지만, 한 함수에서 DynamoDB·S3·SNS를 동시에 쓴다면 압축된 코드 크기가 1MB 또는 10MB 한도에 부딪힐 수 있다. 옮기는 함수의 SDK 사용 패턴을 미리 점검하자. R2를 쓰는 자리라면 `@aws-sdk/client-s3`를 그대로 쓰면 되고(R2는 S3 호환), DynamoDB 호출이 남아 있다면 `aws4fetch` 같은 가벼운 서명 라이브러리로 대체하는 편이 낫다.

옮기는 패턴 자체는 4단계와 비슷하다. shadow mode → 카나리 → 100%. 한 함수씩. 그리고 결정적으로 — **남기는 Lambda는 그대로 둔다.** 옮기지 못하거나 옮길 가치가 없는 Lambda는 그 자리에서 잘 돌아간다. AWS에 한 발, Cloudflare에 한 발. 이 분리가 자연스럽다.

#### 7단계 — Workflows·Queues로 비동기 (Risk: High)

일곱 번째 단계부터 위험도가 한 칸 올라간다. Step Functions·SQS·EventBridge에 의존하던 비동기 흐름을 Workflows·Queues·Cron Triggers로 옮기는 일이다. 왜 위험도가 높은가? 비동기 흐름은 *상태를 가진다*. 진행 중인 instance가 있고, 재시도 카운트가 있고, dead-letter queue가 있다. 옮기는 와중에 메시지가 새거나, 같은 메시지가 두 번 처리되거나, 끝나지 않은 워크플로 instance가 양쪽에 걸린 상태로 멎으면 데이터 정합성이 흔들린다.

| 항목 | 내용 |
|---|---|
| **무엇을** | Step Functions → Workflows, SQS → Queues, EventBridge·`@Scheduled` → Cron Triggers |
| **위험도** | High. in-flight 메시지·instance 처리, idempotency, exactly-once 가정 |
| **롤백** | producer를 SQS·Step Functions로 되돌림. 단, 양쪽 큐에 메시지가 분산된 상태라면 drain 필요 |
| **검증** | dual-write 기간 운영 + 처리 결과 비교. Workflow instance 진행률 추적 |
| **예상 기간** | 6~10주 |

권장 패턴은 *dual-write*다. producer가 한동안 SQS와 Cloudflare Queue 양쪽에 같은 메시지를 보낸다. consumer는 둘 중 한쪽에만 붙어 처리한다. SQS consumer를 쉬게 하고 Queue consumer로 넘기는 식. 이 사이에 idempotency key를 메시지마다 박아 둬야 한다. 같은 message_id로 두 번 처리돼도 안전한 모양이어야 한다. Step Functions → Workflows의 경우는 더 복잡하다. 새 instance만 Workflows로, 진행 중인 instance는 Step Functions에서 끝까지 — 이런 분기가 자연스럽다.

이 단계에서 정직하게 인정할 한 가지가 있다. **EventBridge에 정확히 등가인 도구가 Cloudflare에 없다.** Pub/Sub, SchemaRegistry, EventBus, EventRule의 풍부한 통합은 Cloudflare 생태계에 아직 없다. 그래서 EventBridge를 깊이 쓰는 시스템이라면, 7단계에서 EventBridge는 *옮기지 않는* 결정도 합리적이다. Workers에서 외부 이벤트 큐로 webhook을 보내고, 그쪽에서 EventBridge로 흘리는 식의 하이브리드가 현실적인 종착점이다.

#### 8단계 — 데이터 (Risk: High, 가장 마지막)

마지막 단계가 가장 무겁다. 데이터의 자리다. S3 → R2, DynamoDB → KV/D1/DO, RDS → D1 또는 Hyperdrive 그대로. 데이터를 옮기는 일은 거의 모든 마이그레이션에서 가장 위험한 자리다. 옮기는 동안 *진실의 출처*가 두 곳이 되고, 한쪽이 늦게 갱신되면 사용자 눈에 stale 데이터가 닿고, 잘못 옮기면 데이터 손실은 거의 복구할 수 없다.

| 항목 | 내용 |
|---|---|
| **무엇을** | S3 → R2 (egress 큰 버킷부터), DynamoDB → KV/D1/DO 사용 패턴별, RDS는 그대로 + Hyperdrive |
| **위험도** | High. 정합성, 이중 쓰기 동안의 진실의 출처, 옮기는 비용(S3 → R2 inbound는 AWS egress) |
| **롤백** | dual-write로 양쪽 살아 있다면 read endpoint만 되돌림. single source로 옮긴 뒤엔 단순 롤백 어려움 |
| **검증** | hash 비교(rclone, s3 sync --dryrun), 샘플링 row 비교, p99 latency·error rate 추적 |
| **예상 기간** | 8~16주 (데이터 양·정합성 검증 깊이에 비례) |

S3 → R2부터 살펴보자. **egress가 큰 버킷부터** 옮기는 게 합리적이다. 미디어 정적 자산이 매월 30TB 다운로드된다면, 그 한 버킷만 옮겨도 월 $2,700 → $200 수준의 절감이 따라온다. 옮기는 절차는 rclone으로 sync, 양쪽 read 운영, 어느 시점에 read를 R2로 단일화, 이후 write까지 R2 단일. 다만 *옮기는 그 한 번의 inbound는 AWS egress로 잡힌다*는 사실을 잊지 말자(1장에서 이미 짚은 함정이다). 큰 버킷이라면 그 한 번의 청구서가 깜짝 놀랄 만큼 클 수 있다.

DynamoDB → KV/D1/DO는 더 까다롭다. 4·5장에서 강조했듯, DynamoDB 한 줄 매핑은 거짓말이다. 사용 패턴별로 KV·D1·DO 셋 중 하나로 갈라진다. 세션·플래그는 KV, 관계형은 D1, 강한 일관성·per-entity는 DO. 한 DynamoDB 테이블이 여러 패턴을 동시에 담고 있다면 *분리부터* 한다. 분리 후에 각각을 이전한다. 한꺼번에 옮기려는 시도는 거의 반드시 끔찍한 모양으로 끝난다.

RDS는 한 가지 권장이 분명하다. **그대로 두자.** D1으로 풀이전하는 일은 대개 권장되지 않는다. 5년 치 데이터, 인덱스, 마이그레이션 이력, DBA 운영 절차가 그 자리에 묶여 있다. 그 묶음을 풀어 옮기는 비용은 거의 항상 옮겨서 얻는 이득을 초과한다. 권장은 10장에서 다룬 그림이다 — RDS는 그대로, Hyperdrive를 앞에 둔다. 컴퓨트만 글로벌로 흩뿌리고 데이터는 한 자리에. *DB는 AWS, 컴퓨트는 Cloudflare.* 이게 가장 현실적인 종착점이다.

---

여기까지가 8단계다. 한 표로 다시 모아 두자.

| # | 단계 | 위험 | 롤백 시간 | 예상 기간 |
|---|---|---|---|---|
| 1 | DNS 이전 | Low | 1~2일 | 1~3일 |
| 2 | CDN/WAF | Low~Mid | 5분 | 1~2주 |
| 3 | Tunnel | Low | 분 단위 | 3~5일 |
| 4 | Edge 로직 | Mid | 즉시 | 2~3주 |
| 5 | API Gateway → Workers Routes | Mid | 즉시 | 3~6주 |
| 6 | Stateless Lambda → Workers | Mid | 즉시~수 시간 | 4~8주 |
| 7 | Workflows·Queues로 비동기 | High | drain 필요 | 6~10주 |
| 8 | 데이터 | High | 어렵다 | 8~16주 |

총 누적 기간은 6~12개월 수준이다. 이걸 1~2개월에 마치겠다는 시간 추정이 손에 잡히면, 거의 반드시 한 자리에서 깨진다. 시간을 정직하게 잡는 편이 낫다. 그리고 잊지 말자 — 위 표의 단계마다의 시간은 *예상*이다. 우리 시스템의 복잡도, 팀의 가용성, 옛 시스템의 깊이에 따라 절반이 될 수도, 두 배가 될 수도 있다. 무너지는 자리에서 다시 짚자.

### 하이브리드가 종착점이다

8단계를 다 거치면 모든 게 Cloudflare에 있을까? 거의 그렇지 않다. 가장 현실적인 종착점은 *하이브리드*다. 다음 그림이 가장 흔하다.

```
[해외 사용자]
   ↓
[Cloudflare DNS · WAF · CDN]
   ↓
[Cloudflare PoP의 Workers]   ← 컴퓨트는 여기서 글로벌 분산
   ↓
[Hyperdrive]                  ← 글로벌 connection pool + query cache
   ↓
[AWS RDS Aurora (도쿄)]       ← DB는 여기 그대로
   │
   └─[ECS Fargate Spring Boot] ← 무거운 batch·JVM 도메인은 여기 그대로
```

이 그림에서 무엇이 안 움직였는지 보자. RDS가 안 움직였다. ECS Spring Boot가 안 움직였다. 마이그레이션·백업·DBA 절차가 안 움직였다. 움직인 것은 *사용자 facing 컴퓨트 한 겹과 그 앞단의 라우팅·캐시·보안*뿐이다.

이 형태가 임시인가? 아니다. 많은 시스템에서 이게 *최종*이다. 5년 뒤에도 이 그림으로 운영하는 회사가 흔하다. 왜? 첫째, JVM의 성숙도. Spring Boot + Hibernate + JPA + Spring Batch 위에 쌓인 코드는 그 자리에서 가장 잘 돈다. 둘째, 라이브러리 풍부함. Java 생태계의 PDF·결제·메시징·통계 라이브러리들은 V8 isolate 안으로 옮겨오기 어렵다. 셋째, 팀 역량. Spring 백엔드 팀이 TypeScript Workers를 *운영*까지 해낼 준비가 되어 있는지는 별개의 문제다. 코드 작성과 운영은 다른 영역이다.

그래서 이 책의 권장은 한 줄로 단순하다. **컴퓨트의 *어느 한 겹*만 Cloudflare로 옮기고, 데이터·무거운 배치·핵심 도메인은 AWS에 남기자.** 이 한 줄이 지난 13개 챕터의 응축이다. 8단계 모두를 거치되, 마지막 데이터 단계는 *부분 이전*에서 멈추는 결정이 거의 항상 합리적이다.

### 흔한 함정 — 단계가 아니라 옆에서 찾아온다

8단계를 잘 지키면 사고가 안 나는가? 그렇지 않다. 단계 안쪽이 아니라 *옆*에서 찾아오는 함정이 있다. 네 가지를 함께 살펴보자.

#### Observability 공백

이게 가장 자주 사고를 낸다. 8단계가 진행되는 동안 한 트래픽이 AWS와 Cloudflare 양쪽을 거친다. CloudWatch에는 절반의 그림이, Workers Analytics에는 다른 절반의 그림이 박힌다. 사용자가 신고를 해와도 어느 쪽이 깨졌는지 한눈에 보이지 않는다. 끔찍한 일이다.

권장 패턴은 *외부 통합 APM 한 곳*이다. Datadog, New Relic, Sentry, Baselime, Axiom 중 하나를 골라 양쪽에서 모두 그쪽으로 로그·메트릭·trace를 보낸다. CloudWatch 로그는 로그 export로, Workers 로그는 Logpush로. trace는 OpenTelemetry로 통일한다. 한 사용자 요청이 Cloudflare에서 시작해 AWS origin까지 가는 trace가 한 view에 보이는 그림을 만들자. 이게 없으면 디버깅 시간이 두 배가 된다.

#### 비용 모델 혼합

두 번째 함정. 한 시스템의 비용이 AWS 청구서와 Cloudflare 청구서로 *나뉘어 보인다*. 한쪽만 보면 "어, 비용이 줄었네"라고 안심하지만, 두 청구서를 합산하면 늘어난 경우가 의외로 많다. 옮기는 도중에는 둘 다 사는 *이중 운영* 비용이 누적되기 때문이다.

권장은 *월간 통합 비용 대시보드*다. 두 청구서를 한 표로 합쳐서 매월 추적한다. 이전 시작 전 baseline을 잡고, 단계마다 +/- 변화를 기록한다. 4단계 끝났을 때 -10%, 5단계 끝났을 때 -15% — 이런 식. 그래야 어느 단계가 비용 측면에서 효과적이었는지, 어느 단계가 예상보다 느리게 절감되는지 손에 잡힌다. 부록 C의 비용 시뮬레이션 워크시트가 이 자리에서 다시 쓰인다.

#### IaC 분리

세 번째 함정. AWS는 Terraform 또는 CloudFormation으로 관리하는데, Cloudflare는 Wrangler·Pulumi·Cloudflare Terraform Provider 중 어떤 걸로 관리할지가 갑자기 한 결정 사항이 된다. 둘이 갈라지면 *진실의 출처*가 두 곳이 되고, 환경 일관성이 깨지기 시작한다. staging과 production이 미묘하게 다른 상태가 되는 게 가장 흔한 그림이다.

권장은 두 갈래 중 하나다. 하나, AWS 쪽 Terraform 그대로 두고, Cloudflare는 Wrangler 단독으로. 책임 분리가 명확해진다. `wrangler.toml`이 진실의 출처. 또 하나는, Cloudflare Terraform Provider를 도입해서 한 Terraform 코드베이스에서 양쪽을 관리한다. 이쪽이 더 정합적이지만 운영 학습 비용이 든다. 팀 규모가 작다면 첫 번째가 낫고, 큰 팀에 IaC 전담자가 있다면 두 번째가 낫다. 어느 쪽이든 *둘을 동시에 부분적으로* 운영하지는 말자. 그게 가장 끔찍한 형태다.

#### 팀 역량

네 번째이자 가장 무거운 함정. **Spring 백엔드 팀이 TypeScript Workers를 운영할 준비가 되어 있는가.** 코드를 짜는 일은 한 달이면 따라잡는다. 운영은 다른 영역이다. 새벽 3시에 incident가 났을 때 `wrangler tail`로 로그를 보고, Workers Analytics에서 p95를 읽고, Hyperdrive 풀 상태를 의심하고, KV의 60초 전파 지연이 의심될 때 그걸 한눈에 알아보는 직관 — 이건 한 분기 운영해 봐야 손에 익는다.

권장 흐름은 *작은 영역부터 운영 경험을 쌓기*다. 8단계의 1·2·3단계는 운영 부담이 거의 없다. 4단계에서 한 라우트만 골라 한 달 운영해 본다. 그동안 팀이 Workers를 익힌다. 5단계로 넘어가는 시점에 운영 자신감이 생긴다. 6단계부터는 새벽 incident가 한두 번 일어난다 — 그게 정상이다. 그 incident가 학습이다. *팀이 못 따라오는데 단계만 진행하면* 거의 반드시 한 자리에서 깨진다. 단계의 속도는 팀의 운영 자신감에 묶여야 한다.

### Java/Spring 백엔드의 결정

이 자리는 길게 짚자. 이 책 독자의 상당수가 Spring 백엔드를 운영한다. "Spring 모놀리스를 통째로 옮길 것인가"라는 질문은 거의 모든 회의에서 한 번씩 등장한다. 답을 정직하게 풀어 두자.

**통째로 옮기는 결정은 거의 항상 권장되지 않는다.** 이유를 셋으로 정리하면 이렇다.

첫째, **JVM의 성숙도.** Spring Boot 3·4 + Hibernate JPA + Spring Batch + Spring Security가 쌓아 올린 안정성은 V8 isolate 위에서 재현되지 않는다. 트랜잭션 propagation, AOP 기반 관점, 풍부한 모듈 통합 — 이 묶음을 옮기려면 코드의 본체가 거의 새로 쓰여야 한다. 코드를 새로 쓰는 일은 마이그레이션이 아니라 *재작성*이다. 재작성의 시간·위험은 마이그레이션의 그것과 한 자릿수 다르다.

둘째, **라이브러리 풍부함.** PDF iText, 결제 SDK, 통계 분석, 한국어 자연어 처리, 회계 라이브러리 — Java 생태계가 20년 가까이 쌓아 온 자산이 그대로 우리 도메인 코드에 박혀 있다. 옮기려면 동등한 TypeScript 라이브러리를 찾거나 직접 짜야 한다. 동등하지 않으면 사용자 경험이 떨어진다.

셋째, **팀 역량.** 한국에서 Spring 백엔드 개발자가 수십만 명 단위라면, TypeScript Workers를 production 수준에서 운영하는 개발자는 한참 적다. 채용 시장의 규모가 다르다. 팀의 한 명이 떠나면 그 자리를 채울 후보의 풀 자체가 다르다.

이 셋이 합쳐지면 답은 거의 분명하다. **Spring Boot 모놀리스의 핵심 도메인은 그대로 둔다.** ECS Fargate에 잘 돌고 있는 그 자리에 그대로 있다. 옮기지 *않는 결정*도 정직한 결정이다.

그러면 어디서 Cloudflare가 자리를 잡는가? 세 곳이다.

하나는 **edge 경로의 일부**다. CloudFront Functions·Lambda@Edge에 박혀 있던 짧은 로직. 헤더 조작, 인증 토큰 검증, A/B 테스트, 리다이렉트 — 이건 Spring과 무관한 영역이다. 4단계에서 자연스럽게 옮긴다.

둘은 **public API의 일부**다. Spring API의 read-heavy 엔드포인트, 예를 들어 상품 카탈로그 조회, 이벤트 페이지 응답, 정적 콘텐츠 deliver. 이런 자리는 Workers + Hyperdrive로 옮기면 글로벌 응답이 즉시 빨라진다. write API와 트랜잭션이 깊은 영역은 Spring에 그대로. 이 분기가 자연스럽다.

셋은 **신규 영역**이다. 새로 만드는 RAG 챗봇, 새로 시작하는 SaaS 라인, 실험적 글로벌 서비스. 이 자리는 Spring 모놀리스에 욱여넣기보다 Workers + Hono + Drizzle 조합으로 처음부터 쓰는 게 자연스럽다. *옛 시스템을 옮기지 않고, 새 영역을 새 자리에 시작한다*는 자세. Strangler Fig의 또 다른 얼굴이다.

이 셋을 모두 합쳐도 Spring 모놀리스의 *코어*는 그대로다. 그게 정직한 그림이다. 한국에서 가장 흔한 종착점이다.

### 무너지는 자리 — 8단계가 약속하지 못하는 것

이 책의 마지막 "무너지는 자리" 박스다. 8단계가 어디서 약속을 못 지키는지 정직하게 짚자.

- **모든 시스템에 8단계가 맞지는 않는다.** 강한 region lock(KISA, HIPAA), 깊은 PrivateLink·VPC peering, 단일 region SaaS — 이런 환경에서는 8단계 중 절반이 적용되지 않는다. 1~3단계는 그래도 자리를 가지지만 4단계 이후가 막힌다. *옮기지 않는 결정*이 합리적이다. 5장의 결정 워크시트에서 -3점 이하로 나온 워크로드는 8단계에 들어가지 않는다.

- **단계 건너뛰기는 위험하다.** "DNS·CDN은 너무 시시하니 4단계부터 시작하자"는 유혹이 있다. 권장하지 않는다. 1·2·3단계는 *위험을 흡수하는 안전장치*를 미리 깔아 두는 자리다. DNS·CDN·Tunnel이 안정적으로 자리 잡지 않은 채 컴퓨트만 옮기면, 깨졌을 때 어디서 깨졌는지 분간이 어려워진다. 2단계 cache 동작과 4단계 edge 로직 동작이 동시에 흔들리면 디버깅 시간이 두 배가 아니라 네 배가 된다.

- **시간 추정은 부정확하다.** 위 표의 6~12개월 추정은 *평균*이다. 우리 시스템에 따라 절반이 될 수도, 두 배가 될 수도 있다. 특히 7·8단계(비동기·데이터)는 도메인 복잡도에 매우 민감하다. EventBridge 룰이 200개라거나, DynamoDB가 GSI 5개를 쓰는 패턴이라면 7·8단계만 1년이 걸릴 수도 있다. 시간을 정직하게 잡고, 매 단계마다 다음 단계의 추정을 갱신하자.

- **하이브리드 운영 자체의 비용을 무시하지 말자.** 두 청구서, 두 IaC, 두 observability stack, 두 운영 매뉴얼. 이게 단일 벤더 운영보다 *항상* 싸고 단순한 건 아니다. 옮겨서 줄어드는 비용보다, 양쪽 운영이 늘리는 운영 면적이 더 큰 경우가 있다. 13장의 정직한 한계가 이 자리에서 다시 살아난다.

- **8단계는 *기술* 시퀀스이지 *조직* 시퀀스가 아니다.** 팀 역량, 운영 야간조 구성, 채용 파이프라인, 외부 협력사와의 계약 — 이런 조직적 변수가 단계의 속도를 가장 자주 흔든다. 기술 추정에 조직 변수를 더해 *현실적인* 일정을 잡자. 6개월 추정이 9개월이 되는 게 정상이다. 그게 잘못된 게 아니다.

### 마무리 — 책을 덮은 우리에게

자, 14장의 마지막에 이르렀다. 그리고 이 책의 마지막 페이지에 가까워졌다.

이 책의 첫 장에서 우리는 한 가정을 흔들었다. *Cloudflare는 또 하나의 클라우드가 아니다.* 가정이 다른 edge-first 플랫폼이라는 한 줄을 나침반으로 삼고 13개 챕터를 통과했다. V8 isolate의 가정, Bindings·Compatibility Date의 좌표, KV·D1·DO·R2의 자리, Hyperdrive로 RDS를 살리는 그림, Zero Trust 보안의 다시 짜기, Workflows·Queues·AI Gateway의 빈자리 채우기, 2025년 outage가 가르쳐 준 정직한 한계. 그리고 14장의 8단계까지.

이 책이 약속한 것은 한 줄이었다. **AWS 위에 쌓아온 시스템을 부수지 않고도 Cloudflare를 가장 효과적인 자리에 끼워 넣을 수 있다.** 14장의 8단계가 그 약속을 가장 구체적인 시퀀스로 풀어낸 자리다. 부수지 않는다. 한 겹씩 감싼다. 멈추고 싶을 때 멈춘다. 하이브리드에서 머물러도 된다.

그래서 책의 마지막에 이르러 이 한 줄을 다시 두자. **Cloudflare를 도입하지 말자. Cloudflare에 자리를 내주자.** 도입이라는 단어에는 *우리 시스템 안에 새 제품을 들이는* 그림이 박혀 있다. 자리를 내준다는 단어에는 *우리 아키텍처에 어울리는 한 자리에 한 손님이 들어오는* 그림이 박혀 있다. 두 그림은 같지 않다. 첫 번째는 광고고, 두 번째는 책의 약속이다.

다음 주 월요일 아침, 이 책을 덮은 우리는 한 가지만 해보자. 회사 도메인 하나의 DNS를 Cloudflare로 옮기는 일. 그것이 8단계 중 첫 번째이고, 가장 안전하다. proxy off로 시작해 그저 네임서버만 옮긴다. 트래픽은 한 자도 바뀌지 않는다. 그 한 단계가 지나가면 두 번째 단계가 자연스럽게 손에 잡힌다. proxy를 켜는 일. 그러고 나면 세 번째가 손에 잡힌다. 한 번에 한 손가락씩.

8단계 모두를 다 거치는 데에 6~12개월이 걸린다. 더 걸려도 된다. 멈추고 싶은 자리에서 멈춰도 된다. 데이터를 옮기지 않는 결정도 정직한 결정이다. Spring 백엔드를 그대로 두는 결정도 정직한 결정이다. 옮기지 않는 결정이 옮기는 결정만큼 자주 옳다. 이 자세를 손에 쥐고 자기 시스템 위에 올라서면, 어느 자리에 Cloudflare가 들어와도 좋은지 자기 답을 손에 쥐게 된다.

기억해두자. **Cloudflare는 또 하나의 클라우드가 아니다.** 우리는 그 가정을 잡고 14장을 통과했다. 다음 월요일 아침, 그 한 줄을 머릿속에 두고 DNS 한 도메인을 옮겨 보자. 그게 시작이다.

---

---

## 후기

14장을 통과한 우리에게 한 가지가 손에 남는다. **Cloudflare가 무엇이고, 무엇이 아닌지**의 감각이다. 또 하나의 AWS가 아니라는 것을 머리가 아니라 손끝으로 알게 됐고, 가정이 다른 edge-first 플랫폼이라는 한 줄을 코드로 한 번씩 만져 봤다. 첫 Worker를 5분 만에 글로벌 PoP에 올렸고, 매핑 카탈로그의 거짓말 자리에 표식을 그었고, 결정 워크시트에 자기 시스템 컴포넌트를 채워 넣었다. Hono로 골격을 다시 그렸고, KV와 D1을 5축으로 골라 썼고, Durable Objects로 동시성을 한 줄로 세웠고, Hyperdrive로 RDS를 살려둔 채 컴퓨트만 흩뿌렸고, Access·Tunnel·Turnstile로 경계 대신 identity로 신뢰를 만들었다. 그리고 13장에서 *정직한 한계*를 마주하고, 14장에서 8단계 시퀀스로 모든 것을 한 줄로 세웠다.

다음 주 월요일 아침, 이 책을 덮은 우리에게 한 가지 약속이 남아 있다. **회사 도메인 하나의 DNS를 Cloudflare로 옮기는 일**이다. 8단계 중 첫 번째이고 가장 안전하다. proxy off로 시작해 그저 네임서버만 옮긴다. 트래픽은 한 자도 바뀌지 않는다. 그 한 단계가 지나가면 두 번째 단계가 자연스럽게 손에 잡힌다. 한 번에 한 손가락씩, 6~12개월에 걸쳐 8단계 모두를 거친다. 멈추고 싶은 자리에서 멈춰도 좋다. 옮기지 않는 결정도 옮기는 결정만큼 자주 옳다.

이 책의 시간 도장은 2026년 5월이다. 책장을 덮는 우리가 그 다음 달에 Workers 가격표가 바뀐 페이지를 만나도, 부록 D에 적은 Python Workers의 베타 라인업이 어느 분기에 GA로 풀려도, OpenNext가 Vinext로 자리를 비켜 줘도 — 멘탈 모델은 잘 변하지 않는다. 우리가 잡은 것은 가격표가 아니라 가정이고, 가정이 손에 잡히면 가격표가 바뀌어도 결정이 흔들리지 않는다. 다만 분기마다 한 번씩, 부록 F에 적어둔 추적 채널을 짧게 훑어 주자. 빠르게 움직이는 영역에서는 *모름*이 가장 큰 비용이다.

마지막으로, 정직한 인사 한 줄. *Cloudflare는 또 하나의 클라우드가 아니다.* 우리는 이 한 줄을 잡고 14장을 통과했다. 앞으로의 운영도, 그 한 줄을 머릿속에 두고 차분히 함께 가 보자. 청구서는 매월 한 번 들여다보고, 옵저버빌리티는 외부 APM과 함께 짠다. critical path는 어떤 벤더에 묶여 있어도 회피 전략을 그려 둔다. 자기 시스템에 어울리는 자리를 정직하게 결정하고, 그 결정의 무게를 함께 짊어진다. 그게 우리가 책에서 약속한 자세이고, 책 너머에서도 변하지 않는 자세다.

자, 다음 월요일에 만나자.

---

## 부록

### 부록 A. Wrangler CLI 치트시트

**자주 쓰는 명령 한 표**

| 카테고리 | 명령 | 무엇을 하나 |
|---|---|---|
| 프로젝트 | `npm create cloudflare@latest` | 새 Worker 프로젝트 생성 (TypeScript·Hono·Next.js 템플릿 선택) |
| 개발 | `wrangler dev` | 로컬 미니플레어로 띄우기 (기본 `http://localhost:8787`) |
| 개발 | `wrangler dev --remote` | Cloudflare 네트워크에서 진짜 PoP로 띄우기 |
| 개발 | `wrangler dev --env staging` | 환경별 binding으로 띄우기 |
| 배포 | `wrangler deploy` | 글로벌 PoP에 배포 |
| 배포 | `wrangler deploy --env production` | 환경별 배포 |
| 배포 | `wrangler versions upload` | gradual deploy용 새 버전 업로드 |
| 배포 | `wrangler versions deploy <id>` | 트래픽 일부를 새 버전으로 |
| 로그 | `wrangler tail` | production 로그를 실시간 스트림 |
| 로그 | `wrangler tail --format=pretty` | 사람이 읽기 좋게 |
| 시크릿 | `wrangler secret put <NAME>` | production 시크릿 등록 (값은 stdin) |
| 시크릿 | `wrangler secret list` | 등록된 시크릿 이름만 |
| 타입 | `wrangler types` | binding 기반 `Env` 타입 자동 생성 |
| D1 | `wrangler d1 create <db>` | D1 DB 생성 |
| D1 | `wrangler d1 execute <db> --file=<sql>` | SQL 파일 실행 |
| D1 | `wrangler d1 migrations apply <db>` | 마이그레이션 적용 |
| KV | `wrangler kv:namespace create <ns>` | KV namespace 생성 |
| KV | `wrangler kv:key put --binding=<bind> <k> <v>` | 키 등록 |
| R2 | `wrangler r2 bucket create <name>` | R2 버킷 생성 |
| R2 | `wrangler r2 object put <bucket>/<key> --file=<path>` | 객체 업로드 |
| Queues | `wrangler queues create <name>` | 큐 생성 |
| Workflows | `wrangler workflows trigger <name>` | 워크플로 인스턴스 시작 |

**자주 쓰는 흐름 5개**

1. **새 Worker 프로젝트 시작 → 글로벌 배포까지**
   ```bash
   npm create cloudflare@latest my-worker -- --type=hello-world --ts
   cd my-worker
   wrangler dev          # 로컬 확인
   wrangler deploy       # 글로벌 배포
   wrangler tail         # 로그 실시간 확인
   ```

2. **시크릿·환경변수 분리 운용**
   ```bash
   # 로컬: .dev.vars 파일에 KEY=value (gitignore)
   # production: wrangler secret put DATABASE_URL
   wrangler secret put STRIPE_KEY --env production
   ```

3. **D1 + Drizzle 마이그레이션 사이클**
   ```bash
   wrangler d1 create toby-shop-db
   # wrangler.toml에 binding 추가
   npx drizzle-kit generate          # SQL 파일 만들기
   wrangler d1 migrations apply toby-shop-db --local   # 로컬 적용
   wrangler d1 migrations apply toby-shop-db --remote  # 운영 적용
   ```

4. **gradual deploy로 위험 줄이며 배포**
   ```bash
   wrangler versions upload                  # 새 버전 업로드
   wrangler versions deploy <id> --percentage=10   # 10%만
   # 모니터링 → 이상 없으면
   wrangler versions deploy <id> --percentage=100
   ```

5. **`wrangler types`로 타입 안전 binding 잡기**
   ```bash
   wrangler types        # worker-configuration.d.ts 생성
   # tsconfig.json에 types: ["./worker-configuration.d.ts"]
   ```

**환경별 패턴**

- `--env staging` / `--env production` — `wrangler.toml`의 `[env.staging]`, `[env.production]` 블록 활용
- `--remote` — 로컬 미니플레어 대신 진짜 Cloudflare 네트워크에서 실행 (KV·D1을 production 데이터로)
- `--local` — 강제로 로컬 SQLite·KV 시뮬레이션

---

### 부록 B. 진단 카드 — 어떤 워크로드를 옮길까

5장 결정 트리의 한 페이지 압축 — 책상 옆에 붙여 두고 새 워크로드가 들어올 때마다 5분 안에 답을 내자.

**5축 자가 진단**

| # | 질문 | Yes (옮기기 좋음) | No (옮기지 마시오 / 보류) |
|---|---|---|---|
| 1 | **트래픽이 글로벌 분산인가?** | 미주·유럽·아시아 사용자가 고루 있다 | 한 리전에 90% 이상 몰린다 |
| 2 | **요청이 짧고 spike-y한가?** | p95 < 500ms, RPS 변동 큼 | 10초 이상 지속 처리, 스테디 |
| 3 | **상태가 강한 일관성을 요구하지 않는가?** | eventually consistent OK, 또는 single-key strong OK | 여러 row를 한 트랜잭션에 묶어야 함 |
| 4 | **Node.js 생태계 호환성이 큰 문제가 아닌가?** | TypeScript/JavaScript 또는 Web API로 풀 수 있다 | Java/Spring·Python·.NET 의존이 깊다 |
| 5 | **컴플라이언스(데이터 거주지)가 PoP 모델을 허용하는가?** | 글로벌 PoP OK, 또는 Jurisdiction Hint로 풀린다 | 법적으로 한 리전에서만 처리해야 한다 |

각 Yes에 +1점, No에 -1점, 애매하면 0점. **합산 +3 이상이면 Move now 후보, 0~+2면 Move later, -1 이하면 Don't move.**

**워크로드 패턴 9분류 빠른 매트릭스**

| 패턴 | 기본 답 | 비고 |
|---|---|---|
| 글로벌 사용자 + REST API + DB read 위주 | **Move now** | Hyperdrive로 RDS 연결 가능 |
| 정적 자산·이미지 배포 | **Move now** | R2 + Workers Static Assets |
| 인증 미들웨어 (token verify) | **Move now** | Auth.js·자체 JWT |
| 단순 webhook 수신 + 비동기 큐 | **Move now** | Workers + Queues |
| 채팅방·실시간 협업·재고 동시성 | **Move now (Durable Objects)** | actor 모델 한 자리 |
| 30초 이상 batch 처리 | **Don't move** (Workers CPU time 한도) | 그대로 Lambda·EC2 |
| 큰 파일 ETL (수 GB 단일 작업) | **Move later** | Workers Containers 베타 검토 |
| Bedrock·SageMaker 의존 LLM 워크플로 | **Move later (AI Gateway만)** | LLM 자체는 그대로 두고 Gateway만 끼움 |
| RDS 트랜잭션 깊은 비즈니스 로직 | **Don't move** | Hyperdrive로 컴퓨트만 옮김 |

**의사결정 워크시트 (빈 칸)**

| 컴포넌트 | 트래픽 | 짧고 spike | 일관성 | Node 호환 | 거주지 | 합계 | 결정 |
|---|---|---|---|---|---|---|---|
| (예: 사용자 검색 API) | 글로벌 | Y | weak OK | Y | OK | +5 | Move now |
| | | | | | | | |
| | | | | | | | |

> **주의:** 점수는 워크로드 *각각*에 대한 신호다. 묶음 마이그레이션 위험과 비즈니스 제약(예: "어드민은 한국 EC2 정책")은 점수 밖에서 별도로 판단하자. 13장에서 다룬 단일 벤더 의존 위험도 점수에 거의 반영되지 않는다.

---

### 부록 C. 비용 시뮬레이터 워크시트

**2026년 5월 기준 단가 (대표값 — 책장 펼친 시점에 [공식 가격 페이지](https://developers.cloudflare.com/workers/platform/pricing/) 재확인 필수)**

| 제품 | Free | Standard / Paid | 비고 |
|---|---|---|---|
| Workers 요청 | 100k/일 | $0.30 / 1M 요청 (10M 포함) | I/O 대기는 과금 안 됨 |
| Workers CPU time | 10ms/request | $0.02 / 1M ms (30M ms 포함) | 한도 30s |
| Workers AI | 10k neuron/일 | $0.011 / 1k neuron | 모델별 변동 |
| R2 storage | 10GB | $0.015 / GB·month | egress free |
| R2 Class A (write/list) | 1M/월 | $4.50 / 1M | put·list가 여기 |
| R2 Class B (read) | 10M/월 | $0.36 / 1M | get이 여기 |
| KV reads | 100k/일 | $0.50 / 1M | |
| KV writes/lists/deletes | 1k/일 | $5.00 / 1M | 비대칭 비싸다 |
| D1 reads | 5M/일 | $0.001 / 1k 행 | row 단위 |
| D1 writes | 100k/일 | $1.00 / 1M 행 | |
| D1 storage | 5GB | $0.75 / GB·month | |
| Durable Objects requests | 1M/월 | $0.15 / 1M | |
| Durable Objects duration | 400k GB·s | $12.50 / 1M GB·s | hibernation 권장 |
| Workflows | 100k step·요청 | $0.30 / 1M 요청 | sleep 무료 |
| Queues | 1M/월 | $0.40 / 1M | |
| AI Gateway | 무료 (cache 별도) | request 자체 무료 | LLM 비용은 원 provider |

**워크시트 — 내 워크로드 비용 추정 (월)**

```
[Workers]
요청 수:           ____ M/월   × $0.30 = ____ USD
CPU 시간 평균:     ____ ms/req × 요청 수 × $0.02/1M ms = ____ USD

[R2]
storage:           ____ GB     × $0.015 = ____ USD
Class A (write):   ____ M       × $4.50 = ____ USD     ← 자주 쓰면 큰 자리
Class B (read):    ____ M       × $0.36 = ____ USD
egress:            (0)                                  ← 무료

[KV]
reads:             ____ M       × $0.50 = ____ USD
writes:            ____ M       × $5.00 = ____ USD     ← write 많으면 D1·DO 검토

[D1]
reads (row):       ____ M행    × $0.001/1k = ____ USD
writes (row):      ____ M행    × $1.00/1M = ____ USD
storage:           ____ GB    × $0.75 = ____ USD

[Durable Objects]
requests:          ____ M     × $0.15 = ____ USD
GB·s (hib 적용):   ____ M·GB·s × $12.50 = ____ USD

[Workflows / Queues]
Workflow 요청:     ____ M     × $0.30 = ____ USD
Queue 메시지:      ____ M     × $0.40 = ____ USD

[AI]
Workers AI neuron: ____ k     × $0.011 = ____ USD
AI Gateway:        무료
LLM 외부 호출:     ____ (OpenAI/Anthropic 청구서)

──────────────────────────────────
월 합계 추정:      ____ USD
AWS 동일 워크로드: ____ USD
차액:              ____ USD
```

**비용 폭주 5대 시나리오 (조기 경고 신호)**

1. **R2 Class A 폭주** — 작은 파일을 put 한 번에 1개씩 100만 번 — 신호: Class A 청구서가 storage 청구서를 추월
2. **KV write 폭주** — write가 read의 10% 넘으면 위험 — 신호: KV write 청구서 > read 청구서
3. **DO duration 누락** — hibernation 안 켰을 때 — 신호: GB·s 청구서가 requests 청구서의 10배 이상
4. **Workflows step 폭주** — 한 인스턴스가 step 1만 개 만들 때 — 신호: 평균 step/instance > 50
5. **AI neuron 폭주** — 한 요청에 모델 여러 번 호출 — 신호: neuron/요청 비율 > 100

13장에서 본격적으로 다룬다.

---

### 부록 D. Python Workers 노트

**현재 상태 (2026년 5월)**

- **베타** 상태. production-ready라고 단언하기 어려움
- Pyodide 기반 — Python 코드를 WebAssembly로 컴파일해 V8 isolate 위에서 실행
- 패키지 호환성: `pure Python` 라이브러리는 대부분 OK, C extension(numpy·pandas·boto3 등)은 Pyodide 빌드된 일부만 가능
- 콜드스타트는 JavaScript 워커보다 약간 느림 (보통 50~200ms)

**언제 쓸 만한가**

| 자리 | 권장 |
|---|---|
| Python ML 모델 추론 (작은 모델, ONNX·sklearn pure-py) | 검토 가능 |
| LangChain·LlamaIndex 가벼운 wrapper | 검토 가능 |
| FastAPI 마이그레이션 (단순 REST) | 검토 가능 |
| Django·SQLAlchemy 깊은 의존 | 권장 안 함 |
| boto3 등 C extension 깊은 코드 | 권장 안 함 |
| pandas/numpy 기반 ETL | 권장 안 함 (Workers Containers 검토) |

**최소 예제**

```python
# main.py
from js import Response

async def on_fetch(request, env):
    name = request.url.searchParams.get("name") or "world"
    return Response.new(f"Hello, {name}!")
```

```toml
# wrangler.toml
name = "my-py-worker"
main = "main.py"
compatibility_date = "2026-04-01"
compatibility_flags = ["python_workers"]
```

```bash
wrangler deploy
```

**한계 정직하게**

- C extension 미지원이 큰 벽 — 대부분의 ML·데이터 라이브러리가 막힘
- 디버깅 도구·로그 메시지가 JavaScript 쪽보다 빈약
- production 사례가 적어 운영 노하우가 커뮤니티에 덜 쌓임
- **TypeScript 기본 + 필요 자리만 Python**이 2026년 시점의 권장 패턴

---

### 부록 E. AWS ↔ Cloudflare 빠른 참조

**한 페이지 룩업 표** — 4장의 압축. *주의: 1:1처럼 보여도 가정이 다르다.*

| 카테고리 | AWS | Cloudflare | 1:1 깨지는 자리 |
|---|---|---|---|
| **컴퓨트** | Lambda | Workers | 콜드스타트 모델·CPU time 한도 |
| | Lambda@Edge / CloudFront Functions | Workers | 1:1 매핑 깔끔 |
| | Fargate / ECS | Workers Containers (베타) | GPU·대용량 RAM 제약 |
| | EC2 | (없음) — Workers + Tunnel로 우회 | 직접 등가 없음 |
| | Step Functions | Workflows | sleep 무료, 통합은 빈약 |
| **스토리지** | S3 | R2 | egress free, S3 호환 API |
| | EBS | (없음) — DO storage 또는 외부 | |
| | EFS | (없음) | |
| **DB** | DynamoDB | KV / D1 / DO 셋으로 갈라짐 | 패턴 따라 다름 |
| | RDS / Aurora | (없음) — Hyperdrive로 살려둠 | 점진 마이그레이션 도구 |
| | DAX | Cache API | 글로벌 분산 |
| | Neptune / DocumentDB | (없음) | |
| | OpenSearch (벡터) | Vectorize | 메타데이터 필터 한계 |
| **네트워크·전달** | CloudFront | (Cloudflare CDN) | 무료 plan에서도 광범위 |
| | Route 53 | Cloudflare DNS | DNS 단일 PoP 모델 |
| | API Gateway | Workers + Hono | API Gateway별 라우팅 패턴 |
| | PrivateLink | Tunnel + Mesh (조합) | 정확한 1:1 없음 |
| **보안·인증** | IAM | Bindings + Access | role 모델이 다름 |
| | Cognito | Auth.js / Lucia / Clerk | Cognito 등가 없음 |
| | WAF | Cloudflare WAF | 비교적 직접 매핑 |
| | Shield | DDoS Protection | 무료 plan 포함 |
| | Secrets Manager | Workers Secrets / Secrets Store | rotation 직접 안 됨 |
| | Verified Access | Cloudflare Access | 비교적 직접 매핑 |
| **메시징·이벤트** | SQS | Queues | strict ordering 약속 안 함 |
| | SNS | (없음) — Workers fan-out | |
| | EventBridge Rules | Cron Triggers | 단순 cron만 |
| | EventBridge Scheduler | Cron Triggers | |
| **AI** | Bedrock | Workers AI / AI Gateway | 모델 라인업 좁음 |
| | SageMaker | (없음) | |
| | Kendra | (없음) | |
| **관측성** | CloudWatch Logs | Workers Logs / Logpush | 보존 7일 (확장 시 Logpush) |
| | CloudWatch Metrics | Workers Analytics | 차원 적음 |
| | X-Ray | (없음) — 외부 APM 표준 | Sentry·Baselime·Axiom |

**다섯 가지 거짓말 패턴**

1. *한 이름이 셋으로 갈라짐* — DynamoDB → KV·D1·DO
2. *같은 단어, 다른 모델* — S3 ↔ R2 (egress)
3. *옮기지 않고 살리는 길* — RDS → Hyperdrive
4. *단일 등가물 없음* — Cognito → Auth.js·Lucia·Clerk
5. *리전 vs 글로벌* — CloudFront ↔ Workers (PoP)

---

### 부록 F. 트러블슈팅 + 2025 outage 타임라인

**흔한 5가지 함정과 해결법**

1. **Hyperdrive 연결 실패 (`could not connect`)**
   - 원인: RDS가 publicly accessible이 아니거나, SG에서 Cloudflare egress IP 차단
   - 해결: ① RDS publicly accessible + SG에 [Cloudflare egress IP 화이트리스트](https://developers.cloudflare.com/hyperdrive/configuration/firewall-and-private-network-configuration/) 또는 ② Cloudflare Tunnel로 사설망 outbound-only 연결 (11장)
   - 추가 함정: prepared statement는 connection pooling과 충돌 — `prepare: false` 또는 unnamed prepared 사용

2. **Workers CPU time exceeded**
   - 원인: 한 요청에 30초 넘는 CPU 작업 (JSON 파싱·암호화·이미지 변환 등)
   - 해결: ① 작업을 Queues로 분리 ② 무거운 batch는 Workers Containers 검토 ③ 일부는 그대로 Lambda·EC2

3. **KV stale read (60초 캐시 전파)**
   - 원인: write 직후 다른 PoP에서 옛 값 읽음
   - 해결: ① write-after-read 패턴은 KV 부적합 → D1·DO ② 정말 KV가 답이라면 cache-busting 토큰 또는 짧은 TTL ③ 5장 결정 트리에서 일관성 축 재평가

4. **OpenNext 빌드 에러 — 자주 보이는 7가지**
   - `next.config.js`의 `output: 'standalone'` 누락
   - server actions의 streaming 미지원 (2026년 5월 기준 일부)
   - middleware의 Node.js API 사용 (`fs`·`path`)
   - 동적 라우트의 `revalidate` 값 충돌
   - `next/image` loader가 Cloudflare Images로 안 잡힘
   - Edge runtime 강제 라우트와 Node runtime 라우트 혼재
   - 패키지 의존이 `cloudflare:workers` 아닌 Node-only

5. **Durable Objects migrations 거부 (`migration class mismatch`)**
   - 원인: 클래스 이름·구조 변경 시 migration 정의 누락
   - 해결: `wrangler.toml`의 `[[migrations]]` 블록에 `new_classes` / `renamed_classes` / `deleted_classes` 명시 → `wrangler deploy` 재실행

**2025년 outage 타임라인**

**2025년 11월 18일 outage** ([공식 post-mortem](https://blog.cloudflare.com/18-november-2025-outage/))

- **시작:** 11월 18일 11:20 UTC
- **원인:** Bot Management 설정 파일이 ClickHouse 권한 변경의 부작용으로 2배 크기로 생성됨 → proxy 구성요소가 panic
- **영향:** Workers KV·Turnstile·Dashboard·Workers 일부 라우팅까지 연쇄. CDN·DNS는 살아 있었음
- **복구:** 약 6시간 후 부분 복구, 14시간 후 완전 복구
- **HN 토론:** [item id 45973709](https://news.ycombinator.com/item?id=45973709)
- **교훈:**
  - Cloudflare *내부 의존* 그래프(Bot Management → KV → 다른 제품)가 외부에 잘 안 보였음
  - 자동 롤백 트리거가 없어 사람이 손으로 mitigation
  - Workers 자체가 죽지 않더라도 *주변 SaaS*가 한 번에 흔들릴 수 있음 → critical path는 fallback 설계 필수

**2025년 12월 5일 outage**

- **시작:** 12월 5일 14:00 UTC 부근
- **영향:** 일부 PoP에서 Workers·KV·R2 latency 급증, 요청 실패율 상승
- **HN 토론:** [item id 46162656](https://news.ycombinator.com/item?id=46162656)
- **공식 post-mortem:** 책 집필 시점에 부분만 공개. 본문 인용 시 원문 재확인
- **교훈:**
  - 한 분기에 두 차례라는 빈도 자체가 신호
  - SLA 99.9% 약속과 별개로 *체감 가용성*은 critical path의 다른 의존(외부 APM·CDN·결제 PG)과 함께 측정해야 함

**outage가 가르쳐 준 한 줄**

> Cloudflare의 엔지니어링 신뢰도는 별개의 평가지만, 단일 벤더에 critical path를 거는 일은 본질적으로 위험을 동반한다. 13장의 회피 전략(이중 DNS·외부 APM·결제 PG의 multi-vendor·읽기 트래픽 fallback)을 6개월에 한 번씩 실제로 발화 훈련 해보자.

---

## 참고자료

이 책의 모든 인용·근거는 아래 자료에 출처를 둔다. 책 전반에서 한 자료가 여러 챕터에 인용되어도 여기서 한 번만 등장한다. 카테고리는 *Cloudflare 공식 → 블로그·엔지니어링 → 비교·분석 → 학술·심화 → 커뮤니티 → 한국어*. 책장을 덮은 다음에도 분기마다 한 번씩 훑어 주자.

### Cloudflare 공식 문서

- [Cloudflare Workers Overview](https://developers.cloudflare.com/workers/)
- [Workers Pricing](https://developers.cloudflare.com/workers/platform/pricing/)
- [Workers Limits](https://developers.cloudflare.com/workers/platform/limits/)
- [Workers Security Model](https://developers.cloudflare.com/workers/reference/security-model/)
- [Choosing a data or storage product](https://developers.cloudflare.com/workers/platform/storage-options/)
- [Durable Objects Overview](https://developers.cloudflare.com/durable-objects/)
- [Durable Objects: What are they](https://developers.cloudflare.com/durable-objects/concepts/what-are-durable-objects/)
- [Use WebSockets with Durable Objects](https://developers.cloudflare.com/durable-objects/best-practices/websockets/)
- [Workers KV](https://developers.cloudflare.com/kv/)
- [R2 vs S3 (Cloudflare 비교 페이지)](https://www.cloudflare.com/pg-cloudflare-r2-vs-aws-s3/)
- [Hyperdrive how it works](https://developers.cloudflare.com/hyperdrive/concepts/how-hyperdrive-works/)
- [Hyperdrive connection pooling](https://developers.cloudflare.com/hyperdrive/concepts/connection-pooling/)
- [Hyperdrive AWS RDS Aurora](https://developers.cloudflare.com/hyperdrive/examples/connect-to-postgres/postgres-database-providers/aws-rds-aurora/)
- [Cloudflare Queues](https://developers.cloudflare.com/queues/)
- [Cloudflare Workflows](https://developers.cloudflare.com/workflows/)
- [Workers Containers](https://workers.cloudflare.com/product/containers)
- [AI Gateway](https://developers.cloudflare.com/ai-gateway/)
- [AI Gateway Caching](https://developers.cloudflare.com/ai-gateway/features/caching/)
- [Workers AI Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)
- [Vectorize Overview](https://developers.cloudflare.com/vectorize/)
- [Cloudflare One Overview](https://developers.cloudflare.com/cloudflare-one/)
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/)
- [Cloudflare Tunnel on AWS deploy guide](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/deployment-guides/aws/)
- [Turnstile + WAF + Bot Management](https://developers.cloudflare.com/turnstile/tutorials/integrating-turnstile-waf-and-bot-management/)
- [Workers Secrets](https://developers.cloudflare.com/workers/configuration/secrets/)
- [Wrangler install](https://developers.cloudflare.com/workers/wrangler/install-and-update/)
- [Wrangler commands](https://developers.cloudflare.com/workers/wrangler/commands/)
- [Workers TypeScript](https://developers.cloudflare.com/workers/languages/typescript/)
- [Cloudflare Images Pricing](https://developers.cloudflare.com/images/pricing/)
- [Workers Logs](https://developers.cloudflare.com/workers/observability/logs/)
- [Workers Logpush](https://developers.cloudflare.com/workers/observability/logs/logpush/)
- [Cloudflare Workers Routes](https://developers.cloudflare.com/workers/configuration/routing/routes/)
- [Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)
- [Cache API](https://developers.cloudflare.com/workers/runtime-apis/cache/)
- [Migrate from Pages to Workers](https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/)

### Cloudflare 블로그·엔지니어링

- [Mitigating Spectre and Other Security Threats — Workers Security Model](https://blog.cloudflare.com/mitigating-spectre-and-other-security-threats-the-cloudflare-workers-security-model/)
- [Workers: the Fast Serverless Platform](https://blog.cloudflare.com/cloudflare-workers-the-fast-serverless-platform/)
- [New Workers pricing — never pay to wait on I/O](https://blog.cloudflare.com/workers-pricing-scale-to-zero/)
- [Workflows GA: production-ready durable execution](https://blog.cloudflare.com/workflows-ga-production-ready-durable-execution/)
- [Building Workflows: Durable Execution on Workers](https://blog.cloudflare.com/building-workflows-durable-execution-on-workers/)
- [Workers Durable Objects Beta](https://blog.cloudflare.com/introducing-workers-durable-objects/)
- [Pools across the sea: Hyperdrive](https://blog.cloudflare.com/how-hyperdrive-speeds-up-database-access/)
- [Building Vectorize](https://blog.cloudflare.com/building-vectorize-a-distributed-vector-database-on-cloudflare-developer-platform/)
- [OpenNext Cloudflare adapter announcement](https://blog.cloudflare.com/deploying-nextjs-apps-to-cloudflare-workers-with-the-opennext-adapter/)
- [Baselime moved from AWS to Cloudflare — 80% lower cost](https://blog.cloudflare.com/80-percent-lower-cloud-cost-how-baselime-moved-from-aws-to-cloudflare/)
- [Improving Workers Types](https://blog.cloudflare.com/improving-workers-types/)
- [Automatically generated types](https://blog.cloudflare.com/automatically-generated-types/)
- [Hono on Cloudflare — founder story](https://blog.cloudflare.com/the-story-of-web-framework-hono-from-the-creator-of-hono/)
- [2025-11-18 Outage post-mortem](https://blog.cloudflare.com/18-november-2025-outage/)
- [Python Workers redux](https://blog.cloudflare.com/python-workers-advancements/)
- [Benchmarking Edge Network Performance](https://blog.cloudflare.com/benchmarking-edge-network-performance/)
- [Secrets and Environment Variables to Workers](https://blog.cloudflare.com/workers-secrets-environment/)
- [Cloudflare Secrets Store](https://blog.cloudflare.com/secrets-store/)
- [Workers Logpush GA](https://blog.cloudflare.com/workers-logpush-ga/)
- [Introducing Cloudflare Queues](https://blog.cloudflare.com/introducing-cloudflare-queues/)

### 비교·분석 글

- [OpenNext Cloudflare](https://opennext.js.org/cloudflare)
- [3 Years of OpenNext](https://opennext.js.org/news/2026-03-25-3-years-of-opennext)
- [Workers vs Lambda 2026 (Morph)](https://www.morphllm.com/comparisons/cloudflare-workers-vs-lambda)
- [Workers vs Lambda Edge: Six Months of Production (Rebal AI)](https://blog.rebalai.com/en/2026/03/09/cloudflare-workers-vs-aws-lambda-which-edge-runtim/)
- [Cold Start Comparison (Ddosify)](https://medium.com/ddosify/cold-start-comparison-of-aws-lambda-and-cloudflare-workers-a3f9021ee60a)
- [Workers vs Lambda Edge Computing (ZeonEdge)](https://zeonedge.com/blog/cloudflare-workers-vs-aws-lambda-edge-computing-comparison)
- [Workers V8 Isolates 100x Faster (Kunal Ganglani)](https://www.kunalganglani.com/blog/cloudflare-workers-v8-isolates-ai-agents)
- [R2 vs S3 (digitalapplied)](https://www.digitalapplied.com/blog/cloudflare-r2-vs-aws-s3-comparison)
- [R2 vs Big 3 (yconsulting)](https://yconsulting.substack.com/p/cloudflare-r2-vs-the-big-3-a-deep)
- [DNS comparison (mechcloud)](https://dev.to/mechcloud_academy/cloudflare-dns-vs-aws-route-53-comprehensive-comparative-report-13mk)
- [DNS comparison (spendbase)](https://www.spendbase.co/blog/cloud/amazon-route-53-vs-cloudflare-dns-which-one-fits-your-stack/)
- [Containers vs ECS Fargate (inventivehq)](https://inventivehq.com/blog/cloudflare-containers-vs-aws-ecs-eks-vs-azure-aks-vs-google-gke-comparison)
- [Cloudflare Containers Pricing comparison (HAMY)](https://hamy.xyz/blog/2025-04_cloudflare-containers-comparison)
- [Cloudflare Containers everything to know (Sliplane)](https://sliplane.io/blog/cloudflare-released-containers-everything-you-need-to-know)
- [Durable Execution Showdown — Lambda·Durable Functions·Temporal·Workflows (Medium)](https://medium.com/@rajaravivarman/durable-execution-showdown-aws-lambda-durable-functions-vs-temporal-vs-cloudflare-workflows-6a7785b851b4)
- [LLM Prompt Caching: AI Gateway vs Portkey vs Bedrock (AntStack)](https://www.antstack.com/blog/comparison-of-llm-prompt-caching-cloudflare-ai-gateway-portkey-and-amazon-bedrock/)
- [pgvector vs OpenSearch (Instaclustr)](https://www.instaclustr.com/education/vector-database/pgvector-vs-opensearch-for-vector-databases-5-differences-and-how-to-choose/)
- [D1 vs Neon vs PlanetScale (Bejamas)](https://bejamas.com/compare/cloudflare-d1-vs-neon-vs-planetscale)
- [Edge Database Benchmarks](https://dev.to/algoorgoal/edge-database-benchmarks-2eac)
- [Hono on Workers production API gateway](https://dev.to/young_gao/building-a-production-api-gateway-on-cloudflare-workers-with-hono-2lhg)
- [CDN comparison (inventivehq)](https://inventivehq.com/blog/cloudflare-vs-aws-cloudfront-vs-azure-cdn-vs-google-cloud-cdn-comparison)
- [Workers KV in Practice (eastondev)](https://eastondev.com/blog/en/posts/dev/20260422-cloudflare-workers-kv-guide/)
- [Thinking in Networks not Databases (Jilles Soeters)](https://jilles.me/thinking-in-networks-cloudflare-storage/)
- [Workers vs Lambda new pricing (Vantage)](https://www.vantage.sh/blog/cloudflare-workers-vs-aws-lambda-cost)

### 학술·심화

- [arXiv 2502.15775 — Serverless Edge Computing: Taxonomy & Literature Review (2025)](https://arxiv.org/abs/2502.15775)
- [arXiv 2310.08437 — Cold Start Latency in Serverless: Systematic Review](https://arxiv.org/html/2310.08437v2)
- [arXiv 2105.04995 — Engineering and Benchmarking a Serverless Edge System](https://arxiv.org/abs/2105.04995v1)
- [arXiv 2104.14087 — LaSS: Latency Sensitive Serverless](https://arxiv.org/abs/2104.14087)
- [arXiv 2401.02271 — Seamless Serverless across Edge-Cloud Continuum](https://arxiv.org/abs/2401.02271)
- [arXiv 2111.06563 — Serverless Platforms on the Edge: Performance Analysis](https://ar5iv.labs.arxiv.org/html/2111.06563)
- [arXiv 2403.00515 — Are Unikernels Ready for Serverless on the Edge?](https://arxiv.org/html/2403.00515v1)
- [arXiv 2404.12621 — WebAssembly Runtimes: A Survey](https://arxiv.org/html/2404.12621v1)
- [GWU SRDS19 — Challenges and Opportunities for Efficient Serverless at the Edge](https://www2.seas.gwu.edu/~gparmer/publications/srds19awsm.pdf)
- [InfoQ — Fine-Grained Sandboxing with V8 Isolates (Cloudflare)](https://www.infoq.com/presentations/cloudflare-v8/)
- [InfoQ — Cloudflare Dynamic Workers Open Beta (2026)](https://www.infoq.com/news/2026/04/cloudflare-dynamic-workers-beta/)

### 커뮤니티 (HN·Reddit·블로그)

- [HN 35526356 — "Workers production-ready" 토론](https://news.ycombinator.com/item?id=35526356)
- [HN 46458963 — V8 보안 패치를 Chrome stable보다 먼저 푸는 정책](https://news.ycombinator.com/item?id=46458963)
- [HN 46162656 — 2025-12-05 Outage 토론](https://news.ycombinator.com/item?id=46162656)
- [HN 45973709 — 2025-11-18 post-mortem 토론](https://news.ycombinator.com/item?id=45973709)
- [HN 45584281 — Workers CPU Performance Benchmarks](https://news.ycombinator.com/item?id=45584281)
- [HN 29356036 — "벤더 락인" 시각](https://news.ycombinator.com/item?id=29356036)
- [HN 29226841 — Workers self-host 가능 여부](https://news.ycombinator.com/item?id=29226841)
- [Liftosaur — Workers → Lambda 회귀 사례](https://www.liftosaur.com/blog/posts/how-i-moved-liftosaur-from-cloudflare-workers-to-lambda/)
- [TechPreneur — Workers 마이그레이션 $50K 절감 (unverified)](https://techpreneurr.medium.com/from-aws-lambda-to-cloudflare-workers-our-50k-annual-savings-story-7dcd1851d44c)
- [Bryce Wray — From Pages to Workers (again) revisited](https://www.brycewray.com/posts/2025/11/pages-workers-again-revisited/)
- [Alex Zappa — Pages to Workers migration mess](https://alex.zappa.dev/blog/cloudflare-pages-to-workers-migration/)
- [Vibe Coding With Fred — Pages deprecated 2025 migration](https://vibecodingwithfred.com/blog/pages-to-workers-migration/)
- [Cogley.jp — Cloudflare Pages vs Workers 2026](https://cogley.jp/articles/cloudflare-pages-to-workers-migration)
- [Cloudflare Outage 11/18 Analysis (mgx.dev)](https://mgx.dev/blog/cloudflare1119)
- [Reliability lessons from 2025 Cloudflare outage (Gremlin)](https://www.gremlin.com/blog/reliability-lessons-from-the-2025-cloudflare-outage)
- [Saintmalik — Securing EC2 with Cloudflare Tunnel](https://blog.saintmalik.me/cloudflare-zero-trust-security-ec2/)

### 한국어

- [RIDI — Cloudflare 도입 후기 (Argo Smart Routing)](https://ridicorp.com/story/cloudflare-dos-and-donts/)
- [velog — aws...? cloudflare! 그는 신인가? (D1·Hono·Drizzle 후기)](https://velog.io/@doublezeroman/aws-cloudflare)
- [velog — Cloudflare Workers로 부동산 가격 체크하기](https://velog.io/@gh4777/CloudFlare-Workers%EB%A1%9C-%EB%B6%80%EB%8F%99%EC%82%B0-%EA%B0%80%EA%B2%A9-%EC%B2%B4%ED%81%AC%ED%95%98%EA%B8%B0)
- [velog — veltrends 개발 후기 (Pages → Vercel 이전, velopert)](https://velog.io/@velopert/veltrends-dev-review)
- [marinesnow34 — Workers vs Lambda 비교](https://marinesnow34.github.io/2024/04/25/worker1/)
- [bohyeon.dev — Cloudflare를 웹 애플리케이션 최고의 장소로](https://ktseo41.github.io/blog/log/making-cloudflare-for-web.html)
- [Morgenrøde — Cloudflare Workers 소개·서버리스 앱 개발](https://ryanking13.github.io/2020/07/26/introducing-cf-workers-1.html/)
- [bgpworks — Cloudflare Workers 서버리스](https://medium.com/bgpworks/cloudflare-workers-%EC%84%9C%EB%B2%84%EB%A6%AC%EC%8A%A4-4de0d9d6aeb2)
- [cro.sH — Workers Rust SDK 사용기](https://blog.cro.sh/posts/cloudflare-workers-rust/)

---

*— 끝 —*
