# 3장. smart cast, data object, enumEntries — 2.0이 *조용히* 바꿔놓은 일상

> 이 변화는 누적 캐스케이드의 *공짜로 깔끔해진 것* 갈래에 속한다.

며칠 전까지 빨간 줄이 그어져 있던 자리에 어느 날 갑자기 빨간 줄이 사라져 있다고 해보자. 코드는 손대지 않았는데, 컴파일러를 2.0으로 올린 뒤 IDE를 다시 띄웠더니 `unresolved reference`가 사라지고, `EndOfFile@7a4f`로 찍히던 로그가 그냥 `EndOfFile`로 떨어진다. 이상하게 코드가 더 잘 읽힌다. 한 줄도 안 바꿨는데, 어제보다 깔끔하다. 묘한 느낌이다.

Kotlin 2.0의 큰 변화 — K2 컴파일러, 빌드 스크립트의 재정렬, deprecation 캐스케이드 — 사이에 끼어 *조용히* 들어온 변화들이 있다. 1.9에서 베타였거나 실험 단계였던 기능들이 2.0에서 Stable로 승격되며, 코드를 한 줄도 안 바꿨는데도 컴파일러의 행동이 달라진 지점들이다. 이 장에서 짚을 셋이 그렇다. smart cast가 한 단계 더 똑똑해졌고, `data object`가 `toString()`을 사람 말로 찍기 시작했고, `enumEntries<T>()`가 매번 새 배열을 만들지 않게 됐다. 덤으로 `AutoCloseable`이 KMP 공통 코드까지 내려왔다.

손대지 않아도 코드가 더 잘 동작하게 만드는 변화는, 거꾸로 말하면 *언제 들어왔는지도 모르고 지나가기 쉬운* 변화다. 그래서 한 번 정리하고 가자. 화두 셋이다.

- **K2 안에서 smart cast가 똑똑해졌다는데, 정확히 어디서부터 *말이 통하기 시작했을까?***
- 리플렉션 한 번 부를 때마다 GC가 일을 더 하고 있었다면, 똑같은 한 줄을 어떻게 *비용 없는 한 줄*로 다시 적을 수 있을까?
- sealed 계층의 마지막 케이스를 `object`로 두던 코드, 이제는 어떻게 다듬어야 깔끔할까?

---

## smart cast가 똑똑해진 7가지 장면

1.9에서 가장 자주 부딪히던 장면을 떠올려보자. 분명 위에서 `is` 체크를 했는데, 컴파일러가 그 결과를 *기억하지 못하는* 순간들. 별도 변수에 담았더니 잊어버리고, OR로 묶었더니 모른 척하고, inline 람다 안으로 들어갔더니 안전 호출(`?.`)을 다시 강제하던 그 답답함. 이런 자리마다 우리는 무심코 `!!`을 박거나, `?:`로 떨어뜨리거나, `else throw IllegalStateException(...)` 같은 방어 분기를 한 줄 더 짜 넣고 있었다.

K2는 흐름 분석을 다시 짰다. 결과적으로 7가지 시나리오에서 캐스트가 *말없이* 따라온다. 하나씩 짧게 보자.

### (1) 분리된 Boolean 변수

가장 자주 부딪히던 장면이다.

```kotlin
fun petAnimal(animal: Any) {
    val isCat = animal is Cat
    if (isCat) animal.purr()  // 1.9: unresolved reference
                              // 2.0: OK — animal이 Cat으로 cast
}
```

한 줄로 `if (animal is Cat) animal.purr()`을 쓰면 1.9도 통과한다. 하지만 가독성을 위해 조건을 변수에 담거나, `isCat`을 두 군데에서 재사용하고 싶을 때 1.9 컴파일러는 그 *연결*을 잃었다. 이제는 따라온다.

### (2) OR로 묶은 type check

