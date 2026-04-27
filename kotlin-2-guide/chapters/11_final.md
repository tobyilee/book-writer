# 11장. 아직 끝나지 않은 길 — 2.4를 향한 가늠자, 그리고 우리에게 남은 결정

1장의 빌드 로그를 한 번 더 펼쳐 보자. 월요일 아침, 노트북을 연 그날의 그 화면이다.

```text
# 1장에서 같이 본 2.0 빌드 로그 — 노란 줄이 한 화면을 채웠다
> Task :app:compileKotlin
w: 'kotlinOptions { }' is deprecated. Use 'compilerOptions { }' instead.
w: '-Xcontext-receivers' will be removed in a future release. Use context parameters.
w: 'kotlin-android-extensions' Gradle plugin is deprecated. Use 'kotlin-parcelize'.
w: KAPT is deprecated for K2. Migrate to KSP where possible.
w: 'KotlinCompilation.source(...)' is deprecated. Use 'defaultSourceSet.dependsOn(...)'.
w: implicit 'lambda → invokedynamic' may break Serializable lambdas. See @JvmSerializableLambda.
w: ... (스크롤이 한 번 더 내려간다)
BUILD SUCCESSFUL in 9s
```

이 화면이 처음 우리를 *난감하게* 만든 자리였다. 그 자리에서 이 책이 출발했다. 같은 모듈을 2.3까지 끌어올린 뒤 다시 빌드해 보자.

```text
# 2.3 빌드 로그 — 같은 모듈, 한참을 거슬러 올라온 시간
> Task :app:compileKotlin
BUILD SUCCESSFUL in 7s
```

한 화면을 빼곡히 채우던 노란 줄이 사라졌다. 빌드 시간도 약간 줄었다. 이 한 컷의 차이를 우리는 *9장의 네 번의 점검*과 *6장의 누적 deprecation 표*와 *7장의 context parameters 마이그레이션*과 *5장에서 사라진 의존성*을 거쳐 만들어 왔다. 빌드 로그가 짧아진 만큼, 우리 코드베이스가 *시간의 무게*를 한 단계 내려놓은 셈이다. 그 풍경 앞에 잠깐 서 있어도 좋다. 마지막 장은 그 자리에서 시작한다.

이 변화는 누적 캐스케이드의 *내일 아침 첫 commit*에 속한다. 1~10장의 모든 단계가 *과거의 시간표*를 따라온 길이었다면, 11장은 그 시간표를 닫고 *앞으로의 시간표*를 펼치는 자리다. 머릿속에 화두 셋을 깔아두자.

- 2.3 Experimental 명단 중 어떤 항목이 2.4 Stable로 졸업할 가능성이 높을까?
- Kotlin 2.x의 변화가 우리에게 가르친 *진화 패턴*은 무엇이고, 그 패턴은 어떻게 다음 메이저에 적용될까?
- 이제 우리는 1.9를 떠나 2.3에 도달했다. 그렇다면 *내일 아침 첫 commit*은 무엇이어야 할까?

세 질문에 차례로 답을 얹어 보자.

## 2.3 Experimental 졸업생 후보 — 패턴으로 가늠하기

8장에서 2.3 Experimental의 두 신호 — explicit backing fields와 Unused Return Value Checker — 를 짚었다. 5장에서 *UUID v7 명시 생성*도 같이 봤다. 이 셋이 2.4에서 어떤 운명을 맞을지, *과거의 패턴*으로 가늠해 보자.

가늠의 기준점이 되어 줄 두 묶음을 다시 펼친다.

- **2.1 Preview → 2.2 Stable 졸업생**: guard `when`, multi-dollar interpolation, non-local break/continue.
- **2.2 Preview → 2.3 Stable 졸업생**: data-flow exhaustiveness for `when`, expression body의 `return`, nested type aliases, `kotlin.time.Clock`/`Instant`.

