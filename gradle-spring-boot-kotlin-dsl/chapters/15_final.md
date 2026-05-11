# 15장. GraalVM Native Image로 패키징한다

새벽 두 시, 가상 서버 한 대에 Spring Boot 앱 다섯 개를 띄워야 하는 상황을 가정해보자. 각 앱이 부팅에 4초씩 걸리고, 기동 직후 메모리를 600MB씩 잡아먹는다. 다섯 개면 3GB가 우습게 사라진다. 서버리스 환경이라면 더 난감하다. 사용자가 첫 요청을 보내고 4초를 기다리는 사이, "콜드 스타트"라는 말이 SLA 문서 위로 떠오른다. 그렇다면 어떻게 해야 할까?

GraalVM Native Image는 이 질문에 한 가지 답을 내민다. **JVM을 빼버리자.** Spring Boot 앱을 OS 위에서 직접 도는 단일 실행 파일로 컴파일해버린다. 부팅이 100ms 단위로 떨어지고, 메모리 사용량은 1/3 이하로 줄어든다. 보기에는 마법 같다. 그런데 마법에는 늘 값이 따라온다. 빌드가 5~20분 걸린다. 빌드 한 번에 RAM 4~8GB가 들어간다. 리플렉션을 잘못 쓰면 런타임에 비로소 깨진다. 디버깅이 까다로워진다. **그래서 이 장은 "어떻게 native로 만드는가"만큼이나 "언제 그 비용을 지불할 가치가 있는가"를 같은 비중으로 다루려 한다.**

Part V의 문이 여기서 열린다. Part IV까지 우리는 빌드를 도구로 키우는 길을 걸었다. Part V는 그 도구가 운영 환경의 무게를 떠받치는 시점이다. 운영의 첫 번째 무게는 패키징이다. 우리가 만든 앱을 어떤 모양으로 서버에 던질 것인가. 그 선택지 가운데 가장 극단적인 모양이 native binary다. 14장에서 native 빌드를 PR 흐름에서 따로 빼두자고 약속했었다. 그 약속의 안쪽으로 이제 들어가보자.

## 플러그인 하나가 일으키는 연쇄 반응

`ch15-native/build.gradle.kts`를 열고 한 줄을 추가한다고 해보자.

```kotlin
plugins {
    id("org.springframework.boot") version "4.0.6"
    id("io.spring.dependency-management") version "1.1.7"
    id("org.graalvm.buildtools.native") version "0.11.5"
    kotlin("jvm") version "2.2.20"
    kotlin("plugin.spring") version "2.2.20"
}
```

세 번째 줄, `org.graalvm.buildtools.native` 하나가 들어왔다. 그러면 빌드의 모양이 어떻게 바뀌는가? `./gradlew tasks --group "native"`를 한 번 두드려보자. `nativeCompile`, `nativeRun`, `nativeTest`가 새로 떴다. `./gradlew tasks --group "build"`를 보면 `processAot`, `processTestAot`도 같이 떠 있다. 우리가 적은 줄은 하나인데, 빌드 그래프에 새 식구가 다섯 가족 단위로 들어왔다. 무슨 일이 일어난 걸까?

GraalVM Native plugin이 적용되는 순간, **자기 혼자 들어오는 게 아니라 `org.springframework.boot.aot` 플러그인을 같이 끌고 들어온다.** 이 둘이 합쳐서 다음 변화를 만든다.

1. `aot`, `aotTest`라는 새로운 소스셋이 생긴다.
2. `processAot`, `processTestAot` task가 등록된다 — Spring의 AOT(Ahead-of-Time) 처리를 실행하는 task다.
3. `nativeCompile`이 일반 `compileJava` 출력이 아니라 `processAot`의 출력을 입력으로 받는다.
4. `bootJar`가 만드는 jar 안에 reachability metadata가 같이 들어가고, jar 매니페스트에 `Spring-Boot-Native-Processed: true`라는 줄이 한 줄 추가된다.

이 네 가지가 동시에 일어난다는 점을 기억해두자. 우리는 한 줄을 더했을 뿐인데, Spring Boot의 빌드 파이프라인 자체가 native를 향해 재배열됐다. **AOT 처리가 무엇이며 왜 필요한가**가 자연히 따라오는 질문이다.

