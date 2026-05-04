# 6장. 이 도메인을 어떻게 모델링할까 — 구조적 타입 위에서 잃지 않는 법

Java 백엔드를 몇 년 짠 사람이 처음으로 TypeScript 코드베이스에 들어왔다고 상상해보자. 코드를 읽다가 뭔가 찜찜한 순간이 온다.

```ts
function createOrder(userId: string, productId: string, amount: number) {
  // ...
}
```

Java였다면 `UserId`, `ProductId`라는 별도 타입이 있거나, 적어도 `@NotNull @Size(min=36, max=36) String userId`처럼 Bean Validation이 붙어 있었을 것이다. 그런데 TS 코드에는 그냥 `string`이다. *"이게 맞나? 실수로 userId 자리에 productId를 넣으면 어떻게 되지?"*

더 난감한 건 다음을 발견했을 때다.

```ts
const userId = getUserId();
const productId = getProductId();

// 아무도 에러를 안 낸다
createOrder(productId, userId, 100);
```

컴파일러는 침묵한다. `string`과 `string`은 호환된다. 도메인의 안전망이 그냥 뚫려 있다.

이건 TS의 결함이 아니다. **구조적 타입 시스템**이 가져오는 필연적인 헐거움이다. Java가 명목 타입으로 이것을 막는다면, TS는 다른 방법으로 막아야 한다. 그리고 그 방법은 존재한다 — 커뮤니티가 수년에 걸쳐 정착시킨 표준 패턴들이 있다.

이 장에서 살펴볼 것들은 사실 모두 한 주제로 연결된다. **"TS의 구조적 타입 위에서 도메인 안전성을 어떻게 회복하는가."** `interface`와 `type`의 선택, branded type, enum 대신 union literal, immutability 전략 — 이 모든 것이 같은 질문에 대한 답이다. 그리고 마지막에는 그 질문의 가장 중요한 변주를 다룬다. **"에러를 도메인의 일부로 모델링할 수 있는가."** Java에서 checked exception을 통해 해결하려 했던 그것을, TS에서는 어떻게 접근하는지.

---

## 6.1 데이터 구조를 표현하는 두 도구 — `interface`와 `type alias`

도메인 모델링의 첫 번째 질문은 단순하다. 데이터 구조를 어떻게 표현할 것인가.

Java라면 `class`가 있다. Kotlin이라면 `data class`가 있다. TS에는 두 가지가 있다. `interface`와 `type alias`. 그리고 둘 다 있다고 해서 어느 것을 써야 하는지 명확한 합의가 있는 건 아니라서, 처음에 조금 당황스럽다.

### interface — 객체의 형태를 선언한다

```ts
interface User {
  id: string;
  email: string;
  name: string;
}

interface Order {
  id: string;
  userId: string;
  amount: number;
  createdAt: Date;
}
```

자연스럽다. Java의 인터페이스와 비슷하게 생겼고, 객체의 *형태(shape)*를 선언한다. TS에서 `interface`는 주로 이 용도다.

### type alias — 타입에 이름을 붙인다

```ts
type UserId = string;
type Status = "pending" | "fulfilled" | "cancelled";
type Point = { x: number; y: number };
type MaybeUser = User | null;
```

`type`은 어떤 타입 표현식에도 이름을 붙일 수 있다. primitive, union, intersection, 함수 타입, 튜플 타입 — 모두 `type`으로 이름을 붙일 수 있다. `interface`는 그렇지 않다. `interface Status = "pending" | "fulfilled"`는 문법 에러다.

### 둘의 차이 — 가장 중요한 것들만

`interface`와 `type`의 차이를 낱낱이 비교하다 보면 지치기 쉽다. 실무에서 정말 중요한 차이 두 가지만 짚어보자.

**첫째, `type`은 union과 intersection을 직접 표현할 수 있고 `interface`는 아니다.**

```ts
// type만 가능
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
type Shape = Circle | Square | Triangle;
```

**둘째, `interface`는 선언 병합(declaration merging)이 된다.**

```ts
interface Config {
  host: string;
}

// 나중에 같은 이름으로 다시 선언하면 합쳐진다
interface Config {
  port: number;
}

// Config는 이제 { host: string; port: number }
const config: Config = { host: "localhost", port: 3000 };
```

이게 `interface`의 독특한 능력이다. 라이브러리를 *보강(augment)*할 때 쓴다. Express의 `Request` 타입에 `currentUser` 속성을 추가하고 싶다면, `interface`로 그것을 선언하면 자동으로 병합된다. `type`으로는 이걸 할 수 없다.

### 그렇다면 언제 무엇을 쓸까

커뮤니티에서 오래 논쟁이 있었다. 결론은 생각보다 실용적이다.

- **객체 형태를 표현할 때**: 어느 것이든 동작한다. 팀의 스타일을 따르면 된다.
- **union, intersection, 함수 타입에 이름을 붙일 때**: `type`만 가능하니 `type`을 쓴다.
- **라이브러리 확장(augmentation)**: `interface`를 써야 한다.
- **React 컴포넌트 Props, 함수 인자**: `interface`를 쓰는 팀이 많다. 선언 병합 덕분에 나중에 보강하기 쉽다.
- **도메인 모델의 복잡한 대수적 타입**: `type`이 자연스럽다.

"그러니까 뭘 써야 해요?" 라고 묻는다면, 솔직히 말해서 실무에서 그 차이가 문제가 될 일은 생각보다 드물다. 중요한 건 팀 안에서 일관성이다. "객체 형태는 `interface`, 그 외에는 `type`" 이라는 규칙을 정해두면 대부분의 상황이 해결된다.

가끔 처음 TS를 접한 팀에서 "우리 팀은 `interface`만 쓰기로 했어요"라든가 "저희는 `type`으로 통일했어요" 같은 이야기를 한다. 그것도 나쁘지 않다. 하지만 `interface`만 쓰기로 했다면 union을 표현할 때 조금 어색해진다. 예를 들어 `interface Shape`를 만들고 싶은데 `Circle | Square` 형태를 `interface`로는 직접 표현할 수 없어서, 결국 `type`을 꺼내 들게 된다.

한 가지 덧붙이자면, TypeScript 공식 핸드북은 오랫동안 "가능하면 `interface`를 쓰고, 필요한 경우에만 `type`을 써라"는 권고를 유지했다. 그 이유는 IDE의 에러 메시지 표현에서 `interface`가 더 읽기 좋았기 때문이다. 최근 버전에서는 이 차이가 많이 좁혀졌지만, 레거시 코드베이스에서 이 권고를 따른 흔적을 자주 보게 된다. 맥락을 알면 낯설지 않다.

물론 `interface`와 `type`을 *동시에* 쓸 수도 있다. 겁낼 필요 없다. 실제 코드에서는 둘이 섞여 있는 경우가 더 많다.

```ts
interface UserBase {
  id: string;
  email: string;
}

type AdminUser = UserBase & {
  role: "admin";
  permissions: string[];
};

type RegularUser = UserBase & {
  role: "user";
};

type User = AdminUser | RegularUser;
```

`interface`로 기반을 정의하고, `type`으로 변형·조합하는 패턴이다. 두 개가 사이좋게 공존한다.

---

> **📚 Java/Kotlin 시선 — `data class`/`copy()` ↔ TS `interface` + spread**
>
> Kotlin의 `data class`는 도메인 모델링의 핵심이다. 불변 필드, 자동 생성되는 `equals`/`hashCode`/`toString`, 그리고 `copy()`가 있다.
>
> ```kotlin
> data class User(val id: String, val email: String, val name: String)
>
> val user = User("u1", "alice@example.com", "Alice")
> val updated = user.copy(name = "Alicia")
> ```
>
> TS에는 이에 정확히 대응하는 것이 없다. `interface`는 구조만 선언한다. `equals`는 TS/JS에서 `===`가 참조 동등성이라 객체끼리는 직접 비교가 안 된다. `copy()`는 spread로 흉내 낸다.
>
> ```ts
> interface User {
>   id: string;
>   email: string;
>   name: string;
> }
>
> const user: User = { id: "u1", email: "alice@example.com", name: "Alice" };
> const updated: User = { ...user, name: "Alicia" };
> ```
>
> Kotlin의 `copy()`와 거의 같다. 단, 컴파일러가 강제하지 않는다. `{ ...user, nonExistentField: "x" }` 도 에러 없이 동작한다(초과 속성 검사는 리터럴 할당 시점에만 작동). `equals`에 해당하는 깊은 비교가 필요하면 `deep-equal` 같은 라이브러리를 따로 쓰거나, 직접 구현해야 한다.
>
> **결론**: TS의 `interface` + spread가 `data class`의 *흉내*는 낼 수 있지만, 컴파일러 수준의 강제력은 훨씬 약하다. 이것이 TS 도메인 모델링이 Java/Kotlin보다 더 *규율*이 필요한 이유 중 하나다.

