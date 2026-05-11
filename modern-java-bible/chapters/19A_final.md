# 19A장. 모던 자바의 도구들 — JShell부터 jextract까지

CI 파이프라인이 Java 17을 인식 못 해 빌드가 깨졌다고 해보자.

월요일 아침이다. PayBridge의 결제 게이트웨이 서비스가 Jenkins에서 빌드 실패 알림을 보낸다. 로그를 들여다보면 `error: invalid target release: 17`이다. *어, 분명 Java 17 toolchain을 깔았는데?* 빌드 노드를 SSH로 들어가 `java -version`을 쳐보면 8이 답한다. 어떤 PATH가 어디서 가로채는지 추적하는 데 한나절이 간다. 누군가 Ansible 플레이북에서 `JAVA_HOME`을 *친절하게도* 8로 강제 세팅해 둔 자국이 발견된다. 우리는 toolchain 설정 한 줄에 *하루를 쓴 피곤함*을 안고 자리에 돌아온다.

이 풍경은 우연한 사고가 아니다. 11년 사이 자바 도구는 *조용히, 그러나 단단히* 늘어났다. JShell, jpackage, jlink, jwebserver, jextract, JFR/JMC — 각각 작은 도구 같지만 모이면 풍경이 달라진다. 빌드 도구는 자바 버전을 감지하는 방식이 두 번 바뀌었고, JUnit은 records와 sealed를 자연스럽게 안는 5세대로 진화했다. 우리 손에 있는 도구를 우리는 *어디까지* 알고 있을까?

이 장은 그 점검을 위한 자리다. 큰 진리를 펼치는 자리가 아니라, *책장에서 꺼내 펴 보는 레퍼런스*로 쓰여졌다. 도구 하나하나가 왜 들어왔는지, 어디서 어떻게 쓰면 가장 즐거운지를 차례로 보자.

## §19A.1 JShell — 자바에 도착한 REPL

자바 9가 가져온 도구 중 가장 *덜* 화제가 된 것이 JShell이다. JEP 222로 들어왔는데, 모듈 시스템(Jigsaw)의 그늘에 가려져 입에 잘 오르지 않았다. 그러나 일상 디버깅에서 JShell만큼 *손이 덜 가는* 도구가 드물다.

Python에 익숙한 사람은 REPL을 자연스럽게 여긴다. *코드 한 줄 적으면 한 줄의 결과*가 돌아오는 즉시성. 자바는 오랫동안 그게 없었다. 한 줄을 시험해보려고 `Main` 클래스에 `public static void main`을 둘러 짜고, IDE에서 컴파일하고, 실행하고 — 그 *번거로움*을 다들 한 번씩은 겪었을 것이다. JShell이 그 번거로움을 한 줄로 줄였다.

```bash
$ jshell
|  Welcome to JShell -- Version 25
|  For an introduction type: /help intro

jshell> var list = List.of(1, 2, 3, 4, 5);
list ==> [1, 2, 3, 4, 5]

jshell> list.stream().filter(n -> n % 2 == 1).toList();
$2 ==> [1, 3, 5]

jshell> import java.time.*
jshell> LocalDate.now().plusDays(30)
$3 ==> 2026-06-10
```

세미콜론은 선택이고, 결과는 자동으로 `$1`, `$2` 변수에 잡힌다. `var` 선언이 그대로 먹는다. 새로운 자바 문법을 한번 만져보고 싶을 때, *코드 짜기 전에 감을 잡고 싶을 때*, JShell만 한 도구가 없다.

Spring 개발자라면 더 흥미로운 사용처가 있다. JdbcTemplate이나 JPA 쿼리를 *즉석에서* 테스트하는 자리다. 운영 DB에 붙어 의심스러운 쿼리를 한 줄씩 시험해 보는 일이 흔한데, 매번 디버깅용 컨트롤러를 만들어 띄우는 것은 *찜찜하다*. JShell에 의존성을 통째로 클래스패스로 끼우면 그 자리에서 끝난다.

```bash
$ jshell --class-path "lib/*"

jshell> import com.paybridge.repo.*
jshell> var ds = ApplicationContextStarter.dataSource()
jshell> var jdbc = new JdbcTemplate(ds)
jshell> jdbc.queryForList("SELECT * FROM payment WHERE status = ?", "FAILED")
```

스크립트 파일로도 돌릴 수 있어, 운영 점검 절차를 `.jsh` 파일로 묶어두면 *반복 작업이 깨끗해진다*. CI에 끼워 헬스체크 용도로 쓰는 팀도 있다.

## §19A.2 jpackage — 데스크톱 자바의 부활

