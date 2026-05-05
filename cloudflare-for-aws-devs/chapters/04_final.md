# 4장. AWS ↔ Cloudflare 매핑 카탈로그 — 1:1 표가 거짓말이 되는 지점들

팀 회의실에 모여 화이트보드 앞에 서 있다고 해보자. 누군가가 마커를 들고 표를 그리기 시작한다. 왼쪽에는 AWS, 오른쪽에는 Cloudflare. Lambda 옆에 Workers를 적고, S3 옆에 R2를 적고, DynamoDB 옆에 KV를 적는다. 그리고는 자신 있게 한 줄을 덧붙인다. "그러니까, DynamoDB는 Cloudflare에서 KV로 쓰면 되는 거죠?"

이 장면이 낯설지 않다면, 그건 우리 모두가 한 번쯤 같은 표를 그려봤기 때문이다. 그리고 그 표를 들고 한 달쯤 마이그레이션을 해본 사람이라면, 표 어딘가에서 자기 코드가 발이 걸려 넘어지는 광경을 본 적이 있을 것이다. 1:1 매핑은 정직한 도구처럼 보이지만, 실제로는 가장 위험한 종류의 지도다. 두 플랫폼의 표면이 비슷하게 생긴 자리에 동그라미를 그려 놓고, 그 안쪽 가정이 다르다는 사실을 표가 가려버리기 때문이다.

이 장에서는 매핑 표를 펼친다. 컴퓨트, 스토리지·DB, 네트워크·CDN·DNS, 보안, 메시징·이벤트, AI 여섯 카테고리다. 그런데 표만 그리고 끝내지 않는다. 각 행 끝에 "1:1로 보면 안 되는 이유"를 한두 줄씩 박아 둔다. 그 한두 줄이 사실 이 장의 본문이다. 표는 지도이고, 한두 줄짜리 주석은 그 지도의 위험 표시다. 위험 표시 없는 지도는 친절한 척하는 함정이다.

자, 한 카테고리씩 살펴보자.

## 카테고리 1. 컴퓨트 — 같은 "서버리스"라는 단어 아래의 다른 행성

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

## 카테고리 2. 스토리지·DB — DynamoDB 한 줄 매핑은 거짓말이다

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

## 카테고리 3. 네트워크·CDN·DNS — 본체와 부속의 자리가 뒤집힌다

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

## 카테고리 4. 보안 — IAM의 자리는 셋으로 흩어진다

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

## 카테고리 5. 메시징·이벤트 — SQS는 자연스럽고 EventBridge는 어색하다

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

## 카테고리 6. AI — Bedrock과 Workers AI는 같은 자리가 아니다

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

## 1:1 표가 거짓말이 되는 5가지 패턴

여섯 카테고리를 다 펼쳐 본 뒤, 한 발 물러나서 패턴을 보자. 매핑 표가 거짓말이 되는 자리는 다섯 가지 패턴으로 정리된다. 자기 시스템에 매핑을 적용할 때, 이 다섯 패턴을 점검표처럼 써보자.

**패턴 1. 한 이름이 셋으로 갈라진다.** 가장 위험한 패턴이다. DynamoDB가 KV·D1·DO 셋으로 갈라지는 자리. 한 줄 매핑은 셋 중 하나를 임의로 선택해서 표에 박아 넣는다. 자기 워크로드의 사용 패턴이 그 선택과 맞지 않으면 6개월 뒤 회귀 사례가 된다. *사용 패턴별로 갈라서 보자.*

**패턴 2. 같은 단어, 다른 모델.** Lambda↔Workers, Step Functions↔Workflows에서 일어난다. "둘 다 서버리스", "둘 다 orchestration" 같은 단어로 묶이지만 격리 모델·가격 모델·실행 모델이 정반대다. Lambda 컨테이너 모델로 Workers를 이해하려는 시도가 깨지는 자리이고, Step Functions ASL을 Workflows로 그대로 옮기려는 시도가 무거워지는 자리다. *단어가 아니라 모델을 보자.*

**패턴 3. 옮기지 않고 그대로 살리는 길이 있다.** RDS·Aurora↔Hyperdrive가 정확히 이 패턴이다. D1으로 옮기는 게 매핑 표의 답처럼 보이지만, 실제로는 RDS를 그대로 두고 Hyperdrive를 앞단에 두는 게 가장 risk-low한 길이다. *옮기는 것만 답이 아니다, 그대로 살리는 길도 답이다.* 14장 마이그레이션 시퀀스의 핵심 멘탈이기도 하다.

**패턴 4. AWS에 한 단일 등가물이 있고, Cloudflare에는 셋으로 흩어진다.** IAM이 그렇다. Bindings + Access + WAF rule 셋의 조합으로 다시 짜야 한다. CloudWatch도 비슷하다. AWS에서는 한 단일 제품인데, Cloudflare에서는 Workers Logs + Workers Analytics + Logpush + 외부 APM 조합이 표준이다. *한 제품을 찾지 말고, 조합을 보자.*

