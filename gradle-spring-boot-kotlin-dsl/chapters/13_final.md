# 13장. Configuration Cache를 켠다 — 위반을 진단하고 호환되게 고친다

12장에서 우리는 `shop.build-info`라는 작은 플러그인을 만들었다. git SHA와 빌드 시각을 파일 한 줄로 떨궈주는, 자그마한 도구다. 그걸 만들면서 한 가지를 계속 의식했다. **즉시 평가를 피하라.** `System.getenv`를 직접 부르지 말고 `providers.environmentVariable`을 쓰자. `Project.exec` 대신 `providers.exec`를 쓰자. 그렇게 신경 써서 짠 이유가 이번 장에서 드러난다.

`gradle.properties`에 한 줄을 더 적어보자.

```properties
org.gradle.configuration-cache=true
```

그리고 빌드를 돌려본다. 운이 좋다면 두 번째 실행부터 다음 한 줄이 보일 것이다.

```
Reusing configuration cache.
```

이 한 줄을 만나는 순간, 빌드는 configuration phase를 통째로 건너뛴다. 2장에서 본 Settings → Project → Task 그래프 만드는 그 단계 전부를 말이다. 멀티 모듈에서 `./gradlew :app:bootRun`을 칠 때마다 3~5초씩 까먹던 시간이 사라진다.

그런데 운이 나쁘면 이런 메시지가 줄줄이 쏟아진다.

```
6 problems were found storing the configuration cache.
- Plugin 'com.acme.legacy-reporter': read system property 'user.home' at configuration time
- Task `:app:reportStuff` of type `com.acme.LegacyTask`: invocation of 'Task.project' at execution time
- ...
```

이 시점에서 가장 흔한 반응은 두 가지다. 하나는 "그냥 끄자, 우리 환경엔 안 맞는다." 다른 하나는 "전부 다 고쳐야 하나?" 둘 다 잘못된 반응이다. **점진적으로 도입하는 길이 따로 있다.** 그 길을 13장에서 함께 걸어보자. 이번 장의 코드는 `ch13-config-cache/`에 있고, 마지막에는 모든 빌드가 Configuration Cache + Build Cache 히트로 빠르게 도는 상태가 된다.

## 무엇이 캐시되는가 — Configuration Cache와 Build Cache는 직교한다

먼저 이 두 캐시의 자리를 정확히 갈라두자. 이름이 비슷해서 자주 헷갈리기 때문이다.

2장에서 Gradle 빌드가 세 단계로 흐른다고 말했다. Initialization — 어떤 프로젝트들이 빌드에 참여하는지 정한다. Configuration — 각 프로젝트의 build.gradle.kts를 평가해 Task 그래프를 만든다. Execution — 실제로 task를 돈다.

**Configuration Cache는 두 번째 단계의 결과를, Build Cache는 세 번째 단계의 결과를 저장한다.** 둘은 서로 다른 단계에 작용하므로 직교다. 한쪽만 켜도 되고 둘 다 켜도 된다. 둘 다 켜는 게 권장이다.

| | 무엇을 캐시하나 | 무엇이 빨라지나 |
|---|---|---|
| Configuration Cache | configuration phase의 산출물 — task 그래프, task 입력값, dependency resolution 결과 | 같은 task 호출 시 build.gradle.kts 평가 자체를 건너뛴다 |
| Build Cache | task execution의 산출물 — 컴파일된 클래스 파일, jar, 테스트 리포트 등 | 같은 입력의 task가 이미 돌았다면 그 결과를 그대로 가져다 쓴다 |

그래서 `./gradlew :app:bootRun`을 두 번 연속 칠 때, 첫 번째 가속(configuration phase 스킵)은 Configuration Cache의 몫이고, 두 번째 가속(`:domain:compileJava`가 안 돌고 결과를 가져옴)은 Build Cache의 몫이다. 두 개를 같이 켜면 한 번 돌린 빌드의 결과가 첫 라인부터 끝 라인까지 거의 다 캐시에서 나온다. 풀 빌드 30초짜리가 2~3초 안에 끝나는 광경을 볼 수 있다.

