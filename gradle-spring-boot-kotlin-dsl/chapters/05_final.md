# 5장. 의존성을 다스리는 정석 — Version Catalog와 BOM

4장의 마지막에 한 표를 받았다. Maven의 `<dependencyManagement>`가 Gradle에서 어디로 가는지 정리한 표였다. 거기서 한 줄을 일부러 비워뒀다 — `dependencyManagement → platform()` 그리고 옆에 작은 글씨로 "(자세한 건 5장에서)". 그 자리를 회수할 때가 됐다.

회사에서 Spring Boot 빌드 스크립트를 처음 들춰본 사람은 거의 같은 풍경을 본다. 어떤 프로젝트는 `io.spring.dependency-management` 플러그인을 들고 있고, 어떤 프로젝트는 `dependencies { implementation(platform("...")) }`로 BOM을 적용하고, 어떤 프로젝트는 `gradle/libs.versions.toml`이라는 처음 보는 파일이 루트에 놓여 있다. 셋이 같은 일을 하는 것 같기도 하고, 따로 노는 것 같기도 하다. 그래서 보통은 일단 잘 돌아가는 다른 모듈을 베껴와서 새 모듈을 시작한다. 그렇게 시작한 빌드는 어느 날 의존성 하나의 버전을 올리고 싶을 때 어디를 만져야 할지 갑자기 막막해진다. 난감한 일이다.

이 장에서 풀고 싶은 매듭이 바로 그것이다. **BOM과 Catalog, 둘이 같은 일을 하는 건가, 다른 일을 하는 건가.** 그리고 `io.spring.dependency-management` 플러그인은 그 사이 어디에 서 있는가.

## 굵은 메시지 — BOM은 resolution, Catalog는 declaration, 둘은 직교한다

먼저 척추부터 박아두자. 이 장의 모든 박스와 코드 예제가 이 한 줄을 떠받친다.

**BOM은 의존성을 어떻게 "해결(resolve)"할지에 관여하고, Version Catalog는 의존성을 어떻게 "선언(declare)"할지에 관여한다. 둘은 직교한다. 둘 다 쓴다.**

조금 풀어보자. BOM(Bill of Materials)은 "이 라이브러리들이 함께 동작하도록 검증된 버전 묶음"이다. Spring Boot가 제공하는 `spring-boot-dependencies` BOM에는 수백 개의 의존성 좌표와 정확한 버전이 박혀 있다. 우리가 `spring-boot-starter-web`을 끌어오면 그 안에 또 다른 starter가 딸려오고, 거기에 또 다른 라이브러리가 딸려온다. 이렇게 transitive로 끌려나온 수십~수백 개의 라이브러리들이 서로 충돌하지 않을 버전 조합을 누군가는 정렬해줘야 한다. 그 일을 하는 게 BOM이다. **BOM은 resolution 시점에 작동한다.**

반면 Version Catalog는 `gradle/libs.versions.toml`이라는 단일 파일에 의존성 좌표와 버전을 모아두는 도구다. build.gradle.kts에서는 `libs.spring.boot.starter.web` 같은 짧은 별칭으로 그 좌표를 참조한다. **Catalog는 declaration 시점에 작동한다 — 빌드 스크립트가 평가되기 전에 끝나는 일이다.** transitive 충돌을 정리해주지 않는다. 단지 "여기 한 곳에 의존성 명세가 모여 있다"는 사실만 보장한다.

그래서 둘은 한쪽이 다른 쪽을 대체하지 않는다. Catalog 하나만 쓰면 transitive 버전 정합성이 깨질 수 있고, BOM 하나만 쓰면 build script 곳곳에 의존성 좌표가 흩어진 채로 남는다. **둘을 같이 쓴다. Catalog가 BOM 좌표를 보관하고, build script에서는 `platform(libs.spring.boot.bom)`으로 그 BOM을 끌어와 transitive를 정렬한다.** 이 한 문장이 이 장의 결론이다. 나머지는 그걸 받쳐주는 디테일이다.

## declarable configuration의 정체

본격적으로 들어가기 전에 한 가지를 정리하자. Spring Boot 빌드 스크립트에서 거의 매번 마주치는 `implementation`, `testImplementation` 같은 단어들 — 이게 정확히 무엇인가.

