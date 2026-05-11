# 17장. Gradle 9.x로 옮긴다 — 마이그레이션 노트 모음

회사에 7년 된 Spring Boot 빌드가 하나 있다고 해보자. 처음 만들 때는 Gradle 5.x였다. 누군가 한 번 6으로 올렸고, 또 다른 누군가가 7로 올렸고, 8.4쯤에서 멈춰 있다. 지금 그 빌드를 9.5로 올리라는 임무가 떨어졌다. 한 줄짜리 명령으로 끝났으면 좋겠지만, 우리가 아는 한 그렇지 않을 것이다. 어디부터 깨질지 짐작도 잘 안 간다.

이런 상황은 흔하다. 그리고 솔직히 말해서, **회사 빌드를 9로 옮기는 일은 1주차에 끝나지 않는다.** 1장에서 "8.x를 쓰는 분께"라는 박스로 미뤄둔 약속이 있다. 마이그레이션 체크리스트는 17장에서 다룬다고 했다. 그 약속을 회수할 때다. 다만 여기서 한 가지를 분명히 하고 시작하자. 이 장은 **Gradle 버전 마이그레이션**에 대한 장이다. Spring Boot 3.x에서 4.x로 옮기는 일은 6장에서 이미 다뤘다. 둘은 자주 같이 다가오지만 별개의 일이고, 별개로 진행해야 디버깅이 쉽다.

> **두 마이그레이션의 역할 분담**
> - **6장 — Spring Boot 3.x → 4.x:** Boot 플러그인의 task 시그니처, Paketo builder 기본값, AOT/Native 동작, Spring 측이 요구하는 Gradle 최소 버전(8.14+).
> - **17장 — Gradle 8.x/7.x → 9.5:** Daemon JDK 요구, 제거된 API, archive reproducibility, Configuration Cache, 그리고 third-party plugin 호환성.
>
> 둘을 한 PR에 묶지 말자. 한 번에 한 가지만 옮긴다. 깨지면 어느 마이그레이션이 깬 건지 즉시 안다.

이 장의 흐름은 이렇다. 먼저 Gradle 9.0이 가져온 진짜 큰 변화들을 정리한다. 그 다음 9.1~9.5의 작은 변화 중 마이그레이션 시 도움이 되는 것들을 본다. 그리고 step-by-step 절차를 따른다 — wrapper 올리고, 빌드 깨지고, 메시지 읽고, 가장 자주 깨지는 다섯 가지를 처방한다. 마지막으로 우리 가상 앱 `shop`을 7.x 시절의 가상 빌드로 되돌렸다가 9.5로 다시 올리는 일지를 본다.

## 9.0이 진짜로 가져온 것 — 큰 망치들

9.x 라인 안에서 9.1, 9.2, 9.3은 사실 부드러운 변화들이다. 정작 칼을 휘두른 건 9.0이다. 9.0에서 결정된 변화들이 8.x 빌드를 깨는 거의 모든 원인이다. 여섯 가지로 묶어보자.

### Daemon JDK 17+ 필수

이게 가장 먼저 닿는 벽이다. **Gradle 9.x의 데몬은 JDK 17 이상에서만 돈다.** 8.x는 JDK 8로도 데몬을 띄울 수 있었지만 9.x는 아니다. CI 머신에 JDK 11이 깔려 있고 `JAVA_HOME`이 거기 박혀 있다면, 9.x로 wrapper를 올린 순간 빌드가 시작도 못 한다.

여기서 헷갈리지 말아야 할 게 있다. **데몬 JDK와 빌드 대상 JDK는 다르다.** 데몬은 Gradle 자기 자신이 도는 JVM이다. 빌드 대상 JDK는 우리 앱을 컴파일하는 JDK다. 9.x의 요구는 데몬 JDK다. 우리 앱은 여전히 JDK 21로 컴파일할 수도, JDK 17로 컴파일할 수도 있다. 4장에서 정착시킨 toolchain이 이걸 정확히 처리해준다.

