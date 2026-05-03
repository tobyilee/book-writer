# 챕터 4. 소유권 — "한 명만 가진다"는 단순한 규칙

이 장은 이 책의 *분수령*이다. 여기서 마음을 잘 잡으면 5장 빌림과 6장 라이프타임이 *연결된 한 흐름*으로 보이고, 7장 이후의 모든 도구가 *왜 그 모양인지*가 자연스럽게 이해된다. 반대로 여기서 답답해서 도망가면 *Rust의 가장 큰 보상*을 놓치게 된다. 그래서 이 장은 *유난히 천천히 간다*. 한 페이지씩 같이 호흡하자.

3장 끝 함께해보자에서 다음 코드를 시도해보고 컴파일러에게 거부당했을 것이다.

```rust
let user_a = User::new(...);
let user_b = user_a;
user_a.display();        // 에러!
```

Java/Kotlin이라면 *너무 당연하게* 동작했을 코드다. 참조 변수 두 개로 같은 객체를 가리키는 일상 패턴이다. 그런데 Rust는 이걸 *컴파일조차 안 해준다*. *왜 그럴까?* 이 질문에 답하는 게 이 장 전체다.

먼저 한 가지 마음의 준비를 하자. *Rust의 소유권 규칙은 어렵지 않다*. 단 *세 줄*이다. 다만 *익숙해지는 데 시간이 걸린다*. 십 년 동안 *"객체는 GC가 알아서 회수한다"*는 사고로 코드를 짜온 우리에게는, *"누가 이 메모리의 주인인가"*를 매번 의식하는 게 처음에는 어색하다. 두 달쯤 지나면 그 의식이 *제2의 자연*이 된다. 그때까지 *컴파일러와 친구 되기*다.

## 세 가지 규칙

본격적으로 시작하기 전에, 외워야 할 *전부*를 한 번 보자.

1. **모든 값은 정확히 하나의 owner를 가진다.**
2. **owner가 scope를 벗어나면 값은 즉시 drop된다.**
3. **값을 다른 변수에 대입하거나 함수에 넘기면 ownership이 *이동(move)* 한다.** 단, `Copy` 트레잇이 붙은 원시 타입은 복사된다.

이 세 줄이 전부다. *그런데 이 단순한 세 줄이* NPE도, memory leak도, use-after-free도, double-free도, data race도(다음 장에서 본다) *동시에* 컴파일 타임에 차단한다. 처음 들으면 *과장 같지만* 이 장 끝에서는 그 의미가 손에 잡힌다.

한 줄씩 풀어가자.

### 규칙 1 — 단 한 명의 owner

값마다 *주인이 정확히 한 명*이다. 그 주인은 *변수*다. 다음 코드를 보자.

```rust
let s = String::from("Hello");      // s가 String 값의 owner
```

이 한 줄에서 일어난 일을 그림으로 그려보자.

- `String::from("Hello")`가 *heap에 "Hello"라는 문자열 데이터*를 잡는다.
- 그 데이터의 *포인터·길이·용량 정보를 담은 핸들*이 *스택*에 만들어진다.
- 그 스택의 핸들이 *변수 s*다. *s가 곧 owner*다.

*"한 명만 주인이 된다"*는 규칙은 *그 데이터를 누가 회수하느냐*의 책임을 명확히 하기 위함이다. 두 명이 주인이면 *두 번 회수*되거나(double-free) *서로 미루다* 영원히 회수 안 되거나(memory leak) 한다. 그래서 *주인은 한 명*이다.

### 규칙 2 — scope를 벗어나면 즉시 drop

owner인 변수가 자신의 scope를 벗어나면 *그 즉시* 값이 회수된다. JVM의 GC가 *언젠가 이 객체를 회수하겠지*라고 *런타임에 추적*하던 일을, Rust는 *컴파일 타임에 결정*한다.