```kotlin
sealed interface Status { fun signal() }
class Postponed : Status { override fun signal() {} }
class Declined : Status { override fun signal() {} }

fun signalCheck(s: Any) {
    if (s is Postponed || s is Declined) {
        s.signal()  // 두 분기의 공통 supertype Status로 cast
    }
}
```

1.9에서는 둘의 공통 부모로 좁히는 추론을 못 해 `s as Status` 같은 명시적 캐스트를 써야 했다. 이제는 가장 가까운 공통 supertype이 자동으로 잡힌다. sealed 계층을 다룰 때 잔손이 줄어든다.

### (3) inline 람다 안의 변경 가능 변수

```kotlin
inline fun inlineAction(f: () -> Unit) = f()

fun runProcessor(): Processor? {
    var processor: Processor? = null
    inlineAction {
        if (processor != null) {
            processor.process()  // 2.0: safe call(?.) 불필요
        }
        processor = nextProcessor()
    }
    return processor
}
```

`processor`가 `var`이고 람다 안에서 재할당되기 때문에, 1.9는 `null` 체크 직후의 호출에도 `?.`을 강제했다. K2는 inline 람다라는 사실을 활용해(callsInPlace 계약을 인지해) 호출 시점의 nullability를 좁혀준다.

### (4) 함수 타입 프로퍼티

```kotlin
class Holder(val provider: (() -> Unit)?) {
    fun process() {
        if (provider != null) provider()  // 2.0: OK
    }
}
```

1.9는 `provider?.invoke()`로 풀어 적거나, 지역 변수에 한 번 담아 캡처해야 했다. *프로퍼티는 다른 스레드가 바꿀 수 있으니까* — 라는 보수적 가정이 컴파일러를 지배했다. K2는 `val` 프로퍼티에 한해 그 가정을 풀어준다. (`var`는 여전히 1.9와 같다.)

### (5) try / catch / finally

```kotlin
fun parseLength(input: String?) {
    var stringInput: String? = input
    try {
        stringInput = null
        throw IllegalStateException()
    } catch (e: Exception) {
        println(stringInput?.length)  // 2.0: 컴파일러가 nullable임을 인지
    }
}
```

`try` 블록에서 변수를 `null`로 바꾼 뒤 예외가 났다면, `catch` 블록에서 그 변수가 `null`일 *가능성*을 컴파일러가 알게 됐다. 1.9는 거꾸로 — `try` 시작 시점의 타입 정보를 그대로 들고 와 nullability를 잘못 좁히기 쉬웠다. 가끔씩 NPE의 진원지였던 그 자리다.

### (6) 증감 연산자

```kotlin
sealed class Rho
class Tau : Rho() { operator fun inc(): Sigma = Sigma() }
class Sigma : Rho() { fun sigma() {} }

fun process(input: Rho) {
    var unknown: Rho = input
    if (unknown is Tau) {
        ++unknown          // Tau.inc() 가 Sigma 반환
        unknown.sigma()    // 2.0: Sigma로 cast된 채 호출
    }
}
```

증감 연산자가 *반환 타입을 바꿀 수 있다*는 사실을 K2는 흐름 분석에 흡수한다. 1.9는 `++unknown` 이후에도 `unknown`을 여전히 `Tau`로 보거나, 혹은 다시 `Rho`로 넓혀 캐스트가 풀렸다.

### (7) 그리고 한 가지 더 — bool 변수의 OR 결합

위의 (1)이 *분리된 Boolean*이라면, 이건 *분리된 Boolean들의 결합*이다.

```kotlin
fun describe(value: Any) {
    val isString = value is String
    val isLong = value is Long
    if (isString || isLong) {
        // value는 Any 그대로 — 두 분기의 공통 supertype이 Any뿐이므로
        println(value.toString())
    }
    if (isString) {
        println(value.length)  // 2.0: String으로 cast 따라옴
    }
}
```

