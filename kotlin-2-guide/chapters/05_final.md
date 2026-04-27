# 5장. build.gradle에서 한 줄씩 사라지는 의존성들 — 2.3까지의 stdlib

오랜만에 사내 라이브러리의 의존성 트리를 펼쳐 본다고 해보자. `./gradlew :app:dependencies` 한 줄을 치고 나서, 한참 스크롤을 내리다 보면 어딘가 *낯선 줄* 하나가 눈에 박힌다.

```text
+--- com.example.our-app:domain
\--- commons-codec:commons-codec:1.15
```

이걸 누가 언제 박아 넣은 걸까. blame을 따라가 보면 4년 전, 어느 분주한 금요일 오후의 커밋이다. 메시지는 *"Base64 인코딩 추가"* 한 줄. 동료의 마음이 짐작이 간다 — `java.util.Base64`가 머릿속에서 잘 안 떠올랐을 수도 있고, Apache Commons Codec이라면 어디서나 쉽게 가져다 쓸 수 있다는 안전감이 있었을 수도 있다. 그렇게 들어온 한 줄이 그 뒤로 4년을 모듈 트리 위에 *조용히* 머물렀다.

문제는 이 줄이 *공짜로 머무는 게 아니라*는 데 있다. 빌드 캐시가 한 번씩 어긋날 때마다 commons-codec이 함께 갱신되고, 보안 스캐너가 새 CVE를 들고 올라올 때마다 한 번씩 마음이 *찜찜해진다*. KMP 모듈로 옮기려고 보면 이 의존이 *JVM 한정*이라 common 코드로 끌어 올릴 수도 없다. 정작 우리가 쓰는 건 `Base64.encodeBase64String(bytes)` 한 줄뿐인데, 그 한 줄을 지키려고 의존 트리에 큰 가지 하나가 매달려 있는 셈이다.

비슷한 자리가 한두 군데가 아니다. UUID를 발급할 때 `java.util.UUID.randomUUID()`를 쓰고 있고, 시각을 다룰 때 `kotlinx-datetime`을 따로 의존하며, 멀티플랫폼 모듈에서 atomic 카운터 하나를 쓰고 싶어 `kotlinx-atomicfu`를 또 끌어 들였다. 각각이 한 줄이지만, 모아 놓고 보면 build.gradle.kts의 dependencies 블록이 *조금씩 길어진다*. 그리고 KMP를 시도해 본 사람이라면 안다 — *common 코드*에서 쓸 수 있는 것과 *JVM 한정*인 것 사이의 경계 위에서 이 의존들이 매번 우리를 *난감하게* 만든다.

이 변화는 누적 캐스케이드의 *공짜로 가벼워진 것* 갈래에 속한다. 손을 거의 대지 않고도 build.gradle에서 한 줄씩 사라지는 의존성들의 이야기다. Kotlin 2.0부터 2.3까지 표준 라이브러리는 *조금씩, 그러나 꾸준히* 풍요로워졌고, 그 풍요는 외부 라이브러리에 손을 내밀 일을 줄여준다. 4장의 세 카드가 *언어 문법*을 다듬었다면, 5장은 *의존성 트리*를 다듬는다.

세 가지 화두를 머릿속에 깔고 출발하자.

- 라이브러리 의존성 트리에 *왜 여기에 Apache Commons가 끼어 있지?*라는 줄 하나가 박혀 있다고 해보자. Kotlin 2.2가 그 줄을 지워줄 수 있을까?
- `kotlinx-datetime`을 따로 의존하던 코드, 이제 *표준 라이브러리* 만으로 살아남을 수 있을까?
- UUID v7가 표준에 들어왔다는 건, 우리에게 어떤 새 *기본값*을 권하는 신호일까?

## Base64 4종 — JVM 한정에서 공용으로

먼저 Base64다. 도입부의 `commons-codec`이 4년 동안 매달려 있던 그 자리에서 시작하자.