Java 16의 JEP 343이 도입한 jpackage는 *자바 앱을 OS 네이티브 인스톨러로 패키징*하는 도구다. macOS의 `.dmg`, Windows의 `.msi`, Linux의 `.deb`/`.rpm`까지 — 한 명령어로 빠진다.

오래된 자바 데스크톱 앱 배포가 어땠는지 잠시 떠올려보자. Java Web Start로 띄우거나, exe wrapper(Launch4j 같은)를 손으로 끼우거나, JNLP 파일을 사용자에게 설명하거나 — 한결같이 *피로한* 길이었다. 게다가 Oracle이 Java Web Start를 9에서 deprecate, 11에서 제거한 이후로는 그 길조차 막혔다. jpackage가 그 자리를 채운 것이다.

```bash
jpackage \
  --name PayBridgeAdmin \
  --input target/ \
  --main-jar admin-1.0.jar \
  --main-class com.paybridge.admin.Main \
  --type dmg \
  --runtime-image custom-jre
```

`--runtime-image`에 *jlink로 만든 슬림 JRE*를 끼우면 사용자는 자바 설치 없이 앱만 깔면 된다. 이 한 줄이 데스크톱 자바를 다시 *현실적인 선택지*로 만들었다. JavaFX·Swing 앱을 만지는 팀이라면 이미 한 번씩 만져봤을 것이다.

## §19A.3 jlink — 슬림 JRE를 만들자

jlink는 Java 9 모듈 시스템과 함께 들어왔다. 발상은 단순하다. *내가 안 쓰는 모듈은 빼고, 쓰는 모듈만 모아 작은 JRE를 만들자*.

전통적인 JRE는 200MB대다. 우리 앱이 `java.base`, `java.sql`, `java.net.http`, 그리고 약간의 logging만 쓴다면 — 나머지 198MB는 *우리에게 무의미한 무게*다. 컨테이너 이미지에 들어갈 때 이 무게가 직접 비용으로 잡힌다.

```bash
jlink \
  --module-path $JAVA_HOME/jmods \
  --add-modules java.base,java.sql,java.net.http \
  --strip-debug \
  --compress=2 \
  --no-header-files \
  --no-man-pages \
  --output custom-jre
```

이렇게 만든 JRE는 40~60MB 수준으로 떨어진다. 컨테이너 이미지 사이즈가 200MB대에서 90MB대로 줄어드는 경험은 *후련하다*. Spring Boot 컨테이너 패턴에서는 그래서 두 단계로 빌드한다. *빌드 스테이지*에서 jlink로 슬림 JRE를 만들고, *런타임 스테이지*에서 그 JRE 위에 fat jar를 얹는다. 베이스 이미지로 Alpine이나 distroless를 고르면 더 줄어든다.

물론 jlink가 만능은 아니다. *모듈로 잘 정의되지 않은 라이브러리*를 쓰면 어떤 모듈이 필요한지 찾기가 *번거롭다*. `jdeps` 명령으로 의존 모듈을 뽑아내는 절차를 한 번 익혀두면 마음이 편하다. classpath jar로만 쓰던 시절의 라이브러리는 *automatic module*로 추정돼 들어가는데, 이 추정이 *어긋날 때*가 가끔 있다. 그래도 한 번 셋업해두면 그 다음부터는 잊고 살 수 있는 도구다.

## §19A.4 jwebserver — 5초만에 띄우는 정적 서버

Java 18(JEP 408)이 가져온 `jwebserver`는 *민망할 정도로 단순한* 도구다. 현재 디렉토리를 정적으로 서빙하는 HTTP 서버를 한 줄로 띄운다.

```bash
$ cd target/classes
$ jwebserver -p 8080
Binding to loopback by default. For all interfaces use "-b 0.0.0.0" or "-b ::".
Serving /path/to/target/classes and subdirectories on 127.0.0.1 port 8080
URL http://127.0.0.1:8080/
```

Python의 `python -m http.server`를 자바가 11년 늦게 따라잡은 셈이다. 별것 아닌 도구 같지만, *별것 아니라서 자주 쓴다*. 프론트엔드 빌드 결과물을 잠깐 띄워 확인할 때, API 응답 JSON을 같은 머신의 다른 프로세스에 노출할 때, IDE 의존 없이 동료에게 *지금 이 폴더만 한 번 봐달라*고 보낼 때. 큰 도구는 아니지만, 손에 닿는 자리에 늘 있으면 좋은 도구다.

## §19A.5 jextract — C 헤더를 자바 바인딩으로

