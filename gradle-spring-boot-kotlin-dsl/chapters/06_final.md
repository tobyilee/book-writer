# 6장. Spring Boot Gradle 플러그인의 내부 — bootJar, bootRun, bootBuildImage

`plugins { id("org.springframework.boot") version "4.0.6" }` 한 줄을 친다. Sync가 끝나면 IntelliJ의 Gradle 패널에 `bootJar`, `bootRun`, `bootBuildImage`, `bootTestRun` 같은 task가 줄줄이 새로 떠 있다. 동시에 dependencies 항목에는 `productionRuntimeClasspath`, `developmentOnly`, `testAndDevelopmentOnly`라는 낯선 configuration도 보인다. **이 한 줄이 도대체 무엇을 한 건가.**

`./gradlew bootJar`로 만들어진 jar를 unzip으로 열어보면 더 이상하다. `BOOT-INF/`라는 처음 보는 디렉터리, `layers.idx`라는 텍스트 파일, `org/springframework/boot/loader/`에는 우리가 의존성으로 추가한 적 없는 클래스들이 들어 있다. MANIFEST.MF의 `Main-Class`는 우리가 만든 `ShopApplication`이 아니라 `org.springframework.boot.loader.launch.JarLauncher`로 적혀 있다.

이 모든 게 어떻게 거기에 가 있는가? 그리고 회사 빌드를 Spring Boot 3.x에서 4.0으로 올리려고 plugin 버전 숫자만 바꿨는데 빌드가 깨졌다면, 정확히 어디서 무엇이 바뀐 건가? 6장에서 이 두 질문에 답하자.

미리 한 가지 자리를 분리해두자. **Gradle 9.x 자체로 옮기는 마이그레이션은 17장에서 다룬다.** Daemon JDK가 17+로 강제되는 일, `jcenter()` 제거, Configuration Cache가 preferred mode가 되는 일 같은 Gradle 본체의 변화는 거기 자리다. 6장은 **Spring Boot 플러그인 자체가 3.x → 4.0으로 올라오면서 무엇이 깨지는가**에 집중한다. 둘은 자주 겹쳐서 일어나지만 원인이 다른 변화다.

## 플러그인 한 줄이 일으키는 일

`org.springframework.boot` 플러그인 적용은 그 자체로는 거의 아무 일도 하지 않는다. 정확히는 **다른 플러그인이 적용되기를 기다리는 reaction을 등록**한다. `java` 플러그인이 적용되는 순간(또는 `java-library`, `org.jetbrains.kotlin.jvm`처럼 java를 transitive로 끌어오는 플러그인) 그 reaction이 발화하면서 비로소 task와 configuration이 생긴다.

이 순서를 정확히 짚어두는 게 중요하다. 5장에서 우리는 build.gradle.kts에 이렇게 적었다.

```kotlin
// ch04-bootapp/build.gradle.kts
plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.kotlin.spring)
    alias(libs.plugins.spring.boot)
}
```

`kotlin.jvm`이 `java-base` + `java` 플러그인을 transitive로 적용한다. 그 적용을 본 Spring Boot 플러그인의 reaction이 발화한다. 그 결과로 자동 생성되는 것들이 이렇다.

**Task:**
- `bootJar` — 실행 가능한 fat jar를 만든다 (`BootJar` 타입)
- `bootRun` — 앱을 JVM 모드로 실행한다 (`BootRun` 타입, `JavaExec` 상속)
- `bootBuildImage` — OCI 이미지를 만든다 (`BootBuildImage` 타입)
- `bootTestRun` — test classpath로 앱을 실행한다 (`BootRun` 타입)

**Configuration:**
- `bootArchives` — `bootJar`가 만든 산출물이 들어가는 publication용 configuration
- `developmentOnly` — devtools처럼 dev에서만 쓰는 의존성 자리
- `testAndDevelopmentOnly` — 테스트와 dev 양쪽에서 쓰는 의존성 자리
- `productionRuntimeClasspath` — **runtimeClasspath에서 `developmentOnly`, `testAndDevelopmentOnly`를 뺀 결과**. fat jar가 실제로 포함할 의존성 목록이다.

