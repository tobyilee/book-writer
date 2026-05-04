# 부록 A. Java/Kotlin ↔ TypeScript 용어 매핑 사전

본문을 읽다가 낯선 TypeScript 용어가 나왔을 때, 혹은 반대로 "Java에서 이 개념이 TS에서는 뭐라고 부르지?"라는 물음이 생겼을 때 펼쳐보자. 이 부록은 처음부터 끝까지 통독하는 자료가 아니다. 찜찜한 용어가 생겼을 때 빠르게 확인하는 자리다.

표는 카테고리별로 정리했다. 항목 수가 많아 보이지만 Java/Kotlin 경험이 있다면 대부분 직관적으로 매핑된다. 다만 표만 보면 놓치기 쉬운 미묘한 차이가 있는 핵심 항목 — `interface`, `data class`, `sealed class`, `Mono`/Promise, 데코레이터 기반 DI, `Result<T>` 등 — 에는 별도로 1~2단락 해설을 달았다. 표를 보고 "아, 그거구나" 하다가 해설로 넘어오면 된다.

부록 B(tsconfig 옵션 사전), 부록 C(CLI 워크쓰루), 부록 D(함정 인덱스)는 이 부록 뒤에 이어진다.

---

## 1. 언어 기본

### 표 — 언어 기본 매핑

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| `interface` (Java) | `interface` (TS) | 모양 정의는 같지만 nominal vs structural — 아래 해설 참조 |
| `class` (nominal) | `class` (structural) | TS `class`도 구조적 호환 적용 |
| `abstract class` | `abstract class` | 거의 동일. TS는 abstract method에 구현부 없어야 |
| `enum` (Java) / `enum class` (Kotlin) | `enum` 또는 union literal | TS `enum`은 런타임 객체 생성; union literal 선호 — 아래 해설 참조 |
| `sealed class` (Kotlin) | discriminated union | `kind` 필드 + 타입 좁히기 — 아래 해설 참조 |
| `data class` (Kotlin) / `record` (Java 16+) | `interface` / `type` + spread | TS에 구조적 동등성·copy() 내장 없음 — 아래 해설 참조 |
| `value class` / `inline class` (Kotlin) | branded type (관용) | 제로 비용 래퍼. TS는 언어 지원 없고 패턴으로 구현 |
| `null` (Java) | `null` / `undefined` | TS는 둘을 구분. `strictNullChecks` 켜면 명시 필요 |
| `Optional<T>` (Java) | `T \| null` / `T \| undefined` | TS는 타입 유니언으로 표현. Optional 클래스 없음 |
| `?.` (null safety, Kotlin) | `?.` (optional chaining) | 의미 동일. TS는 `??` nullish coalescing도 지원 |
| `!!` (null 단언, Kotlin) | `!` (non-null assertion) | `value!`로 null/undefined를 강제 배제. 남용 주의 |
| `var` (Kotlin 가변) / `val` (불변) | `let` (가변) / `const` (불변) | Java `var`는 타입 추론 키워드; TS `var`는 쓰지 말자 |
| `final` (Java 필드) | `readonly` (TS) | 클래스 필드, 인터페이스 프로퍼티에 `readonly` |
| `when` (Kotlin) | `switch` + type narrowing | TS `switch`는 타입 좁히기와 결합해 exhaustive check |
| `instanceof` | `instanceof` / type guard | TS는 `instanceof` 외에 사용자 정의 타입 가드도 활용 |
| `is` (Kotlin, 스마트 캐스트) | type predicate (`x is T`) | `function isFoo(x: unknown): x is Foo` 패턴 |
| 스마트 캐스트 (Kotlin) | narrowing (TS) | `if (typeof x === "string")` 이후 TS가 자동 좁히기 |
| generics `<T>` | generics `<T>` | 문법 비슷하지만 TS는 variance annotation 제한적 |
| `? extends T` (Java wildcard) | `extends` in conditional types | TS에는 use-site variance 없음; declaration-site `in`/`out` (TS 4.7+) |
| `in`/`out` variance (Kotlin) | `in`/`out` (TS 4.7+) | 선언부 variance annotation. TS 4.7부터 지원 |
| `Nothing` (Kotlin) | `never` | 도달 불가 타입. exhaustive check에 활용 |
| `Any` (Kotlin) / `Object` (Java) | `unknown` / `any` | `unknown`이 안전한 최상위 타입; `any`는 타입 검사 포기 |
| `Unit` (Kotlin) / `void` (Java) | `void` / `undefined` | 반환 없는 함수. TS `void`는 `undefined`와 미묘하게 다름 |
| `typealias` (Kotlin) | `type` alias | `type UserId = string`. TS는 structural이라 런타임 구분 없음 |
| `companion object` (Kotlin) | `static` 또는 namespace | TS `class`는 `static` 지원. namespace 패턴도 가능 |
| `object` singleton (Kotlin) | module-level const / singleton 패턴 | TS에 언어 레벨 singleton 없음 |
| extension function (Kotlin) | prototype 확장 (권장 안 함) / 모듈 함수 | TS에 확장 함수 없음; 모듈 함수로 대체 |
| `infix` fun (Kotlin) | 없음 (라이브러리 체이닝으로 대체) | — |
| destructuring (Kotlin `val (a, b) = ...`) | destructuring (`const { a, b } = ...`) | 배열·객체 모두 지원. TS는 타입 자동 추론 |
| spread `*list` (Kotlin vararg) | `...args` (rest/spread) | 함수 인자·배열·객체 spread |
| `lazy` (Kotlin) | lazy init 패턴 (getter 캐싱 등) | TS 언어 레벨 없음 |
| `@JvmField`, `@JvmStatic` | 해당 없음 | JVM interop 전용 |

