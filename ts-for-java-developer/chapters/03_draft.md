# 3장. TypeScript는 무엇이며, 무엇이 아닌가 — 컴파일타임의 환상

Spring으로 10년을 짜온 개발자가 TS 프로젝트에 처음 합류한 첫째 주를 상상해보자. 동료가 보내준 PR을 열어보니, 요청 본문 타입이 `interface CreateUserRequest`로 깔끔하게 정의되어 있다. 익숙한 풍경이다. 그런데 그 아래 컨트롤러 코드가 이상하다. `req.body`를 그대로 받아 그 인터페이스 타입에 *맞다고 가정하고* 내부 함수에 넘긴다. `@Valid`도 없고, 어떤 검증 호출도 없다.

*"이거… 그냥 통과돼?"* 동료에게 묻는다. *"네, 컴파일 잘 되고 테스트도 통과해요."*

분명 IDE는 빨간 줄 하나 없다. 빌드도 깔끔하다. 그런데 어딘가 찜찜하다. 익숙한 정적 타입의 안전망이 발 밑에 깔려 있다고 믿었는데, 한 발자국 떼어 보니 그 안전망이 *컴파일이 끝나는 순간 사라진다*는 사실이 어렴풋이 손에 잡힌다. *"그럼 이 타입은 도대체 뭐였지? 런타임에는 어디 있는 거지?"*

질문을 정직하게 받아들여야 한다. 이 챕터는 그 질문 두 개에 답한다. 첫째, **TS의 타입 정보는 런타임에 어디로 가는가?** 둘째, ***"Java처럼 안전하다"*는 직관은 어디서 깨지는가?** 이 두 질문에 손에 잡히는 답을 갖고 나면, TS라는 도구가 *어떤 약속을 하고 어떤 약속은 하지 않는지*가 보인다. 그제야 4장 이후의 모든 도구—추론·좁히기·discriminated union·매핑 타입·branded type—를 *왜 그렇게 생겼는지* 이해하면서 손에 익힐 수 있다.

먼저 1장에서 이름만 호명했던 다섯 핵심 모델을 정면으로 풀어보자. 이 다섯이 책의 *언어 철학적 골격*이다. 여기서부터다.

## 다섯 핵심 모델 — TS의 정체를 한 자리에 모으면

TS를 *언어*로 이해한다는 건 결국 다섯 가지 결정의 묶음을 이해한다는 뜻이다. 점진적 타입(gradual), 구조적 타입(structural), 의도된 unsoundness, type erasure, 그리고 ECMAScript 정렬(TC39 alignment). 이 다섯은 따로 있는 게 아니라, *서로가 서로의 이유*다. 하나가 없으면 다른 넷이 성립하지 않는다.

먼저 다섯을 짧게 펼쳐놓고, 그 다음에 하나씩 깊이 들어가보자.

**(1) 점진적 타입 (gradual typing).** 한 프로그램 안에 *타입이 붙은 코드*와 *타입이 붙지 않은 코드*가 공존할 수 있다. `any`라는 탈출구가 그 다리 역할을 한다. `any`는 어떤 타입과도 양방향으로 호환되며, 그 결과 *기존 JS 코드를 깨지 않고 한 파일씩 점진적으로 TS로 옮겨갈 수 있다*. 이 결정이 없었다면 오늘날의 TS는 없다.

**(2) 구조적 타입 (structural typing).** 두 타입이 호환되는지는 *모양*으로 결정된다. `class Dog implements Animal`이라고 적을 필요가 없다. 멤버가 같으면 같은 타입이다. Java/Kotlin의 명목 타입(nominal)에서 온 사람에게 가장 처음 충격을 주는 자리.

**(3) 의도된 unsoundness.** TS는 *완벽한 타입 안전성을 일부러 포기*했다. 함수 매개변수의 bivariance, `any`의 흡수성, 인덱스 시그니처의 허용 범위, 배열의 공변성 등 학자들이 지목한 6+ 개의 자리에서 *틈*을 의도적으로 남겼다. 이유는 *개발자 생산성과 JS 호환성*. 정합성과 생산성 사이의 균형을 *생산성 쪽으로 기울인* 결정이다.

**(4) 타입 소거 (type erasure).** `tsc`가 끝나면 모든 타입이 사라진다. `interface User`도, `type UserId`도, 제네릭 매개변수도, 전부 다. 결과물은 평범한 JS다. Java erasure가 *제네릭 매개변수만* 지운다면, TS erasure는 *모든 타입을* 지운다.

**(5) ECMAScript 정렬 (TC39 alignment).** TS는 자기만의 길을 가지 않는다. 새 문법은 가능한 한 TC39 표준 진행 단계와 정렬한다. `class`, `async/await`, `decorator`, top-level await — 모두 ECMAScript 표준을 따라간다. *"우리는 JS를 대체하는 언어가 아니라, JS가 잘되도록 돕는 도구다"*가 TS의 자기규정이다.

이 다섯이 한 줄로 합쳐지면 이렇게 된다.

> TypeScript는 JavaScript 위에 *타입 주석과 컴파일러*를 얹은 도구다. 타입은 *컴파일 단계에서만 의미가 있고*, 컴파일이 끝나면 *지워진다*. *모양*으로 호환을 판단하며, *의도적으로 안전성의 일부 틈을 허용*해 *기존 JS 코드와 점진적으로 함께 살 수 있게* 한다. 그리고 자기 마음대로 문법을 만들지 않고 *JS 표준을 따라간다*.

이 한 단락이 이 챕터 전체의 요약이다. 하지만 *요약을 외우는 것*과 *그 요약이 코드에서 어떻게 드러나는지를 손으로 만지는 것*은 다르다. 이제부터 다섯을 하나씩, 코드와 함께, *왜 그래야 했는지의 사연*과 함께 풀어보자. 결이 잡히지 않으면 4장부터의 모든 도구가 *추상적 카탈로그*로만 보이게 된다.

## 컴파일과 런타임 — `tsc`가 끝나면 타입은 어디로 가는가

가장 먼저 손에 잡혀야 하는 건 *컴파일과 런타임의 분리*다. 이게 손에 잡히지 않으면 뒤의 어떤 설명도 공중에 뜬다.

다음 TS 코드를 살펴보자.

```ts
interface User {
  id: number;
  name: string;
  isAdmin: boolean;
}

function greet(user: User): string {
  return `Hello, ${user.name}`;
}

const me: User = { id: 1, name: "Toby", isAdmin: false };
console.log(greet(me));
```

한 눈에 봐도 Java/Kotlin 개발자에게 익숙한 모양이다. `interface`로 데이터 형태를 정의하고, 함수 매개변수에 타입을 주고, 변수 선언에서도 타입을 명시했다.

이걸 `tsc`로 컴파일하면 어떻게 될까? 결과 JS 파일을 보면 이렇다.

```js
function greet(user) {
  return `Hello, ${user.name}`;
}

const me = { id: 1, name: "Toby", isAdmin: false };
console.log(greet(me));
```

깜짝 놀랄 일이 없는, *그냥 JS다*. `interface User`는 어디로 갔을까? 사라졌다. `: User`라는 매개변수 주석도 사라졌다. `: string` 반환 타입도 사라졌다. *모든 타입이 지워진* 평범한 JavaScript만 남았다.