체인이 길어진 코드에서, 위에서 `is`를 한 번 한 결과를 *지역 변수에 담아 두고 여러 분기에서 꺼내 쓰는* 패턴이 사실상 1급 시민이 됐다. 이 한 가지가 sealed 계층 위에서 분기 코드를 다시 한 번 깎게 만든다.

### 1.9 vs 2.0, 같은 코드 한 줄

핵심을 한 줄로 압축하면 이렇다.

```kotlin
// 두 줄을 떼어놓고 봤을 때
val isCat = animal is Cat
if (isCat) animal.purr()
// 1.9: unresolved reference: purr
// 2.0: 통과
```

코드는 한 글자도 다르지 않다. 컴파일러만 바뀌었다. *조용히*가 핵심 키워드인 이유다.

### 죽은 분기를 정리하는 시간

smart cast가 똑똑해지면 그 뒤에 따라오는 정리 작업이 하나 있다. 1.9 시절에 짜놓은 *죽은 분기*들이다. 흔히 이런 모양으로 박혀 있다.

```kotlin
fun handle(result: Any) {
    if (result is ReadResult.Number) {
        consume(result.n)
    } else {
        // K1이 위 cast를 잊어버려서, exhaustive하지 않다는 잔소리를 막으려고
        // 한 줄 박아뒀던 방어 코드
        throw IllegalStateException("never here")
    }
}
```

K2 위에서 다시 보면 `else` 가지 자체가 의미를 잃은 자리가 종종 보인다. IDE의 *Unreachable code* 인스펙션이나 `extraWarnings.set(true)`를 켜두면 한 묶음으로 떠오른다. 이때 한 가지 주의할 게 있다 — 인스펙션이 *진짜로* 도달 불가능하다고 말해주는 것과, 컴파일러가 *그 시점에 한해서* 도달 불가능하다고 보는 것은 다르다. sealed 계층이라면 안전하지만, 외부 입력을 받는 자리라면 방어 코드를 무작정 떼지는 말자. 잊지 말자, 컴파일러의 똑똑해짐과 도메인의 안전함은 같은 축이 아니다.

---

## data object — `toString()` 한 줄이 만드는 차이

1.9에서 sealed 계층의 마지막 케이스를 `object`로 두던 코드를 떠올려보자.

```kotlin
sealed class ReadResult {
    data class Number(val n: Int) : ReadResult()
    data class Text(val text: String) : ReadResult()
    object EndOfFile : ReadResult()  // 1.9 시절
}

println(ReadResult.EndOfFile)
// EndOfFile@1b6d3586  ← 이걸 누가 좋아할까
```

`object`는 `toString()`이 기본 구현 — 즉 `클래스이름@해시` 형태다. 로그를 한 줄 찍거나 테스트 실패 메시지를 들여다볼 때 이 16진수 hash가 끼어 있는 게 늘 찜찜했다. 그렇다고 매번 손으로 `override fun toString() = "EndOfFile"`을 박는 것도 번거로운 일이다.

2.0의 `data object`는 그 한 줄을 거저 준다.

```kotlin
sealed class ReadResult {
    data class Number(val n: Int) : ReadResult()
    data class Text(val text: String) : ReadResult()
    data object EndOfFile : ReadResult()  // 2.0 Stable
}

println(ReadResult.EndOfFile)
// EndOfFile  ← 이렇게 떨어진다
```

차이는 `toString()`만이 아니다. `equals()`와 `hashCode()`도 *클래스 이름 단위*로 합리적으로 정의된다. `object`는 어차피 싱글턴이라 `==` 결과가 같지 않냐고 물을 수 있다. 맞다. 하지만 `data object`는 의미를 *명시적으로* 박는다 — "이건 값으로 비교될 의도의 객체다." sealed 계층에서 `data class`들과 함께 쓰일 때 의미적으로 한 결로 정렬된다.

직렬화 라이브러리들이 이 결을 더 잘 활용한다. kotlinx.serialization은 `data object`를 만나면 *클래스 이름을 식별자로 쓰는* 자연스러운 직렬화를 적용한다. 1.9 시절 `object`에 `@Serializable`을 달고 형태를 어떻게 풀지 고민하던 자리가 한 줄로 정리된다.

