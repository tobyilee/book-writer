# 4장. Maven에서 옮겨오는 다리 — pom.xml과 build.gradle.kts의 1:1 매핑

1장에서 "Maven에서 옮겨온 분께"라는 박스로 약속을 하나 걸어뒀다. phase는 task graph로, dependencyManagement는 platform/BOM으로, parent pom은 Convention Plugin으로. 정확한 매핑은 4장에서 받는다고 했었다. 이 장이 그 약속을 받는 자리다.

Maven으로 5년을 짠 사람이 어느 날 Gradle 프로젝트에 던져졌다고 해보자. Spring Initializr에서 Gradle - Kotlin DSL을 골라 다운로드를 받고, IntelliJ로 열어 본다. `pom.xml`이 있어야 할 자리에 `settings.gradle.kts`와 `build.gradle.kts`라는 두 파일이 있다. 둘 다 열어보면 어쩐지 본 듯한 단어들이 흩어져 있는데 — `dependencies`, `plugins`, `repositories` — 정작 우리가 알던 `<dependencyManagement>`, `<parent>`, `<profile>` 같은 친숙한 친구들은 보이지 않는다. 어디 갔지?

이런 상황이 가장 난감하다. 새 도구를 처음부터 배우는 것보다 더 어려운 건, 옛 도구의 모든 개념이 어디로 갔는지 모르는 상태에서 IDE 자동완성 하나에 기대 더듬더듬 짜는 것이다. 어디로 갔는지를 모르니, 자기가 잘 짜고 있는지조차 알 수가 없다.

이번 장에서 우리는 그 매핑을 정면으로 받는다. Maven의 9개 핵심 개념이 Gradle에서 정확히 어디로 갔는지 표 하나로 그리고, 그 다음 `ch04-bootapp/` 폴더에서 동작하는 Spring Boot 단일 모듈 앱의 `settings.gradle.kts`와 `build.gradle.kts`를 한 줄씩 같이 읽어본다. 이 챕터를 통과하고 나면, 우리가 알던 Maven 개념은 모두 "여기 있다"고 손가락질할 수 있게 될 것이다.

> **이번 챕터는 `ch04-bootapp/` 폴더에서 동작한다.** Spring Initializr가 만든 단일 모듈 Spring Boot 앱이 이번 장의 기반이다. 이후 챕터들이 모두 이 앱 위에 차곡차곡 쌓인다. Toolchain까지 박힌, 회사에 그대로 가져가도 부끄럽지 않을 최소 구성을 목표로 한다.

## 매핑의 큰 그림

먼저 거시 지도부터 보자. Maven에서 익숙했던 개념 9개가 Gradle 9.5에서 어디에 자리잡는지의 매핑표다. 본문에서 하나씩 풀어볼 예정이지만, 일단 전체 그림이 한 번에 보여야 마음이 놓인다.

| Maven (pom.xml) | Gradle (Kotlin DSL) | 자세히 |
|---|---|---|
| `<dependencies>` | `dependencies { implementation(...) }` | 5장 |
| `<dependencyManagement>` | `dependencies { implementation(platform(...)) }` 또는 `io.spring.dependency-management` 플러그인 | 5장 |
| `<parent>` (spring-boot-starter-parent) | `plugins { id("org.springframework.boot") }` + Convention Plugin | 본 장 + 10장 |
| `<profile>` | `bootRun --args` + `-P` Project property + variant | 본 장 |
| `<pluginManagement>` | `settings.gradle.kts`의 `pluginManagement { }` | 본 장 |
| `<repositories>` | `settings.gradle.kts`의 `dependencyResolutionManagement { repositories { } }` | 본 장 |
| `mvn clean install` | `./gradlew clean build` | 본 장 |
| `mvn` 명령 (시스템 설치) | `./gradlew` (프로젝트 wrapper) | 본 장 |
| `<properties><java.version>` | `java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }` | 본 장 |

표만 봐서는 와닿지 않을 것이다. 표를 외우자는 게 아니다. 표는 지도일 뿐, 우리는 이제 길로 들어선다. 하나하나 본문에서 코드로 만나보자.

