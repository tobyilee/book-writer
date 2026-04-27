# 6장. 컴파일 에러로 변한 deprecation들 — kotlinOptions의 마지막 1년

> 이 변화는 누적 캐스케이드의 *비싸게 치러야 하는 것* 갈래에 속한다.

월요일 아침, 출근해서 커피 한 잔을 내리고 자리에 앉는다. 금요일까지만 해도 초록불이 떨어지던 빌드다. 주말 동안 누군가 사내 convention plugin의 Kotlin 버전을 2.1.x에서 2.2.x로 살짝 올려 두고 갔다. PR 본문은 *"Kotlin 패치 업데이트, 별 변화 없음"* 정도. 그런데 빌드 로그에 빨간 줄이 빼곡하다. 어제까지 *deprecated 경고*로 노랗게 흐려져 있던 한 줄이 오늘은 단호한 컴파일 에러다.

```text
e: file:///.../build.gradle.kts:42 'kotlinOptions' is deprecated. ...
   Cannot access script base class.
```

화면 가득히 같은 메시지가 모듈마다 도배돼 있다. 빌드는 한 줄도 진행되지 못한다. 어제까지 *경고*였던 줄이 오늘은 *에러*가 됐다는 말은, 어젯밤과 오늘 아침 사이에 우리가 무언가 *놓쳤다*는 뜻이다. 사내 convention plugin은 사내 라이브러리 팀이 손대는 자리이고, 그 팀이 latest Kotlin 변화를 한 분기씩 늦게 따라가는 일이 드물지 않다. 다른 사람의 한 줄 PR이 우리 모든 모듈의 빌드를 한 번에 멈춰 세운다. 끔찍한 일이다.

이 풍경에서 정말 난감한 점은 *우리 코드 본문은 한 글자도 바뀌지 않았다*는 사실이다. 도메인 로직은 그대로다. 테스트 코드도 그대로다. 한 줄 PR이 들어온 자리는 우리가 평소 거의 들여다보지 않는 *빌드 스크립트*다. 그런데 빌드 스크립트의 한 줄이 우리 모든 모듈의 *컴파일* 자체를 가로막고 있다. 빨간 줄을 따라 들어가도 *우리가 짠 코드*가 아니라 *남이 짠 빌드 로직*이 보인다. 어디서부터 손대야 할지 가늠하기 어렵다. 찜찜하다.

이 장에서는 그 끔찍함을 *왜 미리 못 잡았는가*의 시선으로 들여다보고 싶다. 화두는 세 가지다.

첫째, 어제까지 경고였던 `kotlinOptions { }`가 오늘은 빨간 줄을 그어 버린다면, 그 1년 사이에 무슨 일이 있었나. 둘째, Kotlin은 보통 deprecation을 2년 이상 끄는데, 왜 이 항목은 이렇게 빠르게 에러로 갔을까. 셋째, `kotlin-android-extensions`와 `withJava()`처럼 비슷한 운명을 따라간 *동기화된 deprecation*들은 또 무엇일까.

세 질문을 차례로 따라가 보자.

## kotlinOptions의 1년 — 경고에서 에러까지의 시간표

먼저 시간을 좀 거슬러 가 보자. `kotlinOptions { }`라는 DSL은 우리 모두에게 익숙하다. Android Gradle plugin과 함께 Kotlin을 도입한 이후로, build.gradle 어디를 펼쳐도 한 번쯤은 본 블록이다.

```kotlin
// 1.9 시절의 익숙한 풍경
android {
    kotlinOptions {
        jvmTarget = "17"
        freeCompilerArgs += "-Xjsr305=strict"
    }
}
```

이 블록은 사실 1.9 시점에 이미 *deprecated* 표시가 붙어 있었다. IDE에서 보면 옅은 줄이 그어진 상태다. JetBrains의 권고는 이전부터 분명했다. 같은 설정을 `compilerOptions { }`라는 새 DSL로 옮기라는 것이다.

```kotlin
// 2.0 이후 권장되는 모양
android {
    kotlin {
        compilerOptions {
            jvmTarget.set(JvmTarget.JVM_17)
            freeCompilerArgs.add("-Xjsr305=strict")
        }
    }
}
```

