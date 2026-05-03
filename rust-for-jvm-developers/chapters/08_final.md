# 8장. 스마트 포인터·매크로·unsafe 진입 — 메모리 도구와 안전 경계

7장에서 우리는 표현력의 도구상자를 손에 쥐었다. 이제 8장은 그 표현력 아래에 깔린 *메모리 도구상자*를 펼친다. JVM에서 우리는 *모든 객체 참조가 똑같이 생긴* 단일 모델로 일해왔다. 일반 객체 참조도, 멀티스레드 공유도, 가변 상태 보호도, 불변 보장도 — *코드의 모양*은 같았다. 다른 점은 *우리가 어떤 어노테이션을 붙였는지*, *어떤 lock을 들고 있는지*, *컨벤션을 얼마나 잘 지켰는지*였다. Rust는 그걸 정면으로 뒤집었다. *누가 소유하고, 누가 빌리고, 단일 스레드인지 멀티 스레드인지, 컴파일 검증인지 런타임 검증인지*를 *타입으로 명시한다*. 처음에는 부담이지만, 이 챕터를 지나고 나면 *그 명시가 코드에 박혀 있다*는 사실이 6개월 뒤 가장 큰 보상이 된다는 사실을 받아들이게 된다.

그리고 이 챕터의 마지막 한 절은 정직한 한 줄로 시작한다. `unsafe`는 *컴파일러를 끄는* 게 아니다. *책임을 우리에게 옮기는 계약*이다. 두려움을 부추길 일도 아니고, 가볍게 다룰 일도 아니다. 그 경계가 어디까지인지를 한 절 안에 정확히 박아두자.

## 스마트 포인터 — 다섯 도구의 표 한 장

먼저 표 한 장으로 정면을 보자.

| 도구 | 의미 | 단일/멀티 스레드 | 검증 시점 | JVM 대응물 |
|---|---|---|---|---|
| `Box<T>` | 단일 owner, 힙 할당 | 단일 | 컴파일 | 일반 객체 참조 (단독 owner) |
| `Rc<T>` | 단일 스레드 공유 owner, 참조 카운트 | 단일 | 컴파일 + 런타임(refcount) | (구분 없음) |
| `Arc<T>` | 멀티스레드 공유 owner, atomic refcount | 멀티 | 컴파일 + 런타임(atomic) | `AtomicReference` 감각 |
| `RefCell<T>` | 단일 스레드 interior mutability | 단일 | *런타임* borrow check | 일반 객체의 모양 그대로 |
| `Mutex<T>` (보통 `Arc<Mutex<T>>`) | 멀티스레드 공유 + 가변 | 멀티 | 컴파일 + 런타임(lock) | `synchronized` + 필드 |

이 다섯 도구가 Rust 메모리 도구상자의 95%다. 한 도구씩 천천히 짚어가자.

### `Box<T>` — 가장 단순한 시작

`Box<T>`는 *힙에 값을 올리고, 그 값에 대한 단독 소유권을 들고 있는* 박스다. 가장 단순한 스마트 포인터다.

```rust
let boxed: Box<i32> = Box::new(42);
println!("{}", *boxed);   // dereference로 값을 읽는다
```

언제 쓰는가? 두 가지 경우다. 첫째, 값이 *너무 커서 스택에 두기 부담*이거나(예: 큰 구조체), 둘째, *재귀 자료구조*처럼 컴파일 시점에 크기가 결정되지 않을 때.

```rust
// 재귀 자료구조: 자기 자신을 포함하는 List
enum List {
    Cons(i32, Box<List>),
    Nil,
}
```

`Box`로 감싸지 않으면 `List`의 크기를 *컴파일 시점에 결정할 수 없다*. 자기 자신을 포함하니까 무한 재귀다. `Box`로 감싸면 그 자리에는 *포인터 크기*만 들어가니 크기가 정해진다.

