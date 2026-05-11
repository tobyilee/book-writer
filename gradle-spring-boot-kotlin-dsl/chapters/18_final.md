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