---

## 6.2 구조적 타입의 헐거움 — 왜 `type UserId = string`으로는 부족한가

다시 처음의 문제로 돌아오자.

```ts
type UserId = string;
type ProductId = string;

function createOrder(userId: UserId, productId: ProductId) { /* ... */ }

const uid: UserId = "user-123";
const pid: ProductId = "prod-456";

// 이게 통과된다
createOrder(pid, uid);  // userId에 ProductId를, productId에 UserId를 넣었다
```

`type UserId = string`은 그냥 `string`의 별명이다. TS는 구조적으로 호환 여부를 판단하는데, `string`과 `string`은 당연히 호환된다. `UserId`와 `ProductId`는 컴파일러 눈에 아무 차이가 없다.

Java라면 이것이 컴파일 에러다. `UserId`와 `ProductId`가 다른 클래스이기 때문이다. TS에서는 이런 명목 타입이 기본적으로 없다.

그렇다면 어떻게 해야 할까?

### Branded type — 구조적 타입 위에서 명목 타입을 흉내내다

커뮤니티가 수년에 걸쳐 정착시킨 패턴이 있다. **Branded type** 또는 **nominal trick**이라고 부른다.

```ts
type UserId = string & { readonly _brand: unique symbol };
type ProductId = string & { readonly _brand: unique symbol };
```

`unique symbol`이 핵심이다. TS에서 `unique symbol`은 선언마다 고유한 타입을 만든다. 두 `unique symbol`은 서로 다른 타입이다. 그래서 `UserId`와 `ProductId`는 구조적으로 *다른* 타입이 된다.

실제로 실험해보자.

```ts
declare const _userId: unique symbol;
declare const _productId: unique symbol;

type UserId = string & { readonly _brand: typeof _userId };
type ProductId = string & { readonly _brand: typeof _productId };

function createOrder(userId: UserId, productId: ProductId) {
  // ...
}

const uid = "user-123" as UserId;
const pid = "prod-456" as ProductId;

createOrder(uid, pid);   // OK
createOrder(pid, uid);   // 컴파일 에러! Type 'ProductId' is not assignable to type 'UserId'
```

이제 순서가 바뀌면 컴파일러가 잡아낸다.

### 더 짧고 실용적인 선언 방법

`declare const _userId: unique symbol`을 매번 쓰는 건 번거롭다. 더 일반적으로 쓰이는 패턴은 다음과 같다.

```ts
declare const brand: unique symbol;

type Brand<T, B> = T & { readonly [brand]: B };

type UserId = Brand<string, "UserId">;
type ProductId = Brand<string, "ProductId">;
type OrderId = Brand<string, "OrderId">;
type Amount = Brand<number, "Amount">;
```

`Brand<T, B>` 헬퍼 타입 하나로 모든 branded type을 만들 수 있다. `B` 자리에 문자열 리터럴을 넣어서 구분한다.

### Brand를 만드는 함수 — 생성 지점에서 검증

Branded type의 값을 만드려면 타입 단언(`as`)이 필요하다. 그냥 `"user-123" as UserId`라고 쓸 수 있지만, 이러면 아무 값이나 `UserId`로 만들 수 있어서 취지가 반감된다.

더 나은 방법은 생성 함수(constructor function)를 만드는 것이다.

```ts
function makeUserId(value: string): UserId {
  if (!value.startsWith("user-")) {
    throw new Error(`Invalid UserId: ${value}`);
  }
  return value as UserId;
}

function makeOrderAmount(value: number): Amount {
  if (value <= 0 || !Number.isFinite(value)) {
    throw new Error(`Invalid Amount: ${value}`);
  }
  return value as Amount;
}
```

이제 `UserId`를 만들려면 반드시 `makeUserId()`를 통해야 한다. 검증 없이 `"user-123" as UserId`라고 쓸 수는 있지만, 코드 리뷰에서 `as`는 주의 신호다 — 5장에서 다룬 `as`의 윤리가 여기서도 적용된다. 팀 컨벤션으로 "branded type 생성은 반드시 maker 함수를 거칠 것"이라고 정하면 된다.

### zod와의 결합

앞서 5장에서 봤듯이 zod는 스키마로부터 타입을 유도한다. branded type과 자연스럽게 결합된다.

```ts
import { z } from "zod";

const UserIdSchema = z.string().uuid().brand<"UserId">();
const ProductIdSchema = z.string().uuid().brand<"ProductId">();

type UserId = z.infer<typeof UserIdSchema>;
type ProductId = z.infer<typeof ProductIdSchema>;

// 외부 입력을 검증하면서 branded type을 만든다
function parseUserId(input: unknown): UserId {
  return UserIdSchema.parse(input);
}
```

`z.string().uuid().brand<"UserId">()`는 UUID 형식인지 검증하고, branded type으로 만들어 반환한다. 외부 경계에서 검증과 브랜딩이 동시에 이루어진다.

### Effect-ts와 토스의 사례

Effect-ts는 TS 생태계에서 가장 정교한 함수형 프레임워크 중 하나인데, 여기서도 branded type을 핵심 패턴으로 채택한다.

```ts
import { Brand } from "effect";

type UserId = string & Brand.Brand<"UserId">;
const UserId = Brand.nominal<UserId>();

const uid = UserId("user-123");  // 유효한 UserId 생성
```

토스(Viva Republica)도 내부적으로 비슷한 패턴을 쓴다. 금융 도메인에서 `UserId`, `AccountId`, `TransactionId` 같은 식별자가 뒤섞이는 건 실제로 버그를 유발하는 실수다. Branded type은 이것을 컴파일 타임에 막는다.

---

> **🚧 함정 — 구조적 타입의 헐렁함**
>
> `type UserId = string`이라고 선언하는 순간, TS 컴파일러 눈에 `UserId`와 `string`은 완전히 같다. 나아가 `type ProductId = string`도 선언하면 `UserId`와 `ProductId`도 서로 완전히 같다.
>
> ```ts
> type UserId = string;
> type ProductId = string;
>
> const uid: UserId = "u1";
> const pid: ProductId = uid;  // 에러 없음! UserId를 ProductId에 할당 가능
> ```
>
> Java/Kotlin 개발자에게 이건 충격이다. 다른 이름의 타입이 *같은* 타입이라니. 처음에는 "그냥 가독성을 위한 타입 별명이구나" 하고 넘어가지만, 나중에 `createOrder(pid, uid)`처럼 순서가 바뀌어도 컴파일러가 침묵하는 버그를 만나고 나서야 체감한다.
>
> **처방**: Brand type. 도메인 식별자가 섞일 위험이 있는 곳에는 `Brand<string, "UserId">` 형태를 쓰자. 처음에는 번거롭다고 느껴질 수 있지만, 실제 버그를 한 번 겪고 나면 자연스럽게 채택하게 된다. 특히 금융·의료·물류처럼 식별자가 여러 종류 있고 순서 실수가 치명적인 도메인에서는 표준 패턴이다.

---