---

### 해설 — interface: 모양은 같지만 철학이 다르다

Java와 TypeScript 모두 `interface` 키워드를 쓴다. 하지만 의미가 제법 다르다. Java `interface`는 **명목 타입(nominal type)** 시스템 위에 있다. `class Dog implements Animal`이라고 명시해야만 `Dog`가 `Animal`로 취급된다. 선언이 없으면 모양이 똑같아도 호환되지 않는다.

TypeScript `interface`는 **구조적 타입(structural type)** 위에 있다. `Animal`이 `name: string`을 요구한다면, `name: string`이 있는 객체는 `implements Animal`을 쓰지 않아도 `Animal`로 통한다. Java 출신에게 이건 처음엔 신선하고, 나중엔 찜찜하다. `type UserId = string`을 만들어도 그냥 `string`과 구분이 되지 않는 것처럼, 모양이 같으면 같은 타입으로 취급된다는 뜻이기 때문이다. 도메인 안전성이 필요하면 **branded type** 패턴(`string & { readonly _brand: unique symbol }`)을 써야 한다.

TypeScript `interface`에는 Java에 없는 특징이 하나 더 있다. **선언 병합(declaration merging)**이다. 같은 이름의 `interface`를 두 번 선언하면 자동으로 합쳐진다. 서드파티 라이브러리의 `interface`에 필드를 추가할 때 유용하지만, 의도치 않게 합쳐지면 난감한 상황이 생길 수 있으니 주의해두자.

```typescript
// 선언 병합 예시
interface Window {
  myCustomProp: string;
}
// 이제 Window에는 myCustomProp이 있다 (전역 확장 패턴)
```

`interface`와 `type` alias는 많은 경우 교환 가능하지만, 선언 병합이 필요하거나 클래스가 `implements`할 때는 `interface`가 낫고, 유니언·튜플·조건부 타입을 표현할 때는 `type`이 필요하다.

---

### 해설 — enum: TS enum보다 union literal을 쓰는 편이 낫다

Kotlin `enum class`는 풍부하다. 각 상수에 프로퍼티를 붙이고, 메서드도 정의할 수 있다. Java `enum`도 마찬가지다. TypeScript `enum`은 언뜻 비슷해 보이지만 런타임에 실제 객체를 만들어낸다. 이게 번거로운 이유가 있다.

```typescript
enum Direction { Up, Down, Left, Right }
// 컴파일 후 런타임에 {0: 'Up', Up: 0, ...} 객체가 생성된다
```

tree-shaking이 잘 안 되고, const enum은 또 다른 복잡성을 낳는다. 그래서 TS 커뮤니티에서는 **union literal**을 선호한다.

```typescript
type Direction = "Up" | "Down" | "Left" | "Right";
```

가볍고 tree-shaking 친화적이며, 타입 좁히기도 자연스럽다. 다만 Kotlin `enum class`처럼 각 항목에 메서드를 붙이거나 반복(iteration)이 필요하다면 `const` 배열과 `typeof`를 조합하거나, 별도 맵 구조를 쓰는 편이 낫다. enum과 union literal의 선택은 팀 컨벤션 문제이기도 하니, 처음 시작할 때 합의해두자.

---

### 해설 — data class / record: copy()는 직접 써야 한다