Gradle에서 의존성은 항상 **configuration**에 붙여서 선언한다. 2장에서 Configuration이 declarable/resolvable/consumable 세 역할로 나뉜다고 했는데, 우리가 `dependencies {}` 블록에서 쓰는 것들이 바로 declarable configuration이다. "이 의존성이 어떤 용도로 필요한가"를 Gradle에게 알려주는 통로다. java 플러그인(과 그 뒤에 따라오는 `java-library`, `application`, Spring Boot 플러그인 등)이 표준 declarable 묶음을 만들어 준다.

> **박스 — declarable configuration 5형제와 Spring Boot의 추가 분**
>
> `java` 플러그인이 만들어주는 declarable configuration 5개를 정확히 짚어두자.
>
> - **`implementation`** — 컴파일과 런타임 둘 다 필요. 소비자(consumer)에게는 노출되지 않는다. 캡슐화된다. **기본 선택지다.**
> - **`api`** — public API 표면에 등장하는 타입에만 사용한다. 소비자에게도 컴파일 타임에 노출된다. **`java-library` 플러그인을 적용한 모듈에서만 존재한다.** application 모듈은 보통 `java` plugin이므로 `api`라는 단어 자체가 없다.
> - **`compileOnly`** — 컴파일 타임에만 필요. 런타임 classpath와 jar에는 들어가지 않는다. annotation processor의 호출 인터페이스, Lombok, servlet-api처럼 컨테이너가 제공하는 라이브러리.
> - **`runtimeOnly`** — 런타임에만 필요. 컴파일 시점에 직접 import하지 않는 구현체. JDBC 드라이버가 전형적인 예다.
> - **`annotationProcessor`** — compile 시점에만 동작하는 processor. compile/runtime classpath에서 완전히 분리된다. `spring-boot-configuration-processor`가 여기에 들어간다.
>
> Spring Boot 플러그인을 적용하면 여기에 세 가지가 더 붙는다.
>
> - **`developmentOnly`** — 실행 가능한 jar/war에서 제외된다. `spring-boot-devtools`의 자리.
> - **`testAndDevelopmentOnly`** — 테스트와 dev 모드에서만 들어간다.
> - **`productionRuntimeClasspath`** — dev/test를 제외한 운영 런타임 classpath. `bootJar`가 패키징할 때 이것을 참조한다.
>
> 각각의 이름이 곧 의미다. 이름이 의미하는 그대로의 시점에만 의존성이 살아 있다.

이 5형제 + Spring Boot 3형제, 합쳐 8개로 거의 모든 일을 해낼 수 있다. 그런데 그중에서도 `implementation`과 `api`의 구분만큼은 한 번 더 짚어둘 필요가 있다.

> **박스 — implementation vs api**
>
> 우리가 라이브러리 모듈을 만든다고 해보자. 그 모듈의 public 메서드 시그니처에 어떤 외부 라이브러리의 타입이 등장한다고 치자 — 예를 들어 `fun process(req: HttpRequest): HttpResponse` 같은 식이다. 그러면 이 모듈을 쓰는 소비자 모듈도 컴파일 시점에 그 HttpRequest/HttpResponse 타입을 알아야 한다. 이때만 `api`를 쓴다. 이렇게 노출이 필요한 의존성은 `api`로 선언해야 소비자도 그 타입에 접근할 수 있다.
>
> 그런데 우리가 그 라이브러리를 메서드 시그니처에는 안 쓰고, 함수 안쪽에서만 쓴다면? `api` 대신 `implementation`이어야 한다. 그래야 소비자가 그 라이브러리에 영향받지 않는다.
>
> 이 구분이 왜 그렇게 중요한가. **`api`로 선언한 의존성의 ABI가 바뀌면 그 모듈을 쓰는 소비자 모두가 재컴파일 대상이 된다.** 멀티 모듈에서 `api` 남용은 사소한 라이브러리 버전 업 하나에 빌드 시간이 폭발하는 결과를 낳는다. 끔찍한 일이다.
>
> 그러니 기본 권장은 단순하다 — **무조건 `implementation`을 먼저 쓰자. 컴파일러가 "타입을 못 찾겠다"고 비명을 지르는 그 의존성만 `api`로 올린다.**
>
> 한 가지 더. `java-library` 플러그인을 적용하지 않으면 `api` 자체가 존재하지 않는다. application 모듈 — 우리의 `ch04-bootapp/`처럼 Spring Boot 앱 그 자체 — 은 보통 `java` plugin만 적용된다. 그러니 거기서는 `api` 고민 자체가 없다. **`api`는 라이브러리 모듈에서만 등장하는 단어다.** 이 책의 8장 이후 멀티 모듈에서 다시 만난다.

