# 4장. 2.1이 던진 세 장의 카드 — guard `when`, multi-dollar, non-local break

1.9 시절의 어느 오후를 떠올려 보자. sealed 계층을 펼치는 `when` 블록 앞에서 손가락이 멎는다. 분기는 분명히 타입으로 갈리는데, 정작 분기 안에서 다시 *조건* 하나가 갈린다. 그래서 작성하는 코드가 이런 모양이 되어버린다.

```kotlin
when (animal) {
    is Animal.Dog -> animal.feedDog()
    is Animal.Cat -> {
        if (!animal.mouseHunter) animal.feedCat()
        else println("쥐 잡는 고양이는 알아서 먹는다")
    }
    else -> println("Unknown animal")
}
```

문법적으로 틀린 데가 없다. 하지만 한 화면을 채우고 나면 어딘가 *난감하다*. `when`이 그어준 한 줄짜리 분기 위에 `if-else`라는 두 줄짜리 분기를 다시 얹은 모양새다. 분기 한 갈래가 굵어지면 굵어질수록, 다음 사람이 이 코드를 읽을 때 *어디까지가 어느 분기의 책임인지* 잠깐 멈춰서 따져봐야 한다.

JSON Schema 문서를 문자열로 직렬화해본 사람이라면 다른 종류의 *난감함*도 알 것이다. JSON Schema 키 이름은 하필이면 `$schema`, `$id`, `$ref`로 시작한다. Kotlin의 문자열 보간이 `$`를 *쓱* 가져가버리니, 키 하나하나 앞에 백슬래시를 덧붙여야 한다. `\$schema`, `\$id`, `\$ref`. 한두 줄이라면 참을 만하지만, 이게 한 페이지짜리 스키마가 되면 *백슬래시 도배*다. 그 사이에 진짜로 보간하고 싶은 변수까지 끼어들면, 코드를 읽는 시선이 슬래시 사이에서 길을 잃는다.

람다 안에서 *컨티뉴*를 쓰고 싶었던 순간도 있다. `for` 루프 안에서 nullable을 풀어내야 하는데, `?:` 한 번에 끝내고 싶다. 그런데 `?: continue`는 1.9에서 통하지 않는다. 람다 본문이라서 그렇다. 결국 우리는 이런 우회로를 짠다.

```kotlin
val v = element.nullableMethod() ?: run {
    log.warn("null이라 건너뛴다")
    null              // 우회용 더미
}
if (v == null) continue
// 이제부터 v를 쓴다
```

흐름은 두 단계다. 람다에서 `null`을 *돌려주고*, 다시 그 `null`을 *바깥에서 검사*해 진짜 `continue`를 발사한다. 코드가 두 번 손바닥을 친다. 한 번이면 될 일을. 이 패턴을 습관처럼 쓰다 보면 어느 순간 *찜찜한* 기분이 든다. 본질은 단순한데 우회만 자꾸 늘어난다.

이 변화는 누적 캐스케이드의 *공짜로 우아해진 것* 갈래에 속한다. 손을 거의 대지 않고도 코드의 결이 정돈되는 영역. 2.1이 던진 세 장의 카드 — guard `when`, multi-dollar interpolation, non-local `break`/`continue` — 가 정확히 이 자리에 떨어진다. 세 장이 모두 똑같은 코스를 밟았다는 점도 흥미롭다. *2.1 Preview에서 opt-in으로 잠깐 머물렀다가, 2.2에서 한꺼번에 Stable로 졸업*했다.

본격적으로 들어가기 전에 머릿속에 화두 셋을 깔아두자.

- 1.9 시절 `is X -> if (cond) ... else ...`로 중첩되던 sealed 분기, 이제 어떻게 펼칠 수 있을까?
- JSON Schema나 Bash heredoc을 문자열로 다룰 때 백슬래시로 도배되던 코드, 정말 깨끗해질 수 있을까?
- lambda 안에서 `continue`를 쓰고 싶어 `?: run { ...; null }`로 우회하던 그 패턴, 이제는 작별할 수 있을까?

세 질문에 답을 하나씩 얹어 보자.

## 첫 번째 카드 — guard `when`이 분기 위에 얹는 *그리고*

guard `when`은 KEEP-71140에서 출발해 Kotlin 2.1.0에 Preview로 들어왔다. 활성화하려면 컴파일러 플래그 `-Xwhen-guards`를 켜야 했다. 그러다 2.2.0에서 별도 플래그 없이 *Stable*로 승격됐다.

