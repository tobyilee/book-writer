# 5장. 타입을 만드는 타입 — 제네릭·conditional·infer·매핑·템플릿 리터럴

zod의 코드를 처음 본 날을 떠올려보자. 누군가 짠 코드 한 줄이 눈에 들어온다.

```ts
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().int().nonnegative(),
});

type User = z.infer<typeof UserSchema>;
```

여기서 `User`의 마우스 호버 툴팁을 띄우면 IDE는 친절하게 다음을 보여준다.

```ts
type User = {
  id: string;
  email: string;
  age: number;
}
```

스키마는 분명 *값*이었다. 런타임에 검증을 수행하는 일반 객체였다. 그런데 그 값으로부터 `type User = …`라는 타입이 *유도*되어 나온다. 한 번도 타입을 손으로 적은 적이 없다. 처음 본 사람은 잠깐 멍해진다. *"이게 어떻게 되지? 타입은 컴파일타임에만 존재하는 것 아니었나? 값에서 타입을 어떻게 끌어내지?"*

비슷한 충격이 Hono에도 있다. 라우트 하나를 정의했을 뿐인데 클라이언트 쪽에서 응답 타입이 자동으로 채워진다. tRPC는 더 노골적이다. 서버에서 procedure 하나를 만들면 클라이언트가 그 procedure를 *원격 함수처럼* 호출하는데, 인자 타입과 반환 타입이 정확하게 잡힌다. Prisma는 스키마 파일 한 줄을 바꾸면 IDE의 자동완성이 즉시 따라온다.

이 모든 것이 **타입이 타입을 만든다**는 한 문장으로 요약되는 도구들 위에 서 있다. 5장의 약속은 이거다 — 이 마법을 *부품으로 분해*해서, 다음에 zod 코드를 보면 *"아 이래서 이게 됐구나"*가 손에 잡히도록 하자. 곡예를 부리려는 게 아니다. 우리가 *매일 보는 라이브러리*가 어떤 부품으로 조립되어 있는지를 한 단계씩 올라가며 보자는 것이다.

순서는 이렇다. 먼저 **제네릭과 제약**으로 시작한다. 그 위에 `keyof`·`typeof`·`T[K]`라는 세 도구의 합주를 얹는다. 그 다음이 **매핑 타입** — 객체 타입을 함수처럼 변형하는 도구다. 거기서 한 발 더 나가면 **조건부 타입**이 있고, 그 안에 마법의 키워드 **`infer`**가 숨어 있다. 그 다음이 **템플릿 리터럴 타입**이고, 마지막으로 이 모든 것을 합치면 **재귀 조건부 타입**으로 임의의 깊이를 다룰 수 있다. 부품이 다 모이면 zod·Hono·Prisma·tRPC를 분해해보자. 그 뒤에 두 가지 현실 주제를 다룬다 — *타입 단언(`as`)의 윤리*와 *declaration merging*. 둘 다 입사 첫 달에 마주칠 자리다.

호흡이 길다. 5장이 이 책에서 가장 두꺼운 챕터인 이유가 있다 — *깊이*가 약속이니까. 천천히 읽자.

## 5.1 제네릭은 함수다 — `extends`·default·다중 매개변수

제네릭은 자바 개발자에게 친숙한 개념이다. `List<String>`을 처음 본 날, "오, 컬렉션이 자기 안에 어떤 타입이 들어 있는지를 표현할 수 있구나" 했던 그 감각. TS의 제네릭도 출발점은 같다.

```ts
function identity<T>(value: T): T {
  return value;
}

const a = identity("hello"); // a: string
const b = identity(42);      // b: number
```

여기까지는 자바와 거의 같다. `T`라는 타입 매개변수가 있고, 호출 시점에 실제 타입이 채워진다. *"좋아, 이건 안다"* 싶은 자리다. 그런데 한 발만 더 들어가면 분위기가 달라진다.

### 제네릭은 *값을 받는 함수*가 아니라 *타입을 받는 함수*다

자바에서는 제네릭을 보통 *컬렉션의 빈자리*로 받아들인다. `List<T>`에서 `T`는 그 컬렉션이 담을 원소의 타입이다. 그런데 TS에서는 제네릭을 *타입 수준의 함수*로 받아들이는 편이 낫다.

```ts
type Box<T> = { value: T };
```

이 한 줄을 자바 시선으로 읽으면 *"`T`라는 타입 매개변수를 가진 클래스 비슷한 것"*이다. TS 시선으로 다시 읽으면 *"`T`라는 타입을 받아서 `{ value: T }`라는 타입을 *돌려주는* 타입 함수"*다. 같은 것 같지만 사고 모드가 다르다. 후자로 보기 시작하면, 곧 보게 될 매핑 타입이나 조건부 타입이 *낯설지 않다*. 그것들은 모두 *입력 타입을 받아서 출력 타입을 돌려주는 함수*에 불과하니까.

```ts
type StringBox = Box<string>;  // { value: string }
type NumberBox = Box<number>;  // { value: number }
```

함수 호출과 모양이 똑같다. 인자(`string`)를 넣으면 결과(`{ value: string }`)가 나온다. *"제네릭은 함수다"*라는 직관이 여기서 시작한다.

### `extends`로 제약을 건다 — Java/Kotlin에서 익숙한 자리

제네릭의 빈자리에 *아무 타입이나* 들어와도 되는 건 아니다. *"길이가 있는 것만 받겠다"*고 말하고 싶으면 제약을 건다.

```ts
function logLength<T extends { length: number }>(value: T): T {
  console.log(value.length);
  return value;
}

logLength("hello");          // OK
logLength([1, 2, 3]);        // OK
logLength({ length: 7 });    // OK
logLength(42);               // 에러: number에는 length가 없다
```

자바라면 `<T extends HasLength>` 같은 느낌이고, 코틀린이라면 `<T : HasLength>`다. 이름은 다르지만 의도는 같다 — *"이 타입 매개변수는 이런 모양을 만족해야 한다"*. 그런데 TS의 `extends`가 자바·코틀린의 그것과 한 군데에서 결정적으로 다르다 — TS는 **구조적**이다. 어딘가에 `interface HasLength { length: number }`라고 *선언하지 않아도* `{ length: number }` 모양만 만족하면 호환된다. 3장에서 이미 본 그 *구조적 타입*의 정신이 제네릭 제약에도 그대로 적용된다.

조금 더 흥미로운 패턴을 보자. `T extends keyof U`처럼 *다른 타입 매개변수*에 의존하는 제약도 가능하다.

```ts
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>;
  for (const key of keys) {
    result[key] = obj[key];
  }
  return result;
}

const user = { id: 1, name: "Toby", email: "t@example.com" };
const picked = pick(user, ["id", "name"]);
// picked: { id: number; name: string }
```

여기서 `K extends keyof T`가 핵심이다. *"`K`라는 타입 매개변수는 `T`의 키 중 하나여야 한다"*. 그래서 `pick(user, ["id", "phone"])`이라고 쓰면 컴파일러가 즉시 막는다 — `phone`은 `keyof user`가 아니니까. 자바에서 이 정도의 *키 수준 안전성*을 표현하려면 별도의 `enum` 클래스를 만들거나 reflection을 동원해야 한다. TS는 그것을 타입 매개변수 한 줄로 끝낸다.

### default 타입 매개변수 — 호출자에게 선택권을 주는 패턴

자바 12 즈음부터는 record나 pattern matching이 들어왔지만, 제네릭에 *기본값*을 주는 문법은 (책 집필 시점 기준) 없다. TS에는 있다.

```ts
type ApiResponse<TData = unknown, TError = Error> = {
  data: TData;
  error?: TError;
};

type UserResponse = ApiResponse<User>;        // TError는 Error로 default
type Custom = ApiResponse<User, ApiError>;    // 둘 다 명시
```

이 한 줄은 라이브러리 설계에서 자주 본다. *"보통은 이걸 쓰지만, 필요하면 바꿔라"*는 안내가 타입 수준에 박혀 있는 셈이다. React의 `useState<T = undefined>`, fetch 래퍼의 `Response<TBody = unknown>` 같은 것들이 모두 이 패턴이다.

### 다중 타입 매개변수의 합주

타입 매개변수가 두 개 이상이 되면 *함수가 함수를 받는* 사고가 자연스러워진다.

```ts
function map<T, U>(arr: T[], fn: (item: T) => U): U[] {
  return arr.map(fn);
}

const nums = map(["a", "bb", "ccc"], (s) => s.length);
// nums: number[]
```

`T`는 입력 배열의 원소 타입, `U`는 변환 후의 원소 타입. 호출자가 `(s) => s.length`라고 쓰는 순간 `T = string`, `U = number`가 *추론*된다. 손으로 적지 않아도 컴파일러가 따라온다 — 4장에서 본 *contextual typing*의 연장이다.

