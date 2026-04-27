# 9장. 단계별 마이그레이션 플레이북 — 1.9에서 2.3까지 *네 번의 점검*

> 이 변화는 누적 캐스케이드의 *시간 순서로 묶기* 갈래에 속한다.

## 도입 — *한 번의 PR*에 다 옮기려다 망친 어느 금요일

금요일 오후, 누군가 의기양양하게 PR을 올린다. 제목은 *"chore: bump Kotlin 1.9.24 → 2.3.21"*. 본문은 두 줄이다 — *"한 방에 끝냈습니다. 빨간 줄 다 잡았어요."* 변경 파일이 110개. CI가 30분쯤 돌더니 빨간 X 하나만 남기고 멈춘다. 빌드 로그가 한 화면을 가득 채운다. 그 안에는 invokedynamic 람다 직렬화 회귀 한 줄, `kotlinOptions` 컴파일 에러 두 줄, context receivers 제거 다섯 줄, Apple `iosX64` 타깃 미지원 한 줄, 그리고 KSP 플러그인 호환 에러 두 줄이 *섞여서* 한꺼번에 떨어진다. 어디서부터 손대야 할지 가늠이 안 된다.

이 풍경을 한 번이라도 본 사람이라면 한 줄로 동의할 것이다. *섞인 빨간 줄은 디버깅이 안 된다.* 같은 PR에 2.0의 회귀, 2.2의 단절, 2.3의 제거가 한 번에 모이면, *어느 단계에서 무엇이 깨졌는지*가 영영 안 보인다. 끔찍한 일이다. 그래서 이 책은 1장 첫 단락부터 *시간 순서*를 흐트러뜨리지 말자고 약속해 왔다.

이 장은 그 약속을 *체크리스트의 모양*으로 바꾼다. 1.9 → 2.3을 한 번의 점프가 아니라 *네 번의 점검*으로 나누고, 각 점검의 *순서·시그널·롤백 안전망·완료 정의*를 한 페이지에 묶어 둔다. 코드 디테일은 굳이 다시 펼치지 않는다. 2장의 K2 컴파일 에러 4가지, 6장의 누적 deprecation 표, 7장의 context parameters 4가지 길은 이미 충분히 풀어 두었으니, 여기서는 그 페이지들에 *화살표*만 그어 둔다. 이 챕터의 미덕은 *압축*이다.

화두 셋을 들고 출발하자.

- 거대한 한 번의 마이그레이션 PR이 아니라, *네 번의 점검*으로 나누어 가는 길은 어떻게 생겼을까?
- 각 단계에서 *가장 먼저* 부딪히는 함정은 무엇이고, *가장 늦게* 드러나는 회귀는 무엇일까?
- 롤백 안전망을 어디에 깔아두면 *어느 단계에서든 후퇴*할 수 있을까?

## 9.0 사전 점검 — 점프하기 전에 한 시간만 들이자

본격적인 점프 전, 한 시간 정도 시간을 내서 *위치를 측정*하자. 이 한 시간이 다음 네 단계의 시간을 결정한다. Slack의 Zac Sweers가 *preparing-for-k2*에서 정리한 권고를 우리 한국 코드베이스에 맞춰 세 줄로 압축하면 이렇다.

첫째, **kapt 사용처를 목록으로 적는다**. `./gradlew :app:dependencies`나 빌드 스크립트 grep으로 충분하다. Glide·Dagger·Room·MapStruct가 보이면 가능한 한 *KSP*로 옮길 후보다. 옮기지 못하더라도 6장 박스에서 본 *K2 KAPT*가 2.1.20부터 기본값이 됐으니 일단 흘러가게 두고, 잔재만 메모해 두자.

둘째, **lint를 K2 UAST로 켜 본다**. `gradle.properties`에 한 줄.

```
android.lint.useK2Uast=true
```

이 한 줄을 켰을 때 lint가 깨지지 않는지가 K2 UAST 호환의 첫 시그널이다. 깨진다면 lint 룰 중 IR에 의존하는 자리가 있다는 뜻이고, 우리가 9.1로 넘어가기 전에 정리해야 할 짐 한 자루가 더 생긴 것이다.