JVM 출신은 이런 일을 *한 번도 의식한 적이 없다*. Java에서 모든 객체는 *항상 힙*이고, 객체 참조는 *항상 포인터 크기*다. 그래서 재귀 자료구조도 그냥 `class Node { Node next; }`로 쓴다. 그 *간편함의 비용*이 GC다. Rust는 *언제 힙에 올릴지를 우리가 명시*하는 모델이다.

### `Rc<T>` — 단일 스레드의 공유 소유권

7장의 어느 순간, 우리는 *한 데이터를 여러 군데서 공유 소유*하고 싶을 때가 있었을 것이다. ownership은 한 명만 가지는 게 원칙이지만, 가끔은 그 원칙을 *우회*해야 한다. 그래프 자료구조에서 한 노드를 여러 부모가 가리키거나, 트리 구조에서 자식이 부모를 역참조해야 할 때.

`Rc<T>`는 *Reference Counting*의 약자다. 같은 데이터에 대한 `Rc`를 여러 개 만들 수 있고, *마지막 `Rc`가 drop될 때 데이터가 해제*된다.

```rust
use std::rc::Rc;

let a = Rc::new(String::from("shared"));
let b = Rc::clone(&a);
let c = Rc::clone(&a);

println!("count = {}", Rc::strong_count(&a));   // 3
```

`Rc::clone`은 *데이터를 복제하지 않는다*. *카운트만 1 증가*시킨다. 모든 `Rc`가 같은 데이터를 가리킨다.

여기서 결정적인 한 줄. **`Rc<T>`는 단일 스레드 전용이다.** 다른 스레드로 보내려고 하면 *컴파일 거부*다. 왜? 카운트 증감이 *atomic이 아니라서* 멀티스레드 환경에서는 race condition이 발생할 수 있다. Rust는 그 사실을 *타입 시스템에* 박아놓았다 — `Rc<T>`는 `Send`도 `Sync`도 아니다.

이 사실이 9장에서 다시 호출된다. *왜 컴파일러가 `Rc`를 thread::spawn에 넘기지 못하게 거부하는가*가 9장의 주요 학습 포인트 중 하나다. 5장에서 두 줄 규칙이 데이터 레이스를 컴파일 타임에 끝낸다고 했던 그 약속의 *연장선*이다.

### `Arc<T>` — 멀티스레드의 공유 소유권

`Arc<T>`는 *Atomically Reference Counted*다. `Rc`와 사용법이 같지만, 카운트 증감이 atomic 연산이라서 멀티스레드 환경에서 안전하다.

```rust
use std::sync::Arc;
use std::thread;

let data = Arc::new(vec![1, 2, 3]);

let mut handles = vec![];
for i in 0..3 {
    let data = Arc::clone(&data);
    handles.push(thread::spawn(move || {
        println!("스레드 {i}: {:?}", data);
    }));
}

for h in handles {
    h.join().unwrap();
}
```

세 스레드가 같은 `Vec`을 공유한다. 모든 스레드가 끝나고 마지막 `Arc`가 drop될 때 `Vec`도 해제된다. 이게 가장 흔한 멀티스레드 공유 패턴이다.

JVM에서는 이런 구분이 없었다. 객체를 두 스레드가 공유하면 그저 *같은 참조*를 들고 있을 뿐이다. GC가 reachability를 알아서 추적해서 마지막 참조가 사라질 때 회수한다. Rust는 *atomic 연산의 비용*을 *타입 선택의 결과*로 만들어놓았다 — 단일 스레드면 `Rc`(원자 연산 절감), 멀티스레드면 `Arc`. *우리가 골라야 한다는 부담*이 *그 선택이 코드에 박혀 있다는 보상*과 짝을 이룬다.

### `RefCell<T>` — interior mutability, 컴파일 검증을 *포기*하는 도구

여기서 잠깐 멈추자. 지금까지 우리가 본 모든 가변 borrow는 *컴파일 타임에* 검증됐다. `&mut T`가 단 하나만, 그리고 다른 borrow와 공존 못 한다는 두 줄 규칙. 그런데 가끔 *컴파일러가 그 검증을 못 하는 패턴*이 있다. 예를 들어 캐시처럼, *외부에서 보면 불변이지만 내부적으로 mutable한 상태를 들고 있어야* 하는 경우.

