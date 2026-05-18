# 5장. Spring AOT: 런타임을 빌드 타임으로 옮기다

3장에서 우리는 Quarkus와 Micronaut가 어떻게 빌드 타임으로 갔는지를 보았다. 그들은 어노테이션 프로세서로 DI 코드를 처음부터 새로 짰다. 리플렉션을 쓰지 않는 새로운 자바 프레임워크의 길이었다. 그리고 4장에서는 코드 한 줄 바꾸지 않고 시작 시간을 절반 가까이 깎는 CDS의 영리함도 살펴봤다. 클래스 메타데이터를 빌드 타임에 한 번 만들어두고, 모든 운영 인스턴스가 그 결과를 공유한다.

이쯤에서 의문이 든다. CDS가 그토록 효과적이라면, 왜 굳이 Spring AOT라는 또 다른 도구가 필요할까? CDS와 Spring AOT는 무엇이 다른가? 그리고 더 본질적으로, 만약 정말 Spring AOT가 빌드 타임에서 무언가 결정적인 걸 해준다면, 그것은 도대체 무엇인가?

답을 살짝 미리 보자. CDS는 *클래스를 들고 다니기 좋게* 만든다. JVM이 매번 부팅 때 다시 파싱하던 클래스 메타데이터를 한 번 굳혀서 *재사용 가능한 형태*로 만들어둔다. 그건 자바라는 언어가 짊어진 비용 중 하나만 깎는 일이다. 클래스 로딩의 비용. 자바라는 언어 차원의 문제.

Spring AOT가 푸는 비용은 *그 위의 한 층*이다. 자바의 비용이 아니라 *Spring이라는 프레임워크의 비용*. 클래스가 다 로딩된 다음에도 Spring은 일을 한다 — 그 클래스들 중에 어떤 것이 빈인지, 어떤 어노테이션을 달고 있는지, 어떤 다른 빈에 의존하는지를 *결정하는 일*. 부팅 로그에서 "Started in 4.231 seconds"의 그 4초 중 *3초 가까이*가 이 결정에 쓰이는 앱이 적지 않다. Spring AOT는 그 결정의 비용을 다룬다.

이 챕터는 그 메커니즘을 본격적으로 들여다보려 한다. 그런데 답을 시작하기 전에, 잠깐 옆길로 새서 한 가지 짚고 가야 할 것이 있다. 시작 시간을 줄이고 싶은 개발자가 가장 먼저 손을 뻗는 옵션, 그러나 좋은 답이 아닌 옵션 하나가 있기 때문이다.

---

## 사이드바: 왜 lazy init은 답이 아닌가

Spring Boot 2.2부터 `spring.main.lazy-initialization=true`라는 프로퍼티가 들어왔다. 한 줄만 켜면 모든 `@Bean`이 첫 사용 시점에야 생성된다. 시작 시간을 가장 빠르게, 가장 직관적으로 줄이는 방법이다. 작은 앱에서는 2500ms에서 2000ms로, 약 20% 줄어든다는 보고도 있다.

매력적이지 않은가? 한 줄. 그것이면 끝이다. AOT가 어떻고, RuntimeHints가 어떻고, BeanFactory 처리기가 어떻고 — 그런 복잡한 이야기를 외울 필요 없이. 한 줄 켜는 걸로 시작 시간이 줄어든다면 그게 정답일 것 같지 않은가?

그런데 잠깐, 생각해보자. *시작 시간이 줄어든다*는 말의 의미가 정확히 무엇인지를. 빈 100개가 있다고 해보자. 게으른 초기화를 켜면 그 100개 중 첫 요청이 닿는 빈만 그 자리에서 만들어진다. 시작 시점에 만들어지지 않은 거지, *영원히* 만들어지지 않는 게 아니다. 어디선가는 누군가가 그 비용을 치러야 한다. 그 누군가가 *첫 요청을 받은 사용자*다.

이건 비용 회계의 관점에서 *비용을 0으로 만든 게 아니라 비용 주체를 바꾼 것*에 가깝다. 부팅 비용은 시스템(또는 운영자)이 부담한다. 첫 요청 비용은 *사용자*가 부담한다. lazy init은 이 둘 사이의 *비용 이전*이다. 누가 비용을 부담하는지가 바뀐다. 그리고 그 새 비용 부담자(첫 요청 사용자)가 *우리가 가장 신경 써야 하는 사람*이다.

자, 이제 그림을 다시 그려보자. 우리 앱이 컨테이너에서 돌아간다. 쿠버네티스가 readiness probe로 "준비됐냐"고 묻는다. lazy init을 켠 앱은 빈이 다 만들어지지 않았는데도 *준비됐다*고 답한다. 왜냐? HTTP 8080이 열렸으니까. probe가 검사하는 건 *포트의 응답*이지, *빈 초기화 완료*가 아니다. 그런데 첫 요청이 들어오는 순간, 그제야 한 무더기 빈이 생성되기 시작한다. 트랜잭션 매니저, 데이터소스, 세션 팩토리, 시큐리티 필터 체인. 응답이 2초, 3초 걸린다. 그동안 로드밸런서는 이 인스턴스로 트래픽을 계속 보낸다. 정상이라고 했으니까.

이게 *카나리 배포에서 가장 위험한 시점*이다. 새 버전을 5% 트래픽으로 띄웠는데, 그 5%의 첫 요청이 모두 2~3초 걸린다. 사용자 입장에서는 "사이트가 갑자기 느려졌다"는 인상을 받는다. 메트릭에서는 p99 응답 시간이 폭증한다. 자동 롤백이 트리거된다. 우리는 도대체 무엇이 잘못됐는지 추적하기 시작하는데, 정작 원인은 *시작 시간을 줄이려고 켠 lazy init*이다.

난감한 상황이다. 시작 시간을 줄이려고 켠 옵션이 *첫 요청 latency를 폭발*시켰다. 그리고 첫 요청이 가장 신경 쓰는 사용자에게 도착하는 요청이다. SLA 깨는 게 바로 거기서 일어난다.

문제는 그것만이 아니다. 빈 설정에 오류가 있다고 해보자. DataSource가 잘못된 호스트를 가리키고 있다거나, 어떤 빈이 누락된 프로퍼티를 요구하고 있다거나. 기본 동작에서는 부팅 시점에 *터진다*. fail-fast다. 부팅 로그에 빨간 글씨가 뜨고, ApplicationContext가 거부된다. 무엇이 잘못됐는지 즉시 안다. 그리고 *컨테이너가 죽고 재시작*된다. 쿠버네티스가 그 인스턴스를 unhealthy로 표시하고 다른 인스턴스로 대체한다.

이게 fail-fast의 약속이다. *틀린 설정으로 운영에 올라가지 않는다*. 잘못된 설정이 들어오는 순간, 가장 빠른 시점에, 가장 명확한 방식으로 실패한다. 그래야 사용자에게 부분적으로 망가진 서비스를 보내지 않는다.

그런데 lazy init을 켜면 어떻게 되는가? 그 빈을 처음 호출하는 *그 순간*에 터진다. 운영 1주일 뒤의 일요일 새벽 3시일 수도 있다. 평소에 안 쓰던 관리자 페이지를 누군가 누른 순간일 수도 있다. 결제 환불 같은 *낮은 빈도지만 중요한 기능*에서 처음 호출될 수도 있다. 끔찍한 일이다. 부팅 시점에 잡을 수 있었던 오류를 운영 한복판에서 만난다.

그리고 더 끔찍한 것 — *컨테이너는 죽지 않는다*. 빈 하나가 안 만들어진 게 컨테이너 헬스에는 영향을 안 준다. 일부 요청만 500 응답을 받는다. 다른 요청은 정상이다. 모니터링 대시보드에서 보면 "전반적으로 정상인데 일부 에러" 같은 잡음 패턴이 보인다. 디버깅이 *훨씬 어려워진다*. 차라리 컨테이너가 빨리 죽고 재시작됐다면 즉시 알아챘을 텐데.

그러니 lazy init은 *답이 아니다*. 정확히 말하면, 시작 시간이라는 비용을 *눈에 안 보이는 곳*으로 미루는 것이지 *없애는* 게 아니다. 그리고 그 눈에 안 보이는 곳이 하필 운영 환경의 신뢰성을 결정하는 자리다.

물론 lazy init이 완전히 쓸모없다는 말은 아니다. 개발 환경에서 매번 부팅이 답답할 때 한정으로는 합리적인 선택이다. 매번 로컬에서 앱을 띄울 때마다 6초씩 기다리느니, 그 시간에 첫 요청 살짝 느려도 코드 변경을 빠르게 검증하는 게 낫다. 또는 운영에서도, 사용자가 거의 안 쓰는 한두 개의 거대한 빈에만 `@Lazy`를 붙여 부분적으로 적용하는 것도 신중한 사용법이다. 관리자 페이지의 무거운 시각화 컴포넌트라거나, 월 1회만 도는 배치 작업의 빈이라거나. 그런 *예외적이고 명시적인 적용*은 합리적이다.

하지만 *시작 시간을 줄이는 표준 답*으로 lazy init을 운영에 들이는 것은 — 그건 이불 밑으로 쓰레기를 미는 것에 가깝다. 청소가 아니라 *숨김*이다. 그리고 숨겨진 쓰레기는 언젠가 가장 안 좋은 순간에 발견된다.

그렇다면 어떻게 해야 할까? 빈을 *덜* 만드는 게 아니라, 빈을 만드는 *그 작업 자체를 빌드 타임에 미리 끝내두면* 어떨까? 운영 시작 시점에는 그저 *결과를 로드*하기만 한다면? 부팅의 신뢰성과 fail-fast 보장은 그대로 유지하면서, *결정의 비용*만 빌드 타임으로 옮기는 길이 있다면? 그게 바로 Spring AOT가 던지는 답이다. 이불 밑으로 쓰레기를 미는 게 아니라, 쓰레기 자체를 *빌드 타임에 미리 치우는* 답.

---

## Reflection: 30년 자산을 어떻게 마이그레이션하는가

본격적인 기술 해부로 들어가기 전에, 한 챕터 안에서 잠시 사변 시간을 가지자. Spring AOT를 이해하려면 단지 "이 API가 무엇을 한다"를 읽는 것만으로는 부족하다. *왜 그 API가 굳이 그런 모양*이어야 했는지를 봐야 한다. 그리고 그것은 Spring이 짊어진 한 가지 부채에서 출발한다. 30년짜리 부채. 이름하여 **reflection**이다.

기술적인 사변이지만, 그저 사변에 그치지 않는다. *Spring이 왜 이 길을 택했나*를 알면, 같은 갈림길에서 우리 팀이 비슷한 결정을 내릴 때의 사고 틀을 얻는다. 호환성 자산과 성능 비용의 트레이드오프, 점진적 마이그레이션의 설계, 어색한 보강 작업의 정당화. 이런 것들이 다 같은 갈림길에서 다른 모습으로 나타나는 문제다.

### 리플렉션의 원죄

자바는 1995년에 태어났다. 그리고 거의 처음부터 reflection API가 있었다. `Class.forName()`, `getDeclaredMethods()`, `Method.invoke()`. 클래스를 이름 문자열로 받아서 동적으로 메서드를 호출한다. 컴파일 타임에는 존재하지 않는 클래스를 런타임에 발견하고 사용할 수 있다는 의미였다. 자바의 강한 정적 타입 시스템 위에 *동적 언어의 자유*를 한 줄 그어둔 셈이다.

이건 의도된 설계였다. 자바 설계자들은 *코드가 코드를 들여다보는* 능력을 원했다. 메타 프로그래밍. 이름으로 호출. 동적 발견. 그 능력이 있어야 진정한 의미의 프레임워크가 만들어진다고 봤다. 그리고 그 판단은 *맞았다*.

누구든 이 도구로 자기 프레임워크를 만들 수 있었다. 그래서 만들었다. JDBC 드라이버 로딩, Hibernate의 매핑, Jackson의 직렬화, JUnit의 테스트 발견. 자바 생태계의 거의 모든 굵직한 프레임워크가 이 위에 세워졌다. 이름 문자열을 받아서, 클래스를 찾고, 메서드를 호출한다. *동적*이라는 단어가 자바라는 정적 언어 안에 한 줄기 들어와 있다.

Spring은 어떤가? Spring은 *그 위에 또 한 채를 지었다*. `@Component`, `@Autowired`, `@Bean`, `@Value`. 어노테이션 하나만 붙이면 컨테이너가 알아서 인스턴스를 만들고, 의존성을 찾아 주입하고, 프록시로 감싼다. 그게 가능한 이유는 단 하나, *런타임에 reflection으로 클래스를 들여다보기* 때문이다. 그리고 그 단순한 메커니즘 위에 자바 진영의 거의 모든 엔터프라이즈 앱이 얹혔다. 30년 가까이.