한 가지 미리 짚고 가자. Maven은 `pom.xml` 한 파일이 모든 걸 했다 — 빌드의 입구부터 의존성, 플러그인, repository까지. Gradle은 그 책임을 두 파일로 나눈다. **`settings.gradle.kts`는 빌드의 입구**이고, **`build.gradle.kts`는 한 프로젝트의 구체적인 빌드 정의**다. 9.5 시점의 Gradle은 settings의 책임을 더 명확히 한 방향으로 가고 있다 — repository와 plugin 버전 관리는 settings에서, 의존성과 task 정의는 build에서. 이 분리가 처음에는 번거롭게 느껴지지만, 멀티 모듈로 가면 이 분리가 왜 좋은지 자연스럽게 알게 된다. 일단은 "settings는 입구, build는 본문"이라고 기억해두자.

## settings.gradle.kts — pluginManagement와 dependencyResolutionManagement

`ch04-bootapp/`의 `settings.gradle.kts` 전체를 먼저 보자. 9.5 시점의 표준 골격이다.

```kotlin
// settings.gradle.kts
pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

plugins {
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}

dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories {
        mavenCentral()
    }
}

rootProject.name = "shop"
```

13줄짜리 파일인데, 이 안에 Maven에서 우리가 알던 두 개념이 통째로 들어와 있다. 하나씩 짚어보자.

**`pluginManagement { }` 블록.** Maven의 `<pluginManagement>`에 정확히 대응한다. Maven에서는 부모 pom의 `<pluginManagement>`에 플러그인 버전을 박아두면, 자식 pom들이 버전 없이 플러그인 id만으로 참조했다. Gradle도 같은 발상이다. **플러그인을 어디서 찾을지(`repositories`), 그리고 버전을 어디서 관리할지를 한 곳에 모은다.** 멀티 모듈 빌드가 되면 진가가 드러난다. `app`, `domain`, `payment` 세 모듈의 `build.gradle.kts`에 각각 `id("org.springframework.boot") version "4.0.6"`을 박을 필요 없이, settings의 `pluginManagement`에 버전을 한 번 박고 각 모듈은 `id("org.springframework.boot")`만 적으면 된다. 단일 출처의 원칙이다.

지금 우리 빌드는 단일 모듈이라 그 효과를 직접 느끼긴 어렵다. 그래도 처음부터 `pluginManagement` 골격을 가지고 가는 게 좋다. 멀티 모듈로 옮기는 8장에서 이 골격 그대로 재사용된다.

**`dependencyResolutionManagement { }` 블록.** 이건 9.x에서 자리가 굳어진 신문법이다. Maven에서는 각 pom마다 `<repositories>`를 자유롭게 선언할 수 있었다. 부모 pom에 mavenCentral을 박아도, 자식 pom이 자기만의 private repo를 추가할 수 있었다. 편리해 보이지만, 멀티 모듈 회사 프로젝트가 되면 끔찍한 일이 된다 — 누군가 자기 모듈에 사내 Nexus가 아닌 임의의 외부 repo를 추가해버리면, 우리 빌드의 의존성 출처가 한순간 통제 불가가 된다. 보안팀이 잠을 못 자는 이유다.

Gradle 9.5의 표준은 이걸 settings 한 곳에서만 선언하라고 강제할 수 있게 했다. `repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS` 한 줄이 그 강제 장치다. 이 줄을 박아두면, 어떤 하위 프로젝트의 `build.gradle.kts`에서든 `repositories { }` 블록을 추가하는 순간 빌드가 빨간 메시지를 뱉으며 멈춘다. "이 빌드의 repo는 settings에서만 선언할 수 있습니다"라고. 처음 만나면 짜증이 날 수도 있다. 그런데 이 강제가 멀티 모듈 빌드의 안전망이다. 회사 표준 repo만 쓰게 만들고 싶다면, 이 한 줄로 끝난다.

**`foojay-resolver-convention` 플러그인.** 이건 Maven에는 정확히 대응하는 게 없다. Toolchain 자동 다운로드를 담당하는 settings 수준 플러그인이다. 자세한 건 잠시 후 박스에서 한 번에 정리한다.

