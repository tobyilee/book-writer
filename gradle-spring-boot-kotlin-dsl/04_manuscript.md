# 빌드를 다시 짠다

## Spring Boot × Gradle 9.5 × Kotlin DSL 실전 가이드

저자: Toby-AI · 발행: 2026년 5월 · 판본 v1.0.1

---

## 머리말

이 책은 한 가지 사실에서 시작한다. **build.gradle.kts는 우리가 가장 자주 열어보면서, 가장 적게 들여다보는 파일이다.** Spring Boot 백엔드를 만들어본 사람이라면 이 파일을 매주 열어 의존성 한 줄을 더한다. 그러나 그 파일이 정확히 무엇을 책임지는가, Gradle이 그 안의 코드를 어떻게 평가하는가, 왜 어떤 줄은 `tasks.register`로 쓰고 어떤 줄은 `tasks.named`로 써야 하는가 — 이 질문들 앞에 막연한 침묵이 있었다. 누구도 진지하게 답해주지 않았고, 우리도 진지하게 묻지 않았다.

그 침묵이 회사 빌드를 키울 때 비용으로 돌아온다. 모듈을 쪼개려는 순간 `bootJar`가 이상하게 동작한다. CI 빌드가 매번 처음부터 돈다. 누군가의 노트북에서는 30초에 끝나는 빌드가 다른 누군가의 머신에서는 5분이 걸린다. 보안팀이 transitive 의존성 검증을 묻는데 답할 도구가 없다. Configuration Cache라는 단어를 들었지만 켜본 적은 없다. 켜면 깨질 것 같아서.

이 책은 그 침묵을 깨려고 쓰였다. **build.gradle.kts에 의존성 몇 줄만 추가하던 Spring Boot 백엔드 개발자가 멀티 모듈·커스텀 플러그인·Native까지 자기 빌드를 도구로 키우는 여정**을 18장에 걸쳐 따라간다. 책의 한가운데에는 `shop`이라는 가상 앱 한 채가 있다. 1장의 `shop`은 의존성 한 줄짜리 Hello World다. 18장의 `shop`은 멀티 모듈로 쪼개져 있고, `buildSrc`와 `build-logic` included build로 build logic이 모듈화돼 있고, 커스텀 Gradle 플러그인이 git SHA를 자동으로 박아주고, Configuration Cache와 Build Cache로 incremental 빌드가 빠르고, GitHub Actions에 Build Scan과 dependency graph가 자동으로 올라가고, GraalVM Native Image로 OCI 컨테이너에 들어가고, 의존성은 verification metadata와 lockfile로 묶여 있다.

같은 앱이 자라는 흐름을 따라가는 동안 우리는 두 가지를 얻는다. 하나는 **Gradle 9.5와 Spring Boot 4.0의 정확한 사고 모델**이다. Settings/Project/Task/Configuration이 각각 무엇이고, 3-phase Lifecycle이 빌드를 어떻게 옮기고, Provider/Property API가 왜 lazy 평가의 척추이고, Configuration Cache가 무엇을 캐시하고 어떻게 깨지는지. 다른 하나는 **회사 빌드를 한 단계 위로 올릴 도구 상자**다. Convention Plugin으로 중복을 정리하는 길, `bootJar` 함정을 진단하는 5분 체크리스트, GitHub Actions에 캐시를 회수시키는 한 줄, Dependency Verification으로 supply chain을 잠그는 운영 패턴까지.

### 누구를 위한 책인가

이 책은 Spring Boot로 개발은 해봤지만 `build.gradle.kts`는 의존성 한두 줄 더하는 영역으로만 써온 백엔드 개발자를 정면으로 끌어안는다. Maven 출신이라 Gradle의 멘탈 모델이 어색한 분, 멀티 모듈을 시도했다가 `bootJar` 함정에 한 번 빠져본 분, Configuration Cache라는 단어를 들었지만 켤 엄두를 못 낸 분 — 이 책은 당신을 명시적으로 끌어안는다. Maven 비교는 Part I·II에서 적극적으로 박스로 다루고, Gradle 9.x 신문법은 본문 표준으로 쓴다.

이 책은 또한 한 가지가 아니다. **레퍼런스가 아니다.** 레퍼런스가 필요하면 공식 Gradle User Guide가 가장 좋다. 이 책이 하려는 일은 그 레퍼런스의 단어들이 한 앱이 자라는 흐름 안에서 어떤 자리에 들어가는지를 자기 언어로 잡는 것이다. 모든 챕터에 실제로 빌드되는 코드가 동반된다. 챕터마다 "이 챕터에서 자라는 앱 상태"를 한 줄로 박아두니, 자기 회사 빌드가 지금 어느 단계에 있는지 비교해볼 수 있다.

### 어떻게 읽으면 좋은가

차례대로 읽는 것을 권한다. `shop` 앱은 1장에서 18장까지 한 흐름으로 자라기 때문이다. 다만 한 가지 예외가 있다. 회사 빌드가 8.x나 7.x에 머물러 있고 9.x로 옮기는 마이그레이션이 시급하다면, **17장의 마이그레이션 체크리스트를 먼저 한 번 훑어도 좋다.** 본문 흐름을 따라가다 17장에서 두 번째로 만나는 편이 더 와닿을 것이다.

박스와 본문의 관계도 한 줄 짚어두자. 본문은 흐름이고, 박스는 격리된 디테일이다. 박스를 건너뛰어도 본문은 매끄럽게 흐른다. Maven 비교 박스는 Part I·II에서 자주 등장하고, Part III 이후로는 거의 사라진다 — 그쯤이면 우리가 이미 Gradle 사고로 옮겨가 있을 테니까. 함정 박스는 실무에서 막히는 지점을 본문에서 격리해 표시한다. 마이그레이션 노트 박스는 9.0 이전의 옛 패턴과 현행 표준의 차이를 짚는다.

코드 표기 약속도 미리 두 가지. **Kotlin DSL이 기본이다.** Groovy DSL은 차이가 클 때만 박스로 짧게 병기한다. 그리고 **모든 챕터의 코드는 `ch{NN}-{slug}/` 폴더에 산다** — `ch01/`, `ch04-bootapp/`, `ch08-multimodule/`, `ch09-convention/`, `ch11-composite/`, `ch12-custom-plugin/`, `ch13-config-cache/`, `ch14-ci/`, `ch15-native/`, `ch16-security/`. 챕터마다 도입부에 그 챕터가 어느 폴더에서 동작하는지 한 줄로 박아둔다. 독자가 자기 앱이 자라는 흐름을 폴더 단위로 추적할 수 있다.

### 왜 지금 이 책을 쓰는가

Gradle은 9.0에서 한 번 큰 정리를 했다. Daemon JDK가 17+로 올라가고, `jcenter()`가 제거되고, `Project#exec`과 Convention API가 잘렸다. Configuration Cache가 preferred mode로 격상됐다. Spring Boot 4.0도 비슷한 시기에 자기 큰 정리를 했다. Gradle 8.14+를 요구하고, Kotlin 2.1을 묶고, Paketo builder 기본값을 바꾸고, AOT와 Native 통합을 다듬었다.

두 도구의 큰 정리가 거의 같은 시기에 일어났다는 건 의미가 있다. **지금이 build.gradle.kts를 다시 짤 때다.** 8.x 시절의 관행을 그대로 9.x에 올리면 곳곳에서 미묘한 마찰이 생긴다. 어차피 한 번 정리할 거라면, 새 위에 새 것으로 짓는 편이 낫다. 이 책이 그 새 짓기를 함께 한다.

자, 그러면 1장으로 가자. `shop`이라는 가상의 앱 한 채를 들고, 18장에 걸쳐 빌드를 다시 짠다.

## 차례

### Part I — Gradle 사고방식

- 1장. 왜 build.gradle.kts를 다시 짜야 하는가
- 2장. Gradle의 사고 모델 — Settings, Project, Task, Lifecycle
- 3장. Kotlin DSL 그리고 그 함정

### Part II — 단일 모듈 Spring Boot를 제대로 빌드한다

- 4장. Maven에서 옮겨오는 다리 — pom.xml과 build.gradle.kts의 1:1 매핑
- 5장. 의존성을 다스리는 정석 — Version Catalog와 BOM
- 6장. Spring Boot Gradle 플러그인의 내부 — bootJar, bootRun, bootBuildImage
- 7장. 테스트를 분리한다 — JVM Test Suite로 통합 테스트

### Part III — 규모를 키운다

- 8장. 모듈을 쪼갠다 — settings 구조와 프로젝트 간 의존
- 9장. bootJar 함정 — library 모듈에서 빈 jar가 나오는 사고를 어떻게 진단하고 어떻게 막는가
- 10장. Convention Plugin으로 build logic을 모듈화한다
- 11장. buildSrc 한계를 넘는다 — build-logic included build와 Composite Build

### Part IV — 빌드를 도구로 만든다

- 12장. 커스텀 Task와 Plugin — Provider/Property로 lazy하게
- 13장. Configuration Cache를 켠다 — 위반을 진단하고 호환되게 고친다
- 14장. CI에 올린다 — GitHub Actions와 Build Scan

### Part V — 운영의 무게

- 15장. GraalVM Native Image로 패키징한다
- 16장. 의존성 보안 — Verification, Locking, Repository Content Filtering
- 17장. Gradle 9.x로 옮긴다 — 마이그레이션 노트 모음
- 18장. 이제 어디로 갈 것인가

### 부속

- 맺음말
- 참고문헌
- 판권

---

# Part I — Gradle 사고방식

Maven에서 옮겨온 사람도, Spring Initializr가 만들어준 빌드 스크립트를 그대로 들고 살아온 사람도, 시작은 사고 모델이다. 빌드 도구가 빌드를 어떻게 객체로 보고, 그 객체들을 어떤 순서로 깨워서 task graph로 옮기는지 — 이 모델을 자기 언어로 그릴 수 있어야 그 다음의 모든 결정이 단순 암기에서 벗어난다. `subprojects {}`가 왜 안티패턴인지, `tasks.register`와 `tasks.create`의 차이가 왜 단순 문법 취향이 아닌지, Kotlin DSL의 type-safe accessor가 왜 `plugins {}` 블록 다음에만 노출되는지 — 이런 질문들의 답이 모두 사고 모델에서 따라 나온다.

Part I의 세 챕터는 코드를 최소한으로 둔다. 1장에서 책 전체의 약속 9가지를 받고, 2장에서 Settings/Project/Task/Configuration/Lifecycle을 자기 언어로 잡고, 3장에서 그 사고 모델을 Kotlin DSL이라는 표면 위에서 12줄짜리 첫 빌드 스크립트로 풀어본다. Maven 출신을 명시적으로 끌어안는 부이기도 하다 — 비교 박스가 자주 등장하고, "Maven에서 옮겨온 분께"라는 라벨이 곳곳에 붙어 있다.

Part I이 끝나는 자리에서 우리 손에는 `ch01/`의 12줄짜리 build.gradle.kts 하나가 있다. 작아 보여도, Settings/Project/Plugin/declarable configuration이 다 등장하는 완결된 빌드다. 이 자리에서 출발해서, Part II에서는 진짜 Spring Boot 앱을 빌드하기 시작한다.

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

---

# Part II — 단일 모듈 Spring Boot를 제대로 빌드한다

회사 빌드는 보통 단일 모듈 앱 한 채에서 시작한다. Spring Initializr가 만들어준 build.gradle.kts에 의존성 몇 줄을 더하고, `./gradlew bootRun`으로 띄우고, `./gradlew test`로 단위 테스트를 돌린다. 거기서 멈춰도 일은 된다. 다만 그 빌드가 "잘 짜여진" 빌드인지를 묻기 시작하면 답이 막막해진다. `dependencyManagement`는 어디에 쓰는 게 맞나, `implementation`과 `api`의 차이는 무엇인가, `bootJar`가 만드는 fat jar의 안에는 정확히 무엇이 들어 있는가, 통합 테스트를 단위 테스트와 같은 `test` task에 욱여넣지 않으려면 어떻게 해야 하는가 — 이 질문들이 운영의 무게를 만들기 시작하는 자리다.

Part II의 네 챕터는 이 질문들에 정면으로 답한다. 4장에서 Maven의 모든 개념이 Gradle의 어디로 가는지를 표 하나와 한 줄씩 읽는 build.gradle.kts로 다리를 놓고, 5장에서 BOM과 Version Catalog의 직교 관계를 잡고, 6장에서 `bootJar`/`bootRun`/`bootBuildImage`의 내부를 들여다보고, 7장에서 JVM Test Suite로 통합 테스트를 분리한다. 이 부의 끝에서 우리의 `ch04-bootapp/`은 "기본기는 다 있는, 단일 모듈로는 부족함 없는 빌드"가 된다. 의존성 명세는 catalog가 보관하고, transitive 정렬은 BOM이 책임지고, 실행 가능한 fat jar와 OCI 이미지는 Spring Boot 플러그인이 책임지고, 테스트는 빠른 것과 무거운 것이 자기 자리에서 자기 일을 한다.

회사 프로덕션 코드 한 모듈을 그대로 흉내내도 어색하지 않은 상태. 그게 Part II가 도착하려고 하는 자리다.

# 4장. Maven에서 옮겨오는 다리 — pom.xml과 build.gradle.kts의 1:1 매핑

1장에서 "Maven에서 옮겨온 분께"라는 박스로 약속을 하나 걸어뒀다. phase는 task graph로, dependencyManagement는 platform/BOM으로, parent pom은 Convention Plugin으로. 정확한 매핑은 4장에서 받는다고 했었다. 이 장이 그 약속을 받는 자리다.

Maven으로 5년을 짠 사람이 어느 날 Gradle 프로젝트에 던져졌다고 해보자. Spring Initializr에서 Gradle - Kotlin DSL을 골라 다운로드를 받고, IntelliJ로 열어 본다. `pom.xml`이 있어야 할 자리에 `settings.gradle.kts`와 `build.gradle.kts`라는 두 파일이 있다. 둘 다 열어보면 어쩐지 본 듯한 단어들이 흩어져 있는데 — `dependencies`, `plugins`, `repositories` — 정작 우리가 알던 `<dependencyManagement>`, `<parent>`, `<profile>` 같은 친숙한 친구들은 보이지 않는다. 어디 갔지?

이런 상황이 가장 난감하다. 새 도구를 처음부터 배우는 것보다 더 어려운 건, 옛 도구의 모든 개념이 어디로 갔는지 모르는 상태에서 IDE 자동완성 하나에 기대 더듬더듬 짜는 것이다. 어디로 갔는지를 모르니, 자기가 잘 짜고 있는지조차 알 수가 없다.

이번 장에서 우리는 그 매핑을 정면으로 받는다. Maven의 9개 핵심 개념이 Gradle에서 정확히 어디로 갔는지 표 하나로 그리고, 그 다음 `ch04-bootapp/` 폴더에서 동작하는 Spring Boot 단일 모듈 앱의 `settings.gradle.kts`와 `build.gradle.kts`를 한 줄씩 같이 읽어본다. 이 챕터를 통과하고 나면, 우리가 알던 Maven 개념은 모두 "여기 있다"고 손가락질할 수 있게 될 것이다.

> **이번 챕터는 `ch04-bootapp/` 폴더에서 동작한다.** Spring Initializr가 만든 단일 모듈 Spring Boot 앱이 이번 장의 기반이다. 이후 챕터들이 모두 이 앱 위에 차곡차곡 쌓인다. Toolchain까지 박힌, 회사에 그대로 가져가도 부끄럽지 않을 최소 구성을 목표로 한다.

## 매핑의 큰 그림

먼저 거시 지도부터 보자. Maven에서 익숙했던 개념 9개가 Gradle 9.5에서 어디에 자리잡는지의 매핑표다. 본문에서 하나씩 풀어볼 예정이지만, 일단 전체 그림이 한 번에 보여야 마음이 놓인다.

| Maven (pom.xml) | Gradle (Kotlin DSL) | 자세히 |
|---|---|---|
| `<dependencies>` | `dependencies { implementation(...) }` | 5장 |
| `<dependencyManagement>` | `dependencies { implementation(platform(...)) }` 또는 `io.spring.dependency-management` 플러그인 | 5장 |
| `<parent>` (spring-boot-starter-parent) | `plugins { id("org.springframework.boot") }` + Convention Plugin | 본 장 + 10장 |
| `<profile>` | `bootRun --args` + `-P` Project property + variant | 본 장 |
| `<pluginManagement>` | `settings.gradle.kts`의 `pluginManagement { }` | 본 장 |
| `<repositories>` | `settings.gradle.kts`의 `dependencyResolutionManagement { repositories { } }` | 본 장 |
| `mvn clean install` | `./gradlew clean build` | 본 장 |
| `mvn` 명령 (시스템 설치) | `./gradlew` (프로젝트 wrapper) | 본 장 |
| `<properties><java.version>` | `java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }` | 본 장 |

표만 봐서는 와닿지 않을 것이다. 표를 외우자는 게 아니다. 표는 지도일 뿐, 우리는 이제 길로 들어선다. 하나하나 본문에서 코드로 만나보자.

한 가지 미리 짚고 가자. Maven은 `pom.xml` 한 파일이 모든 걸 했다 — 빌드의 입구부터 의존성, 플러그인, repository까지. Gradle은 그 책임을 두 파일로 나눈다. **`settings.gradle.kts`는 빌드의 입구**이고, **`build.gradle.kts`는 한 프로젝트의 구체적인 빌드 정의**다. 9.5 시점의 Gradle은 settings의 책임을 더 명확히 한 방향으로 가고 있다 — repository와 plugin 버전 관리는 settings에서, 의존성과 task 정의는 build에서. 이 분리가 처음에는 번거롭게 느껴지지만, 멀티 모듈로 가면 이 분리가 왜 좋은지 자연스럽게 알게 된다. 일단은 "settings는 입구, build는 본문"이라고 기억해두자.

## settings.gradle.kts — pluginManagement와 dependencyResolutionManagement

`ch04-bootapp/`의 `settings.gradle.kts` 전체를 먼저 보자. 9.5 시점의 표준 골격이다.

```kotlin
// settings.gradle.kts
pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

plugins {
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}

dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories {
        mavenCentral()
    }
}

rootProject.name = "shop"
```

13줄짜리 파일인데, 이 안에 Maven에서 우리가 알던 두 개념이 통째로 들어와 있다. 하나씩 짚어보자.

**`pluginManagement { }` 블록.** Maven의 `<pluginManagement>`에 정확히 대응한다. Maven에서는 부모 pom의 `<pluginManagement>`에 플러그인 버전을 박아두면, 자식 pom들이 버전 없이 플러그인 id만으로 참조했다. Gradle도 같은 발상이다. **플러그인을 어디서 찾을지(`repositories`), 그리고 버전을 어디서 관리할지를 한 곳에 모은다.** 멀티 모듈 빌드가 되면 진가가 드러난다. `app`, `domain`, `payment` 세 모듈의 `build.gradle.kts`에 각각 `id("org.springframework.boot") version "4.0.6"`을 박을 필요 없이, settings의 `pluginManagement`에 버전을 한 번 박고 각 모듈은 `id("org.springframework.boot")`만 적으면 된다. 단일 출처의 원칙이다.

지금 우리 빌드는 단일 모듈이라 그 효과를 직접 느끼긴 어렵다. 그래도 처음부터 `pluginManagement` 골격을 가지고 가는 게 좋다. 멀티 모듈로 옮기는 8장에서 이 골격 그대로 재사용된다.

**`dependencyResolutionManagement { }` 블록.** 이건 9.x에서 자리가 굳어진 신문법이다. Maven에서는 각 pom마다 `<repositories>`를 자유롭게 선언할 수 있었다. 부모 pom에 mavenCentral을 박아도, 자식 pom이 자기만의 private repo를 추가할 수 있었다. 편리해 보이지만, 멀티 모듈 회사 프로젝트가 되면 끔찍한 일이 된다 — 누군가 자기 모듈에 사내 Nexus가 아닌 임의의 외부 repo를 추가해버리면, 우리 빌드의 의존성 출처가 한순간 통제 불가가 된다. 보안팀이 잠을 못 자는 이유다.

Gradle 9.5의 표준은 이걸 settings 한 곳에서만 선언하라고 강제할 수 있게 했다. `repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS` 한 줄이 그 강제 장치다. 이 줄을 박아두면, 어떤 하위 프로젝트의 `build.gradle.kts`에서든 `repositories { }` 블록을 추가하는 순간 빌드가 빨간 메시지를 뱉으며 멈춘다. "이 빌드의 repo는 settings에서만 선언할 수 있습니다"라고. 처음 만나면 짜증이 날 수도 있다. 그런데 이 강제가 멀티 모듈 빌드의 안전망이다. 회사 표준 repo만 쓰게 만들고 싶다면, 이 한 줄로 끝난다.

**`foojay-resolver-convention` 플러그인.** 이건 Maven에는 정확히 대응하는 게 없다. Toolchain 자동 다운로드를 담당하는 settings 수준 플러그인이다. 자세한 건 잠시 후 박스에서 한 번에 정리한다.

**`rootProject.name`.** 별것 아닌 줄 하나지만 의미가 있다. 폴더 이름을 그대로 쓰지 않고 명시하면, 이 프로젝트가 IDE 모듈명·publish 좌표·build scan에서 일관되게 `shop`으로 보인다. 폴더 이름이 `shop-gradle-journey-ch04-bootapp` 같은 길고 너저분한 이름이어도, 빌드 식별자는 깔끔하게 `shop`이다. 처음부터 박아두자.

> **wrapper distribution-type — 첫 빌드 전에 한 줄**
>
> 1장 박스에서 한 번 짚었지만, `ch04-bootapp/`에서 본격적으로 빌드를 돌리기 전에 다시 확인하자. `gradle/wrapper/gradle-wrapper.properties`의 `distributionUrl`이 `gradle-9.5-bin.zip`으로 끝나는가, `gradle-9.5-all.zip`으로 끝나는가? 후자라면 200MB가 넘는 소스 포함 배포본을 받는다. 첫 빌드가 한참 길어지고, CI runner들이 매번 그걸 캐시한다. 처방은 한 줄이다.
>
> ```bash
> ./gradlew wrapper --gradle-version 9.5 --distribution-type=bin
> ```
>
> `bin`은 실행 바이너리만 받는다. IDE에서 소스 점프가 어차피 필요하면 IntelliJ가 알아서 GitHub에서 가져온다. `all`을 받는 시대는 끝났다. 잊지 말자.

> **Toolchain의 자리**
>
> `build.gradle.kts`의 `java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }` 한 블록과, 위 settings의 `id("org.gradle.toolchains.foojay-resolver-convention")` 한 줄이 짝을 이룬다. 이 두 줄을 4장에서 미리 박고 가야 하는 이유가 있다.
>
> Gradle의 Toolchain은 Maven에서는 잘 안 쓰던 개념이다. 핵심은 한 문장이다 — **Daemon JVM ≠ Build JVM.** Gradle Daemon 자체는 자기가 깔린 JDK 위에서 돈다 (9.x는 17+ 요구). 그런데 우리가 컴파일하고 테스트할 대상 JDK는 별개로 고를 수 있다. 같은 머신에서 JDK 17과 JDK 21이 깔려 있어도, build script가 "이 빌드는 21로 컴파일한다"고 선언하면 Gradle이 21을 골라 그걸로 컴파일한다. 21이 머신에 없으면? `foojay-resolver-convention`이 자동으로 Adoptium에서 받아온다. CI runner마다 JDK 버전이 들쭉날쭉해도 빌드 결과가 같다는 게 이 메커니즘의 약속이다.
>
> 왜 4장부터 박는가? 단일 모듈에서 Toolchain을 잡아두지 않고 멀티 모듈로 넘어가면, 모듈마다 JDK 버전이 미묘하게 다른 상태가 생긴다. 한 번 그렇게 되면 풀기 번거롭다. 처음부터 settings에 foojay를, build에 toolchain을 박아두는 편이 낫다. 회사에서 어떤 JDK가 깔린 머신을 받든, 우리 빌드는 21로 컴파일된다 — 이게 약속할 수 있는 상태다.

## build.gradle.kts — 한 줄씩 읽어보자

settings는 입구였다. 이제 본문이다. `ch04-bootapp/build.gradle.kts` 전체를 펼쳐놓고 한 줄씩 읽어보자.

```kotlin
// build.gradle.kts
plugins {
    id("org.springframework.boot") version "4.0.6"
    id("io.spring.dependency-management") version "1.1.6"
    kotlin("jvm") version "2.2.0"
    kotlin("plugin.spring") version "2.2.0"
}

group = "com.example"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.jetbrains.kotlin:kotlin-reflect")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5")
}

tasks.test {
    useJUnitPlatform()
}
```

30줄이 안 된다. Maven `pom.xml`로 같은 일을 하려면 70~100줄짜리 XML이 필요하다. 줄 수가 짧다고 더 좋은 건 아니다 — 다만 이 짧음의 정체가 뭔지를 정확히 보자.

### plugins 블록

```kotlin
plugins {
    id("org.springframework.boot") version "4.0.6"
    id("io.spring.dependency-management") version "1.1.6"
    kotlin("jvm") version "2.2.0"
    kotlin("plugin.spring") version "2.2.0"
}
```

Maven의 `<build><plugins>`와 같은 위치다. 그런데 동작 방식이 사뭇 다르다. Maven 플러그인은 phase에 goal을 묶는 방식이고, Gradle 플러그인은 **빌드 객체에 task와 configuration을 주입하는 방식**이다. 예를 들어 `org.springframework.boot` 플러그인을 적용하는 순간, 우리 빌드에는 `bootJar`, `bootRun`, `bootBuildImage`, `bootTestRun` 같은 task들이 새로 등록되고, `developmentOnly`, `productionRuntimeClasspath` 같은 configuration이 추가된다. 6장에서 이 안을 깊게 들여다본다.

여기서 미리 한 가지 안내 박스를 받자.

> **`id("io.spring.dependency-management")` 한 줄에 대해서**
>
> 이 플러그인은 Maven의 `<dependencyManagement>`를 Gradle에서 흉내내주는 보조 도구다. Maven에서 옮겨온 사람이 BOM을 가장 익숙하게 쓸 수 있도록 만들어졌다. 다만 Gradle 9.5 기준의 본격적인 권장은 이 플러그인 없이 `dependencies` 블록에서 `implementation(platform(...))`을 직접 쓰는 길이다 — 더 빠르고, Configuration Cache 친화적이다. 두 길의 선택은 5장에서 깊게 다룬다. 이 장에서는 일단 Spring Initializr가 만들어준 그대로 두고 간다. 두 길의 분기점은 5장이 알려준다.

`plugins { }` 블록의 또 한 가지 특징은, **블록 안에서 적용된 플러그인이 그 다음 줄들에서 type-safe accessor로 노출된다**는 점이다. 즉 `plugins { id("org.springframework.boot") ... }` 다음에 나오는 코드에서는 `tasks.named<BootJar>("bootJar") { ... }` 같은 타입 안전한 호출이 컴파일 타임에 잡힌다. 만약 우리가 `apply(plugin = "org.springframework.boot")` 같은 옛 방식으로 플러그인을 적용하면 accessor가 안 생긴다. 이게 Kotlin DSL에서 `plugins { }` 블록을 표준으로 쓰는 이유다.

### group / version / java

```kotlin
group = "com.example"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

Maven의 `<groupId>`, `<artifactId>`, `<version>`이 여기로 왔다. `artifactId`는 어디 갔지? `settings.gradle.kts`의 `rootProject.name`이 그 자리다. 빌드 산출물의 좌표가 `com.example:shop:0.0.1-SNAPSHOT`이 되는 셈이다.

`java { toolchain { } }` 블록이 박혀 있다. 앞서 박스에서 설명한 그 자리다. Maven에서는 보통 `<properties><java.version>21</java.version></properties>`로 했던 일이, Gradle에서는 toolchain의 `languageVersion`이다. 차이는 단지 표기법이 아니다 — Maven의 `java.version`은 "이 JDK로 컴파일하라"는 단순 지시였지만, Gradle의 `languageVersion`은 "이 JDK가 없으면 받아와서라도 그걸로 컴파일하라"는 보장이다. CI runner의 JDK가 17이어도 우리 빌드는 21로 컴파일된다.

`vendor`는 일부러 박지 않았다. Adoptium을 기본으로 받게 되지만, 회사가 Corretto나 Zulu를 표준으로 쓴다면 `vendor = JvmVendorSpec.AMAZON` 같은 한 줄을 추가하면 된다. 작은 디테일이지만 회사 표준화 정책과 맞물리는 부분이다.

### dependencies

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.jetbrains.kotlin:kotlin-reflect")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5")
}
```

Maven `<dependencies>`의 자리다. 한눈에 두 가지 차이가 들어온다.

**첫째, scope의 이름이 다르다.** Maven의 `<scope>compile</scope>`은 Gradle에서 `implementation`이다. `<scope>test</scope>`는 `testImplementation`이다. 단순한 이름 변경이 아니라 의미가 살짝 다르다. Maven의 `compile` scope는 transitive하게 소비자에게도 노출되는 반면, Gradle의 `implementation`은 **소비자에게 노출되지 않는다**. 즉 `app`이 `domain` 모듈을 의존하고 `domain`이 `lib-foo`를 `implementation`으로 의존한다면, `app`은 `lib-foo`의 클래스에 컴파일 타임에 접근할 수 없다. 이게 캡슐화의 강제다. ABI가 변해도 transitive 재컴파일이 폭발하지 않는다. 5장에서 이 의미론을 다시 본다.

**둘째, 버전이 없다.** `implementation("org.springframework.boot:spring-boot-starter-web")` 줄에는 콜론 두 개로 끝나는 좌표만 있을 뿐, `:4.0.6` 같은 버전이 없다. 어디서 오는가? `io.spring.dependency-management` 플러그인이 Spring Boot BOM을 자동으로 적용해, 모든 Spring 관련 의존성의 버전을 BOM에서 가져온다. Maven `spring-boot-starter-parent`를 부모로 두면 같은 일이 일어났다 — 그래서 Maven 출신이 가장 빨리 적응하는 부분이다. 5장에서 이 BOM 적용을 plugin 없이 `implementation(platform(...))`으로 직접 하는 더 권장되는 길을 만난다.

