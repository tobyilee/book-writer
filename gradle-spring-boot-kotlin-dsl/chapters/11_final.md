# 11장. buildSrc 한계를 넘는다 — build-logic included build와 Composite Build

`buildSrc/` 안에 있는 `shop.java-conventions.gradle.kts`를 열어 주석 한 줄을 고친다고 해보자. "이 convention은 회사 표준 JDK 21을 강제한다"는 한 줄짜리 주석 정도다. 아무 task에도 영향이 가지 않는 변경이다. 그 다음 `./gradlew :app:bootRun`을 돌린다.

```
> Task :buildSrc:compileKotlin
> Task :buildSrc:compileJava NO-SOURCE
> Task :buildSrc:jar
...
> Task :app:compileJava
> Task :app:processResources
> Task :app:classes
> Task :domain:compileJava
> Task :order:compileJava
> Task :payment:compileJava
...
```

`:app`만 도는 게 아니라 4개 모듈의 compile이 다 돈다. 직전에 빌드를 돌렸어도 똑같다. `--profile`로 시간을 재 보면 incremental의 단맛이 거의 사라진 모습이다. 주석 한 줄을 고쳤을 뿐인데 빌드 전체가 처음부터 다시 검토되는 셈이다.

10장 끝에서 짧게 짚어둔 "buildSrc의 그림자"가 바로 이 장면이다. 작은 프로젝트에서는 거의 느껴지지 않다가, 회사 빌드처럼 build logic 자체가 자주 진화하는 환경에서는 답답한 비용으로 누적된다. 그리고 답답함이 누적되면 사람은 자연스럽게 잘못된 회피를 시도한다. convention plugin을 만들 엄두를 못 내거나, 이미 만들어둔 convention을 건드리기 두려워하거나. 빌드 도구가 도리어 변경의 적이 되는 셈이다.

이 장에서는 그 답답함의 처방을 본다. **`buildSrc/`를 별도의 included build로 승격시키는 패턴**, 흔히 `build-logic`이라 부르는 구조다. 그리고 그 과정에서 자연스럽게 Composite Build라는 더 일반적인 개념을 만난다. 외부 라이브러리와 동시에 개발하는 시나리오까지 짧게 곁들이긴 하지만, 이 장의 무게는 build-logic 분리에 실려 있다. 회사 빌드를 한 단계 더 자유롭게 만드는 마지막 정리라고 봐도 좋다. Part III의 마지막 장이기도 하다.

이 장에서 자라는 앱 상태는 `ch11-composite/` 폴더에서 동작한다. `ch09-convention/`의 `buildSrc/`가 root 옆 `build-logic/`이라는 standalone Gradle build로 옮겨가 있다. convention plugin들은 거의 그대로 살아남는다 — 우리가 10장에 들인 노력은 11장에서도 그대로 자산이 된다는 게 좋은 소식이다.

## buildSrc의 그림자가 정확히 어디서 시작되는가

처방으로 곧장 넘어가기 전에, `buildSrc/`의 한계를 한 번 더 분명히 짚어두자. 막연히 "느려진다"가 아니라 정확히 어디서 비용이 발생하는지를 봐야, 처방의 모양을 이해할 수 있다.

`buildSrc/`는 Gradle 입장에서 **이 빌드에 참여하는 모든 모듈의 build script가 의존하는 상위 classpath**다. 우리가 작성한 `shop.java-conventions.gradle.kts`는 컴파일되어 `buildSrc/build/libs/buildSrc.jar` 안에 들어가고, 모든 모듈은 그 jar를 자기 build script의 classpath로 받는다. 우리가 모듈의 build.gradle.kts에 `plugins { id("shop.java-conventions") }`를 적은 순간, 그 모듈의 빌드 정의는 `buildSrc/`의 산출물에 묶이는 셈이다.

이게 무엇을 뜻하는가. `buildSrc/`가 바뀌면, 모든 모듈의 빌드 정의가 바뀐 셈이 된다. 모든 모듈의 빌드 정의가 바뀌었다는 건 모든 task의 입력값이 바뀌었을 가능성이 있다는 의미다. Gradle은 안전을 위해 그 가능성을 보수적으로 다룬다. 결과적으로 모든 task가 out-of-date 후보로 들어간다. Build Cache가 일부를 구해주긴 하지만, 빌드 정의의 hash가 달라지면 cache key도 달라진다. 즉 cache hit률 자체가 떨어진다.