**Compile 설정 변경:**
- 소스 인코딩 UTF-8 강제
- Java 컴파일에 `-parameters` 자동 추가 (Spring의 파라미터 이름 기반 바인딩이 reflective하게 동작하도록)

5장에서 우리가 박스에서만 본 `productionRuntimeClasspath`가 여기서 본격적으로 등장한다. `developmentOnly(libs.spring.boot.devtools)`로 추가한 devtools가 왜 fat jar에 포함되지 않는가? 그건 `bootJar`가 의존성 묶음을 가져올 때 `runtimeClasspath`가 아니라 **`productionRuntimeClasspath`**를 본다는 약속 때문이다. devtools는 `developmentOnly`에 있고, productionRuntimeClasspath는 그걸 뺀 집합이고, fat jar는 productionRuntimeClasspath만 본다. 이 사슬이 그대로 박혀 있다.

기억해두자. **`developmentOnly`에 넣은 의존성은 IDE의 `bootRun` 실행 시에는 classpath에 있고, `bootJar` 산출물에는 없다.** 이건 의도된 동작이다. devtools가 production 컨테이너에 같이 실려서 자동 reload가 시도되는 사고를 막는다.

## bootJar의 내부 — fat jar는 어떻게 생겼는가

이제 `./gradlew bootJar`로 만든 산출물을 직접 들여다보자. `ch04-bootapp/build/libs/`에 가보면 jar가 두 개 떠 있다.

```
build/libs/
├── ch04-bootapp-0.0.1-SNAPSHOT.jar         # bootJar의 산출물 — 실행 가능 fat jar
└── ch04-bootapp-0.0.1-SNAPSHOT-plain.jar   # jar의 산출물 — 일반 library jar
```

여기가 처음 만나는 사람에겐 좀 헷갈리는 자리다. `assemble`을 부르면 두 개가 다 나온다. **`bootJar` task가 `jar` task를 대체하는 게 아니라, 둘이 공존한다**는 게 핵심이다. 다만 `bootJar`의 산출물에는 classifier가 비어 있고, 일반 `jar`의 산출물에 `-plain`이라는 classifier가 붙는다. 왜 굳이 둘 다 만드는가? `bootJar`로 만든 fat jar는 fat jar로서는 훌륭하지만 **다른 모듈에서 `dependencies { implementation(project(":app")) }`로 끌어쓰는 일에는 부적합**하다. 그래서 일반 jar도 살려둔다. 이 사정은 9장의 library 모듈 함정에서 본격적으로 본다.

`bootJar` 산출물의 내부를 풀어보자.

```bash
unzip -l build/libs/ch04-bootapp-0.0.1-SNAPSHOT.jar
```

```
ch04-bootapp-0.0.1-SNAPSHOT.jar
├── META-INF/
│   └── MANIFEST.MF                       # Start-Class=ShopApplication, Main-Class=JarLauncher
├── BOOT-INF/
│   ├── classes/                          # 우리 앱의 클래스/리소스
│   │   └── com/example/shop/...
│   ├── lib/                              # 의존성 jar들 그대로
│   │   ├── spring-boot-3.5.x.jar
│   │   ├── spring-context-...jar
│   │   └── ...
│   └── classpath.idx                     # 의존성 jar의 정렬된 인덱스
├── BOOT-INF/layers.idx                   # 레이어 인덱스 (기본 ON)
└── org/springframework/boot/loader/      # spring-boot-loader 클래스
    └── launch/JarLauncher.class
```

각 자리가 무엇인지 천천히 짚어보자.

**`META-INF/MANIFEST.MF`** — 평소 만나던 일반 jar와 다른 점이 두 가지다. `Main-Class`가 우리 앱의 메인 클래스가 아니라 `org.springframework.boot.loader.launch.JarLauncher`로 적혀 있다. 그리고 `Start-Class`라는 비표준 attribute에 우리 앱의 메인 클래스(`com.example.shop.ShopApplication`)가 적혀 있다. `java -jar`은 표준대로 `Main-Class`를 부르고, 그게 `JarLauncher`다. `JarLauncher`가 jar 안의 `BOOT-INF/lib/`에 있는 의존성들을 자신의 ClassLoader에 추가한 뒤 `Start-Class`로 위임한다. **이게 fat jar가 표준 `java -jar`로 실행되는 비결이다.** jar-in-jar를 직접 풀지 않고도, ClassLoader 레벨에서 nested jar를 그대로 읽는다.