Kotlin `data class`는 편리하다. `equals()`, `hashCode()`, `toString()`, `copy()`가 자동으로 생성된다. Java 16+의 `record`도 비슷하다. TypeScript에는 이에 대응하는 언어 내장 기능이 없다.

불변 값 객체는 보통 `interface` 또는 `type`으로 모양을 정의하고, 복사할 때는 spread 연산자를 쓴다.

```typescript
interface Point { readonly x: number; readonly y: number; }

const p1: Point = { x: 1, y: 2 };
const p2: Point = { ...p1, y: 10 };  // Kotlin의 p1.copy(y = 10)에 해당
```

`equals()`에 해당하는 깊은 동등성 비교는 기본 제공이 없다. `JSON.stringify` 비교, lodash `isEqual`, 또는 직접 구현이 필요하다. `Object.freeze()`로 얕은 불변성을 강제할 수 있지만, 중첩 객체는 별도 처리가 필요하다. `Readonly<T>` 유틸리티 타입은 컴파일 타임 불변성을 타입 레벨에서만 보장한다. 런타임에 실제 변경을 막으려면 `Object.freeze()`를 써야 한다.

---

### 해설 — sealed class / discriminated union: `never`로 완전성을 검증하자

Kotlin `sealed class`는 컴파일러가 하위 클래스를 모두 알기 때문에 `when`에서 exhaustive check를 강제한다. 빠진 케이스가 있으면 컴파일 에러다.

TypeScript의 대응은 **discriminated union**이다. 공통 `kind` 필드(또는 `type`, `tag` 등 이름은 자유)로 각 케이스를 구별한다.

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number };

