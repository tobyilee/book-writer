# 15장. 한국 현장의 TypeScript — 함정·논쟁·AI 시대·다음 한 걸음

입사 첫날을 떠올려보자. 이력서에 Spring Boot 5년, Kotlin 3년을 써서 냈는데, 팀 리드가 슬랙으로 링크 하나를 보내온다. "프론트도 같이 봐야 해서요, TypeScript 리포지터리예요." 당연히 열어본다. 코드를 스크롤하는 동안 눈이 미묘하게 흔들린다. `any`가 여기저기 널려 있고, `tsconfig.json`은 옵션이 수십 개다. 익숙한 `@RestController`, `@Service`, `@Autowired`는 없고, 예외 처리가 어디서 이루어지는지 당장 눈에 들어오지 않는다. 무엇보다 이상한 건, 분명히 타입이 있는데도 런타임에서 `TypeError: Cannot read properties of undefined`가 튀어나온다는 점이다.

"타입이 있으면 안전한 거 아닌가?" — 이 질문을 처음 품는 순간이 Java/Kotlin 개발자가 TypeScript를 진지하게 배우기 시작하는 순간이다. 타입이 있어도 안전하지 않을 수 있다는 사실, 그리고 그 이유를 이해하는 것이 이 책 전체의 뼈대였다.

이 책은 그 질문에서 출발했다. 1장에서 TS가 JS의 슈퍼셋이라는 말의 진짜 의미를 짚었다. 언어 스펙이 아니라 타입 체커를 씌운다는 것, 그리고 그 타입 체커가 런타임에는 존재하지 않는다는 것. 2장에서 구조적 타입 시스템의 작동 원리를 파헤쳤다. Java의 명목적 타입과 달리 TypeScript는 형태(shape)가 같으면 같다고 보고, 그 관대함이 어디서 독이 되는지를 봤다. 3장에서는 타입 좁히기와 discriminated union으로 런타임 안전성을 타입 레벨로 끌어올리는 패턴을 익혔다. 4장에서 제네릭이 Java 제네릭과 어떻게 닮고 어떻게 다른지를 비교했다. 5장에서 유틸리티 타입과 타입 연산으로 반복 없이 타입을 조합하는 법을 배웠다. 6장에서 비동기와 에러 — TypeScript 생태계에서 가장 조용히 실수가 쌓이는 영역 — 를 다뤘다. 7장은 this의 함정, 8장은 모듈 시스템과 빌드 도구, 9장은 의존성 주입과 IoC 컨테이너, 10장은 마이그레이션 전략, 11장은 TS를 도구로 실행하는 CLI와 런타임 환경, 12장은 프론트엔드 프레임워크, 13장은 풀스택과 백엔드 프레임워크, 14장은 테스트 전략이었다.

이제 마지막 장이다. 마지막 장의 역할은 새로운 개념을 쌓는 것이 아니다. 지금까지 걸어온 길에서 한국 현장이 어디에서 자주 미끄러지는지를 지도로 그리고, 업계에서 아직 결론이 나지 않은 논쟁들을 균형 있게 정리하고, AI가 TS 코드를 짜는 시대에 사람이 서야 할 자리를 짚고, 이 책을 덮은 다음 어디로 더 깊이 들어갈 수 있는지를 안내한다. 지도와 닫음의 챕터다.

---

## 한국 현장의 함정 — 다섯 가지 카테고리

Java/Kotlin 배경의 개발자가 TypeScript에서 실수를 저지르는 패턴은 무작위가 아니다. 반복된다. 수십 명의 선배가 이미 같은 자리에서 미끄러졌고, 같은 PR 코멘트를 받았고, 같은 밤샘 디버깅을 했다. 그 자리를 미리 알면 최소한 "아, 이게 그 함정이구나" 하고 잠시 멈출 수 있다. 지뢰를 제거하는 것도 가능하지만, 지뢰가 어디 있는지를 아는 것이 먼저다.

리서치와 커뮤니티 경험을 통해 수집한 함정은 12개다. 각 함정의 상세 증상과 처방은 **부록 D**에서 다룬다. 여기서는 큰 카테고리 다섯 개로 묶어 위치를 표시한다. 지도를 그리는 것이 목적이므로, 세부 지형보다 지형의 이름과 대략적인 위치를 먼저 알아두자.

---

### 카테고리 1: 타입 통제의 실패 — `any`의 전염과 구조적 타입의 헐렁함

첫 번째이자 가장 흔한 카테고리는 타입 자체를 잃어버리는 실수다. 타입이 있는 언어를 쓰면서 타입을 잃어버린다는 말이 모순처럼 들리겠지만, TypeScript에서는 충분히 가능한 일이다.

`any`는 TypeScript가 제공하는 공식적인 탈출구다. "이 값의 타입은 신경 쓰지 않겠다"는 선언이다. 타입 추론이 막혔을 때, 서드파티 라이브러리의 타입 정의가 부정확할 때, 마이그레이션 중에 일단 통과시키고 싶을 때 `any`를 쓴다. 문제는 `any`가 전염된다는 것이다.

상황을 그려보자. 동료가 API 응답을 파싱하는 함수 하나에 `any`를 붙였다. 반환 타입이 `any`다. 그 반환값을 받는 변수도 자동으로 `any`가 된다. 그 변수를 인자로 받는 함수도, 그 함수가 돌려주는 값도, 그 값을 사용하는 컴포넌트의 props도 전부 `any`로 오염된다. 처음에는 파일 하나였는데, 한 달 후에는 프로젝트 절반이 `any`의 바다가 되어 있다. 어느 시점부터는 타입 체커가 사실상 꺼진 것과 다름없다. 그런데 IDE는 아무 빨간 줄도 그어주지 않는다. `any`는 "모든 타입과 호환된다"는 선언이기 때문이다.

팀 전체가 `strict: true`를 켜지 않은 채 개발하다 보면 이 상황이 더 빨리 온다. `strict` 모드 없이는 `noImplicitAny`가 꺼져 있어서, 타입 추론이 `any`로 귀결될 때 경고 없이 통과한다. 2장에서 프로젝트를 시작하자마자 `strict: true`를 켜라고 강하게 권한 이유가 여기에 있다.

구조적 타입의 헐렁함은 다른 종류의 함정이다. Java나 Kotlin에서 `UserId`와 `OrderId`는 서로 다른 클래스다. 컴파일러가 두 타입을 혼동하면 바로 에러를 낸다. TypeScript의 구조적 타입 시스템에서는 둘 다 `number`라면, 혹은 둘 다 `{ value: number }` 형태라면, 두 타입은 서로 호환된다. `createOrder(userId: OrderId)`에 `UserId` 값을 넣어도 컴파일러가 통과시킨다.

이를 막으려면 branded type 패턴이 필요하다. `type UserId = number & { readonly __brand: 'UserId' }`처럼 구조에 유일한 식별자를 붙이는 방식이다. 5장에서 이 패턴을 다뤘다. 그런데 실무에서 branded type을 프로젝트 초기부터 전면 도입하는 팀은 드물다. "나중에 필요해지면 하면 되지"라는 판단이 앞선다. 대부분은 버그가 터지고 원인을 추적하다 "어, 여기서 UserId를 OrderId 자리에 넣었네"를 발견한 뒤에야 패턴을 도입한다.

이 카테고리에 속하는 함정은 **부록 D의 함정 1번(묵시적 any와 strict 모드)**과 **함정 2번(구조적 타입의 헐렁함과 branded type)**이다. 두 함정 모두 코드베이스 초기 설정 단계에서 결정이 난다. 나중에 고치려면 전체 코드를 뒤집어야 한다. 처음 설정에 주의를 기울이는 편이 백배 낫다.

타입 통제 실패의 세 번째 축이 있다. `this` 바인딩의 유실이다. Java와 Kotlin에서 `this`는 항상 현재 클래스 인스턴스를 가리킨다. TypeScript에서도 클래스 메서드 안에서는 마찬가지지만, 메서드를 변수에 담거나 콜백으로 넘기는 순간 `this`가 사라진다.

```typescript
class PaymentService {
  private readonly fee = 0.03;

  calculateFee(amount: number): number {
    return amount * this.fee; // this.fee = 0.03
  }
}

const service = new PaymentService();
const calc = service.calculateFee; // 메서드를 변수에 담음
calc(1000); // TypeError: Cannot read properties of undefined (reading 'fee')
```

`calc`를 직접 호출하면 `this`가 `undefined`다. 이벤트 핸들러나 타이머 콜백에 클래스 메서드를 그대로 넘기면 이 함정에 빠진다. 해결은 화살표 함수로 메서드를 정의하거나 `bind(this)`를 쓰는 것이다. 7장에서 다뤘다. 이 함정은 **부록 D의 함정 3번(`this`가 사라진다)**이다.

---

