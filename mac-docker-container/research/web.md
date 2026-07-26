<!-- 검색 시점: 2026-07-25 기준 -->
# 웹 리서치: 맥에서의 컨테이너 기술 (tech-book)
**검색 시점:** 2026-07-25 / **genre:** tech-book / **슬러그:** mac-docker-container

> **읽는 법.**
> - 이 문서의 모든 버전·수치는 "2026-07-25에 그 URL을 열어서 읽은 값"이다. 열어보지 않은 값은 `미확인`으로 남겼다.
> - `docs.spring.io/spring-boot/...`, `docs.docker.com/...`처럼 **버전 없는 URL**은 그날의 current 문서를 서빙한다. "이게 최신 GA다"라고 단정하지 말고 "2026-07-25에 렌더된 문서가 X를 표기했다"로 쓸 것.
> - 로컬 실측값은 `research/env_probe.md`(표본 1, 일반화 금지). 이 문서의 공개 릴리스 라인과 어긋나거나 일치하는 지점은 `## 상충 기록`에 모았다.
> - **레지스트리 직접 조회(`docker buildx imagetools inspect --raw`)** 로 얻은 매니페스트는 문서가 아니라 레지스트리의 현재 상태다. 최상급 1차 근거지만 "2026-07-25 시점의 `:latest` 태그 상태"라는 시점 한정이 붙는다.

---

## E. Spring 애플리케이션 컨테이너화 (사용자 요구 2번 — 최우선)

### E-0. Spring Boot 현재 릴리스 라인 (3.x인가 4.x인가)

- **출처:** Releases · spring-projects/spring-boot — https://github.com/spring-projects/spring-boot/releases (검색: 2026-07-25) · **신뢰성: 최상**
- 확인된 것: **`v4.1.0`이 "Latest" 배지를 단 현재 GA**다. 같은 목록에 `v4.0.7`, `v3.5.16`, `v3.5.15`, `v4.1.0-RC1`이 함께 보였다 → **4.x가 현재 라인이고 3.5.x가 병행 유지되는 구도.**
- **⚠️ 발행일은 미확인.** 이 페이지 조회 요약이 보고한 날짜(예: "v4.1.0 — June 10, 2024")는 **신뢰할 수 없다.** 근거: 같은 방식으로 조회한 kind 릴리스가 "v0.32.0 — June 2, 2025"라고 보고됐는데, 그 릴리스가 담은 노드 이미지가 `kindest/node:v1.36.1`이다 — Kubernetes 1.36은 2026-06-09 릴리스(F-1)이므로 2025-06에 존재할 수 없다. **즉 GitHub Releases 페이지의 날짜 추출이 체계적으로 어긋났다.** 두 도구 보고 모두 날짜를 버리고 버전만 채택한다. (상충 기록 9)
- **책에서의 함의:** 대상 독자(자바/스프링 백엔드)가 3.x를 쓰고 있을 가능성이 크다. `imagePlatform`은 **3.4.0부터**(E-1)이므로 3.4 미만 독자에게는 이 옵션 자체가 없다. **버전 분기 안내를 챕터에 넣어야 한다.**

### E-1. `bootBuildImage` / `spring-boot:build-image` — 기본 빌더와 플랫폼 옵션

2026-07-25에 렌더된 Spring Boot 공식 플러그인 레퍼런스(페이지 상단 표기 **Spring Boot 4.1.0**)에서 직접 읽었다. Gradle·Maven 두 페이지가 같은 값을 말한다.

- **기본 빌더 이미지:** `paketobuildpacks/builder-noble-java-tiny:latest`
  > "The default builder `paketobuildpacks/builder-noble-java-tiny:latest` contains a reduced set of system libraries and does not include a shell."
- **`imagePlatform` 옵션이 존재한다.** Maven CLI 프로퍼티는 `spring-boot.build-image.imagePlatform`.
  > "The platform (operating system and architecture) of any builder, run, and buildpack images that are pulled. Must be in the form of `OS[/architecture[/variant]]`, such as `linux/amd64`, `linux/arm64`, or `linux/arm/v5`. Refer to documentation of the builder being used to determine the image OS and architecture options available."
- **⭐ 이 책에서 가장 값진 한 줄 — `imagePlatform`의 기본값:**
  > "No default value, indicating that the platform of the host machine should be used."

  → **Apple Silicon 맥에서 아무 설정 없이 `./gradlew bootBuildImage`를 돌리면 호스트 플랫폼(=linux/arm64)이 쓰인다**는 것이 공식 문서에 적힌 동작이다. "내 맥에서 만든 이미지가 운영 amd64 서버에서 안 돈다"의 1차 소스 근거. 블로그를 인용할 필요가 없다.
- **도입 버전:** `imagePlatform`은 **Since `3.4.0`** (Maven 플러그인 파라미터 상세에 명시).
- **`bootBuildImage` 설정 옵션 전체 목록(Gradle 문서에 나열된 것 그대로):** `builder`, `trustBuilder`, `imagePlatform`, `runImage`, `imageName`, `pullPolicy`, `environment`, `buildpacks`, `bindings`, `network`, `cleanCache`, `verboseLogging`, `publish`, `tags`, `buildWorkspace`, `buildCache`, `launchCache`, `createdDate`, `applicationDirectory`, `securityOptions`

- **출처:** Packaging OCI Images :: Spring Boot (Maven Plugin) — https://docs.spring.io/spring-boot/maven-plugin/build-image.html (페이지 표기 버전 4.1.0 / 발행일 미확인 — 무버전 URL, 검색: 2026-07-25) · **신뢰성: 최상**
- **출처:** Packaging OCI Images :: Spring Boot (Gradle Plugin) — https://docs.spring.io/spring-boot/gradle-plugin/packaging-oci-image.html (페이지 표기 버전 4.1.0 / 발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- **⚠️ 추론과 인용의 경계:** 위 `imagePlatform` 문구가 직접 말하는 것은 **"pull되는 builder·run·buildpack 이미지의 플랫폼"** 이다. "따라서 **결과 이미지**가 arm64가 된다"는 두 단계 추론이다 — (a) pull 기본값 = 호스트 플랫폼(위 인용) + (b) `run-noble-tiny`가 arm64 매니페스트를 실제로 퍼블리시함(E-2 레지스트리 조회). 두 근거 모두 확보했으므로 결론은 견고하지만, **"공식 문서에 결과 이미지가 arm64라고 적혀 있다"고 쓰면 안 된다.** 책에서는 두 단계를 그대로 보여주는 편이 오히려 좋은 교육 소재다.
- **관련 섹션:** Spring 컨테이너화 챕터 / arm64 함정 챕터

### E-2. ⭐ Paketo 빌더가 arm64 매니페스트를 실제로 퍼블리시하는가 — 레지스트리 직접 조회로 해소

과제가 지정한 정확한 질문("빌더 이미지 **자체**가 arm64 매니페스트를 퍼블리시하는가")에 대해, 문서·블로그를 거치지 않고 레지스트리에 직접 물었다.

```
$ docker buildx imagetools inspect paketobuildpacks/builder-noble-java-tiny:latest --raw
{"schemaVersion":2,"mediaType":"application/vnd.oci.image.index.v1+json","manifests":[
 {"...","digest":"sha256:fad9e3b0dceee89ea705ca81992936a598cf4b4b83ffce3f3d47396d152b80f0",
  "platform":{"architecture":"amd64","os":"linux"}},
 {"...","digest":"sha256:bbdd0f25e8caf9e89a57fe32f7275b919f682e266dd8c26880aa25a2b6d27eed",
  "platform":{"architecture":"arm64","os":"linux"}}]}
```

**확인된 사실 (2026-07-25 조회):**

| 이미지 | 퍼블리시된 플랫폼 |
|---|---|
| `paketobuildpacks/builder-noble-java-tiny:latest` (Spring Boot 기본 빌더) | linux/amd64, linux/arm64 |
| `paketobuildpacks/run-noble-tiny:latest` (해당 run 이미지) | linux/amd64, linux/arm64 |
| `paketobuildpacks/builder-jammy-java-tiny:latest` (이전 세대) | linux/amd64, linux/arm64 |

- 미디어 타입이 `application/vnd.oci.image.index.v1+json` — **OCI 이미지 인덱스(멀티아키 매니페스트 리스트)** 다. 즉 빌더도 run 이미지도 arm64 매니페스트를 갖고 있다.
- **따라서:** Apple Silicon 맥에서 `bootBuildImage`를 돌리면 (a) 빌더가 arm64로 당겨지고 (b) 결과 이미지도 arm64가 된다. (a)는 위 조회, (b)는 E-1의 `imagePlatform` 기본값 문구가 근거다.
- **조사 방법 명시:** 조회 시점 2026-07-25, 조회 도구 `docker buildx imagetools inspect --raw` (buildx v0.35.0-desktop.2, 데몬 Docker Desktop 29.6.2 — `env_probe.md` 참조). `:latest` 태그의 현재 상태이므로 시간이 지나면 digest는 달라진다. 책에는 digest를 못 박지 말고 "당시 조회 결과 amd64/arm64 두 매니페스트가 있었다"로 쓸 것.
- **신뢰성: 최상** (레지스트리 원본 응답)
- **관련 섹션:** Spring 컨테이너화 챕터 / arm64 함정 챕터

### E-3. Paketo의 arm64 지원 경위 — 프로젝트 공식 논의

- **출처:** Arm64 (beta) Support for Paketo Buildpacks · paketo-buildpacks/java · Discussion #1387 — https://github.com/paketo-buildpacks/java/discussions/1387 (저자: anthonydahanne(메인테이너), 최초 게시 2024-04-04, 코멘트 2024-07-27까지, 검색: 2026-07-25) · **신뢰성: 최상**
- 읽은 사실:
  - 2024-04-04 beta 공지로 시작. 메인테이너 코멘트: **"UPDATED MAY 22: no need for beta tag anymore, it's in latest"**
  - 이 논의가 명시적으로 arm64 지원을 말한 빌더는 `paketobuildpacks/builder-jammy-buildpackless-tiny`
  - 2024-04-19 시점 arm64 확보 런타임 빌드팩: Bellsoft Liberica, Oracle, Azul Zulu, Amazon Corretto, SAP Machine
  - 2024-06-11 기준 arm64가 **없는** Java 빌드팩은 둘뿐: `aternity`, `google-stackdriver` — **"those agents do not have arm64 versions"**
  - 2024-07-27 `java-azure` composite 빌드팩도 arm64 추가
