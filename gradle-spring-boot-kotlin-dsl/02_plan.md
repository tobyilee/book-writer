# Gradle 9.5 × Spring Boot 저술 계획

## 0. 책 한 문장 요약 (logline)

> **build.gradle.kts에 의존성 몇 줄만 추가하던 Spring Boot 백엔드 개발자가 멀티 모듈·커스텀 플러그인·Native까지 자기 빌드를 도구로 키우는 여정. Gradle 9.5 · Kotlin DSL 기준.**

EPUB 메타·표지·소개 markdown에 그대로 들어간다. 한 호흡이 길어지지 않도록 두 문장으로 끊었다 (리뷰 §13 반영). Configuration Cache는 logline에서 빼고 "도구로 키우는"으로 압축 — 본문 13장에서 만난다.

---

## 1. 제목 후보

각 후보는 Spring Boot 백엔드 개발자가 "이건 내 책이다"라고 인식할 만한 톤을 노린다. 부제로 Kotlin DSL · Gradle 9.5를 명시해서 검색 가능성과 정확성을 동시에 확보한다.

1. **빌드를 다시 짠다 — Gradle 9.5와 Kotlin DSL로 키우는 Spring Boot 빌드**
   - 톤: 선언적이면서 동반자적. "다시 짠다"가 Maven 사고를 버리고 Gradle 사고로 옮긴다는 함의를 준다.
   - 포지셔닝: Maven 출신과 Gradle 무지한 Spring Boot 개발자 모두에게 "지금까지 build.gradle.kts에 의존성 몇 줄만 쓰던 시절은 끝났다"는 메시지.

2. **build.gradle.kts를 진지하게 — Spring Boot 백엔드 개발자의 Gradle 9.5 실전 가이드**
   - 톤: 솔직하고 실무적. "진지하게"가 그동안 빌드 스크립트를 가볍게 다뤘던 독자의 공감 트리거.
   - 포지셔닝: 검색·서점 알고리즘에 잘 잡히는 키워드(build.gradle.kts, Spring Boot, Gradle 9.5)를 정면에 노출. 기술서 매대용으로 안전한 선택.

3. **자라나는 빌드 — Spring Boot × Gradle 9.5 × Kotlin DSL로 멀티 모듈·커스텀 플러그인·네이티브까지**
   - 톤: 이야기 중심. 책의 서사 축(앱이 자라는 이야기)을 제목에 직접 박아넣는다.
   - 포지셔닝: 다른 Gradle 책과의 차별화. 단순 레퍼런스가 아니라 한 앱을 따라가며 빌드가 자라는 책이라는 약속.

**추천:** **1번 "빌드를 다시 짠다" + 부제 단축안 적용**.
- 첫 문장이 짧고 강하다 — 서점·온라인 매대에서 시각적으로 잡힌다.
- "다시 짠다"가 책의 두 가지 핵심 메시지를 동시에 함축한다: (a) Maven 사고를 버리고 Gradle 사고로 재구성하라, (b) build.gradle.kts 한 파일짜리 빌드를 멀티 모듈·플러그인·CI로 재구성하라.
- **최종 표지 표기:** `빌드를 다시 짠다 — Spring Boot × Gradle 9.5 × Kotlin DSL 실전 가이드` (리뷰 §12 반영, 부제 단축으로 한 줄 시인성 확보. "키우는"은 표지에서 빼고 1장 도입부와 logline에서 회수).

---

## 2. 책 특성

### 장르
**에세이형 기술서 + 실전 가이드**. 평어체와 청유형으로 동반자적 톤을 유지하되, 모든 챕터는 실제 빌드되는 코드를 동반한다. 단순 매뉴얼 번역도, 순수 에세이도 아니다.

### 분량
- **18개 챕터, 5개 부.**
- 전체 약 **120,000~140,000 한글 글자** (영문 기준 약 70k~80k 단어, 인쇄 기준 약 400~480쪽).
- 챕터당 평균 6,000~8,000자. Part I·II 입문부는 다소 짧게 (5,000자 내외), Part III 이후 심화부는 길게 (8,000~10,000자).
- 부록 제외. 부록은 1차 산출 후 필요 시 추가 결정.

### 난이도 곡선
- **Part I (1~3장):** 초급~중급. Gradle 사고방식을 다시 잡는다. Maven 출신을 명시적으로 끌어안는다.
- **Part II (4~7장):** 중급. 단일 모듈 Spring Boot 앱을 처음부터 끝까지 책임지고 빌드한다.
- **Part III (8~11장):** 중급~고급. 모듈을 쪼개고 build logic을 분리한다.
- **Part IV (12~14장):** 고급. 빌드를 도구로 만든다 — 커스텀 플러그인, Configuration Cache, CI.
- **Part V (15~18장):** 고급. 운영의 무게 — Native, 의존성 보안, 마이그레이션. 마지막 18장은 정리·전망.

### 독자 여정
**진입 상태:** Spring Boot 앱은 만들어봤지만 `build.gradle.kts`는 의존성만 추가하는 영역이다. Maven 출신이라 Gradle의 멘탈 모델이 어색하다. 멀티 모듈을 시도했다가 `bootJar` 함정에 빠진 적이 있다. Configuration Cache라는 단어를 들어봤지만 켤 엄두를 못 낸다.

**출구 상태:**
1. Gradle의 Settings/Project/Task/Configuration 모델을 자기 언어로 설명할 수 있다.
2. Kotlin DSL의 lazy Property/Provider API로 build script를 쓰고, eager 패턴을 골라낼 수 있다.
3. Version Catalog + BOM(platform) 조합으로 의존성을 다스리고, `io.spring.dependency-management` 의 위치를 안다.
4. 멀티 모듈 Spring Boot 프로젝트를 `subprojects {}` 없이 Convention Plugin으로 정리한다.
5. Configuration Cache를 켜고, 위반을 진단하고, 자기 빌드를 호환되게 고친다.
6. 커스텀 Task와 Plugin을 Provider/Property 기반으로 만든다.
7. GitHub Actions에 `gradle/actions/setup-gradle` 으로 빌드 캐시·Build Scan·Dependency Graph를 붙인다.
8. GraalVM Native Image, Dependency Verification, Locking, Repository Content Filtering을 운영 환경에 적용할 판단 기준을 갖는다.
9. Gradle 9.x 마이그레이션을 자신감 있게 진행한다.

### 코드 저장소 컨벤션

책 전체가 **하나의 가상 앱 `shop`을 따라간다.** GitHub 레포는 `shop-gradle-journey` (가상)로, 챕터별 폴더 구조:

```
shop-gradle-journey/
├── ch01/               # 가장 단순한 build.gradle.kts (의존성 한 줄)
├── ch02-maven-bridge/  # Maven pom.xml과 Gradle 빌드 1:1 매핑
├── ch04-bootapp/       # 단일 모듈 Spring Boot 앱 (이후 챕터의 기반)
├── ch08-multimodule/   # 멀티 모듈로 분리
├── ch09-convention/    # buildSrc + Convention Plugin
├── ch11-composite/     # build-logic included build
├── ch12-custom-plugin/ # 커스텀 plugin + 커스텀 task
├── ch13-config-cache/  # Configuration Cache 호환 전후
├── ch14-ci/            # .github/workflows + Gradle 캐시
├── ch15-native/        # GraalVM Native Image
├── ch16-security/      # verification-metadata.xml, lockfile
└── ...
```

각 챕터의 첫 페이지에 "이번 챕터는 `chXX-yyy/` 폴더에서 동작한다"는 한 줄로 독자가 GitHub에서 바로 찾을 수 있게 한다. **챕터 시작 시 `ch{N-1}`을 카피해서 위에 쌓는 방식**이라, 독자가 자기 앱이 자라는 흐름을 폴더 단위로 추적할 수 있다.