여기까지는 좋다. 한 가지 단점만 빼면. 리플렉션은 *느리다*. 정확히 말하면, 리플렉션 자체가 본질적으로 느린 게 아니다. 메서드 한 번 호출하는 비용은 직접 호출보다 몇 배 비싸긴 해도, 요즘 JIT는 그것마저 인라이닝한다. 단발성 호출에서 리플렉션이 직접 호출의 10배 걸린다 해도, 그건 마이크로초 단위의 차이다. 진짜 문제는 *클래스패스를 뒤지는 작업*이다.

상상해보자. Spring Boot 앱이 부팅할 때 일어나는 일을. `@SpringBootApplication`이 트리거가 되어 클래스패스 전체를 스캔한다. JAR 50개, 클래스 5만 개. 그중 어떤 클래스에 `@Component`가 붙어 있는지 알려면 *각 클래스의 어노테이션을 모두 읽어야* 한다. 그것도 자바의 표준 reflection으로. 어노테이션 메타데이터를 파싱하고, 후보를 추리고, 다시 conditional을 평가하고, 프록시가 필요한지 판단한다. 빈 하나 만들기 전에 *수 초가 걸리는 결정의 산*이 쌓인다.

이게 다가 아니다. Spring Boot의 핵심 마법인 `@EnableAutoConfiguration`을 떠올려보자. `spring-boot-autoconfigure` JAR 안에는 *수백 개*의 `@Configuration` 클래스가 있다. 각각은 "어떤 라이브러리가 클래스패스에 있으면 어떤 빈을 자동 설정한다"는 조건부 컨피그다. JDBC 드라이버가 있으면 DataSource를, Jackson이 있으면 ObjectMapper를, Reactor가 있으면 WebFlux를. 이 *각각의 컨피그*가 부팅 때마다 평가된다. 어떤 클래스가 클래스패스에 있는지, 어떤 빈이 이미 등록됐는지, 어떤 프로퍼티가 정의됐는지 — 매번 reflection으로 답을 찾는다.

여기에 한 가지가 더 얹힌다. 이 모든 결정은 매번 부팅마다 *처음부터 다시* 일어난다. 어제 했던 결정과 오늘 할 결정이 99% 동일한데, 매번 똑같이 reflection으로 다시 답을 찾는다. 끔찍한 일이다.

비유하자면 이렇다. 매일 아침 출근할 때 *집에서 회사까지 가는 길*을 매번 처음부터 다시 계산하는 셈이다. 어제도 같은 길로 갔는데, 오늘도 같은 길로 갈 텐데, *매번 새로 지도를 펴고 경로를 그린다*. 도착하면 그 지도를 찢어버린다. 다음 날 아침에는 또 새 지도. 이상하지 않은가? 어제의 답을 *기억해뒀다가* 오늘 그대로 쓸 수도 있을 텐데.

### 30년 자산이라는 부채

자, 이제 한 발 뒤로 물러서서 Spring의 입장을 보자. 2018년이다. Quarkus와 Micronaut가 등장했다. 그들은 처음부터 다른 결단을 내렸다. *어노테이션 프로세서로 빌드 타임에 DI 코드를 생성한다*. 리플렉션을 거의 안 쓴다. 그래서 시작이 50ms다.

Spring은 못 했다. 정확히 말하면, *못 했다*기보다는 *못 한 척했다*. 왜냐?

생각해보자. Spring의 reflection 의존도가 단순히 자기 코드 안에만 있다면 호환성을 깨고 다시 쓰면 그만이다. 그런데 그게 그렇지 않다. Spring을 쓰는 *전 세계 수십만 개* 앱이 `BeanDefinitionRegistry`로 런타임에 빈을 등록한다. 자체 `BeanPostProcessor`를 만들어 reflection으로 빈 필드를 조작한다. `ApplicationContext.getBean(Class)` 같은 동적 조회를 한다. *이 모든 것이 reflection의 노출된 표면이다*.

표면이 너무 넓어졌다. Spring이 "이제부터 reflection 안 씁니다"라고 선언하는 순간, 전 세계 Spring 앱의 절반이 부팅에 실패한다. 그것은 *기술적 결단*이 아니라 *생태계 자살*이다.

이게 Spring의 30년 자산이 짊어진 부채다. 자산이 자산인 동시에 부채라는 것. *Spring을 강력하게 만든 그 동적성*이, *Spring을 느리게 만든 그 동적성*과 정확히 같은 것이다. 토비식으로 말하자면, 이건 거의 *철학적 곤란*에 가깝다. Spring은 *호환성 때문에* 빠른 시작을 포기할 것인가? 아니면 *빠른 시작을 위해* 생태계의 절반을 잘라낼 것인가?

답이 어렵다. 호환성을 깨면 — 그러니까 "Spring 7부터는 reflection 안 씁니다"라고 선언하면 — 그건 Spring이 아니라 *Spring을 닮은 다른 것*이 된다. Quarkus나 Micronaut가 이미 그 자리에 있다. Spring이 굳이 같은 자리로 가서 그들과 경쟁할 이유는 없다. 그리고 무엇보다 — *기존 사용자가 그 신버전을 안 따라간다*. 호환성을 깬 메이저 버전이 채택률 바닥을 친 사례는 자바 진영에 차고 넘친다.

반면 호환성을 그대로 두고 시작 시간 문제를 *방치*한다면? 그건 Spring이 *과거의 도구*로 남는다는 의미다. 컨테이너 시대, 서버리스 시대, 카나리 배포의 시대에 Spring을 새로 도입할 이유가 없어진다. 새 프로젝트는 모두 Quarkus나 Micronaut로 간다. 점진적 침식. 5년이면 Spring은 *레거시*가 된다.

답은 둘 중 어느 쪽도 아니었다.

한 가지 더. 이 부채는 *Spring만의 문제가 아니다*. JDK 자체도 같은 부채를 짊어지고 있다. `java.lang.reflect` 패키지는 자바 1.1부터 표준이다. 이걸 제거하면 *자바 자체가 깨진다*. JDK 진영도 이 부채를 어떻게 다룰지 오래 고민했다. JEP 471(`sun.misc.Unsafe` deprecation), JEP 376(ZGC scaling), 그리고 무엇보다 GraalVM의 closed-world는 모두 이 부채 처리의 다른 답들이다. Spring AOT의 RuntimeHints는 그중 *호환성 보존*에 가장 우선순위를 둔 답이다.

이 자리에서 잠깐 비유 하나를 떠올려보자. *유적지 보존*이다. 30년 된 도시 한복판에 낡은 건물이 있다. 그 건물이 도시 인프라의 핵심이다. 모두 그걸 거쳐 다닌다. 그러나 그 건물은 *느리고, 비효율적이고, 현대적 기준에 맞지 않는다*. 어떻게 할까?

세 가지 답이 있다. 첫째, *건물을 부수고 새로 짓는다*. Quarkus·Micronaut의 답이다. 빠르고 효율적이지만, 사람들이 *옛 건물에 정착한 가게와 추억*을 잃는다. 둘째, *그대로 둔다*. 변화 없음. 도시는 점점 낙후된다. 셋째, *외관과 핵심 구조는 유지하면서 내부 시스템을 재배선한다*. 보존과 현대화의 타협. 이게 Spring AOT의 길이다.

세 번째 길은 비싸다. 시간도 오래 걸린다. 그러나 *문화 자산을 잃지 않으면서 효율을 회복*한다. Spring 진영이 30년 자산을 그렇게 다뤘다. 라이브러리도, 책도, Stack Overflow도, 사내 표준도, 개발자 습관도 — 모두 그대로다. 다만 그 안에서 부팅 결정의 *시점*만 바뀌었다. 그게 RuntimeHints API의 풍경이다.

### 영리한 타협: 모델은 유지하고 시점만 옮긴다

Spring 팀이 내린 결단은 이렇다. *모델은 그대로 둔다. 처리 시점만 옮긴다.* 무슨 뜻인가?

`@Component`도 그대로, `@Autowired`도 그대로, `BeanPostProcessor`도 그대로다. 어노테이션 모델, BeanDefinition 모델, 라이프사이클 모델 — 모두 그대로다. 사용자 코드는 한 글자도 안 바꾼다. 그게 *모델 유지*다. 30년치 책, 강의, Stack Overflow 답변, 사내 위키, 사내 표준 — 모든 학습 자산이 그대로 유효하다. *교과서를 새로 쓸 필요가 없다*. Spring 5에서 Spring 6으로 넘어가는 마이그레이션이, 호환성을 깬 신규 프레임워크로 갈아타는 것보다 *비교할 수 없이 가벼운* 이유가 여기에 있다.

그런데 그 모델을 *언제* 처리할지를 바꾼다. 원래는 모두 런타임이었다. 부팅 시점에 클래스패스를 스캔하고, 어노테이션을 읽고, 빈을 찾고, 결정을 내린다. Spring AOT는 *그 작업의 결정 부분*만 빌드 타임으로 옮긴다. 빌드 시점에 *가상의 부팅 시뮬레이션*을 돌리고, 거기서 나온 결정들을 — 어떤 빈이 어떤 순서로 만들어져야 하는지, 어떤 메서드를 어떤 방식으로 호출해야 하는지 — *자바 소스 코드로 생성*한다.

이 분리가 우아한 이유를 한 번 더 풀어보자. 평범한 Spring 부팅은 *결정과 실행이 한 덩어리*로 묶여 있다. `refresh()`가 호출되면 그 안에서 결정도 하고 실행도 한다. 둘이 *같은 함수 안에* 있다. 이걸 떼어내는 게 쉽지 않다. 어떤 결정이 어떤 실행에 의존하는지, 그 의존성이 복잡하게 얽혀 있기 때문이다.

Spring 팀이 한 작업이 이거다. *결정과 실행을 떼어내고*, 결정만 따로 빌드 타임으로 옮겨도 동작하도록 코드 구조를 다시 짠 것. 모델은 그대로지만 *내부의 함수 분리*가 일어났다. 사용자에게는 보이지 않는 작업이다. 그러나 그 한 분리가 *부팅 시간의 70%를 빌드로 보낼 수 있게* 만든다.

런타임에는 그 생성된 코드가 *그대로 실행*된다. 클래스패스를 스캔할 일이 없다. 어노테이션을 다시 읽을 일도 없다. 그저 생성된 자바 코드의 직접 호출이 줄줄이 실행될 뿐이다. reflection은 *남아 있되, 빌드 타임에 사용되고 결과만 코드로 박힌다*.

이게 영리한 타협이다. 표면적으로는 사용자 코드와 라이브러리 호환성을 깨지 않으면서, 내부적으로는 reflection의 *부팅 시점 비용*을 거의 0으로 만든다. *재설계 없는 우회*다.

그런데 한 가지 남은 문제가 있다. 빌드 타임에 모든 reflection 결과를 코드로 박았다 해도, *런타임에 또 reflection이 필요한 경우*가 있다. 예를 들어 Jackson이 임의의 DTO를 받아 직렬화한다거나, JPA가 엔티티의 필드를 조작한다거나. 그건 사용자 코드 안의 reflection이라서 빌드 타임에 *어떤 클래스를 reflect할지* 미리 다 알 수 없다.

이 잔여 부분이 바로 **RuntimeHints**의 자리다. Spring AOT는 사용자에게 이렇게 묻는다. "런타임에 reflect할 클래스가 있으면 *미리 선언해줘*. 그러면 내가 그걸 메타데이터 JSON에 기록할게. 그 JSON을 GraalVM이 읽어서 closed-world 분석에 반영하면, Native Image도 막힘 없이 돈다." 이게 RuntimeHints API다. *reflection을 없애지는 못해도, 어디서 누구를 reflect하는지는 선언해다오*.

이 선언이 본질적으로 무엇인지를 한번 음미해보자. 그것은 *30년 동안 동적으로 결정되던 정보를, 30년 만에 정적 선언으로 끌어올리는 작업*이다. 단순한 API 추가가 아니라, 자바 생태계의 reflection에 대한 *태도 변화*다. "런타임에 결정해도 된다"에서 "런타임에 결정할 거면 미리 알려라"로의 이동.

Quarkus와 Micronaut가 한 일은 다른 의미였다. 그들은 *처음부터 reflection을 거부했다*. 자기 어노테이션 프로세서로 빌드 타임에 코드를 생성했다. 새 집을 지은 격이다. 그 집은 가볍고 빠르다. 그러나 *비어 있다*. 30년치 라이브러리와 패턴, 책과 강의, 사내 표준과 개발자의 습관 — 이 모든 것이 거기 없다. 새로 짓는 데 시간이 걸린다.