같은 일을 하는 두 DSL이라면 *왜 굳이 옮기라고 하는가* 의문이 들 수 있다. 답은 두 줄로 요약된다. 첫째, `kotlinOptions`는 Android Gradle plugin이 들고 있는 별도 확장이라 *KMP나 JVM-only 모듈*에서는 일관되게 쓰이지 못했다. 둘째, 새 DSL은 Kotlin Gradle Plugin(KGP)이 직접 노출하는 *프로퍼티 기반* 인터페이스라 KMP common 모듈과 platform별 모듈에 같은 모양으로 들어간다. 이 두 가지가 *FIR로 정렬된 K2*라는 큰 그림과 결을 같이한다. 한 컴파일러가 모든 타깃을 본다면, 빌드 스크립트의 컴파일러 설정도 *한 모양*이어야 어색하지 않다.

여기까지가 *왜*에 대한 답이다. 그렇다면 *시간표*는 어떻게 흘렀나. 1년 사이의 풍경을 시간 순으로 쥐어 보자.

- **1.9** — `kotlinOptions { }`는 deprecated. IDE에 옅은 줄이 그어지지만 빌드는 통과한다. 노란 경고 한 줄이 깜빡일 뿐이다.
- **2.0 (2024-05)** — 그대로 deprecated 경고. 권장 마이그레이션은 `compilerOptions { }`. JetBrains는 *"마이그레이션을 시작하라"* 고 권하는 정도다.
- **2.1 (2024-11)** — 여전히 deprecated 경고. 마지막으로 *경고로 살아남는 한 분기*다. 이 시점에 사내에서 잔재를 정리하지 않으면 다음 점프에서 발이 묶인다.
- **2.2 (2025-여름)** — *컴파일 에러*. 빌드가 멈춘다. `compilerOptions { }`로 옮기지 않은 모든 모듈은 단 한 줄도 진행되지 못한다.

deprecated가 깜빡이기 시작한 건 1.9 이전이지만, *경고에서 에러로 넘어가는 사다리*는 2.1과 2.2 사이의 약 *1년*에 압축돼 있다. 보통 Kotlin은 deprecation을 *2년 이상* 끌고 가는 편이다. context receivers는 2.0.20에 deprecation이 시작됐는데 제거는 2.3에서 예정돼 있다. `KotlinCompilation.source(...)`는 2.0에 error 처리됐지만 *removed*는 2.3까지 미뤄졌다. 이 평소의 호흡에 비하면 `kotlinOptions`의 1년은 *유난히 짧다*.

왜일까. 두 가지 이유가 같이 작용한 것으로 보인다. 하나, `kotlinOptions`는 *완전한 대체 DSL*이 이미 존재했다는 점이다. `compilerOptions { }`는 새 문법이라기보다 *새 인터페이스*에 가까웠고, 옮길 때 잃는 표현력이 사실상 없었다. 둘, AGP·KGP·KMP 세 축이 *동시에* 새 DSL을 권하고 있었기 때문에 두 DSL이 공존하는 기간이 길수록 *사내 가이드의 분열*이 커지는 자리였다. JetBrains 입장에서는 *깔끔한 단절* 한 번이 더 나은 선택이었던 셈이다.

문제는 이 1년이 *모두에게 충분한 1년*이 아니었다는 점이다. 우리가 직접 짠 build.gradle은 보통 빠르게 따라갈 수 있다. 하지만 사내 buildSrc, 사내 convention plugin, 사내 Maven publish 스크립트 — 이 *공유된 빌드 로직*은 한 사람이 손대지 않는 자리다. 한 사람이 손대지 않는 자리는 *경고를 경고로 그냥 두는* 자리다. 빌드 로그의 노란 한 줄을 매일 보다 보면 어느 순간 그 노란색 자체가 풍경이 된다. 그러다 어느 월요일, 그 풍경이 일제히 빨간색으로 바뀌어 있다.

