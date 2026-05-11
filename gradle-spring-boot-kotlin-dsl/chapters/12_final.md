# 12장. 커스텀 Task와 Plugin — Provider/Property로 lazy하게

배포가 끝난 운영 환경에서 누가 묻는다. "지금 배포된 게 어느 커밋이에요?" 우리는 머쓱하게 GitHub Actions 로그를 뒤지거나, `git log`를 시간대로 좁히면서 추측한다. 한두 번이면 괜찮다. 하루에 세 번씩 배포가 나가는 팀이라면 이건 곧 피곤한 일이 된다.

답은 단순하다. 빌드 시점에 git SHA를 파일 하나에 떨궈서 jar 안에 같이 넣자. Spring Boot 앱은 부팅 때 그 파일을 읽어 `/actuator/info`에 노출한다. 누가 물으면 URL 하나로 답할 수 있다.

그런데 막상 task를 하나 만들려고 build.gradle.kts를 펴면 손이 멈춘다. `tasks.register("buildInfo")` 안에 doLast로 `"git rev-parse HEAD"`를 실행하면 될 것 같은데, 막상 Gradle 9.x 문서를 보면 `providers.exec`, `Property<String>`, `RegularFileProperty`, `abstract class` 같은 단어들이 같이 나온다. 도대체 왜 이렇게 복잡할까. 한 줄짜리 git 명령어 하나 떨구는 데 클래스를 하나 만들어야 한다고?

이 챕터의 핵심 질문이 이거다. **Git SHA를 파일로 떨궈주는 task 하나를 만들고 싶다. 그런데 Configuration Cache와 호환되게.** 마지막 한 줄이 게임의 규칙을 바꾼다. 그 한 줄이 없다면 doLast 안에 `"git rev-parse HEAD".runCommand()` 한 줄로 끝낼 수 있다. 그 한 줄이 있기 때문에 우리는 lazy Property API를 진지하게 익혀야 한다.

3장에서 한 번 약속했었다. "본격적인 Property/Provider API 다이브는 12장에서 다룬다"고. 약속을 지킬 시간이다. 그리고 11장에서 만든 `build-logic` included build가 비로소 진짜 일을 받아간다. `shop.build-info`라는 우리만의 plugin을 거기에 심자. app은 `id("shop.build-info")` 한 줄로 그 plugin을 받아 쓰고, `/actuator/info`로 자기가 어느 커밋인지를 답한다. 8,000자 짜리 코스다. 천천히 가자.

## 한 줄짜리 사고 실험 — 왜 안 되는가

먼저 모범 답안을 보기 전에, 본능적으로 떠오르는 코드부터 적어보자. Gradle을 처음 배우면 누구나 이 모습으로 시작한다.

```kotlin
// app/build.gradle.kts — 안 되는 코드
tasks.register("buildInfo") {
    doLast {
        val sha = ProcessBuilder("git", "rev-parse", "HEAD")
            .start().inputStream.bufferedReader().readText().trim()
        val builtAt = java.time.Instant.now().toString()
        val out = file("src/main/resources/build-info.txt")
        out.writeText("git=$sha\nbuilt=$builtAt\n")
    }
}

tasks.named("processResources") {
    dependsOn("buildInfo")
}
```

`./gradlew bootJar`를 돌려보면 동작한다. `build/libs/app.jar`를 열어보면 안에 `build-info.txt`가 들어 있고, git SHA가 적혀 있다. 일단 작동한다.

그런데 빌드를 두 번째로 돌려보자.

```bash
$ ./gradlew bootJar
> Task :buildInfo
> Task :processResources
> Task :bootJar

BUILD SUCCESSFUL in 8s
$ ./gradlew bootJar
> Task :buildInfo
> Task :processResources
> Task :bootJar

BUILD SUCCESSFUL in 8s
```

코드를 한 줄도 안 바꿨는데 매번 8초가 걸린다. `buildInfo` task가 매번 다시 실행되니까, 그게 입력으로 쓰이는 `processResources`도, 그게 다시 입력이 되는 `bootJar`도 매번 다시 실행된다. 한 task의 어리석음이 빌드 그래프 전체로 번진다.

여기서 한국어 블로그에서 흔히 보는 해결책이 등장한다.

```kotlin
tasks.register("buildInfo") {
    outputs.upToDateWhen { false }   // 매번 실행하라는 뜻
    doLast { ... }
}
```

