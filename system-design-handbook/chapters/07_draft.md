# 7장. CDN·엣지·객체 스토리지 — 사용자 가까이로 가는 길

우리 서비스에 트래픽이 10배 늘면 AWS 청구서는 몇 배 늘까? 답은 "아키텍처에 따라 다르다"이다. 같은 트래픽 10배라도 모든 요청이 us-east-1을 거치면 청구서는 거의 10배가 된다. 그런데 Netflix는 트래픽이 수십 배 늘어도 AWS 청구서는 거의 안 늘었다. 어떻게?

답은 단순하다 — **Netflix는 트래픽의 95%를 AWS 안 거치고 보낸다.** ISP 깊은 곳에 자기 서버를 박아 두고, 사용자가 영상을 받을 때 그 서버에서 직접 받는다. AWS는 "어디서 받을지" 결정하는 control plane만 처리한다. 이게 가능하다는 사실 자체가 우리 설계를 다시 보게 만든다.

결국 우리가 풀려는 한 가지 질문은 이거다 — "이 요청이 정말 origin까지 가야 하는가, 아니면 가까이에서 끝낼 수 있는가." 그 질문에 답하기 위해 사용자에 가까이 가는 부품 세 가지가 한 묶음으로 손에 잡혀야 한다. **CDN**(edge cache로 정적 콘텐츠를 가까이 두기), **edge compute**(연산까지 가까이 두기), **객체 스토리지**(저장 자체를 분산하기). 한국 사례로 네이버·카카오엔터의 콘텐츠 CDN 운영도 짚어 본다.

## CDN의 기본 — PoP, anycast, edge cache, origin shield

CDN(Content Delivery Network)은 단순한 부품이다. 전 세계에 분산된 서버들에 콘텐츠 사본을 두고, 사용자에게 가장 가까운 서버에서 응답한다. 이 단순함이 만들어내는 효과가 흥미롭다.

CDN의 네 가지 핵심 개념을 한 번 짚자.

**1. PoP (Point of Presence).** CDN 사업자가 전 세계에 깔아 둔 서버 거점. Cloudflare는 2026년 기준 330+개 도시에 PoP가 있고, CloudFront는 600+개의 edge location, Akamai는 4,200+개의 edge server를 운영한다. PoP 수 자체가 latency를 결정하는 1차 변수다.

**2. Anycast.** 같은 IP 주소를 여러 PoP가 동시에 광고한다. BGP 라우팅이 사용자의 패킷을 가장 가까운 PoP로 보내 준다. 한국 사용자가 Cloudflare에 접속하면 자동으로 서울 PoP로 라우팅된다. 도쿄로 라우팅되는 경우도 있는데, 그건 ISP의 BGP 결정이다.

**3. Edge cache.** 각 PoP의 메모리·SSD에 콘텐츠 사본을 둔다. TTL 기반으로 유지하다가 만료되면 origin에서 다시 가져온다. cache hit이면 50ms 안에 응답, miss면 origin RTT가 추가된다.

**4. Origin shield.** PoP들이 모두 origin으로 직접 가면 origin이 cache stampede를 맞는다. 그래서 PoP들 위에 한 단의 "shield" 계층을 두어, miss를 모아서 origin에 가는 횟수를 줄인다. Cloudflare의 Argo Tiered Cache, CloudFront Origin Shield가 같은 모양이다.

이 네 개념을 머릿속에 그릴 수 있으면 CDN 운영의 70%는 이해한 셈이다. 나머지 30%는 도메인별 디테일이다.

> 💡 CDN 사용 시 자주 헷갈리는 한 가지 — **cache key**. 같은 URL이라도 query string, Authorization header, Cookie를 cache key에 포함하느냐에 따라 hit ratio가 완전히 다르다. 익명 사용자용 콘텐츠는 cookie를 cache key에서 빼야 hit이 잡힌다. 한 번도 안 빼면 hit ratio 0%로 운영되는 끔찍한 일이 벌어진다.

## Edge compute — V8 isolates의 마법

CDN이 정적 콘텐츠를 캐싱하는 부품에서 한 발 더 나아간 것이 **edge compute**다. 단순 캐싱이 아니라, 동적 응답을 만드는 코드까지 edge에서 돌린다.

대표 도구가 Cloudflare Workers, AWS Lambda@Edge, Vercel Edge Functions, Fastly Compute@Edge다. 이 중 가장 혁신적인 모양이 Cloudflare Workers의 **V8 isolates** 기반 모델이다.