그뿐만이 아니다. 두 번째 그림자가 따라붙는다. **`buildSrc/`는 한 root build에서만 쓸 수 있다.** 사내에서 두 개의 다른 서비스가 같은 convention plugin들을 공유하고 싶다고 해 보자. 한 회사가 결제 서비스와 정산 서비스를 각자의 root build로 운영하고, 둘이 같은 "회사 표준 java convention", "회사 표준 Spring Boot convention"을 따르고 싶은 상황이다. `buildSrc/`로는 이 일이 안 된다. `buildSrc/`는 자신이 속한 root build의 부속물이지 독립적인 산출물이 아니다. 결국 둘 중 한 쪽에 `buildSrc/`를 두고 다른 쪽에 복사해두는, 혹은 사내 Maven에 plugin을 publish하는 식으로 우회해야 한다. 복사는 곧 drift의 시작이고, publish는 별도 발행 절차를 끌어들인다. 어느 쪽이든 가볍지 않다.

세 번째 그림자는 좀 더 미묘하다. **classpath 충돌**. `buildSrc/`의 classpath에는 우리가 의존성으로 추가한 라이브러리, 그리고 적용한 plugin들의 transitive 의존성이 다 들어간다. 예를 들어 우리가 `spring-boot-gradle-plugin`을 buildSrc에 의존성으로 넣으면 그 plugin이 끌고 오는 모든 라이브러리가 buildSrc의 classpath에 있게 된다. 그게 또 다른 plugin이 끌고 오는 라이브러리와 버전 충돌을 일으키면 디버깅이 답답해진다. 빌드 로직이 자라면 자랄수록 이 마찰면이 넓어진다.

이 세 가지 — 변경 시 전체 out-of-date, 재사용 불가, classpath 충돌 — 가 회사 빌드가 일정 규모를 넘으면서 buildSrc를 답답하게 만드는 정확한 지점들이다. 한 가지만 부딪쳐도 충분한 동기가 되는데, 회사 빌드는 종종 셋 다를 동시에 만난다. 그러니 처방이 필요한 시점이 온다.

## included build라는 개념

처방의 이름은 **included build**다. 별로 새로운 단어는 아니다. 1장에서 짧게 settings.gradle.kts를 봤을 때, `include("app", "domain", "order", "payment")`가 등장했다. 이건 root build 안에 subproject를 등록하는 함수다. `includeBuild`는 그것과 비슷한 모양이지만 결정적으로 한 글자 더 길고, 의미는 크게 다르다. **별개의 Gradle 빌드를 한 트리에 묶는다**. 그게 핵심이다.

`include`로 등록된 subproject는 root build와 같은 settings를 공유하는 한 빌드의 부속이다. 같은 wrapper, 같은 plugin management, 같은 dependency resolution management. 반면 `includeBuild`로 묶인 included build는 그 자체로 **독립적인 Gradle 빌드**다. 자기 settings.gradle.kts를 갖고, 원한다면 자기 wrapper도 갖고, 자기 plugin management도 갖는다. root build가 그걸 어떤 식으로 끌어다 쓰는지의 약속만 존재한다.

이 약속이 어떻게 생겼냐가 핵심이다. Gradle은 included build가 발행하는 산출물의 좌표(group:name)를 본다. root build에서 누군가 `org.example.shop:build-logic`이라는 좌표의 의존성을 요청한다면, 그 좌표를 가진 included build가 있는지 본다. 있다면 외부 저장소에 가지 않고 included build의 산출물로 자동 치환한다. **dependency substitution**이 자동으로 일어나는 셈이다.

이 자동 치환 메커니즘이 두 가지 시나리오를 풀어준다. 하나는 우리 관심사인 build-logic 분리다. `buildSrc/`였던 산출물을 별개의 빌드로 옮기고, root에서 `includeBuild`로 끌어 쓰는 식이다. 다른 하나는 외부 라이브러리와의 co-development다. 회사의 다른 팀이 만드는 라이브러리를 매번 사내 Maven에 publish하지 않고도 우리 앱 빌드 옆에 두고 같이 돌리는 식이다. 같은 메커니즘으로 둘 다 풀린다는 게 included build의 아름다움이다.

