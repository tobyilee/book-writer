# 8장. 2.3의 신호들 — backing fields, return-value checker, 그리고 그 너머

ViewModel을 한 번이라도 짜본 사람이라면 이런 모양의 코드에 익숙할 것이다.

```kotlin
class CityViewModel : ViewModel() {
    private val _city = MutableStateFlow("")
    val city: StateFlow<String> = _city.asStateFlow()

    fun updateCity(newCity: String) {
        _city.value = newCity
    }
}
```

한 줄짜리 상태 하나를 노출하기 위해 두 줄을 쓴다. 안쪽으로는 *쓸 수 있는* `MutableStateFlow`를 들고, 바깥으로는 *읽기 전용* `StateFlow`를 내민다. 같은 값을 가리키는 이름이 두 개다 — `_city`와 `city`. 언더스코어 한 글자가 *내부용*과 *외부용*을 가르고, `asStateFlow()`라는 보조 함수가 그 사이를 잇는다. 한 번 쓰면 손에 익지만, 가만히 들여다보면 어딘가 *어색하다*. 우리가 만들고 싶었던 건 *읽기는 누구나, 쓰기는 안에서만*이라는 한 줄짜리 의도였는데, 그걸 표현하려고 줄과 이름을 두 벌씩 들고 있다.

이런 자리에 앉아 있는 코드가 한 ViewModel만이 아니다. Repository에서 캐싱된 사용자 목록을 노출할 때도, Service에서 진행 상태를 흘려보낼 때도 같은 *두 줄* 패턴이 따라붙는다. `_users`/`users`, `_progress`/`progress`. 익숙해진 *어색함*이다.

또 다른 자리. `userRepository.findById(id)`처럼 값을 *돌려주는* 함수를 호출했는데, 그 반환값을 그냥 흘려보낸 코드를 본 적이 있을 것이다. 본인이 짠 코드에서도 그런 자리를 한두 군데는 발견하게 된다.

```kotlin
fun handleRequest(id: String) {
    userRepository.findById(id)   // 반환값을 받지 않는다
    notifyClient(id)
}
```

찾기만 하고 결과는 버린다. 의도였을까, 실수였을까? 이 코드를 며칠 뒤에 다시 보면 확신이 서지 않는다. 만약 의도였다면 *왜 굳이 호출하는가*가 본문 어디에도 적혀 있지 않고, 실수였다면 컴파일러는 한 마디도 잔소리하지 않았다. 이런 *조용한 실수*는 사실 우리가 1.9 시절부터 누적해 온 빚이다. Java에서 한참 전부터 IDE 인스펙션이 잡아주던 자리인데, Kotlin은 컴파일러 단에서 짚어주는 일을 미뤄두고 있었다.

이 변화는 누적 캐스케이드의 *그 후의 미래* 갈래에 속한다. 2.3 시점에서 얼굴을 내민 Experimental 신호들 — 그중 어떤 것은 다음 메이저(2.4)에서 Stable로 졸업하고, 어떤 것은 한 사이클 더 다듬어진 뒤에 합류할 것이다. 지금 우리가 할 일은 *가장 가까운 미래*가 어떤 모양으로 다가오는지를 미리 가늠하는 일이다. 본격적으로 들어가기 전에 머릿속에 화두 셋을 깔아두자.

- `_city`와 `city: StateFlow`로 두 줄을 쓰던 그 어색한 패턴, `field = ...` 한 줄로 정말 사라질까?
- Kotlin이 *함수의 반환값을 무시하지 마라*고 컴파일러 차원에서 잔소리를 하기 시작한 이유는 무엇일까?
- 2.3 시점의 Experimental 기능들, 그중 어떤 것이 *2.4 Stable*로 살아남을지 어떻게 가늠할까?

세 질문에 차례로 답을 얹어 보자.

## 첫 번째 신호 — explicit backing fields, `_` prefix의 종언

도입부의 ViewModel을 다시 가져와서, 2.3 Experimental 문법으로 다시 적어 보자. 이 기능을 켜려면 컴파일러 플래그 `-Xexplicit-backing-fields`를 추가해야 한다.

```kotlin
// 1.9 ~ 2.2 — 두 줄, 두 이름
class CityViewModel : ViewModel() {
    private val _city = MutableStateFlow("")
    val city: StateFlow<String> = _city.asStateFlow()

    fun updateCity(newCity: String) {
        _city.value = newCity
    }
}

// 2.3 Experimental — 한 프로퍼티, 한 이름
class CityViewModel : ViewModel() {
    val city: StateFlow<String>
        field = MutableStateFlow("")

    fun updateCity(newCity: String) {
        city.value = newCity      // 클래스 내부에서는 backing field 타입(MutableStateFlow)으로 접근
    }
}
```