조금 더 구체적으로 들여다보자. 사내 convention plugin이라고 부르는 자리는 보통 이런 모양이다. `buildSrc/src/main/kotlin/MyKotlinJvmConventions.kt` 같은 파일에 *공통 컴파일 옵션*을 한 곳에 모아 두고, 모든 모듈이 `plugins { id("my-kotlin-jvm-conventions") }` 한 줄로 그 설정을 끌어 쓴다. 이 패턴 자체는 좋은 설계다. 한 곳을 손보면 모든 모듈에 일관되게 반영된다. 다만 이 좋은 설계의 *반대편*에는 한 가지 위험이 있다. 그 한 곳에 박힌 `kotlinOptions { jvmTarget = "17" }` 한 줄이 *모든 모듈의 운명을 같이 묶는다*. 한 곳이 빨갛게 변하는 순간, 모든 모듈이 한 번에 멈춘다.

이 사례에서 우리가 챙겨 둘 교훈은 분명하다. *deprecated 경고는 그냥 경고가 아니라 일정이 정해진 알림*이다. 알림을 받으면 다이어리에 *언제까지*를 적어 두는 편이 낫다. 각 항목의 *예상 error 분기점*을 미리 메모해 두지 않으면, 그 분기점이 우리 분기점이 된다.

이쯤 되면 누군가는 한 줄 더 묻고 싶을 것이다. *우리 프로젝트는 buildSrc까지 다 손에 쥐고 있는데*, 그래도 안전한가. 사실 이 질문에 한 번에 답하는 길은 한 줄이다. CI에 `--warning-mode=fail`을 박아 두는 것이다. Gradle의 이 옵션은 deprecated 경고가 한 줄이라도 떨어지면 빌드를 *깨뜨린다*. 평소 우리 빌드가 깨지면 안 되니까 이 옵션은 *모니터링용 잡*에만 따로 둬도 좋다. 하루에 한 번 야간에 도는 그 잡이 빨간색을 띄우는 날, 우리는 *경고가 경고일 때* 그것을 발견한다. 자세한 운용은 9장 9.3절에서 다시 짜 두기로 하자.

여기까지가 첫 화두에 대한 답이다. *1년 사이에 무슨 일이 있었나* — 두 DSL의 정렬을 위해 JetBrains가 *짧은 단절*을 택했고, 우리 사내 빌드 로직은 그 단절을 따라가지 못했을 때 한 번에 멈춘다. *왜 이렇게 빠르게 에러로 갔는가* — 대체 DSL이 완전했고, 두 DSL의 공존 비용이 컸기 때문이다. 두 줄이 한 묶음이다.

## 동기화된 deprecation 4가지 — 같은 박자로 사라진 것들

세 번째 화두는 *비슷한 운명*을 따라간 항목들이다. 결론부터 한 줄로 두자. `kotlinOptions`는 외롭지 않다. 같은 1년 안에 같은 박자로 빌드 스크립트를 비운 항목이 적어도 네 가지 더 있다. 하나씩 살펴보자.

### kotlin-android-extensions — `@Parcelize`의 옛 집

안드로이드 진영에서 익숙한 풍경 하나다. `@Parcelize`를 위해 한때 우리 모두가 적어 뒀던 한 줄.

```kotlin
// 1.9 (kotlin-android-extensions 시절)
plugins {
    id("kotlin-android-extensions")
}

@Parcelize
data class User(val name: String) : Parcelable
```

이 플러그인은 사실 1.4.30 시점에 이미 *kotlin-parcelize*로 쪼개졌다. View binding 생성처럼 Synthetics 쪽 기능은 view binding으로 대체하라는 권고가 같이 붙었다. 즉 `kotlin-android-extensions`는 *2020년 즈음부터 deprecated 알림이 붙어 있던* 자리다. 그런데 우리 사내 코드 어딘가에는 여전히 살아 있는 모듈이 있다. 누군가 처음 짠 베이스 모듈이 그렇고, 한 번 작동하기 시작한 뒤로 손대지 않은 모듈이 그렇다.

이 플러그인의 시간표는 다음과 같다.

- **1.9** — deprecated. 빌드는 통과.
- **2.0/2.1** — deprecated. 여전히 통과.
- **2.2** — *제거*. 플러그인 ID 자체를 인식하지 못한다. configuration error로 빌드가 멈춘다.

옮기는 길은 두 갈래다. 하나, `@Parcelize`를 쓰는 모듈은 `kotlin-parcelize`로 옮기자.

```kotlin
// 2.x 권장
plugins {
    id("kotlin-parcelize")
}

@Parcelize
data class User(val name: String) : Parcelable
```