- **⚠️ 논증 주의:** 이 논의는 **jammy** 계열에 대한 것이다. Spring Boot 4.1.0의 기본 빌더는 **noble** 계열이다. jammy의 arm64 지원은 noble의 arm64 지원을 증명하지 않는다 — 그래서 E-2에서 레지스트리를 직접 조회했다. 책에서도 이 추론 단계를 생략하지 말 것(오히려 좋은 교육 소재다: "비슷하니까 되겠지"가 왜 위험한가).
- **관련 섹션:** Spring 컨테이너화 챕터 / 리서치 방법론 칼럼

### E-4. `bootBuildImage` 크로스 플랫폼 빌드가 깨졌던 실화 (1차 소스)

- **출처:** New arm64 macbooks fail to bootBuildImage due to incorrect platform image · Issue #46665 · spring-projects/spring-boot — https://github.com/spring-projects/spring-boot/issues/46665 (보고자 ofirm93, 오픈 2025-08-04, 상태 Closed, 담당 philwebb, 검색: 2026-07-25) · **신뢰성: 최상**
- 읽은 사실:
  - 증상: arm64 MacBook에서 `imagePlatform`으로 **amd64** 이미지를 만들려 하면 `Invalid buildpack reference '<buildpack>'` 오류
  - 보고된 원인: 플러그인이 빌드팩을 받을 때 `docker pull --platform <imagePlatform>`은 올바르게 쓰지만, 이어지는 `docker save <buildpack>`에는 platform 플래그를 주지 않아 Docker가 호스트(arm64)를 가정 → 받아온 amd64 이미지와 불일치
  - 보고 환경: Spring Boot 3.5.4 / Spring Boot Gradle Plugin 3.5.4 / Docker 4.42.1 / MacBook Pro M4 Pro (arm64)
  - **수정 버전(milestone): 미확인.** Closed인 것만 확인했고 어느 릴리스에서 고쳐졌는지는 못 읽었다. 책에 "X.Y.Z에서 고쳐졌다"라고 쓰지 말 것.
- **관련 섹션:** arm64 함정 챕터 (실화 사례로 최적 — "네이티브 arm64는 잘 되는데, 크로스 빌드가 깨진다"는 구도)

### E-5. layered jar → `-Djarmode=tools` (⚠️ 기억과 다를 수 있는 지점)

2026-07-25에 렌더된 Spring Boot 문서(표기 **4.1.0**)에서 확인한 것:

- 문서에 나오는 명령은 **`-Djarmode=tools`** 이다. **`-Djarmode=layertools`는 이 페이지들에 등장하지 않는다.**
  ```
  Usage:
    java -Djarmode=tools -jar my-app.jar

  Available commands:
    extract      Extract the contents from the jar
    list-layers  List layers from the jar that can be extracted
    help         Help about any command
  ```
- 추출 명령: `java -Djarmode=tools -jar application.jar extract --layers --destination extracted`
- 옵션 도움말: `java -Djarmode=tools -jar my-app.jar help extract`
- **공식 멀티스테이지 Dockerfile 예제 (문서에서 그대로):**
  ```dockerfile
  # Perform the extraction in a separate builder container
  FROM bellsoft/liberica-openjre-debian:25-cds AS builder
  WORKDIR /builder
  ARG JAR_FILE=target/*.jar
  COPY ${JAR_FILE} application.jar
  RUN java -Djarmode=tools -jar application.jar extract --layers --destination extracted

  FROM bellsoft/liberica-openjre-debian:25-cds
  WORKDIR /application
  COPY --from=builder /builder/extracted/dependencies/ ./
  COPY --from=builder /builder/extracted/spring-boot-loader/ ./
  COPY --from=builder /builder/extracted/snapshot-dependencies/ ./
  COPY --from=builder /builder/extracted/application/ ./
  ENTRYPOINT ["java", "-jar", "application.jar"]
  ```
  - 레이어 디렉터리 순서: `dependencies/` → `spring-boot-loader/` → `snapshot-dependencies/` → `application/` (자주 안 바뀌는 것부터)
  - 문서 주석: "Every copy step creates a new docker layer / This allows docker to only pull the changes it really needs", "This layout is efficient to start up and AOT cache (and CDS) friendly"
  - 빌드 명령: `docker build --build-arg JAR_FILE=path/to/myapp.jar .`
- 압축 해제(unpack)를 권하는 이유와 성능 단서:
  > "After startup, you should not expect any differences in execution time between running an executable jar and running an extracted jar."
  → **차이는 "시작"에 있지 "실행"에 있지 않다**는 문장. 챕터에서 오해를 끊는 데 유용하다.
- **미확인:** `layertools`가 언제 deprecate/제거됐는지(어느 버전) — 확인 못 했다. 책에서 "3.x부터 tools로 바뀌었다" 식 단정 금지.
- **출처:** Efficient Deployments :: Spring Boot — https://docs.spring.io/spring-boot/reference/packaging/efficient.html (표기 4.1.0, 발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- **출처:** Dockerfiles :: Spring Boot — https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html (표기 4.1.0, 발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- **관련 섹션:** 이미지 만들기 챕터 / 캐시 레이어 챕터

### E-6. Spring Boot의 Docker Compose 지원과 `@ServiceConnection`

- **출처:** Development-time Services :: Spring Boot — https://docs.spring.io/spring-boot/reference/features/dev-services.html (표기 4.1.0, 발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- 모듈 좌표:
  - Maven: `org.springframework.boot:spring-boot-docker-compose` (`<optional>true</optional>`)
  - Gradle: `developmentOnly("org.springframework.boot:spring-boot-docker-compose")`
- 동작: `compose.yml` 등 일반적인 compose 파일명을 찾아 **`docker compose up`** 을 호출하고, 지원되는 컨테이너마다 service connection 빈을 만들고, 종료 시 **`docker compose stop`** 을 호출한다.
- 라이프사이클 프로퍼티 `spring.docker.compose.lifecycle-management`: `none` / `start-only` / `start-and-stop`
- 그 외 프로퍼티(문서에 나온 그대로): `spring.docker.compose.start.command=up`, `spring.docker.compose.stop.command=down`, `spring.docker.compose.start.arguments[0]=--build`, `spring.docker.compose.stop.arguments[0]=--volumes`, `spring.docker.compose.stop.timeout=1m`, `spring.docker.compose.file=../my-compose.yml`, `spring.docker.compose.profiles.active=myprofile`
- `@ServiceConnection` 지원 서비스(문서 나열): ActiveMQ, Artemis, Cassandra, Elasticsearch, MongoDB, Neo4j, MySQL, PostgreSQL, MariaDB, MSSQL, Oracle, ClickHouse, RabbitMQ, Redis, Hazelcast, Pulsar, LDAP, OTLP(logging/metrics/tracing), Zipkin, JDBC/R2DBC
- 커스텀 이미지에 서비스 연결을 붙이는 라벨: `org.springframework.boot.service-connection: redis` / 무시 라벨: `org.springframework.boot.ignore: true`
- Testcontainers 쪽: `testAndDevelopmentOnly("org.springframework.boot:spring-boot-testcontainers")`, `@ImportTestcontainers`, `@RestartScope`, `DynamicPropertyRegistrar`, 실행은 `spring-boot:test-run`(Maven) / `bootTestRun`(Gradle), 시작 순서는 `spring.testcontainers.beans.startup=sequential|parallel`
- **관련 섹션:** 개발 루프 챕터 (컨테이너를 "배포용"이 아니라 "개발용"으로 쓰는 법)

### E-7. Testcontainers — Docker Desktop이 아닌 런타임에서의 설정

맥에서 Docker Desktop을 안 쓰기로 하면 가장 먼저 깨지는 게 Testcontainers다. 공식 문서가 런타임별 환경변수를 직접 준다.

- **출처:** Supported Docker environments — Testcontainers for Java — https://java.testcontainers.org/supported_docker_environment/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- Docker Desktop: "automatically detected and used by Testcontainers without any additional configuration"
- **Colima:**
  ```
  export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock
  export TESTCONTAINERS_HOST_OVERRIDE=$(colima ls -j | jq -r '.address')
  export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"
  ```
- **Podman (macOS):**
  ```
  export DOCKER_HOST=unix://$(podman machine inspect --format '{{.ConnectionInfo.PodmanSocket.Path}}')
  export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock
  ```
- **Rancher Desktop:** M1 머신용으로 두 구성이 문서화되어 있다.
  - QEMU: `export TESTCONTAINERS_HOST_OVERRIDE=$(rdctl shell ip a show rd0 | awk '/inet / {sub("/.*",""); print $2}')`
  - VZ(비관리자): `DOCKER_HOST` + `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` + host override 조합
- **OrbStack은 이 페이지에 언급 없음(미확인).**
- **관련 섹션:** 대안 런타임 챕터 / 테스트 챕터

### E-8. JVM 컨테이너 인식 튜닝

**공식 문서에서 읽은 것 (JDK 21 `java` man page):**
- `-XX:-UseContainerSupport`
  > "**Linux only:** The VM now provides automatic container detection support, which allows the VM to determine the amount of memory and number of processors that are available to a Java process running in docker containers. It uses this information to allocate system resources. The default for this flag is `true`, and container support is enabled by default. It can be disabled with `-XX:-UseContainerSupport`."
  > "Use `-Xlog:os+container=trace` for maximum logging of container information."
- `-XX:ActiveProcessorCount=x`
  > "Overrides the number of CPUs that the VM will use to calculate the size of thread pools it will use for various operations such as Garbage Collection and ForkJoinPool. ... This flag is honored even if `UseContainerSupport` is not enabled."
- **출처:** java — JDK 21 Tools Reference (Oracle) — https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- ⚠️ 이 페이지 발췌에서 **`-XX:MaxRAMPercentage` / `MinRAMPercentage` / `InitialRAMPercentage` 항목은 읽어내지 못했다**(페이지가 커서 발췌 누락 가능). 공식 문서 인용은 `UseContainerSupport`·`ActiveProcessorCount`까지만 하고, 아래 실측값을 별도 근거로 쓸 것.

