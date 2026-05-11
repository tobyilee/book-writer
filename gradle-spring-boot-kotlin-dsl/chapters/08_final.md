# 8장. 모듈을 쪼갠다 — settings 구조와 프로젝트 간 의존

7장까지 우리는 단일 모듈로 모든 일을 해냈다. `ch04-bootapp/`이라는 폴더 하나에 `build.gradle.kts` 하나가 있었고, 그 한 파일이 java 컴파일, Spring Boot 패키징, 테스트 분리, BOM 적용, 의존성 선언을 모두 받아냈다. 작은 앱이라면 이 구조로 평생 가도 된다.

그런데 회사 앱은 그렇게 작지가 않다. 어느 날 동료가 "주문 도메인하고 결제 도메인을 좀 떼어내자, 같은 jar에 다 들어 있으니 빌드도 느리고 변경 영향도 너무 크다"고 말한다. 합리적인 제안이다. 그래서 우리도 단일 모듈을 졸업할 때가 됐다.

`ch07` 폴더를 통째로 복사해 `ch08-multimodule/`을 만들고, 그 안에 `app`, `domain`, `order`, `payment` 네 디렉터리를 판다고 해보자. 각각의 디렉터리 안에 `build.gradle.kts`를 하나씩 둔다. 그러면 끝일까? 디렉터리만 쪼개면 멀티 모듈이 되는 걸까? 그럴 리가 없다. Gradle에게 "이 네 디렉터리가 같은 빌드에 속한 별개 프로젝트들이다"라고 알려줘야 한다. 그 알림이 곧 `settings.gradle.kts`의 일이다.

이 장에서 풀고 싶은 매듭은 단순하다. **단일 모듈을 멀티 모듈로 어떻게 옮기는가**. 그리고 그 과정에서 4장에 미리 박아둔 `settings.gradle.kts`의 골격이 어떻게 본격적으로 일하기 시작하는가. 마지막으로 — 그럼에도 불구하고 이 장의 끝에서 빌드가 깨진다. 왜 깨지는지의 진단은 9장의 몫이지만, 어떤 모양으로 깨지는지는 이 장의 끝에서 정확히 보여줄 것이다.

## settings는 입구다 — `include`로 모듈을 호명한다

4장에서 settings.gradle.kts는 "빌드의 입구"라고 했다. 그때는 단일 모듈이었으니 입구라는 비유가 좀 추상적으로 느껴졌을 수도 있다. 이제 그 입구가 실제로 어떤 일을 하는지가 드러난다.

`ch08-multimodule/settings.gradle.kts`는 이렇게 생긴다.

```kotlin
// settings.gradle.kts
pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

plugins {
    id("org.gradle.toolchains.foojay-resolver-convention") version "0.8.0"
}

dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories {
        mavenCentral()
    }
}

rootProject.name = "shop"
include("app", "domain", "order", "payment")
```

마지막 줄, `include("app", "domain", "order", "payment")`. 이 한 줄이 단일 모듈과 멀티 모듈을 가르는 분기점이다. Gradle은 이 한 줄을 보고 "아, 이 빌드에는 네 개의 하위 프로젝트가 있구나. 각 디렉터리에 가서 `build.gradle.kts`를 찾아 읽자"라고 결심한다.

이제 디렉터리 구조는 이렇게 된다.

```
ch08-multimodule/
├── settings.gradle.kts
├── gradle/
│   └── libs.versions.toml
├── app/
│   └── build.gradle.kts
├── domain/
│   └── build.gradle.kts
├── order/
│   └── build.gradle.kts
└── payment/
    └── build.gradle.kts
```

`settings.gradle.kts`는 루트에 하나, 그리고 각 모듈마다 `build.gradle.kts`가 하나씩이다. 루트에는 `build.gradle.kts`가 없어도 된다. 루트는 "모듈들을 묶는 컨테이너" 역할만 하고, 실제 빌드 정의는 각 하위 모듈이 가지고 있다. 이게 Gradle이 권장하는 멀티 모듈 골격이다.

> **박스 — `include`의 작은 문법**
>
> `include("order:api", "order:impl")`처럼 콜론으로 중첩 경로를 표현하면, Gradle은 `order/api/`, `order/impl/` 폴더를 찾는다. 그러니 `include(":order")` 처럼 앞에 콜론을 붙이는 건 의미가 없다 — Gradle 9.x에서는 경고도 안 뜨지만, 그냥 콜론 없이 `include("order")`로 쓰는 편이 깔끔하다.
>
> 모듈 디렉터리가 표준 위치와 다르다면 `project(":order").projectDir = file("services/order")` 한 줄을 settings에 추가하면 된다. 별로 권하지는 않는다 — 표준 위치를 따르는 편이 IDE도, 새로 합류한 동료도 모두에게 친절하다.