1.9 시절의 선택지는 둘이었다. 하나는 표준 자바 API.

```kotlin
// 1.9 — JVM 한정
import java.util.Base64

val encoded: String = Base64.getEncoder().encodeToString(bytes)
val decoded: ByteArray = Base64.getDecoder().decode(encoded)
```

다른 하나는 외부 라이브러리. `commons-codec`을 의존에 박은 뒤 `Base64.encodeBase64String(bytes)`를 부르는 식이다. 둘 다 JVM에서만 동작한다. KMP의 common 코드에서는 어느 쪽도 못 쓴다. URL-safe encoding이 필요하거나 PEM 형식이 필요하면, 그 자리에 또 별도 함수를 직접 짜거나 라이브러리를 하나 더 들이게 된다.

Kotlin 2.2에서 이 자리가 *Stable*로 정리된다. `kotlin.io.encoding.Base64`라는 이름으로, *네 가지 변종*이 한자리에 들어왔다.

```kotlin
// 2.2 — KMP 공용
import kotlin.io.encoding.Base64

val encoded: String = Base64.Default.encode(bytes)
val urlSafe: String = Base64.UrlSafe.encode(bytes)
val mime: String   = Base64.Mime.encode(bytes)     // 76자마다 줄바꿈, MIME 표준
val pem: String    = Base64.Pem.encode(bytes)      // 64자마다 줄바꿈, PEM 표준
```

네 변종의 이름이 *그 자체로* 의도를 드러낸다는 점에 주목하자. `Default`는 RFC 4648 표준, `UrlSafe`는 URL과 파일명에 안전한 문자 집합, `Mime`은 MIME 멀티파트에 박아 넣을 때 쓰는 줄바꿈 규칙, `Pem`은 인증서 포맷이 따라가는 줄바꿈 규칙이다. 1.9 시절에 `java.util.Base64.getMimeEncoder()`와 `getUrlEncoder()`를 *기억*해 골라 쓰던 그 자리가, 2.2에서는 *코드 모양*에 의도가 그대로 드러나는 자리로 바뀌었다.

진짜 효용은 그 다음이다. 위 코드는 *common 코드에서 그대로 동작*한다. Kotlin/JVM뿐 아니라 Native, JS, Wasm 어디서든 같은 시그니처로 부른다. KMP에서 *common 코드 비율*을 늘리려고 한 번이라도 머리를 싸매 본 사람이라면, 이 한 줄의 변화가 어떤 무게를 갖는지 짐작이 간다.

JVM 쪽 사용자에게는 보너스가 하나 더 있다. 스트림 통합이다.

```kotlin
// 2.2 — JVM 스트림 위에서 Base64 인코딩
import kotlin.io.encoding.Base64
import kotlin.io.encoding.encodingWith

FileOutputStream("attachment.b64").use { output ->
    output.encodingWith(Base64.Default).use { it.write(bytes) }
}
```

`OutputStream.encodingWith(...)`는 출력 바이트를 *흘러 들어오는 동시에* Base64로 변환해주는 래퍼다. `commons-codec` 시절에는 메모리에 한꺼번에 올린 뒤 인코딩하거나, 직접 PipedStream을 깔아 흐름을 만들곤 했다. 그 자리가 한 줄로 정리됐다.

세 단계로 갈무리하자. 첫째, 기존에 `java.util.Base64`를 *이미 쓰고 있다면* 굳이 서두를 일은 없다. JVM에서는 그대로 동작한다. 다만 같은 코드를 *common 코드로 끌어 올릴* 의도가 있다면 `kotlin.io.encoding.Base64`가 정답이다. 둘째, `commons-codec`이나 비슷한 외부 라이브러리에 *Base64 한 줄을 위해* 의존하고 있었다면, 이번 기회에 그 의존을 지운다. PR 하나에 묶어 올리기 좋은 작은 단위다. 셋째, MIME이나 PEM처럼 *줄바꿈 규칙*까지 신경 써야 했던 자리도 같은 API로 정리된다. 모드 이름만 바꿔 끼우면 된다.