| 구분 | AWS Lambda | Lambda@Edge | Cloudflare Workers |
|------|-----------|-------------|---------------------|
| 실행 환경 | container (Firecracker MicroVM) | container | V8 isolate (Chrome 엔진과 동일) |
| cold start | ~수백 ms | ~수백 ms | <5ms |
| 메모리 | 128MB~10GB | 128MB~10GB | ~128MB |
| 글로벌 분산 | region 단위 | edge location 한정 | 330+ PoP 자동 |
| 사용 가능 언어 | 다양 | 다양 | JS/TS, Rust(WASM), Python(WASM) |
| 가격 모델 | 호출 + 메모리×시간 | 호출 + duration | 호출 only (CPU time 별도) |

V8 isolates의 핵심 아이디어는 **"매 요청마다 새 process를 띄우는 대신, 한 V8 안에서 isolate(샌드박스)만 만든다"**는 것이다. process나 container를 띄우면 cold start가 백~수백 ms 걸리는데, isolate는 메모리 수십 KB만 잡고 시작이 1~5ms다. 같은 글로벌 노드에서 수천 개의 사용자 코드를 동시에 안전하게 돌릴 수 있다.

이 모양 덕분에 Cloudflare Workers는 "글로벌 분산 + 거의 0의 cold start"라는 두 약속을 동시에 한다. 한국 사용자가 Worker를 호출하면, 서울 PoP의 isolate가 1ms 안에 깨어나 응답한다. 같은 코드가 도쿄 PoP, 시드니 PoP에서도 동시에 돌고 있다.

대신 제약도 있다. **V8이 지원하는 언어만 돈다.** JavaScript/TypeScript가 1급(first-class)으로 지원되고, WebAssembly로 Rust·Go·Python을 우회할 수 있지만 native API 호출이 제한된다. 그래서 무거운 비즈니스 로직보다는 **lightweight orchestration**(인증, A/B 테스트 routing, header 변조, API gateway용 transformation)에 잘 맞는다.

## Netflix Open Connect — control과 data를 가르는 결정

Netflix의 사례는 CDN과 edge의 모든 결정이 압축된 케이스 스터디다. Netflix TechBlog가 2025년에 정리한 한 줄이 이렇게 정확하다.

> Around 95% of Netflix traffic is served from Open Connect without touching Netflix's AWS infrastructure at all.

이게 어떻게 가능한가? Netflix는 시스템을 **control plane**과 **data plane**으로 명확히 가른다.

**Control plane (AWS).** 사용자 인증, 추천, 검색, 결제, 카탈로그 메타데이터, A/B 테스트. 트래픽은 작지만 도메인 복잡도가 높은 모든 것. 이건 AWS 위에서 마이크로서비스 수천 개로 돌아간다.

**Data plane (Open Connect).** 영상 비트 자체를 사용자에게 흘려보내는 일. 트래픽은 전체의 95%이지만 도메인 복잡도는 단순(파일 byte 전송). 이건 **OCA (Open Connect Appliance)** 라는 자체 서버에서 처리한다.

OCA는 ISP의 데이터센터 안에 직접 배치된다. KT·SKT·LGU+의 IDC에 Netflix 서버가 들어가 있는 셈이다(한국에서도 같은 구조). 사용자가 영상을 요청하면, AWS는 "어느 OCA에서 받을지"만 결정하고, 실제 비트는 OCA에서 사용자 ISP 내부 망으로 직접 흐른다. 외부 인터넷을 거의 안 거친다.

이게 비용에 어떤 효과를 만드는가? **AWS의 egress 비용은 GB당 ~0.09달러.** Netflix가 매일 만 PB를 흘린다면 AWS만으로는 일일 9억 달러다(절대 가능한 숫자가 아니다). 그런데 OCA를 통하면 외부 egress가 거의 0이라, AWS 청구서는 control plane 비용으로만 한정된다.

기술적인 깊이도 흥미롭다. OCA는 **FreeBSD + sendfile() zero-copy + specialized NIC**로 디스크의 영상 파일을 NIC로 직접 흘린다. 사용자 메모리 공간을 거치지 않고 디스크→NIC로 zero-copy 전송하기 때문에 단일 서버에서 수십 Gbps를 뽑는다. SSL은 별도 NIC가 처리한다(NIC offload).