여기서 한 가지 짚어두자. 제네릭을 잘 다룬다는 것은 *타입 매개변수의 흐름을 머릿속에 그릴 수 있다*는 뜻이다. 입력에서 어떤 타입이 들어와서, 어떤 변환을 거쳐, 어떤 출력이 나가는지. 자바의 `Function<T, R>`, `BiFunction<T, U, R>`을 떠올려보면 친숙할 것이다. 차이는 — TS에서는 그 흐름이 *수십 단계*로 길어질 수 있고, 우리가 5장 후반부에 보게 될 zod·tRPC가 정확히 그런 길이의 흐름이다.

> ### 📚 Java/Kotlin 시선 박스 ① — Kotlin reified generic ↔ TS의 한계와 우회
>
> 코틀린에는 `inline` 함수와 결합된 `reified` 키워드가 있다. 런타임에 타입 매개변수의 정보를 *보존*해서, 함수 안에서 `T::class`를 직접 호출할 수 있게 해준다.
>
> ```kotlin
> // Kotlin
> inline fun <reified T> Gson.fromJson(json: String): T =
>     this.fromJson(json, T::class.java)
>
> val user: User = gson.fromJson(jsonString)
> ```
>
> 자바는 erasure 때문에 이게 안 된다. `Class<T>` 객체를 명시적으로 받아야 한다.
>
> ```java
> // Java
> User user = gson.fromJson(jsonString, User.class);
> ```
>
> TS는 어느 쪽일까? **자바와 같다**. 더 나아가 자바보다 더 가혹하다. `tsc`가 끝나면 *모든 타입이 사라진다*. `Class<T>` 같은 런타임 메타데이터도 없다. 3장에서 본 *type erasure*가 여기서 다시 발목을 잡는다.
>
> ```ts
> // TS — 작동하지 않는다
> function fromJson<T>(json: string): T {
>   return JSON.parse(json) as T;  // 그냥 캐스팅. 검증 없음.
> }
>
> const user = fromJson<User>("{\"id\": 1}");  // 컴파일은 된다. 런타임은 모른다.
> ```
>
> 그래서 TS 진영에는 *우회 전략 두 가지*가 정착했다.
>
> **첫째, 스키마를 값으로 들고 다닌다.** zod·valibot·io-ts 같은 라이브러리가 그 자리다. 스키마 객체에서 *타입을 유도하고*(컴파일타임), *런타임 검증*을 같은 객체로 한다. 한 번 정의하면 두 자리가 동시에 채워진다.
>
> ```ts
> const UserSchema = z.object({ id: z.number(), name: z.string() });
> type User = z.infer<typeof UserSchema>;            // 컴파일타임
> const user = UserSchema.parse(jsonValue);          // 런타임
> ```
>
> **둘째, 런타임 메타데이터가 필요한 곳은 데코레이터 + reflect-metadata로 채운다.** NestJS·TypeORM·class-validator가 이 길을 갔다. 단, TC39 신규 데코레이터 표준에는 reflect-metadata가 빠져 있어서, 두 진영(legacy vs TC39)이 당분간 갈라져 있다. 13장에서 더 깊이 다룬다.
>
> 정리하면 — *코틀린의 reified는 TS에 없다*. 대신 *값과 타입을 같은 정의에서 끌어내는* zod 패턴이 사실상의 표준이 되었다. *"왜 zod가 이렇게 인기가 많지?"*의 답이 절반은 여기에 있다.

## 5.2 `keyof`·`typeof`·`T[K]` — 세 도구의 합주

제네릭을 도구로 쓰려면 *타입을 조작하는 작은 도구들*이 필요하다. TS에는 그런 도구가 여럿 있는데, 가장 자주 함께 등장하는 셋이 `keyof`·`typeof`·`T[K]`다. 처음 보면 따로따로 도는 도구처럼 느껴지지만, 사실은 *3중주*다 — 같이 쓰일 때 위력이 나온다.

### `keyof T` — 객체 타입의 키를 *유니온으로* 꺼낸다

```ts
type User = {
  id: number;
  name: string;
  email: string;
};

type UserKey = keyof User;
// "id" | "name" | "email"
```

`keyof`는 객체 타입을 받아서 *키들의 유니온*을 돌려주는 연산자다. 자바에는 직접 대응이 없다 — 굳이 비교하자면 *컴파일타임의 reflection*에 가까운데, 자바는 그걸 런타임에 `Field[]`로 한다.

여기서 한 가지 짚자. `keyof T`의 결과는 *문자열 리터럴 유니온*이지, 그냥 `string`이 아니다. `"id" | "name" | "email"`이라는 *세 개의 정확한 값들*의 유니온이다. 이게 곧 5.6의 템플릿 리터럴 타입과 결합되면 굉장한 표현력을 낸다.

### `typeof v` — 값에서 타입을 *유도한다*

3장에서 한 번 등장했지만 5장의 맥락에서 다시 보자. `typeof`는 두 얼굴이 있다. 런타임에는 JS 연산자로 동작해서 `"string"`, `"number"` 같은 문자열을 돌려준다. 컴파일타임에는 TS 연산자로 동작해서 *값의 타입을 추론*한다.

```ts
const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
  retry: 3,
} as const;

type Config = typeof config;
// {
//   readonly apiUrl: "https://api.example.com";
//   readonly timeout: 5000;
//   readonly retry: 3;
// }
```

`as const`가 붙어 있어서 리터럴 타입이 그대로 유지된 점에 주목하자(4장 참조). `typeof config`는 그 *전체 모양*을 타입으로 끌어낸다. 손으로 다시 적을 필요가 없다.

이게 곧 zod의 `z.infer<typeof Schema>` 패턴의 절반이다 — *값(스키마)에서 타입을 끌어내기 위해 `typeof`를 쓰는 자리*. 그러니 우리가 zod의 마법을 분해할 때 가장 먼저 만나는 부품이 바로 이 `typeof`다.

### `T[K]` — indexed access, *키로 값의 타입을 꺼낸다*

자바의 `Map`에서 `map.get("name")`을 하면 값을 꺼낸다. TS의 `T[K]`는 그 *컴파일타임 버전*이다.

```ts
type User = { id: number; name: string; email: string };

type Id = User["id"];        // number
type Name = User["name"];    // string
type IdOrName = User["id" | "name"];  // number | string
```

키 자리에 *유니온*을 넣어도 된다. 그러면 결과도 *유니온*으로 나온다. 깔끔하다.

여기까지가 각자의 얼굴이고, 이제 셋이 합주하는 자리를 보자.

### 합주 — 진짜 위력이 나오는 자리

```ts
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { id: 1, name: "Toby", email: "t@example.com" };

const id = getProperty(user, "id");      // id: number
const name = getProperty(user, "name");  // name: string
const oops = getProperty(user, "phone"); // 컴파일 에러
```

이 함수의 시그니처를 천천히 읽어보자. `T`는 객체 타입. `K`는 *그 객체의 키 중 하나*(`extends keyof T`로 제약). 반환 타입은 `T[K]` — *그 키에 해당하는 값의 타입*. 이 한 줄이 *런타임에 키로 값을 꺼낸다*는 동작의 *타입 안전한 일반화*다.

자바라면? 같은 안전성을 얻으려면 *키마다 별도의 메서드*를 만들거나, `Map<String, Object>`에 캐스팅을 끼얹거나, Lombok의 코드 생성에 의존해야 한다. TS는 *세 도구의 합주*로 한 줄에 끝낸다.

이 패턴을 한 번 손에 익혀두면 5장의 나머지가 훨씬 잘 읽힌다. 매핑 타입도, 조건부 타입도, infer도 — 모두 이 *제네릭 제약 + keyof + indexed access*의 변주에 가깝다. *기억해두자.*

## 5.3 매핑 타입 — 객체 타입을 *변형하는 함수*

자바에서 *모든 필드를 nullable로 만든 버전*의 클래스가 필요하다고 해보자. 어떻게 할까? 아마 새 클래스를 *손으로 만든다*. 필드 30개면 30개를 다 적는다. 한 곳을 바꾸면 두 곳을 바꿔야 한다. 끔찍한 일이다.

TS는 이걸 *타입 함수*로 푼다. 매핑 타입(mapped type)이 그 자리다.

```ts
type Partial<T> = {
  [K in keyof T]?: T[K];
};
```

표준 라이브러리에 정의된 `Partial`의 본체다. 한 줄짜리지만 부품이 다 들어 있다.

- `keyof T` — 키들의 유니온
- `[K in keyof T]` — *그 유니온을 순회*
- `?:` — 각 필드를 optional로 만든다
- `T[K]` — 그 키에 해당하는 원래 타입

읽는 법: *"`T`의 모든 키 `K`에 대해, optional이고 타입이 `T[K]`인 필드를 만든다"*. 자바에서 30줄로 적던 걸 TS는 한 줄로 적는다.