> **📚 Java/Kotlin 시선 — 입사 첫째 주에 자주 헷갈리는 다섯 가지**
>
> Spring/Kotlin 시니어가 TypeScript 코드베이스에 처음 합류할 때, 가장 자주 "응?" 하는 순간들을 구체적으로 정리해보자. 이 목록을 보고 "맞아, 나도 그랬어"가 아니라 "아, 이런 게 있구나"로 읽을 수 있다면 더 좋다.
>
> **① `@Autowired` 대신 생성자 주입인데 DI 컨테이너가 안 보인다**
>
> NestJS는 `@Injectable()` 데코레이터와 모듈의 `providers` 배열로 DI를 구성한다. Spring의 component scan처럼 클래스패스를 전체 스캔하지 않는다. 모듈에 명시적으로 등록하지 않은 클래스는 주입되지 않는다. "왜 주입이 안 되지?" 하며 한 시간 이상 헤매는 경우가 많다. 9장의 NestJS 모듈 구조를 다시 보면 도움이 된다.
>
> **② `interface`와 `type alias`가 둘 다 있는데 언제 뭘 써야 하는가**
>
> Java에서 `interface`는 계약이고 `class`는 구현이다. TypeScript에서 `interface`와 `type alias`는 많은 경우 교환 가능하지만 미묘하게 다르다. 선언 병합(declaration merging)은 `interface`에서만 된다. 즉, 같은 이름의 `interface`를 두 번 선언하면 하나로 합쳐지는 것이 TypeScript의 의도된 기능이다. 라이브러리 타입 확장에 이 기능이 쓰인다. 처음 보면 당황스럽다.
>
> **③ `null`과 `undefined`가 둘 다 있다**
>
> Java는 null 하나다. TypeScript는 `null`과 `undefined` 두 개다. `strictNullChecks`를 켜면 둘을 명시적으로 구분해야 한다. 함수가 값을 반환하지 않으면 `undefined`를 반환한다. 객체 속성이 선택적(`?`)이면 `undefined`다. 외부에서 명시적으로 "없음"을 전달할 때는 `null`을 쓰는 패턴이 있지만, 코드베이스마다 다르다. "이게 왜 `undefined`야, `null` 아니고?" — 이 질문을 첫 주에 세 번 이상 하게 된다.
>
> **④ `enum`이 있는데 왜 union literal을 쓰라고 하는가**
>
> TypeScript의 `enum`은 Java의 `enum`과 비슷해 보인다. 그런데 수치 열거형(numeric enum)에는 역방향 매핑이라는 함정이 있다. `Direction.UP`의 값이 `0`이고, 동시에 `Direction[0]`이 `"UP"`이 된다. 이 역방향 매핑이 예상치 못한 동작을 만들기도 한다. 커뮤니티의 합의는 `type Direction = 'UP' | 'DOWN' | 'LEFT' | 'RIGHT'` 형태의 string literal union을 쓰는 것이다. 처음엔 낯설지만, 실제로 더 예측 가능하고 타입 추론이 잘 된다.
>
> **⑤ `catch (e)`의 `e`는 타입이 없다**
>
> Java에서 `catch (IOException e)`는 `e`의 타입이 `IOException`으로 명시된다. TypeScript에서 `catch (e)`의 `e`는 `unknown` 타입이다(`useUnknownInCatchVariables: true`가 기본인 `strict` 모드에서). `e.message`를 바로 쓰면 컴파일 에러가 난다. `instanceof Error`로 좁혀야 한다. 처음엔 번거롭다고 느껴지지만, 예외가 반드시 `Error` 인스턴스인 것은 아니라는 사실을 인지하고 나면 오히려 안전한 습관이 생긴다. `throw "something went wrong"` 같은 코드를 라이브러리 어딘가가 쓸 수도 있기 때문이다.

---

### 카테고리 2: 비동기와 에러 — 조용히 사라지는 예외들

Java Spring의 예외 처리는 편안하다. `@ControllerAdvice`와 `@ExceptionHandler`를 조합하면 어디서 예외가 터지든 중앙에서 잡힌다. 개별 컨트롤러가 예외를 직접 처리하지 않아도 된다. 스프링 프레임워크가 스택 추적을 로깅하고, 적절한 HTTP 응답을 만들어 돌려준다.

TypeScript/Node.js 생태계에서 이것을 당연하게 기대하면 난감한 상황이 생긴다.

NestJS를 쓴다면 exception filter가 Spring의 `@ControllerAdvice`와 비슷한 역할을 한다. 그런데 Express나 Hono, Fastify를 쓴다면 이 구조를 직접 만들어야 한다. 그리고 만들지 않으면, 예외가 어디선가 터졌는데 HTTP 응답은 그냥 502나 503으로 나가거나, 더 나쁜 경우 응답 자체가 없이 커넥션이 끊어진다.

`async/await`의 에러가 특히 조용하다. `async` 함수 안에서 `throw`된 예외는 그 함수가 반환하는 Promise를 reject 상태로 만든다. 이 Promise를 `await`하지 않으면, 예외는 아무도 잡지 않은 채 공중에 뜬다. 코드를 살펴보자.

```typescript
async function processPayment(orderId: string): Promise<void> {
  // 뭔가 잘못됐을 때 throw
  throw new Error("결제 실패");
}

// await 없이 호출하면?
function handleRequest() {
  processPayment("order-123"); // await 없음
  console.log("여기까지는 실행된다");
}
```

`handleRequest()`를 실행하면 "여기까지는 실행된다"가 출력된다. 그리고 Promise는 어디서도 잡히지 않는다. Node.js 버전에 따라 조용히 무시되거나, `UnhandledPromiseRejectionWarning`을 출력하거나, 프로세스가 종료된다. 어느 쪽이든 원하는 동작이 아니다.

Java의 checked exception이 답답하게 느껴졌던 개발자도, 이 경험을 하고 나면 솔직해진다. "그래도 checked exception은 잊기 어렵게 만들어놨구나." TypeScript에서는 `async` 함수를 호출할 때 `await`를 빠뜨리는 순간 에러가 공중에 뜬다. IDE나 컴파일러가 경고해주지 않는다. ESLint의 `@typescript-eslint/no-floating-promises` 규칙을 켜면 이 실수를 잡을 수 있다. 켜자.

또 다른 함정은 `async` 함수 내부의 콜백이다.

```typescript
async function processItems(items: string[]): Promise<void> {
  items.forEach(async (item) => {
    await doSomething(item); // 이 await는 forEach의 콜백 안에만 적용된다
  });
  // forEach 자체는 Promise를 기다리지 않는다
}
```

`forEach`에 `async` 콜백을 넘기면 각 콜백이 Promise를 반환하지만, `forEach` 자체는 그 Promise들을 기다리지 않는다. 결과적으로 `processItems`가 반환된 시점에 `doSomething`이 아직 실행 중일 수 있다. 이런 상황에서 `for...of`나 `Promise.all`을 써야 한다.

```typescript
// 순차 처리
async function processItems(items: string[]): Promise<void> {
  for (const item of items) {
    await doSomething(item);
  }
}

// 병렬 처리
async function processItemsParallel(items: string[]): Promise<void> {
  await Promise.all(items.map((item) => doSomething(item)));
}
```

이 카테고리의 함정은 **부록 D의 함정 4번(비동기 에러의 실종)**이다. 6장에서 이 패턴들을 더 깊이 다뤘다.

비동기와 에러 카테고리에서 특히 한국 현장에서 자주 등장하는 추가 패턴이 있다. NestJS를 쓰는 팀에서 TypeORM이나 Prisma 트랜잭션을 다룰 때다. Spring의 `@Transactional`은 선언적으로 트랜잭션 경계를 설정한다. TypeORM에서는 `QueryRunner`를 직접 관리하거나 `dataSource.transaction()` 콜백을 써야 한다. Prisma는 `prisma.$transaction()` 콜백 방식이다. 이 콜백 안에서 `async` 작업이 여러 개 있을 때 하나라도 `await`를 빠뜨리면 트랜잭션이 커밋된 뒤에야 에러가 감지되거나, 에러가 아예 감지되지 않는다.

```typescript
// 위험한 패턴 — Prisma 트랜잭션 안에서 await 누락
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: userData });
  // await를 빠뜨렸다
  tx.order.create({ data: { userId: user.id, ...orderData } }); // 트랜잭션 밖에서 실행될 수 있다
});

// 안전한 패턴
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: userData });
  await tx.order.create({ data: { userId: user.id, ...orderData } });
});
```

Spring의 `@Transactional`에 익숙한 개발자가 이 차이를 인지하지 못하면, 데이터 정합성 버그가 프로덕션에서 조용히 발생한다. 에러가 나지 않기 때문에 더 찾기 어렵다.

---

### 카테고리 3: 도구 분열 — CJS/ESM, tsconfig 지옥, monorepo IDE 폭주

TypeScript 생태계에서 가장 찜찜한 영역을 꼽자면 도구 설정이다. Java Maven이나 Gradle에서는 빌드 설정이 상대적으로 단순하다. `pom.xml`이나 `build.gradle`에 의존성을 선언하고 플러그인을 붙이면 대부분 돌아간다. TypeScript는 다르다.

**CommonJS와 ESM의 공존**부터 이야기하자. Node.js가 오랫동안 CommonJS(`require()`/`module.exports`) 방식으로 모듈을 불러왔다. ECMAScript 표준은 ESM(`import`/`export`)을 정의했고, Node.js가 뒤늦게 지원했다. 문제는 수십만 개의 npm 패키지가 여전히 CommonJS 기반이라는 점이다. 순수 ESM 패키지는 CommonJS 환경에서 `require()`로 불러올 수 없다. 반대 방향도 마찬가지다.

`package.json`에 `"type": "module"`을 추가하면 Node가 해당 패키지를 ESM으로 취급한다. 그런데 이 한 줄이 기존에 잘 돌아가던 CommonJS 코드를 깨트린다. `ERR_REQUIRE_ESM` 에러가 나온다. 이 에러를 처음 보는 순간 멍해진다. 에러 메시지가 원인을 알려주긴 하지만, 해결 방법은 여러 개고 각각 트레이드오프가 있다.

상황을 더 복잡하게 만드는 것이 `tsconfig.json`이다. TypeScript 컴파일러 옵션은 70개가 넘는다. 그 중에서 `target`, `module`, `moduleResolution`의 조합이 핵심이다.

- `target`: 컴파일된 JS가 어떤 ECMAScript 버전을 지향하는가
- `module`: 생성될 모듈 코드가 CommonJS인가 ESM인가 등
- `moduleResolution`: 모듈 이름을 파일 시스템에서 어떻게 찾는가

이 세 옵션의 조합이 어긋나면 기묘한 상황이 생긴다. 코드는 런타임에 동작하는데 IDE가 빨간 줄을 그어놓거나, IDE는 통과했는데 빌드가 깨지거나, 빌드까지 통과했는데 런타임에서 모듈을 못 찾는 에러가 난다. Matt Pocock의 tsconfig cheat sheet가 한국 개발자들 사이에서 필수 북마크가 된 이유가 여기에 있다. 수십 개의 옵션 중에서 현재 상황(Node.js 서버인지, 브라우저 번들인지, 라이브러리인지)에 맞는 조합이 정해져 있다는 것을 알면 훨씬 단순해진다.