"이게 매번 실행되게 해주는 마법의 한 줄이에요" 같은 설명과 함께. 그런데 이 한 줄은 문제를 푸는 게 아니다. **문제를 영구화하는 코드**다. 13장에서 만날 Build Cache 입장에서 보면 이 task는 영원히 캐시 불가다. 입력이 바뀌지 않아도 매번 실행되니까 출력도 매번 다시 만든다. 멀티 모듈에서 이 task 하나가 빌드 그래프 절반의 캐시를 무효화한다. 진짜 답은 따로 있다. Gradle한테 "이 task의 입력은 무엇이고 출력은 무엇인지"를 정직하게 알려주는 것이다.

좀 더 깊은 문제도 있다. 위 코드는 Configuration Cache가 켜진 순간 비명을 지른다.

```bash
$ ./gradlew bootJar --configuration-cache
> Task :buildInfo FAILED
* What went wrong:
  invocation of 'Task.project' at execution time is unsupported
```

`file(...)`은 내부적으로 `Task.getProject()`를 호출한다. `ProcessBuilder`는 Gradle이 추적하지 못하는 외부 IO다. 둘 다 9.x의 Configuration Cache가 명시적으로 거부하는 패턴이다. 13장에서 우리는 Configuration Cache를 켤 예정이다. 그때 이 task가 발목을 잡으면 곤란하다.

그러니 처음부터 제대로 만들자. 다행히 "제대로"의 길은 한 갈래로 잘 닦여 있다.

## `abstract class` + `Property<T>` 패턴

Gradle 9.x에서 새로 task를 만든다면 답은 거의 항상 같은 모습으로 시작한다.

```kotlin
abstract class GenerateBuildInfoTask : DefaultTask() {

    @get:Input
    abstract val gitSha: Property<String>

    @get:Input
    abstract val builtAt: Property<String>

    @get:OutputFile
    abstract val outputFile: RegularFileProperty

    @TaskAction
    fun run() {
        val target = outputFile.get().asFile
        target.parentFile.mkdirs()
        target.writeText("git=${gitSha.get()}\nbuilt=${builtAt.get()}\n")
    }
}
```

한 줄씩 풀어보자.

**`abstract class`.** Gradle 5쯤부터 권장되어 오던 패턴이 9.x에 와서 사실상 표준이 됐다. 클래스를 abstract로 선언하면, 그 안의 `abstract val` 프로퍼티들에 대한 구현체를 **Gradle이 런타임에 자동으로 만들어준다.** 우리가 손으로 `private val _gitSha = objectFactory.property(String::class.java)` 같은 보일러플레이트를 적을 필요가 없다. 옛날 책에서 본 그런 코드는 잊어버려도 좋다.

**`Property<String>`과 `RegularFileProperty`.** 이게 lazy Property API의 본체다. 보통 변수 같으면 `String`을 쓰면 될 것 같은데 왜 한 단계를 더 감싸는가? 그 한 단계가 **"값을 지금 결정하지 않아도 된다"는 약속**을 만들기 때문이다. configuration phase에서 우리는 `gitSha`에 값을 넣는다고 적기만 한다. 그 값이 실제로 평가되는 건 task가 실행될 때, 즉 `gitSha.get()`이 호출되는 순간이다. Provider/Property는 "약속을 들고 있는 박스"라고 생각하면 편하다. 박스를 만드는 일과, 박스를 여는 일이 다른 시점에 일어난다.

**`@Input` / `@OutputFile` 어노테이션.** 이게 incremental build와 build cache 양쪽의 핵심이다. Gradle은 이 어노테이션을 보고 "이 task의 입력은 `gitSha` 문자열과 `builtAt` 문자열, 출력은 `outputFile`이다"라고 이해한다. 그러면 다음 빌드에서 두 입력의 해시가 똑같고 출력 파일이 그대로 있다면, Gradle은 task를 다시 실행하지 않는다. UP-TO-DATE라고 적고 0초 만에 넘어간다. `outputs.upToDateWhen { false }`로 강제 실행하던 것과 정반대 세계다.

**`@TaskAction`.** 이게 실제로 무엇을 할지를 적는 자리다. 한 가지만 기억해두자. `@TaskAction` 함수 안에서는 **`project.something`을 호출하면 안 된다.** Configuration Cache가 막는다. 필요한 값은 모두 `Property`로 받아서 `.get()`으로 꺼내 써야 한다. 처음엔 답답하지만, 이 제약 덕분에 Gradle은 task를 다른 빌드와 격리해서 실행할 수 있고, 캐시할 수 있다.