이 한 단어 — `field = ...` — 가 무엇을 바꾸어 놓는지 차분히 살펴보자. 본래 Kotlin에는 `field`라는 *암묵적 이름*이 이미 있었다. property의 getter/setter 본문 안에서 backing field를 가리키던 그 키워드 말이다. 다만 그 *암묵적 field*는 프로퍼티의 외부 타입과 *같은 타입*만 가질 수 있었고, 그래서 `MutableStateFlow`를 안에 두고 `StateFlow`만 바깥으로 내보내는 패턴은 표현할 길이 없었다. explicit backing fields는 바로 이 자리에 *명시적인* `field` 선언을 들여놓는다. 외부 타입은 `StateFlow<String>`, 내부 타입은 `MutableStateFlow<String>`. 두 타입이 한 프로퍼티에 *공식적으로* 동거하게 된 셈이다.

호출 시점에 일어나는 일도 직관적이다. *클래스 바깥*에서 `viewModel.city`라고 쓰면 `StateFlow<String>`이 반환된다. *클래스 안*에서 `city`라고 쓰면 `MutableStateFlow<String>`이 반환된다. 같은 이름이지만, 보는 사람의 위치에 따라 타입이 달라진다. 이전 패턴에서 `_city`와 `city`로 갈라놓던 그 *경계*를 컴파일러가 자기 일로 흡수한 것이다.

차이가 단순한 *줄 수 절감*에 그치지 않는다는 점에 주목하자. 두 줄이 한 줄이 된 건 보이는 변화지만, 보이지 않는 변화가 더 크다. 첫째, *이름이 하나*라는 사실 — `_city`라고 적을 자리가 사라지면서 *읽기 이름*과 *쓰기 이름*을 헷갈릴 일이 없어진다. 둘째, `asStateFlow()` 같은 보조 호출이 *시야에서* 사라진다. 의도가 *프로퍼티 선언 한 자리*에 모인다. 셋째, `private val _city`라는 *사적인 흔적*이 클래스 헤더에서 보이지 않는다. 외부 API 표면에 *읽기 전용 타입*만 남는 것이다.

물론 이 기능이 만능은 아니다. 7장에서 짧게 짚었지만, *backing field/initializer/delegation을 가진 property*에는 context parameter를 동시에 둘 수 없다는 제약이 있다. 두 신기능이 같은 자리에서 만났을 때의 우선순위를 조율할 시간이 더 필요한 것이다. 그래서 explicit backing fields는 2.3에서 Stable이 *아니라* Experimental로 들어왔다. 컴파일러 플래그 `-Xexplicit-backing-fields`를 켠 모듈에서만 동작한다.

도입을 결정할 때의 권고. 라이브러리 코드라면 이 플래그에 의존하는 자리는 *피하는 편이 낫다*. 사용자가 그 플래그를 켜고 빌드하리라는 보장이 없다. 사내 애플리케이션 코드라면, ViewModel이나 Repository처럼 *읽기/쓰기 분리*가 반복되는 모듈 한 곳에 좁게 들여 시범 운용해 볼 만하다. 2.4에서 Stable로 졸업할 가능성이 높은 후보이니, *지금 한 모듈에서 손에 익혀두고 졸업과 함께 점진 확산*이라는 흐름이 손이 가장 적게 든다.

한 가지 사소한 주의. 기존 `_city` 패턴에서 explicit backing fields로 옮길 때, *자동 마이그레이션 도구*는 아직 본격적이지 않다. IDE 인스펙션이 일부 자리는 잡아주지만, `asStateFlow()` 호출 위치나 `setValue` 형태의 사용처까지 한꺼번에 바꿔주지는 못한다. 한 클래스씩 직접 손을 대는 편이 안전하다. 새 무기일수록 짧게 들고 다니자.

## 두 번째 신호 — Unused Return Value Checker, *조용한 실수*에 대한 잔소리

도입부의 `userRepository.findById(id)` 자리를 다시 가져오자. 2.3 Experimental의 *Unused Return Value Checker*는 이 코드를 더는 조용히 흘려보내지 않는다. 컴파일러 플래그 `-Xreturn-value-checker=check`를 켠 다음, 함수에 `@MustUseReturnValues`를 붙이거나 파일 상단에 `@file:MustUseReturnValues`를 박으면 된다.