Node.js 서버(ESM)를 위한 최소 설정을 예로 들면:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "strict": true
  }
}
```

`module`과 `moduleResolution`을 `Node16`으로 맞추면 Node.js의 ESM 동작 방식을 TypeScript가 정확히 이해한다. 이 설정 없이는 `.js` 확장자를 import 경로에 붙여야 하는 이유를 IDE가 이해하지 못한다.

monorepo를 도입하면 한 단계 더 복잡해진다. 여러 패키지가 각자의 `tsconfig.json`을 가지면서 서로를 참조할 때, TypeScript의 project references(`tsconfig.references`) 기능을 써야 IDE의 언어 서버가 각 패키지의 경계를 올바르게 인식한다. 이것 없이 수십 개의 패키지를 monorepo에 놓으면 IDE의 TypeScript 서버가 모든 파일을 하나의 거대한 프로젝트로 인식하려 들고, 메모리와 CPU를 폭주시킨다. 에디터가 느려지거나 멈추는 증상이 나온다.

카카오의 "TypeScript Monorepo with pnpm" 기술블로그 글과 당근의 "한 모노레포에서 1000명이 일하는 법"이 한국 학습의 표준 레퍼런스가 된 것은 이 문제가 그만큼 보편적이기 때문이다. 같은 문제로 고생하는 개발자들이 많았고, 그 경험을 글로 남긴 팀들이 있다.

이 카테고리의 함정은 **부록 D의 함정 5번(CJS/ESM 혼란), 함정 6번(tsconfig 지옥), 함정 12번(monorepo IDE 폭주)**이다. 8장에서 이 영역을 다뤘다.

---

### 카테고리 4: 직무 비대칭 — 백엔드는 Spring, 프론트는 TS

이것은 순수한 기술 문제가 아니다. 한국 IT 시장의 구조에서 오는 문제다. 그러나 그 구조가 기술 선택과 학습 경로에 직접 영향을 미친다.

한국 IT 대기업과 SI 업계에서 백엔드는 Java/Spring이 압도적으로 지배한다. 채용 공고를 보면 "Node.js 백엔드" 또는 "NestJS"를 찾는 공고는 Spring 백엔드 대비 한 자릿수 비율이다. 반면 신규 채용 공고에서 TS Node.js 백엔드 비율은 빠르게 늘고 있다. 신생 스타트업, 핀테크, 플랫폼 기업(토스, 당근, 라인, 쿠팡 일부 팀)에서는 이미 Node.js 백엔드가 표준이 된 곳도 있다.

프론트엔드는 이야기가 다르다. TypeScript 없이 프론트엔드 개발자 채용 공고를 낸다는 것은 이미 몇 년째 상상하기 어려운 일이 됐다. "TypeScript 안 쓰면 면접 컷"이라는 말이 정설로 굳어졌다.

이 비대칭이 만드는 문제가 있다.

첫째, 백엔드 Java 시니어가 풀스택 또는 프론트 역할을 겸해야 하는 상황에 놓인다. TS를 주요 기술로 깊이 배우기보다, "일단 돌아가는" 수준에서 사용하게 된다. `any`로 때우고, 에러 처리를 대충 하고, 타입이 실제로 안전한지 확인하지 않는다. 이 태도가 팀 코드베이스 전체의 품질을 갉아먹는다.

둘째, 프론트엔드 TS 시니어가 백엔드 역할을 맡으면, NestJS의 모듈 DI 구조, TypeORM 또는 Prisma의 트랜잭션 처리, 인프라와 배포 관리에서 Spring 경험 없이 혼란스러워한다. TS를 잘 쓴다고 NestJS의 아키텍처를 자동으로 이해하지는 않는다. Java/Spring의 아키텍처 개념이 배경에 있어야 NestJS가 왜 그렇게 설계됐는지가 보인다.

셋째, 팀 내에서 백엔드(Java)와 프론트(TS) 개발자 간의 기술 언어가 달라진다. 백엔드는 Spring MVC, 서블릿 컨텍스트, JPA의 개념으로 이야기하고, 프론트는 React 렌더 사이클, 상태 관리, 번들 최적화 언어로 이야기한다. 두 팀이 같은 테이블에 앉아도 서로 다른 문제를 보고 있는 경우가 많다. API 설계 회의가 이 간극의 가장 뚜렷한 현장이다.

이 책이 Java/Kotlin 개발자를 독자로 설정한 이유가 이 비대칭에 있다. 백엔드 강자의 지식과 직관을 TypeScript 전환에서 최대한 살릴 수 있도록, 공통점과 차이점을 명확히 보여주는 것이 이 책의 목표였다.

---

> **📚 Java/Kotlin 시선 — 한국 채용시장 비대칭 분석**
>
> | 구분 | 백엔드 | 프론트엔드 |
> |------|--------|------------|
> | 지배 기술 | Java/Spring | TypeScript + React |
> | Node.js/TS 서버 비율 | 신생 스타트업·핀테크·플랫폼 한정 | — |
> | TypeScript 필수 여부 | 선택 (증가 중) | 사실상 필수 |
> | NestJS 채용 현황 | 점진 증가 (라인플러스, 쿠팡 일부, 토스) | — |
> | 학습 동기 | 풀스택 전환, 사이드 프로젝트, 경력 다변화 | 취업·이직 직결 |
> | 주요 학습 레퍼런스 | NestJS 공식 문서, Spring 비교 글, 이 책 | React 공식, velopert, 토스 블로그 |
> | 코드 리뷰 갈등 | "`any` 쓰지 말라"는 프론트 리뷰어 vs "왜?"라는 백엔드 PR 작성자 | — |
>
> 이 비대칭은 단순히 시장 정보로 그치지 않는다. 팀 온보딩 설계, 코드 리뷰 기준, 기술 세미나 주제 선택에서도 이 차이를 인식해야 한다. 백엔드 시니어에게 React Hook의 의존성 배열을 설명하는 방식과, 프론트 시니어에게 NestJS 모듈 등록 방식을 설명하는 방식은 다르다. 이 책이 "Java/Kotlin 개발자를 위한"이라는 부제를 달고 있는 것은 그런 맥락에서다. 배경에 따라 무엇이 낯설고 무엇이 익숙한지가 달라진다. 낯선 것을 낯설다고 인정하는 것이 배움의 시작이다.

---

### 카테고리 5: 학습 자원 미스매치 — 깊이가 빠진 한국어 자료

다섯 번째 카테고리는 기술 문제가 아니라 학습 자원의 문제다. "어디서 배우느냐"가 "무엇을 배우느냐"를 결정한다.

TypeScript의 한국어 학습 자원은 양적으로는 충분하지만, 깊이의 편차가 크다. 기초 문법과 기본 사용법을 다루는 자료는 넘친다. "인터페이스 쓰는 법", "제네릭 기초", "tsconfig 설명" 같은 내용은 검색하면 수십 개가 나온다. 그런데 "왜 TypeScript의 타입 시스템이 이렇게 설계됐는가", "구조적 타입과 명목적 타입의 트레이드오프는 무엇인가", "점진적 타입 시스템의 이론적 배경은 무엇인가"를 한국어로 체계적으로 설명한 단일 자료는 드물다.

결과적으로 많은 개발자가 "어떻게 쓰는가"는 알지만 "왜 이렇게 작동하는가"를 모른다. 이 공백이 실무에서 원인 불명의 타입 에러를 만날 때 드러난다. 에러 메시지가 나오는데 왜 나오는지 이해하지 못한다. 해결책을 검색해 복사-붙여넣기 하고 되면 넘어간다. 패턴을 이해하지 못했으니 다음 번에 비슷한 상황이 오면 또 같은 과정을 반복한다.

이 책이 그 빈자리를 채우려 했다. "TypeScript는 이렇게 쓰세요"가 아니라 "TypeScript는 왜 이렇게 생겼는가"를 설명하는 것이 이 책의 약속이었다. 그 약속이 얼마나 이루어졌는지는 독자가 판단할 몫이다.

이 카테고리의 함정은 **부록 D의 함정 8번(런타임 선택 불안)**과 **함정 7번(빌드 도구 피로)**에서 구체적으로 드러난다. "선택지가 너무 많아서 뭘 골라야 할지 모르겠다"는 상태가 학습 자원 미스매치의 가장 흔한 증상이다.

한 가지 덧붙이자. 학습 자원 미스매치가 가장 치명적으로 드러나는 순간이 있다. 공식 문서와 실무 사이의 간극이다. TypeScript 공식 핸드북은 언어 기능을 잘 설명하지만, "실제 프로젝트에서 `tsconfig.json`을 어떻게 세팅하는가", "monorepo에서 패키지 사이의 타입을 어떻게 공유하는가", "Next.js App Router와 서버 액션의 타입을 어떻게 설계하는가"를 체계적으로 설명하지 않는다. 이 간극을 한국어로 채운 자료가 드물다. 결국 영어 블로그, GitHub 이슈, Stack Overflow 답변을 조합해서 퍼즐을 맞추는 과정을 거친다. 이 과정이 번거롭다. 시간이 오래 걸린다. 그리고 각자가 파편적으로 배운 내용이 팀 안에서 충돌하면 "왜 이렇게 설정했어요?"라는 질문이 나온다.

이 간극을 줄이는 가장 실용적인 방법은 팀 위키에 "우리 프로젝트의 TypeScript 설정 결정 기록"을 남기는 것이다. `tsconfig.json`의 각 옵션을 왜 이렇게 설정했는지, 빌드 도구를 왜 이것을 골랐는지를 짧게라도 문서화해두면 온보딩 비용이 크게 줄어든다.

---

## 일곱 개의 논쟁 — 결론이 없는 것들을 균형 있게 보는 법

기술 논쟁에서 한쪽 입장만 옳은 경우는 거의 없다. 맥락이 결론을 바꾼다. 팀 규모, 프로젝트 수명, 기존 스택, 팀원의 배경, 서비스 특성이 모두 "어떤 선택이 낫다"를 결정한다. 여기서는 TypeScript 생태계에서 현재 진행 중인 일곱 개의 논쟁을 정리한다. 강요가 아니라 지도다. 각 논쟁에서 어느 입장이 맞는지는 각자의 맥락에서 판단해야 한다. 이 책은 그 판단에 필요한 정보를 제공하는 것까지만 책임진다.

---

### 논쟁 A: TypeScript는 JS의 올바른 길인가, 또 다른 복잡성 레이어인가

이 논쟁은 TypeScript 생태계의 근본적인 정당성 논쟁이다. "TS를 써야 하는가"가 이미 정착된 팀에서는 한가한 질문처럼 들리겠지만, 설득해야 하는 사람이 있거나 규모가 작은 팀에서 도입을 고민할 때 다시 나오는 질문이다.

**관점 1 — 옹호:** JS만으로 큰 시스템을 짜본 개발자들은 대부분 TS 없이는 어렵다고 말한다. 함수 하나의 시그니처를 보고 "이 함수가 뭘 받아서 뭘 돌려주는가"를 알 수 있다는 것은 협업의 질을 바꿔놓는다. 코드를 작성한 지 6개월이 지난 뒤에도 타입이 문서 역할을 해준다. Stack Overflow 개발자 설문에서 TypeScript는 수년째 "admired" 비율 상위에 있고, GitHub Octoverse에서의 성장세도 같은 방향을 가리킨다. 시장이 이미 답을 냈다는 입장이다.

**관점 2 — 회의:** 결국 빌드 단계가 추가되고, `tsc`는 대규모 코드베이스에서 느리고, TypeScript의 타입 시스템은 엄밀한 의미에서 sound하지 않다. `any`를 허용하고, 구조적 타입이 과도하게 관대하고, 런타임에 타입 정보가 없다. 진짜 해법은 TC39를 통해 ECMAScript 표준 자체에 타입이 들어오는 것이라고 주장한다. "Type Annotations as Comments" 제안이 그 방향이다. 이 제안이 표준이 되면 TypeScript 없이도 타입 주석을 JS에 직접 쓸 수 있게 된다.

**중간 입장:** TS 5.x와 새로 발표된 Go 재작성 버전(TypeScript Native)으로 도구 측 단점이 줄어들면 회의론의 근거가 약해진다. 완벽하지 않지만, 현재로서는 JS 대규모 시스템에서 최선의 균형이다. "안 쓰는 것보단 낫다"로 수렴하는 것이 한국 커뮤니티의 솔직한 결론이다.

**남은 공백:** JS 표준에 타입이 들어오는 날이 실제로 온다면, TypeScript의 위치는 어떻게 달라질까. 타입 소거(type stripping) 방향과 타입 체크 방향 중 어느 것이 표준이 될 것인가. TC39 제안 동향을 주시할 필요가 있다.

이 논쟁에서 한 가지만 짚고 넘어가자. TypeScript 회의론자들이 흔히 드는 반례가 있다. "타입이 있어도 런타임에서 `undefined`가 나온다. 그럼 타입이 무슨 소용인가?" 이 질문에 대한 정직한 답은 이렇다. TypeScript의 타입은 "이 코드가 절대 안전하다"를 보장하지 않는다. 대신 "이 특정 종류의 실수를 컴파일 타임에 잡는다"를 제공한다. 범위가 제한적이지만, 그 범위 안에서는 실질적이다. 타입이 없는 대규모 JS 코드베이스에서 리팩터링을 해본 사람은 그 차이를 몸으로 안다. 함수 시그니처가 바뀌었을 때 어디가 깨지는지를 컴파일러가 알려주는 것과 런타임에서 발견하는 것의 차이다.

---

### 논쟁 B: Bun/Deno는 Node.js를 대체할 수 있는가

이 논쟁은 2024~2025년 Node.js 생태계에서 가장 뜨거운 주제 중 하나다. 11장에서 런타임 선택을 다뤘는데, 여기서는 산업적 전망을 본다.

**관점 1 — Bun 옹호:** Bun은 Node.js 생태계 호환성을 거의 완전히 끌어왔다. 속도는 압도적이다. 번들링, 테스트 러너, 패키지 매니저를 모두 내장해서 별도 도구 없이 TS 개발이 가능하다. CLI 도구와 개발 툴링 시장에서는 이미 Bun 채택이 상당히 진행됐다. `bun run index.ts`로 TypeScript 파일을 직접 실행할 수 있다는 편리함은 한번 경험하면 돌아가기 어렵다.

**관점 2 — Node.js 잔류:** 11년이 넘는 안정성, 깊은 npm 생태계, 기업의 LTS 의존 사이클은 쉽게 바뀌지 않는다. Bun의 long-running 서버 환경에서의 edge case와 메모리 관련 보고가 있다. 프로덕션 전환 비용이 크고, 무엇보다 "Bun이 프로덕션에서 안정적이다"는 신뢰가 Node.js만큼 쌓이지 않았다.

**관점 3 — Deno의 길:** 보안 모델이 독보적이다. 명시적 권한 없이는 파일 시스템, 네트워크, 환경 변수에 접근할 수 없다. 표준 라이브러리가 내장돼 있어 npm 의존성을 최소화할 수 있다. Deno 2의 npm 호환으로 기존 생태계를 사용할 수 있게 됐다. "보안이 중요한 환경"에서는 Deno가 설득력 있다.

**현재 합의:** 2025년 기준 실용적 분업이 정착되고 있다. 로컬 개발과 CLI 도구는 Bun, 프로덕션 서버는 Node.js, 보안과 표준이 중요한 환경은 Deno. 한국 커뮤니티는 "재미있어 보이지만 프로덕션은 아직"이라는 신중한 정서가 지배적이다. 일본 커뮤니티(Hono 저자가 일본인이다)의 적극성과 비교하면 대비가 뚜렷하다.

**남은 공백:** Bun이 프로덕션 안정성을 공식적으로 보증하는 시점, 그리고 기업이 LTS 수준의 신뢰를 언제 줄 수 있는가. 이 질문이 해소되는 속도가 생태계 이행 속도를 결정한다.

---

### 논쟁 C: NestJS는 새 TC39 데코레이터로 이전할 수 있는가

이 논쟁은 한국 NestJS 사용자에게 특히 예민하다. 라인플러스, 쿠팡, 다수의 핀테크 스타트업이 NestJS를 프로덕션에서 쓰고 있기 때문이다. 새 데코레이터 표준으로 이전하는 문제는 기술적 선택이 아니라 프로덕션 안정성의 문제다.

배경을 정리하자. TypeScript 데코레이터는 두 가지다. 하나는 오래된 `experimentalDecorators` 모드(NestJS, TypeORM, class-transformer가 쓴다), 다른 하나는 TC39에서 표준화된 새 데코레이터(TS 5.0에서 도입). TypeScript 5.0 릴리즈 노트는 명확하게 썼다: "We've decided to make a hard pivot to the new decorators proposal." 새 데코레이터가 공식 방향이다.

**관점 1 — 낙관:** NestJS는 결국 새 데코레이터로 이전한다. 메인테이너들이 그 방향을 인지하고 있고, 시간 문제다. TypeScript 자체가 `experimentalDecorators` 모드를 유지하겠다고 했으니 당장 급박하지 않다.

**관점 2 — 비관:** 문제는 메타데이터 기반 reflection이다. `reflect-metadata` 라이브러리가 새 TC39 데코레이터 표준에 포함되지 않았다. NestJS의 DI 컨테이너는 `reflect-metadata`로 클래스 생성자 파라미터의 타입을 읽어서 주입할 의존성을 결정한다. 이 메커니즘 없이는 DI가 작동하지 않는다. 새 표준 데코레이터로 이전하려면 DI 모델 자체를 재설계해야 한다. 이것은 단순한 마이그레이션이 아니라 프레임워크의 근본을 바꾸는 작업이다.

**공식 입장:** TS는 `experimentalDecorators` 모드를 당분간 유지하겠다고 했다. 즉, NestJS는 지금 당장 breaking change를 강요받지 않는다. 하지만 "당분간"이 얼마나 긴지는 알 수 없다.

**현재 합의:** 신규 프로젝트에서 NestJS를 시작한다면 `experimentalDecorators: true`로 가도 괜찮다. 당장 마이그레이션 계획을 세울 필요는 없지만, NestJS의 공식 이슈 트래커와 로드맵을 팔로우하면서 동향을 주시하는 것이 현명하다.

**남은 공백:** NestJS가 새 데코레이터로 공식 마이그레이션 가이드를 제공하는 시점. 이 책 집필 시점 이후에 상황이 바뀔 수 있으므로, 최신 상태를 반드시 확인하자.

---

### 논쟁 D: `as` vs 타입 가드 vs zod — 어디서 어디까지 검증하는가

타입 단언(`as`)을 쓸 것인가, 타입 가드를 쓸 것인가, zod로 런타임 검증을 할 것인가. 이 질문은 TypeScript를 쓰는 거의 모든 팀에서 한 번씩은 토론이 된다. 팀 컨벤션을 정하지 않으면 코드베이스 내에 세 가지 스타일이 섞여서 일관성이 사라진다.

**관점 1 — `as` 실용주의:** 타입 단언은 개발자가 컴파일러에게 "내가 이 타입을 보장한다"고 말하는 도구다. 책임지고 쓰면 된다. API 응답의 타입을 정확히 아는 상황에서 `response as UserResponse`는 합리적이다. 모든 데이터를 런타임에서 검증하는 것은 과잉이다.

**관점 2 — zod 강경파:** 타입 단언은 컴파일러를 속이는 거짓말이다. `as UserResponse`라고 써도 실제 런타임 데이터가 `UserResponse` 형태인지 보장할 수 없다. API가 스펙을 어기거나, 버전이 바뀌거나, 백엔드 팀이 필드를 추가/삭제하면 런타임 에러가 난다. 외부 입력은 무조건 런타임에서 검증해야 한다.

**관점 3 — boundary validation (사실상 합의):** 이 논쟁에는 실용적 합의가 가장 잘 정착되어 있다. 외부 경계(API 응답, 환경 변수, 폼 입력, 설정 파일, 파일 파싱)에서는 zod나 valibot으로 검증하고, 내부 로직에서는 타입을 신뢰한다. Theo, Colin McDonnell(zod 저자) 등이 정착시킨 이 패턴이 커뮤니티 표준이다.

구체적으로 보면 이렇다.

```typescript
import { z } from 'zod';

const UserResponseSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  role: z.enum(['admin', 'user']),
});

type UserResponse = z.infer<typeof UserResponseSchema>;

// API 경계에서 검증
async function fetchUser(id: string): Promise<UserResponse> {
  const raw = await api.get(`/users/${id}`);
  return UserResponseSchema.parse(raw); // 실패 시 ZodError
}

// 내부에서는 타입 신뢰
function formatUserName(user: UserResponse): string {
  // user는 검증된 데이터 — 여기서 as를 쓸 필요 없다
  return `${user.email} (${user.role})`;
}
```

경계에서 한 번 검증하면 내부에서는 타입을 믿을 수 있다. `as`로 경계를 넘기는 것은 "내가 검증한다"는 책임 선언이다. zod로 검증하는 것은 "런타임에서도 확인한다"는 실행이다. 팀의 패턴을 명확히 정해두면 논쟁이 줄어든다.

**남은 공백:** zod의 번들 크기(약 14kb gzipped)가 프론트엔드에서 부담이 될 수 있다. valibot(더 가볍다), arktype(TS 타입과 더 강하게 통합) 같은 경량 대안이 성숙하는 속도를 지켜봐야 한다.

이 논쟁에서 Java/Kotlin 개발자에게 특히 흥미로운 관점이 있다. Spring의 `@Valid`와 Bean Validation(`@NotNull`, `@Email`, `@Size`)이 하는 역할을 TypeScript에서는 zod가 한다고 볼 수 있다. Spring에서 `@RequestBody`에 `@Valid`를 붙이면 컨트롤러에 도달하기 전에 검증이 이루어진다. TypeScript/NestJS에서는 `ValidationPipe`와 `class-validator` 데코레이터가 비슷한 역할을 한다. 그런데 `class-validator`는 데코레이터 기반이라 `experimentalDecorators`가 필요하고, 클래스를 써야 한다. zod는 클래스 없이 스키마 객체로 동작한다. NestJS 팀 내에서도 `class-validator` vs zod가 논쟁 주제가 되는 이유다. 기존 Spring 스타일에 익숙하다면 `class-validator`가 편하고, 함수형 스타일을 선호한다면 zod가 더 자연스럽다. 어느 쪽이 "옳다"가 아니라 팀의 코딩 스타일과 정렬이 관건이다.

---

### 논쟁 E: monorepo의 적정 규모는 어디인가

**관점 1 — monorepo first:** 팀이 하나여도 monorepo가 낫다. 코드 공유, refactor 추적, atomic commit, 일관된 린트/테스트 설정이 훨씬 쉽다. "내가 공유 라이브러리를 수정했는데 그게 어느 앱에 영향 미치는지"를 monorepo 내에서 즉시 알 수 있다.

**관점 2 — polyrepo first:** 소규모 팀에서 Turborepo, Nx, pnpm workspace를 설정하고 관리하는 것은 과한 도구다. 필요성을 느끼기 전에 monorepo를 도입하면 설정 복잡도만 늘어난다. polyrepo로 시작했다가 필요할 때 합치는 것이 낫다.

**도구 스펙트럼:** 세 가지 주요 도구가 스펙트럼을 이룬다.

- **pnpm workspace:** 가장 가볍다. 의존성 호이스팅 최적화, symlink 기반 패키지 공유. 도구 자체의 설정이 단순하다.
- **Turborepo:** 빌드 캐싱과 원격 캐시(Remote Cache)가 핵심 기능이다. 대규모 monorepo에서 빌드 시간을 극적으로 줄인다.
- **Nx:** 가장 풍부한 generator와 plugin 생태계. 의존성 그래프 시각화, 영향 분석, 커스텀 task 등 기능이 많다. 그만큼 학습 곡선도 있다.

**현재 합의:** 프로젝트 초기에는 pnpm workspace로 가볍게 시작하고, 빌드 속도가 병목이 되면 Turborepo를 추가하는 것이 실용적인 경로다. Nx는 팀이 충분히 크고 generator가 실질적으로 필요할 때 도입하는 편이 낫다. 한국에서는 카카오, 당근, 토스의 monorepo 사례가 표준 레퍼런스다.

**남은 공백:** monorepo 도입이 팀의 CI/CD 파이프라인, 특히 PR 단위 배포 전략에 미치는 영향. "어느 패키지가 바뀌었을 때 어느 앱만 재배포한다"는 판단을 자동화하는 것이 실제 운영에서 가장 어렵다.

---

### 논쟁 F: 풀스택 메타프레임워크의 부상 — 모바일이 있는 회사는 어떻게 하는가

Next.js App Router의 Server Components와 Server Actions, React Router 7, SvelteKit, Solid Start가 "프론트가 백엔드를 흡수한다"는 시나리오를 현실로 만들고 있다. BFF(Backend for Frontend)가 Server Actions로 대체되고, API 레이어가 사라지는 구조다.

**관점 1 — 풀스택 옹호:** 타입이 서버와 클라이언트를 관통한다. 서버에서 데이터를 가져오는 코드와 클라이언트에서 렌더링하는 코드가 같은 타입 시스템 아래에 있다. BFF를 별도로 운영할 필요가 없다. 개발 속도가 올라가고, 타입 불일치 버그가 줄어든다.

**관점 2 — 분리 유지:** 모바일 앱, 데스크톱 클라이언트, 다른 웹 서비스 등 다중 소비자 환경에서 API는 별도여야 한다. Next.js 풀스택은 "웹만 있는 서비스"를 위한 해법이다. iOS, Android 앱이 동시에 있는 회사에서 Server Actions로 API를 대체하면 모바일 팀이 소비할 방법이 없다.

**관점 3 — server-first 반동:** SPA(Single Page Application)가 과잉 적용됐다는 반성이 있다. Astro의 Islands 아키텍처, HTMX의 서버 사이드 렌더링 부활이 또 다른 방향이다. "자바스크립트를 최소화하자"는 움직임이 server-first 진영을 만들었다.

**한국 현장:** Spring + REST API + React/Vue가 여전히 표준이다. Next.js 풀스택은 신생 스타트업과 핀테크에 한정되고, 모바일 앱을 운영하는 회사라면 REST API를 유지하는 편이 현실적이다. 토스, 당근, 쿠팡이츠처럼 모바일과 웹이 함께 있는 서비스에서는 Server Actions가 API를 완전히 대체하기 어렵다.

**남은 공백:** tRPC, GraphQL 같은 타입-안전 API 레이어가 "풀스택으로 이전하지 않고도 서버-클라이언트 간 타입 안전성을 보장하는" 방향으로 성숙하고 있다. 이 방향이 한국 현장에서 얼마나 빠르게 채택될지.

---

### 논쟁 G: TypeScript 컴파일러는 어디로 가는가 — TS Native, Node strip-types, Bun

이것은 개발 경험(Developer Experience)의 미래에 관한 논쟁이다. 8장에서 현재의 도구 풍경을 다뤘다면, 여기서는 방향을 본다.

**현재의 문제:** `tsc`는 TypeScript로 작성되어 있어 대규모 코드베이스에서 느리다. 대안인 esbuild와 swc는 타입 체크를 수행하지 않는다. 빠른 트랜스파일과 엄밀한 타입 체크 중에서 하나를 선택해야 하는 상황이 지속됐다. 현재 많은 프로젝트가 "빌드는 esbuild/swc로 빠르게, 타입 체크는 tsc로 별도 실행"하는 두 단계 방식을 쓴다.

**관점 1 — TypeScript Native(Go 재작성):** Microsoft가 2025년 발표한 Go로 재작성한 TypeScript 컴파일러가 게임 체인저다. 목표는 10배 이상의 성능 향상이다. 빠른 빌드와 엄밀한 타입 체크를 동시에 얻을 수 있다면, 두 단계 빌드의 필요성이 사라진다. Go는 병렬 처리와 메모리 효율에서 TypeScript/JavaScript보다 유리하다.

**관점 2 — Node.js `--experimental-strip-types`:** Node.js 자체가 TypeScript를 직접 실행하는 방향이다. Node 22에서 `--experimental-strip-types` 플래그로 TS 파일을 실행할 수 있게 됐다. 타입 주석을 제거(strip)하고 JS로 실행하는 방식이라 타입 체크는 수행하지 않는다. 하지만 빌드 단계 없이 `node index.ts`로 실행할 수 있다는 것만으로 개발 경험이 달라진다.

**관점 3 — Bun의 네이티브 실행:** Bun은 처음부터 TypeScript를 직접 실행하는 런타임이다. `bun run file.ts`가 바로 된다. 타입 체크는 별도로 해야 하지만, 런타임이 TS를 1급 시민으로 취급한다는 점에서 개발 흐름이 단순해진다.

**현재 합의:** 세 방향이 동시에 진행 중이다. TS Native가 GA(General Availability)되면 `tsc`의 속도 문제는 해결된다. Node의 `strip-types`는 타입 체크를 포기하는 대신 빌드 단계를 없앤다. Bun은 개발 환경에서는 이미 충분히 쓸 만하다. 어느 방향이 주류가 될지는 각 방향이 프로덕션 안정성을 어떻게 증명하느냐에 달려 있다.

**남은 공백:** TypeScript Native가 언제 안정 버전으로 출시되는가, 기존 `tsc` 기반 설정이 자동으로 호환되는가. 이 질문에 대한 답이 나오면 생태계 전체의 빌드 설정이 크게 단순해질 것이다.

**한국 현장 시각:** 논쟁 G는 한국 개발자에게 조금 다른 무게감을 갖는다. 한국의 대형 서비스들은 빌드 시간이 개발 생산성에 미치는 영향을 이미 체감하고 있다. 토스, 카카오, 우아한형제들처럼 수백 개의 패키지로 이루어진 monorepo를 운영하는 팀에서 `tsc`의 느린 빌드는 매일 마주치는 실용적 문제다. TypeScript Native가 실제로 10배 빠르다면, 이 팀들의 CI/CD 파이프라인 시간이 크게 줄어든다. 단순한 언어 구현 이야기가 아니라, 수십 명의 개발자가 매일 기다리는 시간의 합산이다. 그래서 이 논쟁이 한국 테크 블로그에서 유독 관심을 받는다.

---

## AI 시대의 TypeScript — 사람이 서야 할 자리

Claude, GitHub Copilot, Cursor가 TypeScript 코드를 작성하는 것이 일상이 됐다. 코드 한 페이지를 1초도 안 되어 생성하고, 함수 시그니처를 보고 구현을 완성하고, 에러 메시지를 붙여넣으면 원인과 수정 방향을 설명한다. 이 사실은 두 가지 질문을 동시에 던진다.

"왜 AI는 TypeScript 코드를 비교적 잘 생성하는가?" 그리고 "AI가 잘못 가는 자리는 어디인가?"

이 절을 쓰는 이유는 단순히 "AI가 TS를 잘 짜니까 안 배워도 된다"고 결론 내리려는 게 아니다. 정반대다. AI가 TS 코드를 생성하는 방식의 구조적 이유를 이해하면, 어디에서 AI를 믿고 어디에서 검토를 강화해야 하는지가 분명해진다. TypeScript를 깊이 이해한 사람만이 AI가 생성한 TS 코드의 품질을 정확하게 판단할 수 있다. 역설적으로 AI 시대에 "언어를 제대로 아는 것"의 가치가 더 높아졌다.

---

### 왜 AI는 TypeScript를 비교적 잘 다루는가

TypeScript가 AI에게 친화적인 이유는 구조에 있다.

**첫째, 타입이 컨텍스트를 제공한다.** 함수 시그니처에 다음과 같이 써 있다면:

```typescript
async function processPayment(
  userId: UserId,
  amount: Money,
  currency: Currency,
): Promise<Result<PaymentReceipt, PaymentError>>
```

AI는 이 함수가 무엇을 받고 무엇을 돌려줘야 하는지를 타입에서 직접 읽는다. `UserId`, `Money`, `Currency`가 branded type이라면 도메인 의미론도 읽힌다. `Result<T, E>` 패턴이 있다면 성공과 실패를 명시적으로 다뤄야 한다는 것도 안다. 타입이 상세할수록 AI가 생성하는 구현의 품질이 올라간다.

Java의 타입도 비슷한 역할을 하지만, TypeScript의 구조적 타입 시스템과 유틸리티 타입은 함수 시그니처에 더 많은 정보를 담는다. discriminated union, conditional type, mapped type이 그 자체로 "어떤 형태의 데이터를 어떻게 다루는가"를 AI에게 알려주는 명세가 된다.

**둘째, 생태계 패턴이 명확하다.** zod 스키마, React 컴포넌트의 props 타입, NestJS 모듈 구조, Express 미들웨어 시그니처 — 이 패턴들이 학습 데이터에 충분하게 있어서 AI는 "여기에 뭐가 들어가야 한다"를 높은 확률로 맞춘다. 특히 TypeScript의 패턴은 자주 반복되고, 구조가 예측 가능하다. 구조적 타입 시스템의 예측 가능성이 AI의 코드 생성과 잘 맞는다.

**셋째, 컴파일러가 즉각적인 피드백을 준다.** AI가 생성한 코드가 타입 체크를 통과하지 못하면, 에러 메시지를 AI에게 다시 넣어서 수정을 요청하는 루프가 자연스럽게 돌아간다. 자기 교정 루프(self-correction loop)가 작동하기 좋은 환경이다. 타입 에러가 없는 코드를 만드는 데 AI가 꽤 효과적인 이유 중 하나다.

---

### AI가 잘못 가는 자리

그러나 AI도 틀린다. 그것도 특정 패턴으로 반복해서 틀린다. 이 패턴을 알아두면 리뷰할 때 집중해야 할 곳이 보인다.

**`any`로의 도주:** 타입 추론이 복잡해지거나, 제네릭 조합이 어려워지거나, 서드파티 라이브러리의 타입 정의가 불완전할 때, AI는 `any`를 선택하는 경향이 있다. "일단 동작하게 만드는 것"이 목표라면 `any`가 가장 쉬운 탈출구다. 그런데 이 코드가 코드베이스에 들어오면 타입 안전성의 균열이 시작된다.

AI에게 명시적으로 "any는 사용하지 말 것"을 요청하는 것도 하나의 방법이다. 또는 코드 리뷰에서 `any`의 존재를 먼저 확인하는 습관을 들이는 편이 낫다. ESLint의 `@typescript-eslint/no-explicit-any` 규칙으로 자동 검출도 가능하다.

**branded type 무시:** AI는 `UserId`와 `OrderId`가 둘 다 `string`이라면 그냥 `string`으로 통일하는 경향이 있다. 도메인 모델의 의미론적 구분을 유지하는 것은 사람의 판단이 필요한 영역이다. AI에게 "UserId는 branded type을 써줘"라고 명시하지 않으면, 구조적으로 동등한 타입을 뭉개버리는 코드를 받게 된다.

**외부 데이터 검증 누락:** API 응답을 받아서 TS 타입으로 처리하는 코드를 AI가 생성할 때, 런타임 검증 없이 `as` 단언만 붙이는 경우가 많다. boundary validation 패턴을 명시하지 않으면 AI는 실용주의적 지름길을 택한다. "API 응답은 zod로 검증한 뒤 사용할 것"을 명시하면 훨씬 나은 코드가 나온다.

**tsconfig 옵션의 가정:** AI는 종종 `strict: true`가 켜진 환경을 가정하지 않거나, 반대로 현재 프로젝트에 없는 엄격한 옵션을 가정한다. 생성된 코드가 현재 프로젝트의 tsconfig와 어긋나는 경우가 생긴다. "이 프로젝트의 tsconfig는 X를 켜고 있다"는 컨텍스트를 제공하면 정확도가 올라간다.

**에러 경로의 단순화:** AI는 성공 경로를 먼저 작성하고 에러 경로를 단순화하는 경향이 있다. Promise의 rejection이 모두 처리되는지, null/undefined 케이스가 빠짐없이 다뤄지는지를 검토해야 한다. 특히 `noUncheckedIndexedAccess: true`가 켜진 환경에서 AI가 생성한 배열 접근 코드는 `undefined` 가능성을 무시하는 경우가 많다.

---

### zod 스키마를 프롬프트의 일부로 쓰는 패턴

실무에서 AI 코드 생성의 품질을 높이는 패턴 하나를 소개하자. AI에게 코드 생성을 요청할 때, zod 스키마를 프롬프트에 포함시키면 타입의 경계를 더 명확히 이해한다.

```typescript
// 프롬프트에 이 스키마를 포함한다
const UserSchema = z.object({
  id: z.string().brand<'UserId'>(),
  email: z.string().email(),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.date(),
  profile: z.object({
    name: z.string().min(1),
    bio: z.string().nullable(),
  }),
});