자, 클래스는 만들었다. 이제 이걸 어떻게 등록하고 git SHA를 어떻게 채워줄지가 다음 문제다.

## `providers.exec`로 git을 부른다 — 정직하게

git SHA를 가져오려면 `git rev-parse HEAD`를 실행해야 한다. 그런데 Gradle에서 외부 명령어를 부르는 길은 두 가지가 있다. 옛날 길과 새 길.

옛날 길:

```kotlin
val sha = project.exec {
    commandLine("git", "rev-parse", "HEAD")
    standardOutput = System.out
}
```

이 코드는 6.x까지는 거의 모든 책에 등장했다. 그런데 Gradle 9.x에서 이 코드는 두 가지 죄를 짓는다. 첫째, `project.exec`는 호출되는 순간 명령어가 즉시 실행된다. configuration phase에서 호출하면 configuration phase에서 git을 부른다. 매번 다시. Configuration Cache가 캐시한 결과를 다시 쓰는 길을 막아버린다. 둘째, execution phase에서 이걸 호출하면 `Task.getProject()`를 깨우는 셈이라 Configuration Cache 위반이다. 위든 아래든 9.x에서는 길이 막혀 있다.

새 길:

```kotlin
val gitShaProvider: Provider<String> = providers.exec {
    commandLine("git", "rev-parse", "HEAD")
}.standardOutput.asText.map { it.trim() }
```

이 한 줄이 옛날 길의 모든 문제를 한 번에 푼다. 풀이를 천천히 보자.

`providers.exec { ... }`는 `ExecOutput`이라는 객체를 돌려준다. 중요한 건 **이 시점에 git이 실행되지 않는다**는 것이다. providers.exec는 "git을 어떻게 부를지에 대한 레시피"만 들고 있다. 그 레시피는 lazy하다. 누군가 `.standardOutput.asText.get()`을 호출하는 순간에야 비로소 git이 실행된다.

`.standardOutput.asText`는 git의 stdout을 `Provider<String>`으로 감싼다. 그리고 `.map { it.trim() }`은 결과 문자열을 다듬는 변환을 lazy하게 얹는다. 이 map 역시 즉시 실행되지 않는다. 다 합쳐서 이 한 줄은 **"git rev-parse HEAD를 실행해서 stdout을 받아 trim한 문자열"이라는 약속을 들고 있는 Provider 하나**다.

이 약속을 우리 task에 넘겨준다.

```kotlin
tasks.register<GenerateBuildInfoTask>("buildInfo") {
    gitSha = providers.exec {
        commandLine("git", "rev-parse", "HEAD")
    }.standardOutput.asText.map { it.trim() }

    builtAt = providers.provider {
        java.time.Instant.now().toString()
    }

    outputFile = layout.buildDirectory.file("generated/build-info.txt")
}
```

`gitSha`는 `Property<String>` 타입이지만 `=` 연산자로 Provider를 그대로 대입할 수 있다. Kotlin DSL이 setter를 깔끔하게 위임해준다. 이게 3장에서 살짝 본 `=` 권장 패턴의 본격적인 모습이다.

`builtAt`은 `providers.provider { ... }`로 만든다. 람다 안의 코드는 task가 실행될 때 평가된다. 그래서 매 빌드의 "지금 시각"이 자연스럽게 잡힌다.

`outputFile`은 `layout.buildDirectory.file("generated/build-info.txt")`로 적는다. `File("build/generated/...")`나 `project.buildDir.resolve(...)` 같은 옛 방식 대신, 이 한 줄이 `RegularFileProperty`를 lazy하게 만들어준다. `layout` 객체는 9.x에서 path를 다루는 정석이다. configuration time IO도 일으키지 않고, Configuration Cache와도 잘 어울린다.

여기까지 적었으면 task 하나는 완성이다. `./gradlew buildInfo`를 돌리면 `build/generated/build-info.txt`가 생긴다. 두 번째 돌리면? `gitSha`가 그대로고, `builtAt`은 매 빌드마다 새 값이 되므로 task는 다시 돈다. 만약 timestamp 없이 SHA만 떨군다면 두 번째 빌드는 UP-TO-DATE로 끝난다. 어노테이션이 정확히 박혀 있으니 가능한 일이다.