플러그인 ID 한 줄만 바꾸면 된다. 코드 본문은 그대로다. 둘, Synthetics(`kotlinx.android.synthetic.*`)을 쓰던 자리는 view binding으로 옮기자. 이쪽은 양이 좀 있다. 한 번에 다 들어내려 하지 말고 모듈별로 잘게 끊어 가는 편이 마음 편하다.

이 두 갈래 작업은 *간단해 보이지만 잔재가 많다*. 사내 convention plugin이 `id("kotlin-android-extensions")`를 *조건부로* 적용하는 자리, 라이브러리 모듈의 publish 설정이 옛 플러그인의 산출물을 같이 묶는 자리, 자동 생성 코드가 옛 plugin namespace를 들고 있는 자리. 이 자잘한 지점들이 한 번에 드러나지 않는다는 점이 진짜 함정이다.

### Apple `ios()` / `watchos()` / `tvos()` 단축형 — 명시 타깃 강제 이주

KMP를 운영하는 팀이라면 한 번쯤 마주치는 항목이다.

```kotlin
// 1.9 시절의 KMP 빌드 스크립트
kotlin {
    ios()       // iosArm64 + iosX64 + iosSimulatorArm64를 한 번에
    watchos()
    tvos()
}
```

이 *단축형* 함수는 KMP 도입 초기, *Apple 진영의 여러 타깃을 한 번에 묶어 주는 편의*로 도입됐다. 그런데 Apple 자신이 Apple Silicon으로 넘어오면서 *어떤 x64 타깃이 살아남고 어떤 타깃이 사라지는지*를 매년 다시 정리하기 시작했다. 단축형은 그 다이내믹스를 깔끔히 표현하지 못한다. *iosX64를 빼고 iosArm64와 iosSimulatorArm64만* 같은 결정이 단축형 한 줄로는 어색하다.

이 항목의 시간표는 짧다.

- **1.9** — warn.
- **2.0** — warn.
- **2.1** — *error*. 빌드가 멈춘다.
- **2.2** — *removed*. 함수 자체가 사라진다.

옮기는 길은 *명시 타깃을 직접 적는다*이다.

```kotlin
// 2.x 권장 — 명시 타깃
kotlin {
    iosArm64()
    iosSimulatorArm64()
    // iosX64()는 비즈니스 결정에 따라
    watchosArm64()
    watchosSimulatorArm64()
    tvosArm64()
    tvosSimulatorArm64()
}
```

명시 타깃으로 옮기면 빌드 스크립트가 길어진다. *번거롭다.* 하지만 *어떤 타깃이 우리 비즈니스 결정에 들어 있는지*가 한 줄씩 분명해지는 일이기도 하다. 2.3에서 iOS 최소 OS가 14로 올라가고, macosX64/iosX64/tvosX64/watchosX64가 *2.4에서 제거 예정*이라는 신호를 받으면, 이 명시화의 가치는 더 커진다. 단축형으로 묶여 있던 자리에서는 그 결정을 *한 번 더 흩어서* 다시 잡기 어렵다.

### `KotlinCompilation.source(...)` — 사라지는 KMP 빌드 API

이쪽은 KMP 라이브러리를 *직접 짜는* 사람들이 부딪히는 자리다.

```kotlin
// 1.9 시절 — source set을 직접 attach
kotlin {
    targets.all {
        compilations.named("main") {
            source(sourceSets["commonMain"])
        }
    }
}
```

이 API는 KMP의 source set 토폴로지를 빌드 스크립트가 *직접 만지는* 길이었다. 그런데 KMP가 정착하면서 source set 사이의 의존 관계는 *기본 토폴로지*로 자동 해결되는 편이 된다. `compilation.source()`라는 *명령형 API*가 굳이 필요한 자리가 거의 없어진 것이다.

시간표는 다음과 같다.

- **1.9** — warn.
- **2.0** — *error*. 호출 자체가 컴파일되지 않는다.
- **2.3** — *removed*. API 자체가 사라진다.

옮기는 길은 source set의 `dependsOn(...)` 관계를 직접 표현하는 것이다.