여기서 잠깐 멈추자. Java 개발자에게 이건 충격이다. Java에서 `class User { int id; String name; boolean isAdmin; }`을 컴파일하면 *런타임까지 살아남는* `User.class` 파일이 만들어진다. `instanceof User`로 검사할 수 있고, `getClass().getName()`으로 이름을 꺼낼 수 있고, 리플렉션으로 필드를 순회할 수 있다. 타입은 *런타임의 시민*이다.

TS는 다르다. *런타임에는 타입이 없다*. `instanceof User`도 쓸 수 없다 — 왜냐면 `User`는 컴파일이 끝나는 순간 *존재 자체가 지워졌기* 때문이다. 다음 코드는 컴파일 자체가 안 된다.

```ts
function isUser(value: unknown): value is User {
  return value instanceof User; // ❌ 'User'는 타입이지 값이 아닙니다
}
```

타입이 *값이 아니다*. 이 한 문장이 TS를 다루는 모든 코드에서 매일 마주치는 제약이다. 처음에는 난감하다. 익숙해지기까지 한참 걸린다.

### "JS 위에 얹힌 타입 레이어"의 실제 모양

그래서 TS의 핵심 한 줄은 이렇게 다시 풀린다.

> TS = JS 코드 + *컴파일 시점에만 존재하는* 타입 주석 + 그것을 검사하는 컴파일러 `tsc` + 에디터에 붙어 자동완성·리팩토링·진단을 제공하는 *언어 서비스*.

핵심 단어는 *컴파일 시점에만 존재하는*이다. 영어 약어로는 *erased at compile time*이라 부른다. TS의 타입은 *유령*이다. 개발 중에는 든든히 옆에 있는 듯하지만, 빌드 버튼을 누르고 결과물을 열어보면 거기 없다.

이 모델을 한 번 손에 잡으면, 이후 챕터의 많은 결정이 *왜 그래야 했는지* 자연스럽게 풀린다. 예를 들어:

- *왜 외부 API 응답을 zod 같은 라이브러리로 검증해야 하는가?* — 응답 객체의 *모양*은 컴파일러가 검사할 길이 없기 때문이다. 컴파일이 끝난 런타임에 도착한 JSON은 그냥 객체다. TS의 `interface ApiResponse`는 코드의 *주석*에 불과하지, 런타임에서 *강제하는 누군가*가 아니다.
- *왜 NestJS·TypeORM 같은 프레임워크가 `experimentalDecorators` + `emitDecoratorMetadata`를 켜야 하는가?* — DI를 작동시키려면 *런타임에 타입 정보가 살아남아야* 하기 때문이다. 이 두 옵션을 켜면 컴파일러가 일부 타입 메타데이터를 `reflect-metadata` 라이브러리에 *기록*해 살려두지만, 이는 TS의 *기본 동작이 아닌* 특수 모드다. 기본 모드에서는 모든 타입이 지워진다.
- *왜 Java 개발자가 가장 즐겨 쓰는 `instanceof` 패턴이 TS에서는 절반만 작동하는가?* — `instanceof`는 *클래스*에는 쓸 수 있지만 *인터페이스나 타입 별칭*에는 쓸 수 없기 때문이다. TS에서 `class`로 정의한 것만 런타임 시민으로 남는다. `interface`와 `type`은 안 남는다.

### Java erasure와는 차원이 다른 이유 — *제네릭만 vs 모든 타입*

여기서 똑똑한 Java 개발자라면 즉시 반문한다. *"잠깐. Java에도 type erasure 있잖아? `List<String>`이 런타임에는 그냥 `List`잖아?"*

맞다. Java에도 erasure가 있다. 그런데 *지워지는 범위가 완전히 다르다*. 이 차이를 정확히 짚어두지 않으면, 두 언어를 같은 풍경으로 착각하게 된다.

다음 Java 코드를 살펴보자.

```java
class Box<T> {
    private T value;
    public T get() { return value; }
    public void set(T v) { this.value = v; }
}

Box<String> b = new Box<>();
b.set("hello");
String s = b.get();
```

이걸 컴파일해 `javap -c -p Box.class`로 들여다보면 흥미로운 풍경을 본다.

```
class Box {
  private java.lang.Object value;        // ← T가 Object로 erasure
  public java.lang.Object get();         // ← 반환 타입도 Object
  public void set(java.lang.Object);     // ← 매개변수도 Object
}
```

`T`는 사라지고 `Object`로 환원되었다. 이게 Java erasure다. *제네릭 매개변수만* 지워지고, *나머지 타입은 살아남는다*. 클래스 이름 `Box`도 살아남고, 메서드 이름과 시그니처도 살아남고, `String`이라는 클래스도 살아남는다. 그래서 `b instanceof Box`는 작동한다 (*다만* `b instanceof Box<String>`은 안 된다 — 그게 erasure가 지운 부분이다).

이제 TS의 같은 코드를 보자.

```ts
class Box<T> {
  private value: T | undefined;
  get(): T | undefined { return this.value; }
  set(v: T): void { this.value = v; }
}

const b = new Box<string>();
b.set("hello");
const s = b.get();
```

`tsc`로 컴파일한 결과는 이렇다.

```js
class Box {
  value;
  get() { return this.value; }
  set(v) { this.value = v; }
}

const b = new Box();
b.set("hello");
const s = b.get();
```

여기서 *모든 타입이 지워졌다*. 매개변수의 `: T`도, 반환 타입의 `: T | undefined`도, 변수 선언의 `<string>`도, *전부*. 클래스 본체와 메서드 시그니처는 살아남았지만, 그건 *클래스가 JS의 일급 시민이기 때문*이지 *타입이라서가 아니다*. 만약 같은 코드를 `interface Box<T>`로 정의했다면, 컴파일된 JS에는 *Box라는 단어가 한 글자도 남지 않는다*.

차이를 한 줄로 정리하자.

> Java erasure는 *제네릭 매개변수만* 지운다. 클래스·메서드·타입은 런타임에 살아 있다.
> TS erasure는 *모든 타입을* 지운다. 살아남는 건 JS의 *값*과 *클래스*뿐이다.

이 차이는 단순한 구현 디테일이 아니다. *프로그래밍 모델 전체의 결정*이다. Java의 reflection·dynamic proxy·annotation processor 같은 도구는 *런타임에 타입이 살아있기 때문에* 가능했다. TS에서 같은 일을 하려면 *별도의 부속물*(reflect-metadata, decorator metadata, schema 라이브러리)을 끌어와야 한다. 그 부속물이 없으면 TS의 타입은 *코드 리뷰에서만 사는 유령*이다.

기억해두자. **TS의 타입은 컴파일러와 IDE에서만 일한다. 런타임에는 출근하지 않는다.** 이 한 문장을 머리에 박아두면 4장 이후의 모든 도구가 *왜 그렇게 설계되었는지* 자연스럽게 보이기 시작한다.

