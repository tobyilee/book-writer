# 7장. context receivers의 묘비명, context parameters의 첫걸음

arrow-kt에 빠져 있던 시절을 한 번 떠올려 보자. `Raise<E>.()` 한 줄을 함수 앞에 붙이면, 그 안쪽에서는 `raise(MyError)`도 `bind()`도 *그저 호출*된다. 점도 없고 수신자도 없다. 같은 결로, 사내 도메인 코드에서도 `context(Logger)`나 `context(Transaction)`을 함수 위에 살짝 얹어 두면 본문이 더없이 깔끔해졌다. `info("...")`, `commit()` 한 줄에 받침이 따로 보이지 않는 그 느낌. *받침대를 깔아 두면 그 위에서는 그냥 걷는다* — context receivers를 처음 만났을 때의 인상이 그랬다.

문제는 그 받침대가 빌드 로그에서 *조용히 흔들리기 시작했다는 것*이다.

```text
w: '-Xcontext-receivers' compiler option is deprecated.
   Please migrate to context parameters.
   See https://kotl.in/context-parameters
```

2.0.20부터 시작된 이 한 줄은 처음에는 *언젠가 고치면 되는* 노란 줄로 보였다. 그런데 What's new 2.3 페이지를 한 번 들춰보면 그 노란 줄의 운명이 명확하다 — *2.3 무렵 제거*. 이미 묘비명이 새겨지는 중이다. 우리가 즐겁게 쓰던 `context(Logger) fun foo() = info("bar")` 한 줄은, 다음 마이너 두어 번 안에 *컴파일 자체가 안 되는 코드*가 된다. 새 받침대인 context parameters가 그 자리에 올라오는데, 들어 보면 결이 미묘하게 다르다 — *이름을 강제*한단다. 같은 자리에서 같은 일을 하는데, 함수 본문이 한 단어 더 길어진다.

아쉽다. 그런데 어쩔 수 없다는 것도 안다. 이 변화는 누적 캐스케이드의 *비싸게 치러야 하는 것* 갈래에 속한다. 5장에서 build.gradle의 의존성이 한 줄씩 사라지던 *공짜 풍요*나 4장의 세 카드 같은 *공짜 우아함*과는 결이 다르다. 6장의 `kotlinOptions`처럼 한 줄짜리 치환으로 끝나는 영역도 아니다. 시그니처가 바뀌고, 호출 본문이 다시 쓰이고, 라이브러리 작성자라면 *dual API* 기간을 어떻게 둘지까지 결정해야 한다. 비용이 가장 무겁게 청구되는 자리가 7장이다.

본문에 들어가기 전에 화두 셋을 깔아 두자.

- `-Xcontext-receivers`로 즐겁게 쓰던 코드가 2.3에서 사라진다면, 우리는 무엇을 잃고 무엇을 얻는가?
- context parameter에 *이름*을 강제한 결정은 옳았을까? scope pollution은 정말 그만한 대가였을까?
- arrow-kt의 `Raise<E>.()` 같은 receiver-heavy 라이브러리는 어떻게 마이그레이션해야 할까?

세 질문을 들고 묘비명 앞에 한 번 서 보자.

## context receivers의 짧은 역사 — 왜 묘비명이 됐나

context receivers가 정식 기능이었던 적은 한 번도 없다. 1.6.20 시절 `-Xcontext-receivers` 라는 컴파일러 플래그 뒤에서 *prototype*으로 살아났고, 그 자리에서 한 번도 Stable로 졸업하지 못한 채 deprecate를 맞이했다. JetBrains의 시간표는 이렇다 — 2.0.20에서 deprecation이 *명시적으로* 시작됐고, *2.3 부근에 제거*가 예정돼 있다. KEEP-259(context receivers)는 KEEP-367(context parameters)에 자리를 내주며 *폐기 표지*가 붙었다. 시간 순서로 한 번 적어 두자.

- **1.6.20 (2022 봄)** — `-Xcontext-receivers` 플래그 뒤에서 prototype 도입.
- **1.7.0 ~ 1.9.x** — 플래그 뒤에서 광범위하게 실험. arrow-kt를 비롯한 라이브러리가 적극 도입.
- **2.0.20 (2024-08)** — 컴파일러 경고로 deprecation 명시 시작. KEEP-367(context parameters) 디자인 공개.
- **2.2.0 (2025-06)** — context parameters가 Preview(`-Xcontext-parameters`)로 등장. 두 받침대가 *한 코드베이스 안에 공존*하는 시기 시작.
- **2.3 (2025-12 부근)** — context receivers 제거 예정. 사용자 코드는 *컴파일 자체가 멈춘다*.

처음 듣는 사람에게는 좀 잔인한 소식이다. *플래그 뒤에 숨어 있던 기능이 졸업도 못 하고 사라진다*는 이야기다. 한국 커뮤니티의 한 후기는 이런 정서를 *"실험적 기능을 너무 적극적으로 끌어들였던 우리의 PR 한 묶음이 통째로 부채가 됐다"*고 적었다. 같은 마음이 든다면, 우리만 그런 건 아니다. arrow-kt 같은 라이브러리도, 사내 도메인 DSL도, 같은 시기에 같은 부채를 안고 마이그레이션 사이클을 돈다.

그런데 KEEP 디자인 문서를 한 번 들춰보면, JetBrains가 왜 이 결정에 이르렀는지가 차분히 적혀 있다. *기능 자체가 잘못됐다*는 이야기는 어디에도 없다. 다만 implicit receiver라는 *모양*이 큰 코드베이스에서 *예상보다 비싸다*는 사실이 도입 후 2년쯤 지나며 분명해졌고, 그 비용을 다른 모양으로 옮긴 것이 KEEP-367이라는 이야기다. 우리도 이 자리에서 한 번 짚고 가자.

context receivers의 가장 큰 매력은 *implicit receiver*였다. 함수 앞에 `context(Logger)`라고 적으면, 본문 안의 `info("...")`가 *어디에서 온 누구*인지 굳이 묻지 않고도 호출됐다. 깔끔했다. 그런데 이 *어디에서 왔는지를 묻지 않는다*는 점이 이 기능의 첫 약점이기도 했다.

함수 본문이 길어지는 순간을 떠올려 보자.

```kotlin
// 1.x context receivers (deprecated)
context(Logger, Transaction, UserService)
fun handleSignup(email: String) {
    info("새 가입 시도: $email")        // Logger의 것?
    val id = createUser(email)         // UserService의 것?
    log("DB에 user $id 생성")          // Logger? Transaction?
    commit()                           // Transaction의 것?
}
```