JVM 위에서 Spring Boot가 부팅할 때는 클래스패스를 훑고, `@Configuration` 클래스들을 찾고, 컴포넌트 스캔을 돌리고, 빈을 만들고, AutoConfiguration 조건을 평가한다. 이 과정의 대부분이 **런타임에 일어난다**. 그런데 native binary는 런타임에 클래스를 새로 로드하지 않는다. 모든 클래스가 빌드 시점에 확정돼야 한다. 그러면 Spring의 그 풍성한 런타임 결정은 어디서 해야 하는가? 답은 하나뿐이다. **빌드 시점으로 옮긴다.** 이게 AOT 처리다. `processAot`이 Spring 컨테이너를 빌드 시점에 한 번 시뮬레이션해서, "이 앱은 결국 이 빈들을 이렇게 만들어 쓴다"라는 결과를 Java 코드와 메타데이터로 미리 적어둔다. 그 결과물이 `aot` 소스셋에 떨어지고, `nativeCompile`이 그걸 입력으로 받아 binary를 만든다.

그래서 GraalVM Native plugin은 단순히 "C로 컴파일하는 도구"가 아니다. **Spring AOT와 GraalVM, 두 도구가 직렬로 연결되도록 빌드 그래프를 다시 그리는 어댑터**다. 이 둘이 잘 짜여 있어서 우리는 플러그인 하나만 적으면 된다. 안에서 일어나는 일이 무엇인지 알고 보면, "처음 native 빌드가 왜 그렇게 한참 돌고 있는가"가 덜 답답해진다.

## `nativeCompile`을 한 번 돌려보자

`ch15-native/`에 작은 컨트롤러 하나를 두자.

```kotlin
@RestController
class HelloController {
    @GetMapping("/hello")
    fun hello(): Map<String, String> = mapOf("greeting" to "hi from native")
}
```

GraalVM이 설치돼 있다고 가정한다. 로컬에 없다면 SDKMAN으로 `sdk install java 21-graalce` 같은 식으로 받아두자. JDK 자체가 GraalVM 배포판이어야 한다. 일반 OpenJDK로는 `nativeCompile`이 돌지 않는다. 이게 첫 번째 진입 비용이다.

```bash
./gradlew nativeCompile
```

처음 누르면 한참 동안 콘솔이 조용하다. 1분쯤 지나면 `processAot`이 도는 로그가 보인다. Spring이 빌드 시점에 컨테이너를 시뮬레이션하며 `META-INF/native-image/...`에 reachability metadata를 떨어뜨린다. 그 다음이 진짜 무거운 단계다. GraalVM의 `native-image` 도구가 우리 코드, 우리가 끌어다 쓴 모든 의존성, JDK 클래스 일부까지 한 binary로 합쳐 정적으로 컴파일한다. 분석(Points-to analysis), 빌딩, 최적화, 이미지 작성. 단계마다 진행 막대가 천천히 차오른다. 이걸 처음 보는 개발자가 "내 컴퓨터가 망가졌나?"라고 생각하는 건 자연스러운 반응이다. 망가진 게 아니다. 그냥 native 빌드가 원래 이만큼 무겁다.

다 끝나면 `build/native/nativeCompile/`에 OS-native 실행 파일이 떨어진다. macOS면 Mach-O, Linux면 ELF다. 그걸 직접 실행해보자.

```bash
./build/native/nativeCompile/ch15-native
```

콘솔에 "Started Application in 0.083 seconds" 같은 줄이 뜨면 성공이다. 한자릿수 밀리초 단위로 떨어지는 부팅 시간을 처음 보면 살짝 놀랍다. JVM에서 같은 앱을 띄우면 보통 1.5~3초 걸리던 게, 여기서는 100ms 안에 끝난다. 메모리도 마찬가지다. `ps -o rss= -p $(pgrep ch15-native)`를 찍어보면 60~120MB 수준이다. JVM이었으면 같은 앱이 400~600MB는 잡는다. 이 숫자들이 native의 마케팅 문구다. 그리고 마케팅 뒤편에 우리가 방금 5~15분간 본 빌드 시간이 있다.

## 빌드 시간의 무게를 받아들이는 법

자, 빌드가 무거운 건 부정할 수 없는 사실이다. 그러면 우리가 일하는 흐름에는 이걸 어떻게 끼워 넣어야 하는가? 답은 단호하게 짚고 가자. **개발자 로컬에서는 JVM 빌드를 유지한다.** 코드 한 줄 바꿀 때마다 `nativeCompile`을 돌리면 일이 안 된다. `./gradlew bootRun`으로 JVM에서 띄우고, 단위 테스트는 `./gradlew test`로 JVM에서 돌리는 일상 흐름은 그대로 둔다. native 빌드는 **확인용이지 개발용이 아니다**.