```kotlin
@file:MustUseReturnValues

class UserRepository {
    fun findById(id: String): User? = ...
    fun save(user: User): User = ...
}

fun handleRequest(id: String) {
    userRepository.findById(id)   // 경고: return value를 사용하지 않는다
    notifyClient(id)
}
```

같은 코드가 어제까지는 통과했고 오늘부터는 빨간 줄을 받는다. 이 *컴파일러의 잔소리*가 왜 이제 와서 들어왔을까? Kotlin이 *함수형* 언어의 결을 강하게 들고 있는 데서 그 답이 나온다. 함수가 값을 *돌려준다*는 건, 그 값을 호출자가 *받아 쓰는 일*까지가 한 묶음이라는 뜻이다. 받아 쓰지 않는 호출은 둘 중 하나다 — 부수효과만을 노린 호출이거나, 실수다. 컴파일러는 두 가지를 구분할 길이 없으니, 그동안은 어느 쪽이든 그저 통과시켰다.

이제는 다르다. `@MustUseReturnValues`가 붙은 함수의 반환값을 받지 않으면 진단이 발생한다. 그렇다면 *의도적으로* 무시하고 싶을 때는 어떻게 할까? Kotlin이 마련해 둔 관용은 깔끔하다.

```kotlin
val _ = computeValue()    // "이 반환값은 일부러 무시한다"는 명시적 신호
```

언더스코어로 받는 한 줄이다. 이름 없는 변수에 *받아두기*만 하고 더는 쓰지 않는다. 코드를 읽는 사람에게 "이 자리는 의도적으로 흘려보낸 자리"임을 즉시 알린다. *말 없는 무시*와 *말 있는 무시*가 시각적으로 갈라지는 셈이다.

이 변화의 적용 범위에 대해 한 가지 짚자. 표준 라이브러리 함수 *전부*가 하루 아침에 `@MustUseReturnValues`를 입는 건 아니다. 2.3 시점에서는 *opt-in*이다. 자기 코드베이스에 어디까지 잔소리를 들이고 싶은지를 어노테이션 단위로 고를 수 있다. 가장 손쉬운 길은 도메인 모델·리포지토리·서비스 같은 *읽기 위주* 모듈의 파일 상단에 `@file:MustUseReturnValues` 한 줄을 박는 것이다. 그 한 줄이 그 파일 안 모든 함수의 반환값에 *책임지고 받자*는 약속을 건다.

1.9 시절과 한번 나란히 두자.

```kotlin
// 1.9 ~ 2.2 — 컴파일러 침묵
fun deactivate(user: User) {
    user.copy(active = false)   // 새 인스턴스를 만들었지만 받지 않음 — 실수다
    save(user)                   // 결국 active = true 인 채로 저장
}

// 2.3 Experimental + @MustUseReturnValues
fun deactivate(user: User) {
    user.copy(active = false)   // 경고: return value를 사용하지 않는다
    save(user)
}
```

이 차이가 진짜로 빛을 발하는 자리는 *불변(immutable) 자료형* 영역이다. `data class`의 `copy`, `kotlinx.collections.immutable`의 `add`/`remove`, `String`의 `replace` — 모두 *원본을 수정하지 않고 새 값을 돌려준다*. 그 새 값을 받지 않으면, 코드는 *아무 일도 하지 않은 채* 다음 줄로 넘어간다. 이 *조용한 무동작*은 1.9 시절부터 한국 커뮤니티에서도 자주 회자되던 단골 함정이다. *불변이라는 사실을 알면서도, 호출 자리에서 변수를 받지 않은 채 끝나버리는* 그 한 줄.

`@MustUseReturnValues`는 이 함정을 컴파일러 단에서 막아준다. 새 인스턴스를 받지 않은 자리가 즉시 빨간 줄로 떠오른다. *부수효과 호출*이라면 명시적으로 `val _ =`로 받아 의도를 표시한다. 코드의 *의도*가 본문 표면에 드러나기 시작하는 것이다.

도입할 때의 권고 하나. 처음부터 코드베이스 전체에 `-Xreturn-value-checker=check`를 켜는 건 권장하지 않는다. 누적된 *조용한 실수*가 한꺼번에 빨간 줄로 떠올라 *경고의 홍수*가 된다. 도메인 모델 한 모듈, 또는 *최근에 쓰인 서비스 클래스* 한 묶음에서 시작해 위에서 아래로 내려가며 정리하는 편이 *현실적이다*. 한 모듈씩 내 코드의 *침묵하던 자리*를 들여다보는 일이라고 생각하자.

