# 13장. 운영과 정직한 한계 — 비용·관측·outage·lock-in

Cloudflare로 옮긴 지 석 달째, 청구서가 도착했다고 해보자. 마이그레이션 발표 자리에서 우리가 약속한 숫자가 있다. "월 비용 60% 절감, p95 응답시간 200ms 단축." 청구서를 열어보니 줄어들긴 했다. 그런데 예상한 만큼은 아니다. 어디선가 한 줄씩 새고 있다. R2 storage 옆에 Class A operations이라는 항목이 처음 보는 숫자로 찍혀 있다. Workers 요청 수는 전월 대비 두 배가 넘는다. 코드를 바꾼 적이 없는데 왜 그럴까. 청구서를 한참 들여다봐도 어디서 새는지 잘 안 보여서 찜찜하다. 슬랙으로 물어보는 사이 Hacker News 첫 페이지에 빨간 글씨가 떠 있다. "Cloudflare global outage." 이번 분기만 두 번째다. 옆 자리 동료가 묻는다. "이거, 옮긴 거 잘한 결정 맞아?" 답하기가 난감하다.

이 자리에서 우리는 정직해야 한다. 책의 앞 12장에서 우리는 Workers의 콜드스타트, R2의 egress free, Hyperdrive의 round-trip 흡수 같은 약속을 살펴봤다. 약속은 진짜다. 하지만 약속이 진짜라는 사실과, 그 약속이 우리 워크로드에서 우리가 기대한 모양으로 작동한다는 사실은 다른 이야기다. 이 책이 Cloudflare 광고가 아니라는 사실을 가장 분명히 드러내야 하는 자리가 바로 이 장이다. 함께 살펴보자. 비용이 어디서 새는지, 관측이 어디서 비는지, 장애가 났을 때 우리가 어디까지 흔들릴 수 있는지, 그리고 한번 들여놓은 Cloudflare를 다시 빼낼 때 어떤 자리에서 발이 묶이는지.

## "I/O 대기 무료"라는 약속이 깨지는 자리

먼저 가격이다. Workers Standard의 가격 모델은 한 줄로 요약된다. **CPU time × 요청 수, I/O 대기는 무료.** Lambda가 메모리·실행 시간(GB-s) × 요청 수로 과금하면서 외부 API 응답을 기다리는 동안에도 비용이 흐르는 것과 정반대다. AI Gateway를 거쳐 LLM을 호출하고 5초씩 응답을 기다리는 워크로드, S3에서 큰 객체를 읽어 변환 없이 그대로 흘려보내는 프록시 워크로드, 외부 결제 게이트웨이의 webhook을 기다리는 워크플로 — 이런 자리에서는 비용 차이가 자릿수 단위로 벌어진다.

Baselime이 공식 블로그에 쓴 사례가 자주 인용된다. AWS Lambda + ECS 위에 돌던 시스템을 3명이 3개월 안에 Workers로 풀 마이그레이션했더니 일 비용이 $790에서 $25로 떨어졌다. 95% 절감이다. 인상적인 숫자다. 그런데 이 숫자를 우리 시스템에 그대로 갖다 붙이려고 하면 첫 번째 함정이 나타난다. **Baselime의 워크로드는 정확히 Workers 가격 모델이 빛나는 형태였다.** 외부 데이터를 받아 가볍게 가공해 다시 외부로 보내는 옵저버빌리티 백엔드. CPU 무거운 연산은 거의 없고, 거의 모든 시간이 I/O 대기다. Workers 가격 모델은 이런 워크로드를 위해 설계됐다고 봐도 과언이 아니다.

우리 워크로드가 그 모양이 아니라면 어떨까? 예컨대 무거운 JSON parsing, 큰 zod 스키마 검증, 이미지 메타데이터 추출, 암호화 연산 위주의 워크로드라면. 이런 자리에서는 CPU time이 그대로 잡히고, "I/O 대기 무료"의 이점이 거의 적용되지 않는다. Workers의 단가가 Lambda보다 저렴할 수는 있어도 "95% 절감" 같은 숫자는 절대 안 나온다. 운이 나쁘면 별 차이가 없거나, 요청 수가 매우 많은 워크로드(예: 작은 이미지를 초당 수천 번 transform)에서는 Workers 쪽이 미세하게 더 비쌀 수도 있다.