> **📚 Java/Kotlin 시선 — `instanceof`의 의미가 다르다**
>
> Java/Kotlin에서 `instanceof`(또는 `is`)는 *모든 명목 타입*에 대해 작동한다. `obj instanceof Animal`이면 `Animal` 인터페이스든 클래스든 상관없이 런타임 검사가 가능하다.
>
> ```java
> // Java
> interface Animal { String name(); }
> class Dog implements Animal { ... }
>
> Object x = new Dog();
> if (x instanceof Animal a) {  // ✅ 인터페이스에도 작동
>     System.out.println(a.name());
> }
> ```
>
> TS에서는 다르다. `instanceof`는 *런타임에 살아남은 클래스*에만 작동한다. `interface`나 `type`에는 못 쓴다.
>
> ```ts
> // TypeScript
> interface Animal { name(): string; }
> class Dog implements Animal {
>   name() { return "Rex"; }
> }
>
> const x: unknown = new Dog();
> if (x instanceof Animal) { /* ❌ 'Animal'은 타입이지 값이 아닙니다 */ }
> if (x instanceof Dog)    { /* ✅ Dog는 클래스라 값으로 살아남음 */ }
> ```
>
> 그래서 TS에서 *interface 모양인지*를 런타임에 검사하려면, 직접 *type predicate* 함수를 쓰거나(`function isAnimal(x): x is Animal`), zod 같은 *런타임 스키마*를 거치거나, *공통 리터럴 필드*로 *discriminated union*을 만들어 `switch`로 갈라야 한다. Java/Kotlin에서 무심코 쓰던 `instanceof`의 자리가 TS에서는 *세 갈래로 흩어진다*. 이 갈래를 손에 익히는 게 4장의 절반이다.

## TS Design Goals — 공식 문서가 직접 말하는 *우리는 무엇을 하지 않는다*

TS가 어떤 도구인지를 알고 싶다면, 가장 좋은 방법은 *TS Design Goals* 원문을 한 번 읽어보는 것이다. Microsoft TS 위키에 공개된 이 문서는 짧지만 결정적이다. 핵심을 옮겨보자.

> **Goals (목표):**
> 1. Statically identify constructs that are likely to be errors. *(에러일 가능성이 높은 구성을 정적으로 식별한다.)*
> 2. Provide a structuring mechanism for larger pieces of code. *(큰 코드 조각을 구조화할 수단을 제공한다.)*
> 3. Impose no runtime overhead on emitted programs. *(컴파일된 프로그램에 런타임 오버헤드를 부과하지 않는다.)*
> 4. Align with current and future ECMAScript proposals. *(현재와 미래의 ECMAScript 제안과 정렬한다.)*
>
> **Non-goals (목표가 아닌 것):**
> - Add or rely on run-time type information. *(런타임 타입 정보를 추가하거나 거기 의존하지 않는다.)*
> - Apply a sound or "provably correct" type system. *(완전무결하거나 "증명 가능하게 옳은" 타입 시스템을 적용하지 않는다.)*

이 문서는 *짧은데 무겁다*. 한 줄 한 줄이 책 한 권의 결정을 압축하고 있다. 함께 읽어보자.

먼저 *목표 3*: *컴파일된 프로그램에 런타임 오버헤드를 부과하지 않는다*. 이게 바로 앞 절에서 우리가 본 *모든 타입이 지워진다*의 공식 근거다. TS는 자기 타입 시스템을 위해 *JS 런타임을 한 줄도 더 무겁게 만들지 않겠다*고 약속했다. 그래서 컴파일된 결과물은 항상 *원본 JS와 거의 같은 크기*다.

다음 *목표 4*: *ECMAScript 제안과 정렬한다*. TS는 자기만의 신박한 문법을 만들 수 있는 권한이 충분히 있는데도, 일부러 *TC39 위원회의 결정에 자기 진화를 묶었다*. `async/await`, optional chaining(`?.`), nullish coalescing(`??`), top-level await, 새 데코레이터 — 전부 *ECMAScript 표준이 먼저, TS가 다음*이다. 자기 야망보다 *생태계의 미래*를 우선한 결정이다. 이게 없었다면 TS는 *JS와 갈라선 별종 언어*가 되었을 것이고, 오늘의 채택률은 절반도 안 됐을 것이다.

그리고 결정적으로, *Non-goal 두 줄*이 이 책의 3장 전체를 정당화한다.

*"런타임 타입 정보를 추가하거나 거기 의존하지 않는다."* — 이건 *type erasure*의 공식 선언이다. *우리는 일부러 타입을 런타임에 안 남긴다*. Java처럼 reflection을 위한 메타데이터를 자동으로 심지 않는다. NestJS·TypeORM이 그걸 끌어 쓰려면 *별도의 옵션과 라이브러리*를 명시적으로 가져와야 한다.

*"완전무결하거나 '증명 가능하게 옳은' 타입 시스템을 적용하지 않는다."* — 이게 바로 *의도된 unsoundness*다. TS는 학자들이 *sound*하다고 부를 수 있는 타입 시스템을 *목표로 삼지 않았다*. 왜? 그게 *생산성과 충돌*하기 때문이다.

이 두 줄을 마음에 새겨두자. TS를 비판하는 글의 90%는 *TS가 약속하지 않은 것을 약속했다고 오해한 데서* 나온다. *"왜 TS는 런타임 안전을 보장 안 해주냐"*는 질문은, 마치 *"왜 망치는 못을 안 빼주냐"*는 질문과 같다. 도구는 *자기가 하기로 한 것*만 한다.

> **💡 작가의 한 마디 — 학계가 부러워한 트레이드오프**
>
> 잠깐 멈춰서 생각해보자. TS의 *Non-goals* 두 줄을, 만약 TS 팀이 거꾸로 적었다면 어떻게 됐을까? *"Add and rely on run-time type information. Apply a sound type system."*
>
> 결과는 끔찍하다. TS는 *기존 JS 코드와 호환되지 않는 별종 언어*가 되었을 것이다. *"우리 회사 JS 코드 5만 줄 중 일부만 TS로 옮기고 싶다"*는 시나리오는 불가능했을 것이다. 모든 타입을 *증명 가능하게* 검사하려면 `any` 같은 탈출구는 못 둔다. `any`가 없으면 점진적 도입은 못 한다. 점진적 도입이 없으면 *시장에 도달*하지 못한다. 시장에 도달 못 하면, 학계가 칭찬해주는 *예쁜 타입 시스템*으로 끝난 채 사장된다. Flow가 그랬고, 그 이전 수많은 타입 첨부 시도들이 그랬다.
>
> 학계의 후속 연구 *Sound Gradual Typing Is Dead?*(Takikawa et al. 2016, POPL)는 이 결정이 *왜 옳았는지*를 정량적으로 보여준다. *sound*와 *gradual*을 동시에 요구하면 *평균 7배, 최악 100배*의 런타임 슬로다운이 발생한다. 즉 *완벽하게 안전한 점진적 타입*은 *현실 성능에서 성립 불가능*하다. TS는 이 사실을 학계가 정량화하기 *2년 먼저*, 직관적으로 알아채고 *실용적 길*을 골랐다.
>
> 그래서 TS의 unsoundness를 *허술함*이 아니라 *겸손함*으로 읽어보자. *"우리는 모든 걸 잡진 못한다. 잡을 수 있는 것을 잡고, 못 잡는 건 솔직히 말하겠다."* 이 자세가 학계와 산업 사이의 다리를 놓았다. TS가 *sound를 포기하지 않았다면*, 우리는 지금 이 책을 쓰지도, 읽지도 않고 있을 것이다. 약속하지 않은 것에 실망하는 대신, *약속한 것을 정확히 받아드는* 자세를 챙겨보자. 그게 도구를 *자기 것으로 만드는* 첫 단계다.