이 두 묶음의 *모양*을 다시 보자. 둘 다 *문법 차원의 ergonomics*이거나 *표준 라이브러리 흡수* 둘 중 하나다. 그렇다면 같은 모양에 속하는 2.3 Experimental은 *졸업 가능성이 높다*고 가늠해도 무리가 없다.

**explicit backing fields**는 첫 번째 카테고리에 정확히 들어맞는다. `_city`/`city` 두 줄을 한 줄로 줄여 주는 *문법 ergonomics*다. 8장에서 본 한 가지 제약 — backing field/initializer/delegation을 가진 property에 context parameter를 동시에 둘 수 없다는 — 만 한 사이클 안에 정리된다면, 2.4에서 무플래그 Stable로 들어올 가능성이 높다. 지금 우리가 할 일은 분명하다. ViewModel 한 모듈을 골라 `-Xexplicit-backing-fields`로 한 사이클을 살려 두는 일이다. 2.4가 도착하면 *플래그만 떼는* 형태로 자연 전환을 받는다.

**UUID v7 / v4 명시 생성**은 두 번째 카테고리에 든다. `Uuid.generateV4()`, `Uuid.generateV7()`, `Uuid.generateV7NonMonotonicAt(instant)`, `Uuid.parseOrNull(...)` — 이 묶음은 *표준 라이브러리 흡수*의 결을 그대로 따른다. `kotlin.time.Clock`이 2.1.20 Experimental에서 2.3 Stable로 졸업한 코스를 그대로 밟을 가능성이 높다. 우리 코드에서 `java.util.UUID.randomUUID()` 한 줄이 박혀 있는 자리들을 *후보로* 메모해 두자. 2.4에서 무플래그 Stable이 되는 순간, 그 자리들이 곧장 `Uuid.generateV7()`로 갈아탈 수 있다. UUID v7는 시간 정렬이 가능하다는 점에서 인덱스 친화적인 새 *기본값*을 우리에게 권하는 신호이기도 하다.

반대 방향으로 가늠해야 할 후보가 **Unused Return Value Checker**다. 이 기능은 *행동 강제* 성격이 강하다 — 무플래그 Stable이 되는 순간 코드베이스 전체에 *수십, 수백 개의 경고*가 한꺼번에 떠오를 수 있다. JetBrains는 이런 변화를 한 번에 밀어 넣지 않는 *습관*을 가지고 있다. opt-in으로 한 사이클을 살린 뒤, 그 사이에 라이브러리 측이 자기 함수에 `@MustUseReturnValues`를 붙여 *준비*하는 시간을 둔다. 2.4에서 Stable이 될 가능성도 있고, 한 사이클을 더 둘 가능성도 있다. 어느 쪽이든 지금 *후보 모듈 한 곳*에서 익혀 두는 일은 손해가 아니다.

라이브러리 작성자용 묶음 — `@JvmExposeBoxed`, annotations in Kotlin metadata — 은 가늠이 더 어렵다. 사용자 베이스가 좁고, 컴파일러 플러그인 생태계의 채택 속도가 변수다. 이 묶음은 2.4보다 그 다음 메이저까지 시야를 늘려 보는 편이 *바람직하다*.

## 알려진 미해결 — macosX64 정리, KSP2 미성숙

미래를 가늠할 때 *졸업 후보*만 보고 말 수는 없다. *닫히는 길*과 *아직 어수선한 길*도 같이 짚어야 가늠이 정직해진다.

먼저 닫히는 길. 2.3에서 Apple 최소 OS가 iOS/tvOS 12 → 14, watchOS 5 → 7로 한 단계 올라갔다. 그리고 한 줄이 더 박혀 있다 — *macosX64 / iosX64 / tvosX64 / watchosX64는 support tier 3, Kotlin 2.4에서 제거 예정*. Intel Mac 시뮬레이터로 KMP 빌드를 돌리던 자리는 다음 메이저에서 *컴파일이 멈춘다*. 9장 9.4절에서 이미 한 번 짚었지만, 11장에서 다시 한 번 강조해 두자. *Apple Silicon 우선*으로 CI 재구성이 늦어도 2.4 도착 전에 끝나야 한다. 사내에 Intel Mac 빌드 노드가 한 대라도 남아 있다면, 그 노드는 시한부다.