왜 *Preview*라는 한 사이클이 필요했을까? 한 가지 짚고 가자. `when` 분기에 `if`를 끼워 넣는다는 발상은 단순해 보이지만, 파서 입장에서는 모호해질 여지가 있다. 기존 `when` 안의 `->` 좌측에는 *값 또는 타입 패턴*만 오던 자리였고, 거기에 boolean 식이 들어간다는 건 문법의 결을 한 줄 더 만들어주는 일이다. JetBrains 입장에서는 이 자리에 정착할 단어를 신중히 골라야 했다. `where`, `&&`, `if` 후보가 한 번씩 거론된 끝에 `if`로 정해졌고, 한 메이저 사이클을 거치며 사용자 코드에서 어색함이 나오는 자리를 다듬었다. 이런 *말로는 단순한* 결정 한 줄에 KEEP 한 건과 Preview 사이클이 들어간다는 사실을 우리는 잠깐 짚어둘 만하다.

문법은 단출하다. 한 분기의 패턴 뒤에 `if`를 붙이고, 그 자리에 추가 조건을 얹는다.

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

여기서 일어나는 일이 무엇인지 차분히 살펴보자. `is Animal.Cat`까지가 *타입 패턴*이다. 그 뒤의 `if !animal.mouseHunter`는 *그 패턴이 매칭됐다는 전제 위에서* 동작하는 추가 조건이다. 그래서 `if` 절 안에서는 이미 `animal`이 `Cat`으로 스마트 캐스트되어 있고, `mouseHunter`에 곧장 접근할 수 있다.

도입부에서 본 1.9 버전과 한번 나란히 두자.

```kotlin
// 1.9
when (animal) {
    is Animal.Dog -> animal.feedDog()
    is Animal.Cat -> {
        if (!animal.mouseHunter) animal.feedCat()
        else println("쥐 잡는 고양이는 알아서 먹는다")
    }
    else -> println("Unknown animal")
}

// 2.2
when (animal) {
    is Animal.Dog -> animal.feedDog()
    is Animal.Cat if !animal.mouseHunter -> animal.feedCat()
    else -> println("Unknown animal")
}
```

차이가 단순한 *줄 수 절감*에 그치지 않는다는 점에 주목하자. 1.9 버전은 분기가 두 *층*으로 쌓여 있다 — 바깥의 `when`과 안쪽의 `if-else`. 2.2 버전은 모든 분기가 한 *평면*에 정렬돼 있다. 코드를 읽는 사람의 시선이 위에서 아래로 한 번에 흐른다. 분기가 넷, 다섯이 되더라도 *층층이 계단을 오르는* 일이 사라진다.

그렇다면 이전에는 왜 안 됐을까? `when` 분기 패턴은 본래 *값 또는 타입*을 매칭하는 자리라 그 자리에 임의의 boolean 식을 끼울 문법적 여백이 없었다. 그 빈자리에 `if`라는 한 단어를 합의해 끼워 넣었다. 사소해 보이지만, 이런 *단어 하나*가 들어오는 데 KEEP 한 건과 Preview 한 사이클이 든다.

또 한 가지 자주 마주치는 자리. 분기의 좌측이 *값* 매칭일 때도 guard가 붙는다. 예를 들어 결제 상태를 정수 코드로 받는 외부 시스템 연동 코드를 떠올려 보자.

```kotlin
// 1.9 — 값 + 추가 조건이 한 분기에 묶이지 않아 if-else로 풀어 적었다
when (code) {
    in 200..299 -> {
        if (body.isNotEmpty()) parseBody(body)
        else markEmptyOk()
    }
    in 400..499 -> handleClientError(code)
    else -> handleUnknown(code)
}

// 2.2 — guard 한 줄로 두 갈래를 평면에 펼친다
when (code) {
    in 200..299 if body.isNotEmpty() -> parseBody(body)
    in 200..299 -> markEmptyOk()
    in 400..499 -> handleClientError(code)
    else -> handleUnknown(code)
}
```

같은 범위 매칭이 두 줄로 갈라지는 게 어색해 보일 수 있지만, 한번 익숙해지고 나면 *어떤 조건일 때 어디로 가는지*가 한 평면에서 즉시 읽힌다. *분기를 두 줄로 적느라 내가 손해 봤다*는 느낌이 아니라, *분기의 의미를 두 줄로 받아 적었다*는 느낌이 든다. 코드 리뷰에서 "여기 안쪽 if는 무엇을 위한 거였더라" 하고 두 번 묻게 만드는 일이 줄어든다.