본문 한 줄 한 줄이 *세 받침대 중 어느 것 위에서* 호출되는지가 *시각적으로 사라진다*. KEEP-367은 이 상태를 *scope pollution*이라고 부른다. receiver가 셋 쌓이고 나면, IDE 자동완성 목록은 세 인터페이스의 멤버를 한 통에 부어버리고, 코드를 읽는 사람의 시선은 점점 *이게 어디에서 온 누구의 메서드지?*를 한 번씩 더 묻게 된다. 처음에는 우아해 보였는데, 한 함수가 두 화면을 넘어가기 시작하면 *찜찜한* 기분이 든다.

두 번째 약점은 *callable reference의 모호성*이었다. `::foo`를 쓰면 어느 receiver를 적용한 것인지 컴파일러가 결정할 자리에 빈자리가 생긴다. context receiver 버전에서는 이 자리에 *implicit*가 끼는 바람에, 라이브러리 작성자가 시그니처를 노출하기에도, 사용자가 *그 시그니처가 정확히 무엇인지*를 읽기에도 까다로웠다. 함수 시그니처를 *말로 적어 보라*고 하면 두 번 멈칫하게 된다. 같은 함수에 `Logger`와 `Transaction` 두 개의 context를 단 채 callable reference로 넘기면, 컴파일러는 *어느 receiver를 어느 자리에 매핑할지*를 결정해 줘야 한다. 이 결정의 모양이 1.x context receivers에서는 KEEP 디자인 시점부터 *명확히 합의되지 않은 자리*였다.

세 번째는 *IDE 추적성*이다. context receiver는 implicit이라 호출 지점에서 "Go to declaration"을 눌렀을 때 *어떤 인터페이스의 어떤 멤버*로 가는지가 K1 시절에는 종종 정확하지 않았다. K2/FIR 위에서 어느 정도 개선됐지만, 본질적으로 *이름이 없는 receiver*를 추적해야 한다는 부담 자체는 사라지지 않는다. 한 함수 안에서 `info(...)` 한 줄을 보고 *이게 어느 Logger의 info인지*를 판단하려면, 사람도 IDE도 *밖으로 한 번 더 나가서* receiver 목록을 다시 들여다본다. 한두 번이라면 괜찮지만, 코드 리뷰 한 번에 다섯 번씩 같은 동작을 반복하게 되면 *번거롭다*.

네 번째는 본질적인 *조합 문제*다. context receivers 위에 다시 context receivers를 쌓는 *중첩 패턴* — 예컨대 `context(Logger) fun Transaction.commitWithLog()` 같은 자리 — 에서, receiver의 *해소 우선순위* 규칙이 처음 보는 사람에게는 한 번에 잡히지 않았다. 이 우선순위가 implicit해질수록 *컴파일러가 무엇을 골랐는지*를 사용자가 추측해야 한다. KEEP-367은 이 자리에서 *이름을 강제*하는 결정이 결국 더 단단하다고 결론을 내린다.

JetBrains 공식 블로그의 한 줄을 그대로 옮겨 두자.

> *"Migration is **strongly recommended**, as we plan to remove context receivers around the 2.3 release."*

*권고*라는 표현을 썼지만, 실질은 시한부 통보에 가깝다. context receivers 위에 쌓아 둔 코드는 가만히 두면 2.3에서 *컴파일이 멈춘다*. 묘비명이 새겨진다. 그래서 우리는 묘비명 앞에 서서, *후속 받침대*가 어떻게 생겼는지부터 차분히 살펴봐야 한다.

## context parameters의 동기 — 잃은 것을 어떻게 보상받는가

KEEP-367의 첫 페이지를 펼치면, context parameters가 풀고자 한 세 문제가 그대로 적혀 있다 — *scope pollution, callable reference 모호성, IDE 추적성*. 결정의 결을 짧게 따라가 보자.

첫째 결정은 *이름을 강제*하자는 것이다. context receivers가 implicit이었다면, context parameters는 *반드시* 이름을 받는다. `context(users: UserService)`처럼 적고, 본문에서는 `users.log(...)`로 부른다. 함수 시그니처만 봐도 *어느 자리에 무엇이 들어와 무엇으로 불릴지*가 한눈에 보인다. JetBrains 블로그는 이 결정을 이렇게 표현했다 — *"The latter [context parameters] **require a name**. Introducing this name also requires prefixing any calls."*

이름을 강제하면 호출 사이트가 *명시적*이 된다. 위 `handleSignup`을 다시 적으면 이렇다.

```kotlin
// 2.2 context parameters
context(logger: Logger, tx: Transaction, users: UserService)
fun handleSignup(email: String) {
    logger.info("새 가입 시도: $email")
    val id = users.createUser(email)
    logger.log("DB에 user $id 생성")
    tx.commit()
}
```

본문이 *말이 더 많아졌다*. 동시에, *어디에서 온 누구의 메서드인지*가 한 줄마다 명확해졌다. scope pollution이 일어날 자리가 사실상 사라졌다. 자동완성 목록이 세 통을 한꺼번에 들이붓지 않는다. 코드를 처음 읽는 사람도, 이 함수 한 덩어리만 보고 *세 받침대가 각각 무엇을 책임지는지*를 즉시 가늠한다.

둘째, callable reference의 모호성이 사라진다. context parameter는 *이름이 있는 파라미터*에 가깝게 다뤄지므로, `::handleSignup`의 시그니처가 컴파일러 입장에서 *명확*해진다. 라이브러리 작성자는 이 시그니처를 그대로 문서에 적을 수 있다. 사용자도 *우리가 이 함수를 callable로 넘길 때 무엇이 따라오는지*를 한 줄로 본다.

셋째, IDE 추적성. *이름이 있는 receiver*는 그 자체로 IDE가 따라가기 좋은 모양이다. Go to declaration이 헷갈릴 자리가 줄어들고, *우리가 쓰던 그 클래스*로 곧장 점프한다. K2/FIR 위에서 implicit receiver를 떠받치던 부담도 함께 가벼워진다.

물론 *얻은 것이 있으면 잃은 것도 있다*. 함수 본문이 길어진다는 점이다. `info("bar")` 한 줄이 `logger.info("bar")`로 늘어나고, 줄바꿈을 따라 점이 한 번 더 찍힌다. 본문 한 화면 안에서 *같은 logger*가 다섯 번 호출된다면, 다섯 번 모두 `logger.` 접두어를 끌고 다닌다. 좀 *번거롭다*. arrow-kt의 `Raise<E>.()` 위에서 `raise(MyError)` 한 단어로 끝나던 결제 도메인 코드를 떠올려 보면, 같은 일을 `raise.raise(MyError)`로 적게 되는 셈이다 (이름을 `raise`로 골랐을 때). 도메인 DSL의 *자연스러운 문장 같은 호출*이 한 단어 두꺼워진다. 이 감각, 진짜다.