```ts
type User = { id: number; name: string; email: string };
type PartialUser = Partial<User>;
// {
//   id?: number;
//   name?: string;
//   email?: string;
// }
```

### modifier — `+`/`-`로 *붙이고 떼기*

매핑 타입의 modifier는 두 가지 — `readonly`와 `?`(optional). 각각 앞에 `+`(붙이기) 또는 `-`(떼기)를 둘 수 있다.

```ts
type Required<T> = {
  [K in keyof T]-?: T[K];   // optional을 떼고 모두 필수로
};

type Mutable<T> = {
  -readonly [K in keyof T]: T[K];   // readonly를 떼서 변경 가능하게
};
```

`Mutable`은 표준에 없지만 자주 직접 만든다. 외부에서 `Readonly<Config>`로 받은 객체를 내부에서 가변 버전으로 다시 받아야 할 때 같은 자리. 한 줄짜리 도구를 자기 코드베이스에 가지고 다니는 셈이다.

`+`는 *기본값*이라 보통 생략한다. `[K in keyof T]+?: T[K]`도 합법이지만, 그냥 `[K in keyof T]?: T[K]`로 적는다.

### key remapping — `as`로 *키 자체를 변형*한다

TS 4.1부터 매핑 타입의 키를 `as`로 다시 적을 수 있게 됐다. 이게 굉장히 유용하다.

```ts
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type User = { id: number; name: string };
type UserGetters = Getters<User>;
// {
//   getId: () => number;
//   getName: () => string;
// }
```

키 자리의 `as`는 *런타임의 타입 단언*이 아니라 *키 변환의 표시*다. 같은 키워드가 두 자리에서 다른 일을 한다 — 헷갈릴 만하지만, 문맥이 다르니 익숙해지면 구분된다.

여기서 `Capitalize`는 5.6에서 만날 *intrinsic string utility*다. 그리고 `string & K`는 키가 `string | number | symbol` 중 *문자열만* 골라내는 트릭이다. 처음 보면 어지럽지만, 5.6까지 가서 다시 보면 자연스럽다.

### *키를 떨어뜨리는* 패턴 — `never`의 조용한 활용

key remapping의 또 다른 쓰임은 *조건에 맞지 않는 키를 떨어뜨리는* 자리다.

```ts
type OmitByValue<T, V> = {
  [K in keyof T as T[K] extends V ? never : K]: T[K];
};

type User = { id: number; name: string; password: string };
type SafeUser = OmitByValue<User, "password" | { password: string }>;
// 타입 V에 맞는 키는 떨어뜨린다.
```

키 자리에 `never`가 들어오면 *그 키는 결과 타입에서 제외*된다. 조건부 타입(다음 절)과 결합된 패턴인데, 한 번 손에 익으면 *"필요 없는 키 빼기"*를 한 줄로 끝낼 수 있다.

이쯤 되면 매핑 타입이 *타입 수준의 `for` 루프 + `if` 분기*처럼 느껴진다. 그게 정확한 직관이다. 자바에서 객체의 모양을 바꾸려면 reflection이나 코드 생성을 동원해야 했지만, TS는 이걸 *타입 시스템 안에서* 한다. 런타임 비용이 0이고, IDE가 즉시 따라온다.

> ### 📚 Java/Kotlin 시선 박스 ② — Java wildcard `? extends`/`? super` ↔ TS variance
>
> 자바 제네릭의 가장 어려운 부분이 변성(variance)이다. `List<? extends Number>`는 *Number의 하위 타입을 담은 List*를 받는다 — *읽기는 되지만 쓰기는 못한다*(producer). `List<? super Integer>`는 *Integer의 상위 타입을 담은 List* — *쓰기는 되지만 읽기는 Object로만*(consumer). PECS — Producer Extends, Consumer Super.
>
> 코틀린은 같은 개념을 `out`/`in` 키워드로 *선언 시점*에 표현한다.
>
> ```kotlin
> interface Producer<out T> { fun produce(): T }
> interface Consumer<in T> { fun consume(item: T) }
> ```
>
> TS는? **변성을 *별도 키워드*로 강제하지 않는다**. 함수 매개변수의 변성은 기본적으로 *bivariant*(양쪽으로 호환) — strict 모드에서 `strictFunctionTypes`를 켜면 *contravariant*(반변)으로 좁혀진다. 4장에서 잠깐 본 그 자리다.
>
> ```ts
> // strictFunctionTypes ON
> type Animal = { name: string };
> type Dog = Animal & { bark(): void };
>
> let f1: (a: Animal) => void = (a) => console.log(a.name);
> let f2: (d: Dog) => void = f1;  // OK — Dog ⊆ Animal이므로 contravariant 호환
> ```
>
> TS 4.7부터는 *명시적 variance annotation*도 들어왔다 — `out`/`in` 키워드를 타입 매개변수 앞에 붙일 수 있다.
>
> ```ts
> interface Producer<out T> { produce(): T; }
> interface Consumer<in T> { consume(item: T): void; }
> ```
>
> 코틀린과 문법까지 같다. 다만 TS의 variance는 *기본이 구조적 추론*이고, `out`/`in`은 *컴파일러에게 힌트를 주거나 의도를 문서화*하는 용도에 가깝다. 자바의 wildcard처럼 *호출자가 매번* `? extends`/`? super`를 적는 모델은 아니다.
>
> 정리: TS의 변성은 자바보다는 코틀린에 가깝지만, 런타임 강제가 없고 unsoundness 자리도 일부 남겨둔다. *변성을 잊고 살아도 일상 코드는 돌아가지만, 라이브러리 설계자라면 `strictFunctionTypes`를 켜고 명시적 `out`/`in`을 쓰는 편이 낫다.* 일반 애플리케이션 개발자가 이 자리에서 발이 걸리는 일은 드물다.

## 5.4 조건부 타입 — `T extends U ? X : Y`

여기서부터가 5장의 *클라이맥스로 가는 길*이다. 조건부 타입(conditional type)은 모양이 단순하다 — *3항 연산자의 타입 버전*이다.

```ts
type IsString<T> = T extends string ? "yes" : "no";

type A = IsString<"hello">;  // "yes"
type B = IsString<42>;        // "no"
type C = IsString<boolean>;   // "no"
```

`T extends U`는 *"`T`가 `U`에 할당 가능한가"*라는 질문이다. 그 답에 따라 `X` 또는 `Y`를 돌려준다. 자바·코틀린에는 직접 대응이 없다. 굳이 비교하자면 *컴파일타임에 동작하는 `if`*다.

이 정도만 보면 *"음, 그래서?"* 싶을 수 있다. 조건부 타입의 진짜 힘은 두 가지 자리에서 나온다 — **distributive 동작**과 **`infer` 키워드**.

### distributive — 유니온이 들어오면 *각 멤버에 분배*된다

```ts
type ToArray<T> = T extends any ? T[] : never;

type A = ToArray<string>;            // string[]
type B = ToArray<string | number>;   // string[] | number[]
```

`B`를 보자. `string | number`라는 유니온이 들어왔는데 결과가 `(string | number)[]`이 *아니라* `string[] | number[]`다. 왜 그럴까?

조건부 타입의 *왼쪽*에 *벌거벗은 타입 매개변수*(naked type parameter)가 들어가면, 컴파일러는 유니온의 *각 멤버*에 대해 *따로 조건을 평가*한다. 위 예에서는 `string extends any ? string[] : never`와 `number extends any ? number[] : never`가 각각 평가되고, 결과가 다시 유니온으로 합쳐진다.

이걸 *"distributive conditional type"*이라고 부른다. 처음엔 마법처럼 느껴지지만, *유니온은 본질적으로 분배된다*는 직관을 가지면 자연스럽다.

### distributive를 *끄는* 트릭 — `[T]`로 감싸기

분배가 *원치 않는* 자리도 있다. 그럴 땐 *튜플로 감싸는* 트릭을 쓴다.

```ts
type IsExactlyString<T> = [T] extends [string] ? "yes" : "no";

type A = IsExactlyString<string>;            // "yes"
type B = IsExactlyString<string | number>;   // "no" — 분배되지 않는다
```

`[T]`로 감싸면 더 이상 *벌거벗은 타입 매개변수*가 아니므로 분배가 일어나지 않는다. 작은 트릭이지만 자주 쓰인다 — *"엄격하게 같은가"*를 확인할 때.

### `Exclude`/`Extract` — 표준에 들어 있는 패턴

조건부 + distributive의 가장 흔한 활용이 *유니온에서 일부를 골라내거나 빼는* 자리다. 표준 라이브러리에 이미 있다.

```ts
type Exclude<T, U> = T extends U ? never : T;
type Extract<T, U> = T extends U ? T : never;

type A = Exclude<"a" | "b" | "c", "b">;  // "a" | "c"
type B = Extract<string | number | boolean, string | number>;  // string | number
```