이 케이스가 한국 백엔드에 시사하는 한 가지가 있다. **트래픽의 도메인 복잡도가 크게 갈리면, control과 data를 가르는 결정을 고려할 만하다**는 점이다. 우리 시스템에서 트래픽이 큰 95%가 "단순한 byte 전송"이라면, 그 부분만 별도 인프라(또는 CDN·객체 스토리지)로 빼서 origin 부담을 줄일 수 있다.

## 객체 스토리지 — S3·GCS·Azure Blob과 한국 옵션

객체 스토리지는 "파일을 안전하게 저장하는 가장 단순한 모양"이다. 키-값 모델이다. key를 주면 byte를 받는다. 그게 전부다.

대표 도구가 AWS S3, Google Cloud Storage, Azure Blob Storage이다. 한국은 NCloud Object Storage, KT Cloud Storage가 있고, 망분리 환경(금융권)은 자체 IDC의 MinIO·Ceph로 비슷한 인터페이스를 흉내낸다.

객체 스토리지의 핵심 약속은 두 가지다.

**1. 11 9's durability.** S3 standard는 99.999999999% 내구성을 약속한다. 1만 개 파일을 1천만 년 동안 저장해도 1개 잃을까 말까. 어떻게 이게 가능한가? 한 파일을 같은 region 안의 여러 AZ에 분산 복제(보통 3+개 사본)하고, erasure coding으로 추가 redundancy를 더한다.

**2. 거의 무한한 throughput.** S3는 prefix 단위로 자동 sharding되어, 한 bucket이 초당 5,500 GET·3,500 PUT 이상의 throughput을 낸다. prefix 분산이 잘 되면 더 늘 수 있다.

이 두 약속 덕분에 객체 스토리지는 다양한 워크로드의 backbone이 된다.

- **정적 자산:** 이미지, 동영상, 문서.
- **백업·아카이브:** DB snapshot, 로그 archive.
- **데이터 레이크:** Parquet·ORC 파일 모아 두고 Athena·BigQuery로 분석.
- **Static website hosting:** S3 + CloudFront로 정적 사이트.

### Tiered storage — 자주 안 쓰는 건 싸게 두자

S3에는 가격이 다른 storage class가 6개나 있다.

| Class | 월 가격 (GB당, 대략) | 검색 latency | 용도 |
|-------|---------------------|--------------|------|
| Standard | $0.023 | ms | 자주 쓰는 콘텐츠 |
| Standard-IA (Infrequent Access) | $0.0125 | ms | 월 1회 이하 쓰는 콘텐츠 |
| One Zone-IA | $0.01 | ms | 단일 AZ, 재생성 가능 |
| Glacier Instant Retrieval | $0.004 | ms | 분기 1회 쓰는 자료 |
| Glacier Flexible Retrieval | $0.0036 | 분~시간 | 연 1회 쓰는 자료 |
| Glacier Deep Archive | $0.00099 | 12시간 | 법적 보관 |

이걸 잘 활용하면 storage 비용이 1/10~1/20로 줄어든다. 핵심 도구가 **lifecycle policy**다. "30일 안 쓴 파일은 Standard-IA로, 90일 안 쓴 건 Glacier로 자동 이동" 같은 규칙을 박을 수 있다.

우아한형제들의 인프라 비용 절감 발표(검증 필요)에서 S3 intelligent tiering이 한 축이었다. AWS가 자동으로 access 패턴을 분석해 적절한 tier로 이동시켜 준다. 사람이 lifecycle policy를 짜는 부담이 줄어든다.

### S3 운영 함정 3가지

S3가 단순해 보이지만 운영에서 끔찍한 일이 자주 일어난다. 한국 백엔드에서 자주 만나는 3가지를 정리하자.

**함정 1. list 비용이 의외로 크다.** 한 bucket에 백만 개 파일이 있는데, "어떤 파일이 있나"를 알기 위해 `ListObjects`를 호출하면 1,000개당 0.005달러가 든다. 백만 개 list는 5달러. 매 분마다 list 호출이 도는 cron이 있다면 한 달이면 두 자릿수 달러가 list만으로 나간다. 끔찍하다. 해결은 **list를 안 쓰는 access 패턴**으로 짜는 것이다. DB에 파일 메타데이터를 별도 저장하고, S3는 그냥 key로만 접근.

**함정 2. request rate per prefix.** S3는 prefix 단위로 자동 sharding되는데, prefix 분포가 한쪽으로 쏠리면 throttling(요청 제한)이 일어난다. 예전에는 prefix를 명시적으로 랜덤화(예: hash prefix)해야 했고, 2018년 이후 자동 sharding이 들어왔지만 여전히 burst에는 약하다. **timestamp 기반 prefix** (`yyyy/mm/dd/hh/`)는 같은 시점에 같은 prefix로 다 쓰니 hot prefix가 된다. random hash를 prefix 앞에 붙이는 패턴이 권장된다.