마이그레이션은 단순하다. 컴파일러를 2.0으로 올린 뒤, sealed 계층 안의 `object`를 IDE의 *Convert object to data object* 인스펙션으로 일괄 변경하는 편이 낫다. 한 가지만 기억해두자. `data object`는 sealed 계층의 *대등한 케이스*로 두는 의도가 명확할 때 쓰는 것이다. 싱글턴 그 자체로 무거운 책임 — 캐시, 매니저, 리소스 보유자 — 을 지는 `object`라면 굳이 `data`를 붙일 이유가 없다.

---

## enumEntries — 무심코 호출하던 한 줄의 진짜 비용

```kotlin
enum class RGB { RED, GREEN, BLUE }

inline fun <reified T : Enum<T>> printAllValues() {
    print(enumValues<T>().joinToString { it.name })  // 1.9 시절
}
```

이 코드를 한 번 호출하면 어떤 일이 일어날까? `enumValues<T>()`는 *호출할 때마다 새 배열을 만든다.* JVM의 `Class.getEnumConstants()`가 내부 캐시를 깎아 새 배열로 복사해 돌려주기 때문이다. enum이 RGB 셋이라면 별 비용이 아니지만, 100개짜리 enum을 가진 코드가 핫 패스에서 매 호출마다 이 한 줄을 부른다고 해보자. 100칸 짜리 새 배열이 매번 힙에 올라가고, GC가 그만큼 일을 더 한다. 한참 들여다봐야 보이는, *조용한 비용*이다.

2.0의 `enumEntries<T>()`는 이 자리를 정확히 짚는다.

```kotlin
inline fun <reified T : Enum<T>> printAllValues() {
    print(enumEntries<T>().joinToString { it.name })  // 2.0 Stable
}
```

`enumEntries<T>()`는 *동일 인스턴스*를 반환한다. 같은 enum 타입에 대해 몇 번을 부르든, 돌려받는 `EnumEntries<T>`는 같은 객체다. 내부적으로 한 번 만들어둔 *불변 리스트*를 캐싱해 돌려주기 때문이다. 비용 비교를 거칠게 그려보면 이렇다.

| 호출 1만 회 시 | `enumValues<T>()` | `enumEntries<T>()` |
| --- | --- | --- |
| 새로 할당되는 배열 | 1만 개 (각각 enum 길이만큼) | 0 (첫 호출 후 캐시) |
| GC가 회수해야 할 객체 | 1만 개 | 0 |
| 반환 타입 | `Array<T>` | `EnumEntries<T>` (`List<T>`) |

추가로 따라오는 이득이 하나 더 있다 — `EnumEntries<T>`는 `List<T>`를 구현한다. `joinToString`, `forEach`, `map` 같은 컬렉션 API를 직접 받는다. 1.9 시절 `enumValues<T>().toList()`로 한 번 더 변환하던 자리가 사라진다. 한 번 더 일을 시키지 않게 된 셈이다.

리플렉션 기반 코드 — DSL 빌더, 직렬화, 환경 변수 매핑, 폼 유효성 검증 — 가 enum을 자주 훑는다면 이 한 줄을 갈아끼우는 일이 가장 손쉬운 GC 다이어트가 된다. 무심코 호출하던 한 줄의 진짜 비용을 들여다보고, 같은 한 줄을 *비용 없는 한 줄*로 다시 적자.

```kotlin
// before — 1.9
fun fromName(name: String): RGB? =
    enumValues<RGB>().firstOrNull { it.name == name }

// after — 2.0
fun fromName(name: String): RGB? =
    enumEntries<RGB>().firstOrNull { it.name == name }
```

코드 모양은 거의 같지만, 핫 패스에서 이 한 줄을 100만 번 부른 뒤 JVM 프로파일러를 띄워보면 차이는 눈에 보일 만큼 분명하다.