도입을 결정할 때 한 가지 기억해두자. opt-in 시절(2.1 Preview)에는 `-Xwhen-guards`를 켠 모듈에서만 동작한다. 라이브러리로 노출할 코드를 짠다면, 라이브러리 사용자가 그 플래그를 켜지 않은 상태로 빌드하더라도 깨지지 않을지 한번 의심해 볼 일이다. 2.2부터는 무플래그가 되었으니 이 고민은 자연스럽게 사라진다. *그저 쓰면 되는 시점*이 도래한 것이다.

## 두 번째 카드 — multi-dollar가 `\$` 도배를 끝낸다

JSON Schema 한 조각을 Kotlin 문자열에 박아넣는다고 해보자. 1.9에서는 거의 이런 모양이다.

```kotlin
// 1.9 — \$ 로 일일이 escape
val schema = """
{
    "\$schema": "https://json-schema.org/draft/2020-12/schema",
    "\$id": "https://example.com/${name}.json",
    "\$dynamicAnchor": "meta",
    "title": "${simpleName ?: "unknown"}",
    "type": "object"
}
"""
```

`$schema`, `$id`, `$dynamicAnchor` — JSON Schema 표준이 정한 키가 하필이면 모두 `$`로 시작한다. Kotlin은 문자열 안의 `$`를 *보간 시작 신호*로 본다. 그래서 키 하나하나 앞에 `\$`를 박는다. 이 코드를 한참 들여다보면 *진짜로 보간되어야 하는* `${name}`과 *그저 리터럴이어야 하는* `\$schema`가 시각적으로 잘 구분되지 않는다. 끔찍한 일이다.

multi-dollar interpolation은 KEEP-2425에서 출발해 똑같은 코스를 밟았다. 2.1.0 Preview(`-Xmulti-dollar-interpolation`) → 2.2.0 Stable. 핵심 아이디어는 단순하다. *몇 개의 `$`가 모이면 보간으로 칠 것인지*를 문자열을 여는 쪽에서 정한다.

```kotlin
val schema = $$"""
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.com/$${name}.json",
    "$dynamicAnchor": "meta",
    "title": "$${simpleName ?: "unknown"}",
    "type": "object"
}
"""
```

문자열을 `$$"""`로 열었다. 이제 보간 신호는 *달러 두 개*다. `$schema`는 달러가 하나뿐이라 그저 리터럴 텍스트로 살아남는다. 진짜로 변수를 박고 싶을 때만 `$${name}`처럼 두 개를 붙여 쓴다. JSON Schema 표준 키 전부가 백슬래시 없이 *원래 모양 그대로* 코드 안에 살게 된다.

비교를 좀 더 확실히 하기 위해 두 버전을 다시 한 화면에 두자.

```kotlin
// 1.9 — \$ 도배
"\$schema": "https://json-schema.org/draft/2020-12/schema",
"\$id": "https://example.com/${name}.json",
"\$dynamicAnchor": "meta",

// 2.2 — $$ 헤더 한 번이면 끝
"$schema": "https://json-schema.org/draft/2020-12/schema",
"$id": "https://example.com/$${name}.json",
"$dynamicAnchor": "meta",
```

JSON Schema뿐만이 아니다. Bash heredoc에서도 똑같은 일이 벌어진다. `$1`, `$@`, `$HOME` 같은 토큰이 죄다 `$`를 달고 있어, Kotlin 코드 안에 Bash 스크립트를 박아두려고 하면 슬래시 지옥이 또 한번 펼쳐진다. AsciiDoc, LaTeX, 또 Vue/Angular 같은 템플릿 언어에서 가져온 조각들도 사정이 비슷하다. 이런 자리마다 multi-dollar 한 줄로 escape를 *통째로* 걷어낼 수 있다.

`$$"""...."""`만 있는 게 아니라 `$$$`, `$$$$`까지 임의의 개수를 쓸 수 있다는 사실도 알아두자. 본문에 `$$`가 *진짜 두 개* 나오는 자료(예: jQuery의 `$$`)를 박아야 한다면 헤더를 `$$$"""`로 한 단계 더 밀어 올리면 된다. *문자열 한 덩어리 안에서 어떤 시퀀스를 보간으로 칠지*를 그때그때 골라 쓸 수 있는 셈이다.