Spring이 한 일은 다르다. *낡은 집의 골조는 그대로 두되, 배선을 다시 깔았다*. 외관은 그대로다. 가구도 그대로다. 사람들이 30년 살던 그 집이다. 그러나 *전기와 수도 시스템은 빌드 타임에 미리 설계되어 들어간다*. 결과적으로 새 집과 비슷한 효율을 내지만, 그 과정에서 30년 자산이 살아 있다. 그게 RuntimeHints의 영리함이다 — 새 패러다임을 *기존 패러다임 위에 얹어* 작동시키는 타협이다.

물론 그 타협의 대가도 있다. 사용자가 RuntimeHints를 잘 선언해야 하고, 라이브러리도 자기 힌트를 제공해야 한다. 빌드 타임에 *모든 reflection 대상을 미리 알릴 수 있다*는 보장이 없다. 정적 분석으로 잡히지 않는 reflection은 여전히 남아 있다. 그래서 다음 절부터 그 메커니즘을 본격적으로 들여다본다. 그리고 그 어색한 보강 작업이 *왜 어쩔 수 없는 모양인지*를, 이 사변을 거친 독자라면 이해할 수 있을 것이다.

한 가지 더 짚어둘 점. 이 타협은 *완전한 답이 아니다*. RuntimeHints로 잡지 못한 reflection은 여전히 런타임에 일어난다. JVM 모드에서는 그래도 동작한다(JVM은 closed-world 가정을 안 하니까). 그러나 Native Image에서는 깨진다. 그래서 6장에서 closed-world의 결단을 다시 만난다. *동일한 reflection 부채가 두 가지 다른 폭으로 다뤄지는* 게 5장과 6장의 분업이다. 여기서는 *RuntimeHints로 표면적 호환성을 유지하는* 영리함을, 6장에서는 *closed-world로 동적성을 완전히 잘라내는* 결단을 본다.

---

## ApplicationContextAotGenerator: 빌드 타임의 가상 부팅

자, 사변은 여기까지. 이제 Spring AOT가 *실제로 무엇을 하는지*를 본다. 핵심 클래스 하나에서 시작한다. `ApplicationContextAotGenerator`. 이름이 거창한데, 하는 일은 이렇게 요약된다.

> "빌드 타임에 ApplicationContext를 *부팅하는 척*하면서, 그 부팅 결과를 자바 소스 코드로 받아쓴다."

이걸 좀 더 풀어보자. *부팅하는 척*이라는 표현이 핵심이다. 진짜로 부팅을 하지는 않는다. 빈을 인스턴스화하지도 않고, 외부 자원에 접근하지도 않고, 라이프사이클 콜백을 호출하지도 않는다. 그러나 *부팅이 진행됐다면 어떤 결정이 내려졌을지*를 시뮬레이션한다. 그 결정 결과를 코드로 받아쓴다. 그게 빌드 타임 AOT의 본질이다.

### refreshForAotProcessing: 인스턴스화 없는 부팅

평범한 Spring 부팅은 어떻게 일어나는가? `ApplicationContext.refresh()`가 호출된다. 이 한 줄이 사실은 *Spring의 모든 것*이 일어나는 자리다. 이 한 줄 안에서 다음과 같은 일이 *순차적으로* 일어난다.

1. 클래스패스 스캔, `@Component` 발견
2. BeanDefinition 등록
3. `@Conditional`, `@Profile` 평가로 어떤 빈이 활성화될지 결정
4. BeanPostProcessor 발견 및 적용
5. **싱글톤 빈을 실제로 *인스턴스화*하고 의존성 주입**
6. `Lifecycle.start()` 호출

5번이 핵심이다. 빈이 거기서 *진짜로 만들어진다*. DataSource가 DB에 연결하고, 톰캣 커넥터가 8080을 열고, 메트릭 컬렉터가 시작한다. 그 전까지의 1~4번은 모두 *준비 작업*이다. 결정만 한다. 실행은 5번에서.

이 분리가 우리에게 유리한 단서를 준다. 잘 보면, 1~4번은 *외부 자원이 거의 필요 없다*. 클래스패스를 읽고, 어노테이션을 해석하고, 조건을 평가하고, 의존성 그래프를 그린다. 이건 모두 *코드와 메타데이터*만으로 가능하다. 빌드 머신에서도 똑같이 할 수 있는 일이다.

그런데 빌드 타임에는 5번을 그대로 할 수 없다. DB에 연결할 수 없다. 포트를 열 수도 없다. 빌드 환경은 운영 환경이 아니니까. 빌드 머신은 운영 머신과 다른 호스트, 다른 네트워크, 다른 보안 설정 안에 있다. *인스턴스화하는 순간 모든 게 깨진다*.

그렇다면 어떻게 빌드 타임에 가상 부팅을 시뮬레이션할까? Spring 팀이 한 답이 이거다. **인스턴스화 전까지만 돌린다**. 정확히는, 1번~4번까지만 한다. 그리고 5번 직전에서 멈춘다.

이 멈춤이 `refreshForAotProcessing(hints)`다. 평범한 `refresh()`와 거의 같은 동작을 하되, *빈을 만들지는 않는다*. 빈이 어떤 클래스의 인스턴스가 되어야 하는지, 어떤 의존성을 갖는지, 어떤 BeanPostProcessor가 그 위에 적용될지 — 이 모든 *결정*은 다 한다. 그러나 *실행*은 하지 않는다.

생각해보면 영리한 분리다. 빈의 *정의*는 코드에서 정적으로 추출 가능하다. 어노테이션을 읽고, 메서드 시그니처를 보고, 어떤 조건이 평가됐는지 기억해두는 일은 클래스패스만 있으면 빌드 타임에도 똑같이 할 수 있다. 정작 외부 자원이 필요한 건 *진짜 인스턴스를 만드는 단계*뿐이다.

그래서 빌드 타임 시뮬레이션은 *결정의 단계*만 돌리고, *실행은 런타임으로 미룬다*. 그러나 런타임에서 다시 결정하지는 않는다 — 결정 결과는 이미 *코드로* 박혀 있으니까.

이 단순한 분리가 얼마나 중요한지 한 번 더 음미해보자. 평범한 Spring에서는 *결정과 실행이 한 덩어리*다. 부팅의 4초 중 결정이 3초, 실행이 1초였다면, AOT는 그 3초를 빌드 타임으로 옮긴다. 런타임에는 1초의 실행만 남는다. 빌드 타임은 어차피 한 번만 일어나는 일이다. 그 한 번의 비용으로 *수천 번의 부팅*에서 3초씩을 절약한다. 도커 이미지 한 번 빌드해서 100대 인스턴스에 배포한다면, 빌드 타임 1분이 운영의 *시간당 100 × 3초 = 5분*을 절약한다.

이게 *결정의 비용을 빌드로 옮기는* 일반적 의미다. CDS가 클래스 메타데이터의 파싱 비용을 빌드 타임으로 옮긴 것과 정확히 같은 패턴이다. 다만 CDS가 *JVM의 결정*을 옮긴 반면, Spring AOT는 *프레임워크의 결정*을 옮긴다. 두 도구가 직교한다고 했던 이유가 여기에 있다. 둘 다 결정을 빌드 타임으로 옮기는데, *옮기는 결정의 종류*가 다르다.

### 세 가지 산출물

`ApplicationContextAotGenerator`가 이 가상 부팅 끝에 남기는 산출물은 세 가지다. 하나씩 들여다보자.

**첫째, `*__BeanDefinitions.java` 형태의 생성 자바 소스.**

이게 핵심이다. 평범한 `@Configuration` 클래스인 `DataSourceConfiguration`이 있다고 해보자. 그 안에 `@Bean` 메서드가 두어 개 있다. Spring AOT는 이 클래스의 동반자(`__BeanDefinitions` 접미사)를 생성한다. 그 안에는 *완전한 자바 코드*로 다음과 같은 내용이 들어 있다.

- 각 `@Bean` 메서드를 호출하는 직접 호출 코드
- 의존성 주입을 reflection 없이 수행하는 setter/생성자 호출 코드
- `@Autowired` 필드를 어떻게 채울지에 대한 명시적 코드
- BeanPostProcessor 적용 순서

런타임에는 이 클래스가 *그냥 실행*된다. reflection도, 어노테이션 파싱도, 조건 평가도 없다. *결과만 박힌 자바 코드의 직선 실행*이다. 그게 시작 시간을 줄이는 진짜 메커니즘이다.

물론 사용자 코드의 `DataSourceConfiguration` 자체는 *그대로 남는다*. AOT는 그 옆에 동반 클래스를 하나 더 만드는 것일 뿐, 사용자 코드를 *건드리지는 않는다*. 이건 중요한 설계 결단이다. 사용자가 자기 코드를 수정 없이 AOT 모드를 켜고 끌 수 있다. 그리고 *디버깅할 때 사용자 코드를 그대로 읽을 수 있다*. 만약 AOT가 사용자 코드를 변형해버렸다면 — 즉, 컴파일 후 어떤 변환을 가했다면 — 디버거에서 보는 코드와 작성한 코드가 달라진다. 이건 디버깅 경험을 끔찍하게 만든다. 그래서 *원본은 그대로, 동반자만 추가*한다는 결단이 중요하다.

이 동반 코드는 일반 자바 파일이다. *jar에 컴파일되어 들어간다*. 빌드 결과물의 일부다. 우리가 빌드한 jar를 압축 해제해보면 `BOOT-INF/classes/` 아래에 `__BeanDefinitions` 접미사가 붙은 클래스들이 함께 들어 있다. *그게 우리 앱의 새로운 신경계*다.

**둘째, RuntimeHints JSON.**

빈 정의로 표현할 수 없는 reflection이 있다. 예를 들어 사용자가 `Class.forName("com.example.SomeDto")` 같은 코드를 어디선가 쓰고 있을지도 모른다. 또는 Jackson이 그 DTO를 reflect해서 JSON으로 직렬화할 것이다. 이런 *런타임 reflection의 대상*은 빌드 타임에 자동으로 알 수 없다. 사용자나 라이브러리가 *명시적으로 선언*해야 한다.

그 선언이 모이는 곳이 RuntimeHints다. JSON으로 직렬화되어 `META-INF/native-image/...` 디렉토리에 박힌다. GraalVM Native Image는 이 JSON을 읽어 closed-world 분석의 출발점으로 삼는다. *어떤 클래스를 reflect할 것인지, 어떤 리소스를 로드할 것인지, 어떤 프록시를 만들 것인지* — 모두 이 JSON 안에 들어 있다.

힌트 JSON의 모양은 대략 이렇다.

```json
{
  "reflection": [
    {
      "name": "com.example.MyDto",
      "allDeclaredConstructors": true,
      "allDeclaredFields": true
    }
  ],
  "resources": {
    "includes": [
      { "pattern": "config/messages_.*\\.properties" }
    ]
  },
  "proxies": [
    { "interfaces": ["com.example.MyDynamicInterface"] }
  ]
}
```

이 JSON이 빌드 결과물에 박힌다. Native Image 빌더는 이 파일을 *반드시* 읽고 분석한다. 누락된 항목은 Native 바이너리에 포함되지 않으므로, 런타임에 그 클래스를 reflect하면 *없는 메서드*로 보인다. `NoSuchMethodException`이다.

JVM 모드에서도 이 JSON은 유효하다. 다만 JVM은 closed-world 가정을 안 하기 때문에 거기서 빠진 클래스가 있어도 일단 reflection이 동작한다. 즉, *Native에서 깨질 수 있는 reflection을 JVM 모드에서 미리 잡고 싶을 때* RuntimeHints가 도움이 된다.

힌트를 잘 쓰면 *어떤 클래스가 동적으로 다뤄지는지* 한눈에 안다. 위 JSON을 보면 우리 앱은 `MyDto` 클래스를 reflect하고, `config/messages_*.properties` 리소스를 로드하고, `MyDynamicInterface`의 동적 프록시를 만든다. 이게 *우리 앱의 동적 행위 명세*다. 코드의 reflection을 일일이 추적하지 않아도, JSON 하나로 전체 동적성을 파악할 수 있다.

**셋째, `ApplicationContextInitializer`라는 진입점 클래스.**

이게 *런타임에서 가장 먼저 실행되는 새 진입점*이다. 평범한 Spring 부팅은 `SpringApplication.run(...)`에서 시작해 `refresh()`로 들어간다. AOT 모드에서는 그 사이에 이 Initializer가 끼어들어 **생성된 BeanDefinitions 코드를 등록**한다. Spring이 클래스패스를 스캔하기 *전에* 빈 정의가 이미 *코드로 박혀 있는 채로* 들어오는 것이다.