```rust
fn main() {
    {
        let s = String::from("Hello");
        // s 사용 가능
    }   // 이 닫는 중괄호에서 s가 drop됨. heap의 "Hello" 데이터가 즉시 해제.

    // 여기서는 s를 쓸 수 없음 (이미 drop됨)
}
```

*"즉시"*라는 단어가 결정적이다. JVM의 `try-with-resources`나 Kotlin의 `use {}`도 비슷한 일을 *지원*하지만, *그 블록 안에서만* 동작한다. `finalize()`는 *언제 불릴지 모른다*(사실상 deprecated). Rust는 *모든 scope 종료에서* 결정적으로 drop이 호출된다. 별도 키워드도 없다. *언어 자체의 동작*이다.

이 결정성이 운영에서 큰 차이를 만든다. 파일 핸들, DB 커넥션, 락, 메모리 — *예측 가능한 시점에 풀린다*. *"왜 이 커넥션이 안 풀렸지?"*라는 질문이 거의 사라진다.

`Drop` 트레잇을 직접 구현하면 *내가 정의한 정리 동작*을 그 시점에 끼워 넣을 수 있다.

```rust
struct DbConnection {
    handle: u32,
}

impl Drop for DbConnection {
    fn drop(&mut self) {
        println!("커넥션 #{} 닫는 중...", self.handle);
        // 실제 정리 동작
    }
}

fn main() {
    let conn = DbConnection { handle: 42 };
    println!("작업 중...");
    // 여기서 conn이 scope 종료, drop() 자동 호출
}
```

실행 결과:

```
작업 중...
커넥션 #42 닫는 중...
```

*RAII*(Resource Acquisition Is Initialization)라는 C++에서 온 패턴이다. *생성과 소멸이 변수의 lifecycle에 묶여 있다*. Java의 `try (var conn = ...)` 블록에 익숙한 사람이라면 *그것보다 한 단계 더 자연스러운* 모양이라고 생각하면 이해하기 쉽다.

### 규칙 3 — move

이제 가장 인상적인 규칙이다. *대입과 전달이 ownership을 옮긴다*. 3장 끝에서 본 그 코드의 정체다.

```rust
let user_a = User::new(...);
let user_b = user_a;    // user_a의 ownership이 user_b로 이동(move)
user_a.display();        // 에러: borrow of moved value
```

*Java라면 어떻게 해석되는가*를 떠올려보자. `User user_b = user_a;`는 *참조 복사*다. user_a와 user_b가 *같은 객체*를 가리킨다. 둘 중 어느 쪽으로도 그 객체에 접근할 수 있다. JVM의 GC가 *어느 한쪽이라도 살아있는 동안*에는 그 객체를 살려둔다.

Rust는 다르게 해석한다. `let user_b = user_a;`는 *user_a가 가지고 있던 ownership을 user_b에게 넘김*이다. 그 순간 *user_a는 더 이상 그 값의 주인이 아니다*. 컴파일러는 user_a를 *"moved"* 상태로 표시한다. 그 뒤 user_a를 사용하려고 하면 *컴파일 거부*다.

*왜 이렇게 설계됐을까?* 답은 *규칙 1의 보호*다. *"주인은 한 명"*을 강제하려면 *대입 시점에 그 주인이 누구인지를 명확히* 해야 한다. 그렇지 않으면 *동시에 두 변수가 같은 메모리의 주인*이 되어, scope 종료 시 *어느 쪽이 회수해야 하는지*가 불분명해진다. 컴파일러는 그 모호함을 *원천 차단*하기 위해 move를 강제한다.

## Copy 트레잇 — 작은 예외, 큰 헷갈림

여기까지 읽고 나면 의문이 하나 든다. *"그러면 i32 같은 원시 타입도 매번 move되나?"*

```rust
let x = 5;
let y = x;
println!("{x}");        // 이건 잘 동작
```

