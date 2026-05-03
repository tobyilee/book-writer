# 챕터 3. 변수·타입·함수·모듈 — Java가 알던 모양과 다른 부분

새 언어를 배울 때 흥미로운 단계가 하나 있다. *문법은 비슷한데 의미가 미묘하게 다른 부분*을 발견하는 단계다. 처음에는 *"어, 익숙한 모양이네"* 싶다가도, 며칠 뒤에 *"어, 이건 내가 알던 그 모양이 아니네"*가 된다. 그 미묘한 어긋남을 *모르고 지나치면* 4장의 소유권에서 컴파일러가 화를 낼 때 *왜 화를 내는지* 영문을 모르게 된다.

그래서 이 장에서는 변수, 타입, 함수, 모듈 같은 *기본 도구*를 살펴본다. 다만 단순히 문법을 나열하는 게 아니라, 매 도구마다 *"Java/Kotlin이 이걸 어떻게 표현하지?"*를 옆에 두고 비교한다. 같은 의미인데 표기가 다른 부분, 표기는 비슷한데 의미가 다른 부분, *이 두 카테고리를 분리해서 머리에 박는 게* 이 장의 목표다.

## 불변이 디폴트라는 사실의 무게

변수 선언부터 보자.

```rust
let x = 5;          // 불변
let mut y = 10;     // 가변
y += 1;             // OK
// x += 1;          // 컴파일 에러: cannot assign twice to immutable variable
```

Kotlin을 써본 사람이라면 익숙한 모양이다. `let`이 `val`이고, `let mut`이 `var`다. 그런데 잠시 멈추고 생각해보자. *왜 굳이* 이렇게 디폴트를 불변으로 잡았을까?

답은 *"변경 가능성은 명시적으로 선언할 만큼 무거운 결정"*이라는 철학이다. Java에서 `final` 키워드를 *언제 붙이는가*를 떠올려보자. 변수 한 개에 `final`을 붙이려면 두 자판을 더 쳐야 한다. 그래서 결국 *대부분의 변수가 final 없이 선언*되고, 동시성 코드에서 *어디가 진짜 가변이고 어디가 사실상 불변인지* 코드만 봐서는 알기 어려워진다. 십 년 동안 우리가 Spring 코드 리뷰에서 *"여기 final 좀 붙여주세요"*라고 잔소리해온 풍경의 본질이 그것이다.

Rust는 그 잔소리를 *컴파일러가 대신* 한다. 그것도 *반대 방향으로*. *기본은 불변이고, 가변이 필요할 때 명시*한다. 그 결과 코드를 읽을 때 `mut` 키워드가 보이는 곳이 *진짜 가변인 곳*임을 단번에 안다. 동시성·재할당 사고를 줄이는 가장 단순한 처방이다. *불변 디폴트의 무게*는 처음에는 잘 안 느껴지지만, 두 달쯤 지나면 *"왜 Java는 이걸 디폴트로 안 했지?"*라는 의문이 들기 시작한다.

또 하나 흥미로운 모양이 *shadowing*이다.

```rust
let x = 5;
let x = x + 1;          // 새 변수 x로 다시 선언, 값은 6
let x = x.to_string();  // 또 다시, 이번엔 타입까지 String으로
println!("{x}");        // 출력: "6"
```

같은 이름으로 *새 변수를 다시 선언*해서 이전 변수를 덮는 패턴이다. 가변이 아니다. 매번 *새 불변 변수*가 만들어진다. Java에선 이게 안 된다(블록 안에서는 변수명 충돌). Kotlin에서도 같은 스코프에선 안 된다. Rust는 허용한다. *왜 허용할까?* 같은 의미적 값이 *다른 형태*로 변환될 때(파싱, 역직렬화, 타입 변환) *변수명을 새로 짜내지 않아도 되도록* 풀어줬다. `let raw_input = read_stdin();` → `let parsed: i32 = raw_input.trim().parse()?;` 같은 흐름이 한 변수명으로 자연스럽게 흐른다. 처음엔 살짝 어색하지만 익숙해지면 *맘에 든다*.

## 원시 타입의 지도 — boxing이 사라진 세계

Java에서 `int`와 `Integer`의 구분에 진절머리가 났던 적이 한 번쯤 있을 것이다. `List<int>`는 못 짜고 `List<Integer>`만 짜야 했고, 그 사이의 auto-boxing/unboxing이 *NullPointerException의 새 출처*가 되곤 했다. Rust는 *boxing이 없다*. 모든 원시 타입이 그냥 *값 그대로* 다뤄진다.

