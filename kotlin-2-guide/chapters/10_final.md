# 10장. 생태계의 적응 — Spring, Ktor, Android Compose, KMP

월요일 아침이라고 해보자. 지난 주에 9장을 따라 1.9에서 2.3까지의 단계 사다리를 정리해 두었고, 이번 주에는 한 번에 한 모듈씩 그 사다리를 오르려 한다. 그런데 첫 모듈을 손대자마자 빌드가 어그러진다. KMP 라이브러리 모듈에 Spring Boot Gradle plugin을 슬쩍 얹은 순간, 콘솔에 deprecation warning이 줄줄이 흐른다. "분명히 작년까지는 잘 됐는데" 하고 머리를 긁는다. 그 옆 모듈에서는 안드로이드 동료가 `composeOptions { kotlinCompilerExtensionVersion = "1.5.14" }` 한 줄을 어떻게 처리할지를 두고 고민에 빠져 있고, 또 그 옆에서는 Compose Multiplatform iOS 빌드가 Xcode 호환 매트릭스를 잘못 읽어 멈춰 있다. 우리가 마주한 풍경은 한 사람의 1.9 → 2.3 마이그레이션이 아니다. *생태계 전체의 적응*이다.

이 변화는 누적 캐스케이드의 *생태계 좌표 잡기* 갈래에 속한다. 9장이 시간 축의 사다리였다면 10장은 같은 시간 축에 *우리 회사의 기술 스택*을 겹쳐 두는 일이다. Spring을 쓰는지 Ktor를 쓰는지, Compose 모듈이 있는지, KMP로 iOS까지 보내는지에 따라 같은 2.0 → 2.1 한 칸도 무게가 다르게 실린다. 생태계의 적응 속도와 *우리의 적응 속도*가 만나는 자리를 가늠해 두지 않으면, 9장의 사다리는 종이 위에서만 멀끔한 그림이 된다.

그래서 같이 풀어볼 화두가 셋이다. Spring Boot Gradle plugin이 KMP 모듈에 닿는 순간 왜 deprecation warning이 쏟아지는가. 어제까지 `kotlinCompilerExtensionVersion = "1.5.14"` 한 줄로 발이 묶였던 우리 빌드가 2.3에서는 `alias(libs.plugins.compose.compiler)` 한 줄로 끝난다고 할 때, 우리가 *잃은 것*은 정말 없는가. 그리고 AGP 9.0이 `org.jetbrains.kotlin.android` 플러그인을 빌트인으로 흡수한다는 것은 안드로이드 빌드 스크립트에 어떤 신호인가. 세 질문 모두 답이 한 줄짜리는 아니다. 하지만 답을 찾아가는 과정이 곧 우리 회사 *기술 스택 조합*의 위치를 잡아주는 과정이 된다.

## Spring Boot와 Ktor — 서버 진영의 적응

Spring Boot가 KMP 모듈을 만나는 자리는 묘하다. JetBrains 공식 권고는 한 줄이다 — *Create separate subproject for Java plugin usage*. 왜 그런 말을 굳이 박아 두었을까. Spring Boot Gradle plugin이 자동으로 Java Application 플러그인을 적용하기 때문이다. 즉 우리가 `id("org.springframework.boot")` 한 줄을 KMP 라이브러리 모듈에 얹는 순간, Gradle은 그 모듈을 "Java Application 모듈"로 간주하기 시작한다. 그런데 KMP 측은 같은 모듈을 "여러 타깃을 가진 멀티플랫폼 모듈"로 간주한다. 두 인식이 한 모듈 위에서 충돌하니, deprecation warning과 task 호환 문제가 동시에 쏟아진다. 빌드는 일단 굴러가지만, 콘솔이 노란 글자로 가득 차서 *어디부터가 진짜 문제인지* 분간이 어려워진다. 난감하다.

해법은 의외로 단순하다. 한 모듈에 두 책임을 욱여넣지 말고, *분리하자*. KMP 라이브러리 모듈은 라이브러리답게 두고, Spring Boot 애플리케이션은 별도의 서브프로젝트로 빼는 편이 낫다. 멀티 모듈 구성이 늘어 부담스럽게 들릴 수도 있다. 하지만 한 모듈이 두 정체성을 동시에 갖는 빌드 스크립트를 매번 의심하며 읽는 비용이 더 크다. 책임 분리가 빌드 스크립트의 *사고 비용*을 낮춰준다고 기억해두자.