**`rootProject.name`.** 별것 아닌 줄 하나지만 의미가 있다. 폴더 이름을 그대로 쓰지 않고 명시하면, 이 프로젝트가 IDE 모듈명·publish 좌표·build scan에서 일관되게 `shop`으로 보인다. 폴더 이름이 `shop-gradle-journey-ch04-bootapp` 같은 길고 너저분한 이름이어도, 빌드 식별자는 깔끔하게 `shop`이다. 처음부터 박아두자.

> **wrapper distribution-type — 첫 빌드 전에 한 줄**
>
> 1장 박스에서 한 번 짚었지만, `ch04-bootapp/`에서 본격적으로 빌드를 돌리기 전에 다시 확인하자. `gradle/wrapper/gradle-wrapper.properties`의 `distributionUrl`이 `gradle-9.5-bin.zip`으로 끝나는가, `gradle-9.5-all.zip`으로 끝나는가? 후자라면 200MB가 넘는 소스 포함 배포본을 받는다. 첫 빌드가 한참 길어지고, CI runner들이 매번 그걸 캐시한다. 처방은 한 줄이다.
>
> ```bash
> ./gradlew wrapper --gradle-version 9.5 --distribution-type=bin
> ```
>
> `bin`은 실행 바이너리만 받는다. IDE에서 소스 점프가 어차피 필요하면 IntelliJ가 알아서 GitHub에서 가져온다. `all`을 받는 시대는 끝났다. 잊지 말자.

> **Toolchain의 자리**
>
> `build.gradle.kts`의 `java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }` 한 블록과, 위 settings의 `id("org.gradle.toolchains.foojay-resolver-convention")` 한 줄이 짝을 이룬다. 이 두 줄을 4장에서 미리 박고 가야 하는 이유가 있다.
>
> Gradle의 Toolchain은 Maven에서는 잘 안 쓰던 개념이다. 핵심은 한 문장이다 — **Daemon JVM ≠ Build JVM.** Gradle Daemon 자체는 자기가 깔린 JDK 위에서 돈다 (9.x는 17+ 요구). 그런데 우리가 컴파일하고 테스트할 대상 JDK는 별개로 고를 수 있다. 같은 머신에서 JDK 17과 JDK 21이 깔려 있어도, build script가 "이 빌드는 21로 컴파일한다"고 선언하면 Gradle이 21을 골라 그걸로 컴파일한다. 21이 머신에 없으면? `foojay-resolver-convention`이 자동으로 Adoptium에서 받아온다. CI runner마다 JDK 버전이 들쭉날쭉해도 빌드 결과가 같다는 게 이 메커니즘의 약속이다.
>
> 왜 4장부터 박는가? 단일 모듈에서 Toolchain을 잡아두지 않고 멀티 모듈로 넘어가면, 모듈마다 JDK 버전이 미묘하게 다른 상태가 생긴다. 한 번 그렇게 되면 풀기 번거롭다. 처음부터 settings에 foojay를, build에 toolchain을 박아두는 편이 낫다. 회사에서 어떤 JDK가 깔린 머신을 받든, 우리 빌드는 21로 컴파일된다 — 이게 약속할 수 있는 상태다.

## build.gradle.kts — 한 줄씩 읽어보자

settings는 입구였다. 이제 본문이다. `ch04-bootapp/build.gradle.kts` 전체를 펼쳐놓고 한 줄씩 읽어보자.

```kotlin
// build.gradle.kts
plugins {
    id("org.springframework.boot") version "4.0.6"
    id("io.spring.dependency-management") version "1.1.6"
    kotlin("jvm") version "2.2.0"
    kotlin("plugin.spring") version "2.2.0"
}

group = "com.example"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.jetbrains.kotlin:kotlin-reflect")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5")
}

tasks.test {
    useJUnitPlatform()
}
```

30줄이 안 된다. Maven `pom.xml`로 같은 일을 하려면 70~100줄짜리 XML이 필요하다. 줄 수가 짧다고 더 좋은 건 아니다 — 다만 이 짧음의 정체가 뭔지를 정확히 보자.

### plugins 블록

```kotlin
plugins {
    id("org.springframework.boot") version "4.0.6"
    id("io.spring.dependency-management") version "1.1.6"
    kotlin("jvm") version "2.2.0"
    kotlin("plugin.spring") version "2.2.0"
}
```

