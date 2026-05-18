# 12장. 진단의 기술: 결정 후, 그 결정이 옳았는지 확인하기

결정은 끝났다. 11장에서 우리는 8개 기술 앞에 격자를 깔고, 워크로드의 모양을 보고, 분기를 따라 길을 골랐다. 한 팀은 Lambda 결제 API에 SnapStart를 골랐고, 다른 팀은 EKS 위 사용자 프로필 마이크로서비스에 Spring AOT + JEP 483을 골랐고, 또 다른 팀은 야간 정산 배치에 CDS + Leyden만으로 충분하다고 결정했다. 결정 트리는 펼쳐졌고, 트레이드오프는 합의되었다.

자, 그 다음이 무엇인가? *옳았는지 확인할 차례다.*

이걸 짚지 않으면 곤란하다. 결정은 *가설*이다. 11장의 결정 트리에서 우리가 답한 것은 "이 워크로드 모양에는 이 기술이 어울린다"이지, "이 기술을 도입하면 시작 시간이 5초에서 2초로 줄어든다"가 아니다. 후자는 *측정*해야 한다. 측정하지 않고 옳았다고 주장하면 그것은 *체감*에 머문다. 동료가 "스테이징에서 빨라 보이던데요" 하고 묻는데 "맞아, 빨라"라고만 답할 수 있다면 그 도입은 *반쪽짜리*다. *수치로* 답할 수 있어야 한다. 한 줄로. "Stage 0에서 6.28초, Stage 2에서 2.33초, 63% 단축. 그중 B단계가 0.4초 줄었고 C단계가 3.1초 줄었다. D는 그대로다." 이렇게 말할 수 있어야 동료를 설득할 수 있고, 회의실의 의사결정을 받을 수 있고, 무엇보다 *자기 자신을 설득*할 수 있다.

체감 아닌 수치. 이게 이 장의 한 줄 메시지다.

그리고 한 가지 약속을 회수할 시점이기도 하다. 2장에서 우리는 5단계 비용 격자를 세우고는 "어떻게 *볼 수 있는가*"라는 자연스러운 질문에 한 문단으로만 답했다. "Spring의 `BufferingApplicationStartup`과 `/actuator/startup`으로 C단계 빈별 시간을, `-XX:+PrintCompilation`으로 D단계 JIT 컴파일 로그를, `-Xlog:class+load`로 B단계 클래스 로딩 시간을 — 이렇게 각 단계마다 *볼 수 있는* 도구가 다 있다"고만 말하고 "본격적인 측정은 12장에서"라고 미뤘다. *이 약속을 갚을 시점이 왔다.* 10개의 챕터를 지나 4개의 패러다임을 보고 결정 트리를 펼친 다음, 비로소 측정의 자리에 도착했다. 늦게 도착한 게 아니다. *제 자리에 도착한 것*이다. 측정은 결정 *후*에 와야 의미가 있기 때문이다.

좀 더 풀어보자. *왜 결정 전이 아니라 결정 후*에 측정인가? 결정 전에도 측정을 할 수는 있다. 자기 앱의 5단계 비용 프로파일을 미리 그려보고 "C단계가 가장 비싸니까 Spring AOT가 답이다" 하는 식으로 결정을 내릴 수도 있다. 그러나 *그게 충분조건이 아니다.* 워크로드 모양, 팀의 역량, 라이브러리 다양성, 컴플라이언스 — 11장에서 본 변수들이 측정만으로는 안 풀린다. 측정은 *결정의 한 입력*일 뿐이지 *결정 자체*가 아니다. 그래서 11장 결정 트리가 먼저 오고, 12장 측정이 뒤따른다.

그리고 한 번 더. 결정 *후*의 측정에는 두 가지 역할이 있다. 첫째, *옳았는지 확인*하는 역할. 둘째, *다음 결정을 위한 데이터를 쌓는 역할*. 첫 번째 도입에서 측정해둔 수치가 다음 도입의 *기준점*이 된다. Stage 0에서 6.28초였다는 사실, Stage 2에서 2.33초까지 갔다는 사실, 그 사이에서 어떤 단계가 얼마나 줄었는지 — 이 모든 게 다음에 "Native로 가야 하는가, CRaC으로 가야 하는가" 같은 더 큰 결정을 할 때 *근거*가 된다. 측정 없는 도입은 다음 도입의 발판이 못 된다. 그래서 측정은 *현재의 검증*이면서 *미래의 기초*다.

이 장에서 우리는 도구 카탈로그를 따라가지 않는다. *언제 어떤 도구를 꺼낼지*의 사고법을 따라간다. 도구는 많다. `BufferingApplicationStartup`, `/actuator/startup`, `FlightRecordingApplicationStartup`, JFR, async-profiler, `-Xlog:class+load`, `-XX:+PrintCompilation`, `native-image-agent`, `cpu-initialization-period` — 한 챕터 안에 다 풀기엔 욕심이다. 그러나 도구 하나하나를 *깊이* 알 필요는 없다. 진짜 필요한 건 *내 앱의 어떤 증상*을 보았을 때 *어떤 도구*가 답인지의 매핑이다. 그게 진단의 기술의 본질이다. 외과 의사가 청진기·MRI·혈액검사를 모두 깊이 아는 게 아니라, *어느 증상에 어느 진단*이 필요한지를 안다. 우리도 그렇게 가자.

좋다, 그럼 출발하자. 두 줄짜리 진단부터 시작해서 점점 깊은 도구로 내려간다.

## 가장 먼저, 두 줄로 시작하자

자기 앱을 처음으로 진단하고 싶을 때, *무엇부터 켜야 하는가?* 도구 카탈로그를 다 펼치기 전에 한 가지 권하고 싶은 게 있다. 일단 두 줄짜리 옵션부터.

```bash
java -verbose:class -XX:+PrintCompilation -jar app.jar 2> diag.log
```

이 두 개의 옵션이 *진단의 첫 입문*이다. `-verbose:class`는 B단계 — 어떤 클래스가 *언제* 로드되는지 — 를 콘솔에 흘려보낸다. `-XX:+PrintCompilation`은 D단계 — 어떤 메서드가 *언제* 어느 컴파일 티어에서 컴파일되는지 — 를 흘려보낸다. 두 단계가 *동시에 일어나는 광경*이 눈앞에 펼쳐진다.

처음 보면 *압도된다.* 콘솔에 글자가 쏟아진다. 수천 줄. 어디서 시작해야 할지 막막하다. 그러나 한 가지만 보자. 시각의 흐름이다. 부팅 시작 0초부터 5~6초까지의 시간 동안 *클래스 로딩이 어디까지 가는지, JIT 컴파일이 어디서부터 시작되는지*. 그 흐름을 한 번 보고 나면 *추상이 사실이 된다.* "내 앱은 5초 부팅에서 1만 5천 개 클래스를 로드한다. 부팅 끝까지 800개 메서드가 C1 컴파일된다. C2 컴파일은 부팅 끝나고 *그 다음*에 시작된다." 이런 사실이 *수치 없이* 머리에 들어온다. *눈으로 본* 사실이 된다.

이 첫 입문이 왜 중요한가? 5단계 격자가 *추상에서 구체로* 바뀌기 때문이다. 2장에서 우리는 A·B·C·D·E를 격자 위에 올렸다. 격자는 머릿속 모델이었다. 그러나 `-verbose:class`로 클래스 로딩을 직접 보고 `-XX:+PrintCompilation`으로 JIT 컴파일을 직접 본 다음에는, 그 격자가 *실제 시간 흐름*과 짝이 맞춰진다. 0~50ms는 A단계, 50~1500ms는 B단계, 1500~4000ms는 C단계, 4000ms 이후가 D단계의 본격적인 작업 — 이런 *시간 매핑*이 머리에 박힌다. 추상에서 구체로의 전환이 한 번 일어나면, 이후의 모든 진단이 더 정확해진다.

물론 이 두 줄이 *모든 답을 주진 않는다.* C단계 — 프레임워크 초기화, 빈 등록, 자동 설정 평가 — 는 이 두 옵션만으로는 보이지 않는다. 클래스 로딩과 JIT 컴파일은 보이는데, 그 사이에 *Spring이 무엇을 하고 있는지*는 보이지 않는다. 그게 다음 도구의 자리다.

## C단계의 본격 진단 — `BufferingApplicationStartup`과 `/actuator/startup`

Spring Boot 2.4부터 들어온 *그러나 거의 알려지지 않은* 진단 도구가 있다. `BufferingApplicationStartup`이다. 이게 무엇을 하는가? *부팅 중 일어나는 이벤트를 모두 시간순으로 기록*해서, 부팅이 끝난 다음 actuator endpoint로 *트리 형태*로 조회할 수 있게 해준다. 빈 하나하나가 *얼마나 걸렸는지*, 어떤 빈이 어떤 빈에 의존하느라 *얼마나 기다렸는지*, 자동 설정 평가에 *몇 밀리초*가 들었는지 — 이게 한 트리에 다 보인다.

