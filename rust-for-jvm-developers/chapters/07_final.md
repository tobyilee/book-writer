# 7장. 트레잇·제네릭·패턴 매칭·에러 처리 — 표현력 도구상자 (전반부)

소유권·빌림·라이프타임의 세 챕터를 지나오면서, 우리는 *컴파일러와 친구가 되는 길*을 절반 정도 걸어왔다. 이제 손에 든 것이 안전성이라는 토대다. 그 토대 위에서 *우리가 표현하고 싶은 것을 어떻게 표현할 것인가* — 그게 7장의 주제다. JVM에서는 인터페이스·제네릭·sealed class·checked exception이 그 일을 했다. Rust는 그 자리에 다른 도구들을 놓았다. 트레잇, 제네릭, enum + match, 그리고 `Result<T, E>`. 이름은 비슷한데 의미가 결정적으로 다르다. *그 차이를 받아들이는 순간, Rust의 표현력이 보인다*.

7장이 책의 무게중심에서 가장 *후련한* 챕터다. 4~6장이 답답함과 패턴 인식의 곡선이었다면, 7장은 그 패턴을 손에 쥔 우리가 *표현력의 보상*을 받는 자리다. 한 단락씩 천천히 가져가자.

## 트레잇은 인터페이스가 아니다

가장 먼저 짚어야 할 한 줄이다. **트레잇은 인터페이스가 아니다.** 비슷해 보이고 비슷하게 쓰이지만, 의미가 결정적으로 다르다. 이 차이를 받아들이는 데 일주일쯤 걸린다. 그러고 나면 *"왜 진작 이렇게 안 만들었지"*라는 후련함이 따라온다.

차이의 핵심은 한 줄이다. *인터페이스는 타입이 자기를 구현하겠다고 선언한다. 트레잇은 외부에서 어떤 타입에 트레잇 구현을 추가할 수 있다.*

Java로 보자.

```java
public interface JsonSerializable {
    String toJson();
}

public class User implements JsonSerializable {
    private String name;
    @Override
    public String toJson() {
        return "{\"name\":\"" + name + "\"}";
    }
}
```

`User`가 `implements JsonSerializable`을 *직접 선언*해야 한다. `User`의 소스를 우리가 가지고 있어야 한다. 만약 `User`가 외부 라이브러리에서 온 클래스라면? 우리는 어쩔 수 없이 `UserJsonAdapter`를 만들거나, decorator 패턴을 동원하거나, AOP를 끌어와야 한다.

Rust로는 같은 일을 이렇게 할 수 있다.

```rust
trait JsonSerializable {
    fn to_json(&self) -> String;
}

// 외부 crate에서 온 타입에 트레잇 구현을 추가
impl JsonSerializable for std::time::Duration {
    fn to_json(&self) -> String {
        format!("{{\"secs\":{}}}", self.as_secs())
    }
}
```

`Duration`은 표준 라이브러리의 타입이다. 우리가 정의한 게 아니다. 그런데 우리는 *우리의 트레잇*을 *그 외부 타입에 구현*했다. 이게 바로 인터페이스가 못 하는 일이다.

이 자유에는 한 가지 안전 장치가 붙는다. **orphan rule** — 트레잇 구현은 *트레잇 자체와 타입 중 적어도 하나는 우리 crate에서 정의되어야 한다*. 즉 *남이 만든 트레잇*을 *남이 만든 타입*에 구현하는 것은 금지된다. 그렇지 않으면 두 라이브러리가 같은 트레잇·같은 타입에 대해 *서로 다른 구현*을 해버려서 충돌이 일어난다. 이 규칙이 없는 Scala 같은 언어에서 가끔 발생하는 implicit 충돌을, Rust는 컴파일러가 미리 차단한다.

JVM에서 우리가 익숙했던 또 다른 패턴 — Spring의 `@Component`/`@Service`로 만들어지는 의존성 그래프 — 와도 발상이 다르다. Spring DI는 *런타임에 컨테이너가 인스턴스를 주입*한다. 트레잇은 *컴파일 타임에 타입 시스템 안에서 동작*을 합성한다. 그래서 트레잇 기반 코드는 *런타임 리플렉션 없이* 같은 일을 해낸다. Spring 없이도 의존성 주입의 명료함을 *타입으로* 표현할 수 있는 이유가 여기 있다.