## 점진적 타입 — `any`라는 탈출구가 왜 필요했는가

이제 첫 번째 핵심 모델, *점진적 타입(gradual typing)*을 본격적으로 풀어보자.

상황을 가정해보자. 회사에 5년 묵은 JS 코드 30만 줄이 있다. 매일 사용자 트래픽이 흐르고 있다. 어느 날 결정한다. *"이걸 TS로 옮기자."* Java로 치면 *Groovy 30만 줄을 Kotlin으로 옮기는 일*에 가깝다. 한 번에 다 옮긴다? 그건 *프로덕션을 멈추고 6개월 동안 리팩토링만 하겠다*는 선언이다. 끔찍한 일이다. 어떤 회사도 못 한다.

그래서 *점진적 마이그레이션*이 필요하다. *오늘은 1번 파일만, 내일은 2번 파일도, 한 달 뒤에는 30번 파일까지*. 이게 가능하려면 한 가지 조건이 절대적이다. *타입이 붙은 코드와 붙지 않은 코드가 한 프로그램 안에서 섞여 살 수 있어야 한다*. 이걸 학계 용어로 *gradual typing*이라 부르고, Siek과 Taha가 2006년에 그 이론적 토대를 닦았다.

TS의 답은 한 단어다. **`any`**. `any`는 *어떤 타입과도 양방향으로 호환되는* 특수 타입이다. *타입을 모르겠다, 일단 통과시켜라*라는 명시적 신호다.

```ts
// 타입이 붙은 코드
function double(n: number): number {
  return n * 2;
}

// 타입이 없는(any) 함수 호출 — JS에서 옮겨오는 중인 코드라고 가정
function legacyCompute(): any {
  return JSON.parse('{"value": 42}').value;
}

// 양방향 호환
const x: number = legacyCompute();   // ✅ any → number 통과
const y: any = double(10);           // ✅ number → any 통과
const z: string = legacyCompute();   // ✅ any → string도 통과 (!!)
```

마지막 줄을 보자. `legacyCompute()`는 사실 *number*를 반환하는데, `string` 변수에 담아도 컴파일러가 통과시킨다. *왜?* `legacyCompute`의 반환 타입이 `any`라서, 컴파일러는 *모른다고 인정하고 모든 검사를 면제*한다. 이게 `any`의 *흡수성(absorption)*이다. `any`는 *타입 검사 안에 뚫린 구멍*이다. 일단 들어가면 검사 없이 어디로든 흘러간다.

처음 보면 *왜 이런 위험한 걸 두냐* 싶다. 답은 단순하다. *그게 없으면 TS 도입이 불가능하다*. 5년 묵은 JS 30만 줄에 *모든 함수에 타입을 다 붙이고 시작하라*고 요구하면, *아무도 시작하지 않는다*.

### Bierman et al. (2014)이 정리한 *6+ 지점의 의도된 unsoundness*

`any`는 가장 잘 알려진 *틈*이지만, TS에는 그 외에도 의도적으로 남겨둔 *틈*이 여러 개 있다. Bierman, Abadi, Torgersen 세 사람이 2014년 ECOOP에서 발표한 *Understanding TypeScript* 논문이 이를 *6+ 지점*으로 정리해두었다. 한국 개발자가 이 논문을 직접 읽기는 부담스럽지만, 결론은 손에 잡혀야 한다. 가장 중요한 다섯 가지를 풀어보자.

**(1) `any`의 양방향 호환.** 위에서 본 그대로다. `any`는 모든 타입과 호환되며, 검사를 통과시킨다.

**(2) 함수 매개변수의 bivariance(쌍변성).** 보통 OOP 언어에서 함수 매개변수는 *반공변(contravariant)*이어야 안전하다. 즉 *부모 타입을 받는 함수*는 *자식 타입을 받는 함수의 자리*에 들어갈 수 있어야 한다 (그 반대는 안 된다). TS는 기본 모드에서 *양쪽 다 허용*한다. 즉, *자식 타입을 받는 함수*도 *부모 타입을 받는 함수의 자리*에 들어갈 수 있다. 결과적으로 다음 같은 코드가 통과한다.

```ts
class Animal { name: string = ""; }
class Dog extends Animal { bark(): void { console.log("woof"); } }

type AnimalHandler = (a: Animal) => void;

const dogHandler: (d: Dog) => void = (d) => d.bark();

const handler: AnimalHandler = dogHandler;  // ✅ 통과 (bivariance)
handler(new Animal());  // ❌ 런타임에서 d.bark() 호출 → undefined.bark() 폭발
```

`strictFunctionTypes` 옵션을 켜면 이 동작이 *반공변으로 엄격해진다*. 하지만 *기본 모드에서는 통과한다*. 왜? *DOM API를 비롯한 수많은 기존 JS 라이브러리가 이 패턴에 의존*하기 때문이다. 만약 TS가 처음부터 엄격했다면 *jQuery 코드 한 줄도 통과 못 했을 것이다*.

**(3) 인덱스 시그니처의 허용 범위.** 객체에 동적 키로 접근할 때 TS는 비교적 관대하다. `obj[key]`가 *진짜 존재하는지* 검사하지 않는다. `noUncheckedIndexedAccess` 옵션을 켜기 전까지는 *없는 키도 그냥 접근 통과*시킨다.

**(4) 객체 리터럴의 *excess property check*가 변수에 담기면 사라진다.** 직접 객체 리터럴로 함수에 넘기면 *추가 속성을 잡아주지만*, 변수에 한 번 담아 넘기면 *통과한다*. 구조적 타입의 호환 규칙과 일관성을 유지하기 위한 트레이드오프다.

```ts
type Point = { x: number; y: number };

function plot(p: Point) { /* ... */ }

plot({ x: 1, y: 2, z: 3 });  // ❌ 'z'는 알 수 없는 속성

const p = { x: 1, y: 2, z: 3 };
plot(p);  // ✅ 통과 — 변수에 담기면 z는 무시
```

**(5) 배열의 공변성.** 배열은 *공변(covariant)*으로 설계되었다. 즉 `Dog[]`는 `Animal[]`의 자리에 들어갈 수 있다. 이게 안전한가? *읽기만 하면* 안전하다. *쓰기까지 하면* 깨진다. Java도 같은 자리에서 `ArrayStoreException`을 런타임에 던지는데, TS는 *컴파일러가 잡지 않고 통과시키고 런타임에서도 던지지 않는다* — 그냥 *조용히 잘못된 데이터가 흘러간다*.

이런 자리들을 본 학자들은 처음에는 *"TS는 unsound하다"*라고 비판했다. 그런데 시간이 지나면서 *"unsound하지만 합리적이다"*로 평가가 바뀌었다. 그 전환점이 다음에 다룰 *Sound Gradual Typing Is Dead?* 논문이다.