**`BOOT-INF/classes/`** — 우리 앱의 컴파일된 `.class` 파일과 `src/main/resources/`의 리소스가 그대로 들어간다. 평소의 jar 루트에 들어가던 게 한 단계 들어간 자리에 들어간 것뿐이다.

**`BOOT-INF/lib/`** — `productionRuntimeClasspath`로 풀린 의존성 jar들이 **풀리지 않은 채로** 그대로 들어간다. Maven의 shade plugin이나 Gradle의 `Jar` task로 만든 "uber jar"와 결정적으로 다른 자리다. uber jar는 의존성을 풀어서 한 디렉터리에 섞어버리지만, Spring Boot의 fat jar는 의존성 jar를 jar 안에 통째로 보관한다. 그 결과 **클래스 시그니처 충돌이나 META-INF 충돌이 안 일어난다.** 두 의존성에 같은 경로의 리소스가 있어도, 각각 자기 jar 안에 사는 채로 격리되기 때문이다.

**`BOOT-INF/classpath.idx`** — `lib/` 아래 jar들의 적용 순서를 명시한 텍스트 파일. ClassLoader가 의존성 jar를 탐색할 순서를 빌드 시점에 미리 결정해서 적어둔다.

**`BOOT-INF/layers.idx`** — 4.0에서도 기본 ON인 레이어 인덱스다. 다음 절에서 본격적으로 들여다본다.

**`org/springframework/boot/loader/`** — `spring-boot-loader` 모듈의 클래스가 fat jar 루트에 unpack된 상태로 박혀 있다. 우리가 `dependencies`에 추가한 적 없는데도 들어 있는 이유는, `JarLauncher` 자체가 `BOOT-INF/lib/` 안에 있으면 부트스트랩이 불가능하기 때문이다. 표준 `java -jar`이 처음 부르는 클래스는 jar 루트의 표준 위치에 있어야 한다. 그래서 이 클래스들만은 풀려서 jar 루트에 박힌다.

## 메인 클래스 자동 탐지와 명시

`bootJar`가 MANIFEST.MF의 `Start-Class`에 무엇을 적을지는 어떻게 결정되는가? 기본 동작은 **자동 탐지**다. main 소스셋의 모든 클래스를 훑어 `public static void main(String[])` 시그니처를 가진 클래스를 찾는다. 후보가 정확히 하나면 그걸 쓴다. 두 개 이상이면 빌드가 명확한 에러로 멈춘다.

자동 탐지는 편하지만 한 가지 위험을 동반한다. **메인 후보가 여럿일 때 자동 탐지가 다른 후보를 골라버리는 사고**다. 회사 빌드에서 `main()`을 가진 유틸리티 클래스 하나가 어쩌다 추가되면 빌드가 갑자기 그쪽을 골라 산출물이 엉뚱한 클래스를 부팅한다. 이 위험을 피하려면 명시하는 편이 낫다.

```kotlin
import org.springframework.boot.gradle.tasks.bundling.BootJar

tasks.named<BootJar>("bootJar") {
    mainClass = "com.example.shop.ShopApplication"
}
```

`bootJar`와 `bootRun` 양쪽이 보는 `mainClass`는 사실 `springBoot` extension에 한 번만 명시하면 두 task가 함께 본다.

```kotlin
springBoot {
    mainClass = "com.example.shop.ShopApplication"
}
```

production 빌드는 이 쪽을 권한다. 자동 탐지는 신규 프로토타입 단계에서는 충분히 편리하지만, 회사 코드베이스에 정착할 무렵엔 명시로 옮겨두는 편이 사고를 줄인다.

## 레이어드 JAR — OCI 이미지 캐시의 토대

`BOOT-INF/layers.idx`를 풀어서 열어보면 이런 내용이다.