Maven의 `<build><plugins>`와 같은 위치다. 그런데 동작 방식이 사뭇 다르다. Maven 플러그인은 phase에 goal을 묶는 방식이고, Gradle 플러그인은 **빌드 객체에 task와 configuration을 주입하는 방식**이다. 예를 들어 `org.springframework.boot` 플러그인을 적용하는 순간, 우리 빌드에는 `bootJar`, `bootRun`, `bootBuildImage`, `bootTestRun` 같은 task들이 새로 등록되고, `developmentOnly`, `productionRuntimeClasspath` 같은 configuration이 추가된다. 6장에서 이 안을 깊게 들여다본다.

여기서 미리 한 가지 안내 박스를 받자.

> **`id("io.spring.dependency-management")` 한 줄에 대해서**
>
> 이 플러그인은 Maven의 `<dependencyManagement>`를 Gradle에서 흉내내주는 보조 도구다. Maven에서 옮겨온 사람이 BOM을 가장 익숙하게 쓸 수 있도록 만들어졌다. 다만 Gradle 9.5 기준의 본격적인 권장은 이 플러그인 없이 `dependencies` 블록에서 `implementation(platform(...))`을 직접 쓰는 길이다 — 더 빠르고, Configuration Cache 친화적이다. 두 길의 선택은 5장에서 깊게 다룬다. 이 장에서는 일단 Spring Initializr가 만들어준 그대로 두고 간다. 두 길의 분기점은 5장이 알려준다.

`plugins { }` 블록의 또 한 가지 특징은, **블록 안에서 적용된 플러그인이 그 다음 줄들에서 type-safe accessor로 노출된다**는 점이다. 즉 `plugins { id("org.springframework.boot") ... }` 다음에 나오는 코드에서는 `tasks.named<BootJar>("bootJar") { ... }` 같은 타입 안전한 호출이 컴파일 타임에 잡힌다. 만약 우리가 `apply(plugin = "org.springframework.boot")` 같은 옛 방식으로 플러그인을 적용하면 accessor가 안 생긴다. 이게 Kotlin DSL에서 `plugins { }` 블록을 표준으로 쓰는 이유다.

### group / version / java

```kotlin
group = "com.example"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

Maven의 `<groupId>`, `<artifactId>`, `<version>`이 여기로 왔다. `artifactId`는 어디 갔지? `settings.gradle.kts`의 `rootProject.name`이 그 자리다. 빌드 산출물의 좌표가 `com.example:shop:0.0.1-SNAPSHOT`이 되는 셈이다.

`java { toolchain { } }` 블록이 박혀 있다. 앞서 박스에서 설명한 그 자리다. Maven에서는 보통 `<properties><java.version>21</java.version></properties>`로 했던 일이, Gradle에서는 toolchain의 `languageVersion`이다. 차이는 단지 표기법이 아니다 — Maven의 `java.version`은 "이 JDK로 컴파일하라"는 단순 지시였지만, Gradle의 `languageVersion`은 "이 JDK가 없으면 받아와서라도 그걸로 컴파일하라"는 보장이다. CI runner의 JDK가 17이어도 우리 빌드는 21로 컴파일된다.

`vendor`는 일부러 박지 않았다. Adoptium을 기본으로 받게 되지만, 회사가 Corretto나 Zulu를 표준으로 쓴다면 `vendor = JvmVendorSpec.AMAZON` 같은 한 줄을 추가하면 된다. 작은 디테일이지만 회사 표준화 정책과 맞물리는 부분이다.

### dependencies

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.jetbrains.kotlin:kotlin-reflect")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5")
}
```

Maven `<dependencies>`의 자리다. 한눈에 두 가지 차이가 들어온다.

**첫째, scope의 이름이 다르다.** Maven의 `<scope>compile</scope>`은 Gradle에서 `implementation`이다. `<scope>test</scope>`는 `testImplementation`이다. 단순한 이름 변경이 아니라 의미가 살짝 다르다. Maven의 `compile` scope는 transitive하게 소비자에게도 노출되는 반면, Gradle의 `implementation`은 **소비자에게 노출되지 않는다**. 즉 `app`이 `domain` 모듈을 의존하고 `domain`이 `lib-foo`를 `implementation`으로 의존한다면, `app`은 `lib-foo`의 클래스에 컴파일 타임에 접근할 수 없다. 이게 캡슐화의 강제다. ABI가 변해도 transitive 재컴파일이 폭발하지 않는다. 5장에서 이 의미론을 다시 본다.