> **🚧 함정 박스 — 묵시적 any와 strict 모드**
>
> **증상:** 함수를 정의했는데, 타입 주석을 빼먹으면 매개변수가 *조용히 `any`로 추론된다*. IDE에서는 빨간 줄이 없다. 빌드도 통과한다. 그런데 그 함수 안에서 *어떤 메서드든 호출이 다 통과해버린다*. 결국 *런타임에 `undefined.foo() is not a function`이라는 폭발이 난다*.
>
> ```ts
> // 묵시적 any가 일어나는 자리
> function process(user) {            // ← user의 타입이 any로 묵시 추론
>   return user.profile.toUpperCase(); // ← 컴파일러는 통과시킴
> }
>
> process({ name: "toby" });   // 런타임 폭발: profile is undefined
> ```
>
> **원인:** TS는 점진적 타입의 정신을 따라 *기본 모드에서는 묵시적 any를 허용*한다. 옛날 JS 파일을 그대로 떠서 TS로 옮기는 시나리오를 위해서다. 그런데 *처음부터 TS로 짜는 신규 코드*에는 이 관대함이 *함정*이 된다. 타입을 적지 않으면 *검사가 사실상 꺼진* 상태로 일하는 셈이다.
>
> **처방:** 신규 프로젝트는 첫 줄부터 `tsconfig.json`에 `"strict": true`를 켜자. 이 한 줄이 다음 7개를 한꺼번에 켠다 — `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, `alwaysStrict`. 가장 중요한 게 첫 번째 `noImplicitAny`다. 이게 켜지면 위 코드는 *컴파일 에러*가 나서 *user의 타입을 명시*하라고 강제한다.
>
> 마이그레이션 중인 레거시 코드는 *strict를 한 번에 다 켜기 어렵다*. 그럴 때는 *파일 단위로 점진적*으로 켜는 패턴이 있다 — 9장 마이그레이션 챕터에서 자세히 다룬다. 신규 프로젝트는 *예외 없이 strict로 시작*하는 편이 낫다. 처음에는 빨간 줄이 많아 짜증나지만, 그 짜증이 *런타임 폭발 한 번*보다 백배 싸다. 잊지 말자.

### Sound Gradual Typing Is Dead? — TS의 unsoundness가 합리적이었던 이유

학계가 한동안 풀고 싶어 한 문제가 있었다. *gradual typing을 sound하게(완전무결하게) 만들 수 있는가?* 이론적으로는 답이 있다. *동적 타입 영역과 정적 타입 영역의 경계마다 런타임 검사를 자동으로 끼워 넣으면* 된다. 즉, *any가 number와 만나는 자리에서 "정말 number야?"를 검사*하면 안전해진다.

문제는 *성능*이다. 검사를 어디에 얼마나 넣어야 할까? 모든 함수 호출 경계? 모든 데이터 접근? 모든 객체 통과 지점?

Takikawa, Greenman, Felleisen 등 여섯 명이 2016년 POPL에서 발표한 *Is Sound Gradual Typing Dead?* 논문이 이 질문을 *정량적으로* 풀었다. Racket 언어로 sound gradual typing 시스템을 구현하고, *부분적으로 타입을 붙인 경우의 모든 조합*을 측정했다. 결론은 충격적이었다.

> *부분적으로 타입을 붙인 코드에서, sound gradual typing은 평균 7배, 최악의 경우 100배의 슬로다운을 일으킨다.*

100배다. *디버그 모드보다도 훨씬 느리다*. 즉, *완벽하게 안전한 점진적 타입*을 *현실 코드*에 적용하면 *프로덕션이 멈춘다*.

이 논문이 발표된 게 2016년이다. TS가 *unsound한 길*을 선택한 게 2012년이다. 즉 TS 팀은 *학계가 4년 뒤에야 정량화한 진실*을 *직관적으로 먼저 알아챘다*. *우리가 sound를 포기한 건 게으름이 아니라 *현실*이다*가 사후적으로 증명되었다.

이 사실을 받아들이면 TS의 *틈*들이 다르게 보인다. 그건 *허술함*이 아니라 *비싼 트레이드오프를 정직하게 받아들인 결과*다. *완벽한 안전*과 *현실의 성능*이 충돌할 때, TS는 *현실을 골랐다*. 그 결과 우리는 오늘 *대규모 JS 코드베이스 위에서 부분적으로라도 타입의 안전망*을 받을 수 있게 되었다.

기억해두자. **TS는 *완벽한 검증자*가 아니라 *합리적인 동반자*다.** 모든 버그를 잡아주지는 않지만, 잡을 수 있는 것은 잡아주고, 못 잡는 것은 *드러내준다*. 이 자세가 손에 잡혀야 4장의 *strict 모드 가족*과 6장의 *branded type*, 그리고 9장의 *마이그레이션 전략*이 *왜 그런 모양인지* 보인다.

> **📚 Java/Kotlin 시선 — 타입 안전성의 약속이 다르다**
>
> Java/Kotlin의 타입 시스템은 *런타임 안전성을 약속*한다. `String s = "hello"`라고 선언했다면, 그 변수는 *런타임에도 String이거나, 아니면 ClassCastException으로 폭발*한다. 사이는 없다.
>
> ```kotlin
> // Kotlin
> val list: List<String> = listOf("a", "b", "c")
> val first: String = list[0]
> // first는 런타임에도 String임을 JVM이 보장
> ```
>
> TS는 다르다. TS의 타입 시스템은 *컴파일 시점의 협상*을 약속할 뿐, 런타임 안전성을 약속하지 않는다.
>
> ```ts
> // TypeScript
> const list: string[] = JSON.parse('["a", 1, true]') as string[];
> const first: string = list[0];
> // first는 number(1)일 수 있다 — 런타임에 .toUpperCase() 호출하면 폭발
> ```
>
> 이 차이를 *결함*으로 받아들이면 TS는 매일 답답한 도구다. *설계*로 받아들이면, *어디에 zod·valibot 같은 런타임 검증을 끼워 넣어야 하는지의 지도*가 손에 잡힌다. 외부에서 들어오는 모든 데이터(API 응답, 사용자 입력, 파일, 환경 변수)는 *경계에서 한 번 검증*해 *내부에서는 타입을 신뢰*하는 패턴 — 이걸 *boundary validation*이라 부른다. 13장 백엔드 챕터에서 본격적으로 다룬다.
>
> Java가 *타입을 강제*한다면, TS는 *타입을 합의*한다. 강제는 단단하지만 비용이 크고, 합의는 가볍지만 깨질 수 있다. 어느 쪽이 우월하다기보다, *서로 다른 트레이드오프*다.

## 구조적 타입 — `type UserId = string`이 그냥 `string`이 되는 첫 충격

다음 핵심 모델, *구조적 타입(structural typing)*으로 넘어가자.

상황을 가정해보자. 토스에서 일하는 백엔드 개발자가, Spring으로 짜던 결제 시스템을 NestJS로 옮긴다. Java에서는 `UserId`와 `OrderId`를 *별도의 클래스*로 분리해 *섞이지 않게* 만들었다. 컴파일러가 *UserId를 OrderId 자리에 못 넣게* 막아준다.

```kotlin
// Kotlin
@JvmInline value class UserId(val value: Long)
@JvmInline value class OrderId(val value: Long)

fun fetchOrder(id: OrderId): Order { ... }

val userId = UserId(123L)
fetchOrder(userId)  // ❌ 컴파일 에러 — UserId is not OrderId
```

든든하다. 이게 *명목 타입(nominal typing)*이다. *이름이 다르면 다른 타입*. 클래스 이름이 *타입 정체성의 핵심*이다.

같은 결정을 TS에서 해보자.

```ts
type UserId = string;
type OrderId = string;

