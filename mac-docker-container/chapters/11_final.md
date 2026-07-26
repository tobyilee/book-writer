# 11장. 쿠버네티스는 언제 쓰는 기술인가

2020년 3월, Hacker News에 「'쿠버네티스를 씁시다.' 이제 당신에겐 여덟 개의 문제가 생겼다」는 제목의 글이 올라왔다. 719점에 댓글 469개(2026년 7월 25일 조회 기준). 그 아래에서 한 사람이 이렇게 받았다.

> "If Kubernetes had only cost us a year and two hundred thousand dollars then we'd have been luckier than we actually are. It definitely has a place, but it is *so* not a good idea for a small team. You don't need K8s until you start to build a half-assed K8s."
> — `zeveb`, HN 22491170 (2020-03-05)

쿠버네티스가 1년과 20만 달러만 앗아갔다면 오히려 운이 좋은 축이었을 거라는 말이다. 그리고 마지막 문장이 유명해졌다. 반쪽짜리 쿠버네티스를 직접 만들기 시작하기 전까진 쿠버네티스가 필요 없다.

그로부터 5년 뒤, 같은 사이트의 다른 스레드에는 이런 문장이 있다.

> "'Avoid k8s' shouldn't mean 'avoid containers' because they have major velocity and reliability benefits for small teams with no ops engineers."
> — `dangus`, HN 44985447 (2025년 8월)

'k8s를 피하라'가 '컨테이너를 피하라'를 뜻해서는 안 된다는 것이다. 운영 엔지니어가 없는 작은 팀에게도 컨테이너 자체는 속도와 안정성 면에서 큰 이득이 있으니까.

두 문장 사이에 5년이 있고, 우리 쪽에는 앞의 열 개 장이 있다. 이미지를 만들고 올리고 갱신하는 이야기는 끝냈으니 남은 질문은 하나다. 그 위에 쿠버네티스를 얹을 것인가?

미리 말해두자. 이 장은 그 답을 주지 않는다. 근거를 양쪽 다 깔되 한쪽으로 정리하지 않을 텐데, 게으름이 아니라 설계다. 대신 논쟁을 자기 판단으로 번역할 축을 챙겨 가자.

### 공식 문서가 직접 말하는, 쿠버네티스가 안 해주는 것

논쟁을 읽기 전에 확인할 것이 있다. 이 기술이 스스로 무엇이 아니라고 말하는가?

쿠버네티스 공식 문서에는 「What Kubernetes is not」이라는 절이 있다. 남이 쓴 비판이 아니라 프로젝트가 자기 소개 페이지에 직접 실어둔 목록이다(kubernetes.io, 2026년 7월 25일 조회).

> "Kubernetes is not a traditional, all-inclusive PaaS (Platform as a Service) system."
> "Does not deploy source code and does not build your application. Continuous Integration, Delivery, and Deployment (CI/CD) workflows are determined by organization cultures and preferences..."
> "Does not provide application-level services, such as middleware (for example, message buses), data-processing frameworks (for example, Spark), databases (for example, MySQL), caches, nor cluster storage systems (for example, Ceph) as built-in services."
> "Does not dictate logging, monitoring, or alerting solutions."
> "Does not provide nor mandate a configuration language/system (for example, Jsonnet)."

한 줄씩 뜯어보면 꽤 서늘하다. 소스 코드를 배포하지도 애플리케이션을 빌드하지도 않으며, CI/CD는 조직의 문화와 선호가 정할 일이라고 못 박는다. 메시지 버스나 데이터베이스, 캐시 같은 애플리케이션 수준 서비스도, 로깅·모니터링·알림 솔루션도, 설정 언어도 주지 않는다.

도입만 하면 배포가 정리되고 DB 운영이 편해지리라는 기대를 공식 문서가 먼저 부정하는 셈이다. 논쟁의 절반은 이 목록을 안 읽은 채로 벌어진다.

그렇다면 무엇은 해주는가? 같은 문서의 반대편 목록은 서비스 디스커버리와 로드 밸런싱, 스토리지 오케스트레이션, 자동화된 롤아웃과 롤백, 자동 빈 패킹, 자가 치유, 시크릿과 설정 관리, 배치 실행, 수평 확장, IPv4-IPv6 듀얼 스택, 확장성을 염두에 둔 설계다. 전부 여러 대에 나눠 돌리는 상태를 유지하는 일이고, 뒤집으면 한 대에서 도는 앱에는 해당 사항이 별로 없다.

