# 6장. 로드 밸런서·게이트웨이·서비스 메시 — L4부터 mesh까지, 어디까지가 우리에게 필요한가

어느 5명짜리 팀이 우리도 service mesh를 써보자며 Istio를 깔았다. 3개월 후, 그 팀은 mesh를 '튜닝'하느라 한 주의 절반을 보내고 있었다. 본업이 무엇이었는지 점점 흐려진다. 채용 공고에는 "Service Mesh 경험자 우대"가 박혀 있고, sidecar 컨테이너의 OOM kill을 추적하느라 슬랙에 매주 새 스레드가 열린다.

이 장면이 어떤 팀에는 미래의 본인 모습이고, 어떤 팀에는 이미 지나간 어제다. 그리고 어이없게도, 이 팀에게 처음 필요했던 건 mesh가 아니라 nginx 하나였을지도 모른다. **서비스 메시는 도입할까 말까의 이분법이 아니다. 어디까지 필요한가의 분해 문제다.** 이 장의 핵심 질문이 거기서 출발한다.

L4와 L7의 차이를 운영 관점에서 말할 수 있는가? 서비스 메시가 우리 팀에 정말 필요한지를 latency 숫자와 메모리 숫자로 답할 수 있는가? 두 질문에 답할 수 있어야 비로소 "트래픽 분배 부품을 안다"고 말할 수 있다.

## L4 vs L7 — 한 줄로는 부족하다

먼저 가장 흔한 오해부터 풀자. "L4는 빠르고 L7은 똑똑하다"는 한 줄짜리 설명은 절반만 맞다. 운영자가 알아야 하는 차이는 더 구체적이다.

**L4 로드 밸런서**는 TCP/UDP 수준에서 동작한다. SYN 패킷이 들어오면 backend를 골라 connection을 묶고, 그 다음부터는 byte를 거의 그대로 흘려보낸다. HTTP를 모르고, URL을 모르고, header를 모른다. 그래서 빠르다. AWS NLB, HAProxy의 tcp mode, Linux의 IPVS가 모두 L4다. 단일 노드에서 초당 수백만 connection을 처리할 수 있다.

**L7 로드 밸런서**는 HTTP를 파싱한다. URL을 보고 라우팅을 결정하고, header를 보고 cookie sticky session을 만들고, TLS를 termination한다. NGINX의 default mode, Envoy, AWS ALB가 L7이다. 똑똑한 만큼 CPU를 더 쓴다.

운영 관점에서 중요한 갈림길은 **TLS termination을 어디서 하는가**다. 상황을 가정해보자.

- **edge에서만 TLS termination**: 외부 트래픽은 ALB가 TLS를 풀고, 내부는 plain HTTP로 흐른다. 가장 흔하고, 가장 단순하고, 가장 성능 좋다. 하지만 내부망에 도청자가 있다고 가정하지 않는다.
- **internal mesh 전체 mTLS**: 내부 모든 service-to-service 호출에 인증서를 붙인다. 보안은 강력하지만 비용이 든다. 9장 보안에서 다시 만난다.

이 결정 하나가 7장 CDN의 anycast 설계와 9장의 망분리·service identity로 줄줄이 이어진다. 그러니 L4·L7의 차이를 "성능 vs 똑똑함"이 아니라 **"어디서 TLS를 풀고, 어디서 라우팅 결정을 내리는가"** 의 질문으로 다시 보자. 그게 운영 관점이다.

## HAProxy·NGINX·Envoy — 셋 중 무엇을 골라야 하는가

같은 L7 로드 밸런서 카테고리 안에서도 셋이 가장 자주 비교된다. 결론부터 말하면 셋은 동등한 대체재가 아니다. 각자 잘하는 자리가 다르다.

Loggly의 벤치마크(W5)와 Envoy 공식 비교가 정리해주는 표가 있다.

