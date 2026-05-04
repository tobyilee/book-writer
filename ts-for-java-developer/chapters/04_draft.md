# 4장. 타입을 손에 익히기 — 추론·좁히기·exhaustive를 도구로

이런 상황을 한번 떠올려보자. 우리는 TS 프로젝트에 갓 합류해서 첫 PR을 낸다. 함수 안에서 `unknown` 값을 다루면서 익숙한 대로 `as User`로 캐스팅했다. 컴파일도 통과하고 동작도 잘 한다. 그런데 리뷰어가 한 줄을 단다. *"여기 `as` 대신 `in` 연산자로 좁혀주세요."*

낯설다. Java라면 `instanceof User`로 끝났을 일이다. Kotlin이라면 `when`이 알아서 분기를 막아준다. TS는 왜 굳이 `in`이라는 자바스크립트 연산자를 동원하는가? 그리고 그 한 줄이 정말로 우리 코드의 안전성을 끌어올리는가?

3장에서 우리는 *"타입은 컴파일타임의 환상이고 런타임에는 사라진다"*는 차가운 진실을 받아들였다. 그렇다면 그 환상이 만들어내는 *실용적 도구들*은 어디까지 뻗어 있을까? 추론은 어디서 멈추고, 좁히기는 어디까지 똑똑하며, 분기는 어떻게 빠짐없이 막을 수 있을까? 4장은 그 도구들을 손에 들고 *직접 두드려보는* 자리다. 처음에는 어색해도, 한두 번 두드리고 나면 *"오, 이게 이렇게까지 표현되는구나"* 하는 작은 쾌감이 따라온다. 그 쾌감을 챕터의 동력으로 삼아 보자.

## 추론은 어디까지 알아주는가

먼저 가장 기본적인 도구, 타입 추론부터 시작하자. Java 11에서 `var`가 들어왔을 때 우리는 어색해하면서도 *"드디어 우리도 타입을 안 적어도 되는구나"* 하고 안도했다. Kotlin은 처음부터 `val`/`var`로 추론을 적극 활용한다. TS도 비슷해 보인다. 변수에 값을 할당하면 알아서 타입이 잡힌다.

```typescript
let count = 10;        // number로 추론
let name = "Toby";     // string으로 추론
let scores = [90, 85]; // number[]로 추론
```

여기까지는 Java `var`와 거의 같다. 그런데 한 줄 더 적어보자.

```typescript
const greeting = "hello"; // 타입은 number? string? — 답은 "hello"
```

`const`로 선언하면 추론된 타입이 단순한 `string`이 아니라 **리터럴 타입** `"hello"`다. 즉 *그 정확한 문자열만* 들어갈 수 있는 타입으로 좁아진다. Java에서는 상상하기 어려운 좁힘이다. Java의 `final String greeting = "hello";`도 변수의 *값*은 고정되지만, *타입*은 여전히 `String`이다. TS는 변경 불가능성과 추론을 엮어, 더 좁은 타입을 만들어 낸다.

이게 별 차이가 아닌 것 같다면, 다음 예를 보자.

```typescript
function move(direction: "up" | "down" | "left" | "right") {
  // ...
}

let dir = "up";
move(dir); // 에러: string은 "up" | "down" | ... 에 들어갈 수 없다

const dir2 = "up";
move(dir2); // 통과 — dir2의 타입이 "up"이라 union의 한 멤버에 정확히 맞는다
```

`let`으로 잡으면 타입이 `string`으로 *넓혀지고*(widening), `const`로 잡으면 *좁혀진다*. Java로는 떠올리기 힘든 결정이다. *"왜 이렇게 만들었을까?"* 답은 단순하다. 변수의 가변성을 그대로 타입에 반영하는 게 *실용적이기 때문*이다. 어차피 다시 대입할 수 있는 값이라면 `string`으로 두는 편이 낫고, 다시 대입 못 할 값이라면 그 정확한 리터럴이 더 정보가 많다.

> 📚 **Java/Kotlin 시선 박스 ① — Java `var` ↔ TS 추론**
>
> Java 11의 `var`는 *지역 변수에 한해* 우변의 정적 타입을 받아쓴다. `var name = "Toby";`라고 적으면 `name`의 타입은 무조건 `String`이다. 더 좁아지지 않는다. 함수 매개변수, 필드, 반환 타입에는 `var`를 쓸 수 없다.
>
> TS의 추론은 더 멀리 간다. (1) 변수의 가변성(`let` vs `const`)에 따라 *리터럴 타입까지* 좁힌다. (2) 함수의 *반환 타입*도 본문에서 추론한다. (3) 콜백에 들어가는 함수의 *매개변수 타입*도 문맥(contextual typing)으로 추론한다. 즉 `arr.map(x => x * 2)`에서 `x`의 타입은 명시 없이도 잡힌다.
>
> 트레이드오프도 있다. TS의 추론이 너무 적극적이라 *원하지 않는 타입으로 추론되는* 경우가 생긴다. Java처럼 명시적 선언을 강제하지 않으니 IDE가 추론을 잘못하면 사람이 알아채야 한다. 익숙해지기 전까지는 함수의 반환 타입만큼은 명시하는 편이 안전하다.

### 문맥이 추론을 도와준다

함수의 매개변수 타입이 *호출 위치의 문맥*에서 결정되는 일도 자주 있다. 이걸 contextual typing이라 부른다.

```typescript
const numbers = [1, 2, 3];
numbers.map(n => n * 2);
//          ^ n의 타입은 number — 명시 없이도 잡힌다
```