기본 원시 타입들의 지도를 한번 그려보자.

| Rust 타입 | 의미 | Java 대응 |
|---|---|---|
| `i8`/`i16`/`i32`/`i64`/`i128` | signed 정수 | `byte`/`short`/`int`/`long`/(없음) |
| `u8`/`u16`/`u32`/`u64`/`u128` | unsigned 정수 | (없음 — Java는 unsigned가 없다) |
| `isize`/`usize` | 포인터 크기 정수 | (없음) |
| `f32`/`f64` | 부동소수점 | `float`/`double` |
| `bool` | 참/거짓 | `boolean` |
| `char` | 유니코드 스칼라 (4바이트) | `char`(2바이트, UTF-16 unit) |
| `()` | unit (값이 없음) | `void` (단 식이 아님) |
| `(T1, T2, ...)` | 튜플 | (없음 — record로 흉내) |

여기서 두 가지 흥미로운 점.

첫째, *unsigned 정수가 있다*. Java는 unsigned를 일관되게 다루지 못해 *부호 있는 정수로 비트만 빌려쓰는* 패턴이 흔했다(`Byte.toUnsignedInt(b)` 같은 헬퍼 함수). Rust는 처음부터 분리해서 다룬다. 바이트 처리, 네트워크 프로토콜, 임베디드에서 더 자연스럽다.

둘째, *char가 4바이트*다. Java의 `char`는 2바이트 UTF-16 unit이라서 *이모지 한 개*가 두 char로 표현된다(surrogate pair). Rust의 `char`는 *유니코드 스칼라 값* 그 자체라 이모지든 한자든 *한 char가 한 글자*다. *체감으로 가장 차이가 나는 부분*이다.

`usize`는 *처음 보면 어색한 타입*이다. 의미는 *"포인터 크기에 맞춘 부호 없는 정수"*다. 64비트 플랫폼에서는 64비트, 32비트에서는 32비트가 된다. 배열·벡터의 인덱스 타입이 `usize`다. 즉 `vec[i]`에서 `i`는 보통 `usize`여야 한다. 다른 정수 타입과 자유롭게 섞이지 않는다(*명시적 캐스트 필요*). 처음엔 번거로워 보이지만, *오버플로 사고를 줄이는 안전 장치*라고 생각하자.

암묵적 형변환이 *없다*는 것도 핵심이다. `i32` 값에 `i64` 값을 더하려면 한쪽을 명시적으로 변환해야 한다.

```rust
let small: i32 = 100;
let big: i64 = 1000;
// let sum = small + big;        // 컴파일 에러
let sum = small as i64 + big;    // OK
```

답답해 보이지만, *우연한 정밀도 손실*이 사라진다. Java의 `long * int`가 묵묵히 잘리던 함정이 *코드에 모양으로 보인다*.

## 타입 추론 — 강하지만 함수 시그니처는 명시한다

Java의 `var`(JEP 286)와 Kotlin의 타입 추론에 익숙한 사람에게 Rust의 추론은 친근하게 다가온다. 다만 *철학이 다르다*. Java/Kotlin은 *지역 변수에서만* 추론을 허용한다. Rust도 그렇다 — *함수 시그니처는 항상 명시한다*. 컴파일러가 추론할 수 있다 해도 강제로 적게 만든다.

```rust
fn add(a: i32, b: i32) -> i32 {       // 시그니처 명시 강제
    let result = a + b;                // 지역 변수는 추론 OK
    result
}
```

*왜 시그니처는 강제일까?* 답은 *"함수 경계가 곧 API 계약이기 때문"*이다. 한 함수의 시그니처가 바뀌면 그 함수를 호출하는 모든 코드의 의미가 바뀔 수 있다. 컴파일러가 매번 그 영향을 *추론으로 풀게 두면* 코드의 의도가 흐려지고 빌드가 폭발적으로 느려진다. 그래서 *경계는 명시, 내부는 추론*이라는 규칙을 박아둔다. *바람직한 분업*이다.

함수의 마지막 줄을 보면 *세미콜론이 없다*. 이게 Rust의 특이점 하나다. *세미콜론이 있으면 statement(값이 없음), 없으면 expression(값이 있음)*이다.

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b              // 세미콜론 없음 → expression → 반환값
}