셋째, **컴파일러 IR에 의존하는 플러그인 목록을 본다**. Anvil이 대표적이다. Sweers의 한 줄을 그대로 옮겨 두자 — *"it will no longer run the compiler IR backend during stub generation, so any compiler plugins that depend on that (i.e. Anvil) will require changes."* 우리 빌드에 Anvil이 살아 있다면 K2 호환 버전을 미리 확인하고, 호환 버전이 없으면 *옮기는 시점*을 별도로 잡는다.

이 셋을 *한 페이지 메모장*에 적으면 사전 점검은 끝이다. 1장 끝의 *측정 baseline*(컴파일 시간, 의존 라이브러리, kapt/KSP 사용처)이 이미 모여 있다면, 거기에 위 세 줄을 더하면 된다. **사전 점검의 완료 정의**는 단순하다 — *clean build green + lint K2 UAST green + IR 의존 플러그인 K2 호환 매트릭스 통과.* 이 셋이 초록불이면 9.1로 넘어가도 좋다.

## 9.1 1.9 → 2.0 — 가장 길지만, 가장 *예측 가능한* 단계

첫 번째 점프는 *가장 손이 많이 가는* 단계지만, 동시에 *가장 예측 가능한* 단계이기도 하다. JetBrains가 8만 프로젝트로 검증한 그 컴파일러를 켜는 일이고, 한국·해외 후기가 가장 많이 쌓여 있는 분기다.

**순서**는 이렇다. 빌드 스크립트 → 컴파일 에러 흡수 → 회귀 점검 순으로 간다.

1. `kotlin = "2.0.x"`로 버전을 올린다 (가능하면 2.0.21처럼 한두 패치 안정화된 자리). `.gitignore`에 `.kotlin/`을 추가한다 — 빌드 산출 디렉터리가 `.gradle/kotlin/`에서 `.kotlin/`으로 옮겨졌다.
2. `kotlinOptions { }`를 `compilerOptions { }`로 옮긴다. 이 시점엔 deprecated 경고일 뿐이지만, *2.2에서 컴파일 에러가 되는 자리*를 미리 정리하는 편이 낫다. 6장에서 이미 한 번 풀었다.
3. Compose 모듈은 `composeOptions { kotlinCompilerExtensionVersion = ... }`을 지우고 `kotlin("plugin.compose") version <kotlin>`으로 옮긴다. 자세한 모양은 10장에서 한 페이지로 다시 본다.
4. 2장의 *K2가 새로 거르는* 4가지 컴파일 에러를 흡수한다 — open property 즉시 초기화, star-projected setter, Java `int @Nullable []`, smart cast 정합성. 나머지 3가지는 부록 A 표에서 한 번에.

**가장 먼저 부딪히는 함정**은 늘 같다. 사내 buildSrc / convention plugin 한 곳이 *옛 DSL을 들고 있어서* 모든 모듈을 함께 멈춰 세우는 자리다. 한국 후기에서도 *"convention 스크립트 한 줄 때문에 한나절 날렸다"*가 가장 자주 등장하는 한 줄이다. 빌드 스크립트는 *본문보다 한 분기 일찍* 옮긴다는 6장의 시차 전략이 여기서 그대로 적용된다.

**가장 늦게 드러나는 회귀**는 invokedynamic 람다 직렬화다. 빌드는 통과하고 테스트도 한참 통과하다가, 어느 날 운영의 이벤트 소싱 큐가 *"Illegal state change detected"*라며 시끄러워진다. 한 번도 본 적 없는 메시지다. 9장 끝의 *공통 회귀 사례*에서 다시 본다.

**롤백 안전망**은 한 줄이다.

```kotlin
kotlin {
    compilerOptions {
        languageVersion.set(KotlinVersion.KOTLIN_1_9)
        apiVersion.set(KotlinVersion.KOTLIN_1_9)
    }
}
```

컴파일러는 K2를 쓰되 언어 시맨틱만 1.9에 묶어 둔다. 빌드 스크립트의 deprecation은 막지 못한다는 6장의 한계를 잊지 말자.

**완료 정의 (Definition of Done)** — *clean build green + 핵심 모듈 incremental green + invokedynamic 회귀 시그널 부재(이벤트 소싱·직렬화·QA 스모크 통과)*. 이 셋이 *연속 3일* 초록색이면 9.2로 넘어간다. 한두 번 초록이고 끝낼 일이 아니다. 회귀의 절반은 *셋째 날 아침*에 드러난다.

## 9.2 2.0 → 2.1 — 가장 *조용한* 단계, 그래서 위험하다