`Array<number>`의 `map`이 받는 콜백 시그니처가 `(value: number) => U`이기 때문에, `n`의 타입은 `map`이 호출되는 그 자리의 문맥으로부터 흘러 들어온다. Java에서는 `stream.map((Integer n) -> n * 2)`처럼 명시하거나, 아니면 그저 람다 매개변수로 두고 끝내야 한다. TS는 그 *유추의 흐름*이 한 단계 더 깊다.

물론 한계도 있다. 함수를 *분리해 따로 정의*하면 문맥이 끊긴다.

```typescript
const double = n => n * 2; // n은 implicit any — strict 모드에서 에러
numbers.map(double);
```

함수가 호출 위치에서 떨어지는 순간 문맥이 사라지므로, 매개변수에 타입을 명시하거나 함수 자체에 타입을 주어야 한다. 추론은 강력하지만 *전능하지는 않다*. 어디까지 알아주는지 감을 잡고, 그 너머에서는 손으로 도와주는 편이 낫다.

### `as const`로 추론을 *얼리기*

리터럴 좁히기를 더 적극적으로 활용하고 싶을 때가 있다. 객체 안의 값까지 전부 리터럴로 잡고 싶다고 해보자.

```typescript
const config = {
  host: "localhost",
  port: 3000,
  protocol: "http",
};
// 추론 결과: { host: string; port: number; protocol: string }
```

각 값이 `string`/`number`로 *넓혀져* 있다. 만약 `protocol`이 정확히 `"http"`라는 사실을 타입에 보존하고 싶다면 `as const`를 붙인다.

```typescript
const config = {
  host: "localhost",
  port: 3000,
  protocol: "http",
} as const;
// 추론 결과: { readonly host: "localhost"; readonly port: 3000; readonly protocol: "http" }
```

객체 전체가 깊이 readonly가 되고, 값은 전부 리터럴로 *얼려진다*. 이 패턴은 의외로 자주 쓴다. 라우팅 테이블, 권한 키 목록, 상태 머신의 상태 집합 등 *값이 곧 타입의 일부인* 자리에 잘 어울린다.

### `satisfies` — 검증은 받되 좁힘은 잃지 않기

여기서 TS 4.9에 들어온 신선한 도구 하나를 만나야 한다. 바로 `satisfies` 연산자다. Java에도 Kotlin에도 없는 자리라, 처음 보면 *"이건 또 뭔가"* 싶다. 천천히 풀어 보자.

상황을 가정해 보자. 우리는 색상 팔레트를 정의하고 싶다. 키는 미리 정해진 색 이름들 중 하나이고, 값은 RGB 배열이거나 해시 문자열이다. 이렇게 적었다고 해 보자.

```typescript
type Color = "red" | "green" | "blue";
type RGB = readonly [number, number, number];

const palette: Record<Color, string | RGB> = {
  red: [255, 0, 0],
  green: "#00ff00",
  blue: [0, 0, 255],
};

palette.red.toUpperCase(); // 에러? 통과? — 통과한다. 그러나 런타임에 폭발한다
```

문제가 보이는가? `palette: Record<Color, string | RGB>`로 *주석을 박는 순간*, 컴파일러는 모든 값이 `string | RGB`라는 사실만 안다. *각 키가 어떤 구체 타입인지*는 잊어버린다. 그래서 `palette.red`가 실은 `RGB`인데도 `string | RGB`로 보이고, `.toUpperCase()`가 `string`의 메서드라 통과해 버린다. *런타임에 가서야 폭발한다.* 난감하다.

그렇다고 주석을 빼면? 이번엔 *키가 `Color`의 멤버인지* 검증을 받지 못한다. 오타를 쳐서 `redd: ...`라고 적어도 컴파일러가 잡아주지 못한다.

이 *둘 다 갖고 싶다*는 욕심에 응답한 게 `satisfies`다.

```typescript
const palette = {
  red: [255, 0, 0],
  green: "#00ff00",
  blue: [0, 0, 255],
} satisfies Record<Color, string | RGB>;

palette.red.toUpperCase();  // 에러 — palette.red는 number[]이지 string이 아니다
palette.red[0];             // 통과 — number
palette.green.toUpperCase(); // 통과 — string
```

`satisfies`는 *"이 객체가 저 타입을 만족하는지 검증해 달라. 단, 변수의 추론된 타입은 객체의 *구체 모양 그대로* 둬라"*고 컴파일러에게 부탁한다. 검증은 받되, 좁힘은 잃지 않는다. 이 한 줄짜리 욕심이 TS 4.9가 풀고 싶었던 문제다.

`satisfies`는 작은 도구지만 한번 익히면 자주 손이 간다. 라우팅 테이블의 핸들러 타입을 검증하면서 각 라우트의 응답 타입은 그대로 유지하고 싶을 때, 환경 변수 객체의 키가 정해진 집합인지 검사하면서 각 값의 정확한 리터럴은 보존하고 싶을 때, 모두 같은 패턴이다. 기억해두자. **타입 주석은 검증과 좁힘을 *맞바꾼다*. `satisfies`는 그 맞바꿈을 *피하게* 해 준다.**

> 💡 **작가의 한 마디 — 주석이냐 `satisfies`냐**
>
> 익숙해지면 손가락이 자동으로 결정한다. *값을 보존하고 싶다면 `satisfies`*. *값보다 인터페이스 계약이 중요하다면 그냥 `: Type`*. 함수 시그니처는 거의 항상 후자, 설정 객체와 룩업 테이블은 거의 항상 전자다. 처음 한 달은 의식적으로 둘을 골라 써 보면, 어느 자리에 어느 도구가 어울리는지 감이 잡힌다.