## 박스 — Project property vs system property vs ext 변수

여기까지 오면 자주 받는 질문이 있다. "버전 같은 값을 빌드 시점에 외부에서 주입하고 싶은데, 어디에 어떻게 적어야 하나?" Gradle에는 비슷해 보이는 세 가지 길이 있다. 헷갈리니까 한 번에 정리해두자.

> **박스 — `-P`, `-D`, `ext`의 정확한 차이**
>
> **(1) Project property (`-P`).** 명령행에서 `./gradlew build -Pversion=1.2.3`처럼 넘긴다. Kotlin DSL에서는 `providers.gradleProperty("version")`으로 받는다. `gradle.properties` 파일에 적어둔 키도 같은 API로 읽힌다. **빌드 자체에 주는 입력**이라고 생각하면 된다. 버전, 환경 이름, feature flag 같은 것들이 여기에 속한다.
>
> **(2) System property (`-D`).** `./gradlew test -Dspring.profiles.active=local`처럼 넘긴다. 이건 Gradle이 아니라 **JVM에 주는 입력**이다. 빌드 스크립트 안에서는 `providers.systemProperty("...")`로 읽고, 테스트 task로는 `systemProperty(...)` 메서드로 전달한다. Spring Boot 앱이 `@Value("${'$'}{...}")`로 읽는 것과 짝이 맞는다.
>
> **(3) `ext` (extra properties).** Groovy DSL 시절의 유산이다. `ext { val foo = "bar" }`로 정의하고 `extra["foo"]`로 읽는다. **빌드 스크립트 내부에서만 공유**되는 값이다. CLI에서 주입할 수 없다. 단순한 상수 공유 외에는 쓸 일이 거의 없고, 9.x에서는 차라리 Version Catalog나 build-logic의 convention plugin으로 빼는 편이 낫다.
>
> 정리하자면, **외부에서 빌드에 주는 입력은 `-P`**, **외부에서 앱/테스트의 JVM에 주는 입력은 `-D`**, **스크립트 안의 임시 공유 변수는 `ext`** 다. 셋을 섞어 쓰는 코드를 만나면 일단 정리할 거리부터 잡힌 거라고 생각해도 좋다.

이 박스를 기억해두면 task의 입력을 외부에서 주입하고 싶을 때 길을 헤매지 않는다. 예컨대 우리 `GenerateBuildInfoTask`에 "릴리스 빌드일 때만 git tag도 같이 떨궈라"는 입력을 더하고 싶다면 `providers.gradleProperty("release")`로 받으면 된다. `System.getenv("RELEASE")` 같은 직접 호출은 절대 쓰지 말자. 다음 절에서 보겠지만 그 한 줄이 모든 캐시를 무력화한다.

## 함정 박스 — `upToDateWhen { false }`라는 안티패턴

앞에서 잠깐 비판했던 한 줄이 너무 자주 등장하니 박스를 따로 두자.

> **함정 — `outputs.upToDateWhen { false }`는 답이 아니다**
>
> task가 매번 안 돌아서 문제라고 느낀다면, 십중팔구 입력/출력 어노테이션이 잘못됐거나 누락됐다는 신호다. 그런데 한국어 자료에서는 "매번 돌게 만들고 싶으면 `outputs.upToDateWhen { false }`를 넣으세요" 같은 답이 자주 보인다. 이건 진통제다. 원인을 가린다.
>
> 이 한 줄을 넣으면 일어나는 일:
> - 해당 task는 항상 실행된다. UP-TO-DATE 판정을 받지 못한다.
> - Build Cache로도 hit이 나지 않는다. 출력을 매번 새로 만들기 때문이다.
> - 그 task의 출력을 입력으로 받는 모든 하류 task가 함께 다시 돈다. 빌드 그래프 절반이 무효화된다.
>
> 정직한 답:
> - 입력으로 가질 값을 모두 `@Input` / `@InputFile` / `@InputDirectory` / `@Nested`로 적어둔다.
> - 출력은 `@OutputFile` / `@OutputDirectory`로 적어둔다.
> - "현재 시각" 같은 본질적으로 비결정적인 값을 입력으로 쓰고 싶다면, 그 값이 정말 입력에 들어가야 하는지 다시 생각해본다. 보통은 git SHA처럼 결정적인 값이면 충분하다.
>
> `upToDateWhen { false }`는 진짜로 쓸 일이 있다 — 외부 시스템의 상태에 의존하는 task(예: 원격 서버 헬스 체크) 같은 경우. 그런데 그런 task는 빌드 그래프의 상류에 두지 말자. 보통은 별도 task로 빼서 명시적으로 호출한다.