> **📚 Java/Kotlin 시선 — Kotlin `value class` ↔ Branded type**
>
> Kotlin에는 `value class`(과거 이름 inline class)가 있다. 런타임 오버헤드 없이 명목 타입을 만든다.
>
> ```kotlin
> @JvmInline
> value class UserId(val value: String)
> @JvmInline
> value class ProductId(val value: String)
>
> fun createOrder(userId: UserId, productId: ProductId) { /* ... */ }
>
> val uid = UserId("user-123")
> val pid = ProductId("prod-456")
>
> createOrder(pid, uid)  // 컴파일 에러! Type mismatch
> ```
>
> 둘 다 zero-cost wrapper다. 런타임에는 감싼 값 자체처럼 동작한다(`UserId`는 그냥 `String`으로). 그런데 **강제 메커니즘이 다르다**.
>
> Kotlin `value class`는 언어 수준에서 강제한다. `UserId`와 `ProductId`는 진짜 다른 타입이다. 생성자를 호출하지 않고는 만들 수 없다.
>
> TS branded type은 타입 시스템의 트릭이다. `"user-123" as UserId`라고 쓰면 컴파일러를 속일 수 있다. 강제하려면 팀 컨벤션이 필요하다 — "직접 `as`로 branded type을 만들지 말고, maker 함수를 써라." 코드 리뷰 문화가 보완재가 된다.
>
> 이 차이가 작아 보이지만, 도메인 안전성에 대한 두 언어의 철학적 거리를 보여준다. Kotlin은 언어가 보장하고, TS는 팀이 보장한다.

---

## 6.3 enum의 함정과 union literal의 우위

Java 개발자에게 `enum`은 익숙한 도구다. 그리고 TS에도 `enum`이 있다. 처음에는 반가울 것이다.

```ts
enum OrderStatus {
  Pending = "PENDING",
  Fulfilled = "FULFILLED",
  Cancelled = "CANCELLED",
}
```

그런데 TS의 `enum`은 커뮤니티에서 뜨거운 논쟁의 대상이다. 결론부터 말하면, **많은 TS 전문가들이 `enum` 사용을 자제하고 union literal을 권장한다**. 왜일까.

### TS enum의 문제들

**첫 번째 문제: 런타임 객체가 생성된다.**

TS의 타입은 컴파일 후 지워진다. 그런데 `enum`은 예외다. 컴파일하면 실제 JS 코드가 만들어진다.

```ts
// TS
enum OrderStatus {
  Pending = "PENDING",
  Fulfilled = "FULFILLED",
}

// 컴파일 결과 JS
var OrderStatus;
(function (OrderStatus) {
  OrderStatus["Pending"] = "PENDING";
  OrderStatus["Fulfilled"] = "FULFILLED";
})(OrderStatus || (OrderStatus = {}));
```

이 런타임 코드는 번들에 포함된다. 작은 것처럼 보이지만 tree-shaking이 잘 안 되고, 번들 크기에 미묘하게 영향을 준다.

**두 번째 문제: 숫자형 enum의 역방향 매핑.**

문자열 enum은 그나마 낫지만, 숫자형 enum은 진짜 함정이다.

```ts
enum Direction {
  Up,    // 0
  Down,  // 1
  Left,  // 2
  Right, // 3
}

Direction[0]         // "Up" — 역방향 매핑이 자동 생성된다
Direction["Up"]      // 0
Direction[Direction.Up]  // "Up"
```

숫자형 enum은 키에서 값으로, 값에서 키로 양방향 조회가 된다. 타입 안전성이 약해진다.

```ts
function setDirection(dir: Direction) { /* ... */ }

setDirection(999)  // 에러 없음! 범위 밖의 숫자가 들어가도 통과
```

**세 번째 문제: `const enum`의 ambient 함정.**

`const enum`은 런타임 코드를 안 만들고 인라인으로 치환하지만, 다른 파일에서 `import`해서 쓸 때 `isolatedModules` 모드에서 에러가 난다. Babel, esbuild, swc는 파일을 개별 변환하므로 `const enum`의 인라인을 수행하지 못한다. 실무에서 번들러를 쓰면 `const enum`은 지뢰가 된다.

### union literal — 가볍고 투명하다

같은 것을 union literal로 표현해보자.

```ts
type OrderStatus = "pending" | "fulfilled" | "cancelled";

function processOrder(status: OrderStatus) {
  switch (status) {
    case "pending":
      return "대기 중";
    case "fulfilled":
      return "완료";
    case "cancelled":
      return "취소";
    default:
      const _exhaustive: never = status;  // 놓친 케이스가 있으면 컴파일 에러
      return _exhaustive;
  }
}
```

컴파일 후 남는 런타임 코드가 없다. 그냥 문자열 비교다. Tree-shaking도 자연스럽게 된다.

타입 좁히기도 자연스럽다.

```ts
type Order = {
  id: string;
  status: OrderStatus;
  amount: number;
};

function cancelOrder(order: Order): Order {
  if (order.status !== "pending") {
    throw new Error("pending 상태에서만 취소할 수 있다");
  }
  return { ...order, status: "cancelled" };
}
```

**discriminated union**으로 더 풍부한 상태를 표현할 수 있다.

```ts
type Order =
  | { status: "pending"; id: string; amount: number }
  | { status: "fulfilled"; id: string; amount: number; fulfilledAt: Date }
  | { status: "cancelled"; id: string; amount: number; cancelledAt: Date; reason: string };

function describeOrder(order: Order): string {
  switch (order.status) {
    case "pending":
      return `주문 ${order.id} 대기 중`;
    case "fulfilled":
      return `주문 ${order.id} ${order.fulfilledAt.toLocaleDateString()} 완료`;
    case "cancelled":
      return `주문 ${order.id} 취소 (사유: ${order.reason})`;
  }
}
```

각 상태마다 다른 필드를 가질 수 있다. `fulfilled` 상태에는 `fulfilledAt`이, `cancelled` 상태에는 `cancelledAt`과 `reason`이 있다. TS 컴파일러는 `switch`에서 `status`로 좁히면, 해당 분기에서 그 상태의 고유 필드에 접근할 수 있음을 안다.

이것이 Kotlin의 `sealed class` + `when`에 가장 가까운 TS 패턴이다.

### enum을 완전히 피해야 하는가

꼭 그런 건 아니다. 문자열 enum을 신중하게 쓰면 문제가 없는 경우도 있다. 특히 외부 API와 교환하는 값에 의미 있는 이름을 붙이고 싶을 때, 타입 안전성과 런타임 객체 둘 다 필요한 경우라면 문자열 enum도 선택지다.

단, **새 프로젝트를 시작할 때 디폴트는 union literal**이라고 보는 편이 낫다. 나중에 필요하다면 enum으로 옮기는 건 어렵지 않다.

---

> **📚 Java/Kotlin 시선 — Java `enum class` ↔ union literal**
>
> Java의 `enum`은 강력하다. 메서드, 필드, 생성자를 가질 수 있고, `switch`에서 exhaustive check가 된다(Java 14+ switch expression).
>
> ```java
> public enum OrderStatus {
>     PENDING("대기"),
>     FULFILLED("완료"),
>     CANCELLED("취소");
>
>     private final String label;
>     OrderStatus(String label) { this.label = label; }
>     public String getLabel() { return label; }
> }
>
> // 사용
> String result = switch (status) {
>     case PENDING -> status.getLabel();
>     case FULFILLED -> status.getLabel();
>     case CANCELLED -> status.getLabel();
> };
> ```
>
> Kotlin의 `enum class`도 비슷하다. 거기에 더해 `sealed class`로 각 케이스가 다른 데이터를 가질 수 있다.
>
> ```kotlin
> sealed class Order {
>     data class Pending(val id: String, val amount: Int) : Order()
>     data class Fulfilled(val id: String, val amount: Int, val fulfilledAt: LocalDate) : Order()
>     data class Cancelled(val id: String, val amount: Int, val reason: String) : Order()
> }
>
> fun describe(order: Order) = when (order) {
>     is Order.Pending -> "대기"
>     is Order.Fulfilled -> "완료: ${order.fulfilledAt}"
>     is Order.Cancelled -> "취소: ${order.reason}"
> }
> ```
>
> TS의 discriminated union이 이것을 흉내 낸다. `kind`(또는 `status`, `type`) 필드가 `is` 연산자 역할을 한다. `switch`에서 `never`로 exhaustive check까지 구현하면 Kotlin `when`의 안전성과 거의 같다.
>
> 차이점: TS union의 각 케이스는 메서드를 가질 수 없다. 데이터만 들어 있다. 메서드가 필요하면 함수를 따로 만들어 매칭하는 방식을 쓴다. 이것이 객체지향 스타일과 함수형 스타일의 경계점이기도 하다.

---

## 6.4 불변성 — `readonly`에서 `as const`까지

