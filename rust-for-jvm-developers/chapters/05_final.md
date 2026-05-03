# 5장. 빌림 — `&T`와 `&mut T`, 그리고 데이터 레이스가 사라지는 이유

처음 몇 주, borrow checker가 우리 코드를 거부할 때면 어쩌면 자기 자신을 의심하게 된다. "10년을 써온 패턴인데, 왜 이게 컴파일이 안 되지?" Java에서는 너무나 당연했던 코드 — 참조 변수 두 개로 같은 객체를 가리키고, 한쪽에서 값을 바꾸면서 다른 쪽으로 읽는 그 일상의 코드 — 가 Rust에서는 빨갛게 거부된다. 난감하다. 그런데 4장의 소유권을 받아들이고 나면, 빌림은 그 답답함의 *해방구*다. ownership을 옮기지 않고도 데이터를 잠깐 빌려주는 도구가 바로 `&T`와 `&mut T`다. 그리고 이 두 줄짜리 규칙이, 놀랍게도, 우리가 지난 20년 동안 `synchronized`와 `ConcurrentModificationException`으로 골머리 앓던 그 문제를 *컴파일 타임에* 끝낸다.

이 한 문장이 너무 큰 약속처럼 들릴지 모르겠다. 하지만 천천히 따라와 보자. 5장이 끝날 때쯤이면 이 약속이 과장이 아니었다는 사실을 손으로 만져본 상태가 되어 있을 것이다.

## 4장의 그 코드를 다시 풀어보자

4장 함께해보자에서 우리는 다음 코드와 마주쳤다.

```rust
let s = String::from("hi");
let t = s;
println!("{s}");   // 컴파일 에러: borrow of moved value: `s`
```

`let t = s`에서 `String`의 ownership이 `t`로 *이동*했고, 그래서 `s`는 빈 껍데기가 됐다. 4장 처방 ①은 `clone()`이었다. 죄책감 없이 복사하라고 했다. 하지만 죄책감이 없다고 해서 비용이 없는 건 아니다. heap에 올려둔 문자열을 통째로 또 한 번 복제하는 일이다. 64바이트짜리 짧은 문자열이라면 모르겠다. 64MB짜리 이미지 버퍼라면? 매 함수 호출마다 그렇게 복제할 수는 없다. 그러면 어떻게 해야 할까?

답이 빌림이다. ownership을 옮기지 말고, 잠깐 *빌려주자*.

```rust
let s = String::from("hi");
let t = &s;          // s의 immutable borrow
println!("{s}, {t}");  // 둘 다 살아있다
```

`&s`는 "`s`의 데이터를 가리키는, 잠깐 빌린 참조"다. ownership은 여전히 `s`가 가지고 있다. `t`는 그 데이터를 *읽을 권한*만 빌렸을 뿐이다. 그래서 `s`도 살아있고 `t`도 살아있다. 함수에 넘길 때도 마찬가지다.

```rust
fn print_len(value: &String) {
    println!("길이는 {}", value.len());
}

let s = String::from("hello");
print_len(&s);
println!("{s}");   // s는 여전히 살아있다
```

JVM에서는 이게 너무나 당연한 코드여서, 따로 설명할 게 없다. Java로 옮기면 한 줄이다. `void printLen(String value) { ... }`. 그런데 Rust는 왜 이렇게 두 가지(`String`과 `&String`)를 구분하는 걸까? 그 이유가 다음 절에서 본격적으로 드러난다.

## 두 줄의 규칙

Rust의 빌림에는 단 두 줄의 규칙이 있다. 외워둘 가치가 충분하다.

1. 한 시점에 mutable borrow(`&mut T`)는 **단 하나만** 존재할 수 있다.
2. mutable borrow가 살아있는 동안 다른 어떤 borrow도(immutable이든 mutable이든) 존재할 수 없다.

뒤집어 말하면, immutable borrow(`&T`)는 *얼마든지 동시에* 존재할 수 있다. 읽기만 하는 한, 여러 명이 동시에 봐도 아무 문제가 없다. 하지만 누군가가 *쓸 권한*을 가지는 순간, 그 사람 외에는 아무도 그 데이터를 볼 수 없다. 이걸 한 줄로 줄이면 *"여러 명이 같이 읽거나, 아니면 한 명만 쓰거나"*다.