읽는 법은 똑같다. `T extends U ? … : …`인데, distributive가 작동해서 유니온의 각 멤버가 따로 평가된다. `Exclude`는 *맞으면 버리고*, `Extract`는 *맞으면 남긴다*. `never`로 떨어진 멤버는 유니온에서 *조용히 사라진다* — `string | never`는 `string`이니까.

이 두 도구는 실전에서 매우 자주 쓰인다. *"이 유니온에서 string만 골라줘"*, *"이 유니온에서 null과 undefined만 빼줘"*(`NonNullable`이 그것이다) 같은 자리.

```ts
type NonNullable<T> = T extends null | undefined ? never : T;

type A = NonNullable<string | null | undefined>;  // string
```

자바였다면 `Optional<T>`로 감싸거나 `if (x != null)`로 좁혔겠지만, TS는 *타입 자체*에서 null/undefined를 제거하는 도구를 표준으로 제공한다.

여기까지가 조건부 타입의 모양이다. 모양은 단순하다 — `T extends U ? X : Y`. 그런데 이 단순한 모양 안에, 이 책 통틀어 가장 강력한 키워드 하나가 들어 있다. **`infer`**다.

## 5.5 `infer`의 실전 — `ReturnType`·`Awaited`·직접 만드는 도구들

조건부 타입의 *조건 절 안*에서, 컴파일러에게 *"이 자리의 타입을 잡아서 변수에 담아라"*라고 시킬 수 있다. 그 키워드가 `infer`다. 한 줄로 보자.

```ts
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
```

천천히 읽자.

- `T`가 *함수 타입*인지 본다 — `(...args: any[]) => …`
- 그 *반환 타입* 자리에 `infer R`을 두고 — *"여길 잡아서 `R`이라고 부르자"*
- 잡혔으면 `R`을 돌려주고, 아니면 `never`

```ts
type A = ReturnType<() => number>;             // number
type B = ReturnType<(s: string) => boolean>;   // boolean
type C = ReturnType<string>;                   // never (함수가 아니므로)
```

처음 본 사람은 잠깐 멈춘다. *"잡는다는 게 뭐지? 패턴 매칭 같은 건가?"* 정확히 그렇다. 코틀린의 destructuring이나 Scala의 pattern matching을 떠올리면 된다. *타입의 모양 안에서 특정 자리에 들어오는 타입을 잡아서 변수에 담는* 도구다.

### `Parameters`도 같은 방식

```ts
type Parameters<T> = T extends (...args: infer P) => any ? P : never;

type A = Parameters<(name: string, age: number) => void>;
// [name: string, age: number]
```

이번엔 매개변수 자리를 잡아서 *튜플*로 돌려준다. 함수의 시그니처에서 *입력 부분만* 끌어내는 도구다. 자바·코틀린에는 이런 메타 조작이 없다 — 굳이 비교하자면 reflection으로 `Method.getParameterTypes()`를 호출하는 자리지만, 이건 *컴파일타임*이다.

### `Awaited` — Promise를 *벗기는* 패턴

```ts
type Awaited<T> = T extends Promise<infer U> ? U : T;

type A = Awaited<Promise<string>>;       // string
type B = Awaited<string>;                // string (그냥 통과)
```

`Promise<U>` 모양이면 `U`를 잡아서 돌려준다. *Promise를 한 겹 벗기는 도구*다. 표준 라이브러리에는 더 정교한 버전이 들어 있는데(중첩된 Promise까지 다 벗긴다), 핵심 아이디어는 같다.

이게 `async` 함수의 반환 타입을 다룰 때 자주 쓰인다.

```ts
async function fetchUser(): Promise<User> { /* ... */ }

type FetchedUser = Awaited<ReturnType<typeof fetchUser>>;
// User
```

`typeof fetchUser`로 함수의 타입을 잡고 → `ReturnType`으로 반환 타입(`Promise<User>`)을 꺼내고 → `Awaited`로 한 겹 벗겨서 `User`를 얻는다. *세 도구의 합주*다. 5.2에서 본 *"세 도구가 함께 작동한다"*는 직관이 여기서도 살아 있다.

### 직접 `PromiseValue`를 만들어보자

표준에 있는 도구만 쓰지 말고 직접 만들어보면 감각이 잡힌다.

```ts
type PromiseValue<T> = T extends Promise<infer U>
  ? U extends Promise<any>
    ? PromiseValue<U>   // 중첩된 Promise면 재귀
    : U
  : T;

type A = PromiseValue<Promise<string>>;              // string
type B = PromiseValue<Promise<Promise<number>>>;     // number
type C = PromiseValue<string>;                       // string
```

조건부 타입을 *재귀*로 호출했다. 이게 가능하다는 것 자체가 처음엔 놀랍다. *"타입이 자기 자신을 호출한다고?"* 그렇다. TS 4.1부터 재귀 조건부 타입이 정식으로 지원된다. 5.7에서 더 본다.

### `infer`의 *위치*가 곧 의미다

`infer`의 흥미로운 점은 *어디에 두느냐에 따라 무엇을 잡을지가 결정된다*는 거다.

```ts
// 함수의 첫 번째 인자만 잡기
type FirstArg<T> = T extends (first: infer F, ...rest: any[]) => any ? F : never;

// 배열의 원소 타입 잡기
type ElementOf<T> = T extends (infer U)[] ? U : never;

// 객체의 특정 필드 타입 잡기
type IdOf<T> = T extends { id: infer I } ? I : never;

type A = FirstArg<(s: string, n: number) => void>;  // string
type B = ElementOf<number[]>;                        // number
type C = IdOf<{ id: number; name: string }>;        // number
```

세 줄짜리 도구들이지만, 한 번 손에 익으면 *어떤 모양에서든 원하는 자리를 잡아낼 수 있다*. 자바·코틀린에서는 reflection이나 별도의 코드 생성으로 풀어야 했던 문제를 *타입 한 줄*로 끝낸다.

여기까지 오면 zod·tRPC·Hono의 기둥이 거의 다 보인다. 5.8에서 분해할 때 *"아 이건 `infer`구나"*가 즉시 잡힐 것이다.

## 5.6 템플릿 리터럴 타입 — `\`/api/${string}\``

문자열도 타입이 될 수 있다는 건 4장에서 봤다. `"pending"`, `"done"` 같은 *리터럴 타입*. 그런데 TS 4.1부터 한 발 더 나갔다 — *문자열 리터럴을 조립할 수 있는 문법*이 들어왔다.

```ts
type ApiPath = `/api/${string}`;

const path1: ApiPath = "/api/users";    // OK
const path2: ApiPath = "/api/posts/1";  // OK
const path3: ApiPath = "/users";        // 컴파일 에러
```

JS의 템플릿 리터럴(`${...}`)과 모양이 똑같다. 다만 *값*이 아니라 *타입*을 조합한다. `string`이라는 타입을 *문자열 자리*에 끼워 넣은 셈이다.

이 도구의 진짜 위력은 *유니온과 결합될 때* 나온다.

```ts
type Method = "get" | "post" | "put" | "delete";
type Resource = "users" | "posts" | "comments";

type Route = `${Method} /${Resource}`;
// "get /users" | "get /posts" | "get /comments"
// | "post /users" | "post /posts" | "post /comments"
// | ...
// 총 12개 조합
```

`Method`(4개) × `Resource`(3개) = 12개의 *정확한 문자열 유니온*이 자동으로 만들어진다. 손으로 12줄을 적을 일이 없다.

### intrinsic string utility — `Uppercase`·`Lowercase`·`Capitalize`·`Uncapitalize`

TS 4.1과 함께 *내장된 문자열 유틸리티 타입*이 네 개 들어왔다. 이름 그대로다.

```ts
type A = Uppercase<"hello">;       // "HELLO"
type B = Lowercase<"HELLO">;       // "hello"
type C = Capitalize<"hello">;      // "Hello"
type D = Uncapitalize<"Hello">;    // "hello"
```

이게 매핑 타입의 key remapping과 결합되면 *"필드 이름 변환"* 같은 일이 한 줄로 된다. 5.3에서 봤던 `Getters<T>`가 그 자리였다.

```ts
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
```

이 한 줄을 다시 읽어보자. `keyof T`로 키를 꺼내고, `Capitalize`로 첫 글자를 대문자화하고, ``get${...}``으로 접두사를 붙이고, 새 키 자리에 `as`로 표시한다. 자바에서 Lombok이 어노테이션으로 처리하던 *getter 생성*을, TS는 *타입 한 줄*로 표현한다. 런타임 코드 생성도 아니다 — 컴파일타임에 *타입만* 만든다. 실제 메서드 본체는 별개다(보통 Proxy로 구현).

### 패턴 매칭의 자리

템플릿 리터럴 타입은 `infer`와 결합되면 *문자열 패턴 매칭*이 된다.

```ts
type ExtractRoute<T> = T extends `${string} ${infer Path}` ? Path : never;

type A = ExtractRoute<"GET /users">;       // "/users"
type B = ExtractRoute<"POST /api/posts">;  // "/api/posts"
```

