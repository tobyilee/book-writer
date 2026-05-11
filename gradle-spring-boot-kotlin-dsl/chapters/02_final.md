# 2장. Gradle의 사고 모델 — Settings, Project, Task, Lifecycle

1장에서 `build.gradle.kts`를 다시 짤 결심을 했다. 그렇다면 어디서부터 시작해야 할까? 도구를 다시 짜려면 도구가 세상을 어떻게 보는지부터 알아야 한다. 즉, Gradle이 빌드를 어떻게 객체로 보고, 그 객체들을 어떤 순서로 깨워서 task graph로 옮겨놓는지 그 사고 모델을 머릿속에 그릴 수 있어야 한다.

Maven에서 옮겨온 사람에게 Gradle의 첫인상은 종종 이렇다. "왜 빌드 파일이 두 개나 되지?" `settings.gradle.kts`, `build.gradle.kts`, 거기에 `gradle/libs.versions.toml`까지. pom.xml 한 파일로 모든 걸 끝내던 사람에겐 이 분산이 살짝 찜찜하게 느껴진다. 하지만 이 분산에는 명확한 이유가 있다. 함께 살펴보자.

## 빌드의 입구는 settings, 프로젝트의 정의는 build

상상해보자. 우리 회사 `shop` 빌드에 어느 날 `payment`라는 새 모듈을 끼워 넣어야 한다. 이 모듈이 빌드에 참여한다는 사실을 Gradle에게 어디서 알려야 할까? 또, `payment` 모듈이 의존하는 라이브러리는 어디에 적는 게 맞을까? 두 질문은 비슷해 보이지만 답이 다르다. 책임이 다르기 때문이다.

`settings.gradle.kts`는 **빌드의 입구**다. 어떤 프로젝트들이 이 빌드에 참여하는지, 플러그인은 어디서 받아오는지, 의존성 저장소는 어디인지 — 이런 "빌드 전체에 대한 결정"이 여기 산다.

```kotlin
// settings.gradle.kts
rootProject.name = "shop"

include("app", "domain", "order", "payment")

pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories {
        mavenCentral()
    }
}
```

`include("payment")` 한 줄로 새 모듈이 빌드에 참여한다. 저장소 선언은 `dependencyResolutionManagement {}` 안에만 둔다. `FAIL_ON_PROJECT_REPOS`를 켜두면 하위 프로젝트의 `build.gradle.kts`에서 `repositories {}`를 쓰는 순간 빌드가 실패한다. 회사 빌드를 운영해본 사람이라면 한 번쯤 겪었을 것이다 — 누가 어딘가에서 `jcenter()`를 몰래 추가해놓고 빌드 트러블슈팅에 반나절을 날려본 경험. 그런 사고를 settings 수준에서 한 번에 막아주는 장치다. 기억해두자.

반면 `build.gradle.kts`는 **한 프로젝트의 정의**다. 그 프로젝트가 어떤 task를 갖는지, 어떤 의존성을 declare하는지, 어떤 플러그인을 적용하는지. 즉 settings가 "어떤 프로젝트가 빌드에 참여하는가"를 다룬다면, build는 "그 프로젝트가 자기 안에서 무엇을 하는가"를 다룬다.

같은 단어 같지만 책임이 다르다. settings는 **참여자 명부**, build는 **각 참여자의 행동 강령**. 이 책 전체에서 둘이 자꾸 등장할 텐데, 어떤 결정을 어느 파일에 둘지 헷갈리면 이 비유를 떠올려보자.

> **Maven에서 옮겨온 분께**
> pom.xml 한 파일이 두 파일로 갈라지는 게 처음엔 어색하다. 대응을 짚어두면 이렇다. `<modules>`, `<repositories>`, `<pluginManagement>`는 모두 `settings.gradle.kts`로 옮겨간다. `<dependencies>`와 `<plugins>` 적용은 각 모듈의 `build.gradle.kts`로 간다. parent pom의 공통 설정은? 그건 settings도 build도 아닌 **Convention Plugin**으로 옮긴다 — 10장에서 자세히 본다.

## 세 단계의 lifecycle

Gradle에게 `./gradlew build`를 던지면 무슨 일이 일어날까? 아무 일도 아니라고 생각하기 쉽지만, 실은 그 짧은 명령 한 줄이 세 단계를 순차적으로 통과한다. 이 셋의 구분을 명확히 잡아두면, 나중에 Configuration Cache 위반이나 `bootJar` 함정 같은 사고를 만났을 때 디버깅의 출발점이 생긴다.