**함정 3. multipart upload incomplete.** 큰 파일을 multipart로 올리다 끊기면, 업로드된 파트가 S3에 남아 storage 비용이 든다. 사용자에겐 안 보이지만 청구서에는 잡힌다. lifecycle policy로 "7일 지난 incomplete multipart는 자동 삭제" 규칙을 박는 편이 낫다.

이 3가지를 default로 챙기는 S3 운영은 한국 백엔드 평균보다 훨씬 비용 효율적이다.

## DDoS 방어 — anycast + scrubbing

CDN과 edge가 사용자 가까이 가는 부품이라는 사실은, 거꾸로 **공격자에게도 가까이 가는** 부품이라는 뜻이다. DDoS 공격은 CDN 운영자가 가장 자주 막아 주는 종류의 사고다.

Cloudflare는 2024년에 단일 공격 기준 **3.8 Tbps**의 DDoS를 막아냈다고 발표했다. 어떻게 가능했을까?

**1. Anycast 자체가 DDoS를 분산한다.** 단일 IP가 330+ PoP에 분산되어 있으니, 공격 트래픽도 자동으로 흩어진다. 한 PoP에 1Tbps가 와도 330개로 분산되면 PoP당 3Gbps 정도. 견딜 수 있는 규모다.

**2. Scrubbing center.** 의심스러운 트래픽을 별도 데이터센터로 우회시켜, 정상 트래픽만 origin으로 보낸다. Cloudflare Magic Transit, AWS Shield Advanced, Akamai Prolexic이 같은 모양이다.

**3. WAF (Web Application Firewall).** L7 공격(SQL injection, cookie 탈취, brute force)을 패턴 매칭으로 차단. OWASP Top 10 룰셋 + 사용자 정의 룰.

여기서 한 가지 운영 관점의 통찰. **DDoS 방어를 사후에 깔기는 어렵다.** 이미 공격이 들어온 상태에서 CDN 앞단을 세우는 건 손이 많이 가고, DNS 전파가 일어나는 동안 origin이 무방비다. 그래서 **DDoS 방어는 production에 올라가기 전에 default로 깔아 두는 편이 낫다.** Cloudflare는 무료 plan에서도 기본 DDoS 보호가 들어 있어, "비용 부담 없이" 깔 수 있다.

## 한국 사례 — 네이버·카카오엔터·통신 3사

해외 사례만 보면 한국 CDN의 모양이 잘 안 보인다. 짚어 둘 사례 두 가지가 있다.

**네이버 CDN.** 네이버는 자체 CDN 인프라를 오랫동안 운영해 왔다. 검색, 블로그, 카페, 쇼핑, 동영상 — 모두 자체 CDN을 통해 사용자에게 전달된다. 글로벌 CDN을 같이 쓰지만, 한국 사용자에 대해서는 자체 인프라가 더 빠르고 비용 효율적이라는 결정이다. 토종 사용자의 트래픽을 자체적으로 처리한다는 방향성은 라인(자체 IDC)·카카오(자체 + 클라우드)와도 같은 맥락이다.

**카카오엔터 콘텐츠 CDN.** 멜론, 카카오웹툰, 카카오페이지의 콘텐츠 트래픽은 매우 크다. 이걸 글로벌 CDN으로 다 보내면 비용이 천문학적으로 늘어난다. 그래서 한국 안에서는 카카오 자체 IDC + 통신사 peering으로 처리하고, 해외 사용자에 한해 글로벌 CDN을 쓰는 hybrid 패턴이다.

한국 망의 특수성 한 가지 — **국내 통신 3사(KT·SKT·LGU+) peering이 CDN의 1차 결정변수다.** 한국 사용자의 95%가 이 3사 ISP를 통해 들어오니, 이 3사의 IDC 안에 직접 콘텐츠를 박아 두면 latency가 압도적으로 짧다. Netflix·YouTube·Facebook 같은 글로벌 사업자도 한국 진출 시 이 3사와의 peering을 1순위로 둔다. **한국 CDN은 global PoP 수의 함수가 아니라, 국내 3사 IDC와의 peering 깊이의 함수다.**

## "Edge에서 처리할 것"과 "Origin이 해야 할 것"을 가르는 4가지 기준