JVM 출신에게 이 규칙은 처음에는 답답하게 들린다. "그러면 동시에 두 군데서 수정하고 싶을 때는 어떻게 하나?"라는 질문이 자연스럽게 떠오른다. 그 답은 *컴파일러가 거부한다*는 것이다. 그리고 그게 5장의 핵심 주장이다 — *그 거부가 사실은 우리에게 보상*이라는 것.

코드로 보자.

```rust
let mut v = vec![1, 2, 3];
let r1 = &v;
let r2 = &v;
println!("{:?}, {:?}", r1, r2);   // OK: 읽기만 하는 두 borrow는 공존 가능
```

여기까지는 문제없다. `r1`과 `r2`는 둘 다 `&Vec<i32>`다. 둘이서 동시에 읽기만 한다. 그런데 한 줄을 더해보자.

```rust
let mut v = vec![1, 2, 3];
let r1 = &v;
let r2 = &mut v;            // 컴파일 에러
println!("{:?}, {:?}", r1, r2);
```

컴파일러는 이렇게 거부한다.

```
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> src/main.rs:4:14
  |
3 |     let r1 = &v;
  |              -- immutable borrow occurs here
4 |     let r2 = &mut v;
  |              ^^^^^^ mutable borrow occurs here
5 |     println!("{:?}, {:?}", r1, r2);
  |                            -- immutable borrow later used here
```

처음 보면 불친절해 보이지만, 자세히 들여다보면 *컴파일러가 손가락으로 줄·열을 짚어주고 있다*. immutable borrow가 어디서 시작됐는지(3번째 줄), mutable borrow가 어디서 충돌하는지(4번째 줄), 그리고 *왜* 거부했는지(5번째 줄에서 immutable borrow가 여전히 사용되기 때문). rustc 에러 메시지를 *읽는 법*을 3장 끝에서 한 번 짚었던 이유가 여기에 있다. 빌림 에러는 무서워 보이지만 사실은 *해결 방법까지 친절히 알려주는* 메시지다.

## 왜 이 규칙이 데이터 레이스를 끝내는가

이제 본격적인 한 줄을 짚어보자. *왜 이 두 줄의 규칙이 동시성 안전성으로 이어지는가?*

데이터 레이스(data race)의 정의를 먼저 떠올려보자. "두 개 이상의 스레드가 같은 메모리 위치에 동시에 접근하고, 그 중 적어도 하나가 *쓰기*이며, 그 접근들이 동기화되어 있지 않을 때" 발생하는 현상이다. JVM에서는 이걸 막기 위해 우리는 평생을 `synchronized`, `ReentrantLock`, `volatile`, `AtomicReference`, `ConcurrentHashMap`을 써왔다. 잘 썼나? 못 썼다. 운영 사고 통계를 보면 안다. NPE 다음으로 많은 게 race condition이다. 왜냐하면 *컴파일러가 강제하지 않기 때문*이다.

Rust의 두 줄 규칙을 다시 보자.

1. 한 시점에 `&mut T`는 단 하나만.
2. `&mut T`가 살아있는 동안 다른 어떤 borrow도 없다.

이 규칙을 만족하는 코드는 *정의상* 데이터 레이스가 일어날 수 없다. 두 스레드가 같은 메모리에 동시에 접근하려면 둘 다 borrow를 들고 있어야 하는데, 그 중 하나라도 `&mut`이면 다른 borrow의 존재 자체가 컴파일 거부다. 둘 다 `&T`(읽기)뿐이라면 동시 접근이 일어나도 아무도 쓰지 않으니 race가 아니다.

이게 *concurrency safety*가 *컴파일 타임*에 보장된다는 말의 의미다. Rust 표준 라이브러리는 여기에 `Send`와 `Sync`라는 마커 트레잇을 더해서 *어떤 타입이 스레드 사이를 안전하게 오갈 수 있는지*까지 타입 시스템에 박아놓았다. 그 이야기는 9장의 몫이다. 5장에서는 *그 토대가 빌림 규칙*이라는 사실만 가져가자.

