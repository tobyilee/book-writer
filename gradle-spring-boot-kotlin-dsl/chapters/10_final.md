# 10장. Convention Plugin으로 build logic을 모듈화한다

9장의 끝에서 우리는 한숨을 돌렸다. `:domain`이 빈 jar를 내놓던 사고가 풀렸고, `./gradlew :app:bootRun`이 드디어 정상으로 떨어졌다. `:app`만 Spring Boot 플러그인을 받고, `:domain`·`:order`·`:payment`는 library로 정리됐다. 빌드는 된다.

그런데 정리된 네 모듈의 build.gradle.kts를 나란히 띄워놓고 보면 마음 한쪽이 찜찜하다. 비슷한 모습을 한 파일이 네 개나 있다.

```kotlin
// domain/build.gradle.kts
plugins {
    `java-library`
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

dependencies {
    implementation(platform("org.springframework.boot:spring-boot-dependencies:4.0.6"))
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.withType<Test>().configureEach {
    useJUnitPlatform()
}
```

`:order`, `:payment`도 거의 똑같다. 어디는 의존성 한 줄만 다르고, 어디는 그마저도 똑같다. `:app`도 `java-library` 대신 `org.springframework.boot`가 들어왔을 뿐 toolchain 블록과 `useJUnitPlatform()`은 그대로 복사돼 있다.

여기서 한 번 상상해보자. 회사에서 JDK 21을 22로 올리기로 했다. 그러면 우리는 네 파일을 열어서 `21`을 `22`로 바꾼다. 또는 BOM 버전이 4.0.6에서 4.0.7로 올라간다. 네 파일을 또 연다. 또는 새로 `:catalog` 모듈을 하나 더 추가한다. 그러면 이 똑같은 블록을 다섯 번째로 복사한다. 한 곳에서 결정해야 할 사실이 네 곳, 다섯 곳에 흩어져 있다는 건 어딘가에서 사고가 날 시간문제라는 뜻이다.

그렇다면 어떻게 해야 할까? Maven을 써본 사람은 본능적으로 한 가지 떠올린다. parent pom. 부모에 공통을 적고 자식들은 부모를 가리키기만 한다. Gradle에도 그런 자리가 있을까? 있다. 그리고 그 자리의 이름은 **convention plugin**이다.

이번 장에서는 8장·9장에서 정리된 4개 모듈의 build.gradle.kts가 각각 **한 줄짜리 plugin 선언으로** 줄어드는 과정을 함께 본다. `ch09-convention/` 폴더에서 동작하는 코드다. 빌드는 9장과 똑같이 잘 되지만, 빌드 스크립트가 비로소 "선언" 같은 모습이 된다.

## 그런데 왜 `subprojects {}`가 아닌가

여기서 잠깐 멈춰야 한다. Gradle을 조금 써본 사람이라면 8장 후반에서 본 `subprojects {}` 박스를 떠올리고 이렇게 말할지도 모른다. "그냥 루트 build.gradle.kts에서 `subprojects { java { toolchain { ... } } }` 한 번 적으면 끝 아닌가?"

코드로 보면 더 매혹적이다.

```kotlin
// 루트 build.gradle.kts — 안티패턴
subprojects {
    apply(plugin = "java")
    java {
        toolchain {
            languageVersion = JavaLanguageVersion.of(21)
        }
    }
    tasks.withType<Test>().configureEach {
        useJUnitPlatform()
    }
    dependencies {
        "implementation"(platform("org.springframework.boot:spring-boot-dependencies:4.0.6"))
    }
}
```

된다. 적어도 빌드 자체는 된다. 그래서 한국어 검색으로 멀티 모듈 예제를 찾으면 절반은 이 모습이다. 그런데 Gradle 공식 문서는 이 패턴을 명시적으로 **안티패턴**이라고 적고 있다. configuration-time coupling을 만들고, 로직의 출처를 가린다는 표현이 그대로 들어 있다. 이게 어떤 뜻일까. 세 가지 구체적인 문제로 풀어보자.