Java에서 `final`, Kotlin에서 `val`로 불변성을 표현한다. TS에는 여러 도구가 있다. 각각의 역할과 한계를 알아보자.

### `readonly` — 속성을 읽기 전용으로

```ts
interface Config {
  readonly host: string;
  readonly port: number;
}

const config: Config = { host: "localhost", port: 3000 };
config.host = "newhost";  // 컴파일 에러
```

`readonly`는 해당 속성을 수정 못 하게 막는다. Kotlin의 `val`과 같은 수준이다. 단, **얕은(shallow) 불변성**이다.

```ts
interface DeepConfig {
  readonly db: {
    host: string;
    port: number;
  };
}

const config: DeepConfig = { db: { host: "localhost", port: 5432 } };
config.db = { host: "other", port: 5432 };  // 컴파일 에러 — db 자체는 바꿀 수 없다
config.db.host = "other";  // 가능! db.host는 readonly가 아니다
```

`readonly db`는 `db` 속성의 재할당을 막지만, `db` 내부의 `host`나 `port`는 막지 않는다.

### `Readonly<T>` — 모든 속성을 얕게 읽기 전용으로

```ts
interface User {
  id: string;
  email: string;
  name: string;
}

type ReadonlyUser = Readonly<User>;
// { readonly id: string; readonly email: string; readonly name: string }
```

`Readonly<T>`는 T의 모든 속성에 `readonly`를 붙인다. 편리하지만 역시 얕다. 중첩 객체의 내부는 막지 않는다.

### `as const` — 리터럴 타입으로 굳힌다

`as const`는 다르다. 값 전체를 가장 좁은 리터럴 타입으로 굳힌다.

```ts
const config = {
  host: "localhost",
  port: 3000,
  db: {
    name: "mydb",
    pool: 5,
  }
} as const;

// config의 타입은:
// {
//   readonly host: "localhost";
//   readonly port: 3000;
//   readonly db: {
//     readonly name: "mydb";
//     readonly pool: 5;
//   }
// }
```

모든 속성이 `readonly`가 되고, 값이 구체적인 리터럴 타입으로 좁혀진다. `host`의 타입이 `string`이 아니라 `"localhost"` 리터럴이다. 중첩 객체도 재귀적으로 처리된다.

`as const`는 런타임 동작을 바꾸지 않는다. 타입 정보만 바꾼다. 상수 테이블, 설정 객체, 고정된 열거형 데이터를 표현할 때 매우 유용하다.

```ts
const ROUTES = {
  home: "/",
  profile: "/profile",
  settings: "/settings",
} as const;

type Route = typeof ROUTES[keyof typeof ROUTES];
// Route = "/" | "/profile" | "/settings"

function navigate(route: Route) {
  window.location.href = route;
}

navigate("/profile");    // OK
navigate("/unknown");   // 컴파일 에러
```

enum 대신 `as const`로 상수 집합을 만들고, `typeof ROUTES[keyof typeof ROUTES]`로 값 타입을 뽑는 패턴이다. 이것이 enum의 런타임 부담 없이 같은 효과를 낸다.

### `Object.freeze()` — 런타임 불변성

앞의 것들은 모두 컴파일 타임 보호다. 런타임에서도 객체를 정말로 불변으로 만들려면 `Object.freeze()`를 써야 한다.

```ts
const DEFAULTS = Object.freeze({
  timeout: 5000,
  retries: 3,
  host: "localhost",
});

DEFAULTS.timeout = 9999;  // 런타임 에러 (strict mode에서)
                           // 혹은 조용히 무시된다
```

단, `Object.freeze()`도 얕다. 중첩 객체까지 완전히 얼리려면 재귀적으로 적용해야 한다. 그리고 TS 타입 시스템은 `Object.freeze()`의 반환 타입을 `Readonly<T>`로 추론하므로, 타입 수준에서도 보호된다.

### 불변성 도구의 위계 정리

```
Object.freeze()   — 런타임 불변성 (얕음)
as const          — 컴파일 타임, 리터럴로 굳힘, 재귀적 readonly
Readonly<T>       — 컴파일 타임, 얕은 readonly
readonly (속성)   — 컴파일 타임, 개별 속성
```

실무에서 가장 많이 쓰는 건 `readonly`와 `as const`다. 깊은 불변성이 꼭 필요하면 `immer` 같은 라이브러리를 쓰거나, 데이터 구조를 처음부터 완전히 불변 스타일로 설계하는 편이 현실적이다.

---

## 6.5 에러를 도메인의 일부로 — throw에서 Result 패턴까지

이제 이 장의 핵심 주제다.

Java 개발자는 에러를 *예외(exception)*로 다룬다. `try-catch`로 잡고, `throws` 선언으로 상위에 전파하고, checked exception으로 컴파일러가 처리를 강제한다. 에러가 타입 시스템의 일부다.

TS에는 checked exception이 없다. 함수 시그니처만 봐서는 그 함수가 어떤 에러를 던지는지 알 수 없다.

```ts
async function fetchUser(userId: string): Promise<User> {
  // 이 함수가 어떤 에러를 던질 수 있는지 타입이 말해주지 않는다
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
}
```

네트워크 에러가 날 수 있다. 404가 올 수 있다. JSON 파싱이 실패할 수 있다. 그런데 시그니처에는 `Promise<User>`만 있다. 호출자는 이것을 알려면 구현을 읽어야 한다.

Java의 checked exception은 이것이 불편해서 함수 시그니처에 `throws IOException`을 강제했다. 물론 Java 개발자들은 이게 번거로워서 `throws Exception`을 달거나 RuntimeException으로 감싸는 편법을 쓰곤 했다. 그래도 *의도*는 좋았다. 에러도 타입의 일부라는 생각.

그렇다면 TS에서는 어떻게 할 수 있을까.

### throw의 현실 — 타입이 없는 에러

먼저 TS에서 `throw`가 어떻게 동작하는지 정확히 이해하자.

```ts
function divide(a: number, b: number): number {
  if (b === 0) throw new Error("Division by zero");
  return a / b;
}

try {
  const result = divide(10, 0);
} catch (e) {
  // e의 타입은 unknown이다 (TS 4.0+, useUnknownInCatchVariables)
  if (e instanceof Error) {
    console.error(e.message);
  }
}
```

`catch` 블록에서 `e`의 타입은 `unknown`이다(TS 4.0 이전에는 `any`였다). 이는 의도적 설계다 — TS는 어떤 값이든 `throw`할 수 있고, 컴파일러는 그게 `Error`라고 가정할 수 없다.

더 중요한 것은, `divide` 함수 시그니처만 봐서는 이 함수가 `throw`할 수 있다는 걸 전혀 알 수 없다는 점이다. `Promise<number>`를 반환하는 함수도 마찬가지다. `reject`될 수 있다는 것도 타입이 표현하지 않는다.

이것은 checked exception에 익숙한 Java 개발자에게는 처음에 좀 당혹스러운 자리다. "에러 처리가 강제되지 않는다고? 그럼 어떻게 신뢰하지?"

### throw는 언제 쓰는 편이 좋을까

`throw`가 나쁜 건 아니다. 단, **어떤 상황에서 쓸지**를 의식적으로 선택하는 편이 낫다.

커뮤니티에서 정착한 실용적 경계는 이렇다.

**Throw를 쓰는 자리:**
- **프로그래밍 오류** — 절대 일어나면 안 되는 상황. `divide(10, 0)`처럼 호출자가 계약을 위반한 경우.
- **시스템 경계(boundary)** — HTTP 요청 핸들러, CLI 진입점처럼 에러를 잡아서 응답으로 변환하는 최상위 레이어.
- **복구 불가능한 상황** — 데이터베이스 연결 자체가 실패한 경우처럼 애플리케이션이 종료되어야 하는 상황.

**Result/Either를 쓰는 자리:**
- **예측 가능한 실패** — 사용자 입력이 유효하지 않다, 아이템이 재고 부족이다, 외부 API가 404를 반환했다.
- **비즈니스 규칙 위반** — 계좌 잔액이 부족하다, 이미 취소된 주문이다.
- **함수형 파이프라인** — 여러 단계의 연산을 체이닝할 때, 중간에 실패가 나면 나머지를 건너뛰고 싶다.