type User = z.infer<typeof UserSchema>;
```

이 스키마를 컨텍스트로 제공하면, AI는 `User` 타입의 제약 조건(branded id, email 형식, 제한된 role 값, Date 타입, nullable bio)을 프롬프트에서 직접 읽는다. "User를 받아서 처리하는 서비스 메서드를 구현해줘"라는 요청에 훨씬 정확한 코드가 나온다. 스키마가 없을 때보다 `bio`의 nullable 처리, `role`에 따른 분기, `createdAt`의 날짜 포맷 처리를 더 정확하게 다룬다.

이 패턴의 확장으로, 현재 프로젝트의 타입 정의 파일을 프롬프트에 첨부하는 것도 효과적이다. AI가 "이미 있는 타입과 어떻게 통합되는가"를 이해한 채로 코드를 생성한다.

---

### AI에게 tsconfig 컨텍스트를 명시하는 휴리스틱

AI에게 코드 생성을 요청할 때 프롬프트에 다음을 포함하면 생성 코드의 품질이 올라간다.

```
이 프로젝트의 tsconfig 설정:
- strict: true (strictNullChecks, strictFunctionTypes, strictBindCallApply 포함)
- noUncheckedIndexedAccess: true (배열/객체 인덱스 접근 시 T | undefined)
- exactOptionalPropertyTypes: true (옵셔널 속성에 명시적 undefined 금지)
- noImplicitReturns: true (모든 코드 경로가 반환값을 가져야 함)