build.gradle.kts에서 한 줄이 사라지는 첫 장면이다.

```kotlin
// before
implementation("commons-codec:commons-codec:1.15")
// after — 의존이 사라졌다
```

## HexFormat — 한 줄짜리 헥사 변환

같은 2.2 Stable 라인에 함께 들어온 친구가 `HexFormat`이다. `Int.toHexString()`이라는 *극단적으로 짧은* 한 줄짜리 API다.

```kotlin
// 2.2
val hex: String = 93.toHexString()       // "5d"
val padded: String = 93.toHexString(HexFormat {
    number.minLength = 4
    number.removeLeadingZeros = false
})                                       // "005d"
```

이 자리에 1.9 시절의 풍경을 한 번 떠올려 보자. `String.format("%02x", value)`에 손이 자주 갔고, 패딩 조건을 맞추려면 포맷 문자열을 *기억해 두거나* 외워둔 유틸을 한 군데에 박아둬야 했다. 색상 코드, 해시값, MAC 주소, 바이트 배열 디버그 출력 — 헥사 변환이 필요한 자리는 의외로 많다. 그때마다 *어떤 포맷 문자열을 써야 했더라*를 한 번씩 검색해 본 기억이 있다면, `toHexString()` 한 줄의 무게가 가벼이 보이지 않을 것이다.

세밀 제어는 `HexFormat { ... }` 빌더로 묶인다. `minLength`, `removeLeadingZeros`, 구분자, 대소문자 같은 옵션이 한 자리에 모인다. 자주 쓰는 포맷이라면 한 번 만들어 상수처럼 두고 재사용한다.

```kotlin
val macFormat = HexFormat {
    upperCase = true
    bytes.byteSeparator = ":"
}
val mac: String = byteArrayOf(0x00, 0x1B, 0x44, 0x11, 0x3A, 0xB7.toByte())
    .toHexString(macFormat)              // "00:1B:44:11:3A:B7"
```

이 또한 KMP 공용이다. JS에서 색상 코드를 헥사로 직렬화하던 코드와, JVM 백엔드에서 SHA-256 다이제스트를 헥사로 찍던 코드를 *같은 함수 호출*로 적을 수 있다. 자잘한 포맷 헬퍼가 모듈마다 따로 흩어져 있던 코드라면, 한 번 모아 정리할 만한 자리다.

여기서 한 가지를 짚어두자. `Int.toHexString()`은 별도 의존성을 *지워주는* 종류의 변화는 아니다. 1.9 시절에 외부 라이브러리에 손을 내밀던 자리가 거의 없었기 때문이다. 다만 *손에 익은 한 줄*이 늘어났다는 점에서 의미가 있다. 평소 `String.format`을 자주 부르던 손버릇이, 한 마이너 버전 안에서 자연스럽게 `toHexString`으로 옮겨 가는 식이다. 작은 무기지만 자주 꺼내 들게 된다.

## kotlin.uuid.Uuid — UUID v7가 권하는 새 기본값

UUID 이야기는 좀 더 무겁다. 단순한 함수 한 줄짜리 변화가 아니라, *기본값을 어디에 둘 것인지*를 다시 생각하게 만드는 변화이기 때문이다.

먼저 시간표를 한 번 짚자. `kotlin.uuid.Uuid`는 2.0.20에서 Experimental로 처음 들어왔다. 그 뒤로 한 마이너 한 마이너 강화되며, 2.3 시점에는 v4·v7 양쪽의 명시적 생성, `parseOrNull`, `parseHexDashOrNull`, `Comparable` 구현까지 갖춘 모양으로 자리잡았다.