두 번째 점프는 풍경이 사뭇 다르다. 빌드 스크립트의 큰 단절은 없다. *조용히* 새 경고가 늘어나고, *조용히* 새 Preview 카드가 손에 쥐어진다. 그래서 오히려 위험하다 — 조용한 분기는 *기록이 남지 않는* 분기고, 9.3의 빨간 줄을 미리 예열할 자리이기도 하다.

**순서**는 이렇다.

1. `extraWarnings.set(true)` 한 줄을 켠다. `REDUNDANT_NULLABLE`, `CAN_BE_VAL`, `UNREACHABLE_CODE` 같은 새 경고가 빌드 로그에 흐른다. 이 경고들의 *목록*을 사내 위키에 박아 두자. 다음 점프에서 빨간 줄이 될 후보 목록이다.
2. K2 KAPT alpha를 *옵트인*으로 시도해 본다. `kapt.use.k2=true`. 2.1에서는 alpha니까 사이드 모듈 한 곳에 먼저 켜고, 빌드 리포트의 KAPT 단계 시간을 그래프로 한 번 그려 보자. 동작에 미세 차이가 보이면 6장 박스의 *K2 KAPT* 절을 다시 펼친다.
3. 3장의 smart cast 강화로 *죽은 분기*가 된 코드를 정리한다. `else throw IllegalState(...)`로 도배돼 있던 sealed `when`이 똑똑해진 exhaustiveness 덕에 *그 한 줄이 더 이상 필요 없는* 자리가 생긴다. IDE 인스펙션을 모듈 단위로 한 번 돌리면 큰 묶음이 한꺼번에 빠진다.
4. 4장의 세 카드(guard `when`·multi-dollar·non-local break/continue)를 *어디까지 들일지* 결정한다. 프로덕션·사이드·라이브러리 중 어디에 opt-in 플래그를 박을지 선을 그어 두자. 2.2 Stable 졸업까지 한 분기다.

**가장 먼저 부딪히는 함정**은 사실 함정이라기보다 *유혹*이다. 새 카드 셋이 너무 깔끔해 보여서 한 번에 다 들이고 싶어진다. 권하는 길은 한 모듈에만 좁혀 들이는 것이다. 사이드 모듈 한 곳에서 한 분기 굴리고, 2.2 Stable로 졸업한 뒤에 프로덕션으로 옮긴다. *Preview는 회의실 발표용이 아니라 사이드 프로젝트용이다*.

**가장 늦게 드러나는 회귀**는 KAPT4의 미세한 동작 차이다. 어노테이션 프로세서가 PSI를 우회하던 자리, Kotlin 메타데이터를 직접 추출하던 자리에서 *동등하지만 동일하지 않은* 동작이 한두 줄 보고된다.

**롤백 안전망**은 *한 모듈씩* 켰다 끄는 단순함이다. K2 KAPT는 `kapt.use.k2=false` 한 줄로 K1으로 돌릴 수 있고, Preview 플래그는 `freeCompilerArgs`에서 한 줄 빼면 끝이다.

**완료 정의** — *warning 수가 baseline 대비 ±10% 이내로 안정화 + 사이드 모듈에서 K2 KAPT alpha green*. 경고 수가 *늘어나는* 쪽은 우리가 정리해야 할 자리이고, *줄어드는* 쪽은 K2가 우리 코드를 더 똑똑하게 본 자리다. 안정화의 의미는 *어느 쪽이든 변화가 잦아드는 시점*이다.

## 9.3 2.1 → 2.2 — 책 전체에서 *가장 위험한* 단계

세 번째 점프가 이 책 전체에서 *가장 무거운 한 분기*다. 6장의 누적 deprecation 표를 다시 펼쳐 두고 가자.

| 항목 | 1.9 | 2.0 | 2.1 | **2.2** | 2.3 |
|---|---|---|---|---|---|
| `kotlinOptions { }` | warn | warn | warn | **error** | error |
| `kotlin-android-extensions` | warn | warn | warn | **removed** | removed |
| Apple `ios()`/`watchos()` 단축형 | warn | warn | error | **removed** | removed |
| `KotlinCompilation.source(...)` | warn | error | error | error | **removed (2.3)** |
| `-language-version=1.6 / 1.7` | ok | ok | warn | **error** | error |
| `kapt.use.k2` 토글 | — | — | alpha | default → **deprec (2.2.20)** | deprec |