결과적으로 `refresh()`는 스캔도 안 하고, 어노테이션도 안 읽고, 거의 *순차적 호출만으로* 빈을 만들어낸다. 시작이 빨라지는 가장 직접적인 메커니즘이 바로 이거다.

이 Initializer의 발견 방식이 흥미롭다. `META-INF/spring.factories` 또는 `META-INF/spring/aot.factories`에 자동 등록되므로, 우리가 *수동으로 연결할 필요가 없다*. 빌드 타임에 AOT가 생성한 Initializer는 *이 메타파일에 자동으로 등록*된다. 런타임에 `SpringApplication`이 이 메타파일을 읽어 Initializer를 찾는다. 그래서 `-Dspring.aot.enabled=true` 플래그 하나만 켜면, 별다른 코드 변경 없이 *AOT 산출물이 전부 활성화*된다.

만약 `-Dspring.aot.enabled=false`로 끄면? 생성된 Initializer가 *발견되지 않고*, Spring은 평범한 부팅 경로로 돌아간다. 빌드 결과물에 AOT 산출물이 *들어 있긴 한데 안 쓰는* 상태가 된다. 도커 이미지에 두 모드의 산출물이 함께 들어 있어도 *런타임 플래그로 선택할 수 있다*. 운영팀이 문제가 생기면 즉시 fallback할 수 있다는 의미이기도 하다.

이 세 가지 산출물의 관계를 표로 정리해보자.

| 산출물 | 들어가는 곳 | 런타임에서 하는 일 |
|---|---|---|
| `*__BeanDefinitions.java` | 컴파일된 클래스로 jar에 포함 | reflection 없이 빈 직접 등록 |
| RuntimeHints JSON | `META-INF/native-image/...` | GraalVM이 closed-world 분석에 사용 |
| `ApplicationContextInitializer` | `SpringApplication`이 자동 발견 | refresh보다 먼저 빈 정의 주입 |

이 세 가지가 함께 굴러갈 때, *결정은 빌드 타임에, 실행은 런타임에*라는 분업이 완성된다.

### 생성된 코드를 직접 들여다보자

여기서 한 가지 권하고 싶다. Spring AOT를 처음 도입한다면, *생성된 코드를 한 번이라도 직접 열어보자*. 그것이 AOT를 *블랙박스에서 화이트박스로 전환*하는 가장 빠른 길이다.

평범한 Spring Boot 앱에 다음과 같은 컨피그가 있다고 해보자.

```java
@Configuration
public class GreetingConfiguration {

    @Bean
    public GreetingService greetingService(MessageSource messageSource) {
        return new GreetingService(messageSource);
    }
}
```

흔한 컨피그다. `MessageSource`를 주입받아 `GreetingService` 빈을 만든다. 평범한 Spring에서는 부팅 시점에 다음 일이 일어난다. 어노테이션 스캔으로 `GreetingConfiguration`을 발견. 그 클래스의 `@Bean` 메서드를 reflection으로 추출. 메서드 파라미터인 `MessageSource` 타입의 빈을 찾아 의존성 그래프 등록. 그 의존성이 먼저 준비된 다음, `greetingService` 메서드를 reflection으로 호출. 반환된 인스턴스를 빈으로 등록.

이 모든 단계가 reflection으로 일어난다. 부팅 때마다.

AOT를 켜고 빌드하면 `GreetingConfiguration__BeanDefinitions.java` 같은 파일이 생성된다. 그 안에는 대략 이런 모양의 코드가 들어 있다.

```java
public final class GreetingConfiguration__BeanDefinitions {

    public static BeanDefinition getGreetingServiceBeanDefinition() {
        Class<?> beanType = GreetingService.class;
        RootBeanDefinition beanDefinition = new RootBeanDefinition(beanType);
        beanDefinition.setInstanceSupplier(GreetingConfiguration__BeanDefinitions::getGreetingServiceInstance);
        return beanDefinition;
    }

    private static GreetingService getGreetingServiceInstance(RegisteredBean registeredBean) {
        GreetingConfiguration configBean = registeredBean.getBeanFactory()
                .getBean(GreetingConfiguration.class);
        MessageSource messageSource = registeredBean.getBeanFactory()
                .getBean(MessageSource.class);
        return configBean.greetingService(messageSource);
    }
}
```

이게 핵심이다. 보이는가? `configBean.greetingService(messageSource)`라는 *직접 메서드 호출*이 코드로 박혀 있다. reflection이 아니라 *컴파일된 자바 메서드 호출*이다. JIT가 인라이닝하기에 가장 좋은 형태다.

런타임에는 이 클래스의 정적 메서드 두 개가 호출될 뿐이다. `getGreetingServiceBeanDefinition()`이 빈 정의를 만들고, 컨테이너가 그 정의를 빈팩토리에 등록한다. 그리고 빈이 실제로 필요해질 때 `getGreetingServiceInstance()`가 호출되어 인스턴스를 만든다. *모든 단계가 정적 메서드 호출의 연쇄*다. reflection 없음. 클래스 스캔 없음. 어노테이션 파싱 없음.

이 생성된 코드를 보면 *Spring AOT가 무엇을 하는지*가 즉시 보인다. 추상적인 "결정을 빌드 타임으로 옮긴다"는 말이 *구체적인 자바 코드의 모양*으로 손에 잡힌다.

실전에서 도입할 때는 빌드 디렉토리를 한 번 열어보자. Maven은 `target/generated-sources/aot/`, Gradle은 `build/generated/aotSources/`. 거기에 우리 앱이 *AOT의 손길로 다시 쓰인 모습*이 들어 있다. 평소 우리가 작성하던 Spring 컨피그가 *명시적인 호출 코드*로 풀어진 모습. 그것을 한 번이라도 본 개발자는 깨지는 패턴을 만났을 때 디버깅이 훨씬 쉽다.

### ApplicationContext와 BeanFactory의 차이

여기서 한 가지 더 짚어두자. 우리가 흔히 *ApplicationContext*라고 부르는 것과 *BeanFactory*는 무엇이 다른가? AOT를 다루다 보면 두 용어가 함께 나오기 때문에 이 구분을 한 번 명확히 하고 가는 게 좋다.

`BeanFactory`는 *빈을 만들고 의존성을 주입하는 가장 작은 컨테이너*다. `getBean(...)` 메서드가 핵심이다. 빈을 등록하고, 찾고, 의존성을 풀고, 인스턴스를 반환한다. 그게 끝이다.

`ApplicationContext`는 *BeanFactory 위에 얹힌 모든 것*이다. 이벤트 발행, 메시지 국제화, 리소스 로딩, 환경(Environment) 추상화, 자동 구성 — 우리가 Spring Boot에서 만나는 거의 모든 기능이 여기 들어 있다. `refresh()`가 호출되는 것도 ApplicationContext다.

AOT의 핵심 처리기 이름이 `BeanFactoryInitializationAotProcessor`인 이유가 여기에 있다. 그 처리기는 *BeanFactory 레벨*에서 작동한다. 모든 빈 등록이 이 레벨에서 일어나기 때문이다. 다만 그 처리기를 *발견하고 호출하는 책임*은 `ApplicationContextAotGenerator`가 진다. 두 레이어의 분담이다.

이 구분이 왜 중요한가? *AOT 확장을 작성할 때 어느 레벨에 작용할지를 결정*해야 하기 때문이다. 빈 자체에 관여한다면 `BeanRegistrationAotProcessor`(빈 레벨)나 `BeanFactoryInitializationAotProcessor`(빈팩토리 레벨)다. 더 큰 컨텍스트 단위 동작(메시지 소스, 이벤트 발행)에 관여하는 일은 *드물지만* 가능하다. 대부분의 일반 사용자는 *빈팩토리 레벨*에서 끝난다.

### 빌드 타임 시뮬레이션이 깨지는 자리

여기서 한 가지 더 짚을 필요가 있다. 빌드 타임의 *가상 부팅*은 인스턴스화를 안 한다고 했다. 그런데 *완전히 안 하는* 게 아니다. 가상 부팅을 위해서는 일부 빈을 빌드 타임에 *진짜로* 만들어야 할 수도 있다.

예를 들어 `BeanFactoryPostProcessor`. 이 빈은 다른 빈 정의를 *수정하는* 역할이라서, 빌드 타임 시뮬레이션에서 이게 동작해야 한다. 그래서 빌드 타임에 진짜로 인스턴스화된다.

이게 무엇을 의미하는가? 우리가 작성한 `BeanFactoryPostProcessor`의 생성자나 `@PostConstruct`에서 *외부 자원에 접근하는 코드*가 있다면, 그건 빌드 타임에 깨진다. 빌드 머신이 운영 DB에 접근할 수 없으니까. 그래서 `BeanFactoryPostProcessor`는 *순수한 변환 함수*에 가까워야 한다 — 다른 빈 정의를 받아서 수정한 결과만 반환하는, 외부 의존성이 없는 코드.

같은 원리로 `Conditional`도 빌드 타임에 평가된다. `@ConditionalOnClass`나 `@ConditionalOnMissingBean` 같은 표준 조건은 클래스패스만 보면 되니 안전하다. 그러나 *사용자 정의 Condition*이 환경변수를 읽거나, DB 상태를 보거나, 외부 API를 호출한다면 — 빌드 타임에 의도와 다르게 평가된다.

이런 사정 때문에 Spring 팀은 *빌드 타임에 안전한 컨디션 작성 가이드*를 따로 두고 있다. 핵심은 "**Condition은 클래스패스와 어노테이션 메타데이터만 봐야 한다**"는 것이다. 환경에 의존하지 말라. 사용자 정의 조건을 만든다면 이 원칙을 기억해두자.

---

## 핵심 API 투어

이제 Spring AOT의 확장점을 한 바퀴 돌아보자. 이 API들은 두 종류로 갈린다. 하나는 *Spring 자체와 라이브러리들이 이미 구현해놓은 것*(우리는 그저 켜기만 하면 동작한다). 또 하나는 *우리가 직접 구현해야 하는 것*(자체 어노테이션이나 동적 빈 등록 패턴을 다룰 때).

일반 애플리케이션 개발자라면 첫 번째 카테고리만 알고 있어도 충분하다. AOT를 켜기만 하면 Spring과 주요 라이브러리들이 이미 자기 몫의 처리기를 갖고 있다. 그러나 *자체 어노테이션을 만든다*거나 *DI 컨테이너를 확장한다*거나 *공유할 라이브러리를 작성한다*면 두 번째 카테고리도 알아야 한다. 각 API를 차례대로 살펴보자.

### BeanFactoryInitializationAotProcessor

가장 큰 단위다. 이름이 길지만 의미는 단순하다. *BeanFactory 전체의 초기화 단계에서 한 번 호출되는 AOT 기여자*다.

이걸 구현하면 빌드 타임에 *내가 원하는 임의의 자바 코드*를 BeanDefinitions 생성에 끼워 넣을 수 있다. 예를 들어 "내 라이브러리는 부팅 시점에 특정 캐시를 초기화하는데, 그 초기화 코드를 빌드 타임에 미리 짜고 싶다" 같은 경우다.

```java
public class MyLibraryAotProcessor implements BeanFactoryInitializationAotProcessor {

    @Override
    public BeanFactoryInitializationAotContribution processAheadOfTime(
            ConfigurableListableBeanFactory beanFactory) {
        return (generationContext, beanFactoryInitializationCode) -> {
            // 여기서 generationContext에 자바 코드를 추가하거나
            // RuntimeHints를 등록한다.
        };
    }
}
```

`processAheadOfTime`이 빌드 타임에 호출된다. 우리가 반환하는 `BeanFactoryInitializationAotContribution`은 *코드 생성에 기여*한다. 익명 람다처럼 보이는 두 번째 람다가 실제 코드 생성 콜백이다.

이 API는 라이브러리 작성자를 위한 것이다. 일반 애플리케이션 개발자는 거의 만들 일이 없다. 그러나 Spring Data가, Spring Security가, Spring Cloud가 — 모두 이 API의 구현체를 들고 있다. 우리가 켜고 끄지 않아도 동작하는 이유다.

예를 들어 Spring Data JPA는 부팅 시점에 `@Entity` 클래스를 스캔해서 `PersistenceManagedTypes`를 구성한다. 평범한 부팅에서는 매번 클래스패스를 스캔한다. Spring Data는 자기 `BeanFactoryInitializationAotProcessor`를 통해 *빌드 타임에 이 스캔을 수행*하고, 그 결과를 자바 코드로 박아넣는다. 런타임에는 *스캔 없이* `PersistenceManagedTypes`가 이미 채워진 채로 등장한다.