function area(s: Shape): number {
  switch (s.kind) {
    case "circle": return Math.PI * s.radius ** 2;
    case "rect":   return s.width * s.height;
    default:
      const _exhaustive: never = s;  // 새 케이스가 생기면 여기서 컴파일 에러
      return _exhaustive;
  }
}
```

`never` 트릭을 빠뜨리면 새로운 variant를 추가했을 때 컴파일러가 놓친다. 기억해두자 — discriminated union을 쓸 때는 `default: never` 패턴을 습관으로 만드는 편이 낫다.

Kotlin `when`처럼 TS `switch`도 타입 좁히기가 일어난다. `case "circle"` 분기 안에서 `s`는 자동으로 `{ kind: "circle"; radius: number }` 타입이 된다. 스마트 캐스트와 같은 역할이다.

---

## 2. 빌드 / 패키징

| Java / Kotlin / JVM | TypeScript / Node | 비고 |
|---|---|---|
| JVM | Node.js / Bun / Deno (런타임) | 단일 표준 JVM과 달리 런타임이 여럿 |
| Maven / Gradle | npm / pnpm / yarn | 빌드 책임이 여러 도구로 분산 |
| `pom.xml` / `build.gradle` | `package.json` | 의존성·스크립트·메타정보 |
| Maven Central / JCenter | npmjs.com (npm registry) | 의존성 trust boundary가 JVM 대비 매우 느슨 |
| JAR / WAR / EAR | npm 패키지 (`node_modules`) | 바이너리 배포 아닌 소스 배포가 기본 |
| `groupId:artifactId:version` (GAV) | `패키지명@버전` | `lodash@4.17.21` 형식 |
| `compile` scope | `dependencies` | 런타임 필요 의존성 |
| `test` scope | `devDependencies` | 빌드·테스트 전용 의존성 |
| `provided` scope | `peerDependencies` | 호스트 환경이 제공하는 의존성 (플러그인 등) |
| `optional` dependency | `optionalDependencies` | 설치 실패해도 무방 |
| `mvn install` / `gradle build` | `npm install` / `pnpm install` | 로컬 의존성 설치 |
| `mvn clean package` | `npm run build` | 빌드 스크립트 실행 |
| `mvnw` / `gradlew` (wrapper) | `npx` | 버전 고정 실행기. `npx tsc` 등 |
| `settings.gradle` (멀티 프로젝트) | `pnpm workspaces` / `npm workspaces` | 모노레포 루트 설정 |
| Turborepo / Nx (TS 생태계) | Turborepo / Nx | 모노레포 빌드 캐싱·태스크 오케스트레이션 |
| `javac` | `tsc` (TypeScript compiler) | 타입 체크 + 트랜스파일. 느림 |
| — | `esbuild` / `swc` | 트랜스파일 전용. 10~100배 빠름. 타입 체크 안 함 |
| — | `vite` | 프론트엔드 dev server + 번들러. esbuild 기반 |
| `.gitignore` | `.gitignore` + `.npmignore` | npm publish 시 배포 제외 목록 |
| `MANIFEST.MF` | `package.json` `"main"` / `"exports"` | 패키지 진입점 정의 |
| JPMS (`module-info.java`) | `"exports"` in `package.json` | 공개 API 제한. ESM 환경에서 |
| OSGi bundle | ESM + `package.json exports` | JS는 모듈 표준 정착이 늦었음 |
| `lock file` (없음) | `package-lock.json` / `pnpm-lock.yaml` | 재현 가능 빌드를 위한 잠금 파일 |
| GraalVM native-image | `bun build --compile` / `deno compile` | 단일 실행 파일 생성 |

---

## 3. 런타임 / 도구

| Java / JVM | TypeScript / Node 생태계 | 비고 |
|---|---|---|
| JVM (HotSpot) | Node.js (V8 + libuv) | V8은 JIT 포함. libuv가 이벤트 루프 |
| JIT 컴파일 | V8 JIT (Turbofan/Maglev) | 런타임 최적화 |
| GC (G1, ZGC, Shenandoah) | V8 GC (Orinoco) | TS/JS 개발자가 GC를 직접 튜닝하는 일은 드물다 |
| 스레드 (`Thread`, `ExecutorService`) | Worker Threads (Node) / 이벤트 루프 | JS는 기본 단일 스레드. 병렬은 Worker로 |
| 스레드풀 (`ForkJoinPool`) | `worker_threads` 모듈 | CPU 집약 작업 시 |
| `System.out.println` | `console.log` | — |
| `System.err.println` | `console.error` | stderr로 출력 |
| JVM 옵션 (`-Xmx`, `-Xms`) | `NODE_OPTIONS=--max-old-space-size=...` | 힙 크기 조정 |
| `java -jar app.jar` | `node dist/app.js` | 실행 |
| JVM 시작 시간 (~수백 ms~수 초) | Node 시작 시간 (~수십 ms) | Bun은 더 빠름 |
| Java 에이전트 (`javaagent`) | Node `--require` / `--import` | 부트스트랩 훅 |
| JMX / Micrometer | OpenTelemetry (SDK), `prom-client` | 관측 가능성 |
| HotSpot / GraalVM | Node.js / Bun / Deno | 실행 엔진 선택지 |
| **Bun** | — | Zig 작성. TypeScript 직접 실행, 빠른 install, 내장 테스트러너 |
| **Deno** | — | TypeScript 일급, 보안 기본(권한 명시), 표준 라이브러리 내장 |
| `jshell` (REPL) | `node` REPL / `bun` REPL | 대화형 실행 |
| Kotlin scripting (`.kts`) | `ts-node` / `bun run file.ts` | TypeScript 파일 직접 실행 |

---

## 4. 비동기

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| `Future<T>` | `Promise<T>` | 단일 비동기 값. JS 표준 |
| `CompletableFuture<T>` | `Promise<T>` + `.then()` / `async/await` | `thenCompose` → `then`, `thenApply` → `then` |
| `Mono<T>` (Reactor) | `Promise<T>` | 단일 값 비동기 스트림 |
| `Flux<T>` (Reactor) | `Observable<T>` (RxJS) | 여러 값 스트림. 아래 해설 참조 |
| `suspend` fun (Kotlin coroutine) | `async` / `await` | 표면 문법 유사. 내부 동작은 다름 |
| Kotlin `Flow` | `AsyncIterator` / `ReadableStream` / Observable | 지연 스트림. 선택지가 여럿 |
| `CoroutineScope` / `CoroutineContext` | — (언어 레벨 없음) | JS는 이벤트 루프가 암묵적 컨텍스트 |
| `Dispatchers.IO` / `Dispatchers.Default` | libuv I/O (암묵적) / Worker Threads | I/O는 이벤트 루프, CPU는 Worker |
| `async { }` block (Kotlin) | `async function` | 비동기 함수 정의 |
| `await` (Kotlin) | `await` | 값 꺼내기 |
| `runBlocking` (Kotlin) | `await Promise` at top level (ESM), `bun run` | 동기 컨텍스트에서 비동기 실행 |
| `try/catch` for exception | `try/catch` | `async/await`에서 예외 잡기 |
| `onErrorResume`, `onErrorReturn` | `.catch()` | Promise 에러 복구 |
| `timeout` operator (Reactor) | `AbortController` + `AbortSignal` | fetch 등 취소 패턴 |
| `zip`, `flatMap` (Reactor) | `Promise.all`, `Promise.allSettled` | 병렬 실행 |
| checked exception | — (JS에 없음) | 아래 해설 참조 |

---

### 해설 — Mono/Flux vs Promise/Observable: 즉시 실행 vs 지연 실행

Java Reactor의 `Mono`/`Flux`와 TypeScript의 `Promise`/`Observable`(RxJS)은 겉으로 비슷해 보이지만 중요한 차이가 있다.

**Promise는 만드는 순간 실행이 시작된다.** `new Promise((resolve) => { /* 이미 실행 중 */ })`. 구독자가 없어도 돈다. 이건 Java의 `CompletableFuture`와 같은 동작이다. 반면 Reactor `Mono`는 구독하기 전까지 아무것도 하지 않는다 — cold publisher다.

RxJS `Observable`도 cold다. `subscribe()`를 호출해야 실행이 시작된다. 이 차이를 모르고 `Observable`을 `Promise`처럼 쓰면 난감한 상황이 생긴다. 함수를 정의만 해두고 실행은 되지 않는다.

```typescript
// Promise: 선언 즉시 fetch 실행
const p = fetch("https://api.example.com/data");