## 정적 디스패치와 동적 디스패치 — 우리가 명시적으로 고른다

트레잇을 사용하는 두 가지 방식이 있다. *정적 디스패치(static dispatch)*와 *동적 디스패치(dynamic dispatch)*. JVM에서는 이 둘이 거의 자동으로 결정되지만, Rust는 *우리가 명시적으로 고른다*.

```rust
trait Greeter {
    fn greet(&self) -> String;
}

struct EnglishGreeter;
impl Greeter for EnglishGreeter {
    fn greet(&self) -> String { "Hello".to_string() }
}

struct KoreanGreeter;
impl Greeter for KoreanGreeter {
    fn greet(&self) -> String { "안녕".to_string() }
}

// 정적 디스패치 — generic
fn greet_static<G: Greeter>(g: &G) {
    println!("{}", g.greet());
}

// 동적 디스패치 — trait object
fn greet_dynamic(g: &dyn Greeter) {
    println!("{}", g.greet());
}
```

차이가 보이는가? `<G: Greeter>`는 *타입 파라미터*다. 컴파일 시점에 `G`가 무엇인지 결정되고, `EnglishGreeter`로 호출하면 `EnglishGreeter` 전용 코드가, `KoreanGreeter`로 호출하면 `KoreanGreeter` 전용 코드가 *각각 생성된다*. 함수 호출은 *직접 호출*이고 인라인도 가능하다. *0-cost*다.

`&dyn Greeter`는 *trait object*다. 런타임에 *vtable*을 거쳐 함수 포인터로 호출된다. Java 인터페이스 메서드 호출과 같은 모양이다. 한 단계의 indirection이 생기지만, *유연성*이 늘어난다 — `Vec<Box<dyn Greeter>>`처럼 *서로 다른 구체 타입을 한 컨테이너에 담을 수 있다*.

언제 어느 것을 쓰는가? 단순한 룰이 있다. **모르겠으면 generic부터 시작하자.** 0-cost고, 컴파일러가 타입 안전성을 더 강하게 검증한다. *런타임에 다양한 구체 타입을 한 컨테이너에 담아야 할 때*만 `dyn Trait`로 옮긴다. 그러면 우리가 트레잇을 도입한 *의도가 코드에 박힌다*.

JVM과 비교하면 이게 매우 명료해진다. Java에서는 `List<Greeter> greeters`라고 쓰면 *항상 vtable을 거치는 동적 디스패치*다. 왜냐하면 `List<EnglishGreeter>`와 `List<KoreanGreeter>`는 *같은 List<Greeter>가 아니므로*, 두 종류를 한 리스트에 담으려면 인터페이스 타입으로 통일해야 하기 때문이다. Rust는 generic이면 *한 종류만 담을 수 있는 대신* 0-cost, `dyn Trait`이면 *여러 종류를 담을 수 있는 대신* vtable. *그 선택이 우리 손에 있다*.

## 제네릭 — type erasure가 아니다

JVM 출신이 처음 만나는 또 한 번의 결정적 차이다. **Rust 제네릭은 monomorphization이지 type erasure가 아니다.**

Java에서 `List<String>`과 `List<Integer>`는 컴파일 후 *모두 그냥 `List`*로 지워진다(erasure). 런타임에 둘을 구분할 수 없다. 그래서 `instanceof List<String>` 같은 검사가 불가능하다. 또 generic 메서드가 호출될 때 타입 정보가 실제로는 사라져 있어서, reflection으로 우회하지 않으면 `T.class` 같은 걸 쓸 수 없다.

Rust는 다르다. `Vec<String>`과 `Vec<i32>`는 컴파일 시점에 *각각 별개의 코드*가 생성된다. `fn first<T>(v: &[T]) -> &T`라는 함수를 짜면, 우리가 `first(&vec_of_strings)`로 부른 자리에는 `first_String`이라는 전용 코드가, `first(&vec_of_i32s)`로 부른 자리에는 `first_i32` 전용 코드가 *각각 펼쳐진다*. 이게 monomorphization이다.

장점: *0-cost*. 타입별 전용 코드라서 인라인이 가능하고, vtable이 없고, boxing/unboxing이 없다. JVM에서 `List<Integer>`에 `Integer` 박싱이 일어나는 비용이 Rust에서는 *원천적으로 없다*. `Vec<i32>`는 *진짜 i32들의 배열*이다.