| 항목 | HAProxy | NGINX | Envoy |
|------|---------|-------|-------|
| **raw L7 throughput / core** | 1위 | 2위 | 250 concurrency 이상에서 우위 |
| **메모리 (idle)** | ~50MB | ~80MB | ~150MB |
| **설정 reload** | hot reload 가능 | reload 시 짧은 끊김 | 동적 xDS API로 무중단 |
| **observability** | 약함 | 중간 | gRPC·http2·trace propagation 풍부 |
| **service mesh data plane** | 안 맞음 | 어색함 | 사실상 표준 |
| **운영 부담** | 낮음 | 낮음 | 높음 (xDS 인프라 필요) |
| **권장 자리** | 입구의 raw L7 분배 | 정적 + dynamic 둘 다 무난 | mesh sidecar, cloud-native |

표를 한 줄로 줄이면 이렇다. **들어오는 트래픽의 입구에서 raw L7을 빠르게 분배해야 한다면 HAProxy, 정적·동적 mix가 있고 익숙한 도구를 원한다면 NGINX, 내부 service-to-service mesh를 깔겠다면 Envoy.** 셋을 동시에 써도 이상하지 않다. edge에 NGINX 두고, 내부 mesh에 Envoy 깔고, 별도 TCP 트래픽 routing에 HAProxy를 두는 식이다.

여기서 흔한 함정 하나. Envoy의 메모리 150MB는 한 instance 기준이지만, mesh를 쓰면 **모든 application pod 옆에 sidecar로 1개씩** 붙는다. pod이 1000개면 sidecar 메모리 합이 150GB다. 5명 팀이 처음 이 숫자를 보면 정신이 아득해진다. mesh의 진짜 비용이 latency 이전에 메모리에서 먼저 드러난다는 점을 기억해두자.

## API Gateway는 어디에 사는가

로드 밸런서와 service mesh 사이에 한 자리가 더 있다. **API Gateway**다. Kong, AWS API Gateway, Spring Cloud Gateway, Apigee 등이 여기 들어간다. 이 자리가 왜 필요한지부터 짚고 가자.

LB가 "어느 backend instance로 보낼까"를 결정한다면, API Gateway는 "어느 service로 보낼까 + 인증·rate limit·response transform"을 결정한다. 그러니까 LB의 위에 한 층 더 얹은 셈이다.

상황을 가정해보자. 마이크로서비스가 10개 있고, 외부 클라이언트가 모두에게 직접 호출하면 endpoint가 10군데로 흩어진다. 인증을 service마다 각자 하면 코드가 10번 중복되고, 일관성도 깨진다. API Gateway 한 자리에 인증·rate limit·CORS·request transform을 모아두면 각 service는 비즈니스만 하면 된다.

다만 API Gateway가 단일 실패점이 된다는 점이 항상 따라 다닌다. 거기가 죽으면 모든 외부 트래픽이 죽는다. 그래서 Gateway는 **stateless + horizontal scale + 다중 region**이 기본 가정이다. 한 region에 Gateway 한 대만 두는 구성은 production에 어울리지 않는다.

한국에서는 토스·우아한형제들·라인이 모두 Gateway 패턴을 쓴다. 토스의 Spring Cloud Gateway, 우아한형제들의 자체 Gateway, 라인의 API 라우터가 각각 자기 도메인 특수성을 흡수한다. 특히 결제 도메인에서는 외부 PG·통신사 본인인증 같은 vendor 호출을 Gateway 뒤에 wrapper layer로 감싸는 패턴이 일반화돼 있는데, 이 wrapper 패턴은 19장 결제에서 다시 만난다.

## 그러면 서비스 메시는 무엇을 더 주는가

API Gateway가 외부 → 내부 입구의 control plane이라면, **service mesh는 내부 service-to-service의 control plane이다.** 그게 한 줄 정의다.

mesh를 깔면 무엇이 자동으로 따라오는가? 보통 세 가지를 약속한다.