다만 두 시나리오의 무게는 다르다. Spring Boot 백엔드를 운영하는 일상에서 **build-logic 분리는 흔하고**, 외부 라이브러리 co-development는 가끔이다. 그래서 이 장의 본문은 build-logic 분리에 집중하고, co-development는 뒤에서 박스로 짧게 다룬다. 어느 쪽이든 같은 `includeBuild` 한 줄로 시작한다는 사실을 먼저 잡아두면 충분하다.

## `buildSrc/`를 `build-logic/`으로 옮긴다

이제 실제로 옮겨보자. 시작점은 10장 마지막의 `ch09-convention/` 구조다. 모습은 이렇다.

```
ch09-convention/
├── settings.gradle.kts
├── build.gradle.kts
├── gradle/libs.versions.toml
├── buildSrc/
│   ├── settings.gradle.kts
│   ├── build.gradle.kts
│   └── src/main/kotlin/
│       ├── shop.java-conventions.gradle.kts
│       └── shop.spring-boot-conventions.gradle.kts
├── app/build.gradle.kts
├── domain/build.gradle.kts
├── order/build.gradle.kts
└── payment/build.gradle.kts
```

목표 구조는 `buildSrc/`만 `build-logic/`으로 갈아 끼우는 모양이다. 즉 다음과 같다.

```
ch11-composite/
├── settings.gradle.kts        # ← pluginManagement에 includeBuild 추가
├── build.gradle.kts
├── gradle/libs.versions.toml
├── build-logic/               # ← 새로 등장. 독립된 Gradle build.
│   ├── settings.gradle.kts    # ← 자체 settings 필요
│   ├── build.gradle.kts
│   └── src/main/kotlin/
│       ├── shop.java-conventions.gradle.kts
│       └── shop.spring-boot-conventions.gradle.kts
├── app/build.gradle.kts
├── domain/build.gradle.kts
├── order/build.gradle.kts
└── payment/build.gradle.kts
```

이름이 `buildSrc`가 아니라 `build-logic`이라는 점이 한 가지 차이다. `buildSrc`라는 이름은 Gradle이 자동으로 인식하는 magic name이라서, 다른 이름을 쓰려면 root settings에서 명시적으로 `includeBuild`를 적어야 한다. 관습적으로 그 이름이 `build-logic`이다. 사실상 표준에 가깝다.

순서대로 따라가보자. 마이그레이션은 네 단계로 정리된다.

**1단계: `build-logic/` 폴더 만들고 `buildSrc/`의 내용 복사.**

`buildSrc/`의 모든 파일을 `build-logic/` 폴더로 복사한다. `settings.gradle.kts`, `build.gradle.kts`, `src/main/kotlin/` 안의 두 convention plugin 모두.

```bash
mv buildSrc build-logic
```

이 순간 build는 깨진다. Gradle이 `buildSrc/`라는 magic name 폴더를 못 찾으니 convention plugin들이 사라진 것처럼 보인다. 그 다음 단계에서 회복시킨다.

**2단계: `build-logic/settings.gradle.kts`를 standalone build답게 보강.**

`buildSrc/` 시절의 settings는 거의 비어 있을 수 있었다. Gradle이 알아서 처리해줬다. 하지만 `build-logic/`은 이제 독립된 build다. 자기 plugin management와 dependency resolution management를 명시적으로 적어야 한다.

```kotlin
// build-logic/settings.gradle.kts
rootProject.name = "build-logic"

dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}
```

`rootProject.name`은 build-logic 자체의 이름이다. 다른 빌드에서 이 이름으로 인식한다. `dependencyResolutionManagement`는 build-logic 안에서 plugin 의존성을 받을 저장소를 명시한다. `gradlePluginPortal()`이 핵심이다 — Spring Boot Gradle plugin, kotlin-dsl plugin 같은 plugin들이 여기서 온다.