코딩 컨벤션:
- any 사용 금지
- 외부 데이터(API 응답, env, 폼)는 zod로 검증
- 내부 로직에서 타입 단언(as)은 최소화
- async 함수 호출 시 항상 await 또는 void 명시
```

이 정도의 컨텍스트를 주면, AI는 `arr[0]`의 결과가 `T | undefined`임을 인지하고, 옵셔널 속성에 `undefined`를 명시적으로 쓰지 않으며, `any` 대신 타입 가드나 조건부 타입을 선택하고, `async` 함수 호출에 `await`를 붙인다.

단, 이 컨텍스트를 매번 직접 입력하는 것은 번거롭다. Cursor의 `.cursorrules` 파일, 또는 팀의 코딩 어시스턴트 설정에 이 내용을 템플릿화해두면 자동으로 포함된다.

---

### AI 시대에 사람이 검토해야 할 자리

AI 코드 생성을 활용하는 팀에서 코드 리뷰의 성격이 바뀐다. "이 코드를 어떻게 더 낫게 쓸까"보다 "이 코드가 안전한가"를 먼저 확인하는 방향으로 무게가 이동한다. TypeScript 코드에서 AI가 생성한 부분을 리뷰할 때 집중해야 할 항목들을 정리해두자.

**타입 경계의 무결성:** 외부 입력이 들어오는 지점에 런타임 검증이 있는가. `as`로 때우고 있는가, zod 파싱이 있는가. API 엔드포인트, 환경 변수 파싱, 폼 제출 핸들러, 파일 읽기가 특히 주의 대상이다.

**`any`의 존재와 정당성:** `any`가 있다면 그것이 불가피한 위치인가, 아니면 AI가 포기해서 쓴 것인가. `any`가 있다면 왜 있는지 주석이 있는가. ESLint `@typescript-eslint/no-explicit-any`로 자동 검출한다.

**도메인 의미론의 보존:** branded type이 제거되거나 희석되지 않았는가. `UserId`와 `OrderId`가 그냥 `string`으로 통일됐는가. 도메인 언어가 타입에 그대로 반영됐는가.

**에러 경로의 완결성:** `async` 함수의 rejection이 모두 처리되는가. Promise가 `await` 없이 floating되지 않는가. try/catch에서 에러 타입이 `unknown`으로 올바르게 처리되는가.

**엣지 케이스 커버리지:** AI가 짠 코드에는 엣지 케이스 테스트가 빠지는 경향이 있다. `null`, `undefined`, 빈 배열, 음수 값, 매우 긴 문자열, 특수 문자를 포함한 테스트가 있는가.

**tsconfig 정합성:** 현재 프로젝트 tsconfig에서 에러가 나지 않는가. 특히 `noUncheckedIndexedAccess`가 켜진 환경에서 배열 접근이 올바르게 처리됐는가.

AI는 코드를 빠르게 생성하는 강력한 도구다. 하지만 도구는 사용자의 판단을 대체하지 않는다. TypeScript를 깊이 이해한 사람만이 AI가 생성한 TS 코드의 품질을 판단할 수 있다. 이 책을 읽는 이유가 여기에 있다.

Java/Kotlin 개발자에게 AI 코드 검토에서 특히 주의해야 할 패턴이 하나 더 있다. AI는 종종 Java/Spring 스타일의 코드를 TypeScript로 직역한다. 클래스 기반 설계, 서비스-리포지터리 레이어 분리, 인터페이스와 구현 클래스 분리 등이다. 이 패턴들이 TypeScript에서 반드시 나쁜 것은 아니지만, TypeScript 생태계가 더 자연스럽게 다루는 방식과 다를 수 있다. 특히 함수형 패턴과 클로저가 TypeScript에서는 클래스보다 더 간결하게 같은 역할을 하는 경우가 많다. AI가 "Java 스타일"로 TypeScript를 짜고 있다면, "이게 TypeScript다운 방식인가"를 한 번 더 물어보자.

---

## 학습 자원 지도 — 다음으로 가는 길

책을 덮은 다음, 어디로 더 깊이 들어갈 수 있는가. 신뢰할 수 있는 자원들을 정리해두자. 유행처럼 나왔다 사라지는 블로그 글이 아니라, 시간이 지나도 가치가 있는 1차 자원들이다.

---

### 한국어 자원

**velopert(김민준) — TypeScript Handbook 한국어판**

TypeScript 공식 핸드북의 한국어 번역과 함께, 개인 velog에 실무 중심의 글을 꾸준히 올린다. 입문 이후 기초를 다시 점검하기 좋다. 한국어로 TypeScript를 처음 배우는 개발자 대부분이 이 자료로 시작한다. `https://typescript-kr.github.io/`