**2.2 열에 굵은 글씨가 가장 많다**는 사실이 한눈에 들어올 것이다. 6장에서 *동기화된 deprecation*이라고 부른 다섯 항목이 한 분기에 일제히 떨어진다. 한 번에 같이 손대지 않으면 한 번에 같이 멈춘다.

**순서**는 신중하게 가야 한다.

1. `kotlinOptions { }` 잔존을 *모두* 정리한다. buildSrc, convention plugin, Maven publish 스크립트, 자동 생성 빌드 스니펫까지. `git grep "kotlinOptions"`로 한 번 훑고, *남은 자리가 0이 될 때까지* 다음 단계로 가지 말자. 6장에서 본 그 한 줄짜리 치환이 자리마다 들어간다.
2. context receivers를 context parameters로 옮긴다. 7장의 4가지 길 — IDE 인스펙션, 이름 부여, 단순 파라미터 강등, extension 강등 — 을 모듈 성격에 맞춰 고른다. 라이브러리라면 *dual API*를 한 메이저 사이클만 끌고 가는 결정도 같이 한다.
3. `kotlin-android-extensions` 잔재를 제거하고 `kotlin-parcelize` + view binding으로 옮긴다.
4. Apple 단축형(`ios()`, `watchos()`, `tvos()`)을 명시 타깃(`iosArm64()`, `iosSimulatorArm64()` 등)으로 풀어 적는다.
5. `KotlinCompilation.source(...)` 사용처를 `defaultSourceSet.dependsOn(...)`로 옮긴다 — 대부분의 자리는 *그냥 지우면 되는* 자리다.
6. JVM default method 변화를 점검한다. 인터페이스 default가 진짜 JVM default로 컴파일된다. Java에서 우리 라이브러리를 쓰는 사용자 베이스가 있다면 `JvmDefaultMode.NO_COMPATIBILITY` 또는 `enable` 중 한쪽으로 *결정*해야 한다.
7. KAPT4가 디폴트로 굳었다는 사실을 *공식적으로* 인정한다. 2.2.20부터 `kapt.use.k2` 프로퍼티 자체가 deprecated다. 토글 자체를 빌드 스크립트에서 지우자.

**가장 먼저 부딪히는 함정**은 1번이다. `kotlinOptions { }`가 *어디 한 군데* 살아 있으면 그 모듈의 빌드 자체가 멈춘다. *모든* 자리를 정리해야 다음으로 갈 수 있다. **가장 늦게 드러나는 회귀**는 6번이다. JVM default method가 진짜 default로 컴파일되면, 우리 라이브러리를 옛 컴파일러로 빌드한 *Java 사용자*의 호출이 미묘하게 깨지는 사례가 있다. 라이브러리 운영자라면 이 한 줄을 PR 본문에 명시하자.

**롤백 안전망**의 한계가 가장 분명한 분기다. `languageVersion = 1.9`는 코드 시맨틱만 묶어 줄 뿐, 빌드 스크립트의 *깔끔한 단절*은 막지 못한다. 6장에서 짚은 *시차 전략*이 유일한 답이다 — 빌드 스크립트는 9.2 단계에서 *이미* 2.2 모양으로 다듬어져 있어야 한다.

**완료 정의** — *6장 누적 deprecation 표의 모든 error 칸이 해소 + dual API 라이브러리 시점 결정 PR 머지 + K2 KAPT 디폴트 전환 후 핵심 모듈 빌드 시간 baseline ±10%*. 이 셋이 모이면 9.4로 넘어가도 좋다.

## 9.4 2.2 → 2.3 — *마지막* 정리, 그리고 미래로 이어지는 다리

네 번째 점프는 풍경이 한결 가볍다. 큰 단절은 9.3에서 이미 끝났고, 9.4는 *마지막 잔재 정리*와 *2.4를 향한 다리 놓기*다.

**순서**는 이렇다.