// Observable: subscribe() 전까지 실행 없음
const obs = new Observable((subscriber) => {
  fetch("https://api.example.com/data").then(r => subscriber.next(r));
});
// obs를 아무도 구독하지 않으면 fetch는 일어나지 않는다
```

현실 TS 코드에서 RxJS는 Angular 프로젝트 외에는 점차 드물어졌다. `async/await` + `AbortController`로 대부분의 시나리오를 커버하고, 복잡한 스트림 조합은 React Query나 SWR 같은 라이브러리가 흡수했다. Reactor 숙련자라면 RxJS가 편할 수 있지만, 팀 전체가 배워야 한다면 `async/await`을 먼저 익히는 편이 낫다.

---

## 5. DI / 프레임워크

| Java / Kotlin (Spring) | TypeScript (NestJS / 기타) | 비고 |
|---|---|---|
| `@Component` | `@Injectable()` (NestJS) | 의존성 주입 대상 등록 |
| `@Service` | `@Injectable()` | NestJS는 역할별 데코레이터 구분 없음 |
| `@Repository` | `@Injectable()` + TypeORM Repository | ORM 레이어는 별도 |
| `@Controller` (MVC) | `@Controller()` (NestJS) | HTTP 요청 처리 |
| `@RestController` | `@Controller()` + `@Get()`/`@Post()` 등 | 아래 해설 참조 |
| `@Configuration` | `@Module()` (NestJS) | 모듈 구성 선언 |
| `@Bean` | `@Module({ providers: [...] })` | Provider 등록 |
| `@Autowired` | 생성자 주입 (NestJS 권장) | NestJS는 생성자 주입 자동 처리 |
| component scan (Spring) | `@Module({ imports: [...] })` 명시 등록 | NestJS는 자동 스캔 없음 — 아래 해설 참조 |
| `ApplicationContext` | NestJS `ModuleRef` | 런타임 컨테이너 접근 |
| `@Scope(prototype)` | `{ scope: Scope.REQUEST }` | 요청별 인스턴스 |
| `@Value("${...}")` | `@Inject(CONFIG)` + ConfigModule | 환경변수 주입 |
| `@Profile` | — (조건부 모듈 구성) | 환경별 모듈 분기 |
| `@ExceptionHandler` | `@Catch()` + ExceptionFilter (NestJS) | 전역 예외 처리 |
| `@ControllerAdvice` | APP_FILTER (전역 ExceptionFilter) | 전역 예외 핸들러 |
| `@Aspect` (AOP) | Interceptor (NestJS) | 횡단 관심사 |
| `@Transactional` | TypeORM DataSource.transaction() | 선언적 트랜잭션 없음 (라이브러리 의존) |
| `HandlerInterceptor` | NestJS `Interceptor` | 요청/응답 전후 처리 |
| `Filter` (Servlet) | NestJS `Guard` / `Middleware` | 인증·인가 |
| Guice / Dagger | tsyringe / InversifyJS | 더 가벼운 DI 컨테이너. Spring보다 Guice에 가까움 |
| legacy `experimentalDecorators` | legacy decorator mode (NestJS 현재) | TS 5.0+ 신규 표준 데코레이터와 다름 |
| TC39 표준 데코레이터 (TS 5.0+) | 신규 decorator proposal | NestJS는 당분간 legacy 유지 |

---

### 해설 — @RestController vs @Controller: Spring의 통합을 NestJS는 나눈다

Spring `@RestController`는 `@Controller + @ResponseBody`의 합성이다. JSON 응답이 기본이다. NestJS `@Controller()`는 라우트 prefix를 지정하고, 메서드별로 `@Get()`, `@Post()` 등을 붙인다. JSON 직렬화는 기본이다.

```typescript
// NestJS
@Controller('users')
export class UsersController {
  @Get(':id')
  findOne(@Param('id') id: string): UserDto {
    return this.usersService.findOne(+id);
  }
}
```

Spring `@RequestMapping`은 NestJS에서 `@Controller('prefix')` + 메서드 데코레이터(`@Get()`, `@Post()`)로 나뉜다. Spring `@PathVariable`은 `@Param()`, `@RequestBody`는 `@Body()`, `@RequestParam`은 `@Query()`로 대응한다.

---

### 해설 — component scan vs Module 명시 등록: NestJS는 자동 스캔을 하지 않는다

Spring의 component scan은 패키지를 뒤져 `@Component` 계열 클래스를 자동으로 빈 컨테이너에 등록한다. 편리하지만 규모가 커지면 "이 빈이 어디서 왔나"가 불투명해질 수 있다.

NestJS는 다르다. 모든 provider는 `@Module({ providers: [UserService, AuthService] })`처럼 **명시적으로 등록**해야 한다. 다른 모듈에서 쓰려면 `exports`에도 적어야 한다. 처음엔 번거롭다. 하지만 의존 관계가 명확해지고, 어디서 무엇이 주입되는지 추적하기 쉬워진다. Spring DI에 익숙한 사람이 NestJS 코드를 처음 봤을 때 "왜 이렇게 verbose한가" 싶은 부분이 바로 이 지점이다. 의도적인 선택이라고 이해해두자.

---

## 6. 검증 (Validation)

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| Bean Validation (`javax.validation` / `jakarta.validation`) | zod / valibot / ArkType | 스키마 우선 설계 |
| `@Valid` | `z.parse()` / `schema.parse()` | 요청 유효성 검증 |
| `@NotNull` | `z.string()` (nullable 제외) | null 불허 |
| `@NotBlank` | `z.string().min(1)` | 빈 문자열 불허 |
| `@Size(min=, max=)` | `z.string().min().max()` | 길이 범위 |
| `@Email` | `z.string().email()` | 이메일 형식 |
| `@Pattern(regexp=)` | `z.string().regex()` | 정규식 |
| `@Min` / `@Max` | `z.number().min().max()` | 숫자 범위 |
| `@Positive` | `z.number().positive()` | 양수 |
| `@Future` / `@Past` | 커스텀 refine | zod `.refine()` 활용 |
| `ConstraintValidator` (커스텀) | `.refine()` / `.transform()` | 복잡한 검증 로직 |
| `@Valid` on nested | `z.object({ nested: z.object({...}) })` | 중첩 검증 |
| Hibernate Validator | zod (가장 광범위) | 커뮤니티 사실상 표준 |
| class-validator (NestJS용) | zod / valibot | NestJS는 class-validator 전통적 선택 |
| `@Validated` groups | `z.discriminatedUnion` / 분기 스키마 | 그룹 검증은 zod에 직접 해당 없음 |

---

## 7. 테스트

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| JUnit 5 | Vitest / Jest | Vitest가 신규 프로젝트 권장. Jest는 기존 표준 |
| `@Test` | `test()` / `it()` | 테스트 함수 |
| `@BeforeEach` / `@AfterEach` | `beforeEach()` / `afterEach()` | 훅 |
| `@BeforeAll` / `@AfterAll` | `beforeAll()` / `afterAll()` | 전체 훅 |
| `@Nested` | `describe()` 중첩 | 테스트 그룹화 |
| `@Disabled` | `test.skip()` | 테스트 비활성화 |
| `@ParameterizedTest` | `test.each()` | 파라미터 테스트 |
| `Assertions.assertEquals` | `expect(a).toBe(b)` | 동등성 검증 |
| `assertThrows` | `expect(() => fn()).toThrow()` | 예외 검증 |
| `assertDoesNotThrow` | `expect(() => fn()).not.toThrow()` | — |
| Mockito | `vi.mock()` (Vitest) / `jest.mock()` | 모킹 |
| `@Mock` / `@InjectMocks` | `vi.fn()` / 수동 주입 | Vitest에 자동 어노테이션 없음 |
| `when().thenReturn()` | `vi.fn().mockReturnValue()` | 목 반환값 설정 |
| `verify()` | `expect(fn).toHaveBeenCalled()` | 호출 검증 |
| MockK (Kotlin) | `vi.mock()` | Kotlin 스타일 목 |
| jqwik (property-based) | fast-check | 속성 기반 테스트. 아래 해설 참조 |
| AssertJ | 없음 (Vitest expect 체이닝) | fluent assertion |
| `@SpringBootTest` | Vitest + supertest | 통합 테스트 |
| RestAssured | supertest / `fetch` + Vitest | HTTP 통합 테스트 |
| WireMock / MockServer | `msw` (Mock Service Worker) | API 목 서버 |
| Selenium / Playwright (Java) | Playwright (TS) | E2E 테스트. TS Playwright가 더 자연스러움 |
| Testcontainers (Java) | Testcontainers (Node) | 실제 DB·서비스 컨테이너 |
| `expect-type` | `expectTypeOf()` (Vitest) | 타입 수준 테스트 — 타입이 맞는지 확인 |

---

## 8. 에러 처리

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| checked exception | 없음 | TS에 checked exception 없음 — 아래 해설 참조 |
| unchecked exception (RuntimeException) | `throw new Error(...)` | JS/TS의 모든 throw는 unchecked |
| `try / catch / finally` | `try / catch / finally` | 동일 |
| `Exception` 계층 | `Error` 계층 (`TypeError`, `RangeError` 등) | 내장 Error 서브클래스 |
| `throws` 선언 | 없음 | 함수 시그니처에 throw 명시 불가 |
| `Throwable` | `unknown` (catch 변수 타입) | TS 4.0+ catch `e`는 `unknown` — `e as Error` 필요 |
| `Result<T>` (Kotlin) | `neverthrow` / `fp-ts` / `Effect-ts` | 아래 해설 참조 |
| `Either<E, A>` (Arrow/Vavr) | `Result<T, E>` (neverthrow) | 실패를 타입으로 표현 |
| `try { } catch (e: SpecificException)` | `catch (e) { if (e instanceof SpecificError) }` | TS catch는 타입 명시 불가 |
| `@ExceptionHandler` (Spring) | NestJS ExceptionFilter | 전역 예외 처리 |
| `ResponseStatusException` | `HttpException` (NestJS) | HTTP 에러 응답 |

---

### 해설 — checked exception vs throw: TS에는 컴파일러 강제가 없다

Java의 checked exception은 사랑받지 못하지만, 적어도 함수가 어떤 예외를 던질 수 있는지 **컴파일러가 강제로 알린다**. TypeScript에는 이 기능이 없다. 모든 throw는 unchecked이며, 함수 시그니처에 "이 함수는 DatabaseError를 던질 수 있다"고 표현하는 방법이 없다.

그래서 많은 팀이 **Result 패턴**을 채택한다. 예외를 던지는 대신 성공/실패를 타입으로 표현하는 것이다.

```typescript
// neverthrow 라이브러리 예시
import { ok, err, Result } from "neverthrow";

