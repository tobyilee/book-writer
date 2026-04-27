# Kotlin 2.0 ~ 2.3 변경점 안내 — 통합 레퍼런스

이 문서는 책 *"Kotlin 2.0 ~ 2.3 변경점 안내서"* 저술을 위한 1차 자료다. JetBrains 공식 What's new (2.0 / 2.0.20 / 2.1 / 2.1.20 / 2.2 / 2.2.20 / 2.3), Kotlin blog, KEEP 제안서, KotlinConf 2024, 그리고 한국·영문 커뮤니티 사례를 교차 검증해 정리했다. 각 섹션의 사실에는 대괄호로 출처를 표기했고, 코드 스니펫은 가능한 한 원문을 그대로 옮겼다.

대상 독자는 Kotlin 1.9까지를 실무에서 써왔지만 2.x로의 변화를 따라가지 못한 백엔드/안드로이드/시니어 개발자, 그리고 KMP·Compose Multiplatform 사용자다.

---

## 1. 핵심 개념 정의

본서 전반에서 자주 등장하는 용어를 먼저 정리한다.

- **K1 / K2 컴파일러** — Kotlin의 컴파일러 프론트엔드 세대. K1은 1.0~1.9까지 이어진 기존 구현이고, K2는 Kotlin 2.0에서 모든 타깃(JVM/Native/Wasm/JS)의 기본 프론트엔드로 정식 승격된 새 구현이다. "rewritten from scratch and multiplatform from the ground up, more performant, and safe to migrate" 라는 표현이 KotlinConf 2024 키노트에서 사용됐다 [KotlinConf 2024 Roundup, JetBrains Blog].

- **FIR (Frontend Intermediate Representation)** — K2의 핵심 자료구조. K1은 PSI(IntelliJ 트리)와 BindingContext에 의존했지만, K2는 컴파일러 프론트엔드가 단일 FIR만 만들도록 재설계됐다. velog의 한 한국어 정리는 K2를 "FIR(Frontend Intermediate Representation) 데이터 구조만 형성하도록 컴파일러 프론트엔드를 재설계해 성능을 개선" 했다고 요약한다 [velog @lifeisbeautiful].

- **KEEP (Kotlin Evolution and Enhancement Process)** — 언어/표준 라이브러리 변경 제안서를 모아둔 GitHub 저장소(`Kotlin/KEEP`). 이 책에서 자주 등장하는 KEEP은 #259 (context receivers, 폐기 예정), #367 (context parameters, 후속), KEEP-2425 (multi-dollar interpolation), KEEP-1436 (non-local break/continue), KEEP-71140 (guard conditions in `when`)이다 [Kotlinlang docs].

- **`-language-version` / `-api-version`** — 컴파일러 플래그. 전자는 어떤 버전의 언어 문법/시맨틱을 사용할지, 후자는 어떤 버전까지의 표준 라이브러리 API를 허용할지 제어한다. K2(2.0)는 `-language-version=1.9`로 K1 시절 동작으로 롤백할 수 있게 해 점진적 이행을 지원한다 [K2 compiler migration guide].

- **kapt / KSP / KSP2** — 자바 어노테이션 프로세서를 끌어안는 kapt, Kotlin 전용 심볼 프로세서 KSP, 그리고 K2 위에서 다시 구현된 KSP2. JetBrains는 마이그레이션 시 가능한 한 kapt → KSP로 옮기길 권장한다. K2 KAPT는 2.1.0에서 alpha, 2.1.20에서 기본값이 됐고, 2.2.20에 들어서면서 `kapt.use.k2` 프로퍼티 자체가 deprecated 됐다 (K2 KAPT가 사실상 표준) [whatsnew21, whatsnew2120, whatsnew2220].

- **Compose compiler plugin** — Kotlin 2.0 이후 Jetpack Compose / Compose Multiplatform 컴파일러는 Kotlin 저장소로 이관되어 `org.jetbrains.kotlin.plugin.compose` Gradle 플러그인으로 이름이 바뀌었고, Kotlin 버전과 동일한 버전으로 함께 릴리스된다 [Android Developers Blog, 2024-04; Compose compiler migration guide].

- **stability tier** — JetBrains는 컴포넌트 안정도를 Stable / Beta / Alpha / Experimental로 구분한다. KMP는 1.9.20부터 Stable이고, Wasm 타깃은 2.2.20에서 Beta로 승격됐다 [components-stability.html].

---

## 2. 버전별 What's New 요약

각 버전 항목은 (정식) / (Preview·Beta) / (Experimental)로 안정성을 표기한다. 모든 항목은 JetBrains 공식 What's new 문서를 기준으로 한다 [whatsnew20, whatsnew2020, whatsnew21, whatsnew2120, whatsnew22, whatsnew2220, whatsnew23].

### 2.1 Kotlin 2.0.0 (2024-05-21)

**핵심 메시지:** "Kotlin 2.0 was released with a stable K2 compiler, which is multiplatform from the ground up, understands your code better, and compiles it twice as fast." [Celebrating Kotlin 2.0, JetBrains Blog].

#### 정식 (Stable)

- **K2 컴파일러 기본 활성** — JVM/Native/Wasm/JS 모든 타깃에서 K2가 디폴트. JetBrains 발표 기준 "10 million lines of code … 18,000 developers … 80,000 projects" 규모로 안정화 검증을 거쳤다 [whatsnew20].
- **smart cast 대폭 확장** — `if (isCat) animal.purr()` 처럼 *분리된 `Boolean` 변수* 안으로 캐스트가 전파된다. logical OR, inline lambda 안의 변경 가능 변수, 함수 타입 프로퍼티, `try`/`catch`/`finally` 블록, 증감 연산 등 7가지 시나리오에서 새로 동작 [whatsnew20].
- **Compose 컴파일러 통합** — `kotlin("plugin.compose") version "2.0.0"`으로 Gradle 플러그인이 바뀜. "The Jetpack Compose compiler … has been merged into the Kotlin repository and will now ship with Kotlin" [Android Developers Blog].
- **`enumEntries<T>()`** — 기존 `enumValues<T>()` 대체. 매번 새 배열을 만들지 않아 더 효율적.
- **lambda → invokedynamic 기본 변환** — 바이너리 크기 축소. 다만 *Serializable* 람다나 `reflect()` API에는 영향이 있어 `@JvmSerializableLambda`나 `-Xlambdas=class`로 회귀 가능 [whatsnew20].
- **Multiplatform** — common ↔ platform 소스의 엄격한 분리, expected/actual에서 *actual*이 더 넓은 가시성 허용 (`expect internal class … actual class …`).
- **Kotlin/Native** — Xcode Instruments 기반 GC 시그널, `@ObjCSignatureOverride`.
- **Kotlin/Wasm** — Binaryen 기본 적용, Named exports, JS 예외 try/catch.
- **Kotlin/JS** — ES2015 컴파일 타깃, per-file 컴파일, npm 매니저 직접 사용 옵션 (`kotlin.js.yarn=false`).
- **build 산출물 디렉터리 변경** — `<project-root>/.kotlin` (이전 `.gradle/kotlin`).

#### Experimental

- `kotlin("plugin.power-assert")` — 테스트 실패 시 부분식 값을 함께 보여주는 플러그인.
- `js-plain-objects` 플러그인 — `@JsPlainObject`로 type-safe JS 객체 생성과 `.copy()` 지원.
- TypeScript 선언 자동 생성 (`generateTypeScriptDefinitions()`).

#### 빠르게 알아야 할 K2 한계

- Gradle 8.3 이전에서는 buildSrc 의존이 있는 프로젝트가 깨질 수 있고, 회피책은 `-language-version=1.9` 또는 Gradle 8.3+ 업그레이드 [whatsnew20].

### 2.2 Kotlin 2.0.20 (2024-08-22)

- **data class `copy()` 가시성 일치** (점진 변경) — 향후 `copy()`가 생성자 가시성을 따른다. 즉시 컴플라이언스 원하면 `@ConsistentCopyVisibility`, 경고 무시하려면 `@ExposedCopyVisibility`. 컴파일러 옵션 `-Xconsistent-data-class-copy-visibility` [whatsnew2020].
- **context receivers 명시적 deprecate 시작** — 2.0.20부터 `-Xcontext-receivers` 사용 시 경고. 2.3에서 제거 예정 [whatsnew2020, JetBrains Blog 2025-04].
- **Compose 컴파일러 기본값 변경** — Strong Skipping Mode가 기본 활성, `includeTraceMarkers=true` 기본 활성, 추상 `@Composable`에 기본값 파라미터 허용 [whatsnew2020].
- **Native concurrent GC** (Experimental) — `kotlin.native.binary.gc=cms`.
- **Wasm** — default export 사용은 이제 *에러*. `import { … } from "module"` 강제. `ExperimentalWasmDsl` 패키지 이동.
- **stdlib UUID API** (Experimental) — `Uuid.fromByteArray`, `fromULongs`, `parse`, `random()`, `toJavaUuid()`/`toKotlinUuid()`.
- **Base64 padding 옵션** — `withPadding(Base64.PaddingOption.PRESENT_OPTIONAL)` 등 4가지.

### 2.3 Kotlin 2.1.0 (2024-11-27)