**둘째, 버전이 없다.** `implementation("org.springframework.boot:spring-boot-starter-web")` 줄에는 콜론 두 개로 끝나는 좌표만 있을 뿐, `:4.0.6` 같은 버전이 없다. 어디서 오는가? `io.spring.dependency-management` 플러그인이 Spring Boot BOM을 자동으로 적용해, 모든 Spring 관련 의존성의 버전을 BOM에서 가져온다. Maven `spring-boot-starter-parent`를 부모로 두면 같은 일이 일어났다 — 그래서 Maven 출신이 가장 빨리 적응하는 부분이다. 5장에서 이 BOM 적용을 plugin 없이 `implementation(platform(...))`으로 직접 하는 더 권장되는 길을 만난다.

### tasks.test useJUnitPlatform()

```kotlin
tasks.test {
    useJUnitPlatform()
}
```

Maven에서는 `<plugin><groupId>org.apache.maven.plugins</groupId><artifactId>maven-surefire-plugin</artifactId>...`로 XML 10여 줄을 써야 했던 일이 Kotlin DSL에서는 두 줄이다. `test` task는 `java` plugin이 만들어주는 표준 task이고, 그 task의 설정 한 줄 — "JUnit 5(Jupiter)를 쓰겠다" — 이 끝이다.

여기서 `tasks.test { }`는 Kotlin DSL의 type-safe accessor 형태다. 내부적으로는 `tasks.named<Test>("test") { ... }`와 같다. accessor가 type을 알기 때문에 `useJUnitPlatform()`이 IDE 자동완성에서 바로 뜬다. 만약 `apply(plugin = "java")` 같은 옛 방식으로 적용했다면 accessor가 안 생겨 `configure<Test>("test") { ... }` 같은 fallback을 써야 한다. `plugins { }` 블록을 표준으로 쓰는 이유가 여기서도 작은 편안함으로 돌아온다.

7장에서 이 `tasks.test` 한 블록을 본격적으로 펼친다 — 통합 테스트를 어떻게 별도 suite로 분리하는지. 일단 4장에서는 이 두 줄로 충분하다.

## Maven 개념 매핑 상세

이제 settings와 build를 다 읽었으니, 표 매핑의 큰 항목들을 본문에서 한 번씩 만나본다. 일부는 위에서 이미 본 것이고, 일부는 이 자리에서 새로 만나는 것이다. 짧게 끊어 가자.

### dependencyManagement → platform() BOM

Maven의 `<dependencyManagement>`는 두 가지 일을 했다. 첫째, transitive 의존성의 버전을 정렬한다. 둘째, `<dependencies>`에서 버전 없이 좌표만 적어도 되게 한다. Spring Boot 프로젝트에서 `spring-boot-starter-parent`를 부모로 두면 이 두 일이 자동으로 됐다.

Gradle에서 이 일을 하는 가장 권장되는 방식은 한 줄이다.

```kotlin
dependencies {
    implementation(platform("org.springframework.boot:spring-boot-dependencies:4.0.6"))
    implementation("org.springframework.boot:spring-boot-starter-web")  // 버전 없음
}
```

`platform(...)`은 Gradle 네이티브 BOM 적용 API다. 이 한 줄로 transitive 버전이 BOM 기준으로 정렬되고, 같은 BOM이 다스리는 의존성들은 `dependencies`에서 버전을 생략할 수 있다. 별도 플러그인이 필요 없고, Configuration Cache 친화적이고, IDE 추적이 잘 된다.

지금 `ch04-bootapp/`은 `io.spring.dependency-management` 플러그인 길로 가고 있다. 둘 다 통한다. 다만 9.5 기준의 권장은 `platform()` 길이다. 두 길의 분기 — 언제 어느 쪽을 고르는가 — 는 5장에서 깊게 다룬다.

### parent pom → Convention Plugin

Maven에서 가장 흔한 패턴이 `<parent>`에 회사 표준 pom을 두고, 거기서 모든 회사 표준 — Java 버전, 인코딩, JUnit 버전, Surefire 설정 — 을 상속받는 것이다. 멀티 모듈에서는 각 자식이 또 부모를 상속한다. 우아한 계층이었다.