그러면 native는 언제 도는가? 두 군데다. 첫째, CI의 별도 job. 둘째, release 파이프라인. 14장 끝에서 나눈 이야기와 정확히 같은 결론으로 다시 돌아온다.

> **함정 박스 — Native 빌드 시간을 어떻게 받아들이는가**
>
> Native 빌드의 시간·메모리 비용을 줄이는 묘약은 사실 없다. 줄이는 게 아니라 **언제 지불할지를 분리해 두는** 것이 운영 패턴이다.
>
> - **PR마다 돌리지 말자.** 14장의 `Native Build` 워크플로우처럼 schedule(예: 매일 18시 UTC)과 `workflow_dispatch`로만 트리거를 둔다. PR 흐름은 JVM 빌드와 통합 테스트로 빠르게 유지한다.
> - **`bootBuildImage`를 쓸 때 buildpack 레이어 캐시를 Volume으로 영속화하자.** 빌드 컨테이너가 매번 paketo builder의 GraalVM 캐시를 새로 받지 않도록 한다. 로컬이면 `~/.docker`/Colima의 데이터 볼륨, CI면 cache action 위에 docker volume을 묶는다. 이 캐시 한 번이 5분 정도를 흡수한다.
> - **메모리 OOM이 뜨면 `-J-Xmx8g`를 한 번 시도해보자.** native-image 도구가 자기 분석 단계에서 힙을 많이 쓴다. Gradle 쪽에 `tasks.named<BuildNativeImageTask>("nativeCompile") { jvmArgs("-J-Xmx8g") }` 식으로 넘기거나, `bootBuildImage`라면 `environment.put("BP_NATIVE_IMAGE_BUILD_ARGUMENTS", "-J-Xmx8g")`로 빌더에 전달한다. GitHub-hosted runner의 기본 7GB로는 큰 앱이 곧잘 터진다.
> - **runs-on을 키우는 것도 한 방법이다.** `ubuntu-latest-8-cores` 같은 large runner를 native job만 쓰도록 한다. PR 빌드는 보통 runner를 그대로 둔다 — 비용 차이가 거기서 갈린다.

이 패턴이 자리잡으면 매일 아침 main 브랜치에 native 빌드 결과 하나가 쌓인다. 한 달 동안 native가 한 번도 깨지지 않았다면 운영 후보로 올릴 수 있다. 깨지는 날이 있다면 그 commit이 무엇이었는지 매일 단위로 좁혀 들어갈 수 있다. **빠른 피드백은 PR 흐름이 책임지고, 깊은 검증은 nightly가 책임진다.** 이렇게 책임을 분리하면 native의 무게가 일상 일을 누르지 않는다.

## `bootBuildImage`가 native 이미지가 되는 순간

6장에서 우리는 `bootBuildImage`를 처음 만났다. Cloud Native Buildpacks가 Dockerfile 없이도 OCI 이미지를 만들어주는 task다. 그때 작은 박스로 "GraalVM Native plugin이 같이 적용돼 있으면 native 이미지로 자동 빌드된다"라고 한 줄 적어두고 지나갔다. 그 한 줄이 이 장에서 회수될 차례다.

15장의 build script는 이미 GraalVM Native plugin을 갖고 있다. 그 상태에서 `bootBuildImage`를 그냥 부르면 어떻게 되는가?

```bash
./gradlew bootBuildImage --imageName=ghcr.io/example/hello:native
```

빌더(paketo의 builder-noble-java-tiny)가 자기 안의 GraalVM buildpack을 자동으로 활성화한다. 컨테이너 안에서 우리가 방금 본 `processAot` → `native-image` 흐름이 그대로 일어난다. 결과는 OCI 이미지 한 장인데, 안에 든 게 jar가 아니라 native 실행 파일이다. **Dockerfile 없이도 native 이미지가 만들어진다.** Spring 팀이 native를 "쉽게" 만들기 위해 얹어둔 자동화 한 겹이 여기서 빛난다.

```kotlin
tasks.named<BootBuildImage>("bootBuildImage") {
    imageName = "ghcr.io/example/hello:${project.version}"
    environment.put("BP_NATIVE_IMAGE", "true")
    environment.put("BP_NATIVE_IMAGE_BUILD_ARGUMENTS", "-J-Xmx8g")
    publish = true
    docker {
        publishRegistry {
            username = providers.environmentVariable("GHCR_USER").get()
            password = providers.environmentVariable("GHCR_TOKEN").get()
        }
    }
}
```

