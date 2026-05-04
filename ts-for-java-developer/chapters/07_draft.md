# 7장. 비동기 모델 — Promise·async/await·Observable·AsyncIterator

Spring WebFlux로 `Mono<ResponseEntity<UserDto>>`를 체이닝하던 손이, 처음으로 TypeScript 코드를 열었다고 해보자. 눈에 들어오는 건 이런 코드다.

```typescript
fetchUser(id)
  .then(user => enrichProfile(user))
  .then(profile => sendEmail(profile))
  .catch(err => logger.error(err));
```

*"아, 이건 Mono랑 비슷하네."* 직감이 빠른 사람이라면 바로 느낀다. `.then()`이 `.map()`처럼 보이고, `.catch()`가 `.onErrorResume()`처럼 읽힌다. 그 감각은 절반쯤 맞다. 하지만 절반쯤 틀리기도 하다. Mono는 구독(subscribe)하기 전에는 아무것도 실행하지 않는다. 반면 Promise는 만들어지는 순간 바로 실행이 시작된다. Mono에서 에러가 흘러내려가지 않으면 체인이 조용히 멈춘다. Promise에서 에러를 받지 않으면 프로세스 전체가 죽을 수도 있다.

이 장은 Java와 Kotlin의 비동기 모델을 알고 있는 사람이 TypeScript의 비동기 세계에 정확히 착지할 수 있도록 돕는 장이다. 이벤트 루프에서 시작해 Promise의 세 상태, async/await의 본질, 에러가 사라지는 이유, AbortSignal로 취소하는 방법, RxJS Observable, AsyncIterator, 그리고 병렬 패턴까지 차례로 살펴보자. 코드를 읽고 짜는 것뿐만 아니라, 예외가 어디로 갔는지 정확히 추적할 수 있는 수준에 도달하는 것이 목표다.

---

## 이벤트 루프 복습 — "단일 스레드인데 어떻게 비동기를 돌리는가"

2장에서 이벤트 루프의 기본 구조를 다뤘다. 여기서는 Promise와 직접 연관된 부분을 다시 꺼내 보자. 바로 *마이크로태스크 큐(microtask queue)*다.

Java/JVM 세계에서 비동기는 보통 스레드를 더 만드는 방식으로 이뤄진다. `ExecutorService`가 스레드 풀을 관리하고, `CompletableFuture`가 그 스레드 위에서 작업을 예약한다. 스레드는 OS 레벨 자원이고, 블로킹이 일어나면 해당 스레드가 잠들었다가 깨어난다. Reactor의 경우는 전용 스케줄러(`Schedulers.boundedElastic()`)를 두어 논블로킹 IO 결과를 특정 스레드로 라우팅한다.

JavaScript는 다르다. 메인 실행 스레드는 하나뿐이다. 그 하나의 스레드가 *이벤트 루프*라는 메커니즘으로 비동기를 처리한다.

```
┌─────────────────────────────────────────────────────┐
│                   이벤트 루프                        │
│                                                      │
│  ┌──────────────────┐   ┌────────────────────────┐  │
│  │  Call Stack      │   │  Web APIs / Node APIs  │  │
│  │  (실행 중인 코드) │   │  (타이머, IO, 네트워크) │  │
│  └──────────────────┘   └────────────────────────┘  │
│           ↑                         │                │
│           │                         ▼                │
│  ┌──────────────────┐   ┌────────────────────────┐  │
│  │  Microtask Queue │ ← │  Macrotask Queue        │  │
│  │  (Promise, queueMicrotask) │  (setTimeout, setInterval, IO) │  │
│  └──────────────────┘   └────────────────────────┘  │
│   콜 스택이 비면 즉시 소진  콜 스택 + 마이크로태스크 후 처리  │
└─────────────────────────────────────────────────────┘
```

이벤트 루프의 동작 순서는 이렇다.

1. **콜 스택이 비어 있는지 확인한다.**
2. **마이크로태스크 큐를 전부 소진한다.** 마이크로태스크 안에서 새 마이크로태스크가 생겨도 그것까지 전부 처리한다.
3. 그 다음에야 **매크로태스크 큐에서 하나**를 꺼내 실행한다.
4. 다시 1로.

Promise가 *마이크로태스크*로 분류된다는 점이 핵심이다. 즉, `setTimeout(fn, 0)`보다 Promise의 `.then()` 콜백이 *먼저* 실행된다.

```typescript
console.log("1: 동기");

setTimeout(() => console.log("4: 매크로태스크"), 0);

Promise.resolve().then(() => console.log("2: 마이크로태스크 첫 번째"));
Promise.resolve().then(() => console.log("3: 마이크로태스크 두 번째"));

console.log("1.5: 동기 계속");

// 출력 순서:
// 1: 동기
// 1.5: 동기 계속
// 2: 마이크로태스크 첫 번째
// 3: 마이크로태스크 두 번째
// 4: 매크로태스크
```

`setTimeout(fn, 0)`이 *"즉시 실행"*처럼 보이지만, 실제로는 마이크로태스크가 전부 빠진 다음에야 실행된다. 이 순서를 이해하지 못하면, 나중에 비동기 코드의 실행 순서가 직관과 다를 때 원인을 찾기 어렵다.

> ### 📚 Java/Kotlin 시선 박스 ④ — `ExecutorService` ↔ 이벤트 루프
>
> | Java `ExecutorService` | JavaScript 이벤트 루프 |
> |---|---|
> | 스레드 풀 기반 | 단일 스레드 기반 |
> | `submit(task)` → 스레드 하나를 점유 | 콜백 → 큐에 등록, 스레드 반환 |
> | 블로킹 IO → 스레드 대기 | 블로킹 IO 없음 (Node.js libuv가 OS에 위임) |
> | 병렬성 = 스레드 수 | 병렬성 = IO 대기 중 다른 태스크 처리 |
> | 오류 → `Future.get()`에서 `ExecutionException` | 오류 → Promise rejection으로 전달 |
>
> Java에서 비동기를 늘리려면 스레드를 더 만든다. Node.js에서 처리량을 늘리려면 *IO를 비동기로 만들고 CPU를 붙잡지 않는다*. CPU 집약적인 작업을 이벤트 루프에서 돌리면 다른 모든 요청이 기다린다 — 이것이 Node.js에서 `worker_threads`나 `cluster`를 쓰는 이유다.
>
> Reactor의 `Schedulers.boundedElastic()`이 IO 스레드 풀을 관리하는 것과, Node.js의 libuv가 OS 비동기 IO를 관리하는 것은 *결과적으로 비슷한 문제를 다른 방식으로 푸는 것*이다. 다만 Node.js는 그 추상화가 언어/런타임 수준에 내장되어 있다.

마이크로태스크 큐가 Promise를 어떻게 굴리는지 이해했으니, 이제 Promise 그 자체를 살펴보자.

---

## Promise — 단일 값을 위한 비동기 컨테이너

### Promise의 세 상태

Promise는 항상 세 상태 중 하나에 있다.

- **Pending(대기)**: 아직 결과가 없다. 초기 상태.
- **Fulfilled(이행)**: 성공적으로 완료되었다. 결과 값을 가진다.
- **Rejected(거부)**: 실패했다. 에러 이유를 가진다.