JetBrains 표현으로 "language features that improve expressivity" 가 키워드. 모두 Preview / opt-in 상태로 도입돼 2.2.0에서 Stable 승격된다 [whatsnew21].

#### Preview (전부 컴파일러 플래그 필요)

- **`when`의 guard 조건** — `is Animal.Cat if !animal.mouseHunter -> …` 형식. opt-in: `-Xwhen-guards`. KEEP-71140.
- **Multi-dollar interpolation** — `$$"""..."""`로 단일 `$`를 리터럴로 보존. JSON 스키마, Bash heredoc 작성 시 유용. opt-in: `-Xmulti-dollar-interpolation`. KEEP-2425.
- **inline lambda에서의 non-local `break`/`continue`** — `for (e in xs) { val v = e.foo() ?: continue }` 가 람다 안에서도 동작. opt-in: `-Xnon-local-break-continue`. KEEP-1436.

#### Alpha → 향후 Stable로

- **K2 KAPT** — 본격적으로 K1과 동등한 성능에 도달. opt-in: `kapt.use.k2=true` (기본값은 아직 `false`).

#### Stable

- **`extraWarnings.set(true)`** — `REDUNDANT_NULLABLE`, `CAN_BE_VAL`, `UNREACHABLE_CODE` 등 추가 경고 묶음 활성화.
- **`@SubclassOptInRequired`** — 라이브러리 작성자가 *상속* 시점에만 opt-in을 강제할 수 있는 새 어노테이션.
- **sealed class exhaustiveness 개선** — `else` 없이도 모든 케이스를 명시한 `when`이 통과 [whatsnew21]. 한 한국어 후기는 *"왜 이걸 2.1.0에 되서야 지원해 주지"* 라며 늦은 도입을 아쉬워한다 [velog @cksgodl].

### 2.4 Kotlin 2.1.20 (2025-03-20)

- **K2 KAPT 기본값화** — `kapt.use.k2=true`가 디폴트. K1으로 되돌리려면 `kapt.use.k2=false` [whatsnew2120].
- **`kotlin.concurrent.atomics`** (Experimental) — `AtomicInt`, `AtomicLong`, `AtomicBoolean`, `AtomicReference` 같은 멀티플랫폼 atomic. JVM 측 `java.util.concurrent.atomic`과는 `asJavaAtomic()` / `asKotlinAtomic()`으로 양방향 변환.
- **`kotlin.time.Clock` & `kotlin.time.Instant`** (Experimental) — `kotlinx-datetime`에서 표준 라이브러리로 이주. `Clock.System.now()`, `Instant.parse(...)`. 이후 2.3에서 Stable 승격.
- **UUID 강화** — `parseHexDash()`, `toHexDashString()`, `Uuid : Comparable<Uuid>`.
- **Multiplatform `executable {}` DSL** — Gradle 8.7부터 충돌하는 Application 플러그인을 대체.
- **Lombok plugin** — `@SuperBuilder`, 생성자에 `@Builder` 지원.
- `withJava()` deprecated, `kotlin-android-extensions` 플러그인 *configuration error*.

### 2.5 Kotlin 2.2.0 (2025-06)

이 버전부터 *Preview 졸업분*이 한꺼번에 들어온다. JetBrains 표현으로 "developer experience matures" 시점.

#### Stable (정식 승격)

- **`when`의 guard 조건** (2.1 Preview → 2.2 Stable).
- **non-local `break`/`continue`** (2.1 Preview → 2.2 Stable).
- **multi-dollar interpolation** (2.1 Preview → 2.2 Stable).
- **Base64 API** — `Base64.Default`, `Base64.UrlSafe`, `Base64.Mime`, `Base64.Pem`. JVM에서는 `OutputStream.encodingWith(Base64.Default)` 같은 스트림 연동.
- **HexFormat API** — `93.toHexString()` → `"5d"`. minLength, removeLeadingZeros 등 세밀한 옵션.
- **JVM default method 기본 생성** — 인터페이스 함수가 JVM `default` 메서드로 컴파일됨. `JvmDefaultMode.NO_COMPATIBILITY`도 선택 가능.

#### Preview (opt-in)

- **context parameters (KEEP-367)** — context receivers의 후속. `context(users: UserService) fun outputMessage(message: String) { users.log(...) }`. opt-in: `-Xcontext-parameters`.
- **context-sensitive resolution** — `enum class Problem { CONNECTION, ... }` 일 때 `when (problem) { CONNECTION -> ... }` 처럼 enum 이름 prefix 생략 가능. opt-in: `-Xcontext-sensitive-resolution`.
- **`@all` 메타 타깃** — `@all:Email`로 param/property/field/get/setparam에 한 번에 적용. opt-in: `-Xannotation-target-all`.

#### Beta

- **nested type aliases** — `class Dijkstra { typealias VisitedNodes = Set<Node>; ... }`. opt-in: `-Xnested-type-aliases`. (2.3에서 Stable.)

#### Experimental

- **annotations in Kotlin metadata** — `KotlinClassMetadata`로 어노테이션을 읽는다. opt-in: `-Xannotations-in-metadata`.
- **`@JvmExposeBoxed`** — value class를 Java에서 쓸 수 있게 boxed variant 노출.
- **`-Xwarning-level=DIAGNOSTIC_NAME:(error|warning|disabled)`** — 진단별로 레벨을 지정.
- **Native Latin-1 strings** — `kotlin.native.binary.latin1Strings=true`로 ASCII 위주 문자열 메모리 절반.
- **KGP Binary Compatibility Validation** — `abiValidation { … }` + `./gradlew checkLegacyAbi`.

#### 주요 *Breaking Changes* (2.2.0)

- `-language-version=1.6 / 1.7` 지원 종료 (최소 1.8) [whatsnew22].
- `kotlinOptions { … }`가 *컴파일 에러*. 반드시 `compilerOptions { … }`로 마이그레이션.
- Ant 빌드 시스템, REPL, JSR-223이 deprecate 또는 opt-in 전용으로 격하.
- `kotlin-android-extensions` 플러그인 제거 → `kotlin-parcelize` + view bindings.
- `KotlinCompilation.source` 제거.

### 2.6 Kotlin 2.2.20 (2025-09-10)

2.3에서 정식이 될 기능들의 Preview가 본격적으로 시작되는 분기점.

- **data-flow exhaustiveness for `when`** (Experimental) — `if (role == ADMIN) return 99 ; when (role) { MEMBER -> ... ; GUEST -> ... }` 처럼 *앞 흐름*을 인지해 `else` 없이도 컴파일. opt-in: `-Xdata-flow-based-exhaustiveness`.
- **expression body의 `return` 허용** (Beta) — `fun f(id: String?): String = g(id ?: return "default")`. 명시적 반환 타입 필요.
- **suspend function type 오버로드 해소** — `transform({ 42 })` vs `transform(suspend { 42 })`.
- **catch 블록의 reified 제네릭** — `inline fun <reified E : Throwable> handle(...)`.
- **Kotlin/Wasm Beta로 승격** — Wasm 타깃 자체가 Beta 안정도 [components-stability].
- **공통 의존성 선언 방식 (Experimental)** — `kotlin { dependencies { implementation(...) } }` (top-level).
- **Swift Export 기본 활성** (Experimental) — Kotlin → Swift 직접 매핑, Objective-C 헤더 우회.
- **`webMain` / `webTest` 자동 생성** — `js()` + `wasmJs()` 공통 코드 작성용.
- **K/N 크로스 컴파일** — Mac이 아닌 호스트에서도 모든 플랫폼 .klib 빌드 가능 (cinterop·CocoaPods·최종 바이너리 제외).
- **`kapt.use.k2` 프로퍼티 deprecated** (K2 KAPT가 사실상 유일).
- **Kotlin/Native 레거시 `kotlin-native.jar` 제거**, x86_64 Apple 타깃을 tier 2로 강등.

### 2.7 Kotlin 2.3.0 (2025-12-16)

이 책 시점의 최신 정식 릴리스. JetBrains는 2.3을 "stable + ergonomics" 위주로 묘사한다 [whatsnew23].

#### Stable

- **nested type aliases** (Preview에서 Stable).
- **data-flow 기반 `when` exhaustiveness**.
- **expression body의 `return` 기본 활성**.
- **`kotlin.time.Clock` / `Instant`**.
- **JS — Unified companion access** (`Foo.Companion.bar()`), `@JsStatic in interfaces`, `@JsQualifier` per-declaration, `@JsExport.Default`.
- **Wasm — KClass.qualifiedName 기본 활성**, **Latin-1 압축 저장 기본 활성** (Wasm 바이너리 최대 13% 축소).
- **Kotlin/JVM — Java 25 바이트코드 지원**.
- **Kotlin/Native — 향상된 Swift Export**: enum이 진짜 Swift enum으로, variadic 인자 매핑. `linkRelease*` 빌드 최대 40% 향상.
- **Compose stack trace mapping** — R8 minify 환경에서 Compose 그룹 키와 ProGuard 매핑 결합. 활성 코드: `Composer.setDiagnosticStackTraceMode(ComposeStackTraceMode.GroupKeys)`. Jetpack Compose runtime ≥1.10 필요.

#### Experimental