### tasks.test useJUnitPlatform()

```kotlin
tasks.test {
    useJUnitPlatform()
}
```

Maven에서는 `<plugin><groupId>org.apache.maven.plugins</groupId><artifactId>maven-surefire-plugin</artifactId>...`로 XML 10여 줄을 써야 했던 일이 Kotlin DSL에서는 두 줄이다. `test` task는 `java` plugin이 만들어주는 표준 task이고, 그 task의 설정 한 줄 — "JUnit 5(Jupiter)를 쓰겠다" — 이 끝이다.

여기서 `tasks.test { }`는 Kotlin DSL의 type-safe accessor 형태다. 내부적으로는 `tasks.named<Test>("test") { ... }`와 같다. accessor가 type을 알기 때문에 `useJUnitPlatform()`이 IDE 자동완성에서 바로 뜬다. 만약 `apply(plugin = "java")` 같은 옛 방식으로 적용했다면 accessor가 안 생겨 `configure<Test>("test") { ... }` 같은 fallback을 써야 한다. `plugins { }` 블록을 표준으로 쓰는 이유가 여기서도 작은 편안함으로 돌아온다.

7장에서 이 `tasks.test` 한 블록을 본격적으로 펼친다 — 통합 테스트를 어떻게 별도 suite로 분리하는지. 일단 4장에서는 이 두 줄로 충분하다.

## Maven 개념 매핑 상세

이제 settings와 build를 다 읽었으니, 표 매핑의 큰 항목들을 본문에서 한 번씩 만나본다. 일부는 위에서 이미 본 것이고, 일부는 이 자리에서 새로 만나는 것이다. 짧게 끊어 가자.

### dependencyManagement → platform() BOM

Maven의 `<dependencyManagement>`는 두 가지 일을 했다. 첫째, transitive 의존성의 버전을 정렬한다. 둘째, `<dependencies>`에서 버전 없이 좌표만 적어도 되게 한다. Spring Boot 프로젝트에서 `spring-boot-starter-parent`를 부모로 두면 이 두 일이 자동으로 됐다.

Gradle에서 이 일을 하는 가장 권장되는 방식은 한 줄이다.

```kotlin
dependencies {
    implementation(platform("org.springframework.boot:spring-boot-dependencies:4.0.6"))
    implementation("org.springframework.boot:spring-boot-starter-web")  // 버전 없음
}
```

`platform(...)`은 Gradle 네이티브 BOM 적용 API다. 이 한 줄로 transitive 버전이 BOM 기준으로 정렬되고, 같은 BOM이 다스리는 의존성들은 `dependencies`에서 버전을 생략할 수 있다. 별도 플러그인이 필요 없고, Configuration Cache 친화적이고, IDE 추적이 잘 된다.

지금 `ch04-bootapp/`은 `io.spring.dependency-management` 플러그인 길로 가고 있다. 둘 다 통한다. 다만 9.5 기준의 권장은 `platform()` 길이다. 두 길의 분기 — 언제 어느 쪽을 고르는가 — 는 5장에서 깊게 다룬다.

### parent pom → Convention Plugin

Maven에서 가장 흔한 패턴이 `<parent>`에 회사 표준 pom을 두고, 거기서 모든 회사 표준 — Java 버전, 인코딩, JUnit 버전, Surefire 설정 — 을 상속받는 것이다. 멀티 모듈에서는 각 자식이 또 부모를 상속한다. 우아한 계층이었다.

Gradle에는 `<parent>`가 없다. 대신 **Convention Plugin**이 있다. 발상 자체가 다르다 — 상속이 아니라 **재사용 가능한 빌드 로직의 모듈화**다. `buildSrc/src/main/kotlin/shop.spring-boot-conventions.gradle.kts` 같은 파일에 회사 표준 설정을 한 번 짜두면, 각 모듈의 `build.gradle.kts`에서 `plugins { id("shop.spring-boot-conventions") }` 한 줄로 그걸 다 받는다. parent pom과 표면적 효과는 비슷한데, 동작 모델이 다르다 — 상속이 아니라 plugin 적용이다.

지금 단일 모듈에서는 Convention Plugin이 필요 없다. 8장에서 멀티 모듈로 넘어가고, 10장에서 본격적으로 Convention Plugin을 짠다. 이 장에서는 "parent pom의 자리는 Convention Plugin이다"라는 매핑만 머리에 박아두자. 그 시점이 오면 더 깊게 본다.

### profile → variant + property

Maven `<profile>`은 환경별 설정 분리의 도구였다. `mvn -P dev` / `mvn -P prod`로 활성화하면 `<dependencies>`, `<properties>`, `<plugins>`까지 다르게 적용됐다.

Gradle에는 `<profile>`이라는 통합 메커니즘이 없다. 대신 작은 도구들이 흩어져 있고, 그 조합으로 같은 일을 한다. 두 가지가 핵심이다.

**Project property**. 빌드 명령에 `-P` 옵션으로 키-값을 넘긴다.

```bash
./gradlew bootRun -Penv=dev
```

빌드 스크립트에서는 이렇게 받는다.

```kotlin
val env = (project.findProperty("env") as String?) ?: "local"
```

이 값으로 `dependencies` 블록을 분기하거나, `bootRun`의 인자를 다르게 줄 수 있다. Maven의 `<activeProfile>`보다 자유롭고, 변수 조합이 폭증하지 않는다.

**`bootRun --args`**. Spring Boot 앱을 실행하면서 런타임 인자를 넘기는 표준 방법이다.

```bash
./gradlew bootRun --args='--spring.profiles.active=dev --server.port=8081'
```

Spring Boot 자체의 `spring.profiles.active`는 그대로 살아 있다. Maven에서 자주 `<profile>`로 했던 "환경별 application.yml 선택"은 Spring Boot의 profile이 더 자연스럽게 해준다 — 빌드 도구의 profile이 아니라, **앱의 profile**이다. 빌드 시점이 아니라 실행 시점에 정해진다. 빌드는 한 번, 실행은 환경마다. 이게 더 깔끔한 분리다.

Maven `<profile>`이 했던 일들의 80%는 Spring Boot의 profile + Project property + `bootRun --args` 조합으로 풀린다. 나머지 20%는 12장에서 다루는 커스텀 plugin 패턴까지 가야 풀리는 경우다. 일단 4장에서는 매핑만 기억하자.

### plugin management → settings.gradle.kts

위에서 이미 만난 것이다. Maven `<pluginManagement>`는 Gradle에서 `settings.gradle.kts`의 `pluginManagement { }` 블록이다. 차이가 하나 있다 — Maven은 **부모 pom에 두는 게 관행**이었지만, Gradle은 **settings에 두는 게 표준**이다. 설계상의 위계가 다르다. settings는 "이 빌드의 입구"라는 명확한 책임이 있고, 거기 plugin 버전을 박는 것이 명시적으로 맞다.

### repositories → dependencyResolutionManagement

이것도 위에서 만났다. 다시 짚자면, Maven은 각 pom이 자유롭게 `<repositories>`를 추가할 수 있었고, Gradle 9.5는 **모든 repo는 settings의 `dependencyResolutionManagement { repositories { } }`에 한 번만**이라는 표준을 강제할 수 있다. `RepositoriesMode.FAIL_ON_PROJECT_REPOS` 한 줄이 그 강제 장치다.

처음에는 강제가 답답하게 느껴진다. 어떤 모듈만 임시로 다른 repo를 쓰고 싶을 때가 있지 않은가. 그런데 그게 가능하다는 게 보안팀의 악몽이다. 회사 표준 외의 repo가 우리 빌드에 끼어드는 순간, 의존성의 출처를 신뢰할 수 없게 된다. 16장에서 의존성 보안을 본격적으로 다룰 때, 이 settings 강제가 첫 번째 안전망임이 다시 드러난다.

특수한 경우 — 예를 들어 사내 Nexus가 있고, 그것이 mavenCentral의 mirror라면 — 그건 settings에 같이 박으면 된다. 모듈마다 분기시킬 일이 거의 없다는 게 핵심이다.

### mvn → ./gradlew

가장 표면적인 매핑이자, 가장 깊은 매핑이다.

표면적으로는 한 단어 바꿈이다. `mvn clean install`이 `./gradlew clean build`다. `mvn test`가 `./gradlew test`다. `mvn package`가 `./gradlew assemble` 또는 `./gradlew bootJar`다.

그런데 `./gradlew`의 앞부분 `./`이 의미가 있다. **Maven의 `mvn`은 시스템에 설치된 Maven을 부르는 명령**이다. CI runner와 내 노트북에 깔린 Maven 버전이 다르면, 빌드 결과가 달라질 수 있다. 회사 표준 Maven 버전을 관리하려면 모두에게 같은 버전을 깔게 해야 한다.

**Gradle의 `./gradlew`는 프로젝트 안에 박힌 wrapper를 부르는 명령**이다. 프로젝트 루트의 `gradlew` 셸 스크립트와 `gradle/wrapper/gradle-wrapper.properties`가 짝이 된다. properties에 `distributionUrl=https\://services.gradle.org/distributions/gradle-9.5-bin.zip`이 박혀 있으면, `./gradlew`를 처음 실행할 때 그 버전을 받아 캐시하고, 이후 모든 빌드가 그 버전으로 돈다. 내 노트북에 깔린 Gradle이 어떤 버전이든 상관없다 — 우리 프로젝트의 빌드는 wrapper에 박힌 9.5로 돈다.

이게 단순 편의가 아니다. **wrapper가 곧 우리 빌드의 Gradle 버전 명세다.** 회사 빌드의 Gradle 버전을 올리는 일은 `./gradlew wrapper --gradle-version 9.5.1 --distribution-type=bin` 한 줄과 그것의 git commit이다. 모든 사람이 다음 빌드부터 9.5.1로 돈다. CI runner에 별도 설치를 강제할 필요가 없다. Maven 시절을 떠올리면 이게 작은 평화가 아니다.

> **함정 — phase 모델과 task graph의 차이**
>
> 같은 단어가 다른 의미를 갖는다는 게 가장 찜찜한 일이다. `clean`을 보자.
>
> Maven에서 `mvn clean`은 **phase**다. `clean` phase에 묶인 모든 goal이 순서대로 실행된다. `clean` phase 다음에 `compile`, `test`, `package`, `install`로 이어지는 정해진 lifecycle이 있고, 우리는 그 lifecycle을 따라간다. `mvn clean install`은 "clean phase부터 install phase까지 다 돌려라"는 뜻이다. 순서가 정해져 있다.
>
> Gradle에서 `./gradlew clean`은 **task**다. `clean`은 `java` plugin이 만들어준 task 하나일 뿐이고, 정해진 다음 task가 없다. `./gradlew clean build`라고 쓰면, Gradle은 "clean task와 build task를 둘 다 실행할 그래프를 짜라"고 받아들인다. 두 task의 의존 관계를 보고 순서를 정한다 — `clean`이 `build`보다 먼저 와야 한다는 의존이 없다면, 병렬로 돌릴 수도 있다. (실무에서는 보통 `clean`을 명령행 첫 인자로 쓰면 먼저 도는 게 자연스럽지만, 이건 관행이지 강제가 아니다.)
>
> 차이가 어디서 드러나느냐. 한 번은 이런 일이 있다. Maven에서 `mvn clean test`를 쓰던 사람이 `./gradlew clean test`라고 쓰면 같이 돌 거라 기대한다. Gradle은 두 task의 의존 그래프를 짜는데, `test`는 `compileJava`, `processResources`, `compileTestJava`에 의존하지만 `clean`에는 의존하지 않는다. 그래서 사람이 보기엔 같은 의도였는데 task 그래프가 미묘하게 다른 순서로 평가되는 경우가 생긴다.
>
> 일반적으로는 `./gradlew clean build`처럼 명령 순서로 쓰는 패턴이면 큰 사고가 안 난다. 다만 머릿속의 모델은 이렇게 바꿔두자 — **Maven은 정해진 phase의 행렬, Gradle은 task의 그래프**. 같은 단어를 봐도 다른 메커니즘이 돈다는 걸 기억해두자.

> **마이그레이션 노트 — `gradle init --type pom`의 한계**
>
> Gradle에는 기존 Maven 프로젝트를 Gradle로 변환해주는 명령이 있다. `gradle init --type pom`이다. `pom.xml`이 있는 폴더에서 실행하면 그걸 읽어 `build.gradle.kts`(또는 Groovy)를 생성해준다. 처음 만나면 "이 한 줄로 끝나는가" 싶은데, 사실은 그렇게 단순하지 않다.
>
> 이 명령은 의존성 목록, repository, 기본 plugin은 잘 옮겨준다. 그러나 다음은 잘 못 옮긴다 — `<profile>` 분기, 회사 표준 parent pom의 상속 내용, `<pluginManagement>`의 세부 설정, Spring Boot Maven plugin의 다양한 옵션, Surefire의 디테일한 설정. 한마디로 **거시 골격은 옮겨주지만, 미시 결정들은 옮겨주지 않는다**.
>
> 실용적인 사용법은 이렇다. `gradle init --type pom`을 일단 돌려본다. 산출물을 그대로 쓰겠다는 게 아니라, 우리 `pom.xml`이 Gradle 사고로 어떻게 번역되는지 한 번 보겠다는 것이다. 그 다음에는 그걸 참고용으로 두고, 우리 프로젝트의 `build.gradle.kts`를 새로 짠다. 본 장에서 한 줄씩 읽어본 `ch04-bootapp/build.gradle.kts`처럼 깔끔한 것을 직접 짜는 편이 낫다. 자동 변환에 기대면 옛 Maven 사고가 그대로 Gradle 스크립트에 묻어들어와, 결국 두 번 짤 일이 생긴다.

## 4장을 닫으며

여기까지 왔다면, Maven 출신 독자의 머릿속 어딘가에 작은 안도감이 생겼을 것이다. dependencyManagement는 platform/BOM으로 갔다. parent pom은 Convention Plugin이라는 다른 모델로 옮겨갔다. profile은 흩어져 있지만 그 조각들의 자리는 분명하다. pluginManagement와 repositories는 settings에 모였다. mvn은 ./gradlew다. clean과 test 같은 단어는 같은 단어인데 다른 메커니즘으로 돈다.

그리고 `ch04-bootapp/`에 동작하는 단일 모듈 Spring Boot 앱이 한 채 서 있다. 30줄이 안 되는 `build.gradle.kts`에 Toolchain까지 박혀 있고, 13줄짜리 `settings.gradle.kts`가 입구를 맡고 있다. 이 앱이 5장부터 18장까지 자라난다.

자라남의 첫 걸음이 5장이다. 4장에서는 의존성을 Spring Initializr가 만들어준 그대로 두고 왔다 — `io.spring.dependency-management` 플러그인 길과 BOM의 미묘한 자리를 그대로 두고 왔다. 5장에서 이 자리를 정리한다. **BOM은 resolution을 다스리고, Version Catalog는 declaration을 다스린다. 둘은 직교한다 — 그래서 둘 다 쓴다.** 한 줄로 적으면 짧지만, 그 뒤에 깔린 의존성 그래프의 사고를 자기 것으로 만드는 게 5장의 일이다. `gradle/libs.versions.toml`이라는 단일 출처 파일을 도입하고, `platform(libs.spring.boot.bom)`이라는 한 줄로 Spring Boot의 모든 transitive를 정렬한다. `implementation`과 `api`의 차이를 짚고, `dependencyInsight`로 의존성 그래프를 디버깅하는 도구를 우리 손에 쥔다.

지금 우리 앱은 한 단계 더 자라날 준비가 되어 있다. 다음 장으로 넘어가자.

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

# 6장. Spring Boot Gradle 플러그인의 내부 — bootJar, bootRun, bootBuildImage

`plugins { id("org.springframework.boot") version "4.0.6" }` 한 줄을 친다. Sync가 끝나면 IntelliJ의 Gradle 패널에 `bootJar`, `bootRun`, `bootBuildImage`, `bootTestRun` 같은 task가 줄줄이 새로 떠 있다. 동시에 dependencies 항목에는 `productionRuntimeClasspath`, `developmentOnly`, `testAndDevelopmentOnly`라는 낯선 configuration도 보인다. **이 한 줄이 도대체 무엇을 한 건가.**

`./gradlew bootJar`로 만들어진 jar를 unzip으로 열어보면 더 이상하다. `BOOT-INF/`라는 처음 보는 디렉터리, `layers.idx`라는 텍스트 파일, `org/springframework/boot/loader/`에는 우리가 의존성으로 추가한 적 없는 클래스들이 들어 있다. MANIFEST.MF의 `Main-Class`는 우리가 만든 `ShopApplication`이 아니라 `org.springframework.boot.loader.launch.JarLauncher`로 적혀 있다.

이 모든 게 어떻게 거기에 가 있는가? 그리고 회사 빌드를 Spring Boot 3.x에서 4.0으로 올리려고 plugin 버전 숫자만 바꿨는데 빌드가 깨졌다면, 정확히 어디서 무엇이 바뀐 건가? 6장에서 이 두 질문에 답하자.

미리 한 가지 자리를 분리해두자. **Gradle 9.x 자체로 옮기는 마이그레이션은 17장에서 다룬다.** Daemon JDK가 17+로 강제되는 일, `jcenter()` 제거, Configuration Cache가 preferred mode가 되는 일 같은 Gradle 본체의 변화는 거기 자리다. 6장은 **Spring Boot 플러그인 자체가 3.x → 4.0으로 올라오면서 무엇이 깨지는가**에 집중한다. 둘은 자주 겹쳐서 일어나지만 원인이 다른 변화다.

## 플러그인 한 줄이 일으키는 일

`org.springframework.boot` 플러그인 적용은 그 자체로는 거의 아무 일도 하지 않는다. 정확히는 **다른 플러그인이 적용되기를 기다리는 reaction을 등록**한다. `java` 플러그인이 적용되는 순간(또는 `java-library`, `org.jetbrains.kotlin.jvm`처럼 java를 transitive로 끌어오는 플러그인) 그 reaction이 발화하면서 비로소 task와 configuration이 생긴다.

이 순서를 정확히 짚어두는 게 중요하다. 5장에서 우리는 build.gradle.kts에 이렇게 적었다.

```kotlin
// ch04-bootapp/build.gradle.kts
plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.kotlin.spring)
    alias(libs.plugins.spring.boot)
}
```

`kotlin.jvm`이 `java-base` + `java` 플러그인을 transitive로 적용한다. 그 적용을 본 Spring Boot 플러그인의 reaction이 발화한다. 그 결과로 자동 생성되는 것들이 이렇다.

**Task:**
- `bootJar` — 실행 가능한 fat jar를 만든다 (`BootJar` 타입)
- `bootRun` — 앱을 JVM 모드로 실행한다 (`BootRun` 타입, `JavaExec` 상속)
- `bootBuildImage` — OCI 이미지를 만든다 (`BootBuildImage` 타입)
- `bootTestRun` — test classpath로 앱을 실행한다 (`BootRun` 타입)

**Configuration:**
- `bootArchives` — `bootJar`가 만든 산출물이 들어가는 publication용 configuration
- `developmentOnly` — devtools처럼 dev에서만 쓰는 의존성 자리
- `testAndDevelopmentOnly` — 테스트와 dev 양쪽에서 쓰는 의존성 자리
- `productionRuntimeClasspath` — **runtimeClasspath에서 `developmentOnly`, `testAndDevelopmentOnly`를 뺀 결과**. fat jar가 실제로 포함할 의존성 목록이다.

**Compile 설정 변경:**
- 소스 인코딩 UTF-8 강제
- Java 컴파일에 `-parameters` 자동 추가 (Spring의 파라미터 이름 기반 바인딩이 reflective하게 동작하도록)

5장에서 우리가 박스에서만 본 `productionRuntimeClasspath`가 여기서 본격적으로 등장한다. `developmentOnly(libs.spring.boot.devtools)`로 추가한 devtools가 왜 fat jar에 포함되지 않는가? 그건 `bootJar`가 의존성 묶음을 가져올 때 `runtimeClasspath`가 아니라 **`productionRuntimeClasspath`**를 본다는 약속 때문이다. devtools는 `developmentOnly`에 있고, productionRuntimeClasspath는 그걸 뺀 집합이고, fat jar는 productionRuntimeClasspath만 본다. 이 사슬이 그대로 박혀 있다.

기억해두자. **`developmentOnly`에 넣은 의존성은 IDE의 `bootRun` 실행 시에는 classpath에 있고, `bootJar` 산출물에는 없다.** 이건 의도된 동작이다. devtools가 production 컨테이너에 같이 실려서 자동 reload가 시도되는 사고를 막는다.

## bootJar의 내부 — fat jar는 어떻게 생겼는가

이제 `./gradlew bootJar`로 만든 산출물을 직접 들여다보자. `ch04-bootapp/build/libs/`에 가보면 jar가 두 개 떠 있다.

```
build/libs/
├── ch04-bootapp-0.0.1-SNAPSHOT.jar         # bootJar의 산출물 — 실행 가능 fat jar
└── ch04-bootapp-0.0.1-SNAPSHOT-plain.jar   # jar의 산출물 — 일반 library jar
```

여기가 처음 만나는 사람에겐 좀 헷갈리는 자리다. `assemble`을 부르면 두 개가 다 나온다. **`bootJar` task가 `jar` task를 대체하는 게 아니라, 둘이 공존한다**는 게 핵심이다. 다만 `bootJar`의 산출물에는 classifier가 비어 있고, 일반 `jar`의 산출물에 `-plain`이라는 classifier가 붙는다. 왜 굳이 둘 다 만드는가? `bootJar`로 만든 fat jar는 fat jar로서는 훌륭하지만 **다른 모듈에서 `dependencies { implementation(project(":app")) }`로 끌어쓰는 일에는 부적합**하다. 그래서 일반 jar도 살려둔다. 이 사정은 9장의 library 모듈 함정에서 본격적으로 본다.

`bootJar` 산출물의 내부를 풀어보자.

```bash
unzip -l build/libs/ch04-bootapp-0.0.1-SNAPSHOT.jar
```

```
ch04-bootapp-0.0.1-SNAPSHOT.jar
├── META-INF/
│   └── MANIFEST.MF                       # Start-Class=ShopApplication, Main-Class=JarLauncher
├── BOOT-INF/
│   ├── classes/                          # 우리 앱의 클래스/리소스
│   │   └── com/example/shop/...
│   ├── lib/                              # 의존성 jar들 그대로
│   │   ├── spring-boot-3.5.x.jar
│   │   ├── spring-context-...jar
│   │   └── ...
│   └── classpath.idx                     # 의존성 jar의 정렬된 인덱스
├── BOOT-INF/layers.idx                   # 레이어 인덱스 (기본 ON)
└── org/springframework/boot/loader/      # spring-boot-loader 클래스
    └── launch/JarLauncher.class
```

각 자리가 무엇인지 천천히 짚어보자.

**`META-INF/MANIFEST.MF`** — 평소 만나던 일반 jar와 다른 점이 두 가지다. `Main-Class`가 우리 앱의 메인 클래스가 아니라 `org.springframework.boot.loader.launch.JarLauncher`로 적혀 있다. 그리고 `Start-Class`라는 비표준 attribute에 우리 앱의 메인 클래스(`com.example.shop.ShopApplication`)가 적혀 있다. `java -jar`은 표준대로 `Main-Class`를 부르고, 그게 `JarLauncher`다. `JarLauncher`가 jar 안의 `BOOT-INF/lib/`에 있는 의존성들을 자신의 ClassLoader에 추가한 뒤 `Start-Class`로 위임한다. **이게 fat jar가 표준 `java -jar`로 실행되는 비결이다.** jar-in-jar를 직접 풀지 않고도, ClassLoader 레벨에서 nested jar를 그대로 읽는다.

**`BOOT-INF/classes/`** — 우리 앱의 컴파일된 `.class` 파일과 `src/main/resources/`의 리소스가 그대로 들어간다. 평소의 jar 루트에 들어가던 게 한 단계 들어간 자리에 들어간 것뿐이다.

**`BOOT-INF/lib/`** — `productionRuntimeClasspath`로 풀린 의존성 jar들이 **풀리지 않은 채로** 그대로 들어간다. Maven의 shade plugin이나 Gradle의 `Jar` task로 만든 "uber jar"와 결정적으로 다른 자리다. uber jar는 의존성을 풀어서 한 디렉터리에 섞어버리지만, Spring Boot의 fat jar는 의존성 jar를 jar 안에 통째로 보관한다. 그 결과 **클래스 시그니처 충돌이나 META-INF 충돌이 안 일어난다.** 두 의존성에 같은 경로의 리소스가 있어도, 각각 자기 jar 안에 사는 채로 격리되기 때문이다.

**`BOOT-INF/classpath.idx`** — `lib/` 아래 jar들의 적용 순서를 명시한 텍스트 파일. ClassLoader가 의존성 jar를 탐색할 순서를 빌드 시점에 미리 결정해서 적어둔다.

**`BOOT-INF/layers.idx`** — 4.0에서도 기본 ON인 레이어 인덱스다. 다음 절에서 본격적으로 들여다본다.

**`org/springframework/boot/loader/`** — `spring-boot-loader` 모듈의 클래스가 fat jar 루트에 unpack된 상태로 박혀 있다. 우리가 `dependencies`에 추가한 적 없는데도 들어 있는 이유는, `JarLauncher` 자체가 `BOOT-INF/lib/` 안에 있으면 부트스트랩이 불가능하기 때문이다. 표준 `java -jar`이 처음 부르는 클래스는 jar 루트의 표준 위치에 있어야 한다. 그래서 이 클래스들만은 풀려서 jar 루트에 박힌다.

## 메인 클래스 자동 탐지와 명시

`bootJar`가 MANIFEST.MF의 `Start-Class`에 무엇을 적을지는 어떻게 결정되는가? 기본 동작은 **자동 탐지**다. main 소스셋의 모든 클래스를 훑어 `public static void main(String[])` 시그니처를 가진 클래스를 찾는다. 후보가 정확히 하나면 그걸 쓴다. 두 개 이상이면 빌드가 명확한 에러로 멈춘다.

자동 탐지는 편하지만 한 가지 위험을 동반한다. **메인 후보가 여럿일 때 자동 탐지가 다른 후보를 골라버리는 사고**다. 회사 빌드에서 `main()`을 가진 유틸리티 클래스 하나가 어쩌다 추가되면 빌드가 갑자기 그쪽을 골라 산출물이 엉뚱한 클래스를 부팅한다. 이 위험을 피하려면 명시하는 편이 낫다.

```kotlin
import org.springframework.boot.gradle.tasks.bundling.BootJar

tasks.named<BootJar>("bootJar") {
    mainClass = "com.example.shop.ShopApplication"
}
```

`bootJar`와 `bootRun` 양쪽이 보는 `mainClass`는 사실 `springBoot` extension에 한 번만 명시하면 두 task가 함께 본다.

```kotlin
springBoot {
    mainClass = "com.example.shop.ShopApplication"
}
```

production 빌드는 이 쪽을 권한다. 자동 탐지는 신규 프로토타입 단계에서는 충분히 편리하지만, 회사 코드베이스에 정착할 무렵엔 명시로 옮겨두는 편이 사고를 줄인다.

## 레이어드 JAR — OCI 이미지 캐시의 토대

`BOOT-INF/layers.idx`를 풀어서 열어보면 이런 내용이다.

```
- "dependencies":
  - "BOOT-INF/lib/spring-boot-3.5.x.jar"
  - "BOOT-INF/lib/spring-context-...jar"
  ...
- "spring-boot-loader":
  - "org/"
- "snapshot-dependencies":
- "application":
  - "BOOT-INF/classes/"
  - "BOOT-INF/classpath.idx"
  - "BOOT-INF/layers.idx"
  - "META-INF/"
```

이 파일이 무엇을 하는가? 단독으로는 거의 아무 것도 안 한다. **OCI 이미지를 만들 때 도커 레이어가 fat jar의 어떤 부분으로 갈라져야 하는지를 미리 적어둔 색인**일 뿐이다. 핵심은 그 분리의 의도다.

- `dependencies` — 우리가 잘 안 바꾸는, BOM이 정한 외부 라이브러리들. 가장 안 변한다.
- `spring-boot-loader` — Spring Boot 자체. plugin 버전이 안 바뀌면 안 변한다.
- `snapshot-dependencies` — `-SNAPSHOT` 의존성 자리. 사내 라이브러리 등이 여기 모인다.
- `application` — 우리 앱 코드. **가장 자주 변한다.**

위에서 아래로 갈수록 변화 빈도가 높다. OCI 이미지의 각 레이어는 hash로 식별되고, 변하지 않은 레이어는 다음 빌드의 cache hit으로 그대로 재사용된다. 코드 한 줄만 고친 빌드의 결과로 만들어지는 이미지에서 95% 이상의 바이트는 캐시에서 재사용되고, 새로 push해야 하는 건 application 레이어 몇 메가뿐이라는 시나리오가 여기서 나온다. **`layers.idx`는 이 캐시 성능의 토대 데이터다.**

기본값으로 충분한 경우가 많아서 다음과 같이 명시적으로 한 번만 박아두면 된다.

```kotlin
tasks.named<BootJar>("bootJar") {
    layered {
        enabled = true
    }
}
```

레이어 정의 자체를 회사 정책에 맞춰 더 세분하고 싶다면 `layered.layerConfiguration`을 다듬는 길이 있지만, 그 자리는 9장 이후의 멀티 모듈 빌드에서 다시 본다. 단일 모듈에서는 기본값 그대로가 안전하다.

## bootRun — JavaExec 그 자체

`bootRun`은 의외로 단순한 task다. `org.springframework.boot.gradle.tasks.run.BootRun`은 **`JavaExec`을 상속**한다. 그 말은 `JavaExec`에 있는 모든 옵션이 그대로 통한다는 뜻이다.