`BP_NATIVE_IMAGE`는 사실 GraalVM plugin이 적용돼 있으면 자동으로 켜진다. 명시적으로 적어두는 건 의도를 드러내기 위해서다. 누가 이 build script를 처음 읽어도 "아, 이건 native 이미지를 만드는 task구나"가 한눈에 들어온다. **빌드 의도가 문서가 되도록 적는 습관**의 한 사례라고 봐도 좋다.

여기서 한 가지 짚자. `bootBuildImage`의 native 빌드는 도커 컨테이너 안에서 일어난다. 즉 **로컬에 GraalVM JDK가 없어도 된다.** `./gradlew nativeCompile`은 로컬 JDK가 GraalVM이어야 하지만, `bootBuildImage`는 빌더 이미지 안의 GraalVM을 쓴다. 도커만 깔려 있으면 어떤 JDK로도 native OCI 이미지를 뽑을 수 있다는 뜻이다. CI runner에 GraalVM을 따로 깔지 않아도 native 이미지를 만들 수 있는 길이 여기에 있다.

대신 도커 빌드의 메모리 한도에 신경 쓰자. Colima나 Docker Desktop의 기본 VM 메모리가 4GB로 잡혀 있다면, native 빌드가 그 안에서 OOM으로 죽는다. Docker Desktop의 Resources 탭에서 메모리를 8~12GB로 키워두는 게 안전하다. 메모리 압박은 native 빌드의 첫 번째 사고 원인이다.

## AOT만 단독으로 — native까지 가지 않더라도

native까지 안 가더라도 AOT 처리 자체가 주는 이득이 있다. 부팅이 빨라지고, 빈 정의가 미리 풀려 있으니 시작 시 JIT 워밍업 시간이 짧아진다. JVM에서 그대로 도는 일반 jar인데도 부팅이 빨라진다는 뜻이다. CDS(Class Data Sharing)와 조합하면 효과가 더 커진다. 그렇다면 native 빌드의 무거운 비용은 지불하지 않고 AOT의 이득만 가져갈 수 없을까? 가능하다.

```kotlin
plugins {
    id("org.springframework.boot") version "4.0.6"
    id("io.spring.dependency-management") version "1.1.7"
    kotlin("jvm") version "2.2.20"
    kotlin("plugin.spring") version "2.2.20"
}

apply(plugin = "org.springframework.boot.aot")
```

GraalVM Native plugin은 빼고, AOT 플러그인만 `apply`로 따로 적용한다. 그러면 `processAot`이 빌드 그래프에 들어오지만 `nativeCompile`은 들어오지 않는다. `bootJar`에 AOT 산출물이 포함된다. 운영에서는 `java -Dspring.aot.enabled=true -jar app.jar` 식으로 띄우면 AOT 결과를 쓴다. 부팅 시간이 보통 30~50% 줄어든다.

**그래서 결정의 사다리는 이런 식으로 그릴 수 있다.** 운영 부팅이 느려서 SLA가 흔들린다면 우선 AOT만 켜보자. 그래도 부족하다면, 그리고 메모리 절감이나 콜드 스타트 100ms가 정말 필요한 워크로드라면 native까지 간다. **거꾸로 가지 말자.** "native가 멋있어 보여서 일단 한다"는 결정은 빌드 비용·디버깅 비용·운영 모니터링 비용으로 청구서가 돌아온다. 매번 답이 native일 필요는 없다.

## 런타임에 비로소 깨지는 클래스

Native 빌드를 처음 운영에 올린 팀이 가장 자주 겪는 사고가 있다. **빌드는 잘 끝났는데, 정작 native 앱을 띄우면 런타임에 `ClassNotFoundException`, `NoSuchMethodException`, `NullPointerException`이 어딘가에서 튀어나오는 일이다.** JVM에서는 잘 돌던 코드가 native에서만 깨진다. 왜 그럴까?

