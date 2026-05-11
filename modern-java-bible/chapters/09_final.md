# 9장. JPMS — 실패인가 미완인가

새 라이브러리를 의존성에 추가했더니 빌드는 통과하는데 런타임에 갑자기 `IllegalAccessError`가 떨어졌다고 해보자. 메시지는 친절하지 않다. "module java.base does not export sun.nio.ch to unnamed module" 같은 한 줄을 보고, 우리는 `--add-opens`라는 마법 주문을 검색창에 입력한다. 한참을 헤매다 `pom.xml`에 `<argLine>`을 한 줄 더 박고 나서야 빌드가 다시 살아난다. 누가 봐도 *번거롭다*.

그런데 그 에러 메시지의 출처가 어디인가? *모듈 시스템*이다. 정확히는 Java 9가 도입한 JPMS — Java Platform Module System. 우리는 `module-info.java`를 한 줄도 쓰지 않는데, 모듈 시스템은 우리 코드의 발목을 잡는다. 이 모순이 9장의 출발점이다.

왜 우리는 `module-info.java`를 쓰지 않게 됐을까? 그리고 안 쓰는데도 왜 모듈 시스템의 영향은 계속 받는 것일까? 함께 짚어보자.

## Project Jigsaw — 12년의 야망

JPMS는 2008년 Sun Microsystems가 *Project Jigsaw*라는 이름으로 시작한 작업이다. Java 7에 들어갈 예정이었다가 한 차례 미뤄지고, Java 8 때 또 미뤄지고, 결국 Java 9(2017)에서야 빛을 봤다. 9년이 걸렸다. 자바 역사에서 가장 오래 끌었고, 가장 많이 논쟁된 변경이다.

그 야망은 단순했다. 세 가지를 한꺼번에 해결하고 싶었다.

첫째, **JAR Hell의 종식**. 같은 클래스가 두 개의 JAR에 들어 있을 때 클래스로더가 무엇을 먼저 로드하느냐에 따라 동작이 달라지는 그 끔찍한 상황 말이다. classpath의 순서를 바꿔야 빌드가 통과되는 코드를 만져본 사람이라면 알 것이다. 그게 *split package*다.

둘째, **strong encapsulation**. `sun.misc.Unsafe`나 `com.sun.*` 패키지처럼 *공식이 아닌데도 모두가 쓰는* 내부 API를 막고 싶었다. Brian Goetz의 표현을 빌리자면, "공개 약속이 아닌 것을 공개 약속처럼 의존해 온 거대한 부채"를 청산하고 싶었다.

셋째, **JDK의 슬림화**. `rt.jar` 한 덩어리에 들어 있던 1만 개 넘는 클래스를, 필요한 모듈만 골라 `jlink`로 작은 런타임 이미지로 만들고 싶었다. 50MB짜리 도커 이미지에 자바 앱을 넣자는 꿈이었다.

이 야망을 한 문장으로 말하면 — *자바를 다시 정리하자*. 21년간 쌓인 의존성·캡슐화·배포의 부채를 한꺼번에 청산하자는 것이었다. 그렇게 모듈 시스템이 들어왔다.

## `module-info.java` — 다섯 개의 키워드

모듈을 선언하는 자리는 `module-info.java`라는 특별한 파일이다. 패키지 루트에 두는 한 장의 메타 파일이고, 거기에 다섯 개의 키워드가 들어간다. 살펴보자.

```java
module com.example.order {
    requires com.example.common;
    requires transitive java.sql;
    requires static lombok;

    exports com.example.order.api;
    exports com.example.order.internal to com.example.payment;

    opens com.example.order.entity to org.hibernate.orm.core;

    uses com.example.order.spi.PaymentGateway;
    provides com.example.order.spi.PaymentGateway
        with com.example.order.gateway.TossGateway;
}
```

다섯 가지를 차례로 보자.

**`requires`**는 의존성 선언이다. 다른 모듈을 *컴파일 타임 + 런타임* 둘 다 필요로 한다고 알린다. `transitive`를 붙이면 이 모듈을 의존하는 쪽도 자동으로 그 의존성을 받는다. Maven의 `compile` 스코프와 유사하다. `static`을 붙이면 컴파일 타임에만 필요하다 — Lombok 같은 annotation processor에 쓴다.