여기서 잠시, 1.9 시절에 우리가 어떻게 이 문제를 *우회*해 왔는지를 떠올려 보자. 흔한 길이 두 가지 있었다. 첫째, 문자열 안에 *플레이스홀더*를 박고 나중에 `replace`로 치환하는 방식. 둘째, 외부 리소스 파일에 진짜 JSON Schema를 넣어두고 `getResourceAsStream`으로 읽어들이는 방식. 둘 다 동작은 했지만, 코드 *근처*에 스키마 텍스트가 없어 흐름을 따라 읽기가 번거로웠다. 본문에 `$schema` 한 줄이 없으면, 어떤 스키마 모양으로 직렬화되는지를 다른 파일을 *열어봐야* 안다. multi-dollar는 이 *원격성*을 한 단어로 끝낸다. 진짜 결과물의 모양 그대로를 코드 본문에 박아넣을 수 있게 해주니, 리뷰 시점에 다른 파일로 옮겨다닐 일이 사라진다.

한 가지 사소한 주의. `$$"""..."""`는 문자열 헤더에서 *원시 문자열* 셋(`"""`)을 그대로 살린다. 따옴표 한 개짜리 일반 문자열에 `$`를 일일이 escape하던 코드도 `$$"..."` 같은 식으로 적용할 수 있는지 궁금할 텐데, multi-dollar는 *어느 문자열 리터럴에든* 적용된다. 다만 한 줄짜리 문자열에 `$`가 한두 개 들어가는 정도라면 굳이 헤더를 늘려 보일 가치가 크지 않다. 백슬래시 한두 개로 충분히 가독성이 살아있는 자리에 *새 문법을 굳이 들이지 않는 편이 낫다.* 새 무기는 진짜 도배가 일어나는 자리에서만 꺼내 들자.

## 세 번째 카드 — `?: run { ...; null }`과의 작별

이 카드는 KEEP-1436. 같은 코스(2.1 Preview `-Xnon-local-break-continue` → 2.2 Stable)를 또 한번 밟는다. *inline lambda 안에서 비지역 `break`/`continue`를 허용*하자는 단순한 제안이다.

도입부의 우회 패턴을 다시 가져와서, 새 문법으로 다시 적어 보자.

```kotlin
// 1.9 — null 더미를 만들고 두 번 검사
fun processList(elements: List<Int>): Boolean {
    for (element in elements) {
        val v = element.nullableMethod() ?: run {
            log.warn("null이라 건너뛴다")
            null
        }
        if (v == null) continue
        if (v == 0) return true
    }
    return false
}

// 2.2 — run { } 안에서 곧장 continue
fun processList(elements: List<Int>): Boolean {
    for (element in elements) {
        val v = element.nullableMethod() ?: run {
            log.warn("null이라 건너뛴다")
            continue            // 람다 안에서 바깥 for 루프로 비지역 점프
        }
        if (v == 0) return true
    }
    return false
}
```

차이가 분명하다. 1.9 버전은 *람다가 `null`을 반환*하고, 그 `null`을 *바깥 함수가 다시 검사*해 `continue`를 던진다. 의도는 "이 원소는 건너뛴다"인데, 실제 흐름은 두 단계로 갈라진다. 2.2 버전은 그 의도가 한 줄로 직선화된다. `run` 람다 안에서 곧장 `continue`가 발사돼 바깥의 `for` 루프로 점프한다. *우리가 원래부터 쓰고 싶었던 그 한 줄*이다.

여기서 중요한 단서 하나. 비지역 `break`/`continue`는 *inline 람다*에서만 동작한다. `run`, `let`, `also`, `apply`, `with`, `forEach`처럼 표준 라이브러리에서 inline으로 정의된 함수가 그 대상이다. 일반 람다(=클래스 객체로 박스되는 람다)에서는 컴파일 타임에 바깥 루프와의 연결이 사라지므로, 비지역 점프가 원천적으로 불가능하다. 평소에 자주 쓰던 함수들은 거의 다 inline이라 큰 제약은 아니지만, 직접 만든 고차함수에서 이 문법을 기대하려면 *함수 시그니처에 `inline` 한 단어를 박아두는 편이 낫다.*

실무에서 자주 부딪히는 또 다른 자리, *forEach 안의 조기 종료*도 같은 결로 풀린다.

```kotlin
// 1.9 — forEach 안에서 break를 못 쓰니, 라벨을 박거나 일반 for로 되돌렸다
elements.forEach Outer@{ e ->
    val v = e.fetch() ?: return@Outer    // continue처럼 사용
    if (v.terminal) return@Outer         // break 흉내는 안 됨, 별도 flag로 처리
}

// 2.2 — 람다 안에서 곧장 break/continue
elements.forEach { e ->
    val v = e.fetch() ?: continue
    if (v.terminal) break
    process(v)
}
```