18장에서 다룬 FFM API를 손에 잡고 쓰려면 *C 함수 시그니처를 자바로 옮기는* 작업이 필요하다. 함수 하나하나를 `Linker`로 손수 묶는 일은 *번거로운* 정도가 아니라 *끔찍한 일*이 된다. 큰 헤더 파일을 가진 라이브러리(예: `libcurl`, `libsqlite3`)를 묶는다고 상상해 보자.

jextract는 그 자리를 자동화한다. C 헤더 파일을 입력으로 받아 *자바 바인딩 클래스*를 생성한다. Project Panama의 자식 도구이며, 별도 다운로드가 필요하다(JDK에 기본 동봉되지는 않는다).

```bash
jextract \
  --output src/main/java \
  --target-package com.paybridge.native.curl \
  --library curl \
  /usr/include/curl/curl.h
```

생성된 클래스에는 함수 매핑·구조체 레이아웃·상수까지 다 들어 있다. 우리는 `Curl.curl_easy_init()`처럼 *그냥 자바 함수처럼* 부르면 된다. JNI 시절에 한 라이브러리를 묶느라 며칠씩 쓰던 자리가 *몇 분*으로 줄어든 풍경 — FFM이 가진 가장 실질적인 약속이다.

## §19A.6 JFR + JMC — production-grade 프로파일링

도구 일습 중 *가장 늦게 빛을 본* 것이 JFR(Java Flight Recorder)과 JMC(JDK Mission Control)다. 둘 다 원래 Oracle JRockit JDK의 상용 도구였고, Hotspot에 흡수된 뒤로도 한참 상용으로 남아 있었다. Java 11에서 JEP 328로 *오픈소스화*되면서, *production에서 부담 없이 켜 둘 수 있는* 프로파일링 도구가 자바 생태계에 들어섰다.

JFR의 특징은 *항상 켜둘 수 있다는 점*이다. 오버헤드가 1~2% 수준으로 잡혀 있어 운영 환경에 부담을 주지 않는다. JVM 내부에서 일어나는 거의 모든 이벤트 — GC, 클래스 로딩, JIT 컴파일, 락 경합, IO, 그리고 14장에서 본 `jdk.VirtualThreadPinned` — 를 *낮은 비용으로* 기록한다.

가장 흔한 사용 패턴은 두 가지다. 운영 중 의심 구간만 일정 시간 *덤프*해 분석하거나, 24시간 *연속 기록*을 굴리면서 문제가 터졌을 때 그 직전 구간을 떠내는 방식이다.

```bash
# 60초 동안 측정해 파일로 떠내기
java -XX:StartFlightRecording=duration=60s,filename=app.jfr -jar app.jar

# 운영 중인 JVM에 jcmd로 붙어서 동적으로 시작
jcmd <pid> JFR.start name=app duration=60s filename=app.jfr

# 연속 기록 (Continuous) — 의심스러울 때 dump
jcmd <pid> JFR.dump name=app filename=snapshot.jfr
```

14장에서 *virtual thread가 deadlock이 났다고 해보자*는 시나리오를 던졌었다. JFR로 *pinning을 잡는 실전 시연*을 여기서 마저 끝내보자. 평소 켜둔 JFR 기록에서 의심 구간을 dump한 다음, `jfr` CLI나 JMC GUI로 연다.

```bash
# CLI로 pinning 이벤트만 추리기
jfr print --events jdk.VirtualThreadPinned snapshot.jfr
```

출력을 보면 *어느 스택*에서 *얼마나 자주* pinning이 났는지가 줄줄이 박혀 있다. 한 줄을 잡아 풀어보면 보통 `synchronized` 블록 안에서 IO 호출이 일어나고 있는 자리다. *어, 이 자리에서 막혔구나*. 그 자리만 `ReentrantLock`으로 바꾸면 문제가 풀린다. *JFR이 없었다면 그 자리를 어떻게 찾을 뻔했는가* — 한 번 겪고 나면 JFR은 *상시 켜두는 도구*로 자리 잡는다.

JMC는 JFR 파일을 *그림으로 보는* GUI 도구다. CPU·메모리·락 경합·IO를 시간축 위에서 한눈에 본다. 처음 익히는 비용은 조금 있지만, 한 번 익히면 CLI보다 빠르게 *어디부터 들여다볼지*가 보인다. AdoptOpenJDK·Adoptium 진영에서 별도 빌드를 배포하고 있어, JDK에서 분리돼 있다는 점만 기억해두자.

## §19A.7 빌드 도구의 자바 호환

이쯤 와서 *현장에서 실제로 가장 자주 막히는 자리*를 짚어보자. 빌드 도구다.