**로컬 실측 (2026-07-25, 이 책을 쓴 맥의 JDK 21.0.10):**
```
$ java -XX:+PrintFlagsFinal -version | grep -Ei "RAMPercentage|ActiveProcessorCount|MaxRAM "
   int  ActiveProcessorCount   = -1            {product} {default}
double  InitialRAMPercentage   = 1.562500      {product} {default}
uint64_t MaxRAM               = 137438953472   {pd product} {default}
double  MaxRAMPercentage       = 25.000000     {product} {default}
double  MinRAMPercentage       = 50.000000     {product} {default}
```
→ **JDK 21.0.10에서 `MaxRAMPercentage` 기본값은 25.0으로 관측됐다.** 즉 "컨테이너에 2GB를 줘도 힙은 기본 500MB 근처"라는 흔한 함정의 실측 근거. 단, 이건 **이 JDK 빌드에서의 관측**이다 — "모든 JVM의 기본값"으로 일반화하지 말고 독자에게 `-XX:+PrintFlagsFinal`로 직접 확인하는 법을 알려주는 편이 낫다.

**Paketo Java 빌드팩의 Memory Calculator (Spring 사용자에게 직접적):**
- 공식: `Heap = Total Container Memory - Non-Heap - Headroom`
- 문서가 언급한 플래그/기본값: `-XX:MaxDirectMemorySize` 10MB, `-XX:ReservedCodeCacheSize` 240MB, `-XX:MaxMetaspaceSize` 자동 계산, `-Xss` 1M × 250(스레드 수 × 스택 크기), `-Xmx`는 나머지. 모두 런타임에 `JAVA_TOOL_OPTIONS`로 붙는다.
- Spring Boot 전용 컴포넌트가 "can apply domain-specific knowledge to optimize the performance of Spring Boot applications"(예: 리액티브 웹 앱의 스레드 수를 50으로 축소)
- **미확인:** `BPL_JVM_THREAD_COUNT` / `BPL_JVM_HEAD_ROOM` 환경변수는 이 페이지 발췌에서 확인 못 했다. CDS/AOT 언급도 이 페이지에는 없었다.
- **출처:** Java Reference — Paketo Buildpacks — https://paketo.io/docs/reference/java-reference/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- **관련 섹션:** JVM과 컨테이너 챕터 (자바 개발자에게 가장 실용적인 절)

### E-9. 세 번째 경로 — Jib

- **출처:** GoogleContainerTools/jib — https://github.com/GoogleContainerTools/jib (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상** (프로젝트 공식 리포)
- 정의(원문): **"Jib builds optimized Docker and OCI images for your Java applications without a Docker daemon - and without deep mastery of Docker best-practices."** Maven·Gradle 플러그인, Java 라이브러리, CLI로 제공.
- README가 내세우는 세 가지:
  > **Fast** — "Jib separates your application into multiple layers, splitting dependencies from classes. Now you don't have to wait for Docker to rebuild your entire Java application."
  > **Reproducible** — "Rebuilding your container image with the same contents always generates the same image. Never trigger an unnecessary update again."
  > **Daemonless** — "Build your Docker image from within Maven or Gradle and push to any registry of your choice. No more writing Dockerfiles and calling docker build/push."
- **daemonless가 맥 독자에게 갖는 의미:** Docker Desktop 라이선스(A-2)·VM 성능(A-1)·런타임 충돌(env_probe 4절) 문제를 **전부 우회**한다. 3경로 비교표에서 Jib의 차별점은 여기다.
- **미확인:** README 발췌에서 **정확한 플러그인 버전 번호와 `jib:build` / `jib:dockerBuild` / `jibDockerBuild` 명령 문법, arm64/멀티플랫폼 지원 서술을 읽어내지 못했다.** README는 하위 디렉터리 문서(jib-maven-plugin / jib-gradle-plugin)로 안내한다. 기본 베이스는 "an OpenJDK base image"라고만 언급. → **책에 Jib 명령이나 버전을 쓰려면 해당 플러그인 문서를 별도로 열어야 한다.**
- **관련 섹션:** Spring 컨테이너화 챕터 (3경로 비교표)

---

## B. 아키텍처 — arm64 vs amd64

### B-1. 멀티 플랫폼 빌드의 세 가지 전략 (공식)

- **출처:** Multi-platform builds — Docker Docs — https://docs.docker.com/build/building/multi-platform/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- 문서가 제시하는 세 전략(원문 표현):
  1. "Using emulation, via QEMU"
  2. "Use a builder with multiple native nodes"
  3. "Use cross-compilation with multi-stage builds"
- 문서에 나오는 명령 형태:
  ```
  docker buildx build --platform linux/amd64,linux/arm64 .
  docker build --platform linux/amd64,linux/arm64 -t multi-platform .
  ```
- 기본 드라이버의 제약: 오래된 Engine이거나 클래식 스토리지 드라이버를 쓰는 경우 두 가지 선택지가 있다 — **containerd image store를 켜거나**, **"Create a custom builder using the `docker-container` driver."**
- 주의 문장: **"Builds with the `docker-container` driver aren't automatically loaded to your Docker Engine image store."** → `--load` / `--push`를 안 붙이면 만들었는데 `docker images`에 안 보이는 그 증상.
- **이 페이지에는 Rosetta·Apple Silicon 언급이 없다(미확인).** Rosetta 얘기는 A 섹션의 Docker Desktop 설정 문서에서 가져와야 한다.
- **관련 섹션:** 멀티아키 빌드 챕터

### B-2. containerd image store — 멀티아키를 "로컬에 담을 수 있는가"의 열쇠

- **출처:** containerd image store — Docker Docs — https://docs.docker.com/desktop/features/containerd/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- 정의: "The image store is the component responsible for pushing, pulling, and storing images on the filesystem."
- **기본값:** "The containerd image store is enabled by default in Docker Desktop version 4.34 and later."
- 클래식 스토어의 한계(원문): **"It doesn't support image indices or manifest lists, so you can't load multi-platform images locally or build images with attestations."**
- containerd image store가 여는 것: 멀티 플랫폼 이미지 로컬 빌드·로드, image attestation, stargz 같은 대체 snapshotter(lazy pulling), nydus·dragonfly 같은 P2P 배포, Wasm 컨테이너
- **책에서의 쓸모:** "매니페스트 리스트를 로컬에 못 담는다"가 왜 `docker buildx build --platform a,b` 뒤에 `--push`를 요구했는지를 설명한다. env_probe의 데몬은 Docker Desktop 29.6.2 / Desktop 4.83.0이므로 이 기본값 조건(4.34+)을 만족한다 — 다만 **이 맥에서 실제로 켜져 있는지는 별도 확인 필요(미확인)**.
- **관련 섹션:** 멀티아키 빌드 챕터

### B-3. `exec format error`

- **미확인.** "`exec format error`"를 정면으로 설명하는 Docker 공식 문서 페이지는 이번 세션에서 확보하지 못했다.
- 대신 **원인을 1차 소스 조합으로 재구성할 수 있다**: (1) `imagePlatform` 기본값 = 호스트 플랫폼(E-1 인용), (2) OCI 이미지 인덱스가 아키텍처별 매니페스트를 가진다(G-3), (3) 클래식 스토어는 매니페스트 리스트를 못 담는다(B-2). 책에서는 증상 문자열을 단정 인용하지 말고 "아키텍처가 안 맞는 바이너리를 커널이 실행하려 할 때 나는 오류"로 서술하고, 재현은 저술 시점에 직접 실행해 캡처하는 편이 안전하다.

---

## A. 맥에서의 Docker 실행 구조

### A-1. VM 매니저(VMM)와 Rosetta — Docker Desktop 설정 (공식)

- **출처:** Change your Docker Desktop settings — https://docs.docker.com/desktop/settings-and-maintenance/settings/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- 설정 이름 그대로:
  - **"Choose Virtual Machine Manager (VMM)"** — 옵션: Docker VMM / Apple Virtualization framework / QEMU
    > "Select **Docker VMM** for the latest and most performant Hypervisor/Virtual Machine Manager. This option is available only on Apple Silicon Macs and is in Beta."
    - **기본 선택이 무엇인지는 이 페이지에서 확인 못 함(미확인).**
  - **"Use Rosetta for x86_64/amd64 emulation on Apple Silicon"** — **기본값 Disabled**
    > "This option is only available if you have selected **Apple Virtualization framework** as the Virtual Machine Manager."
    → **즉 Docker VMM(신형·Beta)을 고르면 Rosetta를 못 켠다.** amd64 성능을 원하면 VMM 선택 자체가 트레이드오프다. 이게 이 섹션의 핵심 판단 기준.
  - **"Choose file sharing implementation for your containers"** — VirtioFS(기본) / gRPC FUSE
    > "VirtioFS has reduced the time taken to complete filesystem operations by up to 98%."
    > "It is the only file sharing implementation supported by Docker VMM."
  - 리소스: Memory limit **"Defaults to 50% of your host's memory."**, Swap **"1 GB default"**, CPU limit·디스크 이미지 위치는 조정 가능
  - "Include VM in Time Machine backups" — 기본 Disabled

- **출처(보강):** Docker VMM / Virtual Machine Manager — https://docs.docker.com/desktop/features/vmm/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
  - **"Docker VMM does not currently support Rosetta, so emulation of amd64 architectures is slow."** ← 위 설정 문서와 정확히 맞물리는 결정적 문장
  - "Docker VMM requires a minimum of 4GB of memory to be allocated to the Docker Linux VM."
  - "Certain databases, like MongoDB and Cassandra, may fail when using virtiofs with Docker VMM."
  - Apple Virtualization framework는 "A stable and well-established option for managing virtual machines on Mac", QEMU·HyperKit은 Legacy/deprecated로 표기
- **관련 섹션:** 맥에서 Docker가 도는 방식 챕터 (VM·파일공유·Rosetta의 3자 트레이드오프 표로 정리하면 좋다)

### A-2. Docker Desktop 라이선스 임계값

- **출처:** Docker Desktop license agreement — https://docs.docker.com/subscription/desktop-license/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- 읽은 문구: 무료 사용 가능한 범위는 **"Small businesses (fewer than 250 employees AND less than $10 million in annual revenue)"**. 그 외 "Professional use in larger organizations", "Government entities"는 유료 구독 필요.
- **표기 권장:** "직원 250명 미만 **그리고** 연매출 1,000만 달러 미만이면 무료 (2026-07 검색 기준)". **AND 조건**임에 주의 — 한쪽만 넘어도 유료다. 한국 중견기업 독자에게 실질적으로 중요한 지점.
- **관련 섹션:** 왜 대안 런타임을 고민하는가 (C 섹션의 동기)

### A-3. Docker Desktop 공개 릴리스 라인 (env_probe 대조용)

