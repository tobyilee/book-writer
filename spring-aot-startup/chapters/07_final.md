# 7장. Native Image 실전: 빌드 시간, 트러블슈팅, PGO

월요일 아침이라고 해보자. 앞 장에서 GraalVM Native Image의 철학을 함께 본 뒤, 자신감이 적당히 충전된 상태로 사무실 책상에 앉는다. closed-world라는 개념도 머리에 들어왔고, points-to analysis가 무엇을 하는지도 안다. 우리 팀의 Spring Boot 결제 API에 한번 적용해 볼 만한 시간 같다. 사이드 프로젝트가 아닌 진짜 운영 코드다. `pom.xml`에 `native-maven-plugin`을 끼우고, 터미널에서 `./mvnw -Pnative native:compile`을 친다.

그리고 기다린다.

1분이 지난다. 빌드 로그가 점점 길어진다. `[1/8] Initializing...`이 끝나고 `[2/8] Performing analysis...`로 넘어간다. 컴퓨터 팬 소리가 평소와 다르다. 2분, 3분이 지난다. 슬슬 다른 일을 하려는 찰나, 갑자기 빨간 글씨가 터미널을 가득 채운다.

```
Error: Classes that should be initialized at run time got initialized during image building:
   ch.qos.logback.classic.Logger was unintentionally initialized at build time...
```

8분 30초 만의 결과다. 빌드 실패. 코드 한 줄도 안 바꿨는데 말이다.

이런 경험을 한 번이라도 해봤다면, 이 장이 어떤 톤으로 흘러갈지 짐작이 갈 것이다. 6장은 *왜 그래야 하는가*의 챕터였다. 7장은 *그래서 실제로 무엇이 깨지는가*의 챕터다. 낭만은 잠시 접어두자. 빌드가 8분 걸리는 현실, 라이브러리마다 어떻게 다른 방식으로 망가지는지, PGO를 운영에서 정말 쓸 수 있는지, 그리고 *Native를 골랐다가 돌아온 팀이 무엇을 배웠는지*를 함께 본다.

## 빌드 시간 8분의 무게

먼저 빌드 시간 이야기부터 정직하게 짚어두자. 평범한 Spring Boot 웹 앱을 Native Image로 빌드하면 노트북에서 보통 1분에서 10분 사이가 걸린다. 작은 데모 앱은 30~40초로 끝나기도 하지만, 영속성 계층과 보안 모듈과 메시지 브로커 클라이언트가 다 들어간 진짜 API는 5분에서 8분이 일상이다. 라이브러리가 많을수록, 도달 가능한 메서드가 많을수록, points-to analysis가 따라가야 할 그래프가 커진다.

이게 왜 문제일까? 단순한 산수다. 평소 JVM 빌드는 `./mvnw clean package`에 30초 안팎. 코드를 한 줄 고치고 테스트를 돌리는 cycle을 한 시간에 열 번쯤 돌릴 수 있다. 그런데 Native 빌드가 8분이 걸리면 한 시간에 최대 일곱 번. 게다가 빌드 중에는 노트북 팬이 소리를 내고 다른 작업이 느려진다. 개발자의 인지 흐름이 그 사이에 끊긴다. *코드를 고치고 결과를 확인하기까지의 거리가 멀어진다*. 이 거리가 늘어나면 사람의 사고도 느슨해진다. Tight feedback loop는 좋은 코드의 전제조건인데, 그게 깨진다. 빌드 한 번을 기다리는 8분 동안 *맥주 한잔 하러 갈 수도 없는* 어정쩡한 시간 — 개발자에게 이만큼 번거로운 일도 드물다.

그렇다면 어떻게 해야 할까? 단호한 분업이 답이다. **dev loop는 JVM 모드로, Native 빌드는 CI에서.** Spring AOT는 5장에서 봤듯이 JVM 모드에서도 `-Dspring.aot.enabled=true`로 동작한다. AOT 처리 자체는 평소 빌드에 끼워두고, 그 결과를 JVM 위에서 검증한다. Native 컴파일은 별도 워크플로우로 분리한다 — pull request마다 도는 PR 검증 잡 하나, 메인 브랜치 머지 후 도는 야간 잡 하나. 이렇게 분리하면 개발자는 평소처럼 일하고, Native Image의 *진짜* 검증은 비동기로 이뤄진다.

GitHub Actions로 예시를 만들어보자. CI 파이프라인을 두 단계로 쪼갠다.

```yaml
# .github/workflows/build.yml (요지만)
jobs:
  jvm-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
      - run: ./mvnw -DskipTests=false -Dspring.aot.enabled=true verify

  native-build:
    runs-on: ubuntu-latest-large  # 더 큰 러너
    needs: jvm-build
    steps:
      - uses: actions/checkout@v4
      - uses: graalvm/setup-graalvm@v1
        with:
          java-version: '21'
          distribution: 'graalvm'
      - run: ./mvnw -Pnative native:compile -DskipTests
      - run: ./target/myapp &
              sleep 2 && curl -fsS localhost:8080/actuator/health
```

여기서 한 가지 주의할 점. Native 빌드는 *메모리를 많이 먹는다*. points-to analysis가 도달 가능 그래프를 메모리에 펼쳐놓고 작업하기 때문이다. GitHub의 기본 러너(7GB RAM)에서는 빌드 중간에 OOM으로 죽는 경우가 흔하다. `ubuntu-latest-large`나 self-hosted 러너로 16GB 이상을 확보하는 편이 낫다. 우리 팀이 처음 Native를 도입할 때 가장 많이 한 헛수고가 "왜 갑자기 빌드가 죽지?"였는데, 결국 러너의 메모리 한계였다. 기억해두자.

또 한 가지. **빌드 시간을 줄이려는 유혹을 조심하자.** GraalVM은 `-O0`(최적화 끄기), `--gc=epsilon`(GC 비활성화) 같은 옵션을 제공한다. 빌드는 정말 빨라진다. 하지만 결과 바이너리는 운영에 못 쓴다. 빌드 시간을 줄이려고 운영성을 깎는 게 아니라, *빌드를 비동기로 만들어* 개발 흐름과 분리하는 게 정공법이다.

### CI에서 Native 빌드를 어떻게 캐싱하는가

빌드가 매번 8분이면 야간 잡을 백번 돌려도 800분이 사라진다. GraalVM은 Native Image Bundle 기능을 제공한다. `--bundle-create`로 빌드 입력을 묶고, `--bundle-apply`로 다른 머신에서 재현할 수 있다. CI에서 의미 있는 활용은 **변경된 부분만 다시 빌드하는 것**이 아니라(이건 아직 잘 안 된다), **레이어 캐싱**이다. Maven `.m2`와 GraalVM의 분석 캐시를 액션 캐시에 올려두면 의존성 다운로드와 일부 분석 단계가 재사용된다.

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.m2/repository
      ~/.gradle/caches
    key: m2-${{ hashFiles('**/pom.xml') }}
```

이 정도로도 빌드 시간 2~3분은 줄어든다. 마법은 아니지만, 일상의 80%를 차지하는 의존성 다운로드는 분명히 비용이었다. 

그리고 한 가지 덧붙이자면, **Native 빌드는 메인 브랜치에만 강제하자**. 모든 PR마다 8분짜리 잡을 강제로 도는 건 PR을 막아두는 것과 같다. PR에서는 JVM 모드 + AOT 활성화로 빠르게 검증하고, 메인 머지 후 야간 잡에서 진짜 Native 빌드가 한 번 돈다. 만약 야간에 깨지면 알람이 다음 날 아침에 도착한다. 이게 현실적인 비동기 운영이다. 빌드 8분짜리 도구는 *동기적으로 다룰 수 없다*는 사실을 받아들이는 게 첫걸음이다.

### 한 가지 더 — 빌드 머신을 따로 두자

여기서 자주 간과되는 부분이 하나 있다. **개발자 노트북에서 Native 빌드를 *돌리지 말자*.** 빌드 자체가 노트북 자원을 거의 다 잡아먹는다. 메모리 8~12GB가 빌드 중 사용된다. 8코어가 모두 100%에 가깝게 돈다. 그 시간 동안 노트북에서 다른 IDE 작업이나 docker 컨테이너 실행이 *체감 가능하게 느려진다*. 

해결책은 자명하다. *전용 빌드 서버*다. 사내 K8s 클러스터의 빌드 잡 노드, AWS EC2 spot 인스턴스, 회사 데스크톱 한 대 등. 중요한 건 *개발자가 코드 작성과 빌드를 같은 머신에서 하지 않게* 만드는 것이다. 빌드를 트리거하고 결과만 받아오는 흐름. 이게 일상의 인지 흐름을 지키는 길이다.

GitHub Actions를 쓴다면 `ubuntu-latest-large`(8 vCPU, 32GB RAM)를 켜고, 분기당 잡 시간을 모니터링하자. 빌드 한 번에 분 단위 과금이라 *야간 잡으로 분산*해야 비용이 합리적이다. AWS CodeBuild나 GCP Cloud Build를 쓰는 경우도 비슷하다 — *큰 인스턴스 + 비동기 실행* 패턴.

자체 K8s 클러스터에서 Tekton이나 Argo Workflows 같은 빌드 시스템을 쓴다면, Native 빌드 잡에 *전용 노드 풀*을 할당하는 게 좋다. CPU 8개 이상, 메모리 16GB 이상, SSD. 이 노드들이 평소에는 idle이라도 *빌드 처리량을 위해* 그 정도 자원이 필요하다. 인프라 비용으로 환산하면 한 달에 수십만 원 단위지만, *개발자 시간 절약*과 비교하면 압도적으로 싸다.

## 트러블슈팅 5선

빌드는 통과했다고 치자. 이제 실행해본다. `./target/myapp`을 친다. 시작은 빠르다 — 정말 50ms 안에 뜬다. 처음으로 그 숫자를 직접 보면 묘하게 감격스럽다. 그 후 curl로 첫 요청을 보낸다.

그리고 만나게 된다.

```
java.lang.NoSuchMethodException: com.example.MyEntity.<init>()
        at java.base@21.0.2/java.lang.Class.getConstructor0(...)