세 단계는 다음과 같다.

**1단계 — Initialization.** Gradle이 `settings.gradle.kts`를 평가한다. "이 빌드에 어떤 프로젝트들이 참여하는가"를 결정하는 단계다. `include("app", "domain", ...)`이 여기서 실행된다.

**2단계 — Configuration.** 참여하기로 정해진 모든 프로젝트의 `build.gradle.kts`를 평가한다. 플러그인이 적용되고, task가 등록되고, 의존성 그래프가 그려진다. 이 단계의 산출물이 바로 task graph — "어떤 task를 어떤 순서로 실행할지"의 청사진이다.

**3단계 — Execution.** 2단계에서 만들어진 task graph를 따라 실제로 task들을 실행한다. 컴파일도, 테스트도, jar 패키징도 모두 이 단계에서 일어난다.

말로만 들으면 추상적이다. 직접 보자.

```bash
$ ./gradlew help --task build

> Task :help
Detailed task information for build

Path
     :build

Type
     Task (org.gradle.api.Task)

Description
     Assembles and tests this project.

Group
     build
```

`./gradlew tasks`를 돌려보면 등록된 모든 task가 출력된다. 이 출력 자체가 Configuration phase의 산출물이다. 빌드를 한 번도 안 돌리고 `tasks`만 호출해도 결과가 나오는 이유다 — Execution phase까지 갈 필요가 없다.

```bash
$ ./gradlew tasks --all
...
Build tasks
-----------
assemble - Assembles the outputs of this project.
bootJar - Assembles an executable jar archive...
build - Assembles and tests this project.
...
```

여기서 한 가지 의문이 생긴다. Configuration phase는 매번 반복되는 게 아닌가? 빌드 스크립트 안의 코드는 매번 다시 실행되는 것 아닌가? 맞다. 그래서 큰 프로젝트일수록 이 단계가 점점 무거워진다. 빌드를 돌릴 때마다 `build.gradle.kts`가 처음부터 다시 평가된다고 생각하면 살짝 끔찍해진다.

> **Configuration Cache가 캐싱하는 자리**
> 바로 이 자리다. Configuration Cache는 2단계 — Configuration phase — 의 산출물을 통째로 캐싱한다. 한 번 만들어둔 task graph를 재사용할 수 있으면, 두 번째 빌드부터는 곧장 Execution phase로 점프한다. Gradle 9.0부터 이건 "preferred mode of execution"으로 격상됐고, 다음 minor 버전에서 default-on 후보로 거론된다. 13장에서 본격적으로 켜본다.

세 단계의 구분이 머릿속에 잡혔는가? 그렇다면 다음 질문으로 넘어가자. Configuration phase가 매번 무거운 게 문제라면, 그 단계에서 일어나는 일을 가볍게 만드는 길은 없을까? 있다. Task를 어떻게 등록하느냐의 문제다.

## Task — lazy로 등록한다

코드를 두 가지로 써보자. 같은 이름의 task를 만들지만, 등록 방식이 다르다.

```kotlin
// (A) eager — 피해야 할 방식
tasks.create("printSha") {
    println("Configuring printSha...")
    doLast { println("HEAD: ...") }
}

// (B) lazy — 정석
tasks.register("printSha") {
    println("Configuring printSha...")
    doLast { println("HEAD: ...") }
}
```

이제 `./gradlew help`를 돌려보자. 빌드 그래프에 `printSha`가 포함되지도 않는 명령이다. 어떤 차이가 보일까?

(A)에서는 `"Configuring printSha..."`가 출력된다. (B)에서는 출력되지 않는다.

이 작은 차이가 의미하는 바가 크다. `tasks.create`는 task를 **즉시(eager) 만든다.** 빌드 그래프에 들어갈지 안 들어갈지 따져보지도 않고 일단 만들어둔다. 반면 `tasks.register`는 task를 **lazy하게 등록한다.** "필요할 때 만들어줄게"라는 약속만 등록해두고, 실제 객체는 그 task가 빌드 그래프에 필요한 시점에야 비로소 realize한다.

`./gradlew help` 같은 가벼운 명령에 우리 회사의 모든 커스텀 task가 일일이 만들어진다고 상상해보자. 50개, 100개의 task가 매번 깨어난다면 Configuration phase가 꽤 둔해진다. 더 심각한 건 따로 있다. eager로 만든 task는 자기 입력값을 즉시 평가하려 들기 때문에, 그 시점에 아직 결정되지 않은 값(예: 다른 task의 출력 경로, environment variable)을 잡으려다 사고가 난다.