```rust
struct Cache {
    storage: HashMap<String, String>,
}

impl Cache {
    // get은 외부에서 보면 불변(&self)인데, 내부적으로 storage를 수정하고 싶다
    fn get(&self, key: &str) -> Option<String> {
        // self.storage.insert(...) — 컴파일 에러: cannot borrow as mutable
    }
}
```

이런 경우에 `RefCell<T>`가 나선다. **`RefCell`은 컴파일 타임 borrow 검증을 *포기*하고 *런타임으로 미루는* 도구다.**

```rust
use std::cell::RefCell;
use std::collections::HashMap;

struct Cache {
    storage: RefCell<HashMap<String, String>>,
}

impl Cache {
    fn get(&self, key: &str) -> Option<String> {
        let storage = self.storage.borrow();   // 런타임 borrow check
        storage.get(key).cloned()
    }

    fn set(&self, key: String, value: String) {
        let mut storage = self.storage.borrow_mut();   // 런타임 borrow check
        storage.insert(key, value);
    }
}
```

`borrow()`는 immutable borrow를, `borrow_mut()`은 mutable borrow를 *런타임에* 가져온다. 두 줄 규칙은 그대로 유효하다 — *런타임에 검사*된다는 차이만 있다. 이 규칙이 위반되면? *panic*이 발생한다. 즉 5장의 컴파일 에러가 *런타임 panic*으로 옮겨오는 것이다.

이게 실수로 잘못 쓰면 *큰 사고*가 된다. 컴파일은 통과하는데 운영에서 panic이 터지는 패턴이다. 그래서 *꼭 필요할 때만 쓰자*. 가능하면 다시 설계해서 `&mut self`로 풀어내는 편이 낫다.

JVM 출신에게 `RefCell`은 사실 *Java의 일반 객체와 가장 닮은* 모양이다. Java 객체는 항상 *interior mutable*이다. `final List<String> list`라고 적어도 `list.add(...)`가 동작한다. 즉 *Java는 `RefCell`이 디폴트인 세계*다. Rust는 그걸 *명시적인 도구로 따로 분리*해서, 우리가 *진짜로 그 모델이 필요할 때만* 의도적으로 선택하게 만든다.

### `Mutex<T>` — `Arc<Mutex<T>>`라는 이름의 표준형

마지막 도구. 멀티스레드 환경에서 *공유 가변* 상태가 필요할 때.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));

let mut handles = vec![];
for _ in 0..10 {
    let counter = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    }));
}

for h in handles {
    h.join().unwrap();
}