```kotlin
// 2.0.20 — Experimental 진입
import kotlin.uuid.Uuid
import kotlin.uuid.ExperimentalUuidApi

@OptIn(ExperimentalUuidApi::class)
fun newId(): Uuid = Uuid.random()
```

여기까지는 `java.util.UUID.randomUUID()`와 큰 차이가 없어 보인다. 진짜 변화는 2.3에서 들어왔다.

```kotlin
// 2.3 — v4 / v7 명시 생성
val v4: Uuid = Uuid.generateV4()
val v7: Uuid = Uuid.generateV7()
val v7At: Uuid = Uuid.generateV7NonMonotonicAt(instant)

// 2.3 — 안전한 파싱
val maybe: Uuid? = Uuid.parseOrNull("not-a-uuid")  // null
val parsed: Uuid = Uuid.parse("550e8400-e29b-41d4-a716-446655440000")
```

UUID v4와 v7이 *같은 자리*에 명시적으로 등장했다는 점에 주목하자. v4는 우리가 익히 알던 *완전 랜덤* UUID다. v7은 좀 다르다. 시간 정보가 *상위 비트*에 박혀 있어, *생성 순서대로 정렬되는* UUID다. 이 둘의 차이가 우리에게 새 기본값에 대한 질문을 던진다.

DB 인덱스 위에 UUID를 PK로 두고 운영해 본 사람이라면 v4가 가져온 *고통*에 익숙할 것이다. 새 행이 끼어드는 자리가 매번 *랜덤*이라, B-tree 인덱스의 페이지 분할이 사방에서 일어난다. 행 수가 많지 않을 때는 별 차이가 없지만, 천만 행 단위로 누적되면 INSERT 성능이 한 단계씩 떨어진다. v7은 이 자리를 *시간 순서*로 정돈해 준다. 새 행은 인덱스의 *끝쪽*에 추가되고, 페이지 분할이 한 곳에 집중된다. 결과적으로 DB 캐시 적중률이 살아남는다. 분산 시스템에서 로그를 모아 정렬할 때도 v7은 *별도 정렬 키 없이* 시간 순서를 따라간다는 점에서 손이 덜 간다.

그동안 v7을 쓰고 싶을 때는 별도 라이브러리를 끌어다 썼다. com.fasterxml.uuid의 Java UUID Generator, 또는 자체 구현. 이제 표준 라이브러리에 들어왔으니 *기본값을 v7로 두는 편이 낫다*는 권유가 자연스럽게 따라온다. 새 PK 컬럼에 `Uuid.generateV7()`를 깔아두면, 외부 의존도 줄고 인덱스 수명도 늘어난다. 일석이조의 자리다.

JVM 쪽 사용자라면 `java.util.UUID`와의 양방향 변환도 알아두자. 기존 코드와 *섞여 사는* 시기가 한동안 이어진다.

```kotlin
import kotlin.uuid.toJavaUuid
import kotlin.uuid.toKotlinUuid

val javaUuid: java.util.UUID = kotlinUuid.toJavaUuid()
val backToKotlin: Uuid = javaUuid.toKotlinUuid()
```

API 경계에서 한 번 변환하면, 안쪽은 `kotlin.uuid.Uuid`로 일관되게 다룰 수 있다. JPA 엔티티가 `java.util.UUID`로 박혀 있더라도 도메인 코드는 `kotlin.uuid.Uuid`로 쓰는 식의 분리가 가능하다.

한 가지 주의해두자. 2.3 시점에도 `kotlin.uuid.Uuid`는 *Experimental*이다. `@OptIn(ExperimentalUuidApi::class)`를 명시해야 한다. 프로덕션에 들이려면 *모듈 단위*로 opt-in 어노테이션을 격리해두는 편이 낫다 — 이 권유는 5장 끝의 마이그레이션 노트에서 한 번 더 다룬다.

build.gradle.kts에서 사라지는 줄을 한 번 더 보자. v7 제너레이터를 위해 끌어다 쓰던 라이브러리가 있다면 그 자리가 비어진다.