**`exports`**는 공개 약속이다. 이 패키지의 `public` 타입을 외부에서 쓸 수 있게 한다. `to`를 붙이면 *qualified export* — 지정한 모듈에만 공개한다. 우리가 친했던 그 표현 "공개 API"가 마침내 컴파일러가 강제하는 약속이 됐다.

**`opens`**는 reflection 허용이다. `exports`는 컴파일 타임 공개고, `opens`는 *런타임 reflection*까지 허용한다. Hibernate가 Entity의 private 필드를 setter 없이 채우려면 reflective access가 필요하니, `opens`를 열어준다. 이게 우리가 매일 마주치는 `--add-opens` 옵션의 정체다.

**`uses`**와 **`provides`**는 `ServiceLoader` 메커니즘을 모듈 시스템 위에 얹은 것이다. SPI 패턴을 언어 차원에서 표현한다고 보면 된다.

언뜻 보면 깔끔하다. *공개 약속*과 *내부 구현*이 컴파일러 수준에서 분리되고, *reflection 허용*은 명시적으로만 가능해진다. JLS의 표현을 빌려보자.

> **JLS §7.7 (Module Declarations)**
>
> *A module declaration specifies a new module, a uniquely named, reusable group of related packages, as well as resources and a module descriptor. A module is the unit of reuse in the modular Java platform.*
>
> 한국어 번역: "모듈 선언은 새 모듈을 명시한다. 모듈은 유일하게 명명된, 관련 패키지들의 재사용 가능한 묶음이며, 리소스와 모듈 기술자(module descriptor)를 포함한다. 모듈은 모듈식 Java 플랫폼에서 재사용의 단위다."
>
> 의미 해설: JLS는 모듈을 *재사용의 단위*로 명확하게 정의한다. 클래스나 패키지가 아닌, 모듈이 *plug-in 가능한 묶음*의 단위라는 선언이다. Java가 21년간 정의해 온 가시성의 단위(public/protected/package-private)에 *모듈 경계*가 한 층 더 얹힌다.
>
> 본문 연결: 이 정의는 다음 절에서 다룰 *strong encapsulation*의 법적 근거다. 모듈이 재사용의 단위라면, *모듈 경계 너머의 internal 코드에 의존하는 것은 약속 위반*이라는 논리가 성립한다.

## strong encapsulation — 우리가 모르는 사이 받은 영향

JPMS가 도입되자 JDK 내부 패키지가 외부에 닫혔다. 이 변화는 자동 모듈을 안 쓰는 사람에게도 직접적인 영향을 줬다. *우리 모두가 받은 영향*이다.

Java 8까지는 `sun.misc.Unsafe`를 그냥 import해서 쓸 수 있었다. 메모리를 직접 만지고, off-heap 버퍼를 직접 할당하고, `volatile` 없이도 메모리 배리어를 강제하고 — 자바답지 않은 어두운 마법을 부릴 수 있었다. Netty, Cassandra, Hadoop, JNA — 이름만 들어도 알 만한 라이브러리가 거의 다 `Unsafe`를 썼다.

Java 9부터 그게 닫혔다. 정확히는 *경고*가 떨어지기 시작했고, Java 16(JEP 396)에서 *기본값 실패*로 바뀌었고, Java 17(JEP 403)에서 *강제 캡슐화*가 default가 됐다. 우리가 라이브러리를 업그레이드하지 않은 채 Java 17로 이주하면, `Unsafe`를 쓰던 트랜시티브 라이브러리 중 하나가 런타임에 폭발한다. 흔한 일이다. *난감하다*.

그렇다면 어떻게 풀어야 할까? 두 가지 길이 있다.

첫째, `--add-opens java.base/sun.nio.ch=ALL-UNNAMED` 같은 JVM 옵션을 박아 캡슐화를 뚫는다. *우회로*다. 안전하지 않고, 다음 LTS에서는 막힐 수 있다고 JEP 문서들이 거듭 경고한다.

둘째, 라이브러리를 업그레이드해 `Unsafe` 의존을 끊은 버전으로 옮긴다. 시간이 걸리지만 *바른길*이다.

흥미로운 점은 — 우리가 `module-info.java`를 한 줄도 안 썼는데도, 모듈 시스템의 *경계 강제*는 그대로 받았다는 사실이다. 이게 JPMS의 정체다. 채택은 선택이지만, 영향은 강제다. 기억해두자.

## 자동 모듈과 unnamed module — 혼란의 자리