Ktor 진영의 적응은 결이 다르다. Ktorfit는 Kotlin 2.x를 빠르게 따라잡았다. 2.0.0, 2.0.10, 2.0.20, 2.0.21, 2.1.0-RC, 2.1.0까지 거의 매 minor 릴리스에 호환을 명시적으로 표기했다. 라이브러리 작성자가 "Kotlin 2.x compatibility"를 changelog에 박아 둔다는 것은, 사용자가 자신의 Kotlin 버전을 올릴 때 *함께 올릴 수 있는 안전선*을 미리 그어 준다는 뜻이다. 사용자 입장에서는 이런 라이브러리에 의존하는 것이 가장 마음이 편하다. 반대로, 자기 회사 내부 라이브러리에는 이런 표기가 없는 경우가 많다. 사내 공통 모듈에 Kotlin 호환 표를 한 줄 추가해 두는 것이 *외부 OSS 라이브러리에서 배운 좋은 습관*임을 잊지 말자.

다만 Ktor 진영도 모든 자리가 매끄럽지는 않았다. Ktor IDEA 플러그인은 IDEA 2024.3 이전까지 K2 mode와 비호환이었다는 보고가 있다. 우리가 IDE의 K2 mode를 켜자마자 Ktor 플러그인이 묘한 빨간 줄을 그어대면 그건 코드의 문제가 아니라 IDE 도구 체인의 비호환 잔재다. 이런 사례는 Ktor 한 군데에 한정되지 않는다. K2 IDE는 컴파일러와 같은 FIR 위에서 돌기 때문에, *컴파일러가 봐주던 것을 IDE가 더 엄격하게 보는* 경우가 종종 있다. 이상한 경고가 보이면 IDE 버전과 플러그인 버전을 한 번 더 점검해보자.

서버 진영에서 함께 따라오는 단골 이슈는 `kotlinx-serialization` 컴파일러 플러그인이다. 2.0의 invokedynamic 람다 변환과 serialization 컴파일러 플러그인이 같은 모듈에서 얽히면 ABI 불일치가 발생할 수 있다. 직렬화가 깨진 람다는 흔히 *"Illegal state change detected!"* 같은 메시지로 모습을 드러낸다. 6장에서 이미 등장한 풍경이지만, 서버 측 이벤트 소싱(CQRS/ES) 시스템에서는 한 번 더 만난다. 안전한 합의는 두 가지다. 직렬화가 필요한 람다에는 `@JvmSerializableLambda`를 붙이거나, 모듈 레벨에서 `-Xlambdas=class`로 옛 동작을 유지한다. 어느 쪽이든 *한 줄 결정*이지만, 그 한 줄을 의식적으로 두지 않으면 운영 환경에서 무성의한 NPE처럼 튀어나온다. 찜찜한 것은 미리 끊어두자.

## Android와 Jetpack Compose — composeOptions의 종언

안드로이드 진영에서 가장 자주 보는 풍경은 한 줄짜리 빌드 스크립트의 변신이다. 1.9 시절, Compose 모듈의 `build.gradle.kts`는 보통 이렇게 생겼다.

```kotlin
// 1.9 시절 (Compose 1.5)
android {
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.14"
    }
}

dependencies {
    implementation("androidx.compose.compiler:compiler:1.5.14")
}
```

이 한 줄이 무엇을 했는지 잠깐 떠올려보자. `kotlinCompilerExtensionVersion`은 *Compose 컴파일러*와 *Kotlin 컴파일러*의 호환 버전을 사람 손으로 묶어 두는 자리였다. Compose 1.5.14가 어떤 Kotlin 버전과 짝이 맞는지를 사람이 *Compose to Kotlin Compatibility Map*을 펼쳐 가며 매번 확인했다. Kotlin을 1.9.21에서 1.9.22로 올리는 사소한 패치 한 번에도, Compose 컴파일러 호환 표를 다시 들여다보고 거기 적힌 숫자를 손으로 옮겨 넣어야 했다. 안드로이드 신규 개발자가 가장 자주 빠지는 함정 중 하나였고, *Compose가 깨지는 가장 흔한 이유*가 늘 이 호환 표였다. 끔찍한 일이다.