```

또는 이런 거.

```
java.io.FileNotFoundException: class path resource [messages/error.properties] cannot be opened
```

또는 이런 거.

```
java.lang.UnsupportedOperationException: 
   Proxy class defined by interfaces [interface com.example.UserService] not found.
```

이 셋 모두 *closed-world의 그늘*이다. 6장에서 본 그 closed-world. 빌드 타임에 *모르고 지나간* 코드 경로가 런타임에 호출되었기 때문에, "그런 코드는 이 바이너리에 없습니다"라고 정직하게 답하는 셈이다. 처음 만나면 정말 찜찜하다. JVM에서는 멀쩡히 돌던 코드가 *바이너리만 다르게 만들었을 뿐인데* 알 수 없는 에러로 거꾸러진다. 그런데 자세히 들여다보면 이게 *결단의 비용*이다. 우리는 6장에서 closed-world를 *받아들이기로* 했다. 이제 그 결정이 운영 현장에서 어떻게 비용 청구서를 내미는지 보는 셈이다.

트러블슈팅은 결국 한 가지 동작이다 — **빌드 타임에 알려주지 못한 정보를 어떻게 알려줄 것인가**. 다섯 가지 패턴으로 정리해보자.

### 패턴 1: `--verbose --no-fallback`으로 빌드 실패 진단

빌드가 깨졌을 때 가장 먼저 켜야 하는 두 플래그가 있다. `--verbose`와 `--no-fallback`이다.

```bash
./mvnw -Pnative native:compile \
  -Dnative.maven.plugin.args="--verbose --no-fallback"
```

`--no-fallback`은 무엇인가? GraalVM은 분석에 실패하면 *fallback image*라는 걸 만든다. JVM을 함께 묶어서 "그래도 일단 동작하게는 해주는" 절충안이다. 친절해 보이지만 실은 *문제를 가려주는* 옵션이다. 결과 바이너리는 200MB가 넘고, 시작 시간 이득도 사라진다. 가짜 성공이다. 

`--no-fallback`을 켜면 GraalVM이 fallback을 만들지 않고 *정직하게 깨진다*. "도달 불가능한 코드 X가 호출됩니다"라거나 "초기화 정책 충돌"이라는 메시지가 빨갛게 뜬다. 처음에는 무서워 보이지만, 진단의 출발점이 되는 정보다. *깨질 거면 시끄럽게 깨지자*가 Native 트러블슈팅의 첫 번째 원칙이다.

`--verbose`는 이름 그대로 단계별 로그를 다 토해낸다. 어느 분석 단계에서 멈췄는지, 어떤 클래스의 도달성을 판단하다가 충돌했는지를 추적할 수 있다. 처음에는 로그가 너무 길어 부담스럽지만, 익숙해지면 빌드 실패의 90%는 verbose 로그의 마지막 50줄에서 답이 보인다. 

여기에 한 옵션을 더 권하고 싶다. `-H:+ReportExceptionStackTraces`. 분석 도중 예외가 나면 풀 스택트레이스를 찍어준다. 라이브러리 어딘가에서 static initializer가 빌드 타임에 실행되다가 어떤 코드 경로를 타고 폭발했는지 보고 싶을 때 필수다.

```bash
-Dnative.maven.plugin.args="--verbose --no-fallback -H:+ReportExceptionStackTraces"
```

이 세 플래그를 *기본값으로 박아두자*. 빌드 성공할 때는 그저 로그가 길 뿐, 실패할 때 비로소 값을 한다. 

좀 더 깊이 들어가면 두 옵션이 더 있다. `-H:+PrintAnalysisCallTree`는 분석이 도달한 메서드 호출 트리를 출력한다. 빌드 결과 디렉토리에 `reports/` 폴더가 생기고 호출 그래프 파일이 떨어진다. *왜 이 클래스가 도달 가능으로 판단됐는가*를 거꾸로 추적할 때 쓴다. 결과 바이너리가 *너무 커서* 줄이고 싶을 때 — 어떤 라이브러리가 의외로 깊이 끌려 들어왔는지 보고 싶을 때 — 유용하다.

`-H:+TraceClassInitialization=<클래스 이름 패턴>`은 특정 클래스의 초기화 시점을 추적한다. "이 클래스가 빌드 타임에 초기화되면 안 되는데 왜 됐나"를 진단할 때 쓴다. Logback이 빌드 타임에 잘못 초기화되어 빌드가 깨지는 경우, 이 옵션으로 *어디서* 초기화가 트리거됐는지 보면 정답이 보인다. 

여기서 한 가지 토비식 권고. **첫 번째 Native 빌드 실패는 *반드시* verbose 로그를 처음부터 끝까지 한 번 읽어보자**. 부담스럽다. 5,000줄이 넘는다. 하지만 그 한 번이 GraalVM 빌드 파이프라인의 머리에 그림을 그려준다. 다음번 빌드 실패부터는 어디를 봐야 할지 *감*이 생긴다. 처음의 30분 투자가 이후 수십 번의 헛수고를 막아준다. 이 점은 정말 권하고 싶다.

### 패턴 2: `NoSuchMethodException` — `reflect-config.json` 또는 `RuntimeHintsRegistrar`로 보강

런타임에 `NoSuchMethodException`이나 `ClassNotFoundException`이 나는 패턴이 가장 흔하다. 보통 라이브러리가 `Class.forName(...)`이나 `clazz.getDeclaredConstructor()` 같은 동적 호출로 접근하는 경우다. 빌드 타임에 그 클래스가 *살아 있을 거라는* 정보가 없으면 GraalVM은 해당 클래스를 도달 불가능으로 판단하고 빼버린다. 그러고는 런타임에 정확히 그 자리에서 폭발한다.

해결은 두 갈래다. 정공법은 RuntimeHints API다.

```java
public class MyHints implements RuntimeHintsRegistrar {
    @Override
    public void registerHints(RuntimeHints hints, ClassLoader cl) {
        hints.reflection().registerType(MyEntity.class,
            MemberCategory.INVOKE_DECLARED_CONSTRUCTORS,
            MemberCategory.DECLARED_FIELDS);
    }
}
```

그리고 `META-INF/spring/aot.factories`에 등록한다.

```
org.springframework.aot.hint.RuntimeHintsRegistrar=\
com.example.MyHints
```

이게 표준 방식이다. Spring AOT는 이걸 GraalVM이 읽는 `reflect-config.json`으로 자동 변환해준다.

또 한 가지 길은 직접 `reflect-config.json`을 작성하는 방법이다. 보통 3rd-party 라이브러리가 자체 힌트를 제공하지 않을 때 쓴다.

```json
[
  {
    "name": "com.example.MyEntity",
    "allDeclaredConstructors": true,
    "allDeclaredFields": true,
    "allDeclaredMethods": true
  }
]
```

`src/main/resources/META-INF/native-image/<groupId>/<artifactId>/reflect-config.json`에 놓는다. 자동으로 picked up된다.

여기서 한 가지 의문이 생긴다. *모든 라이브러리마다 이걸 다 손으로 작성해야 하나?* 다행히 아니다. GraalVM 팀이 운영하는 [`oracle/graalvm-reachability-metadata`](https://github.com/oracle/graalvm-reachability-metadata) 리포지토리가 있다. 주요 라이브러리(Jackson, Hibernate, Logback 등)의 힌트가 이미 모여 있다. Maven/Gradle 플러그인이 빌드 시 자동으로 가져온다.

그런데 — 이 리포지토리에 *없는* 라이브러리를 만나면 어떻게 될까. 솔직히 난감하다. 한국에서 자주 쓰는 NHN Toast 라이브러리, 카카오·네이버 OAuth SDK, MyBatis 한글 매퍼 같은 것들은 아직 메타데이터가 없을 가능성이 높다. 그때는 두 가지 선택지다. (a) 자신이 직접 힌트를 작성해 PR로 기여한다. (b) Tracing Agent로 자동 생성한다 — 이 이야기는 패턴 5에서 다루자.

한 가지 더, 자주 막히는 지점 하나. *프록시 객체의 리플렉션*이다. 예를 들어 Spring Data JPA의 리포지토리는 인터페이스인데, Spring이 런타임에 구현체를 만들어 끼운다. 그 구현체에 reflection으로 메서드를 호출하려 하면 메서드가 *프록시의 declared method가 아니어서* 찾지 못하는 경우가 있다. 이때는 *프록시의 인터페이스*와 *프록시될 구체 메서드*를 함께 등록해야 한다.

```java
@Override
public void registerHints(RuntimeHints hints, ClassLoader cl) {
    hints.reflection().registerType(UserRepository.class,
        MemberCategory.INVOKE_DECLARED_METHODS,
        MemberCategory.PUBLIC_METHODS);
    
    // 부모 인터페이스도 함께
    hints.reflection().registerType(JpaRepository.class,
        MemberCategory.INVOKE_DECLARED_METHODS);
    hints.reflection().registerType(CrudRepository.class,
        MemberCategory.INVOKE_DECLARED_METHODS);
}
```

이 패턴이 *Spring Data Repository 인터페이스*에서 자주 막힌다. 일반적 reflection 등록만으로는 부족하고 상속 사슬 전체를 살려야 한다. Spring AOT가 대부분은 자동으로 잡아주지만, 사용자 정의 리포지토리 인터페이스에 *복잡한 메서드 시그니처*가 섞이면 한 번씩 깨진다.

또 한 가지 자주 만나는 패턴은 **enum의 reflection 사용**이다. Jackson이 enum을 deserialize할 때 reflection으로 `values()`를 호출한다. enum 타입을 reflection 등록하지 않으면 *deserialize는 동작*하지만 그 결과가 null이거나 첫 번째 값으로 고정되는 *조용한 버그*가 난다. 이 케이스는 빌드도 통과하고 런타임에 예외도 안 나서 *발견이 가장 늦다*. 그래서 더 위험하다. enum 타입은 *전부* reflection 등록해두는 편이 안전하다.

```java
hints.reflection().registerType(OrderStatus.class,
    MemberCategory.PUBLIC_FIELDS,
    MemberCategory.INVOKE_PUBLIC_METHODS);