### 표기 컨벤션 (책 전체)
- **Kotlin DSL이 기본.** Groovy DSL은 차이가 클 때만 `> Groovy DSL` 박스로 짧게 병기.
- **마이그레이션 노트 박스:** Gradle 9.x 신문법은 본문에서 표준으로 다룬다. 9.0 이전과 다른 부분은 `> 마이그레이션 노트` 박스로 격리.
- **Maven 비교 박스:** Part I·II에서 적극 사용, Part III 이후는 거의 사용 안 함 (독자가 이미 Gradle 사고로 옮긴 시점).
- **함정 박스:** 실무에서 막히는 지점을 `> 함정` 박스로 본문에 명시.

---

## 3. 내러티브 아크

이 책은 **`shop`이라는 가상 Spring Boot 앱이 자라는 이야기**다. 챕터마다 "지금 우리 앱이 어디까지 왔는가"를 추적할 수 있도록 챕터 항목에 **이 챕터에서 자라는 앱 상태**를 한 줄로 박아넣는다.

5개 부의 역할:

### Part I — Gradle 사고방식 (1~3장)
독자의 멘탈 모델을 다시 짠다. Maven 출신을 명시적으로 끌어안고, Gradle의 Settings/Project/Task/Configuration/Lifecycle을 자기 언어로 설명할 수 있게 만든다. Kotlin DSL의 함정(eager vs lazy, `=` vs `.set()`, type-safe accessor)을 짚는다. 코드는 최소한, 사고 모델이 우선.

### Part II — 단일 모듈 Spring Boot를 제대로 빌드한다 (4~7장)
가장 단순한 Spring Boot 앱을 처음부터 끝까지 책임진다. `bootJar`/`bootRun`/`bootBuildImage`의 내부를 본다. 의존성을 다스리는 정석 — Version Catalog + platform(BOM). 테스트를 분리한다 (JVM Test Suite로 통합 테스트). 이 부의 끝에서 독자의 앱은 "기본기는 다 있는, 단일 모듈로는 부족함 없는 빌드"가 된다.

### Part III — 규모를 키운다 (8~11장)
앱이 자란다. 모듈을 쪼개고, `subprojects {}` 안티패턴을 피하고, Convention Plugin으로 build logic을 모듈화한다. `buildSrc`와 `build-logic` included build의 선택 기준을 잡는다. Composite Build로 외부 라이브러리와 동시 개발하는 패턴까지. 9장의 `bootJar` 함정은 책 전체의 클라이맥스 중 하나.

### Part IV — 빌드를 도구로 만든다 (12~14장)
빌드 스크립트의 소비자에서 생산자로 옮긴다. 커스텀 Task와 Plugin을 Provider/Property 기반으로 만든다. Configuration Cache · Build Cache · Incremental Build를 켜고 위반을 진단한다. CI에 빌드를 올린다. 이 부의 끝에서 독자는 자기 회사·팀에 맞는 빌드 도구를 만들 수 있다.

### Part V — 운영의 무게 (15~18장)
운영 환경에서 빌드가 짊어지는 책임 — GraalVM Native, 의존성 보안(verification/locking/content filtering), Gradle 9.x 마이그레이션, 마지막 18장은 "이제 어디로 갈 것인가" 정리·전망 (Isolated Projects, Develocity, 책에서 다루지 않은 영역 안내).

**왜 이 순서인가:** 빌드 도구는 운영의 마지막 보루다. 1~7장에서 "내 단일 모듈 앱이 잘 빌드되는가"를 확보하고, 8~11장에서 "팀과 함께 일하는 빌드"로 키우고, 12~14장에서 "내가 빌드를 통제하는가"를 만들고, 15~18장에서 "운영 환경에서 살아남는 빌드"로 마무리한다. **각 부의 끝마다 독자가 자기 회사 빌드를 한 단계 위로 올릴 수 있다.**

---

## 4. 챕터 목록

### Part I — Gradle 사고방식

#### 1장. 왜 build.gradle.kts를 다시 짜야 하는가
- **핵심 질문:** 이 책을 다 읽고 나면 Spring Boot 개발자는 build.gradle.kts를 어디까지 만질 수 있게 되는가? (리뷰 §9 반영 — 동기 부여형에서 출구 상태형으로 좁힘)
- **주요 내용:**
  - 빌드 스크립트가 곧 운영의 일부라는 명제 (멀티 모듈, CI, 보안, 이미지화의 출발점)
  - Gradle 9.5와 Spring Boot 4.0의 현재 상태 (Daemon JDK 17+, KGP 2.0+, Configuration Cache가 preferred mode)
  - 이 책이 다루는 가상 앱 `shop` 소개 — 1장의 빌드 스크립트는 의존성 한 줄, 마지막 장의 빌드는 멀티 모듈 + 커스텀 플러그인 + Native 이미지
  - 책 전반 관통하는 약속 — Kotlin DSL 기본, Maven 비교 박스 적극 활용 (Part I·II), 함정 박스로 막히는 지점 표시
  - 독자가 이 책을 통과한 후 할 수 있게 되는 9가지
  - **박스 — "Maven에서 옮겨온 분께":** phase는 task graph로, dependencyManagement는 platform/BOM으로, parent pom은 Convention Plugin으로. 정확한 매핑은 4장에서 받는다는 미끼. Maven으로 돌아갈 일 없게 만든다는 약속 (리뷰 §7·우선순위 §5 반영)
  - **박스 — "이미 8.x를 쓰는 분께":** 이 책은 9.5 기준. 회사 빌드를 9.x로 올릴 마이그레이션 체크리스트 핵심 5개는 17장. 책 본문 흐름을 따라가도 좋고, 17장을 먼저 훑어도 좋다 (리뷰 §2·우선순위 §5 반영)
  - **박스 — wrapper distribution-type:** `./gradlew` 처음 쓰는 독자가 `--distribution-type=bin`을 모르면 200MB+ all distribution을 받아 첫 빌드를 지연시킨다. 14장에서 자세히 다루지만, 첫 빌드 전에 한 줄 처방 (리뷰 §11 반영)
- **이 챕터에서 자라는 앱 상태:** 아직 없다 — 책의 입구.
- **예상 분량:** 짧음 (5,000자) — Maven 미끼 박스 + 8.x 안내 박스 추가로 500자 증가

#### 2장. Gradle의 사고 모델 — Settings, Project, Task, Lifecycle
- **핵심 질문:** Gradle은 빌드를 어떻게 객체로 본 다음 task graph로 옮기는가?
- **주요 내용:**
  - `settings.gradle.kts` — 빌드의 입구. 어떤 프로젝트가 참여하는가
  - `build.gradle.kts` — 한 프로젝트의 task/configurations/extensions
  - 3-phase Lifecycle (Initialization → Configuration → Execution)과 Configuration Cache가 캐싱하는 영역
  - Task의 lazy registration (`tasks.register`) vs eager (`tasks.create`) — 왜 lazy가 정석인가
  - Plugin 세 종류 (Binary / Script / Precompiled convention plugin)와 권장 흐름
  - Configuration의 세 역할 분리 (declarable / resolvable / consumable) — 9.x에서 명시화된 부분
  - Maven 비교 박스: pom.xml 한 파일 vs settings + build, dependency scope vs configuration
- **이 챕터에서 자라는 앱 상태:** 아직 없다 — 사고 모델만.
- **예상 분량:** 중간 (7,000자)