## strict 모드 — 안전망을 켜고 들어가기

타입 추론이 적극적이라는 말은 *추론된 타입을 사람이 신뢰해도 좋다*는 뜻과 같다. 그런데 그 신뢰는 컴파일러가 *까다롭게 검사할 때만* 성립한다. 매개변수 타입을 못 알아내면 `any`로 슬쩍 넘어가는 컴파일러를 신뢰할 수는 없다. 그래서 TS에는 `strict` 모드가 있다.

`tsconfig.json`에 한 줄 적자.

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

이 한 줄이 켜는 검사가 여러 개다. 그중 셋이 특히 핵심이다.

**`noImplicitAny`** — 매개변수나 변수의 타입을 추론할 수 없을 때 *조용히 `any`로 두지 말고* 에러를 내라. 이게 꺼져 있으면 위에서 본 `const double = n => n * 2;` 같은 코드가 통과해 버린다. `n`이 `any`니까 무슨 짓이든 할 수 있고, 무슨 버그든 들어올 수 있다. 끔찍한 일이다.

**`strictNullChecks`** — `null`과 `undefined`를 *모든 타입에 묻혀 다니는 그림자*로 두지 말고 명시적 멤버로 다뤄라. Kotlin의 `null safety`와 의미가 거의 같다. `string`은 `null`이 들어갈 수 없고, `null`을 허용하려면 `string | null`이라고 *적어야* 한다. 이게 꺼져 있으면 `null` 참조 오류가 컴파일 단에서 새 나간다. Java로 넘어온 사람이라면 NPE의 악몽이 떠올라 등이 서늘해질 자리다.

**`strictFunctionTypes`** — 함수 매개변수의 변성(variance)을 *제대로* 검사하라. 끄면 매개변수가 bivariant로 동작해 안전하지 않은 대입이 통과한다. 자세한 내용은 이 장 마지막 절에서 다시 풀자. 일단 *기본으로 켜는 게 좋다*는 정도로 기억해두자.

세 옵션은 `strict: true` 한 줄로 한 번에 켜진다. 한국 커뮤니티에서 *"PR 받자마자 strict 켜라"*는 말이 회자되는 데에는 이유가 있다. strict 없이 자란 코드는 시간이 지날수록 `any`가 곳곳에 박혀서 *나중에 켜기가 더 힘들다*. 신규 프로젝트라면 첫날부터 켜고 시작하자. 기존 프로젝트라면 9장의 점진 마이그레이션 패턴을 활용하면 된다.

> 📖 더 깊이 들어가는 옵션들은 *부록 B. tsconfig 옵션 사전*에 정리해 두었다. Matt Pocock의 "TSConfig Cheat Sheet"가 매우 좋은 출발점이다 — `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`처럼 strict에는 안 들어가지만 *켜면 한 단계 더 안전해지는* 옵션을 잘 정리해 두었다.

## 좁히기 — 컴파일러와 함께 추리하기

이제 4장의 핵심 절로 들어가자. 타입 좁히기, 즉 narrowing이다.

상황을 하나 가정하자. 어떤 함수가 `string | number`를 받는다. 우리는 그 안에서 *문자열일 때만* 길이를 출력하고 싶다.

```typescript
function printLength(value: string | number) {
  console.log(value.length); // 에러 — number에는 length가 없다
}
```

당연히 안 된다. `value`가 *둘 중 하나*라는 사실만 알 뿐, 실제로 어느 쪽인지 모르는 상태다. 어떻게 좁힐까? Java라면 `if (value instanceof String)`을 적었을 것이다. TS에서도 비슷하지만 *`typeof`*를 쓴다.

```typescript
function printLength(value: string | number) {
  if (typeof value === "string") {
    console.log(value.length); // 통과 — value는 이 블록 안에서 string으로 좁혀졌다
  } else {
    console.log(value.toFixed(2)); // value는 number로 좁혀졌다
  }
}
```

`typeof`는 자바스크립트의 런타임 연산자다. 여기에 TS 컴파일러가 *흐름 분석*을 얹어, `if` 블록 안에서 변수의 타입을 *정확히* 좁힌다. Java 14의 패턴 매칭 instanceof와 정신적으로 비슷하지만, TS는 더 일찍부터 더 적극적으로 이 일을 해 왔다. 이 *컴파일러와 함께 하는 추리*가 좁히기의 본질이다.

좁히기에 쓰이는 도구는 여럿이다. 하나씩 살펴보자.

### `typeof` — 원시 타입을 식별

`typeof`는 자바스크립트의 원시 타입 7가지(`"string"`, `"number"`, `"bigint"`, `"boolean"`, `"symbol"`, `"undefined"`, `"object"`, `"function"`) 중 하나를 반환한다. union의 멤버가 *원시 타입*일 때 가장 자주 쓴다.

```typescript
function format(input: string | number | boolean) {
  if (typeof input === "boolean") return input ? "yes" : "no";
  if (typeof input === "number") return input.toFixed(2);
  return input.toUpperCase(); // 여기에서 input은 string으로 좁혀졌다
}
```

위 코드에서 마지막 `return` 시점에 `input`이 `string`으로 좁혀진 것에 주목하자. 앞에서 `boolean`과 `number`를 *쳐냈으니* 남은 가능성은 `string` 하나다. 컴파일러가 이 흐름을 따라간다. 이 *흐름 기반 좁히기*(control flow narrowing)는 이 장에서 우리가 만나는 모든 도구의 공통 기반이다.

### `instanceof` — 클래스 인스턴스를 식별

class 인스턴스를 다룰 때는 Java와 똑같이 `instanceof`를 쓴다.