이 챕터의 핵심 통찰을 한 표로 정리하자. 새 endpoint를 설계할 때 자기에게 던질 4가지 질문이다.

| 기준 | edge에서 처리 적합 | origin이 해야 함 |
|------|------------------|----------------|
| 1. **요청별 응답이 같은가?** | yes (정적 콘텐츠, 카탈로그) | no (사용자별 응답) |
| 2. **stale data를 견딜 수 있는가?** | yes (이미지, 카테고리) | no (잔고, 재고) |
| 3. **응답 만드는 데 origin 데이터가 필요한가?** | no (header 변조, A/B routing) | yes (DB 쿼리 필요) |
| 4. **변경 빈도가 어느 정도인가?** | 낮음 (분~시간 단위) | 높음 (초 단위) |

네 질문에 모두 "edge"라면 무조건 edge로 보내자. 모두 "origin"이라면 origin에 두자. 섞여 있으면 edge에서 일부 처리하고 일부만 origin으로 위임하는 패턴(예: edge에서 인증 검증 → origin에서 비즈니스 로직)이 흔하다. **이 4가지 질문이 머릿속에 자동으로 펼쳐질 때, 우리는 "edge를 안다"고 말할 자격이 있는 백엔드 개발자가 되어 있다.**

## CDN·Edge·Storage 도입 자격을 묻는 5가지 질문

마지막으로 메타 질문. 새 서비스에 이 부품들을 도입하기 전에 자기에게 던질 다섯이다.

1. **사용자가 지리적으로 분산되어 있는가?** 단일 region 내부 사용자만이면 CDN의 효용이 작다.
2. **콘텐츠 중 정적인 비중이 얼마인가?** 모든 응답이 동적이면 CDN cache hit이 거의 없다.
3. **운영자가 cache invalidation을 견딜 수 있는가?** "왜 옛 버전이 보이지" 디버깅이 일상이 된다.
4. **edge compute가 우리 비즈니스 로직과 맞는가?** Java/Spring 프로젝트라면 V8 isolate가 안 맞는다. Cloudflare Workers는 lightweight orchestration에 한정.
5. **객체 스토리지의 lifecycle을 누가 설계할 것인가?** lifecycle 없이 그냥 Standard에 무한 저장하면 비용이 폭발한다.

이 다섯에 답이 명확하지 않다면 단계적으로 도입하는 편이 낫다. 단순 CDN(Cloudflare Free + S3)부터 시작해, 한계가 오면 edge compute를 추가하는 식. 처음부터 모든 부품을 다 깔면 효용보다 운영 부담이 먼저 폭증한다.

## Callback 예고

CDN·edge·객체 스토리지는 책 후반에 다시 만난다.

- **16장 채팅 시스템.** 채팅 이미지·동영상 전송이 어떻게 객체 스토리지 + CDN을 활용하는가.
- **17장 피드·타임라인.** Instagram·Twitter의 이미지 콘텐츠가 어떻게 CDN 위에 분산되는가.
- **20장 이커머스.** 쿠팡 BFCM(Black Friday) 트래픽이 어떻게 CDN으로 분산되는가.

이 챕터들에서 7장의 4가지 기준이 그대로 의사결정에 쓰인다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 사용자에 가까이 가는 세 부품이 손에 잡혀 있다. CDN(PoP·anycast·edge cache·origin shield), edge compute(V8 isolates의 마법), 객체 스토리지(11 9's durability와 tiered storage). Netflix Open Connect의 control/data plane 분리, Cloudflare Workers의 글로벌 분산, 한국 네이버·카카오엔터의 자체 CDN 사례까지가 한 묶음이다.

기억해두자. **AWS 청구서는 아키텍처의 함수다.** 같은 트래픽이라도 control과 data를 가르고, 정적 콘텐츠를 edge로 빼고, 객체 스토리지의 lifecycle을 설계하면 청구서가 1/10이 된다. Netflix가 95%를 AWS 안 거치고 보내는 모양은 우리에게도 적용 가능한 원칙을 가르쳐 준다.

다음 장에서는 분산 시스템의 가장 어두운 코너인 시간·순서·분산 ID를 살펴본다. "지금 몇 시야?"라는 질문에 분산 시스템이 어떻게 답하는지, 그리고 답을 못할 때 무엇으로 대신하는지. DST 전환 새벽에 cron이 두 번 또는 0번 실행되는 그 함정의 모양도 함께 짚어 보자.