다음으로 어수선한 길. KSP2 이야기를 한 번 더 꺼낼 수밖에 없다. 9장에서도 짚었지만, Slack의 Zac Sweers는 KSP2를 *"still has a lot of open issues"*로 평가했다(2024 시점 글). 2025-09 시점(2.2.20)에는 K2 KAPT가 사실상 디폴트라, 현실적인 절충안은 *kapt를 그대로 두고 K2 KAPT를 쓰는* 길이다. 이 책은 *KSP1 → KSP2 권고 시점*과 *K2 KAPT 디폴트화*까지만 다뤘다. KSP2의 *내부 구현*은 아직 안정 단계가 아니라 의도적으로 비워 두었다. 2.4 시점에 KSP2가 어디까지 성숙할지는 *KSP GitHub 이슈 트래커*와 *KotlinConf 2025 발표 자료*를 따라가며 가늠해야 한다.

KotlinConf 2025 자체도 변수다. 본 책의 인용은 KotlinConf 2024 슬라이드와 talk 페이지까지만 닿았다. KotlinConf 2025에서 2.3 관련 세션이 별도 자료를 풀어 놓는다면, *졸업 후보* 명단의 가중치를 다시 잡아야 할 수도 있다. 컨퍼런스 직후의 KEEP 진행 상황과 함께 보면 그 시점의 가늠이 가장 정확해진다. 우리는 책을 닫고도 *KEEP*과 *KotlinConf*는 한동안 더 따라가야 한다는 뜻이다.

## 이 책이 *의도적으로 다루지 않은* 영역 — 다음 행선지 이정표

마무리에 한 번은 정직하게 짚고 가자. 이 책 한 권으로 모든 답이 끝나는 게 아니다. 처음부터 *다루지 않기로* 선을 그은 영역들이 있다. 그 좌표를 다시 펼쳐 두는 일이, 우리 다음 행선지의 이정표가 된다.

첫째, *KSP2 깊은 내부*다. 위에서 짚은 대로다. 이 책은 K2 KAPT 디폴트화까지만 다루고, KSP2의 API 디테일은 KSP GitHub 저장소와 KotlinConf 발표로 넘긴다. 우리 프로젝트에 어노테이션 프로세서가 깊이 박혀 있다면, KSP2 마이그레이션은 *2.4 이후*의 별도 트랙으로 잡아 두는 편이 낫다.

둘째, *Kotlin/Native 컴파일러 백엔드와 LLVM 통합 디테일*이다. 2.3의 Swift Export 기본 활성, 2.2.20의 Native concurrent GC 정도는 5장과 10장에서 다뤘지만, LLVM IR 매핑과 K/N 메모리 모델은 이 책의 독자 — 백엔드/안드로이드/KMP 사용자 — 에게 *과한 깊이*다. K/N 내부에 손대고 싶다면 JetBrains의 native runtime 저장소와 Kotlin 컴파일러 슬랙 채널이 다음 행선지다.

셋째, *Compose Multiplatform의 모든 안정성 변화*다. Compose for iOS·Web의 stability 변천은 Compose Multiplatform 자체 changelog에서 더 정확하게 따라갈 수 있다. 이 책은 *Compose 컴파일러와 Kotlin의 결속*까지만 다뤘다.

넷째, *학술 논문 트랙의 부재*다. 솔직히 말해 이 주제는 학술 논문이 거의 존재하지 않는다. KotlinConf / JVMLS 발표와 KEEP 디자인 문서를 학술 트랙의 대체로 사용했다. paper-research 트랙의 부재는 *의도적 누락*이다.