```typescript
class HttpError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

function handle(err: Error | HttpError) {
  if (err instanceof HttpError) {
    console.log(err.status); // 통과 — HttpError로 좁혀졌다
  } else {
    console.log(err.message); // 통과 — 그냥 Error
  }
}
```

여기까지는 Java와 거의 같아 보인다. 하지만 *주의해야 한다*. TS는 구조적 타입 시스템이라 `instanceof`로 좁힌 결과가 우리 직관과 다를 수 있고, 무엇보다 *interface로 정의된 타입*에는 `instanceof`를 쓸 수 없다. interface는 컴파일타임에만 존재하니까. 이때 등장하는 게 다음 도구다.

### `in` — 멤버의 *존재*로 식별

interface로 정의된 두 타입을 갈라야 한다고 해 보자.

```typescript
interface Cat { meow(): void; }
interface Dog { bark(): void; }

function speak(animal: Cat | Dog) {
  if ("meow" in animal) {
    animal.meow(); // Cat으로 좁혀졌다
  } else {
    animal.bark(); // Dog로 좁혀졌다
  }
}
```

`in`은 자바스크립트에서 *객체에 그 키가 있는지*를 묻는 연산자다. TS는 이 검사를 타입 좁히기로 활용한다. interface로 정의된 *모양*만 다른 두 타입을 가르는 가장 직관적인 도구다. Java라면 두 타입을 공통 부모 인터페이스로 묶거나 `instanceof`를 동원해야 했을 자리에서, TS는 *멤버의 존재* 하나로 가른다. 이게 구조적 타입 시스템의 *재미*다.

### equality narrowing — 값으로 좁히기

`===`와 `!==`도 좁히기에 쓰인다. union의 멤버가 *리터럴 타입*일 때 특히 강력하다.

```typescript
function move(direction: "up" | "down" | "left" | "right") {
  if (direction === "up") {
    // direction은 "up"으로 좁혀졌다
  } else {
    // direction은 "down" | "left" | "right"로 좁혀졌다
  }
}
```

이 좁힘은 다음 절의 분별 유니온에서 *주연*으로 등장한다.

### type predicate — 사용자 정의 좁힘

표준 도구로는 좁히지 못하는 자리가 있다. 예컨대 *런타임에 객체의 모양을 검사하는* 사용자 정의 함수의 결과를 좁힘에 활용하고 싶을 때다. 이때 쓰는 게 type predicate다. 함수의 반환 타입에 `arg is Type` 형태의 *predicate*를 적는다.

```typescript
interface User {
  id: string;
  email: string;
}

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "email" in value &&
    typeof (value as any).id === "string" &&
    typeof (value as any).email === "string"
  );
}

function greet(input: unknown) {
  if (isUser(input)) {
    console.log(`Hello, ${input.email}`); // input은 User로 좁혀졌다
  }
}
```

`isUser`가 `true`를 반환하면, 호출 위치에서 `input`의 타입이 `User`로 좁혀진다. *컴파일러는 함수 본문이 진짜로 그 검사를 제대로 하는지 확인하지 않는다* — 우리가 *약속*한 것이다. 그래서 type predicate는 *조심해 작성해야* 한다. 검사가 부실하면 거짓 약속이 되고, 그 거짓 약속은 런타임에 폭발한다. 찜찜한 자리지만, *경계(boundary)*에서 외부 데이터를 받아들일 때 꼭 필요한 도구다.

> 🚧 **함정 박스 — `as` 대신 `is`로 가는 길**
>
> Java에서 넘어온 사람의 첫 본능은 `as User`다. *"아 그냥 캐스팅하면 되잖아"*. 그런데 TS의 `as`는 *컴파일러를 속이는* 행위에 가깝다. 검증 없이 *그렇다고 우기는* 것이고, 우긴 게 사실이 아니면 런타임에 폭발한다.
>
> type predicate는 *우김을 검증으로 바꾸는* 도구다. `as User` 대신 `if (isUser(value))`로 들어가면, (1) 검증 로직이 한 곳에 모이고, (2) 컴파일러가 좁힘을 보장하고, (3) 호출 측은 `as` 없이 안전하게 멤버에 접근한다. 신규 코드를 쓸 때 `as`가 손에 잡히면, *type predicate로 바꿀 수 있는지* 한 번만 더 생각해보자. 거의 모든 자리에서 가능하다.
>
> 그래도 `as`가 정말 필요한 자리도 있다. 5장에서 그 *세 가지 자리*를 정리한다.

> 📚 **Java/Kotlin 시선 박스 ② — Kotlin smart cast ↔ TS narrowing**
>
> Kotlin의 smart cast는 TS narrowing의 직계 친척이다. `if (animal is Cat) { animal.meow() }`에서 `animal`이 `Cat`으로 자동 캐스팅되는 그 장면, TS의 `if (animal instanceof Cat)`과 거의 같다.
>
> 차이는 두 가지다. 첫째, **검사 도구가 더 다양하다.** Kotlin은 `is`/`!is` 중심이지만, TS는 `typeof`, `instanceof`, `in`, `===`, type predicate를 모두 좁힘에 활용한다. interface처럼 *런타임에 존재하지 않는* 타입까지 가를 수 있는 건 `in`과 type predicate 덕분이다.
>
> 둘째, **재할당의 영향이 다르다.** Kotlin에서는 `var`로 선언된 변수를 다른 스레드가 변경할 수 있다는 가정 때문에 smart cast가 막히는 경우가 있다. TS는 단일 스레드 모델이라 변수 재할당만 하지 않으면 좁힘이 유지된다. 다만 *클로저로 변수를 캡처해 비동기로 호출*하면 좁힘이 풀린다는 점은 양쪽 모두 비슷한 함정이다.
>
> 결론은 같다. 캐스팅 대신 *검사*로 좁히고, 좁혀진 변수를 *그 블록 안에서만* 신뢰하자.