2.0부터는 이 풍경이 통째로 사라진다. Compose 컴파일러가 Kotlin 저장소로 이관됐고, *Kotlin과 같은 버전으로 함께 릴리스*된다. Android Developers Blog 표현 그대로 옮기자면, "The Jetpack Compose compiler … has been merged into the Kotlin repository and will now ship with Kotlin"이다. 그러니 `composeOptions { kotlinCompilerExtensionVersion = ... }` 블록은 더는 의미가 없다. 2.3 시점의 같은 모듈은 이렇게 정리된다.

```kotlin
// 2.3 시점
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.compose.compiler)   // Kotlin과 동일 버전이 자동 적용
}

composeCompiler {
    featureFlags = setOf(
        ComposeFeatureFlag.OptimizeNonSkippingGroups,
    )
}
```

`libs.versions.toml` 쪽도 한 번에 정리된다.

```toml
[versions]
kotlin = "2.3.0"

[plugins]
kotlin-android   = { id = "org.jetbrains.kotlin.android",        version.ref = "kotlin" }
compose-compiler = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
```

세 줄짜리 호환 매트릭스가 *Kotlin 버전 한 줄*로 흡수됐다. 우리가 잃은 것이 정말 없는지 다시 물어보자. *호환 표를 사람 손으로 관리하던 자유*를 잃긴 했다. 즉 Compose 컴파일러를 Kotlin 버전과 *어긋난 채* 의도적으로 쓰는 길이 막혔다는 뜻이다. 그러나 그 자유가 우리에게 행복을 가져다 준 적이 있었던가. 거의 없다. 잃은 것은 *위험한 자유* 한 자락이고, 얻은 것은 *호환 매트릭스를 하루에도 몇 번씩 사람 머리로 검증하던 부담 전체*다. 이 거래는 받아들일 만하다.

부수적으로 따라오는 변화도 점검해두자. 2.0.20부터 Compose 컴파일러는 *Strong Skipping Mode*가 기본이다. 같이 `includeTraceMarkers=true`도 기본이고, 추상 `@Composable`에 기본값 파라미터를 허용한다. 옛 동작이 필요하면 `composeCompiler { featureFlags = setOf(ComposeFeatureFlag.StrongSkipping.disabled()) }`로 끄는 길이 있다. 다만 *기본값을 끄려면 그 이유가 명확해야 한다*는 원칙은 잊지 말자. JetBrains/Google이 한 번 기본을 바꿨다는 것은, 다음 minor에서 그 자리에 더 강한 가정을 얹을 수 있다는 신호이기도 하다.

호환 매트릭스 자체도 한 번 보고 가자. Kotlin / Gradle / AGP / Xcode 네 자리의 짝은 다음과 같다.

| Kotlin | Gradle | AGP | Xcode |
|---|---|---|---|
| 2.0.21 | 7.5–8.8 | 7.4.2–8.5 | 16.0 |
| 2.1.21 | 7.6.3–8.12.1 | 7.3.1–8.7.2 | 16.3 |
| 2.2.21 | 7.6.3–8.14 | 7.3.1–8.11.1 | 26.0 |
| 2.3.21 | 7.6.3–9.3.0 | 8.2.2–9.0.0 | 26.0 |

표를 보면 한 가지가 눈에 띈다. 2.2 → 2.3 사이에 *AGP 하한*이 7.x에서 8.2로 점프했고, *Xcode*는 16에서 26으로 단숨에 올라간다. AGP 하한이 올라간다는 것은 사내 안드로이드 모듈이 AGP 7.x에 멈춰 있다면 2.3 도입을 결정하기 전에 AGP 업그레이드부터 따로 들어가야 한다는 뜻이다. Xcode 26은 macOS 최소 버전과도 얽혀 있어 CI 머신을 손대야 할 수도 있다. 즉 Kotlin 한 칸이 *주변의 두 칸을 같이 끌고 올라가는* 단계다. 이런 자리는 9장 사다리에서도 빨간 별표를 붙여 둘 만하다.