## 2.3에서 Stable이 된 신호들 — data-flow exhaustiveness, expression body return

위 두 가지가 *2.4를 향한 가늠*이라면, 2.3에는 한 메이저 사이클을 거쳐 *졸업한* 신호도 있다. 이 둘은 2.2.20에서 Experimental/Beta로 처음 등장해 2.3에서 무플래그 Stable로 들어왔다.

먼저 *data-flow exhaustiveness*. `when`이 *앞 분기의 데이터 흐름*을 인지하기 시작했다는 이야기다.

```kotlin
enum class Role { ADMIN, MEMBER, GUEST }

// 1.9 ~ 2.2 — 앞에서 ADMIN을 걸렀어도 컴파일러는 모름, else 필요
fun limit(role: Role): Int {
    if (role == Role.ADMIN) return 99
    return when (role) {
        Role.MEMBER -> 10
        Role.GUEST -> 1
        else -> error("도달 불가")    // ADMIN이 이미 빠졌는데도 박아야 했다
    }
}

// 2.3 Stable — 앞 흐름을 컴파일러가 따라간다
fun limit(role: Role): Int {
    if (role == Role.ADMIN) return 99
    return when (role) {
        Role.MEMBER -> 10
        Role.GUEST -> 1
        // else 없음 — 컴파일러는 ADMIN이 이미 처리됐음을 안다
    }
}
```

4장에서 다룬 sealed exhaustiveness 개선이 *닫힌 계층*의 모든 케이스를 명시했을 때 `else`를 떼주는 일이었다면, 이쪽은 한 발 더 나아간다. *함수 안의 흐름*까지 컴파일러가 따라가, 앞 분기에서 이미 처리된 케이스를 빼고 남은 자리를 *exhaustive로 인정*한다. 사람이 머릿속으로 자연스럽게 따라가던 흐름을 컴파일러가 이제야 따라잡은 셈이다. 한국 커뮤니티에서 *"왜 이걸 이제야"* 라는 정서가 또 한 번 들 만한 자리다.

다음은 *expression body의 `return` 허용*. 함수 본문이 한 식으로 끝나는 *표현식 본문* 안에서, 그 표현식 한복판에 `return`을 박을 수 있게 됐다.

```kotlin
// 1.9 ~ 2.2 — expression body 안에서 return 불가, block body로 풀어야 했다
fun greet(id: String?): String {
    if (id == null) return "default"
    return greetUser(id)
}

// 2.3 Stable — expression body 안에서 곧장 return
fun greet(id: String?): String = greetUser(id ?: return "default")
```

이 한 줄이 의미하는 건, *조기 반환*과 *표현식 본문*이 더 이상 서로를 밀어내지 않는다는 사실이다. 1.9 시절에는 둘 중 하나를 골라야 했다 — 표현식 본문을 포기하고 block body로 내려가거나, 조기 반환을 포기하고 `?:` 다음에 *기본값*을 박거나. 2.3은 둘을 한 자리에서 함께 쓰게 해 준다. 다만 한 가지 단서. 표현식 본문 안에 `return`이 들어가려면 *명시적 반환 타입*이 필요하다. 컴파일러가 추론할 여백이 없는 자리이기 때문이다. `fun greet(id: String?) = ...`이 아니라 `fun greet(id: String?): String = ...`로 적자.

이 두 가지가 2.2.20 → 2.3 Stable의 *졸업 코스*를 똑같이 밟았다는 점을 짚어두자. 4장의 guard `when` / multi-dollar / non-local break 셋이 *2.1 Preview → 2.2 Stable* 코스를 한 묶음으로 밟았던 것과 같은 모양이다. 한 사이클의 opt-in을 거친 뒤 무플래그 Stable로 들어오는 *반복되는 패턴*. Kotlin이 새 언어 기능을 들이는 *방식 자체*가 굳어지고 있다는 신호다.

## 라이브러리 작성자용 신호들 — `@JvmExposeBoxed`, annotations in metadata

2.3 Experimental 명단에는 *라이브러리 작성자* 쪽에서 더 무겁게 받아들여질 묶음도 있다. 일반 애플리케이션 개발자에게는 *얼굴 내미는 정도*로만 짚어두자.