**패턴 5. AWS 리전 모델 vs Cloudflare 글로벌 모델.** 이건 가장 깊은 자리에서 일어나는 매핑 거짓말이다. ALB의 자리가 사라지고, "어느 리전에 살까"의 결정이 사라지고, "데이터 jurisdiction은 어디인가"가 새로 등장한다. AWS 리전 모델 위에 익숙해진 멘탈을 글로벌 모델로 바꾸는 일이라, 매핑 표 한 줄로는 표현되지 않는다. 1장과 2장에서 이 차이를 다뤘다.

이 다섯 패턴 중 하나라도 자기 매핑에 걸린다면, *멈춰서 한 번 더 보자.* 한 줄 매핑이 답을 가리키는 게 아니라, 답을 가리고 있는 신호다.

## "1:1 표가 거짓말이 되는 자리" — 매핑 카탈로그의 한계

이 장의 마지막은 정직한 한계로 닫자. 매핑 카탈로그를 펼친 뒤에도 표가 답하지 못하는 자리가 셋 있다.

첫째, **빠르게 변하는 영역**이다. Cloudflare는 분기마다 제품이 추가·변경된다. 2025년 4월에 Pages가 maintenance 모드로 들어가고 Workers Static Assets가 본체가 되었다. 2025년 11월에 Workflows가 GA되었다. 2026년 4월에 Dynamic Workers가 open beta에 들어갔다. Vectorize의 hybrid search 지원, Workers Containers의 GPU·대용량 RAM, Vinext의 안정화 — 이런 영역은 책 출간 후 6개월 안에 바뀔 가능성이 높다. *분기마다 공식 페이지를 다시 보자.* 부록 E에 추적 가이드를 두었다.

둘째, **enterprise 기능 부재**다. AWS의 enterprise 기능 — Glacier·Object Lock·VPC PrivateLink·정교한 IAM policy 언어·복잡한 Route 53 라우팅·Step Functions의 200+ 통합 — 의 일부는 Cloudflare에 같은 형태로 없다. enterprise 컴플라이언스가 강하게 요구되는 워크로드라면, 매핑 표가 답을 가리고 있을 수 있다.

셋째, **일부 SDK 호환성 한계**다. R2는 S3 호환 API라고 하지만 100% 호환은 아니다. Lifecycle policy·Object Lock 같은 기능이 일부 부재하다. AWS SDK의 모든 메서드가 그대로 동작하는 건 아니다. 옮기기 전에 *자기 코드가 실제로 사용하는 메서드 목록*을 확인하는 게 정직한 절차다. 책 한 권으로 모든 SDK 호환성을 확인할 수 없다. 자기 시스템의 코드 베이스 위에서 한 번 점검하자.

매핑 카탈로그는 *지도*이지 *결정*이 아니다. 지도를 본 뒤 어디로 갈지를 정하는 일은 자기 시스템 위에서 자기 손으로 해야 한다. 그 결정 도구가 다음 장에 있다.

## 마무리

자, 매핑 카탈로그를 한 번 펼쳐 봤다. 컴퓨트·스토리지·네트워크·보안·메시징·AI 여섯 카테고리에서 1:1 매핑이 거짓말이 되는 다섯 가지 패턴을 보았다. 한 이름이 셋으로 갈라지는 자리, 같은 단어 아래 다른 모델이 있는 자리, 옮기지 않고 그대로 살리는 길이 있는 자리, 한 단일 등가물이 셋으로 흩어지는 자리, 리전 모델과 글로벌 모델이 부딪히는 자리. 이 다섯을 머릿속에 두고 자기 시스템 위에 매핑을 그리면, 6개월 뒤 회귀 사례가 되는 길을 적어도 한 번은 미리 피할 수 있다.

그런데 매핑 표를 다 본 뒤에 가장 먼저 드는 감정은 시원함이 아니라 막막함이다. *그래서 내 워크로드 중 무엇을 옮길 것인가?* 매핑은 길을 가리켜 주지만 어디로 갈지를 정해주지는 않는다. 옮길 자리와 남길 자리를 구분하는 결정 프레임이 없는 채로 매핑만 들고 뛰어들면, 거의 반드시 한 축에서 빨간불이 켜진 워크로드를 옮기려고 코드를 비비 꼬게 된다.

다음 장에서는 그 결정 프레임을 손에 쥔다. **5축 결정 트리, 자가 진단 18문항, 9패턴 워크로드 결정 매트릭스, 의사결정 워크시트**. 자기 시스템의 컴포넌트 8~12개를 표 한 장에 채워 넣어 "Move now / Move later / 보류 / Don't move"로 분류하는 도구다. 매핑 카탈로그가 *지도*라면, 5장의 결정 프레임은 *나침반*이다. 둘이 한 쌍이다.

기억해두자. **1:1 매핑 표는 친절한 척하는 함정이다.** 표 한 줄 한 줄 끝에 "1:1로 보면 안 되는 이유"가 함께 적혀 있을 때만 정직한 지도가 된다. 그 지도를 들고 함께 다음 장으로 넘어가 보자.