이 두 분류가 명확하게 나뉘는 건 아니다. 팀마다 경계를 다르게 잡는다. 하지만 **비즈니스 로직 안에서 발생하는 예측 가능한 실패는 Result로 표현하는 편이 낫다**는 데는 대체로 합의가 있다.

### Result 타입 직접 만들기

가장 단순한 형태의 Result 타입을 직접 만들어보자.

```ts
type Ok<T> = { ok: true; value: T };
type Err<E> = { ok: false; error: E };
type Result<T, E> = Ok<T> | Err<E>;

function ok<T>(value: T): Ok<T> {
  return { ok: true, value };
}

function err<E>(error: E): Err<E> {
  return { ok: false, error };
}
```

이제 이것을 쓰면:

```ts
type InsufficientFundsError = {
  type: "InsufficientFunds";
  required: number;
  available: number;
};

type TransferError =
  | InsufficientFundsError
  | { type: "AccountNotFound"; accountId: string }
  | { type: "AccountFrozen"; accountId: string };

function transferFunds(
  fromAccountId: string,
  toAccountId: string,
  amount: number
): Result<{ transactionId: string }, TransferError> {
  // 잔액 확인
  const balance = getBalance(fromAccountId);
  if (balance < amount) {
    return err({
      type: "InsufficientFunds",
      required: amount,
      available: balance,
    });
  }

  // ... 실제 이체 로직
  const txId = executeTransfer(fromAccountId, toAccountId, amount);
  return ok({ transactionId: txId });
}

// 호출하는 쪽
const result = transferFunds("acc-1", "acc-2", 50000);

if (result.ok) {
  console.log("이체 완료:", result.value.transactionId);
} else {
  switch (result.error.type) {
    case "InsufficientFunds":
      console.error(`잔액 부족 (필요: ${result.error.required}, 보유: ${result.error.available})`);
      break;
    case "AccountNotFound":
      console.error(`계좌를 찾을 수 없음: ${result.error.accountId}`);
      break;
    case "AccountFrozen":
      console.error(`동결된 계좌: ${result.error.accountId}`);
      break;
  }
}
```

함수 시그니처만 봐도 어떤 에러가 날 수 있는지 안다. `TransferError`를 보면 `InsufficientFunds`, `AccountNotFound`, `AccountFrozen` 세 경우가 있다는 것을 타입이 표현한다. 그리고 `switch` 문에서 모든 케이스를 처리하지 않으면 컴파일러가 경고한다(exhaustive check를 추가하면).

Java의 checked exception이 지향하던 바가 바로 이것이다. 에러를 *타입 시스템의 일부*로 만드는 것. TS에서는 `throw` 대신 `Result`로 이것을 달성한다.

### neverthrow — 실용적인 Result 라이브러리

직접 만든 Result도 충분하지만, 체이닝이나 변환이 필요해지면 코드가 복잡해진다. `neverthrow`는 이것을 깔끔하게 해결하는 작은 라이브러리다.

```bash
npm install neverthrow
```

```ts
import { ok, err, Result, ResultAsync } from "neverthrow";

type ValidationError = { field: string; message: string };

function validateEmail(email: string): Result<string, ValidationError> {
  if (!email.includes("@")) {
    return err({ field: "email", message: "유효한 이메일 주소가 아닙니다" });
  }
  return ok(email);
}

function validateAge(age: number): Result<number, ValidationError> {
  if (age < 0 || age > 150) {
    return err({ field: "age", message: "나이가 유효 범위를 벗어납니다" });
  }
  return ok(age);
}

// 여러 Result를 조합
function validateUser(
  email: string,
  age: number
): Result<{ email: string; age: number }, ValidationError[]> {
  const emailResult = validateEmail(email);
  const ageResult = validateAge(age);

  // combineWithAllErrors는 모든 에러를 모아서 반환
  return Result.combineWithAllErrors([emailResult, ageResult]).map(
    ([validEmail, validAge]) => ({ email: validEmail, age: validAge })
  );
}

// 체이닝
const result = validateEmail("alice@example.com")
  .map(email => email.toLowerCase())
  .andThen(email => findUserByEmail(email));  // Result를 반환하는 함수
```

`map`은 성공 값을 변환한다(실패면 그대로 통과). `andThen`은 성공 값을 받아서 새 Result를 반환하는 함수를 체이닝한다. 실패가 있으면 나머지 체인을 건너뛴다. 이것이 함수형 프로그래밍의 **Railway-oriented programming** 또는 **monadic chaining**이라고 불리는 패턴이다.

### ResultAsync — 비동기 에러를 타입으로

현실 코드는 대부분 비동기다. `neverthrow`의 `ResultAsync`가 이것을 다룬다.

```ts
import { ResultAsync, errAsync, okAsync } from "neverthrow";

function fetchUser(userId: string): ResultAsync<User, FetchError> {
  return ResultAsync.fromPromise(
    fetch(`/api/users/${userId}`).then(res => {
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      return res.json() as Promise<User>;
    }),
    (e): FetchError => ({
      type: "NetworkError",
      message: e instanceof Error ? e.message : "Unknown error",
    })
  );
}

// 체이닝
const result = await fetchUser(userId)
  .map(user => ({ ...user, displayName: `${user.name} (${user.email})` }))
  .andThen(user => updateLastSeen(user.id).map(() => user));

if (result.isOk()) {
  console.log(result.value.displayName);
} else {
  console.error(result.error.message);
}
```

`ResultAsync.fromPromise`는 Promise를 Result로 감싼다. 두 번째 인자는 catch된 에러를 도메인 에러 타입으로 변환하는 함수다. 이렇게 하면 비동기 흐름 전체가 타입이 있는 에러 경로를 가진다.

### fp-ts Either — 더 학술적인 접근

`fp-ts`는 함수형 프로그래밍의 추상화를 TS로 가져온 라이브러리다. `Either<E, A>`가 Result에 해당한다. `Left(e)`가 실패, `Right(a)`가 성공이다.

```ts
import * as E from "fp-ts/Either";
import { pipe } from "fp-ts/function";

function validateEmail(email: string): E.Either<string, string> {
  return email.includes("@")
    ? E.right(email)
    : E.left("유효하지 않은 이메일");
}

function validateAge(age: number): E.Either<string, number> {
  return age >= 0 && age <= 150
    ? E.right(age)
    : E.left("나이가 범위를 벗어남");
}

const result = pipe(
  validateEmail("alice@example.com"),
  E.chain(email =>
    pipe(
      validateAge(25),
      E.map(age => ({ email, age }))
    )
  )
);
```

`pipe`와 `chain`, `map`으로 흐름을 구성한다. 코드가 처음에는 낯설지만, 한번 익숙해지면 읽기 좋다. 단, `fp-ts`는 학습 곡선이 가파르고 번들 크기도 상당하다. 팀 전체가 함수형 스타일을 선호하는 게 아니라면, `neverthrow`가 더 가볍고 친숙한 선택이다.

### Effect-ts — 더 나아간 선택

Effect-ts는 `fp-ts`를 넘어서 ZIO(Scala)·cats-effect에서 영향을 받은 포괄적인 함수형 프레임워크다. Effect-ts에서는 모든 계산이 `Effect<R, E, A>` — 의존성 R, 에러 E, 성공값 A — 로 표현된다.

```ts
import { Effect, pipe } from "effect";

const getUser = (userId: string): Effect.Effect<User, UserNotFoundError> =>
  Effect.tryPromise({
    try: () => fetchUserFromDb(userId),
    catch: () => new UserNotFoundError(userId),
  });

const program = pipe(
  getUser("user-123"),
  Effect.map(user => user.name),
  Effect.flatMap(name => Effect.log(`사용자: ${name}`))
);

// 실행
Effect.runPromise(program);
```

에러 타입이 `Effect` 시그니처 자체에 포함된다. 코드만 봐도 어떤 에러가 날 수 있는지 안다. Dependency injection도 `R` 타입 인자로 표현된다.

강력하지만 무겁다. 전체 아키텍처가 Effect 모델을 중심으로 조직되어야 한다. 입문하기에는 `neverthrow`가 더 현실적이다.

### Java checked exception과의 비교 — 무엇을 얻고 무엇을 잃는가

솔직하게 비교해보자.