println!("{}", *counter.lock().unwrap());   // 10
```

`Mutex<T>`는 *내부 데이터에 접근하려면 lock을 잡아야* 하는 도구다. `lock()`이 `Result<MutexGuard<T>>`를 반환하고, `MutexGuard`가 *RAII 패턴으로 lock을 들고 있다가, drop될 때 자동으로 lock을 푼다*. Java의 `synchronized` 블록이 *블록 경계*에서 lock을 푸는 것과 비교하면, Rust의 `MutexGuard`는 *변수의 scope 경계*에서 푼다. 이 두 모델이 결정적으로 다르다 — Java는 *예외가 발생해도 lock이 풀리지만 try-finally 패턴이 시각적으로 명시되어야 안전했던* 반면, Rust는 *어떤 경로든 scope를 벗어나면 자동으로 풀린다*. lock을 안 풀고 return하는 사고가 *구조적으로 불가능*하다.

`Arc<Mutex<T>>`는 *공유 가변 상태의 표준 표현형*이다. `Arc`로 *공유*를, `Mutex`로 *가변*을 분리해서 표현한 것이다. 처음 보면 두 단계 wrap이 부담스럽지만, *그 둘이 분리되어 있어야 의미가 명료하다*는 사실을 깨닫게 된다. 어떤 자료는 *공유는 하지만 불변*(`Arc<T>`만)이고, 어떤 자료는 *가변이지만 단일 스레드*(`RefCell<T>`)고, 어떤 자료는 *공유 가변*(`Arc<Mutex<T>>`)이다 — 그 셋이 *서로 다른 타입*으로 명시된다.

5장의 카운터 예제를 떠올려보자. 단일 스레드에서 `&mut Counter`로 한 명만 가변 borrow를 들고 있던 그 카운터를, 이제 멀티스레드로 옮기려면 `Arc<Mutex<Counter>>`로 감싸야 한다. 5장에서 약속한 *"이 카운터는 9장 `Arc<Mutex<T>>` 절에서 멀티스레드 안전성으로 다시 호출된다"*는 다리가 8장에서 *도구의 모양*으로 한 번 미리 펼쳐진 셈이다.

## 도구 선택의 의사결정 트리

다섯 도구를 어떤 기준으로 고를까? 한 단락의 의사결정 트리로 정리해보자.

1. *공유가 필요한가?* 아니면 → `Box<T>` 또는 그냥 owned 값.
2. 공유가 필요하면, *멀티스레드인가?* 아니면 → `Rc<T>`.
3. 멀티스레드면 → `Arc<T>`.
4. 거기에 *가변이 필요한가?* 아니면 → 위에서 결정한 그대로.
5. 가변이 필요하고 단일 스레드면 → `Rc<RefCell<T>>` 또는 `RefCell<T>`.
6. 가변이 필요하고 멀티 스레드면 → `Arc<Mutex<T>>` (또는 `Arc<RwLock<T>>`).

이 의사결정 트리를 한 번 손에 두면, 새 자료구조를 설계할 때 *어떤 wrap이 어울리는지*가 자연스럽게 떠오른다. 처음에는 매번 의사결정 트리를 펼쳐야 하지만, 한 달쯤 지나면 *반사적으로* 결정된다.

JVM에서 같은 의사결정을 떠올려보자. Java로 하면 어떻게 될까? *모든 자료가 `Arc<RefCell<T>>` 또는 `Arc<Mutex<T>>` 모드*다 — *항상* 공유 가능하고 *항상* 가변이고, 안전성은 우리가 *코드 리뷰와 컨벤션*으로 보장한다. Rust는 그 모든 결정을 *타입으로 강제*한다. 그게 명시성의 비용과 보상이다.

## 매크로 첫 만남 — Lombok과의 거리

7장에서 우리는 thiserror에서 `#[derive(Error)]`를 만났다. 여기까지 오면서 매번 한 번씩 봤을 매크로가 8장에서 정면으로 등장한다.

Rust 매크로는 두 종류다. **declarative macro**(`macro_rules!`)와 **procedural macro**(`proc_macro`).

declarative macro는 *패턴 매칭으로 코드를 펼치는* 도구다.

```rust
// 가장 흔한 declarative macro: vec!
let v = vec![1, 2, 3];
// 위는 다음으로 펼쳐진다
let v = {
    let mut temp = Vec::new();
    temp.push(1);
    temp.push(2);
    temp.push(3);
    temp
};
```

`vec![]`라는 한 줄이 다섯 줄로 펼쳐졌다. `macro_rules!`로 새 매크로를 정의하는 일도 가능하지만, 입문 단계에서는 *기존 매크로를 잘 쓰는 것*이 우선이다. 직접 만드는 건 13장의 *내 매크로 만들기* 절에서 다룬다.

procedural macro는 더 강력하다. `#[derive(...)]`, `#[tokio::main]`, `#[sqlx::query!]` 같은 게 모두 procedural macro다. 토큰을 받아 *임의의 코드를 생성*해서 펼친다.

JVM의 Lombok과 비교하면 결정적인 차이가 두 가지 있다.