### [박스 1] AGP 9.0+ 빌드 스크립트 다이어트 — before/after 한 페이지

> AGP 9.0+ 환경에서는 `org.jetbrains.kotlin.android` Gradle 플러그인이 더 이상 필요하지 않다. AGP가 빌트인으로 Kotlin을 흡수했기 때문이다. 이 변화가 안드로이드 빌드 스크립트에 보내는 신호는 한 줄로 요약된다. *플러그인 블록이 다이어트한다*. 같은 모듈을 1.9 시절과 AGP 9.0+ 시점에 나란히 두면 다음과 같다.
>
> ```kotlin
> // before — 1.9 시절 모듈 build.gradle.kts
> plugins {
>     id("com.android.application")
>     id("org.jetbrains.kotlin.android")
>     id("kotlin-kapt")
>     id("kotlin-parcelize")
> }
>
> android {
>     namespace = "com.acme.app"
>     compileSdk = 34
>
>     kotlinOptions {
>         jvmTarget = "17"
>     }
>
>     composeOptions {
>         kotlinCompilerExtensionVersion = "1.5.14"
>     }
> }
>
> dependencies {
>     implementation("androidx.compose.compiler:compiler:1.5.14")
>     kapt("com.google.dagger:dagger-compiler:2.51")
> }
> ```
>
> ```kotlin
> // after — AGP 9.0+ / Kotlin 2.3 시점
> plugins {
>     alias(libs.plugins.android.application)
>     alias(libs.plugins.compose.compiler)
>     alias(libs.plugins.ksp)
>     alias(libs.plugins.kotlin.parcelize)
> }
>
> android {
>     namespace = "com.acme.app"
>     compileSdk = 36
>
>     kotlin {
>         compilerOptions {
>             jvmTarget.set(JvmTarget.JVM_17)
>         }
>     }
> }
>
> composeCompiler {
>     featureFlags = setOf(ComposeFeatureFlag.OptimizeNonSkippingGroups)
> }
>
> dependencies {
>     ksp("com.google.dagger:dagger-compiler:2.51")
> }
> ```
>
> 한 줄씩 사라진 것을 세어보자. `id("org.jetbrains.kotlin.android")` 한 줄, `id("kotlin-kapt")` 한 줄, `composeOptions { kotlinCompilerExtensionVersion = ... }` 블록, `androidx.compose.compiler:compiler` 직접 의존 한 줄. 그리고 `kotlinOptions` 블록은 `kotlin { compilerOptions { ... } }`로 모양을 바꿨다. 결과적으로 빌드 스크립트의 *Kotlin 관련 면적이 절반*으로 줄었다. AGP 9.0이 보내는 신호는 분명하다. *빌드 스크립트는 더 가벼워지고, 호환은 도구 체인 안쪽으로 들어간다*. 우리는 그 흐름을 거스르지 말고 한 모듈씩 따라가자.

## KMP와 kotlinx-coroutines — 시간 지도 한 장

KMP 진영의 적응은 *시간 축*으로 본다. 메이저 Kotlin 릴리스가 나오면, kotlinx-coroutines는 한 분기쯤 시차를 두고 안정 minor를 따라온다. 다음 표는 그 시간 지도다.

| coroutines | 함께 쓴 Kotlin | KMP/K2 변경점 |
|---|---|---|
| 1.8.0 (2024-02) | 1.9.21 | Wasm/JS 추가 |
| 1.9.0 (2024-09) | 2.0 | Wasm/WASI 추가, K/N·JS 픽스 |
| 1.10.0 (2024-12) | 2.1.0 | 패키지 구성 평탄화 |
| 1.10.2 (2025-04) | (명시 없음) | 버그픽스 |
| 1.11.0-rc01 (2025-04) | 2.2.20 | Promise 함수 `web` 타깃 이전, Wasm/JS는 `JsAny` 서브타입만 허용 (breaking) |