> **함정 — `subprojects {}`가 일으키는 세 가지 사고**
>
> **1) configuration-time coupling.** 루트의 `subprojects {}` 블록은 모든 서브프로젝트의 configuration phase에 끼어든다. `:domain` 하나만 만지고 싶어도 Gradle은 루트의 코드를 평가하기 위해 `:order`·`:payment`까지 다 깨워야 한다. 단일 모듈만 빌드하는 빠른 길이 사라진다. 모듈이 늘어날수록 이 비용은 곱셈으로 늘어난다.
>
> **2) IDE 추적 불가.** `:order`의 build.gradle.kts를 열어 `useJUnitPlatform()`이 어디서 적용됐는지 IntelliJ에서 Cmd+클릭으로 따라가보자. 따라갈 곳이 없다. 이 설정은 `:order` 파일 어디에도 적혀 있지 않다. 루트의 `subprojects {}` 안에 숨어 있고, IDE는 그 사실을 모른다. 새 팀원이 들어왔을 때 "이 toolchain 설정은 어디서 오는 거예요?"라는 질문에 누군가가 매번 답해줘야 한다. 빌드의 출처가 사람의 기억에 의존하는 순간 신뢰는 무너진다.
>
> **3) Configuration Cache 친화성 ↓.** 13장에서 본격적으로 만날 Configuration Cache는 프로젝트 간 격리를 좋아한다. `subprojects {}`는 정의상 격리를 깨는 코드다. 루트가 모든 서브프로젝트의 상태에 손을 댄다. Configuration Cache를 켰을 때 위반 메시지가 쏟아지는 패턴 중 가장 흔한 것이 cross-project configuration이다. 미래의 자신을 위해서라도 이 패턴은 피하자.
>
> 정리하자면, `subprojects {}`는 동작은 하지만 빌드를 **불투명한 덩어리**로 만든다. 우리는 빌드를 더 명시적이고, 더 추적 가능하고, 더 도구 친화적인 방향으로 키워야 한다.

이제 답이 분명해진다. 공통 build logic은 **그 logic을 적용받는 각 build.gradle.kts에 명시적으로 적용되어야 한다.** 다만 logic 자체는 한 곳에서만 정의한다. 이게 convention plugin이 푸는 문제다.

한 가지 덧붙여두자. 같은 안티패턴을 살짝 부드럽게 만든 변형이 있다 — root build.gradle.kts에 `configure(subprojects.filter { ... }) { ... }` 같은 형태로 일부 모듈에만 cross-project configuration을 거는 패턴이다. 외형은 더 정교해 보이지만 근본은 같다. 빌드 출처를 가리고, configuration coupling을 만들고, IDE 추적을 깬다. 정교해진 코드가 더 깊이 숨는 효과까지 더해질 뿐이다. 한국어 자료에서 흔하게 보이지만 권장할 패턴은 아니다.

## 답은 precompiled convention plugin이다

Gradle은 plugin을 정의하는 길을 세 가지 제공한다. 2장에서 짧게 봤다. binary plugin, script plugin, 그리고 precompiled convention plugin. 셋 중에서 우리가 지금 원하는 것은 세 번째다.

precompiled convention plugin의 정의는 이름이 다 말해준다. "미리 컴파일된 스크립트 플러그인". 우리는 평소 build.gradle.kts에 적는 것과 똑같은 코드를 별도의 `*.gradle.kts` 파일에 적는다. Gradle은 이 파일을 빌드 시점에 진짜 plugin으로 컴파일한다. 그리고 **파일 이름이 그대로 plugin id가 된다.** `shop.java-conventions.gradle.kts`라는 파일을 만들면 `id("shop.java-conventions")`로 적용할 수 있는 plugin이 자동으로 생긴다.

이게 왜 깔끔한가. 첫째, 이미 익숙한 build.gradle.kts 문법을 그대로 쓴다. 새로 배워야 할 클래스 계층이 없다. 둘째, 적용 측에서는 `plugins { id("shop.java-conventions") }` 한 줄로 끝난다. IDE에서 그 plugin id를 Cmd+클릭하면 정확히 정의된 파일로 점프한다. 출처가 명시적이다. 셋째, Gradle 9.x에서 가장 잘 다듬어진 권장 방식이다. 공식 문서 §implementing_gradle_plugins_precompiled에 명시적으로 "현행 권장"이라고 적혀 있다.