```kotlin
import org.springframework.boot.gradle.tasks.run.BootRun

tasks.named<BootRun>("bootRun") {
    jvmArgs("-Dspring.profiles.active=local")
    systemProperty("debug", "true")
    sourceResources(sourceSets["main"])  // src/main/resources를 그대로 본다 → 라이브 리로드
}
```

`sourceResources(sourceSets["main"])` 한 줄이 익숙해질 만한 자리다. 기본 동작은 `bootRun`이 `build/resources/main/`(컴파일 결과 폴더)를 본다. 그래서 정적 리소스(예: `templates/*.html`)를 고쳐도 즉시 반영되지 않고 다시 빌드돼야 한다. `sourceResources()`로 `src/main/resources/`를 직접 가리키게 하면 파일 수정이 IDE에서 즉시 보인다. devtools 없이도 정적 리소스에 한해 라이브 reload가 동작하는 비결이다.

런타임 인자를 넘기는 것도 깔끔하다.

```bash
./gradlew bootRun --args='--spring.profiles.active=dev --server.port=9090'
```

`--args`는 Spring Boot의 `SpringApplication.run(args)`이 받는 그 `args`다. JVM 옵션이 아니라 **앱 자체의 인자**다. 이 둘을 헷갈리지 말자. JVM 옵션은 `-D...`로 시작하고 `jvmArgs`로 설정하거나 `bootRun.jvmArguments` property에 넣는다. 앱 인자는 `--server.port=9090`처럼 Spring 컨벤션을 따르고 `--args`로 넘긴다.

`bootTestRun`도 함께 챙겨두자. 이건 `bootRun`과 거의 똑같지만 classpath가 다르다. **test sourceSet의 classpath로 앱을 실행한다.** 통합 테스트용 설정(예: testcontainers, 인메모리 설정)을 main 코드에 흘리지 않고 별도 fixture로 두면서, 그 fixture 그대로 부팅한 앱을 손으로 확인하고 싶을 때 쓴다. 7장에서 JVM Test Suite로 들어가면 이 task의 자리가 더 또렷해진다.

## bootBuildImage — Dockerfile 없는 OCI 이미지

`bootBuildImage`는 6장에서 가장 마법처럼 보이는 자리다. **Dockerfile을 한 줄도 안 쓰고**, 로컬 Docker daemon에 OCI 이미지가 한 방에 박힌다.

```bash
./gradlew bootBuildImage
```

이 한 줄 안쪽에서 무슨 일이 일어나는가?

`bootBuildImage`는 **Paketo Buildpacks**를 호출한다. Paketo는 Cloud Native Buildpacks (CNB) 사양을 따르는 빌드팩 모음이다. 핵심 idea는 이렇다 — 우리 앱의 산출물(jar)과 메타데이터를 보면 어떤 builder image를 깔고 어떤 launcher를 박을지가 결정된다. 그 결정을 도구가 한다. 우리는 산출물만 제공하고 builder 이미지가 알아서 운영체제 layer, JRE layer, 의존성 layer, 앱 코드 layer를 쌓아 최종 이미지를 만든다.

기본 builder는 Spring Boot 4.0 기준 **`paketobuildpacks/builder-noble-java-tiny:latest`**다. Ubuntu Noble Numbat 기반의 최소 이미지에 buildpack 도구만 박힌 빌더다. (Spring Boot 3.x에서는 기본 builder가 `paketobuildpacks/builder-jammy-tiny` 또는 `builder-jammy-base`였다. 회사 빌드를 4.0으로 올리면서 이미지가 갑자기 커지거나 작아진 걸 보게 된다면, 이 기본값 변화가 원인일 가능성이 높다.)

설정은 이렇게 한다.

```kotlin
import org.springframework.boot.gradle.tasks.bundling.BootBuildImage

tasks.named<BootBuildImage>("bootBuildImage") {
    imageName = "ghcr.io/example/shop:${project.version}"
    environment.put("BP_JVM_VERSION", "21")
    publish = true
    docker {
        publishRegistry {
            username = providers.environmentVariable("GHCR_USER").get()
            password = providers.environmentVariable("GHCR_TOKEN").get()
        }
    }
}
```

`imageName`은 결과 이미지의 태그다. `${project.version}`이 그대로 박힌다. `environment`는 buildpack이 보는 환경변수다. `BP_JVM_VERSION=21`은 Paketo Java buildpack에게 JRE 21을 깔라고 알려준다.

`publish = true`로 두면 빌드가 끝나자마자 레지스트리로 push까지 진행된다. **로컬에 이미지를 만들고 별도로 `docker push`를 부르는 단계가 없다.** 이게 CI 파이프라인에서 가장 빛난다. `./gradlew bootBuildImage` 한 줄이 ghcr.io에 이미지를 올린 결과까지를 만들어낸다. 자격증명을 `providers.environmentVariable(...)`로 받는 패턴도 짚어두자. 직접 `System.getenv("...")`로 받으면 Configuration Cache에서 위반이 잡힌다. Provider API로 받는 게 안전한 길이다. 13장에서 본격적으로 본다.

이미지의 캐시 동작이 인상적이다. 코드 한 줄만 바꾸고 다시 `./gradlew bootBuildImage`를 부르면 빌드 시간이 첫 빌드의 1/10 이하다. buildpack이 layered jar의 레이어 구분을 OCI 레이어로 그대로 매핑하기 때문이다. application 레이어만 갈리고 나머지는 다 캐시에서 재사용된다. 앞 절에서 본 `layers.idx`의 의도가 여기서 결실을 본다.

GraalVM Native Image 플러그인을 함께 적용하면 `bootBuildImage`가 **자동으로 native 이미지를 빌드**한다. JVM 이미지 대신 그 자리에 native binary가 박힌 이미지가 만들어진다. 자세한 자리는 15장이다.

## bootJar와 jar의 공존 — 어느 쪽을 발행하는가

다시 `build/libs/`로 돌아가자. jar가 두 개다. `bootJar`의 산출물(classifier 비어 있음)과 `jar`의 산출물(classifier=`plain`). `assemble`은 둘 다 만든다.

이게 의도된 모양인가? 그렇다. 두 산출물의 쓰임새가 다르다. **`bootJar`의 fat jar는 실행용, `jar`의 일반 library jar는 다른 모듈에서 import해서 쓰는 용도다.** 같은 모듈을 동시에 둘 다로 쓰는 일은 단일 모듈에서는 흔하지 않다. 하지만 이 약속이 박혀 있어야 9장의 멀티 모듈에서 library 모듈의 사고를 깔끔하게 풀 수 있다.

회사 빌드에 따라 `-plain.jar`이 거추장스럽게 느껴진다면, 명시적으로 끌 수 있다.

```kotlin
tasks.named<Jar>("jar") {
    enabled = false
}
```

단일 모듈 앱이고 jar publication을 따로 안 한다면 이 한 줄로 깔끔해진다. 다만 library 모듈로 누군가 import할 일이 있다면 **반드시 살려두자.** 끄는 쪽은 명시적 선택이어야 한다.

## Spring Boot 3.x → 4.x — 무엇이 깨지는가

이제 6장의 또 다른 약속을 풀 차례다. 회사 빌드가 Spring Boot 3.5.x에서 잘 굴러가고 있다고 해보자. 어느 날 4.0.6으로 plugin 버전 숫자만 바꿔보자.

```kotlin
plugins {
    id("org.springframework.boot") version "4.0.6"  // 3.5.6 → 4.0.6
}
```

높은 확률로 빌드가 한두 곳에서 멈춘다. 어디서 무엇이 깨지는가를 미리 알아두면 1시간이 5분으로 줄어든다.

### Gradle 8.14+ 또는 9.x 요구

Spring Boot 4.0은 **Gradle 8.14+ 또는 9.x**를 요구한다. 3.x는 Gradle 7.x도 받아줬지만 4.x는 그 자리를 닫았다. 회사 빌드의 `gradle/wrapper/gradle-wrapper.properties`가 7.6.4면 4.0 plugin은 적용 단계에서 명확한 에러를 던지며 멈춘다.

```bash
./gradlew wrapper --gradle-version 9.5 --distribution-type=bin
```

`--distribution-type=bin`을 빠뜨리지 말자. 기본값인 `all`은 200MB 넘는 소스 포함 배포본이라 CI를 무겁게 만든다. 이 명령을 두 번 부르고(wrapper task 자체가 wrapper 파일 자체를 새로 쓰기 위해 두 번 실행이 권장된다) 커밋하면 끝이다. **Gradle 본체로의 마이그레이션 자체는 17장에서 본격적으로 본다.** 여기서는 Spring Boot 4.0이 그걸 요구한다는 사실만 박아두자.

### Task 시그니처 — lazy property `=` 권장 강화

3.x 시절 우리는 이런 코드를 종종 봤다.

```kotlin
// 3.x 시절 흔한 모양 — 4.x에서도 동작은 하지만 권장 모양은 아님
tasks.named<BootJar>("bootJar") {
    mainClass.set("com.example.shop.ShopApplication")
    archiveClassifier.set("boot")
}
```

`Property<T>`에 `.set(value)`로 값을 넣는 모양이다. 4.x에서는 이 모양이 비권장은 아니지만, Kotlin DSL의 `=` 연산자 오버로딩이 lazy property에도 충분히 잘 동작하게 정리되면서 다음 쪽이 표준이 됐다.

```kotlin
// 4.x 권장 — = 연산자가 lazy property에 자연스럽게 동작
tasks.named<BootJar>("bootJar") {
    mainClass = "com.example.shop.ShopApplication"
    archiveClassifier = "boot"
}
```

`.set()`을 부르던 코드가 동작을 멈추지는 않는다. 다만 **새로 쓰는 코드는 `=`로 쓰는 편이 낫다.** 3장에서 본 Kotlin DSL의 `=`와 lazy property의 사이가 4.x에 와서 한 번 더 정돈됐다. 회사 빌드에서 옛 코드를 발견하면 같은 PR에서 정리하는 쪽이 깔끔하다.

### `bootBuildImage` 기본 builder 변화

앞 절에서 짚었듯 기본 builder가 `paketobuildpacks/builder-jammy-tiny`(또는 `jammy-base`)에서 **`paketobuildpacks/builder-noble-java-tiny:latest`**로 바뀌었다. Ubuntu Jammy(22.04)에서 Noble(24.04)로 베이스가 한 발 올라간 셈이다.

회사가 보안 이유로 builder image를 고정하고 있다면 명시적으로 적어두자.

```kotlin
tasks.named<BootBuildImage>("bootBuildImage") {
    builder = "paketobuildpacks/builder-jammy-tiny:0.0.146"
}
```

기본값에 의존하면 plugin 업그레이드가 silent하게 base OS를 바꾼다. 운영 환경에서 이걸 발견하는 자리가 prod 인시던트라면 늦다. **builder는 명시해두는 편이 안전하다.**

### AOT 동작 변경

`spring-boot-aot` 처리(AOT 빌드 시점에 미리 reflection 메타데이터 등을 생성하는 자리)가 4.x에서 한 번 정돈됐다. 가장 눈에 띄는 자리는 **AOT processing이 `bootRun`에서도 발화하는 옵션이 다듬어진 점**이다. 이 영향이 가장 자주 나타나는 자리는 native 빌드와 함께 쓸 때다. 단일 모듈 JVM 빌드에서는 거의 보이지 않지만, 15장에서 native로 넘어갈 때 다시 만난다.

### Native 통합 변경

`org.graalvm.buildtools.native` 플러그인의 기본 좌표·동작이 4.x와 함께 한 차례 정돈됐다. 회사 빌드에 native 이미지가 들어 있다면 plugin 버전을 함께 올리는 쪽이 안전하다. 자세한 자리는 15장.

### Configuration Cache가 디폴트에 더 가까워졌다

4.0의 plugin은 **Configuration Cache를 완전 지원**한다. 3.x도 대체로 지원했지만 일부 task에 미세한 위반이 남아 있었다. 4.0에 와서 그 미세한 자리들이 정리됐다. 회사 빌드에서 Configuration Cache를 켜두지 않았다면, 4.x로 옮긴 김에 함께 켜보는 편이 낫다. 13장에서 본격적으로 다룬다.

> **박스 — 3.5.x 유지보수 라인 독자용 분기 가이드**
>
> 모두가 당장 4.0으로 올라가는 건 아니다. 회사 정책상 3.5.x를 한참 더 굴려야 한다면 다음을 기억하자.
>
> 1) **3.5.x는 OSS 지원 종료가 2026년 6월로 예정**되어 있다 (Spring Boot의 정규 12개월 OSS support 기준). 그 이후엔 commercial support가 필요해진다.
> 2) **3.5.x → 4.x로 옮길 때 가장 큰 일은 Gradle wrapper 버전**이다. 3.5.x는 Gradle 7.x도 받아주지만 4.x는 안 받는다. wrapper를 9.x로 올리는 작업을 4.0 전환과 별개의 PR로 먼저 처리해두면 PR 하나에 변수 두 개가 섞이지 않는다.
> 3) **builder image는 지금 시점에 명시해두자.** 3.x 시절의 `jammy` 베이스를 명시적으로 박아두면, 추후 4.0 업그레이드 시점에 그 한 줄이 OS layer 변화의 위험을 명시적으로 노출시켜준다.
> 4) **Java 21 toolchain은 미리 옮겨두자.** 3.5.x도 Java 21을 받는다. 4.x로 옮길 때 Java 버전 변화까지 한꺼번에 일어나는 게 가장 사고 위험이 높다.
>
> 4.x로 올라갈 단계가 됐을 때 위 네 가지가 미리 처리돼 있으면, plugin 좌표 한 줄 바꾸는 PR로 전환이 마무리된다.

## 6장에서 자란 빌드와 그 다음

이제 `ch04-bootapp/`의 상태를 한 번 점검하자. 5장 끝에서는 BOM과 Catalog가 자리를 잡은 build script까지였다. 6장에서는 그 위에 다음이 박혔다.

- `./gradlew bootJar`이 `build/libs/ch04-bootapp-0.0.1-SNAPSHOT.jar`를 만든다. `java -jar` 한 줄로 실행되는 fat jar다.
- `./gradlew bootRun`이 IDE를 거치지 않고 앱을 부팅한다. `--args`로 런타임 인자를 받는다.
- `./gradlew bootBuildImage`가 OCI 이미지를 만든다. Dockerfile 없이.
- main class는 자동 탐지에 의존하지 않고 `springBoot { mainClass = "..." }`로 명시했다.
- layered jar는 기본 ON 그대로 두고, 그게 OCI 이미지 캐시의 토대라는 점을 기억해뒀다.

> **박스 — 6장의 마이그레이션 노트 모음**
>
> 회사 빌드에서 이 챕터의 자리들을 옛 모양에서 4.x 표준으로 옮길 때 한꺼번에 보는 자리.
>
> ```kotlin
> // 옛 모양 (3.x 시절 흔히 보던 코드)
> tasks.named<BootJar>("bootJar") {
>     mainClass.set("com.example.shop.ShopApplication")
>     archiveClassifier.set("boot")
> }
>
> // 4.x 권장
> tasks.named<BootJar>("bootJar") {
>     mainClass = "com.example.shop.ShopApplication"
>     archiveClassifier = "boot"
> }
>
> // 더 권장 — extension에 한 번만
> springBoot {
>     mainClass = "com.example.shop.ShopApplication"
> }
> ```
>
> ```kotlin
> // 옛 모양 — Configuration Cache에 친화적이지 않다
> tasks.named<BootBuildImage>("bootBuildImage") {
>     docker {
>         publishRegistry {
>             username = System.getenv("GHCR_USER")
>             password = System.getenv("GHCR_TOKEN")
>         }
>     }
> }
>
> // 4.x 권장 — Provider API로 받는다
> tasks.named<BootBuildImage>("bootBuildImage") {
>     docker {
>         publishRegistry {
>             username = providers.environmentVariable("GHCR_USER").get()
>             password = providers.environmentVariable("GHCR_TOKEN").get()
>         }
>     }
> }
> ```
>
> ```kotlin
> // 옛 모양 — eager 패턴, 9.x에서 deprecation 경고
> tasks {
>     "bootJar"(BootJar::class) {
>         mainClass = "..."
>     }
> }
>
> // 4.x 권장 — lazy
> tasks.named<BootJar>("bootJar") {
>     mainClass = "..."
> }
> ```

남은 매듭이 한두 가지 있다. 우선 우리 빌드의 **테스트가 아직 단순하다.** `test` task 하나에 단위 테스트와 (앞으로 추가될) 통합 테스트가 한꺼번에 들어간다. Spring 앱의 통합 테스트는 컨텍스트 부팅이 들어가서 느리다. 그걸 단위 테스트와 같은 task에서 한꺼번에 돌리면 빠른 피드백을 잃는다. 7장에서 `jvm-test-suite` 플러그인으로 `integrationTest` suite를 별도로 만들고, `check`가 둘을 모두 부르게 정리한다.

그리고 회사 빌드가 이쯤에서 자라기 시작하면, 모듈을 한 번 쪼개고 싶어진다. 도메인을 별도 library 모듈로 빼고, 앱은 그 모듈에 의존하는 모양으로. 그 단계에서 만나는 가장 흔한 사고가 **"library 모듈에서 만든 jar가 비어 보이는"** 일이다. 9장에서 이 사고를 진단하고 막는 자리를 만든다. 6장에서 본 `bootJar`와 `jar`의 공존, `productionRuntimeClasspath`의 의미가 그 자리의 해독 도구로 다시 등장한다.

다음 챕터로 넘어가자. 테스트의 분리부터다.

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

---

# Part III — 규모를 키운다

단일 모듈로는 곧 답답해진다. 도메인이 커지면 한 모듈이 갑갑해진다. `app`, `domain`, `order`, `payment` 같이 책임을 쪼개고 싶어진다. 그런데 모듈을 쪼개는 일이 단순히 `settings.gradle.kts`에 `include(":domain")` 한 줄 더하는 일로 끝나지 않는다는 사실을 우리는 곧 알게 된다. Spring Boot Gradle 플러그인이 library 모듈에 들러붙어서 빈 fat jar를 만들어내는 사고가 기다리고, 4개 모듈의 build.gradle.kts가 거의 똑같이 중복되는 찜찜함이 따라오고, `buildSrc/`로 정리해 둔 build logic이 손바닥만 한 변경에도 빌드 전체를 out-of-date로 만드는 답답함이 누적된다.

Part III의 네 챕터는 빌드의 사회적 측면을 다룬다 — 한 사람이 한 모듈을 책임지던 빌드를, 여러 모듈이 협력하고 여러 사람이 함께 만지는 빌드로 옮기는 과정이다. 8장에서 모듈을 쪼개고 그 끝에서 정상 빌드가 안 되는 사고에 부딪힌다. 9장은 책 전체의 클라이맥스 중 하나다 — `bootJar` 함정을 5분 진단 체크리스트로 풀고, library 모듈에는 Spring Boot 플러그인을 적용하지 않는 정석을 손에 쥔다. 10장에서 4개 모듈의 중복을 Convention Plugin으로 한 줄짜리 plugin 선언까지 줄이고, 11장에서 `buildSrc/`의 그림자를 `build-logic` included build로 넘는다.

Part III이 끝나는 자리에서 우리의 `ch11-composite/`는 멀티 모듈 + Convention Plugin + included build의 토대 위에 정렬돼 있다. 회사 빌드가 이 세 도구 위에 정렬돼 있다면 여러 명이 한 빌드를 만져도 마찰이 작다. 그게 Part III이 약속한 자리다.

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

# 9장. bootJar 함정 — library 모듈에서 빈 jar가 나오는 사고를 어떻게 진단하고 어떻게 막는가

8장 마지막에 손에 쥔 그 출력 로그를 그대로 책상 위에 펼쳐보자. `shop` 앱을 `app + domain + order + payment` 네 모듈로 갈라놓고, 각 모듈에 똑같이 `org.springframework.boot` 플러그인과 `java`를 올렸다. 의존성도 깔끔하게 정리했다. `app`이 `domain`에 의존하고, `order`와 `payment`가 `domain`을 끌어다 쓰고, settings에서 네 모듈을 `include`로 묶었다. 빌드를 한 번 돌려본다.

```
$ ./gradlew :app:bootRun

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
2 errors

FAILURE: Build failed with an exception.

* What went wrong:
Execution failed for task ':order:compileJava'.
> Compilation failed; see the compiler error output for details.
```

찜찜한 일이다. `domain` 모듈에 분명히 `Order` 클래스가 있다. `:domain:compileJava`도 성공했고 `:domain:classes`도 성공했다. 그런데 그 다음 줄에서 `order` 모듈의 컴파일러는 "`com.shop.domain` 패키지가 없다"고 외친다. 단순한 의존성 누락이 아니다 — 우리는 분명히 `implementation(project(":domain"))`을 박아뒀다.

빌드 로그를 한 줄씩 따라가다 보면 두 개의 의심스러운 표지가 보인다. `> Task :domain:bootJar` — 어, `bootJar`? `domain`은 라이브러리 모듈이지 실행 가능한 앱이 아닌데 왜 `bootJar` task가 돌았지? 그리고 그 바로 다음 줄, `> Task :domain:jar SKIPPED` — 일반 `jar`는 왜 SKIPPED인가? 5장에서 분명히 `bootJar`와 `jar`는 공존하고 `assemble`이 둘 다를 굽는다고 했는데, 그 약속이 어디로 갔는가.

미스터리가 두 갈래다. 첫째, `domain`의 일반 `jar`는 왜 SKIPPED인가? 둘째, 그렇다면 `domain`의 컴파일된 클래스들은 지금 어디로 갔는가? `bootJar`에는 들어갔는데 일반 `jar`는 안 만들어졌으니, `order`가 `implementation(project(":domain"))`으로 끌어올 때 보는 그 산출물은 도대체 어떤 모양인가?

이 두 갈래를 풀면 `package com.shop.domain does not exist`의 정체가 한꺼번에 잡힌다. 진단부터 시작하자.

## 5분 진단 체크리스트

같은 사고를 처음 만난 사람이 가장 먼저 하는 일은 `dependencies` task를 돌려보는 일이다. 정말로 `app`이 `domain`을 끌어가고 있는가부터 확인해야 한다.

```bash
$ ./gradlew :app:dependencies --configuration runtimeClasspath

runtimeClasspath - Runtime classpath of source set 'main'.
+--- project :domain
+--- org.springframework.boot:spring-boot-starter-web -> 4.0.6
|    +--- ...
\--- project :order
     \--- project :domain (*)
```

의존성 그래프상으로는 멀쩡하다. `project :domain`이 정확히 자리잡고 있다. 그러면 다음 단계는 `domain`이 만들어내는 jar 자체를 들여다보는 거다. 빌드 산출물의 내용물을 열어보자.

```bash
$ ./gradlew :domain:build
$ ls domain/build/libs/
domain-0.0.1-SNAPSHOT-plain.jar
domain-0.0.1-SNAPSHOT.jar

$ unzip -l domain/build/libs/domain-0.0.1-SNAPSHOT.jar
Archive:  domain/build/libs/domain-0.0.1-SNAPSHOT.jar
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  2026-05-11 14:22   META-INF/
       25  2026-05-11 14:22   META-INF/MANIFEST.MF
        0  2026-05-11 14:22   BOOT-INF/
        0  2026-05-11 14:22   BOOT-INF/classes/
        0  2026-05-11 14:22   BOOT-INF/lib/
...
```

여기서 멈칫하게 된다. `domain-0.0.1-SNAPSHOT.jar` 안에 `BOOT-INF/`가 들어 있다. 그런데 `BOOT-INF/classes/`는 비어 있다. 분명히 `Order.class`가 안에 박혀 있어야 할 자리인데, 아무것도 없다. 옆에 `domain-0.0.1-SNAPSHOT-plain.jar`라는 못 보던 파일이 하나 더 떨궈져 있다. 그쪽을 열어보면 거기에 클래스 파일들이 들어 있다.

> **박스 — 5분 진단 체크리스트**
>
> 멀티 모듈 Spring Boot 빌드에서 `ClassNotFoundException`이나 빈 jar 의심이 들면, 5분 안에 이 네 가지를 차례로 확인해보자. 같은 사고를 처음 만난 사람이 헤매지 않게 하는 최소 체크리스트다.
>
> 1. **의존성 그래프부터 본다.**
>    `./gradlew :<consumer>:dependencies --configuration runtimeClasspath`로 의심되는 모듈이 실제로 classpath에 올라타는지 확인. 여기서 빠져 있으면 `project()` 의존성을 안 박은 것이다.
> 2. **library 모듈의 빌드 산출물 목록을 본다.**
>    `ls <library>/build/libs/` 결과에 `*-plain.jar`가 같이 있다면 이미 99% 진범이 잡힌 셈이다 — Spring Boot 플러그인이 library 모듈에 들러붙어 있다는 뜻이다.
> 3. **jar 안을 들여다본다.**
>    `unzip -l <library>/build/libs/<lib>-*.jar`로 안에 뭐가 들었는지 확인. `BOOT-INF/`만 있고 클래스가 없으면 빈 fat jar다. `META-INF/MANIFEST.MF`만 들어 있는 archive면 빈 jar.
> 4. **MANIFEST의 main 좌표를 본다.**
>    `unzip -p <library>/build/libs/<lib>-*.jar META-INF/MANIFEST.MF`. library 모듈인데도 `Main-Class: org.springframework.boot.loader.launch.JarLauncher`가 박혀 있으면, 그 모듈에 Spring Boot 플러그인이 잘못 적용된 거다.
>
> 이 네 줄로 거의 모든 멀티 모듈 bootJar 사고를 5분 안에 진단할 수 있다. 기억해두자 — `*-plain.jar`가 옆에 떨어졌다면 그게 곧 답이다.

## 무엇이 잘못된 건가 — bootJar가 jar를 갈아 끼우는 메커니즘

진단까지는 했다. 그렇다면 정확히 무엇이 잘못된 걸까. 왜 단일 모듈에서는 멀쩡히 잘 돌아가던 게, 멀티 모듈로 가면 이렇게 모듈 간 의존성을 깨뜨리는가.

답은 `org.springframework.boot` 플러그인의 작동 방식에 있다. 6장에서 우리는 Spring Boot 플러그인이 `java` 플러그인에 반응해서 자동으로 만들어내는 task와 configuration을 살펴봤다. `bootJar`, `bootRun`, `bootBuildImage`, `bootArchives` 같은 것들이다. 그때는 단일 모듈 앱 이야기였으니까, 이게 다 우리한테 좋은 일이었다. 그런데 멀티 모듈로 옮겨오면 한 가지 동작이 우리를 정면으로 친다.

**Spring Boot 플러그인이 적용된 모듈에서는 기본 `jar` task의 동작이 바뀐다.** 정확하게는, 표준 `jar` task가 만들어내는 산출물에 classifier가 `plain`으로 붙고, classifier 없는 메인 좌표(`domain-0.0.1-SNAPSHOT.jar`)는 `bootJar` task의 산출물 — 실행 가능한 fat jar — 로 교체된다. 6장에서 봤듯 fat jar의 클래스는 루트가 아니라 `BOOT-INF/classes/` 안에 들어가 있다.

여기까지가 사고의 메커니즘이다. 천천히 따라가보자.

1. `domain` 모듈에 `org.springframework.boot` 플러그인을 적용한다.
2. 플러그인은 `bootJar` task를 등록하고, 기본 `jar`의 classifier를 `plain`으로 밀어낸다.
3. `domain` 빌드의 결과로 두 개의 jar가 떨궈진다 — `domain-0.0.1-SNAPSHOT.jar`(fat jar 형식)와 `domain-0.0.1-SNAPSHOT-plain.jar`(진짜 클래스가 든 일반 jar).
4. 그런데 `domain`은 library 모듈이라 main class가 없다. main 메서드가 있는 클래스가 없으니, `bootJar`가 만들어내는 fat jar는 그냥 **껍데기**다. `BOOT-INF/classes/`도 비어 있고 `BOOT-INF/lib/`에 의존성만 잔뜩 묶여 있는 일종의 식별 가능한 빈 archive.
5. `app`이 `project(":domain")`을 통해 끌어가는 건 `domain`의 기본 좌표 — 즉, classifier 없는 그 fat jar다. 이건 `bootArchives` configuration을 통해 다른 모듈에 노출된다.
6. `app`이 그걸 풀어서 classpath에 올리면, 거기엔 `Order.class`가 없다. classpath에서 그 클래스를 못 찾는다. `ClassNotFoundException`이 던져진다.

이게 끝이다. 사고의 전 과정이 이 여섯 줄로 정리된다. **Spring Boot 플러그인은 "이 모듈은 실행 가능한 앱이다"라는 가정 위에 동작한다.** library 모듈에 그걸 적용하면 그 가정이 깨지고, 결과물이 우리가 기대한 library jar가 아닌 텅 빈 fat jar로 바뀐다.

처음 이 사고를 만난 사람은 보통 직감으로 모든 모듈에 같은 플러그인을 적용해버린다. Maven 시절의 parent pom 감각으로 빌드 환경을 모듈마다 동일하게 맞춰주려는 본능이다. 같은 BOM, 같은 자바 버전, 같은 컴파일 옵션 — 그러니 같은 플러그인. 그 논리는 자연스럽다. 하지만 Gradle 세계에서, 특히 Spring Boot Gradle 플러그인 같이 "application을 패키징한다"는 자기 정체성이 강한 플러그인을 그대로 library에 들이미는 건 함정이다. **공통 빌드 환경을 맞추는 일과, application 패키징 플러그인을 적용하는 일은 다른 일이다.** 이 둘이 같은 일처럼 보이는 게 이 함정의 진짜 위험성이다.