## 분별 유니온과 `never` — Kotlin sealed의 TS식 표현

이제 4장의 *진짜 재미*가 시작된다. Kotlin 개발자라면 sealed class에 익숙할 것이다.

```kotlin
sealed class Shape
data class Circle(val radius: Double) : Shape()
data class Square(val side: Double) : Shape()
data class Triangle(val base: Double, val height: Double) : Shape()

fun area(shape: Shape): Double = when (shape) {
    is Circle -> Math.PI * shape.radius * shape.radius
    is Square -> shape.side * shape.side
    is Triangle -> 0.5 * shape.base * shape.height
} // when이 exhaustive — Triangle을 빼먹으면 컴파일 에러
```

세 가지가 이 한 묶음의 마법이다. 첫째, *대안의 집합이 닫혀 있다*(sealed). 둘째, *각 분기에서 자동 캐스팅*된다(smart cast). 셋째, *분기가 빠짐없이 다뤄졌는지를 컴파일러가 보장한다*(exhaustive).

TS에는 sealed class가 없다. 그렇다면 같은 보장을 어떻게 받아낼까? 답이 **분별 유니온(discriminated union)**이다.

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius * shape.radius;
    case "square":
      return shape.side * shape.side;
    case "triangle":
      return 0.5 * shape.base * shape.height;
  }
}
```

각 멤버가 공통 리터럴 필드(`kind`)를 가지고, 그 필드의 *값*이 다른 멤버끼리 다르다. 이 필드를 **discriminant**(분별자)라고 부른다. `switch (shape.kind)`로 분기하면, 각 `case` 블록 안에서 `shape`이 해당 모양으로 *자동으로 좁혀진다*. Kotlin의 `is` smart cast와 정신은 같지만, TS는 *값의 같음*으로 좁힌다(equality narrowing).

여기까지는 좋다. 그런데 *exhaustive*는? 위 코드에서 만약 새로운 모양 `Pentagon`을 추가하고 area 함수를 까먹으면 어떻게 될까? *컴파일이 그냥 통과한다.* 함수의 반환 타입이 명시되지 않았다면 `undefined`가 흘러나오고, 명시되어 있다면 *반환이 누락된* 에러가 어디선가 한 줄 뜰지도 모른다. 찜찜하다.

이 자리에 등장하는 게 `never` 타입과 *exhaustiveness check* 패턴이다.

```typescript
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${JSON.stringify(x)}`);
}

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius * shape.radius;
    case "square":
      return shape.side * shape.side;
    case "triangle":
      return 0.5 * shape.base * shape.height;
    default:
      return assertNever(shape); // shape이 never가 아니면 컴파일 에러
  }
}
```

`default` 분기에서 `assertNever(shape)`를 호출한다. 이 함수의 매개변수 타입은 `never`다. *모든 `case`를 다뤘다면* 컴파일러는 `default`에 도달한 시점의 `shape`을 `never`로 좁힌다 — 더 이상 가능한 값이 없으니까. `never`는 `never`에 *대입할 수 있으므로* 컴파일 통과.

만약 새 모양 `Pentagon`을 추가하고 `case "pentagon"`을 빼먹는다면? 컴파일러는 `default` 분기에서 `shape`이 `{ kind: "pentagon"; ... }`으로 좁아진 상태임을 알아챈다. 그건 `never`가 아니다. 따라서 `assertNever(shape)`에 *컴파일 에러*가 뜬다. **컴파일러가 우리 대신 빠짐없이 분기했는지 확인해 준다.** Kotlin `when`의 exhaustive와 *동일한 효과*를 다른 도구로 얻은 것이다.

이걸 처음 두드려보면 *"오, 이게 표현되는구나"* 하는 그 감탄이 나온다. 도메인의 *닫힌 대안 집합*을 union 리터럴로 표현하고, 그 위에 `assertNever`를 세워 두면, 새 멤버를 추가했을 때 *고쳐야 할 모든 자리*를 컴파일러가 알려준다. 리팩토링이 두려울 때 가장 든든한 도구다.

> 📚 **Java/Kotlin 시선 박스 ③ — Kotlin sealed/`when` ↔ discriminated union/`switch`**
>
> 정신은 같지만 도구가 다르다. 한 번 표로 정리해두자.
>
> | 측면 | Kotlin | TypeScript |
> |---|---|---|
> | 대안 집합 정의 | `sealed class` + 서브타입 | `type X = A \| B \| C` (union) |
> | 분별 메커니즘 | 클래스 신원 (`is Circle`) | 공통 리터럴 필드 (`kind: "circle"`) |
> | 분기 문법 | `when` 식 | `switch` 문 (또는 `if`/`else if` 체인) |
> | 자동 캐스팅 | smart cast | flow-based narrowing |
> | exhaustive 보장 | `when`이 식이면 자동 | `assertNever(x: never)` 패턴 |
>
> 결정적 차이는 마지막 줄이다. Kotlin은 `when`이 *식*으로 쓰일 때 컴파일러가 알아서 exhaustive를 검사한다. TS는 `assertNever`라는 *작은 안전망 함수*를 사람이 한 번 만들고, `default` 분기에서 호출한다. 한 번만 만들어 두면 프로젝트 전체에서 재사용 가능하다.
>
> 또 하나, **TS의 분별 유니온은 클래스가 필요 없다.** 그저 객체의 *모양*만 정의하면 된다. JSON으로 직렬화/역직렬화도 자연스럽다. 외부에서 들어오는 메시지(예: WebSocket 이벤트, 큐 메시지)를 모델링할 때 sealed class보다 *훨씬 가볍다*는 점은 분명한 장점이다.