// 같은 의미를 명시적으로:
fn add_explicit(a: i32, b: i32) -> i32 {
    return a + b;      // 세미콜론 있음 → return 키워드 필요
}
```

후자의 모양이 Java/Kotlin과 같다. 전자의 모양이 *Rust스러운 관용*이다. 처음엔 어색해도, 코드가 *간결해지는 효과*가 크다.

## if·match·loop — expression의 세계

if도 expression이다.

```rust
let max = if a > b { a } else { b };
```

Java에서 `int max = a > b ? a : b;`로 적던 그 모양이 Rust에선 *if 그 자체*다. 삼항 연산자가 *별도로 없다* — *if expression이 그 일을 한다*.

여기서 진짜로 흥미로운 도구가 `match`다. Java 17의 sealed class + switch pattern matching에 익숙한 사람이라면 *"아, 이거 비슷한 건가?"* 싶을 텐데, *Rust의 match가 한 발 더 나간 형태*다.

```rust
enum HttpStatus {
    Ok,
    NotFound,
    Redirect(String),       // 데이터를 가진 enum
    ServerError { code: u16, message: String },
}

fn describe(status: HttpStatus) -> String {
    match status {
        HttpStatus::Ok => "정상".to_string(),
        HttpStatus::NotFound => "찾을 수 없음".to_string(),
        HttpStatus::Redirect(url) => format!("리다이렉트 → {url}"),
        HttpStatus::ServerError { code, message } => {
            format!("서버 오류 {code}: {message}")
        }
    }
}
```

세 가지 사실이 한꺼번에 보인다.

첫째, *Rust의 enum은 데이터를 가질 수 있다*. `Redirect(String)`처럼 변형마다 다른 타입의 값을 *내장*한다. 이걸 *algebraic data type*이라고 부른다. Java/Kotlin이 sealed class와 record로 흉내내려는 모양의 *원형*에 가깝다. Java의 코드와 비교해보면 차이가 더 뚜렷하다.

```java
sealed interface HttpStatus permits Ok, NotFound, Redirect, ServerError {}
record Ok() implements HttpStatus {}
record NotFound() implements HttpStatus {}
record Redirect(String url) implements HttpStatus {}
record ServerError(int code, String message) implements HttpStatus {}

String describe(HttpStatus status) {
    return switch (status) {
        case Ok ok -> "정상";
        case NotFound nf -> "찾을 수 없음";
        case Redirect(String url) -> "리다이렉트 → " + url;
        case ServerError(int code, String message) -> "서버 오류 " + code + ": " + message;
    };
}
```

문법이 비슷하다. 그런데 *Rust 쪽이 한 파일에 깔끔하게 모인다*. 변형마다 별도 record를 선언하지 않아도 된다. *enum 한 덩어리에 모든 변형이 산다*.

둘째, *match가 exhaustive다*. 모든 변형을 다루지 않으면 컴파일 에러가 난다. Java 17의 switch pattern도 sealed에 대해서는 exhaustive를 요구하기 시작했지만, *non-sealed에는 default가 강제*된다. Rust는 enum이 곧 sealed이므로 *항상 exhaustive*다. 새 변형이 enum에 추가되면 *match를 안 고친 모든 코드가 컴파일러에 의해 발견*된다. 이게 운영 사고를 줄이는 가장 큰 안전 장치다.

셋째, *match가 expression이다*. 위 함수의 본문 전체가 *match 한 식*이고 그 식의 값이 함수의 반환값이다. Java도 switch expression으로 이걸 따라잡았지만, Rust는 처음부터 그 모양으로 설계됐다.

`if`의 사촌격으로 `if let`도 자주 쓴다. 한 변형만 관심 있을 때다.

```rust
let status = HttpStatus::Redirect("https://example.com".to_string());

if let HttpStatus::Redirect(url) = status {
    println!("리다이렉트할 URL: {url}");
}
```

*Java 21의 `if (obj instanceof Redirect r)` 패턴*과 정확히 같은 의도다. 다만 Rust 쪽이 *더 일찍 자리잡았고 더 자연스럽다*.

루프는 세 가지가 있다.

```rust
// 무한 루프 (이걸로 break해서 빠져나옴)
loop {
    if condition() { break; }
}

// 조건부 루프
while still_running() {
    do_work();
}

