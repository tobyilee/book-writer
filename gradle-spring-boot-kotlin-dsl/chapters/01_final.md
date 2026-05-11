# 1장. 왜 build.gradle.kts를 다시 짜야 하는가

Spring Boot 백엔드를 한 번이라도 만들어본 사람이라면, `build.gradle.kts` 파일을 열어본 적은 있을 것이다. 그런데 거기서 우리가 하는 일은 대개 정해져 있다. 의존성을 한 줄 추가하고, 가끔 `bootRun`을 돌리고, 빌드가 깨지면 Stack Overflow를 뒤지고. 그게 전부였다. 빌드 스크립트는 IDE가 알아서 처리해주는 '검은 상자'에 가까웠고, 우리는 거기에 손을 깊이 넣을 일이 거의 없다고 믿어왔다.

그런데 어느 순간부터 그게 충분치 않다는 의심이 든다. 모듈을 하나 둘 쪼개기 시작하면 `bootJar`가 이상하게 동작한다. CI에서는 매번 처음부터 빌드가 돌고, 누구는 30초에 끝나는 빌드가 다른 누구의 머신에서는 5분이 걸린다. 보안팀이 "transitive 의존성 검증은 어떻게 하느냐"고 물어오면 답을 못 한다. 어딘가에서 `Configuration Cache`라는 단어를 들었는데, 켜본 적은 없다. 켜면 빌드가 깨질 것 같아서 손을 못 댔다.

이게 우리만의 일은 아니다. 한국의 많은 Spring Boot 팀이 비슷한 상태에 있다. 빌드 스크립트는 "그냥 굴러가는 것"이고, 누가 손을 댈 때마다 무언가가 깨진다. 그래서 다들 손대지 않는다. 손대지 않으니 더 모르게 되고, 더 모르니 더 손대기가 무섭다.

이 책은 그 악순환을 끊기 위해 쓰였다.

## 빌드 스크립트는 운영의 일부다

먼저 한 가지 명제를 짚고 가자. **빌드 스크립트는 우리 시스템 운영의 일부다.** 이 한 문장에 동의하느냐가 이 책을 읽을 동기를 결정한다.

생각해보자. 우리가 운영 환경에서 마주치는 일들은 결국 어디에서 출발하는가. 멀티 모듈로 코드를 쪼개려면 빌드가 그 구조를 알아야 한다. CI에 빌드를 올리려면 빌드 스크립트가 CI를 친화적으로 받아들여야 한다. transitive 의존성을 신뢰하려면 빌드가 verification 메커니즘을 알아야 한다. OCI 이미지로 배포하려면 빌드가 그 이미지를 만들 줄 알아야 한다. GraalVM Native binary로 패키징하려면 빌드가 AOT를 처리해야 한다.

운영 환경의 거의 모든 결정이 빌드 스크립트로 흘러들어온다. 그런데 우리는 그 빌드 스크립트를 "Spring Initializr가 만들어준 그대로" 들고 있다. 그러니 멀티 모듈로 가다 사고가 나고, CI가 느리고, 보안 검토가 어렵다.

빌드 스크립트는 의존성 목록이 아니다. 빌드 스크립트는 **우리 팀이 코드를 어떻게 묶고, 어떻게 검증하고, 어떻게 배포하는가**에 대한 선언이다. 코드만큼 진지하게 다뤄야 할 자산이다.

이 명제를 받아들이고 나면, 그 다음은 자연스럽다. 빌드 스크립트도 코드처럼 진지하게 짜야 한다. 코드처럼 리팩토링하고, 코드처럼 테스트하고, 코드처럼 모듈화한다. 그게 이 책에서 함께 해볼 일이다.

## Gradle 9.5와 Spring Boot 4.0이라는 현재

그렇다면 어떤 도구로 짤 것인가. 이 책은 **Gradle 9.5와 Spring Boot 4.0**을 기준으로 한다. 이 조합은 우연이 아니다.

Gradle은 9.0에서 한 번 큰 정리를 했다. Daemon이 도는 JDK 최소 버전을 17로 올렸고, `jcenter()`를 완전히 제거했고, 오래 deprecated 상태였던 `Project#exec`/`javaexec`와 Convention API를 잘라냈다. Kotlin Gradle Plugin도 2.0+를 기본으로 요구한다. 무엇보다 **Configuration Cache가 preferred mode로 격상**됐다 — 9.0 이전에는 "켜볼 만한 옵션" 정도였다면, 9.x부터는 "기본적으로 켜고 가야 하는 것"으로 톤이 바뀌었다.

Spring Boot 4.0도 비슷한 시기에 자기 큰 정리를 했다. Gradle 8.14+ 또는 9.x를 요구하고, Kotlin 2.1을 기본으로 묶고, `paketobuildpacks/builder-noble-java-tiny`로 builder 기본값을 바꾸고, AOT와 Native 통합을 다시 다듬었다. Lazy property는 `=` 권장이 더 강해졌다.