이 코드는 에러가 나지 않는다. *왜?* `i32`는 `Copy` 트레잇이 자동으로 구현된 타입이기 때문이다. `Copy`가 붙은 타입은 *대입 시 move가 아니라 복사*가 일어난다. *원본도 살아 있고 사본도 만들어진다*.

`Copy`가 붙은 타입의 특징은 *"복사 비용이 매우 작은 타입"*이다. 다음이 자동으로 `Copy`다.

- 모든 정수 타입 (`i32`, `u64`, `usize`, ...)
- 모든 부동소수점 (`f32`, `f64`)
- `bool`, `char`
- `Copy` 타입만 담은 튜플 `(i32, bool)`
- 고정 크기 배열의 `Copy` 타입 `[i32; 4]`

*뭐가 자동으로 Copy가 아닌가*를 보면 패턴이 보인다.

- `String` — heap 데이터를 가지므로 복사 비용이 크다. *Copy 아님*.
- `Vec<T>` — 같은 이유로 *Copy 아님*.
- `User` 같은 사용자 정의 struct — 디폴트로 *Copy 아님*.

처음에는 *"왜 어떤 건 되고 어떤 건 안 되지?"*가 헷갈린다. 두 달쯤 지나면 *"heap을 가지면 move, 스택에서 끝나면 Copy"*라는 직관이 생긴다. 자세한 *왜*는 *복사가 얕은 복사인가 깊은 복사인가*의 문제다. 스택에 있는 비트는 *그대로 비트 복사*하면 된다. heap을 가리키는 핸들은 *비트만 복사하면 두 핸들이 같은 heap을 가리켜* 결국 두 명의 주인이 되어 규칙 1을 위반한다. 그래서 heap을 가진 타입은 *Copy를 자동 부여하지 않고* 명시적으로 `.clone()`을 부르게 만든다.

## 함수에 넘기는 것도 move다

대입만 move를 일으키는 게 아니다. *함수 호출에 인자로 넘기는 것*도 move다.

```rust
fn take_string(s: String) {
    println!("{s}");
    // 함수가 끝나면 s가 drop됨
}

fn main() {
    let owned = String::from("Hello");
    take_string(owned);
    // println!("{owned}");      // 에러: ownership이 take_string으로 이동
}
```

`take_string(owned)`을 호출하는 순간 *owned의 ownership이 함수의 파라미터 s로 이동*한다. 함수가 종료되면 s가 scope를 벗어나 *drop된다*. 호출자에서는 더 이상 owned에 접근할 수 없다.

처음에는 *"이게 왜 좋은 거지?"* 싶다. Java라면 *그저 참조를 넘긴 것*이고 호출자도 그 참조로 객체에 계속 접근할 수 있다. 그런데 잠시 멈추고 생각해보자. *"함수에 객체를 넘긴 뒤에도 호출자가 그 객체를 계속 쓰는 코드"*가 *얼마나 많은 사고의 원인*이었는지. 동시 수정 사고, *방어적 복사를 깜빡한 사고*, 파일 핸들이 두 곳에서 닫히는 사고. Rust는 그 카테고리를 *컴파일러가 거부*한다.

*"그런데 함수에 넘기고 나서도 계속 쓰고 싶은 일이 진짜 많지 않나?"* 맞다. 그 자연스러운 욕구를 풀어주는 두 가지 길이 있다.

길 하나: *반환받기*. 함수가 *받은 ownership을 다시 돌려준다*.

```rust
fn take_and_return(s: String) -> String {
    println!("쓰는 중: {s}");
    s   // ownership을 반환
}

fn main() {
    let owned = String::from("Hello");
    let owned = take_and_return(owned);    // 다시 받음
    println!("이제도 쓸 수 있다: {owned}");
}
```

답답하다. *함수마다 매번 반환해야 한다*. 호출자에서도 *변수 재할당*을 매번 해야 한다.

길 둘: *빌려주기(borrowing)*. *5장의 주제*다. 이 장에서는 *"길 둘이 곧 진짜 답"*이라는 것만 알아두자. 길 하나는 *4장의 한정된 도구*고, 5장에서 빌림을 배우면 이 답답함이 *깨끗이 풀린다*.