단점: *컴파일 시간이 늘고 바이너리가 커진다*. `Vec<String>`, `Vec<i32>`, `Vec<User>`, `Vec<Order>`를 각각 쓰면 네 종류의 `Vec` 코드가 생성된다. 이게 후에 13장에서 다룰 *컴파일 시간 함정*의 한 원인이 된다. 함정이지만, 트레이드오프가 명료하다 — *런타임 0-cost를 위해 컴파일 시간을 지불하는 모델*.

generic과 trait bound를 함께 써보자.

```rust
fn print_all<T: std::fmt::Display>(items: &[T]) {
    for item in items {
        println!("{item}");
    }
}
```

`T: Display`는 *"`T`는 `Display` 트레잇을 구현한다"*는 제약이다. Java로 옮기면 `<T extends Display>` 비슷한 모양이다. 다만 `Display`는 인터페이스가 아니라 트레잇이고, 우리가 외부 타입에도 구현을 추가할 수 있다는 차이가 있다.

여러 trait bound를 묶을 때는 `+`로 잇거나 `where` 절을 쓴다.

```rust
fn process<T: Clone + std::fmt::Debug + Send>(item: T) { ... }

// where 절로 분리하면 시그니처가 깔끔해진다
fn process<T>(item: T)
where
    T: Clone + std::fmt::Debug + Send,
{
    // ...
}
```

bound가 많아지면 `where` 절로 분리하는 편이 가독성이 좋다. JVM 출신은 처음에 `<T: A + B + C>` 같은 모양을 보면 답답해 보이지만, 사실 이건 *타입에 대한 명세를 한 자리에 명료하게 적은 것*이다. 메서드 시그니처를 보는 것만으로 *이 함수가 타입에 무엇을 요구하는지*가 한눈에 보인다.

## 학술적 토대 — 트레잇·제네릭의 안전성도 입증됐다

5장에서 RustBelt가 borrow의 안전성을 형식 증명했다고 짚었다. 같은 학계의 흐름은 트레잇과 제네릭에 대해서도 검증을 이어왔다. 2024년 PLDI에 발표된 「RefinedRust: A Type System for High-Assurance Verification of Rust Programs」(Gäher 외)는 trait bound와 lifetime이 결합한 코드의 안전성을 *refinement type*으로 정형화했다. 깊이 들어갈 필요는 없다. 다만 *우리가 지금 배우는 트레잇·제네릭이 그저 컴파일러 구현자의 직관이 아니라, 학계가 별도로 검증해온 모델 위에 있다*는 한 줄을 한 번 더 박아두자. 5장 끝에서 짚었던 그 한 단락의 후속편이다.

## enum + match — algebraic data type의 진짜 모습

Java 17이 sealed class와 switch pattern matching을 도입하면서 *Rust에 한 발짝 다가왔다*. 그 사실 자체가 Rust enum + match의 표현력이 얼마나 강력한지를 보여준다. 한 발짝이지, 같은 자리에 도달한 게 아니다. Java 측 발언자도 이 차이를 인정한다. *"Java's deconstruction is a baby step and not as powerful as deconstruction in Rust."*

Rust enum의 진짜 모습부터 보자.

```rust
enum HttpResponse {
    Ok(String),
    NotFound,
    Redirect { url: String, permanent: bool },
    InternalError(u16, String),
}
```

이게 enum이다. 각 variant가 *데이터를 가질 수 있다*. `Ok`는 `String` 하나, `NotFound`는 데이터 없음, `Redirect`는 두 개의 named field, `InternalError`는 두 개의 unnamed field. 이걸 algebraic data type(ADT)이라 부른다. *합(sum) 타입과 곱(product) 타입을 자유롭게 결합*할 수 있는 타입이다.

Java 17 sealed class로 비슷하게 흉내내면 이렇다.

```java
public sealed interface HttpResponse permits Ok, NotFound, Redirect, InternalError {}
public record Ok(String body) implements HttpResponse {}
public record NotFound() implements HttpResponse {}
public record Redirect(String url, boolean permanent) implements HttpResponse {}
public record InternalError(int code, String message) implements HttpResponse {}
```