```kotlin
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

데몬은 17로 돌고, 컴파일은 21로 한다. toolchain을 4장에서 박아둔 빌드라면 이 변화는 거의 무료다. 박아두지 않았다면 9.x 마이그레이션과 함께 toolchain을 박는 게 좋다 — 미루지 말자.

### `jcenter()` 제거

`jcenter()`가 마침내 사라졌다. JFrog가 2021년에 read-only 상태로 만든 이후 이미 5년 가까이 deprecation 신호가 있었지만, 9.0에서 마침내 빌드 스크립트에서 호출 자체가 불가능해졌다. settings나 build script에 아직 `jcenter()`가 남아 있다면 9.x에서 즉시 빌드 실패다.

```kotlin
// Before — 9.x에서 더 이상 동작하지 않는다
repositories {
    jcenter()
}

// After
repositories {
    mavenCentral()
}
```

대부분의 라이브러리는 Maven Central에 그대로 있다. `jcenter`에만 있고 Central엔 없는 것이 있다면, 그건 이미 유지보수가 끊긴 라이브러리일 가능성이 높다. 이 기회에 의존성을 한번 정리하자.

### `Project#exec` / `Project#javaexec` 제거

8장에서도 미리 한 번 봤지만, 다시 정리하자. Gradle 8.x는 `Project#exec { ... }`나 `Project#javaexec { ... }`를 deprecation 경고로만 띄워줬다. 9.x는 아예 메서드를 지웠다.

```kotlin
// Before — 9.x에서 메서드 자체가 없다
val gitSha = project.exec {
    commandLine("git", "rev-parse", "HEAD")
    standardOutput = ByteArrayOutputStream().also { /* ... */ }
}

// After — providers.exec 로 옮긴다
val gitSha: Provider<String> = providers.exec {
    commandLine("git", "rev-parse", "HEAD")
}.standardOutput.asText.map { it.trim() }
```

이 변화는 단순한 API 교체가 아니다. `Project#exec`는 **즉시 실행**이었다. configuration phase에서 호출되면 그 자리에서 git 명령이 돌았다. 그러니 Configuration Cache와는 본질적으로 양립할 수 없었다. `providers.exec`는 **lazy provider**다. 실제로 값이 필요한 시점까지 실행을 미루고, 그 결과는 Configuration Cache에 안전하게 직렬화된다.

이 차이는 12장에서 우리가 `shop.build-info` 플러그인을 만들 때 이미 만났다. 12장의 그 패턴이 9.x 시대의 표준이다. 거기서 익혔던 `providers.exec { }.standardOutput.asText.map { ... }` 한 줄이 마이그레이션의 답이기도 하다.

### Convention API 완전 제거

이게 빌드 스크립트보다는 **third-party plugin**에 더 큰 영향을 주는 변화다. Gradle 7부터 deprecated 였던 `project.convention` API와 `SourceSetConvention` 같은 옛 모델이 9.0에서 완전히 제거됐다. 그 자리에 들어선 게 우리가 줄곧 써온 **Extensions** 모델이다.

빌드 스크립트 입장에선 큰 영향이 없다. 우리는 이미 `java { ... }`, `kotlin { ... }`, `application { ... }` 같은 extension 블록으로 일하고 있다. 문제는 **오래된 plugin**이다. 사내에서 쓰는 자작 plugin이 5~6년 전에 쓰여졌고, 그동안 손길이 안 닿았다면 `project.convention.getPlugin(...)` 같은 호출이 남아 있을 가능성이 높다. 그게 9.x에서 빌드를 깬다.

처방은 간단하다. plugin 코드를 열어서 `convention.getPlugin(...)` 같은 호출을 `extensions.getByType(...)`로 바꾸는 것. 다만 그 plugin이 오픈소스라면 이미 누군가 PR을 올렸을 가능성이 높다. **9.x 마이그레이션을 시작하기 전에 가장 먼저 할 일은, 우리가 쓰는 third-party plugin들의 최신 버전이 9.x를 지원하는지 점검하는 일이다.** 이건 뒤에서 다시 본다.

### KGP 2.0+ 필수

Kotlin DSL을 쓰고 있다면 — 그러니까 이 책의 모든 독자라면 — **Kotlin Gradle Plugin 2.0 이상이 필수**다. KGP 1.9에 머물러 있는 빌드는 9.x에서 안 돈다.