Gradle에는 `<parent>`가 없다. 대신 **Convention Plugin**이 있다. 발상 자체가 다르다 — 상속이 아니라 **재사용 가능한 빌드 로직의 모듈화**다. `buildSrc/src/main/kotlin/shop.spring-boot-conventions.gradle.kts` 같은 파일에 회사 표준 설정을 한 번 짜두면, 각 모듈의 `build.gradle.kts`에서 `plugins { id("shop.spring-boot-conventions") }` 한 줄로 그걸 다 받는다. parent pom과 표면적 효과는 비슷한데, 동작 모델이 다르다 — 상속이 아니라 plugin 적용이다.

지금 단일 모듈에서는 Convention Plugin이 필요 없다. 8장에서 멀티 모듈로 넘어가고, 10장에서 본격적으로 Convention Plugin을 짠다. 이 장에서는 "parent pom의 자리는 Convention Plugin이다"라는 매핑만 머리에 박아두자. 그 시점이 오면 더 깊게 본다.

### profile → variant + property

Maven `<profile>`은 환경별 설정 분리의 도구였다. `mvn -P dev` / `mvn -P prod`로 활성화하면 `<dependencies>`, `<properties>`, `<plugins>`까지 다르게 적용됐다.

Gradle에는 `<profile>`이라는 통합 메커니즘이 없다. 대신 작은 도구들이 흩어져 있고, 그 조합으로 같은 일을 한다. 두 가지가 핵심이다.

**Project property**. 빌드 명령에 `-P` 옵션으로 키-값을 넘긴다.

```bash
./gradlew bootRun -Penv=dev
```

빌드 스크립트에서는 이렇게 받는다.

```kotlin
val env = (project.findProperty("env") as String?) ?: "local"
```

이 값으로 `dependencies` 블록을 분기하거나, `bootRun`의 인자를 다르게 줄 수 있다. Maven의 `<activeProfile>`보다 자유롭고, 변수 조합이 폭증하지 않는다.

**`bootRun --args`**. Spring Boot 앱을 실행하면서 런타임 인자를 넘기는 표준 방법이다.

```bash
./gradlew bootRun --args='--spring.profiles.active=dev --server.port=8081'
```

Spring Boot 자체의 `spring.profiles.active`는 그대로 살아 있다. Maven에서 자주 `<profile>`로 했던 "환경별 application.yml 선택"은 Spring Boot의 profile이 더 자연스럽게 해준다 — 빌드 도구의 profile이 아니라, **앱의 profile**이다. 빌드 시점이 아니라 실행 시점에 정해진다. 빌드는 한 번, 실행은 환경마다. 이게 더 깔끔한 분리다.

Maven `<profile>`이 했던 일들의 80%는 Spring Boot의 profile + Project property + `bootRun --args` 조합으로 풀린다. 나머지 20%는 12장에서 다루는 커스텀 plugin 패턴까지 가야 풀리는 경우다. 일단 4장에서는 매핑만 기억하자.

### plugin management → settings.gradle.kts

위에서 이미 만난 것이다. Maven `<pluginManagement>`는 Gradle에서 `settings.gradle.kts`의 `pluginManagement { }` 블록이다. 차이가 하나 있다 — Maven은 **부모 pom에 두는 게 관행**이었지만, Gradle은 **settings에 두는 게 표준**이다. 설계상의 위계가 다르다. settings는 "이 빌드의 입구"라는 명확한 책임이 있고, 거기 plugin 버전을 박는 것이 명시적으로 맞다.

### repositories → dependencyResolutionManagement

이것도 위에서 만났다. 다시 짚자면, Maven은 각 pom이 자유롭게 `<repositories>`를 추가할 수 있었고, Gradle 9.5는 **모든 repo는 settings의 `dependencyResolutionManagement { repositories { } }`에 한 번만**이라는 표준을 강제할 수 있다. `RepositoriesMode.FAIL_ON_PROJECT_REPOS` 한 줄이 그 강제 장치다.