기능상 비슷하다. 다섯 줄짜리 enum이 다섯 개의 record와 하나의 sealed interface로 흩어진다. 그리고 record 패턴 매칭은 *최근에야* 가능해졌다.

이걸 처리하는 match를 보자.

```rust
fn describe(response: &HttpResponse) -> String {
    match response {
        HttpResponse::Ok(body) => format!("성공: {} bytes", body.len()),
        HttpResponse::NotFound => "찾을 수 없음".to_string(),
        HttpResponse::Redirect { url, permanent } => {
            let kind = if *permanent { "영구" } else { "임시" };
            format!("{kind} 리다이렉트 → {url}")
        }
        HttpResponse::InternalError(code, msg) => {
            format!("서버 에러 [{code}]: {msg}")
        }
    }
}
```

여기서 결정적으로 중요한 한 가지를 짚어두자. *exhaustive*가 컴파일러 강제다. 만약 우리가 `InternalError` 가지를 깜빡 빼먹으면 컴파일러가 거부한다.

```
error[E0004]: non-exhaustive patterns: `&HttpResponse::InternalError(_, _)` not covered
```

*어떤 variant를 빠뜨렸는지 컴파일러가 손가락으로 짚어준다*. Java switch expression이 default를 강요하는 것과 결정적으로 다르다. default 한 줄로 *모든 미처리 케이스를 조용히 묻어버리는* 그 함정이 Rust에는 없다. 새 variant가 enum에 추가되면 *모든 match 자리가 컴파일 거부*되어 우리에게 처리를 강제한다. 1장에 적었던 운영 사고 노트가 *"새 case를 추가했는데 기존 코드 어딘가에서 default로 잘못 처리됐다"*였다면, Rust enum + match가 그 사고를 컴파일 타임에 끝낸다.

## 패턴 매칭의 깊이

`match`는 단순한 분기가 아니다. *값의 구조*를 분해하면서 분기한다. 몇 가지 자주 쓰는 패턴을 한 묶음으로 보자.

**`if let`** — 한 가지 variant에만 관심 있을 때 match를 짧게 쓴 형태.

```rust
let response = HttpResponse::Ok("data".to_string());

if let HttpResponse::Ok(body) = response {
    println!("받은 본문: {body}");
}
```

`HttpResponse`의 다른 variant는 무시한다. `if response is Ok ok && ok.body() != null`을 자바로 쓰는 것과 비교하면 훨씬 명료하다.

**`while let`** — 패턴이 매치되는 동안 반복.

```rust
let mut stack = vec![1, 2, 3];
while let Some(top) = stack.pop() {
    println!("{top}");
}
```

`Vec::pop`은 `Option<T>`를 반환한다. `Some`이 나오는 동안 반복하다가 `None`이 나오면 종료. 자바의 `while ((x = it.next()) != null)` 패턴이 *훨씬 안전하게* 한 줄에 들어온다.

**guard 절** — 패턴에 추가 조건을 붙인다.

```rust
match temperature {
    t if t < 0 => "영하",
    t if t < 20 => "선선함",
    t if t < 30 => "따뜻함",
    _ => "더움",
}
```

**구조 분해(destructuring)** — 튜플, 구조체, enum의 내부 필드를 한 번에 끄집어낸다.

```rust
struct Point { x: i32, y: i32 }
let p = Point { x: 3, y: 7 };

let Point { x, y } = p;   // x=3, y=7로 분해
println!("{x}, {y}");
```

**`@` 바인딩** — 패턴에 매치되는 *값 전체*를 동시에 잡는다.

```rust
match age {
    n @ 0..=12 => println!("어린이 {n}세"),
    n @ 13..=19 => println!("청소년 {n}세"),
    n => println!("성인 {n}세"),
}
```

이 모든 패턴이 *한 도구 안에서* 합성된다. Java가 record pattern, switch expression, instanceof pattern으로 *나눠서 가지고 있는* 능력을 Rust는 *match 한 곳*에서 표현한다. 처음에는 외울 게 많아 보이지만, 한 달쯤 지나면 *"이걸 if-else로 짜면 얼마나 답답할까"* 싶어진다.

## 에러 처리 — 예외가 아니라 *값*이다