첫째, **Rust 매크로는 토큰을 진짜로 펼쳐서 컴파일러가 다시 검사한다.** Lombok은 *바이트코드 단계에서* 메서드를 추가하는 식이라, IDE가 보지 못하면 *마법처럼 메서드가 생기지만 코드에는 안 보이는* 거리감이 생긴다. Rust는 펼친 결과가 *진짜 Rust 코드*고, `cargo expand`로 그 결과를 *눈으로 볼 수 있다*.

```bash
cargo install cargo-expand
cargo expand
```

이 명령이 매크로가 펼쳐진 *완성된 Rust 코드*를 출력한다. `#[derive(Debug)]`가 어떤 메서드를 만들어내는지, `#[tokio::main]`이 main 함수를 어떻게 wrap하는지를 *눈으로 확인*할 수 있다.

둘째, **Rust 매크로는 컴파일 타임에 동작하므로 런타임 reflection이 필요 없다.** Lombok이 추가한 메서드는 reflection 없이도 호출되지만, Spring의 `@Autowired`나 `@Transactional` 같은 어노테이션은 *런타임 proxy*로 동작한다. 그래서 그 메커니즘을 디버깅하기가 까다롭다. Rust는 *모든 것이 컴파일 타임 코드 생성*이라, 디버거로 펼친 결과를 *그대로 따라갈 수 있다*.

## `unsafe` — 정직한 한 절

이제 8장의 가장 중요한 한 절이다. `unsafe`라는 키워드는 Rust를 둘러싼 가장 큰 오해의 출발점이기도 하다. 첫 줄부터 정직하게 박아두자.

**`unsafe`는 컴파일러를 끄는 게 아니다. 책임을 우리에게 옮기는 계약이다.**

이 한 줄이 8장의 가장 중요한 메시지다. unsafe 블록 안에서도 *대부분의 컴파일러 검사는 그대로 동작한다*. 타입 검사, borrow checker, lifetime 검사 모두 평소처럼 작동한다. 다만 `unsafe`가 우리에게 *추가로 허용해주는 다섯 가지*가 있다. 그게 끝이다.

### unsafe가 허용하는 다섯 가지 — 정확히 이것뿐

1. **raw pointer를 dereference하는 것** (`*const T`, `*mut T`).
2. **mutable static 변수에 접근하는 것** (`static mut`).
3. **다른 unsafe 함수를 호출하는 것**.
4. **unsafe trait을 구현하는 것** (`Send`, `Sync` 같은).
5. **union의 필드에 접근하는 것**.

이게 전부다. *모든 것을 풀어주는* 게 아니다. *이 다섯 가지*에 대해서만 컴파일러가 *우리에게 검증을 위임*한다.

```rust
fn main() {
    let x = 5;
    let raw_ptr = &x as *const i32;

    // 컴파일 에러: dereference of raw pointer is unsafe
    // println!("{}", *raw_ptr);

    // unsafe 블록 안에서만 허용
    unsafe {
        println!("{}", *raw_ptr);   // OK
    }
}
```

`*raw_ptr`이 *raw pointer dereference*에 해당하므로 unsafe가 필요하다. 하지만 *그 안에서도* 다른 검사는 다 동작한다. `let mut s = String::new(); unsafe { let r = &s; let r2 = &mut s; }`처럼 빌림 규칙을 위반하면? *unsafe 블록 안이라도 컴파일 에러*다.

### unsafe를 *언제 써야* 하는가

5가지 경우 중 일상에서 마주치는 건 두 가지다.

**FFI 호출.** C 라이브러리나 OS API를 부를 때. 14장 FFI(JNI/Panama/C ABI) 챕터에서 본격적으로 다룬다. C 함수의 시그니처는 Rust가 모르니, 우리가 *불변 조건을 보증*해야 한다.

```rust
extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    let result = unsafe { abs(-42) };
    println!("{result}");
}
```