처음에는 강제가 답답하게 느껴진다. 어떤 모듈만 임시로 다른 repo를 쓰고 싶을 때가 있지 않은가. 그런데 그게 가능하다는 게 보안팀의 악몽이다. 회사 표준 외의 repo가 우리 빌드에 끼어드는 순간, 의존성의 출처를 신뢰할 수 없게 된다. 16장에서 의존성 보안을 본격적으로 다룰 때, 이 settings 강제가 첫 번째 안전망임이 다시 드러난다.

특수한 경우 — 예를 들어 사내 Nexus가 있고, 그것이 mavenCentral의 mirror라면 — 그건 settings에 같이 박으면 된다. 모듈마다 분기시킬 일이 거의 없다는 게 핵심이다.

### mvn → ./gradlew

가장 표면적인 매핑이자, 가장 깊은 매핑이다.

표면적으로는 한 단어 바꿈이다. `mvn clean install`이 `./gradlew clean build`다. `mvn test`가 `./gradlew test`다. `mvn package`가 `./gradlew assemble` 또는 `./gradlew bootJar`다.

그런데 `./gradlew`의 앞부분 `./`이 의미가 있다. **Maven의 `mvn`은 시스템에 설치된 Maven을 부르는 명령**이다. CI runner와 내 노트북에 깔린 Maven 버전이 다르면, 빌드 결과가 달라질 수 있다. 회사 표준 Maven 버전을 관리하려면 모두에게 같은 버전을 깔게 해야 한다.

**Gradle의 `./gradlew`는 프로젝트 안에 박힌 wrapper를 부르는 명령**이다. 프로젝트 루트의 `gradlew` 셸 스크립트와 `gradle/wrapper/gradle-wrapper.properties`가 짝이 된다. properties에 `distributionUrl=https\://services.gradle.org/distributions/gradle-9.5-bin.zip`이 박혀 있으면, `./gradlew`를 처음 실행할 때 그 버전을 받아 캐시하고, 이후 모든 빌드가 그 버전으로 돈다. 내 노트북에 깔린 Gradle이 어떤 버전이든 상관없다 — 우리 프로젝트의 빌드는 wrapper에 박힌 9.5로 돈다.

이게 단순 편의가 아니다. **wrapper가 곧 우리 빌드의 Gradle 버전 명세다.** 회사 빌드의 Gradle 버전을 올리는 일은 `./gradlew wrapper --gradle-version 9.5.1 --distribution-type=bin` 한 줄과 그것의 git commit이다. 모든 사람이 다음 빌드부터 9.5.1로 돈다. CI runner에 별도 설치를 강제할 필요가 없다. Maven 시절을 떠올리면 이게 작은 평화가 아니다.

> **함정 — phase 모델과 task graph의 차이**
>
> 같은 단어가 다른 의미를 갖는다는 게 가장 찜찜한 일이다. `clean`을 보자.
>
> Maven에서 `mvn clean`은 **phase**다. `clean` phase에 묶인 모든 goal이 순서대로 실행된다. `clean` phase 다음에 `compile`, `test`, `package`, `install`로 이어지는 정해진 lifecycle이 있고, 우리는 그 lifecycle을 따라간다. `mvn clean install`은 "clean phase부터 install phase까지 다 돌려라"는 뜻이다. 순서가 정해져 있다.
>
> Gradle에서 `./gradlew clean`은 **task**다. `clean`은 `java` plugin이 만들어준 task 하나일 뿐이고, 정해진 다음 task가 없다. `./gradlew clean build`라고 쓰면, Gradle은 "clean task와 build task를 둘 다 실행할 그래프를 짜라"고 받아들인다. 두 task의 의존 관계를 보고 순서를 정한다 — `clean`이 `build`보다 먼저 와야 한다는 의존이 없다면, 병렬로 돌릴 수도 있다. (실무에서는 보통 `clean`을 명령행 첫 인자로 쓰면 먼저 도는 게 자연스럽지만, 이건 관행이지 강제가 아니다.)
>
> 차이가 어디서 드러나느냐. 한 번은 이런 일이 있다. Maven에서 `mvn clean test`를 쓰던 사람이 `./gradlew clean test`라고 쓰면 같이 돌 거라 기대한다. Gradle은 두 task의 의존 그래프를 짜는데, `test`는 `compileJava`, `processResources`, `compileTestJava`에 의존하지만 `clean`에는 의존하지 않는다. 그래서 사람이 보기엔 같은 의도였는데 task 그래프가 미묘하게 다른 순서로 평가되는 경우가 생긴다.
>
> 일반적으로는 `./gradlew clean build`처럼 명령 순서로 쓰는 패턴이면 큰 사고가 안 난다. 다만 머릿속의 모델은 이렇게 바꿔두자 — **Maven은 정해진 phase의 행렬, Gradle은 task의 그래프**. 같은 단어를 봐도 다른 메커니즘이 돈다는 걸 기억해두자.