## task에서 plugin으로 — `shop.build-info`

지금까지 우리는 task 클래스 하나를 만들었다. 그런데 이걸 `app/build.gradle.kts` 안에 그대로 적어두면 다른 모듈이나 다른 프로젝트에서 재사용할 수 없다. 그리고 build.gradle.kts에 abstract class 정의가 들어가 있는 모습은 어쩐지 어수선하다. 책이라면 부록으로 빠질 만한 내용이 본문에 끼어 있는 느낌이다.

답은 11장에서 이미 깔아뒀다. `build-logic` included build. 거기에 우리의 plugin을 심자.

먼저 디렉터리 구조를 확인하자. 11장 끝에서 `build-logic`은 이런 모습이었다.

```
shop/
├── settings.gradle.kts
├── build.gradle.kts
├── app/
├── domain/
├── order/
├── payment/
└── build-logic/
    ├── settings.gradle.kts
    ├── build.gradle.kts
    └── src/main/kotlin/
        ├── shop.java-conventions.gradle.kts
        └── shop.spring-boot-conventions.gradle.kts
```

여기에 우리의 새 plugin을 더하자.

```
build-logic/
├── settings.gradle.kts
├── build.gradle.kts
└── src/main/kotlin/
    ├── shop/
    │   └── buildinfo/
    │       ├── GenerateBuildInfoTask.kt
    │       ├── ShopBuildInfoExtension.kt
    │       └── ShopBuildInfoPlugin.kt
    ├── shop.java-conventions.gradle.kts
    └── shop.spring-boot-conventions.gradle.kts
```

세 파일을 차례로 본다. 먼저 task 클래스. 앞에서 만든 그대로다.

```kotlin
// build-logic/src/main/kotlin/shop/buildinfo/GenerateBuildInfoTask.kt
package shop.buildinfo

import org.gradle.api.DefaultTask
import org.gradle.api.file.RegularFileProperty
import org.gradle.api.provider.Property
import org.gradle.api.tasks.Input
import org.gradle.api.tasks.OutputFile
import org.gradle.api.tasks.TaskAction
import org.gradle.api.tasks.CacheableTask

@CacheableTask
abstract class GenerateBuildInfoTask : DefaultTask() {

    @get:Input
    abstract val gitSha: Property<String>

    @get:Input
    abstract val builtAt: Property<String>

    @get:Input
    abstract val applicationName: Property<String>

    @get:OutputFile
    abstract val outputFile: RegularFileProperty

    @TaskAction
    fun run() {
        val target = outputFile.get().asFile
        target.parentFile.mkdirs()
        target.writeText(
            """
            application=${applicationName.get()}
            git=${gitSha.get()}
            built=${builtAt.get()}
            """.trimIndent()
        )
    }
}
```

한 가지가 더해졌다. `@CacheableTask`. 이 어노테이션은 "이 task의 결과는 Build Cache로 캐시할 수 있다"는 선언이다. 13장에서 Build Cache를 켤 예정이라 미리 박아두자. 입력 어노테이션이 정확해야만 캐시가 의미가 있다는 걸 잊지 말자.

다음으로 extension. plugin이 사용자에게 노출할 설정의 모양이다.

```kotlin
// build-logic/src/main/kotlin/shop/buildinfo/ShopBuildInfoExtension.kt
package shop.buildinfo

import org.gradle.api.provider.Property

abstract class ShopBuildInfoExtension {
    abstract val applicationName: Property<String>
}
```

`abstract val applicationName: Property<String>`. 사용자 build.gradle.kts에서 `shopBuildInfo { applicationName = "shop-app" }`처럼 쓰게 될 자리다. extension 안에서도 `Property<T>`를 쓰는 이유는 같다. 값의 결정 시점을 미루기 위해서. 사용자가 `applicationName`을 다른 Provider에서 얻어와 대입할 수도 있다.

마지막으로 plugin 본체.