#### 3장. Kotlin DSL 그리고 그 함정
- **핵심 질문:** Groovy DSL과 Kotlin DSL은 어디서 미묘하게 다른가, 그리고 그 차이가 빌드 스크립트를 어떻게 바꾸는가? (리뷰 §9 반영 — lazy Property 단어 제거)
- **주요 내용:**
  - Kotlin DSL을 선택하는 이유 — 타입 안전성, IDE 지원, 첫 빌드의 단점
  - 문법 함정: 큰따옴표만 허용, type-safe accessor는 `plugins {}` 블록 이후에만 노출
  - `lazy property는 = 권장, eager get(tasks.getByName) 피하라`는 박스로만 가볍게 언급 — 본격적인 Provider/Property API 깊이는 12장에서 다룬다 (리뷰 §4·우선순위 §4 반영, Part I 입문 독자의 진입 장벽 낮춤)
  - `apply(plugin = ...)`로 적용하면 왜 accessor가 안 생기는가, `configure<T> {}` fallback
  - Groovy → Kotlin DSL 1:1 매핑 표
  - 9.5에서 추가된 precompiled Settings plugin type-safe accessor
  - 함정 박스: `subprojects {}` 미리 경고 (자세한 처방은 10장 — 8장은 박스 한 줄 경고만, 두 챕터 연속 cliffhanger를 피한다. 리뷰 §2 반영)
- **이 챕터에서 자라는 앱 상태:** `ch01/build.gradle.kts` — 의존성 한 줄짜리 Hello World 스크립트만 만들어 본다.
- **예상 분량:** 중간 (6,000자) — Provider/Property API 깊이 제거로 500자 축소

### Part II — 단일 모듈 Spring Boot를 제대로 빌드한다

#### 4장. Maven에서 옮겨오는 다리 — pom.xml과 build.gradle.kts의 1:1 매핑
- **핵심 질문:** Maven에서 쓰던 모든 개념은 Gradle에서 어디로 가는가?
- **주요 내용:**
  - `dependencyManagement` → `platform()` BOM 또는 `io.spring.dependency-management` 플러그인 (선택 기준은 5장에서 깊게)
  - `parent pom` → Convention Plugin (preview, 자세히는 10장)
  - `<profile>` → variant + property + `bootRun --args`
  - `<pluginManagement>` → `settings.gradle.kts pluginManagement {}`
  - `<repositories>` → `dependencyResolutionManagement { repositories {} }` + `FAIL_ON_PROJECT_REPOS`
  - `mvn` 명령 → `./gradlew` (그리고 wrapper의 의미)
  - **박스 — wrapper distribution-type=bin:** `./gradlew wrapper --gradle-version 9.5 --distribution-type=bin`을 명시하지 않으면 200MB+ all distribution을 받는다. 1장에서 미리 본 처방을 여기서 실행 (리뷰 §11 반영)
  - **박스 — Toolchain의 자리:** 처음부터 단일 모듈에서 잡고 가야 멀티 모듈로 갈 때 흔들리지 않는다. `java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }` + `foojay-resolver-convention` settings plugin. Daemon JVM ≠ Build JVM의 분리 한 페이지 (리뷰 §3·우선순위 §3 반영 — 13장에서 옮겨옴)
  - 함정 박스: Maven은 phase 모델, Gradle은 task graph — 같은 단어("clean", "test")의 의미가 다르다
  - 마이그레이션 노트 박스: `gradle init --type pom`의 한계
- **이 챕터에서 자라는 앱 상태:** `ch04-bootapp/` — Spring Boot Initializr가 만든 단일 모듈 앱. 이후 챕터의 기반. Toolchain까지 박혀 있다.
- **예상 분량:** 김 (8,500자) — Toolchain + wrapper 박스 추가로 1,000자 증가

#### 5장. 의존성을 다스리는 정석 — Version Catalog와 BOM
- **핵심 질문:** Spring Boot 앱에서 `implementation`, `platform(...)`, `gradle/libs.versions.toml`은 각각 어떤 역할인가?
- **주요 내용:**
  - **본문 굵은 메시지: BOM은 resolution, Catalog는 declaration. 둘은 직교한다 — 둘 다 쓴다.** 흐름을 "BOM → Catalog → 둘을 같이 쓴다"로 단순화 (리뷰 §4 반영)
  - declarable configuration 5개 (`implementation` / `api` / `compileOnly` / `runtimeOnly` / `annotationProcessor`)는 박스로 격리
  - Spring Boot 플러그인이 추가하는 `developmentOnly` / `testAndDevelopmentOnly` / `productionRuntimeClasspath`
  - **박스 — implementation vs api (레퍼런스 §15.1):** 기본은 `implementation`. `api`는 public API 표면 타입에만. 남용 시 transitive 재컴파일 폭발. `java-library` 플러그인 없으면 `api`는 존재하지 않는다 (application 모듈은 보통 `java` plugin이므로 `implementation`만 가능) (리뷰 §1 반영)
  - BOM 통합 두 가지 길: `platform()` (네이티브, 권장) vs `io.spring.dependency-management` 플러그인 (property 오버라이드만 장점)
  - `enforcedPlatform()`은 왜 권장 안 되는가
  - Version Catalog `gradle/libs.versions.toml` 구조와 `alias(libs.plugins.X)` / `libs.bundles.X`
  - **박스 — 의존성 그래프 디버깅:** `./gradlew :app:dependencies --configuration runtimeClasspath`, `./gradlew dependencyInsight --dependency slf4j`, `./gradlew build --scan`. 실무 독자가 빌드 디버깅 시 가장 먼저 닿는 도구 3개를 한 곳에 (리뷰 §1·§11 반영)
  - **박스 — Resolution Strategy 마지막 처방:** BOM으로 못 잡는 transitive를 `configurations.all { resolutionStrategy.eachDependency { ... } }`로 강제 (리뷰 §1 반영)
  - 함정 박스: `extra["springBootVersion"]` 같은 ext 변수는 버려라
  - **함정 박스 — 동시 적용 금지:** `io.spring.dependency-management` 플러그인 + `platform()` BOM을 동시에 적용하면 두 메커니즘이 같은 BOM을 두 번 적용해 우선순위가 모호해진다. 하나만 골라라 (리뷰 §6 반영)
- **이 챕터에서 자라는 앱 상태:** `ch04-bootapp/`에 `libs.versions.toml` 도입, `platform(libs.spring.boot.bom)` 적용.
- **예상 분량:** 김 (9,000자) — declarable 5개 박스화 + 디버깅·resolutionStrategy·동시 적용 함정 추가로 500자 증가. 핵심 메시지는 단순화 유지.

#### 6장. Spring Boot Gradle 플러그인의 내부 — bootJar, bootRun, bootBuildImage
- **핵심 질문:** `org.springframework.boot` 플러그인을 적용하면 정확히 무엇이 일어나는가? 그리고 Spring Boot 3.x 빌드를 그대로 4.0으로 올릴 때 무엇이 바뀌는가? (리뷰 §1·우선순위 §2 반영 — 표지에 Spring Boot 4.0을 박은 이상 핵심 페르소나의 절박한 질문에 답)
- **주요 내용:**
  - 플러그인 적용 시 `java` plugin에 반응해 자동 생성되는 task와 configuration
  - `bootJar`의 내부 구조 — `BOOT-INF/classes`, `BOOT-INF/lib`, `layers.idx`, `spring-boot-loader`의 `JarLauncher`
  - 레이어드 JAR 기본 ON과 OCI 이미지 캐시 최적화의 관계
  - main class detection — 자동 탐지 vs 명시
  - `bootJar`와 `jar` task의 공존 — `assemble`이 둘 다 만든다
  - `bootRun extends JavaExec` — JavaExec의 모든 옵션이 통한다, `--args`로 런타임 인자
  - `bootBuildImage` — Paketo Buildpack 기반, Dockerfile 없이 OCI 이미지, 레지스트리 push까지
  - **섹션 — Spring Boot 3.x → 4.x 옮길 때 무엇이 깨지는가:** Gradle 8.14+/9.x 요구의 정확한 의미, 플러그인 좌표·task 시그니처 변화, Paketo builder 기본값 변화(`paketobuildpacks/builder-noble-java-tiny`), AOT 동작 변경, Native 통합 변경, lazy property `= ` 권장 강화. 17장의 Gradle 마이그레이션과는 별개로, **Spring Boot 버전 마이그레이션의 자리는 여기**임을 명시. 3.5.x 유지 보수 라인 독자를 위한 분기 가이드 한 박스 (리뷰 §1·우선순위 §2 반영)
  - 마이그레이션 노트 박스: 옛 `bootJar { mainClass = ... }` 문법과 9.x 표준의 차이
