# 챕터 1. 왜 지금 Rust인가 — JVM 베테랑에게 보내는 초대장

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