이제 7장의 가장 큰 한 절이다. **Rust에는 예외가 없다.** throw도 없고 catch도 없다. 그러면 실패는 어떻게 표현하는가? *값으로*. `Option<T>`와 `Result<T, E>`라는 두 enum이 그 일을 한다.

`Option<T>`부터 보자.

```rust
enum Option<T> {
    Some(T),
    None,
}
```

값이 *있을 수도 없을 수도* 있을 때 쓴다. Java의 `Optional<T>`와 비슷하지만 결정적인 차이가 하나 있다 — *Rust에는 null이 없다*. Java에서 `Optional<User>`를 반환하기로 약속해도 누군가가 그냥 `null`을 반환할 수 있다. 또는 `Optional`을 쓰지 않고 `User`를 반환하면서 *내부적으로 null이 가능*할 수도 있다. Rust는 그 가능성 자체가 없다. *없을 수 있는 값*을 표현할 길이 `Option`뿐이다.

```rust
fn find_user(id: u64) -> Option<User> {
    // 찾으면 Some(user), 없으면 None
}

if let Some(user) = find_user(42) {
    println!("{}", user.name);
}
```

NPE의 가능성이 *컴파일 타임에 차단된다*. 1장에 적었던 운영 사고 노트가 NPE였다면, 같은 코드를 Rust로 옮기는 순간 *그 사고가 일어날 자리 자체가 사라진다*.

`Result<T, E>`는 한 발 더 나간다.

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

성공이면 `Ok`에 값을 담고, 실패면 `Err`에 에러 정보를 담는다. Java의 checked exception이 *시그니처에 박혀 있던 그 정신*이 살아있되, *예외가 아니라 값*이라서 함수 합성과 자유롭게 어울린다.

```rust
fn parse_age(s: &str) -> Result<u32, std::num::ParseIntError> {
    s.parse::<u32>()
}

match parse_age("42") {
    Ok(age) => println!("나이: {age}"),
    Err(e) => println!("파싱 실패: {e}"),
}
```

여기까지는 Java의 try-catch와 비슷해 보인다. 그런데 `Result`의 진짜 매력은 *합성*에서 나온다.

```rust
let ages: Result<Vec<u32>, _> = vec!["20", "30", "abc"]
    .iter()
    .map(|s| s.parse::<u32>())
    .collect();
// ages는 Err(parse error)다 — 한 번이라도 실패하면 전체가 Err
```

`Result`가 *그저 enum*이라서 `.map()`, `.and_then()`, `.collect::<Result<Vec<_>, _>>()` 같은 일반적인 함수형 도구와 자유롭게 결합된다. Java checked exception은 *예외가 메서드 시그니처를 오염*시키지만 *값이 아니라 제어 흐름*이라 이런 합성이 거의 불가능하다. lambda 안에서 checked exception을 던지려면 wrapping과 unwrapping의 지옥이 펼쳐진다. 그래서 자바 8 이후 *대다수의 코드가 RuntimeException으로 도망갔다*.

## `?` 연산자 — 에러 propagate의 한 글자

`Result`를 쓰면 매번 `match`로 풀어야 할까? 그렇지 않다. `?` 연산자가 그 일을 한 글자로 줄여준다.

```rust
fn read_user_age(path: &str) -> Result<u32, Box<dyn std::error::Error>> {
    let content = std::fs::read_to_string(path)?;
    let age: u32 = content.trim().parse()?;
    Ok(age)
}
```

`?` 한 글자가 무엇을 하는가? *현재 함수가 `Result`를 반환할 때, 이 표현식이 `Err`이면 즉시 early return*한다. 즉 위 코드는 사실 다음과 동치다.

```rust
fn read_user_age(path: &str) -> Result<u32, Box<dyn std::error::Error>> {
    let content = match std::fs::read_to_string(path) {
        Ok(s) => s,
        Err(e) => return Err(e.into()),
    };
    let age: u32 = match content.trim().parse() {
        Ok(n) => n,
        Err(e) => return Err(e.into()),
    };
    Ok(age)
}
```

`?` 한 글자가 다섯 줄을 한 줄로 줄였다. 그리고 *시그니처에 에러가 박혀 있으니* 호출자는 이 함수가 실패할 수 있다는 사실을 *반드시* 인식하고 처리하게 된다. Java의 `throws` chain이 추구한 그 정신이, *시그니처를 오염시키지 않으면서* 더 깔끔하게 살아있다.

