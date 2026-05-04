# 2장. JavaScript와 TypeScript

## 구조적 타입, 클로저, Promise, 그리고 TS 유틸리티 타입의 자리 + 패키지·monorepo

콜백 지옥, 그건 우리도 안다. 한때 한 페이지에 여덟 단 들여쓰기가 박혀 있던 코드를 본 적이 있다면, 이미 이 장의 도입 한 페이지는 건너뛰어도 좋다. JavaScript가 비동기를 표현하는 방식이 콜백에서 Promise로, 그리고 `async`/`await`으로 옮겨 왔다는 사실, 서비스 워커도 이벤트 루프 위에서 도는 한 줄 흐름이라는 사실까지는 익숙하다. 그러니 이 장에서 굳이 콜백 피라미드를 다시 그려 보일 이유는 없다.

대신 한 발 안쪽으로 들어가 보자. Spring과 JPA로 5년, 10년을 굴려 본 손이 TypeScript 프로젝트를 처음 열었을 때 가장 자주 데이는 곳은 어디인가. `tsc` 옵션 한 줄 때문이 아니다. JS의 `this`가 어디서 결정되는지, `forEach` 안의 `await`이 왜 침묵하는지, 구조적 타입 시스템이 `implements` 없이도 인터페이스를 만족시킨다는 사실이 어떤 자유와 어떤 함정을 동시에 가져다주는지 — 그 지점들이다. 그리고 마지막 한 가지, `npm`·`pnpm`·`Bun`과 monorepo로 짜인 의존성 그래프가 Maven multi-module이나 Gradle composite 빌드와 어디서 맞닿아 있고 어디서 갈라지는지를 손에 익히는 일이다.

이 장은 그래서 두 갈래로 흐른다. 앞쪽 절반은 언어다 — Kotlin·Java 출신이 TS에서 다시 학습해야 할 자리와, 그대로 들고 가도 되는 직관을 갈라낸다. 뒤쪽 절반은 도구다 — 패키지 매니저와 monorepo의 풍경을, Spring 모듈 프로젝트 운영자의 눈으로 다시 본다. 둘은 결국 한 질문으로 모인다. **이 환경에서 우리가 가진 백엔드 직관 중 무엇이 그대로 살아남고, 무엇은 다시 짜야 하는가.**

## `this`는 정의 시점이 아니라 호출 시점에 결정된다

Java로 들어간 머리가 JS에서 처음 휘청이는 자리는 거의 예외 없이 `this`다. Java의 `this`는 인스턴스에 묶여 있다. 한 번 메서드를 정의하고 `obj.method()`로 부르든, 그 메서드 참조를 `Runnable`로 넘겨 다른 스레드가 부르든, `this`는 늘 그 인스턴스다. 컴파일러가 그렇게 보장한다.

JS는 다르다. 함수 안의 `this`는 **그 함수가 어떻게 호출됐느냐**에 따라 결정된다. 정의 시점이 아니라 호출 시점이다. 같은 함수가 어디에 붙어 호출되느냐에 따라 다른 객체를 가리킨다. 짧은 코드 한 토막을 보자.

```javascript
class UserService {
  constructor(prefix) {
    this.prefix = prefix;
  }

  greet(name) {
    console.log(`${this.prefix} ${name}`);
  }
}

const svc = new UserService("Hello,");
svc.greet("Toby");          // "Hello, Toby"  — this === svc

const fn = svc.greet;
fn("Toby");                 // TypeError 또는 "undefined Toby" — this === undefined

setTimeout(svc.greet, 100, "Toby");  // 같은 사고
```

`svc.greet("Toby")`는 우리가 기대한 그대로 동작한다. 그런데 `svc.greet`을 `fn`이라는 변수에 담아 부르거나 `setTimeout`에 넘기는 순간, 메서드 안의 `this`는 더 이상 `svc`가 아니다. 함수 객체만 따로 떼어졌고, 호출 시점에 그 함수에 붙은 객체가 없으니 `this`는 `undefined`(strict mode) 또는 전역 객체(sloppy mode)가 된다. Spring에서 `@Autowired`로 주입받은 빈의 메서드 참조를 다른 스레드로 넘긴다고 `this`가 사라지는 일은 없다. JS에서는 일어난다.

여기서 첫 번째 충격이 들어온다. "메서드를 변수에 담는다"는 동작은 Java의 `Runnable r = obj::method`와 다르지 않게 보인다. 그런데 결과는 정반대다. Java의 메서드 참조는 인스턴스를 함께 묶어 가지만, JS는 함수 객체와 호출 컨텍스트를 분리해 다룬다.

그렇다면 어떻게 다뤄야 할까. 이 모델을 받아들이고 두 가지 안전장치를 들이는 편이 낫다. 하나는 명시적으로 묶어 두기 — `const fn = svc.greet.bind(svc);` 처럼 `bind`로 컨텍스트를 박아 두는 방법. 다른 하나는 화살표 함수로 감싸기 — `setTimeout(() => svc.greet("Toby"), 100);`처럼 호출 표현식 자체가 `svc.greet(...)` 모양을 유지하게 하는 방법. 둘 다 "메서드를 떼어 보내지 말고, 호출 표현식을 그대로 옮긴다"는 발상이다.

## 화살표 함수가 잡아 주는 자리, 여전히 남는 함정

화살표 함수는 사실 `this` 문제를 절반쯤 정리해 주려고 들어온 문법이다. 일반 함수와 결정적으로 다른 점은, 화살표 함수가 자기 `this`를 새로 만들지 않는다는 것이다. 정의되는 시점에 둘러싸인 어휘적 스코프(lexical scope)의 `this`를 그대로 잡아 둔다. 그래서 클래스 메서드 안에서 콜백을 넘길 때 화살표 함수로 감싸면 `this`가 바깥 인스턴스를 가리킨다.

