# 3장. Kotlin DSL 그리고 그 함정

> 이번 챕터는 `ch01/` 폴더에서 동작한다. 의존성 한 줄짜리 Hello World 스크립트, 그게 전부다.

2장에서 사고 모델을 짰다. Settings가 빌드의 입구고, Project가 task와 configuration의 묶음이고, declarable/resolvable/consumable 세 역할이 한 단어 `implementation`에 압축되어 있다는 것까지 봤다. 머리로는 정리됐는데, 막상 `build.gradle.kts` 파일을 열어 한 줄을 적으려는 순간 손이 멈춘다. **이게 Kotlin 코드인가, 아니면 Kotlin 척하는 어떤 DSL인가?**

Gradle은 한참 동안 Groovy DSL을 기본으로 써왔다. `apply plugin: 'java'` 같은 문법이 자연스러웠던 시절이다. 동적 언어의 자유로움 덕에 한 줄짜리 빌드 스크립트는 짧고 멋졌다. 그런데 그 자유가 곧 함정이었다. `bootJar { mainClas = 'X' }` 같은 오타를 적어도 빌드 스크립트는 묵묵히 컴파일됐고, 런타임이 되어서야 "그런 프로퍼티는 없는데요" 하고 뒤늦게 비명을 질렀다. 자동완성? IDE가 동적 타입을 어디까지 추론해줄 수 있겠는가. 늘 반쯤만 도와줬다.

Kotlin DSL은 그 정반대의 약속이다. 타입이 있다. 컴파일러가 있다. 그러니 빌드 스크립트도 코드처럼 다루자. 그런데 그 약속을 받아들이는 순간 새로운 함정이 따라온다. 이번 장에서는 그 약속과 함정을 같이 본다.

## 왜 Kotlin DSL인가

먼저 솔직해지자. "타입 안전성이 좋다"는 말은 너무 추상적이다. 구체적으로 무엇이 좋은가.

첫째, **오타가 빌드 스크립트에서 잡힌다.** `bootJar { mainClass = "..." }`를 `mainClas`로 잘못 적으면 IntelliJ가 즉시 빨간 줄을 긋는다. Groovy DSL이라면 `./gradlew bootJar`를 돌리고 한참을 기다린 다음에야 알게 된다. 빌드 스크립트가 길어질수록, 멀티 모듈이 될수록 이 차이는 점점 무겁다.

둘째, **자동완성이 진짜로 동작한다.** `tasks.named<Test>("test") { 여기서 ctrl+space }` 를 누르면 Test task의 모든 프로퍼티가 뜬다. `useJUnitPlatform()`, `maxParallelForks`, `systemProperty(...)`. 이건 IDE가 추론해준 추측이 아니다. 타입이 명시되어 있으니 정확하다. Groovy DSL에선 절반의 시간을 "이 블록 안에서 뭘 쓸 수 있는 거지?"라고 문서를 뒤지며 보냈다면, Kotlin DSL에선 그 시간이 거의 사라진다.

셋째, **리팩토링이 안전하다.** 커스텀 task 이름을 바꿀 때, extension 클래스 시그니처를 바꿀 때, IntelliJ의 rename 한 번이면 빌드 스크립트 전체에 일관되게 반영된다. 동적 언어 빌드 스크립트에선 상상하기 어려운 안전망이다.

그렇다면 단점은 없는가. 있다. 한 가지 — **첫 빌드가 느리다.** Kotlin 컴파일러가 빌드 스크립트를 한 번 컴파일해야 하니까. Groovy DSL에 비해 첫 실행이 몇 초 느리게 느껴질 수 있다. 그런데 두 번째부터는 캐싱이 들어가서 차이가 의미 없는 수준이 된다. 그러니 이 한 가지 단점을 두려워해서 타입 안전성을 포기할 이유는 없다. 오히려 캐싱 메커니즘은 Configuration Cache가 안정화되는 9.x에서 점점 더 강력해진다 — 그건 13장에서 본다.

이 책은 처음부터 끝까지 Kotlin DSL을 기본으로 쓴다. Groovy DSL은 비교 표나 인용 박스에서만 등장한다.

## 첫 build.gradle.kts — 의존성 한 줄

자, 이제 손가락을 움직여보자. `ch01/` 폴더를 만들고, 그 안에 `settings.gradle.kts`와 `build.gradle.kts` 두 파일을 둔다.