```kotlin
// build-logic/src/main/kotlin/shop/buildinfo/ShopBuildInfoPlugin.kt
package shop.buildinfo

import org.gradle.api.Plugin
import org.gradle.api.Project
import org.gradle.kotlin.dsl.create
import org.gradle.kotlin.dsl.register

class ShopBuildInfoPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        val ext = project.extensions.create<ShopBuildInfoExtension>("shopBuildInfo")

        // extension 기본값 — 프로젝트 이름
        ext.applicationName.convention(project.name)

        val buildInfoTask = project.tasks.register<GenerateBuildInfoTask>("buildInfo") {
            applicationName = ext.applicationName

            gitSha = project.providers.exec {
                commandLine("git", "rev-parse", "HEAD")
            }.standardOutput.asText.map { it.trim() }

            builtAt = project.providers.provider {
                java.time.Instant.now().toString()
            }

            outputFile = project.layout.buildDirectory
                .file("generated/build-info/build-info.properties")
        }

        // processResources가 buildInfo의 출력을 자동으로 가져가도록 연결
        project.tasks.matching { it.name == "processResources" }.configureEach {
            dependsOn(buildInfoTask)
            inputs.file(buildInfoTask.flatMap { it.outputFile })
        }

        project.afterEvaluate {
            project.tasks.matching { it.name == "processResources" }
                .configureEach {
                    (this as org.gradle.language.jvm.tasks.ProcessResources)
                        .from(buildInfoTask.flatMap { it.outputFile })
                }
        }
    }
}
```

여기에 처음 보는 패턴이 몇 가지 들어있다. 차분히 풀어보자.

**`ext.applicationName.convention(project.name)`.** `convention(...)`은 "사용자가 명시적으로 값을 안 정하면 이 값을 기본으로 쓴다"는 약속이다. `set`이나 `=`는 명시적으로 값을 정하는 것이고, `convention`은 기본값을 거는 것이다. 9.x의 lazy Property API에서 매우 자주 쓰는 패턴이다.

**Property 끼리의 wire-up.** `applicationName = ext.applicationName`이라는 한 줄을 보자. extension의 Property를 task의 Property에 그대로 대입한다. 이게 lazy API의 진짜 힘이다. 사용자가 build.gradle.kts에서 `shopBuildInfo { applicationName = "..." }`을 적는 순간 그 값은 자동으로 task에까지 흘러간다. 우리가 중간에 값을 "복사"한 게 아니다. **두 Property가 같은 약속을 들고 있다.** 사용자가 값을 늦게 정해도, 사용자가 값을 다른 Provider에서 받아도, 약속만 따라가면 된다. 이것 때문에 `afterEvaluate` 같은 hack을 거의 쓰지 않아도 된다.

**`buildInfoTask.flatMap { it.outputFile }`.** `register<T>(...)`가 돌려주는 건 `TaskProvider<T>` — 역시 lazy 한 박스다. `flatMap`은 그 박스 안의 task에서 다시 `Property`를 꺼내 lazy하게 이어붙인다. "buildInfo task의 출력 파일을 processResources의 입력 파일로 추가"라는 의미가 한 줄로 표현된다. 두 task는 같은 Provider 체인을 공유하니까 dependency가 자동으로 추론된다. `dependsOn`을 따로 적지 않아도 되는 경우가 많지만, 명시적으로 적어두면 의도가 분명해진다.

**`afterEvaluate` 안에서 `from(...)` 추가.** `processResources` task는 `java` plugin이 적용된 다음에 만들어진다. 우리 plugin이 적용되는 시점에 아직 그 task가 없을 수 있어서 `matching { ... }.configureEach { ... }`로 안전하게 잡는다. 그리고 `from(buildInfoTask.flatMap { ... })`로 생성된 파일을 resources 디렉터리로 복사하라고 적어둔다. 이렇게 하면 빌드된 jar 안에 `build-info.properties`가 자연스럽게 포함된다.

이제 plugin id를 등록할 차례다. `build-logic/build.gradle.kts`를 열자.

```kotlin
// build-logic/build.gradle.kts
plugins {
    `kotlin-dsl`
    `java-gradle-plugin`
}

gradlePlugin {
    plugins {
        register("shop-build-info") {
            id = "shop.build-info"
            implementationClass = "shop.buildinfo.ShopBuildInfoPlugin"
        }
    }
}
```