`return@Outer`가 *우회로*인 이유는 라벨이 *람다의 종료*만 가리킬 뿐, *바깥 루프의 종료*를 가리키지 못한다는 데 있다. break를 흉내 내려면 별도 플래그를 두고 *forEach가 끝난 다음*에 다시 검사하는 패턴을 짜야 했다. 두 단계로 갈라진 흐름이다. 비지역 `break`/`continue`는 이 두 단계를 *한 단어*로 합쳐준다.

도입할 때의 권고 하나. 비지역 `continue`/`break`가 들어가면 *람다의 흐름과 바깥 루프의 흐름이 한 곳에서 묶이는* 셈이라, 가독성을 위해 람다는 짧게 유지하는 편이 좋다. 람다 안에서 `continue`가 일어나는지 한눈에 보이지 않으면, 다음 사람이 흐름을 따라가다가 *난감해진다*. 새 무기일수록 짧게 들고 다니자. 람다가 두 화면을 넘어가기 시작하면, 비지역 점프가 들어 있는 자리부터 작은 함수로 추출하는 편이 바람직하다.

## 네 번째 카드처럼 다가오는 두 가지 — sealed exhaustiveness와 `@SubclassOptInRequired`

세 장의 카드가 메인이지만, 같은 2.1.0 릴리스에 함께 *Stable*로 들어온 두 가지를 같이 짚지 않으면 그림이 비어 보인다.

먼저 sealed 계층의 *exhaustiveness*가 한 단계 똑똑해졌다. 모든 케이스를 명시한 `when`이 있으면, `else` 없이도 표현식으로 통과한다. 문장이 짧다. 1.9까지는 다음과 같이 *쓸데없는* `else`를 박곤 했다.

```kotlin
// 1.9
val label = when (result) {
    is ReadResult.Number -> "number"
    is ReadResult.Text -> "text"
    ReadResult.EndOfFile -> "eof"
    else -> error("도달 불가")        // 컴파일러가 sealed를 다 못 따라가서 박았던 죽은 분기
}

// 2.1
val label = when (result) {
    is ReadResult.Number -> "number"
    is ReadResult.Text -> "text"
    ReadResult.EndOfFile -> "eof"
}
```

이 변화에 대해 한국 커뮤니티의 한 후기는 *"왜 이걸 2.1.0에 되서야 지원해 주지"* 라며 늦은 도입을 꼬집는다. 그 정서, 충분히 공감 간다. sealed의 본질이 *닫힌 계층*인데, 컴파일러가 그 닫힘을 *판별식 없이도* 인지하지 못해 줄곧 `else` 한 줄을 더 박아둬야 했던 것이다. 1.9까지의 코드베이스를 한 바퀴 둘러보자. *도달 불가*를 표시하던 `else throw IllegalStateException(...)` 같은 죽은 분기가 곳곳에 박혀 있을 것이다. 2.1로 올라오는 김에 IDE 인스펙션을 돌려 한꺼번에 정리해두는 편이 깔끔하다.

다른 하나는 `@SubclassOptInRequired`다. 라이브러리 작성자에게 새로운 무기 한 자루가 더 들어왔다. 기존의 `@RequiresOptIn`은 *어노테이션이 붙은 API를 호출하는 모든 자리*에 opt-in을 강제했다. 하지만 라이브러리를 쓰는 입장에서 보면 *함수를 호출하는 것*과 *클래스를 상속하는 것*은 위험의 결이 다르다. 호출은 표면적이고, 상속은 침습적이다. `@SubclassOptInRequired`는 이 결을 분리해 *상속 시점에만* opt-in을 강제한다.

```kotlin
@RequiresOptIn(level = RequiresOptIn.Level.WARNING)
annotation class UnstableApi

@SubclassOptInRequired(UnstableApi::class)
abstract class CoreEngine {
    /* 자유롭게 호출은 가능. 단 상속을 하려는 사람만 opt-in을 명시해야 한다. */
}
```

이 분리가 왜 *우아한가* 하면, 라이브러리 사용자에게 *불필요한 잔소리를 줄여*주기 때문이다. 인스턴스를 만들고 함수를 부르는 흔한 사용법은 그대로 두되, *상속이라는 깊은 결합*을 시도할 때만 한 번 더 손을 들게 한다. 라이브러리를 작성해 본 사람이라면, 이 한 어노테이션이 얼마나 갈증을 풀어주는지 짐작이 갈 것이다.