```kotlin
// ch01/settings.gradle.kts
rootProject.name = "ch01"
```

```kotlin
// ch01/build.gradle.kts
plugins {
    java
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.slf4j:slf4j-api:2.0.13")
}
```

이게 전부다. 12줄짜리 빌드 스크립트. 작아 보이지만 한 줄 한 줄에 사고 모델이 다 들어 있다.

`plugins { java }` — 2장에서 본 plugin 적용. `java` 한 단어는 사실 `id("java")`의 줄임이다. Kotlin DSL은 자주 쓰는 코어 플러그인에 대해 이런 짧은 표현을 허용한다. 이 한 줄이 적용되는 순간 `compileJava`, `test`, `jar`, `assemble`, `check`, `build` 같은 task들이 자동 등록되고, `implementation`/`runtimeOnly`/`compileOnly`/`testImplementation` 같은 declarable configuration이 만들어진다. 2장의 사고 모델이 코드로 풀린 첫 순간이다.

`repositories { mavenCentral() }` — 의존성을 어디서 찾을지. 멀티 모듈로 가면 이걸 root의 `settings.gradle.kts`로 옮기는 게 정석이지만(8장에서 본다), 지금은 단일 모듈이니 여기 둔다.

`dependencies { implementation("...") }` — 2장에서 본 declarable configuration의 첫 등장이다. `implementation`은 "이 의존성은 컴파일과 런타임 둘 다 필요하지만, 내 라이브러리를 쓰는 소비자에겐 노출하지 마라"라는 선언이다. 이걸 Gradle이 resolvable configuration(`compileClasspath`, `runtimeClasspath`)로 변환해서 실제 파일을 가져온다. 우리는 "무엇이 필요한지"만 적었지, "어떻게 가져올지"는 적지 않았다. 그게 Gradle 사고 모델의 핵심이라는 점, 다시 기억해두자.

`./gradlew build`를 돌려보면 빌드가 성공한다 — 정확히는 `src/main/java`에 자바 파일이 하나도 없으니 컴파일할 게 없고, 테스트도 없어서 `test`가 건너뛰어진다. 그래도 task graph는 잘 짜여서 흐른다. 이게 우리 책 전체의 출발점이다. 의존성 한 줄. 다음 챕터부터 이게 자라기 시작한다.

## 문법의 함정들

12줄짜리 스크립트는 평화로워 보이지만, 한 발만 더 깊이 들어가면 Kotlin DSL 특유의 함정들이 줄지어 기다린다. 미리 짚어두자.

### 1. 큰따옴표만 허용한다

Groovy DSL에선 `implementation 'org.slf4j:slf4j-api:2.0.13'` 처럼 작은따옴표가 자연스러웠다. 그래서 Groovy 빌드 스크립트를 Kotlin DSL로 옮겨 적다 보면 손이 작은따옴표를 친다.

```kotlin
// 이건 컴파일 에러다
implementation('org.slf4j:slf4j-api:2.0.13')
```

Kotlin에서 작은따옴표는 `Char` 리터럴이다. `'a'`처럼 한 글자만 들어갈 수 있다. 문자열은 반드시 큰따옴표. 사소해 보이지만 Groovy 출신은 이 함정에 한 번씩은 꼭 걸린다. **빌드 스크립트의 모든 문자열은 큰따옴표.** 잊지 말자.

### 2. type-safe accessor는 plugins 블록 이후에만 노출된다

이건 좀 더 미묘하다. Kotlin DSL의 핵심 자랑인 type-safe accessor — 예를 들어 `java { sourceCompatibility = JavaVersion.VERSION_21 }` 같은 깔끔한 문법 — 는 사실 마법이 아니다. Gradle이 `plugins {}` 블록을 먼저 평가해서 어떤 플러그인이 적용되는지 알아낸 다음, 그 플러그인이 만드는 extension/task/configuration에 대해 type-safe accessor를 자동 생성한다.

그러니 순서가 중요하다.

```kotlin
plugins {
    java
}

// 여기서부터 java extension의 type-safe accessor가 노출된다
java {
    sourceCompatibility = JavaVersion.VERSION_21
}
```

`plugins {}` 블록은 빌드 스크립트의 가장 위에 와야 한다. 그 위에 임의의 Kotlin 코드를 적으면 안 된다. 자, 그렇다면 이런 의문이 생긴다. **`plugins {}` 블록을 안 쓰고 다른 방법으로 플러그인을 적용하면?**