1. `-language-version=1.8` 사용처를 종료한다. *비-JVM 타깃*에서는 `1.9`도 더 이상 안 된다. KMP common 모듈이 옛 language version을 들고 있는지 한 번 더 확인한다.
2. Apple 최소 OS를 상향한다 — iOS/tvOS 12 → 14, watchOS 5 → 7. 한국 사용자 베이스에 iOS 13이 비무시할 수준으로 남아 있다면 *비즈니스 결정*이 필요한 자리다. `-Xoverride-konan-properties=minVersion.ios=12.0` 같은 override는 *한시적* 안전망으로만 두자.
3. Intel Mac 시뮬레이터 빌드(macosX64/iosX64/tvosX64/watchosX64)를 정리한다. 2.4에서 *제거 예정*이다. CI를 Apple Silicon 우선으로 재구성한다.
4. Compose stack trace mapping을 켠다. R8 minify 환경에서 Compose 그룹 키와 ProGuard 매핑이 결합되며 *진짜 디버깅 가능한* 스택 트레이스가 떨어진다. Compose runtime 1.10 이상이 필요하다.

   ```kotlin
   Composer.setDiagnosticStackTraceMode(ComposeStackTraceMode.GroupKeys)
   ```

5. 5장의 새 stdlib API를 *후보 모듈에 좁게* 들인다 — `Clock.System.now()`, `Uuid.generateV7()`, `kotlin.concurrent.atomics`. Experimental 마크가 붙은 자리는 한 모듈 단위 opt-in으로 제한한다.
6. AGP 9.0+로 이주한다. `org.jetbrains.kotlin.android` 플러그인이 *빌트인*으로 흡수되니까, 빌드 스크립트에서 그 한 줄을 지우는 일이 마지막 정리다. *before/after* 모양은 10장에서 한 페이지로 본다.

**가장 먼저 부딪히는 함정**은 2번 — Apple 최소 OS 상향 결정이다. 기술 결정이 아니라 *비즈니스 결정*이라는 점을 인정하고, 한국 시장의 사용자 베이스 통계를 들고 회의실로 들어가자. **가장 늦게 드러나는 회귀**는 1번 — `-language-version=1.8` 잔재가 KMP common이나 라이브러리 모듈에 살아 있어, 한 분기 뒤 다른 모듈에서 *원인 모를 빨간 줄*로 돌아오는 자리다.

**롤백 안전망**은 *모듈 단위 opt-in 격리*다. Experimental stdlib API는 한 모듈에서만 쓰고, 그 모듈의 `@OptIn`이 다른 모듈로 새지 않게 막는다. 이 한 줄짜리 격리가 다음 메이저(2.4)에서 안전망 역할을 한다.

**완료 정의** — *`kotlin.experimental.tryNext=true`로 2.4-EAP 프리뷰까지 빌드 통과 + Apple Silicon CI green + Compose stack trace 표본 한 건 캡처*. 마지막 한 줄은 *새 능력을 한 번이라도 써 봤다*는 의미다. 도구를 받아 두고 안 쓰면 도구가 아니다.

## 공통 회귀 5가지 — *어느 단계에서든* 튀어나오는 자리

네 단계를 차례로 짚어도 *예외처럼* 튀어나오는 회귀가 다섯 가지 있다. 단계와 무관하게 *증상의 모양*으로 알아채는 편이 빠르니, 한 번에 묶어 적어 두자.

**(a) 이벤트 소싱 람다 직렬화 깨짐.** 증상은 *"Illegal state change detected! Property has different value when sourcing events."* 한 줄이다. 원인은 2.0의 lambda → invokedynamic 기본 변환. 직렬화가 필요한 람다 한 줄에 `@JvmSerializableLambda`를 붙이거나, 모듈 단위로 `-Xlambdas=class`를 박는다.

```kotlin
class Aggregate {
    @JvmSerializableLambda
    val onEvent: (Event) -> Unit = { ev -> apply(ev) }
}
```

**(b) JUnit 5 백틱 한국어 메서드명 + 람다 명명 path overflow.** 증상은 `FileNotFoundException: The system cannot find the file specified.`. 원인은 K2가 람다를 `$lambda$30` 같은 이름으로 명명하면서, 한국어 백틱 메서드명과 합쳐져 *파일 시스템 경로 한도*를 넘는 자리다. 메서드명을 짧게 줄이거나 `@Nested` depth를 한 단계 낮춘다. 한국어 테스트명을 즐겨 쓰는 한국 팀에서 유난히 잘 보이는 자리다.

**(c) Apple iOS framework 캐싱 stale.** 증상은 *"Module compiled with Kotlin x.x.x cannot be read"*. 원인은 1.9.2x ↔ 2.0 사이 버전 변경 시 Xcode 캐시가 stale로 남는 자리. 한 번씩 청소하자.