JVM에서 우리가 흔히 마주치던 시나리오를 떠올려보자. `@Service`에 `private List<Order> orders = new ArrayList<>();`를 두고, 두 메서드가 동시에 그것을 수정한다고 해보자. 컴파일러는 아무 말이 없다. 잘 돌아가는 줄 알았는데 운영에서 `ConcurrentModificationException`이 터진다. 또는 더 무서운 경우 — 예외 없이 *데이터가 조용히 깨진다*. 우리는 그걸 막으려고 `Collections.synchronizedList`로 감싸거나 `CopyOnWriteArrayList`로 바꾸거나 `ConcurrentHashMap`을 끌어온다. 이 모든 결정이 *런타임에·관행으로·코드 리뷰로* 보장되는 것이다.

Rust에서 같은 자료 구조를 두 메서드가 동시에 수정하려고 하면? 빌림 단계에서부터 컴파일이 거부된다. 만약 그 자료 구조를 *진짜로 두 스레드가 공유해야* 한다면, 우리는 명시적으로 `Arc<Mutex<Vec<Order>>>` 같은 모양을 골라야 한다(8장에서 본격적으로 다룬다). 그 *선택이 코드에 박혀* 있다는 사실이, 6개월 뒤 가장 큰 보상이 된다.

한 줄로 정리하자. **Java의 모든 객체 참조는 늘 mutable이고 동시 접근이 허용된다 — Rust는 그 일상 코드를 컴파일러가 거부한다.** 이 비대칭이 5장의 핵심이다. 흔히 "&T는 final 참조와 같다"고 단순화하는 설명을 만나게 되는데, 그건 정확하지 않다. Java의 `final` 참조는 *재할당 금지*일 뿐, 그 객체의 내부 필드를 바꾸는 것은 막지 못한다. `final List<String> list = new ArrayList<>();` 다음에 `list.add("hi");`는 멀쩡히 동작한다. 반면 `&Vec<String>`은 *그 안의 내용까지* 바꿀 수 없다. 두 개념은 의미 자체가 다르다.

## `&mut T`는 정말 한 명만 — 그 뜻을 손으로 만져보자

작은 카운터 구조체로 두 줄 규칙을 직접 두드려보자.

```rust
struct Counter {
    count: i32,
}

impl Counter {
    fn increment(&mut self) {
        self.count += 1;
    }

    fn value(&self) -> i32 {
        self.count
    }
}

fn main() {
    let mut c = Counter { count: 0 };
    let r1 = &mut c;
    let r2 = &mut c;        // 컴파일 에러
    r1.increment();
    r2.increment();
    println!("{}", c.value());
}
```

컴파일러가 거부한다.

```
error[E0499]: cannot borrow `c` as mutable more than once at a time
 --> src/main.rs:4:14
  |
3 |     let r1 = &mut c;
  |              ------ first mutable borrow occurs here
4 |     let r2 = &mut c;
  |              ^^^^^^ second mutable borrow occurs here
5 |     r1.increment();
  |     -- first borrow later used here
```

두 개의 mutable borrow를 동시에 가지려 했으니 거부된다. 그러면 어떻게 고쳐야 할까? 여기서 NLL(Non-Lexical Lifetimes)이라는, 컴파일러의 한 단계 진화를 만나게 된다.

## NLL — borrow checker가 *덜 까칠해진* 이유

NLL은 Rust 2018 에디션에서 안정화된 기능이다. *Non-Lexical Lifetimes*, "어휘적이지 않은 라이프타임"이라는 다소 어려운 이름이지만, 의미는 단순하다. *borrow가 살아있는 기간을 컴파일러가 더 똑똑하게 판단해준다*는 뜻이다.

NLL 이전에는 borrow가 *변수의 scope 끝까지* 살아있다고 봤다. 그래서 한 번 빌리면 그 변수가 닫히는 `}`까지는 다른 borrow를 못 만들었다. NLL 이후에는 borrow가 *마지막으로 사용되는 지점까지만* 살아있다고 본다. 이 차이가 일상의 답답함을 크게 줄여준다.

위 카운터 코드를 NLL이 풀어주는 패턴으로 다시 써보자.