## 4장에 박아둔 골격이 본격적으로 일한다

settings.gradle.kts의 상단을 다시 보자. `pluginManagement {}`와 `dependencyResolutionManagement {}` 두 블록. 4장에서 단일 모듈에 미리 박아둔 그 골격이다. 그때는 "지금은 효과가 별로 안 느껴지지만 8장에서 진가를 본다"고 했다. 그 시간이 왔다.

**`pluginManagement {}` — 플러그인 버전의 단일 출처.** 멀티 모듈에서는 같은 플러그인을 여러 모듈이 적용한다. `app`도 Spring Boot 플러그인이 필요하고, 만약 `order`나 `payment`도 자체 부트 앱이라면 거기서도 필요하다. 만약 4장의 골격 없이 각 모듈의 `build.gradle.kts`마다 `id("org.springframework.boot") version "4.0.6"`을 박았다고 해보자. 어느 날 4.1.0으로 올리려고 하면 네 모듈을 다 뒤져야 한다. 한 군데 빠뜨리면 모듈 간에 버전이 어긋난다. 끔찍한 일이다.

`pluginManagement`에 한 번 박아두면 그게 끝난다. 4장에서 본 그 골격이다.

```kotlin
// settings.gradle.kts
pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}
```

그리고 각 모듈의 `build.gradle.kts`는 버전 없이 id만 적는다.

```kotlin
// app/build.gradle.kts
plugins {
    id("org.springframework.boot")
    java
}
```

버전은 루트에서, 적용은 각 모듈에서. 단일 출처의 원칙이 이렇게 멀티 모듈에서 본격적으로 작동한다. 4장에서 이걸 미리 박아둔 보람이 비로소 드러난다.

그런데 한 가지 짚고 가자. **버전을 어디에 적을 것인가**에는 사실 두 가지 길이 있다. 위에서 본 것처럼 `pluginManagement`에 박는 길이 있고, 다른 길은 루트의 `build.gradle.kts`에서 `plugins {}` 블록에 `apply false`로 받아두는 길이다. 어느 쪽이 더 좋은가? Gradle 공식 가이드는 후자, 즉 루트 build.gradle.kts의 plugins 블록 + `apply false` 패턴을 권장하는 추세다. 하지만 이 책에서는 `pluginManagement`를 우선으로 잡았다. 이유는 단순하다 — settings 한 곳에 "빌드의 부트스트랩"을 모으는 편이 새로 합류한 동료에게 더 친절하다. 어느 쪽을 쓰든 9.x에서 모두 정상으로 동작하니, 팀 컨벤션에 맞춰 고르면 된다.

**`dependencyResolutionManagement {}` — repo의 단일 출처.** 그리고 이건 한 술 더 뜬다. 4장에서 박은 그 한 줄을 다시 보자.

```kotlin
dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories {
        mavenCentral()
    }
}
```

`FAIL_ON_PROJECT_REPOS`. 이 한 줄이 멀티 모듈 빌드의 안전망이다. 만약 누군가가 `payment/build.gradle.kts`에 슬쩍 `repositories { maven("https://my-private-mirror.example.com") }`를 추가하면, 빌드가 이 한 줄에 걸려 빨간 메시지를 뱉으며 멈춘다.

> Build was configured to prefer settings repositories over project repositories but repository 'maven3' was added by build file 'payment/build.gradle.kts'

처음 받으면 짜증이 날 수도 있다. "내가 내 모듈에 repo 하나 추가하는데 왜 안 되는데?"라고. 그런데 이게 정확히 우리가 원하는 행동이다. 회사 빌드의 의존성 출처가 외부 무명 repo로부터 흘러들어오는 일을 settings 한 줄로 차단할 수 있다. 보안팀이 좋아한다. 우리도 결국 좋아하게 된다.

단일 모듈에서는 이 강제가 큰 의미가 없었다. 어차피 모듈이 하나뿐이니 repo를 settings에 적든 build에 적든 결과가 같다. 멀티 모듈로 넘어오는 이 순간, FAIL_ON_PROJECT_REPOS가 비로소 가치 있는 안전망이 된다.

## 각 모듈의 build.gradle.kts — 일단 중복을 그대로 받아들인다

이제 각 모듈의 `build.gradle.kts`를 들여다보자. `app`부터다.