- **Unused Return Value Checker** — `-Xreturn-value-checker=check`. `@MustUseReturnValues` 또는 파일 단위 `@file:MustUseReturnValues`로 적용. 의도적으로 무시할 때는 `val _ = computeValue()` 관용.
- **Explicit backing fields** — 새 `field = …` 문법으로 `_city ; city: StateFlow ...` 패턴 대체. opt-in: `-Xexplicit-backing-fields`.
- **UUID v7 / v4 명시 생성** — `Uuid.generateV4()`, `Uuid.generateV7()`, `Uuid.generateV7NonMonotonicAt(instant)`, `Uuid.parseOrNull("…")`, `Uuid.parseHexDashOrNull(…)`.
- **JS — Suspend function export to JS** (`@JsExport` + suspend), `BigInt64Array`로 `LongArray` 표현 (`-Xes-long-as-bigint`).

#### Breaking Changes (2.3)

- `-language-version=1.8` 지원 종료. `1.9`는 non-JVM 타깃에서 미지원.
- Android Multiplatform — Google `com.android.kotlin.multiplatform.library` 플러그인으로 마이그레이션 권장. AGP 9.0.0 이후 `org.jetbrains.kotlin.android` 플러그인 자체가 불필요.
- Apple 최소 OS 상향: iOS/tvOS 12 → 14, watchOS 5 → 7. macosX64/iosX64/tvosX64/watchosX64는 support tier 3, **Kotlin 2.4에서 제거 예정**.
- Ant 빌드 시스템 완전 제거.

---

## 3. Kotlin 1.9 vs 2.x 핵심 차이 (한눈에)

| 영역 | Kotlin 1.9 | Kotlin 2.0 ~ 2.3 | 출처 |
|---|---|---|---|
| 컴파일러 프론트엔드 | K1 (PSI + BindingContext) 기본 | K2 / FIR 기본. 평균 컴파일 속도 ~2배 (clean build 기준). | [whatsnew20], [Celebrating Kotlin 2.0] |
| 빌드 산출 디렉터리 | `.gradle/kotlin/` | `.kotlin/` (gitignore 추가 권장) | [whatsnew20] |
| Compose 컴파일러 | `androidx.compose.compiler:compiler` (별도 버전) + `composeOptions { kotlinCompilerExtensionVersion = ... }` | `kotlin("plugin.compose") version <kotlin-version>` (Kotlin과 동일 버전, `composeCompiler { ... }` 블록) | [Compose compiler migration guide], [Android Dev Blog] |
| 람다 → 바이트코드 | 익명 클래스 (Serializable 가능) | invokedynamic 기본 (Serializable 깨질 수 있음, `@JvmSerializableLambda` 또는 `-Xlambdas=class`) | [whatsnew20], [DigitalFrontiers Medium] |
| smart cast 범위 | `if (x is Foo) x.bar()` 정도 | `val isFoo = x is Foo; if (isFoo) x.bar()` 도 통과. inline lambda, `try/catch/finally`, OR 연산자, 함수 타입 프로퍼티에서 확장 | [whatsnew20] |
| `when` exhaustiveness | sealed에서도 `else` 권장 | `else` 없이 통과. 2.2.20부터 data-flow 기반 (앞 분기 고려). 2.3에서 Stable. | [whatsnew21], [whatsnew2220], [whatsnew23] |
| `when` 가드 | 없음 (`is X && cond` 사용) | `is X if cond -> …` (2.2 Stable) | [whatsnew22] |
| 비지역 break/continue | 람다 안에서 불가 | 2.1 Preview → 2.2 Stable | [whatsnew21], [whatsnew22] |
| 문자열 보간 | `"$x"` / `"\$x"`로 escape | `$$"""..."""`로 dollar 단위 제어 (2.2 Stable) | [whatsnew22] |
| `kotlinOptions { jvmTarget = "17" }` | 사용 가능 (deprecated 경고) | **2.2부터 컴파일 에러**. `compilerOptions { jvmTarget.set(JvmTarget.JVM_17) }` 필수 | [whatsnew22], [Medium @l2hyunwoo] |
| context receivers | Experimental (`-Xcontext-receivers`) | Deprecated 시작 (2.0.20). 2.3 무렵 제거. 후속은 **context parameters** (2.2 Preview / `-Xcontext-parameters`) | [JetBrains Blog 2025-04], [KEEP-367] |
| `enumValues<T>()` | 매 호출마다 새 배열 | `enumEntries<T>()` (Stable, 같은 `EnumEntries` 반환) | [whatsnew20] |
| Base64 / HexFormat | 직접 구현 또는 `java.util.Base64` | `kotlin.io.encoding.Base64` 4 종, `Int.toHexString()` (2.2 Stable) | [whatsnew22] |
| UUID | `java.util.UUID` 직접 사용 | `kotlin.uuid.Uuid` (2.0.20 Experimental → 2.3까지 점진 강화) | [whatsnew2020], [whatsnew23] |
| `kotlin.time.Clock` / `Instant` | `kotlinx-datetime`에 의존 | 표준 라이브러리에 편입 (2.3 Stable) | [whatsnew23] |
| KMP (Kotlin Multiplatform) | 1.9.20에서 Stable | Stable. iOS 최소 14, watchOS 최소 7 (2.3). x64 Apple 타깃 곧 제거. Wasm 2.2.20에서 Beta. | [components-stability], [multiplatform-compatibility-guide] |
| KAPT | K1 기반 | 2.1 alpha → 2.1.20 기본 → 2.2.20에서 `kapt.use.k2` 자체가 deprecated | [whatsnew21], [whatsnew2120], [whatsnew2220] |
| Apple/iOS framework 캐싱 | 정상 | 1.9.2x ↔ 2.0.0 사이 버전 변경 시 Xcode 캐시가 stale → `./gradlew clean` + Xcode Clean Build 필요 | [multiplatform-compatibility-guide] |
| `kotlin-android-extensions` | deprecated | **제거** (2.2). `kotlin-parcelize` + view binding | [whatsnew22] |

위 표 자체를 책 도입부의 "1페이지 요약"으로 활용할 수 있다.

---

## 4. K2 컴파일러 — 아키텍처와 성능

### 4.1 아키텍처: K1 → K2 (FIR)

K1은 IntelliJ의 PSI 트리를 그대로 컴파일러 프론트엔드의 1차 시맨틱 자료구조로 사용했다. 결과적으로 (i) IDE와 컴파일러가 같은 트리를 다른 방식으로 해석하고, (ii) 멀티플랫폼 일관성이 부족하며, (iii) 새 언어 기능이 *모든 백엔드*에 들어가는 데 비용이 큰 구조였다 [The K2 Compiler Is Going Stable, JetBrains Blog 2023-02].

K2는 컴파일러 프론트엔드를 *FIR (Frontend Intermediate Representation)* 단일 자료구조로 새로 짜고, IR 백엔드와의 인터페이스를 명확히 분리했다. KotlinConf 2024에서 Michail Zarečenskij는 K2를 "rewritten from scratch and multiplatform from the ground up" 으로 표현했고, 발표 자료 PDF는 `Kotlin Language Features in 2.0 and Beyond`로 공개돼 있다 [resources.jetbrains.com KotlinConf 2024].

velog의 한국어 정리는 K2를 "FIR(Frontend Intermediate Representation) 데이터 구조만 형성하도록 컴파일러 프론트엔드를 재설계해 JVM/JS/wasm/Native 모두에서 성능을 개선" 했다고 풀이한다 [velog @lifeisbeautiful].

### 4.2 안정화 검증 규모

- "10 million lines of code from selected user and internal projects."
- "18,000 developers were involved in the stabilization process, testing the new K2 compiler across a total of 80,000 projects." [whatsnew20]

### 4.3 컴파일 속도 벤치마크

JetBrains 공식 벤치마크 [Kotlin Blog 2024-04, "K2 Compiler Performance Benchmarks and How to Measure Them on Your Projects"]:

| 시나리오 | 프로젝트 | K1 (1.9.23) | K2 (2.0.0) | 상승률 |
|---|---|---|---|---|
| Clean build | Anki-Android | 57.7 s | 29.7 s | **94% 빠름** |
| Clean build | Exposed | 5.8 s | 3.22 s | 80% 빠름 |
| Incremental (ABI 변경) | Anki-Android | — | — | 275% 빠름 |
| Incremental (ABI 미변경) | Exposed | — | — | 7% 빠름 |
| 초기화 단계 | Anki-Android | 0.126 s | 0.022 s | 488% 빠름 |
| 분석 단계 | Anki-Android | 0.581 s | 0.122 s | 376% 빠름 |

JetBrains의 헤드라인 표현은 다음과 같다.

> "The K2 compiler brings up to 94% compilation speed gains."
> "Gradle build speeds were consistently higher by at least 9%."
> [Kotlin Blog 2024-04]

또한 IDE 측은 "around 1.8 times faster code highlighting and a 1.5 completion speed increase" 라고 발표됐고, IntelliJ IDEA 2025.1부터는 K2 모드가 *기본값*이다 [Celebrating Kotlin 2.0; Java Code Geeks 2026 review].

### 4.4 현장 측정과 *상충 관점* (관점 A vs 관점 B)