```toml
# gradle/libs.versions.toml
[versions]
kotlin = "2.2.0"

[plugins]
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }
```

5장에서 정착시킨 Version Catalog가 도움이 된다. catalog 한 곳에서 Kotlin 버전을 올리면 모든 모듈이 동시에 따라온다. 다만 KGP 2.0은 K2 컴파일러를 기본으로 쓰기 때문에, 우리 코드에서 일부 컴파일 오류가 새로 잡힐 수 있다. 이건 KGP의 책임이고, Kotlin 측에서 마이그레이션 가이드가 잘 정리돼 있다. Kotlin 2.1 이후엔 strict nullness가 더 엄격해진 것도 한 줄 기억해두자 — 이전엔 그냥 넘어가던 nullable 추론이 컴파일 오류로 바뀌는 경우가 있다.

### Archive task의 기본 reproducible

이게 가장 조용하면서도 가장 미묘하게 깨지는 변화다. 9.0부터 `Jar`, `Zip`, `Tar` 같은 archive task들이 **기본적으로 reproducible**하게 동작한다. 무슨 뜻인가?

reproducible archive란 같은 입력에 대해 항상 같은 바이트의 archive를 만든다는 뜻이다. 그러기 위해 두 가지를 기본으로 잡는다. **첫째, archive 안의 파일 타임스탬프를 모두 0(또는 고정값)으로 설정한다.** 둘째, **파일 순서를 alphabetical로 정렬한다.** 같은 코드를 빌드하면 어제와 오늘 만든 jar가 바이트 단위로 동일하다.

이건 거의 모든 경우에 좋은 변화다. Build Cache의 효율이 올라가고, 같은 소스에서 같은 image hash가 나오니 OCI 이미지 캐시도 안정적이다. 그런데 한 가지 경우에 깨질 수 있다. **빌드 스크립트나 도구가 jar 안의 파일 타임스탬프에 의존하고 있을 때.** 예를 들어 어떤 회사 도구가 jar를 받아서 "가장 최근 빌드된 파일이 어떤 것이냐"를 manifest의 타임스탬프로 판단한다면, 이제 그 타임스탬프가 모두 0이라 판단이 안 된다.

이 경우 대부분은 도구를 고치는 게 옳지만, 호환을 위해 일시적으로 옛 동작이 필요하다면 명시적으로 끄는 길이 있다.

```kotlin
tasks.named<Jar>("jar") {
    isPreserveFileTimestamps = true
    isReproducibleFileOrder = false
}
```

가능하면 끄지 말자. 이 변화 덕분에 13장의 Build Cache가 더 잘 동작한다.

## 9.1~9.5 — 작은 변화들이 마이그레이션을 돕는다

9.0이 칼을 휘둘렀다면 9.1부터 9.5까지는 **그 칼맞은 자리를 봉합하는** 작업이다. 마이그레이션할 때 직접 도움이 되는 것 위주로 본다.

9.1~9.4의 핵심 흐름은 두 가지다. **Configuration Cache 호환성이 단계적으로 개선됐고**, **진단 메시지가 더 명확해졌다.** 8.x에서 Configuration Cache를 켰을 때 받던 모호한 메시지 — "Some configuration cache problems were found" 만 띄우고 어디서 깨졌는지 알기 힘들었던 — 가 9.x를 거치면서 점차 정확해졌다. 9.3 이후로는 위반 메시지가 "이 task의 이 입력이 이런 이유로 위반"이라는 형식으로 좁아진다.

이게 마이그레이션의 실용적인 함의는 이렇다. **9로 먼저 옮기고 나서 Configuration Cache를 켜야 메시지가 명확하다.** 8.x에서 Configuration Cache를 켜고 9로 옮기려고 시도하면, 8.x의 모호한 메시지와 마이그레이션 깨짐이 섞여서 뭐가 진짜 원인인지 알기 어렵다. 13장에서 우리가 잡아둔 Configuration Cache는, 마이그레이션할 때 잠시 꺼뒀다가 9.5에 도착해서 다시 켜는 편이 낫다.