한 번 Fulfilled 또는 Rejected가 된 Promise는 *다시 상태가 바뀌지 않는다.* 이것을 *settled(정착)* 상태라고 부른다.

```typescript
// Fulfilled Promise 직접 만들기
const fulfilled = Promise.resolve(42);

// Rejected Promise 직접 만들기
const rejected = Promise.reject(new Error("무언가 잘못됨"));

// 직접 제어하기
const manual = new Promise<number>((resolve, reject) => {
  setTimeout(() => {
    const success = Math.random() > 0.5;
    if (success) {
      resolve(100);
    } else {
      reject(new Error("운이 나빴다"));
    }
  }, 1000);
});
```

> ### 📚 Java/Kotlin 시선 박스 ① — `CompletableFuture` ↔ Promise
>
> | Java `CompletableFuture<T>` | TypeScript `Promise<T>` |
> |---|---|
> | `CompletableFuture.completedFuture(v)` | `Promise.resolve(v)` |
> | `CompletableFuture.failedFuture(ex)` | `Promise.reject(err)` |
> | `new CompletableFuture<>()` + `complete(v)` | `new Promise((resolve, reject) => ...)` |
> | `.thenApply(fn)` | `.then(fn)` |
> | `.thenCompose(fn)` | `.then(fn)` (flatMap에 해당) |
> | `.exceptionally(fn)` | `.catch(fn)` |
> | `.handle(fn)` | `.then(ok => ..., err => ...)` 또는 `.finally(fn)` |
> | `future.get()` — 블로킹! | `await promise` — 논블로킹 (이벤트 루프를 양보) |
> | `future.join()` — 블로킹! | `await promise` |
>
> **가장 중요한 차이**: `CompletableFuture`는 `get()`/`join()` 호출 전까지 결과를 *꺼내지 않는다*. 하지만 Promise에서 `await`는 스레드를 블로킹하지 않는다. 이벤트 루프에 제어를 돌려주고, 결과가 준비되면 그 자리부터 다시 실행한다.
>
> **또 하나의 차이**: `CompletableFuture`는 명시적으로 실행기(`Executor`)를 지정하지 않으면 ForkJoinPool을 사용한다. Promise는 항상 이벤트 루프 위에서 마이크로태스크로 실행된다. "어느 스레드"라는 개념 자체가 없다.

### then/catch/finally 체이닝

Promise의 체이닝은 *각 단계가 새 Promise를 반환한다*는 원칙 위에 선다.

```typescript
fetch("https://api.example.com/users/1")
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();  // 이것도 Promise를 반환한다
  })
  .then(user => {
    console.log("사용자:", user.name);
    return user;
  })
  .catch(err => {
    console.error("에러 발생:", err.message);
    // catch도 값을 반환하면 체인이 이어진다
    return null;
  })
  .finally(() => {
    console.log("요청 완료 — 성공이든 실패든");
    // finally는 값을 반환해도 체인에 영향을 주지 않는다
  });
```

`.then(onFulfilled, onRejected)`처럼 두 번째 인자를 쓸 수도 있지만, `.catch(onRejected)`를 따로 쓰는 편이 읽기 훨씬 낫다. 두 인자 형태는 이전 단계의 에러만 잡고, 같은 `.then()` 안의 `onFulfilled`에서 발생한 에러는 잡지 못하기 때문에 더 안전하지도 않다.

한 가지 짚어두어야 할 점이 있다. `.then()` 안에서 *값을 반환하는 것*과 *Promise를 반환하는 것*은 체이닝에서 다르게 동작하지 않는다. 값을 반환하면 자동으로 `Promise.resolve(값)`으로 감싸진다. 이것이 바로 `.thenCompose()`를 따로 둔 Java와의 결정적인 차이다.

```typescript
// 이 두 코드는 체이닝에서 동일하게 동작한다
promise
  .then(v => v + 1)          // 숫자를 반환 → Promise<number>로 자동 래핑
  .then(v => Promise.resolve(v + 1));  // Promise를 반환 → 그대로 사용
```

> ### 📚 Java/Kotlin 시선 박스 ② — Reactor `Mono`/`Flux` ↔ Promise/Observable
>
> | Reactor `Mono<T>` | TypeScript `Promise<T>` |
> |---|---|
> | `Mono.just(v)` | `Promise.resolve(v)` |
> | `Mono.error(ex)` | `Promise.reject(err)` |
> | `.map(fn)` | `.then(fn)` (동기 변환) |
> | `.flatMap(fn)` | `.then(fn)` (비동기 변환, fn이 Promise 반환) |
> | `.onErrorResume(fn)` | `.catch(fn)` |
> | `.doFinally(fn)` | `.finally(fn)` |
> | `.subscribe()` — **구독해야 실행** | Promise는 **생성 즉시 실행** |
>
> **가장 큰 차이**: Reactor는 *콜드 스트림(cold stream)* 기반이다. `Mono`를 만들어도 `.subscribe()`하지 않으면 아무것도 실행되지 않는다. Promise는 생성자(`new Promise(executor)`)가 호출되는 순간 executor 함수가 *즉시* 실행된다. 이미 실행이 시작된 비동기 작업을 나타내는 것이다.
>
> ```typescript
> // Promise는 new 하는 순간 콘솔에 출력된다
> const p = new Promise(resolve => {
>   console.log("지금 바로 실행!");  // subscribe 없이도 출력됨
>   resolve(42);
> });
> ```
>
> Reactor로 오래 일한 사람에게 이 차이는 처음에 꽤 난감하다. "왜 이미 실행이 됐지?"라는 순간이 온다. `Promise.resolve(값)`은 이미 Fulfilled된 Promise를 반환하는 팩토리일 뿐이고, `new Promise(executor)`는 executor를 *즉시* 호출한다는 점을 기억해두자.
>
> | Reactor `Flux<T>` | RxJS `Observable<T>` |
> |---|---|
> | `Flux.just(1, 2, 3)` | `of(1, 2, 3)` |
> | `Flux.fromIterable(list)` | `from(list)` |
> | `.map(fn)` | `.pipe(map(fn))` |
> | `.filter(fn)` | `.pipe(filter(fn))` |
> | `.flatMap(fn)` | `.pipe(mergeMap(fn))` |
> | `.subscribe(onNext, onError, onComplete)` | `.subscribe({next, error, complete})` |
> | `Flux`는 Spring 통합 내장 | RxJS는 별도 라이브러리 |
>
> `Flux`와 RxJS `Observable`은 개념적으로 매우 가깝다. 둘 다 여러 값의 스트림이고, 콜드 스트림이며(구독해야 실행), `subscribe()`로 데이터를 소비한다. 연산자 이름만 달라서 불편할 뿐, 마음 구조는 같다.

---

## async/await — Promise 위의 문법 설탕

`async/await`는 ES2017(ES8)에 들어온 문법이다. Promise 체이닝을 동기식 코드처럼 읽히게 해준다. 핵심은 단 하나다. **`async` 함수는 항상 Promise를 반환한다. `await`는 Promise가 settled될 때까지 해당 async 함수의 실행을 일시 중단하고 이벤트 루프에 제어를 돌려준다.**