**low-level 자료구조의 안전 추상화 안에서.** 이게 더 흥미롭다. 표준 라이브러리의 `Vec`, `String`, `Box`, `Rc`, `Arc`, `Mutex` — *모두 내부에 unsafe 코드가 있다*. 왜? 안전한 추상화만으로 표현할 수 없는 메모리 조작이 필요하기 때문이다. 예를 들어 `Vec::push`는 *capacity가 부족하면 새 메모리를 alloc하고 기존 데이터를 복사*한다. 이 일은 안전한 Rust로 표현할 수 없다. 그래서 `Vec` 내부에 unsafe 블록이 들어간다.

이게 Rust 표준 라이브러리의 핵심 설계 패턴이다. **safe API를 unsafe 위에 얹는다.** `Vec`을 *사용하는* 코드는 unsafe가 필요 없다. `Vec::push`, `Vec::get`, `Vec::iter()`는 모두 safe API다. 그 내부에서 *unsafe로 메모리를 조작하되, 그 unsafe 블록의 invariant를 라이브러리 작성자가 보증*한다. 그 보증된 추상화 위에서 *우리는 안전하게* 살 수 있다.

### unsafe를 *언제 쓰지 말아야* 하는가

이게 더 중요하다. 한 줄로 박아두자. **borrow checker를 우회하려고 unsafe를 쓰면 안 된다.** 99%의 경우, *더 나은 안전 코드로 재설계가 가능하다*.

처음 한 달의 답답함 속에서 우리는 가끔 이런 충동을 느낀다. *"이 코드가 컴파일이 안 되니까, 그냥 unsafe로 둘러싸자."* 이건 거의 항상 잘못된 선택이다. 두 가지 이유가 있다.

첫째, 그 unsafe가 *진짜로 안전한지 검증할 도구가 없다*. borrow checker가 안 잡아주면, 잘못된 메모리 접근이 *조용히 통과*해서 운영에서 *알 수 없는 사고*로 터진다. C에서 우리가 살아온 세계로 돌아가는 거다.

둘째, *안전한 재설계가 거의 항상 가능*하다. 보통 답은 `Rc<RefCell<T>>`, `Arc<Mutex<T>>`, 채널, 또는 *데이터 모델 자체를 다시 그리기*에 있다. 처음에는 그 재설계가 어려워 보이지만, 한 번 익숙해지면 *unsafe로 도망가는 일이 거의 없어진다*.

### Stacked Borrows · Tree Borrows — unsafe 영역의 학술적 검증

5장에서 박아두었던 RustBelt 한 단락을 한 번 더 회수하자. **`unsafe` 코드의 borrow 의미를 어떻게 정의해야 안전한지**를, 학계가 별도로 모델링해왔다는 사실이다.

2020년 POPL에 발표된 「Stacked Borrows」(Jung, Dang, Kang, Dreyer)는 *unsafe 코드 안에서 raw pointer와 reference가 혼재할 때*의 안전성 모델을 제시했다. 그 후속인 「Tree Borrows」(2025 PLDI)는 그 모델의 한계를 보완해서 *더 많은 실제 unsafe 패턴이 모델 안에서 인정받을 수 있게* 했다. Miri라는 도구가 이 모델을 구현해서, *우리가 짠 unsafe 코드가 모델을 위반하는지를 자동으로 검사*해준다.

```bash
cargo +nightly miri test
```

이 한 줄이, unsafe를 포함한 우리 코드를 *형식 모델 안에서 검증*해준다. unsafe를 정말로 써야 하는 자리(예: low-level 자료구조 작성)에서는, Miri로 검증하는 습관이 *최소한의 안전망*이다.

학술 인용 한 줄을 더해보자. Cui 외의 「Is unsafe an Achilles' Heel?」(arXiv:2308.04785)는 실무에서 unsafe가 *잘못 쓰이는 패턴 5가지*를 분류했다. 핵심은 *대부분의 unsafe 사고가 안전 추상화의 invariant를 깨는 데서 온다*는 것이다. 즉 라이브러리 작성자가 *내가 만든 safe API의 사용자가 어떤 invariant를 가정해도 되는지*를 정확히 정의하고, unsafe 블록 안에서 그 invariant를 보장해야 한다.