## 세 카드가 그린 *2.1 Preview → 2.2 Stable*이라는 코스

여기까지 보고 한 발짝 떨어져 보자. guard `when`, multi-dollar, non-local `break`/`continue` — 이 셋은 출처도 다르고 도메인도 다르다. 하나는 분기 문법, 하나는 문자열 문법, 하나는 제어 흐름 문법이다. 그런데 세 장 모두 *2.1.0에 Preview로 등장 → opt-in 플래그로 한 사이클 → 2.2.0에서 무플래그 Stable*이라는 똑같은 길을 걸었다.

이게 우연일까? 패턴이라고 보는 편이 맞다. Kotlin은 *새 언어 기능을 한 번에 박지 않는다*. 먼저 KEEP에 디자인을 띄우고, opt-in 컴파일러 플래그를 단 채로 한 메이저 사이클을 살려본다. 그 사이클 동안 *얼리 어답터*가 자기 모듈에 한정해 써보고, 라이브러리 작성자는 일반 사용자에게 노출하지 않은 채 시그니처만 다듬는다. 한 사이클이 지나면, 의견과 회귀 사례가 모인 자리에서 무플래그 Stable로 밀어 올린다.

그렇다면 우리가 *Preview 기능을 만났을 때 어떻게 결정해야 하는가*가 자연스럽게 따라온다. 다음 메이저에 어차피 Stable이 될 후보임은 거의 분명하다. 다만 이 Preview를 *프로덕션 코드*에 넣을지, *사이드 모듈*에만 넣을지, *공개 라이브러리*에는 절대 안 들일지 — 이 세 가지 결정은 별개로 가져가야 한다. 라이브러리는 사용자가 *우리가 켠 플래그*를 켜고 있을지를 보장할 수 없으니, opt-in 단계에서는 손을 대지 않는 편이 안전하다. 사이드 모듈이나 사내 프로덕션은 플래그를 켠 모듈 한 곳으로 *격리*해두면 회귀 시 롤백이 쉽다.

세 장의 카드 사례에 비추어 보면, 2.1 시점에 도입을 검토한다면 *옵트인 모듈 한 곳에서 시범 운용 → 2.2.0 출시와 함께 무플래그 사용으로 자연 전환*이라는 흐름이 가장 손이 적게 든다. 2.2에 이미 와 있는 코드베이스라면 고민할 거리도 없다. *그저 쓰면 된다.* 컴파일러가 알아서 한 평면으로 펼쳐 주고, 백슬래시를 떼 주고, 람다 한복판에서 `continue`를 받아준다.

## 마무리 — 손대지 않고도 결이 정돈되는 영역

세 카드를 한 번 더 정리하자. guard `when`은 sealed 분기를 *층에서 평면으로* 펼쳤다. multi-dollar는 JSON Schema와 Bash heredoc의 백슬래시를 *통째로* 걷어냈다. non-local `break`/`continue`는 람다 우회로 두 번 손바닥을 치던 패턴을 *한 줄*로 직선화했다. 셋 다 K2 컴파일러 자체가 가져온 *조용한 변화*는 아니다. 명시적인 새 문법이고, 명시적인 새 단어들이다. 그러나 도입할 때의 *비용*이 거의 들지 않는다는 점에서, 3장에서 본 smart cast 확장이나 `enumEntries` 같은 *공짜로 우아해진 것* 영역과 같은 자리에 둘 만하다.

마이그레이션 노트는 한 줄이다. **Preview 기능을 *프로덕션 / 사이드 / 라이브러리* 가운데 어디까지 들일지 선을 긋고, opt-in 플래그를 한 모듈 안으로 격리해두자. 단계별 도입 절차는 9장 9.2절을 참조하면 된다.**

세 카드가 모두 우아한 쪽으로 흘렀다는 건 다행한 일이다. 하지만 누적 캐스케이드의 다음 갈래는 이렇게 친절하지만은 않다. 5장에서는 *build.gradle에서 한 줄씩 사라지는 의존성들* 이야기로 넘어간다. 표준 라이브러리가 풍요로워지면서 외부 의존이 자연스럽게 빠져나가는 흐름인데, 이건 그래도 또 한 번 *공짜에 가까운* 영역이다. 진짜 비용이 청구되는 자리는 그 다음 6장과 7장에서 만나게 된다. 일단 4장의 카드 세 장을 손에 쥔 채로, 다음 페이지로 함께 넘어가 보자.