`pluginManagement`도 필요할까. `buildSrc/`였을 때는 굳이 따로 적지 않아도 root build의 pluginManagement를 상속받는 것처럼 동작했다. `build-logic/`은 독립이라 상속이 없다. 다만 build-logic 자체가 plugin을 적용하는 일이 흔하지는 않다 — 안에 든 건 거의 다 자기가 발행하는 convention plugin이다. 그래서 `pluginManagement {}`는 비워 둬도 큰 문제가 없다. 필요한 시점에 추가하자.

**3단계: `build-logic/build.gradle.kts`를 다시 본다.**

`buildSrc/` 시절의 build.gradle.kts는 보통 이렇게 생겼다.

```kotlin
plugins {
    `kotlin-dsl`
}

repositories {
    gradlePluginPortal()
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-gradle-plugin:4.0.6")
}
```

이걸 그대로 `build-logic/build.gradle.kts`로 복사한다. 다만 `repositories {}` 블록은 이제 build-logic의 settings에서 dependencyResolutionManagement로 잡아 두었으니, 사실 비워 둬도 된다. `RepositoriesMode.FAIL_ON_PROJECT_REPOS`를 settings에서 켰다면 오히려 여기서 repositories를 또 적으면 빌드가 실패한다. 깔끔하게 비워 두자.

```kotlin
// build-logic/build.gradle.kts
plugins {
    `kotlin-dsl`
}

dependencies {
    implementation("org.springframework.boot:spring-boot-gradle-plugin:4.0.6")
}
```

`kotlin-dsl` plugin은 그대로 살아 있어야 한다. 이 plugin이 `*.gradle.kts` precompiled convention plugin들을 자동으로 binary plugin으로 컴파일해주는 핵심 도구다. 10장에서 만난 메커니즘이 그대로 살아남는 셈이다.

**4단계: root의 `settings.gradle.kts`에서 `includeBuild`로 끌어 쓴다.**

이게 마이그레이션의 마지막 한 줄이다. 그리고 가장 흥미로운 한 줄이기도 하다.

```kotlin
// ch11-composite/settings.gradle.kts
pluginManagement {
    includeBuild("build-logic")
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

rootProject.name = "shop"
include("app", "domain", "order", "payment")
```

핵심은 `pluginManagement { includeBuild("build-logic") }` 한 줄이다. 이 한 줄이 무슨 약속을 만드는가. **plugin id를 해결할 때 build-logic 빌드를 먼저 보라**는 약속이다. 우리 모듈들이 `plugins { id("shop.java-conventions") }`라고 적으면, Gradle은 그 plugin id를 가진 빌드가 build-logic이라는 included build 안에 있는지 본다. 있으니 거기서 끌어 쓴다.

여기서 한 가지 미묘한 점. `includeBuild`를 root 수준이 아니라 `pluginManagement {}` 블록 안에 적었다. 왜냐하면 우리가 원하는 건 build-logic의 산출물을 **일반 의존성**으로 쓰는 게 아니라 **plugin**으로 쓰는 일이기 때문이다. plugin 해결 경로는 일반 의존성 해결 경로와 다르다. plugin은 settings 단계에서 plugin management가 먼저 처리한다. 그래서 `pluginManagement` 안에 `includeBuild`를 넣는 모양이 정확하다.

만약 build-logic이 plugin뿐 아니라 일반 library도 발행한다면(예: Kotlin 헬퍼 함수 패키지를 한 모듈에 공유 library로 쓰고 싶다면) root 수준에도 `includeBuild("build-logic")`을 추가로 적는 식이 된다. 다만 그런 경우는 흔하지 않다. 회사 빌드에서 build-logic은 거의 항상 plugin 발행만 한다.

자, 이제 빌드를 돌려보자.

```bash
./gradlew :app:bootRun
```

처음에는 build-logic 자체가 컴파일되는 task가 추가로 도는 게 보인다. 그 다음은 우리가 10장에서 본 익숙한 흐름이다. 4개 모듈이 빌드되고, 앱이 뜬다. 외형적 동작은 완전히 같다. **convention plugin들은 한 줄도 안 고쳤다.** 우리가 한 일은 그 plugin들이 사는 동네를 옮긴 것뿐이다.