같은 패턴이 Spring Security의 필터 체인 구성, Spring Boot의 auto-configuration 평가, Spring Web의 컨트롤러 핸들러 매핑에 적용된다. 각각이 *자기 영역의 부팅 결정*을 빌드 타임으로 옮기는 처리기를 들고 있다. 우리가 코드를 짜지 않아도, 이미 깔린 처리기들이 AOT를 켜자마자 작동한다. 이게 *Spring 생태계가 AOT를 받아들인 방식*이다 — 일관된 확장점을 정의하고, 각 라이브러리가 자기 책임을 진다.

### BeanRegistrationAotProcessor

이건 조금 더 좁다. *개별 빈의 등록 코드*를 생성할 때 끼어드는 기여자다. 예를 들어 "이 빈에는 특별한 생성자 인자가 있어서 직접 호출 코드를 생성하기가 까다롭다" 같은 경우, 이 프로세서로 빌드 타임에 직접 호출 코드를 짜넣는다.

```java
public class MyBeanAotProcessor implements BeanRegistrationAotProcessor {

    @Override
    public BeanRegistrationAotContribution processAheadOfTime(
            RegisteredBean registeredBean) {
        if (!registeredBean.getBeanClass().equals(MySpecialBean.class)) {
            return null;
        }
        return (generationContext, beanRegistrationCode) -> {
            // 이 빈의 등록 코드 생성에 기여
        };
    }
}
```

`@Autowired` 필드를 어떻게 채울지, `@Value`를 어떻게 해석할지를 이 단계에서 결정한다. Spring Framework 내부에서 이미 기본 구현이 동작하므로, 평범한 빈에는 우리가 손댈 일이 없다. 다만 *동적으로 생성되는 빈*이나 *특수한 팩토리 메서드*를 가진 빈은 이 API로 보강해야 할 수 있다.

이 API의 비유는 *대장간 망치*다. 큰 망치인 `BeanFactoryInitializationAotProcessor`로 전체 빈팩토리 단위의 큰 변환을 하고, 작은 망치인 `BeanRegistrationAotProcessor`로 개별 빈의 등록 코드를 세밀히 다듬는다. 대부분의 라이브러리는 큰 망치 한두 개로 충분하지만, 일부 특수한 경우는 작은 망치를 함께 쓴다.

### RuntimeHintsRegistrar

이건 *모든 Spring 개발자가 한 번쯤 만나게 될* API다. 우리가 *런타임에 reflect할 클래스*를 미리 선언하는 도구다.

```java
public class MyHints implements RuntimeHintsRegistrar {

    @Override
    public void registerHints(RuntimeHints hints, ClassLoader classLoader) {
        hints.reflection()
             .registerType(MyDto.class, MemberCategory.INVOKE_DECLARED_CONSTRUCTORS,
                                        MemberCategory.DECLARED_FIELDS);
        hints.resources()
             .registerPattern("config/messages_.*\\.properties");
        hints.proxies()
             .registerJdkProxy(MyDynamicInterface.class);
    }
}
```

`reflection()`은 reflection 대상 클래스를, `resources()`는 클래스패스 리소스 패턴을, `proxies()`는 JDK 동적 프록시 후보를 등록한다. 이 외에도 `serialization()`(자바 직렬화), `jni()`(JNI 호출 대상) 등이 있다.

이 클래스를 작성한 뒤 어떻게 *Spring AOT가 자동으로 발견*하도록 만들까? 두 가지 방법이 있다.

**방법 1: `@ImportRuntimeHints`로 어노테이션 부착.**

```java
@Configuration
@ImportRuntimeHints(MyHints.class)
public class MyConfiguration {
    // ...
}
```

`@Configuration` 클래스 옆에 `@ImportRuntimeHints`를 붙이면, AOT가 그 컨피그를 처리할 때 이 Hints 클래스도 함께 발견한다.

**방법 2: `META-INF/spring/aot.factories`에 등록.**

라이브러리 작성자라면 자기 클래스에 어노테이션을 붙일 수 없을 수도 있다. 또는 사용자 컨피그와 무관하게 *라이브러리 로딩만으로* 힌트가 적용되길 원할 수도 있다. 그럴 때 이 파일에 등록한다.

```properties
# META-INF/spring/aot.factories
org.springframework.aot.hint.RuntimeHintsRegistrar=\
com.example.mylib.MyHints
```

이 등록 방식이 *라이브러리의 책임으로 힌트를 운반하는 표준 방법*이다. 본인 라이브러리에 힌트를 부여할 때 이 패턴을 기억해두자.

여기서 한 가지 흥미로운 점. RuntimeHints는 *Native에서만 의미가 있는 게 아니다*. JVM 모드에서도 일부 의미를 가진다. 예를 들어 RuntimeHints에 등록된 클래스는 *Spring Boot의 진단 도구*가 "AOT에서 처리된 reflection 대상"으로 인식한다. 빌드 로그에 어떤 힌트가 등록됐는지 출력해주는 옵션도 있다. JVM 모드에서 RuntimeHints가 직접적으로 시작 시간을 줄이지는 않지만, *Native로 갈 때를 미리 준비하는 의미*가 있다. 운영팀이 "이 앱은 어떤 reflection을 쓰는지 알고 있다"는 명시적 선언이기도 하다.

JVM 모드 → Native Image로의 *마이그레이션 경로*를 그릴 때 이 점이 중요해진다. 처음부터 Native를 목표로 하지 않더라도 *RuntimeHints는 빌드 타임에 등록해두자*. 그러면 나중에 Native로 갈 때 *별다른 작업 없이* 그 힌트들이 GraalVM의 closed-world 분석에 그대로 쓰인다. 사전 작업이 곧 미래 자산이 되는 경우다.

### @Reflective / @RegisterReflection

좀 더 가벼운 도구다. 클래스 위에 `@Reflective`를 붙이면, AOT가 그 클래스를 reflection 대상으로 자동 등록한다. RuntimeHintsRegistrar를 작성하지 않아도 *어노테이션 하나로 끝낸다*.

```java
@Reflective
public class MyDto {
    private String name;
    private int value;
    // getters/setters...
}
```

`@RegisterReflection`은 좀 더 세밀한 제어가 가능하다. 어떤 멤버 카테고리를 reflect할지를 지정할 수 있다.

이 두 어노테이션은 *작은 도구*다. 단일 클래스에 대해 가볍게 reflection 의도를 표현할 때 쓴다. 더 복잡한 경우는 RuntimeHintsRegistrar를 쓰는 편이 낫다.

여기서 한 가지 선택의 기준을 정해두면 좋다. *단일 클래스를 reflect한다면 `@Reflective`*, *여러 클래스를 패턴으로 reflect한다면 RuntimeHintsRegistrar*. *리소스 패턴 등록이나 프록시 등록까지 필요하다면 무조건 RuntimeHintsRegistrar*. 어노테이션은 가볍고 명시적이지만 표현력이 약하다. Registrar는 무겁지만 모든 종류의 힌트를 다 등록할 수 있다.

예를 들어 자체 어노테이션 `@JsonEvent`를 만들고, 그 어노테이션이 붙은 모든 클래스를 자동으로 reflection 대상으로 등록하고 싶다면 — 그건 Registrar의 영역이다. 어노테이션 발견 로직과 등록 로직을 함께 짜야 하기 때문이다. 반면 단일 DTO 클래스에 reflection 힌트를 부여하고 싶다면 — 그 클래스 위에 `@Reflective` 한 줄이면 끝이다.

### 자주 놓치는 사실: META-INF/spring/aot.factories

라이브러리를 만든다면 이 파일이 *우리 라이브러리와 Spring AOT를 연결하는 다리*다. 다음과 같은 키들을 등록할 수 있다.

| 키 | 등록 대상 | 언제 쓰나 |
|---|---|---|
| `BeanFactoryInitializationAotProcessor` | BeanFactory 전체 기여자 | 라이브러리 전역 초기화 코드 생성 |
| `BeanRegistrationAotProcessor` | 개별 빈 기여자 | 특수 빈의 등록 코드 보강 |
| `RuntimeHintsRegistrar` | reflection·리소스 힌트 등록자 | 라이브러리가 reflect할 클래스 사전 선언 |

이 파일은 Spring Boot의 `META-INF/spring.factories`와 비슷한 자리를 차지한다. 다만 이건 *Spring AOT 전용*이다. 라이브러리 작성자는 이 파일을 *반드시* 갖춰야 자기 라이브러리가 AOT 친화적이 된다.

기억해두자. *라이브러리가 AOT 친화적이 되는 건 자동이 아니다*. 라이브러리 코드와 별개로, AOT 처리기와 힌트 등록자를 같이 패키징해야 비로소 그 라이브러리를 쓰는 앱이 빌드 타임에 빈을 정적으로 만들 수 있다. 우리가 작성한 어떤 Spring 라이브러리든, 이 파일이 없으면 AOT의 혜택을 *우리 사용자에게 줄 수 없다*.

이건 라이브러리 작성자의 *새로운 책임*이다. 옛날에는 라이브러리가 자기 코드만 깔끔하게 짜면 됐다. 사용자가 그 라이브러리를 쓰는 환경(JVM)이 모든 reflection을 자동으로 처리해줬으니까. AOT 시대에는 라이브러리 작성자가 *자기 라이브러리의 reflection 의도를 명시적으로 선언*해야 한다. 어떤 클래스를 reflect하는지, 어떤 리소스를 로드하는지, 어떤 프록시를 만드는지.

이 책임 이동은 마치 *타입 시스템이 도입될 때*의 패턴과 비슷하다. 동적 타입 언어에서 정적 타입 언어로 갈 때, 사용자는 *타입을 명시*해야 했다. 그게 처음에는 귀찮지만 결국 *코드의 명확성과 안정성*을 높인다. AOT의 reflection 선언도 마찬가지다. 처음에는 귀찮지만, 라이브러리가 *무엇을 동적으로 다루는지* 명시적으로 드러난다. 그건 라이브러리의 *문서화*이기도 하다 — RuntimeHints를 읽으면 그 라이브러리가 무엇을 reflect하는지 한눈에 안다.

---

## 자주 놓치는 사실: JVM 모드에서도 AOT는 동작한다

여기서 잠깐 멈추고, 사람들이 가장 자주 오해하는 지점 하나를 짚자.

Spring AOT를 처음 듣는 사람의 머릿속에는 보통 이런 그림이 있다. "AOT는 GraalVM Native Image를 만들 때 쓰는 거 아닌가?" *틀린 말은 아닌데*, 절반의 진실이다. Native Image 빌드 시점에 AOT가 *반드시* 호출되긴 한다. 그게 없으면 Native가 안 만들어진다. Spring Native가 GraalVM과 짝지어 가장 자주 언급되니, 둘이 패키지 딜이라고 생각하는 게 자연스럽다.

그러나 정반대 명제는 성립하지 않는다. *Native 없이도 AOT는 동작한다*. 그것도 매우 잘.

`-Dspring.aot.enabled=true` 한 줄을 평범한 JVM 실행에 더하면, AOT가 빌드 타임에 생성한 모든 코드가 JVM 부팅에 그대로 동원된다. 결과적으로 시작 시간이 *10~20% 줄어든다*. Native 같은 극적인 95% 단축은 아니지만, *코드 수정 거의 없이 한 자릿수 비율만큼이라도 깎는다*는 게 어디인가.

이건 작은 차이가 아니다. Native Image를 도입하려면 빌드 시간 1~10분, 라이브러리 호환성 검토, 트러블슈팅 학습이 모두 필요하다. GraalVM 전문성을 가진 사람이 사내에 적어도 한 명은 있어야 한다. 그리고 *운영 중 진단*이 까다롭다. JFR이 제한적이고, async-profiler 일부 기능이 안 돌아간다. 반면 JVM 모드 AOT는 *그냥 켠다*. 빌드 시간은 약간 늘지만 운영 환경은 똑같다. JFR도 그대로, JIT도 그대로, 디버깅도 그대로다. 운영팀이 기존 도구를 그대로 쓸 수 있다.

생각해보자. Native까지 안 가도 시작 시간을 깎고 싶다. 그런 워크로드가 얼마나 많은가? Lambda가 아니라 EKS 위의 백엔드 API라면, 컨테이너 재기동이 일어날 때마다 6초가 4초가 된다. 그것만으로도 카나리 배포의 안정성이 달라진다. 새 인스턴스가 더 빨리 *준비됨* 상태에 도달하면 로드밸런서가 트래픽을 더 안정적으로 분배한다. 카나리 배포 중 trough에서 한두 인스턴스가 일찍 일어나면 평균 응답 시간이 눈에 띄게 줄어든다. *Native 없는 AOT*는 그래서 의외로 강력한 첫걸음이다.