채택하지 않는 길을 택했다고 모듈 시스템이 사라지는 건 아니다. classpath에 그냥 던진 JAR도 모듈 시스템 안에서 *어떤 자리*에 배치된다. 그 자리가 두 가지다.

`module-info.java`가 없는 JAR가 **classpath**에 있으면, 그건 *unnamed module*에 속한다. 모든 unnamed module은 하나로 묶여 있고, 그 안에서는 캡슐화가 없다. classpath 옛 시절과 동일하게 동작한다.

같은 JAR가 **module path**(`--module-path`)에 있으면, 그건 *automatic module*이 된다. 모듈 이름은 JAR 파일명에서 추론한다(`spring-context-6.1.0.jar` → `spring.context`). automatic module은 모든 패키지를 자동으로 export하고, 다른 모든 모듈을 자동으로 requires하는 *느슨한* 모듈이다.

이 둘이 섞이면 가시성 규칙이 매우 복잡해진다. *explicit module*은 unnamed module을 requires할 수 없다(unnamed module은 이름이 없으니까). 그래서 *explicit module이 되려면 그 의존성 트리의 모든 라이브러리가 modular 또는 적어도 module path에 올라가 있어야 한다*. 한 줄로 말하면 — *우리 코드만 modular로 만들 수가 없다*. 의존성 트리 전체가 함께 움직여야 한다.

이게 JPMS 채택의 첫 번째 *난감함*이다.

## 2017년 — JCP EC 부결 사건

야망이 컸던 만큼 진통도 컸다. 2017년 5월, JPMS는 한 차례 *부결*됐다. Java Community Process(JCP)의 Executive Committee가 Public Review Ballot에서 13:10으로 반대했다(JSR 376). 자바 표준화 역사상 대단히 이례적인 사건이다.

부결의 주축은 IBM과 Red Hat이었다. 두 곳은 *OSGi*라는 또 다른 모듈 시스템을 십수 년간 운영해 온 진영이다. 그들의 비판은 다음과 같이 요약된다.

- *너무 늦었다.* OSGi가 이미 비슷한 일을 해 왔다. 같은 문제를 두 번 풀 필요가 없다.
- *너무 단순하다.* 버전 관리, 동적 모듈 로딩·언로딩, multi-version coexistence 같은 OSGi의 핵심 기능이 빠졌다.
- *반사(reflection) 모델이 깨졌다.* Hibernate·Spring·Jackson처럼 reflective access에 의존하는 거대 라이브러리가 모두 `opens`를 요구하게 된다.

부결 후 한 달간 추가 협상이 진행됐고, 6월에 수정안이 재투표를 통과해 결국 Java 9에 들어갔다. 그러나 그 한 달의 진통이 시그널이었다. *공동체가 이 변화를 충분히 환영하지는 않았다.* 그 그림자가 그 후 9년간 따라다닌다.

## 왜 안 쓰게 됐을까

Java 9 출시로부터 9년이 지난 지금, 솔직하게 짚어보자. 엔터프라이즈 자바 코드 중 `module-info.java`를 가진 곳을 본 적이 있는가? 거의 없다. Spring 6도 modular jar로 제공되지 않는다. Hibernate도 마찬가지다. Jackson도, Logback도, Apache Commons도 — 우리가 매일 쓰는 라이브러리 대부분이 *automatic module* 자리에 머물러 있다.

왜 그럴까. 네 가지 이유가 있다.

**첫째, 너무 늦었다.** 2008년 야망이 2017년에야 도착했다. 그 사이 Maven과 Gradle이 dependency 문제를 해결했고, OSGi가 캡슐화 문제를 해결했고, Docker가 *런타임 격리* 문제를 해결했다. JPMS가 풀려던 문제 대부분이 *이미 부분적으로 풀려 있었다*. "더 나은 길"을 만들어도 *기존 길에서 갈아탈 인센티브*가 충분히 크지 않다.

**둘째, 라이브러리 생태계의 마찰.** 우리가 modular로 가려면 의존성 트리 전체가 모듈화되어 있어야 한다. 하나라도 unnamed module로 남으면 explicit module이 못 된다. 이건 *치킨-에그* 문제다. 라이브러리들은 사용자가 안 쓰니까 modular로 안 만들고, 사용자는 라이브러리가 modular가 아니라서 못 쓴다.