```
- "dependencies":
  - "BOOT-INF/lib/spring-boot-3.5.x.jar"
  - "BOOT-INF/lib/spring-context-...jar"
  ...
- "spring-boot-loader":
  - "org/"
- "snapshot-dependencies":
- "application":
  - "BOOT-INF/classes/"
  - "BOOT-INF/classpath.idx"
  - "BOOT-INF/layers.idx"
  - "META-INF/"
```

이 파일이 무엇을 하는가? 단독으로는 거의 아무 것도 안 한다. **OCI 이미지를 만들 때 도커 레이어가 fat jar의 어떤 부분으로 갈라져야 하는지를 미리 적어둔 색인**일 뿐이다. 핵심은 그 분리의 의도다.

- `dependencies` — 우리가 잘 안 바꾸는, BOM이 정한 외부 라이브러리들. 가장 안 변한다.
- `spring-boot-loader` — Spring Boot 자체. plugin 버전이 안 바뀌면 안 변한다.
- `snapshot-dependencies` — `-SNAPSHOT` 의존성 자리. 사내 라이브러리 등이 여기 모인다.
- `application` — 우리 앱 코드. **가장 자주 변한다.**

위에서 아래로 갈수록 변화 빈도가 높다. OCI 이미지의 각 레이어는 hash로 식별되고, 변하지 않은 레이어는 다음 빌드의 cache hit으로 그대로 재사용된다. 코드 한 줄만 고친 빌드의 결과로 만들어지는 이미지에서 95% 이상의 바이트는 캐시에서 재사용되고, 새로 push해야 하는 건 application 레이어 몇 메가뿐이라는 시나리오가 여기서 나온다. **`layers.idx`는 이 캐시 성능의 토대 데이터다.**

기본값으로 충분한 경우가 많아서 다음과 같이 명시적으로 한 번만 박아두면 된다.

```kotlin
tasks.named<BootJar>("bootJar") {
    layered {
        enabled = true
    }
}
```

레이어 정의 자체를 회사 정책에 맞춰 더 세분하고 싶다면 `layered.layerConfiguration`을 다듬는 길이 있지만, 그 자리는 9장 이후의 멀티 모듈 빌드에서 다시 본다. 단일 모듈에서는 기본값 그대로가 안전하다.

## bootRun — JavaExec 그 자체

`bootRun`은 의외로 단순한 task다. `org.springframework.boot.gradle.tasks.run.BootRun`은 **`JavaExec`을 상속**한다. 그 말은 `JavaExec`에 있는 모든 옵션이 그대로 통한다는 뜻이다.

```kotlin
import org.springframework.boot.gradle.tasks.run.BootRun

tasks.named<BootRun>("bootRun") {
    jvmArgs("-Dspring.profiles.active=local")
    systemProperty("debug", "true")
    sourceResources(sourceSets["main"])  // src/main/resources를 그대로 본다 → 라이브 리로드
}
```

`sourceResources(sourceSets["main"])` 한 줄이 익숙해질 만한 자리다. 기본 동작은 `bootRun`이 `build/resources/main/`(컴파일 결과 폴더)를 본다. 그래서 정적 리소스(예: `templates/*.html`)를 고쳐도 즉시 반영되지 않고 다시 빌드돼야 한다. `sourceResources()`로 `src/main/resources/`를 직접 가리키게 하면 파일 수정이 IDE에서 즉시 보인다. devtools 없이도 정적 리소스에 한해 라이브 reload가 동작하는 비결이다.

런타임 인자를 넘기는 것도 깔끔하다.

```bash
./gradlew bootRun --args='--spring.profiles.active=dev --server.port=9090'
```

`--args`는 Spring Boot의 `SpringApplication.run(args)`이 받는 그 `args`다. JVM 옵션이 아니라 **앱 자체의 인자**다. 이 둘을 헷갈리지 말자. JVM 옵션은 `-D...`로 시작하고 `jvmArgs`로 설정하거나 `bootRun.jvmArguments` property에 넣는다. 앱 인자는 `--server.port=9090`처럼 Spring 컨벤션을 따르고 `--args`로 넘긴다.