문자열의 *공백 뒤 부분*을 잡아서 돌려주는 도구다. `infer Path`가 정확히 그 자리를 잡아낸다. 처음 보면 *"이걸 타입 시스템이 한다고?"* 싶다. 그렇다, 한다.

이 패턴이 Hono의 라우트 정의나 Express의 path parameter 추출 같은 자리에서 핵심적으로 쓰인다 — 5.8에서 보자.

## 5.7 재귀 조건부 타입 — `DeepReadonly`·`Paths`

5.5에서 잠깐 본 *재귀 조건부 타입*을 본격적으로 쓸 차례다. *임의의 깊이를 가진 자료구조*를 다룰 수 있게 해준다.

### `DeepReadonly` — 모든 중첩 필드를 readonly로

표준 `Readonly<T>`는 *얕은* readonly다 — 1단계만 처리한다.

```ts
type Config = {
  api: { url: string; timeout: number };
  retry: number;
};

type A = Readonly<Config>;
// {
//   readonly api: { url: string; timeout: number };  // 안쪽은 readonly가 아니다
//   readonly retry: number;
// }
```

깊이 들어가서 *모든 중첩 필드*를 readonly로 만들고 싶을 때 직접 만든다.

```ts
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object
    ? T[K] extends Function
      ? T[K]
      : DeepReadonly<T[K]>
    : T[K];
};

type A = DeepReadonly<Config>;
// {
//   readonly api: {
//     readonly url: string;
//     readonly timeout: number;
//   };
//   readonly retry: number;
// }
```

핵심은 매핑 타입 안에서 *자기 자신을 재귀 호출*한다는 것. 함수 타입은 빼고(함수도 object라서), 배열·일반 객체에 대해서만 재귀로 들어간다. 이렇게 만들어두면 어떤 깊이의 구조든 한 번에 처리된다.

자바라면? Lombok도 못 한다. 직접 클래스 트리를 다 만들거나 reflection으로 런타임에 freeze해야 한다. *번거로운 일이다.* TS는 타입 한 덩어리로 끝낸다.

### `Paths` — 객체의 경로를 *문자열 유니온으로*

조금 더 야심찬 도구를 만들어보자. *객체의 모든 경로*를 문자열로 표현하는 타입이다.

```ts
type Paths<T> = T extends object
  ? {
      [K in keyof T & string]:
        T[K] extends object
          ? `${K}` | `${K}.${Paths<T[K]>}`
          : `${K}`;
    }[keyof T & string]
  : never;

type Config = {
  api: { url: string; timeout: number };
  retry: number;
};

type P = Paths<Config>;
// "api" | "api.url" | "api.timeout" | "retry"
```

매핑 타입으로 키를 순회하고, 각 키에 대해 *그 키 자체*와 *`키.하위경로`* 형태를 둘 다 만든 뒤, *유니온으로 합친다*. 마지막의 `[keyof T & string]`이 객체의 *값들의 유니온*을 꺼내는 indexed access 트릭이다(5.2의 합주). 재귀 + 매핑 + 인덱스드 액세스 + 템플릿 리터럴이 다 들어 있다.

이런 도구가 실전에서 쓰이는 자리가 *form 라이브러리*다. react-hook-form 같은 곳에서 *필드 경로를 문자열로 받는데 타입은 안전한* 마법이 정확히 이 패턴이다.

```ts
form.setValue("api.url", "https://...");        // OK
form.setValue("api.timeout", 5000);              // OK
form.setValue("api.notExist", "...");           // 컴파일 에러
```

처음 보면 마법 같지만, 부품을 알면 *"아, `Paths<T>`로 키를 끌어내고 indexed access로 값 타입을 잡았구나"*가 보인다. 5.7까지 오면 그 단계다.

### 재귀의 한계 — TS는 *깊이 제한*이 있다

재귀 조건부 타입은 무한히 깊어질 수 없다. TS 컴파일러는 *재귀 깊이 제한*을 걸어둔다(약 50단계). 그 이상으로 가면 *"Type instantiation is excessively deep and possibly infinite"* 에러가 난다.

이건 *기능의 한계가 아니라 안전장치*다. 타입 시스템은 *결정 가능*해야 하니까. 깊은 트리를 다뤄야 한다면 깊이를 *명시적 카운터*로 제한하는 패턴이 정착해 있다.

```ts
type DeepReadonly<T, Depth extends number = 5> =
  Depth extends 0
    ? T
    : { readonly [K in keyof T]: T[K] extends object
        ? DeepReadonly<T[K], Decrement<Depth>>
        : T[K] };
```

이런 자리는 곡예에 가까우니 *현실 코드에서는 거의 안 본다*. 재귀를 쓸 때는 *얕은 깊이로 충분한 자리*에서만 쓰는 편이 낫다 — 라이브러리 설계자가 아니라면 직접 만들 일도 거의 없다. *기억해두자.*

## 5.8 현실 마법의 분해 — zod·Hono·Prisma·tRPC

부품이 다 모였다. 이제 *우리가 매일 보는 코드*를 분해해보자. 5장의 클라이맥스다.

### zod — `z.infer<typeof Schema>`의 부품

처음에 봤던 코드를 다시 본다.

```ts
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().int().nonnegative(),
});

type User = z.infer<typeof UserSchema>;
// { id: string; email: string; age: number }
```

부품을 하나씩 분해해보자.

**부품 1: 스키마는 *값*이다.** `z.object({...})`는 일반 함수 호출이다. 결과는 *런타임 객체* — `parse()`, `safeParse()` 같은 메서드를 가진 객체다.

**부품 2: 그 객체의 *타입*을 `typeof`로 끌어낸다.** `typeof UserSchema`는 *그 객체의 컴파일타임 모양*을 잡는다. zod 내부적으로 이 타입은 대략 이런 모양이다(아주 단순화한 형태다).

```ts
type ZodObject<Shape> = {
  parse: (input: unknown) => OutputOf<Shape>;
  // ... 그 외 메서드들
};
```

여기서 핵심은 — `ZodObject`가 자기가 *어떤 모양의 객체*를 검증하는지를 *타입 매개변수 `Shape`으로 들고 있다*는 것. 그 정보가 컴파일타임에 살아 있다.

**부품 3: `z.infer<T>`로 그 안의 *출력 타입*을 꺼낸다.** zod의 `infer`는 (대략) 이런 모양이다.

```ts
namespace z {
  type infer<T> = T extends ZodType<infer Output> ? Output : never;
}
```

조건부 타입 + `infer`다. `T`(우리 경우 `typeof UserSchema`)가 `ZodType<...>` 모양이면, 그 *내부의 출력 타입*을 잡아서 돌려준다. 5.5에서 본 패턴 그대로다.

세 부품을 합치면 — *값 → typeof로 타입 추출 → infer로 안쪽 타입 잡기*. 이게 zod의 *마법이 아니라 부품 조합*이다.

조금 더 깊이 들어가보자. zod는 매핑 타입까지 동원한다.

```ts
// 단순화한 zod의 내부
type InferShape<S> = {
  [K in keyof S]: S[K] extends ZodType<infer Out> ? Out : never;
};

const schema = z.object({
  id: z.string(),    // ZodString → ZodType<string>
  age: z.number(),   // ZodNumber → ZodType<number>
});

// InferShape<{ id: ZodString; age: ZodNumber }>
// = { id: string; age: number }
```

매핑 타입(`[K in keyof S]`)으로 객체의 각 필드를 순회하고, 조건부 타입과 `infer`로 *각 필드의 zod 타입에서 출력 타입을 끌어낸다*. 한 단계씩 보면 *5.3 + 5.4 + 5.5의 합*이다. 곡예가 아니다.

이제 *왜 zod의 인기가 폭발적이었는지*가 보인다. *값과 타입을 같은 정의에서 끌어낸다*는 패턴은 자바의 Bean Validation으로는 어림도 없는 표현력이다. 한 번 정의하면 컴파일타임 타입과 런타임 검증이 *같이* 따라온다.

### Hono — 라우트 → RPC 클라이언트의 부품

Hono의 마법을 보자.

```ts
// 서버
const app = new Hono()
  .get("/users/:id", (c) => {
    const id = c.req.param("id");
    return c.json({ id, name: "Toby" });
  });

export type AppType = typeof app;
```

```ts
// 클라이언트
import { hc } from "hono/client";
import type { AppType } from "../server";

const client = hc<AppType>("http://localhost:3000");

const res = await client.users[":id"].$get({ param: { id: "1" } });
const data = await res.json();
// data: { id: string; name: string }   ← 자동 추론
```

서버에서 한 일이라곤 *라우트 정의*뿐이다. 클라이언트는 그 라우트를 *원격 함수처럼 호출*하는데, 인자와 반환 타입이 정확히 맞아 들어간다. *"이게 어떻게 되지?"*