**토스 기술블로그 — JavaScript에서 TypeScript로 바꾸기 시리즈**

토스의 실제 마이그레이션 경험을 담았다. 수만 줄의 실제 코드베이스를 어떻게 전환했는지, 어떤 판단을 했는지를 솔직하게 썼다. "이론은 알겠는데 실제로는 어떻게 하는 거지?"라는 질문에 답한다. `https://toss.tech/`

**카카오 기술블로그 — TypeScript Monorepo with pnpm**

pnpm workspace 기반 monorepo 구성의 실무 레퍼런스다. `tsconfig.references` 설정, 패키지 간 의존성 관리, IDE 성능 유지 방법이 구체적으로 나와 있다. monorepo를 도입하려는 팀이라면 반드시 읽어야 한다. `https://tech.kakao.com/`

**당근 기술블로그 — 한 모노레포에서 1000명이 일하는 법**

대규모 monorepo 운영 경험이 담겼다. 팀이 커지면서 생기는 빌드 전략, 패키지 경계 설계, IDE 성능 관리의 실제 판단들이 실용적이다.

**이펙티브 타입스크립트 (Dan Vanderkam 저, 인사이트 번역)**

"어떻게 쓰는가"보다 "왜 이렇게 작동하는가"를 설명하는 책이다. 타입 시스템의 원리, 실무에서 자주 만나는 오류의 근원, 더 나은 타입 설계를 위한 구체적 아이템들이 담겼다. 타입을 어떻게 써야 할지 막막할 때 펼치면 방향이 잡힌다. 한국어로 구할 수 있는 TypeScript 깊이 있는 책 중 현재 최선의 선택이다.

---

### 영어 자원

**Total TypeScript — Matt Pocock**

실무 중심의 TypeScript 심화 학습 플랫폼이다. tsconfig cheat sheet, 제네릭 패턴, conditional type과 infer의 실용 예제, branded type 활용, 타입 좁히기 심화가 체계적으로 정리돼 있다. 무료 콘텐츠만으로도 상당한 깊이를 커버한다. `https://www.totaltypescript.com/`

**Effective TypeScript (2nd ed., 2024) — Dan Vanderkam**

한국어판의 원본이다. 2판에서 최신 TS 기능이 대거 추가됐다. 한국어판이 1판 기준이라면 원서 2판을 함께 보는 편이 낫다. 특히 Item 38~44에서 타입 좁히기, 조건부 타입, infer를 다루는 방식이 깊다.

**Programming TypeScript — Boris Cherny**

타입 시스템을 바닥부터 쌓아 올리는 구성이다. 타입 추론의 알고리즘, 공변성과 반변성의 원리, 클래스와 타입의 관계를 이론적으로 설명한다. "왜 이 제네릭이 이렇게 작동하는가"를 이해하고 싶다면 이 책이다.

**Type-Level TypeScript**

타입 수준 프로그래밍을 다룬다. 타입 자체를 계산하는 기법 — conditional type, infer, 재귀 타입, mapped type의 고급 활용 — 을 체계적으로 배운다. TypeScript의 타입 시스템이 일종의 프로그래밍 언어라는 사실을 실감하게 된다. `https://type-level-typescript.com/`

---

### 다음 책·다음 주제

**Effective TypeScript → Type-Level TypeScript → Programming TypeScript** 순서가 실용적인 심화 경로다. 이펙티브 TS로 원리를 잡고, Type-Level TS로 타입 연산을 익히고, Programming TS로 이론적 배경을 완성하는 흐름이다.

**RxJS 깊이:** 반응형 프로그래밍 패러다임이 TypeScript와 만나는 지점이다. 이벤트 스트림, 옵저버블 패턴, 연산자 파이프라인을 타입-안전하게 다루는 방법은 별도의 학습이 필요하다. Angular를 쓰는 팀이라면 사실상 필수다.

**NestJS 깊이:** DI 원리, interceptor, guard, middleware의 동작 방식, TypeORM 또는 Prisma와의 통합, 새 데코레이터 마이그레이션 동향. NestJS를 프로덕션에서 운영한다면 공식 문서와 이슈 트래커를 직접 파야 한다. `https://docs.nestjs.com/`

**TypeScript 컴파일러 API:** TS 컴파일러를 도구로 사용하는 방법이다. codemod 작성, 커스텀 lint 규칙, 코드 생성 도구를 만들 때 필요하다. 네이버 D2의 컴파일러 API 활용 사례가 한국어 레퍼런스다. `https://d2.naver.com/`

**zod/valibot 생태계:** 런타임 검증 라이브러리가 빠르게 발전하고 있다. zod v4의 API 개선, valibot의 경량 설계, arktype의 TS 타입 통합 방식 차이를 이해하면 boundary validation 전략을 팀 맥락에 맞게 선택할 수 있다.

**Prisma와 타입-안전 ORM:** TypeORM과 달리 Prisma는 스키마에서 타입을 생성한다. 데이터베이스 스키마와 TypeScript 타입이 하나의 소스에서 나오는 방식은 Spring의 JPA와 크게 다르다. 이 차이를 이해하면 백엔드 TypeScript 개발의 타입 안전성 전략이 달라진다.

**tRPC와 타입-안전 API:** REST API를 설계할 때 백엔드가 OpenAPI 스펙을 작성하고 프론트가 그것을 기반으로 클라이언트를 생성하는 방식이 있다. tRPC는 이 워크플로를 없애고, 백엔드 라우터의 타입을 직접 프론트엔드에서 임포트해 사용한다. 서버-클라이언트 간 타입 불일치 버그가 구조적으로 불가능해진다. REST API가 필요한 환경(모바일, 외부 파트너)과 함께 사용하기 어렵다는 제약이 있지만, 웹 전용 풀스택 프로젝트에서는 생산성이 크게 오른다. Spring의 Feign Client가 API 스펙을 공유하는 방식과 철학은 비슷하지만 구현 방식은 완전히 다르다.

---

> **📖 더 깊이 가려면**
>
> 이 책에서 함정의 큰 지형을 그렸다면, 각 함정의 세부 지형은 따로 찾아볼 수 있다.
>
> **→ 부록 D에서 한국 개발자 함정 사전 12개 상세를 다룬다.** 각 함정마다 증상, 원인, 처방을 정리하고, 본문에서 더 깊이 다룬 챕터와 페이지를 안내한다.
>
> - *이펙티브 타입스크립트* Item 7(타입이 값들의 집합이라고 생각하기), Item 38(타입 좁히기), Item 45(any 사용은 최소화하기)는 이 챕터에서 다룬 함정의 이론적 배경을 제공한다.
>
> - *Total TypeScript*의 "Solving TypeScript Errors" 섹션은 실무에서 막히는 타입 에러 패턴별 해결책을 다룬다.
>
> - NestJS 새 데코레이터 마이그레이션 동향은 `https://github.com/nestjs/nest` 이슈 트래커에서 실시간으로 확인하자. 이 책 집필 이후 상황이 달라질 수 있다.

