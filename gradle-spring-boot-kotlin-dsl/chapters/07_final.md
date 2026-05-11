# 7장. 테스트를 분리한다 — JVM Test Suite로 통합 테스트

6장의 마지막에 우리의 `ch04-bootapp/`은 `./gradlew bootJar`로 실행 가능한 fat jar를 뱉어내고, `./gradlew bootBuildImage`로 OCI 이미지까지 만든다. 이제 이 앱에 테스트를 붙일 차례인데, 정확히는 "테스트 하나"가 아니라 "두 종류의 테스트"를 붙일 차례다.

상상해보자. 단위 테스트는 빠르다. 도메인 객체 하나 만들고, 메서드 하나 호출해서, 결과를 assert한다. 수십 개 모여도 1초가 안 걸린다. 그런데 통합 테스트는 다르다. `@SpringBootTest`가 ApplicationContext 전체를 띄우고, 거기에 Testcontainers가 Docker로 Postgres 컨테이너를 한 개 더 끌어올린다. 한 개 돌리는 데 5초, 십수 개면 1분이 우습게 지나간다. 이걸 한꺼번에 `./gradlew test`로 묶어두면 어떤 일이 생기는가? 매번 빌드할 때마다 1분짜리 통합 테스트 묶음을 기다린다. 로컬에서 `./gradlew build`를 한 번 돌릴 때마다 커피 한 잔이 식는다. 난감한 일이다.

그래서 보통은 통합 테스트를 분리한다. 예전부터 익숙한 방식은 `sourceSets.create("integrationTest") { ... }` 한 덩어리를 직접 짜는 일이었다. 소스셋을 만들고, 거기에 맞는 configuration을 손으로 잇고, task를 만들고, classpath를 직접 짜맞춰주고… 한 번 해본 사람이 가장 자주 잊어버리는 한 줄이 있다. 그 한 줄을 빼먹으면 컴파일은 되는데 spring-boot-starter-test의 의존성이 누락된다. 찜찜하다. 그리고 매 프로젝트마다 이 boilerplate를 베껴 다닌다. 동료들에게 "이 한 줄이 왜 있는지 모르겠지만 빼면 깨진다"는 댓글이 달린 채로.

Gradle 9.x는 이 일을 더 이상 손으로 시키지 않는다. **`jvm-test-suite` 플러그인이 9.x에서 incubating을 떼고 정식 표준이 됐다.** 이 장에서 풀고 싶은 매듭은 한 줄이다. **단위 테스트와 통합 테스트를 같은 `test` task에 욱여넣지 않으면서, 손으로 짜던 boilerplate를 어떻게 선언 한 덩어리로 줄이는가.**

## 그 전에 — `test` task의 기본부터

본격적으로 들어가기 전에 한 가지를 정리하자. 우리가 `./gradlew test`라고 칠 때 그 `test`는 정확히 어디서 오는가.

답은 단순하다. `java` 플러그인을 적용하는 순간 Gradle은 표준 소스셋 `main`과 `test`를 만들고, `test` 소스셋을 컴파일하고 실행하는 `test`라는 `Test` 타입 task를 등록한다. Spring Boot 플러그인은 그 위에 올라타기만 한다. 우리가 따로 만들지 않아도 그 task는 이미 있다.

그 task에는 한 가지 선택지가 붙는다 — 어떤 테스트 프레임워크로 돌릴 것인가. JUnit 4의 옛 방식은 별도 설정이 필요 없지만, 우리는 JUnit Jupiter(5)를 쓴다. 그래서 한 줄이 필요하다.

```kotlin
tasks.named<Test>("test") {
    useJUnitPlatform()
}
```

이 한 줄이 우리에게 익숙한 풍경이다. **`useJUnitPlatform()`은 "JUnit Platform 위에서 돌려라"는 선언**이다. Platform이 그 위에서 Jupiter(5), Vintage(4 호환), 그 외 Platform 호환 엔진을 끌어올린다. Spring Initializr가 만들어주는 `build.gradle.kts`에 보통 이 한 줄이 박혀 있다.

그런데 새 표준인 `jvm-test-suite`를 쓰기 시작하면 비슷하지만 살짝 다른 API를 만난다 — `useJUnitJupiter("5.11.4")`. 이름만 보면 같은 일을 하는 것 같은데, 정확히는 한 단계 더 친절하다. **Platform을 깐 위에 Jupiter 의존성까지 자동으로 testImplementation에 더해준다.** 우리가 따로 `org.junit.jupiter:junit-jupiter`를 의존성에 적지 않아도 된다. 버전 인자가 그래서 들어간다.