자, 이제 의존성을 어떤 configuration에 어떻게 붙이는지가 정리됐다. 다음은 그 의존성의 **버전을 어디서 정하는가** 차례다. 여기서 BOM이 등장한다.

## BOM — 의존성 해결을 강제하는 거푸집

Spring Boot 앱을 만들어보면 의존성을 선언할 때 버전을 거의 안 쓴다는 사실이 눈에 띈다.

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}
```

좌표 끝에 버전이 없다. 그런데도 빌드는 잘 된다. 누군가 이 좌표들의 버전을 뒤에서 정해주고 있다는 뜻이다. 그 누군가가 바로 BOM이다.

Spring Boot의 공식 BOM은 `org.springframework.boot:spring-boot-dependencies` 라는 좌표를 가진다. 이 안에는 수백 개의 좌표와 그에 매칭된 정확한 버전이 들어 있다 — Spring Framework, Jackson, Hibernate, Tomcat, Netty, slf4j, logback, junit... Spring Boot 팀이 한 번씩 릴리스할 때마다 이 모든 라이브러리의 버전 조합을 한 번 정합성 테스트하고 BOM으로 묶어 내보낸다. 그러니 BOM을 적용한다는 건 "이 묶음의 버전 정합성을 통째로 빌려 쓰겠다"는 선언이다.

Gradle에서 BOM을 적용하는 길은 두 가지다.

### 길 (A) `platform()` — Gradle 네이티브, 권장

Gradle이 BOM을 1급으로 지원한다. `platform()` 함수가 그 통로다.

```kotlin
import org.springframework.boot.gradle.plugin.SpringBootPlugin

dependencies {
    implementation(platform(SpringBootPlugin.BOM_COORDINATES))
    implementation("org.springframework.boot:spring-boot-starter-web")
}
```

`platform(...)` 호출에 BOM 좌표를 넘기면 Gradle은 그 좌표를 "직접 의존성"이 아니라 "버전 정렬 정보의 출처"로 받아들인다. transitive까지 포함해 모든 의존성이 그 BOM에 박힌 버전으로 정렬된다. 별도 플러그인이 필요 없고, Configuration Cache와도 정합성 문제가 없다.

`SpringBootPlugin.BOM_COORDINATES`는 Spring Boot Gradle 플러그인이 제공하는 상수다. 현재 적용된 Spring Boot 플러그인의 버전과 동일한 BOM을 항상 가리킨다. 별도로 좌표를 박지 않아도 plugin 블록의 버전과 BOM 버전이 어긋날 일이 없다는 점이 편하다.

### 길 (B) `io.spring.dependency-management` 플러그인

Maven 시절의 `<dependencyManagement>` 경험에 가깝게 만들어진 Spring 진영의 별도 플러그인이다.

```kotlin
plugins {
    id("io.spring.dependency-management") version "1.1.6"
}