```kotlin
// 2.x 권장 — defaultSourceSet 의존 관계
kotlin {
    sourceSets {
        val commonMain by getting
        val iosArm64Main by getting {
            dependsOn(commonMain)
        }
        val iosSimulatorArm64Main by getting {
            dependsOn(commonMain)
        }
    }
}
```

대부분의 경우는 *이 코드를 적을 필요조차 없다*. 기본 토폴로지가 같은 일을 자동으로 해 준다. 우리가 `source()`를 부르고 있던 자리는 보통 *기본 토폴로지가 잡아 주지 못하는 특수한 그래프*였을 가능성이 높다. 그 특수성이 정말 필요한지 한 번 더 자문해 보고, 필요하다면 `dependsOn(...)` 패턴으로 명시하자. 필요하지 않다면 그 줄은 그냥 지우는 편이 깔끔하다.

### Ant 빌드 시스템 — 마지막 묘비명

마지막 한 줄짜리 항목이다.

- **1.9 ~ 2.1** — Ant 빌드 시스템 지원, 그대로.
- **2.2** — deprecate.
- **2.3** — *완전 제거*.

Kotlin이 처음 출시되던 시절부터 Ant는 한 자리를 차지하고 있었다. JSR-223 스크립팅과 REPL과 함께 *주류는 아니지만 살아 있던* 자리다. 2.2에서 Ant·REPL·JSR-223이 함께 deprecated 또는 opt-in 전용으로 격하됐고, 2.3에서 Ant는 끝내 묘비명을 새기게 됐다. 이 항목이 우리에게 직접 닿는 일은 드물지만, *이 종류의 깔끔한 단절*이 2.2~2.3 사이에 같이 일어난다는 사실 자체를 머리에 두고 가는 편이 낫다. 같은 분기에 같은 박자로 *옛것이 한 번에 정리되는* 자리이기 때문이다.

이 네 항목을 한 번에 묶어 보면, *동기화된 deprecation*이라는 이름이 그냥 비유가 아니라는 사실이 분명해진다. `kotlinOptions`, `kotlin-android-extensions`, Apple 단축형, `KotlinCompilation.source(...)`, Ant. 모두 1.9 즈음에 deprecated가 시작됐고, 2.1과 2.2 사이의 *짧은 1년*에 일제히 error 또는 removed로 떨어졌다. 한 두 항목은 우연이라 부를 수 있지만, 다섯 항목이 같은 시간에 같은 박자로 떨어지는 건 우연이 아니다. JetBrains는 *"K2와 함께 빌드 스크립트도 한 번 정리한다"* 라는 큰 그림을 들고 있었던 셈이다. 우리가 그 그림을 한 분기 일찍 읽지 못하면, 우리 빌드가 그 정리의 비용을 한 번에 치른다.

## [박스] KAPT4 캐스케이드 — 2.1 alpha → 2.1.20 default → 2.2.20에서 자기 자신이 deprecated

이 박스는 1.9 시점에 kapt에 깊게 묶여 있던 시니어 다수에게 따로 한 페이지를 두고 싶다.

kapt는 자바 어노테이션 프로세서를 코틀린에서 굴리기 위한 다리다. Dagger, Room, Glide, MapStruct — 이 이름들이 익숙하다면 우리 빌드 어디엔가 kapt가 살아 있을 가능성이 높다. K1 시절의 kapt는 K1 컴파일러 위에서 자바 stub을 생성한 뒤 그 stub을 자바 컴파일러로 처리하는 *2단 구조*였다. K2가 등장하면서 이 다리도 새 시대에 맞게 다시 지어야 했다.

JetBrains는 이 다리를 *KAPT4*라는 이름 대신 *K2 KAPT*라는 자세로 옮겼다. 즉 같은 kapt 사용자 인터페이스를 두고 *내부 엔진을 K2로* 갈아 끼우는 방식이다. 시간표는 다음과 같다.

- **2.1.0 (2024-11)** — `kapt.use.k2=true` 옵션이 *alpha*로 도입. 옵트인하면 새 엔진을 시도해 볼 수 있다.
- **2.1.20 (2025-03)** — `kapt.use.k2`가 *기본값 true*로 바뀐다. 이때부터 명시적으로 끄지 않는 한 우리 모두는 K2 KAPT를 쓰고 있는 셈이다.
- **2.2.20 (2025-09)** — `kapt.use.k2` 프로퍼티 *자체가 deprecated*. 즉 K2 KAPT가 *유일한 선택지*가 됐다는 신호다. 이 한 줄은 *이제 더는 토글하지 않는다*는 의미다.