| API | 위치 | 하는 일 |
|---|---|---|
| `useJUnitPlatform()` | `Test` task | "이 task는 JUnit Platform 위에서 돌린다"는 신호. 의존성은 직접 추가해야 한다. |
| `useJUnitJupiter("5.11.4")` | `JvmTestSuite` | Platform 활성화 + Jupiter 의존성 자동 추가. |

같은 단어처럼 보이지만 작동 위치가 다르다. 옛 코드에서는 task 수준에서 platform만 켜고 의존성은 따로 적었다. `jvm-test-suite` 아래에서는 suite 한 곳이 두 일을 함께 한다. 이 차이를 모르면 새 API로 옮긴 뒤 "왜 junit이 두 번 들어가지?"라고 헷갈리기 쉽다. 기억해두자 — **suite 안에서는 `useJUnitJupiter()` 하나면 끝**이다.

## `jvm-test-suite`라는 모델

자, 그러면 `jvm-test-suite`가 정확히 무엇을 추상화한 도구인가.

이름을 풀어보면 더 명확하다. **"JVM 위에서 도는 테스트들의 묶음(suite)"을 빌드의 1급 객체로 본다**는 뜻이다. 옛날엔 테스트라는 게 `test`라는 한 소스셋·한 task에 묶인 단일 개념이었다. JUnit Jupiter가 등장하고, 통합 테스트가 일상화되고, 컨테이너 테스트가 추가되면서 "테스트는 사실 한 종류가 아니다"라는 사실이 드러났다. 그런데 Gradle은 한참 동안 그 사실을 모델로 흡수하지 못해서, 개발자들이 손으로 소스셋·configuration·task를 짜맞추고 있었다.

`jvm-test-suite`는 그 짜맞춤을 한 곳에 흡수한다. `testing { suites { ... } }` 블록 안에 suite를 하나 선언하면, Gradle이 자동으로:

- **소스셋**: `src/<suite-name>/java`, `src/<suite-name>/resources` 디렉터리를 표준 위치로 인식한다.
- **의존성 configuration**: `<suite-name>Implementation`, `<suite-name>RuntimeOnly`, `<suite-name>CompileOnly` 등이 자동 생성된다.
- **task**: `compile<Suite>Java`, `process<Suite>Resources`, 그리고 실제로 실행하는 `<suite-name>` task가 등록된다.

쉽게 말하면, **suite 이름만 정하면 그 이름을 머리에 붙인 모든 관련 객체가 따라 나온다.** 우리가 손으로 잇던 boilerplate가 통째로 사라진다.

그리고 9.x로 오면서 이 플러그인의 incubating 표식이 떨어졌다. 이전엔 "아직 실험 단계이고 시그니처가 바뀔 수 있다"는 경고가 붙어 있었는데, 9.x는 그 표식을 떼고 표준 API로 자리잡았다. 새로 짤 빌드에서 통합 테스트를 분리한다면 더 고민할 이유가 없다.

## `integrationTest` suite를 더한다

이론은 됐고, 우리의 `ch04-bootapp/`에 직접 붙여보자. 빌드 스크립트를 다음과 같이 키운다.