자, 그러면 만들어보자.

## `buildSrc/`를 세운다

precompiled convention plugin이 살 자리가 있다. **`buildSrc/`라는 이름의 특별한 디렉터리**다. Gradle은 프로젝트 루트에 `buildSrc/` 폴더가 있으면 그것을 자동으로 빌드의 일부로 받아들인다. 별도의 settings.gradle.kts를 적지 않아도 된다. 별도로 `include("buildSrc")`라고 선언하지 않아도 된다. 폴더 이름이 곧 규칙이다.

`buildSrc/`의 구조는 의외로 단순하다.

```
shop/
├── settings.gradle.kts
├── build.gradle.kts
├── app/
├── domain/
├── order/
├── payment/
└── buildSrc/
    ├── build.gradle.kts
    └── src/main/kotlin/
        ├── shop.java-conventions.gradle.kts
        └── shop.spring-boot-conventions.gradle.kts
```

먼저 `buildSrc/build.gradle.kts`를 적는다. 이 파일은 우리의 convention plugin들이 **컴파일되기 위해 필요한 환경**을 설정한다.

```kotlin
// buildSrc/build.gradle.kts
plugins {
    `kotlin-dsl`
}

repositories {
    gradlePluginPortal()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-gradle-plugin:4.0.6")
}
```

세 줄짜리 의미를 차분히 풀어보자.

**`kotlin-dsl` 플러그인.** Kotlin DSL로 적힌 `*.gradle.kts` 파일들을 Gradle plugin으로 컴파일해주는 마법의 플러그인이다. 이 한 줄이 `src/main/kotlin/` 아래의 `*.gradle.kts` 파일들을 자동으로 plugin으로 변환한다. `kotlin-dsl` 자체가 Kotlin 컴파일 환경, Gradle API 의존성, plugin id 자동 등록까지 다 묶어준다. 우리가 손으로 챙길 게 거의 없다.

**`gradlePluginPortal()` 저장소.** `kotlin-dsl`이 의존하는 Kotlin 컴파일러 플러그인과, 우리가 곧 가져올 Spring Boot Gradle 플러그인을 받아오는 자리다. `mavenCentral()`이 아니라 plugin portal인 점에 주의하자. plugin들은 portal에서 받는다.

**Spring Boot Gradle 플러그인의 jar.** 이 줄이 가장 헷갈리는 부분이다. 왜 우리가 직접 만드는 convention plugin이 Spring Boot 플러그인 jar를 **implementation 의존성으로** 가지고 있어야 할까? 답: 우리의 convention plugin은 `id("org.springframework.boot")`를 적용할 예정이다. Gradle이 이 plugin id를 컴파일 시점에 찾으려면 해당 plugin의 jar가 buildSrc의 classpath에 올라가 있어야 한다. 다시 말해, **convention plugin은 자기가 다시 적용할 plugin들의 jar를 모두 buildSrc의 의존성으로 가져와야 한다.** 처음엔 어색하지만 한 번 익으면 자연스럽다. "이 jar들이 plugin을 컴파일하기 위한 재료다"라고 생각하자.

여기까지 적으면 `buildSrc/`라는 작은 빌드의 환경이 갖춰졌다. 이제 그 안에서 우리의 첫 convention plugin을 만든다.

## 첫 convention plugin — `shop.java-conventions`

`buildSrc/src/main/kotlin/shop.java-conventions.gradle.kts` 파일을 만든다. 이 파일에 적는 코드는 평범한 build.gradle.kts 그 자체다. 별도의 클래스 선언도, `Plugin<Project>` 같은 인터페이스 구현도 없다. 그냥 build.gradle.kts처럼 적는다.

```kotlin
// buildSrc/src/main/kotlin/shop.java-conventions.gradle.kts
plugins {
    `java-library`
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

tasks.withType<Test>().configureEach {
    useJUnitPlatform()
}
```