Netflix의 사례가 정확히 이 자리에 있다. 3,000개가 넘는 앱을 Spring Boot 3 + Java 17로 올렸는데, Native는 아직 채택하지 않았다. 그래도 *15% 성능 향상*을 봤다. 시작 시간과 처리량을 합쳐서. 그 15%의 상당 부분이 JVM 모드 AOT의 기여다. 5명의 플랫폼 엔지니어가 1,500개 라이브러리를 검토하면서 Native 호환성을 일일이 확인하느니, 그 시간에 JVM 모드 AOT를 *모든 앱에 일괄 적용*하는 게 ROI가 훨씬 컸다. 회사 규모로 보면 그 15%가 연간 수백만 달러의 인프라 비용 차이로 이어진다.

여기에 한 가지 흥미로운 미래도 있다. Project Leyden의 JEP 483, 514, 515가 본격적으로 들어오면 *JVM 모드 AOT + AOT cache*의 조합이 가능해진다. Spring AOT가 C단계(프레임워크 초기화)를 줄이고, AOT cache가 A·B단계(JVM 부팅·클래스 로딩)를 줄이고, JEP 515가 D단계(JIT warm-up)를 줄인다. 셋이 함께 작동하면 Spring Boot 시작이 *Native에 가까운 수준까지 단축*된다는 게 PetClinic 벤치마크의 약속이다. 그것도 closed-world 결단 없이, JVM 모드에서. 이게 10장 Leyden 챕터의 미리보기다.

기억해두자. **Spring AOT는 Native와 짝지을 수도 있지만, 단독으로도 효과가 있다.** 둘을 분리해서 생각하는 게 도입 결정에 훨씬 깔끔하다. 그리고 거의 모든 Spring Boot 3 사용자에게 *첫 시도*로 권할 수 있는 안전한 옵션이다. 사내에 Native를 도입할 만한 자원이 없어도, JVM 모드 AOT는 거의 비용 없이 켤 수 있다. 그 단순한 진입이 *시작 가속의 첫 단계*다.

---

## 깨지는 패턴 갤러리

자, 이제 즐거운 시간이다. *AOT를 켰을 때 무엇이 깨지는가*를 한 바퀴 둘러보자. 깨지는 패턴을 미리 알면 도입 결정도, 코드 정리도 훨씬 수월하다.

패턴 갤러리에서 우리가 둘러볼 것은 *AOT의 정적 분석을 좌절시키는 코드 패턴*들이다. 이런 패턴은 평범한 Spring에서는 잘 동작한다. 그래서 우리는 *알면서도, 모르면서도* 이런 코드를 쓴다. AOT를 켜는 순간 비로소 그것들이 정체를 드러낸다.

각 패턴마다 *어떻게 깨지는지*와 *어떻게 고치는지*를 짝으로 본다. 이 갤러리를 한 바퀴 돌고 나면, 우리 코드 베이스 안의 어떤 패턴이 AOT의 적인지 *직관적으로* 알게 된다.

### 패턴 1: 런타임 BeanDefinitionRegistry로 동적 빈 등록

다음과 같은 코드를 본 적 있는가? 사내 프로젝트에서 한 번쯤 봤을 가능성이 높다.

```java
@Component
public class DynamicBeanRegistrar {

    @Autowired
    private GenericApplicationContext context;

    @PostConstruct
    public void register() {
        if (System.getenv("ENABLE_FEATURE_X") != null) {
            context.registerBean("featureXService", FeatureXService.class);
        }
    }
}
```

런타임에 환경변수를 보고 빈을 동적으로 등록한다. 평범한 Spring에서는 잘 돌아간다. 부팅 중 `@PostConstruct`가 호출되고, 그때 환경변수를 보고 빈을 등록한다. 다른 빈이 그걸 `@Autowired`로 받아갈 수 있다. *그러나 AOT에서는 망한다*. 왜?

빌드 타임에 AOT가 가상 부팅을 돌릴 때, `@PostConstruct`는 호출되지 않는다(인스턴스화가 없으니까). 따라서 빈 정의 그래프에는 `featureXService`가 등장하지 않는다. 빌드 결과물의 BeanDefinitions 코드에 그 빈에 대한 등록 코드가 *없다*. 그런데 런타임에 그 빈을 누가 `@Autowired`로 받아 쓰려고 하면? *빈을 찾을 수 없다*고 터진다.

이런 패턴은 `ImportBeanDefinitionRegistrar`로 옮기는 편이 낫다. 그러면 빌드 타임의 가상 부팅에서도 평가되고, 빈 정의 그래프에 등장한다.

```java
public class FeatureXRegistrar implements ImportBeanDefinitionRegistrar {

    @Override
    public void registerBeanDefinitions(
            AnnotationMetadata metadata, BeanDefinitionRegistry registry) {
        // 빌드 타임에 평가됨 — 다만 환경변수에 기반하면 안 됨, 다음 패턴 참조
        registry.registerBeanDefinition("featureXService",
                BeanDefinitionBuilder.genericBeanDefinition(FeatureXService.class)
                                     .getBeanDefinition());
    }
}
```

한 가지 더 짚을 점. 위의 환경변수 기반 분기는 *그 자체로* 또 다른 문제가 있다. `ImportBeanDefinitionRegistrar`로 옮기는 순간, 환경변수 평가도 *빌드 타임*에 일어난다. CI 빌드 머신의 환경변수가 빈 등록 여부를 결정하게 된다. 운영과 빌드 환경이 다르다면 의도와 다른 결과가 나온다. 이건 패턴 3과 함께 묶어서 이해해야 한다 — *동적 결정 자체를 빌드 타임 친화적인 형태로 다시 설계*해야 한다.

### 패턴 2: 인터페이스 리턴 타입의 `@Bean`

다음 코드는 흔한 패턴이다.

```java
@Configuration
public class DataConfig {

    @Bean
    public DataSource dataSource() {
        return new HikariDataSource(/* ... */);
    }
}
```

리턴 타입을 인터페이스로 선언했다. 빈은 실제로 `HikariDataSource`인데, 메서드 시그니처는 `DataSource`만 약속한다. 평범한 Spring에서는 reflection으로 *실제 인스턴스의 클래스*를 들여다보고 알아낸다.

AOT에서는 *난감하다*. 빌드 타임에는 인스턴스가 없으니, 시그니처만 본다. 그러면 빈의 실제 타입은 `DataSource`로 *추정*된다. 만약 다른 곳에서 `@Autowired HikariDataSource`로 주입받으려고 했다면 — 빈을 못 찾는다.

해결책은 단순하다. *구체 타입을 리턴하라*.

```java
@Bean
public HikariDataSource dataSource() {
    return new HikariDataSource(/* ... */);
}
```

이렇게 하면 AOT가 빈의 정확한 타입을 빌드 타임에 안다. 인터페이스 의존성 주입도 정상적으로 매칭된다.

물론 인터페이스로 리턴하고 싶은 정당한 이유가 있을 수 있다. 추상화 의도, 테스트 더블 교체. 그런 경우에는 `@Bean`에 `Class<?>` 정보를 명시적으로 주는 다른 우회법을 써야 한다. 하지만 대부분의 경우, 그냥 구체 타입으로 리턴하는 게 *훨씬 낫다*.

### 패턴 3: 환경변수 기반 `@Profile`

```java
@Configuration
@Profile("payment-${PAYMENT_PROVIDER}")
public class PaymentConfig {
    // ...
}
```

환경변수 `PAYMENT_PROVIDER`가 `stripe`이면 `payment-stripe` 프로파일이 활성화된다. 평범한 Spring에서는 런타임에 환경변수를 읽어 프로파일을 결정한다.

AOT에서는 *빌드 타임에 환경변수를 읽는다*. 그게 무엇을 의미하는가? **빌드 머신의 환경변수가 운영 환경에 박힌다.** CI 빌드 서버의 `PAYMENT_PROVIDER`가 `dev`였다면, 운영에 배포된 jar에는 `payment-dev` 프로파일이 영구적으로 결정되어 있다. 끔찍한 일이다.

해결책은 두 가지다.

첫째, *프로파일을 빌드 타임에 고정*하고 받아들인다. 즉, 같은 코드 베이스에서 환경별로 다른 빌드를 한다. 빌드 시점에 `-Dspring.profiles.active=production`을 주는 식이다. CI 파이프라인이 복잡해지지만 결정적이다.

둘째, *프로파일 결정 자체를 코드 안으로* 옮긴다. 환경변수를 읽어서 빈을 분기시키는 로직을 `@Conditional` 어노테이션이 아닌 *명시적인 자바 코드*로 다시 쓴다. 가독성은 조금 떨어지지만, 빌드 타임 결정에서 완전히 독립할 수 있다.

어느 쪽이든 *환경변수 기반 동적 프로파일*은 AOT의 적이다. 미리 정리해두는 편이 낫다.

### 패턴 4: 람다·메서드 레퍼런스로 빈 supplier 등록

```java
@Bean
public Supplier<MyService> myServiceSupplier(SomeDep dep) {
    return () -> new MyService(dep, configValue);
}
```

빈을 람다 형태의 supplier로 등록한다. 평범한 Spring에서는 그대로 동작한다. *AOT는 람다의 본문을 정적으로 분석하지 못한다*. 람다는 익명 합성 클래스이고, 그 합성 클래스의 닫힘 변수(closure)에 대한 정보를 빌드 타임에 추출하기 까다롭다.

결과: 빌드 실패 또는 런타임에 빈이 잘못 만들어진다.

해결책은 *명시적인 클래스로 변경*하는 것이다.

```java
@Bean
public MyServiceSupplier myServiceSupplier(SomeDep dep) {
    return new MyServiceSupplier(dep, configValue);
}

static class MyServiceSupplier implements Supplier<MyService> {
    private final SomeDep dep;
    private final String configValue;

    MyServiceSupplier(SomeDep dep, String configValue) {
        this.dep = dep;
        this.configValue = configValue;
    }

    @Override
    public MyService get() {
        return new MyService(dep, configValue);
    }
}
```

코드가 길어진다. 그런데 *빌드 타임에 정적으로 분석할 수 있는 명시적 코드*가 된다. AOT가 친화적이고, *읽기에도 의외로 명확하다*. 람다는 짧지만 닫힘 변수를 숨긴다 — 명시적 클래스는 길지만 모든 의존성이 생성자에 드러난다.

### 패턴 5: 클래스패스의 임의 리소스 로딩

다음 코드를 본 적 있는가?

```java
@Component
public class TemplateLoader {

    public String loadTemplate(String name) {
        try (InputStream in = getClass().getResourceAsStream(
                "/templates/" + name + ".html")) {
            return new String(in.readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```

`getResourceAsStream`으로 클래스패스에서 동적으로 리소스를 로드한다. 평범한 JVM에서는 잘 돈다. *Native Image에서는 그 리소스가 바이너리 안에 포함되지 않는다*. 빌드 타임에 어떤 리소스가 필요할지 알 수 없으니, GraalVM은 *명시적으로 등록된 리소스만* 바이너리에 포함시킨다.

JVM 모드에서는 이 패턴이 깨지지 않는다. 그러나 Native까지 갈 거라면 RuntimeHints로 미리 선언해야 한다.

```java
public class TemplateHints implements RuntimeHintsRegistrar {
    @Override
    public void registerHints(RuntimeHints hints, ClassLoader classLoader) {
        hints.resources().registerPattern("templates/.*\\.html");
    }
}
```

`@ImportRuntimeHints(TemplateHints.class)`까지 어딘가에 붙이면 끝이다. 단순한 작업이지만, *잊어버리기 쉬운 작업*이기도 하다. 보통 Native 빌드 후 런타임에 `Resource not found` 예외가 떠야 알아챈다.

### 패턴 6: ObjectMapper로 임의 DTO 직렬화

```java
@Service
public class EventPublisher {

    private final ObjectMapper objectMapper;

    public void publish(Object event) {
        String json = objectMapper.writeValueAsString(event);
        // ...
    }
}
```

`publish` 메서드에 어떤 객체든 들어올 수 있다. Jackson은 그 객체의 클래스를 reflect해서 필드를 JSON으로 직렬화한다. 평범한 JVM에서는 잘 돌고, *Spring Boot가 자기 빈으로 등록한 DTO들*은 자동으로 힌트가 잡힌다(Spring Boot가 알아서 처리한다). 그러나 *컨트롤러나 빈을 거치지 않는 익명 DTO*가 있다면 Native에서 깨진다.

예를 들어 이런 코드.

```java
public void publishUserLogin(String userId, Instant timestamp) {
    var event = new Object() {
        public final String type = "user.login";
        public final String user = userId;
        public final Instant time = timestamp;
    };
    publish(event);
}
```

익명 클래스로 즉석 객체를 만들어 publish한다. Native에서 이 클래스의 필드를 Jackson이 reflect하려면 *그 익명 클래스를 RuntimeHints에 등록*해야 한다. 그런데 익명 클래스는 이름이 없으니 RuntimeHints에 명시적으로 등록하기도 까다롭다.