오해 하나만 정리하고 가자. 2장에서 예고만 하고 넘어갔던 "쿠버네티스에서 도커가 빠졌다"는 이야기다. 쿠버네티스 공식 블로그(2022년 2월 17일 발행)에 따르면, Docker Engine이 CRI라는 표준 인터페이스를 구현하지 않아 쿠버네티스가 전환용 코드를 자기 안에 넣어두었다. 그게 dockershim이고, 애초에 임시 해법으로 의도된 것이라 이름도 shim이라고 문서는 적는다. 제거는 쿠버네티스 1.24에서 일어났다. 정작 우리가 궁금한 대목의 답은 한 문장이다 — "All your existing images will still work exactly the same." 빠진 것은 어댑터이지 이미지 포맷이 아니다.

### 2020년의 논쟁 — 그때 오간 말들

이제 논쟁을 보자. 다만 시점을 붙들어야 한다. 아래는 전부 2020년 3월 스레드의 발언이다.

필요 없었다는 쪽부터. 한 사람은 자기가 아는 스타트업들이 "k8s/golang/마이크로서비스 물을 들이켠" 탓에 출시가 6~12개월 밀리고 수십만 달러의 엔지니어링·데브옵스 시간을 낭비했다고 적으며 이런 비유를 붙였다.

> "k8s on day one at a startup is like a mom and pop grocery store buying SAP."
> — `sho`, HN 22491170 (2020-03) (본인이 겪은 일이 아니라 전해 들은 이야기라 검증할 수 없다)

스타트업이 첫날부터 k8s를 쓰는 건 동네 구멍가게가 SAP를 사는 격이라는 것이다. 다만 본인이 겪은 일이 아니라 아는 회사들 이야기라는 점은 기억해두자.

숫자를 댄 사람도 있다. 사용자 1000명에 초당 요청이 거의 0인 서비스를 GKE로 3개 대륙에 배포하느라 월 1만 유로를 썼다는 증언이다(`mirko22`, 2020-03, 익명의 개인 경험이다). 이유는 기술이 아니었다. Docker와 그것이 제공한다는 '확장성'이 투자자 슬라이드에서 좋아 보였기 때문이라고 그는 적었다.

더 흥미로운 건 인과를 뒤집는 논거다.

> "Choosing to build microservices is what adds complexity and makes tools like k8s necessary, not the business."
> — `onion2k`, HN 22491170 (2020-03)

복잡도를 만든 것은 사업이 아니라 마이크로서비스를 고르기로 한 결정이라는 것이다. 규모가 커져서 쿠버네티스가 필요해졌다고 말하기 전에 되짚어보게 만드는 문장이다.

반대쪽도 만만치 않았다. 한 사람은 "이런 '너희에겐 k8s가 필요 없다' 글들에 지친다"고 운을 뗀 뒤, 2년 가까이 프로덕션에서 쓰면서 "not a single service downtime, great fault-tolerance, and absolutely zero management effort"였다고 적었다(`WnZ39p0Dgydaz1`). 다운타임 한 번 없었고 관리 노력은 사실상 0이었다는 것이다. `honkycat`은 더 도발적이다. Docker Compose든 ECS든 더 낮은 층위로 가면 결국 더 구린 버전의 쿠버네티스를 다시 만들게 될 뿐이라고 했다. 목적이 아예 다르다는 증언도 있다. `avereveard`는 스케일이 아니라 환경 재현성 때문에 쓴다고 했다 — 아무 브랜치나 네트워킹과 라우팅까지 프로덕션과 똑같이 띄울 수 있다는 것이다.

한쪽은 회사를 죽인다 하고 다른 쪽은 관리 노력이 0이라 한다. 어느 쪽이 거짓말을 하고 있을까? 아마 아무도 아닐 것이다. 이 어긋남 자체가 뒤에서 세울 축의 존재를 알려준다.

### 2025~2026년, 전제가 바뀌었다

5년이 지났으니 최신 논쟁을 보자. 재미있는 건 질문의 형태가 달라졌다는 점이다.

2025년 8월 21일, 같은 커뮤니티에 "2025년에도 초기 스타트업에 K8s는 여전히 금기인가"라는 질문이 올라왔다(27점, 댓글 50개). 질문자는 이미 반박을 깔고 시작한다.

> "However, hosted K8s options have improved significantly in recent years (all cloud providers have Kubernetes options that are pretty much self-managed), and I feel like with LLMs, it's become extremely easy to read & write deployment configs."
> — `herval`, HN 44976292 (2025-08-21)