9.5에서 마이그레이션에 직접 도움이 되는 신규 기능들이 몇 가지 있다. 차례대로 짚자.

**Task provenance** — 빌드가 깨졌을 때 "이 task는 어느 plugin에서, 어느 script에서 등록됐는지"를 출력해준다. 8.x에서 빌드가 실패하면 "이 task가 어디서 왔는지 모르겠는데?" 하는 순간이 자주 있었다. 9.5는 답을 같이 띄워준다. 마이그레이션 중 third-party plugin이 일으킨 깨짐을 추적할 때 시간을 크게 아낀다.

**Wrapper retries** — 14장에서도 한 번 본 변화다. wrapper distribution 다운로드를 자동으로 재시도한다. CI에서 wrapper를 9.5로 올린 직후 잠깐 flaky한 실패가 늘 수 있는데, retries 한 줄로 진정된다.

**Precompiled Settings plugin type-safe accessor** — 10장에서 우리가 정착시킨 convention plugin의 sister 기능이다. project 수준 precompiled plugin은 이미 type-safe accessor가 있었지만, settings 수준은 그동안 string-based API로 떨어졌다. 9.5는 settings precompiled plugin에도 accessor를 만들어준다. 멀티 모듈에서 settings convention을 만들고 있다면 이전보다 훨씬 깔끔하다.

**`disallowChanges()`** — Property를 더 이상 못 바꾸게 잠그는 API다. plugin을 만들 때 "이 시점부터는 사용자가 이 값을 못 바꾼다"고 명시할 수 있다. 12장에서 만든 `shop.build-info` 같은 자작 plugin에 도움이 된다.

**`gradle init --into <dir>`** — 새 프로젝트를 빈 디렉터리에만 만들 수 있던 init이 이제 기존 디렉터리 안으로 파일을 풀어준다. 마이그레이션의 핵심은 아니지만, 새 모듈을 보탤 때 편하다.

**`--develocity-url` CLI** — Develocity URL을 CLI로 한 번에 전달할 수 있다. 사내 Develocity를 쓰는 팀이라면 마이그레이션 후 CI 스크립트가 한 줄 짧아진다.

> **마이그레이션 노트 — 9.0에서 사라진 옛 패턴**
>
> ```kotlin
> // Before (Gradle 7 이전 잔재)
> tasks.create("myTask") {       // eager — 9.x에서 동작은 하지만 권장 안 함
>     doLast { println("hi") }
> }
>
> // After
> tasks.register("myTask") {     // lazy — 정석
>     doLast { println("hi") }
> }
> ```
>
> 3장에서 lazy registration이 정석이라고 미리 약속했었다. 9.x에서 Convention API가 사라지면서, 12장에서 정착시킨 Provider/Property 표준화와 더불어 이 lazy 표준이 더 단단해졌다. eager 패턴이 남아 있는 회사 빌드라면 마이그레이션 PR과 함께 정리하는 게 좋다.

## Step-by-step — 빌드를 9.5로 옮기는 절차

이론은 충분히 봤다. 이제 실제로 옮긴다. 절차는 다섯 단계다.

### 1단계 — 이전 점검: third-party plugin 호환성

가장 먼저 할 일은 **빌드를 건드리지 않는 일**이다. 우리가 쓰는 plugin들이 9.x를 지원하는지 먼저 확인한다. 이걸 빼먹고 wrapper부터 올리면, 정작 깨진 게 우리 빌드 스크립트인지 third-party plugin인지 구분이 안 된다.

확인 방법은 단순하다. 우리 `libs.versions.toml`을 펴서 plugin과 의존성 중 빌드 도구 성격을 가진 것들 — Spring Boot Gradle Plugin, Kotlin Gradle Plugin, Spotless, Detekt, SonarQube plugin, JMH plugin, 사내 자작 plugin 등 — 의 release notes나 changelog에서 "Gradle 9 support"가 언급된 버전을 찾는다. **두 가지가 함께 잡혀야 한다.** Configuration Cache 호환과 Gradle 9.x 호환. 이게 같이 명시된 버전을 골라 catalog에 박는다.