- **출처:** Docker Desktop release notes — https://docs.docker.com/desktop/release-notes/ (검색: 2026-07-25) · **신뢰성: 최상**
- 페이지 최상단(=최신) 항목: **4.83.0, 2026-07-20**
- 4.83.0의 Updates 목록(문서 표기 그대로): Docker Desktop CLI `v0.4.2` / Docker Model Runner v1.2.6 / Docker Offload `v0.6.9` / Docker Agent v1.103.0 / **Docker Compose v5.3.1** / **Docker Desktop Build `v0.36.0`** / **Docker Engine v29.6.2**
- 인접 릴리스: 4.82.0(2026-07-13), 4.81.0(2026-07-06), 4.80.0(2026-06-29, Docker Engine v29.6.1), 4.79.0(2026-06-22)
- → **주 단위(대략 매주 화요일) 릴리스 리듬**으로 보이지만, 문서가 "주 1회"라고 명시하진 않았다. 날짜 나열만 근거로 제시하고 주기를 단정하지 말 것.
- **관련 섹션:** 버전 이야기 / 상충 기록

---

## C. 대안 런타임

### C-1. 각 도구의 공개 최신 릴리스 (GitHub Releases 직접 확인)

| 도구 | 최신 릴리스 | 날짜 | 출처 |
|---|---|---|---|
| Docker Desktop | 4.83.0 | 2026-07-20 | https://docs.docker.com/desktop/release-notes/ |
| Rancher Desktop | v1.23.1 | 2026-06-29 | https://github.com/rancher-sandbox/rancher-desktop/releases |
| Podman Desktop | v1.28.3 | 2026-07-20 | https://github.com/podman-desktop/podman-desktop/releases |
| Colima | v0.10.3 | 2025-06-04 | https://github.com/abiosoft/colima/releases |
| OrbStack | **미확인** | — | 이번 세션에서 확인 못 함 |

- Podman Desktop v1.28.3 릴리스 노트 문구: "feat: updated podman to 5.8.5"
- Colima 인접 릴리스: v0.10.2(2025-06-03), v0.10.1(2025-02-22). v0.10.1에서 "Docker Model Runner를 AI 모델 러너 백엔드로 지원, 기본값으로" 언급.
- Rancher Desktop 1.23.1 설명: "an open source desktop application to bring Kubernetes and container management to macOS, Windows, and Linux"
- **⚠️ 신선도 경고:** Colima의 최신 릴리스가 2025-06-04라는 것은 **1년 이상 새 릴리스가 없다**는 뜻이다(2026-07 기준). 책에 "활발히 개발 중"이라고 쓰지 말 것 — 관측된 사실만 쓰고 판단은 독자에게 넘겨라.
- **신뢰성: 최상** (전부 GitHub Releases / 공식 릴리스 노트)

### C-2. `docker context`와 `DOCKER_HOST`의 우선순위 (공식)

- **출처:** Contexts — Docker Docs — https://docs.docker.com/engine/manage-resources/contexts/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- context의 구성: "Name and description, Endpoint configuration, TLS info"
- 우선순위 문장(원문): **"all `docker` commands run against this context, unless overridden with environment variables such as `DOCKER_HOST` and `DOCKER_CONTEXT`, or on the command-line with the `--context` and `--host` flags."**
  → 명령행 플래그(`--context`/`--host`) > 환경변수(`DOCKER_CONTEXT`/`DOCKER_HOST`) > `docker context use`로 정한 활성 컨텍스트
- 명령: `docker context ls` / `use` / `create` / `inspect` / `export` / `import` / `update`
- **env_probe와의 연결:** 이 맥은 `DOCKER_HOST`가 unset이고 활성 context가 `desktop-linux`였다. 위 우선순위 규칙에 정확히 부합한다 — 즉 "환경변수가 없으니 context가 결정했다". 이 문서 문장이 그 관측의 설명이 된다. **다만 "PATH가 잡은 CLI는 Rancher, context가 가리키는 데몬은 Docker Desktop"이라는 교차 상황 자체는 공식 문서가 다루지 않는다(미확인).** 그래서 이 사례가 책의 고유 가치다.
- **관련 섹션:** 런타임 두 개 깔았을 때 챕터 (env_probe 4절이 주인공)

### C-3. Rancher Desktop의 containerd vs dockerd, `nerdctl`

- **1차 소스 미확보(미확인).** Rancher Desktop 공식 문서에서 컨테이너 엔진 선택(containerd/moby)과 `nerdctl` 사용법 페이지를 이번 세션에서 열지 못했다.
- 확보된 간접 근거: env_probe에서 `~/.rd/bin`에 `nerdctl`, `rdctl`, `helm`, `kuberlr`가 함께 설치되는 것을 관측. Testcontainers 문서가 Rancher Desktop의 QEMU/VZ 두 구성을 구분해 다루는 것(E-7)도 참고.

---

## D. 이미지 만들기·업데이트 (사용자 요구 3번)

### D-1. 레이어 캐시와 캐시 무효화 (공식)

- **출처:** Optimize cache usage in builds — Docker Docs — https://docs.docker.com/build/cache/optimize/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- 캐시 재사용 규칙(원문): **"When building with Docker, a layer is reused from the build cache if the instruction and the files it depends on hasn't changed since it was previously built."** 그리고 "a change causes a rebuild for steps that follow."
- `.dockerignore`: `.gitignore`와 유사하게 동작. **"Ignore-rules specified in the `.dockerignore` file apply to the entire build context, including subdirectories."** 예시:
  ```
  node_modules
  tmp*
  ```
- 레이어 순서 전략: 비싼 작업은 앞에, 자주 바뀌는 단계는 뒤에. 문서 예시는 `package.json`/`yarn.lock`만 먼저 COPY → 의존성 설치 → 소스 COPY.
  → **Spring 독자에겐 그대로 번역된다: `build.gradle`/`gradle/wrapper`만 먼저 COPY → 의존성 해석 → `src` COPY.** (단, 이 Spring 변형 자체는 문서에 없으니 "문서의 원리를 Gradle에 적용하면"이라고 밝힐 것)
- **BuildKit 캐시 마운트** 문법과 예시(문서 그대로):
  ```dockerfile
  RUN --mount=type=cache,target=/root/.npm npm install
  RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
  RUN --mount=type=cache,target=/var/cache/apt,sharing=locked apt update && apt-get install -y gcc
  ```
  → Gradle이면 `target=/root/.gradle` 같은 응용이 되지만, **그 구체 예시는 문서에 없다.** 직접 검증 후 쓸 것.
- **외부 캐시 백엔드:**
  ```
  docker buildx build --cache-from type=registry,ref=user/app:buildcache .
  ```
  CI 설정 예: `cache-from: type=registry,ref=user/app:buildcache` / `cache-to: type=registry,ref=user/app:buildcache,mode=max`
- **미확인:** `--mount=type=secret` 예시는 이 페이지에서 확인 못 했다.
- **관련 섹션:** 이미지 업데이트 챕터 (사용자 요구 3번의 핵심 — "다시 빌드할 때 무엇이 다시 도는가")

### D-2. 취약점 스캔·SBOM — Docker Scout

- **출처:** Docker Scout — https://docs.docker.com/scout/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- 정의: "Docker Scout is a solution for proactively enhancing your software supply chain security." "a standalone service and platform that you can interact with using Docker Hub, the Docker CLI, and the Docker Scout Dashboard."
- SBOM: 이미지를 분석해 "compiles an inventory of components, also known as a Software Bill of Materials (SBOM)" 하고, 이를 "matched against a continuously updated vulnerability database to pinpoint security weaknesses."
- **미확인:** `docker scout cves` / `quickview` / `compare` / `recommendations` 등 **구체 CLI 명령과 Docker Desktop 기본 포함 여부는 이 개요 페이지에서 확인하지 못했다.** 책에 명령어를 쓰려면 별도 레퍼런스 페이지 확인 필요.

### D-3. 베이스 이미지 고정·재빌드 — 사용자 요구 3번("업데이트")의 핵심

- **출처:** Building best practices — Docker Docs — https://docs.docker.com/build/building/best-practices/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- 베이스 이미지 선택: "The first step towards achieving a secure image is to choose the right base image."
- **태그의 의미(중요):** "If you specify `FROM alpine:3.21` in your Dockerfile, `3.21` resolves to the latest patch version for `3.21`."
  → **태그는 고정된 이미지를 가리키지 않는다.** 같은 Dockerfile이 어제와 오늘 다른 이미지를 만든다는 사실의 1차 근거.
- **digest 고정(원문):** **"By pinning your images to a digest, you're guaranteed to always use the same image version, even if a publisher replaces the tag with a new image."**
  ```dockerfile
  FROM alpine:3.21@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
  ```
- **재빌드로 베이스 갱신 받기 — "업데이트 워크플로"의 실제 명령:**
  - `--pull`: "The `--pull` flag forces Docker to check for and download a newer version of the base image, even if you have a version cached locally."
    ```
    docker build --pull -t my-image:my-tag .
    ```
  - `--no-cache`: "The `--no-cache` flag disables the build cache, forcing Docker to rebuild all layers from scratch."
    ```
    docker build --no-cache -t my-image:my-tag .
    ```
  - 둘 다: `docker build --pull --no-cache -t my-image:my-tag .`
  → **이 두 플래그의 차이가 "이미지 업데이트" 절의 뼈대다.** digest로 고정했으면 `--pull`은 아무것도 안 바꾼다(같은 digest니까). 태그로 뒀으면 `--pull`이 베이스 패치를 끌어온다. 캐시 무효화(`--no-cache`)는 또 다른 문제다.
- 멀티스테이지: "Multi-stage builds let you reduce the size of your final image, by creating a cleaner separation between the building of your image and the final output." / 공통 stage 재사용 시 "Docker only needs to build the common stage once. This means that your derivative images use memory more efficiently and load more quickly."
- 레이어 정리: "Always combine `RUN apt-get update` with `apt-get install` in the same `RUN` statement." (캐시 때문에 update가 낡은 채로 굳는 고전적 함정), "Whenever possible, sort multi-line arguments alphanumerically to make maintenance easier."
- **미확인:** 이 페이지에는 **`latest` 태그를 직접 논하는 서술이 없다.** `latest` 안티패턴을 주장하려면 kind 문서의 pull policy 규칙(F-3)을 근거로 삼는 편이 정확하다 — "K8s의 기본 pull policy가 태그 문자열에 따라 달라진다"는 관측 가능한 사실이기 때문이다.
- **미확인:** distroless / Alpine / Debian slim **비교** 기준은 여전히 1차 소스 없음.
- Spring 공식 Dockerfile 예제가 고른 베이스는 `bellsoft/liberica-openjre-debian:25-cds`(E-5) — "Spring 팀이 문서에서 고른 베이스"라는 사실 자체는 인용 가능.
- **관련 섹션:** 이미지 업데이트 챕터 (요구 3번 정면 대응)