// 이터레이션
for item in collection {
    process(item);
}
```

`for in`이 Java의 `for-each`와 의미가 같다. 다만 *Rust의 for는 더 강력하다*. 컬렉션의 *iterator를 자동으로 호출*하고, *클로저 체인(map, filter, fold)*과 매끄럽게 합성된다.

```rust
let sum: i32 = (1..=100)
    .filter(|n| n % 2 == 0)     // 짝수만
    .sum();

println!("{sum}");              // 2550
```

Java 8의 Stream API와 모양이 비슷하다. 차이가 하나 있다면, *Rust의 iterator는 lazy하면서도 zero-cost*다. 위 체인은 컴파일러가 *단일 루프로 인라인*해버리기 때문에 추상화 비용이 0에 수렴한다. Java Stream의 박싱 비용 같은 건 없다. *추상화가 공짜*라는 Rust의 약속이 가장 명료하게 드러나는 지점이다.

## 모듈 시스템 — package + 가시성을 한 도구로

Java/Kotlin에서 패키지와 가시성을 떠올려보자. `package com.example.foo;` 선언, `public`/`protected`/`package-private`/`private` 접근제어자, JPMS의 `module-info.java`까지. *세 층*에 걸쳐 정리돼 있다. Rust에서는 이걸 *crate + mod + pub*의 한 모델로 통합한다.

용어 먼저 정리하자.

- **crate**: Rust의 컴파일 단위. *Maven의 artifact*에 해당한다. 한 crate는 한 개의 라이브러리(`.rlib` 또는 `.so`)나 실행 파일을 만든다.
- **module (mod)**: crate 안의 *namespace*. Java의 package에 가깝다. 다만 *파일 시스템과 1:1 매칭이 강제되지 않는다* — 한 파일 안에 여러 module을 선언해도 되고, 한 module을 여러 파일에 걸쳐 선언해도 된다(하위 mod 분할).
- **pub / pub(crate) / pub(super)**: 가시성. *Java보다 더 세분화*돼 있다.

`pub` 한 단어로 훑어보자.

```rust
mod auth {
    pub struct User {            // 외부에서 보임
        pub name: String,        // 필드도 별도 pub 필요
        password_hash: String,   // 필드는 디폴트로 mod 안에서만
    }

    pub(crate) fn validate(u: &User) -> bool {
        // 같은 crate 안에서만 보임 (외부 crate에는 숨김)
        !u.password_hash.is_empty()
    }

    fn private_helper() {
        // 같은 mod 안에서만 보임
    }
}
```

Java와 한 줄 한 줄 매핑하면 이렇다.

| Rust | Java |
|---|---|
| `pub` | `public` |
| (디폴트) | `package-private` |
| `pub(crate)` | `module-info.java`의 `exports ... to ...`과 비슷 |
| `pub(super)` | (직접 대응 없음) |
| `pub(in path::to::mod)` | (직접 대응 없음) |

`pub(crate)`가 *흥미로운 도구*다. *crate 외부에는 숨기고 싶지만 crate 안에서는 자유롭게 쓰고 싶은* API에 쓴다. 라이브러리를 만들 때 *공개 API와 내부 헬퍼를 분리*하는 가장 자연스러운 도구다. Java의 `module-info.java`가 비슷한 일을 하지만, *모든 자바 프로젝트가 모듈을 쓰지 않는다*는 현실적 한계가 있다. Rust는 *crate가 곧 모듈*이라 이 분리가 *기본값*이다.

파일 구조는 두 스타일이 있다. *모던 스타일*(2018 edition 이후 권장)부터 보자.

```
src/
├── main.rs            # 또는 lib.rs
├── auth.rs            # mod auth
├── auth/
│   ├── login.rs       # mod auth::login
│   └── token.rs       # mod auth::token
└── infra/
    ├── db.rs          # mod infra::db
    └── cache.rs       # mod infra::cache
```

`src/main.rs`(또는 `lib.rs`)는 다음처럼 모듈을 *선언만* 한다.

```rust
mod auth;
mod infra;
```

이 한 줄이 *"`auth.rs` 파일이나 `auth/mod.rs`를 찾아 그 내용을 module로 가져오라"*는 의미다. 하위 모듈도 같은 패턴.

```rust
// auth.rs
pub mod login;
pub mod token;