> **함정 — root 수준 `includeBuild` vs `pluginManagement.includeBuild`**
>
> 두 자리에 `includeBuild`가 등장한다는 사실은 종종 혼란을 부른다. 차이를 한 줄로 정리하자.
>
> - **`pluginManagement { includeBuild(...) }`** — included build의 plugin id를 root에서 적용할 수 있게 한다. Convention plugin을 끌어다 쓸 때 거의 항상 이 자리다.
> - **root 수준의 `includeBuild(...)`** — included build가 발행하는 **일반 의존성**의 좌표를 root build의 `dependencies`에서 끌어다 쓸 수 있게 한다. 예: `implementation("com.example:shop-shared:1.0")`을 included build로 자동 치환.
>
> 둘 중 어느 쪽이 필요한지는 included build가 무엇을 발행하느냐로 정해진다. build-logic이 convention plugin만 발행하면 `pluginManagement` 쪽만, 라이브러리도 같이 발행하면 두 자리 모두 적는다. 두 자리에 같이 적는 일도 흔하다.

## buildSrc였을 때와 무엇이 정확히 달라지는가

옮긴 결과로 우리가 손에 쥔 변화를 정확히 짚어보자. 막연하게 "더 좋아진다"가 아니라, 어디서 어떤 비용이 줄어드는지를 보는 편이 빌드를 운영하는 데에 도움이 된다.

**첫째, 변경 영향 범위가 좁아진다.** `build-logic/`은 root build와 분리된 별개의 빌드다. 그 안의 파일이 바뀌면 build-logic 자체는 다시 컴파일된다. 다만 root build 입장에서는 build-logic이 발행하는 plugin의 산출물(jar)이 바뀌었다는 정보를 받는다. 그 plugin이 적용된 모듈들의 task만 영향을 받는다. 적용 안 된 모듈은 무관하다. 게다가 build-logic의 변경 자체가 정말 plugin 산출물에 영향을 줬는지를 Gradle이 본다. 주석 한 줄 같은 ABI에 영향 없는 변경은 task graph 입장에서 변화가 없을 수도 있다. `buildSrc/` 시절의 "모든 task가 보수적으로 out-of-date"되는 모습과는 다르다.

이 차이가 가장 크게 느껴지는 자리는 회사 빌드처럼 build logic이 자주 진화하는 환경이다. 누군가 convention plugin을 손보고 PR을 올리면, CI는 build-logic 자체와 변경에 영향받는 모듈들만 다시 빌드한다. 다른 모듈들의 Build Cache가 살아남는다. 결과적으로 CI 시간이 짧아지고, 캐시 사용 효율이 올라간다.

**둘째, classpath 분리가 명확해진다.** `build-logic/`은 자기 build.gradle.kts와 settings.gradle.kts를 갖는다. 거기서 들어오는 의존성은 build-logic의 classpath 안에 갇힌다. root build의 plugin classpath와 분리된다. 두 곳에서 다른 버전의 같은 라이브러리를 들이고 싶을 때 이 분리가 자유를 준다. `buildSrc/` 시절에는 한 classpath 안에서 충돌이 정면으로 일어났다.

**셋째, 재사용 가능성이 열린다.** `build-logic/`은 standalone Gradle build다. 다른 root build에서도 같은 `includeBuild("../build-logic")`으로 끌어 쓸 수 있다. 결제 서비스와 정산 서비스가 각자의 root build를 갖고 있되, 둘 다 같은 `../shared/build-logic`을 included build로 끌어 쓰는 식이다. 회사 표준이 한 곳에서 살아 움직이고, 각 서비스의 root build는 거기에 정렬된다. 사내 Maven에 plugin을 publish하지 않고도 이게 가능하다는 게 included build의 매력이다.

**그렇다면 buildSrc는 죽었나?** 그렇지 않다. 10장 마지막에서 짧게 적어둔 자세를 다시 가져오자. **회사 빌드가 작으면 `buildSrc/`로 충분히 만족스럽다.** 모듈 수가 열 개 미만이고, build logic 변경 빈도가 낮고, 한 root build에서만 쓰면 되는 상황이라면 `buildSrc/`가 가장 가벼운 답이다. `build-logic`은 standalone build를 운영하는 만큼 작은 운영 비용이 따라온다 — 자체 settings 관리, includeBuild 한 줄 추가, 두 빌드를 한 IntelliJ 창에서 동시에 추적하기. 그 비용을 정당화할 만큼 build logic이 자라거나 재사용이 필요한 시점이 와야 의미가 있다.