Configuration Cache는 Gradle 9.0부터 **"preferred mode of execution"으로 격상**됐다. 기본값으로 켜져 있지는 않지만, 공식 블로그가 "곧 default-on이 될 후보"라고 말하는 단계다. 옵션이 아니라 표준에 가깝다고 받아들이는 편이 낫다. (참고: [blog.gradle.org/road-to-configuration-cache](https://blog.gradle.org/road-to-configuration-cache))

## 켜는 법 — `problems=warn`으로 시작한다

켜는 줄 자체는 짧다. `gradle.properties`에 다음 세 줄을 적는다.

```properties
# gradle.properties — ch13-config-cache/
org.gradle.configuration-cache=true
org.gradle.configuration-cache.problems=warn
org.gradle.configuration-cache.parallel=true
```

여기서 두 번째 줄 `problems=warn`이 점진 도입 전략의 핵심이다. 이 키의 값은 `fail` 또는 `warn` 두 가지인데, 의미는 이렇다.

- `fail` (기본값): 위반이 하나라도 있으면 빌드 실패. 깔끔하지만 third-party plugin 하나가 비호환이면 그 자리에서 막힌다.
- `warn`: 위반은 보고만 하고 빌드는 계속 진행한다. **단, 캐시는 저장되지 않는다.** 다음 빌드에서 configuration phase는 다시 처음부터 돈다.

그래서 처음에 `warn`으로 켜는 의미는 이렇다. "지금 우리 빌드에 정확히 어떤 위반이 몇 개 있는지 일단 보자. 빌드는 멈추지 말고." 그렇게 위반 목록을 손에 쥔 다음, 하나씩 잡아간다. 위반이 0이 되는 날 `fail`로 바꾸면 그때부터 진짜 캐시가 동작한다.

세 번째 줄 `parallel=true`는 9.x에서 안정화된 옵션이다. configuration phase 안에서 프로젝트들의 평가를 병렬로 돌린다. Configuration Cache가 켜져 있어야 의미가 있는 옵션이라 이 자리에 같이 둔다.

이렇게 켜고 한 번 빌드를 돌리면 마지막에 이런 라인을 만나게 된다.

```
Configuration cache entry stored with 3 problems.
See the complete report at file:///.../build/reports/configuration-cache/...
```

링크된 HTML 리포트를 열어보면 위반마다 **어느 플러그인의 어느 줄에서, 어떤 종류의 위반인지** 명시돼 있다. 이게 9.0부터 강화된 부분이다. 이전 버전에서 종종 silent fail로 묻히던 위반들이 이제는 명시적으로 보고된다. 빌드를 디버깅할 때 첫 번째로 열어볼 파일이 바로 이 HTML 리포트다.

> **박스 — `--scan`으로 위반 진단하기**
>
> 5장에서 BOM과 catalog의 충돌을 추적할 때 Build Scan을 한 번 만났다. `./gradlew build --scan`을 붙이면 끝나고 URL이 하나 떨어진다고 말했다. Configuration Cache 위반 진단에도 같은 도구가 그대로 쓰인다.
>
> Scan을 열면 좌측 메뉴에 **Configuration cache**라는 탭이 있다. 클릭하면 이번 빌드에서 cache hit이었는지, store였는지, 위반은 몇 개였는지, 각 위반이 어느 plugin에서 발생했는지가 표 형태로 정리돼 있다. 로컬 HTML 리포트보다 한 단계 더 정돈된 뷰다. CI에서 위반이 발생했을 때 동료에게 "이 scan 링크 좀 봐달라"고 던지기에도 좋다.
>
> 같은 화면의 Timeline 탭에서는 configuration phase가 정확히 몇 ms 걸렸는지, 어느 프로젝트의 어떤 평가가 오래 걸렸는지도 보인다. 캐시가 켜진 빌드와 안 켜진 빌드 두 개의 scan을 나란히 띄워두면, 우리가 무엇을 절약했는지 숫자로 확인할 수 있다.

## 9.0의 명시적 위반 보고 — 무엇이 금지인가

Configuration Cache가 캐시할 수 있으려면, configuration phase가 만들어내는 모든 것이 **직렬화 가능하고, 실행 시점의 외부 상태에 의존하지 않아야** 한다. 그런데 Gradle을 오래 쓴 사람의 손에는 이 원칙을 깨는 코드가 자연스럽게 배어 있다. 8장에서 이미 한 번 본 패턴인 `subprojects {}`도 그중 하나고, 12장에서 우리가 의식적으로 피했던 `System.getenv`도 그중 하나다.

9.0부터 위반은 silent fail이 아니다. 어떤 종류의 위반이 어디서 발생했는지 명시적으로 보고된다. 흔히 만나는 위반과 그 대체 API를 한 표로 정리해두자. 이 표는 인쇄해서 IDE 옆에 붙여둘 가치가 있다.

| 금지 패턴 | 왜 위반인가 | 대체 API |
|---|---|---|
| `task.project.something` — 실행 시점에 Project 접근 | configuration cache는 execution 시점에 Project를 직렬화하지 않는다 | configuration 시점에 값을 잡아 `Property<T>` / `Provider<T>`로 task에 wire-up |
| `System.getenv("X")` / `System.getProperty("X")` 직접 호출 | 외부 상태를 캐시가 추적할 수 없다 | `providers.environmentVariable("X")` / `providers.systemProperty("X")` |
| `File("config.json")` — configuration 시점의 즉시 IO | 파일이 빌드 입력인지 캐시가 모른다 | `layout.projectDirectory.file("config.json")` |
| `project.exec { ... }` — 즉시 실행 | exec 결과가 캐시되지 않는다 | `providers.exec { commandLine(...) }.standardOutput.asText` |
| `gradle.taskGraph.whenReady { ... }`에서 mutable state 변형 | 콜백 안의 상태 변경이 캐시 일관성을 깨뜨린다 | task에 lazy property를 정의하고 그 안에서 처리 |

이 표를 한 번에 외울 필요는 없다. 한 가지 패턴만 기억하면 된다. **"즉시 평가하지 말고, Provider로 지연시켜라."** Gradle 9의 모든 신규 API가 이 원칙으로 설계됐다. 12장에서 우리가 `providers.exec { commandLine("git", "rev-parse", "HEAD") }`를 썼던 것도, `layout.buildDirectory.file(...)`를 썼던 것도 전부 이 원칙의 적용이었다.

### 12장의 `shop.build-info`를 호환되게 손본다

이걸 구체적으로 느끼기 위해, 12장에서 만든 `shop.build-info`의 두 가지 버전을 나란히 놓고 보자. 한쪽은 의식하지 않고 짠 "옛날 스타일" 코드고, 다른 한쪽은 12장에서 우리가 실제로 짠 코드다.

**비호환 버전 — `org.gradle.configuration-cache=true`에서 위반 보고를 받는다:**

```kotlin
// build-logic/src/main/kotlin/shop/BuildInfoPlugin.kt — 옛 스타일
abstract class GenerateBuildInfoTask : DefaultTask() {

    @get:OutputFile
    abstract val outputFile: RegularFileProperty

    @TaskAction
    fun run() {
        // 위반 1: execution 시점에 Project.exec
        val sha = project.exec {
            commandLine("git", "rev-parse", "HEAD")
            standardOutput = System.out
        }

        // 위반 2: System.getenv 직접 호출
        val ciBuildNumber = System.getenv("BUILD_NUMBER") ?: "local"

        // 위반 3: File("...") 즉시 IO
        val template = File("src/main/resources/buildinfo.template").readText()

        outputFile.get().asFile.writeText("$template\ngit=$sha\nbuild=$ciBuildNumber\n")
    }
}
```

이걸 그대로 두고 `./gradlew :app:generateBuildInfo`를 돌리면, 9.0에서는 위반 세 개가 또렷이 보고된다. silent fail로 묻히지 않는다. 리포트가 친절히 "여기 `Project.exec`가 execution time에 호출됐다"고 줄과 함께 알려준다.

**호환 버전 — 12장에서 실제로 짠 코드:**

```kotlin
// build-logic/src/main/kotlin/shop/BuildInfoPlugin.kt — 9.x 표준
abstract class GenerateBuildInfoTask : DefaultTask() {

    @get:Input
    abstract val gitSha: Property<String>

    @get:Input
    abstract val ciBuildNumber: Property<String>

    @get:InputFile
    abstract val template: RegularFileProperty

    @get:OutputFile
    abstract val outputFile: RegularFileProperty

    @TaskAction
    fun run() {
        val body = template.get().asFile.readText()
        outputFile.get().asFile.writeText(
            "$body\ngit=${gitSha.get()}\nbuild=${ciBuildNumber.get()}\n"
        )
    }
}

class ShopBuildInfoPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        project.tasks.register<GenerateBuildInfoTask>("generateBuildInfo") {
            gitSha = project.providers.exec {
                commandLine("git", "rev-parse", "HEAD")
            }.standardOutput.asText.map { it.trim() }

            ciBuildNumber = project.providers.environmentVariable("BUILD_NUMBER")
                .orElse("local")

            template = project.layout.projectDirectory
                .file("src/main/resources/buildinfo.template")

            outputFile = project.layout.buildDirectory
                .file("generated/build-info.txt")
        }
    }
}
```

차이를 짚어보자. 비호환 버전에서는 `@TaskAction` 안에서 외부 명령을 실행하고, 환경 변수를 읽고, 파일을 직접 열었다. 호환 버전에서는 그 모든 외부 접근이 **task의 입력(`@Input`, `@InputFile`)으로 선언**되고, 값은 **Provider로 wire-up**돼서 평가는 필요한 시점까지 미뤄진다. configuration cache는 이 입력 선언만 알면 캐시 키를 정확히 만들 수 있다.

부가 효과가 하나 더 있다. 12장 끝에서 다뤘던 함정 — `outputs.upToDateWhen { false }`로 매번 실행되게 만드는 안티패턴 — 이 이렇게 `@Input` / `@InputFile`을 정확히 단 코드에서는 **자동으로 해결**된다. git SHA가 바뀌면 입력이 바뀐 거니까 task가 다시 돈다. 안 바뀌면 안 돈다. up-to-date 판단을 Gradle에게 맡기면 된다. 손으로 `upToDateWhen`을 비활성화하지 말자.

12장의 코드를 위반 버전으로 짰다면 13장의 첫 빌드에서 위반 세 개를 보고 당황했을 것이다. 우리가 12장에서 처음부터 호환 패턴으로 짰던 이유가 이 자리에서 회수된다.

## `parallel=true`까지 켠다 — 9.x의 안정성

Configuration Cache를 켜고 위반을 다 잡았다면, 그다음에 켤 만한 게 `org.gradle.parallel=true`다. 이미 위에서 `gradle.properties`에 적었다.

```properties
org.gradle.parallel=true
org.gradle.workers.max=8
```

`parallel=true`는 프로젝트 간 비의존 task를 병렬로 돌린다. 8장에서 우리는 `:domain`, `:order`, `:payment`, `:app`을 분리했다. 이 중 `:order`와 `:payment`는 `:domain`에만 의존하고 서로 의존하지 않는다. 그러면 `:domain`이 끝난 뒤 `:order:compileJava`와 `:payment:compileJava`가 **동시에** 도는 게 가능하다. 단일 모듈에선 의미 없지만 멀티 모듈에선 CPU 코어 수만큼 가속이 붙는다.

`workers.max`는 동시에 돌릴 worker 수의 상한이다. 기본값은 머신 CPU 코어 수다. 명시적으로 적어두면 노트북에서는 8로, CI에서는 4로 같은 빌드를 다르게 돌릴 수도 있다.

여기서 한 가지 주의. `parallel=true`는 빌드 스크립트가 **thread-safe**해야 의미가 있다. `subprojects {}`를 남발한 빌드에서는 한 스레드의 평가가 다른 스레드의 평가에 영향을 주는 race가 생길 수 있다. 그래서 10장에서 `subprojects {}` 대신 convention plugin을 쓰자고 했던 이유 중 하나가 여기서도 회수된다. 명시적인 plugin 적용은 병렬 친화적이다.

## Build Cache를 켠다 — local과 remote

Configuration Cache가 안정됐으면 그 옆자리에 Build Cache를 놓는다. 줄 하나면 끝이다.

```properties
org.gradle.caching=true
```

이 한 줄로 `~/.gradle/caches/build-cache-1/` 아래에 로컬 Build Cache가 활성화된다. 그다음부터 `:domain:compileJava`가 같은 입력으로 한 번 돌면, 두 번째부터는 컴파일된 클래스 파일 묶음을 캐시에서 그대로 가져다 쓴다. 입력이 정확히 같으면 task가 아예 안 도는 게 incremental build고, 이전에 같은 입력이 적어도 한 번이라도 돌았으면 그 결과를 가져오는 게 build cache다. 시점이 다르다.

> **박스 — Remote cache와 Develocity**
>
> 로컬 Build Cache는 한 머신 안에서만 공유된다. 팀원 다섯이 같은 코드를 빌드하면 다섯 번 컴파일된다. 비용이 아깝다.
>
> Remote build cache는 HTTP 기반의 캐시 서버를 두고 여러 머신이 공유하는 방식이다. settings.gradle.kts에 적는다.
>
> ```kotlin
> buildCache {
>     local { isEnabled = true }
>     remote<HttpBuildCache> {
>         url = uri("https://cache.example.com/")
>         isPush = System.getenv("CI") == "true"   // CI에서만 push
>     }
> }
> ```
>
> 직접 운영하는 방식도 가능하지만, 이 영역의 사실상 표준은 **Develocity** (구 Gradle Enterprise)다. 운영형 솔루션으로, Build Scan을 enterprise 단위로 모으고 remote cache를 호스팅한다. 깊이는 이 책의 범위 밖이지만, 팀이 5명을 넘기 시작했다면 한 번 검토해볼 만한 선택지로 기억해두자.

Build Cache가 의미 있게 동작하려면 task의 입출력 어노테이션이 정확해야 한다. 그래서 12장에서 `@Input`, `@InputFile`, `@OutputFile`을 꼼꼼히 다는 연습을 했던 거다.

### `@CacheableTask`와 입출력 어노테이션의 관계

여기서 짚고 넘어갈 게 하나 있다. `@CacheableTask`라는 어노테이션이다. 12장에선 잠깐 나왔다가 묻혔는데, Build Cache가 켜진 지금 다시 본다.

```kotlin
@CacheableTask
abstract class GenerateBuildInfoTask : DefaultTask() { ... }
```

`@CacheableTask`는 "이 task는 Build Cache에 저장하고 거기서 꺼내 써도 안전하다"는 명시적 동의 표시다. **이 어노테이션이 없으면 사용자가 만든 task는 캐시되지 않는다.** Gradle 표준 task(`JavaCompile`, `Test` 등)는 이미 이 어노테이션이 붙어 있어서 자동으로 캐시된다. 하지만 우리가 만드는 task는 별도다.

그렇다면 왜 자동이 아니냐. 답은 단순하다. **모든 task가 캐시 가능한 게 아니기 때문이다.** 예를 들어 task의 출력이 환경 의존적이라면(같은 입력인데 머신마다 결과가 다르다면) 캐시하면 안 된다. 머신 A의 결과를 머신 B로 옮기면 틀린 결과가 나오니까. `@CacheableTask`를 다는 행위는 "내가 이 task의 입출력을 정확히 선언했고, 같은 입력이면 같은 출력이 보장된다"는 책임을 지는 행위다.

12장의 `GenerateBuildInfoTask`라면 어떤가? 입력은 git SHA(문자열), CI 빌드 번호(문자열), 템플릿 파일이다. 출력은 텍스트 파일이다. 같은 입력이면 같은 출력이 나온다. 캐시 가능하다. `@CacheableTask`를 붙이는 게 옳다. 12장의 `ch12-custom-plugin/` 폴더 코드를 13장에서는 이 어노테이션을 추가한 형태로 업데이트해두자.

## Incremental Build의 동작 원리 — 입출력 해시 비교

여기까지 오면 한 가지 의문이 든다. Gradle은 task를 다시 돌릴지 말지 어떻게 판단하나? 답은 의외로 단순하다. **모든 입력의 해시를 계산하고, 모든 출력의 해시를 계산해서, 이전 실행과 비교한다.** 같으면 up-to-date. 하나라도 다르면 다시 돈다.

그래서 task의 `@Input`, `@InputFile`, `@InputDirectory` 어노테이션이 **결정적으로 중요**해진다. 입력으로 선언되지 않은 값은 해시에 들어가지 않는다. 해시에 안 들어간 값이 바뀌어도 Gradle은 모른다. 그러면 캐시에서 잘못된 결과를 가져온다.

비호환 버전의 `GenerateBuildInfoTask`로 돌아가보자. 거기서 `System.getenv("BUILD_NUMBER")`를 `@TaskAction` 안에서 직접 읽었다. 이건 입력으로 선언되지 않았다. 그래서 어제 빌드와 오늘 빌드에서 `BUILD_NUMBER`만 다르면, Gradle은 입력이 같다고 판단하고 어제 결과를 그대로 가져온다. **결과는 틀린다.** 이런 종류의 사고가 가장 디버깅하기 어렵다. 빌드는 성공하는데 결과만 잘못 박힌다.

호환 버전에서는 `ciBuildNumber`를 `@Input`으로 선언했다. 그래서 `BUILD_NUMBER` 환경 변수가 바뀌면 입력 해시가 바뀌고, task가 정확히 다시 돈다. **어노테이션의 정확성이 곧 캐시의 정확성이다.** 이 한 줄을 잊지 말자.

## 점진 도입 — 위반을 하나씩 잡는다

이제 본 챕터의 핵심 질문으로 돌아오자. **Configuration Cache를 켰는데 third-party plugin이 비명을 지른다. 어떻게 점진적으로 도입하는가?**

여기서 마음을 차분히 가지자. 9.0 시점 기준, 인기 50개 플러그인 중 절반 이상이 이미 Configuration Cache 호환이다. Spring Boot Gradle Plugin도 호환이다. JaCoCo, SonarQube, Detekt 같은 자주 쓰는 도구들도 대부분 따라왔다. 비호환인 건 보통 enterprise 환경에서 만든 자체 플러그인이거나, 오랫동안 업데이트가 멈춘 플러그인이다.

도입 순서는 이렇게 잡는 편이 낫다.

**1단계 — `warn`으로 켜고 위반 목록을 본다.** `org.gradle.configuration-cache=true`, `org.gradle.configuration-cache.problems=warn`. 빌드는 멈추지 않고 위반은 HTML 리포트와 Build Scan에 다 기록된다. 우리 빌드에 정확히 어떤 위반이 몇 개 있는지 일단 손에 쥔다.

**2단계 — 위반을 두 분류로 나눈다.** (a) 자체 빌드 스크립트 / convention plugin에서 발생한 위반. (b) third-party plugin 내부에서 발생한 위반.

**3단계 — (a)를 먼저 잡는다.** 우리 손이 닿는 곳이니까. 이번 장의 표를 보면서 `System.getenv` → `providers.environmentVariable`, `Project.exec` → `providers.exec`, `File("...")` → `layout.projectDirectory.file(...)`로 하나씩 옮긴다. 12장에서 짠 `shop.build-info`처럼 이미 호환되게 짰다면 이 단계는 짧다.

**4단계 — (b)는 플러그인을 최신 버전으로 올려본다.** 대부분의 활동적인 플러그인은 이미 9.x 호환 작업을 끝냈다. CHANGELOG에 "Configuration Cache compatible"이 적힌 버전을 찾는다. 없다면 GitHub issue를 검색한다.

**5단계 — 정말 해결이 안 되는 플러그인이 하나 남는다면.** 그 플러그인을 빼는 것까지 검토하되, 못 빼면 `problems=warn`을 유지한 채로 가는 것도 현실적인 선택이다. 캐시 효과는 못 얻지만 다른 가속(Build Cache, parallel)은 그대로 동작한다.

**6단계 — 모든 위반이 0이 되면 `problems=fail`로 바꾼다.** 이제 누군가 회귀를 일으키면 빌드가 막힌다. 정확성이 보장된다.

15장의 페인포인트 모음에서 다시 만나겠지만, 이 점진 도입은 큰 코드베이스에서 한 주에 다 끝나는 일이 아니다. 한 달에 걸쳐 위반을 한두 개씩 줄여간다고 생각하자. 그래도 1단계의 `warn` 한 줄을 켜는 순간부터 위반은 "보이는 것"이 되고, 보이는 것은 결국 줄어든다.

> **함정 박스 — IDE sync는 안 빨라진다**
>
> Configuration Cache를 켜면 CLI 빌드는 정말로 빨라진다. 그런데 IntelliJ에서 프로젝트를 sync(Reload Gradle Project)할 때는 왜 똑같이 느린가?
>
> 답은 슬프지만 명확하다. **Configuration Cache는 IDE sync 자체를 가속하지 않는다.** IDE sync는 별도의 Gradle invocation으로, 캐시되지 않는 모델 빌드 단계를 거친다. CLI에서 5초 걸리던 build가 1초로 줄어도, IDE sync는 그대로 30~60초가 걸린다.
>
> 임시 완화책으로는 `org.gradle.parallel=true`와 `org.gradle.jvmargs=-Xmx4g`가 도움이 된다. Daemon이 OOM으로 죽어서 sync가 재시작되면 더 느려지니까, JVM 힙은 넉넉히 잡아두자.
>
> 진짜 답은 다른 곳에 있다. Gradle 9.x에 incubating으로 들어온 **Isolated Projects**가 IDE sync를 정조준하는 차세대 기능이다. Configuration Cache가 "configuration phase의 결과를 저장"한다면, Isolated Projects는 "프로젝트들을 서로 격리해서 병렬 + 부분 invalidation"을 노린다. 아직 incubating이라 production에서 켜기엔 이르지만, 18장에서 다시 만나게 된다. 그때까지는 sync가 느린 게 우리가 뭘 잘못해서가 아니라는 사실 정도만 기억해두자. 마음의 평화에 도움이 된다.

## 한 곳에 모아두는 `gradle.properties` 표준 키

이번 장에서 다룬 키들이 여러 자리에서 나왔다. 한 곳에 정리해두면 새 프로젝트를 시작할 때마다 복사해서 쓰기 편하다. 13장의 마지막 결과물로서, 멀티 모듈 Spring Boot 빌드의 표준 `gradle.properties`를 한 페이지로 박아둔다.

| 키 | 권장값 | 의미 |
|---|---|---|
| `org.gradle.caching` | `true` | Build Cache 활성화 (task execution 결과 캐시) |
| `org.gradle.parallel` | `true` | 프로젝트 간 task 병렬 실행 |
| `org.gradle.configuration-cache` | `true` | Configuration Cache 활성화 (configuration phase 캐시) |
| `org.gradle.configuration-cache.problems` | 처음엔 `warn`, 안정화되면 `fail` | 위반 발견 시 동작 |
| `org.gradle.configuration-cache.parallel` | `true` | configuration phase 안에서 프로젝트 평가 병렬화 (9.x 안정) |
| `org.gradle.jvmargs` | `-Xmx4g -XX:+UseG1GC` | Daemon JVM 옵션. 멀티 모듈은 2g 이상 필수 |
| `org.gradle.workers.max` | `8` (또는 미지정) | 병렬 worker 상한. 미지정 시 CPU 코어 수 |

`ch13-config-cache/gradle.properties`에 이 표가 그대로 들어 있다.

```properties
# ch13-config-cache/gradle.properties
org.gradle.caching=true
org.gradle.parallel=true
org.gradle.configuration-cache=true
org.gradle.configuration-cache.problems=warn
org.gradle.configuration-cache.parallel=true
org.gradle.jvmargs=-Xmx4g -XX:+UseG1GC
org.gradle.workers.max=8
```

이 일곱 줄이 9.x 멀티 모듈 빌드의 성능 기본기다. 새 레포를 만들 때마다 처음에 박아두고 시작하는 편이 낫다.

## 마무리

13장의 출발에서 우리는 `org.gradle.configuration-cache=true` 한 줄을 켰다. 그 한 줄 뒤에 무엇이 따라오는지 차근차근 보았다. Configuration Cache는 무엇을 캐시하는가(configuration phase의 산출물), Build Cache와 어떻게 직교하는가(execution phase의 산출물), 9.0의 명시적 위반 보고가 무엇을 바꿨는가(silent fail의 종료), 우리가 12장에서 호환 패턴으로 짠 코드가 어떻게 회수되는가, 그리고 third-party plugin이 비명을 지를 때 점진적으로 도입하는 길이 무엇인가.

핵심을 두 줄로 줄이면 이렇다. **Configuration Cache는 옵션이 아니라 9.x의 표준이다. 그리고 `problems=warn`은 큰 코드베이스를 단계적으로 끌고 들어가기 위한 가장 우아한 도구다.** `warn`으로 켜는 순간부터 위반은 보이는 것이 되고, 보이는 것은 한 달 후, 두 달 후에는 0이 된다. 0이 된 자리에서 `fail`로 바꾸면 회귀까지 막힌다.

여기까지 와도 한 가지 풀리지 않은 의문이 남는다. **"우리 노트북에서는 빠른데, CI에서는 왜 똑같이 느린가?"** Build Cache가 머신 사이에 공유되지 않기 때문이다. Configuration Cache의 캐시 엔트리도 마찬가지다. 로컬 캐시는 머신 한 대 안에서만 의미가 있다.

그러면 CI에서 캐시를 살리려면 어떻게 해야 할까? 답은 14장에 있다. `gradle/actions/setup-gradle@v6`라는 GitHub Actions가 캐시를 PR과 main 사이에서 어떻게 운반하는지, Build Scan을 CI에서 어떻게 자동 발행하는지를 다음 장에서 본다. 13장에서 켠 일곱 줄의 `gradle.properties`가 CI에서도 그대로 의미를 가지려면 한 단계가 더 필요하다. 그 단계를 함께 밟아보자.