- **이 챕터에서 자라는 앱 상태:** `ch04-bootapp/`이 `./gradlew bootJar`로 실행 가능 fat jar를 만들고, `./gradlew bootBuildImage`로 OCI 이미지를 만든다.
- **예상 분량:** 김 (9,000자) — Spring Boot 3.x → 4.x 섹션 추가로 500자 증가

#### 7장. 테스트를 분리한다 — JVM Test Suite로 통합 테스트
- **핵심 질문:** 단위 테스트와 통합 테스트를 같은 `test` task에 욱여넣지 않으려면 어떻게 하는가?
- **주요 내용:**
  - `test` task의 기본 동작과 `useJUnitPlatform()` / `useJUnitJupiter()` 차이
  - `jvm-test-suite` 플러그인 — 9.x의 표준 (incubating 기간 종료)
  - `integrationTest` suite를 register하고, 자동 생성되는 소스셋·configuration·task
  - `shouldRunAfter(test)`로 실행 순서 힌트, `check` 의존성으로 CI에서 자동 포함
  - Testcontainers 통합 — `integrationTestImplementation`에 의존성 추가
  - Spring Boot의 `@SpringBootTest` 슬라이스 테스트와 task 분리의 결합
  - 마이그레이션 노트: 옛 `sourceSets.create("integrationTest")` 패턴과 비교
- **이 챕터에서 자라는 앱 상태:** `ch04-bootapp/`에 `src/integrationTest/` 디렉터리 추가, `./gradlew check`가 두 suite 모두 실행.
- **예상 분량:** 중간 (7,000자)

### Part III — 규모를 키운다

#### 8장. 모듈을 쪼갠다 — settings 구조와 프로젝트 간 의존
- **핵심 질문:** 단일 모듈 앱을 `app + domain + order + payment` 같은 멀티 모듈로 어떻게 옮기는가?
- **주요 내용:**
  - `settings.gradle.kts`의 `include(...)`와 모듈 디렉터리 구조
  - `dependencyResolutionManagement` + `RepositoriesMode.FAIL_ON_PROJECT_REPOS` — 모든 repo는 root settings에서만
  - `pluginManagement {}` — 플러그인 버전의 단일 출처
  - `dependencies { implementation(project(":domain")) }`로 프로젝트 간 의존
  - 멀티 모듈에서 Version Catalog가 자동 공유되는 방식
  - 함정 박스 (한 줄): `subprojects {}` / `allprojects {}`는 안티패턴 — 10장에서 처방. 8·9·10장 연속 cliffhanger를 피하기 위해 짧게만 (리뷰 §2 반영)
  - **챕터 마지막 — Cliffhanger 박스 "정상 빌드가 안 된다 — 9장의 미스터리":** 4개 모듈로 쪼개고 `./gradlew :app:bootRun`을 돌려보면 `domain`의 클래스를 못 찾는다는 사고가 일어난다. 출력 로그를 그대로 보여주고, 왜 그런지의 진단을 9장 도입부로 자연스럽게 잇는다 (리뷰 §2·우선순위 §1 반영)
- **이 챕터에서 자라는 앱 상태:** `ch08-multimodule/` — `app + domain + order + payment` 4모듈로 분리. **정상 빌드가 아직 안 된다 — 9장의 bootJar 함정에 걸려 있다.** 아직 모든 build script가 중복.
- **예상 분량:** 중간 (7,000자) — cliffhanger 박스는 본문의 마무리 톤으로 짧게

#### 9장. bootJar 함정 — library 모듈에서 빈 jar가 나오는 사고를 어떻게 진단하고 어떻게 막는가
- **핵심 질문:** library 모듈에서 빈 jar가 나오는 사고를 어떻게 진단하고 어떻게 막는가? (리뷰 §9 반영 — 액션 지향형 질문)
- **주요 내용:**
  - **도입: 8장 마지막의 실패 명령에서 시작.** `./gradlew :app:bootRun` 출력 로그를 다시 가져와 "이 ClassNotFound가 왜 일어나는지부터 본다"로 자연스럽게 잇기 (리뷰 §2·우선순위 §1 반영)
  - 진단: `./gradlew :domain:dependencies`, `unzip -l domain/build/libs/domain-*.jar` 으로 빈 jar 확인 — 독자가 자기 빌드에서 같은 사고를 진단하는 5분 체크리스트 박스 (리뷰 §3 반영)
  - Spring Boot Gradle 플러그인이 멀티 모듈에서 깨는 정확한 이유 — `bootJar`만 생기고 일반 `jar`가 비활성화되는 메커니즘
  - 해결법 1: library 모듈에는 플러그인을 아예 적용 안 한다 + BOM만 platform으로 들여온다 (권장)
  - 해결법 2: `id("org.springframework.boot") apply false` + `java-library`로 일부 task만 끄기
  - `bootArchives` configuration의 의미와 publishing과의 관계
  - 실전 비교: 똑같은 `app + domain` 구조를 두 가지 방법으로 빌드해서 결과 jar 차이를 출력으로 보여준다
  - 함정 박스: 이 문제는 Spring Boot 공식 이슈 #16689 — 책에서 가장 자주 인용되는 함정 중 하나
  - **박스 — 실제 사고 회고:** 한국어 사례 (우아한형제들/카카오/라인 기술블로그에서 발굴, 챕터 저술 시 community-research pass에서 1~2개 인용). 리뷰 §3 + 6장 작성자 메모 반영
  - **챕터 마지막 — 10장 연결:** "이제 빌드는 된다. 하지만 4개 모듈의 build.gradle.kts가 거의 똑같다. 10장에서 정리한다" (리뷰 §2 반영)
- **이 챕터에서 자라는 앱 상태:** `ch08-multimodule/`이 정상 빌드된다 — `domain`/`order`/`payment`는 library, `app`만 Spring Boot 플러그인. 다만 4개 모듈의 빌드 스크립트가 거의 똑같다 — 10장에서 정리.
- **예상 분량:** 김 (9,000자) — 책 전체의 클라이맥스 중 하나. 실제 사고 회고 + 5분 진단 체크리스트로 콘텐츠 밀도 확보 (리뷰 §3 반영)

