# 현장에서 살아남는 시스템 디자인

## 작은 internal 시스템부터 글로벌 SaaS까지

**저자:** Toby-AI
**판본:** v1.0.0 · 2026년 5월 17일
**라이선스:** [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

---

## 머리말 — 왜 이 책을 썼는가

이 책을 쓰는 동안 한 가지 풍경이 머릿속에서 떠나지 않았다. 어느 새벽, 결제 시스템 장애 회의를 마치고 자기 자리로 돌아온 한 사람의 풍경이다. 회의에서는 "아무래도 hot partition 같다"는 말이 오갔고, 누군가는 "celebrity 트래픽 아니냐", 또 누군가는 "consistent hashing 재분배가 늦었다"고 했다. 그 단어들이 무슨 뜻인지 정확히 다시 확인하고 싶어서 책장에 꽂아 둔 시스템 디자인 책을 펴 본다 — 그런데 그 단어 옆에는 이렇게만 적혀 있다. **"면접에서 이렇게 답하면 통과합니다."**

이 풍경이 한국 백엔드의 한 단면이라고 생각한다. 우리는 시중에 잘 만들어진 시스템 디자인 인터뷰 책을 여럿 가지고 있다. *Acing the System Design Interview*, Alex Xu의 *System Design Interview*, 그리고 한 단계 더 깊이 들어가려는 사람을 위한 *Designing Data-Intensive Applications*. 그런데 그 책들이 비춰주지 않는 한 칸이 있다. **"내일 출근해서 우리 서비스의 어디를 의심하고 어떤 도구를 꺼내야 하는가"** 하는, 가장 실무적인 자리다. 면접 30분짜리 화이트보드 풀이로 끝나는 답이 아니라, 다음 날 부하 테스트에서 무엇을 모니터링할지·새벽 alert이 울렸을 때 어디부터 의심해야 할지·이 도구를 도입하면 운영의 무엇을 짊어지게 되는지를 함께 짚는 책이 한 권쯤 있어야 하지 않을까. 그게 이 책을 쓰기로 한 가장 단순한 이유다.

### 누구를 위한 책인가

이 책은 입문서가 아니다. HTTP·SQL·인덱스 같은 단어가 처음 보는 것이라면 다른 책을 먼저 들고 오는 편이 낫다. 우리가 가정하는 독자는 다음 정도다.

- 3~7년차 백엔드 엔지니어. Spring·Node·Go·Python 어느 쪽이든 한 프레임워크로 작은 서비스를 만들어 본 경험.
- 캐시·큐·DB를 "쓸 줄은 안다." 단일 시스템은 만들어 봤지만, 트래픽이 커지거나 장애가 나면 무엇을 어디서부터 의심해야 하는지 자신이 없다.
- 인터뷰 책을 한두 권 읽었지만 "내일 production에서 뭘 해야 하지"에는 답이 안 됐다.

이 책의 마지막 페이지를 덮을 때 손에 남기고 싶은 것은 단순하다. **임의의 분산 시스템 장애 회의에서 "어디서부터 의심해야 하는가"를 첫 5분 안에 추론할 수 있게 되는 감각.** 캐시·큐·DB를 도입할 때 묻는 trade-off 질문 30개가 머리에 자동으로 펼쳐지는 손맛. 그리고 무엇보다 — *Acing*·DDIA·Alex Xu의 영어 예시들이 토스·카카오뱅크·당근·쿠팡의 한국 사례와 어떻게 매핑되는지의 **한국어 자막**.

### *Acing*·DDIA와의 관계 — 대체가 아닌 보강

솔직하게 말해 두자. 이 책은 *Acing*도 DDIA도 대체하지 않는다. 오히려 그 책들과 우리 회사 코드 사이에 layer 하나를 더 깐다고 보면 된다. *Acing*은 인터뷰 통과가 목표라 의사결정 trade-off를 압축적으로 보여 준다 — 30분 안에 답을 내는 훈련이지, 다음 날 부하 테스트에서 무엇을 모니터링할지 알려 주는 책은 아니다. DDIA는 이론·논문 기반이 강력하지만 한국 백엔드의 일상 어휘로는 다소 멀다. "이 챕터를 다 읽었는데 그래서 우리 회사는 어디서 어떻게 쓰지?"라는 질문이 남는다. Alex Xu의 책은 그림이 친절하지만 trade-off 깊이·운영 관점·논쟁점은 옅은 편이다.

이 책은 그 세 책 사이에 비어 있는 한 칸 — **"이 도구를 우리가 쓰면 무엇을 얻고 무엇을 잃는가, 그 결정을 어떤 한국 회사가 먼저 내렸고 무슨 학습을 남겼는가, 장애가 나면 어디부터 의심해야 하는가"** — 을 메우려는 시도다. *Acing*과 DDIA를 모두 옆에 두고 이 책을 함께 펴면, 세 책의 합집합이 한국 백엔드 일상에 가장 가깝게 떨어진다고 본다.

### 한국 독자에게 한마디

이 책에는 한국 백엔드의 색깔이 의도적으로 들어가 있다. 0시 동시 트래픽(이자 받기·청약·콘서트 예매), 본인인증·PG 결제 vendor lock-in, 망분리·하이브리드 클라우드(전자금융감독규정), 한국어 형태소 분석(쿠팡 배송 vs 쿠팡배송), 그리고 카카오톡 새해 인사 fan-out 같은 자리들이 영어책에서는 거의 등장하지 않는다 — 그래서 한 챕터씩 의도적으로 박아 두었다.

토스·카카오·당근·쿠팡·우아한형제들·라인·네이버의 실제 발표·블로그가 chapter마다 1~2개씩 인용된다. SLASH·if(kakao)·우아콘 발표가 한국 백엔드의 진짜 일상이 어디 있는지를 가장 정직하게 짚어 준다는 믿음 때문이다. 영어책으로 시스템 디자인을 배우다 보면 "우리 회사 이야기는 없네" 하는 허전함을 자주 느낀다 — 그 결을 채워 보자는 마음이다.

### 마지막으로 — 동료의 어조로

이 책의 문체는 강의실보다 회의실에 가깝다. "이건 이렇게 설계해야 한다"가 아니라, "이렇게 가는 편이 낫다, 왜냐하면 이런 사고가 있었으니까"로 흘러간다. 동료의 어깨를 두드리며 "한 번 같이 들여다보자"라고 말하는 톤이다. 새벽 alert이 울려 본 사람들, 캐시를 한 번 비웠다가 DB가 죽는 광경을 본 사람들, 0시 트래픽이 통신 3사 API까지 흔드는 광경을 본 사람들끼리, 이 책을 옆에 두고 같이 고민해 보자.

— Toby-AI, 2026년 5월

---

## 이 책을 읽는 법

### 1. 순차 읽기 — 가장 자연스러운 길

이 책은 bottom-up으로 짜여 있다. 1부(빌딩 블록 9개) → 2부(분산 시스템 패턴 6개) → 3부(케이스 스터디 5개) → 부록(현장 노트) 순서. 1부의 부품들이 2·3부에서 되짚는 장치(callback)로 재등장하는 구조라, 0장부터 차례로 읽는 길이 가장 매끄럽다. 시간이 충분하다면 이 길을 권한다.

### 2. 발췌 읽기 — 한 도메인이 급할 때

급한 회의가 잡혀 있다면 3부의 한 챕터(예: 19장 결제)로 바로 점프해도 된다. 모르는 단어가 나오면 1·2부의 해당 챕터로 돌아가도록 콜백이 곳곳에 깔려 있다. 가령 16장 채팅에서 "Cassandra hot partition"이 나오면 2장 NoSQL과 13장 샤딩으로 잠시 들렀다 오는 식이다.

### 3. Reference 모드 — 책장에 두고 회의 직전에

trade-off 표·의사결정 트리·운영 체크리스트가 거의 모든 챕터의 마지막에 박혀 있다. 새 기술 도입 회의에 들어가기 전, 해당 챕터의 트레이드오프 표 한 장을 꺼내 보는 식의 쓰임도 가능하다. 부록 A의 "현장 노트 18선"은 새벽 alert에서 꺼내 보기 좋은 카탈로그다.

### 표기 규약

- **(W#) / (P#) / (C#)** — web 자료 / paper / community 자료 번호. 책 뒤의 참고문헌에서 출처를 찾을 수 있다.
- **(검증 필요)** — 1차 자료가 부족하거나 한쪽 의견이 강한 자료. 부풀려 적기보다 정직하게 표시한다.
- **Trade-off 표** — 거의 모든 빌딩 블록·패턴 챕터 끝에 두세 줄 요약 표.
- **Sidebar / 한국 사례 곁 박스** — 토스·카카오·당근 같은 한국 회사 발표·블로그를 챕터마다 1~2개 끼워 넣는다.

---

## 차례

### 서장
- **0장.** 들어가며 — 이 책을 어떻게 읽을 것인가

### 1부. 빌딩 블록
- **1장.** 관계형 DB — 시스템의 backbone을 다시 보기
- **2장.** NoSQL — Dynamo 계열과 Bigtable 계열을 가르기
- **3장.** 캐시 — 거의 모든 시스템의 첫 번째 latency 무기
- **4장.** 메시지 큐 — 비동기와 decoupling의 토대
- **5장.** 검색 엔진 — 한국어가 영어 분석기로 안 되는 이유부터
- **6장.** 로드 밸런서·게이트웨이·서비스 메시
- **7장.** CDN·엣지·객체 스토리지 — 사용자 가까이로 가는 길
- **8장.** 시간·순서·분산 ID — 분산 시스템의 가장 어두운 코너
- **9장.** 분산 시스템의 보안 — 인증·인가·secret·망분리

### 2부. 분산 시스템 패턴
- **10장.** 멱등성·재시도·서킷 브레이커 — 실패를 가정한 통신
- **11장.** Saga·Transactional Outbox·이벤트 소싱 — 분산 트랜잭션의 현실적 길
- **12장.** 합의·복제·일관성 모델 — Raft를 알면 무엇이 보이는가
- **13장.** 샤딩·파티셔닝·Fan-out — 수평으로 늘리는 기술
- **14장.** Rate Limiting·백프레셔·SLO·관측성·on-call — 시스템이 자기 자신을 보는 법
- **15장.** 데이터 파이프라인과 협업 동기화 — Lambda·Kappa·Dataflow + CRDT 짧게

### 3부. 케이스 스터디
- **16장.** 채팅 시스템 — Discord·LINE·당근·Slack
- **17장.** 피드·타임라인·알림 — Twitter·Instagram·카카오톡 fan-out
- **18장.** 검색·매칭·지오 — 쿠팡·Airbnb·Uber·당근
- **19장.** 결제·금융 — Toss·카카오뱅크·Stripe
- **20장.** 이커머스·재고·정합성 — Shopify·쿠팡·Amazon

### 부록
- **부록 A.** 현장 노트 — 책에 안 나오는 일들

### 책의 마무리
- 감사의 말
- 참고문헌
- 판권 (콜로폰)

---

# 0장. 들어가며 — 이 책을 어떻게 읽을 것인가

어느 새벽, 결제 시스템 장애 회의를 마치고 자리에 돌아왔다고 해보자. 회의에서는 "아무래도 hot partition 같다"는 말이 오갔다. 누군가는 "celebrity 트래픽 아니냐", 또 누군가는 "consistent hashing 재분배가 늦었다"고 했다. 그 단어들이 무슨 뜻인지 정확히 다시 확인하고 싶어서 책장에 꽂아 둔 시스템 디자인 책을 펴 본다 — 그런데 그 단어 옆에는 이렇게만 적혀 있다. "면접에서 이렇게 답하면 통과합니다."

우리는 지금 통과가 아니라 답을 알고 싶다.

이 책이 시중의 시스템 디자인 인터뷰서들과 다른 자리에 서고 싶은 이유가 거기에 있다. 면접실에서 30분짜리 화이트보드 풀이로 끝나는 답이 아니라, 다음 날 출근해서 우리 서비스의 어디를 의심하고 어떤 도구를 꺼내야 하는지 함께 짚어 보자는 것이다. 그래서 우리는 매 챕터를 "면접 대답"이 아니라 "production에서 살아남는 사고법"으로 풀어간다.

## 이 책이 인터뷰서가 아닌 이유

먼저 솔직하게 말해 두자. 시스템 디자인 영역에는 이미 좋은 책이 여럿 있다. 만약 *Acing the System Design Interview*나 Alex Xu의 *System Design Interview*를 본 적 있다면, 그 책들이 만든 격자(load balancer, cache, DB, queue, microservice…)에 익숙할 것이다. *Designing Data-Intensive Applications*까지 완주한 분이라면 더 말할 것도 없다. 그렇다면 굳이 또 한 권을 쓸 이유가 무엇인가?

답은 이 책이 그 세 책 사이에 비어 있는 한 칸을 노린다는 데 있다.

- *Acing*은 인터뷰 통과가 목표라 의사결정 trade-off를 압축해서 보여 준다. 30분 안에 답을 내는 훈련이지, 다음 날 부하 테스트에서 무엇을 모니터링할지 알려 주는 책은 아니다.
- DDIA는 이론·논문 기반이 강력하지만 한국 백엔드의 일상 어휘로는 다소 멀다. "이 챕터를 다 읽었는데 그래서 우리 회사는 어디서 어떻게 쓰지?"라는 질문이 따라붙는다.
- Alex Xu의 책은 그림이 친절하지만 trade-off 깊이·운영 관점·논쟁점은 옅은 편이다.

이 책은 그 세 책 어느 쪽도 대체하지 않는다. 오히려 그 책들과 우리 회사 코드 사이에 layer 하나를 더 깐다고 보면 된다. "이 도구를 우리가 쓰면 무엇을 얻고 무엇을 잃는가", "그 결정을 어떤 한국 회사가 먼저 내렸고 무슨 학습을 남겼는가", "장애가 나면 어디부터 의심해야 하는가" — 이 세 질문에 답하는 layer다.

그래서 이 책의 문체는 강의실보다 회의실에 가깝다. "이건 이렇게 설계해야 한다"가 아니라, "이렇게 가는 편이 낫다, 왜냐하면 이런 사고가 있었으니까"로 흘러간다. 동료의 어깨를 두드리면서 "한 번 같이 들여다보자"라고 말하는 톤이라고 생각하면 된다.

## 4축 지형도 — 책은 어디를 비추는가

시스템 디자인이라는 단어가 광활한 만큼, 이 책이 어디를 비추고 어디는 비추지 않는지 먼저 그려 두자. 우리는 책 전체를 다음 4축으로 본다.

> **A. 빌딩 블록** — 캐시·큐·DB·검색·LB·CDN·시간·보안 같은 부품 하나하나. 1부에서 다룬다.
>
> **B. 분산 시스템 패턴** — 멱등성·saga·합의·샤딩·rate limit·관측성·파이프라인 같이, 부품을 안전하게 잇는 규칙. 2부에서 다룬다.
>
> **C. 케이스 스터디** — 채팅·피드·검색매칭·결제·이커머스 같은 실제 시스템. 1·2부의 부품과 패턴이 한 자리에 모이는 모습을 본다. 3부에서 다룬다.
>
> **D. 운영·관측성·SRE** — SLO·alert·postmortem·배포·chaos. 별도 챕터(14장)에 모아 두고, 케이스 챕터마다 곁 박스(sidebar)로 변주한다.

축은 네 개지만, 사실 책의 척추는 한 줄이다 — **"빌딩 블록(부품) → 패턴(조립) → 케이스(현장)" 의 bottom-up 한 줄**. 부품을 알아야 패턴이 보이고, 패턴을 알아야 현장 시스템이 풀린다. 그리고 그 위에 D축(운영)이 가로지른다 — 부품을 잘 골라도 운영을 못 하면 production에서는 죽기 때문이다.

이 책이 다루지 않는 것도 분명히 해 두자. 모바일 백엔드의 push token·APNS 운영 같은 모바일 특수성은 다루지 않는다. 게임 서버의 tick 기반 게임 루프나 동기화 모델도 짧게만 언급하고 넘어간다. AI/LLM 인프라(vector DB·RAG·LLM serving)는 우리가 이 책에서 잡으려는 결과 한 발 떨어져 있어 부록 한 페이지의 "다음 책의 약속"으로 남겨 둔다 — 도구가 더 늘었을 뿐, 우리가 이 책에서 익히는 빌딩 블록·패턴은 LLM 시대에도 그대로 살아 있다.

그렇다면 이 책의 챕터들은 어떤 순서로 읽어야 할까? 가장 자연스러운 길은 1부부터 차례로 가는 것이다. 1부의 부품들이 2·3부에서 되짚는 장치(callback)로 재등장하기 때문이다 — 가령 2장 NoSQL에서 만난 hot partition은 13장 샤딩에서 다시 등장하고, 16장 Discord 마이그레이션에서 한 번 더 모습을 바꿔 나온다. 하지만 급하다면 3부의 한 챕터(예: 19장 결제)로 바로 점프해도 된다. 모르는 단어가 나오면 1·2부의 해당 챕터로 돌아가도록 되짚는 장치가 곳곳에 깔려 있다. 책장에 펴 두고 회의 직전에 한 챕터를 꺼내 보는 식의 reference로도 쓸 수 있다는 뜻이다.

## 독자에게 기대하는 것들

이 책은 입문서가 아니다. HTTP·SQL·인덱스 같은 단어가 처음 보는 것이라면, 다른 책을 먼저 들고 오는 편이 낫다. 우리가 가정하는 독자는 다음 정도를 이미 알고 있다.

- HTTP 1.1/2/3, REST, JSON 직렬화의 기본
- SQL 한 줄을 쓸 줄 알고, 인덱스가 왜 필요한지 직관적으로 안다
- Java/Spring · Node.js · Go · Python 중 적어도 하나의 백엔드 프레임워크로 작은 서비스를 만들어 본 경험
- Linux command·git·Docker 같은 기본 도구

연차로 환산하면 3~7년차 정도다. 이 정도면 "이 도구는 쓸 줄은 안다, 그런데 무엇을 양보한 건지는 자신이 없다"는 단계에 와 있을 것이다. 이 책은 그 단계를 넘어 "도구의 trade-off를 우리 도메인 언어로 설명할 수 있다"는 단계로 데려가려는 시도다.

## 표기 규약 — 인용·trade-off·검증 필요

본격적으로 들어가기 전에, 책 안에서 반복적으로 등장할 표기 약속을 정리해 두자. 너무 빡빡한 규약은 아니지만, 책 끝의 부록과 reference를 빠르게 찾고 싶을 때 도움이 된다.

**인용 표기.** 본문 안에 "(W11)"이라고 나오면 web 자료 11번, "(P5)"는 paper 5번, "(C7)"은 community 자료 7번이라는 뜻이다. 책 뒤의 reference 색인에서 출처를 찾을 수 있다. 가독성을 위해 본문에는 자연어로 풀어 쓴다 — "Stripe 엔지니어 Brandur가 idempotency key 설계 글에서 말하듯…" 식이다.

**Trade-off 표.** 거의 모든 빌딩 블록·패턴 챕터의 끝에 "이것을 쓰면 무엇이 좋고 무엇을 잃는가"를 두세 줄 표로 요약한다. 책 한 권을 다 읽고 나서 회의 자리에 들고 가야 할 가장 실용적인 산출물이 이 표다.

**"검증 필요" 라벨.** 1차 자료가 부족하거나 한쪽 의견이 강한 자료는 본문에 "(검증 필요)"로 표시해 둔다. 우리가 모르는 것을 모른다고 적는 것이 부풀려 적는 것보다 책으로서 더 정직하다고 본다.

**한국 사례 곁 박스(sidebar).** 토스·카카오·당근·쿠팡·우아한형제들·라인·네이버의 실제 발표·블로그를 챕터마다 1~2개씩 의도적으로 끼워 넣는다. 영어책으로 시스템 디자인을 배우다 보면 "우리 회사 이야기는 없네" 하는 허전함을 자주 느낀다 — 그 결을 채워 보자는 마음이다.

## 이 책의 6가지 약속

책 한 권을 읽는 데에는 적지 않은 시간이 든다. 그 시간을 들이는 독자에게, 마지막 페이지를 덮을 때 손에 무엇이 남아 있을지를 약속해 두는 편이 낫겠다. 이 책의 6가지 약속은 다음과 같다.

1. **장애 회의에서 첫 5분 안에 "어디서부터 의심해야 하는가"를 추론할 수 있게 된다.** 캐시인지 DB인지 네트워크인지, 새벽에 자다 일어났을 때도 의심의 순서가 자동으로 펼쳐지도록.

2. **부품 도입 trade-off 질문 체크리스트가 머리에 자동으로 펼쳐진다.** 캐시·큐·DB·검색·LB·CDN 6개 부품 × 다섯 개 질문 = 30개 질문이 도구처럼 손에 잡힌다.

3. **모든 network 호출에 멱등성·재시도·서킷 브레이커·timeout이 한 묶음으로 떠오른다.** "실패는 정상"이라는 인지가 코드 작성 습관으로 박힌다.

4. **외국 사례와 한국 사례 사이에 한국어 자막이 생긴다.** Stripe와 토스, Twitter와 카카오톡, Shopify와 쿠팡의 결정이 어떻게 닮고 어떻게 다른지가 보인다.

5. **on-call alert가 울릴 때 "이 alert가 정말 사람을 깨워야 했는가"를 묻는 메타 시선이 생긴다.** 알람을 줄이고 runbook을 만들고 postmortem을 blameless하게 쓰는 사람이 된다.

6. **새 endpoint를 설계할 때 "인증·인가·secret·rotation·audit log" 5가지가 자동으로 떠오른다.** 보안이 별도 영역이 아니라 모든 빌딩 블록 위에 깔린 통제 평면(control plane)임이 손에 박힌다.

이 6가지 약속은 마지막 챕터(20장 이커머스)와 부록(현장 노트) 사이에서 한 번 더 회수된다. 그때 다시 만났을 때, "그래, 이 책을 읽기 전과 다른 사람이 되어 있다"는 감각이 남는다면 — 우리의 시도는 성공이라고 봐도 좋다.

## 이력서용 기술 도입의 함정 — 도구를 쓰기 전에 먼저 물을 것

여기까지 읽고 나면 마음이 조금 들떠 있을 수 있다. "그래, 우리 회사도 이제 Kafka를 도입해야겠다", "Redis cluster를 깔아 보자", "service mesh를 한번 써 볼까" — 어떤 도구를 발견했을 때 그것을 쓰고 싶다는 충동은 자연스럽다. 그런데 이 충동에는 함정이 하나 숨어 있다. 이 책의 모든 챕터를 정확히 읽기 위해서, 들어가기 전에 짚고 가야 할 메타 시각이다.

OKKY나 velog 같은 한국 개발자 커뮤니티의 단골 토픽 중에 이런 게 있다.

> "이력서에 Kafka 쓰려고 도입했다. 실제로는 RabbitMQ로 충분했다."

이 한 줄에는 한국 백엔드 시장의 한 단면이 들어 있다. 채용 시장의 압력이 기술 의사결정을 왜곡한다는 것이다. "이 회사에서 이 기술 안 써 보면 다음 이직이 힘들지 않을까"라는 불안이 도구 선택의 첫 번째 이유가 되는 순간, 우리는 더 이상 시스템을 설계하는 게 아니다. 이력서를 설계하고 있는 셈이다.

그런데 솔직히 말해, 이 충동은 우리만의 것이 아니다. 영어권에도 "resume-driven development"라는 비슷한 말이 있다. 사람의 본능 같은 영역이라, 부끄럽다고 부정할 일은 아니다. 다만 그 충동에 휘둘렸을 때 production에 어떤 대가가 따라오는지는 정직하게 들여다보자.

### 도입의 자격 — 다섯 가지 물음

새 도구를 도입할 때 우리가 자주 던지는 질문은 "이 도구가 좋은가?"다. 그런데 더 정확한 질문은 다음 다섯 개다.

1. **이 도구를 안 쓰면 정말 못 푸는 문제가 있는가?** 더 단순한 도구 — 우리가 이미 쓰는 DB, 큐, 캐시 — 로 풀 수 있다면, 거의 항상 그 길이 낫다.
2. **우리 팀의 운영 역량이 이 도구를 감당하는가?** Kafka를 깔면 그날부터 consumer lag, rebalance storm, retention 설계가 매일의 일이 된다. 5명짜리 팀이 쿠버네티스 위에 Istio를 얹어 service mesh까지 운영하는 모습은 — 직설적으로 말해 — 끔찍한 일이다.
3. **장애가 났을 때 누가 새벽에 일어나는가?** 도구를 도입한 사람이 1년 뒤에도 그 회사에 있는가. 떠나고 난 다음, 남은 팀원이 그 도구를 책임질 준비가 되어 있는가.
4. **6개월 뒤 이 도구를 걷어낼 길이 있는가?** Event Sourcing처럼 한 번 박으면 빠지지 않는 도구일수록 도입 전에 자격을 더 따져 봐야 한다.
5. **이 결정을 우리 도메인 언어로 설명할 수 있는가?** "Kafka가 빠르니까"가 아니라 "우리 회사의 X 워크로드가 Y 특성을 가져서, Kafka의 Z 성질이 필요하다"로 말할 수 있는가.

이 다섯 개 질문에 모두 자신 있게 답할 수 있을 때, 비로소 도구 도입의 "자격"이 생긴다고 보는 편이 낫다.

### 사례 — Kafka를 RabbitMQ로 돌렸어야 했던 어떤 팀

상상의 사례 한 토막을 그려 보자. 어느 스타트업이 메시지 큐가 필요해졌다. 사용량은 하루 메시지 100만 건 정도, 4시간 retention이면 충분하고, replay는 거의 안 한다. 팀은 8명, on-call 두 명. 어떤 큐가 어울릴까?

순수하게 부하만 보면 RabbitMQ 단일 노드로 충분하다. 그런데 그 팀은 Kafka를 골랐다. 이유는 발표 자료에 "scalable한 architecture를 위해서"라고 적혀 있었지만, 회식 자리에서는 솔직하게 다른 말이 나왔다. "이력서에 Kafka 한 줄 쓰고 싶었어요." 6개월 뒤 그 팀은 ZooKeeper(이후 KRaft) · partition · consumer group · retention 정책 · rebalance · MirrorMaker까지 매주 한 번씩 운영 미팅을 했다. 부하는 여전히 하루 100만 건이었다. 어디서 본 듯한 풍경이다.

물론 이게 Kafka 자체를 비판하는 이야기는 아니다. 정말 Kafka가 필요한 회사에서는 KRaft 위의 Kafka가 가장 강력한 선택이다 — 4장에서 자세히 다룬다. 다만 "Kafka가 좋다"와 "지금 우리가 Kafka를 쓸 자격이 있다"는 다른 문장이라는 것이다. 이 책의 모든 챕터를 읽을 때, "이 도구를 우리가 쓸 자격이 있는가"라는 질문을 빠뜨리지 말자.

### 또 하나의 사례 — service mesh와 5명의 팀

또 다른 풍경. 어느 5명짜리 팀이 "우리도 mesh를 깔자"며 Istio를 도입했다. 3개월 후, 그 팀은 mesh를 튜닝하느라 한 주의 절반을 보내고 있었다. mTLS·observability·traffic split의 가치를 얻기는 했지만, 그 가치를 누리려면 운영의 손이 그만큼 늘어야 한다. 어느 벤치마크는 이렇게 말한다. mTLS를 켠 Istio sidecar는 응답 지연(latency)을 약 166% 늘리고, HAProxy가 50MB로 끝낼 메모리를 Envoy 프록시는 150MB 가까이 쓴다고. 정확한 숫자는 6장에서 다시 본다.

이 숫자는 "그래도 가치가 있다"의 근거가 될 수도, "지금 우리에게는 과하다"의 근거가 될 수도 있다. 정답은 회사마다 다르다. 다만 정답을 자기 도메인 언어로 말할 수 있는 사람과 그저 "요즘 다 mesh를 쓰니까" 도입한 사람은 production에서 완전히 다른 길을 걷는다.

### 도구는 부채다 — 이 책을 읽는 시선

그래서 이 책을 펴 들고 가장 먼저 바꿔야 할 질문이 하나 있다. "이 도구를 도입할까"가 아니라 "이 도구를 도입할 자격이 우리에게 있는가"다. 그리고 이 질문에 대한 답은 보통 "지금 당장 도입하기보다 조금 더 단순한 길을 먼저 시도하자"로 기운다. 이 책이 "도구 카탈로그"가 아니라 "도구를 쓰기 전에 묻는 질문 모음"인 이유다.

기억해 두자. 도구는 자산처럼 보이지만 운영의 시점에서는 부채다. 우리는 도구를 도입함으로써 새로운 운영 책임을 떠안는다. 한 번 도입한 도구를 1년 뒤 걷어내려고 보면, 그 사이에 쌓인 의존이 의외로 얽혀 있어 찜찜하다 — 그 찜찜함을 도입 전에 한 번이라도 들여다보는 시선이 이 책의 출발점이다. 그래서 각 챕터가 trade-off 표를 빼먹지 않고, 한국 회사들의 실패담을 의도적으로 끼워 넣고, 마지막 부록에서 "현장 노트"라는 형태로 production의 18가지 함정을 모은다.

## 책의 약속과 한계를 확인하며

이쯤에서 한 호흡을 가다듬자. 여기까지 따라온 우리에게는 이미 한 가지 시선이 손에 잡혀 있다. 이 책은 인터뷰서가 아니라 production 운영 가이드라는 자리, 4축으로 짚어 보는 지형도, 3~7년차의 동료 독자라는 가정, 그리고 무엇보다 — 도구를 발견할 때마다 "우리가 이걸 쓸 자격이 있는가"라고 한 번 더 묻는 메타 시각이다.

한 가지 더 약속해 두자. 우리는 매 챕터의 톤을 "동료의 회의실 대화"로 유지하려 한다. 매뉴얼처럼 받아 적어야 할 책이 되기보다, 옆에 두고 한 챕터씩 펴 보면서 "그래, 이 정도면 우리도 비슷한 결정을 내릴 수 있겠다"는 자신감을 키우는 책이 되기를 바란다. 그리고 그 자신감의 마지막 형태는 19장 결제 챕터에서 나타난다 — 책의 1·2부에서 익힌 모든 부품과 패턴이 결제 시스템에 한꺼번에 모이는 장면이, 이 책의 클라이맥스다.

물론 한 권의 책으로 모든 영역을 다 다룰 수는 없다. 보안은 9장에 본격적으로 한 챕터를 박았지만, 모바일 백엔드·게임 서버·AI/LLM 인프라는 이 책 밖의 주제다. 그리고 이 책의 본문이 인용하는 리서치 자료도 한계를 가진다 — 예컨대 보안 영역(9장)은 원래 본 리서치 범위에서 부분만 다뤘기 때문에, 챕터 저술 단계에서 OAuth2 RFC·OWASP·전자금융감독규정 같은 1차 자료를 별도로 보강했다. 그 한계를 숨기지 않고 본문 안에 "검증 필요" 라벨로 표시해 둔다.

마지막으로, 이 책은 옆에서 함께 고민하는 동료의 어조를 잃지 않으려 한다. "반드시 이렇게 해야 한다"는 단언보다는 "이렇게 가는 편이 낫다, 왜냐하면…"의 권유로 흘러간다. 우리는 production에서 자주 만나는 같은 고생을 나누는 사이다. 새벽 alert이 울려 본 사람들, 캐시를 한 번 비웠다가 DB가 죽는 광경을 본 사람들, 0시 트래픽이 통신 3사 API까지 흔드는 광경을 본 사람들끼리, 이 책을 옆에 두고 같이 고민해 보자.

## 마무리 — 다음 장으로

자, 1부의 첫 챕터로 들어가자. 1부의 시작은 한국 백엔드의 가장 익숙한 부품이자 가장 자주 의심받는 부품 — 관계형 DB다. 어제 50ms이던 쿼리가 오늘 5초가 되는 새벽 경험을 한 번이라도 해 본 적이 있다면, 1장의 첫 페이지가 낯설지 않을 것이다. 인덱스를 더 추가해야 할까, 아니면 쿼리 형태를 먼저 의심해야 할까. 그리고 그 답을 우리는 어떤 도메인 언어로 동료에게 설명할 수 있을까. 함께 짚어 보자.


---

# 1부. 빌딩 블록 — 시스템을 이루는 부품들

> 캐시·DB·큐·검색·LB·CDN·시간·보안 — 시스템을 이루는 9개 부품 하나하나의 trade-off·운영 함정·한국 사례.
>
> 각 부품을 "쓸 줄 안다"에서 "이 선택의 대가는 무엇인가"로 한 단계 올라가는 자리다. 마지막 9장 보안이 모든 빌딩 블록 위에 깔리는 control plane으로 자리잡는다.

---

# 1장. 관계형 DB — 시스템의 backbone(뼈대)을 다시 보기

어제 50ms이던 쿼리가 오늘 5초가 되는 경험을 안 해 본 백엔드 개발자가 있을까? 새벽에 alert가 울려 들어왔는데, slow query log를 펴 보니 어제와 같은 쿼리다. 인덱스가 빠진 것도 아니고, 코드가 바뀐 것도 아닌데 plan이 통째로 달라져 있다. 사람을 가장 난감하게 만드는 종류의 장애다.

이런 경험은 흔하다. 토스 SLASH 23의 결제 DB 디버깅 발표를 보고 OKKY에 올라온 첫 댓글이 "통계 정보 갱신 안 된 게 진짜 자주 발생함"이었다. r/PostgreSQL에는 한 달 평균 5건쯤 "어제는 50ms, 오늘은 5초" 토픽이 올라온다. Cloudflare가 사내 블로그에 "We debugged a slow query for 3 days"를 시리즈로 연재하는 이유도 같다. 그러니까 이 장면이 우리만의 무능이 아니라는 점부터 합의하고 시작하자. 관계형 DB는 우리가 가장 오래 써온 부품인데도, 가장 자주 우리를 배신한다.

그러니 배신의 자리에서 시작해보자. Postgres와 MySQL을 10년 써왔다는 사람이 어제 빠르던 쿼리가 오늘 5초 걸리는 이유를 5분 안에 후보 3개로 좁힐 수 있는가. 이 질문에 답할 수 있어야 비로소 "RDB를 안다"고 말할 수 있다.

## 왜 아직도 RDB가 90%인가

먼저 던져야 할 질문이 있다. NoSQL이 등장한 지 15년, NewSQL이 등장한 지 10년이 넘었는데도 왜 새로 시작하는 시스템의 절대다수는 여전히 Postgres나 MySQL부터 켜는가?

HN에서 "Just use Postgres"라는 글이 1,500+ 추천을 받는 이유는 단순하다. Simon Willison과 Will Larson을 비롯해 권위자 다수가 같은 말을 하는 휴리스틱이기 때문이다.

> Postgres can be your queue (LISTEN/NOTIFY, SKIP LOCKED), your full-text search (tsvector), your time-series (Timescale), your JSON store (jsonb), your vector DB (pgvector), and your relational DB. Start there.

이 말을 처음 들으면 과한 농담처럼 느껴진다. 하지만 차분히 곱씹어보면 농담이 아니다. 작은 팀이 시스템을 만든다고 해보자. 큐를 따로 띄우고, 검색을 따로 운영하고, JSON store를 따로 박는 비용을 한 번에 다 치를 여력이 없다. Postgres 하나로 시작해서, 트래픽이 정말로 그 부품의 한계를 넘었을 때 그제서야 분리하는 편이 낫다. 처음부터 Kafka를 쓰고, Elasticsearch를 박고, MongoDB를 곁들이는 시스템은 트래픽이 오기도 전에 운영자가 먼저 지친다.

물론 한계는 분명히 있다. 검색은 한국어 형태소 분석이 들어가는 순간 Elasticsearch가 답이고(5장에서 살펴보자), 시계열은 InfluxDB가, 채팅 메시지처럼 한 사용자당 수십만 row가 쌓이는 곳은 NoSQL이 답이다(2장). 그러나 그 한계가 오기 전까지, 우리는 RDB가 줄 수 있는 것을 다 받아 쓰는 편이 낫다. 그 이유를 한 줄로 줄이면 이렇다. **schema, SQL, ACID, 그리고 30년 누적된 운영 도구다.** 이것을 다른 부품으로 갈아끼우는 일은 생각보다 비싸다 — r/ExperiencedDevs의 한 댓글이 가장 정확하다.

> We changed our cache, our queue, our auth — all 'easy'. We changed our primary DB — it took 18 months.

기억해두자. 캐시·큐·인증은 갈아끼울 수 있어도 primary DB는 마지막에 바꾸는 부품이다. 그래서 처음 결정을 잘 해야 하고, 그래서 우리가 이 책의 1장을 RDB에 쓰는 것이다.

## B+ tree — 인덱스가 정말로 무엇을 약속하는가

"인덱스 추가하면 빠른 거 아닌가요?"라는 질문은 가장 흔하면서 가장 위험하다. 인덱스가 무엇이고 왜 빠른지를 모르고 추가하기 시작하면, 어느 순간 인덱스가 16개쯤 박혀 있는 테이블이 만들어진다. write가 느려지고, plan이 자꾸 잘못된 인덱스를 골라잡고, 디스크는 데이터보다 인덱스가 더 큰 상태가 된다. 끔찍한 일이다.

그러니 인덱스가 정확히 무엇을 약속하는지부터 짚고 가자. 대부분의 RDB가 쓰는 인덱스 구조는 **B+ tree**다. *Database Internals*(P22)이 가장 간결하게 정리한다.

> B+ tree는 정렬된 key를 leaf node에 doubly linked list로 연결한다. internal node는 routing만 한다. leaf 사이의 link 덕분에 range scan이 한 번의 traversal로 끝난다. (Petrov, *Database Internals*)

이 한 문장에 인덱스의 약속이 다 들어 있다. B+ tree는 두 가지를 약속한다.

1. **점 조회는 log N**: `WHERE id = 12345`는 root에서 leaf까지 한 번 따라가면 끝. 100억 row여도 30번 정도의 노드 traverse면 끝난다.
2. **범위 조회는 log N + scan 길이**: `WHERE id BETWEEN 1000 AND 2000`은 시작점만 찾으면 leaf 사이의 link로 1000개를 줄줄이 읽으면 된다.

여기까지가 우리가 평소 떠올리는 인덱스의 효용이다. 그렇다면 왜 인덱스가 있는데도 plan이 안 타는 일이 생기는가? 왜 "어제는 50ms, 오늘은 5초"가 되는가?

B+ tree의 성질이 깨지는 순간이 따로 있기 때문이다. 한 가지씩 살펴보자.

### 함정 1. composite index 순서

`(user_id, created_at)`으로 묶인 인덱스가 있다고 해보자. 그런데 쿼리가 `WHERE created_at > '2026-01-01'`만 걸려 있다면, 이 인덱스는 안 탄다. B+ tree는 정렬이다. `user_id`로 먼저 정렬되고, 같은 `user_id` 안에서 `created_at`으로 정렬된다. `created_at` 단독으로는 정렬이 안 돼 있으니, full scan 외에 다른 방법이 없다.

이걸 처음 만나면 어이가 없다. "분명 created_at에 인덱스가 있다고 떴는데?" 그래서 composite의 첫 컬럼이 왜 중요한지를 한 번 강하게 박아두자. **첫 컬럼이 WHERE 절에 등호 또는 IN으로 등장하지 않으면, 그 인덱스는 안 탄다.** Markus Winand의 *Use The Index, Luke!*가 한 페이지 전체를 이 주제에 쓰는 이유다.

### 함정 2. implicit type conversion

`phone_number`가 `VARCHAR`인데 `WHERE phone_number = 01012345678`로 쿼리를 날리면 어떻게 될까? 좌변 컬럼에 implicit cast가 끼면서 인덱스가 사실상 무력화된다. B+ tree의 정렬은 문자열 순서인데 비교는 정수 순서로 들어가는 셈이라, 정렬 순서가 어긋난다. plan에는 그냥 full scan으로 찍힌다.

이런 일은 ORM이 type을 잘못 추론할 때 자주 일어난다. 특히 한국 백엔드에서 흔한 패턴은 BIGINT id를 String으로 받아서 JPA가 native query를 만들 때 캐스팅이 뒤집히는 경우다. 찜찜한 마음으로 EXPLAIN을 펴 보면 어이없이 full scan이 박혀 있다. 한 번 당하면 평생 기억하게 되는 함정이다.

### 함정 3. 통계 정보가 stale

이게 "어제는 50ms, 오늘은 5초"의 진짜 범인이다. 옵티마이저는 plan을 짤 때 통계 정보(planner cardinality)에 기댄다. "이 컬럼의 distinct 값이 1000개 정도다", "이 값 범위의 row가 전체의 10% 정도다" 같은 추정치다.

문제는 데이터가 빠르게 늘면 통계가 따라가지 못한다는 점이다. 예를 들어 `orders` 테이블에 `status` 컬럼이 있다고 해보자. 한 달 전 통계로는 `status = 'PENDING'`인 row가 0.1%였다. 옵티마이저는 "그럼 status 인덱스를 타고 0.1%만 읽으면 되겠군" 하고 plan을 짠다. 그런데 오늘 갑자기 PG가 죽어서 PENDING이 30%로 늘어 있다. 같은 plan으로는 30%를 인덱스로 읽고 row마다 heap을 fetch하니, 차라리 full scan보다 느려진다.

토스 SLASH 23에서 "통계 정보 갱신 안 된 게 진짜 자주" 발생한다고 한 게 이 얘기다. autoVACUUM·autoANALYZE가 못 따라가는 burst가 들어오면 plan이 박살난다. 그래서 운영 패턴 중 하나가 큰 batch 후에 명시적으로 `ANALYZE`를 돌리는 것이다.

### 함정 4. bind parameter peek과 plan cache

같은 쿼리도 어떤 파라미터로 처음 컴파일됐는지에 따라 cached plan이 다르다. 흔치 않은 값(`user_id = 99999999`, 본인만 가지고 있는 ID)으로 prepared statement가 먼저 컴파일됐는데, 그 plan이 캐시에 박혔다. 그 다음부터 흔한 값(`user_id = 1`, 100만 row 매칭)이 들어오면, 안 맞는 plan으로 100만 row를 인덱스 타고 fetch한다. 끔찍하다.

Postgres에서는 `plan_cache_mode`로, Oracle에서는 bind variable peek 설정으로 제어할 수 있다. 다만 이 함정은 처음 만나면 plan이 왜 갑자기 폭주하는지 단서가 거의 없으니, 한 번 당해본 사람이 두 번째에 의심하는 종류의 함정이다.

### 그래서 어떻게 디버깅하는가

네 함정을 다 모아 보면 한 가지 결론이 나온다. **인덱스가 안 타는 90%는 인덱스가 빠져서가 아니라, query 형태나 데이터 분포가 어긋나서다.** *Use The Index, Luke!*의 Markus Winand가 단호하게 정리한다.

> 90% of slow queries are not 'missing index' but 'wrong query shape'. Adding indexes is the band-aid.

한 줄로 줄이면 "인덱스를 추가하기 전에 query를 의심해라"다. 새벽 3시에 slow query가 떴다고 무작정 `CREATE INDEX`부터 치지 말자. 먼저 EXPLAIN을 펴고, `Rows`가 실제와 얼마나 어긋나 있는지 보자. 통계가 stale인지 의심하고, type cast를 의심하고, composite의 첫 컬럼이 빠졌는지 의심하자. 그 다음에도 답이 없을 때 인덱스를 추가하는 편이 낫다.

이 습관 하나만 박혀도 RDB가 가장 자주 우리를 배신하는 새벽 alert를 절반은 막을 수 있다.

## Connection Pool — 정말로 (core × 2) + 1인가

DB가 느려지는 두 번째 큰 범인은 connection pool이다. 의외로 많은 팀이 pool size를 100, 200으로 박아 두고 "왜 이렇게 늦지" 한다. 답을 먼저 말하면, **pool은 작을수록 좋다**.

HikariCP 공식 wiki가 가장 직설적이다.

> connections = ((core_count * 2) + effective_spindle_count) (HikariCP, About Pool Sizing)

CPU 코어가 8개인 DB 서버에 대해 적정 pool size는 16 + 1 = 17 정도다. 직관과 어긋난다. "동시 사용자가 1000명인데 connection이 17개?" 싶다. 하지만 진실은 단순하다. **DB는 CPU에서만 일을 한다.** 동시 active query 수가 코어 수를 넘어가는 순간, 모든 query는 context switch와 lock contention에 시간을 쓴다. 그래서 pool을 키우는 만큼 throughput이 떨어진다.

HikariCP 공식 벤치마크가 보여주는 곡선이 인상적이다. pool size 50일 때보다 10일 때 throughput이 2배 가까이 높다. 같은 시스템인데, pool을 줄였더니 빨라진다. 처음 보면 "정말?" 싶지만, 위의 설명을 곱씹어보면 당연한 결과다.

물론 cloud SSD 시대에 `spindle = 1`로 박는 가정은 단순화다. NVMe·io2 같은 빠른 스토리지에서는 좀 더 키워도 된다. 그러나 시작점은 "core × 2 + 1"이고, 거기서 부하 테스트로 조금씩 늘려가며 throughput이 더 이상 오르지 않는 지점을 찾는 편이 낫다.

### connection pool exhaustion의 도미노

pool을 잘못 잡으면 어떤 일이 일어나는가? 한 service의 slow query가 전체 mesh를 죽인다. tribal #12, "Database connection pool exhaustion → cascade"가 정확한 이름이다.

상황을 가정해보자. 결제 service가 user service의 API를 호출한다. user service는 user DB를 본다. 어느 날 user DB에 slow query가 떠서 한 connection을 5초간 잡고 있다. 그 사이 user service의 다른 요청들이 모두 connection을 기다리느라 막힌다. 결제 service는 user service의 응답을 기다리느라 자기 connection을 잡고 있고, 다른 service들이 결제 service의 응답을 기다리느라 또 막힌다. 한 DB의 slow query 하나가 5분 만에 전체 mesh를 stall시킨다.

그래서 connection pool은 반드시 두 개의 안전장치를 가져야 한다.

- **timeout**: connection 획득에도, query 실행에도 timeout을 박는다. "Every network call MUST have a timeout"이 그냥 나온 말이 아니다(휴리스틱 4 — 10장에서 자세히 다룬다).
- **circuit breaker**: 5초 안에 응답 못 받는 다운스트림은 잠시 차단해서 cascade를 막는다(역시 10장).

물론 connection pool은 부품 한 개의 설정이지만, 그 결정이 분산 시스템 전체의 회복력(resilience)에 직결된다는 점이 흥미롭다. 빌딩 블록 챕터에서 이미 분산의 어둠이 슬쩍 보이는 셈이다.

## VACUUM과 transaction wraparound — Postgres의 가장 어두운 함정

Postgres를 쓰는 팀이 적어도 한 번은 만나는 함정이 있다. **transaction wraparound**다. tribal #8에 들어가 있는 함정인데, 자주 듣고도 자주 잊는다.

Postgres는 MVCC(Multi-Version Concurrency Control)로 동시성을 처리한다. 한 row를 UPDATE할 때마다 새 버전을 만들고, 옛 버전은 "더 이상 보일 필요 없을 때" VACUUM이 와서 청소한다. 그리고 이 모든 동작에 32-bit transaction ID(XID)가 붙는다.

문제는 XID가 32-bit, 즉 약 40억이라는 점이다. 트랜잭션이 40억 번 발생하면 wraparound가 일어난다. 옛 row의 XID가 미래의 XID보다 커 보이는 모순이 생기고, 그러면 DB가 read-only 모드로 전환되어 버린다. 그 다음 "VACUUM FREEZE 하기 전엔 못 일어난다"는 안내문과 함께 4시간짜리 outage가 시작된다.

이 함정을 처음 듣는 사람은 "40억이면 안전한 거 아닌가?" 싶다. 그런데 초당 1000 트랜잭션이면 46일이면 도달한다. burst 트래픽이 잦은 한국 핀테크 환경에서는 더 빠르다. 카카오뱅크가 청약 0시 트래픽 대응을 하면서 가장 먼저 점검하는 부분 중 하나가 autovacuum 설정이라는 발표가 있었다(한국 1).

이를 막는 방법은 명확하다. **autovacuum을 절대 끄지 말자.** 그리고 큰 테이블에서는 `autovacuum_vacuum_scale_factor`를 기본값(20%)보다 낮춰서, 1~5% 변화에도 vacuum이 돌게 만드는 편이 낫다. 무엇보다 `pg_stat_user_tables`의 `n_dead_tup`과 `last_autovacuum`을 정기적으로 보는 습관을 들이는 것이 좋다.

이 함정의 이름이 한국 SRE 커뮤니티에서 자주 회자되지 않는다는 점이 오히려 위험하다. 너무 드물게 일어나서 잊혀지고, 잊혀진 뒤 첫 번째로 만나는 팀이 4시간 outage를 겪는다. 잊지 말자, 32-bit는 작다.

## Aurora — "log is the database"가 무슨 뜻인가

단일 노드 Postgres·MySQL의 운영 함정은 여기까지다 — 라고 끝낼 수 있으면 좋겠지만, 시스템이 커지면 같은 함정이 더 깊은 자리에서 또 다른 모양으로 우리를 기다린다. AWS Aurora는 무엇이 다른가? 그리고 왜 한국 백엔드의 절반쯤이 RDS Postgres에서 Aurora로 이주하고 있는가?

Aurora 논문(P14, SIGMOD '17)이 가장 단호하게 표현한다.

> The log is the database. (Verbitski et al., 2017)

이 한 줄이 핵심이다. 풀어서 보자.

전통적인 Postgres·MySQL은 write를 처리할 때 여러 IO를 친다. 먼저 WAL(write-ahead log)에 redo를 적고, page를 메모리에서 dirty로 표시하고, 나중에 checkpoint에서 page를 disk로 flush한다. replica가 있다면 binlog/WAL을 따로 전송하고, replica는 받은 log를 다시 apply해서 page를 만든다. 같은 변경이 여러 형태(WAL, page, replica WAL, replica page)로 네 군데 다섯 군데를 옮겨다닌다.

Aurora는 이걸 뒤집는다. compute node는 page를 다루지 않는다. 오직 **redo log만** storage layer로 던진다. storage layer는 6-way replication을 가진 분산 시스템인데, 받은 redo log를 자기네가 알아서 page로 reconstruct한다. compute 노드는 stateless에 가깝고, storage layer가 모든 durability를 책임진다.

> Our central design tenet is that the most precious resource is the network. (Verbitski et al., §1)

이 결정 덕분에 Aurora는 MySQL 대비 5배, Postgres 대비 3배 throughput을 낸다. 그리고 더 중요한 운영상의 이득이 있다. replica를 띄울 때 데이터를 복사할 필요가 없다. 이미 storage layer가 공유돼 있다. 그래서 "Aurora replica 추가"는 분 단위가 아니라 초 단위다. read replica로 read load를 분산하는 일이 정말로 쉬워진다.

물론 trade-off는 있다. Aurora는 AWS lock-in이고, 비용은 RDS보다 높다. 그리고 "log is the database"라는 우아한 모델이지만, write latency는 결국 6 quorum 중 4의 ack를 기다려야 한다. cross-AZ network round-trip이 끼니, 단일 노드 Postgres보다 write latency가 약간 더 길 수 있다. NewSQL인 CockroachDB·Spanner와 비교했을 때, Aurora는 "single-leader Postgres의 storage만 분산화한" 모델임을 기억해두자(W4 CockroachDB 비교). 진짜 multi-region active-active write를 원하면 Aurora로는 부족하고, Spanner나 CockroachDB가 답이다.

그러나 한국의 90% 케이스에서, RDS Postgres가 한계에 부딪혔다고 느낄 때 가장 먼저 시도할 마이그레이션은 Aurora다. 우아한형제들도 Aurora I/O optimized로 비용을 30% 줄였다는 발표가 있었다(검증 필요). RDS에서 Aurora로 가는 길은 거의 무중단으로 가능하다. 그게 가장 큰 강점이다.

## Trade-off 표 — 어떤 DB를 골라야 하는가

이 정도 살펴봤으면, 새 서비스에 RDB를 골라야 할 때 무엇을 보고 결정할지 한 장으로 압축할 차례다. 우리가 평소에 가장 자주 만나는 4개를 표로 모아 보자.

| 항목 | Postgres (self-managed) | MySQL (self-managed) | Aurora (Postgres/MySQL) | CockroachDB |
|------|--------------------------|------------------------|--------------------------|-------------|
| **architecture** | single leader + streaming replication | single leader + binlog replication | "log is the database", 6-way storage | distributed SQL, HLC 기반 |
| **write throughput** | 단일 노드 한계 (코어·디스크 종속) | Postgres와 비슷 | Postgres 대비 ~3x (P14) | 수평 확장 가능, 단 single-row write는 더 느림 |
| **read replica 추가** | streaming setup, 분~시간 | binlog setup, 분~시간 | shared storage, 분 단위 즉시 | 자동 |
| **multi-region write** | 불가 (read-only replica만) | 불가 (read-only replica만) | Global Database (write는 한 region) | active-active 가능 |
| **isolation** | true serializable 가능 | repeatable read (default) | Postgres/MySQL 동일 | serializable default |
| **운영 부담** | 자체 backup·HA·VACUUM 모두 직접 | 자체 backup·replication 직접 | AWS가 backup·failover 처리 | 자체 운영, 또는 CockroachDB Cloud |
| **vendor lock-in** | 없음 | 없음 | AWS 강함 | 약함 (self-hosted 가능) |
| **권장 케이스** | 시작점, 작은 팀 | OLTP write-heavy, MySQL 운영 경험 풍부 | RDS의 다음 단계, AWS 친화 팀 | 진짜 multi-region 필요, 글로벌 서비스 |
| **회피 케이스** | 진짜 multi-region | 진짜 multi-region | 진짜 multi-region active-active | OLTP latency 민감, 작은 팀 |

표를 한 줄로 줄이면 이렇다. **시작은 Postgres, 한계가 오면 Aurora, 진짜 글로벌이면 CockroachDB나 Spanner.** 그리고 Daniel Abadi가 NewSQL 비판에서 짚은 대로, "NewSQL이 default로 serializable이라는 marketing은 종종 사실이 아니다"는 점도 기억해두자(자료 4, Abadi 2018). NewSQL의 약속을 곧이곧대로 받아들이지 말고, 자기 isolation level을 한 번은 EXPLAIN으로 검증하는 편이 낫다.

## Sidebar: JPA N+1과 우아한형제들의 진단 패턴

한국 백엔드의 일상에서 가장 흔하면서 가장 silent killer — 조용히 죽이는 함정 — 인 녀석을 한 페이지 따로 보고 가자. **JPA N+1**이다.

상황을 가정해보자. `Order` 엔티티가 `User`를 ManyToOne으로 참조하고, `User`가 `Address`를 OneToMany로 가지고 있다. 화면에서 주문 목록 100개를 보여주려고 `orderRepository.findAll()`을 호출한다. 한 번의 SQL로 끝날 것 같지만, fetch type이 LAZY로 잡혀 있으면 N+1 query가 터진다.

- `SELECT * FROM orders LIMIT 100` — 1 쿼리
- `SELECT * FROM users WHERE id = ?` — 100 쿼리 (각 order의 user 조회)
- `SELECT * FROM addresses WHERE user_id = ?` — 100 쿼리 (각 user의 주소 조회)

총 201개의 쿼리가 한 화면 렌더링에 나간다. 끔찍하다. 그리고 더 끔찍한 건, 개발 환경에서는 데이터가 적어서 안 보인다는 점이다. production에 올라가서 트래픽이 들어와야 비로소 DB가 비명을 지른다.

우아한형제들 techblog에 N+1 회피 가이드가 여러 번 올라온 이유가 이거다(한국 6). 한국 백엔드의 절대다수가 Spring + JPA를 쓰니, 이 패턴이 일상의 함정이다. 우아한형제들이 정착시킨 진단 패턴을 한 줄로 줄이면 다음과 같다.

1. **개발 환경에 hibernate.show_sql + p6spy를 켜자.** 실제 query가 몇 개 나가는지를 눈으로 본다.
2. **fetch join 또는 @EntityGraph로 명시적 join을 강제하자.** LAZY가 default라 가정하고, 한 화면에서 함께 보여줄 연관 엔티티는 명시적으로 한 쿼리에 모은다.
3. **DTO projection을 우선시하자.** 화면 전용 view라면 굳이 엔티티 전체를 가져올 필요가 없다. JPQL의 `new com.example.OrderDto(o.id, u.name, ...)`로 select projection을 박는다.
4. **production에서 query log + APM의 SQL count를 모니터링하자.** 한 요청당 query가 갑자기 100개를 넘는 endpoint가 있으면 N+1을 의심한다.

JPA를 쓰지 않는 사람도 같은 함정을 ORM마다 자기 식으로 만난다. Rails의 ActiveRecord에서는 `.includes`로, Prisma에서는 `include`로 해결한다. 도구는 다르지만, "한 화면에 쓰일 데이터는 한 쿼리에 모으자"는 원칙은 같다.

5장 검색 엔진에서 만나게 될 인덱싱 파이프라인의 silent killer — 한국 백엔드는 그 함정과 이 N+1, 두 개를 평생 안고 산다. 잊지 말자.

## 이 장의 약속 회수

새벽 3시에 slow query alert가 울렸다고 해보자. 이 장을 다 읽은 우리는 무엇을 첫 5분 안에 할 수 있는가?

1. **인덱스 추가부터 의심하지 않는다.** EXPLAIN을 펴고, `Rows estimated`와 `Rows actual`의 괴리부터 본다. 통계가 stale인지 의심한다.
2. **composite index의 첫 컬럼이 WHERE에 등호로 들어 있는지 확인한다.** 빠져 있으면 인덱스는 안 탄다.
3. **type cast가 발생하는지 EXPLAIN의 plan에서 보자.** implicit conversion이 잡히면 거의 확정 범인이다.
4. **trace한 query가 prepared statement라면, plan cache가 잘못 박혔는지 의심한다.** 같은 쿼리를 ad-hoc으로 던져 본 plan과 비교한다.
5. **autovacuum이 돌고 있는지, `n_dead_tup`이 얼마나 쌓였는지** `pg_stat_user_tables`로 확인한다. burst 직후라면 명시적 `ANALYZE`를 한 번 돌린다.
6. **그리고 마지막에야 인덱스 추가를 고민한다.**

이 6단계가 머릿속에 자동으로 펼쳐지면, 우리는 "RDB를 안다"고 말할 자격이 있다. 그리고 이 책의 6번째 약속 — "이 책을 다 읽으면 새 endpoint를 설계할 때 자동으로 의심해야 할 5가지가 떠오른다" — 의 첫 번째 회수가 여기서 일어났다.

## 다음 장으로 가는 다리

RDB는 우리에게 schema·SQL·ACID·30년 운영 도구를 약속한다. 그러나 단일 노드의 한계, 한 row당 수십만 versioned write, partition key를 마음대로 정해야 할 도메인을 만나면 RDB는 더 이상 답이 아니다.

그래서 다음 장에서는 NoSQL을 살펴본다. 정확히 말하면, "schema가 유연해서" "확장이 쉬워서" NoSQL을 고른다면 도대체 무엇을 양보한 것인지를 묻는다. Dynamo 계열과 Bigtable 계열이 어떻게 다르고, hot partition이 왜 평생의 적인지를 살펴보자. RDB에서 가장 자주 우리를 배신하던 통계 정보의 함정이, NoSQL에서는 어떻게 다른 모습으로 나타나는지도 함께 본다.

다음 장으로 가기 전에 한 번 정리하자. **RDB가 우리를 배신하는 90%는 인덱스가 빠져서가 아니라, query 형태와 데이터 분포가 어긋나서다.** 이걸 기억하는 것만으로도 우리는 한 단계 위로 올라간 백엔드 개발자다.

---

---

# 2장. NoSQL — Dynamo 계열과 Bigtable 계열을 가르기

AWS Summit Korea의 어느 발표에서, 한 엔지니어가 이런 말을 했다고 해보자. "DynamoDB 마이그레이션 중에 부하 테스트는 모두 통과했다. 그런데 출시 30분 만에 한 partition이 전체 트래픽의 95%를 받기 시작했다. 우리 서비스에 celebrity 사용자가 있었다는 사실은 그날 밤 12시에 알게 됐다."

이 한 토막에 NoSQL이라는 영역의 모든 어려움이 농축돼 있다. 어제까지 RDB가 자기 일을 잘하고 있었는데, "확장이 안 된다"는 이유로 NoSQL을 도입하면 그날부터 새로운 종류의 고통이 시작된다. 그 고통의 이름은 대부분의 경우 **hot partition**이다. 그리고 이 단어가 무서운 진짜 이유는, 부하 테스트로는 잘 안 잡힌다는 데 있다. 우리는 보통 uniform random key로 부하를 흘리는데, 실제 사용자는 절대 uniform하지 않다.

NoSQL이 "schema-less라 편하다"는 이유로 도입된 적이 있다면, 이미 우리 회사 어딘가에는 hot partition 폭탄이 깔려 있을 가능성이 적지 않다. 1장에서 RDB를 다뤘으니, 이제 RDB의 결을 따라가지 않는 시스템들 — Dynamo 계열과 Bigtable 계열의 두 큰 갈래 — 을 함께 짚어 보자. 이 둘을 가르고 나면 NoSQL이라는 막연한 단어가 훨씬 또렷한 두 모양으로 보이기 시작한다.

## 1. NoSQL이라는 단어가 진짜로 양보한 것

먼저 솔직하게 짚자. "NoSQL"이라는 단어 자체는 마케팅 용어에 가깝다. SQL이 없다는 것보다, 무엇을 양보하고 무엇을 얻었는지가 본질이다. NoSQL이라는 우산 아래 들어가는 시스템들의 공통 양보 항목은 대체로 다음과 같다.

- **schema의 강제력**을 양보했다. 컬럼 추가가 쉬워지지만, 그 대신 application이 schema를 책임진다.
- **다중 row JOIN과 복잡 트랜잭션**을 양보했다. 단일 row의 빠른 read·write를 얻는 대신.
- **strong consistency를 (대부분) 양보**했다. Dynamo 계열은 양보하고, Bigtable 계열은 부분만 양보한다 — 이게 두 갈래의 본질적 차이다.

그 대신 무엇을 얻었는가? horizontal scale, write throughput, write-heavy workload, 그리고 "schema migration이 비교적 덜 아픈" 구조. 이게 NoSQL의 표면 가치다.

여기서 자주 오해되는 단어가 하나 있다 — "schema-less"다. 정확한 표현은 **"schema-on-read"(읽을 때 비로소 schema가 적용된다)** 또는 **"query-first schema"**다. 데이터 모델링을 안 해도 된다는 뜻이 아니라, 어떤 query를 자주 던질 것인지를 먼저 결정하고 그 query에 맞게 데이터 모양을 박는다는 뜻이다. RDB는 데이터를 정규화해 두고 query 시점에 join으로 합치지만, NoSQL은 query 모양대로 데이터를 미리 비정규화해서 박는다. 이 인지가 없으면 NoSQL을 도입한 뒤 "왜 우리 쿼리가 다 secondary index가 필요하지?"라며 찜찜해진다 — 처음부터 query-first로 설계하지 않은 결과다.

기억해 두자. **NoSQL은 schema-less가 아니라 query-first다**. 이 한 줄이 이 챕터를 관통하는 한 줄의 지도다.

## 2. Dynamo 계열 — leaderless·eventual·vector clock의 세계

2007년, Amazon이 SOSP 학회에 발표한 한 편의 논문이 NoSQL의 한 갈래를 결정지었다. Werner Vogels와 동료들이 쓴 *Dynamo: Amazon's Highly Available Key-value Store*다. 이 논문이 던진 질문은 이거였다 — **장바구니가 절대 사라지지 않도록 만들려면, 일관성을 어디까지 양보해야 하는가?**

Amazon의 답은 분명했다. 장바구니에 물건을 담을 때 잠시 두 버전이 동시에 존재하더라도, "장바구니에 물건이 들어갔다는 사실 자체는 반드시 살아남아야" 한다는 것이다. 즉 **availability와 partition tolerance를 우선하고, consistency를 application 레벨에서 합친다**. CAP 정리의 단어로 말하면 AP를 골랐다는 뜻이다.

### Dynamo 계열의 네 가지 핵심 결정

1. **Leaderless replication.** master가 없다. 모든 노드가 read·write를 받는다. 이건 SPOF를 없애고 write availability를 끌어올리는 결정이다. 대신 conflict가 생긴다.
2. **Consistent hashing + virtual node.** 키를 ring 위에 매핑하고, vnode 100~200개로 나누어 노드 추가·제거 시 데이터 이동을 최소화한다. 이건 13장 샤딩에서 더 자세히 다룬다.
3. **N/R/W tunable quorum.** 데이터를 N개 노드에 복제하고, read에 R개·write에 W개의 응답을 기다린다. R + W > N이면 strong-ish consistency를 얻고, 그렇지 않으면 더 빠른 응답을 얻는다. trade-off는 application이 정한다.
4. **Vector clock으로 conflict 해소.** 두 노드가 동시에 같은 key에 write를 하면 vector clock이 두 버전을 모두 들고 다닌다. 그리고 application이 "어떤 버전을 살릴 것인가"를 결정한다. 장바구니라면 union, 카운터라면 max — 도메인 의미가 conflict 해소에 들어온다.

이 네 가지 결정이 합쳐져, **Dynamo 계열은 "느슨한 합의로 always-writable(언제나 쓸 수 있다)"**라는 한 줄로 요약된다. 그 후예가 오늘날의 DynamoDB (Amazon이 만든 managed 서비스), Cassandra (Facebook이 SIGOPS 2010에 발표한 P9), ScyllaDB (Cassandra wire-compatible 재구현), Riak (지금은 명맥이 약해진 OSS Dynamo) 등이다.

여기서 흥미로운 사실 — **DynamoDB와 Dynamo 논문은 다른 시스템**이다. 논문의 Dynamo는 내부 시스템이었고, 오늘의 DynamoDB는 그 영감을 받았지만 single-leader per partition + Paxos 기반 metadata로 구현됐다. 그래서 DynamoDB는 strong consistency 옵션도 제공한다. "Dynamo 계열"이라는 분류는 마케팅이 아니라 설계 철학을 가리키는 단어로 받아들이는 편이 낫다.

## 3. Bigtable 계열 — single-leader·tablet·strong consistency

같은 시기, 다른 회사의 답은 달랐다. 2006년 OSDI 학회에 Google이 발표한 *Bigtable: A Distributed Storage System for Structured Data* (P8)는 또 다른 갈래를 만들었다. Bigtable이 풀려고 한 문제는 Dynamo와 정반대였다 — **거대한 sparse 테이블을 strong consistency로 잘게 쪼개서, 빠른 range scan을 가능하게 하자**.

### Bigtable 계열의 네 가지 핵심 결정

1. **Tablet 단위 single-leader.** 전체 테이블을 row key 범위로 쪼개 tablet으로 만들고, 각 tablet마다 leader가 한 명 있다. 그 leader가 해당 tablet의 read·write를 모두 책임진다. partition 단위의 strong consistency.
2. **Chubby (지금은 Spanner의 일부)에 의존한 metadata.** tablet location, leader election을 외부 coordination service에 맡긴다. 이게 운영 부담의 진짜 원천이다 — 8장의 분산 조정 서비스 영역과 닿는다.
3. **Range-based partitioning.** Dynamo 계열의 hash 기반과 달리, row key의 사전 순서대로 partition을 만든다. range scan이 빨라지지만, key가 timestamp나 sequential ID이면 latest partition으로 모든 write가 몰린다. 또 다른 hot partition이다.
4. **Column family + sparse storage.** 한 row가 수백만 컬럼을 가질 수 있고, 컬럼 family 단위로 LSM-tree 파일이 갈린다.

Bigtable 계열의 후예는 HBase (Apache, Hadoop 생태계), Google Cloud Bigtable (managed), 그리고 Spanner (TrueTime이 추가된 외부 일관성 글로벌 DB — 12장에서 다룬다). 분류 측면에서는 HBase가 가장 직설적인 Bigtable 후계자다.

## 4. 두 갈래 비교 — 표 하나로 보는 trade-off

말로 풀어 쓴 차이를 한 페이지의 표로 압축해 보자. 이 표는 회의 자리에서 "우리 워크로드는 어느 계열에 어울리는가"를 결정할 때 손에 잡히는 도구가 된다.

| 축 | Dynamo 계열 (Cassandra·DynamoDB·Scylla) | Bigtable 계열 (HBase·Bigtable) |
|---|---|---|
| 복제 모델 | Leaderless quorum (N/R/W) | Tablet-level single-leader |
| 기본 consistency | Eventual (tunable) | Strong (per tablet) |
| Partition 방식 | Hash-based (consistent hashing) | Range-based |
| 핵심 의존성 | gossip protocol | external coordination (ZooKeeper·Chubby) |
| Hot partition 원인 | celebrity key | sequential key |
| Conflict 해소 | vector clock·LWW | leader가 단일 truth |
| Write 친화도 | 매우 높음 | 매우 높음 |
| Range scan | 약함 | 강함 |
| 대표 사례 | Discord·당근·Netflix·Apple iCloud | Spanner·Bigtable·HBase·LINE 일부 |

표는 깔끔하지만, 정작 production에서는 어느 줄 하나가 우리를 새벽에 깨운다. 그게 다음 절의 주제다.

## 5. Hot Partition — 평생의 적

NoSQL을 1년 이상 운영한 팀은 거의 예외 없이 hot partition에 한 번씩 데인다. HN의 한 토론에서 어떤 엔지니어가 적었다고 한다. "We had a celebrity in our user table. 1 partition was 95% of our reads." 그리고 또 다른 사용자는 "Adaptive capacity kicks in after 5-15 min, but we lost 4 hours before figuring out our key was wrong"이라고 적었다. 이 두 줄에 hot partition 디버깅의 잔인함이 다 있다.

왜 hot partition은 막기 어려울까? 이유는 다섯 가지가 겹쳐 있다.

1. **부하 테스트가 uniform random key로 돌아간다.** 실제 사용자는 절대 uniform하지 않다. 한 명의 celebrity, 한 개의 viral content, 한 곳의 이벤트가 분포를 완전히 비튼다.
2. **Alert가 "전체 QPS"만 보고 있다.** shard별 QPS skew는 잡지 않는 경우가 흔하다.
3. **Adaptive capacity가 즉시 발동하지 않는다.** DynamoDB는 5~15분이 지나서야 hot key의 capacity를 다시 분배한다. 그 사이의 5분이 사용자에게는 영원이다.
4. **NoSQL의 partition key는 한 번 정하면 바꾸기 매우 어렵다.** RDB의 인덱스처럼 마음껏 추가·삭제할 수 없다.
5. **Celebrity는 늘 출현한다.** 사용자가 1억 명이면 1억분의 1 확률의 거물이 반드시 한 명 이상 있다.

이런 사정을 알면, hot partition을 막는 작업은 도구 도입의 시점이 아니라 **partition key 첫 줄을 쓰는 그 순간**에 시작된다는 것이 이해된다. 그래서 NoSQL을 다루는 시니어 백엔드는 partition key 첫 줄을 보면 거의 직감적으로 "이거 hot 가능성 있다"고 느낀다. 이 직감을 키우는 방법은 안티패턴 몇 개를 손에 익히는 것이다.

### Partition key 안티패턴 5선

다음 다섯 가지 key 설계는 hot partition을 거의 보장한다 — 가능하면 처음부터 피하자.

1. **시간 prefix만 박은 key** (예: `2026-05-16#order-id`) — 자정마다 모든 write가 한 partition에 몰린다. Bigtable 계열에서 특히 치명적이다.
2. **enum 값을 prefix로 박은 key** (예: `status#PENDING#order-id`) — status가 PENDING인 row가 압도적으로 많으면 한 partition이 다 받는다.
3. **순차 증가 ID prefix** (예: auto-increment ID로 partition) — 가장 최신 partition으로 모든 write가 쏠린다.
4. **소수의 정상 사용자 key** — Twitter나 Instagram의 celebrity 사용자가 그대로 partition key가 되면, 그 사람이 트윗 올리는 순간 한 partition으로 모든 트래픽이 쏠린다 — 숫자로 적기 민망한 QPS다.
5. **너무 큰 grain의 key** (예: country code로 partition) — 한국·미국·일본이면 partition이 3개라는 뜻이다. 분산이 거의 안 된다.

이 5개를 피하기만 해도 운영의 절반은 이긴 셈이다. 그렇다면 hot partition이 일단 발생했을 때 무엇을 할 수 있을까?

### Hot partition 발생 후 — 응급 처치 3단계

**1단계: write-side에 jitter·shard 추가.** key 뒤에 random suffix(`#0`~`#15` 같은)를 붙여 한 사용자의 write가 16개 sub-partition으로 흩어지게 한다. read 시점에 16개를 모두 읽어 합쳐야 하므로 비용은 크지만, 응급 처치로는 빠르다.

**2단계: read-side에 cache layer 또는 request coalescing.** 같은 key를 동시에 30,000번 요청하는 게 hot partition의 본질이라면, 그 30,000번을 1번으로 합치는 게 가장 직접적인 방어다. Discord가 정확히 이 길을 택했다 — 잠시 후에 다룬다.

**3단계: 파티션 키 재설계 + 마이그레이션.** 가장 비싼 길이지만, 진짜 root cause다. dual-write·shadow read로 점진 이전하는 plan은 11장에서 다룬다. 한 번 결정하면 보통 2~3개월의 작업이라, 새벽 alert가 1주일 째 안 멈춘다면 결단이 필요하다.

기억해 두자. **hot partition은 거의 모든 NoSQL 운영의 1번 알람이다**. partition key 설계 단계에서 안티패턴을 피하는 비용이, production에서 마이그레이션하는 비용보다 1000배쯤 싸다.

## 6. LSM-tree — write-heavy의 진짜 이유

NoSQL이 write-heavy workload에 강하다는 말은 자주 들리지만, 그 이유가 정확히 무엇인지는 덜 다뤄진다. 답은 대부분 **LSM-tree (Log-Structured Merge Tree)**에 있다. 1996년 P. O'Neil 외 4인이 발표한 원전 논문(P13)이 이 자료구조를 처음 제시했고, 오늘날 Cassandra·RocksDB·LevelDB·DynamoDB 내부·HBase가 모두 이 구조 위에 올라가 있다.

LSM-tree의 핵심 아이디어는 단순하다. **메모리에 정렬된 buffer(memtable)를 두고, full이 되면 disk에 sorted file(SSTable)로 흘려보낸다**. 그러고 나서 정해진 간격으로 여러 SSTable을 merge해 더 큰 SSTable을 만든다. 이걸 compaction이라고 부른다.

이 구조의 가치는 두 가지다. 첫째, **write가 sequential I/O**다 — disk seek가 없다. SSD에서도 random write보다 sequential write가 더 빠르고 lifetime에 유리하다. 둘째, **write가 immutable**이다 — 한 번 disk에 쓴 SSTable은 더 이상 수정되지 않는다. 이게 동시성·복제·snapshot을 단순하게 만든다.

대신 양보한 게 있다. **read amplification**이다. 한 key를 읽으려면 memtable 1개 + disk에 있는 N개의 SSTable을 모두 뒤져야 한다. 이걸 완화하는 도구가 **bloom filter**다 — 각 SSTable마다 "이 key가 여기 있을 수도 있다 / 없다"를 빠르게 판단하는 확률적 자료구조. 없다고 판단되면 그 SSTable은 안 본다. 그런데 bloom filter의 false positive ("있을 수도 있다고 잘못 알려줌")가 가끔 over-fetch를 일으킨다. 첫 번째 만남에서는 거의 늘 의심하지 않는 자리라 더 찜찜하다 — 이 함정은 부록 A의 18가지 tribal knowledge 중 7번 항목에서 다시 다룬다.

또 하나의 함정 — **tombstone**이다. delete가 "지우기"가 아니라 "삭제 마커 쓰기"로 구현되는 LSM-tree의 특성상, TTL이나 대량 delete가 많으면 read가 tombstone을 잔뜩 만나게 된다. Cassandra에서는 한 partition의 tombstone이 1000개를 넘으면 alert를 띄우는 게 거의 표준이다. 이 함정도 부록 A에서 다시 다룬다.

LSM-tree와 대비되는 게 1장 RDB에서 다룬 **B+ tree**다. B+ tree는 in-place update라 read가 predictable하고 write amplification이 낮지만, 대신 random write이라 throughput 한계가 더 빠르다. **write/read 비율과 latency 분포의 모양이 둘 중 어느 쪽이 어울리는지를 결정한다** — write가 99%이고 read의 latency tail이 길어도 괜찮다면 LSM, read latency 일관성이 중요하면 B+ tree.

## 7. Discord 마이그레이션 — 디테일까지 들여다보는 사례

Dynamo 계열의 가장 유명한 운영 케이스 하나를 깊이 들여다보자. 2022년경 Discord가 자사 메시지 storage를 **Cassandra 약 177노드에서 ScyllaDB 약 72노드로** 옮긴 이야기다 (정확한 노드 수는 Discord 발표 자료 기준 — 검증 필요).

Discord가 직면한 문제는 두 가지였다. 첫째, **GC pause**다. Cassandra는 JVM 기반이라 stop-the-world GC가 평균 read latency를 흔든다. 둘째, **single message hot key**다. 어느 인기 메시지 하나가 초당 30,000번 요청을 받는다 — 한 partition이 죽기에 충분한 부하다.

ScyllaDB는 C++로 Cassandra wire protocol을 재구현한 시스템이다. JVM이 없으니 GC pause가 없고, shard-per-core 아키텍처로 NUMA 친화적이다. 마이그레이션 후 **p99 read latency가 40~125ms에서 약 15ms로 떨어졌다**고 Discord 엔지니어링 블로그는 적는다. 노드 수도 절반 미만으로 줄었다.

하지만 진짜 흥미로운 부분은 ScyllaDB 자체가 아니라 **Rust로 작성한 data services layer**다. Discord는 이 layer에서 **request coalescing**을 구현했다. 같은 메시지에 대한 동시 요청을 한 묶음으로 합쳐 DB에는 한 번만 보낸다는 뜻이다. 인용을 보자.

> "Request coalescing is an important responsibility to avoid multiple database calls when many users request the same message."

이 한 줄에 NoSQL 운영의 한 통찰이 들어 있다. **DB 자체를 더 좋은 것으로 바꾸는 것보다, DB 앞에 코드 한 줄을 잘 짜는 게 훨씬 효과적일 때가 있다**. 30,000번을 1번으로 합치면, 어떤 DB든 살아난다. 이 패턴은 3장 캐시의 singleflight 패턴과 한 가족이다.

Discord 마이그레이션은 16장 채팅 시스템에서 한 번 더 깊이 다룬다. 거기서는 메시지 모델·sharding·WebSocket connection 관리와 함께 본다.

## 8. 한국 사례 — 당근의 DynamoDB 선택

이번엔 한국 사례 한 자락을 짚어 보자. 당근(이전 당근마켓)이 채팅 시스템을 만들 때 한 의사결정이다. 당근 채팅팀은 채팅 storage로 **Cassandra가 아닌 DynamoDB**를 골랐다. 이유는 발표(AWS Summit Korea 2022 "2200만 사용자 채팅")에서 솔직하게 밝혀졌다 — **"Cassandra 운영 부담을 회피"**.

이 결정에는 한국 백엔드의 현실적 맥락이 묻어 있다. 자체 IDC가 아니라 AWS 위에 시스템을 올리는 회사 — 인프라팀이 작거나, 24시간 on-call 인력이 충분하지 않은 회사 — 에서는 Cassandra의 운영 부담이 매우 크다. compaction tuning, JVM heap 관리, repair 운영, gossip protocol 디버깅이 모두 Cassandra 운영의 일이다. DynamoDB는 이 모든 걸 AWS가 책임지는 managed 서비스다.

대신 양보한 것도 있다. **DynamoDB는 cost가 throughput·storage 양쪽에 붙는다.** 트래픽이 급증하는 시점에는 on-demand 모드의 청구서가 무서워질 수 있다. 그리고 DynamoDB의 query 패턴은 매우 제한적이다 — partition key + sort key 조합으로만 빠른 query가 가능하고, secondary index(GSI/LSI)는 별도 비용과 별도 일관성 모델을 갖는다.

당근의 결정에서 우리가 배울 것은 단순하다 — **"운영 부담"이 의사결정의 정당한 한 축이 된다**는 점이다. 기술적으로 더 우월한 도구라도, 우리 팀이 감당할 수 없으면 도입할 자격이 없다. 0장에서 짚은 "도입의 자격" 다섯 물음 중 두 번째(우리 팀의 운영 역량)가 정확히 이 자리에서 작동한 사례다.

## 9. 비교 표 한 장 — Cassandra·DynamoDB·ScyllaDB

Dynamo 계열 안에서도 셋의 선택은 갈린다. Hello Interview의 NoSQL 비교 자료(W9)와 reference §2.4를 기반으로 한 페이지 표로 압축해 보자.

| 축 | Cassandra | DynamoDB | ScyllaDB |
|---|---|---|---|
| Hosting | self-managed (Apache 또는 DataStax) | AWS managed | self-managed 또는 ScyllaCloud |
| 언어 | Java (JVM GC 부담) | (AWS 비공개) | C++ (no GC, shard-per-core) |
| Wire protocol | CQL | proprietary API | CQL (Cassandra 호환) |
| 운영 부담 | 매우 높음 | 매우 낮음 | 중간 (Cassandra보다 적음) |
| 비용 모델 | 인프라 비용 | per-request + storage | 인프라 비용 또는 managed |
| 강점 | 성숙도, OSS 생태계 | 운영 부담 zero에 가까움 | 처리량·latency tail |
| 약점 | GC pause, 운영 인력 필요 | cost 예측 어려움, query 제약 | OSS 생태계 비교적 작음 |
| 어울리는 곳 | 대형 internal, 자체 인프라팀 | startup, AWS lock-in 수용 | high-throughput 채팅·게임·IoT |

이 표를 들고 회의 자리에 가면, 적어도 "왜 우리는 X를 골랐나"를 도메인 언어로 설명할 수 있다. 더 좋은 토론은 그 다음에 시작된다.

## 10. NoSQL 도입의 자격 — 다섯 물음 다시 보기

0장에서 우리는 도구 도입의 자격을 묻는 다섯 물음을 정리했다. NoSQL에 적용해 보자.

1. **이 도구를 안 쓰면 정말 못 푸는 문제가 있는가?** RDB의 read replica·partitioning·shard로 풀 수 있는 워크로드라면, NoSQL은 아직 자격이 없다. 정말 write throughput이 RDB의 한계를 넘는가, 정말 schema flexibility가 마이그레이션 비용보다 더 큰 가치인가.
2. **우리 팀의 운영 역량이 이 도구를 감당하는가?** Cassandra라면 JVM·repair·gossip·compaction의 운영을 누가 책임지는가. DynamoDB라면 cost forecasting과 GSI 설계의 한계를 우리 application이 받아들일 수 있는가.
3. **장애가 났을 때 누가 새벽에 일어나는가?** Cassandra 운영자가 1년 뒤에도 우리 회사에 있는가. DynamoDB의 throttling alert를 누가 첫 5분 안에 추적할 수 있는가.
4. **6개월 뒤 이 도구를 걷어낼 길이 있는가?** NoSQL은 데이터 모양이 query-first로 굳어 있어서, RDB로 되돌리는 비용이 매우 크다. 이 결정을 되돌릴 수 없다는 사실을 받아들이는가.
5. **이 결정을 우리 도메인 언어로 설명할 수 있는가?** "scalable해서"가 아니라 "우리 워크로드가 X 패턴을 가져서, partition key를 Y로 잡으면 hot이 안 날 가능성이 높다"고 말할 수 있는가.

이 다섯 물음에 자신 있는 답이 가능할 때, NoSQL을 도입할 자격이 생긴다. 그렇지 않다면, "Just use Postgres" — 1장의 휴리스틱 3이 여전히 정답일 가능성이 높다. RDB의 한계가 오기 전까지 우리가 알지 못하는 NoSQL 운영의 함정이 너무 많기 때문이다.

## 11. 흔히 듣는 오해 다섯 가지

회의 자리에서 자주 도는 오해 다섯 가지를 짚어 보자. 이 다섯 개 답이 손에 익으면, "Mongo 쓰자"는 한 마디에 자동으로 다섯 개의 질문이 떠오른다.

**오해 1: "NoSQL은 스키마가 없어서 schema migration이 없다."** — 틀린 말이다. application 레벨에서 schema가 살아 있고, 그 schema의 변화는 backfill 작업으로 나타난다. RDB의 ALTER TABLE이 안 보일 뿐, 그만큼의 일이 다른 layer에 옮겨 와 있다.

**오해 2: "NoSQL이 RDB보다 빠르다."** — 단일 row read는 그럴 수 있다. 그러나 복잡한 query(join, aggregation)는 거의 항상 RDB가 빠르거나, 아예 안 된다. RDB 인덱스가 잘 잡힌 read는 NoSQL을 가뿐히 이긴다.

**오해 3: "Cassandra가 항상 strong consistency보다 빠르다."** — quorum read(R + W > N)를 쓰면 Cassandra도 latency가 올라간다. eventual 모드일 때만 강점이 빛난다.

**오해 4: "DynamoDB는 매니지드라 운영이 zero다."** — partition key 설계·GSI 관리·cost forecasting·throttling 모니터링은 여전히 우리 일이다. infra 운영은 zero에 가까울 수 있지만, application 레벨의 운영은 그대로 남는다.

**오해 5: "NoSQL은 ACID가 안 된다."** — 더 이상 사실이 아니다. DynamoDB transactions, MongoDB multi-document transactions, Cassandra lightweight transactions가 모두 ACID 일부를 지원한다. 다만 비용이 따로 붙고, 사용 범위에 제한이 있다.

이 다섯 오해를 손에 익히는 것이 NoSQL을 다루는 시니어 백엔드가 되는 길이다. "Mongo가 빠르대"라는 한 마디에 회의 자리에서 멈칫하지 않고 한 박자 깊은 질문을 돌려줄 수 있게 된다.

## 12. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 두 갈래의 지형이 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **두 갈래의 결정 트리.** Dynamo 계열(AP, leaderless, eventual)과 Bigtable 계열(CP, single-leader per tablet, strong). 우리 워크로드가 strong consistency를 어디까지 필요로 하는지가 결정한다.
- **query-first.** 데이터 모델링이 사라진 게 아니라, query를 먼저 정하고 그 모양대로 비정규화해서 박는 일이다.
- **Hot partition은 평생의 적이다.** partition key 첫 줄을 보면 거의 직감적으로 "이거 hot 가능성 있다"고 느끼는 게 시니어의 감각이다. alert에 shard별 QPS skew 한 줄만 더 박아 두자 — 그게 새벽 3시의 자신을 살린다. 응급 처치는 jitter·request coalescing·재설계 3단계.
- **LSM-tree가 write-heavy의 근거다.** 그 대가는 read amplification·tombstone·bloom filter false positive. 부록 A의 tribal 7번·16번 항목으로 다시 만난다.
- **Discord가 보여준 통찰** — DB 자체를 바꾸는 것보다 앞에 request coalescing 한 줄을 잘 짜는 게 더 효과적일 수 있다. 30,000번을 1번으로 합치는 사고는 NoSQL 운영의 보편 도구다.
- **당근이 보여준 통찰** — "운영 부담"은 의사결정의 정당한 한 축이다. 기술적으로 우월한 도구라도 우리 팀이 감당 못하면 자격이 없다.

다음 장에서는 캐시를 짚는다. NoSQL과 캐시는 사실 같은 가족에 가깝다 — 둘 다 RDB의 부담을 다른 layer로 옮겨 빠르게 만든다는 점에서. 그런데 캐시는 NoSQL과는 다른 종류의 잔인함을 품고 있다. 캐시를 한 번이라도 비워본 적이 있다면, 그날 DB가 무사했는지 한 번 떠올려 보자. 그게 3장의 시작이다.


---

# 3장. 캐시 — 거의 모든 시스템의 첫 번째 latency 무기

production Redis를 한 번이라도 `FLUSHDB` 해본 적이 있다면, 그 다음 1분 동안 무슨 일이 벌어졌는지 생생하게 떠오를 것이다. DB CPU가 100%를 찍고, p99 latency가 30초로 솟구치고, 알람이 도미노처럼 울린다. 그 와중에 누군가 사색이 된 얼굴로 "혹시 캐시 비웠어요?"라고 묻는다. 우리는 한참 뒤에야 "네"라고 답하고, 그 뒤로 한 시간쯤 회의실에서 무언가를 적게 된다.

캐시는 무기다. 같은 쿼리를 1000번 다시 묻지 않게 해주고, DB와 origin(원본 서비스)이 평소의 1/10 부하로 살게 해준다. 그런데 그 무기를 잘못 잡으면 우리 손에서 폭발한다. 캐시 하나를 비웠다는 단 한 줄의 작업이, 1분 안에 전체 서비스를 멈춰 세울 수 있다. 이 양면성이 캐시라는 부품을 흥미롭게 만든다.

그래서 캐시는 두 모양을 한꺼번에 머릿속에 그려야 다룰 수 있는 부품이다. 한쪽은 **잘 작동할 때의 모양** — 어떤 위치에 어떤 패턴으로 두면 latency가 얼마나 줄어드는지. 다른 한쪽은 **망가질 때의 모양** — thundering herd, cache stampede, 일관성 깨짐 같은 사고가 어떻게 cascading failure로 번지는지. 그 두 모양이 같이 떠올라야 비로소 캐시를 두려움 없이 잡을 수 있다.

## 캐시의 위치 — origin부터 client까지 6단

캐시가 어디에 있느냐는 질문에 대한 가장 흔한 답은 "Redis"다. 그런데 사실 그건 분산 캐시 한 종류일 뿐이고, 시스템 안에는 origin에서 client까지 가는 길에 캐시가 무려 여섯 군데쯤 깔려 있다. 이 6단 지형도를 한 번 그려 보자.

| 단 | 위치 | 대표 도구 | 평균 latency | 보호 대상 |
|----|------|----------|------------|----------|
| 1 | DB internal cache | Postgres buffer pool, MySQL InnoDB buffer pool | 1~10μs | disk IO |
| 2 | App in-process cache | Caffeine, Guava (Java), `lru-cache` (Node) | 100ns~1μs | DB query |
| 3 | 분산 캐시 | Redis, Memcached | 200μs~2ms | DB, upstream service |
| 4 | Reverse proxy cache | NGINX, Varnish | 1~5ms | app server |
| 5 | CDN edge cache | Cloudflare, CloudFront, Akamai | 5~50ms | origin (전 세계 분산) |
| 6 | Client cache | browser HTTP cache, mobile local DB | 0ms (네트워크 자체 안 탐) | 모든 backend |

이 6단을 한 번에 다 깔라는 얘기는 아니다. 시스템마다 어디까지 필요한지가 다르다. 사내 admin 도구는 1·2단만으로 충분하고, B2B SaaS는 보통 1·2·3단까지 깐다. B2C 글로벌 서비스는 4·5·6단까지 다 깔린다. 그런데 어느 단을 깔든 한 가지 원칙은 공통이다 — **caching closer to the user is always cheaper**. 사용자에 가까울수록 적은 자원으로 큰 latency 단축이 일어난다.

그래서 이 책에서 가장 깊이 짚을 단은 2단과 3단이다. CDN(5단)은 7장에서 따로 다루고, DB buffer pool(1단)은 1장에서 이미 잠깐 만났다. 우리가 매일 코드를 짤 때 가장 직접 손대는 두 단이 2단과 3단이고, 사고도 그 두 단에서 가장 자주 난다.

## Cache-aside vs read-through vs write-through vs write-back — 4가지 패턴

캐시와 origin 사이의 데이터 흐름을 어떻게 묶느냐에 따라 4가지 표준 패턴이 갈린다. AWS Caching Whitepaper가 가장 깔끔하게 정리한다.

> A cache-aside cache is updated after the data is requested. A read-through cache updates itself. (AWS, *Database Caching Strategies Using Redis*)

이 한 줄 안에 핵심 차이가 다 들어 있다. 한 번씩 짚어 보자.

### 패턴 1. Cache-aside (가장 흔한 default)

app이 직접 캐시를 들고 있는 가장 단순한 모양이다.

```
read:
  data = cache.get(key)
  if data is None:
      data = db.query(key)
      cache.set(key, data, ttl=300)
  return data

write:
  db.update(key, value)
  cache.delete(key)  # 또는 cache.set(key, value)
```

읽을 때는 캐시를 먼저 보고, 없으면 DB에서 채워 캐시에 박는다. 쓸 때는 DB를 먼저 쓰고, 캐시는 invalidate(삭제) 또는 update한다. 이 모양이 가장 흔한 이유는 단순하기 때문이다. app만 알면 되고, 캐시 layer는 그냥 멍청한 key-value store로 두면 된다.

대신 두 가지 함정이 있다. **첫째, cache miss 시점에 DB로 부하가 몰린다.** 캐시가 없으면 모든 read가 DB로 간다. 둘째, **write 시점에 캐시와 DB 사이의 일관성이 깨질 수 있다.** DB는 업데이트됐는데 캐시 invalidate가 실패하면? 또는 그 사이 다른 요청이 옛 값을 캐시에 다시 박으면? 이 경계의 모양을 그려 두는 게 중요하다.

### 패턴 2. Read-through (캐시가 origin을 알고 있다)

```
read:
  return cache.get_or_load(key, loader=lambda: db.query(key))
```

캐시 자체가 loader 함수를 알고 있어서, miss가 나면 알아서 origin에서 채워 온다. 코드가 더 깔끔하지만, 캐시 layer가 origin에 대한 의존성을 직접 갖는 단점이 있다. AWS DAX(DynamoDB Accelerator), 일부 Hibernate L2 cache 구현이 이 모양이다.

### 패턴 3. Write-through (쓸 때마다 캐시도 같이)

```
write:
  cache.set(key, value)
  db.update(key, value)
```

쓸 때 캐시와 DB를 같이 쓴다. 일관성은 좋아지지만, **write가 두 군데로 가니 write latency가 늘고, 절대 안 읽힐 값까지 캐시에 쓴다.** read-heavy + write-light + 일관성 중요 시스템에 적합하다.

### 패턴 4. Write-back / Write-behind (쓸 때는 캐시만, 나중에 DB)

```
write:
  cache.set(key, value, dirty=True)
  # background worker가 일정 주기로 DB에 sync
```

write latency가 가장 짧다. 그런데 dirty data가 캐시에 있을 때 캐시 노드가 죽으면 **데이터가 사라진다.** Redis cluster의 일부 운영 모드가 이 모양을 흉내내지만, 진짜 write-back은 좀처럼 안 쓴다. 너무 위험하다.

> 💡 이 4가지 패턴을 한 줄로 요약하면 이렇다.
> - Cache-aside = 일반적, 단순, 일관성은 약함
> - Read-through = 코드 깔끔, 캐시 layer가 origin 알아야 함
> - Write-through = 일관성 좋음, write 비쌈
> - Write-back = write 빠름, 데이터 손실 위험
>
> 처음 시스템 짤 때는 거의 cache-aside로 시작하고, 일관성이 절박해질 때만 write-through로 옮기는 편이 낫다.

## Redis vs Memcached — 무엇을 어떻게 가르나

분산 캐시 후보로 가장 자주 거론되는 둘이 Redis와 Memcached다. "Redis"라고 답하는 사람이 90%이지만, Memcached도 여전히 유효한 도구다. 두 선택지의 trade-off를 한 표로 정리하자.

| 차원 | Redis | Memcached |
|------|-------|-----------|
| 자료구조 | string, hash, list, set, sorted set, stream, bitmap, geo | string only |
| persistence | RDB snapshot + AOF (선택) | 없음 (in-memory only) |
| eviction | allkeys-lru, allkeys-lfu, volatile-lru, allkeys-random, ... 6개 정책 | LRU only |
| replication | primary-replica, Cluster mode (sharding 내장) | 없음 (client-side sharding) |
| persistence 옵션 | RDB + AOF, durable cache 가능 | 순수 cache |
| 성능 (단일 노드) | 매우 빠름, 자료구조 op 풍부 | 더 빠름 (단순함) |
| 메모리 효율 | overhead 있음 | 효율 좋음 |
| pub/sub, scripting | Lua scripting, pub/sub, transaction | 없음 |
| 분산 lock, rate limit | Redlock(논쟁), counter, ... 도구로 활용 가능 | 어려움 |

이 표를 보면 두 도구의 위치가 자연스럽게 드러난다. **Memcached는 "순수 캐시"이고, Redis는 "캐시이자 자료구조 서버"다.** 한 줄 캐시만 필요하면 Memcached가 더 빠르고 메모리도 적게 쓴다. 하지만 sorted set으로 leaderboard를 만들거나, list로 작업 큐를 흉내내거나, pub/sub으로 가벼운 메시징을 하거나, Lua로 atomic operation을 짜야 한다면 Redis로 가는 편이 낫다.

한국 백엔드에서는 거의 Redis가 표준이다. 데이터 구조의 풍부함, persistence option, Sentinel·Cluster의 운영 성숙도, 한국 운영 도구·문서의 양 등 이유는 많다. 새 시스템이라면 일단 Redis로 시작해서, 메모리 효율이 정말 부족할 때만 Memcached 검토하는 편이 낫다.

> 한 가지 주의 사항. Redis는 **single-threaded**다. (정확히는 background thread가 일부 있지만, command 실행은 한 스레드.) 그래서 `KEYS *`, `SMEMBERS bigset` 같은 O(N) 명령은 1초 이상 걸릴 수 있고, 그동안 다른 모든 요청이 막힌다. production에서 `KEYS`를 치지 말자 — 이 한 가지 규칙만으로 한국 백엔드에서 흔한 Redis 사고의 절반을 막을 수 있다. 대신 `SCAN`을 쓰자.

## Cache stampede — 같은 키를 1000개의 요청이 동시에 미스할 때

이제 가장 자주 망가지는 모양을 보자. **cache stampede** 또는 **thundering herd**라 부르는 현상이다. 영어로는 "성난 떼"라는 뜻인데, 한 번 겪어 보면 그 이름이 왜 붙었는지 절감하게 된다.

상황을 가정해 보자. 우리 서비스에 "지금 인기 상품 Top 10"이라는 캐시 키가 있다고 하자. 5분마다 갱신되도록 TTL이 300초로 박혀 있다. 1초에 1000개 요청이 이 캐시를 본다. 평소에는 1000개 모두 캐시 hit으로 끝나서, DB로 가는 부담은 거의 0이다.

그런데 0초에 캐시가 만료되는 순간 무슨 일이 벌어질까? 1초에 1000개 요청이 동시에 캐시 miss를 받는다. 1000개 요청이 모두 DB에 같은 쿼리를 던진다. DB는 평소 1초에 0~1개 받던 쿼리를 1000개 받는다. 첫 번째 요청이 결과를 받아와 캐시에 박을 때까지 다른 999개도 같은 쿼리를 처리하느라 DB는 CPU 100%로 비명을 지른다.

이게 thundering herd다. 그리고 단 한 키가 아니라 **여러 인기 키가 비슷한 시각에 동시 만료**되는 패턴이 가장 끔찍하다. 카카오 if(kakao) 2021 발표(검증 필요)에서 비슷한 결의 회고가 등장한다 — "single key TTL 동시 만료가 가장 무섭다"는 결. 새벽 0시·1시·5분 정각처럼 의외로 한국 백엔드의 일상 어디에든 깔려 있는 자리다.

같은 결의 사고가 한 가지 더 있다. **cache flush 직후의 cold cache(차가워진 캐시 — 데이터가 비어 있는 상태).** 운영자가 디버깅 중에 `FLUSHDB`나 `FLUSHALL`을 친 직후, 모든 키가 한 번에 사라진다. 그 다음 1분 동안 모든 요청이 cache miss로 origin에 직격탄을 날린다. Cloudflare 사내 블로그의 한 일화가 그대로다 — "We cleared our Redis to fix a bug and brought down origin for 20 minutes."

그렇다면 어떻게 막을까? 세 가지 패턴이 한국·해외 백엔드에서 정착되어 있다.

### 방어 1. Jittered TTL — 만료 시각을 랜덤으로 흩어 놓는다

가장 단순한 방어다. TTL을 그냥 300초로 박지 말고, "300초 + 0~60초 사이 랜덤"으로 박는다.

```python
import random

def set_with_jitter(cache, key, value, base_ttl=300, jitter=60):
    ttl = base_ttl + random.randint(0, jitter)
    cache.set(key, value, ttl=ttl)
```

이 한 줄이 모든 키의 만료 시각을 한 번에 몰리지 않게 흩어 놓는다. 우아한형제들이 배민 캐시 운영에서 "jittered TTL + lazy refresh"를 정착시킨 이유가 이거다. 가장 쉽고 효과가 큰 1차 방어선이다.

### 방어 2. Singleflight / Request Coalescing — 같은 키 요청을 하나로 합친다

같은 키에 대해 동시에 들어온 요청들을 한 번의 origin 호출로 묶는 패턴이다. Go의 `golang.org/x/sync/singleflight`이 표준 구현이다.

```go
var group singleflight.Group

func GetTopProducts(ctx context.Context) ([]Product, error) {
    v, err, _ := group.Do("top-products", func() (any, error) {
        // 이 함수는 같은 키에 대해 동시에 한 번만 실행됨
        return db.QueryTopProducts(ctx)
    })
    if err != nil { return nil, err }
    return v.([]Product), nil
}
```

캐시가 miss 났을 때, 100개의 요청이 모두 같은 key의 loader를 호출하더라도 group이 한 번만 실행하고 나머지는 그 결과를 공유한다. Java 진영에서는 Caffeine의 `LoadingCache.get(key, loader)`이 기본으로 이 모양을 보장한다. Discord의 chat 메시지 캐싱에서도 같은 패턴이 쓰인다 — request coalescing.

### 방어 3. Probabilistic Early Expiration — 만료 전에 미리 갱신한다

Vasilis Vasilakos의 2015년 논문 "Optimal Probabilistic Cache Stampede Prevention"이 제안한 우아한 방법이다. 핵심 아이디어는 이렇다.

> 만료에 가까워질수록 확률적으로 미리 갱신해 두면, 동시 만료가 일어날 확률이 거의 0이 된다.

수식으로는 이렇다. expiry time `t_e`, 현재 시각 `t_now`, 갱신에 걸리는 시간(beta로 표현)을 알 때, 다음 조건이 참이면 갱신한다.

```
delta * beta * ln(random()) >= t_e - t_now
```

복잡해 보이지만, 직관은 단순하다. "만료 직전에 가까울수록, 확률적으로 누군가 한 명이 미리 갱신하게 만든다." 모든 요청이 정확히 만료 시각에 동시에 miss를 받지 않게 흩어 놓는다.

Redis 자체적으로 이걸 해주진 않지만, app 단에서 한 줄 추가로 구현할 수 있다. 한국 백엔드에서는 토스·우아한형제들이 이 패턴을 일부 hot key에 적용한다는 사례가 발표에 등장한다.

### 방어 정리 — 어느 방어선부터 깔까

세 방어선 중 어느 것부터 깔아야 하는가? 보통 다음 순서가 합리적이다.

1. **jittered TTL을 모든 캐시에 default로 깔자.** 한 줄짜리 코드 변경으로 가장 큰 효과.
2. **hot key 또는 long-running loader가 있는 곳에 singleflight를 추가하자.** request coalescing 효과가 크다.
3. **만료 패턴이 정말 critical하다면 probabilistic early expiration까지 검토하자.** 코드 복잡도가 늘지만 가장 견고하다.

이 셋을 다 깔아도 막을 수 없는 사고가 하나 더 있다. cache layer 자체가 멈출 때. Redis primary가 죽거나 Cluster의 한 shard가 split-brain에 빠지면, 그 사이 모든 요청이 origin으로 직격탄을 날린다. 이 경우엔 캐시 패턴이 아니라 **circuit breaker**가 답이다 — 캐시가 일정 시간 응답이 없으면 origin 호출 자체를 차단해 cascade를 막는다. 이 패턴은 10장 멱등성·재시도·서킷 브레이커 챕터에서 자세히 다룬다.

## Eviction — 메모리가 가득 찰 때 무엇을 버릴 것인가

캐시는 본질적으로 **유한한 메모리**다. 새 데이터를 넣으려면 옛 데이터를 버려야 한다. 어느 키를 버릴지 결정하는 정책이 eviction이다. Redis는 6가지 정책을 제공하는데, 자주 헷갈리니 한 번 정리하자.

| 정책 | 무엇을 버리는가 | 언제 쓰나 |
|------|----------------|---------|
| `noeviction` | 안 버림, write 실패 시킴 | 캐시가 손실되면 데이터 자체가 사라지는 경우 (사실상 storage 용도) |
| `allkeys-lru` | 모든 키 중 가장 안 쓰인(LRU) 것 | 일반 캐시. 가장 무난한 default |
| `allkeys-lfu` | 모든 키 중 가장 적게 쓰인(LFU) 것 | 일부 키만 극단적으로 hot한 access 패턴 |
| `allkeys-random` | 무작위 | 모든 키가 거의 균등하게 쓰일 때 |
| `volatile-lru` | TTL 있는 키 중 LRU | TTL 없는 키는 절대 안 버려야 할 때 |
| `volatile-ttl` | TTL이 가장 빨리 만료되는 키 | 만료가 의미 있는 데이터일 때 |

가장 무난한 default는 `allkeys-lru`다. 대부분의 access 패턴은 "최근에 쓴 게 곧 또 쓰일" 가능성이 높다는 LRU 가정에 부합한다. 그런데 access 패턴이 명확히 다르면 LFU가 더 좋을 수 있다. 예를 들어 인기 상품 Top 100 같은 키는 매우 자주 쓰이는데, 잠깐 안 쓰였다고 LRU로 밀려나면 다음 access에서 cache miss가 난다. 이런 경우 LFU가 적합하다.

`noeviction`을 default로 두면 끔찍한 일이 일어난다. Redis가 메모리 한계에 도달하면 모든 write가 OOM 에러로 실패한다. session·rate-limit·queue를 Redis로 쓰는 시스템이라면, 어느 날 갑자기 로그인이 안 되고 API가 5xx로 떨어지는 사고가 날 수 있다. 그래서 `maxmemory-policy`는 항상 `allkeys-lru` 또는 `allkeys-lfu`로 시작하는 편이 낫다.

> 💡 운영 팁 — Redis 메모리는 80%를 임계치로 잡자. `maxmemory`를 instance 메모리의 75~80%로 설정하고, 90%를 넘으면 alert을 띄우자. Redis가 메모리 한계에 가까워지면 fragmentation·eviction·persistence가 모두 느려져 latency가 폭증한다.

## Multi-tier cache — L1 in-process + L2 분산

큰 시스템이 되면 분산 캐시(L2) 위에 in-process 캐시(L1)를 한 단 더 깔게 된다. L1은 app 프로세스 안의 메모리고, L2는 Redis다.

```
read:
  data = local_cache.get(key)
  if data is None:
      data = redis.get(key)
      if data is None:
          data = db.query(key)
          redis.set(key, data, ttl=300)
      local_cache.set(key, data, ttl=10)  # 짧게
  return data
```

L1 hit이면 1μs 이내, L2 hit이면 1ms, miss면 100ms+ — 이런 3단 계층이 만들어진다. Java에서는 **Caffeine**이 표준이고, Node에서는 `lru-cache`나 `lru-cache-fp`가 흔하다. Caffeine은 W-TinyLFU 알고리즘으로 LRU보다 hit rate가 높은 것으로 알려져 있다.

L1 캐시의 장점은 두 가지다. **첫째, 가장 빠르다.** Redis는 네트워크 호출이 끼지만 L1은 같은 프로세스 메모리다. 둘째, **Redis 트래픽을 줄여 비용·부하를 낮춘다.** Redis가 1초에 100만 op을 처리한다면, 그 절반을 L1이 흡수해 주는 식이다.

대신 단점도 있다. **일관성이 어려워진다.** Redis는 한 곳이라 invalidate가 정확하지만, L1은 모든 app instance에 다 있다. 한 사용자가 자기 데이터를 수정했는데, 다른 instance의 L1 캐시에는 옛 값이 5~10초 동안 남아 있을 수 있다. 그래서 L1은 **TTL을 매우 짧게(보통 5~30초)** 잡거나, **거의 안 변하는 데이터(설정, lookup 테이블)에만** 쓰는 편이 낫다. 또는 분산 invalidation pub/sub을 깔아 한 instance가 update 시 모든 instance에 invalidate를 broadcast하는 패턴도 있는데 — 일관성 절에서 다시 만난다(Facebook TAO의 두 단계 invalidation). 다만 복잡도가 빠르게 늘어, 신중하게 짚어 보는 편이 낫다.

## 한국 사례 — 카카오·우아한형제들의 캐시 운영 패턴

해외 사례만 봐서는 우리 일상이 잘 안 보인다. 한국 백엔드의 두 가지 대표 발표를 짚어 보자.

### 카카오 if(kakao) 2021 — "트래픽 폭증과 캐시 정책"

카카오톡은 새해·설날·발렌타인데이·어버이날 같은 정기 이벤트에서 평소의 수십 배 트래픽을 받는다. 광고는 점심·퇴근 시간에 spike가 친다. 그러니 캐시 정책의 모양이 매일이 다르다.

발표의 핵심 메시지 중 하나는 "single key TTL 동시 만료가 가장 무서웠다"였다. 단일 hot key가 만료되는 순간 thundering herd가 터지는 패턴을 여러 차례 겪었고, jittered TTL + 일부 hot key는 background refresh로 갱신하는 형태로 정착시켰다. 그리고 한 가지 더 — 캐시 클러스터를 **트래픽 유형별로 분리**해 두었다. 광고 캐시가 폭증해도 메시지 캐시는 영향 받지 않게.

### 우아한형제들 — 배민 캐시 운영 전략

배민 techblog과 우아콘에서 여러 번 다뤄진 패턴이다. 핵심을 한 줄로 줄이면 "hot key는 lazy refresh + jittered TTL"이다.

```java
@Cacheable(value = "popularStores", key = "#regionId")
public List<Store> getPopularStores(Long regionId) {
    // ...
}

// 별도 스케줄러가 만료 직전에 미리 갱신
@Scheduled(fixedDelay = 30000)
public void refreshPopularStores() {
    for (Long regionId : getActiveRegions()) {
        cache.put("popularStores::" + regionId, query(regionId));
    }
}
```

기본 캐시는 TTL 5분 + jitter, 그리고 인기 keys는 별도 스케줄러가 매 30초 background refresh를 돌린다. 사용자 요청은 항상 hit하고, 갱신은 보이지 않는 곳에서 일어난다.

이 패턴이 가능한 이유는 **"인기 keys"가 미리 알려져 있기 때문**이다. 모든 keys를 백그라운드로 갱신할 수는 없다. hit rate 분석 도구로 상위 N개를 골라 그 키들만 별도 워크플로로 묶는다. 이런 운영 관점의 디테일이 발표에서 강조되는 이유다.

## Callback 예고 — 17장 피드 시스템의 fanout cache

캐시는 17장 피드·타임라인 챕터에서 다시 만난다. Twitter·Instagram이 fanout-on-write로 home timeline을 만들 때, 각 사용자의 timeline 자체가 Redis 안의 sorted set으로 캐시된다. follower가 1만 명인 셀럽 한 명의 트윗 한 개가 만 개의 cache write를 만든다. 이 패턴을 "fanout cache"라 부르며, 단순 read-cache와는 다른 의사결정이 필요하다.

그 챕터에서는 어떤 key를 어떤 size로 어떻게 TTL 박는지, 셀럽 예외(fanout-on-read)는 어떻게 가르는지를 깊게 본다. 지금 챕터에서 배운 패턴(jittered TTL, singleflight, eviction)이 그 위에 그대로 얹힌다. **빌딩 블록이 곧 패턴의 재료가 된다는 사실**이 책 전체를 통해 반복되는 메시지다.

## 일관성 — "캐시는 결국 stale data를 견디는 layer다"

캐시를 깐다는 결정은 곧 **"일관성을 일부 양보하겠다"는 결정**이다. DB에 새 값이 쓰였는데 캐시는 아직 옛 값을 들고 있을 수 있다. 이 시차를 얼마나 견딜 수 있느냐가 캐시 도입 자격의 첫 번째 질문이다.

가장 흔한 패턴은 TTL 기반이다. "5분이면 stale data가 사라진다"는 약속으로 일관성을 흉내낸다. 90%의 도메인은 5분 stale을 견딜 수 있다. 인기 상품 목록, 카테고리, 메뉴 — 이런 데이터는 5분 늦어도 큰 문제가 없다.

그런데 견딜 수 없는 도메인이 있다. **결제 정보, 잔고, 권한, 재고**. 이런 데이터를 캐시한다는 결정은 매우 신중해야 한다. 잔고가 stale이면 사용자가 이미 다 쓴 돈을 또 쓸 수 있다. 권한이 stale이면 해고된 사용자가 한동안 접근 가능하다. 재고가 stale이면 0개 남은 상품을 100명에게 팔게 된다. 끔찍한 일이다.

이 경우 두 가지 선택지가 있다. **첫째, 캐시 자체를 깔지 않는다.** 잔고는 매번 DB에서 읽는다. 둘째, **invalidation을 강력하게 한다.** write 시 캐시를 동기로 invalidate하고, 캐시 invalidate가 실패하면 write도 롤백한다. 그러면 결국 캐시 layer가 critical path에 들어와, 캐시 장애가 곧 service 장애가 된다. 이 trade-off를 짊어질 만한 도메인이라면 그렇게 하는 편이 낫고, 아니라면 차라리 캐시를 안 까는 편이 낫다.

그리고 한 가지 더 — **"두 단계 invalidation"** 패턴이 있다. Facebook의 TAO 시스템이 정착시킨 패턴인데, write는 두 단계로 처리한다. (1) DB에 쓰고, (2) Kafka에 invalidate 이벤트를 발행한다. invalidate consumer가 모든 캐시 instance(L1·L2)에서 그 키를 지운다. 이렇게 하면 일관성이 좀 더 강해지지만, 캐시 invalidation의 latency가 늘고 시스템 복잡도가 커진다. 한국에서는 카카오 일부 광고 시스템, 네이버 일부 추천 시스템이 비슷한 패턴을 쓴다고 알려져 있다.

이 모든 trade-off의 결론은 한 가지다 — **"이 데이터를 캐시할 자격이 있는가"를 도메인별로 묻는 습관을 기르자.** 모든 데이터를 default로 캐시하면 빠르긴 하지만, 어느 날 stale data가 사고로 번진다. 도메인별로 stale 허용 시간을 미리 정해 두는 편이 낫다.

## 운영 모니터링 — 캐시 대시보드 7가지

마지막으로, 캐시를 production에서 운영하는 동안 항상 띄워두면 좋은 지표 7가지를 정리하자.

| # | 지표 | 의미 | 위험 임계 |
|---|------|------|----------|
| 1 | hit ratio (hits / (hits + misses)) | 캐시 효용 | 90% 미만이면 패턴 재검토 |
| 2 | latency p50·p99 | 캐시 응답 분포 | p99가 p50의 10배 이상이면 slow command 의심 |
| 3 | memory usage (%) | 메모리 압박 | 80% 넘으면 ramp-up 검토 |
| 4 | evictions / sec | 메모리 부족으로 강제 만료 | 0이 정상, 0보다 크면 의심 |
| 5 | network bandwidth | I/O 포화 | 80% 넘으면 의심 |
| 6 | connected_clients | 연결 수 | 비정상 증가 시 connection leak 의심 |
| 7 | slow log count | O(N) 명령 발생 | 0 외에 한 건이라도 보이면 즉시 확인 |

이 7가지를 한 화면에 띄워 두면, 새벽에 alert가 울려도 어느 지표를 가장 먼저 봐야 하는지가 명확해진다. 특히 **hit ratio**는 캐시 전체의 건강 척도다. hit ratio가 평소 95%였는데 갑자기 70%로 떨어졌다면, 누군가 캐시를 비웠거나, 캐시 layer가 부분 장애 상태이거나, 또는 access 패턴이 바뀐 것이다. 어느 쪽이든 즉각적인 조사가 필요하다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 캐시라는 무기의 양면이 손에 잡혀 있다. 4가지 패턴(cache-aside·read-through·write-through·write-back), Redis와 Memcached의 갈림, eviction 정책, multi-tier 계층, 그리고 망가질 때의 모양 — thundering herd·cold cache·stale data. 한국 백엔드의 카카오·우아한형제들 발표에서 정착된 jittered TTL + lazy refresh + 트래픽 격리 패턴까지가 한 묶음이다.

기억해두자. 캐시는 가장 흔하게 깔지만, 가장 자주 우리를 배신하는 부품이다. "왜 캐시를 깔까"보다 "캐시를 까는 자격이 우리 도메인에 있는가"를 먼저 묻는 편이 낫다. 그리고 한 번 깔았다면, 잘 작동할 때의 모양만큼 망가질 때의 모양도 머릿속에 그려두자. 새벽 한 시에 그 그림이 우리를 살린다. 그리고 그 그림이 머릿속에 자동으로 펼쳐질 때, 우리는 "캐시를 안다"고 말할 자격이 있는 백엔드 개발자가 되어 있다.

다음 장에서는 캐시와 함께 비동기 시스템의 양대 부품인 메시지 큐를 살펴본다. Kafka·RabbitMQ·SQS의 trade-off를 한 장의 표로 그리는 작업, 그리고 "lag가 4시간"이라는 sound조차 낯설지 않게 만드는 운영 함정들을 짚어 보자. 그곳에서도 우리는 같은 질문을 마주하게 된다 — "이 부품을 도입할 자격이 우리 팀에 있는가."

---

# 4장. 메시지 큐 — 비동기와 decoupling의 토대

오전 9시, 슬랙에 "큐 lag 4시간"이라는 메시지가 떴다고 해보자. 누가 봐도 1주일 전 배포가 원인 같다. 그런데 이상하게 누구도 처음엔 그 배포를 의심하지 않는다. 어제까지 멀쩡했으니까. 메트릭 대시보드를 펴 보니 그제부터 consumer lag이 조금씩 쌓이기 시작해서, 지난 새벽에 갑자기 직선으로 솟구쳐 있다.

큐는 조용히 망가진다. DB가 느려지면 latency 알람이 즉시 뜨고, 캐시가 비면 origin이 비명을 지른다. 그런데 큐는 다르다 — producer는 멀쩡히 send에 성공하고, broker도 조용히 메시지를 받아 쌓는다. 망가지는 곳은 consumer이고, 망가지는 모양은 "쌓이는 메시지의 모양"이다. 큐 모니터링이 없으면 우리는 그 모양을 볼 수 없다. 그게 큐를 가장 무서운 부품으로 만든다.

그래서 큐는 두 모양을 같이 머릿속에 그려야 다룰 수 있는 부품이다. **잘 작동할 때** — Kafka·RabbitMQ·SQS가 무엇을 약속하고 무엇을 양보하는지. **망가질 때** — consumer lag, rebalance storm, retention loss, exactly-once의 진실. 도입 자격을 묻는 6가지 질문이 마지막에 손에 잡힌다면, 큐를 잡는 두려움이 한 단계 가벼워진다.

## 큐를 도입한다는 결정은 무엇을 양보하는 결정인가

큐는 두 service를 비동기로 갈라 놓는다. producer는 send만 하고 끝낸다. consumer는 자기 속도로 받아서 처리한다. 이 한 줄짜리 구조 변경이 시스템에 가져오는 효과는 크게 네 가지다.

**1. 시간 디커플링.** producer가 보내는 시점과 consumer가 받는 시점이 분리된다. consumer가 잠시 죽어도 큐에 메시지가 쌓여 있어 producer는 영향이 없다.

**2. 부하 평탄화 (load smoothing).** 짧은 burst를 큐가 흡수하고, consumer는 평균 속도로 처리한다. 카카오의 0시 트래픽, 토스의 새벽 이자 정산 같은 burst 패턴이 큐 없이는 견디기 어렵다.

**3. 디커플링.** producer는 누가 메시지를 받는지 모른다. 새 consumer를 추가해도 producer 코드는 안 바뀐다. event-driven 아키텍처의 토대다.

**4. retry·재처리 가능성.** 메시지가 큐에 저장되어 있으니, 실패한 consumer가 재시도하거나, 새 버전의 consumer가 옛 메시지를 다시 처리할 수 있다.

이 네 효과가 정말 매력적이라서, 많은 팀이 큐를 default로 깐다. 그런데 큐를 깐다는 결정은 거꾸로 보면 **양보**의 결정이기도 하다. 무엇을 양보하는가?

**1. 즉시 응답을 양보한다.** "보냈다"는 producer의 약속이고, "정말 처리됐다"는 약속이 아니다. 결제 confirm 같은 sync 응답이 필요한 도메인은 큐로 갈 수 없다.

**2. 일관성을 양보한다.** producer가 DB에 commit하고 큐에 메시지를 보내는 사이에 시스템이 죽으면, DB만 변하고 메시지는 안 보내진 상태가 된다. 그 반대도 가능하다. 이 dual-write 문제를 어떻게 푸는가가 11장 Saga·Outbox 챕터의 핵심이다.

**3. 디버깅 가시성을 양보한다.** sync 호출이면 stack trace 한 번으로 누가 뭘 보냈는지 보인다. 큐는 producer와 consumer의 trace가 따로 떠다닌다. distributed tracing(W3C trace context) 없이는 디버깅이 끔찍해진다.

**4. 운영 부담을 추가한다.** broker 자체를 운영해야 한다. 모니터링, 백업, upgrade, partition rebalance — 새로운 종류의 새벽 alert가 추가된다.

그래서 큐 도입은 "필요한가"를 먼저 묻는 편이 낫다. 큐 없이 sync API로 충분히 풀리는 도메인에 굳이 큐를 깔면, 운영 부담만 늘고 새 종류의 사고가 생긴다. **"큐의 4가지 효과 중 우리에게 정말 필요한 게 무엇인가"를 자기 도메인 언어로 답할 수 있어야 도입 자격이 생긴다.**

## Kafka vs RabbitMQ vs SQS vs Pulsar — 어디가 어떻게 다른가

큐 선택지로 가장 자주 거론되는 4가지를 한 표로 정리하자. 한국 백엔드에서는 Kafka와 RabbitMQ가 가장 흔하고, AWS 친화 팀은 SQS를 쓰고, Pulsar는 채택률이 낮지만 일부 팀이 검토한다.

| 차원 | Kafka | RabbitMQ | SQS (AWS) | Pulsar |
|------|-------|----------|-----------|--------|
| 기본 모델 | log + partition + offset | exchange + queue + routing key | distributed queue | log + tiered storage |
| 메시지 소비 후 | retention 동안 유지 (default 7일) | ack 시 삭제 | ack 시 삭제 (visibility timeout) | retention 동안 유지 |
| ordering | partition 내 순서 보장 | FIFO 큐만 보장 | FIFO 큐 또는 standard | partition 내 |
| throughput | 매우 높음 (~10만 msg/sec/partition) | 중간 (~1만/sec) | 무제한 (manage) | 매우 높음 |
| replay 가능 | 됨 (retention 안에서) | 안 됨 (소비 후 삭제) | 안 됨 | 됨 |
| consumer model | consumer group, pull | push 또는 pull | poll only | consumer group |
| 운영 모델 | 자체 cluster 또는 managed (MSK·Confluent) | 자체 cluster | 완전 managed | 자체 cluster |
| 학습 곡선 | 가파름 | 완만 | 매우 완만 | 가파름 |
| 가장 강한 곳 | event streaming, 데이터 파이프라인, 높은 throughput | RPC-like 비동기, 복잡한 routing | AWS 단일 region 비동기 | tiered storage, multi-tenancy |

이 표를 보면 두 모델이 갈린다. Kafka·Pulsar는 **"simple broker, complex consumer"** — broker는 그냥 log를 쌓고, consumer가 offset을 관리한다. RabbitMQ·SQS는 **"complex broker, simple consumer"** — broker가 routing·delivery·retry를 다 책임지고, consumer는 그냥 받기만 한다.

이 차이가 왜 중요한가? Jack Vanlightly의 RabbitMQ 시리즈가 가장 명확히 설명한다.

> Kafka uses a "simple broker, complex consumer" approach, while RabbitMQ follows a "complex broker, simple consumer" model. (Quix Comparison)

Kafka에서는 같은 토픽을 두 그룹의 consumer가 각자 자기 offset으로 따로 소비할 수 있다. event sourcing, audit trail, 데이터 파이프라인의 fanout에 잘 맞는다. RabbitMQ에서는 메시지가 소비되면 사라진다. 작업 큐, RPC-like 비동기, 복잡한 routing(direct·topic·fanout exchange)에 잘 맞는다.

선택의 한 줄 가이드를 굳이 만들면 이렇다.

- **데이터 파이프라인·event log·replay가 필요한가?** Kafka.
- **routing·dead letter queue·작업 큐가 단순한가?** RabbitMQ.
- **AWS only이고 운영 비용 최소화가 우선인가?** SQS.
- **multi-tenant·glacier 같은 tiered storage가 필요한가?** Pulsar (단, 운영 인력 필요).

한국 백엔드에서는 Kafka가 압도적이다. 카카오·라인·쿠팡·우아한형제들 모두 Kafka 기반 인프라가 있다. 그러나 도메인에 따라 RabbitMQ가 답인 경우도 적지 않다. 토스의 결제 후처리 일부, 우아한형제들의 일부 작업 큐가 RabbitMQ로 운영된다는 사례가 있다. **"이력서에 Kafka 쓰려고 도입했다. 실제로는 RabbitMQ로 충분했다"**는 한국 백엔드 익명 후회 글이 OKKY에 정기적으로 올라오는 이유다(community 휴리스틱 10). 도구 선택은 도메인이 먼저고 이력서가 다음이다.

## Kafka의 모양 — partition, offset, consumer group

가장 많이 쓰이는 Kafka의 모양을 한 번 깊이 들여다보자. 다른 큐들도 모양은 다르지만 개념은 비슷하다.

### Topic, Partition, Offset

Kafka의 모든 메시지는 **topic**에 속한다. topic은 여러 **partition**으로 나뉘는데, 각 partition은 순서가 있는 append-only log다. 메시지는 partition 안에서 0부터 차례로 **offset**을 부여받는다.

```
topic: orders
  partition 0: [msg0, msg1, msg2, msg3, ...]   offset 0~3
  partition 1: [msg0, msg1, msg2, ...]          offset 0~2
  partition 2: [msg0, msg1, ...]                offset 0~1
```

같은 partition 안에서는 순서가 엄격히 보장된다. partition 사이에는 순서가 없다. 그래서 "한 사용자의 모든 이벤트는 같은 partition으로"라는 규칙이 자주 쓰인다. partition key를 user_id로 잡으면, 한 사용자의 메시지는 항상 같은 partition으로 가니 순서가 보장된다.

> 💡 partition 수는 한 번 정하면 늘리기는 쉬워도 줄이기는 어렵다. 그리고 partition을 늘리면, 같은 key가 다른 partition으로 가 순서 보장이 깨질 수 있다. **초기에 적당히 넉넉하게 잡는 편이 낫다.** 보통 consumer 최대 수 × 2~3 정도가 시작점이다.

### Consumer Group과 offset commit

consumer 여러 개가 모여 **consumer group**을 이룬다. 같은 group의 consumer들은 partition을 나눠서 소비한다. 한 partition은 한 group 안에서 정확히 한 consumer만 소비한다. 즉 **group 안에서 병렬도는 partition 수가 상한**이다.

```
topic: orders (3 partitions)
group: payment-processor (2 consumers)
  consumer A → partition 0, partition 1
  consumer B → partition 2
```

consumer를 3개로 늘리면 1:1로 매핑된다. 4개로 늘리면 한 consumer는 놀게 된다. partition 수를 미리 넉넉하게 잡아 두라는 이유가 여기에도 있다.

각 consumer는 어느 offset까지 처리했는지를 **commit**한다. commit은 두 가지 방식이 있다.

- **Auto commit (default):** `enable.auto.commit=true`로 두면 5초마다 자동 commit. 편하지만 **메시지 손실 위험**이 있다. consumer가 메시지를 받았는데 처리 전에 죽고 그 사이 auto commit이 일어나면, 그 메시지는 영영 안 처리된다.
- **Manual commit:** 처리 끝난 뒤에 명시적으로 `commitSync()` 호출. 안전하지만 코드가 더 복잡하고, **duplicate 위험**이 있다. 처리는 끝났는데 commit 직전에 죽으면, 다음에 같은 메시지를 또 처리한다.

이 두 모양이 곧 **at-least-once vs at-most-once**의 갈림이다. 둘 중 어느 쪽도 "정확히 한 번"은 아니다.

### Exactly-once의 진짜 의미

"Kafka는 exactly-once를 지원합니다"라는 말을 자주 듣는다. 사실은 그 말이 약간 부정확하다. Kafka의 transactional producer + read_committed consumer + idempotent producer를 함께 쓰면 **Kafka 내부에서는** exactly-once가 가능하다. 그런데 consumer가 메시지를 받아 **외부 시스템(DB, 다른 API)에 쓸 때** exactly-once는 보장되지 않는다. 외부 시스템도 transactional하게 묶어야 한다.

그래서 현실적으로는 거의 모든 시스템이 **at-least-once + idempotent consumer** 패턴을 쓴다. consumer 쪽에 idempotency key·중복 제거 로직을 두어, 같은 메시지가 두 번 와도 한 번만 효과가 나게 만든다. 이 패턴은 10장 멱등성·재시도·서킷 브레이커 챕터에서 깊게 다룬다. exactly-once를 약속하기보다, at-least-once를 받아들이고 idempotent하게 짜는 편이 훨씬 견고하다.

### KRaft — ZooKeeper와의 결별

Kafka 2.8+ 부터는 **KRaft**(Kafka Raft) 모드로 ZooKeeper 없이 metadata를 자체 관리한다. 그 전까지는 broker 메타데이터, partition leader 정보, consumer group 정보의 일부를 ZooKeeper에 저장해야 했다. ZooKeeper는 잘 만들어진 도구지만, Kafka와 함께 운영하는 부담이 만만치 않았다.

Raft 알고리즘 자체는 12장 합의·복제·일관성 챕터에서 깊게 다룬다. 여기서 짚어 둘 것은 **운영 부담이 알고리즘 선택보다 크다는 사실**이다. ZooKeeper는 안정적인 ZAB 합의 알고리즘으로 잘 돌았는데, Kafka는 굳이 자기 Raft를 새로 만들었다. 왜? "또 다른 분산 시스템을 운영하는 부담을 없애기 위해"가 가장 큰 동기였다.

이 사실은 우리에게도 시사점이 있다. **새 분산 부품을 도입한다는 건 새 운영 부담을 짊어진다는 것**이다. Kafka는 자기 부담을 줄이려고 결국 ZooKeeper를 떼어냈다. 우리가 큐 하나를 깐다는 것도 비슷한 무게의 결정이다.

## 한국 큐 운영 — LINE·카카오·쿠팡 사례

해외 사례가 모양을 가르쳐 준다면, 한국 사례는 우리 일상의 함정을 가르쳐 준다. 세 가지를 짚어 보자.

### LINE — Apache HTTP client 업그레이드로 throughput 1/3

LINE Engineering blog에 "Kafka 운영 실패담" 시리즈가 올라온 적이 있다. 가장 끔찍한 사례 중 하나는 **Apache HTTP client 라이브러리를 업그레이드한 후 throughput이 1/3로 떨어진** 사건이다. 코드는 안 바꿨고, 큐 설정도 그대로다. 단지 dependency 한 줄을 올렸을 뿐인데.

원인은 HTTP client의 connection pool 동작 변경이었다. 새 버전이 기본 connection 수를 줄였고, Kafka 쪽이 아닌 그 다음 단계 service의 throughput이 막혔다. 큐는 잘 작동했지만, downstream이 막히니 consumer가 lag을 쌓기 시작했고, 새벽이 되어서야 alert가 떴다.

이 사례가 가르쳐 주는 게 두 가지 있다.

1. **dependency upgrade는 dark deployment처럼 (실 트래픽 일부에만 먼저 흘려) 점검하자.** 기능에 변화가 없어도 throughput은 변할 수 있다.
2. **consumer lag을 메인 SLO 지표에 포함하자.** "처리 성공률"만 보면 throughput 저하가 안 보인다. lag 자체가 SLO의 한 축이 되어야 한다.

### 카카오 — 공용 메시징 플랫폼 TF

카카오 인프라팀은 2021년에 공용 Kafka/RabbitMQ MessageQueue TF를 정식으로 신설했다. 그 전까지는 각 서비스팀이 자체적으로 broker를 띄워 쓰는 형태였는데, 결과적으로 다음 문제들이 누적됐다.

- 같은 회사 안에 Kafka·RabbitMQ·자체 큐가 수십 개 운영. 운영자별 노하우가 흩어짐.
- 큐 사이의 메시지 라우팅이 service 코드 안에 박혀, decoupling이 무너짐.
- broker 한 대 장애 시 영향 범위 추적이 어려움.

TF의 결정은 명료했다. **공용 broker를 중앙에서 운영하고, 서비스팀은 producer·consumer 코드만 짠다.** 이 결정 덕분에 서비스팀의 큐 운영 부담이 줄고, 큐 사이의 흐름이 명확해졌다. 한국 백엔드의 일반적인 운영 패턴 중 하나로 자리잡고 있다.

### 쿠팡 — Kafka 기반 검색 indexing pipeline

쿠팡 엔지니어링 Medium에 "대용량 트래픽 처리를 위한 백엔드 전략"이라는 글이 있다. 쿠팡 검색 indexing pipeline은 Kafka가 중심이다. 상품 데이터가 변할 때마다 Kafka에 이벤트가 발행되고, 검색 indexing 파이프라인이 그 이벤트를 consume해 Elasticsearch에 색인한다.

이 구조의 가치는 **decoupling**이다. 상품 service는 Elasticsearch를 모른다. 검색 indexing pipeline은 상품 service의 DB 스키마를 모른다. 둘은 Kafka 토픽의 이벤트 schema로만 연결된다. 검색 indexing을 새 버전으로 갈아 끼울 때 상품 service는 영향이 없다.

이런 구조가 가능한 이유는 Kafka가 **retention 안에서 replay 가능**하기 때문이다. 새 indexing pipeline을 띄우면 offset 0부터 다시 읽어 전체를 재색인할 수 있다. RabbitMQ로는 이걸 못한다. Kafka의 "log is the queue" 모양이 이런 패턴을 가능하게 한다.

5장 검색 엔진에서 이 쿠팡 indexing pipeline의 디테일을 다시 다룬다. 큐와 검색은 떼어 놓을 수 없는 쌍이다.

## 메시지 큐의 운영 함정 5가지

큐가 망가지는 모양 다섯 가지를 정리하자. 큐 운영자라면 새벽에 alert가 울렸을 때 가장 먼저 떠올려야 할 후보들이다.

### 함정 1. Consumer Lag — 가장 흔하고 가장 silent

**가장 자주, 가장 silent하게 망가지는 모양**이다 — 1장 sidebar에서 JPA N+1을 두고 "조용히 죽이는 함정"이라 부른 패턴과 같은 결이다. 한국 백엔드는 평생 이런 silent killer를 안고 산다. 메시지는 producer가 잘 보내고 있고 broker는 잘 저장하고 있는데, consumer가 따라가지 못해 점점 쌓인다. lag이 1만, 10만, 100만으로 늘어 가는 동안 producer는 영문도 모른 채 평소처럼 메시지를 보낸다.

원인 후보는 다양하다.

- consumer의 downstream(DB, API)이 느려졌다.
- consumer 코드 안에 thread block이 생겼다(I/O 처리 누락 등).
- partition 수가 적어 병렬도가 부족하다.
- consumer instance 수가 partition보다 많아 일부가 놀고 있다.

대처는 lag 모니터링 + 자동 scale이 답이다. Kafka에서는 `kafka-consumer-groups.sh --describe`로 group별 lag을 볼 수 있고, Datadog·Burrow 같은 도구가 자동 모니터링을 제공한다. lag이 일정 임계를 넘으면 즉시 alert를 띄우자.

### 함정 2. Rebalance Storm

consumer가 죽거나 새로 뜨면 partition을 재할당하는 **rebalance**가 일어난다 — 부록 A의 tribal #5가 정확히 가리키는 함정이다. 이 동안 모든 consumer가 잠시 멈춘다. Kafka의 옛 버전(2.3 이하)에서는 모든 partition이 한 번에 재할당되어, group 전체가 수 초~수십 초 멈춘다. consumer가 자주 죽고 뜨는 환경에서는 rebalance만 1분에 한 번씩 일어나 throughput이 절반이 된다.

해결은 Kafka 2.4+로 올리고 **incremental cooperative rebalancing**을 켜는 것이다. partition 재할당이 점진적으로 일어나, 모든 consumer가 동시에 멈추지 않는다. 그리고 consumer의 죽고 뜨는 빈도 자체를 줄이는 게 더 근본적이다 — K8s에서 readiness probe 잘못 잡아 consumer가 자주 restart하는 경우가 흔하다.

### 함정 3. Retention 짧음 + Consumer down → 데이터 loss

Kafka의 default retention은 7일이다. 그런데 짧게 잡아 둔 경우 끔찍한 일이 일어날 수 있다.

상황을 가정해 보자. retention 1일로 설정된 토픽이 있다. consumer가 무슨 사고로 23시간 멈춰 있었다. 깨어나서 처리하려고 보니, 가장 오래된 메시지는 1시간 안에 만료된다. 그 메시지를 미처 처리하기 전에 retention이 끝나고 메시지가 삭제된다.

HN에 "How we lost 24 hours of data with Kafka"라는 글이 있다. `auto.offset.reset=latest` 설정이 함께 작용해, consumer가 깨어났을 때 옛 메시지를 다 건너뛰고 최신 메시지부터 읽기 시작한 사례다. 24시간치 데이터가 영영 사라졌다.

대처는 두 가지다.

1. **Critical 토픽의 retention은 충분히 길게 (보통 7일 이상).** 단, retention이 길어지면 storage 비용이 늘어난다.
2. **`auto.offset.reset=earliest`로 설정.** consumer가 깨어났을 때 옛 메시지부터 읽도록.

### 함정 4. Producer의 Dual-Write 문제

producer가 DB에 record를 쓰고, 그 다음에 Kafka에 이벤트를 발행하는 코드가 흔하다.

```python
def create_order(order):
    db.insert(order)        # 성공
    kafka.send(event)       # 실패 → 메시지 안 감
```

이 사이에 시스템이 죽으면? DB에는 주문이 들어 있는데 Kafka에는 이벤트가 없다. 다음 단계(결제·배송·알림)가 안 일어난다. 끔찍하다.

이 dual-write 문제의 정식 해법이 **Transactional Outbox 패턴**이다. DB 트랜잭션 안에서 outbox 테이블에 이벤트를 함께 insert하고, 별도 워커(Debezium 같은 CDC)가 그 테이블의 변경을 tail로 따라가며 Kafka에 발행한다. 같은 트랜잭션이라 atomic하다. 자세한 내용은 11장 Saga·Outbox 챕터에서 다룬다.

### 함정 5. 메시지가 너무 큰 경우

Kafka의 default `message.max.bytes`는 1MB다. 큰 binary payload나 거대한 JSON을 그대로 큐로 흘리려고 하면 broker가 거부한다. 설정을 높여서 보낼 수도 있지만, 그러면 broker·consumer 모두 메모리 부담이 크다.

표준 패턴은 **claim-check pattern(보관증 패턴)**이다. 큰 payload는 S3에 올리고, Kafka에는 그 S3 "보관증"(key)만 보낸다. consumer가 받아서 S3에서 가져온다. binary file processing pipeline에 자주 쓰이는 모양이다.

## Delivery Semantic — at-most-once vs at-least-once vs exactly-once

큐의 delivery 모드 3가지를 한 번 정리하자. 이름이 자주 헷갈리는 부분이다.

| 모드 | 의미 | 위험 |
|------|------|------|
| At-most-once | 0번 또는 1번 처리 | 메시지 손실 가능 |
| At-least-once | 1번 이상 처리 | 중복 처리 가능 |
| Exactly-once | 정확히 1번 처리 | broker·consumer·외부 시스템 모두 transactional 필요 |

Kafka·RabbitMQ·SQS 모두 default는 at-least-once다. consumer 입장에서는 같은 메시지가 두 번 올 수도 있다는 가정으로 코드를 짜야 한다.

**휴리스틱 하나를 마음에 새기자 — idempotent하지 않은 consumer는 큐를 쓸 자격이 없다.** 같은 메시지가 두 번 와도 한 번만 효과가 나도록 짜야 한다. 결제 처리, 잔고 차감, 알림 발송 — 모두 idempotency key로 중복을 제거하는 패턴이 필수다.

exactly-once를 약속하는 broker가 있다고 해도, 외부 시스템(우리 DB, 다른 API)에 쓰는 동작은 결국 우리 책임이다. broker의 exactly-once는 broker 안에서만 유효하다. 그래서 현실은 거의 항상 **at-least-once + idempotent consumer** 패턴이다. 이 두 단어를 마음에 새겨 두자.

## 큐 도입 자격을 묻는 6가지 질문

지금까지 살펴본 내용을 자기 팀 회의실에 가져가 보자. 큐를 도입하려는 결정 앞에서 자기에게 던져야 할 6가지 질문이다.

1. **이 흐름이 정말 비동기여야 하는가?** sync API로 충분히 풀리면, 큐는 차라리 안 까는 편이 낫다.
2. **어떤 delivery semantic이 필요한가?** at-most-once를 견딜 수 있는가, idempotent consumer를 짤 수 있는가?
3. **메시지 ordering이 필요한가, 필요하다면 어느 단위로?** user 단위? order 단위? 전체 토픽 단위? partition key 선택이 거기서 갈린다.
4. **retention이 얼마나 필요한가?** replay가 필요한가, 아니면 소비 후 삭제로 충분한가?
5. **운영 부담을 짊어질 수 있는가?** managed (MSK·SQS·Confluent Cloud)로 갈 것인가, 자체 운영할 것인가?
6. **모니터링은 어떻게 할 것인가?** consumer lag·rebalance·throughput 모니터링이 도입과 동시에 깔리는가?

이 여섯에 답이 안 나오면 도입을 미루는 편이 낫다. 답이 다 나오면, 그때야 broker 선택의 영역으로 넘어간다. **Kafka·RabbitMQ·SQS의 선택은 마지막 결정이지 첫 결정이 아니다.**

## Callback 예고 — 10·11·19장에서 큐가 다시 등장한다

큐는 빌딩 블록이지만, 본격적인 무대는 패턴과 케이스 스터디에서다.

- **10장 멱등성·재시도·서킷 브레이커.** 큐의 at-least-once가 idempotent consumer를 어떻게 만나는지.
- **11장 Saga·Outbox·이벤트 소싱.** dual-write 문제를 Outbox + CDC가 어떻게 푸는지. Saga의 compensating transaction이 큐 위에서 어떻게 흐르는지.
- **19장 결제 시스템.** 토스 결제 critical path가 어떻게 sync(승인)와 async(영수증·알림·정산)를 가르는지.

이 세 챕터에서 4장의 기초가 그대로 얹힌다. **빌딩 블록의 trade-off를 모르면 패턴의 의사결정이 막막해진다**는 사실이 이 책 전체에 흐르는 메시지다. 큐의 모양을 머릿속에 정확히 그려 두면, 나중 챕터들의 결정 트리가 자연스럽게 따라온다.

## 운영 모니터링 — 메시지 큐 대시보드 7가지

마지막으로 운영 대시보드를 정리하자.

| # | 지표 | 의미 | 위험 임계 |
|---|------|------|----------|
| 1 | producer send rate | 발행 속도 | 평소 ±50% 벗어나면 의심 |
| 2 | consumer fetch rate | 소비 속도 | producer rate보다 낮으면 lag 쌓임 |
| 3 | consumer lag (per group) | 처리 지연 | 임계 (예: 1만) 넘으면 즉시 alert |
| 4 | rebalance count | rebalance 발생 빈도 | 시간당 한 자릿수면 정상, 더 많으면 의심 |
| 5 | broker disk usage | retention storage | 80% 넘으면 retention 축소 또는 storage 증설 |
| 6 | broker network IO | 네트워크 포화 | 80% 넘으면 의심 |
| 7 | producer error rate / consumer error rate | 발행·소비 실패율 | 0이 정상, 0 초과면 즉시 조사 |

특히 **consumer lag**은 큐 운영의 가장 중요한 지표다. lag 그래프 하나가 큐 시스템의 건강을 압축적으로 보여 준다. lag 모니터링이 없는 큐는 안 깐 것과 다름없다고 봐도 좋다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 메시지 큐의 양면이 손에 잡혀 있다. 비동기·decoupling·load smoothing·replay라는 4가지 효과, Kafka·RabbitMQ·SQS·Pulsar의 갈림, 그리고 망가질 때의 5가지 모양 — consumer lag, rebalance storm, retention loss, dual-write, 메시지 크기. 한국 사례도 LINE의 HTTP client 업그레이드 실패담, 카카오 공용 메시징 플랫폼 TF, 쿠팡 검색 indexing pipeline까지 함께 짚었다.

기억해두자. 큐는 두 service를 시간으로 갈라 놓는 부품이다. 그 갈라짐 자체가 효과인 만큼, 갈라진 사이의 시야가 없으면 큐는 silent하게 망가진다. **lag 모니터링이 깔리지 않은 큐는 깔지 않은 것과 같다**는 사실을 마음에 새기자. 그리고 도입 전에 자기에게 6가지 질문을 던지자. 답이 다 안 나오면 도입을 미루는 편이 낫다.

다음 장에서는 검색 엔진을 살펴본다. 한국어가 영어 분석기로 안 되는 이유부터, Elasticsearch shard 100개의 진짜 의미까지. 그곳에서도 우리는 같은 질문을 만난다 — "이 부품을 도입할 자격이 우리에게 있는가."

---

# 5장. 검색 엔진 — 한국어가 영어 분석기로 안 되는 이유부터

신입 개발자가 처음으로 검색 페이지를 만들었다고 해보자. Elasticsearch를 띄우고, `match` 쿼리를 박고, 화면에 결과를 뿌렸다. 로컬에서 테스트하니 잘 된다. 그런데 production에 올렸더니 사용자가 "쿠팡 배송"을 검색했는데, "쿠팡배송"이라고 띄어쓰기가 다른 글이 안 잡힌다고 항의가 들어온다.

개발자는 어이가 없다. "쿠팡 배송"이나 "쿠팡배송"이나 같은 말 아닌가? 그런데 Elasticsearch는 그렇게 보지 않는다. 영어 분석기는 공백을 단어 경계로 보고 토큰을 자른다. "쿠팡 배송"은 "쿠팡"과 "배송" 두 토큰, "쿠팡배송"은 "쿠팡배송"이라는 한 토큰. 둘은 같은 단어가 아니라 완전히 다른 토큰이다. 그러니 매칭이 안 된다.

이게 한국어 검색의 첫 관문이다. 영어책에는 안 나오는 문제다. 영어는 띄어쓰기가 단어 경계라 그냥 두면 된다. 한국어는 조사가 붙고, 띄어쓰기가 규범과 다르게 쓰이고, 합성어가 띄어쓰기를 넘어 만들어진다. 검색이 어렵다.

검색 엔진은 결코 단순한 "match 쿼리 한 줄"이 아니다. 한국어 관점에서 깊게 들어가야 비로소 부품의 진짜 모양이 보인다. inverted index가 무엇을 약속하는지, 한국어 형태소 분석기 5종이 어떻게 다른지, Elasticsearch의 shard 100개가 과연 무슨 결정이었는지, 그리고 vector search가 무대로 올라오는 순간 무엇이 또 바뀌는지 — 한 박자씩 짚어 보자.

## Inverted Index — 검색이 빠른 진짜 이유

검색 엔진의 심장은 **inverted index**다. 일반 인덱스는 "row → 컬럼 값"이지만, inverted index는 "단어 → 그 단어가 등장한 문서들"이다. 마치 책 끝에 붙어 있는 색인을 생각하면 가깝다. 단어가 알파벳 순으로 정렬되어 있고, 그 옆에 등장한 페이지가 적혀 있다.

```
문서 1: "쿠팡 배송 빠르다"
문서 2: "쿠팡 직구 배송"
문서 3: "배송 추적 어디서"

inverted index:
  쿠팡   → [1, 2]
  배송   → [1, 2, 3]
  빠르다 → [1]
  직구   → [2]
  추적   → [3]
  어디서 → [3]
```

이 구조 덕분에 "쿠팡"으로 검색하면, 전체 문서를 다 스캔하지 않고 색인의 "쿠팡" 항목만 보면 끝난다. 100만 개 문서가 있어도 검색은 거의 즉시다.

여기서 두 가지 흥미로운 함의가 나온다.

**첫째, 색인이 무거운 작업이다.** 새 문서가 들어올 때마다 모든 토큰을 추출해 색인을 갱신해야 한다. 이걸 동기로 처리하면 write가 매우 느려진다. 그래서 검색 엔진은 보통 색인을 비동기로 처리한다. write와 read 사이에 **인덱싱 지연(indexing lag)**이 존재한다.

**둘째, 토큰을 어떻게 자르냐가 검색 품질을 결정한다.** "쿠팡 배송"을 어떻게 토큰화하는지가 결국 "쿠팡배송"이라는 검색어가 잡히느냐 안 잡히느냐를 결정한다. 이게 한국어 검색이 영어 검색과 결정적으로 갈리는 지점이다.

## Lucene과 Elasticsearch — 같은 심장, 다른 옷

Elasticsearch는 자체 검색 엔진이 아니다. 심장은 **Lucene**이다. Lucene은 자바로 짠 inverted index 라이브러리고, Elasticsearch는 그 Lucene 위에 분산 처리, REST API, 클러스터 운영, 메트릭 등 엔터프라이즈 기능을 입힌 wrapper(외피)다. Solr도 Lucene 기반이다.

이 사실이 의외로 중요하다. 한 가지 결과로 이어진다 — **Elasticsearch 운영 함정의 절반은 Lucene 함정이다.** segment 구조, refresh, merge, 분석기 동작 — 모두 Lucene 레벨에서 일어난다. Elasticsearch 매뉴얼만 봐서는 어디가 어디인지 헷갈리는 경우가 많다.

Lucene의 핵심 개념을 짧게 정리하자.

- **Index = shard들의 모음**. 각 shard는 Lucene index 한 개.
- **Segment = shard 안의 immutable 파일 단위**. 한 번 쓰여진 segment는 수정 불가, 삭제는 tombstone으로 표시.
- **Refresh = 메모리 buffer의 데이터를 새 segment로 flush해 검색 가능하게 만드는 작업.** default 1초.
- **Merge = 작은 segment들을 큰 segment로 합치는 작업.** I/O 부담이 큼, background에서 진행.
- **Flush = WAL(translog)을 디스크에 동기화.** durability 보장.

이 다섯 개념이 머릿속에 있어야 Elasticsearch 운영 함정을 디버깅할 수 있다. 안 그러면 매번 "왜 검색이 안 되지?", "왜 디스크가 가득 차지?" 같은 새벽 질문을 받게 된다.

## 한국어 분석기 5종 — mecab-ko, NORI, KOMORAN, Khaiii, KIWI

토큰을 어떻게 자르냐의 문제로 돌아오자. 영어는 공백·구두점 기준으로 자르면 거의 끝이다. 한국어는 그렇지 않다. 다음 분석기 5종이 한국어 검색의 주요 선택지다.

| 분석기 | 출처 | 기반 | 특징 |
|--------|------|------|------|
| **mecab-ko (은전한닢)** | 일본 mecab 한국어 포트 | 사전 기반 | 가장 오래되고 안정적. 사전 갱신이 보수적. |
| **NORI** | Lucene 내장 (KOMORAN 기반) | 사전 + 규칙 | Elasticsearch 기본 한국어 분석기. 의존성 없이 깔리는 장점. |
| **KOMORAN** | shineware | 사전 + 규칙 | 사용자 사전 추가 쉬움. 한국어 형태소 분석기 비교 글에 자주 등장. |
| **Khaiii** | 카카오 | CNN 기반 (deep learning) | 비교적 새 모델. 신조어·구어체 강함. |
| **KIWI** | 한국어 형태소 오픈소스 | 사전 + 통계 | 빠른 속도, 사용자 사전 손쉬움. 최근 한국 백엔드에서 인기 상승. |

이 다섯이 각각 어떻게 자를까? "쿠팡 배송 빠르다"라는 문장을 한 번 비교해 보자(개략적인 결과 — 실제 출력은 버전별로 다를 수 있다, 검증 필요).

```
mecab-ko:  [쿠팡(고유명사), 배송(명사), 빠르(형용사 어간), 다(어미)]
NORI:      [쿠팡, 배송, 빠르다]
KIWI:      [쿠팡(NNP), 배송(NNG), 빠르(VA), 다(EF)]
```

조사, 어미가 분리되거나 아니거나, 어간만 남기거나 어형까지 남기거나 차이가 있다. 검색 품질은 이 토큰화의 디테일에 좌우된다.

그리고 한국어 검색에는 두 가지 추가 처리가 거의 필수다.

**1. Synonym (동의어).** "삼성전자" ↔ "삼성", "맥북" ↔ "MacBook" 같은 동의어 사전. 이건 분석기와 별개로 Elasticsearch synonym filter로 처리한다.

**2. n-gram 또는 부분 매칭.** "쿠팡 배송"으로 검색했을 때 "쿠팡배송"도 잡히게 하려면 n-gram을 함께 색인하는 패턴이 자주 쓰인다. 예를 들어 2-gram이면 "쿠팡배송"은 ["쿠팡", "팡배", "배송"]으로 색인된다. 색인 크기가 커지는 부담이 있지만, 부분 매칭이 가능해진다.

> 💡 한국어 검색을 시작할 때 분석기 선택의 한 줄 가이드. **새 프로젝트면 KIWI 또는 NORI로 시작하자.** Khaiii는 신조어·구어체 강점이 명확한 도메인(채팅·SNS)에 한해 검토. mecab-ko는 안정성으로 굳어진 곳에서 계속 쓰는 편이 낫지만, 새 프로젝트의 default로는 KIWI·NORI가 운영 도구 풍부함에서 앞선다.

## "쿠팡 배송" vs "쿠팡배송" — 한국어 검색 7가지 함정

5종 분석기 중 무엇을 골라도 한국어 검색의 함정은 비슷하다. 한국 백엔드에서 자주 만나는 7가지를 정리하자.

**1. 합성어 띄어쓰기.** "쿠팡 배송" vs "쿠팡배송", "강남역" vs "강남 역". 사용자는 자기 마음대로 띄어 쓴다. n-gram 색인 또는 띄어쓰기 정규화가 필요하다.

**2. 조사·어미 처리.** "배송이", "배송을", "배송에서"가 다 "배송"의 변형이다. 형태소 분석기가 어간을 추출하므로 보통 해결되지만, 색인 시와 검색 시 동일한 분석기를 적용해야 한다.

**3. 신조어·외래어.** "맥북" / "MacBook" / "맥북프로" / "Macbook Pro", "갓성비" / "가성비". 사전 기반 분석기는 사용자 사전을 정기 갱신해야 한다.

**4. 영문·한글 혼용.** "iPhone 15" 검색이 "아이폰 15"도 잡히게 할지, "iphone15" 띄어쓰기 없는 입력도 잡히게 할지. synonym + n-gram 조합으로 풀거나, 입력 시점에 normalize한다.

**5. 자동완성·오타 교정.** "쿠팡"을 치다 "쿠퍙"으로 친다든지. edit distance 기반 fuzzy 검색, 또는 자모 단위 색인으로 풀 수 있다. Elasticsearch의 `completion suggester`, `phonetic analyzer` 등이 도구.

**6. 검색 의도 분기.** "쿠팡 배송"을 친 사용자는 (a) 쿠팡의 배송 정책을 찾는 건가 (b) 쿠팡으로 배송된 상품을 찾는 건가? 같은 검색어가 도메인에 따라 다른 의도다. 의도 분류는 검색 quality team의 주요 과제다.

**7. 색인 갱신 지연.** 새 상품 정보를 등록했는데 검색에서 안 잡힌다는 항의. inverted index 특성상 indexing lag이 있다. `refresh_interval`을 줄이거나, 갱신 후 명시적 `_refresh` 호출이 필요한 경우가 있다.

이 7가지를 다 한 번에 풀 수는 없다. 도메인에 따라 우선순위가 다르다. 이커머스는 1·3이 중요하고, 채팅 검색은 5가 중요하고, 뉴스 검색은 6이 중요하다. **무엇을 먼저 풀지 도메인이 결정하게 두는 편이 낫다.**

## Shard 설계 — 100개가 정말 필요했는가

Elasticsearch 운영의 가장 자주 묻는 질문이 "shard를 몇 개로 잡을까"다. 한국 백엔드에서 "shard 100개", "shard 200개"라는 발표를 들으면 멋있어 보이지만, 정작 그게 정말 필요했는지를 묻는 사람은 적다.

Elastic 공식 가이드의 한 줄이 가장 직설적이다.

> An optimal shard should hold 10-50GB of data, with fewer than 200 million documents per shard. (Elastic Docs, *Shards and Replicas Guide*)

shard 하나당 10~50GB, 2억 doc 이하. 이 한 줄에서 시작하자. 우리 인덱스가 100GB라면 shard 2~10개면 충분하다. 100GB 인덱스에 shard 100개를 박는 건 shard당 1GB 꼴이고, 이건 oversharding이다.

oversharding이 왜 문제일까?

- **shard마다 Lucene 오버헤드.** segment 메타데이터, 메모리, 파일 핸들이 shard 수만큼 곱해진다.
- **검색 시 모든 shard에 fan-out.** 검색 한 번이 100개 shard를 거치니, 네트워크·CPU 부담이 곱해진다.
- **cluster state 비대.** shard가 많으면 master node의 cluster state 관리가 무거워져, master가 느려진다.

undersharding은 반대로 한 shard가 너무 커져 검색·인덱싱이 한 노드에 집중된다. 50GB를 넘어가면 GC, merge, recovery가 모두 끔찍해진다.

그래서 정상 범위는 **인덱스 크기 / 30GB 정도가 shard 수의 시작점**이다. 거기에 미래 성장 + 여유분으로 1.5배쯤 잡는다. 100GB 인덱스라면 shard 4~5개, 1TB 인덱스라면 30~40개. 처음부터 100개를 박는 게 아니라, 인덱스가 자라면서 새 인덱스를 만들거나 reindex로 재구성하는 편이 낫다.

> 💡 한국 백엔드의 흔한 함정 — "남들이 shard 100개라고 하니까 우리도." 도구 도입의 자격 검증과 같은 결의 함정이다. 우리 데이터 크기가 shard 100개를 요구하는가? 답이 "아니다"라면 100개는 oversharding이고 운영 부담만 늘린다. **shard 수는 패션이 아니라 데이터 크기의 함수다.**

## JVM Heap — 32GB의 마법선

Elasticsearch는 자바로 짠 시스템이다. JVM 위에서 돌고, JVM의 GC가 latency에 직접 영향을 준다. 그래서 JVM 튜닝의 한 줄 규칙이 한국·해외 모두에 정착되어 있다.

> Above ~32GB, pointers become 64-bit, you lose compressed oops, and you might as well have 60GB to break even. (heuristic #1 in 한국 운영 커뮤니티)

JVM은 64-bit OS에서 기본 포인터가 64-bit지만, heap이 32GB 이하면 **compressed oops**(ordinary object pointers)로 32-bit 포인터를 쓴다. heap이 작아서가 아니라, 메모리 효율을 위해 압축된 포인터를 쓰는 것. 32GB를 넘는 순간 이 압축이 풀려, 같은 객체 수에 메모리가 더 들고 cache miss가 늘어 오히려 느려진다.

그래서 ES·Cassandra·Kafka·Solr 등 JVM 기반 시스템의 heap은 모두 **30GB 또는 31GB 이하로 잡는 게 표준**이다. 한 노드의 메모리가 128GB라면 ES heap은 30GB, 나머지 98GB는 OS file system cache로 쓴다. Lucene의 inverted index는 file system cache의 효과가 매우 크기 때문에 이 분배가 합리적이다.

이 한 줄 규칙을 어기는 운영을 한 번 본 적 있다. 메모리 256GB짜리 ES 노드에 heap을 128GB로 잡았는데, GC pause가 늘어 latency p99가 30초까지 솟구쳤다. 적정 heap(30GB)으로 줄였더니 같은 노드에서 latency p99가 200ms로 돌아왔다. JVM tuning은 작은 결정 같지만 운영에서 가장 큰 차이를 만들 수 있다.

## `refresh_interval` — 1초 default의 함정

Elasticsearch가 새 문서를 색인하면, default 1초마다 segment를 만들어 검색 가능하게 한다(`refresh_interval=1s`). 거의 실시간으로 검색이 된다는 약속이다.

그런데 이 default가 write-heavy 시스템에서는 끔찍한 함정이다. write가 분당 수만 건씩 들어오는 indexing pipeline이라면, 매초 segment가 만들어진다. segment가 빠르게 늘면 merge가 따라가지 못하고, merge가 느려지면 디스크 IO가 폭증하고, GC가 잦아진다. 결과적으로 색인 throughput이 절반으로 떨어진다. 새 ES 클러스터 띄운 첫 주의 일상이다 — 부하 테스트에서는 보이지 않다가 production 트래픽이 들어오자마자 찜찜한 lag 차트가 등장한다.

해결은 단순하다 — **write-heavy 인덱스의 `refresh_interval`을 30초 또는 60초로 늘리자.**

```
PUT /products/_settings
{
  "refresh_interval": "30s"
}
```

이 한 줄로 throughput이 2~3배 올라가는 경우가 흔하다. 단, 새 문서가 검색에 보이기까지 30초 지연이 생긴다. 30초 지연을 못 견디는 도메인(실시간 chat 검색 등)은 1초를 유지하거나, 아예 검색 직전에 `_refresh`를 명시적으로 호출하는 패턴을 쓴다.

그리고 한 가지 더 — **bulk indexing 시에는 `refresh_interval`을 -1로 잡고, 끝난 뒤에 한 번 refresh하는 패턴**이 표준이다. 1억 doc을 색인하는 batch라면 이 패턴이 throughput을 10배 늘릴 수 있다.

tribal #17 — "refresh_interval 1초 default 함정"이 한국 운영 커뮤니티에 단골로 올라오는 이유다. 새 ES 클러스터 만들 때 이 한 줄을 챙기는 편이 낫다.

## ES vs OpenSearch 분기 — 그리고 자체 엔진

2021년 Elastic이 라이선스를 SSPL로 바꿨고, AWS는 그 직전 fork인 ES 7.10을 기반으로 **OpenSearch**를 분리했다. 그 이후 두 엔진은 다른 길로 분기 중이다.

| 항목 | Elasticsearch | OpenSearch |
|------|---------------|-----------|
| 라이선스 | Elastic License v2 / SSPL (상용) | Apache 2.0 (완전 오픈) |
| 매니지드 | Elastic Cloud, AWS Elastic Cloud | AWS OpenSearch Service |
| 부가 기능 | ML, alerting, security 풍부 | 일부 무료 (보안·alerting 포함) |
| ML | Elastic ML 라이선스 별도 | OpenSearch ML 무료 |
| Vector search | dense_vector + HNSW | k-NN plugin (HNSW) |

새 프로젝트가 AWS 중심이고 비용 절감이 우선이라면 OpenSearch가 합리적이다. Elastic의 부가 기능(ML, security)이 필요하면 Elasticsearch. 한국 백엔드에서는 양쪽 모두 채택 사례가 있다.

한 가지 더, 큰 회사는 종종 **자체 엔진**을 만든다. LINE NSE, 카카오 다음 검색, 네이버 자체 검색 엔진. 이유는 단순하다 — ES·OpenSearch가 못 풀어주는 특정 도메인 문제가 있어서다.

- **LINE NSE.** 메신저 대화 검색은 일반 ES로 안 풀리는 이슈가 많다(privacy, encryption, multi-language).
- **네이버.** 한국어 형태소 + 다음·네이버 도메인 + 광고·랭킹 알고리즘. ES로는 부족하다.
- **Slack KalDB.** Slack 메시지 검색은 ES로 했지만, **로그 검색은 ES 한계로 자체 KalDB 개발**. logz.io의 분석에 따르면 ES가 로그 같은 high-volume immutable data에 비싸다는 평가다.

자체 엔진을 만든다는 결정은 거의 항상 **연 100만 query 이상**의 규모이고, **20명 이상의 search team**이 있는 회사의 결정이다. 일반 한국 백엔드 팀의 자격 검증을 통과하지 않는다. ES·OpenSearch가 충분한 선택이고, 자체 엔진은 안 만드는 편이 낫다.

## 쿠팡 검색 — Kafka 기반 indexing pipeline

한국 백엔드에서 가장 자주 인용되는 검색 사례는 쿠팡이다. 쿠팡 엔지니어링 Medium에 "Fueling the Coupang Search Engine"이라는 글이 있다.

핵심 구조는 다음과 같다.

1. **상품 데이터의 변화**(가격·재고·설명 등 변경)가 일어나면, 상품 service가 **Kafka**에 변경 이벤트를 발행한다.
2. **indexing pipeline**(자체 구축)이 이 이벤트를 consume해, 검색용 schema로 변환한다. ML 기반 feature, 카테고리 분류 등이 이 단계에서 추가된다.
3. 변환된 doc을 **Elasticsearch**(또는 자체 엔진)에 색인한다.
4. **검색 API**가 ES를 호출해 결과를 반환한다.

이 구조의 가치는 **decoupling**이다. 상품 service는 검색 schema를 모른다. 검색 indexing pipeline은 상품 DB schema를 모른다. 둘은 Kafka의 이벤트 schema로만 묶인다. 4장 메시지 큐 챕터에서 본 그 decoupling 패턴이 여기서 그대로 작동한다.

그리고 한 가지 더 흥미로운 점 — **rebuild가 쉽다**. 검색 schema를 바꿔야 한다면, 새 ES 인덱스를 만들고 Kafka offset 0부터 다시 consume하면 된다. Kafka의 retention 안에서 replay가 가능하기 때문이다. 검색 schema는 도메인이 진화하면 자주 바뀌는데, 이 rebuild 패턴이 그 진화를 견디는 무기다.

## Slack 검색 — 메시지와 로그를 가르는 결정

Slack은 10B 메시지 이상을 다루는데, **검색은 Elasticsearch, 로그는 자체 KalDB**라는 결정을 했다. 같은 검색이라도 도메인에 따라 도구를 가른 사례다.

왜 갈렸을까? 두 도메인의 특성이 다르기 때문이다.

| 차원 | 메시지 검색 | 로그 검색 |
|------|-----------|----------|
| 빈도 | 사용자가 자주 검색 | 디버깅 시에만 |
| 데이터 양 | 메시지 1개당 작음, 총량 큼 | 로그 1개당 더 작음, 총량 훨씬 큼 |
| ranking | 관련도, 시간, 채널 가중 등 복잡 | 시간 순 + 키워드 필터 단순 |
| 갱신 | append-only | append-only |
| 가용성 | high (사용자 영향 직접) | medium (디버깅용) |

메시지는 ranking이 복잡하고 사용자에게 즉시 영향을 주니 ES가 잘 맞는다. 로그는 단순 시간 순 + 필터, 그리고 데이터 양이 너무 커서 ES의 비용이 감당이 안 된다. 그래서 자체 KalDB로 분리.

**도구는 도메인이 결정한다는 사실**이 여기서도 작동한다. "Slack은 검색에 ES 쓴다"가 아니라, "Slack은 메시지에 ES, 로그에 KalDB"가 정확한 진술이다. 우리도 자기 검색 도메인을 세분화해서, 어디까지 ES이고 어디부터 다른 도구인지 가르는 편이 낫다.

## Vector Search — ANN의 무대

2023년 이후 검색에 새로운 축이 들어왔다. **벡터 검색**, 정확히는 **ANN (Approximate Nearest Neighbor)** 검색이다. LLM이 일상이 된 첫 해에 검색이라는 부품도 자연스럽게 이 새 축을 받아들였다. 텍스트를 임베딩 벡터로 변환해, 의미가 비슷한 문서를 찾는다. "쿠팡 배송"을 검색했을 때 정확히 "쿠팡 배송"이 안 적혀 있어도, 의미가 유사한 "쿠팡 빠른배송", "쿠팡 익일배송" 같은 문서를 찾을 수 있다.

ANN 알고리즘에는 크게 두 갈래가 있다.

- **HNSW (Hierarchical Navigable Small World).** 그래프 기반. 검색 속도 빠름, 메모리 많이 씀, 인덱스 갱신은 비교적 어렵다. Elasticsearch dense_vector, Pinecone, Weaviate가 채택.
- **IVF (Inverted File Index).** 클러스터 기반. 인덱스 갱신 쉬움, 메모리 적게 씀, 검색 정확도는 HNSW보다 약간 낮다. FAISS의 default, Airbnb 채택.

Airbnb의 흥미로운 결정이 여기 있다. Airbnb는 가격·가용성이 매우 자주 바뀌는 도메인이라, **인덱스 갱신 속도가 검색 정확도보다 우선**이라는 결론에 도달했다. 그래서 HNSW가 아닌 IVF를 채택했다. 일반적인 "HNSW가 빠르고 정확하다"는 통념이 도메인에 따라 뒤집힐 수 있다는 사례다.

벡터 검색은 텍스트 검색을 대체하지 않는다. **하이브리드 검색** — 텍스트 매칭 + 벡터 유사도를 함께 쓰는 패턴이 표준이다. Elasticsearch 8.x의 dense_vector + BM25 결합, OpenSearch의 k-NN + 일반 검색 결합이 그 모양이다. 한국 백엔드에서도 2025년부터 본격적으로 채택 사례가 늘고 있다.

자세한 내용은 15장 데이터 파이프라인·CRDT 챕터에서 vector DB(Pinecone, Weaviate, pgvector)와 함께 다시 다룬다. 검색 엔진은 이제 텍스트와 벡터의 양 축을 가르는 부품이다.

## 검색 운영 함정 5가지 정리

지금까지 살펴본 함정들을 한 번 정리하자. 새 ES 클러스터를 띄울 때 챙겨야 할 5가지다.

| # | 함정 | 대처 |
|---|------|------|
| 1 | shard oversharding | 인덱스 크기 / 30GB 시작점. 패션이 아니라 데이터 함수. |
| 2 | JVM heap > 32GB | 30GB 이하로 잡고 나머지는 file system cache로. |
| 3 | refresh_interval 1초 default | write-heavy 인덱스는 30s 또는 60s로. bulk는 -1. |
| 4 | 분석기 mismatch | 색인 시와 검색 시 동일 분석기 사용. 한국어는 NORI·KIWI 시작. |
| 5 | indexing lag 무관심 | producer→Kafka→indexer→ES 사이 latency 모니터링. lag을 SLO에 포함. |

이 5가지를 default로 챙기는 ES 클러스터는 한국 백엔드 평균보다 훨씬 안정적이다.

## 검색 도입 자격을 묻는 5가지 질문

마지막으로 메타 질문. 새 시스템에 검색 엔진을 도입하려는 결정 앞에서 자기에게 던질 5가지 질문이다.

1. **DB로 충분히 풀리지 않는가?** Postgres의 `tsvector`, MySQL의 `FULLTEXT` 인덱스로 처음에는 충분한 경우가 많다. 휴리스틱 3 "Just use Postgres"의 한 영역이다.
2. **검색 트래픽이 어느 정도인가?** QPS가 낮으면 ES의 운영 부담을 정당화하기 어렵다.
3. **한국어 처리가 필요한가?** 필요하다면 분석기를 어디까지 튜닝할 것인가?
4. **indexing pipeline을 어떻게 만들 것인가?** dual-write로 갈 것인가, Kafka 기반 event sourcing으로 갈 것인가?
5. **운영 부담을 짊어질 수 있는가?** ES는 운영이 무거운 시스템이다. 자체 운영할지, 매니지드(Elastic Cloud, AWS OpenSearch)로 갈지 결정해야 한다.

이 다섯에 답이 명확하지 않다면, 우선 Postgres `tsvector`로 시작해서 한계가 오면 ES로 옮기는 편이 낫다. **검색 엔진 도입의 자격은 검색 트래픽이 보장해 준다.**

## Callback 예고

검색 엔진은 책 후반에 다시 나타난다.

- **15장 데이터 파이프라인·CRDT.** vector DB와 ANN 알고리즘을 깊게.
- **18장 검색·매칭·지오.** 매칭 시스템(Uber·당근·배민 라이더)의 search + geo + ranking 결합.

이 두 챕터에서 5장의 기초가 그대로 얹힌다. inverted index, 분석기, shard 설계, JVM tuning — 모두 그 위에서 도메인별 디자인이 펼쳐진다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 검색 엔진의 한국어 관점이 손에 잡혀 있다. inverted index의 약속, Lucene과 Elasticsearch의 관계, 한국어 분석기 5종, "쿠팡 배송 vs 쿠팡배송"의 함정, shard 설계와 JVM heap, refresh_interval, ES vs OpenSearch 분기, 그리고 쿠팡·Slack·Airbnb의 검색 사례까지. 마지막으로 vector search라는 새 축이 어떻게 텍스트 검색 옆에 자리잡았는지가 한 묶음이다.

기억해두자. **검색 엔진은 'match 쿼리'가 아니라 토큰화·shard·refresh의 트리오로 결정된다.** 그리고 영어책에 안 나오는 한국어 함정이 우리 일상이다. 이 함정의 모양이 머릿속에 자동으로 펼쳐질 때, 우리는 "검색을 안다"고 말할 자격이 있는 백엔드 개발자가 되어 있다.

다음 장에서는 로드 밸런서·게이트웨이·서비스 메시를 살펴본다. L4와 L7이 운영 관점에서 어떻게 다른지, 그리고 5명짜리 팀이 Istio를 깔았다가 한 주의 절반을 mesh 튜닝에 쓰게 되는 그 함정의 모양을 함께 짚어 보자.

---

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

여기서 흔한 함정 하나. Envoy의 메모리 150MB는 한 instance 기준이지만, mesh를 쓰면 **모든 application pod 옆에 sidecar로 1개씩** 붙는다. pod이 1000개면 sidecar 메모리 합이 150GB다. 5명 팀이 운영하는 cluster 전체 메모리가 보통 100~200GB라는 점을 떠올려 보면, **mesh 도입이 cluster 메모리를 두 배 가까이 늘리는 결정**이라는 사실이 보인다. 5명 팀이 처음 이 숫자를 보면 정신이 아득해진다. mesh의 진짜 비용이 latency 이전에 메모리에서 먼저 드러난다는 점을 기억해두자.

## API Gateway는 어디에 사는가

로드 밸런서와 service mesh 사이에 한 자리가 더 있다. **API Gateway**다. Kong, AWS API Gateway, Spring Cloud Gateway, Apigee 등이 여기 들어간다. 이 자리가 왜 필요한지부터 짚고 가자.

LB가 "어느 backend instance로 보낼까"를 결정한다면, API Gateway는 "어느 service로 보낼까 + 인증·rate limit·response transform"을 결정한다. 그러니까 LB의 위에 한 층 더 얹은 셈이다.

상황을 가정해보자. 마이크로서비스가 10개 있고, 외부 클라이언트가 모두에게 직접 호출하면 endpoint가 10군데로 흩어진다. 인증을 service마다 각자 하면 코드가 10번 중복되고, 일관성도 깨진다. API Gateway 한 자리에 인증·rate limit·CORS·request transform을 모아두면 각 service는 비즈니스만 하면 된다.

다만 API Gateway가 단일 실패점이 된다는 점이 항상 따라 다닌다. 거기가 죽으면 모든 외부 트래픽이 죽는다. 그래서 Gateway는 **stateless + horizontal scale + 다중 region**이 기본 가정이다. 한 region에 Gateway 한 대만 두는 구성은 production에 어울리지 않는다.

한국에서는 토스·우아한형제들·라인이 모두 Gateway 패턴을 쓴다. 토스의 Spring Cloud Gateway, 우아한형제들의 자체 Gateway, 라인의 API 라우터가 각각 자기 도메인 특수성을 흡수한다. 특히 결제 도메인에서는 외부 PG·통신사 본인인증 같은 vendor 호출을 Gateway 뒤에 wrapper layer(외부 vendor 호출을 한 층 더 감싸는 층)로 감싸는 패턴이 일반화돼 있는데, 이 wrapper 패턴은 19장 결제에서 다시 만난다.

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

이 숫자가 처음 눈에 들어오면 한참 응시하게 된다. **Istio 전통 모드의 +166% latency는 농담이 아니다.** p50 50ms 응답하던 service가 mesh 깔자마자 130ms로 치솟는 자리다. 그리고 pod마다 150MB sidecar가 붙으니, 100개 pod 운영하던 cluster의 메모리 사용량이 15GB 늘어난다. 사용자가 느끼는 latency도, AWS 청구서도, 둘 다 만만치 않다.

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

이걸 분해 도구로 정리해보면 다음 4개 질문이 mesh 도입의 정량적 의사결정 도구가 된다.

1. **service 수**: 50 미만 → mesh 없이 LB + Gateway로 충분.
2. **팀 수**: 5 미만 → 한 팀이 모든 service를 운영하므로 mesh 없이도 일관성 유지 가능.
3. **mTLS audit 요구**: 금융·의료 외에는 보통 strong 요구가 아니다. 한국 금융권은 9장에서 다시 본다.
4. **on-call 인력**: 24/7 SRE가 없으면 Istio sidecar OOM kill을 새벽 3시에 추적할 사람이 없다. Linkerd나 Ambient를 먼저 고려하자.

네 질문에 모두 "그렇다"가 나올 때만 mesh 도입을 검토하는 편이 낫다. 그 전에 mesh를 깐다면, mesh 자체가 우리 팀의 본업이 돼버리는 끔찍한 일이 일어난다.

## 한국 사례 — 토스·우아한형제들·라인의 선택

한국에서 mesh를 어떻게 다루고 있는지를 한 단락으로 정리하자. 공개 발표·conference 발언 기준으로 다음과 같은 큰 흐름이 잡힌다.

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

그리고 가장 중요한 결론 한 줄. **mesh는 도입 여부의 문제가 아니라, mTLS·observability·traffic split 중 무엇을 켤지의 분해 문제다.** mTLS만 필요한가, observability만 필요한가, traffic split만 필요한가를 따로 따져보자. mesh 없이도 셋 다 가능한 자리가 많다. ALB의 weighted target group, OpenTelemetry collector, AWS PrivateLink로 셋이 따로따로 해결되는 경우가 흔하다.

mesh를 깔자고 결정한 팀에게도 같은 조언이 적용된다. **Istio 전통 sidecar의 +166% latency를 정량으로 알고 도입하는 편이 낫다.** Linkerd나 Istio Ambient로 시작해서 점진적으로 옮겨가는 길이 항상 열려 있다. 한 번에 모든 service에 sidecar를 다는 결정은 거의 항상 후회로 끝난다.

## 다음 장으로 가는 다리

여기까지가 외부 트래픽이 우리 시스템 안으로 들어오는 입구의 풍경이다. LB가 트래픽을 받아 backend로 흘리고, Gateway가 인증을 처리하고, mesh가 내부 호출을 묶는다. 그렇다면 그 트래픽은 어디에서 왔는가?

다음 장에서는 사용자에 더 가까운 자리, **CDN과 edge**를 살펴본다. Netflix가 왜 자기 비디오 트래픽의 거의 전체를 AWS origin을 거치지 않고 ISP에 박은 Open Connect Appliance로 보내고 있는지(검증 필요), edge compute가 cold start <5ms로 어떻게 가능한지, 객체 스토리지의 S3 함정은 무엇인지를 함께 본다. LB가 origin 앞에서 트래픽을 받는 부품이라면, CDN은 origin에 도달하지 않게 트래픽을 미리 흡수하는 부품이다. 둘은 보완재다.

가기 전에 한 번 정리하자. **5명 팀이 Istio를 깔면 안 된다는 결론이 너무 강하게 들렸다면, 그건 우리 팀의 안전을 위한 단호함이다.** 도구가 우리를 일하게 하는 자리가 아니라, 우리가 도구를 일하게 하는 자리에 우리 팀을 두자. 그게 mesh 도입 결정의 진짜 틀이다.

---

---

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

---

# 8장. 시간·순서·분산 ID — 분산 시스템의 가장 어두운 코너

매년 봄과 가을, 트위터에는 같은 모양의 글이 한 번씩 올라온다고 해보자. "DST(서머타임) 전환 새벽 2시에 우리 cron이 두 번 돌았다", 혹은 "0번 돌았다." 글 아래에는 "또 시작이네"라는 댓글이 줄을 잇는다. 매년, 새로운 백엔드 개발자들이 똑같은 함정에 빠진다 — 시간은 단순해 보이지만 분산 시스템에서는 가장 어려운 질문 중 하나다.

"지금 몇 시야?" 같은 질문에 친구는 손목시계를 보고 답한다. 그런데 분산 시스템에서는 그 질문에 누구도 자신 있게 답하지 못한다. 노드마다 시계가 다 미세하게 어긋나 있고, GPS·atomic clock 같은 하드웨어가 없으면 그 어긋남을 안전하게 줄일 방법도 마땅치 않다. 그렇다면 무엇으로 시간을 대신할 것인가 — 그게 이 챕터의 출발점이다.

Lamport가 1978년에 시작한 사고 실험에서부터, Spanner의 TrueTime이 GPS와 원자시계를 데이터베이스 안으로 끌고 들어온 결정, NTP의 slew와 step이 Snowflake ID에 미치는 영향, 그리고 매년 우리를 흔드는 timezone hell까지 — 한 박자씩 짚어 가자. 마지막엔 한국 토스 SLASH 발표가 짚은 실무 디테일과, 흔히 도입되는 분산 lock(특히 Redis Redlock)의 논쟁점도 함께 본다.

## 1. Lamport의 1978년 — 시간을 인과로 다시 정의하기

분산 시스템에서 시간이 어려운 가장 근본 이유는 단순하다. **두 노드의 시계는 절대 정확히 같지 않다.** NTP가 잘 돌고 있어도 수 ms ~ 수십 ms의 어긋남(skew)이 있고, 데이터센터마다·rack마다 그 어긋남의 모양이 다르다. 그렇다면 노드 A에서 일어난 사건과 노드 B에서 일어난 사건의 "순서"는 어떻게 정의할까?

Lamport는 1978년 *Time, Clocks, and the Ordering of Events in a Distributed System*(P4)에서 이 문제를 정면으로 풀었다. 핵심 통찰은 한 줄이다 — **"실제 시간을 포기하자. 인과만 정의하자."**

이걸 happens-before(→) 관계라고 부른다. 한 노드 안에서 A가 B보다 먼저 일어났다면 A → B. 노드 A가 보낸 메시지를 노드 B가 받았다면, A의 send → B의 receive. 그 외의 사건들은 "concurrent" — 동시에 일어났다고 봐도 된다는 뜻이다. 이렇게 인과로 묶이는 사건들 사이에는 부분 순서(partial order)가 생긴다.

논문의 진가는 그 다음에 있다. Lamport는 happens-before를 보존하는 가장 간단한 시계 — **Lamport timestamp**를 제시했다. 각 노드가 카운터를 하나씩 들고, 이벤트가 일어날 때마다 +1, 메시지를 받을 때는 받은 timestamp와 자기 카운터 중 큰 값 + 1로 갱신한다. 이 단순한 규칙이 **"인과적으로 앞선 사건은 timestamp도 작다"는 성질**을 보장한다.

다만 Lamport timestamp의 한계도 분명하다. **timestamp가 작다고 인과적으로 앞선 것은 아니다.** 두 노드의 카운터가 우연히 같은 값이 될 수 있고, "동시"인 사건들의 순서는 임의로 정해진다. 이걸 더 정밀하게 잡으려면 **vector clock** — 각 노드가 N개 카운터를 들고 다니는 자료구조 — 가 필요하다. Vector clock은 인과를 정확히 잡지만, 노드 수에 비례해 메모리·네트워크 비용이 늘어난다. 그래서 production에서는 N이 10개 이하인 경우 외에는 잘 쓰지 않는다.

기억해 두자. **Lamport의 통찰은 "벽시계를 포기하자, 인과만 잡자"였다.** 이 시각 하나가 그 후 50년의 분산 시스템 이론을 지탱한다.

### Lamport timestamp가 부족한 자리 — 한 사례

Lamport timestamp만으로는 잡지 못하는 자리를 짧게 그려 보자. 노드 A에서 카운터가 5일 때 이벤트 X가 생기고, 노드 B에서 카운터가 5일 때 이벤트 Y가 생긴다. 두 사건은 인과적으로 무관하다. 그런데 Lamport timestamp만 보면 둘 다 5라서 "동시"라고 묶이거나, tie-breaker로 임의 순서가 매겨진다. 이게 진짜 인과적으로 동시인지, 아니면 그냥 카운터가 우연히 같은 값이 된 건지 — Lamport timestamp는 구별하지 못한다.

vector clock은 이 차이를 잡는다. 노드 A의 timestamp는 (A:5, B:0), 노드 B의 timestamp는 (A:0, B:5). 두 vector를 비교하면 어느 한쪽이 다른 쪽을 dominate하지 않는다 — 그래서 진짜 "concurrent"라고 판정할 수 있다. 정확하지만, 노드 수에 비례해 비용이 늘어난다는 함정이 따라온다. 메모리도, 네트워크도, 비교 연산도 모두 N에 비례한다. 그래서 production에서는 노드 수가 작거나 conflict 해소가 정말 중요한 자리(Dynamo의 vector clock, version vector)에만 쓰인다.

## 2. Hybrid Logical Clock — 두 세계의 타협

Lamport는 인과를 잡았고, NTP는 (불완전하나마) 벽시계를 동기화한다. 그런데 production에서는 둘 다 필요할 때가 많다. "사건의 인과적 순서가 맞아야 하는 동시에, 시계도 사람이 읽을 수 있게 사람의 시간과 가까워야 한다." 이 두 요구를 함께 만족하려는 게 **Hybrid Logical Clock (HLC)**다.

HLC는 단순하게 말하면 "Lamport timestamp의 카운터 자리에 NTP의 physical timestamp를 끼워 넣는다"는 발상이다. 각 노드는 (physical time, logical counter) 쌍을 timestamp로 쓴다. 보통은 physical time이 카운터처럼 작동하다가, NTP가 어긋나거나 같은 ms 안에 여러 이벤트가 발생하면 logical counter가 +1씩 늘며 차이를 보정한다.

CockroachDB가 HLC를 골랐다. 이유는 분명하다 — **GPS·atomic clock 같은 특수 하드웨어 없이도 글로벌 분산 SQL DB가 작동해야 했기 때문**이다. HLC는 commodity hardware + NTP만으로 굴러간다. 대신 uncertainty가 더 크다. NTP의 skew가 클수록 HLC의 정확도도 떨어진다.

HLC가 작동하는 모습을 한 줄로 그려 보자. 노드 A의 physical time이 100, logical counter가 0인 상태(100, 0). 같은 ms 안에 이벤트가 또 일어나면 (100, 1), (100, 2)로 logical counter만 늘어난다. 노드 A가 (100, 2) timestamp가 박힌 메시지를 노드 B로 보내고, 노드 B의 physical time이 마침 99 (NTP가 살짝 어긋남)였다면? 노드 B는 받은 (100, 2)와 자기 (99, 0) 중 큰 것 + 1로 갱신해 (100, 3)을 쓴다. 이렇게 **physical time이 비정상이어도 인과는 깨지지 않는다**는 보장을 만들어 낸다. 우아하다.

그렇다면 GPS와 atomic clock을 직접 데이터베이스 안에 박아 넣으면 어떻게 될까? 그게 Spanner의 답이다.

## 3. TrueTime — GPS와 원자시계를 DB 안으로

Google이 2012년 OSDI에 발표한 *Spanner: Google's Globally-Distributed Database*(P5)는 분산 DB 영역에 한 가지 충격적인 결정을 던졌다. **"우리 데이터센터마다 GPS 안테나와 atomic clock을 설치해, 시계 자체를 데이터베이스의 일부로 만든다."**

TrueTime API는 단순하다. `TT.now()`를 호출하면 단순한 timestamp가 아니라 `[earliest, latest]` 구간을 돌려준다. "현재 시간은 이 두 값 사이 어딘가에 있다"는 보장이다. 그 구간의 폭이 uncertainty ε인데, Google 발표 기준 ε는 보통 약 3ms 정도다 (외부 벤치마크가 없어 검증 필요).

이 작은 ε이 외부 일관성(external consistency)이라는 강력한 성질을 만들어 낸다. Spanner는 commit을 끝내기 전에 ε 만큼 기다린다 — "commit wait." 한 트랜잭션 T1이 timestamp `t1`로 commit되고 ε 동안 기다린 뒤, 다른 트랜잭션 T2가 시작하면 T2의 timestamp는 반드시 `t1`보다 크다. 즉 **글로벌하게 "시간상 나중에 commit된 트랜잭션은 timestamp도 나중"**이라는 강한 성질이 보장된다. 이게 글로벌 strong consistency의 비결이다.

DDIA를 다 읽었다고 해도, 동료가 어느 날 "우리 결제 시스템은 strong consistency가 필요한가?"라고 물으면 막힌다. 답은 책 안에 있지만, 책의 단어와 우리 회사의 단어가 다르기 때문이다. Spanner의 3ms commit wait이 우리에게 던지는 질문은 결국 한 줄이다 — "당신 시스템의 그 한 작업, 3ms를 더 기다려도 괜찮은가? 그 대가로 글로벌하게 인과가 보장되는가?"

대부분의 한국 백엔드 시스템은 이 질문에 "기다리지 않아도 된다"고 답한다 — 그래서 우리는 HLC나 Lamport timestamp나, 더 단순하게는 single-leader RDB의 transaction order만으로도 충분히 살 수 있다. 다만 **무엇을 양보했는지 알고 양보하는 것**이 시니어와 그렇지 않은 사람의 차이다.

## 4. NTP slew vs step — Snowflake ID가 죽는 자리

이제 한 박자 내려와서, 실무에서 매일 만지는 자리를 들여다보자. NTP(Network Time Protocol)는 시스템 시계를 외부 source(보통 stratum 1·2 서버)와 맞춰 주는 표준 도구다. 문제는 그 "맞추는 방식"에 두 가지가 있다는 것이다.

- **Slew (천천히 조정).** 시계가 어긋났을 때 단번에 점프하지 않고, 일정 시간 동안 조금씩 빠르게/느리게 흘려서 맞춘다. cron·timer·monotonic counter가 안전하다.
- **Step (한 번에 점프).** 시계가 너무 많이 어긋났을 때 (보통 0.5초 이상) 단번에 새 값으로 바꾼다. 빠르지만, 시계가 역행할 수 있다.

기본 NTP 데몬은 차이가 작으면 slew, 크면 step하는 hybrid를 쓴다. 문제는 step이 일어났을 때다. 시계가 역행하면 — 예컨대 03:00:01에서 02:59:59로 점프하면 — 그 사이에 만들어진 timestamp들이 같은 값 또는 역순이 된다.

이 함정은 Snowflake ID 같은 timestamp-prefix 분산 ID 생성기를 정면으로 흔든다. Twitter의 Snowflake ID 구조를 잠깐 풀어 보면 이해가 쉽다.

```
| 1 bit | 41 bit               | 10 bit       | 12 bit             |
| unused | timestamp (ms 단위) | machine ID  | per-ms sequence    |
```

41bit가 약 69년치 millisecond를 표현하고, 10bit machine ID로 1024개 노드, 12bit sequence로 같은 ms 안에 4096개 ID를 만들 수 있다. **충돌이 안 나는 비결은 시계가 단조 증가한다는 가정**이다. 시계가 1초 역행하면 그 1초 동안 같은 timestamp prefix + 같은 sequence 조합이 다시 나올 수 있어 **ID 충돌**이 발생한다. 운이 나쁘면 production DB의 primary key가 깨진다 — 한 번 겪고 나면 NTP 모니터링이 일상 도구가 된다.

방어법은 분명하다 — **slew만 쓰자**. NTP 데몬에서 step을 비활성화하거나, chrony 같은 모던 도구를 써 step 임계값을 매우 작게 잡는다. 그리고 ID 생성기 코드에 "마지막 timestamp보다 작으면 wait" 로직을 박아 둔다. 잠깐의 추가 latency가 ID 충돌보다는 백 배 낫다.

이 함정이 부록 A의 tribal knowledge 18선 중 첫 번째 항목으로 박힌 데는 이유가 있다. 만나본 사람과 만나보지 못한 사람이 새벽 alert에서 보이는 차이가 크기 때문이다. **NTP는 시계를 맞추지만, 잘못 설정된 NTP는 시계를 무기로 만든다** — 기억해 두자.

## 5. 분산 ID 한 자리에 모아 보기 — Snowflake·ULID·UUIDv7

분산 시스템에서 ID를 어떻게 만들지는 의외로 자주 마주치는 질문이다. RDB의 auto-increment는 single-leader가 아니면 못 쓰고, UUIDv4 같은 random ID는 정렬 가능성이 없어 인덱스 친화적이지 않다. 그렇다면 어떤 선택지가 있을까?

**Snowflake (Twitter, 2010).** 64-bit를 1(reserved) + 41(timestamp ms) + 10(machine ID) + 12(per-ms sequence)로 자른다. 약 3.5조 개의 ID를 시간 순으로 만들어 낸다. 정렬 가능 + 분산 + DB 인덱스 친화적이라는 세 가치를 한 자리에 잡았다. 단 NTP의 step에 취약하다는 함정이 따라온다.

**ULID (2016, Alizain Feerasta).** 128-bit. 앞 48-bit는 millisecond timestamp, 뒤 80-bit는 random. UUID와 동일한 크기이면서 시간 순서를 보장한다. Snowflake보다 충돌 방어가 강하고(80-bit random), machine ID 관리가 필요 없다.

**UUIDv7 (RFC 9562, 2024년 표준화).** 128-bit. ULID와 거의 같은 구조지만 UUID 표준 안에서 정의됐다. 기존 UUID 인프라(라이브러리·DB 컬럼 타입·문자열 표현)를 그대로 쓰면서 시간 정렬을 얻을 수 있다. 2024년 이후 새 프로젝트의 default로 자리 잡는 중이다.

세 가지를 짧은 비교 표로 정리해 보자.

| 축 | Snowflake | ULID | UUIDv7 |
|---|---|---|---|
| 크기 | 64-bit | 128-bit | 128-bit |
| Timestamp 정밀도 | 1ms | 1ms | 1ms |
| Machine ID 필요? | 필요 (10bit) | 불필요 (random) | 불필요 (random) |
| 표준 | Twitter 내부 + 사실상 | 커뮤니티 spec | RFC 9562 (공식) |
| DB 인덱스 친화도 | 매우 높음 | 높음 | 높음 |
| 문자열 표현 | 16진수 (긴 숫자) | 26자 Crockford base32 | 36자 UUID (표준) |
| NTP step 취약도 | 매우 높음 | 낮음 | 낮음 |

회의 자리에서 가장 자주 듣는 질문은 "그래서 뭐 쓸까?"다. 우리 답은 단순하다 — **64-bit가 꼭 필요하지 않다면(저장 비용·네트워크 비용 어쩌면 5% 차이가 진짜 critical하지 않다면) UUIDv7이 가장 안전한 default다.** 이유는 세 가지. ① 공식 RFC. ② UUID 인프라 그대로. ③ NTP step에 강하다. Snowflake는 machine ID 관리·NTP 모니터링이라는 두 운영 비용을 짊어진다는 점을 항상 기억해 두자.

## 6. Timezone Hell — 매년 봄·가을 반복되는 함정

이제 가장 일상적인 자리다. 한국에서 시스템을 만드는데, 사용자는 미국·일본·유럽에서도 접속한다고 해보자. 시간을 어떻게 저장하고 어떻게 보여줄까? 표준 답은 "DB에는 UTC로 저장, 표시는 사용자 timezone으로." 누구나 들어본 답이다. 그런데 이 한 줄에는 함정이 숨겨져 있다.

### 함정 1: legacy DB의 timestamp(timezone 없는 컬럼)

PostgreSQL이라면 `TIMESTAMP`와 `TIMESTAMPTZ`라는 두 자료형이 있다. 비슷해 보여서 처음에는 별 차이가 없을 거라고 생각하기 쉽다. 그런데 **`TIMESTAMP` (timezone 없음)는 "DB가 시간대를 기억하지 않는다"는 뜻**이다. KST로 넣었는지 UTC로 넣었는지 아무도 모른다. application 어딘가에서 가정이 깨지는 순간 모든 시간 데이터가 무의미해진다 — 끔찍한 일이다. 새 프로젝트라면 거의 항상 `TIMESTAMPTZ`를 쓰자.

### 함정 2: DST (서머타임) 전환

매년 봄과 가을, 미국·유럽·호주의 일부 지역에서 시계가 1시간 앞당겨졌다 다시 되돌아간다. 그 결과 — **새벽 2시가 두 번 등장하거나 한 번도 등장하지 않는다.** 이게 정확히 그 시간에 돌도록 잡혀 있는 cron job을 흔든다. "매일 새벽 2시 5분에 돌아라"라고 한 cron이 그날만 2번 또는 0번 돈다. 매년, 어딘가의 백엔드가 이걸로 알람을 받는다.

방어법은 두 가지. ① cron 표현을 "매일 2시 5분"이 아닌 "1시간 간격" 또는 "UTC 기준 시간"으로 바꾼다. ② DST가 없는 timezone(한국은 그 자체로 DST 없음)에 cron을 둔다. 그래도 미국 사용자에게 보여줄 시간이라면 application 레벨에서 timezone 변환을 해야 하니, 그 한 자리는 잘 테스트해 두자.

### 함정 3: 미래 일정은 local time으로 저장

이건 덜 알려진 함정이다. UTC 저장 + local 표시는 "과거 사건"에만 안전하다. **미래에 일어날 일정(예약·예약된 cron)은 정부가 timezone 규칙을 바꿀 수 있어서, UTC로 변환해서 저장하면 위험하다.** 예컨대 "2027년 3월 8일 새벽 2시에 알람"을 UTC로 저장해 두면, 그 사이에 미국 정부가 DST를 폐지하면 알람이 1시간 어긋난다. 미래 일정은 (`local time`, `timezone name`) 쌍으로 저장하고, 알람 시점에 변환하는 편이 낫다.

### 함정 4: leap second — 매 몇 년에 한 번 1초가 추가된다

마지막 함정 하나만 더. **leap second**는 지구 자전 속도가 미세하게 느려지는 걸 보정하려고 UTC에 1초를 추가하는 작업이다. 2012년·2015년·2016년·2017년이 가장 최근 사례들이고, 이때마다 일부 인터넷 서비스가 흔들렸다. 23시 59분 60초라는 한 번도 안 쓰는 시각이 등장하기 때문이다. 일부 라이브러리는 이걸 처리 못하고 죽고, 어떤 시스템은 시계를 step해서 NTP step 함정에 또 빠진다. 다행히 2035년부터 leap second가 폐지될 예정이라(검증 필요 — IERS 발표), 이 함정은 점차 사라질 거다. 다만 그때까지는 **leap second smearing**(Google·AWS가 채택한 12시간에 걸쳐 부드럽게 1초를 흘리는 기법)을 쓰는 NTP 서버를 골라 두는 편이 낫다.

### 한국 사례 — 토스 SLASH 22 "분산 시스템에서 시간 다루기"

이 timezone hell을 한국 백엔드 시각에서 가장 정직하게 짚은 발표가 있다. **토스 SLASH 22의 "분산 시스템에서 시간 다루기"**다. OKKY와 트위터에서 발표 후 "이게 가장 현실적인 발표였다"는 반응이 자주 인용된다(community 패턴 3).

발표는 한국 결제 시스템에서 만난 구체적 문제들을 짚는다. 일본 트래픽이 섞인 hourly job이 KST 기준과 JST 기준에서 3시간 다른 결과를 내는 사고, leap second(2016년·2017년)가 거래 timestamp에 미친 영향, 그리고 IANA timezone database 업데이트가 production 컨테이너에 안 들어가 있어서 한 국가의 timezone 변경이 반영 안 됐던 사례 등. 영어책에서는 거의 안 다루는 자리들이다.

발표가 짚는 한 가지 메시지를 빌리자면 — **"한국 회사라고 KST만 다룬다고 생각하는 순간이 가장 위험하다."** 결제 회사에는 일본 사용자가 들어오고, 게임 회사에는 글로벌 트래픽이 섞이고, 광고 회사에는 유럽 사용자의 click이 새벽에 쌓인다. timezone을 application 레벨에서 일관되게 다루는 표준 라이브러리(Java의 `ZonedDateTime`, JavaScript의 `Temporal` proposal, Python의 `zoneinfo`)를 처음부터 골라 두자. 익숙해진 뒤 바꾸려 하면 마이그레이션 비용이 만만치 않다.

기억해 두자. **시간은 단순해 보이지만 분산 시스템에서는 가장 비싼 영역이다.** 그리고 한국 백엔드는 한국 기준에 미국·일본·유럽 사용자가 섞이는 일이 흔해서 timezone hell을 한 번 정도는 꼭 거친다. 거치기 전에 한 챕터 펴 두는 정도의 보험을 들어 두는 편이 낫다.

## 7. 분산 lock — Redis Redlock 논쟁

시간 다음의 사촌 주제로 분산 lock도 짧게 짚어 두자. "두 노드가 동시에 같은 자원을 만지면 안 된다"는 요구는 분산 시스템에 흔하다. 카드 결제 idempotency, 재고 차감, leader election. Redis Redlock·ZooKeeper·etcd가 대표 도구다.

**Redis Redlock**은 Salvatore Sanfilippo(antirez)가 제안한 알고리즘이다. N개의 독립 Redis 인스턴스에 lock을 동시에 시도하고, majority가 동의하면 lock 획득. 단순해 보이지만 — Martin Kleppmann이 2016년에 "이 알고리즘은 wall clock에 너무 의존해 안전하지 않다"는 비판을 공개 글로 올리면서 큰 논쟁이 됐다 (검증 필요 — 두 글의 원문을 찾아 읽어 보길 권한다).

Kleppmann의 비판은 두 줄로 요약된다. ① Redlock은 노드 간 시계가 어긋나지 않는다고 가정하는데, NTP step 같은 일이 일어나면 lock이 두 노드에서 동시에 획득될 수 있다. ② 자원 보호의 진짜 안전성을 원한다면 fencing token (단조 증가하는 lock ID)을 자원 쪽에서 검증해야 한다. antirez는 "lease 기반 lock은 어차피 단순 race condition 외에는 안전하지 않다, 그 한계 안에서 Redlock은 충분히 실용적이다"로 반박했다.

결론을 강제로 짓지는 말자. **production에 분산 lock이 정말 필요한지부터 묻는 편이 낫다.** 많은 경우 lock 없이도 풀 수 있다 — 멱등성 키, 단일 leader, optimistic concurrency control. 정말 필요하다면 ZooKeeper나 etcd 같은 합의 기반 도구가 Redis lock보다 안전한 default다. Redis lock을 쓸 때는 "여기 lock이 풀려도 데이터 정합성이 깨지지 않는다"는 자기 검증이 한 줄 필요하다. 결제 같은 critical path에서는 거의 항상 fencing이 함께 가야 한다.

## 8. 의사결정 트리 — 이 데이터에 진짜 시간이 필요한가

여기까지 따라온 우리에게 필요한 도구는 — "이 데이터에 진짜 시간 보장이 필요한가, 아니면 순서만 있으면 되는가"를 묻는 짧은 트리다. 회의 자리에서 한 박자 안에 던질 수 있는 질문 5개로 정리해 보자.

1. **이 데이터에 글로벌 strong consistency가 필요한가?** 결제 audit·금융 거래라면 yes — TrueTime 가진 Spanner나 그에 준하는 도구. 거의 모든 경우 no — 다음 질문으로.
2. **인과 순서만 보장되면 충분한가?** 메시지 ordering, audit log라면 yes — Lamport timestamp나 HLC면 충분.
3. **단일 region 안에서만 순서가 필요한가?** 한국 한정 서비스라면 yes — single-leader RDB의 transaction order로 충분. 분산 lock도 필요하지 않을 가능성이 높다.
4. **ID에 시간 prefix가 필요한가?** Yes라면 UUIDv7 default. NTP 모니터링 필요. No라면 UUIDv4면 충분 — random ID가 가장 단순하다.
5. **미래 시점 일정을 다루는가?** Yes라면 (local time, timezone name) 쌍으로 저장. UTC 변환은 알람 시점에. timezone database 업데이트를 자동화한다.

이 5개 질문에 답할 수 있으면 시간이라는 어두운 코너에서 길을 잃지 않는다.

## 9. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 시간이라는 까다로운 영역의 지형이 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **Lamport의 통찰** — 벽시계를 포기하고 인과만 잡자. happens-before가 분산 시스템 50년의 토대다.
- **TrueTime의 결정** — GPS·atomic clock을 데이터베이스 안으로. ε~3ms commit wait이 글로벌 strong consistency의 비용이다. 우리 대부분에게는 과한 도구지만, 무엇을 양보했는지 알고 양보하는 게 중요하다.
- **HLC는 commodity hardware로도 굴러간다.** CockroachDB가 골랐다. TrueTime보다 ε가 크지만, 그 대가로 어떤 데이터센터에서도 작동한다.
- **NTP step은 시계를 역행시킨다.** Snowflake ID의 가장 큰 적이다. slew 권장 + ID 생성기에 wait 로직. 부록 A의 tribal 1번 항목으로 다시 만난다.
- **분산 ID의 모던 default는 UUIDv7.** Snowflake도 좋지만 NTP 운영 비용을 짊어진다는 점, 항상 기억해 두자.
- **Timezone hell은 매년 반복된다.** UTC 저장 + 사용자 timezone 표시 + 미래 일정은 (local, timezone name) 쌍. DST 영향 받는 cron은 호출 표현 자체를 손본다. 토스 SLASH 22 발표가 한국 백엔드의 현실 카탈로그다.
- **분산 lock이 정말 필요한지부터 묻자.** Redlock은 NTP step에 취약하다. critical path라면 fencing token + 합의 기반 도구(ZooKeeper·etcd)가 default다.

다음 장(9장)에서는 보안 — 인증·인가·secret·망분리 — 을 짚는다. 보안은 모든 빌딩 블록 위에 깔리는 통제 평면(control plane)이고, 한국 백엔드에서는 망분리·전자금융감독규정 같은 한국 특유의 맥락이 가장 두드러지는 자리다. 시간이 분산 시스템의 가장 어두운 코너였다면, 보안은 가장 약한 고리다. 옆에 두고 같이 짚어 보자.


---

# 9장. 분산 시스템의 보안 — 인증·인가·secret·망분리

팀 슬랙에 누군가 깃허브 public repo에 `.env`를 푸시했다는 알림이 떴다고 해보자. 그 파일 안에는 AWS access key가 통째로 들어 있다. 5분 안에 누군가 그 키로 EC2를 켜고 비트코인을 채굴한다. 청구서는 다음 날 아침에 도착한다 — 만 달러 단위로.

이런 일이 흔할까? 사실 매우 흔하다. GitHub에는 매일 수천 개의 secret이 실수로 push된다. 자동 봇이 GitHub의 공개 push를 실시간으로 스캔해, 노출된 AWS key·GCP service account·Stripe key를 분 단위로 채굴한다. **secret을 코드에서 분리하지 않은 한 줄의 게으름이 회사를 흔든다.**

보안은 production의 가장 약한 고리고, 우리가 매일 만지는 영역이다. 그런데도 한국 시스템 디자인 책 대부분이 보안을 "별도 책의 주제"로 미루거나 한 페이지로 처리한다. 분산 환경의 위협 모델, 인증·인가의 표준 패턴, secret 관리, 한국 망분리 환경, Zero Trust — 빌딩 블록의 일부로 한 박자씩 짚어 가자. 마지막엔 모든 새 endpoint 설계 시 자동으로 던질 5가지 질문을 손에 챙겨 두자.

## 분산 환경 위협 모델 — 3축으로 가르기

분산 시스템의 보안을 다룰 때 가장 먼저 그릴 그림이 위협 모델이다. 누가 누구에게 "나는 X다"라고 증명해야 하는지를 명확히 가르는 작업. 크게 세 축이 있다.

**1. Service-to-service (내부).** 우리 service A가 service B를 호출한다. A는 B에게 "나는 우리 회사의 신뢰받는 service"임을 증명해야 한다. mTLS, SPIFFE, service mesh가 이 영역.

**2. User-to-service (외부).** 사용자가 우리 API를 호출한다. 사용자는 우리에게 "나는 user 12345"임을 증명해야 한다. OAuth2/OIDC, JWT, session token이 이 영역.

**3. Admin-to-system (운영).** 운영자가 인프라에 접근한다. 운영자는 인프라에게 "나는 인증된 staff이고, 이 권한이 있다"를 증명해야 한다. SSO, MFA, JIT(Just-In-Time) access가 이 영역.

이 세 축의 신뢰 경계와 공격 표면이 모두 다르다. 그래서 한 가지 도구로 해결되지 않는다. 예를 들어 OAuth2는 (2)에는 표준이지만 (1)·(3)에는 부적합. mTLS는 (1)에는 표준이지만 (2)에는 사용자 경험 측면에서 거의 안 쓴다.

| 축 | 신뢰 경계 | 표준 도구 | 공격 표면 |
|----|---------|----------|---------|
| Service-to-service | 회사 내부 망 | mTLS, SPIFFE, service mesh | network sniff, lateral movement |
| User-to-service | 인터넷 ↔ API | OAuth2, JWT, session token | credential theft, replay, CSRF |
| Admin-to-system | staff ↔ 인프라 | SSO, MFA, JIT, audit log | insider threat, key leak |

각 축마다 다른 도구가 들어간다는 사실을 머릿속에 그려 두자. 보안 도입 시 첫 질문은 "어느 축의 위협이 우리에게 critical한가"이다.

## 인증·인가 두 단계 구분 — Authentication vs Authorization

용어부터 정리하자. 비슷한 발음 때문에 자주 혼동된다.

- **Authentication (AuthN, 인증):** "나는 누구다"를 증명. ID/password, OAuth login.
- **Authorization (AuthZ, 인가):** "나는 이걸 할 권한이 있다"를 증명. RBAC, ABAC, scope.

이 두 단계는 별개로 처리되는 편이 낫다. 인증은 한 번만 (login 시점), 인가는 매 요청마다 검증.

### OAuth2/OIDC 표준 흐름

웹·모바일 인증의 사실상 표준이 OAuth2 (RFC 6749)와 그 위의 OpenID Connect다. 흐름 4가지를 짧게 정리하자.

**1. Authorization Code Grant + PKCE (권장).** 가장 안전한 흐름. 모바일·SPA에 사용. PKCE(Proof Key for Code Exchange)는 authorization code 탈취 공격을 막는다.

```
1. User → Authorization Server: "log in" + PKCE challenge
2. Authorization Server → User: "이 client에 이 권한 줄까?"
3. User → Authorization Server: "yes"
4. Authorization Server → Client: authorization code
5. Client → Token Server: code + PKCE verifier
6. Token Server → Client: access_token + refresh_token
```

**2. Client Credentials.** Service-to-service에 사용. user 없음, client_id + client_secret으로 직접 token 받음.

**3. Implicit (Deprecated).** SPA에서 한때 쓰였으나 보안 위험으로 사실상 폐기. Authorization Code + PKCE로 대체.

**4. Resource Owner Password Credentials (Deprecated).** username + password를 client가 받음. 매우 위험. legacy migration용으로만 한정.

새 시스템이라면 **무조건 Authorization Code + PKCE**가 답이다. 다른 흐름은 legacy 호환 또는 service-to-service(Client Credentials)로 한정.

### JWT — 검증·만료·rotation

OAuth2의 access_token은 보통 **JWT** (JSON Web Token, RFC 7519) 포맷이다. 다음과 같이 생겼다.

```
header.payload.signature

eyJhbGciOiJIUzI1NiJ9.
eyJzdWIiOiIxMjM0NSIsImV4cCI6MTYzMjQwMDAwMH0.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

3개 부분으로 나뉘고, signature가 위변조를 막는다. 자체 검증이 가능해 server-to-server 통신에서 stateless 인증이 가능하다.

JWT의 함정은 두 가지다.

**1. 만료(expiry) 없는 token.** JWT에 `exp` claim을 안 넣으면 영원히 유효하다. 한 번 탈취당하면 영영 막을 수 없다. 그래서 access_token은 보통 **15분~1시간** 짧게.

**2. Refresh token rotation.** access_token이 짧으면 사용자가 자주 로그인해야 한다. 그래서 refresh_token을 함께 발급해 자동 갱신. 그런데 refresh_token이 탈취되면 새 access_token을 무한히 발급 가능. 대처는 **refresh token rotation** — refresh로 새 access를 받을 때마다 refresh 자체도 바꾼다. 옛 refresh는 즉시 invalidate.

```
초기: refresh_v1 발급
사용: refresh_v1 → access_v1 + refresh_v2 발급, refresh_v1 invalidate
도난: 공격자가 refresh_v1 사용 시도 → invalidate된 토큰 → 자동 차단 + 사용자 모든 세션 강제 로그아웃
```

이 패턴이 OAuth2 Best Current Practice (RFC 8252)의 표준이다. 한국 핀테크에서는 default로 적용된다.

### RBAC vs ABAC

인가(authorization)는 두 모델이 있다.

**RBAC (Role-Based).** "user에게 role을 부여, role마다 권한 set." 단순하고 직관적. user_id → role → permissions. Spring Security, Django, Rails의 기본 모델.

**ABAC (Attribute-Based).** "user의 attribute + resource의 attribute + context로 permission 결정." 더 유연하지만 복잡. AWS IAM의 condition, Open Policy Agent (OPA)가 ABAC.

대부분의 시스템에는 RBAC로 시작하고, 복잡한 조건(시간·지역·자원 attribute)이 필요해질 때 ABAC를 추가한다. 처음부터 ABAC 전체를 깔면 운영 부담이 크다.

## Service-to-Service 신뢰 — mTLS와 SPIFFE

내부 service 간 통신은 다른 모델이 필요하다. OAuth2 token을 service 간에 흘리는 건 어색하고 위험하다. 그래서 등장한 표준이 **mTLS** (mutual TLS)다.

TLS는 보통 client가 server를 검증한다(우리가 브라우저에서 https 사이트 접속 시). mTLS는 server도 client를 검증한다. 양쪽이 서로의 인증서를 제시하고 검증.

```
service A → service B: 내 cert 보낸다 + B의 cert 검증
service B → service A: 내 cert 보낸다 + A의 cert 검증
양쪽 OK → secure channel
```

이 모양은 다음을 약속한다.

- **상호 인증.** A는 정말 B와 통신 중이라는 확신, B도 마찬가지.
- **암호화.** 중간에서 sniff해도 내용을 못 본다.
- **무결성.** 메시지 위변조가 불가능.

mTLS의 운영 부담이 크다. 모든 service에 인증서를 발급·갱신·revoke해야 한다. 이걸 자동화하는 표준이 **SPIFFE/SPIRE**다.

**SPIFFE** (Secure Production Identity Framework For Everyone)는 service identity를 표준화한다. 각 service에 `spiffe://example.org/ns/prod/sa/payment` 같은 URI를 부여하고, 그 URI를 cert에 박는다. **SPIRE**가 이 cert를 자동 발급·갱신.

그리고 **service mesh** (Istio, Linkerd)가 mTLS를 자동화한다. application code는 plain HTTP를 쓰고, sidecar proxy가 mTLS를 처리. 6장 로드 밸런서·서비스 메시 챕터에서 이미 그 trade-off를 다뤘다.

## Secret 관리 — Vault·KMS의 진짜 운영 과제

서두의 `.env` 사고로 돌아오자. secret을 안전하게 다루는 표준은 무엇인가?

### 평문 secret 금지

다음은 모두 끔찍한 패턴이다.

- **`.env` 파일을 git에 commit.** GitHub 검색에서 가장 자주 노출되는 파턴.
- **환경변수에 직접 박기.** docker-compose, K8s manifest에 평문 적기.
- **로그에 secret 출력.** 디버깅용 `print(config)`가 production에서 통째로 secret을 CloudWatch에 보낸다.
- **에러 메시지에 secret 포함.** stack trace가 secret과 함께 사용자에게 표시.

이 모양들은 secret이 어딘가에 영구적으로 남게 만든다. 한 번 노출되면 회수 불가능. **rotation해야 한다.**

### 표준 도구

- **HashiCorp Vault.** open source의 사실상 표준. dynamic secret, KMS, transit encryption까지. 운영 부담 있음.
- **AWS Secrets Manager.** managed. AWS 친화 팀 default.
- **AWS Parameter Store.** 더 가벼움. 작은 시스템에 적합.
- **GCP Secret Manager.** GCP의 동등 도구.
- **KMS (Key Management Service).** 암호화 key 자체를 관리. 다른 secret 도구의 backbone이 되기도.

이 도구들이 약속하는 핵심 두 가지가 **rotation과 revocation 자동화**다.

**Rotation.** 매 30일·90일마다 secret을 자동으로 바꾼다. 옛 secret이 노출되어도 30일 후엔 무효. 사람이 손으로 돌리던 시절에는 "이번 분기 secret rotation 안 함" 같은 상태가 흔했다. 자동화가 이걸 푼다.

**Revocation.** secret이 노출된 게 발견되면 즉시 invalidate. application들이 자동으로 새 secret을 fetch.

이 두 자동화가 안 되는 secret 도구는 사실 의미가 적다. 평문보다 약간 나은 정도. 새 시스템 도입 시 이 두 능력을 1순위로 확인하는 편이 낫다.

### Application 수준의 패턴

application 코드에서 secret을 안전하게 가져오는 패턴.

```python
# 나쁜 예 — 환경변수 직접 사용
db_password = os.environ['DB_PASSWORD']  # 어디서 왔는지 추적 불가

# 좋은 예 — Vault에서 매 요청 또는 lease로 받기
db_password = vault.read('secret/database')['password']

# 더 좋은 예 — IAM 기반 짧은 lease
db_creds = vault.read_aws_database_credentials('db-role-prod')
# db_creds는 1시간 lease, 자동 rotation
```

가장 안전한 모양이 **dynamic secret**이다. application이 시작할 때 1시간짜리 short-lived credential을 발급받는다. 시간이 지나면 자동 만료. 한 application이 노출돼도 1시간 후엔 그 credential이 무효.

## 한국 환경의 망분리 (한국 2·9)

한국 금융·공공·일부 대기업에는 다른 나라에 없는 보안 요건이 있다. **망분리**다.

**전자금융감독규정**은 금융권에 인터넷망과 업무망을 물리적으로 분리할 것을 요구한다. 즉 결제·송금·계좌 처리하는 시스템은 인터넷에 직접 노출되면 안 된다. 공공기관·일부 대기업도 비슷한 요건이 있다.

이 요건이 클라우드 아키텍처에 미치는 영향이 크다.

**1. Public cloud 그대로 못 쓴다.** AWS·GCP의 일반 region은 인터넷 연결이 default. 망분리 환경에 그대로 쓸 수 없다.

**2. Hybrid cloud 모델 등장.** 인터넷 노출 부분은 public cloud, 내부 처리 부분은 private cloud 또는 자체 IDC. AWS Outposts, GCP Anthos, Azure Stack이 이 시나리오.

**3. VPN / Direct Connect 필수.** public cloud와 internal 망 연결을 위해 dedicated network 연결.

**4. CI/CD 분리.** 코드를 internal 망에 배포하기 위한 별도 pipeline. 인터넷에서 가져온 dependency가 내부 망에 들어오는 과정 검증.

한국 핀테크의 대표 사례 셋을 짚자.

**토스 hybrid cloud.** 토스페이먼츠는 public(AWS) + private(자체) 혼합. critical한 결제 코어는 private, 외부 인증·통신은 public. 이 결정이 progressive rollout, multi-region DR 같은 운영 패턴까지 영향을 준다.

**LINE 자체 IDC.** LINE은 도쿄·한국에 자체 IDC를 운영. 메시징·사용자 데이터가 외부 cloud에 안 나간다. 글로벌 서비스에 자체 인프라 운영 능력이 있는 회사의 모델.

**카카오뱅크 보안 architecture.** 카카오뱅크는 99.99% SLA + 망분리 + 24/7 운영. 메인프레임 → MSA 전환 중에도 망분리 요건을 유지. tech.kakaobank.com에 일부 architecture 공개.

한국 백엔드가 글로벌 회사로 이직하면 가장 낯선 게 망분리가 없다는 점이다. 반대로 글로벌 회사가 한국 진출할 때 가장 큰 장벽이 망분리 대응이다.

> 💡 한국 환경 한 줄 가이드 — **금융·공공·대기업 안의 시스템이라면 망분리 요건을 먼저 확인하자.** 그 요건이 아키텍처의 큰 차원(public vs private, cloud vs IDC)을 결정한다. AWS Outposts·자체 IDC가 단순 선택지가 아니라 필수가 되는 경우가 흔하다.

## Zero Trust — 신뢰 경계가 사라진 시대

전통적인 보안 모델은 **perimeter security(경계 기반 보안)**다. "방화벽 안은 안전, 밖은 위험"이라는 모양. 회사 망 안에 들어온 호출은 신뢰, 밖에서 온 호출은 검증.

이 모델이 깨졌다. 클라우드, 모바일, SaaS, 원격 근무가 perimeter를 사라지게 했다. 우리 직원의 노트북은 카페 wifi에서, 가정 인터넷에서, 호텔에서 모든 곳에서 회사 system에 접속한다. "회사 망 안"이라는 개념 자체가 모호하다.

**Zero Trust**는 이걸 정면으로 받아들인다. "기본은 불신, 모든 호출에 인증을 강제."

Google이 2009년 Operation Aurora 사건 이후 도입한 **BeyondCorp** 모델이 Zero Trust의 사실상 시작이다. 핵심 원칙은 다음과 같다.

- **모든 호출에 인증.** 회사 망 안에서 온 호출이라도 검증.
- **device trust + user trust 결합.** 사용자 ID만이 아니라 device의 무결성도 검증.
- **least privilege.** 작업에 필요한 최소 권한만 부여.
- **continuous verification.** 한 번 인증한 session도 주기적 재검증.

한국 백엔드에서도 Zero Trust 채택이 늘고 있다. 토스·카카오 일부 시스템에 BeyondCorp 모델이 도입된 사례가 있다. perimeter security의 한계를 절감한 후 자연스럽게 가는 방향이다.

## API Gateway와 백엔드의 책임 분리

6장에서 다룬 API Gateway가 보안에도 핵심 역할을 한다. 책임 분리의 모양을 그려 두자.

**API Gateway 책임:**
- Rate limiting (DDoS 1차 방어)
- WAF (SQL injection, XSS 패턴)
- 인증 위임 (OAuth2 검증, JWT verification)
- TLS termination (or pass-through)

**Backend 책임:**
- 비즈니스 인가 (이 user가 이 resource를 정말 볼 수 있는가)
- 도메인 룰 (잔고 검증, 재고 검증)
- 감사 로그 (누가 무엇을 했는지 audit)

이 분리가 왜 중요한가? **gateway는 평면적 룰(이 user는 이 endpoint 호출 가능)에 강하고, backend는 도메인 룰(이 user는 이 specific 자원에 접근 가능)에 강하다.** 둘을 안 가르고 backend에 다 박으면, backend 코드가 보안 로직으로 비대해진다. 둘을 안 가르고 gateway에 다 박으면, gateway가 도메인을 알아야 해서 backend와 결합도가 높아진다.

## DB 접근 통제 — Least Privilege

application이 DB에 접근할 때 항상 admin 권한으로 접근하는 경우가 많다. 끔찍하다. application이 SQL injection으로 침해당하면 DB 전체가 노출된다.

표준 패턴은 **least privilege**다. application별로 별도 DB user를 만들고, 그 user에게 최소 권한만 부여.

```sql
-- 결제 service는 결제 테이블만, 그것도 SELECT/INSERT만
CREATE USER payment_app;
GRANT SELECT, INSERT ON payments TO payment_app;
GRANT SELECT ON users TO payment_app;

-- 다른 테이블엔 접근 불가
```

추가로 **IAM 기반 DB auth**가 secret 없이 접근하는 모양을 가능하게 한다.

- **AWS IAM DB auth.** RDS Postgres·MySQL에서 IAM role로 인증. password 없음.
- **GCP Cloud SQL IAM.** 동등 기능.

이 모양이 가능한 환경에서는 DB password를 secret store에 두지 않아도 된다. application의 IAM identity가 곧 DB 접근 권한이 된다.

## 비밀번호·PII 저장

사용자 password와 PII (Personally Identifiable Information)는 별도 보호가 필요하다.

### Password 저장

평문 저장은 절대 금지. hash 저장이 표준인데, 일반 hash(MD5·SHA-256)는 빠르게 brute force 가능. 그래서 **bcrypt, scrypt, argon2** 같은 의도적으로 느린 hash를 쓴다.

```python
import bcrypt

# 저장 시
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
# rounds=12 → 2^12=4096회 반복. 한 password hash에 ~200ms.

# 검증 시
if bcrypt.checkpw(password.encode(), hashed):
    # OK
```

bcrypt의 12 round가 2026년 표준. CPU가 발전하면 14·16으로 올라갈 것. argon2는 GPU 공격에도 강하지만 의존성이 무거워, 새 시스템 외에는 bcrypt가 default.

**rainbow table 방어:** salt가 hash마다 다르게 박혀, 미리 계산된 rainbow table 공격 불가. bcrypt는 salt를 자동 처리.

### 한국 개인정보보호법 맥락

한국에서는 **주민번호·신용정보**가 별도 강력 보호 대상이다. 개인정보보호법 + 신용정보법.

- 주민번호: 저장 자체가 제한. 꼭 필요한 경우만, 별도 암호화(AES-256+) + 접근 통제.
- 신용정보: 신용정보법으로 별도 보호. 일반 PII보다 강한 통제.
- 일반 PII (이름·이메일·전화): encryption at rest + in transit, 접근 로그.

한국 핀테크에서 새 시스템 만들 때 가장 먼저 챙길 게 이 법적 요건이다. "그냥 PII 저장" 같은 단순한 답은 한국에서 불법이 될 수 있다.

## OWASP API Security Top 10 — 백엔드 시각 3가지

OWASP가 API 보안 위협 Top 10을 정기적으로 발표한다. 그 중 백엔드 개발자가 가장 자주 만나는 3가지를 짚자.

**1. Broken Object Level Authorization (BOLA).** 가장 흔한 함정. user A가 user B의 자원에 접근할 수 있는 endpoint. `GET /users/123/orders`에서 123이 자기 user_id가 아니어도 조회 가능한 경우.

```python
# 나쁜 예 — 인증만 검증, 인가는 누락
def get_orders(user_id):
    if not is_authenticated():
        return 401
    return db.query("SELECT * FROM orders WHERE user_id=?", user_id)

# 좋은 예 — 인가 검증 추가
def get_orders(user_id):
    if not is_authenticated() or current_user.id != user_id:
        return 403
    return db.query("SELECT * FROM orders WHERE user_id=?", user_id)
```

**2. Mass Assignment.** request body를 그대로 ORM에 넣으면 위험한 필드까지 갱신. 예를 들어 `User` 객체에 `is_admin` 필드가 있는데, 사용자가 자기 프로필 update 요청에 `is_admin=true`를 끼워 보내면?

```python
# 나쁜 예
def update_user(req):
    user.update(**req.json())  # 사용자가 보낸 모든 필드 적용

# 좋은 예 — allowlist
def update_user(req):
    allowed = {'name', 'email', 'phone'}
    updates = {k: v for k, v in req.json().items() if k in allowed}
    user.update(**updates)
```

**3. Server-Side Request Forgery (SSRF).** 사용자가 보낸 URL을 server가 그대로 fetch하면, 내부 망의 sensitive endpoint(`http://169.254.169.254/`의 AWS metadata service)에 접근 가능.

```python
# 나쁜 예
url = request.json['callback_url']
response = requests.get(url)

# 좋은 예 — allowlist + 내부 IP 차단
if not is_allowed_domain(url) or is_internal_ip(url):
    return 400
```

이 셋만 챙겨도 한국 백엔드에서 자주 만나는 보안 사고의 대부분이 막힌다.

## 사고 사례 — 2022 카카오 SK C&C 화재

한국 보안 사례 중 가장 잘 알려진 게 2022년 10월 카카오 데이터센터 화재다. SK C&C 판교 IDC에 화재가 나서 카카오의 다수 서비스가 멈췄다. 보안 사건은 아니지만, **신뢰성·보안의 경계**에 있는 사고였다.

이 사고에서 드러난 보안·운영 관점의 교훈 몇 가지.

1. **자체 IDC 단일 의존성의 위험.** 다른 region·다른 데이터센터에 hot standby가 없었다. multi-region이 이후 한국 기업의 표준 화두로 격상.
2. **DR(Disaster Recovery) 계획 vs 실제 실행 gap.** DR 계획은 있었으나 실제 실행은 며칠 걸렸다. 정기 DR drill이 없으면 계획서는 종이일 뿐.
3. **secret·인증서의 multi-region 분배.** 데이터센터가 죽으면 그 안의 secret도 함께 죽는다. KMS·Vault의 multi-region 복제가 critical.

이 사고 이후 한국 기업의 multi-region·multi-cloud 채택이 빠르게 늘었다. 보안과 신뢰성은 한 차원에서 만난다.

## 모든 새 endpoint에 던질 5가지 질문

이 챕터의 핵심 통찰을 5가지 질문으로 압축하자. 새 endpoint를 설계할 때 자동으로 떠올리는 5가지다.

1. **인증?** 누가 호출하는지 어떻게 검증하는가? OAuth2/JWT, mTLS, IAM 중 무엇?
2. **인가?** 인증된 사용자가 이 자원에 접근할 권한이 있는가? object level까지 검증하는가?
3. **Secret 어디서 어떻게?** 평문 박지 않았는가? secret store에서 dynamic하게 가져오는가?
4. **Rotation?** secret이 30일·90일마다 자동 갱신되는가?
5. **Audit log?** 누가 무엇을 언제 했는지 기록되는가? 사후 추적 가능한가?

이 다섯이 머릿속에 있으면 코드 리뷰에서 "이 endpoint는 BOLA 검증 빠진 것 같은데?", "이 secret은 어디서 왔어?" 같은 질문이 자연스럽게 나온다. **그리고 그 다섯 질문이 자동으로 떠오를 때, 0장에서 약속한 6번째 약속 — "보안이 별도 영역이 아니라 모든 빌딩 블록 위에 깔린 통제 평면(control plane)임이 손에 박힌다" — 의 회수가 여기서 일어난다.**

## Callback 예고

보안은 이 책의 후속 챕터에서 다음 자리에 핵심으로 다시 등장한다.

- **19장 결제·금융.** 결제 audit chain·blameless postmortem이 9장의 control plane(인증·인가·secret·audit log) 위에서 작동.

6장 로드 밸런서·서비스 메시에서 다룬 mTLS·service mesh도 9장의 service-to-service 위협 모델 위에서 작동하는데, 이건 6장에서 이미 함께 짚었다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 분산 시스템 보안의 지형이 손에 잡혀 있다. 3축 위협 모델(service-to-service·user-to-service·admin-to-system), OAuth2/OIDC·JWT·RBAC/ABAC, mTLS·SPIFFE·service mesh, Vault·KMS의 rotation·revocation, 한국 망분리(전자금융감독규정 + 토스·LINE·카카오뱅크 사례), Zero Trust·BeyondCorp, API Gateway 책임 분리, OWASP API Top 10, 그리고 2022 카카오 화재의 교훈까지가 한 묶음이다.

기억해두자. 보안은 production의 가장 약한 고리고, 우리가 매일 만지는 영역이다. `.env`를 git에 push하는 한 줄 게으름이 회사를 흔든다. secret을 코드에서 분리하고, 모든 endpoint에 5가지 질문(인증·인가·secret·rotation·audit)을 자동으로 던지는 습관이 우리 시스템의 1번 안전망이다.

여기까지가 1부 빌딩 블록의 끝이다. 다음 10장부터는 2부 — 부품들을 안전하게 엮는 **분산 시스템 패턴**으로 들어간다. 멱등성·재시도·서킷 브레이커가 첫 챕터다. 우리가 1부에서 손에 쥔 부품들이 어떤 규칙으로 조립될 때 production에서 살아남는지, 함께 짚어 보자. 이 챕터의 보안 통찰이 2·3부 모든 시스템 아래에 control plane으로 깔린다.

---

# 2부. 분산 시스템 패턴 — 빌딩 블록을 조립하는 규칙

> 1부의 부품들을 어떻게 엮어 분산 시스템의 정합성·확장성·내구성을 만드는가.
>
> 멱등성·Saga·합의·샤딩·rate limit·관측성·데이터 파이프라인 — 6개 패턴이 부품 위에 깔리는 조립 규칙이다. "실패는 정상"이라는 인지가 코드 작성 습관으로 박히는 자리.

---

# 10장. 멱등성·재시도·서킷 브레이커 — 실패를 가정한 통신

결제 시스템에서 "재시도"라는 단어는 위험하다. 어떤 사용자가 카드 결제를 누른다. 응답이 안 온다. 답답해서 한 번 더 누른다. 그런데 사실은 첫 번째 결제는 카드사에서 처리됐고, 단지 응답이 우리 서버에 도착하기 전에 timeout이 났을 뿐이다. 두 번째 요청도 카드사로 가서 또 처리된다. 사용자는 같은 금액을 두 번 낸다.

이 사고가 일어나는 순간 누구도 정상이 아니다. 사용자는 카드 명세서를 보고 분노하고, 운영자는 환불을 어떻게 처리할지 고민하고, 결제팀은 "왜 idempotency를 안 챙겼나"라는 회고를 쓴다. 사실 문제의 뿌리는 한 가지다 — **분산 시스템에서 모든 network 호출은 언젠가 실패한다.** 그 사실을 코드로 표현하지 않으면, 실패가 사용자의 카드로 전가된다.

분산 시스템에서 모든 network 호출은 언젠가 실패한다. 그 사실을 코드로 표현하면 어떤 모양이 되는가 — 멱등성(idempotency), 재시도(retry)·백오프·jitter, 서킷 브레이커(circuit breaker), 격벽(bulkhead), 그리고 timeout. 다섯 부품을 함께 깔면, 같은 사용자가 한 번 누른 결제를 두 번 처리하는 사고가 일어나지 않게 된다. 한 박자씩 짚어 보자.

## 분산 시스템 8가지 거짓말 — 우리가 가진 잘못된 직관

Sun Microsystems의 Peter Deutsch가 1994년에 정리한 "Fallacies of Distributed Computing"이 있다. 분산 시스템을 처음 다룰 때 우리 안에 깔려 있는 잘못된 직관 8가지다.

1. **The network is reliable.** — 네트워크는 신뢰할 수 있다.
2. **Latency is zero.** — 지연은 0이다.
3. **Bandwidth is infinite.** — 대역폭은 무한하다.
4. **The network is secure.** — 네트워크는 안전하다.
5. **Topology doesn't change.** — 토폴로지는 변하지 않는다.
6. **There is one administrator.** — 관리자는 한 명이다.
7. **Transport cost is zero.** — 전송 비용은 0이다.
8. **The network is homogeneous.** — 네트워크는 동질적이다.

이 8가지가 모두 거짓이다. production에 가는 순간 우리는 이 거짓을 매일 확인하게 된다. 그런데도 우리가 코드에서 자주 만나는 모양은 마치 8가지 모두 참인 것처럼 짠 코드다.

```python
def charge_card(amount, card_token):
    response = payment_gateway.charge(amount, card_token)
    return response.transaction_id
```

이 한 줄짜리 함수가 production에서 만나는 현실은 다음과 같다.

- **네트워크가 끊긴다.** `requests.post`가 timeout을 던진다. 카드는 결제됐는지 안 됐는지 모름.
- **응답이 오는데 5초 걸린다.** 그 사이 사용자는 페이지를 새로 고친다.
- **5xx 응답이 온다.** 카드사가 자기도 일관성 없는 상태가 됐다.
- **DNS가 갑자기 바뀐다.** payment_gateway의 IP가 5분 동안 잘못된 곳을 가리킨다.

이 모든 시나리오에서 위 한 줄 코드는 안전하지 않다. 안전한 코드는 다음을 모두 가져야 한다.

1. **Timeout.** 5초 안에 응답이 안 오면 포기한다.
2. **Idempotency key.** 같은 결제를 두 번 보내도 두 번 처리되지 않게.
3. **Retry with backoff + jitter.** 실패 시 무작정 즉시 재시도하지 않게.
4. **Circuit breaker.** 카드사가 통째로 죽으면 호출 자체를 차단.
5. **Bulkhead.** 카드 결제 thread pool이 다른 기능까지 죽이지 않게.

이 다섯이 이 챕터의 다섯 주인공이다. 하나씩 살펴보자.

## Idempotency Key — Stripe의 1번 약속

Stripe의 Brandur Leach가 블로그에 쓴 글이 idempotency의 사실상 표준이다.

> An idempotency key is a unique value generated by a client and sent to an API along with a request, with the server storing the key for bookkeeping the status of that request. (Brandur, Stripe)

핵심 아이디어는 단순하다. **client가 매 요청마다 UUID를 생성해 보내고, server는 같은 UUID로 두 번째 요청이 오면 첫 번째 응답을 그대로 반환한다.** 그래서 retry해도 한 번만 처리된다.

server 쪽 구현은 대략 다음과 같다.

```python
def charge_card(idempotency_key, amount, card_token):
    # 1. 같은 key로 이전 요청이 있는지 확인
    existing = db.query("SELECT response FROM idempotency_log WHERE key = ?", idempotency_key)
    if existing:
        if existing.status == 'completed':
            return existing.response  # 첫 응답 그대로 반환
        if existing.status == 'in_progress':
            raise Conflict("이미 처리 중인 요청입니다")
    
    # 2. in_progress로 마킹 (UNIQUE constraint로 race 방지)
    db.insert("INSERT INTO idempotency_log (key, status) VALUES (?, 'in_progress')", idempotency_key)
    
    # 3. 실제 처리
    try:
        result = payment_gateway.charge(amount, card_token)
        db.update("UPDATE idempotency_log SET status='completed', response=? WHERE key=?", result, idempotency_key)
        return result
    except Exception as e:
        db.update("UPDATE idempotency_log SET status='failed', error=? WHERE key=?", str(e), idempotency_key)
        raise
```

이 단순한 코드 한 블록이 결제 시스템의 1번 안전망이다. 같은 idempotency key로 두 번째 요청이 오면 첫 번째 응답을 그대로 반환한다. retry해도 결제는 한 번만 일어난다.

여기서 디테일 두 가지가 있다.

**1. Idempotency key는 client가 생성한다.** server가 생성하면 retry 시 client가 새 key를 보내, idempotency가 무효가 된다. client가 처음 요청 보낼 때 UUID v4를 만들고, 그 UUID를 retry 시에도 그대로 보내야 한다.

**2. Idempotency log는 만료가 있어야 한다.** 모든 결제마다 row가 영원히 쌓이면 DB가 비대해진다. 보통 24~72시간 retention으로 만료시킨다. retry는 그 안에서만 보장된다.

이 패턴이 IETF에서 표준화 진행 중이다 — `Idempotency-Key` HTTP 헤더 (draft-ietf-httpapi-idempotency-key-header). 2026년 기준 RFC 초안 상태(검증 필요)이고, Stripe·Square·일부 결제 API가 이미 채택했다. 한국 핀테크에서도 채택 사례가 빠르게 늘고 있다.

> 💡 휴리스틱 5 — "Retry는 idempotent 호출에만." Stripe Brandur의 블로그에 한 줄로 정리되어 있다.
>
> "If you don't have idempotency keys, every retry can double-charge customers. We learned this the hard way."
>
> idempotency key 없는 mutation endpoint에 retry를 박는 건 사고의 시작이다. 모든 mutation은 idempotency key를 default로 가져가는 편이 낫다.

### Idempotent하지 않은 호출은 어떻게?

모든 호출이 idempotent하지는 않다. "잔고 100원 차감" 같은 **상대적(delta) 연산**은 두 번 호출하면 200원 차감된다. 어떻게 idempotent하게 만들까?

**1. Operation을 idempotent하게 다시 정의.** "100원 차감" 같은 **상대적(delta) 연산**이 아니라 "잔고를 X원으로 set" 같은 **절대적(absolute) 연산**으로 바꾼다. 단 race condition 처리(optimistic locking)가 필요.

**2. Idempotency key + 결과 캐싱.** 위 패턴 그대로. 같은 key는 같은 효과만 일으킨다.

**3. State machine.** 결제가 PENDING → AUTHORIZED → CAPTURED → COMPLETED로 흐른다고 정의. 같은 transition을 두 번 시도해도 한 번만 일어난다.

이 셋 중 어느 것이 가장 좋은가? 도메인이 결정한다. 그러나 가장 보편적인 답은 idempotency key + key별 결과 저장이다.

## Timeout — 휴리스틱 4 "Timeout 없는 호출은 없다"

AWS Builders Library와 토스 SLASH 23이 입을 모아 강조한 한 줄이 있다.

> Every network call MUST have a timeout. Default of 'forever' is the cause of more outages than any bug.

기본값이 "영원히"인 timeout이 어느 bug보다 많은 outage의 원인이다. 이 한 줄이 어디서 가져온 통찰일까?

상황을 가정해 보자. service A가 service B를 호출한다. service B가 멈췄다. service A의 thread는 응답을 기다린다. 1초, 10초, 1분, 1시간. 그 사이 새 사용자 요청이 들어와 새 thread가 또 B를 호출한다. 또 멈춘다. service A의 thread pool이 가득 찬다. service A 자체가 응답 못 한다. cascade failure가 mesh 전체로 번진다.

이 모양은 한국·해외 모두에서 가장 흔한 production outage 모양이다. **한 service의 slow downstream이 전체 mesh를 stall시키는 일.** 시작은 timeout이 없는 호출이다.

그래서 모든 network 호출에는 명시적 timeout이 박혀야 한다.

```python
# 나쁜 예
response = requests.post(url, data=payload)

# 좋은 예
response = requests.post(url, data=payload, timeout=5.0)
```

그리고 timeout 값은 무작정 짧게 잡지도 말자. p99 latency보다 약간 길게 (예: p99의 2배). 너무 짧으면 정상 응답도 cut되고, 너무 길면 timeout의 의미가 없다.

```python
# 평소 p99가 100ms라면
timeout = 0.5  # 500ms, 충분히 여유 있음
```

> tribal #12 — "Database connection pool exhaustion → cascade." 1장 RDB에서 처음 만난 함정이다. circuit breaker 없으면 한 service의 slow query가 전체 mesh를 죽인다. timeout이 1차 방어선이고, circuit breaker가 2차 방어선이다.

## Retry with Backoff + Jitter — AWS Builders Library

retry는 idempotent 호출에서만 안전하다. 그렇다면 retry를 어떻게 해야 안전한가? AWS Builders Library가 정리한 표준 패턴이 있다.

```python
import random

def retry_with_backoff(func, max_retries=5, base_delay=0.1, max_delay=10):
    for attempt in range(max_retries):
        try:
            return func()
        except RetryableError:
            if attempt == max_retries - 1:
                raise
            # exponential backoff + jitter
            delay = min(base_delay * (2 ** attempt), max_delay)
            delay = delay * (0.5 + random.random() * 0.5)  # 0.5x ~ 1.0x
            time.sleep(delay)
```

핵심 두 가지 디테일이 있다.

**1. Exponential backoff.** 1차 retry는 100ms 후, 2차는 200ms, 3차는 400ms, 4차는 800ms... 실패가 계속되면 점점 더 길게 기다린다. downstream이 회복할 시간을 준다.

**2. Jitter.** 단순 exponential backoff만 쓰면, 모든 client가 같은 시각에 retry하는 **retry storm**이 일어난다. 100개 client가 동시에 retry하면 downstream에 또 thundering herd가 친다. jitter(랜덤)를 더해 retry 시각을 흩어 놓아야 한다.

> Jitter adds randomness to backoff to spread retries around in time. (AWS Builders Library)

jitter에는 여러 종류가 있다.

| 종류 | 식 | 특징 |
|------|-----|------|
| Full jitter | `random(0, backoff)` | 가장 분산이 큼, downstream 부하 최소 |
| Equal jitter | `backoff/2 + random(0, backoff/2)` | 절반은 보장, 절반은 랜덤 |
| Decorrelated jitter | `random(base, last_delay * 3)` | 이전 retry의 영향을 받음 |

AWS SDK는 2016년부터 client-side에 token bucket 기반 retry throttling을 내장했다. 같은 token이 떨어지면 retry 자체를 하지 않는다. 이런 메커니즘이 retry storm을 막는다.

### Retry할 것과 안 할 것 가르기

모든 실패를 retry하면 안 된다. **idempotent하지 않은 호출**, **client error (4xx)**, **인증 실패**는 retry해도 같은 결과다. retry는 다음 카테고리에 한정해야 한다.

| 분류 | retry 적합 | 이유 |
|------|-----------|------|
| 5xx server error | yes | 일시적 server 장애 가능 |
| Network timeout | yes (idempotent만) | 일시적 네트워크 문제 |
| 429 Too Many Requests | yes | retry-after 헤더 준수 |
| 4xx client error | **no** | 요청 자체가 잘못됨 |
| 401/403 인증 실패 | **no** | retry해도 같은 실패 |
| 결제 status: insufficient_funds | **no** | 잔액 부족은 retry로 안 풀림 |

retry 코드를 짤 때 이 카테고리를 명확히 가르는 편이 낫다. 무작정 모든 실패를 retry하면 사용자에게 잘못된 응답을 주고, downstream에 불필요한 부하만 늘린다.

## Circuit Breaker — 3-State 패턴

다음 방어선은 **circuit breaker**다. 회로 차단기처럼 작동하는 패턴이다. downstream이 너무 자주 실패하면 호출 자체를 일정 시간 차단한다.

3-state 모델이 표준이다. Netflix Hystrix가 정착시켰고, resilience4j가 Java 진영의 표준이 되었다.

```
[CLOSED]  ── 정상 호출, 실패율 카운팅
   │
   │ (실패율 > threshold)
   ▼
[OPEN]    ── 호출 차단, 즉시 실패 응답
   │
   │ (cool-down 시간 경과)
   ▼
[HALF-OPEN] ── 일부 호출만 통과, 성공률 측정
   │
   ├── (성공) → CLOSED
   └── (실패) → OPEN
```

- **Closed:** 정상 상태. 호출이 흐르고, 실패율을 카운팅한다.
- **Open:** 실패율이 threshold(예: 50%)를 넘으면 차단. cool-down 시간(예: 30초) 동안 모든 호출을 즉시 실패 응답.
- **Half-Open:** cool-down 후 일부 호출만 통과시켜 본다. 성공하면 closed로 복귀, 실패하면 다시 open.

이 패턴의 가치는 **downstream이 회복할 시간을 주는 것**이다. downstream이 100% 실패하는 동안 1000번의 호출을 보내봤자 다 실패한다. 그 사이 downstream은 회복 시도조차 못한다. circuit breaker가 잠시 호출을 차단해 주면, downstream이 자기 thread pool·connection pool을 비울 시간을 얻는다.

resilience4j의 한 줄 예시.

```java
CircuitBreaker breaker = CircuitBreaker.ofDefaults("paymentGateway");
Supplier<Response> decorated = CircuitBreaker.decorateSupplier(
    breaker, () -> paymentGateway.charge(amount));

try {
    Response r = decorated.get();
} catch (CallNotPermittedException e) {
    // circuit breaker가 open 상태, fallback 처리
    return fallbackResponse();
}
```

이 한 블록이 결제 시스템의 외부 vendor 호출에 들어가면, vendor가 죽었을 때 호출이 즉시 실패 응답이 된다. user thread가 5초씩 기다리지 않으니 thread pool이 가득 차지 않는다.

> Circuit breaker는 timeout과 함께 갈 때 효과가 가장 크다. timeout 없이 circuit breaker만 있으면 한 호출이 영원히 끝나지 않아 closed 상태에서 빠지지 못한다. **두 부품을 한 쌍으로 보자.**

## Bulkhead — 격벽으로 cascade 차단

마지막 방어선이 **bulkhead**(격벽)다. 배의 격벽을 떠올리면 가깝다. 한 칸이 침수되어도 다른 칸은 막혀 있다.

소프트웨어에서 bulkhead는 **thread pool 또는 connection pool을 작업 단위로 격리하는 것**이다. 결제 호출용 pool, 알림 호출용 pool, 추천 호출용 pool — 각각 별도. 한 pool이 가득 차도 다른 pool은 영향 없다.

```java
// 나쁜 예 — 공용 thread pool
ExecutorService sharedPool = Executors.newFixedThreadPool(100);
sharedPool.submit(() -> paymentService.charge(...));
sharedPool.submit(() -> notificationService.send(...));
// payment가 멈추면 notification도 영향

// 좋은 예 — 격리된 pool
ExecutorService paymentPool = Executors.newFixedThreadPool(20);
ExecutorService notificationPool = Executors.newFixedThreadPool(20);
paymentPool.submit(() -> paymentService.charge(...));
notificationPool.submit(() -> notificationService.send(...));
```

이 한 줄 차이가 cascade를 막는다. payment가 slow downstream으로 죽어도 notification은 자기 pool에서 정상 동작한다.

bulkhead는 thread pool뿐 아니라 connection pool, semaphore에도 적용할 수 있다. 핵심 원칙은 **"한 작업의 자원 부족이 다른 작업까지 죽이지 않게 가른다"**다.

## 한국 사례 — 토스 본인인증 vendor 다중 failover

한국 백엔드의 좋은 사례는 토스의 결제 발표다. 토스 SLASH 23에서 "본인인증 vendor 다중 failover" 패턴을 공유했다.

상황은 이렇다. 한국에서 결제·송금·청약 등 모든 금융 행위에는 **본인인증**이 필요하다. 본인인증 API는 통신 3사(KT·SKT·LGU+)와 제휴된 vendor(KCB·NICE·KCP·다날 등)가 제공한다. 문제는 이 vendor들이 SLA가 낮고, 0시·9시 같은 한국 특유의 burst 트래픽에 자주 죽는다는 점이다.

토스의 해결책은 **다중 vendor + 동적 failover**다.

1. 평소에는 vendor A(가장 싼 곳)로 라우팅.
2. vendor A의 성공률·latency를 실시간 모니터링.
3. 성공률이 임계(예: 95%)를 떨어지면 **circuit breaker가 open**, 트래픽을 vendor B로 자동 이동.
4. vendor A의 cool-down 후 일부 트래픽으로 다시 테스트.
5. 회복되면 vendor A로 복귀.

이 패턴이 그대로 이 챕터의 다섯 부품을 다 활용한다. timeout, retry+backoff+jitter, circuit breaker, bulkhead. 그리고 idempotency도 — 같은 사용자가 인증을 두 번 시도해도 한 번만 처리된다.

> 패턴 9 — "신규 서비스인데 갑자기 본인인증 API가 죽었다." 한국 핀테크의 일상 함정이다. 토스의 다중 vendor failover는 이 함정의 모범 답안이다. 다른 한국 핀테크들도 비슷한 패턴을 정착시키고 있다. **이 한 사례가 다섯 부품(timeout·idempotency·retry·circuit breaker·bulkhead)이 함께 작동할 때 우리가 얻는 효과의 결정적 모범 답안이다 — 사용자가 0시에 본인인증을 누르고 1초 안에 응답을 받는 일상이 그 위에 깔린다.**

## 모든 network 호출에 던질 5가지 질문

이 챕터의 핵심 통찰을 한 줄로 압축하면 이거다. **모든 network 호출에 대해 5가지를 자동으로 물어야 한다.**

1. **Timeout은 얼마인가?** 기본값 "영원히"는 outage의 원인이다.
2. **Retry해도 되는가? Idempotent한가?** 결제는 idempotency key 없이 retry하면 안 된다.
3. **Retry 시 backoff + jitter를 쓰는가?** 단순 즉시 retry는 storm을 만든다.
4. **Circuit breaker가 있는가?** downstream이 죽었을 때 호출을 차단할 수 있는가.
5. **Bulkhead가 있는가?** 이 호출의 thread pool이 다른 기능을 죽이지 않는가.

이 5가지가 머릿속에 자동으로 떠오르면 코드 리뷰에서 "이 endpoint는 idempotent한가?", "여기 timeout 누락된 것 같은데?" 같은 질문이 자연스럽게 나온다. 그 한 줄 질문이 새벽 alert를 줄여 준다. **그리고 그 질문이 자동으로 떠오를 때, 0장에서 약속한 3번째 약속 — "모든 network 호출에 멱등성·재시도·서킷 브레이커·timeout이 한 묶음으로 떠오른다 — '실패는 정상'이라는 인지가 코드 작성 습관으로 박힌다" — 의 본격 회수가 여기서 일어난다.**

## 운영 모니터링 — Resilience 대시보드 6가지

이 다섯 부품을 깔았다면, 그 효과를 모니터링하는 6가지를 마지막으로 정리하자.

| # | 지표 | 의미 | 임계 |
|---|------|------|------|
| 1 | timeout error rate (per endpoint) | timeout 발생률 | 0.1% 넘으면 의심 |
| 2 | retry count per request | retry 빈도 | 평균 0.5 이상이면 downstream 의심 |
| 3 | circuit breaker state | open/half-open/closed | open 상태 알림 즉시 |
| 4 | thread pool utilization | pool 사용률 | 80% 넘으면 ramp-up 검토 |
| 5 | idempotency hit rate | 같은 key 재요청 비율 | 평소 1~3% (적당한 retry 분포) |
| 6 | downstream success rate | 외부 vendor 성공률 | 95% 미만 즉시 alert |

이 6가지를 한 화면에 띄워두면, 새벽에 alert가 울려도 어느 지표를 먼저 봐야 할지가 분명하다. 특히 **circuit breaker가 open으로 전환되는 순간**이 가장 critical하다. 이 알림이 없으면 vendor 장애가 우리 사용자 응답으로 그대로 전파된다.

## Callback 예고

10장의 다섯 부품은 책 후반에 핵심 도구로 반복 등장한다.

- **11장 Saga·Outbox.** 분산 트랜잭션의 **보상 작업(compensating action)**이 idempotency 위에서 작동한다.
- **19장 결제 시스템.** 토스 결제 critical path가 정확히 이 다섯 부품을 다 활용한다. idempotency가 결제 안전망의 1번 줄이다.
- **20장 이커머스.** 쿠팡 BFCM 대응이 circuit breaker + bulkhead로 cascade를 막는다.

이 챕터의 다섯 부품이 머릿속에 있어야 후속 챕터의 의사결정이 따라온다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 실패를 가정한 통신의 다섯 부품이 손에 잡혀 있다. Idempotency key (Stripe), Timeout (휴리스틱 4), Retry with backoff + jitter (AWS Builders Library), Circuit breaker 3-state (Hystrix·resilience4j), Bulkhead. 그리고 한국 토스의 본인인증 다중 vendor failover 사례까지가 한 묶음이다.

기억해두자. 분산 시스템에서 모든 network 호출은 언젠가 실패한다. 그 사실을 코드로 표현하지 않으면, 실패가 사용자의 결제로 전가된다. 위 다섯 부품을 default로 깔자. 그리고 새 endpoint 설계 시 5가지 질문을 자동으로 던지자 — "timeout? retry? idempotent? circuit breaker? bulkhead?"

다음 장에서는 분산 트랜잭션을 살펴본다. 2PC를 안 쓴다면 마이크로서비스 사이의 일관성은 누가 책임지는가? Saga와 Outbox와 Event Sourcing의 세 갈래를 함께 짚어 보자. 그 위에서 이번 장의 idempotency가 어떻게 안전망의 1번 줄이 되는지를 함께 보자.

---

# 11장. Saga·Transactional Outbox·이벤트 소싱 — 분산 트랜잭션의 현실적 길

어떤 결제 시스템에서, 카드 승인은 성공했는데 우리 DB에 기록을 못 남기는 사고가 있다고 해보자. 사용자 입장에서는 돈이 빠져나갔다. 카드사 명세서에 결제 기록이 찍혔다. 그런데 우리 DB에는 그 결제가 없다. 결제 영수증을 발급하라는 후속 작업도 안 일어난다. 사용자가 "왜 영수증이 안 와요?"라고 문의를 넣는다. 우리는 시스템 로그를 펴 보고 한참 뒤에야 무슨 일이 일어났는지 추측한다.

이런 상황을 한 번 겪고 나면 "dual-write 문제"라는 단어가 평생 따라다닌다. **두 시스템(우리 DB + 카드사)에 같은 트랜잭션을 atomic하게 쓰는 게 불가능하다**는 진실. 둘 중 하나는 성공하고 다른 하나는 실패할 수 있는 그 가능성이 분산 시스템의 가장 어두운 균열이다.

그래서 이 균열을 어떻게 메우는지가 이번 장의 주된 사고 실험이다. 가장 단순한 해법인 2PC가 왜 거의 안 쓰이는지, 그 대신 무엇이 들어왔는지. Saga, Transactional Outbox + CDC, Event Sourcing의 세 갈래를 짚고, 각각이 어떤 도메인에 맞는지 의사결정 트리를 손에 잡자. 한국 토스 코어뱅킹의 SAGA + 2PC 혼합 사례까지 함께 본다.

## 왜 2PC를 거의 안 쓰는가

분산 시스템의 일관성을 보장하는 가장 단순한 답은 **2PC (Two-Phase Commit)**다. 1980년대부터 알려진 표준 프로토콜이다. 흐름은 단순하다.

```
Phase 1 (Prepare):
  Coordinator → Participants: "이 트랜잭션 commit할 수 있어?"
  Participants → Coordinator: "yes" 또는 "no"

Phase 2 (Commit):
  모두가 yes면 → "commit해라" 명령
  하나라도 no면 → "abort해라" 명령
```

이론적으로 깔끔하다. 그런데 production에서 2PC를 쓰는 마이크로서비스 시스템은 거의 없다. 왜?

**1. Blocking.** Phase 1에서 yes를 답한 participant는 commit이 결정될 때까지 lock을 잡고 대기한다. coordinator가 죽거나 응답이 늦어지면 그동안 자원이 잠긴다. 한 transaction이 1분 동안 lock을 잡으면, 그 자원을 쓰려는 다른 트랜잭션이 다 막힌다. 끔찍하다.

**2. SPOF (Single Point of Failure).** Coordinator가 죽으면 전체 트랜잭션이 stuck된다. Phase 2 명령이 안 와서, participant는 영원히 lock을 잡고 기다린다.

**3. Network Partition 취약성.** Network split이 나면 participant들이 서로 다른 결정을 받을 수 있다. 일관성이 깨진다.

**4. Throughput 한계.** Lock과 latency 때문에 throughput이 단일 DB의 1/10~1/100로 떨어진다. 마이크로서비스 환경에서 감당이 안 된다.

그래서 마이크로서비스 시대 이후로 2PC는 거의 자취를 감췄다. 대신 등장한 세 패턴이 Saga, Transactional Outbox, Event Sourcing이다. 이 셋이 각자 다른 방식으로 "분산 트랜잭션 없이도 일관성을 만드는" 길을 제시한다.

## Saga — 일련의 local transaction으로 분해

Saga는 1987년 Princeton에서 제안된 패턴인데, 마이크로서비스 시대에 다시 주목받았다. Chris Richardson의 *Microservices Patterns*가 가장 정리된 설명이다.

핵심 아이디어는 단순하다. **하나의 큰 분산 트랜잭션을 여러 개의 local transaction의 sequence로 분해한다.** 각 step은 자기 service의 DB에서 local로 commit한다. 중간에 실패하면 이미 commit된 step들을 **compensating action**(보상 작업)으로 되돌린다.

```
주문 처리 Saga:
  1. 재고 차감 (inventory service local commit)
  2. 결제 처리 (payment service local commit)
  3. 배송 등록 (shipping service local commit)
  
  실패 시 compensating action:
  1. 배송 등록 실패 → 결제 환불 + 재고 복원
  2. 결제 실패 → 재고 복원
```

이 모양에는 두 가지 변형이 있다.

### Choreography — 이벤트 기반 분산

각 service가 이벤트를 발행하고 다른 service가 그 이벤트에 반응한다. 중앙 조정자가 없다.

```
주문 service: OrderCreated 이벤트 발행
  ↓
재고 service: 이벤트 수신 → 재고 차감 → InventoryReserved 이벤트 발행
  ↓
결제 service: 이벤트 수신 → 결제 처리 → PaymentCompleted 이벤트 발행
  ↓
배송 service: 이벤트 수신 → 배송 등록
```

장점은 service들이 느슨하게 결합된다는 점. 새 service를 추가해도 기존 service는 모른다. 단점은 **전체 흐름 추적이 어렵다**는 점. 트랜잭션 하나가 어디까지 왔는지 보려면 여러 service의 로그를 다 모아 봐야 한다. 이른바 "event soup"가 만들어진다.

### Orchestration — 중앙 조정자

중앙의 **orchestrator**가 각 service에 명령을 보내고, 응답을 모아 다음 step을 결정한다.

```
Orchestrator:
  1. inventoryService.reserve(orderId) → 성공
  2. paymentService.charge(orderId) → 실패
  3. inventoryService.cancel(orderId) — 보상 실행
```

장점은 흐름이 한눈에 보인다는 점. orchestrator 한 곳만 보면 트랜잭션 상태를 알 수 있다. 단점은 orchestrator가 **SPOF**가 될 수 있다는 점, 그리고 orchestrator 자체의 복잡도가 커진다는 점이다.

대표 도구가 Camunda, Temporal, AWS Step Functions이다. 한국 핀테크에서는 Temporal이 빠르게 채택되고 있다.

### Choreography vs Orchestration

| 차원 | Choreography | Orchestration |
|------|-------------|---------------|
| 결합도 | 낮음 (이벤트로만 연결) | 높음 (orchestrator가 모두 알아야 함) |
| 가시성 | 낮음 (분산 로그) | 높음 (orchestrator 한 곳) |
| 새 step 추가 | 쉬움 (consumer만 추가) | orchestrator 코드 수정 |
| 실패 디버깅 | 어려움 | 쉬움 |
| 적합 규모 | 작은 service 수 (~5개) | 큰 service 수 또는 복잡한 흐름 |

작은 시스템은 choreography로 시작하고, service가 5개를 넘기 시작하면 orchestration으로 옮기는 편이 낫다. 흐름 추적이 어느 순간 운영의 최대 비용이 되기 시작한다.

### 보상 작업 설계의 함정

Saga의 가장 큰 함정이 **보상 작업이 항상 가능한 건 아니라는 사실**이다. 결제 환불은 가능하지만, 이미 발송된 알림은 취소가 불가능하다. 이미 출고된 상품은 회수가 어렵다.

이 한계를 풀어주는 패턴이 **세마틱 보상**이다. 진짜로 되돌리는 게 아니라, "되돌렸다는 상태"를 만든다. 알림을 취소할 수 없다면 "취소 알림"을 다시 보낸다. 출고된 상품을 회수할 수 없다면 "주문 취소 + 환불" 흐름으로 처리한다.

또 한 가지 — **보상 자체도 실패할 수 있다.** 보상 작업이 실패하면 어떻게 할까? 보통 retry + dead letter queue + 운영자 수동 개입 패턴이다. 이 모양이 10장 idempotency·retry·circuit breaker와 그대로 만난다.

> 💡 흔한 오해 — "Saga = 분산 트랜잭션 만능 해법." 실제로는 **보상 가능한 도메인에서만 작동**한다. 보상 불가능한 작업(이메일 발송, 알림, 외부 통신)이 끼면 saga 모델이 깨진다. 이런 경우 그 작업을 saga의 마지막에 두거나, "보상 없이 안전한" 다른 패턴(Outbox)으로 대체해야 한다.

## Transactional Outbox + CDC — Dual-Write 문제의 표준 답

가장 흔한 dual-write 시나리오를 다시 떠올려 보자.

```python
def create_order(order):
    db.insert(order)         # 성공
    kafka.send(event)        # 실패 → 메시지 안 감
```

DB에는 주문이 있는데 Kafka에는 이벤트가 없다. 다음 단계(결제·배송·알림)가 안 일어난다. 이걸 어떻게 안전하게 풀까?

**Transactional Outbox** 패턴이 사실상의 표준 답이다. 핵심 아이디어는 단순하다. **DB 트랜잭션 안에 메시지 자체를 outbox 테이블에 함께 insert한다.** 별도 워커가 outbox 테이블을 tail해 Kafka에 발행한다.

```python
def create_order(order):
    with db.transaction():
        db.insert(order)
        db.insert_outbox(event)  # 같은 트랜잭션
    # commit 끝, DB만 변경됨
    # 별도 worker가 outbox를 polling하거나 CDC로 tail
```

이 한 줄짜리 변경이 dual-write 문제를 통째로 해결한다. DB 트랜잭션이 atomic이니, order와 outbox row가 동시에 commit되거나 동시에 롤백된다.

별도 worker가 outbox를 처리하는 방법은 두 가지다.

### Polling 기반

worker가 일정 주기로 outbox 테이블을 SELECT해 미처리 row를 처리한다.

```python
while True:
    rows = db.query("SELECT * FROM outbox WHERE published=FALSE LIMIT 100")
    for row in rows:
        kafka.send(row.event)
        db.update("UPDATE outbox SET published=TRUE WHERE id=?", row.id)
    time.sleep(1)
```

장점은 단순함. 단점은 polling 주기에 따른 latency, 그리고 DB 부하.

### CDC (Change Data Capture) 기반

**Debezium** 같은 도구가 DB의 WAL(Write-Ahead Log) 또는 binlog를 tail해, 변경 사항을 Kafka로 자동 발행한다. polling 없이 거의 실시간 (~ms 단위).

```
Postgres WAL → Debezium → Kafka topic "outbox-events"
```

이 모양이 가장 우아하다. 거의 zero-latency, ordering 보존, DB 부하 최소. 한국 백엔드에서도 Debezium 채택이 늘고 있다.

Debezium 공식 문서의 한 줄이 그 가치를 정리한다.

> The Outbox Event Router SMT can be used to forward outbox events to a destination topic for asynchronous propagation, providing an at-least-once delivery guarantee. (Debezium docs)

### Polling vs CDC

| 차원 | Polling | CDC (Debezium) |
|------|---------|----------------|
| Latency | 초 단위 | ms 단위 |
| DB 부하 | 추가 query | log tail만 |
| 구현 복잡도 | 매우 단순 | Debezium·Kafka Connect 운영 필요 |
| Ordering | LIMIT 순서 | DB log 순서 자동 보존 |
| Throughput | 제한적 | 매우 높음 |

작은 시스템은 polling으로 충분하다. 마이크로서비스가 늘고 throughput이 커지면 CDC로 옮기는 편이 낫다.

### Outbox + Saga = 안전한 분산 흐름

Outbox와 Saga를 함께 쓰면 진짜 안전한 분산 흐름이 만들어진다. 각 step은 outbox로 다음 step을 트리거하고, 실패 시 compensating outbox로 보상한다.

```
주문 service:
  TRANSACTION:
    INSERT order
    INSERT outbox(OrderCreated event)
  
재고 service:
  consume(OrderCreated)
  TRANSACTION:
    UPDATE inventory SET qty = qty - 1
    INSERT outbox(InventoryReserved event)
  
결제 service:
  consume(InventoryReserved)
  ... 같은 패턴
```

이 모양은 어떻게 실패가 발생해도 다음 두 가지가 보장된다.

1. **로컬 DB와 outbox는 atomic.** DB가 변경되면 이벤트도 반드시 발행된다.
2. **At-least-once delivery.** 이벤트가 최소 한 번은 전달된다. 같은 이벤트가 두 번 와도 idempotent consumer가 한 번만 처리.

이 두 약속이 분산 시스템의 일관성을 만든다. **idempotent consumer**의 패턴은 10장에서 다룬 idempotency key가 그대로 사용된다. 10장과 11장이 한 쌍으로 작동하는 셈이다.

## Event Sourcing — State를 event log로 대체

세 번째 갈래가 **Event Sourcing**이다. 보다 깊은 패턴이고, 모든 시스템에 적용할 만한 패턴은 아니다.

전통적인 데이터 모델은 현재 state를 저장한다. "사용자 잔고 = 10,000원". Event Sourcing은 그 대신 모든 변경 이벤트를 저장한다.

```
event log:
  AccountCreated(userId=1, balance=0)
  DepositMade(userId=1, amount=10000)
  WithdrawMade(userId=1, amount=3000)
  DepositMade(userId=1, amount=3000)
```

현재 잔고를 알려면 event들을 순서대로 replay한다. 0 + 10000 - 3000 + 3000 = 10000원. 또는 snapshot을 주기적으로 만들어 그 위에 새 event만 replay하면 빠르다.

이 패턴의 장점이 크다.

**1. 완벽한 audit trail.** 모든 변경 history가 남는다. "왜 이렇게 됐지?"라는 질문에 항상 답할 수 있다.

**2. Time travel.** 특정 시점의 state를 재구성할 수 있다. "어제 오후 3시 사용자 잔고는?" 같은 질문에 답한다.

**3. CQRS와 자연스럽게 결합.** Write 모델은 event를 append, Read 모델은 event로부터 다양한 projection 생성.

**4. 새 view 추가가 쉽다.** 새 read model이 필요하면 event를 처음부터 replay해 새 view를 만든다.

하지만 Martin Fowler가 "신중하게 쓰라"고 경고한 이유도 있다.

> You should be very cautious about using CQRS... it can add significant complexity and make a significant drag on productivity. (Martin Fowler)

Event Sourcing의 함정은 다음과 같다.

**1. Event schema migration이 가장 어렵다.** Hugo Rocha가 자기 글에서 정확히 짚었다 — "event는 영원히 남는다." event schema를 한 번 정하면, 5년 전 event도 새 코드가 해석할 수 있어야 한다. 변경 시 versioning + upcasting 로직이 필요하다.

**2. Query가 직관적이지 않다.** "잔고가 500원 이하인 사용자 목록"을 알려면 모든 사용자의 event를 다 replay해야 한다. CQRS로 read model을 별도 두지 않으면 불가능하다.

**3. 학습 곡선이 가파르다.** 도메인 모델, event design, projection, snapshot, idempotency — 모두 새 개념. team이 이 모델에 익숙해지는 데 시간이 든다.

**4. event 폭증.** "사용자 매 클릭"을 다 event로 저장하면 storage가 폭증한다. 도메인의 의미 있는 결정만 event로 잡아야 한다.

그래서 Event Sourcing은 다음 도메인에서만 가치가 있다.

- **금융·회계.** audit trail이 법적 의무.
- **게임.** 사용자 행동 분석에 event log가 자연스럽다.
- **협업 도구.** time travel, undo가 핵심 기능.

일반 CRUD 도메인에는 과한 패턴이다. Fowler의 경고를 마음에 새기는 편이 낫다.

## 의사결정 트리 — 4가지 후보 패턴 중 무엇을 고를까

지금까지 살펴본 4가지 후보(2PC, Saga, Outbox+CDC, Event Sourcing)를 한 의사결정 트리로 정리하자.

```
분산 트랜잭션이 정말 필요한가?
├── No → 단일 DB에서 처리 (1장 RDB 참고)
└── Yes → 다음 질문
    
    Strong consistency가 critical한가? (예: 잔고 차감, 재고 동시 결정)
    ├── Yes, blocking 견딜 수 있음 → 2PC (드문 경우)
    └── Yes, blocking은 못 견딤 또는 No → Eventual consistency 패턴
        
        도메인의 step이 보상 가능한가?
        ├── No (이메일 발송, 알림 등) → Outbox + CDC (이벤트 발행만)
        └── Yes → Saga 가능
            
            service 수가 적은가? (~5개 이하)
            ├── Yes → Saga choreography (이벤트 기반)
            └── No → Saga orchestration (Temporal/Camunda)
        
        과거 모든 변경 history가 audit·time travel·undo에 필요한가?
        ├── Yes, 도메인이 금융·게임·협업 → Event Sourcing 검토
        └── No → 위 Saga/Outbox로 충분
```

이 트리에서 가장 자주 가는 길은 **Saga + Outbox 결합**이다. 각 step은 outbox로 다음 step 트리거, 실패 시 compensating outbox로 보상. 한국 백엔드의 대부분 분산 트랜잭션이 이 모양으로 가고 있다.

## 한국 사례 — 토스 코어뱅킹 SAGA + 2PC 혼합

한국에서 가장 자주 인용되는 분산 트랜잭션 사례가 토스 코어뱅킹이다. 토스 SLASH 23에서 공개된 발표에 따르면, 토스 뱅킹의 core transaction은 **SAGA와 2PC를 혼합**한 모델을 쓴다.

상황을 한 번 떠올려 보자. 토스에서 A 사용자가 B 사용자에게 송금한다. 두 사용자의 계좌가 같은 은행이면 한 DB 안에서 트랜잭션이라 단순. 그런데 토스에서는 마이크로서비스 분리로 인해 송금이 다음 service들을 거친다.

1. 송금 service: 송금 요청 검증
2. 계좌 service A: A의 잔고 차감
3. 계좌 service B: B의 잔고 추가
4. 거래 history service: 거래 기록
5. 알림 service: A·B에게 push

핵심 결정은 **2-4 사이는 SAGA, 그 안에서 가장 critical한 잔고 차감/추가는 2PC**라는 모양이다. 왜 이렇게 갈랐을까?

- **잔고 차감/추가의 strong consistency가 절대 critical.** A의 잔고가 줄었는데 B의 잔고가 안 늘면 그건 돈이 증발한 것이다. 절대 일어나면 안 된다. → 2PC로 atomic.
- **거래 history·알림은 eventual consistency 가능.** 거래 기록은 몇 초 늦어도 됨. 알림도 마찬가지. → SAGA로 비동기.

이 혼합 모델이 한국 핀테크의 가장 sophisticated한 패턴이다. 2PC를 완전히 안 쓰는 게 아니라, **2PC를 정말 필요한 좁은 범위로 한정**하고, 나머지는 SAGA로 푸는 것. 토스의 결정은 분산 시스템 설계의 정교한 균형을 보여 준다.

> 한 줄 통찰 — **모든 트랜잭션이 같은 일관성 수준을 요구하지 않는다.** 도메인별로 strong consistency가 진짜 필요한 경계를 찾고, 그 안에는 2PC를 쓰되, 그 밖에는 SAGA/Outbox로 푸는 편이 낫다.

## Saga·Outbox·Event Sourcing 도입 자격 5가지 질문

새 분산 시스템을 설계할 때 자기에게 던질 다섯이다.

1. **이 트랜잭션이 정말 분산이어야 하는가?** 단일 service·DB로 끝낼 수 있으면 그게 가장 단순한 답.
2. **strong consistency가 critical한가?** 잔고·재고 같은 도메인은 strong, 알림·로그 같은 도메인은 eventual.
3. **step들이 보상 가능한가?** 이메일·외부 알림이 끼면 saga 모델이 깨진다.
4. **service 수가 5개 이하인가?** choreography로 시작, 그 이상이면 orchestration(Temporal).
5. **event log가 도메인 가치를 만드는가?** 금융 audit, 게임 분석 같은 도메인 외에는 Event Sourcing은 과하다.

이 다섯에 답이 명확하지 않으면 일단 단일 DB + Outbox 패턴으로 시작하고, 한계가 오면 Saga를 추가하는 편이 낫다. 처음부터 Event Sourcing + CQRS + Saga를 다 깔면 운영 부담만 폭증한다.

## Callback 예고

11장의 세 패턴은 책 후반에 핵심 부품으로 반복 등장한다.

- **19장 결제·금융.** 토스 결제 critical path가 이 챕터의 SAGA + 2PC 모델을 그대로 활용. 외부 vendor failover + Saga + Outbox.
- **20장 이커머스.** 쿠팡 BFCM 주문 흐름이 Saga choreography 기반.

이 챕터의 의사결정 트리가 머릿속에 있어야 후속 케이스 스터디의 결정이 따라온다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 분산 트랜잭션의 네 후보 패턴이 손에 잡혀 있다. 2PC(이론은 깔끔, 실용은 거의 안 씀), Saga(choreography vs orchestration, 보상 가능 도메인 한정), Transactional Outbox + CDC(dual-write 문제의 표준 답), Event Sourcing(audit·time travel 도메인 한정). 토스 코어뱅킹의 SAGA + 2PC 혼합 모델까지가 한 묶음이다.

기억해두자. 분산 시스템에서 일관성은 무료가 아니다. strong consistency를 약속하면 blocking을, eventual을 받아들이면 보상 가능 도메인에 한정된다는 trade-off가 있다. **모든 트랜잭션을 같은 일관성 수준으로 다루지 말자.** 도메인별로 strong이 정말 필요한 좁은 범위를 찾고, 그 밖에는 Saga/Outbox로 푸는 편이 낫다.

다음 장에서는 합의·복제·일관성 모델을 깊이 들여다본다. CAP·PACELC·linearizability·causal·eventual — 이 단어들을 우리 도메인 언어로 다시 정의해 보자. Raft를 알면 무엇이 보이는지, Spanner·CockroachDB의 약속이 정확히 무엇인지 함께 짚자.

---

# 12장. 합의·복제·일관성 모델 — Raft를 알면 무엇이 보이는가

회의에서 동료가 묻는다고 해보자. "우리 결제 시스템은 strong consistency가 필요한가요?" 답이 입에서 나오기 전에 머리 안에서 단어 한 무더기가 부딪힌다 — linearizability, sequential, causal, eventual, PACELC. 정의는 책에서 본 적이 있는데, 우리 결제 시스템이 정확히 이 중 어느 줄에 있는지 한 박자에 답하기는 어렵다. DDIA를 다 읽었다고 해도, 한 달 뒤 그 질문 앞에서 똑같이 막힌다. 답은 책 안에 있지만, 책의 단어와 우리 회사의 단어가 다르기 때문이다.

이 한 줄을 풀려고 우리는 분산 시스템 50년의 이론을 다섯 페이지로 압축해야 한다. 그 압축이 이번 장의 목적이다. Paxos가 1989년에 시작한 합의의 사고법, Raft가 2014년에 그걸 "이해 가능하게" 다시 쓴 결정, ZAB이 ZooKeeper에 자리 잡았다가 Kafka가 KRaft로 옮겨 간 운영의 진실, single-leader·multi-leader·leaderless 복제가 약속하는 것·양보하는 것, 그리고 마지막으로 CAP→PACELC→CALM이라는 일관성 이론의 세 단계 — 이걸 우리 도메인 언어로 다시 묶어 보자.

## 1. FLP impossibility — 분산 합의의 출발점에 박힌 한 줄

분산 합의에 관한 이야기를 시작할 때 빼놓을 수 없는 한 편의 논문이 있다. **FLP impossibility (Fischer·Lynch·Paterson, 1985, P30)**다. 한 줄로 요약하면 — **"완전 비동기 네트워크에서, 결정적 알고리즘으로는 합의를 보장할 수 없다."** 한 노드가 영원히 멈춰 있는지, 단순히 느린지 — 비동기 모델에서는 이걸 결정적으로 구별할 수 없기 때문이다.

이 결과는 분산 시스템 학계에 큰 충격이었다. 그렇다면 합의는 어떻게 가능한가? 답은 **"실용 알고리즘은 무엇을 양보해서 가능하게 만들었는지 정확히 봐야 한다"**는 것이다. Paxos·Raft·ZAB 같은 알고리즘들은 모두 FLP의 그림자 안에서 작동한다. 보통은 두 가지 중 하나(또는 둘 다)를 양보한다.

- **Liveness 양보.** 네트워크가 안정될 때까지 진행이 멈출 수 있다. 안정되면 결국 합의가 끝난다 — eventual progress.
- **Stable leader 가정.** leader가 가끔 바뀌어도 대부분 시간 동안은 한 명의 leader가 유지된다고 가정한다.

기억해 두자. **분산 합의는 마법이 아니라 trade-off다.** "Raft를 도입하니 다 해결됐다"가 아니라, "Raft가 어떤 가정 아래에서 어떤 보장을 주는지 알고 도입하면 새벽 alert이 줄어든다"는 자세가 시니어와 그렇지 않은 사람의 차이다.

## 2. Paxos — 유명하기 어렵게 유명한 합의

1989년 Leslie Lamport가 *The Part-Time Parliament* (P1)에서 처음 제시한 Paxos는, 학계에서 "이 논문 이해하기 너무 어려워서 reject 당한" 일화로 유명하다. 결국 1998년에 출판됐고, 그 후 2001년 Lamport가 *Paxos Made Simple*이라는 친절한 후속 논문을 또 써야 했다. 그래도 어렵다는 평가는 사라지지 않았다.

Paxos가 어려운 데는 이유가 있다. 한 라운드의 합의를 **prepare·promise·accept·learn 4단계**로 나누어 설명하는데, 각 단계의 의미와 어떻게 안전성·진행성을 보장하는지가 한 번에 머리에 들어오기 어렵다. 그리고 "단일 값 합의"인 basic Paxos를 "log 합의"로 확장한 Multi-Paxos는 또 한 단계 복잡해진다. 그래서 Google Chubby·Spanner 같이 Paxos를 실제 production에 박은 사례는 있지만, 일반 개발자가 Paxos를 직접 다루는 일은 거의 없다 — 대부분 도구가 추상화해 둔다.

그럼 왜 Paxos를 굳이 짚어야 할까? **현대 모든 합의 알고리즘이 Paxos가 만든 사고 틀 위에 있기 때문**이다. Raft도 ZAB도 Paxos가 푼 문제(왜 majority quorum이 안전한가, 왜 한 번 결정된 값은 바뀔 수 없는가)를 다른 표현으로 다시 쓴 것에 가깝다. Paxos를 정복할 필요는 없지만, 그 영향 아래 있다는 사실은 알아 두는 편이 낫다.

## 3. Raft — "이해 가능성"을 first-class goal로

2014년 Diego Ongaro와 John Ousterhout가 발표한 *In Search of an Understandable Consensus Algorithm* (P2)는 합의 알고리즘 영역의 풍경을 바꿨다. Raft 논문은 자기 첫 문단에서 도발적으로 선언한다 — **"Paxos가 어렵다는 사실은 학습·실무 양쪽에 해로웠다. 우리는 이해 가능성(understandability)을 first-class goal로 두는 합의 알고리즘을 만들었다."**

Raft가 단순한 비결은 세 가지 분해다.

1. **Leader election.** 일정 시간 leader로부터 heartbeat이 없으면 follower 중 하나가 candidate가 되고, majority의 표를 받으면 새 leader가 된다. 단순하고 명확하다.
2. **Log replication.** leader가 모든 write를 받아 자기 log에 append하고, follower들에게 복제한다. majority가 commit하면 그 entry는 "committed"로 marking된다.
3. **Safety.** 새 leader는 자기 log가 이전 commit된 entry를 모두 포함하고 있을 때만 선출될 수 있다 — log completeness check.

이 세 분해가 Raft의 강점이다. Paxos가 한 묶음으로 다루던 합의 과정을 세 독립 메커니즘으로 나눠 설명하니, 학습 비용이 훨씬 낮아진다. 그리고 그 효과는 production에 즉시 나타났다 — Raft는 출현 후 10년 사이에 **etcd, Consul, TiKV, CockroachDB, Kafka KRaft, 그리고 수많은 OSS 프로젝트의 default 합의 알고리즘**으로 자리 잡았다. 분산 합의 영역의 사실상 산업 표준이라고 봐도 좋다.

> "Raft separates the key elements of consensus, such as leader election, log replication, and safety." — Ongaro 2014 (P2)

## 4. ZAB — ZooKeeper의 atomic broadcast, 그리고 Kafka의 결정

세 번째 합의 알고리즘 **ZAB (ZooKeeper Atomic Broadcast)**도 짧게 짚어 두자. ZAB는 ZooKeeper 안에서 작동하며, 2008년경부터 Hadoop·HBase·초기 Kafka 같은 거대 시스템들의 coordination 레이어를 책임져 왔다 (P3).

ZAB는 Paxos·Raft와 형제 알고리즘에 가깝다. 안정 leader + log 복제 + majority quorum 같은 핵심 아이디어가 같다. 다만 "broadcast"라는 단어가 보여주듯, ZAB는 client 명령을 전체 ensemble에 atomic하게 퍼뜨리는 데 최적화돼 있다. ZooKeeper API의 단순함이 이 위에 얹혀 있다.

그런데 — Kafka가 2.8부터 ZooKeeper를 떼어내고 **KRaft (Kafka Raft)**로 갈아탔다는 사실이 시사하는 게 있다. 알고리즘 자체보다 **운영 부담**이 더 큰 결정 요인이라는 것이다. ZooKeeper를 Kafka와 함께 운영한다는 건 두 개의 분산 시스템을 동시에 책임진다는 뜻이다 — leader election·split-brain·persistent storage·JVM tuning이 두 배가 된다. Raft를 Kafka broker 자체에 내장하면 그 부담이 절반이 된다. 알고리즘이 더 우수해서가 아니라, 운영의 한 layer를 없애는 게 더 큰 가치였다.

**기억해 두자 — 합의 알고리즘 선택은 보통 알고리즘 자체보다 그것을 운영하는 시스템의 layer 수가 더 큰 변수다.** 우리가 새 시스템을 만들 때 ZooKeeper를 떠올리기 전에 "정말 외부 coordination service가 필요한가, etcd로 충분한가, 아니면 application 안에 Raft library를 박는 게 더 단순한가"를 한 번 더 묻는 편이 낫다.

## 5. Replication — leader 수로 보는 세 갈래

합의는 보통 "복제 log를 안전하게 합치는 방법"으로 쓰인다. 그렇다면 복제 자체는 어떤 모양들이 있을까? Leader 수로 가르는 게 가장 명쾌한 분류다.

### Single-leader replication

한 명의 leader가 모든 write를 받고, follower들이 비동기 또는 동기로 그 write를 복제받는다. Postgres·MySQL·Redis(default)·MongoDB(primary-secondary)가 모두 이 모델이다. 단순하고 빠르고, 대부분 시스템의 default다.

양보한 것은 명확하다. **write 가용성이 leader 1명에 묶여 있다.** leader가 죽으면 새 leader가 선출되기 전까지 write가 멈춘다 — failover 기간 동안 짧은 다운타임이 생긴다. Single-leader 시스템의 운영 깊이는 보통 이 failover의 정밀도(자동·수동·시간)에서 결정된다.

### Multi-leader replication

여러 leader가 각자 write를 받는다. 데이터센터마다 하나씩 leader를 두고 사용자 가까운 leader에 write를 보내는 모델이다. 글로벌 서비스에서 latency를 줄이는 데 강하지만 — **write conflict가 필연적**이다. 같은 row를 두 leader가 동시에 수정하면 어떤 버전을 살릴지 결정해야 한다. last-write-wins, application-level merge, CRDT 같은 도구가 동원된다.

Multi-leader는 운영이 까다로워 일반 시스템에는 잘 쓰이지 않는다. 대신 **multi-datacenter Cassandra, BDR(Bi-Directional Replication) for Postgres, CouchDB 같은 특수 케이스**에 등장한다. 그리고 15장에서 다룰 CRDT가 이론적 기반을 제공한다 — CALM theorem과 연결된다(이건 잠시 후에 본다).

### Leaderless replication

leader가 없다. 모든 노드가 write를 받고, quorum 합의로 consistency를 만든다. **Dynamo·Cassandra·Riak**이 이 모델의 대표다. N(복제본 수)·R(read quorum)·W(write quorum)을 application이 튜닝한다 — R + W > N이면 strong-ish consistency, 그렇지 않으면 더 빠른 응답. 2장 NoSQL에서 짧게 본 내용이다.

Leaderless의 강점은 분명하다 — **write가 멈추지 않는다.** 노드 하나가 죽어도 다른 노드들이 write를 받는다. 양보한 것은 strong consistency다. 모든 conflict가 application 책임이 된다.

세 갈래를 한 줄 표로 정리해 보자.

| 축 | Single-leader | Multi-leader | Leaderless |
|---|---|---|---|
| Write 가용성 | leader 살아 있을 때만 | 항상 (각 leader 독립) | 항상 (quorum 살아 있으면) |
| Consistency | 강함 | 충돌 — application | quorum 튜닝 |
| 운영 복잡도 | 낮음 | 매우 높음 | 중간 |
| 대표 사례 | Postgres·MySQL·Redis | Cassandra multi-DC·BDR·CouchDB | Dynamo·Cassandra·Riak |
| 어울리는 곳 | 90% 시스템 | 글로벌 다중 데이터센터 | write-heavy + AP 선호 |

회의 자리의 정답은 보통 **"우선 single-leader. multi-leader·leaderless는 강한 정당화가 있어야 한다."**다. 한국 백엔드의 90%는 single-leader RDB로 충분하고, 운영 깊이는 그 위에 read replica·read 분산·partitioning을 얹는 데서 결정된다. multi-leader를 떠올렸다면 그 회의 자리에서 한 번 더 의심해 보자.

## 6. 일관성 모델 — 강 → 약 한 줄로 늘어놓기

이제 본격적으로 동료의 질문 — "우리 시스템에 strong consistency가 필요한가?" — 에 답할 수 있는 어휘를 정리하자. 일관성 모델은 강한 것부터 약한 것까지 한 줄로 늘어놓는 게 가장 명쾌하다.

### Linearizability — 가장 강한 보장

**linearizability**는 "분산 시스템이 마치 single-machine atomic 연산을 하는 것처럼 보이는" 가장 강한 보장이다. 한 client가 write를 끝낸 직후, 다른 client가 read하면 그 write가 반드시 보인다. global wall clock 시각에 맞춰진 단일 순서가 모든 노드에 일관되게 보이는 모델이다.

대가는 크다. 글로벌 strong consistency를 보장하려면 commit 전에 cross-region quorum 응답을 기다려야 한다 — latency가 region 간 RTT만큼 늘어난다. Spanner의 commit wait이 그 비용 중 하나다 (8장 callback). 거의 모든 시스템이 이 비용을 감당할 가치가 있는 자리는 매우 좁다 — 금융 거래, 글로벌 inventory, audit chain 같이 한 줄도 어긋나면 안 되는 자리.

### Sequential consistency — 단일 순서, but wall clock 자유

**sequential consistency**는 모든 노드가 같은 순서로 연산을 본다는 보장. 다만 그 순서가 실제 시간(wall clock)에 맞을 필요는 없다. "한 client가 A → B 순서로 호출하면 다른 모든 client에서도 A → B 순서로 보인다"가 핵심이다. linearizability보다 한 단계 약하지만, 분산 시스템에서 흔히 보는 보장이다.

### Causal consistency — 인과만 보존

**causal consistency**는 인과 관계가 있는 연산들의 순서만 보존한다. A가 B를 일으켰다면 모든 노드가 A를 먼저 본다. 인과 관계가 없는 연산들은 순서가 자유롭다. 8장에서 다룬 Lamport의 happens-before가 정확히 이 보장을 만든다.

흥미로운 점은 — **causal consistency는 HAT (Highly Available Transactions) 영역에서 도달 가능한 가장 강한 보장**이다. Bailis와 동료들이 2013년 발표한 *Highly Available Transactions* (P12)에서 정리한 결과다. 네트워크 partition이 일어나도 양쪽 partition에서 모두 진행이 가능하면서, causal 순서는 깨지지 않는다. multi-master·offline-first 시스템이 이 결을 따라간다 — Figma·Linear 같은 협업 도구가 대표 사례다 (15장 callback).

### Read-your-writes, monotonic reads — 약하지만 자주 필요한 보장

**read-your-writes** = "내가 방금 쓴 값은 내가 다시 읽으면 반드시 보인다." session 단위로 제공되는 보장이다. 캐시 layer가 있는 시스템에서 자주 깨지는데, 사용자 경험에 즉시 영향을 준다 — "방금 댓글 달았는데 새로고침하니 사라졌어요"의 정체. session affinity나 read 후 write까지 단일 노드로 라우팅하는 게 방어법이다.

**monotonic reads** = "내가 한 번 본 값보다 옛 값을 다시 보지는 않는다." 시간이 거꾸로 가는 듯한 광경을 막는다. 약하지만 사용자에게는 일관성의 최소 단위다.

### Eventual consistency — 가장 약한 보장

**eventual consistency**는 "충분한 시간이 지나면 결국 모든 노드가 같은 값을 본다"는 보장. 그 사이의 임시 불일치는 허용한다. Dynamo·Cassandra의 default이고, 캐시·CDN·검색 인덱스 같은 layer가 대부분 이 모델에서 작동한다.

여섯 단계의 강도 차이를 한 그림으로 그려 보자.

```
linearizability  >  sequential  >  causal  >  read-your-writes  >  monotonic reads  >  eventual
       강                                                                             약
   global wall                                                              "결국엔 같아짐"
```

이 사다리 어느 줄에 우리 시스템 데이터가 있는지 — 그게 회의 자리에서 동료에게 답하는 첫 단계다.

## 7. CAP → PACELC — 한 박자 더 정직한 trade-off

CAP 정리는 모두 들어봤을 거다. Eric Brewer가 2000년 conjecture로 제시했고, Gilbert·Lynch가 2002년에 증명했다(P31). "분산 시스템은 Consistency·Availability·Partition tolerance 중 두 가지만 동시에 만족할 수 있다." 단순하고 강력한 한 줄이다.

다만 CAP에는 함정이 하나 있다. **CAP가 가정하는 "partition"이 production에서 일어나는 시간은 매우 짧다**는 점이다. 한 시스템이 1년 중 99% 이상은 partition 없는 상태로 돈다. 그 99% 시간 동안 CAP는 답을 주지 않는다 — "consistency vs availability"는 partition 상황의 trade-off일 뿐이다.

그래서 Daniel Abadi가 2010년에 **PACELC** 확장을 제안했다(W17). 한 줄로 풀면 — **"Partition 시에는 A vs C(원래 CAP), Else에는 L(latency) vs C(consistency)."**

이 한 줄이 production의 진짜 trade-off를 잡는다. partition이 없는 99% 시간 동안에도, strong consistency를 원하면 commit 전에 multi-node 합의를 기다려야 한다 — latency가 늘어난다. eventual consistency를 받아들이면 즉시 응답할 수 있다. **이게 평상시 진짜 trade-off**다.

> "Eventual consistency is often chosen for performance reasons during normal operation, not just for partition resilience." — Abadi (W17)

PACELC 한 단어가 회의 자리에서 의외로 강력하다. "우리 시스템은 PA/EL입니다"라고 답할 수 있으면, 동료에게 partition·평상시 두 시나리오에서 무엇을 양보했는지를 한 줄로 전달한 셈이다.

### Abadi의 NewSQL 비판 — 한 박자 짚고 가기

Abadi는 같은 발표에서 NewSQL의 marketing에 한 가지 가시 같은 비판을 던졌다. **"Spanner의 default isolation level은 사실상 not serializable이다"**(W4 — 검증 필요, Abadi 원문 참조 권장). Spanner가 강한 consistency를 약속하지만, default가 snapshot isolation에 가까워 실제 serializable한 동시성 보장이 아니라는 지적이다.

NewSQL 도구들의 마케팅과 실제 보장 사이의 gap을 정직하게 보는 시각이 필요하다는 의미다. **"strong consistency"라는 단어를 도구 광고에서 봤다면, 정확히 어느 줄(linearizability? sequential? causal? snapshot isolation?)에 해당하는지 한 번 더 묻자.** 도구마다 그 단어가 다른 곳을 가리킨다.

## 8. CALM theorem — CRDT가 왜 가능한지의 이론적 근거

마지막으로 짚어 둘 한 가지 — **CALM theorem (Consistency As Logical Monotonicity, 2011, P6)**이다. Hellerstein과 동료들이 발표한 이 정리는 분산 시스템 이론에 한 가지 우아한 답을 제공한다 — **"coordination-free한 분산 계산이 가능한 조건은, 그 계산이 monotonic하다는 것이다."**

monotonic하다는 건 한 번 도달한 결과가 시간이 지나도 뒤집히지 않는다는 뜻이다. 집합에 원소를 추가하기만 하는 연산, max·min을 계산하는 연산, true가 되면 false로 안 돌아가는 flag 같은 게 monotonic이다. 반면 "원소를 추가도 하고 삭제도 한다"는 연산은 monotonic이 아니다 — 결과가 시간에 따라 뒤집힌다.

CALM의 핵심 함의는 — **"분산 시스템에서 coordination(합의·잠금) 없이 일관성을 얻고 싶다면, 데이터 모델을 monotonic하게 설계하라"**. 이게 CRDT(Conflict-free Replicated Data Type)의 이론적 근거다. CRDT는 union·max 같은 monotonic 연산만으로 구성된 자료구조라, multi-leader 환경에서도 conflict 없이 동작한다.

CALM의 실무적 가치는 — **"이 데이터에 합의가 필요한가, 아니면 monotonic 설계로 우회할 수 있는가"를 묻는 시각**이다. 예컨대 "총 좋아요 수" 같은 카운터는 add-only로 만들면 monotonic이라 합의가 필요 없다. "삭제 가능한 좋아요"라면 monotonic이 아니라 합의가 필요해진다. 작은 모델링 차이가 운영 비용을 결정한다.

15장에서 CRDT를 짧게 sidebar로 다룬다 — Figma multiplayer·local-first software의 수학적 기반이다. CALM theorem이 그 영역의 출발점이라는 사실만 여기 박아 두자.

## 9. 한국 사례 — 카카오뱅크 99.99% 가용성과 합의의 자리

한국 백엔드 시각으로 합의·일관성이 가장 두드러지는 자리는 금융이다. **카카오뱅크의 99.99% 가용성**(W41)은 이 챕터의 사고법이 production에 어떻게 적용되는지를 보여주는 한 가지 사례다.

99.99%라는 숫자는 한 해 약 53분의 다운타임을 허용한다는 뜻이다. 결제·송금이라는 critical path에서 이 정도를 지키려면 — single-leader RDB의 failover 시간 자체가 SLO budget의 큰 비중을 차지한다. 그래서 카카오뱅크는 메인프레임에서 MSA로 옮겨가면서, **각 도메인의 SLO를 따로 측정하고 각자 적합한 일관성·복제 모델을 골랐다**고 발표에서 짚는다 (검증 필요 — 발표 원문 확인 권장).

핵심은 두 가지다. ① **모든 도메인에 strong consistency를 강제하지 않는다.** 정산은 strong, 알림은 eventual, audit log는 strong + append-only. 도메인마다 그 사다리의 다른 줄에 위치한다. ② **합의가 정말 필요한 자리(이체·결제)와 그렇지 않은 자리(통계·푸시)를 가르는 게 운영 비용을 결정한다.** 모든 데이터에 합의를 강제하면 latency가 무너지고, 모든 데이터에 eventual을 허용하면 audit가 깨진다.

이 결정 패턴이 19장 결제 챕터에서 한 번 더 깊이 다뤄진다. 이 챕터의 사고 도구가 케이스 스터디에서 어떻게 작동하는지 그때 본다.

## 10. 의사결정 트리 — 우리 데이터에 어떤 일관성이 필요한가

여기까지의 어휘를 가지고, 실무에서 한 박자 안에 던질 수 있는 질문 5개를 정리해 두자.

1. **이 데이터가 어긋나면 어떤 손해가 나는가?** 금융·재고 같은 자리는 strong (linearizability·serializable isolation). UI 보여주기·통계는 eventual로 충분.
2. **글로벌 다중 region이 필요한가?** No라면 single-leader RDB로 충분. Yes라면 PACELC를 분명히 정하고 들어가자 — PA/EL이면 multi-leader 또는 leaderless + CRDT, PC/EC이면 Spanner·CockroachDB 계열.
3. **사용자 경험에 필요한 최소 보장은 무엇인가?** read-your-writes·monotonic reads는 약해 보여도 사용자 경험의 바닥이다. session affinity·write-after-read 같은 기본 도구를 챙기자.
4. **데이터 모델을 monotonic하게 설계할 수 있는가?** Yes라면 합의 없이 CRDT로 갈 수 있다. add-only counter, set union, max·min 같은 모양이 monotonic의 후보.
5. **이 결정을 우리 도메인 언어로 설명할 수 있는가?** "Cassandra가 빠르니까"가 아니라 "우리 워크로드는 PA/EL이라 eventual을 허용하지만 read-your-writes는 session affinity로 보장한다"로 말할 수 있는가.

이 다섯 물음을 들고 회의 자리에 가면, 동료의 "strong consistency 필요한가요?" 질문에 첫 5분 안에 답할 수 있다.

## 11. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 분산 합의·복제·일관성이라는 어려운 영역의 지형이 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **FLP impossibility** — 분산 합의는 trade-off의 산물이다. Paxos·Raft·ZAB가 무엇을 양보해서 어떻게 가능하게 만들었는지 알고 도입하자.
- **Raft가 사실상 산업 표준이다.** etcd·Consul·CockroachDB·Kafka KRaft 모두 Raft 위에 있다. Paxos를 외울 필요는 없지만, 그 그림자 안에 있다는 사실은 기억하자.
- **합의 알고리즘 선택보다 layer 수가 더 큰 변수다.** Kafka가 ZooKeeper를 떼어내고 KRaft로 옮긴 결정이 이 진실을 보여 준다.
- **Replication 세 갈래** — single-leader가 90% 시스템의 default. multi-leader·leaderless는 강한 정당화가 있어야 한다.
- **일관성 사다리 6단계** — linearizability → sequential → causal → read-your-writes → monotonic reads → eventual. 우리 데이터가 어느 줄에 있는지 한 박자에 답할 수 있는 어휘다.
- **CAP보다 PACELC가 정직하다.** partition 없는 99% 시간의 latency vs consistency가 진짜 trade-off다. "우리는 PA/EL입니다"라고 답할 수 있는 시스템이 되자 — 그게 새벽 3시의 자신을 살린다.
- **CALM theorem** — coordination-free = monotonic의 동치. CRDT의 이론적 근거이자, 데이터 모델 설계가 운영 비용을 결정한다는 시각.
- **카카오뱅크의 패턴** — 모든 도메인에 같은 일관성을 강제하지 않는다. 정산은 strong, 알림은 eventual. 도메인마다 사다리의 다른 줄을 고르는 게 99.99% SLO의 비결.

다음 장(13장)에서는 샤딩과 파티셔닝을 짚는다. "트래픽 10배가 와도 무너지지 않는 시스템은 무엇을 미리 정해 두었는가" — 이 질문에 답하려면 합의의 자리에서 한 박자 내려와, 데이터를 수평으로 가르는 사고법이 필요하다. 함께 들여다보자.


---

# 13장. 샤딩·파티셔닝·Fan-out — 수평으로 늘리는 기술

Sharding key를 잘 골랐다고 자신했던 어떤 팀이 있다. 새 시스템 출시일, 모든 부하 테스트가 통과했고, 데이터 분포 시뮬레이션도 정상이었다. 그런데 출시 30분 만에 한 partition이 전체 트래픽의 95%를 받고 있는 광경을 목격한다. 알고 보니 그날 어떤 인플루언서가 자기 SNS에 우리 서비스 링크를 올렸다. 그 한 사람의 ID가 모든 트래픽을 한 partition으로 몰아넣었다.

이 순간 "celebrity"라는 단어가 단순한 비유가 아니라 진짜 운영 용어가 된다. 우리 시스템에는 항상 celebrity가 있고, sharding 설계는 그 celebrity의 존재를 가정해야 한다. 그게 이 챕터의 출발점이다.

수평 확장(horizontal scaling)이 분산 시스템의 핵심 약속이라면, 그 약속을 가능하게 하는 것이 sharding(또는 partitioning)이다. sharding의 세 방식, consistent hashing의 모양, hot partition을 만드는 5가지 안티패턴, fan-out 패턴(push/pull/hybrid), 그리고 re-sharding의 잔혹함까지 — 한 박자씩 짚어 보자. 한국 사례로 당근 동(neighborhood) 단위 partition도 함께 본다.

## Sharding의 세 가지 방식 — Range, Hash, Directory

데이터를 여러 노드에 나눠 두는 방법은 크게 세 가지다. 각각 다른 trade-off를 갖는다.

### Range-based — 정렬된 key 범위로 분할

key 범위를 노드별로 나눈다. Bigtable, HBase, MongoDB(기본)이 이 모델이다.

```
shard 1: key A-F
shard 2: key G-M
shard 3: key N-S
shard 4: key T-Z
```

장점은 **범위 쿼리가 효율적**이라는 점. `WHERE name BETWEEN 'C' AND 'E'`는 shard 1만 보면 끝난다.

단점은 **hot partition이 잘 생긴다**는 점. 만약 key가 timestamp라면 최신 데이터가 항상 한 shard로 몰린다. 모든 write가 마지막 shard에 가는 상태가 된다.

### Hash-based — 해시값으로 균등 분할

key를 hash 함수에 통과시켜 그 결과로 shard를 정한다. Dynamo, Cassandra, Riak이 이 모델이다.

```
shard_id = hash(key) % N
```

장점은 **균등 분포**가 자연스럽다. timestamp가 key라도, hash가 충돌하지 않으면 모든 shard에 균등하게 흩어진다.

단점은 **범위 쿼리가 불가능**하다는 점. `WHERE timestamp BETWEEN ...`은 모든 shard를 다 봐야 한다. 그리고 **노드 추가·제거 시 거의 모든 key가 재배치**된다. `hash % 4`에서 `hash % 5`로 바뀌면 약 80%의 key가 다른 shard로 이동한다.

### Directory-based — 명시적 매핑

별도의 lookup table이 "이 key는 어느 shard"를 알려 준다. Vitess의 VSchema, MongoDB의 일부 sharding 모드가 이 모델이다.

```
lookup table:
  shop_id 100 → shard 1
  shop_id 101 → shard 1
  shop_id 102 → shard 2
  ...
```

장점은 **유연성**. 특정 shop을 다른 shard로 옮기고 싶으면 lookup table만 갱신하면 된다. hot tenant를 별도 shard로 분리하는 식의 운영이 가능하다.

단점은 **lookup table 자체가 SPOF**가 될 수 있다는 점. 이걸 잘 분산·캐싱해야 한다.

| 방식 | 분포 균등성 | 범위 쿼리 | 재배치 부담 | 대표 사례 |
|------|-----------|---------|------------|---------|
| Range-based | 약함 (hot partition 위험) | 강함 | 노드 추가 시 일부 재배치 | Bigtable, HBase |
| Hash-based | 강함 | 약함 | 노드 추가 시 거의 전체 | Dynamo, Cassandra |
| Directory-based | 운영자 결정 | 약함 | 명시적 마이그레이션 | Vitess, MongoDB (일부) |

## Consistent Hashing — Hash-based의 진화

Hash-based의 가장 큰 약점이 "노드 추가·제거 시 거의 전체 재배치"였다. 이 문제를 푸는 자료구조가 **consistent hashing**이다.

핵심 아이디어는 단순하다. hash 결과 공간을 ring으로 시각화하고, 각 노드를 ring 위 여러 지점에 배치한다. key의 hash가 떨어지는 지점에서 ring을 따라 시계 방향으로 가다가 처음 만나는 노드가 그 key를 소유한다.

```
Ring (0 ~ 2^32):
   Node A: 위치 10, 100, 1000, ... (여러 vnode)
   Node B: 위치 50, 200, 500, ...
   Node C: 위치 30, 300, 800, ...
   
key X의 hash = 250 → 다음 노드가 Node B → Node B가 소유
```

노드 D를 추가하면? D를 ring 위 여러 지점에 배치하면, **D 주변의 일부 key만** D로 이동한다. 다른 노드는 그대로다. 평균적으로 `K/N` 만큼의 key만 이동한다 (K=전체 key, N=노드 수).

여기서 중요한 디테일이 **virtual node**(vnode)다. 노드를 ring 위 한 지점에만 두면 분포가 불균등해진다. 각 노드를 100~200개의 vnode로 ring에 흩어 놓으면 분포가 균등해진다.

> 노드당 100~200 vnode가 일반적. Dynamo·Cassandra·Riak·memcached(client-side) 모두 채택. (ByteByteGo, Consistent Hashing 101)

Consistent hashing은 캐시 cluster(Memcached, Redis Cluster)와 분산 DB(Dynamo, Cassandra)의 backbone이다. 이 모양 없이 큰 분산 시스템을 운영하는 건 거의 불가능하다.

## Hot Partition을 만드는 5가지 안티패턴

2장 NoSQL에서 hot partition은 "평생의 적"이라고 말했다. 그 적을 만드는 5가지 안티패턴을 정리하자. 새 시스템의 sharding key를 정할 때 자기 코드를 한 번 체크해 보자.

### 안티패턴 1. Timestamp를 partition key로

```
PRIMARY KEY (created_at, ...)
```

최신 데이터가 모두 한 partition으로 몰린다. write-heavy 시스템이라면 그 partition은 5분도 못 버틴다.

**해결:** date를 day 단위로 자르고 user_id나 다른 차원과 조합. 예: `PRIMARY KEY ((user_id, date_bucket), ...)`.

### 안티패턴 2. Boolean 또는 enum을 partition key로

```
PRIMARY KEY (status, ...)  -- status: PENDING / COMPLETED / FAILED
```

distinct 값이 3개뿐이라 3개 partition만 쓴다. 나머지 노드는 모두 idle.

**해결:** 더 cardinality가 높은 차원을 partition key로. status는 secondary index로.

### 안티패턴 3. Celebrity user를 가정 안 함

```
PRIMARY KEY (user_id, ...)
```

대부분 user는 100개씩 row를 가지는데, 한 celebrity user는 1억 row를 가질 수 있다. 그 user의 partition이 비대해진다.

**해결:** celebrity의 데이터를 별도 partition으로 분리 (Twitter의 fanout-on-read 모델 참고).

### 안티패턴 4. Sequential ID를 partition key로

```
PRIMARY KEY (id, ...)  -- id가 auto-increment
```

새 row가 모두 마지막 partition으로 간다 (range-based 시). 또는 hash-based여도 cardinality는 높지만 한 partition 안에 너무 많은 row가 쌓일 수 있다.

**해결:** prefix 또는 hash 첨가로 분산.

### 안티패턴 5. Compound key의 첫 컬럼만 보고 분포 가정

```
PRIMARY KEY ((tenant_id, doc_id), ...)
```

tenant_id가 균등 분포라고 가정. 실제로는 한 tenant가 전체 트래픽의 95%인 경우.

**해결:** tenant 단위 분포 분석 + hot tenant 분리.

## 분포 검증의 두 가지 방법

sharding key를 정했다면 분포를 미리 검증해야 한다. 두 가지 방법이 있다.

**1. Production data sample을 hash로 시뮬레이션.** 실제 데이터에서 1만 row sample을 뽑아 sharding key로 hash해 본다. 분포가 균등한지 시각화. 한 partition에 5% 이상 몰리면 안티패턴 의심.

**2. Top-N partition 모니터링.** production에서 partition별 read·write 빈도를 모니터링한다. Top 10 partition이 전체의 50% 이상을 받고 있다면 hot partition 발생 중.

Cassandra에서는 `nodetool tablestats`, DynamoDB에서는 CloudWatch의 ConsumedCapacity per partition으로 확인할 수 있다. 이런 모니터링이 없으면 hot partition은 5분 만의 사고로만 보이고, 그제야 원인을 찾기 시작한다.

## Shopify Pods — Directory-based의 모범 답

한 가지 흥미로운 사례가 Shopify의 pods 아키텍처다. Shopify는 수백만 개의 상점(shop)을 호스팅하는 SaaS다. 각 상점의 트래픽이 크게 다르고, BFCM(Black Friday/Cyber Monday) 시점에 일부 상점이 폭주한다.

Shopify는 **pods**라는 단위를 도입했다. 각 pod은 완전 독립된 MySQL cluster + Redis + 배경 인프라다. shop_id가 어느 pod에 속할지를 directory table이 관리한다.

```
shop 12345 → pod-3
shop 67890 → pod-3
shop 11111 → pod-7
```

이 모양의 장점이 크다.

**1. 운영 격리.** pod-3에 사고가 나도 pod-7은 영향 없다. blast radius가 한 pod으로 한정.
**2. Hot tenant 분리.** 폭주하는 shop이 있으면 그 shop을 자기만의 pod으로 옮길 수 있다.
**3. 점진적 마이그레이션.** 새 기능을 한 pod에만 먼저 배포해 보고, 안정되면 전체로 확장.

Shopify 엔지니어링의 한 줄이 이 결정을 정리한다.

> Only the databases are podded since they are the hardest component to scale, and everything else that is stateless is scaled automatically. (Shopify Engineering)

DB만 pod 단위로 격리하고, 나머지 stateless 컴포넌트는 K8s autoscale로 처리. 운영 부담을 분산 SQL(CockroachDB·Spanner)으로 가는 대신 directory-based sharding으로 푼 사례다.

## Fan-out — Push / Pull / Hybrid

Sharding이 데이터를 가르는 패턴이라면, **fan-out**은 한 이벤트를 여러 대상에 분배하는 패턴이다. 가장 흔한 예가 SNS의 timeline이다.

A가 트윗 한 개를 올렸다. A를 팔로우하는 사람이 1만 명이라면, 그 트윗은 1만 명의 home timeline에 도달해야 한다. 이 1:N 분배를 어떻게 구현할까? 세 가지 모델이 있다.

### Fanout-on-write (Push)

A가 트윗을 올리는 순간, A의 1만 follower의 home timeline에 그 트윗을 미리 분배한다.

```
A의 트윗 → 1만 follower의 timeline cache(예: Redis sorted set)에 모두 insert
```

**장점:** read가 매우 빠르다. follower가 home을 열면 자기 timeline cache를 그대로 read.
**단점:** write가 비싸다. follower가 1만이면 write 1번이 1만 번의 cache insert가 된다.

### Fanout-on-read (Pull)

A가 트윗을 올린다. 다른 곳에 분배하지 않는다. follower가 home을 열 때, follower가 팔로우하는 모든 user의 최근 트윗을 모아 정렬한다.

```
follower B의 home 열기 → B가 팔로우하는 user들의 최근 트윗 모두 read → merge sort
```

**장점:** write가 싸다. 트윗 1번은 그냥 자기 timeline에 1 insert.
**단점:** read가 비싸다. 1000명 팔로우 중인 B가 home을 열면 1000명의 트윗을 read해야 한다.

### Hybrid — 둘을 결합

Twitter, Instagram 같은 큰 SNS의 결정은 hybrid다.

- **일반 사용자:** fanout-on-write (push). follower 수가 적어 cost가 낮음.
- **Celebrity (10K+ followers):** fanout-on-read (pull). 한 트윗으로 100만 cache insert는 감당 불가.

follower가 home을 열 때, push로 받은 일반 사용자 트윗 + pull로 가져온 celebrity 트윗을 merge한다. follow 시점에 user별로 push/pull 모드가 결정되어 있다.

이 hybrid 모양이 Twitter, Instagram, Facebook 등의 home timeline 표준이다. 한국에서는 LINE, 카카오스토리, 인스타그램(한국) 모두 비슷한 모양을 쓴다.

> 💡 celebrity 임계 기준 — Twitter는 10K, Instagram은 1K~10K. 도메인마다 다르다. 자기 시스템에서는 **fanout cost가 user별로 어떻게 분포되는지 미리 시뮬레이션**해서 임계를 정하는 편이 낫다.

## 한국 사례 — 당근 동(neighborhood) 단위 partition

당근마켓의 sharding은 특이하다. 일반 SNS는 user_id로 partition하지만, 당근은 **지역(동)** 단위로 partition한다. 왜?

당근의 핵심 도메인은 hyperlocal 거래다. 사용자가 보는 채팅·검색·매물은 모두 자기 동(neighborhood) 안의 데이터다. 그래서 user_id 대신 region_id로 partition하면 다음 이득이 생긴다.

**1. Locality.** 한 사용자의 모든 쿼리가 한 partition으로 간다. cross-partition 쿼리가 거의 없음.
**2. Cache 친화적.** 같은 동 사람들이 같은 데이터를 보니 cache hit이 높다.
**3. Hot region 격리.** 강남·송파처럼 활성도 높은 지역은 별도 partition으로 분리 가능.

당근 채팅 시스템(W31)이 DynamoDB를 채택하면서 동 단위 partition을 채택한 이유가 이거다. AWS Summit Korea 2022 "2200만 사용자를 위한 채팅 시스템 아키텍처"에서 변규현 발표자가 정확히 짚었다. **"hyperlocal 도메인이라면 partition도 hyperlocal이어야 한다."**

이 결정은 도메인이 sharding key를 결정한 사례다. 일반적인 "user_id로 partition"이 모든 시스템의 답은 아니다. 자기 도메인의 본질이 무엇인지 보고, 그 본질에 맞는 partition key를 골라야 한다.

## Re-sharding의 잔혹함

sharding key를 한 번 정하면 바꾸기 매우 어렵다. 그래서 신중하게 정해야 하지만, 그래도 결국 re-shard가 필요한 순간이 온다. 데이터가 커지거나, partition key 결정이 잘못된 게 늦게 발견되거나, 도메인이 변하거나.

re-sharding의 표준 패턴은 다음 4단계다.

```
1. Dual-write: 새 shard와 옛 shard에 모두 write 시작
2. Backfill: 옛 shard의 모든 데이터를 새 shard로 복제
3. Shadow read: 새 shard에서도 read 시작, 옛 shard 결과와 비교 (consistency 검증)
4. Cutover: 새 shard로 read·write 모두 전환, 옛 shard 정리
```

이 패턴은 단순해 보이지만 끔찍한 디테일이 많다.

**1. Dual-write 일관성.** 두 shard에 write가 atomic하지 않으니, 한쪽만 성공하는 경우가 생긴다. retry + idempotency로 해결.

**2. Backfill 시간.** TB급 데이터라면 backfill에 며칠~몇 주가 걸린다. 그 사이 dual-write 부담도 지속.

**3. Consistency 검증.** shadow read에서 두 shard의 결과가 다른 경우, 어느 쪽이 맞는지 판단해야 한다. 당근의 Cassandra → DynamoDB 마이그레이션에서 가장 큰 도전이 이 부분이었다(community 패턴 10).

**4. Rollback 가능성.** cutover 후 문제가 발견되면 옛 shard로 돌아갈 수 있어야 한다. cutover 직후 며칠은 옛 shard도 유지.

re-sharding을 한 번이라도 해본 팀은 그 잔혹함을 평생 기억한다. 그래서 **처음에 sharding key를 정할 때 다음 5년의 트래픽 패턴을 충분히 시뮬레이션**하는 편이 낫다. 또는 directory-based를 채택해 운영 시 유연성을 확보하는 것도 방법이다.

## Cross-region Replication — 광역 분산의 trade-off

마지막으로 광역 분산(multi-region)을 짚자. 단일 region 안에서의 sharding이 끝나면, 다음 단계는 region 단위 분산이다. AWS의 us-east-1과 ap-northeast-2에 데이터를 모두 두는 식.

이 결정의 trade-off는 **latency와 consistency**다.

**1. Active-Passive.** 한 region이 primary, 다른 region은 replica (DR용). write는 항상 primary로, read는 양쪽 가능. failover 시 primary 전환.

**2. Active-Active.** 두 region 모두 write 가능. 같은 데이터에 두 region에서 동시 write 시 conflict resolution 필요.

**3. Geo-partition.** 한 region이 한국 사용자, 다른 region이 일본 사용자. 데이터 자체가 region별로 갈림.

| 모델 | latency | consistency | 운영 복잡도 |
|------|---------|------------|----------|
| Active-Passive | primary 가까운 곳만 빠름 | strong (single primary) | 보통 |
| Active-Active | 모든 region에서 빠름 | conflict resolution 필요 | 매우 높음 |
| Geo-partition | region별 사용자만 빠름 | region 내 strong | 보통 |

Spanner·CockroachDB가 active-active를 약속하지만, 그 비용은 commit wait 또는 cross-region round-trip이다. 한국 백엔드의 90%는 active-passive(DR용)로 충분하다. active-active가 정말 필요한 경우는 글로벌 서비스(LINE 메시징, 카카오엔터 글로벌 콘텐츠 등)에 한정.

## Sharding 도입 자격을 묻는 5가지 질문

새 시스템에 sharding을 도입하기 전에 자기에게 던질 다섯이다.

1. **단일 DB로 정말 안 되는가?** Postgres·MySQL의 single primary는 수십만 QPS까지 견딘다. 한계가 명확히 보인 후에야 sharding.
2. **partition key가 자기 도메인의 본질을 반영하는가?** user_id가 default지만, hyperlocal·tenant·time 등 다른 차원이 맞을 수 있다.
3. **hot partition 가능성을 시뮬레이션했는가?** 5가지 안티패턴 중 어느 하나에 해당하지 않는지 검증.
4. **re-shard rollout plan을 가지고 있는가?** 처음 정한 key가 잘못됐을 때 어떻게 옮길지 미리 준비.
5. **fan-out이 필요한가, 그렇다면 push/pull/hybrid 중 무엇이 맞는가?** celebrity의 존재가 fan-out 모델을 결정.

이 다섯에 답이 명확하지 않으면 sharding을 미루는 편이 낫다. 단일 DB로 시작해서 한계가 오면 그때 sharding을 도입해도 늦지 않다.

## Callback 예고

13장의 sharding·fan-out은 후속 챕터에서 핵심 패턴으로 등장한다.

- **17장 피드·타임라인.** Twitter·Instagram·카카오스토리의 hybrid fan-out 구조.
- **18장 검색·매칭·지오.** Uber H3, 당근 거래 매칭의 geo partition.
- **19장 결제·금융.** 토스 코어뱅킹의 user 단위 partition + 거래 history sharding.

이 챕터의 5가지 안티패턴이 머릿속에 있어야 후속 케이스 스터디의 sharding 결정이 따라온다.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 수평 확장의 세 패턴이 손에 잡혀 있다. Range/Hash/Directory 세 sharding 방식, consistent hashing의 ring 모양과 vnode, hot partition을 만드는 5가지 안티패턴, fan-out의 push/pull/hybrid 결정, Shopify pods와 당근 동 단위 partition의 사례, 그리고 re-sharding의 잔혹함과 광역 분산의 trade-off까지가 한 묶음이다.

기억해두자. sharding은 한 번 정하면 바꾸기 어려운 결정이다. partition key를 한 번 잘못 정하면 5년의 운영 부담으로 돌아온다. 그래서 처음에 자기 도메인의 본질을 정확히 보고 key를 정하는 편이 낫다. 그리고 항상 **celebrity가 존재한다**는 사실을 가정하자. 그 가정이 없는 sharding은 출시 30분 만에 무너진다.

다음 장에서는 시스템이 자기 자신을 보는 법을 살펴본다. Rate limiting, 백프레셔, SLO, 관측성, on-call. 분산 시스템을 만드는 것만큼 운영하는 일이 어렵다는 사실을, 그 운영에 필요한 부품들과 함께 짚어 보자.

---

# 14장. Rate Limiting·백프레셔·SLO·관측성·on-call — 시스템이 자기 자신을 보는 법

어떤 팀의 alert가 새벽 3시에 울렸다고 해보자. on-call 엔지니어가 컴퓨터를 켜고 보니, 5분 안에 자동 해결된 일이었다. 같은 alert가 그 주에만 11번 울렸다. 한 달 뒤 그 엔지니어는 퇴사했다.

on-call burnout은 alert 설계의 실패다. 사람을 깨우는 모든 page는 그만한 가치가 있어야 한다. Charity Majors의 한 줄이 정확히 짚었다 — "**3am에 사람이 할 게 없으면 page 보내지 마라**." 이 한 문장이 운영 문화의 핵심이고, 동시에 우리 시스템이 자기 자신을 보는 능력의 척도다.

시스템이 자기 한계를 표현하는 5가지 도구가 있다. Rate limiting, backpressure, SLO/Error Budget, 관측성 3-pillar, 배포 전략, chaos engineering. 그리고 그 위에 얹히는 운영 문화 — blameless postmortem, on-call humanism. 빌딩 블록과 패턴을 다 갖춘 시스템이 production에서 살아남으려면 이 도구들이 모두 깔려 있어야 한다. 한 박자씩 짚어 보자.

## Rate Limiting — 자기 처리량을 외부에 알리는 법

Rate limiting은 시스템이 "나는 분당 N개까지만 처리할 수 있다"고 외부에 선언하는 도구다. 잘 깔린 rate limiter는 시스템 한계 이상의 트래픽이 들어오기 전에 일부를 거절(429 Too Many Requests)해, 시스템 자체가 무너지지 않게 한다.

Cloudflare 사내 블로그가 정리한 5가지 알고리즘을 보자.

### 1. Token Bucket — Default

매 초 N개씩 token이 bucket에 추가된다. 요청이 올 때마다 token 1개를 꺼낸다. bucket이 비면 거절.

```
bucket capacity: 100 (burst 허용)
refill rate: 10/sec
요청 들어옴 → token 1개 차감 (남으면 통과, 없으면 거절)
```

장점: **burst 허용**. 순간 burst가 와도 capacity 안에서는 통과. AWS API의 client-side throttling이 이 모델이다.

### 2. Leaky Bucket — Constant Egress

요청을 큐에 쌓고, 일정 속도로만 처리. burst가 와도 출력 속도는 일정.

```
incoming → queue → constant rate output
```

장점: **smooth output**. 단점: burst 거부, queue가 가득 차면 drop.

### 3. Fixed Window

1분 단위로 카운터. "이 분에 100개 처리"하면 다음 요청은 다음 분까지 거절.

```
00:00 - 00:59: 100 requests
01:00 - 01:59: 카운터 reset
```

단점: **boundary burst 문제**. 00:59에 100개 + 01:00에 100개 = 1초 안에 200개 가능.

### 4. Sliding Window Log — 정확

모든 요청의 timestamp를 저장. 최근 1분 안의 요청 수가 임계 넘는지 체크.

```
log = [00:01, 00:15, 00:42, ...]
새 요청 시 1분 이전 timestamp 모두 삭제 + 남은 수 체크
```

장점: 가장 정확. 단점: **메모리 비싸다**. 요청마다 timestamp 저장.

### 5. Sliding Window Counter — Cloudflare Default

두 fixed window의 가중평균.

```
현재 window 카운트 + (이전 window 카운트 × 남은 시간 비율)
```

Cloudflare 실측 0.003% error로 사실상 표준. 정확도와 메모리 효율의 균형.

| 알고리즘 | burst 허용 | 정확도 | 메모리 | 추천 |
|---------|-----------|--------|--------|------|
| Token bucket | yes | medium | 작음 | 일반 API default |
| Leaky bucket | no | high | 중간 | smooth output 필요 시 |
| Fixed window | yes (boundary) | 낮음 | 작음 | 단순 구현 |
| Sliding window log | yes | 매우 높음 | 큼 | 정확도 critical |
| Sliding window counter | yes | 매우 높음 | 작음 | **default 권장** |

### 분산 Rate Limit 구현

여러 server가 같은 limit을 공유하려면 중앙 카운터가 필요하다. Redis가 표준이다.

```lua
-- Lua script (atomic)
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local current = redis.call('INCR', key)
if current == 1 then
    redis.call('EXPIRE', key, 60)  -- 1분 window
end
if current > limit then
    return 0  -- 거절
end
return 1  -- 통과
```

Lua script로 INCR + EXPIRE를 atomic하게 처리한다. 분산 server들이 모두 같은 Redis key를 보니 글로벌 rate limit이 자연스럽게 가능하다.

복잡한 시스템에서는 **hierarchical token bucket**을 쓴다 — 전역 limit, 사용자별 limit, endpoint별 limit이 계층적으로 적용. AWS API Gateway가 이 모델이다.

## 백프레셔 — Producer가 Consumer를 살린다

Rate limiting이 "외부 → 우리"의 흐름을 제어하면, **백프레셔**(backpressure)는 "우리 내부의 빠른 producer → 느린 consumer" 흐름을 제어한다.

상황을 가정해 보자. service A가 service B에 1초에 1000개 메시지를 보낸다. B는 100개밖에 처리 못한다. A는 어떻게 알 수 있을까?

답은 **B가 A에게 "천천히"라고 말하는 것**이다. 그 신호가 백프레셔다.

표준 패턴들이 있다.

**1. Reactive Streams.** Java 9+, Node.js, Project Reactor의 표준. consumer가 producer에게 `request(N)`을 보내 N개만큼만 요청. consumer가 처리 가능할 때만 다음 N개.

**2. gRPC Flow Control.** HTTP/2 기반의 flow control. 각 stream에 window size가 있고, consumer가 ACK 보낼 때까지 producer가 새 데이터를 못 보냄.

**3. Kafka Consumer Poll Throttling.** consumer가 poll 속도를 조절. lag이 쌓이면 fetch 빈도를 줄임. broker가 backpressure 신호를 producer로 전달하지는 않지만, lag 모니터링으로 producer 측에서 결정.

**4. Queue 길이.** 가장 단순. consumer 앞의 큐 길이가 임계 넘으면 producer에 "stop"을 보낸다. 큐 길이가 시스템 건강의 1차 신호.

> 💡 큐 길이의 한 줄 통찰 — **producer는 queue 길이를 보고 자기 속도를 결정하라.** consumer의 처리 속도가 아니라 queue 길이로 판단해야 한다. consumer가 일시적으로 빠르더라도 queue가 차 있으면 system이 따라가지 못하는 것.

## SLI / SLO / Error Budget — "100%는 잘못된 목표다"

Google SRE Book이 분산 시스템 운영의 표준을 정립했다. 가장 큰 기여 중 하나가 **SLI / SLO / Error Budget**이라는 어휘다.

- **SLI (Service Level Indicator):** 시스템 건강 지표. "성공률", "p99 latency", "처리량".
- **SLO (Service Level Objective):** SLI의 목표값. "성공률 99.9%", "p99 latency < 500ms".
- **SLA (Service Level Agreement):** 외부 약속, 위반 시 비용 (보통 환불). SLO보다 약간 느슨하게.
- **Error Budget:** 100% - SLO. "한 달에 0.1% (43분) 동안 장애 허용."

이 어휘의 가장 큰 통찰은 — **100%는 잘못된 목표다.**

100% 안정성은 무한 비용이다. 99.99% (year에 52분 다운)에서 99.999% (5분 다운)로 가려면 비용이 10배 든다. 사용자 대부분은 그 차이를 못 느낀다. 그래서 SLO를 90%·95%·99%·99.9% 등 도메인에 맞춰 정하고, **그 안의 error budget을 새 기능 출시에 자유롭게 쓴다**는 모델이 합리적이다.

```
SLO 99.9% → error budget 0.1% (한 달 43분)

이번 달:
- 신규 기능 배포로 12분 장애
- 인프라 장애로 8분
- 합계 20분 사용 (남은 budget 23분)
→ 자유롭게 새 기능 배포 가능

다음 달:
- 큰 장애로 50분 다운
→ budget 초과 → 새 기능 freeze, 안정성에 집중
```

이 모양이 **release 속도와 안정성의 협상 테이블**이다. SRE팀이 "더 안전하게"라고만 외치고 product팀이 "더 빨리"라고만 외치면 갈등이 끝나지 않는다. error budget이 그 갈등을 데이터로 풀어 준다.

### Burn Rate Alerting

SLO를 모니터링할 때 단순 임계 alerting은 함정이 많다. "99.9% 미만이면 alert"는 noisy alert를 만든다.

표준은 **multi-window multi-burn-rate alerting**이다. error budget을 소진하는 속도를 본다.

```
fast burn (1시간 window):
  1시간 안에 한 달치 budget의 2%를 소진 → 즉시 page

slow burn (6시간 window):
  6시간 안에 한 달치 budget의 5%를 소진 → 1시간 후 page

dlow burn (3일 window):
  3일 안에 한 달치 budget의 10%를 소진 → 다음 영업일 ticket
```

이 multi-window는 fast/slow burn 각각에 맞는 응답을 만든다. 빠른 장애엔 page, 느린 누수엔 ticket. 새벽 3시에 ticket으로 깨지 않는다.

## Three Pillars of Observability — Logs · Metrics · Traces

시스템이 자기 상태를 외부에 보여 주는 3가지 차원이 **logs, metrics, traces**다.

| 차원 | 무엇을 본다 | 대표 도구 |
|------|-----------|---------|
| Logs | 어떤 일이 일어났는가 (events) | ELK·Loki·CloudWatch |
| Metrics | 얼마나 자주·어느 정도 (aggregations) | Prometheus·Datadog |
| Traces | 한 요청이 어디를 거쳤는가 (request flow) | Jaeger·Zipkin·OpenTelemetry |

이 셋이 보완 관계다. 한 가지만 가지고는 production 디버깅이 어렵다.

### OpenTelemetry — vendor lock-in 깨기

2022년경부터 CNCF 표준이 된 **OpenTelemetry**가 관측성 영역에 큰 변화를 만들었다. 핵심은 **OTLP wire format으로 logs·metrics·traces를 통일**한 것.

```
application → OpenTelemetry SDK → OTLP → OTel Collector → 어떤 backend든
```

application code는 OTel SDK만 알면 된다. Collector가 batching·filtering·routing을 처리하고, 어느 backend(Datadog·NewRelic·Jaeger·Prometheus)든 보낼 수 있다. vendor lock-in이 깨졌다.

그리고 가장 강력한 기능이 **trace_id correlation**이다. 한 요청에 trace_id가 부여되면, 그 trace_id가 logs·metrics·traces에 모두 박힌다. 한 요청을 따라가면서 3 pillar를 한 화면에서 본다.

### 로그 철학 — "Logs are events, not strings"

Charity Majors의 한 줄이 wide-event observability를 정리한다.

> Logs should be wide events with high cardinality, not just strings. (휴리스틱 7)

전통 로그는 string이다. `"User 12345 logged in"`. 이 문자열을 parse하기 어렵고, 검색이 비효율적이다.

wide-event 로그는 structured object다.

```json
{
  "event": "user_login",
  "user_id": 12345,
  "device": "ios",
  "ip": "1.2.3.4",
  "auth_method": "password",
  "duration_ms": 230,
  "trace_id": "abc123",
  ...
}
```

cardinality (distinct value 수)가 매우 높은 필드를 자유롭게 박는다. 디버깅 시 "device=ios && duration_ms > 1000인 login 이벤트"를 즉시 query 가능. Honeycomb, Datadog가 이 모델로 인기.

### Cardinality 관리

metrics는 반대 방향이다. cardinality가 너무 높으면 storage·CPU가 폭증한다. label에 user_id를 넣으면 안 되는 이유다 — distinct user 수만큼 series가 만들어진다. Prometheus가 1억 series로 메모리 폭발하는 사고가 자주 일어난다.

원칙: **logs는 high cardinality OK, metrics는 low cardinality.**

### Sampling 전략

traces는 모두 저장하면 storage가 폭증한다. sampling이 필수.

- **Head sampling.** 요청 시작 시점에 10% 비율로 결정. 단순하지만 error trace가 sampling으로 빠질 수 있음.
- **Tail sampling.** 요청 끝난 후 결정. error나 slow trace는 100% 저장, 정상은 1%. 더 똑똑한 sampling이지만 buffer 필요.

production에서는 보통 tail sampling을 쓴다. error·outlier 위주로 저장.

## p99 latency — "Averages Lie, Percentiles Tell the Truth"

Gil Tene의 유명한 강연 "How NOT to Measure Latency"가 분산 시스템 measurement의 표준을 만들었다. 핵심은 한 줄.

> p99 latency가 진짜 latency다. average는 거짓말한다.

상황을 가정해 보자. 1만 요청 중 9900개가 10ms, 100개가 10초가 걸렸다.

- average = `(9900 × 10 + 100 × 10000) / 10000` = 109ms. "괜찮은 듯."
- p99 = 10초. "끔찍."
- p50 = 10ms. "정상."

이 1%의 끔찍한 응답이 시스템의 진짜 모습이다. average는 그걸 가려 버린다. p99·p95·p999가 진짜 보여 주는 그림이다.

### Coordinated Omission 함정

또 한 가지 함정이 **coordinated omission**이다. load test에서 자주 만난다.

```
부하 테스트:
  10000 req/s 보내기로 설정
  → server가 느려져 응답이 1초 지연됨
  → load gen이 send rate를 자동으로 낮춤 (req/s 유지하려)
  → 측정된 latency는 actual latency를 underreport
```

진짜 latency를 측정하려면 "client가 보내려고 했던 시점부터 응답 받은 시점까지"를 봐야 한다. send 후 응답까지가 아니다. HdrHistogram, k6 같은 도구가 이걸 잘 처리한다.

## 배포 전략 — Deploy ≠ Release

전통적으로 deploy = release였다. 새 코드를 production에 올리면 즉시 모든 사용자에게 노출. 끔찍한 일이 자주 일어났다.

현대 배포는 deploy와 release를 분리한다.

**1. Blue-Green.** 같은 capacity의 두 환경(blue=current, green=new) 동시 운영. load balancer를 green으로 전환. 문제 시 즉시 blue로 rollback.

**2. Canary.** 1% → 10% → 50% → 100% 점진적 트래픽 이동. 각 단계에서 SLO 측정. 문제 시 즉시 rollback.

**3. Feature Flag.** 코드는 모두 배포, **runtime에 일부 사용자에게만 노출**. LaunchDarkly·Unleash·Flagsmith가 표준 도구. "코드 deploy는 매일, feature release는 별도 일정"의 모델.

이 세 도구가 결합되면 **progressive delivery**가 만들어진다. 토스의 결제 시스템이 1% 단위 progressive rollout을 쓰는 이유가 이거다. 새 기능을 1%에만 노출, SLO·error rate 측정, 문제없으면 5%, 10%로 확장. 19장 결제 챕터에서 깊게 다룬다.

> 💡 휴리스틱 8 — **Deploy ≠ Release.** 코드를 production에 올리는 것과 사용자가 그 기능을 보는 것은 다른 일이다. feature flag로 이 둘을 분리하면 deploy 빈도를 무한히 늘릴 수 있다. Etsy·Stripe·Toss는 하루에 수십 번 deploy한다.

## Chaos Engineering — 평소에 일부러 깨자

Netflix가 2011년 Chaos Monkey를 도입했다. production VM을 무작위로 종료한다. 끔찍한 발상 같지만, 통찰은 명확하다.

> 장애를 평소에 일부러 일으켜 본 사람만이 진짜 장애를 견딘다.

Netflix Simian Army가 그 진화 — Latency Monkey (지연 주입), Conformity Monkey (잘못된 설정 식별), Chaos Gorilla (AZ 통째 종료), Chaos Kong (region 통째 종료).

핵심 원칙 4가지가 *Principles of Chaos Engineering*에 정리되어 있다.

1. **Hypothesis 정의.** "AZ 한 곳이 죽어도 5xx 응답이 1%를 안 넘는다."
2. **Real-world event 시뮬레이션.** 실제 일어날 수 있는 장애(network partition, host failure, latency spike).
3. **Production 환경에서.** staging이 아닌. 진짜 환경에서만 진짜 견디는지 안다.
4. **Blast radius 최소화.** 점진적, 일부 사용자만, 즉시 rollback 가능.

한국에서는 토스가 game day 문화를 가장 적극적으로 도입했다. 한 달에 한 번 의도적 장애 주입을 통해 on-call 대응 능력을 검증한다.

## Blameless Postmortem — 학습 조직의 기반

장애가 발생했다고 해보자. 회고에서 두 가지 답이 가능하다.

- **Blameful:** "왜 김OO이 그 deploy를 했지? 누구 책임이지?"
- **Blameless:** "왜 우리 시스템·프로세스가 그 deploy의 위험을 사전에 차단하지 못했지?"

Google SRE Book이 정립한 표준이 **blameless postmortem**이다. 사람이 아닌 시스템·프로세스를 비판한다. 그렇지 않으면 사람들이 사고를 숨기고, 학습이 일어나지 않고, 같은 사고가 반복된다.

표준 postmortem 양식:

1. **Summary.** 한 단락으로 무슨 일이 일어났는지.
2. **Impact.** 사용자·매출에 미친 영향, 시간.
3. **Root Cause.** 5 Whys로 근본 원인 추적.
4. **Detection.** 어떻게 발견했는가? 더 빨리 발견할 수 있었나?
5. **Response.** 어떻게 대응했는가? 잘된 점·아쉬운 점.
6. **Lessons Learned.** 시스템·프로세스 측면에서 무엇을 배웠나.
7. **Action Items.** 누가 언제까지 무엇을 한다. 추적 가능한 ticket.

가장 중요한 건 **action item 추적의 정직함**이다. postmortem만 쓰고 action item이 잊혀지면 의미가 없다. 한국에서는 카카오와 우아한형제들이 postmortem 공유 문화를 일부 외부에 공개하며 정착시켰다.

## On-call 휴머니즘 — alert는 사람을 깨운다

이 챕터의 도입에서 던진 질문으로 돌아오자. on-call burnout은 alert 설계의 실패다. 그 실패를 막는 5가지 원칙을 정리하자.

**1. Actionable alerts only.** 사람이 깨어나서 할 일이 없으면 page 보내지 마라. 자동 해결되는 일은 알람이 아닌 ticket으로.

**2. Burn rate으로 noise 줄이기.** SLO 임계만 보면 false positive가 많다. burn rate alerting으로 fast/slow 가르기.

**3. Runbook 필수.** 모든 alert에 "이 alert이 울리면 무엇을 봐야 하는지" 문서. runbook 없는 alert는 깨우지 마라.

**4. Escalation 정책.** primary on-call이 5분 안에 응답 안 하면 secondary. 한 사람이 항상 책임지지 않게.

**5. Pager fatigue 측정.** 한 명의 on-call이 한 달에 page를 몇 번 받는지 추적. 임계 (예: 5회/주) 넘으면 alert 정책 재점검.

토스 SLASH 22 "토스의 on-call 문화" 발표가 한국 백엔드에 강한 인상을 남겼다. 그 핵심은 **alert의 절반을 자동화**한 것이다. "사람이 안 깨어나도 되는 일"을 정확히 가르고, 그 부분을 자동 복구·자동 ticket으로 전환. 결과적으로 page 빈도가 절반 이하로 줄었다.

> 💡 한 줄 — **사람을 깨우는 모든 page는 그만한 가치가 있어야 한다.** 가치 없는 page를 줄이는 것이 on-call 문화의 기본기다.

## 시스템 한계 표현 도구 — 5가지 정리

이 챕터의 핵심 통찰을 5가지 도구로 압축하자.

| 도구 | 무엇을 표현 | 누구가 보는가 |
|------|----------|---------------|
| Rate limiting | 외부 → 우리의 한계 | 외부 client |
| Backpressure | 내부 producer → consumer 한계 | 내부 system |
| SLO + Error Budget | 우리가 약속하는 신뢰성 | 운영자·사용자·product |
| Observability (logs·metrics·traces) | 우리 시스템의 현재 상태 | 운영자·디버거 |
| 배포 전략 + Chaos | 변경의 위험·복구의 능력 | 운영자·product |

이 5가지가 한 layer로 깔린 시스템은 자기 자신을 안다. 한 가지라도 빠지면 시스템은 자기 한계를 모르고, 한계를 모르는 시스템은 새벽 alert로 우리를 깨운다.

## Callback 예고

14장의 도구들은 후속 챕터에서 그대로 반복 등장한다.

- **3부 케이스 16~20장.** 각 시스템(채팅·피드·검색·결제·이커머스)마다 "이 시스템의 운영 — SLO·alert·rollback" sidebar로 변주.
- **19장 결제·금융.** 토스 결제의 progressive rollout·canary·feature flag·on-call이 이 챕터의 도구를 정확히 활용.
- **부록 A 현장 노트.** on-call 휴머니즘이 한 번 더 깊게.

## 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 시스템이 자기 자신을 보는 5가지 도구가 손에 잡혀 있다. Rate limiting 5 알고리즘, backpressure 패턴, SLI/SLO/Error Budget, three pillars + OpenTelemetry + wide-event observability + cardinality, p99 latency와 coordinated omission, blue-green/canary/feature flag, chaos engineering 4 원칙, blameless postmortem, on-call humanism 5원칙. 토스 on-call 자동화, 카카오·우아한형제들 postmortem 공유 문화까지가 한 묶음이다.

기억해두자. 분산 시스템을 만드는 것만큼 운영하는 일이 어렵다. 우리 시스템에 자기 한계를 표현하는 5가지 도구가 깔려 있고, 그 위에 blameless 문화가 있고, alert이 actionable하다면, 새벽 alert가 사람을 망가뜨리지 않는다. **사람을 깨우는 모든 page는 그만한 가치가 있어야 한다**는 원칙이 이 챕터의 한 줄 요약이다.

다음 장에서는 데이터 파이프라인과 협업 동기화를 살펴본다. Lambda·Kappa·Dataflow 아키텍처와 CRDT의 기초. 그 위에서 협업 도구(Figma·Linear)가 어떻게 multi-writer 일관성을 만드는지 함께 본다.

---

# 15장. 데이터 파이프라인과 협업 동기화 — Lambda·Kappa·Dataflow + CRDT 짧게

어느 광고 회사의 정산팀이 한 새벽에 비상 회의를 열었다고 해보자. 광고주가 "어제 우리가 본 클릭 수와 오늘 청구서의 클릭 수가 다릅니다"라고 항의해 왔다. 회사 내부의 batch 집계는 1시간 지연 후 정확한 숫자를 만드는데, 실시간 stream 집계는 그것보다 빠르게 다른 숫자를 보여 주고 있었다. 같은 데이터의 두 진실 — 한 쪽은 정확하지만 느리고, 한 쪽은 빠르지만 어긋난다.

이 풍경은 분산 시스템의 한 정직한 단면이다. **"이 데이터의 진실을 어디서 합칠 것인가"** 라는 질문은 옛 batch 시대부터 modern stream 시대까지 한 번도 사라지지 않았다. Lambda는 두 layer를 모두 두고 합쳤다. Kappa는 한 layer로 통일했다. Dataflow는 두 모드를 한 추상화로 묶었다. 이번 장에서는 그 진화의 한 줄을 짚어 보자. 그리고 마지막에 sidebar로 "여러 source의 진실"이 아닌 "여러 writer의 진실" — Figma·Linear 같은 협업 도구의 동기화 — 도 함께 들여다본다.

## 1. Lambda Architecture — batch + stream의 첫 번째 답

2011년, Nathan Marz가 *Big Data*라는 책에서 정리한 **Lambda Architecture**가 한 시대의 default가 됐다. 핵심 아이디어는 세 layer를 명시적으로 가르는 것이다.

```
incoming data
    │
    ├─→ Batch Layer (Hadoop MapReduce, Spark)
    │     - 모든 데이터를 처음부터 재처리
    │     - 정확하지만 1시간~1일 지연
    │     - precomputed view 생성
    │
    └─→ Speed Layer (Storm, Spark Streaming)
          - 최근 데이터만 처리
          - 빠르지만 정확도 trade-off
          - real-time view 생성

Serving Layer:
    Batch view + Speed view → 사용자 응답
```

이 모양의 가치는 분명하다. **batch는 정확성, speed는 저지연**. 둘을 한 자리에서 합쳐 "1시간 전까지는 정확, 그 이후는 빠른 근사"라는 응답을 만들어 낸다. 광고 클릭 집계·실시간 추천·금융 reconciliation 같이 두 시간축이 모두 필요한 도메인에 잘 어울렸다.

그런데 단점이 점점 커졌다. **같은 비즈니스 로직을 두 layer에 두 번 짠다.** 광고 클릭 집계 로직이 MapReduce 코드 + Storm 코드로 두 번 존재한다. 둘이 미세하게 어긋나면 도입부의 광고 환불 사고가 일어난다. 그리고 두 codebase를 평행하게 유지하는 운영 부담이 절대 만만치 않다. Lambda는 우아하지만 — 그 우아함이 일상의 부담으로 바뀌었다.

이 코드 중복을 한 번 겪고 나면 누구나 "다른 모양은 없을까"를 묻기 시작한다. 그 답이 2014년에 나왔다.

## 2. Kappa Architecture — stream 단일, replay로 재처리

2014년 Jay Kreps (당시 LinkedIn, 지금 Confluent CEO)가 *Questioning the Lambda Architecture*라는 글에서 정면으로 던졌다. **"Lambda의 batch layer를 없애자. stream 하나로 통일하자. 재처리가 필요하면 Kafka에서 replay하자."**

이게 **Kappa Architecture**다. 단순한 아이디어 같지만 깊은 결과를 만든다.

```
incoming data → Kafka (long retention)
                  ↓
              Stream processor (Flink, Kafka Streams)
                  ↓
              Materialized view (DB, Elasticsearch)

재처리 시: 새 processor 띄우고 offset 0부터 replay
```

이 모양이 우아한 이유는 두 가지다.

**1. 코드 하나.** 비즈니스 로직이 stream processor 안에 한 번만 있다. batch와 stream의 어긋남이 원천적으로 없다.

**2. 재처리가 자연스럽다.** 새 schema, 새 비즈니스 로직, 버그 수정 — 모두 replay로 처리된다. Kafka가 단순한 큐가 아니라 **immutable log of truth**가 되는 셈이다.

대신 Kappa의 가정이 분명하다. **모든 데이터가 Kafka에 충분히 retention된다.** 1년치 데이터 재처리가 필요하면 Kafka에 1년치 데이터가 있어야 한다. storage 비용 + 운영 부담이 만만치 않다. 그래서 hot data는 Kafka, cold data는 별도 storage(S3·HDFS)로 가는 hybrid 모델도 흔하다 — Confluent의 tiered storage가 그 답 중 하나다.

또 하나 — **stream processor의 정확성**이 핵심 변수가 된다. 이 점은 exactly-once 절에서 더 짚자.

## 3. Dataflow — 4축으로 batch와 stream을 통합하기

2015년 Google의 Tyler Akidau와 동료들이 발표한 *The Dataflow Model* (P20)이 이 분야의 추상화를 한 단계 더 끌어올렸다. 핵심 통찰은 직설적이다.

> batch와 stream은 다른 일이 아니다. 같은 4축의 다른 설정값이다.

4축은 다음과 같다.

**1. Event-time.** 이벤트가 실제로 일어난 시각. processing-time(시스템이 처리한 시각)과 분명히 구분한다. 8장에서 짚은 분산 시간 다루기가 여기에서도 그대로 적용된다.

**2. Watermark.** "시간 t 이전의 모든 데이터가 도착했다"고 시스템이 추정하는 시점. 늦게 도착하는 데이터(late arrival)를 어떻게 다룰지 결정하는 신호다.

**3. Trigger.** 결과를 언제 emit할지 결정한다. event-time watermark 도달 시, processing-time 주기, 데이터 수 기준 등 다양하게 설정할 수 있다.

**4. Accumulation.** 같은 window에 대해 결과를 누적할지(accumulating), 매번 새로 시작할지(discarding), 또는 둘 다 보낼지(accumulating + retracting)를 정한다.

이 4축을 적절히 설정하면 batch도 stream도 같은 코드로 처리된다. batch는 "모든 데이터가 도착한 후에 한 번 emit", stream은 "watermark마다 emit"의 차이일 뿐이다. **Apache Beam**이 이 추상화를 구현했고, Flink가 Beam 호환 runner를 제공하면서 사실상 산업 표준이 됐다.

```python
# Beam — batch와 stream 모두 같은 코드
import apache_beam as beam

(pipeline
 | 'Read' >> beam.io.ReadFromKafka(...)  # 또는 ReadFromGCS for batch
 | 'Window' >> beam.WindowInto(FixedWindows(60))  # 1분 window
 | 'Count' >> beam.combiners.Count.PerKey()
 | 'Write' >> beam.io.WriteToBigQuery(...))
```

이 코드는 Kafka에서 stream으로 읽으면 stream 처리, GCS에서 batch로 읽으면 batch 처리. 같은 비즈니스 로직이 두 모드를 모두 책임진다. **batch = bounded stream**이라는 한 줄이 modern 데이터 파이프라인의 mental model이다.

## 4. 도구의 풍경 — MapReduce에서 Flink까지

이 진화를 도구 시점으로 한 표에 정리해 보자.

| 도구 | 시기 | 모델 | 핵심 특징 |
|------|------|------|-----------|
| MapReduce (P16) | 2004 | Batch | Hadoop ecosystem. disk I/O 무거움. |
| Spark RDD (P17) | 2010 | Batch + Micro-batch | 메모리 기반, lineage replay. iterative ML 강점. |
| Storm | 2011 | Stream | 초기 stream 처리, low-level API. |
| Spark Streaming | 2013 | Micro-batch (1초 단위) | Spark ecosystem 활용. true stream은 아님. |
| Flink (P18) | 2015 | True stream + bounded batch | event-time, watermark, exactly-once. 현재 mainstream. |
| Kafka Streams | 2016 | Stream (library) | Kafka native, JVM에 임베디드, 운영 가볍다. |
| Beam (P20) | 2016 | 추상화 layer | Flink·Dataflow·Spark runner 위에서 같은 코드. |

2026년 기준 현실적 선택은 도메인마다 다르다.

- **단순 ETL batch**: Spark.
- **Real-time stream + complex logic**: Flink.
- **Kafka native·가볍게 시작**: Kafka Streams (library 형태, JVM application에 임베드).
- **Multi-runner·portable**: Beam.
- **Cloud managed**: GCP Dataflow (Beam runner), AWS Kinesis Analytics for Apache Flink.

표 한 장으로 정리하면 깔끔해 보이지만, 정작 production에서는 **어느 도구를 쓰느냐보다 그 도구를 정확히 운영하는 능력**이 더 큰 변수다. 그 운영의 핵심이 exactly-once와 watermark다.

## 5. Exactly-once의 진짜 의미 — checkpoint와 watermark

stream 처리에서 가장 자주 헷갈리는 단어가 **exactly-once**다. Flink는 "exactly-once"를 약속하는데, 그 약속의 정확한 의미가 뭘까?

**Flink의 exactly-once는 "state에 대한 보장"이다.** 메시지가 1번만 받아져 1번만 처리된다는 뜻이 아니다. 메시지는 여러 번 받을 수 있지만, **state 갱신은 정확히 한 번**만 적용된다는 보장이다.

이 보장을 가능하게 하는 메커니즘이 **checkpoint**다. Flink는 일정 주기(예: 10초)마다 전체 stream graph의 state를 distributed snapshot으로 저장한다. 장애가 나면 마지막 checkpoint로 복귀해 거기서부터 다시 처리. Kafka offset도 함께 저장되니, replay가 일관되게 일어난다.

```
T=0   메시지 1 처리, state 갱신
T=10  Checkpoint 1 저장 (state + Kafka offset)
T=15  메시지 2 처리, state 갱신
T=20  장애 발생!
T=21  Checkpoint 1로 복구, T=10 시점의 offset부터 다시 처리
      → 메시지 2를 또 받지만, state는 정확히 1번만 갱신된 효과
```

이 모양이 가능한 이유는 **state 자체가 checkpoint에 포함**되기 때문이다. application state가 외부에 있고 그 외부 storage가 transactional하다면(예: Postgres) 같은 모델이 가능하다. **Kafka transactional producer + idempotent consumer + transactional sink**가 한 묶음일 때 비로소 진짜 end-to-end exactly-once다. 한 layer만 빠져도 깨진다 — 그래서 운영 단순함이 가장 큰 비결이다.

### Watermark의 함정 — late arrival을 어떻게 다룰까

**Watermark**는 또 다른 함정이다. "이 시간 t 이전 모든 데이터가 도착했다"고 추정하는 신호인데, 실제로는 늦게 도착하는 데이터(**late arrival**)가 있을 수 있다. 어떻게 다룰까?

- **Drop late data.** 단순. 일부 데이터 손실을 감수한다.
- **Allowed lateness.** watermark 후에도 일정 시간(예: 1시간) window를 유지한다. 그 안에 들어오면 window 결과를 재계산한다.
- **Side output.** late data를 별도 stream으로 출력한다. 사후 처리 책임이 application에 남는다.

이 결정은 도메인이 정한다. real-time analytics는 drop 가능, financial reconciliation은 절대 drop 불가. **"exactly-once + 0 loss"는 매우 좁은 가정의 보장**임을 마음에 새겨 두는 편이 낫다. 도구가 약속하는 단어를 그대로 믿지 말고, 우리 도메인에서 정확히 무엇이 보장되는지 한 번 더 확인하자 — 그게 새벽 alert이 줄어드는 길이다.

## 6. 한국 사례 — 카카오 광고 stream과 쿠팡 검색 indexing

한국 백엔드에서 자주 인용되는 두 사례를 짚어 두자.

**카카오 광고 추천 Kafka 기반 stream 파이프라인.** 카카오 광고팀이 if(kakao) 2021·2022 발표에서 정리한 모델이다 (W33). 광고 클릭·노출 이벤트가 Kafka로 들어오고, Flink stream processor가 실시간으로 사용자 모델·광고주 모델을 갱신한다. ML model training과 serving이 분리돼 — training pipeline은 batch (Spark), serving은 stream (Flink). batch + stream 두 layer가 같은 Kafka topic을 공유하는 모양으로, 본질적으로는 Kappa에 가깝다.

여기서 흥미로운 점은 — **"clicks가 진짜 사용자에게 보여줬을 때만 카운트한다"**는 정합성 조건을 위해 stream pipeline 안에서 "노출 이벤트 도착 후에야 클릭 이벤트가 활성화되는" join 로직이 들어 있다는 것이다. event-time과 watermark 설정이 production에서 자주 데이는 자리라는 점을 카카오 발표가 정직하게 짚는다 (검증 필요 — 발표 원문 확인 권장).

**쿠팡 검색 indexing pipeline.** 5장 검색 챕터에서 이미 짚었지만 데이터 파이프라인 관점에서 다시 보자 (W32). 상품 변경 이벤트가 Kafka로 발행되고 Flink가 실시간 indexing pipeline을 실행해 Elasticsearch에 색인한다. 핵심 가치는 **decoupling + replay**다. 검색 schema를 바꾸면 새 processor를 띄워 처음부터 replay하면 된다. 운영 단순성과 확장성을 둘 다 잡은 패턴이다.

이 두 사례가 보여 주는 한 가지 — **한국 백엔드의 데이터 파이프라인은 거의 Kappa로 정착 중이다.** Hadoop·MapReduce 기반 Lambda는 legacy로 남아 있고, 새 시스템은 Flink + Kafka 기반이다. Beam·Dataflow는 GCP 친화 팀에 한해 채택하는 정도다.

## 7. 의사결정 — 5가지 차원

새 데이터 파이프라인을 설계할 때 자기에게 던질 다섯 질문이다.

1. **Latency target?** real-time (ms~초) → Flink·Kafka Streams. near-real-time (분~시간) → Spark Streaming. batch (시간~일) → Spark.
2. **정확도 vs 속도?** financial → exactly-once 필수. analytics → at-least-once 또는 best-effort 가능.
3. **재처리 빈도?** 자주 → Kappa (Kafka replay). 드물게 → Lambda 또는 Kappa 둘 다 가능.
4. **운영 인력?** 작음 → managed (GCP Dataflow, AWS Kinesis Analytics, Confluent Cloud). 큼 → self-hosted Flink.
5. **비용?** Kafka long retention은 비싸다. cold data는 S3 archive로 옮기는 hybrid 검토.

이 다섯에 답이 명확하면 도구 선택은 자연스럽게 따라온다. 정답을 도메인 언어로 답할 수 있어야 그 결정이 운영의 새벽 alert에서도 무너지지 않는다.

## 8. CRDT — 협업 도구의 수학적 기반 (Sidebar 4p)

여기서 잠시 시야를 협업 동기화로 옮겨 보자. Figma·Linear·Notion 같은 협업 도구의 multi-writer 동기화는 분산 시스템의 또 다른 흥미로운 자식이다.

상황을 가정해 보자. Figma 디자인 파일에서 두 사용자 A와 B가 동시에 같은 사각형의 색을 바꾼다. A는 빨강, B는 파랑. 네트워크 latency 때문에 두 변경이 거의 동시에 발생한다. 어떤 색이 최종 결과여야 할까? 이게 단순한 last-write-wins 문제 같지만, offline 편집·peer-to-peer 동기화·중앙 server 없이 작동하는 시스템에서는 답이 훨씬 까다로워진다.

이 문제를 푸는 자료구조가 **CRDT** (Conflict-free Replicated Data Type)다. Marc Shapiro와 동료들이 2011년 정리한 *Conflict-free Replicated Data Types* (P11) 논문이 표준이다.

### CRDT의 핵심 약속

> 모든 replica가 같은 update들을 어떤 순서로 받든, 결국 같은 state로 수렴한다 (strong eventual consistency).

이게 가능한 이유는 update가 **commutative**(교환 가능)이고 **idempotent**(중복 적용 가능)하기 때문이다. A의 update를 먼저 적용하든 B의 update를 먼저 적용하든 결과가 같다. 같은 update를 두 번 적용해도 한 번 적용한 것과 같다. 12장에서 본 **CALM theorem** — "coordination-free = monotonic" — 이 정확히 이 결과의 이론적 토대다.

### State-based vs Op-based

CRDT에는 두 모양이 있다.

**State-based (CvRDT).** replica들이 서로 state를 통째로 보내 merge한다. merge 함수가 semilattice의 join 연산 (commutative·associative·idempotent)이라는 수학적 보장이 핵심이다. 운영이 단순하지만 state가 클수록 네트워크 비용이 커진다.

**Op-based (CmRDT).** replica들이 operation 자체를 broadcast하고, 다른 replica들이 같은 op을 적용한다. op들이 commutative하다는 보장이 필요하다. 네트워크는 가볍지만, op delivery 보장(at-least-once + idempotent)이 까다롭다.

### 자주 쓰이는 CRDT 자료구조

- **G-Counter:** grow-only counter. 증가만 가능 — 좋아요 수 카운터 같은 자리.
- **PN-Counter:** positive-negative counter. 증감 모두 가능 — 좋아요 토글 가능한 자리.
- **OR-Set (Observed-Remove Set):** set에서 add/remove. add가 remove를 이긴다. Notion 댓글 같이 "한 번이라도 등장한 댓글은 가능한 한 살린다" 정책.
- **LWW-Element-Set:** Last-Write-Wins set. timestamp 기반. 단순하지만 시계 어긋남에 약하다 (8장 NTP step 참고).
- **RGA (Replicated Growable Array):** 텍스트 편집에 사용. Y.js·Automerge가 이걸 구현.

### 누가 CRDT를 쓰는가

- **Riak**: CRDT를 native data type으로 제공.
- **Redis Enterprise**: Active-Active CRDT module.
- **Y.js·Automerge**: JavaScript CRDT 라이브러리. 협업 도구에서 가장 많이 쓰인다.
- **Figma·Linear·Notion 일부**: 자체 CRDT-like 모델로 multi-writer 합치기.

### OT — Operational Transform과의 비교

CRDT의 경쟁자가 **OT (Operational Transform)**다. Google Docs가 2009년부터 쓰는 모델로, 중앙 server가 각 client의 operation을 받아 다른 client의 op과 transform해서 일관성을 유지한다.

```
client A: insert "X" at position 5
client B: insert "Y" at position 3 (이미 적용된 op)
server: A의 op을 transform → "X" at position 6 (B의 insert 반영)
```

OT는 **중앙 server**가 필요하다 (authoritative ordering). CRDT는 server 없이도 peer-to-peer로 가능하다 — 이게 **local-first software** (자료 28)의 핵심이다. offline 편집 후 나중에 sync하는 식의 워크플로우가 CRDT 위에서 자연스럽게 작동한다.

### "이 데이터는 CRDT가 어울리는가, OT면 충분한가" — 4가지 질문

도메인을 보고 둘 중 하나를 결정해야 할 때 던질 네 질문이다.

1. **Offline 편집이 필요한가?** Yes → CRDT. server 없이 local로 작업한 뒤 나중에 sync 가능.
2. **중앙 server가 가능한가?** Yes → OT. authoritative ordering으로 구현이 단순.
3. **데이터 타입이 자연스럽게 commutative한가?** counter·set은 쉽다. text·rich document는 어려워서 RGA·Yjs 같은 특수 자료구조가 필요.
4. **conflict resolution을 사용자가 봐도 되는가?** No → CRDT가 자동 merge. Yes → 단순 last-write-wins나 사용자 prompt도 가능.

Figma는 CRDT-like (offline 가능), Google Docs는 OT (server authoritative), Linear는 hybrid다. 도구마다 결정이 다르고, 그 결정이 사용자 경험을 본질적으로 가른다.

## 9. 분산 파이프라인과 CRDT — 같은 주제의 두 단면

이 챕터의 한 줄 통찰을 정리해 보자. **분산 시스템은 결국 "여러 진실을 하나로 합치는" 문제다.**

- **분산 파이프라인**은 여러 source(events·batch records)의 진실을 하나의 view로 합친다. Lambda/Kappa/Dataflow가 그 모양.
- **CRDT/OT**는 여러 writer의 진실을 하나의 state로 합친다. Figma/Google Docs가 그 모양.

둘은 다른 영역처럼 보이지만 본질은 같다. **시간(event-time vs processing-time), 순서(causal happens-before), 충돌(merge function vs OT transform)** 같은 개념이 양쪽에서 반복된다. 8장에서 다룬 Lamport happens-before가 양쪽의 토대이고, 12장의 CALM theorem이 CRDT의 이론적 근거였다 — 이 챕터는 그 이론들이 production에서 어떻게 작동하는지를 두 측면에서 보여 준다.

기억해 두자. **합치는 방식이 도메인을 정의한다.** real-time analytics는 Kappa, financial reconciliation은 정확한 Lambda, multi-writer 협업은 CRDT 또는 OT. 자기 도메인의 본질을 정확히 보고 도구를 고르는 편이 낫다.

## 10. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 데이터 파이프라인의 세 갈래와 협업 동기화의 두 모양이 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **Lambda Architecture** — batch + speed 두 layer. 정확성·저지연 둘 다 잡지만 코드 중복이 비싸다. financial reconciliation 같은 자리에 여전히 유효.
- **Kappa Architecture** — stream 단일 + Kafka replay. 코드 하나 + 재처리 자연스러움. 한국 백엔드의 default. Kafka long retention 비용을 받아들이는 게 조건.
- **Dataflow 4축** — event-time·watermark·trigger·accumulation. batch = bounded stream의 mental model. Apache Beam이 그 추상화.
- **현재 mainstream은 Flink + Kafka.** Beam·Dataflow는 GCP 친화 팀. Spark는 batch ETL에 여전.
- **Exactly-once는 state 보장**이지 메시지 보장이 아니다. checkpoint + transactional sink가 한 묶음일 때만 진짜 end-to-end exactly-once.
- **Watermark + late arrival**은 도메인이 정하는 결정. 단순 drop·allowed lateness·side output 세 갈래. 도구가 약속하는 단어를 그대로 믿지 말자.
- **CRDT는 coordination-free 동기화의 수학적 기반**이다. monotonic 자료구조 + commutative op = 충돌 없이 수렴.
- **OT vs CRDT** — server authoritative면 OT, peer-to-peer·offline-first면 CRDT. 네 질문으로 갈라진다.
- **한 줄 통찰** — 분산 시스템은 결국 진실을 합치는 문제다. 그게 새벽 3시의 자신을 살린다.

여기까지가 2부의 마지막 챕터다. 빌딩 블록(1부)과 분산 시스템 패턴(2부)을 모두 갖춘 우리가, 다음 부에서는 **케이스 스터디**로 넘어간다. 채팅(16장) → 피드(17장) → 검색·매칭(18장) → 결제(19장 클라이맥스) → 이커머스(20장). 우리가 익힌 도구들이 실제 시스템에서 어떤 조합으로 등장하는지, 같이 들여다보자.


---

# 3부. 케이스 스터디 — 실제 시스템들

> 채팅·피드·검색매칭·결제·이커머스 — 5개 도메인의 대표 시스템을 1부·2부에서 익힌 도구로 해부한다.
>
> 클라이맥스는 19장 결제다. 1부 9개 부품·2부 6개 패턴이 한 시스템에 한꺼번에 모이는 자리. 임의의 시스템을 봤을 때 "이건 1부 ○장, 2부 △장과 비슷하군"이라는 자동 mapping이 손에 잡힌다.

---

# 16장. 채팅 시스템 — Discord·LINE·당근·Slack

Discord 엔지니어가 어느 날 사내 블로그에 한 줄을 올렸다. "We had a single message that was getting requested 30,000 times per second. Our database was suffering." 메시지 하나가 시스템 전체를 위협한다. 인기 채널의 누군가가 농담 한 줄을 던졌고, 그 한 줄을 모두가 동시에 본다. 같은 row가 초당 3만 번 read되는 그림 — 단순한 KV조회처럼 들리지만, partition 하나가 그 부하를 받기 시작하면 cluster 전체가 휘청거린다.

채팅 시스템은 듣기에 평범하다. 메시지 보내고, 받고, 저장하고, 보여준다. 그런데 운영해 보면 가장 잔인한 시스템 중 하나다. **메시지 1조 건이 쌓이는 시스템은 무엇을 양보했고, 무엇을 지켜냈는가** — 이 질문에 답할 수 있어야 채팅 시스템을 안다고 말할 수 있다.

3부 케이스 스터디의 첫 챕터로 채팅을 고른 이유가 있다. 채팅은 1·2부에서 배운 부품과 패턴이 거의 모두 한 시스템 안에 등장한다. 2장 NoSQL의 hot partition, 3장 캐시의 stampede, 4장 큐의 fan-out, 9장 보안의 token 인증, 13장 sharding, 14장 관측성·on-call — 모두 채팅의 어느 자리에서 다시 만난다. 1·2부의 학습이 한 도메인에서 어떻게 동시에 쓰이는지를 보는 첫 자리다.

## 도메인이 요구하는 5가지 — ordering·durability·history·real-time·fan-out

채팅 시스템 설계는 도메인 요구 5가지의 정의에서 시작한다. 한 줄로 줄이면 다음과 같다.

- **Ordering**: 같은 채팅방 안에서 메시지 순서는 결코 뒤바뀌면 안 된다. 8장에서 본 시간·순서 문제가 채팅 도메인의 1번 줄이다.
- **Durability**: "보낸 메시지가 사라졌다"는 채팅 시스템의 가장 큰 죄다. 한 번 ack한 메시지는 잃지 않는다.
- **History**: 사용자는 1년 전 메시지도 검색해서 본다. cold data가 hot data의 100배 이상이다.
- **Real-time delivery**: 메시지 보낸 사람이 손가락을 떼는 순간 받는 사람 화면에 떠야 한다. p50 100ms 이내가 사용자 체감 기준선.
- **Fan-out**: group chat에서 메시지 하나가 1000명에게 동시에 가야 한다. 1조 건 stored = N조 건 delivered.

이 5가지가 서로 충돌한다. Ordering을 지키려면 single-leader가 편하지만, fan-out과 real-time을 위해서는 horizontal scale이 필요하다. Durability를 위해서는 WAL을 강제해야 하지만, real-time을 위해서는 sync write가 부담된다. 그래서 채팅 시스템 설계는 **5축의 trade-off 어디에 점을 찍을지**의 문제다.

Discord·LINE·당근·Slack은 각자 다른 자리에 점을 찍었다. 이제 네 시스템이 어디에 무엇을 양보했는지를 차례로 살펴보자.

## WebSocket connection — 듣기에 단순하지만 운영하면 잔인하다

채팅의 첫 번째 기술 결정은 어떤 transport로 메시지를 보내는가다. HTTP polling? Long polling? Server-Sent Events? 정답은 명확하다. **WebSocket이다.** 양방향 + 낮은 latency + 1억 단위 동시 connection을 운영 가능하다.

그런데 WebSocket이 운영하기 시작하면 채팅 시스템의 가장 골치 아픈 자리가 된다. 상황을 가정해보자. 사용자 1억 명이 동시 접속해 있다. server pod 하나가 떨어진다. 그 pod이 들고 있던 1만 connection이 한꺼번에 다른 pod으로 reconnect 시도를 한다. reconnect storm이 시작되면 다른 pod도 OOM kill되기 시작한다. 끔찍한 일이다.

LINE이 이 자리를 어떻게 풀었는지가 인상적이다. LINE Engineering blog의 messaging hub 시리즈가 정리해준다(W30).

> connection-manager (WebSocket) ↔ message-router (gRPC) ↔ Kafka 큐 (LINE Engineering, 2022)

WebSocket connection을 받는 pod(connection-manager)과 비즈니스 로직을 처리하는 pod(message-router)을 분리했다. connection-manager는 connection의 상태와 user identity만 관리한다. 메시지가 들어오면 gRPC로 message-router에 던지고, Kafka로 흘려보낸다. **WebSocket의 stateful 책임과 메시지 처리의 stateless 책임을 분리한 것**이다.

이렇게 분리하면 무엇이 좋은가? message-router를 무중단으로 배포할 수 있다. WebSocket connection은 connection-manager가 들고 있고, message-router는 stateless라 rolling deploy가 자유롭다. 한쪽이 죽어도 다른 쪽은 살아있다. resilience 패턴이 두 layer로 분리된 셈이다.

물론 한 가지 함정이 있다. LINE이 발표에서 정직하게 풀어놓은 실패담이다.

> Apache HTTP client 라이브러리 버전 업그레이드 한 번으로 throughput이 1/3로 떨어진 적이 있다. (LINE Engineering, W30)

라이브러리 한 줄 업그레이드가 메신저의 처리량을 1/3로 만든다. 다른 시스템 같으면 한 번에 못 발견할 수도 있었을 것이다. 채팅처럼 latency·throughput에 민감한 도메인이라 빠르게 잡혔다. 잊지 말자. WebSocket 시스템은 의존성 한 줄도 검증 없이 올리면 안 된다. 14장의 관측성 패턴 — p99 latency·throughput·error rate — 가 매일 신뢰의 1차 신호다.

## Discord 마이그레이션 — Cassandra에서 ScyllaDB로 가는 9일

채팅 시스템 케이스 스터디에서 가장 인기 있는 deep dive가 Discord의 Cassandra → ScyllaDB 마이그레이션이다. 숫자가 인상적이다(W21, 자료 4.1).

| 항목 | Cassandra (before) | ScyllaDB (after) |
|------|---------------------|--------------------|
| 노드 수 | 177 | 72 |
| p99 read latency | 40~125ms | 15ms |
| p99 write latency | 5~70ms | 5ms |
| 운영자 부담 | GC pause로 새벽 page 잦음 | GC 없음, page 격감 |

왜 노드가 절반 이하로 줄었는데 latency가 더 좋아졌는가? 두 가지 이유다.

**첫 번째, JVM GC를 떼어냈다.** Cassandra는 JVM 기반이라 GC pause를 피할 수 없다. p99에서 100ms 안팎의 stop-the-world가 정기적으로 찍힌다. ScyllaDB는 C++로 작성됐고 shared-nothing per-core 모델이라 GC가 없다. p99이 깨끗하게 떨어진다.

**두 번째, 더 중요한 결정 — Rust로 작성한 data services layer를 추가했다.** 이 layer가 application과 ScyllaDB 사이에 끼어서 한 가지 일을 한다. **Request coalescing.** Discord 글이 직접 인용한다.

> Request coalescing is an important responsibility to avoid multiple database calls when many users request the same message. (Discord Engineering, W21)

상황을 다시 떠올려보자. 인기 채널의 한 메시지가 초당 3만 번 read된다. 만약 모든 read가 ScyllaDB까지 내려간다면 그 partition은 즉시 hot이 된다. data services가 그 앞에 서서 **같은 메시지에 대한 1000개의 동시 request를 1개의 DB call로 묶어서** 보낸다. 응답이 오면 그 1000개에 fan-out한다. 같은 결과를 가져오는 일을 1000배 줄인 것이다.

이게 3장 캐시 챕터에서 본 stampede 패턴의 채팅 도메인 변주다. 일반적인 캐시는 TTL 만료 시 stampede를 막기 위해 singleflight를 쓰는데, 채팅의 hot 메시지는 그것이 read 자체의 정상 상태다. **싱글 키 stampede가 일상이라서 coalescing이 application 옆에 layer로 박혀야 했다.** 같은 원리, 다른 모양이다.

그리고 마이그레이션 자체가 인상적이다. 처음 추정치는 "3개월". 실제로 걸린 시간은 **9일**. 무엇이 달랐는가? 마이그레이션 도구를 Rust로 다시 짰다. Cassandra에서 ScyllaDB로 row를 옮기는 streaming engine을, throughput을 한계까지 끌어올린 도구로 자체 제작한 것이다. 마이그레이션이 본업이 아닌 회사가 마이그레이션 도구를 처음부터 짜기로 결정한 것은 이례적이지만, 결과적으로 그 결정이 비용을 90% 줄였다.

이 사례에 한 가지 교훈이 있다. tribal #10에 들어 있는 휴리스틱이다. "DB는 마지막에 바꿔라 — 가장 비싼 마이그레이션." Discord는 그걸 알면서도 결정을 내렸다. 그리고 마이그레이션 도구라는 본업 외 자원에 투자해 비용을 줄였다. **마이그레이션 도구가 마이그레이션의 비용을 결정한다**는 사실은 기억해두자.

## 당근 채팅 — DynamoDB를 고른 한국 hyperlocal

한국 사례로 넘어와 보자. 당근마켓이 채팅을 따로 분리하면서 내린 결정은 책 전체에서 가장 흥미로운 한국 케이스 중 하나다(W31, 자료 4.11).

당근 채팅팀이 정리한 결정 사항을 한 줄로 줄이면 이렇다.

> 채팅을 별도 MSA로 분리 + 회사 첫 Go 도입 + DynamoDB를 storage로 선택. Cassandra 운영 부담을 회피하기 위함. (당근 blog, W31)

Cassandra가 아닌 DynamoDB를 고른 이유가 명시적으로 적혀 있다. **운영 부담 회피.** Discord 같은 회사는 Cassandra를 깊이 운영할 인력이 있지만, 당근은 채팅이라는 한 도메인에 그만한 운영 자원을 쓸 수 없다. 그래서 AWS managed service로 그 부담을 outsource한 것이다. 정직한 trade-off다.

물론 trade-off의 다른 쪽도 있다. DynamoDB는 vendor lock-in이 강하고, write 비용이 read 비용의 5배 이상이다. group chat의 fan-out이 많은 도메인에서는 비용이 빠르게 늘 수 있다. 그래서 당근은 도메인을 정확히 잘랐다. **거래 위치 기반의 1대1 채팅, 거래 완료 후 chat archive라는 라이프사이클** — 카카오톡 같은 영구 group chat과는 다른 게임이다(한국 7).

푸시 알림은 또 다른 결정이다. Node.js로 짠 push service가 초당 1500 RPS를 처리한다. 1500이 큰 숫자는 아니지만, 한국 hyperlocal의 트래픽 패턴(동네 단위 부분 spike)에 맞춘 capacity 결정이다. 글로벌 시스템처럼 10만 RPS를 미리 박지 않는다.

이게 도메인을 정확히 자른 시스템 디자인의 한 사례다. "쿠팡처럼 만들어야 한다"는 강박이 없다. 자기 도메인이 무엇이고, 어떤 라이프사이클을 가지고 있고, 운영자가 몇 명이고, 트래픽 패턴이 어떤지를 정확히 셈한 결과의 그림이다. 다른 회사 운영 시스템을 그대로 베끼면 안 된다는 점을 한국 사례가 거꾸로 증명한다.

## Slack — workspace sharding의 단단함

Slack은 또 다른 길을 갔다. 10B+ messages를 처리하는 시스템인데, 핵심 결정 하나가 모든 것을 단단하게 만든다(W22, 자료 4.2).

> Workspace-based sharding. shop_id처럼 workspace_id 기준으로 MySQL을 샤딩한다. PHP WebApp(저장) + Java RTM(real-time messaging). Elasticsearch가 search, 자체 KalDB가 logging. (Slack Engineering)

Slack의 채팅은 회사 단위(workspace) 안에서만 일어난다. 같은 workspace 안의 사용자만 같은 채널을 공유한다. 즉 **cross-workspace 쿼리가 사실상 없다**. 이게 sharding key를 결정할 때의 황금 같은 조건이다. 13장에서 본 hot partition의 함정이 거의 발생하지 않는다 — workspace는 자연스럽게 적당히 균등하게 분포한다.

Slack은 KalDB라는 자체 로그 스토리지까지 만들었다. 왜? Elasticsearch가 logging에 안 맞아서다. 5장에서 본 ES의 한계 — JVM heap 32GB cap, refresh interval 1초로 인한 write 부하 — 가 trillions of log를 다루기 시작하면 한계가 명확해진다. 회사가 자체 로그 store를 만든다는 결정은 엄청난 비용이지만, Slack 같은 규모에서는 운영비 절감이 그 비용을 회수한다.

여기서 한 가지 흥미로운 비교를 해보자.

| 항목 | Discord | LINE | 당근 | Slack |
|------|---------|-------|------|-------|
| **scale** | trillions of messages | 새해 0시 정상 평균 수십 배 | 한국 hyperlocal | 10B+ messages |
| **transport** | WebSocket | WebSocket (connection-manager 분리) | WebSocket | WebSocket (Java RTM) |
| **storage** | Cassandra → ScyllaDB | Akka actor + Redis Cluster (LIVE) | DynamoDB | MySQL workspace sharding |
| **sharding key** | channel_id | user_id | room_id (거래) | workspace_id |
| **fan-out 전략** | data services coalescing | message-router → Kafka | DynamoDB stream + Node.js | RTM Java service |
| **운영 철학** | 직접 다 만든다 | platform화 후 분리 | managed service 활용 | 자체 도구 투자 |
| **trade-off 회피** | JVM GC, hot partition | reconnect storm | Cassandra 운영 부담 | ES logging 한계 |

표를 한 줄로 줄이면 이렇다. **네 시스템은 모두 자기 도메인의 가장 큰 적을 명확히 정의했고, 그 적을 피하기 위해 비싼 결정을 했다.** Discord는 GC와 hot partition을, LINE은 reconnect storm을, 당근은 운영 부담을, Slack은 ES limit을 적으로 정의했다. 채팅 시스템 설계의 본질은 **자기 도메인의 1번 적을 정직하게 정의하는 일**이다.

## Sidebar: 카카오톡 새해·설날 트래픽 — fan-out 비용의 한국 버전

한국 메신저의 트래픽 패턴을 한 페이지 따로 보고 가자. 카카오 if(kakao) 발표가 정리한 카카오톡의 비정상 트래픽 시기다(한국 4).

- **새해 0시**: 평상시 대비 메시지 트래픽 5~30배 spike (시기마다 다름).
- **설날 아침**: 부모님께 보내는 메시지의 fan-out이 가장 거대한 도메인 spike 중 하나.
- **어버이날·발렌타인·크리스마스**: 같은 패턴.

평상시 카카오톡의 초당 메시지 수가 수십만 건 단위인데, 그게 5~30배가 되면 산술적으로 분당 수억 건의 메시지가 처리돼야 한다. 이걸 단순히 "노드를 30배 늘려 두자"로 풀 수 있을까? 두 가지 이유로 답은 No다.

첫째, **비용**. 30배 capacity를 평소에 들고 있는 비용은 한 회사가 감당하기 어렵다. 둘째, **autoscale의 한계**. 0시 정각에 트래픽이 30배 점프하는 데, 그 시점에 autoscale로 노드 늘리려고 하면 이미 늦었다. cold start latency가 5~10분이라, 그 사이 1번 메시지부터 30번 메시지까지가 모두 지연된다.

그래서 한국 메신저들이 채택하는 패턴이 몇 가지 있다. 카카오 발표에서 명시적으로 풀이된 부분과 추정으로 정리해보면 다음과 같다.

1. **사전 예열(pre-warming)**: 새해 0시·설날 아침 같은 정해진 시간 전에 capacity를 미리 늘린다. autoscale에 기대지 않고, 운영자가 명시적으로 노드를 띄운다.
2. **백프레셔 + queue 흡수**: 메시지 큐(4장)를 두텁게 만들어 burst를 흡수한다. 메시지 일부에는 1~5초의 지연을 받아들이고, ordering을 보장한 채 흘려보낸다.
3. **group push fan-out 분리**: 1대N의 fan-out은 별도 layer에서 처리한다. 메시지 저장과 별개의 파이프라인이라, 저장이 빠르게 ack된 뒤 push가 비동기로 일어난다.
4. **광고 트래픽은 다른 패턴**: 점심·퇴근 시간대 spike는 메시지와 다른 시스템에서 처리한다 — 트래픽 분리가 곧 안전이다.

이 sidebar의 핵심은 한국 환경의 정시(0시·9시) 일제 트래픽이 **시스템 디자인을 elastic이 아닌 burst-tolerant로 만든다**는 점이다. 17장 fan-out 챕터에서 Twitter·Instagram의 fan-out 패턴을 볼 텐데, 그것이 글로벌 일상의 fan-out이라면 카카오톡 fan-out은 한국 정시 트래픽의 fan-out이다. 같은 패턴, 다른 압력. 잊지 말자.

## 채팅 시스템에서 1·2부가 모두 재등장하는 자리

여기까지 보고 나면 한 가지 그림이 자연스럽게 떠오른다. 채팅 시스템은 1·2부 모든 챕터의 회수 장면이다. 한 줄로 정리해보자.

- **2장 NoSQL hot partition** → Discord의 30K req/s 같은 메시지가 같은 partition을 두드리는 자리. data services의 coalescing이 그 답.
- **3장 캐시 stampede** → Discord coalescing의 다른 이름. 인기 채널 메시지가 곧 stampede의 대상.
- **4장 메시지 큐** → LINE의 Kafka, 카카오톡의 burst 흡수 queue. 비동기로 ordering을 지키는 1번 layer.
- **8장 시간·순서** → 채팅의 ordering 요구. 같은 채팅방의 단일 leader 또는 채널별 sequence number.
- **9장 보안** → WebSocket 위의 JWT·session token, secret rotation, 카카오톡의 E2E 암호화 도입 흐름.
- **13장 sharding** → Slack의 workspace, 당근의 거래(room_id), Discord의 channel_id가 모두 sharding key.
- **14장 관측성·on-call** → LINE의 Apache HTTP client 사건이 어떻게 일찍 잡혔는지, autoscale 미작동을 사전 예열로 어떻게 막는지.

이게 케이스 스터디의 약속이다. 1·2부의 학습이 한 시스템 안에서 어떻게 동시에 쓰이는지를 채팅이라는 도메인에서 처음 본다. 이 패턴이 17장 피드, 18장 검색·매칭, 19장 결제, 20장 이커머스로 가면서 반복된다. 어떤 시스템을 봐도 "이건 X장 Y절과 비슷하군"이라는 자동 mapping이 머릿속에 생기기 시작한다.

## Sidebar: 다른 유사 시스템 한 단락 — WhatsApp의 Erlang VM

본문이 다루지 못한 채팅 도메인의 또 다른 대표 사례를 한 단락으로 봐 두자. **WhatsApp**이다(검증 필요).

WhatsApp이 1조 메시지 단계로 가는 동안 한 가지 결정으로 유명하다. 처음부터 끝까지 **Erlang VM** 위에서 돌아간다. Erlang은 1980년대 통신사 스위치를 위해 설계된 언어인데, lightweight process(한 노드에 수십만 프로세스 가능)와 supervisor tree(실패 격리)가 채팅 도메인의 connection management·fault tolerance에 절묘하게 맞아떨어진다. 한 노드에 수십만 동시 connection을 운영하면서도 한 connection이 죽어도 다른 connection이 영향받지 않는다.

WhatsApp 인수 당시 50명도 안 되는 엔지니어가 5억 사용자를 운영했다는 사실이 자주 회자된다(검증 필요). 그 비밀의 절반은 Erlang의 선택이다. 나머지 절반은 단순함 — feature를 의도적으로 줄이고, 핵심 도메인(1대1·group 메시지)만 깊게 만든 것이다. **단순함이 운영의 무기**라는 점도 잊지 말자.

## Sidebar: 이 시스템의 운영 — SLO·alert·rollback

채팅 시스템의 운영을 한 페이지 따로 보자. 14장에서 본 일반 운영론이 채팅 도메인에서 어떻게 변주되는지의 한 사례다.

**핵심 SLI**: 메시지 send latency p99 (목표 100ms), message delivery success rate (목표 99.99%), WebSocket connection success rate (목표 99.95%). 이 셋이 채팅의 사용자 체감과 직결된다.

**SLO burn rate alerting**: 빠른 소진(1시간 동안 budget 2% 이상 소진)은 즉시 page, 느린 소진(6시간 5% 또는 24시간 10%)은 다음 영업일 ticket. WebSocket 끊김은 사용자가 직접 알아채는 자리라 page 임계값을 낮게 잡는다.

**Connection re-balance alert**: server pod이 떨어졌을 때 reconnect storm을 감지하는 alert가 따로 있다. 1분 안에 한 server pod에 reconnect가 평소 5배 이상 몰리면 즉시 page. autoscale이 따라오지 못하면 즉시 capacity 강제 증가.

**Rollback 전략**: 채팅 시스템은 message format 변경이 자주 일어난다. backward-compatibility를 깨는 변경은 절대 한 번에 배포하지 않는다 — feature flag로 1% → 10% → 100% 점진 rollout. 메시지가 한 번이라도 잘못 저장되면 영구 손실이라, blue-green이나 canary 같은 일반 패턴보다 더 엄격하게 적용한다.

**카오스 게임 day**: 분기별로 한 region을 의도적으로 끊는다. 5명 팀이 그 사이 사용자에게 영향이 가는지를 본다. 14장의 chaos engineering 패턴이 채팅 도메인의 안전 검증 1번 도구가 된다.

이 운영 5축이 채팅의 24/7 신뢰를 만든다. 가장 잔인한 시스템 중 하나라는 첫 줄을 다시 떠올려보자. 운영을 어떻게 만드느냐가 사용자가 느끼는 그 잔인함을 흡수한다.

## 이 장의 약속 회수

채팅 시스템을 직접 설계할 일이 없는 사람도, 이 장을 다 읽으면 한 가지를 머릿속에 가지고 갈 수 있다. **어떤 의사결정 축이 있고, 한국 메신저가 무엇을 골랐는지**의 한 페이지 표다.

5축의 trade-off (ordering·durability·history·real-time·fan-out), 그 위에 4개 회사의 결정(Discord·LINE·당근·Slack), 그리고 한국 환경의 트래픽 패턴(카카오톡 spike)이 한 그림으로 묶인다. 새로운 채팅 시스템을 봤을 때 어디에 점이 찍혀 있는지를 물을 수 있게 된다. 그게 1·2부의 약속이 케이스 스터디에서 처음 회수되는 자리다.

기억해두자. **채팅 시스템 설계의 본질은 자기 도메인의 1번 적을 정직하게 정의하는 일이다.** 당근이 Cassandra 운영 부담을 적으로 정의했기 때문에 DynamoDB를 골랐다. Discord가 GC와 hot partition을 적으로 정의했기 때문에 ScyllaDB + Rust coalescing을 만들었다. 적을 잘못 정의하면 비싼 도구를 사도 적이 죽지 않는다.

## 다음 장으로 가는 다리

채팅이 1대1과 group의 fan-out을 다뤘다면, 다음 장 피드·타임라인은 1대N (그것도 N이 1억까지 가는) fan-out의 극단을 본다. **1억 팔로워의 한 게시물을 모두에게 보여주는 비용을 누가 부담하는가?** 같은 fan-out이지만 카카오톡의 group push와는 다른 게임이다. Twitter의 hybrid fan-out, Instagram의 Cassandra timeline, 카카오톡의 group push가 어떻게 같은 문제를 다르게 풀고 있는지를 살펴보자.

가기 전에 한 번 정리하자. **운영해 보면 가장 잔인한 시스템 중 하나라는 사실은 그 시스템의 약점이 아니라 그 시스템의 본질이다.** 잔인함을 정직하게 마주한 회사만이 1조 메시지의 신뢰를 만든다. 우리도 자기 도메인 안에서 같은 정직함을 가질 수 있는가, 가 케이스 스터디 5개 장의 공통 질문이다.

---

---

# 17장. 피드·타임라인·알림 — Twitter·Instagram·카카오톡 fan-out

어떤 가수가 트윗을 올린다고 해보자. 팔로워가 1억 명이다. 이 한 글을 1억 명의 home timeline에 미리 박아 두려면 1억 번 write가 필요하다. 실시간으로 가능할까? Twitter 엔지니어들이 처음 던진 질문이 정확히 이거다. 그리고 답은 "한 모델로는 안 된다"였다. **celebrity는 pull, 일반 사용자는 push.** 이 hybrid 모델이 modern 피드 시스템의 default가 됐다.

그런데 그 hybrid의 단순한 문장 뒤에 결정해야 할 것들이 한 무더기 쌓여 있다. celebrity의 기준은 누가 정하는가? 10만 팔로워? 100만? push의 비용과 pull의 latency는 어느 자리에서 만나는가? 일반 사용자가 어느 날 갑자기 viral해서 1억 팔로워를 얻으면 시스템은 무엇을 하는가? 그리고 알림(push notification)이라는 또 다른 레이어 — APNS·FCM·웹푸시 — 가 그 위에 한 번 더 얹힌다. 이번 장에서는 Twitter·Instagram·카카오톡 같은 시스템이 이 결정들을 어떻게 풀어냈는지 한 박자씩 짚어 가자.

## 1. Fan-out 세 갈래 — push·pull·hybrid

피드 시스템의 가장 근본적 결정은 **fan-out 모델**이다. "한 사람이 글을 올렸을 때, 그 글이 팔로워들의 home timeline에 어떻게 도착하는가." 답은 세 갈래다.

### Push (fan-out-on-write)

글이 올라오면 **즉시** N명 팔로워의 timeline 캐시에 미리 박아 둔다. read 시점에는 자기 timeline cache만 읽으면 끝나니까 매우 빠르다. 13장 샤딩에서 짧게 짚은 user-by-shard 모델이 이 구조의 토대다.

```
A가 글을 올림 → A의 팔로워 N명의 timeline cache에 즉시 fan-out write
→ 각 팔로워가 read하면 자기 timeline cache 읽기 (한 번의 read로 끝)
```

장점은 분명하다. **read latency가 작고 예측 가능**하다. 사용자 경험이 가장 매끈하다. 단점은 — celebrity가 글 하나 올릴 때 1억 번 write가 필요해진다는 점이다. 비용과 latency가 폭발한다.

### Pull (fan-out-on-read)

write 시점에 아무것도 안 한다. read 시점에 사용자가 follow하는 모든 사람의 최근 글을 모아서 정렬한 뒤 응답한다.

```
A가 글을 올림 → A의 글 store에 저장만 함
사용자 B가 home timeline 요청 → B가 follow하는 모든 사람의 최근 글을 query → merge·정렬 → 응답
```

장점은 — **write가 싸다.** celebrity가 글 1억 개 올려도 write는 1번이다. 단점은 — **read가 비싸다.** B가 1만 명을 follow하면 read마다 1만 명의 store를 뒤져야 한다. latency가 부풀어 오른다.

### Hybrid — celebrity는 pull, 일반은 push

Twitter가 2010년대 초중반에 자리 잡힌 답이 hybrid다 (W23). 단순한 한 줄.

> celebrity (예: 10만 팔로워 이상)는 pull, 일반 사용자는 push.

각 사용자의 home timeline은 두 source로 구성된다.
- (1) 일반 follow 대상이 push해서 미리 박아 둔 timeline cache
- (2) celebrity follow 대상의 최근 글을 read 시점에 pull해서 합친 결과

read 시점에 (1)과 (2)를 merge하면 완성된 home timeline이 만들어진다. push 비용을 일반 사용자에 한정하고, pull 비용을 celebrity의 일부 follow로 제한한다 — 양쪽 비용 모두 통제 가능한 범위로 떨어진다.

### 세 갈래 비교 표

| 축 | Push | Pull | Hybrid |
|---|---|---|---|
| Write 비용 | O(팔로워 수) | O(1) | O(보통 팔로워 수) |
| Read 비용 | O(1) | O(follow 수) | O(celebrity follow 수) |
| Read latency | 매우 낮음 | 변동 큼 | 낮음~중간 |
| Storage | 사용자별 timeline cache | 글 store만 | 양쪽 모두 |
| 어울리는 곳 | 보통 사용자 분포 | follow 비대칭 큰 곳 | 대부분 modern 피드 |
| 대표 사례 | 작은 SNS, 초기 Facebook | 단순 RSS 리더 | Twitter·Instagram |

회의 자리의 정답은 보통 hybrid다. **단, hybrid를 시작하기 전에 push로 충분한지 한 번 더 물어보자.** 사용자 100만 명에 follow 분포가 비교적 균등하다면 push만으로도 살아간다. hybrid는 정당화가 필요한 복잡도다 — celebrity가 시스템 비용을 무너뜨리기 시작할 때 비로소 도입의 자격이 생긴다.

## 2. Celebrity 임계값을 어떻게 정할 것인가

hybrid에서 가장 까다로운 결정이 **"누가 celebrity인가"**라는 임계값 설정이다. 너무 낮게 잡으면 pull 비용이 모든 read에 깔린다. 너무 높게 잡으면 push 비용이 실제 celebrity에서 폭발한다.

Twitter 엔지니어링 블로그에서 자주 인용되는 한 줄 — **"약 10K 팔로워가 우리의 절단점이었다"** (검증 필요, W23). 다만 이 숫자는 Twitter의 워크로드·인프라·비용 구조에 맞춰진 값이다. 우리 회사 사이즈에는 다른 숫자가 어울린다.

임계값 결정을 위한 다섯 질문은 다음과 같다.

1. **한 push의 비용은 얼마인가?** Redis write 한 번이 얼마, Kafka publish 한 번이 얼마. 그걸 N팔로워에 곱하면 한 글의 fan-out 비용.
2. **한 pull의 비용은 얼마인가?** N follow의 글 store를 read해서 merge하는 비용. follow 수에 비례.
3. **사용자 분포의 long tail은 어떻게 생겼는가?** 99% 사용자가 1만 이하라면 임계값을 거기 두는 게 자연스럽다.
4. **사용자가 자기 follow 수를 늘리는 속도는?** 어제 1만이던 사용자가 오늘 10만이 되면 — 어느 자리에서 hybrid로 옮길지의 동적 전환 로직이 필요하다.
5. **알림이 따라 가야 하는가?** push가 timeline cache에만 들어가는지, 푸시 알림까지 트리거되는지에 따라 비용 모양이 다르다.

이 다섯 질문에 답이 명확하면, 임계값은 자연스럽게 정해진다. 그리고 **임계값은 한 번 정하고 끝나는 숫자가 아니다.** 사용자 분포·인프라 비용·viral 패턴이 바뀌면 임계값도 따라간다 — modern 피드 시스템은 보통 이 임계값을 모니터링·자동 조정하는 layer를 따로 둔다.

## 3. Twitter Timeline — Manhattan + Redis cluster

Twitter의 timeline 시스템을 한 자리에 모아 보자. 2017년 발표 자료(W23)에서 자주 인용되는 구조다.

### 저장소 layer

- **Manhattan** — Twitter가 자체 개발한 distributed KV store. user metadata, tweet 자체, social graph 일부를 저장한다.
- **Redis cluster** — 사용자별 timeline cache를 저장한다. 각 사용자의 최근 800~1000개 tweet ID 리스트가 Redis list로 들어간다.
- **Tweet store** — actual tweet 본문 + media reference. Manhattan 위에 layer.

### 처리 흐름

```
tweet 작성:
  → tweet store에 저장 (1번)
  → 일반 follower들의 Redis timeline cache에 push (N번, fan-out worker)
  → celebrity인 경우 push 안 함

home timeline read:
  → user의 Redis timeline cache에서 tweet ID list 읽기
  → user가 follow하는 celebrity의 최근 tweet 직접 pull (Manhattan query)
  → 둘을 merge·정렬·필터링
  → tweet 본문은 tweet store에서 batch fetch
  → 응답
```

이 흐름의 가장 무거운 자리는 **fan-out worker**다. tweet 한 개가 발행되면 fan-out worker가 follow graph를 traverse해 각 팔로워의 Redis에 write를 보낸다. 평균 follower 수를 가정하면 한 tweet에 수백~수천 번 write. tweet 발행 빈도가 분당 수십만이라면 fan-out worker의 throughput이 시스템의 1차 제약이다.

### 운영 sidebar — 이 시스템의 운영

Twitter의 timeline 운영에서 자주 짚히는 자리들:

- **Celebrity alert**: 새로운 celebrity가 등장하면(예: 어떤 사용자가 갑자기 10K 팔로워 돌파) hybrid 라우팅을 자동으로 갱신해야 한다. 이게 늦으면 push 비용이 폭발한다.
- **Timeline cache eviction**: 모든 사용자의 timeline cache를 영원히 들고 있을 수 없다. inactive 사용자(예: 30일 동안 안 들어온)는 cache eviction. 다시 들어오면 backfill로 복구.
- **Fan-out worker lag**: fan-out worker queue가 lag 4시간이 되면 — 사용자 timeline에서 4시간 전 tweet이 그제서야 보이는 사고다. 큐 길이 alert이 SLO의 1차 신호.
- **Hot key**: celebrity가 tweet 하나 올렸을 때 그 tweet의 read가 한 partition에 몰린다. 2장 NoSQL의 hot partition이 정확히 이 자리에 다시 등장. request coalescing + 캐싱 layer가 답.

### 결정적 한 자리 — viral pivot

Twitter timeline 운영의 가장 잔인한 자리 한 가지를 더 짚어 두자. **viral pivot**이다. 평범한 사용자가 한 tweet으로 갑자기 1억 view를 얻는 순간 — 그 사람의 hybrid 분류가 일반에서 celebrity로 동적으로 전환되어야 한다. 그렇지 않으면 그 사용자가 다음 tweet을 올릴 때마다 1억 명에게 push가 시도되어 fan-out worker가 무너진다. 이 자동 전환을 어떻게 빠르게 감지하고 안전하게 옮길지가 운영의 결정적 한 줄이다. 같은 사용자에 대한 fan-out 결정을 한 박자 안에 바꾸려면, follow graph 안의 그 사용자 metadata를 update + 일관성 있게 모든 fan-out worker에 전파해야 한다 — 12장 합의·복제의 단어들이 production의 잔인한 자리에서 등장하는 한 사례다.

## 4. Instagram — Python·Django·PostgreSQL + 사진 S3

Instagram은 다른 출발점에서 다른 답에 도달했다 (W24). Twitter가 자체 Manhattan·Redis cluster를 만들었다면, Instagram은 **Django + PostgreSQL + Cassandra + S3**로 시작했다.

### 저장소 layer

- **PostgreSQL** — user metadata, social graph, post metadata. user_id 기반 sharding.
- **Cassandra** — feed cache (Twitter의 Redis timeline cache 역할).
- **S3** — 사진 자체. 다양한 해상도로 multi-resolution thumbnail 저장.
- **Memcached** — read-heavy hot key 캐싱.

### Fan-out 모델

Instagram의 초기 fan-out은 **Gearman**(작업 큐)으로 작업을 분산했다. tweet 작성 시 Gearman worker가 follower들의 feed cache에 push. 사용자 증가에 따라 Gearman은 **Kafka 기반 fan-out pipeline**으로 옮겨갔다. Kafka가 backpressure·replay·scalability 측면에서 훨씬 단단했기 때문이다 (4장·15장 callback).

### Ranking layer — 시간 순이 답은 아니다

Instagram이 Twitter와 결정적으로 다른 한 가지는 **ranking**이다. 2016년 Instagram이 시간 역순 timeline을 폐지하고 **engagement-based ranking**으로 옮긴 결정이 있었다. 사용자별로 "이 글이 얼마나 흥미로울까"를 ML model로 예측해 정렬한다.

이게 fan-out 구조에 영향을 미친다. **모든 글이 user에게 보일 후보**가 되어야 하므로, push와 pull을 단순히 시간 순으로 merge하면 안 된다. ranking score를 함께 계산하고 top N개만 응답하는 구조가 된다.

```
home timeline read:
  → push timeline cache + pull celebrity 글 = candidate pool
  → 각 candidate에 ranking score 계산 (engagement·recency·diversity·...)
  → top 50개 선택
  → 응답
```

ranking score 계산은 별도 ML model serving layer가 책임진다. **feature store**(예: Feast, Tecton)에서 user feature·item feature·context feature를 가져와 model이 추론한다. 이 layer가 추가되면 시스템 복잡도가 한 단계 더 올라간다. 처음부터 ranking을 도입할 자격이 있는지 한 번 묻는 편이 낫다 — 대부분의 회사에 시간 역순 timeline이 정답이고, ranking은 사용자 수가 일정 규모를 넘었을 때 비로소 의미가 있다.

## 5. 카카오톡 fan-out — 한국 4 sidebar

한국 백엔드 시각에서 가장 흥미로운 fan-out 사례는 카카오톡이다(community 한국 4).

### 그룹 채팅의 fan-out

카카오톡 그룹 채팅에서 메시지 1개가 발행되면 — 그 그룹의 N명에게 모두 push가 가야 한다. 이게 정확히 Twitter의 fan-out과 같은 구조다. 다만 한국 메신저 시장의 특수성이 몇 가지 더 얹힌다.

- **새해·설날·발렌타인 traffic spike** — 평상시 대비 5~30배 트래픽이 한 순간에 몰린다 (한국 4). 0시 정각 새해 인사 같은 패턴은 fan-out worker queue를 한 박자에 폭발시킨다.
- **단톡방 광고·스팸** — 한 사람이 광고 메시지를 100개 그룹에 동시 발행하면, 각 그룹의 N명에게 fan-out 비용이 곱셈으로 늘어난다. rate limiting + abuse detection이 fan-out 앞에 깔린다.
- **푸시 알림 → 사용자별 OFF/ON** — 모든 메시지가 푸시 알림으로 전달되지 않는다. 사용자별 알림 설정(전체 OFF, 키워드 ON, 시간대 제한 등)이 fan-out 결정에 들어간다.

### "미리 계산" 패턴

if(kakao) 2022·2023 발표에서 자주 인용되는 한 패턴 — **"새해 인사처럼 예측 가능한 spike는 미리 계산해 둔다"** (검증 필요, 카카오 발표 원문 확인 권장). 0시 정각 직전에 fan-out worker 인스턴스를 N배 늘리고, 일부 timeline cache를 pre-warm한다. **chaos·spike를 예측하고 평소에 준비해 두는 것이 한국 메신저 운영의 핵심**이다 — 13장 chaos engineering·rate limit의 한국 적용 사례와 닿는다.

### 단톡방의 fan-out 위계

카카오톡의 단톡방은 일반 1대1 채팅보다 fan-out 결정이 한 단계 더 까다롭다. 인원 수에 따라 다른 모델이 적용되는 셈이다. 인원 100명 이하의 작은 단톡방은 단순 push가 자연스럽다. 인원이 1만 명 이상인 오픈채팅 같은 자리는 — 모든 메시지에 push를 보내면 fan-out worker가 무너지고, push 알림 비용도 폭발한다. 그래서 큰 단톡방에서는 hybrid 모델이 들어간다. 일부 사용자만 push, 나머지는 read 시점에 pull. 그리고 그 안에서도 "내가 mention된 메시지는 push, 일반 메시지는 pull" 같은 사용자별 세부 결정이 한 번 더 얹힌다. 한 카톡 메시지가 사용자 device에 도달하는 길은 — 표면에서 보는 것보다 훨씬 많은 결정을 거치고 있다. 카카오 엔지니어링의 한 발표가 이 위계를 정직하게 짚었다는 점이 인상적이다 (검증 필요).

### 시스템의 운영 — 이 챕터의 운영 sidebar

카카오톡 fan-out 시스템의 운영에서 자주 짚히는 자리:

- **Fan-out queue length SLO**: 평상시 lag 1초 이내, spike 시 lag 10초 이내. 그 위는 alert.
- **APNS·FCM throttling 대응**: Apple/Google이 자기 서버 보호를 위해 throttle을 거는 자리. retry + backoff + jitter가 필수 (10장 callback).
- **Rate limit per sender**: 한 사람이 분당 N개 이상 메시지 발행 못함. 광고 스팸 방어 + fan-out 비용 통제.
- **Progressive rollout for feature changes**: 알림 UI 변경 같은 release는 1% → 10% → 100% canary (14장 callback). 카카오톡 사용자가 5천만이라는 점이 progressive rollout의 정당성을 강화한다.

## 6. 알림(Push Notification) — APNS·FCM·웹푸시

피드와 함께 자주 등장하는 영역이 **푸시 알림**이다. 사용자가 앱을 안 열어 둔 상태에서도 "새 메시지가 왔어요" 같은 알림을 보내려면 OS 레벨 push channel을 거쳐야 한다.

### 세 channel

- **APNS (Apple Push Notification Service).** iOS·macOS. token 기반, HTTP/2 connection.
- **FCM (Firebase Cloud Messaging).** Android·iOS·웹. token 기반, 다양한 priority·collapse key.
- **웹푸시 (Web Push Protocol).** RFC 8030. VAPID 키 기반, 브라우저 native.

각 channel은 자기 protocol·SLO·throttle 정책을 가진다. 우리 application은 그 세 channel을 추상화한 **notification service**를 한 layer 둔다. application 레벨 코드는 "notification을 보내라"만 호출하고, channel별 디테일은 service가 처리한다.

### 운영 디테일

푸시 알림은 fan-out과 결합되면 운영 디테일이 더 까다로워진다.

- **Deduplication.** 같은 사용자에게 같은 알림을 두 번 보내지 않기 위해, idempotency key가 필요하다 (10장 callback). 한 메시지의 fan-out이 retry되면 같은 알림이 두 번 전송될 수 있다.
- **Rate limit per recipient.** 한 사용자에게 분당 알림 N개 이상은 안 보낸다. 알림 폭탄 방어.
- **Token expiration·refresh.** APNS·FCM token은 OS 업데이트·앱 재설치 시 변경된다. invalid token 응답을 받으면 token 갱신 흐름을 트리거해야 한다.
- **Backpressure from channel**: APNS가 throttle 응답을 보내면 우리 system이 backpressure를 받아야 한다. 그렇지 않으면 notification service 큐가 lag 4시간으로 쌓인다 (14장 callback).

알림은 작아 보이는 layer지만 — 운영에서 가장 자주 사용자 불만이 흘러나오는 자리다. "알림이 안 와요" 또는 "알림이 너무 많이 와요"가 거의 동시에 들어온다. SLO·alert·rate limit이 모두 잘 박혀 있어야 사용자 경험이 무너지지 않는다.

## 7. 캐시의 역할 — timeline cache와 fanout cache

피드 시스템에서 캐시는 단순한 KV가 아니다 — **fanout의 데이터 구조 자체**다. 3장에서 짚은 캐시의 일반론이 여기서 새 형태로 등장한다.

### Timeline cache의 구조

각 사용자의 timeline cache는 보통 **Redis list 또는 sorted set**이다.

```
Redis: user:12345:timeline → [tweet_id_1, tweet_id_2, ...]
       (최근 800~1000개)
```

새 tweet이 push되면 list 앞에 LPUSH, 오래된 tweet은 list 끝에서 LTRIM. 이런 자료구조 자체가 **자연스럽게 fan-out 비용을 통제**한다. 사용자별로 800개 한도가 박혀 있으니 메모리 폭주가 없다.

### Cache stampede 대비

timeline cache가 비어 있는 사용자(예: 신규 또는 inactive)가 들어오면, backfill이 일어난다. backfill은 follow 그래프 + 최근 tweet store에서 reconstruct하는 비용이 큰 작업이다. 동시에 100명이 backfill을 요청하면 — 3장 캐시의 thundering herd 패턴이 정확히 등장한다.

방어 도구는 익숙하다.
- **Singleflight / request coalescing**: 같은 사용자에 대한 동시 backfill 요청을 1번으로 합친다 (2장 Discord callback).
- **Jittered TTL**: timeline cache의 만료 시각에 random jitter를 더한다.
- **Background pre-warm**: inactive 사용자가 다시 로그인할 때를 예측해 미리 backfill.

이 패턴들은 채팅 시스템·검색 시스템에도 그대로 쓰인다. **fanout이 있는 모든 시스템은 thundering herd 방어가 default 운영 도구**다 — 기억해 두자.

## 8. 의사결정 트리 — 우리 피드는 어디서 멈출 것인가

피드 시스템을 처음 설계하거나 기존 시스템을 손볼 때 자기에게 던질 다섯 질문이다.

1. **사용자·follow 분포는 어떻게 생겼는가?** 균등하다면 push로 충분. long tail이 길다면 hybrid.
2. **celebrity 임계값은 무엇으로 정할 것인가?** 비용 측정 + 사용자 분포 + viral 패턴. 한 번 정한 임계값을 모니터링·자동 조정하는 layer를 따로 두자.
3. **timeline ranking이 필요한가?** 사용자 수가 일정 규모를 넘었거나, content diversity가 중요한 도메인에서만 도입. 처음부터 도입할 자격은 거의 없다 — 시간 역순으로 시작하자.
4. **푸시 알림은 어떤 channel이 필요한가?** 모바일이면 APNS·FCM, 웹이면 웹푸시. notification service 한 layer로 channel을 추상화하자.
5. **운영 alert는 어디에 박혀 있는가?** fan-out queue length, push channel throttle, timeline backfill lag, celebrity rerouting 지연 — 이 네 자리가 SLO의 1차 신호다.

이 다섯 질문이 머릿속에 자동으로 펼쳐지면, 회의 자리에서 피드 시스템 결정을 첫 5분 안에 풀어낼 수 있다.

## 9. 다른 유사 시스템 sidebar — TikTok recommendation pipeline

본 챕터가 다루지 못한 대표 시스템 하나를 1단락으로 압축해 두자. **TikTok**의 피드는 "follow 그래프 기반 fan-out"이 아니라 **"For You Page (FYP) recommendation pipeline"** 이 중심이다. follow하지 않는 사용자의 콘텐츠도 사용자 행동·viral 신호 기반으로 추천된다. 이 구조에서는 fan-out 자체가 거의 사라지고, **candidate generation + ranking + filter**의 ML pipeline이 timeline의 주역이 된다. Twitter·Instagram이 "친구의 글을 어떻게 보여줄까"였다면, TikTok은 "이 사람에게 보여줄 글을 어디서 가져올까"가 본질 — 같은 피드라는 단어 안에 본질적으로 다른 시스템이 있다는 점, 기억해 두자.

## 10. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 피드·타임라인·알림 시스템의 지형이 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **Fan-out 세 갈래** — push (write 비쌈, read 쌈) / pull (write 쌈, read 비쌈) / hybrid (Twitter default). 대부분 modern 피드가 hybrid.
- **Celebrity 임계값**은 한 번 정하고 끝나는 숫자가 아니다. 사용자 분포·인프라 비용·viral 패턴이 바뀌면 따라 움직여야 한다.
- **Twitter Timeline** — Manhattan + Redis cluster + fan-out worker. hot key 방어는 request coalescing(2장 callback).
- **Instagram** — Python·Django·PostgreSQL·Cassandra·S3 + engagement-based ranking. fan-out은 Gearman → Kafka로 진화.
- **카카오톡 fan-out** — 새해·설날 5~30배 spike를 미리 계산. 광고 스팸 방어 + 사용자별 알림 설정이 fan-out 결정에 들어간다.
- **알림 layer** — APNS·FCM·웹푸시 세 channel + notification service 추상화. dedup·rate limit·token refresh가 운영의 1차 도구.
- **Timeline cache는 fanout 데이터 구조다.** Redis list/sorted set + thundering herd 방어(singleflight·jittered TTL)가 default.
- **운영 SLO의 1차 신호** — fan-out queue length·push channel throttle·timeline backfill lag·celebrity rerouting 지연. 그게 새벽 3시의 자신을 살린다.

다음 장(18장)에서는 검색·매칭·지오를 짚는다. 쿠팡 검색·Airbnb 검색·Uber dispatch·당근 hyperlocal — "근처 어디"와 "찾고 싶은 무엇"을 합치는 시스템들의 결정 패턴을 함께 들여다보자.


---

# 18장. 검색·매칭·지오 — 쿠팡·Airbnb·Uber·당근

당근에 글을 올리면 우리 동네에서만 보이고 옆 동네에서는 안 보인다. 이 단순한 사실이 처음에는 당연해 보인다. 그런데 한 번 멈춰서 생각해보자. 사용자가 "사당동"에 살고, 검색은 "30분 안에 만날 수 있는 거리"여야 하고, 글은 "동네 단위"로만 보여야 한다. 그리고 이 모든 결정이 동시에 빠르게 — 보통 50ms 안에 — 일어나야 한다. 한국이라는 도메인이 시스템 설계 결정에 미친 영향이 가장 노골적으로 드러나는 사례다.

검색·매칭·지오라는 세 도메인을 한 챕터에 묶은 이유가 있다. 셋이 같은 골격 위에 서 있다. **"index에서 후보를 좁히고, scoring으로 순위를 매기고, dispatch로 사용자에게 흘려보낸다."** 어떤 도메인이든 이 세 단계의 합이다. 쿠팡 검색이 이걸 한 가지 방식으로, Airbnb 검색이 다른 방식으로, Uber dispatch가 또 다른 방식으로 푼다. 같은 골격, 다른 압력이다.

"근처 어디"와 "찾고 싶은 무엇"을 합치는 시스템은 어떻게 만들어지는가 — 이 질문에 답할 수 있어야 검색·매칭·지오를 안다고 말할 수 있다. 그리고 한국 hyperlocal이 미국 글로벌 매칭과 어떻게 다른 게임인지를 정확히 셈할 수 있어야 한다.

## 검색·매칭·지오의 공통 골격 — index + scoring + ranking + dispatch

먼저 셋의 공통 구조를 한 페이지에 압축해보자. 어떤 검색·매칭·지오 시스템을 떼어 보더라도 다음 4단계로 분해된다.

1. **Index 구축**: 검색 가능한 모든 entity(상품·숙소·드라이버·매물)를 어떤 기준으로 색인한다. inverted index, vector embedding, H3 hexagonal grid가 모두 index의 한 형태다.
2. **Candidate retrieval**: 사용자 query에 대해 후보를 N개 추린다. 보통 1만~10만 → 200개 수준의 1차 필터링. 5장에서 본 ES inverted index, Airbnb의 IVF ANN, Uber의 H3 k-ring이 모두 이 단계다.
3. **Scoring + ranking**: 후보를 정밀하게 점수 매긴다. ML 모델, business rule, 가격·평점·거리의 weighted sum이 여기서 동작한다. 후보 200개 → 정렬된 20개.
4. **Dispatch**: 결과를 사용자에게 흘려보낸다. 검색은 list 응답으로, 매칭은 driver assignment로, 지오는 인접 cell의 entity 노출로. 응답 latency는 보통 p99 100~500ms.

이 4단계가 검색·매칭·지오의 본체다. 도메인이 달라져도 이 골격은 거의 안 바뀐다. 다른 것은 1단계 index가 무엇으로 구성되는가, 그리고 4단계 dispatch에서 무엇이 사용자 체감의 1번 신호인가다.

이 골격을 머리에 박아두고 네 시스템을 차례로 살펴보자. 같은 골격, 다른 압력의 그림을 본다.

## 쿠팡 검색 — 한국어 형태소와 indexing pipeline의 silent killer

쿠팡 검색은 한국 e-commerce 검색의 베이스라인이다. 쿠팡 엔지니어링 블로그가 정리한 시스템 구조를 한 단락으로 줄이면 다음과 같다(W32).

> Elasticsearch + Kafka indexing pipeline. 상품 update event는 Kafka로 흘러 들어가고, indexer가 ES shard에 반영한다. 검색 query는 ES에 직접 들어가지 않고 search service가 한 layer 더 위에서 처리한다. (쿠팡 엔지니어링)

별로 새로운 그림이 아니다. ES + Kafka 조합은 5장에서 본 표준 indexing 패턴이다. 그런데 쿠팡이 이 시스템에서 가장 자주 부딪힌 함정 두 가지가 인상적이다.

**첫 번째, 한국어 형태소 분석.** 영어 분석기로 한국어 검색을 그대로 돌리면 "쿠팡 배송"으로 검색했을 때 "쿠팡배송"이 안 나온다. 한국어는 띄어쓰기와 조사가 검색을 어렵게 만든다. 5장에서 본 mecab-ko, NORI, KOMORAN, Khaiii, KIWI 같은 한국어 형태소 분석기 중 하나를 골라 색인 단계에 박아야 한다. 분석기 선택이 검색 품질의 30%를 결정한다(한국 3).

쿠팡은 NORI를 기반으로 자체 dictionary를 쌓아 올리는 길을 갔다고 알려져 있다(검증 필요). "로켓배송"·"새벽배송"처럼 쿠팡 도메인 고유 용어를 dictionary에 박지 않으면, 사용자가 "로켓"으로 검색했을 때 "로켓배송" 상품이 안 나오는 끔찍한 일이 생긴다.

**두 번째, indexing pipeline의 silent killer.** 1장 sidebar에서 한국 백엔드의 silent killer로 JPA N+1을 봤다. 5장에서는 검색 인덱싱 파이프라인의 silent killer가 따로 있다. 가장 흔한 시나리오를 떠올려보자.

- 상품 가격이 update된다 → Kafka에 event 발행
- indexer가 event를 consume → ES bulk update
- 사용자 검색 query는 cache hit 상태 → 30초간 stale 가격 노출
- 그 30초 사이에 누군가 cache 만료된 가격으로 결제 시도 → 가격이 안 맞아 실패

이 silent killer는 production에서는 들키지 않는다. 사용자가 한 명씩 결제 실패하는데, "왜 안 되지?" 새로고침하면 그새 cache가 갱신돼 잘 된다. 일주일에 한 번씩 OKKY에 "쿠팡에서 결제할 때 가격이 바뀌었다는 알림 뜨는데 뭐죠?" 같은 글이 올라온다. 이게 indexing pipeline의 staleness가 사용자에게 새는 자리다.

쿠팡이 어떻게 대응했는지는 명확히 공개되지 않았지만(검증 필요), 일반적인 대응은 다음 세 가지의 조합이다.

1. **가격 같은 hot data는 short TTL (10초 이하).**
2. **search service가 ES 결과를 받은 직후 가격을 primary DB에서 한 번 더 verify.** latency 비용은 늘지만 staleness가 잡힌다.
3. **결제 단계에서 다시 한 번 가격을 verify.** 사용자가 결제 버튼을 누른 순간이 진실의 기준점.

이게 검색이 1·2부의 캐시·NoSQL·Kafka·결제 모두와 어떻게 묶이는지의 한 사례다. 검색은 검색 단독으로 안 끝난다. 데이터 파이프라인 전체의 정합성이 사용자 마지막 클릭까지 이어진다.

## Airbnb 검색 — IVF ANN을 HNSW 대신 고른 이유

검색 도메인을 더 깊게 보려면 vector search의 결정 한 자리를 짚고 가야 한다. Airbnb는 embedding-based retrieval 시스템에서 한 가지 인상적인 결정을 했다(W28, 자료 4.8).

> IVF(Inverted File Index) ANN을 HNSW 대비 채택. 이유: high real-time update rate — 가격과 가용성이 빈번히 변경되기 때문. (Airbnb Tech)

vector search 알고리즘 두 가지를 빠르게 비교해보자.

| 항목 | HNSW (Hierarchical Navigable Small World) | IVF (Inverted File Index) |
|------|--------------------------------------------|----------------------------|
| **search latency** | 빠름 (수십μs~수ms) | 약간 느림 (수~수십ms) |
| **build cost** | 높음 (graph 구축) | 중간 (centroid clustering) |
| **incremental update** | 어려움 — graph 재구축 필요 | 쉬움 — 단순 inverted list 추가 |
| **recall (정확도)** | 매우 높음 | 비슷하지만 약간 낮음 |
| **권장 케이스** | static catalog, 정밀 검색 | high real-time update |

Airbnb의 도메인을 떠올려보자. 숙소 가격은 시즌·요일·이벤트마다 바뀐다. 가용성(available/unavailable)은 예약 한 건만 들어와도 즉시 바뀐다. 이런 도메인에서 HNSW를 쓰면 graph 재구축 비용이 비명을 지른다. 그래서 약간의 latency를 양보하고 incremental update가 쉬운 IVF를 택했다.

이 결정에 한 가지 교훈이 있다. **"가장 빠른 알고리즘이 가장 좋은 알고리즘이 아니다."** 도메인의 update 패턴이 알고리즘 선택의 1번 변수다. Discord가 ScyllaDB를 고른 결정(16장)도 같은 결이다. 자기 도메인의 가장 큰 적이 무엇인지를 정직하게 정의했기 때문에 비싼 결정을 할 수 있었다.

그리고 Airbnb 글에서 한 가지 더 인상적인 부분이 있다. 시스템 운영 standards다.

> SOA service platform standards로 모든 신규 service에 outlier detection과 circuit breaker를 강제. (Airbnb Tech, W28)

10장에서 본 회복력 패턴(circuit breaker)을 organization-wide standard로 강제했다. 한 service가 느려지면 다른 service가 그걸 자동으로 차단한다. mesh를 깐 게 아니라, 모든 service의 코드 standard로 circuit breaker가 들어 있다. 잊지 말자. 회복력은 mesh의 기능이기 전에 조직 standard의 결정이다.

## Uber Dispatch — H3 hexagonal grid가 풀어준 매칭의 본질

매칭 도메인의 가장 유명한 케이스가 Uber Dispatch다(W26, 자료 4.6). 핵심 결정 한 자리가 모든 것을 단단하게 만든다.

> 지구를 icosahedron(20면체)으로 분할한 다음, hexagon 계층 grid로 나눈다 — 0~15 resolution. H3라고 부른다. (Uber Engineering)

왜 hexagon인가? square grid나 geohash와 비교해보면 답이 나온다.

| 격자 방식 | 이웃 cell 수 | 이웃 거리 균등성 | 계층 구조 | 한국 활용 |
|------------|---------------|--------------------|-------------|-------------|
| **Geohash** | 8개 (모서리 vs 변) | 비균등 — 모서리가 멀다 | base32 prefix 자연 계층 | 흔함 |
| **S2 (Google)** | 8개 | 비균등 | Hilbert curve 기반 | Google 계열 |
| **H3 (Uber)** | 6개 (모두 변) | **균등** | parent-child 계층 | Uber·당근(추정) |

hexagon은 이웃이 6개고, 모든 이웃과의 거리가 같다. 매칭처럼 "가장 가까운 후보 N개"를 찾는 도메인에서는 이 균등성이 결정적이다. square grid에서는 같은 cell 두 칸 옆이 대각선 이웃보다 더 가깝다는 어이없는 일이 생긴다. H3에서는 그런 모순이 없다.

H3 위에 Uber가 얹은 dispatch optimizer가 DISCO다. 한 줄로 줄이면 이렇다.

> 매칭은 단순 "가장 가까운 driver"가 아니다. wait time, repositioning cost, ML acceptance probability, driver preference의 multi-objective optimization. (Uber Engineering, W26)

"가장 가까운 driver를 보낸다"는 직관은 틀렸다. 가까운 driver가 거절할 수도 있고, 그 driver를 보내면 다른 zone에 공급이 부족해질 수도 있다. ML 모델이 "이 driver가 이 ride를 받을 확률은 70%"라고 예측하면, 그 70%와 거리·repositioning cost를 같이 셈해서 최종 후보를 고른다. 이게 multi-objective optimization의 실전 사례다.

한국으로 옮겨와 보자. **배민 라이더 dispatch도 같은 골격을 쓰지만, 압력이 다르다.** 배민은 한 점심 시간에 한 라이더가 여러 주문을 묶음 배달한다. 1대1 매칭이 아니라 1대N batching이다. multi-objective에 batching constraint가 더 들어간다. 도메인이 미세하게 다르면 같은 H3 + optimizer 위에서도 결정의 변수가 한 차원 더 생긴다.

이게 매칭 시스템이 한국 도메인에서 어떻게 변주되는지의 한 사례다. 라이브러리는 글로벌이지만, 도메인 압력은 항상 로컬이다.

## 당근 hyperlocal — 동(neighborhood) 단위 partition

이제 당근으로 와 보자. 한국 hyperlocal이 시스템 설계에 미친 영향이 가장 노골적인 사례다(W31, 한국 7, 자료 4.11).

당근의 sharding key는 **동(neighborhood)**이다. 사용자가 사는 동을 partition key로 박는다. 같은 동의 사용자만 같은 상품을 본다. 옆 동은 partition이 다르다.

이 결정이 무엇을 풀어주는가? 세 가지를 한꺼번에 푼다.

1. **검색 query 좁히기**: "사당동"이라는 partition 안에서만 search한다. ES shard가 자연스럽게 동 단위로 갈린다. cross-shard query가 거의 없으니 latency가 안정적이다.
2. **dispatch 규칙 단순화**: 옆 동 글은 옆 동 사용자에게만. 1대N fan-out의 범위가 동의 크기로 제한된다 — group push 비용이 카카오톡 같은 거대 fan-out과는 다른 게임이다(16장 sidebar callback).
3. **거래 라이프사이클 명확**: 거래는 같은 동에서, 거래 완료 후 chat이 archive되는 흐름. 한 partition 안에서 모든 흐름이 닫힌다.

이게 13장 sharding에서 본 "도메인에 맞는 partition key 선택"의 가장 깨끗한 한국 사례다. Shopify가 shop_id를 골랐고, Slack이 workspace_id를 골랐다면, 당근은 neighborhood_id를 골랐다. 그리고 그 결정이 검색·매칭·dispatch·결제·운영 모두를 단단하게 만든다.

물론 trade-off도 있다. 동 단위 partition은 **공급 부족 동**의 함정이 있다. 신도시처럼 사용자가 적은 동에서는 search 결과가 비어 있을 수 있다. 그래서 당근은 "인접 동" 개념을 두고, 일정 거리 안의 동들을 logical group으로 묶어 검색할 수 있게 한다(추정, 검증 필요). 한 partition을 절대 안 넘는 게 아니라, "도메인이 허용하는 만큼만" 넘는다. 이게 13장 fan-out 패턴의 hyperlocal 변주다.

## hot region — 검색·매칭·지오 공통의 가장 큰 적

여기까지 네 시스템을 봤으면, 한 가지 공통의 적이 보인다. **hot region**이다.

- **쿠팡 검색**: 신상품 출시 직후 검색 query 90%가 한 카테고리에 몰림.
- **Airbnb 검색**: 휴가철 한 region의 숙소 검색이 정상 50배.
- **Uber dispatch**: 야구 경기 끝난 시점, 한 H3 cell의 ride 요청이 폭주.
- **당근**: 인기 거래 동(예: 강남)의 트래픽이 다른 동의 100배.

같은 그림이다. 13장에서 본 hot partition의 검색·매칭·지오 도메인 변주다. 모든 시스템이 평소에는 잘 돌다가, 한 region의 burst가 들어오면 시스템이 비명을 지른다.

대응 패턴 셋만 정리해두자.

1. **shard skew 모니터링**: 14장 관측성의 한 자리. 한 shard의 QPS가 평소 5배 이상이면 즉시 alert. region 단위로 트래픽 분포를 시각화한다.
2. **hot region replica 추가**: 인기 region은 read replica를 더 둔다. 신도시·강남·휴가지 같은 자리에 미리 capacity를 예치한다.
3. **rate limit by region**: 13장 rate limit과 14장 백프레셔 패턴. 한 region이 cluster 전체를 못 죽이도록 region별 token bucket을 둔다.

이 셋이 hot region을 흡수하는 일반 패턴이다. 그리고 그 위에 도메인별 미세 조정이 들어간다. 당근의 동 단위 burst는 신도시 launch 일정에 맞춰 사전 capacity를 늘린다. Uber는 콘서트·스포츠 경기 일정을 미리 알고 driver supply를 인센티브로 모은다. 도메인을 알면 burst를 예측할 수 있다 — 이게 글로벌 framework 위의 로컬 지식의 가치다.

## Sidebar: 다른 유사 시스템 한 단락 — Airbnb Categories ML

본문이 다루지 못한 검색 도메인의 또 다른 사례를 한 단락으로 봐 두자. **Airbnb의 Categories ML** 시스템이다(검증 필요).

Airbnb는 검색 결과를 단순 list로만 보여주지 않는다. "초소형 주택", "성", "트리하우스" 같은 카테고리로 묶어서 사용자가 visual하게 탐색하게 한다. 이 카테고리 분류는 ML 모델이 숙소 사진과 description을 보고 자동으로 부여한다. 모델이 새 카테고리를 발견하면 디자이너가 검토하고 출시한다.

이 시스템의 흥미로운 부분은 **사용자 query가 없는 검색**이라는 점이다. 사용자가 단어를 입력하지 않아도, 사진 한 장을 보고 "이거 마음에 들어"로 매칭이 일어난다. 검색·매칭·discovery의 경계가 흐려진 자리다. 한국에서는 무신사의 큐레이션 시스템이 비슷한 결로 운영된다. 검색이 query-driven에서 discovery-driven으로 옮겨가는 큰 흐름 중 하나다.

## Sidebar: 이 시스템의 운영 — region별 shard skew alert

검색·매칭·지오의 운영을 한 페이지 따로 보자. 14장 일반론이 이 도메인에서 어떻게 변주되는지의 사례다.

**핵심 SLI**: search query p99 (목표 200ms), dispatch matching latency p99 (목표 500ms), match success rate (목표 99%), region별 shard QPS skew (목표 평균 대비 3배 이하). 마지막이 도메인 특수 SLI다.

**Region별 alert 임계값**: 일반 시스템은 평균값으로 alert를 잡는데, 검색·매칭·지오는 그러면 안 된다. 강남 동이 정상 트래픽이 다른 동의 10배라, 평균값으로 alert를 잡으면 강남이 항상 alert가 떠 있고 다른 동의 burst는 묻힌다. **region별 historical baseline의 3배 이상**이 alert 기준이 된다. 14장의 fast/slow burn rate alerting을 region 단위로 변주한 셈이다.

**Shard skew 대응 runbook**: alert가 떴을 때 운영자가 무엇을 하는가? 4단계 runbook이 표준이다. (1) 어떤 region·shard인지 확인 → (2) 트래픽 패턴이 정상 burst(예: 콘서트, 신도시 launch)인지 비정상인지 분간 → (3) 정상이면 capacity 늘리기, 비정상이면 rate limit 강화 → (4) 30분 후 재확인. 이 runbook이 새벽 3시 alert를 5분 안에 끝낸다.

**Rollback 전략**: 검색·매칭의 ML 모델 변경은 점진적이어야 한다. canary 1% → 10% → 100%. 모델 변경이 매칭 성공률을 0.5%만 떨어뜨려도 사용자 만족도가 폭락한다. 14장의 progressive rollout이 모델 단위로 적용된다.

**Region-level chaos game day**: 분기별로 한 region의 검색 cluster를 의도적으로 끊는다. 다른 region이 어떻게 그 부하를 흡수하는지를 본다. cross-region routing과 fallback이 잘 동작하는지의 검증 자리다.

이 운영 5축이 검색·매칭·지오의 24/7 안정성을 만든다. **운영이 도메인 특수성을 담을 수 있을 때 시스템 디자인이 비로소 완성된다는 사실**을 잊지 말자.

## 이 장의 약속 회수

검색·매칭·지오 시스템 셋을 직접 설계할 일이 없는 사람도, 이 장을 다 읽으면 다음 한 페이지를 머릿속에 가지고 갈 수 있다.

- **공통 골격 4단계**: index → candidate retrieval → scoring·ranking → dispatch.
- **5개 시스템의 핵심 결정**: 쿠팡(NORI + Kafka indexing pipeline), Airbnb(IVF over HNSW), Uber(H3 + DISCO multi-objective), 당근(동 단위 partition), 배민(1대N batching).
- **공통의 적**: hot region. 13장의 hot partition이 region 단위로 변주된 그림.
- **운영 1번 신호**: region별 shard skew alert. 평균값이 아닌 region별 historical baseline.

새로운 검색·매칭·지오 시스템을 봤을 때, 이 골격 위에 그 시스템의 결정을 한 자리씩 박을 수 있게 된다. 그게 케이스 스터디의 약속이다.

기억해두자. **검색·매칭·지오 시스템 설계의 본질은 자기 도메인의 update 패턴과 burst 패턴을 정직하게 정의하는 일이다.** Airbnb가 가용성 update 빈도를 적으로 정의했기 때문에 HNSW가 아닌 IVF를 골랐다. 당근이 동 단위 라이프사이클을 정직하게 받아들였기 때문에 동을 partition key로 박았다. 도메인을 정직하게 보면 알고리즘이 알아서 선택된다.

## 다음 장으로 가는 다리

검색·매칭·지오가 "어디·무엇"의 매칭을 다뤘다면, 다음 장은 책의 클라이맥스 — **결제·금융**이다. **"한 번도 두 번 결제되지 않고, 한 번도 누락되지 않는다"**는 명제가 책 전체 약속의 가장 강한 검증이 되는 자리다. Toss·카카오뱅크·Stripe가 어떻게 1·2부의 9개 부품과 6개 패턴을 모두 한 시스템 안에 동시에 박았는지를 본다. 한국 결제의 본인인증·PG vendor lock-in·0시 트래픽·전자금융감독규정·audit chain이 모두 모인다.

가기 전에 한 번 정리하자. **검색·매칭·지오의 가장 흥미로운 자리는 글로벌 알고리즘 위에 로컬 도메인 지식이 얹히는 자리다.** H3는 글로벌 표준이지만, 그 위에 어떤 multi-objective를 얹는가는 한국 환경의 결정이다. 한국 개발자가 그 결정의 깊이에서 일할 수 있는 자리가 점점 많아지고 있다는 사실이 흥미롭다.

---

---

# 19장. 결제·금융 — Toss·카카오뱅크·Stripe

한국에서 0시 정각에 "이자 받기" 버튼을 누른다고 해보자. 같은 순간에 수십만 명이 같은 행동을 한다. 청약 9시도, 콘서트 8시도 같은 그림이다. 이 트래픽이 결제 시스템뿐 아니라 통신 3사 본인인증 API에까지 도착하면, 그 API는 10초 안에 죽는다. 그래도 우리 시스템은 살아남아야 한다. 한 번도 두 번 결제되지 않고, 한 번도 누락되지 않은 채로.

이 한 문장이 결제·금융 시스템의 가장 단단한 약속이다. **"한 번도 두 번 결제되지 않고, 한 번도 누락되지 않는다."** 분산 환경에서 이 약속을 어떻게 지키는가가 이 책의 클라이맥스다.

19장에 도착한 우리는 이미 1부의 9개 부품(RDB·NoSQL·캐시·큐·검색·LB·CDN·시간·보안)과 2부의 6개 패턴(멱등성·Saga·합의·sharding·rate limit·관측성·파이프라인+CRDT)을 모두 본 사람이다. 그 모든 학습이 한 도메인 — 결제 — 안에서 동시에 등장하는 자리가 여기다. 채팅·피드·검색·매칭이 1·2부의 일부를 회수했다면, 결제는 거의 전부를 회수한다. 그리고 그 위에 한국 환경의 5축 — 본인인증·PG vendor lock-in·0시 트래픽·전자금융감독규정 망분리·audit chain — 이 추가로 얹힌다.

이번 한 챕터를 다 읽고 나면 한 가지가 머릿속에 박힌다. **"외부 vendor failure를 가정하지 않은 코드는 production이 아니다."** 결제 시스템 설계의 1번 mental model이다. 그리고 그 mental model이 책 전체의 약속(0장)의 가장 강력한 검증이 되는 자리다.

## 결제 도메인의 4가지 약속 — idempotency·audit·SLO·compliance

결제 시스템의 도메인 요구를 한 페이지에 정리해보자. 어떤 결제 시스템이든 다음 네 가지를 동시에 지켜야 한다.

1. **Idempotency**: 같은 결제 요청이 두 번 들어와도 카드에서 두 번 차감되지 않는다. 네트워크는 실패하고 retry는 일상이라, 이 약속이 없으면 결제 시스템은 production이 안 된다.
2. **Audit trail**: 모든 결제 event는 영구적으로 추적된다. "누가 언제 얼마를 어디로 보냈는가"가 5년 뒤에도 확인 가능해야 한다. 금융감독원 감사가 들어오는 자리다.
3. **99.99% SLO**: 1년에 52분 이하의 다운타임. 카카오뱅크·토스 같은 한국 금융권의 표준 목표다. 1·2부에서 본 운영 도구가 모두 이 SLO 한 줄을 위해 작동한다.
4. **Regulatory compliance**: 전자금융감독규정·개인정보보호법·신용정보법 등의 한국 특수 규제. 망분리·암호화·secret 관리·audit 요구가 시스템 아키텍처의 형태를 결정한다.

이 네 가지가 동시에 충돌한다. Idempotency를 위해서는 strong consistency가 좋지만, 99.99% SLO를 위해서는 multi-region replication이 필요하고, 그러면 latency가 늘어난다. Audit trail은 모든 event를 영구 저장하라는데, compliance는 사용자 데이터를 일정 시점 후 삭제하라고 한다. 결제 시스템 설계는 **이 4축 trade-off 위에 한국 환경 5축을 더한 9차원 의사결정**이다.

답답해 보이지만 정직하게 마주하면 정답이 있다. 차례로 보자.

## Stripe의 idempotency key — 한 줄에 모든 것이 들어 있다

결제 도메인에서 가장 자주 인용되는 한 줄이 있다. Brandur Leach가 Stripe 블로그에 쓴 글의 첫 문장이다(W11, 자료 11).

> An idempotency key is a unique value generated by a client and sent to an API along with a request, with the server storing the key for bookkeeping the status of that request. (Stripe Engineering, Brandur Leach, 2017)

10장에서 멱등성·재시도·서킷 브레이커를 봤다. 그 패턴이 결제 도메인에서는 1번 줄이 된다. Stripe의 모든 mutation endpoint에 idempotency key가 박혀 있다. 카드 결제·환불·구독 변경 — 모두 client가 만든 unique key를 헤더에 실어 보낸다.

이게 왜 결제의 1번 줄인가? 네트워크가 실패하는 흔한 시나리오를 떠올려보자.

- 사용자가 결제 버튼을 누른다 → POST /charges 요청 발송
- 네트워크가 끊긴다 → client는 timeout
- client는 "결제가 됐는지 안 됐는지 모른다" 상태
- 만약 retry하면? 같은 카드에서 두 번 차감될 위험

Stripe의 답은 단순하다. client가 매 요청마다 unique key를 만든다(보통 UUIDv4). 같은 결제 시도라면 client는 같은 key를 다시 보낸다. server는 그 key를 저장하고 있다가, 두 번째 요청이 오면 첫 번째 응답을 그대로 돌려준다. **idempotency key가 두 번 결제의 안전망이다.**

Brandur의 글에서 한 가지 정밀한 디테일이 들어 있다. **Two-Phase Idempotency** 패턴이다(자료 11). 단순히 key + response cache가 아니다.

| 단계 | server 동작 | 목적 |
|------|------------|------|
| 1. Request lock | key를 받자마자 DB에 lock row INSERT | 같은 key 동시 요청 차단 |
| 2. Business 실행 | charge 실제 수행 | 결제 처리 |
| 3. Response cache | response를 lock row에 저장 | 다음 retry에 같은 응답 반환 |
| 4. Lock release | row를 idempotent state로 마킹 | 재처리 가능 |

왜 lock과 cache를 분리하는가? lock 없이 cache만 있으면, 같은 key의 동시 요청 두 개가 같은 시점에 들어왔을 때 둘 다 charge를 수행한다. 1장에서 본 race condition의 결제 도메인 변주다. lock이 동시성을 막고, cache가 재시도를 막는다. 두 단계가 같이 있어야 진짜 idempotent다.

이 패턴은 IETF 표준화 진행 중인 `Idempotency-Key` HTTP header로 굳어지고 있다(W11). 즉 Stripe의 한 회사 결정이 산업 표준이 돼 가는 자리다. 결제 API를 만든다면 이 헤더를 따르는 편이 낫다.

8장(시간·순서·분산 ID)에서 본 timestamp-prefix ID(Snowflake·ULID·UUIDv7)가 여기서 다시 만난다. idempotency key가 단순 random이어도 충돌은 매우 드물지만, time-ordered key를 쓰면 lock row를 자연스럽게 시간 순으로 정렬하면서 cleanup이 쉬워진다. 8장 부품이 10장 패턴 위에서 결제 도메인에 어떻게 묶이는지의 한 사례다.

## Toss 결제 시스템 — legacy를 정직하게 정리하는 길

이제 한국으로 와 보자. 토스의 결제 시스템 현대화 발표는 한국 결제 도메인의 가장 솔직한 케이스 중 하나다(W29, 자료 4.9).

> 토스페이먼츠는 hybrid cloud (Public + Private). 1% 단위 progressive rollout CI/CD platform. 토스뱅크는 코어뱅킹을 MSA로 전환 — "지금 이자 받기" 같은 대량 트래픽 ad-hoc feature가 가능해진 배경. 분산 트랜잭션은 SAGA + 2PC 혼합 적용. (토스 tech, W29)

이 한 단락에 한국 결제 시스템의 거의 모든 결정이 들어 있다. 하나씩 풀어보자.

**Hybrid cloud (Public + Private)**: 한국 핀테크의 표준 아키텍처다. 외부 노출 영역(API gateway, web frontend)은 public cloud에, 결제 코어·고객 정보는 private cloud(자체 IDC 또는 VPC isolated)에 둔다. 9장에서 본 망분리(전자금융감독규정, 한국 2)의 실제 적용이다. 이 결정 하나가 시스템 디자인 전체에 6장 LB·게이트웨이의 구성, 7장 CDN의 origin 분리, 9장 service identity의 두 영역 분리를 모두 강제한다.

**1% 단위 progressive rollout**: 14장에서 본 canary release의 결제 도메인 변주다. 새 기능을 한 번에 100% 풀지 않는다. 1% → 10% → 100%로 점진 출시한다. 결제는 실수가 한 번이라도 production에 새면 사용자에게 직접 돈 문제로 다가가는 도메인이라, blue-green이나 일반 canary보다 더 엄격한 단계가 필요하다. **Error budget burn rate를 분 단위로 모니터링하면서 다음 단계로 진행할지 멈출지를 결정한다.**

**SAGA + 2PC 혼합**: 이게 정말 흥미로운 결정이다. 11장에서 본 Saga 패턴(eventual consistency)과 12장에서 본 합의·2PC(strong consistency)를 한 시스템 안에서 동시에 쓴다. 어디에 어떤 게 쓰이는가?

- **SAGA (choreography or orchestration)**: 외부 vendor 호출이 끼는 흐름. 결제 vendor·환불·정산처럼 여러 service가 cross-system event로 묶이는 부분. compensating transaction으로 보상 가능.
- **2PC**: 단일 도메인 안의 정밀 일관성. 한 사용자의 잔액·이체·이자 같은 코어뱅킹 내부 transaction. 짧은 시간 strong consistency를 강제할 수 있는 자리.

11장에서 "Saga가 분산 트랜잭션의 현실적 길"이라고 봤지만, 12장 합의에서 본 strong consistency를 절대 양보 못 하는 자리가 따로 있다는 것이 토스의 답이다. 한 시스템 안에서 두 패턴이 공존한다. 이게 1·2부의 학습이 결제에서 어떻게 한 결정으로 묶이는지의 가장 강력한 예다.

**"지금 이자 받기"의 의미**: 단순한 UI 기능 같지만 시스템 아키텍처 관점에서는 거대하다. 사용자가 0시 정각에 버튼을 누르면 그 순간 이자가 잔액에 더해진다. 이게 가능하려면 코어뱅킹이 ad-hoc batch를 실시간으로 받을 수 있어야 한다. 메인프레임 기반 전통 코어뱅킹에서는 불가능한 그림이다. MSA로 전환하면서 이 ad-hoc 트래픽을 흡수할 수 있게 됐다. 한국 핀테크가 글로벌과 다른 차별 포인트 중 하나가 바로 이런 한국식 ad-hoc burst feature를 가능하게 만드는 architecture의 깊이다.

## 카카오뱅크 99.99% — 메인프레임에서 MSA로 가는 24/7

카카오뱅크의 결정도 비슷한 방향이지만 출발점이 다르다(W41, 자료 4.10).

카카오뱅크는 출범 자체가 mobile-first MSA였다. 다른 시중은행처럼 메인프레임 legacy를 끌어안고 시작하지 않았다. 그래서 SLO 목표를 처음부터 99.99%로 박을 수 있었다. 1년에 52분 이하의 다운타임이다.

이 숫자를 만드는 운영 도구가 무엇인지를 풀어보면 14장의 일반론이 결제 도메인에서 어떻게 변주되는지를 본다.

| 운영 도구 | 14장 일반론 | 카카오뱅크 결제 변주 |
|-----------|--------------|------------------------|
| **SLI 정의** | latency·error rate·throughput | 결제 success rate · 본인인증 success rate · 정산 정확도 |
| **Error budget** | 분기별 0.1% | 분기별 0.1% (52분) — 한 번의 incident가 거의 전체 budget |
| **Burn rate alert** | fast/slow burn | fast burn 1시간 budget 5%, slow burn 6시간 10% |
| **Blameless postmortem** | Google SRE 표준 | 한국 SK C&C 화재 이후 표준 정착, 한국 9 |
| **Chaos engineering** | game day | 정기 region 단절 + vendor 단절 시뮬레이션 |
| **배포 전략** | canary 1%→10%→100% | 1% 단계마다 30분 관찰 + fast/slow burn check |

여기서 중요한 패턴 한 가지를 짚자. **24/7 운영**이다. 시중은행은 새벽 점검 시간이 있다. 카카오뱅크는 없다. 이 결정이 시스템 디자인에 엄청난 영향을 미친다. backup, migration, schema change, cache 갱신 — 모두 점검 시간에 의존할 수 없다. **모든 운영 작업이 zero-downtime으로 설계돼야 한다.** 1장에서 본 RDS Postgres → Aurora 무중단 마이그레이션, 3장에서 본 캐시 갱신 zero-downtime 패턴, 13장에서 본 점진 sharding이 모두 24/7 환경에서 비로소 진가를 발휘한다.

그리고 카카오뱅크가 한국에서 가지는 또 다른 의미가 있다. **2022 SK C&C 판교 화재**(한국 9). 카카오 계열 전체가 multi-region 부재의 비용을 거대한 outage로 학습한 사건이다. 이후 한국 핀테크 전반의 multi-region·DR 표준이 한 단계 올라갔다. 12장에서 본 multi-region active-active의 한국 도입 흐름이 이 사건 이후로 가속됐다.

## 한국 결제의 다섯 축 — 본인인증·PG·0시·망분리·audit

이제 한국 결제만의 특수성을 5축으로 모아 정리해보자. 글로벌 결제 시스템(Stripe·PayPal)과 한국 결제 시스템이 다른 게임이 되는 자리다.

### 축 1. 통신 3사 본인인증 — vendor failover의 영원한 숙제

한국 결제는 카드사·은행에 직접 가지 않는다. 거의 모든 흐름이 **본인인증**으로 시작된다. SKT·KT·LG U+ 세 통신사 API 또는 KCB·NICE 인증기관을 거친다. 그리고 이 API들은 SLA가 약하다. 평소에는 잘 돌지만, 0시 정각·9시 청약 같은 burst 시간에는 timeout이 일상이다(한국 8).

OKKY와 핀테크 velog의 단골 토픽이다.

> 9시 0분에 모두 이체하니 인증 API가 1분간 timeout. 사용자 1만 명이 동시에 결제 실패. 어이없는 일이다. (한국 핀테크 velog 인용, 검증 필요)

이 자리의 답이 정해져 있다. **다중 vendor failover**다. KCB가 죽으면 NICE로, NICE가 죽으면 통신사 직접 호출로 흘려보낸다. 그리고 그 wrapper layer가 6장에서 본 API Gateway 패턴의 한국 결제 변주다.

```
[Client] → [API Gateway] → [Auth Wrapper Layer]
                              ├── KCB (1순위)
                              ├── NICE (2순위)
                              ├── 통신사 직접 (3순위, 비싸지만 안전)
                              └── circuit breaker for each
```

10장에서 본 timeout·circuit breaker가 여기서 1번 줄이 된다. timeout 없는 호출은 production이 아니라는 휴리스틱(4)이 결제에서는 더 단호하다. 한 vendor의 5초 timeout이 결제 service 전체를 5초 잡으면, 그 사이 다음 1만 명의 요청이 누적된다 — connection pool exhaustion(1장 sidebar)으로 cascading failure가 일어난다.

토스의 결제 system이 이 wrapper layer를 6장에서 본 service mesh 위에서 운영한다(검증 필요). mTLS로 service-to-service identity를 강제하고, mesh의 traffic split으로 failover를 점진 적용한다. 6장의 mesh 도입 4질문 framework에서 토스 결제는 모든 조건이 "예"가 되는 자리 중 하나다.

### 축 2. PG (Payment Gateway) vendor lock-in과 wrapper layer

본인인증 다음 단계가 PG 호출이다. NHN KCP·NICE·KCB·다날·토스페이먼츠가 한국 PG의 주요 벤더다. PG마다 API 형태가 다르고, error code 표준이 없고, 결제 결과 통보 방식이 제각각이다. 그래서 한국 결제 서비스의 거의 모든 회사가 **PG wrapper layer**를 자체 제작한다(한국 8).

이게 6장에서 한 단락으로 흘려넘어간 wrapper layer 패턴의 결제 도메인 deep dive다. wrapper의 책임을 풀어보면 다음과 같다.

1. **API 변환**: vendor마다 다른 request·response 형태를 internal 표준 형식으로 정규화.
2. **Error code 통합**: vendor의 error code 700개씩을 회사 내부 30개 정도의 표준 error code로 매핑.
3. **Failover 관리**: 1순위 vendor 실패 시 2순위로 자동 전환.
4. **Retry policy**: vendor마다 다른 retry 가이드라인을 통합 정책으로 적용.
5. **Idempotency 보장**: vendor에 같은 요청이 두 번 가지 않도록 wrapper 안에서 idempotency key 관리.
6. **관측성**: vendor별 latency·success rate를 14장 표준 SLI로 변환.

wrapper 하나의 책임이 한 회사의 거의 모든 결제 안정성을 결정한다. 그래서 한국 핀테크에서 "결제 wrapper 개발자"가 가장 자주 채용되는 자리 중 하나다. 6장 wrapper layer의 한 단락이 한 직무 카테고리로 펼쳐지는 그림이다.

### 축 3. 0시 동시 트래픽 — 한국 핀테크의 정시 burst

0시 0분에 이자 받기 버튼을 누른 100만 명. 9시 0분에 청약 신청 버튼을 누른 50만 명. 콘서트 8시 예매 버튼을 누른 30만 명. 한국 결제 시스템은 이 정시 burst에 살아남아야 한다(한국 1).

3장 캐시·4장 큐·13장 rate limit이 모두 이 burst 흡수를 위한 도구다. 한 줄로 변주를 정리해보자.

- **3장 캐시**: 결제 직전 사용자 정보·잔액 lookup이 burst의 90%를 차지. read-through cache + TTL stampede 방어(15장 패턴 4 callback)로 DB 부하를 줄인다.
- **4장 큐 + 백프레셔**: burst 트래픽을 일단 큐로 흡수. 사용자에게는 "결제 처리 중" UI를 1~5초 보여주고, 실제 결제는 큐에서 worker가 ordered로 처리. 14장 백프레셔 패턴의 결제 도메인 변주.
- **13장 rate limit by user**: 한 사용자가 5초에 결제 1건 이상 못 하도록 token bucket. 같은 user의 중복 click이 시스템을 죽이지 않게 한다.

그리고 토스의 1% progressive rollout이 여기서 한 번 더 의미를 가진다. **새로운 burst feature(예: "이자 받기")의 첫 출시는 1% 사용자에게만 노출한다.** 0시 정각에 100만 명이 아니라 1만 명만 들어온다. 시스템이 1만 명을 견디면 그 다음에 10%로 늘린다. 한국 핀테크의 burst feature가 그렇게 단계적으로 검증되며 확장된다.

### 축 4. 망분리 (전자금융감독규정) — 9장 보안의 결제 도메인 변주

9장에서 본 망분리가 결제 도메인에서 가장 강하게 적용된다. 전자금융감독규정은 다음을 요구한다(한국 2).

- **인터넷망과 내부망의 물리적 분리**: 결제 코어는 외부 인터넷에서 직접 접근 불가.
- **개발 환경의 분리**: 코드 작성은 인터넷 가능 PC, 코드 배포는 내부망 PC.
- **CI/CD의 분리**: 배포 파이프라인 자체가 내부망 안에 있어야 함.
- **secret 관리의 분리**: HashiCorp Vault·AWS KMS 같은 도구도 망분리 영역 안에 한정.

이 요구가 시스템 아키텍처에 미치는 영향이 거대하다. 클라우드 도입 자체가 hybrid가 된다. AWS Outposts·자체 IDC + AWS Direct Connect 조합이 흔하다. 9장에서 본 mTLS·SPIFFE/SPIRE 같은 service identity 도구가 망분리 영역 안에서 자체 PKI로 운영된다.

그리고 운영자 입장에서 가장 어려운 자리. **새벽 3시 alert가 망분리 영역 안에서 떴을 때, 외부에서는 못 본다.** 9장의 secret rotation이 망 안과 밖 양쪽에서 일관되게 일어나야 한다. 14장의 관측성 도구가 망 양쪽에 모두 깔려야 한다. 작은 결정 하나가 운영의 모든 자리에 영향을 미친다. (이 영역의 일부 운영 디테일은 회사별·발표별 변주가 있어 정확한 비교는 검증 필요.)

### 축 5. Audit chain — 5년 뒤에도 추적 가능한 결제

마지막 축이 audit chain이다. 모든 결제 event는 immutable log로 영구 저장된다. 금융감독원 감사가 들어왔을 때 "이 사용자의 2023년 3월 4일 결제가 어떻게 처리됐는가"를 한 줄씩 보여줄 수 있어야 한다.

이게 11장에서 본 **Event Sourcing**(자료 3.6)의 결제 도메인 standard implementation이다. mutation을 record로 저장하지 않고 event로 저장한다. 현재 잔액은 이벤트 stream에서 derive한다. 모든 변경의 history가 보존된다.

그리고 이 chain이 9장 보안과 만난다. audit log 자체가 변조 가능하면 audit이 의미가 없다. 그래서 audit chain은 보통 다음 세 가지를 둔다.

1. **Immutable storage**: append-only. delete 권한 자체를 운영자에게 안 준다.
2. **Cryptographic chaining**: 각 event에 이전 event의 hash를 박는다. 블록체인의 hash chain과 같은 결.
3. **Independent audit replication**: audit log를 결제 service와 다른 권한·다른 region·다른 cloud로 복제. 한쪽이 침해돼도 다른 쪽에서 진실이 보존된다.

부록에서 다룰 사고 사례 중 하나가 이 chain이 어떻게 침해를 막아주는지의 한 예다. 9장 보안이 결제 audit chain에서 가장 단단한 형태로 재등장하는 자리다.

## "한 번도 두 번 결제되지 않는다" — 한 결제 흐름의 전체 그림

여기까지 본 도구를 한 결제 흐름에 모아 그려보자. 사용자가 "결제하기" 버튼을 누른 후 응답을 받기까지의 한 줄짜리 그림이다.

```
[Client] 
  ├─ idempotency key 생성 (UUIDv7, 8장)
  ├─ HTTPS + TLS 1.3 (9장, 7장 edge termination)
  └─ POST /charges with Idempotency-Key header
      ↓
[API Gateway] (6장, hybrid cloud public 영역)
  ├─ rate limit by user (13장 token bucket)
  ├─ 인증 token 검증 (9장 OAuth2/OIDC)
  └─ ↓ private 영역으로 mTLS 전송 (9장 망분리 경계)
      ↓
[Payment Service] (1장 Postgres + Aurora replica)
  ├─ idempotency key lock (Stripe Two-Phase, 10장)
  ├─ 사용자 잔액 lookup (3장 Redis cache, stampede 방어)
  ├─ 본인인증 wrapper 호출 (Auth Wrapper Layer)
  │   ├─ KCB 1순위 (10장 timeout + circuit breaker)
  │   ├─ NICE 2순위
  │   └─ 통신사 직접 3순위
  ├─ PG wrapper 호출 (외부 vendor)
  │   ├─ NHN KCP / NICE / 토스페이먼츠
  │   └─ 결과 응답 cache (Two-Phase Idempotency)
  ├─ 잔액 차감 + 거래 기록 (12장 2PC, 단일 도메인 strong consistency)
  ├─ event 발행 (4장 Kafka, 11장 Outbox 패턴)
  └─ Saga orchestration (11장)
      ├─ 정산 service event
      ├─ 알림 service event
      └─ Audit log event (Event Sourcing + cryptographic chain)
          ↓
[Audit Layer] (별도 region, 별도 권한)
  └─ Immutable append-only storage (5년 보존)
          ↓
[Observability] (14장)
  ├─ trace propagation (모든 service에 trace_id)
  ├─ SLI: success rate · p99 latency · 본인인증 success rate
  └─ Burn rate alert (1% 단계마다 30분 관찰)
```

한 결제 요청에 1·2부의 거의 모든 부품과 패턴이 동시에 등장한다. RDB(1장)·캐시(3장)·큐(4장)·LB(6장)·CDN(7장)·시간(8장)·보안(9장)·멱등성(10장)·Saga(11장)·합의(12장)·sharding(13장)·rate limit·관측성(14장)·event sourcing(11장→15장 callback)이 모두 한 자리에 모인다.

이게 결제가 책의 클라이맥스인 이유다. 1·2부의 모든 학습이 여기서 회수된다. **임의의 분산 시스템 장애 회의에서 어디서부터 의심해야 하는가**라는 0장의 약속이 결제 시스템에서 가장 단호하게 검증된다. idempotency가 빠졌는지, timeout이 없는지, audit이 새는지, 본인인증 fallback이 작동하는지 — 다섯 자리만 5분 안에 확인하면 결제 incident의 90%는 후보가 좁혀진다.

## Sidebar: 다른 유사 시스템 한 단락 — Spanner의 글로벌 분산 결제 인프라

본문이 다루지 못한 결제 도메인의 또 다른 사례를 한 단락으로 봐 두자. **Google Spanner**의 글로벌 분산 결제 인프라(reference §4.12)다.

Spanner는 12장에서 본 TrueTime 기반 external consistency를 제공하는 글로벌 SQL이다. Stripe·Square·일부 글로벌 핀테크가 Spanner 위에 결제 인프라를 깔고 있다. 왜? **글로벌 결제는 region 간 일관성이 strong해야 한다.** 미국 user가 유럽 merchant에게 결제할 때, 두 region의 ledger가 한 결정에 합의해야 한다. eventual consistency로는 "한 번도 두 번 결제되지 않는다"의 보장이 어렵다.

Spanner의 TrueTime(GPS + 원자시계 기반 [earliest, latest] uncertainty)이 이 자리의 결정적 도구다. 8장에서 본 시간의 다양한 모델 중 TrueTime이 유일하게 글로벌 strong consistency를 제공한다. 그래서 한 글로벌 결제 회사가 "왜 Spanner를 쓰는가"의 답은 한 줄이다. **2개 region 사이의 결제도 한 transaction 안에서 끝낼 수 있기 때문이다.** 한국 핀테크 대부분은 single-region 운영이라 Spanner 이전에 다른 해법이 충분하지만, 글로벌 결제로 영역을 확장하는 회사라면 TrueTime 위에서 어떤 결정을 할지가 다음 과제다.

## Sidebar: 이 시스템의 운영 — 결제 SLO·alert·rollback

결제 시스템의 운영을 한 페이지 따로 보자. 책의 클라이맥스인 만큼 14장 일반론이 가장 정밀하게 변주되는 자리다.

**핵심 SLI**: 결제 success rate (목표 99.99%), 결제 latency p99 (목표 2초 — 본인인증 + PG round-trip 포함), 본인인증 vendor success rate (목표 vendor당 99.5%, failover 후 통합 99.95%), Audit log durability (목표 100% — 절대 누락 불가).

**SLO Error budget**: 분기별 0.1% — 결제 SLO 99.99%는 1년에 52분, 분기당 13분의 다운타임 허용. 한 번의 incident가 거의 전체 budget을 쓴다. 그래서 모든 결제 incident는 분기 budget의 burn rate로 환산된다.

**Burn rate alert (다층)**:
- **Fast burn**: 1시간 동안 분기 budget 5% 이상 소진 → 즉시 page (on-call 1차).
- **Slow burn**: 6시간 동안 분기 budget 10% 또는 24시간 30% 소진 → 다음 영업일 ticket.
- **Vendor-specific burn**: 본인인증·PG vendor별 별도 burn 추적. 한 vendor의 burn이 빠르면 자동 failover로 다른 vendor로 트래픽을 옮긴다.

**Progressive rollout (Toss 1% 패턴)**: 모든 결제 관련 변경은 1% → 10% → 50% → 100%. 각 단계마다 30분~2시간 관찰. 단계 사이에 fast burn이 발생하면 자동 rollback. 14장의 canary release가 결제 도메인에서 가장 엄격한 형태로 적용된다.

**Postmortem (blameless)**: 모든 결제 incident는 24~72시간 안에 postmortem 문서화. 사람이 아닌 시스템·프로세스를 비판한다. action item을 4주 안에 close하지 못한 incident는 escalation. 토스 SLASH 22 발표에서 정리된 한국 핀테크 postmortem 문화의 표준이다(한국 6).

**Chaos game day**: 분기별 1회 의도적 장애. 한 본인인증 vendor 단절, 한 region 단절, 한 PG vendor 응답 시간 5초로 늘림. 실제 트래픽이 흐르는 production에서 game day가 진행된다. 14장 chaos engineering의 결제 도메인 최강 적용.

이 운영 5축이 99.99% SLO 한 줄을 만든다. 그리고 그 5축이 14장의 도구를 정확히 회수한다. **운영이 도메인 압력 위에서 결정적으로 작동하는 자리** — 그게 결제다.

## Sidebar: 우리가 결제 시스템을 안 만드는 사람이라도

이 챕터를 다 읽었어도, 우리 대부분은 결제 시스템을 직접 안 만든다. 그러면 이 챕터의 학습이 우리에게 무슨 의미인가? 한 페이지에 정리해보자.

**1. "외부 vendor failure를 가정하지 않은 코드는 production이 아니다"가 결제만의 약속이 아니다.** 우리가 만드는 시스템도 외부 API에 의존한다. 결제만 vendor failover가 필요한 게 아니라, 우리 시스템의 모든 외부 호출에 같은 mental model이 필요하다. 10장의 timeout·circuit breaker가 결제에서 어떻게 1번 줄이 되는지를 본 우리는, 우리 시스템의 외부 호출에도 같은 단호함을 적용할 수 있다.

**2. Idempotency가 결제만의 패턴이 아니다.** 우리가 만드는 endpoint가 mutation이라면, 어떤 도메인이든 같은 약속이 필요할 수 있다. 이메일 발송 service에서 같은 이메일을 두 번 보내면 안 된다. 알림 service도 마찬가지. 결제가 가장 단호한 idempotency 도메인이라는 점에서 우리의 도메인이 어디까지 idempotency가 필요한지를 셈할 수 있게 된다.

**3. 한국 환경 5축이 결제만의 환경이 아니다.** 본인인증·PG·0시·망분리·audit 중 어느 하나라도 우리 도메인에 닿는다면, 결제의 답을 변주해서 가져올 수 있다. 본인인증을 쓰는 모든 서비스는 결제의 multi-vendor failover에서 답을 빌릴 수 있다. 망분리가 적용되는 모든 서비스는 토스의 hybrid cloud architecture에서 영감을 얻을 수 있다.

**4. SLO 99.99%가 결제만의 목표가 아니다.** 우리 시스템에 SLO를 처음 정할 때, 결제가 어떻게 99.99%라는 숫자를 정직하게 운영하는지를 본 우리는 너무 야심차지도 너무 낮지도 않은 목표를 정할 수 있다. 우리 도메인에 맞는 SLO는 결제보다 낮을 가능성이 크지만, 그 결정의 framework는 같다.

이게 책의 클라이맥스의 진짜 약속이다. **결제를 안 만들어도, 결제의 mental model을 알면 우리는 시스템 디자인에서 한 단계 올라간 사람이 된다.**

## 이 장의 약속 회수

0장에서 책이 약속한 6가지를 다시 떠올려보자. 결제 시스템이 이 약속을 어떻게 회수하는지 한 줄씩 정리해본다.

1. **장애 회의 첫 5분 안에 어디서부터 의심하는가** → 결제는 다섯 자리(idempotency·timeout·audit·본인인증 failover·SLO burn rate)만 보면 incident의 90% 후보가 좁혀진다. 클라이맥스에서 가장 단단한 검증.
2. **6개 부품 × 5개 질문 = 30개 trade-off 체크리스트** → 결제 흐름 한 그림에 6개 부품(RDB·캐시·큐·LB·CDN·시간) + 9장 보안 + 6개 패턴이 동시에 등장한다. 머릿속 자동 질문이 결제에서 처음 모두 펼쳐진다.
3. **모든 network 호출에 timeout·retry·circuit breaker 자동 호출** → 결제 wrapper layer가 이 휴리스틱의 가장 단호한 적용. "실패는 정상"이 코드 습관으로 박힌다.
4. **DDIA·Alex Xu 예시가 한국 사례로 매핑되는 한국어 자막** → 토스·카카오뱅크가 어떻게 글로벌 사례와 닮고 다른지의 가장 풍부한 매핑. 한국 결제의 5축이 그 자막을 명확히 만든다.
5. **on-call alert가 사람을 깨워야 하는가** → 결제 burn rate alert의 fast/slow 분리가 이 메타 시선의 모범 사례. pager fatigue를 줄이는 운영 문화의 한국 도입이 여기서 가장 명확히 드러난다.
6. **새 endpoint 설계 시 자동으로 묻는 5가지 보안 질문** → 결제 audit chain + 망분리 + secret rotation이 9장의 control plane을 가장 단호하게 적용한 자리. 한국 망분리·전금감규 환경의 mental model이 여기서 완성된다.

여섯 약속이 한 도메인에서 동시에 회수된다. 이게 결제가 책의 클라이맥스인 가장 정확한 이유다.

기억해두자. **결제 시스템 설계의 본질은 "외부는 모두 실패한다"와 "내부는 모두 정직하다"를 동시에 받아들이는 일이다.** vendor·network·hardware는 실패한다고 가정한다. 그러나 우리 audit·idempotency key·event log는 진실이다. 이 두 명제 위에서 분산 결제 시스템이 비로소 가능해진다.

## 다음 장으로 가는 다리

결제·금융이 책의 클라이맥스였다면, 다음 장은 **이커머스·재고**의 차분한 회수다. 결제만큼 극단적이지는 않지만 1·2부의 모든 빌딩 블록이 다시 한 번 다른 조합으로 등장한다. 쿠팡 로켓배송의 자정 cutoff, Shopify Pods의 modular monolith, 재고 1개를 누구에게 줄 것인가의 reserve→confirm→settle 3단계 패턴을 살펴보자.

가기 전에 한 번 정리하자. **결제는 시스템 디자인의 모든 어려움이 한 자리에 모이는 영역이라는 첫 줄을 우리는 한 챕터를 통해 직접 확인했다.** 그리고 그 어려움을 정직하게 마주한 회사들이 — Toss·카카오뱅크·Stripe — 한국과 글로벌에서 어떻게 그 약속을 지키는지를 본 우리는, 어떤 시스템을 봐도 "이건 결제의 어느 자리와 비슷하군"이라는 mental mapping을 가지고 가게 된다.

20장의 이커머스가 책 전체 약속의 마지막 회수가 되고, 부록의 현장 노트가 "production은 결국 사람의 영역"이라는 동료적 마무리로 닫는다. 우리는 그 마지막 두 자리를 향해 함께 가고 있다.

---

---

# 20장. 이커머스·재고·정합성 — Shopify·쿠팡·Amazon

쿠팡 로켓배송의 자정 cutoff는 절대 어길 수 없다고 해보자. 자정 1초 전에 들어온 주문은 오늘 새벽에 출발하는 트럭에 실려야 한다. 그 1초 사이에 재고 확인·결제 승인·배차 결정·창고 배정이 모두 정확하게 일관되어야 한다. 자정 0시 1초에 들어온 같은 주문은 — 같은 사용자가 같은 상품을 같은 가격에 클릭했어도 — 내일 새벽 트럭에 실린다. 단 2초 차이가 사용자 경험을 완전히 다른 모양으로 만든다.

이 1초의 결정이 이커머스 시스템의 정직한 단면이다. 속도(2초 안에 모든 결정)와 정합성(재고 1개의 마지막 한 명을 누구에게 줄 것인가)을 동시에 잡아야 한다. **속도는 단축할수록 정합성이 흔들리고, 정합성은 강할수록 속도가 무너진다.** 이 trade-off의 가장 잔인한 자리들이 한국 이커머스에 모여 있다 — 그 잔인함을 한 번 들여다보면, 1·2부에서 익힌 부품·패턴들이 한꺼번에 다시 등장하는 광경을 볼 수 있다.

여기서는 Shopify의 majestic monolith + pods 모델, 쿠팡 로켓배송의 자정 cutoff, Amazon의 Dynamo 원전 도메인을 짚으면서 — **reserve → confirm → settle** 3단계 일관성 패턴으로 이커머스의 정직한 결정 모양을 그려 보자. 19장 결제가 한 번도 두 번 결제되지 않는 자리였다면, 20장은 한 번도 두 번 팔리지 않는 자리다.

## 1. Shopify Pods — Majestic Monolith의 정직한 답

Ruby on Rails 진영에서 일했던 사람이라면 "majestic monolith"라는 단어를 들어본 적이 있을 것이다. Shopify가 자기 시스템을 부르는 이름이다(W27). 모든 마이크로서비스 트렌드와 반대 방향 — **하나의 거대한 Ruby on Rails monolith**가 Shopify의 핵심이다.

이 결정의 정직한 배경은 무엇일까? Shopify의 사용자는 거대 enterprise가 아니라 **수백만 개의 작은 쇼핑몰**이다. 각 shop이 자기 데이터·자기 트래픽 패턴을 가진다. 그리고 shop 단위로는 트래픽이 작다. 이 워크로드에 마이크로서비스를 깔면 — 서비스 간 통신 latency + 분산 트랜잭션 비용 + 운영 부담이 비즈니스 가치를 압도한다. monolith가 단순하고 빠르고 정확하다.

### Packwerk — Monolith 안의 module boundary

다만 monolith가 진짜로 한 덩어리라면 — 코드베이스가 무너진다. Shopify의 답은 **Packwerk**라는 자체 도구다. 같은 Ruby application 안에서 module boundary를 정의하고, "이 module은 저 module의 internal API에 접근할 수 없다"는 컴파일 타임 enforcement를 건다. **모듈러 모놀리스**가 그 이름이다.

이게 마이크로서비스와 무엇이 다른가? 핵심 차이는 — **마이크로서비스는 process boundary로 분리, 모듈러 모놀리스는 코드 boundary로만 분리**. 모듈러 모놀리스는 같은 process·같은 DB·같은 transaction을 공유한다. **분산 시스템의 비용 없이 코드 boundary의 가치를 얻는 길**이다. 5명짜리 팀이 Istio·Kafka·k8s 위에 mesh를 깔지 않고도 코드를 정리할 수 있다 — 0장의 도입 자격 5문항이 정확히 이 자리에서 작동한다.

### MySQL podding by shop_id

Shopify의 규모가 커지면서 — 한 monolith·한 DB로는 모든 shop을 담을 수 없다. 답은 **podding by shop_id**다. 13장 샤딩의 directory-based sharding 패턴 그대로다.

각 shop은 자기 pod에 묶인다. pod 하나에 수만 개 shop이 들어가고, pod마다 독립된 MySQL primary + replica + Redis + worker가 있다. shop A의 주문은 pod 1에서만 처리되고, shop B의 주문은 pod 2에서만. **shop 단위 데이터 격리 + pod 단위 인프라 분리**가 이 모델의 핵심이다.

장점이 분명하다. ① **pod 하나의 사고가 다른 pod에 안 전파된다.** 한 인기 shop의 트래픽 폭증이 다른 shop을 무너뜨리지 않는다. ② **pod 단위 deploy·rollback이 가능하다.** canary가 자연스럽다 (14장 callback). ③ **MySQL의 단일 leader 한계 안에서 글로벌 확장 가능**. 13장의 5가지 sharding 안티패턴을 피하면서 직관적 분할 기준(shop_id)을 택한 결과.

### BFCM 대응 — Load Shedding과 Queue Throttling

Shopify의 1년 중 가장 큰 사건은 **Black Friday Cyber Monday (BFCM)**다. 11월 마지막 주 + 12월 첫 주 — 평상시 대비 10~30배 트래픽이 한 번에 몰린다(검증 필요, Shopify Engineering 블로그 다년간 발표).

이 spike 앞에서 Shopify가 쓰는 도구 두 가지가 인상적이다.

**1. Load shedding.** 시스템이 한계에 가까워지면 **일부 요청을 의도적으로 거부**한다. 단순 rate limit이 아니라 — "지금 5xx 응답률이 임계 넘었다 → 가장 덜 critical한 요청부터 거부 시작" 같은 dynamic logic. 14장 SLO·burn rate 도구의 본격 적용이다.

**2. Queue-based throttling.** 결제 요청을 직접 받지 않고 **큐로 받는다**. 큐에서 일정 속도로 dequeue해 처리한다. 사용자는 "잠시만 기다려 주세요"라는 페이지를 본다. 끔찍해 보이지만 — 시스템이 무너지는 것보다 1분 기다리는 게 훨씬 낫다. 사용자도 그 사실을 안다.

이 두 도구가 BFCM 운영의 핵심이다. **시스템에 한계를 정직하게 표현하는 일이 사용자 신뢰의 토대다** — 14장의 SLO·rate limit 일반론이 BFCM이라는 도메인에서 정확히 적용되는 사례다.

## 2. 쿠팡 로켓배송 — 자정 cutoff와 한국 5

한국 백엔드 시각에서 가장 잔인한 이커머스 사례가 쿠팡 로켓배송이다(community 한국 5). Shopify가 "각 shop 단위로 격리"를 답했다면, 쿠팡은 정반대 — **전국 단일 시스템에서 자정 cutoff를 절대 어기지 않는 것**이 핵심이다.

### 자정 cutoff의 의미

쿠팡 로켓배송의 약속은 단순하다. "오늘 자정 전에 주문하면 내일 새벽에 받는다." 이 약속을 지키려면 — 자정 시점까지 **재고·결제·배차·창고 배정**이 모두 결정돼야 한다. 자정 0시 1초의 주문은 다음 날로 밀린다.

이 cutoff의 잔인함은 — **trade-off의 양 끝을 동시에 잡아야 한다**는 점이다.

- **속도** — 1초 안에 재고 확인 + 결제 승인 + 창고 배정 + 트럭 배차 결정.
- **정합성** — 재고 1개의 마지막 한 명을 누구에게 줄지 한 번도 두 번 팔리지 않도록.

이 두 가지가 정면충돌할 때 — 보통 시스템은 "지연되더라도 정확하게" 또는 "빠르게라도 가끔 어긋나게"를 고른다. 쿠팡은 둘 다 양보할 수 없는 입장이다.

### Reserve → Confirm → Settle 3단계 패턴

이 trade-off를 풀어내는 표준 패턴이 **reserve → confirm → settle** 3단계 일관성이다. 책 전체 부품·패턴이 한 자리에 모이는 도구다.

```
1. Reserve (수십 ms)
   - 재고 in-memory reservation
   - "이 사용자가 N초 동안 이 상품 1개를 잡아 둠"
   - 정합성: 같은 상품을 동시에 다른 사용자가 reserve 못함

2. Confirm (수백 ms)
   - 결제 승인 (19장 결제 시스템 호출)
   - 결제 성공 시 reservation을 confirm으로 전환
   - idempotency key 필수 (10장 callback)

3. Settle (분~시간)
   - 창고에 출고 지시
   - 배차 결정
   - eventual reconciliation으로 모든 layer에 전파
```

각 단계의 trade-off가 다르다.

- **Reserve 단계**는 strong consistency가 필요하다. 같은 상품 1개에 동시 reserve 두 번은 안 된다. **distributed lock (Redis Redlock with fencing) 또는 RDB row-level lock**이 답이다 (8장 분산 lock callback).
- **Confirm 단계**는 idempotency가 핵심. retry해도 결제는 한 번만, reservation 전환도 한 번만 (10장·19장 callback).
- **Settle 단계**는 eventual consistency 허용. 창고 시스템·배차 시스템·웹 UI가 결국 같은 상태에 도달하면 된다 (12장 일관성 회수).

이 3단계가 분명히 분리돼 있어야 — 자정 cutoff 안에 모든 결정이 끝난다. 단계 하나라도 섞이면 — 예컨대 confirm 단계에서 strong consistency를 강제하면 — 한 트랜잭션이 수초 걸리고 cutoff를 어긴다.

### 이 시스템의 운영 — 자정 cutoff 알림

쿠팡 로켓배송의 운영에서 가장 무거운 자리는 자정 자체의 트래픽이다. 22:00 ~ 24:00 사이에 트래픽이 평상시의 5~10배가 된다. 그리고 **자정 직전 1~5분**이 가장 잔인하다 — 사용자들이 "마지막 1분"을 노리고 클릭한다.

이 패턴에 대응하는 운영 도구들:

- **자정 cutoff burn rate alert** — error budget이 23시 50분 시점에 정상 비율을 넘으면 즉시 page. 자정 후 fix는 너무 늦다.
- **Pre-warm**: 22시쯤부터 reservation system·결제 시스템·창고 시스템의 instance를 N배 늘려 둔다. 17장 카카오톡 새해 인사 pre-warm 패턴과 같은 결.
- **Load shedding ladder**: 23:55 ~ 24:00 사이에 "재고 확인 요청만 받음, 결제 비핵심 endpoint는 거부" 같은 dynamic load shedding이 발동된다.
- **Postmortem 매주**: 매주 자정 시점의 SLO 위반·user impact·시스템 hot spot을 회고. blameless 문화로 사람을 비판하지 않고 시스템·프로세스를 점검 (14장 callback).

자정이라는 한 시점이 — 14장 운영 5도구(SLO·observability·배포·chaos·on-call)가 모두 모이는 운영의 가장 단단한 자리가 되는 셈이다.

## 3. Amazon — Dynamo 원전 도메인

이커머스 시스템의 또 다른 거대 사례는 Amazon이다. 그런데 Amazon은 다른 두 회사와 결을 달리한다. **Amazon의 핵심은 Dynamo가 태어난 그 자리**다 (2장 NoSQL callback).

2007년 SOSP에 발표된 Dynamo 논문(P7)이 풀려고 한 문제는 단순했다 — **"BlackFriday에 한 사용자의 장바구니에 물건을 담을 때, 절대로 'item could not be added'라는 에러가 보이면 안 된다."** Amazon은 매년 BFCM에 단 1초의 장바구니 다운타임도 허용하지 않으려 했고, 그래서 **eventual consistency + always-writable**라는 결정을 정면으로 골랐다.

그 결과가 — 같은 물건을 두 번 담을 수 있는 conflict가 가끔 발생한다는 점이다. Dynamo는 두 버전을 모두 저장하고, **장바구니 도메인의 의미로 conflict를 해소한다** — "두 버전을 union하면 된다, 사용자가 의도한 건 두 물건 모두 담는 것이다." application-level conflict resolution이 이 결정의 비결이다.

이 패턴이 modern 이커머스의 한 한 자리를 차지한다. **장바구니는 eventual consistency가 default**, 결제는 strong consistency, 재고는 reserve-confirm-settle 3단계. 모든 도메인에 같은 일관성을 강제하지 않는 게 운영 비용을 결정한다 — 12장 카카오뱅크 패턴 회수다.

### 사이드 박스 — 다른 유사 시스템 1단락: Stripe Sigma·Amazon Aurora

본 챕터가 다루지 못한 한 자리를 짚어 두자. **Amazon Aurora**(P14)는 Amazon이 자기 운영 부담을 풀려고 만든 modern RDBMS다. "log is the database"라는 한 줄로 1장 RDB 챕터에서 다뤘는데, 이커머스 시각에서는 — **상품·주문 데이터의 글로벌 region 확장**을 가능하게 한 도구다. Aurora Global Database가 cross-region replication을 자동으로 한다. 그리고 **Stripe Sigma**는 모든 거래 데이터를 SQL로 쿼리할 수 있게 하는 자체 서비스 — 19장 결제의 한 사례지만, 이커머스 회사가 결제 데이터를 직접 분석하는 시각으로 보면 한 단계 더 강력하다. 두 도구 모두 "이커머스의 거대 SQL 데이터를 어떻게 다루는가"라는 같은 문제의 다른 답들이다.

## 4. 재고 일관성 — Reserve의 잔인함

이커머스 시스템에서 가장 자주 데이는 자리가 **재고 일관성**이다. "재고 1개의 마지막 한 명을 누구에게 줄 것인가." 이 한 줄을 풀어내는 답은 도메인마다 다르다.

### Distributed Lock

가장 직설적인 답이다. 재고 차감 시 distributed lock을 잡는다.

```
1. Redis에 SETNX inventory_lock:sku_123 with TTL
2. 잠금 성공 → DB에서 inventory_count >= 1 확인 → 차감
3. lock 해제
```

문제는 8장에서 짚은 Redlock의 NTP 함정 + lock 자체의 SPOF다. **fencing token + ZooKeeper/etcd 기반 합의가 안전한 default**다 (12장 합의 callback). 단 모든 재고 차감에 합의 호출이 들어가면 — 자정 cutoff 안에 끝나기 어렵다. trade-off가 정직하게 트인다.

### In-Memory Reservation

대안 — 재고를 Redis 또는 application memory에 두고, atomic decrement를 쓴다.

```
1. Redis DECR inventory:sku_123
2. 결과 >= 0이면 reserve 성공, < 0이면 거부 (atomic)
3. 비동기로 DB에 reflect
```

이게 쿠팡·11번가 같은 대형 한국 이커머스가 자주 쓰는 패턴이다. 속도는 빠르지만 — **Redis 장애 시 재고 손실**이 핵심 함정이다. 1차 방어는 Redis cluster + persistence, 2차 방어는 DB 기반 reconciliation job(예: 5분마다 Redis·DB 일관성 점검).

### Eventual Reconciliation

가장 느슨한 답 — reserve 시점에 정확한 확인 없이 일단 받고, 사후에 reconciliation으로 정리. **재고가 충분한 경우 99%** 작동하지만, **재고 1개에 100명이 동시 클릭하는 1%의 자리**가 문제다. "주문은 받았는데 발송이 안 되네요" 같은 사용자 불만이 그 1%의 자리에서 흘러나온다.

세 답의 비교 표.

| 축 | Distributed Lock | In-memory Reservation | Eventual Reconciliation |
|---|---|---|---|
| 일관성 | 매우 강 | 강 | 약 |
| 속도 | 느림 | 매우 빠름 | 매우 빠름 |
| Redis 의존 | 부분 | 매우 큼 | 없음 |
| 어울리는 곳 | 한정판·금융 | 일반 대형 이커머스 | 재고 풍부 |

회의 자리의 정답은 보통 **In-memory Reservation + DB reconciliation hybrid**다. 정확한 합의가 필요한 critical 상품(한정판)만 distributed lock으로, 일반 상품은 in-memory로. 그리고 사후 reconciliation이 정기적으로 일관성을 보강한다. 이게 쿠팡·11번가의 평균 모델일 가능성이 높다 (검증 필요).

## 5. 카트·체크아웃의 멱등성

이커머스의 또 한 자리에 **카트·체크아웃의 멱등성**이 있다. 사용자가 "주문하기" 버튼을 두 번 클릭하면 — 한 번만 주문돼야 한다. 결제 retry도 마찬가지. 10장의 idempotency key 패턴이 정확히 이 자리에서 작동한다.

표준 흐름은 단순하다.

```
1. 카트 → "주문 시작" 버튼 클릭
   → server가 idempotency_key 생성 (UUID v7 권장, 8장 callback)
   → client에 전달
2. client → "결제 요청" with idempotency_key
   → server: 같은 key의 이전 요청 있으면 그 결과 반환, 없으면 새로 처리
3. 결제 완료 → order 생성 → reservation을 confirmed로 전환
```

이 흐름이 "user가 주문 버튼 두 번 클릭"·"네트워크 timeout 후 retry"·"브라우저 새로고침" 같은 모든 unhappy path를 같은 결과로 수렴시킨다. **idempotency key는 카트·체크아웃의 1번 줄**이다.

### 우아한형제들 배민 주문 처리 — 한국 6

한국 백엔드의 또 다른 흥미로운 이커머스 사례가 우아한형제들 배민이다(community 한국 6). 배민은 쿠팡·11번가와 다른 도메인 — **음식점에 주문을 전달하는 시스템**이라 정합성의 결이 다르다.

배민의 핵심 약속은 **"같은 주문이 음식점에 두 번 들어가지 않는다"**다. 이게 깨지면 음식점이 같은 음식을 두 번 만들어 환불 발생, 신뢰 무너짐. 우아한형제들 발표에서 자주 짚히는 패턴은 — **주문을 받는 layer + 음식점에 전달하는 layer의 명시적 분리**다. 사용자 클릭이 바로 음식점에 가는 게 아니라, 중간 reliable layer가 idempotency·retry·timeout을 책임진다. 11장 Saga + Transactional Outbox 패턴이 이 자리에서 정확히 작동한다.

그리고 또 한 가지 — **음식점 영업시간 cutoff**가 쿠팡 자정 cutoff와 비슷한 결의 운영 함정이다. 영업 종료 30분 전에 들어온 주문은 처리·취소·환불 흐름이 까다롭다. 14장의 SLO + alert이 배민에서는 영업시간 단위로 작동한다.

## 6. BFCM·자정 cutoff — Spike 대응의 한 묶음

Shopify의 BFCM과 쿠팡의 자정 cutoff는 — 시간축이 다르지만 본질은 같다. **예측 가능한 거대 spike에 어떻게 대응할 것인가**.

표준 도구 5가지를 정리해 두자.

1. **Pre-warm.** 예측 가능한 spike라면 사전에 instance를 N배 늘려 둔다. cold start 비용을 spike 시점에 부담하지 않는다.
2. **Load shedding ladder.** spike 시점에 점진적으로 덜 critical한 endpoint를 거부한다. 5xx보다 429가 사용자 신뢰에 덜 해롭다.
3. **Queue-based throttling.** 즉시 처리하지 않고 큐로 받는다. "1분 기다려 주세요"가 무너지는 것보다 낫다.
4. **Pre-computed timeline / inventory.** spike 직전에 hot path 데이터를 미리 캐시·warm. 17장 카카오톡 새해 인사 pre-warm 패턴.
5. **Chaos drill before spike.** spike 시점 1주 전에 평소에 일부러 fail-over·throttle을 일으켜 본다. 14장 chaos engineering의 BFCM 도메인 적용.

이 5가지가 머리에 자동으로 펼쳐지면 — 한국·미국·일본 어디서든 거대 spike 도메인 시스템 운영의 1차 도구를 손에 쥔 셈이다.

## 7. 의사결정 트리 — 우리 이커머스 시스템은 어디서 멈출 것인가

새 이커머스 시스템을 설계하거나 기존 시스템을 손볼 때 자기에게 던질 다섯 질문이다.

1. **monolith·모듈러·MSA 중 무엇인가?** 5명 팀이면 monolith로 시작. shop 수가 폭증하면 모듈러 monolith (Shopify Packwerk 패턴). 도메인이 진짜 분리되면 MSA. 13장 샤딩의 directory-based pattern (shop_id) 우선 검토.
2. **재고 일관성은 어느 수준인가?** 한정판·금융 → distributed lock + fencing. 일반 대형 이커머스 → in-memory reservation + DB reconciliation hybrid. 재고 풍부 → eventual reconciliation.
3. **카트·체크아웃 멱등성은 박혀 있는가?** idempotency_key는 시작점. 결제 retry·사용자 더블 클릭·브라우저 새로고침 모두 같은 결과로 수렴해야 한다 (10장·19장 callback).
4. **거대 spike(BFCM·자정 cutoff)에 대응하는 5가지 도구가 박혀 있는가?** pre-warm·load shedding·queue throttling·pre-computed·chaos drill 5가지. 한 가지라도 빠지면 spike 시점에 시스템이 무너진다.
5. **재고·주문·결제·창고 layer가 reserve → confirm → settle 3단계로 명시 분리돼 있는가?** 한 layer가 다른 layer의 일관성을 가정하면 — cascading failure의 시작점이 된다.

이 다섯 질문이 머릿속에 자동으로 펼쳐지면, 회의 자리에서 이커머스 시스템 결정을 첫 5분 안에 풀어낼 수 있다.

## 8. 책의 약속 회수 — 6가지 약속이 손에 잡혔는가

0장에서 우리는 6가지 약속을 박았다. 이커머스 챕터를 마치면서 — 그 약속들이 얼마나 손에 잡혔는지 한 번 되돌아보자.

1. **장애 회의에서 첫 5분 안에 어디서부터 의심할까.** 이커머스 도메인에서는 — 재고가 어긋나면 reserve layer를, 결제가 두 번 되면 idempotency key를, 자정 cutoff를 못 지키면 spike 대응 5도구를. 도메인 언어가 손에 잡혀 있어야 5분 안에 답이 나온다.
2. **부품 도입 trade-off 체크리스트.** 6개 부품 × 5문항 = 30문항이 의사결정 트리에서 일관되게 등장했다. RDB의 pod 분할(13장), in-memory reservation의 Redis 의존(3장), idempotency key의 멱등성(10장), 결제 vendor failover의 saga(11장).
3. **모든 network 호출에 멱등성·timeout·circuit breaker.** 카트·체크아웃·결제·창고·배차 모든 layer가 이 한 묶음 위에서 작동한다. "실패는 정상"이라는 인지가 이커머스의 1번 줄이다.
4. **외국·한국 사례 한국어 자막.** Shopify pods ↔ 쿠팡 pod 단위 격리, BFCM ↔ 자정 cutoff, Amazon Dynamo ↔ 한국 이커머스 in-memory reservation. 두 결정이 어떻게 닮고 어떻게 다른지가 보이는 게 5번째 자막이다.
5. **on-call alert의 메타 시선.** 자정 cutoff burn rate alert·spike pre-warm·load shedding ladder 모두 14장 운영 도구의 이커머스 도메인 적용. 알람을 줄이고 runbook을 만들고 postmortem을 blameless하게 쓰는 사람이 되는 길에 한 발 더 다가갔다.
6. **모든 endpoint에 인증·인가·secret·rotation·audit log.** 9장 보안의 control plane이 이커머스에서는 — 사용자 결제 정보·shop 결제 정보·창고 운영 API·배차 API 모두에 깔린다. 한국 망분리·전자금융감독규정과 닿는다.

여섯 약속이 다 풀어졌으면 — 이 책의 한 번 통독이 끝난 셈이다. 다 안 풀어졌어도 괜찮다. 책장에 두고 다음에 필요할 때 한 챕터씩 다시 펴 보면 된다. 동료의 어깨를 두드리며 "한 번 같이 들여다보자"는 톤은 그대로 우리 옆에 있다.

## 9. 손에 남기고 가야 할 것들

여기까지 따라온 우리에게는 이미 이커머스·재고·정합성의 지형이 손에 잡혀 있다. 한 줄씩 다시 꺼내 보자.

- **Shopify Pods + Majestic Monolith.** 모듈러 monolith로 분산 시스템 비용 없이 코드 boundary의 가치. 13장 directory-based sharding의 한 사례.
- **BFCM 대응 5도구** — pre-warm·load shedding·queue throttling·pre-computed·chaos drill. 거대 spike 운영의 표준.
- **쿠팡 자정 cutoff** — 속도와 정합성 양 끝을 동시에 잡는 자리. reserve → confirm → settle 3단계 분리가 답.
- **Amazon Dynamo 원전 도메인** — 장바구니 always-writable + application-level conflict resolution. 모든 도메인에 같은 일관성을 강제하지 않는 게 운영 비용을 결정한다 (12장 카카오뱅크 회수).
- **재고 일관성 3답** — distributed lock·in-memory reservation·eventual reconciliation. 일반 대형 이커머스의 default는 hybrid.
- **카트·체크아웃 멱등성** — idempotency_key가 1번 줄. 10장의 패턴이 이커머스에서 가장 직접적으로 작동.
- **우아한형제들 배민** — 음식점 영업시간 cutoff + 주문 layer 분리 + 11장 Saga·Outbox 패턴.
- **이커머스의 한 줄 통찰** — 한 번도 두 번 팔리지 않게, 그리고 자정 cutoff를 어기지 않게. 그게 새벽 3시의 자신을 살린다.

여기까지가 3부 케이스 스터디의 마지막 챕터다. 0장에서 약속했던 책 전체의 그림 — 빌딩 블록 → 패턴 → 케이스 → 운영의 4축 지형도 — 가 손에 잡혔길 바란다. **production은 결국 사람의 영역이다**. 부록 A에서는 그 사람의 영역을 정직하게 들여다본다. 책으로는 안 배우는, 코드로만 만나는 18가지 함정. 동료적 마무리로 책을 닫는 자리다.


---

# 부록 A. 현장 노트 — 책에 안 나오는 일들

어떤 베테랑 SRE는 후배에게 이렇게 말한다. "이 18가지를 한 번씩 만나보면, 너도 5년차다." 책으로는 안 배우는, 코드로만 만나는 함정들이 있다. 우리는 그것들을 책의 끝으로 모아 둔다.

19장 결제 클라이맥스가 책 전체의 부품·패턴이 한 시스템에 어떻게 모이는지의 회수였다면, 부록은 다른 종류의 회수다. **production은 결국 사람의 영역이다.** 책으로는 절대 다 배울 수 없는 함정 18가지, 한국 환경의 야사 몇 토막, on-call의 휴머니즘, 이력서용 기술 도입의 함정, 그리고 한 페이지 분량의 AI/LLM 시대 약속 — 이 짧은 부록이 책 전체의 동료적 마무리다.

새벽 3시 alert가 울렸을 때 옆자리에 펴두는 reference로 이 부록이 작동하기를 바란다. 책장에 꽂아두고, 장애 회의에서 꺼내 보고, 후배에게 한 페이지씩 짚어주는 종류의 자리로.

## Tribal Knowledge 18선 — production에 늘 있는 것

각 함정은 다음 네 줄로 정리한다. **증상 → 원인 → 즉시 mitigation → 근본 fix.** 짧은 카드 형식이지만 한 번씩은 다 만나본 것들이다.

### 1. NTP slew vs step — 시간이 한 번에 점프하면

- **증상**: cron job이 두 번 실행되거나 한 번 빠진다. Snowflake ID에 중복이 생긴다. 8장에서 본 분산 ID 시스템이 시간 점프에 취약하다.
- **원인**: NTP가 시간 차이를 "step"으로 한 번에 점프하면 OS 입장에서 시간이 거꾸로 가거나 뛴다. cron·timer·log timestamp가 같이 흔들린다.
- **즉시 mitigation**: 의심되면 `timedatectl status` + `chronyc tracking`으로 마지막 동기화 형태 확인. 운영 중인 ID generator의 sequence를 추적해 중복 가능성 검사.
- **근본 fix**: chrony 또는 ntpd를 slew 모드로 강제(`makestep 0 -1`). 점프가 일어나지 않게 천천히 조정. 분산 ID 라이브러리에는 NTP slew 권장 가이드가 있다(8장 callback).

### 2. Linux file descriptor limit (ulimit -n) — 기본 1024는 부족하다

- **증상**: NGINX·Redis·MySQL이 갑자기 새 connection을 못 받는다. "Too many open files" 에러가 로그에 박힌다.
- **원인**: Linux 기본 ulimit -n이 1024다. production에서 1만 이상 connection을 받는 service가 이 한계에 부딪힌다.
- **즉시 mitigation**: `ulimit -n 65536` 또는 `prlimit --pid PID --nofile=65536:65536`로 임시 상향.
- **근본 fix**: systemd unit 파일이나 `/etc/security/limits.conf`에 LimitNOFILE 박기. container라면 docker-compose·k8s pod 설정에. 신규 service 띄울 때 체크리스트의 1번 줄.

### 3. TCP TIME_WAIT 누적 — short-lived connection의 함정

- **증상**: 트래픽은 평소대로인데 새 connection이 안 만들어진다. `netstat | grep TIME_WAIT | wc -l`이 수만을 넘는다.
- **원인**: short-lived connection이 많은 service(예: API gateway, batch worker)에서 close 후 TIME_WAIT 상태 socket이 60초간 남는다. 포트가 빠르게 소진된다.
- **즉시 mitigation**: `SO_REUSEPORT` 활성화 + `net.ipv4.tcp_tw_reuse=1` 임시 적용.
- **근본 fix**: connection pool 도입(1장 callback). short-lived connection을 long-lived pooled connection으로 바꿔서 TIME_WAIT 발생 자체를 줄인다.

### 4. DNS TTL이 cache layer로 작동 — service discovery 변경했는데 트래픽이 30분 안 와

- **증상**: 새 backend pod을 띄우고 ELB·NLB에 등록했는데, 일부 client가 30분간 옛 IP로 트래픽을 보낸다. AWS도 같은 문제 있음.
- **원인**: DNS resolver의 TTL caching이 application 위에서 invisible layer로 작동한다. JVM의 `networkaddress.cache.ttl`이 가장 흔한 함정.
- **즉시 mitigation**: JVM이면 `-Dnetworkaddress.cache.ttl=10`로 짧게. 운영 중인 service라면 강제 재시작이 가장 빠른 길.
- **근본 fix**: client-side service discovery(Eureka·Consul) 또는 service mesh의 endpoint resolver를 쓴다(6장 callback). DNS를 service discovery 도구로 쓰지 않는 편이 낫다.

### 5. Kafka consumer rebalance storm — lag이 갑자기 폭발

- **증상**: consumer 하나가 죽거나 추가됐는데, group 전체가 rebalance에 들어가서 5분간 메시지 처리가 멈춘다. lag이 10M으로 점프한다.
- **원인**: Kafka 2.3 이전의 stop-the-world rebalance. partition 재할당이 끝날 때까지 모든 consumer가 동결.
- **즉시 mitigation**: `session.timeout.ms`와 `max.poll.interval.ms`를 조정해 false rebalance 줄이기. consumer 추가·제거는 한 번에 하나씩.
- **근본 fix**: Kafka 2.4+ + Cooperative Sticky Assignor 도입. incremental rebalancing으로 일부 partition만 이동하니 storm이 사라진다(4장 callback).

### 6. JVM safepoint pause — jstack 한 번이 SLO를 깬다

- **증상**: 평소 p99 50ms이던 service가 갑자기 p99 5초가 됐다. JVM thread dump를 운영자가 막 찍은 직후.
- **원인**: `jstack` 호출은 JVM safepoint를 trigger한다. 모든 application thread가 멈출 때까지 GC stop-the-world와 비슷한 pause가 생긴다.
- **즉시 mitigation**: production에서는 `jstack -F`(강제) 쓰지 않기. 정 필요하면 carbon copy(replica)에서 찍기.
- **근본 fix**: async profiler·JFR(Java Flight Recorder) 같은 sampling 도구 사용. safepoint 없이 stack trace를 모은다.

### 7. Bloom filter false positive로 read amplification 폭증

- **증상**: Cassandra·HBase에서 평소 read latency 5ms인데 가끔 50ms로 튄다. CPU 사용량이 같이 폭증.
- **원인**: Bloom filter false positive 비율이 일정하게 발생. partition이 거대해지면 false positive로 인한 disk read가 곱해진다.
- **즉시 mitigation**: 해당 sstable의 bloom filter 통계 확인(`nodetool cfstats`). false positive rate 조정.
- **근본 fix**: `bloom_filter_fp_chance`를 default 0.01에서 0.001로 낮춤(메모리 비용 증가). 또는 partition을 더 잘게 쪼개기(2장 NoSQL callback).

### 8. Postgres VACUUM 실패 — transaction wraparound 4시간 outage

- **증상**: Postgres가 갑자기 read-only로 전환된다. 로그에 "must be vacuumed within X transactions" 경고.
- **원인**: 32-bit XID가 wrap around 위험에 도달. autovacuum이 못 따라잡았다. 1장에서 본 가장 어두운 함정이 그대로 현실이 되는 자리.
- **즉시 mitigation**: 영향받은 테이블에 `VACUUM FREEZE` 수동 실행. 4시간 outage 각오.
- **근본 fix**: `autovacuum_vacuum_scale_factor`를 0.2에서 0.05로 낮춤. `pg_stat_user_tables`의 `n_dead_tup`을 정기 monitoring(1장 본문 callback).

### 9. TLS handshake가 1ms RTT 추가 — 곱셈으로 영향

- **증상**: HTTP/1.1로 동작하던 시스템에서 internal API 호출이 갑자기 100ms 느려졌다. 알고 보니 동기 호출 chain에 TLS termination이 5번 끼었다.
- **원인**: 매 connection마다 TLS handshake가 1~2ms RTT 추가. chain이 길면 곱셈으로 영향. keep-alive 안 살아 있으면 매 요청마다.
- **즉시 mitigation**: keep-alive 명시적 설정. connection pool로 handshake 비용을 한 번에 분산.
- **근본 fix**: HTTP/2 또는 gRPC 도입. multiplexing으로 한 connection에 다수 stream. TLS 1.3의 0-RTT resumption도 도움(6·9장 callback).

### 10. DST 1주일 전 cron 시간 비교 디버깅 — 매년 봄·가을

- **증상**: 11월 첫 주 cron job이 한 번 빠지거나 두 번 실행된다.
- **원인**: 시스템 시간이 UTC라도 application timezone이 KST/EST면 DST 전환 시 1시간 점프. 한국은 DST가 없지만 글로벌 service면 UTC + region 별 timezone 변환 burden이 따라온다.
- **즉시 mitigation**: DST 전환 주는 critical cron을 수동 모니터링. 두 번 실행 또는 빠진 job 즉시 catch-up.
- **근본 fix**: cron 표현식을 UTC로 통일. 시간 관련 로직은 모두 UTC 기반, display layer만 timezone 변환. 8장에서 본 시간 패턴(C3 Timezone Hell)의 부록 회수.

### 11. AWS NAT Gateway inter-AZ traffic 비용 — 빌의 80%

- **증상**: AWS 청구서가 매달 30% 늘어난다. 그런데 인스턴스 수는 안 늘었다.
- **원인**: NAT Gateway를 통한 inter-AZ traffic이 GB당 비용이 비싸다. private subnet의 ELB·RDS 호출이 의외로 cross-AZ로 흘러간다.
- **즉시 mitigation**: VPC Flow Logs로 cross-AZ traffic의 출처 파악. 가장 큰 source부터 cutoff.
- **근본 fix**: VPC endpoint(S3·DynamoDB) 도입으로 AWS service 호출 비용 제거. AZ-aware routing으로 application이 같은 AZ의 backend 우선 선택(우아한형제들이 30% 절감한 패턴, 검증 필요).

### 12. Database connection pool exhaustion → cascade

- **증상**: 한 service의 slow query 하나로 전체 mesh가 5분간 stall.
- **원인**: connection pool이 가득 차서 다음 요청들이 모두 connection 대기. downstream pool도 같이 차서 cascading.
- **즉시 mitigation**: 문제 service 격리, circuit break 강제.
- **근본 fix**: pool size를 작게 + timeout 짧게 + circuit breaker 의무화(1·10장 callback). HikariCP의 `connectionTimeout`과 `leakDetectionThreshold`가 1차 방어선.

### 13. Redis MGET vs pipeline 차이 — cluster mode의 함정

- **증상**: Redis cluster에서 `MGET key1 key2 key3`이 CROSSSLOT 에러로 실패. local Redis에서는 잘 됐는데.
- **원인**: cluster mode는 한 명령이 한 hash slot 안의 key만 다룰 수 있다. MGET은 단일 명령이라 cross-slot 불가. pipeline은 여러 명령의 묶음이라 가능.
- **즉시 mitigation**: MGET 대신 pipeline으로 변환. hash tag(`{tag}`) 활용으로 같은 slot에 묶기.
- **근본 fix**: cluster mode 도입 전 application 코드가 cluster-aware인지 검증. 라이브러리에 cluster-friendly hash tag 패턴 강제(3장 callback).

### 14. gRPC Java client의 deadline propagation — context 안 넘기면 client·server timeout이 따로

- **증상**: client는 5초 timeout으로 끊었는데, server는 30초 동안 계속 처리한다. 그 사이 client는 retry. server는 같은 요청을 동시에 두 번 처리.
- **원인**: gRPC deadline이 context로 전파되지 않으면 server는 client가 끊었는지 모른다. metadata에 deadline이 없으면 server 기본값으로 처리.
- **즉시 mitigation**: 의심되는 endpoint의 server-side 처리 시간 + client-side timeout 비교. log 분석.
- **근본 fix**: gRPC Java의 `Context.current().withDeadline()` 패턴 강제. interceptor로 모든 호출에 deadline propagation 박기. 10장 timeout 패턴의 gRPC 특수 변주.

### 15. Kubernetes liveness probe로 인한 self-restart loop

- **증상**: pod이 30초마다 재시작한다. DB 일시 끊김 직후 liveness fail로 K8s가 pod kill.
- **원인**: liveness probe가 너무 엄격해서 일시 장애에도 fail. readiness만 fail시키면 트래픽만 빠지는데, liveness가 fail이면 pod 자체가 죽는다.
- **즉시 mitigation**: liveness 임계값 늘리기 또는 일시 비활성화. readiness 우선.
- **근본 fix**: liveness는 "정말 죽었는가?"만 (자체 health endpoint, application 내부 deadlock 같은). DB 끊김은 readiness에서만 fail. 14장 health check 패턴의 K8s 변주.

### 16. Cassandra tombstone 누적 — TTL+delete가 read를 죽인다

- **증상**: Cassandra 같은 LSM-based DB의 read latency가 점차 늘어난다. p99이 100ms에서 시작해 시간이 갈수록 1초로.
- **원인**: tombstone(삭제 표시)이 sstable에 누적. read 시 tombstone scan 비용이 누적된다. TTL과 explicit delete가 많은 도메인에서 자주 발생.
- **즉시 mitigation**: `nodetool compact`로 강제 compaction. tombstone GC 임계값 조정.
- **근본 fix**: tombstone TTL을 짧게 설정(기본 10일 → 1~3일). 도메인 모델을 "삭제 없는 append-only"로 변경(15장 Event Sourcing callback). 2장 NoSQL의 silent killer.

### 17. Elasticsearch refresh_interval 1초 default — write 부하 폭발

- **증상**: ES write throughput이 평소의 1/3로 떨어진다. indexing thread가 끊임없이 busy.
- **원인**: `refresh_interval=1s`가 default. 1초마다 새 segment 만들어 indexing 부하 폭발. 검색 latency는 좋아도 write가 죽는다.
- **즉시 mitigation**: write 많은 index에 `refresh_interval=30s` 또는 `-1`(수동 refresh). bulk indexing 시는 -1로 끄기.
- **근본 fix**: 도메인별 refresh_interval 정책. 검색 즉시성이 필요한 index(채팅·트랜잭션)만 짧게, 분석성 index는 30초+. 5장 검색 silent killer의 부록 회수.

### 18. HikariCP의 leakDetectionThreshold — connection leak을 production에서 잡는 가장 빠른 방법

- **증상**: 시간이 갈수록 connection pool이 점차 줄어든다. 재시작하면 정상.
- **원인**: application 코드가 connection을 try-with-resources 없이 사용. exception path에서 close()를 빠뜨림.
- **즉시 mitigation**: 재시작으로 일단 회복.
- **근본 fix**: HikariCP의 `leakDetectionThreshold=60000`(60초) 활성화. 60초 이상 미반환 connection의 stack trace를 로그에 남긴다. 어느 메서드가 leak하는지 production에서 바로 잡힌다. 1장 connection pool의 부록 회수.

## 한국 환경 야사 — 회식 자리에서 가장 자주 나오는 이야기

tribal 18선이 글로벌 함정이라면, 한국 환경에는 그 위에 더해지는 야사가 있다. 회식 자리에서 가장 자주 나오는 세 가지를 짧게 봐 두자.

### 0시 트래픽과 새벽 운영자의 농담

한국 핀테크 운영자들이 농담처럼 하는 말이 있다. "한국에서 가장 무서운 단어는 청약·이자·콘서트다." 셋 모두 정시 burst의 대표 도메인이다. 19장에서 본 0시 트래픽이 운영자 입장에서는 매년 12번씩 만나는 시험이다. 새해 0시는 송년 메시지·이자·할인 쿠폰이 동시에 터지고, 12월의 새해 첫날은 모두가 출근 전에 결제·이체·청약을 하루로 몰아 둔다. 한국 SRE의 12월 첫 주는 다른 나라의 Black Friday Cyber Monday와 같은 무게다.

운영자가 그 자리에서 배우는 것: **트래픽은 절대 예측대로 오지 않는다. 사전 예열·rate limit·점진 출시가 같이 가야 한다.** 19장에서 본 토스의 1% progressive rollout이 이 환경에서 비로소 의미를 가진다.

### 카카오 SK C&C 화재 — 2022년 10월의 회고

2022년 10월 15일, 판교의 SK C&C 데이터센터에서 화재가 발생했다. 카카오 계열 service(카카오톡·카카오페이·카카오뱅크·다음 등)가 길게는 5일간 부분 중단됐다. 한국 IT 역사에서 가장 큰 outage 중 하나로 기록된다(한국 9).

회사가 발표한 교훈은 한 줄이다. **단일 IDC 의존은 위험하다.** 카카오 계열은 이후 multi-region·multi-IDC 아키텍처로 빠르게 이전했다. 12장에서 본 multi-region active-active의 한국 도입이 이 사건 이후로 폭발적으로 가속됐다. 그리고 다른 한국 IT 기업들도 같은 자기 검토를 했다.

운영자가 그 자리에서 배우는 것: **DR(Disaster Recovery)은 표 위의 도식이 아니라 분기마다 실제로 돌려보는 game day의 영역이다.** 9장 보안의 망분리와 14장 chaos engineering이 한 사건을 통해 어떻게 산업 표준이 됐는지의 한국 변주다.

### 우아한형제들 배민의 새벽 0시 운영 패턴

배민의 트래픽 패턴은 인상적이다. **저녁 6~9시가 정점이고, 자정~새벽 4시가 또 작은 정점**이다. 야식 시장이다. 그리고 새벽 4~7시는 거의 트래픽이 없다. 이 5시간이 운영자에게는 "큰 변경을 안전하게 할 수 있는 자리"다.

우아한형제들이 그 시간대를 활용한 패턴이 있다. 큰 마이그레이션이나 schema change를 4~7시 사이에 배치. 새벽 0시 야식 정점 직후·아침 정점 직전. 이게 한국 도메인의 운영 리듬이 시스템 디자인에 박힌 한 사례다(한국 6).

운영자가 그 자리에서 배우는 것: **도메인의 트래픽 리듬을 알면 운영 자유도가 늘어난다.** 글로벌 모범 사례(zero-downtime always)를 따르는 것도 좋지만, 도메인 리듬을 활용한 정직한 새벽 배포 운영도 좋은 선택이다.

## On-call의 휴머니즘 — alert가 사람을 깨우는가

14장에서 본 on-call burnout 패턴을 부록에서 한 번 더 되짚자. 카카오뱅크 채용 후기 jobplanet에 단골로 올라오는 불만이 "당직 빈도가 너무 잦음"이다(검증 필요). 그리고 비슷한 글이 토스·라인·우아한형제들·쿠팡 어느 회사 후기에도 한 번씩은 등장한다.

Charity Majors가 X에 2023년 쓴 한 줄이 가장 정직하다.

> If you can't sleep through your on-call, your alerts are wrong. (Charity Majors, X, 2023)

한국 핀테크의 on-call 문화는 글로벌 표준보다 무거운 경우가 많다. 24/7 운영의 부담, 망분리 환경에서의 escalation 복잡성, 5명 이하 팀에서의 rotation 부족이 모두 겹친다. 이 자리의 정답은 두 가지다.

1. **Alert 절반 자동화.** 토스 SLASH 22 발표가 정리한 패턴이다. on-call 엔지니어가 컴퓨터를 켜자마자 자동 해결된 alert가 보이면, 그 alert는 자동화 대상이다. 운영자가 직접 손대지 않는 alert를 매주 늘려 가는 것이 page fatigue 방어의 첫 줄.
2. **Runbook 의무화.** 모든 alert는 "이걸 받았을 때 처음 30초에 무엇을 해야 하는지" runbook이 있어야 한다. 없으면 alert를 보내면 안 된다. 14장 alert 설계의 가장 단호한 적용이다.

운영자가 사람으로 살아남을 수 있는 환경을 만드는 게 시스템 디자인의 한 자리다. 코드보다 더 중요한 자리.

## 이력서용 기술 도입의 함정 — "Kafka 쓰려고 도입했다"

OKKY에 정기적으로 올라오는 글이 있다. "이력서에 Kafka 쓰려고 도입했다. 실제로는 RabbitMQ로 충분했다."(한국 10) 회사에서 새 기술을 도입하는 결정의 30%는 비즈니스 필요가 아니라 채용·이력서 의도라는 농담 섞인 진실이다.

두 가지 사례를 짧게 보자.

**사례 1**: 한국 모 중규모 e-commerce가 service mesh를 도입했다(검증 필요). 도입 동기는 "채용 공고에 Istio 경험자 우대를 박기 위해"라는 자조 섞인 회고가 한 발표에서 흘러나왔다. 결과는 6장에서 본 그림 그대로. 5명 팀이 6개월간 mesh 튜닝에 시간을 보내고, sidecar OOM 디버깅에 새벽이 사라졌다. 1년 후 mesh를 들어내고 ALB + AWS PrivateLink로 단순화했다. 그 6개월의 학습이 회사에 무엇을 남겼는가 — "도구 선택은 이력서 아닌 비즈니스를 위한 것이다"는 단순한 명제 하나.

**사례 2**: 한국 모 핀테크가 NoSQL을 도입했다(검증 필요). 도입 동기는 "확장성을 위해"였다. 그런데 운영해 보니 데이터의 95%가 strong consistency가 필요한 결제·잔액 데이터였다. 2장에서 본 NoSQL의 schema-less 약속과 eventual consistency가 결제 도메인에 안 맞았다. 1년 후 Postgres로 다시 이전. 마이그레이션 비용은 NoSQL 1년 운영비의 3배.

이 사례들이 책 전체의 메타 약속을 다시 한 번 박는다. **시스템 디자인 결정은 우리의 도메인과 우리의 팀 규모와 우리의 운영 능력의 곱이다.** 다른 회사가 쓴다고 우리도 써야 하는 게 아니다. 0장 도입부에서 한 번 짚었던 명제가 부록에서 사례 두 개로 다시 회수된다.

## 배포·마이그레이션 실패담 두 가지

### 사례 1: 한국 모 핀테크의 blue-green 잘못 끊기 — 결제 30분 정지

(검증 필요) 한국 핀테크 한 곳이 blue-green 배포를 진행하다 결제가 30분간 정지된 사례가 있다. 시나리오를 풀어보면 다음과 같다.

- 새 버전(green)을 띄우고, traffic을 1% → 50% → 100%로 옮기는 중이었다.
- 100% 전환 직후, blue 환경을 즉시 종료했다. **이것이 첫 번째 실수.**
- 그런데 새 버전에 있던 미세 버그가 결제 일부 경로에서만 발생했다. canary 단계에서는 발견 안 된 버그.
- 100% green으로 가자마자 결제 실패율이 0.05% → 5%로 치솟았다.
- 운영자가 rollback하려고 보니 blue 환경이 이미 destroy된 상태. 새로 띄우는 데 30분.

이 사고에서 배운 두 가지 교훈. **첫째, blue 환경은 100% 전환 후에도 최소 30분~2시간 동안 hot-standby로 유지한다.** rollback 시점에 다시 띄울 시간이 없다. **둘째, canary 단계마다 결제 실패율의 fast/slow burn을 정량으로 확인한다.** 100%로 가도 되는지를 사람이 아닌 burn rate가 결정한다. 14장 progressive rollout의 부록 사례가 한국 핀테크에 어떻게 박혔는지의 회수.

### 사례 2: Slack 2021 outage — DNS 변경이 자기 자신을 끊었다

(검증 필요) 2021년 1월 4일, Slack이 4시간 가까이 부분 outage. postmortem이 매우 정직하다.

- 사내 DNS configuration을 routine하게 변경하던 중, 새 record가 이전 record를 덮어쓰며 internal service discovery가 무너졌다.
- 그런데 Slack의 SRE 팀이 사용하는 internal tool도 같은 DNS에 의존하고 있었다.
- "DNS를 고치러 들어가려고 했는데, internal tool에 접근이 안 됐다."
- 4시간이 걸린 가장 큰 이유는 외부 ssh로 직접 access해 DNS를 수동 수정해야 했기 때문이다.

이 사고에서 배운 두 가지 교훈. **첫째, infrastructure 변경의 blast radius를 항상 한 단계 더 넓게 본다.** DNS 변경 한 줄이 운영 도구를 같이 끊을 수 있다. **둘째, break-glass access path를 별도로 둔다.** internal tool이 죽었을 때 외부에서 직접 접근할 수 있는 emergency channel이 항상 있어야 한다. 9장 보안의 망분리에서도 break-glass 패턴이 한국 핀테크 표준이다(검증 필요).

운영의 가장 비싼 학습은 항상 사고에서 온다. 그래서 blameless postmortem이 한국 IT의 표준 문화로 정착되는 이유다.

## AI/LLM 한 페이지 — 다음 책의 약속

이 책은 LLM·vector DB·RAG·embedding service를 본격적으로 다루지 않는다. 2026년 현재 이 영역은 빠르게 변하고 있어서, 한 권의 책으로 정리하기에는 아직 이르다. 그러나 한 가지 명제는 분명하다.

**이 책의 모든 빌딩 블록과 패턴이 LLM 시대에도 살아 있다. 도구가 더 늘었을 뿐이다.**

0장 도입부에서 약속한 "다음 책의 약속"이 여기서 한 페이지로 회수된다. 6개 영역의 매핑을 짧게 보자.

- **Vector DB**(pgvector·Pinecone·Weaviate·Qdrant): 1장 RDB·2장 NoSQL의 검색 패턴이 embedding 위로 확장된 형태. ANN 알고리즘이 18장에서 본 IVF·HNSW다.
- **RAG (Retrieval-Augmented Generation)**: 5장 검색·11장 데이터 파이프라인·3장 캐시가 한 자리에 모이는 새 도메인. document → chunk → embed → retrieve → LLM의 파이프라인이 15장의 Lambda/Kappa 패턴 위에 얹힌다.
- **LLM serving**: 4장 큐(batch inference)·14장 rate limit·14장 백프레셔가 GPU 자원의 희소성 환경에서 다른 결로 변주된다. token bucket이 GPU compute slot 단위로 적용된다.
- **Embedding service**: 6장 service mesh·9장 보안·10장 멱등성이 새 도메인에서 그대로 적용된다. embedding API 호출도 멱등하지 않으면 결제처럼 비용이 두 번 청구된다.
- **Agent orchestration**: 11장 Saga·12장 합의·13장 Fan-out이 multi-agent workflow에서 같은 모양으로 등장한다. agent A가 agent B에 작업을 위임하는 흐름이 분산 트랜잭션의 새 변주다.
- **Cost control**: 7장 CDN·FinOps가 LLM token 비용 관리로 확장된다. prompt caching·response caching·model routing이 cache 챕터의 새 자리.

이 모든 자리에서, 1·2부의 부품과 패턴이 새 도메인의 1번 줄이 된다. LLM이 시스템 디자인을 바꾸는 게 아니라, 시스템 디자인이 LLM을 운영 가능하게 만든다.

**다음 책의 약속**: 이 영역이 안정화되면 별권으로 정리할 만하다. 그때 다시 만나는 자리에서, 이 책의 mental model이 어떻게 확장 적용되는지를 함께 살펴보자.

## 책의 한계 — 우리가 안 다룬 영역

마지막으로 정직하게 짚자. 이 책이 안 다룬 영역이 몇 가지 있다.

- **모바일 백엔드 특수성**: push notification provider(FCM·APNs) 운영, offline-first sync, mobile-specific authentication. 이건 별도 책의 주제다.
- **게임 서버 특수성**: tick-rate 기반 simulation, lockstep / rollback netcode, MMORPG의 shard 운영. 별도 도메인.
- **데이터 거버넌스 / GDPR·CCPA·PIPA**: 한국 개인정보보호법은 9장에서 잠깐 짚었지만, 깊이 있는 데이터 권리·삭제 요청·DSAR 처리는 별도 주제.
- **ML / Data Engineering의 deep dive**: 15장에서 파이프라인의 큰 그림을 봤지만, feature store·model registry·ML observability는 별도 영역.

이 한계들은 책의 부족함이 아니라, 한 책이 다룰 수 있는 범위의 정직한 인정이다. 우리는 분산 시스템의 빌딩 블록·패턴·케이스 스터디의 한 권을 만들었다. 모든 것을 한 권에 담는 책은 그 어느 것도 깊이 다루지 못한다.

## 마지막 한 줄 — production은 결국 사람의 영역

부록의 끝에서 한 번 더 짚는다. **production은 결국 사람의 영역이다.** 새벽 3시 alert를 받는 사람, blameless postmortem을 쓰는 사람, 마이그레이션을 결심하는 사람, 도구를 선택하는 사람 — 모두 사람이다.

이 책의 모든 부품·패턴·케이스는 결국 그 사람의 결정을 더 정직하게 만드는 도구다. 도구가 우리를 일하게 하는 자리가 아니라, 우리가 도구를 일하게 하는 자리에 우리 팀을 두자(6장 회수). 그게 시스템 디자인의 진짜 마지막 약속이다.

새벽 alert가 울리는 그 자리, 코드를 함께 들여다보는 그 자리에서 — 이 책이 한 번이라도 옆자리의 동료처럼 느껴진다면, 우리의 약속은 지켜졌다.

수고했다. 함께 와줘서 고맙다.

---

---


# 감사의 말

이 책은 한 사람의 머리에서 한 번에 나온 책이 아니다. 한국 백엔드 커뮤니티가 지난 10여 년 동안 쌓아 올린 발표·블로그·논쟁의 위에 얹혀 있다.

먼저 토스·카카오·당근·쿠팡·우아한형제들·라인·네이버·카카오뱅크의 엔지니어링 팀에 감사를 전한다. SLASH·if(kakao)·우아콘·DEVIEW 같은 발표 자리에서 정직하게 풀어낸 실패담과 결정 과정이 이 책의 한국 사례 절들의 토대가 됐다. 발표 자료를 공개로 두는 결정 하나가 후배 세대의 학습 비용을 얼마나 줄이는지 — 그 가치는 측정하기 어렵다.

영어권 거인들에게도 빚이 있다. Martin Kleppmann의 *Designing Data-Intensive Applications*가 분산 시스템 이론을 일상의 어휘로 끌어내린 책이라면, 이 책은 그 어휘를 한국 백엔드 일상으로 한 번 더 번역하려는 시도다. AWS Builders' Library·Google SRE Book·Stripe Engineering Blog·Discord Engineering·Shopify Engineering 같은 기업 블로그들이 production의 진짜 디테일을 공개로 풀어내 준 덕분에 케이스 챕터들이 비로소 가능해졌다. Daniel Abadi·Marc Brooker·Charity Majors·Brandur Leach 같은 권위자들의 시각은 trade-off 표 곳곳에 스며들어 있다.

논문과 시스템의 원전 저자들 — Leslie Lamport, Diego Ongaro, Jay Kreps, Marc Shapiro, James Hamilton, Werner Vogels — 의 작업이 이 책의 척추다. 인용 표시에 (P#)이 박힌 자리마다, 우리 모두가 그 어깨 위에 서 있다는 사실을 기억해 두자.

마지막으로, 이 책을 읽어 줄 한국 백엔드 동료들에게. 새벽 alert을 받고, 캐시를 한 번 비웠다가 DB가 죽는 광경을 본 사람들. 0시 트래픽이 통신 3사 API까지 흔드는 광경을 본 사람들. 이력서용 기술 도입의 함정에 한 번씩 빠져 본 사람들. 함께 이 길을 걷는 동료가 있다는 사실이 이 책을 쓰는 동안의 가장 큰 위안이었다. 부족한 부분이 보이면 거리낌없이 짚어 주시기 바란다 — 다음 판본에 반영하겠다.

— Toby-AI

---

# 참고문헌

본문 안에서 (P#)·(W#)·(C#)·(자료 #)으로 표기된 인용의 색인이다. 권위 등급 ★★★ (1차 자료·peer-reviewed) / ★★ (검증된 industry 자료) / ★ (커뮤니티·블로그) 순서로 분류되어 있다.

## 1. 논문 — Academic ★★★

- Lamport, L. (1978). Time, Clocks, and the Ordering of Events in a Distributed System. *CACM*, 21(7), 558–565. **(P4)**
- Fischer, M., Lynch, N., Paterson, M. (1985). Impossibility of Distributed Consensus with One Faulty Process. *JACM*, 32(2), 374–382. **(P30)**
- O'Neil, P., Cheng, E., Gawlick, D., O'Neil, E. (1996). The Log-Structured Merge-Tree. *Acta Informatica*, 33(4), 351–385. **(P13)**
- Lamport, L. (1998). The Part-Time Parliament. *ACM TOCS*, 16(2), 133–169. **(P1)**
- Gilbert, S., Lynch, N. (2002). Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services. *SIGACT News*, 33(2). **(P31)**
- Dean, J., Ghemawat, S. (2004). MapReduce: Simplified Data Processing on Large Clusters. *OSDI '04*. **(P16)**
- Chang, F., et al. (2006). Bigtable: A Distributed Storage System for Structured Data. *OSDI '06*. **(P8)**
- DeCandia, G., et al. (2007). Dynamo: Amazon's Highly Available Key-value Store. *SOSP '07*, 205–220. **(P7)**
- Hunt, P., Konar, M., Junqueira, F., Reed, B. (2010). ZooKeeper: Wait-Free Coordination for Internet-Scale Systems. *USENIX ATC '10*. **(P3)**
- Lakshman, A., Malik, P. (2010). Cassandra: A Decentralized Structured Storage System. *SIGOPS OSR*, 44(2). **(P9)**
- Shapiro, M., Preguiça, N., Baquero, C., Zawirski, M. (2011). Conflict-Free Replicated Data Types. *SSS '11*, LNCS 6976. **(P11)**
- Corbett, J., et al. (2012). Spanner: Google's Globally-Distributed Database. *OSDI '12* → *ACM TOCS* 2013, 31(3). **(P5)**
- Thomson, A., et al. (2012). Calvin: Fast Distributed Transactions for Partitioned Database Systems. *SIGMOD '12*. **(P10)**
- Zaharia, M., et al. (2012). Resilient Distributed Datasets. *NSDI '12*. **(P17)**
- Shute, J., et al. (2013). F1: A Distributed SQL Database That Scales. *VLDB 2013*, 1068–1079. **(P15)**
- Bailis, P., et al. (2014). Highly Available Transactions: Virtues and Limitations. *VLDB 2014*. **(P12)**
- Ongaro, D., Ousterhout, J. (2014). In Search of an Understandable Consensus Algorithm. *USENIX ATC '14*, 305–319. **(P2)**
- Akidau, T., et al. (2015). The Dataflow Model. *VLDB 2015*. **(P20)**
- Carbone, P., et al. (2015). Apache Flink: Stream and Batch Processing in a Single Engine. *IEEE Data Engineering Bulletin*, 38(4). **(P18)**
- Verbitski, A., et al. (2017). Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases. *SIGMOD '17*, 1041–1052. **(P14)**
- Hellerstein, J. M., Alvaro, P. (2020). Keeping CALM: When Distributed Consistency is Easy. *CACM*, 63(9), 72–81. **(P6)**
- Kleppmann, M. (2022). Convergence: Local-first software. *ACM Queue*, 20(4). **(자료 28)**

## 2. 서적 ★★★

- Beyer, B., Jones, C., Petoff, J., Murphy, N. (eds) (2016). *Site Reliability Engineering*. O'Reilly. **(P23)**
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. **(P21)**
- Beyer, B., et al. (2018). *The Site Reliability Workbook*. O'Reilly. **(P24)**
- Burns, B. (2018). *Designing Distributed Systems*. O'Reilly. **(P27)**
- Richardson, C. (2018). *Microservices Patterns*. Manning. **(P25)**
- Petrov, A. (2019). *Database Internals*. O'Reilly. **(P22)**
- Newman, S. (2021). *Building Microservices*, 2nd ed. O'Reilly. **(P26)**

## 3. 공식 문서·기업 엔지니어링 블로그 ★★

- AWS Caching Strategies Whitepaper. https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html **(W1)**
- AWS Builders' Library: Timeouts, Retries and Backoff with Jitter. https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ **(W16)**
- AWS Builders' Library: Caching challenges and strategies. **(W40 참조)**
- Cloudflare: How we built rate limiting capable of scaling. https://blog.cloudflare.com/counting-things-a-lot-of-different-things/ **(W15)**
- Cloudflare: 330+ city PoP network. https://www.cloudflare.com/network/ **(W6)**
- Stripe: Designing robust and predictable APIs with idempotency (Brandur Leach, 2017). https://stripe.com/blog/idempotency **(W11)**
- Debezium: Reliable Microservices Data Exchange with the Outbox Pattern. https://debezium.io/blog/2019/02/19/reliable-microservices-data-exchange-with-the-outbox-pattern/ **(W13)**
- Discord: How Discord Stores Trillions of Messages. https://discord.com/blog/how-discord-stores-trillions-of-messages **(W21)**
- Netflix TechBlog: Netflix Live Origin (2025). https://netflixtechblog.com/netflix-live-origin-41f1b0ad5371 **(W25)**
- Uber: H3 — A Hexagonal Hierarchical Geospatial Indexing System. https://www.uber.com/us/en/blog/h3/ **(W26)**
- Shopify Engineering: A Pods Architecture To Allow Shopify To Scale. https://shopify.engineering/a-pods-architecture-to-allow-shopify-to-scale **(W27)**
- Airbnb Engineering: Categories ML / Search Ranking. **(W28)**
- Slack Engineering: KalDB — search infrastructure. **(W22)**
- Twitter Engineering: Manhattan KV. **(W23)**
- Instagram Engineering: Feed fanout via Gearman → Kafka. **(W24)**
- LinkedIn: Jay Kreps, Questioning the Lambda Architecture (2014). https://www.oreilly.com/radar/questioning-the-lambda-architecture/ **(자료 19)**
- Loggly: HAProxy vs NGINX vs Envoy benchmark. **(W5)**
- Google SRE Workbook: Implementing SLOs. https://sre.google/workbook/implementing-slos/ **(W35)**
- Google SRE Book: Postmortem Culture. https://sre.google/sre-book/postmortem-culture/ **(W36)**
- OpenTelemetry: Observability primer. https://opentelemetry.io/docs/concepts/observability-primer/ **(W37)**
- Principles of Chaos Engineering. https://principlesofchaos.org/ **(W38)**
- LaunchDarkly: Deploying without downtime. https://launchdarkly.com/blog/deploying-without-downtime/ **(W39)**
- Service Mesh latency benchmarks (Linkerd vs Istio vs Ambient). **(W44)**

### 한국 기업 엔지니어링 블로그·발표

- Toss tech: 토스의 결제 시스템 현대화. https://toss.tech/article/payments-legacy-1 **(W29)**
- Toss tech: SLASH 23 코어뱅킹. https://toss.tech/article/slash23-corebanking **(W29)**
- LINE Engineering ko: 메시징 허브 시리즈. https://engineering.linecorp.com/ko/blog/about-messaging-hub-2 **(W30)**
- 당근마켓 채팅팀 채용 비전·문화. https://about.daangn.com/ **(W31)**
- 쿠팡 엔지니어링 (Medium ko). https://medium.com/coupang-engineering/ **(W32)**
- 카카오 tech: 공용 Kafka/RabbitMQ 메시징 플랫폼. https://tech.kakao.com/2021/12/23/kafka-rabbitmq/ **(W33)**
- 카카오뱅크 tech. https://tech.kakaobank.com/ **(W41)**
- 네이버 검색 엔지니어링 가이드. https://naver-career.gitbook.io/kr/service/search/engine-and-solution/search-engine **(W45)**
- 네이버 D2. https://d2.naver.com/
- 우아한형제들 기술블로그. https://techblog.woowahan.com/

## 4. 권위자 블로그·X ★★

- Martin Kleppmann (DDIA 저자). https://martin.kleppmann.com/
- Marc Brooker (AWS Distinguished Engineer). https://brooker.co.za/blog/
- Daniel Abadi (NewSQL 비판, PACELC). http://dbmsmusings.blogspot.com/ **(W17)**
- Charity Majors (Honeycomb CTO). https://charity.wtf/ + X @mipsytipsy
- Will Larson (*Staff Engineer* 저자). https://lethain.com/
- Camille Fournier (*The Manager's Path* 저자). https://skamille.medium.com/
- Cindy Sridharan (*Distributed Systems Observability*). https://copyconstruct.medium.com/
- Brandur Leach (Stripe 전 엔지니어). https://brandur.org/
- Salvatore Sanfilippo / antirez (Redis 창시자). http://antirez.com/

## 5. 커뮤니티 인덱스 ★

- Hacker News. https://news.ycombinator.com/
- Reddit: r/ExperiencedDevs · r/programming · r/devops · r/SRE · r/aws · r/kubernetes
- OKKY. https://okky.kr/
- velog (백엔드 태그). https://velog.io/tags/backend
- Use The Index, Luke! (Markus Winand). https://use-the-index-luke.com/

## 6. 보조 자료·외부 규제 1차 자료

- OAuth 2.0 RFC 6749. https://datatracker.ietf.org/doc/html/rfc6749
- OAuth 2.1 draft. https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1
- PKCE RFC 7636. https://datatracker.ietf.org/doc/html/rfc7636
- OpenID Connect Core 1.0. https://openid.net/specs/openid-connect-core-1_0.html
- OWASP API Security Top 10 (2023). https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- SPIFFE/SPIRE 공식 문서. https://spiffe.io/docs/
- 전자금융감독규정 (한국 금융감독원). https://www.fss.or.kr/
- IANA Time Zone Database. https://www.iana.org/time-zones
- Web Push Protocol RFC 8030. https://datatracker.ietf.org/doc/html/rfc8030

---

# 판권

**현장에서 살아남는 시스템 디자인** — 작은 internal 시스템부터 글로벌 SaaS까지

- **저자:** Toby-AI
- **첫 출간:** 2026년 5월 17일
- **책 판본:** v1.0.0
- **언어:** 한국어
- **식별자:** `system-design-handbook-v1.0.0`

## 라이선스

이 책은 [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 라이선스로 배포된다.

- **저작자 표시(BY):** 출처를 밝힐 것.
- **비상업적 이용(NC):** 상업적 목적으로 이용할 수 없다.
- **동일조건 변경허락(SA):** 변경·재배포 시 동일한 라이선스를 적용해야 한다.

라이선스 전문: https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.ko

## 발행

이 책은 **book-writer harness v1.2.0** (MIT 라이선스) 으로 자동 생성됐다. 하네스 소스: https://github.com/ (오픈 소스로 공개됨). 하네스는 리서치 → 저술 계획 → 챕터 저술(Toby 스타일) → 편집 → EPUB 빌드를 한 명령으로 수행하는 AI 자동 저술 파이프라인이다.

하네스 코드 자체는 MIT 라이선스, 이 책의 콘텐츠는 CC BY-NC-SA 4.0이다 — 두 라이선스는 별개로 적용된다.

## 저자 소개

**Toby-AI** — AI 자동 저술 하네스가 산출한 가상 저자. 한국 백엔드 커뮤니티의 발표·블로그·논쟁 위에 학습되어 토스·카카오·당근·쿠팡 같은 회사의 실무 디테일을 한국어로 풀어낸다. 이 책 외에 다른 책들도 동일 하네스에서 산출되어 있다.

## 인용·연락처

이 책을 인용할 때는 다음 형식을 권한다.

> Toby-AI (2026). *현장에서 살아남는 시스템 디자인 — 작은 internal 시스템부터 글로벌 SaaS까지* (v1.0.0). CC BY-NC-SA 4.0.

오류 제보·피드백: book-writer 하네스의 GitHub issue를 통해 받는다.

---

*production은 결국 사람의 영역이다.*