### 한 발 더 — 응답 타입 모델링

분별 유니온이 가장 빛나는 자리는 *상태가 분기되는 응답*이다. 가령 비동기 데이터 로딩 상태를 모델링한다고 해 보자.

```typescript
type LoadState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function render<T>(state: LoadState<T>) {
  switch (state.status) {
    case "idle":
      return "(아직 시작 안 함)";
    case "loading":
      return "로딩 중...";
    case "success":
      return `데이터: ${JSON.stringify(state.data)}`;
    case "error":
      return `에러: ${state.error.message}`;
  }
}
```

여기서 `success`일 때만 `data`가 있고, `error`일 때만 `error`가 있다. 잘못된 조합이 *타입 단에서* 차단된다. *"로딩 중인데 데이터가 있다"*는 비논리적인 상태가 아예 표현 불가능해진다. **표현 불가능한 상태를 표현 불가능하게 만든다** — Yaron Minsky의 그 유명한 격언이 분별 유니온의 정신을 한 줄로 요약한다. Kotlin sealed class도 같은 정신이지만, TS는 그걸 *문법 없이 union 하나로* 표현한다. 가볍고, 충분히 강력하다.

## 유틸리티 타입 — 카탈로그가 아니라 *패턴*으로

분별 유니온까지 익혔으니, 이제 도메인 타입을 *재료*로 새 타입을 *조립하는* 도구를 만나자. TS에는 표준 유틸리티 타입이 30개쯤 들어 있다. 외울 필요는 없다. 자주 쓰는 8개의 *언제 쓰는가*만 손에 익히면, 나머지는 그때그때 검색하면 된다. 표로 던지지 말고 *상황별로* 풀어보자.

### `Partial<T>` — 부분 업데이트의 친구

REST API의 `PATCH` 핸들러를 떠올려 보자. 사용자의 일부 필드만 받아 업데이트한다. *전체 User 모양은 필요 없고, 일부만 들어온다.* 이때 쓰는 게 `Partial<T>`다.

```typescript
interface User {
  id: string;
  email: string;
  name: string;
  age: number;
}

function updateUser(id: string, patch: Partial<User>) {
  // patch는 { email?: string; name?: string; age?: number; ... }
}

updateUser("u-1", { name: "Toby" }); // 통과
```

`Partial<User>`는 모든 필드를 *옵셔널*로 만든다. PATCH·폼 부분 입력·설정 객체의 디폴트 병합 등 *완전하지 않은 모양을 다루는 자리*에 가장 자주 쓴다. 한 가지 주의할 점. `Partial`은 한 단계만 파고든다. 깊이 nested된 객체까지 옵셔널로 만들고 싶다면 `DeepPartial<T>` 같은 재귀 헬퍼를 직접 만들거나 라이브러리(예: `type-fest`)를 가져와야 한다.

### `Required<T>` — 옵셔널을 필수로 되돌리기

반대 방향도 있다. 외부에서 받은 옵셔널 투성이 객체를 *내부에서는 모든 필드가 채워진* 상태로 다루고 싶을 때다.

```typescript
interface Config {
  host?: string;
  port?: number;
  timeout?: number;
}

function applyDefaults(input: Config): Required<Config> {
  return {
    host: input.host ?? "localhost",
    port: input.port ?? 3000,
    timeout: input.timeout ?? 5000,
  };
}
```

함수 *경계*에서는 옵셔널을 받되, 내부에서는 *모든 값이 보장된* 타입으로 좁혀 다루는 패턴이다. Java의 빌더 패턴 끝에서 `build()` 호출 후 모든 필드가 채워진다는 *그 보장*을 타입으로 표현한 셈이다.

### `Readonly<T>` — 변경 금지 표지판

객체를 *읽기 전용*으로 만들고 싶을 때 쓴다.

```typescript
interface Point { x: number; y: number; }

const origin: Readonly<Point> = { x: 0, y: 0 };
origin.x = 10; // 에러
```

주의해두자. `Readonly`는 *컴파일타임* 보장이다. 런타임에는 여전히 변경 가능하다(`Object.freeze`가 필요하면 따로 호출해야 한다). 그럼에도 *의도를 표현*하는 데에는 충분히 가치 있다. 함수의 매개변수에 `Readonly<Config>`를 박아두면, 호출자가 *내가 이 객체를 변경하지 않을 것이다*라는 약속을 받는다. Kotlin의 `val`과 `data class`의 `copy` 패턴이 *문화적으로 강제하는* 그 약속을, TS는 타입 한 글자로 박는다.

### `Pick<T, K>` — 필요한 필드만 떼어내기

`User`에서 `id`와 `email`만 필요한 자리가 있다고 하자.

```typescript
type UserSummary = Pick<User, "id" | "email">;
// { id: string; email: string }
```

리스트 화면에 보여줄 *요약 모양*, 캐시 키로 쓸 *식별자 모양* 같은 자리에서 자주 쓴다. 새 인터페이스를 따로 *복사해 적기*보다 `Pick`으로 *유도*하는 편이 낫다. 원본이 바뀌면 따라서 바뀐다.

### `Omit<T, K>` — 필요 없는 필드만 떼기

`Pick`의 반대. 가장 흔한 자리는 *서버에서 ID를 만들기 전*의 모양을 표현할 때다.