**Java checked exception이 좋은 점:**
- 컴파일러가 처리를 강제한다. `throws IOException`이 있으면 반드시 `try-catch`하거나 다시 `throws`를 선언해야 한다.
- 라이브러리 API만 봐도 어떤 예외가 날 수 있는지 안다.

**Java checked exception의 문제:**
- 개발자들이 결국 `throws Exception`이나 `RuntimeException`으로 감싸서 체크를 회피한다.
- checked exception이 API 계약의 일부가 되어, 라이브러리 내부 구현이 바뀌면 API도 바뀐다.
- 람다·스트림과 궁합이 나쁘다. checked exception을 던지는 함수를 `map()`에 넣으면 번거롭다.

**TS의 throw:**
- 유연하다. 어디서든 던질 수 있고, 잡든 안 잡든 컴파일러는 신경 안 쓴다.
- 타입이 없어서 호출자가 믿고 쓰기 어렵다.

**TS의 Result 패턴:**
- 함수 시그니처에 에러 타입이 포함된다. checked exception의 *정신*을 가져올 수 있다.
- 컴파일러가 강제하지 않는다. 팀이 컨벤션을 지켜야 한다.
- 람다·체이닝과 궁합이 좋다. `map`, `andThen`으로 흐름이 자연스럽다.
- JS/TS 생태계의 많은 라이브러리가 여전히 `throw`를 쓰므로, 경계에서 변환이 필요하다.

결국 **TS에서 Result 패턴은 "언어가 강제하지 않는 checked exception"**이다. 컴파일러의 강제 대신 팀의 컨벤션으로 유지된다. 불완전해 보이지만, Java checked exception도 실제로 그 강제 덕분에 자주 우회되었던 것을 생각하면, 현실에서 차이가 생각만큼 크지 않을 수 있다.

---

> **📚 Java/Kotlin 시선 — Kotlin `Result<T>`/Arrow `Either` ↔ neverthrow**
>
> Kotlin에도 Result 타입이 있다.
>
> ```kotlin
> fun fetchUser(userId: String): Result<User> = runCatching {
>     // 예외가 발생하면 Failure로 감싸진다
>     userRepository.findById(userId) ?: throw UserNotFoundException(userId)
> }
>
> val result = fetchUser("user-123")
> result.fold(
>     onSuccess = { user -> println("사용자: ${user.name}") },
>     onFailure = { e -> println("에러: ${e.message}") }
> )
> ```
>
> Kotlin의 `Result<T>`는 성공/실패를 감싸지만, 에러 타입이 `Throwable`로 고정이다. 어떤 에러인지 타입 수준에서 표현하려면 Arrow 라이브러리의 `Either<E, A>`를 쓴다.
>
> ```kotlin
> import arrow.core.Either
> import arrow.core.right
> import arrow.core.left
>
> sealed class TransferError {
>     data class InsufficientFunds(val required: Int, val available: Int) : TransferError()
>     data class AccountNotFound(val accountId: String) : TransferError()
> }
>
> fun transfer(from: String, to: String, amount: Int): Either<TransferError, String> {
>     val balance = getBalance(from)
>     return if (balance < amount)
>         InsufficientFunds(amount, balance).left()
>     else
>         executeTransfer(from, to, amount).right()
> }
>
> // 체이닝
> val result = transfer("acc-1", "acc-2", 50000)
>     .map { txId -> "완료: $txId" }
>     .flatMap { msg -> sendNotification(msg).map { msg } }
> ```
>
> TS의 `neverthrow`와 개념이 정확히 같다. `Either.right()`가 `ok()`, `Either.left()`가 `err()`다. `map`과 `flatMap`(TS에서는 `andThen`)도 같다.
>
> 차이: Arrow는 성숙한 생태계와 풍부한 추상화를 제공한다. Kotlin의 언어 기능(sealed class, data class, `when`)과도 자연스럽게 결합된다. TS의 `neverthrow`는 훨씬 작고 단순하다 — 그것이 장점이기도 하다. Arrow처럼 포괄적인 도구가 필요하다면 TS 생태계에서는 `fp-ts`나 `Effect-ts`가 그 위치에 있다.

---

## 6.6 에러 타입의 설계 — 도메인 에러를 어떻게 표현할까

Result 패턴을 쓰기로 했다면, 에러 타입을 어떻게 설계할지가 중요하다.

### 단순한 시작 — 문자열 에러

```ts
function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return err("Division by zero");
  return ok(a / b);
}
```

빠르고 편하지만, 에러 메시지가 `string`이면 처리 분기를 타입으로 표현할 수 없다. 호출자는 문자열 비교로 분기해야 한다.

### 태그된 에러 — discriminated union 활용

더 나은 방법은 에러를 discriminated union으로 표현하는 것이다.

```ts
type OrderError =
  | { type: "OrderNotFound"; orderId: string }
  | { type: "OrderAlreadyCancelled"; orderId: string; cancelledAt: Date }
  | { type: "InsufficientStock"; productId: string; requested: number; available: number }
  | { type: "PaymentFailed"; reason: string; retryable: boolean };

function processOrder(orderId: string): Result<Order, OrderError> {
  const order = db.findOrder(orderId);
  if (!order) {
    return err({ type: "OrderNotFound", orderId });
  }

  if (order.status === "cancelled") {
    return err({
      type: "OrderAlreadyCancelled",
      orderId,
      cancelledAt: order.cancelledAt!,
    });
  }

  // ... 처리
  return ok(processedOrder);
}

// 호출 측에서 타입 안전하게 처리
const result = processOrder("order-123");

if (!result.ok) {
  switch (result.error.type) {
    case "OrderNotFound":
      return sendNotFound(result.error.orderId);
    case "OrderAlreadyCancelled":
      return sendConflict(`이미 ${result.error.cancelledAt}에 취소됨`);
    case "InsufficientStock":
      return sendBadRequest(`재고 부족: ${result.error.available}개 남음`);
    case "PaymentFailed":
      if (result.error.retryable) {
        return scheduleRetry(orderId);
      }
      return sendPaymentError(result.error.reason);
  }
}
```

에러마다 다른 데이터가 있고, `switch`에서 타입이 좁혀지므로 각 케이스의 고유 필드에 안전하게 접근할 수 있다. Kotlin의 `sealed class`와 거의 같은 표현력이다.

### 에러 계층 — 작게 시작하고 필요하면 합치자

프로그램이 커지면 에러 타입도 많아진다. 계층을 구성하는 방법이 있다.

```ts
// 도메인별 에러
type UserError =
  | { type: "UserNotFound"; userId: string }
  | { type: "UserAlreadyExists"; email: string };

type OrderError =
  | { type: "OrderNotFound"; orderId: string }
  | { type: "InsufficientStock"; productId: string };

// 상위 레벨에서 합치기
type AppError =
  | { domain: "user"; error: UserError }
  | { domain: "order"; error: OrderError }
  | { domain: "system"; error: { message: string; stack?: string } };
```

또는 에러 코드를 namespace로 구분하는 방법도 있다.

```ts
type ErrorCode =
  | `USER_${string}`
  | `ORDER_${string}`
  | `SYSTEM_${string}`;

type AppError = {
  code: ErrorCode;
  message: string;
  metadata?: Record<string, unknown>;
};
```

어떤 방식이든 정답은 없다. 중요한 건 팀 내에서 일관성을 유지하는 것이다.

### boundary에서 throw, 내부에서 Result

앞서 말한 실용적 경계를 코드로 보여주자. HTTP 핸들러가 좋은 예다.

```ts
// 내부 비즈니스 로직 — Result를 사용
function cancelOrder(
  orderId: string,
  userId: string
): Result<Order, OrderError> {
  const order = db.findOrder(orderId);
  if (!order) return err({ type: "OrderNotFound", orderId });
  if (order.userId !== userId) return err({ type: "NotOwner", orderId, userId });
  if (order.status === "cancelled") {
    return err({
      type: "OrderAlreadyCancelled",
      orderId,
      cancelledAt: order.cancelledAt!,
    });
  }

  const updated = db.updateOrder(orderId, { status: "cancelled" });
  return ok(updated);
}

// HTTP boundary — throw/catch로 외부에 전달
app.delete("/orders/:id", async (req, res) => {
  const result = cancelOrder(req.params.id, req.user.id);

  if (result.ok) {
    return res.json({ success: true, order: result.value });
  }

  switch (result.error.type) {
    case "OrderNotFound":
      return res.status(404).json({ error: "주문을 찾을 수 없습니다" });
    case "NotOwner":
      return res.status(403).json({ error: "권한이 없습니다" });
    case "OrderAlreadyCancelled":
      return res.status(409).json({ error: "이미 취소된 주문입니다" });
  }
});
```