```kotlin
// app/build.gradle.kts
plugins {
    id("org.springframework.boot")
    java
}

group = "com.shop"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

dependencies {
    implementation(project(":domain"))
    implementation(project(":order"))
    implementation(project(":payment"))

    implementation(platform(SpringBootPlugin.BOM_COORDINATES))
    implementation("org.springframework.boot:spring-boot-starter-web")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.test {
    useJUnitPlatform()
}
```

여기 새 얼굴이 하나 등장한다 — `implementation(project(":domain"))`. 이 한 줄이 프로젝트 간 의존성의 정체다. `org.springframework.boot:spring-boot-starter-web`처럼 외부 라이브러리 좌표를 적는 자리에, `project(":domain")` 함수를 호출해 같은 빌드 안의 다른 프로젝트를 가리킨다. settings.gradle.kts의 `include("domain")`이 만들어둔 그 `:domain` 프로젝트다.

`domain`, `order`, `payment` 세 모듈의 `build.gradle.kts`도 각자 비슷한 모양이다. `domain`을 보자.

```kotlin
// domain/build.gradle.kts
plugins {
    id("org.springframework.boot")
    java
}

group = "com.shop"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

dependencies {
    implementation(platform(SpringBootPlugin.BOM_COORDINATES))
    implementation("org.springframework:spring-context")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.test {
    useJUnitPlatform()
}
```

`order/build.gradle.kts`와 `payment/build.gradle.kts`도 거의 똑같이 생겼다. `domain`에 의존성이 필요한 모듈은 `implementation(project(":domain"))`을 하나 추가한 정도가 다를 뿐, 위의 골격은 완전히 동일하다.

이 시점에서 눈썰미 있는 독자는 한 가지를 알아챈다. **네 모듈의 build.gradle.kts가 거의 똑같다.** 같은 java toolchain, 같은 group/version, 같은 BOM, 같은 useJUnitPlatform(). 이걸 그대로 두는 게 정말 맞을까? 본능적으로 "네 군데 똑같은 게 들어 있으면 한 곳에 모아야지" 하는 마음이 든다. 찜찜하다.

그 본능은 옳다. 그런데 본능을 따라 한 곳에 모으는 가장 흔한 방법 — `subprojects {}` 블록 — 은 사실 안티패턴이다.

> **함정 박스 — `subprojects {}` / `allprojects {}`는 안티패턴**
>
> 루트 build.gradle.kts에 `subprojects { java { toolchain { ... } } }` 같은 블록을 두면 네 모듈에 일괄로 적용되긴 한다. 단기적으로 편해 보인다. 그런데 이 패턴은 **configuration-time coupling**을 만든다 — 루트가 모든 하위 프로젝트의 평가 시점을 강제로 묶어버린다는 뜻이다. IntelliJ에서 "이 설정이 어디서 적용된 거지?" 추적도 안 되고, Configuration Cache 친화성도 떨어진다.
>
> 그러니 일단 이 장에서는 중복을 그대로 두자. **`subprojects {}`로 모으지 말자.** 답은 10장의 Convention Plugin이다. 10장에서 이 중복을 깔끔하게 정리한다. 지금은 "중복이 보인다, 찜찜하다, 곧 정리한다"고 기억해두면 된다.

자, 그러면 일단 네 모듈의 build.gradle.kts를 그대로 둔 상태에서, 모듈 간 의존성이 어떻게 표현되는지를 마저 보자.

## `project(":domain")` — 같은 빌드 안의 의존성

`app/build.gradle.kts`에 적힌 `implementation(project(":domain"))`. 이게 정확히 무슨 일을 하는가.

Gradle은 이 한 줄을 보고 두 가지 일을 한다. 첫째, `app`을 컴파일할 때 `domain`의 컴파일 산출물(class 파일들)을 classpath에 올려준다. 둘째, `app`을 빌드하기 전에 `domain`이 먼저 빌드되도록 task 의존성을 자동으로 잡는다. 우리가 따로 "domain 먼저, app 다음"이라고 적지 않아도, `implementation(project(":domain"))` 한 줄이 그 순서까지 책임진다.

콜론 표기를 한 번 짚어두자. `project(":domain")`의 콜론은 "빌드 루트로부터의 절대 경로"라는 뜻이다. 만약 `include("services:order")` 처럼 중첩으로 모듈을 호명했다면, 그 모듈을 가리킬 때는 `project(":services:order")`로 쓴다. 디렉터리 구분자 `/`가 콜론 `:`으로 바뀐 형태라고 외워두면 편하다.