```typescript
type NewUser = Omit<User, "id">;

function createUser(input: NewUser): User {
  return { id: generateId(), ...input };
}
```

*"하나만 빼고 다"*가 직관적으로 떠오를 때 `Omit`이다. Java라면 `UserCreateRequest` DTO를 따로 정의해야 했을 자리에서, TS는 `Omit` 한 줄로 끝낸다. 도메인 모델 한 벌로 *변형들*을 모두 유도해 내는 이 패턴이 익숙해지면, DTO가 폭발하는 Java 백엔드의 그 답답함이 새삼 느껴진다.

### `Record<K, V>` — 키와 값의 모양으로 객체 모델링

키 집합이 정해져 있고, 각 키에 같은 모양의 값이 들어가는 객체.

```typescript
type Role = "admin" | "user" | "guest";
type Permissions = Record<Role, string[]>;

const perms: Permissions = {
  admin: ["read", "write", "delete"],
  user: ["read", "write"],
  guest: ["read"],
};
```

`Record`는 *맵 같은 객체*를 모델링하는 가장 기본적인 도구다. 키가 union 리터럴이면 컴파일러가 *모든 키를 채웠는지* 검사해 준다. `guest`를 빼먹으면 컴파일 에러. exhaustive와 정신이 통하는 자리다.

### `ReturnType<T>` — 함수의 반환 타입 추출

이 도구부터는 *제네릭과 conditional이 짜깁기된* 고급 도구다. 자세한 작동은 5장에서 풀고, 여기서는 *언제 쓰는가*만 보자.

```typescript
function fetchUser(id: string) {
  return { id, email: "x@y.com", roles: ["user"] };
}

type FetchUserResult = ReturnType<typeof fetchUser>;
// { id: string; email: string; roles: string[] }
```

함수의 반환 타입을 *별도로 명시하지 않고도* 그 모양을 타입으로 끌어낸다. *함수가 곧 모양의 정의*가 되는 셈이다. 작은 함수에서는 별 가치가 없지만, 라이브러리가 *복잡한 모양을 반환하는* 함수를 노출할 때(예: 빌더의 결과, ORM 쿼리의 결과) 매우 유용하다. 5장에서 zod의 `z.infer`와 함께 다시 만나게 된다.

### `Awaited<T>` — Promise를 풀기

`Promise<User>`에서 `User`를 꺼내고 싶을 때.

```typescript
async function fetchUser(id: string): Promise<User> { /* ... */ return null as any; }

type User = Awaited<ReturnType<typeof fetchUser>>;
// User
```

`ReturnType`으로 함수의 반환 타입을 꺼내면 `Promise<User>`이다. 거기서 한 겹 더 벗기는 게 `Awaited`. 비동기 함수의 *결과 모양*을 타입으로 다룰 때 거의 자동으로 손이 간다. 7장의 비동기 절에서 다시 만난다.

> 💡 **유틸리티 타입을 바라보는 작은 팁**
>
> 8개를 한꺼번에 외우려 들지 말자. *상황을 맞닥뜨릴 때마다* "이런 모양이 필요한데 이미 있는 도구가 없을까?" 하고 손이 가게 만드는 편이 낫다. 처음 한두 달은 `Pick`/`Omit`/`Partial`만 써도 충분하다. `ReturnType`/`Awaited`는 *라이브러리가 복잡한 타입을 반환할 때* 자연스럽게 손이 간다. 한 번 손이 가면 그 다음부터는 고민할 필요가 없다.

## 함수 타입과 bivariance — Java로는 이해 안 되는 자리

마지막으로, 함수 타입의 *변성(variance)*을 짚자. 이 자리는 Java/Kotlin 개발자가 *처음에는 도무지 이해가 안 가는* 곳 중 하나다. 천천히 풀어보자.

먼저 변성이 뭔지 짧게 복습하자. 어떤 타입 `T`가 다른 타입 `U`의 서브타입이라고 하자(예: `Dog`은 `Animal`의 서브타입). 이때 `Container<T>`와 `Container<U>` 사이의 관계가 어떻게 되는가? *공변(covariant)*이라면 `Container<Dog>`이 `Container<Animal>`의 서브타입. *반공변(contravariant)*이라면 그 반대. *불변(invariant)*이라면 둘은 무관.

함수 매개변수의 변성은 *반공변*이 안전하다. 왜? 함수 `(d: Dog) => void`에 `(a: Animal) => void`를 *대입할 수 있는가*를 따져보자. 답은 *그렇다*. `Animal`을 받는 함수는 *모든 Animal*에 대해 동작하므로, *Dog*가 들어와도 당연히 동작한다. 반대는 안 된다. `Dog`만 받는 함수에 `Animal`을 던지면, `Dog`이 아닌 다른 `Animal`이 들어왔을 때 깨진다.

이게 *반공변*이다. Java의 wildcard `? super T`가 같은 정신이다.

그런데 TS는 기본적으로 *bivariant*로 동작한다. 즉 `(d: Dog) => void`에 `(a: Animal) => void`도, `(c: Corgi) => void`도 *둘 다 대입 가능*하다. 후자는 *안전하지 않다*. `Corgi`만 받는 함수에 `Dog`을 일반적으로 던지면 `Corgi`가 아닌 다른 `Dog`이 들어왔을 때 깨진다.

*"왜 이렇게 만들었나?"* 하고 묻고 싶어진다. 답은 *실용성* 때문이다. 자바스크립트 라이브러리들이 이 안전하지 않은 패턴을 워낙 많이 써 왔고, TS가 strict 반공변을 강제하면 *기존 JS 라이브러리의 타입 정의*가 죄다 깨진다. 그래서 의도된 unsoundness 중 하나로 두었다.