```typescript
class OrderProcessor {
  private logger: Logger;
  private orders: Order[];

  constructor(logger: Logger, orders: Order[]) {
    this.logger = logger;
    this.orders = orders;
  }

  // 함정: 메서드 참조를 그대로 넘긴다
  runWrong() {
    this.orders.forEach(this.process);   // this가 사라진다
  }

  // 안전: 화살표로 감싸 호출 표현식을 유지
  runRight() {
    this.orders.forEach((order) => this.process(order));
  }

  private process(order: Order) {
    this.logger.info(`processing ${order.id}`);  // runWrong이면 this === undefined
  }
}
```

`runWrong`을 부르면 `this.process` 자체는 함수 객체로 떼어지고, `forEach`가 그것을 호출할 때 `this`는 사라진다. 메서드 안의 `this.logger.info(...)`가 그대로 폭발한다. `runRight`처럼 화살표로 감싸 두면 `(order) => this.process(order)`에서의 `this`가 정의 시점의 어휘적 `this` — 즉 `OrderProcessor` 인스턴스 — 로 고정된다.

다만 화살표 함수가 모든 `this` 문제를 다 잡아 주는 건 아니다. 두 가지 함정이 남는다. 첫째, 클래스 메서드 자체를 화살표 함수로 정의해 버리면(`process = (order) => { ... }`) 인스턴스 필드가 되어 모든 인스턴스가 자기만의 함수 객체를 들고 다니게 된다. 메모리 측면에서 손해다. 작은 서비스에선 문제가 안 되지만, 다수의 인스턴스를 들고 다니는 자리에선 의도하고 써야 한다. 둘째, 라이브러리가 자체적으로 `this`를 바꿔 호출하는 자리(jQuery류의 콜백, Mocha의 `function() { this.timeout(...) }` 같은 자리)에선 화살표 함수가 오히려 자체 `this`를 막아 버려 라이브러리가 제공한 컨텍스트를 못 받는다.

정리하면 이렇다. **클래스 메서드 안에서 콜백을 넘길 때는 화살표 함수로 감싸 호출 표현식을 유지하라.** 라이브러리가 `this`를 통해 컨텍스트를 주입하는 자리에서는 일반 함수를 그대로 두라. 이 두 조건만 머리에 박아 두면 `this` 사고는 80% 정리된다.

한 가지 더 짚어 두자. NestJS·Express의 컨트롤러 메서드에서 이 함정이 잘 안 보이는 이유는, 프레임워크가 라우터에 핸들러를 등록할 때 인스턴스를 함께 묶어 주기 때문이다. Spring의 `@RequestMapping` 메서드가 호출자 입장에서 `this` 걱정 없이 도는 것과 같은 자리다. 그래서 단순한 라우트 처리만 하는 코드는 `this` 사고를 만나지 않는다. 함정은 한 발 떨어진 자리 — 우리가 직접 콜백을 넘기는 자리, 즉 `setInterval`·`Promise.then`·이벤트 emitter의 listener 등록·`Array.prototype.forEach` 같은 자리에서 등장한다. 이 점만 기억해 두면, "왜 NestJS에선 이 함정이 안 터지는데 직접 짠 코드에선 터지는가"라는 어색함이 자연스럽게 풀린다.

## 클로저와 `var`/`let` — Java `final` 캡처와 어디서 갈라지나

Java의 람다나 익명 클래스는 바깥 변수를 캡처할 때 한 가지 조건을 건다 — 그 변수는 사실상 `final`이어야 한다(effectively final). 컴파일러가 변수의 값을 캡처 시점에 박아 두는 모델이다. 한 번 잡힌 값은 변하지 않는다. 그래서 Java 출신은 클로저를 "스냅샷"으로 이해하기 쉽다.

JS는 변수의 값이 아니라 **변수 자체**를 캡처한다. 클로저 안에서 그 변수를 다시 보면, 그동안 값이 바뀌었을 수 있다. 여기에 `var`의 함수 스코프가 끼면 익숙한 함정이 등장한다.

```javascript
// 함정 — var의 함수 스코프
function buildHandlers() {
  const handlers = [];
  for (var i = 0; i < 3; i++) {
    handlers.push(() => console.log(i));
  }
  return handlers;
}

const hs = buildHandlers();
hs[0](); // 3
hs[1](); // 3
hs[2](); // 3
```

세 개의 핸들러가 모두 같은 `i`를 캡처한다. `var`로 선언된 `i`는 함수 스코프에 단 하나만 존재하고, 루프가 끝난 뒤 `i`는 3이 되어 있다. 클로저가 잡고 있는 건 그 단 하나의 `i`다. Java였다면 `i`는 effectively final이 아니므로 컴파일조차 안 된다. JS는 조용히 통과시키고, 호출 시점에 의도와 다른 값을 보여 준다. 찜찜한 자리다.

`let`이 들어오면서 이 함정은 거의 정리됐다. `let`은 블록 스코프이고, 매 반복마다 새 바인딩이 만들어진다.

```javascript
function buildHandlers() {
  const handlers = [];
  for (let i = 0; i < 3; i++) {
    handlers.push(() => console.log(i));
  }
  return handlers;
}

buildHandlers().forEach((h) => h()); // 0, 1, 2
```

이게 우리가 기대하는 동작이다. 그래서 권고는 단순하다 — **2026년 시점의 새 코드에 `var`를 쓸 이유는 사실상 없다. 기본은 `const`, 변경이 필요하면 `let`이다.** 이 한 줄로 클로저 사고의 절반은 막힌다.

`var`의 또 한 가지 함정은 호이스팅(hoisting)이다. 함수 어디서든 `var x`를 선언하면 그 선언은 함수 시작점으로 끌어올려진다. 선언 전에 사용해도 `undefined`로 잡힌다. `let`/`const`는 같은 선언이라도 "Temporal Dead Zone"에서 ReferenceError를 던진다. 모양이 비슷한데 의미가 다르다. `let` 일관 사용이 결국 자신을 지키는 길이다.

마지막으로, Java `final` 캡처와의 차이를 한 줄로 정리해 두자. **Java는 변수의 값을 정의 시점에 박는다. JS는 변수 자체를 가리키고, 사용 시점에 다시 본다.** 이 차이는 다음 절의 `Promise`·`async`/`await` 함정으로 그대로 이어진다.