*해결책은 익명 클래스를 명시적인 클래스로 바꾸는 것*이다. 그게 단순하고 명확하다.

```java
public record UserLoginEvent(String type, String user, Instant time) {
    public static UserLoginEvent of(String userId, Instant timestamp) {
        return new UserLoginEvent("user.login", userId, timestamp);
    }
}
```

`record`로 깔끔하게 정리되고, 필요하면 `@Reflective`를 붙여 힌트로 등록한다. 코드는 짧아지고 AOT 친화적이 된다.

### 패턴 갤러리의 메시지

위 여섯 가지 패턴을 한 줄로 요약하면 이렇다.

> **AOT는 *빌드 타임에 정적으로 분석할 수 있는 코드*를 좋아한다. 동적인 결정, 환경변수 의존, 람다·익명 클래스, 인터페이스 리턴, 임의 리소스 로딩 — 정적 분석을 어렵게 만드는 모든 것이 적이다.**

생각해보면 이건 *코드 품질 관점에서도 좋은 신호*다. 환경변수를 어노테이션에 박는 것보다 코드 안에서 명시적으로 처리하는 게 읽기 쉽다. 람다보다 명시적 클래스가 의존성 추적이 쉽다. 인터페이스 리턴보다 구체 타입이 IDE 친화적이다. 익명 객체보다 record가 도메인 의미를 더 잘 담는다. AOT를 *코드 정리의 명분*으로 삼는 사용자도 적지 않다. "AOT 친화적으로 리팩토링해야 한다"는 핑계로 사내 정리할 코드를 정리하는 셈이다.

또 한 가지. 이 패턴들의 *공통된 본질*은 결국 *컴파일 타임에 알 수 있는 정보를 더 많이 드러내는 것*이다. 인터페이스 리턴 `@Bean`이 깨지는 이유는 *구체 타입이 컴파일 타임에 숨겨졌기 때문*이다. 환경변수 `@Profile`이 깨지는 이유는 *프로파일 이름이 컴파일 타임에 결정되지 않기 때문*이다. 람다 supplier가 깨지는 이유는 *닫힘 변수가 명시적이지 않기 때문*이다. 패턴이 다 달라 보이지만 결국 *컴파일 타임 정보의 부족*이라는 한 가지 원인이 다른 모양으로 나타난 것이다.

이 본질을 한 번 잡으면, 새로운 깨지는 패턴을 만났을 때도 *왜 그게 깨지는지*를 빠르게 추론할 수 있다. "이 코드는 컴파일 타임에 결정될 수 없는 어떤 정보를 갖고 있나?"라는 질문 한 줄이면 된다.

물론 모든 코드를 이렇게 갈아엎으라는 말은 아니다. *우선은 AOT를 켜보고 무엇이 깨지는지를 본 다음*, 깨진 곳만 차근차근 정리하면 된다. 빌드 실패 메시지는 의외로 친절하다. 어떤 빈에서, 어떤 결정이, 왜 정적으로 풀리지 않는지를 명확하게 말해준다. 처음 한두 번 빌드 실패를 정리하다 보면, *우리 코드의 어떤 패턴이 AOT 친화적이지 않은지*에 대한 감각이 생긴다. 그 감각이 생기면 그 다음부터는 새 코드를 쓸 때 자연스럽게 AOT 친화적으로 짜게 된다.

---

## Stage 1: 한 스프린트, 코드 약간

자, 이제 도입 가이드 단계로 간다. 4장 끝에서 Stage 0(CDS)을 봤다. 코드 0줄로 시작 시간을 15~30% 깎는 첫걸음. 그 다음 단계가 Stage 1, Spring AOT다.

이 단계는 *한 스프린트 정도 걸린다*. 그리고 코드 수정도 약간 필요하다. 그러나 그 수정은 거의 *코드 정리에 가까운 작업*이므로 부담은 크지 않다.

### 1단계: AOT를 켜본다

가장 먼저, *그냥 켠다*. Maven이라면 `spring-boot-maven-plugin` 설정에서 AOT를 활성화한다.

```xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <executions>
        <execution>
            <id>process-aot</id>
            <goals>
                <goal>process-aot</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

Gradle이라면 `org.springframework.boot` 플러그인에 이미 AOT 태스크가 들어 있다. `./gradlew processAot`이면 된다.

그리고 실행 시 `-Dspring.aot.enabled=true`. 이게 끝이다.

### 2단계: 빌드 결과를 살펴본다

`processAot`이 끝나면 `build/generated/aotSources/`(Gradle) 또는 `target/generated-sources/aot/`(Maven) 디렉토리에 생성된 소스가 떨어진다. *직접 들여다보자*.

이상한 일이 아니다. 이 코드는 *우리 코드*다. 빌드 타임에 Spring이 우리 컨피그를 시뮬레이션해서 만들어낸 결과물이다. 무엇이 생성되는지를 한 번이라도 본 사람과 안 본 사람은 AOT에 대한 이해도가 다르다. 마치 *어셈블리 코드를 한 번도 안 본 C 개발자*와 *디스어셈블러로 자기 코드의 결과를 본 적 있는 C 개발자*가 같은 코드를 보면서 다른 깊이의 이해를 갖는 것과 비슷하다.

처음 보면 길고 복잡해 보일 수 있다. 그러나 패턴은 단순하다. 우리가 작성한 각 `@Configuration` 클래스마다 `__BeanDefinitions` 동반자가 생긴다. 그 안에는 빈 등록 코드가, reflection 없는 직접 호출로 작성되어 있다. *내 코드가 이렇게 풀어지는구나*라는 감각을 한 번 얻으면, 깨지는 패턴을 만났을 때도 디버깅이 훨씬 쉽다.

추천하는 연습이 있다. *작은 Spring Boot 앱 하나*를 만들어, 빈을 두어 개만 등록하고, AOT를 켜고 빌드해보자. 생성된 코드를 *전부* 읽어보자. 100줄도 안 된다. 우리가 작성한 `@Configuration` 클래스 하나가, AOT의 손길로 어떤 모양이 됐는지를 한눈에 본다. 그 한 번의 작업이 *AOT에 대한 직관*을 가장 빠르게 만든다.

### 3단계: 빌드 실패하면 패턴 갤러리를 펼쳐본다

빌드가 한 번에 깔끔하게 끝나면 좋겠지만, 실전에서는 *대개 그렇지 않다*. 어딘가에서 깨진다. 위에서 본 네 가지 패턴 중 하나, 또는 우리가 모르는 어떤 라이브러리의 reflection.

당황하지 말고 에러 메시지를 본다. Spring AOT의 빌드 실패 메시지는 의외로 자세하다. 어떤 빈에서, 어떤 결정이, 왜 풀리지 않는지를 말해준다. 그것을 들고 패턴 갤러리를 펼친다.

가장 흔한 두 가지 작업이 있다.

첫째, *깨지는 코드를 정리*한다. 인터페이스 리턴 `@Bean`을 구체 타입으로, 람다 supplier를 명시적 클래스로, 환경변수 `@Profile`을 빌드 타임 고정 또는 명시적 코드로.

둘째, *RuntimeHints를 추가*한다. 우리 코드의 어딘가에서 `Class.forName()`이나 `ObjectMapper.readValue()`로 임의의 DTO를 다룬다면, 그 DTO를 RuntimeHintsRegistrar로 사전 등록한다.

이 정리 작업이 끝나면 우리 코드는 *예전보다 깨끗해진다*. 환경변수에 묶인 결정이 코드 안으로 들어오고, 동적 빈 등록이 명시적 등록으로 바뀌고, 람다가 추적 가능한 클래스가 된다. AOT를 켠 진짜 보너스다.

### 4단계: 측정하고 비교한다

이제 AOT 켠 빌드와 안 켠 빌드의 시작 시간을 *측정*해본다. 측정 방법은 12장에서 자세히 다루겠지만, 가장 간단히는 다음과 같다.

```
# AOT 꺼짐
java -jar app.jar
# 콘솔: Started MyApplication in 4.231 seconds (process running for 4.512)

# AOT 켜짐
java -Dspring.aot.enabled=true -jar app.jar
# 콘솔: Started MyApplication in 3.486 seconds (process running for 3.715)
```

대략 15~20% 단축이 일반적이다. 앱마다 다르다. 빈이 많고 reflection이 많은 앱일수록 효과가 크다. 단순한 CRUD API는 효과가 작을 수 있다. *수백 개 자동 구성이 활성화된 풀스택 Spring Boot 앱*은 효과가 가장 크다.

여기서 한 가지 주의. 단발성 측정은 *오해의 여지가 크다*. 첫 번째 실행은 JIT warm-up과 OS 캐시 효과가 섞인다. 자바 부팅 시간 측정의 *영원한 함정*이다. 적어도 10회 반복, 워밍업 2회 후 중앙값을 취한다. 자세한 방법은 12장으로.

측정 결과 외에 *부팅 로그를 함께 본다*. AOT가 잘 처리됐다면 부팅 로그에 다음과 비슷한 줄이 보인다.

```
Application starting (AOT mode enabled)
```

또는 디버그 로그를 켜면 *얼마나 많은 빈이 AOT로 처리됐는지* 통계도 볼 수 있다. 빈 100개 중 95개가 AOT로 처리되고 5개가 fallback이라면, 그 5개가 *AOT 친화적이지 않은 빈*이다. 그 다섯 개를 정리하면 추가로 시작 시간을 더 깎을 수 있다.

### 5단계: 운영 배포

AOT 켜진 빌드가 CI에서 안정적으로 통과하고, 측정 결과가 만족스러우면, 운영에 올린다. JVM 옵션 한 줄(`-Dspring.aot.enabled=true`)이 추가될 뿐이다. 운영 환경이 바뀌는 건 *시작 로그 줄과 시작 시간*뿐이다.

그리고 *CDS와 함께 켠다*. AOT는 C단계를 줄이고, CDS는 A·B단계를 줄인다. 둘은 직교다. 둘 다 켜면 *둘의 효과가 더해진다*. Spring Boot 3.3부터는 CDS 통합도 깔끔하므로, 빌드 파이프라인에 동시에 들어가는 게 자연스럽다.

도커 이미지 빌드 단계에서 둘을 함께 처리하는 패턴을 살펴보자.

```dockerfile
# 1단계: 빌드와 훈련
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app
COPY . .
RUN ./gradlew bootJar  # AOT 처리 포함
RUN java -Dspring.aot.enabled=true \
         -XX:ArchiveClassesAtExit=/app/app.jsa \
         -Dspring.context.exit=onRefresh \
         -jar build/libs/app.jar

# 2단계: 운영 이미지
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=builder /app/build/libs/app.jar .
COPY --from=builder /app/app.jsa .
ENTRYPOINT ["java", "-Dspring.aot.enabled=true", \
            "-XX:SharedArchiveFile=app.jsa", \
            "-jar", "app.jar"]