#### 10장. Convention Plugin으로 build logic을 모듈화한다
- **핵심 질문:** 4개 모듈에 똑같이 들어가는 `java { toolchain { ... } }`, `useJUnitPlatform()`, BOM 적용을 어떻게 한 곳에 모으는가?
- **주요 내용:**
  - `subprojects {}` 안티패턴이 일으키는 구체적 문제 — configuration-time coupling, IDE 추적 불가, Configuration Cache 친화성 ↓
  - Precompiled convention plugin이 답이다 — `*.gradle.kts` 파일 이름이 곧 plugin id
  - `buildSrc/` 구조: `build.gradle.kts`, `kotlin-dsl` plugin, `gradlePluginPortal()` repo
  - `buildSrc/src/main/kotlin/shop.java-conventions.gradle.kts`, `shop.spring-boot-conventions.gradle.kts` 작성
  - convention plugin에서 BOM을 적용하는 방법 — `"implementation"(platform(...))` string-receiver
  - 적용 측 `plugins { id("shop.spring-boot-conventions") }` — 깔끔한 한 줄
  - convention plugin이 다른 convention plugin을 적용하는 패턴 (`shop.spring-boot-conventions`가 `shop.java-conventions`을 의존)
  - **박스 — "왜 여기서 갑자기 string?":** convention plugin에서 `"implementation"(platform(...))` 같은 string-receiver가 등장하는 이유. type-safe accessor는 해당 plugin이 적용된 시점 이후에만 노출되는데, precompiled plugin은 java plugin이 아직 적용 안 된 시점이라 string fallback. Kotlin DSL의 타입 안전성을 강조해온 책에서 갑자기 string이 등장하는 혼란을 정면 해소 (리뷰 §8 반영)
  - Maven 비교 박스: parent pom vs Convention Plugin (마지막 비교 박스, 이 시점에서 독자는 이미 Gradle 사고)
- **이 챕터에서 자라는 앱 상태:** `ch09-convention/` — 4개 모듈의 build.gradle.kts가 각 한 줄로 줄어든다.
- **예상 분량:** 김 (8,500자)

#### 11장. buildSrc 한계를 넘는다 — build-logic included build와 Composite Build
- **핵심 질문:** `buildSrc`를 건드릴 때마다 모든 task가 out-of-date되는 게 답답하다. 그리고 외부 라이브러리와 동시에 개발하고 싶다.
- **주요 내용:**
  - `buildSrc` 한계: 변경 시 모든 task out-of-date, classpath 충돌, 재사용 불가
  - `build-logic`을 별도 included build로 옮기기 — 자체 `settings.gradle.kts`, `pluginManagement { includeBuild("build-logic") }`
  - buildSrc → build-logic 마이그레이션 step-by-step
  - Composite Build의 본질 — 별개의 Gradle 빌드를 한 트리에 묶는다
  - `includeBuild("../shared-library")` — group:name 매칭으로 자동 substitution
  - 매칭이 안 될 때 `dependencySubstitution { substitute(...) }`로 명시
  - 세 가지 용도 중 build-logic 분리가 핵심. co-development와 monorepo는 "언제 이게 필요한가" 가이드 한 박스로 좁힘 (리뷰 §4 반영 — Spring Boot 백엔드 핵심 페르소나의 실무 빈도가 낮음)
  - 선택 가이드: 단일 root + 모듈 < 10 → buildSrc, 모듈 많음/회사 표준 → build-logic, 외부 라이브러리 co-development → Composite (한 줄 가이드만)
- **이 챕터에서 자라는 앱 상태:** `ch11-composite/` — `build-logic`이 included build로 분리. 외부 `shop-shared` 라이브러리는 한 박스 시나리오로만 짧게 소개.
- **예상 분량:** 중간 (7,000자) — co-development 분량 축소로 1,000자 감소 (리뷰 §4 반영)

### Part IV — 빌드를 도구로 만든다

#### 12장. 커스텀 Task와 Plugin — Provider/Property로 lazy하게
- **핵심 질문:** Git SHA를 파일로 떨궈주는 task 하나를 만들고 싶다. 그런데 Configuration Cache랑 호환되게.
- **주요 내용:**
  - `DefaultTask`를 상속한 `abstract class` + `abstract val` 패턴 (9.x 표준)
  - Input/Output annotation — `@Input`, `@InputFile`, `@OutputFile`, `@Classpath`, `@Nested`, `@CacheableTask`
  - Property/Provider API — 즉시 평가를 피한다 (3장에서 박스로만 본 주제를 여기서 본격적으로 다룬다 — 리뷰 §4 반영)
  - `providers.exec { commandLine("git", "rev-parse", "HEAD") }` 으로 git SHA 가져오기
  - `providers.environmentVariable("...")`, `providers.systemProperty("...")` — Configuration Cache 친화
  - **박스 — Project property vs system property vs ext 변수:** `-P` vs `-D` vs `extra[]` 세 가지의 정확한 차이와 언제 어느 것을 쓰는가 (리뷰 §11 반영)
  - `layout.buildDirectory.file(...)`, `layout.projectDirectory.file(...)`
  - 금지 사항: `System.getenv()`, `File("...")`, `Task.getProject()` 실행 시점 호출, `Project.exec {}`
  - **함정 박스 — `outputs.upToDateWhen { false }`:** 매번 실행되게 만들어 Build Cache를 무효화하는 안티패턴. 정확한 입력/출력 어노테이션으로 풀어라 (리뷰 §6 반영)
  - Plugin 패턴: `Plugin<Project>` 구현, Extension 만들기, `project.extensions.create<T>("ext-name")`
  - Task 입출력 ↔ Extension 연결 — Property를 그대로 wire-up
  - 책의 가상 plugin `shop.build-info` — git SHA + 빌드 시간을 `resources/build-info.txt`로 떨궈주고, Spring Boot의 `@Value`로 읽는 코드까지 보여준다
  - **외부 발행은 Out of Scope:** Plugin Portal/사내 Maven 발행 절차는 본 챕터에서 다루지 않는다. `java-gradle-plugin` + `gradlePlugin {}` plugin id 등록까지만 한 박스 — 리뷰 §3·우선순위 §3에 따른 분량 분산
  - 마이그레이션 노트: Gradle 7 이전의 eager `tasks.create` / `<<` 연산자와 비교
- **이 챕터에서 자라는 앱 상태:** `ch12-custom-plugin/` — `build-logic`에 `shop.build-info` 커스텀 plugin 추가, app에 적용.
- **예상 분량:** 김 (8,000자) — Plugin Portal 발행 부분 축소로 1,500자 감소. `shop.build-info` 한 가지 예에 집중 (리뷰 §3·우선순위 §3 반영)

#### 13장. Configuration Cache를 켠다 — 위반을 진단하고 호환되게 고친다
- **핵심 질문:** Configuration Cache를 켰는데 third-party plugin이 비명을 지른다. 어떻게 점진적으로 도입하는가?
- **주요 내용:**
  - Configuration Cache가 캐시하는 것 (configuration phase 산출물) vs Build Cache가 캐시하는 것 (task execution)
  - 활성화 — `gradle.properties`에 `org.gradle.configuration-cache=true`, `problems=warn`으로 점진 도입
  - 9.0부터의 명시적 위반 보고 — silent fail이 아닌 명확한 메시지
  - 금지 패턴 ↔ 대체 API 표 (실행 시점 Project 접근, `System.getenv`, `File("")`, `Project.exec`, `whenReady` mutable state)
  - `parallel=true`까지 켜기 — 9.x에서 안정화
  - Build Cache 활성화 — local + remote (Develocity 옵션 짧게)
  - `@CacheableTask`와 정확한 input/output 어노테이션의 관계
  - Incremental Build의 동작 원리 — 입출력 해시 비교
  - **Toolchain은 4장으로 이동.** 13장에서 Toolchain을 빼고 분량 분산 (리뷰 §3·우선순위 §3 반영). 본 챕터에서는 Configuration Cache + Build Cache + Incremental에 집중
  - 현실 — 일부 enterprise plugin이 아직 비호환. `warn` 모드로 시작해서 위반을 하나씩 잡는 점진 도입 전략
  - **함정 박스 — IDE sync (레퍼런스 §15.10):** Configuration Cache는 빌드는 가속하지만 IDE sync 자체는 가속하지 않는다. IDE sync가 느린 문제의 답은 9.x incubating 단계의 Isolated Projects — 18장에서 다시 본다 (리뷰 §1·§5 반영)
  - **박스 — `--scan` 으로 위반 진단:** 5장에서 한 번 만난 Build Scan을 Configuration Cache 위반 진단에도 쓴다. timeline과 configuration cache 통계 (리뷰 §11 반영)
  - **표 — gradle.properties 표준 키 정리:** `org.gradle.caching`, `org.gradle.parallel`, `org.gradle.configuration-cache`, `org.gradle.configuration-cache.problems`, `org.gradle.jvmargs`, `org.gradle.workers.max` 한 곳에서 정리 (리뷰 §11 nice-to-have 반영)