```kotlin
// before
implementation("com.fasterxml.uuid:java-uuid-generator:5.0.0")
// after — 표준 라이브러리로 충분
```

## kotlin.time.Clock — kotlinx-datetime이 *집*을 찾았다

UUID v7 이야기 끝에 *시각*이 자연스럽게 따라 나온다. v7은 `Instant`를 받아 시간 비트를 박아 넣는데, 그 `Instant`는 어디서 가져오는가? 1.9 시절의 답은 한 가지였다 — `kotlinx-datetime`.

```kotlin
// 1.9 ~ 2.1 — kotlinx-datetime에 의존
// build.gradle.kts
// implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.6.0")

import kotlinx.datetime.Clock
import kotlinx.datetime.Instant

val now: Instant = Clock.System.now()
```

`kotlinx-datetime`은 좋은 라이브러리였다. 멀티플랫폼 환경에서 시각을 일관되게 다루기 위한 Kotlin 진영의 *공식 답*에 가까웠다. 그런데 한 가지 *어색한 자리*가 있었다. 이 라이브러리에서 가장 자주 쓰는 두 타입 — `Clock`과 `Instant` — 가 사실은 *언어 표준 라이브러리에 있어도 이상하지 않을* 무게의 추상이라는 점이다. *지금 시각을 묻는다*는 행위를 하기 위해 외부 라이브러리에 의존해야 한다는 사실이, 코드를 짜는 동안에는 자연스러워 보였지만 한 발짝 떨어져 보면 어딘가 *낯설다*.

2.1.20에서 Kotlin은 이 자리를 정리하기 시작한다. `kotlin.time.Clock`과 `kotlin.time.Instant`가 *Experimental*로 표준 라이브러리에 들어왔다. 그리고 2.3에서 *Stable*로 졸업했다.

```kotlin
// 2.3 — 표준 라이브러리
import kotlin.time.Clock
import kotlin.time.Instant

val now: Instant = Clock.System.now()
val parsed: Instant = Instant.parse("2025-01-01T00:00:00Z")
```

import 한 줄이 `kotlinx.datetime`에서 `kotlin.time`으로 바뀌었을 뿐이다. 함수 시그니처는 거의 같다. 그러나 의미는 다르다 — *외부 라이브러리에 묻던 질문을 이제 표준 라이브러리에 묻는다*. `kotlinx-datetime`이 *집을 찾았다*는 표현이 잘 어울린다.

물론 `kotlinx-datetime`이 사라지는 건 아니다. `LocalDate`, `LocalDateTime`, `TimeZone`처럼 *달력 시간*을 다루는 풍부한 API는 여전히 그 라이브러리에 살아 있다. 다만 *machine time*에 가까운 두 타입(`Clock`, `Instant`)이 표준 라이브러리로 *흡수*된 형국이다. 도메인 코드의 80% 자리에서 쓰던 그 두 타입이 사라지면, 적지 않은 모듈에서 `kotlinx-datetime` 의존을 *제거*할 수 있게 된다.

build.gradle.kts에서 또 한 줄이 사라진다.

```kotlin
// before — 시각만 다루는 모듈에서도 매달려 있던 의존
implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.6.0")
// after — kotlin.time만으로 충분한 자리라면, 의존 자체를 뺀다
```

UUID v7와 묶어 쓰는 자리도 한 번 보자.

```kotlin
import kotlin.time.Clock
import kotlin.uuid.Uuid

@OptIn(kotlin.uuid.ExperimentalUuidApi::class)
fun newAuditId(): Uuid {
    val ts = Clock.System.now()
    return Uuid.generateV7NonMonotonicAt(ts)
}
```