> **함정 박스 — Spring Boot 공식 이슈 #16689**
>
> 이 문제는 Spring Boot 프로젝트 GitHub에 #16689로 등록돼 있는 잘 알려진 함정이다. 이슈 자체는 멀티 모듈 Kotlin 프로젝트에서 발생한 `bootJar` 관련 사고 보고이지만, 그 댓글 흐름이 거의 멀티 모듈 Spring Boot 빌드 패턴의 표준 처방 모음에 가깝다. Gradle Discuss 포럼 41459번 글도 같은 사고의 변형이다. 처방의 결론은 한결같다 — **library 모듈에는 Spring Boot 플러그인을 적용하지 말 것.** 다음 절에서 그 처방을 두 가지 길로 살펴보자.

## 해결법 (A) — library 모듈에는 플러그인을 적용하지 않는다 (권장)

가장 깔끔한 처방부터 보자. **library 모듈에는 `org.springframework.boot` 플러그인을 아예 올리지 않는다. BOM만 `platform()`으로 들여온다.** 그러면 `domain` 모듈은 그냥 평범한 자바 라이브러리로 동작하고, 빌드 산출물도 우리가 기대하는 그 평범한 jar가 된다.

`app/build.gradle.kts`는 그대로 둔다 — application 모듈이니까 Spring Boot 플러그인이 자기 자리를 잡고 있을 권리가 있다.

```kotlin
// app/build.gradle.kts
import org.springframework.boot.gradle.plugin.SpringBootPlugin

plugins {
    java
    id("org.springframework.boot") version "4.0.6"
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

dependencies {
    implementation(platform(SpringBootPlugin.BOM_COORDINATES))

    implementation(project(":domain"))
    implementation(project(":order"))
    implementation(project(":payment"))

    implementation("org.springframework.boot:spring-boot-starter-web")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.named<Test>("test") {
    useJUnitPlatform()
}
```

핵심은 `domain` 쪽이다. 여기서는 `org.springframework.boot` 플러그인이 사라진다. 대신 BOM만 `platform()`으로 들여와서 Spring Framework, Jackson 같은 의존성의 버전 정합성은 보장받는다.

```kotlin
// domain/build.gradle.kts
import org.springframework.boot.gradle.plugin.SpringBootPlugin

plugins {
    `java-library`
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

dependencies {
    implementation(platform(SpringBootPlugin.BOM_COORDINATES))

    // 도메인 모듈이 정말로 외부에 노출해야 하는 타입에만 api
    api("org.springframework:spring-context")
    implementation("com.fasterxml.jackson.core:jackson-databind")
}

tasks.named<Test>("test") {
    useJUnitPlatform()
}
```

`order`와 `payment`도 같은 패턴이다. `java-library` + BOM platform 조합이다. 5장에서 만난 그 직교 원리 — "BOM은 resolution, Catalog는 declaration" — 가 여기서 그대로 살아 있다. **`platform()`이 BOM의 좌표 정합성만 빌려오고, 패키징 동작은 빌려오지 않는다는 점이 핵심이다.** Spring Boot 플러그인이 제공하는 가치 중에서 library 모듈에게 필요한 것은 의존성 버전 정렬뿐이다. fat jar 패키징, main class 탐지, `bootRun`, `bootBuildImage` — 이건 application 모듈에만 의미가 있다.

이렇게 바꿔놓고 다시 빌드를 돌려본다.

```bash
$ ./gradlew :domain:build
$ ls domain/build/libs/
domain-0.0.1-SNAPSHOT.jar

$ unzip -l domain/build/libs/domain-0.0.1-SNAPSHOT.jar | head -20
Archive:  domain/build/libs/domain-0.0.1-SNAPSHOT.jar
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  2026-05-11 14:31   META-INF/
       25  2026-05-11 14:31   META-INF/MANIFEST.MF
        0  2026-05-11 14:31   com/
        0  2026-05-11 14:31   com/shop/
        0  2026-05-11 14:31   com/shop/domain/
     1842  2026-05-11 14:31   com/shop/domain/Order.class
     2118  2026-05-11 14:31   com/shop/domain/OrderItem.class
     ...
```

이제 jar 안에 클래스가 들어 있다. `-plain` classifier가 붙은 jar도 없다. `app:bootRun`을 돌리면 `Order` 타입이 정상적으로 로드된다. 사고가 사라졌다.

## 해결법 (B) — apply false로 받고 일부 task만 끄기

(A)가 충분히 깔끔한데 왜 두 번째 처방을 또 보는가. 현실에서는 한 가지 사정이 끼어든다. 어떤 팀은 library 모듈에서도 Spring Boot가 제공하는 일부 기능 — 예를 들어 `developmentOnly` configuration이나, 자동으로 추가되는 `-parameters` 컴파일 옵션, 혹은 Spring Boot의 일부 source-set 처리 — 을 그대로 받고 싶어 한다. 이런 경우 플러그인을 통째로 빼버리기에는 아깝다. 그렇다면 플러그인은 적용하되, 우리를 함정에 빠뜨린 그 부분 — `bootJar`가 기본 jar를 갈아 끼우는 동작 — 만 꺼버리면 어떨까.

방법이 있다. **`apply false`로 플러그인을 settings 수준에서 가져오기만 하고, library 모듈에는 적용은 하되 `bootJar`/`bootRun` task만 비활성화한다.** 그러면 플러그인이 들고 오는 BOM과 부가 동작은 살리되, 패키징 동작은 비활성화된다.

```kotlin
// 루트 settings.gradle.kts에서 플러그인 버전만 잡아두는 게 가장 깔끔하지만,
// 여기서는 모듈 단위로 보여준다.

// domain/build.gradle.kts
plugins {
    id("org.springframework.boot")
    `java-library`
}

tasks.named<org.springframework.boot.gradle.tasks.bundling.BootJar>("bootJar") {
    enabled = false
}

tasks.named<Jar>("jar") {
    enabled = true
    archiveClassifier = ""   // -plain classifier를 제거하고 기본 좌표로 떨군다
}

tasks.named<org.springframework.boot.gradle.tasks.run.BootRun>("bootRun") {
    enabled = false
}
```

핵심 세 줄이다. `bootJar`를 끄고, 기본 `jar`를 다시 살리되 classifier를 비워서 메인 좌표 자리를 차지하게 한다. `bootRun`도 같이 꺼두자 — library 모듈에서 `./gradlew :domain:bootRun`을 잘못 돌리면 main class를 못 찾아 또 다른 사고가 난다.

이 방식이 (A)보다 나은 경우가 있을까. 솔직히 말하면, 일반적인 Spring Boot 백엔드 빌드에서는 (A)가 거의 항상 정답이다. (B)는 Spring Boot 플러그인의 부가 기능 — 컴파일 옵션 자동화, `developmentOnly` 같은 configuration — 을 library에도 균일하게 적용하고 싶은 팀이 선택할 만한 길이다. 다만 그 부가 가치 대비 비용 — `tasks.named<BootJar>` 같은 줄을 라이브러리마다 박아두는 번거로움, 그리고 누군가 그 코드를 빠뜨렸을 때 다시 함정에 빠질 위험 — 을 진지하게 가늠해봐야 한다.

> **박스 — `bootArchives` configuration의 정체와 publishing**
>
> 처방 (A)와 (B)의 차이를 정말로 이해하려면 `bootArchives`라는 configuration의 역할을 한 번 짚어둘 필요가 있다. Spring Boot 플러그인은 적용된 모듈마다 `bootArchives`라는 consumable configuration을 만든다. 이건 "이 모듈의 fat jar를 외부로 노출할 통로"다. `maven-publish` 플러그인이 적용되면 이 configuration이 기본 publication에 자동으로 묶이고, 결과적으로 Maven 좌표상의 main artifact가 fat jar가 된다.
>
> 단일 application 모듈에서는 이게 우리가 원하는 동작이다. CI에서 `./gradlew publish`를 돌리면 사내 Nexus에 실행 가능한 fat jar가 올라간다. 그런데 library 모듈에 이 동작이 그대로 들러붙으면 사내 의존성 저장소가 빈 fat jar로 가득 차게 된다. 다른 팀이 그 좌표를 import하면 또 같은 `ClassNotFoundException`을 만난다. 처음에 만났던 그 사고의 사내 버전이다.
>
> 처방 (A)는 `bootArchives` 자체를 만들지 않으니 publishing 시점에도 자연스레 일반 library jar가 main artifact가 된다. 처방 (B)는 `bootJar.enabled = false`로 막아도 `bootArchives` configuration은 살아 있을 수 있다 — 그래서 publishing을 같이 쓴다면 `configurations.named("bootArchives") { isCanBeConsumed = false }` 같은 줄이 추가로 필요해질 수 있다는 점을 기억해두자. 사내 의존성 저장소를 운영하는 팀이라면 이 부분이 운영 사고로 번지기 쉬운 자리다.

## 같은 구조, 두 가지 결과 — 실전 비교

말로만 둘이 다르다고 해선 와닿지 않는다. 똑같은 `app + domain` 구조를 두 가지 방법으로 빌드해서 결과 jar를 비교해보자.

먼저 사고 직전의 상태 — 모든 모듈에 Spring Boot 플러그인을 그냥 적용해버린 (X) 상태다.

```bash
# (X) library에도 Spring Boot 플러그인을 적용한 상태
$ ./gradlew :domain:build
$ ls domain/build/libs/
domain-0.0.1-SNAPSHOT-plain.jar       # 진짜 클래스가 든 jar (38KB)
domain-0.0.1-SNAPSHOT.jar             # 빈 fat jar (16MB, 의존성만 잔뜩)

$ unzip -p domain/build/libs/domain-0.0.1-SNAPSHOT.jar META-INF/MANIFEST.MF
Manifest-Version: 1.0
Main-Class: org.springframework.boot.loader.launch.JarLauncher
Start-Class: (없음)
Spring-Boot-Version: 4.0.6
...

$ ./gradlew :app:bootRun
... ClassNotFoundException: com.shop.domain.Order
```

이번엔 처방 (A)를 적용한 상태다.

```bash
# (A) library 모듈에서 Spring Boot 플러그인을 제거
$ ./gradlew :domain:build
$ ls domain/build/libs/
domain-0.0.1-SNAPSHOT.jar             # 평범한 library jar (38KB)

$ unzip -p domain/build/libs/domain-0.0.1-SNAPSHOT.jar META-INF/MANIFEST.MF
Manifest-Version: 1.0

$ unzip -l domain/build/libs/domain-0.0.1-SNAPSHOT.jar | grep ".class"
     1842  com/shop/domain/Order.class
     2118  com/shop/domain/OrderItem.class
     ...

$ ./gradlew :app:bootRun
... Started ShopApplication in 2.341 seconds
```

차이가 한눈에 들어온다. (X)에서는 16MB짜리 빈 fat jar와 38KB짜리 진짜 jar가 동시에 떨궈진다. main 좌표가 빈 fat jar로 잡혀 있으니 `app`이 그걸 끌어가서 사고가 난다. (A)에서는 38KB짜리 단일 jar만 떨궈진다. main 좌표가 그것이고, 내부에 우리가 작성한 클래스들이 그대로 들어 있다. 같은 소스, 같은 의존성, 다른 플러그인 적용 정책. 그것만의 차이다.