function fetchOrder(id: OrderId): Order { ... }

const userId: UserId = "user-123";
fetchOrder(userId);  // ✅ 통과 — 컴파일 에러 없음
```

Spring 출신 개발자에게 이건 *처음 본 충격*이다. 분명 `UserId`와 `OrderId`라는 *다른 이름*을 줬는데, 컴파일러가 둘을 *구분하지 않는다*. *왜?*

TS는 *구조적 타입(structural typing)* 시스템이기 때문이다. 두 타입의 호환성을 *이름*으로 판단하지 않고 *모양*으로 판단한다. `UserId`도 모양이 `string`이고 `OrderId`도 모양이 `string`이라면, *둘은 같은 타입*이다. `type` 별칭은 *별명일 뿐, 새 타입을 만들지 않는다*.

이건 단순한 디자인 선택이 아니다. *JS의 본성*에서 직접 흘러나온 결정이다. JS는 처음부터 *모양 기반 객체*였다. *덕 타이핑(duck typing)* — *오리처럼 걸으면 오리다*. JS 함수는 *전달된 객체에 어떤 메서드가 있는지*만 보고 동작한다. *그 객체가 어떤 클래스의 인스턴스인지*는 신경 쓰지 않는다. TS의 구조적 타입은 *이 JS 본성을 정직하게 타입 시스템으로 끌어올린* 결과다.

### 구조적 타입의 *부드러움* — 한 자리에서 보이는 풍경

구조적 타입이 어떻게 작동하는지 한 자리에서 보자.

```ts
interface Named {
  name: string;
}

class Dog {
  constructor(public name: string, public breed: string) {}
  bark() { console.log("woof"); }
}

class Robot {
  name: string;
  serial: number;
  constructor(name: string, serial: number) {
    this.name = name;
    this.serial = serial;
  }
}

function greet(thing: Named) {
  console.log(`Hello, ${thing.name}`);
}

greet(new Dog("Rex", "Labrador"));         // ✅ name 있음 → 통과
greet(new Robot("R2D2", 42));               // ✅ name 있음 → 통과
greet({ name: "Plain Object" });            // ✅ name 있음 → 통과
greet({ name: "Toby", age: 30 });           // ✅ name 있음, age는 무시 → 통과
```

`Dog`, `Robot`, *그냥 객체 리터럴* 모두 *`name: string` 멤버를 가졌다는 이유 하나로* `Named` 자리에 들어간다. *어디에도 `implements Named`라고 쓴 적이 없는데도*. 멤버가 더 많아도 (`breed`, `serial`, `age`) 상관없다. *필요한 것이 있으면 통과*다.

이게 *부드러움*이다. Java/Kotlin의 명목 타입에서 온 사람에게 처음에는 *너무 헐겁다*는 인상을 준다. 익숙해지기까지 한참 걸린다.

### 부드러움의 댓가 — *도메인 안전성이 새는* 자리

이 부드러움이 좋기만 한 건 아니다. 다시 토스의 결제 시스템으로 돌아가자. `UserId`와 `OrderId`가 *둘 다 string 모양이라서 컴파일러가 구분 못 한다*는 사실은, *진짜 사고로 이어진다*.

```ts
type UserId = string;
type OrderId = string;

function refund(orderId: OrderId): void { ... }
function getCurrentUserId(): UserId { return "user-789"; }

// 어느 날 졸린 개발자가...
const userId = getCurrentUserId();
refund(userId);  // ✅ 컴파일 통과
                 // 💥 런타임에 "user-789"라는 ID로 환불 처리 시도 → 실제로 다른 사용자 환불
```

*컴파일러는 한 마디도 안 해주고 통과시켰다*. 사용자 ID를 주문 환불 함수에 넘긴 명백한 실수인데도. 이게 *구조적 타입의 헐거움이 도메인 안전성을 새게 만드는* 자리다.

찜찜한가? 찜찜해야 한다. 이게 한국 시니어 개발자가 TS를 만났을 때 가장 먼저 걸리는 *두 번째 함정*이다(첫 번째는 *묵시적 any*).

### 처방 — *branded type*으로 명목 흉내 내기

답은 있다. *모양에 가짜 표식을 하나 더 붙여서* 두 타입을 *구조적으로도 구분되게* 만드는 것. 이게 *branded type* 또는 *nominal trick*이라 부르는 패턴이다. 6장 도메인 모델링에서 본격 풀어내지만, 여기서 맛만 보자.

```ts
type UserId = string & { readonly _brand: unique symbol };
type OrderId = string & { readonly _brand: unique symbol };

function refund(orderId: OrderId): void { ... }
function getCurrentUserId(): UserId { return "user-789" as UserId; }