- **이 챕터에서 자라는 앱 상태:** `ch13-config-cache/` — 모든 빌드가 Configuration Cache + Build Cache hit으로 빠르게 돌아간다. `shop.build-info`가 호환되도록 12장 코드를 손본 비교 보여준다.
- **예상 분량:** 김 (8,500자) — Toolchain 부분 4장으로 이전 + 분량 분산으로 1,000자 감소 (리뷰 §3·우선순위 §3 반영)

#### 14장. CI에 올린다 — GitHub Actions와 Build Scan
- **핵심 질문:** 로컬에서 잘 도는 빌드를 CI에서도 빠르고 신뢰성 있게 돌리려면 무엇이 필요한가?
- **주요 내용:**
  - Gradle Wrapper의 의미 — `./gradlew`가 곧 빌드의 Gradle 버전 명세
  - `wrapper` task로 버전 올리기 — `--distribution-type=bin` 명시 (안 하면 200MB+ all)
  - 9.5의 wrapper retries — 다운로드 실패 시 재시도
  - `gradle/actions/setup-gradle@v6` workflow 작성
  - 핵심 input — `cache-read-only` (feature 브랜치 read-only, main만 write), `dependency-graph: generate-and-submit` (Dependabot alert), `build-scan-publish: true`
  - Build Scan을 읽는 법 — task timeline, dependency conflict, Configuration Cache 통계
  - 통합 테스트를 분리 job으로 — matrix로 JDK 17/21 병렬
  - Native 이미지는 별도 job (15장 예고)
  - 마이그레이션 노트: 옛 `gradle-build-action`에서 `setup-gradle`로
- **이 챕터에서 자라는 앱 상태:** `ch14-ci/.github/workflows/build.yml` — PR마다 build + integrationTest + Build Scan publish.
- **예상 분량:** 김 (8,000자)

### Part V — 운영의 무게

#### 15장. GraalVM Native Image로 패키징한다
- **핵심 질문:** Spring Boot 앱을 native binary로 만들면 뭐가 변하고, 언제 그 비용을 지불할 가치가 있는가?
- **주요 내용:**
  - `org.graalvm.buildtools.native` 플러그인 적용 — `org.springframework.boot.aot`가 자동 적용
  - 자동 생성되는 `aot`/`aotTest` 소스셋, `processAot`/`processTestAot` task
  - `nativeCompile`이 `processAot` 출력을 사용 — reachability metadata와 `Spring-Boot-Native-Processed` 매니페스트
  - AOT만 단독 적용 (CDS 활용 등) — `apply(plugin = "org.springframework.boot.aot")`
  - `bootBuildImage`에 GraalVM Native plugin이 함께 있으면 native 이미지로 자동 빌드
  - 현실 — 빌드 시간 5~20분, 메모리 4~8GB. 개발자 로컬은 JVM 빌드 유지, CI에서 native는 별도 job (주기적 또는 release만)
  - **함정 박스 — Native 빌드 시간 완화 (레퍼런스 §15.6):** CI에서 native는 별도 job (PR마다가 아니라 nightly/release), 14장의 GitHub Actions matrix와 연결. `bootBuildImage` 캐시(buildpack layer cache)를 Volume으로 영속화. 메모리 OOM 시 `-J-Xmx8g` (리뷰 §1 반영)
  - 함정 박스: Reflection/Resource hint 누락 시 런타임 실패 — `runtime-hints-agent`로 trace 수집
- **이 챕터에서 자라는 앱 상태:** `ch15-native/` — `./gradlew nativeCompile` 또는 `bootBuildImage`로 native OCI 이미지 산출.
- **예상 분량:** 중간 (7,500자)

#### 16장. 의존성 보안 — Verification, Locking, Repository Content Filtering
- **핵심 질문:** Spring Boot의 transitive 수백~수천 개 의존성을 어떻게 신뢰할 수 있는가?
- **주요 내용:**
  - Dependency Verification — `./gradlew --write-verification-metadata sha256,pgp build` 부트스트랩
  - `gradle/verification-metadata.xml` 구조와 모드(strict/lenient/off)
  - Spring Boot 프로젝트 함정 — transitive 폭발로 수백~수천 줄, PR 리뷰가 어렵다, 일부 의존성은 PGP 서명 없음
  - Dependency Locking — `dependencyLocking { lockAllConfigurations(); lockMode = STRICT }`
  - `gradle.lockfile` 갱신 — `dependencies --write-locks`, 부분 갱신 `--update-locks 'org.springframework:*'`
  - Dependabot이 lockfile은 지원하지만 verification metadata는 아직 지원 안 함 → 운영 전략
  - Repository Content Filtering — `content { excludeGroup(...) }`, `includeGroup(...)`, `exclusiveContent {}` (메모: 레퍼런스 §17.3에 따라 공식 anchor URL은 챕터 저술 단계에서 재확인 필요)
  - 타입스쿼팅과 내부 의존성 누출 방지 — 회사 그룹은 내부 Nexus만, 그 외는 mavenCentral만
  - **함정 박스 — `./gradlew build --refresh-dependencies`:** 부분 갱신으로 오해하고 매번 사용하면 lockfile/verification metadata와 충돌. 정확한 갱신 도구는 `--write-locks` / `--write-verification-metadata` (리뷰 §6 반영)
  - 실전 가이드: CI는 strict, 부트스트랩/업데이트 PR은 lenient
- **이 챕터에서 자라는 앱 상태:** `ch16-security/` — `verification-metadata.xml` + `gradle.lockfile` + content filtering 모두 적용.
- **예상 분량:** 김 (8,500자) — verification + locking + content filtering 세 영역 + 함정 박스를 압축하지 않도록 1,000자 증가 (리뷰 §10 반영). content filtering의 일부는 8장(settings 수준 dependencyResolutionManagement)에서 미리 만나니, 본 챕터는 보안 관점에서 다시 본다.

#### 17장. Gradle 9.x로 옮긴다 — 마이그레이션 노트 모음
- **핵심 질문:** 회사의 Gradle 8.x (혹은 7.x) 빌드를 9.x로 올릴 때 무엇이 깨지고, 무엇을 먼저 점검하는가?
- **주요 내용:**
  - 9.0 메이저 변경점 정리 — Daemon JDK 17+ 필수, `jcenter()` 제거, `Project#exec`/`javaexec` 제거, Convention API 완전 제거, KGP 2.0+
  - Archive task의 기본 reproducible — 타임스탬프·파일 순서 의존 빌드 영향
  - JSpecify nullability + Kotlin 2.1 strict nullness
  - 9.1~9.4 incremental 변경 (Configuration Cache 호환성 + 진단 메시지 개선)
  - 9.5 신규 — Task provenance, Wrapper retries, precompiled Settings plugin type-safe accessor, `disallowChanges()`, `gradle init --into`, `--develocity-url`
  - 마이그레이션 step-by-step: wrapper 업그레이드 → 빌드 실패 메시지 읽기 → 가장 자주 깨지는 5가지 처방
  - third-party plugin 호환성 체크리스트 — Configuration Cache 호환 여부 확인
  - 본 책의 가상 앱 `shop`을 7.x 시절 빌드로 시작해서 9.5로 점진 마이그레이션하는 일지
  - **박스 — Spring Boot 3.x → 4.x는 6장에서:** Spring Boot 버전 마이그레이션은 6장에서 다뤘다. 본 챕터는 Gradle 버전 마이그레이션 — 두 마이그레이션의 역할 분담을 명시 (리뷰 §1·우선순위 §2 반영)