이 한 함수 안에 *외부 의존이 한 줄도 끼어 있지 않다*. `kotlin.time.Clock`, `kotlin.uuid.Uuid` — 두 import 모두 표준 라이브러리에서 온다. 4년 전 commons-codec을 박아 넣던 그 마음과는 풍경이 사뭇 다르다. 별것 아닌 한 줄짜리 *시각 + 식별자* 함수를 짜기 위해, 이제 우리는 어떤 라이브러리도 끌어 들일 필요가 없다. 의외로 풍요롭다.

## kotlin.concurrent.atomics — 코루틴 의존 없는 KMP 공용 원자성

원자 카운터 하나를 KMP common 코드에서 쓰고 싶다고 해보자. 1.9 시절의 답은 또 외부 라이브러리였다 — `kotlinx-atomicfu`. JVM에서는 `java.util.concurrent.atomic`이 잘 깔려 있지만, common 코드로 끌어 올리려면 atomicfu의 컴파일러 플러그인까지 같이 들여야 했다. 라이브러리 작성자에게는 익숙한 풍경이었지만, 보통 애플리케이션 개발자에게는 *왜 이 한 카운터를 위해 컴파일러 플러그인까지*라는 어색함이 있었다.

2.1.20에서 `kotlin.concurrent.atomics`가 Experimental로 들어왔다. KMP 공용이다.

```kotlin
import kotlin.concurrent.atomics.AtomicInt
import kotlin.concurrent.atomics.AtomicLong
import kotlin.concurrent.atomics.AtomicBoolean
import kotlin.concurrent.atomics.AtomicReference
import kotlin.concurrent.atomics.ExperimentalAtomicApi

@OptIn(ExperimentalAtomicApi::class)
class RequestCounter {
    private val count = AtomicLong(0L)
    fun bump(): Long = count.incrementAndFetch()
    fun snapshot(): Long = count.load()
}
```

JVM 한정에서 common으로 *그저 옮겨 왔다*는 표현이 가장 정확하다. JVM의 `java.util.concurrent.atomic`이 거의 그대로의 시그니처로 KMP 공용 자리에 들어왔다. 그래서 마이그레이션이 한결 가볍다 — 1.9 시절에 atomicfu로 짜둔 코드를 새 API로 옮길 때, 메서드 이름이 *대부분 그대로* 남는다.

JVM 쪽 사용자라면 양방향 변환을 알아두자. 기존 `j.u.c.atomic`과의 경계 위에서 한 번씩 마주칠 자리다.

```kotlin
import kotlin.concurrent.atomics.asJavaAtomic
import kotlin.concurrent.atomics.asKotlinAtomic

@OptIn(ExperimentalAtomicApi::class)
fun bridgeWithJavaApi(legacy: java.util.concurrent.atomic.AtomicLong) {
    val k: AtomicLong = legacy.asKotlinAtomic()
    val j: java.util.concurrent.atomic.AtomicLong = k.asJavaAtomic()
}
```

`asJavaAtomic()`과 `asKotlinAtomic()` — 이 두 함수가 양쪽 세계를 잇는다. 외부 라이브러리가 `j.u.c.atomic`을 받는 시그니처를 노출한다면, 우리 common 코드는 `kotlin.concurrent.atomics`로 짜되 경계에서만 변환해 넘기면 된다. 2.2.20에서는 `update`, `fetchAndUpdate`, `updateAndFetch` 같은 함수가 추가되어 *함수형 원자 갱신* 패턴도 자연스럽게 풀린다.

build.gradle.kts에서 또 한 줄이 사라질 후보다.

```kotlin
// before
implementation("org.jetbrains.kotlinx:atomicfu:0.23.2")
// after — 보통 애플리케이션 코드라면, 의존을 뺀다
```

라이브러리 작성자라면 좀 더 신중하게 가는 편이 좋다. atomicfu는 *컴파일러 플러그인*이 일부 백엔드에서 더 효율적인 인스트럭션을 깔아주기도 한다. 핫패스에 atomic이 깔리는 라이브러리라면 두 API의 성능 프로파일을 *직접 측정*해 결정하자. 평균이 아닌 분산이 진실이라는 1장의 톤이 여기서도 그대로 적용된다.