deepSURF (IEEE S&P 2026, arXiv:2506.15648)는 *unsafe 영역의 메모리 사고를 자동으로 탐지하는 도구*다. 이런 학계의 노력이 한 방향을 가리킨다 — *unsafe를 두려워할 필요는 없다, 다만 정직하게 다뤄야 한다*.

### 안전 경계의 역할 — 마지막 한 단락

이제 8장의 마지막 한 단락이다. `unsafe`라는 도구가 Rust의 안전성에 어떤 위치를 차지하는지를 한 번 더 명료하게 박아두자.

Rust의 안전성 모델은 다음과 같이 *단계적*이다. *대부분의 코드*는 safe Rust로 짠다 — borrow checker가 모든 것을 검증한다. *드물게* unsafe가 필요한 자리(저수준 자료구조, FFI)에서는, *그 unsafe 블록을 safe API로 wrap*해서 외부에 안전한 인터페이스만 노출한다. 사용자는 그 safe API만 본다. 안전하다.

이 모델이 무너지는 건 *unsafe의 invariant를 깨는 코드*가 들어왔을 때다. 라이브러리 작성자가 보증하기로 한 invariant를 사용자가 *우회해서 깨면*, 그게 운영 사고로 이어진다. 그래서 unsafe를 포함한 라이브러리 작성자는 *문서에 invariant를 정확히 적고*, *그것을 깰 수 있는 사용 패턴을 차단*해야 한다.

JVM에서는 이런 모델이 다르게 펼쳐졌다. *모든 것이 안전한 Java*가 있고, *unsafe는 JNI 너머의 C/C++ 세계*다. 두 세계의 경계가 *명확하게 분리*되어 있다. Rust는 그 두 세계가 *같은 언어 안에 있되, 명시적인 키워드로 경계가 그어져 있다*. unsafe가 *진짜로 필요한 자리*에서만 *국소적으로 허용*되고, 그 외 모든 곳에서는 안전성이 *기본*이다.

그리고 한 가지 더 — *15장 JNI/Panama/C ABI는 unsafe의 가장 큰 사용처다*. 거기서 우리는 *Java 객체와 Rust 데이터를 잇는 경계*에서 어떤 invariant를 보증해야 하는지를 정면으로 다룬다. 그때 8장의 이 절을 다시 펼쳐 읽게 될 것이다.

## 함께 해보자

8장의 도구 다섯을 한 자리에서 손으로 만져보자. 작은 트리 구조를 만들어 한 노드의 값을 바꾸는 연습이다.

```rust
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
struct Node {
    value: i32,
    children: Vec<Rc<RefCell<Node>>>,
}

fn main() {
    let leaf1 = Rc::new(RefCell::new(Node { value: 1, children: vec![] }));
    let leaf2 = Rc::new(RefCell::new(Node { value: 2, children: vec![] }));
    let root = Rc::new(RefCell::new(Node {
        value: 0,
        children: vec![Rc::clone(&leaf1), Rc::clone(&leaf2)],
    }));

    // leaf1의 값을 바꿔보자
    leaf1.borrow_mut().value = 100;

    // root에서 leaf1을 봐도 100으로 바뀌어 있다 (공유되니까)
    println!("{:?}", root);
}
```

이 코드를 직접 두드려보고, 다음 두 가지를 손으로 시도해보자.

1. `Rc::clone(&leaf1)`이 *데이터를 복제하지 않고 카운트만 늘린다*는 사실을, `Rc::strong_count(&leaf1)`을 출력해 확인해보자. root를 만들기 전후로 카운트가 어떻게 변하는지.
2. `leaf1.borrow_mut()`을 두 번 동시에 들고 있으려고 시도해보자. *컴파일은 통과하지만 런타임 panic*이 발생한다. 이게 `RefCell`의 *런타임 borrow check*가 동작하는 모양이다. 5장의 컴파일 에러가 *런타임으로 옮겨진* 사례를 직접 보면 *왜 가능하면 컴파일 검증으로 풀어내야 하는지*가 손에 묻는다.