```

Spring Boot 3.2 이후 `@Reflective` 어노테이션이 추가됐다. enum이나 DTO 클래스에 붙이면 자동으로 reflection 힌트가 등록된다. 어노테이션을 코드에 직접 박는 게 부담이라면, 별도 `RuntimeHintsRegistrar`에 enum 패키지 전체를 스캔해 등록하는 방법도 있다. *어느 쪽이든* 명시적으로 챙겨두자.

### 패턴 3: 리소스 못 찾음 — 패턴으로 등록

```
java.io.FileNotFoundException: class path resource [messages/error_ko.properties] cannot be opened
```

이 메시지를 보면 처음에는 *클래스패스 문제인가* 의심하게 된다. 하지만 JVM 모드에서는 멀쩡히 동작했다면 99% Native Image의 리소스 처리 문제다.

Native Image는 빌드 타임에 *명시적으로 등록된 리소스만* 바이너리에 포함시킨다. 등록되지 않은 파일은 그냥 존재하지 않는 셈이다. `.properties`, `.yml`, `.sql`, 정적 HTML, 메시지 번들 — 이 모두가 잠재적 함정이다.

해결은 단순하다. 패턴으로 등록하면 된다.

```java
hints.resources().registerPattern("messages/.*\\.properties");
hints.resources().registerPattern("META-INF/sql/.*\\.sql");
hints.resources().registerPattern("static/.*");
```

혹은 `resource-config.json`으로.

```json
{
  "resources": {
    "includes": [
      {"pattern": "messages/.*\\.properties"},
      {"pattern": "META-INF/sql/.*\\.sql"}
    ]
  }
}
```

Spring Boot 3.x는 일부 자동 등록을 해준다 — `application.yml`이나 `messages.properties`는 알아서 잡힌다. 하지만 *언어별 메시지 번들*이나 *마이그레이션 SQL 파일* 같은 것들은 명시 등록이 안전하다.

자주 빠뜨리는 함정 하나 더. `META-INF/services/` 아래의 ServiceLoader 파일들. JDK 표준 ServiceLoader는 GraalVM이 자동으로 처리하지만, 일부 라이브러리가 *커스텀 서비스 디스커버리*를 구현하면 따로 등록해야 한다. 빌드는 통과하고 런타임에 "프로바이더가 없습니다" 같은 정체불명의 에러가 뜬다면 ServiceLoader 의심해볼 만하다.

여기서 한 가지 더 깊이 들어가보자. **리소스 등록의 *역방향 문제*도 있다.** 너무 많이 등록하면 바이너리가 비대해진다. 예를 들어 `.*`라는 패턴으로 모든 클래스패스 리소스를 등록하면 빌드는 통과한다. 하지만 바이너리에 200MB가 추가된다. 클래스패스에 우연히 들어 있는 README, 사용 안 하는 SQL 마이그레이션, 테스트 fixture들이 다 들어간다. 

원칙은 *정확히 필요한 패턴만*이다.

```java
// 나쁜 예 — 너무 많이 등록
hints.resources().registerPattern(".*\\.json");

// 좋은 예 — 정확히 어디서 쓰는지 명시
hints.resources().registerPattern("data/initial/.*\\.json");
hints.resources().registerPattern("config/feature-flags\\.json");
```

이게 *일상의 부주의*가 누적되면 운영 바이너리가 200~300MB가 된다. 컨테이너 이미지 크기와 ECR 다운로드 시간에 그대로 영향을 미친다. 정기적으로 `target/native/reachability-metadata-dump.json`을 들여다보고 *불필요한 등록*을 청소하는 루틴이 있으면 좋다. 빌드 산출물의 *리소스 섹션 통계*를 한 번씩 검토하는 습관이 운영 비용을 줄인다.

**i18n 메시지 번들의 함정도 짚고 가자.** `messages_ko.properties`, `messages_en.properties`, `messages_ja.properties` 같은 언어별 번들은 `ResourceBundle.getBundle("messages", Locale.KOREAN)`처럼 *동적*으로 로드된다. GraalVM은 이 패턴을 자동 감지하지 못하는 경우가 있다.

```java
hints.resources().registerResourceBundle("messages");
hints.resources().registerResourceBundle("validation");
hints.resources().registerResourceBundle("errors");
```

`registerResourceBundle`은 *언어 접미사 포함 전체*를 자동으로 등록해준다. 한국어 + 영어 + 일본어를 모두 지원하는 서비스라면 *각 번들마다* 이 등록이 필요하다. 모르면 *한국어 사용자만 메시지가 안 뜨는* 부분 장애로 발현된다. *세계 어딘가 한 언어 사용자만 보이는 버그*는 운영에서 발견이 늦다.

### 패턴 4: JDK 프록시 오류 — `registerJdkProxy`

```
java.lang.UnsupportedOperationException: 
   Proxy class defined by interfaces [interface com.example.UserService] not found.
```

JDK 동적 프록시(`java.lang.reflect.Proxy.newProxyInstance(...)`)는 런타임에 인터페이스를 받아 *그 자리에서* 구현체를 생성한다. 본질적으로 closed-world와 충돌한다. GraalVM은 빌드 타임에 *어떤 인터페이스 조합으로 프록시가 만들어질지* 알아야 한다.

이건 사실 Spring 개발자가 자주 만나는 패턴이다. Spring AOP, `@Transactional`, Feign 클라이언트, MyBatis 매퍼 인터페이스 — 모두 JDK 프록시를 쓴다. Spring AOT가 5장에서 본 것처럼 *대부분*은 자동으로 잡아준다. 하지만 라이브러리가 *런타임에* 프록시를 만드는 패턴이라면 빠질 수 있다.

명시 등록은 이렇게.

```java
hints.proxies().registerJdkProxy(UserService.class);
hints.proxies().registerJdkProxy(
    UserService.class,
    AuditAware.class
);  // 다중 인터페이스 프록시
```

자주 헷갈리는 점 하나. **CGLIB 프록시는 JDK 프록시와 다르다.** CGLIB은 바이트코드 조작으로 *클래스* 프록시를 만든다. Spring은 `@Configuration` 클래스에 CGLIB을 쓰는데, GraalVM Native에서는 이 패턴이 안 된다. 그래서 Spring AOT가 5장에서 본 것처럼 `@Configuration` 클래스도 처리 시점을 빌드 타임으로 옮겨 *프록시를 만들 필요가 없게* 미리 풀어버린다. 이 영리한 회피가 Spring AOT의 핵심 가치 중 하나다.

여기서 한 가지 자주 만나는 진짜 함정. **`@Async`와 `@Scheduled`의 프록시 문제다.** 두 어노테이션 모두 AOP 기반이라 프록시를 만든다. `@Async`는 JDK 동적 프록시 또는 CGLIB 둘 다 가능한데, 빈 타입이 인터페이스를 구현하면 JDK 프록시로 떨어진다. 그 인터페이스가 RuntimeHints에 등록 안 되면 런타임에 `UnsupportedOperationException`이 난다. Spring AOT가 보통 자동 처리하지만, *조합이 복잡할 때* 빠진다.

예를 들어 이런 구조가 깨지기 쉽다.

```java
public interface NotificationService {
    void send(Message msg);
}