**관점 A — JetBrains / 일부 사용자: 체감 가능한 가속.**
독일 DigitalFrontiers의 Benedikt Jerat는 두 서비스에서 다음을 측정했다 [Migrating to Kotlin 2.0 — A slightly bumpy journey, Medium]:

| | `compileKotlin` | `compileTestKotlin` |
|---|---|---|
| Service 1 | 14,586 ms → 9,624 ms (34%↓) | 36,263 ms → 13,400 ms (63%↓) |
| Service 2 | 47,496 ms → 21,529 ms (55%↓) | 124,267 ms → 33,881 ms (73%↓) |

저자의 결론: *"The switch from Kotlin 1 to Kotlin 2 went surprisingly smooth. … nothing that felt like a show-stopper."*

**관점 B — Slack 엔지니어 Zac Sweers: 프로젝트마다 다르며, 회귀 사례 존재.**
"Contrary to advertised 2x+ gains, real-world results vary significantly. Sweers measured `a ~17% slowdown` on Slack's codebase while observing improvements elsewhere. His recommendation: `I would highly recommend doing your own measurements`." [zacsweers.dev / preparing-for-k2]

이 책에서는 두 관점을 병기하고, 독자에게 *자신의 프로젝트에서 직접 벤치마크*할 것을 권하는 톤이 적절하다.

### 4.5 K2가 새로 거르는 컴파일 에러 패턴

[K2 compiler migration guide] 정리:

1. **Open property는 즉시 초기화 필요.**
   ```kotlin
   open class Base {
       open val a: Int    // ERROR: open val must have initializer
       init { this.a = 1 }
   }
   ```
   해결: `open val a: Int = 1`로 즉시 초기화하거나 final로 변경.

2. **별도 변수로 추출된 `is` 체크의 smart cast.** K1은 unresolved reference 에러 → K2는 통과 (개선).

3. **Star-projected receiver의 synthetic setter** — `starProjected.foo = sampleString`이 2.0부터 에러.

4. **부적절한 모듈 의존으로 generic 타입에 접근 불가** — "the type of the implicit lambda parameter (it) resolves to Node, which is inaccessible." 해결: 모듈 의존 그래프 점검.

5. **`expect`/`actual` open 클래스에 abstract 멤버** — K2는 `expect override fun listFiles()` 같은 명시적 override 요구.

6. **Java `int @Nullable []` 처리 강화** — `dataService.fetchData()[0]`이 K1은 통과했으나 K2는 nullable 인지로 에러. 해결: `?.get(0)`.

7. **Kotlin property vs Java field 우선순위 일관화** — K1은 케이스에 따라 super의 Java field 또는 derived의 Kotlin property로 갈렸다. K2는 *항상* derived 우선.

추가로 흔히 부딪히는 사례 [Migrating to Kotlin 2.0, DigitalFrontiers Medium]:

8. **JUnit 5 `@Nested` + 백틱 한국어/긴 메서드 이름** — K2가 람다를 `$lambda$30` 등으로 명명하면서 파일 시스템 경로 한도를 초과해 `FileNotFoundException: The system cannot find the file specified`. 해결: 메서드명 단축 또는 nested depth 축소.

9. **이벤트 소싱(CQRS/ES)의 람다 직렬화** — invokedynamic 기본 변환으로 *"Illegal state change detected! Property has different value when sourcing events"* 발생. 해결: 직렬화 필요한 람다에 `@JvmSerializableLambda` 또는 모듈에 `-Xlambdas=class`.

10. **Anvil 등 컴파일러 IR 백엔드에 의존하는 플러그인** — Sweers: *"it will no longer run the compiler IR backend during stub generation, so any compiler plugins that depend on that (i.e. Anvil) will require changes."*

### 4.6 Gradle / Maven 플래그 변화

- 기본 활성: Kotlin 버전을 2.0+로 올리면 K2 사용.
- K1로 롤백: `-language-version=1.9` (또는 KGP `compilerOptions { languageVersion.set(KotlinVersion.KOTLIN_1_9) }`).
- 빌드 리포트: `kotlin.build.report.output=file | single_file | json | http | build_scan` [K2 compiler migration guide].
- `kotlin.experimental.tryNext=true` — 다음 버전 언어 레벨 미리보기 (2.0에서 2.1을 시도하는 식).

---

## 5. 언어 기능 자세히 — 코드와 함께

### 5.1 data objects (2.0 Stable)

`data object`는 1.9 베타에서 2.0 Stable로 승격됐다. `toString()`, `equals()`, `hashCode()`가 *클래스 이름 단위*로 합리적으로 정의된 sealed hierarchy의 종착 케이스 표현에 적합하다.

```kotlin
sealed class ReadResult {
    data class Number(val number: Int) : ReadResult()
    data class Text(val text: String) : ReadResult()
    data object EndOfFile : ReadResult()
}

println(ReadResult.EndOfFile) // "EndOfFile" (object의 hex hash 대신)
```

### 5.2 smart cast — 7 가지 새 시나리오 (2.0)

[whatsnew20]에서 직접 인용한 코드.

```kotlin
// 1) 분리된 Boolean
fun petAnimal(animal: Any) {
    val isCat = animal is Cat
    if (isCat) animal.purr()    // 2.0에서 OK
}

// 2) OR로 묶인 type check → 공통 supertype 으로 캐스트
fun signalCheck(s: Any) {
    if (s is Postponed || s is Declined) s.signal()  // Status로 cast
}

// 3) inline 함수 안의 callsInPlace
inline fun inlineAction(f: () -> Unit) = f()
fun runProcessor(): Processor? {
    var processor: Processor? = null
    inlineAction {
        if (processor != null) processor.process() // safe call 불필요
        processor = nextProcessor()
    }
    return processor
}

// 4) 함수 타입 프로퍼티
class Holder(val provider: (() -> Unit)?) {
    fun process() { if (provider != null) provider() }
}

// 5) try / catch / finally
try { ... ; stringInput = null ; throw Exception() }
catch (e: Exception) { println(stringInput?.length) } // nullable 인지

// 6) 증감 연산자
var unknown: Rho = input
if (unknown is Tau) { ++unknown; unknown.sigma() } // Sigma로 캐스트
```

### 5.3 `enum entries` (2.0 Stable)

```kotlin
enum class RGB { RED, GREEN, BLUE }
inline fun <reified T : Enum<T>> printAllValues() {
    print(enumEntries<T>().joinToString { it.name })
}
printAllValues<RGB>() // RED, GREEN, BLUE
```

`enumValues<T>()`는 호출마다 새 배열을 만들지만 `enumEntries<T>()`는 *동일 인스턴스*를 반환한다.

### 5.4 guard `when` (2.1 Preview → 2.2 Stable)

```kotlin
sealed interface Animal {
    data class Cat(val mouseHunter: Boolean) : Animal { fun feedCat() {} }
    data class Dog(val breed: String) : Animal { fun feedDog() {} }
}

fun feedAnimal(animal: Animal) {
    when (animal) {
        is Animal.Dog -> animal.feedDog()
        is Animal.Cat if !animal.mouseHunter -> animal.feedCat()
        else -> println("Unknown animal")
    }
}
```

이전 1.9 코드는 흔히 `is Animal.Cat -> if (!animal.mouseHunter) ... else ...` 같이 중첩됐고, 가독성이 떨어졌다.

### 5.5 multi-dollar string interpolation (2.1 Preview → 2.2 Stable)

```kotlin
val KClass<*>.jsonSchema : String get() = $$"""
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.com/product.schema.json",
    "$dynamicAnchor": "meta",
    "title": "$${simpleName ?: qualifiedName ?: "unknown"}",
    "type": "object"
}
"""
```

`$schema`, `$id`는 리터럴 그대로 보존되고, `$${...}` 만 보간된다. JSON Schema, Bash heredoc, AsciiDoc/LaTeX 등을 다룰 때 `\$`로 일일이 escape 하던 코드가 깔끔해진다.

### 5.6 non-local `break` / `continue` (2.1 Preview → 2.2 Stable)

```kotlin
fun processList(elements: List<Int>): Boolean {
    for (element in elements) {
        val variable = element.nullableMethod() ?: run {
            log.warning("Element is null or invalid, continuing...")
            continue           // run { } 안에서 비지역 continue
        }
        if (variable == 0) return true
    }
    return false
}
```

이전에는 `?: run { ...; null }` 으로 더미 값을 만들고, `null` 검사를 한 번 더 하는 식의 우회가 많았다.

### 5.7 context parameters (2.2 Preview, KEEP-367)

#### 동기 — 왜 context receivers를 *대체*하나

JetBrains 공식 글의 핵심 인용 [Update on Context Parameters, Kotlin Blog 2025-04]:

> "Migration is **strongly recommended**, as we plan to remove context receivers around the 2.3 release."
> "The latter [context parameters] **require a name**. Introducing this name also requires prefixing any calls."
> "We recognize the need for a good migration path from context receivers into the new context parameter world."

KEEP 자체의 진단 [KEEP context-parameters]:

- context receivers는 *implicit receiver*로 동작해 호출 지점에서 어떤 함수가 어디서 왔는지 추적이 어려운 *scope pollution* 문제가 있었다.
- context parameters는 (i) *이름*이 있어 호출이 명시적이고 (`users.log(...)`), (ii) extension receiver와는 별개로 동작해 callable reference 의미가 명확해지며, (iii) 클래스에 다는 형식은 일단 보류하고 함수/프로퍼티 단위에 한정한다.