```kotlin
plugins {
    `jvm-test-suite`
    id("org.springframework.boot")
    id("io.spring.dependency-management")
    // ... 5장에서 정리한 다른 플러그인들
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
                implementation("org.testcontainers:postgresql")
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

코드는 짧지만 들여다볼 곳이 몇 군데 있다.

먼저 **기본 `test` suite는 `getting`으로 가져온다.** `jvm-test-suite` 플러그인이 적용된 순간 `test`라는 이름의 suite가 이미 등록되어 있다. 우리가 새로 만드는 게 아니라, 거기에 `useJUnitJupiter("5.11.4")` 한 줄을 더해 Platform과 Jupiter 의존성을 같이 활성화한다. Initializr에서 받은 빌드의 `useJUnitPlatform()` 한 줄을 이 자리로 옮기는 셈이다.

그 다음 줄에서 **`register<JvmTestSuite>("integrationTest")`로 새 suite를 추가한다.** 이름은 자유다 — `integrationTest`, `e2eTest`, `slowTest`, 회사 컨벤션에 맞게 정하면 된다. 이 한 줄이 떨어진 순간 Gradle 안에서 다음이 일제히 일어난다.

- `src/integrationTest/java`, `src/integrationTest/resources`가 표준 소스셋 위치가 된다.
- `integrationTestImplementation`, `integrationTestRuntimeOnly`, `integrationTestCompileOnly` configuration이 자동으로 생긴다.
- `compileIntegrationTestJava`, `processIntegrationTestResources`, 그리고 `integrationTest`라는 이름의 `Test` 타입 task가 등록된다.

우리가 손으로 만든 게 아니라 suite 한 덩어리에서 따라 나온 결과다. 옛 `sourceSets.create("integrationTest") { ... }` 패턴을 써본 사람이라면 그때 손으로 잇던 코드를 떠올려보자 — 소스셋 만들고, configuration extends를 직접 잇고, task를 만들어 classpath를 짜맞추고, output을 testRuntimeClasspath에 연결하고… 그 모든 짜맞춤이 한 줄의 `register`로 압축됐다.

## suite 안의 의존성 선언

`dependencies { ... }` 블록은 suite 내부에 있다는 점에 주의하자. 여기서 적는 의존성은 `integrationTestImplementation`이라는 configuration에 자동으로 붙는다. 바깥 `dependencies {}` 블록에서 `"integrationTestImplementation"(...)` 식의 문자열 receiver를 쓰는 대신, **suite 안에서는 그냥 `implementation(...)`이라고 쓰면 Gradle이 알아서 `integrationTestImplementation`으로 라우팅한다.** 짧고 명확하다.

다만 한 가지 묘한 줄이 있다.

```kotlin
implementation(project())
```

이 한 줄은 무엇인가. `project(":app")`도 아니고, 좌표 문자열도 아니다. 인자 없이 `project()`. **"이 suite를 호스팅하는 프로젝트(우리 자신)의 main 소스셋을 의존성으로 끌어오겠다"는 선언**이다. integrationTest는 main의 클래스를 호출해야 의미가 있는데, suite 모델에서는 그 연결을 명시해야 한다. 옛 `sourceSets.create(...)` 시절엔 `sourceSets["main"].output`을 직접 더해주던 일이 이 한 줄로 줄었다.

그리고 Spring Boot 통합 테스트의 단골인 `spring-boot-starter-test`와 Testcontainers의 `junit-jupiter`, `postgresql` 모듈을 더했다. 버전이 비어 있는 이유는 5장에서 이미 봤다 — Spring Boot BOM(`platform(...)`)이 transitive를 정렬해주기 때문이다. 새 suite여도 이 정합성은 그대로 이어진다. **suite는 의존성 구조를 새로 짜는 게 아니라 이름공간만 분리한다는 점**을 기억해두자.

## 실행 순서와 `check` 연결

자, 이제 두 가지가 남았다. **언제 돌리고, 어떻게 자동으로 끌려 들어가게 할 것인가.**

```kotlin
targets.all {
    testTask.configure {
        shouldRunAfter(test)
    }
}
```

`shouldRunAfter`는 의존이 아니다 — **단지 "이 task가 같이 실행될 때는 test가 먼저 돌고 나서 그 다음 차례여야 한다"는 순서 힌트**다. 의존성(`dependsOn`)이면 `integrationTest`만 호출해도 `test`가 강제로 따라온다. 그렇게 되면 분리한 의미가 옅어진다 — 통합 테스트만 빨리 돌려보고 싶은데 단위 테스트가 매번 같이 끌려 나오면 답답하다. `shouldRunAfter`는 그 모호함 없이 "둘이 같이 호출됐을 때만 순서를 지킨다"는 뜻이다. 단위 테스트가 빠르니 먼저 실패시켜서 빨리 신호를 받자는 휴리스틱이 그 안에 들어 있다.

그리고 `check` task에 의존을 더한다.

```kotlin
tasks.named("check") {
    dependsOn(testing.suites.named("integrationTest"))
}
```

`check`는 Gradle의 표준 lifecycle task다. 보통 CI에서는 `./gradlew check`(혹은 `build`, build가 check를 포함한다)로 모든 검증을 한 번에 돌린다. 기본적으로 `check`에는 `test`가 이미 의존으로 걸려 있고, 우리가 한 줄을 더하면 `integrationTest`도 그 의존으로 들어간다. **그러니 CI에서는 두 suite가 모두 자동으로 실행된다.** 로컬에서는 빠른 피드백을 받으려고 `./gradlew test`만 호출할 수 있고, 통합 테스트가 필요할 땐 `./gradlew integrationTest`만 따로 돌릴 수도 있다. CI는 한 번에 다 본다. 셋이 자기 자리를 가진다.

## Testcontainers와 `@SpringBootTest`의 결합

이 분리의 진짜 가치는 통합 테스트가 실제로 무거운 짐을 짊어질 때 드러난다. `src/integrationTest/java/com/example/shop/OrderApiIT.java`에 다음과 같은 테스트가 들어갔다고 해보자.

```kotlin
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class OrderApiIT {

    companion object {
        @Container
        @JvmStatic
        val postgres = PostgreSQLContainer("postgres:16-alpine")

        @JvmStatic
        @DynamicPropertySource
        fun props(registry: DynamicPropertyRegistry) {
            registry.add("spring.datasource.url", postgres::getJdbcUrl)
            registry.add("spring.datasource.username", postgres::getUsername)
            registry.add("spring.datasource.password", postgres::getPassword)
        }
    }

    @Autowired
    lateinit var restTemplate: TestRestTemplate

    @Test
    fun `주문을 만들고 조회한다`() {
        // ApplicationContext가 RANDOM_PORT로 떠 있고,
        // Postgres 컨테이너가 살아 있는 상태에서 실제 HTTP 호출로 시나리오를 본다
    }
}
```

이 한 클래스가 ApplicationContext를 띄우고, Docker로 Postgres를 띄우고, `@DynamicPropertySource`로 컨테이너의 JDBC URL을 Spring property에 주입하고, HTTP까지 한 바퀴 돈다. 한 번 도는 데 수 초가 걸린다. 비싼 짐이다.

그리고 이 비싼 짐이 **`integrationTest` task 안에만 묶여 있다.** 단위 테스트는 그동안 자기 자리에서 빠르게 자기 일을 본다. 로컬에서 `./gradlew test`로 단위 테스트만 돌리는 한, 우리 머신에서 Docker가 깨어날 일이 없다.

**`@SpringBootTest`가 보통 권장되지 않는 이유**도 여기서 정리된다. `@SpringBootTest`는 전체 ApplicationContext를 띄우니 비용이 크다. 그래서 평소엔 `@WebMvcTest`, `@DataJpaTest` 같은 슬라이스 테스트를 쓴다. 그런 슬라이스 테스트들은 단위 테스트만큼은 아니어도 가볍게 도는 편이라 `test` suite에 머문다. **본격적으로 ApplicationContext 전체 + 외부 컨테이너까지 끌어올리는 시나리오만 `integrationTest`로 분리한다.** 슬라이스가 어디까지가 단위인지에 대해선 팀마다 결정이 다를 수 있는데, 그 결정의 자유가 suite 분리로 비로소 가능해진다. suite가 한 덩어리였다면 "어떤 테스트가 빠르고 어떤 테스트가 느린가"라는 질문 자체가 무의미하다 — 어차피 한 번에 다 도니까.

## `integrationTest` 디렉터리 구조

마지막으로, 막상 디렉터리를 만들려고 하면 한 번 헤맨다. 어디에 어떤 클래스를 두는가.

```
ch04-bootapp/
├── build.gradle.kts
└── src/
    ├── main/
    │   ├── java/com/example/shop/...
    │   └── resources/
    │       └── application.yml
    ├── test/                          # 단위 테스트 — 빠르게
    │   ├── java/com/example/shop/...
    │   └── resources/
    │       └── application-test.yml
    └── integrationTest/               # 통합 테스트 — 무겁게
        ├── java/com/example/shop/...
        └── resources/
            └── application-integrationTest.yml