```

빌드 단계에서 두 가지가 일어난다. Gradle의 `bootJar`가 AOT 처리를 포함해 jar를 만든다(`process-aot` 태스크가 자동 실행된다). 그리고 그 jar를 *한 번 띄워서 빈 초기화까지 돌리고* CDS 아카이브를 생성한다. `-Dspring.context.exit=onRefresh`가 `refresh()` 직후 종료를 트리거하므로, 실제 트래픽을 받지 않고도 CDS 아카이브가 만들어진다.

운영 단계에서는 두 산출물을 함께 로드한다. `app.jar`에는 AOT가 생성한 BeanDefinitions 코드가 들어 있고, `app.jsa`에는 CDS가 미리 처리한 클래스 메타데이터가 들어 있다. 부팅 시 둘 다 *읽기 전용 매핑*으로 메모리에 올라간다. JVM은 클래스 메타데이터를 다시 파싱하지 않고, Spring은 빈 정의를 다시 결정하지 않는다.

이렇게 Stage 1이 끝난다. 코드 정리 약간, 빌드 설정 변경 약간. 그리고 시작 시간이 10~20% 더 짧아진 앱. CDS까지 함께 켜면 *합쳐서 30~50% 단축*도 가능하다. *Native 없이도 이 정도의 효과를 보는 게 Spring AOT의 진짜 매력*이다.

### 도입 시 자주 묻는 질문 몇 가지

처음 도입할 때 흔히 나오는 의문 몇 가지를 정리해두자.

**Q. 개발 환경에서도 AOT를 켜야 하나?**

권하지 않는다. AOT를 켜면 빌드 시간이 늘어난다(작은 앱에서 3~5초 추가, 큰 앱에서 30초 이상). dev loop이 늦어진다. 개발 환경은 평범한 부팅으로 두고, AOT는 CI 빌드와 운영 빌드에만 적용하는 편이 낫다. Spring Boot의 `bootRun` 태스크는 기본적으로 AOT를 안 거치므로 이 분리가 자연스럽다.

다만 *AOT 친화성을 빠르게 검증*하고 싶을 때는 개발 환경에서도 한 번씩 켜보는 게 좋다. AOT를 안 켜고 짠 코드가 운영 빌드에 처음 들어가서야 깨지면 그제야 정리 작업이 시작된다. 그것보다는 *주기적으로* 개발 환경에서도 AOT 빌드를 돌려서 깨지는 패턴을 일찍 발견하는 편이 낫다.

**Q. 모든 모듈을 한꺼번에 AOT 켜야 하나?**

그럴 필요 없다. AOT는 *앱 단위*로 켠다. 멀티 모듈 프로젝트라면 각 부팅 가능한 앱(Spring Boot 메인 클래스를 가진 모듈)에서 개별적으로 켤지 결정한다. 라이브러리 모듈은 AOT 자체를 켜지 않지만, *AOT 친화적으로 작성*되어야 한다(`META-INF/spring/aot.factories`와 RuntimeHintsRegistrar 제공).

**Q. AOT 켰는데도 시작 시간이 거의 안 줄어든다. 왜?**

세 가지 가능성이 있다. 첫째, *애초에 C단계 비용이 크지 않은 앱*이다. 단순한 CRUD API에 빈이 30개 정도라면 AOT의 효과는 미미하다. 빈이 수백 개, auto-configuration이 많이 활성화된 거대한 앱일수록 AOT 효과가 크다. 둘째, *측정이 잘못됐다*. 첫 실행만 측정하면 OS 캐시 효과로 두 번째부터의 측정과 다른 값이 나온다. 셋째, *AOT가 잘 동작하지 않는 빈이 많다*. 이런 경우 빌드 로그에 "could not be processed for AOT" 같은 경고가 뜬다. 그 경고들을 정리하는 만큼 효과가 늘어난다.

**Q. AOT 켠 앱과 안 켠 앱이 동작이 다를 수 있나?**

이론상 *동일*해야 한다. 그게 Spring 팀의 약속이다. 그러나 실전에서는 *극히 드물게* 차이가 난다. 보통 그 차이는 위의 패턴 갤러리에서 본 깨지는 패턴들이 미묘하게 다른 결과를 내는 경우다. 예를 들어 환경변수 기반 `@Profile`이 빌드 타임에 평가되어 *다른* 빈이 활성화되는 식. 운영에 올리기 전 *반드시 통합 테스트를 한 번 더 돌리는* 게 안전하다. AOT 켜진 빌드로.

**Q. AOT 빌드가 실패한다. 어디서 시작해야 하나?**

Spring AOT의 빌드 실패 메시지는 자세하다. "Failed to process bean 'xxx'" 같은 메시지를 찾는다. 그 빈의 정의를 보고, 패턴 갤러리에서 본 패턴 중 하나에 해당하는지 확인한다. 90% 이상의 경우 패턴 갤러리에서 답이 나온다. 나머지 10%는 보통 *라이브러리 호환성 문제*다. 그 라이브러리가 AOT 친화적이지 않은 경우다. 그럴 때는 라이브러리 버전을 올려보거나, 해당 라이브러리의 GitHub 이슈를 확인한다. Spring 생태계의 주요 라이브러리는 대부분 AOT 호환성이 갖춰져 있다.

**Q. 어떤 라이브러리가 AOT 호환되는지 어떻게 확인하나?**

Spring 생태계 안의 라이브러리 — Spring Data, Spring Security, Spring Cloud, Spring Web — 는 모두 AOT 호환된다. 핵심 빈에 대한 처리기를 자기 패키지에 들고 있다. 외부 라이브러리는 *그 라이브러리의 GitHub 리포지토리에서 RuntimeHints 클래스 또는 `META-INF/spring/aot.factories` 파일을 검색*해보면 된다. 있으면 호환. 없어도 단순한 빈 사용은 동작할 수 있지만, *reflection을 적극적으로 쓰는 라이브러리*라면 위험하다. Hibernate, Jackson, MyBatis 같은 대형 라이브러리는 자체 힌트 등록자를 들고 있다. 무명 사내 라이브러리나 오래된 오픈소스라면 직접 RuntimeHintsRegistrar를 작성해야 할 수도 있다.

**Q. AOT 효과를 *지속적으로 모니터링*하려면?**

도입 직후에는 시작 시간이 줄어들지만, 시간이 지나면서 새 코드가 추가되고 라이브러리가 업데이트되면서 *AOT 효과가 미세하게 변한다*. 그래서 시작 시간을 *지속적인 메트릭으로* 관리하는 게 좋다.

가장 단순한 방법은 부팅 로그에서 "Started ... in X.YYY seconds"를 *프로메테우스 메트릭*으로 익스포트하는 것이다. Spring Boot Actuator의 `application_started_time_seconds` 메트릭이 이미 있다. 이걸 Grafana 대시보드에 띄워두면, 매 배포 직후 *시작 시간의 변화*가 보인다. 어느 날 갑자기 시작 시간이 1초 늘었다면 무언가 바뀐 거다. 새 라이브러리 추가, 빈 등록 증가, 또는 AOT가 잘 안 풀린 컨피그.

이 메트릭을 운영 SLO의 일부로 잡는 팀도 있다. "시작 시간 p99가 3초 이하"라는 식이다. 시작 시간이 그 임계를 넘으면 알람이 울린다. 이런 운영 패턴까지 가면 *시작 시간이 더 이상 한 번 측정하고 잊는 값*이 아니라 *지속적으로 관리하는 운영 지표*가 된다. 그게 클라우드 시대 자바의 새 표준이라고 봐도 좋다.

---

## 마무리

이번 챕터에서 우리는 Spring AOT가 *정확히 무엇을 빌드 타임에 해주는지*를 보았다. 한 줄로 요약하면 이거다.

> **빈을 만드는 결정은 빌드 타임에, 실행은 런타임에.**

원래 Spring이 부팅 때마다 매번 새로 하던 결정들 — 클래스패스 스캔, 어노테이션 해석, 조건 평가, 빈 의존성 결정 — 이 작업이 빌드 타임에 *단 한 번* 일어나고, 그 결과가 자바 소스 코드로 박힌다. 런타임에는 그 코드가 *그대로 실행*된다. reflection 비용도, 스캔 비용도, 결정 비용도 0이 된다.

이 원리는 단순하지만 결과는 크다. 한 번의 빌드로 *수천 번의 부팅*에서 매번 같은 결정을 반복하던 비용이 사라진다. 컨테이너가 매분 새 인스턴스를 띄우는 시대에, 매번 같은 결정을 반복하지 않는 것 — 그게 클라우드 시대 자바의 *생존 전략*이라고 해도 과언이 아니다.

이 영리함은 30년 자산이라는 부채 위에서 나왔다. Spring은 reflection을 *제거하지 않는다*. 다만 *어디서 누가 무엇을 reflect할지*를 빌드 타임에 알아낼 수 있도록 RuntimeHints API를 도입했다. 사용자 코드와 라이브러리 호환성은 그대로다. 모델은 유지하고 시점만 옮겼다. 이게 Quarkus·Micronaut와 Spring AOT를 가르는 결정적 차이다. 그들은 *새 집을 지었고*, Spring은 *낡은 집의 배선을 다시 깔았다*.

그래서 lazy init과 Spring AOT는 *근본적으로 다른 답*이다. lazy init은 비용을 *눈에 안 보이는 곳*으로 미루고, AOT는 비용을 *눈에 안 보이는 시점*(빌드 타임)에 *완료*한다. 첫 요청 latency는 그대로, 운영 안정성은 그대로, 그러면서 시작 시간만 줄어든다. 그래서 lazy init은 답이 아니고, Spring AOT는 답이다 — 같은 문제를 풀려고 했는데 한쪽은 미루고, 다른 한쪽은 완료한다.

여기서 잊지 말아야 할 사실이 두 가지다.

**첫째, JVM 모드에서도 AOT는 동작한다.** Native까지 안 가도 10~20%의 단축은 얻을 수 있다. Native 도입의 무게가 부담스럽다면, *JVM 모드 AOT를 먼저 켜보는 것이 합리적인 첫 단계*다. Netflix가 정확히 그 선택을 했다.

**둘째, 깨지는 패턴 여섯 가지는 미리 정리해두는 편이 낫다.** 런타임 동적 빈 등록, 인터페이스 리턴 `@Bean`, 환경변수 `@Profile`, 람다 supplier, 클래스패스 리소스 동적 로딩, 익명 DTO 직렬화. 이 여섯 가지가 가장 흔한 함정이다. AOT를 켜기 전에 코드를 한 바퀴 둘러보자. 정리 작업 자체가 *코드 품질 개선*이기도 하다.

물론 우리가 Spring AOT를 다 알았다고 말하긴 어렵다. 이 챕터에서 다룬 것은 C단계 — 프레임워크 초기화 — 의 비용을 빌드 타임으로 옮기는 일이었다. 그러나 자바 앱의 시작 시간은 5단계 비용의 합이다. A·B단계(JVM·클래스 로딩)는 4장의 CDS가 다루고, D단계(JIT warm-up)는 9·10장에서 다룰 것이다.

각 단계의 도구가 직교한다는 사실은 *조합의 가능성*을 열어준다. CDS + Spring AOT + Leyden JEP 515의 조합은 A·B·C·D 네 단계의 비용을 모두 빌드 타임으로 옮긴다. 남는 건 E단계(첫 요청 처리)뿐이고, 이건 어떤 도구로도 줄일 수 없는 *본질적인 hot path 진입 비용*이다. 즉, 이 조합으로 우리는 *시작 시간의 거의 모든 비용을 빌드 타임으로 미루는* 셈이다. closed-world 결단 없이도. 이게 *Java의 미래*에 가장 가까운 그림 중 하나다.

그리고 *진짜 시작 시간 단축의 끝판왕*인 GraalVM Native Image는 다음 두 챕터에서 본격적으로 들여다본다. 그 둘은 C단계뿐 아니라 A·B·D까지 한꺼번에 제거한다. 단, 큰 *결단*을 요구한다. 빌드 시점에 모든 코드가 알려져야 한다는 closed-world 가정. 이 결단의 철학적 의미는 6장에서 차근차근 알아보자. 5장에서 던진 reflection 사변이 거기서 *더 좁은 폭으로* 받아진다.

기억해두자. **Spring AOT는 가장 안전한 Stage 1이다.** Native나 CRaC 같은 큰 결단을 내리기 전에, 이 단계만으로 우리 앱은 더 빨라지고, 우리 코드는 더 깔끔해진다. 그리고 그 정리된 코드는 — 미래에 우리가 Native까지 가기로 결심했을 때 — *훨씬 매끄러운 마이그레이션 경로*가 된다. 인터페이스 리턴을 구체 타입으로 바꾸고, 람다를 명시적 클래스로 풀고, 환경변수 의존을 코드로 옮긴 그 모든 정리 작업은 *Native에서도 그대로 유효하다*. AOT 친화적인 코드는 Native 친화적인 코드의 *부분 집합*이다.

마지막으로 한 가지를 더 짚고 마치자. Spring AOT는 *완벽한 답이 아니다*. 한계가 있다. 환경변수 기반 결정은 빌드 타임에 고정되고, 일부 동적 패턴은 깨지고, RuntimeHints를 잘못 선언하면 런타임에 NoSuchMethodException이 터진다. 도입 비용도 0은 아니다. 빌드 시간은 약간 늘고, 깨지는 패턴을 정리하는 데 한 스프린트 정도가 든다. 그러나 그 비용에 비해 *효과는 명확히 측정 가능*하다. 시작 시간 10~20% 단축. JVM 진단 도구는 그대로. 운영 환경은 그대로.

비용과 효과의 균형을 따져보면, *AOT를 안 켜고 그냥 두는 것*은 잃는 게 많다. 무엇보다 그 *잃는 효과*가 매분 새 컨테이너가 뜨는 클라우드 환경에서 지속적으로 누적된다. 한 번의 빌드 시간 추가로 *수천 시간의 운영 비용*을 절약할 수 있다면, 그건 분명히 가치 있는 거래다.

다음 챕터에서 우리는 그 더 큰 결단의 세계로 들어간다. closed-world의 결단, 그리고 그 결단이 약속하는 50ms의 시작. Spring AOT가 *호환성 위의 영리한 타협*이었다면, GraalVM Native Image는 *그 타협을 넘어선 결단*이다. 무엇을 얻고 무엇을 잃는지, 그리고 어떤 워크로드에 그 결단이 어울리는지 — 6장에서 차근차근 살펴보자.