dependencyManagement {
    imports {
        mavenBom("org.springframework.boot:spring-boot-dependencies:4.0.6")
    }
}
```

이 플러그인이 `platform()`에 비해 갖는 거의 유일한 장점은 **property 기반 버전 오버라이드**다.

```kotlin
ext["slf4j.version"] = "2.0.13"
```

이 한 줄로 BOM이 정해놓은 slf4j 버전을 부분적으로 덮어쓸 수 있다. Maven `<properties>`에서 `<slf4j.version>`을 오버라이드하던 경험과 거의 동일하다. Maven 출신 팀이 그 경험을 그대로 가져가고 싶다면 자리는 있다.

다만 Spring Boot 공식 Gradle 플러그인 문서는 명시적으로 **"likely result in faster builds"**라며 (A) `platform()` 방식을 권장한다. 이유는 단순하다. (A)는 Gradle 네이티브 메커니즘 위에서 동작하니까 빌드 캐시·Configuration Cache와의 호환이 자연스럽고, (B)는 별도 플러그인을 한 번 거치는 만큼 그 호환을 별도로 관리해야 한다.

### 길 (C) `enforcedPlatform()`은 왜 권장 안 되는가

`platform()`의 변형으로 `enforcedPlatform()`이 있다. 이름이 강해 보여서 "더 강한 platform이니까 더 안전하지 않을까" 싶지만 정반대다.

`platform()`은 BOM이 정한 버전을 "권장(constraint)"으로 적용한다. 다른 의존성 선언이 더 높은 버전을 요구하면 Gradle의 충돌 해결 규칙이 그쪽을 채택한다. 자연스러운 협상이다.

`enforcedPlatform()`은 BOM 버전을 "강제(forced)"한다. 다른 선언이 무엇을 요구하든 BOM 버전으로 못박는다. 결과적으로 Gradle의 conflict resolution 자체를 무력화시킨다. 우리가 명시적으로 어떤 라이브러리를 더 높은 버전으로 끌어올리고 싶을 때조차 BOM 버전으로 끌어내려진다. 그러면 어디서 버전이 정해진 건지 추적이 어려워지고, 충돌 진단도 어려워진다.

이 책의 결론은 단순하다 — **`platform()`을 쓰자. `enforcedPlatform()`은 명확한 이유 없이는 쓰지 말자.**

### 비교 요약

세 가지 길을 한 표로 정리해두자.

| 길 | 메커니즘 | property 오버라이드 | 권장도 | 자리 |
|----|----------|---------------------|---------|------|
| `platform()` | Gradle 네이티브 | 직접 dependency constraint로 | **권장** | 새 프로젝트의 기본 선택 |
| `io.spring.dependency-management` | 별도 플러그인 | `ext["x.version"]`으로 가능 | 선택지 중 하나 | Maven 경험을 그대로 가져가고 싶을 때 |
| `enforcedPlatform()` | Gradle 네이티브 (강제) | 직접 가능 | 비권장 | 거의 안 쓴다 |

이 책은 새로 만드는 빌드 스크립트에서는 (A) `platform()`을 기본으로 가져간다. (B) `io.spring.dependency-management`는 "기존 빌드에 이미 들어 있다면 그대로 둬도 된다, 다만 새로 추가하지는 말자" 정도의 자리에 놓는다. Spring Boot 4.0이 BOM을 자체적으로 잘 제공하기 때문에 별도 플러그인 없이도 부족함이 없다.

> **함정 — 동시 적용 금지**
>
> 가장 흔한 사고가 여기서 일어난다. 누군가 (B) `io.spring.dependency-management` 플러그인을 적용해놓은 빌드에, 다른 누군가가 "더 모던하다"는 이유로 (A) `dependencies { implementation(platform(...)) }`을 추가로 박아넣는 경우다. **두 메커니즘이 같은 BOM을 두 번 적용한다.** 잘 돌아갈 때도 있지만, transitive 충돌이 났을 때 어느 메커니즘이 어느 의존성을 어느 버전으로 정렬한 건지 추적이 사실상 불가능해진다. 빌드가 깨질 때까지 모르고 살다가 어느 날 갑자기 라이브러리 하나 올렸을 뿐인데 `NoSuchMethodError`가 터진다. 진단이 끔찍하다.
>
> **둘 중 하나만 골라라.** 새 프로젝트는 (A). 기존에 (B)가 있다면 (B)로 통일하고 (A)를 빼거나, (B)를 걷어내고 (A)로 통일하거나. 어느 쪽으로 통일해도 좋지만 동시 적용은 피하자.

## Version Catalog — 의존성 선언의 단일 출처

여기까지가 BOM 이야기였다. 이제 Catalog 차례다. 다시 한번 척추 메시지 — BOM은 resolution, Catalog는 declaration. 둘은 직교한다.

`gradle/libs.versions.toml` 파일이 Catalog의 자리다. 이름과 위치가 고정돼 있다. Gradle이 그 위치에 있는 파일을 자동으로 인식하고, `libs`라는 type-safe accessor를 build script에 노출한다.

전형적인 모습은 이렇다.

```toml
# gradle/libs.versions.toml

[versions]
spring-boot = "4.0.6"
kotlin = "2.2.0"
junit = "5.11.4"

[libraries]
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web", version.ref = "spring-boot" }
spring-boot-starter-data-jpa = { module = "org.springframework.boot:spring-boot-starter-data-jpa", version.ref = "spring-boot" }
spring-boot-starter-test = { module = "org.springframework.boot:spring-boot-starter-test", version.ref = "spring-boot" }
spring-boot-bom = { module = "org.springframework.boot:spring-boot-dependencies", version.ref = "spring-boot" }
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }

[bundles]
spring-web = ["spring-boot-starter-web", "spring-boot-starter-data-jpa"]

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }
```

네 개의 섹션이 있다.

- **`[versions]`** — 버전 문자열의 모음. 별칭(`spring-boot`, `kotlin`...) 하나에 버전 하나.
- **`[libraries]`** — 라이브러리 좌표의 모음. `version.ref`로 위쪽 `[versions]`의 별칭을 참조한다. 하나의 버전을 여러 좌표가 공유할 수 있다 — `spring-boot-starter-*` 셋이 모두 `spring-boot` 버전을 공유하듯이.
- **`[bundles]`** — 자주 같이 쓰이는 라이브러리들을 한 묶음으로. 위 예시의 `spring-web`은 starter-web과 starter-data-jpa를 한 번에 끌어온다.
- **`[plugins]`** — Gradle 플러그인의 id와 버전. `[libraries]`와 따로 살아 있는 섹션이다.

build.gradle.kts에서 이 catalog는 `libs`라는 이름으로 참조된다.

```kotlin
plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.spring.boot)
}

dependencies {
    implementation(platform(libs.spring.boot.bom))
    implementation(libs.bundles.spring.web)
    testImplementation(libs.spring.boot.starter.test)
}
```

몇 가지를 같이 짚어두자.

**플러그인은 `alias(libs.plugins.X)`로 적용한다.** 일반적인 `id("...") version "..."` 형식 대신 alias 함수를 쓴다. 이러면 plugin id와 버전이 catalog의 `[plugins]` 섹션에서 단일하게 관리된다.

**TOML의 dash(`-`)는 Kotlin DSL의 dot(`.`)으로 변환된다.** `spring-boot-starter-web`이 catalog에 적혀 있으면 build.gradle.kts에서는 `libs.spring.boot.starter.web`으로 접근한다. 일종의 nested 구조처럼 보이지만 실제로는 단순 변환이다.

**bundle은 여러 의존성을 한 번에 끌어오는 단축이다.** `libs.bundles.spring.web` 한 줄이 starter-web과 starter-data-jpa 두 줄을 대신한다. 같이 쓰이는 의존성이 정해져 있다면 묶어두면 좋다.

**Dependabot이 `libs.versions.toml`을 읽는다.** GitHub의 Dependabot이 이 파일의 형식을 정식으로 지원한다. PR로 라이브러리 버전 업데이트가 자동으로 올라온다. catalog를 쓰는 이유 중 무시할 수 없는 부분이다.

> **함정 — `extra` 변수는 버려라**
>
> 옛 Spring Boot 빌드 스크립트에서 자주 보던 패턴이다.
>
> ```kotlin
> extra["springBootVersion"] = "3.2.0"
> extra["kotlinVersion"] = "1.9.20"
>
> dependencies {
>     implementation("org.springframework.boot:spring-boot-starter-web:${extra["springBootVersion"]}")
> }
> ```
>
> `extra`(또는 `ext`) 변수에 버전 문자열을 박아두고 의존성 좌표에서 문자열 보간으로 끌어다 쓴다. 한때는 이게 "버전을 한 곳에서 관리하는" 정답처럼 보였다. 지금은 아니다.
>
> 이 방식은 **타입 안전성이 없다.** 오타를 내면 런타임에 빌드 시점에야 알게 된다. IDE 자동완성도 없다. Dependabot이 못 읽는다. 멀티 모듈에서 자동 공유도 안 된다 — root에서 정의하면 subproject가 일일이 끌어다 써야 한다.
>
> **Version Catalog가 이 모든 단점을 정확히 풀어준다.** 새로 시작하는 프로젝트에서 `extra["..."]`로 버전을 관리하는 패턴은 그냥 버리자. 기존 빌드에 박혀 있다면 마이그레이션 우선순위에 올려두자.

## 둘을 같이 쓴다 — 정석 build.gradle.kts

이제 약속한 자리다. BOM과 Catalog를 같이 쓰는 모습을 한 파일로 보자. 4장에서 만든 `ch04-bootapp/`에 Version Catalog를 도입하고 `platform(libs.spring.boot.bom)`을 적용한 결과다.

```toml
# ch04-bootapp/gradle/libs.versions.toml

[versions]
spring-boot = "4.0.6"
kotlin = "2.2.0"