@Service
public class EmailNotificationService implements NotificationService {
    @Async
    @Override
    public void send(Message msg) { ... }
}
```

평소 JVM에서는 `@Async`가 JDK 프록시로 `NotificationService` 인터페이스를 감싼다. Native에서 빌드는 통과해도 런타임에 첫 호출 시 *프록시 클래스를 찾지 못한다는 에러*가 난다. 명시 등록이 필요하다.

```java
hints.proxies().registerJdkProxy(NotificationService.class);
```

이 패턴이 한국 백엔드 코드에서 자주 보인다. 사용자 알림, 이메일 발송, 로깅 같은 부수 작업을 `@Async`로 분리하는 게 일반적인 설계라서 그렇다. 그래서 운영 *첫 사용자가 메시지를 보내는 순간* 폭발하는 경우가 있다. *알림 코드가 빠지면 핵심 비즈니스는 동작*하니까 더 발견이 늦다. 

조금 더 일반적인 가이드. **AOP 어노테이션이 붙은 메서드의 클래스 타입과 인터페이스를 *모두* 검토하자.** `@Transactional`, `@Cacheable`, `@Async`, `@Scheduled`, `@PreAuthorize`, `@Retryable` — 이 모든 어노테이션이 프록시 기반이다. 빌드 직후 첫 통합 테스트에서 이 어노테이션이 붙은 메서드를 *모두 한 번씩* 호출해보는 게 검증의 첫걸음이다. 빌드 통과가 정상 동작을 보장하지 않는다는 점, 잊지 말자.

### 보너스 패턴 — JSON 직렬화의 *조용한* 함정

다섯 가지 패턴 외에 한 가지 더 짚어두자. Jackson을 통한 JSON 직렬화·역직렬화는 *조용히* 깨진다. 빌드도 통과하고, 런타임에 예외도 거의 안 난다. 다만 *결과가 비어 있거나 잘못된다*. 이게 가장 위험하다.

예를 들어 이런 DTO를 보자.

```java
public record UserResponse(
    String name,
    int age,
    List<String> roles
) {}
```

JVM에서는 잘 동작한다. Native Image에서는 *직렬화 결과의 필드가 누락*되거나 *역직렬화 시 모든 필드가 null*인 현상이 일어날 수 있다. 이유는 Jackson이 record의 접근자 메서드(`name()`, `age()`, `roles()`)에 reflection으로 접근하는데, reachability metadata에 등록되지 않으면 Jackson이 "이런 필드가 없다"고 판단해 무시한다.

해결은 두 갈래다.

```java
// 방식 1: 어노테이션
@Reflective
public record UserResponse(...) {}

// 방식 2: RuntimeHints에서 명시 등록
hints.reflection().registerType(UserResponse.class,
    MemberCategory.INVOKE_DECLARED_CONSTRUCTORS,
    MemberCategory.INVOKE_DECLARED_METHODS,
    MemberCategory.DECLARED_FIELDS);

// 방식 3: Spring Boot 3.2의 자동 처리
// @RestController 메서드의 반환 타입은 Spring AOT가 자동 등록
```

가장 안전한 패턴은 **Controller 메서드의 입출력 DTO를 *명시적으로* RuntimeHintsRegistrar로 모아두는 것**이다. Spring AOT가 자동으로 잡는 경우가 많지만, *복잡한 제네릭*이나 *간접 참조*가 끼면 빠진다. 자기 도메인 모델만큼은 손으로 챙기는 편이 안전하다.

이 패턴의 *조용한 버그* 성격을 다시 강조하고 싶다. 운영 배포 후 API가 정상 200을 반환하는데 *응답 본문이 비어 있는* 사고를 만나면, 디버깅의 시작점이 어디인지 막막하다. 로그에도 단서가 없다. 클라이언트가 *몇 시간 뒤에야* "응답이 이상하다"고 알려온다. 그래서 **DTO reflection 등록 누락은 *통합 테스트로 반드시* 검증**해야 한다. 빌드 통과만으로 안전하다고 생각하면 안 된다.

### 패턴 5: Tracing Agent — 자동 힌트 생성과 그 한계

지금까지 본 네 패턴은 결국 같은 동작이다 — 빌드 타임에 알려주지 못한 정보를 *손으로* 보강한다. 그렇다면 의문이 든다. *그 정보를 자동으로 수집하면 안 되나?* 

GraalVM 팀도 같은 질문을 했다. 답이 Tracing Agent다.

```bash
java -agentlib:native-image-agent=config-output-dir=src/main/resources/META-INF/native-image/myapp \
  -jar app.jar
```

JVM에 이 agent를 붙이면 실행 중에 만나는 *모든* reflection·resource·proxy 호출을 기록한다. 통합 테스트나 부하 테스트를 한 번 돌리고 나면 `META-INF/native-image/` 아래에 다섯 개 JSON 파일이 자동으로 생긴다. 다음 Native 빌드는 그 힌트를 자동으로 읽는다.

이론적으로는 완벽하다. 실전에서는 *반쪽짜리 답*이다. 왜 그럴까?

**한계 1: 커버리지가 100%가 아니다.** Agent는 *실행된* 경로만 기록한다. 통합 테스트가 다루지 않은 분기, 예외 처리 경로, 특정 환경변수 조합에서만 도는 코드는 잡히지 않는다. 운영에서 만나는 첫 사용자가 그 경로를 밟으면 폭발한다. 부하 테스트 시나리오를 *최대한 두껍게* 만들어야 하는데, 그 자체로 큰 일이다.

**한계 2: 너무 많이 잡는다.** 반대 문제도 있다. Agent가 한 번 본 reflection 호출은 다 등록한다. 디버그 라이브러리가 잠깐 들춰본 클래스, 테스트 환경에서만 쓰는 mock 객체까지 다 들어간다. 그래서 결과 reachability-metadata가 *비대해진다*. 바이너리 크기와 빌드 시간이 늘어난다. 

**한계 3: 진단 가치가 사라진다.** Agent를 켜놓고 빌드를 통과시키면 *왜 그 힌트가 필요한지* 모르게 된다. 한 라이브러리를 업데이트했을 때 새 힌트가 필요해진 건지, 기존 힌트가 더 이상 필요 없는 건지 추적이 어려워진다. *자동화의 그늘*이다.

권장 운용은 이렇다. **Agent는 처음 도입 단계와 새 라이브러리 추가 시점에만**. 그 결과를 *그대로* 채택하지 말고, 진단 자료로 본 다음 *손으로 정리한 힌트*를 코드에 둔다. 통합 테스트가 정말 두꺼우면 agent 결과를 검증된 source of truth로 쓸 수 있지만, 그 정도 테스트 두께를 갖춘 팀은 사실 흔치 않다.

여기에 한 가지 토비식 당부를 덧붙이자. *agent에 의존하기 시작하면 closed-world의 의미가 흐려진다*. 6장에서 우리가 받아들였던 결단 — "빌드 타임에 다 알려져야 한다" — 이 사실상 "테스트가 한 번 본 것만 알려진다"로 변질된다. 그게 정말 우리가 원하는 안전성일까? 한번 생각해볼 일이다.

## PGO: 이론과 운영 사이

자, 빌드가 되고 트러블슈팅도 마무리됐다고 해보자. Native 바이너리가 운영에서 동작한다. 시작 시간 50ms, 메모리는 절반. 만족스럽다. 그런데 한 가지 아쉬운 점이 보인다. *피크 처리량이 JVM 대비 살짝 낮다*. 50,000 RPS를 받던 서비스가 Native로 가니 40,000 RPS에서 한계가 온다.

이 격차는 어디서 오나? JIT의 적응형 최적화가 사라졌기 때문이다. JVM은 운영 중에 hot path를 발견하고 C2 컴파일러로 인라이닝·escape analysis·loop unrolling을 적용한다. Native는 빌드 타임에 *한 번* 최적화하고 끝이다. 운영 중 워크로드 패턴에 맞춰 다시 컴파일할 기회가 없다.

여기서 등장하는 게 PGO(Profile-Guided Optimization)다. 이름 그대로 *프로파일을 가이드로 최적화*한다. 개념은 단순하다.

```
1단계: --pgo-instrument로 instrumented 바이너리 빌드
2단계: 대표 워크로드를 그 바이너리에 흘려 default.iprof 생성
3단계: --pgo=default.iprof로 최종 빌드
```

이론적으로는 JIT가 *런타임에* 하는 일을 *빌드 타임에* 시뮬레이션하는 셈이다. 결과 바이너리는 hot path가 미리 최적화돼 있고, 분기 예측과 인라이닝 결정이 워크로드에 맞게 조정된다. Oracle 문서는 약 6% 런타임 속도 향상, 15% 바이너리 크기 감소를 보고한다.

하지만 이론과 운영 사이에는 *세 개의 벽*이 있다.

### 벽 1: Enterprise 한정

PGO는 Oracle GraalVM Enterprise(현재는 Oracle GraalVM)에서만 제공된다. Community Edition에는 없다. 이게 무엇을 의미하나? 라이선스 비용이 발생할 수 있고, 사내 컴플라이언스 검토가 필요하다. 작은 팀이나 오픈소스 프로젝트는 PGO를 *고려조차 할 수 없다*. 시작부터 진입 장벽이 있다.

이 문제를 GraalVM 팀도 인식해서, **ML 기반 추론 프로파일**을 *기본값으로* 적용한다. PGO 명령을 안 써도 빌드 타임에 머신러닝 모델이 "이런 패턴의 코드는 이렇게 최적화되어야 한다"는 일반화된 프로파일을 적용한다. 효과는 PGO보다 작지만 *공짜*다. CE 사용자도 일부 이득을 본다. 이게 GraalVM 6.0 이후의 기본 동작이다.

### 벽 2: instrumented 바이너리는 운영 불가

이 한계가 가장 치명적이다. PGO의 1단계 — instrumented 빌드 — 결과 바이너리는 *느리다*. 모든 메서드에 카운터를 박아두기 때문에 30~50% 오버헤드가 있다. 디스크 I/O도 증가한다. 즉, 이 바이너리를 *운영 트래픽에 노출시킬 수 없다*. 

그렇다면 어떻게 프로파일을 모아야 하나? 두 갈래다.

**(a) 합성 벤치마크.** 운영 워크로드를 시뮬레이션하는 부하 테스트를 만든다. JMeter, Gatling, k6 같은 도구로 합성 트래픽을 만들어 instrumented 바이너리에 흘린다. 하지만 *합성과 실제 사이의 격차*가 항상 문제다. 운영의 분기 패턴, 데이터 분포, 에러 비율을 100% 재현하기 어렵다. 결과 프로파일은 *부분적*이다.

**(b) 운영의 그림자.** 일부 트래픽을 운영에서 instrumented 바이너리로 mirroring한다. 사용자에게는 보여주지 않고, 백그라운드에서만 돌린다. 더 현실적인 프로파일을 얻지만 인프라가 복잡해진다. *PGO를 위해 별도 인프라를 운영해야 한다*는 셈이다.

대규모 마이크로서비스 팀이 아니라면 (b)는 사실상 불가능하다. 그래서 PGO는 *대기업 + 안정적 워크로드* 조합에서나 실용적이다.

### 잠깐 — PGO를 *그래도* 시도해본다면

여기서 한 가지 시나리오를 짚고 가자. *우리 팀이 PGO를 쓸 수 있는 조건에 있다*면 어떻게 시작하나? Oracle GraalVM 라이선스가 있고, 워크로드가 안정적이며, 별도 인프라 비용을 감당할 수 있다는 가정에서다.

표준 워크플로우는 3단계다.

```bash
# 1단계: instrumented 바이너리 빌드
./mvnw -Pnative native:compile -Dnative.maven.plugin.args="--pgo-instrument"