여기서 챙겨 둘 결은 두 가지다. 하나, 이 1년의 캐스케이드는 *조용했다*. 우리가 kapt를 그대로 두고 Kotlin 버전을 따라 올렸다면, 알아채지 못한 사이에 K1 KAPT → K2 KAPT alpha → K2 KAPT default로 끌려갔을 가능성이 높다. 둘, 그 조용함이 *반드시 좋은 일은 아니다*. K2 KAPT는 K1 KAPT와 *동등한* 동작을 목표로 하지만, *동일한* 동작을 보장하지는 않는다. 어노테이션 프로세서가 사용하는 PSI 우회 패턴이나 *Kotlin 메타데이터 추출* 패턴 같은 자리에서 미묘한 회귀가 보고된 사례가 있다.

그래서 권하는 길은 두 갈래다. *프로덕션 모듈*에서는 의식적으로 한 분기 정도 K2 KAPT를 더 지켜본다. 빌드 리포트의 KAPT 단계 시간을 그래프로 한 번 그려 보고, 동작에 미세한 차이가 없는지 PR 리뷰의 시선으로 한 번 훑는다. *사이드 모듈*에서는 새 옵션을 일찍 시도해 사내 사례를 만든다. JetBrains의 공식 권고는 여전히 *KSP를 우선*하라는 쪽이지만, KSP2가 아직 메이저 라이브러리 마이그레이션을 다 끝낸 상태가 아니라는 평가도 같이 있다. *kapt를 그대로 두고 K2 KAPT를 쓴다*는 절충안이 2.2.20 시점에서는 가장 안전한 길로 자리잡았다.

이 박스의 한 줄 요약은 이렇다. *2.1 alpha → 2.1.20 default → 2.2.20 deprec*. kapt에 묶여 있는 코드베이스라면, 이 세 점프를 *조용한 변경*으로 흘려보내지 말고, 매 점프마다 한 시간씩 빌드 리포트를 들여다보는 편이 낫다.

## 누적 deprecation 표 — 1.9에서 2.3까지 한 페이지로

지금까지 본 항목들을 한 표에 모아 두자. 이 표가 책에서 가장 자주 펼쳐질 한 페이지가 되도록 설계했다.

| 항목 | 1.9 | 2.0 | 2.1 | 2.2 | 2.3 |
|---|---|---|---|---|---|
| `kotlinOptions { }` | warn | warn | warn | **error** | error |
| `kotlin-android-extensions` | warn | warn | warn | **removed** | removed |
| context receivers (`-Xcontext-receivers`) | exp | warn (2.0.20) | warn | warn | **removed (예정)** |
| `KotlinCompilation.source(...)` | warn | **error** | error | error | **removed** |
| Apple `ios()`/`watchos()`/`tvos()` 단축형 | warn | warn | **error** | **removed** | removed |
| `withJava()` | ok | ok | warn (2.1.20) | warn | warn |
| `-language-version=1.6 / 1.7` | ok | ok | warn | **error** | error |
| `-language-version=1.8` | ok | ok | ok | ok | **error** |
| Ant 빌드 시스템 | ok | ok | ok | **warn** | **removed** |
| `kapt.use.k2` (KAPT4 토글) | — | — | alpha | default (2.1.20) | **deprecated (2.2.20)** |

표를 한 번 가로로 훑어 보면, *2.2 열에 굵은 글씨가 가장 많다*는 사실이 눈에 들어올 것이다. 우리가 2.1 → 2.2 점프를 *책 전체에서 가장 위험한 단계*라고 부르는 이유가 여기에 있다. context receivers 같은 항목이 2.3 열로 넘어가긴 하지만, 빌드 스크립트의 *깔끔한 단절*은 2.2 한 분기에 압축돼 있다.