```

핵심은 **`src/integrationTest/`라는 폴더가 표준 위치로 그대로 통한다**는 점이다. 우리가 `sourceSets`로 폴더를 손으로 지정할 필요가 없다. suite 이름과 폴더 이름이 같으면 Gradle이 자동으로 잡는다. resources도 `src/integrationTest/resources` 아래에 두면 그대로 integrationTest의 runtime classpath에 들어간다. `application-integrationTest.yml` 같은 profile-specific 파일을 두고, `@ActiveProfiles("integrationTest")`로 묶는 패턴이 자연스럽다.

> **마이그레이션 노트 — 옛 `sourceSets.create("integrationTest")` 패턴**
>
> Gradle 7.x 이전 시절, 또는 9.x에서도 옛 빌드를 유지보수하는 팀에서는 이런 코드를 만난다.
>
> ```kotlin
> sourceSets {
>     create("integrationTest") {
>         compileClasspath += sourceSets.main.get().output + configurations.testRuntimeClasspath.get()
>         runtimeClasspath += output + compileClasspath
>     }
> }
>
> val integrationTestImplementation by configurations.getting {
>     extendsFrom(configurations.testImplementation.get())
> }
>
> val integrationTest = tasks.register<Test>("integrationTest") {
>     description = "Runs integration tests."
>     group = "verification"
>     testClassesDirs = sourceSets["integrationTest"].output.classesDirs
>     classpath = sourceSets["integrationTest"].runtimeClasspath
>     shouldRunAfter("test")
>     useJUnitPlatform()
> }
>
> tasks.named("check") { dependsOn(integrationTest) }
> ```
>
> 길고, 손으로 잇는 줄이 많다. 빼먹기 쉬운 한 줄은 `extendsFrom(configurations.testImplementation.get())` — 이걸 빼면 `spring-boot-starter-test`가 integrationTest에 안 들어와서 컴파일이 깨진다. 옛날엔 그게 통과의례였다.
>
> 같은 결과를 새 표준에서는 위에서 본 `register<JvmTestSuite>("integrationTest") { ... }` 한 덩어리로 끝낸다. **이전 빌드를 9.x로 옮길 때, 통합 테스트 분리 코드는 이 한 덩어리로 갈아끼우는 편이 낫다.** 동작은 같고, 코드는 1/3이고, 그 한 줄을 빼먹어서 깨지는 사고가 사라진다. 이미 잘 돌고 있는 빌드를 굳이 건드릴 필요는 없지만, 한 번 손볼 일이 생기면 그 김에 마이그레이션하자.

## 7장을 닫으며

이번 장에서 우리가 한 일을 정리해두자. 우리의 `ch04-bootapp/`에 `src/integrationTest/` 디렉터리가 새로 생겼고, 빌드 스크립트의 `testing { suites { ... } }` 블록 안에서 `integrationTest`라는 suite를 한 덩어리로 선언했다. `./gradlew test`는 빠른 단위 테스트만 돌고, `./gradlew integrationTest`는 Testcontainers와 ApplicationContext가 동원되는 무거운 시나리오만 돌고, `./gradlew check`는 둘 다 돌린다. CI는 `check`만 호출하면 된다. 우리가 손으로 잇는 코드는 거의 없었다 — suite 한 덩어리에서 모든 게 따라 나왔다.

여기까지가 Part II의 끝이다. 4장에서 Maven에서 Gradle로 다리를 건너고, 5장에서 의존성을 다스리고, 6장에서 Spring Boot 플러그인의 안쪽을 본 다음, 7장에서 테스트를 두 layer로 갈랐다. 단일 모듈로는 부족함이 없는 빌드가 됐다. **이 시점에서 우리의 `ch04-bootapp/`은 회사 프로덕션 코드 한 모듈을 그대로 흉내내도 어색하지 않다.** 의존성 명세는 catalog가 보관하고, transitive 정렬은 BOM이 책임지고, 실행 가능한 fat jar와 OCI 이미지는 Spring Boot 플러그인이 책임지고, 테스트는 빠른 것과 무거운 것이 자기 자리에서 자기 일을 한다.

그런데 회사 빌드는 보통 여기서 멈추지 않는다. 도메인이 커지면 한 모듈이 갑갑해진다. `app`, `domain`, `order`, `payment` 같이 책임을 쪼개고 싶어진다. 그렇게 모듈을 쪼개기 시작하는 순간 — 단순히 `settings.gradle.kts`에 `include(":domain")` 한 줄 더하는 일로 끝나지 않는다는 사실을 우리는 곧 알게 된다. `bootJar`가 멀티 모듈에서 만들어내는 묘한 사고 하나가 우리를 기다리고 있다. 8장에서 그 첫 단추를 끼우고, 9장에서 그 사고를 정면으로 진단한다. Part III의 시작이다.