# 2단계: 대표 워크로드 실행 → default.iprof 생성
./target/myapp &
APP_PID=$!
# JMeter나 k6로 부하 테스트 실행
k6 run loadtest.js
kill $APP_PID
# default.iprof가 생성됨

# 3단계: 프로파일 기반 최종 빌드
./mvnw -Pnative native:compile \
  -Dnative.maven.plugin.args="--pgo=default.iprof"
```

여기서 *2단계가 가장 까다롭다*. 대표 워크로드를 어떻게 만들지가 PGO 성공의 80%를 결정한다. 권장 패턴은 이렇다.

**(a) 운영 트래픽의 분석:** 지난 30일 운영 로그에서 *상위 80% 트래픽을 만든* API 엔드포인트와 그 호출 비율을 추출. 이 비율로 k6 시나리오를 작성.

**(b) 분기 커버리지 보강:** 정상 응답뿐 아니라 에러 응답, 인증 실패, rate limit 등의 *비주류 분기*도 일정 비율로 포함. 이 분기들도 *컴파일된 핫 패스*에 들어가야 한다.

**(c) 데이터 분포 모사:** 실제 운영 데이터의 분포(예: 한국 사용자의 한글 입력 비율, 특정 사용자 그룹의 비중)를 시뮬레이션. 동일 입력만 반복하면 *과적합된 프로파일*이 나와서 운영에서 역효과가 날 수 있다.

이 세 가지를 다 갖춘 부하 테스트를 만들려면 *전담 엔지니어 1명이 한 분기*는 잡아먹는다. 그래서 PGO는 큰 회사에서나 의미가 있다. 일반화하자면 *연간 운영비가 PGO 인프라 구축 비용을 압도하는* 워크로드에서만 ROI가 나온다. *Lambda에서 매달 수억 건 호출*되는 핵심 서비스 같은 게 그 예다.

작은 팀에 대한 정직한 조언. PGO는 *없다고 가정하자*. ML 추론 프로파일과 적절한 RuntimeHints 정제로 충분히 만족스러운 결과를 얻을 수 있다. PGO 도입에 시간 쓰느니, 같은 시간을 *진단 도구 학습*과 *리포지토리 정리*에 쓰는 게 운영 효율로 직결된다.

### 벽 3: 워크로드 변화

PGO의 또 한 가지 함정. *워크로드는 변한다*. 비즈니스 로직이 바뀌고, 새 기능이 추가되고, 트래픽 패턴이 진화한다. 6개월 전 모은 프로파일이 지금도 유효할까? 어쩌면 *역방향*으로 최적화되어 있을 수도 있다. PGO를 도입한 팀은 *프로파일 재수집을 정례화*해야 한다. 분기마다? 매달? 새 기능 출시마다?

이 모든 비용을 다 감안하면, PGO는 *워크로드가 안정적인 마이크로서비스에서만* 의미가 있다. 자주 변하는 비즈니스 로직 위에 PGO를 얹으면 운영 부담만 늘고 이득은 작아진다. 그래서 GraalVM 팀의 권고는 정직하다 — **"PGO 안 써도 ML 추론 프로파일로 일정 이득은 본다. 그 정도로 만족하라."**

토비식으로 정리하자. PGO는 *멋진 도구*다. 하지만 우리 대부분에게는 *호화로운 도구*다. ML 추론 프로파일을 켜두고 기본 빌드로 만족하는 편이 낫다. *시작 50ms와 메모리 절반*이라는 본질 가치는 PGO 없이도 누릴 수 있다. PGO에 매달리다 운영 인프라가 복잡해지는 게 *진짜 손해*다.

### ML 추론 프로파일이라는 *공짜*

여기서 한 번 더 강조하고 싶은 게 있다. ML 추론 프로파일(ML-based profile inference)은 GraalVM 23 이후 *기본값으로* 켜져 있다. 별도 옵션을 켜지 않아도, 빌드 타임에 GraalVM이 자체 학습된 모델로 "이런 코드 패턴은 이렇게 최적화하는 게 좋다"는 일반적 프로파일을 적용한다. 

효과는 PGO보다 작지만 *완전 공짜*다. Community Edition에서도 동작한다. 별도 인프라도 필요 없다. 빌드 한 번에 추가 시간이 거의 안 든다. 그런데 의외로 많은 개발자가 *이 사실을 모른다*. PGO가 Enterprise 한정이라는 이야기에 좌절해서 "그러면 Native는 피크 처리량이 영원히 JVM보다 느린가" 결론을 내린다. 그게 아니다.

벤치마크를 보면 ML 추론 프로파일이 켜진 GraalVM CE는 *순수 PGO 없는 빌드 대비* 약 2~4% 처리량 향상이 있다. PGO와 비교하면 절반 정도지만, 비용은 0이다. *얻을 수 있는 건 다 얻자*는 자세로 충분하다.

만약 더 욕심을 내고 싶다면, **iterative profiling**이라는 우회로가 있다. 운영에서 일정 기간 JVM 모드로 앱을 돌려 Spring AOT의 RuntimeHints를 채취한 다음, 그 힌트를 가지고 Native 빌드를 한다. 이건 PGO는 아니지만 *비슷한 발상*이다 — *실제 호출 패턴을 빌드에 반영*. RuntimeHints가 GraalVM의 reachability 분석을 더 정밀하게 만들어 *불필요한 코드 제거*를 통한 바이너리 크기 감소를 가져온다. 이 패턴은 사실상 누구나 할 수 있는 *poor man's PGO*다.

## Liberty Mutual 사례 심층 — 9배 단축, 그러나

Native Image 도입 사례 중 가장 많이 인용되는 게 Liberty Mutual이다. 미국의 대형 보험사로, Spring Cloud Function을 AWS Lambda 위에서 운영한다. 그들이 InfoWorld에 공개한 숫자를 정리해보자.

| 항목 | 값 |
|------|---|
| 이전 (Spring Boot JVM Lambda) | Init Duration **5,770 ms** |
| 이후 (Native, Zip 배포) | Init Duration **655 ms** |
| 단축률 | **약 9배** |
| 워밍 후 처리 duration | 20 ms / 함수 호출당 |
| 바이너리 크기 | 160 MB |
| 동시 실행 cold start 확률 | 거의 0 |

숫자만 보면 그저 멋진 성공담이다. *5.7초가 0.65초가 됐다*. Lambda 환경에서 이 격차는 비용으로 직결된다. Init Duration이 줄면 *Init phase 과금*이 줄어들고, cold start로 발생하던 타임아웃과 SLA 위반이 사라진다. 보험 청구 처리 API에서 cold start로 인한 9배 지연은 사용자 경험에서 *재앙*이다.

그런데 — 이 사례를 *얕게 인용*하고 끝내면 잘못된 교훈을 얻기 쉽다. Liberty Mutual의 발표를 자세히 읽으면 *세 가지 함정*이 같이 적혀 있다.

### 함정 1: OCI 컨테이너 회귀

Liberty Mutual은 처음에 Native 바이너리를 **Lambda Zip 형식**으로 배포했다. 결과가 655ms. 그런데 같은 코드를 **OCI 컨테이너 형식**으로 배포하니 *3.4초*로 회귀했다. 5배 이상 느려진 것이다.

원인은 ECR 이미지 다운로드 오버헤드였다. 컨테이너 이미지는 Lambda가 ECR에서 끌어와 압축을 풀고 마운트해야 한다. Native 바이너리가 아무리 빨라도, 이 *컨테이너 부팅 비용*이 그대로 추가된다. Zip 배포는 Lambda 자체가 최적화된 경로로 다루기 때문에 다운로드 오버헤드가 거의 없다.

여기서 얻을 교훈은 무엇일까? **Native의 시작 시간 이득은 배포 모델과 결합되어야 한다.** Lambda Zip은 250MB 제한이라 큰 바이너리는 곤란하다. 하지만 Native는 보통 150~200MB로 들어간다. 만약 컨테이너 이미지를 *반드시* 써야 하는 사정이 있다면 — 예를 들어 OS 의존성을 묶어야 한다든지 — Native의 이득이 *부분 상쇄*된다는 점을 인정해야 한다. *맥락 없이 9배만 외우면 함정에 빠진다*. 

### 함정 2: Spring profiles 동적 해석 불가

Liberty Mutual이 가장 고생한 부분이 이거였다. Spring profiles. 평소 Spring Boot 앱은 환경변수 `SPRING_PROFILES_ACTIVE`로 profile을 동적 결정한다. dev, staging, prod가 같은 jar 파일에서 환경변수 한 줄로 갈린다.

Native Image에서는 이게 안 된다. *왜?* closed-world 때문이다. profile별로 활성화되는 빈이 달라지면, GraalVM이 *어떤 빈이 도달 가능한지* 빌드 타임에 결정해야 한다. profile이 런타임에 정해지면 closed-world 분석이 *모든 가능성*을 함께 다 살려둬야 하는데, 그러면 도달 가능 그래프가 폭발한다.

GraalVM은 이 문제를 *원천적으로 막는다*. Spring AOT는 빌드 타임에 *활성 profile을 고정*하고 그 profile에 맞춰서만 빈 그래프를 만든다. 결과로:
- profile이 dev/staging/prod로 갈리면 **각각 별도 빌드**가 필요하다.
- 또는 *환경별 분기를 환경변수 외부화*로 풀어야 한다. 예: profile 대신 `@Value("${app.feature-x.enabled}")`로 빈 동작을 분기.

Liberty Mutual은 두 번째 길을 갔다. *프로파일 의존도를 줄이고, 동작 분기를 환경변수 기반 condition으로 옮겼다*. 코드 베이스 전체에서 `@Profile` 사용처를 찾아 리팩토링한 셈이다.

이게 *얼마나 큰 작업*인지 짐작이 갈 것이다. 중규모 Spring 앱에서 `@Profile`을 50군데 쓰고 있다고 해보자. 각 사용처를 *런타임 조건*으로 바꾸려면 빈 구조, 설정 클래스, 자동설정 의존성을 다 손봐야 한다. *Native 도입 비용의 절반이 여기서 나온다*는 추정도 과장이 아니다.

### 함정 3: 디버깅의 그림자

Liberty Mutual이 명시적으로 강조하지는 않았지만, 그들의 후속 발표와 GraalVM 컨퍼런스 토크를 보면 *운영 디버깅의 어려움*이 반복적으로 등장한다. Native Image는 JFR 지원이 제한적이고, async-profiler의 일부 기능이 동작하지 않으며, jstack/jmap 같은 표준 진단 도구가 통하지 않는다. 운영에서 *왜 이 함수가 느린지* 알아내려면 새로운 도구 세트를 배워야 한다.

물론 GraalVM에도 진단 도구가 있다 — `native-image-inspect`, GraalVM Dashboard, 일부 JFR 이벤트. 하지만 *학습 곡선*이 있다. 사내에 GraalVM 디버깅 노하우가 없으면 운영 사고 대응이 느려진다. *9배 빨라진 시작 시간*과 *5배 느려진 사고 대응*은 다른 차원의 비용이다. 

### Liberty Mutual에서 배울 것

이 사례는 *Native가 옳지 않다*는 이야기가 아니다. 정반대다. Liberty Mutual은 *실제로 성공했다*. 그러나 그 성공의 이면을 정직하게 들여다보면:

1. **워크로드의 적합성**: 짧은 수명 Lambda 함수. Native가 가장 잘 맞는 유형이다. 긴 수명 EKS 백엔드였다면 같은 ROI가 안 나왔다.
2. **배포 모델의 선택**: Zip 배포. 컨테이너였다면 효과가 반쪽이었다.
3. **profile 리팩토링**: 코드 베이스 전체에 걸친 작업. 작은 팀이라면 감당이 어렵다.
4. **사내 GraalVM 전문성**: 인용된 발표자들은 GraalVM에 깊이 들어간 엔지니어들이다. *팀에 그런 사람이 있는가*가 도입 결정의 첫 변수다.

이걸 *낭만 없이* 본 시각이다. 9배 단축이라는 헤드라인 뒤에 *9배만큼의 사전 조건*이 있었다. 우리 팀에 그 조건들이 다 갖춰져 있나? 그 점을 먼저 따져보는 편이 낫다.

### Liberty Mutual이 *말하지 않은* 부분도 보자

공식 발표에 명시되지 않았지만 GraalVM 컨퍼런스 토크와 후속 인터뷰에서 흘러나온 정보가 있다. *조직적 비용*이다.

Liberty Mutual은 GraalVM 도입을 위해 *전담 플랫폼 팀*을 두었다. 정확한 인원은 공개되지 않았지만 최소 3~5명의 시니어 엔지니어가 *GraalVM 운영*에 시간을 할애하는 것으로 추정된다. 이 팀이 하는 일이 정말 많다.

- 새 라이브러리 도입 시 reachability metadata 검증
- 빌드 파이프라인 유지보수와 캐싱 최적화
- 운영 사고 발생 시 GraalVM 측면 디버깅 지원
- 내부 트레이닝 자료 작성과 다른 팀 onboarding
- Spring 메이저 업그레이드 시 RuntimeHints 호환성 검증

이 다섯 가지가 *일상의 운영 작업*으로 추가된다. 평소 Spring Boot JVM을 운영하는 팀이라면 이런 일은 *거의 없다*. JVM 위에서 라이브러리가 호환되지 않을 가능성이 1% 미만이고, 빌드 파이프라인도 단순하며, 사고 디버깅은 표준 도구로 충분하다. Native는 *이 모든 일을 다시 만든다*. 

그래서 한 가지 질문이 자연스럽게 떠오른다. **Liberty Mutual이 *지금* 다시 결정한다면 어떻게 할까?** 흥미롭게도 그들의 후속 토크에서는 *조심스러운 어조*가 보인다. "우리에게는 잘 맞았지만, *모든 워크로드에* 추천하지는 않는다"는 식의 단서가 자주 붙는다. 9배 단축의 성공담을 자랑하면서도 *일반화의 위험*을 본인들이 의식하고 있는 셈이다.

이게 *큰 회사의 도입 사례*를 읽는 올바른 방법이다. 헤드라인 숫자가 아니라 *조직 구조의 변화*까지 함께 보는 것. 우리 팀이 *5명의 플랫폼 엔지니어를 전담시킬 수 있는가*를 먼저 자문해야 한다. 답이 *아니오*라면, Liberty Mutual의 9배는 우리 것이 아니다.

## Spring profiles와 Native Image — 어떻게 함께 갈까

Liberty Mutual의 profile 함정은 우리 모두가 만날 문제다. 조금 더 자세히 들여다보자.

Spring profiles는 두 시점에 평가된다. 하나는 *컴파일 시점*(빈 정의의 활성화 여부), 다른 하나는 *런타임 시점*(설정 값 바인딩, 빈 동작 분기). Native Image는 *컴파일 시점 평가를 빌드 타임에 고정*한다. 그래서 다음과 같은 패턴들이 문제가 된다.

```java
// 패턴 A: 빈 활성화 분기 — 빌드 타임에 고정됨
@Configuration
@Profile("production")
public class ProductionDatabaseConfig {
    @Bean DataSource ds() { ... }
}