### 3. apply(plugin = ...) fallback

옛 스타일 또는 동적으로 플러그인을 적용할 때 `apply(plugin = "...")` 문법을 쓴다.

```kotlin
apply(plugin = "io.spring.dependency-management")

// 이건 컴파일 에러 — type-safe accessor가 안 생긴다
dependencyManagement {
    imports { mavenBom("...") }
}
```

왜? `apply(plugin = "...")`은 빌드 스크립트가 컴파일된 다음, **실행 시점**에 플러그인을 적용한다. 그러니 컴파일 단계에선 그 플러그인이 어떤 extension을 만들지 알 수 없다. 그러니 accessor도 못 만든다. 이 경우 `configure<T> {}` 형태의 fallback을 써야 한다.

```kotlin
apply(plugin = "io.spring.dependency-management")

configure<io.spring.gradle.dependencymanagement.dsl.DependencyManagementExtension> {
    imports { mavenBom("...") }
}
```

코드가 못나졌다. 그래서 **가능하면 `plugins {}` 블록을 쓰는 편이 낫다.** `apply(...)`는 정말 필요할 때만 — 예를 들어 convention plugin 내부에서 다른 plugin을 조건부 적용할 때 정도.

이 함정은 10장 Convention Plugin 챕터에서 또 한 번 만난다. 거기선 `"implementation"(platform(...))` 같이 갑자기 문자열이 등장하는 이유를 정면으로 다룬다. 일단 지금은 "type-safe accessor는 공짜가 아니다, plugins 블록의 산물이다"라는 한 줄만 기억해두면 충분하다.

> **lazy property는 `=` 권장, eager get은 피하기**
>
> 빌드 스크립트를 적다 보면 task의 프로퍼티를 설정할 일이 생긴다. 두 가지 스타일이 있다.
>
> ```kotlin
> // 권장 — Gradle 8.2+
> tasks.named<Jar>("jar") {
>     archiveClassifier = "boot"
> }
>
> // legacy — 가능하지만 권장하지 않음
> tasks.named<Jar>("jar") {
>     archiveClassifier.set("boot")
> }
> ```
>
> 그리고 task를 가져오는 두 가지 방법도 있다.
>
> ```kotlin
> // 정석 — lazy, 필요할 때만 실체화
> tasks.named<Test>("test") { useJUnitPlatform() }
>
> // 피하라 — eager, 즉시 실체화
> tasks.getByName<Test>("test") { useJUnitPlatform() }
> ```
>
> `=`가 권장되는 이유, `named`가 정석인 이유는 Gradle의 lazy Property API와 task lazy registration 메커니즘에 뿌리가 있다. 빌드 그래프를 실제로 다 만들기 전까지는 task를 실체화하지 않는 게 Configuration Cache 친화적이고, 빌드 시간도 짧다. **본격적인 Property/Provider API 다이브는 12장에서 다룬다.** 거기서 커스텀 task를 만들 때 이 약속들이 왜 그리 중요한지 손에 잡힌다. 지금은 그저 "`=` 쓰고, `getByName` 대신 `named` 쓴다"는 두 줄 규칙만 챙기자.

## Groovy → Kotlin DSL 매핑 표

기존 Groovy 빌드 스크립트를 Kotlin DSL로 옮기거나, 인터넷에서 본 Groovy 예제를 따라 적을 때 자주 쓰는 매핑을 한 곳에 정리해두자.

| Groovy DSL | Kotlin DSL |
|---|---|
| `apply plugin: 'java'` | `plugins { java }` (또는 `id("java")`) |
| `implementation 'org.springframework.boot:spring-boot-starter-web'` | `implementation("org.springframework.boot:spring-boot-starter-web")` |
| `bootJar { mainClass = 'X' }` | `tasks.named<BootJar>("bootJar") { mainClass = "X" }` |
| `ext.springBootVersion = '4.0.6'` | `extra["springBootVersion"] = "4.0.6"` (또는 Version Catalog, 5장) |
| `task myTask(type: Copy) { ... }` | `tasks.register<Copy>("myTask") { ... }` |
| `subprojects { ... }` | **피하라** (10장에서 Convention Plugin으로 대체) |
| `sourceCompatibility = 1.8` | `java { sourceCompatibility = JavaVersion.VERSION_1_8 }` |