한 가지 더 짚어두자. **Workers 가격 모델은 "외부 API 대기는 무료"인 대신 동시 연결 수에는 한도가 있다.** 한 isolate가 동시에 열 수 있는 outbound 연결은 6개로 제한된다. 평소에는 신경 쓸 일이 없지만, 한 요청 안에서 외부 API를 8개·10개씩 fan-out하는 패턴(예: 한 사용자 요청에 여러 microservice를 한꺼번에 호출하는 BFF 패턴)에서는 이 한도가 곧 응답 시간으로 잡힌다. 7번째 연결은 6번째가 끝날 때까지 큐에 줄을 선다. Lambda에서는 이런 한도가 메모리 단위로 훨씬 느슨하다. 이걸 모르고 옮기면 "왜 같은 코드인데 Workers에서 두 배 느리지?"라는 의문이 한참 풀리지 않아 번거롭다.

또 하나의 함정은 Workers의 **CPU time 한도 자체**다. Workers Standard는 한 요청당 30초의 CPU time까지 허용한다(실제 wall clock은 더 길어도 된다). 30초 안에 끝나는 워크로드라면 충분하지만, 한 요청 안에서 큰 데이터를 정렬하거나 복잡한 검색을 돌리는 워크로드라면 이 한도에 부딪힌다. AWS Lambda는 메모리 단위로 15분까지 허용하기 때문에 한도 감각 자체가 다르다. 이런 자리는 12장의 Workflows로 분해하거나, 아예 ECS에 남기는 편이 낫다.

그렇다면 결정의 첫 단추는 무엇일까. **우리 워크로드의 시간 중 몇 퍼센트가 I/O 대기인지 한 번 측정해보자.** Lambda에서 X-Ray로, ECS에서 APM으로 측정할 수 있다. 80% 이상이 I/O 대기라면 Workers 가격 모델은 우리 편이다. 50% 안팎이라면 비용은 비슷하거나 약간 절감되는 수준이다. 30% 미만, 즉 CPU bound 워크로드라면 비용보다는 글로벌 분산·콜드스타트 같은 다른 이점에서 가치를 찾아야 한다. "egress free 때문에 옮긴다"가 의사결정의 시작점이 되면 이 측정 단계가 통째로 빠지는 경우가 많다. 청구서를 받기 전까지는 모른다. 받고 나면 늦다.

## R2 egress free의 얇은 진실

가격에서 가장 화려한 약속은 R2의 egress free다. S3 Standard에서 30TB를 한 달 동안 다운로드하면 약 $2,700이 나온다. 같은 양을 R2에서 받으면 storage 비용 외에는 0이다. 미디어 스트리밍, 백업 다운로드, AI 모델 가중치 배포처럼 outbound가 큰 워크로드에서는 절감 폭이 90~99%에 이르는 사례가 흔하다. 책 1장에서도 같은 약속을 적었다. 이 약속은 진짜다. 하지만 진짜 약속과 현장에서 우리가 받는 청구서 사이에는 세 가지 함정이 있다.

첫째, **R2는 egress가 free일 뿐 storage와 operations은 free가 아니다.** 2026년 5월 기준 가격으로 storage가 GB당 월 $0.015, Class A operations(쓰기·list·multipart) 100만 건당 $4.50, Class B operations(읽기·head) 100만 건당 $0.36이다. 이 단가만 보면 S3보다 저렴해 보이지만, 작은 객체를 매우 많이 읽고 쓰는 패턴에서는 operations 비용이 한 달에 storage 비용을 넘어서기도 한다. 100만 건당 몇 달러가 별것 아닌 것 같지만, 1초에 1,000건 read가 한 달이면 26억 건이 넘는다. 갑자기 청구서에 $1,000짜리 줄이 하나 더 생긴다. 미디어 한 덩어리를 통째로 받는 워크로드와, 작은 메타데이터 객체를 초당 수천 번 읽는 워크로드는 같은 R2라도 비용 모양이 완전히 다르다.

둘째, **inbound는 free이지만 inbound를 일으키는 쪽의 egress는 그대로 잡힌다.** 마이그레이션 첫 달, S3에서 30TB를 R2로 옮긴다고 해보자. R2 입장에서는 inbound 0원이지만 AWS 입장에서는 그게 30TB의 egress다. CloudFront를 통하면 약 $2,500 안팎, 직접 S3에서 받으면 더 비싸다. 옮긴 다음 달부터는 절감되지만, 옮기는 그 한 달의 청구서가 깜짝 놀랄 만큼 커질 수 있다. 이건 함정이라기보다는 회계의 문제다. 옮길 가치가 충분히 있는 결정이라도 의사결정 라인에서 "첫 달 청구서가 평소보다 $2,500 더 나옵니다"라는 한 줄을 빼먹으면 신뢰가 흔들린다. 미리 말해두는 편이 낫다.