---

## F. Kubernetes (사용자 요구 4번)

### F-1. 현재 지원 버전대와 릴리스 주기

- **출처:** Kubernetes Releases — https://kubernetes.io/releases/ (검색: 2026-07-25) · **신뢰성: 최상**

| Minor | Latest Patch | Release Date | End of Life |
|---|---|---|---|
| 1.36 | 1.36.2 | 2026-06-09 | 2027-06-28 |
| 1.35 | 1.35.6 | 2026-06-09 | 2027-02-28 |
| 1.34 | 1.34.9 | 2026-06-09 | 2026-10-27 |

  > "The Kubernetes project maintains release branches for the most recent three minor releases (1.36, 1.35, 1.34)."
  > "Kubernetes 1.19 and newer receive approximately 1 year of patch support. Kubernetes 1.18 and older received approximately 9 months of patch support."

- **출처:** Kubernetes Release Cycle — https://kubernetes.io/releases/release/ (검색: 2026-07-25) · **신뢰성: 최상**
  > **"Kubernetes releases currently happen approximately three times per year."**
  > "Created at the time of the `vX.Y-rc.0` release and maintained after the release for approximately 12 months with `vX.Y.Z` patch releases."
  - 릴리스 사이클 구조: Normal Dev(1~11주) → Code Freeze(12~14주) → Post-Release(14주~). **"약 14~16주 사이클"은 이 타임라인에서 유도한 값이지 문서의 문장이 아니다** — 인용할 때 유도임을 밝힐 것.
- **⚠️ 도구 오류 기록:** 최초 `kubernetes.io/releases/` 조회 요약은 "quarterly cadence (4/year)"라고 추정 서술했다. 릴리스 사이클 페이지의 명시 문장("approximately three times per year")과 어긋난다. **후자를 채택.** (상충 기록 참조)
- **env_probe 대조:** 이 맥의 `kubectl` client는 **v1.32.1** — 위 지원 범위(1.34~1.36)보다 낮다. 지원 종료된 마이너 라인의 클라이언트다. 버전 skew를 설명할 실물 소재.

### F-2. dockershim 제거 이후 — CRI와 컨테이너 런타임

- **출처:** Dockershim Removal FAQ — Kubernetes Blog — https://kubernetes.io/blog/2022/02/17/dockershim-faq/ (발행일: 2022-02-17, 검색: 2026-07-25) · **신뢰성: 최상** · ⚠️ 4년 전 글이지만 "제거 사실" 자체는 확정 사실이라 신선도 리스크가 낮다.
  > "Early versions of Kubernetes only worked with a specific container runtime: Docker Engine. Later, Kubernetes added support for working with other container runtimes. The CRI standard was created to enable interoperability between orchestrators (like Kubernetes) and many different container runtimes. Docker Engine doesn't implement that interface (CRI), so the Kubernetes project created special code to help with the transition, and made that _dockershim_ code part of Kubernetes itself."
  > "The dockershim code was always intended to be a temporary solution (hence the name: shim)."
  > "The dockershim removal occurred in Kubernetes 1.24."
  > **"Yes, the images produced from `docker build` will work with all CRI implementations. All your existing images will still work exactly the same."**
  → **자바 개발자가 가장 많이 오해하는 지점을 한 문장으로 끝낸다: "도커가 쿠버네티스에서 빠졌다"는 말은 이미지가 못 쓰이게 됐다는 뜻이 아니다.**
- **관련 섹션:** OCI/CRI 원리 챕터 / K8s 챕터 도입부

### F-3. 로컬 K8s에 내 이미지 올리기

**kind**
- **출처:** kind — Quick Start — https://kind.sigs.k8s.io/docs/user/quick-start/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- 명령(문서 그대로):
  ```
  kind create cluster
  kind create cluster --name kind-2
  kind create cluster --wait 30s
  kind load docker-image my-app:latest
  kind load docker-image my-app:latest my-db:latest my-cache:latest
  kind load docker-image my-app:latest --name test-cluster
  kind load image-archive /my-image-archive.tar
  ```