#### 문법

```kotlin
interface UserService {
    fun log(message: String)
    fun findUserById(id: Int): String
}

context(users: UserService)
fun outputMessage(message: String) {
    users.log("Log: $message")
}

context(users: UserService)
val firstUser: String
    get() = users.findUserById(1)

context(_: UserService)
fun logWelcome() {
    outputMessage("Welcome!")  // _로 받아도 in-scope 이라 호출 가능
}
```

호출 측은 *type matching*으로 해결된다. 다중 인스턴스가 있으면 ambiguity 에러가 뜨고, `context(serviceA) { ... }` 블록으로 명시한다.

#### 1.9 → 2.2 마이그레이션

A) 제일 깔끔한 옵션은 IntelliJ IDEA 2025.1+의 *"Migrate from context receivers to context parameters"* 인스펙션을 모듈/프로젝트 단위로 적용하는 것이다 [JetBrains Blog 2025-04].

B) IDE 마이그레이션이 못 잡는 부분은 손으로 옮긴다:

```kotlin
// 1.x context receivers (deprecated)
context(Logger)
fun foo() = info("bar")

// 2.2 context parameters
context(logger: Logger)
fun foo() = logger.info("bar")

// 또는 단순 파라미터로 강등
fun foo(logger: Logger) = logger.info("bar")

// 또는 extension으로 강등
fun Logger.foo() = info("bar")
```

[Kotlin 2.0.20 docs]가 직접 제시하는 도식이다.

#### 한계 (2.2.0 시점)

- `class` 자체에는 context parameter를 못 단다 (개별 함수/프로퍼티만).
- *constructor*에는 context parameter 불가.
- context parameter를 가진 함수의 *callable reference*는 2.2.0 미지원, 2.3에서 도입 계획.
- backing field/initializer/delegation을 가진 property에는 context parameter를 동시에 둘 수 없다.

### 5.8 Compose 컴파일러의 위치 변화 (2.0+)

#### 2.0 이전

```kotlin
android {
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.14"
    }
}
```

위 블록이 *Compose ↔ Kotlin 버전 호환성 매트릭스*를 사람 손으로 관리하던 문법이었다 (대표적인 안드로이드 신규 개발자 함정).

#### 2.0 이후 [Compose compiler migration guide]

```toml
# libs.versions.toml
[versions]
kotlin = "2.3.21"

[plugins]
compose-compiler = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
```

```kotlin
// app/build.gradle.kts
plugins {
    alias(libs.plugins.compose.compiler)   // Kotlin과 동일 버전이 자동 적용
}

composeCompiler {
    // featureFlags = setOf(...) 등
}

// composeOptions { kotlinCompilerExtensionVersion = ... } 블록 제거
```

직접 의존성 좌표를 쓰던 빌드 스크립트는 다음과 같이 갱신한다:
- `androidx.compose.compiler:compiler` → `org.jetbrains.kotlin:kotlin-compose-compiler-plugin-embeddable`
- `androidx.compose.compiler:compiler-hosted` → `org.jetbrains.kotlin:kotlin-compose-compiler-plugin`

2.0.20에서는 *Strong Skipping Mode*가 기본값이 되며, 이전의 `enableStrongSkippingMode` 플래그는 deprecate되고 `featureFlags`로 통합됐다 [whatsnew2020]:

```kotlin
composeCompiler {
    featureFlags = setOf(
        ComposeFeatureFlag.IntrinsicRemember.disabled(),
        ComposeFeatureFlag.OptimizeNonSkippingGroups,
        ComposeFeatureFlag.StrongSkipping.disabled()
    )
}
```

### 5.9 stdlib 변화 핵심

- **Base64** (2.2 Stable) — `Base64.Default`, `UrlSafe`, `Mime`, `Pem`. JVM에서는 `output.encodingWith(Base64.Default).use { it.write(bytes) }` 같은 스트림 통합.
- **HexFormat** (2.2 Stable) — `93.toHexString()` → `"5d"`. `HexFormat { number.minLength = 4 ; number.removeLeadingZeros = true }`로 `"005d"`.
- **UUID** (2.0.20 Experimental → 2.3 강화 Experimental) — `Uuid.parse`, `Uuid.random()`, `Uuid.generateV4()`, `Uuid.generateV7()`, `Uuid.parseOrNull(...)`, `Uuid.parseHexDashOrNull(...)`. JVM 측 `java.util.UUID` 와는 `toJavaUuid()`/`toKotlinUuid()` 변환.
- **`kotlin.time.Clock` & `Instant`** (2.1.20 Experimental → 2.3 Stable) — `kotlinx-datetime`이 사실상 표준 라이브러리에 흡수.
- **`kotlin.concurrent.atomics`** (2.1.20 Experimental) — `AtomicInt`, `AtomicLong`, `AtomicBoolean`, `AtomicReference` (KMP 공용). `asJavaAtomic()` / `asKotlinAtomic()`. 2.2.20에서 `update`, `fetchAndUpdate`, `updateAndFetch` 추가.
- **AutoCloseable** (2.0 Stable, 공용) — `AutoCloseable { writer.flushAndClose() }.use { ... }`.

---

## 6. 마이그레이션 가이드 — 단계별 체크리스트

### 6.1 1.9 → 2.0

1. **사전 점검** (Zac Sweers 권고):
   - kapt 의존을 가능한 한 *KSP*로 전환 (Glide, Dagger, Room 등).
   - lint를 최신 알파로 올리고 `android.lint.useK2Uast=true`로 K2 UAST 활성.
   - 라이브러리 작성자라면 Compose compiler / Gradle plugin 종속 코드 사전 점검.
2. **Gradle**:
   - `kotlin = "2.0.x"` 으로 버전 갱신.
   - `.gitignore`에 `.kotlin/` 추가.
   - `kotlinOptions { jvmTarget = "17" }` → `compilerOptions { jvmTarget.set(JvmTarget.JVM_17) }`. (1.9에서는 deprecated 경고지만, 2.2부터는 컴파일 에러.)
   - Compose 사용 모듈은 `kotlin("plugin.compose") version "2.0.x"`로 옮기고 `composeOptions { kotlinCompilerExtensionVersion = ... }` 제거.
3. **Compile error 흡수** — 4.5절의 7~10번 패턴 점검.
4. **롤백 안전망** — 문제 발생 시 `compilerOptions { languageVersion.set(KotlinVersion.KOTLIN_1_9) }`로 K1 시맨틱 유지.

### 6.2 2.0 → 2.1

1. `extraWarnings.set(true)`로 새 경고 묶음 한 번 보기.
2. K2 KAPT 시도: `kapt.use.k2=true` (이때까지는 alpha, 2.1.20에서 디폴트화).
3. sealed exhaustiveness가 더 똑똑해지므로 *기존 `else -> error(...)`* 가 죽은 코드로 보일 수 있음 → 정리.
4. 새 Preview 기능을 도입할지 결정: guard `when`, multi-dollar, non-local break/continue (모두 `-X` 플래그 opt-in).

### 6.3 2.1 → 2.2

1. `kotlinOptions { ... }` 잔존 여부 확인 — 2.2부터 *컴파일 에러*다.
2. context receivers 사용처 → IntelliJ "Migrate to context parameters" 인스펙션 적용. opt-in: `-Xcontext-parameters`.
3. `kotlin-android-extensions` 잔재 제거 → `kotlin-parcelize` + view binding.
4. JVM default method 변화 점검: 인터페이스 default가 진짜 JVM default로 컴파일됨. Java 호환성이 중요한 라이브러리는 `JvmDefaultMode.NO_COMPATIBILITY` / `enable` 중 선택.
5. `KotlinCompilation.source` 사용처 제거 → `defaultSourceSet.dependsOn(...)` 패턴 [multiplatform-compatibility-guide].
6. Apple 타깃 단축형 `ios()`, `watchos()`, `tvos()` → 명시 타깃으로.

### 6.4 2.2 → 2.3

1. `-language-version=1.8` 종료. `1.9`도 비-JVM 타깃에서 종료.
2. Apple 최소 OS 상향: iOS/tvOS 14, watchOS 7. 더 낮은 OS 지원이 필요하면 `-Xoverride-konan-properties=minVersion.ios=12.0` 같은 override 사용 [whatsnew23].
3. Intel Mac 시뮬레이터 빌드(macosX64/iosX64/tvosX64/watchosX64)는 tier 3, 2.4에서 제거 예정. Apple Silicon 우선으로 CI 재구성.
4. Compose stack trace mapping 활성: Composer.setDiagnosticStackTraceMode(...) + Compose runtime ≥1.10.
5. 새 stdlib API 채택 검토: `Clock.System.now()`, `Uuid.generateV7()`, `kotlin.concurrent.atomics`.
6. AGP 9.0+ 사용 시 `org.jetbrains.kotlin.android` 플러그인 제거(빌트인).

### 6.5 누적 deprecation 표 (1.9 → 2.3)