## Promise·`async`/`await`의 함정 3종 — TS로 시연

`async`/`await`은 Java의 `CompletableFuture` 체인을 동기 코드처럼 보이게 정리해 준다는 점에서 강력한 도구다. `CompletableFuture.thenCompose`로 잇던 세 단계 비동기를 `await` 세 번으로 풀어 쓰면, 흐름이 위에서 아래로 흐른다. 좋다. 그런데 모양이 동기처럼 보인다는 사실이 가장 자주 데이는 함정의 출발점이다. **모양이 동기 같아 보이는 코드가 실제로는 비동기로 흩어진다는 점**을 잊으면 세 가지 사고가 줄지어 따라온다.

### 함정 1 — `forEach` 안의 `await`은 아무 일도 안 한다

```typescript
async function notifyAll(users: User[]): Promise<void> {
  users.forEach(async (user) => {
    await sendEmail(user);   // 각 user마다 비동기로 시작되지만,
  });                         // forEach는 결과를 기다리지 않는다
  console.log("done");        // 메일이 실제로 가기 전에 찍힌다
}
```

`Array.prototype.forEach`는 콜백의 반환값을 받지 않는다. 콜백을 `async`로 만들었으니 각각은 `Promise`를 반환하지만, `forEach`는 그걸 무시한다. 결과적으로 `notifyAll`은 메일 발송이 끝나기 전에 `console.log("done")`을 찍고 함수 자체도 즉시 resolve된다. 호출자가 `await notifyAll(users)`로 기다려도 메일은 아직 발송 중이다.

이 자리에서 가장 안전한 표현은 두 가지다. 직렬로 보내야 한다면 `for...of`로 돌리고, 병렬로 보내도 무방하면 `Promise.all` + `map`으로 묶는다.

```typescript
// 직렬: 외부 API rate limit이 있을 때
async function notifyAll(users: User[]): Promise<void> {
  for (const user of users) {
    await sendEmail(user);
  }
}

// 병렬: 서로 독립적일 때
async function notifyAll(users: User[]): Promise<void> {
  await Promise.all(users.map((user) => sendEmail(user)));
}
```

`forEach`에 `async` 콜백을 넘기는 패턴은, 보이는 모양은 자연스럽지만 실제로는 거의 항상 버그다. ESLint의 `no-misused-promises` 룰을 켜 두면 정적 단계에서 잡힌다.

### 함정 2 — 빠진 `Promise.all`로 직렬화되는 호출

두 번째 함정은 정반대 방향이다. 서로 무관한 비동기 호출 두 개를 차례로 `await`하면, 그 순간 둘은 직렬화된다.

```typescript
async function loadDashboard(userId: string): Promise<Dashboard> {
  const user = await fetchUser(userId);          // 200ms
  const orders = await fetchOrders(userId);      // 200ms
  const notifications = await fetchNotifications(userId); // 200ms
  return { user, orders, notifications };
}                                                 // 합계 ~600ms
```

이 코드는 동작한다. 결과도 맞다. 다만 600ms가 든다. 세 호출은 서로 의존하지 않는다. 사용자 정보를 받기 전에 주문을 못 가져올 이유가 없다. `Promise.all`로 묶어야 한다.

```typescript
async function loadDashboard(userId: string): Promise<Dashboard> {
  const [user, orders, notifications] = await Promise.all([
    fetchUser(userId),
    fetchOrders(userId),
    fetchNotifications(userId),
  ]);                                             // ~200ms
  return { user, orders, notifications };
}
```

이 함정은 IDE도 린터도 잡아 주지 않는다. 코드는 자연스럽고 컴파일도 된다. 그런데 응답 시간은 세 배가 된다. Spring `WebClient`의 `Mono.zip`이나 Kotlin 코루틴의 `awaitAll`이 풀던 자리와 정확히 같은 자리다. **`await`이 여러 줄 이어진다면, 줄 사이에 의존성이 진짜 있는지 한 번 의심해 보는 편이 낫다.**

### 함정 3 — 잡히지 않은 rejection이 프로세스를 죽인다

```typescript
async function processOrder(orderId: string) {
  const order = await loadOrder(orderId);
  await chargeCard(order);                  // 여기서 throw가 나면?
  await markAsPaid(order);
}

// 호출자
processOrder("o-123");  // 반환된 Promise를 받지도, await도 catch도 안 한다
```

`chargeCard`가 거절(rejection)되면, `processOrder`가 반환한 `Promise`는 거절 상태가 된다. 그런데 호출자가 그 `Promise`를 받지 않았다. `await`도 없고 `.catch`도 없다. 어디에서도 처리되지 않은 거절(unhandled rejection)이 된다. Node.js는 기본 정책상 `unhandledRejection`을 내고, 2026년 현재 LTS의 기본 동작은 프로세스를 종료시키는 쪽이다. 운영 사고로 가는 가장 흔한 경로 중 하나다.

이 자리에서 가장 안전한 패턴은 두 갈래다. fire-and-forget이 정말 의도라면 명시적으로 잡아 두기.

```typescript
processOrder("o-123").catch((err) => {
  logger.error({ err, orderId: "o-123" }, "process failed");
});
```

또는 호출자도 `async`라면 `await`을 잊지 않기. 그리고 한 번 더 안전판으로, 프로세스 레벨에서 `process.on("unhandledRejection", ...)` 핸들러를 둬 마지막 그물을 친다.

```typescript
process.on("unhandledRejection", (reason) => {
  logger.fatal({ reason }, "unhandled rejection");
  // 진단 로그를 충분히 남긴 뒤 종료시키는 게 일반적
});
```

이 세 함정 — `forEach` 안의 `await`, 빠진 `Promise.all`, 잡히지 않은 rejection — 은 한 번씩 데어 본 사람이라면 다 안다. 그런데 PR 리뷰에서 자주 미끄러진다. 9장에서 PR 리뷰 함정을 다시 모아 볼 때, 이 세 가지가 첫 줄에 다시 등장한다.