다 봤다. 9장의 `:domain`·`:order`·`:payment` build.gradle.kts에 똑같이 들어가던 그 블록이다. `java-library` plugin 적용, toolchain 21, `useJUnitPlatform()`. 이게 그대로 한 파일로 묶였다.

여기에 한 가지 매직이 있다. **파일 이름이 plugin id가 된다.** `shop.java-conventions.gradle.kts`라는 이름은 곧 `shop.java-conventions`라는 plugin id를 낳는다. 점이 들어간 prefix(`shop.`)는 plugin id의 namespace 역할을 한다. 회사 또는 프로젝트 이름을 prefix로 두는 것이 관습이다. 이렇게 적어두면 적용 측에서는 이렇게 쓴다.

```kotlin
// domain/build.gradle.kts
plugins {
    id("shop.java-conventions")
}
```

이 한 줄이 `java-library` 적용, toolchain 설정, `useJUnitPlatform()`까지 모두 끌어온다. 그리고 IntelliJ에서 이 plugin id를 Cmd+클릭하면 정확히 `shop.java-conventions.gradle.kts` 파일이 열린다. 출처가 명시적이고, 추적 가능하고, 도구 친화적이다.

한 가지 작은 디테일을 짚어두자. `plugins {}` 블록 안에 `java-library`가 backtick 둘러싸인 모습으로 들어가 있다. `` `java-library` ``. 이건 Kotlin DSL에서 type-safe accessor를 호출하는 단축 문법이다. 그 자리는 `id("java-library")`라고 적어도 똑같이 동작한다. 어느 쪽이든 동등하니 회사 컨벤션에 맞춰 쓰면 된다. 점 없는 core plugin들(`java`, `java-library`, `application`)은 backtick 형태가 좀 더 간결하고, 점이 들어간 외부 plugin id들은 `id("...")` 형태가 자연스럽다.

## 두 번째 convention plugin — Spring Boot와 BOM을 묶는다

`:app`은 추가로 Spring Boot 플러그인을 적용하고, 모든 모듈이 BOM을 받는다. 이걸 어떻게 묶을까. 자연스러운 답: 두 번째 convention plugin을 만든다. 이름은 `shop.spring-boot-conventions`로 한다.

```kotlin
// buildSrc/src/main/kotlin/shop.spring-boot-conventions.gradle.kts
plugins {
    id("shop.java-conventions")
    id("org.springframework.boot")
}

dependencies {
    "implementation"(platform("org.springframework.boot:spring-boot-dependencies:4.0.6"))
}
```

여기서 두 가지 흥미로운 일이 동시에 일어난다.

첫째, **convention plugin이 다른 convention plugin을 적용한다.** `plugins {}` 블록 안에 `id("shop.java-conventions")`라고 적었다. 즉 `shop.spring-boot-conventions`를 적용하는 모듈은 `shop.java-conventions`도 자동으로 같이 받는다. toolchain·`useJUnitPlatform()`이 따라온다. 한 곳에 정의한 규칙이 합성된다. 이건 Maven의 parent pom 한 단계보다 더 유연하다. parent는 하나만 가질 수 있지만, convention plugin은 필요한 만큼 조합할 수 있다.

둘째, `dependencies {}` 블록 안에 갑자기 큰따옴표가 등장했다. `"implementation"(platform(...))`. 책 전체에서 우리는 Kotlin DSL의 타입 안전성을 자랑해왔는데 여기서 갑자기 문자열이 나타난다. 이게 오타가 아니다. 일부러 이렇게 쓴다. 다음 박스에서 정면으로 풀어보자.