`bootTestRun`도 함께 챙겨두자. 이건 `bootRun`과 거의 똑같지만 classpath가 다르다. **test sourceSet의 classpath로 앱을 실행한다.** 통합 테스트용 설정(예: testcontainers, 인메모리 설정)을 main 코드에 흘리지 않고 별도 fixture로 두면서, 그 fixture 그대로 부팅한 앱을 손으로 확인하고 싶을 때 쓴다. 7장에서 JVM Test Suite로 들어가면 이 task의 자리가 더 또렷해진다.

## bootBuildImage — Dockerfile 없는 OCI 이미지

`bootBuildImage`는 6장에서 가장 마법처럼 보이는 자리다. **Dockerfile을 한 줄도 안 쓰고**, 로컬 Docker daemon에 OCI 이미지가 한 방에 박힌다.

```bash
./gradlew bootBuildImage
```

이 한 줄 안쪽에서 무슨 일이 일어나는가?

`bootBuildImage`는 **Paketo Buildpacks**를 호출한다. Paketo는 Cloud Native Buildpacks (CNB) 사양을 따르는 빌드팩 모음이다. 핵심 idea는 이렇다 — 우리 앱의 산출물(jar)과 메타데이터를 보면 어떤 builder image를 깔고 어떤 launcher를 박을지가 결정된다. 그 결정을 도구가 한다. 우리는 산출물만 제공하고 builder 이미지가 알아서 운영체제 layer, JRE layer, 의존성 layer, 앱 코드 layer를 쌓아 최종 이미지를 만든다.

기본 builder는 Spring Boot 4.0 기준 **`paketobuildpacks/builder-noble-java-tiny:latest`**다. Ubuntu Noble Numbat 기반의 최소 이미지에 buildpack 도구만 박힌 빌더다. (Spring Boot 3.x에서는 기본 builder가 `paketobuildpacks/builder-jammy-tiny` 또는 `builder-jammy-base`였다. 회사 빌드를 4.0으로 올리면서 이미지가 갑자기 커지거나 작아진 걸 보게 된다면, 이 기본값 변화가 원인일 가능성이 높다.)

설정은 이렇게 한다.

```kotlin
import org.springframework.boot.gradle.tasks.bundling.BootBuildImage

tasks.named<BootBuildImage>("bootBuildImage") {
    imageName = "ghcr.io/example/shop:${project.version}"
    environment.put("BP_JVM_VERSION", "21")
    publish = true
    docker {
        publishRegistry {
            username = providers.environmentVariable("GHCR_USER").get()
            password = providers.environmentVariable("GHCR_TOKEN").get()
        }
    }
}
```

`imageName`은 결과 이미지의 태그다. `${project.version}`이 그대로 박힌다. `environment`는 buildpack이 보는 환경변수다. `BP_JVM_VERSION=21`은 Paketo Java buildpack에게 JRE 21을 깔라고 알려준다.

`publish = true`로 두면 빌드가 끝나자마자 레지스트리로 push까지 진행된다. **로컬에 이미지를 만들고 별도로 `docker push`를 부르는 단계가 없다.** 이게 CI 파이프라인에서 가장 빛난다. `./gradlew bootBuildImage` 한 줄이 ghcr.io에 이미지를 올린 결과까지를 만들어낸다. 자격증명을 `providers.environmentVariable(...)`로 받는 패턴도 짚어두자. 직접 `System.getenv("...")`로 받으면 Configuration Cache에서 위반이 잡힌다. Provider API로 받는 게 안전한 길이다. 13장에서 본격적으로 본다.

이미지의 캐시 동작이 인상적이다. 코드 한 줄만 바꾸고 다시 `./gradlew bootBuildImage`를 부르면 빌드 시간이 첫 빌드의 1/10 이하다. buildpack이 layered jar의 레이어 구분을 OCI 레이어로 그대로 매핑하기 때문이다. application 레이어만 갈리고 나머지는 다 캐시에서 재사용된다. 앞 절에서 본 `layers.idx`의 의도가 여기서 결실을 본다.