```bash
./gradlew clean
# 그리고 Xcode → Product → Clean Build Folder (Shift+Cmd+K)
```

**(d) kotlinx-serialization + invokedynamic 람다 직렬화 회귀.** (a)와 비슷해 보이지만 결이 한 겹 다르다. `kotlinx-serialization` 컴파일러 플러그인과 invokedynamic 람다 변환이 *같이* 얽힐 때, ABI가 미묘하게 어긋나며 직렬화 산출물이 깨진다. 증상은 `SerializationException: Polymorphic serializer was not found for class …` 또는 *직렬화는 통과하지만 역직렬화에서 필드가 비는* 자리다. 응급 처치는 두 갈래다 — `kotlinx-serialization`을 Kotlin 메이저에 맞춰 함께 올리고(메이저 + 1쿼터 호흡 기억), 직렬화 대상 클래스의 람다 필드에 `@JvmSerializableLambda`를 붙인다. 둘 다 안 되면 모듈 단위 `-Xlambdas=class`로 invokedynamic 변환을 끈다. 이 회귀는 9.1 분기에 가장 자주 보이지만, 9.3에서 컴파일러 플러그인 버전을 같이 올리지 않으면 *그때 다시* 돌아온다.

**(e) buildSrc + Gradle 8.3 미만 호환.** 증상은 `Could not load script 'buildSrc/build.gradle.kts'` 또는 의존성 해소 실패. 원인은 Kotlin 2.0이 buildSrc 의존이 있는 프로젝트에서 *Gradle 8.3 이상*을 요구하는 자리. 회피책은 두 갈래 — Gradle을 8.3+로 올리거나, 임시로 `compilerOptions { languageVersion.set(KotlinVersion.KOTLIN_1_9) }` 안전망을 켜고 한 분기를 산다. 안전망은 *기한*을 함께 적어 두자.

이 다섯 자리는 *어느 단계의 잘못도 아닌* 자리다. 우리 코드가 다섯 가지 함정에 *동시에* 걸리지 않게, 단계마다 한 번씩 이 목록을 펼쳐 두는 편이 낫다.

## build.gradle.kts *full diff* — 1.9 시절에서 2.3 시점으로

이 챕터의 정수가 여기 있다. 같은 안드로이드 + KMP 모듈의 build.gradle.kts를 *1.9 시절의 한 파일*과 *2.3 시점의 한 파일*로 나란히 두자. 위 다섯 항목과 다섯 회귀가 *한 파일의 어느 줄에 모이는지*가 한눈에 보인다.

```kotlin
// === 1.9 시절 ===========================================================
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android") version "1.9.24"
    id("kotlin-android-extensions")           // (1) 2.2 removed
    id("kotlin-kapt")
}

android {
    namespace = "com.example.app"
    compileSdk = 34

    kotlinOptions {                           // (2) 2.2 컴파일 에러
        jvmTarget = "17"
        freeCompilerArgs += listOf(
            "-Xjsr305=strict",
            "-Xcontext-receivers",            // (3) 2.3 제거
        )
    }

    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.14"   // (4) 2.0+ 별도 plugin
    }
}

kotlin {
    ios()                                     // (5) 2.2 removed
    watchos()
    tvos()

    sourceSets {
        targets.all {
            compilations.named("main") {
                source(sourceSets["commonMain"])  // (6) 2.3 removed
            }
        }
    }
}

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.5.0") // (7) 2.3 stdlib
    implementation("commons-codec:commons-codec:1.16.0")          // (8) 2.2 stdlib Base64
    kapt("com.google.dagger:hilt-compiler:2.50")                  // (9) KSP 권고
}
```

같은 파일을 2.3 시점으로 옮기면 이렇다. 늘어난 줄보다 *지워진 줄*이 더 많다는 사실이 한눈에 들어온다.