좋은 소식은 buildSrc에서 build-logic으로의 마이그레이션이 어렵지 않다는 점이다. 방금 본 네 단계가 전부고, convention plugin 자체는 한 줄도 안 바뀐다. 그러니 처음부터 욕심을 내서 build-logic으로 시작하기보다는 buildSrc로 정착하고, 답답함이 누적된 시점에 옮기는 편이 자연스럽다. 빌드 도구를 단번에 완벽하게 만들려는 시도는 거의 항상 과도한 일반화로 빠진다.

## Composite Build의 본질을 한 번 더 짚는다

여기서 잠깐 한 박자를 쉬고, 우리가 방금 한 일의 정체를 큰 시야에서 다시 보자. `build-logic`을 included build로 끌어 들이는 패턴 — 이게 사실 **Composite Build**의 한 사례다. Composite Build라는 단어가 거창하게 들리지만, 본질은 한 줄로 표현된다.

> **별개의 Gradle 빌드를 한 트리에 묶는다.**

그게 전부다. root build와 included build가 각각 독립된 Gradle 빌드이되, 한 명령(`./gradlew`)으로 함께 실행될 수 있고, 산출물의 좌표가 매칭되면 외부 저장소를 거치지 않고 서로의 산출물을 substitution한다.

Gradle 공식 문서가 Composite Build의 세 가지 용도를 든다. (a) 빌드 로직의 분리, (b) 라이브러리와 소비자의 동시 개발, (c) monorepo 구성. 셋 다 같은 `includeBuild` 메커니즘 위에서 일어난다. 이 장에서 깊게 다루는 건 (a)다. Spring Boot 백엔드 개발자가 일상에서 가장 자주 부딪치는 용도이기 때문이다. 나머지 두 용도는 다음 박스에서 짧게 본다.

> **언제 co-development와 monorepo 구성이 필요한가**
>
> Composite Build의 나머지 두 용도는 회사 상황이 그걸 요구할 때 짧게 적용하는 도구다. 깊게 들어가지 않고, "언제 이 패턴이 필요한가"만 잡아두자.
>
> **(1) 외부 라이브러리와의 co-development.** 회사의 platform 팀이 만드는 공통 라이브러리 `shop-shared`가 있다고 해 보자. 평소에는 그 팀이 사내 Maven에 publish하고, 우리 앱은 `implementation("com.example:shop-shared:1.0")`으로 끌어다 쓴다. 그런데 어느 날 그 라이브러리 안에 버그가 있어서 우리 팀이 직접 PR을 만들어야 한다고 해 보자. 사내 Maven에 1.0.1-SNAPSHOT을 push하고, 우리 앱 빌드에서 그 SNAPSHOT 버전을 쓰고, 다시 push하고… 매번 publish-fetch 왕복이 답답하다.
>
> 이 자리에 `includeBuild`가 들어간다. 우리 앱의 root settings에 한 줄을 적는다.
>
> ```kotlin
> // settings.gradle.kts
> includeBuild("../shop-shared")
> ```
>
> 그러면 빌드를 돌릴 때 `com.example:shop-shared:1.0`이라는 좌표를 외부 저장소에서 끌어 오는 대신, 옆 폴더에 있는 `shop-shared` 빌드의 산출물로 자동 substitution한다. 우리는 두 빌드를 같은 IntelliJ 창에서 열어 두고, 라이브러리 쪽 코드를 고치고, 우리 앱 쪽에서 즉시 그 변경을 확인한다. publish-fetch 왕복이 사라진다. PR을 마무리할 때 `includeBuild` 한 줄을 지우거나 주석 처리하면 다시 정상 좌표 의존으로 돌아간다.
>
> **(2) Monorepo 구성.** 여러 개의 독립된 Gradle 빌드를 한 git repo 안에 묶고 싶을 때다. 예를 들어 결제 서비스와 정산 서비스가 각자의 root build를 갖되 한 repo에서 함께 진화하는 모양. 최상위에 우산 역할의 작은 root build를 두고, 각 서비스를 `includeBuild`로 묶는다. 한 명령으로 둘 다 빌드하는 일이 가능해진다. 다만 monorepo는 빌드 도구 외에도 git 운영·CI 분리·소유권 모델 같은 큰 의사결정이 따라온다. Composite Build는 그 그림의 한 조각일 뿐이다.
>
> 두 용도 모두 Spring Boot 백엔드의 일상 빈도는 낮다. 다만 만났을 때 정답이 무엇인지를 알아두면 그 자리에서 답답하지 않을 수 있다.