```typescript
// Promise 체이닝 스타일
function fetchUserProfile(userId: number): Promise<Profile> {
  return fetchUser(userId)
    .then(user => fetchPermissions(user.id))
    .then(permissions => buildProfile(user, permissions))  // 이런, user 스코프 문제!
    .catch(err => {
      throw new Error(`프로필 로드 실패: ${err.message}`);
    });
}

// async/await 스타일 — 훨씬 읽기 쉽다
async function fetchUserProfile(userId: number): Promise<Profile> {
  try {
    const user = await fetchUser(userId);
    const permissions = await fetchPermissions(user.id);  // user가 스코프에 있다
    return buildProfile(user, permissions);
  } catch (err) {
    throw new Error(`프로필 로드 실패: ${(err as Error).message}`);
  }
}
```

위 두 코드는 *기능적으로 동일하다*. `async/await`는 컴파일러가 Promise 체이닝으로 변환해주는 문법 설탕이다. 표면은 동기 코드처럼 생겼지만, `await` 시점에 이벤트 루프에 제어를 넘긴다.

### async 함수의 반환 타입

`async` 함수는 항상 `Promise<T>`를 반환한다. 안에서 `return 42`를 써도 실제 반환 타입은 `Promise<number>`다.

```typescript
async function greet(): Promise<string> {
  return "안녕하세요";  // 자동으로 Promise.resolve("안녕하세요") 가 된다
}

async function fail(): Promise<never> {
  throw new Error("실패");  // 자동으로 Promise.reject(new Error("실패")) 가 된다
}
```

TypeScript에서는 반환 타입을 명시하는 편이 낫다. 그래야 함수 내부에서 실수로 다른 타입을 반환할 때 컴파일러가 잡아준다.

> ### 📚 Java/Kotlin 시선 박스 ③ — Kotlin coroutine `suspend` ↔ async/await
>
> 표면적으로 Kotlin의 `suspend fun`과 TypeScript의 `async function`은 매우 비슷해 보인다.
>
> ```kotlin
> // Kotlin
> suspend fun fetchUser(id: Int): User {
>     val response = httpClient.get("/users/$id")  // suspend point
>     return response.body<User>()
> }
> ```
>
> ```typescript
> // TypeScript
> async function fetchUser(id: number): Promise<User> {
>     const response = await fetch(`/users/${id}`);  // await point
>     return response.json();
> }
> ```
>
> 둘 다 비동기 코드를 동기처럼 읽히게 한다. 둘 다 중간에 실행을 일시 중단하고 제어를 반환한다. 하지만 근본적인 차이가 있다.
>
> | 비교 | Kotlin `suspend` | TypeScript `async/await` |
> |---|---|---|
> | 컴파일 결과 | CPS(Continuation Passing Style) 변환 — suspend point마다 상태 머신 | Promise 체이닝으로 변환 |
> | 스케줄러 | `CoroutineDispatcher`로 선택 가능 (`Dispatchers.IO`, `Dispatchers.Main`) | 항상 이벤트 루프의 마이크로태스크 |
> | 취소 | `Job.cancel()` — 협조적 취소, suspend point마다 취소 확인 | `AbortController` — 라이브러리별 구현 필요 |
> | 구조적 동시성 | `CoroutineScope` — 부모가 취소되면 자식도 취소 | 없음 (직접 관리) |
> | `suspend` 전파 | `suspend`는 호출 스택을 따라 전파 | `async`는 선택적 — `await` 없이도 호출 가능 |
>
> Kotlin의 구조적 동시성(Structured Concurrency)은 JS에는 없다. `CoroutineScope`가 취소되면 그 안에서 실행 중인 모든 자식 코루틴도 자동으로 취소된다. TypeScript에서는 이것을 `AbortController`로 직접 구현해야 한다. (AbortSignal 절에서 자세히 다룬다.)
>
> 또 하나의 차이: `suspend fun`을 호출하려면 코루틴 컨텍스트가 필요하다 — `launch`, `async`, `runBlocking` 안에서만 호출할 수 있다. TypeScript에서 `async function`은 어디서든 호출할 수 있다. 다만 결과를 `await`하지 않으면 Promise가 공중에 떠 있게 된다 — 이것이 에러 처리의 함정으로 이어진다.

### await를 빠뜨리면 생기는 일

Java에서 `future.get()`을 빠뜨리면 그냥 Future 객체가 변수에 들어가고, 결과를 꺼내지 못한다. TypeScript에서 `await`를 빠뜨리면 비슷한 일이 일어나지만, 에러 처리가 걸린 경우 훨씬 더 난감한 결과를 낳는다.

```typescript
async function saveUser(user: User): Promise<void> {
  try {
    await db.save(user);
    console.log("저장 완료");
  } catch (err) {
    console.error("저장 실패:", err);
  }
}

// await를 깜빡했다
async function handler(): Promise<void> {
  saveUser(user);  // await 없음 — Promise를 만들고 즉시 다음 줄로 간다
  console.log("이미 다음 줄로 넘어왔다");
  // saveUser 내부의 에러가 catch에서 잡히지 않는다
  // 에러는 Unhandled Rejection이 된다
}
```

TypeScript와 ESLint의 `@typescript-eslint/no-floating-promises` 규칙이 이런 실수를 잡아준다. 프로젝트에 ESLint를 쓴다면 이 규칙을 켜두는 편이 낫다.

---

## 에러 흐름 — try/catch가 잡는 것과 못 잡는 것

비동기 에러 처리는 TypeScript에서 가장 많은 개발자가 발을 헛디디는 영역이다. 솔직하게 말하면, 이 부분은 Java/Kotlin보다 훨씬 더 주의가 필요하다.

> ### 🚧 함정 박스 — 비동기 에러는 어디로 가는가
>
> **Case 1: async 함수 안의 throw — 잘 잡힌다**
>
> ```typescript
> async function fetchData(): Promise<string> {
>   throw new Error("뭔가 잘못됨");
> }
>
> async function main() {
>   try {
>     const data = await fetchData();
>   } catch (err) {
>     console.log("잡혔다:", (err as Error).message);  // ✅ 잡힌다
>   }
> }
> ```
>
> **Case 2: `.then()` 체인 안의 throw — 잘 잡힌다**
>
> ```typescript
> fetchData()
>   .then(data => {
>     throw new Error("then 안에서 에러");
>   })
>   .catch(err => {
>     console.log("잡혔다:", err.message);  // ✅ 잡힌다
>   });
> ```
>
> **Case 3: await 없는 Promise — 잡히지 않는다** ⚠️
>
> ```typescript
> async function main() {
>   try {
>     fetchData();  // await 없음
>   } catch (err) {
>     console.log("잡힌다고 생각하겠지만");  // ❌ 잡히지 않는다
>   }
> }
>
> // fetchData()의 에러는 Unhandled Rejection이 된다
> ```
>
> **Case 4: setTimeout 콜백 안의 throw — 잡히지 않는다** ⚠️
>
> ```typescript
> async function main() {
>   try {
>     setTimeout(() => {
>       throw new Error("타이머 콜백 에러");
>     }, 100);
>   } catch (err) {
>     console.log("절대 여기 오지 않는다");  // ❌ 잡히지 않는다
>   }
> }
>
> // setTimeout 콜백은 다른 이벤트 루프 tick에서 실행된다
> // try/catch 블록이 이미 끝난 이후이므로 잡을 수 없다
> ```
>
> **Case 5: Promise 생성자 외부의 throw — 잡히지 않는다** ⚠️
>
> ```typescript
> // 이건 Promise가 아니다 — 일반 예외
> function badFunction() {
>   const p = new Promise((resolve, reject) => {
>     resolve(42);
>   });
>   throw new Error("Promise 밖에서 던짐");  // 동기 예외
>   return p;
> }
>
> // 이것은 잡힌다 — 동기 예외니까
> try {
>   badFunction();
> } catch (err) {
>   console.log("동기 예외라 잡힌다");  // ✅ 잡힌다
> }
> ```
>
> **핵심 규칙**: `await`된 Promise 안의 에러는 try/catch로 잡힌다. `await`하지 않은 Promise의 에러는 잡히지 않는다. `setTimeout`/`setInterval` 콜백 안의 에러는 async/await와 무관하게 잡히지 않는다.