비즈니스 로직은 Result로 흐른다. HTTP 핸들러가 boundary다 — 여기서 Result를 HTTP 응답으로 변환한다. 핸들러 자체에서 예상치 못한 `throw`가 난다면(DB 연결 실패 같은), Express의 에러 미들웨어가 잡는다. 이 두 층이 분리되어 있다.

---

## 6.7 도메인 모델 설계 — 모든 것을 합쳐서

지금까지 살펴본 도구들을 모아서 작은 도메인 모델을 설계해보자. 간단한 전자상거래 주문 도메인이다.

### 식별자 타입 정의

```ts
declare const _brand: unique symbol;
type Brand<T, B> = T & { readonly [_brand]: B };

type UserId = Brand<string, "UserId">;
type ProductId = Brand<string, "ProductId">;
type OrderId = Brand<string, "OrderId">;
type Money = Brand<number, "Money">;  // 원화 기준, 정수

function makeUserId(v: string): UserId {
  if (!v || v.trim().length === 0) throw new Error("UserId cannot be empty");
  return v as UserId;
}

function makeMoney(v: number): Result<Money, { type: "InvalidAmount"; value: number }> {
  if (!Number.isInteger(v) || v < 0) {
    return err({ type: "InvalidAmount", value: v });
  }
  return ok(v as Money);
}
```

### 도메인 상태 표현

```ts
type OrderStatus =
  | { status: "pending" }
  | { status: "confirmed"; confirmedAt: Date }
  | { status: "shipped"; confirmedAt: Date; shippedAt: Date; trackingNumber: string }
  | { status: "delivered"; confirmedAt: Date; shippedAt: Date; deliveredAt: Date }
  | { status: "cancelled"; cancelledAt: Date; reason: string };

type OrderItem = {
  readonly productId: ProductId;
  readonly quantity: number;
  readonly unitPrice: Money;
};

type Order = {
  readonly id: OrderId;
  readonly userId: UserId;
  readonly items: ReadonlyArray<OrderItem>;
  readonly totalAmount: Money;
} & OrderStatus;
```

`Order`는 `OrderId`, `UserId`, `items`, `totalAmount`에 더해 `OrderStatus`가 intersection으로 붙어 있다. 상태에 따른 추가 필드가 자동으로 포함된다.

### 도메인 로직

```ts
type OrderDomainError =
  | { type: "EmptyCart" }
  | { type: "OrderNotCancellable"; currentStatus: string }
  | { type: "InvalidQuantity"; productId: ProductId; quantity: number };

function createOrder(
  userId: UserId,
  items: Array<{ productId: ProductId; quantity: number; unitPrice: Money }>
): Result<Order, OrderDomainError> {
  if (items.length === 0) {
    return err({ type: "EmptyCart" });
  }

  const invalidItem = items.find(i => i.quantity <= 0);
  if (invalidItem) {
    return err({
      type: "InvalidQuantity",
      productId: invalidItem.productId,
      quantity: invalidItem.quantity,
    });
  }

  const totalAmount = items.reduce(
    (sum, item) => sum + item.unitPrice * item.quantity,
    0
  ) as Money;

  const order: Order = {
    id: generateOrderId() as OrderId,
    userId,
    items: items.map(i => ({
      productId: i.productId,
      quantity: i.quantity,
      unitPrice: i.unitPrice,
    })),
    totalAmount,
    status: "pending",
  };

  return ok(order);
}

function cancelOrder(
  order: Order,
  reason: string
): Result<Order, OrderDomainError> {
  if (order.status !== "pending") {
    return err({
      type: "OrderNotCancellable",
      currentStatus: order.status,
    });
  }

  const cancelled: Order = {
    ...order,
    status: "cancelled",
    cancelledAt: new Date(),
    reason,
  };

  return ok(cancelled);
}
```

이 도메인 모델의 특징을 정리하면:

1. **식별자 혼용 불가**: `UserId`와 `ProductId`가 섞이면 컴파일 에러.
2. **상태 전이가 타입에 표현됨**: `cancelOrder`는 `pending` 상태에서만 가능하다는 게 `switch`/`if` 안에서 타입이 보증한다.
3. **에러가 타입의 일부**: `OrderDomainError`를 보면 어떤 실패가 가능한지 안다.
4. **불변성**: `readonly`와 `ReadonlyArray`로 직접 수정을 막는다.

완벽하지는 않다. Kotlin의 `data class`나 `sealed class`처럼 컴파일러가 강제해주는 부분이 훨씬 많지 않다. `as Money` 같은 단언이 여전히 필요하다. 하지만 이 정도면 실무에서 도메인 버그를 상당히 컴파일 타임에 잡을 수 있다.

---

## 6.8 실전 패턴 — 조합하면 어떻게 보이는가

실제 서비스 코드에서 이 패턴들이 어떻게 어울리는지 더 완전한 예제로 보자.

### 사용자 등록 유스케이스

```ts
// 도메인 에러
type RegistrationError =
  | { type: "EmailAlreadyExists"; email: string }
  | { type: "WeakPassword"; minLength: number }
  | { type: "InvalidEmail"; email: string }
  | { type: "DatabaseError"; message: string };

// 입력 타입 (외부에서 받은 raw 데이터)
type RegisterInput = {
  email: string;
  password: string;
  name: string;
};

// 검증된 값 타입 (branded)
type ValidatedEmail = Brand<string, "ValidatedEmail">;
type HashedPassword = Brand<string, "HashedPassword">;

// 검증 함수들
function validateEmail(
  email: string
): Result<ValidatedEmail, RegistrationError> {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return err({ type: "InvalidEmail", email });
  }
  return ok(email as ValidatedEmail);
}

function validatePassword(
  password: string
): Result<string, RegistrationError> {
  const MIN_LENGTH = 8;
  if (password.length < MIN_LENGTH) {
    return err({ type: "WeakPassword", minLength: MIN_LENGTH });
  }
  return ok(password);
}

// 서비스 레이어
async function registerUser(
  input: RegisterInput
): Promise<Result<{ userId: UserId }, RegistrationError>> {
  // 검증
  const emailResult = validateEmail(input.email);
  if (!emailResult.ok) return emailResult;

  const passwordResult = validatePassword(input.password);
  if (!passwordResult.ok) return passwordResult;

  // 중복 확인
  const existing = await db.users.findByEmail(emailResult.value);
  if (existing) {
    return err({ type: "EmailAlreadyExists", email: input.email });
  }

  // 저장
  try {
    const hashedPassword = await hashPassword(passwordResult.value) as HashedPassword;
    const userId = await db.users.create({
      email: emailResult.value,
      password: hashedPassword,
      name: input.name,
    });
    return ok({ userId: userId as UserId });
  } catch (e) {
    // 예상치 못한 DB 에러는 Result로 변환
    return err({
      type: "DatabaseError",
      message: e instanceof Error ? e.message : "Unknown database error",
    });
  }
}

// HTTP 핸들러
app.post("/users/register", async (req, res) => {
  const result = await registerUser(req.body);

  if (result.ok) {
    return res.status(201).json({ userId: result.value.userId });
  }

  switch (result.error.type) {
    case "InvalidEmail":
      return res.status(400).json({ field: "email", message: "이메일 형식이 올바르지 않습니다" });
    case "WeakPassword":
      return res.status(400).json({
        field: "password",
        message: `비밀번호는 최소 ${result.error.minLength}자 이상이어야 합니다`,
      });
    case "EmailAlreadyExists":
      return res.status(409).json({ message: "이미 가입된 이메일입니다" });
    case "DatabaseError":
      console.error("DB Error:", result.error.message);
      return res.status(500).json({ message: "서버 오류가 발생했습니다" });
  }
});
```

이 코드를 처음 본 Java/Kotlin 개발자는 낯설게 느낄 수 있다. `Result`를 `if (!emailResult.ok) return emailResult`로 일일이 체크하는 것이 번거롭다고 느낄 수 있다. 사실 그 느낌이 맞다. `neverthrow`의 `andThen` 체이닝을 쓰면 이 보일러플레이트를 줄일 수 있다.