표만 보고 옮기다 보면 한 가지 패턴이 보인다. **Groovy DSL이 동적으로 풀어주던 문맥을 Kotlin DSL은 타입과 명시적 호출로 풀어낸다.** `bootJar { ... }` 한 줄은 Groovy에선 마법처럼 동작하지만, Kotlin DSL에선 "어떤 task인지(`bootJar`), 어떤 타입인지(`BootJar`), 어떻게 가져올지(`named`)"를 다 적어줘야 한다. 처음엔 번거롭게 느껴진다. 익숙해지면 그 명시성이 곧 안정성이라는 걸 알게 된다.

## 9.5의 신호 — precompiled Settings plugin accessor

9.5에서 Kotlin DSL과 관련해 작지만 의미 있는 개선이 하나 있다. **precompiled Settings plugin에 대해서도 type-safe accessor가 생성된다.**

직접 만나기엔 아직 이르다. 10장에서 Convention Plugin을 만들 때, 그리고 settings 수준의 공통 설정을 plugin으로 모듈화하고 싶을 때 이게 빛난다. 이전엔 settings 수준 convention plugin을 쓰면 그 안에서 `the<DependencyResolutionManagementExtension>()` 같은 string-based fallback으로 떨어졌는데, 9.5부터는 project plugin과 동일한 type-safe 경험을 받는다. 사소해 보이지만, "Kotlin DSL의 약속이 settings 영역까지 확장된다"는 신호다. 9.x가 점점 더 Kotlin DSL을 1급 시민으로 대접하고 있다는 흐름의 한 조각.

> **함정 박스 — `subprojects {}` 안티패턴 예고**
>
> 멀티 모듈 빌드를 검색해보면 `subprojects { apply plugin: 'java' ... }` 같은 예제가 산처럼 쏟아진다. 동작은 한다. 그런데 그게 곧 좋은 패턴은 아니다. configuration-time coupling, IDE 추적 불가, Configuration Cache 친화성 저하 — 단점이 길다. 처방은 **Convention Plugin**이고, 10장이 그 자리다. 지금 단일 모듈에서 빌드 스크립트를 적을 때야 무관하지만, 8장에서 모듈을 쪼개기 시작하면 이 유혹이 곧 찾아온다. **그때 손이 `subprojects {}`로 가려고 하면, 잠시 멈추고 10장으로 점프하자.** 지금은 한 줄 예고만.

## 3장을 닫으며 — Part I 마무리

Part I 세 챕터를 통과했다. 1장에서 빌드 스크립트를 다시 짜야 하는 이유와 이 책의 출구 상태를 봤고, 2장에서 Gradle의 사고 모델 — Settings/Project/Task/Configuration/Lifecycle — 을 자기 언어로 풀었다. 그리고 이번 3장에선 그 사고 모델을 Kotlin DSL이라는 표면 위에서 실제 코드 12줄로 풀어보고, 그 12줄 뒤에 숨은 함정들을 짚었다.

지금 우리 손엔 `ch01/build.gradle.kts` 한 파일이 있다. 의존성 한 줄. 그게 전부다. 작아 보여도, Settings/Project/Plugin/declarable configuration이 다 등장하는 완결된 빌드다. 이 자리에서 출발해서, Part II 4장부터 우리는 진짜 Spring Boot 앱을 빌드하기 시작한다.

다음 챕터의 출발점은 익숙한 질문이다. **Maven에서 쓰던 모든 개념은 Gradle에서 어디로 가는가?** `pom.xml`의 모든 요소 — `dependencyManagement`, `parent`, `<profile>`, `<repositories>`, `<pluginManagement>` — 가 Gradle 어디에 자리를 잡는지 1:1로 다리를 놓는다. Maven 출신이 가장 답답해하는 영역을 가장 먼저 풀어주는 챕터다. Maven 경험이 없는 독자도 안심해도 좋다. Maven 비교는 박스로 격리해서, 박스를 건너뛰어도 본문은 매끄럽게 흐른다.

Part I이 사고 모델이라면, Part II는 그 사고 모델로 단일 모듈 Spring Boot 앱을 책임지고 빌드하는 부다. 의존성 한 줄짜리 `ch01`이 4장에서 `ch04-bootapp/`로 자라난다.