> **박스 — 왜 여기서 갑자기 string이 나오는가**
>
> 3장에서 우리는 Kotlin DSL의 핵심 매력 중 하나로 **type-safe accessor**를 들었다. `implementation("...")`, `testImplementation("...")` 같은 함수가 빌드 스크립트 안에서 자동으로 생긴다. 그런데 그 자동 생성에는 한 가지 전제가 있었다. "**해당 accessor를 만들어주는 plugin이 이미 적용된 상태여야 한다**"는 것.
>
> 예를 들어 `implementation`이라는 함수는 `java` 또는 `java-library` plugin이 적용된 뒤에야 생긴다. 그 plugin이 `implementation`이라는 이름의 configuration을 등록하고, Kotlin DSL이 그 시점 이후의 코드를 컴파일할 때 type-safe accessor를 만들어 끼워넣는다.
>
> 그런데 우리가 지금 적고 있는 `shop.spring-boot-conventions.gradle.kts`는 **plugin 그 자체**다. 이 파일이 컴파일되는 시점에 `java` plugin은 아직 적용된 상태가 아니다. plugin은 자기를 적용받는 모듈마다 다른 순간에 깨어난다. precompiled plugin을 컴파일하는 시점은 그보다 훨씬 이르다. 컴파일러는 `implementation`이라는 type-safe accessor를 만들 근거가 없다. 그래서 그 함수는 존재하지 않는다.
>
> 그 자리를 메우는 게 **string fallback**이다. Gradle은 어떤 시점에서도 `"implementation"(...)`처럼 configuration의 이름을 문자열로 받는 형태의 API를 제공한다. 이 형태는 plugin이 아직 적용되지 않은 시점에도 동작한다. Gradle은 빌드가 실제로 돌아갈 때 "implementation"이라는 이름의 configuration이 있으면 거기에 의존성을 추가하고, 없으면 에러를 던진다.
>
> 그래서 convention plugin 안에서 의존성 declaration은 거의 항상 string-receiver를 쓴다. 한 번 익어두면 헷갈리지 않는다. **"여기는 type-safe accessor가 노출되기 이전 시점이다"**라는 신호로 받아들이자. 적용 측 build.gradle.kts에서는 여전히 우리가 사랑하는 `implementation("...")`을 그대로 쓰면 된다. 그쪽은 plugin이 이미 적용된 상태이기 때문이다.
>
> 한 가지 더. `plugins { id("org.springframework.boot") }`처럼 다른 plugin 적용은 type-safe 형태로 적을 수 있다. plugin id 자체는 컴파일 시점에 알려져 있기 때문이다. 즉 **plugin은 type-safe, configuration accessor는 string fallback** — 이게 convention plugin 안에서의 일반 규칙이다.

이 박스를 한 번 곱씹어두면 앞으로 convention plugin을 만들 때마다 string과 typed가 섞이는 모습이 자연스럽게 보인다. 책 전체에서 강조해온 Kotlin DSL의 타입 안전성과 모순되는 게 아니라, **타입 안전성이 동작하는 시점에 대한 정확한 이해의 결과**라고 정리하자.

## 적용 측: 한 줄로 줄어든다

이제 4개 모듈의 build.gradle.kts가 어떻게 줄어드는지 본다. 9장에서 비슷해 보이던 파일들이 정말로 한 줄짜리로 변한다.

```kotlin
// domain/build.gradle.kts
plugins {
    id("shop.java-conventions")
}
```

```kotlin
// order/build.gradle.kts
plugins {
    id("shop.java-conventions")
}

dependencies {
    implementation(project(":domain"))
}
```

```kotlin
// payment/build.gradle.kts
plugins {
    id("shop.java-conventions")
}

dependencies {
    implementation(project(":domain"))
}
```

```kotlin
// app/build.gradle.kts
plugins {
    id("shop.spring-boot-conventions")
}

dependencies {
    implementation(project(":domain"))
    implementation(project(":order"))
    implementation(project(":payment"))
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
}
```

깔끔하다. `:domain`은 정말로 한 줄짜리다. `:order`·`:payment`는 자기 의존성만 갖고 있다. `:app`은 starter들만 명시적으로 추가한다. 그 외 모든 빌드 결정 — toolchain 21, JUnit Platform, BOM 적용, Spring Boot 플러그인 적용 — 은 convention plugin이 책임진다. 한 곳에서 결정되고, 모든 모듈이 같은 결정을 공유한다.

확인해보자.

```bash
./gradlew :app:bootRun
```