---

## AutoCloseable의 공통화 — KMP 작성에서 줄어드는 코드 양

KMP 공통 코드에서 자원을 다루는 자리를 떠올려보자. 1.9까지의 `kotlin.AutoCloseable`은 JVM 한정 — 안드로이드와 백엔드에서는 잘 됐지만, iOS, Native, Wasm 공통 코드에서는 쓸 수 없었다. 그래서 KMP 라이브러리 작성자들은 자기들만의 인터페이스를 다시 그렸다. `Closeable`, `Disposable`, `Cancelable`... 이름만 다르고 모양은 똑같은 것들이 라이브러리마다 따로 있었다.

2.0부터 `AutoCloseable`이 *공용*이다. 같은 인터페이스가 JVM, Native, JS, Wasm 모든 타깃에서 쓰인다.

```kotlin
// commonMain 에서 그대로 쓸 수 있다
class FileWriter : AutoCloseable {
    fun write(s: String) { /* ... */ }
    override fun close() { /* flush + release */ }
}

fun saveLog(message: String) {
    FileWriter().use { writer ->
        writer.write(message)
    }
}
```

여기서 한 발 더 — 2.0은 `AutoCloseable { ... }` 빌더 함수도 공용으로 제공한다. 이미 만들어진 닫기 동작을 한 줄로 감쌀 때 쓴다.

```kotlin
val cleanup = AutoCloseable {
    writer.flushAndClose()
}
cleanup.use { /* 본문 */ }
```

KMP 라이브러리 코드 양이 가장 직접적으로 줄어드는 자리다. 인터페이스 expect/actual 선언, 플랫폼별 구현 분기, 그 위에 얹은 `use { }` 헬퍼 — 이 셋이 *한 인터페이스 + 한 use 함수*로 정리된다. 5장에서 더 폭넓게 다룰 stdlib 흡수의 첫 신호이기도 하다.

---

## 다리 — 2.1이 던진 세 장의 카드로

이 셋(smart cast, data object, enumEntries)과 한 묶음(AutoCloseable)에는 공통점이 있다. *코드를 한 줄도 안 바꿔도 K2 활성만으로 행동이 바뀌거나, IDE 인스펙션 한 번으로 일괄 정리되는* 변화들이라는 점이다. "조용히 깔끔해지는" 부류다. 2.0이 가져온 무게감 있는 변화 — K2 컴파일러 교체, 빌드 스크립트의 재정렬 — 사이에 끼어 눈에 잘 띄지 않는 자리지만, 매일 짜는 코드의 결을 가장 자주 만지는 변화이기도 하다.

다음 장은 이 결과 다른 갈래다. 2.1이 던진 *세 장의 카드* — guard `when`, multi-dollar interpolation, non-local break/continue. 이쪽은 컴파일러가 알아서 따라오는 변화가 아니라, *우리가 새 문법을 손에 익혀야* 비로소 코드가 바뀌는 갈래다. Preview에서 시작해 Stable로 졸업하는 *시간 지도*까지 함께 살펴보자.

그 전에, 이번 장의 변화들을 자기 코드베이스로 한 번 흘려보내보자. IDE를 열고 K2 모드를 켰다면, *Unreachable code* 인스펙션과 *Convert object to data object* 인스펙션을 한 번씩 돌려보는 것으로 충분하다. 무심코 박아뒀던 한 줄들이 정리되는 자리에서, *조용히* 들어온 변화를 비로소 손끝으로 느낄 수 있다.

---

**마이그레이션 노트.** smart cast 강화로 *죽은 분기*가 된 `else throw IllegalStateException(...)` 패턴을 IDE *Unreachable code* 인스펙션으로 일괄 정리하고, `kotlin { compilerOptions { extraWarnings.set(true) } }`로 새로 떠오르는 경고를 한 묶음으로 모으자. 단계별 절차는 9장 9.2절 참조.