GraalVM Native Image 플러그인을 함께 적용하면 `bootBuildImage`가 **자동으로 native 이미지를 빌드**한다. JVM 이미지 대신 그 자리에 native binary가 박힌 이미지가 만들어진다. 자세한 자리는 15장이다.

## bootJar와 jar의 공존 — 어느 쪽을 발행하는가

다시 `build/libs/`로 돌아가자. jar가 두 개다. `bootJar`의 산출물(classifier 비어 있음)과 `jar`의 산출물(classifier=`plain`). `assemble`은 둘 다 만든다.

이게 의도된 모양인가? 그렇다. 두 산출물의 쓰임새가 다르다. **`bootJar`의 fat jar는 실행용, `jar`의 일반 library jar는 다른 모듈에서 import해서 쓰는 용도다.** 같은 모듈을 동시에 둘 다로 쓰는 일은 단일 모듈에서는 흔하지 않다. 하지만 이 약속이 박혀 있어야 9장의 멀티 모듈에서 library 모듈의 사고를 깔끔하게 풀 수 있다.

회사 빌드에 따라 `-plain.jar`이 거추장스럽게 느껴진다면, 명시적으로 끌 수 있다.

```kotlin
tasks.named<Jar>("jar") {
    enabled = false
}
```

단일 모듈 앱이고 jar publication을 따로 안 한다면 이 한 줄로 깔끔해진다. 다만 library 모듈로 누군가 import할 일이 있다면 **반드시 살려두자.** 끄는 쪽은 명시적 선택이어야 한다.

## Spring Boot 3.x → 4.x — 무엇이 깨지는가

이제 6장의 또 다른 약속을 풀 차례다. 회사 빌드가 Spring Boot 3.5.x에서 잘 굴러가고 있다고 해보자. 어느 날 4.0.6으로 plugin 버전 숫자만 바꿔보자.

```kotlin
plugins {
    id("org.springframework.boot") version "4.0.6"  // 3.5.6 → 4.0.6
}
```

높은 확률로 빌드가 한두 곳에서 멈춘다. 어디서 무엇이 깨지는가를 미리 알아두면 1시간이 5분으로 줄어든다.

### Gradle 8.14+ 또는 9.x 요구

Spring Boot 4.0은 **Gradle 8.14+ 또는 9.x**를 요구한다. 3.x는 Gradle 7.x도 받아줬지만 4.x는 그 자리를 닫았다. 회사 빌드의 `gradle/wrapper/gradle-wrapper.properties`가 7.6.4면 4.0 plugin은 적용 단계에서 명확한 에러를 던지며 멈춘다.

```bash
./gradlew wrapper --gradle-version 9.5 --distribution-type=bin
```

`--distribution-type=bin`을 빠뜨리지 말자. 기본값인 `all`은 200MB 넘는 소스 포함 배포본이라 CI를 무겁게 만든다. 이 명령을 두 번 부르고(wrapper task 자체가 wrapper 파일 자체를 새로 쓰기 위해 두 번 실행이 권장된다) 커밋하면 끝이다. **Gradle 본체로의 마이그레이션 자체는 17장에서 본격적으로 본다.** 여기서는 Spring Boot 4.0이 그걸 요구한다는 사실만 박아두자.

### Task 시그니처 — lazy property `=` 권장 강화

3.x 시절 우리는 이런 코드를 종종 봤다.

```kotlin
// 3.x 시절 흔한 모양 — 4.x에서도 동작은 하지만 권장 모양은 아님
tasks.named<BootJar>("bootJar") {
    mainClass.set("com.example.shop.ShopApplication")
    archiveClassifier.set("boot")
}
```

`Property<T>`에 `.set(value)`로 값을 넣는 모양이다. 4.x에서는 이 모양이 비권장은 아니지만, Kotlin DSL의 `=` 연산자 오버로딩이 lazy property에도 충분히 잘 동작하게 정리되면서 다음 쪽이 표준이 됐다.

```kotlin
// 4.x 권장 — = 연산자가 lazy property에 자연스럽게 동작
tasks.named<BootJar>("bootJar") {
    mainClass = "com.example.shop.ShopApplication"
    archiveClassifier = "boot"
}
```