**셋째, Spring·Hibernate의 깊은 reflection.** Spring의 핵심 메커니즘 중 하나가 *런타임 reflection을 통한 의존성 주입*이다. Hibernate는 *Entity의 private 필드를 setter 없이 채운다*. 두 라이브러리 모두 `opens`를 광범위하게 요구한다. modular 환경에서 이 둘을 쓰려면 거의 모든 도메인 패키지를 `opens`해야 하고, 그러면 *캡슐화의 이득이 거의 사라진다*. 그럴 거면 차라리 classpath 쓰는 게 깔끔하다.

**넷째, 학습 곡선과 에러 메시지.** 처음 `requires`·`exports`·`opens`를 마주친 개발자가 그 차이를 이해하기까지 며칠이 걸린다. 그 와중에 떨어지는 에러 메시지는 *split package*, *uses constraint violation* 같은 자바답지 않은 표현을 동원한다. 학습 비용이 ROI를 압도한다.

이게 *실패론*의 골격이다. 정직하게 인정하자. JPMS는 *애플리케이션 레벨에서는* 실패에 가깝다.

## 그러나 — JDK는 모듈화됐다

물론 실패라고만 부르긴 부당하다. JPMS의 가장 큰 *조용한 성공*은 JDK 자체에 있다.

Java 9 이전 JDK는 `rt.jar` 한 덩어리였다. Java 9 이후는 80개가 넘는 `java.*`·`jdk.*` 모듈로 쪼개졌다. 그 덕분에 다음과 같은 일이 가능해졌다.

`jlink`로 *우리 앱이 진짜 쓰는 모듈만 골라* slim runtime image를 만들 수 있다. 컨테이너 시대에 이게 얼마나 큰 자산인가. 표준 JDK가 300MB인데, `jlink`로 만든 이미지는 50MB까지 줄어든다. AWS Lambda나 GraalVM Native Image 같은 환경에서 이 차이는 *실제 비용*이다.

```bash
jlink --add-modules java.base,java.logging,java.net.http \
      --output myapp-runtime --strip-debug --compress=2
```

`jdeps`로 의존성을 정적으로 분석해 우리 앱이 어떤 JDK 내부 API를 건드리는지 진단할 수 있다.

```bash
jdeps --jdk-internals --multi-release 17 app.jar
```

`jpackage`로 OS-네이티브 인스톨러(Windows .msi, macOS .pkg, Linux .deb/.rpm)를 만들 때, jlink로 만든 runtime을 묶어 배포할 수 있다. 데스크톱 자바 앱이 이렇게 다시 가능해진 데에는 JPMS의 공이 크다.

그리고 무엇보다 — strong encapsulation 덕분에 *Project Loom*, *Project Panama*, *Project Leyden*이 JDK 내부를 자유롭게 재설계할 수 있게 됐다. `Thread`의 내부 구조를 바꾸고, `MemorySegment`로 native interop을 새로 쓰고, AOT 캐시로 클래스 로딩을 재구성하는 일이 — *공개 API를 깨지 않고도* 가능해진 것이다. JDK 내부의 자유는 외부 사용자의 부담을 늘렸지만, 그 부담만큼 JDK는 더 빠르게 진화하고 있다.

이게 *미완론*의 골격이다. JPMS는 *애플리케이션의 도구로는* 실패에 가깝지만, *JDK의 진화 기반으로는* 명백한 성공이다.

## Spring의 우회 — modular jar로 가지 않는 이유

Spring Framework 6과 Spring Boot 3은 Java 17을 베이스라인으로 정했다. 그렇다면 modular jar로 진화하지 않았을까? 답은 — *아니다*. Spring은 의도적으로 modular path를 택하지 않았다. 왜 그럴까.

Spring의 핵심 가치 중 하나는 *유연한 reflection 기반 DI*다. `@Autowired`, `@Configuration`, `@ConditionalOnProperty` — 이 모든 것이 *런타임에 클래스를 들여다보고 결정*하는 메커니즘이다. modular 환경에서 이걸 유지하려면 우리 도메인 패키지 거의 전부를 `opens`해야 하고, 그러면 캡슐화의 이득이 사라진다.

대신 Spring은 *다른 길*을 택했다. **Spring AOT**(Ahead-of-Time processing)다. 빌드 타임에 BeanFactory의 구조를 정적으로 계산해 `BeanDefinition`을 코드로 생성한다. 런타임에는 이미 만들어진 결정 트리를 *읽기만* 한다. reflection이 거의 필요 없어진다.