## clone() — 죄책감 없이 쓰자

길 셋이 하나 더 있다. `.clone()`이다. 명시적으로 *데이터 복사본을 하나 더 만든다*.

```rust
let owned = String::from("Hello");
let copy = owned.clone();      // heap 데이터까지 복사
println!("{owned} {copy}");    // 둘 다 살아 있음
```

`.clone()`은 *깊은 복사*다. heap에 *"Hello" 데이터를 한 벌 더* 만든다. 그래서 두 변수가 *별개의 데이터*를 owned하게 된다.

*입문자에게 가장 자주 하는 권고* 하나는 이것이다. *"clone을 죄책감 없이 쓰자."* Rust 커뮤니티에 *"clone()을 너무 많이 쓰면 성능에 안 좋다"*는 교조적인 분위기가 있는데, *입문자에게는 그 조언이 학습을 망치는 가장 큰 적*이다. 처음 한 달은 *clone으로 풀 수 있는 모든 문제를 clone으로 풀고*, 6장 이후 빌림과 라이프타임에 익숙해지면 *그때 clone을 빌림으로 옮겨가도 늦지 않다*.

```rust
fn print_user(u: User) {
    println!("{}", u.email);
}

fn main() {
    let user = User::new(...);
    print_user(user.clone());      // 복사 한 벌 만들어 넘김
    println!("{}", user.email);    // 원본도 살아 있음
}
```

성능이 *진짜로 문제가 되는 hot path*에서는 빌림으로 옮긴다. *그 외에는 clone이 충분히 좋은 답*이다. 단순한 도메인 객체 한 개를 복사하는 비용은 *현대 하드웨어에서 거의 측정 불가능*하다. 학습의 흐름을 끊지 말고 *clone으로 일단 통과시키자*. 익숙해지는 게 먼저다.

## Vec<T>로 본 move의 의미

도메인 객체 단위가 아니라 *컬렉션 단위*에서 move를 보면 그 의미가 더 또렷해진다.

```rust
fn process(numbers: Vec<i32>) -> i32 {
    numbers.iter().sum()
}

fn main() {
    let nums = vec![1, 2, 3, 4, 5];
    let total = process(nums);
    // println!("{:?}", nums);    // 에러: nums의 ownership은 process로 이동
    println!("합: {}", total);
}
```

`Vec<i32>`을 함수에 넘기면 *그 Vec 전체*의 ownership이 이동한다. 호출자에서는 더 이상 nums에 접근 못 한다. *왜 이렇게 동작하는가*는 다시 *규칙 1*이다. *주인은 한 명*. 함수 안에서도 호출자에서도 *동시에 주인*일 수 없다.

Java로 같은 의미를 짜본다고 해보자.

```java
int process(List<Integer> numbers) {
    return numbers.stream().mapToInt(Integer::intValue).sum();
}

void main() {
    List<Integer> nums = List.of(1, 2, 3, 4, 5);
    int total = process(nums);
    System.out.println(nums);    // OK — 그저 참조 복사
}
```

Java는 *그저 참조 복사*다. nums와 numbers가 *같은 List를 가리킨다*. 그래서 *호출자에서 nums.add(...)*를 하면 함수 내부에서도 *영향*을 받는다(만약 함수가 그 시점에 iteration 중이었다면 ConcurrentModificationException). 십 년 동안 *방어적 복사로 막아온 함정*이다. Rust에서는 *컴파일러가 거부*한다. 그게 이 책 1장에서 말한 *"안전을 보장하는 시점이 다르다"*의 구체적 풍경이다.

다시, 이 답답함의 답은 *5장의 빌림*이다. `&Vec<i32>`로 넘기면 *읽기만 하는 빌림*이고, ownership은 호출자에 남는다. 다음 장에서 만나자.