세로로도 한 번 훑어 보자. `kotlinOptions`, `kotlin-android-extensions`, Apple 단축형, `KotlinCompilation.source(...)`, Ant. 다섯 항목이 *비슷한 박자*로 굵은 글씨를 떨어뜨린다. 한 두 항목이 박자를 살짝 어긋나기는 하지만 *전체적인 곡선*은 한 방향이다. *2.2를 향해 같이 떨어진다*. 이 곡선이 우리에게 주는 메시지는 한 줄이다. **2.1 → 2.2 점프 한 번에 빌드 스크립트의 다섯 자리가 같이 잡힌다.** 한 번에 같이 손대는 편이 낫고, 손대지 않으면 한 번에 같이 멈춘다.

`withJava()`는 표에서 외롭게 *warn*으로만 살아남은 항목이다. 이 자리는 KMP 모듈이 자바 소스를 같이 묶을 때 쓰던 한 줄인데, 2.1.20에 deprecated가 시작됐지만 2.3까지도 warn 상태로 끌고 가는 중이다. *동기화된 deprecation*의 흐름과 살짝 어긋나는 한 항목인 셈이다. 사내에 자바 + KMP가 섞여 있는 구조라면 이 한 줄을 따로 메모해 두자. 다음 분기 어딘가에서 비슷한 박자에 합류할 가능성이 있다.

이 표를 사내 위키 한 페이지로 박아 두는 작업을 권하고 싶다. 누군가 사내 convention plugin에 한 줄을 더할 때, 이 표가 옆에 펼쳐져 있으면 *그 한 줄이 어느 분기에서 빨갛게 변할지*를 PR 시점에 가늠할 수 있다. 표를 만드는 비용은 크지 않다. 위 마크다운을 그대로 붙여 넣고, 사내 코드베이스에서 사용 중인 항목에만 굵은 표시를 더하면 된다. 한 번 박아 두면 다음 마이그레이션 분기마다 같은 표를 다시 펼치게 되고, 그때마다 이 *한 페이지*가 우리 사내의 짧은 합의문이 되어 준다.

## 롤백 안전망 — `languageVersion = 1.9`의 한계

여기까지 읽고 *우리 사내 빌드는 도저히 한 번에 못 옮긴다*는 결론에 이른 독자가 있을 것이다. 사실 이 정서는 흔하다. buildSrc가 거대하고, convention plugin이 여러 단계로 얹혀 있고, 사내 라이브러리 publish 채널이 묶여 있는 코드베이스라면 *2.2 점프 한 번에 모든 모듈*을 옮기는 일이 비현실적일 수 있다. 그럴 때 우리에게 남는 마지막 안전망이 한 줄짜리 토글이다.

```kotlin
// 안전망 — K1 시맨틱 유지
kotlin {
    compilerOptions {
        languageVersion.set(KotlinVersion.KOTLIN_1_9)
        apiVersion.set(KotlinVersion.KOTLIN_1_9)
    }
}
```

이 한 줄은 컴파일러는 K2(2.x)를 쓰되, *언어 시맨틱*만 1.9 시절로 묶어 두는 의미다. 2장에서 가볍게 짚었던 *컴파일러 버전과 언어 버전의 분리*가 정확히 여기에 쓰인다. 새 컴파일러의 빠른 분석은 누리되, *우리 코드가 새 시맨틱에 맞춰 다시 쓰일 때까지의 시간*을 산다.

다만 이 안전망의 *한계*도 분명히 짚어 두자. 한 줄 요약은 이렇다. **`languageVersion = 1.9`는 코드의 시맨틱은 묶어 줄지언정, 빌드 스크립트의 deprecation은 막지 못한다.** `kotlinOptions { }`가 2.2부터 컴파일 에러가 되는 자리는 *language version*이 아니라 *KGP의 빌드 시간 동작*이다. 안전망을 켜더라도 빌드 스크립트의 `kotlinOptions { }`는 그대로 빨간 줄을 단다. `kotlin-android-extensions`는 plugin ID가 사라지므로 *configuration 단계*에서 멈춘다 — language version의 영역이 아니다. Apple 단축형도 KGP의 함수가 사라지므로 빌드 스크립트가 컴파일되지 않는다.

즉 안전망이 사 주는 시간은 *코드 본문*의 시간이지, *빌드 스크립트*의 시간이 아니다. 우리가 진짜로 *위험하다*고 느끼는 자리 — `kotlinOptions { }`가 가득한 사내 convention plugin — 은 안전망 바깥에 있다. 안전망이 있으니까 천천히 가도 된다는 결론은 위험하다. 안전망은 *코드의 시맨틱 회귀*에 한해서만 우리에게 시간을 사 주고, 빌드 스크립트의 *깔끔한 단절*은 결국 그 분기 안에 같이 손봐야 한다.