const userId = getCurrentUserId();
refund(userId);  // ❌ 'UserId' is not assignable to 'OrderId'
```

가짜 `_brand` 속성을 *구조에 끼워 넣어* 두 타입의 *모양이 달라지게* 만들었다. 런타임에는 그냥 string이지만, *컴파일 시점에는 다른 타입*으로 취급된다. 토스, Effect-ts, zod 같은 라이브러리가 이 패턴을 *표준화*했다. Kotlin의 `value class`와 비슷한 자리지만, *강제 메커니즘이 다르다*. Kotlin은 *컴파일러가 자동으로* 구분해주고, TS는 *개발자가 명시적으로 표식을 박아야* 한다.

이 패턴이 손에 익으면, *구조적 타입의 헐거움*을 *도메인의 결*에 맞춰 *봉합*할 수 있다. 헐거운 도구를 *헐겁게 쓰지 않는 법*이다. 6장에서 본격 다룬다.

> **📚 Java/Kotlin 시선 — Java 타입 안전성 vs TS 의도된 unsoundness**
>
> Java의 `record User(long id, String name)`은 *명목 타입*이다. *이름이 User라서 User*이고, *모양이 같은 다른 record*가 있어도 *서로 호환되지 않는다*.
>
> ```java
> // Java
> record User(long id, String name) {}
> record Customer(long id, String name) {}
>
> User u = new User(1, "Toby");
> Customer c = u;  // ❌ 컴파일 에러 — incompatible types
> ```
>
> TS의 `interface`/`type`은 *구조적 타입*이다. *모양이 같으면 같은 타입*이다.
>
> ```ts
> // TypeScript
> interface User { id: number; name: string; }
> interface Customer { id: number; name: string; }
>
> const u: User = { id: 1, name: "Toby" };
> const c: Customer = u;  // ✅ 통과 — 모양이 같아서 호환
> ```
>
> 어느 쪽이 더 좋은가? *상황에 따라 다르다*. 명목 타입은 *도메인 분리에 강하고*, 구조적 타입은 *호환성과 유연성에 강하다*. 외부 데이터를 다루는 자리에서 구조적 타입은 *덕 타이핑의 자연스러운 확장*이다 — JSON 응답이 *내가 정의한 인터페이스 모양*이면 그냥 통과시킬 수 있다. 반면 *비즈니스 도메인의 핵심 식별자*들에는 *branded type*으로 명목성을 흉내 내야 사고를 막는다.
>
> 정답은 *둘을 합치는* 것이다. *외부 경계*에서는 구조적 타입의 부드러움을 활용하고, *도메인 내부*에서는 branded type으로 명목성을 강제하자. Java만 써본 사람은 모든 자리에 *명목성을 갖다 박으려* 하는데, 그러면 TS의 부드러움이 주는 이득을 다 잃는다. *어디에 명목성이 필요한지의 결*을 익히는 게 6장의 핵심 학습 곡선이다.

## ECMAScript 정렬 — TS가 자기 길을 가지 않은 이유

다섯 번째 핵심 모델, *ECMAScript 정렬(TC39 alignment)*을 짧게 짚어두자. 이건 다른 넷에 비해 *언어 디자인의 자세*에 가까운 결정이지만, 그래서 더 중요하다.

TS는 충분히 *자기 마음대로 새 문법을 만들* 수 있는 도구다. 컴파일러를 가지고 있으니, *TS만의 키워드와 연산자*를 추가하고 *컴파일러가 알아서 JS로 풀어주는* 길도 가능했다. 실제로 초기 TS는 그랬다. `enum`, `namespace`, `parameter property`(생성자에서 `public`/`private` 한 줄로 필드 선언), legacy `decorator` — 이런 *TS 고유 문법*이 일부 들어 있다.

그런데 시간이 지나면서 TS 팀은 *방향을 바꿨다*. *우리는 ECMAScript에 합류한다*. 새 기능은 가능한 한 *TC39의 표준 진행 단계와 발맞춰* 들어가고, *TS만 가지는 신박한 문법*은 *피하거나 줄인다*. 그래서 다음과 같은 일이 일어났다.

- `class`, `async/await`, `Promise`, `import/export`, `Proxy`, optional chaining(`?.`), nullish coalescing(`??`), top-level await — *모두 ECMAScript 표준이 먼저, TS는 표준을 따라가는 모드*다.
- *데코레이터*는 TS가 일찍 도입한 `experimentalDecorators`(NestJS·TypeORM이 의존)와 *TC39가 다듬어 표준화한 새 데코레이터*가 따로 있다. TS 5.0이 *새 데코레이터로 hard pivot*을 선언했다 — 자기 길을 *고집하지 않고* 표준 쪽으로 옮겨갔다.
- TS만의 신박한 시도는 점점 *위축*되었다. `namespace`는 사실상 *권장하지 않는 문법*이 되었고, `enum`도 *union literal로 대체하라*는 권고가 정착되었다. *모든 게 ECMAScript 표준에 맞춰가는* 방향이다.

왜 이게 중요한가? *생태계 호환성*이다. TS가 자기 길을 갔다면, *TS 코드와 JS 코드가 점점 멀어졌을 것이다*. 그러면 *기존 JS 코드를 점진적으로 옮기는 시나리오*는 깨졌을 것이고, *TS가 곧 죽을* 위험에 노출됐을 것이다. *호환성을 우선시한 자세*가 결국 TS를 살렸다.

이 자세는 책 후반부에서도 반복적으로 보인다. 9장 마이그레이션에서 *왜 `allowJs`가 가능한지*, 8장 모듈/빌드에서 *왜 ESM이 결국 표준으로 자리잡았는지*, 13장 백엔드에서 *왜 Hono가 Web Standards만으로 모든 런타임에서 도는지* — 전부 *ECMAScript 정렬*이라는 한 자세에서 흘러나온 결과다.

## 컴파일타임 vs 런타임 — `instanceof`, `typeof`, `Array.isArray`로 할 수 있는 것

여기까지 다섯 모델을 다 봤다. 이제 *실무에서 매일 마주칠* 손에 잡히는 질문 하나를 다뤄보자. *런타임에 무엇을 할 수 있고 무엇을 할 수 없는가?*

타입이 다 지워진 다음, 우리에게 남은 *런타임 검사 도구*는 단 셋이다.

**(1) `typeof`** — *원시 타입*만 검사할 수 있다.

```ts
function describe(value: unknown): string {
  if (typeof value === "string") return `문자열: ${value}`;
  if (typeof value === "number") return `숫자: ${value}`;
  if (typeof value === "boolean") return `불리언: ${value}`;
  if (typeof value === "function") return `함수`;
  if (typeof value === "undefined") return `없음`;
  if (typeof value === "object") return `객체 또는 null`;  // ← null도 object!
  return `기타`;
}
```

`typeof`는 *7가지 결과*만 반환한다 — `"string"`, `"number"`, `"bigint"`, `"boolean"`, `"undefined"`, `"object"`, `"function"`, `"symbol"`. *클래스나 인터페이스 이름*은 알 수 없다. 그리고 악명 높은 함정 — `typeof null === "object"`다. JS의 *역사적 버그*인데 *고치면 호환성이 깨져* 그대로 두기로 했다. 잊지 말자.

**(2) `instanceof`** — *클래스로 정의된 타입*만 검사할 수 있다.

```ts
class HttpError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

function handleError(e: unknown) {
  if (e instanceof HttpError) {
    console.log(`HTTP ${e.status}: ${e.message}`);
  } else if (e instanceof Error) {
    console.log(`일반 에러: ${e.message}`);
  } else {
    console.log(`알 수 없는 throw 값: ${e}`);
  }
}
```

`HttpError`처럼 *클래스로 선언한 것*은 런타임에도 살아남아서 `instanceof`가 작동한다. 하지만 *`interface`나 `type`*으로 정의한 건 안 된다 — 컴파일이 끝나면 사라지기 때문이다.

`instanceof`에는 또 한 가지 함정이 있다. *프레임 경계*(iframe, worker, vm context)를 넘어오면 깨진다. 같은 `Array`인데도 *다른 컨텍스트의 Array*면 `arr instanceof Array`가 `false`가 된다. 그래서 표준 라이브러리는 더 신뢰할 수 있는 검사를 따로 제공한다 — 다음에 볼 `Array.isArray()`가 그 예다.

**(3) `Array.isArray()`, `Number.isFinite()`, 직접 만든 *type predicate*** — 더 정밀한 검사가 필요할 때.

```ts
function processItems(value: unknown) {
  if (Array.isArray(value)) {
    // 여기서 value는 any[] (또는 unknown[])로 좁혀진다
    value.forEach((item) => console.log(item));
  }
}

// 직접 만드는 type predicate
function isUser(value: unknown): value is { id: number; name: string } {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value && typeof (value as any).id === "number" &&
    "name" in value && typeof (value as any).name === "string"
  );
}

