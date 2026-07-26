# 웹 리서치 보강 2차 조사 (갭 클로징)
**검색 시점:** 2026-07-25 / **genre:** tech-book / **슬러그:** mac-docker-container
**범위:** 1차 `web.md`가 남긴 6개 갭 한정. 그 외 주제는 다루지 않는다.

> **증거 규율:** 이 문서의 모든 버전·플래그·기본값은 2026-07-25 세션에서 직접 열어본 1차 소스 페이지에서 읽은 것만 기재한다. 확인하지 못한 것은 "미확인"으로 남기고 빈칸을 두지 않는다.
>
> **WebFetch 한계 고지:** 페이지 추출은 소형 모델을 거친다. 같은 문서(`multi-platform/`와 `multi-platform.md`)를 두 번 가져왔을 때 발췌 범위가 서로 달랐다. 따라서 **"해당 문구를 찾지 못함"은 "문서에 없음"의 증거가 아니다.** 이 문서에서 부재를 말할 때는 항상 "확인한 페이지 목록"을 함께 적는다.

---

## G1. Paketo / `bootBuildImage` 멀티아키 현황 ⭐

### 결론: **여전히 단일 플랫폼** (1회 빌드 = 1개 아키텍처)

커뮤니티 리서치가 확보한 Paketo 메인테이너 dmikusa의 2024-11-21 진술 — "Neither `pack build` nor `spring-boot:build-image` will build images for multiple architectures in one run" — 은 **2026-07-25 현재 공식 문서 기준으로도 유효하다.** 아래 네 갈래 1차 증거가 서로 독립적으로 같은 결론을 가리킨다.

#### 증거 1 — Spring Boot Gradle 플러그인 레퍼런스 (`imagePlatform`은 단일 값)

> "The platform (operating system and architecture) of any builder, run, and buildpack images that are pulled. Must be in the form of `OS[/architecture[/variant]]`, such as `linux/amd64`, `linux/arm64`, or `linux/arm/v5`. Refer to documentation of the builder being used to determine the image OS and architecture options available."
>
> Default value: "No default value, indicating that the platform of the host machine should be used."

- URL: https://docs.spring.io/spring-boot/gradle-plugin/packaging-oci-image.html
- 문서 표기: **Spring Boot 4.1.0 문서 기준** (발행일: 미확인 — 페이지에 날짜 표기 없음)
- 신뢰성: **최상** (공식 레퍼런스)
- 검색: 2026-07-25
- 문법 자체가 단일 값이다: `OS[/architecture[/variant]]`. 콤마 구분 목록을 허용한다는 서술이 없다. 커맨드라인 옵션은 `--imagePlatform`.
- 같은 페이지에서 읽은 기본 빌더: `paketobuildpacks/builder-noble-java-tiny:latest`

#### 증거 2 — Spring Boot Maven 플러그인 레퍼런스 (동일 문구, 단일 값)

> "The platform (operating system and architecture) of any builder, run, and buildpack images that are pulled. Must be in the form of `OS[/architecture[/variant]]`, such as `linux/amd64`, `linux/arm64`, or `linux/arm/v5`."

- URL: https://docs.spring.io/spring-boot/maven-plugin/build-image.html
- User property: `spring-boot.build-image.imagePlatform`
- 문서 표기: **Spring Boot 4.1.0 문서 기준**. 파라미터의 "Since" 필드는 **3.4.0** (발행일: 미확인)
- 신뢰성: **최상**
- 검색: 2026-07-25
- Gradle 쪽과 문구가 글자 단위로 같다 → 두 플러그인이 같은 단일 플랫폼 모델을 공유한다.

#### 증거 3 — `pack build` CLI 레퍼런스 (`--platform`은 `string`, 복수형 아님) ⭐ 가장 단단한 증거

`pack build`의 플래그 표에서 **타입 표기**가 결정적이다:

> `--platform string` — "Platform to build on (e.g., "linux/amd64")"

같은 표의 다른 플래그와 비교하면 의도가 드러난다:

> `-t, --tag strings` — Additional tags for the output image
> `-b, --buildpack strings` — Buildpack to use...
> `--pre-buildpack stringArray` — Buildpacks to prepend to builder's order

- URL: https://buildpacks.io/docs/for-platform-operators/how-to/integrate-ci/pack/cli/pack_build/
- 발행일: 미확인 (CLI 레퍼런스, 날짜 표기 없음) / 검색: 2026-07-25
- 신뢰성: **최상**
- **왜 단단한가:** `string` vs `strings`/`stringArray` 구분은 CLI 플래그 정의에서 기계 생성된 것이다. 산문 설명과 달리 저자의 표현 실수일 여지가 거의 없다. `--platform`이 `string`(단수)이라는 것은 **한 번에 한 플랫폼**이라는 뜻이다.
- ⚠️ 같은 페이지의 `-B, --builder` 기본값이 `cnbs/sample-builder:resolute`로 표기돼 있으나 이는 **문서용 샘플**이다. pack의 실제 운영 기본 빌더로 인용하지 말 것.

#### 증거 4 — CNB 공식 "Build for ARM architecture" (교차 아키텍처 빌드 미지원 명시)

> "Our current multi-architecture support allows building an ARM64 app image on an ARM64 host, and building an AMD64 app image on an AMD64 host."

> "We do not currently support building an app image for one architecture on a different architecture. However, if your host machine supports emulation (for example, with QEMU) you may be able to perform cross platform builds, albeit with a performance penalty."

> "By default, `pack` uses the current architecture for multi-arch builders like `heroku/builder:24`, so an AMD64 image will be built on AMD64 systems."

- URL: https://buildpacks.io/docs/for-app-developers/how-to/special-cases/build-for-arm/
- 발행일: 미확인 / 검색: 2026-07-25 / 신뢰성: **최상**
- 같은 페이지에서 읽은 멀티아키 빌더 예시: `heroku/builder:24` (AMD64 + ARM64, .NET·Go·Java·Node.js·PHP·Python·Ruby·Scala 빌드팩 멀티아키 지원)

### ⚠️ 반드시 구분해서 쓸 것 — "CNB 멀티아키 지원"의 두 얼굴

CNB 생태계에 "멀티아키 지원"이라는 말이 돌아다니는데 **두 개의 서로 다른 것**이다. 구분하지 않으면 위 결론이 CNB 자기 문서와 모순되는 것처럼 보인다.

| 대상 | 멀티아키 지원 여부 | 근거 |
|------|-------------------|------|
| **빌더 · 빌드팩 패키징** (`pack builder create`, `pack buildpack package`) | **지원** — 이미지 인덱스(image index) 생성 | CNB RFC 0128 (본문 직접 열람, **Approved**) — 아래 증거 5 |
| **앱 이미지 1회 빌드** (`pack build`, `bootBuildImage`, `spring-boot:build-image`) | **미지원** — 1회 1아키텍처 | 위 증거 1~4 (모두 본문 직접 열람) |

독자에게 중요한 것은 **아래 행**이다. 빌더가 멀티아키여도, 그 빌더로 만드는 내 앱 이미지는 한 번에 하나다.

#### 증거 5 — CNB RFC 0128이 스스로 범위를 "빌더·패키지"로 한정한다 ⭐ 결론을 잠그는 증거

- URL: https://github.com/buildpacks/rfcs/blob/main/text/0128-multiarch-builders-and-package.md
- 상태: **Approved** / 발행일: 미확인 / 검색: 2026-07-25 / 신뢰성: **최상** (프로젝트 공식 RFC)

RFC가 문제를 세 갈래로 쪼갠 뒤(원문):
> "The problem for adding support for multi-platform buildpacks can be divided into three parts:
> 1. Support buildpack authors to migrate their existing buildpacks to support multiple operating systems, architectures, variants and distros.
> 2. Support buildpack authors to create new buildpacks and builders that handle multi-arch from the beginning.
> 3. Support application developers to create application images using multi-arch buildpacks and builders."

**자신의 범위를 2번으로 못 박는다 (원문):**
> "The purpose of this RFC is to solve the statement 2, adding the capability to the commands: `pack buildpack package`, `pack builder create`..."