Configuration Cache의 관점에서 보면 더 명확하다. 캐시 대상은 Configuration phase의 결과 자체다. eager로 즉시 평가된 task는 캐시 키 안에 그 즉시 값이 박혀 들어간다. 환경이 조금만 바뀌어도 캐시가 무효화된다. lazy로 등록된 task는 필요할 때만 realize되고, 입력값도 Provider로 감싸진 채 lazy하게 평가되니 캐시 친화적이다.

그러니 task를 만들 때는 `tasks.register`가 정석이다. 기억해두자. `tasks.create`는 Gradle 7 이전 시대의 잔재이며, 9.x를 쓰는 우리에겐 이유 없는 선택이다. 마찬가지로 이미 등록된 task를 가져올 때도 `tasks.named<Test>("test") { ... }`가 좋다. `tasks.getByName("test")`는 호출 즉시 realize되어 lazy의 이점을 모두 날려버린다.

이 lazy 모델은 단순한 문법 차이가 아니다. **Gradle 9.x의 사고 모델 그 자체**다. 12장에서 커스텀 task를 만들 때 다시 만난다. 그때까지는 "register는 lazy, create는 eager, 우리는 register만 쓴다" 정도면 충분하다.

## Plugin의 세 종류

Gradle에서 plugin은 빌드에 task, configuration, convention을 주입하는 단위다. 그런데 plugin이라는 한 단어가 실은 세 가지 다른 모습으로 등장한다.

첫째, **Binary plugin.** JVM 클래스로 컴파일된 `Plugin<Project>` 구현체다. `org.springframework.boot`, `org.jetbrains.kotlin.jvm` 같은 외부 plugin이 모두 여기 속한다. 빌드 스크립트에서는 이렇게 적용한다.

```kotlin
plugins {
    id("org.springframework.boot") version "4.0.6"
    java
}
```

가장 흔하고 가장 표준적인 형태다. 의심 없이 이걸 기본으로 쓴다.

둘째, **Script plugin.** 다른 `.gradle.kts` 파일을 `apply(from = "shared.gradle.kts")`로 끌어와 적용하는 방식이다. 옛날엔 이 방식으로 여러 모듈이 공통 설정을 공유했다. 하지만 솔직히 지금 시점에 이걸 쓰는 건 끔찍한 일이다. 타입 안전성이 사라지고, IDE 추적도 깨지고, Configuration Cache 친화성도 떨어진다. **legacy로 분류해두고 새로 쓰지는 말자.**

셋째, **Precompiled convention plugin.** `buildSrc/` 또는 `build-logic/`에 두는 `*.gradle.kts` 파일을 말한다. 파일 이름이 곧 plugin id가 되고, Gradle이 자동으로 binary plugin으로 컴파일해준다.

```kotlin
// buildSrc/src/main/kotlin/shop.spring-boot-conventions.gradle.kts
plugins {
    java
    id("org.springframework.boot")
}

java {
    toolchain { languageVersion = JavaLanguageVersion.of(21) }
}
```

소비 측에서는 한 줄이다.

```kotlin
// app/build.gradle.kts
plugins {
    id("shop.spring-boot-conventions")
}
```

이게 바로 회사 단위 표준 빌드를 모듈마다 똑같이 반복하지 않고 한 곳에 모으는 권장 방식이다. 자세히는 10장에서 본다. 지금 기억할 건 하나다 — **precompiled convention plugin이 9.x의 표준이며, script plugin은 피한다.**

## Configuration의 세 역할

Gradle의 단어 중에 `configuration`만큼 처음 보는 사람을 혼란스럽게 만드는 게 또 있을까? Maven 출신에겐 더 그렇다. `<configuration>` 태그를 `<plugin>` 안에 적던 그 단어와는 의미가 완전히 다르다.

Gradle에서 **Configuration은 의존성 버킷**이다. 의존성들이 모여 있는 통이라고 생각하면 쉽다. `implementation`도 configuration이고, `compileClasspath`도 configuration이며, `apiElements`도 configuration이다. 같은 단어로 세 가지가 불린다.

처음엔 헷갈리지만, 9.x에 와서 이 셋의 역할이 명시적으로 분리됐다. 표로 정리해보자.

| 역할 | declarable | resolvable | consumable | 대표 예 |
|------|-----------|-----------|-----------|---------|
| **Dependency scope** | ✅ | ❌ | ❌ | `implementation`, `api`, `compileOnly` |
| **Resolvable** | ❌ | ✅ | ❌ | `compileClasspath`, `runtimeClasspath` |
| **Consumable** | ❌ | ❌ | ✅ | `apiElements`, `runtimeElements` |