Native binary에는 우리가 "쓸 거라고 native-image 도구가 판단한 클래스"만 들어간다. 정적 분석으로 도달 가능(reachable)하다고 본 코드만 묶는다는 뜻이다. 그런데 자바·코틀린 코드는 곳곳에 정적으로 보이지 않는 호출이 있다. `Class.forName("com.example.MyHandler")` 같은 리플렉션, `getResourceAsStream("config/data.json")` 같은 리소스 로딩, JDK Proxy로 만드는 동적 프록시 — 이런 호출은 native-image 도구가 "어떤 클래스가 결국 필요한지"를 정적으로 알 수 없다. 빌드가 끝나면 그 클래스들은 binary에 안 들어가 있다. 운영에서 그 코드가 도는 순간 비로소 "그런 클래스 없는데?"라는 예외가 튀어나온다. **JVM이라면 ClassLoader가 그때그때 찾아주던 게, native에는 ClassLoader가 없다.**

Spring 자체의 코드는 Spring AOT 처리가 이 hint들을 거의 다 자동으로 만들어준다. `@Configuration`, `@RestController`, `RestTemplate` 등이 안에서 어떤 리플렉션을 쓰는지 Spring 팀이 다 알고 있어서, Spring 코드의 reachability metadata는 GraalVM reachability metadata 저장소 또는 Spring 자체의 hint 코드가 채워둔다. 우리가 그걸 의식할 일이 별로 없다는 게 native가 사용 가능한 수준까지 올라온 이유다.

문제는 **우리 코드 중에 리플렉션을 쓰는 부분**, 그리고 **third-party 라이브러리 가운데 아직 hint가 정비되지 않은 것**이다. Jackson으로 직렬화하는 우리 데이터 클래스, JPA로 매핑하는 엔티티 클래스, 우리가 직접 짠 `Class.forName` 한 줄 — 이런 것들이 사고의 진원지가 된다.