`.set()`을 부르던 코드가 동작을 멈추지는 않는다. 다만 **새로 쓰는 코드는 `=`로 쓰는 편이 낫다.** 3장에서 본 Kotlin DSL의 `=`와 lazy property의 사이가 4.x에 와서 한 번 더 정돈됐다. 회사 빌드에서 옛 코드를 발견하면 같은 PR에서 정리하는 쪽이 깔끔하다.

### `bootBuildImage` 기본 builder 변화

앞 절에서 짚었듯 기본 builder가 `paketobuildpacks/builder-jammy-tiny`(또는 `jammy-base`)에서 **`paketobuildpacks/builder-noble-java-tiny:latest`**로 바뀌었다. Ubuntu Jammy(22.04)에서 Noble(24.04)로 베이스가 한 발 올라간 셈이다.

회사가 보안 이유로 builder image를 고정하고 있다면 명시적으로 적어두자.

```kotlin
tasks.named<BootBuildImage>("bootBuildImage") {
    builder = "paketobuildpacks/builder-jammy-tiny:0.0.146"
}
```

기본값에 의존하면 plugin 업그레이드가 silent하게 base OS를 바꾼다. 운영 환경에서 이걸 발견하는 자리가 prod 인시던트라면 늦다. **builder는 명시해두는 편이 안전하다.**

### AOT 동작 변경

`spring-boot-aot` 처리(AOT 빌드 시점에 미리 reflection 메타데이터 등을 생성하는 자리)가 4.x에서 한 번 정돈됐다. 가장 눈에 띄는 자리는 **AOT processing이 `bootRun`에서도 발화하는 옵션이 다듬어진 점**이다. 이 영향이 가장 자주 나타나는 자리는 native 빌드와 함께 쓸 때다. 단일 모듈 JVM 빌드에서는 거의 보이지 않지만, 15장에서 native로 넘어갈 때 다시 만난다.

### Native 통합 변경

`org.graalvm.buildtools.native` 플러그인의 기본 좌표·동작이 4.x와 함께 한 차례 정돈됐다. 회사 빌드에 native 이미지가 들어 있다면 plugin 버전을 함께 올리는 쪽이 안전하다. 자세한 자리는 15장.

### Configuration Cache가 디폴트에 더 가까워졌다

4.0의 plugin은 **Configuration Cache를 완전 지원**한다. 3.x도 대체로 지원했지만 일부 task에 미세한 위반이 남아 있었다. 4.0에 와서 그 미세한 자리들이 정리됐다. 회사 빌드에서 Configuration Cache를 켜두지 않았다면, 4.x로 옮긴 김에 함께 켜보는 편이 낫다. 13장에서 본격적으로 다룬다.

> **박스 — 3.5.x 유지보수 라인 독자용 분기 가이드**
>
> 모두가 당장 4.0으로 올라가는 건 아니다. 회사 정책상 3.5.x를 한참 더 굴려야 한다면 다음을 기억하자.
>
> 1) **3.5.x는 OSS 지원 종료가 2026년 6월로 예정**되어 있다 (Spring Boot의 정규 12개월 OSS support 기준). 그 이후엔 commercial support가 필요해진다.
> 2) **3.5.x → 4.x로 옮길 때 가장 큰 일은 Gradle wrapper 버전**이다. 3.5.x는 Gradle 7.x도 받아주지만 4.x는 안 받는다. wrapper를 9.x로 올리는 작업을 4.0 전환과 별개의 PR로 먼저 처리해두면 PR 하나에 변수 두 개가 섞이지 않는다.
> 3) **builder image는 지금 시점에 명시해두자.** 3.x 시절의 `jammy` 베이스를 명시적으로 박아두면, 추후 4.0 업그레이드 시점에 그 한 줄이 OS layer 변화의 위험을 명시적으로 노출시켜준다.
> 4) **Java 21 toolchain은 미리 옮겨두자.** 3.5.x도 Java 21을 받는다. 4.x로 옮길 때 Java 버전 변화까지 한꺼번에 일어나는 게 가장 사고 위험이 높다.
>
> 4.x로 올라갈 단계가 됐을 때 위 네 가지가 미리 처리돼 있으면, plugin 좌표 한 줄 바꾸는 PR로 전환이 마무리된다.