→ **3번(애플리케이션 개발자가 멀티아키 앱 이미지를 만드는 것)은 이 RFC의 대상이 아니다.** CNB 자신이 "빌더·패키지 멀티아키"와 "앱 이미지 멀티아키"를 별개 문제로 번호 매겨 분리했고, 구현한 것은 앞의 것이다. **G1 결론이 CNB 공식 문서와 모순되지 않음을 이 RFC가 직접 증명한다.**

### 실무 결론 (책에 쓸 형태)

맥(arm64)에서 `bootBuildImage`를 그냥 돌리면 **arm64 이미지**가 나온다. amd64 서버에 배포하려면 둘 중 하나다.

1. `imagePlatform=linux/amd64` 지정 — 호스트 에뮬레이션이 필요하고 성능 페널티가 있다 (CNB 문서가 QEMU 경로를 명시적으로 인정)
2. 두 아키텍처를 **각각 독립적으로 빌드**한 뒤 `docker manifest`로 인덱스 이미지를 합성 (dmikusa 2024-11-21 권고 — 2026-07 현재 공식 문서와 모순 없음)

**Dockerfile + buildx 경로와의 결정적 차이가 여기다.** `docker buildx build --platform linux/amd64,linux/arm64`는 콤마 목록을 받아 한 번에 매니페스트 리스트를 만든다(G6 참조). Buildpacks는 못 한다. 이 대비가 책의 "3경로 비교" 축이다.

### 확인한 페이지 목록 (G1)
- https://docs.spring.io/spring-boot/gradle-plugin/packaging-oci-image.html ✅
- https://docs.spring.io/spring-boot/maven-plugin/build-image.html ✅
- https://buildpacks.io/docs/for-platform-operators/how-to/integrate-ci/pack/cli/pack_build/ ✅
- https://buildpacks.io/docs/for-app-developers/how-to/special-cases/build-for-arm/ ✅
- https://github.com/buildpacks/pack/releases ✅
- https://github.com/buildpacks/pack/issues/1570 ✅ — "Multi arch image build support", **Closed**, 생성 **2022-12-06**. 최종 활동일·메인테이너 최종 코멘트는 **읽어내지 못함**(페이지 추출 실패). 이 이슈를 "멀티아키가 구현되어 닫혔다"는 근거로 쓰지 말 것 — 닫힌 사유 미확인.

#### pack CLI 릴리스 (신선도 앵커)
- 최신: **v0.40.8 (2026-07-13)**
- 직전: v0.40.7 (2026-06-23), v0.40.6 (2026-05-16), v0.40.5 (2026-05-15), v0.40.4 (2026-05-02), v0.40.3 (2026-04-22), v0.40.2 (2026-03-13), v0.40.1 (2026-03-02), v0.40.0 (2026-02-03)
- 최근 릴리스에서 아키텍처 관련 유일 언급: v0.40.2 — "fix: treat amd64 as equivalent to x86-64 for lifecycle binary selection" (lifecycle 바이너리 선택 버그 수정. **앱 이미지 멀티아키 출력과 무관**)
- URL: https://github.com/buildpacks/pack/releases / 검색: 2026-07-25

**관련 섹션:** 스프링 부트 이미지 빌드 3경로 비교 / 맥에서 빌드해 서버에 배포하기 / 멀티아키 트러블슈팅

---

## G2. Jib

### 결론: **Jib은 한 번의 빌드로 매니페스트 리스트(멀티플랫폼)를 만든다 — 단, 레지스트리 push 경로에서만, 그리고 incubating이다**

이것이 Paketo와의 결정적 차이다. 3경로 비교표의 핵심 대비축.

#### 목표(goal)·태스크 이름