다섯째, 그리고 가장 *찜찜한* 자리 — *국내 대형 서비스(카카오·우아한형제들·라인·NHN)의 K2 도입 후기 부재*다. 검색 가능한 1차 자료가 부족하다는 한계를 그대로 인정하자. velog와 Medium-Korean의 개인 후기를 인용하는 선에서 그쳤다. 이 빈틈은 다음 박스로 이어진다.

## [박스] 사내 도입 정당화용 *대체 자료* — 결정자 무기

> 회사에서 K2 도입을 *위에 설득해야 하는* 자리에 서 있다고 해보자. "국내 대형사가 어디까지 도입했나"라는 질문에 정직한 답은 *"공개된 1차 자료가 부족하다"*다. 그 자리에서 손에 쥘 수 있는 *대체 자료*를 한 묶음으로 정리해 두자. 결정자 무기로 그대로 쓸 수 있다.
>
> **(1) GitHub 메이저 OSS의 K2 도입 PR**
> — Square 진영(Anvil, Moshi 등), Apollo Kotlin, Ktor, kotlinx-coroutines, kotlinx-serialization. 각 저장소의 PR 검색에서 `K2`, `FIR`, `compose-compiler` 키워드로 좁히면 *어떤 회귀를 어떻게 잡았는지*가 commit 단위로 남아 있다. Apollo의 K2 적응 블로그는 10장 박스에서 한 번 인용했다. 이 묶음은 *기술 차원의 신뢰성*을 보여 주는 자료다.
>
> **(2) JetBrains *Customer Story* 페이지 트래킹**
> — Anki-Android(clean build 57.7s → 29.7s, 94% 단축), Exposed(80% 단축) 같은 *공식 사례*가 정기적으로 업데이트된다. 1장과 2장에서 인용한 수치들이 모두 이 트랙에서 나온다. 결정자에게 *수치로 말하는 자료*가 필요할 때 이 페이지가 가장 빠르다.
>
> **(3) KotlinConf 한국어 발표 / 한국 KUG 발표 트래킹**
> — KotlinConf 2024 / 2025의 한국어 발표(있다면)와 Kakao·라인·우아한형제들 사내 KUG 발표는 *국내 맥락의 1차 자료*에 가장 가까운 묶음이다. 발표 슬라이드가 공개돼 있는 자리는 결정자 미팅의 *가장 짧은* 인용이 된다. 한국어 KUG meetup 페이지를 한 번씩 훑어 두자.
>
> **(4) 자기 회사 사례를 *오픈소스 후기로 남기는* 행동**
> — 가장 어려운, 그러나 가장 큰 효용을 가진 자리다. 우리 회사의 K2 도입 절차를 velog / Medium / 사내 기술 블로그 한 편으로 풀어 공개하자. 1년 뒤 누군가가 "국내 대형사 사례"를 검색했을 때, 그 한 편이 *우리가 비웠던 빈자리*를 채운다. 이 책의 빈자리를 이 책의 독자가 메우는 길이다 — 이 청유는 마지막까지 한 번 더 이어진다.

## 5가지 큰 그림 다시 — 책 한 권을 한 페이지로

1장에서 던졌던 질문들에 답을 얹을 자리다. 책 한 권을 *한 페이지로* 다시 정리해 두자.

**첫째, K2는 단순 빠른 컴파일러가 아니라 IDE/플러그인 생태계의 기반이다.** 2장에서 본 FIR이라는 단일 자료구조가 IDE·컴파일러·멀티플랫폼을 *처음으로 같은 트리* 위에 정렬했다. 컴파일 시간이 ±94%/−17%로 흩어지는 *분산*보다 더 큰 변화는, K2가 *2.x 시대의 모든 변화가 깔리는 기반 인프라*라는 사실이었다. 1장에서 켠 IDE K2 모드 토글이 그 기반에 발을 올린 *첫 행동*이었다.