```kotlin
// === 2.3 시점 ===========================================================
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.android.application)
    // alias(libs.plugins.kotlin.android)              // ← AGP 9.0+ 빌트인 흡수
    alias(libs.plugins.kotlin.parcelize)               // (1) android-extensions 대체
    alias(libs.plugins.compose.compiler)               // (4) Compose 컴파일러 통합
    alias(libs.plugins.ksp)                            // (9) kapt → KSP
}

android {
    namespace = "com.example.app"
    compileSdk = 36
}

kotlin {
    compilerOptions {                                  // (2) compilerOptions로 이주
        jvmTarget.set(JvmTarget.JVM_17)
        freeCompilerArgs.addAll(
            "-Xjsr305=strict",
            "-Xcontext-parameters",                    // (3) 후속 받침대
        )
    }

    iosArm64()                                         // (5) 명시 타깃
    iosSimulatorArm64()
    watchosArm64()
    watchosSimulatorArm64()
    tvosArm64()
    tvosSimulatorArm64()
    // sourceSets는 기본 토폴로지에 맡긴다 (6: dependsOn 명시 불필요)
}

composeCompiler {
    featureFlags = setOf(
        ComposeFeatureFlag.OptimizeNonSkippingGroups,
    )
}

dependencies {
    // implementation("org.jetbrains.kotlinx:kotlinx-datetime:…")  // (7) 표준 흡수
    // implementation("commons-codec:commons-codec:…")             // (8) 표준 흡수
    ksp(libs.hilt.compiler)                                       // (9) KSP 디폴트
}
```

`gradle.properties`에 한 줄을 더 깔아 두자.

```
# .gitignore에는 .kotlin/ 추가
android.lint.useK2Uast=true
# kapt.use.k2 토글은 2.2.20부터 deprecated — 줄 자체를 둘 필요 없음
```

같은 파일이 *9줄 짧아졌고*, 외부 의존이 *두 줄 사라졌다*. 한 화면으로 내려오는 가독성은 덤이다. 이 *한 페이지*가 9장의 정수다. 사내 위키 첫 페이지에 박아 두자. 누군가 사내 convention plugin에 한 줄을 더할 때, 이 한 페이지가 옆에 펼쳐져 있으면 *그 한 줄이 어느 시점에 빨갛게 변할지*를 PR 단계에서 가늠할 수 있다. 우리 사내의 짧은 합의문이 한 페이지로 정리되는 셈이다.

## 닫는 단락 — 네 번의 점검을 마쳤을 때의 풍경

네 번의 점검을 모두 마치고 나면, 책 첫 장의 그 *난감한 월요일*이 다른 모양으로 찾아온다. CI는 여전히 가끔 빨간색을 띄우지만, 그 빨간 줄은 *하나의 단계*에서 온다. 9.1의 회귀와 9.3의 단절이 *한 빌드에 섞여 떨어지는* 일은 더는 일어나지 않는다. 같은 빨간 줄이 *예상 가능한 표지판*으로 바뀐 풍경이다.

이 변화의 진짜 가치는 *속도*가 아니라 *예측 가능성*이다. 다음 마이너 버전이 나왔을 때, 우리는 이미 *9.0의 사전 점검 메모장*을 다시 펼치고 *9.1의 빌드 스크립트 정리 → 9.2의 조용한 분기 → 9.3의 위험한 단절 → 9.4의 마지막 다리* 패턴을 익혀 두었다. 같은 골격이 2.4·2.5에도 그대로 들어맞는다. JetBrains의 *Preview → Stable* 시간 지도가 패턴이라면, 우리의 *네 번의 점검*도 패턴이다. 한 번 익힌 패턴은 다음 분기에서 *한 시간*을 절약한다.

마지막으로 한 줄을 청유로 남기자. 지금까지 우리가 본 *순서·시그널·롤백·완료 정의*를 사내 위키 한 페이지에 옮겨 적자. 위 build.gradle.kts *full diff*를 그대로 붙여 넣고, 단계마다 *우리 코드베이스에서 손볼 자리*에 굵은 표시를 더하자. 이 한 페이지가 다음 분기에 우리를 한 번 더 살린다. 한 번에 다 옮기려 하지 말고, *네 번의 점검*으로 나누어 함께 건너가 보자.

다음 장에서는 이 플레이북을 *생태계 좌표*에 비춰 본다. Spring Boot Gradle plugin이 KMP 모듈에 닿는 순간, AGP 9.0이 `org.jetbrains.kotlin.android`를 빌트인으로 흡수하는 순간, Compose 컴파일러가 Kotlin과 *같은 버전*으로 묶이는 순간 — 우리 사내 빌드가 어느 *조합*에 속하는지가 풍경을 다시 한번 바꾼다.

---

> **마이그레이션 노트** — 이 챕터 자체가 종합본이다. *내일 아침 첫 commit*으로 무엇을 할지 한 페이지 액션 리스트는 **부록 A** 참조.