9장과 똑같이 잘 돈다. 빌드 결과물도 그대로다. 다만 우리가 손에 쥔 빌드 스크립트의 크기가 크게 줄었다. 한 번 더 검증해보자. `./gradlew :domain:dependencies --configuration runtimeClasspath` 명령을 돌려보면 9장에서 봤던 그 의존성 트리가 그대로 나온다. Spring Boot BOM이 정렬해주는 spring-context·jackson 같은 라이브러리들이 똑같이 보인다. 즉 빌드의 외형적 동작은 완전히 동일하다. 우리는 동작은 그대로 두고, **빌드를 정의하는 코드를 단정하게 정리**했을 뿐이다. 리팩토링의 본 모습이다.

여기서 한 가지 즐거운 효과가 추가로 따라온다. 새 모듈이 들어왔을 때 새 팀원이 그 모듈의 build.gradle.kts를 열어봐도 한 줄짜리 plugin 선언만 보인다. 헷갈릴 여지가 거의 없다. "이 모듈은 회사 표준 java convention을 따른다" 또는 "이 모듈은 회사 표준 Spring Boot convention을 따른다" — plugin id가 그 사실을 그대로 말해준다. plugin id를 Cmd+클릭해서 정의된 파일로 들어가면 거기서 toolchain·BOM·테스트 설정이 한눈에 보인다. 추적이 안 되는 마법이 사라진다.

장기적으로 더 좋은 효과는 변경의 비용이다. JDK를 22로 올린다고 해보자. 우리가 만지는 파일은 `shop.java-conventions.gradle.kts` 한 곳이다. `21`을 `22`로 바꾸면 끝이다. BOM 버전을 4.0.7로 올린다고 해보자. `shop.spring-boot-conventions.gradle.kts` 한 곳이다. 4.0.6을 4.0.7로 바꾼다. 끝이다. `:catalog` 모듈을 새로 추가한다고 해보자. 새 모듈의 build.gradle.kts에 `plugins { id("shop.java-conventions") }` 한 줄을 적는다. 그 모듈은 즉시 회사 표준에 정렬된다. 끝이다.

이게 build logic의 모듈화가 가져다주는 안도감이다. 다섯 곳을 동시에 만져야 하는 두려움이 한 곳을 만지면 되는 안도감으로 바뀐다. 미래의 우리 자신을 위해서라도 이 정리는 반드시 거치자.

## Maven에서 옮겨온 사람을 위한 마지막 비교 박스

Part I·II에서 우리는 Maven 비교 박스를 자주 봤다. dependency scope는 configuration으로, phase는 task graph로, parent pom은 convention plugin으로. 그 약속 중 마지막을 여기서 회수한다. 그리고 이게 책 전체에서 **마지막으로 등장하는 Maven 비교 박스**다. 이 시점에서 독자는 이미 Gradle 사고로 옮겨와 있다.

> **Maven 비교 — parent pom vs Convention Plugin**
>
> Maven의 parent pom은 **상속**의 모델이다. 자식 pom은 `<parent>` 한 곳을 가리키고, 부모의 dependency·plugin·property를 물려받는다. 단일 부모 모델이라 간단하지만, 두 가지 한계가 분명히 있다.
>
> 첫째, **상속이 하나뿐이다.** Spring Boot의 spring-boot-starter-parent를 부모로 쓰는 동안에는 회사 표준 parent를 동시에 쓸 수 없다. 회사 parent가 spring-boot-starter-parent를 다시 상속하는 multi-level inheritance를 만들거나, 회사 parent에서 BOM(`dependencyManagement` import)만 빌려 쓰는 식으로 우회해야 한다. 어느 쪽이든 빌드 정의가 두꺼워진다.
>
> 둘째, **logic이 아니라 데이터에 가깝다.** parent pom은 의존성 관리·플러그인 설정 같은 XML 데이터를 물려준다. 조건부 분기를 표현하기 어렵고, 함수처럼 합성하기도 어렵다. profile이 그 빈자리를 채우지만 profile은 잘 알려진 함정이다.
>
> Convention plugin은 다르다. **조합**의 모델이다. 한 모듈은 필요한 만큼 plugin을 골라서 적용한다.
>
> ```kotlin
> plugins {
>     id("shop.java-conventions")
>     id("shop.test-fixtures-conventions")
>     id("shop.publishing-conventions")
> }
> ```
>
> 셋 다 회사 표준을 따른다. 동시에 셋이 적용되고, 충돌이 생기면 그 자리에서 분명히 드러난다. 그리고 각 convention plugin 안에는 Kotlin 코드가 들어 있다 — 조건부 분기, 함수 호출, Provider/Property 모두 자연스럽다. 데이터가 아니라 코드다.
>
> 한 줄로 정리하자면, **parent pom은 "물려받는" 모델, convention plugin은 "조립하는" 모델**이다. Spring Boot 백엔드처럼 한 회사에서 여러 종류의 모듈(앱, library, plugin, BOM 발행 모듈)이 공존하는 환경에서는 조립의 유연성이 곧 빌드의 건강이다.
>
> 이 박스를 끝으로 책에서 Maven을 직접 비교하는 자리는 마무리한다. 이후 챕터에서 Maven은 거의 등장하지 않는다. 우리는 이미 다른 사고 모델에 도착했다.