여기서 한 가지 안전판을 더 쌓아 두자. `tsconfig.json`의 `strict` 군과 ESLint의 `@typescript-eslint/no-floating-promises`, `@typescript-eslint/no-misused-promises` 두 룰을 켜 두면, 위 세 함정 중 절반은 컴파일·린트 단계에서 자동으로 잡힌다. `no-floating-promises`는 `Promise`를 반환하는 호출을 `await`이나 `.then`/`.catch`로 받지 않은 자리를 찾아낸다. `no-misused-promises`는 `forEach`나 `if` 같이 `Promise`를 받으면 안 되는 자리에 비동기 함수가 들어간 경우를 잡는다. Spring 진영의 `findbugs`·`SpotBugs`나 IntelliJ의 inspection 룰처럼, 정적 도구를 처음부터 켜 두는 편이 사고를 줄인다.

## Kotlin `suspend`와 JS `async`/`await` — 모양은 비슷, 실행 모델은 다르다

Kotlin을 함께 써 본 사람은 `suspend fun loadUser(): User`와 TS의 `async function loadUser(): Promise<User>`가 같은 일을 하는 두 표현이라 느낀다. 부르는 쪽도 비슷하다 — Kotlin에서는 `val user = loadUser()`(코루틴 스코프 안), TS에서는 `const user = await loadUser()`. 한 페이지에 양쪽을 나란히 두면 차이가 잘 보인다.

```kotlin
// Kotlin
suspend fun loadUser(id: String): User {
    val profile = userApi.fetchProfile(id)
    val prefs = settingsApi.fetchPrefs(id)
    return User(profile, prefs)
}

suspend fun loadUserParallel(id: String): User = coroutineScope {
    val profile = async { userApi.fetchProfile(id) }
    val prefs = async { settingsApi.fetchPrefs(id) }
    User(profile.await(), prefs.await())
}
```

```typescript
// TypeScript
async function loadUser(id: string): Promise<User> {
  const profile = await userApi.fetchProfile(id);
  const prefs = await settingsApi.fetchPrefs(id);
  return new User(profile, prefs);
}

async function loadUserParallel(id: string): Promise<User> {
  const [profile, prefs] = await Promise.all([
    userApi.fetchProfile(id),
    settingsApi.fetchPrefs(id),
  ]);
  return new User(profile, prefs);
}
```

표면 모양은 거의 동일하다. 그런데 실행 모델은 다르다.

Kotlin의 `suspend` 함수는 호출하는 그 자리에서 일을 시작하지 않는다. 정확히 말하면, 컴파일러가 `suspend` 함수를 상태 머신으로 바꿔 두고, 코루틴 컨텍스트에서 실행을 시작한 디스패처(`Dispatchers.IO`, `Dispatchers.Default` 등)가 어디서 일을 돌릴지를 결정한다. 함수 자체를 부른다고 작업이 시작되는 게 아니라, 코루틴 빌더(`launch`, `async`, `runBlocking`)가 시작 신호를 준다.

JS의 `async` 함수는 호출 즉시 실행을 시작한다. `loadUser(id)`라고만 적어도 그 줄에서 첫 동기 부분이 실행되고, 첫 `await`을 만나면 그 자리에서 micro-task로 양보한다. 반환된 `Promise`는 이미 진행 중인 작업의 핸들이다. 그래서 `loadUser(id)`라고 적고 변수에 담지 않으면, 작업은 떠나고 호출자는 그 결과를 받을 길이 없어진다.

이 차이는 두 가지 실무 결과로 이어진다. 첫째, Kotlin은 `coroutineScope`·`supervisorScope`로 구조적 동시성(structured concurrency)을 언어 차원에서 지원한다. 자식 작업의 실패가 어떻게 부모로 전파되는지, 부모가 취소되면 자식이 어떻게 함께 취소되는지가 모두 컴파일러와 런타임의 합의 안에 있다. JS의 `async`/`await`에는 이 개념이 빌트인되어 있지 않다. `AbortController`·`AbortSignal`로 비슷한 효과를 흉내 낼 수는 있지만, 라이브러리마다 지원이 들쭉날쭉하고, "한 묶음의 작업을 한 번에 취소" 같은 패턴은 직접 짜 줘야 한다. 둘째, Kotlin은 디스패처를 명시적으로 골라 작업이 어느 스레드에서 도는지를 통제한다. JS는 단일 스레드이니 그 선택지 자체가 없다 — 그래서 1장에서 본 "이벤트 루프를 막지 마라"가 그렇게 결정적인 권고가 된다.

Joffrey Bion의 정리가 정확하다 — **"Kotlin의 suspend는 JavaScript의 async가 아니다. JavaScript의 await에 가깝다."** Kotlin은 호출 시점에 양보(suspension)를 일으키고, JS는 호출 시점에 시작하고 `await` 시점에 양보한다. 모양만 보고 같은 도구라 단정하면, 구조적 동시성과 디스패처 같은 Kotlin의 무게추를 잃은 채 코드를 짜게 된다.

## 구조적 타입 vs 명목적 타입 — 자유와 위험이 같은 자리에

Java는 명목적(nominal) 타입 시스템이다. 두 클래스가 모양이 같아도, 한 쪽이 다른 쪽의 인터페이스를 `implements` 하지 않으면 다른 타입이다. `Comparator<String>` 자리에 `Comparator<String>` 시그니처와 똑같은 람다를 그냥 던지면 안 되고, 함수형 인터페이스로 명시적으로 변환되어야 한다. 컴파일러가 "당신이 이 인터페이스를 구현하기로 동의했나"를 묻고 들어간다.

TypeScript는 구조적(structural) 타입 시스템이다. 두 타입의 모양이 호환되면, 같은 타입으로 본다. `implements`는 코드의 의도를 분명히 적기 위한 도구일 뿐, 호환성의 필수 조건이 아니다.

```typescript
interface Logger {
  log(level: string, msg: string): void;
}

class ConsoleLogger {
  log(level: string, msg: string) {
    console.log(`[${level}] ${msg}`);
  }
}

function ship(logger: Logger) {
  logger.log("INFO", "shipped");
}

ship(new ConsoleLogger()); // OK — implements를 안 적어도 모양이 맞으면 통과
```