> **함정 박스 — `RuntimeHintsAgent`로 hint를 채우자**
>
> Spring Framework는 `org.springframework:spring-core-test` 모듈 안에 **RuntimeHintsAgent**라는 Java agent를 함께 배포한다. JVM 위에서 우리 앱이나 통합 테스트를 한 번 실제로 굴리는 동안, 어떤 리플렉션·리소스·프록시 접근이 일어났는지 메서드 호출 단위로 기록해서 우리가 빠뜨린 hint를 보여준다. ([Spring Framework Reference — Core/AOT/Hints](https://docs.spring.io/spring-framework/reference/core/aot.html))
>
> 적용은 우리가 직접 `-javaagent`로 붙여 준다. Spring Boot가 따로 Gradle plugin을 한 줄짜리로 노출하지 않으니, 이 절차는 일종의 의식이 된다.
>
> ```kotlin
> // app/build.gradle.kts
> val runtimeHintsAgent: Configuration by configurations.creating
>
> dependencies {
>     runtimeHintsAgent("org.springframework:spring-core-test")
> }
>
> testing {
>     suites {
>         val integrationTest by getting(JvmTestSuite::class) {
>             targets.all {
>                 testTask.configure {
>                     jvmArgs("-javaagent:${runtimeHintsAgent.asPath}")
>                 }
>             }
>         }
>     }
> }
> ```
>
> 통합 테스트에 `@EnabledIfRuntimeHintsAgent`를 단 클래스들은 agent가 붙어 있을 때만 실행되고, agent가 모은 trace를 검증한다. agent가 본 호출들을 그대로 `RuntimeHints`로 옮겨서 우리 hint 코드에 누락된 호출이 있는지 비교하는 패턴이 가장 흔하다.
>
> 핵심은 **"운영에서 실제로 도는 코드 경로"를 hint 수집에 포함시키는 것**이다. 단위 테스트만 돌고 끝나면 운영 경로의 리플렉션이 빠진다. 통합 테스트가 controller부터 repository까지 한 바퀴 도는 시나리오를 갖고 있다면, 그 위에 agent를 한 번 얹는 것만으로도 hint 누락의 대부분이 메워진다. 7장의 JVM Test Suite로 분리해 둔 `integrationTest`가 여기서 두 번째 일을 한다.

만약 agent를 돌렸는데도 운영에서 사고가 나면? Native binary에 디버그 심볼을 같이 넣어 두자. `tasks.named<BuildNativeImageTask>("nativeCompile") { debug.set(true) }`로 켜면 stack trace가 의미 있는 모양으로 나온다. 그리고 운영 인프라에 `gdb`로 native 프로세스에 붙어 들여다볼 수 있는 채널을 미리 준비해 두자. JVM의 `jstack`, `jmap` 같은 도구는 native에서 안 통한다. **native 운영은 디버깅 도구 자체가 새로 짜인다.** 이 점이 native 도입 결정에서 가장 자주 과소평가되는 비용이다.

## 그래서 언제 native를 쓰는가

장 초반의 질문으로 돌아가자. 언제 그 비용을 지불할 가치가 있는가? 운영 현장의 패턴을 보면 답이 두세 묶음으로 정리된다.

**첫째, 서버리스와 콜드 스타트가 매출에 직결되는 환경.** AWS Lambda, Google Cloud Run 같은 데서 Spring Boot를 띄울 때, JVM의 1.5~3초 부팅이 사용자 첫 응답 시간으로 직접 노출되는 경우. 여기서는 native의 100ms 부팅이 그냥 좋은 정도가 아니라 매출의 일부다. 빌드 비용은 release 파이프라인 안에서 흡수된다.

**둘째, 같은 노드에 작은 앱을 여러 개 띄워야 하는 환경.** Kubernetes 위에서 마이크로서비스 50개를 한 클러스터에 올린다고 해보자. JVM 50개가 각자 400MB씩 잡으면 노드가 빨리 닳는다. native binary 50개라면 노드의 메모리 풋프린트가 절반 이하로 떨어진다. 회사 인프라 비용이 줄어드는 종류의 의사결정이다.

**셋째, 작은 CLI 도구.** Spring 기반 admin CLI, 운영 스크립트 등 부팅과 종료가 자주 일어나는 짧은 프로세스. JVM 워밍업 비용이 작업 본체보다 큰 케이스다.

거꾸로, native를 굳이 안 가도 되는 경우가 많다. 오랫동안 떠 있는 monolith라면 부팅 시간은 한 번의 비용이다. JIT가 데우는 동안의 워밍업도 어차피 한 번이다. 메모리 절감은 절약 폭이 작고, 디버깅 도구가 줄어드는 비용은 항상 크다. **이런 워크로드에는 AOT만 켜고 native까지는 안 가는 게 균형 잡힌 선택이다.**

회사가 native를 도입한다고 하면, 한 가지 더 권하고 싶은 게 있다. **운영 모니터링에 부팅 시간과 RSS를 metric으로 박아두자.** native가 약속한 이득이 실제로 들어오는지 숫자로 확인할 수 있어야 한다. JVM 시절의 prometheus 메트릭 수집은 native에서도 그대로 된다(Micrometer가 native에서 동작한다). 부팅 시간 metric은 application이 띄워질 때 한 번 적어두자. 한 달 뒤에 그 그래프가 한 자릿수 밀리초 영역에 머물러 있으면 도입이 잘된 것이다. 1초대로 슬며시 올라가 있다면 어떤 startup 처리가 잘못 들어간 신호다. **숫자로 검증하지 못하는 도입은 도입이 아니다.**

## 마무리

15장에서 우리는 GraalVM Native Image의 안쪽을 들여다봤다. 플러그인 한 줄이 Spring AOT 플러그인을 같이 끌어와 빌드 그래프를 재배열한다는 것을 봤다. `processAot` → `native-image` 흐름으로 native binary가 나오고, 그게 100ms 부팅과 1/3 메모리라는 결과로 떨어지는 길을 따라가봤다. `bootBuildImage`가 같은 build script로 native OCI 이미지를 자동으로 만들어주는 자리도 확인했다. AOT만 단독으로 적용해서 native까지는 안 가는 중간 선택지도 손에 넣었다.

그리고 그 위에 비용을 두고 왔다. 5~20분의 빌드 시간, 4~8GB의 메모리, 런타임에 비로소 깨지는 reflection hint, 줄어든 디버깅 도구. 이 비용을 PR 흐름 바깥으로 분리해 nightly와 release만 책임지게 두는 운영 패턴을 잡았다. native가 어울리는 워크로드와 그렇지 않은 워크로드를 두 묶음으로 나눠 봤다. **Native는 "더 나은 패키징"이 아니라 "조건이 맞을 때 쓰는 도구"임을 기억해두자.**

Part V의 첫 장이 끝났다. 운영의 첫 번째 무게가 패키징이었다면, 두 번째 무게는 **신뢰**다. 우리 빌드 산출물의 안에는 직접 적은 코드보다 훨씬 더 많은 transitive 의존성이 들어 있다. 그 의존성들을 우리는 어디서 받았고, 누가 서명했으며, 다음 빌드에 같은 것이 들어온다는 보장이 어디 있는가? 16장에서 Dependency Verification, Dependency Locking, Repository Content Filtering을 한 자리에 놓고, **공급망 보안**의 모양을 그려보자.