pub fn shared_helper() { /* ... */ }
```

*전통 스타일*은 `auth/mod.rs`를 만들어 같은 일을 한다. 둘 다 작동하지만, *모던 스타일이 권장*이다. 파일 트리만 봐도 모듈 구조가 보이고, `mod.rs`라는 *이름이 덜 의미적*이라는 비판이 있었기 때문이다.

다른 mod의 항목을 가져올 땐 `use`다. Java의 `import`에 해당한다.

```rust
use crate::auth::User;          // crate 루트에서 시작하는 절대 경로
use super::shared_helper;       // 부모 mod에서
use self::login::Token;         // 같은 mod의 하위
```

*prelude*라는 흥미로운 도구가 하나 더 있다. *"import 없이 보이는 항목 모음"*이다. `Option`, `Result`, `Vec`, `String`, `Box`, `Drop`, `Clone` 같이 *거의 모든 코드에서 쓰이는 항목*은 prelude에 들어 있어서 import 없이 바로 쓸 수 있다. Java라면 `java.lang.*`이 자동으로 import되는 것과 비슷한 발상이다.

## prelude — 이미 import된 친구들

prelude에 들어 있는 항목을 한번 훑어보자. 자주 만나는 것들이다.

```rust
// 표준 라이브러리 prelude (자동 import)
Option, Some, None
Result, Ok, Err
Vec
String
Box
Clone, Copy
Drop
Iterator, IntoIterator
ToString, ToOwned
Debug (트레잇은 보통 derive로 사용)
PartialEq, Eq, PartialOrd, Ord
Send, Sync
```

*이 친구들은 import 없이 바로 보인다*. Java로 치면 `Optional`, `String`, `ArrayList`, `Comparable`을 import 없이 쓸 수 있다는 뜻이다. 그래서 Rust 코드의 `use` 줄이 Java의 `import`보다 *대체로 짧다*.

라이브러리도 자체 prelude를 제공할 수 있다. tokio는 `tokio::prelude`(이제는 deprecate됐지만 한때 표준이었다), diesel은 `diesel::prelude::*`를 쓴다. 라이브러리 문서에 *"prelude를 import하라"*는 안내가 있으면 *"이 라이브러리가 자주 쓰는 트레잇 묶음"*이라는 뜻이다. Spring의 `import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*` 같은 패턴이 *언어 차원에서 표준화*된 셈이다.

## 함수 — 일급 시민, 그리고 클로저

함수 자체는 익숙한 모양이지만 한 가지 짚을 게 있다. *Rust 함수는 일급 시민*이다. 변수에 담고, 인자로 넘기고, 반환할 수 있다. 클로저(Java의 람다)도 자연스럽게 같은 모양으로 쓰인다.

```rust
fn double(x: i32) -> i32 {
    x * 2
}

let f: fn(i32) -> i32 = double;     // 함수 포인터
let g = |x: i32| x * 2;             // 클로저
let h = |x| x * 2;                  // 타입 추론

println!("{} {} {}", f(5), g(5), h(5));   // 10 10 10
```

세 모양이 모두 같은 동작을 한다. Java 8 이후의 `Function<Integer, Integer>` + 람다와 모양이 비슷한데, *Rust 쪽이 더 가볍다*. 박싱이 없고, 인라인이 잘 된다.

클로저는 *환경을 캡처하는 방식*에서 trait 이름이 결정된다. `Fn`, `FnMut`, `FnOnce` 세 가지인데, 이 셋의 차이는 *4장 소유권을 본 뒤에* 명료해진다. 지금은 *"보통 클로저는 자동으로 잘 동작하고, 가끔 컴파일러가 'this closure implements FnMut, not Fn' 같은 메시지를 띄울 때 그 차이를 의식하게 된다"* 정도만 손에 묻혀두자.

## String과 &str — 함정 5의 첫 만남

여기서 *Rust 입문자가 가장 많이 헷갈리는 지점* 하나를 미리 짚어두자. 문자열 타입이 *두 개*다.

```rust
let owned: String = String::from("Hello");   // heap-allocated, owned
let borrowed: &str = "Hello";                 // borrowed view
let borrowed2: &str = &owned;                 // String을 &str로 빌림
```

`String`은 *heap에 잡힌, 소유권을 가진, 늘어날 수 있는 문자열*이다. Java의 `StringBuilder`에 가깝다. `&str`은 *빌려온 view*고 *변경 불가*다. 문자열 리터럴 `"Hello"`의 타입이 `&str`이다.

이게 왜 두 개로 나뉘어 있을까? Java/Kotlin의 `String`은 *항상 immutable이고 ownership 개념이 없으니* 한 타입으로 충분했다. Rust에서는 *소유 vs 빌림*이 언어 차원의 1급 구분이라서, *문자열도 그 구분을 따라야* 한다. 처음엔 답답하다.

처방은 단순하다. *디폴트 패턴*을 머리에 박아두자.

- *함수의 입력 파라미터*는 보통 `&str`로 받는다. 호출자에게 *소유권을 옮기지 않아도 되니* 가장 유연하다.
- *함수의 반환값이나 구조체 필드*는 보통 `String`으로 잡는다. *데이터를 들고 있으려면 소유*해야 한다.

```rust
fn greet(name: &str) -> String {        // 입력은 빌림, 반환은 소유
    format!("Hello, {name}!")
}