- **이 챕터에서 자라는 앱 상태:** 새 앱 상태 변화는 없다 — 회고. 다만 9.x로 옮기는 동안 깨지는 코드 예시들을 비교 박스로.
- **예상 분량:** 김 (8,000자)

#### 18장. 이제 어디로 갈 것인가
- **핵심 질문:** 이 책에서 다루지 않은 영역 중 당신 회사 빌드에 가장 먼저 적용할 만한 것은 무엇인가? (리뷰 §9 반영 — 안내문에서 의사결정형으로)
- **주요 내용:**
  - **1장 약속 회수 + 회고:** 책에서 다룬 18가지를 발자취로. 1장의 "build.gradle.kts를 어디까지 만질 수 있게 되는가" 질문에 답을 돌려준다 (리뷰 §10 반영)
  - **다음으로 도입할 만한 3가지 + 각각의 진입 비용 추정** (리뷰 §3·§10 반영, 7가지를 3가지로 좁힘):
    1. **Isolated Projects** — Configuration Cache의 후계. 프로젝트 간 격리를 통한 병렬 configuration. 9.x incubating, IDE sync 속도 개선의 답. 13장에서 만난 IDE sync 문제의 회수 (리뷰 §5 반영)
    2. **Develocity (구 Gradle Enterprise)** — 사내 Build Scan 호스팅, 원격 Build Cache, 테스트 분산(Predictive Test Selection). 진입 비용: 라이선스 + 운영 인력
    3. **GraalVM Native 운영 심화** — 15장에서 본 분량의 다음 단계. AOT hint 디버깅, profiling, GC 튜닝
  - **Out of Scope 회수:** Android Gradle Plugin, Kotlin Multiplatform, Tooling API는 §5 Out of Scope에서 이미 언급. 본 챕터에서는 한 줄씩 포인터만 (리뷰 §10 반영)
  - Gradle 커뮤니티에서 신호 따라가기 — release notes, Gradle Slack, Discuss 포럼, GitHub gradle/gradle 이슈
  - 빌드 도구가 곧 운영의 일부라는 1장의 약속을 다시 본다 — 클로징
- **이 챕터에서 자라는 앱 상태:** `shop` 앱의 마지막 모습 — 단일 의존성 한 줄에서 시작해서 멀티 모듈 + 커스텀 플러그인 + Configuration Cache + CI + Native + 보안까지.
- **예상 분량:** 중간 (5,500자) — 7가지에서 3가지로 좁혀 깊이 확보 (리뷰 §3·§10 반영)

---

## 5. 의도적으로 제외한 것 (Out of Scope)

독자 기대치 관리를 위해 명시한다:

1. **Android Gradle Plugin (AGP)** — 본 책은 백엔드 Spring Boot에 집중. AGP의 variant API, Library publishing, app/aar 등은 다루지 않는다. 마지막 18장에서 한 번 언급만.
2. **Kotlin Multiplatform 빌드** — KMP의 `commonMain`/`jvmMain` 등 multiplatform target 구성은 별도 책이 필요한 영역.
3. **Maven 사용법 자체** — Maven은 비교 박스(Part I·II)와 마이그레이션 다리 챕터(4장)에서만. Maven 입문은 다루지 않는다.
4. **Groovy DSL 사용법 자체** — 차이가 클 때만 `> Groovy DSL` 박스로 짧게 병기. Groovy DSL을 기본으로 쓰는 사람을 위한 책은 아니다.
5. **Gradle 8.x 이전의 deprecated API** — 17장 마이그레이션 노트에서 "이건 사라졌다"만 표기. 옛 API 사용법 자체는 안 다룬다.
6. **Java 외 JVM 언어 빌드** — Scala, Groovy 자체 빌드, Java + Kotlin 혼합 모듈 구성은 짧게만 (5장 toolchain 부근). Spring Boot 백엔드의 Kotlin 비중이 일반적이므로 KGP는 들어간다.
7. **Tooling API / IDE 플러그인 개발** — 18장에서 포인터만 남긴다. 책 본문에선 다루지 않는다.
8. **Bazel · Buck · Maven 등 다른 빌드 도구 비교** — Maven은 비교 박스로 들어가지만, 다른 빌드 도구는 다루지 않는다.
9. **Gradle Plugin Portal에 플러그인 발행하기** — 커스텀 플러그인은 12장에서 만들지만, 외부 발행 절차(라이선스, 메타데이터, signing)는 다루지 않는다. 사내 Maven 발행도 짧게만.
10. **Develocity 운영** — 18장에서 포인터만. 사내 Develocity 인스턴스 운영, Predictive Test Selection 튜닝 등은 별도 책 영역.

---

## 6. 리서치 한계 보강 권고 (작성자 메모)

레퍼런스 §17에 정리된 한계를 챕터별로 추적해두면 챕터 저술 단계에서 보강 리서치가 필요할 시점을 놓치지 않는다:

- **9장 (bootJar 함정):** 한국어 자료(우아한형제들·카카오 기술블로그) 직접 발굴 권장 — 실제 사고 사례가 챕터의 신뢰성을 올린다.
- **13장 (Configuration Cache):** 비호환 third-party plugin 사례 모음을 community-research로 1회 더 발굴 권장.
- **15장 (Native):** Spring Boot 팀 SpringOne 발표(Phil Webb / Andy Wilkinson) 영상 자료 보강 후보.
- **16장 (보안):** Repository Content Filtering 공식 anchor URL 재확인 필요.
- **17장 (마이그레이션):** Gradle 9.1~9.4 incremental 변경점은 release notes 직접 확인 단계에서 보강.

위 항목들은 챕터 저술 시 필요해지는 시점에 별도 리서치 pass를 돌린다.

---

## 7. 작성자 셀프 체크 — 설계 원칙 반영도

| 원칙 | 챕터 매핑 | 충족 여부 |
|---|---|---|
| A. 서사 축 — 앱이 자라는 이야기 | 4장 `ch04-bootapp/`부터 18장까지 `shop` 앱이 단계적으로 자라며 각 챕터에 "자라는 앱 상태" 표기 | ✔ |
| B. 9.5 기준을 본문에 녹임 | 9.5 신문법(Configuration Cache, lazy Property/Property, settings 수준 dependencyResolutionManagement, precompiled settings plugin accessor)을 1~14장 본문 표준으로. 9.0 이전 차이는 17장과 마이그레이션 노트 박스로 격리 | ✔ |
| C. 함정 우선 | 함정 박스를 전 챕터 (특히 9장 bootJar, 13장 Configuration Cache, 5장 BOM vs Catalog) 본문에 명시 | ✔ |
| D. 코드 신뢰성 | 모든 챕터에 `shop` 앱의 실제 동작 build.gradle.kts/settings.gradle.kts + 실행 결과 흐름 | ✔ |
| E. Maven 출신 보호 | Part I·II (1~7장) Maven 비교 박스 적극 활용, 4장 전체를 Maven → Gradle 1:1 매핑 다리로 할애 | ✔ |

---

## 8. 커버리지 체크리스트 매핑