1. **mTLS 자동화**: 모든 service-to-service 호출이 자동으로 mutual TLS로 암호화·인증된다. 인증서 발급·갱신·rotation이 mesh의 일이 된다.
2. **observability**: trace propagation, latency histogram, error rate가 application 코드를 한 줄도 안 고치고 붙는다.
3. **traffic split**: 새 버전으로 5%만 보낸다든가, canary release를 자동화한다든가.

이게 다 매력적이다. 그래서 5명 팀도 "우리도 한 번"이라고 깔게 된다. 그런데 mesh의 진짜 비용을 한 번 정량으로 보자.

## Service mesh의 진짜 비용 — 정량으로 답하기

Buoyant가 정리한 비교(W44, Linkerd 모회사라 다소 편향이지만 정량 데이터는 신뢰)와 arXiv 2411.02267의 mTLS 성능 정량 측정을 합쳐 보면 다음과 같다.

| mesh | mTLS 적용 시 latency 증가 | 메모리 (sidecar 1개) | 운영 복잡도 |
|------|---------------------------|------------------------|---------------|
| **mesh 없음 (baseline)** | 0% | 0MB | 낮음 |
| **Linkerd** | +33% | ~30MB | 중간 |
| **Istio Ambient (sidecar-less)** | +8% | ~10MB (node 공유) | 중간~높음 |
| **Istio (전통 sidecar)** | +166% | ~150MB | 높음 |

이 숫자가 처음 눈에 들어오면 한참 응시하게 된다. Istio 전통 모드의 +166% latency는 농담이 아니다. p50 50ms 응답하던 service가 mesh 깔자마자 130ms로 치솟는다. 그리고 pod마다 150MB sidecar가 붙으니, 100개 pod 운영하던 cluster의 메모리 사용량이 15GB 늘어난다. 사용자가 느끼는 latency도, AWS 청구서도, 둘 다 만만치 않다.

물론 Istio Ambient가 +8%까지 끌어내리면서 sidecar-less라는 새 트렌드를 열었다. Linkerd는 처음부터 +33%로 더 가벼웠다. 그러니 "mesh는 비싸다"가 아니라 **"어떤 mesh를 어떻게 깔았느냐"의 문제**다. 그 결정을 안 하고 그냥 "Istio 깔고 mTLS 켰다"가 +166%의 의자에 앉는 가장 빠른 길이다.

기억해두자. mesh는 도입 자체가 결정이 아니라, **mTLS·observability·traffic split 중 무엇을 켤지가 도입 결정이다.** 셋 다 켜야만 mesh를 쓰는 것이 아니다.

## 5명 팀 ≠ K8s + Istio

이 정도까지 보고 나면 한 가지 결론이 자연스럽게 따라온다. **5명짜리 팀이 K8s + Istio를 깔면, 그 팀의 본업은 '인프라 운영'으로 슬그머니 변경된다.**

DHH(David Heinemeier Hansson)가 자주 하는 말이 있다.

> Most teams that adopted Kubernetes did not need Kubernetes. They needed Heroku.

거칠지만 정확한 지적이다. 5명 팀이 정말로 필요한 것이 무엇인지를 따져보면 다음과 같다.

- **HTTPS termination?** ALB나 Cloudflare가 한다.
- **load balancing?** ALB나 nginx 한 대가 한다.
- **rolling deploy?** ECS·Fargate·Render·Fly.io가 한다.
- **service-to-service 인증?** 내부 트래픽이 같은 VPC 안에 있다면 보통 충분하다.
- **traffic split·canary?** ALB의 weighted target group으로도 된다.

mesh가 정말로 도움이 되는 자리는 **service가 50개를 넘어가고**, **여러 팀이 독립적으로 배포하고**, **service-to-service identity가 audit 요구사항인** 환경부터다. 한국 환경으로 옮기면, **토스·쿠팡·우아한형제들** 같은 규모에서 mesh가 의미를 가진다. 그 아래에서는 보통 over-engineering이다.