설정은 간단하다. `SpringApplication` 인스턴스에 `BufferingApplicationStartup`을 등록한다.

```java
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication app = new SpringApplication(MyApplication.class);
        app.setApplicationStartup(new BufferingApplicationStartup(2048));
        app.run(args);
    }
}
```

2048은 버퍼 크기다. 빈이 *몇 천 개* 되는 대형 앱이라면 더 키워도 된다. 그리고 `application.yml`에 actuator를 노출한다.

```yaml
management:
  endpoints:
    web:
      exposure:
        include: startup
```

그 다음, 부팅이 끝나면 `curl localhost:8080/actuator/startup`을 친다. JSON이 뱉어진다. 거대한 JSON. `jq`로 정리해서 보자.

```bash
curl localhost:8080/actuator/startup | jq '.timeline.events[] | {name: .startupStep.name, tags: .startupStep.tags, duration: .duration}' | head -50
```

뱉어지는 결과를 한 번 살펴보자. 시간순으로 정렬된 이벤트들이 흐른다. `spring.beans.instantiate`라는 step이 거대 빈마다 등장하고 각각 몇 ms 걸렸는지가 적혀 있다. `spring.boot.application.environment-prepared`, `spring.boot.application.context-loaded`, `spring.beans.smart-initialize` 같은 큰 단계도 보인다. 그리고 가장 중요한 것 — *각 빈의 의존성 그래프와 그 빈을 만드는 데 걸린 시간*.