// 패턴 B: ConditionalOnProperty — Native에서도 OK
@Bean
@ConditionalOnProperty(name = "app.cache.enabled", havingValue = "true")
public Cache cache() { ... }

// 패턴 C: 런타임 조건 — Native에서도 OK
@Bean
public NotificationService notification(
    @Value("${app.notification.channel}") String channel) {
    return switch (channel) {
        case "email" -> new EmailService();
        case "sms" -> new SmsService();
        default -> new NoOpService();
    };
}
```

패턴 A는 빌드 타임 결정이다. `--Pnative -Dspring.profiles.active=production`으로 빌드하면 production용 바이너리가 나오고, 다른 환경에서는 다시 빌드해야 한다.

패턴 B와 C는 런타임에 동작한다. 환경변수나 설정 파일로 분기가 가능하다. *환경별 빌드를 한 번만 하고* 운영에서 환경변수로 차이를 만들 수 있다.

그렇다면 어떻게 마이그레이션해야 할까? 두 길이 있다.

**(a) 환경별 빌드 분리.** dev/staging/prod 각각 별도 Native 빌드. CI 파이프라인이 복잡해지고 ECR 이미지 수가 늘어난다. *변경 시마다 세 번 빌드해야* 한다. 작은 팀에는 부담이다.

**(b) profile을 property로 옮긴다.** `@Profile("production")`을 `@ConditionalOnProperty`로 변경. 빈을 두 개 다 정의해두고 런타임 조건으로 활성 하나만 선택. 코드는 조금 늘지만 *빌드는 한 번*. 운영 유연성이 높다.

대부분의 팀은 (b)가 정답이다. (a)는 *환경별 동작 차이가 정말 크고 보안적으로 분리가 필요한 경우*에만 의미가 있다.

여기에 한 가지 더 토비식 당부. **profile은 *생성* 시점에 고정되는 정보로만 쓰자**. "이건 production인가, dev인가" 같은 환경 정체성. 그 외의 모든 *행동 분기*는 property로 옮기는 편이 낫다. 그러면 profile은 *빌드 산출물의 이름*에 가까워지고, 동작은 *런타임 설정*으로 분리된다. 책임 분리가 깔끔해진다.

## 한국 커뮤니티의 실패담

이 책을 쓰면서 한 가지 솔직히 인정해야 할 점이 있다. *한국 기업의 공식 Native Image 도입 사례*를 찾지 못했다. 토스, 카카오, 네이버, 쿠팡 — 어디에도 회사 공식 기술 블로그에 GraalVM Native를 운영에 적용했다는 글이 없다. 검색에서 잡히는 건 개인 학습 블로그(velog)와 OKKY 토론뿐이다.

이건 데이터의 한계다. 하지만 한편으로는 *그 자체가 신호*이기도 하다. 한국 대형 백엔드 팀들이 Native를 운영에 안 가져간 데에는 이유가 있을 것이다. 그래서 이 절에서는 한국 개발자들의 *실패담*을 인용해본다. 학습 자료라 일반화는 조심스럽지만, *어떤 함정에서 멈췄는지*는 보편적이다.

### velog @profoundsea25 — "SpringBoot 3, GraalVM Native Image 적용 실패담"

이분은 사이드 프로젝트에 Native Image를 적용해보려다 *세 번 막혔다*고 정리해두었다. 인용해보자.

> 빌드는 됐다. 그런데 실행 시점에 JPA 엔티티의 setter를 못 찾는다는 에러가 떴다. Hibernate가 리플렉션으로 접근하는데, RuntimeHints가 잡지 못한 모양이었다. 한참 헤매다 reflect-config.json을 손으로 작성해서 넘겼다.

이 패턴이 우리가 본 *패턴 2*다. Hibernate가 사용하는 reflection이 자동 힌트로 커버되지 않은 경우다. GraalVM Reachability Metadata 리포지토리에 Hibernate 메타데이터가 있긴 한데, 버전 매칭이 안 되거나 사용자 엔티티의 특정 필드 접근이 누락된 케이스가 있다.

> 두 번째 벽은 Lombok이었다. Lombok이 생성하는 코드가 빌드 시점에는 멀쩡한데, 그게 reflection으로 호출되는 어떤 경로에서 InvocationTargetException이 났다.

Lombok과 GraalVM의 조합도 한국 개발자 사이에 자주 보이는 토픽이다. Lombok 자체는 빌드 타임 처리라 GraalVM과 직접 충돌하지 않지만, *Lombok이 생성한 게터/세터를 reflection으로 부르는 라이브러리*가 있으면 그 자리에서 문제가 생긴다. Jackson, Hibernate, Spring Validator 등이 후보다.

> 결국 포기했다. 사이드 프로젝트라 들이는 시간 대비 이득이 안 보였다. JVM 모드로 Spring AOT만 켜고 끝냈다.

이게 *현실적인 결정*이다. 개인 학습용 사이드 프로젝트에서 cold start가 5초든 0.5초든 본질적으로 중요하지 않다. 트러블슈팅에 들인 며칠이 그 이득을 *압도적으로* 상회한다. 운영 ROI가 없는 환경에서 Native를 강행하는 건 *시간 낭비*다. 

### OKKY — "GraalVM은 아직 전격적으로 도입하기엔 무리인듯 하네요"

OKKY의 한 토론 글이 한국 백엔드 개발자 다수의 *현재 정서*를 잘 보여준다. 글쓴이는 GraalVM Native를 *진지하게* 검토했지만 다음과 같은 이유로 *유보*를 결정했다.

1. 빌드 시간이 길어 CI 비용이 늘어남
2. 라이브러리 호환성 lottery — 어떤 게 깨질지 미리 모름
3. 사내에 GraalVM 디버깅 가능한 사람이 없음
4. 시작 시간 단축의 ROI가 명확하지 않음 (Lambda 안 쓰는 환경)

이 네 가지가 *한국 백엔드 컨텍스트의 정직한 그림*이다. 한국 대형 서비스는 대부분 EKS나 자체 K8s 클러스터에서 *긴 수명 백엔드*를 운영한다. Lambda 같은 짧은 수명 워크로드 비중이 작다. 그러면 Native의 시작 50ms가 *비즈니스 가치로 환산되지 않는다*. 

그렇다면 답은 무엇인가? 8장에서 보게 될 CRaC, 그리고 10장에서 보게 될 Project Leyden이 더 적합한 후보다. *코드를 안 바꾸고 시작을 80%+ 줄이는* 길이 따로 있다. Native만이 답이 아니다. 한국 컨텍스트에서는 *Native가 답일 가능성이 더 작다*고 정직하게 말하는 편이 낫다.

### velog @harperkwon — "GraalVM 도입 효과 비교 정리"

이 글은 실패담은 아니지만, 한 가지 중요한 관찰을 담고 있다.

> Spring Boot 3 + JVM 모드 + AOT 활성화만으로도 시작 시간이 20% 줄었다. 코드 한 줄 안 고치고. Native까지 안 가도 이 정도면 충분히 의미 있는 것 같다.

이게 우리가 5장에서 본 *JVM 모드 AOT의 자주 놓치는 사실*이다. 많은 한국 개발자들이 GraalVM Native까지 가지 않고도 그 *전 단계*에서 만족스러운 결과를 얻고 있다. Native 도입 결정 전에 한 번쯤 *그 단계*에서 멈출 수 있는지 묻는 게 합리적이다.

### 한국 사례에서 배울 것

데이터 부족이라는 한계가 있지만, *공통된 그림*이 보인다. 한국의 개인 개발자들은 Native를 *시도했고*, 트러블슈팅의 벽을 만났고, *대부분 후퇴*했다. 회사 차원의 도입 사례는 *아직* 공식화되지 않았다.

이게 미래에도 그럴까? 그건 모른다. JEP 483과 Leyden이 본격 채택되면 *Native까지 가지 않아도* 비슷한 시작 가속을 얻을 수 있다. 그러면 Native의 상대 가치가 더 작아진다. 반대로 Lambda 같은 짧은 수명 워크로드가 한국 백엔드 비중에서 늘어나면 Native 도입이 가속될 수 있다. 변수가 많다.

우리가 확신할 수 있는 한 가지. *Native를 도입할 거면 한국 컨텍스트의 함정을 미리 알아두자*. Lombok·Hibernate·Jackson의 조합에서 어떤 reflection이 깨지는지, MyBatis 한글 매퍼가 GraalVM에서 어떻게 동작하는지(*아직 데이터 없음*), 한국 OAuth SDK(카카오·네이버) 호환성이 어떤지 — 이 정보들은 *직접 검증*해야 할 가능성이 크다. 채택 결정의 첫 변수가 *팀의 검증 역량*인 이유다.

### 한국 OSS 생태계에 한 가지 부탁

한 가지 솔직한 부탁이 있다. 만약 우리 회사가 Native를 *실패한 경험*이 있다면, 그 경험을 *공유해주면 좋겠다*. 회사 공식 블로그가 아니어도 좋다. 발표자 개인의 블로그, 사내 위키의 공개 가능한 부분, DEVIEW나 IF Kakao 같은 컨퍼런스 토크. *어떻게 망했나*가 사실 *어떻게 성공했나*보다 훨씬 가치 있는 정보다.

지금 한국 백엔드 생태계에는 *영어로 적힌 Liberty Mutual의 성공*만 도는 상태다. 같은 기술이 한국 컨텍스트에서 어떻게 *흔히 부서지는지*에 대한 집합지식이 부족하다. 그 빈자리를 채울 수 있다면 다음 세대 한국 개발자들의 의사결정이 더 합리적이 된다. 

이건 책의 범위를 벗어난 이야기지만, 저자로서 한 번은 말해두고 싶었다. *우리의 실패담은 누군가의 좋은 첫 결정*이 된다.

## 채택 결정의 첫 질문: 사내에 GraalVM 전문가가 있는가

11장의 결정 트리에서 본격적으로 다룰 내용이지만, 7장의 결론에 해당하는 *한 가지 질문*을 먼저 던지자.

> 사내에 GraalVM Native Image 트러블슈팅을 *주도적으로* 할 수 있는 사람이 1명 이상 있는가?

이 질문 하나로 채택 가능성의 70%가 결정된다. *왜 그럴까?* 

Native Image는 라이브러리 호환성 lottery다. 우리 팀의 의존성 트리에 어떤 라이브러리가 *언제* 어떻게 깨질지 예측 불가능하다. 새 라이브러리를 추가했더니 빌드가 깨진다. 기존 라이브러리가 메이저 업데이트했더니 reachability metadata가 안 맞는다. Spring Boot 마이너 버전을 올렸더니 RuntimeHints API가 달라졌다.

이 모든 사건은 *언젠가 일어난다*. 그리고 그때마다 *해결할 수 있는 사람이 필요하다*. 그 사람이 없으면 운영이 멈춘다. *몇 시간 안에 풀어야 할 사고*가 *며칠짜리 외부 컨설팅 의뢰*가 된다. 

여기서 한 가지 솔직한 질문을 더 던지자. *지금 우리 팀에서 그 역할을 누가 할 수 있나?* 만약 머릿속에 즉시 떠오르는 사람이 없다면, Native 도입은 *지금 시점에는 아직 이르다*. 도구를 도입하기 전에 *사람을 먼저 키우는* 편이 낫다. 한 명을 GraalVM 학습에 한 분기 정도 투자시키고, 그 사람이 사이드 프로젝트로 한 번 끝까지 가본 다음, 그제서야 운영 도입을 검토하는 순서다. 

그리고 한 가지 더. **전문가는 *대체 가능해야* 한다.** 한 명에게만 의존하면 그 사람이 퇴사하는 순간 우리는 Liberty Mutual의 *후속 절반*을 만난다. 시작 시간은 빠르지만 *디버깅이 불가능한* 운영 환경. 두 명 이상이 기본 검증된 노하우를 공유하고 있어야 한다. 그것까지 갖춰지면 비로소 *조직적 도입*이 가능하다. 

## GraalVM 라이선스 한 페이지 정리

마지막으로 짧게 라이선스 이야기를 정리하고 가자. 이게 *법무 검토 수준*은 아니지만, 도입 결정 전에 한 번 들여다볼 필요는 있다. 

2024년부터 Oracle은 GraalVM의 라이선스 구조를 한 번 더 정비했다. 핵심만 보자.

**Community Edition (CE):** GPL v2 with Classpath Exception. 무료. 운영에서도 자유 사용 가능. 대부분의 기능(Native Image, AOT 컴파일러)이 포함된다.

**Oracle GraalVM:** Oracle GraalVM Free Terms and Conditions (GFTC) 라이선스. 무료지만 *Oracle의 조건*을 따른다. PGO, 일부 고급 최적화, Enterprise 지원이 포함된다. 

**Oracle GraalVM Enterprise (구 명칭):** Oracle Java SE Subscription에 포함되는 상용 라이선스. 정식 지원, SLA, 보안 패치를 받는다.

여기서 *주의해야 할 변수*가 몇 가지 있다.

**(a) GFTC의 조건은 자주 바뀐다.** Oracle은 라이선스 텍스트를 주기적으로 개정한다. "지금은 자유롭게 운영 사용 가능"이라는 조건이 *내년에 같은가*는 보장이 없다. 2023년에 Java SE의 라이선스 정책이 바뀌어 한 차례 시끄러웠던 일을 기억해두자. 

**(b) PGO와 일부 최적화는 Oracle GraalVM 한정이다.** CE에서는 PGO를 못 쓴다. ML 추론 프로파일은 양쪽 다 된다. 우리 워크로드가 PGO 없이도 만족스럽다면 CE로 충분하다.

**(c) 컴플라이언스 검토가 필요할 수 있다.** 사내 법무팀이 OSS 라이선스 정책을 세웠다면 GFTC가 그 정책에 맞는지 확인해야 한다. GPL Classpath Exception은 보편적으로 안전한 라이선스로 인정되지만, GFTC는 *Oracle 고유* 조건이다.

권장 흐름은 이렇다. **사이드 프로젝트나 검증 단계는 CE로**. *운영 도입을 결정하기 전에* 사내 법무 검토를 거치고, 필요하면 Oracle 라이선스를 선택. 도입 후 *연 1회는* 라이선스 텍스트를 다시 확인하는 운영 루틴을 만들자. *기술 변수가 아닌 라이선스 변수로 운영이 흔들리는 일*이 한 번 일어나면 정말 끔찍하다. 미리 막아두는 편이 낫다.

대안 배포판도 짚고 가자. **Liberica Native Image Kit**, **Mandrel** 두 가지를 알아두면 도움이 된다.

- **Liberica NIK**: BellSoft가 배포하는 GraalVM 기반 빌드. GPL Classpath Exception. *Liberica JDK와 통합*되어 있고 한국에서 일부 회사가 JDK 공급원으로 BellSoft를 쓰는 경우 자연스럽게 후보가 된다.
- **Mandrel**: Red Hat의 GraalVM Native Image 다운스트림. *Quarkus와 함께 검증된 빌드*. Spring 사용자에게도 사용 가능하지만 Spring 팀이 공식 권고하는 건 *Oracle GraalVM 또는 Liberica NIK*다.

이 모든 배포판이 *기능적으로는 거의 동등*하다. 차이는 (a) 빌드 안정성, (b) 보안 패치 주기, (c) 상용 지원 가용성. 작은 팀이라면 Oracle GraalVM CE로 시작해도 충분하다. *라이선스 risk를 줄이고 싶다면* GPL Classpath Exception인 Liberica NIK가 일반적으로 안전하다. 

여기서 한 가지 토비식 권고. ***라이선스 결정은 빨리 끝내자*.** 도입 검증 단계에서 라이선스 변수가 결정되지 않으면 나중에 운영 환경에서 *배포판을 갈아끼우는 작업*이 생긴다. 같은 GraalVM 기반이라도 *세부 동작에서 미묘한 차이*가 있다. 빌드가 한 배포판에서는 통과하는데 다른 배포판에서는 깨질 수 있다. 처음부터 *운영에 쓸 배포판으로* 검증을 시작하는 게 낫다.

## 마무리

7장에서 우리는 Native Image의 *낭만 없는 현실*을 함께 봤다. 빌드 8분의 무게, 다섯 가지 트러블슈팅 패턴, PGO의 세 벽, Liberty Mutual 9배 단축 뒤의 세 함정, 한국 커뮤니티의 후퇴, 채택 결정의 첫 질문, 라이선스 변수. 6장의 철학과는 다른 색이다. *closed-world라는 결단*이 운영 현장에서 어떻게 비용으로 환산되는지를 본 셈이다.

여기서 한 가지 잊지 말아야 할 점이 있다. *Native Image는 좋은 도구다*. 시작 50ms, 메모리 절반, 컨테이너 이미지 100MB → 50MB. 이 가치들은 진짜다. 짧은 수명 함수형 워크로드에서 Native는 *압도적으로 잘 맞는다*. Liberty Mutual의 9배 단축은 *잘못된 숫자가 아니다*.

다만 그 가치를 누리는 데는 *비용*이 있다. 빌드 시간, 라이브러리 lottery, 디버깅의 그림자, 사내 전문성, 라이선스 변수. 이 비용을 *정직하게* 비교해야 한다. *낭만으로 Native를 도입하면* 18개월 뒤 JVM으로 후퇴하는 가상 사례(11장에서 다룬다)의 주인공이 될 수 있다.

기억해두자. 도구 자체에는 *옳고 그름*이 없다. 우리의 워크로드와 팀과 조직적 여건이 *그 도구와 맞는가*가 결정한다. 첫 질문은 늘 같다 — *우리에게 이게 필요한가, 우리에게 이걸 운영할 역량이 있는가*. 두 질문 모두에 *예*로 답할 수 있는 팀만 Native로 들어가는 게 낫다.

다음 8장에서는 시야를 옆으로 돌린다. *코드를 거의 안 바꾸고 80% 이상 시작을 줄일 수 있다면*? CRaC와 SnapStart의 시간 여행 이야기다. closed-world라는 결단 없이도 비슷한 이득을 얻는 길이 있다는 사실 — 이게 다음 챕터의 출발점이다. Native에서 후퇴한 한국의 많은 팀들이 *진짜로 가야 할 곳*은 어쩌면 거기일지도 모른다. 함께 살펴보자.