이 한계를 받아들이고 나면 전략이 단순해진다. *빌드 스크립트는 본문보다 한 분기 일찍* 옮긴다. 우리가 2.1을 쓰고 있다면, 빌드 스크립트는 이미 *2.2의 모양*으로 다듬어져 있어야 한다. 빌드 스크립트가 미리 깨끗하면, 본문은 안전망 아래에서 한 분기를 더 산다. 그 사이에 사내 시니어가 시간을 벌어 본문 시맨틱을 정리한다. 이 *시차 전략*이 우리에게 남은 가장 깔끔한 길이다. 자세한 단계는 9장 9.3절의 *2.1 → 2.2 단계*에서 다시 한 번 시간 순으로 묶어 둔다.

한 가지 더 짚어 두자. 안전망을 *얼마나 오래 켜 둘 것인가*도 결정해야 한다. `languageVersion = 1.9`로 묶어 둔 모듈은 *2.x의 새 시맨틱이 가져다주는 이득*을 그만큼 미루는 셈이다. smart cast 강화, data object의 깔끔한 `toString()`, sealed exhaustiveness의 똑똑함 — 3장에서 본 *조용한 변화*들이 안전망 안에서는 들어오지 않는다. 한두 분기는 무리 없는 절충이지만, 한 해가 넘게 안전망을 켜 두면 우리 코드는 *형식상 2.x인데 시맨틱은 1.9*인 어색한 상태에 머물게 된다. 안전망에 *기한*을 두자. 다이어리에 *언제까지 이 한 줄을 지운다*를 적어 두는 편이 낫다. 기한 없는 안전망은 안전망이 아니라 *미루기*다.

## 닫는 단락 — context receivers의 묘비명으로 가는 다리

여기까지 우리는 *경고가 에러로 변하는 1년*의 모양을 따라왔다. `kotlinOptions { }`의 짧은 1년, 동기화된 다섯 항목의 같은 박자, KAPT4 캐스케이드의 조용한 변경, 누적 deprecation 표의 굵은 글씨, 그리고 안전망의 한계. 한 줄로 묶으면 이렇다. **K2가 컴파일러를 다시 짠 김에, 빌드 스크립트도 한 번에 정리됐다.** 그 정리의 시점이 2.2이고, 그 정리의 비용을 늦게 치른 사내 빌드 로직이 한 번에 멈췄다.

이 장에서 가장 중요하게 머리에 둘 한 가지를 고르라면, *동기화된 deprecation*이라는 발음이다. 한 두 항목이 우연히 같이 사라진 게 아니다. 다섯 항목이 *한 박자*로 떨어졌다. 이 박자를 미리 듣고 있던 팀과 듣지 못한 팀의 차이는 *한 분기의 시차*였다. 그 한 분기를 사 두는 길은 의외로 단순하다. CI에 모니터링 잡 하나, 누적 deprecation 표 한 페이지, 그리고 *경고를 경고일 때 발견하는 습관*. 이 셋이면 우리 사내 빌드가 다음 점프에서 한 번에 멈출 확률이 크게 줄어든다.

다음 장에서는 *비싸게 치르는 영역*의 다른 한 축을 본다. 빌드 스크립트가 한 번에 정리됐듯이, *언어 기능*에서도 한 번 도입됐다 사라지는 항목이 있다. context receivers라는 한때의 실험이 어떻게 *묘비명*을 새기게 되는지, 그 자리에 들어선 context parameters가 어떤 *trade-off*를 들고 왔는지를 같이 따라가 보자. 빌드 스크립트의 깔끔한 단절을 본 우리에게는, 그 다음 장의 *언어 시그니처 단절*이 한결 익숙하게 느껴질 것이다.

> **마이그레이션 노트(1줄 액션)** — 사내 buildSrc / convention plugin이 latest Kotlin을 따라가도록 CI에 `--warning-mode=fail`을 박아 *경고가 에러로 변하기 전에* 잡자. 자세한 절차는 9장 9.3절 참조.