## `From` 트레잇과 `?`의 자동 변환

`?`의 진짜 매력은 *타입 변환을 자동으로 처리*한다는 데 있다. 위 함수에서 `read_to_string`은 `std::io::Error`를 반환하고 `parse`는 `ParseIntError`를 반환한다. 둘 다 다른 타입의 에러인데, 함수 시그니처는 `Box<dyn std::error::Error>` 하나다. 어떻게 한 자리에서 두 종류의 에러가 통합될까?

답은 `From` 트레잇이다. `?`는 실패 시 `Err(e.into())`로 변환을 거친다. `into()`는 `From` 트레잇이 정의된 타입 사이를 변환하는 메서드다. `Box<dyn Error>`는 `std::io::Error`와 `ParseIntError`에 대한 `From`이 자동으로 정의되어 있어서, `?`가 알아서 변환한다.

이걸 직접 만들어보자. 예를 들어 우리 도메인의 에러 타입을 정의하고, 다른 라이브러리 에러를 흡수하고 싶다면.

```rust
#[derive(Debug)]
enum AppError {
    Io(std::io::Error),
    Parse(std::num::ParseIntError),
}

impl From<std::io::Error> for AppError {
    fn from(e: std::io::Error) -> Self { AppError::Io(e) }
}

impl From<std::num::ParseIntError> for AppError {
    fn from(e: std::num::ParseIntError) -> Self { AppError::Parse(e) }
}

fn read_user_age(path: &str) -> Result<u32, AppError> {
    let content = std::fs::read_to_string(path)?;   // io::Error → AppError 자동 변환
    let age: u32 = content.trim().parse()?;          // ParseIntError → AppError 자동 변환
    Ok(age)
}
```

`?` 한 글자가 *trait dispatch까지 자동으로 처리*한다. Java에서 같은 일을 하려면 try-catch로 받아서 다시 throw하는 변환 코드를 *모든 호출 자리마다* 적어야 한다. 그래서 자바는 결국 unchecked exception으로 도망갔다. Rust는 *trait + `?` 한 글자*로 그 패턴을 깔끔하게 풀었다.

## `panic!` — 진짜 끝났을 때

마지막 한 도구는 `panic!`이다. *복구 불가능한* 에러를 표현한다. JVM의 `Error`(OOM 같은 류)에 가깝다. 라이브러리 코드에서는 거의 쓰지 않는다 — 호출자에게 *실패 가능성*을 알리는 게 더 정직하기 때문이다. 하지만 *프로그램의 invariant가 깨졌다*는 사실을 알리고 싶을 때(예: index out of bounds, 절대 일어나서는 안 되는 case에 도달), 그때 `panic!`을 던진다.

`Option::unwrap()`, `Result::unwrap()`은 내부적으로 panic을 일으킨다. 빠른 prototyping에서는 자주 쓰이지만, 프로덕션 코드에서는 *불러일으킬 수 있는 panic이 이 한 줄에 박혀 있다*는 사실을 한 번 더 의식하는 편이 낫다. clippy는 `unwrap()` 남용을 경고로 잡아준다.

## anyhow와 thiserror — 분업의 도구

위에서 우리는 `From` 트레잇 구현을 직접 적었다. 매번 이렇게 적을까? 그렇지 않다. **두 개의 crate가 그 노동을 대신해준다.** *anyhow*와 *thiserror*. 둘은 *경쟁이 아니라 분업*이다.

**anyhow** — *애플리케이션* 코드에서. 핸들러, 서비스 코드, main 함수 등.

```rust
use anyhow::{Context, Result};

fn read_user_age(path: &str) -> Result<u32> {
    let content = std::fs::read_to_string(path)
        .context(format!("파일 {path}을 읽지 못했다"))?;
    let age: u32 = content.trim().parse()
        .context("나이를 파싱하지 못했다")?;
    Ok(age)
}
```

`anyhow::Result<T>`는 `Result<T, anyhow::Error>`의 줄임말이다. `anyhow::Error`는 *어떤 에러든 box로 감싸서 들고 다닌다*. `.context()`로 *어디서 실패했는지 사람이 읽을 수 있는 컨텍스트*를 덧붙인다. 호출 chain을 따라가며 context가 쌓이고, 최종적으로 `eprintln!("{:?}", e)`로 출력하면 *어디서부터 어디까지 실패가 전파됐는지가 한눈에 보인다*.