| 항목 | 1.9 | 2.0 | 2.1 | 2.2 | 2.3 |
|---|---|---|---|---|---|
| `kotlinOptions { }` | warn | warn | warn | **error** | error |
| `kotlin-android-extensions` | warn | warn | warn | **removed** | removed |
| context receivers (`-Xcontext-receivers`) | exp | warn (2.0.20) | warn | warn | **removed (예정)** |
| `KotlinCompilation.source(...)` | warn | error | error | error | **removed** |
| Apple `ios()`/`watchos()`/`tvos()` shortcut | warn | warn | error | **removed** | removed |
| `withJava()` | ok | ok | warn (2.1.20) | warn | warn |
| `-language-version=1.6 / 1.7` | ok | ok | warn | **error** | error |
| `-language-version=1.8` | ok | ok | ok | ok | **error (2.3)** |
| Ant 빌드 시스템 | ok | ok | ok | warn | **removed** |
| KSP (1) → KSP2 권고 시점 | KSP1 | 권고 시작 | 권고 | 권고 | 권고 |

---

## 7. 생태계 영향

### 7.1 Spring Boot / Ktor

- **Spring Boot Gradle plugin은 자동으로 Java Application 플러그인을 적용**하기 때문에, KMP 모듈에 직접 Spring Boot plugin을 얹으면 *deprecation warning*과 함께 일부 task 호환 문제가 발생한다. JetBrains 공식 권고는 *"Create separate subproject for Java plugin usage"* — 즉 KMP 라이브러리 모듈과 Spring Boot 애플리케이션 모듈을 분리하라는 것 [whatsnew2020, multiplatform-compatibility-guide].
- **Ktor 측의 Kotlin 2.x 지원**: Ktorfit는 2.0.0, 2.0.10, 2.0.20, 2.0.21, 2.1.0-RC, 2.1.0까지 빠르게 따라가며 Kotlin 2.x compatibility를 명시적으로 표기한다 [foso.github.io/Ktorfit/CHANGELOG]. Ktor 자체의 IDEA 플러그인은 *IDEA 2024.3* 이전까지 K2 mode와 비호환이었다는 보고가 있다 [DigitalFrontiers Medium].

### 7.2 Android

- **AGP 호환 매트릭스** [multiplatform-compatibility-guide]:

| Kotlin | Gradle | AGP | Xcode |
|---|---|---|---|
| 2.0.21 | 7.5–8.8 | 7.4.2–8.5 | 16.0 |
| 2.1.21 | 7.6.3–8.12.1 | 7.3.1–8.7.2 | 16.3 |
| 2.2.21 | 7.6.3–8.14 | 7.3.1–8.11.1 | 26.0 |
| 2.3.21 | 7.6.3–9.3.0 | 8.2.2–9.0.0 | 26.0 |

- **Compose 컴파일러 ↔ Kotlin 1대1 결속** — 2.0부터 Compose 컴파일러는 Kotlin과 같은 버전이고 같은 시점에 릴리스된다. 즉 Kotlin 2.3.x를 쓰면 Compose 컴파일러도 2.3.x. [Android Dev Blog 2024-04, Compose Compiler Gradle plugin docs]
- **AGP 9.0+ 빌트인 Kotlin 지원** — `org.jetbrains.kotlin.android` plugin이 더 이상 필요하지 않다 [whatsnew23].
- **K2 IDE 경험** — IDEA 2024.2에서 K2 mode가 stable로 출시됐고 IDEA 2025.1에서 *기본값*이 됐다. "1.8× faster code highlighting and 1.5× faster code completion on large codebases" [Java Code Geeks 2026 review].
- **Lint K2 UAST** — `android.lint.useK2Uast=true` + `android.experimental.lint.version=8.5.0-alpha08`로 lint도 K2화 [Sweers / preparing-for-k2].

### 7.3 KMP 라이브러리 호환 (kotlinx-coroutines / Compose Multiplatform)

[github.com/Kotlin/kotlinx.coroutines/releases]:

| coroutines | 함께 사용한 Kotlin | KMP/K2 변경점 |
|---|---|---|
| 1.8.0 (2024-02) | 1.9.21 | Wasm/JS 추가 |
| 1.9.0 (2024-09) | 2.0 | Wasm/WASI 추가, K/N·JS 픽스 |
| 1.10.0 (2024-12) | 2.1.0 | 평탄화된 패키지 구성 |
| 1.10.2 (2025-04) | (명시 없음) | 버그픽스 |
| 1.11.0-rc01 (2025-04) | 2.2.20 | Promise 관련 함수 `web` 타깃으로 이전, Wasm/JS는 `JsAny` 서브타입만 허용 (breaking) |

요약: Kotlin 메이저 버전 + 1쿼터 정도의 시차로 안정 minor 릴리스가 따라온다. 2.x로 올릴 때 coroutines를 같이 올리면 호환 문제는 거의 없다.

Compose Multiplatform 측은 Kotlin 2.0과 동시에 Compose 컴파일러 통합이 이뤄졌고, 이후 KMP의 stable 영역이 점진 확장됐다 (2.2.20 Wasm Beta, 2.3 Swift Export 기본 활성).

---

## 8. 한국 커뮤니티 사례

(검색 가능한 한국어 자료를 기준으로 정리. 구글 검색 인덱스의 한계상 OKKY/우아한형제들/카카오의 *전용* K2 후기는 풍부하지 않으며, velog와 Medium-Korean이 1차 자료다.)

- **HyunWoo Lee, "Kotlin 2.0으로 마이그레이션하기"** [Medium @l2hyunwoo] — Android + Compose 프로젝트 마이그레이션. `.gitignore`에 `.kotlin/` 추가, `kotlinOptions` → `compilerOptions` (`JvmTarget.JVM_17`), `composeOptions { kotlinCompilerExtensionVersion = ... }` 제거 후 `org.jetbrains.kotlin.plugin.compose` 도입. convention script에서 `KotlinJvmOptions` → `KotlinAndroidProjectExtension` 교체. 빌드 로직 모듈에서 `org.jetbrains.kotlin:compose-compiler-gradle-plugin` 의존성을 *`compileOnly`*로 둬야 `kotlin-compiler-embeddable`과 중복 클래스 충돌이 안 난다는 실전 팁. 저자 코멘트: *"아직 출시된 지 3일밖에 안된 버전인만큼 안정성/성능에 대한 보고가 명확히 나온 것이 없습니다. 따라서 현실 프로덕트에 적용되기에는 무리가 있어보입니다"* — 1.9 → 2.0.0 직후 시점의 한국 개발자 정서를 잘 보여준다.

- **velog @cksgodl, "Kotlin 2.1.0 언어 변경점 5분 톺기"** — guard `when`, 비지역 break/continue, multi-dollar interpolation을 담백하게 정리. sealed exhaustiveness 개선에 대해 *"왜 이걸 2.1.0에 되서야 지원해 주지"* 라며 늦은 도입을 꼬집음.

- **velog @lifeisbeautiful, "Kotlin 2.0 K2 컴파일러 사용하기"** — Android Studio에서 K2 모드를 켜는 절차, 그리고 K2 / FIR 한국어 설명.

- **velog @gudrmsglgl, "Kotlin 2.0 Migration"** — `build.gradle` (Groovy) 기반 프로젝트에서의 마이그레이션 절차. Compose compiler 플러그인의 ID가 *Google → JetBrains*으로 바뀐 점을 강조.

- **velog @parkchaebin, "Kotlin 2.2.20 코드 개선사항"** — 2.2.20의 신규 어노테이션 메타 타깃, when 데이터 흐름 exhaustiveness 등.

- **하회탈의 블로그, "Kotlin 2.0 으로 마이그레이션(KSP, proto dataStore)"** — KSP 위주의 실전 마이그레이션. kapt 잔재 제거가 가장 큰 일이라는 결론.

이들 자료의 공통 톤은 다음과 같다:

1. *큰 시각의 드라마는 없다*. 안드로이드 프로젝트 기준 빌드 스크립트 변경이 핵심이고, 코드 자체의 변경은 거의 필요 없다.
2. *Compose 컴파일러 플러그인 변경*이 가장 자주 부딪히는 함정이다.
3. *"바로 프로덕션에 올리지는 마라"*. 여러 저자가 2.0 출시 직후 두세 마이너 버전을 기다린 뒤 도입하라고 권한다.

---

## 9. 1.9 vs 2.x — 코드 비교 사례 모음

### 9.1 1.9에서는 실험적이었으나 2.x에서 정식이 된 API

| API | 1.9 상태 | 2.x 상태 |
|---|---|---|
| K2 컴파일러 | beta opt-in (`-language-version=2.0`) | 2.0 Stable 기본 |
| `data object` | 1.9 beta | 2.0 Stable |
| `enumEntries<T>()` | 1.9 experimental | 2.0 Stable |
| `AutoCloseable` (common) | 1.9 experimental | 2.0 Stable |
| Compose compiler integration | 미통합 | 2.0 통합 |
| Kotlin Multiplatform | 1.9.20 Stable | 그대로 Stable |
| `kotlin.io.encoding.Base64` | 1.8 experimental | 2.2 Stable |
| `Int.toHexString()` (HexFormat) | 1.8 experimental | 2.2 Stable |
| guard `when` | 없음 | 2.1 Preview → 2.2 Stable |
| non-local break/continue (inline lambda) | 없음 | 2.1 Preview → 2.2 Stable |
| multi-dollar interpolation | 없음 | 2.1 Preview → 2.2 Stable |
| `kotlin.time.Clock` / `Instant` | `kotlinx-datetime` | 2.3 Stable (stdlib) |