function divide(a: number, b: number): Result<number, "division-by-zero"> {
  if (b === 0) return err("division-by-zero");
  return ok(a / b);
}

const result = divide(10, 0);
if (result.isOk()) {
  console.log(result.value);
} else {
  console.log("실패:", result.error);
}
```

`neverthrow`, `fp-ts`, `Effect-ts` 등이 이 패턴을 라이브러리로 제공한다. `Effect-ts`는 함수형 프로그래밍 전반을 제공하며 Kotlin Arrow와 유사한 위치다. 팀에 따라 호불호가 갈린다 — "너무 복잡하다"는 팀과 "이게 맞다"는 팀으로. 처음엔 `neverthrow` 정도가 진입 장벽이 낮은 편이다.

외부 I/O 경계(DB 호출, HTTP 요청, 파일 읽기)에서는 `try/catch`를 쓰고, 내부 도메인 로직에서는 Result 패턴을 쓰는 절충도 자주 쓰인다.

---

## 9. 타입 시스템 심화

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| 제네릭 `<T>` | 제네릭 `<T>` | 문법 유사 |
| 상한 경계 `<T extends Foo>` | `<T extends Foo>` | 동일 |
| 하한 경계 `<T super Foo>` | 없음 (conditional type으로 우회) | TS에 직접 대응 없음 |
| wildcard `<?>` | `unknown` / `any` | TS에 use-site wildcard 없음 |
| 공변 `out T` (Kotlin) | `out T` (declaration-site, TS 4.7+) | 읽기 전용 위치 |
| 반변 `in T` (Kotlin) | `in T` (declaration-site, TS 4.7+) | 쓰기 전용 위치 |
| reified generics (Kotlin inline) | 없음 | TS generics는 런타임 소거 |
| `Class<T>` | 없음 (structural이라 불필요한 경우 많음) | 런타임 타입 토큰 |
| `instanceof` 타입 체크 | `instanceof` / type predicate / `typeof` | |
| sealed 계층 + when | discriminated union + switch/narrowing | |
| `Nothing` | `never` | 하위 타입. exhaustive check |
| `Any?` / `Object` | `unknown` | 모든 타입의 상위. 사용 전 narrowing 필요 |
| conditional type | `T extends U ? X : Y` | Java에 없음. TS 고유 강점 |
| mapped type | `{ [K in keyof T]: ... }` | Java에 없음. 타입을 변환 |
| template literal type | `` `prefix_${T}` `` | Java에 없음. 문자열 타입 조합 |
| `infer` | `infer R` in conditional types | 타입에서 타입을 추출 |
| `typeof` (Java reflection) | `typeof value` / `ReturnType<typeof fn>` | 값에서 타입 추출 |
| `keyof T` | `keyof T` | 객체 키의 유니언 타입 |
| `Partial<T>` | `Partial<T>` | 모든 필드 optional |
| `Required<T>` | `Required<T>` | 모든 필드 required |
| `Readonly<T>` | `Readonly<T>` | 모든 필드 readonly |
| `Record<K, V>` | `Record<K, V>` | 키–값 맵 타입 |
| `Pick<T, K>` | `Pick<T, K>` | 일부 필드만 선택 |
| `Omit<T, K>` | `Omit<T, K>` | 일부 필드 제외 |
| `ReturnType<F>` | `ReturnType<typeof fn>` | 함수 반환 타입 추출 |
| `Parameters<F>` | `Parameters<typeof fn>` | 함수 인자 타입 추출 |
| `Awaited<T>` | `Awaited<T>` | Promise의 resolved 타입 추출 |

---

## 10. 모듈 시스템

| Java / Kotlin | TypeScript | 비고 |
|---|---|---|
| `import com.example.Foo` | `import { Foo } from "./foo"` | 경로 기반 (상대·절대) |
| `package` 선언 | 없음 | TS는 파일 자체가 모듈 |
| `public` / `private` (클래스) | `export` / 미export | 파일 레벨 export 제어 |
| JPMS `exports` | `package.json "exports"` | 패키지 공개 API |
| CJS (`require()`) | CommonJS (Node 기본 레거시) | `"type": "commonjs"` or `.cjs` |
| ESM (`import`) | ESM (`"type": "module"`) | 현재 표준. 혼용 시 주의 |
| `import static` | `import { fn }` (named import) | — |
| wildcard `import *` | `import * as ns from "..."` | namespace import |
| default `import` | `import Foo from "..."` | default export |
| 순환 의존성 금지 | 순환 import 가능하지만 권장 안 함 | 런타임 undefined 가능성 |
| `package-info.java` | `index.ts` (barrel export) | 모듈 진입점 관용 |
| `tsconfig.paths` | `tsconfig "paths"` | 경로 alias (`@/` 등) |
| `tsconfig.references` | `tsconfig.references` | 모노레포 프로젝트 참조 (IDE 성능) |

---

## 마무리

이 사전은 살아있는 문서다. TypeScript 생태계는 빠르게 움직이기 때문에, 특히 런타임 선택(Node/Bun/Deno)과 데코레이터 표준화 부분은 1~2년 사이에도 바뀔 수 있다. 표의 "비고" 란에 "당분간"이나 "현재 기준"이라고 적힌 항목들은 그 변화가 빠른 영역이다.

본문에서 개념을 따라가다 이 부록으로 돌아올 때마다, "아, Java에서는 이걸 이렇게 불렀지"라는 연결고리가 생겼으면 좋겠다. 낯선 용어가 익숙한 이름을 달고 있을 때, 전환의 속도는 훨씬 빨라진다.

다음으로는 **부록 B — tsconfig 옵션 사전**이 이어진다. `strict`가 사실 하나의 옵션이 아니라 여러 옵션의 묶음이라는 것, `moduleResolution`이 왜 이렇게 많은 값을 가지는지, 현실적인 tsconfig 템플릿 다섯 가지가 거기서 기다리고 있다.