## String과 &str — 함정 5의 정면 처방

3장에서 *"두 개가 있다는 사실"*만 짚었던 String과 &str을 이제 *정면으로* 다룰 차례다. 이제 ownership의 눈으로 보면 *왜 두 개인지*가 자연스럽게 풀린다.

```rust
let owned: String = String::from("Hello");      // heap에 데이터, 핸들이 owner
let borrowed: &str = "Hello";                    // 프로그램 binary 안의 데이터를 빌림
let borrowed_from_owned: &str = &owned;          // owned가 가진 데이터를 빌림
```

세 변수의 정체를 그림으로 그려보자.

- `owned` — *heap에 잡힌 "Hello" 5바이트* + 그 데이터의 *포인터·길이·용량을 담은 핸들*(스택). 핸들이 owner. owned가 scope를 벗어나면 heap의 5바이트도 함께 회수.
- `borrowed` — *프로그램 binary의 read-only 영역에 박힌 "Hello" 5바이트*를 *빌려본 view*. 데이터의 owner는 *프로그램 그 자체*(`'static` 라이프타임). borrowed가 scope를 벗어나도 데이터는 그대로.
- `borrowed_from_owned` — *owned가 가진 heap 데이터를* 빌려본 view. owner는 여전히 owned. borrowed_from_owned는 *owned보다 오래 살 수 없다*(이게 6장 라이프타임의 본질).

Java/Kotlin의 `String`은 *항상 immutable이고 ownership 개념이 없다*. JVM이 *문자열 풀*로 일부 최적화를 하지만, 개발자 시야에서는 모든 String이 똑같다. Rust는 *"이 문자열의 데이터가 어디 있고 누가 주인인가"*를 *타입 차원에서 분리*한다. 처음엔 답답하다. 두 달 뒤엔 *"이 정도는 알아야 시스템을 짜지"*라는 감각이 생긴다.

함수 시그니처에서의 디폴트 패턴을 다시 한번 못 박아두자.

```rust
// 좋은 패턴: 입력은 &str, 반환은 String
fn build_greeting(name: &str) -> String {
    format!("Hello, {name}!")
}

// 답답한 패턴: 입력도 String (호출자가 ownership을 잃음)
fn build_greeting_bad(name: String) -> String {
    format!("Hello, {name}!")
}

fn main() {
    let user_name = String::from("Spring 개발자");

    let greeting1 = build_greeting(&user_name);     // 좋음: user_name 살아 있음
    println!("{greeting1} {user_name}");

    let greeting2 = build_greeting_bad(user_name);  // 답답: user_name 사라짐
    // println!("{user_name}");                      // 에러
}
```

*입력은 빌림으로, 출력은 소유로*. 이 한 줄을 머리에 새겨두자.

## Drop 트레잇 — 결정적 자원 해제의 진짜 매력

위에서 잠깐 본 `Drop`을 *제대로* 한 번 더 들여다보자. 이 트레잇 하나가 운영의 풍경을 바꾼다.

흔한 시나리오 하나. *DB 커넥션을 빌려와 작업하고, 작업이 끝나면 풀에 반납*하는 코드다. Java로 짜면 다음과 같다.

```java
try (Connection conn = dataSource.getConnection()) {
    // 작업
} // try-with-resources가 close()를 호출
```

`try-with-resources`가 처리하지만, *try 블록 안에서만* 동작한다. 메서드 안에서 `Connection`을 얻어 *반환하면* 호출자가 *닫을 책임*을 지게 된다. 그 책임 이전이 사고의 원인이다.

Rust로 짠다면.

```rust
fn process_user(pool: &ConnectionPool, user_id: i64) -> Result<User, DbError> {
    let conn = pool.acquire()?;
    let user = conn.fetch_user(user_id)?;
    Ok(user)
    // conn이 여기서 scope 종료, Drop이 호출되어 풀에 자동 반납
}
```