이 거래가 정말 그만한 가치가 있었을까? KEEP의 답은 *yes*에 가깝다. 받침대가 서너 개 쌓일 때의 scope pollution 비용이, 한 단어 짧게 쓰고 싶다는 욕망보다 무겁다는 판단이다. 한국 커뮤니티의 후기 톤도 비슷하다 — *처음에는 어색하지만, 큰 코드베이스에서는 명시적인 쪽이 마음이 편하다*. 결론에 도달하기까지 한 번쯤 *아쉬워하고 시작*하는 사람이 많지만, 두세 PR을 옮기고 나면 그 후회가 자연스럽게 옅어진다. 한 가지 흥미로운 관찰이 있다 — 마이그레이션 후 한 사이클이 지난 시점에 *이전 코드를 되돌아보면*, 우리가 implicit receiver의 우아함이라고 부르던 것이 실은 *호출 사이트의 모호함*이었다는 사실이 새삼 보인다. PR 리뷰에서 *"여기 info는 어디서 온 거지?"*를 한 번도 묻지 않게 된다는 사실 하나만으로도 거래가 반쯤 성공한 셈이다.

여기서 한 가지를 분명히 하고 가자. *이름이 길어서 우아함이 깨진다*는 감각은 진짜다. 우리가 그 감각을 진짜로 받아들여야, 라이브러리 작성자가 *어디까지 dual API를 유지할지*, 사용자 코드가 *어디서부터 단순 파라미터로 강등할지*를 차분히 결정할 수 있다. *그렇다면 우리는 어떻게 가야 할까?* 우아함을 잃은 자리에는 *명시성*이라는 다른 결의 우아함이 들어왔다고 받아들이는 편이 마음 편하다. 그리고 *진짜로 우아함이 필요했던 자리*에는 — 짧은 도메인 DSL이거나, 한 함수 한 줄짜리 호출이거나 — context parameter를 쓰지 않고 단순 파라미터나 extension으로 풀어 내는 길도 함께 열려 있다. 이 길은 잠시 뒤 마이그레이션 절에서 (c)·(d)로 다시 만난다.

## 잠시 — 한국 개발자들의 마이그레이션 풍경

본격 문법으로 들어가기 전에, 한국 개발자들의 후기 톤을 짧게 짚어 두자. velog와 한국어 블로그에 올라온 *2.0.20 → 2.2 마이그레이션* 후기들을 한 자리에 모아 두면 풍경이 어렴풋이 잡힌다. 첫 반응은 거의 한결같다 — *"드디어 손을 대 보았다"*, *"미루고 미루다 결국 부딪쳤다"*. arrow-kt나 사내 도메인 DSL에 context receivers를 적극 끌어들였던 팀일수록, 마이그레이션의 *체감 무게*가 무겁다. 한 후기는 이렇게 적는다 — *"PR 한 번에 함수 시그니처 80개가 한꺼번에 바뀐다. 리뷰가 의미를 잃는다."*

이 톤이 우리에게 던지는 신호가 있다. 한꺼번에 옮기는 *큰 PR*은 답이 아니라는 점이다. 모듈 단위로, 도메인 단위로, 호출 체인 단위로 PR을 쪼개야 한다. 처음 한두 PR은 인스펙션의 1:1 변환을 그대로 받아 두고, 익숙해진 다음에야 (c)·(d)로의 강등 결정을 내리는 편이 *마음이 편하다*. 첫 PR부터 결정 부하를 다 짊어지면, 본문 호출이 어색한 자리를 *못 알아보고 그대로 머지*하게 된다. 끔찍한 일이다.

또 다른 후기 한 줄을 옮겨 두자 — *"이름을 'logger'로 통일하니, 처음에는 길어 보이던 본문이 *읽히기 시작*했다."* 이름을 강제한 결정이 가져온 *읽힘의 회복*이라는 효용을 한국 개발자들도 한 사이클 안에 체감하는 모습이 보인다. 우리도 이 효용을 한 PR 안에서 받아 들이게 될 것이다.

## 문법 — `context(name: Type)`의 자리들

KEEP-367이 정한 문법은 단출하다. 함수, 프로퍼티 게터, 람다 자리에 `context(name: Type)`를 붙인다. 빈 자리를 받고 싶으면 이름을 `_`로 둔다. 호출은 *type matching*으로 디스패치된다.

가장 흔한 모양부터 보자.

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
```

함수에도 붙고, *프로퍼티 게터*에도 붙는다. context parameter를 가진 프로퍼티는 backing field를 가질 수 없다는 한 가지 제약이 있는데, 이건 잠시 뒤에 다시 짚는다.

본문에서 *그 받침대를 굳이 직접 쓰지는 않을 때*도 있다. 다른 함수가 같은 받침대를 요구해서 *그저 통과시키기만 하면 되는* 경우다. 그럴 때는 이름을 `_`로 둔다.

```kotlin
context(_: UserService)
fun logWelcome() {
    outputMessage("Welcome!")  // _로 받았어도 in-scope이니 호출 가능
}
```

`_`는 *이 함수는 UserService를 in-scope으로 받지만, 본문에서 직접 부를 일이 없다*는 약속을 시그니처에 박아 둔 것이다. 흔히 컨트롤러나 어댑터처럼 *받아서 흘려 보내는* 함수에서 자주 등장한다. 이름을 강제한 결정의 *날카로움을 살짝 무디게* 해 주는 안전판이라고 봐도 좋다.

호출 측은 type matching이 처리한다. 동일 타입의 후보가 둘 이상이면 컴파일러가 *ambiguity*를 보고하므로, 그 자리에서 `context(serviceA) { ... }` 블록으로 명시한다. 이 블록 문법은 *지정 receiver 블록*과 결이 같다. 한 함수 안에서 잠시 다른 받침대를 끼워 넣고 싶을 때 쓴다.

```kotlin
context(primary: UserService, secondary: UserService)
fun reconcile() {
    // 직접 부르려면 이름으로 — primary.findUserById(1)
    // outputMessage("...")는 ambiguity. 블록으로 명시한다.
    context(primary) { outputMessage("primary로 수행") }
    context(secondary) { outputMessage("secondary로 수행") }
}
```

람다 자리에도 context parameter를 둘 수 있다. 함수형 타입의 *receiver 자리*가 아니라, 람다 *시그니처* 위에 `context(...)`를 얹는 모양이다.

```kotlin
fun <T> withTransaction(block: context(Transaction) () -> T): T = ...