[libraries]
spring-boot-bom = { module = "org.springframework.boot:spring-boot-dependencies", version.ref = "spring-boot" }
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web" }
spring-boot-starter-data-jpa = { module = "org.springframework.boot:spring-boot-starter-data-jpa" }
spring-boot-starter-test = { module = "org.springframework.boot:spring-boot-starter-test" }
spring-boot-devtools = { module = "org.springframework.boot:spring-boot-devtools" }
spring-boot-configuration-processor = { module = "org.springframework.boot:spring-boot-configuration-processor" }

[bundles]
spring-web = ["spring-boot-starter-web", "spring-boot-starter-data-jpa"]

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
spring-dependency-management = { id = "io.spring.dependency-management", version = "1.1.6" }
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }
kotlin-spring = { id = "org.jetbrains.kotlin.plugin.spring", version.ref = "kotlin" }
```

starter 좌표에 `version.ref`가 없다는 점을 눈여겨보자. **버전을 catalog의 `[libraries]`에 적지 않았다.** 버전 정렬은 BOM에게 맡길 것이기 때문이다.

build.gradle.kts는 이렇게 짧아진다.

```kotlin
// ch04-bootapp/build.gradle.kts

plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.kotlin.spring)
    alias(libs.plugins.spring.boot)
}

group = "com.example.shop"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    // BOM — transitive 버전을 정렬한다 (resolution)
    implementation(platform(libs.spring.boot.bom))

    // 좌표만 — 버전은 위 BOM이 정한다 (declaration)
    implementation(libs.bundles.spring.web)
    developmentOnly(libs.spring.boot.devtools)
    annotationProcessor(libs.spring.boot.configuration.processor)
    testImplementation(libs.spring.boot.starter.test)
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

`implementation(platform(libs.spring.boot.bom))` 한 줄이 척추 메시지의 결정적 증명이다. **catalog가 BOM 좌표를 보관(declaration)하고, build script에서 `platform()`으로 그 BOM을 끌어와 transitive를 정렬(resolution)한다.** 둘이 직교한 채로 함께 동작한다.

스크립트 본문에 버전 문자열이 단 하나도 없다는 점도 보자. 모든 버전은 catalog로 모였고, transitive는 BOM이 책임진다. 빌드 스크립트는 "무엇을 쓰겠다"만 선언한다. "어느 버전으로 풀어낼지"는 한 곳에서만 정한다. 이게 우리가 노린 모양이다.

`io.spring.dependency-management` 플러그인은 보다시피 catalog `[plugins]`에 등록만 해두고 build script에 적용하지 않았다. Spring Boot 4.0 BOM이 충분하기 때문에 굳이 별도 플러그인을 거칠 필요가 없다. 회사 빌드에 기존 코드가 의존성을 property로 오버라이드한다면 그때 가서 적용을 고민하면 된다.

## 의존성을 디버깅한다

여기까지 잘 갖춰놓아도 어느 날 빌드는 사고를 친다. transitive에서 끌려온 어떤 라이브러리의 버전이 예상과 다르거나, BOM이 정렬해주지 못한 라이브러리가 충돌하거나, `NoSuchMethodError`가 런타임에 터진다. 그럴 때 어디서부터 들여다봐야 할까. 이 자리의 도구 세 가지를 한 박스에 묶어두자.

> **박스 — 의존성 그래프 디버깅 도구 3종**
>
> 빌드가 의존성 문제로 막혔을 때 가장 먼저 닿는 명령들이다.
>
> **1) `:dependencies` — 전체 그래프를 본다.**
> ```bash
> ./gradlew :app:dependencies --configuration runtimeClasspath
> ```
> 특정 configuration의 의존성 트리를 통째로 출력한다. Spring Boot 앱은 runtimeClasspath가 가장 자주 쓰인다. `compileClasspath`, `testRuntimeClasspath` 등으로 바꿔가며 본다. configuration을 지정하지 않으면 모든 configuration이 한꺼번에 쏟아지니, 거의 항상 `--configuration`을 같이 쓰는 편이 낫다.
>
> **2) `dependencyInsight` — 특정 라이브러리의 출처를 추적한다.**
> ```bash
> ./gradlew :app:dependencyInsight --dependency slf4j --configuration runtimeClasspath
> ```
> "slf4j가 왜 1.7.36이 아니라 2.0.13으로 풀려 있는가"를 정확히 답해준다. 어디서 요청됐고, 어느 BOM이 어느 버전으로 정렬했고, 충돌이 어떻게 해결됐는지를 트리로 보여준다. **버전 미스터리에 빠지면 거의 무조건 이 명령으로 시작한다.**
>
> **3) `--scan` — Build Scan으로 전체를 본다.**
> ```bash
> ./gradlew build --scan
> ```
> 빌드 결과를 Gradle이 호스팅하는 Build Scan 페이지로 업로드한다. URL이 콘솔에 찍힌다. 그 페이지에서 의존성 그래프, task 타임라인, configuration 정보, 캐시 통계까지 한꺼번에 본다. 콘솔 출력만으로는 추적이 안 되는 transitive 충돌을 시각적으로 풀어준다. 자세한 활용은 14장에서 CI 통합과 함께 다시 본다.
>
> 이 세 가지를 손에 익혀두자. 의존성 사고가 났을 때 막연한 두려움이 명령 한 줄로 줄어든다.