| 영역 | 챕터 |
|---|---|
| 1. Gradle 기본 개념 (Project/Settings/Task/Plugin/Lifecycle) | 2장 |
| 2. Kotlin DSL 문법과 Groovy DSL 차이 | 3장 |
| 3. 가장 단순한 Spring Boot 단일 모듈 빌드 스크립트 | 4장 |
| 4. 의존성 관리 (configuration, BOM, java-platform, Spring Dependency Management, Version Catalog) | 5장 |
| 5. Spring Boot Gradle Plugin (bootJar, bootRun, bootBuildImage, layered) | 6장 |
| 6. 테스트 (test task, JVM Test Suites로 통합 테스트 분리) | 7장 |
| 7. 멀티 모듈 (settings, subprojects 안티패턴, Convention Plugin) | 8장 + 10장 |
| 8. buildSrc vs included build | 11장 |
| 9. Composite Build | 11장 |
| 10. 커스텀 플러그인 (Plugin, Task, Extension, Provider/Property) | 12장 |
| 11. Configuration Cache + Build Cache + Incremental | 13장 |
| 12. CI 통합 (Wrapper, setup-gradle, Build Scans) | 14장 |
| 13. GraalVM Native Image | 15장 |
| 14. 의존성 보안 (verification, locking, repository content filtering) | 16장 |
| 15. Gradle 9.x 변경점과 마이그레이션 | 17장 + 6장(Spring Boot 3.x → 4.x 분리) |

모든 영역이 챕터에 명확히 매핑된다.

### §15 실무 페인포인트 매핑 (리뷰 §1 반영)

레퍼런스 §15의 10개 페인포인트가 챕터에서 어디로 흡수되는지:

| 페인포인트 | 흡수 챕터 |
|---|---|
| §15.1 implementation vs api 구분 | 5장 박스 |
| §15.2 Maven dependencyManagement 매핑 | 4장 + 5장 |
| §15.3 Configuration Cache 비호환 plugin 대처 | 13장 본문 |
| §15.4 Version Catalog vs BOM vs ext | 5장 본문 (핵심 메시지) |
| §15.5 buildSrc는 죽었나 | 11장 본문 |
| §15.6 Native 빌드 시간 완화 | 15장 함정 박스 |
| §15.7 subprojects {} 안티패턴 | 10장 도입 |
| §15.8 library 모듈 bootJar 함정 | 9장 (챕터 전체) |
| §15.9 Gradle wrapper 버전 업그레이드 | 1장 박스 + 4장 + 14장 |
| §15.10 IDE sync 속도 | 13장 함정 박스 + 18장 Isolated Projects 회수 |

---

## Revision Log — Phase 3 Round 1 (1차 리뷰 반영)

이번 라운드에서 02_plan.md를 다음과 같이 갱신했다. 모든 변경은 챕터 내 박스/도입부/일부 내용 조정 수준이며, 18장 5부 골격은 유지.

1. **Top 3 Critical 처리**
   - **(1) 8장 → 9장 cliffhanger 연결:** 8장 마지막에 "정상 빌드가 안 된다 — 9장의 미스터리" 박스 추가, 8장의 자라는 앱 상태에 "정상 빌드가 아직 안 된다 — 9장의 함정에 걸려 있다" 명시. 9장 도입을 "8장 마지막의 실패 명령에서 시작"으로 자연스럽게 이음.
   - **(2) Spring Boot 3.x → 4.x 마이그레이션 약속:** 6장에 "Spring Boot 3.x → 4.x 옮길 때 무엇이 깨지는가" 섹션을 본문에 명시(핵심 질문에도 한 줄 추가). 17장은 Gradle 버전 마이그레이션, 6장은 Spring Boot 버전 마이그레이션으로 역할 분담을 17장에 박스로 회수.
   - **(3) Part IV 분량 분산:** 12장 9,500자 → 8,000자(Plugin Portal 발행 부분 축소, `shop.build-info` 한 예에 집중). 13장 9,500자 → 8,500자(Toolchain을 4장으로 이동). 4장에 Toolchain 박스 추가(7,500 → 8,500자). Plugin Portal 발행 제거 + Toolchain 4장 이전으로 Part IV 두 무거운 챕터 연속 배치 해소.

2. **그 외 리뷰 피드백 반영**
   - **3장:** lazy Property/Provider API를 빼고 박스 한 줄로만 언급, 본격적 깊이는 12장(리뷰 §4·우선순위 §4).
   - **1장:** Maven 출신 미끼 박스 + 8.x 사용자 안내 박스 + wrapper distribution-type 박스 3개 추가(리뷰 §7·§2·§11·우선순위 §5).
   - **5장:** implementation vs api 박스(§15.1), 의존성 그래프 디버깅 박스(dependencyInsight/dependencies/scan), Resolution Strategy 박스, dual-apply 함정 박스 추가. 본문 메시지는 "BOM은 resolution, Catalog는 declaration"으로 단순화(리뷰 §1·§4·§6).
   - **8장:** subprojects 경고를 박스 한 줄로 축소(두 장 연속 cliffhanger 회피). 9장과의 자연스러운 연결로 대체(리뷰 §2).
   - **9장:** 핵심 질문을 액션 지향형으로 좁힘. 5분 진단 체크리스트 박스 + 실제 사고 회고 박스(한국어 자료 발굴 필요) 추가로 9,000자 콘텐츠 밀도 확보(리뷰 §3·§9).
   - **10장:** "왜 여기서 갑자기 string?" 박스 추가 — convention plugin의 string-receiver 정면 해소(리뷰 §8).
   - **11장:** Composite Build의 co-development 부분 축소, build-logic 분리에 집중. 8,000자 → 7,000자(리뷰 §4).
   - **12장:** outputs.upToDateWhen{false} 함정 박스, Project vs system vs ext property 박스 추가(리뷰 §6·§11).
   - **13장:** IDE sync 함정 박스(§15.10) + 18장 Isolated Projects 회수 약속, gradle.properties 표준 키 정리 표 추가(리뷰 §1·§5·§11).
   - **15장:** Native 빌드 시간 완화 함정 박스(§15.6) 추가(리뷰 §1).
   - **16장:** `--refresh-dependencies` 함정 박스 추가, 분량 7,500 → 8,500자로 압축 해소(리뷰 §6·§10).
   - **18장:** 핵심 질문을 의사결정형으로 좁힘, 안내 7가지를 "다음으로 도입할 만한 3가지 + 진입 비용"으로 좁힘. AGP/KMP는 Out of Scope 회수만(리뷰 §3·§9·§10).
   - **제목 표지:** 부제 단축안 적용 — `빌드를 다시 짠다 — Spring Boot × Gradle 9.5 × Kotlin DSL 실전 가이드`(리뷰 §12).
   - **logline:** 한 호흡 두 문장으로 단축(리뷰 §13).
   - **§8 커버리지 표:** §15 실무 페인포인트 10개 매핑 표 추가(리뷰 §1).

3. **동의하지 않거나 본문에 이미 흡수된 사항 — 별도 처리 없음**
   - 리뷰 §3 18장 분량 5,500자 유지 — 7가지를 3가지로 좁히면서 깊이를 채우는 방향으로 처리. 분량은 그대로.
   - 리뷰 §2의 "17장을 0장처럼 옮기는 검토" 옵션 — 본문 흐름상 17장 현 위치가 자연스럽다는 리뷰어의 결론에 동의. 1장 박스로 미리보기만 추가.
   - 리뷰 §4의 5장 분량 8,500자 — declarable 5개를 박스로 격리하면서 의존성 디버깅 + resolution strategy + dual-apply 함정 박스가 추가되어 결과적으로 9,000자로 소폭 증가. 메시지는 "BOM/Catalog 직교"로 단순화한 점은 반영.

이 라운드의 모든 변경은 챕터 재배열 없이 챕터 내 박스/도입부/일부 분량 조정으로 처리. 다음 단계(챕터 저술) 진입 준비 완료.