### Unhandled Rejection — 조용히 사라지거나 프로세스를 죽인다

`await`하지 않은 Promise에서 에러가 나면 어떻게 될까? 브라우저에서는 `unhandledrejection` 이벤트가 발생한다. Node.js에서는 버전에 따라 동작이 달랐다.

- **Node.js 14 이전**: 경고만 출력하고 계속 실행 (조용히 넘어감)
- **Node.js 15+**: 기본적으로 **프로세스 종료**

프로세스가 죽는다. 운영 환경이라면 찜찜함을 넘어서 실제 장애다.

```typescript
// Node.js에서 Unhandled Rejection 전역 처리
process.on("unhandledRejection", (reason, promise) => {
  console.error("처리되지 않은 Promise 거부:", reason);
  // 이 시점에 로깅을 하고 프로세스를 안전하게 종료할 수 있다
  process.exit(1);
});

// 브라우저에서
window.addEventListener("unhandledrejection", (event) => {
  console.error("처리되지 않은 거부:", event.reason);
  event.preventDefault();  // 브라우저 기본 에러 처리 막기
});
```

Java의 `Future.get()`과 비교해보면 어떻게 다를까? Java에서 `Future.get()`을 호출하지 않으면 `ExecutionException`이 그냥 묻힌다 — 하지만 적어도 스레드는 계속 살아있고 다른 코드는 돌아간다. Node.js에서는 Unhandled Rejection이 *프로세스 자체를 죽일 수 있다*는 점이 다르다. 그래서 더 주의가 필요하다.

실무에서 권장하는 패턴은 세 가지다.

```typescript
// 패턴 1: void 연산자로 의도적으로 무시함을 명시
void somePromise().catch(logger.error);

// 패턴 2: 항상 await, catch 붙이기
async function safeWrapper() {
  try {
    await riskyOperation();
  } catch (err) {
    logger.error("안전하게 로깅", err);
  }
}

// 패턴 3: 전역 핸들러 + 구조적 종료
process.on("unhandledRejection", (reason) => {
  logger.fatal("미처리 거부", { reason });
  // 그레이스풀 셧다운 후 종료
  gracefulShutdown().then(() => process.exit(1));
});
```

---

## AbortSignal과 취소 — 잊혀지는 자리

많은 학습서가 `AbortController`를 `fetch` 예제로 잠깐 소개하고 넘어간다. 하지만 Java/Kotlin 개발자에게 취소 패턴은 매우 중요하다. Spring WebFlux에서는 구독 해제(`dispose()`)를 Reactor가 관리해준다. Kotlin에서는 `Job.cancel()`이 있다. TypeScript에서는 `AbortController`가 그 역할을 한다 — 하지만 훨씬 더 명시적으로 직접 구현해야 한다.

### AbortController와 AbortSignal 기본

```typescript
// AbortController: 취소 신호를 보내는 주체
const controller = new AbortController();

// AbortSignal: 취소 신호를 받는 토큰
const signal = controller.signal;

// 5초 후 자동 취소
const timeoutId = setTimeout(() => controller.abort("5초 타임아웃"), 5000);

try {
  const response = await fetch("https://api.example.com/data", { signal });
  
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  
  const data = await response.json();
  clearTimeout(timeoutId);  // 성공 시 타임아웃 해제
  return data;
} catch (err) {
  if (err instanceof DOMException && err.name === "AbortError") {
    console.log("요청이 취소되었습니다:", controller.signal.reason);
  } else {
    throw err;
  }
}
```

`abort()` 메서드를 호출하면 `signal.aborted`가 `true`가 되고, `signal.reason`에 취소 이유가 저장된다. `fetch`는 이 신호를 감지해 요청을 중단하고 `AbortError`를 던진다.

### AbortSignal.timeout — 내장 타임아웃

Node.js 17+ / 최신 브라우저에서는 더 간단한 방법이 생겼다.

```typescript
// 3초 타임아웃을 가진 signal 직접 생성
const response = await fetch("https://api.example.com/data", {
  signal: AbortSignal.timeout(3000)
});
```

`AbortSignal.timeout(ms)`는 지정된 시간 후 자동으로 abort되는 signal을 반환한다. `AbortController`를 따로 만들고 타임아웃을 관리하는 보일러플레이트가 사라진다.

### 커스텀 함수에서 AbortSignal 지원하기

`fetch`뿐만 아니라 자신이 만드는 함수에도 `AbortSignal`을 지원할 수 있다.

```typescript
async function downloadWithProgress(
  url: string,
  onProgress: (loaded: number, total: number) => void,
  signal?: AbortSignal
): Promise<Blob> {
  const response = await fetch(url, { signal });
  
  if (!response.body) throw new Error("스트림 없음");
  
  const contentLength = Number(response.headers.get("Content-Length") ?? 0);
  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let loaded = 0;
  
  while (true) {
    // 취소 신호 확인
    if (signal?.aborted) {
      reader.cancel();
      throw new DOMException("다운로드 취소됨", "AbortError");
    }
    
    const { done, value } = await reader.read();
    
    if (done) break;
    
    chunks.push(value);
    loaded += value.length;
    onProgress(loaded, contentLength);
  }
  
  return new Blob(chunks);
}

// 사용 예
const controller = new AbortController();

downloadButton.addEventListener("click", async () => {
  try {
    const blob = await downloadWithProgress(
      "/large-file.zip",
      (loaded, total) => updateProgressBar(loaded / total),
      controller.signal
    );
    saveFile(blob);
  } catch (err) {
    if (err instanceof DOMException && err.name === "AbortError") {
      showMessage("다운로드가 취소되었습니다");
    } else {
      showError(err);
    }
  }
});

cancelButton.addEventListener("click", () => {
  controller.abort("사용자가 취소");
});
```

### AbortSignal.any — 여러 신호 합치기

Node.js 20+ / 최신 브라우저에서는 `AbortSignal.any(signals)`로 여러 신호를 OR 조건으로 합칠 수 있다.

```typescript
// 타임아웃 또는 사용자 취소 중 하나가 먼저 오면 취소
const userController = new AbortController();
const combinedSignal = AbortSignal.any([
  userController.signal,
  AbortSignal.timeout(30_000)
]);

const data = await fetch(url, { signal: combinedSignal });
```

Java/Kotlin 비교 관점에서 정리하면 이렇다.