## AutoCloseable — 한 번 더 짚고 가는 KMP 공용 무기

3장에서 가볍게 짚었던 친구를 한 번만 다시 부르자. `AutoCloseable`이 2.0에서 *공용 코드의 Stable*로 자리잡으면서, KMP 라이브러리 작성자에게 자주 마주치는 *boilerplate 한 줄*이 사라진다.

```kotlin
// 2.0 — common 코드에서 그대로
val resource = AutoCloseable { writer.flushAndClose() }
resource.use { /* ... */ }
```

JVM 한정에서 자연스럽게 쓰던 `use { }` 블록이 common 코드에서도 똑같이 동작한다는 사실, 그 자체가 5장의 메시지와 정렬된다 — *common 코드 비율이 자연스럽게 늘어난다*. 자원 관리 코드를 위해 expect/actual로 두 백엔드용 구현을 따로 짜던 자리가, 한 줄로 정리된다.

## 외부 의존이 줄어드는 방향이 가리키는 곳

여기까지를 한 발짝 떨어져 보자. Base64 4종, HexFormat, `kotlin.uuid.Uuid`, `kotlin.time.Clock` & `Instant`, `kotlin.concurrent.atomics`, 그리고 `AutoCloseable`. 이 여섯 친구의 공통점은 무엇일까.

첫째, *외부 의존을 줄이는 방향*으로 일관되게 정렬돼 있다. commons-codec, java-uuid-generator, kotlinx-atomicfu, 그리고 `kotlinx-datetime`의 두 타입 — 이 자리에 매달려 있던 줄들이 표준 라이브러리에 흡수되며 *자연스럽게* 빠져나간다.

둘째, *KMP 공용*이 기본값이다. 1.9 시절의 답이 `java.util.X`이거나 `j.u.c.X`였던 자리들이, 2.x에서는 *common 코드*에서 그대로 동작하는 모양으로 다시 짜였다. KMP에서 *common 코드 비율*을 높이려고 한 번이라도 머리를 싸매 본 사람이라면, 이 흐름의 무게를 안다.

셋째, *기본값에 대한 권유*가 함께 따라온다. UUID는 v4에서 v7으로, 시각은 외부 라이브러리에서 표준 라이브러리로, atomic은 컴파일러 플러그인에서 stdlib 함수로. 이 세 권유는 모두 *덜 의존하고, 더 일관되게*를 가리킨다.

build.gradle.kts에서 사라진 줄들의 미니 표를 한 번 그려 보자.

```text
                    1.9              →  2.3
─────────────────────────────────────────────────────────────
Base64           commons-codec       →  kotlin.io.encoding.Base64
UUID v7          java-uuid-generator →  kotlin.uuid.Uuid.generateV7()
시각              kotlinx-datetime   →  kotlin.time.Clock & Instant
KMP atomic       kotlinx-atomicfu    →  kotlin.concurrent.atomics
공용 자원 관리      expect/actual 헬퍼  →  AutoCloseable (common Stable)
```

물론 이 표가 *지워야 할 것의 목록*은 아니다. `kotlinx-datetime`은 달력 시간을 다루는 자리에서는 여전히 본진이고, atomicfu는 라이브러리 작성자에게 여전히 무기다. 다만 *가벼운 애플리케이션 코드*에서 한 줄짜리 사용을 위해 매달아 두던 의존이라면, 한 번 정리할 만한 자리들이 늘어났다.

## 마무리 — 한 번에 다 지우려 들지 말자

여기까지 보고 나면 *내일 아침 출근하자마자 build.gradle.kts를 열어 의존성 목록을 정리하고 싶다*는 마음이 들지도 모르겠다. 그 마음은 좋다. 다만 한 가지를 함께 권하고 싶다 — *한 번에 다 지우려 들지 말자*.