자바 LTS가 11에서 17, 다시 21·25로 빠르게 넘어오는 동안, Maven과 Gradle은 각자의 속도로 따라왔다. 한 가지는 기억해두는 편이 낫다.

- **Maven**: 3.6.3 이상이 Java 17과 안정적으로 동작한다. 3.9.x가 Java 21·25 호환의 *권장 라인*이다.
- **Gradle**: 7.3 이상이 Java 17, 8.5 이상이 Java 21을 안정 지원한다. Java 25는 Gradle 8.10+가 안전한 선이다.

낮은 버전을 쓰던 프로젝트에 새 자바를 끼우면 *알 수 없는 컴파일 오류*가 흩어져 나오는 풍경을 한 번씩 본다. *번거롭게* 한참을 들여다본 끝에 도착하는 결론이 빌드 도구 버전이라는 사실이 *허탈하다*. 새 자바를 도입하기 전, 빌드 도구 버전부터 한 번 올리고 가는 편이 낫다.

도구 호환의 다음 매듭은 *toolchain*이다. 빌드 시스템이 *어떤 JDK로 컴파일하고 실행할지*를 명시적으로 묶는 장치다. 머신에 깔린 PATH의 JDK에 끌려가지 않고, 프로젝트가 *원하는 JDK*를 골라 쓴다.

Maven의 toolchain 설정은 `~/.m2/toolchains.xml`에 JDK 경로를 등록하고, `pom.xml`에서 `maven-toolchains-plugin`으로 묶는다.

```xml
<plugin>
  <artifactId>maven-toolchains-plugin</artifactId>
  <configuration>
    <toolchains>
      <jdk>
        <version>21</version>
        <vendor>temurin</vendor>
      </jdk>
    </toolchains>
  </configuration>
</plugin>
```

Gradle은 *toolchain 자체를 자동으로 다운로드*해 주는 길까지 열어두었다. `build.gradle`에 한 블록만 적으면 된다.

```groovy
plugins {
    id 'java'
    id 'org.gradle.toolchains.foojay-resolver-convention' version '0.8.0'
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
        vendor = JvmVendorSpec.ADOPTIUM
    }
}
```

`foojay-resolver-convention` 플러그인이 *foojay Disco API*에 붙어 우리가 요청한 JDK를 알아서 받아온다. 머신마다 손으로 JDK를 깔던 시절을 깨끗하게 정리한 길이다. CI 머신에 *JDK가 안 깔려 있어도* Gradle이 알아서 받아 쓰니, Jenkins 노드 셋업이 한결 가벼워진다. 모놀리식 빌드 머신에 11과 17과 21을 동시에 굴리는 *옛 풍경*을 끝내고 싶다면, 이 한 줄이 시작점이다.

여기에 **Maven Wrapper**(`mvnw`)와 **Gradle Wrapper**(`gradlew`)를 더하면 *Maven/Gradle 자체*도 머신에 깔 필요가 없어진다. 레포에 wrapper 스크립트만 들어 있으면, 처음 실행 시 알맞은 버전의 빌드 도구를 자동으로 받는다. *어느 머신에서나 같은 빌드*가 보장되는 풍경 — 11년 전 자바 개발자가 보면 *부러워할 만한* 풍경이다.

Spring Boot의 Maven/Gradle 플러그인도 toolchain 정보를 읽어 *어떤 자바로 컴파일·패키징할지*를 자동으로 맞춰준다. 컨테이너 이미지 빌드(buildpack 또는 layered jar)도 toolchain의 자바 버전을 그대로 따른다. *플러그인 한 줄과 toolchain 블록 한 줄*이면, "이 프로젝트는 Java 21 LTS로 도는 결제 서비스다"라는 사실이 빌드 시스템에 *명시적으로* 박힌다. 옆 팀이 우리 레포를 처음 클론해 빌드하더라도 머신의 자바 버전 때문에 *난감해질 일*이 없다.

## §19A.8 JUnit 5와 Modern Java

마지막으로 테스트다. 도구가 늘어나면 *테스트하는 방법*도 같이 진화해야 한다. JUnit 5(Jupiter)는 Modern Java의 도구들과 자연스럽게 결합한다.

**records와 `@ParameterizedTest`** — records의 *값 객체* 성격이 파라미터화 테스트와 궁합이 좋다. 옛 JUnit에서 케이스를 표현하려면 `Object[][]`나 `Stream<Arguments>` 같은 흐릿한 형태에 의존해야 했는데, records는 그 흐릿함을 정리해준다.