함수의 *어디서 return하든*, *조기 return이든*, *? 연산자로 즉시 빠져나가든*, conn이 scope를 벗어나는 *모든 경로*에서 Drop이 호출된다. *코드에 close() 한 줄도 없는데* 누수가 안 난다. *기억해두자. 이게 RAII의 진짜 매력*이다.

여러 자원이 얽혀 있을 때 더 빛난다.

```rust
fn complex_work() -> Result<(), AppError> {
    let conn = acquire_db_connection()?;     // 1번 자원
    let lock = acquire_distributed_lock()?;  // 2번 자원
    let temp_file = create_temp_file()?;     // 3번 자원

    do_work(&conn, &lock, &temp_file)?;
    Ok(())
    // 함수가 끝나면 temp_file → lock → conn 순서로 (선언 역순으로) drop
}
```

세 자원이 *선언의 역순으로* 깨끗하게 풀린다. Java라면 *try-with-resources 세 겹*이거나 *try/finally 중첩*인데, Rust는 *그저 변수 선언*만으로 같은 안전성을 얻는다. *코드가 더 짧고, 누락 가능성이 0이다*.

## 같은 의미를 두 가지 길로 풀어보자

이쯤 되면 *3장 끝의 그 코드*를 두 가지 길로 풀 수 있다. 마지막으로 그 코드를 다시 펼쳐보자.

```rust
fn main() {
    let s = String::from("Hello");
    let t = s;
    println!("{s}");     // 에러: borrow of moved value
}
```

*길 하나*: clone으로 풀기.

```rust
fn main() {
    let s = String::from("Hello");
    let t = s.clone();    // s의 데이터를 한 벌 더 만들어 t의 owner로
    println!("{s} {t}");   // 둘 다 살아 있음
}
```

*길 둘*: borrow로 풀기 (*5장의 정식 답*, 미리보기).

```rust
fn main() {
    let s = String::from("Hello");
    let t = &s;           // s를 빌림. ownership은 s에 남음
    println!("{s} {t}");   // 둘 다 사용 가능
}
```

길 둘이 더 가볍다. 데이터를 복사하지 않는다. 다만 *어떤 규칙으로 빌림이 안전을 보장하는지*가 5장의 본문이다. 일단 *두 길이 있다는 것*까지 손에 묻혀두자.

## NPE는 어디로 갔을까

여기서 한 가지 흥미로운 사실을 짚고 가자. *Rust에는 null이 없다*. 변수의 값이 *비어있을 가능성*을 표현하려면 `Option<T>`라는 enum을 *명시적으로* 써야 한다.

```rust
// Java 스타일 (Rust에선 컴파일 안 됨)
// String name = null;          // 이 자체가 문법 에러

// Rust 스타일
let name: Option<String> = None;            // 비어있음을 명시
let name2: Option<String> = Some(String::from("toby"));   // 값 있음

match name2 {
    Some(s) => println!("이름: {s}"),
    None => println!("이름이 없음"),
}
```

3장에서 잠깐 본 *exhaustive match*가 여기서 진짜로 빛난다. *Some 케이스만 처리하고 None을 빼먹으면* 컴파일러가 거부한다. Java의 `Optional<T>`도 비슷한 의도를 가지지만, `optional.get()`을 *그냥 호출해서 NPE 비슷한 NoSuchElementException을 받는* 코드가 너무 흔하다. Rust는 그 우회로를 *언어 차원에서 막아둔다*. `Option<String>`을 그냥 `String`처럼 쓸 수가 *없다*.

자세한 처방은 7장 에러 처리에서 본다. 지금 단계에서는 *"null이 아예 없다는 사실"* 그리고 *"NPE라는 사고 카테고리가 언어에서 사라진다는 사실"*만 손에 묻혀두자. 이게 1장에서 적어둔 운영 사고 메모가 NPE였다면, *그 사고는 Rust로 짠 순간 컴파일 타임에 잡혔을 것이다*. 7장에서 다시 만나자.