이걸 *GraalVM Native Image*와 결합하면 *closed-world 가정*에서 동작하는 네이티브 이미지를 만들 수 있다. 시작 시간은 50ms 수준으로 떨어지고, 메모리는 100MB 미만이 되고, JIT compilation 비용은 0이 된다. JPMS가 풀려던 문제 — *런타임 슬림화*와 *내부 캡슐화* — 를, Spring은 *전혀 다른 길*로 풀어버렸다.

이 우회는 우연이 아니다. 큰 프레임워크가 한 차례 다른 길로 갈아타면, 그 생태계 전체가 따라간다. Quarkus도, Micronaut도, Helidon도 — modular jar가 아니라 빌드 타임 처리 + 네이티브 이미지로 갔다. JPMS의 *애플리케이션 레벨 패배*는 이 시점에 결정됐다고 봐도 무방하다.

## JEP 511 — 작은 화해의 신호

그래도 JPMS가 사라지지는 않는다. 오히려 Java 25는 흥미로운 화해의 신호를 보냈다. **JEP 511: Module Import Declarations**(Java 25 표준)다.

기존에는 `import java.util.List; import java.util.Map; import java.util.ArrayList; ...` 같이 한 줄씩 import해야 했다. JEP 511은 *모듈 단위 import*를 가능하게 한다.

```java
import module java.base;

public class Demo {
    public static void main(String[] args) {
        List<String> names = List.of("Toby", "Alice");
        Map<String, Integer> ages = Map.of("Toby", 41);
        System.out.println(names);
    }
}
```

`import module java.base;` 한 줄이면 `java.util.*`, `java.io.*`, `java.lang.*` 등 `java.base` 모듈의 모든 export된 패키지의 public 타입을 쓸 수 있다. 작은 변화지만 의미가 크다. *모듈을 안 써도, 모듈의 존재는 utility로 활용할 수 있다*는 메시지다. JEP 458의 *compact source file*과 결합하면, 스크립트 같은 자바 코드를 더 짧게 적을 수 있다(10장에서 다룬다).

JPMS가 *내부 도구*에서 출발해, 천천히 *입문자의 친구*로 자리를 옮기는 중이라고 봐도 좋다. 12년의 야망이 처음과는 다른 모습으로 살아남고 있다.

## 정리 — 안 써도 부끄러워하지 말자

이 장의 핵심을 다시 정리해보자.

- JPMS는 2008년 시작해 2017년 도착한 *모듈 시스템*이다. JAR Hell·strong encapsulation·JDK 슬림화라는 세 가지를 한꺼번에 풀고자 했다.
- `module-info.java`의 다섯 키워드(`requires`, `exports`, `opens`, `uses`, `provides`)가 모듈 간 관계를 명시한다.
- *애플리케이션 레벨에서는* 거의 채택되지 않았다. 라이브러리 생태계 호환, Spring/Hibernate의 reflection 의존, 학습 곡선이 주요 이유다.
- *JDK 내부에서는* 명백히 성공했다. `jlink`·`jdeps`·`jpackage`로 슬림 배포가 가능해졌고, Loom·Panama·Leyden이 자유롭게 JDK를 재설계할 수 있게 됐다.
- strong encapsulation의 영향은 채택과 무관하게 *모든* 자바 개발자가 받는다. `sun.misc.Unsafe`가 닫히고, 라이브러리들이 그에 적응하는 비용은 우리 모두가 지불했다.
- Spring은 *Spring AOT + GraalVM Native Image* 조합으로 JPMS를 우회했다. 이 우회가 자바 생태계 전체의 방향을 결정했다.

그러니 — 우리 회사 코드에 `module-info.java`가 없다고 부끄러워할 일이 아니다. *대다수가 그렇게 살고 있고*, 그게 합리적인 선택이다. 다만 strong encapsulation의 영향은 외면할 수 없다. Java 17 이상으로 이주할 때 `--add-opens`를 만나면, *그 자리에서 우회로를 박는 대신 라이브러리 업그레이드를 우선 검토*하는 편이 낫다. 기억해두자.

다음 장은 같은 시기의 *훨씬 더 사용된* 변화들을 다룬다. `var`, switch expression, text blocks, sequenced collections — 우리 손가락이 매일 만나는 작은 문법 변화들이다. JPMS가 *못 박힌 야망*이라면, 이쪽은 *조용히 스민 진화*다. 함께 살펴보자.