`ConsoleLogger`는 `Logger`를 `implements` 하지 않는다. 그런데 `Logger` 자리에 그대로 들어간다. 모양이 맞기 때문이다. 이 자유가 가져다주는 것이 두 가지 있다. 하나는 라이브러리 통합이 가벼워진다는 것 — 외부 라이브러리의 객체가 우리 인터페이스의 모양을 만족하면, 어댑터 클래스 없이 그냥 쓴다. 다른 하나는 테스트 더블이 단순해진다는 것 — Mock 라이브러리가 클래스 계층을 흉내 내지 않아도, 인터페이스 모양만 갖춘 객체로 충분하다.

그런데 같은 자유가 함정도 만든다.

```typescript
interface User {
  id: string;
  name: string;
}

interface Product {
  id: string;
  name: string;
}

function welcome(user: User) {
  console.log(`Welcome, ${user.name}`);
}

const product: Product = { id: "p-1", name: "Hat" };
welcome(product); // OK — 모양이 같으니 컴파일러는 통과시킨다
```

`User`와 `Product`는 의도가 전혀 다른 타입인데, 모양이 같으니 컴파일러가 같은 자리에 들어가는 것을 막지 않는다. Java라면 `User`와 `Product`는 별개의 클래스이므로, `welcome`에 `Product`를 넣는 일은 컴파일 단계에서 거부된다. TS에선 통과한다. 그리고 실제 운영에서 우리가 마주한 버그 중 적지 않은 비율이 이런 모양이다 — 같은 모양 다른 의도가 통과해 버려, 한참 지나서 잘못된 데이터가 한 자리를 침범한다.

이 함정을 메우는 대표적 패턴이 **branded types**(또는 nominal typing emulation)다.

```typescript
type UserId = string & { readonly __brand: "UserId" };
type ProductId = string & { readonly __brand: "ProductId" };

function makeUserId(s: string): UserId {
  return s as UserId;
}

function findUser(id: UserId) { /* ... */ }

const pid = "p-1" as ProductId;
findUser(pid); // 컴파일 에러 — 같은 string이지만 brand가 다르다
```

`__brand` 같은 가짜 필드를 끼워, 모양이 비슷한 타입에 억지로 명목성을 부여한다. 신원·금액·좌표처럼 헷갈리면 큰일 나는 자리에 자주 쓴다. 모든 타입에 일일이 brand를 박을 필요는 없지만, **같은 모양으로 헷갈릴 가능성이 큰 도메인 식별자에 한해 명목성을 손으로 회복하는 패턴은 알아 두는 편이 낫다.**

## TS 제네릭의 컴파일 타임 소거 — Java와 닮았지만 다르다

Java 출신이 가장 빨리 익숙해지는 자리가 TS 제네릭이다. `<T extends Foo>`로 상한을 두고, `<T, U>`로 두 개를 함께 잡고, `Map<K, V>` 모양의 컬렉션 타입을 정의한다. 모양이 거의 그대로다. 실행 시점에 타입이 사라진다는 사실까지 닮아 있다. Java는 type erasure로 런타임에 `List<String>`이 그냥 `List`가 된다. TS는 한 발 더 나아가서, 컴파일이 끝나면 타입 정보 자체가 JS에서 통째로 사라진다.

다만 닮은 만큼 다른 점도 있다. 두 가지를 짚어 두자.

첫째, Java의 type erasure는 JVM의 한계와 호환성 때문에 생긴 결과다. 런타임에 `instanceof List<String>` 같은 검사가 안 된다. TS는 그게 한계가 아니라 출발 가정이다. JS는 원래 동적 타입이고, TS는 그 위에 컴파일타임 검사를 얹은 도구다. 그래서 런타임에 타입을 알아야 하는 자리에선 다른 도구를 쓴다 — `class`의 `instanceof`, 라이브러리 차원의 런타임 검증(`zod`, `valibot`, `io-ts`). Spring에서 `Class<T>` 토큰을 들고 다니던 자리는 TS에서 schema 객체를 들고 다니는 자리로 바뀐다.

둘째, TS는 Java 제네릭이 제공하지 않는 두 가지 도구를 가지고 있다 — `keyof`와 조건부 타입(conditional types). 이 둘이 합쳐지면 데이터 변환의 타입을 정확히 표현할 수 있다.

```typescript
type Keys<T> = keyof T;

interface User {
  id: string;
  name: string;
  email: string;
}

type UserKeys = Keys<User>; // "id" | "name" | "email"

// 조건부 타입
type IsString<T> = T extends string ? true : false;
type A = IsString<"hello">; // true
type B = IsString<42>;      // false
```

`keyof`는 객체 타입의 키 집합을 유니온으로 뽑는다. `keyof User`가 `"id" | "name" | "email"`이 된다. 조건부 타입은 `T extends X ? A : B` 모양으로, 타입에 따라 다른 결과를 만든다. 이 둘을 합치면 다음 절의 유틸리티 타입들이 가능해진다.

## 유틸리티 타입 — Kotlin 데이터 클래스 + 리플렉션을 컴파일타임에

Kotlin에서 DTO를 다루던 사람은 데이터 클래스의 `copy(...)`나 리플렉션 기반 매핑에 익숙하다. "이 필드만 빼고 나머지는 그대로 복사", "이 필드들만 골라 입력 DTO로", "응답에서 비밀번호 빼기" 같은 작업을 데이터 클래스 + 리플렉션 또는 MapStruct로 풀어 왔다. TS는 같은 일을 **컴파일 타임에** 끝낸다.

`Partial<T>`, `Pick<T, K>`, `Omit<T, K>`, `Record<K, V>`, `ReturnType<F>` 같은 유틸리티 타입이 그 자리다. 이름은 단순하지만 실무에선 거의 매일 쓴다.

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  passwordHash: string;
  createdAt: Date;
}

// 입력 DTO — 새 사용자 생성 시 id·createdAt·passwordHash는 받지 않는다
type CreateUserInput = Omit<User, "id" | "createdAt" | "passwordHash">;