> **박스 — 어디서나 반복되는 사고 패턴**
>
> 이 함정의 진짜 무서움은 한 팀의 실수가 아니라 어디서나 같은 모양으로 반복된다는 점이다. Spring Boot 공식 이슈 트래커 [#16689](https://github.com/spring-projects/spring-boot/issues/16689)와 Gradle Discuss 포럼 [thread 41459](https://discuss.gradle.org/t/41459)을 따라가 보면 같은 사고가 거의 동일한 시나리오로 반복된다. 도메인 모듈을 사내 Nexus에 publish해서 여러 서비스가 공유하는 구조 → 새 서비스에서 `NoClassDefFoundError`가 줄을 잇기 시작 → 한참 의존성 그래프와 component scan 경로를 뒤지다 → 누군가 `domain.jar`를 직접 다운받아 `unzip`을 떠보고 빈 `BOOT-INF/classes/`를 본 순간 답이 나온다.
>
> 시발점은 거의 매번 같다. 첫 모듈은 보통 Spring Initializr가 만들어준 build.gradle.kts에서 출발하는데, 그 템플릿에는 `id("org.springframework.boot")`가 첫 줄부터 박혀 있다. 모듈을 늘릴 때 그 파일을 그대로 복사해 쓰면 도메인·공통 모듈에까지 그 한 줄이 따라 들어간다. 누구도 의도하지 않은 적용이지만, 결과는 빈 fat jar로 동일하다.
>
> 결론은 단순하다. **복사-붙여넣기로 늘어난 빌드 스크립트는 그 자체가 함정이다.** 다음 장에서 우리가 정확히 그 문제를 손볼 것이다.

## 마무리 — 빌드는 됐다. 그런데 build.gradle.kts가 너무 똑같다

자, 이제 `ch08-multimodule/`이 정상적으로 빌드된다. `domain`, `order`, `payment`는 library, `app`만 Spring Boot 플러그인을 적용한 application 모듈. `./gradlew :app:bootRun`을 돌리면 `Order` 타입이 멀쩡히 로드된다. 사고가 끝났다.

그런데 한 가지 찜찜한 게 남아 있다. 우리가 만든 네 모듈의 build.gradle.kts를 나란히 펼쳐놓고 보면, 거의 모든 줄이 똑같다. `java.toolchain.languageVersion = JavaLanguageVersion.of(21)`도 네 번 반복되고, `useJUnitPlatform()`도 네 번 반복되고, `implementation(platform(SpringBootPlugin.BOM_COORDINATES))`도 네 번 반복된다. 새 모듈을 추가하려고 할 때마다 어느 모듈의 build.gradle.kts를 베껴 와야 할지 막막하다. 그러다 한 줄을 빠뜨리면 또 어디선가 사고가 난다. 끔찍한 일이다.

처음 이걸 본 사람의 반사 신경은 — Maven 출신이라면 특히 — "그러면 root build.gradle.kts에 `subprojects {}` 블록 하나 만들어서 거기에 다 박으면 안 되나?"라는 질문일 것이다. 3장 끝에 이미 살짝 경고만 해뒀던 그 안티패턴 말이다. 다음 장에서 그 질문을 정면으로 받는다. **Convention Plugin이라는 정석으로, 4개 모듈의 build.gradle.kts를 각 한 줄짜리 짧은 파일로 줄이는 길**을 보자. 10장에서 그 작업을 한다.

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

---

# Part IV — 빌드를 도구로 만든다

여기까지 우리는 빌드 도구의 **소비자**였다. Spring Boot Gradle 플러그인이 만들어준 task를 썼고, JVM Test Suite 플러그인이 만들어준 task를 썼고, 외부에서 가져온 plugin들의 행동을 조정했다. Part IV에서 우리는 그 자리를 옮긴다. **빌드 도구의 생산자**로.

12장에서 우리 회사 빌드에만 의미 있는 task와 plugin을 직접 만든다. Git SHA를 파일로 떨궈주는 task 하나를 시작점으로, Provider/Property API와 `abstract class` 패턴과 Input/Output 어노테이션의 사고 모델을 손에 익힌다. 우리가 만든 `shop.build-info` plugin은 Part III에서 만든 `build-logic` included build에 자연스럽게 들어간다 — 그 자리가 바로 우리 회사 빌드의 도구 상자다. 13장에서 마지막 큰 스위치를 켠다. **Configuration Cache.** Gradle 9.x가 "preferred mode of execution"으로 못박은 모드다. 12장의 코드가 이미 그 세계의 시민권을 갖고 있다는 사실이 여기서 회수된다. third-party plugin이 비명을 지를 때 `problems=warn`으로 점진 도입하는 전략도 잡는다. 14장에서 그 도구를 CI 위에 올린다. `gradle/actions/setup-gradle@v6`로 캐시를 PR과 main 사이에서 운반하고, Build Scan을 PR에 자동으로 박아 동료들이 빌드 상태를 한 링크로 추적할 수 있게 만든다.

Part IV가 끝나는 자리에서 빌드는 더 이상 우리가 "한 번 적고 잊는 파일"이 아니다. **매일 우리와 함께 일하는 도구다.** 그리고 그 도구의 상태를 들여다볼 창이 PR에 한 줄로 달려 있다. 다음 Part는 그 도구가 운영 환경의 무게를 떠받치는 자리로 옮긴다.

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

# 14장. CI에 올린다 — GitHub Actions와 Build Scan

13장의 끝에서 우리는 로컬 빌드에 Configuration Cache와 Build Cache를 모두 켰다. 같은 입력으로 두 번 돌리면 두 번째는 거의 즉시 끝난다. 그런데 거기서 한 가지 아쉬움이 남는다. 로컬에서 빠른 빌드는 어디까지나 한 사람의 캐시다. 동료가 PR을 올리면 CI가 처음부터 다시 깡통에서 빌드를 돌린다. 그 깡통이 매번 의존성을 받고, 매번 Kotlin 컴파일러를 데우고, 매번 통합 테스트를 처음부터 띄운다. 로컬에서 1분 만에 끝나는 작업이 CI에서는 10분을 잡아먹는다. 무엇이 잘못된 걸까?

답은 둘 중 하나다. 정말로 빌드가 느리거나, 아니면 **CI가 제대로 캐시를 회수하지 못하고 있거나**. 우리 대부분의 경우는 후자다. 그리고 후자라면 도구가 거의 다 준비돼 있다. 이번 장에서는 13장에서 다듬어놓은 빌드를 GitHub Actions 위에 올린다. 그러는 동안 한 가지 욕심을 더 부린다 — CI가 끝날 때마다 Build Scan 링크가 PR에 자동으로 달리게 만들자. 빌드가 느리거나 깨졌을 때 동료가 그 링크 하나로 원인을 추적할 수 있게.

## 빌드의 Gradle 버전은 누가 정하는가

CI 워크플로우 파일을 열기 전에 한 가지를 다시 확인하자. **이 빌드의 Gradle 버전은 누가 정하는가?**

흔히 하는 답은 "내 PC에 깔린 Gradle"이지만, 그건 위험한 답이다. 내 PC에는 9.5가 깔려 있고 동료 PC에는 9.2가 깔려 있다면, 같은 코드를 빌드해도 결과가 다를 수 있다. CI 서버에는 또 다른 버전이 깔려 있을 수도 있다. 이게 운영에서 가장 짜증나는 종류의 차이다. "내 컴퓨터에선 되는데" 류의 차이가 빌드 도구 자체에서 발생하면 디버깅 비용이 끔찍하다.

그래서 답은 정해져 있다. **`./gradlew`로 빌드한다.** 프로젝트에 체크인된 Gradle Wrapper가 곧 빌드의 Gradle 버전 명세다. wrapper가 자기에게 맞는 distribution을 자동으로 받아다 캐시에 풀고, 그 버전으로 빌드를 돌린다. 누가 어디서 빌드를 돌리든 같은 Gradle을 쓴다. 너무 당연한 얘기 같지만, 실무에서 `gradle build`라고 시스템 Gradle을 부르는 PR을 종종 본다. CI 스크립트에 `gradle`이라고 적은 사람도 있다. 그러지 말자.

wrapper가 빌드 버전 명세라는 사실은 한 단계 더 나간 결론을 만든다. **wrapper를 올리는 일이 곧 이 빌드의 Gradle을 올리는 일이다.** 그리고 이 일은 한 줄로 끝난다.

```bash
./gradlew wrapper --gradle-version 9.5 --distribution-type=bin
```

`--gradle-version`은 익숙한 옵션이다. 그런데 `--distribution-type=bin`이 더 중요하다. 이 옵션을 빼먹으면 Gradle이 기본값인 `all` distribution을 받는다. `all`은 binary 외에 모든 소스와 문서를 포함하는 200MB+짜리 큰 묶음이다. IDE의 코드 점프에 도움이 되는 게 아니라면 사실상 쓸 데가 없는 200MB다. 그런데 CI는 새 머신에서 시작할 때마다 이 200MB를 받아온다. 매 빌드마다 다운로드 30초가 어디서 오는지 모를 때, 이 한 줄이 범인인 경우가 의외로 많다. 기억해두자. **wrapper를 올릴 때는 `--distribution-type=bin`을 항상 적자.**

그리고 9.5에서 wrapper에 작은 선물이 하나 더 붙었다. **다운로드 재시도(retries)**다. CI 머신이 가끔 네트워크를 한 번 놓쳐서 distribution 다운로드에 실패하는 경우가 있다. 이전에는 그 한 번의 실패가 PR을 빨갛게 만들었다. 9.5의 wrapper는 이걸 재시도한다.

```properties
# gradle/wrapper/gradle-wrapper.properties
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-9.5-bin.zip
networkTimeout=10000
retries=3
retryBackOffMs=1000
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

`retries=3`과 `retryBackOffMs=1000`. 작은 줄 두 개지만 CI의 flaky한 실패 한 종류를 사라지게 한다. 새 프로젝트라면 처음부터 넣자. 기존 프로젝트라면 wrapper를 9.5로 올리면서 같이 넣자. wrapper가 자체 다운로드를 재시도한다는 점 — 작지만 9.5의 좋은 변화 중 하나다.

## 가장 단순한 워크플로우부터

이제 GitHub Actions 워크플로우를 적어보자. 진짜로 가장 짧게 시작하자. `.github/workflows/build.yml` 파일을 하나 두고, 이렇게 적는다.

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-java@v5
        with:
          distribution: temurin
          java-version: 21
      - uses: gradle/actions/setup-gradle@v6
      - run: ./gradlew build
```

이게 거의 전부다. `checkout`으로 코드를 받고, `setup-java`로 Temurin 21을 깔고, `setup-gradle`로 Gradle 관련 셋업을 마치고, `./gradlew build`를 돌린다. 이 정도면 빌드가 일단 돈다.

그런데 우리가 13장에서 들인 노력 — Configuration Cache와 Build Cache —을 CI가 회수하게 만들려면 한 발 더 가야 한다. `setup-gradle` action이 그 자리에서 빛난다. 이 action이 정확히 무슨 일을 해주는지 알아두는 편이 낫다.

**첫째, Gradle User Home을 GitHub Actions 캐시에 자동으로 저장하고 복원한다.** `~/.gradle/caches/`에는 두 종류의 캐시가 산다. 의존성을 모아둔 `modules-2/`와 task 결과를 모아둔 `build-cache/`. `setup-gradle`은 이 둘을 함께 챙겨준다. 이 한 단계 덕분에 두 번째 빌드부터 의존성 다운로드 시간이 사라지고, 컴파일 task가 cache hit으로 즉시 끝나는 풍경이 펼쳐진다. 13장에서 만든 캐시가 이 자리에서 비로소 진가를 발휘한다.

**둘째, 다음 빌드를 위해 GitHub Actions의 캐시에 새 값을 다시 저장한다.** 캐시 키는 일·시간·brand 등 여러 신호를 조합해서 결정된다.

이 두 가지가 기본 동작이다. 거의 모든 PR에서 두 번째 빌드부터 이 차이를 체감할 수 있다. 그런데 이걸 그대로 쓰면 한 가지가 살짝 찜찜하다. **PR 브랜치마다 캐시에 쓰기를 한다는 점이다.** 동료가 깨진 빌드로 PR을 열면 그 깨진 상태의 캐시가 다른 PR로 흘러갈 수 있다. 그러지 않게 만들 방법이 있다.

## 캐시 오염을 막는 한 줄

답은 `cache-read-only`라는 input이다. 이름 그대로 캐시를 읽기 전용으로 쓰겠다는 선언이다. 그런데 이걸 무턱대고 켜면 캐시가 영영 갱신되지 않는다. 우리가 원하는 정책은 보통 이렇다. **`main` 브랜치는 캐시에 써도 된다. feature 브랜치는 읽기만 한다.** 메인 브랜치만이 빌드의 진실이고, 거기서 만든 캐시만 다른 빌드에 전염된다.

GitHub Actions의 표현식 한 줄로 정확히 이 정책을 만든다.

```yaml
- uses: gradle/actions/setup-gradle@v6
  with:
    cache-read-only: ${{ github.ref != 'refs/heads/main' }}
```

`github.ref`가 `refs/heads/main`이면 false(쓰기 허용), 아니면 true(읽기 전용). main에서만 캐시를 갱신하고, PR은 그 캐시를 읽기만 한다. PR이 캐시를 오염시킬 가능성이 사라진다. 작은 한 줄이지만 캐시 운영에서 가장 중요한 한 줄이다. 잊지 말자.

## Build Scan을 PR에 박는다

여기까지가 캐시 회수의 절반이다. 다른 절반은 진단이다. **빌드가 느려졌거나 깨졌을 때, 동료가 한 번에 원인을 찾을 수 있어야 한다.** Build Scan이 이 일을 해준다.

5장에서 우리는 한 번 `--scan`을 만났다. 로컬에서 빌드를 돌리고 끝에 `scans.gradle.com/...`로 시작하는 링크가 한 줄 나온 그 풍경이다. CI에서도 똑같이 이게 자동으로 떨어지게 만들 수 있다.

```yaml
- uses: gradle/actions/setup-gradle@v6
  with:
    cache-read-only: ${{ github.ref != 'refs/heads/main' }}
    build-scan-publish: true
    build-scan-terms-of-use-url: 'https://gradle.com/help/legal-terms-of-use'
    build-scan-terms-of-use-agree: 'yes'
```

`build-scan-publish: true` 한 줄이 핵심이다. 그 아래의 두 줄은 약관 동의를 워크플로우에 박아두는 거다. scans.gradle.com은 무료지만 공개 서비스고, 그 위에 빌드 내용을 올린다는 동의가 필요하다. 그 동의를 코드에 박는다.

이게 켜지면 CI가 끝날 때마다 PR 코멘트로 Build Scan 링크가 자동으로 달린다. 동료가 그 링크를 누르면 다음 정보가 한 화면에 펼쳐진다.

**task timeline.** 어떤 task가 몇 초 걸렸는지, 어느 task가 cache hit이고 어느 task가 새로 돌았는지, 어느 task가 다른 task를 기다리느라 멍하니 서 있었는지가 한 그래프에 보인다. 빌드가 갑자기 느려졌을 때 가장 먼저 보는 화면이다. 보통은 한두 개 task가 비정상적으로 길어진 게 눈에 들어온다.

**dependency 화면.** 어떤 라이브러리가 어떤 버전으로 들어왔는지, 누가 누구를 끌어들였는지, 어디에 충돌이 있었는지가 트리로 나온다. 9장에서 `bootJar` 함정을 진단할 때 우리는 이걸 손으로 추적했지만, Build Scan은 이걸 클릭으로 풀어준다. 의존성 충돌이 나서 빌드가 깨졌을 때 가장 빠른 진단 경로다.

**Configuration Cache 통계.** 13장의 회수 지점이 여기다. 이번 빌드가 configuration cache hit이었는지, 아니라면 왜 miss였는지, 어떤 task가 configuration cache를 깨뜨렸는지가 정리돼 나온다. "어제까지 빠르던 빌드가 오늘 갑자기 느려졌다"는 상황에서 첫 번째로 클릭할 자리다.

이 세 화면을 한 번씩 열어보는 습관을 들이자. 빌드가 느려지는 순간을 일찍 알아챈다.

## Dependabot도 같이 키우자

여기에 한 가지를 더 얹자. **`dependency-graph: generate-and-submit`이라는 input이다.**

```yaml
- uses: gradle/actions/setup-gradle@v6
  with:
    cache-read-only: ${{ github.ref != 'refs/heads/main' }}
    dependency-graph: generate-and-submit
    build-scan-publish: true
    build-scan-terms-of-use-url: 'https://gradle.com/help/legal-terms-of-use'
    build-scan-terms-of-use-agree: 'yes'
```

이 input을 켜면 setup-gradle이 빌드의 의존성 스냅샷을 GitHub Dependency Graph API에 자동으로 제출한다. 그러면 GitHub이 우리 Repository의 의존성 트리를 정확히 알게 된다. 무슨 이득이 있는가? **Dependabot alert이 정확해진다.**

Gradle 빌드를 Dependabot으로 관리해본 경험이 있는 사람은 알겠지만, 기본 Dependabot의 Gradle 지원은 살짝 어설프다. `build.gradle.kts`를 텍스트로 파싱해서 의존성을 추론하다 보니, version catalog나 platform BOM, convention plugin을 거치는 의존성을 놓친다. 그런데 우리가 8장에서 version catalog를 깔고, 10장과 11장에서 convention plugin·build-logic으로 의존성 관리를 추상화한 빌드라면, 텍스트 파싱은 거의 의미가 없다. `generate-and-submit`은 실제 빌드가 만든 정확한 dependency graph를 제출한다. 그 위에서 Dependabot이 돈다. alert이 빠지지도, 거짓으로 뜨지도 않는다.

한 줄로 이 차이가 만들어진다. 새 프로젝트라면 처음부터 켜자.

## 통합 테스트는 따로 보내자

여기까지가 단일 job 구성이다. 그런데 7장에서 우리는 통합 테스트를 별도 suite로 분리했다. `integrationTest`라는 이름의 task가 따로 등록돼 있고, Testcontainers가 그 안에서 Postgres를 띄운다. 이걸 CI에서 어떻게 다룰지가 중요한 결정이 된다.

가장 단순한 답은 한 job에서 `./gradlew build integrationTest`를 같이 돌리는 거다. 그러면 잘 돈다. 그런데 한 가지가 아쉽다. **통합 테스트가 단위 테스트에 비해 훨씬 무겁다는 점이 PR 피드백 속도에 그대로 반영된다.** 단위 테스트가 30초 만에 끝나도 통합 테스트가 4분을 잡아먹으면, PR 결과를 보기까지 4분 30초가 걸린다. 이걸 그대로 둘 이유가 없다.

병렬로 쪼개자.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-java@v5
        with:
          distribution: temurin
          java-version: 21
      - uses: gradle/actions/setup-gradle@v6
        with:
          cache-read-only: ${{ github.ref != 'refs/heads/main' }}
          dependency-graph: generate-and-submit
          build-scan-publish: true
          build-scan-terms-of-use-url: 'https://gradle.com/help/legal-terms-of-use'
          build-scan-terms-of-use-agree: 'yes'
      - run: ./gradlew build -x integrationTest

  integration-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-java@v5
        with:
          distribution: temurin
          java-version: 21
      - uses: gradle/actions/setup-gradle@v6
        with:
          cache-read-only: ${{ github.ref != 'refs/heads/main' }}
          build-scan-publish: true
          build-scan-terms-of-use-url: 'https://gradle.com/help/legal-terms-of-use'
          build-scan-terms-of-use-agree: 'yes'
      - run: ./gradlew integrationTest
```

두 job이 GitHub Actions의 기본 동작으로 병렬로 돈다. `build` job에서 `-x integrationTest`로 통합 테스트를 빼고, `integration-test` job에서 그것만 따로 돌린다. PR 화면에 두 개의 체크가 나란히 진행되고, 둘 중 늦은 쪽의 시간이 곧 PR 피드백 시간이 된다. 둘이 같이 4분이라면 4분으로 끝난다.

여기서 한 가지 좋은 점이 더 있다. **두 job이 같은 Gradle User Home 캐시를 읽는다.** `setup-gradle`이 캐시를 공유하기 때문에, `build` job이 의존성을 받아두면 `integration-test` job도 같은 캐시에서 의존성을 가져온다. 다운로드 비용이 한 번만 든다.

## JDK matrix — 두 버전을 한 번에

조금 더 욕심을 부려보자. 4장에서 우리는 빌드 JVM과 toolchain의 차이를 봤다. 빌드 JVM은 17 이상 아무거나 써도 되고, 빌드 대상 toolchain은 별도로 지정한다는 그림이었다. 그런데 회사에 따라서는 "JDK 17과 21 양쪽에서 다 돌아야 한다"는 요구가 있다. 운영 환경이 한쪽이라 해도, 옮겨갈 때를 대비해서 양쪽 호환성을 미리 확보하고 싶다는 마음이다. matrix가 이 요구를 깔끔하게 받아준다.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        java: [17, 21]
      fail-fast: false
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-java@v5
        with:
          distribution: temurin
          java-version: ${{ matrix.java }}
      - uses: gradle/actions/setup-gradle@v6
        with:
          cache-read-only: ${{ github.ref != 'refs/heads/main' }}
          build-scan-publish: true
          build-scan-terms-of-use-url: 'https://gradle.com/help/legal-terms-of-use'
          build-scan-terms-of-use-agree: 'yes'
      - run: ./gradlew build -x integrationTest
```

`matrix.java`에 17과 21을 두면 같은 job이 두 번 병렬로 실행된다. `fail-fast: false`도 의식적으로 켜두자. 기본값은 true인데, 그러면 한 쪽이 실패하는 순간 다른 쪽이 취소된다. 우리는 보통 두 결과를 다 보고 싶다. "17에서만 깨지고 21에서는 잘 도는" 결과 자체가 진단의 단서다. 다른 한 쪽이 일찍 끊어지면 그 단서를 잃는다.

여기서 한 가지 짚자. **빌드 JVM이 17이라고 해서 컴파일 결과가 17 바이트코드라는 뜻은 아니다.** 4장의 toolchain이 여전히 같은 결정을 한다. matrix의 17과 21은 Gradle 데몬을 굴리는 JVM이 17과 21이라는 의미일 뿐, 우리 코드가 어떤 바이트코드로 떨어질지는 `java { toolchain { languageVersion = JavaLanguageVersion.of(...) } }`이 정한다. matrix는 "Gradle 자체가 이 두 JVM에서 모두 정상 동작하는가"를 본다고 이해하자. 운영 JVM 호환성은 별개의 결정이다.

## Native 이미지는 한 발 비켜두자

PR마다 위 워크플로우가 돈다고 해보자. 빌드와 통합 테스트가 같이 끝나면 보통 3~5분 정도다. 무리 없는 속도다. 그런데 다음 장(15장)에서 다룰 GraalVM Native Image를 여기에 끼우면 어떻게 되는가? Native 이미지 빌드는 한 번에 5~20분, 메모리 4~8GB가 든다. 이걸 PR마다 돌리면 PR 피드백 시간이 갑자기 15분 뒤로 밀린다. 다른 개발자들이 PR을 줄줄이 올리면 GitHub Actions의 동시 실행 한도를 빠르게 소진하기도 한다.

그래서 답은 정해져 있다. **Native 이미지는 PR마다 돌리지 말자.** 별도 워크플로우로 빼고, 트리거를 둘 중 하나로 둔다. 첫째는 nightly schedule. 매일 한 번 main 브랜치에서 native 빌드를 돌려서 호환성을 확인한다. 둘째는 release 시점. 태그가 붙거나 release 워크플로우가 발사될 때만 native 이미지를 만든다.

```yaml
name: Native Build

on:
  schedule:
    - cron: '0 18 * * *'
  workflow_dispatch:

jobs:
  native:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: graalvm/setup-graalvm@v1
        with:
          java-version: '21'
          distribution: 'graalvm-community'
      - uses: gradle/actions/setup-gradle@v6
        with:
          cache-read-only: ${{ github.ref != 'refs/heads/main' }}
          build-scan-publish: true
          build-scan-terms-of-use-url: 'https://gradle.com/help/legal-terms-of-use'
          build-scan-terms-of-use-agree: 'yes'
      - run: ./gradlew nativeCompile
```

이 정도면 native 빌드를 PR 흐름에서 분리하면서도 정기적으로 검증이 일어난다. 15장에서 native 이미지의 의미·비용·운영 패턴을 본격적으로 다룰 때 이 워크플로우를 다시 만난다. 지금은 "native는 별도 job, 별도 트리거"라는 원칙만 챙기자.

## 마이그레이션 노트 — 옛 `gradle-build-action`을 보고 있다면

회사에 이미 굴러가는 Gradle CI 워크플로우가 있고, 그 안에 `gradle/gradle-build-action@v2` 같은 줄이 보인다면 한 단계 정리할 자리다. **`gradle-build-action`은 deprecated됐고, `gradle/actions/setup-gradle@v6`가 그 자리를 차지했다.** 둘은 같은 가족이지만 책임이 살짝 다르다.

`gradle-build-action`은 한 action이 두 일을 같이 했다 — Gradle 셋업과 빌드 실행. `with: arguments: build` 같은 식으로 빌드 명령까지 input으로 받았다. 그러다 보니 워크플로우의 `run:` 단계가 줄어들고, 빌드 명령이 action의 input으로 숨어버리는 구조가 됐다. 디버깅이 살짝 까다로워졌다.

`setup-gradle`은 책임을 다시 나눴다. **자기는 셋업만 책임지고, 빌드 명령은 일반 `run:` 단계에 둔다.** 우리가 이 장에서 쓴 모양이 정확히 그렇다 — `uses: gradle/actions/setup-gradle@v6`이 한 단계, `run: ./gradlew build`가 한 단계. 워크플로우의 흐름이 다시 명시적이 된다. 그리고 `gradle-build-action`이 모아두던 input들(cache-read-only, dependency-graph, build-scan-publish 등)이 그대로 setup-gradle로 옮겨왔다. 마이그레이션의 모양은 보통 이런 식이다.

```yaml
# 옛 모양
- uses: gradle/gradle-build-action@v2
  with:
    arguments: build
    cache-read-only: ${{ github.ref != 'refs/heads/main' }}

# 새 모양
- uses: gradle/actions/setup-gradle@v6
  with:
    cache-read-only: ${{ github.ref != 'refs/heads/main' }}
- run: ./gradlew build
```

거의 그대로 옮긴다. 다만 옮기는 김에 한 번에 `build-scan-publish`, `dependency-graph`도 같이 켜두자. 두 input은 새 action에서 정식 지원이고, 이 장에서 봤듯이 작은 비용으로 큰 진단 자산을 만든다.

## Part IV를 닫으며

12장에서 우리는 빌드 자체를 도구로 만드는 길에 발을 디뎠다. 13장에서 Configuration Cache와 Build Cache로 그 도구를 빠르게 만들었다. 14장에서 그 도구를 CI 위에 올리고, Build Scan으로 도구의 상태를 들여다볼 창을 열었다. 이 셋이 Part IV의 묶음이다. **빌드는 더 이상 우리가 "한 번 적고 잊는 파일"이 아니라, 매일 우리와 함께 일하는 도구다.**

지금 우리의 `ch14-ci/.github/workflows/build.yml`을 보면 모양이 이렇다. PR이 열리면 두 개의 체크가 동시에 돈다 — `build`와 `integration-test`. 둘 다 setup-gradle이 깔아둔 Gradle User Home 캐시를 공유한다. JDK matrix가 17과 21 양쪽을 동시에 확인한다. 빌드가 끝나면 PR에 Build Scan 링크가 한 줄 달린다. main 브랜치만 캐시에 쓴다. Dependabot은 정확한 dependency graph 위에서 alert을 만든다.

이 정도면 매일 일하는 빌드의 기본기는 갖춰졌다. 다음 Part는 "운영의 무게"다. 빌드를 만든 도구가 운영 환경의 요구를 만나면서 어떤 새 질문이 생기는가. 첫 번째 질문이 15장에서 기다린다. **Spring Boot 앱을 GraalVM Native Image로 만들면 무엇이 변하고, 그 비용을 언제 지불할 가치가 있는가?** 이번 장에서 따로 빼둔 native 워크플로우의 안쪽으로 들어가보자.

---

# Part V — 운영의 무게

Part IV까지 빌드를 도구로 키우는 길을 걸었다. Part V는 그 도구가 운영 환경의 요구를 떠받치는 시점이다. 운영의 첫 번째 무게는 **패키징**이다. JVM 위의 fat jar로 충분한가, GraalVM Native binary까지 가야 하는가, 그 비용을 언제 지불할 가치가 있는가. 두 번째 무게는 **신뢰**다. 우리 빌드 산출물 안에는 직접 적은 코드보다 훨씬 더 많은 transitive 의존성이 들어 있다 — 그 수백 개를 우리는 정말 신뢰하고 있는가. 세 번째 무게는 **마이그레이션**이다. 회사 빌드가 8.x나 7.x에 머물러 있고 9.x로 옮기는 임무가 떨어졌다면 어디서부터 깨질지 알아야 한다.

Part V의 네 챕터는 이 세 무게를 다룬다. 15장에서 GraalVM Native Image의 안쪽을 들여다보고 — 5~20분의 빌드 시간, 4~8GB의 메모리, 런타임에 비로소 깨지는 reflection hint — 그 비용을 PR 흐름 바깥으로 분리해 nightly와 release만 책임지게 두는 운영 패턴을 잡는다. 16장에서 Dependency Verification, Dependency Locking, Repository Content Filtering 세 도구를 한 자리에 놓고 supply chain의 모양을 그린다. 8장에서 만든 settings 레벨의 일관성이 16장의 보안으로 그대로 흘러드는 자리이기도 하다. 17장에서 회사 빌드를 9.5로 옮기는 step-by-step 절차를 따라간다 — Daemon JDK 17+, `jcenter()` 제거, `Project#exec` 제거, Convention API 제거, KGP 2.0+, archive reproducibility까지. 6장의 Spring Boot 버전 마이그레이션과 17장의 Gradle 버전 마이그레이션의 역할 분담을 명확히 한다. 18장은 책의 마지막 장이다. 1장의 9가지 약속을 회수하고, 책에서 다루지 않은 영역 중 회사 빌드에 다음으로 도입할 만한 세 가지를 고른다.

Part V가 끝나는 자리에서 우리 `shop` 앱은 책을 떠난다. 단일 의존성 한 줄에서 시작해서, 멀티 모듈 + 커스텀 플러그인 + Configuration Cache + CI + Native + 보안까지 자랐다. 그 자리에 이제 당신 회사의 `build.gradle.kts`가 선다.

# 15장. GraalVM Native Image로 패키징한다

새벽 두 시, 가상 서버 한 대에 Spring Boot 앱 다섯 개를 띄워야 하는 상황을 가정해보자. 각 앱이 부팅에 4초씩 걸리고, 기동 직후 메모리를 600MB씩 잡아먹는다. 다섯 개면 3GB가 우습게 사라진다. 서버리스 환경이라면 더 난감하다. 사용자가 첫 요청을 보내고 4초를 기다리는 사이, "콜드 스타트"라는 말이 SLA 문서 위로 떠오른다. 그렇다면 어떻게 해야 할까?

GraalVM Native Image는 이 질문에 한 가지 답을 내민다. **JVM을 빼버리자.** Spring Boot 앱을 OS 위에서 직접 도는 단일 실행 파일로 컴파일해버린다. 부팅이 100ms 단위로 떨어지고, 메모리 사용량은 1/3 이하로 줄어든다. 보기에는 마법 같다. 그런데 마법에는 늘 값이 따라온다. 빌드가 5~20분 걸린다. 빌드 한 번에 RAM 4~8GB가 들어간다. 리플렉션을 잘못 쓰면 런타임에 비로소 깨진다. 디버깅이 까다로워진다. **그래서 이 장은 "어떻게 native로 만드는가"만큼이나 "언제 그 비용을 지불할 가치가 있는가"를 같은 비중으로 다루려 한다.**

Part V의 문이 여기서 열린다. Part IV까지 우리는 빌드를 도구로 키우는 길을 걸었다. Part V는 그 도구가 운영 환경의 무게를 떠받치는 시점이다. 운영의 첫 번째 무게는 패키징이다. 우리가 만든 앱을 어떤 모양으로 서버에 던질 것인가. 그 선택지 가운데 가장 극단적인 모양이 native binary다. 14장에서 native 빌드를 PR 흐름에서 따로 빼두자고 약속했었다. 그 약속의 안쪽으로 이제 들어가보자.

## 플러그인 하나가 일으키는 연쇄 반응

`ch15-native/build.gradle.kts`를 열고 한 줄을 추가한다고 해보자.

```kotlin
plugins {
    id("org.springframework.boot") version "4.0.6"
    id("io.spring.dependency-management") version "1.1.7"
    id("org.graalvm.buildtools.native") version "0.11.5"
    kotlin("jvm") version "2.2.20"
    kotlin("plugin.spring") version "2.2.20"
}
```

세 번째 줄, `org.graalvm.buildtools.native` 하나가 들어왔다. 그러면 빌드의 모양이 어떻게 바뀌는가? `./gradlew tasks --group "native"`를 한 번 두드려보자. `nativeCompile`, `nativeRun`, `nativeTest`가 새로 떴다. `./gradlew tasks --group "build"`를 보면 `processAot`, `processTestAot`도 같이 떠 있다. 우리가 적은 줄은 하나인데, 빌드 그래프에 새 식구가 다섯 가족 단위로 들어왔다. 무슨 일이 일어난 걸까?

GraalVM Native plugin이 적용되는 순간, **자기 혼자 들어오는 게 아니라 `org.springframework.boot.aot` 플러그인을 같이 끌고 들어온다.** 이 둘이 합쳐서 다음 변화를 만든다.

1. `aot`, `aotTest`라는 새로운 소스셋이 생긴다.
2. `processAot`, `processTestAot` task가 등록된다 — Spring의 AOT(Ahead-of-Time) 처리를 실행하는 task다.
3. `nativeCompile`이 일반 `compileJava` 출력이 아니라 `processAot`의 출력을 입력으로 받는다.
4. `bootJar`가 만드는 jar 안에 reachability metadata가 같이 들어가고, jar 매니페스트에 `Spring-Boot-Native-Processed: true`라는 줄이 한 줄 추가된다.

이 네 가지가 동시에 일어난다는 점을 기억해두자. 우리는 한 줄을 더했을 뿐인데, Spring Boot의 빌드 파이프라인 자체가 native를 향해 재배열됐다. **AOT 처리가 무엇이며 왜 필요한가**가 자연히 따라오는 질문이다.

JVM 위에서 Spring Boot가 부팅할 때는 클래스패스를 훑고, `@Configuration` 클래스들을 찾고, 컴포넌트 스캔을 돌리고, 빈을 만들고, AutoConfiguration 조건을 평가한다. 이 과정의 대부분이 **런타임에 일어난다**. 그런데 native binary는 런타임에 클래스를 새로 로드하지 않는다. 모든 클래스가 빌드 시점에 확정돼야 한다. 그러면 Spring의 그 풍성한 런타임 결정은 어디서 해야 하는가? 답은 하나뿐이다. **빌드 시점으로 옮긴다.** 이게 AOT 처리다. `processAot`이 Spring 컨테이너를 빌드 시점에 한 번 시뮬레이션해서, "이 앱은 결국 이 빈들을 이렇게 만들어 쓴다"라는 결과를 Java 코드와 메타데이터로 미리 적어둔다. 그 결과물이 `aot` 소스셋에 떨어지고, `nativeCompile`이 그걸 입력으로 받아 binary를 만든다.

그래서 GraalVM Native plugin은 단순히 "C로 컴파일하는 도구"가 아니다. **Spring AOT와 GraalVM, 두 도구가 직렬로 연결되도록 빌드 그래프를 다시 그리는 어댑터**다. 이 둘이 잘 짜여 있어서 우리는 플러그인 하나만 적으면 된다. 안에서 일어나는 일이 무엇인지 알고 보면, "처음 native 빌드가 왜 그렇게 한참 돌고 있는가"가 덜 답답해진다.

## `nativeCompile`을 한 번 돌려보자

`ch15-native/`에 작은 컨트롤러 하나를 두자.

```kotlin
@RestController
class HelloController {
    @GetMapping("/hello")
    fun hello(): Map<String, String> = mapOf("greeting" to "hi from native")
}
```

GraalVM이 설치돼 있다고 가정한다. 로컬에 없다면 SDKMAN으로 `sdk install java 21-graalce` 같은 식으로 받아두자. JDK 자체가 GraalVM 배포판이어야 한다. 일반 OpenJDK로는 `nativeCompile`이 돌지 않는다. 이게 첫 번째 진입 비용이다.

```bash
./gradlew nativeCompile
```

처음 누르면 한참 동안 콘솔이 조용하다. 1분쯤 지나면 `processAot`이 도는 로그가 보인다. Spring이 빌드 시점에 컨테이너를 시뮬레이션하며 `META-INF/native-image/...`에 reachability metadata를 떨어뜨린다. 그 다음이 진짜 무거운 단계다. GraalVM의 `native-image` 도구가 우리 코드, 우리가 끌어다 쓴 모든 의존성, JDK 클래스 일부까지 한 binary로 합쳐 정적으로 컴파일한다. 분석(Points-to analysis), 빌딩, 최적화, 이미지 작성. 단계마다 진행 막대가 천천히 차오른다. 이걸 처음 보는 개발자가 "내 컴퓨터가 망가졌나?"라고 생각하는 건 자연스러운 반응이다. 망가진 게 아니다. 그냥 native 빌드가 원래 이만큼 무겁다.

다 끝나면 `build/native/nativeCompile/`에 OS-native 실행 파일이 떨어진다. macOS면 Mach-O, Linux면 ELF다. 그걸 직접 실행해보자.

```bash
./build/native/nativeCompile/ch15-native
```

콘솔에 "Started Application in 0.083 seconds" 같은 줄이 뜨면 성공이다. 한자릿수 밀리초 단위로 떨어지는 부팅 시간을 처음 보면 살짝 놀랍다. JVM에서 같은 앱을 띄우면 보통 1.5~3초 걸리던 게, 여기서는 100ms 안에 끝난다. 메모리도 마찬가지다. `ps -o rss= -p $(pgrep ch15-native)`를 찍어보면 60~120MB 수준이다. JVM이었으면 같은 앱이 400~600MB는 잡는다. 이 숫자들이 native의 마케팅 문구다. 그리고 마케팅 뒤편에 우리가 방금 5~15분간 본 빌드 시간이 있다.

## 빌드 시간의 무게를 받아들이는 법

자, 빌드가 무거운 건 부정할 수 없는 사실이다. 그러면 우리가 일하는 흐름에는 이걸 어떻게 끼워 넣어야 하는가? 답은 단호하게 짚고 가자. **개발자 로컬에서는 JVM 빌드를 유지한다.** 코드 한 줄 바꿀 때마다 `nativeCompile`을 돌리면 일이 안 된다. `./gradlew bootRun`으로 JVM에서 띄우고, 단위 테스트는 `./gradlew test`로 JVM에서 돌리는 일상 흐름은 그대로 둔다. native 빌드는 **확인용이지 개발용이 아니다**.

그러면 native는 언제 도는가? 두 군데다. 첫째, CI의 별도 job. 둘째, release 파이프라인. 14장 끝에서 나눈 이야기와 정확히 같은 결론으로 다시 돌아온다.

> **함정 박스 — Native 빌드 시간을 어떻게 받아들이는가**
>
> Native 빌드의 시간·메모리 비용을 줄이는 묘약은 사실 없다. 줄이는 게 아니라 **언제 지불할지를 분리해 두는** 것이 운영 패턴이다.
>
> - **PR마다 돌리지 말자.** 14장의 `Native Build` 워크플로우처럼 schedule(예: 매일 18시 UTC)과 `workflow_dispatch`로만 트리거를 둔다. PR 흐름은 JVM 빌드와 통합 테스트로 빠르게 유지한다.
> - **`bootBuildImage`를 쓸 때 buildpack 레이어 캐시를 Volume으로 영속화하자.** 빌드 컨테이너가 매번 paketo builder의 GraalVM 캐시를 새로 받지 않도록 한다. 로컬이면 `~/.docker`/Colima의 데이터 볼륨, CI면 cache action 위에 docker volume을 묶는다. 이 캐시 한 번이 5분 정도를 흡수한다.
> - **메모리 OOM이 뜨면 `-J-Xmx8g`를 한 번 시도해보자.** native-image 도구가 자기 분석 단계에서 힙을 많이 쓴다. Gradle 쪽에 `tasks.named<BuildNativeImageTask>("nativeCompile") { jvmArgs("-J-Xmx8g") }` 식으로 넘기거나, `bootBuildImage`라면 `environment.put("BP_NATIVE_IMAGE_BUILD_ARGUMENTS", "-J-Xmx8g")`로 빌더에 전달한다. GitHub-hosted runner의 기본 7GB로는 큰 앱이 곧잘 터진다.
> - **runs-on을 키우는 것도 한 방법이다.** `ubuntu-latest-8-cores` 같은 large runner를 native job만 쓰도록 한다. PR 빌드는 보통 runner를 그대로 둔다 — 비용 차이가 거기서 갈린다.

이 패턴이 자리잡으면 매일 아침 main 브랜치에 native 빌드 결과 하나가 쌓인다. 한 달 동안 native가 한 번도 깨지지 않았다면 운영 후보로 올릴 수 있다. 깨지는 날이 있다면 그 commit이 무엇이었는지 매일 단위로 좁혀 들어갈 수 있다. **빠른 피드백은 PR 흐름이 책임지고, 깊은 검증은 nightly가 책임진다.** 이렇게 책임을 분리하면 native의 무게가 일상 일을 누르지 않는다.

## `bootBuildImage`가 native 이미지가 되는 순간

6장에서 우리는 `bootBuildImage`를 처음 만났다. Cloud Native Buildpacks가 Dockerfile 없이도 OCI 이미지를 만들어주는 task다. 그때 작은 박스로 "GraalVM Native plugin이 같이 적용돼 있으면 native 이미지로 자동 빌드된다"라고 한 줄 적어두고 지나갔다. 그 한 줄이 이 장에서 회수될 차례다.

15장의 build script는 이미 GraalVM Native plugin을 갖고 있다. 그 상태에서 `bootBuildImage`를 그냥 부르면 어떻게 되는가?

```bash
./gradlew bootBuildImage --imageName=ghcr.io/example/hello:native
```

빌더(paketo의 builder-noble-java-tiny)가 자기 안의 GraalVM buildpack을 자동으로 활성화한다. 컨테이너 안에서 우리가 방금 본 `processAot` → `native-image` 흐름이 그대로 일어난다. 결과는 OCI 이미지 한 장인데, 안에 든 게 jar가 아니라 native 실행 파일이다. **Dockerfile 없이도 native 이미지가 만들어진다.** Spring 팀이 native를 "쉽게" 만들기 위해 얹어둔 자동화 한 겹이 여기서 빛난다.

```kotlin
tasks.named<BootBuildImage>("bootBuildImage") {
    imageName = "ghcr.io/example/hello:${project.version}"
    environment.put("BP_NATIVE_IMAGE", "true")
    environment.put("BP_NATIVE_IMAGE_BUILD_ARGUMENTS", "-J-Xmx8g")
    publish = true
    docker {
        publishRegistry {
            username = providers.environmentVariable("GHCR_USER").get()
            password = providers.environmentVariable("GHCR_TOKEN").get()
        }
    }
}
```

`BP_NATIVE_IMAGE`는 사실 GraalVM plugin이 적용돼 있으면 자동으로 켜진다. 명시적으로 적어두는 건 의도를 드러내기 위해서다. 누가 이 build script를 처음 읽어도 "아, 이건 native 이미지를 만드는 task구나"가 한눈에 들어온다. **빌드 의도가 문서가 되도록 적는 습관**의 한 사례라고 봐도 좋다.

여기서 한 가지 짚자. `bootBuildImage`의 native 빌드는 도커 컨테이너 안에서 일어난다. 즉 **로컬에 GraalVM JDK가 없어도 된다.** `./gradlew nativeCompile`은 로컬 JDK가 GraalVM이어야 하지만, `bootBuildImage`는 빌더 이미지 안의 GraalVM을 쓴다. 도커만 깔려 있으면 어떤 JDK로도 native OCI 이미지를 뽑을 수 있다는 뜻이다. CI runner에 GraalVM을 따로 깔지 않아도 native 이미지를 만들 수 있는 길이 여기에 있다.

대신 도커 빌드의 메모리 한도에 신경 쓰자. Colima나 Docker Desktop의 기본 VM 메모리가 4GB로 잡혀 있다면, native 빌드가 그 안에서 OOM으로 죽는다. Docker Desktop의 Resources 탭에서 메모리를 8~12GB로 키워두는 게 안전하다. 메모리 압박은 native 빌드의 첫 번째 사고 원인이다.

## AOT만 단독으로 — native까지 가지 않더라도

native까지 안 가더라도 AOT 처리 자체가 주는 이득이 있다. 부팅이 빨라지고, 빈 정의가 미리 풀려 있으니 시작 시 JIT 워밍업 시간이 짧아진다. JVM에서 그대로 도는 일반 jar인데도 부팅이 빨라진다는 뜻이다. CDS(Class Data Sharing)와 조합하면 효과가 더 커진다. 그렇다면 native 빌드의 무거운 비용은 지불하지 않고 AOT의 이득만 가져갈 수 없을까? 가능하다.

```kotlin
plugins {
    id("org.springframework.boot") version "4.0.6"
    id("io.spring.dependency-management") version "1.1.7"
    kotlin("jvm") version "2.2.20"
    kotlin("plugin.spring") version "2.2.20"
}

apply(plugin = "org.springframework.boot.aot")
```

GraalVM Native plugin은 빼고, AOT 플러그인만 `apply`로 따로 적용한다. 그러면 `processAot`이 빌드 그래프에 들어오지만 `nativeCompile`은 들어오지 않는다. `bootJar`에 AOT 산출물이 포함된다. 운영에서는 `java -Dspring.aot.enabled=true -jar app.jar` 식으로 띄우면 AOT 결과를 쓴다. 부팅 시간이 보통 30~50% 줄어든다.

**그래서 결정의 사다리는 이런 식으로 그릴 수 있다.** 운영 부팅이 느려서 SLA가 흔들린다면 우선 AOT만 켜보자. 그래도 부족하다면, 그리고 메모리 절감이나 콜드 스타트 100ms가 정말 필요한 워크로드라면 native까지 간다. **거꾸로 가지 말자.** "native가 멋있어 보여서 일단 한다"는 결정은 빌드 비용·디버깅 비용·운영 모니터링 비용으로 청구서가 돌아온다. 매번 답이 native일 필요는 없다.

## 런타임에 비로소 깨지는 클래스

Native 빌드를 처음 운영에 올린 팀이 가장 자주 겪는 사고가 있다. **빌드는 잘 끝났는데, 정작 native 앱을 띄우면 런타임에 `ClassNotFoundException`, `NoSuchMethodException`, `NullPointerException`이 어딘가에서 튀어나오는 일이다.** JVM에서는 잘 돌던 코드가 native에서만 깨진다. 왜 그럴까?

Native binary에는 우리가 "쓸 거라고 native-image 도구가 판단한 클래스"만 들어간다. 정적 분석으로 도달 가능(reachable)하다고 본 코드만 묶는다는 뜻이다. 그런데 자바·코틀린 코드는 곳곳에 정적으로 보이지 않는 호출이 있다. `Class.forName("com.example.MyHandler")` 같은 리플렉션, `getResourceAsStream("config/data.json")` 같은 리소스 로딩, JDK Proxy로 만드는 동적 프록시 — 이런 호출은 native-image 도구가 "어떤 클래스가 결국 필요한지"를 정적으로 알 수 없다. 빌드가 끝나면 그 클래스들은 binary에 안 들어가 있다. 운영에서 그 코드가 도는 순간 비로소 "그런 클래스 없는데?"라는 예외가 튀어나온다. **JVM이라면 ClassLoader가 그때그때 찾아주던 게, native에는 ClassLoader가 없다.**

Spring 자체의 코드는 Spring AOT 처리가 이 hint들을 거의 다 자동으로 만들어준다. `@Configuration`, `@RestController`, `RestTemplate` 등이 안에서 어떤 리플렉션을 쓰는지 Spring 팀이 다 알고 있어서, Spring 코드의 reachability metadata는 GraalVM reachability metadata 저장소 또는 Spring 자체의 hint 코드가 채워둔다. 우리가 그걸 의식할 일이 별로 없다는 게 native가 사용 가능한 수준까지 올라온 이유다.

문제는 **우리 코드 중에 리플렉션을 쓰는 부분**, 그리고 **third-party 라이브러리 가운데 아직 hint가 정비되지 않은 것**이다. Jackson으로 직렬화하는 우리 데이터 클래스, JPA로 매핑하는 엔티티 클래스, 우리가 직접 짠 `Class.forName` 한 줄 — 이런 것들이 사고의 진원지가 된다.

> **함정 박스 — `RuntimeHintsAgent`로 hint를 채우자**
>
> Spring Framework는 `org.springframework:spring-core-test` 모듈 안에 **RuntimeHintsAgent**라는 Java agent를 함께 배포한다. JVM 위에서 우리 앱이나 통합 테스트를 한 번 실제로 굴리는 동안, 어떤 리플렉션·리소스·프록시 접근이 일어났는지 메서드 호출 단위로 기록해서 우리가 빠뜨린 hint를 보여준다. ([Spring Framework Reference — Core/AOT/Hints](https://docs.spring.io/spring-framework/reference/core/aot.html))
>
> 적용은 우리가 직접 `-javaagent`로 붙여 준다. Spring Boot가 따로 Gradle plugin을 한 줄짜리로 노출하지 않으니, 이 절차는 일종의 의식이 된다.
>
> ```kotlin
> // app/build.gradle.kts
> val runtimeHintsAgent: Configuration by configurations.creating
>
> dependencies {
>     runtimeHintsAgent("org.springframework:spring-core-test")
> }
>
> testing {
>     suites {
>         val integrationTest by getting(JvmTestSuite::class) {
>             targets.all {
>                 testTask.configure {
>                     jvmArgs("-javaagent:${runtimeHintsAgent.asPath}")
>                 }
>             }
>         }
>     }
> }
> ```
>
> 통합 테스트에 `@EnabledIfRuntimeHintsAgent`를 단 클래스들은 agent가 붙어 있을 때만 실행되고, agent가 모은 trace를 검증한다. agent가 본 호출들을 그대로 `RuntimeHints`로 옮겨서 우리 hint 코드에 누락된 호출이 있는지 비교하는 패턴이 가장 흔하다.
>
> 핵심은 **"운영에서 실제로 도는 코드 경로"를 hint 수집에 포함시키는 것**이다. 단위 테스트만 돌고 끝나면 운영 경로의 리플렉션이 빠진다. 통합 테스트가 controller부터 repository까지 한 바퀴 도는 시나리오를 갖고 있다면, 그 위에 agent를 한 번 얹는 것만으로도 hint 누락의 대부분이 메워진다. 7장의 JVM Test Suite로 분리해 둔 `integrationTest`가 여기서 두 번째 일을 한다.

만약 agent를 돌렸는데도 운영에서 사고가 나면? Native binary에 디버그 심볼을 같이 넣어 두자. `tasks.named<BuildNativeImageTask>("nativeCompile") { debug.set(true) }`로 켜면 stack trace가 의미 있는 모양으로 나온다. 그리고 운영 인프라에 `gdb`로 native 프로세스에 붙어 들여다볼 수 있는 채널을 미리 준비해 두자. JVM의 `jstack`, `jmap` 같은 도구는 native에서 안 통한다. **native 운영은 디버깅 도구 자체가 새로 짜인다.** 이 점이 native 도입 결정에서 가장 자주 과소평가되는 비용이다.

## 그래서 언제 native를 쓰는가

장 초반의 질문으로 돌아가자. 언제 그 비용을 지불할 가치가 있는가? 운영 현장의 패턴을 보면 답이 두세 묶음으로 정리된다.

**첫째, 서버리스와 콜드 스타트가 매출에 직결되는 환경.** AWS Lambda, Google Cloud Run 같은 데서 Spring Boot를 띄울 때, JVM의 1.5~3초 부팅이 사용자 첫 응답 시간으로 직접 노출되는 경우. 여기서는 native의 100ms 부팅이 그냥 좋은 정도가 아니라 매출의 일부다. 빌드 비용은 release 파이프라인 안에서 흡수된다.

**둘째, 같은 노드에 작은 앱을 여러 개 띄워야 하는 환경.** Kubernetes 위에서 마이크로서비스 50개를 한 클러스터에 올린다고 해보자. JVM 50개가 각자 400MB씩 잡으면 노드가 빨리 닳는다. native binary 50개라면 노드의 메모리 풋프린트가 절반 이하로 떨어진다. 회사 인프라 비용이 줄어드는 종류의 의사결정이다.

**셋째, 작은 CLI 도구.** Spring 기반 admin CLI, 운영 스크립트 등 부팅과 종료가 자주 일어나는 짧은 프로세스. JVM 워밍업 비용이 작업 본체보다 큰 케이스다.

거꾸로, native를 굳이 안 가도 되는 경우가 많다. 오랫동안 떠 있는 monolith라면 부팅 시간은 한 번의 비용이다. JIT가 데우는 동안의 워밍업도 어차피 한 번이다. 메모리 절감은 절약 폭이 작고, 디버깅 도구가 줄어드는 비용은 항상 크다. **이런 워크로드에는 AOT만 켜고 native까지는 안 가는 게 균형 잡힌 선택이다.**

회사가 native를 도입한다고 하면, 한 가지 더 권하고 싶은 게 있다. **운영 모니터링에 부팅 시간과 RSS를 metric으로 박아두자.** native가 약속한 이득이 실제로 들어오는지 숫자로 확인할 수 있어야 한다. JVM 시절의 prometheus 메트릭 수집은 native에서도 그대로 된다(Micrometer가 native에서 동작한다). 부팅 시간 metric은 application이 띄워질 때 한 번 적어두자. 한 달 뒤에 그 그래프가 한 자릿수 밀리초 영역에 머물러 있으면 도입이 잘된 것이다. 1초대로 슬며시 올라가 있다면 어떤 startup 처리가 잘못 들어간 신호다. **숫자로 검증하지 못하는 도입은 도입이 아니다.**

## 마무리

15장에서 우리는 GraalVM Native Image의 안쪽을 들여다봤다. 플러그인 한 줄이 Spring AOT 플러그인을 같이 끌어와 빌드 그래프를 재배열한다는 것을 봤다. `processAot` → `native-image` 흐름으로 native binary가 나오고, 그게 100ms 부팅과 1/3 메모리라는 결과로 떨어지는 길을 따라가봤다. `bootBuildImage`가 같은 build script로 native OCI 이미지를 자동으로 만들어주는 자리도 확인했다. AOT만 단독으로 적용해서 native까지는 안 가는 중간 선택지도 손에 넣었다.

그리고 그 위에 비용을 두고 왔다. 5~20분의 빌드 시간, 4~8GB의 메모리, 런타임에 비로소 깨지는 reflection hint, 줄어든 디버깅 도구. 이 비용을 PR 흐름 바깥으로 분리해 nightly와 release만 책임지게 두는 운영 패턴을 잡았다. native가 어울리는 워크로드와 그렇지 않은 워크로드를 두 묶음으로 나눠 봤다. **Native는 "더 나은 패키징"이 아니라 "조건이 맞을 때 쓰는 도구"임을 기억해두자.**

Part V의 첫 장이 끝났다. 운영의 첫 번째 무게가 패키징이었다면, 두 번째 무게는 **신뢰**다. 우리 빌드 산출물의 안에는 직접 적은 코드보다 훨씬 더 많은 transitive 의존성이 들어 있다. 그 의존성들을 우리는 어디서 받았고, 누가 서명했으며, 다음 빌드에 같은 것이 들어온다는 보장이 어디 있는가? 16장에서 Dependency Verification, Dependency Locking, Repository Content Filtering을 한 자리에 놓고, **공급망 보안**의 모양을 그려보자.

# 16장. 의존성 보안 — Verification, Locking, Repository Content Filtering

> 이 챕터는 `ch16-security/` 폴더에서 동작한다. `ch15-native/`를 카피해 그 위에 `verification-metadata.xml`과 `gradle.lockfile`을 쌓고, settings의 repository 선언에 content filter를 박는다.

신선한 Spring Boot 프로젝트 한 곳에서 `./gradlew :app:dependencies --configuration runtimeClasspath`를 돌려보자. 의존성 트리가 화면 한 페이지를 가뿐히 넘기고, 두 페이지를 넘기고, 끝내 수백 줄에서 멈춘다. 직접 적은 의존성은 `spring-boot-starter-web`과 `spring-boot-starter-data-jpa` 두 줄이었는데, 그 두 줄이 끌어들인 transitive가 200개를 넘는 풍경이 펼쳐진다. 우리는 그중 단 하나의 jar도 직접 검증한 적이 없다. mavenCentral이 가져다 준 그 파일이 정말 우리가 의도한 그 파일인지, 누가 중간에서 손을 댄 건 아닌지, 그 안에 어떤 PostInstall 비슷한 게 들어 있는 건 아닌지, 우리는 모른다.

이 풍경이 평소엔 잘 안 보인다. `implementation("org.springframework.boot:spring-boot-starter-web")` 한 줄을 적으면 빌드가 돌고, 앱이 뜨고, 동료의 PR을 머지한다. 그렇게 운영까지 나간다. 어느 날 supply chain 사고 뉴스가 떨어진다. log4shell이든, ua-parser-js든, event-stream이든. 그날 우리는 처음으로 `dependencies` 출력을 끝까지 스크롤해보고 묻는다. **이 수백 개를 우리는 정말 신뢰하고 있었던 건가?**

이번 장은 그 질문에 도구 셋으로 답한다. Dependency Verification으로 "이 jar의 해시는 우리가 한 번 확인한 그 해시인가"를 잠그고, Dependency Locking으로 "오늘 빌드한 버전이 내일 빌드와 같은 버전인가"를 잠그고, Repository Content Filtering으로 "회사 내부 좌표는 외부 저장소를 절대 보지 못한다"를 잠근다. 셋 다 Gradle이 처음부터 들고 있던 도구지만, Spring Boot의 transitive 폭발 앞에서는 운영의 무게가 다르다. 그 무게를 솔직히 다루자.

## Dependency Verification — 한 번 본 jar의 해시를 잠근다

먼저 가장 본격적인 도구부터 보자. **Dependency Verification**은 모든 의존성 아티팩트에 대해 미리 기록된 SHA-256 해시(그리고 선택적으로 PGP 서명)와 빌드 시점에 받아온 파일의 해시를 대조한다. 다르면 빌드를 실패시킨다. 누군가 mavenCentral의 미러를 위변조했든, 사내 Nexus의 캐시가 손상됐든, 의존성 좌표를 살짝 비슷한 다른 이름으로 바꿔치기했든 — 잠긴 해시가 다르면 빌드가 멈춘다.

말은 거창한데, 도입은 한 줄이다.

```bash
./gradlew --write-verification-metadata sha256,pgp build
```

이 한 줄을 처음 돌리면 두 가지 일이 일어난다. 빌드가 정상적으로 도는 동안 Gradle이 사용된 모든 아티팩트의 SHA-256(가능하면 PGP 서명까지)을 모아 `gradle/verification-metadata.xml`이라는 파일에 적는다. 그게 부트스트랩의 결과물이다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<verification-metadata>
    <configuration>
        <verify-metadata>true</verify-metadata>
        <verify-signatures>false</verify-signatures>
    </configuration>
    <components>
        <component group="org.springframework.boot" name="spring-boot" version="4.0.6">
            <artifact name="spring-boot-4.0.6.jar">
                <sha256 value="a1b2c3..." origin="Generated by Gradle"/>
            </artifact>
            <artifact name="spring-boot-4.0.6.module">
                <sha256 value="d4e5f6..." origin="Generated by Gradle"/>
            </artifact>
        </component>
        <!-- 수백 개가 이어진다 -->
    </components>
</verification-metadata>
```

이 파일을 한 번 만들고 나면, 이후 모든 빌드는 받아온 jar의 해시가 이 파일과 같은지 검증한다. 한 줄이라도 다르면 빌드가 멈춘다. 우리가 한 번 본 jar의 모습이 그 jar의 정의가 되는 셈이다.

좋다. 그런데 이 부트스트랩에는 잊지 말아야 할 전제가 하나 있다. **`--write-verification-metadata`는 지금 우리 환경에서 받아온 산출물을 그대로 신뢰한다.** 즉 부트스트랩 시점의 mavenCentral이 정상이고, 사내 Nexus 캐시가 깨끗하고, 누구도 중간에서 손을 대지 않았다는 가정 위에서 metadata를 만든다. 만약 이미 망가진 환경에서 부트스트랩을 돌리면 그 망가진 해시가 그대로 잠겨버린다. **부트스트랩은 깨끗한 환경에서, 신뢰할 수 있는 사람의 손으로 한 번에 해야 한다.** 가능하면 깨끗한 CI 러너 한 대를 잡고, network mirror 설정을 점검하고, 그 위에서 돌리는 편이 낫다. 자기 노트북에서 PostInstall 후 한 달 만에 처음 돌리는 부트스트랩은 찜찜하다.

검증의 강도는 세 가지 모드로 조절한다. 기본은 `strict` — 다르면 즉시 실패. `lenient` — 경고만 찍고 빌드는 계속. `off` — 검증을 끈다. 운영 가이드는 단순하다. **CI는 strict, 부트스트랩과 업데이트 PR은 lenient.** 이 두 줄이 거의 모든 운영 결정의 정답이다. CI에서 strict가 아니면 검증이 켜져 있는 의미가 없다. 반대로 의존성을 한 번에 100개씩 갱신하는 PR에서 strict면 작업자가 비명을 지른다. 작업자가 자기 PC에서 `-Dorg.gradle.dependency.verification=lenient`로 돌려서 metadata를 새로 모으고, 그걸 PR에 같이 넣고, CI는 strict로 검증한다. 이게 표준 흐름이다.

이쯤에서 솔직해질 차례다. **Dependency Verification을 Spring Boot 프로젝트에 처음 도입하면 충격이 크다.**

부트스트랩 직후 `verification-metadata.xml`을 열어보면, 단순한 web 앱이라도 파일이 수백 줄, 보통은 천 줄을 넘는다. spring-boot-starter-web 하나에 transitive 50개가 따라오고, 거기 각 좌표마다 jar 해시와 module 해시가 두 줄씩 들어간다. PR에 이 파일이 처음 올라가면 리뷰어가 화면을 보고 한숨을 쉰다. 의존성을 하나만 추가해도 이 파일이 같이 변경된다. PR 차분(diff)에서 한 줄짜리 의존성 변경이 30줄짜리 metadata 변경과 함께 따라온다. 이게 처음에는 정말 번거롭다.

그리고 또 하나. **모든 의존성이 PGP 서명을 제공하지는 않는다.** `verify-signatures`를 true로 켜면, 서명이 없는 의존성은 SHA-256 체크섬으로 fallback해서 검증한다. 서명까지 잠그고 싶다는 선의가 실무에서 부분적으로만 작동한다는 뜻이다. PGP 서명이 있는 의존성에는 가치가 분명하지만, "모든 의존성에 PGP가 있을 거다"라는 기대는 빠르게 접는 편이 낫다. 우리가 잠그는 것의 대부분은 SHA-256이다.

> **함정 박스 — `./gradlew build --refresh-dependencies`로 의존성을 갱신한다는 오해**
>
> `--refresh-dependencies`는 의존성 갱신 도구처럼 자주 오용된다. 이름 때문이다. 그런데 이 옵션은 단지 "Gradle의 로컬 캐시를 무시하고 원격 저장소를 다시 확인하라"는 신호일 뿐이다. lockfile이나 verification-metadata.xml을 갱신하지는 않는다. **오히려 두 파일과 충돌해 빌드를 깨뜨릴 수 있다.** 의존성을 정말로 갱신하고 싶다면 `--write-locks`와 `--write-verification-metadata`가 정답이다. `--refresh-dependencies`는 "원격 변동을 의심할 때만" 쓰는 디버깅 도구로 남겨두자. 매 빌드 스크립트에 `--refresh-dependencies`가 박혀 있는 CI 워크플로우를 종종 본다. 그 워크플로우는 lockfile을 도입하는 순간부터 매 빌드가 빨갛게 된다. 기억해두자.

## Dependency Locking — 오늘과 내일이 같은 버전이도록

해시를 잠그는 일과 별개로 잠가야 할 게 또 있다. **버전 자체**다.

Spring Boot의 BOM이 거의 모든 버전을 고정해주지만, transitive 한 줄을 들여다보면 `1.4.+`나 `[1.0, 2.0)` 같은 동적 버전 표기가 가끔 보인다. 잘 알려진 라이브러리들이 가끔 그렇다. 그리고 dependency resolution이 늘 결정적이지는 않다. 같은 빌드 스크립트라도 새 transitive가 어제 release되면 오늘 받은 버전이 어제와 다를 수 있다. 5장에서 우리는 Version Catalog로 직접 선언한 좌표의 버전을 단일 출처에 모았다. 하지만 그 출처가 잡지 못하는 깊은 transitive가 있다. Dependency Locking은 그 빈 자리를 메운다.

설정은 두 줄이다. settings 레벨이 아니라 build 스크립트 — 보통은 10장에서 만든 convention plugin 한 곳에 박는다.

```kotlin
// buildSrc/src/main/kotlin/shop.java-conventions.gradle.kts
import org.gradle.api.artifacts.dsl.LockMode

dependencyLocking {
    lockAllConfigurations()
    lockMode = LockMode.STRICT
}
```

`lockAllConfigurations()`는 이름 그대로 모든 configuration의 의존성을 잠근다. `lockMode = STRICT`는 lockfile이 없는데 lock된 configuration이 해결되면 실패시킨다. **lock된 configuration은 반드시 lockfile이 있는 상태에서만 해결될 수 있다**는 안전장치다. 두 줄이 들어가면 빌드를 한 번 돌릴 때 빨간 메시지가 뜬다. 아직 lockfile이 없기 때문이다.

부트스트랩은 한 줄이다.

```bash
./gradlew dependencies --write-locks
```

이 줄을 돌리면 모든 configuration의 해결된 버전이 `gradle.lockfile`이라는 단일 파일에 모인다. 모듈마다 따로 만들어지는 게 아니라 프로젝트 루트 또는 각 모듈 디렉터리에 한 파일이다. 안에는 `group:name:version=configurationA,configurationB` 형식의 한 줄이 의존성 수만큼 들어 있다.

```
# This is a Gradle generated file for dependency locking.
# Manual edits can break the build and are not advised.
# This file is expected to be part of source control.
ch.qos.logback:logback-classic:1.5.18=runtimeClasspath,testRuntimeClasspath
org.springframework.boot:spring-boot:4.0.6=compileClasspath,runtimeClasspath,...
org.springframework:spring-core:7.0.6=compileClasspath,runtimeClasspath,...
# 수백 줄
empty=annotationProcessor
```

이 파일을 커밋한다. 그 다음부터는 `./gradlew build`가 이 파일에 적힌 버전과 정확히 같은 버전을 해결하지 못하면 실패한다. 오늘과 내일이 같은 버전을 본다는 약속이 잠긴다.

업데이트는 두 가지 방식이다.

```bash
# 전체 lockfile 새로 쓰기 — 보통 분기당 한 번, 주기적 maintenance PR
./gradlew dependencies --write-locks

# 부분 갱신 — Spring Boot만 새 버전으로 띄우고 나머지는 그대로
./gradlew dependencies --update-locks 'org.springframework:*'
```

부분 갱신을 쓰는 편이 실무에서는 훨씬 자연스럽다. 한 라이브러리를 갱신하고 싶은데 그 김에 lockfile 전체가 새 버전으로 흔들리는 건 PR 리뷰의 악몽이다. `--update-locks '<group>:<name>'` 패턴으로 좌표 단위 갱신을 하자. wildcard도 잘 작동한다.

여기서 운영의 무게가 한 단계 더 올라간다. **Dependabot은 lockfile은 지원하지만, verification-metadata.xml은 아직 지원하지 않는다.** Dependabot이 spring-boot의 새 patch 버전을 발견해서 PR을 열어주면, `gradle.lockfile`은 봇이 같이 갱신한 채로 PR이 올라온다. 그런데 `verification-metadata.xml`은 봇이 손을 못 댄다. 그 PR을 머지하면 CI가 strict 모드에서 검증에 실패한다. 봇이 갱신해준 jar의 해시가 metadata에 없기 때문이다.

이걸 현실적으로 풀어내는 운영 방식은 보통 두 가지다.

첫 번째, **사람이 lenient 모드로 metadata를 재생성한 뒤 봇의 PR 위에 commit을 얹어 올린다.** 가장 정직한 방식이다. 봇이 만든 PR에 사람이 한 commit을 더 얹는다. 작업자 PC에서 `./gradlew --write-verification-metadata sha256 build`를 돌리면 새 jar의 해시가 자동으로 metadata에 들어간다. 그걸 같이 푸시한다. PR 리뷰는 metadata 차분(diff)을 같이 본다.

두 번째, **CI 워크플로우 자체가 metadata도 같이 갱신하도록 잡아준다.** Dependabot PR이 열리면 워크플로우 한 단계가 `--write-verification-metadata sha256`을 돌리고 그 차분을 같은 PR에 다시 push한다. 자동화가 가능하지만, 봇이 봇 위에 commit을 얹는 셀프-체이닝의 부담이 있어 작은 팀에서는 첫 번째 방식이 더 안전하다.

어느 쪽이든 결론은 같다. **Dependabot이 lockfile만 지원한다는 한계를 우리가 운영 절차로 메워야 한다.** 이건 도구의 미완성이고, 우리는 그 미완성 위에서 실무를 한다. 솔직히 다소 번거롭다. 그렇지만 이 번거로움의 대가로 우리는 transitive 폭발 위에서도 supply chain 사고의 신호를 자동으로 받게 된다. 거래는 나쁘지 않다.

## Repository Content Filtering — 어느 좌표는 어느 저장소만 본다

세 번째 도구는 결이 조금 다르다. Dependency Verification과 Locking이 "받아온 jar"를 단속한다면, **Repository Content Filtering은 "받아오는 경로"를 단속한다.**

8장에서 우리는 `dependencyResolutionManagement`를 settings 레벨에서 처음 만났다. 그때 우리는 모든 모듈이 동일한 저장소 목록을 보게 만들었고, `RepositoriesMode.FAIL_ON_PROJECT_REPOS`로 모듈마다 다른 repository를 적는 안티패턴을 막았다. 그건 일관성 차원의 정리였다. 16장에서는 같은 자리를 보안 관점으로 다시 본다.

Spring Boot 빌드의 settings는 보통 이런 모습이다.

```kotlin
// settings.gradle.kts
dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories {
        mavenCentral()
        maven("https://nexus.example.com/internal")
    }
}
```

mavenCentral과 사내 Nexus 두 곳이다. 의존성을 요청하면 두 저장소에서 같은 좌표를 둘 다 찾아본다. 같은 좌표가 두 곳에 모두 있으면 보통 선언 순서가 우선하지만, 그 동작은 우리가 매일 의식하지 않는다. 그리고 여기서 두 가지 위험이 살짝 고개를 든다.

**첫째, 내부 좌표의 외부 누출.** 회사 내부에서만 쓰는 좌표 `com.example.shop:domain-core`를 외부 mavenCentral에도 같은 이름으로 누군가가 publish해 둔다면 어떻게 될까. 우리는 사내 Nexus에서 받기를 기대하지만, Gradle은 그 좌표를 양쪽 저장소에서 모두 탐색한다. 시점에 따라 mavenCentral의 같은 이름 가짜 좌표를 받을 수도 있다. 이 시나리오가 바로 dependency confusion 공격이고, 실제로 큰 회사 사고가 여러 번 있었다.

**둘째, 타입스쿼팅.** 우리가 의도한 게 `commons-lang3`인데 손가락이 미끄러져 `commons-langs3`라고 적었다고 하자. 누군가가 mavenCentral에 같은 이름으로 악성 좌표를 올려둔 적이 있다면 그게 들어온다. 사내 Nexus만 보던 시절에는 일어날 수 없는 종류의 사고였지만, mavenCentral을 같이 보는 순간 가능해진다.

Repository Content Filtering이 이 두 위험을 정확히 닫는다. 방식은 단순하다. **각 저장소에 "어느 좌표를 받을 수 있는지"를 명시한다.** mavenCentral은 회사 그룹을 절대 보지 않고, 사내 Nexus는 회사 그룹만 본다. 두 줄이 추가된다.

```kotlin
// settings.gradle.kts
dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories {
        mavenCentral {
            content {
                excludeGroup("com.example")           // 회사 그룹은 mavenCentral에서 절대 안 받는다
                excludeGroupByRegex("com\\.example\\..*")
            }
        }
        maven("https://nexus.example.com/internal") {
            content {
                includeGroup("com.example")           // 이 저장소는 회사 그룹만 받는다
                includeGroupByRegex("com\\.example\\..*")
            }
        }
    }
}
```

`excludeGroup`과 `includeGroup`은 정확히 짝이다. mavenCentral은 회사 그룹을 의도적으로 모르게 만들고, Nexus는 회사 그룹만 답하게 만든다. 두 저장소의 역할이 깔끔히 갈린다. dependency confusion이 닫히고, 회사 좌표를 우연히 외부에서 받는 풍경이 사라진다.

여기서 더 강하게 잠그는 도구가 `exclusiveContent`다. 이름 그대로 "이 좌표는 **오직** 이 저장소에서만 받아라."

```kotlin
exclusiveContent {
    forRepository {
        maven("https://nexus.example.com/internal")
    }
    filter {
        includeGroupByRegex("com\\.example\\..*")
    }
}
```

`exclusiveContent`를 쓰면 그 안에 적힌 좌표는 다른 저장소가 무엇을 답하든 무시한다. 회사 좌표의 출처를 한 군데로 못 박는 가장 단단한 방법이다. `include`/`exclude` 짝을 양쪽에 빠짐없이 적어주는 일이 부담스럽다면 `exclusiveContent`가 더 안전하다.

여기서 8장과의 회수가 자연스럽게 일어난다. 그때 우리는 일관성을 위해 settings 레벨에 repository를 모았다. 그 자리가 지금 그대로 보안 정책의 자리이기도 하다. 회사 그룹 정책을 한 곳에서 선언하니, 멀티 모듈의 어느 한 모듈이 `repositories { mavenCentral() }`을 따로 적어 정책을 우회하는 일이 처음부터 막힌다. `FAIL_ON_PROJECT_REPOS`가 그걸 강제했기 때문이다. **8장의 일관성이 16장의 보안으로 그대로 흘러든다.** 같은 두 줄이 두 가지 무게를 동시에 지고 있다.

## 셋을 같이 켜면 일어나는 일

여기까지의 도구 셋 — verification, locking, content filtering — 을 모두 켠 `ch16-security/`의 settings/build는 다음 모습이 된다.

```kotlin
// settings.gradle.kts
pluginManagement {
    repositories {
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode = RepositoriesMode.FAIL_ON_PROJECT_REPOS
    repositories {
        mavenCentral {
            content {
                excludeGroupByRegex("com\\.example\\..*")
            }
        }
        maven("https://nexus.example.com/internal") {
            content {
                includeGroupByRegex("com\\.example\\..*")
            }
        }
    }
}

rootProject.name = "shop"
include(":app", ":domain", ":order", ":payment")
```

```kotlin
// buildSrc/src/main/kotlin/shop.java-conventions.gradle.kts
import org.gradle.api.artifacts.dsl.LockMode

plugins {
    java
}

dependencyLocking {
    lockAllConfigurations()
    lockMode = LockMode.STRICT
}
```

그리고 프로젝트에는 두 종류의 새 산출물이 산다.

```
shop/
├── gradle/
│   ├── verification-metadata.xml   # 모든 jar의 SHA-256 해시
│   └── libs.versions.toml
├── app/
│   ├── build.gradle.kts
│   └── gradle.lockfile             # app 모듈의 모든 configuration의 해결된 버전
├── domain/
│   ├── build.gradle.kts
│   └── gradle.lockfile
└── settings.gradle.kts
```

`gradle.lockfile`은 모듈별로 하나씩 생긴다. `verification-metadata.xml`은 빌드 전체에 하나다. 둘 다 소스 컨트롤에 들어간다. 둘 다 PR 리뷰의 대상이 된다.

이제 다음 풍경이 펼쳐진다. 누군가 의존성 한 줄을 추가하는 PR을 연다. `gradle.lockfile`에 새 줄이 들어가고, `verification-metadata.xml`에 새 component가 들어간다. 둘 다 차분(diff)으로 보인다. 리뷰어가 어떤 좌표가 어느 버전으로 들어왔는지, 그 jar의 해시가 무엇인지 정확히 본다. supply chain의 변동이 코드 변경과 같은 자리에 묶인다. 일주일 뒤 mavenCentral의 어떤 미러가 손상돼도, 우리 빌드의 해시가 같지 않으니 CI가 멈춘다. 6개월 뒤 누군가 회사 좌표와 같은 이름의 외부 좌표를 mavenCentral에 publish해도, 우리 mavenCentral은 회사 그룹을 보지 않게 잠겨 있으니 의존성 해결이 그쪽으로 흘러가지 않는다.

대신 우리 PR의 차분이 길어진다. 의존성 갱신은 더 의례적인 작업이 된다. 부트스트랩 한 번의 비용이 처음에 크다. `--refresh-dependencies` 같은 단어가 입에 붙어 있던 동료는 한 번씩 비명을 지른다.

**이 거래가 가치 있는가?** 답은 빌드의 운영 무게에 달려 있다. 사내에서만 도는 작은 앱이라면 셋 다 켜는 부담이 과할 수도 있다. 그런데 결제를 다루거나, 외부 데이터를 받거나, 운영의 가시성이 중요한 앱이라면 — 우리가 부분적으로라도 이 도구들을 들이기 시작한 순간이, 사고 한 번을 미리 막은 순간일 가능성이 높다. 그 사고가 일어난 후에 같은 도구를 도입하는 비용은 비교할 수 없이 크다.

## 실전 운영의 다섯 가지 정착 패턴

마지막으로 책의 앞 챕터들과 자연스럽게 짝을 이루는 실전 패턴 몇 개를 정리하자. 이건 셋을 켤지 말지가 아니라, 어떻게 켜야 PR 리뷰가 지치지 않는가의 문제다.

**(1) lockfile만 먼저, verification은 그 다음.** 셋을 한꺼번에 켜지 말자. lockfile은 PR 차분(diff)이 비교적 작고, Dependabot이 알아서 갱신해준다. lockfile을 먼저 한 분기 운영해서 팀이 적응한 다음 verification을 켜자. content filtering은 시간이 별로 들지 않으니 가장 먼저 켜도 좋다.

**(2) verification은 sha256만, signature는 나중.** 처음에는 `--write-verification-metadata sha256`로만 부트스트랩하자. `verify-signatures`를 true로 켜면 PGP 키 trust 관리라는 새로운 운영 영역이 따라 들어온다. SHA-256 잠금만으로 가장 큰 위험을 닫는다. signature는 한 분기 뒤에.

**(3) CI strict, 로컬 lenient.** CI에서는 strict가 정답이다. `./gradlew build`가 검증에 실패하면 PR이 빨갛게 변한다. 한편 로컬에서는 작업자가 의존성을 갱신할 때 lenient로 돌리고 싶다. `gradle.properties`에 `org.gradle.dependency.verification=strict`를 박아두지 말고, CI 환경 변수로 strict를 강제하고 로컬은 기본값을 lenient로 두는 식이 자연스럽다. 작업자가 자기 PC에서 `-Dorg.gradle.dependency.verification=lenient`를 매번 적기보다는 환경 설정으로 분리하자.

**(4) lockfile 갱신은 약속된 주기로.** Dependabot이 patch 단위로 PR을 매일 열어주는 한편, 작업자가 의존성을 직접 손대는 일은 보통 분기당 한 번 정도다. 그 갱신은 약속된 주기 — 분기 maintenance 윈도우 — 에 한 번씩 `./gradlew dependencies --write-locks`를 돌려서 lockfile 전체를 새로 쓰는 편이 낫다. 일상 PR에서는 부분 갱신 `--update-locks '<group>:<name>'`만 쓴다. 두 모드를 의식적으로 구분하자.

**(5) `--refresh-dependencies`를 빌드 스크립트에서 쫓아내자.** CI 워크플로우의 `./gradlew build --refresh-dependencies` 한 줄이 lockfile을 도입한 순간부터 빌드를 깬다. 캐시 디버깅이 필요할 때만 손으로 한 번 돌리는 옵션으로 남겨두자. 워크플로우에 박혀 있다면 빼자.

이 다섯 가지가 우리가 결국 도착하는 자리다. 시작은 두 줄, 도착은 다섯 가지 운영 패턴.

## 마무리

이번 장에서 우리는 Spring Boot의 transitive 폭발 앞에서 "이 수백 개를 우리는 정말 신뢰하고 있는가"라는 질문에 도구 셋으로 답했다. Dependency Verification으로 jar의 해시를 잠그고, Dependency Locking으로 버전을 잠그고, Repository Content Filtering으로 좌표가 흘러가는 경로를 잠갔다. 셋 다 도입 비용이 있고, 부트스트랩의 위생이 중요하고, Dependabot과의 호환에서 한 발 모자란 자리가 있다. 우리는 그 모자란 자리를 운영 절차로 메우는 거래를 받아들였다. 거래의 대가는 supply chain 사고 한 번을 미리 막을 가능성이다.

8장에서 settings 레벨로 모았던 `dependencyResolutionManagement`가 그대로 보안 정책의 자리였다는 사실도 다시 확인했다. 일관성을 위해 만든 자리가 보안의 자리가 되었다. 빌드 도구의 좋은 도구들은 종종 이렇게 한 자리에서 여러 무게를 같이 진다.

다음 17장에서는 회사의 8.x(또는 7.x) 빌드를 9.x로 옮기는 마이그레이션 노트를 모은다. 이번 장에서 만난 verification/locking 같은 도구도 9.x에서 일부 동작이 다듬어졌다. 그 변화를 포함해서, 우리의 가상 앱 `shop`을 옛 버전 빌드에서 9.5로 한 단계씩 올리는 일지를 같이 따라가보자.

# 17장. Gradle 9.x로 옮긴다 — 마이그레이션 노트 모음

회사에 7년 된 Spring Boot 빌드가 하나 있다고 해보자. 처음 만들 때는 Gradle 5.x였다. 누군가 한 번 6으로 올렸고, 또 다른 누군가가 7로 올렸고, 8.4쯤에서 멈춰 있다. 지금 그 빌드를 9.5로 올리라는 임무가 떨어졌다. 한 줄짜리 명령으로 끝났으면 좋겠지만, 우리가 아는 한 그렇지 않을 것이다. 어디부터 깨질지 짐작도 잘 안 간다.

이런 상황은 흔하다. 그리고 솔직히 말해서, **회사 빌드를 9로 옮기는 일은 1주차에 끝나지 않는다.** 1장에서 "8.x를 쓰는 분께"라는 박스로 미뤄둔 약속이 있다. 마이그레이션 체크리스트는 17장에서 다룬다고 했다. 그 약속을 회수할 때다. 다만 여기서 한 가지를 분명히 하고 시작하자. 이 장은 **Gradle 버전 마이그레이션**에 대한 장이다. Spring Boot 3.x에서 4.x로 옮기는 일은 6장에서 이미 다뤘다. 둘은 자주 같이 다가오지만 별개의 일이고, 별개로 진행해야 디버깅이 쉽다.

> **두 마이그레이션의 역할 분담**
> - **6장 — Spring Boot 3.x → 4.x:** Boot 플러그인의 task 시그니처, Paketo builder 기본값, AOT/Native 동작, Spring 측이 요구하는 Gradle 최소 버전(8.14+).
> - **17장 — Gradle 8.x/7.x → 9.5:** Daemon JDK 요구, 제거된 API, archive reproducibility, Configuration Cache, 그리고 third-party plugin 호환성.
>
> 둘을 한 PR에 묶지 말자. 한 번에 한 가지만 옮긴다. 깨지면 어느 마이그레이션이 깬 건지 즉시 안다.

이 장의 흐름은 이렇다. 먼저 Gradle 9.0이 가져온 진짜 큰 변화들을 정리한다. 그 다음 9.1~9.5의 작은 변화 중 마이그레이션 시 도움이 되는 것들을 본다. 그리고 step-by-step 절차를 따른다 — wrapper 올리고, 빌드 깨지고, 메시지 읽고, 가장 자주 깨지는 다섯 가지를 처방한다. 마지막으로 우리 가상 앱 `shop`을 7.x 시절의 가상 빌드로 되돌렸다가 9.5로 다시 올리는 일지를 본다.

## 9.0이 진짜로 가져온 것 — 큰 망치들

9.x 라인 안에서 9.1, 9.2, 9.3은 사실 부드러운 변화들이다. 정작 칼을 휘두른 건 9.0이다. 9.0에서 결정된 변화들이 8.x 빌드를 깨는 거의 모든 원인이다. 여섯 가지로 묶어보자.

### Daemon JDK 17+ 필수

이게 가장 먼저 닿는 벽이다. **Gradle 9.x의 데몬은 JDK 17 이상에서만 돈다.** 8.x는 JDK 8로도 데몬을 띄울 수 있었지만 9.x는 아니다. CI 머신에 JDK 11이 깔려 있고 `JAVA_HOME`이 거기 박혀 있다면, 9.x로 wrapper를 올린 순간 빌드가 시작도 못 한다.

여기서 헷갈리지 말아야 할 게 있다. **데몬 JDK와 빌드 대상 JDK는 다르다.** 데몬은 Gradle 자기 자신이 도는 JVM이다. 빌드 대상 JDK는 우리 앱을 컴파일하는 JDK다. 9.x의 요구는 데몬 JDK다. 우리 앱은 여전히 JDK 21로 컴파일할 수도, JDK 17로 컴파일할 수도 있다. 4장에서 정착시킨 toolchain이 이걸 정확히 처리해준다.

```kotlin
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

데몬은 17로 돌고, 컴파일은 21로 한다. toolchain을 4장에서 박아둔 빌드라면 이 변화는 거의 무료다. 박아두지 않았다면 9.x 마이그레이션과 함께 toolchain을 박는 게 좋다 — 미루지 말자.

### `jcenter()` 제거

`jcenter()`가 마침내 사라졌다. JFrog가 2021년에 read-only 상태로 만든 이후 이미 5년 가까이 deprecation 신호가 있었지만, 9.0에서 마침내 빌드 스크립트에서 호출 자체가 불가능해졌다. settings나 build script에 아직 `jcenter()`가 남아 있다면 9.x에서 즉시 빌드 실패다.

```kotlin
// Before — 9.x에서 더 이상 동작하지 않는다
repositories {
    jcenter()
}

// After
repositories {
    mavenCentral()
}
```

대부분의 라이브러리는 Maven Central에 그대로 있다. `jcenter`에만 있고 Central엔 없는 것이 있다면, 그건 이미 유지보수가 끊긴 라이브러리일 가능성이 높다. 이 기회에 의존성을 한번 정리하자.

### `Project#exec` / `Project#javaexec` 제거

8장에서도 미리 한 번 봤지만, 다시 정리하자. Gradle 8.x는 `Project#exec { ... }`나 `Project#javaexec { ... }`를 deprecation 경고로만 띄워줬다. 9.x는 아예 메서드를 지웠다.

```kotlin
// Before — 9.x에서 메서드 자체가 없다
val gitSha = project.exec {
    commandLine("git", "rev-parse", "HEAD")
    standardOutput = ByteArrayOutputStream().also { /* ... */ }
}

// After — providers.exec 로 옮긴다
val gitSha: Provider<String> = providers.exec {
    commandLine("git", "rev-parse", "HEAD")
}.standardOutput.asText.map { it.trim() }
```

이 변화는 단순한 API 교체가 아니다. `Project#exec`는 **즉시 실행**이었다. configuration phase에서 호출되면 그 자리에서 git 명령이 돌았다. 그러니 Configuration Cache와는 본질적으로 양립할 수 없었다. `providers.exec`는 **lazy provider**다. 실제로 값이 필요한 시점까지 실행을 미루고, 그 결과는 Configuration Cache에 안전하게 직렬화된다.

이 차이는 12장에서 우리가 `shop.build-info` 플러그인을 만들 때 이미 만났다. 12장의 그 패턴이 9.x 시대의 표준이다. 거기서 익혔던 `providers.exec { }.standardOutput.asText.map { ... }` 한 줄이 마이그레이션의 답이기도 하다.

### Convention API 완전 제거

이게 빌드 스크립트보다는 **third-party plugin**에 더 큰 영향을 주는 변화다. Gradle 7부터 deprecated 였던 `project.convention` API와 `SourceSetConvention` 같은 옛 모델이 9.0에서 완전히 제거됐다. 그 자리에 들어선 게 우리가 줄곧 써온 **Extensions** 모델이다.

빌드 스크립트 입장에선 큰 영향이 없다. 우리는 이미 `java { ... }`, `kotlin { ... }`, `application { ... }` 같은 extension 블록으로 일하고 있다. 문제는 **오래된 plugin**이다. 사내에서 쓰는 자작 plugin이 5~6년 전에 쓰여졌고, 그동안 손길이 안 닿았다면 `project.convention.getPlugin(...)` 같은 호출이 남아 있을 가능성이 높다. 그게 9.x에서 빌드를 깬다.

처방은 간단하다. plugin 코드를 열어서 `convention.getPlugin(...)` 같은 호출을 `extensions.getByType(...)`로 바꾸는 것. 다만 그 plugin이 오픈소스라면 이미 누군가 PR을 올렸을 가능성이 높다. **9.x 마이그레이션을 시작하기 전에 가장 먼저 할 일은, 우리가 쓰는 third-party plugin들의 최신 버전이 9.x를 지원하는지 점검하는 일이다.** 이건 뒤에서 다시 본다.

### KGP 2.0+ 필수

Kotlin DSL을 쓰고 있다면 — 그러니까 이 책의 모든 독자라면 — **Kotlin Gradle Plugin 2.0 이상이 필수**다. KGP 1.9에 머물러 있는 빌드는 9.x에서 안 돈다.

```toml
# gradle/libs.versions.toml
[versions]
kotlin = "2.2.0"

[plugins]
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }
```

5장에서 정착시킨 Version Catalog가 도움이 된다. catalog 한 곳에서 Kotlin 버전을 올리면 모든 모듈이 동시에 따라온다. 다만 KGP 2.0은 K2 컴파일러를 기본으로 쓰기 때문에, 우리 코드에서 일부 컴파일 오류가 새로 잡힐 수 있다. 이건 KGP의 책임이고, Kotlin 측에서 마이그레이션 가이드가 잘 정리돼 있다. Kotlin 2.1 이후엔 strict nullness가 더 엄격해진 것도 한 줄 기억해두자 — 이전엔 그냥 넘어가던 nullable 추론이 컴파일 오류로 바뀌는 경우가 있다.

### Archive task의 기본 reproducible

이게 가장 조용하면서도 가장 미묘하게 깨지는 변화다. 9.0부터 `Jar`, `Zip`, `Tar` 같은 archive task들이 **기본적으로 reproducible**하게 동작한다. 무슨 뜻인가?

reproducible archive란 같은 입력에 대해 항상 같은 바이트의 archive를 만든다는 뜻이다. 그러기 위해 두 가지를 기본으로 잡는다. **첫째, archive 안의 파일 타임스탬프를 모두 0(또는 고정값)으로 설정한다.** 둘째, **파일 순서를 alphabetical로 정렬한다.** 같은 코드를 빌드하면 어제와 오늘 만든 jar가 바이트 단위로 동일하다.

이건 거의 모든 경우에 좋은 변화다. Build Cache의 효율이 올라가고, 같은 소스에서 같은 image hash가 나오니 OCI 이미지 캐시도 안정적이다. 그런데 한 가지 경우에 깨질 수 있다. **빌드 스크립트나 도구가 jar 안의 파일 타임스탬프에 의존하고 있을 때.** 예를 들어 어떤 회사 도구가 jar를 받아서 "가장 최근 빌드된 파일이 어떤 것이냐"를 manifest의 타임스탬프로 판단한다면, 이제 그 타임스탬프가 모두 0이라 판단이 안 된다.

이 경우 대부분은 도구를 고치는 게 옳지만, 호환을 위해 일시적으로 옛 동작이 필요하다면 명시적으로 끄는 길이 있다.

```kotlin
tasks.named<Jar>("jar") {
    isPreserveFileTimestamps = true
    isReproducibleFileOrder = false
}
```

가능하면 끄지 말자. 이 변화 덕분에 13장의 Build Cache가 더 잘 동작한다.

## 9.1~9.5 — 작은 변화들이 마이그레이션을 돕는다

9.0이 칼을 휘둘렀다면 9.1부터 9.5까지는 **그 칼맞은 자리를 봉합하는** 작업이다. 마이그레이션할 때 직접 도움이 되는 것 위주로 본다.

9.1~9.4의 핵심 흐름은 두 가지다. **Configuration Cache 호환성이 단계적으로 개선됐고**, **진단 메시지가 더 명확해졌다.** 8.x에서 Configuration Cache를 켰을 때 받던 모호한 메시지 — "Some configuration cache problems were found" 만 띄우고 어디서 깨졌는지 알기 힘들었던 — 가 9.x를 거치면서 점차 정확해졌다. 9.3 이후로는 위반 메시지가 "이 task의 이 입력이 이런 이유로 위반"이라는 형식으로 좁아진다.

이게 마이그레이션의 실용적인 함의는 이렇다. **9로 먼저 옮기고 나서 Configuration Cache를 켜야 메시지가 명확하다.** 8.x에서 Configuration Cache를 켜고 9로 옮기려고 시도하면, 8.x의 모호한 메시지와 마이그레이션 깨짐이 섞여서 뭐가 진짜 원인인지 알기 어렵다. 13장에서 우리가 잡아둔 Configuration Cache는, 마이그레이션할 때 잠시 꺼뒀다가 9.5에 도착해서 다시 켜는 편이 낫다.

9.5에서 마이그레이션에 직접 도움이 되는 신규 기능들이 몇 가지 있다. 차례대로 짚자.

**Task provenance** — 빌드가 깨졌을 때 "이 task는 어느 plugin에서, 어느 script에서 등록됐는지"를 출력해준다. 8.x에서 빌드가 실패하면 "이 task가 어디서 왔는지 모르겠는데?" 하는 순간이 자주 있었다. 9.5는 답을 같이 띄워준다. 마이그레이션 중 third-party plugin이 일으킨 깨짐을 추적할 때 시간을 크게 아낀다.

**Wrapper retries** — 14장에서도 한 번 본 변화다. wrapper distribution 다운로드를 자동으로 재시도한다. CI에서 wrapper를 9.5로 올린 직후 잠깐 flaky한 실패가 늘 수 있는데, retries 한 줄로 진정된다.

**Precompiled Settings plugin type-safe accessor** — 10장에서 우리가 정착시킨 convention plugin의 sister 기능이다. project 수준 precompiled plugin은 이미 type-safe accessor가 있었지만, settings 수준은 그동안 string-based API로 떨어졌다. 9.5는 settings precompiled plugin에도 accessor를 만들어준다. 멀티 모듈에서 settings convention을 만들고 있다면 이전보다 훨씬 깔끔하다.

**`disallowChanges()`** — Property를 더 이상 못 바꾸게 잠그는 API다. plugin을 만들 때 "이 시점부터는 사용자가 이 값을 못 바꾼다"고 명시할 수 있다. 12장에서 만든 `shop.build-info` 같은 자작 plugin에 도움이 된다.

**`gradle init --into <dir>`** — 새 프로젝트를 빈 디렉터리에만 만들 수 있던 init이 이제 기존 디렉터리 안으로 파일을 풀어준다. 마이그레이션의 핵심은 아니지만, 새 모듈을 보탤 때 편하다.

**`--develocity-url` CLI** — Develocity URL을 CLI로 한 번에 전달할 수 있다. 사내 Develocity를 쓰는 팀이라면 마이그레이션 후 CI 스크립트가 한 줄 짧아진다.

> **마이그레이션 노트 — 9.0에서 사라진 옛 패턴**
>
> ```kotlin
> // Before (Gradle 7 이전 잔재)
> tasks.create("myTask") {       // eager — 9.x에서 동작은 하지만 권장 안 함
>     doLast { println("hi") }
> }
>
> // After
> tasks.register("myTask") {     // lazy — 정석
>     doLast { println("hi") }
> }
> ```
>
> 3장에서 lazy registration이 정석이라고 미리 약속했었다. 9.x에서 Convention API가 사라지면서, 12장에서 정착시킨 Provider/Property 표준화와 더불어 이 lazy 표준이 더 단단해졌다. eager 패턴이 남아 있는 회사 빌드라면 마이그레이션 PR과 함께 정리하는 게 좋다.

## Step-by-step — 빌드를 9.5로 옮기는 절차

이론은 충분히 봤다. 이제 실제로 옮긴다. 절차는 다섯 단계다.

### 1단계 — 이전 점검: third-party plugin 호환성

가장 먼저 할 일은 **빌드를 건드리지 않는 일**이다. 우리가 쓰는 plugin들이 9.x를 지원하는지 먼저 확인한다. 이걸 빼먹고 wrapper부터 올리면, 정작 깨진 게 우리 빌드 스크립트인지 third-party plugin인지 구분이 안 된다.

확인 방법은 단순하다. 우리 `libs.versions.toml`을 펴서 plugin과 의존성 중 빌드 도구 성격을 가진 것들 — Spring Boot Gradle Plugin, Kotlin Gradle Plugin, Spotless, Detekt, SonarQube plugin, JMH plugin, 사내 자작 plugin 등 — 의 release notes나 changelog에서 "Gradle 9 support"가 언급된 버전을 찾는다. **두 가지가 함께 잡혀야 한다.** Configuration Cache 호환과 Gradle 9.x 호환. 이게 같이 명시된 버전을 골라 catalog에 박는다.

```toml
[versions]
spring-boot = "4.0.6"
kotlin = "2.2.0"
spotless = "7.0.0"
detekt = "1.23.7"
```

특히 사내 자작 plugin이 있다면, 그 plugin의 코드를 한번 훑어보자. `project.convention`, `Project#exec`, `tasks.create`, `tasks.getByName` 같은 옛 패턴이 있다면 마이그레이션과 함께 정리해야 한다.

> **함정 박스 — Configuration Cache 호환과 Gradle 9 호환은 다르다**
> Configuration Cache 호환만 된다고 Gradle 9에서 자동으로 도는 게 아니다. 예를 들어 `Project#exec`만 쓰던 plugin은 Configuration Cache에선 동작했었지만(deprecation 경고만 떠 있었음) Gradle 9에서는 메서드 자체가 없으니 즉시 실패한다. **두 가지를 모두 확인하자.**

### 2단계 — wrapper 업그레이드

이제 칼을 뽑는다. 한 줄이다.

```bash
./gradlew wrapper --gradle-version 9.5 --distribution-type=bin
```

`--distribution-type=bin`은 14장에서 정한 표준이다. 잊지 말자. 이 명령은 `gradle/wrapper/gradle-wrapper.properties`의 `distributionUrl`만 9.5로 바꾼다. 다음 빌드부터 9.5가 자동으로 받아진다.

그리고 이 wrapper 변경을 **별도의 한 PR로 박자.** 빌드 스크립트 변경과 섞지 말자. 이 PR이 깨지면 깨진 채로 머지하지 말고, 어디까지 깨졌는지 본다. 이게 마이그레이션의 출발선이다.

### 3단계 — 빌드 실패 메시지 읽기

`./gradlew build`를 돌려본다. 거의 확실히 어딘가에서 깨진다. 9.x의 메시지는 8.x보다 훨씬 친절해졌으니, **메시지를 끝까지 읽자.** 다음 몇 가지 패턴을 자주 본다.

```
> Could not resolve all artifacts for configuration ':compileClasspath'.
   > Cannot resolve external dependency com.example:foo because no repositories are defined.
```

`jcenter()`를 지웠는데 거기에만 있던 의존성이 있을 때 나오는 메시지다. 의존성 좌표를 확인하고, Maven Central에 있는지 본다. 없다면 그 라이브러리가 이미 EOL이다.

```
> Unresolved reference: convention
```

자작 plugin의 코드가 `project.convention.getPlugin(...)`을 쓰고 있을 때 나오는 메시지다. `extensions.getByType<JavaPluginExtension>()` 같은 형태로 옮긴다.

```
> Cannot use 'project.exec' from outside of a configured execution.
```

(혹은 메서드 자체가 없다는 컴파일 오류.) `Project#exec` 호출이 남아 있다. `providers.exec { }`로 옮긴다 — 12장의 패턴 그대로다.

```
> Unsupported class file major version 65
```

JDK 17 미만으로 데몬을 띄우려 했을 때 나는 메시지다. `JAVA_HOME`을 확인하고, CI라면 `actions/setup-java@v5`의 `java-version`을 17 이상으로 올린다. 우리 앱은 toolchain으로 계속 21에 머무를 수 있다.

### 4단계 — 가장 자주 깨지는 다섯 가지 처방

수십 개의 마이그레이션 사례를 압축하면 가장 자주 깨지는 자리는 다섯 군데로 좁혀진다. 표로 정리하자.

| # | 깨지는 자리 | 증상 | 처방 |
|---|---|---|---|
| 1 | `Project#exec` / `Project#javaexec` | `Unresolved reference: exec`(혹은 컴파일 실패) | `providers.exec { commandLine(...) }.standardOutput.asText.map { it.trim() }` |
| 2 | `jcenter()` | dependency resolution 실패 | `mavenCentral()`로 교체. 없는 의존성은 EOL이다 |
| 3 | `tasks.create` / `getByName` eager | deprecation 경고 더미 (실패는 아님) | `tasks.register` / `named<T>(...)` 로 교체. 마이그레이션 끝나고 한 번에 정리 |
| 4 | 자작 plugin의 Convention API | `Unresolved reference: convention` | `project.extensions.getByType<...Extension>()` 로 교체 |
| 5 | Archive 타임스탬프 의존 도구 | 외부 도구가 jar 내부 timestamp로 판단 실패 | 도구를 고치는 게 옳다. 임시 호환은 `isPreserveFileTimestamps = true` |

이 표가 회사 빌드를 옮길 때 첫 1주의 절반을 단축해준다. 깨진 메시지를 받으면 이 표부터 보자.

### 5단계 — Configuration Cache를 다시 켠다

마이그레이션 PR에서 잠시 꺼뒀던 Configuration Cache를 9.5에서 다시 켠다.

```properties
# gradle.properties
org.gradle.configuration-cache=true
org.gradle.configuration-cache.problems=warn
org.gradle.configuration-cache.parallel=true
```

13장에서 다듬어둔 그대로다. 9.x의 진단 메시지가 8.x보다 훨씬 명확하니, 혹시 8.x에서는 "이상한데 동작은 하던" 코드가 있었다면 9.5에서 깨끗하게 잡힐 수 있다. 잡히는 위반은 13장의 처방대로 하나씩 정리한다. 그리고 `problems=warn`을 `=fail`로 옮긴다.

## 회고 — `shop` 앱의 7.x 시절로 돌아가본다

이론과 절차를 봤으니 우리 가상 앱 `shop`으로 한 번 시뮬레이션해보자. 이 책이 9.5 기준으로 자라왔지만, 만약 같은 앱을 7.x 시절에 만들었다면 어떤 모양이었을까. 그 코드를 9.5로 옮기는 과정을 짧은 일지로 본다.

7.x 시절의 `shop`은 대략 이렇게 생겼을 것이다.

```kotlin
// settings.gradle.kts (7.x 시절)
rootProject.name = "shop"
include("app", "domain", "order", "payment")

// 의존성 repo는 각 모듈에서 따로 선언
```

```kotlin
// app/build.gradle.kts (7.x 시절)
import java.io.ByteArrayOutputStream

plugins {
    id("org.springframework.boot") version "2.7.18"
    id("io.spring.dependency-management") version "1.1.4"
    kotlin("jvm") version "1.9.10"
    kotlin("plugin.spring") version "1.9.10"
}

repositories {
    mavenCentral()
    jcenter()  // 여전히 살아 있던 시절
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation(project(":domain"))
}

dependencyManagement {
    imports {
        mavenBom("org.springframework.boot:spring-boot-dependencies:2.7.18")
    }
}

tasks.create("printGitSha") {
    doLast {
        val out = ByteArrayOutputStream()
        project.exec {
            commandLine("git", "rev-parse", "HEAD")
            standardOutput = out
        }
        println(out.toString().trim())
    }
}
```

이 빌드를 9.5로 옮기는 일지다.

**Day 1 — 점검.** 먼저 plugin들의 9.x 호환 버전을 본다. Spring Boot는 4.0.6, Kotlin은 2.2.0이 9.x 라인을 지원한다. 우리는 Spring Boot 3.x → 4.x도 같이 옮길 게 아니라, **이번 PR은 Gradle만** 옮기기로 한다. Spring Boot는 일단 3.5.x(유지보수 라인)에 머물러도 9.x와 호환된다는 점을 확인했다 — 두 마이그레이션을 분리한다.

**Day 2 — wrapper.** `./gradlew wrapper --gradle-version 9.5 --distribution-type=bin` 한 줄. 별도 PR로 박는다. `./gradlew build`를 돌리면 빨갛게 깨진다.

**Day 3~4 — 메시지 한 줄씩.** 4단계의 표를 옆에 두고 깨진 곳을 하나씩 본다.

- `jcenter()`가 첫 번째로 잡힌다. Maven Central에 있는 의존성만 우리 빌드에 들어 있으니 `jcenter()` 한 줄만 지운다.
- `Kotlin Gradle Plugin 1.9 incompatible`이 두 번째로 잡힌다. catalog로 Kotlin을 2.2.0으로 올린다. `kotlin("plugin.spring")`도 같이 올라온다.
- `project.exec`가 세 번째로 잡힌다. 위의 `printGitSha` task를 다시 짠다.

```kotlin
// After — providers.exec 로 옮긴다
abstract class PrintGitShaTask : DefaultTask() {
    @get:Input
    abstract val gitSha: Property<String>

    @TaskAction
    fun run() {
        println(gitSha.get())
    }
}

tasks.register<PrintGitShaTask>("printGitSha") {
    gitSha = providers.exec {
        commandLine("git", "rev-parse", "HEAD")
    }.standardOutput.asText.map { it.trim() }
}
```

12장의 패턴 그대로다. 그리고 `tasks.create`도 같이 `tasks.register`로 바꾼다.

- 네 번째로 IDE에서 Kotlin 2.2의 strict nullness가 옛 코드 한두 줄을 잡는다. nullable 타입을 명시한다. 이건 KGP 2.0 마이그레이션 가이드의 영역이다.

**Day 5 — Configuration Cache.** `org.gradle.configuration-cache=true`를 켠다. `problems=warn`으로 시작한다. 처음 빌드에서 한두 개 위반이 더 잡힌다 — Build Cache 어노테이션이 누락된 자작 task가 있었다. `@InputFile`, `@OutputFile`을 정확히 박는다. 그러고 나면 빌드가 두 번째부터 빠르게 돈다.

**Day 6~ — Spring Boot.** Gradle 마이그레이션이 안정화된 다음, 별도 PR로 Spring Boot 3.x → 4.x로 옮긴다. 이건 6장의 영역이다.

이 일지가 모든 회사 빌드에 그대로 맞지는 않는다. 자작 plugin이 많고 의존성이 복잡한 회사일수록 Day 3~4의 메시지 처리에 시간이 더 든다. 그게 정상이다. **점진 도입을 받아들이자.** 한 PR로 모든 걸 옮기려 들지 말고, wrapper 한 PR, 깨진 자리 처방 한 PR, Configuration Cache 활성화 한 PR, Spring Boot 마이그레이션 한 PR로 나누자. 깨졌을 때 어느 PR이 깬 건지 즉시 안다. 1주차에 끝나지 않는다는 사실을 받아들이는 게 마이그레이션을 빨리 끝내는 길이다.

## 마무리

Gradle 9.x 마이그레이션은 결국 세 가지를 점검하는 일이다. **데몬 JDK가 17 이상인가, third-party plugin들이 9.x를 지원하는가, 그리고 빌드 스크립트에 옛 API의 잔재가 남아 있는가.** 셋 다 클리어하면 9.x는 8.x와 거의 같은 느낌으로 돈다. 다만 옛 API의 잔재가 우리 빌드만의 문제가 아니라 회사가 5~7년 쌓아온 빚일 수 있다는 점, 그 빚을 한 번에 정리할 수는 없다는 점을 받아들이자.

이 장의 처방 표를 한번 더 짚자. `Project#exec`는 `providers.exec`로, `jcenter()`는 `mavenCentral()`로, `tasks.create`는 `tasks.register`로, `project.convention`은 `extensions.getByType`으로, archive timestamp 의존은 가능하면 도구 쪽을 고친다. 다섯 가지만 기억해두면 대부분의 빌드가 9.x에 도착한다.

그리고 이 책의 약속을 두 개 회수했다. **1장의 약속** — 8.x 사용자를 위한 마이그레이션 체크리스트가 17장에 있다는 약속. 그리고 **3장의 lazy registration 약속** — Convention API가 사라지면서 lazy + Property가 단단한 표준이 됐다는 약속. 두 약속을 회수했으니 책의 거의 끝에 다다랐다.

다음 18장은 마지막 장이다. 책에서 다룬 18가지를 회고하면서, "이제 어디로 갈 것인가"를 본다. Isolated Projects, Develocity, GraalVM Native 운영 심화 — 이 책에서 다 다루지 못한 다음 단계들을 짧게 짚는다. 우리 `shop` 앱의 마지막 모습도 거기서 본다.

# 18장. 이제 어디로 갈 것인가

월요일 아침, 회사 자리에 앉아 자기 회사의 `build.gradle.kts`를 다시 연다고 해보자. 1장에서 처음 이 책을 펼쳤을 때와 같은 파일이다. 그런데 같은 파일이 다르게 읽힌다. `subprojects {}` 한 블록이 눈에 들어오면 "여기는 convention plugin으로 옮겨야 한다"가 자동으로 떠오르고, `tasks.create` 한 줄이 보이면 "lazy registration으로 바꾸자"가 손가락에 먼저 닿는다. `org.gradle.configuration-cache` 줄이 없는 `gradle.properties`를 보면 답답하다. 회사 CI에서 wrapper가 매번 200MB짜리 all distribution을 받고 있다는 사실이 갑자기 거슬린다.

이 감각이 이 책이 도착하려고 한 자리다. 1장에서 "build.gradle.kts를 어디까지 만질 수 있게 되는가"를 물었다. 9가지로 약속을 걸었다. 이제 그 약속을 회수할 시간이다. 그리고 회수한 다음에는, 책에서 다루지 않은 영역 중 당신 회사 빌드에 가장 먼저 적용할 만한 것이 무엇인지 골라야 한다.

## 18장의 발자취 — 1장에서 17장까지

`shop` 앱이 자라온 흔적을 잠깐 되짚어보자. 그래야 다음으로 어디로 갈지 정할 수 있다.

`ch01/`의 `build.gradle.kts`는 의존성 한 줄짜리 Hello World였다. 2장에서 Gradle이 빌드를 settings + project + task로 어떻게 보는지를 자기 언어로 잡았고, 3장에서 Kotlin DSL의 type-safe accessor가 왜 `plugins {}` 다음에만 노출되는지를 만났다. 4장에서 Maven의 `<dependencyManagement>`, `<parent>`, `<profile>`이 Gradle의 어디로 옮겨가는지를 한 번에 받았고, Toolchain을 단일 모듈에서 미리 박았다.

`ch04-bootapp/`에 들어가서 5장에서 BOM은 resolution, Catalog는 declaration이라는 직교 관계를 잡고 `gradle/libs.versions.toml`을 도입했다. 6장에서는 `bootJar`의 `BOOT-INF/classes`, `BOOT-INF/lib`, `layers.idx`를 열어봤고, Spring Boot 3.x에서 4.x로 옮길 때 무엇이 깨지는지도 챙겼다. 7장에서 JVM Test Suite로 `integrationTest`를 분리했다.

8장에서 `ch08-multimodule/`로 옮기면서 모듈을 쪼갰고, 그 끝에서 정상 빌드가 안 되는 사고에 정면으로 부딪혔다. 9장 — 책 전체의 클라이맥스 중 하나 — 에서 library 모듈에 빈 jar가 나오는 그 사고를 5분 진단 체크리스트로 풀었다. 10장에서 4개 모듈에 똑같이 들어가던 코드가 convention plugin 한 줄로 줄어들었고, 11장에서 `buildSrc`의 한계를 `build-logic` included build로 넘었다.

12장에서 소비자에서 생산자로 옮겼다. `shop.build-info` 커스텀 plugin을 Provider/Property로 만들고, Input/Output 어노테이션을 정확히 박아서 Build Cache hit이 일어나게 했다. 13장에서 Configuration Cache를 켜고 위반을 진단했다. third-party plugin이 비명을 지를 때 `problems=warn`으로 점진 도입하는 전략을 잡았다. 14장에서 `gradle/actions/setup-gradle@v6`로 CI에 올렸고, Build Scan을 읽는 법을 손에 익혔다.

15장에서 `nativeCompile`이 5분에서 20분을 받아먹는 현실을 인정하고, native는 CI 별도 job으로 격리했다. 16장에서 의존성 보안 — verification + locking + content filtering — 세 영역을 운영 관점에서 다시 봤다. 17장에서 회사 빌드를 8.x나 7.x에서 9.x로 올리는 일이 막연한 두려움에서 점검 가능한 체크리스트로 바뀌었다.

지금 `shop`의 마지막 모습은 이렇다. 단일 의존성 한 줄에서 출발해서, 멀티 모듈 + 커스텀 플러그인 + Configuration Cache + CI + Native + 보안까지. 1장의 9가지 약속이 모두 자리를 잡았다. 9개 중에서 지금 자기가 할 수 있는 게 몇 개인지, 한 번 세어보자. 1장 끝에 세어봤던 숫자와 비교해보면 좋다.

그런데 이게 끝이 아니다. Gradle은 계속 자라는 도구다. 그리고 회사 빌드에는 책에서 다루지 않은 영역이 아직 남아 있다. 다음으로 무엇을 도입할지 고르자.

## 다음으로 도입할 만한 세 가지

도입 후보를 7개, 10개로 나열하는 건 별 도움이 안 된다. 회사 빌드에 실제로 한 가지를 추가하는 일은 분기를 하나 잡고 PR을 만들고 팀에 설명하는 노동이다. 그 노동의 비용을 감수할 만한 후보를 셋만 고르자. 각각의 진입 비용도 솔직히 추정해두자.

### 1. Isolated Projects — 13장에서 미뤄둔 IDE sync 문제의 답

13장에서 Configuration Cache를 켰을 때 한 가지를 미뤘다. **Configuration Cache는 빌드는 가속하지만 IDE sync 자체는 가속하지 않는다.** IntelliJ에서 import 후 sync가 한참 걸리는 문제, `org.gradle.parallel=true`로 임시 완화는 되지만 본질은 그대로다.

본질의 답이 Isolated Projects다. Configuration Cache의 후계다. 프로젝트 간 격리를 통해 각 프로젝트의 configuration phase를 병렬로 돌린다. 큰 멀티 모듈 빌드에서 IDE sync 시간이 단축되는 게 핵심 가치다. **9.x에 incubating으로 도입되어 있고**, 안정화 시점은 아직 미정이다.

활성화 자체는 단순하다.

```properties
# gradle.properties
org.gradle.unsafe.isolated-projects=true
```

`unsafe.` prefix와 `isolated-` 키워드가 보여주듯 아직 incubating이다. 켜는 순간 자기 빌드의 cross-project 접근(다른 프로젝트의 `tasks`, `extensions`를 직접 들여다보는 코드)이 줄줄이 위반으로 잡힌다. 13장의 Configuration Cache 위반보다 더 엄격하다고 보면 된다.

**진입 비용:** 위반 패턴을 잡아내는 시간이 가장 크다. 회사 빌드의 cross-project 접근이 얼마나 많은지에 따라 며칠에서 몇 주가 든다. 10장에서 `subprojects {}`를 convention plugin으로 옮겨놨다면 그 노동의 절반이 이미 끝난 셈이다. 그게 안 된 상태에서 Isolated Projects를 켜려고 하면 두 일을 동시에 하게 된다.

**언제 도입할 만한가:** 모듈이 10개를 넘어가고 IDE sync가 분 단위로 느린 팀. Isolated Projects가 incubating에서 stable로 올라오는 신호를 release notes로 지켜보면서, 그 전에 자기 빌드의 cross-project 접근부터 정리해두자. 안정화되는 순간 자기 회사 IDE 환경이 즉시 빨라진다.

### 2. Develocity — 사내 Build Scan 호스팅과 원격 캐시

14장에서 `--scan`을 한 번씩 띄울 때마다 Gradle의 무료 서비스에 결과가 publish됐다. 회사 빌드의 dependency conflict, task timeline, Configuration Cache 통계가 외부 URL로 올라간다. 작은 팀이라면 충분히 쓸 만하지만, 회사 보안 정책에 따라 외부 publish가 막히기도 한다. 그리고 무료 서비스는 보존 기간이 짧다.

Develocity(구 Gradle Enterprise)는 그 자리에 들어간다. **사내에서 Build Scan을 호스팅한다.** 무한 보존이 가능하고, 팀 단위 dashboard가 붙는다. 여기까지가 첫 번째 가치다.

두 번째 가치는 원격 Build Cache다. 13장에서 활성화한 local cache는 자기 머신에만 쌓인다. CI의 cache는 GitHub Actions의 cache에 의존한다. Develocity 원격 cache는 회사 네트워크 안에 cache 서버를 두고, 개발자 A의 머신에서 빌드한 결과를 개발자 B와 CI가 그대로 받아 쓰게 한다. 큰 빌드일수록 효과가 극적이다.

세 번째 가치가 Predictive Test Selection이다. 코드 변경의 영향을 받지 않는 테스트는 건너뛴다. 통합 테스트 1000개를 다 돌리던 PR이 영향받는 200개만 돌린다. 큰 monorepo에서 CI 시간이 절반 이하로 떨어진다는 사례가 나온다.

**진입 비용:** 라이선스 비용이 첫째다. 사용자 수 기반의 commercial license다. 두 번째는 운영 인력 — Develocity 인스턴스 자체를 사내에서 호스팅하거나 SaaS로 받거나 하는 선택이 필요하고, cache 서버의 디스크와 네트워크 비용이 운영 항목으로 들어온다. 세 번째는 학습 — dashboard를 어떻게 읽고, 어떤 metric을 팀의 KPI로 잡을지 정해야 한다.

**언제 도입할 만한가:** CI 시간이 팀의 생산성을 명백히 깎아먹는 시점이다. PR 한 번에 30분이 걸리고, 개발자들이 그 사이에 다른 일로 옮겨가서 컨텍스트 스위칭 비용이 누적되고 있다면, Develocity 라이선스 비용이 그 비용보다 작을 가능성이 높다. 책에서는 포인터만 던졌으니, 도입을 검토할 시점에 공식 문서와 사례를 한 번 더 들여다보자.

### 3. GraalVM Native 운영 심화 — 15장의 다음 한 걸음

15장에서 `./gradlew nativeCompile`이 5분에서 20분을 받아먹는 현실, reflection/resource hint가 누락되면 런타임에 터지는 함정을 만났다. 그래서 native는 CI 별도 job으로, 개발자 로컬은 JVM 빌드로 분리했다. 거기까지가 책의 진입선이다.

운영에 native를 실제로 올리면 그 다음 영역이 열린다. 세 가지를 짚어두자.

**첫째, AOT hint 디버깅.** Spring Boot의 `processAot` task가 자동으로 생성하는 reachability metadata가 모든 케이스를 커버하지 않는다. 런타임에 `ClassNotFoundException`이나 `MissingResourceException`이 터지는 사고는 native 운영의 가장 흔한 사고다. `runtime-hints-agent`로 JVM 모드에서 trace를 수집해서 hint를 생성하는 워크플로가 정석이지만, 실무에선 agent가 잡지 못하는 동적 패턴(`Class.forName`을 변수로 받는 코드, SpEL 표현식, 동적 proxy)이 남는다. 이 사각지대를 잡는 일이 native 운영의 첫 번째 영역이다.

**둘째, profiling.** `native-image`는 PGO(Profile-Guided Optimization)를 지원한다. 운영 환경에서 수집한 profile 데이터를 빌드에 다시 먹여서 hot path를 최적화하는 방식이다. JVM의 JIT이 런타임에 하는 일을 AOT에서 빌드 시점에 흉내내는 셈이다. 일반 빌드의 두 배 가까운 시간이 들지만 throughput이 의미 있게 올라간다. 빌드와 운영의 피드백 루프를 만드는 일이라 인프라 작업이 적지 않다.

**셋째, GC 튜닝.** Native binary는 기본 Serial GC를 쓴다. 짧은 lifecycle의 serverless 워크로드에는 적합하지만, long-running 서버에는 G1이나 Epsilon GC가 더 나은 선택이 되는 경우가 있다. native-image의 `--gc` 옵션과 GraalVM의 GC 옵션은 일반 JVM의 그것과 일치하지 않는 부분이 있어, 옵션 매핑을 다시 잡아야 한다.

**진입 비용:** 인프라 작업 비중이 크다. CI에 profiling job을 추가하고, 운영에서 profile 데이터를 회수해서 빌드 파이프라인에 다시 먹이는 루프는 단순한 task 한두 개로 끝나지 않는다. GraalVM 자체의 release cycle도 빠르다 — 6개월마다 메이저 변경이 들어오니, native에 운영 의존성을 박는 순간 GraalVM 버전 관리도 회사 빌드의 일부가 된다.

**언제 도입할 만한가:** 콜드 스타트 시간이 비즈니스 KPI인 경우다. 서버리스 워크로드, on-demand 작업자 풀, 메모리 비용이 크게 잡히는 환경. 그 외에는 15장의 진입선(`bootBuildImage`로 native 이미지를 만들 수 있다, CI에 별도 job으로 띄운다)에서 멈춰도 충분히 가치를 얻는다. 다음 한 걸음은 비즈니스가 그 비용을 정당화할 때 떼자.

## 책에서 다루지 않은 영역 — Out of Scope 회수

세 가지를 깊게 다뤘다. 그 외에 책이 의도적으로 빠뜨린 영역도 짧게 짚어두자. 회사 빌드의 다음 한 분기가 이 영역 중 하나에 닿을 수 있다.

- **Android Gradle Plugin (AGP)**. 본 책은 백엔드 Spring Boot에 집중했다. variant API, library publishing, app/aar 분리는 AGP의 영역이고, Spring Boot Gradle 플러그인과는 다른 사고 모델을 요구한다. 백엔드와 Android를 한 monorepo로 운영하는 회사라면 AGP의 멘탈 모델을 별도로 잡아야 한다. 시작점은 Android 공식 문서다.

- **Kotlin Multiplatform**. KMP의 `commonMain`/`jvmMain`/`nativeMain` target 구성은 한 권의 책이 더 필요한 영역이다. 백엔드 Spring Boot가 클라이언트 SDK를 같은 코드베이스에서 발행해야 하는 시점에 KMP가 후보로 올라온다. JetBrains의 KMP 공식 문서가 첫 자료다.

- **Tooling API**. IntelliJ나 사내 도구에서 Gradle 빌드를 프로그래밍 방식으로 호출하는 API다. IDE 플러그인을 직접 만들거나, 빌드 결과를 자체 dashboard로 끌어오는 도구를 만들 때 닿는다. 회사가 빌드 인프라를 자체 도구로 감싸는 단계에 도달했다면 다음 후보다.

- **Maven 사용법 자체**. 4장에서 Maven에서 Gradle로 옮겨오는 다리만 놨다. 회사 빌드에 Maven 모듈이 일부 남아 있고 그것을 그대로 유지해야 한다면, Maven의 깊은 영역은 별도 자료로 잡아야 한다.

- **Bazel · Buck**. 더 큰 monorepo와 더 엄격한 hermetic build가 필요한 단계의 도구들이다. Gradle로 멀티 모듈을 잘 운영하고 있다면 당분간 옮길 일은 없다. 회사 규모가 수백 모듈을 넘어가고 빌드 격리가 비즈니스 요구가 되는 시점에 후보로 올라온다.

각 영역에 한 줄씩만 적었다. 이 한 줄 자체가 포인터다. 회사 빌드의 다음 단계가 이 중 어디에 닿을지는 자기 팀의 컨텍스트가 결정한다.

## Gradle의 변화를 따라가는 법

이 책이 9.5를 기준으로 잡혔지만, Gradle은 멈추지 않는다. 책이 출간된 다음 minor에서 9.6이, 그 다음에 10.x가 나온다. 어디서 신호를 따라가야 그 변화에 자기 회사 빌드가 뒤처지지 않을지 짧게 정리해두자.

**Release notes를 분기마다 한 번씩 읽자.** `docs.gradle.org/current/release-notes.html`에 minor 릴리스마다 갱신된다. 새 기능, deprecation 예고, breaking change 예고가 한 곳에 모인다. 17장에서 마이그레이션이 막연한 두려움에서 체크리스트로 바뀌었다면, release notes를 분기마다 읽는 일이 그 체크리스트를 미리 채워두는 작업이다.

**Gradle Slack과 Discuss 포럼.** `gradle-community.slack.com`은 활발하다. `#help` 채널에서 비슷한 사고를 누군가가 먼저 겪고 있다. 9장의 bootJar 함정 같은 사고가 거기서도 매주 새로운 형태로 올라온다. Discuss 포럼(`discuss.gradle.org`)은 더 긴 호흡의 토론에 적합하다.

**GitHub `gradle/gradle` 이슈.** 본인 빌드에서 마주친 사고가 third-party plugin이 아니라 Gradle 자체의 버그라는 의심이 들 때, 이슈 검색이 먼저다. 같은 사고를 누군가가 이미 등록했을 확률이 높다. milestone 라벨로 다음 릴리스에 무엇이 들어올지도 미리 보인다.

**Spring Boot도 같이 따라가야 한다.** Spring Boot Gradle 플러그인은 Gradle release cycle과 별개로 움직인다. 6장에서 Spring Boot 3.x에서 4.x로 옮길 때 무엇이 깨지는지 다뤘다. Spring Boot의 다음 메이저가 나올 때 Gradle 호환성 요구가 어떻게 바뀌는지를 spring-projects/spring-boot 릴리스에서 분기마다 챙기자.

이 네 가지 신호를 분기 한 번씩 보면 충분하다. 매일 들여다볼 필요는 없다. 빌드는 운영의 일부지만, 신호 추적이 풀타임이 되면 정작 회사 코드 자체에 손이 안 간다.

## 18장을 닫으며 — 그리고 책을 닫으며

1장에서 빌드 스크립트가 곧 운영의 일부라는 명제를 걸었다. 멀티 모듈, CI, 보안, 이미지화 — 회사 빌드가 짊어지는 책임이 의존성 몇 줄 추가하는 영역보다 훨씬 넓다는 명제였다. 18장을 통과해온 지금 이 명제가 어떻게 읽히는가.

처음 1장에서는 추상적인 표어로 들렸을 것이다. 그러나 9장의 빈 jar 사고에 부딪혔을 때, 10장에서 convention plugin이 똑같은 코드 네 덩어리를 한 줄로 줄였을 때, 13장에서 Configuration Cache 위반 메시지가 자기 코드 라인을 정확히 찍었을 때, 16장에서 `verification-metadata.xml`에 의존성 수백 줄이 박혔을 때 — 그 순간마다 빌드 스크립트가 운영의 일부라는 명제가 더 이상 표어가 아니라 일상이었다는 것이 보였을 것이다.

당신은 이제 build.gradle.kts를 의존성 몇 줄 추가하는 영역 너머로 옮길 준비가 됐다. 회사 빌드를 한 단계 위로 올릴 수 있다. 다음 PR에 어떤 한 줄을 넣을지 정해보자. `org.gradle.configuration-cache=true` 한 줄이어도 좋고, `subprojects {}` 한 블록을 `buildSrc/src/main/kotlin/`의 convention plugin 하나로 옮기는 PR이어도 좋다. 다음 분기에 Develocity 라이선스를 검토하는 일정을 잡아도 좋고, Isolated Projects의 release notes를 분기 한 번 읽는 routine을 세팅해도 좋다.

`shop` 앱은 여기서 책을 떠난다. 단일 의존성 한 줄에서 시작해서 멀티 모듈 + 커스텀 플러그인 + Configuration Cache + CI + Native + 보안까지 17장에 걸쳐 자랐다. 이제 당신 회사의 `build.gradle.kts`가 그 자리에 선다. 한 가지만 기억해두자. **빌드 도구는 한 번 잘 짜둔다고 끝나는 도구가 아니라, 회사가 자라는 만큼 같이 자라야 하는 도구다.** Gradle도, Spring Boot도, 회사의 코드도 멈추지 않는다. 그러니 자기 빌드도 멈추지 말자.

여기서 책을 닫는다. 다음 PR이 빌드 디렉터리에 작게라도 한 줄을 추가하는 일이 되기를. 그 한 줄이 모이면 1년 뒤 회사 빌드는 지금과 전혀 다른 자리에 가 있을 것이다.

---

## 맺음말

이 책의 마지막 페이지에 도착했다. 18장의 끝에서 우리는 `shop` 앱을 책에서 떠나보냈다. 단일 의존성 한 줄에서 시작해서 멀티 모듈 + 커스텀 플러그인 + Configuration Cache + CI + Native + 보안까지 자란 앱이었다. 그 자리에 이제 당신 회사의 `build.gradle.kts`가 선다.

이 책을 닫으면서 한 가지를 더 짚어두고 싶다. **당신이 책을 통과하는 동안 변한 것은 코드가 아니라 당신 자신이다.** 1장에서 우리는 "빌드 스크립트는 운영의 일부다"라는 명제를 세웠다. 그때 그 명제는 표어처럼 들렸을지도 모른다. 멋있지만 추상적이고, 동의는 하지만 일상과는 거리가 있는 한 줄. 그런데 지금 그 명제를 다시 읽어보자. 어딘가에서 그 명제가 더 이상 표어가 아니라 익숙한 사실로 느껴지는 자리가 보일 것이다.

9장에서 `:domain:bootJar`가 빈 fat jar를 만들어내던 그 출력 로그 앞에서, "Spring Boot 플러그인이 library 모듈에 들러붙으면 빈 jar가 나온다"는 진단을 5분 안에 내릴 수 있게 됐을 때 — 그 순간이 변화의 한 자리였다. 10장에서 4개 모듈의 똑같은 build.gradle.kts가 convention plugin 한 줄로 줄어드는 풍경을 봤을 때, 그 풍경이 단순한 코드 정리가 아니라 회사 빌드의 변경 비용을 다섯 군데에서 한 군데로 옮긴 의사결정임이 보였을 때 — 그것도 변화였다. 12장에서 `providers.exec { commandLine("git", "rev-parse", "HEAD") }.standardOutput.asText.map { it.trim() }` 한 줄의 모든 부분을 자기 언어로 설명할 수 있게 됐을 때, 그 한 줄이 왜 `Project#exec`보다 안전하고 왜 Configuration Cache와 함께 살 수 있는지가 손에 잡혔을 때 — 그것도 변화였다. 16장의 `verification-metadata.xml`이 수백 줄짜리 PR diff로 처음 올라왔을 때, 그 diff가 거추장스러운 부담이 아니라 supply chain의 변동이 코드 변경과 같은 자리에 묶이는 안전망임이 보였을 때 — 그것도 변화였다.

이 변화들의 공통점은 무엇인가. **빌드가 더 이상 불투명한 검은 상자가 아니라는 점**이다. `build.gradle.kts`의 한 줄을 보면 그 줄이 무엇을 책임지는지, 그 줄이 빠지면 어디서 깨지는지, 그 줄을 다르게 적으면 무슨 비용이 따라오는지 — 추측이 아니라 사고 모델로 답할 수 있게 됐다. 이게 1장에서 약속한 출구 상태였다. **build.gradle.kts를 어디까지 만질 수 있게 되는가**라는 질문에 대한 9가지 약속이 모두 자기 자리를 잡았다.

이제 당신은 회사 빌드를 들고 와도 다른 눈으로 본다. `subprojects { ... }`가 보이면 convention plugin으로 옮기고 싶어진다. `tasks.create`가 보이면 lazy registration으로 바꾸고 싶어진다. `org.gradle.configuration-cache=true`가 없는 `gradle.properties`가 답답하다. CI가 `--refresh-dependencies`로 매번 깡통 빌드를 도는 게 거슬린다. 이 감각이 이 책이 만들어내려고 한 것이다. **빌드를 한 단계 위로 올리고 싶은 본능**, 그것이 이 책의 진짜 출구다.

이 본능을 가지고 무엇을 할지는 이제 당신의 일이다. 다음 PR에 어떤 한 줄을 넣을지 정해보자. `org.gradle.configuration-cache=true` 한 줄이어도 좋고, `subprojects { }` 한 블록을 `buildSrc/src/main/kotlin/`의 convention plugin 하나로 옮기는 PR이어도 좋다. 한 번에 큰 변화를 일으키려 들지 말자. 빌드 도구는 한 번에 완벽해지는 도구가 아니다. 한 PR에 한 줄씩 쌓아가는 도구다. 그 한 줄들이 한 분기 뒤, 한 해 뒤에는 회사 빌드 전체를 한 단계 위로 옮긴다.

마지막으로, 빌드 도구의 변화는 멈추지 않는다. Gradle은 이 책이 출간된 다음 minor에서 9.6이, 그 다음에 10.x가 나올 것이다. Spring Boot도 4.1이, 5.0이 따라온다. Configuration Cache가 default-on이 되는 날도 멀지 않았다. Isolated Projects가 stable로 올라오는 날도 온다. 이 모든 변화의 신호를 매일 추적할 필요는 없다. **분기 한 번씩 release notes를 읽는 routine** 정도면 충분하다. 그 routine 안에서 당신은 이 책이 짠 사고 모델을 다음 도구들에도 그대로 적용하게 될 것이다. 사고 모델이 도구보다 오래 산다.

여기서 책을 닫는다. 다음 PR이 빌드 디렉터리에 작게라도 한 줄을 추가하는 일이 되기를. 그 한 줄이 모이면 1년 뒤 회사 빌드는 지금과 전혀 다른 자리에 가 있을 것이다. 그 한 줄을 적는 사람이, 더 이상 build.gradle.kts를 "검은 상자"로 보지 않는 사람이라는 사실이, 이 책이 함께한 가장 작은 변화이자 가장 큰 변화다.

---

## 참고문헌

### 1차 자료 (공식 문서)

- **Gradle User Guide (current = 9.5)** — https://docs.gradle.org/current/userguide/userguide.html
  - 핵심 섹션: `build_lifecycle`, `kotlin_dsl`, `multi_project_builds`, `composite_builds`, `sharing_build_logic_between_subprojects`, `best_practices_structuring_builds`
  - 의존성 관련: `declaring_configurations`, `version_catalogs`, `dependency_locking`, `dependency_verification`, `repository_content_filtering`
  - 성능 관련: `config_cache:intro`, `config_cache:requirements`, `config_cache:ide`, `build_cache`, `incremental_build`, `lazy_configuration`
  - 빌드 도구화: `jvm_test_suite_plugin`, `custom_tasks`, `implementing_gradle_plugins`, `implementing_gradle_plugins_precompiled`
  - JVM 관리: `toolchains`
- **Spring Boot Gradle Plugin Reference (current = 4.0.6)** — https://docs.spring.io/spring-boot/gradle-plugin/index.html
  - Packaging Executable Archives, Packaging OCI Images, Running, Managing Dependencies, AOT, Reacting to Other Plugins
- **Gradle 9.0 Release Notes** — https://docs.gradle.org/9.0.0/release-notes.html
- **Gradle 9.5 Release Notes** — https://docs.gradle.org/current/release-notes.html
- **Upgrading to Gradle 9.0** — https://docs.gradle.org/current/userguide/upgrading_major_version_9.html
- **Kotlin Gradle Docs** — https://kotlinlang.org/docs/gradle.html
- **gradle/actions/setup-gradle 공식 문서** — https://github.com/gradle/actions/blob/main/docs/setup-gradle.md
- **GraalVM Native Build Tools — Gradle Plugin** — https://graalvm.github.io/native-build-tools/latest/gradle-plugin.html

### 보조 자료

- Gradle Blog — "State of the Configuration Cache (Road to Gradle 9)" — https://blog.gradle.org/road-to-configuration-cache
- Eric Haag — "Bootiful Builds: Best Practices for Spring Boot with Gradle" — https://erichaag.dev/posts/bootiful-builds-best-practices-spring-boot-gradle/
- Spring Boot Issue #16689 — multi-module Kotlin bootJar 함정 — https://github.com/spring-projects/spring-boot/issues/16689
- Gradle Discuss Forum #41459 — multi-module bootJar 의존성 — https://discuss.gradle.org/t/understanding-dependencies-in-multi-module-project-with-spring-boot-plugin/41459

### 커뮤니티·신호 추적

- Gradle Community Slack — https://gradle-community.slack.com
- Gradle Discuss Forum — https://discuss.gradle.org
- `gradle/gradle` GitHub Issues — https://github.com/gradle/gradle/issues
- Spring Boot Releases — https://github.com/spring-projects/spring-boot/releases

---

## 판권

**빌드를 다시 짠다 — Spring Boot × Gradle 9.5 × Kotlin DSL 실전 가이드**

- 저자: Toby-AI
- 발행일: 2026-05-11
- 판본: v1.0.1
- 라이선스: CC BY-NC-SA 4.0
  - 저작자 표시 · 비상업적 이용 · 동일조건 변경허락
  - https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko
- ⓒ 2026 Toby-AI. CC BY-NC-SA 4.0
- 식별자: `gradle-spring-boot-kotlin-dsl-v1.0.1`
- 산출: book-writer harness v1.2.0 — https://github.com/tobyilee/book-writer (가상)