## Box<T> 살짝 — heap에 의도적으로 올리고 싶을 때

규칙 1·2·3까지 익혔다면 한 가지 의문이 들 수 있다. *"struct 같은 것도 매번 스택에 들어가나? heap에 올리고 싶으면?"* 답이 `Box<T>`다.

```rust
let on_stack: User = User::new(...);             // 스택에 직접
let on_heap: Box<User> = Box::new(User::new(...)); // heap에 잡고 핸들이 스택에
```

`Box<T>`는 *가장 단순한 스마트 포인터*다. *값을 heap에 올리고, 그 값의 owner는 Box 자신*이다. 함수에 넘기면 Box의 ownership이 이동하고, scope를 벗어나면 Box가 drop되면서 *heap 데이터까지 함께 회수*된다. 즉 *Box도 같은 세 가지 규칙을 따른다*.

*언제 Box가 필요한가*는 처음에는 잘 안 떠오를 수 있다. 가장 흔한 세 가지 상황만 알아두자.

1. *재귀적 자료구조* — 트리, 연결 리스트처럼 *자기 자신을 포함*하는 타입. 컴파일 타임에 크기가 무한히 커질 수 있어서 *스택에 직접 못 둔다*.
2. *큰 struct를 함수 사이로 옮기는 게 비싼 경우* — 비트 단위 복사 비용을 줄이려고 *포인터만 옮기는* 패턴.
3. *trait object* — `Box<dyn Trait>` 형태로 *다형성*을 표현 (8장 본격).

지금은 *"Box가 있다는 사실"*과 *"heap에 직접 올리고 싶을 때 쓴다"*만 손에 묻혀두자. 8장에서 `Rc<T>`, `Arc<T>`, `RefCell<T>`까지 *스마트 포인터의 전체 지도*를 그린다.

## 한국 개발자의 후기 한 줄

이 장의 무게를 *체험적으로* 한 번 환기하자. 4년간 Rust를 써온 한 한국 개발자가 자기 블로그에 이렇게 적었다. *"익숙해지면 사고가 정리되는 느낌이고, 한 번 작동하면 정말 잘 작동한다."*[^1]

이 한 줄에 두 가지 의미가 들어 있다.

첫째, *"익숙해지면"*. 익숙해지기 전까지는 답답하다는 솔직한 인정이다. corrode의 마이그레이션 가이드도 *4~6개월의 적응 기간*을 권한다.[^2] 처음 한 달은 *컴파일러가 너무 까다롭게* 느껴진다. 두 달째에 *"왜 이렇게 까다롭게 굴었는지"*가 보인다. 석 달째에 *손가락이 익는다*. 이 곡선은 누구도 건너뛰지 못한다.

둘째, *"한 번 작동하면 정말 잘 작동한다"*. 익숙해진 뒤의 보상이다. NPE도, 메모리 누수도, double-close도, 데이터 레이스도(다음 장) *컴파일러가 다 잡아준다*. 운영 중인 시스템에서 *"왜 이게 죽지?"라는 의문이 줄어든다*. 십 년 동안 우리가 *알람 받고 새벽에 깨던* 그 카테고리가 *대부분 사라진다*. 그 보상이 4~6개월의 답답함을 정당화한다.

## 마무리 — 다음 장으로의 다리

이 장에서 한 일을 정리해보자. *세 가지 단순한 규칙*을 봤다. *주인은 한 명*, *scope 종료 시 즉시 drop*, *대입과 전달은 move*. 이 세 줄이 NPE·memory leak·use-after-free·double-free를 *동시에* 차단한다는 것을 손에 담았다. `Copy` 트레잇이 *작은 예외*를 만들고, `String`과 `&str`이 *왜 두 개로 나뉘는지*가 풀렸다. `Drop`이 *결정적 자원 해제*를 약속한다는 것도 봤다.