이걸 framework로 정리해보면 다음 4개 질문이 mesh 도입의 정량적 의사결정 도구가 된다.

1. **service 수**: 50 미만 → mesh 없이 LB + Gateway로 충분.
2. **팀 수**: 5 미만 → 한 팀이 모든 service를 운영하므로 mesh 없이도 일관성 유지 가능.
3. **mTLS audit 요구**: 금융·의료 외에는 보통 strong 요구가 아니다. 한국 금융권은 9장에서 다시 본다.
4. **on-call 인력**: 24/7 SRE가 없으면 Istio sidecar OOM kill을 새벽 3시에 추적할 사람이 없다. Linkerd나 Ambient를 먼저 고려하자.

네 질문에 모두 "그렇다"가 나올 때만 mesh 도입을 검토하는 편이 낫다. 그 전에 mesh를 깐다면, mesh 자체가 우리 팀의 본업이 돼버리는 끔찍한 일이 일어난다.

## 한국 사례 — 토스·우아한형제들·라인의 선택

한국에서 mesh를 어떻게 다루고 있는지를 한 단락으로 정리하자. 정확한 발표 출처는 검증 필요하지만, 공개 발표·conference 발언 기준으로 다음과 같은 큰 흐름이 잡힌다.

**토스**는 코어뱅킹 MSA 도입과 함께 mesh를 일부 핵심 도메인에 적용한다. 19장 결제 클라이맥스에서 이 결정의 대가가 어떻게 나타나는지를 다시 본다. **우아한형제들**은 모듈러 모놀리스 진화와 함께 자체 Gateway + 일부 mesh 도입을 점진적으로 진행한 것으로 알려져 있다(검증 필요). **라인**은 자체 PaaS를 오랫동안 운영해 K8s + Istio의 전형적 조합과는 다른 길을 갔다. **카카오**는 일부 영역에 Mesos를, 일부에 K8s를 운영한다(검증 필요).

이 차이가 한 가지 사실을 보여준다. **mesh 도입 여부는 회사 규모만의 함수가 아니라, 기존 인프라 자산·on-call 문화·도메인 audit 요구사항의 함수다.** 토스가 mesh를 쓴다고 우리 팀도 써야 하는 건 아니다. 라인이 mesh 없이도 거대한 트래픽을 운영한다는 사실이 그걸 말해준다.

## Sidebar: mesh 도입 전 체크리스트 — 운영자의 새벽 시나리오

mesh를 도입하기 전에, 새벽 3시 시나리오를 한 번 머릿속에서 돌려보자. 다음 7가지에 막힘없이 답할 수 있는가?

1. **Envoy sidecar 하나가 OOM kill됐을 때, 어떤 pod의 어떤 컨테이너가 죽었는지 5분 안에 찾을 수 있는가?** istio-proxy의 메모리 limit 잡는 자리를 모르면 답이 안 나온다.
2. **xDS configuration이 컨트롤 플레인과 데이터 플레인 사이에 sync가 안 됐을 때, 그 사실을 어떻게 알아채는가?** Istio의 `istioctl proxy-status`나 Linkerd의 `linkerd check`가 운영자의 첫 손이다.
3. **mTLS 인증서가 만료됐을 때, 자동 rotation이 잘 동작했는가?** rotation 실패는 silent killer다. 갱신이 안 됐다는 사실은 인증서가 실제로 만료되는 그 분에 처음 알게 된다.
4. **mesh 자체의 control plane이 죽었을 때, data plane은 계속 트래픽을 흘리는가?** Istio Pilot, Linkerd identity가 죽었을 때 5분간 무엇이 어떻게 동작하는지를 미리 알아두자.
5. **mesh upgrade를 무중단으로 할 수 있는가?** mesh upgrade는 보통 1년에 한두 번이지만, 그게 가장 위험한 순간이다.
6. **service A → B 호출이 갑자기 5초 latency가 됐다. mesh가 끼어 있는데, 진짜 5초가 application인지 sidecar인지 어떻게 가르는가?** trace propagation 설정과 sidecar metric 두 자리를 모르면 못 가른다.
7. **mesh 없을 때보다 알람이 몇 배 늘었는가?** mesh 도입 후 알람이 줄어드는 팀은 거의 없다. 늘어난 알람을 받을 on-call 인력이 있는가?