요지는 단순하다. Kotlin 메이저를 올릴 때 coroutines를 같이 올리면 호환 문제는 거의 없다. 정작 주의할 자리는 *coroutines만 먼저* 혹은 *Kotlin만 먼저* 올라가는 어긋남이다. 사내 buildSrc가 coroutines 1.8.x에 묶여 있는데 main 빌드만 Kotlin 2.1로 올린다거나, 반대로 Kotlin은 1.9에 그대로 두고 coroutines만 1.10으로 올리면, 묘한 컴파일 에러가 *어느 한 모듈*에서 갑자기 튀어나온다. coroutines와 Kotlin은 *세트로 움직이는 것이 좋다*고 기억해두자.

한 가지 별도로 짚어둘 자리가 있다. 1.11.0-rc01부터 Wasm/JS 측의 변경이 *breaking*이다. Promise 관련 함수가 `web` 타깃으로 옮겨졌고, Wasm/JS는 이제 `JsAny`의 서브타입만 허용한다. 이 두 줄이 별것 아닌 것처럼 들릴 수 있지만, Wasm/JS 코드를 가진 KMP 라이브러리 입장에서는 *공개 API 시그너처*가 흔들린다는 뜻이다. JsAny 서브타입 제약은 IDE 자동 변환으로는 해소가 어렵고, 사람이 한 번 읽고 결정해야 하는 자리가 많다. Wasm/JS 타깃을 켜둔 모듈이 있다면 9장 9.4 사다리의 2.2 → 2.3 칸 옆에 *별도 sub-task*로 올려두는 편이 낫다.

Compose Multiplatform 측은 흐름이 결을 같이한다. 2.0과 동시에 Compose 컴파일러 통합이 일어났고, 2.2.20에서 Wasm 타깃이 Beta로 승격됐고, 2.3에서는 Swift Export가 기본 활성화됐다. *Swift Export*는 Kotlin → Swift 직접 매핑 길이다. Objective-C 헤더를 우회해 enum이 진짜 Swift enum으로 매핑되고 variadic 인자가 자연스럽게 옮겨간다. 더불어 `linkRelease*` 빌드가 최대 40%까지 빨라진다는 보고가 있다. 다만 2.3 시점에서도 Experimental이라는 표시는 그대로다. iOS 진영에서는 Swift Export를 켜고 Objective-C 헤더 출력도 같이 두는 *이중 운영* 기간을 두는 편이 낫다. 어느 한쪽으로 단번에 옮기기에는 Swift 측 도구 체인이 아직 자리를 다 잡지 못했다.

## K2 IDE 경험 — 토글의 무게

여기서 잠깐 1장의 IDE K2 mode 토글을 다시 떠올려보자. IDEA 2024.2에서 K2 mode가 stable로 출시됐고, IDEA 2025.1에서는 *기본값*이 됐다. JetBrains 측 보고는 한 줄이다 — "1.8× faster code highlighting and 1.5× faster code completion on large codebases". 시니어 결정자에게 이 한 줄은 두 가지로 읽힌다.

첫째, *컴파일러와 IDE가 같은 FIR 위에서 같은 트리를 본다*는 사실이 마침내 IDE 사용자 경험으로 반영됐다. 1.x 시절에는 컴파일러는 K1, IDE 하이라이팅은 별개의 분석기였다. 두 분석기가 *서로 약간 다르게 보던* 시절의 사소한 빨간 줄·노란 줄들이 K2 모드에서는 일관된 한 가지로 정리된다. 둘째, *큰 코드베이스일수록 효과가 크다*. 작은 토이 프로젝트에서는 1.8배 가속의 체감이 적지만, 모듈 수십 개짜리 사내 빌드에서는 IDE를 켜자마자 차이가 보인다. 이 두 가지는 결정자에게 던질 만한 *조용한 무기*다. 9장 9.0 사전 점검 단계에서 IDE K2 mode를 켠 채 한 주를 보내고, 사내 시니어 두세 명에게 *체감*을 모아두자. 숫자보다 시니어의 한 마디가 도입 결정을 더 확실하게 끌어준다.

