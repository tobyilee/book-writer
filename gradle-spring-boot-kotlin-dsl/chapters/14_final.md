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