이걸 *트리 시각화*로 보면 진가가 드러난다. Spring Boot Actuator UI나 [Spring Boot Admin](https://github.com/codecentric/spring-boot-admin) 같은 도구를 쓰면 트리가 그려진다. 또는 자기 손으로 만들 수도 있다. JSON을 D3.js로 그리는 작은 스크립트면 충분하다. 트리가 그려지고 나면 *가장 두꺼운 가지*가 눈에 들어온다. "어, 이 빈 하나가 1.2초나 걸리네?" 이게 *첫 번째 발견*이다. 추상적이던 C단계가 *구체적인 빈들*로 분해된다.

자주 만나는 *두꺼운 가지의 정체*가 몇 가지 있다. 짚어두자.

**JPA EntityManagerFactory 초기화.** 이게 종종 가장 두껍다. Hibernate가 모든 엔티티 클래스를 스캔하고, 메타데이터를 빌드하고, 스키마 검증을 한다. 엔티티가 100개 넘는 앱에서 *1~2초가 그냥 간다.* 만약 `spring.jpa.hibernate.ddl-auto: validate`로 설정되어 있으면 DB와 통신까지 일어나면서 더 길어진다. 이게 *Spring AOT로 옮길 수 있는* 작업이다. 5장에서 본 `PersistenceManagedTypesScanner`가 빌드 타임 스캔으로 이걸 줄인다. 진단으로 *얼마나 줄어들지*를 미리 가늠할 수 있다.

**Flyway 또는 Liquibase 마이그레이션.** 이것도 종종 두껍다. 부팅 시점에 마이그레이션 스크립트를 확인하고, 필요하면 실행한다. 마이그레이션이 *많이 누적된 앱*에서 500ms~2초 든다. 이건 *AOT로 옮기기 어렵다* — DB 상태에 의존하기 때문이다. 다만 *마이그레이션을 부팅 외부로 분리*할 수는 있다. CI 파이프라인에서 DB 마이그레이션을 *부팅 전에* 돌리고, 앱은 마이그레이션 검증만 빠르게 하는 모드(`baselineOnMigrate: true` 등)로 부팅한다.

**자동 설정 평가의 폭발.** Spring Boot가 *수백 개*의 `@Configuration` 클래스를 자동 후보로 보고, 각각의 `@Conditional`을 평가한다. 평가 자체는 빠르지만 *수가 많으면* 누적된다. `/actuator/startup`에서 `spring.boot.autoconfigure.conditions.evaluate`라는 step이 여기에 해당한다. 의외로 무거울 수 있다. 만약 사용하지 않는 starter가 의존성에 들어와 있다면 — 예를 들어 `spring-boot-starter-data-redis`가 있는데 실제로는 Redis를 안 쓴다면 — *불필요한 평가*가 추가된다. 의존성 정리만으로도 200~300ms를 줄일 수 있다.

**거대 캐시 빈 또는 사전 로드 빈.** 부팅 시점에 캐시를 미리 채우거나, 외부 API를 호출해 데이터를 가져오거나, 큰 설정 파일을 읽는 빈. 이런 게 있으면 *그 빈 하나가* 두꺼운 가지로 나타난다. 이건 *비즈니스 결정*의 문제다. 부팅 시점에 사전 로드를 할지, lazy로 미룰지. 1장에서 본 *Lazy Init이 답이 아닌 이유*를 다시 생각해볼 자리다. 부팅이 빨라지면 첫 요청이 느려진다. 그 균형을 *데이터로* 잡는다.

이 트리 분석이 *Spring AOT 도입의 가장 강력한 근거*가 된다. Spring AOT를 켜기 전후로 `/actuator/startup`을 비교해보면, 어떤 빈이 *빌드 타임으로 옮겨졌는지*가 정확히 보인다. "Spring AOT를 켜니 C단계가 4.2초에서 2.8초로 줄었다. 그중 1.0초가 자동 설정 평가에서 줄었고, 0.3초가 JPA EntityManagerFactory에서 줄었다." 이런 수치가 나온다. 도입을 *데이터로 정당화*할 수 있다.

찜찜한 함정 하나. `BufferingApplicationStartup`은 *모든 이벤트를 메모리에 저장*한다. 부팅이 매우 길고 빈이 매우 많은 앱에서는 *진단을 켜는 것 자체가 메모리에 부담*이 될 수 있다. 운영에서는 이걸 *상시 켜두지 말자*. 진단 환경에서만 켜고, 운영 빌드에서는 `DefaultApplicationStartup`(기본값, no-op)을 쓴다. *진단 도구가 운영 비용이 되면 안 된다.*

## 한 단계 더 깊이 — JFR로 시작 전체를 기록하기

`BufferingApplicationStartup`이 *Spring 빈 트리*를 보여준다면, JFR(Java Flight Recorder)은 *JVM 전체*를 보여준다. JIT 컴파일, GC, 클래스 로딩, 스레드, 메모리 할당 — JVM 내부의 거의 모든 이벤트가 JFR로 기록된다. 그리고 Spring에는 `FlightRecordingApplicationStartup`이 있다. 이 친구가 `BufferingApplicationStartup`과 같은 일을 하지만 결과를 *JFR 형식*으로 저장한다. 그래서 *Spring 이벤트와 JVM 이벤트가 같은 타임라인*에 얹혀서 보인다.

설정은 비슷하다.

```java
SpringApplication app = new SpringApplication(MyApplication.class);
app.setApplicationStartup(new FlightRecordingApplicationStartup());
app.run(args);
```

그리고 부팅을 JFR로 동시에 기록한다.

```bash
java -XX:+FlightRecorder \
     -XX:StartFlightRecording=duration=30s,filename=startup.jfr,settings=profile \
     -jar app.jar
```

부팅이 끝난 뒤에 `startup.jfr` 파일을 [JDK Mission Control](https://www.oracle.com/java/technologies/jdk-mission-control.html) 또는 [JMC for Eclipse](https://adoptium.net/jmc/)에서 열면 *세 개의 레이어*가 동시에 보인다.

첫째 레이어, Spring 이벤트. `spring.beans.instantiate`, `spring.boot.application.context-loaded` 같은 *애플리케이션 수준* 이벤트가 타임라인에 점으로 박혀 있다.

둘째 레이어, JIT 컴파일. 어떤 메서드가 *언제* 어느 티어로 컴파일됐는지가 *연속된 막대*로 그려진다. C1 컴파일과 C2 컴파일이 색깔로 구분된다.

셋째 레이어, 클래스 로딩과 GC. 부팅 중에 *몇 개 클래스가 로드됐는지*, *GC가 몇 번 일어났는지*, 각 GC에서 *얼마나 회수했는지*가 보인다.

이 세 레이어를 *겹쳐서 보면* 진짜 그림이 나온다. 예를 들어 *부팅이 갑자기 멈춘 듯한 구간*이 있다면 그게 *GC 풀 사이클*일 수도 있고 *JIT 컴파일러 스레드가 큰 메서드를 컴파일하느라 메인 스레드를 막은* 것일 수도 있다. JFR 없이는 이 구분이 안 된다. *체감*으로는 "어, 여기서 1초 멈췄네"인데 *데이터*로는 "C2가 `SomeHugeMethod`를 850ms 동안 컴파일하고 있었음"이라는 사실이 보인다. 진단의 깊이가 한 단계 내려간다.

JFR이 *얼마나 가벼운가*도 중요한 사실이다. 운영 부담이 작다. `settings=profile` 기준으로 *오버헤드가 1~2%* 수준이다. 그래서 일부 팀은 *운영에서 상시* JFR을 켜둔다. 무언가 이상하다 싶을 때 *그 시점의 JFR 파일*을 다운로드해서 분석한다. 이게 가능한 도구는 흔치 않다. 보통 진단 도구는 *오버헤드가 커서 운영에서 못 켠다*. JFR은 *상시 켜둘 수 있을 만큼 가볍다*는 점이 차별점이다.

함정 하나. 6장과 7장에서 본 GraalVM Native Image에서는 *JFR 지원이 제한적*이다. 부팅 이벤트 일부, 컴파일러 이벤트는 거의 없음(이미 컴파일되어 있으니까), 클래스 로딩 이벤트도 의미가 다름. Native 환경에서는 JFR이 *반쪽 진단*이 된다. 그래서 Native로 간 팀은 *진단 방식을 바꿔야 한다*. 이건 잠시 후 native-image-agent 섹션에서 다시 다룬다.

## 시작의 flame graph — async-profiler

JFR이 *JVM이 알려주는 이벤트*를 본다면, [async-profiler](https://github.com/async-profiler/async-profiler)는 *CPU가 어디서 시간을 쓰는지*를 본다. 도구의 결이 다르다. JFR은 이벤트 기반, async-profiler는 *샘플링 기반*. 후자가 더 *날것의 진실*에 가깝다. Krzysztof Slusarski가 [async-profiler manual by use cases](https://krzysztofslusarski.github.io/2022/12/12/async-manual.html)에서 자세히 다룬 그 도구다.

부팅의 flame graph를 그리는 방법은 한 줄이다.

```bash
java -agentpath:/path/to/libasyncProfiler.so=start,event=cpu,file=startup.html,interval=1ms \
     -jar app.jar
```

`interval=1ms`는 *1ms마다 한 번씩* 스택을 샘플링하라는 뜻이다. 부팅이 5초라면 5,000개의 샘플이 모인다. 충분한 데이터다. 부팅이 끝나면 `startup.html`이 만들어진다. 브라우저로 열면 *flame graph*가 보인다.

flame graph가 왜 강력한가? *한 화면*에 전체 그림이 들어오기 때문이다. 가로축은 *시간*(또는 더 정확히 *샘플 수*), 세로축은 *콜 스택 깊이*. 넓은 막대일수록 *CPU를 많이 쓴 경로*다. 깊은 막대일수록 *호출이 깊이 들어간* 경로다. 가장 넓고 가장 깊은 막대를 찾는 게 *병목 발견의 핵심 동작*이다.

부팅 flame graph에서 자주 발견되는 핫스팟 몇 개를 짚어보자.

**`ClassLoader.loadClass` 또는 `ClassReader.<init>`이 넓다면** — 클래스 로딩 자체가 비싸다. 클래스 수가 많거나 jar 파일 구조가 비효율적이거나(예: 거대한 fat jar). 4장 CDS의 자리다. AppCDS나 JEP 483으로 *로드된 상태를 캐싱*하면 이 막대가 *상당 부분 사라진다.*

**`org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider`가 넓다면** — Spring의 컴포넌트 스캔이 비싸다. `@ComponentScan`이 *너무 넓은 패키지*를 스캔하고 있을 가능성. 좁히는 게 답이다. 또는 Spring AOT로 *빌드 타임에 스캔을 끝내는 것*. 5장의 자리다.

**`java.lang.reflect.Method.invoke`가 깊이 박혀 있다면** — 리플렉션 호출이 핫 패스에 있다. 이게 *부팅 중*에 일어난다면 자동 설정의 conditional 평가, 빈 팩토리 메서드 호출, 프록시 생성 등이 후보다. Spring AOT가 이걸 *직접 호출로 바꿔준다*. flame graph 비교(AOT 켜기 전후)로 그 효과가 *시각적으로* 보인다.

**`java.util.regex.Pattern.compile`이 종종 나타나면** — 정규식 컴파일이 핫스팟. 부팅 중에 정규식이 컴파일된다면 그게 *왜 부팅 시점*에 일어나는지 의심해봐야 한다. 어떤 라이브러리가 `Pattern.compile`을 *static initializer*나 *bean 초기화 시점*에 호출하고 있을 가능성. 이런 건 *지연 로드*로 옮길 수 있다.

**JIT 컴파일러 스레드(`CompilerThread`)가 넓다면** — 부팅 중에 *JIT 컴파일* 자체가 CPU를 많이 먹고 있다. D단계의 비용이 부팅 시간에 *직접 더해지고* 있다는 뜻. JEP 515(AOT Method Profiling) 또는 Azul ReadyNow 같은 *컴파일 캐싱*의 자리다. 9장과 10장에서 본 답들.

async-profiler의 또 다른 강점은 *Native Image에서도 동작*한다는 것이다. JFR이 Native에서 제한적인 반면, async-profiler는 OS 수준의 perf 이벤트를 활용하기 때문에 Native에서도 *시작 flame graph*를 그릴 수 있다. 7장에서 Native Image 트러블슈팅을 다룰 때 우리는 *진단의 어려움*을 언급했다. async-profiler가 그 어려움을 *부분적으로* 메꿔주는 도구다.

함정. async-profiler는 *bytecode-level* 정보를 가지고 있다. 그래서 *컴파일된 메서드의 라인 정보*가 정확하지 않을 수 있다. JIT가 인라이닝한 메서드는 *호출자 안에 흡수*되어 별도 막대로 안 보일 수 있다. 또 *JIT 컴파일 중인 메서드*의 시간이 *컴파일러 스레드 쪽*에 표시되어 *어떤 메서드를 컴파일하는 건지*가 안 보일 수 있다. JFR과 함께 *교차 검증*하는 게 좋다. JFR이 "C2가 `MethodX`를 850ms 컴파일했음"을 알려주면, async-profiler가 "그 850ms 동안 CompilerThread가 CPU를 거의 다 썼음"을 보강한다. 두 도구가 *서로 다른 각도*에서 같은 사실을 비춘다.

## CDS와 JEP 483 효과 측정하기

CDS·AppCDS·JEP 483 — 4장과 10장에서 본 캐시 기반 가속 — 의 효과를 *수치로* 확인하려면 몇 가지 옵션이 있다.

먼저 *CDS가 켜져 있는지*를 확인한다.

```bash
java -Xshare:on -XX:+PrintSharedArchiveAndExit -jar app.jar
```

`-Xshare:on`은 *CDS 아카이브를 반드시 쓰라*는 강제 옵션이다(없으면 부팅 실패). `-XX:+PrintSharedArchiveAndExit`은 *공유 아카이브의 내용을 출력하고 종료*한다. 결과로 *어떤 클래스가 공유 아카이브에 들어 있는지, 아카이브의 크기는 얼마인지, 매핑 주소는 어디인지*가 보인다. 한 번 출력해보자.

```
Loaded base archive /usr/lib/jvm/java-21-openjdk/lib/server/classes.jsa
- archive map base: 0x0000000800000000
- archive size: 11.5 MB
- mapped classes: 1213
...
Loaded dynamic archive app.jsa
- archive map base: 0x0000000820000000  
- archive size: 28.3 MB
- mapped classes: 7842
...
```

이렇게 *베이스 아카이브(JVM 자체)*와 *동적 아카이브(애플리케이션)*가 별도로 출력된다. 베이스는 11.5MB에 1,213 클래스, 동적은 28.3MB에 7,842 클래스. 이 숫자가 *시작 시간 단축의 근거*가 된다. 이만큼의 클래스를 *매번 다시 파싱·검증하지 않는다*는 사실이 수치로 확인된다.

다음으로 *효과의 측정*. 부팅 시간 자체를 측정하는 방법은 단순하다. `time` 명령으로 wallclock을 잰다.

```bash
# CDS 없이
time java -jar app.jar &
# 부팅 끝나면 죽임

# CDS 켜고
time java -XX:SharedArchiveFile=app.jsa -jar app.jar &
```

그러나 부팅 *어디까지가 끝났는지*가 모호하다. 보통 *애플리케이션이 첫 요청을 처리할 준비가 됐을 때*를 기준으로 한다. Spring Boot라면 `ApplicationReadyEvent`가 발생한 시점. 이걸 *코드로* 측정하는 게 정확하다.

```java
@Component
public class StartupTimer implements ApplicationListener<ApplicationReadyEvent> {
    @Override
    public void onApplicationEvent(ApplicationReadyEvent event) {
        long startupMs = ManagementFactory.getRuntimeMXBean().getUptime();
        System.out.println("Application ready in " + startupMs + " ms");
    }
}
```

`RuntimeMXBean.getUptime()`은 *JVM 시작 시점부터의 경과 시간*을 반환한다. `ApplicationReadyEvent` 시점에 이 값을 출력하면 *순수한 부팅 시간*이 잡힌다. 한 번이 아니라 *10번 측정해서 중앙값*을 쓰는 게 좋다. 첫 한두 번은 디스크 캐시가 따뜻해지면서 빨라지기 때문에 *별도로 본다*. 또는 워밍업 후 측정.

JEP 483 AOT 캐시의 효과도 같은 방식으로 측정한다. 다만 *훈련 단계가 추가*된다. JEP 514 덕분에 한 줄 옵션이긴 하다.

```bash
# 훈련 + 어셈블 (1회)
java -XX:AOTCacheOutput=app.aot -jar app.jar

# 운영 (이 시점부터 측정)
java -XX:AOTCache=app.aot -jar app.jar
```

훈련 실행과 운영 실행을 비교해보면 *AOT 캐시의 진짜 효과*가 보인다. 일반적으로 *부팅 시간 40~50% 단축*이 보인다. 측정 결과가 *그 범위에 있으면* 도입이 성공한 것이다. 만약 *효과가 미미하다면* 10장에서 언급한 함정 중 하나에 걸렸을 가능성 — 커스텀 클래스로더, JVMTI agent, ZGC와의 비호환 — 을 의심한다.

CDS와 AOT 캐시 모두 *클래스 로딩(B단계)을 노린다*. 그래서 그 효과를 *분해해서* 보려면 `-Xlog:class+load=info` 로그를 함께 본다. 무엇이 *공유 아카이브에서 로드*됐고 무엇이 *디스크에서 로드*됐는지가 한 줄씩 출력된다.

```bash
java -Xlog:class+load=info:file=load.log -XX:SharedArchiveFile=app.jsa -jar app.jar
```

`load.log`에 *각 클래스가 어디서 왔는지*가 기록된다. 'source: shared objects file'이라고 적혀 있으면 *CDS에서 왔다*는 뜻이고, 'source: file:.../app.jar'라고 적혀 있으면 *jar에서 직접 로드*한 것이다. CDS 적중률을 *클래스 수 기준*으로 계산할 수 있다.

```bash
grep "source: shared" load.log | wc -l   # CDS hit
grep "source: file:" load.log | wc -l    # disk load
```

CDS hit이 85%, disk load가 15% 같은 결과가 나오면 CDS가 *제대로 일하고 있다*. 만약 50% 미만이라면 *훈련이 충분하지 않았다* — 즉 훈련 실행 때 *충분한 클래스가 로드되지 않은 것*. 훈련 워크로드를 *실제 운영과 가깝게* 만들어 다시 훈련해야 한다.

## D단계 JIT 측정 — `PrintCompilation`과 그 너머

D단계는 진단이 까다롭다. *JIT 컴파일이 부팅이 끝난 뒤에도 계속 일어나기 때문*이다. 그리고 *언제 끝났다고 말할지*도 모호하다. 카나리 배포에서 SLA를 깨는 *warm-up spike*가 일어나는 자리가 정확히 D단계인데, 그 spike를 *측정하지 못하면 답이 없다*.

기본 도구는 `-XX:+PrintCompilation`이다. JIT 컴파일 이벤트를 한 줄씩 콘솔에 흘려보낸다.

```bash
java -XX:+PrintCompilation -XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining -jar app.jar 2> jit.log
```

`-XX:+PrintInlining`까지 더하면 *어떤 메서드가 어느 호출 사이트에 인라이닝됐는지*도 보인다. 출력은 이렇게 생겼다.

```
  1234   45  3  java.util.HashMap::put (199 bytes)
  1240   46  4  org.springframework.boot.SpringApplication::run (45 bytes)
```

첫 번째 숫자(1234)는 *JVM 시작 후 경과 시간(ms)*. 두 번째(45)는 *컴파일 ID*. 세 번째(3)는 *티어*(3은 C1 with profiling, 4는 C2). 그 뒤가 메서드 이름과 크기.

이 로그를 *어떻게 활용하는가?* 핵심 질문 두 가지다.

**첫째, C2 컴파일이 언제 시작되는가?** `grep " 4 " jit.log | head -1`로 *첫 C2 컴파일 시각*을 확인한다. 보통 부팅이 끝난 *직후~몇 초 이내*에 시작된다. 그러나 *큰 메서드*들은 이때부터 컴파일되기 시작해도 *몇 초 더* 걸린다. 이 구간이 warm-up spike가 일어나는 자리다. C2가 끝나기 전에 트래픽을 받으면 *느린 코드(C1 또는 인터프리터)로 응답*한다.

**둘째, 컴파일이 *언제 안정화*되는가?** `awk` 한 줄로 *분당 컴파일 수*를 셀 수 있다.

```bash
awk '{ print int($1/1000) }' jit.log | sort | uniq -c
```

초당 컴파일 수가 *어디서 떨어지는지* 본다. 보통 부팅 직후 *몇 초간* 분당 수백 컴파일이 일어나다가, *천천히* 분당 수십 → 수 → 안정 — 이런 패턴이 보인다. *안정 시점*이 D단계가 *대체로 끝난 시점*이다. 운영 환경에서는 이 안정 시점이 *부팅 후 30초 ~ 5분* 사이에 있다. 트레이딩이나 광고 입찰처럼 *워크로드가 변동성이 큰* 시스템에서는 *안정이라는 단어 자체가 없을 수도 있다* — 새 워크로드가 들어올 때마다 새 메서드가 hot이 되면서 *영원히 컴파일이 계속*된다.

JFR로 더 정밀하게 볼 수도 있다. JFR의 `jdk.Compilation` 이벤트가 *각 컴파일의 시작·끝·CPU 시간·인라이닝 정보*를 다 가지고 있다. JMC로 열어서 *시간순으로 컴파일 막대*를 그려보면 위에서 설명한 안정화 패턴이 *그래프로* 보인다.

그러나 한 가지 더 깊은 도구가 있다. *JIT compiler logs*라고 부르는, 더 자세한 출력이다.

```bash
java -XX:+UnlockDiagnosticVMOptions -XX:+LogCompilation \
     -XX:LogFile=compiler.log -jar app.jar
```

`compiler.log`는 *XML 형식*으로 *각 컴파일의 내부 결정*을 다 기록한다. 인라이닝 결정, 디옵트(deoptimization), 트랩(trap) 발생, 어셈블리 코드까지. 이걸 [JITWatch](https://github.com/AdoptOpenJDK/jitwatch) 같은 도구로 열면 *JIT의 의사결정 과정*이 시각화된다. *왜 이 메서드는 C2까지 안 갔는가, 왜 이 인라이닝은 안 일어났는가* 같은 질문에 답할 수 있다.

그렇지만 솔직히 말하면, *대부분의 팀에는 이 수준이 과하다.* JITWatch까지 가는 팀은 *트레이딩, 광고 입찰, 금융 같은 D단계가 1순위 병목인 워크로드*다. 일반 백엔드 API에서는 `PrintCompilation`만으로 충분하다. *C2 시작 시점*과 *안정화 시점* 두 가지만 알면 D단계의 *모양*은 잡힌다.

D단계 측정에서 *가장 중요한 사실* 하나만 짚자. **부팅 시간 측정에 D단계를 포함시키지 마라.** ApplicationReadyEvent 시점은 *부팅의 끝*이지 *D단계의 끝*이 아니다. 두 가지를 *분리해서* 측정하는 게 맞다. 부팅 시간(`ApplicationReadyEvent`까지)과 워밍업 시간(*JIT 컴파일이 안정화될 때까지*)을 *각각* 잰다. 그래야 *어느 단계가 얼마나 비싼지*가 분리된다. 한 덩어리로 보면 *D단계가 부풀어 오른 만큼 부팅이 길어진 것처럼* 보이고, 그러면 *Spring AOT 같은 C단계 도구로 풀어보려는 잘못된 시도*를 하게 된다. 단계가 섞이면 답도 섞인다.

## Native Image의 진단 — 다른 무대

GraalVM Native Image로 갔다면 — 6장과 7장에서 본 그 길이라면 — 진단의 무대가 *완전히 달라진다*. JFR이 반쪽이고, `BufferingApplicationStartup`은 부팅 시 동작하지만 빈 트리의 의미가 다르고(이미 빌드 타임에 일어난 일이라), `PrintCompilation`은 *아예 의미가 없다*(JIT가 없으니까).

좋은 소식은 Native에서는 *D단계가 사라졌다*는 것이다. JIT warm-up 진단이 필요 없다. 나쁜 소식은 *대신 빌드 시점의 진단*이 새로 등장한다는 것이다. 7장에서 본 트러블슈팅 5선 — 빌드 실패, NoSuchMethodException, 리소스 누락, JDK 프록시, Tracing Agent — 이 모두 *빌드 시점의 진단*이다. 측정의 무게중심이 *런타임에서 빌드 타임*으로 이동한다.

런타임에서 측정할 수 있는 것은 *부팅 시간 자체*다. `RuntimeMXBean.getUptime()`은 Native에서도 동작한다. `ApplicationReadyEvent`도 동작한다. 그래서 *부팅 시간 측정 자체는 쉽다*. 보통 Native에서 *50~500ms* 범위로 떨어진다. JVM 모드 대비 *10~50배 단축*이 보인다. 이 수치 하나로 *Native 도입의 성공/실패가 판가름*된다.

뭔가 더 깊이 보고 싶다면 *async-profiler*가 답이다. JFR보다 *Native에서 호환성이 훨씬 좋다*. 한 줄 명령으로 Native 바이너리의 flame graph를 그릴 수 있다.

```bash
./my-native-app -agentpath:/path/to/libasyncProfiler.so=start,event=cpu,file=native-startup.html
```

그러면 *어떤 함수에 CPU를 쓰고 있는지*가 flame graph로 보인다. JVM 환경의 flame graph와 *모양이 매우 다르다*. JIT 컴파일러 스레드가 없고, 클래스 로더 호출이 거의 없고, 대신 *Substrate VM의 런타임 시스템*과 *static initializer 잔여물*이 핫스팟으로 보인다. 익숙해지는 데 시간이 좀 든다.

빌드 시점 진단의 핵심 도구는 *native-image-agent*다.

```bash
java -agentlib:native-image-agent=config-output-dir=./meta -jar app.jar
```

이걸 *JVM 모드에서 한 번 실행*하면, 그 실행 동안 *어떤 리플렉션, 리소스 접근, JDK 프록시, 직렬화*가 일어났는지가 `./meta` 디렉토리에 JSON으로 기록된다. 이 JSON을 Native Image 빌드의 입력으로 넣으면 *자동으로 힌트가 추가*된다. 7장에서 본 *Tracing Agent의 한계*도 다시 짚자. 이 agent는 *실행 경로*만 추적한다. 실행되지 않은 코드 경로의 리플렉션은 *기록되지 않는다*. 그래서 *대표 워크로드를 충분히 다 돌려야* 한다. 통합 테스트 전체를 agent 켠 상태로 한 번 돌리는 식이 일반적인 패턴이다.

Native에서 *진단의 어려움*을 한 줄로 요약하자면 이렇다. **운영 중인 Native 바이너리의 내부를 *런타임에* 보기는 어렵다.** JVM 모드처럼 *프로파일러를 attach해서* 동적으로 확인하는 일이 거의 안 된다. 대부분의 진단을 *빌드 시점*과 *부팅 직후 짧은 시간*에 끝내야 한다. *문제를 미리 예방*하는 쪽으로 진단의 무게가 옮겨간다. 운영 중에 발견된 문제는 *재현 가능한 환경에서 다시 빌드해 재현*하는 식으로 풀어야 한다. 이 부담이 *Native 도입을 망설이게 만드는* 진짜 이유 중 하나다. 7장에서 짚은 *"진단 인프라가 약해진다"*의 구체적 모습이다.

## K8s 측 진단 — 인프라까지 보자

여기까지는 *JVM 안*의 진단이었다. 그러나 운영에서는 *컨테이너 바깥*도 진단의 일부다. K8s에서 도는 Spring Boot 앱이라면 *Pod이 띄워지고 Service에 등록되기까지의 전체 흐름*이 시작 시간이다. JVM 시간만 보는 것은 *반쪽 진단*이다.

K8s 측 진단의 첫 도구는 `kubectl describe pod`와 `kubectl logs`다. 너무 기본적이라 짚지 않을 수도 있지만, 시작 시간 진단에서 *놓치기 쉬운 사실*이 두 가지 있다.

**첫째, Image Pull 시간.** `kubectl describe pod`의 Events 섹션에 `Pulling image`와 `Successfully pulled image` 사이의 시간이 보인다. 이게 *컨테이너 cold cache*에서는 *수십 초~수 분*까지 갈 수 있다. Liberty Mutual 사례에서 *Zip 배포(655ms)와 OCI 컨테이너 배포(3.4초)의 차이*가 여기서 왔다. ECR에서 OCI 이미지를 *pull하는 데 드는 시간*이 부팅 시간을 *오염*시켰다. JVM 안의 부팅이 빨라져도, image pull이 *몇 초*면 그 효과가 *상쇄*된다.

이 문제의 진단은 *시간 분해*다. Pod이 만들어진 시점부터 *Image pull 완료, 컨테이너 시작, 첫 health check 통과, Service endpoint 등록*까지를 각각 측정한다. 어디서 시간이 가는지 *분해해야* 어디를 줄일지가 보인다. Image pull이 병목이라면 *이미지 크기 줄이기, 노드 캐싱(node-local image cache), pre-pulling*이 답이다.

**둘째, Readiness probe의 함정.** Spring Boot 3.x는 *Liveness probe*와 *Readiness probe*를 actuator endpoint로 제공한다. `/actuator/health/liveness`와 `/actuator/health/readiness`. Readiness는 *애플리케이션이 트래픽을 받을 준비*가 됐는지를 알린다. 그런데 *어느 시점에 readiness가 true가 되는가?* 기본 동작은 `ApplicationReadyEvent` 발생 시점에 true가 된다. 즉 *부팅 끝*이다.

여기서 미묘한 함정이 있다. ApplicationReadyEvent는 *Spring 빈이 모두 초기화된 시점*이지 *JIT가 워밍업된 시점*이 아니다. Readiness가 true가 되자마자 K8s는 *Service endpoint에 이 Pod을 추가*하고, 트래픽이 *바로 들어오기 시작*한다. 이 시점이 *D단계의 한가운데*다. *warm-up spike*가 그대로 사용자에게 노출된다. 처음 몇 초간 99th percentile latency가 *수십 배 튄다.* 카나리 배포에서 새 Pod이 5% 트래픽을 받기 시작하는 순간, 그 5% 사용자가 *느린 응답*을 본다.

이 문제의 해결은 *워밍업을 readiness에 포함*시키는 것이다. Spring Boot의 `ReadinessState`를 활용해서, ApplicationReadyEvent 시점에 *별도 워밍업 스레드*를 띄우고, 그 스레드가 *대표 요청들을 자기 자신에게 보낸 다음*에야 ReadinessState를 ACCEPTING_TRAFFIC으로 바꾼다.

```java
@Component
public class WarmupRunner implements ApplicationListener<ApplicationReadyEvent> {
    @Autowired
    private ApplicationAvailability availability;
    @Autowired
    private ApplicationEventPublisher publisher;

    @Override
    public void onApplicationEvent(ApplicationReadyEvent event) {
        // Readiness를 REFUSING_TRAFFIC으로 고정
        AvailabilityChangeEvent.publish(publisher, this,
            ReadinessState.REFUSING_TRAFFIC);

        // 워밍업 트래픽
        warmupCriticalPaths();

        // 다 끝나면 ACCEPTING으로
        AvailabilityChangeEvent.publish(publisher, this,
            ReadinessState.ACCEPTING_TRAFFIC);
    }

    private void warmupCriticalPaths() {
        // 가장 자주 호출되는 엔드포인트를 N회 자기 자신에게 호출
        // 이 동안 C2 컴파일이 일어나면서 hot path가 컴파일됨
    }
}
```

이 패턴이 들어가면 *readiness가 true가 되는 시점*이 *부팅 끝 + 워밍업 끝*으로 늦춰진다. 절대 시간은 *길어진다*. 그러나 *사용자에게 보이는 latency*는 안정적이다. 트레이드오프는 명확하다 — *Pod이 트래픽을 받기 시작하는 시점을 늦추는 대신, 받기 시작한 후의 응답을 안정적으로*. 카나리 배포의 안정성을 *이 트레이드오프로 산다*. 9장에서 본 Azul ReadyNow나 JEP 515 같은 *컴파일 캐싱*은 *이 워밍업 시간 자체를 짧게* 만들어준다. 두 접근이 짝을 이룬다.

**셋째, HPA의 `cpu-initialization-period`.** HPA(Horizontal Pod Autoscaler)는 CPU 사용률을 기반으로 scale-up/down을 결정한다. 그런데 부팅 중인 Pod은 *CPU를 100%* 쓴다 — JIT 컴파일, 빈 초기화 등. 이걸 *정상 부하*로 오해하면 HPA가 *불필요하게 scale-up*을 한다. 그래서 K8s에는 `--horizontal-pod-autoscaler-cpu-initialization-period`라는 옵션이 있다(기본값 5분). 이 시간 동안은 *해당 Pod의 CPU를 스케일링 결정에서 제외*한다.

5분이라는 기본값이 *대부분의 백엔드 API에는 충분*하다. 그러나 Lambda나 단명 워크로드처럼 *Pod이 5분도 안 살고 죽는* 경우엔 의미가 없다. 그리고 *부팅이 매우 길어서 5분 안에 안 끝나는* 거대 모놀리식의 경우엔 이 값을 *늘려야* 한다. 이건 *측정으로 정한다*. 자기 앱이 *부팅 + warm-up까지 평균 몇 분 걸리는지*를 측정해서, 그보다 *1~2분 더 큰 값*으로 설정한다. 측정 없이 기본값을 쓰면 *HPA가 잘못된 결정*을 한다. 측정이 *인프라 설정의 근거*가 된다.

## 트러블슈팅 시나리오 5선 — 진짜 만날 법한 문제들

지금까지 도구를 봤다면, 이제 *그 도구를 어떻게 조합해서 진짜 문제를 푸는지*를 보자. 자주 만나는 시나리오 다섯 개를 풀어본다. 각 시나리오마다 *증상 → 진단 도구 선택 → 해결*의 흐름을 따라간다.

### 시나리오 1: 빈 등록 폭발

**증상.** 부팅이 *갑자기* 두 배로 늘었다. 어제까지 4초였는데 오늘 8초. 코드 변경은 *작은 기능 추가뿐*이었다. 무엇이 8초로 만들었는가?

**첫 진단 도구.** `BufferingApplicationStartup`. `/actuator/startup`을 트리로 뽑아서 *어제 측정한 트리와 비교*한다. (어제 트리를 저장해두지 않았다면 *교훈 1번: 트리를 평소에 저장하자*.)

**발견.** `spring.beans.instantiate`가 어제는 1,200개였는데 오늘 3,800개다. 빈이 *세 배*로 늘었다. 트리에서 *가장 두꺼운 새 가지*를 찾아보면 — `XxxAutoConfiguration` 안에서 `@Bean` 메서드가 *동적으로 1,000개 빈*을 등록하고 있다. 새로 추가한 starter가 *Multi-tenant 처리용*인데, 테넌트마다 빈을 따로 등록하는 패턴이었다.

**해결.** 두 갈래다. (a) Multi-tenant 빈을 *prototype scope*로 바꾸고 *요청 시점에 생성*. (b) 빈 자체를 *하나로 통합*하고 내부에서 테넌트별로 분기. 어느 쪽이 맞는지는 *빈의 책임 모델*에 따른다. 진단은 *빈 수가 폭증했다는 사실*까지만 알려준다. 그 다음은 설계의 영역.

**교훈.** `/actuator/startup` 트리를 *기준선으로 저장*해두자. 부팅 시간이 이상해질 때 *비교할 대상*이 있는 것과 없는 것은 천지차이다. CI에서 매 빌드마다 *부팅 시간 + 빈 수*를 기록하고 *임계점을 넘으면 알람*을 띄우는 게 좋다. *진단 자동화*가 진단 능력의 가장 큰 도약이다.

### 시나리오 2: 라이브러리 자동설정 누락

**증상.** Spring AOT를 켜고 빌드했는데 *어떤 기능*이 동작 안 한다. 예를 들어 *분산 트레이싱*이 안 잡힌다. 또는 *Redis 캐시*가 안 작동한다. 일반 JVM 모드에서는 동작하던 것이었다.

**첫 진단 도구.** Spring AOT 빌드 산출물 검사. `target/spring-aot/main/sources/` 디렉토리에서 *생성된 코드*를 살펴본다. 그리고 `target/spring-aot/main/resources/META-INF/native-image/.../reflect-config.json`을 살펴본다. *내가 기대한 빈 정의가 생성됐는지, 리플렉션 힌트가 제대로 있는지*를 확인한다.

**발견.** 트레이싱 라이브러리(예: Micrometer Tracing)의 자동 설정이 *Spring AOT 빌드 산출물에 누락*되어 있다. 원인은 두 가지 중 하나다. (a) 그 라이브러리가 `META-INF/spring/aot.factories`를 안 제공한다. (b) `@Conditional`이 빌드 타임에 *false로 평가*되어서 자동 설정 자체가 *건너뛰어졌다*.

**해결.** (a)라면 *해당 라이브러리의 PR 기다리기* 또는 *자기 손으로 `aot.factories` 만들어 사이드 라이브러리로 추가*. (b)라면 `@Conditional`의 의존성을 *빌드 타임에 만족시키는* 방향으로 환경을 조정한다. 예를 들어 `@ConditionalOnProperty`가 *환경 변수에 의존*한다면, *빌드 시에도 그 환경 변수를 설정*해야 한다.

**교훈.** Spring AOT 빌드 산출물은 *블랙박스가 아니다*. 직접 열어볼 수 있다. *생성된 Java 소스 코드*는 표준 Java라서 IDE에서 열린다. 디버깅이 어려워 보이지만 *생성된 코드를 직접 읽으면* 의외로 잘 보인다. 5장에서 본 *블랙박스에서 화이트박스로의 전환*이 이 자리에서 빛을 발한다.

### 시나리오 3: 컨테이너 cold cache로 인한 회귀

**증상.** 스테이징에서는 부팅이 1.5초인데, *production에서는 5초*. 같은 이미지, 같은 JVM 옵션. 무엇이 다른가?

**첫 진단 도구.** `kubectl describe pod`의 Events 타임라인. 그리고 `kubectl exec`로 *Pod 안에서 직접 부팅 시간 측정*. 분리해서 보자.

**발견.** *Pod 안 부팅*은 1.5초로 동일하다. 그러나 *Pod이 만들어지고 컨테이너가 시작되기까지*가 *production에서 3.5초 더 걸린다*. Image pull 때문이다. 스테이징은 *노드에 이미지가 캐싱*되어 있는데, production은 *오토스케일링으로 새 노드가 자주 만들어지고* 그때마다 *ECR에서 이미지를 새로 받는다*. Liberty Mutual 사례의 OCI 컨테이너 회귀가 *바로 이 패턴*이다.

**해결.** 두 갈래. (a) *이미지 크기 줄이기* — multi-stage build, distroless base image, JRE만 포함. 100MB → 50MB로 줄어들면 pull 시간도 절반 가까이 준다. (b) *Node-local image cache* 또는 *pre-pulling*. K8s의 `DaemonSet`으로 모든 노드에 *주요 이미지를 미리 받아두기*. 새 노드가 만들어질 때 그 이미지가 *이미 있게* 한다.

**교훈.** *JVM 부팅 시간*과 *컨테이너 부팅 시간*을 분리해서 측정하자. 둘이 섞이면 *어디가 병목인지* 모른다. JVM 안의 Spring AOT, JEP 483 도입은 *Pod 안 부팅*에만 영향을 준다. 컨테이너 부팅이 병목이라면 *완전히 다른 답*이 필요하다. 단계가 섞이면 답도 섞인다는 원칙이 여기서도 적용된다.

### 시나리오 4: JIT thrashing — 컴파일이 끝나지 않는다

**증상.** 부팅 후 *몇 분이 지나도* CPU가 70% 이상이다. 트래픽은 일정한데. JIT 컴파일러 스레드가 계속 일하는 것 같다.

**첫 진단 도구.** `-XX:+PrintCompilation` 로그를 *상시 켜두고* 분당 컴파일 수를 측정. 그리고 JFR로 `jdk.Compilation` 이벤트의 *deoptimization*을 확인.

**발견.** JIT 컴파일이 *안정화되지 않는다*. 분당 수십 컴파일이 *계속 일어난다*. JFR을 보면 *디옵트(deoptimization)*가 빈번하다. 같은 메서드가 *컴파일 → 디옵트 → 재컴파일*을 반복한다. 원인은 *프로파일이 안정되지 않기 때문*. 예를 들어 어떤 메서드 안에서 *타입 분기*가 일어나는데 그 분기 패턴이 *시간에 따라 변한다*. JIT가 "이 분기는 90% A 타입" 가정으로 컴파일했는데 *나중에 B 타입이 자주 들어와서* 디옵트하고 재컴파일한다. 메가모픽(megamorphic) 호출 사이트의 전형적 증상.

**해결.** (a) *코드 수준* — 분기 패턴을 *단순화*. 추상화 계층을 *지나치게 깊이* 쌓지 않기. 인터페이스 구현체가 *4개 이상*인 핫 패스는 디스패치 비용이 크다. (b) *JIT 튜닝* — `-XX:CompileThresholdScaling=2.0`으로 컴파일 임계를 *높여서* 더 안정된 프로파일 후에 컴파일하기. (c) *Azul ReadyNow* 또는 *JEP 515 AOT Method Profiling* — 이전 실행의 *프로파일을 학습*해서 더 좋은 시작점에서 컴파일. 9장과 10장의 자리.

**교훈.** D단계는 *부팅 이후*에도 계속 살아 있는 비용이다. 부팅이 끝났다고 D단계가 끝난 게 아니다. 그리고 *워크로드가 변동성이 크면* D단계는 *영원히 끝나지 않을 수도 있다*. JIT thrashing은 트레이딩과 광고 입찰에서 *흔한* 문제다. 일반 백엔드에서도 *마이크로서비스의 메서드 다형성이 높은 경우* 나타날 수 있다. JIT 로그를 *주기적으로* 보자.

### 시나리오 5: GC 첫 사이클 — 부팅 직후 일시 정지

**증상.** 부팅이 끝났다고 신호가 떴는데 *첫 요청에 갑자기 200ms~1초 정지*. 그 후로는 정상. *부팅 시간 측정에 잡히지 않는* 느린 첫 요청.

**첫 진단 도구.** GC 로그. `-Xlog:gc*=info:file=gc.log`. 또는 JFR의 `jdk.GarbageCollection` 이벤트.

**발견.** 부팅 직후 *첫 풀 GC*가 일어났다. 부팅 중에 *수많은 객체가 생성*되었고, 그 일부가 *Old generation으로 promotion*되었다. ApplicationReadyEvent가 발생한 직후 GC가 *Young + Old 정리*를 시작했다. 그 정리에 *수백 ms ~ 1초*가 들었다. 그 사이 첫 요청이 들어왔고, *멈춤*을 경험했다.

**해결.** (a) *부팅 직후 명시적 GC* — 부팅 끝나면 `System.gc()`를 *한 번 호출*해서 풀 GC를 *제어된 시점*에 일으키기. ReadinessState를 ACCEPTING_TRAFFIC으로 바꾸기 *전에* 한다. (b) *G1 또는 ZGC* — 저지연 GC로 옮긴다. 풀 GC의 *멈춤 시간 자체를 짧게* 한다. ZGC는 *1ms 미만* 일시 정지를 약속한다. 10장에서 본 ZGC + JEP 483 호환성 이슈를 다시 확인해야 하지만, *저지연 GC가 답인 워크로드*에서는 이 조합을 *기다리거나 G1으로 우회*한다. (c) *워밍업 단계 포함* — 시나리오 4에서 본 워밍업 패턴 안에서 *GC도 같이 안정화*시킨다.

**교훈.** GC도 *D단계의 일부*다. JIT 컴파일과 함께 *부팅 직후 안정화*가 필요한 작업이다. 시작 시간 진단에서 *GC 로그를 빼먹지 말자*. ApplicationReadyEvent 시점에 GC가 *얼마나 안정*되었는지가 *첫 요청 응답성*을 좌우한다.

## 진단의 사고법 — 도구를 어떻게 고를 것인가

다섯 시나리오를 본 다음에 우리가 진짜 얻어야 할 것은 *도구 이름*이 아니라 *도구 선택의 사고법*이다. 정리해보자.

**첫째, 단계부터 묻는다.** 어떤 증상을 봤을 때 *5단계 중 어디의 문제*인지를 먼저 묻는다. 부팅이 길어졌다면 A·B·C·D·E 중 어디? 첫 요청이 느리다면 D·E 중 어디? 메모리 스파이크가 있다면 B(클래스 로딩으로 인한 metaspace 폭발)인가 C(빈 자체가 큼)인가? 단계를 먼저 좁히지 않으면 *도구가 너무 많아서* 어디서 시작할지 모른다. 단계는 *도구 선택의 첫 필터*다.

**둘째, 도구는 단계와 짝을 이룬다.** 단계가 좁혀지면 도구가 자동으로 좁혀진다.

| 단계 | 의심 가는 증상 | 첫 도구 | 그 다음 도구 |
|------|----------------|--------|-------------|
| A. JVM 부팅 | 빈 jar도 느림 | `time java -version` | JVM 옵션 검토, CDS 적용 검토 |
| B. 클래스 로딩 | 클래스 수가 폭발 | `-Xlog:class+load=info` | CDS 적용, `jcmd VM.classloader_stats` |
| C. 프레임워크 | 빈 초기화 트리 | `/actuator/startup` | JFR + Spring 이벤트 |
| D. JIT warm-up | warm-up spike | `-XX:+PrintCompilation` | JFR Compilation, JITWatch |
| E. 첫 요청 | 첫 응답만 느림 | application log timestamp | 워밍업 패턴 적용 검토 |
| 인프라 | production만 느림 | `kubectl describe pod` | Image pull 시간, HPA 설정 |

이 표가 *진단 흐름의 첫 가지치기*다. 도구의 풀카탈로그를 다 외울 필요가 없다. *어떤 단계에 어떤 도구*가 답인지의 매핑만 머리에 있으면 된다.

**셋째, 두 개 도구가 짝이 될 때 진짜 답이 보인다.** 한 도구만 쓰면 *반쪽 그림*이다. JFR이 "C2가 850ms 동안 무언가 컴파일 중"이라고 알려주고, async-profiler가 "그 850ms 동안 CompilerThread가 CPU를 거의 다 썼음"을 보강하면 *그림이 맞춰진다*. `/actuator/startup`이 "JPA EntityManagerFactory가 1.2초"라고 알려주고, `-Xlog:class+load`가 "그 1.2초 동안 Hibernate 메타데이터 클래스 800개가 로드됨"을 보강하면 *원인이 좁혀진다*. *교차 검증*이 진단의 깊이를 만든다.

**넷째, 측정은 *반복 가능*해야 한다.** 한 번 측정해서 "5.2초"라고 적어두면 그건 *체감*과 다를 게 없다. *같은 환경*에서 *여러 번* 측정해서 *중앙값과 표준편차*를 알아야 한다. 첫 번째 부팅은 *디스크 캐시가 차가워서* 느리다. 평균 10번 측정에서 *첫 1~2회를 워밍업으로 제외*하고 나머지의 중앙값을 쓴다. *데이터에 변동성이 있다*는 사실을 인정하고, *변동성보다 큰 차이*만을 *의미 있는 차이*로 받아들인다. 5.2초 → 4.9초는 *측정 노이즈일 수도 있다*. 5.2초 → 2.4초는 *명백한 차이*다.

**다섯째, 측정 환경이 운영과 같아야 한다.** 로컬 맥북에서 측정한 결과는 *production K8s 노드*에서 다르다. CPU 모델, 메모리, 디스크 IO, JVM 옵션, GC 알고리즘 — 모든 게 다르다. 가능하면 *production과 같은 노드 스펙*의 스테이징 환경에서 측정한다. 그게 안 되면 *production에 직접 진단을 켜고* 측정한다 — 운영 부담이 낮은 도구(`BufferingApplicationStartup` 가벼운 모드, JFR `settings=default`)만 사용한다. 로컬에서 측정한 수치로 production 결정을 내리는 일은 피하자. *환경 차이*가 *기술 차이*보다 큰 경우가 많다.

## 진단의 자동화 — CI에서 매번 측정하자

여기서 한 걸음 더 가자. *측정을 자동화*하는 일. 진단을 *한 번 켰다 끄는 작업*이 아니라 *상시 흐르는 데이터*로 만드는 일이다.

가장 단순한 패턴은 CI에서 *매 빌드마다 부팅 시간을 측정*하는 것. PR이 머지될 때마다 *자동으로 부팅 시간이 기록*되고, *기준선 대비 X% 이상 증가*하면 *빌드 실패* 또는 *경고*. 자기 손으로 쓸 수 있는 코드는 50줄 정도.

```java
// 부팅 시간 측정 + JSON 출력
@SpringBootApplication
public class StartupBenchmark {
    public static void main(String[] args) throws Exception {
        long startNs = System.nanoTime();
        ConfigurableApplicationContext ctx = SpringApplication.run(
            StartupBenchmark.class, args);
        long readyMs = (System.nanoTime() - startNs) / 1_000_000;

        // 빈 수 카운트
        int beanCount = ctx.getBeanDefinitionCount();

        // JSON 출력
        System.out.println("{\"startup_ms\":" + readyMs +
                          ",\"bean_count\":" + beanCount + "}");

        ctx.close();
    }
}
```

이걸 CI 스크립트에서 *3번 돌려 중앙값*을 뽑고, *기준값과 비교*한다. 결과를 *시계열로 저장*하면 *시간에 따른 부팅 시간 변화*가 그래프로 보인다. 어느 PR에서 *부팅이 길어졌는지*가 한눈에 보인다. 그 PR을 *되돌리거나 최적화 PR을 짝지을지* 결정할 수 있다.

여기서 *측정 → 의사결정 → 측정 → 의사결정*의 루프가 닫힌다. 측정 없는 결정은 *체감*이고, 측정 있는 결정은 *데이터*다. 데이터로 결정을 내리면 *결정의 누적이 가능*하다. 1년 전의 결정과 오늘의 결정을 *비교*할 수 있다. *어떤 결정이 옳았는지*를 *과거의 측정*과 *현재의 측정*으로 *검증*할 수 있다. 이게 측정 자동화의 진짜 값어치다. *결정의 역사*가 *근거 있는 형태로* 보존된다.

좀 더 깊이 가면 *프로파일링 자동화*도 가능하다. CI에서 *부팅 flame graph를 매번 생성*하고, *주요 메서드의 비중*을 *기준선과 비교*한다. async-profiler 한 줄과 [FlameScope](https://github.com/Netflix/flamescope) 같은 분석 도구의 조합. 빌드 실패 기준이 단순한 *시간 임계*뿐 아니라 *flame graph의 모양 변화*까지 포함되면 — *어떤 메서드가 갑자기 핫스팟이 됐는지*도 자동 감지된다. 이게 *진단 자동화의 정점*이다.

물론 모든 팀이 여기까지 갈 필요는 없다. *부팅 시간 + 빈 수*만 매 빌드마다 기록해도 충분히 가치 있다. *작게 시작해서 필요해질 때 깊이*를 추가하자. 진단 자동화는 *일회성 프로젝트*가 아니라 *지속적 운영*이다. 작게 시작하는 게 *오래 가는* 길이다.

## 한 가지 사변 — 측정과 결정의 관계

여기서 한 가지 사변을 해보자. *측정과 결정은 어떤 관계인가?*

상식적인 답은 "측정이 결정의 근거"라는 것이다. 측정 → 결정 — 인과의 방향이 *그 한쪽*으로만 흐른다. 그러나 이 책의 11장 결정 트리는 *그 인과를 뒤집었다*. 측정 *전에* 결정을 먼저 하라고. 워크로드 모양, 팀 역량, 라이브러리 다양성 — 측정으로는 안 잡히는 변수들이 *결정의 진짜 입력*이라고. 이게 *측정 → 결정*의 단순한 인과를 깬다.

그리고 12장에서 우리는 *결정 → 측정*의 방향을 짚었다. 결정 후의 측정이 *옳았는지 확인*이고 *다음 결정의 기초*라고. 그래서 측정과 결정은 *순환 관계*다. 측정 → 결정 → 측정 → 결정 — 이 루프가 *시간에 걸쳐* 돈다. 한 시점의 측정이 *그 시점의 결정의 입력*이 되고, 그 결정 후의 측정이 *다음 시점의 결정의 입력*이 된다. 인과가 일방향이 아니라 *피드백 루프*다.

이 사변이 의미하는 바가 있다. *측정 능력 자체*가 *결정 능력*을 키운다. 측정을 자주, 정확히, 자동으로 할 수 있는 팀은 *결정의 누적*이 일어난다. 1년 전의 결정과 오늘의 결정 사이에 *측정으로 검증된 경험치*가 쌓인다. 그 경험치가 *다음 결정을 더 빠르게, 더 정확하게* 만든다. *측정은 단순히 결정의 입력이 아니라, 결정 능력의 자산*이다.

그래서 *어떤 도구를 도입했는가*보다 *측정 인프라를 어떻게 깔았는가*가 *팀의 장기적 역량*을 더 크게 좌우한다. Spring AOT, Native, CRaC을 모두 시도해본 팀과, 그 시도들을 *모두 측정으로 검증해서 데이터로 누적한 팀*은 *완전히 다른 위치*에 있다. 후자는 *다음 기술의 도입을 빠르게* 결정한다. 측정 인프라가 *결정의 가속*을 만든다.

이게 *진단의 기술이 한 권의 책에서 한 챕터*를 차지하는 이유다. 도구가 멋있어서가 아니다. 진단 *능력*이 *팀의 장기 자산*이기 때문이다. 한 번 도입한 기술은 *한 번의 이득*이지만, 한 번 갖춘 진단 인프라는 *영원한 이득*이다. 측정의 메타가 이 챕터의 진짜 무게다.

## 마무리 — 측정 없이 옳음을 주장하지 말자

이 장에서 우리는 결정 후의 *측정*을 다뤘다. `-verbose:class`와 `-XX:+PrintCompilation`의 두 줄짜리 첫 입문부터 시작해서, `BufferingApplicationStartup`으로 C단계 빈 트리를 분해하고, JFR로 JVM 전체 타임라인을 보고, async-profiler로 시작 flame graph를 그리고, CDS와 JEP 483의 효과를 분리해서 측정하고, D단계 JIT 컴파일의 안정화 시점을 추적하고, Native Image의 빌드 시점 진단 도구를 봤다. K8s 측에서는 Image pull 시간, Readiness probe의 함정, HPA `cpu-initialization-period`까지 다뤘다. 그리고 다섯 가지 시나리오로 *도구의 조합*이 어떻게 진짜 문제를 푸는지 보았다.

그리고 한 가지 약속을 갚았다. 2장에서 "본격적인 측정은 12장에서"라고 미뤘던 그 약속이다. 격자를 세우고 결정 트리를 펼친 다음에야 측정이 *제 자리*를 찾는다는 이야기. 측정이 결정 *전*이 아니라 결정 *후*에 와야 의미를 가진다는 이야기. 그 약속이 이 장에서 회수됐다.

기억해두자. **체감 아닌 수치다.** 도입 후 빨라 보인다고 도입의 성공을 말할 수 없다. *수치로* 답할 수 있어야 한다. 6.28초 → 2.33초 → 63% 단축. 그중 C가 3.1초, B가 0.4초 줄었음. D는 그대로임. 이런 분해된 수치가 있어야 동료를 설득하고, 회의실의 의사결정을 받고, 무엇보다 *다음 결정의 기초*가 된다. 측정 없이는 결정이 누적되지 않는다.

잊지 말자. **도구는 단계와 짝을 이룬다.** 5단계 격자가 도구 선택의 *첫 필터*다. 어떤 증상을 봤을 때 *어느 단계의 문제*인지를 먼저 묻는다. 그 다음에 도구를 꺼낸다. 도구 카탈로그를 다 외울 필요는 없다. *단계 → 도구*의 매핑만 머리에 있으면 충분하다. 그 매핑이 진단의 기술의 본질이다.

주의해야 한다. **측정 환경이 운영과 같아야 한다.** 로컬에서 잰 수치로 production 결정을 내리는 일은 피하자. *환경 차이*가 *기술 차이*보다 큰 경우가 많다. 가능하면 production과 같은 노드에서 측정하고, 안 되면 *production에 직접 가벼운 진단을 켜고* 측정한다. 그리고 *여러 번 측정해서 중앙값*을 쓴다. 한 번의 측정은 *체감과 같은 정도*의 신뢰성이다.

한 가지 더. **진단도 자동화의 자리에 들어갈 수 있다.** CI에서 매 빌드마다 부팅 시간을 측정하고 기준값과 비교하는 패턴은 50줄 코드로 시작 가능하다. 그 자동화가 *시간에 걸친 결정의 누적*을 만든다. *측정 인프라 자체*가 *팀의 장기 자산*이다. 한 번 도입한 기술의 이득보다, 한 번 갖춘 진단 인프라의 이득이 *훨씬 더 길게* 간다.

그리고 마지막으로 — 가장 깊은 한 가지를 짚어두자. *측정과 결정은 일방향 인과가 아니라 피드백 루프*다. 11장의 결정 → 12장의 측정 → 다시 다음 11장의 결정 → 다시 다음 12장의 측정. 이 루프가 시간에 걸쳐 돌면서 팀의 결정 능력이 *자라난다*. 한 결정의 옳고 그름을 *과거의 측정*과 *현재의 측정*으로 검증하는 일. 그 검증의 누적이 *근거 있는 직관*을 만든다. *직관이 데이터를 갖춘 형태*. 그게 베테랑이 신참과 다른 자리다. *측정으로 키운 직관*은 *그냥 직관*보다 *훨씬 빠르고 훨씬 정확*하다.

자, 책의 마지막 장이 남았다. 13장에서는 *미래*를 본다. Leyden premain 브랜치의 AOT Code Compilation, Virtual Threads와 시작 가속의 *관계 없음*, ZGC와의 상호작용, 그리고 *10년 뒤 JVM 애플리케이션은 어떻게 시작할까*. 책을 닫기 전에 *시야를 한 단계 더 위로* 올려보자. 12장이 *현재의 결정과 측정*을 다뤘다면, 13장은 *다음 10년의 결정과 측정의 형태*를 다룬다. 시작이라는 단어 자체가 어떻게 변할지의 이야기다.

그러나 다음 장으로 넘어가기 전에 한 번 더 짚자. *이 장에서 본 도구 중 두 가지만 골라서 오늘 자기 앱에 적용*해보자. 한 가지는 `BufferingApplicationStartup`이고 한 가지는 `-verbose:class -XX:+PrintCompilation` 두 줄. 이 두 가지가 *진단의 첫 입문*이다. 자기 앱의 5단계 비용 프로파일이 *눈에 보이는 사실*이 되는 가장 짧은 길이다. 책을 덮기 전에 그 한 번을 *직접* 해보면, 이 장의 모든 도구가 *다른 무게*로 머리에 남는다. 측정은 *책으로 배우는 것*이 아니라 *몸으로 익히는 것*이다. 첫 입문이 짧을수록 좋다. 오늘이 가장 좋다.