`java-gradle-plugin` 플러그인이 새로 들어왔다. 이게 우리 binary plugin을 plugin id로 등록할 수 있게 해주는 표준 도구다. `gradlePlugin { plugins { register(...) } }` 블록에 plugin id와 구현 클래스를 매핑한다. 이렇게 등록하면 다른 모듈에서 `id("shop.build-info")` 한 줄로 우리 plugin을 받을 수 있다.

> **박스 — Plugin Portal 발행은 본 책의 범위 밖**
>
> `java-gradle-plugin` + `gradlePlugin { ... }` 등록은 **사내 발행이든 외부 발행이든 공통의 출발선**이다. 여기까지는 누구나 한다. 그 다음 단계 — Gradle Plugin Portal 발행, 사내 Nexus/Artifactory로 publish, signing, 메타데이터 작성 — 는 별도의 큰 주제다. 본 책에서는 다루지 않는다.
>
> 짧게만 가이드를 남기면, 외부 발행은 `com.gradle.plugin-publish` plugin과 portal API key가, 사내 발행은 `maven-publish` plugin과 사내 저장소의 URL/credential이 필요하다. Configuration Cache 시대의 추세는 — 사내 표준이라면 **included build로 쓰는 편이 발행해서 의존하는 것보다 빠르고 디버그하기 쉽다**는 것이다. 우리가 11장에서 `build-logic`을 included build로 둔 게 그 이유다.

## app에서 plugin을 쓴다

이제 app 쪽으로 가서 받아 쓰자. settings.gradle.kts에는 11장에서 이미 `pluginManagement { includeBuild("build-logic") }`을 적어뒀다. 그러니 plugin id만 알면 된다.

```kotlin
// app/build.gradle.kts
plugins {
    id("shop.spring-boot-conventions")
    id("shop.build-info")
}

shopBuildInfo {
    applicationName = "shop-app"
}

dependencies {
    implementation(project(":domain"))
    implementation("org.springframework.boot:spring-boot-starter-actuator")
}
```

`plugins { id("shop.build-info") }` 한 줄로 plugin이 들어왔다. extension 블록 `shopBuildInfo { ... }`로 설정을 준다. 이게 다다.

`./gradlew :app:bootJar`를 돌려보자.

```bash
$ ./gradlew :app:bootJar
> Task :build-logic:compileKotlin
> Task :build-logic:jar
> Task :app:buildInfo
> Task :app:processResources
> Task :app:bootJar

BUILD SUCCESSFUL in 6s
```

`build/libs/app.jar`를 열어보면 안에 `BOOT-INF/classes/build-info.properties`가 들어 있고, 우리가 적은 형식대로 git SHA, 빌드 시각, 애플리케이션 이름이 적혀 있다.

이제 Spring Boot 쪽에서 이걸 읽자. `@Value`로 properties 파일에서 값을 끌어다 actuator info에 노출하면 된다.

```kotlin
// app/src/main/kotlin/shop/app/config/BuildInfoConfig.kt
package shop.app.config

import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.actuate.info.Info
import org.springframework.boot.actuate.info.InfoContributor
import org.springframework.context.annotation.Configuration
import org.springframework.context.annotation.PropertySource

@Configuration
@PropertySource("classpath:build-info.properties")
class BuildInfoConfig(
    @Value("\${application}") private val application: String,
    @Value("\${git}") private val git: String,
    @Value("\${built}") private val built: String,
) : InfoContributor {

    override fun contribute(builder: Info.Builder) {
        builder.withDetail(
            "build",
            mapOf("application" to application, "git" to git, "built" to built),
        )
    }
}
```

application.yml에 `management.endpoints.web.exposure.include: info`를 더해놓고 `./gradlew :app:bootRun` 후 `curl localhost:8080/actuator/info`를 때려보자.

```json
{
  "build": {
    "application": "shop-app",
    "git": "a1b2c3d...",
    "built": "2026-05-11T03:14:15.926Z"
  }
}
```

처음 시작한 질문에 답이 나왔다. 누가 묻든, URL 한 번으로 "지금 배포된 게 어느 커밋인지" 답할 수 있다. 그것도 Configuration Cache가 켜져도 깨지지 않는 방식으로.

## 마이그레이션 노트 — Gradle 7 이전을 기억한다면

오래 Gradle을 써온 사람이라면 옛 코드와 새 코드의 거리감이 더 크게 느껴진다. 짧게 비교해두자.