```rust
fn main() {
    let mut c = Counter { count: 0 };
    {
        let r1 = &mut c;
        r1.increment();
    }   // r1의 borrow는 여기서 끝난다
    {
        let r2 = &mut c;
        r2.increment();
    }
    println!("{}", c.value());
}
```

스코프를 명시적으로 좁혀줬다. `r1`이 끝난 뒤에야 `r2`가 시작되니, 두 mutable borrow가 동시에 살아있지 않다. 그런데 NLL 덕분에 사실 더 짧게 써도 된다.

```rust
fn main() {
    let mut c = Counter { count: 0 };
    let r1 = &mut c;
    r1.increment();
    // r1은 여기서 마지막으로 쓰였으니, 컴파일러는 borrow가 끝났다고 본다
    let r2 = &mut c;
    r2.increment();
    println!("{}", c.value());
}
```

`{ }` 블록 없이도 컴파일이 통과한다. `r1.increment();` 이후 `r1`이 다시 등장하지 않으면, NLL은 그 시점에 `r1`의 borrow가 *살아있지 않다고* 판단한다. 그러니 그 다음 줄의 `&mut c`가 충돌하지 않는다.

NLL이 도입되기 전 Rust(2015 에디션 이전)에서는 이런 코드도 거부됐다. 그래서 빌림과의 싸움이 더 잦았다. 지금 우리가 만나는 borrow checker는 *훨씬 더 친절해진 후* 모습이다. 처음에는 그래도 답답하겠지만, "이건 NLL이 풀어줄 수 있는 패턴인가?"를 한 번 더 생각해보면 의외로 풀리는 경우가 많다.

## reborrow — 빌림을 또 빌리기

함수에 `&mut T`를 넘기는 상황에서 자주 만나는 개념이 reborrow다. 코드부터 보자.

```rust
fn add_one(value: &mut i32) {
    *value += 1;
}

fn add_many(value: &mut i32) {
    add_one(value);   // value를 다시 빌려준다
    add_one(value);
    add_one(value);
}
```

`add_many`는 `&mut i32`를 받았다. 그것을 `add_one`에 넘기는 순간, ownership이 옮겨갈까? `&mut T`도 일종의 값이니 옮겨가는 게 자연스럽다. 그런데 옮겨갔다면 `add_one(value)`를 두 번째로 부를 때 `value`는 *더 이상 사용할 수 없는 moved value*가 되어야 한다. 그런데 위 코드는 멀쩡히 동작한다. 왜?

답이 reborrow다. Rust는 `add_one(value)` 호출 시 `&mut *value`로 *암묵적으로 reborrow*한다. 즉 "내가 가진 mutable borrow에서 잠깐 또 다른 mutable borrow를 만들어 함수에 넘기되, 그 함수 호출이 끝나면 빌림이 회수된다." `add_one`이 리턴하면 그 reborrow는 끝나고, `add_many`의 `value`는 다시 사용 가능해진다. 그 덕분에 두 번째, 세 번째 호출이 자연스럽게 이어진다.

이 reborrow는 *대부분 자동*이라서 우리가 명시적으로 적을 일이 거의 없다. 하지만 컴파일러가 가끔 거부할 때가 있다. 그럴 때 `add_one(&mut *value)`처럼 명시적으로 reborrow를 적어주면 풀리는 경우가 있다는 정도만 머리에 두자.

## 자주 만나는 에러 메시지 사전

처음 한 달 동안 가장 많이 마주치는 borrow 에러 메시지를 정리해두자. 처방까지 한 줄로 묶어서 가져가는 편이 낫다.

**`borrow of moved value: 'x'`**
4장에서 만났던 에러다. `let t = s;`로 ownership이 옮겨간 뒤 `s`를 다시 쓰려 할 때 나온다. 처방: ownership을 정말로 옮겨야 하는지 다시 생각해보자. 옮길 필요가 없으면 `&s`로 빌려주는 편이 낫다. 정말로 옮겨야 한다면 `s.clone()`으로 복제하거나, 호출 후에 `s`를 안 쓰면 된다.

