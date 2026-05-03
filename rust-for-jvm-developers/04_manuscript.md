# JVM 출신을 위한 Rust

### Spring 다음에 읽는 책

**저자:** Toby-AI
**판본:** 1.0.0 · 2026년
**대상 독자:** Java/Kotlin/Spring 다년 백엔드 개발자
**한 줄 카피:** Spring 너머의 시스템을 빌드하는 16개의 챕터.


---

# 서문 — JVM 출신을 환영하며

## 왜 이 책을 썼는가

월요일 아침 결제 서비스에서 NPE 17건이 떴다는 슬랙 메시지를 받아본 사람이라면, 이 책의 첫 줄을 읽기 전에 이미 절반쯤 책의 정서를 알고 있다. 우리가 십 년 넘게 Spring으로 시스템을 만들면서 *어쩔 수 없이 감수해온 카테고리*의 사고들이 있다. NullPointerException, ConcurrentModificationException, OutOfMemoryError, GC pause로 인한 tail latency 스파이크, Native Query와 스키마가 어긋나서 *배포 직후에야* 드러나는 컬럼 불일치. 익숙하다. 그리고 솔직히 *번거롭다*.

이 책은 그 사고들의 *큰 덩어리*를 *런타임이 아니라 빌드 단계*로 옮길 수 있는 도구 한 가지를 소개하기 위해 쓰였다. 이름은 Rust다. 그 이름이 백엔드 개발자의 의제로 떠오른 건 어제오늘 일이 아니지만, JVM 출신만의 동선으로 정리된 한국어 입문·활용서가 시장에 비어 있었다. *『러스트 프로그래밍 언어』*는 언어 표준 레퍼런스를 다루고, *『프로그래밍 러스트』*는 시스템 프로그래밍의 깊이로 가고, *『LUVIT 실전 백엔드 러스트 Axum 프로그래밍』*은 axum 사용법을 정면으로 다룬다. 모두 좋은 책이다. 다만 *"내일 출근해서 Spring 카운터파트와 한 줄씩 비교하며 axum + sqlx로 결제 API를 짜야 하는 시니어 개발자"*에게 직선으로 가는 책은 자리가 비어 있었다. 이 책이 채우려는 빈자리가 거기다.

이 책은 *번역 가이드*다. 자네가 이미 Spring DI, JPA, CompletableFuture, Kotlin Coroutine을 손에 익힌 상태에서 *그 익숙함을 닻으로 삼아* Rust의 새 개념을 옮겨 심는 책이다. 16개 챕터 모두에 *JVM 대응물 매핑*이 시그니처로 박혀 있다. 빠지는 챕터가 없다. 이 한 가지 약속이 책 전체를 한 줄로 꿰는 시그니처다.

## 누구를 위한 책인가

먼저 호명하자. *Java 또는 Kotlin으로 Spring 백엔드를 3년 이상 짠 미들~시니어 개발자*다. JPA·Spring Data·CompletableFuture·Kotlin Coroutine 중 적어도 둘 정도는 손에 잡혀 있어야 한다. JNI를 한 번이라도 만져본 적이 있다면 15장이 더 빠르게 읽힌다. Java 21의 Virtual Thread 또는 GraalVM Native Image를 한 번 검토해본 적이 있다면 1장과 14장의 비교가 더 깊게 들어온다.

다음으로 *호명하지 않는* 독자다. 첫째, *Rust로 OS 커널이나 임베디드 펌웨어를 짜고 싶은 사람*이다. 그 영역은 본 책의 백엔드 스코프 밖이고, 더 좋은 책들이 따로 있다. 둘째, *프로그래밍 자체를 처음 배우는 사람*이다. 이 책은 자네가 *시스템을 만들 줄 안다*는 사실을 전제 삼아 출발한다. 셋째, *Rust 표준 라이브러리의 모든 함수와 메서드를 망라하기를 원하는 사람*이다. 그건 공식 문서가 더 잘 한다. 이 책은 *시야의 책*이지 레퍼런스가 아니다.

마지막으로 정직한 한 줄. 이 책은 *마법으로 학습 곡선을 줄여주지 않는다*. corrode의 권고를 그대로 인용하면 *"Plan 4-6 months for your engineers to get comfortable with Rust"*다. 이 책의 역할은 그 4~6개월의 곡선을 *없애는* 것이 아니라 *함께 걷는* 것이다. 그 정직함을 받아들이고 한 페이지를 더 펴줬으면 좋겠다.

## 어떻게 읽으면 좋은가

권장 동선은 *처음부터 끝까지 순서대로 한 번 읽고, 부록을 책상 옆에 펴두고 다시 한 번 펴는* 것이다. 책의 흐름이 독자의 감정 곡선에 맞춰 다섯 단계로 설계됐다. *의심 → 호기심*(1~2장), *작은 성취 → 막막함*(3~4장), *친구되기 → 표현력*(5~7장), *안전 경계 → 자신감 → 실무*(8~13장), *출시 → 폴리글랏 → 사람*(14~16장). 한 장 한 장이 다음 장의 *복선*과 *회수*로 이어진다. 가능하면 5~6장을 한 자리에 빠뜨리지 말고 가자. 4장 소유권의 막막함이 5장 빌림에서 풀리고, 6장 라이프타임에서 안도감으로 닫힌다. 이 흐름을 끊으면 *답답함만 손에 남는다*.

매 챕터 끝의 *"함께 해보자"* 절을 *진짜로 손으로* 따라 짜보자. 1장에서 적어둔 *자기 회사의 운영 사고 한 줄*은 7장·9장·10장·16장에서 다시 호명된다. 2장에서 짠 작은 CLI는 13장의 clap 절에서 완성형으로 회수된다. 3장에서 만든 도메인 struct는 4장 소유권의 첫 예제, 7장 thiserror 모델링으로 이어진다. 11장에서 띄운 in-memory 서비스는 12장에서 PostgreSQL로 옮겨지고, 13장에서 workspace로 쪼개지고, 14장에서 8MB 컨테이너로 빌드되고, 15장에서 JVM과 잇는 다리가 된다. 한 줄로 정리하면 *책 전체가 한 채의 시스템을 같이 짓는 한 줄짜리 동선*으로 꿰어져 있다.

부록 4편(JVM↔Rust 매핑 표 / cargo 치트시트 / 추천 crate 카탈로그 / 4~6개월 학습 가이드)은 *책 본문을 다 읽기 전에도* 펴봐도 좋다. 특히 부록 D는 *책을 다 읽기 전에 자기 캘린더를 짜는* 데 쓰자. 책상 옆에 붙여두자.

마지막 한 줄. 이 책의 어조는 평어체와 청유형이 섞여 있다. *지시*가 아니라 *동행*의 톤이다. 4~6개월의 적응 기간을 *함께 걷는* 동료의 자리에 책이 앉아 있기를 바랐다. 자네가 한 챕터씩 지나오는 동안 그 자리가 *조금이라도 가벼웠기를*. 이제 시작하자.


---

# 목차

**서문 — JVM 출신을 환영하며**

**Part 1. 왜 Rust인가, 그리고 첫 만남**
- 1장. 왜 지금 Rust인가 — JVM 베테랑에게 보내는 초대장
- 2장. 첫 만남 — cargo로 5분 만에 빌드하기
- 3장. 변수·타입·함수·모듈 — Java가 알던 모양과 다른 부분

**Part 2. Rust의 마음 — 컴파일러와 친구되기**
- 4장. 소유권 — "한 명만 가진다"는 단순한 규칙
- 5장. 빌림 — `&T`와 `&mut T`, 그리고 데이터 레이스가 사라지는 이유
- 6장. 라이프타임 — `'a`라는 메타데이터에 익숙해지자
- 7장. 트레잇·제네릭·패턴 매칭·에러 처리 — 표현력 도구상자
- 8장. 스마트 포인터·매크로·unsafe 진입 — 메모리 도구와 안전 경계

**Part 3. 실무 시스템을 만든다**
- 9장. 동시성 기초 — 스레드, channel, Mutex, 그리고 `Send`/`Sync`
- 10장. async와 tokio — Spring WebFlux/Kotlin Coroutine 다음의 모델
- 11장. axum으로 첫 HTTP 서비스 — Spring Controller가 Rust로 보이는 순간
- 12장. 데이터베이스 — sqlx로 컴파일 타임 검증된 SQL을, sea-orm으로 친숙한 ORM을

**Part 4. 출시와 그 다음**
- 13장. 테스트·품질·도구 인프라·CLI — cargo가 IDE·Sonar·JMH·picocli·OWASP를 모두 안고 있다
- 14장. 출시 — 8MB 컨테이너와 OpenTelemetry 관측
- 15장. JVM과 함께 — FFI·JNI·Project Panama·폴리글랏 아키텍처
- 16장. Rust로 가는 길 — 사람·조직·커리어, 그리고 매듭

**에필로그 — 책을 닫으며**

**부록**
- 부록 A. JVM ↔ Rust 한 페이지 매핑 표
- 부록 B. cargo / rustup / clippy / rustfmt 치트시트
- 부록 C. 추천 crate 카탈로그
- 부록 D. 4~6개월 학습 가이드 — 주차별 마일스톤

**참고문헌**

**감사의 글**


---

# Part 1. 왜 Rust인가, 그리고 첫 만남

> *"JVM 출신을 환영합니다"의 톤으로 시작하자. 첫 두 챕터의 목표는 도망가지 않게 하는 것이다.*

Part 1은 *의심에서 호기심으로* 가는 다리다. 1장은 *왜 지금 Rust가 백엔드 개발자의 의제인지*를 ONCD/NSA 권고와 Discord/Cloudflare/AWS/Microsoft 사례로 짚고, *이 책이 시장의 어느 빈자리를 채우는지*를 정직하게 적었다. 2장은 cargo로 *5분 만에 첫 바이너리*를 손에 쥐는 경험을 깐다. Maven/Gradle/Sonar/JMH/picocli/Spotless가 *cargo 한 도구 안에* 어떻게 들어와 있는지를 손가락으로 만져보자. 3장은 변수·타입·함수·모듈을 *Java/Kotlin과의 1:1 대응*으로 빠르게 흡수시킨 다음, *에러 메시지 읽는 법* 한 절로 4장 소유권의 첫 컴파일 거부에 미리 대비시킨다.

**포함 챕터**

- 1장. 왜 지금 Rust인가 — JVM 베테랑에게 보내는 초대장
- 2장. 첫 만남 — cargo로 5분 만에 빌드하기
- 3장. 변수·타입·함수·모듈 — Java가 알던 모양과 다른 부분


---

# 1장. 왜 지금 Rust인가 — JVM 베테랑에게 보내는 초대장

월요일 아침 9시, 운영팀에서 슬랙 메시지가 하나 떨어졌다고 해보자. "어젯밤 결제 서비스에서 NullPointerException이 17건, 메모리 누수로 보이는 OOM이 1건 났습니다. 알람 받으셨죠?" 익숙한 풍경 아닌가? Spring Boot로 결제 시스템을 짜온 지 십 년 가까이 됐는데도, 이런 알림 앞에서 우리는 매번 같은 일을 한다. 스택 트레이스를 펼쳐보고, 어디서 null이 끼어들었는지 추적하고, 힙 덤프를 떠서 어느 컬렉션이 부풀었는지를 본다.

그런데 잠시 멈추고 생각해보자. 만약 그 NPE가 *컴파일 단계에서 빨간 줄로 그어졌다면* 어땠을까? OOM의 원인이 된 그 객체가 *함수가 끝나는 순간 결정적으로 회수됐다면* 어땠을까? 십 년 동안 우리가 운영 시간에 잡아온 사고들의 큰 덩어리를, 만약 빌드 시간에 못 박을 수 있다면? 이것이 Rust가 지난 몇 년 사이 *백엔드 개발자의 의제*가 된 이유다.

물론 새 언어를 배운다는 게 가벼운 일은 아니다. 우리에게는 이미 Spring이 있고, JPA가 있고, Kotlin coroutine이 있다. 굳이 또 하나의 언어를? 그런 의심을 품고 이 책을 펼친 독자가 가장 많을 것이다. 그 의심을 부정하지 않는다. 오히려 그 의심에서 출발하자. 이 챕터에서 우리가 같이 점검할 것은 두 가지다. 첫째, *왜 지금 시점에 Rust가 백엔드 개발자의 의제인가*. 둘째, *왜 다른 Rust 책이 아니라 굳이 이 책인가*. 둘 다 정직한 답을 가지고 있어야 4~6개월의 적응 기간을 함께 걸을 수 있다.

## "메모리 안전"이 정부 권고가 된 시대

먼저 시장의 풍향부터 살펴보자. 2024년 2월, 미국 백악관 산하 ONCD(Office of the National Cyber Director)가 「Back to the Building Blocks: A Path Toward Secure and Measurable Software」라는 기술 보고서를 발표했다.[^1] 이 보고서가 권한 메시지는 단순하다. *"메모리 안전 언어로 옮겨가자."* 그리고 보고서가 사실상 유일하게 "메모리 안전 언어"의 사례로 호명한 언어가 Rust였다. 정부 기관이 특정 프로그래밍 언어를 권한 일은 흔하지 않다. 1년 뒤인 2025년 6월에는 미국 NSA가 「Memory Safe Languages: Reducing Vulnerabilities in Modern Software Development」를 펴내며 같은 방향으로 한 번 더 못을 박았다.[^2]

왜 이런 일이 벌어졌을까? Microsoft가 자사 제품의 보안 취약점을 분석했더니 *전체 취약점의 약 70%가 C/C++의 메모리 오류에서 비롯됐다*는 결과가 나왔기 때문이다.[^3] 버퍼 오버플로, use-after-free, double-free, dangling pointer 같은 것들이다. 이 숫자는 Microsoft만의 문제가 아니다. 그동안 우리가 "어쩔 수 없이 감수하던" 카테고리의 사고였다.

Java/Kotlin 개발자 입장에서는 한 발짝 떨어진 이야기처럼 들릴 수도 있다. JVM은 GC가 있고, 포인터 산술이 없고, NPE는 있을지언정 use-after-free는 없으니까. 그런데 흥미로운 사실 하나. ONCD/NSA의 권고가 호명한 "메모리 안전 언어" 목록에는 Java도 포함된다. 다만 Java가 그 안전성을 *런타임 GC와 JVM 검증*으로 얻는 반면, Rust는 *컴파일러의 정적 검증*으로 얻는다. 둘 다 안전하지만, *언제 안전을 보장하는가*가 다르다. 그리고 그 시점의 차이가 운영의 풍경을 바꾼다. GC가 도는 동안의 stop-the-world, JIT warm-up 동안의 느린 응답, 힙 200MB를 미리 잡고 시작해야 하는 컨테이너 — JVM의 안전성에는 그만한 청구서가 따라온다. Rust는 *그 청구서를 받지 않으면서* 같은 안전성을 가져간다.

## 시장 신호 — 의심에서 채택으로

신호 하나로는 부족하니 몇 개 더 보자. 매년 발표되는 *State of Rust Survey*의 2024년판에 따르면 **응답 조직의 45%가 Rust를 프로덕션에서 의미 있게 사용**한다고 답했다.[^4] 2023년의 38%에서 1년 만에 7%p가 올랐다. 그중 가장 큰 도메인이 백엔드/서버사이드(51.7%)다. *"Rust는 시스템 프로그래머들의 장난감이다"*라는 말이 한 시절의 말이 됐다는 신호다.

개발자 커뮤니티의 체온도 같은 방향이다. 2025년 Stack Overflow Developer Survey에서 Rust는 **9년 연속 "most admired language" 1위**, admiration rate 83%를 기록했다.[^5] "내가 쓰고 있고 앞으로도 쓰고 싶은 언어"가 어떤 것이냐는 질문에 가장 많은 개발자가 Rust를 꼽았다는 뜻이다. 9년 연속 1위는 인내심 시험에 가까운 기록이다. *"한 번 써본 사람의 만족도가 일관되게 높다"*는 말과 같다.

물론 이 숫자만 보고 "Rust로 다 갈아엎자"고 하는 건 다른 종류의 위험이다. 9년 연속 1위라는 신호의 *그늘*도 함께 봐야 한다. 같은 2024 State of Rust 보고서에서 응답자의 27%는 *컴파일 시간이 큰 문제*라고 답했고, 41.6%는 *언어 복잡성*에 우려를 표했다.[^6] 학습 곡선이 가파르다는 사실은 누구도 부정하지 않는다. 그래서 이 책의 목소리는 처음부터 끝까지 정직해야 한다. *"마법으로 학습 곡선을 줄여주는 책이 아니다. 4~6개월의 동반이다."*

## JVM 개발자가 Rust에서 가장 먼저 실감하는 두 가지

수치와 사례 사이에 *체감의 풍경*을 한 번 끼워 넣자. JVM 백엔드 개발자가 Rust로 한 달 정도 코드를 짜본 뒤에 가장 자주 토로하는 게 *두 가지*다.

첫째, *컴파일러가 잡아주는 양이 압도적으로 많아진다*. Spring 코드를 짤 때 IntelliJ가 빨간 줄로 잡아주는 것과는 차원이 다르다. 변수의 사용 시점, 가변성, 동시 접근, 메모리 lifetime, 에러 가능성, 타입 일치까지 *모든 것을 컴파일러가 한 번에 본다*. 십 년 동안 NPE와 ConcurrentModificationException과 ClassCastException을 *런타임에 받아왔던 사고*들이 *빌드 단계에서 멈춘다*. *처음에는 답답하지만, 두 달쯤 지나면 마약 같다*는 표현이 자주 나온다.

둘째, *그 대가로 컴파일러와의 "대화"가 잦아진다*. 처음 한 달은 *"왜 이게 컴파일이 안 되지?"*라는 질문이 매일 떨어진다. *"borrow checker와의 싸움"*이 일상이 된다.[^16] 컴파일러가 거부하는 코드 하나를 통과시키느라 한 시간이 가는 일이 흔하다. 이 답답함을 어떻게 견딜 것인가? 가장 자주 인용되는 처방이 *"borrow checker를 적이 아니라 동료(co-author)로 받아들이자"*다. 처음에는 *까다로운 시니어처럼* 느껴지지만, *익숙해지면 그 시니어가 잡아주지 않는 코드는 오히려 불안하게* 느껴진다는 게 4년차 한국 개발자의 후기다.[^15]

이 두 가지 체감을 *건너뛰어서 가르쳐주는 책은 없다*. 이 책도 마찬가지다. 4~6개월의 답답함은 *건너뛰지 않고 함께 통과*한다. 그 통과를 가능한 한 매끄럽게 해주는 게 이 책의 역할이다.

## 사례 네 개 — 이미 우리 옆에 와 있다

추상적인 신호만으로는 마음이 잘 움직이지 않는다. 구체적인 사례를 보자. JVM 백엔드 개발자라면 한 번쯤 들어봤을 회사들의 이름이다.

**Discord**는 자사의 Read States 서비스(어떤 채널의 어느 메시지까지 읽었는지를 추적하는 서비스)를 Go에서 Rust로 옮겼다.[^7] 원래 Go 버전에서는 GC가 약 2분마다 동작하면서 10~40ms의 tail latency 스파이크가 났다. 메시지를 열 때마다 사용자가 잠깐씩 멈춤을 느끼는 셈이었다. Rust로 옮긴 결과? LRU 캐시에서 evict될 때 메모리가 즉시 해제되어 평균 응답시간이 ms에서 μs로 떨어졌고, 스파이크가 사라졌다. *"GC가 없어서 좋다"*는 추상적인 말의 구체적인 모양이 이것이다.

**Cloudflare**는 자사 인터넷 인프라의 핵심인 reverse proxy를 Nginx에서 Rust 기반의 Pingora로 옮겼다.[^8] 일일 1조 건 이상의 요청을 처리하는 시스템이다. 결과는 **CPU 70% 절감, 메모리 67% 절감**. 이 숫자가 의미하는 게 무엇일까? 같은 트래픽을 처리하는 데 서버가 1/3만 있으면 된다는 뜻이다. 클라우드 비용으로 환산하면 연간 수백만 달러 단위다.

**AWS**의 서버리스 인프라(Lambda, Fargate)를 떠받치는 microVM monitor인 **Firecracker**도 Rust로 작성됐다.[^9] **125ms 미만의 시작 시간, 5MiB 미만의 메모리 footprint, 한 호스트에서 초당 150개의 microVM 생성**. AWS Lambda를 호출할 때마다 우리가 모르는 사이에 Rust가 동작하고 있다.

**Microsoft**의 Azure CTO Mark Russinovich는 신규 C/C++ 프로젝트를 금지하고 Rust를 권장한다고 공식적으로 밝혔다.[^10] Windows 커널에 `win32kbase_rs.sys` 같은 Rust 코드가 이미 들어가 있고, Azure Data Explorer의 storage layer는 35만 라인의 Rust 코드로 매일 수백 PB의 데이터를 처리한다.[^11] *2030년까지 C/C++ 코드를 모두 Rust로 옮기겠다*는 목표가 공개돼 있다.

여기서 잠깐 균형을 잡자. 위 사례들이 보여주는 게 *"Rust로 모든 걸 갈아엎으라"*는 메시지일까? 아니다. 자세히 보면 모두 *hot path*에 대한 이야기다. Discord의 Read States, Cloudflare의 reverse proxy, AWS의 microVM monitor, Microsoft의 커널·storage layer. 비즈니스 로직 전체를 옮긴 사례가 아니다. 즉 이 책의 메시지도 같다. *"Spring을 버리자"*가 아니라, *"Spring 옆에 Rust를 한 자리 둘 만한 이유가 생겼다"*다.

## JVM이 풀려는 갭, Rust가 이미 풀어둔 갭

물론 JVM 진영도 손 놓고 있지 않았다. Java 21의 Virtual Thread가 등장하면서 *"가벼운 동시성"*에 대한 답이 한 발 진보했고, GraalVM Native Image는 *"빠른 시작과 작은 메모리 footprint"*라는 갭을 정조준한다. Spring Boot 3.x는 GraalVM 친화적인 AOT 컴파일을 표준으로 받아들였다. 이 흐름은 우리 모두에게 반갑다.

그렇다면 Rust는 그 진보들을 본 뒤에도 여전히 매력적인가? 답은 *"풀려는 갭이 다르다"*다. GraalVM Native Image는 *런타임 효율*(빠른 시작, 작은 메모리)을 풀지만, *메모리 안전성*은 여전히 JVM의 GC에 의존한다. 즉 GC가 사라지진 않는다. 단지 AOT로 미리 컴파일됐을 뿐이다. Reflection이나 dynamic proxy를 쓰는 코드는 깨질 수 있다는 trade-off가 따라오고, AOT 빌드 시간은 폭증한다. Virtual Thread는 *동시성*을 풀지만, *데이터 레이스*를 컴파일 타임에 막아주지는 않는다. 여전히 `synchronized`나 `AtomicReference`를 직접 챙겨야 한다.

Rust는 그 두 갭을 *함께* 풀어둔 언어다. GC 없이 결정적으로 메모리를 해제하면서, 데이터 레이스를 컴파일러가 거부한다. 시작 시간은 즉시이고, 메모리는 한 자릿수 MB로 시작한다. *그 대가*는 4~6개월의 학습 곡선이다. JVM 진영의 답들은 *기존 자산을 유지하면서 점진적으로* 갭을 메우는 길이고, Rust는 *새 언어로 한 번에* 두 갭을 푸는 길이다. 둘 중 하나가 우월하다는 말이 아니다. *어느 길로 갈 것인지를 의식적으로 선택할 만한 시점이 됐다*는 말이다.

## 이 책의 자리 — 시장의 빈자리를 채운다

여기서 가장 솔직한 질문을 던져보자. *"이미 한국어 Rust 책이 있는데, 왜 또 한 권을 쓰는가?"* 시장에 어떤 책들이 있는지부터 보자.

『러스트 프로그래밍 언어』(rinthel 한국어 번역, 공식 doc.rust-kr.org에서 무료로 읽을 수 있다)는 Rust 공식 문서의 한국어판이다.[^12] *언어 표준의 결정판*이고, Rust로 일하려는 사람이라면 책장에 한 권 있어야 한다. 하지만 이 책은 *언어 자체*를 처음부터 끝까지 가르치는 책이다. JVM 출신이라는 전제가 없다. Spring 카운터파트와의 비교가 없다.

『프로그래밍 러스트』(O'Reilly)는 시스템 프로그래밍의 깊이를 다루고, 『러스트 인 액션』(Manning)은 시스템 코드 연습 중심이다. *Hands-on Rust*는 게임을 만들면서 배운다. 모두 좋은 책이지만, *"내일 출근해서 axum + sqlx로 결제 API를 짜야 하는 Spring 시니어"*에게 직선으로 가는 책은 아니다.

한국어 출간물 중에서는 『LUVIT 실전 백엔드 러스트 Axum 프로그래밍』(제이펍)이 axum 사용법을 정면으로 다룬다.[^13] 이 책 역시 좋은 자료다. 다만 axum 사용법에 집중하기 때문에 *"왜 이 코드가 Spring의 그것과 다른 모양이 되는가"*, *"sqlx의 컴파일 타임 검증이 JPA의 어떤 함정을 잡아주는가"*, *"폴리글랏 아키텍처에서 JNI/Panama로 어떻게 잇는가"* 같은 *비교축*이 책의 중심에 있지는 않다.

이 책의 자리는 거기다. *JVM 출신만이 알 수 있는 닻*에 새 개념을 묶어 가르치는 책. 매 챕터마다 *"이건 Spring의 무엇과 같고, Spring의 무엇과 다른가"*를 시그니처로 박는다. 16개 챕터 모두에 *JVM 대응물 매핑*이 들어 있다. 빠지는 챕터가 없다.

이 책이 채우려는 빈자리를 한 줄로 표현하면 이렇다. *"이미 잘 알고 있는 것에 닻을 내려, 새 개념을 옮겨 심는 책."* 동반자적 어조로 4~6개월의 여정을 같이 걷는 책. 그게 이 책이 약속하는 것이다.

## 약속과 약속이 아닌 것

여정에 들어가기 전에 약속을 분명히 하자. 약속하는 것부터다.

이 책을 끝까지 읽고 손으로 따라 코드를 짜본다면, 출구에서는 다음을 할 수 있게 된다. cargo로 새 프로젝트를 만들고, 워크스페이스로 도메인을 분리하고, axum으로 HTTP 핸들러를 짜고, sqlx로 컴파일 타임에 검증된 SQL을 실행하고, tokio로 비동기 동시성을 다루고, tracing-opentelemetry로 분산 추적을 붙이고, musl + distroless로 8MB 컨테이너를 만들고, JNI나 Project Panama로 기존 Spring 시스템과 잇는 폴리글랏 아키텍처를 설계할 수 있다. 모든 챕터에서 *Spring의 어느 도구가 어떻게 옮겨오는지*를 함께 본다. *입장 상태*가 "JVM 베테랑이지만 Rust는 모르는 개발자"라면, *출구 상태*는 "JVM 시스템 옆에 Rust 사이드카나 hot path를 직접 만들어 출시할 수 있는 폴리글랏 백엔드 개발자"다.

다음으로 약속하지 *않는* 것이다. 첫째, 이 책은 *"JVM을 떠나라"*고 말하지 않는다. corrode의 Rust 마이그레이션 가이드는 4~6개월의 적응 기간을 권하면서도 동시에 *"전부 Rust로 갈아엎기는 거의 모든 사례에서 권장되지 않는다"*고 못 박는다.[^14] 이 책의 결론도 같다. Spring/Kotlin은 비즈니스 로직과 빠른 개발 사이클에 여전히 강하다. Rust는 *그 옆에 추가되는 무기*다. 16장 마지막 절은 그 결론에 한 번 더 닿는다.

둘째, 이 책은 *마법으로 학습 곡선을 줄여주지 않는다*. corrode의 표현을 빌리면 *"Plan 4-6 months for your engineers to get comfortable with Rust"*다.[^14] borrow checker와의 첫 한 달은 답답하다. 두 달째에 패턴이 보이기 시작하고, 석 달째에 손가락이 익는다. 4~6개월이 지나면 *"한 번 컴파일이 통과하면 정말 잘 작동한다"*는 4년차 한국 개발자의 후기에 공감하게 된다.[^15] 이 책의 역할은 그 곡선을 *없애는* 것이 아니라 *함께 걷는* 것이다.

마지막으로 한 가지. 이 책은 *Rust 표준 라이브러리 레퍼런스가 아니다*. 모든 함수와 메서드를 망라하지 않는다. 그건 공식 문서가 더 잘 한다. 이 책은 *시야의 책*이다. *"이 도구가 Spring의 무엇에 해당하고, 어떤 함정에 빠지지 말아야 하며, 4~6개월 뒤에 어떤 풍경에 도달하게 되는가"*를 보여주는 책이다.

## 마무리 — 첫 한 걸음을 위한 작은 약속

지금 이 챕터를 닫으면서, 한 가지를 함께 약속하자. 이 책은 *읽기만 하는 책이 아니라 손으로 따라 짜는 책*이다. 다음 챕터부터 매장 끝에는 "함께 해보자" 절이 붙는다. 거기서 짜는 작은 코드가 다음 장에서 다시 호출된다. 그 작은 누적이 4~6개월 뒤의 풍경을 만든다.

기억해두자. *Rust는 JVM의 적이 아니다.* GraalVM도, Virtual Thread도, Loom도 같은 방향을 다른 길로 가고 있다. 우리가 하는 일은 *그 흐름의 한 갈래에 한 발을 더 들이는 것*이다. 4~6개월 뒤, 자기 회사의 hot path에 Rust 사이드카를 한 개 띄워 운영 알림을 한 카테고리쯤 줄였다면, 이 책의 약속은 지켜진 것이다.

다음 챕터로 가기 전에 짧은 숙제 하나. 자기 회사의 가장 최근 운영 사고 1건을 떠올려 보자. NPE였는가? deadlock이었는가? memory leak이었는가? 슬랙에 떴던 그 알림 한 줄을 머릿속에서 꺼내 한 단락으로 적어두자. *Rust가 그 사고를 컴파일 타임에 잡았을지, 잡았다면 어떻게 잡았을지*를 짧게 메모해두자. 이 메모는 이 책의 7장(Result/Option, 예외 없이 에러 다루기), 9장(Send/Sync, 데이터 레이스 막기), 10장(async와 데드락) 세 군데에서 다시 펼치게 된다. 그때마다 *"아, 이래서 그 사고가 잡혔겠구나"* 또는 *"아, 이건 Rust로도 못 잡겠구나"*를 손에 묻혀가며 읽으면, 책이 끝날 즈음에는 자기 시스템에 대한 새로운 시야가 생겨 있을 것이다.

## 함께 해보자

자기 회사(또는 사이드 프로젝트)에서 *최근 한 달 사이* 발생한 운영 사고 1건을 떠올려 다음 양식으로 한 단락 메모를 남겨보자.

- *사고 한 줄 요약*: 무엇이, 언제, 어떤 시스템에서 났는가.
- *분류*: NPE / deadlock / race condition / memory leak / OOM / 그 외.
- *근본 원인*: 한 줄로.
- *Rust 가설*: 같은 코드를 Rust로 짰다면 컴파일 타임에 잡혔을까? 그렇다면 어떤 도구가? (지금은 답이 없어도 좋다. 7장·9장·10장에서 다시 본다.)

이 메모를 책의 첫 페이지나 README에 붙여두자. 7장 마지막 절, 9장 마지막 절, 10장 마지막 절에서 *"1장에서 적어둔 그 사고"*로 다시 부른다. 그때마다 한 줄씩 답을 채워가자.

다음 장에서는 입에 쓴 약을 마시기 전에 입에 단 사탕부터 하나 물자. *"5분 만에 첫 Rust 바이너리를 손에 쥐는 경험"*이다. cargo가 Maven/Gradle/Sonar/Spotless를 모두 안고 있는 그 감각을 먼저 묻혀보자.

---

## 참고

[^1]: White House ONCD, ["Back to the Building Blocks: A Path Toward Secure and Measurable Software" (2024-02)](https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/02/Final-ONCD-Technical-Report.pdf).
[^2]: NSA, ["Memory Safe Languages: Reducing Vulnerabilities in Modern Software Development" (2025-06)](https://media.defense.gov/2025/Jun/23/2003742198/-1/-1/0/CSI_MEMORY_SAFE_LANGUAGES_REDUCING_VULNERABILITIES_IN_MODERN_SOFTWARE_DEVELOPMENT.PDF).
[^3]: ["Microsoft's Rust Bet — From Blue Screens to Safer Code" — The New Stack](https://thenewstack.io/microsofts-rust-bet-from-blue-screens-to-safer-code/).
[^4]: ["2024 State of Rust Survey Results" — Rust Blog (2025-02)](https://blog.rust-lang.org/2025/02/13/2024-State-Of-Rust-Survey-results/); ["Survey: Memory-Safe Rust Gains 45% of Enterprise Development" — The New Stack](https://thenewstack.io/survey-memory-safe-rust-gains-45-of-enterprise-development/).
[^5]: ["2025 Stack Overflow Developer Survey"](https://survey.stackoverflow.co/2025/).
[^6]: ["Rust 2025 Survey: 45.5% Adoption, 41.6% Worry Complexity" — byteiota](https://byteiota.com/rust-2025-survey-45-5-adoption-41-6-worry-complexity/); ["Rust compiler performance survey 2025 results" — Rust Blog](https://blog.rust-lang.org/2025/09/10/rust-compiler-performance-survey-2025-results/).
[^7]: ["Why Discord is switching from Go to Rust" — Discord Blog](https://discord.com/blog/why-discord-is-switching-from-go-to-rust).
[^8]: ["How we built Pingora, the proxy that connects Cloudflare to the Internet" — Cloudflare Blog](https://blog.cloudflare.com/how-we-built-pingora-the-proxy-that-connects-cloudflare-to-the-internet/).
[^9]: ["Firecracker microVMs"](https://firecracker-microvm.github.io/); ["Firecracker — Open Source Secure Fast microVM Serverless" — AWS Open Source Blog](https://aws.amazon.com/blogs/opensource/firecracker-open-source-secure-fast-microvm-serverless/).
[^10]: ["Russinovich: Microsoft is 'All-in' on Rust" — Thurrott](https://www.thurrott.com/dev/317950/russinovich-microsoft-is-all-in-on-rust).
[^11]: ["Microsoft's Rust Bet" — The New Stack](https://thenewstack.io/microsofts-rust-bet-from-blue-screens-to-safer-code/); ["Microsoft is rewriting core Windows libraries in Rust" — The Register](https://www.theregister.com/2023/04/27/microsoft_windows_rust/).
[^12]: [The Rust Programming Language 한국어판 (rinthel)](https://rinthel.github.io/rust-lang-book-ko/), [공식 doc.rust-kr.org](https://doc.rust-kr.org/).
[^13]: [Indo Yoon, "실전 백엔드 러스트 Axum 프로그래밍 — 책 소개"](https://devbull.xyz/blog/axum-book).
[^14]: ["Migrating from Java to Rust" — corrode](https://corrode.dev/learn/migration-guides/java-to-rust/).
[^15]: ["4년간의 Rust 사용 후기" — blog.cro.sh](https://blog.cro.sh/posts/four-years-of-rust/).
[^16]: ["Rust's Learning Curve: Community Debates Borrow Checker and Lifetime Complexity" — BigGo News](https://biggo.com/news/202502181925_rust-learning-curve-debate); ["Rust ownership and borrows: Fighting the borrow-checker" — DEV.to](https://dev.to/daaitch/rust-ownership-and-borrows-fighting-the-borrow-checker-4ea3).

---

# 2장. 첫 만남 — cargo로 5분 만에 빌드하기

새 언어를 배울 때 가장 먼저 부딪히는 벽이 무엇일까? 문법이 아니다. *환경 구성*이다. 회사에서 새 프로젝트를 시작할 때를 떠올려보자. JDK 버전을 깔고, IntelliJ를 깔고, Maven 또는 Gradle을 설정하고, `pom.xml`이나 `build.gradle.kts`를 채우고, 코드 포매터(Spotless, google-java-format)를 붙이고, 정적 분석 도구(SpotBugs, Sonar)를 CI에 끼워 넣는다. *Hello World 한 줄*을 화면에 띄우기까지 한나절이 가는 일이 흔하다. 처음 학습할 때 가장 사기를 떨어뜨리는 게 바로 이 *세팅의 늪*이다.

그렇다면 Rust는 어떨까? 다행스럽게도 *완전히 반대편*에 있다. 도구 한 개로 끝난다. 이름이 cargo다. 이 챕터에서는 cargo로 첫 바이너리를 빌드하는 데까지 걸리는 시간이 정말로 *5분*이라는 것을 손으로 확인해보자. 그리고 그 5분 사이에 Maven/Gradle/Sonar/JMH/picocli/Spotless가 한 도구 안에 어떻게 들어와 있는지를 같이 알아보자.

## rustup — sdkman의 감각으로 toolchain을 다루자

먼저 Rust 자체를 깔아야 한다. 자바 진영에서 sdkman을 써본 적이 있는가? 여러 JDK 버전을 한 명령으로 전환하는 그 도구다. Rust에서 그 역할을 하는 게 rustup이다. rustup은 *toolchain manager* — 즉 컴파일러(rustc)와 표준 라이브러리, cargo, rustfmt, clippy 같은 도구 묶음을 버전별로 설치·전환하는 매니저다.

설치는 한 줄이다. macOS나 Linux라면 다음 명령을 셸에 붙여넣자.

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

윈도우는 [rustup.rs](https://rustup.rs/)에서 인스톨러를 받으면 된다. 설치가 끝나면 `~/.cargo/bin`이 PATH에 들어간다. 셸을 새로 열거나 `source ~/.cargo/env`로 환경을 적용한 뒤 확인해보자.

```bash
$ rustc --version
rustc 1.83.0 (90b35a623 2025-11-26)
$ cargo --version
cargo 1.83.0 (5ffbef321 2025-10-29)
```

이 두 줄이 떴다면 Rust 환경은 이미 끝났다. JDK 설치 후 `JAVA_HOME`을 잡고 IntelliJ에서 SDK를 등록하던 그 모든 절차가 *한 명령*으로 끝났다. *조금 허무할 정도다*.

toolchain 채널은 세 가지가 있다. *stable*(6주마다 정식 릴리즈), *beta*(다음 stable 후보), *nightly*(매일 빌드, 실험적 기능 활성화). 처음 시작하는 우리에게는 stable이 답이다. 일부 라이브러리(특히 임베디드, 컴파일러 플러그인)는 nightly 기능을 요구하기도 하는데, 그땐 다음처럼 채널을 토글한다.

```bash
$ rustup toolchain install nightly
$ rustup default stable          # 디폴트는 stable로 두자
$ rustup run nightly cargo build # 가끔 nightly가 필요할 때만
```

프로젝트 디렉터리에 `rust-toolchain.toml` 파일 하나를 두면 그 폴더에서는 자동으로 정해진 toolchain이 쓰인다.

```toml
# rust-toolchain.toml
[toolchain]
channel = "1.83.0"
components = ["rustfmt", "clippy"]
```

이 파일이 sdkman의 `.sdkmanrc`처럼 *"이 프로젝트는 이 버전으로 빌드한다"*는 약속을 코드 옆에 박아둔다. 신규 멤버가 합류해도 `cargo build` 한 번이면 똑같은 toolchain이 자동으로 설치된다. Maven/Gradle wrapper의 `mvnw`/`gradlew`가 하는 일을 *언어 레벨*에서 처리한다고 생각하면 이해하기 쉽다.

## cargo new — 5분의 시작

이제 본격적으로 첫 프로젝트를 만들어보자. 작업 디렉터리에서 다음을 친다.

```bash
$ cargo new hello-jvm
     Created binary (application) `hello-jvm` package
$ cd hello-jvm
$ tree -a
.
├── .git
├── .gitignore
├── Cargo.toml
└── src
    └── main.rs
```

이게 끝이다. Maven archetype으로 새 프로젝트를 뽑을 때 디렉터리 트리가 한 화면을 채우던 풍경과 비교해보자. *눈물이 날 정도로 단순하다*. 그리고 `git init`까지 알아서 해준다. `.gitignore`에 `/target`이 이미 들어 있다(target은 cargo가 빌드 산출물을 떨어뜨리는 폴더, Maven의 `target/`이나 Gradle의 `build/`와 같다).

`src/main.rs`를 열어보자.

```rust
fn main() {
    println!("Hello, world!");
}
```

이게 자동 생성된 본문 전부다. 한번 돌려보자.

```bash
$ cargo run
   Compiling hello-jvm v0.1.0 (/path/to/hello-jvm)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello-jvm`
Hello, world!
```

여기까지 걸린 시간이 *얼마나 됐는지* 시계를 한번 보자. rustup 설치 1~2분, `cargo new`와 `cargo run`이 1분 이내. 5분이라는 약속이 결코 과장이 아니다.

본문을 살짝 바꿔보자. JVM 출신답게 `"Hello, JVM"`을 외쳐보자.

```rust
fn main() {
    let runtime = "JVM";
    println!("Hello, {runtime}! Now we have one more weapon: Rust.");
}
```

다시 `cargo run`을 친다.

```
Hello, JVM! Now we have one more weapon: Rust.
```

이 한 문장이 곧 이 책 전체의 메시지다. *"JVM을 떠나는 게 아니라, 무기를 하나 더 얹는다."*

## Cargo.toml을 한 줄씩 해부해보자

자동 생성된 `Cargo.toml`을 열어보자.

```toml
[package]
name = "hello-jvm"
version = "0.1.0"
edition = "2024"

[dependencies]
```

짧다. 그런데 이 짧은 파일이 `pom.xml` 또는 `build.gradle.kts`가 하던 일의 *대부분*을 한다. 한 줄씩 보자.

`[package]` 섹션은 메타데이터다. `name`, `version`은 Maven의 `artifactId`, `version`과 의미가 같다. 그룹id에 해당하는 *namespace는 없다*. crates.io에서는 이름이 globally unique이기 때문이다. 그래서 처음 라이브러리를 출판할 때는 *이름 선점 전쟁*이 살짝 벌어지기도 한다(이 점이 Maven Central의 그룹id 모델과 가장 다른 부분이다).

`edition`은 *Rust 언어 자체의 호환성 묶음*이다. 2015 / 2018 / 2021 / 2024 네 개가 있고, edition을 올리면 새 키워드(`async`, `dyn` 등의 의미 변화)가 활성화된다. JVM에 비유하자면 `pom.xml`의 `<source>21</source>`/`<target>21</target>`에 가까운 개념인데, *언어 호환성 정책*이 더 명시적이다. 새 프로젝트는 가장 최신 edition을 쓰는 편이 낫다.

`[dependencies]` 섹션이 비어있다. 의존성이 없는 상태다. 한번 채워보자. CLI 인자를 파싱하는 라이브러리 `clap`을 추가해보자.

```toml
[dependencies]
clap = { version = "4", features = ["derive"] }
```

이게 Maven의 `<dependency>` XML 다섯 줄이 하던 일이다. `version = "4"`는 semver(semantic versioning)로 *4.x.y 중 호환되는 최신*을 뜻한다. Cargo는 semver를 매우 강하게 따른다. 메이저 버전이 다르면 *별개의 라이브러리로 취급*해서 한 그래프 안에 동시에 넣어준다(JVM 진영에서 이걸 못 해서 발생하는 *jar hell*과 가장 큰 차이점). `features`는 그 라이브러리의 *옵션 기능*을 켠다는 뜻인데, 잠시 후에 더 다룬다.

`Cargo.toml`을 저장한 뒤 다시 `cargo build`를 친다.

```bash
$ cargo build
    Updating crates.io index
  Downloaded clap v4.5.20
  Downloaded clap_derive v4.5.18
  ... (여러 개)
   Compiling proc-macro2 v1.0.92
   Compiling quote v1.0.37
   Compiling syn v2.0.90
   ...
   Compiling clap v4.5.20
   Compiling hello-jvm v0.1.0
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 12.34s
```

전이 의존성이 자동으로 받아진다. `crates.io`에서 다운로드해서 `target/`에 빌드하고, 우리 프로젝트와 링크한다. Maven Central에서 jar를 받아 `~/.m2/repository`에 캐시하던 그 흐름과 같다. cargo는 `~/.cargo/registry`에 같은 일을 한다.

빌드 산출물을 보자.

```bash
$ ls target/debug/hello-jvm
target/debug/hello-jvm
$ file target/debug/hello-jvm
target/debug/hello-jvm: Mach-O 64-bit executable arm64
```

*하나의 정적 바이너리*다. JAR 파일이 아니라 *OS가 직접 실행하는 실행 파일*이다. 이 점이 운영에서 가장 큰 차이를 만든다(자세한 것은 14장에서 본다). 지금은 그저 *"실행 파일이 한 개로 떨어진다"*는 사실만 손에 묻혀두자.

## semver와 feature flag — 의존성 관리의 두 핵심

`clap = { version = "4", features = ["derive"] }`라고 적은 한 줄을 좀 더 깊게 보자.

semver 표기는 다음 네 가지가 자주 쓰인다.

```toml
clap = "4.5.20"           # 4.5.20과 호환되는(>=4.5.20, <5.0.0) 모든 버전
clap = "=4.5.20"          # 정확히 4.5.20만
clap = "^4.5.20"          # "4.5.20"과 동일 (캐럿이 디폴트)
clap = "~4.5.20"          # 4.5.x만 (4.6은 거부)
```

Maven/Gradle에서 `4.5.20`이라고 쓰면 *그 버전만* 받지만, Cargo의 `4.5.20`은 *4.x 호환 범위*를 의미한다. 기본 가정이 정반대다. *처음에 가장 많이 헷갈리는 지점*이다. 정확한 버전 고정이 필요하면 `=4.5.20`을 명시해야 한다. 다만 *실제로는 신경 쓸 필요가 거의 없다*. cargo가 `Cargo.lock` 파일에 *실제 빌드된 정확한 버전*을 박아두기 때문이다(Gradle의 `gradle.lockfile`과 같은 역할). 신규 멤버가 같은 lock으로 빌드하면 같은 버전이 깔린다.

`features`는 *코드 레벨의 conditional compile*이다. 이 점이 Maven profile이나 Gradle variant와 결정적으로 다르다. Maven profile은 *어떤 모듈을 빌드에 포함할지*를 고르는 정도지만, Cargo feature는 *라이브러리 내부의 어떤 코드 경로를 컴파일할지*를 토글한다. 예를 들어 `clap`의 `derive` feature를 끄면 `#[derive(Parser)]` 같은 매크로 지원 코드가 *통째로 바이너리에서 빠진다*. 결과: 바이너리가 작아지고 컴파일도 빨라진다.

자기 라이브러리에서 feature를 정의할 수도 있다.

```toml
[features]
default = ["postgres"]
postgres = ["sqlx/postgres"]
mysql = ["sqlx/mysql"]
metrics = ["prometheus"]
```

코드에서는 다음처럼 분기한다.

```rust
#[cfg(feature = "postgres")]
mod postgres_repo;

#[cfg(feature = "mysql")]
mod mysql_repo;
```

*Maven profile이 어쩌다 한 번 손대는 그늘진 영역*이라면, Cargo feature는 *일상 도구*다. 다만 워크스페이스에서 같은 의존성이 다른 feature 조합으로 두 번 등장하면 *unification 함정*이 생긴다(13장에서 자세히 본다). 그때 `resolver = "2"`라는 한 줄이 처방인데, 새 프로젝트의 디폴트가 이미 `2`이므로 보통은 신경 쓸 필요가 없다.[^1]

## cargo의 일상 명령들 — 한 도구가 다 한다

cargo의 진짜 매력은 *개발 사이클의 모든 동작이 한 도구로 끝난다*는 점이다. 자주 쓰는 명령을 모아보자.

```bash
$ cargo new <name>                   # 새 binary 프로젝트
$ cargo new --lib <name>             # 새 library 프로젝트
$ cargo build                         # 디버그 빌드
$ cargo build --release              # 릴리즈 빌드 (최적화 on)
$ cargo run                           # 빌드 + 실행
$ cargo run -- arg1 arg2             # 인자 전달
$ cargo test                          # 모든 테스트 실행
$ cargo test some_function           # 이름 매칭 테스트만
$ cargo check                         # 컴파일 검증만 (실행 파일 X) — 빠르다
$ cargo clippy                        # 정적 분석 (린터)
$ cargo fmt                           # 포매터
$ cargo doc --open                    # 문서 빌드 + 브라우저로 열기
$ cargo bench                         # 벤치마크 (criterion 등 필요)
$ cargo update                         # 의존성 lock 갱신
$ cargo tree                          # 의존성 트리 출력
$ cargo install <crate>              # 글로벌 CLI 도구 설치
```

이 표를 가만히 보면 *충격적인 사실 하나*가 보인다. JVM 진영에서 `mvn` 또는 `gradle`로 빌드를 하고, IntelliJ에서 테스트를 돌리고, JaCoCo로 커버리지를 재고, Spotless로 포매팅을 하고, SpotBugs/Sonar로 정적 분석을 하고, JMH로 벤치마크를 하고, JavaDoc으로 문서를 만들고, picocli로 CLI를 짜고, OWASP Dependency Check으로 취약점을 스캔하던 *그 모든 도구*가 cargo 한 곳에 모여 있다.

물론 cargo 안에 들어 있지 않은 일도 있다(예: 컨테이너 이미지 빌드). 하지만 *언어와 가장 가까운 영역*은 거의 다 cargo가 안고 있다. 신규 멤버가 합류했을 때 *"우리 회사는 어떤 도구를 쓰나요?"*라는 질문이 *없다*. 답이 그냥 *"cargo"*다. 이게 *체감으로 가장 큰 차이*다.

자주 잊지 말아야 할 명령 하나가 `cargo check`다. *컴파일 가능성만 검증하고 실행 파일은 만들지 않는* 명령인데, *cargo build보다 훨씬 빠르다*. IDE의 rust-analyzer가 매번 백그라운드에서 돌리는 게 사실 `cargo check`다. 코드를 짜면서 *"이게 컴파일되나?"*만 확인하고 싶을 때 자주 쓰는 편이 낫다.

## workspace 미리보기 — Gradle multi-module의 감각

이 책의 후반부에서는 한 프로젝트를 *여러 crate로 쪼개는* 패턴을 자주 본다(13장에서 본격적으로 다룬다). 이걸 cargo에서는 *workspace*라고 부른다. 미리 한 번만 모양을 봐두자.

```
my-service/
├── Cargo.toml          # 워크스페이스 루트
├── crates/
│   ├── domain/
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   ├── infra/
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   └── web/
│       ├── Cargo.toml
│       └── src/main.rs
└── target/             # 모든 crate가 공유
```

루트 `Cargo.toml`은 다음처럼 쓴다.

```toml
[workspace]
resolver = "2"
members = ["crates/domain", "crates/infra", "crates/web"]

[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
```

각 멤버 crate의 `Cargo.toml`에서는 다음처럼 부모 워크스페이스의 의존성을 *상속*한다.

```toml
[dependencies]
tokio = { workspace = true }
serde = { workspace = true }
domain = { path = "../domain" }
```

Gradle multi-module을 써본 사람이라면 패턴이 그대로 보일 것이다. 다만 *세팅이 한 줄로 끝난다*. `settings.gradle.kts` + `build.gradle.kts` × N + 버전 카탈로그를 짜던 일이 *Cargo.toml 몇 줄*이 된다. 이 단순함이 cargo의 진짜 매력이다.[^2]

지금 단계에서는 *"이런 모양이 가능하다"* 정도만 손에 담아두자. 13장에서 axum + sqlx 서비스를 도메인/인프라/웹 crate로 쪼갤 때 다시 펼친다.

## IDE 셋업 — 세 가지 선택지

코드를 손으로 짜기 시작하기 전에 IDE 환경을 한 번만 정리하자. 선택지는 셋이다.

**VSCode + rust-analyzer.** 가장 가볍고, 가장 활발히 발전 중이다. VSCode 마켓플레이스에서 `rust-analyzer` 확장을 설치하면 끝이다. *내 추천*은 처음 시작하는 사람에게 이쪽이다. rust-analyzer가 *백그라운드에서 cargo check를 돌리며* 실시간으로 에러·경고를 보여준다. type inline hint(타입을 추론한 결과를 회색으로 표시)와 *enum match exhaustiveness*도 즉시 잡아준다. 무료다.

**RustRover (JetBrains).** IntelliJ에 익숙한 사람에게 가장 친근한 선택. 별도 IDE로 분리됐다(과거엔 IntelliJ Rust 플러그인이었다). 디버거 통합이 가장 매끈하고, refactoring·navigation의 깊이가 깊다. JetBrains 라이센스가 있다면 첫 후보다.

**IntelliJ IDEA + Rust 플러그인.** 위와 비슷하지만 IDEA 본체에 얹는 형태. 이미 IDEA를 메인으로 쓰는 사람에게 자연스럽다.

어떤 IDE를 쓰든 *공통적으로* 한 번에 켜두면 좋은 것이 있다. *저장 시 자동 포매팅*과 *clippy 경고 표시*다. VSCode라면 settings.json에 다음을 넣자.

```json
{
  "rust-analyzer.checkOnSave.command": "clippy",
  "[rust]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "rust-lang.rust-analyzer"
  }
}
```

이 두 줄이 *지속 가능한 코드 품질*의 시작점이다. clippy가 보여주는 경고를 실시간으로 보면서 짜면, *처음 한 달*의 코드 품질이 비약적으로 좋아진다. 일종의 *친절한 시니어 페어*가 옆에 앉아 있는 셈이다.

## 사전 커밋 훅 — 팀 합류 첫날의 약속

마지막으로 한 가지 권하고 싶은 게 있다. *사전 커밋 훅*이다. 새로 합류한 팀원의 코드가 빌드를 망가뜨리거나, 포맷이 어긋나거나, clippy 경고가 잔뜩 들어오는 일을 *원천 차단*하는 장치다. JVM 진영에서 husky + lint-staged나 pre-commit framework를 써본 사람이라면 익숙할 것이다.

가장 단순한 형태는 `.git/hooks/pre-commit`에 다음 한 줄을 넣는 것이다.

```bash
#!/bin/bash
set -e
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

`-D warnings`는 *clippy의 경고를 에러로 격상*시킨다. 즉 경고가 한 개라도 있으면 빌드가 깨진다. 처음엔 답답하게 느껴질 수 있지만, *깨끗한 코드베이스를 유지하는 가장 단순한 처방*이다. 이 동일한 명령을 CI에서도 똑같이 돌리면, *"내 머신에선 되는데"*라는 익숙한 변명이 사라진다.

팀 단위로는 [pre-commit framework](https://pre-commit.com/) 또는 cargo의 `.cargo/config.toml`로 좀 더 정교하게 관리할 수 있다. 다만 처음에는 위의 세 줄짜리 훅으로 충분하다. *기억해두자. 처음 한 달의 풍경을 만드는 건 이 작은 훅 하나다.*

## crates.io — Maven Central의 자리

마지막으로 *어디서 라이브러리를 찾는가*를 짧게 짚어두자. Maven Central에 해당하는 게 [crates.io](https://crates.io/)다. 검색하면 다운로드 수, 최근 업데이트, README, dependents가 한 화면에 보인다. 살펴볼 만한 핵심 라이브러리들의 위치만 미리 알아두자.

- **tokio** — 비동기 런타임 (10장).
- **axum** — HTTP 프레임워크 (11장).
- **sqlx / sea-orm / diesel** — 데이터베이스 (12장).
- **serde / serde_json** — 직렬화 (어디서나).
- **tracing / tracing-subscriber / tracing-opentelemetry** — 관측 (14장).
- **anyhow / thiserror** — 에러 처리 (7장).
- **clap** — CLI 인자 파싱 (방금 설치).
- **reqwest** — HTTP 클라이언트.

이 정도가 Spring 백엔드의 *기본 스타터 묶음*에 해당한다고 보면 된다. *Spring Boot starter 한 줄로 끝나던 세계*와 비교하면 *직접 골라야 한다*는 부담이 있긴 하다. 하지만 그만큼 *어떤 도구를 왜 골랐는지가 코드에 남는다*. 처음엔 번거롭다. 두 달 뒤엔 *그 명시성이 운영을 살린다*.

[crates.io](https://crates.io/)와 함께 [lib.rs](https://lib.rs/), [docs.rs](https://docs.rs/)도 자주 쓴다. lib.rs는 카테고리별 큐레이션이 잘 된 미러이고, docs.rs는 *모든 crate의 문서를 자동으로 호스팅*한다. URL 패턴이 `docs.rs/{crate-name}` 한 줄로 일관돼 있다. 라이브러리 문서를 찾을 때 가장 빠른 진입점이다.

## 마무리 — 5분의 약속이 지켜졌다

이 챕터에서 한 일을 한 줄로 정리해보자. *rustup으로 toolchain을 깔고, cargo new로 프로젝트를 만들고, Cargo.toml에 의존성을 추가하고, cargo run으로 첫 바이너리를 실행했다.* 5분이라는 약속은 정직하게 지켜진 셈이다. 그리고 그 5분 사이에 cargo가 Maven, Gradle, Sonar, Spotless, JMH, picocli, JavaDoc, OWASP Dependency Check를 *모두 안고 있다*는 사실을 손에 묻혔다.

기억해두자. cargo의 진짜 매력은 단순함 그 자체가 아니다. *팀 전체가 같은 도구로 같은 절차를 따른다*는 일관성이다. 신규 멤버 합류, CI 셋업, 새 프로젝트 시작, 이 모두가 *같은 cargo 명령*으로 끝난다. 십 년 동안 Maven plugin 모음·Gradle convention plugin·Spotless config·sonar-project.properties를 회사마다 다르게 짜왔던 우리 입장에서는 *조금 어이없을 정도로 단순하다*.

다만 이 단순함이 *Rust의 학습 곡선까지 단순하게* 만들어주지는 않는다. 환경이 단순하다고 *언어가 쉬운 건 아니다*. 다음 챕터에서 곧바로 그 사실을 손으로 확인하게 된다. 변수 선언 한 줄, 함수 시그니처 하나, 모듈 가시성 한 단어가 *Java가 알던 모양과 미묘하게 다르다*. 그 미묘한 차이가 4장의 소유권으로 이어지는 다리다.

## 함께 해보자

방금 만든 `hello-jvm` 프로젝트를 한 단계 키워보자. 인자 한 개를 받아 인사하는 작은 CLI다. `Cargo.toml`은 이미 `clap`을 추가해뒀다.

`src/main.rs`를 다음처럼 바꿔보자.

```rust
use clap::Parser;

#[derive(Parser, Debug)]
#[command(name = "hello-jvm", about = "JVM 출신을 환영합니다")]
struct Args {
    /// 인사할 대상의 이름
    #[arg(short, long, default_value = "JVM 개발자")]
    name: String,

    /// 인사 횟수
    #[arg(short, long, default_value_t = 1)]
    count: u8,
}

fn main() {
    let args = Args::parse();
    for _ in 0..args.count {
        println!("Hello, {}! Now we have one more weapon: Rust.", args.name);
    }
}
```

빌드와 실행은 다음 한 줄이다.

```bash
$ cargo run -- --name "Spring 개발자" --count 3
   Compiling hello-jvm v0.1.0
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 3.21s
     Running `target/debug/hello-jvm --name 'Spring 개발자' --count 3`
Hello, Spring 개발자! Now we have one more weapon: Rust.
Hello, Spring 개발자! Now we have one more weapon: Rust.
Hello, Spring 개발자! Now we have one more weapon: Rust.
```

이 작은 CLI에서 다음 세 가지를 손으로 확인해보자.

1. `cargo run -- --help`를 쳐보자. clap이 *자동으로 도움말을 생성*한다. picocli나 Spring Shell의 그것과 비교해보자.
2. `cargo build --release`로 릴리즈 빌드를 만들어 `target/release/hello-jvm`의 *파일 크기*를 재보자. JAR 파일 크기와 비교해보자(JVM은 JRE까지 포함하면 200MB대다).
3. `Cargo.toml`의 `clap = { version = "4", features = ["derive"] }`에서 `features = ["derive"]`를 지운 뒤 `cargo build`를 시도해보자. 어떤 에러가 나는가? 그 에러를 가만히 읽어보자. *cargo의 에러 메시지가 친절하다는 사실*도 같이 묻혀두자.

이 작은 CLI는 *13장의 clap 절*에서 다시 호출되어 *완성형*으로 키워진다. subcommand, env var, completion script까지 붙여본다.

다음 장에서는 코드 자체의 모양을 정면으로 본다. `let`/`let mut`은 `val`/`var`과 어떻게 다르고, `match`는 Java 17의 switch expression과 어디가 다르며, `String`과 `&str`이 *왜 두 개*인가 — Java가 알던 모양과 살짝씩 어긋난 부분들을 같이 살펴보자.

---

## 참고

[^1]: ["Cargo Workspaces" — The Cargo Book](https://doc.rust-lang.org/cargo/reference/workspaces.html); ["cargo-features2 RFC"](https://rust-lang.github.io/rfcs/2957-cargo-features2.html); ["Cargo Workspace and the Feature Unification Pitfall" — nickb.dev](https://nickb.dev/blog/cargo-workspace-and-the-feature-unification-pitfall/).
[^2]: ["Workspaces" — The Cargo Book](https://doc.rust-lang.org/cargo/reference/workspaces.html).

---

# 3장. 변수·타입·함수·모듈 — Java가 알던 모양과 다른 부분

새 언어를 배울 때 흥미로운 단계가 하나 있다. *문법은 비슷한데 의미가 미묘하게 다른 부분*을 발견하는 단계다. 처음에는 *"어, 익숙한 모양이네"* 싶다가도, 며칠 뒤에 *"어, 이건 내가 알던 그 모양이 아니네"*가 된다. 그 미묘한 어긋남을 *모르고 지나치면* 4장의 소유권에서 컴파일러가 화를 낼 때 *왜 화를 내는지* 영문을 모르게 된다.

그래서 이 장에서는 변수, 타입, 함수, 모듈 같은 *기본 도구*를 살펴본다. 다만 단순히 문법을 나열하는 게 아니라, 매 도구마다 *"Java/Kotlin이 이걸 어떻게 표현하지?"*를 옆에 두고 비교한다. 같은 의미인데 표기가 다른 부분, 표기는 비슷한데 의미가 다른 부분, *이 두 카테고리를 분리해서 머리에 박는 게* 이 장의 목표다.

## 불변이 디폴트라는 사실의 무게

변수 선언부터 보자.

```rust
let x = 5;          // 불변
let mut y = 10;     // 가변
y += 1;             // OK
// x += 1;          // 컴파일 에러: cannot assign twice to immutable variable
```

Kotlin을 써본 사람이라면 익숙한 모양이다. `let`이 `val`이고, `let mut`이 `var`다. 그런데 잠시 멈추고 생각해보자. *왜 굳이* 이렇게 디폴트를 불변으로 잡았을까?

답은 *"변경 가능성은 명시적으로 선언할 만큼 무거운 결정"*이라는 철학이다. Java에서 `final` 키워드를 *언제 붙이는가*를 떠올려보자. 변수 한 개에 `final`을 붙이려면 두 자판을 더 쳐야 한다. 그래서 결국 *대부분의 변수가 final 없이 선언*되고, 동시성 코드에서 *어디가 진짜 가변이고 어디가 사실상 불변인지* 코드만 봐서는 알기 어려워진다. 십 년 동안 우리가 Spring 코드 리뷰에서 *"여기 final 좀 붙여주세요"*라고 잔소리해온 풍경의 본질이 그것이다.

Rust는 그 잔소리를 *컴파일러가 대신* 한다. 그것도 *반대 방향으로*. *기본은 불변이고, 가변이 필요할 때 명시*한다. 그 결과 코드를 읽을 때 `mut` 키워드가 보이는 곳이 *진짜 가변인 곳*임을 단번에 안다. 동시성·재할당 사고를 줄이는 가장 단순한 처방이다. *불변 디폴트의 무게*는 처음에는 잘 안 느껴지지만, 두 달쯤 지나면 *"왜 Java는 이걸 디폴트로 안 했지?"*라는 의문이 들기 시작한다.

또 하나 흥미로운 모양이 *shadowing*이다.

```rust
let x = 5;
let x = x + 1;          // 새 변수 x로 다시 선언, 값은 6
let x = x.to_string();  // 또 다시, 이번엔 타입까지 String으로
println!("{x}");        // 출력: "6"
```

같은 이름으로 *새 변수를 다시 선언*해서 이전 변수를 덮는 패턴이다. 가변이 아니다. 매번 *새 불변 변수*가 만들어진다. Java에선 이게 안 된다(블록 안에서는 변수명 충돌). Kotlin에서도 같은 스코프에선 안 된다. Rust는 허용한다. *왜 허용할까?* 같은 의미적 값이 *다른 형태*로 변환될 때(파싱, 역직렬화, 타입 변환) *변수명을 새로 짜내지 않아도 되도록* 풀어줬다. `let raw_input = read_stdin();` → `let parsed: i32 = raw_input.trim().parse()?;` 같은 흐름이 한 변수명으로 자연스럽게 흐른다. 처음엔 살짝 어색하지만 익숙해지면 *맘에 든다*.

## 원시 타입의 지도 — boxing이 사라진 세계

Java에서 `int`와 `Integer`의 구분에 진절머리가 났던 적이 한 번쯤 있을 것이다. `List<int>`는 못 짜고 `List<Integer>`만 짜야 했고, 그 사이의 auto-boxing/unboxing이 *NullPointerException의 새 출처*가 되곤 했다. Rust는 *boxing이 없다*. 모든 원시 타입이 그냥 *값 그대로* 다뤄진다.

기본 원시 타입들의 지도를 한번 그려보자.

| Rust 타입 | 의미 | Java 대응 |
|---|---|---|
| `i8`/`i16`/`i32`/`i64`/`i128` | signed 정수 | `byte`/`short`/`int`/`long`/(없음) |
| `u8`/`u16`/`u32`/`u64`/`u128` | unsigned 정수 | (없음 — Java는 unsigned가 없다) |
| `isize`/`usize` | 포인터 크기 정수 | (없음) |
| `f32`/`f64` | 부동소수점 | `float`/`double` |
| `bool` | 참/거짓 | `boolean` |
| `char` | 유니코드 스칼라 (4바이트) | `char`(2바이트, UTF-16 unit) |
| `()` | unit (값이 없음) | `void` (단 식이 아님) |
| `(T1, T2, ...)` | 튜플 | (없음 — record로 흉내) |

여기서 두 가지 흥미로운 점.

첫째, *unsigned 정수가 있다*. Java는 unsigned를 일관되게 다루지 못해 *부호 있는 정수로 비트만 빌려쓰는* 패턴이 흔했다(`Byte.toUnsignedInt(b)` 같은 헬퍼 함수). Rust는 처음부터 분리해서 다룬다. 바이트 처리, 네트워크 프로토콜, 임베디드에서 더 자연스럽다.

둘째, *char가 4바이트*다. Java의 `char`는 2바이트 UTF-16 unit이라서 *이모지 한 개*가 두 char로 표현된다(surrogate pair). Rust의 `char`는 *유니코드 스칼라 값* 그 자체라 이모지든 한자든 *한 char가 한 글자*다. *체감으로 가장 차이가 나는 부분*이다.

`usize`는 *처음 보면 어색한 타입*이다. 의미는 *"포인터 크기에 맞춘 부호 없는 정수"*다. 64비트 플랫폼에서는 64비트, 32비트에서는 32비트가 된다. 배열·벡터의 인덱스 타입이 `usize`다. 즉 `vec[i]`에서 `i`는 보통 `usize`여야 한다. 다른 정수 타입과 자유롭게 섞이지 않는다(*명시적 캐스트 필요*). 처음엔 번거로워 보이지만, *오버플로 사고를 줄이는 안전 장치*라고 생각하자.

암묵적 형변환이 *없다*는 것도 핵심이다. `i32` 값에 `i64` 값을 더하려면 한쪽을 명시적으로 변환해야 한다.

```rust
let small: i32 = 100;
let big: i64 = 1000;
// let sum = small + big;        // 컴파일 에러
let sum = small as i64 + big;    // OK
```

답답해 보이지만, *우연한 정밀도 손실*이 사라진다. Java의 `long * int`가 묵묵히 잘리던 함정이 *코드에 모양으로 보인다*.

## 타입 추론 — 강하지만 함수 시그니처는 명시한다

Java의 `var`(JEP 286)와 Kotlin의 타입 추론에 익숙한 사람에게 Rust의 추론은 친근하게 다가온다. 다만 *철학이 다르다*. Java/Kotlin은 *지역 변수에서만* 추론을 허용한다. Rust도 그렇다 — *함수 시그니처는 항상 명시한다*. 컴파일러가 추론할 수 있다 해도 강제로 적게 만든다.

```rust
fn add(a: i32, b: i32) -> i32 {       // 시그니처 명시 강제
    let result = a + b;                // 지역 변수는 추론 OK
    result
}
```

*왜 시그니처는 강제일까?* 답은 *"함수 경계가 곧 API 계약이기 때문"*이다. 한 함수의 시그니처가 바뀌면 그 함수를 호출하는 모든 코드의 의미가 바뀔 수 있다. 컴파일러가 매번 그 영향을 *추론으로 풀게 두면* 코드의 의도가 흐려지고 빌드가 폭발적으로 느려진다. 그래서 *경계는 명시, 내부는 추론*이라는 규칙을 박아둔다. *바람직한 분업*이다.

함수의 마지막 줄을 보면 *세미콜론이 없다*. 이게 Rust의 특이점 하나다. *세미콜론이 있으면 statement(값이 없음), 없으면 expression(값이 있음)*이다.

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b              // 세미콜론 없음 → expression → 반환값
}

// 같은 의미를 명시적으로:
fn add_explicit(a: i32, b: i32) -> i32 {
    return a + b;      // 세미콜론 있음 → return 키워드 필요
}
```

후자의 모양이 Java/Kotlin과 같다. 전자의 모양이 *Rust스러운 관용*이다. 처음엔 어색해도, 코드가 *간결해지는 효과*가 크다.

## if·match·loop — expression의 세계

if도 expression이다.

```rust
let max = if a > b { a } else { b };
```

Java에서 `int max = a > b ? a : b;`로 적던 그 모양이 Rust에선 *if 그 자체*다. 삼항 연산자가 *별도로 없다* — *if expression이 그 일을 한다*.

여기서 진짜로 흥미로운 도구가 `match`다. Java 17의 sealed class + switch pattern matching에 익숙한 사람이라면 *"아, 이거 비슷한 건가?"* 싶을 텐데, *Rust의 match가 한 발 더 나간 형태*다.

```rust
enum HttpStatus {
    Ok,
    NotFound,
    Redirect(String),       // 데이터를 가진 enum
    ServerError { code: u16, message: String },
}

fn describe(status: HttpStatus) -> String {
    match status {
        HttpStatus::Ok => "정상".to_string(),
        HttpStatus::NotFound => "찾을 수 없음".to_string(),
        HttpStatus::Redirect(url) => format!("리다이렉트 → {url}"),
        HttpStatus::ServerError { code, message } => {
            format!("서버 오류 {code}: {message}")
        }
    }
}
```

세 가지 사실이 한꺼번에 보인다.

첫째, *Rust의 enum은 데이터를 가질 수 있다*. `Redirect(String)`처럼 변형마다 다른 타입의 값을 *내장*한다. 이걸 *algebraic data type*이라고 부른다. Java/Kotlin이 sealed class와 record로 흉내내려는 모양의 *원형*에 가깝다. Java의 코드와 비교해보면 차이가 더 뚜렷하다.

```java
sealed interface HttpStatus permits Ok, NotFound, Redirect, ServerError {}
record Ok() implements HttpStatus {}
record NotFound() implements HttpStatus {}
record Redirect(String url) implements HttpStatus {}
record ServerError(int code, String message) implements HttpStatus {}

String describe(HttpStatus status) {
    return switch (status) {
        case Ok ok -> "정상";
        case NotFound nf -> "찾을 수 없음";
        case Redirect(String url) -> "리다이렉트 → " + url;
        case ServerError(int code, String message) -> "서버 오류 " + code + ": " + message;
    };
}
```

문법이 비슷하다. 그런데 *Rust 쪽이 한 파일에 깔끔하게 모인다*. 변형마다 별도 record를 선언하지 않아도 된다. *enum 한 덩어리에 모든 변형이 산다*.

둘째, *match가 exhaustive다*. 모든 변형을 다루지 않으면 컴파일 에러가 난다. Java 17의 switch pattern도 sealed에 대해서는 exhaustive를 요구하기 시작했지만, *non-sealed에는 default가 강제*된다. Rust는 enum이 곧 sealed이므로 *항상 exhaustive*다. 새 변형이 enum에 추가되면 *match를 안 고친 모든 코드가 컴파일러에 의해 발견*된다. 이게 운영 사고를 줄이는 가장 큰 안전 장치다.

셋째, *match가 expression이다*. 위 함수의 본문 전체가 *match 한 식*이고 그 식의 값이 함수의 반환값이다. Java도 switch expression으로 이걸 따라잡았지만, Rust는 처음부터 그 모양으로 설계됐다.

`if`의 사촌격으로 `if let`도 자주 쓴다. 한 변형만 관심 있을 때다.

```rust
let status = HttpStatus::Redirect("https://example.com".to_string());

if let HttpStatus::Redirect(url) = status {
    println!("리다이렉트할 URL: {url}");
}
```

*Java 21의 `if (obj instanceof Redirect r)` 패턴*과 정확히 같은 의도다. 다만 Rust 쪽이 *더 일찍 자리잡았고 더 자연스럽다*.

루프는 세 가지가 있다.

```rust
// 무한 루프 (이걸로 break해서 빠져나옴)
loop {
    if condition() { break; }
}

// 조건부 루프
while still_running() {
    do_work();
}

// 이터레이션
for item in collection {
    process(item);
}
```

`for in`이 Java의 `for-each`와 의미가 같다. 다만 *Rust의 for는 더 강력하다*. 컬렉션의 *iterator를 자동으로 호출*하고, *클로저 체인(map, filter, fold)*과 매끄럽게 합성된다.

```rust
let sum: i32 = (1..=100)
    .filter(|n| n % 2 == 0)     // 짝수만
    .sum();

println!("{sum}");              // 2550
```

Java 8의 Stream API와 모양이 비슷하다. 차이가 하나 있다면, *Rust의 iterator는 lazy하면서도 zero-cost*다. 위 체인은 컴파일러가 *단일 루프로 인라인*해버리기 때문에 추상화 비용이 0에 수렴한다. Java Stream의 박싱 비용 같은 건 없다. *추상화가 공짜*라는 Rust의 약속이 가장 명료하게 드러나는 지점이다.

## 모듈 시스템 — package + 가시성을 한 도구로

Java/Kotlin에서 패키지와 가시성을 떠올려보자. `package com.example.foo;` 선언, `public`/`protected`/`package-private`/`private` 접근제어자, JPMS의 `module-info.java`까지. *세 층*에 걸쳐 정리돼 있다. Rust에서는 이걸 *crate + mod + pub*의 한 모델로 통합한다.

용어 먼저 정리하자.

- **crate**: Rust의 컴파일 단위. *Maven의 artifact*에 해당한다. 한 crate는 한 개의 라이브러리(`.rlib` 또는 `.so`)나 실행 파일을 만든다.
- **module (mod)**: crate 안의 *namespace*. Java의 package에 가깝다. 다만 *파일 시스템과 1:1 매칭이 강제되지 않는다* — 한 파일 안에 여러 module을 선언해도 되고, 한 module을 여러 파일에 걸쳐 선언해도 된다(하위 mod 분할).
- **pub / pub(crate) / pub(super)**: 가시성. *Java보다 더 세분화*돼 있다.

`pub` 한 단어로 훑어보자.

```rust
mod auth {
    pub struct User {            // 외부에서 보임
        pub name: String,        // 필드도 별도 pub 필요
        password_hash: String,   // 필드는 디폴트로 mod 안에서만
    }

    pub(crate) fn validate(u: &User) -> bool {
        // 같은 crate 안에서만 보임 (외부 crate에는 숨김)
        !u.password_hash.is_empty()
    }

    fn private_helper() {
        // 같은 mod 안에서만 보임
    }
}
```

Java와 한 줄 한 줄 매핑하면 이렇다.

| Rust | Java |
|---|---|
| `pub` | `public` |
| (디폴트) | `package-private` |
| `pub(crate)` | `module-info.java`의 `exports ... to ...`과 비슷 |
| `pub(super)` | (직접 대응 없음) |
| `pub(in path::to::mod)` | (직접 대응 없음) |

`pub(crate)`가 *흥미로운 도구*다. *crate 외부에는 숨기고 싶지만 crate 안에서는 자유롭게 쓰고 싶은* API에 쓴다. 라이브러리를 만들 때 *공개 API와 내부 헬퍼를 분리*하는 가장 자연스러운 도구다. Java의 `module-info.java`가 비슷한 일을 하지만, *모든 자바 프로젝트가 모듈을 쓰지 않는다*는 현실적 한계가 있다. Rust는 *crate가 곧 모듈*이라 이 분리가 *기본값*이다.

파일 구조는 두 스타일이 있다. *모던 스타일*(2018 edition 이후 권장)부터 보자.

```
src/
├── main.rs            # 또는 lib.rs
├── auth.rs            # mod auth
├── auth/
│   ├── login.rs       # mod auth::login
│   └── token.rs       # mod auth::token
└── infra/
    ├── db.rs          # mod infra::db
    └── cache.rs       # mod infra::cache
```

`src/main.rs`(또는 `lib.rs`)는 다음처럼 모듈을 *선언만* 한다.

```rust
mod auth;
mod infra;
```

이 한 줄이 *"`auth.rs` 파일이나 `auth/mod.rs`를 찾아 그 내용을 module로 가져오라"*는 의미다. 하위 모듈도 같은 패턴.

```rust
// auth.rs
pub mod login;
pub mod token;

pub fn shared_helper() { /* ... */ }
```

*전통 스타일*은 `auth/mod.rs`를 만들어 같은 일을 한다. 둘 다 작동하지만, *모던 스타일이 권장*이다. 파일 트리만 봐도 모듈 구조가 보이고, `mod.rs`라는 *이름이 덜 의미적*이라는 비판이 있었기 때문이다.

다른 mod의 항목을 가져올 땐 `use`다. Java의 `import`에 해당한다.

```rust
use crate::auth::User;          // crate 루트에서 시작하는 절대 경로
use super::shared_helper;       // 부모 mod에서
use self::login::Token;         // 같은 mod의 하위
```

*prelude*라는 흥미로운 도구가 하나 더 있다. *"import 없이 보이는 항목 모음"*이다. `Option`, `Result`, `Vec`, `String`, `Box`, `Drop`, `Clone` 같이 *거의 모든 코드에서 쓰이는 항목*은 prelude에 들어 있어서 import 없이 바로 쓸 수 있다. Java라면 `java.lang.*`이 자동으로 import되는 것과 비슷한 발상이다.

## prelude — 이미 import된 친구들

prelude에 들어 있는 항목을 한번 훑어보자. 자주 만나는 것들이다.

```rust
// 표준 라이브러리 prelude (자동 import)
Option, Some, None
Result, Ok, Err
Vec
String
Box
Clone, Copy
Drop
Iterator, IntoIterator
ToString, ToOwned
Debug (트레잇은 보통 derive로 사용)
PartialEq, Eq, PartialOrd, Ord
Send, Sync
```

*이 친구들은 import 없이 바로 보인다*. Java로 치면 `Optional`, `String`, `ArrayList`, `Comparable`을 import 없이 쓸 수 있다는 뜻이다. 그래서 Rust 코드의 `use` 줄이 Java의 `import`보다 *대체로 짧다*.

라이브러리도 자체 prelude를 제공할 수 있다. tokio는 `tokio::prelude`(이제는 deprecate됐지만 한때 표준이었다), diesel은 `diesel::prelude::*`를 쓴다. 라이브러리 문서에 *"prelude를 import하라"*는 안내가 있으면 *"이 라이브러리가 자주 쓰는 트레잇 묶음"*이라는 뜻이다. Spring의 `import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*` 같은 패턴이 *언어 차원에서 표준화*된 셈이다.

## 함수 — 일급 시민, 그리고 클로저

함수 자체는 익숙한 모양이지만 한 가지 짚을 게 있다. *Rust 함수는 일급 시민*이다. 변수에 담고, 인자로 넘기고, 반환할 수 있다. 클로저(Java의 람다)도 자연스럽게 같은 모양으로 쓰인다.

```rust
fn double(x: i32) -> i32 {
    x * 2
}

let f: fn(i32) -> i32 = double;     // 함수 포인터
let g = |x: i32| x * 2;             // 클로저
let h = |x| x * 2;                  // 타입 추론

println!("{} {} {}", f(5), g(5), h(5));   // 10 10 10
```

세 모양이 모두 같은 동작을 한다. Java 8 이후의 `Function<Integer, Integer>` + 람다와 모양이 비슷한데, *Rust 쪽이 더 가볍다*. 박싱이 없고, 인라인이 잘 된다.

클로저는 *환경을 캡처하는 방식*에서 trait 이름이 결정된다. `Fn`, `FnMut`, `FnOnce` 세 가지인데, 이 셋의 차이는 *4장 소유권을 본 뒤에* 명료해진다. 지금은 *"보통 클로저는 자동으로 잘 동작하고, 가끔 컴파일러가 'this closure implements FnMut, not Fn' 같은 메시지를 띄울 때 그 차이를 의식하게 된다"* 정도만 손에 묻혀두자.

## String과 &str — 함정 5의 첫 만남

여기서 *Rust 입문자가 가장 많이 헷갈리는 지점* 하나를 미리 짚어두자. 문자열 타입이 *두 개*다.

```rust
let owned: String = String::from("Hello");   // heap-allocated, owned
let borrowed: &str = "Hello";                 // borrowed view
let borrowed2: &str = &owned;                 // String을 &str로 빌림
```

`String`은 *heap에 잡힌, 소유권을 가진, 늘어날 수 있는 문자열*이다. Java의 `StringBuilder`에 가깝다. `&str`은 *빌려온 view*고 *변경 불가*다. 문자열 리터럴 `"Hello"`의 타입이 `&str`이다.

이게 왜 두 개로 나뉘어 있을까? Java/Kotlin의 `String`은 *항상 immutable이고 ownership 개념이 없으니* 한 타입으로 충분했다. Rust에서는 *소유 vs 빌림*이 언어 차원의 1급 구분이라서, *문자열도 그 구분을 따라야* 한다. 처음엔 답답하다.

처방은 단순하다. *디폴트 패턴*을 머리에 박아두자.

- *함수의 입력 파라미터*는 보통 `&str`로 받는다. 호출자에게 *소유권을 옮기지 않아도 되니* 가장 유연하다.
- *함수의 반환값이나 구조체 필드*는 보통 `String`으로 잡는다. *데이터를 들고 있으려면 소유*해야 한다.

```rust
fn greet(name: &str) -> String {        // 입력은 빌림, 반환은 소유
    format!("Hello, {name}!")
}

let user_name = String::from("Spring 개발자");
let message = greet(&user_name);        // String을 &str로 빌려 넘김
println!("{message}");                   // "Hello, Spring 개발자!"
```

이 디폴트 한 줄을 머리에 박아두면 *처음 한 달의 90% 상황을 풀 수 있다*. 자세한 *왜*는 4장 소유권에서 풀린다. 지금은 *"두 개가 있다는 사실과, 함수 파라미터는 보통 &str"*만 기억하자. 이 미묘한 어긋남이 4장의 첫 컴파일 거부로 이어지는 다리다.

## struct와 derive — 도메인 모델의 첫 모양

비즈니스 도메인을 모델링하려면 struct가 필요하다. Java의 record와 모양이 가장 비슷한 도구다.

```rust
struct User {
    id: i64,
    email: String,
    created_at: i64,        // unix timestamp 가정
}

impl User {
    fn new(id: i64, email: String, created_at: i64) -> Self {
        User { id, email, created_at }
    }

    fn is_recent(&self) -> bool {
        let now = current_unix_timestamp();
        now - self.created_at < 86400
    }
}

fn current_unix_timestamp() -> i64 {
    // (실제로는 std::time::SystemTime을 쓴다)
    0
}
```

여기서 두 가지가 흥미롭다.

첫째, *필드와 메서드가 분리*된다. struct 본문에는 *데이터 필드만* 있고, 메서드는 별도 `impl` 블록에 둔다. Java의 클래스가 *데이터와 행동을 한 덩어리*에 묶는 것과 다른 발상이다. *왜 이렇게 분리했을까?* 답은 *"데이터와 행동의 결합도를 낮추고, 한 데이터 타입에 여러 impl 블록을 자유롭게 추가할 수 있게"* 하기 위함이다(7장 trait에서 다시 본다). 처음엔 어색하지만 *지나면 자연스러워진다*.

둘째, `Self`가 *현재 impl 블록의 타입*을 가리키는 *별칭*이다. `User`라고 적어도 같지만, *리팩토링에 강하다*. 타입명을 바꿔도 `Self`는 자동으로 따라간다.

도메인 모델에 *기본 트레잇 묶음*을 자동으로 부여하는 도구가 `#[derive(...)]`다.

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
struct User {
    id: i64,
    email: String,
    created_at: i64,
}
```

이 한 줄로 *디버그 출력*, *복제*, *동등 비교*가 자동으로 구현된다. Lombok의 `@Data` + `@Builder`와 의도가 같다. 다만 *Lombok은 IDE 외부에서는 동작이 잘 안 보이는 마법*이라면, Rust의 `derive`는 *컴파일러가 토큰 레벨에서 진짜 코드를 펼쳐* 내부 검증을 거친다. `cargo expand`(`cargo install cargo-expand`로 설치)로 그 펼친 모양을 *실제 코드로* 볼 수 있다. 마법의 거리감이 *훨씬 적다*.

자주 쓰는 derive를 미리 모아두자.

- `Debug` — `{:?}` 포매터로 출력 가능 (`println!("{:?}", user)`).
- `Clone` — `.clone()` 메서드 호출 가능.
- `Copy` — *값 의미로 복사* (작은 타입에만, `Clone`이 함께 필요).
- `PartialEq, Eq` — `==`/`!=` 비교 가능.
- `PartialOrd, Ord` — 정렬 가능.
- `Hash` — HashMap의 키로 사용 가능.
- `Default` — `T::default()`로 디폴트 인스턴스 생성.
- `serde::Serialize, serde::Deserialize` — JSON 등 직렬화 (별도 crate 필요).

도메인 모델을 짤 때 *반사적으로* 다음 정도는 붙여두는 편이 낫다.

```rust
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
struct User { /* ... */ }
```

## 에러 메시지 읽는 법 — 4장 첫 컴파일 거부 앞의 다리

이 장의 마지막 절은 *Rust 컴파일러의 에러 메시지를 읽는 법*이다. 다음 장(4장 소유권)에서 처음으로 *"왜 이게 컴파일이 안 되지?"*라는 질문에 부딪히게 된다. 그때를 위한 사전 준비다.

Rust의 컴파일러 메시지는 *친절하기로 유명*하다. JVM 진영의 NullPointerException 한 줄과 비교하면 *책 한 페이지처럼 길다*. 처음엔 *길어서 부담*이지만, *그 안에 답이 들어 있는 경우가 대부분*이다. 한 번 길게 읽어보자.

가상 예제 하나를 짜보자.

```rust
fn main() {
    let s = String::from("Hello");
    let t = s;
    println!("{s}");        // 일부러 에러 유발
}
```

`cargo run`을 치면 다음과 같은 에러가 뜬다.

```
error[E0382]: borrow of moved value: `s`
 --> src/main.rs:4:16
  |
2 |     let s = String::from("Hello");
  |         - move occurs because `s` has type `String`, which does not implement the `Copy` trait
3 |     let t = s;
  |             - value moved here
4 |     println!("{s}");
  |                ^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
3 |     let t = s.clone();
  |              ++++++++

For more information about this error, try `rustc --explain E0382`.
```

이 메시지를 *한 부분씩* 뜯어보자.

1. **에러 코드** (`error[E0382]`): 첫 줄의 `[E0382]` 같은 코드. `rustc --explain E0382`를 치면 *그 에러의 일반론적인 설명*을 책 한 단원처럼 펼쳐준다. 처음 한 달은 모르는 코드가 뜰 때마다 한 번씩 explain을 쳐보자. *공식 문서를 손에 쥐고 학습하는 셈*이다.

2. **요약** (`borrow of moved value: 's'`): 무엇이 잘못됐는지 한 줄. *영문이지만 단어가 정확하다*. "moved", "borrow", "owned"는 4장에서 익숙해진다.

3. **위치 표시** (`--> src/main.rs:4:16`): 파일·줄·열. IDE의 클릭 가능한 링크로 보통 동작한다.

4. **본문 — 컨텍스트 표시**: 문제 라인 주변을 *그림으로* 보여준다.
   ```
   2 |     let s = String::from("Hello");
     |         - move occurs because `s` has type `String`, which does not implement the `Copy` trait
   3 |     let t = s;
     |             - value moved here
   4 |     println!("{s}");
     |                ^ value borrowed here after move
   ```
   *세 줄에 걸친 에러의 흐름*이 한 그림에 보인다. 어디서 move가 일어났고, 어디서 그 다음 사용이 일어났는지가 *시각적으로* 표시된다. 이 정도까지 친절한 컴파일러는 정말 드물다.

5. **help / suggestion**: 가능한 처방. 위 예제에서는 `s.clone()`으로 고치라는 *구체적인 제안*까지 준다. *문자 그대로* 그 자리에 `clone()`을 붙이면 된다.

처음 한 달의 *가장 빠른 학습 전략*은 단순하다. *컴파일러가 보여주는 메시지를 그대로 따르는 것*이다. *"borrow checker를 적이 아니라 동료(co-author)로 받아들이자"*는 표현이 자주 등장하는데,[^1] 이게 진심으로 맞다. 처음엔 컴파일러가 *너무 까다로운 시니어*처럼 느껴진다. 두 달쯤 지나면 *"왜 그렇게 까다롭게 굴었는지"*가 이해된다. 석 달이 되면 *그 시니어가 잡아주지 않는 코드는 오히려 불안하게* 느껴진다. 일종의 사고방식의 전환이다.

흔히 쓰는 한 가지 처방을 미리 알려두자. 에러 메시지가 너무 길거나 복잡할 때는 `cargo build 2>&1 | less` 또는 `cargo build 2>&1 | head -50`으로 *처음 에러 한두 개만* 본다. 첫 에러를 고치면 종종 그 뒤의 에러들이 *연쇄적으로 사라진다*. 한꺼번에 다 풀려고 하지 말자. *한 개씩, 위에서부터*.

## 마무리 — 다음 장의 다리

이 장에서 우리가 한 일을 정리해보자. 변수의 불변 디폴트가 *어떤 무게*인지를 봤고, 원시 타입의 지도를 그렸다. 함수와 if·match·loop의 *expression-oriented* 모양을 익혔다. 모듈과 가시성이 Java의 그것보다 *더 세분화된 모델*이라는 것을 봤고, struct와 derive로 도메인 모델의 첫 모양을 잡았다. 끝으로 *Rust 컴파일러 에러 메시지의 구조*를 한 번 펼쳐 봤다.

기억해두자. 이 장에서 익힌 도구들은 *모두 4장의 소유권으로 이어지는 다리*다. `let`과 `let mut`이 가변성을 명시하는 모양은 *소유권의 move 의미*로 확장된다. `String`과 `&str`의 두 모양은 *소유와 빌림*의 가장 첫 사례다. struct의 필드 선언은 *그 필드를 누가 소유하느냐*는 질문으로 이어진다. *지금까지 익힌 모양들이 의미를 갖는 자리가 4장*이다.

다음 장에서는 드디어 *Rust의 가장 인상적인 한 가지*를 만난다. *"한 명만 가진다"*는 단순한 규칙이 어떻게 NPE, memory leak, use-after-free, double-free를 *동시에* 컴파일 타임에 차단하는지를 본다. 그리고 그 첫 만남에서 컴파일러가 *우리 코드를 거부*하는 풍경에 부딪힌다. 이 장 끝에서 본 에러 메시지 읽기가 *그때 진짜로 도움이 된다*.

## 함께 해보자

자기가 Java로 짜본 적 있는 *작은 도메인 클래스 하나*를 떠올려보자. 예를 들어 사용자 모델 같은 것이다. 다음처럼 Rust struct로 옮겨보자.

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
struct User {
    id: i64,
    email: String,
    created_at: i64,         // unix timestamp
    is_admin: bool,
}

impl User {
    fn new(id: i64, email: String, created_at: i64) -> Self {
        User {
            id,
            email,
            created_at,
            is_admin: false,
        }
    }

    fn promote(&mut self) {
        self.is_admin = true;
    }

    fn display(&self) {
        println!("{:?}", self);
    }
}

fn main() {
    let mut user = User::new(1, "toby@example.com".to_string(), 1700000000);
    user.display();
    user.promote();
    user.display();
}
```

이 코드를 짜본 뒤 다음을 손으로 확인해보자.

1. `#[derive(Debug)]`를 빼고 `cargo build`를 시도해보자. 어떤 에러가 뜨는가? 그 에러를 읽어 *왜* 그런 에러가 나는지 한 줄로 적어보자.
2. `email` 필드를 `pub email: String`으로 바꾼 뒤 다른 모듈에서 직접 접근해보자. Java의 *getter 없이 public 필드에 직접 접근*하는 감각이 어떻게 다른가? 한 줄로 적어보자.
3. `cargo expand`(`cargo install cargo-expand` 후)를 쳐 `#[derive(Debug, Clone, PartialEq, Eq)]`가 *실제로 어떤 코드를 만들어내는지* 펼쳐보자. Lombok의 `@Data`가 IDE에서만 보이는 마법이라면, Rust의 derive는 *진짜 코드*다.
4. 이 `User` struct를 `let user_a = User::new(...); let user_b = user_a;` 후 `user_a.display();`를 시도해보자. *어떤 에러가 나는가?* 그 에러가 *4장에서 정면으로 다룰* 그 에러다.

다음 장에서는 마지막 4번 시도가 왜 거부되는지를 정면으로 푼다. *세 가지 단순한 규칙*이면 답이 나온다.

---

## 참고

[^1]: ["The Borrow Checker: Rust's Tough-Love Mentor" — woodruff.dev](https://www.woodruff.dev/the-borrow-checker-rusts-tough-love-mentor/); ["Rust ownership and borrows: Fighting the borrow-checker" — DEV.to](https://dev.to/daaitch/rust-ownership-and-borrows-fighting-the-borrow-checker-4ea3).

---

# Part 2. Rust의 마음 — 컴파일러와 친구되기

> *책의 무게중심이다. JVM 출신이 가장 많이 부딪히고 가장 많이 보상받는 영역이다.*

Part 2의 다섯 챕터가 이 책의 *가장 어두운 골짜기*이자 *가장 큰 보상의 자리*다. 4장에서 소유권의 *세 가지 규칙*에 첫 번째 컴파일 거부를 받고, 5장에서 빌림의 *두 줄 규칙*으로 그 답답함이 풀린다. 5장 끝에는 RustBelt / Stacked Borrows / Tree Borrows 한 단락이 박혀 있다 — *이 두 줄의 규칙은 학술적으로 입증된 안전성*이라는 위상 신호다. 6장에서 라이프타임 elision으로 *진짜로 `'a`를 써야 하는 순간은 손에 꼽힌다*는 안도가 오고, 7장에서 트레잇·제네릭·패턴 매칭·에러 처리(`Result<T, E>` / `?` / anyhow / thiserror)로 *표현력의 도구상자*를 손에 쥔다. 8장에서 스마트 포인터(`Box`/`Rc`/`Arc`/`RefCell`/`Mutex`)와 매크로, 그리고 *unsafe 한 절*로 Rust의 안전 경계가 어디까지인지를 명료하게 본다. *unsafe는 컴파일러를 끄는 것이 아니라 책임을 인간이 보증하는 계약이다*라는 한 줄이 이 Part의 매듭이다.

**포함 챕터**

- 4장. 소유권 — "한 명만 가진다"는 단순한 규칙
- 5장. 빌림 — `&T`와 `&mut T`, 그리고 데이터 레이스가 사라지는 이유
- 6장. 라이프타임 — `'a`라는 메타데이터에 익숙해지자
- 7장. 트레잇·제네릭·패턴 매칭·에러 처리 — 표현력 도구상자
- 8장. 스마트 포인터·매크로·unsafe 진입 — 메모리 도구와 안전 경계


---

# 4장. 소유권 — "한 명만 가진다"는 단순한 규칙

이 장은 이 책의 *분수령*이다. 여기서 마음을 잘 잡으면 5장 빌림과 6장 라이프타임이 *연결된 한 흐름*으로 보이고, 7장 이후의 모든 도구가 *왜 그 모양인지*가 자연스럽게 이해된다. 반대로 여기서 답답해서 도망가면 *Rust의 가장 큰 보상*을 놓치게 된다. 그래서 이 장은 *유난히 천천히 간다*. 한 페이지씩 같이 호흡하자.

3장 끝 함께해보자에서 다음 코드를 시도해보고 컴파일러에게 거부당했을 것이다.

```rust
let user_a = User::new(...);
let user_b = user_a;
user_a.display();        // 에러!
```

Java/Kotlin이라면 *너무 당연하게* 동작했을 코드다. 참조 변수 두 개로 같은 객체를 가리키는 일상 패턴이다. 그런데 Rust는 이걸 *컴파일조차 안 해준다*. *왜 그럴까?* 이 질문에 답하는 게 이 장 전체다.

먼저 한 가지 마음의 준비를 하자. *Rust의 소유권 규칙은 어렵지 않다*. 단 *세 줄*이다. 다만 *익숙해지는 데 시간이 걸린다*. 십 년 동안 *"객체는 GC가 알아서 회수한다"*는 사고로 코드를 짜온 우리에게는, *"누가 이 메모리의 주인인가"*를 매번 의식하는 게 처음에는 어색하다. 두 달쯤 지나면 그 의식이 *제2의 자연*이 된다. 그때까지 *컴파일러와 친구 되기*다.

## 세 가지 규칙

본격적으로 시작하기 전에, 외워야 할 *전부*를 한 번 보자.

1. **모든 값은 정확히 하나의 owner를 가진다.**
2. **owner가 scope를 벗어나면 값은 즉시 drop된다.**
3. **값을 다른 변수에 대입하거나 함수에 넘기면 ownership이 *이동(move)* 한다.** 단, `Copy` 트레잇이 붙은 원시 타입은 복사된다.

이 세 줄이 전부다. *그런데 이 단순한 세 줄이* NPE도, memory leak도, use-after-free도, double-free도, data race도(다음 장에서 본다) *동시에* 컴파일 타임에 차단한다. 처음 들으면 *과장 같지만* 이 장 끝에서는 그 의미가 손에 잡힌다.

한 줄씩 풀어가자.

### 규칙 1 — 단 한 명의 owner

값마다 *주인이 정확히 한 명*이다. 그 주인은 *변수*다. 다음 코드를 보자.

```rust
let s = String::from("Hello");      // s가 String 값의 owner
```

이 한 줄에서 일어난 일을 그림으로 그려보자.

- `String::from("Hello")`가 *heap에 "Hello"라는 문자열 데이터*를 잡는다.
- 그 데이터의 *포인터·길이·용량 정보를 담은 핸들*이 *스택*에 만들어진다.
- 그 스택의 핸들이 *변수 s*다. *s가 곧 owner*다.

*"한 명만 주인이 된다"*는 규칙은 *그 데이터를 누가 회수하느냐*의 책임을 명확히 하기 위함이다. 두 명이 주인이면 *두 번 회수*되거나(double-free) *서로 미루다* 영원히 회수 안 되거나(memory leak) 한다. 그래서 *주인은 한 명*이다.

### 규칙 2 — scope를 벗어나면 즉시 drop

owner인 변수가 자신의 scope를 벗어나면 *그 즉시* 값이 회수된다. JVM의 GC가 *언젠가 이 객체를 회수하겠지*라고 *런타임에 추적*하던 일을, Rust는 *컴파일 타임에 결정*한다.

```rust
fn main() {
    {
        let s = String::from("Hello");
        // s 사용 가능
    }   // 이 닫는 중괄호에서 s가 drop됨. heap의 "Hello" 데이터가 즉시 해제.

    // 여기서는 s를 쓸 수 없음 (이미 drop됨)
}
```

*"즉시"*라는 단어가 결정적이다. JVM의 `try-with-resources`나 Kotlin의 `use {}`도 비슷한 일을 *지원*하지만, *그 블록 안에서만* 동작한다. `finalize()`는 *언제 불릴지 모른다*(사실상 deprecated). Rust는 *모든 scope 종료에서* 결정적으로 drop이 호출된다. 별도 키워드도 없다. *언어 자체의 동작*이다.

이 결정성이 운영에서 큰 차이를 만든다. 파일 핸들, DB 커넥션, 락, 메모리 — *예측 가능한 시점에 풀린다*. *"왜 이 커넥션이 안 풀렸지?"*라는 질문이 거의 사라진다.

`Drop` 트레잇을 직접 구현하면 *내가 정의한 정리 동작*을 그 시점에 끼워 넣을 수 있다.

```rust
struct DbConnection {
    handle: u32,
}

impl Drop for DbConnection {
    fn drop(&mut self) {
        println!("커넥션 #{} 닫는 중...", self.handle);
        // 실제 정리 동작
    }
}

fn main() {
    let conn = DbConnection { handle: 42 };
    println!("작업 중...");
    // 여기서 conn이 scope 종료, drop() 자동 호출
}
```

실행 결과:

```
작업 중...
커넥션 #42 닫는 중...
```

*RAII*(Resource Acquisition Is Initialization)라는 C++에서 온 패턴이다. *생성과 소멸이 변수의 lifecycle에 묶여 있다*. Java의 `try (var conn = ...)` 블록에 익숙한 사람이라면 *그것보다 한 단계 더 자연스러운* 모양이라고 생각하면 이해하기 쉽다.

### 규칙 3 — move

이제 가장 인상적인 규칙이다. *대입과 전달이 ownership을 옮긴다*. 3장 끝에서 본 그 코드의 정체다.

```rust
let user_a = User::new(...);
let user_b = user_a;    // user_a의 ownership이 user_b로 이동(move)
user_a.display();        // 에러: borrow of moved value
```

*Java라면 어떻게 해석되는가*를 떠올려보자. `User user_b = user_a;`는 *참조 복사*다. user_a와 user_b가 *같은 객체*를 가리킨다. 둘 중 어느 쪽으로도 그 객체에 접근할 수 있다. JVM의 GC가 *어느 한쪽이라도 살아있는 동안*에는 그 객체를 살려둔다.

Rust는 다르게 해석한다. `let user_b = user_a;`는 *user_a가 가지고 있던 ownership을 user_b에게 넘김*이다. 그 순간 *user_a는 더 이상 그 값의 주인이 아니다*. 컴파일러는 user_a를 *"moved"* 상태로 표시한다. 그 뒤 user_a를 사용하려고 하면 *컴파일 거부*다.

*왜 이렇게 설계됐을까?* 답은 *규칙 1의 보호*다. *"주인은 한 명"*을 강제하려면 *대입 시점에 그 주인이 누구인지를 명확히* 해야 한다. 그렇지 않으면 *동시에 두 변수가 같은 메모리의 주인*이 되어, scope 종료 시 *어느 쪽이 회수해야 하는지*가 불분명해진다. 컴파일러는 그 모호함을 *원천 차단*하기 위해 move를 강제한다.

## Copy 트레잇 — 작은 예외, 큰 헷갈림

여기까지 읽고 나면 의문이 하나 든다. *"그러면 i32 같은 원시 타입도 매번 move되나?"*

```rust
let x = 5;
let y = x;
println!("{x}");        // 이건 잘 동작
```

이 코드는 에러가 나지 않는다. *왜?* `i32`는 `Copy` 트레잇이 자동으로 구현된 타입이기 때문이다. `Copy`가 붙은 타입은 *대입 시 move가 아니라 복사*가 일어난다. *원본도 살아 있고 사본도 만들어진다*.

`Copy`가 붙은 타입의 특징은 *"복사 비용이 매우 작은 타입"*이다. 다음이 자동으로 `Copy`다.

- 모든 정수 타입 (`i32`, `u64`, `usize`, ...)
- 모든 부동소수점 (`f32`, `f64`)
- `bool`, `char`
- `Copy` 타입만 담은 튜플 `(i32, bool)`
- 고정 크기 배열의 `Copy` 타입 `[i32; 4]`

*뭐가 자동으로 Copy가 아닌가*를 보면 패턴이 보인다.

- `String` — heap 데이터를 가지므로 복사 비용이 크다. *Copy 아님*.
- `Vec<T>` — 같은 이유로 *Copy 아님*.
- `User` 같은 사용자 정의 struct — 디폴트로 *Copy 아님*.

처음에는 *"왜 어떤 건 되고 어떤 건 안 되지?"*가 헷갈린다. 두 달쯤 지나면 *"heap을 가지면 move, 스택에서 끝나면 Copy"*라는 직관이 생긴다. 자세한 *왜*는 *복사가 얕은 복사인가 깊은 복사인가*의 문제다. 스택에 있는 비트는 *그대로 비트 복사*하면 된다. heap을 가리키는 핸들은 *비트만 복사하면 두 핸들이 같은 heap을 가리켜* 결국 두 명의 주인이 되어 규칙 1을 위반한다. 그래서 heap을 가진 타입은 *Copy를 자동 부여하지 않고* 명시적으로 `.clone()`을 부르게 만든다.

## 함수에 넘기는 것도 move다

대입만 move를 일으키는 게 아니다. *함수 호출에 인자로 넘기는 것*도 move다.

```rust
fn take_string(s: String) {
    println!("{s}");
    // 함수가 끝나면 s가 drop됨
}

fn main() {
    let owned = String::from("Hello");
    take_string(owned);
    // println!("{owned}");      // 에러: ownership이 take_string으로 이동
}
```

`take_string(owned)`을 호출하는 순간 *owned의 ownership이 함수의 파라미터 s로 이동*한다. 함수가 종료되면 s가 scope를 벗어나 *drop된다*. 호출자에서는 더 이상 owned에 접근할 수 없다.

처음에는 *"이게 왜 좋은 거지?"* 싶다. Java라면 *그저 참조를 넘긴 것*이고 호출자도 그 참조로 객체에 계속 접근할 수 있다. 그런데 잠시 멈추고 생각해보자. *"함수에 객체를 넘긴 뒤에도 호출자가 그 객체를 계속 쓰는 코드"*가 *얼마나 많은 사고의 원인*이었는지. 동시 수정 사고, *방어적 복사를 깜빡한 사고*, 파일 핸들이 두 곳에서 닫히는 사고. Rust는 그 카테고리를 *컴파일러가 거부*한다.

*"그런데 함수에 넘기고 나서도 계속 쓰고 싶은 일이 진짜 많지 않나?"* 맞다. 그 자연스러운 욕구를 풀어주는 두 가지 길이 있다.

길 하나: *반환받기*. 함수가 *받은 ownership을 다시 돌려준다*.

```rust
fn take_and_return(s: String) -> String {
    println!("쓰는 중: {s}");
    s   // ownership을 반환
}

fn main() {
    let owned = String::from("Hello");
    let owned = take_and_return(owned);    // 다시 받음
    println!("이제도 쓸 수 있다: {owned}");
}
```

답답하다. *함수마다 매번 반환해야 한다*. 호출자에서도 *변수 재할당*을 매번 해야 한다.

길 둘: *빌려주기(borrowing)*. *5장의 주제*다. 이 장에서는 *"길 둘이 곧 진짜 답"*이라는 것만 알아두자. 길 하나는 *4장의 한정된 도구*고, 5장에서 빌림을 배우면 이 답답함이 *깨끗이 풀린다*.

## clone() — 죄책감 없이 쓰자

길 셋이 하나 더 있다. `.clone()`이다. 명시적으로 *데이터 복사본을 하나 더 만든다*.

```rust
let owned = String::from("Hello");
let copy = owned.clone();      // heap 데이터까지 복사
println!("{owned} {copy}");    // 둘 다 살아 있음
```

`.clone()`은 *깊은 복사*다. heap에 *"Hello" 데이터를 한 벌 더* 만든다. 그래서 두 변수가 *별개의 데이터*를 owned하게 된다.

*입문자에게 가장 자주 하는 권고* 하나는 이것이다. *"clone을 죄책감 없이 쓰자."* Rust 커뮤니티에 *"clone()을 너무 많이 쓰면 성능에 안 좋다"*는 교조적인 분위기가 있는데, *입문자에게는 그 조언이 학습을 망치는 가장 큰 적*이다. 처음 한 달은 *clone으로 풀 수 있는 모든 문제를 clone으로 풀고*, 6장 이후 빌림과 라이프타임에 익숙해지면 *그때 clone을 빌림으로 옮겨가도 늦지 않다*.

```rust
fn print_user(u: User) {
    println!("{}", u.email);
}

fn main() {
    let user = User::new(...);
    print_user(user.clone());      // 복사 한 벌 만들어 넘김
    println!("{}", user.email);    // 원본도 살아 있음
}
```

성능이 *진짜로 문제가 되는 hot path*에서는 빌림으로 옮긴다. *그 외에는 clone이 충분히 좋은 답*이다. 단순한 도메인 객체 한 개를 복사하는 비용은 *현대 하드웨어에서 거의 측정 불가능*하다. 학습의 흐름을 끊지 말고 *clone으로 일단 통과시키자*. 익숙해지는 게 먼저다.

## `Vec<T>`로 본 move의 의미

도메인 객체 단위가 아니라 *컬렉션 단위*에서 move를 보면 그 의미가 더 또렷해진다.

```rust
fn process(numbers: Vec<i32>) -> i32 {
    numbers.iter().sum()
}

fn main() {
    let nums = vec![1, 2, 3, 4, 5];
    let total = process(nums);
    // println!("{:?}", nums);    // 에러: nums의 ownership은 process로 이동
    println!("합: {}", total);
}
```

`Vec<i32>`을 함수에 넘기면 *그 Vec 전체*의 ownership이 이동한다. 호출자에서는 더 이상 nums에 접근 못 한다. *왜 이렇게 동작하는가*는 다시 *규칙 1*이다. *주인은 한 명*. 함수 안에서도 호출자에서도 *동시에 주인*일 수 없다.

Java로 같은 의미를 짜본다고 해보자.

```java
int process(List<Integer> numbers) {
    return numbers.stream().mapToInt(Integer::intValue).sum();
}

void main() {
    List<Integer> nums = List.of(1, 2, 3, 4, 5);
    int total = process(nums);
    System.out.println(nums);    // OK — 그저 참조 복사
}
```

Java는 *그저 참조 복사*다. nums와 numbers가 *같은 List를 가리킨다*. 그래서 *호출자에서 nums.add(...)*를 하면 함수 내부에서도 *영향*을 받는다(만약 함수가 그 시점에 iteration 중이었다면 ConcurrentModificationException). 십 년 동안 *방어적 복사로 막아온 함정*이다. Rust에서는 *컴파일러가 거부*한다. 그게 이 책 1장에서 말한 *"안전을 보장하는 시점이 다르다"*의 구체적 풍경이다.

다시, 이 답답함의 답은 *5장의 빌림*이다. `&Vec<i32>`로 넘기면 *읽기만 하는 빌림*이고, ownership은 호출자에 남는다. 다음 장에서 만나자.

## String과 &str — 함정 5의 정면 처방

3장에서 *"두 개가 있다는 사실"*만 짚었던 String과 &str을 이제 *정면으로* 다룰 차례다. 이제 ownership의 눈으로 보면 *왜 두 개인지*가 자연스럽게 풀린다.

```rust
let owned: String = String::from("Hello");      // heap에 데이터, 핸들이 owner
let borrowed: &str = "Hello";                    // 프로그램 binary 안의 데이터를 빌림
let borrowed_from_owned: &str = &owned;          // owned가 가진 데이터를 빌림
```

세 변수의 정체를 그림으로 그려보자.

- `owned` — *heap에 잡힌 "Hello" 5바이트* + 그 데이터의 *포인터·길이·용량을 담은 핸들*(스택). 핸들이 owner. owned가 scope를 벗어나면 heap의 5바이트도 함께 회수.
- `borrowed` — *프로그램 binary의 read-only 영역에 박힌 "Hello" 5바이트*를 *빌려본 view*. 데이터의 owner는 *프로그램 그 자체*(`'static` 라이프타임). borrowed가 scope를 벗어나도 데이터는 그대로.
- `borrowed_from_owned` — *owned가 가진 heap 데이터를* 빌려본 view. owner는 여전히 owned. borrowed_from_owned는 *owned보다 오래 살 수 없다*(이게 6장 라이프타임의 본질).

Java/Kotlin의 `String`은 *항상 immutable이고 ownership 개념이 없다*. JVM이 *문자열 풀*로 일부 최적화를 하지만, 개발자 시야에서는 모든 String이 똑같다. Rust는 *"이 문자열의 데이터가 어디 있고 누가 주인인가"*를 *타입 차원에서 분리*한다. 처음엔 답답하다. 두 달 뒤엔 *"이 정도는 알아야 시스템을 짜지"*라는 감각이 생긴다.

함수 시그니처에서의 디폴트 패턴을 다시 한번 못 박아두자.

```rust
// 좋은 패턴: 입력은 &str, 반환은 String
fn build_greeting(name: &str) -> String {
    format!("Hello, {name}!")
}

// 답답한 패턴: 입력도 String (호출자가 ownership을 잃음)
fn build_greeting_bad(name: String) -> String {
    format!("Hello, {name}!")
}

fn main() {
    let user_name = String::from("Spring 개발자");

    let greeting1 = build_greeting(&user_name);     // 좋음: user_name 살아 있음
    println!("{greeting1} {user_name}");

    let greeting2 = build_greeting_bad(user_name);  // 답답: user_name 사라짐
    // println!("{user_name}");                      // 에러
}
```

*입력은 빌림으로, 출력은 소유로*. 이 한 줄을 머리에 새겨두자.

## Drop 트레잇 — 결정적 자원 해제의 진짜 매력

위에서 잠깐 본 `Drop`을 *제대로* 한 번 더 들여다보자. 이 트레잇 하나가 운영의 풍경을 바꾼다.

흔한 시나리오 하나. *DB 커넥션을 빌려와 작업하고, 작업이 끝나면 풀에 반납*하는 코드다. Java로 짜면 다음과 같다.

```java
try (Connection conn = dataSource.getConnection()) {
    // 작업
} // try-with-resources가 close()를 호출
```

`try-with-resources`가 처리하지만, *try 블록 안에서만* 동작한다. 메서드 안에서 `Connection`을 얻어 *반환하면* 호출자가 *닫을 책임*을 지게 된다. 그 책임 이전이 사고의 원인이다.

Rust로 짠다면.

```rust
fn process_user(pool: &ConnectionPool, user_id: i64) -> Result<User, DbError> {
    let conn = pool.acquire()?;
    let user = conn.fetch_user(user_id)?;
    Ok(user)
    // conn이 여기서 scope 종료, Drop이 호출되어 풀에 자동 반납
}
```

함수의 *어디서 return하든*, *조기 return이든*, *? 연산자로 즉시 빠져나가든*, conn이 scope를 벗어나는 *모든 경로*에서 Drop이 호출된다. *코드에 close() 한 줄도 없는데* 누수가 안 난다. *기억해두자. 이게 RAII의 진짜 매력*이다.

여러 자원이 얽혀 있을 때 더 빛난다.

```rust
fn complex_work() -> Result<(), AppError> {
    let conn = acquire_db_connection()?;     // 1번 자원
    let lock = acquire_distributed_lock()?;  // 2번 자원
    let temp_file = create_temp_file()?;     // 3번 자원

    do_work(&conn, &lock, &temp_file)?;
    Ok(())
    // 함수가 끝나면 temp_file → lock → conn 순서로 (선언 역순으로) drop
}
```

세 자원이 *선언의 역순으로* 깨끗하게 풀린다. Java라면 *try-with-resources 세 겹*이거나 *try/finally 중첩*인데, Rust는 *그저 변수 선언*만으로 같은 안전성을 얻는다. *코드가 더 짧고, 누락 가능성이 0이다*.

## 같은 의미를 두 가지 길로 풀어보자

이쯤 되면 *3장 끝의 그 코드*를 두 가지 길로 풀 수 있다. 마지막으로 그 코드를 다시 펼쳐보자.

```rust
fn main() {
    let s = String::from("Hello");
    let t = s;
    println!("{s}");     // 에러: borrow of moved value
}
```

*길 하나*: clone으로 풀기.

```rust
fn main() {
    let s = String::from("Hello");
    let t = s.clone();    // s의 데이터를 한 벌 더 만들어 t의 owner로
    println!("{s} {t}");   // 둘 다 살아 있음
}
```

*길 둘*: borrow로 풀기 (*5장의 정식 답*, 미리보기).

```rust
fn main() {
    let s = String::from("Hello");
    let t = &s;           // s를 빌림. ownership은 s에 남음
    println!("{s} {t}");   // 둘 다 사용 가능
}
```

길 둘이 더 가볍다. 데이터를 복사하지 않는다. 다만 *어떤 규칙으로 빌림이 안전을 보장하는지*가 5장의 본문이다. 일단 *두 길이 있다는 것*까지 손에 묻혀두자.

## NPE는 어디로 갔을까

여기서 한 가지 흥미로운 사실을 짚고 가자. *Rust에는 null이 없다*. 변수의 값이 *비어있을 가능성*을 표현하려면 `Option<T>`라는 enum을 *명시적으로* 써야 한다.

```rust
// Java 스타일 (Rust에선 컴파일 안 됨)
// String name = null;          // 이 자체가 문법 에러

// Rust 스타일
let name: Option<String> = None;            // 비어있음을 명시
let name2: Option<String> = Some(String::from("toby"));   // 값 있음

match name2 {
    Some(s) => println!("이름: {s}"),
    None => println!("이름이 없음"),
}
```

3장에서 잠깐 본 *exhaustive match*가 여기서 진짜로 빛난다. *Some 케이스만 처리하고 None을 빼먹으면* 컴파일러가 거부한다. Java의 `Optional<T>`도 비슷한 의도를 가지지만, `optional.get()`을 *그냥 호출해서 NPE 비슷한 NoSuchElementException을 받는* 코드가 너무 흔하다. Rust는 그 우회로를 *언어 차원에서 막아둔다*. `Option<String>`을 그냥 `String`처럼 쓸 수가 *없다*.

자세한 처방은 7장 에러 처리에서 본다. 지금 단계에서는 *"null이 아예 없다는 사실"* 그리고 *"NPE라는 사고 카테고리가 언어에서 사라진다는 사실"*만 손에 묻혀두자. 이게 1장에서 적어둔 운영 사고 메모가 NPE였다면, *그 사고는 Rust로 짠 순간 컴파일 타임에 잡혔을 것이다*. 7장에서 다시 만나자.

## `Box<T>` 살짝 — heap에 의도적으로 올리고 싶을 때

규칙 1·2·3까지 익혔다면 한 가지 의문이 들 수 있다. *"struct 같은 것도 매번 스택에 들어가나? heap에 올리고 싶으면?"* 답이 `Box<T>`다.

```rust
let on_stack: User = User::new(...);             // 스택에 직접
let on_heap: Box<User> = Box::new(User::new(...)); // heap에 잡고 핸들이 스택에
```

`Box<T>`는 *가장 단순한 스마트 포인터*다. *값을 heap에 올리고, 그 값의 owner는 Box 자신*이다. 함수에 넘기면 Box의 ownership이 이동하고, scope를 벗어나면 Box가 drop되면서 *heap 데이터까지 함께 회수*된다. 즉 *Box도 같은 세 가지 규칙을 따른다*.

*언제 Box가 필요한가*는 처음에는 잘 안 떠오를 수 있다. 가장 흔한 세 가지 상황만 알아두자.

1. *재귀적 자료구조* — 트리, 연결 리스트처럼 *자기 자신을 포함*하는 타입. 컴파일 타임에 크기가 무한히 커질 수 있어서 *스택에 직접 못 둔다*.
2. *큰 struct를 함수 사이로 옮기는 게 비싼 경우* — 비트 단위 복사 비용을 줄이려고 *포인터만 옮기는* 패턴.
3. *trait object* — `Box<dyn Trait>` 형태로 *다형성*을 표현 (8장 본격).

지금은 *"Box가 있다는 사실"*과 *"heap에 직접 올리고 싶을 때 쓴다"*만 손에 묻혀두자. 8장에서 `Rc<T>`, `Arc<T>`, `RefCell<T>`까지 *스마트 포인터의 전체 지도*를 그린다.

## 한국 개발자의 후기 한 줄

이 장의 무게를 *체험적으로* 한 번 환기하자. 4년간 Rust를 써온 한 한국 개발자가 자기 블로그에 이렇게 적었다. *"익숙해지면 사고가 정리되는 느낌이고, 한 번 작동하면 정말 잘 작동한다."*[^1]

이 한 줄에 두 가지 의미가 들어 있다.

첫째, *"익숙해지면"*. 익숙해지기 전까지는 답답하다는 솔직한 인정이다. corrode의 마이그레이션 가이드도 *4~6개월의 적응 기간*을 권한다.[^2] 처음 한 달은 *컴파일러가 너무 까다롭게* 느껴진다. 두 달째에 *"왜 이렇게 까다롭게 굴었는지"*가 보인다. 석 달째에 *손가락이 익는다*. 이 곡선은 누구도 건너뛰지 못한다.

둘째, *"한 번 작동하면 정말 잘 작동한다"*. 익숙해진 뒤의 보상이다. NPE도, 메모리 누수도, double-close도, 데이터 레이스도(다음 장) *컴파일러가 다 잡아준다*. 운영 중인 시스템에서 *"왜 이게 죽지?"라는 의문이 줄어든다*. 십 년 동안 우리가 *알람 받고 새벽에 깨던* 그 카테고리가 *대부분 사라진다*. 그 보상이 4~6개월의 답답함을 정당화한다.

## 마무리 — 다음 장으로의 다리

이 장에서 한 일을 정리해보자. *세 가지 단순한 규칙*을 봤다. *주인은 한 명*, *scope 종료 시 즉시 drop*, *대입과 전달은 move*. 이 세 줄이 NPE·memory leak·use-after-free·double-free를 *동시에* 차단한다는 것을 손에 담았다. `Copy` 트레잇이 *작은 예외*를 만들고, `String`과 `&str`이 *왜 두 개로 나뉘는지*가 풀렸다. `Drop`이 *결정적 자원 해제*를 약속한다는 것도 봤다.

기억해두자. *이 장의 답답함은 정상이다*. 모든 JVM 출신이 같은 자리에서 한 달 정도 답답해한다. 그 답답함이 *5장에서 깨끗이 풀린다*. *빌림*이라는 두 줄의 규칙으로, *"함수에 넘기고 나서도 계속 쓰고 싶다"*는 자연스러운 욕구가 *컴파일러와 충돌하지 않게* 표현된다. 그리고 그 두 줄의 규칙이 다시 *데이터 레이스를 컴파일 타임에 차단*하는 자리(9장 Send/Sync)로 이어진다. *모든 것이 연결돼 있다*.

다음 장 가기 전에 한 가지를 약속하자. *컴파일러가 거부하는 코드가 있을 때, 화내지 말자*. 그 메시지를 *공책에 옮겨 적고 한 줄씩 읽어보자*. 처음에는 시간이 걸리지만, *그 습관이 두 달 뒤의 풍경을 만든다*. borrow checker는 *적이 아니라 코드를 함께 짜는 시니어*다.

## 함께 해보자

다음 코드를 한번 손으로 짜보자. *일부러 컴파일이 안 되는 모양*으로 시작한다.

```rust
fn main() {
    let s = String::from("Hello, Rust!");
    let t = s;
    println!("{s}, {t}");        // 컴파일 에러
}
```

`cargo build`(또는 `cargo check`)로 에러 메시지를 띄우고, 그 메시지를 *처음부터 끝까지 한 줄씩 읽어보자*. 다음 네 가지를 손으로 직접 시도해보자.

1. *clone()으로 풀기*. `let t = s.clone();`로 바꿔 컴파일을 통과시키자. *어떤 일이 일어났는지* 한 단락으로 적어보자(heap에 무엇이 일어났는가?).

2. *borrow로 풀기*. `let t = &s;`로 바꿔 컴파일을 통과시키자. clone과 비교해 *데이터 측면에서 무엇이 다른가*를 한 단락으로 적어보자.

3. *함수로 풀어보기*. 다음 코드를 짜고 동작을 확인하자.
   ```rust
   fn print_string(s: String) {
       println!("{s}");
   }

   fn main() {
       let s = String::from("Hello");
       print_string(s);
       // print_string(s);       // 두 번째 호출에서 에러
   }
   ```
   왜 두 번째 호출이 에러인지를 *세 줄의 규칙*으로 설명해보자.

4. *Drop을 직접 구현해보기*. 다음 코드를 짜고 출력 순서를 확인해보자.
   ```rust
   struct Logger { name: String }

   impl Drop for Logger {
       fn drop(&mut self) {
           println!("Logger '{}' 종료", self.name);
       }
   }

   fn main() {
       let _a = Logger { name: "A".to_string() };
       {
           let _b = Logger { name: "B".to_string() };
           println!("내부 블록");
       }
       println!("외부 블록");
   }
   ```
   출력 순서를 *예측해본 뒤* 실행 결과와 비교해보자. *왜 B가 먼저 종료되고, A는 main의 끝에서 종료되는가?*

이 4번 예제는 *RAII의 가장 작은 모양*이다. 이 출력 순서가 *예측 가능*하다는 사실이 운영 환경에서 어떤 안심감을 주는지를 두 달쯤 뒤에 다시 떠올려보자.

다음 장에서는 *빌림(borrowing)*을 본다. *"한 명만 가진다"*는 규칙을 깨지 않으면서, *"잠깐 빌려쓰는"* 길을 푸는 *두 줄의 규칙*이 등장한다. 그리고 그 두 줄이 *데이터 레이스를 컴파일 타임에 차단*하는 자리로 9장에서 다시 호출된다. *연결이 시작된다*.

---

## 참고

[^1]: ["4년간의 Rust 사용 후기" — blog.cro.sh](https://blog.cro.sh/posts/four-years-of-rust/).
[^2]: ["Migrating from Java to Rust" — corrode](https://corrode.dev/learn/migration-guides/java-to-rust/).

---

# 5장. 빌림 — `&T`와 `&mut T`, 그리고 데이터 레이스가 사라지는 이유

처음 몇 주, borrow checker가 우리 코드를 거부할 때면 어쩌면 자기 자신을 의심하게 된다. "10년을 써온 패턴인데, 왜 이게 컴파일이 안 되지?" Java에서는 너무나 당연했던 코드 — 참조 변수 두 개로 같은 객체를 가리키고, 한쪽에서 값을 바꾸면서 다른 쪽으로 읽는 그 일상의 코드 — 가 Rust에서는 빨갛게 거부된다. 난감하다. 그런데 4장의 소유권을 받아들이고 나면, 빌림은 그 답답함의 *해방구*다. ownership을 옮기지 않고도 데이터를 잠깐 빌려주는 도구가 바로 `&T`와 `&mut T`다. 그리고 이 두 줄짜리 규칙이, 놀랍게도, 우리가 지난 20년 동안 `synchronized`와 `ConcurrentModificationException`으로 골머리 앓던 그 문제를 *컴파일 타임에* 끝낸다.

이 한 문장이 너무 큰 약속처럼 들릴지 모르겠다. 하지만 천천히 따라와 보자. 5장이 끝날 때쯤이면 이 약속이 과장이 아니었다는 사실을 손으로 만져본 상태가 되어 있을 것이다.

## 4장의 그 코드를 다시 풀어보자

4장 함께해보자에서 우리는 다음 코드와 마주쳤다.

```rust
let s = String::from("hi");
let t = s;
println!("{s}");   // 컴파일 에러: borrow of moved value: `s`
```

`let t = s`에서 `String`의 ownership이 `t`로 *이동*했고, 그래서 `s`는 빈 껍데기가 됐다. 4장 처방 ①은 `clone()`이었다. 죄책감 없이 복사하라고 했다. 하지만 죄책감이 없다고 해서 비용이 없는 건 아니다. heap에 올려둔 문자열을 통째로 또 한 번 복제하는 일이다. 64바이트짜리 짧은 문자열이라면 모르겠다. 64MB짜리 이미지 버퍼라면? 매 함수 호출마다 그렇게 복제할 수는 없다. 그러면 어떻게 해야 할까?

답이 빌림이다. ownership을 옮기지 말고, 잠깐 *빌려주자*.

```rust
let s = String::from("hi");
let t = &s;          // s의 immutable borrow
println!("{s}, {t}");  // 둘 다 살아있다
```

`&s`는 "`s`의 데이터를 가리키는, 잠깐 빌린 참조"다. ownership은 여전히 `s`가 가지고 있다. `t`는 그 데이터를 *읽을 권한*만 빌렸을 뿐이다. 그래서 `s`도 살아있고 `t`도 살아있다. 함수에 넘길 때도 마찬가지다.

```rust
fn print_len(value: &String) {
    println!("길이는 {}", value.len());
}

let s = String::from("hello");
print_len(&s);
println!("{s}");   // s는 여전히 살아있다
```

JVM에서는 이게 너무나 당연한 코드여서, 따로 설명할 게 없다. Java로 옮기면 한 줄이다. `void printLen(String value) { ... }`. 그런데 Rust는 왜 이렇게 두 가지(`String`과 `&String`)를 구분하는 걸까? 그 이유가 다음 절에서 본격적으로 드러난다.

## 두 줄의 규칙

Rust의 빌림에는 단 두 줄의 규칙이 있다. 외워둘 가치가 충분하다.

1. 한 시점에 mutable borrow(`&mut T`)는 **단 하나만** 존재할 수 있다.
2. mutable borrow가 살아있는 동안 다른 어떤 borrow도(immutable이든 mutable이든) 존재할 수 없다.

뒤집어 말하면, immutable borrow(`&T`)는 *얼마든지 동시에* 존재할 수 있다. 읽기만 하는 한, 여러 명이 동시에 봐도 아무 문제가 없다. 하지만 누군가가 *쓸 권한*을 가지는 순간, 그 사람 외에는 아무도 그 데이터를 볼 수 없다. 이걸 한 줄로 줄이면 *"여러 명이 같이 읽거나, 아니면 한 명만 쓰거나"*다.

JVM 출신에게 이 규칙은 처음에는 답답하게 들린다. "그러면 동시에 두 군데서 수정하고 싶을 때는 어떻게 하나?"라는 질문이 자연스럽게 떠오른다. 그 답은 *컴파일러가 거부한다*는 것이다. 그리고 그게 5장의 핵심 주장이다 — *그 거부가 사실은 우리에게 보상*이라는 것.

코드로 보자.

```rust
let mut v = vec![1, 2, 3];
let r1 = &v;
let r2 = &v;
println!("{:?}, {:?}", r1, r2);   // OK: 읽기만 하는 두 borrow는 공존 가능
```

여기까지는 문제없다. `r1`과 `r2`는 둘 다 `&Vec<i32>`다. 둘이서 동시에 읽기만 한다. 그런데 한 줄을 더해보자.

```rust
let mut v = vec![1, 2, 3];
let r1 = &v;
let r2 = &mut v;            // 컴파일 에러
println!("{:?}, {:?}", r1, r2);
```

컴파일러는 이렇게 거부한다.

```
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> src/main.rs:4:14
  |
3 |     let r1 = &v;
  |              -- immutable borrow occurs here
4 |     let r2 = &mut v;
  |              ^^^^^^ mutable borrow occurs here
5 |     println!("{:?}, {:?}", r1, r2);
  |                            -- immutable borrow later used here
```

처음 보면 불친절해 보이지만, 자세히 들여다보면 *컴파일러가 손가락으로 줄·열을 짚어주고 있다*. immutable borrow가 어디서 시작됐는지(3번째 줄), mutable borrow가 어디서 충돌하는지(4번째 줄), 그리고 *왜* 거부했는지(5번째 줄에서 immutable borrow가 여전히 사용되기 때문). rustc 에러 메시지를 *읽는 법*을 3장 끝에서 한 번 짚었던 이유가 여기에 있다. 빌림 에러는 무서워 보이지만 사실은 *해결 방법까지 친절히 알려주는* 메시지다.

## 왜 이 규칙이 데이터 레이스를 끝내는가

이제 본격적인 한 줄을 짚어보자. *왜 이 두 줄의 규칙이 동시성 안전성으로 이어지는가?*

데이터 레이스(data race)의 정의를 먼저 떠올려보자. "두 개 이상의 스레드가 같은 메모리 위치에 동시에 접근하고, 그 중 적어도 하나가 *쓰기*이며, 그 접근들이 동기화되어 있지 않을 때" 발생하는 현상이다. JVM에서는 이걸 막기 위해 우리는 평생을 `synchronized`, `ReentrantLock`, `volatile`, `AtomicReference`, `ConcurrentHashMap`을 써왔다. 잘 썼나? 못 썼다. 운영 사고 통계를 보면 안다. NPE 다음으로 많은 게 race condition이다. 왜냐하면 *컴파일러가 강제하지 않기 때문*이다.

Rust의 두 줄 규칙을 다시 보자.

1. 한 시점에 `&mut T`는 단 하나만.
2. `&mut T`가 살아있는 동안 다른 어떤 borrow도 없다.

이 규칙을 만족하는 코드는 *정의상* 데이터 레이스가 일어날 수 없다. 두 스레드가 같은 메모리에 동시에 접근하려면 둘 다 borrow를 들고 있어야 하는데, 그 중 하나라도 `&mut`이면 다른 borrow의 존재 자체가 컴파일 거부다. 둘 다 `&T`(읽기)뿐이라면 동시 접근이 일어나도 아무도 쓰지 않으니 race가 아니다.

이게 *concurrency safety*가 *컴파일 타임*에 보장된다는 말의 의미다. Rust 표준 라이브러리는 여기에 `Send`와 `Sync`라는 마커 트레잇을 더해서 *어떤 타입이 스레드 사이를 안전하게 오갈 수 있는지*까지 타입 시스템에 박아놓았다. 그 이야기는 9장의 몫이다. 5장에서는 *그 토대가 빌림 규칙*이라는 사실만 가져가자.

JVM에서 우리가 흔히 마주치던 시나리오를 떠올려보자. `@Service`에 `private List<Order> orders = new ArrayList<>();`를 두고, 두 메서드가 동시에 그것을 수정한다고 해보자. 컴파일러는 아무 말이 없다. 잘 돌아가는 줄 알았는데 운영에서 `ConcurrentModificationException`이 터진다. 또는 더 무서운 경우 — 예외 없이 *데이터가 조용히 깨진다*. 우리는 그걸 막으려고 `Collections.synchronizedList`로 감싸거나 `CopyOnWriteArrayList`로 바꾸거나 `ConcurrentHashMap`을 끌어온다. 이 모든 결정이 *런타임에·관행으로·코드 리뷰로* 보장되는 것이다.

Rust에서 같은 자료 구조를 두 메서드가 동시에 수정하려고 하면? 빌림 단계에서부터 컴파일이 거부된다. 만약 그 자료 구조를 *진짜로 두 스레드가 공유해야* 한다면, 우리는 명시적으로 `Arc<Mutex<Vec<Order>>>` 같은 모양을 골라야 한다(8장에서 본격적으로 다룬다). 그 *선택이 코드에 박혀* 있다는 사실이, 6개월 뒤 가장 큰 보상이 된다.

한 줄로 정리하자. **Java의 모든 객체 참조는 늘 mutable이고 동시 접근이 허용된다 — Rust는 그 일상 코드를 컴파일러가 거부한다.** 이 비대칭이 5장의 핵심이다. 흔히 "&T는 final 참조와 같다"고 단순화하는 설명을 만나게 되는데, 그건 정확하지 않다. Java의 `final` 참조는 *재할당 금지*일 뿐, 그 객체의 내부 필드를 바꾸는 것은 막지 못한다. `final List<String> list = new ArrayList<>();` 다음에 `list.add("hi");`는 멀쩡히 동작한다. 반면 `&Vec<String>`은 *그 안의 내용까지* 바꿀 수 없다. 두 개념은 의미 자체가 다르다.

## `&mut T`는 정말 한 명만 — 그 뜻을 손으로 만져보자

작은 카운터 구조체로 두 줄 규칙을 직접 두드려보자.

```rust
struct Counter {
    count: i32,
}

impl Counter {
    fn increment(&mut self) {
        self.count += 1;
    }

    fn value(&self) -> i32 {
        self.count
    }
}

fn main() {
    let mut c = Counter { count: 0 };
    let r1 = &mut c;
    let r2 = &mut c;        // 컴파일 에러
    r1.increment();
    r2.increment();
    println!("{}", c.value());
}
```

컴파일러가 거부한다.

```
error[E0499]: cannot borrow `c` as mutable more than once at a time
 --> src/main.rs:4:14
  |
3 |     let r1 = &mut c;
  |              ------ first mutable borrow occurs here
4 |     let r2 = &mut c;
  |              ^^^^^^ second mutable borrow occurs here
5 |     r1.increment();
  |     -- first borrow later used here
```

두 개의 mutable borrow를 동시에 가지려 했으니 거부된다. 그러면 어떻게 고쳐야 할까? 여기서 NLL(Non-Lexical Lifetimes)이라는, 컴파일러의 한 단계 진화를 만나게 된다.

## NLL — borrow checker가 *덜 까칠해진* 이유

NLL은 Rust 2018 에디션에서 안정화된 기능이다. *Non-Lexical Lifetimes*, "어휘적이지 않은 라이프타임"이라는 다소 어려운 이름이지만, 의미는 단순하다. *borrow가 살아있는 기간을 컴파일러가 더 똑똑하게 판단해준다*는 뜻이다.

NLL 이전에는 borrow가 *변수의 scope 끝까지* 살아있다고 봤다. 그래서 한 번 빌리면 그 변수가 닫히는 `}`까지는 다른 borrow를 못 만들었다. NLL 이후에는 borrow가 *마지막으로 사용되는 지점까지만* 살아있다고 본다. 이 차이가 일상의 답답함을 크게 줄여준다.

위 카운터 코드를 NLL이 풀어주는 패턴으로 다시 써보자.

```rust
fn main() {
    let mut c = Counter { count: 0 };
    {
        let r1 = &mut c;
        r1.increment();
    }   // r1의 borrow는 여기서 끝난다
    {
        let r2 = &mut c;
        r2.increment();
    }
    println!("{}", c.value());
}
```

스코프를 명시적으로 좁혀줬다. `r1`이 끝난 뒤에야 `r2`가 시작되니, 두 mutable borrow가 동시에 살아있지 않다. 그런데 NLL 덕분에 사실 더 짧게 써도 된다.

```rust
fn main() {
    let mut c = Counter { count: 0 };
    let r1 = &mut c;
    r1.increment();
    // r1은 여기서 마지막으로 쓰였으니, 컴파일러는 borrow가 끝났다고 본다
    let r2 = &mut c;
    r2.increment();
    println!("{}", c.value());
}
```

`{ }` 블록 없이도 컴파일이 통과한다. `r1.increment();` 이후 `r1`이 다시 등장하지 않으면, NLL은 그 시점에 `r1`의 borrow가 *살아있지 않다고* 판단한다. 그러니 그 다음 줄의 `&mut c`가 충돌하지 않는다.

NLL이 도입되기 전 Rust(2015 에디션 이전)에서는 이런 코드도 거부됐다. 그래서 빌림과의 싸움이 더 잦았다. 지금 우리가 만나는 borrow checker는 *훨씬 더 친절해진 후* 모습이다. 처음에는 그래도 답답하겠지만, "이건 NLL이 풀어줄 수 있는 패턴인가?"를 한 번 더 생각해보면 의외로 풀리는 경우가 많다.

## reborrow — 빌림을 또 빌리기

함수에 `&mut T`를 넘기는 상황에서 자주 만나는 개념이 reborrow다. 코드부터 보자.

```rust
fn add_one(value: &mut i32) {
    *value += 1;
}

fn add_many(value: &mut i32) {
    add_one(value);   // value를 다시 빌려준다
    add_one(value);
    add_one(value);
}
```

`add_many`는 `&mut i32`를 받았다. 그것을 `add_one`에 넘기는 순간, ownership이 옮겨갈까? `&mut T`도 일종의 값이니 옮겨가는 게 자연스럽다. 그런데 옮겨갔다면 `add_one(value)`를 두 번째로 부를 때 `value`는 *더 이상 사용할 수 없는 moved value*가 되어야 한다. 그런데 위 코드는 멀쩡히 동작한다. 왜?

답이 reborrow다. Rust는 `add_one(value)` 호출 시 `&mut *value`로 *암묵적으로 reborrow*한다. 즉 "내가 가진 mutable borrow에서 잠깐 또 다른 mutable borrow를 만들어 함수에 넘기되, 그 함수 호출이 끝나면 빌림이 회수된다." `add_one`이 리턴하면 그 reborrow는 끝나고, `add_many`의 `value`는 다시 사용 가능해진다. 그 덕분에 두 번째, 세 번째 호출이 자연스럽게 이어진다.

이 reborrow는 *대부분 자동*이라서 우리가 명시적으로 적을 일이 거의 없다. 하지만 컴파일러가 가끔 거부할 때가 있다. 그럴 때 `add_one(&mut *value)`처럼 명시적으로 reborrow를 적어주면 풀리는 경우가 있다는 정도만 머리에 두자.

## 자주 만나는 에러 메시지 사전

처음 한 달 동안 가장 많이 마주치는 borrow 에러 메시지를 정리해두자. 처방까지 한 줄로 묶어서 가져가는 편이 낫다.

**`borrow of moved value: 'x'`**
4장에서 만났던 에러다. `let t = s;`로 ownership이 옮겨간 뒤 `s`를 다시 쓰려 할 때 나온다. 처방: ownership을 정말로 옮겨야 하는지 다시 생각해보자. 옮길 필요가 없으면 `&s`로 빌려주는 편이 낫다. 정말로 옮겨야 한다면 `s.clone()`으로 복제하거나, 호출 후에 `s`를 안 쓰면 된다.

**`cannot borrow 'x' as mutable because it is also borrowed as immutable`**
방금 본 그 에러다. immutable borrow가 살아있는 동안 mutable borrow를 만들 수 없다. 처방: immutable borrow의 사용 범위를 좁혀라(NLL이 풀어준다). 또는 둘을 *순차적으로* 분리하라.

**`cannot borrow 'x' as mutable more than once at a time`**
mutable borrow는 단 하나만 가능하다. 두 개를 동시에 만들려고 했을 때 나온다. 처방: 한쪽이 끝난 뒤 다른 쪽을 시작하라. 또는 *진짜로* 두 군데서 쓸 권한이 필요하다면 자료 구조를 다시 설계하자(8장의 `Rc<RefCell<T>>` 또는 `Arc<Mutex<T>>`).

**`'x' does not live long enough`**
빌림이 가리키는 데이터가 *빌림보다 먼저 사라진다*는 뜻이다. 6장 라이프타임에서 본격적으로 다룰 영역이다. 처방: 빌림의 lifetime을 데이터의 lifetime 안으로 좁히거나, 데이터를 더 오래 살게 만들거나, ownership을 옮기자.

**`cannot move out of borrowed content`**
빌린 것에서 *값을 가져오려* 했을 때 나온다. `&Vec<String>`에서 `String` 하나를 꺼내려고 하면 거부된다. 처방: `clone()`하거나, `vec.iter()`로 빌림으로만 순회하거나, `vec.into_iter()`로 ownership을 *통째로* 가져오자.

이 다섯 가지 패턴이 첫 한 달의 80%를 차지한다. 외우려고 애쓸 필요는 없다. 컴파일러가 매번 손가락으로 짚어준다. 그 손가락을 *동료의 조언*으로 받아들이는 자세, 그게 첫 처방이다. 한국의 한 시니어 개발자가 4년의 경험을 정리하며 쓴 한 줄을 그대로 가져오자. *"익숙해지면 사고가 정리되는 느낌이고, 한 번 작동하면 정말 잘 작동한다."* 빌림 단계의 첫 한 달을 지나면 그 감각이 천천히 손에 묻기 시작한다.

## 이 두 줄의 규칙은 학술적으로 입증됐다

5장의 마지막 한 절이다. 잠시 깊은 곳을 한 번 들여다보자.

지금까지 우리는 "두 줄의 규칙이 데이터 레이스를 끝낸다"고 말했다. 이 주장이 그저 *Rust 커뮤니티의 관행적 자신감*일까, 아니면 *학술적으로도 검증된* 사실일까? 답은 후자다. 그리고 그 사실을 알고 나면 우리가 지금 배우는 두 줄 규칙의 무게가 한 단계 다르게 다가온다.

2018년 POPL(Principles of Programming Languages) 학회에 「RustBelt: Securing the Foundations of the Rust Programming Language」라는 논문이 실렸다. Ralf Jung과 그의 동료들(MPI-SWS)이 *Rust 언어의 type system이 메모리 안전성과 스레드 안전성을 보장한다*는 사실을 *기계 검증된(machine-checked) 형식 증명*으로 보였다. 이는 현실적인 부분집합의 Rust에 대한 *최초의 형식 안전성 증명*이었다. 즉, Rust가 안전하다는 주장이 *경험과 직관*이 아니라 *수학적 증명*에 의해 뒷받침된다.

그 후속 작업으로 같은 그룹은 2020년 POPL에 「Stacked Borrows: An Aliasing Model for Rust」를 발표했다. 이 논문은 `unsafe`를 포함한 코드에서 *borrow의 의미*를 어떻게 정의해야 하는지를 모델링했다. 그리고 2025년 PLDI(Programming Language Design and Implementation)에는 그 후속인 「Tree Borrows」가 실렸다. Stacked Borrows의 한계를 보완해서, 더 많은 실제 코드 패턴이 *모델 안에서 안전하다*고 인정받을 수 있게 해주는 모델이다.

이 세 편의 흐름이 우리에게 주는 메시지는 한 줄이다. *Rust의 두 줄 규칙은 그저 컴파일러 구현자의 직관이 아니다.* 별도의 학계가 *형식적으로 검증된 모델*을 가지고 *언어의 안전성을 증명*해왔고, 그 모델은 unsafe 코드 영역까지 확장되어 검증되고 있다. 우리가 지금 손으로 두드려본 그 두 줄의 규칙은, 그 어떤 다른 언어도 이 정도로 *학술적 토대 위에서* 만들어지지 않았다.

깊이 들어갈 필요는 없다. 학회 논문을 직접 읽지 않아도 된다. 그저 *우리가 배우는 것이 입증된 안전성*이라는 사실을 한 번 짚어두는 것으로 충분하다. 8장 unsafe 절에서 이 한 단락을 한 번 더 회수하게 된다 — *unsafe라도 검증할 수 있는 형태로* 모델이 만들어진 이유가 거기서 명료해진다.

## 함께 해보자

작은 카운터 구조체 하나를 직접 손으로 두드려보자. 다음 두 가지를 차례로 시도해보고 컴파일러의 메시지를 *손가락으로 짚어가며* 읽어보자.

1. 위에서 살펴본 `Counter`에서, 동시에 두 개의 `&mut`을 만들어보자. 컴파일러가 어느 줄에서 거부하는지, 그리고 어떤 노트(note)와 도움말(help)을 함께 보여주는지 적어보자.
2. NLL이 풀어주는 패턴(스코프 좁히기 또는 마지막 사용 지점 이후로 borrow 종료)으로 같은 코드를 고쳐보자. 어떤 변형이 통과하고 어떤 변형이 여전히 거부되는지 한 줄씩 비교해보자.

이 카운터는 9장 `Arc<Mutex<T>>` 절에서 *멀티스레드 안전성*으로 다시 호출된다. 두 줄의 규칙이 단일 스레드에서 어떻게 동시성 안전성으로 번역되는지를, 그때 한 단계 더 깊이 이해하게 된다.

빌림의 두 줄 규칙은 머리로 외우는 게 아니라 손에 묻히는 규칙이다. 처음 한 달은 매일 컴파일러와 짧은 대화를 나누며 살게 된다. 그 대화가 답답하게 느껴질 때, 한 가지만 기억해두자 — *이 규칙은 우리가 지난 20년 동안 런타임에서 잡으려 애쓰던 그 사고들을 컴파일 타임으로 옮겨주는, 학술적으로 검증된 안전망*이다. 그 안전망을 친구로 받아들이는 데까지 4~6개월. 그 시간이 지나면 빌림은 더 이상 적이 아니다.

다음 6장에서는 빌림과 짝을 이루는 *라이프타임*을 다룬다. `'a` 어노테이션이 처음 등장할 때의 그 막막함, 그리고 *사실 우리가 명시적으로 라이프타임을 적는 일은 한 손에 꼽을 정도라는* 안도감을 함께 가져가자.

---

## 참고

- [Rust ownership and borrows: Fighting the borrow-checker — DEV.to](https://dev.to/daaitch/rust-ownership-and-borrows-fighting-the-borrow-checker-4ea3)
- [The Borrow Checker: Rust's Tough-Love Mentor](https://www.woodruff.dev/the-borrow-checker-rusts-tough-love-mentor/)
- [Rust for Java Developers — Ownership](https://tkaitchuck.github.io/Rust4JavaDevelopers/ownership.html)
- Jung, R., Jourdan, J.-H., Krebbers, R., Dreyer, D. — [RustBelt: Securing the Foundations of the Rust Programming Language (POPL 2018)](https://plv.mpi-sws.org/rustbelt/popl18/paper.pdf)
- Jung, R., Dang, H.-H., Kang, J., Dreyer, D. — [Stacked Borrows: An Aliasing Model for Rust (POPL 2020)](https://plv.mpi-sws.org/rustbelt/stacked-borrows/paper.pdf)
- Villani, N., Hostert, J., Dreyer, D., Jung, R. — [Tree Borrows (PLDI 2025)](https://iris-project.org/pdfs/2025-pldi-treeborrows.pdf)
- [Send and Sync — The Rustonomicon](https://doc.rust-lang.org/nomicon/send-and-sync.html)
- [4년간의 Rust 사용 후기 — blog.cro.sh](https://blog.cro.sh/posts/four-years-of-rust/)

---

# 6장. 라이프타임 — `'a`라는 메타데이터에 익숙해지자

5장에서 빌림의 두 줄 규칙과 친구가 되었다. 그런데 잠깐, 한 가지가 남아있다. 함수 시그니처에서 가끔 본 적 있을 것이다 — `fn longest<'a>(x: &'a str, y: &'a str) -> &'a str` 같은, 따옴표 하나에 알파벳 한 자가 붙은 *그 이상한 표기*. 처음 보면 난감하다. *왜 이게 있어야 하지? 이걸 매번 적어야 하나?* 한국의 한 시니어 개발자가 4년의 경험을 정리하며 솔직하게 적은 한 줄이 있다. *"slices from String differences and lifetime annotations ('a, 'static)은 명료히 이해하기 어렵다."* 이 공감을 먼저 짚고 시작하자. 라이프타임이 어렵게 느껴지는 건 *우리만의 문제*가 아니다.

그런데 이 챕터를 읽기 전에 미리 한 가지 안도감을 가져가자. **사실 우리가 명시적으로 라이프타임을 적는 일은 한 손에 꼽을 정도다.** 입문자가 매일 보는 함수의 99%는 `'a`를 적지 않는다. 컴파일러가 알아서 추론해준다. 라이프타임 어노테이션이 *진짜로 등장해야 하는* 패턴은 사실 정해져 있다. 그 패턴을 인식하는 게 6장의 목표다. 그러고 나면 라이프타임은 더 이상 신비한 무엇이 아니다 — *컴파일러에게 우리가 알고 있는 사실 하나를 알려주는 메타데이터*일 뿐이다.

## 라이프타임이 뭘 하는 도구인가

먼저 한 줄 정의부터 잡자. **라이프타임은 *런타임 비용 0의 컴파일러 메타데이터*다.** 참조가 가리키는 데이터보다 참조가 *더 오래 살지 않는지*를 컴파일러가 검증할 때 쓰는 도구다. 런타임에는 아무 것도 일어나지 않는다. `'a`는 컴파일이 끝나면 사라진다 — 메모리에 차지하는 자리가 없고, CPU 사이클을 쓰지도 않는다.

왜 이런 게 필요할까? 5장에서 본 것처럼 빌림은 *데이터를 빌려주는* 행위다. 그러면 한 가지 위험이 따라온다 — *원본 데이터가 사라진 뒤에도 빌림이 살아있으면?* 빌림이 가리키는 곳에는 더 이상 우리가 빌렸던 그 데이터가 없다. 다른 데이터가 들어와 있을 수도 있고, 비어있을 수도 있다. 이걸 dangling reference라고 부른다. C에서는 흔한 사고다. `int* p = &local_var; ... return p;`로 함수 종료 후에도 살아있는 포인터를 만들면, 그 포인터를 따라가는 순간 무엇이 나올지 모른다.

Rust는 이걸 *컴파일 타임에 100% 차단*한다. 어떻게? 모든 참조에 *살아있을 기간(lifetime)을 추적*해서, 참조가 그 기간을 벗어나는 시점에 컴파일을 거부한다. 그 추적이 가능하도록 컴파일러가 알아야 하는 정보가 바로 라이프타임 어노테이션이다.

JVM에서는 이런 일이 *런타임에* 일어난다. GC가 객체의 reachability를 추적해서, *어떤 객체에 대한 참조가 더 이상 도달 불가능*해지면 그 객체를 회수한다. "참조가 가리키는 객체가 먼저 사라지는" 일은 GC 덕분에 *원천적으로 일어날 수 없다*. 그 대가로 우리는 GC pause를 받아들이고, *어떤 객체가 언제까지 살아 있는가*를 *짐작은 해도 강제는 못 하는* 상태로 산다. Rust는 그 결정 시점을 *컴파일 타임으로 옮긴* 대신, *컴파일러에게 일러주는 비용*을 가끔 우리에게 청구한다 — 그 비용이 `'a` 어노테이션이다.

JVM 출신이 라이프타임을 어렵게 느끼는 진짜 이유는 문법이 아니다. *"메모리 lifetime을 내가 직접 사고해본 적이 없다"*는 사고의 공백이다. 우리가 Java나 Kotlin으로 일하는 동안 객체가 언제 살고 죽는지를 한 번도 직접 따져본 적이 없으니, *직접 따져야 한다는 사실 자체*가 낯선 것이다. 그러니 처방은 단순하다 — *예제 → 컴파일러와의 대화 → 패턴 인식*. 천천히 가자.

## 함수 시그니처에서의 `'a`

가장 많이 인용되는 예제가 두 문자열 슬라이스 중 더 긴 쪽을 반환하는 함수다.

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
```

처음 보면 `'a`가 세 군데 박혀있어서 머리가 아프다. 한 번 풀어 읽어보자.

- `<'a>`: 이 함수는 `'a`라는 이름의 라이프타임을 *받는다*. 제네릭 타입 파라미터처럼, 라이프타임도 일종의 파라미터다.
- `x: &'a str`, `y: &'a str`: 두 입력 참조는 *모두 `'a`만큼 살아있다*고 컴파일러에게 약속한다.
- `-> &'a str`: 반환되는 참조도 *최소 `'a`만큼 살아있다*고 보증한다.

이게 왜 필요한가? `longest`는 `x` 또는 `y` 중 하나를 반환한다. 컴파일러는 *어느 쪽을 반환할지 호출 시점에 결정되니* 미리 알 수 없다. 그러니 *반환되는 참조의 lifetime은 입력 두 개의 lifetime 중 더 짧은 쪽*이어야 안전하다. `'a`라는 한 글자로 그 관계를 표현한 것이다. *세 참조가 모두 `'a`로 묶인다 — 셋 중 가장 짧은 lifetime이 `'a`*. 그러면 호출자는 반환된 참조를 안전하게 사용할 수 있다.

이걸 적지 않으면 어떻게 될까?

```rust
fn longest(x: &str, y: &str) -> &str {  // 컴파일 에러
    if x.len() > y.len() { x } else { y }
}
```

```
error[E0106]: missing lifetime specifier
 --> src/main.rs:1:33
  |
1 | fn longest(x: &str, y: &str) -> &str {
  |               ----     ----     ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the
          signature does not say whether it is borrowed from `x` or `y`
```

컴파일러가 친절히 설명해준다 — *반환 타입이 `x`에서 빌린 건지 `y`에서 빌린 건지 알 수 없다*. 이 모호함을 풀어주려고 우리가 `'a`를 적는다.

## 라이프타임 elision — 99%는 안 적어도 된다

그렇다면 우리가 이걸 매번 적어야 할까? 다행히 그렇지 않다. Rust에는 *elision* 규칙이 있어서, 정해진 패턴에는 컴파일러가 알아서 라이프타임을 채워준다. 세 가지 규칙이다.

**규칙 1.** 입력 파라미터의 각 참조에 별개의 라이프타임이 부여된다.

```rust
fn print(s: &str) { ... }
// 컴파일러가 보는 모양: fn print<'a>(s: &'a str)
```

**규칙 2.** 입력 파라미터에 라이프타임이 *정확히 하나뿐*이면, 그 라이프타임이 모든 출력 참조에 부여된다.

```rust
fn first_word(s: &str) -> &str { ... }
// 컴파일러가 보는 모양: fn first_word<'a>(s: &'a str) -> &'a str
```

**규칙 3.** `&self` 또는 `&mut self`가 입력에 있으면, *self의 라이프타임*이 모든 출력 참조에 부여된다.

```rust
impl User {
    fn name(&self) -> &str { &self.name }
    // 컴파일러가 보는 모양: fn name<'a>(&'a self) -> &'a str
}
```

이 세 규칙으로 대부분의 함수가 elision으로 처리된다. 우리가 만든 함수의 99%는 둘 중 하나에 해당한다 — 입력 참조가 하나뿐이거나, 메서드라서 `&self`가 있거나. 그래서 라이프타임을 *명시적으로* 적어야 하는 함수는 책 한 권에서 *손에 꼽을 정도*다.

`longest` 함수가 elision으로 처리되지 않는 이유가 보이는가? 입력 참조가 두 개(`x`와 `y`)인데 `&self`도 없다. 규칙 2가 적용 안 되고, 규칙 3도 적용 안 된다. 그래서 컴파일러가 *어느 입력의 라이프타임을 반환에 묶을지* 모르고, 우리에게 명시를 요구한다. 이런 상황이 *진짜로 명시해야 하는 패턴*의 첫 번째다.

## 진짜로 명시해야 하는 두 번째 패턴 — 구조체에 참조 필드 두기

구조체가 *참조를 필드로 들고 있을 때*도 라이프타임을 명시해야 한다.

```rust
struct UserView<'a> {
    name: &'a str,
    email: &'a str,
}
```

이 구조체는 `String`을 소유하지 않고, 다른 어딘가에 있는 문자열 데이터를 *빌림으로 들고 있다*. 그 빌림이 가리키는 데이터가 사라지면 이 구조체는 dangling reference를 들고 있게 된다. 컴파일러는 그게 일어나지 않도록 검증해야 하니, 구조체 자체에 라이프타임을 박아준다.

JVM에서는 이런 구분이 없다. 모든 객체 필드는 그저 *참조*다. `class UserView { String name; String email; }`이라고 적으면 그만이다. GC가 알아서 처리한다. Rust는 그 비용을 *명시*로 받아낸다.

그런데 잠깐, 이런 구조체를 *진짜로 자주 만들어야 할까?* 답은 "아니오"에 가깝다. 입문자에게는 이런 패턴이 부담스럽다. 그래서 처음에는 그냥 `String`을 *소유*하는 형태로 두는 편이 낫다.

```rust
struct User {
    name: String,
    email: String,
}
```

`User`는 자기 데이터를 *직접 소유*한다. 라이프타임 어노테이션이 필요 없다. 약간의 메모리 복사가 일어나지만, 처음에는 *clone을 죄책감 없이 쓰자*는 4장의 처방을 그대로 따르는 편이 정신 건강에 좋다. 정말로 zero-copy가 필요한 순간이 오면 그때 `UserView<'a>` 같은 형태로 옮기면 된다. 입문자의 99%는 그 순간이 한참 뒤에 온다.

## `'static`의 두 얼굴

라이프타임 중 가장 자주 마주치고, 가장 자주 헷갈리는 게 `'static`이다. 이게 두 가지 의미로 쓰이기 때문이다.

**의미 1: 문자열 리터럴의 lifetime.**

```rust
let s: &'static str = "hello, world";
```

문자열 리터럴 `"hello, world"`는 컴파일된 바이너리의 read-only 데이터 영역에 박혀있다. 프로그램이 시작될 때 거기 있고, 프로그램이 끝날 때까지 거기 있다. 그래서 그 참조의 lifetime은 프로그램 전체 — `'static`이다. 이 의미는 직관적이다. *"프로그램이 살아있는 동안 영원히 살아있다"*.

**의미 2: 트레잇 객체의 bound로서의 `'static`.**

```rust
fn spawn<F: FnOnce() + Send + 'static>(f: F) { ... }
```

이 시그니처에서 `'static`은 "*참조를 들고 있다면, 그 참조는 'static lifetime이어야 한다*"는 의미다. 더 정확히 말하면 *"이 타입은 'static보다 짧은 어떤 빌림도 들고 있지 않다"*. 즉 *소유한 데이터*거나, *static 데이터를 빌린 참조*만 허용된다.

왜 이게 필요할까? `spawn`이 새로운 스레드를 만들어 거기서 `f`를 실행한다고 해보자. 그 스레드가 *얼마나 살지* 컴파일러는 모른다. 그러니 `f`가 들고 있는 데이터가 *언제 사라질지 모르는 짧은 빌림*이라면, 스레드가 그 빌림을 따라가는 순간 dangling이다. 그래서 `f`는 *스레드가 아무리 오래 살아도 안전한* 데이터만 들고 있어야 한다 — 그게 `'static`이다.

이 두 번째 의미가 처음에는 매우 헷갈린다. *"문자열도 아닌데 왜 'static이 붙지?"* 라는 질문을 한 번쯤 떠올리게 된다. 답은 *"문자열의 lifetime이 아니라 *트레잇이 들고 있을 수 있는 빌림의 lifetime*에 대한 제약"*이라는 것이다. 10장 tokio `spawn` 시그니처에서 다시 만나게 되니, 일단 *"`'static` bound = 이 값은 빌림 없이 살 수 있다"*는 한 줄로 머리에 두자.

## 라이프타임은 추론하지 *실행하지* 않는다

이쯤 와서 한 번 강조해두는 편이 낫겠다. **라이프타임은 컴파일 타임 개념이다. 런타임에는 아무 일도 일어나지 않는다.** 우리가 `'a`를 적는다고 해서 메모리에 뭔가가 추가되거나, 함수 호출에 오버헤드가 붙거나 하지 않는다. 컴파일러가 *코드의 정합성*을 검증할 때만 쓴다.

이게 zero-cost abstraction의 한 면이다. Java의 GC가 *런타임에* 객체 reachability를 추적하느라 CPU와 메모리를 쓴다면, Rust는 *컴파일 타임에* 라이프타임을 추적하느라 *컴파일 시간*을 쓴다. 런타임에는 아무 비용도 없다. 이 사실 하나가 Rust가 한 자릿수 MB 컨테이너로 마이크로서비스를 띄울 수 있는 이유 중 하나다.

## 흔한 컴파일 거부 패턴 — `'x' does not live long enough`

5장 끝에서 짚었던 그 에러 메시지가 사실 라이프타임 에러다. 손으로 한 번 두드려보자.

```rust
fn dangling() -> &i32 {     // 컴파일 에러
    let x = 5;
    &x
}
```

`x`는 함수 안에서 만들어진 지역 변수다. 함수가 끝나면 `x`는 drop된다. 그런데 우리는 `&x`를 반환하려 한다. 함수가 끝난 뒤 그 참조를 따라가면 *이미 사라진 데이터*를 가리키게 된다. 컴파일러는 이걸 거부한다.

```
error[E0106]: missing lifetime specifier
...
= help: this function's return type contains a borrowed value, but
        there is no value for it to be borrowed from
```

elision 규칙으로도 채울 수 없는 형태(입력에 참조가 없는데 출력은 참조)니, 컴파일러가 명시를 요구한다. 우리가 어떤 라이프타임을 박아주든 — `'a`든 `'static`이든 — 결국 거부된다. *지역 변수가 함수보다 오래 살 수는 없으니까*.

해결은? `&i32`가 아니라 `i32`를 반환하면 된다. ownership을 *통째로* 옮겨버리는 거다.

```rust
fn not_dangling() -> i32 {
    let x = 5;
    x
}
```

이게 4~6장이 가르치는 대원칙이다. *옮길 것인가, 빌릴 것인가, 빌림이라면 얼마나 오래 살 것인가*. 이 세 질문에 답하는 게 Rust 코드 짜기의 일상이다. JVM 출신은 이 세 질문을 한 번도 의식해본 적이 없다. 그래서 처음 한 달이 답답한 거다. 하지만 패턴이 손에 묻으면, 이 세 질문이 *코드의 의도를 자기 자신에게 명료하게 설명하는 도구*가 된다는 사실을 깨닫게 된다.

## 라이프타임이 진짜로 어려워지는 두 가지 패턴

지금까지 본 패턴들은 입문 단계에서도 필요할 때 한 번씩 마주친다. 그런데 라이프타임이 *진짜로 어려워지는* 영역은 따로 있다. 두 가지만 짚어두자.

**패턴 1: 두 개 이상의 입력 lifetime을 출력에 묶는 경우.**

`longest`는 두 입력 모두를 *같은 lifetime `'a`*로 묶었다. 두 입력의 lifetime이 *서로 다를* 때 어떻게 할까?

```rust
fn first_or_second<'a, 'b>(x: &'a str, y: &'b str, use_first: bool) -> &?? str {
    if use_first { x } else { y }
}
```

`&'a`도 `&'b`도 정답이 아니다. 둘 중 어느 것도 다른 쪽을 포함하지 않는다. 이런 경우 보통 `'b: 'a` 같은 *lifetime bound*("`'b`는 `'a`만큼은 산다")로 둘의 관계를 명시해주거나, 한쪽으로 통일하거나, 아예 ownership을 옮긴 `String` 반환으로 바꿔서 라이프타임 자체를 없애는 편이 낫다. 입문 단계에서는 *후자*가 99% 정답이다.

**패턴 2: 클로저나 트레잇 객체에 빌림을 가두는 경우.**

```rust
fn make_counter<'a>(name: &'a str) -> Box<dyn Fn() + 'a> {
    Box::new(move || println!("{name}"))
}
```

이 함수가 반환하는 `Box<dyn Fn()>`은 *내부에 `name`을 빌림으로 들고 있다*. 그러니 그 클로저는 `name`보다 오래 살 수 없다. `+ 'a`가 그 사실을 표현한다. 만약 `'static`을 적었다면 *어떤 짧은 빌림도 들고 있지 않다*는 약속이 깨지므로 컴파일이 거부된다. 이런 패턴은 axum 핸들러나 tokio `spawn`에서 종종 마주친다. 그때 *이 챕터를 다시 펼쳐 읽으면 된다*는 마음으로 일단 머리에 한 번 박아두자.

## 한 단계 더 — borrow checker는 *우리 편*이다

처음 한 달은 *컴파일러가 내 적처럼 느껴진다*. 두 달째는 *컴파일러가 까칠한 사수처럼 느껴진다*. 6개월째는 *컴파일러가 동료처럼 느껴진다*. 이 변화는 거의 모든 Rust 후기에서 반복적으로 등장한다. corrode가 정리한 한 줄을 그대로 가져와보자. *"With Rust, you can write concurrent applications more easily than Java — this is 9 months of experience overtaking 10 years of experience."* 9개월이라는 숫자가 4~6개월보다 길지만, 한 가지는 분명하다 — *어느 시점부터는 Java보다 빠르게 동시성 코드를 짜게 된다*. 라이프타임도 그 곡선의 한 부분이다.

라이프타임이 어렵게 느껴진다면 한 가지를 기억해두자. *컴파일러가 거부하는 라이프타임 코드는, 사실 우리가 사고하지 못한 메모리 안전성의 갭을 컴파일러가 미리 짚어주는 것*이다. JVM에서라면 운영에서 NPE나 race condition으로 터졌을 그 사고의 한 형태가, Rust에서는 빌드 단계에서 잡힌다. 그게 라이프타임이 우리에게 청구하는 비용의 *반대급부*다.

## 함께 해보자

함수 두 개를 직접 손으로 두드려보자.

1. 두 `&str`을 받아 더 긴 쪽을 반환하는 함수를 *elision 없이* 적어보자. 컴파일러가 어떤 시점에 `'a`를 요구하는지, 그리고 우리가 그 `'a`를 박아주면 어떻게 통과하는지 확인해보자. 그다음, 입력 참조를 *하나만* 받는 함수(예: 첫 단어를 반환)로 바꿔서 elision이 어떻게 그 자리를 메우는지 비교해보자.
2. `Box<dyn Fn() + 'static>`이 왜 `'static`을 요구하는지 한 단락으로 적어보자. 만약 `'a` lifetime이 박힌 빌림을 그 클로저가 들고 있다면 어떤 일이 벌어질까? *"이 클로저가 빌린 데이터가 클로저보다 먼저 사라지면 안 된다"*는 사고를 한 번 해보면 된다.

이 `'static` bound는 10장 tokio `spawn` 시그니처에서 다시 호출된다. 거기서 우리는 *"새로 만든 스레드/태스크가 부모 스코프와 독립적으로 살아갈 수 있어야 한다"*는 동기성 안전 조건을 만나게 된다.

라이프타임은 외워야 하는 문법이 아니다. *컴파일러가 우리에게 묻는 질문*에 답해주는 도구다. 입문 한 달은 그 질문 자체가 낯설게 느껴지지만, 익숙해지고 나면 *그 질문이 사실 우리가 짠 코드의 메모리 의도를 명료하게 만들어주는 동료의 질문*이라는 사실을 손으로 만지게 된다. Part 2의 4·5·6장이 함께 가르치고자 한 것이 바로 그 사고 전환이다.

다음 7장에서는 표현력 도구상자를 펼친다. 트레잇·제네릭·패턴 매칭·에러 처리. JVM의 인터페이스, 제네릭, sealed class, checked exception이 하던 일을 Rust는 어떤 도구로 옮겼는지를 한 챕터로 묶어 살펴보자.

---

## 참고

- [Rust Lifetimes: A Complete Guide — Earthly](https://earthly.dev/blog/rust-lifetimes-ownership-burrowing/)
- [4년간의 Rust 사용 후기 — blog.cro.sh](https://blog.cro.sh/posts/four-years-of-rust/)
- [The Rust Programming Language Book — Validating References with Lifetimes](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html)
- [Rust for Java Developers — tkaitchuck](https://tkaitchuck.github.io/Rust4JavaDevelopers/ownership.html)
- [Migrating from Java to Rust — corrode](https://corrode.dev/learn/migration-guides/java-to-rust/)
- Jung, R., Jourdan, J.-H., Krebbers, R., Dreyer, D. — [RustBelt: Securing the Foundations of the Rust Programming Language (POPL 2018)](https://plv.mpi-sws.org/rustbelt/popl18/paper.pdf)

---

# 7장. 트레잇·제네릭·패턴 매칭·에러 처리 — 표현력 도구상자

소유권·빌림·라이프타임의 세 챕터를 지나오면서, 우리는 *컴파일러와 친구가 되는 길*을 절반 정도 걸어왔다. 이제 손에 든 것이 안전성이라는 토대다. 그 토대 위에서 *우리가 표현하고 싶은 것을 어떻게 표현할 것인가* — 그게 7장의 주제다. JVM에서는 인터페이스·제네릭·sealed class·checked exception이 그 일을 했다. Rust는 그 자리에 다른 도구들을 놓았다. 트레잇, 제네릭, enum + match, 그리고 `Result<T, E>`. 이름은 비슷한데 의미가 결정적으로 다르다. *그 차이를 받아들이는 순간, Rust의 표현력이 보인다*.

7장이 책의 무게중심에서 가장 *후련한* 챕터다. 4~6장이 답답함과 패턴 인식의 곡선이었다면, 7장은 그 패턴을 손에 쥔 우리가 *표현력의 보상*을 받는 자리다. 한 단락씩 천천히 가져가자.

## 트레잇은 인터페이스가 아니다

가장 먼저 짚어야 할 한 줄이다. **트레잇은 인터페이스가 아니다.** 비슷해 보이고 비슷하게 쓰이지만, 의미가 결정적으로 다르다. 이 차이를 받아들이는 데 일주일쯤 걸린다. 그러고 나면 *"왜 진작 이렇게 안 만들었지"*라는 후련함이 따라온다.

차이의 핵심은 한 줄이다. *인터페이스는 타입이 자기를 구현하겠다고 선언한다. 트레잇은 외부에서 어떤 타입에 트레잇 구현을 추가할 수 있다.*

Java로 보자.

```java
public interface JsonSerializable {
    String toJson();
}

public class User implements JsonSerializable {
    private String name;
    @Override
    public String toJson() {
        return "{\"name\":\"" + name + "\"}";
    }
}
```

`User`가 `implements JsonSerializable`을 *직접 선언*해야 한다. `User`의 소스를 우리가 가지고 있어야 한다. 만약 `User`가 외부 라이브러리에서 온 클래스라면? 우리는 어쩔 수 없이 `UserJsonAdapter`를 만들거나, decorator 패턴을 동원하거나, AOP를 끌어와야 한다.

Rust로는 같은 일을 이렇게 할 수 있다.

```rust
trait JsonSerializable {
    fn to_json(&self) -> String;
}

// 외부 crate에서 온 타입에 트레잇 구현을 추가
impl JsonSerializable for std::time::Duration {
    fn to_json(&self) -> String {
        format!("{{\"secs\":{}}}", self.as_secs())
    }
}
```

`Duration`은 표준 라이브러리의 타입이다. 우리가 정의한 게 아니다. 그런데 우리는 *우리의 트레잇*을 *그 외부 타입에 구현*했다. 이게 바로 인터페이스가 못 하는 일이다.

이 자유에는 한 가지 안전 장치가 붙는다. **orphan rule** — 트레잇 구현은 *트레잇 자체와 타입 중 적어도 하나는 우리 crate에서 정의되어야 한다*. 즉 *남이 만든 트레잇*을 *남이 만든 타입*에 구현하는 것은 금지된다. 그렇지 않으면 두 라이브러리가 같은 트레잇·같은 타입에 대해 *서로 다른 구현*을 해버려서 충돌이 일어난다. 이 규칙이 없는 Scala 같은 언어에서 가끔 발생하는 implicit 충돌을, Rust는 컴파일러가 미리 차단한다.

JVM에서 우리가 익숙했던 또 다른 패턴 — Spring의 `@Component`/`@Service`로 만들어지는 의존성 그래프 — 와도 발상이 다르다. Spring DI는 *런타임에 컨테이너가 인스턴스를 주입*한다. 트레잇은 *컴파일 타임에 타입 시스템 안에서 동작*을 합성한다. 그래서 트레잇 기반 코드는 *런타임 리플렉션 없이* 같은 일을 해낸다. Spring 없이도 의존성 주입의 명료함을 *타입으로* 표현할 수 있는 이유가 여기 있다.

## 정적 디스패치와 동적 디스패치 — 우리가 명시적으로 고른다

트레잇을 사용하는 두 가지 방식이 있다. *정적 디스패치(static dispatch)*와 *동적 디스패치(dynamic dispatch)*. JVM에서는 이 둘이 거의 자동으로 결정되지만, Rust는 *우리가 명시적으로 고른다*.

```rust
trait Greeter {
    fn greet(&self) -> String;
}

struct EnglishGreeter;
impl Greeter for EnglishGreeter {
    fn greet(&self) -> String { "Hello".to_string() }
}

struct KoreanGreeter;
impl Greeter for KoreanGreeter {
    fn greet(&self) -> String { "안녕".to_string() }
}

// 정적 디스패치 — generic
fn greet_static<G: Greeter>(g: &G) {
    println!("{}", g.greet());
}

// 동적 디스패치 — trait object
fn greet_dynamic(g: &dyn Greeter) {
    println!("{}", g.greet());
}
```

차이가 보이는가? `<G: Greeter>`는 *타입 파라미터*다. 컴파일 시점에 `G`가 무엇인지 결정되고, `EnglishGreeter`로 호출하면 `EnglishGreeter` 전용 코드가, `KoreanGreeter`로 호출하면 `KoreanGreeter` 전용 코드가 *각각 생성된다*. 함수 호출은 *직접 호출*이고 인라인도 가능하다. *0-cost*다.

`&dyn Greeter`는 *trait object*다. 런타임에 *vtable*을 거쳐 함수 포인터로 호출된다. Java 인터페이스 메서드 호출과 같은 모양이다. 한 단계의 indirection이 생기지만, *유연성*이 늘어난다 — `Vec<Box<dyn Greeter>>`처럼 *서로 다른 구체 타입을 한 컨테이너에 담을 수 있다*.

언제 어느 것을 쓰는가? 단순한 룰이 있다. **모르겠으면 generic부터 시작하자.** 0-cost고, 컴파일러가 타입 안전성을 더 강하게 검증한다. *런타임에 다양한 구체 타입을 한 컨테이너에 담아야 할 때*만 `dyn Trait`로 옮긴다. 그러면 우리가 트레잇을 도입한 *의도가 코드에 박힌다*.

JVM과 비교하면 이게 매우 명료해진다. Java에서는 `List<Greeter> greeters`라고 쓰면 *항상 vtable을 거치는 동적 디스패치*다. 왜냐하면 `List<EnglishGreeter>`와 `List<KoreanGreeter>`는 *같은 `List<Greeter>`가 아니므로*, 두 종류를 한 리스트에 담으려면 인터페이스 타입으로 통일해야 하기 때문이다. Rust는 generic이면 *한 종류만 담을 수 있는 대신* 0-cost, `dyn Trait`이면 *여러 종류를 담을 수 있는 대신* vtable. *그 선택이 우리 손에 있다*.

## 제네릭 — type erasure가 아니다

JVM 출신이 처음 만나는 또 한 번의 결정적 차이다. **Rust 제네릭은 monomorphization이지 type erasure가 아니다.**

Java에서 `List<String>`과 `List<Integer>`는 컴파일 후 *모두 그냥 `List`*로 지워진다(erasure). 런타임에 둘을 구분할 수 없다. 그래서 `instanceof List<String>` 같은 검사가 불가능하다. 또 generic 메서드가 호출될 때 타입 정보가 실제로는 사라져 있어서, reflection으로 우회하지 않으면 `T.class` 같은 걸 쓸 수 없다.

Rust는 다르다. `Vec<String>`과 `Vec<i32>`는 컴파일 시점에 *각각 별개의 코드*가 생성된다. `fn first<T>(v: &[T]) -> &T`라는 함수를 짜면, 우리가 `first(&vec_of_strings)`로 부른 자리에는 `first_String`이라는 전용 코드가, `first(&vec_of_i32s)`로 부른 자리에는 `first_i32` 전용 코드가 *각각 펼쳐진다*. 이게 monomorphization이다.

장점: *0-cost*. 타입별 전용 코드라서 인라인이 가능하고, vtable이 없고, boxing/unboxing이 없다. JVM에서 `List<Integer>`에 `Integer` 박싱이 일어나는 비용이 Rust에서는 *원천적으로 없다*. `Vec<i32>`는 *진짜 i32들의 배열*이다.

단점: *컴파일 시간이 늘고 바이너리가 커진다*. `Vec<String>`, `Vec<i32>`, `Vec<User>`, `Vec<Order>`를 각각 쓰면 네 종류의 `Vec` 코드가 생성된다. 이게 후에 13장에서 다룰 *컴파일 시간 함정*의 한 원인이 된다. 함정이지만, 트레이드오프가 명료하다 — *런타임 0-cost를 위해 컴파일 시간을 지불하는 모델*.

generic과 trait bound를 함께 써보자.

```rust
fn print_all<T: std::fmt::Display>(items: &[T]) {
    for item in items {
        println!("{item}");
    }
}
```

`T: Display`는 *"`T`는 `Display` 트레잇을 구현한다"*는 제약이다. Java로 옮기면 `<T extends Display>` 비슷한 모양이다. 다만 `Display`는 인터페이스가 아니라 트레잇이고, 우리가 외부 타입에도 구현을 추가할 수 있다는 차이가 있다.

여러 trait bound를 묶을 때는 `+`로 잇거나 `where` 절을 쓴다.

```rust
fn process<T: Clone + std::fmt::Debug + Send>(item: T) { ... }

// where 절로 분리하면 시그니처가 깔끔해진다
fn process<T>(item: T)
where
    T: Clone + std::fmt::Debug + Send,
{
    // ...
}
```

bound가 많아지면 `where` 절로 분리하는 편이 가독성이 좋다. JVM 출신은 처음에 `<T: A + B + C>` 같은 모양을 보면 답답해 보이지만, 사실 이건 *타입에 대한 명세를 한 자리에 명료하게 적은 것*이다. 메서드 시그니처를 보는 것만으로 *이 함수가 타입에 무엇을 요구하는지*가 한눈에 보인다.

## 학술적 토대 — 트레잇·제네릭의 안전성도 입증됐다

5장에서 RustBelt가 borrow의 안전성을 형식 증명했다고 짚었다. 같은 학계의 흐름은 트레잇과 제네릭에 대해서도 검증을 이어왔다. 2024년 PLDI에 발표된 「RefinedRust: A Type System for High-Assurance Verification of Rust Programs」(Gäher 외)는 trait bound와 lifetime이 결합한 코드의 안전성을 *refinement type*으로 정형화했다. 깊이 들어갈 필요는 없다. 다만 *우리가 지금 배우는 트레잇·제네릭이 그저 컴파일러 구현자의 직관이 아니라, 학계가 별도로 검증해온 모델 위에 있다*는 한 줄을 한 번 더 박아두자. 5장 끝에서 짚었던 그 한 단락의 후속편이다.

## enum + match — algebraic data type의 진짜 모습

Java 17이 sealed class와 switch pattern matching을 도입하면서 *Rust에 한 발짝 다가왔다*. 그 사실 자체가 Rust enum + match의 표현력이 얼마나 강력한지를 보여준다. 한 발짝이지, 같은 자리에 도달한 게 아니다. Java 측 발언자도 이 차이를 인정한다. *"Java's deconstruction is a baby step and not as powerful as deconstruction in Rust."*

Rust enum의 진짜 모습부터 보자.

```rust
enum HttpResponse {
    Ok(String),
    NotFound,
    Redirect { url: String, permanent: bool },
    InternalError(u16, String),
}
```

이게 enum이다. 각 variant가 *데이터를 가질 수 있다*. `Ok`는 `String` 하나, `NotFound`는 데이터 없음, `Redirect`는 두 개의 named field, `InternalError`는 두 개의 unnamed field. 이걸 algebraic data type(ADT)이라 부른다. *합(sum) 타입과 곱(product) 타입을 자유롭게 결합*할 수 있는 타입이다.

Java 17 sealed class로 비슷하게 흉내내면 이렇다.

```java
public sealed interface HttpResponse permits Ok, NotFound, Redirect, InternalError {}
public record Ok(String body) implements HttpResponse {}
public record NotFound() implements HttpResponse {}
public record Redirect(String url, boolean permanent) implements HttpResponse {}
public record InternalError(int code, String message) implements HttpResponse {}
```

기능상 비슷하다. 다섯 줄짜리 enum이 다섯 개의 record와 하나의 sealed interface로 흩어진다. 그리고 record 패턴 매칭은 *최근에야* 가능해졌다.

이걸 처리하는 match를 보자.

```rust
fn describe(response: &HttpResponse) -> String {
    match response {
        HttpResponse::Ok(body) => format!("성공: {} bytes", body.len()),
        HttpResponse::NotFound => "찾을 수 없음".to_string(),
        HttpResponse::Redirect { url, permanent } => {
            let kind = if *permanent { "영구" } else { "임시" };
            format!("{kind} 리다이렉트 → {url}")
        }
        HttpResponse::InternalError(code, msg) => {
            format!("서버 에러 [{code}]: {msg}")
        }
    }
}
```

여기서 결정적으로 중요한 한 가지를 짚어두자. *exhaustive*가 컴파일러 강제다. 만약 우리가 `InternalError` 가지를 깜빡 빼먹으면 컴파일러가 거부한다.

```
error[E0004]: non-exhaustive patterns: `&HttpResponse::InternalError(_, _)` not covered
```

*어떤 variant를 빠뜨렸는지 컴파일러가 손가락으로 짚어준다*. Java switch expression이 default를 강요하는 것과 결정적으로 다르다. default 한 줄로 *모든 미처리 케이스를 조용히 묻어버리는* 그 함정이 Rust에는 없다. 새 variant가 enum에 추가되면 *모든 match 자리가 컴파일 거부*되어 우리에게 처리를 강제한다. 1장에 적었던 운영 사고 노트가 *"새 case를 추가했는데 기존 코드 어딘가에서 default로 잘못 처리됐다"*였다면, Rust enum + match가 그 사고를 컴파일 타임에 끝낸다.

## 패턴 매칭의 깊이

`match`는 단순한 분기가 아니다. *값의 구조*를 분해하면서 분기한다. 몇 가지 자주 쓰는 패턴을 한 묶음으로 보자.

**`if let`** — 한 가지 variant에만 관심 있을 때 match를 짧게 쓴 형태.

```rust
let response = HttpResponse::Ok("data".to_string());

if let HttpResponse::Ok(body) = response {
    println!("받은 본문: {body}");
}
```

`HttpResponse`의 다른 variant는 무시한다. `if response is Ok ok && ok.body() != null`을 자바로 쓰는 것과 비교하면 훨씬 명료하다.

**`while let`** — 패턴이 매치되는 동안 반복.

```rust
let mut stack = vec![1, 2, 3];
while let Some(top) = stack.pop() {
    println!("{top}");
}
```

`Vec::pop`은 `Option<T>`를 반환한다. `Some`이 나오는 동안 반복하다가 `None`이 나오면 종료. 자바의 `while ((x = it.next()) != null)` 패턴이 *훨씬 안전하게* 한 줄에 들어온다.

**guard 절** — 패턴에 추가 조건을 붙인다.

```rust
match temperature {
    t if t < 0 => "영하",
    t if t < 20 => "선선함",
    t if t < 30 => "따뜻함",
    _ => "더움",
}
```

**구조 분해(destructuring)** — 튜플, 구조체, enum의 내부 필드를 한 번에 끄집어낸다.

```rust
struct Point { x: i32, y: i32 }
let p = Point { x: 3, y: 7 };

let Point { x, y } = p;   // x=3, y=7로 분해
println!("{x}, {y}");
```

**`@` 바인딩** — 패턴에 매치되는 *값 전체*를 동시에 잡는다.

```rust
match age {
    n @ 0..=12 => println!("어린이 {n}세"),
    n @ 13..=19 => println!("청소년 {n}세"),
    n => println!("성인 {n}세"),
}
```

이 모든 패턴이 *한 도구 안에서* 합성된다. Java가 record pattern, switch expression, instanceof pattern으로 *나눠서 가지고 있는* 능력을 Rust는 *match 한 곳*에서 표현한다. 처음에는 외울 게 많아 보이지만, 한 달쯤 지나면 *"이걸 if-else로 짜면 얼마나 답답할까"* 싶어진다.

## 에러 처리 — 예외가 아니라 *값*이다

이제 7장의 가장 큰 한 절이다. **Rust에는 예외가 없다.** throw도 없고 catch도 없다. 그러면 실패는 어떻게 표현하는가? *값으로*. `Option<T>`와 `Result<T, E>`라는 두 enum이 그 일을 한다.

`Option<T>`부터 보자.

```rust
enum Option<T> {
    Some(T),
    None,
}
```

값이 *있을 수도 없을 수도* 있을 때 쓴다. Java의 `Optional<T>`와 비슷하지만 결정적인 차이가 하나 있다 — *Rust에는 null이 없다*. Java에서 `Optional<User>`를 반환하기로 약속해도 누군가가 그냥 `null`을 반환할 수 있다. 또는 `Optional`을 쓰지 않고 `User`를 반환하면서 *내부적으로 null이 가능*할 수도 있다. Rust는 그 가능성 자체가 없다. *없을 수 있는 값*을 표현할 길이 `Option`뿐이다.

```rust
fn find_user(id: u64) -> Option<User> {
    // 찾으면 Some(user), 없으면 None
}

if let Some(user) = find_user(42) {
    println!("{}", user.name);
}
```

NPE의 가능성이 *컴파일 타임에 차단된다*. 1장에 적었던 운영 사고 노트가 NPE였다면, 같은 코드를 Rust로 옮기는 순간 *그 사고가 일어날 자리 자체가 사라진다*.

`Result<T, E>`는 한 발 더 나간다.

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

성공이면 `Ok`에 값을 담고, 실패면 `Err`에 에러 정보를 담는다. Java의 checked exception이 *시그니처에 박혀 있던 그 정신*이 살아있되, *예외가 아니라 값*이라서 함수 합성과 자유롭게 어울린다.

```rust
fn parse_age(s: &str) -> Result<u32, std::num::ParseIntError> {
    s.parse::<u32>()
}

match parse_age("42") {
    Ok(age) => println!("나이: {age}"),
    Err(e) => println!("파싱 실패: {e}"),
}
```

여기까지는 Java의 try-catch와 비슷해 보인다. 그런데 `Result`의 진짜 매력은 *합성*에서 나온다.

```rust
let ages: Result<Vec<u32>, _> = vec!["20", "30", "abc"]
    .iter()
    .map(|s| s.parse::<u32>())
    .collect();
// ages는 Err(parse error)다 — 한 번이라도 실패하면 전체가 Err
```

`Result`가 *그저 enum*이라서 `.map()`, `.and_then()`, `.collect::<Result<Vec<_>, _>>()` 같은 일반적인 함수형 도구와 자유롭게 결합된다. Java checked exception은 *예외가 메서드 시그니처를 오염*시키지만 *값이 아니라 제어 흐름*이라 이런 합성이 거의 불가능하다. lambda 안에서 checked exception을 던지려면 wrapping과 unwrapping의 지옥이 펼쳐진다. 그래서 자바 8 이후 *대다수의 코드가 RuntimeException으로 도망갔다*.

## `?` 연산자 — 에러 propagate의 한 글자

`Result`를 쓰면 매번 `match`로 풀어야 할까? 그렇지 않다. `?` 연산자가 그 일을 한 글자로 줄여준다.

```rust
fn read_user_age(path: &str) -> Result<u32, Box<dyn std::error::Error>> {
    let content = std::fs::read_to_string(path)?;
    let age: u32 = content.trim().parse()?;
    Ok(age)
}
```

`?` 한 글자가 무엇을 하는가? *현재 함수가 `Result`를 반환할 때, 이 표현식이 `Err`이면 즉시 early return*한다. 즉 위 코드는 사실 다음과 동치다.

```rust
fn read_user_age(path: &str) -> Result<u32, Box<dyn std::error::Error>> {
    let content = match std::fs::read_to_string(path) {
        Ok(s) => s,
        Err(e) => return Err(e.into()),
    };
    let age: u32 = match content.trim().parse() {
        Ok(n) => n,
        Err(e) => return Err(e.into()),
    };
    Ok(age)
}
```

`?` 한 글자가 다섯 줄을 한 줄로 줄였다. 그리고 *시그니처에 에러가 박혀 있으니* 호출자는 이 함수가 실패할 수 있다는 사실을 *반드시* 인식하고 처리하게 된다. Java의 `throws` chain이 추구한 그 정신이, *시그니처를 오염시키지 않으면서* 더 깔끔하게 살아있다.

## `From` 트레잇과 `?`의 자동 변환

`?`의 진짜 매력은 *타입 변환을 자동으로 처리*한다는 데 있다. 위 함수에서 `read_to_string`은 `std::io::Error`를 반환하고 `parse`는 `ParseIntError`를 반환한다. 둘 다 다른 타입의 에러인데, 함수 시그니처는 `Box<dyn std::error::Error>` 하나다. 어떻게 한 자리에서 두 종류의 에러가 통합될까?

답은 `From` 트레잇이다. `?`는 실패 시 `Err(e.into())`로 변환을 거친다. `into()`는 `From` 트레잇이 정의된 타입 사이를 변환하는 메서드다. `Box<dyn Error>`는 `std::io::Error`와 `ParseIntError`에 대한 `From`이 자동으로 정의되어 있어서, `?`가 알아서 변환한다.

이걸 직접 만들어보자. 예를 들어 우리 도메인의 에러 타입을 정의하고, 다른 라이브러리 에러를 흡수하고 싶다면.

```rust
#[derive(Debug)]
enum AppError {
    Io(std::io::Error),
    Parse(std::num::ParseIntError),
}

impl From<std::io::Error> for AppError {
    fn from(e: std::io::Error) -> Self { AppError::Io(e) }
}

impl From<std::num::ParseIntError> for AppError {
    fn from(e: std::num::ParseIntError) -> Self { AppError::Parse(e) }
}

fn read_user_age(path: &str) -> Result<u32, AppError> {
    let content = std::fs::read_to_string(path)?;   // io::Error → AppError 자동 변환
    let age: u32 = content.trim().parse()?;          // ParseIntError → AppError 자동 변환
    Ok(age)
}
```

`?` 한 글자가 *trait dispatch까지 자동으로 처리*한다. Java에서 같은 일을 하려면 try-catch로 받아서 다시 throw하는 변환 코드를 *모든 호출 자리마다* 적어야 한다. 그래서 자바는 결국 unchecked exception으로 도망갔다. Rust는 *trait + `?` 한 글자*로 그 패턴을 깔끔하게 풀었다.

## `panic!` — 진짜 끝났을 때

마지막 한 도구는 `panic!`이다. *복구 불가능한* 에러를 표현한다. JVM의 `Error`(OOM 같은 류)에 가깝다. 라이브러리 코드에서는 거의 쓰지 않는다 — 호출자에게 *실패 가능성*을 알리는 게 더 정직하기 때문이다. 하지만 *프로그램의 invariant가 깨졌다*는 사실을 알리고 싶을 때(예: index out of bounds, 절대 일어나서는 안 되는 case에 도달), 그때 `panic!`을 던진다.

`Option::unwrap()`, `Result::unwrap()`은 내부적으로 panic을 일으킨다. 빠른 prototyping에서는 자주 쓰이지만, 프로덕션 코드에서는 *불러일으킬 수 있는 panic이 이 한 줄에 박혀 있다*는 사실을 한 번 더 의식하는 편이 낫다. clippy는 `unwrap()` 남용을 경고로 잡아준다.

## anyhow와 thiserror — 분업의 도구

위에서 우리는 `From` 트레잇 구현을 직접 적었다. 매번 이렇게 적을까? 그렇지 않다. **두 개의 crate가 그 노동을 대신해준다.** *anyhow*와 *thiserror*. 둘은 *경쟁이 아니라 분업*이다.

**anyhow** — *애플리케이션* 코드에서. 핸들러, 서비스 코드, main 함수 등.

```rust
use anyhow::{Context, Result};

fn read_user_age(path: &str) -> Result<u32> {
    let content = std::fs::read_to_string(path)
        .context(format!("파일 {path}을 읽지 못했다"))?;
    let age: u32 = content.trim().parse()
        .context("나이를 파싱하지 못했다")?;
    Ok(age)
}
```

`anyhow::Result<T>`는 `Result<T, anyhow::Error>`의 줄임말이다. `anyhow::Error`는 *어떤 에러든 box로 감싸서 들고 다닌다*. `.context()`로 *어디서 실패했는지 사람이 읽을 수 있는 컨텍스트*를 덧붙인다. 호출 chain을 따라가며 context가 쌓이고, 최종적으로 `eprintln!("{:?}", e)`로 출력하면 *어디서부터 어디까지 실패가 전파됐는지가 한눈에 보인다*.

**thiserror** — *라이브러리* 코드에서. 도메인 모델의 에러 타입을 *enum으로 정의*할 때.

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AuthError {
    #[error("잘못된 비밀번호")]
    InvalidPassword,

    #[error("토큰이 만료됐다")]
    ExpiredToken,

    #[error("요청 한도 초과 — {0:?} 후 재시도")]
    RateLimited(std::time::Duration),

    #[error("DB 에러: {0}")]
    DatabaseError(#[from] sqlx::Error),
}
```

`#[derive(Error)]`가 `std::error::Error` 트레잇 구현을 자동 생성한다. `#[error("...")]`가 `Display` 구현을 만들고, `#[from] sqlx::Error`는 `From<sqlx::Error> for AuthError` 구현을 자동으로 깔아준다. 이제 우리 함수에서 `?` 한 글자로 sqlx 에러를 `AuthError::DatabaseError`로 변환할 수 있다.

```rust
async fn authenticate(
    pool: &sqlx::PgPool,
    username: &str,
    password: &str,
) -> Result<User, AuthError> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE name = $1", username)
        .fetch_one(pool)
        .await?;   // sqlx::Error → AuthError::DatabaseError 자동 변환

    if !verify_password(password, &user.password_hash) {
        return Err(AuthError::InvalidPassword);
    }
    Ok(user)
}
```

호출자는 `AuthError`를 보고 *어떤 종류의 인증 실패인지* 즉시 알 수 있다. `match`로 분기하면 *모든 variant를 처리하지 않으면* 컴파일이 거부된다 — 새 인증 실패 종류를 추가하면 모든 호출자가 *그것을 처리하도록 강제*된다. checked exception이 가지고 있던 그 정신이 *컴파일러 강제*로 살아있되, 시그니처가 깨끗하다.

## 분업의 기준선 — 한 줄로

언제 anyhow를, 언제 thiserror를 써야 할까? 한 줄짜리 가이드라인은 이렇다.

- **라이브러리 = thiserror** — 호출자가 *어떤 종류의 실패인지* 분간할 수 있어야 하는 자리.
- **애플리케이션 = anyhow** — 호출자가 *그저 컨텍스트와 함께 위로 던지면 되는* 자리.

Spring 프로젝트로 비유하면 *Repository/Service 계층은 thiserror*(도메인 의미를 보존), *Controller/Main은 anyhow*(컨텍스트 더해서 위로 보낸다). 이 분업이 처음에는 헷갈리지만, 한 프로젝트만 짜보면 *어느 자리에 어느 도구가 어울리는지*가 손에 묻는다.

## 1장의 운영 사고 노트, 다시 호명하자

1장 함께해보자에서 우리는 *자기 회사의 가장 최근 운영 사고 1건*을 떠올려봤다. 그 사고가 NPE였다면, 같은 코드를 Rust로 짰을 때 컴파일 타임에 잡혔을 자리는 어디인가? 아마 `Option<T>`로 표현되었어야 할 값이 그저 `User`로 반환되고 있던 함수의 시그니처 자리다. 또는 `Result<T, AuthError>`로 표현되었어야 할 인증 실패가 `User` 또는 null로 흩어져 있던 자리다.

7장의 도구들이 모이면, 우리가 일상에서 짜는 코드의 *실패 가능성이 시그니처에 명료하게 박힌다*. 그 박힘이 한 달 뒤에는 *답답함*으로 느껴지지만, 6개월 뒤에는 *대견함*으로 바뀐다. *이 함수가 어떤 입력을 받고, 어떤 출력을 주고, 어떤 실패를 가질 수 있는지*가 시그니처 한 줄에 모두 담겨 있다 — 그게 Rust 코드를 *몇 달 뒤에 다시 봐도* 즉시 이해할 수 있게 만드는 비결이다.

## 함께 해보자

7장의 도구를 한 자리에서 손으로 두드려보자. 사용자 인증 도메인을 작은 enum으로 표현하는 연습이다.

```rust
use thiserror::Error;
use std::time::Duration;

#[derive(Error, Debug)]
pub enum AuthError {
    #[error("잘못된 비밀번호")]
    InvalidPassword,

    #[error("토큰이 만료됐다")]
    ExpiredToken,

    #[error("요청 한도 초과 — {0:?} 후 재시도")]
    RateLimited(Duration),

    #[error("DB 에러: {0}")]
    DatabaseError(#[from] sqlx::Error),
}

pub struct User {
    pub id: i64,
    pub name: String,
}

pub async fn authenticate(
    pool: &sqlx::PgPool,
    username: &str,
    password: &str,
) -> Result<User, AuthError> {
    // ① 사용자 찾기 — 없으면? Option을 Result로 변환하기
    // ② 비밀번호 검증 — 틀리면 InvalidPassword
    // ③ rate limit 검사 — 초과면 RateLimited(retry_after)
    // ④ 토큰 만료 검사 — 만료면 ExpiredToken
    todo!()
}
```

이 함수의 본문을 직접 채워보자. `?` 연산자가 어디에 들어가고, 어디서 `return Err(...)`를 명시적으로 적어야 하는지 손으로 만져보자. 그다음, 같은 도메인을 *Java checked exception*으로 표현해보자. `class InvalidPasswordException extends Exception`, `class ExpiredTokenException extends Exception`, `class RateLimitedException extends Exception { Duration retryAfter; }` ... 그리고 메서드 시그니처에 `throws InvalidPasswordException, ExpiredTokenException, RateLimitedException, SQLException`을 줄줄이 적어보자. *어느 쪽이 더 답답한가*를 한 단락으로 적어보자.

이 `AuthError`는 11장 axum의 `IntoResponse` 절에서 다시 호출된다. 거기서 우리는 *도메인 에러가 HTTP 응답으로 어떻게 깔끔하게 변환되는지*를 만나게 된다. 그 변환을 직접 짜보면, *도메인 모델 → 트랜스포트 계층*의 분리가 트레잇 한 줄로 풀린다는 사실에 한 번 놀라게 된다.

7장이 책의 무게중심에서 가장 *후련한* 챕터라고 첫 단락에서 약속했다. 트레잇·제네릭·match·`Result<T, E>`라는 네 도구가 모이면, JVM에서 인터페이스·sealed class·exception이 *각자 다른 모델로 흩어져 있던* 표현력이 *한 모델 안에서 일관되게* 손에 들어온다. 그 일관성이 처음 한 달의 답답함을 보상하는, Rust 표현력의 진짜 보상이다.

다음 8장에서는 메모리 도구상자를 펼친다. `Box<T>`, `Rc<T>`, `Arc<T>`, `RefCell<T>`, `Mutex<T>` — 그리고 안전 경계의 마지막 한 절, `unsafe`. *unsafe는 컴파일러를 끄는 도구가 아니라 책임을 우리에게 옮기는 계약*이라는 정직한 한 줄로, Rust의 안전성이 어디까지인지를 명료하게 보자.

---

## 참고

- [Rust Traits are not interfaces — James Sturtevant](https://www.jamessturtevant.com/posts/rust-traits-are-not-interfaces-and-a-little-on-lifetimes/)
- [Rust Static vs. Dynamic Dispatch — softwaremill](https://softwaremill.com/rust-static-vs-dynamic-dispatch/)
- [Trait Objects to Abstract over Shared Behavior — The Rust Book](https://doc.rust-lang.org/book/ch18-02-trait-objects.html)
- [The state of pattern matching in Java 17 — deepu.tech](https://deepu.tech/state-of-pattern-matching-java/)
- [Rust Error Handling Guide 2025 — Markaicode](https://markaicode.com/rust-error-handling-2025-guide/)
- [Rust Error Handling Compared: anyhow vs thiserror vs snafu — DEV.to](https://dev.to/leapcell/rust-error-handling-compared-anyhow-vs-thiserror-vs-snafu-2003)
- Gäher, L. et al. — [RefinedRust: A Type System for High-Assurance Verification of Rust Programs (PLDI 2024)](https://plv.mpi-sws.org/refinedrust/paper-refinedrust.pdf)
- [Migrating from Java to Rust — corrode](https://corrode.dev/learn/migration-guides/java-to-rust/)

---

# 8장. 스마트 포인터·매크로·unsafe 진입 — 메모리 도구와 안전 경계

7장에서 우리는 표현력의 도구상자를 손에 쥐었다. 이제 8장은 그 표현력 아래에 깔린 *메모리 도구상자*를 펼친다. JVM에서 우리는 *모든 객체 참조가 똑같이 생긴* 단일 모델로 일해왔다. 일반 객체 참조도, 멀티스레드 공유도, 가변 상태 보호도, 불변 보장도 — *코드의 모양*은 같았다. 다른 점은 *우리가 어떤 어노테이션을 붙였는지*, *어떤 lock을 들고 있는지*, *컨벤션을 얼마나 잘 지켰는지*였다. Rust는 그걸 정면으로 뒤집었다. *누가 소유하고, 누가 빌리고, 단일 스레드인지 멀티 스레드인지, 컴파일 검증인지 런타임 검증인지*를 *타입으로 명시한다*. 처음에는 부담이지만, 이 챕터를 지나고 나면 *그 명시가 코드에 박혀 있다*는 사실이 6개월 뒤 가장 큰 보상이 된다는 사실을 받아들이게 된다.

그리고 이 챕터의 마지막 한 절은 정직한 한 줄로 시작한다. `unsafe`는 *컴파일러를 끄는* 게 아니다. *책임을 우리에게 옮기는 계약*이다. 두려움을 부추길 일도 아니고, 가볍게 다룰 일도 아니다. 그 경계가 어디까지인지를 한 절 안에 정확히 박아두자.

## 스마트 포인터 — 다섯 도구의 표 한 장

먼저 표 한 장으로 정면을 보자.

| 도구 | 의미 | 단일/멀티 스레드 | 검증 시점 | JVM 대응물 |
|---|---|---|---|---|
| `Box<T>` | 단일 owner, 힙 할당 | 단일 | 컴파일 | 일반 객체 참조 (단독 owner) |
| `Rc<T>` | 단일 스레드 공유 owner, 참조 카운트 | 단일 | 컴파일 + 런타임(refcount) | (구분 없음) |
| `Arc<T>` | 멀티스레드 공유 owner, atomic refcount | 멀티 | 컴파일 + 런타임(atomic) | `AtomicReference` 감각 |
| `RefCell<T>` | 단일 스레드 interior mutability | 단일 | *런타임* borrow check | 일반 객체의 모양 그대로 |
| `Mutex<T>` (보통 `Arc<Mutex<T>>`) | 멀티스레드 공유 + 가변 | 멀티 | 컴파일 + 런타임(lock) | `synchronized` + 필드 |

이 다섯 도구가 Rust 메모리 도구상자의 95%다. 한 도구씩 천천히 짚어가자.

### `Box<T>` — 가장 단순한 시작

`Box<T>`는 *힙에 값을 올리고, 그 값에 대한 단독 소유권을 들고 있는* 박스다. 가장 단순한 스마트 포인터다.

```rust
let boxed: Box<i32> = Box::new(42);
println!("{}", *boxed);   // dereference로 값을 읽는다
```

언제 쓰는가? 두 가지 경우다. 첫째, 값이 *너무 커서 스택에 두기 부담*이거나(예: 큰 구조체), 둘째, *재귀 자료구조*처럼 컴파일 시점에 크기가 결정되지 않을 때.

```rust
// 재귀 자료구조: 자기 자신을 포함하는 List
enum List {
    Cons(i32, Box<List>),
    Nil,
}
```

`Box`로 감싸지 않으면 `List`의 크기를 *컴파일 시점에 결정할 수 없다*. 자기 자신을 포함하니까 무한 재귀다. `Box`로 감싸면 그 자리에는 *포인터 크기*만 들어가니 크기가 정해진다.

JVM 출신은 이런 일을 *한 번도 의식한 적이 없다*. Java에서 모든 객체는 *항상 힙*이고, 객체 참조는 *항상 포인터 크기*다. 그래서 재귀 자료구조도 그냥 `class Node { Node next; }`로 쓴다. 그 *간편함의 비용*이 GC다. Rust는 *언제 힙에 올릴지를 우리가 명시*하는 모델이다.

### `Rc<T>` — 단일 스레드의 공유 소유권

7장의 어느 순간, 우리는 *한 데이터를 여러 군데서 공유 소유*하고 싶을 때가 있었을 것이다. ownership은 한 명만 가지는 게 원칙이지만, 가끔은 그 원칙을 *우회*해야 한다. 그래프 자료구조에서 한 노드를 여러 부모가 가리키거나, 트리 구조에서 자식이 부모를 역참조해야 할 때.

`Rc<T>`는 *Reference Counting*의 약자다. 같은 데이터에 대한 `Rc`를 여러 개 만들 수 있고, *마지막 `Rc`가 drop될 때 데이터가 해제*된다.

```rust
use std::rc::Rc;

let a = Rc::new(String::from("shared"));
let b = Rc::clone(&a);
let c = Rc::clone(&a);

println!("count = {}", Rc::strong_count(&a));   // 3
```

`Rc::clone`은 *데이터를 복제하지 않는다*. *카운트만 1 증가*시킨다. 모든 `Rc`가 같은 데이터를 가리킨다.

여기서 결정적인 한 줄. **`Rc<T>`는 단일 스레드 전용이다.** 다른 스레드로 보내려고 하면 *컴파일 거부*다. 왜? 카운트 증감이 *atomic이 아니라서* 멀티스레드 환경에서는 race condition이 발생할 수 있다. Rust는 그 사실을 *타입 시스템에* 박아놓았다 — `Rc<T>`는 `Send`도 `Sync`도 아니다.

이 사실이 9장에서 다시 호출된다. *왜 컴파일러가 `Rc`를 thread::spawn에 넘기지 못하게 거부하는가*가 9장의 주요 학습 포인트 중 하나다. 5장에서 두 줄 규칙이 데이터 레이스를 컴파일 타임에 끝낸다고 했던 그 약속의 *연장선*이다.

### `Arc<T>` — 멀티스레드의 공유 소유권

`Arc<T>`는 *Atomically Reference Counted*다. `Rc`와 사용법이 같지만, 카운트 증감이 atomic 연산이라서 멀티스레드 환경에서 안전하다.

```rust
use std::sync::Arc;
use std::thread;

let data = Arc::new(vec![1, 2, 3]);

let mut handles = vec![];
for i in 0..3 {
    let data = Arc::clone(&data);
    handles.push(thread::spawn(move || {
        println!("스레드 {i}: {:?}", data);
    }));
}

for h in handles {
    h.join().unwrap();
}
```

세 스레드가 같은 `Vec`을 공유한다. 모든 스레드가 끝나고 마지막 `Arc`가 drop될 때 `Vec`도 해제된다. 이게 가장 흔한 멀티스레드 공유 패턴이다.

JVM에서는 이런 구분이 없었다. 객체를 두 스레드가 공유하면 그저 *같은 참조*를 들고 있을 뿐이다. GC가 reachability를 알아서 추적해서 마지막 참조가 사라질 때 회수한다. Rust는 *atomic 연산의 비용*을 *타입 선택의 결과*로 만들어놓았다 — 단일 스레드면 `Rc`(원자 연산 절감), 멀티스레드면 `Arc`. *우리가 골라야 한다는 부담*이 *그 선택이 코드에 박혀 있다는 보상*과 짝을 이룬다.

### `RefCell<T>` — interior mutability, 컴파일 검증을 *포기*하는 도구

여기서 잠깐 멈추자. 지금까지 우리가 본 모든 가변 borrow는 *컴파일 타임에* 검증됐다. `&mut T`가 단 하나만, 그리고 다른 borrow와 공존 못 한다는 두 줄 규칙. 그런데 가끔 *컴파일러가 그 검증을 못 하는 패턴*이 있다. 예를 들어 캐시처럼, *외부에서 보면 불변이지만 내부적으로 mutable한 상태를 들고 있어야* 하는 경우.

```rust
struct Cache {
    storage: HashMap<String, String>,
}

impl Cache {
    // get은 외부에서 보면 불변(&self)인데, 내부적으로 storage를 수정하고 싶다
    fn get(&self, key: &str) -> Option<String> {
        // self.storage.insert(...) — 컴파일 에러: cannot borrow as mutable
    }
}
```

이런 경우에 `RefCell<T>`가 나선다. **`RefCell`은 컴파일 타임 borrow 검증을 *포기*하고 *런타임으로 미루는* 도구다.**

```rust
use std::cell::RefCell;
use std::collections::HashMap;

struct Cache {
    storage: RefCell<HashMap<String, String>>,
}

impl Cache {
    fn get(&self, key: &str) -> Option<String> {
        let storage = self.storage.borrow();   // 런타임 borrow check
        storage.get(key).cloned()
    }

    fn set(&self, key: String, value: String) {
        let mut storage = self.storage.borrow_mut();   // 런타임 borrow check
        storage.insert(key, value);
    }
}
```

`borrow()`는 immutable borrow를, `borrow_mut()`은 mutable borrow를 *런타임에* 가져온다. 두 줄 규칙은 그대로 유효하다 — *런타임에 검사*된다는 차이만 있다. 이 규칙이 위반되면? *panic*이 발생한다. 즉 5장의 컴파일 에러가 *런타임 panic*으로 옮겨오는 것이다.

이게 실수로 잘못 쓰면 *큰 사고*가 된다. 컴파일은 통과하는데 운영에서 panic이 터지는 패턴이다. 그래서 *꼭 필요할 때만 쓰자*. 가능하면 다시 설계해서 `&mut self`로 풀어내는 편이 낫다.

JVM 출신에게 `RefCell`은 사실 *Java의 일반 객체와 가장 닮은* 모양이다. Java 객체는 항상 *interior mutable*이다. `final List<String> list`라고 적어도 `list.add(...)`가 동작한다. 즉 *Java는 `RefCell`이 디폴트인 세계*다. Rust는 그걸 *명시적인 도구로 따로 분리*해서, 우리가 *진짜로 그 모델이 필요할 때만* 의도적으로 선택하게 만든다.

### `Mutex<T>` — `Arc<Mutex<T>>`라는 이름의 표준형

마지막 도구. 멀티스레드 환경에서 *공유 가변* 상태가 필요할 때.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));

let mut handles = vec![];
for _ in 0..10 {
    let counter = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    }));
}

for h in handles {
    h.join().unwrap();
}

println!("{}", *counter.lock().unwrap());   // 10
```

`Mutex<T>`는 *내부 데이터에 접근하려면 lock을 잡아야* 하는 도구다. `lock()`이 `Result<MutexGuard<T>>`를 반환하고, `MutexGuard`가 *RAII 패턴으로 lock을 들고 있다가, drop될 때 자동으로 lock을 푼다*. Java의 `synchronized` 블록이 *블록 경계*에서 lock을 푸는 것과 비교하면, Rust의 `MutexGuard`는 *변수의 scope 경계*에서 푼다. 이 두 모델이 결정적으로 다르다 — Java는 *예외가 발생해도 lock이 풀리지만 try-finally 패턴이 시각적으로 명시되어야 안전했던* 반면, Rust는 *어떤 경로든 scope를 벗어나면 자동으로 풀린다*. lock을 안 풀고 return하는 사고가 *구조적으로 불가능*하다.

`Arc<Mutex<T>>`는 *공유 가변 상태의 표준 표현형*이다. `Arc`로 *공유*를, `Mutex`로 *가변*을 분리해서 표현한 것이다. 처음 보면 두 단계 wrap이 부담스럽지만, *그 둘이 분리되어 있어야 의미가 명료하다*는 사실을 깨닫게 된다. 어떤 자료는 *공유는 하지만 불변*(`Arc<T>`만)이고, 어떤 자료는 *가변이지만 단일 스레드*(`RefCell<T>`)고, 어떤 자료는 *공유 가변*(`Arc<Mutex<T>>`)이다 — 그 셋이 *서로 다른 타입*으로 명시된다.

5장의 카운터 예제를 떠올려보자. 단일 스레드에서 `&mut Counter`로 한 명만 가변 borrow를 들고 있던 그 카운터를, 이제 멀티스레드로 옮기려면 `Arc<Mutex<Counter>>`로 감싸야 한다. 5장에서 약속한 *"이 카운터는 9장 `Arc<Mutex<T>>` 절에서 멀티스레드 안전성으로 다시 호출된다"*는 다리가 8장에서 *도구의 모양*으로 한 번 미리 펼쳐진 셈이다.

## 도구 선택의 의사결정 트리

다섯 도구를 어떤 기준으로 고를까? 한 단락의 의사결정 트리로 정리해보자.

1. *공유가 필요한가?* 아니면 → `Box<T>` 또는 그냥 owned 값.
2. 공유가 필요하면, *멀티스레드인가?* 아니면 → `Rc<T>`.
3. 멀티스레드면 → `Arc<T>`.
4. 거기에 *가변이 필요한가?* 아니면 → 위에서 결정한 그대로.
5. 가변이 필요하고 단일 스레드면 → `Rc<RefCell<T>>` 또는 `RefCell<T>`.
6. 가변이 필요하고 멀티 스레드면 → `Arc<Mutex<T>>` (또는 `Arc<RwLock<T>>`).

이 의사결정 트리를 한 번 손에 두면, 새 자료구조를 설계할 때 *어떤 wrap이 어울리는지*가 자연스럽게 떠오른다. 처음에는 매번 의사결정 트리를 펼쳐야 하지만, 한 달쯤 지나면 *반사적으로* 결정된다.

JVM에서 같은 의사결정을 떠올려보자. Java로 하면 어떻게 될까? *모든 자료가 `Arc<RefCell<T>>` 또는 `Arc<Mutex<T>>` 모드*다 — *항상* 공유 가능하고 *항상* 가변이고, 안전성은 우리가 *코드 리뷰와 컨벤션*으로 보장한다. Rust는 그 모든 결정을 *타입으로 강제*한다. 그게 명시성의 비용과 보상이다.

## 매크로 첫 만남 — Lombok과의 거리

7장에서 우리는 thiserror에서 `#[derive(Error)]`를 만났다. 여기까지 오면서 매번 한 번씩 봤을 매크로가 8장에서 정면으로 등장한다.

Rust 매크로는 두 종류다. **declarative macro**(`macro_rules!`)와 **procedural macro**(`proc_macro`).

declarative macro는 *패턴 매칭으로 코드를 펼치는* 도구다.

```rust
// 가장 흔한 declarative macro: vec!
let v = vec![1, 2, 3];
// 위는 다음으로 펼쳐진다
let v = {
    let mut temp = Vec::new();
    temp.push(1);
    temp.push(2);
    temp.push(3);
    temp
};
```

`vec![]`라는 한 줄이 다섯 줄로 펼쳐졌다. `macro_rules!`로 새 매크로를 정의하는 일도 가능하지만, 입문 단계에서는 *기존 매크로를 잘 쓰는 것*이 우선이다. 직접 만드는 건 13장의 *내 매크로 만들기* 절에서 다룬다.

procedural macro는 더 강력하다. `#[derive(...)]`, `#[tokio::main]`, `#[sqlx::query!]` 같은 게 모두 procedural macro다. 토큰을 받아 *임의의 코드를 생성*해서 펼친다.

JVM의 Lombok과 비교하면 결정적인 차이가 두 가지 있다.

첫째, **Rust 매크로는 토큰을 진짜로 펼쳐서 컴파일러가 다시 검사한다.** Lombok은 *바이트코드 단계에서* 메서드를 추가하는 식이라, IDE가 보지 못하면 *마법처럼 메서드가 생기지만 코드에는 안 보이는* 거리감이 생긴다. Rust는 펼친 결과가 *진짜 Rust 코드*고, `cargo expand`로 그 결과를 *눈으로 볼 수 있다*.

```bash
cargo install cargo-expand
cargo expand
```

이 명령이 매크로가 펼쳐진 *완성된 Rust 코드*를 출력한다. `#[derive(Debug)]`가 어떤 메서드를 만들어내는지, `#[tokio::main]`이 main 함수를 어떻게 wrap하는지를 *눈으로 확인*할 수 있다.

둘째, **Rust 매크로는 컴파일 타임에 동작하므로 런타임 reflection이 필요 없다.** Lombok이 추가한 메서드는 reflection 없이도 호출되지만, Spring의 `@Autowired`나 `@Transactional` 같은 어노테이션은 *런타임 proxy*로 동작한다. 그래서 그 메커니즘을 디버깅하기가 까다롭다. Rust는 *모든 것이 컴파일 타임 코드 생성*이라, 디버거로 펼친 결과를 *그대로 따라갈 수 있다*.

## `unsafe` — 정직한 한 절

이제 8장의 가장 중요한 한 절이다. `unsafe`라는 키워드는 Rust를 둘러싼 가장 큰 오해의 출발점이기도 하다. 첫 줄부터 정직하게 박아두자.

**`unsafe`는 컴파일러를 끄는 게 아니다. 책임을 우리에게 옮기는 계약이다.**

이 한 줄이 8장의 가장 중요한 메시지다. unsafe 블록 안에서도 *대부분의 컴파일러 검사는 그대로 동작한다*. 타입 검사, borrow checker, lifetime 검사 모두 평소처럼 작동한다. 다만 `unsafe`가 우리에게 *추가로 허용해주는 다섯 가지*가 있다. 그게 끝이다.

### unsafe가 허용하는 다섯 가지 — 정확히 이것뿐

1. **raw pointer를 dereference하는 것** (`*const T`, `*mut T`).
2. **mutable static 변수에 접근하는 것** (`static mut`).
3. **다른 unsafe 함수를 호출하는 것**.
4. **unsafe trait을 구현하는 것** (`Send`, `Sync` 같은).
5. **union의 필드에 접근하는 것**.

이게 전부다. *모든 것을 풀어주는* 게 아니다. *이 다섯 가지*에 대해서만 컴파일러가 *우리에게 검증을 위임*한다.

```rust
fn main() {
    let x = 5;
    let raw_ptr = &x as *const i32;

    // 컴파일 에러: dereference of raw pointer is unsafe
    // println!("{}", *raw_ptr);

    // unsafe 블록 안에서만 허용
    unsafe {
        println!("{}", *raw_ptr);   // OK
    }
}
```

`*raw_ptr`이 *raw pointer dereference*에 해당하므로 unsafe가 필요하다. 하지만 *그 안에서도* 다른 검사는 다 동작한다. `let mut s = String::new(); unsafe { let r = &s; let r2 = &mut s; }`처럼 빌림 규칙을 위반하면? *unsafe 블록 안이라도 컴파일 에러*다.

### unsafe를 *언제 써야* 하는가

5가지 경우 중 일상에서 마주치는 건 두 가지다.

**FFI 호출.** C 라이브러리나 OS API를 부를 때. 14장 FFI(JNI/Panama/C ABI) 챕터에서 본격적으로 다룬다. C 함수의 시그니처는 Rust가 모르니, 우리가 *불변 조건을 보증*해야 한다.

```rust
extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    let result = unsafe { abs(-42) };
    println!("{result}");
}
```

**low-level 자료구조의 안전 추상화 안에서.** 이게 더 흥미롭다. 표준 라이브러리의 `Vec`, `String`, `Box`, `Rc`, `Arc`, `Mutex` — *모두 내부에 unsafe 코드가 있다*. 왜? 안전한 추상화만으로 표현할 수 없는 메모리 조작이 필요하기 때문이다. 예를 들어 `Vec::push`는 *capacity가 부족하면 새 메모리를 alloc하고 기존 데이터를 복사*한다. 이 일은 안전한 Rust로 표현할 수 없다. 그래서 `Vec` 내부에 unsafe 블록이 들어간다.

이게 Rust 표준 라이브러리의 핵심 설계 패턴이다. **safe API를 unsafe 위에 얹는다.** `Vec`을 *사용하는* 코드는 unsafe가 필요 없다. `Vec::push`, `Vec::get`, `Vec::iter()`는 모두 safe API다. 그 내부에서 *unsafe로 메모리를 조작하되, 그 unsafe 블록의 invariant를 라이브러리 작성자가 보증*한다. 그 보증된 추상화 위에서 *우리는 안전하게* 살 수 있다.

### unsafe를 *언제 쓰지 말아야* 하는가

이게 더 중요하다. 한 줄로 박아두자. **borrow checker를 우회하려고 unsafe를 쓰면 안 된다.** 99%의 경우, *더 나은 안전 코드로 재설계가 가능하다*.

처음 한 달의 답답함 속에서 우리는 가끔 이런 충동을 느낀다. *"이 코드가 컴파일이 안 되니까, 그냥 unsafe로 둘러싸자."* 이건 거의 항상 잘못된 선택이다. 두 가지 이유가 있다.

첫째, 그 unsafe가 *진짜로 안전한지 검증할 도구가 없다*. borrow checker가 안 잡아주면, 잘못된 메모리 접근이 *조용히 통과*해서 운영에서 *알 수 없는 사고*로 터진다. C에서 우리가 살아온 세계로 돌아가는 거다.

둘째, *안전한 재설계가 거의 항상 가능*하다. 보통 답은 `Rc<RefCell<T>>`, `Arc<Mutex<T>>`, 채널, 또는 *데이터 모델 자체를 다시 그리기*에 있다. 처음에는 그 재설계가 어려워 보이지만, 한 번 익숙해지면 *unsafe로 도망가는 일이 거의 없어진다*.

### Stacked Borrows · Tree Borrows — unsafe 영역의 학술적 검증

5장에서 박아두었던 RustBelt 한 단락을 한 번 더 회수하자. **`unsafe` 코드의 borrow 의미를 어떻게 정의해야 안전한지**를, 학계가 별도로 모델링해왔다는 사실이다.

2020년 POPL에 발표된 「Stacked Borrows」(Jung, Dang, Kang, Dreyer)는 *unsafe 코드 안에서 raw pointer와 reference가 혼재할 때*의 안전성 모델을 제시했다. 그 후속인 「Tree Borrows」(2025 PLDI)는 그 모델의 한계를 보완해서 *더 많은 실제 unsafe 패턴이 모델 안에서 인정받을 수 있게* 했다. Miri라는 도구가 이 모델을 구현해서, *우리가 짠 unsafe 코드가 모델을 위반하는지를 자동으로 검사*해준다.

```bash
cargo +nightly miri test
```

이 한 줄이, unsafe를 포함한 우리 코드를 *형식 모델 안에서 검증*해준다. unsafe를 정말로 써야 하는 자리(예: low-level 자료구조 작성)에서는, Miri로 검증하는 습관이 *최소한의 안전망*이다.

학술 인용 한 줄을 더해보자. Cui 외의 「Is unsafe an Achilles' Heel?」(arXiv:2308.04785)는 실무에서 unsafe가 *잘못 쓰이는 패턴 5가지*를 분류했다. 핵심은 *대부분의 unsafe 사고가 안전 추상화의 invariant를 깨는 데서 온다*는 것이다. 즉 라이브러리 작성자가 *내가 만든 safe API의 사용자가 어떤 invariant를 가정해도 되는지*를 정확히 정의하고, unsafe 블록 안에서 그 invariant를 보장해야 한다.

deepSURF (IEEE S&P 2026, arXiv:2506.15648)는 *unsafe 영역의 메모리 사고를 자동으로 탐지하는 도구*다. 이런 학계의 노력이 한 방향을 가리킨다 — *unsafe를 두려워할 필요는 없다, 다만 정직하게 다뤄야 한다*.

### 안전 경계의 역할 — 마지막 한 단락

이제 8장의 마지막 한 단락이다. `unsafe`라는 도구가 Rust의 안전성에 어떤 위치를 차지하는지를 한 번 더 명료하게 박아두자.

Rust의 안전성 모델은 다음과 같이 *단계적*이다. *대부분의 코드*는 safe Rust로 짠다 — borrow checker가 모든 것을 검증한다. *드물게* unsafe가 필요한 자리(저수준 자료구조, FFI)에서는, *그 unsafe 블록을 safe API로 wrap*해서 외부에 안전한 인터페이스만 노출한다. 사용자는 그 safe API만 본다. 안전하다.

이 모델이 무너지는 건 *unsafe의 invariant를 깨는 코드*가 들어왔을 때다. 라이브러리 작성자가 보증하기로 한 invariant를 사용자가 *우회해서 깨면*, 그게 운영 사고로 이어진다. 그래서 unsafe를 포함한 라이브러리 작성자는 *문서에 invariant를 정확히 적고*, *그것을 깰 수 있는 사용 패턴을 차단*해야 한다.

JVM에서는 이런 모델이 다르게 펼쳐졌다. *모든 것이 안전한 Java*가 있고, *unsafe는 JNI 너머의 C/C++ 세계*다. 두 세계의 경계가 *명확하게 분리*되어 있다. Rust는 그 두 세계가 *같은 언어 안에 있되, 명시적인 키워드로 경계가 그어져 있다*. unsafe가 *진짜로 필요한 자리*에서만 *국소적으로 허용*되고, 그 외 모든 곳에서는 안전성이 *기본*이다.

그리고 한 가지 더 — *15장 JNI/Panama/C ABI는 unsafe의 가장 큰 사용처다*. 거기서 우리는 *Java 객체와 Rust 데이터를 잇는 경계*에서 어떤 invariant를 보증해야 하는지를 정면으로 다룬다. 그때 8장의 이 절을 다시 펼쳐 읽게 될 것이다.

## 함께 해보자

8장의 도구 다섯을 한 자리에서 손으로 만져보자. 작은 트리 구조를 만들어 한 노드의 값을 바꾸는 연습이다.

```rust
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
struct Node {
    value: i32,
    children: Vec<Rc<RefCell<Node>>>,
}

fn main() {
    let leaf1 = Rc::new(RefCell::new(Node { value: 1, children: vec![] }));
    let leaf2 = Rc::new(RefCell::new(Node { value: 2, children: vec![] }));
    let root = Rc::new(RefCell::new(Node {
        value: 0,
        children: vec![Rc::clone(&leaf1), Rc::clone(&leaf2)],
    }));

    // leaf1의 값을 바꿔보자
    leaf1.borrow_mut().value = 100;

    // root에서 leaf1을 봐도 100으로 바뀌어 있다 (공유되니까)
    println!("{:?}", root);
}
```

이 코드를 직접 두드려보고, 다음 두 가지를 손으로 시도해보자.

1. `Rc::clone(&leaf1)`이 *데이터를 복제하지 않고 카운트만 늘린다*는 사실을, `Rc::strong_count(&leaf1)`을 출력해 확인해보자. root를 만들기 전후로 카운트가 어떻게 변하는지.
2. `leaf1.borrow_mut()`을 두 번 동시에 들고 있으려고 시도해보자. *컴파일은 통과하지만 런타임 panic*이 발생한다. 이게 `RefCell`의 *런타임 borrow check*가 동작하는 모양이다. 5장의 컴파일 에러가 *런타임으로 옮겨진* 사례를 직접 보면 *왜 가능하면 컴파일 검증으로 풀어내야 하는지*가 손에 묻는다.

그다음, `cargo expand`로 `#[derive(Debug)]`가 무슨 코드를 만들어내는지 펼쳐보자. *마법이 사라진다*. 펼쳐진 코드가 그저 *우리가 손으로 적을 수 있는 Rust 코드*일 뿐이라는 사실을 눈으로 보면, 매크로가 더 이상 *블랙박스*가 아니다.

이 `Rc<RefCell<T>>` 패턴은 9장에서 *Send 위반으로 컴파일이 거부되는* 사례로 다시 호출된다. *왜 이걸 thread::spawn에 못 넘기는지*가 거기서 명료해진다. 그리고 unsafe는 15장 JNI 함수 시그니처에서 다시 호출된다. *Java 객체와 Rust 데이터의 경계*에서 어떤 invariant를 보증해야 하는지를, 그때 정면으로 다룬다.

8장이 Part 2의 마지막 챕터다. 4·5·6·7·8장을 묶어, 우리는 *컴파일러와 친구가 되는 길*을 절반 이상 걸어왔다. 소유권으로 시작해서 빌림으로 데이터 레이스를 끝내고, 라이프타임으로 메모리 lifetime을 사고하는 법을 배우고, 트레잇·제네릭·match·`Result`로 표현력의 도구상자를 손에 쥐고, 마지막으로 스마트 포인터·매크로·unsafe로 메모리 도구의 전 영역을 펼쳐봤다. 이제 손에 든 것이 *Rust의 마음*이다.

다음 9장에서는 그 도구들을 들고 *동시성*의 세계로 들어간다. 5장의 두 줄 규칙이 *멀티스레드 안전성*으로 어떻게 보상받는지, 그리고 `Send`와 `Sync`라는 마커 트레잇이 *왜 8장의 `Rc`를 thread::spawn에 못 넘기게 만드는지*를 정면으로 다룬다. *"이제 Spring으로 짜던 그 서비스가 Rust로 보인다"*는 자신감이 본격적으로 손에 묻기 시작하는 챕터다.

---

## 참고

- [Smart Pointers Demystified — DEV.to](https://dev.to/sgchris/smart-pointers-demystified-box-rc-and-refcell-27k)
- [Mastering Safe Pointers in Rust — Technorely](https://technorely.com/insights/mastering-safe-pointers-in-rust-a-deep-dive-into-box-rc-and-arc)
- [The Drop Trait as Finalizer — Medium](https://medium.com/@bugsybits/the-drop-trait-as-finalizer-rusts-hidden-destructor-pattern-d7d38798d6ac)
- [Procedural macros in Rust — LogRocket](https://blog.logrocket.com/procedural-macros-in-rust/)
- [Macros — The Rust Book](https://doc.rust-lang.org/book/ch19-06-macros.html)
- [Send and Sync — The Rustonomicon](https://doc.rust-lang.org/nomicon/send-and-sync.html)
- Jung, R., Dang, H.-H., Kang, J., Dreyer, D. — [Stacked Borrows: An Aliasing Model for Rust (POPL 2020)](https://plv.mpi-sws.org/rustbelt/stacked-borrows/paper.pdf)
- Villani, N., Hostert, J., Dreyer, D., Jung, R. — [Tree Borrows (PLDI 2025)](https://iris-project.org/pdfs/2025-pldi-treeborrows.pdf)
- Cui, M. et al. — [Is unsafe an Achilles' Heel? A Comprehensive Study of Safety Requirements in Unsafe Rust Programming (arXiv:2308.04785)](https://arxiv.org/abs/2308.04785)
- [deepSURF: Detecting Memory Safety Vulnerabilities in Rust (IEEE S&P 2026, arXiv:2506.15648)](https://arxiv.org/html/2506.15648v2)

---

# Part 3. 실무 시스템을 만든다

> *"이제 Spring으로 짜던 그 서비스가 Rust로 보인다."*

Part 3은 *손이 코드를 만지는 자리*다. 9장 동시성 기초에서 5장 borrow의 두 줄 규칙이 *멀티스레드 안전성*으로 보상받는 순간을 맛보고, `Arc<Mutex<T>>`가 *공유 가변 상태의 표준 표현형*이라는 사실을 손가락으로 확인한다. 10장에서 async/await와 tokio로 Kotlin Coroutine 다음의 모델을 손에 쥐고, *세 가지 함정*(JoinHandle 누락 / await를 가로지르는 동기 Mutex guard / async 안 blocking 호출)을 미리 박아둔다. 11장 axum에서 *Spring Controller가 Rust로 보이는 순간*이 오고, 7장에서 만든 `AuthError` enum이 `IntoResponse`로 자연스럽게 HTTP 응답에 매핑되는 모양을 본다. 12장에서 sqlx의 *컴파일 타임 검증된 SQL*과 sea-orm의 친숙한 ORM 사이에서 *자기 출신에 맞는 길*을 고르고, 11장의 in-memory 서비스를 PostgreSQL 위로 옮긴다. Part 3이 끝나면 자네는 *Spring으로 짜던 그 서비스 한 채를 Rust로 짤 수 있다*는 자신감에 도달해 있다.

**포함 챕터**

- 9장. 동시성 기초 — 스레드, channel, Mutex, 그리고 `Send`/`Sync`
- 10장. async와 tokio — Spring WebFlux/Kotlin Coroutine 다음의 모델
- 11장. axum으로 첫 HTTP 서비스 — Spring Controller가 Rust로 보이는 순간
- 12장. 데이터베이스 — sqlx로 컴파일 타임 검증된 SQL을, sea-orm으로 친숙한 ORM을


---

# 9장. 동시성 기초 — 스레드, channel, Mutex, 그리고 `Send`/`Sync`

월요일 아침 결제 API에 부하가 몰린다고 해보자. 트래픽이 두 배로 뛴 순간 응답이 느려지고, 한참 뒤 로그를 들춰보니 `ConcurrentModificationException`이 한 줄, 그리고 의심 가는 카운터의 값이 *이상하게* 작다. 누군가 동시 접근을 막지 않았다. `synchronized`를 빼먹었거나, `AtomicInteger`로 바꾼다는 걸 깜빡했거나. 코드 어디인지 *런타임이 한참 지나서야* 드러난다. 이런 사고를 한 번이라도 겪어본 사람이라면 다음 질문이 자연스럽게 떠오른다. *왜 컴파일러는 이걸 못 잡아주지?*

자바 진영의 답은 늘 비슷했다. `@ThreadSafe`라는 어노테이션이 있긴 하다. 그런데 그게 *문서일 뿐* 강제력이 없다. `@GuardedBy("this")`도 마찬가지다. FindBugs/SpotBugs가 *힌트로* 잡아주긴 하지만, 어기는 코드를 *빌드가 거부*하지는 않는다. 결국 우리는 *관행과 코드 리뷰*에 데이터 안전성을 맡겨왔다.

Rust가 이 지점에서 다른 길을 간다. 같은 카운터, 같은 멀티스레드, 같은 의도다. 하지만 *컴파일러가* `synchronized`를 빼먹은 코드를 거부한다. 9장의 전부가 이 한 줄이다. **JVM의 `synchronized`는 잊어도 된다 — 왜냐하면 컴파일러가 그 자리에 들어와 있기 때문이다.** 이 문장이 과장처럼 들린다면, 5장에서 심어둔 *빌림의 두 줄 규칙*이 어떻게 *멀티스레드 안전성*으로 자라나는지를 함께 따라가 보자.

## std::thread::spawn — `Thread`/`ExecutorService`의 첫 인사

먼저 가장 단순한 모양부터 손에 묻혀보자. JVM에서 `new Thread(() -> { ... }).start()` 하던 일을 Rust는 이렇게 적는다.

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        println!("새 스레드에서 한마디");
    });
    handle.join().unwrap();
    println!("메인 스레드도 끝.");
}
```

`thread::spawn`이 받는 건 `FnOnce + Send + 'static` 클로저다. 이 세 단어가 결국 9장의 모든 함정과 보상을 미리 박아둔다는 사실을 한번 짚어두자. `Send`는 이 챕터의 후반부에서 본격적으로 다룰 마커이고, `'static`은 6장에서 만난 *그 long-lived 라이프타임*이다. JVM에서 `Runnable`을 `Thread` 생성자에 넘길 때는 라이프타임 따위를 신경 쓸 필요가 없었다 — GC가 알아서 잡아주니까. Rust는 *컴파일러에게 한 번 일러두자*. "이 클로저 안에서 빌리는 모든 값은 새 스레드보다 오래 산다."

실제로 이런 코드를 짜보자.

```rust
let s = String::from("hello");
let handle = thread::spawn(|| {
    println!("{s}");
});
```

이게 바로 컴파일러가 거부하는 코드다. `s`를 빌리려 했는데, 메인 스레드에서 `s`가 *언제 drop될지*를 컴파일러가 보증할 수 없다. 그래서 에러 메시지가 친절하게 일러준다. *"closure may outlive the current function, but it borrows `s`"*. 처방은 두 가지다. 하나, `move` 키워드로 ownership을 새 스레드에 넘긴다.

```rust
let s = String::from("hello");
let handle = thread::spawn(move || {
    println!("{s}");
});
handle.join().unwrap();
```

이제 컴파일이 통과한다. 둘, 정말로 빌리고 싶다면 `Arc`로 감싸야 한다 — 이 얘기는 잠시 뒤에 본격적으로 한다.

JVM에서 `ExecutorService`로 풀(pool)을 만들어 작업을 던지던 패턴은 Rust에서는 *런타임을 직접 들이는* 모양이 된다. `std::thread`만으로도 풀을 짤 수 있지만, 실무에서는 `rayon`(데이터 병렬)이나 `tokio`(async, 10장)를 쓰는 편이 낫다. 9장은 그 토대를 깔아둘 뿐이다.

## std::sync::mpsc — `BlockingQueue`의 감각

스레드 사이에 데이터를 주고받자. JVM에서는 `BlockingQueue<T>`(또는 Kotlin의 `Channel<T>`)로 producer-consumer를 짜던 일이다. Rust 표준 라이브러리에는 `std::sync::mpsc`가 있다. mpsc는 *multi-producer, single-consumer*의 약자다.

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    for i in 0..3 {
        let tx = tx.clone();
        thread::spawn(move || {
            tx.send(format!("작업 {i} 완료")).unwrap();
        });
    }
    drop(tx); // 모든 송신자가 닫혀야 rx의 iter가 종료된다.

    for msg in rx {
        println!("받음: {msg}");
    }
}
```

`tx.clone()`이 producer를 늘리는 자연스러운 표현이다. JVM의 `BlockingQueue`는 producer/consumer 구분이 없는 한 객체였다는 점과 비교해보자. Rust는 *송신*과 *수신*을 타입으로 분리한다 — 누가 보내고 누가 받는지가 코드에 드러난다는 사실 자체가 동시성 코드의 가독성을 한 단계 끌어올려 준다.

여기서 한 가지 혼동하기 쉬운 부분을 미리 짚자. `std::sync::mpsc`는 *동기 채널*이다. 10장에서 만나게 될 `tokio::sync::mpsc`(async 채널)와 이름은 같지만 다른 도구다. async 함수 안에서는 std mpsc를 쓰지 *말아야 한다* — 블로킹이 일어나면 같은 스레드의 다른 task가 멈춘다. 이 함정은 10장에서 본격적으로 다시 만난다.

다양한 모양이 필요하면 `crossbeam::channel`을 쓰는 편이 낫다. select, bounded 채널, deadline 등 std mpsc가 안 가진 기능을 다 갖췄다. JVM 출신에게는 LMAX Disruptor의 감각이 가장 가깝다.

## `Arc<Mutex<T>>` — 공유 가변 상태의 표준 표현형

이제 5장의 카운터를 다시 꺼내자. 5장에서 우리는 *한 시점에 mutable borrow는 하나만*이라는 두 줄의 규칙을 배웠다. 그 규칙이 *멀티스레드*로 옮겨오면 어떤 모양이 될까?

먼저 의도적으로 잘못된 코드를 짜보자.

```rust
use std::thread;

fn main() {
    let mut counter = 0i64;
    let mut handles = vec![];

    for _ in 0..100 {
        let handle = thread::spawn(|| {
            counter += 1; // 컴파일 에러!
        });
        handles.push(handle);
    }
    for h in handles { h.join().unwrap(); }
    println!("{counter}");
}
```

컴파일러가 곧장 거부한다. *"closure may outlive the current function"* — 5장에서 본 그 메시지의 멀티스레드 버전이다. 더 구체적으로는 *"cannot borrow `counter` as mutable, as it is a captured variable in a `Fn` closure"*. 100개 클로저가 동시에 같은 카운터를 mutable borrow하겠다는 건 *두 줄 규칙*의 정면 위반이다. JVM이라면 이 코드가 *컴파일은 통과하고* 런타임에 카운터가 90 언저리로 끝나서 *우리가 한참 뒤에 발견*했을 코드다. Rust는 *빌드가 거부*한다. 이 차이가 9장 전체의 한 문장이라는 점을 잊지 말자.

처방은 `Arc<Mutex<T>>` 패턴이다. 8장의 스마트 포인터 표를 다시 펼쳐보자. `Arc<T>`는 *멀티스레드 공유 owner*, `Mutex<T>`는 *동기화된 가변 접근*. 이 둘을 합치면 *공유 가변 상태의 표준 표현형*이 된다.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0i64));
    let mut handles = vec![];

    for _ in 0..100 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut guard = counter.lock().unwrap();
            *guard += 1;
        });
        handles.push(handle);
    }
    for h in handles { h.join().unwrap(); }

    println!("{}", *counter.lock().unwrap());
}
```

100개 스레드가 같은 카운터를 안전하게 +1 한다. 결과는 정확히 100이다 — *언제나 100이다*. JVM에서 `synchronized` 블록을 빼먹어 88, 92, 95로 흔들리던 그 사고가 *코드 모양으로 불가능해진* 셈이다.

여기서 두 가지를 자세히 보자. 첫째, `Arc::clone(&counter)`는 *데이터를 복제*하지 않는다 — 참조 카운트를 +1할 뿐이다. 100개 스레드가 같은 `Mutex<i64>`를 공유한다. 둘째, `counter.lock().unwrap()`이 반환하는 `MutexGuard`는 *RAII로 풀린다*. 즉 스코프를 벗어나는 순간 자동으로 unlock된다. JVM의 `synchronized` 블록은 닫는 중괄호에서 풀리지만, `ReentrantLock.lock()` 다음에 `try { ... } finally { lock.unlock(); }`을 빠뜨려 *영원히 잠긴 락*을 만든 사고는 한 번쯤 본 적이 있을 것이다. Rust에서는 *그 사고가 구조적으로 불가능하다*. lock guard를 들고 있다가 panic이 나도 스택 unwinding 과정에서 자동으로 풀린다.

`Mutex` 외에 `RwLock<T>`도 있다. 다수 reader / 단일 writer가 필요하다면 `Arc<RwLock<T>>`. JVM의 `ReentrantReadWriteLock`과 같은 발상이다. 그리고 카운터처럼 단순한 정수 연산이라면 `std::sync::atomic::AtomicI64`를 쓰는 편이 더 가볍다 — `AtomicReference`, `AtomicLong`의 Rust 대응물이다.

## 그런데 왜 `Mutex`가 아니라 `Arc<Mutex<T>>`인가

JVM 출신이 자주 묻는 질문이다. Java라면 그냥 `Mutex<T>` 같은 객체 하나를 만들어 모든 스레드가 같은 참조를 들면 끝 아닌가? 왜 한 단계 더 감싸야 하지?

답은 4장의 소유권에 있다. `Mutex<T>`는 *그 자체로 owner*다. 누군가 한 명만 가진다. 100개 스레드가 같은 mutex를 *나눠 가지려면* 누군가 owner를 *공유 가능한 형태*로 만들어줘야 한다. 그게 바로 `Arc<T>`의 일이다. JVM은 *모든 객체 참조가 늘 공유 가능*하기 때문에 이 단계가 보이지 않았을 뿐이다.

그래서 Rust 코드에서 `Arc<Mutex<T>>`라는 표현형을 만나면 두 부분을 분리해서 읽자. `Arc`는 *공유*, `Mutex`는 *동기화된 가변*. 이 두 책임이 *분리된 타입으로 코드에 박혀 있다*는 사실이 처음엔 번거롭게 느껴지지만, 6개월 뒤에는 *읽는 순간 의미가 잡히는* 안도감이 된다.

## Send / Sync — 컴파일러가 채워주는 마커 트레잇

이제 9장의 핵심으로 들어가자. *Rust는 어떻게 data race를 컴파일 타임에 차단하는가?* 답이 `Send`와 `Sync`라는 두 마커 트레잇이다.

먼저 정의를 짚고 가자.

- **`Send`** — "이 타입의 값은 ownership을 다른 스레드로 *이동*시켜도 안전하다."
- **`Sync`** — "이 타입의 값을 여러 스레드에서 *동시에 참조*해도 안전하다(`&T`로)."

이름이 직관적이지 않아 처음에는 헷갈린다. 이렇게 외워두자. *Send는 보내는 것, Sync는 함께 보는 것*. 그리고 둘 다 *마커 트레잇*이다 — 메서드가 없다. 그저 *"이 타입이 멀티스레드에 안전하다"*는 정보를 타입 시스템에 박아두는 라벨일 뿐이다.

여기서 한숨 돌리자. **Send/Sync는 우리가 늘 적는 트레잇이 아니다.** 컴파일러가 *자동으로* 채워준다. 어떤 구조체의 모든 필드가 Send면 그 구조체도 Send. 모든 필드가 Sync면 그 구조체도 Sync. 우리가 새 타입을 만들 때 *대부분의 경우* `impl Send for ...`나 `impl Sync for ...`를 직접 적을 일이 없다. 8장에서 만난 거의 모든 타입(`i32`, `String`, `Vec<T>`, `Box<T>`, `Arc<T>`, `Mutex<T>`)이 자동으로 둘 다 구현한다.

그렇다면 *언제* Send/Sync가 *없는* 타입을 만나는가? 두 자리만 기억해두면 된다.

첫째, **`Rc<T>`는 Send도 Sync도 아니다.** 8장에서 본 `Rc<T>`는 *단일 스레드 reference counting*이다. 참조 카운트 변경이 atomic하지 않기 때문에 멀티스레드에서 race condition이 일어난다. 그래서 Rust 표준 라이브러리는 *아예 Send/Sync를 구현하지 않는다*. 8장의 트리 예제에 썼던 `Rc<RefCell<Node>>`를 한번 멀티스레드로 옮겨보자.

```rust
use std::rc::Rc;
use std::cell::RefCell;
use std::thread;

fn main() {
    let shared = Rc::new(RefCell::new(0));
    let s = Rc::clone(&shared);
    thread::spawn(move || {        // 컴파일 에러!
        *s.borrow_mut() += 1;
    });
}
```

에러 메시지가 곧장 나온다. *"`Rc<RefCell<i32>>` cannot be sent between threads safely"*. `Rc<T>`가 Send가 아니기 때문이다. 처방은 명확하다. 멀티스레드라면 `Arc<T>`로 옮긴다. 그리고 `RefCell`도 Sync가 아니므로 안쪽도 `Mutex`로 바꿔야 한다. 결과적으로 `Arc<Mutex<i32>>` — 위에서 본 그 표준 표현형이다. 컴파일러가 한 줄 한 줄 *어디를 바꿔야 하는지*를 일러준다.

둘째, **`*const T`와 `*mut T`(raw pointer)는 Send도 Sync도 아니다.** 8장의 unsafe 절에서 만난 그 raw pointer다. 멀티스레드 안전성을 컴파일러가 보장할 수 없으니 *기본은 거부*한다. 정말로 멀티스레드에 들이려면 우리가 *unsafe로 보증*하면서 `unsafe impl Send for MyType {}`를 적어준다. 표준 라이브러리의 거의 모든 자료구조 내부에 이 패턴이 깔려 있다.

이 자동 채움 메커니즘이 갖는 의미를 한 번 더 짚자. JVM에서 우리는 *어떤 객체가 thread-safe인지*를 *문서를 읽어* 알아내야 했다. `HashMap`은 thread-safe가 아니고 `ConcurrentHashMap`은 thread-safe다. 그런데 *어기는 코드를 컴파일러가 거부하는가?* 아니다. `HashMap`을 멀티스레드에서 쓰는 코드도 *빌드는 통과하고* 런타임에 데이터가 깨질 뿐이다. Rust는 그 일을 *타입 시스템에 박아둔다*. 함수 시그니처가 `T: Send + 'static`을 요구하면 컴파일러가 거부하고, 우리가 잘못된 타입을 넣으면 *빌드가 멈춘다*. **JVM의 `@ThreadSafe`/`@GuardedBy`가 *문서이자 분석 도구의 힌트*였다면, Send/Sync는 *컴파일러의 거부*다.** 이 한 줄이 토픽 5의 모든 것이다.

## Lock guard의 RAII — "lock 안 풀고 return"이 구조적으로 불가능한 이유

위에서 잠깐 짚었던 부분을 한 번 더 손에 묻혀두자. JVM에서 가장 흔한 락 사고는 두 가지다. 하나, `lock.unlock()`을 빠뜨려 영원히 잠긴 락. 둘, 예외가 나서 `unlock`이 안 불리는 락. 그래서 Java 코드는 항상 이렇게 적도록 권장된다.

```java
lock.lock();
try {
    // critical section
} finally {
    lock.unlock();
}
```

또는 `synchronized` 블록을 쓰는 편이 낫다. 그럼 닫는 중괄호에서 자동으로 풀린다. 그런데 Java 24가 와도 *컴파일러는 `lock.lock()` 뒤에 `unlock()` 빼먹은 코드를 거부하지 않는다*. 우리가 *관행*으로 막아왔을 뿐이다.

Rust는 다르다. `Mutex<T>::lock()`이 반환하는 건 단순한 boolean이 아니라 `LockResult<MutexGuard<'_, T>>`다. `MutexGuard`는 4장의 `Drop` 트레잇을 구현한 RAII 가드다. 이 가드가 *스코프를 벗어나는 순간* 자동으로 unlock된다. 우리는 그저 가드의 데이터에 접근만 하면 된다.

```rust
fn increment(counter: &Mutex<i64>) {
    let mut guard = counter.lock().unwrap();
    *guard += 1;
} // 여기서 guard가 drop되면서 자동 unlock.
```

panic이 나도 스택 unwinding이 `Drop`을 호출한다 — 락이 풀린다(엄밀히는 *poisoned* 상태가 되어 다음 lock 호출이 에러를 반환하는데, 이 자체가 *데이터가 손상됐을 수 있다*는 신호다). JVM의 `try-finally`가 *관행으로* 보장하던 일이 *타입 시스템의 결과로* 따라온다. 4장에서 만난 `Drop`이 멀티스레드에서 *어떻게 보상받는지*가 바로 이 자리에서 드러난다.

## Send 위반 한 컷 더 — `MutexGuard`는 Send지만 Sync는 아니다

조금 깊은 이야기 하나만 짚고 가자. 처음 봤을 때 *왜?* 싶은 사실이다. `Mutex<T>::lock()`이 반환하는 `MutexGuard<'_, T>`는 Send도 Sync도 양쪽 다일 것 같지만, 사실 `Sync`가 아니다(엄밀히는 T가 Sync일 때만 Send이고, 본인은 Sync 제약이 다르다). 더 중요한 함정은 *async 코드에서* 이 가드를 await 지점을 가로질러 들고 있으면 데드락이 난다는 점이다. 이 부분은 10장에서 본격적으로 다룬다.

핵심은 이렇다. **표준 라이브러리의 동시성 도구들은 자기가 어디까지 안전한지를 *타입의 trait 구현으로* 표현한다.** 우리가 잘못된 자리에 가져다 놓으면 컴파일러가 `Send` 또는 `Sync` 제약 위반을 들먹이며 거부한다. *어디가 문제인지를 문장으로* 일러준다. 이 대화의 패턴에 익숙해지면, 첫 한 달의 *막막함*이 *컴파일러와의 짧은 대화*로 바뀌어 간다.

## 데드락은 안 막아준다 — Rust의 솔직한 한계

여기서 한 번 솔직해지자. 9장의 모든 자랑에도 불구하고, **Rust도 데드락은 안 막는다**. 두 개의 mutex를 서로 다른 순서로 잠그는 코드를 짜면 *런타임에* 데드락이 난다. Java/Kotlin과 똑같다. 컴파일러는 *데이터 race*를 막을 뿐, *락 ordering*까지 추적해주지는 않는다.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let a = Arc::new(Mutex::new(0));
let b = Arc::new(Mutex::new(0));

let (a1, b1) = (Arc::clone(&a), Arc::clone(&b));
thread::spawn(move || {
    let _g1 = a1.lock().unwrap();
    let _g2 = b1.lock().unwrap(); // 운 나쁘면 여기서 멈춤.
});

let _g1 = b.lock().unwrap();
let _g2 = a.lock().unwrap(); // 운 나쁘면 여기서 멈춤.
```

이 코드는 컴파일이 잘 통과한다. 그리고 운이 나쁘면 *영원히 멈춘다*. 처방은 JVM 출신이 이미 알고 있는 그것이다. *락 순서를 항상 같게 유지한다, 한 번에 하나의 락만 잡는다, 가능하면 lock-free 자료구조나 채널 기반 설계로 옮긴다*. Rust가 컴파일러로 막아주지 못하는 영역이 어디까지인지를 정확히 알아두는 것이 *바이블*의 정직한 자세다.

`parking_lot` crate는 표준 `Mutex`보다 빠르고 poisoning이 없으며 deadlock detection 기능을 옵션으로 제공한다. 큰 서비스에서는 한번 들여다볼 만하다. 그리고 `tokio-console`(14장)이 async 환경에서 데드락 후보를 시각화해준다 — 이 얘기는 10장에서 다시 만난다.

## Send/Sync가 잡지 못하는 사각지대 정리

한 번에 정리해두자. Rust 컴파일러가 동시성에 대해 *잡아주는 일*과 *못 잡는 일*은 이렇게 갈린다.

| 항목 | 컴파일러가 잡는가? |
|---|---|
| Data race (한 자리를 동시에 read/write) | 잡는다 |
| 다른 스레드로 보낼 수 없는 타입 전달 | 잡는다 |
| Lock unlock 누락 | 잡는다 (RAII) |
| 락 ordering 위반으로 인한 데드락 | *못 잡는다* |
| Atomic 연산의 memory ordering 오용 | *못 잡는다* (런타임 검증 도구 필요) |
| Logical race (의미상의 경합) | *못 잡는다* |
| Async Mutex guard를 await 가로질러 들고 있기 | clippy가 경고는 한다 (10장) |

JVM의 어떤 도구도 첫 세 줄을 *컴파일 타임에* 잡지는 못한다. 그게 Rust가 9장에서 손에 쥐여주는 *진짜 보상*이다. 마지막 세 줄은 어느 언어든 여전히 우리의 사고를 요구한다 — 컴파일러가 모든 일을 해주지는 않는다는 *균형 감각*을 잃지 말자.

## 함께 해보자

100개 스레드가 동시에 카운터를 +1하는 코드를 짜보자. 첫 시도는 의도적으로 Mutex 없이 — 컴파일러가 무엇을 거부하는지 한 줄 한 줄 읽어보자. 그다음 `Arc<Mutex<i64>>`로 고쳐 통과시키고, 결과가 *언제나 정확히 100*인지 100번 돌려보자. 마지막으로 `Rc<Mutex<i64>>`로 바꿔서 컴파일러가 무엇을 *추가로* 거부하는지 확인하자(Send 트레잇 결여).

여유가 있다면 `std::sync::atomic::AtomicI64`로 같은 카운터를 짜보고, `Arc<Mutex<i64>>` 버전과 처리량을 비교해보자. 단순 정수 카운터라면 atomic이 더 가볍다는 사실을 손에 묻혀두자. *(이 `Arc<Mutex<T>>` 패턴은 11장 axum의 `State`에서 다시 호출되고, Send 위반은 10장 tokio `spawn`의 함정에서 한 번 더 만난다. 그리고 데드락 회고는 16장 운영 사고 회고에서 다시 다룬다.)*

## 마무리

9장의 한 줄을 다시 적어두자. **JVM의 `synchronized`는 잊어도 된다 — 그 자리에 컴파일러가 들어와 있다.** 5장에서 심은 빌림의 두 줄 규칙이 `Send`/`Sync`라는 마커를 통해 *멀티스레드 안전성*으로 자라났다. 우리가 직접 `impl Send for ...`를 적을 일은 거의 없다 — 컴파일러가 *알아서* 채워주는 마커이고, 그 자동 채움이 우리 일상의 동시성 코드를 *조용히 검증*한다. 그 사실이 안도감을 준다. *어떤 객체가 thread-safe인지를 문서로 외워야 했던 시절*이 끝난 것이다.

물론 데드락과 logical race는 여전히 우리의 사고를 요구한다. Rust는 *마법*이 아니다. 그러나 *압도적 다수의 동시성 사고*를 *빌드 타임에* 잡아준다는 사실 하나만으로도, 운영팀의 새벽 알림이 한 카테고리만큼 줄어든다.

다음 10장에서는 *async/await*로 넘어간다. 9장의 `std::thread`가 OS 스레드를 직접 다뤘다면, 10장은 *수만 개의 task를 한 줌의 스레드에* 얹는 모델이다. Spring WebFlux와 Kotlin Coroutine을 써본 출신이 가장 빠르게 적응할 영역이지만, *함수 색깔(function coloring)*이라는 코루틴과의 가장 큰 철학 차이가 한 절을 차지하게 된다. *async는 마법이 아니다 — `Future`는 상태 머신이고, `.await`는 일시 정지점일 뿐이다*는 한 줄을 미리 머리에 넣어두자.

## 참고

- *Send and Sync — The Rustonomicon*. https://doc.rust-lang.org/nomicon/send-and-sync.html
- *The Rust Programming Language — Fearless Concurrency*. (rust-lang 공식 책)
- *Tokio docs — Channels*. https://docs.rs/tokio/
- 토픽 5(reference.md §132–163): Send/Sync, async/await, tokio, channel, Mutex.
- 토픽 4(reference.md §104–130): 스마트 포인터 표(`Box`/`Rc`/`Arc`/`RefCell`/`Mutex`/`RwLock`).

---

# 10장. async와 tokio — Spring WebFlux/Kotlin Coroutine 다음의 모델

월요일 오후, 마이크로서비스 한 대가 외부 API 열 곳을 동시에 호출하고 결과를 합산해 응답해야 한다고 해보자. JVM 출신이라면 머릿속에 곧장 세 가지 그림이 떠오른다. *CompletableFuture* 체인, *Spring WebFlux*의 `Mono.zip`, 또는 *Kotlin Coroutine*의 `coroutineScope { ... }`. Java 21을 쓴다면 *Virtual Thread*에 그냥 블로킹 호출 열 개를 던져도 된다. 이 네 모델 사이를 오가본 사람일수록 새 도구 앞에서 한 가지 질문을 먼저 던지게 된다. *Rust async는 이 중에서 어디에 가깝고, 어디가 다른가?*

가장 짧은 답을 먼저 적어두자. 사용 감각은 **Kotlin Coroutine과 가장 비슷하다**. `suspend` 키워드 자리에 `async`가 들어가고, `await`가 `.await`로 바뀐다. 콜백이 사라지고 sequential하게 읽힌다. 그런데 한 발만 더 들어가면 차이가 드러난다. 첫째, **runtime을 우리가 직접 골라야 한다.** 둘째, **`Future`는 컴파일러가 만들어주는 상태 머신이라서 모양이 *훨씬 더 명시적*이다.** 셋째, 지금부터 본격적으로 다룰 *function coloring* 문제 — async fn과 sync fn이 *언어 차원에서 분리*되어 있다.

이 챕터의 한 문장을 미리 적어두자. **async는 마법이 아니다 — `Future`는 상태 머신이고, `.await`는 그 상태 머신의 일시 정지점일 뿐이다.** 이 한 문장을 머리에 박은 채로 들어가면, 처음 만나는 `Pin`도, `Send` 경계도, `tokio::spawn`이 까칠하게 구는 이유도 *이미 알던 것의 이름*이 된다.

## Future는 상태 머신이다 — 모델부터 잡고 들어가자

설명을 잠깐 미루고 코드 한 줄을 보자.

```rust
async fn greet(name: &str) -> String {
    format!("hello, {name}")
}
```

이게 사실은 *함수 정의*가 아니다. 컴파일러가 이걸 다음과 비슷한 모양으로 펼친다(엄밀한 코드는 아니고 *모델*이다).

```rust
fn greet(name: &str) -> impl Future<Output = String> {
    GreetFuture { name, state: 0 }
}

struct GreetFuture<'a> {
    name: &'a str,
    state: u8,
}

impl<'a> Future for GreetFuture<'a> {
    type Output = String;
    fn poll(self: Pin<&mut Self>, cx: &mut Context) -> Poll<String> {
        // 상태 머신을 한 단계 진행시킨다.
        // .await가 없으니 곧장 Ready를 돌려준다.
        Poll::Ready(format!("hello, {}", self.name))
    }
}
```

`async fn`은 *호출하는 순간 실행되는* 함수가 아니다. *`Future`라는 상태 머신을 만드는* 팩토리에 가깝다. 그 상태 머신을 *어떻게 진행시킬지*는 우리가 정한 runtime이 결정한다. 그래서 `tokio::spawn`이 등장하기 전까지는 우리 코드가 *한 줄도 실행되지 않는다*.

`.await`는 그 상태 머신의 *일시 정지점*이다. 컴파일러는 `.await`가 등장할 때마다 상태 머신에 새 분기를 만든다. 함수 안에 `.await`가 두 개 있으면 상태가 0, 1, 2(완료) 세 가지다. JVM의 `CompletableFuture.thenApply` 체인이 *런타임에 객체로 표현된 그래프*라면, Rust의 async는 *컴파일러가 정적으로 펼친 enum*이다.

이 모델 차이가 실무에서 어떻게 드러나는지 잠시 짚자.

- *컴파일 타임에 펼쳐진다* → 런타임 비용이 거의 없다. heap allocation이 최소화된다. 사례 4의 Cloudflare Pingora가 *CPU 70% 절감*을 본 데에는 이 zero-cost async가 한몫했다.
- *상태 머신이 정적이다* → 그 안에 `&mut` 빌림이 살아 있는 채로 `.await`를 만나면, 컴파일러가 5장의 빌림 규칙 그대로 거부한다. JVM처럼 *런타임에 race를 만들고 발견*하지 않는다.
- *runtime이 분리된다* → 표준 라이브러리는 `Future` trait만 정의한다. *poll을 누가 호출할지*는 우리가 고른다. 자유의 대가다.

이 모델을 한 번 잡아두면, 나머지는 모두 *이 위에 얹는 도구*다.

## #[tokio::main] — 첫 async 코드를 띄워보자

가장 단순한 모양부터 손에 묻혀보자.

```rust
// Cargo.toml
// [dependencies]
// tokio = { version = "1", features = ["full"] }

#[tokio::main]
async fn main() {
    let s = greet("toby").await;
    println!("{s}");
}

async fn greet(name: &str) -> String {
    format!("hello, {name}")
}
```

`#[tokio::main]`이 하는 일은 한 줄로 적을 수 있다. *`main` 함수를 동기 함수로 두되, 그 안에 tokio runtime을 띄우고 우리의 async main을 그 위에서 실행한다*. 이걸 직접 풀어 적으면 이렇다.

```rust
fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        let s = greet("toby").await;
        println!("{s}");
    });
}
```

`block_on`은 *동기 세계와 async 세계의 다리*다. 이 함수가 *지금 스레드를 점유한 채* async 블록이 끝날 때까지 기다린다. 9장에서 만난 `thread::spawn(...).join()`과 정신은 같은데, 여기서는 *runtime 위의 task*가 그 자리를 차지한다.

JVM 출신에게 이 자리는 어디일까? Spring Boot의 `main` 메서드에서 `SpringApplication.run`이 *`ApplicationContext`를 띄우는 일*과 거의 같은 자리다. Spring Boot가 *tomcat이나 reactive netty를* 우리 등 뒤에서 띄워주듯, `#[tokio::main]`이 *tokio runtime*을 등 뒤에서 띄워준다. 다만 *어떤 runtime을 띄울지*가 어노테이션 뒤에 숨어있지 않고 *우리가 직접 골랐다는 사실*이 코드에 박혀 있다.

## tokio::spawn과 JoinHandle — 동시 작업의 첫 모양

이제 동시에 여러 작업을 굴려보자. JVM의 `CompletableFuture.supplyAsync(() -> ...)` 또는 Kotlin의 `async { ... }`의 자리다.

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let h1 = tokio::spawn(async {
        sleep(Duration::from_millis(200)).await;
        "task A 완료"
    });
    let h2 = tokio::spawn(async {
        sleep(Duration::from_millis(100)).await;
        "task B 완료"
    });

    let (a, b) = tokio::join!(h1, h2);
    println!("{}, {}", a.unwrap(), b.unwrap());
}
```

`tokio::spawn`은 task를 *runtime의 스케줄러*에 던진다. 반환값은 `JoinHandle<T>`다. `JoinHandle`이 `Future`를 구현하므로 그대로 `.await`할 수 있고, 여러 개를 모으려면 `tokio::join!` 매크로를 쓰는 편이 편하다. 9장의 `std::thread::spawn(...).join()`과 *시그니처가 거의 같은데*, 차이는 한 가지다 — *수만 개를 띄워도 안 죽는다*.

이게 work-stealing 스케줄러의 보상이다. tokio의 워커는 보통 CPU 코어 수만큼 OS 스레드를 띄우고, 각 워커가 *수천 개의 task*를 자기 local queue에 들고 있다가 *바쁘지 않으면 다른 워커의 queue에서 훔쳐온다*. Go·Erlang의 검증된 패턴이다 — 그래서 *20,768개 crate가 tokio에 의존한다*. 사실상 표준이다.

여기서 함정 하나를 미리 짚어두자. `tokio::spawn`이 받는 future는 *`Send + 'static`*이어야 한다. 9장에서 본 그 두 단어다. 새 task가 어느 워커 스레드에서 돌아갈지 *컴파일 타임에 모르므로* — work-stealing이니까 — Send 제약이 생긴다. 그리고 task가 spawn 함수보다 오래 살 수 있으니 `'static`이 필요하다. 9장에서 `Rc<T>`가 spawn에서 거부됐던 이유가 여기서 *그대로 다시 등장한다*. 컴파일러가 보내는 메시지는 *"`Rc<...>` cannot be sent between threads safely"* — 9장에서 본 그 모양이다.

## select! — 여러 future 중 먼저 끝나는 것

JVM에서 `CompletableFuture.anyOf` 또는 Kotlin coroutine의 `select { ... }`로 풀던 일이다. *외부 API 두 곳에 같은 질문을 던지고 먼저 답하는 쪽을 받는다, 또는 timeout 채널과 데이터 채널을 동시에 기다린다*.

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let a = async {
        sleep(Duration::from_millis(200)).await;
        "느린 응답"
    };
    let b = async {
        sleep(Duration::from_millis(50)).await;
        "빠른 응답"
    };

    tokio::select! {
        result = a => println!("a 먼저: {result}"),
        result = b => println!("b 먼저: {result}"),
    }
}
```

`select!`가 두 future를 동시에 polling하다가 *먼저 ready가 되는 쪽*의 분기를 실행한다. 다른 쪽은 *그 자리에서 drop된다* — 즉 cancel된다. JVM의 `CompletableFuture.anyOf`는 다른 future를 *명시적으로 cancel하지 않으면 그대로 굴러간다*는 점에서 다르다. Rust의 `select!`는 cancellation이 *기본*이다. 이 차이가 *connection 누수* 같은 함정을 줄여준다 — *물론 select 분기 안에 락을 잡고 있었다면 그 락이 풀리는지를 우리가 봐야 한다*.

## tokio::sync — 채널과 동기화 기본 도구

9장에서 `std::sync::mpsc`를 봤다. 이름이 같고 의도도 같지만, async 세계에서는 *그 도구를 쓰면 안 된다*. blocking이기 때문이다 — 한 task가 std mpsc의 `recv()`에서 블록되면 그 task가 점유한 워커 스레드 전체가 멈춰버린다. 다른 수천 개 task가 *그 한 줄 때문에* 굳는다.

처방은 `tokio::sync::*`다.

```rust
use tokio::sync::{mpsc, oneshot, broadcast, watch};

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel::<String>(32); // bounded.

    tokio::spawn(async move {
        for i in 0..3 {
            tx.send(format!("작업 {i}")).await.unwrap();
        }
    });

    while let Some(msg) = rx.recv().await {
        println!("받음: {msg}");
    }
}
```

`mpsc`(다대일), `oneshot`(단일 응답 — request/reply 패턴), `broadcast`(다대다 fan-out), `watch`(가장 최근 값만 읽는 SPSC 옵저버) — 네 가지가 거의 모든 패턴을 커버한다. JVM 출신에게 매핑하면 이렇다.

- `mpsc` ↔ `BlockingQueue` (단, async 친화)
- `oneshot` ↔ `CompletableFuture` 자체 (한 번 보내고 끝)
- `broadcast` ↔ `EventBus`/`SubmissionPublisher`
- `watch` ↔ Kotlin `StateFlow`

채널만이 동기화 도구가 아니다. `tokio::sync::Mutex`도 있다. *9장의 `std::sync::Mutex`와 무엇이 다르냐?* 핵심 한 줄: **`tokio::sync::Mutex::lock()`은 `.await`가 가능하다.** 즉 락을 *기다리는 동안* 다른 task가 같은 워커 스레드에서 진행할 수 있다. 9장의 std Mutex는 OS 스레드를 *그 자리에 멈춰* 세우므로 async에서는 위험하다. 함정 절에서 이 부분을 본격적으로 다시 만난다.

## Mutex와 await — 함정 한 컷

10장에서 가장 유명한 함정이다. 코드를 먼저 보자.

```rust
use std::sync::Mutex;
use std::sync::Arc;

async fn buggy(state: Arc<Mutex<i32>>) {
    let mut guard = state.lock().unwrap();
    *guard += 1;
    do_async_work().await; // 위험!
    *guard += 1;
}

async fn do_async_work() {
    tokio::time::sleep(std::time::Duration::from_millis(10)).await;
}
```

이 코드의 무엇이 문제일까? `do_async_work().await`에서 task가 *일시 정지된다*. 그 사이에 *같은 워커 스레드가 다른 task를 굴린다*. 그런데 우리 task는 `std::sync::MutexGuard`를 들고 있다. 만약 그 다른 task도 같은 mutex를 잡으려 한다면 — 데드락이다. 같은 OS 스레드 위의 두 task가 서로를 기다린다.

clippy가 이 패턴을 경고한다(`await_holding_lock` lint). 그리고 `tokio::sync::Mutex`로 바꾸면 잠재적 위험은 사라지지만, *async Mutex는 일반적으로 더 비싸다*. 모범 답안은 셋 중 하나다.

1. **가드 범위를 좁힌다** — `.await` 전에 가드를 drop한다.
   ```rust
   {
       let mut guard = state.lock().unwrap();
       *guard += 1;
   } // 여기서 guard drop.
   do_async_work().await;
   ```
2. **`tokio::sync::Mutex`로 바꾼다** — `.lock().await`가 되고, `.await` 가로질러 들고 있어도 안전하다.
3. **공유 가변 상태 자체를 줄인다** — 채널로 우회한다. *single-writer + 메시지로 변경 의도 전달*이라는 actor 패턴이 자연스러워진다.

JVM 출신은 이 함정을 처음 만나면 *왜 이런 일이 일어나지?*가 막막할 수 있다. JVM의 락은 *OS 스레드 단위*다. 그래서 *같은 OS 스레드가 같은 락을 두 번 잡으려는 일*이 흔치 않다(reentrant lock이라 가능하긴 하지만 의미가 다르다). Rust async에서는 *한 OS 스레드 위에 수천 개 task*가 얹혀 있다. Mutex가 *task 단위가 아니라 OS 스레드 단위*로 동작한다는 사실 하나가 함정의 뿌리다. 모델을 잡으면 처방은 자연스럽다.

## spawn_blocking — 블로킹 호출은 격리한다

또 하나 흔한 함정이다. async 함수 안에서 *오래 걸리는 동기 작업*을 직접 호출하면 안 된다. 예를 들어 큰 JSON 파싱, 무거운 암호화, 또는 *옛 API 호출*(예: 동기 JDBC, 동기 파일 I/O).

```rust
async fn buggy() {
    let data = std::fs::read("big.txt").unwrap(); // 블로킹!
    process(&data);
}
```

이 한 줄이 워커 스레드를 점유하는 동안 *그 워커에 얹힌 다른 모든 task가 멈춘다*. 처방은 `tokio::task::spawn_blocking`이다.

```rust
async fn fixed() -> std::io::Result<()> {
    let data = tokio::task::spawn_blocking(|| std::fs::read("big.txt"))
        .await
        .unwrap()?;
    process(&data);
    Ok(())
}
```

`spawn_blocking`은 작업을 *별도의 blocking 스레드 풀*로 보낸다. tokio가 기본으로 가지고 있는 풀이 따로 있다. 결과는 `JoinHandle`로 돌아온다. JVM에서 reactive 코드 안에 동기 호출이 끼면 *Schedulers.boundedElastic()*으로 옮기던 일과 거의 같다.

또 하나의 함정. **`block_on`을 async 함수 안에서 호출하지 말 것.** 즉 `#[tokio::main]` 안에서 다시 `Runtime::new().block_on(...)`을 부르거나, async 함수 안에서 `block_in_place`도 없이 `block_on`을 부르면 *런타임 내부에서 panic이 난다*. tokio는 *현재 task가 어디 위에 얹혀 있는지*를 알기에 이런 호출을 명시적으로 거부한다. 동기 코드와 async 코드를 섞을 때는 항상 *경계*를 의식하자 — `block_on`은 *맨 바깥*에서만, `spawn_blocking`은 *안으로* 들어가는 다리다.

## 함수 색깔(Function Coloring) — 코루틴과의 가장 큰 철학 차이

여기까지 따라온 사람이라면 한 가지 질문이 떠올랐을 것이다. *`async fn`이 그저 `Future`를 반환하는 함수라면, 그냥 일반 함수처럼 부르면 안 되나? 왜 호출하는 쪽도 async fn이 되어야 하지?*

이게 바로 **function coloring** 문제다. Bob Nystrom이 2015년에 쓴 글 *"What Color is Your Function?"*에서 처음 통용된 말이다. 핵심은 이렇다 — *언어 차원에서 함수가 두 색깔(빨강 sync / 파랑 async)로 나뉘어 있고, 빨강이 파랑을 호출할 수 없다*는 비대칭. 한 번 async가 되면 *호출 체인 위쪽이 모두 async가 되는* 전염이 일어난다.

Rust는 *명백히 colored 언어*다. `async fn` 안에서만 `.await`를 쓸 수 있고, sync 함수는 async 함수를 *그냥은* 부를 수 없다. `block_on`이라는 다리가 있긴 하지만, 그 다리는 *runtime 위에서 한 번만, 맨 바깥에서만* 안전하다.

비교하자면 Kotlin Coroutine은 *언어 차원에서 두 색깔이고 라이브러리가 다리를 놔준* 구조다. `suspend fun`이 빨강이고 일반 fun이 파랑인데, `runBlocking`/`launch`/`async`로 다리가 잘 놓여 있다. Java 21 Virtual Thread는 *색깔 자체를 없애려는 시도*다 — 모든 함수가 그저 함수고, 블로킹 호출도 lightweight thread 위에서 *그냥 블로킹처럼 보이지만 실제로는 양보한다*. 이 둘 사이의 trade-off가 바로 코루틴/virtual thread/Rust async의 *큰 갈래*다.

Rust의 입장은 정직하다. *function coloring은 비용이지만, 그 대가로 zero-cost와 정적 안전성을 얻는다*. async fn이 만든 상태 머신은 *컴파일 타임에 펼쳐진다*. heap allocation이 최소화되고, 런타임 디스패치가 없다. Send/Sync 마커가 *컴파일러의 거부*로 동시성 안전을 보증한다. Virtual Thread는 그 대가로 *같은 함수가 가벼운 스레드와 무거운 스레드 양쪽에서 동작*하는 dynamic dispatch를 받아들인다 — 안전성과 효율 모두에서 trade-off가 있다.

이 철학 차이를 한 단락으로 정리하자. **Kotlin coroutine은 *runtime이 표준 라이브러리에 묶여 있고* `suspend`가 함수 색깔이 *라이브러리 컨벤션*인 반면, Rust는 *runtime을 프로젝트가 직접 고르고* `async`/`await`가 *컴파일러가 만든 상태 머신*이다.** 그래서 Rust async가 더 명시적이고, 함정의 자리도 다르다. *명시성과 zero-cost가 보상이고, function coloring과 runtime 분열이 대가다*.

비판적 시각도 있다는 사실을 함께 적어두자. *"Async Rust Is A Bad Language"*라는 글이 있고, *"Pin and suffering"* 같은 시리즈가 *Pin·Send 경계·async-trait의 dyn 미지원*을 지적한다. Rust async는 *별도의 sub-language가 됐다*는 신랄한 평이다. 맞는 부분도 있다. 그래서 우리가 *언제 async를 써야 하는가*도 중요하다 — *I/O 멀티플렉싱이 핵심이 아니라면 동기 코드도 충분히 빠르다*. 일이 *수만 개 connection*이 아니라 *수십 개 thread*로 끝나는 영역이라면, std::thread + rayon으로도 충분할 때가 많다. 도구를 *과하게* 쓰지 말자.

## async fn in trait — 1.75 stabilize와 그 후

JVM 출신이 거의 자동으로 짜는 패턴 중 하나가 *인터페이스에 async 메서드를 두는* 것이다. Kotlin에서는 너무도 자연스럽다.

```kotlin
interface UserRepository {
    suspend fun findById(id: Long): User?
}
```

Rust에서 같은 일을 하려면 어떻게 적을까?

```rust
trait UserRepository {
    async fn find_by_id(&self, id: i64) -> Option<User>;
}
```

Rust 1.75(2023-12)에서 *이 문법이 stabilize됐다*. 그 전까지는 `async-trait` crate를 써서 우회해야 했다. 그런데 한 가지 함정이 남아있다. *`dyn UserRepository`로 받으려 하면 컴파일이 안 된다*. dyn-safety가 아직 미해결이기 때문이다. async fn in trait이 반환하는 future의 타입이 *컴파일러가 만들어준 익명 타입*이라 vtable에 못 들어간다.

처방은 두 가지다.

1. **제네릭으로 받는다 (정적 디스패치)** — 서비스 코드에서는 이쪽이 자연스럽다.
   ```rust
   async fn handle<R: UserRepository>(repo: R, id: i64) { ... }
   ```
2. **`async-trait` crate를 쓴다 (동적 디스패치 필요할 때)** — `Box<dyn UserRepository>`가 필요하면 여전히 이 crate가 답이다. 비용은 *반환값이 `Box<dyn Future<...>>`로 할당*된다는 것.
   ```rust
   #[async_trait::async_trait]
   trait UserRepository { ... }
   ```

JVM에서는 *모든 인터페이스 메서드가 dyn-safe(virtual method)*가 디폴트다. Rust에서는 *어디서 동적 디스패치를 받아들일지*를 우리가 골라야 한다. 11장 axum의 핸들러도 이 결정을 곳곳에서 만난다.

## JVM 4종 비교 — 한 페이지 정리

이 자리에서 한 페이지로 묶어두자. 같은 일(*외부 API 10곳을 동시 호출해 합산*)을 다섯 가지 방식으로 짜면 어떻게 다른지 한 줄씩 비교하면 이렇다.

| 모델 | 핵심 도구 | 장점 | 단점 |
|---|---|---|---|
| Spring WebFlux (Reactor) | `Mono`/`Flux`, `zip`, `flatMap` | backpressure, reactive ecosystem | callback chain, 스택 트레이스 난해, 학습 곡선 |
| Kotlin Coroutine | `suspend`, `async/await`, structured concurrency | sequential 스타일, 구조화된 cancellation | runtime이 KotlinX 묶음, JVM에 종속 |
| Java CompletableFuture | `supplyAsync`, `thenApply`, `allOf` | 표준 라이브러리, 익숙함 | 체이닝 위주, cancellation 약함 |
| Java 21 Virtual Thread | 그냥 Thread + 블로킹 호출 | 색깔 없음, 익숙한 패러다임 | 성숙도 진행 중, 일부 native 코드 호환 이슈 |
| Rust async (tokio) | `async fn`, `.await`, `tokio::join!` | zero-cost, 정적 안전성, 가장 빠름 | function coloring, Pin/Send 부담, runtime 분열 |

한 줄 결론: **사용 감각은 Kotlin coroutine과 가장 비슷하고, 비용 모델은 Virtual Thread보다 더 명시적이며, 디버깅 가능성은 WebFlux보다 단순하다.** 우리 손이 어느 모양에 가장 익숙한지가 어디서 출발할지를 알려준다. JVM에서 Coroutine을 깊게 써본 사람이라면 Rust async에서 가장 적게 헤맨다.

## runtime 분열 — tokio가 표준이지만

10장의 마지막 한 절이다. 위에서 잠깐 짚었듯, Rust async는 *runtime이 표준 라이브러리에 없다*. tokio가 사실상 표준이긴 하다 — 20,768개 crate가 의존한다. 그런데 표준이 *하나뿐*이라는 사실이 또 다른 부담을 만든다.

- `async-std`는 2025년 *공식 sunset*됐다. 후속은 `smol`이다.
- `smol`은 "tokio 안에서도 돌아가는 작은 빌딩 블록"으로 부상 중이다. crate 작성자에겐 smol이 더 안전한 default라는 의견도 있다.
- crate를 만들 때 *어떤 runtime에 묶일지*를 결정해야 한다. tokio에 묶이면 다른 runtime에서 못 쓴다("executor coupling").

실무 권고는 단순하다. **애플리케이션 코드는 tokio를 그냥 쓰자.** 90% 이상의 ecosystem이 tokio다. *crate 작성자*가 아니라면 이 결정에 시간을 많이 쓸 필요가 없다. crate 작성자라면 `agnostic`/`pollster` 같은 runtime-agnostic 도구나 smol 기반을 검토하는 편이 낫다.

## 함께 해보자

tokio로 *10개의 외부 HTTP 호출을 동시에 보내고 결과를 모아 합산하는* 작은 함수를 짜보자. `reqwest` crate를 의존성에 추가하고, `tokio::join!` 또는 `futures::future::join_all`로 모아보자.

같은 일을 Java `CompletableFuture`로 짠다면 코드가 어떤 모양일까, Kotlin `coroutineScope { ... async { ... } }`라면 어떤 모양일까를 한 단락씩 머릿속에 비교해보자. *어느 쪽이 더 짧은가, 어느 쪽이 더 명시적인가, 디버깅이 어느 쪽이 쉬울까*.

그다음 함정 한 컷을 의도적으로 짜보자. `await`를 가로지르는 `std::sync::Mutex` 가드를 한 자리 넣고, `cargo clippy`가 무엇을 경고하는지 확인하자. 그 경고를 세 가지 처방(가드 범위 좁히기 / `tokio::sync::Mutex`로 바꾸기 / 채널로 우회하기) 중 둘로 고쳐보고, 비용이 어떻게 다른지 한 단락으로 적어보자. *(이 동시 호출 패턴은 11장 axum 핸들러 안의 외부 API 호출에서 다시 호출되고, Mutex/await 함정은 16장 운영 사고 회고에서 한 번 더 만난다. 그리고 `JoinHandle` 패턴은 12장 sqlx 트랜잭션의 `pool.acquire()`에서 비슷한 모양으로 재등장한다.)*

## 마무리

10장의 한 줄을 다시 박자. **async는 마법이 아니다 — `Future`는 상태 머신이고, `.await`는 그 상태 머신의 일시 정지점일 뿐이다.** 이 한 줄이 머리에 박혀 있으면, `Pin`도 `Send` 경계도 *상태 머신을 다루는 조연*으로 자리잡는다. tokio는 그 상태 머신을 *수만 개* 동시에 굴리는 work-stealing 스케줄러이고, `tokio::sync::*`는 같은 모델 위에서 짜인 채널·동기화 도구다.

Function coloring은 비용이다. 부정하지 말자. *async를 한 번 쓰면 호출 체인이 전염된다*. 대신 zero-cost와 정적 안전성을 얻었다 — 이 trade-off를 우리가 *받아들여야* 한다. Kotlin coroutine과 Java Virtual Thread가 다른 길을 갔다는 사실도 함께 기억하자. *어느 길이 옳은가*는 답이 없는 질문이고, 우리가 *어느 길의 보상을 더 원하는가*가 진짜 질문이다.

다음 11장에서는 *axum*으로 첫 HTTP 서비스를 띄운다. 여기서 본 `tokio::spawn`, `Send + 'static`, `Arc<Mutex<T>>`가 *모두* 그 자리에서 다시 호명된다. 그리고 *DI 컨테이너 없이* Spring Controller가 어떻게 보이는지 — 핸들러는 그저 async 함수일 뿐인데도 — 손에 묻혀보자. *Spring Controller가 Rust로 보이는 순간*이 그 챕터다.

## 참고

- *Why async Rust? — without.boats*. https://without.boats/blog/why-async-rust/
- *Catching up with async Rust — fasterthanlime*. https://fasterthanli.me/articles/catching-up-with-async-rust
- *Surviving Rust async interfaces — fasterthanlime*. https://fasterthanli.me/articles/surviving-rust-async-interfaces
- *Making the Tokio scheduler 10x faster*. https://tokio.rs/blog/2019-10-scheduler
- *async fn and return-position impl Trait in traits — Rust Blog (2023-12)*. https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/
- *Async Rust Is A Bad Language — Bit Bashing*. https://bitbashing.io/async-rust.html
- *Goodbye Async-Std, Welcome Smol — Rust Bytes*. https://weeklyrust.substack.com/p/goodbye-async-std-welcome-smol
- 토픽 5(reference.md §132–163): Send/Sync, async/await, tokio, channel, Mutex.
- 함정 2(reference.md §400–404): JoinHandle 누락, Mutex/await 데드락, blocking 호출.
- 논쟁점 3.2(reference.md §313–319): tokio vs async-std vs smol, function coloring 비판.

---

# 11장. axum으로 첫 HTTP 서비스 — Spring Controller가 Rust로 보이는 순간

10년쯤 Spring으로 컨트롤러를 짜왔다고 해보자. `@RestController`를 클래스에 붙이고, `@GetMapping("/users/{id}")`로 엔드포인트를 매핑하고, `@PathVariable Long id`로 URL 변수를 받고, `@Autowired UserService`로 서비스를 주입받고, 응답으로 `ResponseEntity<User>`나 그저 `User` 한 객체를 던져주면 끝이다. 너무 익숙해서 손이 먼저 움직인다. 그런데 이 전부가 *어떻게* 동작하는지를 솔직하게 적자면 — *Spring이 런타임에 reflection으로 클래스를 스캔하고, 어노테이션을 읽고, proxy를 만들고, DI 컨테이너에서 의존성을 찾아 주입하고, request mapping 트리를 빌드해 라우팅하는* 일련의 일이 *애플리케이션이 뜨는 그 한순간*에 일어난다. 잘못된 시그니처를 적어도 *컴파일은 통과하고*, *애플리케이션이 뜨는 순간까지* 모른다.

axum이 다른 길을 간다. 이번 챕터의 핵심 한 줄은 이렇다. **axum의 핸들러는 그냥 async 함수이고, DI는 *컴파일러가 타입으로 검증한다*.** 그래서 *애플리케이션이 뜨는 순간*이 아니라 *빌드가 도는 순간* 잘못된 핸들러를 잡는다. Spring을 손에 깊게 익힌 사람이 처음 axum을 보면 *너무 단순해서 의심스럽다*. 그 의심을 한 챕터에 걸쳐 풀어보자.

먼저 솔직히 짚을 부분 하나. **axum이 Spring Boot처럼 안 느껴질 수 있다.** DI 컨테이너가 없고, AppState를 직접 들고 다닌다. `@Service` 자동 등록도 없고, `@Transactional` AOP도 없다. *덜 매직이고 더 명시적이다*. 처음에는 *이 정도까지 손으로 적어야 하나*가 답답하지만, 6개월쯤 지나면 *어디서 무엇이 동작하는지가 코드에 다 보인다*는 안도감이 그 자리를 차지한다.

## 프레임워크 지형 — 셋 중 어디에서 출발할까

본격적으로 들어가기 전에 지형 한 장을 보자. Rust 백엔드 프레임워크는 사실상 셋이다.

- **axum** — tokio 팀의 작품. tower 기반. extractor 패턴이 매력적이고 미들웨어가 곧 `Service` trait이라 *cross-framework로 재사용*된다. 가장 활발한 선택지.
- **actix-web** — actor 모델. 가장 오래되고 가장 빠르다(벤치 기준 axum보다 처리량 10~15% 우위). 코드 모양이 *조금 더 무겁다*는 평.
- **loco-rs** — 사실상 *Rust on Rails*다. CLI 스캐폴드, ORM(sea-orm), 백그라운드 잡, 스토리지가 통합. 내부적으로는 axum + sea-orm + sidekiq-rs를 합쳐 놓은 것이다. Spring Boot의 *batteries included* 감각을 가장 가깝게 재현한다.

이 셋 중 무엇부터 손에 잡으면 좋을까? 답은 *axum*이다. 이유 두 가지. 첫째, 생태계가 가장 활발해서 검색이 잘 된다. 둘째, *조립형이라 어디서 무엇이 동작하는지가 가장 잘 보인다* — 입문자가 *모델을 잡기에는* 이게 가장 좋다. loco-rs는 *axum을 손에 익힌 다음* "Spring Boot 같은 생산성이 그리워질 때" 한 번 들여다보면 된다.

## 첫 핸들러 — `Hello, JVM`을 띄워보자

cargo로 새 프로젝트를 하나 만들고 시작하자.

```toml
# Cargo.toml
[dependencies]
axum = "0.7"
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

다음은 가장 단순한 axum 서비스다.

```rust
use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    let app = Router::new().route("/", get(hello));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000")
        .await
        .unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn hello() -> &'static str {
    "Hello, JVM"
}
```

Spring Boot를 처음 시작했을 때 본 `Application.java` + `HelloController.java` 두 파일이 *Rust 한 파일*에 들어가 있다. 자세히 보자.

- `#[tokio::main]` — 10장에서 본 그 어노테이션. tokio runtime을 띄운다.
- `Router::new().route("/", get(hello))` — *어떤 URL에서 어떤 메서드일 때 어떤 함수를 호출할지*를 *코드로* 적어둔다. Spring의 `@GetMapping("/")`이 *어노테이션*이라면 axum은 *함수 호출 체인*이다.
- `async fn hello() -> &'static str` — 핸들러는 그저 async 함수다. 어노테이션도 인터페이스도 없다.

`cargo run`으로 띄우고 `curl http://localhost:3000`을 두드리면 `Hello, JVM`이 돌아온다. Spring Boot보다 *훨씬 빠르게 뜬다* — 100ms 언저리. JVM warmup이 없다. 그리고 이 서비스의 *바이너리 크기*가 release 빌드에서 5MB 안팎이라는 사실은 14장에서 다시 확인하게 된다.

## Extractor 패턴 — `@PathVariable`/`@RequestBody`/`@RequestParam`이 한 모양으로

Spring의 컨트롤러를 짜다 보면 어노테이션이 정말 많다. `@PathVariable`, `@RequestParam`, `@RequestBody`, `@RequestHeader`, `@CookieValue`, `@SessionAttribute`. 어노테이션마다 *어디서* 데이터를 꺼낼지를 일러준다. axum은 이 모든 것을 *extractor*라는 한 패턴으로 통일한다.

```rust
use axum::{
    extract::{Path, Query, State, Json},
    http::HeaderMap,
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

#[derive(Serialize)]
struct User {
    id: i64,
    name: String,
    email: String,
}

#[derive(Deserialize)]
struct ListParams {
    page: Option<u32>,
    limit: Option<u32>,
}

async fn get_user(Path(id): Path<i64>) -> Json<User> {
    Json(User { id, name: "toby".into(), email: "t@x".into() })
}

async fn list_users(Query(params): Query<ListParams>) -> Json<Vec<User>> {
    let _ = (params.page, params.limit);
    Json(vec![])
}

async fn create_user(
    headers: HeaderMap,
    Json(payload): Json<CreateUser>,
) -> Json<User> {
    let _ = headers.get("authorization");
    Json(User { id: 1, name: payload.name, email: payload.email })
}
```

핸들러 시그니처를 한 줄씩 보자.

- `Path(id): Path<i64>` — URL path의 변수를 꺼낸다. Spring `@PathVariable Long id`.
- `Query(params): Query<ListParams>` — 쿼리스트링을 struct로 deserialize. Spring `@RequestParam`을 한 객체로 묶은 셈. 더 깔끔하다.
- `Json(payload): Json<CreateUser>` — body를 JSON으로 deserialize. Spring `@RequestBody`.
- `HeaderMap` — 모든 HTTP 헤더 접근. Spring `@RequestHeader` 묶음.

처음 보면 이상한 부분이 있다. *함수의 매개변수 위치만 다른데 어떻게 이걸 axum이 다 알아듣지?* 답은 trait이다. axum은 `FromRequestParts`/`FromRequest` trait을 구현한 타입이라면 *어떤 것이든* 핸들러 매개변수에 들어갈 수 있게 해놓았다. 그리고 `Path<T>`, `Query<T>`, `Json<T>`, `HeaderMap` 등이 그 trait을 구현해 놓았다.

이 자리에서 한 가지 안도감을 주는 사실 — **잘못된 시그니처는 컴파일이 거부한다**. 예를 들어 `Path(id): Path<i64>`인데 라우터에서 `/users/:user_id`로 등록했다고 해보자. 빌드 자체는 통과하지만(타입은 맞으니까), 라우터의 path placeholder 이름이 안 맞으면 *컴파일러보다 한 단계 위에서* 잡힌다 — 사실 이 부분은 axum 0.7부터는 매우 엄격해져서, 잘못된 placeholder는 라우터 등록 시점에 panic이 난다. *애플리케이션이 뜨는 순간이 아니라 빌드 직후 첫 실행*에서. Spring 진영 사람이 가장 자주 묻는 *"잘못된 시그니처를 컴파일러가 정말 다 잡나?"*에 답하자면 — *대부분 잡지만, 라우터-핸들러 시그니처 매핑은 한 단계 안전망이 추가로 필요하다*. 그래도 *애플리케이션이 뜨는 순간까지 모르는* Spring보다는 한참 앞이다.

## State — DI 컨테이너 없이 의존성을 끼워 넣는 법

이제 Spring 출신이 가장 자주 묻는 질문이다. *`@Autowired`가 없으면 의존성은 어떻게 주입하나?*

axum의 답은 `State<T>`다. *애플리케이션 전체가 공유하는 상태*를 한 타입으로 묶어, 모든 핸들러가 그것을 extractor로 받는다. 이 상태에 DB 풀, 캐시 클라이언트, 외부 API client, 설정값 등을 다 넣는다.

```rust
use axum::{
    extract::State,
    routing::get,
    Router,
};
use std::sync::Arc;
use dashmap::DashMap;

#[derive(Clone)]
struct AppState {
    users: Arc<DashMap<i64, User>>,
    // 나중에 db_pool: PgPool, http: reqwest::Client, ... 추가.
}

#[derive(Clone, serde::Serialize)]
struct User {
    id: i64,
    name: String,
}

async fn get_user(
    State(state): State<AppState>,
    axum::extract::Path(id): axum::extract::Path<i64>,
) -> Result<axum::Json<User>, axum::http::StatusCode> {
    state.users.get(&id)
        .map(|u| axum::Json(u.clone()))
        .ok_or(axum::http::StatusCode::NOT_FOUND)
}

#[tokio::main]
async fn main() {
    let state = AppState {
        users: Arc::new(DashMap::new()),
    };
    state.users.insert(1, User { id: 1, name: "toby".into() });

    let app = Router::new()
        .route("/users/:id", get(get_user))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

자세히 보자. `AppState`는 *그저 struct*다. `Clone`을 derive해야 한다(axum이 필요할 때 복제하므로). 그 안에 `Arc<DashMap<i64, User>>`가 있다 — 9장에서 본 `Arc`의 그 모양이다. *멀티스레드 공유* 의도가 코드에 박혀 있다. `DashMap`은 동시 접근이 가능한 HashMap이다(ConcurrentHashMap의 Rust 대응). 더 복잡한 상태라면 `Arc<Mutex<HashMap<...>>>`이나 `Arc<RwLock<...>>`을 넣는다.

`with_state(state)`로 라우터에 한 번 등록하면, 모든 핸들러가 `State<AppState>`로 그것을 받을 수 있다. 컴파일러가 *타입으로* 검증한다. 잘못된 타입을 받으려 하면 *빌드가 거부한다*. Spring `@Autowired`가 *애플리케이션이 뜨는 순간 빈을 못 찾으면 NoSuchBeanDefinitionException으로 죽었다*면, axum은 *빌드 단계에서 컴파일 에러로 멈춘다*.

여기서 한 가지 호불호가 갈리는 부분이 있다. **`AppState`를 *직접 들고 다닌다*.** Spring은 *`@Service` 클래스를 자동으로 빈으로 등록*하고, 다른 곳에서 *`@Autowired`로 가져다 쓴다*. axum은 *우리가 손으로 struct에 넣고, 손으로 with_state로 등록한다*. 처음에는 *왜 이걸 매번 적어야 하나*가 답답하다. 적응되면 *어떤 의존성이 있는지가 한 자리에 다 보인다*는 안도감이 그 자리를 차지한다 — *AppState struct만 보면 이 서비스의 외부 의존성이 한 줄로 정리된다*.

회사 코드가 커지면 *AppState를 너무 비대하게 만들지 말자*. trait로 추상화하거나, *기능별 sub-state*로 쪼개는 패턴이 자연스럽다. 그 부분은 13장에서 workspace로 도메인을 나눌 때 다시 호명된다.

## tower와 Layer — Filter/Interceptor/AOP가 한 모델로

axum의 진짜 힘은 *미들웨어*에서 드러난다. tower라는 라이브러리의 `Service<Request>` trait이 *비동기 함수(요청→응답)를 일급 시민*으로 만든다. axum, tonic(gRPC), hyper, reqwest가 *모두* 같은 추상화 위에 있어서 미들웨어가 *cross-framework로 재사용*된다.

JVM에서는 같은 의도를 *세 개의 다른 메커니즘*으로 풀어왔다. **Servlet Filter**가 가장 바깥, **Spring HandlerInterceptor**가 그 안, **`@Aspect` AOP**가 그 안에서 메서드 단위로 동작했다. 셋이 *우선순위와 사용처가 미묘하게 다르고*, 한 회사 코드에서 *세 종류가 다 섞여 있는* 일이 흔했다. tower는 이 셋을 *한 모델*로 통일한다.

가장 자주 쓰는 미들웨어 한 줄씩 살펴보자.

```rust
use axum::{Router, routing::get};
use tower_http::{
    trace::TraceLayer,
    cors::CorsLayer,
    timeout::TimeoutLayer,
};
use std::time::Duration;

let app = Router::new()
    .route("/", get(|| async { "ok" }))
    .layer(TraceLayer::new_for_http())          // 모든 요청 로그.
    .layer(CorsLayer::permissive())              // CORS 헤더 자동.
    .layer(TimeoutLayer::new(Duration::from_secs(5))); // 5초 타임아웃.
```

`tower_http` crate에 표준 미들웨어가 다 들어 있다. `TraceLayer`는 Spring Cloud Sleuth + Logback 자리. `CorsLayer`는 Spring `WebMvcConfigurer.addCorsMappings()` 자리. `TimeoutLayer`는 *Spring에서 직접 짜야 했던* 영역.

직접 미들웨어를 쓰고 싶다면 어떻게 할까? `axum::middleware::from_fn`이 가장 쉬운 다리다.

```rust
use axum::{
    extract::Request,
    http::{header, HeaderValue, StatusCode},
    middleware::Next,
    response::Response,
};
use uuid::Uuid;

async fn add_request_id(mut req: Request, next: Next) -> Response {
    let request_id = Uuid::new_v4().to_string();
    req.headers_mut().insert(
        "x-request-id",
        HeaderValue::from_str(&request_id).unwrap(),
    );
    let mut response = next.run(req).await;
    response.headers_mut().insert(
        "x-request-id",
        HeaderValue::from_str(&request_id).unwrap(),
    );
    response
}

async fn require_auth(
    req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let auth = req.headers().get(header::AUTHORIZATION)
        .and_then(|v| v.to_str().ok());
    match auth {
        Some(token) if token.starts_with("Bearer ") => Ok(next.run(req).await),
        _ => Err(StatusCode::UNAUTHORIZED),
    }
}
```

위가 모든 요청에 X-Request-Id 헤더를 부여하는 미들웨어, 아래가 인증 미들웨어다. *Spring `OncePerRequestFilter`/`HandlerInterceptor`로 짜던 일과 모양이 거의 똑같다*. 차이는 한 가지 — *컴파일러가 시그니처를 검증한다*. `req`를 `Request`로 받는지, `next.run(req)`을 호출하는지, 반환 타입이 `Response`인지를 다 컴파일러가 본다.

라우터에 끼우는 모양도 단순하다.

```rust
let public_routes = Router::new()
    .route("/", get(|| async { "public" }));

let private_routes = Router::new()
    .route("/me", get(|| async { "private" }))
    .layer(axum::middleware::from_fn(require_auth));

let app = Router::new()
    .merge(public_routes)
    .merge(private_routes)
    .layer(axum::middleware::from_fn(add_request_id));
```

*어떤 라우터에 어떤 미들웨어를 끼울지*가 코드에 *그래프로* 박혀 있다. Spring `WebSecurityConfigurer`가 *어노테이션과 빈 구성*으로 표현하던 일을, axum은 *함수 호출 체인*으로 표현한다. 그래프가 보인다는 사실 자체가 *디버깅의 비용*을 줄여준다.

## 라우터 합성 — `merge`와 `nest`

서비스가 자라면 라우터를 *모듈별로 쪼갤* 필요가 생긴다. axum은 두 가지 합성 도구를 준다.

```rust
fn user_routes() -> Router<AppState> {
    Router::new()
        .route("/", get(list_users).post(create_user))
        .route("/:id", get(get_user))
}

fn order_routes() -> Router<AppState> {
    Router::new()
        .route("/", get(list_orders))
}

let app = Router::new()
    .nest("/api/v1/users", user_routes())
    .nest("/api/v1/orders", order_routes())
    .with_state(state);
```

`nest`는 *prefix를 붙여 라우터를 끼운다*. Spring의 `@RequestMapping("/api/v1/users")`를 컨트롤러 클래스에 붙이는 자리다. `merge`는 *prefix 없이 합치는* 도구. 이 둘이 *복잡한 라우팅 그래프*를 *함수로 합성*한다는 점에서 깔끔하다.

## IntoResponse와 에러 처리 — `Result<T, AppError>`가 HTTP 응답으로

이제 7장에서 만든 `thiserror` 기반 도메인 에러를 *HTTP 응답으로 변환*하는 자리다. 7장의 *함께 해보자*에서 `AuthError` enum을 만들었다. 그것이 *어떻게* HTTP 401/429/500으로 자연스럽게 매핑되는지 손에 묻혀보자.

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde::Serialize;
use std::time::Duration;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("invalid password")]
    InvalidPassword,
    #[error("expired token")]
    ExpiredToken,
    #[error("rate limited (retry after {0:?})")]
    RateLimited(Duration),
    #[error("user not found: {0}")]
    NotFound(i64),
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("internal error")]
    Internal(#[from] anyhow::Error),
}

#[derive(Serialize)]
struct ErrorBody {
    code: &'static str,
    message: String,
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, code) = match &self {
            AppError::InvalidPassword => (StatusCode::UNAUTHORIZED, "invalid_password"),
            AppError::ExpiredToken => (StatusCode::UNAUTHORIZED, "expired_token"),
            AppError::RateLimited(_) => (StatusCode::TOO_MANY_REQUESTS, "rate_limited"),
            AppError::NotFound(_) => (StatusCode::NOT_FOUND, "not_found"),
            AppError::Database(e) => {
                tracing::error!(error = ?e, "database error");
                (StatusCode::INTERNAL_SERVER_ERROR, "database_error")
            }
            AppError::Internal(e) => {
                tracing::error!(error = ?e, "internal error");
                (StatusCode::INTERNAL_SERVER_ERROR, "internal")
            }
        };
        (status, Json(ErrorBody {
            code,
            message: self.to_string(),
        })).into_response()
    }
}
```

이 코드의 핵심은 한 줄이다. **`AppError`가 `IntoResponse`를 구현하는 순간, 모든 핸들러가 `Result<T, AppError>`를 그저 반환할 수 있다.** 그러면 `?` 연산자로 에러 전파가 자동이 된다.

```rust
async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as!(
        User,
        "SELECT id, name FROM users WHERE id = $1",
        id
    )
    .fetch_optional(&state.db)
    .await?  // sqlx::Error → AppError::Database 자동 변환.
    .ok_or(AppError::NotFound(id))?;

    Ok(Json(user))
}
```

`?` 연산자가 7장에서 본 `From` trait의 자동 변환을 활용한다. `#[from]` 속성이 `From<sqlx::Error> for AppError`를 자동으로 만들어주기 때문에, `await?` 한 줄이 *실패 시 즉시 early return*하면서 에러 타입 변환까지 처리한다. Spring `@RestControllerAdvice`로 *예외를 한 자리에 모아 처리*하던 패턴이 *타입 시스템 안에 박혀* 있다.

JVM 출신은 이 자리에서 비교 한 단락을 머리에 꼭 새겨두자. **Spring의 `@RestControllerAdvice`/`@ExceptionHandler`는 *런타임 디스패치*다.** AOP proxy가 던져진 예외를 잡아서 매핑한다. 잘못 매핑된 예외는 *런타임에 발견*된다. axum의 `IntoResponse` 패턴은 *컴파일 타임 매핑*이다 — 핸들러의 반환 타입이 `Result<T, AppError>`로 정해지면 *그 타입의 에러만* 반환할 수 있고, 그 타입의 모든 분기가 *컴파일러가 강제하는 exhaustive match*로 처리된다. *exception 누락*이 *컴파일 단계에서* 잡힌다.

## 통합 — 작은 in-memory 서비스 한 채

지금까지 본 모든 조각을 한 화면에 모아보자. *작은 user CRUD를 in-memory로 띄우는* 미니 서비스다.

```rust
use axum::{
    extract::{Path, State},
    http::StatusCode,
    middleware,
    response::{IntoResponse, Response},
    routing::get,
    Json, Router,
};
use dashmap::DashMap;
use serde::{Deserialize, Serialize};
use std::sync::{atomic::{AtomicI64, Ordering}, Arc};
use thiserror::Error;
use tower_http::trace::TraceLayer;

#[derive(Clone, Serialize)]
struct User {
    id: i64,
    name: String,
    email: String,
}

#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

#[derive(Clone)]
struct AppState {
    users: Arc<DashMap<i64, User>>,
    next_id: Arc<AtomicI64>,
}

#[derive(Error, Debug)]
enum AppError {
    #[error("user not found: {0}")]
    NotFound(i64),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        match self {
            AppError::NotFound(id) => (
                StatusCode::NOT_FOUND,
                Json(serde_json::json!({"code": "not_found", "id": id})),
            ).into_response(),
        }
    }
}

async fn list_users(State(s): State<AppState>) -> Json<Vec<User>> {
    Json(s.users.iter().map(|e| e.value().clone()).collect())
}

async fn get_user(
    State(s): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<User>, AppError> {
    s.users.get(&id)
        .map(|u| Json(u.clone()))
        .ok_or(AppError::NotFound(id))
}

async fn create_user(
    State(s): State<AppState>,
    Json(body): Json<CreateUser>,
) -> (StatusCode, Json<User>) {
    let id = s.next_id.fetch_add(1, Ordering::SeqCst);
    let user = User { id, name: body.name, email: body.email };
    s.users.insert(id, user.clone());
    (StatusCode::CREATED, Json(user))
}

async fn add_request_id(
    mut req: axum::extract::Request,
    next: middleware::Next,
) -> Response {
    let id = uuid::Uuid::new_v4().to_string();
    req.headers_mut().insert(
        "x-request-id",
        axum::http::HeaderValue::from_str(&id).unwrap(),
    );
    let mut res = next.run(req).await;
    res.headers_mut().insert(
        "x-request-id",
        axum::http::HeaderValue::from_str(&id).unwrap(),
    );
    res
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let state = AppState {
        users: Arc::new(DashMap::new()),
        next_id: Arc::new(AtomicI64::new(1)),
    };

    let app = Router::new()
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user))
        .layer(middleware::from_fn(add_request_id))
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    println!("listening on http://0.0.0.0:3000");
    axum::serve(listener, app).await.unwrap();
}
```

한 화면에 들어가는 분량이다. Spring Boot에서 같은 일을 짜자면 *application.properties + @SpringBootApplication + @RestController + @Service + @Configuration + 빈 등록*이 적어도 5~6 파일. axum은 *한 파일에 한 모듈로 끝난다*. 더 중요한 건 *어디서 무엇이 동작하는지가 한눈에 보인다*는 사실이다. State에 무엇이 들어 있고, 라우터가 어떻게 연결되고, 미들웨어가 어떤 순서로 끼워지는지 — *모두 코드의 한 자리*에서 읽힌다.

`cargo run`으로 띄우고 `curl` 한 줄씩 두드려보자.

```
curl localhost:3000/users
curl -X POST localhost:3000/users -H 'Content-Type: application/json' -d '{"name":"toby","email":"t@x"}'
curl localhost:3000/users/1
```

문제없이 동작한다. 응답에 `x-request-id` 헤더가 자동으로 붙어 있다. 잘못된 ID로 GET하면 404 + JSON body가 돌아온다. *정확히 우리가 적은 대로* 동작한다.

## 성능 한 줄 — 그리고 단서

11장의 마지막에 성능 한 줄을 정직하게 적자. 100 동시 연결 / JSON+PostgreSQL 시나리오에서 Spring Boot(JVM)는 4,200 req/s, P99 45ms, 280MB. axum + tokio는 42,000 req/s, P99 3ms, 12MB. **약 10배 처리량, 1/15 latency, 1/23 메모리**라는 보고가 있다.

이 숫자에 흥분하기 전에 *단서*를 함께 적자. 첫째, *매우 단순한 시나리오*다. 비즈니스 로직이 깊어지면 격차는 줄어든다. 둘째, Spring을 *WebFlux*로 옮기면 JVM 측이 더 따라붙는다. 셋째, 메모리 격차는 *배포 환경에 따라 의미가 다르다* — 컨테이너 cost가 비싼 환경에서는 1/23이 *바로 청구서*에 보이지만, 대형 인스턴스에서는 절대값이 더 중요할 수 있다.

그래도 한 줄은 분명하다. **컨테이너 한 대당 메모리 280MB가 12MB로 줄어든다는 사실**은 마이크로서비스 수가 *수십~수백 개*에 이르는 회사라면 인프라 비용 청구서에서 *체감*된다. 그 보상이 우리 회사에 *얼마나 클지*를 *스스로 계산*해보는 것이 11장의 진짜 숙제다.

## 함께 해보자

Spring으로 짜본 적 있는 작은 REST 엔드포인트 하나(예: `GET /users/:id`, `POST /users`)를 axum으로 옮겨보자. 위 통합 예제를 그대로 베껴 시작해도 좋다. 위에서 본 것처럼 in-memory `DashMap`을 State에 두고 시작하면 된다.

여유가 되면 다음 한 줄씩을 추가해 보자.

1. **인증 미들웨어** — `Authorization: Bearer ...` 헤더가 없으면 401. Spring `@PreAuthorize`/Security Filter 자리.
2. **CORS** — `tower_http::cors::CorsLayer`로 한 줄.
3. **요청 trace** — `tracing-subscriber::fmt::init()` + `TraceLayer`. 요청별 로그가 자동.
4. **에러 응답 통일** — 위에서 본 `AppError`/`IntoResponse` 패턴을 도입하고, 핸들러를 `Result<T, AppError>`로 바꾼다.

마지막으로, 같은 일을 Spring Boot로 짤 때 *몇 개의 파일과 어노테이션*이 필요한지를 한 단락으로 비교해보자. *어느 쪽이 더 짧은가*가 아니라 *어느 쪽이 어디서 무엇이 동작하는지 더 잘 보이는가*를 기록해두자. *(이 in-memory 서비스는 12장에서 sqlx + PostgreSQL로 옮겨가 다시 호출되고, 미들웨어 패턴은 14장 운영의 OpenTelemetry trace에서 한 번 더 만난다. 그리고 `IntoResponse` 패턴은 13장 cargo workspace의 *웹 crate*가 *도메인 crate의 에러*를 어떻게 받아들이는지의 모양으로 다시 등장한다.)*

## 마무리

11장의 한 줄을 다시 박자. **axum의 핸들러는 그저 async 함수이고, DI는 컴파일러가 타입으로 검증한다.** 그래서 *애플리케이션이 뜨는 순간이 아니라 빌드가 도는 순간* 잘못된 핸들러를 잡는다. extractor 패턴이 `@PathVariable`/`@RequestBody`/`@RequestHeader`를 한 모양으로 통일했고, `State<T>`가 `@Autowired`의 자리를 *명시적*으로 차지했다. tower의 `Layer`가 Filter/Interceptor/AOP 셋을 한 모델로 합쳤고, `IntoResponse` trait이 `@RestControllerAdvice`의 일을 *타입 시스템 안*에서 한다.

솔직히 한 번 더 짚자. axum은 *Spring Boot처럼 안 느껴질 수 있다*. DI 컨테이너가 없고, AppState를 직접 들고 다니고, *@Service 자동 등록도 @Transactional AOP도 없다*. 그 *덜 매직*이 처음에는 답답하다. 6개월쯤 지나면 *어디서 무엇이 동작하는지가 다 보인다*는 안도감이 그 자리를 채운다 — 그리고 *애플리케이션이 빨리 뜬다, 메모리가 작다, 빌드가 잘못된 코드를 거부한다*는 보상이 따라온다.

다음 12장에서는 *데이터베이스*다. 위의 in-memory `DashMap`을 *PostgreSQL*로 옮길 때, *sqlx의 `query!` 매크로*가 *컴파일 타임에 SQL을 검증*한다는 사실의 충격을 손에 묻혀보자. JPA에서 *런타임에 발견*하던 오류를 *빌드*가 막는다 — 11장의 *빌드가 잘못된 핸들러를 거부한다*는 한 줄이 *DB 영역까지* 자라난 모양이다.

## 참고

- *Announcing Axum — Tokio Blog*. https://tokio.rs/blog/2021-07-announcing-axum
- *axum docs*. https://docs.rs/axum/latest/axum/
- *Unpacking the Tower Abstraction Layer in Axum and Tonic — Leapcell*. https://leapcell.io/blog/unpacking-the-tower-abstraction-layer-in-axum-and-tonic
- *Introduction to the Tower library — Frankel*. https://blog.frankel.ch/introduction-tower/
- *Practical Clean Architecture in Rust — YouTube*. https://www.youtube.com/watch?v=TrNpyFMtnzI
- *Rust, Axum, and Onion Architecture — Medium*. https://medium.com/@jonathan.el.baz/rust-axum-and-onion-architecture-escaping-the-tech-debt-spiral-14df5db946df
- *Spring Boot Webflux vs Rust (Axum) — Medium*. https://medium.com/deno-the-complete-reference/spring-boot-webflux-vs-rust-axum-hello-world-performance-28611da8bfc2
- *Loco.rs*. https://loco.rs/, *What if Rails was Built on Rust?*. https://loco.rs/blog/hello-world/
- *Rust Web Frameworks Compared — DEV.to*. https://dev.to/leapcell/rust-web-frameworks-compared-actix-vs-axum-vs-rocket-4bad
- 토픽 8(reference.md §184–211): axum, actix-web, loco-rs, tower, axum 패턴, 성능 비교.
- 인용(reference.md §444): Spring Boot 4,200 req/s vs Rust+Axum 42,000 req/s.

---

# 12장. 데이터베이스 — sqlx로 컴파일 타임 검증된 SQL을, sea-orm으로 친숙한 ORM을

수요일 새벽 두 시. 운영 알림이 울린다. 결제 API의 어떤 SELECT가 *컬럼 이름이 틀렸다*고 토하면서 죽었다. *어제* 누군가 마이그레이션으로 컬럼 이름을 `created_at`에서 `created_time`으로 바꿨고, JPA Native Query에 박혀 있던 SQL이 *그 사실을 모른 채* 배포됐다. 빌드는 통과했다. 단위 테스트도 통과했다. 그런데 *진짜 운영 부하*를 받자마자 드러났다. 이런 사고를 한 번이라도 겪어본 사람이라면 다음 질문이 자연스럽게 떠오른다. *왜 빌드가 이걸 못 잡지? SQL과 스키마가 어긋난 사실을, 컴파일러는 왜 모르지?*

JVM 진영의 답은 늘 비슷했다. JPA를 쓰면 *대부분*의 SQL이 자동 생성되니 *어느 정도는* 안전하다. 그러나 Native Query, MyBatis XML, JdbcTemplate에 박힌 raw SQL은 *컴파일러의 사각지대*다. QueryDSL이 그 자리를 메우려 했지만 *어차피 Java 코드의 검증*일 뿐, *DB 스키마와의 일치*는 검증하지 못한다. 결국 우리는 *마이그레이션 후 통합 테스트*를 빠짐없이 돌리는 *관행*에 의존해왔다.

Rust 진영의 답이 *충격적이다*. **`sqlx::query!` 매크로는 컴파일 타임에 실제 DB에 접속해 SQL을 검증한다.** 컬럼 이름이 틀리면, 타입이 틀리면, 함수 시그니처가 틀리면 — *빌드가 깨진다*. 12장의 핵심 한 줄이 이 문장이다. *JPA에서 런타임에 발견하던 오류를 빌드가 막는다*는 사실의 무게를, 한 챕터 동안 손에 묻혀보자.

물론 sqlx만 답은 아니다. JPA처럼 모델 중심으로 가고 싶은 사람을 위한 sea-orm, 컴파일 타임 type safety를 가장 강하게 가져가는 diesel — 셋이 *경쟁이 아니라 공존*한다. JPA·MyBatis·QueryDSL이 자바에 공존하듯이.

## 셋 중 어디에서 출발할까 — 출신별 추천

본격 코드로 들어가기 전에 한 표를 보자.

| JVM 출신 | Rust에서의 자연스러운 선택 |
|---|---|
| MyBatis 좋아함 / SQL 직접 쓰는 게 편함 | **sqlx** |
| Spring Data JPA / Hibernate 좋아함 | **sea-orm** |
| QueryDSL을 좋아함 / 강한 type-safety가 우선 | **diesel** |
| ORM과 raw SQL을 자유롭게 섞고 싶음 | sea-orm(아래에 sqlx가 노출됨) |

이 책의 본문은 *sqlx 중심*으로 깔고, sea-orm을 한 절로 손에 묻힌 뒤, diesel은 한 단락으로 위치만 짚어두자. 이유 셋. 첫째, sqlx의 *컴파일 타임 SQL 검증*이 Rust 데이터베이스 영역의 *시그니처 자체*다. 둘째, sea-orm은 *내부적으로 sqlx를 쓰므로* sqlx를 먼저 알면 sea-orm 학습이 자연스럽다. 셋째, 11장에서 띄운 axum 서비스를 PostgreSQL로 옮기는 가장 짧은 길이 sqlx다.

## sqlx — raw SQL + 컴파일 타임 검증

sqlx를 의존성에 한 번 적어보자.

```toml
# Cargo.toml
[dependencies]
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres", "macros", "migrate", "uuid", "chrono"] }
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
```

*기능 플래그*가 길다. 한 줄씩 풀자. `runtime-tokio`(tokio 위에서 동작), `postgres`(드라이버), `macros`(`query!`/`query_as!` 매크로), `migrate`(마이그레이션 도구), `uuid`/`chrono`(데이터 타입 매핑). MySQL이라면 `mysql`, SQLite라면 `sqlite`로 바꾼다.

연결 풀을 띄우고 첫 쿼리를 날려보자.

```rust
use sqlx::postgres::PgPoolOptions;

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    let pool = PgPoolOptions::new()
        .max_connections(10)
        .connect("postgres://app:secret@localhost/mydb")
        .await?;

    let row = sqlx::query!("SELECT 1 as one")
        .fetch_one(&pool)
        .await?;
    println!("결과: {}", row.one.unwrap());
    Ok(())
}
```

여기서 첫 신기한 일이 일어난다. `cargo build`를 돌리면 *컴파일러가 실제로 PostgreSQL에 접속해서* `SELECT 1 as one` 이 SQL이 유효한지를 검증한다. `DATABASE_URL` 환경 변수로 접속 정보를 넘겨야 한다.

```bash
export DATABASE_URL="postgres://app:secret@localhost/mydb"
cargo build
```

DB가 안 떠 있으면 빌드가 실패한다. DB는 떠 있는데 컬럼 이름이 틀리면 빌드가 실패한다. 타입이 안 맞으면 빌드가 실패한다. *런타임이 아니라 빌드*다. 처음 본 사람은 *이게 정말 동작하나?*가 의심스러울 정도다. 동작한다.

## query! 매크로의 진짜 무게

조금 더 진지한 예제를 보자. 사용자 한 명을 ID로 조회하는 함수다.

```rust
use sqlx::PgPool;

#[derive(Debug)]
struct User {
    id: i64,
    name: String,
    email: String,
    created_at: chrono::DateTime<chrono::Utc>,
}

async fn find_user(pool: &PgPool, id: i64) -> Result<Option<User>, sqlx::Error> {
    let row = sqlx::query!(
        r#"
        SELECT id, name, email, created_at
        FROM users
        WHERE id = $1
        "#,
        id
    )
    .fetch_optional(pool)
    .await?;

    Ok(row.map(|r| User {
        id: r.id,
        name: r.name,
        email: r.email,
        created_at: r.created_at,
    }))
}
```

이 코드가 컴파일되면서 sqlx가 검증하는 것을 한 줄씩 보자.

1. **SQL 문법** — `SELECT ... FROM ... WHERE ...`가 PostgreSQL이 받아들이는 모양인지.
2. **테이블 존재 여부** — `users` 테이블이 진짜 있는지.
3. **컬럼 존재 여부** — `id`, `name`, `email`, `created_at`이 진짜 있는지.
4. **컬럼 타입** — `id`가 `BIGINT`라서 Rust 측에서 `i64`로 받는 게 맞는지.
5. **placeholder 바인딩** — `$1`에 `i64`를 넘기는 게 맞는지.
6. **결과 row의 nullable 여부** — `name`이 NOT NULL이면 `String`, NULL 가능이면 `Option<String>`.

여섯 가지 *전부* 빌드 단계에서 잡힌다. JPA Native Query에서 *런타임 부하 받기 전까지 모르던* 오류가 *git push 직전*에 잡힌다는 뜻이다.

조금 더 편하게 적으려면 `query_as!`를 쓰는 편이 낫다. 결과를 *바로 struct로 받는* 매크로다.

```rust
async fn find_user(pool: &PgPool, id: i64) -> Result<Option<User>, sqlx::Error> {
    sqlx::query_as!(
        User,
        r#"
        SELECT id, name, email, created_at as "created_at!"
        FROM users
        WHERE id = $1
        "#,
        id
    )
    .fetch_optional(pool)
    .await
}
```

`User` struct의 필드와 SELECT 컬럼이 *이름과 타입 모두* 맞아야 한다. 어느 한쪽이 틀리면 *빌드*가 거부한다. `as "created_at!"`의 느낌표는 *이 컬럼은 NOT NULL이라고 확신한다*는 sqlx 문법이다(view나 outer join 결과를 다룰 때 유용).

여기서 한 단락 정직하게 적자. **이 마법이 공짜는 아니다.** 첫째, *빌드 시간이 길어진다* — 매 빌드에서 SQL 검증을 위해 DB에 쿼리를 보내야 하기 때문이다. 큰 프로젝트에서는 체감된다. 둘째, *CI에서 DB가 필요하다* — 빌드 자체가 DB 연결을 요구하므로. 이 두 부담을 풀어주는 도구가 다음 절의 *offline 모드*다.

## offline 모드 — CI에서 DB 없이 빌드하기

sqlx가 처음부터 갖춘 도구다. `cargo sqlx prepare` 명령으로 *모든 매크로를 미리 컴파일해 메타데이터를 디스크에 저장*하고, 그것을 git에 커밋하면 *CI는 메타데이터만 읽어 검증*한다.

```bash
# 로컬에서 한 번:
cargo install sqlx-cli --no-default-features --features postgres
export DATABASE_URL="postgres://app:secret@localhost/mydb"
cargo sqlx prepare

# 그러면 .sqlx/ 디렉터리에 query-*.json 파일들이 생성됨.
git add .sqlx
git commit -m "sqlx prepare: schema sync"
```

CI 환경 변수로 `SQLX_OFFLINE=true`를 두면 빌드가 *디스크의 메타데이터만 읽어* 검증한다. DB는 필요 없다.

이 두 단계 워크플로가 처음에는 *번거롭게* 느껴진다. *왜 매번 prepare를 해야 하나?* 답은 *명시적인 게 안전하다*는 Rust 철학에 있다. SQL이 바뀌면 prepare 메타데이터도 바뀌어야 한다. *그 변경이 git diff에 보인다는 사실 자체*가 코드 리뷰의 도구가 된다 — *"이 PR이 어떤 쿼리를 어떻게 바꿨나"*가 한 자리에서 보인다.

팀에 sqlx를 도입할 때 가장 자주 묻는 부분이 이 offline 모드다. CI 파이프라인 한 줄에 `cargo sqlx prepare --check`를 끼워 *prepare 메타데이터가 최신인지를 검증*하는 것이 표준 패턴이다. 그러면 *누가 SQL을 바꾸고 prepare를 빠뜨리면* 빌드가 거부한다.

## 마이그레이션 — sqlx-cli로 Flyway의 자리를

JPA를 쓰면서 Flyway나 Liquibase로 스키마 마이그레이션을 관리하던 경험이 있을 것이다. sqlx도 같은 자리의 도구를 준다.

```bash
sqlx migrate add create_users_table

# migrations/20260503_create_users_table.sql 파일이 생성됨. 그 안에:
# CREATE TABLE users (
#     id BIGSERIAL PRIMARY KEY,
#     name TEXT NOT NULL,
#     email TEXT NOT NULL UNIQUE,
#     created_at TIMESTAMPTZ NOT NULL DEFAULT now()
# );

sqlx migrate run    # 적용.
sqlx migrate revert # 롤백(reversible로 만들어 놨다면).
```

또는 *애플리케이션 시작 시 자동으로 적용*하는 패턴도 있다.

```rust
sqlx::migrate!("./migrations").run(&pool).await?;
```

위 한 줄이 *모든 미적용 마이그레이션을 순서대로 실행*한다. Spring Boot의 `spring.flyway.enabled=true` 자리다. 처음에는 편하지만, 운영에서는 *마이그레이션과 배포를 분리*하는 편이 낫다 — *한 마이그레이션이 큰 락을 잡으면 새 인스턴스가 안 뜬다*. 이 트레이드오프는 Spring Boot도 똑같다.

## 트랜잭션 — `pool.begin()`과 `tx.commit()`

JPA의 `@Transactional`은 *AOP proxy*로 메서드 경계를 가로채 트랜잭션을 관리한다. 너무 자연스러워서 *트랜잭션이 어디서 시작하고 어디서 끝나는지*를 코드에서 보기 어렵다 — 그래서 인터뷰 단골 질문이 됐다(*self-invocation 안 됨*, *체크 예외 vs unchecked 차이*, *propagation 옵션*…). sqlx는 이 자리를 *명시적인 함수 호출*로 두었다.

```rust
async fn transfer(
    pool: &PgPool,
    from_id: i64,
    to_id: i64,
    amount: i64,
) -> Result<(), sqlx::Error> {
    let mut tx = pool.begin().await?;

    sqlx::query!(
        "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
        amount, from_id
    )
    .execute(&mut *tx)
    .await?;

    sqlx::query!(
        "UPDATE accounts SET balance = balance + $1 WHERE id = $2",
        amount, to_id
    )
    .execute(&mut *tx)
    .await?;

    tx.commit().await?;
    Ok(())
}
```

`pool.begin()`이 트랜잭션을 연다. `tx.commit()`이 닫는다. 만약 두 UPDATE 사이에서 `?`로 early return이 일어나면? `tx`가 *drop되면서 자동 rollback*된다. 4장에서 본 `Drop` 트레잇의 RAII가 *트랜잭션*에까지 자라난 모양이다. *try-finally*로 commit/rollback을 챙기던 일이 *타입 시스템의 결과로* 따라온다.

`@Transactional(propagation = REQUIRES_NEW)` 같은 의미는 *함수에 `pool: &PgPool`을 넘기느냐 `tx: &mut Transaction<'_, Postgres>`를 넘기느냐*로 명시적으로 표현된다. 함수 시그니처를 보면 *트랜잭션 안에서 도는지 밖인지*가 한눈에 보인다. 이 *명시성*이 처음에는 번거롭지만, 결제·정산 같은 도메인에서는 *코드만 봐도 의도가 잡힌다*는 안도감을 준다.

JPA의 *함정*들 — 같은 클래스 안 self-invocation에서 `@Transactional`이 안 먹히는 일, lazy loading이 트랜잭션 밖에서 터지는 일, propagation 옵션을 잘못 골라 *상상 못 한 트랜잭션 경계*가 만들어지는 일 — 이 *모양으로 보인다*. 함정이 줄어든다.

## axum 통합 — 11장 in-memory를 PostgreSQL로

이제 11장에서 띄운 axum 서비스의 in-memory `DashMap`을 PostgreSQL로 옮겨보자. 변경 지점이 의외로 적다.

```rust
use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::{IntoResponse, Response},
    routing::get,
    Json, Router,
};
use serde::{Deserialize, Serialize};
use sqlx::PgPool;
use thiserror::Error;

#[derive(Clone, Serialize, sqlx::FromRow)]
struct User {
    id: i64,
    name: String,
    email: String,
}

#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

#[derive(Clone)]
struct AppState {
    db: PgPool,
}

#[derive(Error, Debug)]
enum AppError {
    #[error("user not found: {0}")]
    NotFound(i64),
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, code) = match &self {
            AppError::NotFound(_) => (StatusCode::NOT_FOUND, "not_found"),
            AppError::Database(e) => {
                tracing::error!(error = ?e, "db error");
                (StatusCode::INTERNAL_SERVER_ERROR, "internal")
            }
        };
        (status, Json(serde_json::json!({"code": code, "message": self.to_string()})))
            .into_response()
    }
}

async fn list_users(State(s): State<AppState>) -> Result<Json<Vec<User>>, AppError> {
    let users = sqlx::query_as!(
        User,
        "SELECT id, name, email FROM users ORDER BY id LIMIT 100"
    )
    .fetch_all(&s.db)
    .await?;
    Ok(Json(users))
}

async fn get_user(
    State(s): State<AppState>,
    Path(id): Path<i64>,
) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as!(
        User,
        "SELECT id, name, email FROM users WHERE id = $1",
        id
    )
    .fetch_optional(&s.db)
    .await?
    .ok_or(AppError::NotFound(id))?;
    Ok(Json(user))
}

async fn create_user(
    State(s): State<AppState>,
    Json(body): Json<CreateUser>,
) -> Result<(StatusCode, Json<User>), AppError> {
    let user = sqlx::query_as!(
        User,
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email",
        body.name, body.email
    )
    .fetch_one(&s.db)
    .await?;
    Ok((StatusCode::CREATED, Json(user)))
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let db = sqlx::postgres::PgPoolOptions::new()
        .max_connections(10)
        .connect(&std::env::var("DATABASE_URL")?)
        .await?;

    sqlx::migrate!("./migrations").run(&db).await?;

    let state = AppState { db };

    let app = Router::new()
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    axum::serve(listener, app).await?;
    Ok(())
}
```

11장과 *거의 같은 모양*이다. 달라진 건 다섯 줄.

1. `AppState`의 `users: Arc<DashMap<...>>`이 `db: PgPool`로 바뀌었다.
2. 핸들러가 `DashMap` API 대신 `sqlx::query_as!` 매크로를 쓴다.
3. `AppError::Database(#[from] sqlx::Error)`가 추가됐다 — `?` 연산자가 자동 변환을 처리하므로 핸들러 코드는 깨끗하다.
4. `main`에서 `PgPool`을 만들고 `migrate!`로 마이그레이션을 적용한다.
5. `User` struct에 `sqlx::FromRow`를 derive해 컬럼-필드 매핑을 명시한다(엄밀히는 `query_as!`만 쓰면 derive가 필수는 아니지만, 다른 쿼리 형태와 함께 쓸 때 유용하다).

11장의 in-memory 핸들러와 12장의 PostgreSQL 핸들러를 *나란히 놓고 한 줄씩 비교*해보자. *데이터 소스만 바뀌었는데 비즈니스 코드는 거의 그대로다*. 이게 *State 기반 설계*의 진짜 보상이다.

이 코드가 빌드되려면 PostgreSQL이 띄워져 있고 `users` 테이블이 만들어져 있어야 한다. 그렇지 않으면 `query_as!` 매크로가 컴파일 단계에서 거부한다 — *컬럼이 없다, 타입이 안 맞는다, 테이블이 없다*. 이 사실의 무게를 한 번만 더 적자. **JPA에서는 운영 부하를 받고서야 발견하던 사고가, 빌드 단계에서 잡힌다.**

## sea-orm — Spring Data JPA가 그리워질 때

sqlx의 *raw SQL + 컴파일 타임 검증*이 멋지긴 한데, *모델 중심으로 가고 싶다*는 사람도 있다. 엔티티 클래스 하나 만들어 두면 `find_by_id`/`save`/`delete`가 알아서 굴러가는, JPA의 그 감각. 그 자리에 sea-orm이 있다.

sea-orm은 *async-first*이고 *내부적으로 sqlx 위에 구축*되어 있다. Active Record 패턴을 따른다.

```toml
# Cargo.toml
[dependencies]
sea-orm = { version = "0.12", features = ["sqlx-postgres", "runtime-tokio-rustls", "macros"] }
```

엔티티 정의는 이렇다(보통 `sea-orm-cli generate entity`로 자동 생성).

```rust
use sea_orm::entity::prelude::*;

#[derive(Clone, Debug, PartialEq, DeriveEntityModel)]
#[sea_orm(table_name = "users")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i64,
    pub name: String,
    pub email: String,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}
```

사용은 JPA와 모양이 비슷하다.

```rust
use sea_orm::*;

async fn find_user(db: &DatabaseConnection, id: i64) -> Result<Option<Model>, DbErr> {
    User::find_by_id(id).one(db).await
}

async fn create_user(db: &DatabaseConnection, name: String, email: String) -> Result<Model, DbErr> {
    let user = ActiveModel {
        name: Set(name),
        email: Set(email),
        ..Default::default()
    };
    user.insert(db).await
}

async fn list_users(db: &DatabaseConnection) -> Result<Vec<Model>, DbErr> {
    User::find().limit(100).all(db).await
}
```

JPA Repository를 써본 사람에게는 *놀랍도록 익숙한 모양*이다. `find_by_id`, `find()`, `insert()`, `update()`, `delete()` — 모두 자리에 있다. 마이그레이션은 `sea-orm-cli`가 관리한다.

sqlx와 sea-orm 중 무엇을 고를지는 *우리 팀의 SQL 친밀도*에 달렸다. SQL을 손으로 적는 게 편하면 sqlx, 모델 중심이 편하면 sea-orm. *둘을 한 프로젝트에 섞어 쓸 수도 있다* — sea-orm의 `query.into_raw_sql()`로 빠지거나, sea-orm 위에서 sqlx의 raw query를 직접 부를 수 있다. 11장에서 살짝 언급했던 *loco-rs*는 sea-orm을 기본 채택한 starter라, *Rails 생산성*을 빠르게 잡고 싶으면 그쪽이 좋은 출발점이다.

## diesel — 한 단락

diesel은 *가장 오래되고 가장 type-safe한* 선택이다. 기본은 sync(`diesel_async`로 async 가능). 스키마 자체를 Rust 타입으로 표현해서, `users::table.filter(users::name.eq("toby"))` 같은 query가 *컴파일러에 의해 검증*된다. QueryDSL을 좋아하던 사람에게 가장 자연스럽다.

단점은 *async가 디폴트가 아니라는 점*과 *학습 곡선이 가장 가파르다*는 것. 새 프로젝트라면 sqlx나 sea-orm으로 출발하는 편이 낫고, *최강의 type safety가 우선순위*인 도메인에서만 diesel을 들이는 편이 낫다고 한 줄 적어두자.

## 트랜잭션 한 컷 더 — sea-orm

sqlx의 트랜잭션을 위에서 봤다. sea-orm도 같은 의도를 *비슷한 모양*으로 표현한다.

```rust
use sea_orm::TransactionTrait;

async fn transfer(
    db: &DatabaseConnection,
    from_id: i64,
    to_id: i64,
    amount: i64,
) -> Result<(), DbErr> {
    db.transaction::<_, (), DbErr>(|txn| Box::pin(async move {
        let from = Account::find_by_id(from_id).one(txn).await?
            .ok_or(DbErr::Custom("from not found".into()))?;
        let to = Account::find_by_id(to_id).one(txn).await?
            .ok_or(DbErr::Custom("to not found".into()))?;

        let mut from: ActiveModel = from.into();
        from.balance = Set(from.balance.unwrap() - amount);
        from.update(txn).await?;

        let mut to: ActiveModel = to.into();
        to.balance = Set(to.balance.unwrap() + amount);
        to.update(txn).await?;

        Ok(())
    })).await
}
```

`db.transaction(|txn| ...)`이 클로저 안에서 트랜잭션을 굴리고, *클로저가 Err를 반환하거나 panic이 나면 자동 rollback*한다. JPA `@Transactional` 어노테이션을 함수에 붙이던 일과 의도는 같은데, *경계가 코드에 박혀 있다*. *함수 시그니처에 `txn: &DatabaseTransaction`이 등장하면 그 함수는 트랜잭션 안에서만 도는 함수*다 — 의도가 모양으로 보인다.

## 함정 한 컷 — connection pool과 async, 그리고 long-running query

마지막으로 *실무에서 자주 만나는 함정* 하나만 짚자. sqlx도 sea-orm도 *async pool*이다. `pool.acquire()`로 connection을 빌리는데, 이걸 *오래 들고 있으면* 다른 task가 기다린다. JPA에서 *connection을 한 트랜잭션 동안 점유*하던 패턴을 그대로 옮기면, async 환경에서는 *전체 처리량을 갉아먹는다*.

처방은 두 가지다. 첫째, **트랜잭션을 짧게**. 가능하면 한 트랜잭션이 외부 API 호출을 가로지르지 않게. 둘째, **pool 크기를 신중하게**. PostgreSQL의 max_connections와 잘 맞춰야 한다 — 100개 connection을 띄우려는 앱이 50개로 제한된 DB를 만나면 *connection 고갈로 응답이 멈춘다*. 일반 가이드는 *(코어 수 × 2 + 디스크 수)* 언저리. 의외로 *작은 풀이 더 빠르다*.

세 번째 함정 — *long-running query가 connection을 오래 점유*해서 풀이 굳는 일. PostgreSQL이라면 `statement_timeout`을 connection 옵션으로 박아두는 편이 낫다. 또는 sqlx의 `acquire_timeout`/`idle_timeout` 옵션으로 풀의 health를 챙긴다. 이 함정은 16장 운영 사고 회고에서 한 번 더 만난다.

## 함께 해보자

11장에서 띄운 작은 in-memory CRUD를 PostgreSQL 위로 옮겨보자. 첫 시도는 sqlx로. PostgreSQL을 docker로 한 줄 띄우고(`docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=secret postgres:16`), `sqlx migrate add create_users_table`로 첫 마이그레이션을 만들고, `sqlx migrate run`으로 적용하자. 그다음 위의 통합 예제를 그대로 짜서 띄우고, 11장의 in-memory 버전과 *외부 동작이 똑같다*는 사실을 한 번 손에 묻혀보자.

다음 단계로, 다음 두 가지를 시도해보자.

1. **SQL 한 줄을 일부러 틀리게 적자.** `SELECT id, nme, email`처럼 컬럼 이름을 오타 내고 `cargo build`가 어떤 메시지로 거부하는지 그대로 읽어보자. JPA Native Query였다면 *언제* 발견했을지 한 줄로 적어보자.
2. **같은 도메인을 sea-orm으로 다시 짜자.** `sea-orm-cli generate entity`로 엔티티를 만들고, `Entity::find_by_id`/`Entity::find`/`ActiveModel::insert`로 핸들러를 다시 짠다. sqlx 코드와 sea-orm 코드를 한 줄씩 비교해 *어디가 더 명시적이고 어디가 더 함축적인지* 한 단락으로 정리하자.

그리고 작은 트랜잭션을 한 번 짜보자. `transfer(from, to, amount)` 같은 의도로, 두 UPDATE를 하나의 트랜잭션에 묶고 *중간에 의도적으로 panic을 발생*시켜 *rollback이 동작하는지* 손으로 확인하자. JPA `@Transactional`의 자동 rollback과 *모양이 어떻게 다른지* 한 단락으로 적어두자. *(이 sqlx 기반 CRUD 서비스는 13장에서 도메인/인프라/웹 세 crate로 쪼개져 workspace로 묶이고, 14장에서 musl + distroless 8MB 컨테이너로 빌드되어 다시 호출된다. 그리고 트랜잭션의 `Drop` 자동 rollback 패턴은 16장 운영 사고 회고의 *예외 처리* 영역에서 한 번 더 만난다.)*

## 마무리

12장의 한 줄을 다시 적어두자. **`sqlx::query!` 매크로는 컴파일 타임에 실제 DB에 접속해 SQL을 검증한다.** 컬럼 이름, 타입, nullable 여부, placeholder 바인딩 — 모두 *빌드 단계에서* 잡는다. JPA Native Query에서 *런타임 부하 받고서야 발견*하던 그 사고가, *git push 직전*에 컴파일러의 거부로 멈춘다. 이 사실 하나만으로도 sqlx를 한 번 써볼 가치가 있다.

그리고 *마법은 공짜가 아니다*는 사실도 함께 적어두자. 빌드 시간이 길어진다, CI에 DB(또는 prepare 메타데이터)가 필요하다, prepare 단계가 워크플로에 끼어든다. 이 부담을 *명시적으로 받아들일 때* sqlx의 보상이 따라온다. *명시적인 게 안전하다*는 Rust 철학이 *데이터베이스 영역에까지* 자라난 모양이다.

JPA의 모델 중심이 그리우면 sea-orm이 그 자리에 있다. QueryDSL의 강한 type-safety가 우선이면 diesel이 답이다. 셋이 *경쟁이 아니라 공존*한다는 사실 — JPA·MyBatis·QueryDSL이 자바에 공존하듯이 — 이 Rust 데이터베이스 생태계의 균형 잡힌 그림이다.

11장의 핸들러가 *State 기반 의존성 주입*으로 *컴파일 타임에 잡혔다*. 12장의 핸들러가 *컴파일 타임에 검증된 SQL*로 *데이터 영역까지 잡힌다*. 이 두 안전망이 합쳐지면, *애플리케이션이 뜨는 순간이 아니라 빌드가 도는 순간 잘못된 코드를 거부한다*는 한 문장이 *서비스 한 채*에 *통째로 적용*된다. **이제 Spring으로 짜던 그 서비스가 Rust로 보인다.** Part 3의 마지막 한 줄이 이 자리에서 닫힌다.

다음 13장은 *cargo가 JUnit/JMH/Sonar/picocli/OWASP를 모두 안고 있다*는 사실을 한 챕터로 정리한다. workspace로 도메인을 쪼개고, doctest로 문서를 살아있는 예제로 만들고, criterion으로 처리량을 재고, cargo audit/deny/vet로 의존성을 게이트로 걸고, 첫 매크로를 직접 짜보자. 13장이 닫히면 *이제 실무 시스템 한 채를 Rust로 짤 수 있다*는 자신감이 손에 묻는다. Part 4(출시·폴리글랏·사람)가 그 자신감 위에 얹힌다.

## 참고

- *sqlx repo*. https://github.com/launchbadge/sqlx
- *sqlx::query 매크로*. https://docs.rs/sqlx/latest/sqlx/macro.query.html
- *SQLx Compile Time Verification — DeepWiki*. https://deepwiki.com/launchbadge/sqlx/8.3-offline-mode-(prepare-command)
- *Diesel — diesel.rs*. https://diesel.rs/
- *Compare with Diesel — SeaORM*. https://www.sea-ql.org/SeaORM/docs/internal-design/diesel/
- *SeaORM vs SQLx — Medium*. https://techpreneurr.medium.com/seaorm-vs-sqlx-the-rust-orm-war-ends-with-seaorm-1-0-2026-production-ready-87e219ae6fab
- *Rust ORMs in 2026 — Medium*. https://aarambhdevhub.medium.com/rust-orms-in-2026-diesel-vs-sqlx-vs-seaorm-vs-rusqlite-which-one-should-you-actually-use-706d0fe912f3
- *A Guide to Rust ORMs in 2025 — Shuttle*. https://www.shuttle.dev/blog/2024/01/16/best-orm-rust
- 토픽 9(reference.md §213–243): sqlx, diesel, sea-orm, 마이그레이션.
- 논쟁점 3.3(reference.md §321–327): sqlx vs diesel vs sea-orm 선택 기준.

---

# Part 4. 출시와 그 다음

> *"Rust는 JVM의 대체가 아니라 무기 추가다."*

Part 4는 *기술서를 사람의 책으로 닫는* 자리다. 13장에서 cargo가 JUnit/Mockito/JMH/SpotBugs/Sonar/picocli/OWASP를 *언어 코어 안에서* 어떻게 안고 있는지를 정리하고, 길어진 컴파일 시간 처방, `cargo audit`/`deny`/`vet` 보안 게이트, *내 첫 매크로 만들기*까지 손에 묻힌다. 14장에서 musl + distroless로 *8MB 컨테이너*를 빌드하고, `tracing` + `tracing-opentelemetry`로 *Spring Cloud Sleuth가 하던 일*을 옮긴다. 15장에서 JVM을 *떠나지 않고* Rust를 들이는 다리(JNI / Project Panama / C ABI / 사이드카 패턴)를 깐다 — 8장의 unsafe 절이 본격적으로 회수되는 자리다. 마지막 16장은 *사람과 조직과 커리어*의 자리다. 두 사례("AWS 비용 81% 절감" vs "I Rewrote A Java Microservice In Rust And Lost My Job")의 솔직한 대조, Dropbox Magic Pocket의 그늘, 4~6개월 학습 곡선, 조직 도입의 정치 5가지 권고, 한국 커뮤니티 매듭. 그리고 책의 마지막 한 줄. *"Rust는 JVM의 대체가 아니라 무기 추가다. Spring 다음의 시스템을 손에 쥐자."*

**포함 챕터**

- 13장. 테스트·품질·도구 인프라·CLI — cargo가 IDE·Sonar·JMH·picocli·OWASP를 모두 안고 있다
- 14장. 출시 — 8MB 컨테이너와 OpenTelemetry 관측
- 15장. JVM과 함께 — FFI·JNI·Project Panama·폴리글랏 아키텍처
- 16장. Rust로 가는 길 — 사람·조직·커리어, 그리고 매듭


---

# 13장. 테스트·품질·도구 인프라·CLI — cargo가 IDE·Sonar·JMH·picocli·OWASP를 모두 안고 있다

12장까지 따라온 자네에게 자기 회사 백엔드의 빌드 파이프라인을 한 장에 그려보라고 하면, 아마 대여섯 줄 정도는 우습게 나올 것이다. JUnit과 Mockito가 한 줄, JaCoCo가 한 줄, Spotless 또는 google-java-format이 한 줄, SpotBugs와 Sonar가 한 줄, JMH가 한 줄, OWASP Dependency Check 또는 Snyk가 한 줄, picocli나 Spring Shell이 한 줄. Spring Boot 본체는 그 위에 또 한 층이다. 신규 멤버가 들어오면 *이 도구들이 왜 이 자리에 있는지*를 한 시간씩 설명해야 하고, *플러그인 버전이 안 맞으면* 빌드가 통째로 무너진다. 익숙하지만 솔직히 *번거롭다*. 그리고 가끔은 *피곤하다*.

그렇다면 Rust는 어떨까? cargo 한 도구가 위 목록 거의 전부를 *언어 코어 안에서* 안고 있다. 외부 도구는 보강만 한다. 신규 멤버 onboarding이 *체감으로* 다르다. 이 챕터는 cargo가 어디까지 안고 있는지를 한 줄씩 정리하면서, 길어진 컴파일 시간을 어떻게 다스리는지, 보안 게이트를 CI에 어떻게 박는지, 그리고 *내 첫 매크로*는 어떻게 짜는지까지 손에 묻혀보려 한다. 함께 살펴보자.

## cargo test와 doctest — JUnit이 언어 코어로 들어왔을 때

JUnit은 외부 라이브러리다. JUnit 4와 JUnit 5의 어노테이션이 다르고, Surefire/Failsafe 플러그인 버전이 안 맞으면 통합 테스트가 안 돈다. Rust의 단위 테스트는 *언어 코어*다. 모듈 안에 한 블록이 들어갈 뿐이다.

```rust
pub fn add(a: i64, b: i64) -> i64 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adds_two_numbers() {
        assert_eq!(add(2, 3), 5);
    }
}
```

`cargo test` 한 줄이면 끝난다. `#[cfg(test)]`가 붙은 모듈은 release 빌드에 포함되지 않으므로, *프로덕션 바이너리에 테스트 코드가 섞여 들어가는 일*이 구조적으로 없다. 통합 테스트는 crate 루트의 `tests/` 디렉터리에 별도 파일로 둔다. JUnit이 `src/test/java`로 분리되는 것과 같은 발상이지만, *Maven Surefire 같은 플러그인 없이* 그냥 디렉터리 규약 하나로 끝난다.

여기까지는 JUnit과 도긴개긴이다. doctest로 가면 이야기가 달라진다. JavaDoc에 `@code` 블록을 적으면 *문서로만* 남는다. 거기 적힌 예제가 다음 릴리스에서도 컴파일되는지는 *아무도 보장해주지 않는다*. 그래서 우리는 README의 예제 코드가 깨진 것을 PR 리뷰에서 발견하고 *찜찜한 한숨*을 쉬곤 한다. Rust의 doctest는 그 찜찜함을 단번에 거둬간다.

```rust
/// 두 정수를 더한다.
///
/// # 예시
///
/// ```
/// use mycrate::add;
/// assert_eq!(add(2, 3), 5);
/// ```
pub fn add(a: i64, b: i64) -> i64 {
    a + b
}
```

`cargo test --doc`을 돌리면 주석 안의 ` ```rust ... ``` ` 블록이 *진짜로 컴파일되고 실행된다*. JavaDoc과 JUnit이 한 줄로 합쳐진 셈이다. *문서가 곧 살아있는 예제*가 된다는 표현은 빈말이 아니다. 한 번 익숙해지면, *문서의 예제가 빌드에서 깨지는 경험*이 *문서가 옳다는 증거*로 바뀐다. 이 감각은 손에 묻혀봐야 안다.

## mocking — "mock 없는 mocking"이라는 패턴

Spring 출신은 Mockito 없이 테스트를 짜본 기억이 별로 없을 것이다. `@MockBean`, `when().thenReturn()`, `verify()` — 거의 반사 신경처럼 손이 간다. Rust에도 mocking 라이브러리는 있다. `mockall`이 가장 널리 쓰인다. 트레잇에 `#[automock]`을 붙이면 mock 구현이 자동으로 생성된다.

그런데 Rust 커뮤니티에서 더 자주 권하는 패턴은 *mock이 없는 mocking*이다. 트레잇으로 의존성을 추상화하고, 테스트에서는 더미 구현체를 손으로 한 줄 끼워 넣는다.

```rust
trait Clock {
    fn now(&self) -> u64;
}

struct SystemClock;
impl Clock for SystemClock {
    fn now(&self) -> u64 { /* ... */ 0 }
}

struct FakeClock(u64);
impl Clock for FakeClock {
    fn now(&self) -> u64 { self.0 }
}
```

생각해보자. Mockito가 강력한 이유는 자바의 *모든 것이 객체*라는 전제와 *모든 메서드가 사실상 virtual*이라는 모델 위에서 *런타임에 동적 프록시*를 생성할 수 있기 때문이다. 그 강력함 뒤에 *프록시가 self-invocation을 못 잡는*다거나 *final 메서드를 mock 못 한다*는 함정이 따라붙는 것은 익숙한 이야기다. Rust는 다른 길을 골랐다. *의존성을 명시적으로 주입*하는 코드가 자연스러우니, *mock도 명시적인 한 줄*로 충분해진다는 발상이다. 처음에는 *번거롭게* 느껴지지만, 한 달쯤 익숙해지면 *코드가 더 솔직해졌다*는 감각이 든다. 어떤 패턴을 고를지는 팀의 취향이지만, *Mockito 없이도 충분하다*는 사실은 알아두자.

## clippy와 rustfmt — Sonar와 ktlint가 cargo 안에 들어왔을 때

Java 진영에서 코드 품질 도구를 처음 깐 날을 떠올려보자. SonarQube 서버를 세우고, 룰 셋을 고르고, SpotBugs/PMD/Checkstyle 가운데 무엇을 쓸지 합의하고, Maven 빌드에 플러그인을 끼우고, CI에서 결과를 게시할 채널을 정하고, *false positive 한 줄*을 어떻게 무시할지 룰까지 정한다. 한 분기는 잡아먹는다.

clippy는 그 일들을 cargo 한 줄로 끝낸다. `cargo clippy`다. 100개가 넘는 lint가 *correctness, suspicious, style, complexity, perf* 같은 카테고리로 묶여 있다. 입문자가 가장 빨리 *좋은 Rust 코드*로 가는 길은 clippy가 시키는 대로 따라가는 것이다. CI에서는 한 단계 더 강하게, `cargo clippy -- -D warnings`로 *경고를 에러로 승격*시킨다.

```bash
cargo clippy -- -D warnings
```

처음에는 빨간 메시지가 페이지 단위로 쏟아져 *난감하다*고 느낄 수 있다. 하지만 메시지 한 줄 한 줄이 *왜 이게 더 좋은지*를 설명한다. 그리고 거의 모든 메시지에 *수정 코드 예시*가 따라붙는다. 컴파일러가 스승이 되는 감각은 4장에서 borrow checker와 만났을 때 이미 한 번 겪었다. clippy는 그 스승의 *코드 리뷰 모드*다. 적이 아니라 동료(co-author)다.

rustfmt는 더 단순하다. ktlint와 google-java-format을 한 줄로 합친 것이다. `cargo fmt`. 끝이다. 팀에서 합의해야 할 것은 `rustfmt.toml`의 몇 줄이 전부다. 들여쓰기가 탭이냐 공백이냐로 한 시간 회의하던 시절이 *조금 멀어진다*.

## criterion — JMH가 cargo 한 도구 안에서 굴러간다

JMH(Java Microbenchmark Harness)를 한 번이라도 진지하게 써본 적이 있다면, *마이크로벤치는 정직하게 어렵다*는 사실을 알 것이다. JIT warmup, dead code elimination, false sharing, GC 잡음 — 한두 가지만 놓쳐도 *말도 안 되는 숫자*가 나온다. 그래서 JMH는 fork·warmup·measurement iteration·blackhole 같은 수단을 정성껏 쥐여준다.

Rust 생태계의 표준은 criterion이다. JMH의 정신을 거의 그대로 가져왔다.

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn fib(n: u64) -> u64 {
    if n < 2 { n } else { fib(n - 1) + fib(n - 2) }
}

fn bench_fib(c: &mut Criterion) {
    c.bench_function("fib 20", |b| {
        b.iter(|| fib(black_box(20)))
    });
}

criterion_group!(benches, bench_fib);
criterion_main!(benches);
```

`cargo bench`로 돌리면 통계적으로 안정된 수치가 나오고, `target/criterion/` 아래에 *HTML 리포트*가 떨어진다. throughput, outlier 분석, 이전 측정과의 비교 그래프까지 그려준다. JMH 보고서를 별도 도구로 시각화하던 *번거로움*이 한 단계 줄어든다. JIT가 없는 Rust에서는 워밍업의 의미가 다르지만, *측정값을 신뢰하려면 통계가 필요하다*는 원리는 똑같다. 측정 없이 "이게 더 빠를 것이다"라고 말하는 습관이 줄어드는 것 — 그것이 criterion이 팀에 가져다주는 가장 큰 선물이다.

## cargo workspace — Gradle multi-module의 깔끔한 형제

12장의 axum + sqlx 서비스를 그대로 한 crate에 두고 굴리는 데는 한계가 빨리 온다. 도메인 로직, 인프라 어댑터(DB·외부 API), 웹 핸들러를 *같은 crate*에 두면 *컴파일 시간*과 *모듈 경계*가 동시에 무너진다. workspace로 쪼개야 할 시점이다. Gradle multi-module을 한 번이라도 써봤다면, 발상은 익숙하다.

```toml
# Cargo.toml (워크스페이스 루트)
[workspace]
resolver = "2"
members = [
    "crates/domain",
    "crates/infra",
    "crates/web",
]

[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
sqlx  = { version = "0.8", features = ["postgres", "macros", "runtime-tokio"] }
```

각 멤버 crate의 `Cargo.toml`에서는 `tokio = { workspace = true }`처럼 한 줄로 가져다 쓴다. 버전 관리가 한 곳으로 모이는 감각은 Gradle의 `versions.toml`이나 BOM(Bill of Materials)과 결이 같다. *결정적 차이*가 한 가지 있다. Rust는 *멤버 crate들이 같은 의존성의 다른 feature*를 요구하면, 빌드 그래프 안에서 *하나의 컴파일 단위로 통합*해버린다. 이른바 *feature unification*이다. 한 crate에서 reqwest의 `rustls-tls` feature를 켜고, 다른 crate에서 `native-tls` feature를 켜면, 두 feature가 *모두 활성화*된 상태로 빌드된다. 의도치 않게 OpenSSL을 끌어들이는 사고로 이어지기도 한다. 그래서 워크스페이스를 만들 때 `resolver = "2"`를 명시하는 것이 *디폴트*다. 잊지 말자.

도메인 crate에 doctest를 한두 개 박아두면 *살아있는 명세*가 된다. 인프라 crate는 *외부 시스템 어댑터*만 두어 mock과 fake가 들어갈 자리를 비워두자. 웹 crate는 axum의 라우터·핸들러·State에 집중하고, 비즈니스 로직은 도메인 crate에 위임한다. *얼마나 얇게 쪼개야 적당한가?* 정답은 없지만, *서로 다른 사람이 다른 PR로 만질 자리*가 보이면 그 자리가 경계다.

## 컴파일 시간 — 27%가 가장 큰 불만으로 꼽은 영역

Rust로 한 달쯤 일해보면 누구나 한 번은 마주치는 한 줄 호소가 있다. *"5초 짜리 변경에 1분이 걸린다."* 2025 Rust Compiler Performance Survey에서 27%가 *가장 큰 불만*으로 컴파일 시간을 꼽았다. 솔직히 인정하자. Rust 컴파일러는 *많은 일을 한다*. borrow checker, monomorphization, LLVM 최적화 — 그래서 컴파일 시간이 길어지는 것은 *공짜로 받은 안전성*의 뒷면이다. 그래도 손쓸 수 있는 길은 여럿 있다. 처방을 단계별로 정리해보자.

첫째, **`cargo check`를 먼저 쓴다.** 코드 변경 직후 *진짜로 빌드까지 가야 할 때*는 의외로 적다. 타입 검사만 통과해도 80%의 안심은 얻는다. `cargo check`는 LLVM 최적화·코드 생성을 건너뛰므로 `cargo build`보다 한참 빠르다. IDE의 rust-analyzer가 사실상 백그라운드에서 같은 일을 한다.

둘째, **워크스페이스를 쪼갠다.** 한 crate가 너무 비대해지면, 한 줄 변경에 그 crate 전체의 의존 그래프가 다시 빌드된다. 도메인·인프라·웹으로 쪼개면 자주 만지는 자리만 다시 빌드된다. 모듈 경계가 *컴파일 단위로* 그대로 보상받는다.

셋째, **sccache로 빌드 캐시를 공유한다.** Mozilla가 만든 컴파일러 캐시다. 같은 입력에 대한 컴파일 결과를 *디스크 또는 S3*에 저장하고, CI 머신끼리도 공유할 수 있다. 환경 변수 한 줄로 켠다.

```bash
export RUSTC_WRAPPER=sccache
cargo build --release
```

넷째, **링커를 바꾼다.** macOS는 기본 링커가 빠른 편이지만, Linux의 기본 ld는 큰 바이너리에서 *링크 단계가 빌드 시간의 절반*을 차지하기도 한다. `mold` 또는 `lld`를 끼우면 링크가 *몇 배*로 빨라진다. `~/.cargo/config.toml`에 한 줄을 추가한다.

```toml
[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=mold"]
```

다섯째, **dev 프로파일과 release 프로파일을 분리한다.** 개발 중에는 `codegen-units`를 키워(예: 256) 병렬화하고 LTO를 끈다. 배포 빌드에서만 `codegen-units = 1`, `lto = "thin"`을 켜서 최적화를 최대화한다. 개발 중인 한 시간을 위해 *프로덕션 수준의 최적화*를 매번 돌리는 것은 *낭비*다.

여섯째, **`cargo nextest`를 시도해보자.** cargo 표준 테스트 러너의 대안이다. 프로세스 분리·병렬화·격리가 더 공격적이라 큰 워크스페이스에서는 30~50% 빠르다는 보고가 흔하다.

이쯤에서 마음에 드는 한 가지를 골라 *오늘 당장* 적용해보자. 컴파일 시간 단축은 한 번 익숙해지면 *되돌아갈 수 없는 안락함*이다. 그리고 이 안락함은, 신규 멤버가 *대기 시간 때문에 흐름을 잃는 일*을 막아준다. 팀 차원의 생산성에 곧장 닿는다.

## 보안 도구 — `cargo audit`·`cargo deny`·`cargo vet`

Spring 출신은 OWASP Dependency Check, Snyk, FOSSA의 어딘가에 익숙할 것이다. 라이브러리 버전을 한 번 잘못 잡았다가 CVE가 한꺼번에 뜨면서 *식은땀*을 흘려본 기억도 있을 것이다. Rust는 이 영역도 cargo의 친척 도구로 안고 있다.

`cargo audit`는 RustSec Advisory DB를 조회해 *현재 의존성에 알려진 취약점이 있는지*를 빠르게 검사한다.

```bash
cargo install cargo-audit
cargo audit
```

CI에 한 줄로 끼우면 *취약한 의존성이 들어오는 순간 빌드가 깨진다*. 게시 직전이 아니라 PR 단계에서 잡힌다. OWASP Dependency Check를 처음 도입했을 때의 안도감이 *cargo install* 한 줄로 돌아온다.

`cargo deny`는 한 단계 더 넓다. 라이선스 정책, 출처(crates.io 외 git/path), 중복 의존성, 금지 crate를 한 파일에 선언적으로 적는다.

```toml
# deny.toml
[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause"]
deny  = ["GPL-3.0"]

[bans]
multiple-versions = "warn"
```

조직의 *법무 정책을 코드로 박아두는* 감각이다. 사내 OSS 정책을 매번 PDF로 회람하던 *번거로움*이 줄어든다.

`cargo vet`는 *공급망 감사(supply chain audit)*에 쓴다. *어떤 사람이 어떤 crate의 어떤 버전을 검토했고, 안전하다고 서명했는가*를 워크스페이스에 기록한다. 큰 회사 단위에서 *서로의 감사 결과를 공유*할 수 있도록 설계되어 있다. Mozilla·Google이 자기네 워크스페이스에서 운영하는 vet 결과를 *공개*해 두기 때문에, 우리는 그 위에 *우리 회사 추가본*을 얹는 모양으로 가볍게 시작할 수 있다. 쉽게 말해 *체인지로그가 보안 감사로 진화*한 도구다.

CI 게이트는 보통 이 정도면 충분하다.

```bash
cargo fmt --check && \
cargo clippy -- -D warnings && \
cargo test && \
cargo audit && \
cargo deny check && \
cargo bench --no-run
```

여섯 줄이면 *포맷·정적 분석·테스트·취약점·정책·벤치 컴파일*이 한 번에 잡힌다. JVM 진영의 동등한 파이프라인을 떠올려보자. Maven 플러그인 여섯 개와 그 사이의 *버전 호환표*가 보일 것이다. 16장에서 다시 짚겠지만, *Rust 도입의 최소 조건*이 이 한 줄짜리 게이트다.

## clap — picocli와 Spring Shell이 한 라이브러리에 모이다

2장에서 만든 `hello-jvm` CLI를 기억하는가? `cargo new` 다음 줄에 `clap = { version = "4", features = ["derive"] }`를 끼워넣고 인자 한 개를 받았던 그 작은 프로그램. 이제 그 CLI를 완성형으로 다시 보자.

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "hello-jvm", version, about = "JVM 출신을 위한 첫 CLI")]
struct Cli {
    #[command(subcommand)]
    command: Cmd,
}

#[derive(Subcommand)]
enum Cmd {
    Hello {
        #[arg(short, long, env = "GREET_NAME", default_value = "Toby")]
        name: String,
    },
    Bench { iterations: u64 },
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Cmd::Hello { name } => println!("Hello, {name}!"),
        Cmd::Bench { iterations } => {
            for i in 0..iterations { println!("iter {i}"); }
        }
    }
}
```

picocli를 써본 사람은 *한 줄이 한 줄로 대응*되는 모양이 익숙할 것이다. `#[derive(Parser)]`가 `@Command`고, `#[arg(short, long, env, default_value)]`가 `@Option`이다. subcommand·flag·env 변수·기본값이 한 라이브러리 안에서 깔끔하게 정리된다. cargo·ripgrep·bat·fd·exa의 친숙한 CLI 감각이 모두 clap 위에 있다. 셸 자동완성도 `clap_complete` 한 줄로 생성된다.

Spring Shell을 따로 끼워야 했던 *번거로움*이 사라진다. 작은 운영 도구를 만들 때 *별도 프레임워크를 골라야 하나*를 고민하지 않게 되는 것 — 이 가벼움이 cargo 생태계의 매력이다. 한 번 이 감각에 익숙해지면, *내 다음 사내 도구는 Rust + clap*이 자연스러워진다.

## 내 첫 매크로 — 작성도 할 수 있는 도구라는 사실

8장에서 매크로를 *호출하는* 모양으로 처음 만났다. `println!`, `vec!`, `#[derive(Debug, Clone, Serialize)]`이 매크로다. 그때 약속했던 한 가지가 있었다. *매크로는 작성도 할 수 있는 도구*라는 사실. 13장에서 그 약속을 갚자. 깊이 들어가지는 않는다. *어떻게 시작하는지*만 손에 묻혀보자.

먼저 declarative 매크로다. `macro_rules!`로 정의한다. *부동소수점 비교*에서 자주 필요한 `assert_close!`를 하나 짜보자.

```rust
#[macro_export]
macro_rules! assert_close {
    ($left:expr, $right:expr, $eps:expr $(,)?) => {{
        let l = $left;
        let r = $right;
        let e = $eps;
        if (l - r).abs() > e {
            panic!("assert_close 실패: |{l} - {r}| > {e}");
        }
    }};
}

#[test]
fn pi_is_close_to_three_point_one_four() {
    assert_close!(3.14159_f64, 3.14, 0.01);
}
```

`$left:expr`는 *표현식 한 덩어리*를 받는 fragment specifier다. `expr` 외에도 `ident`(식별자), `ty`(타입), `block`(블록), `pat`(패턴) 등이 있다. *문법 수준의 패턴 매칭*이다. 자바의 어노테이션 프로세서와 가장 큰 차이는, 매크로가 *실제 코드 토큰*으로 펼쳐진 뒤 *컴파일러가 다시 검사*한다는 점이다. 잘못 펼쳐지면 *그 자리에서 컴파일 에러*다. 마법이 적고 디버깅이 솔직하다.

펼쳐진 모양이 궁금하면 `cargo expand`를 쓰자.

```bash
cargo install cargo-expand
cargo expand --test mytest
```

자바 Lombok이 *바이트코드 단계*에서 일을 끝내 *디버깅 시점*에는 잘 안 보이는 데 비해, Rust의 매크로는 *언제든 펼쳐서 사람의 눈으로 읽을 수 있다*. 안심하고 쓸 수 있는 이유다.

다음은 procedural attribute 매크로다. 이쪽은 진짜로 *컴파일러 플러그인*에 가까운 도구다. 깊게 들어가면 한 챕터가 또 필요하니, 여기서는 *모양만* 보자. 별도 crate를 만들고 `proc-macro = true`로 선언한 뒤, `syn`으로 토큰을 파싱하고 `quote`로 코드를 만든다.

```rust
// my_macros/Cargo.toml
// [lib]
// proc-macro = true
//
// [dependencies]
// syn   = { version = "2", features = ["full"] }
// quote = "1"
// proc-macro2 = "1"

use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, ItemFn};

#[proc_macro_attribute]
pub fn my_handler(_attr: TokenStream, item: TokenStream) -> TokenStream {
    let func = parse_macro_input!(item as ItemFn);
    let name = &func.sig.ident;
    let body = &func.block;
    quote! {
        async fn #name() {
            tracing::info!("핸들러 진입: {}", stringify!(#name));
            #body
            tracing::info!("핸들러 종료: {}", stringify!(#name));
        }
    }.into()
}
```

호출하는 쪽은 그냥 `#[my_handler]`를 붙인다. axum 핸들러에 트레이스 로그를 자동으로 박는 식의 일이 가능해진다. Spring AOP의 `@Around`가 했던 일과 결이 비슷하지만, *런타임 프록시*가 아니라 *컴파일 타임 토큰 변환*이다. 그래서 *self-invocation 안 됨* 같은 함정이 없다.

여기까지가 첫 매크로다. 깊이는 다음 학습으로 미루자. 중요한 것은, *매크로가 작성도 할 수 있는 도구*라는 사실을 *손으로 한 번 만져봤다*는 경험이다. 그 경험이 있고 없고가, 다음에 마주칠 *복잡한 derive 매크로의 디버깅*에서 결정적 차이를 만든다.

## cargo 한 도구가 안고 있는 것 — JVM 대응표

여기까지 본 도구들을 한 표로 정리해두자. 책상 옆에 펴 놓고 보는 cheatsheet라고 생각하자.

| 영역 | Rust(cargo 또는 표준 crate) | JVM 대응물 |
|---|---|---|
| 단위 테스트 | `cargo test`, `#[test]` | JUnit 5 |
| 통합 테스트 | `tests/` 디렉터리 | JUnit + Surefire/Failsafe |
| 문서 + 테스트 통합 | doctest (`cargo test --doc`) | JavaDoc + 별도 JUnit |
| Mocking | `mockall`, trait 더미 구현 | Mockito |
| 정적 분석 | `cargo clippy` | SpotBugs + PMD + Sonar |
| 포매터 | `cargo fmt` | ktlint, google-java-format, Spotless |
| 벤치마크 | `cargo bench` + `criterion` | JMH |
| 코드 커버리지 | `cargo tarpaulin`, `cargo llvm-cov` | JaCoCo |
| 멀티모듈 빌드 | cargo workspace | Gradle multi-module, Maven 모듈 |
| 의존성 캐시 | `sccache` | Gradle build cache, Develocity |
| 취약점 스캔 | `cargo audit` | OWASP Dependency Check |
| 라이선스/정책 | `cargo deny` | FOSSA, Snyk Open Source |
| 공급망 감사 | `cargo vet` | (대응물 거의 없음 — Sigstore가 가장 가깝다) |
| CLI 인자 파싱 | `clap` | picocli + Spring Shell |
| 매크로/AOP | `macro_rules!`, proc-macro | Lombok + AspectJ |

JVM 칸의 도구 수를 세보자. 열다섯 줄에 *서로 다른 라이브러리·플러그인 이름이 스무 개 가까이* 들어간다. Rust 칸은 거의 *cargo와 그 형제 도구*다. *결정적 차이* 한 단락은 이렇다. JVM은 *언어 한 개에 도구 수십 개*를 조합하는 ecosystem 모델이고, Rust는 *cargo 한 도구가 핵심을 다 안고* 외부 도구는 *보강만* 한다. 신규 멤버 onboarding 시간이 *체감으로* 다르다는 말이 빈말이 아니다. 이 차이는 회사가 커져 *팀이 늘어날수록* 더 크게 느껴진다.

## 사전 커밋 훅과 CI — 한 줄짜리 게이트

마지막으로 권장 워크플로 한 줄을 적어두자. 회사의 첫 Rust 프로젝트에 *오늘 당장* 끼울 만한 모양이다.

```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit  (또는 cargo-husky / lefthook 등으로 관리)
set -euo pipefail
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

CI 파이프라인은 여기에 보안과 벤치를 더한 한 줄이면 충분하다.

```bash
cargo fmt --check && \
cargo clippy --all-targets -- -D warnings && \
cargo test && \
cargo audit && \
cargo deny check && \
cargo bench --no-run
```

*벤치마크 자체*가 아니라 *컴파일만 검증*하는 `--no-run`이 핵심이다. 진짜 측정은 별도 머신에서 주기적으로 돌리는 편이 낫다. CI에서 매번 벤치를 돌리면 *결과가 흔들려* 의미가 빠르게 닳는다.

이 한 줄짜리 게이트가 자리잡으면, 자네 팀의 신규 멤버는 *첫 PR을 올리는 날* 게이트의 모든 단계를 *자동으로* 통과하게 된다. *코드 리뷰의 절반은 이미 끝나 있는* 셈이다. Rust의 도구 인프라가 주는 가장 큰 선물은 *속도*가 아니라 *합의 비용의 감소*다. 기억해두자.

## 마무리 — 함께 해보자

12장의 axum + sqlx 서비스를 도메인·인프라·웹 세 crate로 쪼개 cargo workspace로 묶어보자. 도메인 crate의 핵심 함수 하나에 doctest를 한 줄 붙여 `cargo test --doc`로 통과시켜 보고, 같은 함수에 criterion 벤치를 붙여 HTML 리포트를 한 번 열어보자. 그 옆에 CI 파이프라인을 한 줄짜리 셸 스크립트로 적어두고, `cargo audit`과 `cargo deny check`를 게이트로 끼워 *고의로 취약한 의존성*을 한 번 추가해 빌드가 깨지는 모습을 손으로 확인하자. 마지막으로 `assert_close!` 매크로를 직접 짜서 도메인 crate의 부동소수점 테스트에서 한 번 써보자. *(이 워크스페이스는 14장에서 musl + distroless로 빌드되어 한 자릿수 MB 컨테이너로 다시 호출되고, `cargo audit` 게이트는 16장에서 *조직 도입의 최소 조건*으로 다시 호출된다.)*

다음 14장에서는 그 워크스페이스를 *진짜로 출시*해보자. 8MB 컨테이너와 OpenTelemetry 관측이 기다리고 있다.

## 참고

- *cargo test*, doctest, criterion, clippy, rustfmt 워크플로 — reference 토픽 7
- 컴파일 시간 함정과 처방 — reference 함정 6, 2025 Rust Compiler Performance Survey
- `cargo audit` / `deny` / `vet` — reference 토픽 7 보강
- `clap` CLI — reference 토픽 10.1
- workspace와 feature unification 함정 — reference 토픽 6

---

# 14장. 출시 — 8MB 컨테이너와 OpenTelemetry 관측

운영 중인 Spring Boot 서비스의 도커 이미지 한 개가 디스크에서 얼마나 차지하는지 떠올려보자. fat jar에 JDK까지 얹은 표준 Layered JAR 이미지는 보통 *200MB에서 400MB*다. Spring Initializr에서 갓 만든 *Hello World* 한 줄짜리 서비스도 비슷한 무게다. JVM과 base 라이브러리, 그리고 표준 의존성이 차지하는 무게는 코드의 양과 거의 관계가 없다. 13장에서 잘 다듬은 axum + sqlx 워크스페이스를 *진짜로 출시*하면 그 이미지가 몇 MB가 될까? 답을 먼저 적자. **8MB 안팎**이다. Spring Boot 이미지의 *25분의 1에서 50분의 1* 사이다.

이 숫자는 자랑하려고 적는 것이 아니다. 이미지가 작아진다는 것은 *Docker pull 시간이 줄고, 콜드 스타트가 빨라지고, 공격 표면이 좁아지고, 배포 단위 비용이 떨어진다*는 의미다. 그리고 이 숫자가 *한 번의 빌드 설정*만으로 손에 쥐어진다면, 그 변화는 운영 팀의 한 분기를 가볍게 만든다. 14장은 그 빌드 설정을 손에 묻혀주려 한다. 그다음에는 *그 안에서 무슨 일이 벌어지는지를 어떻게 들여다보는가* — 관측·프로파일링·컴플라이언스를 한 절씩 풀어보자. JVM 운영 노하우의 90%는 그대로 통한다. 안심하고 따라오자.

## 8MB 컨테이너 — musl과 distroless의 두 줄

먼저 이미지 크기 표를 한 줄 적어두자. 같은 의미의 *작은 HTTP 서비스* 한 개를 다섯 가지 방식으로 빌드한 결과다.

| 빌드 방식 | 이미지 크기(대략) | 한 줄 메모 |
|---|---|---|
| Spring Boot 3 + `eclipse-temurin:21-jre` | 280~360 MB | 가장 흔한 모양 |
| Spring Boot 3 Layered JAR + alpine-jre | 180~220 MB | 최적화 끝판이지만 여전히 무겁다 |
| GraalVM native-image + alpine | 80~120 MB | 빌드 시간이 5~15배 늘고 reflection 함정 |
| Rust + glibc + `debian:slim` | 30~50 MB | 첫 시도가 보통 이 정도 |
| **Rust + musl + `gcr.io/distroless/static`** | **6~10 MB** | 이번 절의 목표 |

마지막 줄이 우리가 만들 모양이다. 두 가지 결정으로 끝난다. *musl libc로 정적 링크*된 바이너리, 그리고 *런타임 OS는 distroless static* 또는 `scratch`. 한 줄씩 보자.

### musl 정적 바이너리

리눅스의 표준 C 라이브러리는 glibc다. 동적 링크가 기본이라 바이너리 옆에 `libc.so.6`이 따라 붙어야 한다. distroless 이미지에 `glibc` 변종을 골라 쓰면 동작은 한다. 그런데 *완전 정적 링크*까지 가려면 musl libc를 쓰는 편이 솔직하다. Rust는 `x86_64-unknown-linux-musl` 타겟을 표준으로 지원한다.

```bash
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl
```

빌드 결과는 `target/x86_64-unknown-linux-musl/release/`에 떨어지고, *어떤 라이브러리에도 동적 링크되지 않은* 바이너리가 한 개 생긴다. `ldd`로 확인해보면 *not a dynamic executable*이라는 한 줄이 나온다. 이 바이너리를 `scratch`에 넣어도 *그냥 돈다*. JVM 출신에게는 이 한 줄이 묘하게 신기하다. *런타임 의존성이 없는 실행 파일*이라는 개념을, JVM에서는 GraalVM native-image에 가서야 만났기 때문이다. Rust는 처음부터 그 모양이 자연스럽다.

OpenSSL 같은 C 라이브러리에 동적 링크된 crate를 쓴다면 musl 빌드가 한 번에 안 된다. 그럴 때는 `rustls`(순수 Rust TLS) 같은 *pure Rust 대체재*를 고르거나, `clux/muslrust` 같은 빌드용 도커 이미지를 쓰면 된다. 처방은 정해져 있다. 처음 musl 빌드가 안 돌면 *어떤 의존성이 C에 묶여 있는지*를 먼저 보자. 90%는 TLS·압축·암호화 라이브러리다.

### multi-stage Dockerfile

이제 표준 패턴을 적자. *빌더 stage*에서 musl 빌드를 돌리고, *런타임 stage*에는 distroless 또는 scratch에 바이너리만 복사한다.

```dockerfile
# syntax=docker/dockerfile:1.7

# 1) builder
FROM rust:1.83-alpine AS builder
RUN apk add --no-cache musl-dev pkgconfig openssl-dev
WORKDIR /app
COPY . .
RUN cargo build --release --target x86_64-unknown-linux-musl

# 2) runtime — 8MB짜리 결과물
FROM gcr.io/distroless/static-debian12
COPY --from=builder \
    /app/target/x86_64-unknown-linux-musl/release/myservice /app/myservice
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/app/myservice"]
```

13장에서 만들어둔 워크스페이스를 그대로 이 Dockerfile에 태우면 8MB 안팎 이미지가 떨어진다. `docker build` 한 줄로 끝난다. *Spring Boot의 `mvn spring-boot:build-image`*가 했던 일을 한 단계 더 깊은 곳에서 끝낸 셈이다. 안심하고 운영에 올려보자.

distroless static 이미지에는 *셸도, 패키지 매니저도, 심지어 libc도* 없다. *공격 표면이 거의 0에 가깝다*. nonroot로 떨어뜨리는 한 줄까지 박아두면 컨테이너 안에서 권한 상승 사고가 거의 사라진다. 이 영역은 ONCD/NSA의 메모리 안전 권고와 이어진다 — 잠시 뒤 컴플라이언스 절에서 회수하자.

### release 프로파일 튜닝

이미지 크기를 더 줄이고 싶다면, `Cargo.toml`의 `[profile.release]`에 한 단락을 더 박는다.

```toml
[profile.release]
opt-level = 3
lto = "thin"          # link-time optimization
codegen-units = 1     # 최적화 폭 최대 (빌드 시간↑)
strip = true          # 디버그 심볼 제거
panic = "abort"       # panic 시 unwinding 안 함
```

`strip = true`만으로도 보통 30~40% 줄어든다. `lto = "thin"`은 inline 한계를 모듈 경계 너머로 넓혀 *런타임 성능*도 올린다. `panic = "abort"`는 panic이 났을 때 *스택 unwinding 정보*를 빼서 바이너리를 줄인다. 단, FFI 경계에서 panic이 새지 않도록 처리하는 책임이 늘어난다. 15장 FFI에서 다시 짚자.

이 네 줄로 *4~5MB짜리* 바이너리가 떨어지는 일도 흔하다. 다만 *codegen-units = 1*은 빌드 시간을 두 배 가까이 늘린다. 13장의 처방대로 *dev 프로파일*은 그대로 두고 *release 프로파일*에만 적용하는 편이 낫다. 빌드 시간과 바이너리 크기 사이의 trade-off는 자기 팀의 배포 주기에 맞게 골라잡자.

## 관측 표준 스택 — `tracing` + OpenTelemetry

이미지가 작아진 만큼 *그 안에서 무슨 일이 벌어지는지*가 더 중요해진다. JVM 진영에서 우리는 보통 Spring Cloud Sleuth + OpenTelemetry Java agent + Micrometer + Logback의 어딘가에 앉아 있다. *agent 한 줄*로 자동 계측이 들어와서 편하지만, *내부에서 무슨 일이 일어나는지*는 살짝 안갯속이다. Rust는 그 자리를 명시적으로 풀어둔다. `tracing` crate가 출발점이다.

```rust
use tracing::{info, instrument};

#[instrument(skip(pool))]
async fn get_user(pool: &PgPool, id: i64) -> Result<User, AppError> {
    info!(user_id = id, "사용자 조회 시작");
    let user = sqlx::query_as!(User, "SELECT id, name FROM users WHERE id = $1", id)
        .fetch_one(pool)
        .await?;
    info!(name = %user.name, "사용자 조회 완료");
    Ok(user)
}
```

`#[instrument]` 한 줄이면 함수 진입과 종료에 *span*이 자동으로 만들어진다. `skip(pool)`로 큰 인자를 로그에서 제외할 수 있다. `info!` 매크로는 *구조화된 필드*를 키-값으로 받는다. `%user.name`은 Display로, `?value`는 Debug로 직렬화된다. JSON 로그·트레이스 모두 같은 한 줄에서 출발한다.

런타임에서 어떤 subscriber로 흘려보낼지는 main에서 한 번만 정한다. *콘솔 JSON 로그*와 *OTLP 트레이스*를 동시에 보내는 모양은 보통 이렇다.

```rust
use opentelemetry_otlp::WithExportConfig;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // 1) OTLP exporter — Jaeger / Tempo / Datadog
    let tracer = opentelemetry_otlp::new_pipeline()
        .tracing()
        .with_exporter(
            opentelemetry_otlp::new_exporter()
                .tonic()
                .with_endpoint("http://otel-collector:4317"),
        )
        .install_batch(opentelemetry_sdk::runtime::Tokio)?;

    // 2) tracing → console JSON + OTLP
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::from_default_env())
        .with(tracing_subscriber::fmt::layer().json())
        .with(tracing_opentelemetry::layer().with_tracer(tracer))
        .init();

    // 3) axum 서비스 기동
    // ...
    Ok(())
}
```

여기까지 셋업하고 핸들러에 `#[instrument]`만 붙이면, OpenTelemetry Collector → Jaeger/Tempo/Datadog 어디로 보내든 *span tree가 그대로 보인다*. Spring Cloud Sleuth + OpenTelemetry Java SDK 조합과 *거의 같은 모델*이다. *결정적 차이*는 한 단락이다. JVM agent는 *바이트코드 instrumentation*으로 일을 끝낸다 — 자동이라 편하지만, *내가 무엇을 계측하고 있는지가 살짝 안 보인다*. Rust의 `#[instrument]`는 *코드에 박힌다* — 한 줄을 더 적어야 하지만, *무엇이 어디서 측정되는지가 코드 안에 그대로 보인다*. 어느 쪽이 더 좋은가? 정답은 없다. 다만 SRE 팀의 *디버깅 동선*을 떠올려보자. 코드에서 출발하는 사람에게는 후자가 더 솔직하게 느껴진다.

### 메트릭 — `metrics` crate

span만으로는 부족할 때가 있다. *p99 latency, 처리량, 에러율* 같은 게이지·카운터·히스토그램이다. Java의 Micrometer에 해당하는 자리는 `metrics` crate다.

```rust
use metrics::{counter, histogram};

async fn handler() -> impl IntoResponse {
    let start = std::time::Instant::now();
    counter!("http_requests_total", "route" => "/users").increment(1);

    let result = do_work().await;

    histogram!("http_request_duration_seconds", "route" => "/users")
        .record(start.elapsed().as_secs_f64());
    result
}
```

`metrics-exporter-prometheus`로 Prometheus가 긁어갈 `/metrics` 엔드포인트를 한 줄로 띄운다. Micrometer의 `Counter`/`Timer`/`Gauge`가 *거의 같은 이름*으로 옮겨와 있다. JVM 출신이 가장 평탄하게 건너오는 영역이다.

### panic hook과 Sentry

운영 사고는 보통 *예상하지 못한 panic*에서 시작된다. JVM의 `Thread.UncaughtExceptionHandler`에 해당하는 것이 Rust의 `std::panic::set_hook`이다. Sentry 연동은 `sentry` crate 한 줄이면 끝난다.

```rust
let _guard = sentry::init((
    "https://example@sentry.io/0",
    sentry::ClientOptions {
        release: sentry::release_name!(),
        traces_sample_rate: 0.1,
        ..Default::default()
    },
));
```

`tracing-sentry` layer를 끼우면 `tracing`의 ERROR 레벨 이벤트가 Sentry 이슈로 자동 등록된다. JVM의 Sentry SDK가 했던 일과 *체감으로 동일*하다. 사고 자료를 모으는 운영 동선은 그대로다.

## 프로파일링 — flamegraph·tokio-console·samply

JFR과 Async Profiler에 익숙한 자네에게 Rust 측 프로파일링은 가장 편한 영역이다. 도구 이름만 외우면 손이 즉시 따라붙는다.

`cargo flamegraph`는 perf(Linux) 또는 dtrace(macOS) 위에 *flamegraph SVG*를 그려준다.

```bash
cargo install flamegraph
sudo cargo flamegraph --bin myservice -- --port 8080
```

Async Profiler가 만들어주던 그 *오렌지색 그래프*가 그대로 떨어진다. `inferno`라는 별도 도구로 한 단계 깊게 분석할 수도 있다.

`tokio-console`은 *async task* 차원의 인사이트가 필요할 때 쓴다. *어떤 task가 가장 오래 잠들어 있는가, 어떤 task가 spawn된 뒤 부모가 떠나 고아가 됐는가, 어떤 task가 너무 많이 wake되고 있는가* — JVM의 thread dump가 답해주지 못하는 질문에 답한다. JVM의 Virtual Thread 출신이라면 익숙한 발상이다.

```toml
# Cargo.toml
[dependencies]
console-subscriber = "0.4"
```

```rust
console_subscriber::init();
```

위 두 줄을 추가하고 `tokio-console` 클라이언트로 붙으면 실시간 task 그래프가 보인다. *Spring Reactor의 BlockHound*가 했던 검증보다 한 단계 더 깊다.

`samply`는 sampling profiler다. 빌드한 바이너리에 그대로 붙어 *Firefox Profiler 호환 포맷*으로 결과를 떨어뜨린다. JFR 출신이 가장 빠르게 손에 잡는 도구다.

```bash
cargo install samply
samply record ./target/release/myservice
```

*어떤 도구를 언제 쓰는가*는 한 줄로 정리할 수 있다. *CPU 어디가 뜨거운가*는 flamegraph, *async task가 어떻게 흐르는가*는 tokio-console, *프로덕션 바이너리 그대로 떠보고 싶다*는 samply다. JFR/Async Profiler의 감각이 *세 도구로 분리된* 모양이지만, 각 도구의 깊이는 더 깊다.

### PGO와 LTO — 마지막 한 자리수

마지막 한 자리수의 처리량을 짜내고 싶다면 *PGO(Profile-Guided Optimization)*까지 가자. 운영 환경에서 `cargo pgo`로 *대표 트래픽*을 흘려 프로파일을 모으고, 그 프로파일로 다시 빌드한다. JVM의 *JIT가 자동으로 하는 일*을 *AOT 단계에서 한 번에 하는* 발상이다.

```bash
cargo install cargo-pgo
cargo pgo build
# 대표 트래픽으로 워밍업
cargo pgo run -- --warmup-traffic
cargo pgo optimize build
```

처리량이 5~15% 정도 더 나오는 보고가 흔하다. 첫 출시에서 곧장 손댈 영역은 아니다. *p99 latency가 한 자리수 ms 단위에서 더 줄어야 할 때*에 들이대는 도구다. 이 시점이 오면 *너의 시스템이 이미 충분히 무르익었다*는 신호이기도 하다. 그때 한 번 시도해보자.

## 헬스체크와 graceful shutdown

쿠버네티스 환경에서 가장 흔한 *운영 사고 한 줄*은 *SIGTERM이 와도 in-flight 요청을 마무리하지 않고 죽었다*는 보고다. Spring Boot는 `server.shutdown=graceful`과 `spring.lifecycle.timeout-per-shutdown-phase`로 처리한다. axum + tokio에서는 한 패턴으로 박는다.

```rust
use tokio::signal;

async fn shutdown_signal() {
    let ctrl_c = async { signal::ctrl_c().await.expect("ctrl_c handler"); };
    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("SIGTERM handler")
            .recv()
            .await;
    };
    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }
    tracing::info!("종료 신호 수신, graceful shutdown 진입");
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let app = router();
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await?;
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;
    Ok(())
}
```

헬스체크는 그냥 라우트 한 줄이다.

```rust
async fn liveness() -> &'static str { "ok" }
async fn readiness(State(pool): State<PgPool>) -> impl IntoResponse {
    if sqlx::query("SELECT 1").fetch_one(&pool).await.is_ok() {
        StatusCode::OK
    } else {
        StatusCode::SERVICE_UNAVAILABLE
    }
}
```

Spring Actuator의 `/actuator/health`/`/actuator/health/liveness`/`/actuator/health/readiness`가 *코드 한 줄*로 풀린다. 마법이 줄어든 만큼 *내 헬스체크가 무엇을 검사하고 있는지*가 명료하게 보인다. 한 번 손에 익으면 안심된다.

## 컴플라이언스 — ONCD·NSA의 회수

1장에서 ONCD(2024-02)와 NSA(2025-06)의 *메모리 안전 언어 권고*를 본 적이 있다. *"C/C++ 취약점의 70%가 메모리 오류"*라는 Microsoft의 한 줄과 함께였다. 14장에서 그 권고를 운영의 자리로 회수하자.

ONCD 보고서는 미국 정부가 *새로 작성하는 시스템*에 메모리 안전 언어를 *쓸 것을 권고*한다는 한 단락이다. NSA는 한 단계 더 강하게 *메모리 안전 언어*의 대표 후보로 Rust·Go·Java·C#·Swift를 명시한다. 정부·금융·국방 도메인은 이미 *왜 안전한 언어를 쓰지 않느냐*를 묻는 단계로 진입했다. 한국 공공 SI 시장에서도 비슷한 신호가 늘고 있다.

여기서 *잘 굴러가던 Spring 시스템을 다 뒤엎어야 하는가*라는 질문은 잘못된 질문이다. *새로 짜는 컴포넌트* — 사이드카, hot path, 데이터 처리 파이프라인, 보안 관련 라이브러리 — 부터 메모리 안전 언어를 고르라는 권고다. JVM은 GC 덕분에 메모리 안전 언어 카테고리에 들어간다. Rust는 *런타임 GC 없이* 같은 자리에 든다. *그래서 두 언어를 함께 가져가는 폴리글랏*이 자연스러운 선택이 된다. 15장의 본 주제가 그 자리다.

distroless 이미지의 *공격 표면이 거의 0*이라는 사실도 같은 결의 이야기다. *셸이 없으면 RCE가 와도 발판이 없다*. 정부·금융 시장의 *컴플라이언스 체크리스트*에서 distroless가 점점 위로 올라오는 이유다. 한 표 더 적어두자.

| 컴플라이언스 항목 | 일반 JVM 운영 | Rust + distroless |
|---|---|---|
| 메모리 안전성 | GC가 보장 | 컴파일 타임 보장 |
| 컨테이너 셸 접근 | bash 있음 | 없음 |
| 의존성 취약점 스캔 | OWASP/Snyk(외부 도구) | `cargo audit`(워크플로 내장) |
| 라이선스 정책 | FOSSA/Snyk OSS | `cargo deny`(워크플로 내장) |
| 공급망 감사 | Sigstore(별도 셋업) | `cargo vet`(파일 한 개) |
| panic·crash 보고 | Sentry SDK | Sentry crate + panic hook |
| 추적·로그 표준 | OTel Java agent | `tracing` + `tracing-opentelemetry` |

JVM 운영 노하우의 *90%는 그대로 통한다*. SRE 팀이 *처음부터 다시 배워야 한다*는 두려움은 거의 근거가 없다. 새로 익혀야 하는 것은 *musl·distroless·tracing crate 셋팅* 정도다. 나머지는 익숙한 도구의 *Rust 친척*을 한 줄씩 끼워 넣는 일이다. 이 사실은 조직에 Rust를 들이는 정치적 비용을 크게 낮춘다. 16장에서 다시 짚겠지만, *운영팀이 동의한다*는 한 줄이 *결재 라인에서 가장 큰 무게*를 가진다.

## 8MB 이미지가 가져오는 부수 효과

마지막으로 한 단락만 보태자. 이미지가 작아진다는 것은 단순히 *디스크 공간 문제*가 아니다.

첫째, *콜드 스타트*가 빨라진다. 쿠버네티스 노드가 새 파드를 띄울 때 가장 느린 단계가 *이미지 pull*이다. 200MB가 8MB로 줄면 그 단계가 *수십 초에서 1~2초*로 줄어든다. AWS Lambda 같은 서버리스 환경에서는 그 차이가 사용자 응답으로 곧장 보인다.

둘째, *메모리 footprint*가 작아진다. JVM 출신이 가장 놀라는 숫자다. axum + tokio 서비스 한 개가 *5~15MB* 메모리에서 굴러간다. 같은 의미의 Spring Boot 서비스가 *250~400MB*를 잡는 것과 비교하면 *20~30배*다. 한 노드에 *수십 배 많은 인스턴스*를 띄울 수 있다는 뜻이다. 클라우드 비용이 그만큼 떨어진다. 15장의 *AWS 비용 81% 절감* 사례가 이 자리에 닿아 있다.

셋째, *정리정돈의 동력*이 생긴다. 이미지가 8MB로 떨어지면 *불필요한 의존성을 안 끌어들이는 습관*이 자연스럽게 자리잡는다. Spring Boot의 *부풀어 오른 의존성*에 익숙해진 손이, *crate 한 개를 추가할 때 한 번 더 생각하는* 손으로 바뀐다. 이 변화는 코드 품질로 천천히 돌아온다.

물론 *모든 것을 Rust로 옮기자*는 이야기가 아니다. 이 책의 한 줄 결론은 *Rust는 JVM의 대체가 아니라 무기 추가다*. 작은 이미지는 그 무기의 *손에 잡히는 형태*일 뿐이다. 그 무기를 어디에 어떻게 끼워 넣을지가 다음 15장의 주제다.

## 마무리 — 함께 해보자

13장의 axum + sqlx 워크스페이스를 musl + distroless로 빌드해 이미지 크기를 측정하자. 한 줄짜리 표를 적어두면 좋다. *Spring Boot 같은 서비스의 `mvn spring-boot:build-image` 결과*와 옆에 나란히 적자. 두 숫자의 비율을 한 번 보면 마음이 한 번 흔들린다. 그다음 핸들러 하나에 `#[tracing::instrument]` 한 줄을 붙이고 `tracing-opentelemetry`로 OTLP exporter를 띄워, *Jaeger 컨테이너에 트레이스가 들어가는 모습*을 직접 보자. *그 트레이스가 코드의 어디에서 시작해 어디에서 끝나는지*를 손가락으로 짚어보자. 마지막으로 SIGTERM을 보내봐서 *graceful shutdown이 in-flight 요청을 끝낸 뒤*에 종료되는지 확인하자. *(이 8MB 이미지는 15장에서 *Spring 시스템 옆 사이드카*로 배치되어 다시 호출된다.)*

다음 15장에서는 그 8MB 컨테이너를 JVM 시스템 *옆에 또는 안에* 들이는 세 가지 길 — 사이드카, hot path 추출, in-process FFI(JNI/Panama) — 를 한 줄씩 풀어보자. *JVM을 떠나지 않고 Rust를 들이는 다리*가 그 자리에 깔린다.

## 참고

- musl 정적 바이너리 + distroless — reference 토픽 11.1, muslrust GitHub
- `tracing` + `tracing-opentelemetry` 표준 스택 — reference 토픽 11.2, Datadog 가이드
- `cargo flamegraph`, `tokio-console`, `samply` — reference 토픽 11.3
- ONCD/NSA 메모리 안전 언어 권고 — reference 토픽 11.4
- 8MB 이미지 사례 — reference 토픽 11.1, OneUptime 가이드

---

# 15장. JVM과 함께 — FFI·JNI·Project Panama·폴리글랏 아키텍처

이 책의 한 줄 결론을 먼저 박아두자. **Rust는 JVM의 대체가 아니라 무기 추가다.** 1장에서 약속한 한 줄이 15장에서 본격적으로 풀린다. 자네 회사의 Spring 시스템이 *훌륭하게 굴러가고 있는데*, 그 옆에 또는 그 안에 Rust를 어떻게 끼워 넣을 것인가? JNI가 있고, Project Panama가 있고, C ABI가 있고, gRPC 사이드카가 있다. 어느 다리를 어느 모양으로 놓아야 하는가? 그리고 그 다리 위에서 *UB(undefined behavior)*가 새지 않게 하려면 무엇을 잊지 말아야 하는가?

15장은 *떠나지 않는 도입*의 챕터다. *전부 Rust로 갈아엎자*는 단어는 어디에도 등장하지 않는다. 14장에서 만든 8MB 컨테이너를 *Spring 시스템의 짝꿍*으로 배치하는 길, 그리고 한 단계 더 들어가 *같은 프로세스 안에서 Rust 함수를 호출*하는 길까지 한 줄씩 풀어보자. 마지막에는 *AWS 비용 81% 절감* 사례를 솔직한 한 단락으로 회상하자. 이 챕터의 마지막에서도 한 번 더 박을 것이다 — Rust는 JVM의 대체가 아니라 무기 추가다.

## 폴리글랏 전략의 정석 — 세 가지 패턴

JVM 시스템에 Rust를 들이는 길은 사실상 세 가지다. *거리·격리·지연·복잡도*의 4축으로 trade-off가 갈린다. 표 한 줄로 먼저 정리해두자.

| 패턴 | 거리 | 프로세스 격리 | 호출 지연 | 도입 복잡도 | 어울리는 자리 |
|---|---|---|---|---|---|
| **사이드카(gRPC/HTTP)** | 같은 노드/파드 | 강함 | µs~ms 단위 | 낮음 | 이미지 처리, 검색, 변환 |
| **hot path 추출(별도 서비스)** | 같은 클러스터 | 강함 | ms 단위 | 중간 | 매칭 엔진, 인증, 게이트웨이 |
| **in-process FFI(JNI/Panama)** | 같은 프로세스 | 없음 | ns~µs 단위 | 높음 | 해시·인코딩·압축 같은 순수 함수 |

세 패턴은 *어느 하나만 골라야 하는* 양자택일이 아니다. 회사 시스템 전체에서 *위치별로 다르게* 고를 수 있다. 한 줄씩 풀어보자.

### 사이드카 패턴 — 가장 부담이 적은 출발점

14장에서 만든 8MB 컨테이너를 Spring 시스템 옆에 *그냥 한 파드 안의 사이드카*로 배치한다. Spring 측에서는 `localhost:8081`로 gRPC나 HTTP를 한 번 부르면 된다. *프로세스가 분리되어 있어* Rust 측에서 panic이 나도 JVM 측은 영향을 받지 않는다. 가장 안전한 출발점이다.

```yaml
# kubernetes deployment.yaml — 일부
spec:
  containers:
  - name: spring-app
    image: registry/myapp:1.0
  - name: rust-sidecar
    image: registry/myapp-rust:1.0   # 8MB 이미지
    ports:
    - containerPort: 8081
```

Spring 측 호출은 익숙한 모양이다.

```java
@RestController
class ImageController {
    private final WebClient client = WebClient.create("http://localhost:8081");

    @PostMapping("/thumbnail")
    public Mono<byte[]> thumbnail(@RequestBody byte[] image) {
        return client.post().uri("/resize")
            .bodyValue(image)
            .retrieve().bodyToMono(byte[].class);
    }
}
```

WebClient 한 줄로 끝난다. 처음 도입할 때는 *내부 도구*나 *비크리티컬 hot path* 한두 개부터 시작하는 편이 낫다. 운영팀이 *이게 뭐였지*에 빠지지 않게, *왜 이 사이드카가 거기 있는지*를 한 페이지짜리 RFC로 남겨두자. 16장에서 다시 짚을 *조직 도입의 정치*에서 가장 효과가 큰 한 줄이다.

### hot path 추출 — 별도 서비스로 떼어내기

조금 더 진지한 자리는 hot path 추출이다. 사이드카처럼 *한 파드 안에* 있을 필요가 없는, *별도 서비스로 분리*한 모양이다. 이미지 처리 파이프라인, 매칭 엔진, 데이터 직렬화 모듈, 인증 체크 — 자네 시스템에서 *CPU·메모리를 가장 많이 먹는 한 자리*가 후보다. 그 한 자리만 Rust로 옮겨도, 14장에서 본 *20~30배 메모리 절감*과 *5~10배 처리량 증가*가 그대로 따라온다.

이쯤에서 한 사례를 짚어보자. *"I Replaced My Spring Boot Microservice with Rust and Go"*라는 후기 글이 있다. 단일 hot path만 분리해 *AWS 비용을 81% 줄였다*는 보고다. 핵심은 *전체를 옮기지 않았다*는 점이다. 비즈니스 로직 다수는 Spring/Kotlin 그대로 두고, *변환 + 캐싱이 무거웠던 한 자리*만 떼어냈다. 그 후 *기술적으로도 정치적으로도 성공*했다는 한 줄로 글이 닫힌다. *기술 성공·정치 성공*의 두 박수가 동시에 들어와야 한다는 점은 16장에서 다시 짚자.

Cloudflare의 Pingora도 같은 결의 사례다. Nginx + Lua 기반 reverse proxy의 *hot path 한 자리*를 Rust로 다시 짜서 *CPU 70% 절감, 메모리 67% 절감*을 얻었다. 일일 1조 건이 넘는 요청을 처리하면서다. Discord의 Read States 서비스도 *Go GC의 2분마다 spike*를 *Rust 단일 컴포넌트로 분리*해 풀었다. 패턴은 같다. *전체*가 아니라 *한 자리*다.

### in-process FFI — 같은 프로세스 안에서 호출

마지막은 가장 가까운 거리다. JVM 프로세스 안에서 *Rust 함수를 직접 호출*한다. JNI 또는 Project Panama가 그 길이다. 호출 지연은 *나노초 단위*로 떨어지지만, *프로세스 격리가 없다*. Rust 측에서 panic이 새면 JVM이 *Segmentation Fault*로 죽는다. 가장 강력하지만 가장 위험한 길이다. 그래서 이 길은 *순수한 계산*에 집중한다. SHA-256 해시, ZSTD 압축, base64 인코딩, 정규식 매칭 — *외부 자원에 손대지 않는* 함수일수록 안전하다.

세 패턴 중 어느 것이 자네 자리에 맞을까? *모르겠으면 사이드카부터*. 사이드카로 운영해본 경험이 쌓이면 *프로세스 분리의 비용*이 얼마인지 손에 묻혀진다. 그 비용이 정말 아쉬워질 때, 한 단계 안으로 들어가 in-process FFI를 시도해보면 된다. 처음부터 in-process로 들어가는 것은 *난이도가 높다*. 잊지 말자.

## JNI로 JVM에서 Rust 호출

JNI 자체는 자바 출신에게 절반은 익숙한 길이다. *Java 측 코드*를 짜본 적이 있다면, 이 절은 *그 익숙함의 반대편(Rust 측)*을 이어주는 다리다. `jni` crate를 쓰자.

먼저 Java 측 선언이다. *native 메서드*를 한 줄 적어두면 된다.

```java
// io/example/HashLib.java
public final class HashLib {
    static { System.loadLibrary("hashlib"); }
    public static native String sha256Base64(String input);
}
```

이제 Rust 측이다. `Cargo.toml`에 한 단락을 박는다.

```toml
[lib]
name = "hashlib"
crate-type = ["cdylib"]

[dependencies]
jni = "0.21"
sha2 = "0.10"
base64 = "0.22"
```

본 코드는 이렇게 적는다. JNI 함수의 이름 규약은 *Java\_패키지\_클래스\_메서드*다.

```rust
use base64::{engine::general_purpose::STANDARD, Engine as _};
use jni::objects::{JClass, JString};
use jni::sys::jstring;
use jni::JNIEnv;
use sha2::{Digest, Sha256};

#[no_mangle]
pub extern "system" fn Java_io_example_HashLib_sha256Base64<'a>(
    mut env: JNIEnv<'a>,
    _class: JClass<'a>,
    input: JString<'a>,
) -> jstring {
    // JString → Rust String (소유권 가져오기)
    let input_owned: String = match env.get_string(&input) {
        Ok(s) => s.into(),
        Err(_) => return std::ptr::null_mut(),
    };

    // 진짜 일은 safe Rust로 — UB 회피의 첫 번째 원칙
    let digest = Sha256::digest(input_owned.as_bytes());
    let encoded = STANDARD.encode(digest);

    // Rust String → JString
    env.new_string(encoded)
        .map(|s| s.into_raw())
        .unwrap_or(std::ptr::null_mut())
}
```

`#[no_mangle]`은 *함수 이름을 mangling 없이 그대로* 쓰라는 표시다. JNI 측에서 정확한 이름으로 찾아야 하니 필수다. `extern "system"`은 OS가 정한 ABI(Linux x86_64에서는 System V AMD64)를 쓰라는 선언이다.

8장에서 *unsafe 한 절*을 봤던 기억이 있는가? 그때 약속한 회수가 여기다. *왜 JNI 함수가 사실상 unsafe인가?* 두 가지 이유다. 첫째, *JVM이 넘겨주는 jstring/jobject가 진짜로 살아있는 객체인지*를 Rust 측이 보장할 수 없다. JVM의 GC가 *호출 도중*에 그 객체를 옮겨버릴 수도 있다(`JNIEnv`의 local frame이 그래서 존재한다). 둘째, *Rust 측에서 panic이 나면* 그 panic이 JVM 측으로 *unwinding*되며 프로세스 전체가 *죽는다*. 그래서 *JNI 함수의 본문*은 *한 줄도 panic이 나지 않게* 정성껏 다뤄야 한다.

처방은 정해져 있다. *JNI 함수 본문은 외피로만 쓰고, 진짜 일은 safe Rust 함수에 위임*한다. 위 코드도 그 패턴이다. `JString` → `String` 변환만 외피에서 하고, SHA-256 해시는 평범한 safe 함수가 끝낸다. 이 한 줄짜리 규율이 UB의 90%를 막는다. 잊지 말자.

빌드는 `cargo build --release`로 끝난다. macOS에서는 `target/release/libhashlib.dylib`, Linux에서는 `target/release/libhashlib.so`가 떨어진다. JVM 측 `-Djava.library.path`에 그 디렉터리를 박으면 끝이다.

### `catch_unwind`로 panic 막기

이름 그대로 panic이 FFI 경계를 넘는 것을 *잡는* 함수다. `std::panic::catch_unwind`로 본 함수를 감싸 두면, panic이 났을 때 Rust 측에서 *Java 예외*로 변환해 다시 던질 수 있다.

```rust
#[no_mangle]
pub extern "system" fn Java_io_example_HashLib_sha256Base64<'a>(
    mut env: JNIEnv<'a>,
    _class: JClass<'a>,
    input: JString<'a>,
) -> jstring {
    let result = std::panic::catch_unwind(|| {
        // ... 위 본문과 동일
        let s: String = env.get_string(&input).ok()?.into();
        Some(STANDARD.encode(Sha256::digest(s.as_bytes())))
    });

    match result {
        Ok(Some(s)) => env.new_string(s).map(|j| j.into_raw())
                          .unwrap_or(std::ptr::null_mut()),
        Ok(None) => std::ptr::null_mut(),
        Err(_) => {
            // Java RuntimeException으로 던지기
            let _ = env.throw_new("java/lang/RuntimeException", "Rust 측 panic");
            std::ptr::null_mut()
        }
    }
}
```

이 한 단락이 *FFI 경계의 안전벨트*다. `panic = "abort"` 빌드(14장의 release 프로파일 튜닝에서 본)와 함께 쓰면 *panic이 일어나는 즉시 프로세스가 죽는 모양*이 되어, 오히려 디버깅이 쉬워질 때도 있다. 어느 쪽을 고를지는 자네 자리의 신뢰성 요구에 달렸다.

## C ABI와 `#[repr(C)]` — 데이터 경계의 모양

JNI 외에도 *C ABI*를 직접 노출하는 길이 있다. JNR-FFI나 Project Panama처럼 *C ABI를 통해 Rust dylib을 호출*하는 자리에서 필요하다. 핵심은 *Rust struct의 메모리 layout*을 C 호환으로 강제하는 일이다.

기본 Rust struct는 *컴파일러가 마음대로 필드를 재배치*한다. 패킹·정렬·ABI에 대한 가정을 다른 언어 측이 *다르게* 하면 *조용히* 데이터가 깨진다. 가장 흔한 사고다. 처방은 attribute 한 줄이다.

```rust
#[repr(C)]
pub struct Point {
    pub x: f64,
    pub y: f64,
}

#[repr(C)]
pub enum Color {
    Red,
    Green,
    Blue,
}

#[no_mangle]
pub extern "C" fn distance(a: Point, b: Point) -> f64 {
    ((a.x - b.x).powi(2) + (a.y - b.y).powi(2)).sqrt()
}
```

`#[repr(C)]`는 *C 컴파일러가 같은 struct를 짤 때와 같은 레이아웃*을 강제한다. `#[repr(transparent)]`는 *단일 필드 newtype*에 쓴다 — wrapper를 끼워도 ABI 상으로는 *내부 타입과 동일*하다는 약속이다. `#[repr(u8)]`은 enum의 *discriminant 크기*를 명시한다. JVM Panama나 JNR-FFI 측에서 *struct layout을 어떻게 가정할지*가 이 한 줄로 정해진다.

C 헤더 파일을 손으로 적기는 *번거롭다*. `cbindgen`이라는 도구가 그 일을 자동으로 한다.

```bash
cargo install cbindgen
cbindgen --crate mycrate --output include/mycrate.h
```

```c
// include/mycrate.h — 자동 생성
typedef struct Point {
  double x;
  double y;
} Point;

double distance(Point a, Point b);
```

자바 Panama의 `jextract`도 같은 발상이다. *언어 사이의 헤더는 사람이 손으로 적는 것이 아니라 도구가 만든다*는 원칙을 마음에 박자. 손으로 적은 헤더는 *조용히 어긋나는 사고*의 가장 흔한 원인이다.

## Project Panama — 가장 깔끔한 미래

JEP 442/454로 GA가 된 Project Panama는 JVM의 차세대 native interop이다. `Foreign Function & Memory API(FFM API)`로 *JNI 보일러플레이트 없이* Rust dylib을 호출할 수 있다. Java 22+가 기본이다.

```java
// Project Panama 스타일
import java.lang.foreign.*;
import java.lang.invoke.MethodHandle;

public final class HashLib {
    private static final SymbolLookup LIB =
        SymbolLookup.libraryLookup("hashlib", Arena.global());
    private static final MethodHandle SHA = Linker.nativeLinker().downcallHandle(
        LIB.find("sha256_hex").orElseThrow(),
        FunctionDescriptor.of(
            ValueLayout.ADDRESS,   // 반환: 문자열 포인터
            ValueLayout.ADDRESS    // 인자: 입력 문자열 포인터
        )
    );

    public static String sha256Hex(String input) throws Throwable {
        try (Arena arena = Arena.ofConfined()) {
            MemorySegment in = arena.allocateUtf8String(input);
            MemorySegment out = (MemorySegment) SHA.invokeExact(in);
            return out.reinterpret(64).getUtf8String(0);
        }
    }
}
```

이 모양의 매력은 두 가지다. 첫째, *jextract 도구로 헤더에서 자동 바인딩이 생성*된다. 위 코드도 사람이 직접 적기보다는 *도구가 만든 모양*에 가깝다. 둘째, *Arena로 메모리 수명*을 명시적으로 관리한다 — JNI의 local frame보다 *훨씬 솔직한 모델*이다. JVM 출신이 *익숙한 try-with-resources* 모양 그대로다.

*현재 가장 깔끔한 미래*라는 평이 흔하다. 단, JNI vs Panama의 *latency/throughput 정량 비교* 자료는 본 책의 리서치 시점에서 충분히 모이지 않았다(reference 8 한계 2). JEP 442/454의 GA 이후 측정 데이터가 더 모이면 *어느 쪽이 얼마나 빠른지*가 명확해질 것이다. 지금 시점에서는 *새로 시작하는 폴리글랏*이라면 Panama를, *기존 JNI 코드와 호환을 유지해야 한다*면 JNI를 권한다.

JNR-FFI는 또 다른 대안이다. C ABI 기반이라 *Rust 측에 JNI 의존성이 없다*는 매력이 있다. JNI보다 가볍지만 Panama 등장으로 *위치가 애매해지는 중*이다. 새 프로젝트라면 Panama를 먼저 고려하는 편이 낫다.

## UB 회피의 표준 패턴 — 다섯 가지 체크리스트

FFI는 *unsafe의 가장 큰 사용처*다. 한 줄 실수가 *segfault → 데이터 손상 → 보안 사고*로 빠르게 미끄러질 수 있다. 8장 unsafe 절에서 짚었던 원칙을 *FFI 자리*에 맞게 다시 적어두자. 다섯 줄로 외워두면 좋다.

**1. unsafe API는 항상 safe wrapper 뒤에 둔다.**

```rust
// 나쁜 예 — 호출하는 사람이 매번 unsafe 책임을 짐
pub unsafe fn read_buffer(ptr: *const u8, len: usize) -> Vec<u8> {
    std::slice::from_raw_parts(ptr, len).to_vec()
}

// 좋은 예 — 호출자는 safe 함수만 본다
pub fn read_buffer(ptr: *const u8, len: usize) -> Option<Vec<u8>> {
    if ptr.is_null() || len == 0 { return None; }
    // 안전 조건이 위에서 검증됐으니 여기서만 unsafe
    let slice = unsafe { std::slice::from_raw_parts(ptr, len) };
    Some(slice.to_vec())
}
```

unsafe 블록이 *어디서 시작해서 어디서 끝나는지*가 한 줄로 보이는 모양이다. 호출자는 *safe 함수만 보고도 안심*할 수 있다.

**2. lifetime이 불분명한 raw pointer는 즉시 owned로 복사한다.**

JNI/Panama에서 받은 포인터가 *언제까지 유효한지*는 보통 *한 번의 호출 동안*만 보장된다. Rust 측에서 그 포인터를 *struct 안에 보관*하는 순간 사고다. 들어오자마자 `.to_vec()`이나 `.to_owned()`으로 *복사*하자. 비용이 한 번 더 들지만 *마음의 평화*는 그 이상이다.

**3. JVM 측 Java 객체는 JNIEnv local frame을 명시적으로 관리한다.**

긴 루프에서 Java 객체를 반복 생성하면 *local reference table이 차서* JVM이 죽는다. `env.with_local_frame(16, |env| { ... })`로 *프레임 범위*를 명시적으로 잡자. JNI 책에서 가장 자주 등장하는 사고다.

**4. panic은 절대 FFI 경계를 넘지 않게 한다.**

위에서 본 `catch_unwind`다. *외피 함수에 한 번만* 깔아두면 된다. `panic = "abort"` 프로파일과 조합해 *방어선을 두 겹*으로 두는 팀도 많다.

**5. `cargo miri`로 unsafe 코드를 검증한다.**

miri는 *Mid-level IR Interpreter*다. Rust 코드를 *AST 직전 단계에서 해석*하면서 *UB가 발생하는 순간*을 잡아낸다. 일반 테스트로는 잡히지 않는 *aliasing 위반*이나 *uninitialized 메모리 접근*이 한 줄로 드러난다.

```bash
rustup +nightly component add miri
cargo +nightly miri test
```

CI에 miri를 게이트로 박아두는 팀도 있다. 빌드 시간이 *몇 배*로 늘어 매 PR에는 어렵지만, *주 1회 정기 실행*은 충분히 현실적이다. unsafe 코드의 안전망을 한 단계 더 두는 셈이다.

학술 인용을 한 줄 보태두자. *deepSURF*라는 도구가 IEEE S&P 2026에 발표됐다. *FFI 경계의 메모리 안전성을 자동으로 검증*하는 정적 분석기다. 산업 도구로 내려오기까지는 시간이 더 걸리겠지만, *학계가 같은 문제를 같은 자리에서 풀고 있다*는 신호로 알아두자. FFI 안전성은 우리만 고민하는 문제가 아니다.

## 사이드카가 아닌 또 다른 모양들

세 패턴(사이드카·hot path·FFI) 외에도 알아두면 좋은 변형이 두 가지 있다. *결*을 풍성하게 만들어주는 자리들이다.

### Mozilla application-services 패턴

한 Rust crate를 iOS·Android·Desktop이 *공유*하는 모양이다. Mozilla의 [application-services](https://github.com/mozilla/application-services) 저장소가 가장 잘 정돈된 사례다. 인증, 로그인, 동기화 같은 *비즈니스 로직 코어*를 Rust로 짜고, 각 플랫폼은 *JNI(Android), Swift(iOS), Electron 바인딩(Desktop)*로 호출한다. *코드 중복이 사라지는 동시에* 메모리 안전성이 따라온다. 백엔드 책의 스코프 밖이지만, *Kotlin Multiplatform과 같은 발상*이라는 한 줄을 알아두자. Rust가 *모바일까지 한 손에 잡는* 자리에 닿는다.

### WebAssembly — 또 다른 배포 단위

Wasmtime, Wasmer, Spin, wasmCloud 같은 런타임이 *사이드카가 아닌 또 다른 배포 단위*로 떠오르는 중이다. Rust 코드를 `wasm32-wasi` 타겟으로 컴파일하면 *어떤 호스트에서도 동일하게 도는* 작은 모듈이 된다. JVM의 *컴파일 한 번 어디서나 실행*이라는 약속을 *런타임 없이* 풀어내는 모양이다. 백엔드 책의 본 스코프는 아니지만, *플랫폼 간 이식성*이 화두인 자리에서 자주 등장한다. 한국 사례로는 일부 핀테크가 *내부 룰 엔진*을 wasm으로 풀고 있다는 신호도 들린다. 알아두자.

### no_std·임베디드 한 단락

마지막으로 *백엔드 출신이 가장 만나기 어려운* 영역 한 줄을 짚어두자. `no_std`는 *표준 라이브러리 없이 컴파일되는 Rust*다. heap allocation 자체를 *선택적*으로 한다. 임베디드, 펌웨어, 커널 모듈, 부트로더 — Rust는 이 영역에서도 *운영체제 없는 자리*를 메우고 있다. arXiv의 *"Rust for Embedded Systems: Current State and Open Problems"*가 잘 정리해둔 한 편이다.

백엔드 자네에게는 *직접 만질 자리는 거의 없다*. 다만 회사가 IoT·하드웨어·드론 같은 자리로 확장될 때 *Rust가 그 자리에서도 같은 언어로 통한다*는 사실이 *전략적 자산*이 된다. 한 표 더 적어두자.

| 영역 | Rust 자리 | JVM 자리 |
|---|---|---|
| 백엔드 서비스 | 가능(이 책의 본 스코프) | 가능(주력) |
| 모바일 | 가능(application-services 패턴) | Android 가능, iOS 어려움 |
| 데스크톱 | 가능(Tauri, egui) | 가능(JavaFX) |
| 임베디드 | 가능(no_std) | 어려움(GraalVM도 한계) |
| 커널·드라이버 | 가능(Linux/Windows kernel 채택 중) | 거의 없음 |
| WebAssembly | 1급 시민 | 일부 가능(TeaVM) |

JVM이 비워두는 칸이 보일 것이다. *그 빈칸*이 Rust의 자리다. 이 자리들을 잠재적으로 *손에 쥘 수 있다*는 사실이, 자네 회사의 5년 후 기술 지도에 *한 줄짜리 보험*이 된다. 무기 추가다.

## 솔직한 사례 회상 — AWS 비용 81% 절감

15장을 닫으면서 한 사례를 솔직하게 회상하자. *"I Replaced My Spring Boot Microservice with Rust and Go"* 글의 한 단락이다.

저자는 처음부터 *Rust로 다 옮기겠다*고 결심하지 않았다. 자기 시스템의 *AWS 청구서*를 보다가, *변환 + 캐싱이 무거웠던 한 자리*가 비용의 절반을 차지한다는 사실을 발견했다. *그 한 자리만* 떼어 Rust로 다시 짰다. 결과는 *AWS 비용 81% 절감*이었다. 비즈니스 로직 다수는 Spring/Kotlin 그대로 두었다. *기술적으로도 정치적으로도 성공*했다는 한 줄로 글이 닫힌다.

이 사례에서 마음에 새겨야 할 한 줄은 *전체*가 아니라 *한 자리*라는 점이다. *전부 Rust로 갈아엎자*는 결심은 *대부분의 자리에서 정치적 실패*로 끝난다(다음 16장에서 그 그늘을 솔직하게 보자). 반대로 *가장 무거운 한 자리*를 골라 *조용히 다리를 놓는* 결심은 *기술과 정치 두 박수*를 동시에 받는다.

Cloudflare의 Pingora도 같은 모양이다. Nginx 전체를 갈아엎지 않고, *reverse proxy 한 자리*만 다시 짰다. Discord의 Read States도, AWS의 Firecracker도 마찬가지다. *한 자리*다. 자네 회사 시스템에서 *그 한 자리*가 어디인지 — 답은 자네의 모니터링 대시보드 어딘가에 이미 적혀 있다.

## 다시 한 줄로 — Rust는 JVM의 대체가 아니라 무기 추가다

이 챕터의 처음과 같은 한 줄로 닫자. **Rust는 JVM의 대체가 아니라 무기 추가다.** 8MB 사이드카는 그 무기의 한 모양이고, JNI/Panama로 호출되는 순수 함수는 또 다른 모양이다. 어느 모양을 골라도 *JVM을 떠나지 않는다*. *떠나지 않으면서 더 잘하게 된다*는 약속이 이 챕터 전체를 관통한다.

자네 회사의 시스템 지도를 펴보자. 비즈니스 로직 다수는 Spring/Kotlin 그대로 두자. CPU·메모리 가장 많이 먹는 *한 자리*를 골라 사이드카로 떼어 보자. *그 한 자리에서 시작된 변화*가 어디까지 갈지는 — 이 책 다음의 자네 손에 달려 있다. 그것이 16장의 본 주제다.

## 마무리 — 함께 해보자

13장 워크스페이스의 도메인 crate에서 *순수 함수 하나*를 골라보자. SHA-256 해시 + Base64 인코딩 같은, *외부 자원에 손대지 않는* 깔끔한 함수가 좋다. 그 함수를 JNI로 노출해보자. Spring Boot 측에 작은 컨트롤러를 만들어 호출해보고, JFR로 measure해 *같은 함수를 Java로 짠 것*과 처리량을 비교하자. 그다음 같은 함수를 Project Panama 바인딩으로도 노출해 *JNI vs Panama의 보일러플레이트 양 차이*를 손으로 확인해 보자. 두 모양이 같은 일을 *얼마나 다른 모양으로* 해내는지 한 단락으로 정리해두면 좋다. 마지막으로 그 hot path를 *별도 사이드카 컨테이너*로 한 번 떼어내 보자. *세 가지 패턴*을 한 함수로 다 해본 셈이 된다. *(이 hot path 분리 경험은 16장의 *조직 도입 전략*에서 다시 호출된다.)*

여기서부터는 책 안의 다음 챕터가 아니라 *부록 A의 JVM↔Rust 매핑 표를 자네 책상에 펴두고*, 자기 시스템에서 *어디부터 Rust로 옮길지*를 한 줄씩 적어보자. 본문에 산발적으로 박힌 매핑이 *한 페이지에 모인 모양*이라 hot path 후보 결정이 한층 빨라진다. 그 한 줄들이 다음 16장의 *조직 도입 전략*과 그대로 이어진다.

다음 16장에서는 사람과 조직의 자리로 간다. 4~6개월의 학습 곡선, 도입의 정치, 한국 커뮤니티 자원, 그리고 책의 마지막 매듭이 기다리고 있다.

## 참고

- 폴리글랏 전략(사이드카·hot path·FFI) — reference 토픽 12, 토픽 10.3
- JNI(`jni-rs`) 사용법 — reference 토픽 10.3, jni-rs docs
- Project Panama(JEP 442/454) — reference 토픽 10.3
- C ABI / `#[repr(C)]` / cbindgen — reference 토픽 2 보강, 토픽 10.3
- UB 회피 패턴 — reference 토픽 4·8 보강, deepSURF (IEEE S&P 2026)
- Mozilla application-services — reference 토픽 10.3
- AWS 비용 81% 절감 사례 — reference 4.8
- Cloudflare Pingora, Discord Read States — reference 4.1·4.2

---

# 16장. Rust로 가는 길 — 사람·조직·커리어, 그리고 매듭

여기까지 함께 와줘서 고맙다. 자네가 이 책을 처음 펼쳤을 때 1장에서 한 가지 작은 숙제를 적었던 것을 기억하는가? *자기 회사의 가장 최근 운영 사고 한 건을 떠올려 보자. NPE인가, deadlock인가, memory leak인가? Rust가 그 사고를 컴파일 타임에 잡았을지를 한 단락으로 적어보자.* 그 노트를 다시 펴보자. 7장 Result/Option, 9장 Send/Sync, 10장 async 데드락에서 한 번씩 회상했던 그 노트다. 16장 마지막에서 한 번 더 호출할 것이다.

15장까지 우리는 *기술의 자리*에 있었다. 16장은 *사람과 조직의 자리*다. 4~6개월의 학습 곡선을 *팀 차원에서* 어떻게 설계할 것인가, 도입의 정치적 함정은 무엇이고 어떻게 피할 것인가, 한국에서 Rust로 일을 하려면 어디로 가야 하는가, 그리고 이 책 다음의 한 걸음은 무엇인가 — 네 가지 질문을 차례로 풀어보자. 마지막에는 매듭을 짓자. 책 한 권을 읽었다는 사실보다 *그 책이 자네 다음 한 분기를 얼마나 가볍게 만들 수 있는가*가 더 중요하다.

## 솔직한 사례 두 편 — 성공과 실패의 대조

먼저 두 편의 후기 글을 나란히 놓자. 같은 결심에서 출발한 두 사람이 *완전히 다른 끝*에 닿은 이야기다. 16장의 모든 권고가 이 두 사례에서 출발한다.

### 사례 A — *"AWS 비용 81% 절감"*

15장에서 회수했던 *"I Replaced My Spring Boot Microservice with Rust and Go"*다. 한 사람이 자기 시스템의 *변환 + 캐싱 hot path 한 자리*를 Rust로 다시 짰다. 비즈니스 로직 다수는 Spring/Kotlin 그대로 두었다. *전체*가 아니라 *한 자리*였다. 결과는 AWS 비용 81% 절감, P99 latency 대폭 개선이었다. *기술적·정치적 모두 성공*이라는 한 줄로 글이 닫힌다.

이 글의 핵심은 숫자가 아니다. *어떻게 했는가*다. 저자는 PoC를 *비크리티컬 한 자리*에서 시작했다. 사이드카로 운영해본 경험이 두 분기 정도 쌓인 뒤에야 *비용 청구서를 결재 라인에 올렸다*. 그제야 *팀 전체에 Rust를 한 단계 더 들이자*는 합의를 받아냈다. 한 줄로 정리하면 — *기술 성공이 정치 성공으로 자연스럽게 연결되도록* 동선을 깔았다. 이 동선이 거꾸로 가면 두 번째 사례가 된다.

### 사례 B — *"I Rewrote A Java Microservice In Rust And Lost My Job"*

같은 출발점, 다른 끝이다. 자기 회사의 Java 마이크로서비스 한 개를 Rust로 *다시 짰다*. 기술적으로는 *훌륭하게 성공*했다. 코드는 깨끗했고, 메모리는 줄었고, latency는 떨어졌다. 그런데 6개월 뒤 *자기 자리가 사라졌다*. 글의 한 줄을 그대로 인용하자. *"The decision was technically right, politically wrong, and culturally radioactive."*

무슨 일이 벌어진 걸까? 회사에 *Rust를 알 줄 아는 사람이 그 한 명뿐*이었다. 그 한 명이 휴가를 가면 *코드가 묶였다*. 그 한 명이 회사를 떠나면 *그 코드가 짐이 되었다*. *bus factor가 1*인 시스템은, 아무리 코드가 깨끗해도 *조직의 짐*이다. 그래서 그 한 명이 먼저 짐이 되었다. 슬프지만 이상하지 않은 결말이다.

### Dropbox Magic Pocket의 그늘

세 번째 사례를 한 단락으로 보태자. Dropbox의 Magic Pocket은 exabyte-scale blob storage의 storage engine을 Go에서 Rust로 부분 재작성한 *역사적 성공 사례*다. 3~5x tail latency 개선, 노드당 CPU/RAM 절감, OOM 위협 해소. *기술 성공*은 의심의 여지가 없다.

그늘이 한 줄 있다. *너무 잘 굴러가서 손이 안 갔다*. 원작자들이 *떠나자* 그 코드를 다룰 수 있는 엔지니어가 부족해졌다. 한 줄로 인용하자. *"The Rust component just worked, so nobody touched it. When the original authors moved on, finding engineers who could maintain it became a real challenge."*

기술이 너무 잘 돌아가는 것도 *조직 차원의 위험*이 될 수 있다는 한 줄. 우리가 마음에 새겨야 할 한 줄이다. *지속 가능한 유지보수 인력 확보*가 *기술 도입의 한 축*이 되어야 한다는 뜻이다. 다음 절의 권고가 바로 이 자리에서 출발한다.

## 학습 곡선의 정석 — 4~6개월의 정직한 그래프

자, 이제 학습 곡선 자체를 솔직하게 그려보자. corrode의 권고는 한 줄이다. *"Plan 4-6 months for your engineers to get comfortable with Rust, and expect a few bumps along the way."* 4~6개월. 짧지 않다. 하지만 이 책의 1장에서도 같은 한 줄을 적어두었다 — *마법으로 학습 곡선을 줄여주는 책도 아니다 — 4~6개월의 정직한 동반.* 정직하게 가자.

정직한 그래프는 보통 다음 모양이다.

| 시기 | 감정 | 손에 잡히는 것 |
|---|---|---|
| 1주차~1개월 | "왜 컴파일이 안 되지" | 컴파일러 에러 메시지 읽는 법 |
| 1~2개월 | "borrow checker가 적이다" | 5장의 두 줄 규칙, 함수 시그니처에서 `&` `&mut` 구분 |
| 2~3개월 | "borrow checker가 친구가 되어간다" | 7장의 trait 모델링, anyhow/thiserror로 도메인 에러 |
| 3~4개월 | "한 번 빌드되면 정말 잘 돌아간다" | 9장 동시성, 10장 async, 11장 axum 핸들러 |
| 4~6개월 | "Spring 다음의 시스템이 손에 잡힌다" | sqlx CRUD 한 채, 8MB 컨테이너 한 개, 사이드카 한 자리 |

corrode는 *9 months of Rust experience overtaking 10 years of Java experience*라는 한 줄을 남겼다. 한국 4년차 개발자의 후기도 결이 같다. *"익숙해지면 사고가 정리되는 느낌이고, 한 번 작동하면 정말 잘 작동한다."* 4~6개월이 길게 느껴지지만, *그 곡선의 끝에서 손에 들어오는 것*이 있다. 정직한 그래프를 받아들이는 것이 가장 빠른 길이다.

처음 한 달의 처방은 한 줄이면 된다. **컴파일러 에러 메시지를 그대로 따라가는 것이 가장 빠른 길이다.** Rust 컴파일러는 *친절하기로 유명*하다. *어디가 틀렸고, 왜 틀렸고, 어떻게 고치면 되는지*를 거의 모든 메시지에서 알려준다. 처음에는 메시지를 읽는 데 시간이 더 걸린다. 한 달쯤 지나면 메시지가 *번역기 없이 한 번에 들어온다*. 그때부터가 *친구가 되는 시작*이다.

팀 단위로 학습할 때 권하는 모양이 두 가지 있다. 하나는 *주 1회 코드 리뷰 모임*이다. 한 사람이 그 주에 짠 Rust 코드를 다섯 명이 함께 본다. *왜 이렇게 짰는가*를 이야기하는 자리다. 정답을 가르치는 자리가 아니라 *함께 헤맸던 자리를 짚어주는* 자리다. 다른 하나는 *2명 이상의 동시 학습*이다. 한 명이 휴가를 가도 *다른 한 명이 같은 자리에 있다*. bus factor 2가 *1보다 두 배 안전*하다는 뜻이 아니다. *한 사람이 막혔을 때 물어볼 사람이 있다*는 뜻이다. 학습은 외로우면 빨리 닳는다.

## 조직 도입의 정치 — 다섯 가지 권고

이제 *조직 도입의 정치*다. 사례 B의 그늘에서 출발한 다섯 줄이다. 회사에 첫 Rust 프로젝트를 들이려는 자네에게, *기술이 아니라 정치 문서*로 권한다.

**1. 첫 도입은 *기존 시스템 옆*에 두자.**

15장에서 본 사이드카 패턴이다. *기존 Spring 시스템을 안 건드리는* 자리에 Rust를 박는다. 일이 잘 풀리면 *추가된 가치가 명확*하고, 일이 안 풀려도 *기존 시스템은 그대로 굴러간다*. 결재 라인에서 가장 안전한 한 줄이다. *전부 Rust로 갈아엎자*는 결심은 사례 B로 가는 빠른 길이다.

**2. Rust를 아는 사람은 항상 *2명 이상* 두자.**

bus factor 1이 가장 큰 위험이다. 첫 PoC를 시작할 때부터 *최소 두 명*이 같이 들어가야 한다. 한 명만 시작하면 *그 한 명이 퇴사하는 순간 그 코드가 짐*이 된다. 두 명 이상이 같이 시작하면 *코드 리뷰가 가능*하고 *지식이 분산*된다. 사람 비용이 두 배라고 느낄 수 있지만, *그 비용이 1년 뒤 사례 B를 막는다*. 잊지 말자.

**3. 코드 리뷰 가능한 시니어 한 명을 *먼저* 길러내자.**

신규 멤버가 Rust를 짤 때 *PR을 받아서 리뷰해줄 수 있는 한 명*이 있어야 한다. 그 한 명이 없으면 *모든 PR이 그냥 머지*되고, 6개월 뒤 *코드베이스가 무너진다*. 시니어 한 명을 6개월 정도 *집중적으로 키운 다음* 본격 도입하는 편이 낫다. 이 6개월의 *느린 출발*이 결과적으로는 *가장 빠른 길*이다.

**4. CI에 `cargo fmt`/`clippy`/`test`/`audit` 게이트는 *처음부터* 박자.**

13장에서 본 한 줄짜리 게이트를 그대로 옮기자.

```bash
cargo fmt --check && \
cargo clippy --all-targets -- -D warnings && \
cargo test && \
cargo audit && \
cargo deny check
```

이 한 줄이 *코드 리뷰의 절반*을 자동화한다. 신규 멤버의 첫 PR이 게이트를 통과하는 순간 *팀의 표준에 자동으로 정렬된다*. *나중에 추가하자*는 결심은 거의 항상 *나중*이 영영 오지 않는다. 처음부터 박자.

**5. 동료 팀에게 *왜 Rust를 골랐는지* 한 페이지 RFC를 남기자.**

이 한 줄이 가장 정치적이다. *기술 결정의 근거*를 *글로 남기는* 행위다. *왜 사이드카인가, 왜 hot path인가, 왜 이 자리인가, 왜 다른 언어가 아닌 Rust인가, 어떤 운영 비용이 따라오고 어떤 비용이 줄어드는가, bus factor를 어떻게 관리하는가* — 한 페이지면 충분하다. 결재자는 *그 한 페이지를 읽고 결정*한다. 이 페이지가 없으면 *결정이 한 사람의 의견*으로 보이고, 결정이 흔들린다. *한 페이지의 정치 문서*가 *6개월 뒤의 자기 자리*를 지켜준다. 사례 B의 저자가 *처음에 안 적었던 그 한 페이지*다.

다섯 줄을 한 줄로 줄이면 — *기술적으로 옳은 결정이 정치적으로도 옳게 흐르도록* 동선을 깔자. 사례 A와 사례 B의 차이는 *그 동선의 차이*뿐이었다.

## 한국 커뮤니티와 자료 매듭

한국에서 Rust로 일을 하려면 어디로 가야 할까? 본 책의 시점에서 손에 잡히는 자리들을 한 줄씩 모아두자.

**rust-kr.org와 디스코드.** 한국 러스트 사용자 그룹의 공식 사이트가 [rust-kr.org](https://rust-kr.org/)다. Discord 채널 + 정기 Meetup 중심으로 활동한다. *현업에서 러스트로 제품을 개발하고 있는 개발자들이 여럿 상주*한다는 한 줄이 사이트에 적혀 있다. 첫 PoC를 시작하면서 *막힌 자리*를 가벼운 질문으로 던질 수 있는 자리가 한 곳쯤 있다는 사실은 학습 곡선을 한 단계 평탄하게 만든다. 자네의 첫 한 달 안에 가입해두자.

**한국어 도서.** 『러스트 프로그래밍 언어』(rinthel 번역)가 가장 권위 있는 표준 레퍼런스다. 공식 [doc.rust-kr.org](https://doc.rust-kr.org/)로 무료로 볼 수 있다. 본 책이 *JVM 출신을 위한 번역 가이드*라면, rinthel 번역서는 *언어 자체의 표준 레퍼런스*다. 두 책을 책상 옆에 함께 펴두는 모양을 권한다. 그리고 『LUVIT 실전 백엔드 러스트 Axum 프로그래밍』(제이펍)이 한국어로 axum을 깊게 다룬 가장 최근의 한 권이다. 11장에서 axum을 처음 만났던 자네가 *한 단계 더 깊이* 들어가고 싶을 때 권한다.

**한국 개발자 후기 네 편.** 검색으로 찾을 수 있는 1차 자료들이다.

- 김대현, *"Rust를 업무용 언어로 쓰다"* — 서버리스 Lambda + Rust로 비용·응답 모두 만족했다는 한 페이지짜리 후기. 첫 PoC의 모양으로 가장 가깝다.
- Jinwoo Park, *"Rust를 회사 업무로 쓰고난지 5개월 정도"* — 임베디드/시스템 영역에서의 도입. *5개월*이라는 시간이 의미심장하다.
- Option::None(닉네임), *"4년간의 Rust 사용 후기"* — *익숙해지면 사고가 정리되는 느낌이고, 한 번 작동하면 정말 잘 작동한다*는 한 줄이 여기서 나왔다.
- 비브로스 기술 블로그, *"웹프론트엔드 개발자의 Rust 돌려까기"* — 솔직한 그늘 측 후기. 균형 잡힌 마음을 위해 한 번 읽어두자.

**OKKY Rust 채널과 채용 신호.** OKKY 같은 한국 개발자 커뮤니티에 *Rust 토픽 채널*이 늘어나고 있다. 채용 공고 한 줄도 있다 — [디지털헬스케어 Rust 백엔드 개발자(랠릿)](https://www.rallit.com/positions/3247/). 한국 시장에 *Rust 백엔드 채용 자체가 존재한다*는 신호다. 5년 전과는 다른 풍경이다.

**확인 필요한 자리.** 우아한형제들·토스·당근·카카오·네이버·쿠팡 같은 대형 한국 IT의 *공식 Rust 프로덕션 사용기*는 본 리서치 시점에서 충분히 확보하지 못했다. 채용 공고를 통해 *일부 기업이 Rust 백엔드를 운영 중*이라는 *간접 신호*는 있지만, 공식 기술 블로그 글은 *향후 별도 추적*이 필요하다. 이 책이 출간된 뒤 그 글이 나오기를 *함께 기다리자*. 그리고 자네 회사의 첫 Rust 후기가 *그 한 편*이 될 수도 있다.

## 커리어 경로 — 백엔드 시니어가 Rust를 손에 쥐었을 때

자네가 이 책을 끝낸 시점에서, *백엔드 시니어*인 자네가 손에 쥔 것은 단순히 *언어 한 개*가 아니다. *인접 영역*이 함께 열린다. 다섯 줄로 정리해두자.

**1. 시스템·인프라.** 데이터베이스 엔진(SurrealDB·TiKV), proxy(Pingora 후속들), sidecar 런타임(Linkerd2 데이터 플레인 등). *백엔드와 인프라 사이*의 자리가 한층 가까워진다. SRE와 백엔드의 경계가 흐려지는 시대에 *결정적 무기*다.

**2. 임베디드와 IoT.** 위 15장에서 짚은 `no_std`다. 회사가 하드웨어 영역으로 확장될 때 *같은 언어로 통한다*는 사실이 *전략적 자산*이다.

**3. blockchain과 핀테크.** Solana·Aptos 같은 체인이 Rust로 짜여 있다. 한국 시장에서도 *블록체인 백엔드*는 Rust 채용이 가장 활발한 자리 중 하나다.

**4. AI infrastructure.** tokenizer(Hugging Face의 `tokenizers`), inference proxy, vector database(Qdrant), LLM 게이트웨이 — AI infra 영역에서 Rust의 자리가 빠르게 커지고 있다. AI는 모델만의 일이 아니다. *모델을 받쳐주는 인프라*가 곧 시장이다. 자네의 백엔드 경험이 *그 자리에 자연스럽게 닿는다*.

**5. 데스크톱과 크로스 플랫폼.** Tauri로 데스크톱 앱을, Mozilla application-services 패턴으로 모바일 코어를 묶을 수 있다. *백엔드 → 풀스택*의 다리 한 줄이 더 생긴다.

JVM 백엔드의 다음 챕터로서의 Rust — 이것이 한 줄로 정리한 커리어 메시지다. *대체*가 아니라 *추가*다. JVM 위에서 쌓아 올린 자네의 시스템 사고가 *그대로* 새 자리들에 옮겨간다. *9개월의 Rust 경험이 10년의 Java 경험을 추월한다*는 corrode의 한 줄은, *10년의 Java 경험이 사라진다*는 뜻이 아니다. *그 10년이 9개월의 Rust 위에서 한 단계 더 멀리 간다*는 뜻이다. 잊지 말자.

## 매듭 — 1장의 그 운영 사고를 다시 보자

이제 책을 닫을 시간이다. 1장에서 적었던 노트를 다시 펴보자.

자네 회사의 가장 최근 운영 사고 한 건. NPE였는가? deadlock이었는가? memory leak이었는가? 그 사고를 *지금* 다시 본다면, Rust가 *그 사고를 컴파일 타임에 잡았을지*에 대해 자네는 *훨씬 구체적인 답*을 적을 수 있을 것이다.

NPE였다면 — 7장의 `Option<T>`를 떠올려보자. Rust에는 `null`이 없다. *없을 수도 있는 값*은 시그니처에 *그대로* 드러난다. 그 NPE가 *발생한 자리*에 `Option`이 있었다면, 컴파일러가 *호출하는 쪽에서 None을 처리하지 않은 코드*를 빌드 단계에서 거부했을 것이다.

Deadlock이었다면 — 5장의 borrow와 9장의 Send/Sync, 10장의 await/Mutex 함정을 떠올려보자. Rust는 *data race를 컴파일 타임에 차단*한다. await 지점을 가로지르는 동기 Mutex guard는 clippy가 경고로 잡아준다. 모든 deadlock을 잡아주지는 못한다. 하지만 *가장 흔한 모양*의 deadlock은 컴파일 단계에서 모양 자체가 만들어지지 않는다.

Memory leak이었다면 — 4장의 소유권과 8장의 RAII Drop을 떠올려보자. *변수가 scope를 벗어나면 즉시 drop*된다. 파일 핸들, DB 커넥션, 락이 *예측 가능한 시점*에 풀린다. Java의 `try-with-resources`보다 한 단계 더 결정적이다. *finalize를 까먹어서 leak난 그 사고*는, Rust 코드에서는 *모양 자체가 만들어지기 어렵다*.

물론 모든 사고가 잡힌다는 약속은 아니다. *논리 오류*는 어느 언어로도 잡히지 않는다. 그래서 1장의 한 줄을 다시 적자. *Rust는 마법이 아니다.* 다만 *흔한 사고의 큰 카테고리*가 *컴파일 타임으로 옮겨진다*. 그 차이가 *연 1회 운영 회의의 분위기*를 바꾼다. 자네 팀에 *밤늦게 호출되는 사고가 한 분기에 한 건 줄어든다*. 그것이 이 책이 약속한 한 줄이다.

## 동반자로서의 한 단락

이 책을 쓰면서 한 가지 마음을 내내 품고 있었다. *Rust 책 한 권이 자네의 한 분기를 정말로 가볍게 만들 수 있는가*라는 질문이었다. 글을 적는 사람의 입장에서, 자네에게 *지시*를 내리는 책은 짓고 싶지 않았다. *함께 헤맨 자리*를 같이 짚어주는 책, *권유와 청유*로 한 줄씩 같이 가는 책이고 싶었다. 그래서 이 책은 *반말체에 가까운 평어체*로 시작했고, *함께 해보자*로 매 챕터를 닫았다. 자네가 이 동선을 한 챕터씩 지나오는 동안, *적어도 한두 자리에서는* 책이 옆에 앉아 있는 동료처럼 느껴졌기를 바란다.

그리고 또 한 가지 마음이 있었다. *기술서가 사람의 책으로 닫혀야 한다*는 마음이다. 1~15장은 기술의 자리였다. 16장은 의도적으로 *사람과 조직과 커리어*의 자리에 두었다. 책의 마지막을 *코드 한 줄*이 아니라 *팀의 한 페이지짜리 RFC*와 *4~6개월 캘린더의 첫 한 줄*로 닫는 결정이 그 마음의 표현이다. *기술이 사람을 살린다*는 한 줄은 빈말이지만, *기술 결정이 사람의 자리를 지킨다*는 한 줄은 사례 A와 사례 B의 대조에서 본 그대로다. 자네 팀의 사람이 자네의 결정으로 *지켜지기를*. 그리고 그 지켜진 자리에서 *Spring 다음의 시스템*이 같이 자라기를.

## 마지막 한 줄

여기까지 온 자네에게 한 줄. *Spring을 짤 줄 안다는 건 이미 시스템을 만들 줄 안다는 뜻이다.* 컨트롤러를 짤 줄 알고, 서비스 계층을 분리할 줄 알고, 트랜잭션 경계를 그을 줄 알고, 데이터베이스 마이그레이션을 굴릴 줄 알고, 로그와 트레이스로 사고를 추적할 줄 알고, 운영팀과 같은 언어로 말할 줄 안다는 뜻이다. *그 모든 것은 어디로도 가지 않는다.* Rust는 그 위에 *한 가지 도구*를 더 얹어주었을 뿐이다.

이 책의 마지막 한 줄을 1장에서 약속한 모양 그대로 적자.

> **Rust는 JVM의 대체가 아니라 무기 추가다. Spring 다음의 시스템을 손에 쥐자.**

표지에서 만났던 한 줄, 1장 *"이 책의 자리"* 절에서 다시 만났던 한 줄, 그리고 16장에서 한 번 더 만나는 한 줄이다. 세 자리가 한 줄로 정렬되는 모양이, 이 책이 *바이블*을 자처한 한 가지 작은 약속이었다.

## 마무리 — 함께 해보자

자기 회사 시스템의 모듈 지도를 한 장 그려보자. 큰 종이가 좋다. *비즈니스 로직*(Spring/Kotlin 유지) / *hot path 후보*(Rust 사이드카로 분리 가능) / *통신 경계*(gRPC vs JNI vs HTTP)를 색깔로 구분하자. *지금 당장 Rust로 옮길 수 있는 가장 작은 모듈 하나*를 골라, *다음 달 사이드 PoC*의 출발점으로 삼자. 그다음 *2명 이상의 동료*에게 같은 PoC를 함께 하자고 청해보자. 이 책의 다섯 권고를 한 페이지짜리 RFC로 옮겨 적어 *동료 팀에게 회람*하자. 마지막으로 부록 D의 4~6개월 학습 가이드를 펴서 *첫 4주 일정을 자기 캘린더에 한 줄씩 옮기자*. 첫 주는 1~3장, 둘째 주는 4~6장, 셋째 주는 7장, 넷째 주는 8~9장. 작게 시작하자.

이것이 이 책의 마지막 *함께 해보자*다. *다음 호출 지점*은 더 이상 책 안의 어떤 챕터가 아니라 *자네의 코드*다. 자네가 *오늘 적은 한 줄*이 *다음 분기 자네 회사의 첫 8MB 컨테이너*가 된다. 그 컨테이너가 자기 시스템의 *어느 한 자리*에 조용히 들어가 일을 시작한다. 한 분기 뒤 자네는 운영 사고 회의에서 *한 건이 줄었다*는 한 줄을 발표한다. 그 한 줄이 *결재 라인의 다음 한 페이지짜리 RFC*가 된다. 이 동선이 한 번만 한 바퀴 돌면, 자네 팀의 다음 시스템은 *Rust로 시작할 수 있는 자리*에 도달해 있을 것이다.

여기까지 온 자네에게 한 번 더 — Spring을 짤 줄 안다는 건 이미 시스템을 만들 줄 안다는 뜻이다. Rust는 그 위에 한 가지 도구를 더 얹어주었을 뿐이다. *Spring 다음의 시스템을 손에 쥐자.* 함께 가자.

## 참고

- 사례 두 편의 솔직한 대조 — reference 4.8
- Dropbox Magic Pocket의 그늘 — reference 3.4, 4.3
- 4~6개월 학습 곡선 — reference 3.5, corrode "Migrating from Java to Rust"
- 한국 커뮤니티 자원 — reference 토픽 12, 4.7, 한국어 자료 절
- 한국 개발자 후기 네 편 — reference 한국어 자료 절
- 한국 채용 신호 — reference 4.7
- 1장 운영 사고 후크의 회수 — reference 토픽 3·4·5

---

# 에필로그 — 책을 닫으며

여기까지 와줘서 고맙다. 16장이 사람과 조직의 자리에서 책의 매듭을 지었으니, 에필로그는 *책 한 권 전체를 한 호흡으로 닫는* 짧은 자리로 두자.

처음 1장에서 우리가 함께 던진 질문이 있었다. *"Spring으로 잘 굴러가던 내가, 왜 굳이 새로운 언어를 또 배워야 하는가?"* 그 의심에서 출발해서 cargo로 첫 바이너리를 띄워보고, 소유권·빌림·라이프타임의 골짜기를 *천천히* 통과하고, 트레잇과 표현력 도구상자를 손에 쥐었다. 동시성과 async가 *컴파일 타임에* 데이터 레이스를 잡아주는 모습을 봤고, axum 핸들러가 *그저 async 함수*라는 사실을 손가락으로 만져봤다. sqlx가 SQL을 *빌드 단계에서* 검증해주는 약속을 받았고, 8MB 컨테이너로 출시하는 길을 깔았다. 마지막에는 JNI와 Panama로 JVM을 *떠나지 않고* Rust를 들이는 다리를 놓고, 사람과 조직의 자리에서 매듭을 지었다.

이 모든 흐름이 한 줄짜리 약속으로 꿰어진다는 사실을 책의 마지막에서 다시 확인하자. *Rust는 JVM의 대체가 아니라 무기 추가다.* 표지에서 만났던 한 줄, 1장 *"이 책의 자리"* 절에서 다시 만났던 한 줄, 16장 마지막에서 한 번 더 만났던 한 줄이다. 책 한 권의 무게가 이 한 줄로 정렬된다.

그리고 솔직한 한 줄을 더 적자. *이 책은 자네를 4~6개월의 학습 곡선에서 면제해주지 않는다.* 컴파일러와 싸우는 첫 한 달이 *그대로* 자네를 기다리고 있다. 7장의 `Result<T, E>`가 *도메인 모델로 옮겨가는 자리*에서, 9장의 `Send`/`Sync`가 *멀티스레드 빌드를 거부하는 자리*에서, 10장의 `Pin`과 await/Mutex 함정이 *async fn의 시그니처를 한 번 더 들여다보게 만드는 자리*에서, 자네는 책을 다시 펴게 될 것이다. 그때마다 이 책이 *옆에 앉은 동료*처럼 한 줄을 짚어줬으면 한다. 그게 이 책이 약속한 일이다.

이 책의 *다음 호출 지점*은 더 이상 책 안의 챕터가 아니다. *자네의 코드*다. 자네가 *오늘 첫 번째로 실행할 cargo 명령*이 *다음 분기 자네 회사의 첫 8MB 컨테이너*가 된다. 그 컨테이너가 자기 시스템의 *어느 한 자리*에 조용히 들어가 일을 시작하는 풍경. 한 분기 뒤 자네가 운영 사고 회의에서 *"한 카테고리의 사고가 한 건 줄었습니다"*라는 한 줄을 발표하는 풍경. 그 한 줄이 *결재 라인의 다음 한 페이지짜리 RFC*가 되는 풍경. 이 동선이 한 번만 한 바퀴 돌면, 자네 팀의 다음 시스템은 *Rust로 시작할 수 있는 자리*에 도달해 있을 것이다.

여기까지 읽어준 자네에게 한 줄. *Spring을 짤 줄 안다는 건 이미 시스템을 만들 줄 안다는 뜻이다.* 컨트롤러를 짤 줄 알고, 트랜잭션 경계를 그을 줄 알고, 스키마 마이그레이션을 굴릴 줄 알고, 운영팀과 같은 언어로 말할 줄 안다는 뜻이다. *그 모든 것은 어디로도 가지 않는다.* Rust는 그 위에 *한 가지 도구*를 더 얹어줬을 뿐이다. *Spring 다음의 시스템을 손에 쥐자.* 함께 가자.


---

# 부록

본문 16장에 산발적으로 박혀 있던 *JVM ↔ Rust 매핑*과 *cargo 명령*과 *추천 crate*와 *학습 일정*을 한 자리에 모은 부록 네 편이다. 본문이 *시야의 책*이라면 부록은 *책상 옆의 도구*다. 기억해두자 — 이 부록은 *책을 다 읽기 전에도* 펴봐도 좋다. 특히 부록 D의 4~6개월 학습 가이드는 *오늘 자기 캘린더에 첫 한 줄을 옮기는* 데 쓰자.

- **부록 A. JVM ↔ Rust 한 페이지 매핑 표** — 10개 영역의 1:1 대응. 책상 옆에 펴 놓고 보는 *cheatsheet의 cheatsheet*.
- **부록 B. cargo / rustup / clippy / rustfmt 치트시트** — 매일 손에 잡는 명령들의 한 페이지 정리.
- **부록 C. 추천 crate 카탈로그** — *"이 일을 하려면 어떤 crate?"*의 표준 답안. JVM 출신의 Maven Central 즐겨찾기에 해당.
- **부록 D. 4~6개월 학습 가이드** — 주차별 마일스톤을 4단계로 묶은 정직한 그래프.


---

# 부록 A. JVM ↔ Rust 한 페이지 매핑 표

이 부록의 약속은 한 줄이다. *책상 옆에 한 장 펴 놓고 매일 본다*. 본문 16개 챕터에 산발적으로 박힌 *"JVM 대응물 매핑"*을 10개 영역으로 묶어 한 자리에 모았다. 매 행 끝에 *본문 N장 X절 참조*를 박아두었으니, 표만 보다가 깊이가 부족하면 그 자리로 돌아가 본문을 한 절 더 펴자.

기억해두자 — *어떤 매핑도 100% 일치하지는 않는다*. *"의미가 비슷하다"*와 *"표기가 비슷하다"*는 다른 카테고리고, *"역할은 같지만 시점이 다르다"*가 가장 자주 나오는 패턴이다(런타임 검증 vs 컴파일 검증). 표의 *결정적 차이* 열을 꼭 함께 보자.

## A.1 타입 시스템

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| `int` / `long` / `double` / `boolean` / `char` | `i32` / `i64` / `f64` / `bool` / `char` | Rust는 boxing/unboxing 없음. `usize`/`isize`는 *플랫폼 워드 크기*. | 3장 |
| `Integer` / `Long` (autoboxing) | (없음 — 원시 타입 그대로) | Rust는 `Option<i32>`로 *부재*를 표현, `null` 자체가 없음. | 3·7장 |
| `String` (불변) | `String` (heap-allocated owned) + `&str` (borrowed view) | 두 개로 갈라진 게 4장의 *복선*. 함수 파라미터는 보통 `&str`. | 3·4장 |
| `ArrayList<T>` / `List<T>` | `Vec<T>` / `&[T]` (slice) | `Vec<T>`는 owned, `&[T]`는 borrowed. | 3장 |
| `HashMap<K, V>` | `HashMap<K, V>` (`std::collections`) | Rust 표준 HashMap은 *DoS-resistant* hash 사용. | 3장 |
| `Optional<T>` (Java 8+) | `Option<T>` (`Some`/`None`) | Rust는 *exhaustive match*가 컴파일러 강제. NPE 자체가 모양으로 만들어지지 않음. | 7장 |
| `record User(...)` (Java 14+) | `struct User { ... }` + `#[derive(Debug, Clone)]` | Rust는 getter/setter 자동 생성 X — `pub` 필드로 노출하거나 명시적 메서드. | 3·7장 |
| `enum Color { RED, GREEN }` | `enum Color { Red, Green }` | Rust enum은 *algebraic data type* — 변종마다 데이터 보유 가능 (`enum Result<T, E> { Ok(T), Err(E) }`). | 7장 |
| sealed class + pattern matching (Java 17+) | enum + `match` | Rust `match`는 *식*이고 *exhaustive 강제*. `default` 강요 없음. | 3·7장 |
| `interface` / abstract class | `trait` | Rust trait은 *외부 타입에도 구현 가능*(orphan rule 안에서). 정적/동적 디스패치 명시. | 7장 |
| Generics (type erasure) | Generics (monomorphization) | Rust는 컴파일 시점 코드 생성 → 0-cost. 단점은 컴파일 시간·바이너리 크기. | 7장 |

## A.2 제어 흐름

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| `if (...) { } else { }` | `if ... { } else { }` (식) | Rust `if`는 *값을 반환*. `let x = if cond { 1 } else { 2 };`. | 3장 |
| `switch` / `switch expression` | `match` (식) | exhaustive 강제. guard·구조 분해·`@` 바인딩 가능. | 3·7장 |
| `for (T x : collection)` | `for x in collection { }` | `for in`은 `IntoIterator`를 구현한 모든 타입에. | 3장 |
| `while (cond) { }` / `do-while` | `while cond { }` / `loop { ... break value; }` | Rust `loop`는 *값을 반환할 수 있는 무한 루프*. | 3장 |
| `try / catch / finally` | `Result<T, E>` + `?` 연산자 | 예외가 아니라 *값*. `?`는 fallible 함수에서 early return sugar. | 7장 |
| checked exception (`throws`) | `Result<T, E>` 반환 | Rust는 *모든 실패 가능성*이 시그니처에 드러남. | 7장 |
| `RuntimeException` (unchecked) | `panic!` (unrecoverable) | `panic!`은 *복구하지 않을 자리*. 95% 코드는 `Result`. | 7장 |
| `if (x != null)` 가드 | `if let Some(x) = opt { }` 또는 `match` | Rust는 *부재*를 타입으로 강제. | 7장 |

## A.3 모듈·패키지·가시성

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| `package com.example.foo` | `mod foo` (파일 경로 = 모듈 경로) | Rust 모듈은 *파일 시스템에 연결*되지만 명시적 `mod` 선언 필요. | 3장 |
| `import java.util.List;` | `use std::collections::HashMap;` | prelude(`Option`, `Result`, `Vec`, `String`)는 import 없이 보임. | 3장 |
| `public` / package-private / `private` | `pub` / `pub(crate)` / `pub(super)` / (default = private) | Rust 디폴트가 *private*. | 3장 |
| `module-info.java` (JPMS) | `Cargo.toml` + `[lib]` / `[bin]` | crate 단위가 *컴파일·배포 단위*. | 2·13장 |
| Maven multi-module | cargo workspace (`[workspace]`) | 단일 `Cargo.lock`, 단일 `target/` 공유. | 2·13장 |
| jar / war | rlib / dylib / staticlib / 바이너리 | crate type을 `Cargo.toml`에서 선언. | 2장 |

## A.4 예외·에러 처리

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| checked exception (`throws IOException`) | `Result<T, E>` + `?` | 시그니처가 *값*으로 표현됨 → 함수 합성에 자유. | 7장 |
| try-with-resources / `AutoCloseable` | `Drop` 트레잇 (RAII) | scope 종료 시 *결정적*으로 호출. `try` 블록보다 한 단계 더 결정적. | 4·8장 |
| `NullPointerException` | (모양 자체가 안 만들어짐) | Rust에는 `null`이 없음. `Option<T>`로 강제. | 7장 |
| 예외 wrapping (`new RuntimeException(e)`) | anyhow `?` + context (`.context("...")?`) | `anyhow::Result`는 *애플리케이션* 영역. | 7장 |
| 도메인 예외 계층 | thiserror `enum AuthError { ... }` | `#[derive(thiserror::Error)]`로 enum에 자동 구현. *라이브러리* 영역. | 7장 |
| `Optional.orElseThrow` | `option.ok_or(err)?` | sugar의 결이 같지만 *타입 안전*. | 7장 |
| stack trace | `Backtrace` (anyhow + `RUST_BACKTRACE=1`) | 환경 변수로 활성화. | 7장 |

## A.5 동시성·async

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| `Thread` / `ExecutorService` | `std::thread::spawn` / `tokio::spawn` | 표준은 OS 스레드, async 런타임은 별도(tokio). | 9·10장 |
| `Runnable` / `Callable<T>` | 클로저 + `Send + 'static` bound | `'static` bound가 *컴파일러가 강제하는 lifetime 계약*. | 9·10장 |
| `synchronized` (블록) | `Mutex<T>::lock()` (RAII guard) | guard가 scope 종료 시 자동 해제 — *lock 안 풀고 return* 사고가 *모양으로* 안 됨. | 9장 |
| `AtomicInteger` / `AtomicReference` | `AtomicI32` / `AtomicPtr` (`std::sync::atomic`) | Memory ordering(`Ordering::SeqCst` 등)을 *명시*. | 9장 |
| `BlockingQueue` / Kotlin `Channel` | `std::sync::mpsc` / `tokio::sync::mpsc` | std는 동기, tokio는 async. | 9·10장 |
| `@ThreadSafe` / `@GuardedBy` | `Send` / `Sync` 마커 트레잇 | 어노테이션이 아니라 *컴파일러 검증*. | 9장 |
| Java 21 `Virtual Thread` | Rust async + tokio (다른 축) | Virtual Thread는 *블로킹 코드 그대로*, async는 *함수 색깔이 갈림*. | 10장 |
| `CompletableFuture<T>` | `Future` trait + `async` / `await` | `Future`는 컴파일러가 만드는 *상태 머신*. | 10장 |
| Kotlin `suspend fun` | Rust `async fn` | 사용 감각은 가장 가까움. runtime은 직접 골라야 함. | 10장 |
| Spring WebFlux (Reactor `Mono`/`Flux`) | tokio + futures crate stream | callback chain 없음. await는 sequential하게 읽힘. | 10장 |

## A.6 빌드·의존성·도구

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| Maven / Gradle | cargo | 언어 코어에 내장. 외부 도구 별도 조합 불필요. | 2·13장 |
| `pom.xml` / `build.gradle.kts` | `Cargo.toml` (TOML) | `[dependencies]` / `[dev-dependencies]` / `[features]` | 2장 |
| Maven Central | crates.io | semver 표기 (`"1.2"` = `>=1.2, <2.0`). | 2장 |
| sdkman java | rustup toolchain | toolchain 전환 한 줄. `rust-toolchain.toml`로 프로젝트별 고정. | 2장 |
| Gradle multi-module | cargo workspace | `[workspace]` 한 절로 묶음. | 13장 |
| `mvn clean package` / `gradle build` | `cargo build` (`--release`) | 디폴트는 debug, `--release`로 최적화. | 2장 |
| `mvn dependency:tree` | `cargo tree` | 의존 그래프 시각화. | 2장 |
| Spotless / google-java-format | `cargo fmt` (rustfmt) | 한 줄 명령. | 2·13장 |
| SpotBugs / Sonar | `cargo clippy` | 100여 lint 카테고리. `-D warnings`로 CI 게이트. | 13장 |
| OWASP Dependency Check / Snyk | `cargo audit` (RustSec) | 취약점 DB 조회. | 13장 |
| Gradle build cache | sccache | 컴파일 결과 캐시. | 13장 |

## A.7 테스트·품질

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| JUnit 5 | `cargo test` (`#[test]` / `#[cfg(test)]`) | 언어 코어 내장. 통합 테스트는 `tests/` 디렉터리. | 13장 |
| JavaDoc + 코드 예제 | doctest (` ```rust ... ``` `) | 주석 안 코드가 *자동 테스트*. | 13장 |
| Mockito | `mockall` crate | trait 기반. *trait + 더미 구현* 패턴이 더 자주 쓰임. | 13장 |
| JMH | criterion | 통계적 벤치마크. warm-up + outlier 처리 + HTML 리포트. | 13장 |
| AssertJ / Hamcrest | `assert_eq!` / `assert!` / `pretty_assertions` crate | 매크로 기반. | 13장 |
| Property-based testing (jqwik) | `proptest` / `quickcheck` | 입력 자동 생성. | 13장 |
| Snapshot testing (없음 in std) | `insta` crate | UI/JSON 스냅샷. | 13장 |
| JaCoCo (커버리지) | `cargo tarpaulin` / `cargo llvm-cov` | LLVM coverage 인스트루멘테이션. | 13장 |

## A.8 웹 프레임워크

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| Spring Boot | axum + tokio (또는 loco-rs) | DI는 `State<T>` 타입 기반. *컴파일 타임 검증*. | 11장 |
| `@RestController` | (없음 — 함수가 곧 핸들러) | 핸들러는 그저 async 함수. | 11장 |
| `@GetMapping("/users/{id}")` | `Router::new().route("/users/:id", get(handler))` | 라우팅이 *코드*로 표현. | 11장 |
| `@PathVariable Long id` | `Path(id): Path<i64>` (extractor) | extractor가 *타입 기반 시그니처*. | 11장 |
| `@RequestBody User u` | `Json(user): Json<User>` | serde로 자동 직렬화. | 11장 |
| `@Autowired Service s` | `State(state): State<AppState>` | *컴파일 타임 검증*. | 11장 |
| `Filter` / `HandlerInterceptor` / `@Aspect` | tower `Layer` (`Service<Request>` 트레잇) | 한 모델로 통일. axum/tonic/hyper/reqwest 공유. | 11장 |
| `ResponseEntity<T>` | `Result<Json<T>, AppError>` | `IntoResponse` 트레잇 구현으로 응답 변환. | 11장 |
| Tomcat / Netty | hyper (axum 내장) | HTTP/1.1·HTTP/2·HTTP/3. | 11장 |
| `application.properties` / `application.yml` | `config` crate / `figment` / `clap` env | 표준이 없음. crate 선택. | 11·13장 |

## A.9 데이터베이스

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| JDBC | sqlx (raw SQL + 컴파일 타임 검증) | `sqlx::query!`가 *빌드 시점에 DB 접속*해 SQL 검증. | 12장 |
| MyBatis (XML / 매퍼) | sqlx (`query!` / `query_as!` 매크로) | XML 대신 매크로로 SQL 직접 작성. | 12장 |
| Spring Data JPA / Hibernate | sea-orm (Active Record, async) | Entity·ActiveModel·find_by_id/save. loco-rs 기본 ORM. | 12장 |
| QueryDSL / jOOQ | diesel (타입 기반 query DSL) | 가장 *type-safe*. 컴파일 타임 SQL 생성. | 12장 |
| Flyway / Liquibase | `sqlx-cli` / `sea-orm-cli` / `diesel migration` | 마이그레이션 파일 + 버전 관리. | 12장 |
| `@Transactional` (AOP proxy) | `pool.begin().await?` → `tx.commit().await?` | 트랜잭션 경계가 *코드의 한 줄*. self-invocation 함정 없음. | 12장 |
| HikariCP (커넥션 풀) | `sqlx::PgPool` / `sea_orm::DatabaseConnection` | crate 내장. | 12장 |
| MyBatis Generator | `cargo sqlx prepare` (offline 모드) | `.sqlx/` 메타데이터로 CI에서 DB 없이 빌드. | 12장 |

## A.10 관측·운영·배포

| JVM | Rust | 결정적 차이 | 본문 |
|---|---|---|---|
| SLF4J + Logback | `tracing` + `tracing-subscriber` | structured logging이 *기본*. 매크로(`info!`, `error!`). | 14장 |
| Spring Cloud Sleuth | `tracing-opentelemetry` | OTLP exporter로 Jaeger/Tempo/Datadog 전송. | 14장 |
| Micrometer | `metrics` crate / `prometheus` crate | 카운터·게이지·히스토그램. | 14장 |
| Async Profiler / JFR | `cargo flamegraph` (perf 기반) | flamegraph SVG 자동 생성. | 14장 |
| VisualVM (스레드 덤프) | `tokio-console` (async task) | async task의 *대기 위치*를 실시간으로. | 14장 |
| jlink + alpine-jre 이미지 (50~80MB) | musl + distroless 이미지 (8~10MB) | 정적 바이너리 + scratch/distroless. | 14장 |
| GraalVM Native Image | `cargo build --release --target ...-musl` | Rust는 처음부터 그 길로 설계. reflection 깨짐 없음. | 14장 |
| Spring Boot Actuator (헬스체크) | tower middleware + axum route | `/health` 엔드포인트 직접 작성. | 14장 |
| `kill -TERM` → graceful shutdown | tokio signal + `axum::Server::with_graceful_shutdown` | in-flight 요청 마무리. | 14장 |
| JNI (Java → Native) | `jni` crate / Project Panama (Java 22+) | 8장 unsafe + 15장 `#[no_mangle] pub extern "system" fn`. | 8·15장 |

---

표 한 장만 펴 놓고도 *오늘 출근해서 axum + sqlx로 작은 핸들러 한 개*는 짤 수 있는 모양이 됐을 것이다. 깊이가 부족하면 본문의 해당 절을 한 번 더 펴자. 매핑이 *비슷해 보이지만 시점이 다른 자리*가 가장 자주 발이 걸리는 곳이다 — 그때마다 *결정적 차이* 열을 함께 보자.


---

# 부록 B. cargo / rustup / clippy / rustfmt 치트시트

매일 손에 잡는 명령들을 한 페이지에 모았다. JVM 출신이 *gradle / mvn* 명령을 외워 쓰던 감각으로 *cargo* 명령을 손에 묻혀보자. 하나만 기억하면 된다 — *cargo가 거의 다 안고 있다*. 이 부록의 명령 99%는 cargo 한 도구 안에서 끝난다.

## B.1 rustup — toolchain 관리 (sdkman java의 감각)

rustup은 *Rust 자체를 깔고 버전을 전환하는 도구*다. 한 번 깔고 잊어도 되는 자리.

| 명령 | 의미 |
|---|---|
| `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh` | Rust 첫 설치 (Linux/macOS) |
| `rustup update` | 최신 stable로 업데이트 |
| `rustup show` | 현재 설치된 toolchain 확인 |
| `rustup toolchain list` | 설치된 toolchain 목록 |
| `rustup toolchain install nightly` | nightly toolchain 추가 설치 |
| `rustup toolchain install 1.83.0` | 특정 버전 설치 |
| `rustup default stable` | 기본 toolchain 변경 |
| `rustup override set nightly` | 현재 디렉터리만 nightly 사용 |
| `rustup target add x86_64-unknown-linux-musl` | 크로스 컴파일 타겟 추가 (musl 정적 빌드용) |
| `rustup target list --installed` | 설치된 타겟 목록 |
| `rustup component add rustfmt clippy rust-src rust-analyzer` | 컴포넌트 추가 |
| `rustup self uninstall` | rustup 제거 |

**프로젝트 단위 toolchain 고정:** 프로젝트 루트에 `rust-toolchain.toml`을 두고 다음을 적자.

```toml
[toolchain]
channel = "1.83.0"
components = ["rustfmt", "clippy"]
targets = ["x86_64-unknown-linux-musl"]
```

신규 멤버가 클론하면 *자동으로 같은 toolchain*으로 빌드한다.

## B.2 cargo — 빌드·테스트·실행

| 명령 | 의미 |
|---|---|
| `cargo new myproj` | 새 바이너리 프로젝트 생성 |
| `cargo new --lib mylib` | 새 라이브러리 프로젝트 |
| `cargo init` | 현재 디렉터리에 프로젝트 구조 추가 (이미 git init된 자리에) |
| `cargo build` | 디버그 빌드 (`target/debug/`) |
| `cargo build --release` | 릴리스 빌드 (`target/release/`, 최적화 적용) |
| `cargo run` | 빌드 + 실행 |
| `cargo run --release` | 릴리스 빌드로 실행 |
| `cargo run -- arg1 arg2` | 프로그램에 인자 전달 (`--` 뒤가 프로그램 인자) |
| `cargo check` | 타입 체크만 (코드 생성 X). 가장 빠른 피드백 |
| `cargo clean` | `target/` 삭제 |
| `cargo doc --open` | 문서 생성 후 브라우저에서 열기 |
| `cargo doc --no-deps` | 의존성 문서 제외 |
| `cargo update` | `Cargo.lock` 갱신 |
| `cargo update -p some-crate --precise 1.2.3` | 특정 crate를 특정 버전으로 |
| `cargo tree` | 의존성 트리 시각화 |
| `cargo tree -i syn` | `syn`을 *역방향*으로 누가 쓰는지 |
| `cargo search axum` | crates.io 검색 |
| `cargo add axum` | `Cargo.toml`에 의존성 추가 |
| `cargo add tokio --features full` | feature 함께 추가 |
| `cargo remove axum` | 의존성 제거 |

**자주 쓰는 옵션:**

| 옵션 | 의미 |
|---|---|
| `--release` | 릴리스 프로파일로 |
| `--features "foo bar"` | feature 활성화 |
| `--no-default-features` | 디폴트 feature 비활성화 |
| `--all-features` | 모든 feature 활성화 |
| `--workspace` | 워크스페이스 모든 멤버 대상 |
| `--package mycrate` (`-p`) | 특정 crate만 |
| `--bin myapp` | 특정 바이너리만 |
| `--example demo` | examples/ 안의 예제 실행 |
| `--all-targets` | bin/lib/test/example/bench 모두 |
| `--target x86_64-unknown-linux-musl` | 크로스 타겟 |

## B.3 cargo test — 단위·통합·doctest

| 명령 | 의미 |
|---|---|
| `cargo test` | 모든 테스트 실행 (단위 + 통합 + doctest) |
| `cargo test foo` | 이름에 `foo`가 들어간 테스트만 |
| `cargo test --lib` | 라이브러리 단위 테스트만 |
| `cargo test --bin myapp` | 특정 바이너리 테스트 |
| `cargo test --doc` | doctest만 |
| `cargo test --release` | 릴리스 빌드로 테스트 |
| `cargo test -- --nocapture` | `println!` 출력 보기 (`--` 뒤는 test runner 인자) |
| `cargo test -- --test-threads=1` | 단일 스레드로 (테스트 격리 깨질 때) |
| `cargo test -- --ignored` | `#[ignore]` 표시된 테스트도 |
| `cargo test --workspace` | 모든 멤버 |

**더 빠르고 깔끔한 테스트 러너:** [cargo-nextest](https://nexte.st/)

| 명령 | 의미 |
|---|---|
| `cargo install cargo-nextest --locked` | 설치 |
| `cargo nextest run` | 병렬 테스트 + 깔끔한 출력 |
| `cargo nextest run --workspace` | 워크스페이스 전체 |
| `cargo nextest run --no-fail-fast` | 실패해도 끝까지 |

## B.4 clippy — Sonar/SpotBugs의 Rust 표준판

clippy는 100여 카테고리의 lint를 묶은 *Rust 표준 정적 분석기*다. JVM 출신이 SpotBugs/Sonar를 *외부 도구*로 다루던 감각과 달리, clippy는 *cargo의 한 명령*이다.

| 명령 | 의미 |
|---|---|
| `cargo clippy` | 모든 lint 실행 |
| `cargo clippy --workspace --all-targets` | 워크스페이스 + 모든 타겟 |
| `cargo clippy -- -D warnings` | 경고를 *에러*로 (CI 게이트의 표준) |
| `cargo clippy --fix` | 자동 수정 가능한 항목 fix |
| `cargo clippy --fix --allow-dirty --allow-staged` | git에 안 올린 변경도 fix |

**자주 쓰는 lint 카테고리(`#![warn(...)]` 또는 `Cargo.toml`에 적용):**

| 카테고리 | 의미 |
|---|---|
| `clippy::pedantic` | 까다로운 스타일 권고 (취향 영역) |
| `clippy::nursery` | 실험적 lint |
| `clippy::cargo` | Cargo.toml 자체 lint |
| `clippy::complexity` | 복잡도 |
| `clippy::correctness` | 명백한 버그 (가장 중요) |
| `clippy::perf` | 성능 |
| `clippy::style` | 스타일 |
| `clippy::suspicious` | 의심스러운 패턴 |

**lint 끄기 (한 줄):** `#[allow(clippy::too_many_arguments)]`

## B.5 rustfmt — 한 줄 포매터 (ktlint/google-java-format의 감각)

| 명령 | 의미 |
|---|---|
| `cargo fmt` | 모든 파일 포맷 |
| `cargo fmt --check` | 변경 없이 *포맷이 맞는지만* 체크 (CI 게이트) |
| `cargo fmt -- --emit files` | 실제 파일에 쓰기 (디폴트) |
| `cargo fmt -- --emit stdout` | 표준 출력으로 |

**프로젝트 설정:** 루트에 `rustfmt.toml`을 두자.

```toml
edition = "2021"
max_width = 100
hard_tabs = false
tab_spaces = 4
imports_granularity = "Crate"
group_imports = "StdExternalCrate"
```

## B.6 cargo audit / deny / vet — 보안 도구 (OWASP Dependency Check의 감각)

| 명령 | 의미 |
|---|---|
| `cargo install cargo-audit --locked` | 설치 |
| `cargo audit` | 의존성을 RustSec Advisory DB와 대조 |
| `cargo audit --deny warnings` | 경고를 에러로 (CI 게이트) |
| `cargo install cargo-deny --locked` | cargo-deny 설치 |
| `cargo deny init` | `deny.toml` 생성 |
| `cargo deny check` | license / source / dependency / advisory 종합 검사 |
| `cargo deny check licenses` | 라이선스만 |
| `cargo install cargo-vet --locked` | cargo-vet 설치 (supply chain 감사) |
| `cargo vet init` | 감사 대상 등록 |
| `cargo vet check` | 감사 상태 확인 |

**`deny.toml` 미니 예시:**

```toml
[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause", "MPL-2.0"]
deny = ["GPL-3.0", "AGPL-3.0"]

[bans]
multiple-versions = "warn"

[advisories]
db-path = "~/.cargo/advisory-db"
yanked = "deny"
```

## B.7 cargo expand / flamegraph / miri — 디버깅·프로파일링

| 명령 | 의미 |
|---|---|
| `cargo install cargo-expand --locked` | 매크로 펼친 모양 보기 |
| `cargo expand` | 모든 매크로 펼치기 |
| `cargo expand --bin myapp` | 특정 바이너리만 |
| `cargo expand foo::bar` | 특정 모듈만 |
| `cargo install flamegraph --locked` | flamegraph 설치 (perf 필요) |
| `cargo flamegraph --bin myapp` | 프로파일링 후 SVG 생성 |
| `rustup +nightly component add miri` | miri 설치 (UB 검출) |
| `cargo +nightly miri test` | miri로 테스트 (unsafe 검증) |
| `cargo +nightly miri run` | miri로 실행 |

## B.8 cargo workspace — 멀티 모듈 (Gradle multi-module의 감각)

루트 `Cargo.toml`에:

```toml
[workspace]
resolver = "2"
members = ["domain", "infra", "web"]

[workspace.dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
anyhow = "1"
thiserror = "2"
```

각 멤버 `Cargo.toml`에서:

```toml
[package]
name = "domain"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { workspace = true }
anyhow = { workspace = true }
```

| 명령 | 의미 |
|---|---|
| `cargo build --workspace` | 모든 멤버 빌드 |
| `cargo test --workspace` | 모든 테스트 |
| `cargo build -p web` | `web` crate만 |
| `cargo run -p web --bin server` | 특정 바이너리 |

**resolver = "2" 함정 한 줄:** workspace 멤버들이 *다른 feature 조합*으로 같은 의존성을 요구하면 *통합되지 않고 각각 빌드*된다 — 컴파일 시간이 폭증할 수 있으니 13장의 처방을 한 번 펴자.

## B.9 Cargo.toml — 자주 쓰는 항목 미니 레퍼런스

```toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"
authors = ["Toby <toby@example.com>"]
description = "한 줄 설명"
license = "MIT OR Apache-2.0"
repository = "https://github.com/me/myapp"
readme = "README.md"
keywords = ["cli", "tool"]
categories = ["command-line-utilities"]

[dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"], default-features = false }
axum = "0.7"
sqlx = { version = "0.7", features = ["postgres", "runtime-tokio-rustls"] }
tracing = "0.1"
anyhow = "1"
thiserror = "2"

[dev-dependencies]
tokio-test = "0.4"
mockall = "0.13"
proptest = "1"

[build-dependencies]
prost-build = "0.13"

[features]
default = ["postgres"]
postgres = ["sqlx/postgres"]
mysql = ["sqlx/mysql"]

[profile.release]
opt-level = 3
lto = "thin"
codegen-units = 1
strip = true
panic = "abort"

[profile.dev]
opt-level = 0
debug = true

[[bin]]
name = "server"
path = "src/bin/server.rs"

[[bench]]
name = "my_bench"
harness = false
```

**semver 표기 한 줄 정리:**

| 표기 | 의미 |
|---|---|
| `"1.2.3"` | `>=1.2.3, <2.0.0` (caret) |
| `"^1.2.3"` | 위와 동일 (명시적 caret) |
| `"~1.2.3"` | `>=1.2.3, <1.3.0` (tilde) |
| `"=1.2.3"` | 정확히 이 버전 |
| `">=1.2, <2"` | 범위 직접 지정 |
| `"1"` | `>=1.0.0, <2.0.0` |
| `{ git = "...", branch = "main" }` | git 의존성 |
| `{ path = "../mylib" }` | 로컬 경로 |

## B.10 pre-commit 훅 추천 한 단락

`.git/hooks/pre-commit`에 다음을 두자(또는 [pre-commit](https://pre-commit.com) framework 사용).

```bash
#!/usr/bin/env bash
set -euo pipefail
cargo fmt --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
cargo audit --deny warnings
cargo deny check
```

CI 파이프라인의 권장 형태도 같은 줄이다. *fmt → clippy → test → audit → deny → bench --no-run*. 신규 멤버가 들어오는 첫날에 이 한 줄을 박아두면, 6개월 뒤 코드 리뷰 시간이 *체감으로* 짧아져 있다.

---

명령 100여 개를 한 페이지에 모았지만, 매일 손에 잡는 건 *그중 열 개*다. `cargo build`, `cargo test`, `cargo run`, `cargo check`, `cargo fmt`, `cargo clippy -- -D warnings`, `cargo add`, `cargo tree`, `cargo audit`, `rustup update`. 이 열 개만 외워두면 95%의 자리에서 손이 멈추지 않는다. 나머지는 책상 옆에 펴 놓고 보자.


---

# 부록 C. 추천 crate 카탈로그

JVM 출신의 *Maven Central 즐겨찾기*에 해당하는 한 페이지다. *"이 일을 하려면 어떤 crate?"*에 대한 표준 답안. 카테고리별로 *권장 crate / 대안 / 용도 / JVM 카운터파트*를 묶어 정리했다. 모든 crate에 한 줄짜리 *언제 쓰고 언제 안 쓰는가*를 함께 박아두었다 — 무작정 표준이라고 받아들이기보다 *자기 자리의 trade-off*에 맞춰 고르자.

## C.1 웹 프레임워크

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **axum** ★ | tokio 위 HTTP 서버. 가장 활발한 생태계 | Spring MVC | 2024년 이후의 *사실상 표준*. tower 기반. extractor 패턴이 깔끔. |
| **actix-web** | actor 기반. 가장 오래된 production-ready | (직접 대응 없음) | 단일 머신 *처음부터 끝까지 최고 성능*이 필요하면. 학습 곡선 약간 가파름. |
| **poem** | tower 기반, OpenAPI 자동 생성 강점 | Spring + springdoc-openapi | OpenAPI 스펙이 *제품 요구*면 후보. |
| **rocket** | declarative routing (예전엔 nightly 필수였음) | Spring MVC | 2024년 기준 stable. *Spring과 가장 닮은 모양*이지만 axum보다 생태계 작음. |
| **loco-rs** | "Rust on Rails". batteries-included | Spring Boot starter | 빠르게 prototyping하고 싶으면. axum + sea-orm을 한 묶음으로. |
| **tower** | `Service<Request>` 트레잇 + 미들웨어 합성 | Spring `Filter` + AOP | 거의 모든 위 프레임워크가 *그 위에 있다*. 미들웨어 작성 시 이걸 배우자. |
| **hyper** | low-level HTTP/1.1·2·3 | Netty | axum/reqwest의 기반. *직접 만질 일은 드물다*. |
| **tonic** | gRPC 서버·클라이언트 | grpc-java | tower 기반이라 axum 미들웨어를 그대로 쓸 수 있음. |

**언제 axum을 안 쓰는가:** 단일 머신 극한 처리량(actix가 약간 빠름) / OpenAPI 자동 생성이 *제품 요구*(poem) / Rails 스타일 scaffolding 우선(loco-rs).

## C.2 비동기 런타임

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **tokio** ★ | work-stealing 멀티스레드 executor + I/O + sync primitives | (단일 표준 없음 — Spring + Reactor + ExecutorService를 묶은 자리) | 20,768개 crate가 의존하는 *사실상 유일한 선택*. 백엔드면 그냥 tokio. |
| **smol** | 작고 모듈러한 빌딩 블록 | (없음) | 라이브러리·임베디드·*최소 의존*이 필요하면. |
| **async-std** | 표준 라이브러리와 같은 API의 async 버전 | (없음) | 2025년 sunset 발표. 신규 프로젝트에는 권장 안 함. |
| **futures** | `Future` 트레잇 확장(`Stream`, `Sink`, `join_all` 등) | Reactor `Flux`의 한 결 | tokio와 함께 거의 항상 쓰임. |

**언제 tokio가 아닌 것을 고르는가:** *임베디드 / WebAssembly / 최소 바이너리* — smol 또는 `embassy`. 그 외 백엔드는 tokio가 정답.

## C.3 데이터베이스

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **sqlx** ★ | raw SQL + 컴파일 타임 검증 | MyBatis + JDBC | SQL을 직접 짜는 출신(MyBatis/JdbcTemplate)에게 가장 자연스러움. `query!` 매크로가 *빌드 시점에 DB 접속*해 검증. |
| **sea-orm** | Active Record, async-first | Spring Data JPA / Hibernate | JPA 출신이 가장 친숙. loco-rs 기본. |
| **diesel** | 타입 기반 query DSL, 가장 type-safe | QueryDSL / jOOQ | 컴파일 타임 SQL 생성. `r2d2` 기반(전통적으로 sync, 최근 async 지원 추가). |
| **sqlx-cli** | sqlx 마이그레이션 도구 | Flyway | `sqlx migrate add ...` / `sqlx migrate run`. |
| **sea-orm-cli** | sea-orm 마이그레이션 + entity 생성 | Hibernate Tools | `sea-orm-cli generate entity`로 스키마에서 entity 자동 생성. |
| **deadpool** / **bb8** | 커넥션 풀 (sqlx 외 라이브러리용) | HikariCP | sqlx는 자체 풀 내장이라 별도 필요 X. |

**선택 기준 한 줄:** *raw SQL이 좋다 → sqlx*. *ORM의 친숙함이 좋다 → sea-orm*. *컴파일 타임 query DSL의 안전성이 최우선 → diesel*.

## C.4 직렬화

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **serde** ★ | 직렬화 *프레임워크*. derive로 자동 구현 | Jackson `@JsonProperty` 어노테이션 | `#[derive(Serialize, Deserialize)]` 한 줄로 끝. *모든* 직렬화의 기반. |
| **serde_json** | JSON 포맷 백엔드 | Jackson `ObjectMapper` | `serde_json::to_string(&value)?` / `serde_json::from_str::<T>(s)?`. |
| **toml** | TOML 백엔드 | (없음 — config 라이브러리에 묻혀 있음) | Cargo.toml 자체가 TOML. |
| **serde_yaml** | YAML 백엔드 | SnakeYAML | 비활성 유지보수 → `serde_yaml_ng` 또는 `serde_yml` 후보. |
| **bincode** | 컴팩트한 바이너리 포맷 | Java Serializable | RPC 페이로드, 캐시 직렬화. |
| **prost** / **tonic** | Protocol Buffers + gRPC | grpc-java + protoc-jar | gRPC 메시지. |
| **rmp-serde** | MessagePack | msgpack-jvm | 작고 빠른 바이너리. |
| **ciborium** | CBOR | (드묾) | IoT/표준 사양에서 가끔. |

**언제 serde가 아닌가:** 사실상 *모두 serde 위에서 동작*한다. derive 매크로 컴파일 시간이 부담이면 `miniserde` 같은 경량 대안.

## C.5 CLI

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **clap** ★ | argparse 결정판. derive 매크로 | picocli | `#[derive(Parser)]` 한 줄로 subcommand·flag·env·default·completion까지. |
| **structopt** | (deprecated, clap에 흡수됨) | — | clap 4 derive로 대체됨. |
| **dialoguer** | 대화형 CLI(prompt, confirm, select) | jline | Wizard 스타일 CLI에. |
| **indicatif** | 진행률 표시(progress bar, spinner) | (jansi 정도) | 긴 작업의 사용자 피드백. |
| **console** | 색상·터미널 제어 | jansi | indicatif와 한 묶음. |
| **owo-colors** | 컬러 출력 (가벼운 대안) | — | `"hello".green()` 한 줄. |
| **anstyle** | clap 4의 색상 출력 표준 | — | clap을 쓰면 자동으로 따라옴. |

**clap 미니 예제:**

```rust
use clap::Parser;

#[derive(Parser)]
#[command(name = "myapp", version, about)]
struct Cli {
    #[arg(short, long, default_value = "info")]
    log_level: String,
    #[arg(env = "DATABASE_URL")]
    database_url: String,
}
```

## C.6 관측(Observability)

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **tracing** ★ | structured logging + span 기반 추적 | SLF4J + Spring Cloud Sleuth | 백엔드의 *기본 로깅*. `info!()` / `error!()` 매크로. |
| **tracing-subscriber** | tracing 출력 백엔드 | Logback | 포맷·필터·레이어 설정. |
| **tracing-opentelemetry** | OpenTelemetry exporter 어댑터 | OpenTelemetry Java SDK | OTLP로 Jaeger/Tempo/Datadog. |
| **opentelemetry** + **opentelemetry-otlp** | OTel 코어 + OTLP 익스포터 | OTel Java | 보통 위 두 crate와 함께. |
| **metrics** | 백엔드 중립적 메트릭 façade | Micrometer | `counter!()` / `gauge!()` / `histogram!()` 매크로. |
| **metrics-exporter-prometheus** | Prometheus 익스포터 | micrometer-registry-prometheus | `/metrics` 엔드포인트 자동. |
| **prometheus** | 직접 Prometheus 라이브러리 | simpleclient | 더 low-level, 직접 등록. |
| **log** | 단순 logging façade | java.util.logging | tracing 이전 표준. 라이브러리에서 호환을 위해 가끔. |
| **env_logger** | log façade의 간단한 백엔드 | — | 작은 CLI에서 충분. |
| **sentry** | 에러 트래킹 | sentry-java | 프로덕션 알림. |

**권장 한 묶음:** `tracing` + `tracing-subscriber` + `tracing-opentelemetry` + `opentelemetry-otlp` + `metrics` + `metrics-exporter-prometheus`. 14장의 출시 절을 그대로 따르면 된다.

## C.7 테스트

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **tokio-test** | tokio async 테스트 유틸 | — | `#[tokio::test]`만으로 충분한 경우 많음. |
| **mockall** ★ | trait 기반 mocking | Mockito | trait + `#[automock]`으로 mock 자동 생성. |
| **criterion** ★ | 통계적 벤치마크 | JMH | warm-up + outlier + HTML 리포트. |
| **proptest** | property-based testing | jqwik | 입력을 *자동으로 생성*해 가설 검증. |
| **quickcheck** | proptest의 다른 결 | (jqwik) | 더 가벼운 대안. proptest가 우세. |
| **insta** | snapshot testing | — | UI/JSON 스냅샷. `cargo install cargo-insta`로 review CLI. |
| **wiremock** | HTTP mock 서버 | WireMock | 외부 API 통합 테스트. |
| **fake** | 더미 데이터 생성 | java-faker | 사용자명·이메일 등. |
| **rstest** | 파라미터화된 테스트 | JUnit `@ParameterizedTest` | `#[rstest]` + `#[case(...)]`. |
| **pretty_assertions** | diff가 보이는 assert_eq | — | 긴 struct 비교에 필수. |

## C.8 에러 처리

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **thiserror** ★ | 라이브러리용 derive 매크로 | checked exception 계층 | `enum AuthError { ... }` 도메인 에러에. `#[from]`으로 변환 자동. |
| **anyhow** ★ | 애플리케이션용 box 에러 + context | RuntimeException 래핑 | `Result<_, anyhow::Error>` + `.context("...")?`. |
| **snafu** | thiserror의 다른 결, context 강조 | (없음) | 컨텍스트 체이닝이 정교함. |
| **eyre** | anyhow의 fork (color-eyre로 컬러 출력) | — | CLI에서 보기 좋은 에러 출력 원하면. |
| **color-eyre** | eyre + 컬러 백트레이스 | — | 개발 중에 traceback 가독성 큰 폭으로 향상. |

**선택 기준 한 줄:** *내가 라이브러리를 짜고 있다 → thiserror*. *내가 애플리케이션을 짜고 있다 → anyhow*. 둘 다 함께 쓰는 경우가 가장 많다.

## C.9 동시성 자료구조

| crate | 용도 | JVM 카운터파트 | 한 줄 |
|---|---|---|---|
| **parking_lot** ★ | std `Mutex`/`RwLock`보다 빠른 대체 | (없음 — JDK 표준이 빠른 편) | poisoning 없고 더 작음. 거의 항상 std보다 좋음. |
| **dashmap** ★ | concurrent HashMap | ConcurrentHashMap | shard 기반. multi-thread 카운터·캐시. |
| **crossbeam** | 채널·스레드·atomic 확장 | java.util.concurrent | std mpsc보다 빠른 채널. work-stealing 큐 등. |
| **crossbeam-channel** | crossbeam의 채널만 | — | std mpsc의 *직접 대체*. multi-producer + multi-consumer. |
| **flume** | 또 다른 빠른 채널 | — | crossbeam-channel의 대안. |
| **arc-swap** | atomic Arc 교체 | AtomicReference | 자주 읽고 가끔 교체하는 설정 객체에. |
| **once_cell** | 지연 초기화 | (lazy init 패턴) | `OnceCell::new()`. 1.80부터 std에 통합되어 가는 중. |
| **rayon** | data parallelism | parallel streams | `iter().par_iter()` 한 줄로 병렬화. |

**`parking_lot::Mutex`를 안 쓰는 자리:** poisoning이 *반드시* 필요한 경우(거의 없음).

## C.10 보안 도구 (cargo subcommand)

이건 *crate*라기보다 *cargo plugin*이지만 묶어두자.

| 도구 | 설치 | 의미 | JVM 카운터파트 |
|---|---|---|---|
| **cargo-audit** ★ | `cargo install cargo-audit --locked` | RustSec Advisory DB 조회 | OWASP Dependency Check |
| **cargo-deny** ★ | `cargo install cargo-deny --locked` | license / source / dependency policy | OWASP DC + license check + Snyk |
| **cargo-vet** | `cargo install cargo-vet --locked` | supply chain 감사 (Mozilla 주도) | (직접 대응 없음) |
| **cargo-geiger** | `cargo install cargo-geiger --locked` | unsafe 사용량 측정 | — |
| **cargo-outdated** | `cargo install cargo-outdated --locked` | 오래된 의존성 표시 | versions-maven-plugin |
| **cargo-edit** | (1.62부터 cargo 내장) | `cargo add/rm/upgrade` | — |
| **cargo-machete** | `cargo install cargo-machete --locked` | 사용하지 않는 의존성 검출 | — |

**CI 게이트의 표준:** `cargo audit --deny warnings && cargo deny check`. 13장의 마지막 한 줄.

## C.11 부록의 부록 — 자주 쓰는 *기타* crate

한 카테고리로 묶기 애매하지만 매일 쓰게 될 crate들이다.

| crate | 용도 |
|---|---|
| **chrono** / **time** | 날짜·시간. `time`이 더 새롭고 권장 |
| **uuid** | UUID 생성·파싱 |
| **regex** | 정규식 (PCRE보다 빠른 자체 엔진) |
| **url** | URL 파싱 |
| **bytes** | byte buffer (tokio 의존성으로 자주 묻혀 옴) |
| **hex** | hex 인코딩 |
| **base64** | base64 인코딩 |
| **sha2** / **sha3** / **blake3** | 해시 함수 |
| **ring** / **rustls** | 암호화 / TLS (OpenSSL 회피) |
| **reqwest** | HTTP 클라이언트 (axum + tower 생태계 호환) |
| **clap_complete** | clap 자동 완성 생성 |
| **dotenvy** | `.env` 로드 |
| **config** | 설정 파일 로드 (TOML/YAML/JSON/env) |
| **tempfile** | 임시 파일·디렉터리 |
| **walkdir** | 재귀 디렉터리 순회 |
| **notify** | 파일 시스템 변경 감시 |
| **directories** | OS별 사용자 디렉터리 (Linux/Mac/Windows) |
| **tower-http** | axum용 HTTP 미들웨어 (CORS, trace, compression) |
| **axum-extra** | axum 추가 extractor (cookie, typed-header) |
| **tower_governor** | rate limit 미들웨어 |
| **jsonwebtoken** | JWT |
| **argon2** / **bcrypt** | 패스워드 해시 |

---

*"이 crate를 쓰면 됩니다"*는 누구나 한 줄로 적을 수 있다. *"이 crate를 안 쓰면 무엇이 어려운가"*까지 함께 적어야 표가 살아난다. 위 표의 *한 줄* 열을 그 자리로 두려고 했다. 카탈로그 한 페이지를 책상 옆에 펴 두자. 새 작업 앞에서 *"어떤 crate?"* 질문이 떠오를 때 가장 먼저 펴는 자리가 되기를.

마지막 권고 한 줄. 새 crate를 추가할 때마다 *`cargo audit`을 한 번 더 돌리자*. 의존성 트리는 시간이 갈수록 무거워지고, 그 무게는 *6개월 뒤*에 청구서로 돌아온다. 그때 손에 잡히는 도구가 있다는 것 — 그게 cargo 생태계가 JVM 출신에게 가장 친절한 자리다.


---

# 부록 D. 4~6개월 학습 가이드 — 주차별 마일스톤

이 부록은 *오늘 자기 캘린더에 첫 한 줄을 옮기는* 데 쓰기 위해 쓰였다. 16장에서 본 *정직한 그래프*를 24주짜리 마일스톤으로 풀었다. 정직한 그래프는 한 가지를 약속한다 — *4~6개월이 길게 느껴지지만, 그 곡선의 끝에서 손에 들어오는 것이 있다*. 이 약속을 받아들이고, 한 주씩 같이 가자.

기억해두자. *모든 주차에 막힐 수 있다*. 막힌 주는 *한 주 더 써도 괜찮다*. 4~6개월이라는 범위가 그 여유를 미리 깔아둔 것이다. 지치면 쉬자. 단, *완전히 멈추지는 말자*. 한 주에 *코드 한 줄*이라도 짜자.

## D.1 1단계 (1~4주차) — "컴파일러와 싸우는 시기"

### 감정의 풍경

처음 한 달은 *컴파일이 안 되는 한 시간*이 매일 한두 번씩 떨어진다. 답답하다. 그런데 이 답답함은 *모든 Rust 입문자가 통과하는 자리*다. 한국 4년차 개발자의 후기에서도 같은 한 줄이 나온다. *"처음 한 달은 borrow checker와의 싸움이었다."* 이 시기의 처방은 한 줄이면 된다. **컴파일러 에러 메시지를 그대로 따라가자.** Rust 컴파일러는 *어디가 틀렸고, 왜 틀렸고, 어떻게 고치면 되는지*를 거의 모든 메시지에서 알려준다.

### 주차별 일정

**1주차 — 환경 + 기본 문법**
- 본문: 1장 + 2장
- 짤 코드: `cargo new hello-jvm` → 인자 한 개를 받아 출력하는 CLI (clap derive)
- 외부 자료:
  - [The Rust Programming Language 한국어판](https://doc.rust-kr.org/) Ch.1~3 (설치, Hello World, 변수와 타입)
  - [Rust by Example](https://doc.rust-lang.org/rust-by-example/) Hello World
- 멈춰도 되는 신호: rustup·cargo가 잘 깔리고 `cargo run`이 화면에 한 줄 출력하면 1주차는 성공이다.

**2주차 — 변수·타입·함수·모듈**
- 본문: 3장
- 짤 코드: 자기가 잘 아는 Java/Kotlin 도메인 클래스 한 개(예: `User`)를 Rust struct로 옮기기. `#[derive(Debug, Clone)]` 붙여보기.
- 외부 자료:
  - [Rust 한국어판](https://doc.rust-kr.org/) Ch.5~6 (Struct, Enum)
  - [Rust for Java Developers — tkaitchuck](https://tkaitchuck.github.io/Rust4JavaDevelopers/ownership.html)
- 멈춰도 되는 신호: `String` vs `&str`이 *완전히 이해 안 돼도 괜찮다*. 4주차에 한 번 더 만난다.

**3주차 — 소유권의 첫 벽**
- 본문: 4장
- 짤 코드: 책에 나온 `let s = String::from("hi"); let t = s; println!("{s}");` 같은 코드들을 *컴파일러가 거부하는 모양*으로 손에 묻혀보기. clone과 borrow 둘 다로 풀어보기.
- 외부 자료:
  - [Rust 한국어판](https://doc.rust-kr.org/) Ch.4 (Ownership)
  - [scalalang2, "Rust의 소유권 이야기" — CURG](https://medium.com/curg/rust%EC%9D%98-%EC%86%8C%EC%9C%A0%EA%B6%8C-%EC%9D%B4%EC%95%BC%EA%B8%B0-a4c19c1b2c10) — 한국어 입문자 정리
- 멈춰도 되는 신호: *"왜 이게 안 되지?"*가 매일 떠오르면 정상이다. 4주차의 borrow가 답이다.

**4주차 — 빌림과 라이프타임**
- 본문: 5장 + 6장
- 짤 코드: 카운터 구조체 만들고 `&mut`을 *동시에* 두 개 시도해 컴파일러가 거부하는 모양 보기. NLL로 풀기. 함수 시그니처 한 개를 elision으로 시작해서 컴파일러가 `'a`를 요구하는 시점 보기.
- 외부 자료:
  - [Without Boats: Pin](https://without.boats/blog/pin/) — 6장 끝에 미리 펼쳐두면 10장에서 도움
  - [appleseed, "일주일만에 Rust에 매료되다"](https://blog.appleseed.dev/post/fascinated-by-rust-in-a-week/) — 한국어 동기 부여
- 멈춰도 되는 신호: 라이프타임 elision의 *세 가지 규칙*이 손가락으로 짚어지면 1단계 성공이다. `'static`은 7장 이후에 다시 만난다.

### 1단계 매듭

4주차 끝에서 자네가 손에 쥔 것은 *컴파일러와 대화할 줄 아는 기본기*다. 아직 친구는 아니다. *어떤 자리에서 거부당하는지*는 안다. 거부당했을 때 *clone으로 일단 풀어두는 패턴*과 *borrow로 옮겨가는 패턴*이 손에 묻었다. 이것만으로도 1단계는 충분하다.

## D.2 2단계 (5~8주차) — "패턴 인식이 시작되는 시기"

### 감정의 풍경

borrow checker가 *까다로운 시니어*에서 *익숙한 동료*로 변하기 시작하는 시기다. 같은 패턴이 두세 번 반복되면 *왜 거부당하는지*가 보이고, *어떻게 고치면 되는지*가 손가락에 묻어난다. 이 시기의 보상은 두 가지다. 하나는 *Rust로 사고하는 법*이 시작되는 것. 다른 하나는 *7장의 표현력 도구상자*를 손에 쥐면서 *코드의 모양이 점점 깨끗해지는* 경험.

### 주차별 일정

**5주차 — 트레잇·제네릭·패턴 매칭**
- 본문: 7장 전반부 (트레잇, 제네릭, enum + match)
- 짤 코드: 사용자 인증 도메인을 작은 enum으로 표현 (`enum AuthError { ... }`).
- 외부 자료:
  - [Rust 한국어판](https://doc.rust-kr.org/) Ch.10 (Generic Types, Traits, Lifetimes)
  - [softwaremill: Rust Static vs. Dynamic Dispatch](https://softwaremill.com/rust-static-vs-dynamic-dispatch/)

**6주차 — 에러 처리 (Result/Option/?/anyhow/thiserror)**
- 본문: 7장 후반부
- 짤 코드: 위 `AuthError`에 thiserror 적용. `Result<User, AuthError>` 반환 함수 작성. `?` 연산자와 `From` 변환 손에 묻히기.
- 외부 자료:
  - [Rust Error Handling Compared: anyhow vs thiserror vs snafu — DEV.to](https://dev.to/leapcell/rust-error-handling-compared-anyhow-vs-thiserror-vs-snafu-2003)
  - 1장에서 적어둔 *운영 사고 노트* 다시 펴기 — 이번 주에 답을 한 줄 채워보기

**7주차 — 스마트 포인터 + 매크로 + unsafe 진입**
- 본문: 8장
- 짤 코드: `Rc<RefCell<Node>>` 트리 구조 만들어보기. `cargo expand`로 `#[derive(Debug)]`가 펼쳐지는 모양 보기.
- 외부 자료:
  - [The Rustonomicon — Send and Sync](https://doc.rust-lang.org/nomicon/send-and-sync.html) — 9주차 복선
  - [Cui et al. "Is unsafe an Achilles' Heel?"](https://arxiv.org/abs/2308.04785) — unsafe 함정 다섯 가지

**8주차 — 동시성 기초**
- 본문: 9장
- 짤 코드: 100개 스레드가 카운터를 +1하는 코드. Mutex 없이 거부 → `Arc<Mutex<i64>>`로 통과 → `Rc<Mutex<i64>>`로 *Send 위반* 거부 보기.
- 외부 자료:
  - [Tokio docs — Channels](https://docs.rs/tokio/) — 9주차 복습 + 9장 mpsc

### 2단계 매듭

8주차 끝에서 자네는 *Rust로 도메인을 모델링할 줄 안다*. trait + generics + enum + Result/Option이 손에 묻고, `Send`/`Sync`가 *컴파일러의 거부*라는 사실을 손가락으로 확인했다. 1장에서 적어둔 운영 사고 노트의 NPE 자리에 *"여기는 `Option<T>`가 잡았겠다"*라는 한 줄을 채울 수 있다면, 2단계는 후한 점수로 통과다.

## D.3 3단계 (9~16주차) — "첫 실무 코드"

### 감정의 풍경

이제 손이 코드를 만지기 시작한다. async와 axum과 sqlx로 *진짜 서비스 한 채*를 짤 수 있게 된다. *"한 번 빌드되면 정말 잘 돌아간다"*는 4년차 한국 개발자의 후기에 처음으로 공감하는 시기다. 그리고 *컴파일 시간이 길다*는 첫 불만도 시작되는 시기 — 13장의 처방을 미리 한 번 펴자.

### 주차별 일정

**9주차 — async와 tokio**
- 본문: 10장
- 짤 코드: tokio로 외부 HTTP 호출 10개를 동시에 보내고 결과를 합산. await 가로지르는 동기 Mutex를 일부러 넣어 clippy 경고 보기.
- 외부 자료:
  - [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
  - [fasterthanlime: Catching up with async Rust](https://fasterthanli.me/articles/catching-up-with-async-rust)
  - [corrode: The State of Async Rust](https://corrode.dev/blog/async/)

**10주차 — async 깊이 + Pin**
- 본문: 10장 후반 (function coloring, async fn in trait)
- 짤 코드: `tokio::select!`로 두 작업 중 먼저 끝나는 것 받기. cancellation 패턴.
- 외부 자료:
  - [Without Boats: Pin](https://without.boats/blog/pin/)
  - [Without Boats: Three problems of pinning](https://without.boats/blog/three-problems-of-pinning/)

**11주차 — axum 첫 핸들러**
- 본문: 11장 전반
- 짤 코드: `GET /users/{id}`, `POST /users` 두 핸들러. `Arc<DashMap<i64, User>>`로 in-memory 저장.
- 외부 자료:
  - [axum docs](https://docs.rs/axum/)
  - [Indo Yoon, "실전 백엔드 러스트 Axum 프로그래밍" — 책 소개](https://devbull.xyz/blog/axum-book) — 한국어 보강

**12주차 — axum + tower 미들웨어**
- 본문: 11장 후반
- 짤 코드: 11주차 서비스에 `X-Request-Id` 헤더 자동 부여 미들웨어. 인증 미들웨어 한 개. 7장의 `AuthError`를 `IntoResponse`로 매핑.
- 외부 자료:
  - [Leapcell: Unpacking the Tower Abstraction Layer](https://leapcell.io/blog/unpacking-the-tower-abstraction-layer-in-axum-and-tonic)

**13주차 — sqlx로 옮기기**
- 본문: 12장 전반
- 짤 코드: 11주차의 in-memory CRUD를 PostgreSQL로 옮기기. SQL 한 줄을 일부러 틀리게 적어 빌드가 거부하는 모습 보기.
- 외부 자료:
  - [sqlx repo](https://github.com/launchbadge/sqlx)
  - [Leapcell: Unraveling sqlx Macros](https://leapcell.io/blog/unraveling-sqlx-macros-compile-time-sql-verification-and-database-connectivity-in-rust)

**14주차 — sea-orm + 트랜잭션**
- 본문: 12장 후반
- 짤 코드: 같은 도메인을 sea-orm으로 다시 짜보기. 두 코드의 한 줄 한 줄이 어떻게 다른 trade-off인지 노트.
- 외부 자료:
  - [SeaORM docs](https://www.sea-ql.org/SeaORM/)
  - [sangjinsu, "Rust로 실전 백엔드 개발을 경험하다"](https://velog.io/@sangjinsu/Rust%EB%A1%9C-%EC%8B%A4%EC%A0%84-%EB%B0%B1%EC%97%94%EB%93%9C-%EA%B0%9C%EB%B0%9C%EC%9D%84-%EA%B2%BD%ED%97%98%ED%95%98%EB%8B%A4) — 한국어 후기

**15주차 — workspace + 테스트 + 도구 인프라**
- 본문: 13장 전반 (workspace, doctest, criterion, clippy)
- 짤 코드: 13~14주차 서비스를 도메인/인프라/웹 세 crate로 쪼개기. 도메인 함수 하나에 doctest 붙이기.
- 외부 자료:
  - [The Cargo Book — Workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html)

**16주차 — 보안 게이트 + 매크로 + CLI**
- 본문: 13장 후반 (cargo audit/deny/vet, 매크로 작성, clap)
- 짤 코드: CI에 `cargo audit` 게이트 끼우기. `assert_close!` 매크로 직접 짜보기. 2주차의 CLI를 clap으로 완성형으로.
- 외부 자료:
  - [cargo-audit](https://github.com/RustSec/rustsec)
  - [The Rust Reference — Macros](https://doc.rust-lang.org/reference/macros.html)

### 3단계 매듭

16주차 끝에서 자네는 *axum + sqlx로 작은 서비스 한 채를 짜고 워크스페이스로 쪼개고 CI 게이트를 박을 줄 안다*. 이 자리가 *Spring 다음의 시스템*에 첫 발이 닿는 자리다. 잠시 멈춰서 자축하자. 4개월 전의 자신이 *"왜 이게 컴파일이 안 되지?"* 했던 자리에서 *지금의 자신*은 *컴파일러가 이걸 잡아주니까 평일 새벽 알람이 줄겠구나*를 생각하고 있다. 그 변화가 가장 큰 보상이다.

## D.4 4단계 (17~24주차) — "Rust로 출시하는 시기"

### 감정의 풍경

이제 *팀과 회사*를 바라보기 시작한다. 자네가 짠 첫 사이드 프로젝트를 *결재 라인에 올리는* 자리, 동료를 *함께 학습하자고 끌어들이는* 자리, 한국 커뮤니티에 *첫 글을 올리는* 자리. 기술의 자리에서 사람의 자리로 무게중심이 한 번 옮겨가는 시기다.

### 주차별 일정

**17주차 — 8MB 컨테이너로 출시**
- 본문: 14장 전반 (musl + distroless)
- 짤 코드: 16주차의 axum + sqlx 서비스를 musl + distroless로 빌드. 이미지 크기를 Spring Boot 이미지와 비교.
- 외부 자료:
  - [muslrust GitHub](https://github.com/clux/muslrust)
  - [Chainguard: Distroless container images](https://edu.chainguard.dev/chainguard/chainguard-images/about/getting-started-distroless/)
  - [Leapcell: Building Minimal and Secure Rust Web Applications with Docker](https://leapcell.io/blog/building-minimal-and-secure-rust-web-applications-with-docker)

**18주차 — 관측(tracing + OpenTelemetry)**
- 본문: 14장 후반
- 짤 코드: 핸들러에 `#[tracing::instrument]` 붙이고 OTLP exporter로 Jaeger에 트레이스 보기. `tokio-console`로 task 들여다보기.
- 외부 자료:
  - [tracing docs](https://docs.rs/tracing)
  - [Datadog: How to monitor your Rust applications with OpenTelemetry](https://www.datadoghq.com/blog/monitor-rust-otel/)

**19주차 — JNI로 첫 다리 놓기**
- 본문: 15장 전반 (JNI, C ABI, `#[repr(C)]`)
- 짤 코드: 도메인 crate에서 순수 함수 하나(SHA-256 해시 + Base64)를 JNI로 노출. Spring Boot에서 호출하기.
- 외부 자료:
  - [jni-rs GitHub](https://github.com/jni-rs/jni-rs)
  - [Tweede golf: Mix in Rust with Java (or Kotlin!)](https://tweedegolf.nl/en/blog/147/mix-in-rust-with-java-or-kotlin)
  - [Comprehensive Rust — Java interop (Google)](https://google.github.io/comprehensive-rust/android/interoperability/java.html)

**20주차 — Project Panama + UB 회피**
- 본문: 15장 후반
- 짤 코드: 19주차의 함수를 Panama 바인딩으로도 노출. 보일러플레이트 양 비교. `std::panic::catch_unwind` 패턴 손에 묻히기.
- 외부 자료:
  - [Frankel: Rust and the JVM](https://blog.frankel.ch/start-rust/7/)
  - [JEP 442 / 454 — Foreign Function & Memory API](https://openjdk.org/jeps/454)

**21주차 — 사이드카 패턴**
- 본문: 15장 + 16장 도입
- 짤 코드: 17주차의 8MB 컨테이너를 *Spring 시스템 옆에 사이드카로* 배치. gRPC 또는 HTTP로 통신.
- 외부 자료:
  - [I Replaced My Spring Boot Microservice with Rust and Go](https://medium.com/@toyezyadav/i-replaced-my-spring-boot-microservice-with-rust-and-go-heres-the-system-design-that-saved-my-f3ccedd6e494) — 사례 회독
  - [Cloudflare: How we built Pingora](https://blog.cloudflare.com/how-we-built-pingora-the-proxy-that-connects-cloudflare-to-the-internet/)

**22주차 — 첫 RFC + 동료 끌어들이기**
- 본문: 16장 (조직 도입의 정치 5가지 권고)
- 짤 코드: 자기 회사 시스템의 *모듈 지도*를 한 장 그리기. *비즈니스 로직 / hot path 후보 / 통신 경계*를 색깔로 구분.
- 외부 자료:
  - [I Rewrote A Java Microservice In Rust And Lost My Job](https://medium.com/@noahblogwriter2025/i-rewrote-a-java-microservice-in-rust-and-lost-my-job-2c01f63ed0ca) — *반면교사*로 회독
  - [Dropbox: Inside the Magic Pocket](https://dropbox.tech/infrastructure/inside-the-magic-pocket)
- 추가 활동: 한 페이지짜리 RFC 초안을 동료 한 명과 함께 검토.

**23주차 — 한국 커뮤니티에 첫 발 들이기**
- 본문: 16장 한국 커뮤니티 절
- 활동:
  - [rust-kr.org](https://rust-kr.org/) 가입
  - [한국 러스트 디스코드](https://rust-kr.org/) 또는 OKKY Rust 태그 둘러보기
  - 자기 8MB 사이드카 PoC를 짧은 글로 정리해 velog 또는 회사 블로그에 올리기
- 외부 자료:
  - [김대현, "Rust를 업무용 언어로 쓰다"](https://medium.com/happyprogrammer-in-jeju/rust%EB%A5%BC-%EC%97%85%EB%AC%B4%EC%9A%A9-%EC%96%B8%EC%96%B4%EB%A1%9C-%EC%93%B0%EB%8B%A4-7723cd2c0a59)
  - [Option::None, "4년간의 Rust 사용 후기"](https://blog.cro.sh/posts/four-years-of-rust/)

**24주차 — 매듭과 그 다음의 한 걸음**
- 본문: 16장 매듭
- 활동:
  - 1장에서 적어둔 운영 사고 노트의 *마지막 답*을 채우기
  - 자기 캘린더에 *다음 4주의 첫 한 줄*을 적기 (24주차로 끝나지 않는다 — 그저 *공식 일정의 끝*이다)
  - 동료 한 명에게 *다음 분기 함께할 PoC*를 청하기
- 외부 자료: 부록 A·B·C를 책상 옆에 펴두자. *이 자리부터는 책 밖이다*.

### 4단계 매듭

24주차 끝에서 자네는 *Spring 시스템 옆에 Rust 사이드카 한 채를 띄울 줄 안다*. 첫 PoC가 결재 라인에 올라가 있을 수도 있고, 한국 Rust 커뮤니티에 자네 글이 한 편 올라가 있을 수도 있다. 그게 아니라도 좋다 — *4~6개월 전의 자신*이 *지금의 자신*을 보면 어떤 표정을 지을까. 그 표정이 이 동선 전체의 보상이다.

## D.5 6개월 이후 — 책 밖의 시간

이 가이드는 24주차에서 끝나지만 *학습은 끝나지 않는다*. 사실 이 자리부터가 *진짜 시작*이다. 6개월 이후의 자네에게 권하고 싶은 세 가지를 적어두고 부록을 닫자.

**첫째, 자기 회사 시스템에 *두 번째 PoC*를 시작하자.** 첫 PoC가 사이드카였다면, 두 번째는 *in-process FFI*나 *완전한 마이크로서비스*가 될 수 있다. 한 번 한 바퀴 돈 동선이 두 번째에 *체감으로 빨라진다*. 그게 4년차 한국 개발자의 후기에 적힌 *"한 번 작동하면 정말 잘 작동한다"*가 의미하는 한 줄이다.

**둘째, 한국 Rust 커뮤니티에서 *기여자*가 되어보자.** rust-kr.org의 글에 댓글을 다는 것부터 시작해도 좋다. 자기 회사의 PoC 사례를 *한 페이지 글*로 정리해 한국 커뮤니티에 공유하면, *우리가 1장에서 함께 기다린* 그 글 — *한국 대형 IT 기업의 공식 Rust 프로덕션 사용기* — 의 한 자리를 자네가 채우게 된다. 그 글이 다음 입문자에게 닻이 된다.

**셋째, 인접 영역으로 한 발 더 나가보자.** Rust를 손에 쥔 백엔드 시니어 앞에는 새 자리들이 열려 있다. 시스템·인프라(데이터베이스 엔진, proxy, sidecar), AI 인프라(tokenizer, inference proxy, vector DB), 임베디드, blockchain. *JVM 백엔드의 다음 챕터*로서의 Rust가 본격적으로 펼쳐지는 자리다.

마지막 한 줄. *4~6개월의 학습 곡선은 길다*. 그러나 그 곡선의 끝에서 자네가 손에 쥔 것은 *언어 한 개*가 아니라 *사고 모델 한 가지*다. 그 사고 모델은 *어디로도 가지 않는다*. 그게 이 동선이 약속한 한 가지다. 함께 가자.


---

# 참고문헌

본문 16개 챕터의 각주에서 인용한 모든 자료를 카테고리별로 묶어 한 자리에 모았다. 발행 연도가 명시된 자료는 함께 적었다. 한국어 자료는 별도 카테고리로 묶어 검색 동선을 줄였다.

## 학술 논문

- Cui, M. et al. ["Is unsafe an Achilles' Heel? A Comprehensive Study of Safety Requirements in Unsafe Rust Programming" (arXiv:2308.04785, 2023)](https://arxiv.org/abs/2308.04785).
- deepSURF authors. ["deepSURF: Detecting Memory Safety Vulnerabilities in Rust" (IEEE S&P 2026, arXiv:2506.15648)](https://arxiv.org/html/2506.15648v2).
- Gäher, L. et al. ["RefinedRust: A Type System for High-Assurance Verification of Rust Programs" (PLDI 2024)](https://plv.mpi-sws.org/refinedrust/paper-refinedrust.pdf).
- Jung, R., Dang, H.-H., Kang, J., Dreyer, D. ["Stacked Borrows: An Aliasing Model for Rust" (POPL 2020)](https://plv.mpi-sws.org/rustbelt/stacked-borrows/paper.pdf).
- Jung, R., Jourdan, J.-H., Krebbers, R., Dreyer, D. ["RustBelt: Securing the Foundations of the Rust Programming Language" (POPL 2018)](https://plv.mpi-sws.org/rustbelt/popl18/paper.pdf); [CACM 2021 정리본](https://iris-project.org/pdfs/2021-rustbelt-cacm-final.pdf).
- "Rust for Embedded Systems: Current State and Open Problems" [(arXiv:2311.05063, 2023)](https://arxiv.org/html/2311.05063v2).
- "A Grounded Conceptual Model for Ownership Types in Rust" [(arXiv:2309.04134, 2023)](https://arxiv.org/pdf/2309.04134).
- Villani, N., Hostert, J., Dreyer, D., Jung, R. ["Tree Borrows" (PLDI 2025)](https://iris-project.org/pdfs/2025-pldi-treeborrows.pdf); [블로그 소개 — Ralf Jung](https://www.ralfj.de/blog/2023/06/02/tree-borrows.html).
- Xu, H. et al. ["Memory-Safety Challenge Considered Solved? An In-Depth Study with All Rust CVEs" (arXiv:2003.03296, 2020)](https://arxiv.org/abs/2003.03296v1).

## 공식 문서·정부 보고서

- [The Rust Programming Language Book](https://doc.rust-lang.org/book/) — Steve Klabnik, Carol Nichols.
- [The Cargo Book](https://doc.rust-lang.org/cargo/).
- [The Rustonomicon — Send and Sync](https://doc.rust-lang.org/nomicon/send-and-sync.html).
- [The Rust Reference — Macros](https://doc.rust-lang.org/reference/macros.html).
- [Tokio docs](https://docs.rs/tokio/), [tokio.rs Tutorial](https://tokio.rs/tokio/tutorial).
- [axum docs](https://docs.rs/axum/).
- [sqlx repo](https://github.com/launchbadge/sqlx); [sqlx 매크로 레퍼런스](https://docs.rs/sqlx/latest/sqlx/macro.query.html).
- [Diesel — diesel.rs](https://diesel.rs/); [Diesel relations](https://diesel.rs/guides/relations.html).
- [SeaORM — sea-ql.org](https://www.sea-ql.org/SeaORM/).
- [clap docs](https://docs.rs/clap/); [clap derive 튜토리얼](https://docs.rs/clap/latest/clap/_derive/_tutorial/index.html).
- [tracing docs](https://docs.rs/tracing); [tracing-opentelemetry docs](https://docs.rs/tracing-opentelemetry).
- [JEP 442 / 454 — Foreign Function & Memory API](https://openjdk.org/jeps/454).
- [Workspaces — The Cargo Book](https://doc.rust-lang.org/cargo/reference/workspaces.html).
- [White House ONCD: "Back to the Building Blocks: A Path Toward Secure and Measurable Software" (2024-02)](https://bidenwhitehouse.archives.gov/wp-content/uploads/2024/02/Final-ONCD-Technical-Report.pdf).
- [NSA: "Memory Safe Languages — Reducing Vulnerabilities in Modern Software Development" (2025-06)](https://media.defense.gov/2025/Jun/23/2003742198/-1/-1/0/CSI_MEMORY_SAFE_LANGUAGES_REDUCING_VULNERABILITIES_IN_MODERN_SOFTWARE_DEVELOPMENT.PDF).

## 산업 사례 — 회사 엔지니어링 블로그

- AWS: [Firecracker GitHub](https://github.com/firecracker-microvm/firecracker); [Firecracker AWS Blog](https://aws.amazon.com/blogs/aws/firecracker-lightweight-virtualization-for-serverless-computing/); [Firecracker Open Source Blog](https://aws.amazon.com/blogs/opensource/firecracker-open-source-secure-fast-microvm-serverless/); [Firecracker NSDI 논문](https://assets.amazon.com/96/c6/302e527240a3b1f86c86c3e8fc3d/firecracker-lightweight-virtualization-for-serverless-applications.pdf).
- Cloudflare: ["How we built Pingora"](https://blog.cloudflare.com/how-we-built-pingora-the-proxy-that-connects-cloudflare-to-the-internet/); ["20-percent internet upgrade"](https://blog.cloudflare.com/20-percent-internet-upgrade/).
- Convex: ["A Tale of Three Rust Codebases"](https://news.convex.dev/a-tale-of-three-codebases/).
- Discord: ["Why Discord is switching from Go to Rust"](https://discord.com/blog/why-discord-is-switching-from-go-to-rust).
- Dropbox: ["Inside the Magic Pocket"](https://dropbox.tech/infrastructure/inside-the-magic-pocket); ["Why we built a custom Rust library for Capture"](https://dropbox.tech/application/why-we-built-a-custom-rust-library-for-capture); [InfoQ Magic Pocket 정리](https://www.infoq.com/articles/dropbox-magic-pocket-exabyte-storage/).
- Figma: ["Rust in production at Figma"](https://www.figma.com/blog/rust-in-production-at-figma/); ["Making multiplayer more reliable"](https://www.figma.com/blog/making-multiplayer-more-reliable/); ["Faster File Load Times with Memory Optimizations in Rust"](https://www.figma.com/blog/supporting-faster-file-load-times-with-memory-optimizations-in-rust/).
- Microsoft: ["Microsoft's Rust Bet — The New Stack"](https://thenewstack.io/microsofts-rust-bet-from-blue-screens-to-safer-code/); ["Russinovich: All-in on Rust — Thurrott"](https://www.thurrott.com/dev/317950/russinovich-microsoft-is-all-in-on-rust); ["Microsoft is rewriting core Windows libraries in Rust — The Register"](https://www.theregister.com/2023/04/27/microsoft_windows_rust/).

## 산업 사례 — 마이그레이션·후기 (Medium / DEV.to / HN)

- ["I Replaced My Spring Boot Microservice with Rust and Go" — Medium](https://medium.com/@toyezyadav/i-replaced-my-spring-boot-microservice-with-rust-and-go-heres-the-system-design-that-saved-my-f3ccedd6e494).
- ["I Rewrote A Java Microservice In Rust And Lost My Job" — Medium](https://medium.com/@noahblogwriter2025/i-rewrote-a-java-microservice-in-rust-and-lost-my-job-2c01f63ed0ca).
- Kasun Ranasinghe ["Before moving to Rust from Java" — Medium](https://keazkasun.medium.com/before-moving-to-rust-from-java-2b87a70654c0).
- ["How Discord Moved from Go to Rust" — OpenSourceScribes (Medium)](https://medium.com/sourcescribes/how-discord-moved-from-go-to-rust-ad98cf0a1d59).
- [Hacker News: Why Discord is switching from Go to Rust (2020)](https://news.ycombinator.com/item?id=26227339).
- [Hacker News: Rust in production at Figma (2018)](https://news.ycombinator.com/item?id=16977932).
- [Hacker News: Spring-rs is a microservice framework in Rust (2024)](https://news.ycombinator.com/item?id=41274138).
- [Hacker News: Ask HN — How to structure Rust, Axum, and SQLx for clean architecture?](https://news.ycombinator.com/item?id=40294092).

## 블로그·기술 매체 (개념·비교)

- [Rust Blog: "2024 State of Rust Survey Results" (2025-02)](https://blog.rust-lang.org/2025/02/13/2024-State-Of-Rust-Survey-results/).
- [Rust Blog: "Rust compiler performance survey 2025 results" (2025-09)](https://blog.rust-lang.org/2025/09/10/rust-compiler-performance-survey-2025-results/).
- [Rust Blog: "2025 State of Rust Survey Results" (2026-03)](https://blog.rust-lang.org/2026/03/02/2025-State-Of-Rust-Survey-results/).
- [Rust Blog: "Announcing async fn and RPIT in traits" (2023-12)](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/).
- [The New Stack: "Survey: Memory-Safe Rust Gains 45% of Enterprise Development"](https://thenewstack.io/survey-memory-safe-rust-gains-45-of-enterprise-development/).
- [The New Stack: "Nearly half of all companies now use Rust in production"](https://thenewstack.io/rust-enterprise-developers/).
- [JetBrains RustRover Blog: "The State of Rust Ecosystem 2025" (2026-02)](https://blog.jetbrains.com/rust/2026/02/11/state-of-rust-2025/).
- [JetBrains RustRover Blog: "The Evolution of Async Rust" (2026-02)](https://blog.jetbrains.com/rust/2026/02/17/the-evolution-of-async-rust-from-tokio-to-high-level-applications/).
- [Stack Overflow Blog: "In Rust We Trust? White House Office urges memory safety" (2024-12)](https://stackoverflow.blog/2024/12/30/in-rust-we-trust-white-house-office-urges-memory-safety/).
- [2025 Stack Overflow Developer Survey](https://survey.stackoverflow.co/2025/).
- [corrode: "Migrating from Java to Rust"](https://corrode.dev/learn/migration-guides/java-to-rust/).
- [corrode: "Flattening Rust's Learning Curve"](https://corrode.dev/blog/flattening-rusts-learning-curve/).
- [corrode: "The State of Async Rust — Runtimes"](https://corrode.dev/blog/async/).
- [Without Boats: "Why async Rust?"](https://without.boats/blog/why-async-rust/); [Without Boats: "Pin"](https://without.boats/blog/pin/); [Without Boats: "Three problems of pinning"](https://without.boats/blog/three-problems-of-pinning/).
- [fasterthanlime: "Catching up with async Rust"](https://fasterthanli.me/articles/catching-up-with-async-rust); [fasterthanlime: "Surviving Rust async interfaces"](https://fasterthanli.me/articles/surviving-rust-async-interfaces); [fasterthanlime: "Pin and suffering"](https://fasterthanli.me/articles/pin-and-suffering); [fasterthanlime: "Some mistakes Rust doesn't catch"](https://fasterthanli.me/articles/some-mistakes-rust-doesnt-catch).
- [Niko Matsakis: baby steps blog](https://smallcultfollowing.com/babysteps/).
- [Tokio Blog: "Making the Tokio scheduler 10x faster"](https://tokio.rs/blog/2019-10-scheduler).
- [Tokio Blog: "Announcing Axum"](https://tokio.rs/blog/2021-07-announcing-axum).
- [Bit Bashing: "Async Rust Is A Bad Language"](https://bitbashing.io/async-rust.html).
- [Rust for Java Developers — tkaitchuck](https://tkaitchuck.github.io/Rust4JavaDevelopers/ownership.html).
- [softwaremill: "Rust Static vs. Dynamic Dispatch"](https://softwaremill.com/rust-static-vs-dynamic-dispatch/).
- [Comprehensive Rust — Java interop (Google)](https://google.github.io/comprehensive-rust/android/interoperability/java.html).
- [jni-rs GitHub](https://github.com/jni-rs/jni-rs); [jni-rs docs](https://docs.rs/jni).
- [Tweede golf: "Mix in Rust with Java (or Kotlin!)"](https://tweedegolf.nl/en/blog/147/mix-in-rust-with-java-or-kotlin).
- [Loco.rs](https://loco.rs/); [Loco GitHub](https://github.com/loco-rs/loco); [Loco InfoQ 소개](https://www.infoq.com/news/2024/02/loco-new-framework-rust-rails/); [Loco Hello World](https://loco.rs/blog/hello-world/); ["Introducing Loco" — Shuttle](https://www.shuttle.dev/blog/2023/12/20/loco-rust-rails).
- [Leapcell: "Unpacking the Tower Abstraction Layer in Axum and Tonic"](https://leapcell.io/blog/unpacking-the-tower-abstraction-layer-in-axum-and-tonic).
- [Leapcell: "Unraveling sqlx Macros"](https://leapcell.io/blog/unraveling-sqlx-macros-compile-time-sql-verification-and-database-connectivity-in-rust).
- [Leapcell: "Building Minimal and Secure Rust Web Applications with Docker"](https://leapcell.io/blog/building-minimal-and-secure-rust-web-applications-with-docker).
- [Frankel: "Introduction to Tower"](https://blog.frankel.ch/introduction-tower/); [Frankel: "Rust and the JVM"](https://blog.frankel.ch/start-rust/7/).
- [Datadog: "How to monitor your Rust applications with OpenTelemetry"](https://www.datadoghq.com/blog/monitor-rust-otel/).
- [Phoronix: "Cloudflare Ditches Nginx For In-House, Rust-Written Pingora"](https://www.phoronix.com/news/CloudFlare-Pingora-No-Nginx).
- [Aarambh Dev Hub: "Rust Web Frameworks in 2026"](https://aarambhdevhub.medium.com/rust-web-frameworks-in-2026-axum-vs-actix-web-vs-rocket-vs-warp-vs-salvo-which-one-should-you-2db3792c79a2); [Aarambh Dev Hub: "Rust ORMs in 2026"](https://aarambhdevhub.medium.com/rust-orms-in-2026-diesel-vs-sqlx-vs-seaorm-vs-rusqlite-which-one-should-you-actually-use-706d0fe912f3).
- [Tech Tonic / Medium: "Spring Boot Webflux vs Rust (Axum)"](https://medium.com/deno-the-complete-reference/spring-boot-webflux-vs-rust-axum-hello-world-performance-28611da8bfc2).
- [JavaRevisited: "Rust vs Spring Boot vs Quarkus"](https://medium.com/javarevisited/rust-vs-spring-boot-vs-quarkus-the-performance-truth-nobody-talks-about-09941b196f8e).
- [Substack: "Goodbye Async-Std, Welcome Smol"](https://weeklyrust.substack.com/p/goodbye-async-std-welcome-smol).
- [Substack: "Tree Borrows Just Landed"](https://weeklyrust.substack.com/p/tree-borrows-just-landed).
- [BigGo News: "Rust's Learning Curve Debate"](https://biggo.com/news/202502181925_rust-learning-curve-debate).
- [byteiota: "Rust 2025 Survey: 45.5% Adoption, 41.6% Worry Complexity"](https://byteiota.com/rust-2025-survey-45-5-adoption-41-6-worry-complexity/).
- [muslrust GitHub](https://github.com/clux/muslrust); [Chainguard: "Distroless container images"](https://edu.chainguard.dev/chainguard/chainguard-images/about/getting-started-distroless/).
- [Java Code Geeks: "Memory Safety and Performance — Rust's Theoretical Edge"](https://www.javacodegeeks.com/2025/12/memory-safety-and-performance-rusts-theoretical-edge-over-traditional-languages.html).
- [Rust Magazine: "How Tokio schedules tasks — A hard lesson learnt"](https://rustmagazine.org/issue-4/how-tokio-schedule-tasks/).
- [woodruff.dev: "The Borrow Checker — Rust's Tough-Love Mentor"](https://www.woodruff.dev/the-borrow-checker-rusts-tough-love-mentor/).
- [DEV.to: "Rust ownership and borrows: Fighting the borrow-checker"](https://dev.to/daaitch/rust-ownership-and-borrows-fighting-the-borrow-checker-4ea3).
- [DEV.to / Leapcell: "Rust Error Handling Compared: anyhow vs thiserror vs snafu"](https://dev.to/leapcell/rust-error-handling-compared-anyhow-vs-thiserror-vs-snafu-2003).
- [DEV.to / Leapcell: "Rust Web Frameworks Compared: Actix vs Axum vs Rocket"](https://dev.to/leapcell/rust-web-frameworks-compared-actix-vs-axum-vs-rocket-4bad).
- [Shuttle: "A Guide to Rust ORMs in 2025"](https://www.shuttle.dev/blog/2024/01/16/best-orm-rust).

## 한국어 자료

- [한국 러스트 사용자 그룹 (rust-kr.org)](https://rust-kr.org/).
- [The Rust Programming Language 한국어판 — rinthel](https://rinthel.github.io/rust-lang-book-ko/).
- [Rust 한국어판 공식 (doc.rust-kr.org)](https://doc.rust-kr.org/).
- 김대현. ["Rust를 업무용 언어로 쓰다" — HappyProgrammer (Medium)](https://medium.com/happyprogrammer-in-jeju/rust%EB%A5%BC-%EC%97%85%EB%AC%B4%EC%9A%A9-%EC%96%B8%EC%96%B4%EB%A1%9C-%EC%93%B0%EB%8B%A4-7723cd2c0a59).
- Jinwoo Park. ["Rust를 회사 업무로 쓰고난지 5개월 정도"](https://pmnxis.github.io/posts/five_mothes_ago_from_using_rust_as_work_kr/).
- Option::None. ["4년간의 Rust 사용 후기" — blog.cro.sh](https://blog.cro.sh/posts/four-years-of-rust/).
- appleseed. ["일주일만에 Rust에 매료되다"](https://blog.appleseed.dev/post/fascinated-by-rust-in-a-week/).
- SmileCat. ["Rust 찍먹후기"](https://blog.smilecat.dev/posts/research-rust/).
- 비브로스 기술 블로그. ["웹프론트엔드 개발자의 Rust 돌려까기"](https://boostbrothers.github.io/experience/2022/03/28/rust-trun-around/).
- 이랜서 블로그. ["왜 많은 개발자들이 Rust로 이동할까?"](https://www.elancer.co.kr/blog/detail/808).
- scalalang2. ["Rust의 소유권 이야기" — CURG (Medium)](https://medium.com/curg/rust%EC%9D%98-%EC%86%8C%EC%9C%A0%EA%B6%8C-%EC%9D%B4%EC%95%BC%EA%B8%B0-a4c19c1b2c10).
- sangjinsu. ["🦀 Rust로 실전 백엔드 개발을 경험하다" (velog)](https://velog.io/@sangjinsu/Rust%EB%A1%9C-%EC%8B%A4%EC%A0%84-%EB%B0%B1%EC%97%94%EB%93%9C-%EA%B0%9C%EB%B0%9C%EC%9D%84-%EA%B2%BD%ED%97%98%ED%95%98%EB%8B%A4).
- Indo Yoon. ["실전 백엔드 러스트 Axum 프로그래밍 — 책 소개"](https://devbull.xyz/blog/axum-book).
- [한국 채용 — 디지털헬스케어 Rust 백엔드 개발자 (랠릿)](https://www.rallit.com/positions/3247/).
- [namu.wiki: Rust(프로그래밍 언어)](https://namu.wiki/w/Rust(%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%20%EC%96%B8%EC%96%B4)); [Rust(프로그래밍 언어)/비판](https://namu.wiki/w/Rust(%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%20%EC%96%B8%EC%96%B4)/%EB%B9%84%ED%8C%90).


---

# 감사의 글

이 책은 사람의 손이 아니라 *AI의 손*으로 쓰였다. 정직하게 적자. 토비(Toby)의 글쓰기 스타일과 책 저술 자동화 하네스 위에서, Claude가 챕터별로 리서치·계획·집필·편집을 거쳐 한 권으로 묶었다. 그래서 이 책의 결정과 한계는 모두 그 자동화의 결정과 한계다. 부족한 부분이 있다면 너그러이 양해해주기를 바라고, 좋았던 부분이 있다면 그 자리에 인용된 *학자들과 엔지니어들과 한국 개발자들*에게 마음의 한 줄을 보내주기를 바란다. 그분들의 글이 없었다면 이 책은 있을 수 없었다. 그리고 *이 책을 끝까지 읽어준 자네에게* 가장 큰 감사를 보낸다. 4~6개월 동안 자네가 손으로 짜 올릴 첫 8MB 컨테이너 한 개 — 그것이 이 책이 받을 수 있는 가장 좋은 응답이다.