## dependency substitution이 매칭되지 않을 때

자동 substitution이 일어나려면 좌표(group:name)가 정확히 매칭돼야 한다. included build가 자기를 `com.example:shop-shared`라는 group:name으로 발행하고, 소비자 쪽에서도 같은 좌표를 의존성으로 요청해야 자동으로 묶인다. 거의 모든 경우는 이 매칭이 잘 일어나고 우리가 따로 신경 쓸 일이 없다. 다만 가끔 매칭이 어긋나는 상황이 있다.

가장 흔한 경우는 included build의 `group`이 비어 있거나 다른 group으로 잡혀 있을 때다. 사내 정책으로 인해 좌표가 의도와 다르게 발행되는 식이다. 이 자리에서 사용하는 도구가 **명시적 substitution**이다.

```kotlin
// settings.gradle.kts (소비자 쪽)
includeBuild("../shop-shared") {
    dependencySubstitution {
        substitute(module("com.example:shop-shared"))
            .using(project(":"))
    }
}
```

`substitute(module(...))`로 "이 외부 좌표를 보면" 약속을 적고, `.using(project(...))`로 "이 included build 안의 어느 프로젝트로 갈아 끼운다"를 적는다. `:`은 included build의 root project를 가리킨다. included build가 멀티 프로젝트면 `:lib`, `:core` 같은 path가 들어간다.

이 명시적 substitution은 자동 매칭이 안 될 때만 쓴다. 자동이 잘 동작하면 굳이 적을 필요가 없다. 다만 "왜 substitution이 안 일어나지?"라는 의문이 생겼을 때 가장 먼저 의심할 자리가 group:name 불일치다. included build의 `build.gradle.kts`를 열어서 `group`이 무엇인지 확인하고, 소비자 쪽이 요청하는 좌표와 정확히 매칭되는지 본다. 두 좌표가 맞으면 끝이다. 안 맞으면 위 박스의 명시적 substitution으로 해결한다.

## 선택 가이드: 어떤 모양을 언제 쓰나

이 장에서 본 세 가지 모양 — `buildSrc + convention plugin`, `build-logic included build`, 그리고 Composite Build를 통한 co-development — 을 회사 상황에 어떻게 매핑하는지 한 줄짜리 가이드로 정리하자. 자기 회사 빌드를 점검할 때 이 표 하나를 떠올리는 편이 낫다.

| 상황 | 선택 |
|---|---|
| 단일 root, 모듈 수 < 10, build logic 변경 빈도 낮음 | **buildSrc + convention plugin** |
| 모듈 많거나 build logic 자주 진화, 또는 여러 root build에서 재사용 | **build-logic included build** |
| 외부 라이브러리를 publish 없이 동시 개발 | **Composite Build (`includeBuild`로 라이브러리 끌어들임)** |

이 표를 외울 필요는 없다. 다만 한 가지 마음가짐만 가져가자. **빌드 도구의 구조는 회사 빌드의 현재 상태에 맞는 것이 정답이다.** 처음부터 가장 일반적인 도구(build-logic + Composite Build)를 도입하려는 욕심을 누르자. buildSrc로 충분한 회사가 build-logic을 적용하면 운영 비용이 작은 마찰로 누적된다. 반대로 buildSrc로 답답한 회사가 buildSrc를 고집하면 변경 비용이 큰 마찰로 누적된다. 자기 회사 빌드의 답답함이 정확히 어디서 오는지를 본 다음, 그 답답함을 푸는 도구를 고르자.

