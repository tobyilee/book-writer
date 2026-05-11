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