```ts
import { ResultAsync } from "neverthrow";

async function registerUser(
  input: RegisterInput
): ResultAsync<{ userId: UserId }, RegistrationError> {
  return validateEmail(input.email)
    .asyncAndThen(email =>
      validatePassword(input.password).asyncAndThen(password =>
        ResultAsync.fromPromise(
          db.users.findByEmail(email),
          (e): RegistrationError => ({ type: "DatabaseError", message: String(e) })
        ).andThen(existing => {
          if (existing) {
            return err({ type: "EmailAlreadyExists", email: input.email });
          }
          return ResultAsync.fromPromise(
            (async () => {
              const hashed = await hashPassword(password);
              const userId = await db.users.create({ email, password: hashed, name: input.name });
              return { userId: userId as UserId };
            })(),
            (e): RegistrationError => ({ type: "DatabaseError", message: String(e) })
          );
        })
      )
    );
}
```

스타일이 다르다. 어느 쪽이 더 가독성이 좋은지는 팀마다 다를 수 있다. 중요한 건 어떤 스타일이든 **에러 타입이 함수 시그니처에 표현된다**는 점이다.

---

## 6.9 `as const`로 객체를 열거형처럼 쓰기

enum의 대안으로 `as const`를 쓰는 패턴을 조금 더 살펴보자. 실무에서 자주 만나는 패턴이다.

### 상수 맵 패턴

```ts
const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  NOT_FOUND: 404,
  CONFLICT: 409,
  INTERNAL_ERROR: 500,
} as const;

type HttpStatusCode = typeof HTTP_STATUS[keyof typeof HTTP_STATUS];
// 200 | 201 | 400 | 401 | 404 | 409 | 500

function sendResponse(status: HttpStatusCode, body: unknown) {
  // ...
}

sendResponse(HTTP_STATUS.OK, { success: true });
sendResponse(200, { success: true });          // 직접 숫자도 허용
sendResponse(999, { success: true });          // 컴파일 에러
```

`HTTP_STATUS`는 런타임에 실제 객체로 존재한다. enum처럼 쓸 수 있으면서 tree-shaking도 되고, 타입도 정확하다.

### 설정 객체 패턴

```ts
const FEATURE_FLAGS = {
  enableNewCheckout: true,
  enableBetaSearch: false,
  maxCartItems: 50,
} as const;

type FeatureFlag = keyof typeof FEATURE_FLAGS;

function isEnabled(flag: FeatureFlag): boolean {
  return FEATURE_FLAGS[flag] as boolean;
}

isEnabled("enableNewCheckout");  // OK
isEnabled("unknownFlag");        // 컴파일 에러
```

---

## 6.10 실무 체크리스트 — 도메인 모델링할 때 물어볼 것들

마지막으로, 새 도메인을 TS로 모델링할 때 체크해볼 질문들을 정리하자.

**식별자 안전성**
- [ ] 여러 종류의 `string` 식별자가 함수에 같이 들어가는가? → Branded type 고려
- [ ] 생성 지점에서 검증이 필요한가? → maker 함수 추가

**상태 표현**
- [ ] 상태마다 다른 필드가 있는가? → discriminated union
- [ ] 상태 전이 규칙이 있는가? → 전이 함수에서 타입으로 표현

**에러 처리**
- [ ] 이 실패가 비즈니스 규칙 위반인가? → Result 패턴
- [ ] 이 실패가 프로그래밍 오류인가? → throw
- [ ] 호출자가 에러를 처리하지 않으면 안 되는가? → Result로 강제

**불변성**
- [ ] 생성 후 바뀌면 안 되는 필드가 있는가? → `readonly`
- [ ] 설정/상수 객체인가? → `as const`
- [ ] 컬렉션이 수정되면 안 되는가? → `ReadonlyArray<T>`

**열거형**
- [ ] 고정된 값의 집합이 필요한가? → union literal 우선
- [ ] 런타임에 열거형 값을 순회해야 하는가? → `as const` 객체
- [ ] 외부 API와 값을 교환하면서 이름이 필요한가? → 문자열 enum 고려

---

> **📖 더 깊이 가려면**
>
> 이 장에서 다룬 branded type, discriminated union, Result 패턴은 도메인 모델링의 기초다. 여기서 한 발 더 나가면 몇 가지 방향이 있다.
>
> **함수형 도메인 모델링**: `fp-ts`와 `Effect-ts`는 이 패턴들을 더 체계화한다. Functor, Applicative, Monad 등의 개념으로 에러 처리 체인을 더 우아하게 구성할 수 있다. 단, 학습 곡선이 가파르다.
>
> **zod와 런타임 검증**: 도메인 모델의 타입을 zod 스키마로 정의하면, 타입 추론과 런타임 검증을 한 곳에서 관리할 수 있다. 외부 경계(API 입력, env 변수)에서 특히 유용하다.
>
> **테스트**: 도메인 타입이 잘 설계되어 있으면 테스트도 더 명확해진다. Result 타입을 반환하는 함수는 `result.ok`와 `result.value` / `result.error`를 단언하는 식으로 깔끔하게 테스트할 수 있다.
>
> → **14장에서 도메인 모델 + Result 패턴의 *타입 단위 테스트*를 다룬다.** 이 장에서 만든 `createOrder`, `cancelOrder`, `registerUser` 같은 함수를 어떻게 테스트하는지, branded type이 테스트에서 어떻게 도움이 되는지를 구체적으로 살펴볼 것이다.

---

## 마무리

이 장에서 살펴본 것들을 정리해보자.

`interface`와 `type alias`는 둘 다 써도 된다. 객체 형태에는 어느 것이든, union이나 intersection에는 `type`, 라이브러리 확장에는 `interface`를 쓰면 된다. 두 개가 공존하는 코드베이스가 더 흔하다.

TS의 구조적 타입 시스템은 도메인 식별자를 자동으로 구분하지 않는다. `UserId`와 `ProductId`가 모두 `string`이면 서로 섞여도 컴파일러가 침묵한다. Branded type이 이것을 해결한다. 토스, Effect-ts, zod 모두 채택한 표준 패턴이다.

TS `enum`은 함정이 있다. 런타임 객체 생성, 숫자형 enum의 역방향 매핑, `const enum`과 번들러의 충돌. 새 코드에서는 union literal을 디폴트로 쓰는 편이 낫다. discriminated union + `never`로 exhaustive check까지 구현하면 Kotlin `sealed class` + `when`과 거의 같은 표현력이 나온다.

불변성은 `readonly`, `Readonly<T>`, `as const`, `Object.freeze()`의 네 도구로 접근한다. 모두 얕은 불변성이라는 한계가 있다. 깊은 불변성이 필요하면 `immer` 같은 라이브러리가 필요하다.

가장 중요한 것은 에러 처리다. TS에는 checked exception이 없다. `throw`는 타입 정보가 없다. 이것이 Java/Kotlin에서 온 개발자에게 처음에는 불안하게 느껴진다. 하지만 `Result<T, E>` 패턴으로 에러를 타입의 일부로 만들 수 있다. `neverthrow`가 이것을 실용적으로 제공한다. 경계에서는 throw, 내부 비즈니스 로직에서는 Result — 이 두 층을 의식적으로 분리하면 코드가 훨씬 명확해진다.

이 모든 것을 처음부터 완벽하게 적용하려고 하면 번거롭다. 기억해두자 — 도구를 점진적으로 도입하는 편이 낫다. 먼저 discriminated union으로 상태를 표현하는 것부터 시작해도 좋다. Branded type은 식별자 혼용으로 버그를 한 번 겪은 뒤에 도입해도 늦지 않는다. Result 패턴은 비즈니스 로직이 복잡해지면서 자연스럽게 필요성을 느끼게 된다.

도메인 모델이 충실하게 설계되면, 그 다음 레이어들이 훨씬 안정적이 된다. 7장에서는 이 도메인 객체들이 비동기 흐름에서 어떻게 움직이는지를 살펴보자. Promise, async/await, 그리고 Java의 `CompletableFuture`·Reactor `Mono`와의 비교가 기다리고 있다.