그다음, `cargo expand`로 `#[derive(Debug)]`가 무슨 코드를 만들어내는지 펼쳐보자. *마법이 사라진다*. 펼쳐진 코드가 그저 *우리가 손으로 적을 수 있는 Rust 코드*일 뿐이라는 사실을 눈으로 보면, 매크로가 더 이상 *블랙박스*가 아니다.

이 `Rc<RefCell<T>>` 패턴은 9장에서 *Send 위반으로 컴파일이 거부되는* 사례로 다시 호출된다. *왜 이걸 thread::spawn에 못 넘기는지*가 거기서 명료해진다. 그리고 unsafe는 15장 JNI 함수 시그니처에서 다시 호출된다. *Java 객체와 Rust 데이터의 경계*에서 어떤 invariant를 보증해야 하는지를, 그때 정면으로 다룬다.

8장이 Part 2의 마지막 챕터다. 4·5·6·7·8장을 묶어, 우리는 *컴파일러와 친구가 되는 길*을 절반 이상 걸어왔다. 소유권으로 시작해서 빌림으로 데이터 레이스를 끝내고, 라이프타임으로 메모리 lifetime을 사고하는 법을 배우고, 트레잇·제네릭·match·`Result`로 표현력의 도구상자를 손에 쥐고, 마지막으로 스마트 포인터·매크로·unsafe로 메모리 도구의 전 영역을 펼쳐봤다. 이제 손에 든 것이 *Rust의 마음*이다.

다음 9장에서는 그 도구들을 들고 *동시성*의 세계로 들어간다. 5장의 두 줄 규칙이 *멀티스레드 안전성*으로 어떻게 보상받는지, 그리고 `Send`와 `Sync`라는 마커 트레잇이 *왜 8장의 `Rc`를 thread::spawn에 못 넘기게 만드는지*를 정면으로 다룬다. *"이제 Spring으로 짜던 그 서비스가 Rust로 보인다"*는 자신감이 본격적으로 손에 묻기 시작하는 챕터다.

---

## 참고

- [Smart Pointers Demystified — DEV.to](https://dev.to/sgchris/smart-pointers-demystified-box-rc-and-refcell-27k)
- [Mastering Safe Pointers in Rust — Technorely](https://technorely.com/insights/mastering-safe-pointers-in-rust-a-deep-dive-into-box-rc-and-arc)
- [The Drop Trait as Finalizer — Medium](https://medium.com/@bugsybits/the-drop-trait-as-finalizer-rusts-hidden-destructor-pattern-d7d38798d6ac)
- [Procedural macros in Rust — LogRocket](https://blog.logrocket.com/procedural-macros-in-rust/)
- [Macros — The Rust Book](https://doc.rust-lang.org/book/ch19-06-macros.html)
- [Send and Sync — The Rustonomicon](https://doc.rust-lang.org/nomicon/send-and-sync.html)
- Jung, R., Dang, H.-H., Kang, J., Dreyer, D. — [Stacked Borrows: An Aliasing Model for Rust (POPL 2020)](https://plv.mpi-sws.org/rustbelt/stacked-borrows/paper.pdf)
- Villani, N., Hostert, J., Dreyer, D., Jung, R. — [Tree Borrows (PLDI 2025)](https://iris-project.org/pdfs/2025-pldi-treeborrows.pdf)
- Cui, M. et al. — [Is unsafe an Achilles' Heel? A Comprehensive Study of Safety Requirements in Unsafe Rust Programming (arXiv:2308.04785)](https://arxiv.org/abs/2308.04785)
- [deepSURF: Detecting Memory Safety Vulnerabilities in Rust (IEEE S&P 2026, arXiv:2506.15648)](https://arxiv.org/html/2506.15648v2)