세 역할은 이렇게 갈린다.

**Dependency scope (declarable).** 사용자가 `dependencies { implementation("…") }`처럼 직접 적는 자리. 이건 의존성을 **선언만** 하는 통이다. 통 자체를 resolve해서 classpath로 펴내지는 않는다.

**Resolvable.** 통에 모인 의존성을 실제로 트리로 풀어내는 자리. `compileClasspath`는 컴파일 시점에 필요한 모든 transitive를 resolve해 펼친 결과다. 이건 plugin이 만들어준다. 사용자가 직접 만질 일은 거의 없다.

**Consumable.** 다른 프로젝트가 이 프로젝트를 의존할 때 노출하는 자리. `apiElements`는 "내 API를 쓰려면 이 의존성들이 필요해" 라고 알리는 통이다. 역시 plugin이 만들어준다.

핵심은 이거다 — **우리가 직접 다루는 건 거의 declarable 뿐**이다. `implementation`, `api`, `compileOnly`, `runtimeOnly`, `annotationProcessor` 다섯 개. 나머지는 plugin이 알아서 만든다.

그렇다면 왜 이 셋의 구분이 9.x에서 중요해졌을까? 옛날엔 한 configuration이 세 역할을 동시에 떠안았다. 그래서 우연히도 `implementation`을 resolve해버리는 코드가 빌드 어딘가에 박혀 있어도 빌드가 돌아갔다. 하지만 이건 굉장히 찜찜한 상태다. 의존성 그래프가 의도와 다르게 풀려도 빌드는 침묵하기 때문이다. 9.x는 이걸 명시적으로 막는다. declarable을 resolve하려 하면 빌드가 실패한다.

이 사고 모델은 5장에서 의존성을 본격적으로 다룰 때 다시 만난다. 그때까지는 "configuration은 통이고, 통마다 declarable/resolvable/consumable 역할이 따로 있다"는 정도가 손에 잡히면 충분하다.

> **Maven에서 옮겨온 분께**
> Maven의 dependency scope(`compile`, `provided`, `runtime`, `test`)는 Gradle의 declarable configuration으로 대응된다. `compile` → `implementation`(혹은 `api`), `provided` → `compileOnly`, `runtime` → `runtimeOnly`, `test` → `testImplementation`. 다만 의미가 미묘하게 다르다 — Gradle의 `implementation`은 컴파일·런타임 모두 포함하면서 소비자에겐 노출되지 않는, Maven에 정확히 1:1 대응이 없는 개념이다. 자세히는 5장에서 풀어본다.

## 2장을 닫으며

여기까지 따라왔다면 Gradle이 빌드를 어떻게 바라보는지 그 골격이 잡혔을 것이다. 정리해보자.

빌드는 두 종류의 파일에 갈라져 산다. settings는 빌드의 입구이자 참여자 명부, build는 각 프로젝트의 행동 강령. 그리고 Gradle은 빌드를 세 단계로 통과시킨다 — Initialization에서 명부를 읽고, Configuration에서 task graph를 그리고, Execution에서 그 그래프를 따라간다. Configuration Cache는 두 번째 단계의 산출물을 통째로 캐싱한다.

Task는 lazy로 등록하는 게 표준이다. `tasks.register`와 `tasks.named`. 이건 단순한 문법 취향이 아니라, Configuration Cache 친화성과 시작 속도까지 좌우하는 사고의 기본기다. Plugin은 binary, script, precompiled convention 셋 중 — 우리는 binary와 precompiled convention만 쓰고, script는 잊는다. Configuration이라는 한 단어가 declarable·resolvable·consumable 세 역할로 나뉜다는 것도 머릿속 어딘가에 박아두자. 5장에서 다시 만난다.

그런데 이렇게 사고 모델만 머리에 넣고 막상 `build.gradle.kts`를 짜기 시작하면, 의외로 다른 곳에서 발이 걸린다. Kotlin DSL이라는 언어 자체의 함정이다. `=`와 `.set()`은 같은가 다른가, type-safe accessor는 왜 어떤 plugin에선 안 보이는가, `subprojects {}`를 쓰면 왜 자꾸 누가 말리는가. 사고 모델은 맞아도, 문법의 미묘한 함정에 한 번 발이 빠지면 뒷맛이 꽤 찜찜해진다.

3장에서 그 함정들을 하나씩 짚어보자.