`@JvmExposeBoxed`는 Kotlin의 value class를 *Java에서 쓸 수 있게* 박싱된 변형을 노출한다. value class는 본래 *런타임 박싱을 피하기 위해* 만들어졌지만, 그 정직함이 Java 측 사용자에겐 도리어 장벽이 됐다. value class를 가진 함수의 시그니처가 Java 입장에서 *읽히지 않는* 자리가 생기곤 했다. `@JvmExposeBoxed`는 *런타임 효율*과 *Java 호환*을 한 어노테이션으로 동시에 챙기는 길을 열어준다. KMP 라이브러리를 짜는 입장에서는 *우리 라이브러리를 Java에서도 부르는 사용자가 있는가*를 한 번 더 생각하게 만드는 신호다.

*annotations in Kotlin metadata*도 같은 결이다. `KotlinClassMetadata`로 어노테이션을 *읽는* 길이 열린다. 컴파일러 플러그인을 짜거나, 리플렉션 기반 도구를 만드는 사람에게는 새로운 무기가 된다. 외부 의존 없이 Kotlin 메타데이터에서 직접 어노테이션 정보를 끌어올 수 있게 된다는 의미다. Plugin 작성자에게는 *덜 유용한 우회로*를 한 묶음 줄여주는 변화다.

이 둘 모두 2.2.20에서 등장한 Experimental인데, 2.3에서도 *그대로* Experimental로 남아 있다. 한 사이클이 더 필요하다는 판단이다. 2.4에서 Stable로 갈지, 아니면 더 다듬어진 후보로 한 사이클을 더 살지는 *KEEP*과 *KotlinConf 2025*의 후속 발표를 따라가며 가늠하면 된다. 라이브러리를 짜는 입장이 아니라면 *이런 신호가 있다*는 정도로 머릿속 한쪽에 메모해 두자.

여기에 함께 짚어둘 만한 두 가지가 더 있다. 2.2.20에서 등장한 *suspend function type 오버로드 해소*는 `transform({ 42 })`와 `transform(suspend { 42 })`가 같은 함수의 다른 오버로드로 명확히 갈리도록 정리해 준다. 코루틴 기반 라이브러리를 짤 때 시그니처 충돌로 *왜 이 오버로드가 우선 매칭되는지* 한참 따져야 했던 자리가 줄어든다. *catch 블록의 reified 제네릭*도 같은 시점에 들어왔다. `inline fun <reified E : Throwable> handle(...)` 안에서 `catch (e: E)`처럼 reified 타입을 그대로 받을 수 있게 되었다. 예외 타입을 제네릭으로 받아 처리하는 헬퍼 함수를 만들 때 *우회로*가 한 단계 줄어든 셈이다.

## *Preview → Stable* 패턴으로 2.4 가늠하기

여기까지 보고 한 발짝 떨어져 보자. 2.3 Experimental 명단을 다시 펼친다.

- explicit backing fields
- Unused Return Value Checker (`@MustUseReturnValues`)
- UUID v7 / v4 명시 생성 (`Uuid.generateV4()`, `Uuid.generateV7()` 등)
- `@JvmExposeBoxed`
- annotations in Kotlin metadata
- JS — Suspend function export, `BigInt64Array`로 LongArray 표현

이 중 어떤 것이 2.4 Stable로 졸업할까? 직접적인 답은 KotlinConf 2025와 KEEP 진행 상황을 따라가야 나오겠지만, *과거의 패턴*으로 가늠하는 길은 있다. Kotlin은 한 메이저 사이클의 opt-in 이후 무플래그 Stable로 밀어 올리는 *습관*을 굳혀 왔다.

- 2.1 Preview → 2.2 Stable 졸업생: guard `when`, multi-dollar interpolation, non-local break/continue.
- 2.2 Preview → 2.3 Stable 졸업생: data-flow exhaustiveness for `when`, expression body의 `return`, nested type aliases, `kotlin.time.Clock`/`Instant`.

이 두 묶음의 모양을 한번 들여다보자. 둘 다 *문법 차원의 ergonomics*거나, *표준 라이브러리 흡수* 둘 중 하나다. 이 두 카테고리에 속하는 2.3 Experimental은 *졸업 가능성이 높다*. explicit backing fields는 첫 번째 카테고리(문법 ergonomics)에 정확히 속한다. UUID v7는 두 번째(표준 라이브러리 흡수)에 속한다.