```toml
[versions]
spring-boot = "4.0.6"
kotlin = "2.2.0"
spotless = "7.0.0"
detekt = "1.23.7"
```

특히 사내 자작 plugin이 있다면, 그 plugin의 코드를 한번 훑어보자. `project.convention`, `Project#exec`, `tasks.create`, `tasks.getByName` 같은 옛 패턴이 있다면 마이그레이션과 함께 정리해야 한다.

> **함정 박스 — Configuration Cache 호환과 Gradle 9 호환은 다르다**
> Configuration Cache 호환만 된다고 Gradle 9에서 자동으로 도는 게 아니다. 예를 들어 `Project#exec`만 쓰던 plugin은 Configuration Cache에선 동작했었지만(deprecation 경고만 떠 있었음) Gradle 9에서는 메서드 자체가 없으니 즉시 실패한다. **두 가지를 모두 확인하자.**

### 2단계 — wrapper 업그레이드

이제 칼을 뽑는다. 한 줄이다.

```bash
./gradlew wrapper --gradle-version 9.5 --distribution-type=bin
```

`--distribution-type=bin`은 14장에서 정한 표준이다. 잊지 말자. 이 명령은 `gradle/wrapper/gradle-wrapper.properties`의 `distributionUrl`만 9.5로 바꾼다. 다음 빌드부터 9.5가 자동으로 받아진다.

그리고 이 wrapper 변경을 **별도의 한 PR로 박자.** 빌드 스크립트 변경과 섞지 말자. 이 PR이 깨지면 깨진 채로 머지하지 말고, 어디까지 깨졌는지 본다. 이게 마이그레이션의 출발선이다.

### 3단계 — 빌드 실패 메시지 읽기

`./gradlew build`를 돌려본다. 거의 확실히 어딘가에서 깨진다. 9.x의 메시지는 8.x보다 훨씬 친절해졌으니, **메시지를 끝까지 읽자.** 다음 몇 가지 패턴을 자주 본다.

```
> Could not resolve all artifacts for configuration ':compileClasspath'.
   > Cannot resolve external dependency com.example:foo because no repositories are defined.
```

`jcenter()`를 지웠는데 거기에만 있던 의존성이 있을 때 나오는 메시지다. 의존성 좌표를 확인하고, Maven Central에 있는지 본다. 없다면 그 라이브러리가 이미 EOL이다.

```
> Unresolved reference: convention
```

자작 plugin의 코드가 `project.convention.getPlugin(...)`을 쓰고 있을 때 나오는 메시지다. `extensions.getByType<JavaPluginExtension>()` 같은 형태로 옮긴다.

```
> Cannot use 'project.exec' from outside of a configured execution.
```

(혹은 메서드 자체가 없다는 컴파일 오류.) `Project#exec` 호출이 남아 있다. `providers.exec { }`로 옮긴다 — 12장의 패턴 그대로다.

```
> Unsupported class file major version 65
```

JDK 17 미만으로 데몬을 띄우려 했을 때 나는 메시지다. `JAVA_HOME`을 확인하고, CI라면 `actions/setup-java@v5`의 `java-version`을 17 이상으로 올린다. 우리 앱은 toolchain으로 계속 21에 머무를 수 있다.

### 4단계 — 가장 자주 깨지는 다섯 가지 처방

수십 개의 마이그레이션 사례를 압축하면 가장 자주 깨지는 자리는 다섯 군데로 좁혀진다. 표로 정리하자.

| # | 깨지는 자리 | 증상 | 처방 |
|---|---|---|---|
| 1 | `Project#exec` / `Project#javaexec` | `Unresolved reference: exec`(혹은 컴파일 실패) | `providers.exec { commandLine(...) }.standardOutput.asText.map { it.trim() }` |
| 2 | `jcenter()` | dependency resolution 실패 | `mavenCentral()`로 교체. 없는 의존성은 EOL이다 |
| 3 | `tasks.create` / `getByName` eager | deprecation 경고 더미 (실패는 아님) | `tasks.register` / `named<T>(...)` 로 교체. 마이그레이션 끝나고 한 번에 정리 |
| 4 | 자작 plugin의 Convention API | `Unresolved reference: convention` | `project.extensions.getByType<...Extension>()` 로 교체 |
| 5 | Archive 타임스탬프 의존 도구 | 외부 도구가 jar 내부 timestamp로 판단 실패 | 도구를 고치는 게 옳다. 임시 호환은 `isPreserveFileTimestamps = true` |