| 취소 메커니즘 | TypeScript | Java/Kotlin |
|---|---|---|
| 취소 토큰 | `AbortSignal` | Kotlin `Job`, Reactor `Disposable` |
| 취소 발동 | `AbortController.abort()` | `Job.cancel()`, `dispose()` |
| 타임아웃 | `AbortSignal.timeout(ms)` | Kotlin `withTimeout`, Reactor `timeout()` |
| 구조적 취소 | 직접 구현 | Kotlin CoroutineScope 자동 전파 |
| 취소 확인 | `signal.aborted` 체크 | Kotlin `isActive`, `ensureActive()` |

Kotlin의 구조적 동시성에 익숙한 사람이라면 TypeScript의 취소 모델이 좀 번거롭게 느껴질 수 있다. 맞다. JS 생태계에는 Kotlin처럼 언어 수준에서 취소를 보장하는 메커니즘이 없다. `signal`을 함수 시그니처로 전달하고, 각 비동기 함수가 그것을 *협조적으로* 체크해야 한다. 이 점은 솔직히 Kotlin이 앞선 부분이다.

---

## Observable (RxJS) — 여러 값의 스트림

Promise는 *단 하나*의 값(또는 에러)을 표현한다. 하지만 클릭 이벤트, 웹소켓 메시지, 센서 데이터 스트림처럼 *시간에 걸쳐 여러 값이 흘러오는* 상황은 어떻게 처리할까?

이 문제를 위해 나온 것이 RxJS의 `Observable`이다.

### Observable의 기본 구조

```typescript
import { Observable, Subject, interval, fromEvent } from "rxjs";
import { map, filter, take, debounceTime, switchMap } from "rxjs/operators";

// Observable 직접 만들기
const countdown$ = new Observable<number>(subscriber => {
  let count = 3;
  const id = setInterval(() => {
    subscriber.next(count--);  // 값 발행
    if (count < 0) {
      clearInterval(id);
      subscriber.complete();   // 완료
    }
  }, 1000);
  
  // cleanup 함수 — unsubscribe 시 실행됨
  return () => {
    clearInterval(id);
    console.log("cleanup 완료");
  };
});

// 구독
const subscription = countdown$.subscribe({
  next: value => console.log(`카운트다운: ${value}`),
  error: err => console.error("에러:", err),
  complete: () => console.log("완료!")
});

// 나중에 구독 해제
setTimeout(() => subscription.unsubscribe(), 2500);
```

`$` 접미사는 RxJS 커뮤니티의 관행이다 — Observable임을 나타낸다.

### 실전 패턴 — 자동완성 검색

Observable의 진가가 드러나는 예제를 보자. 입력창의 자동완성 — 사용자가 타이핑할 때마다 API를 호출하되, 이전 요청을 취소하고 입력이 멈춘 후에만 검색하는 패턴이다.

```typescript
import { fromEvent } from "rxjs";
import { debounceTime, distinctUntilChanged, switchMap, catchError } from "rxjs/operators";
import { from, EMPTY } from "rxjs";

const searchInput = document.getElementById("search") as HTMLInputElement;

const search$ = fromEvent(searchInput, "input").pipe(
  map(event => (event.target as HTMLInputElement).value),
  debounceTime(300),          // 300ms 동안 입력이 없을 때만 통과
  distinctUntilChanged(),     // 이전과 같은 값이면 무시
  switchMap(query => {        // 이전 요청 취소하고 새 요청 시작
    if (!query.trim()) return EMPTY;  // 빈 검색어 무시
    return from(
      fetch(`/api/search?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
    ).pipe(
      catchError(err => {
        console.error("검색 에러:", err);
        return EMPTY;  // 에러 시 빈 결과
      })
    );
  })
);

const sub = search$.subscribe(results => {
  renderResults(results);
});

// 컴포넌트 해제 시
// sub.unsubscribe();
```

`switchMap`이 핵심이다. 이전 Observable을 자동으로 취소(unsubscribe)하고 새 것으로 교체한다. Reactor의 `Flux.switchMap()`과 정확히 같은 개념이다.

### Hot vs Cold Observable

Reactor에서 `Flux`와 `ConnectableFlux`의 차이를 아는 사람이라면 이 개념이 친숙할 것이다.

- **Cold Observable**: 구독할 때마다 새 실행이 시작된다. 각 구독자가 전체 스트림을 받는다. (Reactor의 `Mono`/`Flux` 기본 동작과 유사)
- **Hot Observable**: 이미 진행 중인 스트림에 구독자가 *참여*한다. 구독 시점 이후의 값만 받는다. (웹소켓, 이벤트, `Subject`)

```typescript
import { Subject } from "rxjs";

// Subject는 Hot Observable이자 Observer다
const subject$ = new Subject<string>();

// 첫 번째 구독자
subject$.subscribe(v => console.log("구독자 A:", v));

subject$.next("첫 번째 값");  // A만 받는다

// 두 번째 구독자 — 이후부터만 받는다
subject$.subscribe(v => console.log("구독자 B:", v));

subject$.next("두 번째 값");   // A와 B 모두 받는다
subject$.next("세 번째 값");   // A와 B 모두 받는다
subject$.complete();
```

### RxJS의 주요 연산자 맵

Reactor를 쓰던 개발자라면 연산자 이름이 다를 뿐, 개념은 같다.

| Reactor | RxJS | 설명 |
|---|---|---|
| `map()` | `map()` | 동기 변환 |
| `flatMap()` | `mergeMap()` | 비동기 변환, 순서 보장 없음 |
| `concatMap()` | `concatMap()` | 비동기 변환, 순서 보장 |
| `switchMap()` | `switchMap()` | 이전 취소, 새 것으로 교체 |
| `filter()` | `filter()` | 조건부 통과 |
| `take(n)` | `take(n)` | n개만 받고 완료 |
| `takeUntil(signal)` | `takeUntil(notifier$)` | 신호 오면 완료 |
| `debounce()` | `debounceTime(ms)` | 입력 안정화 |
| `zip()` | `zip()` | 쌍으로 합치기 |
| `combineLatest()` | `combineLatest()` | 최신 값 조합 |
| `shareReplay()` | `shareReplay()` | 멀티캐스트 |

---

## AsyncIterator와 `for await...of`

RxJS Observable은 강력하지만 별도 라이브러리다. ECMAScript 표준도 비동기 스트림을 다루는 방법을 정의했는데, 바로 **AsyncIterator**다.

### AsyncIterator 프로토콜

```typescript
// AsyncIterator를 구현하는 객체는 이 인터페이스를 따른다
interface AsyncIterator<T> {
  next(): Promise<{ done: boolean; value: T }>;
  return?(value?: any): Promise<{ done: boolean; value: any }>;
  throw?(e?: any): Promise<{ done: boolean; value: any }>;
}

interface AsyncIterable<T> {
  [Symbol.asyncIterator](): AsyncIterator<T>;
}
```

실제로 직접 만들 일은 적고, `async generator`로 만드는 것이 훨씬 편하다.

### async generator — AsyncIterator를 쉽게 만들기

```typescript
// async generator 함수는 AsyncIterator를 반환한다
async function* readLines(url: string): AsyncGenerator<string> {
  const response = await fetch(url);
  if (!response.body) throw new Error("스트림 없음");
  
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  
  try {
    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        if (buffer) yield buffer;  // 마지막 줄
        break;
      }
      
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";  // 미완성 줄은 버퍼에 남긴다
      
      for (const line of lines) {
        yield line;  // 완성된 줄마다 yield
      }
    }
  } finally {
    reader.releaseLock();
  }
}