반대로 *행동 강제* 성격의 변화 — 즉 기존 코드에 *경고*나 *에러*를 새로 박아넣는 것 — 는 한 사이클을 더 두고 가는 경향이 있다. Unused Return Value Checker가 그 결이다. 이 기능이 무플래그 Stable이 되는 순간 코드베이스 전체에 *수십, 수백 개의 경고*가 한꺼번에 떠오를 수 있다. JetBrains는 이런 변화를 *한 번에 밀어 넣지 않는다*. opt-in으로 한 사이클을 살린 뒤, 그 사이에 라이브러리 측이 자기 함수에 `@MustUseReturnValues`를 붙여 *준비*하는 시간을 준다. 2.4에서 Stable이 될 가능성도 있고, 한 사이클을 더 둘 가능성도 있다. 어느 쪽이든 *지금 후보 모듈 한 곳에서 익혀두는 일*은 손해 보지 않는다.

`@JvmExposeBoxed`와 annotations in metadata 같은 *라이브러리 작성자용* 변화는 가늠이 더 어렵다. 사용자 베이스가 좁고, 컴파일러 플러그인 생태계의 채택 속도가 변수다. 이 묶음은 2.4보다 그 다음 메이저까지 시야를 늘려 보는 편이 *바람직하다*.

이 패턴 자체가 우리에게 알려주는 큰 메시지가 하나 있다. *Preview → Stable의 시간 지도는 우연이 아니라 패턴*이다. 그렇다면 우리가 해야 할 일도 분명해진다. 2.3 Experimental을 *지금* 도입하되, 한 모듈로 좁게 격리해두는 일이다. 2.4가 그 졸업생을 안고 도착하면, 격리해 둔 모듈 하나를 *플래그만 떼는* 형태로 자연 전환할 수 있다. 그 자리에서 우왕좌왕할 일이 사라진다.

## 마무리 — *그 후의 미래*에서 마이그레이션 플레이북으로

2.3은 *stable + ergonomics*라는 한 줄로 요약된다고 JetBrains는 말한다. 4장이 우리에게 손에 쥐여준 세 카드(guard `when`, multi-dollar, non-local break)가 한 사이클의 졸업생이었다면, 8장은 *다음 한 사이클의 후보들*이다. explicit backing fields는 `_city` 두 줄을 한 줄로 줄여줄 *어색함의 종결자*가 될 가능성이 높고, Unused Return Value Checker는 우리가 1.9 시절부터 누적해 온 *조용한 실수*에 컴파일러의 잔소리를 들여놓는 변화다. data-flow exhaustiveness와 expression body return은 이미 무플래그 Stable로 들어와 있으니, 코드베이스가 2.3에 이미 와 있다면 *그저 쓰면 된다*. 라이브러리 작성자용 신호들은 좀 더 긴 호흡으로 가져가자.

Preview → Stable 패턴이 우리에게 가르쳐준 건 결국 한 가지다. *Kotlin은 한 사이클을 살린다.* 우리도 같은 호흡으로 가야 한다. 한 모듈에 좁게 들이고, 한 사이클을 살려 보고, 다음 메이저에서 자연 전환을 받는다. 이 흐름이 손에 익으면, *2.4를 무엇이 가져올까*라는 질문 앞에서 우리는 더는 짐작하지 않게 된다. 우리 코드베이스가 이미 그 답의 절반을 *시범 운용* 중일 것이기 때문이다.

여기까지 1장에서 8장까지, 우리는 K2의 등장(2장), 조용한 일상의 변화(3장), 2.1이 던진 세 카드(4장), build.gradle에서 사라지는 의존성(5장), 컴파일 에러로 변한 deprecation(6장), context receivers의 묘비명과 context parameters의 첫걸음(7장), 그리고 2.3의 신호(8장)까지 *변화 카테고리별*로 한 바퀴를 돌았다. 이제 9장에서는 이 모든 변화를 *시간 순서*로 다시 묶어 본다. *1.9에서 2.3까지 네 번의 점검*이라는 단계별 마이그레이션 플레이북. 어느 단계에서 무엇을 가장 먼저 부딪히고, 어디에 롤백 안전망을 깔아두면 *어느 단계에서든 후퇴*할 수 있는지 — 그 지도를 함께 펼쳐 보자.

**마이그레이션 노트(1줄 액션):** 2.3 Experimental(`-Xexplicit-backing-fields`, `-Xreturn-value-checker=check`, `@MustUseReturnValues`)은 *후보 모듈 한 곳*에 좁게 들이고, opt-in 어노테이션과 컴파일러 플래그를 그 모듈 경계 안에서 끝내자. 2.4 Stable 전환을 점검하는 절차는 9장 9.4절을 참조하면 된다.
