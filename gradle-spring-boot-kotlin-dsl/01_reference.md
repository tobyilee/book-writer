# Gradle 9.5 × Spring Boot (Kotlin DSL) 레퍼런스

> 본 문서는 책 저술의 1차 자료다. 모든 인용은 1차 자료(Gradle User Guide / Spring Boot Gradle Plugin Reference / 공식 Release Notes)의 섹션 ID로 회수 가능하도록 표기한다.

---

## 1. 개요 — 정확성 기준

- **Gradle:** 9.5 (2026-05 시점 current). 9.0에서 메이저 점프, 9.x 라인은 minor.
- **Spring Boot:** 4.0.x stable (3.5.x도 유지보수). 둘 다 Gradle 8.14+/9.x 요구.
- **Kotlin DSL 기본.** Groovy DSL은 차이가 있을 때만 짧게 병기.
- **JDK:** Gradle 9.x **데몬은 JDK 17+ 필수** (toolchain으로 빌드 대상 JDK는 별도 지정 가능).
- **Kotlin Gradle Plugin:** 9.x는 KGP 2.0.0+ 필수.

[Gradle 9.0 Release Notes](https://docs.gradle.org/9.0.0/release-notes.html), [Spring Boot Gradle Plugin Reference §1](https://docs.spring.io/spring-boot/gradle-plugin/index.html), [Gradle Upgrading to 9.0](https://docs.gradle.org/current/userguide/upgrading_major_version_9.html)

---

## 2. Gradle 핵심 모델

Gradle 실행을 이해하려면 다음 객체들의 책임 분리를 명확히 잡아야 한다.

### 2.1 Project / Settings / Build / Gradle

- **Settings (`settings.gradle.kts`)** — 빌드에 어떤 프로젝트들이 포함되는지 결정. `rootProject.name`, `include(...)`, `includeBuild(...)`, `pluginManagement {}`, `dependencyResolutionManagement {}`이 여기 산다. Gradle 9.0부터 일부 신규 plugin은 settings 수준에서만 적용 가능. (User Guide §multi_project_builds)
- **Project (`build.gradle.kts`)** — 하나의 빌드 단위. `tasks`, `dependencies`, `configurations`, `extensions`를 갖는다. **단일 프로젝트**라도 root project가 늘 하나 존재.
- **Build / Gradle 객체** — 빌드 전체 lifecycle 훅 (`gradle.beforeProject {}`, `gradle.taskGraph.whenReady {}`) 제공.

### 2.2 Lifecycle (3-phase)

1. **Initialization** — settings를 평가하고 어떤 프로젝트들이 참여할지 결정.
2. **Configuration** — 모든 참여 프로젝트의 build script를 평가해 task graph를 만든다. **이 단계의 산출물이 Configuration Cache 대상**이다.
3. **Execution** — 요청된 task 그래프를 순차/병렬 실행.

(User Guide §build_lifecycle)

### 2.3 Task

Task는 단위 작업의 추상화. **lazy registration (`tasks.register`)이 정석**, eager `tasks.create`는 피한다 — Configuration Cache 친화성과 시작 속도 모두를 위해. (User Guide §incremental_build, §lazy_configuration)

```kotlin
tasks.register("hello") {
    doLast { println("Hello") }
}
```

### 2.4 Plugin

Plugin은 빌드에 task·configuration·convention을 주입하는 단위. 세 종류:
- **Binary plugin** — JVM 클래스로 컴파일된 `Plugin<Project>` 구현체.
- **Script plugin** — 다른 `.gradle.kts`를 `apply(from = ...)` 으로 끌어오기. **legacy, 피해야 함.**
- **Precompiled script plugin (convention plugin)** — `buildSrc` 또는 `build-logic`에 두는 `*.gradle.kts` 파일. 자동으로 binary plugin으로 컴파일된다. **현행 권장 방식.** (User Guide §implementing_gradle_plugins_precompiled)

### 2.5 Configuration

**Configuration = 의존성 버킷.** Gradle은 한 가지 단어 "configuration"을 세 가지 역할로 쓰는데, 9.x에서 명시적으로 분리됐다:

| 역할 | `canBeDeclared` | `canBeResolved` | `canBeConsumed` | 대표 예 |
|------|------|------|------|---------|
| **Dependency scope (declarable)** | true | false | false | `implementation`, `api`, `compileOnly` |
| **Resolvable** | false | true | false | `compileClasspath`, `runtimeClasspath` |
| **Consumable** | false | false | true | `apiElements`, `runtimeElements` |

핵심: **사용자가 직접 다루는 건 거의 declarable**. classpath 같은 resolvable은 plugin이 만들어준다. (User Guide §declaring_configurations#dependency-scope-configurations, §declaring_configurations#configuration-roles)

---

## 3. Kotlin DSL

### 3.1 왜 Kotlin DSL인가

- **타입 안전성**: 잘못된 호출은 컴파일 타임에 잡힌다.
- **IDE 지원**: IntelliJ에서 자동완성/소스 점프/리팩토링이 일관되게 동작.
- **단점**: 첫 빌드가 Groovy DSL보다 느릴 수 있다 (Kotlin 컴파일 오버헤드). 캐싱 후에는 차이가 무의미.

(User Guide §kotlin_dsl)

### 3.2 문법 함정

- **문자열은 반드시 큰따옴표**. 작은따옴표는 Kotlin에서 `Char` 리터럴이다.
- **lazy property 할당은 `=`를 권장**. Gradle 8.2+부터 `.set()` 대신 `=` 연산자 사용 가능:
  ```kotlin
  // 권장
  archiveClassifier = "boot"
  // 호환 가능 (legacy)
  archiveClassifier.set("boot")
  ```
- **type-safe accessor는 `plugins {}` 블록 이후에만 노출**된다. `apply(plugin = "...")`로 적용된 플러그인은 accessor가 안 생긴다 — 이 경우 `configure<T> {}` 또는 string 기반 접근으로 fallback.
- **eager get 피하기**: `tasks.named<Test>("test") { ... }`가 정석. `tasks.getByName("test")`는 즉시 realize되어 성능 저하.

### 3.3 Groovy → Kotlin 마이그레이션 1:1

| Groovy | Kotlin DSL |
|---|---|
| `apply plugin: 'java'` | `plugins { java }` (또는 `id("java")`) |
| `implementation 'org.springframework.boot:spring-boot-starter-web'` | `implementation("org.springframework.boot:spring-boot-starter-web")` |
| `bootJar { mainClass = 'X' }` | `tasks.named<BootJar>("bootJar") { mainClass = "X" }` |
| `ext.springBootVersion = '4.0.6'` | `extra["springBootVersion"] = "4.0.6"` (또는 **version catalog**) |
| `subprojects { ... }` | **피하라** (§5 참고) |

### 3.4 9.5 Kotlin DSL 신규

Gradle 9.5는 **precompiled Settings plugin (`*.settings.gradle.kts`)에 대해서도 타입-안전 accessor를 생성**한다. 이전엔 settings 수준 convention plugin을 쓸 때 string-based API로 떨어졌지만, 이제 project plugin과 동일한 경험. ([Gradle 9.5 Release Notes](https://docs.gradle.org/current/release-notes.html))

---

## 4. 의존성 관리 deep-dive

### 4.1 declarable configuration 의미론

- **`implementation`** — 컴파일·런타임 둘 다 필요. 소비자(consumer)에게 노출 안 됨 → 캡슐화. **기본 선택.**
- **`api`** — `java-library` 플러그인에서만 노출. 소비자에게도 컴파일 타임에 노출. **API 표면에 등장하는 타입에만 사용.** 남용 시 abi 변경마다 transitive 재컴파일 폭발.
- **`compileOnly`** — 컴파일에만. 런타임 classpath/jar에 미포함. annotation processor 호출 인터페이스, Lombok, servlet-api(컨테이너 제공) 등.
- **`runtimeOnly`** — 런타임만. JDBC 드라이버처럼 인터페이스 의존이 없는 구현체.
- **`annotationProcessor`** — compile 시에만 동작하는 processor. compile/runtime classpath에서 분리. (e.g. `spring-boot-configuration-processor`)
- **Spring Boot 플러그인이 추가로 만들어주는 것:**
  - `developmentOnly` — 실행 가능한 jar/war에서 제외. (e.g. `spring-boot-devtools`)
  - `testAndDevelopmentOnly` — 테스트와 dev에서만.
  - `productionRuntimeClasspath` — dev/test 제외한 런타임 classpath. (Spring Boot Gradle Plugin §reacting:java)

### 4.2 BOM 통합: 두 가지 길

**(A) Gradle 네이티브 platform()** — **권장**. 별도 플러그인 필요 없음, Configuration Cache 친화적.

```kotlin
import org.springframework.boot.gradle.plugin.SpringBootPlugin

dependencies {
    implementation(platform(SpringBootPlugin.BOM_COORDINATES))
    implementation("org.springframework.boot:spring-boot-starter-web")
}
```

`enforcedPlatform()` 변형은 모든 충돌을 BOM 버전으로 강제(권장 X — Gradle의 conflict resolution을 무력화).

**(B) `io.spring.dependency-management` 플러그인** — Maven `dependencyManagement` 흉내. Property 기반 버전 오버라이드(`extra["slf4j.version"] = "..."`)가 가능하다는 게 유일한 장점. 공식 문서가 **"likely result in faster builds"**라며 (A)를 권장. (Spring Boot Gradle Plugin §managing-dependencies)

### 4.3 Version Catalog (`gradle/libs.versions.toml`)

**`gradle/libs.versions.toml`**이 단일 출처가 된다. Dependabot도 이 파일을 읽는다.

```toml
[versions]
spring-boot = "4.0.6"
kotlin = "2.2.0"
junit = "5.11.4"

[libraries]
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web", version.ref = "spring-boot" }
spring-boot-starter-data-jpa = { module = "org.springframework.boot:spring-boot-starter-data-jpa", version.ref = "spring-boot" }
spring-boot-bom = { module = "org.springframework.boot:spring-boot-dependencies", version.ref = "spring-boot" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }

[bundles]
spring-web = ["spring-boot-starter-web", "spring-boot-starter-data-jpa"]

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }
```

```kotlin
// build.gradle.kts
plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.spring.boot)
}

dependencies {
    implementation(platform(libs.spring.boot.bom))
    implementation(libs.bundles.spring.web)
    testImplementation(libs.junit.jupiter)
}
```

**catalog vs BOM:**
- Catalog는 **빌드 스크립트의 declaration을 단축**한다 (빌드 타임 only).
- BOM/platform은 **resolution 시점에 transitive 버전을 정렬**한다.
- **둘 다 쓴다.** Catalog가 BOM 좌표를 보관하고, build script에서 `platform(libs.spring.boot.bom)` 으로 적용.

(User Guide §version_catalogs#sec:version-catalog-declaration, §sec:accessing-catalog)

### 4.4 Resolution 제어

- **Dependency lock**: `gradle.lockfile` (configuration별 정확한 버전 고정). `dependencyLocking { lockAllConfigurations() }` + `--write-locks`.
  - 모드: `DEFAULT` / `STRICT` / `LENIENT`. CI에선 `STRICT` 권장.
- **Dependency verification**: `gradle/verification-metadata.xml`. checksum(SHA-256) + 선택적으로 PGP 서명. `--write-verification-metadata sha256,pgp` 로 부트스트랩.
- **Resolution strategy** (transitive 강제):
  ```kotlin
  configurations.all {
      resolutionStrategy.eachDependency {
          if (requested.group == "org.slf4j") useVersion("2.0.13")
      }
  }
  ```

(User Guide §dependency_locking, §dependency_verification, §13)

---

## 5. 멀티 모듈 패턴

### 5.1 settings 구조

```kotlin
// settings.gradle.kts
rootProject.name = "shop"
include("app", "core", "order", "payment")

pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS  // root settings에서만 repo 선언 강제
    repositories {
        mavenCentral()
    }
}
```

(User Guide §multi_project_builds#sec:adding_subprojects)

### 5.2 `subprojects {}` / `allprojects {}` 는 안티패턴

공식 문서가 명시적으로 "configuration-time coupling between projects를 만들고, 로직의 출처를 가린다"며 **cross-project configuration을 피하라**고 한다. 대안은 **convention plugin** (다음 §8). (User Guide §sharing_build_logic_between_subprojects#sec:convention_plugins_vs_cross_configuration)

### 5.3 프로젝트 간 의존

```kotlin
dependencies {
    implementation(project(":core"))
    implementation(project(":order"))
}
```

Spring Boot 환경에서 **library 모듈은 `bootJar`를 사용해선 안 된다**. 다음 §6.4의 함정 참고.

---

## 6. Spring Boot Gradle 플러그인

### 6.1 적용

```kotlin
plugins {
    id("org.springframework.boot") version "4.0.6"
    java
    // 또는: kotlin("jvm") version "2.2.0"
}
```

Spring Boot 4.0.x는 **Gradle 8.14+ 또는 9.x** 요구. Configuration Cache 호환. ([Spring Boot Gradle Plugin Reference](https://docs.spring.io/spring-boot/gradle-plugin/index.html))

### 6.2 `java` plugin이 적용되면 일어나는 일

자동 생성되는 task와 configuration:
- `BootJar` task `bootJar`
- `BootBuildImage` task `bootBuildImage`
- `BootRun` task `bootRun`, `BootTestRun` task `bootTestRun`
- configuration: `bootArchives`, `developmentOnly`, `testAndDevelopmentOnly`, `productionRuntimeClasspath`
- compile 설정: UTF-8 인코딩, `-parameters` 자동 추가

(Spring Boot Gradle Plugin §reacting:java)

### 6.3 `bootJar` 내부

```
my-app.jar
├── META-INF/MANIFEST.MF        # Start-Class, Main-Class=JarLauncher
├── BOOT-INF/
│   ├── classes/                # 앱 클래스/리소스
│   ├── lib/                    # 의존성 jar들
│   └── layers.idx              # 레이어 인덱스 (layered jar 기본 on)
└── org/springframework/boot/loader/  # JarLauncher 클래스 (spring-boot-loader)
```

- **`jar` task와 공존**: `bootJar`는 실행 가능한 fat jar, `jar`는 classifier=`plain`인 일반 library jar. `assemble` → 둘 다.
- **레이어드 JAR (기본 ON)**: `dependencies` / `spring-boot-loader` / `snapshot-dependencies` / `application` 네 레이어. 도커 이미지 최적화의 핵심.
- **main class detection**: main 소스셋에서 `public static void main(String[])`을 갖는 클래스 자동 탐지.

```kotlin
tasks.named<BootJar>("bootJar") {
    archiveClassifier = "boot"
    mainClass = "com.example.ShopApplication"
    layered {
        enabled = true
    }
}

tasks.named<Jar>("jar") {
    enabled = true  // library jar도 함께 발행하고 싶을 때
}
```

(Spring Boot Gradle Plugin §packaging-executable, §packaging-layers)

### 6.4 멀티 모듈 흔한 함정 — library 모듈에서 bootJar 비활성화

`org.springframework.boot` 플러그인을 library 모듈에 적용하면 `bootJar`가 생기고 정작 plain `jar`가 비활성화되어, **다른 모듈에서 `project(":lib")`로 끌어쓸 때 메인 jar가 비어 보이는 사고**가 잦다.

**해결법 1 — library 모듈에는 spring-boot 플러그인을 아예 적용 안 한다** (BOM만 platform으로 들여온다):

```kotlin
// settings.gradle.kts
include("app", "lib-domain")

// app/build.gradle.kts
plugins {
    id("org.springframework.boot")
    java
}

// lib-domain/build.gradle.kts — 플러그인 적용 X
plugins {
    `java-library`
}

dependencies {
    implementation(platform(SpringBootPlugin.BOM_COORDINATES))
    api("org.springframework:spring-context")
}
```

**해결법 2 — 플러그인을 `apply false`로 받고 일부 task만 끄기**:

```kotlin
plugins {
    id("org.springframework.boot") apply false
    `java-library`
}
// bootJar/bootRun 비활성화, jar는 살림
```

(GitHub `spring-projects/spring-boot#16689`, [Gradle discuss 41459](https://discuss.gradle.org/t/understanding-dependencies-in-multi-module-project-with-spring-boot-plugin/41459))

### 6.5 OCI 이미지 — `bootBuildImage`

기본 빌더: **`paketobuildpacks/builder-noble-java-tiny:latest`**. Cloud Native Buildpacks 기반이라 Dockerfile 없이도 OCI 이미지를 만든다.

```kotlin
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

- GraalVM Native Image 플러그인을 함께 적용하면 **native 이미지로 자동 빌드**.
- 빌더가 layered jar의 레이어를 그대로 OCI 레이어로 매핑 → 의존성만 바꿔도 앱 코드 레이어는 캐시 hit.

(Spring Boot Gradle Plugin §packaging-oci-image)

### 6.6 `bootRun`

`BootRun extends JavaExec`. JavaExec에서 쓸 수 있는 모든 옵션이 통한다.

```kotlin
tasks.named<BootRun>("bootRun") {
    jvmArgs("-Dspring.profiles.active=local")
    systemProperty("debug", "true")
    sourceResources(sourceSets["main"])  // static 리소스 라이브 리로드
}
```

```bash
./gradlew bootRun --args='--spring.profiles.active=dev --server.port=9090'
```

(Spring Boot Gradle Plugin §running-your-application)

---

## 7. 테스트 — JVM Test Suite로 통합 테스트 분리

`integrationTest`를 별도 소스셋·task로 분리하는 정석.

```kotlin
plugins {
    `java-library`
    `jvm-test-suite`
    id("org.springframework.boot")
}

testing {
    suites {
        val test by getting(JvmTestSuite::class) {
            useJUnitJupiter("5.11.4")
        }

        register<JvmTestSuite>("integrationTest") {
            useJUnitJupiter("5.11.4")
            dependencies {
                implementation(project())
                implementation("org.springframework.boot:spring-boot-starter-test")
                implementation("org.testcontainers:junit-jupiter")
            }
            targets.all {
                testTask.configure {
                    shouldRunAfter(test)
                }
            }
        }
    }
}

tasks.named("check") {
    dependsOn(testing.suites.named("integrationTest"))
}
```

자동으로 생기는 것들:
- 소스셋: `src/integrationTest/java`, `src/integrationTest/resources`
- 의존성 configuration: `integrationTestImplementation`, `integrationTestRuntimeOnly` …
- task: `compileIntegrationTestJava`, `integrationTest`

(User Guide §jvm_test_suite_plugin#sec:declare_an_additional_test_suite)

---

## 8. Build Logic 모듈화 — buildSrc vs build-logic vs Convention Plugin

### 8.1 한 줄 결론

> **`subprojects {}` 안티패턴 → precompiled convention plugin.**
> 소규모/단일 빌드: `buildSrc` 안에 convention plugin.
> 다수 빌드/대규모: `build-logic` included build.

(User Guide §sharing_build_logic_between_subprojects, §best_practices_structuring_builds)

### 8.2 buildSrc 안의 convention plugin

```
buildSrc/
├── build.gradle.kts
├── settings.gradle.kts
└── src/main/kotlin/
    ├── shop.java-conventions.gradle.kts
    └── shop.spring-boot-conventions.gradle.kts
```

```kotlin
// buildSrc/build.gradle.kts
plugins { `kotlin-dsl` }
repositories { gradlePluginPortal() }
dependencies {
    implementation("org.springframework.boot:spring-boot-gradle-plugin:4.0.6")
}

// buildSrc/src/main/kotlin/shop.java-conventions.gradle.kts
plugins { java }
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
tasks.withType<Test>().configureEach {
    useJUnitPlatform()
}

// buildSrc/src/main/kotlin/shop.spring-boot-conventions.gradle.kts
plugins {
    id("shop.java-conventions")
    id("org.springframework.boot")
}
dependencies {
    "implementation"(platform("org.springframework.boot:spring-boot-dependencies:4.0.6"))
}
```

소비 측:

```kotlin
// app/build.gradle.kts
plugins {
    id("shop.spring-boot-conventions")
}
```

### 8.3 build-logic included build

```kotlin
// settings.gradle.kts
pluginManagement {
    includeBuild("build-logic")
}
```

`build-logic/`은 자체 settings/build를 가진 standalone Gradle build이며 conventionplugin을 발행한다. `buildSrc` 대비 장점:
- **classpath 분리**가 명확. 의존성 충돌 적음.
- buildSrc는 **변경 시 모든 task가 out-of-date**가 되지만, build-logic은 영향 범위가 좁다.
- 여러 root build에서 재사용 가능.

(User Guide §composite_builds#build-logic-pattern, §sharing_build_logic_between_subprojects#sec:sharing_logic_via_composite_build)

### 8.4 어느 시점에 무엇을?

| 상황 | 선택 |
|---|---|
| 단일 root, 모듈 수 < 10 | **buildSrc + convention plugin** |
| 모듈 수 많고 build logic이 빈번히 변경 | **build-logic included build** |
| 회사 단위 표준 빌드 로직 외부 공유 | **별도 plugin 프로젝트 + Gradle Plugin Portal 또는 사내 Maven** |
| 단발성 helper 함수, 매우 단순 로직 | buildSrc의 일반 Kotlin 코드 |

---

## 9. Composite Build

`includeBuild`로 **별개의 Gradle 빌드를 한 트리에 묶는다**. 멀티 프로젝트와 다른 점:
- 멀티 프로젝트의 subproject는 같은 build settings에 등록(`include`).
- Composite의 included build는 **독립적인 build** — 자체 settings.gradle.kts/wrapper를 가진다.

```kotlin
// settings.gradle.kts
includeBuild("../shared-library")
```

라이브러리와 소비자를 동시에 개발하면서 publish 없이 substitution이 자동으로 일어난다. (group:name이 매칭되면 외부 좌표 → 로컬 project로 자동 치환.) 매칭이 안 되면 명시:

```kotlin
includeBuild("../utils") {
    dependencySubstitution {
        substitute(module("org.sample:utils")).using(project(":"))
    }
}
```

용도 세 가지: **co-development**, **monorepo 구성**, **build-logic 분리**. (User Guide §composite_builds#defining-composite-builds)

---

## 10. 커스텀 플러그인 / 커스텀 Task

### 10.1 Lazy Property API

Gradle 9.x의 모든 신규 API는 **Provider / Property** 기반. 즉시 평가를 피해 Configuration Cache 친화적으로.

```kotlin
abstract class GenerateBuildInfoTask : DefaultTask() {

    @get:Input
    abstract val gitSha: Property<String>

    @get:OutputFile
    abstract val outputFile: RegularFileProperty

    @TaskAction
    fun run() {
        outputFile.get().asFile.writeText("git=${gitSha.get()}\nbuilt=${java.time.Instant.now()}\n")
    }
}

tasks.register<GenerateBuildInfoTask>("buildInfo") {
    gitSha = providers.exec {
        commandLine("git", "rev-parse", "HEAD")
    }.standardOutput.asText.map { it.trim() }
    outputFile = layout.buildDirectory.file("generated/buildinfo.txt")
}
```

키 포인트:
- **`abstract class` + `abstract val`** 패턴이 Gradle 9 표준. Gradle이 런타임에 implementation을 생성해준다.
- 입력은 `@Input`/`@InputFile`/`@InputDirectory`/`@Classpath`/`@Nested`로 정확히 표기 → 이게 incremental build와 build cache 키를 결정한다.
- 출력은 `@OutputFile`/`@OutputDirectory`. 최소 하나의 출력이 없으면 task는 항상 실행된다.
- **`System.getenv("X")` 직접 호출 금지** — `providers.environmentVariable("X")`. Configuration Cache 위반.
- **`Task.getProject()` 실행 시점 호출 금지** — execution phase에서 Project 접근 불가.

(User Guide §custom_tasks, §lazy_configuration, §incremental_build#sec:task_input_output_annotations)

### 10.2 Plugin + Extension

```kotlin
abstract class ShopBuildInfoExtension {
    abstract val applicationName: Property<String>
}

class ShopBuildInfoPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        val ext = project.extensions.create<ShopBuildInfoExtension>("shopBuildInfo")
        project.tasks.register<GenerateBuildInfoTask>("buildInfo") {
            gitSha = ext.applicationName  // 예시: extension 값을 task로 전달
            outputFile = project.layout.buildDirectory.file("generated/buildinfo.txt")
        }
    }
}
```

binary plugin으로 발행하려면 `java-gradle-plugin` 적용 + `gradlePlugin {}`에 plugin id 등록. (User Guide §implementing_gradle_plugins)

### 10.3 Pre-compiled script plugin

`*.gradle.kts` 파일을 `buildSrc/src/main/kotlin/`(또는 build-logic)에 두면 **파일 이름이 그대로 plugin id**가 된다.

```kotlin
// buildSrc/src/main/kotlin/shop.java-conventions.gradle.kts
plugins { java }
// ... 일반 build.gradle.kts처럼 작성
```

→ `id("shop.java-conventions")`로 적용. **현대 multi-module Spring Boot 빌드의 표준.**

---

## 11. 성능

### 11.1 Configuration Cache

**Gradle 9.0부터 "preferred mode of execution"** — 기본 ON은 아직 아니지만 강하게 권장된다. 다음 minor에서 default-on 후보. (Configuration Cache는 Isolated Projects의 전제. [blog.gradle.org/road-to-configuration-cache](https://blog.gradle.org/road-to-configuration-cache))

활성화:

```properties
# gradle.properties
org.gradle.configuration-cache=true
org.gradle.configuration-cache.problems=warn   # 처음엔 warn, 안정화되면 fail
org.gradle.configuration-cache.parallel=true   # 9.x에서 안정
```

**캐시되는 것:** configuration phase의 결과 = 어느 task가 그래프에 들어가는지, task의 입력값, dependency resolution 결과. **캐시 hit 시 configuration phase 전체 skip.**

**금지 패턴 (위반 시 fail):**

| 위반 | 대체 |
|---|---|
| `task.project.something` (실행 시점 Project 접근) | configuration 시점에 값을 잡아 Property로 보관 |
| `System.getenv("X")` / `System.getProperty("X")` 직접 사용 | `providers.environmentVariable("X")` / `providers.systemProperty("X")` |
| `File("...")` 즉시 IO at configuration time | `layout.projectDirectory.file("...")` |
| `Project.exec { ... }` 즉시 실행 | `providers.exec { ... }.standardOutput.asText` |
| `gradle.taskGraph.whenReady`에서 mutable state | configuration cache 친화적인 API로 재작성 |

Gradle 9.0은 위반을 **silent fail이 아니라 명시적으로 보고**한다. 9.0에서 popular 50개 plugin 중 절반 이상이 이미 호환. Spring Boot Gradle Plugin은 호환. ([blog.gradle.org](https://blog.gradle.org/road-to-configuration-cache))

**상충 관점:** 일부 enterprise 환경의 자체 플러그인이 아직 비호환. → `org.gradle.configuration-cache.problems=warn`으로 시작하고 violation을 하나씩 잡는 점진 도입이 현실적.

(User Guide §config_cache:intro, §config_cache:requirements)

### 11.2 Build Cache

**Configuration Cache는 configuration phase를, Build Cache는 task execution을 스킵**한다. 둘은 직교.

```properties
org.gradle.caching=true
```

- **Local cache** (`~/.gradle/caches/build-cache-1`): 자동.
- **Remote cache**: HTTP 기반. Develocity (구 Gradle Enterprise)가 운영형 옵션.
- 커스텀 task가 캐시 가능하려면 **`@CacheableTask` + 정확한 input/output 어노테이션** 필수.

(User Guide §build_cache, §build_cache#sec:caching_java_projects)

### 11.3 Incremental Build / 병렬

```properties
org.gradle.parallel=true
org.gradle.workers.max=8
```

- Incremental은 task의 input/output 해시 비교 결과. 어노테이션이 정확해야 동작.
- Parallel은 프로젝트 간 병렬. Configuration Cache 활성 시 같은 프로젝트 내 비의존 task도 병렬 가능.

(User Guide §incremental_build#sec:how_does_it_work)

### 11.4 Toolchain

```kotlin
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
        vendor = JvmVendorSpec.ADOPTIUM
    }
}
```

`settings.gradle.kts`에 Foojay resolver를 적용하면 누락된 JDK를 자동 다운로드:

```kotlin
// settings.gradle.kts
plugins {
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}
```

**Daemon JVM ≠ Build JVM** — Gradle 자체는 17+에서 돌지만 빌드 대상 JDK는 toolchain으로 별도 지정 가능. CI 일관성의 핵심. (User Guide §toolchains#sec:provisioning)

---

## 12. CI & Native

### 12.1 Gradle Wrapper

**언제나 wrapper(`./gradlew`)로 실행.** wrapper가 곧 빌드의 Gradle 버전 명세다. 9.5는 wrapper에 retry 옵션이 추가됨:

```properties
# gradle/wrapper/gradle-wrapper.properties
retries=3
retryBackOffMs=1000
```

([Gradle 9.5 Release Notes](https://docs.gradle.org/current/release-notes.html))

### 12.2 GitHub Actions — `gradle/actions/setup-gradle`

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-java@v5
        with:
          distribution: temurin
          java-version: 21
      - uses: gradle/actions/setup-gradle@v6
        with:
          cache-read-only: ${{ github.ref != 'refs/heads/main' }}
          dependency-graph: generate-and-submit
          build-scan-publish: true
          build-scan-terms-of-use-url: 'https://gradle.com/help/legal-terms-of-use'
          build-scan-terms-of-use-agree: 'yes'
      - run: ./gradlew build
```

핵심 input:
- `cache-read-only` — feature 브랜치에선 read-only, main에서만 write (PR이 캐시 오염 시키지 않게).
- `dependency-graph: generate-and-submit` — GitHub Dependency Graph API에 의존성 스냅샷 제출 → Dependabot alert.
- `build-scan-publish: true` — scans.gradle.com에 빌드 스캔 자동 발행.

([gradle/actions/setup-gradle docs](https://github.com/gradle/actions/blob/main/docs/setup-gradle.md))

### 12.3 GraalVM Native

```kotlin
plugins {
    id("org.springframework.boot") version "4.0.6"
    id("org.graalvm.buildtools.native") version "0.11.5"
    java
}
```

native plugin 적용 시:
1. `org.springframework.boot.aot` 플러그인이 **자동 적용**.
2. `aot`/`aotTest` 소스셋과 `processAot`/`processTestAot` task 등록.
3. `nativeCompile`이 `processAot` 출력을 사용.
4. `bootJar`에 reachability metadata와 `Spring-Boot-Native-Processed: true` 매니페스트 항목 추가.

**AOT만 단독 적용** (native 빌드 없이 JVM에서 CDS 활용 등):

```kotlin
plugins {
    id("org.springframework.boot")
    java
}
apply(plugin = "org.springframework.boot.aot")
```

(Spring Boot Gradle Plugin §aot, §packaging-oci-image#packaging-oci-image.native-image)

---

## 13. 의존성 보안

### 13.1 Dependency Verification

부트스트랩:

```bash
./gradlew --write-verification-metadata sha256,pgp build
```

`gradle/verification-metadata.xml` 생성. 이후 build마다 checksum 검증.

```xml
<verification-metadata>
    <configuration>
        <verify-metadata>true</verify-metadata>
        <verify-signatures>false</verify-signatures>
    </configuration>
    <components>
        <component group="org.springframework.boot" name="spring-boot" version="4.0.6">
            <artifact name="spring-boot-4.0.6.jar">
                <sha256 value="..." />
            </artifact>
        </component>
    </components>
</verification-metadata>
```

모드: `strict`(기본) / `lenient`(경고만) / `off`. CI는 strict, 부트스트랩/업데이트 PR은 lenient.

**Spring Boot 프로젝트 함정:**
- transitive 폭발 — 처음 부트스트랩하면 수백~수천 줄. PR 리뷰가 어렵다.
- 일부 의존성은 PGP 서명이 없다 → checksum fallback.
- `--write-verification-metadata`는 **현재 repo의 산출물을 그대로 신뢰**한다 → 부트스트랩 환경의 위생이 중요.

(User Guide §dependency_verification)

### 13.2 Dependency Locking

```kotlin
dependencyLocking {
    lockAllConfigurations()
    lockMode = LockMode.STRICT
}
```

```bash
./gradlew dependencies --write-locks   # 전체 lockfile 갱신
./gradlew dependencies --update-locks 'org.springframework:*'   # 부분 갱신
```

`gradle.lockfile` 한 파일에 모든 configuration의 해결된 버전. Dependabot이 verification metadata는 못 다루지만 lockfile은 다룬다.

(User Guide §dependency_locking)

### 13.3 Repository Content Filtering

타입스쿼팅·우발적 internal 의존성 누출 방지:

```kotlin
dependencyResolutionManagement {
    repositories {
        mavenCentral {
            content {
                excludeGroup("com.example.internal")
            }
        }
        maven("https://nexus.example.com/internal") {
            content {
                includeGroup("com.example.internal")  // 이 repo는 회사 그룹만
            }
        }
    }
}
```

`exclusiveContent {}`는 더 강한 형태 — "이 좌표는 **오직** 여기서만 받아라."

(User Guide §repository_content_filtering — 페이지 별도 anchor가 비공개일 수 있어 검증 필요)

---

## 14. Gradle 9.x 변경점 요약 (Spring Boot 관점)

### 9.0 (메이저)

- **Daemon JDK 17+ 필수**. 빌드 대상 JDK는 toolchain으로 별도 지정.
- **Configuration Cache = preferred mode**. 미사용 빌드 종료 시 활성화 안내 메시지.
- **Convention API 완전 제거** (`project.convention`, `SourceSetConvention` 등). 모든 빌드 스크립트가 영향 — Spring Boot 자체는 OK, 그러나 일부 third-party 플러그인이 깨질 수 있음.
- **`jcenter()` repository 제거.** 아직 남아있다면 `mavenCentral()`로 교체.
- **`Project#exec()` / `Project#javaexec()` 제거** → `providers.exec { }`.
- **Kotlin 2.2 / Groovy 4 베이스.** Kotlin Gradle Plugin 2.0+, Android Gradle Plugin 8.4+ 필수.
- **Archive task가 기본 reproducible**. 타임스탬프·파일 순서 의존 빌드 영향.
- **JSpecify nullability** 도입 (JSR-305 대체). Kotlin 2.1 strict nullness가 더 엄격해짐.
- `tasks { "test"() { ... } }` 같은 string-receiver eager 패턴 제거.

([Upgrading to Gradle 9.0](https://docs.gradle.org/current/userguide/upgrading_major_version_9.html))

### 9.1 ~ 9.4 (선택 하이라이트)

- Configuration Cache 호환성 + 진단 메시지 개선
- Tooling API 개선

### 9.5 (현재 current)

- **Task provenance**: 실패 task의 등록 출처(plugin/script) 명시.
- **Wrapper retries**: 다운로드 실패 시 재시도.
- **Precompiled Settings plugin에 type-safe accessor 생성**.
- `disallowChanges()` for domain object collection.
- `gradle init --into <dir>`.
- `--develocity-url` CLI 옵션.
- `--help` 출력 그룹화.

([Gradle 9.5 Release Notes](https://docs.gradle.org/current/release-notes.html))

### Isolated Projects (참고)

Configuration Cache의 후계. 프로젝트 간 격리를 통한 병렬 configuration. **9.x에 incubating 도입 계획**, 안정화 시점은 미정.

---

## 15. 실무 페인포인트 모음

### 15.1 "implementation vs api를 왜 구분해?"

- 기본은 `implementation`. `api`는 **public API 표면에 등장하는 타입에만** (return type, public method signature).
- `api` 남용 → 의존성 ABI 변경 시 consumer 전부 재컴파일 → 빌드 시간 폭발.
- **`java-library` 플러그인 없이는 `api`가 존재하지 않는다.** application 모듈은 보통 `java` plugin → `implementation`만 가능.

### 15.2 "Maven에서 옮길 때 `dependencyManagement`는?"

- 두 가지 길:
  - `io.spring.dependency-management` 플러그인 (Maven에 가장 비슷한 경험).
  - `dependencies { implementation(platform("...:spring-boot-dependencies:..."))` — Gradle 네이티브, 공식 권장.

### 15.3 "Configuration Cache 켰더니 X 플러그인이 비호환"

- 9.0부터 violation이 명확히 보고된다. 해결 순서:
  1. 위반 메시지가 third-party plugin 코드를 가리킴 → 해당 plugin의 최신 버전 확인 (대부분 호환 작업이 진행됨).
  2. 자체 빌드 스크립트의 위반 → §11.1 표 참고해 lazy API로 재작성.
  3. 정말 해결 불가 → 해당 configuration만 `org.gradle.configuration-cache.problems=warn`으로 일시 허용.

### 15.4 "Version Catalog vs BOM vs `ext` 변수"

- `ext` 변수(`extra["springBoot"] = "..."`) — **legacy, 피하라.** 타입 안전성 없음.
- BOM(`platform()`) — **transitive 버전 정렬** 도구.
- Version Catalog — **declaration 단축 + Dependabot 호환** 도구.
- **답: catalog + BOM 병용.** ext 변수는 버려라.

### 15.5 "buildSrc는 죽었나?"

- 죽지 않았다. 작은 규모엔 여전히 적합. **단, 변경 시 전체 task가 out-of-date** 되는 비용 인지. 대규모는 `build-logic` included build로.

### 15.6 "Native 빌드 시간이 너무 길다"

- 정상이다. native-image는 GraalVM의 whole-program 분석 + AOT 컴파일. 빌드 시간 5~20분이 흔하다.
- 완화: CI에서 native는 별도 job(주기적 또는 release만), 개발자 로컬은 JVM 빌드.
- `bootBuildImage` 캐시(buildpack layer cache)를 Volume으로 영속화하면 두 번째 빌드부터 단축.

### 15.7 "subprojects {} 쓰면 안 되는 이유"

- configuration time coupling — root가 모든 subproject를 평가해야 한다.
- IDE에서 "이 설정이 어디서 적용된 거지?" 추적 불가.
- Configuration Cache 친화성 ↓.
- 대안: convention plugin. 한 번 만들면 명시적이고, IntelliJ가 정확히 점프해준다.

### 15.8 "library 모듈 bootJar 함정"

- §6.4 그대로. library에는 `org.springframework.boot` 플러그인 미적용 + BOM만 platform으로.

### 15.9 "Gradle wrapper 버전 어떻게 올리나"

```bash
./gradlew wrapper --gradle-version 9.5 --distribution-type=bin
```

`--distribution-type=bin`을 명시하지 않으면 `all` (소스 포함, 200MB+)이 받아져 CI를 느리게 한다.

### 15.10 "왜 IDE에서 import 후 sync가 이렇게 오래 걸리나"

- Configuration Cache가 IDE sync 자체는 가속하지 않는다. Isolated Projects가 그 영역.
- 임시 완화: `org.gradle.parallel=true`, `org.gradle.jvmargs=-Xmx4g`. Daemon이 OOM이면 sync가 재시작되며 더 느려진다.

---

## 16. 참고문헌

### 1차 자료 (공식)

- **Gradle User Guide (current = 9.5)** — https://docs.gradle.org/current/userguide/userguide.html
  - §build_lifecycle, §kotlin_dsl, §multi_project_builds, §composite_builds, §sharing_build_logic_between_subprojects, §best_practices_structuring_builds
  - §declaring_configurations, §version_catalogs, §dependency_locking, §dependency_verification, §repository_content_filtering
  - §config_cache:intro, §config_cache:requirements, §config_cache:ide
  - §build_cache, §incremental_build, §lazy_configuration
  - §jvm_test_suite_plugin, §custom_tasks, §implementing_gradle_plugins, §implementing_gradle_plugins_precompiled
  - §toolchains
- **Gradle 9.0 Release Notes** — https://docs.gradle.org/9.0.0/release-notes.html
- **Gradle 9.5 Release Notes** — https://docs.gradle.org/current/release-notes.html
- **Upgrading to Gradle 9.0** — https://docs.gradle.org/current/userguide/upgrading_major_version_9.html
- **Spring Boot Gradle Plugin Reference (current = 4.0.6)** — https://docs.spring.io/spring-boot/gradle-plugin/index.html
  - Packaging Executable Archives, Packaging OCI Images, Running, Managing Dependencies, AOT, Reacting to Other Plugins
- **Kotlin Gradle docs** — https://kotlinlang.org/docs/gradle.html
- **gradle/actions/setup-gradle** — https://github.com/gradle/actions/blob/main/docs/setup-gradle.md

### 보조 자료

- Gradle blog — "State of the Configuration Cache (Road to Gradle 9)" — https://blog.gradle.org/road-to-configuration-cache
- Eric Haag — "Bootiful Builds: Best Practices for Spring Boot with Gradle" — https://erichaag.dev/posts/bootiful-builds-best-practices-spring-boot-gradle/
- Spring Boot issue #16689 (multi-module Kotlin bootJar) — https://github.com/spring-projects/spring-boot/issues/16689
- Gradle discuss forum 41459 (multi-module bootJar 의존성) — https://discuss.gradle.org/t/understanding-dependencies-in-multi-module-project-with-spring-boot-plugin/41459

---

## 17. 리서치 한계

이번 1차 리서치에서 **얕게 다루었거나 확인이 더 필요한 항목**:

1. **학술 문헌**: Build system 일반론(Bazel hermetic build, dependency hell resolution algorithm) 관련 학술 인용은 본 문서에 포함하지 않았다. 책의 신뢰성 보강용으로 1~2회 인용할 만한 후보:
   - Bazel: A Build System for the Cloud (Google whitepaper류) — incremental·hermetic build 이론
   - PubGrub algorithm (Dart team) — dependency resolution 의사결정
   - 챕터 저술 시 필요해지면 별도 paper-research pass 권장.

2. **커뮤니티 페인포인트 심화**: Reddit/HN/OKKY 1차 인용은 본 문서에서 §15에 요약했지만, **구체적 thread 인용은 책 저술 시 필요한 챕터에 한해 추가 발굴이 필요**. 특히:
   - "Configuration Cache 호환 안 되는 third-party plugin 사례 모음" — 책의 §11 보강에 유용.
   - "Maven → Gradle 마이그레이션 후일담" — 책 초반 챕터에 유용.
   - 한국어 자료(우아한형제들·카카오 기술블로그) 직접 발굴이 미흡.

3. **Repository Content Filtering 공식 anchor**: 페이지 fetch가 404 — 실제 anchor는 `filtering_repositories.html` 또는 `declaring_repositories_basics.html#sec:repository-content-filtering`로 추정. 챕터 작성 전 정확한 URL 재확인 필요.

4. **Gradle 9.1~9.4 변경점**: 9.0와 9.5만 정밀히 다뤘다. 9.1~9.4의 incremental 변경 사항(Configuration Cache 호환성 개선 등)은 필요 시 release notes를 통해 보강.

5. **GraalVM Native 운영 사례**: 빌드 시간/메모리 요구, CI 분리 전략의 1차 자료가 아직 얕다. Spring Boot 팀의 발표 자료(Phil Webb / Andy Wilkinson SpringOne)를 영상으로 보강 가능.

6. **Develocity / Build Scans 심화**: enterprise 캐시 서버, 테스트 분산 등은 본 문서에 개요만 포함. 책의 §11 또는 §12에서 짧게 다루되, 깊이 들어가지는 않을 것을 권장.

7. **Spring Boot Gradle Plugin 4.0의 신규 동작 변경점**: 3.x → 4.x 차이는 공식 reference를 통해 일부 확인됐으나, Migration 가이드 풀텍스트는 챕터 저술 시 별도 검증 권장.