이 표가 회사 빌드를 옮길 때 첫 1주의 절반을 단축해준다. 깨진 메시지를 받으면 이 표부터 보자.

### 5단계 — Configuration Cache를 다시 켠다

마이그레이션 PR에서 잠시 꺼뒀던 Configuration Cache를 9.5에서 다시 켠다.

```properties
# gradle.properties
org.gradle.configuration-cache=true
org.gradle.configuration-cache.problems=warn
org.gradle.configuration-cache.parallel=true
```

13장에서 다듬어둔 그대로다. 9.x의 진단 메시지가 8.x보다 훨씬 명확하니, 혹시 8.x에서는 "이상한데 동작은 하던" 코드가 있었다면 9.5에서 깨끗하게 잡힐 수 있다. 잡히는 위반은 13장의 처방대로 하나씩 정리한다. 그리고 `problems=warn`을 `=fail`로 옮긴다.

## 회고 — `shop` 앱의 7.x 시절로 돌아가본다

이론과 절차를 봤으니 우리 가상 앱 `shop`으로 한 번 시뮬레이션해보자. 이 책이 9.5 기준으로 자라왔지만, 만약 같은 앱을 7.x 시절에 만들었다면 어떤 모양이었을까. 그 코드를 9.5로 옮기는 과정을 짧은 일지로 본다.

7.x 시절의 `shop`은 대략 이렇게 생겼을 것이다.

```kotlin
// settings.gradle.kts (7.x 시절)
rootProject.name = "shop"
include("app", "domain", "order", "payment")

// 의존성 repo는 각 모듈에서 따로 선언
```

```kotlin
// app/build.gradle.kts (7.x 시절)
import java.io.ByteArrayOutputStream

plugins {
    id("org.springframework.boot") version "2.7.18"
    id("io.spring.dependency-management") version "1.1.4"
    kotlin("jvm") version "1.9.10"
    kotlin("plugin.spring") version "1.9.10"
}

repositories {
    mavenCentral()
    jcenter()  // 여전히 살아 있던 시절
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation(project(":domain"))
}

dependencyManagement {
    imports {
        mavenBom("org.springframework.boot:spring-boot-dependencies:2.7.18")
    }
}

tasks.create("printGitSha") {
    doLast {
        val out = ByteArrayOutputStream()
        project.exec {
            commandLine("git", "rev-parse", "HEAD")
            standardOutput = out
        }
        println(out.toString().trim())
    }
}
```

이 빌드를 9.5로 옮기는 일지다.

**Day 1 — 점검.** 먼저 plugin들의 9.x 호환 버전을 본다. Spring Boot는 4.0.6, Kotlin은 2.2.0이 9.x 라인을 지원한다. 우리는 Spring Boot 3.x → 4.x도 같이 옮길 게 아니라, **이번 PR은 Gradle만** 옮기기로 한다. Spring Boot는 일단 3.5.x(유지보수 라인)에 머물러도 9.x와 호환된다는 점을 확인했다 — 두 마이그레이션을 분리한다.

**Day 2 — wrapper.** `./gradlew wrapper --gradle-version 9.5 --distribution-type=bin` 한 줄. 별도 PR로 박는다. `./gradlew build`를 돌리면 빨갛게 깨진다.

**Day 3~4 — 메시지 한 줄씩.** 4단계의 표를 옆에 두고 깨진 곳을 하나씩 본다.

- `jcenter()`가 첫 번째로 잡힌다. Maven Central에 있는 의존성만 우리 빌드에 들어 있으니 `jcenter()` 한 줄만 지운다.
- `Kotlin Gradle Plugin 1.9 incompatible`이 두 번째로 잡힌다. catalog로 Kotlin을 2.2.0으로 올린다. `kotlin("plugin.spring")`도 같이 올라온다.
- `project.exec`가 세 번째로 잡힌다. 위의 `printGitSha` task를 다시 짠다.