셋째, **R2가 흡수하지 못하는 enterprise 기능들이 있다.** Lifecycle policy의 일부, Glacier 같은 cold storage tier, Object Lock, S3 Inventory, Replication의 일부 — 이런 기능에 의존하던 워크로드는 R2로 옮긴 직후가 아니라 한두 달 뒤 운영 자동화 스크립트가 깨지는 형태로 문제가 드러난다. 옮기기 전에 우리 S3 버킷에 어떤 기능이 켜져 있는지 한 번 점검하자. AWS 콘솔에서 "Properties" 탭과 "Management" 탭을 한 번씩 둘러보는 것만으로도 미리 발견되는 함정이 많다.

한 가지 시뮬레이션을 해보자. 월 30TB outbound, 200만 객체, 객체당 평균 read 5회·write 0.2회인 미디어 서빙 워크로드를 가정한다. S3 Standard에서는 storage $1,380 + egress $2,700 + 작은 ops 비용 = 약 $4,100/월. 같은 워크로드를 R2로 옮기면 storage $900 + egress $0 + Class A ops($1) + Class B ops($3.6) = 약 $905/월. 단순 비교로 78% 절감이다. 이게 정직한 R2의 강점이다. 하지만 같은 30TB가 작은 객체(예: 1KB 메타데이터)를 1억 건씩 read하는 패턴이라면? Class B ops만 100M × $0.36/M = $36/월. 별것 아닌 것 같지만 객체가 매우 많고 자주 읽히는 패턴에서는 ops 비용이 storage 비용을 추월하기도 한다. 우리 워크로드의 객체 크기 분포와 read/write 빈도를 한 번 측정하자. R2 절감폭은 미디어처럼 큰 객체일수록 압도적이고, 작은 객체 다량 패턴일수록 평범해진다.

## KV·D1·DO·Workflows·Queues — 가격 모양의 한 표

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

## 같은 트래픽, 두 청구서 — 한 시뮬레이션

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

## CloudWatch에 익숙한 눈으로 보면 빠진 것들

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

## 2025년 11월 18일, 그리고 12월 5일

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

## "no lock-in"이라는 마케팅과 lock-in이라는 현실

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

## V8 패치 정책 — 빠른 보안의 양면

Cloudflare 운영에서 의외로 자주 토론되는 자리가 V8 패치 정책이다. **Cloudflare는 V8의 보안 패치를 Chrome stable 채널보다 먼저 production에 배포한다.** 보안 취약점이 발견되면 Chrome 사용자보다 Workers 사용자가 먼저 패치된 V8 위에서 코드를 돌리게 된다.

이게 어떤 의미인지 두 방향에서 봐야 한다.

**한 방향에서 보면 강점이다.** Spectre 같은 사이드채널 공격, V8 엔진의 zero-day가 보고된 직후 가장 빠르게 production에 패치가 도달한다. 우리 코드가 multi-tenant 환경에서 다른 고객의 코드와 같은 isolate pool 위에서 돈다는 사실을 떠올리면, 이 빠른 패치는 결정적이다. AWS Lambda는 microVM 격리라서 V8 단일 취약점에 좀 더 둔감하지만, Workers는 V8 단일 취약점이 곧 격리 모델 자체를 흔드는 일이 될 수 있다. 그래서 Cloudflare는 V8 보안에 매우 공격적으로 빠르게 움직인다. 이걸 못 마땅하게 볼 이유는 없다.

**다른 방향에서 보면 양날의 검이다.** Chrome stable에서 며칠 또는 몇 주 더 검증된 패치와, 패치되자마자 production에 들어간 패치는 안정성 면에서 다르다. Hacker News의 한 토론(HN 46458963)에서 정확히 이 자리가 논쟁이 됐다. 어떤 개발자는 "더 빠른 보안이 좋다"고 했고, 어떤 개발자는 "검증되지 않은 패치가 production에 먼저 들어오는 게 무섭다"고 했다. 둘 다 일리 있다.

여기서 정직한 한 줄을 적자. **어떤 워크로드는 한 박자 늦은 버전이 필요할 수 있다.** 결제·금융·의료처럼 안정성 SLA가 보안 SLA만큼 중요한 자리, 또는 V8 자체에 의존하는 매우 정교한 코드(예: 특정 정수 연산 동작에 의존하는 가상 머신)를 돌리는 자리. 이런 자리는 Workers 위에 올리는 게 자연스럽지 않을 수 있다. 대부분의 일반 웹 워크로드는 빠른 보안이 더 좋다. 하지만 모든 워크로드가 그런 건 아니라는 사실을 인정하는 게 정직함이다.