부품을 분해하자.

**부품 1: `Hono` 클래스가 자기 *라우트 정보를 타입 매개변수에 누적*한다.** Hono의 `.get()`, `.post()` 같은 메서드는 호출할 때마다 *반환 타입에 자기를 추가한 새 Hono를 돌려준다*. 단순화하면 이런 모양이다.

```ts
class Hono<Routes = {}> {
  get<Path extends string, Handler>(
    path: Path,
    handler: Handler,
  ): Hono<Routes & { [K in Path]: { get: { response: ReturnType<Handler> } } }> {
    // ...
  }
}
```

매번 새 Hono를 돌려줄 때 *제네릭 매개변수에 라우트 정보를 누적*한다. 메서드 체이닝(`.get().post().put()`)이 끝나면 결과 Hono는 *모든 라우트의 타입 정보*를 자기 안에 들고 있다.

**부품 2: `typeof app`으로 그 누적된 정보를 *통째로 추출*한다.** 5.2에서 본 그 `typeof`다. 이걸 `AppType`이라는 이름으로 export하면 *서버의 라우트 정보*가 *순수 타입*으로 클라이언트에 전달된다.

**부품 3: `hc<AppType>()`이 그 정보로 *프록시 클라이언트*를 만든다.** 클라이언트 쪽 `hc`는 런타임에는 `Proxy` 객체이고, 컴파일타임에는 `AppType`의 *모양을 그대로 따라가는* 타입 함수다. 매핑 타입으로 라우트 키를 순회하고, 각 라우트의 `request`/`response` 타입을 *조건부 + infer*로 끌어낸다.

부품 셋이 합쳐지면 — *서버에서 정의한 라우트의 타입이 클라이언트에 그대로 흐른다*. *런타임 코드 생성도, 빌드 단계의 codegen도 없다*. 순수 타입 시스템 안에서 일어나는 일이다.

이 패턴이 가능한 *근본 이유*가 두 가지다.

첫째, **TS의 타입 시스템이 *튜링 완전*에 가깝다**(공식적으로는 sound가 아니지만 충분히 강력하다). 임의의 변형을 타입 수준에서 표현할 수 있다.

둘째, **TS는 라이브러리 작성자가 *프레임워크 수준의 마법*을 만들 수 있게 설계되었다**. 자바였다면 annotation processor + 코드 생성으로 풀어야 했을 일이 *타입만으로* 가능하다.

### Prisma — 생성된 타입의 형태

Prisma는 조금 다른 자리에 있다 — *codegen*을 쓴다.

```prisma
// schema.prisma
model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
}
```

`prisma generate`를 돌리면 `node_modules/.prisma/client/`에 자동 생성된 TS 파일들이 만들어진다. 그 안에 이런 타입들이 들어 있다(아주 단순화한 형태).

```ts
type User = {
  id: number;
  email: string;
  name: string | null;
};

type UserCreateInput = Omit<User, "id"> & {
  // id는 autoincrement이므로 입력에서 제외
};

type UserWhereInput = {
  id?: IntFilter | number;
  email?: StringFilter | string;
  name?: StringNullableFilter | string | null;
};

type UserDelegate = {
  findUnique<T extends UserFindUniqueArgs>(args: T): Promise<...>;
  findMany<T extends UserFindManyArgs>(args: T): Promise<...>;
  // ...
};
```

여기서 흥미로운 자리는 — Prisma가 *타입을 100% 코드 생성*으로 만들지만, 그 *생성된 타입의 모양*이 우리가 5장에서 본 도구의 합이라는 점. `Omit`, 매핑 타입(`Partial`-like 변환), 조건부 타입(`Filter` 변형), `infer`(`include`/`select`로 결과 모양을 좁히는 자리) — 다 들어 있다.

특히 `select`/`include`의 마법이 인상적이다.

```ts
const user = await prisma.user.findUnique({
  where: { id: 1 },
  select: { id: true, email: true },
});
// user: { id: number; email: string } | null
//                                       ^^ name이 없다
```

`select`로 골라낸 필드만 *결과 타입에 포함*된다. 이건 `select` 객체의 키를 *조건부 + 매핑 타입*으로 다시 잡아내는 도구가 Prisma 안에 들어 있다는 뜻이다. 단순화하면 이런 모양이다.

```ts
type SelectResult<Model, Select> = {
  [K in keyof Select & keyof Model as Select[K] extends true ? K : never]: Model[K];
};
```

매핑 타입의 key remapping(`as`) + 조건부 타입(`Select[K] extends true`)으로 *true로 고른 키만 결과에 포함*시킨다. 5.3과 5.4의 합이다.

### tRPC — procedure 타입의 추출

마지막으로 tRPC를 보자. Hono와 비슷하지만 *순수 함수 호출 모양*에 더 집중한다.

```ts
// 서버
import { initTRPC } from "@trpc/server";
import { z } from "zod";

const t = initTRPC.create();

const appRouter = t.router({
  user: {
    getById: t.procedure
      .input(z.object({ id: z.number() }))
      .query(({ input }) => {
        return { id: input.id, name: "Toby" };
      }),
  },
});

export type AppRouter = typeof appRouter;
```

```ts
// 클라이언트
import { createTRPCProxyClient } from "@trpc/client";
import type { AppRouter } from "../server";

const client = createTRPCProxyClient<AppRouter>({ /* ... */ });

const user = await client.user.getById.query({ id: 1 });
// user: { id: number; name: string }   ← 자동
```

부품은 Hono와 거의 같다.

- 서버에서 `appRouter`라는 *값*을 만들고
- `typeof appRouter`로 *타입을 추출해서* `AppRouter`로 export
- 클라이언트에서 `createTRPCProxyClient<AppRouter>`로 *그 모양을 따라가는 프록시*를 만든다

내부적으로는 router의 각 procedure에서 *`input`의 zod 스키마*에서 입력 타입을, *`query`/`mutation`의 반환값*에서 출력 타입을 추출한다. 5.5의 `infer`가 정확히 그 자리에서 일한다.

```ts
// 단순화한 tRPC 내부
type ProcedureInput<P> = P extends { _input: infer I } ? I : never;
type ProcedureOutput<P> = P extends { _output: infer O } ? O : never;
```

여기까지 분해하고 나면 *"아, 이게 마법이 아니라 부품 조합이구나"*가 손에 잡힌다. zod·Hono·Prisma·tRPC가 각자 다른 모양으로 같은 도구를 쓴다. 매핑 + 조건부 + `infer` + 템플릿 리터럴. 5.1부터 차근차근 올라온 부품들이다.

이 직관 하나만 남기자. *현실 코드의 마법은 부품의 조합이지 새 마법이 아니다.* 다음에 처음 보는 라이브러리를 만나서 *"이게 어떻게 되지?"* 싶을 때, 그 안에 매핑 타입이 있는지, 조건부 + infer가 있는지, 템플릿 리터럴이 있는지를 의심해보자. *대부분 답이 거기 있다.*

## 5.9 `as`의 윤리 — 쓰지 않고 끝내는 6가지 길

5장의 호흡을 잠시 바꾸자. 도구 이야기를 이어가다가, 한 자리에서 *우리가 매일 마주치는 유혹*에 대해 솔직하게 이야기하고 싶다. *타입 단언(`as`)*이다.

```ts
const data = await fetch("/api/user").then((r) => r.json()) as User;
```

이 한 줄이 *왜* 찜찜한가?

`fetch().json()`의 반환 타입은 `Promise<any>`다. 그걸 `as User`로 *그냥 단언*하면 컴파일러는 입을 다문다 — *"네가 User라고 했으니 User로 알겠다"*. 그런데 런타임에 진짜 `User` 모양이 올지는 *아무도 모른다*. API가 어제까지 `name`을 주다가 오늘부터 `fullName`을 주기로 바꿨을 수도 있다. 컴파일러는 모른다. 거짓말 위에 빌드된 빌딩 같은 자리다.

그래서 커뮤니티에는 *"`as`는 거짓말이다"*라는 강한 입장이 있고, *"필요할 땐 써야 한다"*는 절충 입장이 있다. 둘 다 일리가 있다. 5장의 입장은 *중간*이다. **`as`를 쓰면 죄짓는 건 아니지만, 안 쓸 수 있다면 안 쓰는 편이 낫다.** 그 *안 쓰는 길*을 먼저 보고, 그래도 *써야 하는 자리* 셋을 짚자.

### 안 쓰고 끝내는 6가지 길

**길 1: 사용자 정의 type predicate.** 4장에서 본 도구다. *"이 값이 이 타입인지 확인하는 함수를 만들고 그 결과를 컴파일러가 신뢰하게 한다"*.

```ts
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value
  );
}

const data = await fetch("/api/user").then((r) => r.json());
if (isUser(data)) {
  // data: User
}
```