// 호출
withTransaction { /* 안쪽에서 Transaction이 in-scope */ }
```

이 패턴은 *사용자가 람다를 받침대 위에 짧게 써 내려가게 해 주는* 자리에서 자주 등장한다. arrow-kt의 `either { ... }`나 `effect { ... }` 같은 도메인 DSL이 정확히 이 모양으로 옮겨 간다.

여기서 한 가지를 짚어 두자. 1.x의 `context(Receiver)`(이름 없음) 시절 코드와 2.2의 `context(name: Receiver)` 시절 코드를 *시각적으로 비교*하면 차이가 한 줄로 정리된다.

```kotlin
// 1.x — implicit, scope pollution 위험
context(Logger)
fun foo() = info("bar")

// 2.2 — explicit, prefix 강제
context(logger: Logger)
fun foo() = logger.info("bar")
```

같은 일을 하는 같은 함수다. 다만 2.2 버전은 *이름이 시그니처에 박혀 있고, 호출이 점을 한 번 더 찍는다*. 이 두 줄이 7장 전체에서 가장 많이 펼쳐져야 할 *비교 한 페이지*다. 이 비교를 마음에 두고, 이제 *우리가 쥔 코드를 어떻게 옮길지*로 들어가 보자.

## 1.x → 2.2 마이그레이션 — 네 가지 길

context receivers가 박힌 함수 한 토막을 우리는 정확히 네 가지 길로 옮길 수 있다. *각 길은 함수의 의도와 호출 사이트의 모양에 따라 우열이 다르다.* 한 함수에 한 길만 정답이 아니다. 한 모듈을 옮길 때, 우리는 네 길을 *섞어* 쓰게 된다. 같은 시그니처를 네 번 변형해 본다.

원본 함수 한 줄.

```kotlin
// 출발점 — 1.x context receivers
context(Logger)
fun foo() = info("bar")
```

### 길 (a) — IntelliJ 인스펙션에 일임

가장 손이 적게 드는 길이다. IntelliJ IDEA 2025.1 이후의 *"Migrate from context receivers to context parameters"* 인스펙션을 모듈 단위로 적용하면, 함수 시그니처와 본문 호출이 *기계적으로* 옮겨진다.

```kotlin
// 인스펙션 결과 — 흔한 패턴
context(logger: Logger)
fun foo() = logger.info("bar")
```

이름은 인스펙션이 *타입에서 유추한 변수명*을 채워 준다. `Logger`라면 `logger`, `Transaction`이라면 `transaction`, `UserService`라면 `userService` 같은 식이다. 이름이 마음에 들지 않으면 PR 단계에서 일괄 rename으로 다듬는다. 프로젝트 전체를 한 번에 옮길 때 *first pass*로 거의 무조건 권장하는 길이다. 인스펙션을 돌리기 전에 한 가지를 권하고 싶다 — 모듈을 git 커밋 단위로 쪼개 두고, 인스펙션 결과를 *모듈마다 별개 커밋*으로 떨어뜨리자. 한 PR에 50개 함수가 한꺼번에 옮겨지면 리뷰가 사실상 불가능해진다. *받침대가 비슷한 함수끼리 묶어* 작은 PR로 끊어 가는 편이 낫다.

다만 인스펙션이 못 잡는 자리가 있다. 예를 들어 *receiver가 nullable이거나, 같은 타입이 두 번 등장하거나, 람다 안에서 implicit receiver를 받던 자리*는 손으로 마무리해야 한다. 인스펙션 결과를 일단 받아 두고, 컴파일러가 빨간 줄을 그어 주는 자리만 따로 걸러 보면 된다. 우리 경험 한 줄을 적어 두자 — 인스펙션이 옮겨 놓은 자리의 80%는 그대로 두고, 나머지 20%에서 단순 파라미터·extension·새 wrapper 함수 가운데 하나를 골라 다시 적게 된다. 이 20%가 7장의 진짜 노동이다.

### 길 (b) — `context(name: Receiver)`로 직접 옮기기

인스펙션을 못 쓰거나(예: 매크로/코드 생성 단계), 인스펙션이 만든 이름이 도메인에 어울리지 않을 때 직접 옮긴다. 결국 같은 모양이 나오지만, *이름을 우리가 고르는 자리*가 다르다.

```kotlin
context(log: Logger)         // 사내 컨벤션이 'log'를 선호한다면
fun foo() = log.info("bar")
```

이 길은 *라이브러리 공개 API*를 옮길 때 특히 신중해진다. 인스펙션이 골라 준 이름은 사용자에게도 노출되는 *공식 시그니처*가 된다. 프로젝트 코딩 컨벤션이 `logger`와 `log` 중 어느 쪽을 쓰는지를 한 번 정리하고 시작하자. 한 라이브러리 안에서 함수마다 이름이 들쭉날쭉하면, 다음 사람이 *저 자리에는 무엇을 넘겨야 하지?*를 다시 묻게 된다. 끔찍한 일이다.

### 길 (c) — 단순 파라미터로 강등

context의 *implicit성*이 그렇게까지 매력적이지 않은 함수라면, 그냥 일반 파라미터로 내리는 편이 낫다.

```kotlin
fun foo(logger: Logger) = logger.info("bar")
```

호출 사이트가 `foo(logger)` 한 번 적는 비용을 *충분히 감당할 수 있는* 자리라면 이 길이 가장 깔끔하다. 함수가 *대부분 단발 호출*이고, 호출자도 그 자리에서 logger를 *어쨌거나 직접 들고 있는* 경우다. context의 진짜 가치는 *받침대를 한 번 깔아 두고 그 위에서 여러 함수를 부른다*는 데 있다. 그 패턴이 아니라면, context를 굳이 쓰지 않는 편이 *코드 한 줄을 줄여* 준다. context를 *없는 편이 나은 자리*에 두는 일이야말로, KEEP-367이 *명시성*을 강조한 이유에 가장 잘 부합한다.

### (c)에 잠깐 더 — 강등이 *기본 옵션*이라는 시각

한 가지를 좀 더 강조해 두자. context parameters 도입 직후의 한국·해외 후기들이 공통적으로 짚는 한 가지가 있다 — *생각보다 (c) 단순 파라미터로의 강등이 자주 답이다*. 1.x 시절에 우리가 *우아함*에 끌려 context receiver를 단 자리 중 상당수가, 사실 *함수 호출 한 번만 깔끔해지면 되는* 자리였다는 이야기다. 받침대를 한 번 깔아 두고 *그 위에서 여러 함수를 부른다*는 패턴이 진짜로 작동하는 자리는 의외로 좁다. 받침대 한 번에 함수 한 번 호출이라면, context의 *implicit*은 비용 대비 효용이 맞지 않는다.

그래서 마이그레이션의 첫 결정을 *(c)부터* 검토하는 편이 권장될 만하다. *이 함수가 정말 받침대를 필요로 하는가*를 한 번 묻고, 답이 *아니오*에 가까우면 (c)로 강등한다. (a)·(b)는 답이 *예*에 가까울 때만 선택한다. 이 순서를 뒤집으면 *모든 함수에 명시적 이름이 박힌 시그니처*가 모듈을 채우게 되고, 본문이 한 단어씩 길어진 무게가 모듈 전체에 깔린다. *번거롭다*.

### 길 (d) — extension으로 강등

함수가 *Logger의 메서드처럼 동작하길* 원했던 자리라면, 사실 우리가 처음부터 원했던 건 extension function이었을 가능성이 높다.

```kotlin
fun Logger.foo() = info("bar")
```

호출 사이트가 `logger.foo()`로 모이는 그림이라면, extension이 가장 자연스럽다. 1.x 시절에 context receivers를 쓰던 자리 중 *상당수*가 사실은 extension으로도 충분했다. 우리가 *받침대*를 너무 사랑한 나머지, extension으로 끝낼 일을 굳이 context로 두른 경우가 적지 않다. 이 김에 한 번 정리해 두자. extension으로 강등할 수 있다면 강등하는 편이 *받침대 비용을 0으로* 만든다.

다만 *둘 이상의 receiver*를 한꺼번에 요구하던 함수는 extension으로 옮기기 어렵다. extension은 *receiver 한 개*만 받으니, 나머지는 context parameter로 남겨야 한다.

```kotlin
context(tx: Transaction)
fun Logger.bar() {
    info("foo")
    tx.commit()
}
```

extension과 context parameter가 *한 시그니처에 공존*하는 패턴이다. 이렇게 두면 함수 본문에서 `info("...")`는 extension receiver의 implicit 호출이 되고, `tx.commit()`은 context parameter의 명시적 호출이 된다. 둘의 결을 *시각적으로 분리*한 셈이다. 1.x context receivers가 두 받침대를 *한 통에* 부어버리던 모습과 비교하면 결이 한참 깔끔하다.

### 한 페이지 비교 — 같은 함수, 네 가지 변형

이제 같은 함수 한 토막을 네 길로 동시에 펼쳐 두자. 이 한 페이지를 머리에 박아 두면, 한 모듈을 옮길 때 *어느 함수에 어느 길을 쓸지*가 거의 자동으로 떠오른다.

```kotlin
// 출발점
context(Logger)
fun foo() = info("bar")