const data: unknown = JSON.parse('...');
if (isUser(data)) {
  console.log(data.name);  // ✅ data가 좁혀짐
}
```

`isUser` 함수의 반환 타입에 적힌 `value is { ... }`가 핵심이다. 이게 TS 컴파일러에게 *"이 함수가 true를 반환하면, value의 타입은 이 모양이다"*라고 *약속*하는 신호다. 4장에서 *user-defined type predicate*로 본격 다룬다.

이 셋이 우리에게 주어진 *런타임 도구의 전부*다. 그리고 이것만으로는 *복잡한 외부 데이터의 모양*을 검사하기 충분치 않다. 그래서 zod·valibot 같은 *런타임 스키마 라이브러리*가 등장했다. *컴파일러가 못 봐주는 자리*를 *런타임 검증으로 메우는* 패턴 — 6장과 13장에서 표준 처방으로 다룬다.

기억해두자. **TS의 컴파일타임은 부드럽고 똑똑하지만, 런타임에는 무력해진다. 그 경계를 어디에 그을지가 *설계*다.** 이 한 문장이 4장부터의 모든 도구가 *왜 그렇게 생겼는지*의 답이다.

## 마무리 — 우리는 무엇을 손에 쥐었는가

여기까지 왔다면 손에 쥔 게 하나 있다. *TS는 무엇이고, 무엇이 아닌가*에 대한 정직한 지도다.

다섯 핵심 모델을 다시 한번 한 자리에 모아보자. 외우려 하지 말고, *왜 그렇게 되었는지의 사연*과 함께 떠올려보자.

- **점진적 타입 (gradual)** — 타입이 붙은 코드와 붙지 않은 코드가 *함께 살 수 있게*. `any`라는 탈출구가 그 다리다. 이게 없으면 *기존 JS 30만 줄을 옮기는* 시나리오는 불가능했다.
- **구조적 타입 (structural)** — 호환을 *모양*으로 판단한다. JS의 덕 타이핑 본성을 정직하게 타입 시스템으로 끌어올린 결과. *부드럽지만 도메인 안전성은 새기 쉬워*, *branded type*으로 봉합한다.
- **의도된 unsoundness** — 학자들이 *6+ 지점*으로 정리한 의도적 *틈*. `any`의 흡수성, 함수 매개변수의 bivariance, 인덱스 시그니처의 관대함, 배열의 공변성. *완벽한 안전*과 *현실의 성능* 사이에서 *현실*을 골랐다. *Sound Gradual Typing Is Dead?* 논문이 그 결정의 합리성을 사후적으로 정량화했다.
- **타입 소거 (type erasure)** — `tsc`가 끝나면 *모든 타입이 사라진다*. Java erasure가 *제네릭만* 지운다면, TS erasure는 *전부 다* 지운다. 그래서 런타임 검증은 *별도의 도구*가 필요하다.
- **ECMAScript 정렬 (TC39)** — TS는 자기 길을 가지 않는다. 새 문법은 *TC39 표준 진행*과 정렬한다. *호환성*이라는 자세가 결국 TS를 살렸다.

이 다섯이 뼈대다. 4장부터의 모든 도구는 *이 뼈대 위에서 작동*한다. 4장의 *strict 모드 가족*은 *unsoundness의 일부 틈을 메우는 옵션*이다. 4장의 *type predicate*는 *런타임에 살아있는 셋(typeof, instanceof, isArray)을 컴파일타임 좁히기와 잇는* 다리다. 5장의 *제네릭과 conditional, infer*는 *타입이 타입을 만드는* 도구로, *type erasure의 한계 위에서도 표현력을 뽑아내는* 곡예다. 6장의 *branded type, discriminated union, immutability*는 *구조적 타입의 헐거움을 도메인의 결로 봉합*하는 패턴들이다.

3장이 *언어 철학적 골격*이라 했던 이유가 여기 있다. 4·5·6장이 *전술*이라면, 3장은 *전략*이다. 전략을 손에 쥐지 않고 전술을 외우면, 그건 *이유 없는 카탈로그*다. 같은 도구를 *왜 어떤 상황에 쓰는지*의 결을 모른다.

또 한 가지 가져갈 것. **TS를 *비판할 때*도, *옹호할 때*도, *그것이 무엇을 약속했는지*에서 출발하자.** *"왜 TS는 런타임 안전을 보장 안 해주냐"*는 비판은, TS가 *Non-goals*에 적어둔 *애초에 약속하지 않은 것*에 대한 실망이다. *"TS만 쓰면 모든 버그가 사라진다"*는 옹호도 같은 종류의 오해다. TS는 *합리적인 동반자*이지, *완벽한 검증자*가 아니다. 그 자리를 *zod·valibot·테스트 코드·코드 리뷰·관측 도구*가 함께 채운다.

다음 4장에서는 *이 뼈대 위에서 타입을 도구로 손에 익히는* 단계로 들어간다. *TS의 적극적인 추론, narrowing의 다섯 가지 도구, discriminated union과 `never`로 만드는 exhaustiveness, utility 타입 8개, strict 모드 가족*을 본격적으로 풀어낸다. Java의 `var`보다 훨씬 적극적인 추론이 *왜 그렇게 작동하는지*, Kotlin sealed class의 자리를 TS가 *어떻게 다른 결로 채우는지*가 손에 잡힐 것이다. *첫 "오, 이게 표현되는구나"의 쾌감*이 4장에 있다.

5장은 *타입이 타입을 만드는* 단계다. 제네릭·conditional·infer·매핑·템플릿 리터럴 — 한국 시니어가 *"Kotlin sealed class를 다뤄봤지만 TS에 이런 표현력이 있을 줄은 몰랐다"*라고 인정하는 자리. zod·Hono·Prisma·tRPC의 *현실 코드의 타입 마법*이 부품 단위로 분해된다.

6장은 *도메인 모델링*. 구조적 타입의 부드러움을 *도메인의 결*에 맞춰 *봉합*하는 표준 패턴들. branded type, discriminated union, immutability, *에러를 도메인의 일부로* 다루는 자세. checked exception 정신구조에서 온 사람이 TS의 throw·Result·Effect를 어떻게 받아들일지를 정직하게 푼다.

3장에서 잡은 골격이, 4·5·6장에서 *살이 붙는다*. 한 번에 익히려 하지 말자. *돌아오면서, 다시 보면서, 손에 익혀가자*. 그게 언어를 자기 도구로 만드는 길이다.

> **📖 더 깊이 가려면**
>
> - **TypeScript Design Goals** — Microsoft TS Wiki. https://github.com/Microsoft/TypeScript/wiki/TypeScript-Design-Goals — 이 챕터의 1차 자료. 영어 한 페이지 분량이라 직접 읽는 편이 낫다.
> - **TypeScript Handbook — The Basics & Type Compatibility** — https://www.typescriptlang.org/docs/handbook/2/basic-types.html — 구조적 타입의 표준 설명.
> - **Bierman, Abadi, Torgersen (2014) — *Understanding TypeScript*** — ECOOP 2014. *6+ 지점의 의도된 unsoundness*를 학술적으로 정리. PDF는 검색하면 무료로 구할 수 있다.
> - **Takikawa et al. (2016) — *Is Sound Gradual Typing Dead?*** — POPL 2016. *sound + gradual = 7~100배 슬로다운*을 정량화한 논문. 학회 발표 영상이 ACM Digital Library에 있다.
> - **Daniel Rosenwasser — TypeScript 5.0 Release Notes** — https://devblogs.microsoft.com/typescript/announcing-typescript-5-0/ — 새 데코레이터로의 *hard pivot* 결정 발표. ECMAScript 정렬 자세를 가장 잘 보여주는 글.
> - **velopert(김민준) — TypeScript Handbook 한국어판** — https://typescript-kr.github.io/ — 영문 핸드북을 처음 한국어로 정독하는 데 가장 안정적인 길.
> - **토스 기술블로그 — JavaScript에서 TypeScript로 바꾸기** — https://toss.tech/article/typescript-1 — 한국 현장에서 *점진적 타입의 실전*이 어떻게 적용되었는지를 본 시리즈.
> - **이펙티브 타입스크립트** (Dan Vanderkam, 인사이트 번역) — *구조적 타입과 의도된 unsoundness*에 대한 챕터들이 이 책 3장의 자매 자료다.