`as`를 *런타임 검증으로 대체*했다. 검증 함수를 한 번 만들어두면 어디서든 재사용한다. *번거롭다*고 느낄 수 있는데, 그 번거로움이 사실은 *타입 시스템이 보장하지 못하는 자리를 명시*하는 안전장치다.

**길 2: 런타임 스키마(zod·valibot).** 5.8에서 본 자리다. type predicate를 손으로 적는 대신 스키마로 적고, 검증과 타입 추출을 한 객체로 묶는다.

```ts
const User = z.object({ id: z.number(), name: z.string() });

const data = User.parse(await fetch("/api/user").then((r) => r.json()));
// data: User (검증 통과한 결과)
```

`as`가 사라졌다. 외부 입력의 *경계*에서 zod로 검증하면 내부 코드는 *타입을 신뢰*해도 된다. 커뮤니티 합의가 정착한 *boundary validation* 패턴이다.

**길 3: 제네릭으로 흘려 보내기.** *"내가 알아야 하는 타입"*이 아니라 *"호출자가 정해줄 타입"*이라면 제네릭으로 받는 게 낫다.

```ts
// Bad
function unwrap(promise: Promise<unknown>): User {
  return promise as unknown as User;
}

// Good
async function unwrap<T>(promise: Promise<T>): Promise<T> {
  return await promise;
}
```

타입을 *결정하는 책임*을 호출자에게 넘긴다. 함수 본체는 *어떤 타입이 올지 알 필요가 없다*. `as`가 *모름을 숨기는* 도구라면, 제네릭은 *모름을 정직하게 표현하는* 도구다.

**길 4: discriminated union으로 좁히기.** 4장에서 본 분별 유니온을 다시 떠올리자. *"이 값이 어떤 종류인지 `kind` 필드로 표시"*해두면 컴파일러가 자동으로 좁힌다.

```ts
type ApiResult =
  | { kind: "success"; data: User }
  | { kind: "error"; message: string };

function handle(result: ApiResult) {
  if (result.kind === "success") {
    result.data.name;  // OK — User로 좁혀짐
  } else {
    result.message;    // OK — error로 좁혀짐
  }
}
```

`as`로 *어느 분기인지 단언*하지 않아도 된다. 분기 자체가 자기 타입을 *선언*한다.

**길 5: `satisfies` 연산자(TS 4.9+).** 4장에서 본 *"타입을 좁히지 않으면서 만족 여부만 검사하는"* 도구다.

```ts
// Bad
const config = {
  apiUrl: "https://...",
  timeout: 5000,
} as Config;
// config의 구체 타입이 Config로 *넓어진다* (apiUrl: string으로)

// Good
const config = {
  apiUrl: "https://...",
  timeout: 5000,
} satisfies Config;
// config의 타입은 그대로 유지되면서, Config 모양인지 *검사만* 한다
```

`as`가 *넓힘*이라면 `satisfies`는 *검사*다. 리터럴 타입을 잃지 않으면서 호환성만 확인한다. *익혀두면 `as`의 70%를 대체할 수 있다.*

**길 6: 함수 시그니처 다시 보기.** 가장 자주 놓치는 자리다. *"왜 여기서 `as`를 써야 했지?"*를 거꾸로 물어보면, 사실은 *함수 시그니처가 너무 좁거나 너무 넓다*는 답이 나오는 경우가 많다. 시그니처를 다시 잡으면 `as`가 사라진다.

```ts
// Bad
function process(input: unknown) {
  const user = input as User;  // 매번 단언
  // ...
}
const user1 = process(data);  // 호출자도 결과 타입을 모름

// Good
function process<T extends User>(input: T): T {
  // ...
}
const user1 = process(data);  // 호출자가 정확한 타입을 받음
```

타입 설계 한 번에 `as` 다섯 개가 사라진다. *번거로워 보이지만 한 번이다.*

### 그래도 `as`가 필요한 3가지 자리

이 *6가지 길*을 다 시도해도 `as`를 써야 하는 자리가 있다. 셋이다.

**자리 1: 컴파일러가 *추론할 수 없는 형변환*.** 가령 *유니온의 한 분기를 강제로 좁혀야 하는데 좁힐 정보가 코드에 없는* 자리.

```ts
const button = document.querySelector(".submit") as HTMLButtonElement;
button.disabled = true;
```

`querySelector`의 반환 타입은 `Element | null`이다. *우리는 `.submit`이 button임을 알지만 컴파일러는 모른다*. 이런 자리는 솔직하게 `as`로 표시한다. 다만 한 번 더 살펴보자 — `instanceof HTMLButtonElement`로 *체크 후 좁히는 길*이 더 안전한 경우가 많다.

**자리 2: 타입 시스템의 *표현 한계*를 만났을 때.** 라이브러리 작성자라면 가끔 마주치는 자리다. *복잡한 매핑 타입의 결과가 컴파일러에는 너무 일반적으로 잡혀서, 안다는 사실을 단언으로 표시*해야 할 때.

```ts
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>;  // 빈 객체에서 시작
  for (const key of keys) {
    result[key] = obj[key];
  }
  return result;
}
```

빈 객체 `{}`는 `Pick<T, K>`가 *아니다*. 우리가 *루프를 다 돌면 그 모양이 된다*는 걸 알지만, 컴파일러는 따라오지 못한다. 이런 자리에서 `as`는 *프로그래머가 책임지는 작은 거짓말*이다. 함수가 작고 검증 가능한 범위에서만 쓰자.

**자리 3: 마이그레이션 중인 *임시 자리*.** 9장에서 다룰 자바스크립트 → 타입스크립트 마이그레이션 도중에는 *모든 자리를 한 번에 정확히 잡을 수 없다*. 임시로 `as`를 쓰고 *주석으로 TODO*를 남긴 뒤, 다음 PR에서 풀어내는 패턴이 합리적이다.

```ts
// TODO: replace with zod schema before v2 release
const user = legacyData as User;
```

*"`as`를 쓰는 것 자체가 죄"*는 아니다. *"왜 썼는지를 설명할 수 있는가, 안 쓸 길을 충분히 시도했는가"*가 기준이다.

> ### 💡 작가의 한 마디 — `as unknown as X`를 줄이는 다섯 가지 길
>
> *`as unknown as X`*. 한 번이라도 손가락이 이 모양으로 움직여본 적 있다면 알 것이다. *컴파일러가 `as X`를 막을 때 `unknown`을 거쳐가는 우회로*다. 두 번 캐스팅하면 컴파일러는 입을 다문다 — *"네가 그렇게까지 말한다면 어쩔 수 없다"*. 절대 그게 *허락*은 아니다. *"코드를 통과시키되 너의 책임"*이라는 *마지막 경고*다.
>
> 이걸 줄이는 다섯 가지 길을 권하고 싶다.
>
> **첫째, 의심하자.** `as unknown as X`가 보이면 *2분만* 멈춰서 묻는다. *"이 자리에 진짜 X가 올 거라는 보장이 어디에 있나?"* 답이 *"내가 그냥 안다"*면 위험 신호다. 답이 *"위에서 zod로 검증했다"*면 안전하다.
>
> **둘째, 경계를 가능한 한 안쪽으로 옮기자.** 외부 입력이 들어오는 자리에서 *한 번* 검증하고, 그 안쪽 코드는 타입을 *신뢰*한다. `as`가 *경계 한 자리*에만 모이면 감당 가능한 위험이 된다. 코드 곳곳에 흩어져 있다면 *어디서 거짓말이 시작됐는지* 알 수 없다.
>
> **셋째, 라이브러리의 타입 정의를 의심하자.** `@types/...`가 너무 넓게 잡혀 있어서 `as`가 필요해지는 경우가 자주 있다. 그런 자리는 *라이브러리에 PR을 보내거나*, 자기 프로젝트에 *type augmentation*(5.10에서 다룬다)으로 좁힌다. *"내 코드가 잘못한 게 아니라 타입 정의가 부족한 거였구나"*가 답인 경우가 의외로 많다.
>
> **넷째, 큰 함수를 쪼개자.** 한 함수에서 `as`가 두 번 이상 나오면 *함수가 너무 많은 일을 한다*는 신호다. 책임을 나누면 각 작은 함수가 *명확한 입출력 타입*을 가지게 되고, 거짓말이 사라진다.
>
> **다섯째, *나중*을 신뢰하지 말자.** *"일단 `as`로 통과시키고 나중에 고쳐야지"*라고 적은 코드는, *나중에 고치지 않는다*. 실험으로 증명된 바가 있다(농담이지만 진짜다). `// TODO: fix this`가 영원히 남는 자리들. *지금* 작은 시도를 한 번 더 해보는 편이 낫다.
>
> *`as`는 도구다.* 도구를 잘 쓴다는 건 *언제 쓰지 않을지를 안다*는 뜻이다. TS의 타입 시스템이 강력해진 만큼, *`as` 없이 끝나는 자리*가 매년 넓어지고 있다. 그 흐름을 타자.