// (a) IntelliJ 인스펙션 — 이름 자동 부여
context(logger: Logger)
fun foo() = logger.info("bar")

// (b) 직접 부여 — 컨벤션에 맞춘 이름
context(log: Logger)
fun foo() = log.info("bar")

// (c) 단순 파라미터로 강등 — context의 implicit이 굳이 필요 없을 때
fun foo(logger: Logger) = logger.info("bar")

// (d) extension으로 강등 — Logger의 메서드처럼 호출되길 원했을 때
fun Logger.foo() = info("bar")
```

이 네 변형 사이에서 결정을 내리는 *간단한 휴리스틱*은 이렇다. 한 함수가 *세 줄짜리 단발 호출*이고 호출 사이트가 *Logger를 어차피 쥐고 있다면* (c). 호출 사이트가 *`logger.foo()` 모양으로 모인다면* (d). 받침대를 *한 번 깔고 여러 함수를 부른다면* (a) 또는 (b). 인스펙션이 골라 준 이름이 마음에 든다면 (a), 도메인 컨벤션을 따르고 싶으면 (b). 이 한 줄만 머리에 두고 모듈을 한 바퀴 돌면, 마이그레이션의 절반은 끝난다.

조금 더 길게 적자면, 결정의 자리는 *함수의 호출 빈도*와 *받침대의 재사용 폭*이라는 두 축으로 갈라진다. 한 함수가 모듈 안에서 *20번 호출*되는데 그때마다 호출자가 같은 Logger를 쥐고 있다면, (c) 단순 파라미터로 강등하는 순간 호출 사이트 20곳이 모두 한 단어 길어진다. 이 경우는 (a)·(b)가 낫다. 반대로 한 함수가 *세 곳에서만* 호출되고 그 세 곳이 모두 같은 함수 본문 안이라면, (c)로 강등해도 호출 사이트의 비용은 한 화면 안에서 끝난다. 받침대의 재사용 폭이 좁다면 굳이 context의 *implicit*을 끌어올 이유가 없는 셈이다. 실제로 모듈 한 바퀴를 돌아 보면, 1.x 시절에 context receiver를 단 함수 중 *절반 이상*이 (c)나 (d)로 강등 가능한 자리였다는 인상이 든다. 이 김에 한 번 정리해 두는 편이 낫다.

도메인별 권장 동선을 짧게 적어 두자. *로깅·메트릭 같은 횡단 관심사*는 (a)·(b)가 자연스럽다. 한 도메인 함수 본문에서 같은 Logger가 여러 번 호출되니, 받침대를 한 번 깔아 두는 가치가 있다. *트랜잭션·세션 같은 라이프사이클 컨텍스트*는 (b)가 안정적이다. 이름을 도메인 용어로 골라 두면(`tx`, `session`) 시그니처가 사용자 코드에서 일종의 문서가 된다. *짧은 검증·계산 함수*는 (c)가 깔끔하다. *receiver의 메서드처럼 호출되길 원했던 자리*는 (d)다. 이 네 분류 위에서 모듈을 다시 한 바퀴 보면, 어느 자리에 어느 길이 어울리는지 자연스럽게 떠오른다.

마지막으로 한 가지 주의를 더 박아 두자. 같은 함수에 *두 길을 동시에 적용*하지 말자. 예컨대 (a)로 옮긴 함수의 시그니처를 PR 후반부에 (c)로 다시 강등하면, 호출 사이트가 *두 번* 바뀐다. 리뷰가 *난감해*진다. 한 함수에 한 길을 정하고, 같은 PR 안에서는 그 결정을 흔들지 않는 편이 바람직하다. 결정을 흔들고 싶다면 별도 PR로 분리하자.

### 한 도메인 함수의 마이그레이션을 따라가 보자

한 도메인 함수가 네 길로 갈라지는 모습을 직접 따라가 보자. 결제 도메인의 가상 함수 하나를 잡아 본다.

```kotlin
// 1.x — Logger와 Transaction을 둘 다 받침대로 깔았다
context(Logger, Transaction)
fun chargePayment(orderId: Long, amount: Long) {
    info("결제 시작 order=$orderId")
    val charged = doCharge(orderId, amount)
    info("결제 완료 charge=$charged")
    commit()
}
```

이 함수를 옮기는 길은 케이스에 따라 다르다.

```kotlin
// 옵션 A — (a)/(b)로 그대로 옮긴다. 받침대 둘 다 본문에서 여러 번 쓰인다.
context(log: Logger, tx: Transaction)
fun chargePayment(orderId: Long, amount: Long) {
    log.info("결제 시작 order=$orderId")
    val charged = doCharge(orderId, amount)
    log.info("결제 완료 charge=$charged")
    tx.commit()
}