기억해두자. *이 장의 답답함은 정상이다*. 모든 JVM 출신이 같은 자리에서 한 달 정도 답답해한다. 그 답답함이 *5장에서 깨끗이 풀린다*. *빌림*이라는 두 줄의 규칙으로, *"함수에 넘기고 나서도 계속 쓰고 싶다"*는 자연스러운 욕구가 *컴파일러와 충돌하지 않게* 표현된다. 그리고 그 두 줄의 규칙이 다시 *데이터 레이스를 컴파일 타임에 차단*하는 자리(9장 Send/Sync)로 이어진다. *모든 것이 연결돼 있다*.

다음 장 가기 전에 한 가지를 약속하자. *컴파일러가 거부하는 코드가 있을 때, 화내지 말자*. 그 메시지를 *공책에 옮겨 적고 한 줄씩 읽어보자*. 처음에는 시간이 걸리지만, *그 습관이 두 달 뒤의 풍경을 만든다*. borrow checker는 *적이 아니라 코드를 함께 짜는 시니어*다.

## 함께 해보자

다음 코드를 한번 손으로 짜보자. *일부러 컴파일이 안 되는 모양*으로 시작한다.

```rust
fn main() {
    let s = String::from("Hello, Rust!");
    let t = s;
    println!("{s}, {t}");        // 컴파일 에러
}
```

`cargo build`(또는 `cargo check`)로 에러 메시지를 띄우고, 그 메시지를 *처음부터 끝까지 한 줄씩 읽어보자*. 다음 네 가지를 손으로 직접 시도해보자.

1. *clone()으로 풀기*. `let t = s.clone();`로 바꿔 컴파일을 통과시키자. *어떤 일이 일어났는지* 한 단락으로 적어보자(heap에 무엇이 일어났는가?).

2. *borrow로 풀기*. `let t = &s;`로 바꿔 컴파일을 통과시키자. clone과 비교해 *데이터 측면에서 무엇이 다른가*를 한 단락으로 적어보자.

3. *함수로 풀어보기*. 다음 코드를 짜고 동작을 확인하자.
   ```rust
   fn print_string(s: String) {
       println!("{s}");
   }

   fn main() {
       let s = String::from("Hello");
       print_string(s);
       // print_string(s);       // 두 번째 호출에서 에러
   }
   ```
   왜 두 번째 호출이 에러인지를 *세 줄의 규칙*으로 설명해보자.

4. *Drop을 직접 구현해보기*. 다음 코드를 짜고 출력 순서를 확인해보자.
   ```rust
   struct Logger { name: String }

   impl Drop for Logger {
       fn drop(&mut self) {
           println!("Logger '{}' 종료", self.name);
       }
   }

   fn main() {
       let _a = Logger { name: "A".to_string() };
       {
           let _b = Logger { name: "B".to_string() };
           println!("내부 블록");
       }
       println!("외부 블록");
   }
   ```
   출력 순서를 *예측해본 뒤* 실행 결과와 비교해보자. *왜 B가 먼저 종료되고, A는 main의 끝에서 종료되는가?*

이 4번 예제는 *RAII의 가장 작은 모양*이다. 이 출력 순서가 *예측 가능*하다는 사실이 운영 환경에서 어떤 안심감을 주는지를 두 달쯤 뒤에 다시 떠올려보자.

다음 장에서는 *빌림(borrowing)*을 본다. *"한 명만 가진다"*는 규칙을 깨지 않으면서, *"잠깐 빌려쓰는"* 길을 푸는 *두 줄의 규칙*이 등장한다. 그리고 그 두 줄이 *데이터 레이스를 컴파일 타임에 차단*하는 자리로 9장에서 다시 호출된다. *연결이 시작된다*.

---

## 참고

[^1]: ["4년간의 Rust 사용 후기" — blog.cro.sh](https://blog.cro.sh/posts/four-years-of-rust/).
[^2]: ["Migrating from Java to Rust" — corrode](https://corrode.dev/learn/migration-guides/java-to-rust/).

---