호스팅형 K8s 선택지가 크게 좋아졌고 LLM 덕에 배포 설정을 읽고 쓰기가 쉬워졌다는 것이다. 2020년 논쟁의 주요 논거 두 개 — 셋업이 어렵다, YAML 배우는 데 시간이 든다 — 를 질문자가 먼저 무력화하고 들어온 셈이다.

그렇다면 답은 "이제 괜찮다"로 정리됐을까? 이 장에서 가장 조심해서 읽어야 할 대목이 여기다. 같은 스레드, 같은 날에 두 증언이 정면으로 부딪힌다. 그리고 둘 다 자체 운영이 아니라 매니지드 EKS 이야기다.

> "I set up managed k8s using EKS several years ago for a client and... it just chugs along, self-healing, with essentially zero maintenance. ... At this stage I consider managed k8s my default go-to unless it's something so lightweight I just want to push it to Vercel and forget about it."
> — `tnjm`, HN 44976744 (2025-08-21)

> "After 7 years, and me wanting to move off EKS since I got the job 4 years ago, we are moving to ECS... The time sink required for the care and feeding just isn't worth it. I pretty much have to dedicate one engineer about 50% of the year to keeping the dang thing updated."
> — `therealfiona`, HN 44978566 (2025-08-21)

한쪽은 EKS로 셋업해줬더니 자가 치유되며 그냥 굴러가고 유지보수가 사실상 0이라 매니지드가 자기 기본 선택이라고 한다. 다른 쪽은 7년을 굴리고 ECS로 내려가는 중이며, 그 물건을 최신으로 유지하는 데만 엔지니어 한 명을 1년의 절반쯤 붙여놔야 한다고 한다.

같은 제품, 같은 날, 정반대의 청구서다. 읽는 쪽은 난감하다. 그러니 "매니지드를 쓰면 해결된다"는 정리는 하지 않겠다. 그건 합의가 아니다. 한쪽을 골라 결론으로 삼는 순간 근거의 절반을 버리게 된다.

2026년으로 오면 무게중심이 한 번 더 옮겨간다. 2026년 1월, 쿠버네티스가 과했다며 Docker Compose로 내려왔다는 글이 올라왔고(22점, 댓글 17개), 댓글 중 하나가 이 대목을 짚었다.

> "That's when I realized: we'd built a dependency on one person's specialized knowledge. And that knowledge had nothing to do with our actual product."
> — `elthor89`가 기사에서 인용, HN 46577325 (2026-01-11)

한 사람의 특수 지식에 대한 의존성을 만들어놨는데 그 지식은 우리 제품과 아무 상관이 없었다는 것이다. 인용한 사람은 관찰을 덧붙인다. 작은 조직에서 이런 걸 자주 보는데, 운영에 세 명이 필요해서가 아니라 한 명이 자리를 비우면 지식이 통째로 사라지기 때문에 문제라는 것이다.

축이 옮겨간 지점이 여기다. 2020년의 질문은 "이 기술이 복잡한가"였고, 2026년의 질문은 "우리 조직이 그 지식을 감당할 수 있는가"에 가깝다.

### 「쓴다」와 「운영한다」는 다른 결정이다

앞 소절의 두 증언이 왜 그렇게 어긋났는지, 2020년 스레드에 이미 실마리가 있다.

> "k8s is raw technology like linux kernel. You shouldn't use it directly which will be hard to maintain. There are bunch of packaged solutions around k8s like Google GKE or AWS EKS."
> — `adieu`, HN 22491170 (2020-03)

쿠버네티스는 리눅스 커널 같은 날것의 기술이라 직접 쓰면 유지가 어렵고, 그래서 GKE나 EKS 같은 포장된 해법들이 있다는 것이다. 같은 스레드의 `supermatt`도 비슷한 선을 긋는다. 자기 하드웨어에서 직접 관리하면 작은 팀에게 부담이 되지만 "all of these pain points go away with a managed kubernetes"라고 적었다. 2020년 당시의 판단이며, `therealfiona`가 2025년에 매니지드 EKS를 두고 정반대 이야기를 했다는 사실과 나란히 놓고 읽는 편이 낫다.

그래도 두 사람이 그은 선 자체는 남는다. **쿠버네티스를 쓴다와 쿠버네티스를 운영한다는 다른 결정이다.** 앞의 것은 매니페스트를 쓰고 앱을 올리고 롤아웃을 지켜보는 일이고, 뒤의 것은 클러스터 자체를 살아 있게 유지하는 일이다. 논쟁 대부분이 이 둘을 안 나눠서 평행선을 달린다. 한쪽이 "그냥 굴러간다"고 할 때 말하는 건 앞의 것이고, 다른 쪽이 "인력 0.5명"이라 할 때 말하는 건 뒤의 것이다.