let user_name = String::from("Spring 개발자");
let message = greet(&user_name);        // String을 &str로 빌려 넘김
println!("{message}");                   // "Hello, Spring 개발자!"
```

이 디폴트 한 줄을 머리에 박아두면 *처음 한 달의 90% 상황을 풀 수 있다*. 자세한 *왜*는 4장 소유권에서 풀린다. 지금은 *"두 개가 있다는 사실과, 함수 파라미터는 보통 &str"*만 기억하자. 이 미묘한 어긋남이 4장의 첫 컴파일 거부로 이어지는 다리다.

## struct와 derive — 도메인 모델의 첫 모양

비즈니스 도메인을 모델링하려면 struct가 필요하다. Java의 record와 모양이 가장 비슷한 도구다.

```rust
struct User {
    id: i64,
    email: String,
    created_at: i64,        // unix timestamp 가정
}

impl User {
    fn new(id: i64, email: String, created_at: i64) -> Self {
        User { id, email, created_at }
    }

    fn is_recent(&self) -> bool {
        let now = current_unix_timestamp();
        now - self.created_at < 86400
    }
}

fn current_unix_timestamp() -> i64 {
    // (실제로는 std::time::SystemTime을 쓴다)
    0
}
```

여기서 두 가지가 흥미롭다.

첫째, *필드와 메서드가 분리*된다. struct 본문에는 *데이터 필드만* 있고, 메서드는 별도 `impl` 블록에 둔다. Java의 클래스가 *데이터와 행동을 한 덩어리*에 묶는 것과 다른 발상이다. *왜 이렇게 분리했을까?* 답은 *"데이터와 행동의 결합도를 낮추고, 한 데이터 타입에 여러 impl 블록을 자유롭게 추가할 수 있게"* 하기 위함이다(7장 trait에서 다시 본다). 처음엔 어색하지만 *지나면 자연스러워진다*.

둘째, `Self`가 *현재 impl 블록의 타입*을 가리키는 *별칭*이다. `User`라고 적어도 같지만, *리팩토링에 강하다*. 타입명을 바꿔도 `Self`는 자동으로 따라간다.

도메인 모델에 *기본 트레잇 묶음*을 자동으로 부여하는 도구가 `#[derive(...)]`다.

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
struct User {
    id: i64,
    email: String,
    created_at: i64,
}
```

이 한 줄로 *디버그 출력*, *복제*, *동등 비교*가 자동으로 구현된다. Lombok의 `@Data` + `@Builder`와 의도가 같다. 다만 *Lombok은 IDE 외부에서는 동작이 잘 안 보이는 마법*이라면, Rust의 `derive`는 *컴파일러가 토큰 레벨에서 진짜 코드를 펼쳐* 내부 검증을 거친다. `cargo expand`(`cargo install cargo-expand`로 설치)로 그 펼친 모양을 *실제 코드로* 볼 수 있다. 마법의 거리감이 *훨씬 적다*.

자주 쓰는 derive를 미리 모아두자.

- `Debug` — `{:?}` 포매터로 출력 가능 (`println!("{:?}", user)`).
- `Clone` — `.clone()` 메서드 호출 가능.
- `Copy` — *값 의미로 복사* (작은 타입에만, `Clone`이 함께 필요).
- `PartialEq, Eq` — `==`/`!=` 비교 가능.
- `PartialOrd, Ord` — 정렬 가능.
- `Hash` — HashMap의 키로 사용 가능.
- `Default` — `T::default()`로 디폴트 인스턴스 생성.
- `serde::Serialize, serde::Deserialize` — JSON 등 직렬화 (별도 crate 필요).

도메인 모델을 짤 때 *반사적으로* 다음 정도는 붙여두는 편이 낫다.

```rust
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
struct User { /* ... */ }
```

## 에러 메시지 읽는 법 — 4장 첫 컴파일 거부 앞의 다리

이 장의 마지막 절은 *Rust 컴파일러의 에러 메시지를 읽는 법*이다. 다음 장(4장 소유권)에서 처음으로 *"왜 이게 컴파일이 안 되지?"*라는 질문에 부딪히게 된다. 그때를 위한 사전 준비다.

Rust의 컴파일러 메시지는 *친절하기로 유명*하다. JVM 진영의 NullPointerException 한 줄과 비교하면 *책 한 페이지처럼 길다*. 처음엔 *길어서 부담*이지만, *그 안에 답이 들어 있는 경우가 대부분*이다. 한 번 길게 읽어보자.

가상 예제 하나를 짜보자.

```rust
fn main() {
    let s = String::from("Hello");
    let t = s;
    println!("{s}");        // 일부러 에러 유발
}
```

`cargo run`을 치면 다음과 같은 에러가 뜬다.

```
error[E0382]: borrow of moved value: `s`
 --> src/main.rs:4:16
  |