// 옵션 B — Logger만 (c)로 강등, Transaction은 receiver로 살린다.
context(tx: Transaction)
fun chargePayment(log: Logger, orderId: Long, amount: Long) {
    log.info("결제 시작 order=$orderId")
    val charged = doCharge(orderId, amount)
    log.info("결제 완료 charge=$charged")
    tx.commit()
}

// 옵션 C — 둘 다 (c)로 강등. 호출 사이트가 어쨌거나 둘 다 쥐고 있다면 가장 깔끔.
fun chargePayment(log: Logger, tx: Transaction, orderId: Long, amount: Long) {
    log.info("결제 시작 order=$orderId")
    val charged = doCharge(orderId, amount)
    log.info("결제 완료 charge=$charged")
    tx.commit()
}
```

세 옵션 사이에서 무엇이 정답인지는 *호출 사이트의 모양*에 달렸다. 호출자가 같은 도메인 서비스 안에서 같은 Logger·Transaction을 쥐고 *연속해서 여러 결제 함수를 호출*한다면 옵션 A가 자연스럽다. 호출자가 *Transaction을 받침대로 쥔 채 Logger는 그때그때 가져온다*면 옵션 B다. 호출자가 *둘 다 즉석에서 만들어 넘긴다*면 옵션 C다. 한 함수 한 결정이라기보다, *호출 체인 한 묶음 한 결정*이라는 시각이 자연스럽다. 이 시각으로 모듈을 한 바퀴 돌면, 같은 도메인 안에서 *받침대 모양이 통일*되어 간다. 모양이 통일되면 다음 사람의 코드 리뷰가 한결 가벼워진다.

## 현 시점의 한계 — 2.2의 받침대는 아직 못 닿는 자리

context parameters가 첫걸음이라는 표현을 7장 제목에 박아 둔 데에는 이유가 있다. 2.2.0 시점의 context parameters는 *모든 자리에 닿지 못한다*. KEEP-367과 What's new 2.2 페이지가 직접 적어 둔 한계가 넷 있다.

첫째, *클래스 자체에는 context parameter를 못 단다*. 함수와 프로퍼티에만 붙는다. 1.x 시절에 *클래스에 context receiver를 단 패턴*을 갖고 있었다면, 그 자리는 일단 *멤버 함수마다 context parameter를 따로 다는* 모양으로 풀어야 한다. 살짝 *번거롭다*. 클래스 차원의 받침대는 KEEP의 *후속 단계*에서 다시 다뤄질 예정이다.

둘째, *생성자에도 못 단다*. 생성자가 받침대를 요구하던 패턴은 *factory 함수*에 context parameter를 다는 식으로 우회한다.

```kotlin
context(logger: Logger)
fun userService(repo: UserRepo): UserService =
    UserServiceImpl(repo, logger)
```

생성자 호출 한 번을 함수 호출 한 번으로 옮긴 셈이다. 한 줄 더 길어졌다. 어쩔 수 없다.

셋째, *callable reference가 2.2에서는 미지원*이다. `::foo` 형태로 context parameter를 가진 함수를 넘기지 못한다. JetBrains 블로그에 따르면 이 자리는 *2.3에서 도입* 예정이다. 라이브러리에서 *함수 참조를 표면 API로 노출*하던 자리는 2.2 시점에는 일반 함수 호출 wrapper로 우회해야 한다.

```kotlin
// 2.2에서는 이렇게 못 한다
val ref: KFunction1<String, Unit> = ::handleSignup

// wrapper로 우회
val ref: (String) -> Unit = { email -> handleSignup(email) }
```

이 자리는 *2.3 출시 시점에 자연스럽게 풀린다*. 우리가 지금 wrapper를 둘 자리는 그때 한 번 더 정리하면 된다.

넷째, *backing field/initializer/delegation을 가진 프로퍼티에는 context parameter를 동시에 둘 수 없다*. 게터만 있는 프로퍼티에는 붙지만, `var x = computeFromContext()` 같은 자리에는 못 붙는다는 이야기다. 그 자리는 함수 호출로 풀거나, lazy delegation으로 우회한다.

```kotlin
// 2.2에서는 못 한다
context(repo: UserRepo)
val current: User = repo.fetchCurrent()   // initializer 자리에 context 동시 사용 불가

// 함수로 우회
context(repo: UserRepo)
fun current(): User = repo.fetchCurrent()

// 또는 lazy로 우회 (호출 시점이 있는 경우)
context(repo: UserRepo)
val current: User
    get() = repo.fetchCurrent()
```

이 네 한계를 한 줄로 정리하면 이렇다 — *2.2 context parameters는 함수와 게터에만 닿는 첫걸음*이다. 그래서 1.x context receivers의 *모든* 패턴이 즉시 옮겨지지는 않는다. 못 옮기는 자리는 단순 파라미터·factory 함수·wrapper로 우회한 뒤, 2.3에서 callable reference가 풀리고 그 다음 사이클에서 클래스/생성자가 풀릴 때마다 *조금씩 이름표를 바꿔 다는* 길이 현실적이다.

여기서 한 가지를 권하고 싶다. 한계에 부딪힌 자리를 만나면 *주석 한 줄*을 박아 두자. 예컨대 `// TODO(kotlin-2.3): callable reference 도입 후 wrapper 제거` 같은 식이다. 이 한 줄이 다음 minor 업그레이드 시점에 우리를 다시 그 자리로 데려다 준다. 마이그레이션 한 번으로 영원히 끝나는 일이 아니라, *한 사이클 뒤에 한 번 더 다듬는다*는 사실을 받아들여 두는 편이 마음 편하다. 빨간 줄이 사라진 그 시점에 *주석 한 줄을 미리 깔아 두는* 작업이, 다음 단계의 우리에게 보내는 가장 정직한 편지다.

## bridge functions와 dual API — arrow-kt의 마음을 읽어 보자