뒤쪽에 무엇이 얹히는지는 공식 문서로 확인할 수 있다. 쿠버네티스 프로젝트는 최근 세 개의 마이너 릴리스에 대해서만 릴리스 브랜치를 유지한다. 1.19 이후 버전은 대략 1년의 패치 지원을 받고, 릴리스는 "approximately three times per year" — 대략 연 3회 일어난다(kubernetes.io, 2026년 7월 25일 조회 기준). 같은 시점에 유지되던 라인은 1.36·1.35·1.34였고, 1.34의 수명 종료일은 2026년 10월 27일로 적혀 있다.

숫자만 보면 담백하다. 다만 이 책을 쓴 맥에 깔린 `kubectl` 클라이언트는 v1.32.1이다. 유지되는 세 라인이 1.34부터였으니 이미 범위 밖이고, 특별히 방치한 것도 아닌데 그렇게 됐다. 연 3회 릴리스와 1년 남짓한 패치 창은 문서에 적힌 사실이고, 그 위에서 "그래서 업데이트는 끝나지 않는 업무가 된다"는 해석은 `therealfiona`의 증언이 대신 말해준다.

### 그 사이에 무엇이 있는가

2020년 스레드에는 이 책의 독자가 서 있는 자리를 정확히 짚은 질문이 하나 있다.

> "It seems to me that there's something of a gap between 'for single machine setups' (eg docker-compose) and 'for 500-engineer teams' (eg kubernetes)."
> — `skrebbel`, HN 22491170 (2020-03)

한 대짜리 셋업용 도구와 500명 엔지니어 팀용 도구 사이에 간극이 있는 것 같다는 말이다. 우리 대부분은 그 간극 안에 있다. 그 사이에는 무엇이 있을까?

가장 자주 나온 답은 소박하다. `mrweasel`은 머신 두 대와 로드밸런서를 권하며 이유를 붙였다 — "when stuff breaks, you'll prefer that it's not the Kubernetes stuff." 뭔가 깨질 때, 그게 쿠버네티스 쪽이 아니길 바라게 될 거라는 것이다. 직접 굴린다면 디버깅이 극도로 복잡하다는 이유도 함께 들었다.

Compose를 그대로 쓰는 길도 있다. `supermatt`는 움직이는 부품이 적고 단일 VM에서 굴리기 쉽지만 규모가 커졌을 때 원하게 될 동적 기능들은 없다고 정리했다. 다만 그가 덧붙인 한 문장이 우리에게 특히 중요하다 — "The same containers can run on both." 앞의 열 개 장에서 만든 이미지는 어느 쪽을 고르든 그대로 쓰인다는 뜻이고, 선택을 미룰 수 있다는 건 생각보다 큰 자유다.

옮겨가는 경로 이야기도 있었다. 원글이 compose에서 쿠버네티스로 가는 마이그레이션이 사소하다고 적자 `mosselman`이 반박했다. compose에서 swarm으로 가는 길은 사실상 명령 한두 줄인데, "I have looked into k8s and it wasn't as easy as this"라는 것이다.

내려오는 방향의 증언도 최근에 나왔다. 앞 소절에서 본 2026년 1월의 글인데, 여덟 명짜리 팀이 기능을 내놓는 대신 주당 60시간을 쿠버네티스 관리에 쓰고 있었다는 대목이 인용되며 화제가 됐다. 이 수치는 조심해서 다루자. 이 책은 원 기사를 열어보지 않았고, 확인한 것은 그런 주장을 담은 글이 Hacker News에 올라왔고 댓글이 그 대목을 옮겨 적었다는 사실까지다. 반박도 곧바로 붙었다. 성장통을 받아들이는 대신 "throw the baby out with the bath water", 목욕물과 함께 아기까지 버린 것이라는 지적이었다(`halfmatthalfcat`, 2026-01-11).

여기서도 판정은 나지 않았다. 내려온 사람과 성급하다 보는 사람이 같은 자리에 있다.

### 판단 축을 나누기

논쟁을 다 읽고 나면 인상이 하나 남는다. 사람들이 서로 다른 질문에 답하고 있다. 챙겨 갈 것은 결론이 아니라 축이다.

첫째, 쓰는 일인가 운영하는 일인가. 이 축이 없으면 "유지보수 0"과 "인력 0.5명"이 왜 같은 제품 이야기인지 영영 이해되지 않는다.