## "이 기술이 무너지는 자리" — 운영과 정직성 편

> **이 챕터 자체가 무너지는 자리.** 이 장은 의도적으로 정직한 한계를 다루지만, 그 정직함에도 한계가 있다.
>
> 첫째, **다음 outage는 예측할 수 없다.** 11월 18일과 12월 5일의 사건이 마지막이라는 보장이 없다. AWS·GCP도 마찬가지다. 우리가 할 수 있는 일은 critical path를 솎아내고 회피 전략을 미리 그려 두는 것까지다.
>
> 둘째, **가격 모델은 변동성이 크다.** 이 책의 표는 2026년 5월 기준이다. R2의 Class A/B operations 단가, KV의 free tier 한도, Workers AI의 Neuron 단가 — 이런 숫자는 분기 단위로 바뀐다. 결정 시점에 공식 페이지를 한 번씩 다시 확인하는 편이 낫다. 부록 E에 추적 가이드가 있다.
>
> 셋째, **lock-in의 깊이는 주관적이다.** 한 팀에는 깊은 lock-in이고, 다른 팀에는 그게 그렇게 깊지 않다. 추상화 레이어 한 겹을 짤 수 있는 팀과 그렇지 못한 팀의 결정이 같을 수 없다. 표는 평균값에 가깝다. 우리 팀의 코드 베이스, 마이그레이션 경험, 운영 인력에 따라 한 칸씩 위 또는 아래로 옮겨 읽자.
>
> 넷째, **이 책 자체에 시간 도장이 찍혀 있다.** 책이 출간된 시점과 우리가 이 페이지를 읽는 시점 사이에 어쩌면 1년이 흘렀을 수 있다. Workers Containers의 GPU 지원, Vectorize hybrid search, Vinext의 production 진입 — 이 책 출간 후 자리가 바뀌었을 영역이 있다. 부록 E의 추적 채널을 한번씩 점검하자.

## 운영 체크리스트 한 페이지

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

## 마무리

이 장에서 우리는 가장 무거운 자리를 살펴봤다. Workers Standard의 가격 모델이 어디서 약속을 지키고 어디서 약속이 얇아지는지, R2 egress free의 진짜 의미와 Class A/B operations·inbound 청구서의 함정, CloudWatch에 익숙한 눈으로 보면 빠진 옵저버빌리티 조각들과 외부 APM이 사실상 표준 패턴이라는 사실, 2025년 두 차례 outage가 가르쳐준 "어디까지 의존할까"의 질문, lock-in의 깊이가 자리마다 다르다는 사실, 그리고 V8 보안 패치 정책의 양면성. 이 장 어디에도 "그래도 Cloudflare가 최고다"라는 결론은 없다. 광고는 다른 책이 하면 된다.

이 책의 자세를 한 줄로 다시 적자. **Cloudflare는 또 하나의 클라우드가 아니라 자리를 잘 골라 내주면 강점이 큰 edge-first 플랫폼이다. 그리고 운영자는 그 강점과 함께 한계도 함께 짊어진다.** 이 자세에서 출발하면 결정이 훨씬 쉬워진다. R2·AI Gateway·Hyperdrive처럼 lock-in이 얕은 자리는 부담 없이 들이고, Durable Objects·Workflows처럼 깊은 자리는 그 깊이만큼 가치가 있을 때만 들이고, critical path는 어떤 벤더에 묶여 있어도 회피 전략을 그려 두자. 청구서는 매월 한 번 들여다보고, 옵저버빌리티는 외부 APM과 함께 짠다.

기억해두자. 이 책은 Cloudflare로 옮기라고 권하는 책이 아니라, **자기 시스템에 Cloudflare가 들어올 자리를 정직하게 결정하도록 돕는 책**이다. 13장은 그 결정의 가장 무거운 무게추다.

다음 14장에서는 이 무게추를 손에 든 채로 마지막 한 걸음을 내딛는다. 5장에서 "무엇을 옮길 것인가"를 결정했고, 6장부터 12장까지 "어떻게 옮길 것인가"의 구체적 도구들을 살펴봤고, 13장에서 "옮긴 다음 어떻게 살 것인가"의 정직한 그림을 그렸다. 14장은 이 모든 것을 시퀀스로 묶는다. **Strangler Fig 패턴 8단계로, AWS 위에 쌓아 올린 시스템을 부수지 않고 Cloudflare를 어디에서부터 어떻게 끼워 넣을 것인가.** 책의 마지막 약속을 함께 살펴보자.