라이브러리 작성자라면 한 가지를 더 고민해야 한다. *우리 라이브러리 사용자 중 절반은 1.x context receivers 코드를 갖고 있고, 절반은 2.2 context parameters로 옮긴 뒤다*. 한 사이클 동안은 *둘 다*를 지원해야 한다. 라이브러리가 한 메이저 업그레이드 시점에 사용자 코드를 *통째로* 깨뜨리면, 사용자는 그 라이브러리를 *건너뛰는* 결정을 한다. 그렇다고 옛 시그니처를 *영원히* 유지하면 라이브러리 안쪽이 두 갈래로 갈라져 있는 시기가 길어진다. 이 사이의 패턴이 *bridge functions*다.

arrow-kt 같은 receiver-heavy 라이브러리를 한 번 떠올려 보자. `Raise<E>.()`로 함수 본문 안에서 `raise(MyError)`를 부르는 그 패턴, 라이브러리의 가장 큰 매력 중 하나였다. 2.0.20에서 deprecation이 시작된 뒤 arrow-kt는 *이중 API* 모양을 한 사이클 동안 유지했다. 옛 시그니처와 새 시그니처가 *한 라이브러리 안에 함께 살아 있는* 시기가 만들어진 것이다.

대략적인 모양은 이렇다.

```kotlin
// 옛 시그니처 — 1.x 사용자를 위해 한 사이클 더 살려 둔다
@Deprecated(
    "Use the context-parameter version. context receivers will be removed in Kotlin 2.3.",
    ReplaceWith("either { block(this) }")
)
context(Raise<E>)
fun <E, A> oldEither(block: () -> A): Either<E, A> = ...

// 새 시그니처 — 2.2 context parameters
fun <E, A> either(block: context(Raise<E>) () -> A): Either<E, A> = ...
```

두 함수가 *같은 일*을 한다. 옛 시그니처에 `@Deprecated`가 붙어 있고, `ReplaceWith`로 *새 호출 모양*을 IDE가 자동으로 제안한다. 사용자 입장에서는 라이브러리 버전을 올린 직후에는 *옛 코드가 노란 줄*이 되고, IDE 인스펙션 한 번으로 새 시그니처로 옮겨 간다. 이중 API 기간은 *옛 사용자를 깨뜨리지 않으면서 새 받침대로 안내하는* 다리 역할을 한다.

라이브러리 작성자가 신경 쓸 결정은 셋이다.

먼저, *어느 시점부터 dual API를 시작할지*. 너무 일찍 시작하면 라이브러리 사용자 중 1.x context receivers 의존자가 많지 않은 시기에 *번거롭게* 두 API를 보여 주는 셈이 된다. 늦게 시작하면 사용자 코드에 deprecation 노란 줄이 쌓이는 동안 *우리는 가만히* 있는 셈이 된다. JetBrains의 시간표를 따르면, 2.0.20에 deprecation이 시작된 시점부터 dual API를 제공하는 편이 자연스럽다.

다음, *어느 시점에 옛 API를 정리할지*. 너무 빨리 정리하면 사용자가 *우리 라이브러리 메이저 업그레이드* 한 번에 코드 전체를 옮겨야 한다. 너무 늦게 정리하면 deprecation 코드가 *수년간 라이브러리 안에 남아* 있다.

세 번째, *완전 제거 시점*. 이 시점은 보통 *Kotlin이 옛 문법을 완전히 제거하는 시점*에 맞춘다. context receivers의 경우 2.3이 그 자리다. 우리가 이 시점을 라이브러리 자체의 메이저 버전 업과 맞춰 두면, 사용자 입장에서 *한 번의 마이그레이션*으로 끝난다.

휴리스틱 한 줄로 정리하면 이렇다 — *dual API는 한 메이저 사이클(약 1년) 정도 유지하고, 다음 minor에서 정리한다*. semver상의 메이저 갱신과 Kotlin의 메이저 사이클(2.x → 2.(x+1)), 우리 라이브러리의 의존자 수 — 이 셋을 함께 보고 시점을 정하면 흔들리지 않는다. 의존자가 많은 라이브러리(arrow-kt, Ktor 등)는 *한 사이클 더* 보수적으로 유지하는 편이 안전하고, 의존자가 적은 사내 공용 라이브러리는 *한 사이클 짧게* 가도 큰 부담이 없다. 단계별 시점 결정은 9장 9.3절에서 다시 짚는다.

dual API 기간을 *어떻게 신호*하느냐도 중요한 결정이다. 사용자 입장에서 가장 친절한 신호는 두 가지다. 첫째, `@Deprecated`의 `ReplaceWith`를 *정확히* 채워 두자. IDE의 *"Replace with"* 한 번 클릭으로 마이그레이션이 끝나는 자리에서, 사용자는 그 라이브러리에 *고마움*을 느낀다. 둘째, `DeprecationLevel`을 단계적으로 올려 가자. 처음에는 `WARNING`으로 시작해 한 사이클 뒤에 `ERROR`로, 다시 한 사이클 뒤에 코드 자체를 제거한다. 이 *2단 점진*이 사용자에게 *예측 가능한 마이그레이션 시간표*를 약속하는 셈이다.

```kotlin
// 사이클 1 — WARNING
@Deprecated("Use context-parameter version. See migration guide.",
    ReplaceWith("either { block(this) }"),
    level = DeprecationLevel.WARNING)
context(Raise<E>)
fun <E, A> oldEither(block: () -> A): Either<E, A> = ...

// 사이클 2 — ERROR
@Deprecated("...", ReplaceWith("either { block(this) }"),
    level = DeprecationLevel.ERROR)
context(Raise<E>)
fun <E, A> oldEither(block: () -> A): Either<E, A> = ...

// 사이클 3 — 제거
// (코드 자체가 사라진다)
```

라이브러리 사용자 입장이라면 *옛 사용자*를 신경 쓸 일은 없다. 다만 한 가지를 권하고 싶다 — IntelliJ 인스펙션의 *"Migrate from context receivers to context parameters"*를 한 번 돌리고, 그 결과를 그대로 받아들이지 말고 *길 (a)·(b)·(c)·(d)*의 결정을 함수마다 한 번 더 내리자. 인스펙션은 *기계적*인 1:1 변환을 해 주지만, 사람의 손은 *그 함수에 진짜 어울리는 길*을 고른다. 이 작은 차이가 마이그레이션 PR을 *기계 번역*과 *진짜 정리* 사이에서 갈라 놓는다.