### 9.2 1.9 코드가 2.x에서 컴파일 에러를 만드는 대표 사례

```kotlin
// ❌ 1.9 OK / ❌ 2.0 ERROR
open class Base {
    open val a: Int      // K2: open val must have initializer
    open var b: Int
    init {
        this.a = 1       // K2: error
        this.b = 1
    }
}
```

```kotlin
// ❌ 1.9 OK (warn) / ❌ 2.2 ERROR
android {
    kotlinOptions {
        jvmTarget = "17"
    }
}

// ✅ 2.0+ 권장
android {
    kotlin {
        compilerOptions {
            jvmTarget.set(JvmTarget.JVM_17)
        }
    }
}
```

```kotlin
// 1.9 (Compose 1.5)
android {
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.14"
    }
}

// 2.0+
plugins {
    alias(libs.plugins.compose.compiler)
}
composeCompiler {
    featureFlags = setOf(
        ComposeFeatureFlag.OptimizeNonSkippingGroups,
    )
}
```

```kotlin
// 1.9 (kotlin-android-extensions)
@Parcelize        // kotlin-android-extensions 시절
data class User(val name: String) : Parcelable

// 2.0+ (kotlin-parcelize, 1.4.30부터 권고됐지만 2.2에서 강제됨)
plugins { id("kotlin-parcelize") }
@Parcelize
data class User(val name: String) : Parcelable
```

```kotlin
// 1.9 (이벤트 소싱 직렬화 람다)
class Aggregate {
    val onEvent: (Event) -> Unit = { ev -> apply(ev) }   // 직렬화 OK
}

// 2.0+ (invokedynamic 기본 → 직렬화 깨짐)
class Aggregate {
    @JvmSerializableLambda                                // 또는 모듈 레벨 -Xlambdas=class
    val onEvent: (Event) -> Unit = { ev -> apply(ev) }
}
```

```kotlin
// 1.9 — Java int[]
val first = dataService.fetchData()[0]  // K1: OK

// 2.0+ — int @Nullable []
val first = dataService.fetchData()?.get(0)  // K2: ?. 강제
```

### 9.3 2.x에서만 작성 가능한 우아한 표현

```kotlin
// guard when (2.2 Stable)
sealed interface Animal {
    data class Cat(val mouseHunter: Boolean) : Animal
    data class Dog(val breed: String) : Animal
}
fun feed(a: Animal) = when (a) {
    is Animal.Dog -> "give bone"
    is Animal.Cat if !a.mouseHunter -> "give can"
    is Animal.Cat -> "let it hunt"
}
```

```kotlin
// data object + sealed (2.0 Stable)
sealed class ReadResult {
    data class Number(val n: Int) : ReadResult()
    data class Text(val t: String) : ReadResult()
    data object EndOfFile : ReadResult()       // toString() == "EndOfFile"
}
```

```kotlin
// context parameters (2.2 Preview)
context(logger: Logger, tx: Transaction)
fun saveUser(u: User) {
    logger.info("saving ${u.id}")
    tx.persist(u)
}

context(logger, tx) {
    saveUser(u)
}
```

```kotlin
// non-local continue (2.2 Stable)
fun process(elements: List<Int?>): Int {
    var sum = 0
    for (e in elements) {
        val v = e ?: run { log.warn("null"); continue }
        sum += v
    }
    return sum
}
```

```kotlin
// multi-dollar interpolation in JSON Schema (2.2 Stable)
val schema = $$"""
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/$${name}.json"
}
"""
```

```kotlin
// explicit backing field (2.3 Experimental)
val city: StateFlow<String>
    field = MutableStateFlow("")
fun updateCity(newCity: String) { city.value = newCity }
```

```kotlin
// kotlin.time.Clock + Uuid v7 (2.3)
val ts = Clock.System.now()
val id = Uuid.generateV7NonMonotonicAt(ts)
```

---

## 10. 논쟁점·미해결

이 책의 후반부에서 *균형 잡힌 시선*을 위해 명시할 만한 쟁점.

1. **K2 컴파일 속도 — 어디까지 일반화 가능한가?**
   - 관점 A (JetBrains): "compiles it twice as fast."
   - 관점 B (Sweers / Slack): 자기 codebase에서 ~17% *느려짐*. "I would highly recommend doing your own measurements."
   - 결론: 평균은 상승, 분산은 크다. 책에서는 "벤치마크의 *모양*과 *측정 방법*"을 가르치는 챕터가 가치 있다.

2. **context parameters의 *이름 강제*에 대한 반응.**
   - 옹호 측 (JetBrains): scope pollution 해결, IDE 추적성, callable reference 모호성 해결.
   - 비판 측 (커뮤니티 일부 / 옛 context receivers 사용자): *"introducing this name also requires prefixing any calls"* — 즉, 함수 본문이 더 verbose 해진다. KEEP 자체에 *"bridge functions"* 패턴이 마이그레이션 권고로 들어간 것은 이 verbosity를 의식한 것이다.
   - 결론: arrow-kt의 `Raise<E>.()`처럼 receiver 의존이 깊은 라이브러리는 *dual API* 기간이 필요하다.

3. **kapt vs KSP2 vs K2 KAPT.**
   - JetBrains 공식 권고: *KSP를 우선*.
   - Sweers: KSP2는 "still has a lot of open issues" 라며 메이저 라이브러리 마이그레이션이 끝나지 않았다고 평가 (2024 시점 글). 2025-09 시점(2.2.20)에는 K2 KAPT가 사실상 디폴트라 "kapt를 그대로 두고 K2 KAPT를 쓰는" 길이 가장 안전한 절충안.

4. **KMP의 Apple 타깃 정리.**
   - 2.3에서 iOS/tvOS 12 → 14, watchOS 5 → 7. macosX64/iosX64/tvosX64/watchosX64는 2.4에서 제거 예정.
   - 한국에서는 여전히 iOS 13 사용자 베이스가 통계적으로 비무시할 수준이라, *비즈니스 결정*이 필요한 영역.

5. **2.2의 "kotlinOptions 컴파일 에러"의 강제성.**
   - 2.0에서 deprecate 됐지만 *2년에 걸친 점진적 deprecate*에 비해 짧은 기간(약 1년)으로 error 화. 일부 빌드 로직 모듈(특히 사내 convention plugin)이 이 변경에 늦게 대응해 빌드가 한 번에 멈추는 사례.

---

## 11. 참고문헌

### JetBrains 공식 (1차 자료)

- *What's new in Kotlin 2.0.0*, https://kotlinlang.org/docs/whatsnew20.html (Release: 2024-05-21).
- *What's new in Kotlin 2.0.20*, https://kotlinlang.org/docs/whatsnew2020.html (2024-08-22).
- *What's new in Kotlin 2.1.0*, https://kotlinlang.org/docs/whatsnew21.html (2024-11-27).
- *What's new in Kotlin 2.1.20*, https://kotlinlang.org/docs/whatsnew2120.html (2025-03-20).
- *What's new in Kotlin 2.2.0*, https://kotlinlang.org/docs/whatsnew22.html (2025-06).
- *What's new in Kotlin 2.2.20*, https://kotlinlang.org/docs/whatsnew2220.html (2025-09-10).
- *What's new in Kotlin 2.3.0*, https://kotlinlang.org/docs/whatsnew23.html (2025-12-16).
- *K2 compiler migration guide*, https://kotlinlang.org/docs/k2-compiler-migration-guide.html.
- *Compose Compiler migration guide*, https://kotlinlang.org/docs/compose-compiler-migration-guide.html.
- *Components stability levels*, https://kotlinlang.org/docs/components-stability.html.
- *Multiplatform compatibility guide*, https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html.
- *Context parameters*, https://kotlinlang.org/docs/context-parameters.html.
- *The K2 Compiler Is Going Stable in Kotlin 2.0*, https://blog.jetbrains.com/kotlin/2023/02/k2-kotlin-2-0/ (2023-02).
- *K2 Compiler Performance Benchmarks and How to Measure Them on Your Projects*, https://blog.jetbrains.com/kotlin/2024/04/k2-compiler-performance-benchmarks-and-how-to-measure-them-on-your-projects/ (2024-04).
- *Celebrating Kotlin 2.0: Fast, Smart, and Multiplatform*, https://blog.jetbrains.com/kotlin/2024/05/celebrating-kotlin-2-0-fast-smart-and-multiplatform/ (2024-05).
- *Kotlin 2.0.20 Released*, https://blog.jetbrains.com/kotlin/2024/08/kotlin-2-0-20-released/ (2024-08).
- *Update on Context Parameters*, https://blog.jetbrains.com/kotlin/2025/04/update-on-context-parameters/ (2025-04).
- *Kotlin Roundup: KotlinConf 2024 Keynote Highlights*, https://blog.jetbrains.com/kotlin/2024/05/kotlin-roundup-kotlinconf-2024-keynote-highlights/.
- Michail Zarečenskij, *Kotlin Language Features in 2.0 and Beyond*, KotlinConf 2024 발표 슬라이드, https://resources.jetbrains.com/storage/products/kotlinconf-2024/may-23/Michail%20Zarecenskij-Kotlin%20Language%20Features%20in%202.0%20and%20Beyond.pdf (2024-05).
- KotlinConf 2024 talk page, *K2: How to make a better compiler but keep Kotlin the same*, https://kotlinconf.com/2024/talks/627087/.