---

## 마무리 — 도구의 경계를 아는 것이 도구를 잘 쓰는 것이다

책 한 권이 끝났다. 1장에서 15장까지, TypeScript가 왜 이렇게 생겼는지를 Java/Kotlin 개발자의 시선으로 해체하고 재조립했다.

걸어온 길을 한번 돌아보자.

TypeScript의 타입은 컴파일 타임에만 존재한다. 런타임에서 타입은 사라진다. 이 사실이 이 책의 출발점이었다. Java나 Kotlin의 타입은 런타임 객체에 붙어 있다. 리플렉션으로 `getClass()`를 호출하면 타입 정보가 나온다. TypeScript는 다르다. 컴파일되면 타입 정보는 증발한다. 남는 것은 JS 값뿐이다. 이 차이를 이해하면 "타입이 있는데 왜 런타임 에러가 나는가"의 답이 보인다.

구조적 타입 시스템이 명목적 타입 시스템과 어떻게 다른지, 그 차이가 실무에서 어디서 틈새를 만드는지를 봤다. Java에서 `UserId`와 `OrderId`가 다른 클래스이기 때문에 컴파일러가 혼동을 막아주는 것이 당연하게 느껴졌다면, TypeScript에서 그 기대가 배반당하는 순간이 온다. branded type 패턴이 그 배반을 막는 방어다.

비동기의 에러가 어디로 사라지는지, `async/await`이 Java의 `CompletableFuture`와 무엇이 같고 무엇이 다른지를 살폈다. Java의 checked exception이 불편하다고 느꼈다면, TypeScript에서 `await`를 빠뜨려 에러가 공중에 뜨는 경험을 하고 나면 생각이 달라진다. 명시적 강제와 묵시적 자유 사이의 트레이드오프를 다시 생각하게 된다.

모듈 시스템의 역사적 혼란이 왜 생겼고, 2025년 현재 어느 방향으로 정착하는지를 추적했다. CommonJS와 ESM의 공존은 당분간 계속된다. 그 혼란을 피하는 가장 좋은 방법은 프로젝트 초기에 모듈 방식을 명확히 결정하고 tsconfig를 정렬하는 것이다.

데코레이터가 두 종류로 갈라진 이유와 그 갈림길이 NestJS에 어떤 긴장을 만드는지를 봤다. Spring의 `@Autowired`와 NestJS의 `@Injectable()`이 비슷해 보이지만 메커니즘이 다르다는 것, 그 메커니즘이 새 데코레이터 표준으로 이전할 때 왜 문제가 되는지를 이해했다.

React의 타입 철학이 Vue, Svelte, Solid와 어떻게 다른지, 그 차이가 컴포넌트 설계에서 어떻게 나타나는지를 비교했다. 한국 시장에서 React가 압도적이라는 현실을 인정하면서도, 다른 프레임워크를 만날 때 "이 프레임워크의 reactivity 모델은 어디가 다른가"를 볼 수 있는 눈을 만들려 했다.

풀스택의 경계가 어디까지 확장됐고, 한국 현장에서 그 경계가 어디 있는지를 짚었다. Spring + REST + React가 여전히 표준인 한국 시장에서 Next.js 풀스택이나 tRPC가 어떤 의미를 갖는지를 실용적으로 봤다.

14장에서 테스트 전략을 다뤘다. TypeScript 코드를 테스트하는 것이 Java와 어떻게 다른지, `vitest`와 `jest`의 차이, 타입 수준에서 테스트하는 `tsd`와 `expect-type`의 역할, 그리고 모킹(mocking)이 Java의 Mockito와 어떻게 닮고 어떻게 다른지를 살폈다. 특히 TypeScript에서 인터페이스가 런타임에 존재하지 않기 때문에 Mockito 스타일의 `mock(SomeInterface.class)` 패턴을 그대로 쓸 수 없다는 점, 대신 구조적 타입의 특성을 활용해 테스트용 객체를 훨씬 간단히 만들 수 있다는 점이 핵심 차이였다.

그리고 이 마지막 장에서 함정의 지형을 그리고, 논쟁의 위치를 표시하고, AI 시대의 역할을 생각했다.

---

### TypeScript를 잘 쓴다는 것이 무엇인가

책을 닫기 전에 이 질문을 한 번 더 생각해보자. "TypeScript를 잘 쓴다"는 것이 무엇을 의미하는가.

타입 에러가 하나도 없는 코드를 짜는 것인가? 아니다. `as any`를 모든 곳에 쓰면 에러가 없어지지만, 그것은 타입 체커를 속인 것이다. `strict: true` 아래에서 타입 에러 없이 코드를 짜는 것인가? 가깝지만 아직 충분하지 않다. 컴파일 타임 오류가 없어도 런타임 버그는 얼마든지 있을 수 있다.

TypeScript를 잘 쓴다는 것은 타입 시스템과 협력하는 법을 안다는 것이다. 다시 말해 두 가지를 동시에 안다는 뜻이다.

**타입 시스템이 보장해주는 것:** 컴파일 타임에 선언된 타입이 일치하는 것. 함수가 선언된 인자 타입을 받고 선언된 반환 타입을 돌려주는 것. 구조적으로 호환되지 않는 값을 넣으면 컴파일러가 잡아주는 것.

**타입 시스템이 보장해주지 않는 것:** 런타임에 외부에서 들어온 데이터가 선언된 타입과 실제로 일치하는 것. `as` 단언이 진실인 것. 모든 `async` 에러가 잡히는 것. `null` 병합 연산자 없이 객체 속성에 안전하게 접근하는 것.

이 두 가지 경계를 안다면, 타입 시스템이 보장해주는 영역에서는 컴파일러를 믿고, 보장해주지 않는 영역에서는 런타임 검증과 방어적 코딩으로 직접 채운다. 이 판단을 자연스럽게 하는 사람이 TypeScript를 잘 쓰는 사람이다.

Java/Kotlin에서 건너온 개발자에게 이 경계를 이해하는 것이 특히 중요하다. Java는 런타임에도 타입 정보가 살아 있다. 클래스 계층, 인터페이스 구현, 리플렉션이 모두 런타임에서 타입 기반으로 동작한다. TypeScript는 다르다. 컴파일 타임에 타입을 검사하고, 런타임에서는 타입이 없다. 이 차이를 몸에 새기는 것이 TypeScript를 진짜 이해하는 것이다.

흥미로운 역설이 있다. TypeScript를 잘 이해할수록 타입을 덜 쓰게 된다. 필요한 곳에만, 적절한 방식으로 타입을 쓴다. 모든 변수에 타입을 명시하는 것이 아니라, 타입 추론이 충분한 곳에서는 추론에 맡기고, 추론이 틀릴 가능성이 있는 경계에서만 명시한다. "타입을 많이 쓸수록 TypeScript를 잘 쓰는 것"이라는 오해가 있는데, 정반대다. 필요한 곳에 정확하게 쓰는 것이 잘 쓰는 것이다.

이 감각이 쌓이는 데는 시간이 필요하다. 코드를 짜고, 타입 에러를 만나고, 원인을 추적하고, 더 나은 방법을 찾는 과정이 반복되면서 쌓인다. 이 책이 그 과정을 조금 더 빠르게, 조금 덜 고통스럽게 만들었으면 하는 것이 저자의 바람이다.

---

지금 이 책을 읽고 있는 당신이 어떤 상황에 있든, 한 가지는 분명하다. TypeScript를 배우기로 결심하는 것은 기술 스택 하나를 추가하는 일이 아니다. 타입 시스템을 다르게 생각하기로 결심하는 일이다. Java/Kotlin의 명목적 타입에서 TypeScript의 구조적 타입으로 세계관을 확장하는 일이다. 컴파일 타임 안전성이 런타임까지 보장하지 않는다는 사실을 받아들이고, 그 간격을 어떻게 채울지를 설계하는 일이다.

이 전환이 처음에는 낯설다. 당연하다. 10년 넘게 Java나 Kotlin으로 사고하던 사람이 TypeScript의 구조적 타입을 처음 만나면 "이게 왜 이렇게 동작하지?"를 여러 번 되묻는다. 그 질문이 멈추는 순간이 TypeScript가 자기 것이 되는 순간이다.

그 순간이 오면, 이 책을 다시 한번 펼쳐보자. 처음 읽을 때와 다른 것이 보일 것이다.

---

AI가 코드를 써주는 시대에 역설적으로 "언어의 원리를 이해하는 것"의 가치가 올라간다. AI가 `any`를 쓴 이유를 이해하려면 `any`가 무엇인지 알아야 한다. AI가 branded type을 뭉갠 이유를 알아채려면 구조적 타입이 무엇인지 알아야 한다. AI가 생성한 `async` 함수에서 rejection이 처리됐는지 판단하려면 비동기 에러의 전파 방식을 알아야 한다.

원리를 모르면 AI가 틀렸을 때 틀린 줄 모른다. 원리를 알면 AI가 만든 코드를 더 빠르게, 더 정확하게 검토할 수 있다. AI는 생산성 도구다. 하지만 그 도구를 제대로 쓰려면 당신이 TypeScript를 제대로 알아야 한다.

---

> **저자의 마지막 한 마디**
>
> TS는 도구다. 도구의 경계를 안다는 것이 도구를 잘 쓴다는 뜻이다. 그 경계가 AI 시대에도 변하지 않는다.
>
> TypeScript의 타입은 컴파일 타임에만 있다. 런타임에서 외부에서 들어오는 데이터는 타입 시스템 밖에서 온다. 이 경계를 아는 사람이 `any`를 언제 쓰면 안 되는지 알고, 경계에서 검증해야 하는 이유를 알고, AI가 생성한 코드에서 무엇을 봐야 하는지 안다.
>
> 책을 덮고, 지금 당장 코드를 한 줄 써보자. `strict: true`를 켜고, `any`를 하나 지우고, 타입 가드를 하나 써보자. 그 한 줄이 이 책이 드리는 마지막 선물이다.