```java
record DiscountCase(int amount, int memberLevel, int expected) {}

@ParameterizedTest
@MethodSource("discountCases")
void 할인_계산이_레벨별로_달라진다(DiscountCase tc) {
    assertThat(calculator.discount(tc.amount(), tc.memberLevel()))
        .isEqualTo(tc.expected());
}

static Stream<DiscountCase> discountCases() {
    return Stream.of(
        new DiscountCase(10_000, 1, 1_000),
        new DiscountCase(10_000, 2, 1_500),
        new DiscountCase(10_000, 3, 2_500)
    );
}
```

*어떤 입력에서 어떤 결과를 기대하는지* 한눈에 들어온다. 케이스가 늘어날수록 records의 가독성 효과가 더 커진다.

**sealed exhaustiveness 테스트** — 13장에서 `switch`의 *모든 가지를 다루었는지* 컴파일러가 검증해주는 흐름을 봤다. 그 보장은 *컴파일 타임*의 것이고, 런타임에 *모든 분기가 실제로 도달 가능한지*는 테스트로 한 번 더 잡아두는 편이 낫다. `@ParameterizedTest`에 `Stream`을 모든 permitted 서브타입으로 채워 *전부 한 번씩 통과시키는* 패턴이 유용하다.

**virtual thread를 위한 `@Timeout`** — virtual thread 코드를 테스트할 때 한 가지 *함정*이 있다. JUnit의 기본 `@Timeout`은 *같은 스레드*에서 시간을 잰다. 우리 테스트 코드가 virtual thread 안에서 막혀 있으면, 외부에서 timeout이 발화돼야 하는데 그게 안 일어날 수 있다. JUnit 5.10부터 들어온 `threadMode = SEPARATE_THREAD` 옵션이 그 자리를 풀어준다.

```java
@Test
@Timeout(value = 5, unit = TimeUnit.SECONDS, threadMode = ThreadMode.SEPARATE_THREAD)
void virtual_thread_안에서_데드락이_나도_빠져나온다() {
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        // 의심스러운 코드
    }
}
```

테스트가 *무한히 매달리는* 사고를 피하는 한 줄. 14장의 *끔찍한 새벽*을 두 번 겪지 않으려면 기억해두자.

## 마무리: PayBridge의 CI 파이프라인 변천기

이번 장에서 짚은 도구들을 *한 회사의 CI 변천*으로 묶어 보자. PayBridge는 2014년에 Java 8 + Maven 3.2 + JUnit 4 + Jenkins 1.x로 시작했다. 빌드 머신에 JDK 8을 직접 깔았고, *어떤 머신*에서 빌드되느냐가 결과를 *살짝씩* 흔들었다. 2018년에 Java 11로 옮기면서 모듈 시스템에 발을 담갔고, jlink로 슬림 JRE를 만들기 시작했다. 컨테이너 이미지가 600MB에서 220MB로 줄었다.

2021년에 Java 17 LTS로 한 번 더 옮기면서, Gradle 7.3과 toolchain plugin·foojay-resolver를 도입했다. CI 머신에 JDK를 깔지 않게 됐다. *Jenkins 노드 셋업이 한 단계 줄어든 날* 운영팀이 한숨을 돌렸다. JFR을 production에 *상시 켜두기* 시작한 것도 이때다. p99 알람이 울리면 그 직전 1분의 JFR snapshot이 자동으로 슬랙으로 떨어진다.

2024년에 Java 21로 가면서 virtual thread를 도입했고, JUnit 5의 `threadMode = SEPARATE_THREAD`를 테스트 디폴트로 묶었다. 2026년 지금, Java 25를 검토하는 단계다. 19장에서 본 CDS·AOT 캐시를 컨테이너 빌드에 끼우고, Compact Object Headers를 켤지를 측정으로 결정 중이다.

이 변천을 한 줄로 묶는다면 — *도구는 자바와 함께 자란다*. 우리가 자바 11년치의 언어 진화를 따라온 만큼, 도구 진화에도 따라잡을 자격이 있다. JShell 한 번 띄워 새 문법 감을 잡고, jpackage로 사내 도구 인스톨러를 만들고, jwebserver로 빠르게 정적 파일을 내주고, JFR를 켜둬 운영을 관찰하고, toolchain plugin으로 빌드를 단단히 묶는 일 — 어느 것도 *큰 결단을 필요로 하지 않는다*. 손에 닿을 때마다 한 도구씩 익혀두자.

다음 장에서는 결을 크게 돌린다. *멈춰 있는 코드베이스를 어디서부터 손대야 하는가*. Java 8 → 17 마이그레이션의 현장 함정과 권장 순서를 정리한다. 11년의 진화가 마이그레이션이라는 한 단어에 모이는 자리다.