Lint 측 K2 적응도 같이 챙긴다. `gradle.properties`에 `android.lint.useK2Uast=true`를 두고, 더불어 `android.experimental.lint.version=8.5.0-alpha08` 같은 alpha 버전을 잠깐 시험해 보면 lint도 K2 UAST 위에서 돌기 시작한다. 이것은 단순한 속도 개선이 아니라 *컴파일러와 lint가 같은 트리를 보는* 자리를 만드는 일이다. Compose 사용 모듈이 많을수록 효과가 빠르게 드러난다. 다만 alpha 버전은 회사 메인 브랜치에 바로 박지 말고, 별도 *experiments* 브랜치에서 한 주쯤 묵혀 본 뒤 결정하는 편이 낫다.

### [박스 2] Apollo Kotlin / Anvil의 K2 도입기 — IR 의존 플러그인의 길

> 컴파일러 IR 백엔드에 의존하는 플러그인은 K2에서 한 번씩 *재공사*를 거쳤다. Slack 엔지니어 Zac Sweers의 *Preparing for K2* 글에서 가장 유명한 한 줄은 다음과 같다 — *"it will no longer run the compiler IR backend during stub generation, so any compiler plugins that depend on that (i.e. Anvil) will require changes."* 무슨 뜻일까. 1.x 시절 KAPT 같은 플러그인은 *stub generation* 단계에서 컴파일러 IR 백엔드를 한 번 더 돌려, 자기 코드를 거기에 끼워넣곤 했다. K2 위에서는 그 우회로가 닫힌다. Dagger Anvil처럼 그 우회로 위에 서 있던 플러그인은 *접근 경로 자체*를 다시 그려야 했다. Square 진영의 Anvil 후속 (anvil-ksp 흐름 등)은 그 재공사의 결과다.
>
> Apollo Kotlin은 결이 다른 도입기다. *Journey to K2: using the New Compiler in Apollo Kotlin*에서 그들이 강조한 것은 *측정*과 *단계적 활성*이다. K2를 켜기 전후의 빌드 시간, IDE 인덱싱 시간, 테스트 통과 시간 셋을 *자기 codebase 위에서* 잰 다음, 회귀가 보이는 모듈은 따로 빼서 `languageVersion = 1.9` 안전망을 일정 기간 유지했다. 이 두 사례에서 끌어올 수 있는 교훈은 두 줄이다. *컴파일러 플러그인 의존을 미리 점검하자*. 그리고 *자기 codebase 위에서 직접 측정하자*. 평균값으로 도입을 결정하지 말고, 우리의 분산을 우리가 손으로 잡자.

## 자기 생태계 진단 체크리스트 — 우리 조합은 어디인가

세 진영을 다 돌았으니, 이제 우리 회사의 *조합*으로 돌아오자. 결정의 부담을 줄이려면 우리가 어느 자리에 있는지 한 줄로 적을 수 있어야 한다. 다음 다섯 줄짜리 체크리스트를 펼쳐보자.

1. **서버 진영**. Spring Boot 모듈만 있는가, Ktor 모듈만 있는가, 둘 다 있는가. KMP 라이브러리 모듈이 Spring Boot Gradle plugin과 *같은 모듈*에 묶여 있는가, 아니면 별도 서브프로젝트인가.
2. **안드로이드 진영**. Compose 사용 모듈의 비중이 얼마나 되는가. `composeOptions { kotlinCompilerExtensionVersion = ... }` 블록이 사내에 *몇 군데* 남아 있는가. AGP 버전 분포는 7.x 잔재를 얼마나 끌고 있는가.
3. **KMP 진영**. iOS 타깃을 함께 끌고 있는가. macosX64/iosX64/tvosX64/watchosX64 같은 Intel 시뮬레이터 빌드가 CI에 박혀 있는가. Wasm/JS 타깃이 켜져 있는가.
4. **컴파일러 플러그인 진영**. Anvil, Apollo Kotlin, kotlinx-serialization, KSP, KAPT 중 어느 것이 빌드에 박혀 있는가. KAPT가 KSP로 옮길 수 있는 자리가 얼마나 남았는가.
5. **IDE / Lint 진영**. IDE K2 mode를 켜둔 시니어가 몇 명인가. `android.lint.useK2Uast=true`를 켜본 적이 있는가.