### KEEP / GitHub (1차 자료)

- KEEP, *Context parameters*, https://github.com/Kotlin/KEEP/blob/master/proposals/context-parameters.md.
- Kotlin/KEEP issue #367, *Context parameters*, https://github.com/Kotlin/KEEP/issues/367.
- KT-71140, KT-2425, KT-1436, KT-71439 (YouTrack) — 각 Preview 기능별 트래커.
- kotlinx.coroutines releases, https://github.com/Kotlin/kotlinx.coroutines/releases.

### Android Developers (1차 자료)

- *Jetpack Compose compiler moving to the Kotlin repository*, Android Developers Blog, https://android-developers.googleblog.com/2024/04/jetpack-compose-compiler-moving-to-kotlin-repository.html (2024-04).
- *Compose Compiler Gradle plugin*, https://developer.android.com/develop/ui/compose/compiler.
- *Compose to Kotlin Compatibility Map*, https://developer.android.com/jetpack/androidx/releases/compose-kotlin.

### 영문 커뮤니티·실무 사례

- Benedikt Jerat, *Migrating to Kotlin 2.0 — A slightly bumpy journey*, Medium — DigitalFrontiers, https://medium.com/digitalfrontiers/migrating-to-kotlin-2-0-a-slightly-bumpy-journey-33f688a0a86a.
- Zac Sweers, *Preparing for K2*, https://www.zacsweers.dev/preparing-for-k2/.
- Apollo GraphQL, *Journey to K2: using the New Compiler in Apollo Kotlin*, https://www.apollographql.com/blog/journey-to-k2-using-the-new-compiler-in-apollo-kotlin.
- Kacper Wojciechowski, *Kotlin 2.0 — Android project migration guide*, Medium, https://medium.com/@kacper.wojciechowski/kotlin-2-0-android-project-migration-guide-b1234fbbff65.
- Iniyan Murugavel, *Migrating to Kotlin 2.0.0: A Comprehensive Guide*, Medium, https://medium.com/@javainiyan/migrating-to-kotlin-2-0-0-a-comprehensive-guide-2b1c785770a7.
- Carrion.dev, *Understanding Context Parameters in Kotlin 2.2.0*, https://carrion.dev/en/posts/context-parameters-kotlin/.
- Kirill Rakhman, *Kotlin: Emerging Patterns with Context Parameters*, https://rakhman.info/blog/kotlin-emerging-patterns-with-context-parameters/.
- droidcon, *Migrating To Kotlin 2.0 In Your Jetpack Compose Project*, https://www.droidcon.com/2025/04/29/migrating-to-kotlin-2-0-in-your-jetpack-compose-project/.
- Java Code Geeks, *Kotlin in 2025–2026: The K2 Era and the Rise of True Multiplatform Development*, https://www.javacodegeeks.com/2026/04/kotlin-in-2025-2026-the-k2-era-and-the-rise-of-true-multiplatform-development.html.
- InfoQ, *Kotlin 2.0 Launched with New, Faster, More Flexible K2 Compiler*, https://www.infoq.com/news/2024/05/kotlin-2-k2-compiler/.

### 한국어 자료

- HyunWoo Lee (이현우), *Kotlin 2.0으로 마이그레이션하기*, Medium, https://medium.com/@l2hyunwoo/kotlin-2-0%EC%9C%BC%EB%A1%9C-%EB%A7%88%EC%9D%B4%EA%B7%B8%EB%A0%88%EC%9D%B4%EC%85%98%ED%95%98%EA%B8%B0-1742f294df51.
- velog @cksgodl, *[Kotlin] Kotlin 2.1.0 언어 변경점 5분 톺기*, https://velog.io/@cksgodl/Kotlin-Kotlin-2.1.0-%EC%96%B8%EC%96%B4-%EB%B3%80%EA%B2%BD%EC%A0%90-5%EB%B6%84-%ED%86%BA%EA%B8%B0.
- velog @cksgodl, *[Kotlin] The road to K2 compiler 리캡*, https://velog.io/@cksgodl/Kotlin-The-road-to-K2-compiler-%EB%A6%AC%EC%BA%A1.
- velog @lifeisbeautiful, *Kotlin 2.0 K2 컴파일러 사용하기*, https://velog.io/@lifeisbeautiful/Kotlin2.0-K2-%EC%BB%B4%ED%8C%8C%EC%9D%BC%EB%9F%AC-%EC%82%AC%EC%9A%A9%ED%95%98.
- velog @gudrmsglgl, *Kotlin 2.0 Migration*, https://velog.io/@gudrmsglgl/Kotlin-2.0-Migration.
- velog @parkchaebin, *Kotlin 2.2.20 코드 개선사항*, https://velog.io/@parkchaebin/Kotlin-2.2.20-%EC%BD%94%EB%93%9C-%EA%B0%9C%EC%84%A0%EC%82%AC%ED%95%AD.
- 하회탈, *Kotlin 2.0 으로 마이그레이션(KSP, proto dataStore)*, https://hhtt.kr/103405.
- Munseong, *[Kotlin] K2 Compiler란?*, https://munseong.dev/kotlin/k2compiler/.
- 노성현 LinkedIn 게시글, *K2 컴파일러가 Kotlin 2.0에 들어왔어요*, https://kr.linkedin.com/posts/devload_k2-%EC%BB%B4%ED%8C%8C%EC%9D%BC%EB%9F%AC%EA%B0%80-kotlin-20%EC%97%90-%EB%93%A4%EC%96%B4%EC%99%94%EC%96%B4%EC%9A%94-activity-7105825334742175744-Ft4t.
- *Kotlin 2.0 출시: 빠른 속도, 스마트한 기능, 멀티플랫폼 지원* (Kotlin Blog 한국어판), https://blog.jetbrains.com/kotlin/2024/05/celebrating-kotlin-2-0-fast-smart-and-multiplatform/.

---

## 12. 리서치 한계 (커버하지 못한 영역)

이 1차 레퍼런스는 다음 영역에서 보강이 필요하다. 이후 챕터 저술 단계에서 필요시 추가 리서치를 트리거할 만한 지점들이다.

1. **Reddit r/Kotlin / r/androiddev의 *원문 스레드 인용*.** Web 검색 인덱스를 통해 *요약*은 확보했지만 (예: K2 17% 회귀 보고, IDEA Ktor 플러그인 미호환 등) 개별 댓글의 토큰 단위 인용은 확보하지 못했다. 마이그레이션 챕터에서 "Reddit 원문 인용"이 필요하면 Reddit search/Pushshift 같은 API로 추가 수집을 권장한다.

2. **국내 카카오·우아한형제들·라인·NHN 기술 블로그의 K2 도입 후기.** 검색 결과에서 직접 매칭되는 1차 글이 잡히지 않았다. 한국어 사례는 velog와 Medium-Korean 위주로만 정리됐다. 책에서 *국내 대형 서비스의 도입기* 챕터를 두려면 별도 인터뷰/사례 수집이 필요하다.

3. **YouTrack KT-* 이슈 단위의 회귀 사례 deep-dive.** 본 문서는 JetBrains가 What's new에서 언급한 회귀와 Sweers/DigitalFrontiers가 정리한 사례까지만 다뤘다. *현 시점(2026-04)에서 살아 있는 K2 회귀 이슈*의 상세 목록은 별도 검색이 필요하다.

4. **JVMLS / KotlinConf 2025 발표.** 본 문서는 KotlinConf 2024 자료(슬라이드, talk 페이지)까지만 인용했다. KotlinConf 2025 발표 중 2.3 관련 세션이 별도 자료를 제공하면 9·10절 보강에 유용하다.

5. **Compose Multiplatform의 Stable 영역 변천.** 2.3 What's new가 다룬 부분 외, Compose for iOS / Web의 stability 변화는 Compose Multiplatform 자체 changelog에서 더 정확히 확인해야 한다 (kotlinlang.org가 아닌 jetbrains.com/lp/compose-multiplatform 측 문서).

6. **paper-researcher 트랙 — 학술 논문 부재.** 본 주제는 학술 논문이 거의 존재하지 않아, 의도적으로 *KotlinConf / JVMLS 발표*와 *KEEP 디자인 문서*로 학술 트랙을 대체했다. 향후 컴파일러 IR 디자인 관련 학술 글(예: Roman Elizarov 등의 Stack-machine FIR 디자인 토크)을 보강할 수 있다.

7. **Reddit/HN의 K2 *수치 검증*.** Slack의 17% 회귀처럼 *역방향 수치*가 더 있는지의 체계적 추적은 본 문서 범위 밖.

위 한계를 명시한 채로, 본 문서는 대상 독자(1.9 → 2.x 마이그레이션을 검토하는 시니어 개발자)가 *책 본문 챕터 1~7*의 토대로 사용하기에 충분한 1차 레퍼런스다.