## `buildSrc/`의 그림자

축배를 들기 전에 한 가지를 살짝 짚어두자. `buildSrc/`는 깔끔하지만 완벽하지 않다. 두 가지 그림자가 따라붙는다.

가장 자주 부딪치는 한계는 이거다. **`buildSrc/` 안의 무엇이든 한 글자라도 바뀌면 이 빌드의 모든 task가 out-of-date가 된다.** 왜 그럴까. Gradle 입장에서 `buildSrc/`는 모든 모듈의 빌드 스크립트가 의존하는 일종의 상위 classpath다. 그 classpath가 바뀌었다는 건 모든 모듈의 빌드 정의가 바뀌었을 가능성을 의미한다. 그래서 안전을 위해 모든 task를 다시 검토한다. 결과적으로 convention plugin의 주석 한 줄을 고쳐도 전체 모듈의 컴파일·테스트·jar가 다시 돌 가능성이 생긴다.

이게 작은 프로젝트에서는 거의 느껴지지 않는다. convention plugin을 한 번 안정화하고 나면 그 후로는 바꿀 일이 자주 생기지 않기 때문이다. 다만 회사 빌드처럼 build logic 자체가 자주 진화하는 환경에서는 답답한 비용이 된다. CI 입장에서도 비슷한 일이 일어난다 — Build Cache가 잡아주는 부분이 있긴 하지만, `buildSrc/`가 자주 바뀌는 빌드는 Build Cache hit률이 떨어진다.

다른 한 가지 그림자는 재사용성이다. `buildSrc/`는 한 root build에서만 쓸 수 있다. 두 개의 다른 root build가 같은 build logic을 공유하고 싶을 때 `buildSrc/`는 답이 안 된다. 사내 표준 빌드 로직을 여러 팀이 같이 쓰고 싶다면 다른 길이 필요하다.

이 두 문제를 푸는 답은 `buildSrc/`를 **별도의 included build**로 옮기는 패턴이다. 관습적으로 이름은 `build-logic`. 다음 11장에서 본격적으로 다룬다. 다행히도 11장의 마이그레이션은 어렵지 않다. `buildSrc/`에서 정의한 convention plugin들이 거의 그대로 옮겨간다. 즉 우리가 이번 장에 들인 노력은 11장에서도 그대로 살아남는다.

그러니 회사 빌드가 작다면 `buildSrc/`로 충분히 만족스럽다. 그리고 회사 빌드가 커지더라도 `buildSrc/`는 좋은 출발선이다. 처음부터 `build-logic` included build로 시작하려는 욕심을 누르고, `buildSrc/`로 먼저 정착하는 편이 낫다. 빌드 도구를 단번에 완벽하게 만들려는 시도는 거의 항상 과도한 일반화로 빠진다. 동작하는 작은 도구를 먼저 만들고, 필요해진 시점에 키우자.

## convention plugin을 키우는 작은 규칙들

마지막으로 convention plugin을 운영하면서 익혀두면 좋은 작은 규칙 몇 가지를 모아두자. 큰 원리는 아니지만 알아두면 빌드가 일찍 다치는 걸 막아준다.