**`cannot borrow 'x' as mutable because it is also borrowed as immutable`**
방금 본 그 에러다. immutable borrow가 살아있는 동안 mutable borrow를 만들 수 없다. 처방: immutable borrow의 사용 범위를 좁혀라(NLL이 풀어준다). 또는 둘을 *순차적으로* 분리하라.

**`cannot borrow 'x' as mutable more than once at a time`**
mutable borrow는 단 하나만 가능하다. 두 개를 동시에 만들려고 했을 때 나온다. 처방: 한쪽이 끝난 뒤 다른 쪽을 시작하라. 또는 *진짜로* 두 군데서 쓸 권한이 필요하다면 자료 구조를 다시 설계하자(8장의 `Rc<RefCell<T>>` 또는 `Arc<Mutex<T>>`).

**`'x' does not live long enough`**
빌림이 가리키는 데이터가 *빌림보다 먼저 사라진다*는 뜻이다. 6장 라이프타임에서 본격적으로 다룰 영역이다. 처방: 빌림의 lifetime을 데이터의 lifetime 안으로 좁히거나, 데이터를 더 오래 살게 만들거나, ownership을 옮기자.

**`cannot move out of borrowed content`**
빌린 것에서 *값을 가져오려* 했을 때 나온다. `&Vec<String>`에서 `String` 하나를 꺼내려고 하면 거부된다. 처방: `clone()`하거나, `vec.iter()`로 빌림으로만 순회하거나, `vec.into_iter()`로 ownership을 *통째로* 가져오자.

이 다섯 가지 패턴이 첫 한 달의 80%를 차지한다. 외우려고 애쓸 필요는 없다. 컴파일러가 매번 손가락으로 짚어준다. 그 손가락을 *동료의 조언*으로 받아들이는 자세, 그게 첫 처방이다. 한국의 한 시니어 개발자가 4년의 경험을 정리하며 쓴 한 줄을 그대로 가져오자. *"익숙해지면 사고가 정리되는 느낌이고, 한 번 작동하면 정말 잘 작동한다."* 빌림 단계의 첫 한 달을 지나면 그 감각이 천천히 손에 묻기 시작한다.

## 이 두 줄의 규칙은 학술적으로 입증됐다

5장의 마지막 한 절이다. 잠시 깊은 곳을 한 번 들여다보자.

지금까지 우리는 "두 줄의 규칙이 데이터 레이스를 끝낸다"고 말했다. 이 주장이 그저 *Rust 커뮤니티의 관행적 자신감*일까, 아니면 *학술적으로도 검증된* 사실일까? 답은 후자다. 그리고 그 사실을 알고 나면 우리가 지금 배우는 두 줄 규칙의 무게가 한 단계 다르게 다가온다.

2018년 POPL(Principles of Programming Languages) 학회에 「RustBelt: Securing the Foundations of the Rust Programming Language」라는 논문이 실렸다. Ralf Jung과 그의 동료들(MPI-SWS)이 *Rust 언어의 type system이 메모리 안전성과 스레드 안전성을 보장한다*는 사실을 *기계 검증된(machine-checked) 형식 증명*으로 보였다. 이는 현실적인 부분집합의 Rust에 대한 *최초의 형식 안전성 증명*이었다. 즉, Rust가 안전하다는 주장이 *경험과 직관*이 아니라 *수학적 증명*에 의해 뒷받침된다.

그 후속 작업으로 같은 그룹은 2020년 POPL에 「Stacked Borrows: An Aliasing Model for Rust」를 발표했다. 이 논문은 `unsafe`를 포함한 코드에서 *borrow의 의미*를 어떻게 정의해야 하는지를 모델링했다. 그리고 2025년 PLDI(Programming Language Design and Implementation)에는 그 후속인 「Tree Borrows」가 실렸다. Stacked Borrows의 한계를 보완해서, 더 많은 실제 코드 패턴이 *모델 안에서 안전하다*고 인정받을 수 있게 해주는 모델이다.

이 세 편의 흐름이 우리에게 주는 메시지는 한 줄이다. *Rust의 두 줄 규칙은 그저 컴파일러 구현자의 직관이 아니다.* 별도의 학계가 *형식적으로 검증된 모델*을 가지고 *언어의 안전성을 증명*해왔고, 그 모델은 unsafe 코드 영역까지 확장되어 검증되고 있다. 우리가 지금 손으로 두드려본 그 두 줄의 규칙은, 그 어떤 다른 언어도 이 정도로 *학술적 토대 위에서* 만들어지지 않았다.