// for await...of로 소비
async function processLogFile(url: string) {
  let errorCount = 0;
  
  for await (const line of readLines(url)) {
    if (line.includes("ERROR")) {
      errorCount++;
      console.log("에러 발견:", line);
    }
  }
  
  console.log(`총 에러 수: ${errorCount}`);
}
```

`for await...of`는 AsyncIterator를 소비하는 문법이다. 각 iteration마다 `await`가 내장되어 있다.

### Node.js Streams와 AsyncIterator

Node.js의 Readable 스트림은 AsyncIterator 프로토콜을 구현한다. 파일을 라인 단위로 읽는 것이 매우 자연스러워졌다.

```typescript
import { createReadStream } from "fs";
import { createInterface } from "readline";

async function processLargeFile(filePath: string): Promise<void> {
  const fileStream = createReadStream(filePath);
  const rl = createInterface({
    input: fileStream,
    crlfDelay: Infinity,
  });
  
  let lineNumber = 0;
  
  // readline이 AsyncIterator를 구현하므로 for await...of 사용 가능
  for await (const line of rl) {
    lineNumber++;
    
    if (line.trim() === "") continue;
    
    await processLine(lineNumber, line);
  }
  
  console.log(`총 ${lineNumber}줄 처리 완료`);
}
```

Java에서 `Files.lines(path)` + `Stream.forEach()`로 처리하던 것과 유사한 패턴이다. 다만 Java는 동기 스트림이고, 이것은 비동기다.

### AsyncIterator vs Observable

둘 다 여러 값의 스트림이지만 차이가 있다.

| 비교 | AsyncIterator | RxJS Observable |
|---|---|---|
| 표준 여부 | ECMAScript 표준 | 별도 라이브러리 |
| Pull vs Push | **Pull** — 소비자가 요청 | **Push** — 생산자가 능동적으로 발행 |
| 배압(backpressure) | 자연스럽게 지원 | `operators`로 제어 필요 |
| 에러 처리 | try/catch | `.catchError()` |
| 완료 | `done: true` | `complete()` |
| 연산자 | 없음 (직접 구현) | 풍부한 연산자 생태계 |
| 적합한 상황 | 순차 처리, 파일/DB | 이벤트, 실시간, 복잡한 스트림 |

간단한 순차 처리나 파일/DB 스트리밍이라면 AsyncIterator로 충분하다. 복잡한 이벤트 조합이나 실시간 데이터 처리라면 RxJS가 낫다.

---

## 병렬 패턴 — Promise.all/allSettled/race/any 4종

비동기 작업을 *병렬로* 실행하고 결과를 모아야 할 때는 Promise 정적 메서드 4개를 쓴다. Java의 `CompletableFuture.allOf()`, `Future`의 `invokeAll()`에 해당하는 도구들이다.

### Promise.all — 전부 성공해야 한다

```typescript
// 세 API를 병렬로 호출하고 전부 완료되면 결과 반환
async function fetchDashboardData(userId: number) {
  const [user, orders, notifications] = await Promise.all([
    fetchUser(userId),
    fetchOrders(userId),
    fetchNotifications(userId),
  ]);
  
  return { user, orders, notifications };
}
```

하나라도 실패하면 Promise.all 전체가 즉시 거부된다. 나머지 Promise는 취소되지 않고 계속 실행되지만, 그 결과는 무시된다. Java의 `CompletableFuture.allOf()`와 비슷하지만, 타입 추론이 튜플로 정확하게 된다는 점이 더 편하다.

타입 추론이 어떻게 되는지 보자.

```typescript
// TypeScript는 Promise.all의 타입을 정확히 추론한다
const result = await Promise.all([
  fetchUser(1),        // Promise<User>
  fetchOrders(1),      // Promise<Order[]>
  Promise.resolve(42), // Promise<number>
]);

// result의 타입은 [User, Order[], number] — 튜플!
const [user, orders, count] = result;
// user: User, orders: Order[], count: number
```

### Promise.allSettled — 성패 무관하게 전부 기다린다

`Promise.all`과 달리, 하나가 실패해도 나머지를 기다린다. 각 결과가 `fulfilled` 또는 `rejected` 상태로 온다.

```typescript
async function fetchMultipleExchangeRates(currencies: string[]) {
  const results = await Promise.allSettled(
    currencies.map(currency => fetchExchangeRate(currency))
  );
  
  const rates: Record<string, number> = {};
  const failures: string[] = [];
  
  results.forEach((result, index) => {
    if (result.status === "fulfilled") {
      rates[currencies[index]] = result.value;
    } else {
      failures.push(currencies[index]);
      console.warn(`환율 조회 실패: ${currencies[index]}`, result.reason);
    }
  });
  
  if (failures.length > 0) {
    console.warn(`${failures.length}개 통화 조회 실패`);
  }
  
  return rates;
}
```

일부 실패가 허용되는 상황 — 여러 소스에서 데이터를 가져오되, 일부 소스가 죽어도 나머지로 처리하는 경우 — 에 적합하다.

### Promise.race — 가장 빠른 하나

여러 Promise 중 가장 먼저 settled되는 것을 쓴다. 성공이든 실패든 상관없다.

```typescript
// 타임아웃 구현 — AbortSignal 없이
function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error(`${ms}ms 타임아웃`)), ms)
  );
  
  return Promise.race([promise, timeout]);
}

// 또는 AbortSignal로 더 깔끔하게
const result = await withTimeout(fetchData(), 5000);
```

단, `Promise.race`는 "패한" Promise를 취소하지 않는다. 단지 결과를 무시할 뿐이다. 타임아웃 같은 경우에 `Promise.race` + `AbortSignal`을 함께 쓰면 실제 요청도 취소할 수 있다.

```typescript
async function fetchWithTimeout<T>(
  promiseFactory: (signal: AbortSignal) => Promise<T>,
  ms: number
): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(`${ms}ms 초과`), ms);
  
  try {
    return await promiseFactory(controller.signal);
  } finally {
    clearTimeout(timeoutId);
  }
}

// 사용
const user = await fetchWithTimeout(
  signal => fetchUser(userId, signal),
  3000
);
```

### Promise.any — 하나라도 성공하면 된다

`Promise.race`와 비슷하지만, 성공한 것을 기다린다. 모두 실패해야 거부된다.

```typescript
// 여러 CDN에서 파일을 받고 가장 빠른 것을 쓴다
async function fetchFromFastestCDN(path: string): Promise<Response> {
  const cdnUrls = [
    `https://cdn1.example.com${path}`,
    `https://cdn2.example.com${path}`,
    `https://cdn3.example.com${path}`,
  ];
  
  try {
    return await Promise.any(
      cdnUrls.map(url => fetch(url))
    );
  } catch (err) {
    // AggregateError — 모든 Promise가 거부됨
    if (err instanceof AggregateError) {
      throw new Error(`모든 CDN 실패: ${err.errors.map(e => e.message).join(", ")}`);
    }
    throw err;
  }
}
```

`Promise.any`가 모두 실패하면 `AggregateError`가 던져진다. 이것은 모든 에러를 `errors` 배열에 담는다.

### 4종 비교 요약

```typescript
const p1 = delay(100).then(() => "A");    // 100ms 후 성공
const p2 = delay(200).then(() => { throw new Error("B 실패"); });  // 200ms 후 실패
const p3 = delay(300).then(() => "C");    // 300ms 후 성공