// 응답 DTO — 비밀번호 해시는 절대 노출하지 않는다
type UserResponse = Omit<User, "passwordHash">;

// 부분 수정 DTO — 모든 필드를 선택적으로
type UpdateUserInput = Partial<Omit<User, "id" | "createdAt" | "passwordHash">>;

// 좁힌 응답 — 목록 화면에서는 id와 name만
type UserListItem = Pick<User, "id" | "name">;
```

API 한 도메인의 DTO 군이 한 페이지에 정리된다. 도메인 모델 `User`를 단 한 번 정의하고, 입력·수정·응답·요약을 그것의 변환으로 표현한다. Kotlin에서 데이터 클래스 + 리플렉션 + MapStruct를 함께 굴리던 작업이, TS에서는 타입 표현 한 줄이 된다. 그리고 이 모든 게 컴파일이 끝나면 사라진다. 런타임 비용은 0이다.

여기에 `Record`와 `ReturnType`이 더해지면 도구가 한 단계 더 늘어난다.

```typescript
// Record — 키 집합과 값 타입으로 객체 형태를 만든다
type RoleConfig = Record<"admin" | "editor" | "viewer", { canEdit: boolean }>;

const roles: RoleConfig = {
  admin: { canEdit: true },
  editor: { canEdit: true },
  viewer: { canEdit: false },
};

// ReturnType — 함수의 반환 타입을 추출
async function fetchUser(id: string) {
  return { id, name: "Toby" };
}

type FetchUserResult = Awaited<ReturnType<typeof fetchUser>>;
// { id: string; name: string }
```

`Record`는 모든 키가 같은 형태의 값을 가지는 맵 타입을 정의한다. `ReturnType`과 `Awaited`를 묶으면 함수 시그니처에서 응답 타입을 자동 추출할 수 있다 — 함수의 응답 모양이 바뀌면 사용처의 타입이 따라 바뀐다. Spring에서 `ResponseEntity<T>`의 `T`를 손으로 동기화하던 자리가, TS에선 시그니처를 따라 자동으로 흐른다.

이 도구들은 한 번 익숙해지면 잘 안 떼어진다. **Kotlin 데이터 클래스로 잘 정의해 둔 DTO 그래프를, 별도 매퍼 없이 입력·수정·응답까지 컴파일타임에 짜낼 수 있다는 점이 TS의 가장 분명한 강점 중 하나다.** Java/Kotlin 출신이 TS에서 가장 빨리 "이건 좋다"고 느끼는 자리이기도 하다.

다만 한 가지 주의할 자리가 있다. 유틸리티 타입은 컴파일타임에만 존재하므로, 런타임 검증(들어온 JSON이 실제로 그 모양인지)은 별도 도구가 필요하다. 외부에서 들어온 데이터에 대해 `as User`로 단언만 하고 통과시키면, 컴파일러는 안심하지만 런타임은 그 단언을 검증하지 않는다. JSON에 `passwordHash`가 빠져 있어도, 우리가 `as User`로 강제했으니 코드는 그 사실을 모르고 흐른다. 이 자리를 메우는 표준 도구가 `zod`·`valibot` 같은 schema validator다. 한 schema에서 TS 타입과 런타임 검증을 함께 뽑아낸다.

```typescript
import { z } from "zod";

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  passwordHash: z.string(),
  createdAt: z.coerce.date(),
});

type User = z.infer<typeof UserSchema>;  // 위에서 정의한 인터페이스와 같은 모양

function parseUser(raw: unknown): User {
  return UserSchema.parse(raw);  // 검증 실패 시 throw
}
```

`UserSchema`에서 `User` 타입을 추론하므로, schema 한 곳을 고치면 타입과 검증이 함께 따라온다. Spring에서 Bean Validation(`@Valid`, `@NotBlank` 등) + Jackson 역직렬화 + DTO 클래스가 풀던 세 자리를 한 도구가 묶어 준다. **외부 경계(HTTP 요청 본문, 외부 API 응답, 메시지 큐 페이로드)에서는 unknown으로 받아 schema로 parse하고 들어와라.** 이 한 줄 합의가 운영 사고의 적지 않은 비율을 줄여 준다.

## 점진적 도입 — JS → JSDoc → `// @ts-check` → TS

이미 운영 중인 JS 코드베이스를 한꺼번에 TS로 옮기는 일은 거의 항상 실패한다. Spring/Kotlin 팀이 TS를 받아들일 때 안전한 길은 단계적이다. 네 단계로 끊어 가는 편이 낫다.

첫 단계는 **순수 JS**다. 새 코드를 그대로 짠다. 두 번째는 **JSDoc 주석으로 타입 표현**이다. 함수 시그니처에 `/** @param {string} id */` 같은 주석을 달아 둔다. 코드 자체는 JS이지만, IDE가 그 주석을 읽어 자동완성과 부분적 검사를 해 준다. 세 번째는 **`// @ts-check` 디렉티브**다. 파일 맨 위에 `// @ts-check` 한 줄을 박으면, TypeScript 컴파일러가 그 JS 파일을 검사 대상에 올려 JSDoc 타입을 진짜 타입처럼 검사한다. 빌드 결과는 그대로 JS이지만, 검사가 들어온다. 네 번째는 **`.ts` 파일로 점진 변환**이다. 새 모듈부터 `.ts`로 짜고, 기존 `.js`는 손이 닿을 때마다 같이 옮긴다.

이 단계가 안전한 이유는, 매 단계가 정상 동작하는 상태로 끝난다는 점이다. 어디서 멈춰도 시스템은 굴러간다. 한 번에 큰 PR로 옮기면 리뷰가 어렵고, 마이그레이션 중간에 다른 변경이 끼면 충돌이 폭발적으로 늘어난다. Spring에서 Kotlin으로 점진 전환하던 팀이 같은 길을 걸었다면, JS → TS도 같은 사고방식으로 가는 편이 안전하다.