**둘째, 2.x는 한 번의 점프가 아니라 *4단계의 누적 캐스케이드*다.** `kotlinOptions {}`가 2.0 warn → 2.2 error로, context receivers가 2.0.20 deprec → 2.3 제거로, KAPT4가 2.1 alpha → 2.1.20 default → 2.2.20 deprecated로 흘러온 시간의 모양을 우리는 6장과 7장에서 따라갔다. 이 시간의 모양을 이해해야, 1.9에 멈춰 있던 코드를 *어느 단계*로 끌어올릴지 결정할 수 있다.

**셋째, Preview → Stable의 시간 지도는 *패턴*이지 우연이 아니다.** 4장의 세 카드(guard `when`·multi-dollar·non-local break)가 2.1 Preview → 2.2 Stable로 졸업했고, 8장의 data-flow exhaustiveness와 expression body return이 2.2 Preview → 2.3 Stable로 졸업했다. 이 패턴 위에서 우리는 2.4에 들어올 졸업생들을 *가늠*할 수 있게 됐다. 새 기능은 한 사이클의 opt-in을 거쳐 무플래그 Stable로 들어온다 — 이 한 줄이 Kotlin이 진화하는 *방식 자체*다.

**넷째, 빌드 스크립트가 1.9에서 2.3까지 가장 많이 바뀐 *현장*이다.** 코드 자체의 변경은 의외로 적었다. velog와 Medium의 한국어 후기 첫 문단들이 모두 비슷했던 이유다 — *"코드 자체의 변경은 거의 필요 없다, 빌드 스크립트 변경이 핵심이다."* 5장의 사라진 의존성, 6장의 deprecation 캐스케이드, 9장의 build.gradle.kts full diff 한 페이지가 모두 그 *현장*을 가리킨다. 우리 코드베이스가 가장 많이 바뀐 자리는 `.kt` 파일이 아니라 `build.gradle.kts` 한 파일이었다.

**다섯째, 자신의 프로젝트로 직접 측정하라 — 평균이 아니라 *분산*이 진실에 가깝다.** Anki +94%와 Slack −17%가 같은 컴파일러에서 나온다는 사실을 2장에서 봤다. 사내 buildSrc가 2.2 컴파일 에러를 어떻게 맞이하는지의 사례는 사람마다 회사마다 다르다. 평균 뒤의 *내 케이스*를 직접 확인하지 않으면 어떤 가이드도 무력하다는 점, 이 한 줄이 책 전체를 관통하는 톤이었다. `kotlin.build.report.output=file` 한 줄이 그 측정의 시작점이었다.

이 다섯 줄이 책 한 권의 *압축본*이다. 책장에서 다시 꺼낼 일이 있다면, 이 다섯 줄을 먼저 펼치고 필요한 장으로 점프해도 좋다.

## 두 빌드 로그를 나란히 — 한 컷으로 닫는다

마지막으로, 1장의 그 빌드 로그와 지금의 빌드 로그를 한 자리에 다시 놓자. 책 전체를 *한 컷으로* 닫는 자리다.

```text
# 1장에서 본 2.0 빌드 로그 — 노란 줄이 한 화면을 채웠다
> Task :app:compileKotlin
w: 'kotlinOptions { }' is deprecated. ...
w: '-Xcontext-receivers' will be removed ...
w: 'kotlin-android-extensions' is deprecated. ...
w: KAPT is deprecated for K2. ...
w: 'KotlinCompilation.source(...)' is deprecated. ...
w: implicit 'lambda → invokedynamic' may break Serializable lambdas. ...
w: ... (스크롤이 한 번 더 내려간다)
BUILD SUCCESSFUL in 9s
```

```text
# 11장의 2.3 빌드 로그 — 같은 모듈, 한참을 거슬러 올라온 시간
> Task :app:compileKotlin
BUILD SUCCESSFUL in 7s
```