여섯 친구 중 둘은 *Stable*이지만 넷은 여전히 *Experimental*이다. `kotlin.io.encoding.Base64`(2.2 Stable), `Int.toHexString()`(2.2 Stable), `AutoCloseable`(2.0 Stable, 공용)은 부담 없이 들일 만하다. 반면 `kotlin.uuid.Uuid`, `kotlin.concurrent.atomics`, 그리고 2.1.20~2.2 시점의 `kotlin.time.Clock`은 Experimental 마크가 붙어 있다. (`kotlin.time.Clock`/`Instant`는 2.3에서 Stable로 졸업했다.)

Experimental API를 프로덕션에 들일 때 한 가지 원칙이 도움이 된다 — *opt-in 어노테이션을 모듈 단위로 격리한다*. `@OptIn(ExperimentalUuidApi::class)`을 클래스마다 흩어 박지 말고, 한 모듈의 `build.gradle.kts`에서 컴파일러 옵션으로 한 번만 켜두는 식이다.

```kotlin
// build.gradle.kts
kotlin {
    compilerOptions {
        optIn.addAll(
            "kotlin.uuid.ExperimentalUuidApi",
            "kotlin.concurrent.atomics.ExperimentalAtomicApi",
        )
    }
}
```

이 모듈 안에서만 새 API를 쓰고, 다른 모듈에는 *Stable한 결과물*만 노출하는 식의 격리다. 4장에서 본 *Preview 기능을 사이드 모듈에 격리*하는 패턴과 같은 결이다. opt-in의 폭발적 전염을 막아두면, Stable 졸업 시점에 격리 모듈만 *한 번 손대*는 식으로 정리할 수 있다.

PR 단위도 *작게 끊어 올리는 편이 낫다*. commons-codec 한 줄을 지우는 PR 하나, java-uuid-generator 한 줄을 지우는 PR 하나, kotlinx-atomicfu 한 줄을 지우는 PR 하나 — 이런 식으로 의존성 한 줄이 사라질 때마다 PR이 끊긴다. 한꺼번에 묶어 올리면 회귀가 났을 때 *어느 줄이 원인인지* 가늠하기 어려워진다. 5장의 변화는 *공짜에 가까운* 영역이지만, 그 공짜를 안전하게 받기 위해서는 *작게 끊어 받는 편이 낫다*.

마이그레이션 노트는 한 줄이다. **Experimental 마크가 붙은 stdlib API는 *모듈 단위 opt-in*으로 격리해 들이고, 의존성 한 줄이 사라질 때마다 PR을 작게 끊어 올리자. 자세한 절차는 9장 9.3절·9.4절을 참조하면 된다.**

3장이 K2 활성만으로 *조용히* 행동이 바뀐 자리들을, 4장이 *손도 안 대고 우아해진* 세 카드를 보여줬다면, 5장은 *build.gradle에서 한 줄씩 사라지는 의존성들*의 풍경을 모았다. 셋 모두 *공짜로 가벼워진 것* 갈래에 속한다. 시니어 독자는 이 세 장에서 "쉽게 얻는 것"의 윤곽을 잡았을 것이다.

다음 장은 톤이 바뀐다. 같은 누적 캐스케이드라도 *비용을 치르는 영역*이 시작된다. 어제까지 노란 줄이었던 `kotlinOptions { }`가 오늘은 빨간 줄을 그어버리는 그 1년 사이에 무슨 일이 있었는지, 6장에서 함께 짚어 보자. 5장의 풍요를 받기 위해, 빌드 스크립트 어딘가는 다시 쓰게 된다 — 5장과 6장 사이의 이 톤 전환이 책 전체의 *카테고리 경첩*이다. 일단 지금까지 손에 쥔 세 카드를 챙겨 들고, 다음 페이지로 넘어가 보자.