**plugin id에 namespace를 박자.** `java-conventions`처럼 짧게 적고 싶은 충동이 들지만, 권장은 `shop.java-conventions`처럼 점이 들어간 namespace 형태다. 이유 두 가지. 첫째, 회사 표준 plugin과 외부 plugin이 우연히 같은 이름을 갖는 사고를 막아준다. 둘째, IDE가 자동 완성을 줄 때 namespace로 그룹핑된다. `shop.`만 타이핑하면 우리 표준 plugin 목록이 죽 뜬다.

**convention은 작게 쪼개자.** 한 convention plugin에 모든 걸 욱여넣고 싶은 욕심이 든다. 그러면 한 줄짜리 적용이 가능하니까. 그런데 결국 일부 모듈에만 필요한 설정이 다른 모듈까지 끌려간다. `shop.java-conventions`(공통 토대), `shop.spring-boot-conventions`(앱용), `shop.publishing-conventions`(library 발행용)처럼 책임을 나누는 편이 낫다. 적용 측에서 plugin id를 여러 개 적는 비용은 거의 무시할 만하다.

**convention 안에서 적용 측 build.gradle.kts를 흉내내지 말자.** convention plugin은 build.gradle.kts와 똑같이 적을 수 있다는 매력 때문에, 자칫 그 안에 모듈별 의존성을 박아넣게 된다. `implementation(project(":domain"))`을 convention 안에 넣어버리는 식이다. 그러면 그 convention을 적용받는 모든 모듈이 `:domain`을 끌어다 쓰게 된다. 결과적으로 cross-project coupling이 다른 모양으로 다시 등장한다. **모듈별 결정은 모듈별 build.gradle.kts에**, **공통 결정만 convention 안에**라는 선을 분명히 긋자.

**string fallback이 등장할 때 의식적으로 인지하자.** 박스에서 봤듯이 `"implementation"(...)`은 oversight가 아니라 정확한 선택의 결과다. 그런데 익숙해지면 적용 측 build.gradle.kts에서도 같은 모양으로 적는 실수가 생긴다. 적용 측에서는 typed accessor가 노출돼 있으니 `implementation(...)`을 쓰자. string과 typed가 섞인 모습이 일관성 없어 보이지만, 그게 정확한 모습이다.

이 네 가지를 손에 익혀두면 convention plugin이 회사 빌드의 짐이 되지 않고 자산이 된다.

## 10장을 닫으며

8장에서 우리는 모듈을 쪼갰고, 9장에서 `bootJar` 함정을 진단해서 빌드를 정상으로 돌렸고, 10장에서 그 후에 남은 중복을 convention plugin으로 정리했다. Part III의 큰 흐름 중 하나가 이렇게 닫혔다.

지금 우리의 `ch09-convention/` 폴더를 보면 모습이 이렇다. 4개 모듈의 build.gradle.kts는 거의 plugin 한 줄짜리다. `buildSrc/` 안에 두 개의 convention plugin이 살아 있다. `shop.java-conventions`가 토대를 잡고, `shop.spring-boot-conventions`가 그 위에 Spring Boot를 얹는다. JDK를 올리는 결정, BOM을 올리는 결정, JUnit Platform을 강제하는 결정 — 모두 한 곳에서 일어난다. IntelliJ는 그 모든 결정을 정확히 추적한다.

다만 이쯤에서 두 가지 의문이 차오른다. 하나는 방금 짧게 본 `buildSrc/`의 그림자다. "build logic을 한 줄만 고쳐도 모든 task가 out-of-date가 된다"는 비용을 어떻게 우회하는가. 다른 하나는 좀 더 넓은 질문이다. "외부 라이브러리를 회사에서 같이 만들고 있는데, 그 라이브러리를 매번 publish하지 않고 우리 앱 빌드와 같이 돌릴 수 없을까?"

두 질문 모두 답이 같다. **included build**라는 개념이다. 11장에서 `buildSrc/`를 `build-logic`이라는 standalone included build로 승격시키는 작업과, 외부 라이브러리를 composite build로 묶어 들이는 패턴을 함께 본다. 이번 장의 convention plugin들이 그대로 살아남으면서 한 단계 더 자유로워지는 모습을 함께 보자.