그리고 `implementation`을 썼다는 사실에 한 번 더 주목하자. 5장에서 `implementation`과 `api`의 구분을 살펴봤었다. `app`이 `domain`의 타입을 자기 메서드 시그니처에 노출하지 않고 안에서만 쓴다면 `implementation`이 맞다. 만약 `order`가 자기 public API에 `domain`의 `Order` 클래스를 노출한다면 — 그래서 `app`이 `order`의 메서드를 호출하면서 자동으로 `Order` 타입을 받게 된다면 — `order`의 build.gradle.kts에서는 `api(project(":domain"))`을 써야 할 수도 있다. 단, `api`를 쓰려면 `java-library` 플러그인이 적용된 모듈이어야 한다. 지금 우리 네 모듈은 다 `java` plugin이라 `api`라는 단어 자체가 없다. 그러니 일단은 모두 `implementation`이다.

> **박스 — `compileOnly`도 같은 문법을 쓴다**
>
> 5장에서 본 다른 declarable configuration들도 `project(...)`를 받는다. `compileOnly(project(":api-spec"))`, `testImplementation(project(":test-fixtures"))` 같은 식이다. 한 가지 기억할 점은 `testFixtures` 컴포넌트를 쓰려면 `java-test-fixtures` 플러그인을 적용한 모듈에서 `testImplementation(testFixtures(project(":domain")))`로 명시해야 한다는 정도다. 본격적인 활용은 운영 챕터에서 다시 만난다.

## Version Catalog는 자동으로 모듈 전체에 공유된다

5장에서 BOM과 Version Catalog의 관계를 다잡았다. 그때 만든 `gradle/libs.versions.toml`이 이번에도 그대로 살아 있다. 그리고 멀티 모듈에서 한 가지 좋은 소식이 있다 — **Catalog는 settings.gradle.kts에 따로 등록하지 않아도, `gradle/libs.versions.toml` 파일이 루트의 `gradle/` 폴더 안에 있기만 하면 모든 모듈에 자동으로 보인다.**

`app/build.gradle.kts`에서도, `domain/build.gradle.kts`에서도, 똑같이 `libs.spring.boot.starter.web` 같은 짧은 별칭이 type-safe accessor로 보인다. IntelliJ가 자동완성으로 띄워준다. 이게 멀티 모듈에서 Catalog가 빛나는 지점이다 — 한 파일에 의존성 좌표를 모아두고, 네 모듈이 모두 그 한 파일을 본다.

```kotlin
// app/build.gradle.kts
dependencies {
    implementation(project(":domain"))
    implementation(platform(libs.spring.boot.bom))
    implementation(libs.spring.boot.starter.web)
    testImplementation(libs.spring.boot.starter.test)
}
```

`libs.versions.toml`을 settings의 `dependencyResolutionManagement { versionCatalogs { ... } }` 블록에서 명시적으로 선언할 수도 있다 — 여러 Catalog를 쓰거나 파일명이 표준이 아닐 때다. 우리는 한 개의 Catalog만 쓰고 파일명도 표준이니 자동 등록에 맡긴다. 깔끔하다.

## 그래서 — `./gradlew :app:bootRun`을 돌려보자

자, 네 모듈로 쪼개기를 끝냈다. settings.gradle.kts에 `include("app", "domain", "order", "payment")`를 적었고, 각 모듈에 build.gradle.kts를 두었고, `app`은 나머지 세 모듈을 `project(...)`로 끌어왔다. `domain`에는 `Order`, `OrderRepository` 같은 도메인 클래스들이 있고, `order` 모듈에는 그 도메인을 쓰는 `OrderService`가, `payment` 모듈에는 `PaymentService`가 있다. `app`의 `ShopApplication`은 이 모든 모듈의 빈을 끌어 모아 Spring Boot 앱으로 띄운다.

이제 첫 빌드를 돌릴 차례다.

```bash
$ ./gradlew :app:bootRun
```

콘솔에 친숙한 Spring Boot 배너가 떠야 한다. 그런데 — 뜨지 않는다. 대신 이런 로그가 떨어진다.

```
> Task :domain:compileJava
> Task :domain:processResources NO-SOURCE
> Task :domain:classes
> Task :domain:bootJar
> Task :domain:inspectClassesForKotlinIC SKIPPED
> Task :domain:jar SKIPPED
> Task :order:compileJava FAILED

/Users/me/ch08-multimodule/order/src/main/java/com/shop/order/OrderService.java:3:
error: package com.shop.domain does not exist
import com.shop.domain.Order;
                      ^
/Users/me/ch08-multimodule/order/src/main/java/com/shop/order/OrderService.java:4:
error: package com.shop.domain does not exist
import com.shop.domain.OrderRepository;
                      ^
2 errors

FAILURE: Build failed with an exception.

* What went wrong:
Execution failed for task ':order:compileJava'.
> Compilation failed; see the compiler error output for details.

* Try:
> Run with --stacktrace option to get the stack trace.
> Run with --info or --debug option to get more log output.
> Run with --scan to get full insights.
```