- pull policy 함정(원문): "The Kubernetes default pull policy is `IfNotPresent` unless the image tag is `:latest`...in which case the default policy is `Always`." → 해결: `:latest` 태그를 쓰지 말거나 `imagePullPolicy: IfNotPresent`/`Never` 명시.
- 런타임: kind는 "can auto-detect the docker, podman, or nerdctl installed and choose the available one." → **Rancher Desktop만 깐 맥에서도 nerdctl 경유로 동작 여지가 있다.**
- 노드 이미지: `kindest/node`. 어떤 K8s 버전이 있는지는 "check the release notes for your given kind version".
- **kind 최신 릴리스:** `v0.32.0` (https://github.com/kubernetes-sigs/kind/releases, 검색 2026-07-25). 이 릴리스가 담은 노드 이미지: `kindest/node` v1.36.1 / v1.35.5 / v1.34.8 / v1.33.12. 기본 노드 이미지는 breaking changes 절 기준 `kindest/node:v1.36.1@sha256:3489c7674813ba5d8b1a9977baea8a6e553784dab7b84759d1014dbd78f7ebd5`.
  - **⚠️ 릴리스 날짜는 미확인.** 조회 요약이 "2025-06-02"라고 보고했으나, 이 릴리스가 담은 v1.36.1은 K8s 1.36 라인(2026-06-09 릴리스, F-1)이라 시간순이 성립하지 않는다 → 날짜 폐기, 버전만 채택. (상충 기록 9 참조)

**minikube**
- **출처:** Pushing images — minikube — https://minikube.sigs.k8s.io/docs/handbook/pushing/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- 문서화된 방법(총 8가지 중 주요 명령):
  ```
  eval $(minikube docker-env) && docker build -t my_image .
  minikube image load my_image
  minikube image build -t my_image .
  minikube cache add alpine:latest / minikube cache reload / minikube cache list
  eval $(minikube podman-env) && podman build -t my_image .
  minikube addons enable registry
    docker build --tag $(minikube ip):5000/test-img . && docker push $(minikube ip):5000/test-img
  ```
- 공통 함정(원문): **"Remember to turn off the `imagePullPolicy:Always` (use `imagePullPolicy:IfNotPresent` or `imagePullPolicy:Never`)"**
- **env_probe 대조:** 이 맥의 minikube는 v1.35.0.

### F-4. Kubernetes를 언제 쓰고 언제 쓰지 않는가 (공식 서술)

- **출처:** What is Kubernetes? (Overview) — https://kubernetes.io/docs/concepts/overview/ (발행일 미확인, 검색: 2026-07-25) · **신뢰성: 최상**
- 정의: "Kubernetes is a portable, extensible, open source platform for managing containerized workloads and services that facilitate both declarative configuration and automation."
- **"What Kubernetes is not" 원문 핵심 (인용 가능):**
  > "Kubernetes is not a traditional, all-inclusive PaaS (Platform as a Service) system."
  > "Does not deploy source code and does not build your application. Continuous Integration, Delivery, and Deployment (CI/CD) workflows are determined by organization cultures and preferences as well as technical requirements."
  > "Does not provide application-level services, such as middleware (for example, message buses), data-processing frameworks (for example, Spark), databases (for example, MySQL), caches, nor cluster storage systems (for example, Ceph) as built-in services."
  > "Does not dictate logging, monitoring, or alerting solutions."
  > "Does not provide nor mandate a configuration language/system (for example, Jsonnet)."
  > "Does not provide nor adopt any comprehensive machine configuration, maintenance, management, or self-healing systems."
  > "Additionally, Kubernetes is not a mere orchestration system. In fact, it eliminates the need for orchestration. ... Kubernetes comprises a set of independent, composable control processes that continuously drive the current state towards the provided desired state."
  → **"K8s를 도입하면 배포가 해결된다"는 기대를 공식 문서가 직접 반박한다.** 빌드도 CI/CD도 DB도 로깅도 안 준다. 이 목록을 그대로 "K8s가 당신에게 안 해주는 것" 절로 쓰면 챕터 하나가 선다.
- "Why you need Kubernetes and what it can do" 항목(문서 나열): Service discovery and load balancing / Storage orchestration / Automated rollouts and rollbacks / Automatic bin packing / Self-healing / Secret and configuration management / Batch execution / Horizontal scaling / IPv4/IPv6 dual-stack / Designed for extensibility
- **관련 섹션:** "쿠버네티스는 언제 쓰는 기술인가" 챕터 (사용자 요구 4번의 전반부 — 이 페이지 하나로 뼈대가 나온다)

---

## G. 원리

### G-1. 리눅스 네임스페이스 (man7, 1차 소스)

- **출처:** namespaces(7) — Linux manual page — https://man7.org/linux/man-pages/man7/namespaces.7.html (Linux man-pages **6.18**, 페이지 날짜 **2026-02-08**, 검색: 2026-07-25) · **신뢰성: 최상**
- 정의(원문): **"A namespace wraps a global system resource in an abstraction that makes it appear to the processes within the namespace that they have their own isolated instance of the global resource."**
- 네임스페이스 종류 표(문서 그대로):

| Namespace | Flag | Isolates |
|---|---|---|
| Cgroup | CLONE_NEWCGROUP | Cgroup root directory |
| IPC | CLONE_NEWIPC | System V IPC, POSIX message queues |
| Network | CLONE_NEWNET | Network devices, stacks, ports, etc. |
| Mount | CLONE_NEWNS | Mount points |
| PID | CLONE_NEWPID | Process IDs |
| Time | CLONE_NEWTIME | Boot and monotonic clocks |
| User | CLONE_NEWUSER | User and group IDs |
| UTS | CLONE_NEWUTS | Hostname and NIS domain name |

- **책에서의 쓸모:** "컨테이너는 리눅스 커널 기능이다 → 맥에는 리눅스 커널이 없다 → 그래서 VM이 낀다"의 첫 단추. 8종 표를 그대로 실으면 "컨테이너 = 격리된 프로세스"라는 주장에 실체가 생긴다.

### G-2. cgroups (man7, 1차 소스)

- **출처:** cgroups(7) — Linux manual page — https://man7.org/linux/man-pages/man7/cgroups.7.html (Linux man-pages 6.18, 페이지 날짜 2026-02-08, 검색: 2026-07-25) · **신뢰성: 최상**
- 정의(원문): **"Control groups, usually referred to as cgroups, are a Linux kernel feature which allow processes to be organized into hierarchical groups whose usage of various types of resources can then be limited and monitored."**
- cgroups v2 컨트롤러(문서 나열): cpu, cpuset, freezer, hugetlb, io, memory, perf_event, pids, rdma
- v1/v2 관계(원문): "Although cgroups v2 is intended as a replacement for cgroups v1, the older system continues to exist (and for compatibility reasons is unlikely to be removed)." / "Currently, cgroups v2 implements only a subset of the controllers available in cgroups v1."
- **E-8과 연결:** JVM의 `UseContainerSupport`가 "읽는 것"이 바로 이 cgroup의 memory·cpu 제한이다. 원리 → 실무가 한 줄로 이어지는 지점.

### G-3. OCI 이미지 스펙 — 매니페스트·레이어·digest

- **출처:** OCI Image Format Specification — Image Manifest — https://github.com/opencontainers/image-spec/blob/main/manifest.md (발행일 미확인(main 브랜치), 검색: 2026-07-25) · **신뢰성: 최상**
- 매니페스트 미디어 타입: `application/vnd.oci.image.manifest.v1+json`. `schemaVersion` "MUST be `2` to ensure backward compatibility with older versions of Docker."
- config 미디어 타입: `application/vnd.oci.image.config.v1+json`. "Implementations MUST NOT attempt to parse the referenced content if this media type is unknown."
- layers: descriptor 배열, 인덱스 0이 base layer, 이후 stack order. 지원해야 하는 미디어 타입:
  `application/vnd.oci.image.layer.v1.tar`, `...tar+gzip`, `application/vnd.oci.image.layer.nondistributable.v1.tar`, `...tar+gzip`. `...tar+zstd`는 "SHOULD also support".
- digest는 SHA256. 빈 descriptor 예시 digest: `sha256:44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`
- **E-2와의 연결:** 멀티아키 빌더 조회에서 본 `application/vnd.oci.image.index.v1+json`이 바로 이 스펙의 **이미지 인덱스**다. "태그 하나 → 인덱스 → 아키텍처별 매니페스트 → 레이어 digest" 사슬을 실제 응답으로 보여줄 수 있다.

### G-4. rootless·이미지 서명(cosign)·SBOM

- **1차 소스 미확보(미확인).** rootless 모드, Sigstore/cosign 서명, SBOM 생성에 대한 공식 문서를 이번 세션에서 열지 못했다. 확보된 것은 Docker Scout의 SBOM 정의 한 줄(D-2)뿐이다.

---

## 보너스: 한국어·회사 엔지니어링 블로그

### 자료: 쿠버네티스를 이용해 테스팅 환경 구현해보기 (우아한형제들 기술블로그)
- **출처:** https://techblog.woowahan.com/2562/ (저자: WoowaTech, 발행일: **2018-03-13**, 검색: 2026-07-25)
- **신뢰성: 중** — 회사 공식 기술블로그지만 **8년 전 글이다. 구버전 정보일 가능성이 매우 높다.** 명령어·API·버전은 절대 인용하지 말 것. 인용한다면 "당시 이런 고민을 했다"는 서사·동기 용도로만.
- 인용 가능 구절:
  > "필자는 로컬에서 도커 이미지를 빌드하여 ECR 에 푸쉬한 후 클러스터에서 사용하였다"
  > "helm을 사용하여 차트를 배포할 때 `--name` 파라미터로 지정한 값으로 치환되어 들어갈 것이다"
- 관련 섹션: K8s 챕터의 "왜 쓰게 되는가" 도입 (테스트 환경 격리라는 국내 실무 동기)

### 수집 한계 (한국어 소스)
- `d2.naver.com` / `toss.tech` / `tech.kakao.com` / LINE 대상 도메인 한정 검색에서 **Apple Silicon·멀티아키·Spring 컨테이너화를 정면으로 다루는 최근 글을 찾지 못했다.** 검색어 변형(멀티 아키텍처 / M1 / arm64 / 이미지 최적화)까지 시도했으나 상위 결과는 Medium·개인 블로그·클라우드 벤더 한국어 문서였다.
- 클라우드 벤더 한국어 문서(GKE·EMR on EKS의 멀티아키 이미지 페이지)는 검색 결과에 노출됐으나 **직접 열지 않았으므로 인용하지 않는다.** 필요하면 Phase 1 보강에서 열 것.
- 이번 리서치는 blocking fact-check 게이트를 고려해 **한국어 비중보다 1차 소스 비중을 우선**했다. 대상 독자 친화성은 저술 단계에서 문체로 확보하는 편이 안전하다.

---

## 상충 기록

1. **[해소] Paketo arm64 — 2차 추론 vs 레지스트리 실물.**
   WebSearch 요약과 커뮤니티 논의(#1387)는 **jammy** 계열 빌더의 arm64 지원을 말한다. 그런데 Spring Boot 4.1.0 문서의 기본 빌더는 **noble** 계열이다. jammy→noble 추론을 하지 않고 `docker buildx imagetools inspect`로 **noble 빌더와 run 이미지가 amd64/arm64 두 매니페스트를 실제로 갖고 있음**을 직접 확인해 해소했다. → 레지스트리 조회 채택.

2. **[해소] Kubernetes 릴리스 주기 — 도구 요약 vs 공식 문장.**
   `kubernetes.io/releases/` 조회 요약이 "quarterly cadence(연 4회)"라고 **추정 서술**했다. `kubernetes.io/releases/release/`의 명시 문장은 **"Kubernetes releases currently happen approximately three times per year."** → **연 3회 채택.** (도구 요약문 안의 비인용 수치는 신뢰하지 않는다는 규칙을 이 사건이 정당화한다.)

3. **[일치 — 상충 아님] probe의 Docker Desktop 계열 값 vs 공개 릴리스 라인.**
   probe: Docker Desktop 4.83.0 / Engine 29.6.2 / Compose v5.3.1. 공개 릴리스 노트: 4.83.0(2026-07-20)이 "Docker Engine v29.6.2", "Docker Compose v5.3.1"을 번들. **세 값이 정확히 일치**한다. 즉 이 맥의 Docker Desktop은 2026-07-25 시점 최신 릴리스다. (Compose가 v5 라인이라는 것도 공개 릴리스 노트로 확인됨 — 기억으로 "v2일 것"이라 고치면 안 된다.)

4. **[미해소] buildx 버전 표기 불일치.**
   probe: `docker buildx version` → `v0.35.0-desktop.2`. 4.83.0 릴리스 노트: **"Docker Desktop Build `v0.36.0`"**. 두 이름이 같은 컴포넌트인지(그렇다면 0.35 vs 0.36 불일치), 다른 컴포넌트인지 **확인하지 못했다.** 또한 probe의 buildx는 Rancher Desktop이 PATH에 심은 `~/.rd/bin/docker-buildx`일 가능성도 배제하지 못한다. → 책에서 buildx 버전 숫자를 단정하지 말 것.

5. **[불일치 — 관측 그대로 기록] Rancher Desktop.**
   probe: 1.17.1 설치됨. 공개 최신: **v1.23.1 (2026-06-29)**. 이 맥의 Rancher Desktop은 여러 마이너 뒤처져 있다. → "1.17.1이 최신"이라고 쓰면 오류. "이 맥엔 1.17.1이 깔려 있었고, 당시 공개 최신은 1.23.1이었다"로 병기.

6. **[불일치 — 관측 그대로 기록] kubectl 클라이언트.**
   probe: client v1.32.1. kubernetes.io 지원 범위: 1.34 / 1.35 / 1.36. → 이 맥의 kubectl은 **지원 종료된 라인**의 클라이언트다. 버전 skew 서술의 실물 소재이지 "정상 상태"가 아니다.

7. **[주의] `layertools` vs `jarmode=tools`.**
   널리 퍼진 2차 자료(블로그·강의)는 `-Djarmode=layertools`를 쓴다. 2026-07-25에 렌더된 Spring Boot 4.1.0 공식 문서 두 페이지에는 **`layertools`가 등장하지 않고 `-Djarmode=tools`만 나온다.** → 공식 문서 채택. 전환 시점(어느 버전부터)은 미확인이므로 "언제부터"는 쓰지 말 것.

9. **[미해소 — 도구 신뢰성] GitHub Releases의 날짜 추출이 어긋났다.**
   `spring-projects/spring-boot/releases` 조회는 v4.1.0을 "2024-06-10"으로, `kubernetes-sigs/kind/releases` 조회는 v0.32.0을 "2025-06-02"로 보고했다. 그런데 kind v0.32.0은 `kindest/node:v1.36.1`을 담고 있고, Kubernetes 1.36은 2026-06-09 릴리스다(F-1, kubernetes.io 1차 확인). **담긴 것이 담은 것보다 나중일 수 없으므로 보고된 날짜는 틀렸다.** GitHub의 상대 시간 표기("3 weeks ago")를 절대 날짜로 환산하는 과정에서 어긋난 것으로 보인다.
   → **조치:** 두 릴리스 페이지에서 **버전(Latest 배지·태그명)만 채택하고 날짜는 전부 폐기**했다. 다른 GitHub Releases 출처(Rancher Desktop·Podman Desktop·Colima)의 날짜도 같은 경로로 얻은 값이므로 **약한 근거**로 취급할 것. 반면 `docs.docker.com/desktop/release-notes/`의 날짜(4.83.0 = 2026-07-20)는 페이지 본문에 인쇄된 값이라 상대적으로 신뢰도가 높다.

10. **[주의] 무버전 문서 URL의 함정.**
   `docs.spring.io/spring-boot/...`는 그날의 current를 서빙한다. 이 문서가 "4.1.0"을 표기했다는 것은 **문서가 4.1.0 기준으로 렌더됐다**는 뜻이지, 4.1.0이 그날의 GA라는 증명이 아니다. GA 버전·릴리스 날짜는 **미확인**(spring.io 프로젝트 페이지에서 날짜를 못 읽었고 GitHub Releases는 열지 않았다).

---

## 미확인 목록

| # | 항목 | 무엇을 했고 왜 못 찾았나 |
|---|---|---|
| 1 | Spring Boot GA **릴리스 날짜** | 버전은 확보(GitHub Releases에서 v4.1.0 = Latest, E-0). 날짜는 도구 보고가 내부 모순을 일으켜 폐기(상충 9) |
| 2 | Spring Boot #46665의 수정 마일스톤 | 이슈 페이지를 열었고 Closed·담당자까지 읽었으나 milestone/수정 커밋을 읽어내지 못함 |
| 3 | `-Djarmode=layertools` 제거·deprecate 시점 | 4.1.0 문서에 없다는 것만 확인. 변경 이력(릴리스 노트) 미열람 |
| 4 | `-XX:MaxRAMPercentage` 공식 문서 기재 | JDK 21 `java` man page를 열었으나 발췌에 해당 항목이 없었음(페이지가 커서 누락 추정). 로컬 `PrintFlagsFinal` 관측값(25.0)으로만 보유 |
| 5 | Paketo `BPL_JVM_THREAD_COUNT` / `BPL_JVM_HEAD_ROOM` | java-reference 페이지 발췌에 없음 |
| 6 | `exec format error`의 공식 문서 서술 | Docker 멀티플랫폼 문서에 해당 문자열 없음. 전용 트러블슈팅 페이지 미발견 |
| 7 | Docker Desktop의 기본 VMM(맥) | 설정 문서·VMM 문서 둘 다 열었으나 "어느 것이 기본"인지 명시 문장을 찾지 못함 |
| 8 | Docker Desktop 내장 Kubernetes 버전 | 릴리스 노트 4.83.0 Updates 목록에 Kubernetes 항목이 없었음 |
| 9 | OrbStack 최신 버전 | 이번 세션에서 조회하지 않음(예산) |
| 10 | Rancher Desktop containerd/moby 선택·`nerdctl` 공식 문서 | 공식 docs 페이지 미열람. env_probe의 `~/.rd/bin` 목록만 보유 |
| 11 | Docker Scout CLI 명령(`cves`/`quickview`/`compare`) 및 Desktop 기본 포함 여부 | 개요 페이지만 열었고 CLI 레퍼런스 미열람 |
| 12 | `latest` 태그 안티패턴의 공식 서술 | Docker best-practices 페이지에 `latest` 직접 언급 없음. digest 고정·`--pull`·`--no-cache`는 확보(D-3). semver 태깅 전략 공식 가이드는 여전히 없음 |
| 13 | distroless / Alpine / Debian slim 베이스 **비교** 1차 소스 | 미열람. best-practices는 "choose the right base image"까지만 말함 |
| 19 | Jib 플러그인 버전·명령 문법(`jib:build` 등)·arm64 지원 | 리포 README를 열었으나 발췌에 버전·명령·플랫폼 서술 없음. jib-maven-plugin / jib-gradle-plugin 하위 문서 미열람 |
| 14 | `--mount=type=secret` 예시 | cache optimize 페이지에 없음 |
| 15 | rootless 모드 / cosign 서명 / SBOM 생성 공식 문서 | 미열람 |
| 16 | kind 릴리스 **날짜** | 버전은 확보(v0.32.0, 기본 노드 이미지 v1.36.1). 날짜는 시간순 모순으로 폐기(상충 9) |
| 20 | GitHub Releases 계열 출처의 발행일 전반 | Rancher Desktop·Podman Desktop·Colima 날짜도 같은 추출 경로 → **약한 근거**. 정밀한 날짜가 필요하면 각 릴리스 개별 페이지를 열어 재확인할 것 |
| 17 | Rosetta 활성화 시 amd64 성능 수치 | 공식 문서에 정량 수치 없음("emulation ... is slow" 정성 서술만) |
| 18 | 한국 회사 엔지니어링 블로그의 최신 컨테이너/멀티아키 사례 | 도메인 한정 검색 2회 시도, 최근 글 미발견 |

---

## 커버리지 자기평가

| 영역 | 등급 | 빠진 것 |
|---|---|---|
| **E. Spring 컨테이너화** | **보통** | 핵심(기본 빌더·`imagePlatform` 기본값·noble arm64 매니페스트·layered Dockerfile·compose 지원·Testcontainers)은 전부 1차 소스로 확보. Jib은 개념·차별점까지만 확보. 남은 결손: ①JVM `MaxRAMPercentage` 공식 문서 근거 없음(로컬 관측만) ②`layertools` 전환 시점 미확인 ③#46665 수정 버전 미확인 ④Jib 명령·버전·arm64 서술 미확인 |
| **B. 아키텍처(arm64/amd64)** | **보통** | 멀티플랫폼 3전략·드라이버 제약·containerd image store는 1차 확보. `exec format error` 공식 서술 없음, Rosetta 정량 성능 없음, buildx 드라이버 4종(docker/docker-container/kubernetes/remote) 전체 비교 문서 미열람 |
| **A. 맥에서의 실행 구조** | **충분** | VMM 3종·Rosetta 조건·VirtioFS·리소스 기본값(메모리 50%, swap 1GB)·라이선스 임계값·릴리스 라인 모두 1차 소스 + 날짜 확보. 기본 VMM이 무엇인지만 미확인(경미). "왜 VM이 끼는가"의 커널 논거는 G-1로 대체 가능 |
| **C. 대안 런타임** | **보통** | 4개 도구의 공개 최신 버전 + 날짜 확보, `docker context` 우선순위 공식 문장 확보. 그러나 OrbStack 전무, Rancher의 containerd/nerdctl 공식 문서 없음, 각 런타임의 VM/하이퍼바이저 아키텍처 비교는 1차 소스 없음 |
| **D. 이미지 만들기·업데이트** | **보통** | 캐시·`.dockerignore`·캐시 마운트·외부 캐시 + digest 고정·`--pull`/`--no-cache`·멀티스테이지까지 1차 확보(D-1, D-3). 남은 결손: semver 태깅·태그 승격 워크플로 공식 가이드 없음, distroless/Alpine/slim **비교** 기준 없음, `docker scout` CLI 명령 미확인, `dive`·`docker history` 소스 없음 |
| **F. Kubernetes** | **보통** | 지원 버전표·EOL 날짜·연 3회 주기·1년 패치 지원·dockershim 제거 버전·"What Kubernetes is not" 전문·kind/minikube 이미지 로딩 명령·kind v0.32.0 노드 이미지 전부 1차 확보. 그러나 **Docker Desktop 내장 K8s 버전이 미확인**(버전 민감 항목 결손) + kind 릴리스 날짜 폐기 + Ingress 예제·k3s/Colima K8s 경로 없음 → 루브릭상 충분 불가 |
| **G. 원리** | **보통** | namespaces(7)·cgroups(7)·OCI manifest는 최상급 1차(man-pages 6.18, 2026-02-08). overlayfs 전용 문서 미열람, 컨테이너 vs VM 보안 경계 논거 1차 없음, rootless/cosign/SBOM 전무 |
| **보너스(한국어)** | **부족** | 2018년 글 1건뿐. 최신 국내 사례 없음 |

**종합 판단:** 사용자 4대 요구 중 **1번(맥 환경)·2번(Spring 배포)·4번(K8s)은 챕터를 쓸 재료가 있다.** 3번(이미지 만들기·업데이트)도 D-1·D-3으로 뼈대가 섰다.

Phase 2 전에 보강할 순서(효용 큰 것부터):
1. **Jib 플러그인 문서** — 3경로 비교표의 한 칸이 비어 있다. 명령·버전·arm64 서술이 필요하다 (미확인 #19)
2. **베이스 이미지 비교(distroless/Alpine/Debian slim)** — 요구 3번의 "무엇 위에 얹을 것인가"에 판단 기준이 없다 (미확인 #13)
3. **한국어·국내 사례** — 현재 2018년 글 1건. 대상 독자 친화성이 가장 약한 지점
4. **Docker Desktop 내장 K8s 버전** — F를 충분으로 올리는 마지막 조각 (미확인 #8)
5. **`docker scout` CLI 레퍼런스** — 취약점 스캔 절을 명령 수준으로 쓰려면 필요 (미확인 #11)

**재조사 불필요:** noble 빌더 arm64(E-2에서 레지스트리 실물로 종결), `imagePlatform` 기본값(E-1 인용 확보), digest 고정·`--pull`/`--no-cache`(D-3), K8s 릴리스 주기·지원 범위(F-1).

---

## 신선도 원장

> **fact-checker에게 — "발행일 미확인"을 읽는 법.** 아래 표에 미확인이 많은 것은 리서치 태만이 아니라 **소스 유형의 구조적 특성**이다.
> - `docs.docker.com` / `docs.spring.io` / `kubernetes.io/docs` / `man7.org`(일부) / 프로젝트 문서 사이트는 **본문에 발행일을 노출하지 않는다.** 이 경우 "검색 시점"이 사실상의 유효 기준이다.
> - 반대로 **날짜가 있는 행은 실제로 페이지에 인쇄된 값**이다: Docker Desktop 릴리스 노트(2026-07-20), Kubernetes 릴리스 표(2026-06-09 등), dockershim FAQ(2022-02-17), man-pages(2026-02-08), GitHub 이슈·논의(2024-04-04, 2025-08-04), 우아한형제들 글(2018-03-13).
> - **GitHub Releases에서 온 날짜는 폐기했다**(상충 9). 해당 행의 "미확인"은 적극적 판단이지 누락이 아니다.

| 주장 | 값 | 1차 소스 URL | 발행일 | 검색 시점 |
|------|-----|--------------|--------|-----------|
| Spring Boot 현재 GA (Latest 배지) | v4.1.0 (3.5.x 병행 유지) | https://github.com/spring-projects/spring-boot/releases | 미확인 (날짜 폐기, 상충 9) | 2026-07-25 |
| kind 최신 릴리스 | v0.32.0, 기본 노드 이미지 `kindest/node:v1.36.1` | https://github.com/kubernetes-sigs/kind/releases | 미확인 (날짜 폐기, 상충 9) | 2026-07-25 |
| Spring Boot 플러그인 문서의 기본 빌더 이미지 | `paketobuildpacks/builder-noble-java-tiny:latest` | https://docs.spring.io/spring-boot/gradle-plugin/packaging-oci-image.html | 미확인 (문서 표기 4.1.0) | 2026-07-25 |
| `imagePlatform` 도입 버전 | Since 3.4.0 | https://docs.spring.io/spring-boot/maven-plugin/build-image.html | 미확인 (문서 표기 4.1.0) | 2026-07-25 |
| `imagePlatform` 기본값 | 없음 = 호스트 머신 플랫폼 사용 | https://docs.spring.io/spring-boot/maven-plugin/build-image.html | 미확인 (문서 표기 4.1.0) | 2026-07-25 |
| noble 빌더의 퍼블리시 플랫폼 | linux/amd64 + linux/arm64 (OCI image index) | `docker buildx imagetools inspect paketobuildpacks/builder-noble-java-tiny:latest --raw` (레지스트리 직접 조회) | 해당 없음 (레지스트리 현재 상태) | 2026-07-25 |
| `paketobuildpacks/run-noble-tiny:latest` 플랫폼 | linux/amd64 + linux/arm64 | 동일 도구 조회 | 해당 없음 | 2026-07-25 |
| Paketo Java 빌드팩 arm64 beta 태그 해제 | "no need for beta tag anymore, it's in latest" (2024-05-22 코멘트) | https://github.com/paketo-buildpacks/java/discussions/1387 | 2024-04-04 (이후 코멘트 2024-07-27) | 2026-07-25 |
| arm64 미지원 Java 빌드팩 | `aternity`, `google-stackdriver` 2종 | https://github.com/paketo-buildpacks/java/discussions/1387 | 2024-06-11 (코멘트) | 2026-07-25 |
| bootBuildImage 크로스 빌드 버그 보고 환경 | Spring Boot 3.5.4 / M4 Pro arm64 | https://github.com/spring-projects/spring-boot/issues/46665 | 2025-08-04 (오픈) | 2026-07-25 |
| 위 이슈의 수정 버전 | **미확인** | 동일 | 미확인 | 2026-07-25 |
| Spring Boot jar 추출 명령 | `java -Djarmode=tools -jar app.jar extract --layers --destination extracted` | https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html | 미확인 (문서 표기 4.1.0) | 2026-07-25 |
| Spring 공식 Dockerfile 예제 베이스 이미지 | `bellsoft/liberica-openjre-debian:25-cds` | 동일 | 미확인 (문서 표기 4.1.0) | 2026-07-25 |
| `spring-boot-docker-compose` 라이프사이클 값 | `none` / `start-only` / `start-and-stop` | https://docs.spring.io/spring-boot/reference/features/dev-services.html | 미확인 (문서 표기 4.1.0) | 2026-07-25 |
| Testcontainers Colima 설정 3종 env var | `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE`, `TESTCONTAINERS_HOST_OVERRIDE`, `DOCKER_HOST` | https://java.testcontainers.org/supported_docker_environment/ | 미확인 | 2026-07-25 |
| `UseContainerSupport` 기본값·플랫폼 | 기본 true, **Linux only** | https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html | 미확인 | 2026-07-25 |
| `MaxRAMPercentage` 기본값 | 25.0 (**로컬 JDK 21.0.10 관측값**, 공식 문서 미확인) | `java -XX:+PrintFlagsFinal -version` (이 책을 쓴 맥) | 해당 없음 | 2026-07-25 |
| Paketo Memory Calculator 공식 | `Heap = Total Container Memory - Non-Heap - Headroom` | https://paketo.io/docs/reference/java-reference/ | 미확인 | 2026-07-25 |
| Paketo 기본 `-XX:ReservedCodeCacheSize` | 240MB | https://paketo.io/docs/reference/java-reference/ | 미확인 | 2026-07-25 |
| containerd image store 기본 활성 버전 | Docker Desktop **4.34 이상** | https://docs.docker.com/desktop/features/containerd/ | 미확인 | 2026-07-25 |
| 클래식 이미지 스토어의 한계 | 매니페스트 리스트 미지원 → 멀티플랫폼 로컬 로드 불가 | 동일 | 미확인 | 2026-07-25 |
| Docker Desktop 최신 릴리스 | **4.83.0 / 2026-07-20** | https://docs.docker.com/desktop/release-notes/ | 2026-07-20 | 2026-07-25 |
| 4.83.0 번들 Docker Engine | v29.6.2 | 동일 | 2026-07-20 | 2026-07-25 |
| 4.83.0 번들 Docker Compose | v5.3.1 | 동일 | 2026-07-20 | 2026-07-25 |
| 4.83.0 번들 "Docker Desktop Build" | v0.36.0 (probe의 buildx v0.35.0-desktop.2와 불일치 — 상충 4) | 동일 | 2026-07-20 | 2026-07-25 |
| Docker Desktop 무료 사용 임계값 | 직원 250명 미만 **AND** 연매출 $10M 미만 | https://docs.docker.com/subscription/desktop-license/ | 미확인 | 2026-07-25 |
| Rosetta 설정의 전제 조건 | Apple Virtualization framework를 VMM으로 선택해야만 사용 가능 (기본 Disabled) | https://docs.docker.com/desktop/settings-and-maintenance/settings/ | 미확인 | 2026-07-25 |
| Docker VMM의 Rosetta 지원 | 미지원 — "emulation of amd64 architectures is slow" | https://docs.docker.com/desktop/features/vmm/ | 미확인 | 2026-07-25 |
| Docker Desktop 기본 파일공유 구현 | VirtioFS (대안 gRPC FUSE) | https://docs.docker.com/desktop/settings-and-maintenance/settings/ | 미확인 | 2026-07-25 |
| Docker Desktop 기본 메모리 한도 | 호스트 메모리의 50% (swap 기본 1GB) | 동일 | 미확인 | 2026-07-25 |
| Rancher Desktop 최신 릴리스 | v1.23.1 / 2026-06-29 | https://github.com/rancher-sandbox/rancher-desktop/releases | 2026-06-29 | 2026-07-25 |
| Podman Desktop 최신 릴리스 | v1.28.3 / 2026-07-20 (podman 5.8.5 번들) | https://github.com/podman-desktop/podman-desktop/releases | 2026-07-20 | 2026-07-25 |
| Colima 최신 릴리스 | v0.10.3 / 2025-06-04 (1년 이상 신규 릴리스 없음) | https://github.com/abiosoft/colima/releases | 2025-06-04 | 2026-07-25 |
| OrbStack 버전 | **미확인** | — | 미확인 | 2026-07-25 |
| docker context 우선순위 | CLI 플래그 > 환경변수(`DOCKER_HOST`/`DOCKER_CONTEXT`) > 활성 context | https://docs.docker.com/engine/manage-resources/contexts/ | 미확인 | 2026-07-25 |
| Kubernetes 지원 마이너 | 1.36 / 1.35 / 1.34 (최근 3개) | https://kubernetes.io/releases/ | 미확인 | 2026-07-25 |
| Kubernetes 최신 패치 | 1.36.2 (2026-06-09), EOL 2027-06-28 | https://kubernetes.io/releases/ | 2026-06-09 | 2026-07-25 |
| Kubernetes 릴리스 주기 | "approximately three times per year" (연 3회) | https://kubernetes.io/releases/release/ | 미확인 | 2026-07-25 |
| Kubernetes 패치 지원 기간 | 1.19 이상 약 1년 | https://kubernetes.io/releases/ | 미확인 | 2026-07-25 |
| dockershim 제거 버전 | Kubernetes **1.24** | https://kubernetes.io/blog/2022/02/17/dockershim-faq/ | 2022-02-17 | 2026-07-25 |
| `docker build` 이미지의 K8s 호환성 | "will work with all CRI implementations" | 동일 | 2022-02-17 | 2026-07-25 |
| K8s 기본 imagePullPolicy 규칙 | `IfNotPresent`, 단 태그가 `:latest`면 `Always` | https://kind.sigs.k8s.io/docs/user/quick-start/ | 미확인 | 2026-07-25 |
| kind 로컬 이미지 적재 명령 | `kind load docker-image my-app:latest` | 동일 | 미확인 | 2026-07-25 |
| minikube 로컬 이미지 적재 명령 | `minikube image load my_image` | https://minikube.sigs.k8s.io/docs/handbook/pushing/ | 미확인 | 2026-07-25 |
| Linux 네임스페이스 종류 | 8종 (Cgroup/IPC/Network/Mount/PID/Time/User/UTS) | https://man7.org/linux/man-pages/man7/namespaces.7.html | 2026-02-08 (man-pages 6.18) | 2026-07-25 |
| cgroups v2 컨트롤러 | cpu, cpuset, freezer, hugetlb, io, memory, perf_event, pids, rdma | https://man7.org/linux/man-pages/man7/cgroups.7.html | 2026-02-08 (man-pages 6.18) | 2026-07-25 |
| OCI 이미지 매니페스트 미디어 타입 | `application/vnd.oci.image.manifest.v1+json` | https://github.com/opencontainers/image-spec/blob/main/manifest.md | 미확인 (main 브랜치) | 2026-07-25 |
| OCI 이미지 인덱스 미디어 타입 | `application/vnd.oci.image.index.v1+json` (레지스트리 응답에서 실물 확인) | 레지스트리 직접 조회 + image-spec | 해당 없음 | 2026-07-25 |
| 태그의 해석 방식 | `FROM alpine:3.21` → 3.21의 최신 패치로 해석됨(고정 아님) | https://docs.docker.com/build/building/best-practices/ | 미확인 | 2026-07-25 |
| digest 고정의 보장 | 퍼블리셔가 태그를 갈아끼워도 같은 이미지 보장 | 동일 | 미확인 | 2026-07-25 |
| 베이스 이미지 갱신 명령 | `docker build --pull` (캐시 무시는 `--no-cache`) | 동일 | 미확인 | 2026-07-25 |
| Jib의 정의 | "builds optimized Docker and OCI images for your Java applications without a Docker daemon" | https://github.com/GoogleContainerTools/jib | 미확인 | 2026-07-25 |
| Jib 플러그인 버전·명령 | **미확인** | — | 미확인 | 2026-07-25 |
| 우아한형제들 K8s 테스트 환경 글 | 2018년 글 — 명령·버전 인용 금지 | https://techblog.woowahan.com/2562/ | 2018-03-13 | 2026-07-25 |

---

## 수집 한계

- **검색 도구 실패:** `https://bugs.openjdk.org/browse/JDK-8350596` 는 **HTTP 403**으로 접근 실패했다(컨테이너 워크로드의 `MaxRAMPercentage` 기본값 변경 논의). 재시도 대신 로컬 `PrintFlagsFinal` 관측으로 대체했다. 이 항목은 여전히 1차 문서 근거가 없다.
- **의도적으로 제외한 소스:** 개인 블로그·Medium·Stack Overflow는 버전·플래그·기본값의 근거로 채택하지 않았다(과제 규칙). 검색 결과에 노출됐던 `dashaun.com`, `dev.to`, Medium 글들은 **열지 않았고 인용하지 않는다.**
- **WebSearch 요약문 자체를 소스로 쓰지 않았다.** 첫 검색 요약이 "Spring Boot 3.4.0의 멀티아키 지원", "dashaun/builder:tiny 대안" 등을 단언했으나, 인용문이 아닌 생성 문장이므로 채택하지 않고 전부 1차 소스로 재확인했다.
- **레지스트리 조회는 시점 의존적이다.** E-2의 digest는 2026-07-25의 `:latest` 상태다. 책에는 digest 문자열을 못 박지 말 것.