두 도구의 큰 정리가 거의 같은 시기에 일어났다는 건 의미가 있다. **지금이 build.gradle.kts를 다시 짤 때**라는 뜻이다. 8.x 시절의 관행과 3.x 시절의 관행을 그대로 들고 9.x/4.0 위에 올리면 곳곳에서 이상한 마찰이 생긴다. 어차피 한 번 정리할 거라면, 새 위에 새 것으로 짓는 편이 낫다.

> **이미 Gradle 8.x를 쓰는 분께**
>
> 이 책은 9.5를 기준으로 쓰였다. 회사 빌드가 8.x에 머물러 있어도 책의 사고 모델은 그대로 통한다 — 대부분의 9.x 변경은 정리이지 새로운 패러다임이 아니다. 다만 회사 빌드를 9.x로 올릴 계획이 있다면, **17장의 마이그레이션 체크리스트**를 먼저 한 번 훑고 본문으로 들어와도 좋다. 본문 흐름을 따라가다 17장에서 만나도 좋고, 두 번째 만남이 더 와닿을 것이다.

## 가상 앱 shop을 따라간다

이 책은 레퍼런스가 아니다. 레퍼런스가 필요하면 공식 문서가 가장 좋다. 이 책이 하려는 건 **한 앱이 자라는 이야기를 따라가는 것**이다.

우리는 책 전체에서 `shop`이라는 가상의 Spring Boot 앱을 하나 들고 간다. 1장의 `shop`은 빌드 스크립트가 거의 비어 있다. 의존성 한 줄, plugin 두어 개. Spring Initializr가 막 뱉어낸 모습 그대로다. 그런데 책의 마지막에 도착했을 때 같은 `shop`은 이렇게 자라 있다 — 멀티 모듈로 쪼개져 있고, `buildSrc`와 `build-logic` included build로 build logic이 모듈화돼 있고, 커스텀 Gradle 플러그인이 git SHA와 빌드 시간을 자동으로 박아주고, Configuration Cache와 Build Cache로 인크리멘털 빌드가 빠르고, GitHub Actions에 Build Scan과 의존성 그래프가 자동으로 올라가고, GraalVM Native Image로 OCI 컨테이너에 들어간다. 의존성은 verification metadata와 lockfile로 묶여 있다.

한 앱이 18개 챕터를 거쳐 자라난다. 챕터마다 "지금 우리 앱이 어디까지 왔는가"를 한 줄로 박아두니, 자기 회사 빌드가 지금 어느 단계에 있는지 비교해볼 수 있을 것이다.

이게 단순 레퍼런스 책과 가장 다른 점이다. 우리는 빌드 도구의 모든 기능을 카탈로그처럼 훑지 않는다. 한 앱이 정말로 자라나는 흐름에서, **그 자람에 필요한 도구만** 그 자리에서 만난다. Composite Build를 왜 다른 챕터들 한참 뒤에서 만나는지, Configuration Cache를 왜 12장 다음에서 켜는지, 다 이유가 있다.

코드 표기 약속도 한 번 짚자.

- **Kotlin DSL이 기본**이다. Groovy DSL은 차이가 클 때만 박스로 짧게 병기한다. 회사 빌드가 아직 Groovy라도 따라올 수 있도록 핵심 매핑은 명시한다. 다만 책의 주인공은 Kotlin DSL이다.
- **함정 박스**가 자주 나온다. 실무에서 우리를 막아세우는 지점들을 본문에서 따로 격리해 표시해둔다. `> 함정`, `> 마이그레이션 노트`, `> Maven에서 옮겨온 분께` 같은 라벨이 붙어 있다.
- **Maven 비교 박스**는 Part I과 Part II에서 적극 쓴다. Part III 이후로 가면 거의 사라진다 — 그쯤이면 우리가 이미 Gradle 사고로 옮겨가 있을 테니까.

## 이 책이 약속하는 9가지

이 책을 다 통과하고 나면 Spring Boot 백엔드 개발자는 build.gradle.kts를 어디까지 만질 수 있게 되는가. 9가지로 약속해두자. 이 9가지가 이 책의 출구 상태다.