## 5.10 declaration merging과 module augmentation — Express의 `Request.user`

마지막 절이다. *현실에서 가장 자주 보는* 자리 하나를 짚고 챕터를 닫자. **선언 병합(declaration merging)**과 **모듈 보강(module augmentation)**이다.

자바·코틀린에는 이런 개념이 없다. *"같은 이름의 타입을 두 곳에 적으면 컴파일러가 합쳐준다"*는 발상이 어색할 수 있다. 그런데 TS는 *이게 된다*. JS의 동적 본성과 TS의 타입 시스템을 잇는 자리에서 합리적이기도 하다.

### 단순한 declaration merging

```ts
interface User {
  id: number;
  name: string;
}

interface User {
  email: string;
}

// 합쳐진 결과
// interface User { id: number; name: string; email: string }
```

같은 이름의 `interface`를 두 번 적으면 *합쳐진다*. `type`은 안 된다 — `type`은 별칭이지 선언이 아니라서.

자체로는 큰 의미가 없어 보이지만, 이게 *모듈 경계를 넘어서 작동*한다는 게 실전에서 중요하다.

### module augmentation — *남의 모듈*을 확장한다

Express에서 가장 자주 보는 자리다. Express의 `Request` 객체에 *우리가 만든 미들웨어가 추가한 필드*를 타입으로 표현하고 싶다고 해보자.

```ts
// auth.middleware.ts
app.use((req, res, next) => {
  req.user = { id: 1, name: "Toby" };  // 미들웨어가 user를 붙임
  next();
});

// 라우트
app.get("/me", (req, res) => {
  res.json(req.user);  // 컴파일 에러 — req.user가 타입에 없음
});
```

미들웨어가 런타임에 `req.user`를 *붙이는* 건 자유다. JS는 그걸 막지 않는다. 하지만 TS는 *Express의 `Request` 타입*에 `user` 필드가 없다는 것을 안다. 그래서 컴파일 에러가 난다.

이걸 해결하는 *나쁜 방법*은 매번 `(req as RequestWithUser).user`로 캐스팅하는 것이다. 5.9에서 본 바로 그 *피해야 할 자리*다.

*좋은 방법*이 module augmentation이다.

```ts
// types/express.d.ts
import "express";

declare module "express" {
  interface Request {
    user?: { id: number; name: string };
  }
}
```

이 한 파일을 프로젝트 어딘가에 두면, *Express의 `Request` 타입에 `user` 필드가 추가된다*. 합쳐진다. 코드는 자연스럽게 돌아간다.

```ts
app.get("/me", (req, res) => {
  res.json(req.user);  // OK — req.user는 { id: number; name: string } | undefined
});
```

이게 자바·코틀린에는 없는 자리다. 자바였다면 `Request`를 *상속한 새 클래스*를 만들거나, request에 *attribute로 넣고 키로 꺼내거나*(`request.getAttribute("user")`), 아예 *별도의 컨텍스트 객체*를 들고 다녀야 한다. TS는 *원래 타입을 그 자리에서 확장*한다.

### 흔한 실전 패턴들

module augmentation이 자주 쓰이는 자리는 의외로 많다.

**환경변수 타입.** `process.env`를 타입 안전하게 만들고 싶을 때.

```ts
// types/env.d.ts
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      DATABASE_URL: string;
      JWT_SECRET: string;
      NODE_ENV: "development" | "production" | "test";
    }
  }
}
```

이제 `process.env.DATABASE_URL`이 `string | undefined`가 아니라 그냥 `string`으로 잡힌다. *zod로 한 번 검증한 뒤* 이런 augmentation을 두는 패턴이 흔하다.

**Vite의 `import.meta.env`** 같은 자리도 같은 패턴.

```ts
// vite-env.d.ts
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

**Window 확장.** 글로벌 객체에 라이브러리가 자기를 붙이는 경우가 있다(예: 분석 SDK).

```ts
declare global {
  interface Window {
    gtag: (event: string, ...args: unknown[]) => void;
  }
}
```

각 자리에서 공통점을 보자 — *남이 만든 타입에 우리가 필요한 모양을 덧붙인다*. 자바스크립트의 *open-by-default*한 동적 본성에 *닫힌 타입 시스템*이 적응한 결과다.

### 주의할 자리 — 너무 자주 쓰면 *글로벌 오염*이 된다

module augmentation은 *글로벌 효과*가 있다. 한 곳에서 `Request`에 `user`를 추가하면 프로젝트 전체에서 그 모양이 보인다. 편하지만, *남용하면 어디서 누가 어떤 필드를 추가했는지 추적이 어려워진다*. 끔찍한 일이다.

권장 패턴은 두 가지다.

- **augmentation을 *한 파일에 모은다*.** `types/global.d.ts`나 `types/express.d.ts` 같은 *지정된 자리*에서만 한다. 흩어지지 않게.
- **꼭 필요한 자리에만 쓴다.** 프레임워크가 *진짜로* 동적으로 필드를 붙이는 자리(미들웨어가 추가하는 `req.user` 같은 것)에서만 쓴다. *그냥 새 타입을 만들면 되는 자리*에서는 쓰지 않는다.

이 두 원칙만 지키면 declaration merging은 *현실 코드의 거친 자리*를 매끄럽게 만드는 좋은 도구다.

## 5.11 마무리

5장은 길었다. *깊이*가 약속이었으니 어쩔 수 없다.

지금까지 부품을 하나씩 쌓았다. 제네릭과 제약 → `keyof`/`typeof`/`T[K]`의 합주 → 매핑 타입 → 조건부 타입 → `infer` → 템플릿 리터럴 → 재귀. 그 위에서 zod·Hono·Prisma·tRPC를 분해했다. *현실 코드의 마법은 부품의 조합이지 새 마법이 아니다.* 이게 5장의 한 문장 약속이다.

기억해두자. *제네릭은 함수다*. 입력 타입을 받아서 출력 타입을 돌려주는 함수. 매핑 타입은 *타입 수준의 for 루프*고, 조건부 타입은 *if*고, `infer`는 *패턴 매칭으로 변수에 잡기*다. 이 직관 셋만 남기면 5장의 모든 도구가 한 자리에 정렬된다.

`as`의 윤리 한 절도 함께 기억하자. *쓰면 죄짓는 건 아니지만, 안 쓸 수 있다면 안 쓰는 편이 낫다.* 6가지 길이 있고, 그래도 써야 하는 3가지 자리가 있다. *경계에 모으고, 내부는 신뢰하자.*

declaration merging은 자바·코틀린에 없는 자리지만, *Express·Vite·Node*의 현실 코드를 매끄럽게 만드는 좋은 도구다. 한 파일에 모으고, 꼭 필요할 때만 쓰자.

다음 6장에서는 이 부품들을 *도메인 모델링*에 쓰는 패턴을 본다. branded type·`interface` vs `type`·immutability·*에러를 도메인의 일부로*. 5장이 *부품 사전*이었다면 6장은 *그 부품으로 자기 도메인을 어떻게 표현할까*의 자리다. 결을 잃지 않는 도메인 모델링이라는 약속을 6장이 이어받는다.

> ### 📖 더 깊이 가려면
>
> - **공식 핸드북** — *TypeScript Handbook*의 *Type Manipulation* 섹션 (Generics, Keyof Type Operator, Typeof Type Operator, Indexed Access Types, Conditional Types, Mapped Types, Template Literal Types). 5장의 모든 도구가 1차 자료로 정리되어 있다.
> - **Matt Pocock의 *Total TypeScript*** — *Type Transformations* 워크숍이 5장의 도구를 *문제 풀이로* 익히는 데 가장 효과적인 자료다. 한국어 번역도 일부 있다.
> - **이펙티브 타입스크립트 (Dan Vanderkam)** — *Item 14~22* 가 제네릭과 매핑 타입의 실전 패턴, *Item 27~28*이 `as`와 type guard의 윤리. 한국어 번역본 인사이트 시리즈로 출간.
> - **zod 공식 문서의 *"From Schema to TypeScript"*** — `z.infer<typeof Schema>`의 내부 동작을 라이브러리 작성자 시선에서 정리한 자료. 5.8의 zod 분해를 직접 따라가볼 수 있다.
> - **Hono의 *RPC* 가이드** — Hono의 *type-safe client*가 어떻게 만들어지는지 공식 문서가 단계별로 보여준다. 5.8의 Hono 분해와 짝을 이룬다.
> - **→ 14장에서 `expect-type`으로 *타입 자체를 단위 테스트*하는 패턴을 다룬다.** 5장에서 만든 도구들이 *진짜로 우리가 의도한 모양*을 만들어내는지 *런타임 없이 검증*하는 자리다. 라이브러리 작성자뿐 아니라 큰 프로젝트의 도메인 타입을 다루는 사람도 익혀둘 가치가 있다.