가끔은 BOM이 정렬해주지 않거나, 정렬해줬는데도 transitive로 끌려온 어떤 라이브러리가 우리가 원하는 버전과 안 맞을 때가 있다. 그럴 때의 마지막 처방이 resolution strategy다.

> **박스 — Resolution Strategy 마지막 처방**
>
> BOM으로도 못 잡히는 transitive를 마지막으로 강제하는 도구다. 사용 자체가 신호 — "여기서 정상적인 메커니즘이 풀어주지 못한 충돌이 있다"는 표시다.
>
> ```kotlin
> configurations.all {
>     resolutionStrategy.eachDependency {
>         if (requested.group == "org.slf4j") {
>             useVersion("2.0.13")
>             because("CVE-2023-XXXXX 회피")
>         }
>     }
> }
> ```
>
> `configurations.all { ... }` 안의 `resolutionStrategy.eachDependency`는 모든 의존성을 검사할 기회를 우리에게 준다. 조건에 맞는 의존성에 `useVersion()`으로 버전을 강제하고, `because()`로 강제한 이유를 남긴다. `because()`는 빌드가 출력하는 메시지에 그대로 노출되기 때문에 미래의 누군가(아마 미래의 우리)에게 친절한 흔적이 된다.
>
> 다만 이 도구는 **마지막 처방**이다. 가능하면 BOM의 버전 조합으로 해결하고, 그게 어려운 라이브러리에만 적용하자. resolution strategy가 빌드 스크립트 곳곳에 깔리기 시작하면 의존성 정합성이 어디서 결정되는지 추적이 어려워진다.

## 5장을 닫으며

척추 메시지를 한 번만 더 박아두자. **BOM은 resolution, Catalog는 declaration, 둘은 직교한다. 둘 다 쓴다.** 이 한 줄이 우리가 5장 내내 풀어낸 매듭이다.

`io.spring.dependency-management` 플러그인은 우리의 새 빌드에 들어가지 않았다. 강요해서 빼는 게 아니라, Spring Boot 4.0 BOM을 `platform()`으로 직접 끌어오는 것만으로 충분히 잘 동작해서다. 회사 빌드에 이미 들어 있는 경우엔 굳이 빼지 않아도 좋다. 다만 **`platform()`과 동시에 적용하지 않는다는 규칙만 지키자.** 두 메커니즘이 같은 BOM을 두 번 적용하는 사고가 가장 흔한 함정이다.

`ch04-bootapp/` 폴더의 모습이 한 단계 자랐다. `gradle/libs.versions.toml`이 루트에 생겼고, build.gradle.kts에서는 버전 문자열이 사라졌다. 의존성 선언은 catalog가 보관하고, transitive 정렬은 BOM이 책임진다. 빌드 스크립트가 비로소 "선언적"이라는 단어에 어울리는 모습이 됐다.

이제 다음 의문이 자연스럽게 떠오른다. `plugins { alias(libs.plugins.spring.boot) }` — 이 한 줄이 정확히 무엇을 한 건가? Spring Boot 플러그인을 적용한 순간 `bootJar`, `bootRun`, `bootBuildImage` 같은 task가 줄줄이 생긴다. 어떤 task가 생기는지, 그게 정확히 무엇을 만드는지, `bootJar`가 만드는 fat jar의 내부는 어떻게 생겼는지, 그리고 Spring Boot 3.x에서 4.x로 올라올 때 그 안에서 무엇이 바뀌었는지. 6장에서 그 안쪽을 들여다보자. 우리의 `ch04-bootapp/`이 진짜로 실행 가능한 fat jar와 OCI 이미지까지 만들어내는 모습을 함께 본다.