**`tasks.create(...)` vs `tasks.register(...)`.** 7.x 이전 코드에서는 `tasks.create("buildInfo")`가 정석이었다. 그런데 `create`는 **즉시 task 객체를 만든다.** configuration phase에서 모든 task가 생성된다. 작은 빌드라면 상관없지만, 모듈 수십 개짜리 빌드에서는 빌드 시작이 무거워진다. `register`는 lazy하다. "이런 task가 있다"는 약속만 들고 있다가, 실제로 그 task가 그래프에 들어갈 때만 실체화한다. 9.x에서는 무조건 `register`다.

**`<<` 연산자.** 5.x 이전에는 `task buildInfo << { ... }` 같은 코드가 흔했다. 이건 `doLast { ... }`의 줄임이었다. `<<` 연산자 자체가 7.x에서 제거된 지 오래다. 보면 일단 옛 코드라고 생각하자.

**`Project.exec { ... }`.** 6.x까지 정석이었던 외부 명령 호출 방법이다. 9.x에서는 `providers.exec`가 답이다. 옛 책에서 `project.exec` 코드를 봤다면 Provider 기반으로 다시 적는 편이 낫다. Configuration Cache 호환성이 다르다.

**`getByName("...")`.** task에 접근할 때 `tasks.getByName("test")`로 즉시 실체화하던 패턴이다. 3장에서 본 것처럼 9.x에서는 `tasks.named<Test>("test") { ... }`가 권장이다. 같은 lazy 정신이다.

이 네 가지 차이를 머릿속에 두면, 옛 자료를 볼 때 "어, 이건 옛날 방식이구나"를 한 번에 알아본다. 그러면 그 자료에서 무엇만 흡수하고 무엇은 버려야 할지가 분명해진다.

## 12장을 닫으며

처음 질문은 단순했다. git SHA를 파일로 떨궈서 actuator/info에 노출하고 싶다. 답을 찾는 길은 짧지 않았다. doLast 한 줄로 끝낼 수 있는 일이 왜 abstract class와 `Property<T>`와 `providers.exec`까지 끌고 와야 했는지, 한 줄씩 풀어왔다.

핵심을 다시 정리하자.

**Lazy Property API.** `Property<T>`와 `Provider<T>`는 "값을 지금 결정하지 않아도 된다"는 약속이다. 그 약속 덕분에 task의 입력과 출력은 늦게 평가될 수 있고, configuration phase의 부담이 줄어들고, Configuration Cache에 친화적이 된다. 3장에서 미뤘던 약속을 여기서 정면으로 마주봤다.

**입력/출력 어노테이션.** `@Input`, `@OutputFile`, `@CacheableTask` 같은 어노테이션은 단순히 문서가 아니다. Gradle이 task를 incremental하게 돌리고, Build Cache에 넣고, Configuration Cache로 격리할 수 있는 **계약**이다. 어노테이션이 정확할수록 빌드는 빨라진다.

**Plugin과 Extension의 분리.** task 하나가 자라면 자연스럽게 plugin이 된다. Extension은 사용자에게 노출하는 설정의 모양, Plugin은 그 설정을 받아 task에 wire-up하는 코드. 이 분리가 깔끔하면 plugin은 재사용 가능한 도구가 된다. `shop.build-info`를 우리가 어느 모듈에든, 다른 프로젝트에든 `id("shop.build-info")` 한 줄로 받아 쓸 수 있는 이유다.

**11장의 build-logic이 살아남.** 11장에서 included build로 분리해둔 `build-logic`은 이번 장에서 비로소 자기 역할을 받았다. convention plugin과 binary plugin이 한 자리에 모이는 곳. 빌드의 도구 상자다. 앞으로 새로 만들 plugin들도 거의 다 여기로 들어간다.

다음 장에서 우리는 마지막 큰 스위치를 켠다. **Configuration Cache.** 9.x가 "preferred mode of execution"이라고 못박은 모드다. 우리 코드는 이미 그 세계에 들어갈 준비가 됐다 — task가 `Property` 기반이고, 외부 명령은 `providers.exec`고, 파일 경로는 `layout.buildDirectory`니까. 그래도 막상 `--configuration-cache`를 붙이면 전에 안 보이던 위반들이 튀어나올 수 있다. 그걸 어떻게 진단하고, 어떻게 점진적으로 켜 나가는지가 13장의 일이다. Part IV의 두 번째 장이 기다린다.