`tsconfig.json`을 짤 때는 처음부터 `strict: true`를 켜라는 권고가 강하지만, 옮기는 중에는 `strict: false`로 출발해 모듈별로 strict로 올리는 점진 전략도 현실적이다. `noImplicitAny`, `strictNullChecks` 같은 개별 플래그를 한 번에 하나씩 켜는 식이다. 처음부터 strict로 박으면, 옮기는 동안 빌드가 깨져 진척이 멈춘다.

## 패키지 매니저와 monorepo — Maven 모듈 그래프의 자리

언어를 정리했으니 도구 쪽으로 옮겨 보자. JS 생태계의 의존성 운영은 Maven/Gradle과 사상이 다르다는 것부터 받아들이는 편이 낫다. 한 줄로 박으면 이렇다 — **Java 진영은 "한 빌드에 한 라이브러리는 한 버전"이고, JS 진영은 "각 패키지가 자기 의존성 트리를 따로 가질 수 있다"이다.**

Maven은 같은 라이브러리의 두 버전이 한 classpath에 올라오면 의존성 분쟁(conflict resolution) 알고리즘으로 하나만 고르고 다른 하나는 버린다. classpath는 단일하다. 그래서 dependency tree에 같은 라이브러리가 다섯 번 나오더라도 결과 jar에는 한 버전만 들어간다. 좋게 보면 일관성, 나쁘게 보면 가짜 호환성 — 우리가 직접 쓰는 라이브러리가 X 1.0을 요구해도 다른 라이브러리가 끌어온 X 2.0이 우선되어 런타임 ClassNotFoundException이 터지는 자리.

JS의 `node_modules`는 트리다. 같은 라이브러리의 두 버전이 한 프로젝트에 공존할 수 있다. 어떤 라이브러리는 `lodash@4.17.x`를 들고 자기 폴더에 두고, 다른 라이브러리는 `lodash@3.x`를 자기 폴더에 둔다. 둘이 충돌하지 않는다. 단점은 디스크 사용량과 호이스팅(hoisting)의 복잡성, 장점은 호환성 분쟁 자체가 잘 안 일어난다는 것이다. 같은 코드베이스 안에서 두 버전이 공존하는 사실은, Java 개발자에게 처음엔 거북하지만 곧 자연스러워진다.

### npm vs pnpm vs Bun

2026년 시점에 살아남은 패키지 매니저는 셋이다. `npm`, `pnpm`, 그리고 `Bun`(런타임 겸 매니저). yarn은 v1이 사실상 deprecated이고 yarn berry는 한쪽 길에 자리잡긴 했지만 새 프로젝트의 디폴트는 거의 셋 중 하나다. 차이를 정리하면 이렇다.

| 항목 | npm | pnpm | Bun |
|---|---|---|---|
| 설치 속도 | 중 | 빠름 | 매우 빠름 |
| 디스크 사용 | 큼(중복 복사) | 작음(content-addressable store + symlink) | 큼 |
| `node_modules` 구조 | flat hoisting | strict — 선언한 의존성만 보인다 | flat |
| Lockfile | `package-lock.json` | `pnpm-lock.yaml` | `bun.lockb`(바이너리) |
| 장점 | 표준, 어디서나 동작 | 디스크 절약, 유령 의존성 차단 | 속도, 통합 런타임 |
| 약점 | 가장 느린 편 | symlink 비호환 자리 가끔 | 생태계 호환성 일부 |

`npm`은 Node.js와 함께 따라오는 표준이고, 어디서나 동작하지만 가장 느린 편이다. `pnpm`이 만든 가장 큰 차이는 두 가지 — 첫째, 모든 패키지를 글로벌 store에 한 번만 받아 두고 프로젝트마다 symlink로 연결한다. 같은 라이브러리를 50개 프로젝트가 쓰면 디스크에 한 번만 들어간다. 둘째, `node_modules`를 strict하게 구성해서 `package.json`에 직접 선언한 의존성만 import 가능하다. npm의 flat hoisting은 의도치 않게 transitive 의존성까지 import 가능하게 만들고, 그 의존성이 다음 버전에서 빠지면 갑자기 빌드가 깨진다 — 이른바 phantom dependency 문제다. pnpm은 그걸 정직하게 막는다.

`Bun`은 런타임이자 매니저이자 번들러를 통합한 도구다. 패키지 설치 속도는 npm 대비 한 자릿수 배수로 빠르다. `Bun.serve` 같은 자체 HTTP 서버, 자체 JS 엔진(JavaScriptCore 기반) 등을 들고 있어 단순 매니저 이상의 야심을 품고 있다. 다만 2026년 시점에도 일부 라이브러리(특히 native addon이 있는 것들)와 호환성 이슈가 남아 있고, 운영 환경에서 Node.js를 통째로 대체하는 사례는 아직 보수적으로 봐야 한다. 9장에서 Bun과 Deno를 짧게 다시 본다.

권고를 한 줄로 정리하면 — **새 프로젝트는 `pnpm`을 디폴트로 두고, 사내 표준이 npm이라면 그대로 가도 큰 문제는 없다. Bun은 사이드 프로젝트나 빌드 도구로 먼저 들이고, 운영 런타임 교체는 충분한 검증 뒤에.**

### Lockfile은 버전 핀이 아니다 — 결정론(determinism)이다

Maven의 `pom.xml`에 적힌 버전은 그 자체로 핀이다. `1.2.3`이라 적으면 그 버전이 박힌다. JS의 `package.json`은 다르다 — `"^1.2.3"`처럼 적힌 범위(range)는 "1.2.3 이상이고 2.0.0 미만이라면 어느 minor·patch든 OK"라는 뜻이다. 같은 `package.json`으로 두 사람이 `npm install`을 해도, 한 사람은 `1.2.3`을 받고 다른 사람은 그 사이에 출시된 `1.5.0`을 받을 수 있다. 동일한 빌드라는 보장이 깨진다.

이 자리를 메우는 것이 lockfile이다. `package-lock.json`, `pnpm-lock.yaml`, `bun.lockb`는 **그 시점에 실제로 받은 정확한 버전과 트리 모양**을 박아 둔다. CI/CD와 다른 개발자의 머신 모두 lockfile에 박힌 그 트리를 그대로 받는다. CI에서는 `npm ci`(or `pnpm install --frozen-lockfile`) 로 lockfile을 따라가게 강제한다.