이 7가지가 모두 "예"여야 mesh가 우리 도구가 된 것이다. 한두 가지가 "글쎄"라면, 그 자리가 새벽 3시에 우리를 깨우는 자리가 된다. 14장에서 on-call 휴머니즘을 더 깊게 다룬다.

## 이 장의 약속 회수

L4·L7·LB·API Gateway·service mesh를 한 줄로 다시 정리하면 이렇다.

- **L4**는 byte를 빠르게 흘리고, **L7**은 HTTP를 똑똑하게 라우팅한다.
- **API Gateway**는 외부 → 내부 입구에서 인증·rate limit을 모은다.
- **Service Mesh**는 내부 service-to-service에 mTLS·observability·traffic split을 자동화한다.

그리고 가장 중요한 결론. **mesh는 도입 여부의 문제가 아니라 분해의 문제다.** mTLS만 필요한가, observability만 필요한가, traffic split만 필요한가를 따로 따져보자. mesh 없이도 셋 다 가능한 자리가 많다. ALB의 weighted target group, OpenTelemetry collector, AWS PrivateLink로 셋이 따로따로 해결되는 경우가 흔하다.

mesh를 깔자고 결정한 팀에게도 같은 조언이 적용된다. **Istio 전통 sidecar의 +166% latency를 정량으로 알고 도입하는 편이 낫다.** Linkerd나 Istio Ambient로 시작해서 점진적으로 옮겨가는 길이 항상 열려 있다. 한 번에 모든 service에 sidecar를 다는 결정은 거의 항상 후회로 끝난다.

## 다음 장으로 가는 다리

여기까지가 외부 트래픽이 우리 시스템 안으로 들어오는 입구의 풍경이다. LB가 트래픽을 받아 backend로 흘리고, Gateway가 인증을 처리하고, mesh가 내부 호출을 묶는다. 그렇다면 그 트래픽은 어디에서 왔는가?

다음 장에서는 사용자에 더 가까운 자리, **CDN과 edge**를 살펴본다. Netflix가 왜 자기 트래픽의 95%를 AWS를 거치지 않고 보내고 있는지, edge compute가 cold start <5ms로 어떻게 가능한지, 객체 스토리지의 S3 함정은 무엇인지를 함께 본다. LB가 origin 앞에서 트래픽을 받는 부품이라면, CDN은 origin에 도달하지 않게 트래픽을 미리 흡수하는 부품이다. 둘은 보완재다.

가기 전에 한 번 정리하자. **5명 팀이 Istio를 깔면 안 된다는 결론이 너무 강하게 들렸다면, 그건 우리 팀의 안전을 위한 단호함이다.** 도구가 우리를 일하게 하는 자리가 아니라, 우리가 도구를 일하게 하는 자리에 우리 팀을 두자. 그게 mesh 도입 결정의 진짜 frame이다.

---

*챕터 작성 메모: 02_plan §3 6장 사양 충실 반영. L4/L7 / HAProxy·NGINX·Envoy 비교 / API Gateway 패턴 / Service Mesh (Istio·Linkerd·Ambient) / mTLS 정량 비용 (+166%/+33%/+8%) / 5명 팀 ≠ K8s+Istio 논쟁 G / mesh 도입 4질문 framework / 한국 사례 / 새벽 3시 7체크리스트 sidebar. W5·W44·논쟁 G(K8s) 인용. 한국 사례는 일부 정확한 출처 미확정 부분에 "(검증 필요)" 라벨 (0장 표기 규약 따름). 분량 약 18p 추정 (한국어 ~5000자).*