// Promise.all — 하나라도 실패하면 전체 실패
await Promise.all([p1, p2, p3]);
// → 200ms 후 Error("B 실패")로 거부

// Promise.allSettled — 전부 기다리고 상태 반환
await Promise.allSettled([p1, p2, p3]);
// → 300ms 후 [
//     { status: "fulfilled", value: "A" },
//     { status: "rejected", reason: Error("B 실패") },
//     { status: "fulfilled", value: "C" }
//   ]

// Promise.race — 가장 빠른 것 (성공/실패 무관)
await Promise.race([p1, p2, p3]);
// → 100ms 후 "A"

// Promise.any — 가장 빠른 성공
await Promise.any([p1, p2, p3]);
// → 100ms 후 "A" (p2가 실패해도 p1이 성공했으므로)
```

---

## 실전 패턴 — 재시도, 쓰로틀링, 동시성 제한

Promise 4종을 조합하면 실무에서 자주 쓰는 패턴들을 만들 수 있다.

### 재시도 (Retry with Exponential Backoff)

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  options: {
    maxAttempts: number;
    initialDelay: number;
    backoffFactor: number;
    signal?: AbortSignal;
  }
): Promise<T> {
  const { maxAttempts, initialDelay, backoffFactor, signal } = options;
  let lastError: Error;
  
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    if (signal?.aborted) {
      throw new DOMException("재시도 취소됨", "AbortError");
    }
    
    try {
      return await fn();
    } catch (err) {
      lastError = err as Error;
      
      if (attempt < maxAttempts) {
        const delay = initialDelay * Math.pow(backoffFactor, attempt - 1);
        console.warn(`시도 ${attempt} 실패, ${delay}ms 후 재시도:`, err);
        
        await new Promise<void>((resolve, reject) => {
          const id = setTimeout(resolve, delay);
          signal?.addEventListener("abort", () => {
            clearTimeout(id);
            reject(new DOMException("대기 중 취소됨", "AbortError"));
          }, { once: true });
        });
      }
    }
  }
  
  throw lastError!;
}

// 사용
const data = await withRetry(
  () => fetchData(url),
  { maxAttempts: 3, initialDelay: 1000, backoffFactor: 2 }
);
```

### 동시성 제한 (Concurrency Limiting)

100개의 URL을 동시에 모두 fetch하면 서버에 과부하가 걸린다. N개씩 제한해서 처리하자.

```typescript
async function* chunks<T>(arr: T[], size: number): AsyncGenerator<T[]> {
  for (let i = 0; i < arr.length; i += size) {
    yield arr.slice(i, i + size);
  }
}

async function fetchWithConcurrencyLimit<T, R>(
  items: T[],
  fn: (item: T) => Promise<R>,
  concurrency: number
): Promise<R[]> {
  const results: R[] = new Array(items.length);
  let index = 0;
  
  async function worker() {
    while (index < items.length) {
      const currentIndex = index++;
      results[currentIndex] = await fn(items[currentIndex]);
    }
  }
  
  // concurrency개의 워커를 동시에 실행
  await Promise.all(
    Array.from({ length: concurrency }, () => worker())
  );
  
  return results;
}

// 사용 — 5개씩 병렬로 처리
const results = await fetchWithConcurrencyLimit(
  urls,
  url => fetch(url).then(r => r.json()),
  5
);
```

Reactor에서 `Flux.flatMap(fn, 5)`로 동시성을 제한하던 것과 같은 효과다.

### 쓰로틀링과 디바운싱 (직접 구현)

RxJS 없이 Promise로 구현한다.

```typescript
// Debounce — 마지막 호출 후 delay ms 지나야 실행
function debounce<T extends (...args: any[]) => Promise<any>>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => Promise<ReturnType<T>> {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;
  let pendingResolve: ((value: ReturnType<T>) => void) | null = null;
  let pendingReject: ((reason: any) => void) | null = null;
  
  return function (...args: Parameters<T>): Promise<ReturnType<T>> {
    if (timeoutId) clearTimeout(timeoutId);
    
    return new Promise((resolve, reject) => {
      pendingResolve = resolve as any;
      pendingReject = reject;
      
      timeoutId = setTimeout(async () => {
        try {
          const result = await fn(...args);
          pendingResolve?.(result);
        } catch (err) {
          pendingReject?.(err);
        }
      }, delay);
    });
  };
}

const debouncedSearch = debounce(searchAPI, 300);
```

---

## 타입스크립트로 비동기 타입 다루기

### Promise 타입 추론

TypeScript는 Promise의 타입 매개변수를 잘 추론한다.

```typescript
// 추론 가능 — 명시 불필요
async function fetchUser(id: number) {
  const response = await fetch(`/users/${id}`);
  return response.json() as Promise<User>;
}
// 반환 타입: Promise<User>

// 명시 권장 — 인터페이스 계약이 있을 때
async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/users/${id}`);
  const data: unknown = await response.json();
  
  // 런타임 검증 (zod 등)
  return UserSchema.parse(data);
}
```

### `Awaited<T>` 유틸리티 타입

Promise에서 타입을 꺼낼 때 `Awaited<T>`를 쓴다.

```typescript
type FetchResult = Awaited<ReturnType<typeof fetchUser>>;
// FetchResult = User

// 중첩 Promise도 평탄화
type Unwrapped = Awaited<Promise<Promise<string>>>;
// Unwrapped = string
```

### 에러 타입 처리

TypeScript의 catch 블록에서 `err`의 타입은 `unknown`이다. Java처럼 예외 타입을 선언할 수 없다.

```typescript
try {
  await riskyOperation();
} catch (err) {
  // err는 unknown — 타입 좁히기가 필요하다
  
  if (err instanceof Error) {
    console.error(err.message);
    console.error(err.stack);
  } else if (typeof err === "string") {
    console.error(err);
  } else {
    console.error("알 수 없는 에러:", err);
  }
}
```

커스텀 에러 클래스를 만들면 더 구조적으로 처리할 수 있다.

```typescript
class ApiError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly requestId?: string
  ) {
    super(message);
    this.name = "ApiError";
    // Node.js에서 스택 트레이스 보정
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, ApiError);
    }
  }
}

class NetworkError extends Error {
  constructor(message: string, public readonly cause?: Error) {
    super(message, { cause });
    this.name = "NetworkError";
  }
}

async function apiCall<T>(url: string): Promise<T> {
  let response: Response;
  
  try {
    response = await fetch(url);
  } catch (err) {
    throw new NetworkError("네트워크 오류", err instanceof Error ? err : undefined);
  }
  
  if (!response.ok) {
    throw new ApiError(
      `API 오류: ${response.statusText}`,
      response.status,
      response.headers.get("X-Request-ID") ?? undefined
    );
  }
  
  return response.json();
}