Java 진영의 직관과 비교하면, **lockfile은 사실상 Gradle의 dependency lock 파일과 같은 역할**을 한다. Maven에는 기본적으로 같은 메커니즘이 없고(플러그인을 따로 붙여야 한다), 그래서 JS 진영에서 처음 넘어온 사람은 lockfile을 git에 함께 넣어야 한다는 합의에 한 번씩 놀란다. 합의는 단순하다 — **lockfile은 git에 넣는다. CI는 `npm ci` 같은 결정론적 설치 명령을 쓴다. lockfile을 임의로 지우거나 무시하지 않는다.**

### Monorepo — npm/pnpm workspaces의 자리

Spring에서 Maven multi-module 또는 Gradle composite 빌드로 한 저장소에 여러 모듈을 함께 두는 패턴은 익숙하다. 부모 `pom.xml`이나 `settings.gradle.kts`에 자식 모듈을 등록하고, 자식끼리는 그룹·아티팩트 ID로 서로를 참조한다. `mvn install -pl module-a`로 한 모듈만 빌드하기도 한다.

JS 진영에서 같은 자리를 차지하는 것이 **workspaces**다. npm 7+, pnpm, yarn 모두 비슷한 모양으로 지원한다. 루트 `package.json`에 `"workspaces"` 필드를 두고, 자식 패키지 디렉터리들을 등록한다.

```json
// 루트 package.json
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

`packages/`에는 도메인 라이브러리들, `apps/`에는 실제 배포 단위(API 서버, BFF, 워커)가 들어간다. 자식들끼리는 `package.json`의 `"dependencies"`에 워크스페이스 이름을 적어 참조한다 — `"@my/core": "workspace:*"`처럼. `pnpm install`을 한 번 돌리면 모든 워크스페이스의 의존성이 한 번에 정리되고, 자식들끼리는 symlink로 연결된다.

여기서 한 단계 더 가면 **Turborepo**나 **Nx** 같은 빌드 그래프 도구가 들어온다. 이 도구들이 풀어 주는 문제는 두 가지다.

첫째, **변경된 패키지만 빌드·테스트한다.** 100개 패키지 중 두 개를 바꿨다면, 그 둘과 그 둘에 의존하는 패키지만 다시 돌린다. Gradle composite 빌드의 incremental + build cache와 같은 자리다.

둘째, **빌드 결과를 캐시한다.** 같은 입력(소스 + 의존성)에 대해 같은 출력이 나오므로, 한 번 빌드한 결과를 재사용한다. 로컬은 물론 CI에서도, 팀 단위 원격 캐시로도. Gradle의 build cache가 풀던 자리다.

| 비교축 | Maven multi-module | Gradle composite | npm/pnpm workspaces |
|---|---|---|---|
| 모듈 정의 | parent `pom.xml` + `<modules>` | `settings.gradle.kts` + `includeBuild` | 루트 `package.json` + `"workspaces"` |
| 자식간 참조 | groupId/artifactId | project(":module-a") 또는 composite | `"workspace:*"` |
| 부분 빌드 | `mvn -pl module-a` | `:module-a:build` + 의존 그래프 | `pnpm --filter @my/api build` |
| 빌드 캐시 | 없음(별도 도구) | 빌트인 build cache | Turborepo/Nx로 보강 |
| 의존성 lock | 별도 플러그인 | dependency-lock 옵션 | lockfile 표준 |

monorepo가 가져다주는 효과는 코드 공유와 atomic 변경이다. 한 BFF의 인터페이스가 바뀌었을 때, 그것을 쓰는 워커와 CLI까지 한 PR로 함께 고칠 수 있다. Spring 모듈 프로젝트에서 도메인 모듈이 바뀌었을 때 같은 자리에 PR을 모아 두던 경험이 있다면, JS workspaces도 같은 사고방식으로 받아들이면 된다.

다만 monorepo는 공짜가 아니다. 빌드 시간이 길어지고(그래서 Turborepo가 필요해지고), CI 캐시 전략이 서야 하고, 팀 간 코드 소유권이 명확해야 한다. 처음부터 monorepo로 가는 게 항상 옳은 건 아니다. **단일 저장소에 한 앱이 사는 단순한 구조로 시작하고, 두 번째 배포 단위가 생기는 시점에 workspaces를 들이는 편이 안전하다.** 7장의 CI/CD 절에서 monorepo의 GitHub Actions 캐시 전략을 다시 본다.

## 마무리

이 장은 두 갈래로 흘렀다. 앞쪽은 언어였다 — `this`는 호출 시점에 결정되고, 클로저는 변수 자체를 캡처하며, `forEach` 안의 `await`은 침묵하고, 빠진 `Promise.all`이 응답 시간을 세 배로 늘린다는 사실. Kotlin `suspend`와 JS `async`는 모양이 닮았지만 실행 모델은 갈라진다는 사실. 구조적 타입의 자유와 위험, 유틸리티 타입이 Kotlin 데이터 클래스 + 리플렉션의 자리를 컴파일타임에 채운다는 사실.

뒤쪽은 도구였다 — npm/pnpm/Bun 중 어느 것을 디폴트로 두느냐, lockfile이 결정론을 보장하는 핵심이라는 점, monorepo가 Maven multi-module/Gradle composite의 자리에서 어떻게 비슷하게, 어디서 다르게 풀리는지.

이 두 갈래가 합쳐지면, 우리는 손에 한 가지 작업 환경을 들고 있다 — TypeScript로 타입을 짜고, pnpm으로 의존성을 관리하고, lockfile로 결정론을 잡고, workspaces로 모듈 그래프를 구성하는 환경. **이제 이 환경 위에 어떤 패턴으로 백엔드를 짜야 하는지를 살펴볼 차례다.** Spring 진영에서 익숙했던 도구들 — MVC·Batch·WebFlux·Cloud Function — 의 자리에 Node 진영은 무엇을 두고 있는가. 다음 장에서 활용 패턴의 지형을 그려 보자.