**thiserror** — *라이브러리* 코드에서. 도메인 모델의 에러 타입을 *enum으로 정의*할 때.

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AuthError {
    #[error("잘못된 비밀번호")]
    InvalidPassword,

    #[error("토큰이 만료됐다")]
    ExpiredToken,

    #[error("요청 한도 초과 — {0:?} 후 재시도")]
    RateLimited(std::time::Duration),

    #[error("DB 에러: {0}")]
    DatabaseError(#[from] sqlx::Error),
}
```

`#[derive(Error)]`가 `std::error::Error` 트레잇 구현을 자동 생성한다. `#[error("...")]`가 `Display` 구현을 만들고, `#[from] sqlx::Error`는 `From<sqlx::Error> for AuthError` 구현을 자동으로 깔아준다. 이제 우리 함수에서 `?` 한 글자로 sqlx 에러를 `AuthError::DatabaseError`로 변환할 수 있다.

```rust
async fn authenticate(
    pool: &sqlx::PgPool,
    username: &str,
    password: &str,
) -> Result<User, AuthError> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE name = $1", username)
        .fetch_one(pool)
        .await?;   // sqlx::Error → AuthError::DatabaseError 자동 변환

    if !verify_password(password, &user.password_hash) {
        return Err(AuthError::InvalidPassword);
    }
    Ok(user)
}
```

호출자는 `AuthError`를 보고 *어떤 종류의 인증 실패인지* 즉시 알 수 있다. `match`로 분기하면 *모든 variant를 처리하지 않으면* 컴파일이 거부된다 — 새 인증 실패 종류를 추가하면 모든 호출자가 *그것을 처리하도록 강제*된다. checked exception이 가지고 있던 그 정신이 *컴파일러 강제*로 살아있되, 시그니처가 깨끗하다.

## 분업의 기준선 — 한 줄로

언제 anyhow를, 언제 thiserror를 써야 할까? 한 줄짜리 가이드라인은 이렇다.

- **라이브러리 = thiserror** — 호출자가 *어떤 종류의 실패인지* 분간할 수 있어야 하는 자리.
- **애플리케이션 = anyhow** — 호출자가 *그저 컨텍스트와 함께 위로 던지면 되는* 자리.

Spring 프로젝트로 비유하면 *Repository/Service 계층은 thiserror*(도메인 의미를 보존), *Controller/Main은 anyhow*(컨텍스트 더해서 위로 보낸다). 이 분업이 처음에는 헷갈리지만, 한 프로젝트만 짜보면 *어느 자리에 어느 도구가 어울리는지*가 손에 묻는다.

## 1장의 운영 사고 노트, 다시 호명하자

1장 함께해보자에서 우리는 *자기 회사의 가장 최근 운영 사고 1건*을 떠올려봤다. 그 사고가 NPE였다면, 같은 코드를 Rust로 짰을 때 컴파일 타임에 잡혔을 자리는 어디인가? 아마 `Option<T>`로 표현되었어야 할 값이 그저 `User`로 반환되고 있던 함수의 시그니처 자리다. 또는 `Result<T, AuthError>`로 표현되었어야 할 인증 실패가 `User` 또는 null로 흩어져 있던 자리다.

7장의 도구들이 모이면, 우리가 일상에서 짜는 코드의 *실패 가능성이 시그니처에 명료하게 박힌다*. 그 박힘이 한 달 뒤에는 *답답함*으로 느껴지지만, 6개월 뒤에는 *대견함*으로 바뀐다. *이 함수가 어떤 입력을 받고, 어떤 출력을 주고, 어떤 실패를 가질 수 있는지*가 시그니처 한 줄에 모두 담겨 있다 — 그게 Rust 코드를 *몇 달 뒤에 다시 봐도* 즉시 이해할 수 있게 만드는 비결이다.

## 함께 해보자

7장의 도구를 한 자리에서 손으로 두드려보자. 사용자 인증 도메인을 작은 enum으로 표현하는 연습이다.

```rust
use thiserror::Error;
use std::time::Duration;

#[derive(Error, Debug)]
pub enum AuthError {
    #[error("잘못된 비밀번호")]
    InvalidPassword,

    #[error("토큰이 만료됐다")]
    ExpiredToken,

    #[error("요청 한도 초과 — {0:?} 후 재시도")]
    RateLimited(Duration),

    #[error("DB 에러: {0}")]
    DatabaseError(#[from] sqlx::Error),
}

pub struct User {
    pub id: i64,
    pub name: String,
}

pub async fn authenticate(
    pool: &sqlx::PgPool,
    username: &str,
    password: &str,
) -> Result<User, AuthError> {
    // ① 사용자 찾기 — 없으면? Option을 Result로 변환하기
    // ② 비밀번호 검증 — 틀리면 InvalidPassword
    // ③ rate limit 검사 — 초과면 RateLimited(retry_after)
    // ④ 토큰 만료 검사 — 만료면 ExpiredToken
    todo!()
}
```

이 함수의 본문을 직접 채워보자. `?` 연산자가 어디에 들어가고, 어디서 `return Err(...)`를 명시적으로 적어야 하는지 손으로 만져보자. 그다음, 같은 도메인을 *Java checked exception*으로 표현해보자. `class InvalidPasswordException extends Exception`, `class ExpiredTokenException extends Exception`, `class RateLimitedException extends Exception { Duration retryAfter; }` ... 그리고 메서드 시그니처에 `throws InvalidPasswordException, ExpiredTokenException, RateLimitedException, SQLException`을 줄줄이 적어보자. *어느 쪽이 더 답답한가*를 한 단락으로 적어보자.

이 `AuthError`는 11장 axum의 `IntoResponse` 절에서 다시 호출된다. 거기서 우리는 *도메인 에러가 HTTP 응답으로 어떻게 깔끔하게 변환되는지*를 만나게 된다. 그 변환을 직접 짜보면, *도메인 모델 → 트랜스포트 계층*의 분리가 트레잇 한 줄로 풀린다는 사실에 한 번 놀라게 된다.

7장이 책의 무게중심에서 가장 *후련한* 챕터라고 첫 단락에서 약속했다. 트레잇·제네릭·match·`Result<T, E>`라는 네 도구가 모이면, JVM에서 인터페이스·sealed class·exception이 *각자 다른 모델로 흩어져 있던* 표현력이 *한 모델 안에서 일관되게* 손에 들어온다. 그 일관성이 처음 한 달의 답답함을 보상하는, Rust 표현력의 진짜 보상이다.

다음 8장에서는 메모리 도구상자를 펼친다. `Box<T>`, `Rc<T>`, `Arc<T>`, `RefCell<T>`, `Mutex<T>` — 그리고 안전 경계의 마지막 한 절, `unsafe`. *unsafe는 컴파일러를 끄는 도구가 아니라 책임을 우리에게 옮기는 계약*이라는 정직한 한 줄로, Rust의 안전성이 어디까지인지를 명료하게 보자.

---

## 참고

- [Rust Traits are not interfaces — James Sturtevant](https://www.jamessturtevant.com/posts/rust-traits-are-not-interfaces-and-a-little-on-lifetimes/)
- [Rust Static vs. Dynamic Dispatch — softwaremill](https://softwaremill.com/rust-static-vs-dynamic-dispatch/)
- [Trait Objects to Abstract over Shared Behavior — The Rust Book](https://doc.rust-lang.org/book/ch18-02-trait-objects.html)
- [The state of pattern matching in Java 17 — deepu.tech](https://deepu.tech/state-of-pattern-matching-java/)
- [Rust Error Handling Guide 2025 — Markaicode](https://markaicode.com/rust-error-handling-2025-guide/)
- [Rust Error Handling Compared: anyhow vs thiserror vs snafu — DEV.to](https://dev.to/leapcell/rust-error-handling-compared-anyhow-vs-thiserror-vs-snafu-2003)
- Gäher, L. et al. — [RefinedRust: A Type System for High-Assurance Verification of Rust Programs (PLDI 2024)](https://plv.mpi-sws.org/refinedrust/paper-refinedrust.pdf)
- [Migrating from Java to Rust — corrode](https://corrode.dev/learn/migration-guides/java-to-rust/)