다행히 도구는 있다. tsconfig의 `strictFunctionTypes: true`(또는 `strict: true`로 자동 켜짐)를 켜면, 함수 타입에 한해 *반공변*으로 검사한다. 단, *메서드 표기법*(`m(x: T): void`)은 여전히 bivariant로 남고, *함수 표기법*(`m: (x: T) => void`)에서만 strict 반공변이 적용된다. 이 비대칭 또한 *기존 코드를 깨지 않으려는* 타협이다.

```typescript
interface Listener<T> {
  // 메서드 표기 — 여전히 bivariant
  handle(event: T): void;
}

interface Listener2<T> {
  // 함수 표기 — strictFunctionTypes 하에서 반공변
  handle: (event: T) => void;
}
```

실무 결론은 단순하다. 첫째, **`strictFunctionTypes`는 켜라**. 둘째, *함수의 변성에 민감한 자리(콜백, 이벤트 핸들러)*에서는 함수 표기법으로 적자. 이 정도만 지키면, TS의 함수 변성이 우리를 *덜 자주* 배신한다. 깊이 이해하고 싶다면 5장의 제네릭 절에서 variance를 한 번 더 다룬다 — 거기서 Java wildcard와의 매핑을 더 자세히 풀자.

> 💡 **작가의 한 마디 — bivariance에 너무 시달리지 말자**
>
> 솔직히 고백하자면, 함수 변성은 일상 코드에서 발등을 찍는 일이 그렇게 많지 않다. 대부분의 자리는 `strictFunctionTypes`가 알아서 잡아주고, 알아서 못 잡는 자리는 *애초에 우리가 그런 코드를 잘 쓰지 않는* 자리다. 처음에는 *"아, 이런 자리가 있구나"* 정도로 알아두고, 실제로 발등이 찍히면 그때 다시 펼쳐 보자. *언어를 외우려 들기보다, 도구로 두드려 보는 편이 낫다.*

## 마무리 — 처음 두드려본 도구의 손맛

여기까지 두드려본 도구를 정리하자. 추론은 *적극적*이지만 *전능하지 않다*. 좁히기는 `typeof`/`instanceof`/`in`/`===`/type predicate라는 *다섯 도구*를 모두 동원한다. 분별 유니온과 `assertNever`는 Kotlin sealed class와 *같은 정신*을 *다른 도구*로 구현한다. 유틸리티 타입은 *카탈로그가 아니라 패턴*이다 — 상황을 만나면 손이 가게 두자. `satisfies`는 *검증과 좁힘을 동시에* 갖고 싶을 때의 신선한 도구다. 함수 변성은 `strictFunctionTypes`로 막을 수 있는 만큼만 막고, 나머지는 알아두는 정도로 충분하다.

이 챕터를 마치고 났을 때 우리가 손에 든 것은 *문법의 카탈로그*가 아니다. *도메인의 결을 타입으로 표현하는 작은 감각*이다. 새 모양을 추가하면 컴파일러가 *고쳐야 할 모든 자리를 알려주고*, 잘못된 상태 조합은 *애초에 표현이 안 되며*, 외부에서 들어온 `unknown`은 *type predicate를 거쳐야 안으로 들어온다*. 이 감각이 한 번 손에 잡히면, *그다음 코드가 다른 모양으로 흐르기 시작한다.* 그게 4장이 의도한 첫 *쾌감*이다.

다만 이 도구들의 *심층*은 아직 다 펼치지 않았다. 분별 유니온의 멤버 자체를 *다른 타입에서 유도*하고 싶다면? 함수의 매개변수 모양을 *추출*해 새 함수를 합성하고 싶다면? `Partial<T>`처럼 *타입에서 타입을 만드는* 도구를 직접 만들고 싶다면? 이 모든 질문이 5장의 *제네릭과 매핑·조건부 타입* 절로 이어진다. zod의 `z.infer`, Hono의 자동 추론, Prisma의 생성 타입 같은 *마법 같은 부품들*이 그 자리에서 *부품 단위로* 보이기 시작한다.

> 📖 **더 깊이 가려면**
>
> - **타입 단위 테스트가 궁금하다면** → 14장. 타입이 *런타임에 사라지므로* 단위 테스트도 다른 도구가 필요하다. `expect-type`/`tsd`로 *타입 자체*를 단정문으로 검증하는 패턴을 자세히 다룬다. 본 장에서 만든 분별 유니온이 *의도대로 좁혀지는지*를 자동화 테스트로 못 박는 자리.
> - **strict 모드의 모든 옵션을 일별하고 싶다면** → 부록 B. tsconfig 옵션 사전. `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes` 같은 *strict 가족 너머의 한 단계*를 정리해 두었다. Matt Pocock의 cheat sheet도 함께 참조하면 좋다.
> - **type predicate vs zod 같은 런타임 검증의 *경계 정책*이 궁금하다면** → 15장의 함정 절. 한국 팀의 *경계 검증(boundary validation)* 패턴이 어떻게 정착되었는지 사례와 함께.
> - **함수 변성을 *진지하게* 파고 싶다면** → 5장의 제네릭 variance 절. `extends`/`infer`와 함께 wildcard 타입의 TS식 표현을 본격적으로 다룬다.

타입을 *문법으로 외우는* 단계는 여기서 졸업이다. 다음 장에서는 *타입을 만드는 타입*의 자리로 넘어가자. 부품이 더 작아지고, 조립의 자유가 더 커진다. 5장에서 만나자.