다섯 줄에 답을 적고 나면, 우리 회사의 기술 스택 *조합*이 한 문단으로 정리된다. 예를 들면 이렇다 — *"우리는 Spring Boot + Compose 안드로이드 + iOS KMP의 풀 스택 조합이고, AGP 8.x에 머물러 있으며, Anvil을 쓰는 모듈이 두 개 있다. Wasm/JS 타깃은 없고 IDE K2 mode는 시니어 세 명만 켜고 있다."* 이 한 문단은 9장 사다리에서 *어느 칸이 우리에게 가장 위험한지*를 곧장 짚어준다. 위 예시라면, 9장 9.0 사전 점검에서 Anvil 점검이 가장 위험한 자리가 되고, 9.4 단계에서 AGP 9.0 도약이 두 번째로 위험한 자리가 된다. 사다리 칸 옆에 *우리 조합 라벨*을 한 줄씩 붙여 두자. 라벨이 붙은 사다리는 단순한 시간 축이 아니라, *우리 회사의 의사결정 지도*가 된다.

조합 진단을 마쳤다면 마지막으로 한 가지를 더 점검하자. 우리 회사의 사례가 검색 가능한 자리에 *남아 있는가*. 한국 커뮤니티 자료를 모아 보면 velog와 Medium 한국어 진영의 1차 자료가 1.9 → 2.0 직후 시점의 정서를 잘 보여주지만, *2.2 → 2.3 시점*의 한국어 후기는 아직 얇다. 우리 회사가 그 자리를 한 칸 채워주면, 다음 결정자가 *"국내 대형사 사례 부재"*라는 한 줄에 막혀 결정을 미루는 일이 줄어든다. 이건 11장에서 한 번 더 호명할 화두지만, 10장의 마지막에 한 줄 미리 박아두자. *우리 회사의 적응 결과를 짧게라도 외부에 남기는 것*이 생태계 적응의 마지막 걸음이다.

## 마무리 — 분산이 진실이다

이 장에서 우리가 본 풍경은 한 줄로 요약된다. *생태계의 적응 속도는 한 가지가 아니다*. Spring Boot는 KMP와 만날 때 모듈 분리라는 한 줄을 요구하고, Compose는 1.5.14 호환 표를 내려놓고 plugin.compose 한 줄로 통합되며, KMP는 Kotlin 메이저 + 1쿼터의 시간 지도를 그리고, IDE는 K2 mode 토글 한 번에 1.8배 빨라진다. 어느 진영도 *2.x로의 이주가 한 번에 끝나는 점프*가 아니다. 모두 한 칸씩의 *생태계 적응 누적*이다.

조금 더 분명히 말하자. *분산이 진실*이라는 메시지는 9장 사다리에서 한 번 등장했지만, 10장에서 다시 한 번 호명할 가치가 있다. Anki에서 K2가 94% 빨라졌다는 보고와 Slack에서 17% 느려졌다는 보고가 *같은 컴파일러* 위에서 함께 나왔다. 그 차이를 만든 것은 컴파일러가 아니라 *그 코드베이스의 조합*이다. 우리 회사가 어떤 조합인지를 한 줄로 적어두지 않으면, 외부 평균값에 휘둘려 의사결정이 흔들린다. 반대로 우리 조합 한 문단이 손에 쥐어져 있으면, 어떤 외부 보고가 들어와도 *우리 자리에서 어떻게 읽힐 것인가*로 변환할 수 있다. 생태계 적응이라는 것은 결국, 외부 변화의 한 칸을 *우리 자리의 한 칸*으로 다시 쓰는 일이다.

11장에서는 이 누적의 끝에서 한 칸 더 나아간다. 2.3 Experimental 명단 중 어떤 항목이 2.4 Stable로 졸업할지, 그리고 우리 결정자에게 마지막 무기로 쥐여줄 *대체 자료*는 무엇인지를 다룬다. 그 전에, 이 장의 마지막 한 줄짜리 마이그레이션 노트를 적어두자.

> **마이그레이션 노트(1줄 액션):** 우리 회사 기술 스택 조합을 한 줄로 적은 뒤, 9장 9.0 ~ 9.4 사다리 옆에 그 조합에서 *가장 위험한 칸* 하나에 별표를 친다. 그리고 그 칸 위에 9.N 절 번호 라벨을 붙인다. 라벨이 붙은 사다리가 우리 회사의 *의사결정 지도*다.