같은 모듈 한 토막이 두 개의 로그를 만들어 낸다. 첫 번째는 *시간이 쌓인 결과*였고, 두 번째는 *시간을 풀어낸 결과*다. 그 사이에 우리는 *네 번의 점검*을 거쳤고, *한 페이지의 누적 deprecation 표*를 펼쳐 놓고 한 줄씩 지웠으며, *한 줄씩 사라지는 의존성*을 따라 build.gradle.kts를 다시 썼다. 빌드 로그가 짧아진 만큼 코드베이스가 가벼워졌다. 그 가벼움이 *눈에 보이는* 자리가 이 두 컷이다. 한 번쯤 *뭉클하다*고 말해도 좋은 자리다.

다만 이 가벼움은 *영원하지 않다*. 2.4가 도착하면 또 새로운 노란 줄들이 우리 로그에 들어올 것이다. macosX64 시뮬레이터를 쓰던 자리에 빨간 줄이 박힐 것이고, 2.3 Experimental의 어떤 기능은 무플래그 Stable로 들어와 우리에게 *지금 한 모듈에서 살려 두라*고 신호를 보낼 것이다. 그 신호를 *예상 안*에서 받기 위해, 우리는 이 책의 *시간표 보는 법*을 손에 익혀 둔 것이다.

## 마지막 청유 — *내일 아침 첫 commit* 한 줄

이 책의 마지막 한 줄은 청유다.

책을 덮고 IDE를 여는 그 순간, 메모장 한 장에 *한 줄만* 적어 두자. *언제까지 어떤 단계를 마칠 것인가*. 한 줄의 양식은 자유다. 다만 *시점*과 *완료 정의*는 빠뜨리지 말자.

> *"이번 분기 안에 9.1절을 끝낸다. 완료 정의는 clean build + 핵심 모듈 incremental green이다."*
>
> *"다음 주 금요일까지 6장의 누적 deprecation 표에서 우리 프로젝트에 해당하는 줄들을 지운다."*
>
> *"내일 아침 첫 commit으로 IDE K2 모드를 켜고, `./gradlew build --warning-mode=all`의 노란 줄 목록을 baseline.md에 옮긴다."*

세 번째 자리에 자기 이름과 자기 시점을 박아 보자. 그 한 줄이 *내일 아침 첫 commit*이 된다. 거대한 한 번의 PR이 아니라, *한 줄짜리 commit*에서 시작하는 길이다. 우리가 1장에서 출발할 때부터 약속했던 호흡이기도 하다 — *한 번에 다 옮기려 하지 말고, 네 번의 점검으로 나누어 함께 건너가 보자*.

마지막으로, 한 자리만 더 기억해 두자. 이 책이 *비워 둔* 자리들이다. 국내 대형사 K2 도입 후기, KSP2 깊은 내부, KotlinConf 2025 한국어 세션, 우리 회사 사내 buildSrc 정비기 — 이 빈자리들의 첫 후기를 *우리가* 남길 수 있다. velog 한 편, 사내 위키 한 페이지, 회사 기술 블로그 한 편. 그 한 편이 1년 뒤 누군가의 *늦었다는 자각* 앞에 한 줄 등불이 된다. 이 책의 빈자리를 이 책의 독자가 메우는 자리, 그 자리에서 책은 정말로 닫힌다.

부록 A의 *내일 아침 첫 commit 체크리스트*가 이 청유의 *물리적 동반자*다. 9장 9.0 ~ 9.4 단계별 *오늘·이번 주·이번 분기* 액션이 한 페이지 워크시트로 정리돼 있다. 책장을 한 번 더 넘기고, 워크시트의 첫 칸에 *오늘 날짜*부터 적자. 그 한 칸이 1.9에서 2.3까지를 닫는 *마지막 한 줄*이자, 2.4를 향해 펼치는 *첫 한 줄*이다.

자, 이제 IDE를 열자. 빌드 로그를 짧게 만든 그 손으로, 한 줄을 더 적어 보자.