## 6장에서 자란 빌드와 그 다음

이제 `ch04-bootapp/`의 상태를 한 번 점검하자. 5장 끝에서는 BOM과 Catalog가 자리를 잡은 build script까지였다. 6장에서는 그 위에 다음이 박혔다.

- `./gradlew bootJar`이 `build/libs/ch04-bootapp-0.0.1-SNAPSHOT.jar`를 만든다. `java -jar` 한 줄로 실행되는 fat jar다.
- `./gradlew bootRun`이 IDE를 거치지 않고 앱을 부팅한다. `--args`로 런타임 인자를 받는다.
- `./gradlew bootBuildImage`가 OCI 이미지를 만든다. Dockerfile 없이.
- main class는 자동 탐지에 의존하지 않고 `springBoot { mainClass = "..." }`로 명시했다.
- layered jar는 기본 ON 그대로 두고, 그게 OCI 이미지 캐시의 토대라는 점을 기억해뒀다.

> **박스 — 6장의 마이그레이션 노트 모음**
>
> 회사 빌드에서 이 챕터의 자리들을 옛 모양에서 4.x 표준으로 옮길 때 한꺼번에 보는 자리.
>
> ```kotlin
> // 옛 모양 (3.x 시절 흔히 보던 코드)
> tasks.named<BootJar>("bootJar") {
>     mainClass.set("com.example.shop.ShopApplication")
>     archiveClassifier.set("boot")
> }
>
> // 4.x 권장
> tasks.named<BootJar>("bootJar") {
>     mainClass = "com.example.shop.ShopApplication"
>     archiveClassifier = "boot"
> }
>
> // 더 권장 — extension에 한 번만
> springBoot {
>     mainClass = "com.example.shop.ShopApplication"
> }
> ```
>
> ```kotlin
> // 옛 모양 — Configuration Cache에 친화적이지 않다
> tasks.named<BootBuildImage>("bootBuildImage") {
>     docker {
>         publishRegistry {
>             username = System.getenv("GHCR_USER")
>             password = System.getenv("GHCR_TOKEN")
>         }
>     }
> }
>
> // 4.x 권장 — Provider API로 받는다
> tasks.named<BootBuildImage>("bootBuildImage") {
>     docker {
>         publishRegistry {
>             username = providers.environmentVariable("GHCR_USER").get()
>             password = providers.environmentVariable("GHCR_TOKEN").get()
>         }
>     }
> }
> ```
>
> ```kotlin
> // 옛 모양 — eager 패턴, 9.x에서 deprecation 경고
> tasks {
>     "bootJar"(BootJar::class) {
>         mainClass = "..."
>     }
> }
>
> // 4.x 권장 — lazy
> tasks.named<BootJar>("bootJar") {
>     mainClass = "..."
> }
> ```

남은 매듭이 한두 가지 있다. 우선 우리 빌드의 **테스트가 아직 단순하다.** `test` task 하나에 단위 테스트와 (앞으로 추가될) 통합 테스트가 한꺼번에 들어간다. Spring 앱의 통합 테스트는 컨텍스트 부팅이 들어가서 느리다. 그걸 단위 테스트와 같은 task에서 한꺼번에 돌리면 빠른 피드백을 잃는다. 7장에서 `jvm-test-suite` 플러그인으로 `integrationTest` suite를 별도로 만들고, `check`가 둘을 모두 부르게 정리한다.

그리고 회사 빌드가 이쯤에서 자라기 시작하면, 모듈을 한 번 쪼개고 싶어진다. 도메인을 별도 library 모듈로 빼고, 앱은 그 모듈에 의존하는 모양으로. 그 단계에서 만나는 가장 흔한 사고가 **"library 모듈에서 만든 jar가 비어 보이는"** 일이다. 9장에서 이 사고를 진단하고 막는 자리를 만든다. 6장에서 본 `bootJar`와 `jar`의 공존, `productionRuntimeClasspath`의 의미가 그 자리의 해독 도구로 다시 등장한다.

다음 챕터로 넘어가자. 테스트의 분리부터다.