// 사용 시 타입 좁히기
try {
  const user = await apiCall<User>("/users/1");
} catch (err) {
  if (err instanceof ApiError) {
    console.error(`API ${err.statusCode}:`, err.message);
    if (err.statusCode === 401) redirectToLogin();
  } else if (err instanceof NetworkError) {
    console.error("네트워크:", err.message, err.cause);
    showOfflineMessage();
  } else {
    throw err;  // 알 수 없는 에러는 다시 던진다
  }
}
```

### Result 타입 패턴

예외를 던지는 대신 Result 타입을 반환하는 패턴도 점점 많이 쓰인다. Kotlin의 `Result<T>`와 유사하다.

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function safeApiCall<T>(url: string): Promise<Result<T>> {
  try {
    const data = await apiCall<T>(url);
    return { ok: true, value: data };
  } catch (err) {
    return { ok: false, error: err instanceof Error ? err : new Error(String(err)) };
  }
}

// 사용 — 예외 없이 분기 처리
const result = await safeApiCall<User>("/users/1");

if (result.ok) {
  console.log("사용자:", result.value.name);
} else {
  console.error("실패:", result.error.message);
}
```

Effect-ts나 neverthrow 같은 라이브러리가 이 패턴을 더 정교하게 구현해준다.

---

## 실전 예제 — API 클라이언트 구현

지금까지 배운 모든 것을 통합한 실전 예제다. 재시도, 타임아웃, 취소, 에러 처리를 모두 갖춘 API 클라이언트를 만들어보자.

```typescript
interface RequestConfig {
  method?: "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
  body?: unknown;
  headers?: Record<string, string>;
  signal?: AbortSignal;
  timeout?: number;
  retries?: number;
}

interface ApiClientOptions {
  baseUrl: string;
  defaultTimeout: number;
  defaultRetries: number;
  onError?: (err: Error, url: string) => void;
}

class ApiClient {
  constructor(private readonly options: ApiClientOptions) {}
  
  async request<T>(path: string, config: RequestConfig = {}): Promise<T> {
    const {
      method = "GET",
      body,
      headers = {},
      signal,
      timeout = this.options.defaultTimeout,
      retries = this.options.defaultRetries,
    } = config;
    
    const url = `${this.options.baseUrl}${path}`;
    
    // 타임아웃과 사용자 취소 신호 합치기
    const signals: AbortSignal[] = [AbortSignal.timeout(timeout)];
    if (signal) signals.push(signal);
    const combinedSignal = AbortSignal.any(signals);
    
    return withRetry(
      async () => {
        const response = await fetch(url, {
          method,
          headers: {
            "Content-Type": "application/json",
            ...headers,
          },
          body: body ? JSON.stringify(body) : undefined,
          signal: combinedSignal,
        });
        
        if (!response.ok) {
          const errorBody = await response.text().catch(() => "");
          throw new ApiError(
            `${method} ${path} 실패: ${response.statusText}`,
            response.status,
            response.headers.get("X-Request-ID") ?? undefined
          );
        }
        
        if (response.status === 204) return undefined as T;
        return response.json() as Promise<T>;
      },
      {
        maxAttempts: retries,
        initialDelay: 500,
        backoffFactor: 2,
        signal: combinedSignal,
      }
    );
  }
  
  get<T>(path: string, config?: RequestConfig): Promise<T> {
    return this.request<T>(path, { ...config, method: "GET" });
  }
  
  post<T>(path: string, body: unknown, config?: RequestConfig): Promise<T> {
    return this.request<T>(path, { ...config, method: "POST", body });
  }
}

// 사용
const api = new ApiClient({
  baseUrl: "https://api.example.com",
  defaultTimeout: 10_000,
  defaultRetries: 3,
});

// 취소 가능한 요청
const controller = new AbortController();
const user = await api.get<User>("/users/1", { signal: controller.signal });

// 5초 후 취소
setTimeout(() => controller.abort("페이지 벗어남"), 5000);
```

---

## 비동기 테스트 패턴 맛보기

비동기 코드 테스트의 핵심은 *Promise를 반환하거나 async를 쓰는 것*이다. 자세한 내용은 14장에서 다루지만, 기본 패턴만 짚어두자.

```typescript
import { describe, it, expect, vi } from "vitest";

describe("fetchUserProfile", () => {
  it("성공 시 프로필을 반환한다", async () => {
    // Arrange
    vi.spyOn(global, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ id: 1, name: "Alice" }))
    );
    
    // Act
    const profile = await fetchUserProfile(1);
    
    // Assert
    expect(profile.name).toBe("Alice");
  });
  
  it("API 실패 시 에러를 던진다", async () => {
    vi.spyOn(global, "fetch").mockResolvedValue(
      new Response(null, { status: 404 })
    );
    
    await expect(fetchUserProfile(1)).rejects.toThrow(ApiError);
  });
  
  it("타임아웃 시 AbortError가 발생한다", async () => {
    vi.spyOn(global, "fetch").mockImplementation(
      () => new Promise(resolve => setTimeout(resolve, 10_000))  // 느린 응답
    );
    
    const fetchWithShortTimeout = () =>
      fetchWithTimeout(signal => fetchUserProfile(1, signal), 100);
    
    await expect(fetchWithShortTimeout()).rejects.toThrow();
  });
});
```

> **📖 더 깊이 가려면**
>
> 비동기 코드 테스트 패턴 — fake timer, mock vs stub, async error 검증, Promise.all 테스트 — 은 14장에서 자세히 다룬다. 특히 `vi.useFakeTimers()`로 setTimeout을 제어하는 방법과, msw(Mock Service Worker)로 fetch를 인터셉트하는 패턴이 실무에서 자주 쓰인다.

---

## 마무리

비동기 모델은 TypeScript를 배우면서 가장 시간이 걸리는 부분 중 하나다. Java/Kotlin의 비동기 모델이 이미 머릿속에 자리 잡혀 있어서, 겉으로 비슷해 보이는 Promise가 실제로는 다르게 동작할 때 혼란이 온다. 특히 두 가지를 꼭 기억해두자.

**첫째, Promise는 생성 즉시 실행된다.** Mono처럼 구독 전에 멈춰있지 않는다. `await`를 빠뜨리면 Promise가 허공을 떠다니고, 그 안의 에러가 Unhandled Rejection이 된다. Node.js 15+에서는 그것이 프로세스 종료로 이어진다.

**둘째, try/catch는 만능이 아니다.** `await`된 비동기 코드의 에러는 잡힌다. `setTimeout` 콜백이나 `await`하지 않은 Promise의 에러는 잡히지 않는다. 이 규칙을 체화하면 비동기 에러 디버깅이 훨씬 빨라진다.

취소 패턴은 Kotlin만큼 매끄럽지 않다. 하지만 `AbortController`와 `AbortSignal`을 꼼꼼히 전달하면 실용적인 수준의 취소는 충분히 구현된다. 번거롭더라도 시간이 지남에 따라 익숙해진다.

Observable과 AsyncIterator는 필요할 때 꺼내는 도구다. 단순한 비동기 요청은 Promise와 async/await로 충분하다. 이벤트 스트림이나 실시간 데이터가 필요해지면 그때 RxJS를 꺼내도 늦지 않다.

다음 장에서는 모듈 시스템과 빌드 도구로 넘어간다. CommonJS와 ESM이 공존하는 혼란스러운 세계, `tsconfig.json`의 핵심 옵션들, 그리고 빌드 파이프라인을 어떻게 구성하는지 살펴보자. 비동기 코드를 짤 줄 알게 되었다면, 이제 그 코드를 배포 가능한 형태로 묶는 법을 알아야 한다.