> **마이그레이션 노트 — `gradle init --type pom`의 한계**
>
> Gradle에는 기존 Maven 프로젝트를 Gradle로 변환해주는 명령이 있다. `gradle init --type pom`이다. `pom.xml`이 있는 폴더에서 실행하면 그걸 읽어 `build.gradle.kts`(또는 Groovy)를 생성해준다. 처음 만나면 "이 한 줄로 끝나는가" 싶은데, 사실은 그렇게 단순하지 않다.
>
> 이 명령은 의존성 목록, repository, 기본 plugin은 잘 옮겨준다. 그러나 다음은 잘 못 옮긴다 — `<profile>` 분기, 회사 표준 parent pom의 상속 내용, `<pluginManagement>`의 세부 설정, Spring Boot Maven plugin의 다양한 옵션, Surefire의 디테일한 설정. 한마디로 **거시 골격은 옮겨주지만, 미시 결정들은 옮겨주지 않는다**.
>
> 실용적인 사용법은 이렇다. `gradle init --type pom`을 일단 돌려본다. 산출물을 그대로 쓰겠다는 게 아니라, 우리 `pom.xml`이 Gradle 사고로 어떻게 번역되는지 한 번 보겠다는 것이다. 그 다음에는 그걸 참고용으로 두고, 우리 프로젝트의 `build.gradle.kts`를 새로 짠다. 본 장에서 한 줄씩 읽어본 `ch04-bootapp/build.gradle.kts`처럼 깔끔한 것을 직접 짜는 편이 낫다. 자동 변환에 기대면 옛 Maven 사고가 그대로 Gradle 스크립트에 묻어들어와, 결국 두 번 짤 일이 생긴다.

## 4장을 닫으며

여기까지 왔다면, Maven 출신 독자의 머릿속 어딘가에 작은 안도감이 생겼을 것이다. dependencyManagement는 platform/BOM으로 갔다. parent pom은 Convention Plugin이라는 다른 모델로 옮겨갔다. profile은 흩어져 있지만 그 조각들의 자리는 분명하다. pluginManagement와 repositories는 settings에 모였다. mvn은 ./gradlew다. clean과 test 같은 단어는 같은 단어인데 다른 메커니즘으로 돈다.

그리고 `ch04-bootapp/`에 동작하는 단일 모듈 Spring Boot 앱이 한 채 서 있다. 30줄이 안 되는 `build.gradle.kts`에 Toolchain까지 박혀 있고, 13줄짜리 `settings.gradle.kts`가 입구를 맡고 있다. 이 앱이 5장부터 18장까지 자라난다.

자라남의 첫 걸음이 5장이다. 4장에서는 의존성을 Spring Initializr가 만들어준 그대로 두고 왔다 — `io.spring.dependency-management` 플러그인 길과 BOM의 미묘한 자리를 그대로 두고 왔다. 5장에서 이 자리를 정리한다. **BOM은 resolution을 다스리고, Version Catalog는 declaration을 다스린다. 둘은 직교한다 — 그래서 둘 다 쓴다.** 한 줄로 적으면 짧지만, 그 뒤에 깔린 의존성 그래프의 사고를 자기 것으로 만드는 게 5장의 일이다. `gradle/libs.versions.toml`이라는 단일 출처 파일을 도입하고, `platform(libs.spring.boot.bom)`이라는 한 줄로 Spring Boot의 모든 transitive를 정렬한다. `implementation`과 `api`의 차이를 짚고, `dependencyInsight`로 의존성 그래프를 디버깅하는 도구를 우리 손에 쥔다.

지금 우리 앱은 한 단계 더 자라날 준비가 되어 있다. 다음 장으로 넘어가자.