1. **Gradle의 멘탈 모델**을 자기 언어로 설명할 수 있다 — Settings, Project, Task, Configuration이 각각 무엇이고, 3-phase Lifecycle(Initialization → Configuration → Execution)이 빌드를 어떻게 옮기는지.
2. **Kotlin DSL의 lazy Property와 Provider API**로 빌드 스크립트를 쓸 수 있다. 어디가 eager 패턴이고, `=`와 `.set()`의 차이가 무엇이고, type-safe accessor가 언제 노출되는지 골라낼 수 있다.
3. **Version Catalog와 BOM(platform)** 조합으로 의존성을 다스린다. `io.spring.dependency-management` 플러그인의 자리가 어디인지, `implementation`과 `api`의 차이가 무엇인지, `enforcedPlatform`은 왜 권장되지 않는지 안다.
4. **멀티 모듈 Spring Boot 프로젝트**를 `subprojects {}` 안티패턴 없이 Convention Plugin으로 정리한다. 4개 모듈에 똑같이 들어가던 코드가 각 한 줄로 줄어든다.
5. **Configuration Cache를 켜고**, 위반을 진단하고, 자기 빌드를 호환되게 고친다. third-party 플러그인이 비명을 지를 때 점진 도입 전략을 안다.
6. **커스텀 Task와 Plugin**을 Provider/Property 기반으로 만든다. Configuration Cache와 호환되게, Input/Output 어노테이션을 정확히 붙여서, Build Cache hit이 일어나게.
7. **GitHub Actions**에 `gradle/actions/setup-gradle`로 빌드 캐시, Build Scan, Dependency Graph를 붙인다. PR마다 build와 integrationTest가 빠르게 돈다.
8. **GraalVM Native Image, Dependency Verification, Locking, Repository Content Filtering**을 운영 환경에 적용할 판단 기준을 갖는다. "켤까 말까"가 아니라 "언제 어떤 비용을 지불할 가치가 있는가"로 사고한다.
9. **Gradle 9.x 마이그레이션**을 자신감 있게 진행한다. 회사 빌드를 8.x나 7.x에서 9.x로 올리는 일이 막연한 두려움에서 점검 가능한 체크리스트로 바뀐다.

이 9가지 중에서 지금 자기가 할 수 있는 게 몇 개인가. 한 번 세어보고 시작하자. 책을 다 읽은 뒤에 다시 세어보면 좋다.

> **Maven에서 옮겨온 분께**
>
> 환영한다. 이 책은 당신을 명시적으로 끌어안으려고 쓰였다. Maven에서 익숙한 거의 모든 개념은 Gradle에 자리가 있다 — 다만 이름과 동작이 미묘하게 다르다. **phase 모델은 task graph로 옮겨가고**, `<dependencyManagement>`는 `platform()` BOM 또는 `io.spring.dependency-management` 플러그인으로, `<parent>` pom은 Convention Plugin으로, `<profile>`은 variant + property로, `<pluginManagement>`는 `settings.gradle.kts`의 `pluginManagement {}`로. 정확한 1:1 매핑 표는 4장에서 한 번에 받는다. 그러니 1장과 2장이 어색해도 너무 빨리 책을 덮지 말자. 4장에 다리가 놓여 있다. Maven으로 돌아갈 일은 없게 만들 생각이다.

> **wrapper distribution-type — 첫 빌드 전에 이 한 줄**
>
> `./gradlew`를 처음 쓰는 분에게 미리 한 가지 처방을 건넨다. wrapper를 만들 때 distribution type을 명시하지 않으면 기본값으로 `all` distribution을 받는다. 소스와 문서까지 들어 있어 200MB가 넘는다. 첫 빌드가 한참 지연된다. 다음 한 줄을 wrapper 생성 시 반드시 같이 쓰자.
>
> ```bash
> ./gradlew wrapper --gradle-version 9.5 --distribution-type=bin
> ```
>
> `bin` distribution은 30MB 남짓이다. CI에서도 wrapper 다운로드가 짧아진다. 자세한 설명은 14장에서 다시 만난다. 그때까지는 이 한 줄로 충분하다.

## 1장을 닫으며

여기까지가 이 책의 입구다. 빌드 스크립트가 운영의 일부라는 명제, Gradle 9.5와 Spring Boot 4.0이라는 현재 좌표, 가상 앱 `shop`이 자라는 이야기로 18장을 따라간다는 약속, 그리고 출구에서 받게 될 9가지.

그런데 정작 빌드를 다시 짜려면 한 가지가 먼저 필요하다. **Gradle이 빌드를 어떻게 보는가** — 그 사고 모델 자체다. `settings.gradle.kts`와 `build.gradle.kts`가 각각 무엇을 책임지는지, Task가 왜 객체로 모델링되는지, Lifecycle 3-phase가 빌드를 어떻게 옮기는지, Configuration이 declarable/resolvable/consumable로 왜 나뉘는지. 이 모델을 자기 언어로 잡지 않으면, 그 뒤의 모든 챕터가 단순 암기로 흘러간다.

2장에서 그 모델을 함께 잡아보자. 코드는 거의 없다. 사고 모델이 우선이다. Maven 출신이라면 거기서 phase 모델과 task graph의 결정적 차이를 만나게 될 것이고, Gradle을 막연히 쓰던 분이라면 그동안 손에 잡히지 않던 개념들이 자리를 찾아갈 것이다.