```kotlin
// After — providers.exec 로 옮긴다
abstract class PrintGitShaTask : DefaultTask() {
    @get:Input
    abstract val gitSha: Property<String>

    @TaskAction
    fun run() {
        println(gitSha.get())
    }
}

tasks.register<PrintGitShaTask>("printGitSha") {
    gitSha = providers.exec {
        commandLine("git", "rev-parse", "HEAD")
    }.standardOutput.asText.map { it.trim() }
}
```

12장의 패턴 그대로다. 그리고 `tasks.create`도 같이 `tasks.register`로 바꾼다.

- 네 번째로 IDE에서 Kotlin 2.2의 strict nullness가 옛 코드 한두 줄을 잡는다. nullable 타입을 명시한다. 이건 KGP 2.0 마이그레이션 가이드의 영역이다.

**Day 5 — Configuration Cache.** `org.gradle.configuration-cache=true`를 켠다. `problems=warn`으로 시작한다. 처음 빌드에서 한두 개 위반이 더 잡힌다 — Build Cache 어노테이션이 누락된 자작 task가 있었다. `@InputFile`, `@OutputFile`을 정확히 박는다. 그러고 나면 빌드가 두 번째부터 빠르게 돈다.

**Day 6~ — Spring Boot.** Gradle 마이그레이션이 안정화된 다음, 별도 PR로 Spring Boot 3.x → 4.x로 옮긴다. 이건 6장의 영역이다.

이 일지가 모든 회사 빌드에 그대로 맞지는 않는다. 자작 plugin이 많고 의존성이 복잡한 회사일수록 Day 3~4의 메시지 처리에 시간이 더 든다. 그게 정상이다. **점진 도입을 받아들이자.** 한 PR로 모든 걸 옮기려 들지 말고, wrapper 한 PR, 깨진 자리 처방 한 PR, Configuration Cache 활성화 한 PR, Spring Boot 마이그레이션 한 PR로 나누자. 깨졌을 때 어느 PR이 깬 건지 즉시 안다. 1주차에 끝나지 않는다는 사실을 받아들이는 게 마이그레이션을 빨리 끝내는 길이다.

## 마무리

Gradle 9.x 마이그레이션은 결국 세 가지를 점검하는 일이다. **데몬 JDK가 17 이상인가, third-party plugin들이 9.x를 지원하는가, 그리고 빌드 스크립트에 옛 API의 잔재가 남아 있는가.** 셋 다 클리어하면 9.x는 8.x와 거의 같은 느낌으로 돈다. 다만 옛 API의 잔재가 우리 빌드만의 문제가 아니라 회사가 5~7년 쌓아온 빚일 수 있다는 점, 그 빚을 한 번에 정리할 수는 없다는 점을 받아들이자.

이 장의 처방 표를 한번 더 짚자. `Project#exec`는 `providers.exec`로, `jcenter()`는 `mavenCentral()`로, `tasks.create`는 `tasks.register`로, `project.convention`은 `extensions.getByType`으로, archive timestamp 의존은 가능하면 도구 쪽을 고친다. 다섯 가지만 기억해두면 대부분의 빌드가 9.x에 도착한다.

그리고 이 책의 약속을 두 개 회수했다. **1장의 약속** — 8.x 사용자를 위한 마이그레이션 체크리스트가 17장에 있다는 약속. 그리고 **3장의 lazy registration 약속** — Convention API가 사라지면서 lazy + Property가 단단한 표준이 됐다는 약속. 두 약속을 회수했으니 책의 거의 끝에 다다랐다.

다음 18장은 마지막 장이다. 책에서 다룬 18가지를 회고하면서, "이제 어디로 갈 것인가"를 본다. Isolated Projects, Develocity, GraalVM Native 운영 심화 — 이 책에서 다 다루지 못한 다음 단계들을 짧게 짚는다. 우리 `shop` 앱의 마지막 모습도 거기서 본다.