당황스럽다. `domain` 모듈에는 분명 `com.shop.domain.Order`라는 클래스가 있다. `domain:compileJava`도 성공했고, `domain:classes`도 성공했다. `order` 모듈은 `implementation(project(":domain"))`을 정확히 적었다. 그런데 `order:compileJava`는 "`com.shop.domain` 패키지가 없다"고 한다.

뭐가 잘못된 건가? 분명 단일 모듈에서는 멀쩡히 돌던 코드다. `ch07`의 코드를 그대로 네 폴더로 쪼개 옮겼을 뿐이다. 모듈을 쪼갰다는 사실 자체가 `domain`의 클래스를 사라지게 했을 리는 없다. 그런데 컴파일러는 `com.shop.domain` 패키지 자체가 보이지 않는다고 말한다.

로그를 다시 한 줄씩 살펴보자. `> Task :domain:bootJar` — 어, `bootJar`? `domain`은 라이브러리 모듈이지 실행 가능한 앱이 아닌데 왜 `bootJar` task가 돌았지? 그리고 그 바로 다음 줄, `> Task :domain:jar SKIPPED` — 일반 `jar`는 왜 SKIPPED인가? 5장에서 분명히 `bootJar`와 `jar`는 공존하고 `assemble`이 둘 다를 굽는다고 했는데. 뭔가 어긋났다.

여기서 미스터리가 두 갈래다. **첫째, `domain`의 일반 `jar`는 왜 SKIPPED인가?** **둘째, 그렇다면 `domain`의 컴파일된 클래스들은 지금 어디로 갔는가?** `bootJar`에는 들어갔는데, 일반 `jar`는 안 만들어졌으니, `order`가 `implementation(project(":domain"))`으로 끌어올 때 받는 그 jar는 도대체 어떤 모양인 것일까?

> **Cliffhanger — 정상 빌드가 안 된다. 9장의 미스터리.**
>
> 단일 모듈 `ch07`에서 멀쩡히 돌던 코드를 네 모듈로 쪼갰을 뿐인데 `./gradlew :app:bootRun`이 `package com.shop.domain does not exist`로 깨진다. `domain:compileJava`는 성공했는데도 그렇다. 그리고 빌드 로그에는 의심스러운 두 줄이 있다 — `:domain:bootJar` 가 돌았고, `:domain:jar`는 SKIPPED 됐다.
>
> 이게 정확히 어떤 메커니즘으로 일어나는지, 그리고 왜 Spring Boot 공식 이슈 트래커에 같은 사고가 반복되는지를 9장에서 정면으로 진단한다. 우리 빌드는 멀티 모듈로 넘어오는 순간 Spring Boot Gradle 플러그인의 가장 유명한 함정 하나에 발이 걸렸다.
>
> 위의 출력 로그를 손에 쥐고 9장으로 넘어가자. 진단부터 시작한다.

## 마무리

8장에서 우리는 단일 모듈을 졸업했다. `settings.gradle.kts`에 `include(...)`로 네 모듈을 호명했고, 4장에 미리 박아둔 `pluginManagement`와 `dependencyResolutionManagement` 골격이 멀티 모듈에서 본격적으로 일하기 시작했다. `FAIL_ON_PROJECT_REPOS`가 회사 표준 repo를 강제하는 안전망이라는 의미도 이제 손에 잡힌다. `implementation(project(":domain"))`으로 같은 빌드 안의 다른 프로젝트를 끌어 쓰는 문법도 익혔다. Version Catalog는 `gradle/libs.versions.toml` 한 곳에서 네 모듈을 자동으로 먹여주고 있다.

그런데 빌드가 깨졌다. 네 모듈의 build.gradle.kts가 거의 똑같은 모양으로 중복되는 찜찜함도 남아 있다. 두 가지 숙제가 생긴 셈이다.

먼저 **9장**에서 빌드를 살려낸다. `:domain:bootJar`와 `:domain:jar SKIPPED`의 정체를 정면으로 진단하고, library 모듈에는 어떻게 손을 대야 정상 빌드가 되는지 두 가지 처방을 살펴본다.

그 다음 **10장**에서 네 모듈의 중복을 정리한다. `subprojects {}`라는 안티패턴을 피하고, Convention Plugin이라는 깔끔한 답을 손에 쥔다. 그러면 네 모듈의 build.gradle.kts는 각각 단 몇 줄로 줄어든다.

일단은 9장이다. 위의 실패 로그를 그대로 들고 넘어가자.