여기서 한 가지를 더 짚어 두자. dual API 기간 동안 *우리 코드 안*에서도 두 받침대가 공존한다. 같은 모듈 안에서 한 함수는 1.x context receivers 위에 있고, 다른 함수는 2.2 context parameters로 옮겨 간 모양이다. 이 공존 자체는 자연스럽다. 다만 한 함수의 시그니처가 다른 함수를 *호출*할 때 결이 어긋나는 자리가 생긴다 — 옛 함수는 implicit receiver로 받고, 새 함수는 명시적 파라미터로 받는다. 이 자리를 그대로 두면 호출 사이트가 *두 모양으로 갈라져* 있게 된다. 우리 권고는 단순하다 — 한 *호출 체인*은 한 사이클 안에 통째로 옮기자. *호출자가 옮긴 함수에 닿으려면 그 위 호출자도 함께 옮긴다*는 원칙을 PR 단위로 지키면, 모듈 안의 받침대 모양이 *조각조각 흩어지지* 않는다.

## 마무리 — 비용을 치른 직후, 다음 페이지로

여기까지 한 번 호흡을 가다듬자. 7장은 코드 한 줄을 옮기는 이야기였지만, 그 한 줄에 *디자인 결정 한 묶음*이 같이 따라왔다. 받침대를 어떻게 깔지, 이름을 강제할지 말지, 옛 사용자를 한 사이클 더 챙길지, 라이브러리 안쪽의 두 받침대 공존을 어떻게 정리할지 — 이 결정들이 한 PR 안에 같이 담긴다. 한 번에 다 결정하지 말고, *한 모듈*에서 한 번씩 시도해 본 다음에야 큰 모듈로 넓혀 가는 편이 *마음이 편하다*.

7장은 비용이 가장 무겁게 청구되는 장이었다. 5장에서 build.gradle의 의존성이 한 줄씩 사라질 때의 *공짜 풍요*나, 4장의 세 카드 같은 *공짜 우아함*과 결이 다르다. 시그니처가 바뀌고, 본문 호출이 다시 쓰이고, 라이브러리 작성자라면 dual API 기간을 결정해야 했다. 받침대 위에서 점 없이 걷던 시절의 *우아함을 잃은 자리*에, *명시성*이라는 다른 결의 우아함이 들어왔다고 받아들이자.

한 가지 시각을 더 남겨 두고 싶다. 7장은 *받침대 한 번을 잃고 다른 받침대로 옮겨 타는* 이야기처럼 보였지만, 한 발짝 떨어져 보면 결이 조금 다르다. 우리는 *받침대 자체를 다시 점검*하는 자리에 와 있다. 1.x 시절에 우리가 context receiver를 단 자리들 가운데 *진짜로 받침대가 필요했던 자리*는 의외로 좁고, 그 외의 자리는 단순 파라미터·extension·factory 함수로 *강등*해 두는 편이 모듈 전체 결을 단단하게 만든다. KEEP-367이 *이름을 강제*한 결정은 사실 우리에게 *이 받침대가 정말 필요한가*를 한 번 더 묻게 만드는 장치이기도 하다.

세 화두에 짧게 답을 적어 두자. 첫째, `-Xcontext-receivers`로 즐겁게 쓰던 코드를 우리는 *implicit*의 우아함과 함께 잃는다. 그 자리에 얻는 것은 *명시성*과 *callable reference·IDE 추적성의 정직함*이다. 둘째, 이름을 강제한 결정은 본문이 한 단어 길어지는 비용을 받아들이고 scope pollution을 끊어 낸다는 거래다. 큰 코드베이스일수록 그 거래는 *옳았다*는 쪽으로 기운다. 셋째, arrow-kt 같은 receiver-heavy 라이브러리는 *dual API*를 한 메이저 사이클 둔 뒤 다음 minor에서 정리하는 흐름이 가장 손이 적게 든다.

기억해 두자. context receivers의 묘비명 앞에서 *아쉬워*하는 건 자연스럽다. 다만 그 묘비명 옆에서 *context parameters의 첫걸음*을 같이 본 다음에야, 우리는 한 모듈을 네 길로 나누어 옮길 결심이 선다. 인스펙션 한 번을 돌리고, 그 결과를 (a)·(b)·(c)·(d)로 다시 한 번 골라 적어 보자. 한 PR로 한 모듈씩 끊어 가면, 빌드 로그의 노란 줄은 한 줄씩 자연스럽게 사라진다.

마이그레이션을 시작하기 전 체크리스트 한 줄을 권하고 싶다. 첫째, 모듈 안의 *context receiver 사용처*를 한 번 세 보자. 검색 한 번이면 된다 — `context\(`로 정규식을 걸어 모듈 안의 등장 횟수를 본다. 50개 미만이면 한 PR로 끝낼 만하고, 200개를 넘기면 도메인별로 PR을 쪼개는 편이 낫다. 둘째, *opt-in 플래그*를 모듈 단위로 좁히자. `-Xcontext-parameters`는 한 모듈 한 곳에서 켜고, 그 모듈을 first PR로 옮긴 뒤 다음 모듈로 옮겨 가자. 한꺼번에 모든 모듈을 켜면 컴파일 에러가 한 번에 쏟아진다. *난감하다*. 셋째, 1.x 잔재인 `-Xcontext-receivers` 플래그가 여전히 켜져 있는 모듈이 있다면, 마이그레이션 후 *그 플래그를 빌드 스크립트에서 지우자*. 노란 줄을 한 줄 지우는 것이 아니라, *플래그 자체*를 지우는 단계까지 가야 7장의 비용 청구서가 완전히 결제된다.

비용을 치른 직후의 시야에서, 다음 페이지로 넘어가자. 8장은 결을 한 번 바꿔, *2.3이 보내 온 미래의 신호*를 짧게 살펴본다. `_city`와 `city: StateFlow` 두 줄로 쓰던 어색한 패턴이 `field = ...` 한 줄로 어떻게 사라지는지, *함수의 반환값을 무시하지 마라*고 컴파일러가 잔소리를 시작한 이유는 무엇인지, 2.3 Experimental 명단 중 어떤 항목이 2.4 Stable로 살아남을지를 가늠해 보는 장이다. 7장의 비용을 한 번 치르고 나면, 8장의 미래는 한결 가볍게 읽힌다. 비싸게 치러야 하는 영역의 *마지막 페이지*를 닫고 넘어가자.

---

**마이그레이션 노트(1줄 액션):** 라이브러리 작성자라면 *dual API*를 한 메이저 사이클(약 1년)만 유지하고 다음 minor에서 정리한다 — semver, Kotlin 메이저 사이클, 의존자 수 셋을 함께 보고 결정하자. 단계별 시점 결정은 9장 9.3절 참조.