둘째, 규모가 아니라 역량이다. 2020년 스레드에서 가장 균형 잡힌 발언은 성공 사례 쪽에서 나왔다. `theptip`은 2년 차부터 k8s를 썼고 엔지니어 15명이 될 때까지 전담 운영 인력이 필요 없었다고 하면서, 곧바로 조건을 붙인다.

> "I was also very familiar with k8s ahead of time. I would not recommend someone in my shoes to learn k8s from scratch at the stage I rolled it out."
> — `theptip`, HN 22491170 (2020-03)

자기는 미리 잘 알고 있었고, 같은 처지에서 맨바닥부터 배우라고는 권하지 않겠다는 것이다. 기준이 팀 규모에서 팀 안에 아는 사람이 있는가로 옮겨간다.

셋째, 문제의 위치를 먼저 확인했는가. 확장성 문제를 겪는 고객 대부분은 쿠버네티스보다 데이터베이스를 먼저 들여다볼 필요가 있다는 지적이다(`mrweasel`).

넷째, 원인이 어디서 왔는가. 지금 겪는 복잡도가 사업에서 온 것인지, 마이크로서비스를 고르기로 한 결정에서 온 것인지(`onion2k`).

다섯째, 기술 밖의 이유들. 그 시스템에 들어맞는다는 것 자체가 동료들에게 읽히는 값을 준다는 논거(`bertil`), 고객이 "당신들의 쿠버네티스 스토리는 뭐냐"고 묻더라는 B2B 쪽 압력(`TallGuyShort`), 신기술을 안 쓰면 엔지니어가 떠난다는 채용 쪽 반론(`marcinzm`). 진짜 이유가 아니라고 치울 수는 없다. 다만 기술적 필요와 섞으면 판단이 흐려지니, 어느 쪽 계정에 다는지는 알고 있는 편이 낫다.

2025년 스레드는 판정 문장을 보탰다. `more_corn`은 복잡도 증가·가시성 저하·잡일 증가라는 값을 치를 만큼 이득을 보는지 물은 뒤 잘랐다 — "If you can't immediately rattle off those three things, you don't need it." 잘하는 세 가지를 즉석에서 못 읊으면 필요 없는 것이라는 뜻이다. `tdsanchez`는 쿠버네티스에서 돌리기 위해서만 시스템을 재설계해야 한다면 아직 충분히 모르는 것이라고 했다.

축만 받아 들고 "그래서 나는?"에서 멈추면 이 장은 남의 이야기로 끝난다. 위 기준들을 질문으로 바꿔 여섯 개만 남긴다. 새로 만든 기준은 없다 — 인용한 사람들의 문장을 당신 쪽으로 돌려놓은 것뿐이다.

1. 쿠버네티스가 잘하는 것 세 가지를 지금 즉석에서 읊을 수 있는가?
2. 나는 쿠버네티스를 쓰려는 것인가, 운영하려는 것인가?
3. 매니지드를 쓴다면, 그 지식을 아는 사람이 팀을 떠나면 어떻게 되는가?
4. 먼저 데이터베이스를 봤는가?
5. 쿠버네티스에서 돌리기 위해서만 시스템을 재설계해야 하는가?
6. 지금 겪는 문제가 마이크로서비스 선택에서 왔는가, 사업에서 왔는가?

여섯 개가 술술 나온다면 이미 판단이 서 있는 것이고, 막히는 자리가 있다면 거기가 지금 알아봐야 할 것의 목록이다. 하나도 안 나온다고 부끄러워할 일은 아니다. 6년째 이 논쟁을 하는 사람들도 서로 다른 답을 들고 있다.

---

이 장을 열었던 두 문장으로 돌아가자. 2020년의 그 사람은 반쪽짜리 쿠버네티스를 만들기 전까진 필요 없다고 했고, 2025년의 그 사람은 k8s를 피하라는 말이 컨테이너를 피하라는 뜻이 되어선 안 된다고 했다. 둘은 싸우는 것 같지만 다른 층을 말한다. 앞의 문장은 클러스터를 운영하는 일에 대한 것이고, 뒤의 문장은 우리가 열 개 장에 걸쳐 만들어온 그 이미지에 대한 것이다.

그러니 결론은 비워둔 채로 두겠다. 대신 하나만 챙기자. 도입 여부는 아직 안 정해도 되지만, 그 판단을 하려면 이 물건이 실제로 어떻게 생겼는지는 한 번 봐야 한다. 남의 청구서만 읽어서는 자기 계산이 서지 않는다. 다행히 그건 클러스터를 사거나 팀을 꾸리지 않고도 할 수 있는 일이다. 맥 한 대면 된다.