2 |     let s = String::from("Hello");
  |         - move occurs because `s` has type `String`, which does not implement the `Copy` trait
3 |     let t = s;
  |             - value moved here
4 |     println!("{s}");
  |                ^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
3 |     let t = s.clone();
  |              ++++++++

For more information about this error, try `rustc --explain E0382`.
```

이 메시지를 *한 부분씩* 뜯어보자.

1. **에러 코드** (`error[E0382]`): 첫 줄의 `[E0382]` 같은 코드. `rustc --explain E0382`를 치면 *그 에러의 일반론적인 설명*을 책 한 단원처럼 펼쳐준다. 처음 한 달은 모르는 코드가 뜰 때마다 한 번씩 explain을 쳐보자. *공식 문서를 손에 쥐고 학습하는 셈*이다.

2. **요약** (`borrow of moved value: 's'`): 무엇이 잘못됐는지 한 줄. *영문이지만 단어가 정확하다*. "moved", "borrow", "owned"는 4장에서 익숙해진다.

3. **위치 표시** (`--> src/main.rs:4:16`): 파일·줄·열. IDE의 클릭 가능한 링크로 보통 동작한다.

4. **본문 — 컨텍스트 표시**: 문제 라인 주변을 *그림으로* 보여준다.
   ```
   2 |     let s = String::from("Hello");
     |         - move occurs because `s` has type `String`, which does not implement the `Copy` trait
   3 |     let t = s;
     |             - value moved here
   4 |     println!("{s}");
     |                ^ value borrowed here after move
   ```
   *세 줄에 걸친 에러의 흐름*이 한 그림에 보인다. 어디서 move가 일어났고, 어디서 그 다음 사용이 일어났는지가 *시각적으로* 표시된다. 이 정도까지 친절한 컴파일러는 정말 드물다.

5. **help / suggestion**: 가능한 처방. 위 예제에서는 `s.clone()`으로 고치라는 *구체적인 제안*까지 준다. *문자 그대로* 그 자리에 `clone()`을 붙이면 된다.

처음 한 달의 *가장 빠른 학습 전략*은 단순하다. *컴파일러가 보여주는 메시지를 그대로 따르는 것*이다. *"borrow checker를 적이 아니라 동료(co-author)로 받아들이자"*는 표현이 자주 등장하는데,[^1] 이게 진심으로 맞다. 처음엔 컴파일러가 *너무 까다로운 시니어*처럼 느껴진다. 두 달쯤 지나면 *"왜 그렇게 까다롭게 굴었는지"*가 이해된다. 석 달이 되면 *그 시니어가 잡아주지 않는 코드는 오히려 불안하게* 느껴진다. 일종의 사고방식의 전환이다.

흔히 쓰는 한 가지 처방을 미리 알려두자. 에러 메시지가 너무 길거나 복잡할 때는 `cargo build 2>&1 | less` 또는 `cargo build 2>&1 | head -50`으로 *처음 에러 한두 개만* 본다. 첫 에러를 고치면 종종 그 뒤의 에러들이 *연쇄적으로 사라진다*. 한꺼번에 다 풀려고 하지 말자. *한 개씩, 위에서부터*.

## 마무리 — 다음 장의 다리

이 장에서 우리가 한 일을 정리해보자. 변수의 불변 디폴트가 *어떤 무게*인지를 봤고, 원시 타입의 지도를 그렸다. 함수와 if·match·loop의 *expression-oriented* 모양을 익혔다. 모듈과 가시성이 Java의 그것보다 *더 세분화된 모델*이라는 것을 봤고, struct와 derive로 도메인 모델의 첫 모양을 잡았다. 끝으로 *Rust 컴파일러 에러 메시지의 구조*를 한 번 펼쳐 봤다.

기억해두자. 이 장에서 익힌 도구들은 *모두 4장의 소유권으로 이어지는 다리*다. `let`과 `let mut`이 가변성을 명시하는 모양은 *소유권의 move 의미*로 확장된다. `String`과 `&str`의 두 모양은 *소유와 빌림*의 가장 첫 사례다. struct의 필드 선언은 *그 필드를 누가 소유하느냐*는 질문으로 이어진다. *지금까지 익힌 모양들이 의미를 갖는 자리가 4장*이다.

다음 장에서는 드디어 *Rust의 가장 인상적인 한 가지*를 만난다. *"한 명만 가진다"*는 단순한 규칙이 어떻게 NPE, memory leak, use-after-free, double-free를 *동시에* 컴파일 타임에 차단하는지를 본다. 그리고 그 첫 만남에서 컴파일러가 *우리 코드를 거부*하는 풍경에 부딪힌다. 이 장 끝에서 본 에러 메시지 읽기가 *그때 진짜로 도움이 된다*.

## 함께 해보자

자기가 Java로 짜본 적 있는 *작은 도메인 클래스 하나*를 떠올려보자. 예를 들어 사용자 모델 같은 것이다. 다음처럼 Rust struct로 옮겨보자.

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
struct User {
    id: i64,
    email: String,
    created_at: i64,         // unix timestamp
    is_admin: bool,
}

impl User {
    fn new(id: i64, email: String, created_at: i64) -> Self {
        User {
            id,
            email,
            created_at,
            is_admin: false,
        }
    }

    fn promote(&mut self) {
        self.is_admin = true;
    }

    fn display(&self) {
        println!("{:?}", self);
    }
}

fn main() {
    let mut user = User::new(1, "toby@example.com".to_string(), 1700000000);
    user.display();
    user.promote();
    user.display();
}
```