깊이 들어갈 필요는 없다. 학회 논문을 직접 읽지 않아도 된다. 그저 *우리가 배우는 것이 입증된 안전성*이라는 사실을 한 번 짚어두는 것으로 충분하다. 8장 unsafe 절에서 이 한 단락을 한 번 더 회수하게 된다 — *unsafe라도 검증할 수 있는 형태로* 모델이 만들어진 이유가 거기서 명료해진다.

## 함께 해보자

작은 카운터 구조체 하나를 직접 손으로 두드려보자. 다음 두 가지를 차례로 시도해보고 컴파일러의 메시지를 *손가락으로 짚어가며* 읽어보자.

1. 위에서 살펴본 `Counter`에서, 동시에 두 개의 `&mut`을 만들어보자. 컴파일러가 어느 줄에서 거부하는지, 그리고 어떤 노트(note)와 도움말(help)을 함께 보여주는지 적어보자.
2. NLL이 풀어주는 패턴(스코프 좁히기 또는 마지막 사용 지점 이후로 borrow 종료)으로 같은 코드를 고쳐보자. 어떤 변형이 통과하고 어떤 변형이 여전히 거부되는지 한 줄씩 비교해보자.

이 카운터는 9장 `Arc<Mutex<T>>` 절에서 *멀티스레드 안전성*으로 다시 호출된다. 두 줄의 규칙이 단일 스레드에서 어떻게 동시성 안전성으로 번역되는지를, 그때 한 단계 더 깊이 이해하게 된다.

빌림의 두 줄 규칙은 머리로 외우는 게 아니라 손에 묻히는 규칙이다. 처음 한 달은 매일 컴파일러와 짧은 대화를 나누며 살게 된다. 그 대화가 답답하게 느껴질 때, 한 가지만 기억해두자 — *이 규칙은 우리가 지난 20년 동안 런타임에서 잡으려 애쓰던 그 사고들을 컴파일 타임으로 옮겨주는, 학술적으로 검증된 안전망*이다. 그 안전망을 친구로 받아들이는 데까지 4~6개월. 그 시간이 지나면 빌림은 더 이상 적이 아니다.

다음 6장에서는 빌림과 짝을 이루는 *라이프타임*을 다룬다. `'a` 어노테이션이 처음 등장할 때의 그 막막함, 그리고 *사실 우리가 명시적으로 라이프타임을 적는 일은 한 손에 꼽을 정도라는* 안도감을 함께 가져가자.

---

## 참고

- [Rust ownership and borrows: Fighting the borrow-checker — DEV.to](https://dev.to/daaitch/rust-ownership-and-borrows-fighting-the-borrow-checker-4ea3)
- [The Borrow Checker: Rust's Tough-Love Mentor](https://www.woodruff.dev/the-borrow-checker-rusts-tough-love-mentor/)
- [Rust for Java Developers — Ownership](https://tkaitchuck.github.io/Rust4JavaDevelopers/ownership.html)
- Jung, R., Jourdan, J.-H., Krebbers, R., Dreyer, D. — [RustBelt: Securing the Foundations of the Rust Programming Language (POPL 2018)](https://plv.mpi-sws.org/rustbelt/popl18/paper.pdf)
- Jung, R., Dang, H.-H., Kang, J., Dreyer, D. — [Stacked Borrows: An Aliasing Model for Rust (POPL 2020)](https://plv.mpi-sws.org/rustbelt/stacked-borrows/paper.pdf)
- Villani, N., Hostert, J., Dreyer, D., Jung, R. — [Tree Borrows (PLDI 2025)](https://iris-project.org/pdfs/2025-pldi-treeborrows.pdf)
- [Send and Sync — The Rustonomicon](https://doc.rust-lang.org/nomicon/send-and-sync.html)
- [4년간의 Rust 사용 후기 — blog.cro.sh](https://blog.cro.sh/posts/four-years-of-rust/)