그리고 한 가지 더. **세 모양 사이의 마이그레이션은 모두 가볍다**. buildSrc → build-logic은 이 장에서 본 네 단계다. 평소 잘 굴러가는 buildSrc를 굳이 미리 옮길 필요가 없다. 답답함이 생기는 시점에 옮기면 된다. co-development의 `includeBuild` 한 줄은 PR을 마무리할 때 지우면 된다. 도구를 가볍게 들이고 가볍게 내릴 수 있다는 자신감이 빌드 운영의 핵심이다.

## 11장을 닫으며

Part III의 첫 머리에서 우리는 모듈을 쪼개기로 했다. 8장에서 단일 모듈 앱을 4개 모듈로 분리했고, 빌드가 정상 동작하지 않는 사고를 만났다. 9장에서 그 사고가 `bootJar` 함정에서 비롯됐음을 진단하고 두 가지 처방으로 빌드를 정상화했다. 그 다음 10장에서 4개 모듈의 build.gradle.kts에 남은 중복을 `buildSrc/`의 convention plugin으로 정리했다. 그리고 이번 11장에서 그 `buildSrc/`의 그림자를 들여다보고, `build-logic`이라는 included build로 승격시키는 길을 봤다. Composite Build라는 더 일반적인 개념이 그 길의 바탕이라는 사실도 한 번 짚었다.

지금 우리의 `ch11-composite/` 폴더 모습은 이렇다. root settings가 `pluginManagement { includeBuild("build-logic") }` 한 줄을 갖고 있다. `build-logic/`은 standalone Gradle build로 살아 있고, 그 안에 10장에서 만든 두 개의 convention plugin이 그대로 들어가 있다. 4개 모듈의 build.gradle.kts는 여전히 plugin 한 줄짜리다. JDK를 올리는 결정, BOM을 올리는 결정, JUnit Platform을 강제하는 결정은 모두 한 곳에서 일어난다. 그 한 곳이 root build 안의 `buildSrc/`였던 자리에서 root build 옆의 `build-logic/`으로 옮겨갔을 뿐이다. 우리가 빌드를 정의하는 방식의 표면 모양은 거의 그대로다. 다만 변경의 영향 범위가 좁아지고, 재사용 가능성이 열리고, classpath가 분리된 셈이다.

여기까지가 Part III "규모를 키운다"의 마지막 장이다. 한 번 회고해보자. 우리는 8~11장에서 빌드의 사회적 측면을 다뤘다 — 한 사람이 한 모듈을 책임지던 빌드를, 여러 모듈이 협력하고 여러 사람이 함께 만지는 빌드로 옮긴 과정이다. 이 사회적 측면을 다루는 도구들이 멀티 모듈, convention plugin, build-logic include build였다. 회사 빌드가 이 세 도구 위에 정렬돼 있다면 여러 명이 한 빌드를 만져도 마찰이 작다. 그게 Part III가 약속한 자리다.

자, 이제 우리의 관심사가 한 번 더 옮겨간다. Part IV의 주제는 **빌드를 도구로 만든다**이다. 지금까지 우리는 빌드 도구의 **소비자**였다. Spring Boot Gradle plugin이 만들어 준 task를 썼고, JVM Test Suite plugin이 만들어 준 task를 썼고, 외부에서 가져온 plugin들의 행동을 조정했다. 12장부터는 빌드 도구의 **생산자**로 옮긴다. 우리 회사 빌드에만 의미 있는 task와 plugin을 우리가 직접 만든다. Git SHA를 파일로 떨궈주는 task 하나를 시작점으로, Provider/Property API와 Configuration Cache 친화적인 커스텀 plugin의 정석을 손에 익힌다.

그리고 그 plugin이 사는 자리가 어디일까. 바로 이 장에서 만든 `build-logic/`이다. 우리가 만들 커스텀 plugin은 새 폴더에 들어가는 게 아니라, 이미 살아 움직이는 `build-logic/` 안에 자연스럽게 추가된다. Part III에서 만든 토대가 Part IV의 작업대가 되는 셈이다. 빌드 도구가 자라는 모습이 이런 식이다 — 한 번 잘 정리해 둔 토대 위에 다음 도구가 자연스럽게 얹힌다. 12장에서 이어서 만나자.