이 코드를 짜본 뒤 다음을 손으로 확인해보자.

1. `#[derive(Debug)]`를 빼고 `cargo build`를 시도해보자. 어떤 에러가 뜨는가? 그 에러를 읽어 *왜* 그런 에러가 나는지 한 줄로 적어보자.
2. `email` 필드를 `pub email: String`으로 바꾼 뒤 다른 모듈에서 직접 접근해보자. Java의 *getter 없이 public 필드에 직접 접근*하는 감각이 어떻게 다른가? 한 줄로 적어보자.
3. `cargo expand`(`cargo install cargo-expand` 후)를 쳐 `#[derive(Debug, Clone, PartialEq, Eq)]`가 *실제로 어떤 코드를 만들어내는지* 펼쳐보자. Lombok의 `@Data`가 IDE에서만 보이는 마법이라면, Rust의 derive는 *진짜 코드*다.
4. 이 `User` struct를 `let user_a = User::new(...); let user_b = user_a;` 후 `user_a.display();`를 시도해보자. *어떤 에러가 나는가?* 그 에러가 *4장에서 정면으로 다룰* 그 에러다.

다음 장에서는 마지막 4번 시도가 왜 거부되는지를 정면으로 푼다. *세 가지 단순한 규칙*이면 답이 나온다.

---

## 참고

[^1]: ["The Borrow Checker: Rust's Tough-Love Mentor" — woodruff.dev](https://www.woodruff.dev/the-borrow-checker-rusts-tough-love-mentor/); ["Rust ownership and borrows: Fighting the borrow-checker" — DEV.to](https://dev.to/daaitch/rust-ownership-and-borrows-fighting-the-borrow-checker-4ea3).

---