**Maven** (URL: https://github.com/GoogleContainerTools/jib/blob/master/jib-maven-plugin/README.md, 신뢰성: **최상**, 발행일: 미확인, 검색: 2026-07-25)
- `jib:build` — push to registry
- `jib:dockerBuild` — build to Docker daemon
- `jib:buildTar` — save as tarball

**Gradle** (URL: https://github.com/GoogleContainerTools/jib/blob/master/jib-gradle-plugin/README.md, 신뢰성: **최상**, 발행일: 미확인, 검색: 2026-07-25)
- `gradle jib` — "Builds and pushes a container image to a registry"
- `gradle jibDockerBuild` — "Builds directly to a local Docker daemon"
- `gradle jibBuildTar` — "Builds and saves the image as a tarball to `build/jib-image.tar`"

#### 플러그인 버전

| 플러그인 | 버전 | 출처 | 발행일 |
|---------|------|------|--------|
| `jib-maven-plugin` | **3.5.2** | README 퀵스타트 스니펫 + GitHub Releases 태그 `v3.5.2-maven` | **미확인** |
| `jib-gradle-plugin` | **3.5.4** | README 플러그인 블록 `id 'com.google.cloud.tools.jib' version '3.5.4'` + Releases 태그 `v3.5.4-gradle` | **미확인** |
| `jib-core` | **0.28.2** | Releases 태그 `v0.28.2-core` | **미확인** |

⚠️ **날짜 신뢰 불가 — 반드시 읽을 것.** GitHub Releases 페이지 추출이 최신 3건(`v3.5.4-gradle`, `v3.5.2-maven`, `v0.28.2-core`)의 날짜를 **2024-07-14**로 보고했으나, 같은 추출이 그 릴리스의 변경 내용으로 "Java version support (Java 25)"를 들었다. Java 25는 2024-07 시점에 존재하지 않았으므로 **날짜 추출이 틀렸다.** 따라서 **버전 번호만 채택하고 날짜는 전부 "미확인"으로 처리한다.** 책에 Jib 릴리스 날짜를 쓰지 말 것.

Gradle 쪽 버전(3.5.4)이 Maven 쪽(3.5.2)보다 앞서 있다 — Jib은 Maven/Gradle 플러그인이 **독립 버저닝**된다. "Jib 3.5.x" 식으로 뭉뚱그리지 말고 플러그인별로 표기할 것.

#### 기본 베이스 이미지

> "The image reference for the base image" — 기본값 **`eclipse-temurin:{8,11,17,21,25}-jre`** (JAR 프로젝트), WAR 프로젝트는 **`jetty`**

⚠️ `{8,11,17,21,25}`는 **문서 표기법**이다 — 프로젝트의 자바 버전에 따라 결정된다는 뜻이지 리터럴 태그가 아니다. Dockerfile에 그대로 복사하면 안 된다.

- 출처: jib-maven-plugin README / jib-gradle-plugin README (둘 다 동일 서술)
- → **G3와 직결.** Jib을 쓰면 베이스 이미지를 안 골라도 Temurin JRE가 자동으로 붙는다. 이게 "Dockerfile을 직접 쓸 때만 `FROM` 고민이 생긴다"는 책의 구조를 만든다.

#### 멀티플랫폼 — `platforms` 설정

`from` 아래에 `platforms` 리스트를 둔다.

**Maven README의 정의:**
> `platforms` (list) — "Configures platforms of base images to select from a manifest list."
> `architecture` (string, 기본값 `amd64`) — "The architecture of a base image to select from a manifest list."
> `os` (string, 기본값 `linux`) — "The OS of a base image to select from a manifest list."

**Gradle 예제 (README 그대로):**
```groovy
from {
  platforms {
    platform {
      architecture = 'amd64'
      os = 'linux'
    }
    platform {
      architecture = 'arm64'
      os = 'linux'
    }
  }
}
```

#### ⭐ 출력이 매니페스트 리스트인가 — FAQ가 답한다 (YES)

- URL: https://github.com/GoogleContainerTools/jib/blob/master/docs/faq.md
- 신뢰성: **최상** (공식 FAQ) / 발행일: 미확인 / 검색: 2026-07-25

> "When multiple platforms are specified, Jib creates and pushes a manifest list (also known as a fat manifest) after building and pushing all the images for the specified platforms."

**즉 `platforms`는 "베이스 이미지 고르기"에 그치지 않고, 출력 이미지도 매니페스트 리스트가 된다.** Maven README의 property 설명("select from a manifest list")만 보면 입력 선택으로만 읽히므로, 반드시 FAQ의 이 문장을 근거로 쓸 것.

#### Jib 멀티플랫폼의 제약 (FAQ 원문 기반) — 책에 반드시 병기

**incubating feature**로 표시돼 있다. 제약:
- **"OCI image indices are not supported (as opposed to Docker manifest lists)."**
- **"Does not support pushing to a Docker daemon (`jib:dockerBuild` / `jibDockerBuild`) or building a local tarball (`jib:buildTar` / `jibBuildTar`)."** → **멀티플랫폼은 `jib` / `jib:build`(레지스트리 push) 전용**
- architecture와 os만 지원 (variant 미지원)
- 로컬 Docker 데몬 이미지·타르볼을 베이스 이미지로 쓸 수 없음
- **크로스 컴파일 미지원** — FAQ 원문 표현으로 "platform-specific binaries needed"

⚠️ **"매니페스트 리스트를 만든다"와 "크로스 컴파일 미지원"은 모순이 아니다.** 앞은 **출력 이미지 형태**에 관한 것이고(복수 platform 지정 시 fat manifest를 push), 뒤는 **플랫폼별 네이티브 바이너리가 필요한 경우** Jib이 그 바이너리를 대신 만들어주지는 않는다는 제약이다. 두 문장을 나란히 읽는 사람이 충돌로 오해하기 쉬우니 책에서는 반드시 이 구분을 붙일 것.
> (저자 해석 — 출처 없음, 책에 쓸 때 별도 확인 필요: 순수 JVM 바이트코드만 담긴 일반 스프링 부트 앱이라면 이 제약이 실질 문제가 되지 않을 가능성이 크다. 이 문장은 이번 조사에서 **1차 소스로 확인하지 않았다.**)

#### Docker 데몬 없이 레지스트리 직행

`jib` / `jib:build`의 문서 서술은 "Builds and pushes a container image to a registry"이며, 프리퀴짓으로 Docker를 요구하지 않는다. 반면 `jibDockerBuild`는 "Builds directly to a local Docker daemon"으로 명시적으로 데몬을 쓴다. 두 태스크가 **분리되어 있다는 사실 자체**가 "`jib`은 데몬 없이 동작한다"의 구조적 근거다.

⚠️ 다만 "Docker 데몬 불필요"라는 **적극적 문장 자체는 이번 세션에서 확보하지 못했다.** 책에 쓸 때는 "레지스트리로 직접 push하는 태스크(`jib`)와 데몬으로 빌드하는 태스크(`jibDockerBuild`)가 별개다"라는 **관찰된 사실**로 쓰고, "데몬이 전혀 필요 없다"는 단정은 피하거나 (사실 확인 필요) 표시할 것.

### 3경로 비교표 (이번 조사로 채워진 부분)

| | Dockerfile + buildx | Paketo (`bootBuildImage`) | Jib |
|---|---|---|---|
| 1회 빌드 멀티아키 출력 | **가능** — `--platform linux/amd64,linux/arm64` (docker-container 드라이버) | **불가** — `imagePlatform` 단일 값 | **가능** — `platforms` 복수 지정 시 매니페스트 리스트 push (incubating) |
| 멀티아키 제약 | `--load`로 로컬 로드 불가(기본 스토어), `--push` 필요 | 아키텍처별 독립 빌드 후 `docker manifest`로 합성 | `jib`(레지스트리) 전용. `jibDockerBuild`·`jibBuildTar` 불가. OCI index 미지원 |
| 베이스 이미지 | 직접 `FROM` 지정 | 빌더가 결정 (`paketobuildpacks/builder-noble-java-tiny:latest`) | 기본 `eclipse-temurin:{8,11,17,21,25}-jre` |
| Docker 데몬 | 필요 | 필요 | `jib`은 레지스트리 직행 (위 ⚠️ 참조) |

**관련 섹션:** 스프링 부트 이미지 빌드 3경로 비교 / 맥에서 빌드해 서버에 배포하기

---

## G3. 베이스 이미지 선택 기준

### Google distroless

- URL: https://github.com/GoogleContainerTools/distroless
- 신뢰성: **최상** (프로젝트 공식 리포 README) / 발행일: 미확인 / 검색: 2026-07-25

**설계 의도 (원문):**
> "Distroless" images contain only your application and its runtime dependencies.

**무엇이 빠져 있나 (원문):**
> they do not include "package managers, shells or any other programs you would expect to find in a standard Linux distribution."

**자바 이미지 — 제공된다 (Debian 13 기준, README에서 읽은 목록):**
- `gcr.io/distroless/java-base-debian13`
- `gcr.io/distroless/java17-debian13`
- `gcr.io/distroless/java21-debian13`
- `gcr.io/distroless/java25-debian13`

아키텍처 변형: amd64, arm64, s390x, ppc64le, riscv64 → **arm64 제공. 맥에서 그대로 쓸 수 있다.**
태그 변형: `latest`, `nonroot`, `debug`, `debug-nonroot`

**디버그 변형 — 존재한다 (원문):**
디버그 이미지는 "a busybox shell to enter"를 제공한다. 이미 태그가 붙은 이미지(예: `java17-debian13:nonroot`)의 디버그 변형은 `debug-<기존 태그>` 형식 → `debug-nonroot`.

**Java 이미지 deprecated 여부:** README에 deprecated 표시 **없음**. `SUPPORT_POLICY.md`의 지원 정책 아래 유지 중으로 표기.

**책에서 쓸 각도:** distroless는 셸이 없다 → `docker exec ... sh`가 안 된다 → 그래서 `:debug` 태그가 따로 있다. 이 3단 논리가 자바 독자에게 distroless의 트레이드오프를 설명하는 가장 빠른 길이다.

### Alpine

- URL: https://www.alpinelinux.org/about/
- 신뢰성: **최상** (프로젝트 공식) / 발행일: 미확인 / 검색: 2026-07-25

> "Alpine Linux is built around musl libc and busybox. This makes it small and very resource efficient."

크기 수치(공식):
> "A container requires no more than 8 MB"
> "a minimal installation to disk requires around 130 MB of storage"

보안:
> "All userland binaries are compiled as Position Independent Executables (PIE) with stack smashing protection. These proactive security features prevent exploitation of entire classes of zero-day and other vulnerabilities."

### Debian slim

- URL: https://github.com/docker-library/docs/blob/master/debian/README.md
- 신뢰성: **최상** (Docker Official Images 문서) / 발행일: 미확인 / 검색: 2026-07-25

`-slim` 변형 설명 (원문):
> "These tags are an experiment in providing a slimmer base (removing some extra files that are normally not necessary within containers, such as man pages and documentation)"

제거 대상의 구체 명세는 `debuerreotype-slimify` 스크립트를 참조하라고 안내한다.

스위트 코드네임: `bookworm`(12), `bullseye`(11), `trixie`(13, latest 표시). `-slim`, `-backports` 변형과 `stable`/`testing`/`unstable`/`sid` 롤링 태그.
지원 아키텍처: **"amd64, arm32v5, arm32v7, arm64v8, i386, mips64le, ppc64le, riscv64, s390x"**

**책에서 쓸 각도:** slim은 "man page·문서를 뺀 것"이지 **런타임을 바꾼 게 아니다**(여전히 glibc/Debian). Alpine은 **libc 자체가 다르다**(musl). 이 차이가 자바에서 갈리는 지점이다.

### Eclipse Temurin (자바 전용 배포판)

- URL: https://github.com/docker-library/docs/blob/master/eclipse-temurin/README.md
- 신뢰성: **최상** (Docker Official Images 문서) / 발행일: 미확인 / 검색: 2026-07-25

**태그 라인업 (README에서 읽은 예시):** Java 8, 11, 17, 21, 25, 26 버전 축 × 배포판 축
- `eclipse-temurin:25-jdk-alpine-3.23` ← **Alpine 변형 존재, 그것도 JDK**
- `eclipse-temurin:25-jre-jammy`
- `eclipse-temurin:25-jdk-noble`
- `jammy`/`noble`/`resolute`는 "suite code names for releases of Ubuntu"

**지원 아키텍처 (원문):** "amd64, arm32v7, arm64v8, ppc64le, riscv64, s390x, windows-amd64" → **arm64 제공**

**Alpine 변형에 대한 공식 주의사항 (원문):**
> "Alpine Linux is much smaller than most distribution base images (~5MB), and thus leads to much slimmer images in general... the main caveat to note is that it does use musl libc instead of glibc and friends, so software will often run into issues depending on the depth of their libc requirements/assumptions."

**JRE에 대한 권고 (원문):**
> "JRE images are available for all versions of Eclipse Temurin but it is recommended that you produce a custom JRE-like runtime using jlink."

→ 책에서 `jlink`/커스텀 런타임 절의 근거로 쓸 수 있는 **공식 권고**다.

### BellSoft Liberica — Spring 공식 Dockerfile 예제가 쓰는 이미지 ⭐

- URL: https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html
- 문서 표기: **Spring Boot 4.1.0 문서 기준** / 발행일: 미확인 / 검색: 2026-07-25
- 신뢰성: **최상**

Spring Boot 공식 문서의 Dockerfile 예제는 **빌더 스테이지와 런타임 스테이지 모두** `bellsoft/liberica-openjre-debian:25-cds`를 쓴다. 표준 멀티스테이지 예제 원문:

```dockerfile
# Perform the extraction in a separate builder container
FROM bellsoft/liberica-openjre-debian:25-cds AS builder
WORKDIR /builder
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} application.jar
RUN java -Djarmode=tools -jar application.jar extract --layers --destination extracted

# This is the runtime container
FROM bellsoft/liberica-openjre-debian:25-cds
WORKDIR /application
COPY --from=builder /builder/extracted/dependencies/ ./
COPY --from=builder /builder/extracted/spring-boot-loader/ ./
COPY --from=builder /builder/extracted/snapshot-dependencies/ ./
COPY --from=builder /builder/extracted/application/ ./
ENTRYPOINT ["java", "-jar", "application.jar"]
```

**부수 수확 — 이건 책의 별도 절 하나를 만들 만하다:**
- `java -Djarmode=tools -jar application.jar extract --layers --destination extracted` — 레이어 분리 추출 명령 (원문 그대로)
- 문서의 주석: "This layout is efficient to start up and AOT cache (and CDS) friendly"
- **AOT 캐시 (Java 25+)**: 훈련 실행 `RUN java -XX:AOTCacheOutput=app.aot -Dspring.context.exit=onRefresh -jar application.jar` / 실행 `ENTRYPOINT ["java", "-XX:AOTCache=app.aot", "-jar", "application.jar"]`
- **CDS (Java 24+)**: 훈련 실행 `RUN java -XX:ArchiveClassesAtExit=application.jsa -Dspring.context.exit=onRefresh -jar application.jar` / 실행 `ENTRYPOINT ["java", "-XX:SharedArchiveFile=application.jsa", "-jar", "application.jar"]`
- 문서의 권고: **Java 25+에서는 CDS보다 AOT 캐시를 권장**

Liberica 자체의 태그 라인업(musl/alpine 변형 존재 여부)은 **미확인** — bell-sw.com 공식 문서를 이번 세션에서 열지 않았다.

### ⚠️ G3 핵심 판정 — "Alpine JDK는 Java API의 부분집합만 지원한다"

**판정: 이 주장을 뒷받침하는 공식 서술을 찾지 못했다. 책에 쓰지 말 것.**

반증에 가까운 1차 증거:
1. **Eclipse Temurin이 `eclipse-temurin:25-jdk-alpine-3.23`을 JDK로 배포한다.** 부분집합 런타임이라면 `jdk` 태그를 달 수 없다.
2. **공식 주의사항은 Java API가 아니라 libc 문제다.** Temurin README의 caveat은 "it does use musl libc instead of glibc and friends, so software will often run into issues depending on the depth of their libc requirements/assumptions" — 이는 **네이티브 라이브러리(JNI)·libc 의존 소프트웨어**의 호환성 문제지, Java 표준 API가 잘려 있다는 말이 아니다.

**민담의 기원 추정 (검증 실패 — 책에 쓰지 말 것):** OpenJDK의 Alpine/musl 포트 관련 JEP를 확인하려 https://openjdk.org/jeps/386 을 시도했으나 **HTTP 403으로 접근 실패**. JEP 번호·제목·상태 모두 **미확인**. 이번 세션에서 확인하지 못했으므로 인용하지 않는다.

**책에 쓸 형태:** "Alpine 자바 이미지의 진짜 주의점은 API가 아니라 musl libc다. 네이티브 라이브러리를 쓰는 의존성(일부 이미지 처리, 암호화, DB 드라이버)에서 문제가 날 수 있다" — 이건 Temurin 공식 caveat으로 근거가 있다. "Java API 부분집합"이라는 표현은 **금지**.

### 베이스 이미지 선택 요약표 (책 초안용)

| 후보 | 특징 | 공식 근거 |
|------|------|-----------|
| `eclipse-temurin:{ver}-jre-{noble\|jammy}` | Ubuntu 기반, glibc, 무난한 기본값 | docker-library/docs eclipse-temurin README |
| `eclipse-temurin:{ver}-jdk-alpine-{ver}` | ~5MB 베이스, **musl libc 주의** | 위 README caveat 원문 |
| `debian:{suite}-slim` | man page·문서 제거, 런타임은 그대로 | docker-library/docs debian README |
| `gcr.io/distroless/java{17\|21\|25}-debian13` | 셸·패키지 매니저 없음, `nonroot`/`debug` 변형 | GoogleContainerTools/distroless README |
| `bellsoft/liberica-openjre-debian:25-cds` | **Spring Boot 공식 문서 예제가 쓰는 이미지**, CDS/AOT 친화 | Spring Boot 4.1.0 문서 Dockerfile 예제 |

**관련 섹션:** `FROM` 한 줄 고르기 / 이미지 크기 다이어트 / 보안과 공격 표면

---

## G4. `docker scout` CLI

### 하위 명령 전체 목록 (공식 CLI 레퍼런스 원문)

- URL: https://docs.docker.com/reference/cli/docker/scout/
- 발행일: 미확인 / 검색: 2026-07-25 / 신뢰성: **최상**

| 명령 | 설명 (문서 원문) |
|------|------------------|
| `attestation` | Manage attestations on images |
| `cache` | Manage Docker Scout cache and temporary files |
| `compare` | Compare two images and display differences (experimental) |
| `config` | Manage Docker Scout configuration |
| `cves` | Display CVEs identified in a software artifact |
| `enroll` | Enroll an organization with Docker Scout |
| `environment` | Manage environments (experimental) |
| `help` | Display information about the available commands |
| `integration` | Commands to list, configure, and delete Docker Scout integrations |
| `policy` | Evaluate local Rego policies against an image and display the results (experimental) |
| `push` | Push an image or image index to Docker Scout |
| `quickview` | Quick overview of an image |
| `recommendations` | Display available base image updates and remediation recommendations |
| `repo` | Commands to list, enable, and disable Docker Scout on repositories |
| `sbom` | Generate or display SBOM of an image |
| `stream` | Manage streams (experimental) |
| `version` | Show Docker Scout version information |
| `vex` | Manage VEX attestations on images |
| `watch` | Watch repositories in a registry and push images and indexes to Docker Scout |

### 책에서 쓸 핵심
- `docker scout quickview` — 이미지 한 장 요약
- `docker scout cves` — "Display CVEs identified in a software artifact"
- `docker scout recommendations` — **"Display available base image updates and remediation recommendations"** → G3 "베이스 이미지 언제 올릴까"와 직결. 베이스 이미지 업데이트 권고를 도구가 직접 준다.
- `docker scout compare` — 두 이미지 비교. **문서에 `(experimental)` 표시 있음** → 책에 쓸 때 반드시 병기할 것.

### SBOM
**`docker scout sbom` 명령이 존재한다** — "Generate or display SBOM of an image". 별도 도구 없이 SBOM 생성·조회 가능.

### Docker Desktop 번들 여부 — **해소**

- URL: https://docs.docker.com/scout/install/
- 발행일: 미확인 / 검색: 2026-07-25 / 신뢰성: **최상**

> "The Docker Scout CLI plugin comes pre-installed with Docker Desktop."

> "If you run Docker Engine without Docker Desktop, Docker Scout doesn't come pre-installed, but you can install it as a standalone binary."

독립 설치 경로: 자동 설치 스크립트를 실행하거나, 릴리스 페이지에서 바이너리를 내려받아 `.docker/config.json`에 디렉터리를 추가해 Docker CLI 플러그인으로 등록.

→ **맥 독자(Docker Desktop 사용)는 추가 설치 없이 바로 `docker scout`을 쓸 수 있다.** 이건 책에서 실습 진입 장벽을 낮추는 좋은 재료다.

**관련 섹션:** 이미지 업데이트·취약점 스캔 / 베이스 이미지 유지보수

---

## G5. Docker Desktop 내장 Kubernetes

- URL: https://docs.docker.com/desktop/features/kubernetes/
- 발행일: 미확인 / 검색: 2026-07-25 / 신뢰성: **최상**

### 활성화 방법 (문서 원문)

> "Open the Docker Desktop Dashboard and select the **Kubernetes** view. Select **Create cluster**. Choose your cluster type: **Kubeadm** creates a single-node cluster and the version is set by Docker Desktop. **kind** creates a multi-node cluster and you can set the version and number of nodes."

⭐ **1차 리서치에 없던 중요한 발견.** Docker Desktop의 내장 Kubernetes가 **kubeadm / kind 두 가지 프로비저너 선택제**다. "설정에서 체크박스 하나 켜면 클러스터가 뜬다"는 옛 모델로 서술하면 틀린다.

### kubeadm vs kind 비교표 (문서에 실린 표 그대로)

| 항목 | kubeadm | kind |
|------|---------|------|
| 멀티 노드 지원 | No | Yes |
| 버전 선택 | No | Yes |
| 프로비저닝 속도 | ~1 min | ~30 seconds |
| ECI 지원 | No | Yes |
| Docker image store 호환 | Yes | **No** |
| containerd image store 호환 | Yes | Yes |

→ **kind가 Docker image store와 호환되지 않는다**는 항목이 실무적으로 가장 아프다. 로컬에서 `docker build`한 이미지를 kind 클러스터가 바로 못 본다는 뜻이고, 이건 자바 개발자가 "로컬에서 빌드해서 로컬 클러스터에 올린다" 흐름에서 정확히 부딪히는 벽이다. G6의 containerd image store 논의와 이어진다.

### 번들 Kubernetes 버전 — **문서에 명시 없음**

확인한 페이지(위 URL)에 **버전 숫자 명시 없음.** 문서가 안내하는 것은 직접 확인뿐이다:

> "check which version of Kubernetes you're on with: `kubectl version`"

- kubeadm 경로: "the version is set by Docker Desktop" (Docker Desktop이 정함, 사용자가 못 고름)
- kind 경로: "you can set the version" (사용자가 고름)

**책에는 특정 버전 숫자를 쓰지 말고 `kubectl version`으로 확인하라고 안내할 것.** 1차 리서치가 4.83.0 릴리스 노트에서 Kubernetes 버전을 못 찾은 것과 일관된다 — Docker가 이 숫자를 문서에 고정하지 않는 것으로 보인다.

### kind / minikube / Docker Desktop 선택 가이드
**확인한 페이지에서 minikube·독립 kind와의 비교를 찾지 못했다.** 확인 페이지: https://docs.docker.com/desktop/features/kubernetes/
다만 위 kubeadm vs kind 표 자체가 Docker Desktop 내부 선택 기준으로는 충분하고, **공식 표라서 인용 안전하다.**

**관련 섹션:** 로컬 쿠버네티스 / 컨테이너에서 오케스트레이션으로

---

## G6. `exec format error` / 멀티아키 트러블슈팅 공식 서술

### `exec format error`라는 문자열 — **확인한 페이지에서 찾지 못함**

확인 페이지:
- https://docs.docker.com/build/building/multi-platform/
- https://docs.docker.com/build/building/multi-platform.md
- docs.docker.com 도메인 한정 검색 (`"exec format error" architecture mismatch multi-platform`)

Docker 공식 문서가 이 오류 문자열 자체를 다루는 페이지는 확인 범위 안에서 없었다. **하지만 원인은 명확히 서술한다.** 아래가 이 증상을 설명할 공식 근거다.

### 아키텍처 불일치의 원인 (공식 서술)

- URL: https://docs.docker.com/build/building/multi-platform/ / 신뢰성: **최상** / 발행일: 미확인 / 검색: 2026-07-25

> "Multi-platform images contain a manifest list, pointing to multiple manifests, each of which points to a different configuration and set of layers."

컨테이너는 호스트 커널을 공유하므로 안에서 도는 코드가 호스트 아키텍처와 호환돼야 하고, 그래서 에뮬레이션 없이는 arm64 호스트에서 linux/amd64 컨테이너를 돌릴 수 없다 — 이것이 문서의 설명이다. 플랫폼을 지정하지 않았는데 로컬 캐시 이미지의 OS/아키텍처가 맞지 않으면, 가용 이미지로 컨테이너를 만들되 **플랫폼 불일치 경고**를 붙인다.

레지스트리 동작: 멀티플랫폼 이미지를 push하면 레지스트리가 매니페스트 리스트와 개별 매니페스트를 모두 저장하고, pull 시 레지스트리가 매니페스트 리스트를 돌려주면 Docker가 **호스트 아키텍처에 맞는 변형을 자동 선택**한다.

### 에뮬레이션 성능 (공식 서술)

> "Emulation with QEMU can be much slower than native builds, especially for compute-heavy tasks like compilation and compression or decompression."

→ 맥에서 amd64 이미지를 QEMU로 빌드할 때 느린 이유의 1차 근거. **자바 빌드는 정확히 "compute-heavy compilation" 범주다.** G1의 Paketo `imagePlatform=linux/amd64` 경로가 왜 아픈지도 이 문장으로 설명된다.

### 멀티플랫폼 빌드 3전략 (문서 구조 그대로)
1. **QEMU 에뮬레이션** — "the easiest way to get started", Dockerfile 수정 불필요, BuildKit이 가용 아키텍처 자동 감지
2. **여러 네이티브 노드** — 아키텍처별 빌더 분리, 복잡한 빌드에서 성능 우위
3. **크로스 컴파일** — 멀티스테이지 + `BUILDPLATFORM`, `TARGETOS`, `TARGETARCH` 빌드 인자

### containerd 이미지 스토어 (⚠️ 반드시 원문 그대로 인용)

> "Docker Desktop and Docker Engine 29.0+ use the containerd image store by default, which supports multi-platform images out of the box."

> "Builds with the `docker-container` driver aren't automatically loaded to your Docker Engine image store."

⚠️ 이 두 문장은 **의역 금지.** 같은 문서를 두 번 페치했을 때 이 부분의 렌더링 범위가 미묘하게 달랐다. 바꿔 쓰면 오류가 주입된다. 특히 "Docker Engine 29.0+"라는 버전 경계는 원문 그대로만 쓸 것.

### `--load` / `--push` / `--platform` — 공식 CLI 레퍼런스로 확정

- URL: https://docs.docker.com/reference/cli/docker/buildx/build/
- 발행일: 미확인 / 검색: 2026-07-25 / 신뢰성: **최상**

| 옵션 | 문서 원문 |
|------|-----------|
| `--load` | "Shorthand for `--output=type=docker`" — 단일 플랫폼 빌드 결과를 `docker images`에 자동 로드 |
| `--push` | "Shorthand for `--output=type=registry`" — 결과를 레지스트리에 자동 push |
| `--platform` | "Set the target platform for the build. All `FROM` commands inside the Dockerfile without their own `--platform` flag will pull base images for this platform." |
| `--output` | "Sets the export action for the build result." 형식: `-o, --output=[PATH,-,type=TYPE[,KEY=VALUE]` |

⭐ **핵심 제약 (원문):**
> "The default image store in Docker Engine doesn't support loading multi-platform images."

⭐ **`--platform`의 복수 값 (문서 서술):** 값의 형태는 `os/arch` 또는 `os/arch/variant`(예: `linux/amd64`). **`docker-container` 드라이버를 쓸 때는 콤마로 구분한 여러 값을 지정할 수 있고, 그 결과 모든 플랫폼에 대한 매니페스트 리스트가 만들어진다.**

→ **이게 G1과의 결정적 대비다.** buildx의 `--platform`은 콤마 목록을 받는다. pack의 `--platform string`은 안 받는다. Spring의 `imagePlatform`도 안 받는다.

### ⚠️ `--load` 제약의 진짜 조건 — 이미지 스토어에 따라 갈린다 (절대 규칙으로 쓰지 말 것)

같은 Docker 문서 안에 얼핏 충돌하는 두 문장이 있다:

> (A) "The default image store in Docker Engine doesn't support loading multi-platform images." — buildx build CLI 레퍼런스
> (B) "Docker Desktop and Docker Engine 29.0+ use the containerd image store by default, which supports multi-platform images out of the box." — multi-platform 문서

**해소됨.** 세 번째 1차 소스가 조건을 확정한다:

- URL: https://docs.docker.com/engine/storage/containerd/
- 발행일: 미확인 / 검색: 2026-07-25 / 신뢰성: **최상**

> "Building and storing multi-platform images locally. With classic storage drivers, you need external builders for multi-platform images."

> "The containerd image store is the default storage backend for Docker Engine 29.0 and later on fresh installations."

> "If you upgraded from an earlier version, your daemon continues using the legacy graph drivers (overlay2) until you enable the containerd image store."

**즉 (A)의 "default image store"는 classic/legacy 그래프 드라이버(overlay2)를 가리키는, containerd 전환 이전 시점의 서술이다.** 두 문장은 모순이 아니라 **스토어 세대가 다르다.**

**책에 쓸 실무 규칙 (버전 조건부로 쓸 것):**
- **containerd 이미지 스토어**를 쓰면 멀티플랫폼 이미지를 로컬에 빌드·저장할 수 있다. Docker Desktop과 **Docker Engine 29.0+ 신규 설치**는 기본이 containerd다 → **맥에서 Docker Desktop을 쓰는 이 책의 독자는 대체로 여기에 해당한다.**
- **classic 스토리지 드라이버**(구버전에서 업그레이드해 overlay2를 계속 쓰는 경우)라면 멀티플랫폼 이미지를 로컬에 못 넣는다 → 외부 빌더 + **`--push`로 레지스트리 경유**가 필요하다
- 콤마로 여러 플랫폼을 쓰려면 `docker-container` 드라이버 빌더가 필요하다
- 단일 플랫폼이면 어느 쪽이든 `--load`로 로컬 확인 가능

⚠️ **"멀티플랫폼은 `--load` 못 한다"를 무조건 규칙으로 쓰면 틀린다.** 독자 환경(스토어 종류)에 따라 갈린다. 책에서는 반드시 "내 스토어가 무엇인지 확인하는 법"을 먼저 안내한 뒤 조건부로 서술할 것. (스토어 확인 명령 자체는 이번 세션에서 공식 문서로 확인하지 않았다 — **(사실 확인 필요)**)

### ⭐ 책에서 가르칠 정석 확인 명령: `docker buildx imagetools inspect`

- URL: https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/
- 신뢰성: **최상** / 발행일: 미확인 / 검색: 2026-07-25

설명 (원문): **"Show details of an image in the registry"**
사용법 (원문): `docker buildx imagetools inspect [OPTIONS] NAME`

주요 옵션:
- `--format` — "Format the output using the given Go template" (기본값 `{{.Manifest}}`)
- `--raw` — "Show original, unformatted JSON manifest"

문서에 실린 예제 (그대로):
```console
$ docker buildx imagetools inspect moby/buildkit:master --format "{{.Manifest}}"
```
```console
$ docker buildx imagetools inspect --raw moby/buildkit:master | jq
```

두 방식 모두 이미지가 지원하는 플랫폼(linux/amd64, linux/arm64, linux/s390x 등)을 드러낸다.

⚠️ **"내 이미지가 무슨 아키텍처인가"를 확인하는 방법으로는 이 명령만 가르칠 것.** `docker image inspect --format '{{.Os}}/{{.Architecture}}'` 같은 다른 명령은 이번 세션에서 공식 문서로 확인하지 않았으므로 쓰지 말 것.

**관련 섹션:** 멀티아키 트러블슈팅 / 맥에서 빌드해 서버에 배포하기 / 첫 배포 실패기(오프닝 후보)

---

## G7. 한국어 최신 사례

### 결론: **이번 조사(도메인 한정 검색 3회) 범위에서 "컨테이너 × 멀티아키 × Apple Silicon" 주제의 2023년 이후 한국어 글을 찾지 못했다**

⚠️ **이걸 "국내에 이런 글이 사실상 없다"로 격상하지 말 것.** 근거는 US 기반 검색 도구의 도메인 한정 검색 3회뿐이고, 그 정도로는 부재를 증명할 수 없다. 아래 검색 표가 정직한 산출물이고, "없다"는 판정은 산출물이 아니다. **서문 포지셔닝 문구로 인용 금지** — 서문은 검증 불가능한 단정이 그대로 굳는 자리다.

### 수행한 검색 (도메인 한정)
| 검색어 | 대상 도메인 | 결과 |
|--------|------------|------|
| `Apple Silicon 컨테이너 멀티아키텍처 arm64 amd64 도커 빌드 배포` | d2.naver.com, toss.tech, techblog.woowahan.com, tech.kakao.com, engineering.linecorp.com, techblog.lycorp.co.jp | 멀티아키 직결 한국어 글 **0건** |
| `도커 컨테이너 이미지 빌드 스프링 부트 배포 쿠버네티스 2024 2025` | techblog.woowahan.com, toss.tech, tech.kakao.com, d2.naver.com | 쿠버네티스·배포 파이프라인 글 다수, **멀티아키·Apple Silicon 직결 0건** |
| `M1 맥북 Apple Silicon 도커 arm64 로컬 개발 환경` | 위 5개 도메인 | **0건** |

### 유일한 근접 자료 (한국어 아님)

**"Docker Bake 食譜公開：一次烤出多種 Image"**
- URL: https://techblog.lycorp.co.jp/zh-hant/docker-bake
- 저자: Zion Lee (EC Dev UIT Engineer)
- 언어: **번체 중국어** (한국어판 링크 없음)
- 발행일: **미확인** (페이지에 날짜 표기를 찾지 못함)
- 신뢰성: **중** (회사 엔지니어링 블로그이나 날짜 미확인 + 한국어 아님)
- 내용: Bake 설정에서 `--platform linux/amd64,linux/arm64`를 다루고, `docker buildx`의 동시 다중 아키텍처 빌드를 설명. Docker Bake를 "빌드 타깃·태그·플랫폼·시크릿·캐시를 하나의 레시피로 묶는 오케스트레이션 도구"로 소개.
- **활용법:** 인용보다는 "LY Corp에서도 Bake로 멀티아키를 묶어 관리한다" 정도의 맥락 예시. 버전·플래그의 근거로는 쓰지 말 것(2차 소스).

### 참고로 확보된 국내 컨테이너·배포 사례 (멀티아키 아님, 배경용)
- 우아한형제들 "쿠버네티스를 이용해 테스팅 환경 구현해보기" — https://techblog.woowahan.com/2562/ (발행일 미확인)
- 우아한형제들 "안정적인 AI 서빙 시스템 + 자동화" — https://techblog.woowahan.com/19548/ (발행일 미확인)
- 카카오 "쿠버네티스 프로비저닝 툴과의 만남부터 헤어짐까지" — https://tech.kakao.com/2023/02/10/making-of-kubernetes-provisioning-tool/ (URL에 **2023-02-10** 표기)
- LINE "Private Docker Registry를 구축하기 위한 오픈소스 Harbor 도입기" — https://engineering.linecorp.com/ko/blog/harbor-for-private-docker-registry/ (발행일 미확인)

⚠️ 위 4건은 **제목·URL만 확인**했고 본문을 열지 않았다. 인용하려면 별도 확인 필요.

**관련 섹션:** 서문(왜 이 책이 필요한가) / 국내 사례 부족을 근거로 한 포지셔닝

---

## 미확인 목록

| 항목 | 무엇을 확인했고 왜 못 찾았나 |
|------|------------------------------|
| pack issue #1570의 종료 사유·최종 코멘트 | https://github.com/buildpacks/pack/issues/1570 을 열었으나 페이지 추출이 메인테이너 코멘트를 반환하지 않음. 번호·제목·Closed 상태·생성일(2022-12-06)까지만 확인. **"멀티아키 구현되어 닫힘"의 근거로 쓰지 말 것** |
| Jib 릴리스 날짜 전부 | GitHub Releases 추출이 최신 3건을 2024-07-14로 보고했으나 같은 릴리스의 변경 내용에 "Java 25 지원"이 있어 날짜가 명백히 틀림. **버전 번호만 채택, 날짜 전부 미확인 처리** |
| Jib "Docker 데몬 불필요"의 적극적 문장 | jib-maven/gradle README에서 `jib`(레지스트리)와 `jibDockerBuild`(데몬)의 분리는 확인. 그러나 "does not require a Docker daemon"류 명시 문장은 확보 못 함. 구조적 추론으로만 쓰고 단정 금지 |
| OpenJDK Alpine/musl 포트 JEP | https://openjdk.org/jeps/386 시도 → **HTTP 403 Forbidden**. 1회 재시도 여력을 다른 갭에 배분. JEP 번호·제목·상태 전부 미확인. **인용 금지** |
| "Alpine JDK = Java API 부분집합" 주장 | 공식 근거를 찾지 못함. 반대로 Temurin이 `25-jdk-alpine-3.23`을 JDK로 배포하고, 공식 caveat은 musl libc 호환성 문제. **이 주장을 책에 쓰지 말 것 (반증 우세)** |
| `exec format error` 문자열의 Docker 공식 서술 | multi-platform 문서 2판 + docs.docker.com 도메인 검색에서 미발견. 원인 설명(커널 공유·아키텍처 호환)은 확보. **"공식 문서에 없다"고 단정하지 말고 "확인한 페이지에서 못 찾았다"로 표기** |
| Docker Desktop 번들 Kubernetes 버전 숫자 | https://docs.docker.com/desktop/features/kubernetes/ 에 숫자 명시 없음. 문서는 `kubectl version`으로 확인하라고만 안내. 1차 리서치의 4.83.0 릴리스 노트 결과와 일관 |
| minikube/독립 kind vs Docker Desktop 공식 비교 | Docker Desktop Kubernetes 페이지에 없음. kubeadm vs kind 표만 확보 |
| BellSoft Liberica 태그 라인업 (alpine/musl 변형) | Spring Boot 문서의 `bellsoft/liberica-openjre-debian:25-cds` 사용만 확인. bell-sw.com 공식 문서 미열람 |
| Docker Bake 기사 발행일 | techblog.lycorp.co.jp 페이지에서 날짜 표기를 찾지 못함 |
| 내 Docker가 어느 이미지 스토어를 쓰는지 확인하는 명령 | containerd 스토어 문서에서 스토어 종류·버전 경계는 확보했으나, **확인 명령 자체**는 이번 세션에서 공식 문서로 읽지 않았다. 책에 쓰려면 별도 확인 필요 — **(사실 확인 필요)** |
| Jib 멀티플랫폼이 순수 JVM 앱에서 실질 제약이 없는지 | FAQ는 "크로스 컴파일 미지원 / platform-specific binaries needed"까지만 말한다. "순수 바이트코드 앱은 무관"은 **저자 해석이며 1차 소스 미확인** |

### ✅ 이번 라운드에서 해소된 항목 (이전 초안의 미확인에서 제거)
- **CNB RFC 0128 본문** → 직접 열람 완료. Approved 상태, 범위가 "statement 2"(빌더·패키지)로 명시 한정됨을 원문으로 확인. G1의 결정적 보강 증거가 됨
- **`--load` 멀티플랫폼 제약의 조건** → https://docs.docker.com/engine/storage/containerd/ 로 해소. classic 드라이버 vs containerd 스토어의 차이였음. 절대 규칙이 아니라 **버전·스토어 조건부**

---

## 신선도 원장 (이번 보강분)

| 주장 | 값 | 1차 소스 URL | 발행일 | 검색 시점 |
|------|-----|--------------|--------|-----------|
| Spring Boot Gradle `imagePlatform` 형식 | `OS[/architecture[/variant]]`, 단일 값, 기본값 없음(호스트 플랫폼) | https://docs.spring.io/spring-boot/gradle-plugin/packaging-oci-image.html | 미확인 (문서 표기 4.1.0 기준) | 2026-07-25 |
| Spring Boot Maven `imagePlatform` since 버전 | 3.4.0 | https://docs.spring.io/spring-boot/maven-plugin/build-image.html | 미확인 (문서 표기 4.1.0 기준) | 2026-07-25 |
| Paketo 기본 빌더 이미지 | `paketobuildpacks/builder-noble-java-tiny:latest` | https://docs.spring.io/spring-boot/gradle-plugin/packaging-oci-image.html | 미확인 | 2026-07-25 |
| `pack build --platform` 타입 | `string` (단수) — 1회 1플랫폼 | https://buildpacks.io/docs/for-platform-operators/how-to/integrate-ci/pack/cli/pack_build/ | 미확인 | 2026-07-25 |
| CNB 교차 아키텍처 앱 이미지 빌드 | 미지원 (QEMU 에뮬레이션 시 가능, 성능 페널티) | https://buildpacks.io/docs/for-app-developers/how-to/special-cases/build-for-arm/ | 미확인 | 2026-07-25 |
| CNB 멀티아키 빌더 예시 | `heroku/builder:24` (amd64 + arm64) | https://buildpacks.io/docs/for-app-developers/how-to/special-cases/build-for-arm/ | 미확인 | 2026-07-25 |
| pack CLI 최신 버전 | **v0.40.8** | https://github.com/buildpacks/pack/releases | **2026-07-13** | 2026-07-25 |
| pack v0.40.0 릴리스 | v0.40.0 | https://github.com/buildpacks/pack/releases | 2026-02-03 | 2026-07-25 |
| `jib-maven-plugin` 버전 | **3.5.2** | https://github.com/GoogleContainerTools/jib/blob/master/jib-maven-plugin/README.md + /releases | **미확인** (Releases 날짜 추출 오류) | 2026-07-25 |
| `jib-gradle-plugin` 버전 | **3.5.4** | https://github.com/GoogleContainerTools/jib/blob/master/jib-gradle-plugin/README.md + /releases | **미확인** (동일) | 2026-07-25 |
| `jib-core` 버전 | 0.28.2 | https://github.com/GoogleContainerTools/jib/releases | 미확인 | 2026-07-25 |
| Jib 기본 베이스 이미지 | `eclipse-temurin:{8,11,17,21,25}-jre` (WAR은 `jetty`) | jib-maven-plugin / jib-gradle-plugin README | 미확인 | 2026-07-25 |
| Jib 멀티플랫폼 출력 | 복수 platform 지정 시 매니페스트 리스트 생성·push (incubating) | https://github.com/GoogleContainerTools/jib/blob/master/docs/faq.md | 미확인 | 2026-07-25 |
| Jib 멀티플랫폼 제약 | OCI index 미지원, `jibDockerBuild`/`jibBuildTar` 불가, variant 미지원, 크로스 컴파일 미지원 | 위 FAQ | 미확인 | 2026-07-25 |
| distroless 자바 이미지 태그 | `gcr.io/distroless/java{17,21,25}-debian13`, `java-base-debian13` | https://github.com/GoogleContainerTools/distroless | 미확인 | 2026-07-25 |
| distroless 태그 변형 | `latest`, `nonroot`, `debug`, `debug-nonroot` | 위 | 미확인 | 2026-07-25 |
| distroless 아키텍처 | amd64, arm64, s390x, ppc64le, riscv64 | 위 | 미확인 | 2026-07-25 |
| Alpine 컨테이너 크기 | "no more than 8 MB" | https://www.alpinelinux.org/about/ | 미확인 | 2026-07-25 |
| Alpine 디스크 설치 크기 | "around 130 MB" | https://www.alpinelinux.org/about/ | 미확인 | 2026-07-25 |
| Temurin Alpine 태그 예시 | `eclipse-temurin:25-jdk-alpine-3.23` | https://github.com/docker-library/docs/blob/master/eclipse-temurin/README.md | 미확인 | 2026-07-25 |
| Temurin 지원 아키텍처 | amd64, arm32v7, arm64v8, ppc64le, riscv64, s390x, windows-amd64 | 위 | 미확인 | 2026-07-25 |
| Alpine 베이스 크기 (Temurin 문서 표기) | "~5MB" | 위 | 미확인 | 2026-07-25 |
| Debian 스위트 코드네임 | bookworm(12), bullseye(11), trixie(13, latest) | https://github.com/docker-library/docs/blob/master/debian/README.md | 미확인 | 2026-07-25 |
| Spring Boot 공식 Dockerfile 베이스 이미지 | `bellsoft/liberica-openjre-debian:25-cds` | https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html | 미확인 (문서 표기 4.1.0 기준) | 2026-07-25 |
| Spring Boot 레이어 추출 명령 | `java -Djarmode=tools -jar application.jar extract --layers --destination extracted` | 위 | 미확인 | 2026-07-25 |
| AOT 캐시 플래그 (Java 25+) | `-XX:AOTCacheOutput=app.aot` / `-XX:AOTCache=app.aot` | 위 | 미확인 | 2026-07-25 |
| CDS 플래그 (Java 24+) | `-XX:ArchiveClassesAtExit=application.jsa` / `-XX:SharedArchiveFile=application.jsa` | 위 | 미확인 | 2026-07-25 |
| Spring 권고: CDS vs AOT | Java 25+에서는 AOT 캐시 권장 | 위 | 미확인 | 2026-07-25 |
| `docker scout` 하위 명령 수 | 19개 (표 참조), `compare`/`environment`/`policy`/`stream`은 experimental | https://docs.docker.com/reference/cli/docker/scout/ | 미확인 | 2026-07-25 |
| Docker Scout 번들 여부 | "comes pre-installed with Docker Desktop" / Docker Engine 단독은 별도 설치 | https://docs.docker.com/scout/install/ | 미확인 | 2026-07-25 |
| Docker Desktop Kubernetes 프로비저너 | kubeadm(단일 노드) / kind(멀티 노드) 선택제 | https://docs.docker.com/desktop/features/kubernetes/ | 미확인 | 2026-07-25 |
| Docker Desktop 번들 K8s 버전 | **문서에 명시 없음** — `kubectl version`으로 확인 | 위 | 미확인 | 2026-07-25 |
| kind의 Docker image store 호환 | **No** (containerd image store는 Yes) | 위 | 미확인 | 2026-07-25 |
| containerd 이미지 스토어 기본 적용 경계 | "Docker Desktop and Docker Engine 29.0+ use the containerd image store by default" | https://docs.docker.com/build/building/multi-platform/ | 미확인 | 2026-07-25 |
| `--load` 정의 | "Shorthand for `--output=type=docker`" | https://docs.docker.com/reference/cli/docker/buildx/build/ | 미확인 | 2026-07-25 |
| `--push` 정의 | "Shorthand for `--output=type=registry`" | 위 | 미확인 | 2026-07-25 |
| 멀티플랫폼 `--load` 제약 (classic 스토어 한정) | "The default image store in Docker Engine doesn't support loading multi-platform images." — **classic/legacy 그래프 드라이버 기준** | 위 | 미확인 | 2026-07-25 |
| containerd 스토어의 멀티플랫폼 로컬 지원 | "Building and storing multi-platform images locally. With classic storage drivers, you need external builders for multi-platform images." | https://docs.docker.com/engine/storage/containerd/ | 미확인 | 2026-07-25 |
| containerd 스토어 기본 적용 조건 | "The containerd image store is the default storage backend for Docker Engine 29.0 and later on **fresh installations**" | 위 | 미확인 | 2026-07-25 |
| 업그레이드 설치의 스토어 | "your daemon continues using the legacy graph drivers (overlay2) until you enable the containerd image store" | 위 | 미확인 | 2026-07-25 |
| CNB RFC 0128 범위 | 빌더·빌드팩 패키지 한정 ("solve the statement 2": `pack buildpack package`, `pack builder create`). 앱 이미지 멀티아키(statement 3)는 대상 아님. 상태 **Approved** | https://github.com/buildpacks/rfcs/blob/main/text/0128-multiarch-builders-and-package.md | 미확인 | 2026-07-25 |
| `--platform` 복수 값 조건 | `docker-container` 드라이버에서 콤마 구분 복수 지정 → 매니페스트 리스트 생성 | 위 | 미확인 | 2026-07-25 |
| `docker buildx imagetools inspect` 설명 | "Show details of an image in the registry" | https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/ | 미확인 | 2026-07-25 |
| `imagetools inspect --format` 기본값 | `{{.Manifest}}` | 위 | 미확인 | 2026-07-25 |
| 국내 5대 기술블로그 멀티아키/Apple Silicon 글 | **0건 (확인 범위 내)** | 도메인 한정 검색 3회 (G7 표 참조) | 해당 없음 | 2026-07-25 |

---

## 조사 한계 (정직 고지)

1. **발행일 대부분이 "미확인"이다.** 공식 문서 페이지(docs.docker.com, docs.spring.io, buildpacks.io, GitHub README)는 대체로 발행일을 노출하지 않는다. 대신 **문서 표기 버전**(Spring Boot 4.1.0)과 **검색 시점**(2026-07-25)을 앵커로 삼았다. GitHub Releases만 날짜를 주는데, Jib은 그 날짜조차 신뢰할 수 없었다(위 미확인 목록).
2. **WebFetch 추출 편차.** 같은 URL의 두 판(`multi-platform/`과 `multi-platform.md`)이 서로 다른 발췌를 냈다. 그래서 부재 판정은 전부 "확인한 페이지에서 못 찾음"으로 약하게 기술했고, 핵심 문장(containerd/29.0+)은 원문 인용 강제 표시를 붙였다.
   - **문서 간 충돌 1건을 발견하고 해소했다.** buildx CLI 레퍼런스의 "default image store doesn't support loading multi-platform images"와 multi-platform 문서의 "Docker Engine 29.0+ use the containerd image store by default, which supports multi-platform images out of the box"가 정면 충돌하는 것처럼 보였다. 추론으로 메우지 않고 세 번째 1차 소스(containerd 스토어 문서)를 열어 **"classic 드라이버 vs containerd 스토어"라는 조건 차이**임을 확정했다. 이 항목은 이 책의 핵심 축(맥에서 빌드 → 서버 배포)에 직결되므로, 절대 규칙으로 서술했다면 독자 다수에게 틀린 지시가 됐을 것이다.
3. **openjdk.org 403** 1건. 재시도 대신 다른 갭에 예산을 배분했고, 해당 주장(Alpine JDK 부분집합설)은 다른 1차 증거로 반증 우세 판정을 냈다.
4. **개인 블로그·Medium·Stack Overflow는 이번 조사에서 한 건도 채택하지 않았다.** 버전·플래그·기본값은 전부 공식 1차 소스에서만 읽었다.
