# 13장. 웹 백엔드와 풀스택 — Express·Fastify·Hono·NestJS·Next·Astro의 여섯 길

Spring 백엔드를 5년 넘게 짜온 개발자라고 해보자. 그에게 "이번 프로젝트는 Node.js 백엔드로 갑니다"라는 말이 날아온다. 손에 익은 `@RestController`, `@Service`, `@Repository` 패턴은 어디 갔나. `ApplicationContext`가 알아서 주입해주던 의존성은 이제 누가 관리하나. 처음에는 낯설고 막막하다. 그런데 NestJS 공식 문서를 열어본 순간 — 어, 이거 Spring 아닌가? `@Module`, `@Controller`, `@Injectable`, `@Inject`. 눈에 익은 어휘들이 줄지어 나온다.

그렇다면 NestJS는 정말 "Spring의 TS판"인가? 아, 거의 맞다. 하지만 "거의"라는 단어가 굉장히 중요하다. 모양이 비슷해서 자신감을 갖고 뛰어들었다가 예상 밖의 자리에서 발이 걸리면 그때의 당혹감이 더 크다. 이 챕터는 그 "거의"의 안쪽을 정직하게 들여다보는 챕터다.

동시에 이 챕터는 NestJS 한 가지만 이야기하지 않는다. Spring 베테랑이 익숙함을 찾아 NestJS로 첫 발을 딛는 길 외에, 전혀 다른 철학으로 설계된 Hono라는 길이 있다. 타입이 라우트 정의 시점부터 자동으로 흘러나와 RPC 클라이언트까지 자동 생성되는 그 마법 — 5장의 "타입을 만드는 타입"이 현실 코드에서 어떻게 살아남는지가 여기서 드러난다. 그리고 Express와 Fastify는 여전히 현장의 표준으로 버티고 있으며, Next.js를 비롯한 풀스택 메타프레임워크는 "백엔드와 프론트엔드의 경계"라는 오래된 질문을 새로 제기하고 있다.

여섯 길을 걸어보자. 어떤 길이 당신 팀에 맞는지 — 그 판단을 이 챕터에서 가져갈 수 있길 바란다.

---

## NestJS — Spring 베테랑의 환영

### 1:1 대응이 진짜인 자리

솔직히 말하면, NestJS의 첫인상은 Spring 개발자에게 상당히 친절하다. 단순히 느낌이 비슷한 게 아니라 실제로 1:1 대응이 성립하는 영역이 넓다. 코드를 나란히 놓고 보는 게 가장 빠르다.

---

📚 **Java/Kotlin 시선 ① — Spring `@RestController` ↔ NestJS `@Controller`**

```java
// Spring
@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<UserDto> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }

    @PostMapping
    public ResponseEntity<UserDto> createUser(@RequestBody @Valid CreateUserRequest req) {
        return ResponseEntity.status(201).body(userService.create(req));
    }
}
```

```typescript
// NestJS
@Controller('users')
export class UserController {
    constructor(private readonly userService: UserService) {}

    @Get(':id')
    getUser(@Param('id') id: string): Promise<UserDto> {
        return this.userService.findById(id);
    }

    @Post()
    @HttpCode(201)
    createUser(@Body() req: CreateUserDto): Promise<UserDto> {
        return this.userService.create(req);
    }
}
```

데코레이터 이름, 파라미터 추출 방식, 의존성 주입 — 패턴이 거의 동일하다. Spring 백엔드 경험자라면 이 코드를 처음 봐도 뜻을 읽는 데 10초도 걸리지 않는다. NestJS가 Spring·Angular의 설계 철학을 의도적으로 차용했다는 점은 공식 문서에도 명시되어 있다.

서비스 계층과 주입 방식도 마찬가지다.

```java
// Spring
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    public UserDto findById(Long id) { ... }
}
```

```typescript
// NestJS
@Injectable()
export class UserService {
    constructor(
        @InjectRepository(User)
        private readonly userRepository: Repository<User>
    ) {}

    findById(id: string): Promise<UserDto> { ... }
}
```

`@Service` ↔ `@Injectable`. `@Autowired` ↔ 생성자 주입. 구조가 1:1이다. 심지어 `@Module`이 Spring의 `@Configuration`+`@ComponentScan` 역할을 한다는 것까지.

```typescript
@Module({
    imports: [TypeOrmModule.forFeature([User])],
    controllers: [UserController],
    providers: [UserService],
    exports: [UserService],       // ← 이 줄이 핵심 차이점
})
export class UserModule {}
```

---

### Spring과 다른 의외의 자리

1:1 대응이 안심을 주다가, 막상 실제 코드를 짜면 생각지 못한 곳에서 발이 걸린다. 이런 자리를 미리 알아두면 입사 첫 달의 시행착오를 상당히 줄일 수 있다.

**첫 번째: 모듈 명시 등록 vs Spring component scan**

Spring에서는 `@ComponentScan`이 지정된 패키지 아래를 자동으로 스캔해서 `@Component`, `@Service`, `@Repository`를 가진 클래스를 찾아 빈으로 등록한다. 별도로 "이 서비스를 이 컨트롤러에 연결하겠다"고 선언할 필요가 없다. 패키지 구조만 맞으면 자동이다.

NestJS는 다르다. 모든 프로바이더는 해당 모듈의 `providers` 배열에 명시적으로 등록해야 한다. 그리고 모듈 밖에서 쓰려면 `exports` 배열에도 추가해야 한다. 처음에 이게 번거로워 보인다. 그런데 사실 이 명시성이 장점이다 — 의존성 그래프가 모듈 파일만 봐도 보인다.

---

📚 **Java/Kotlin 시선 ② — Spring component scan ↔ NestJS Module 재구성**

```java
// Spring — @ComponentScan 범위 안에 있으면 자동 등록
@SpringBootApplication  // @ComponentScan 포함
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// UserService가 같은 패키지 트리에 있으면 자동 발견됨
@Service
public class UserService { ... }
```

```typescript
// NestJS — 모듈에 명시적으로 등록해야 함
@Module({
    providers: [UserService],   // 이 줄이 없으면 DI 컨테이너에 없음
    controllers: [UserController],
    exports: [UserService],     // 다른 모듈이 쓰려면 이 줄도 필요
})
export class UserModule {}

// AppModule에서 UserModule을 imports에 넣어야 함
@Module({
    imports: [UserModule, AuthModule],
})
export class AppModule {}
```

Spring 베테랑이 처음 NestJS에서 만나는 난감한 에러 중 하나가 "Nest can't resolve dependencies of the XService"다. 열심히 `@Injectable()`을 붙였는데 왜? 라며 30분을 날린다. 답은 항상 모듈 `providers` 배열에 등록을 빠뜨렸거나, 다른 모듈의 서비스를 `exports`하지 않았기 때문이다.

---

**두 번째: Module re-export 모델**

NestJS의 모듈은 다른 모듈을 imports한 뒤 그것을 다시 exports할 수 있다. 이걸 module re-export라고 한다.

```typescript
@Module({
    imports: [TypeOrmModule.forFeature([User, Post])],
    providers: [UserService, PostService],
    exports: [
        UserService,
        TypeOrmModule,  // ← TypeOrmModule 자체를 re-export
    ],
})
export class CoreModule {}

// CoreModule을 import하는 모듈은 TypeOrmModule도 같이 받는다
@Module({
    imports: [CoreModule],  // UserService와 TypeOrmModule이 함께 들어옴
})
export class FeatureModule {}
```

Spring에는 이런 개념이 없다. Spring에서는 빈이 애플리케이션 컨텍스트 전체에 공유된다. NestJS에서는 모듈 경계가 DI 스코프를 나눈다 — 그래서 "어느 모듈이 어떤 모듈을 볼 수 있는가"를 모듈 파일을 보면 명시적으로 알 수 있다는 이점이 생긴다.

**세 번째: Exception Filter의 결**

Spring에서는 `@ControllerAdvice` + `@ExceptionHandler`로 전역 예외를 처리한다. NestJS에는 `ExceptionFilter`가 있다. 원리는 비슷하지만 등록 방식이 다르다.

```typescript
// NestJS Exception Filter
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
    catch(exception: HttpException, host: ArgumentsHost) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse<Response>();
        const status = exception.getStatus();

        response.status(status).json({
            statusCode: status,
            message: exception.message,
            timestamp: new Date().toISOString(),
        });
    }
}

// 등록 방식 세 가지
// 1. 컨트롤러 레벨
@UseFilters(new HttpExceptionFilter())
export class UserController {}

// 2. 메서드 레벨
@Get(':id')
@UseFilters(HttpExceptionFilter)
getUser(@Param('id') id: string) {}

// 3. 전역 (main.ts)
app.useGlobalFilters(new HttpExceptionFilter());
```

Spring의 `@ControllerAdvice`는 클래스 하나로 모든 컨트롤러에 적용된다. NestJS는 전역·모듈·컨트롤러·메서드 네 단계 스코프를 선택할 수 있다. 세밀하지만, 처음에는 "어디에 등록해야 하는 거지?" 하는 당혹감이 있다.

**네 번째: Pipe vs Filter — Guard까지**

Spring에는 `HandlerInterceptor`, `OncePerRequestFilter`, `@PreAuthorize` 같은 인터셉터/필터/보안 어노테이션이 있다. NestJS에는 이를 대응하는 개념이 다섯 가지로 나뉜다.

| NestJS 개념 | 역할 | Spring 대응 |
|---|---|---|
| Guard | 인증·인가 — 요청을 허용할지 결정 | `@PreAuthorize` / Security Filter |
| Pipe | 입력 변환·검증 | `@Valid` + Converter |
| Interceptor | 요청·응답 가로채기 | `HandlerInterceptor` |
| Exception Filter | 예외를 HTTP 응답으로 변환 | `@ExceptionHandler` / `@ControllerAdvice` |
| Middleware | Express 미들웨어와 동일 | Servlet Filter |

Spring에서 하나의 개념(`Filter`, `Interceptor`)이 하던 일을 NestJS가 다섯으로 분리했다고 이해하면 된다. 실수하기 쉬운 자리는 "이 로직은 Guard인가 Interceptor인가"다 — 인가(authorization)는 Guard, 로깅·응답 가공은 Interceptor로 가는 편이 낫다.

**다섯 번째: Provider Scope**

Spring의 빈은 기본이 싱글톤이다. NestJS도 기본은 싱글톤이다 — 여기까진 같다. 그런데 NestJS는 `REQUEST` 스코프와 `TRANSIENT` 스코프를 지원한다.

```typescript
// REQUEST 스코프 — 각 요청마다 새 인스턴스
@Injectable({ scope: Scope.REQUEST })
export class RequestScopedService {}

// TRANSIENT 스코프 — 주입될 때마다 새 인스턴스
@Injectable({ scope: Scope.TRANSIENT })
export class TransientService {}
```

함정이 있다. `REQUEST` 스코프 프로바이더를 싱글톤 프로바이더에 주입하면 싱글톤이 REQUEST 스코프 프로바이더를 고정 참조하게 되어 의도대로 동작하지 않는다. 이런 scope propagation 문제는 Spring에도 존재하지만, NestJS에서는 에러 메시지가 덜 친절한 편이라 디버깅이 번거롭다.

---

🚧 **함정 박스 — 데코레이터 두 종류 혼동**

**증상**: `@Inject()`, `@Injectable()` 같은 데코레이터를 쓰는데 "Experimental support for decorators is a feature that is subject to change"라는 경고가 뜨거나, tsconfig 설정을 아무리 건드려도 런타임 에러가 난다. 또는 새 프로젝트에 NestJS를 설치했는데 `reflect-metadata`를 import하지 않으면 동작하지 않는다.

**원인**: TypeScript의 데코레이터는 현재 두 종류가 공존한다.
- **Legacy 데코레이터** (`experimentalDecorators: true`): NestJS·TypeORM·class-validator가 의존하는 구버전. 런타임 메타데이터를 쓰기 위해 `emitDecoratorMetadata: true`와 `reflect-metadata` 라이브러리가 함께 필요하다.
- **TC39 Stage 3 데코레이터** (TS 5.0+): ECMAScript 표준 제안에 정렬된 신버전. 메타데이터 reflection API가 별도 제안(Decorator Metadata)으로 분리되어 있으며, NestJS가 의존하는 `reflect-metadata`와 호환되지 않는다.

TS 5.0 릴리즈 노트는 명시적으로 "we've decided to make a hard pivot to the new decorators proposal"이라고 선언했다. 그런데 NestJS는 여전히 legacy 데코레이터를 사용한다. 새 표준으로의 마이그레이션이 NestJS 아키텍처 전체를 바꾸는 작업이기 때문이다.

**처방**: NestJS 프로젝트라면 tsconfig에서 반드시 `"experimentalDecorators": true`와 `"emitDecoratorMetadata": true`를 유지하고, `main.ts` 또는 진입 파일 최상단에 `import 'reflect-metadata'`를 두어야 한다. 새 TC39 데코레이터와 혼용하지 말 것. 새 프로젝트에서 NestJS를 도입할 때는 `@nestjs/cli`가 생성하는 기본 tsconfig를 그대로 쓰는 편이 안전하다.

---

### Spring 시니어가 처음 만났을 때 헷갈리는 5가지

이 다섯 가지를 미리 알면 입사 첫 달이 달라진다.

**① 모듈 등록 빠뜨리기** — "Nest can't resolve dependencies" 에러의 99%는 `providers`나 `exports`에 빠진 항목이 있어서다. 에러가 나면 먼저 모듈 파일을 보자.

**② 순환 의존성** — A 모듈이 B 모듈을 import하고 B 모듈이 A 모듈을 import하면 NestJS가 시작 시 에러를 낸다. `forwardRef(() => BModule)` 패턴으로 해결하지만, 이게 필요해졌다는 것은 모듈 분리가 잘못됐다는 신호이기도 하다. Spring에서는 같은 상황에 `@Lazy`를 쓰거나 구조를 재설계했을 것이다.

**③ `async` 프로바이더와 초기화 순서** — 비동기로 초기화해야 하는 프로바이더(예: DB 커넥션 확인)는 `useFactory`와 `async/await`를 조합한 async provider 패턴을 써야 한다. Spring의 `@PostConstruct`나 `InitializingBean`과 비슷하지만, 실수로 `async`를 빠뜨리면 초기화 전에 요청이 들어와 난감한 상황이 생긴다.

**④ Guard와 Interceptor의 실행 순서** — Middleware → Guard → Interceptor(before) → Pipe → Controller → Interceptor(after) → Exception Filter 순서다. Spring의 Filter → Interceptor(preHandle) → Controller → Interceptor(postHandle) → Filter(after) 순서와 비슷하지만 이름과 계층이 달라 헷갈린다. Pipe가 Guard 이후에 실행된다는 점 — 즉, 인가가 먼저 통과된 후에 입력 검증이 된다는 점 — 이 의외로 중요하다.

**⑤ `@Param()`, `@Body()`, `@Query()` 데코레이터 타입** — NestJS의 `@Param('id')`는 항상 `string`을 반환한다. Spring의 `@PathVariable Long id`처럼 자동 형변환이 없다. `parseInt(id)`를 직접 하거나, `ParseIntPipe`를 함께 쓰는 패턴을 알아야 한다.

```typescript
// 타입 변환을 Pipe에 위임하는 패턴
@Get(':id')
getUser(@Param('id', ParseIntPipe) id: number): Promise<UserDto> {
    return this.userService.findById(id);
}
```

---

### NestJS의 legacy decorator 미래 — 어디로 가는가

솔직히 이 부분은 커뮤니티에서도 의견이 갈린다. NestJS가 TC39 신규 표준 데코레이터로 마이그레이션할 수 있을까?

기술적 난관이 있다. 신규 데코레이터 표준은 `reflect-metadata`가 제공하는 런타임 메타데이터 API와 호환되지 않는다. NestJS의 DI 컨테이너, class-validator의 `@IsString()`, TypeORM의 `@Column()`은 모두 이 메타데이터에 의존한다. 메타데이터 reflection을 위한 별도 TC39 제안(Decorator Metadata)이 있지만, 아직 표준이 완전히 자리를 잡지 않았다.

낙관론자는 "결국 이전한다, 시간 문제"라고 말한다. 비관론자는 "구조 전체를 바꿔야 하는데, NestJS가 그 비용을 감당하려면 결국 다른 아키텍처로 가야 한다"고 말한다. 2025년 현재의 현실적인 답은: **NestJS는 당분간 legacy 데코레이터 위에 머문다.** `experimentalDecorators` 모드는 TS 팀이 유지하겠다고 밝혔으므로, 기존 NestJS 코드베이스는 그대로 동작한다. 신규 프로젝트에 NestJS를 도입할 때 이 점을 인지하고 선택하는 편이 낫다.

---

### DI 컨테이너 비교 — NestJS vs InversifyJS vs tsyringe

NestJS가 아닌 환경에서 DI가 필요할 때는 선택지가 있다.

| | NestJS | InversifyJS | tsyringe |
|---|---|---|---|
| 철학 | 프레임워크 내장 DI | 독립 DI 컨테이너 | 경량 DI 컨테이너 |
| Spring 비유 | Spring DI + 프레임워크 | Guice | Dagger (가벼운 쪽) |
| 데코레이터 | legacy `experimentalDecorators` | legacy | legacy |
| 메타데이터 | `reflect-metadata` 의존 | `reflect-metadata` 의존 | `reflect-metadata` 의존 |
| 학습 곡선 | 가파름 (모듈 체계 이해 필요) | 중간 | 완만 |
| 사용 맥락 | 백엔드 풀프레임워크 | 복잡한 독립 앱, CLI | 간단한 DI 필요 시 |

InversifyJS는 Spring보다 Guice에 가깝다 — 바인딩을 명시적으로 선언하고, 컨테이너에서 해결(resolve)하는 패턴이다. Spring의 자동 와이어링에 비하면 조금 더 명시적이고, NestJS의 모듈 체계보다 가볍다. Express나 Fastify와 함께 DI만 붙이고 싶을 때 선택지가 된다.

---

## Hono — 타입이 흐르는 Web Standards 서버

### 5장의 마법이 현실이 되는 자리

5장에서 `infer`, mapped types, 조건부 타입을 배울 때 "이게 실제로 어디에 쓰이는 거지?"라는 의문이 생겼다면, Hono가 그 답 중 하나다. Hono의 라우터는 라우트 정의 시점부터 응답 타입이 자동으로 추론되어 흐른다 — 그리고 그 타입을 바탕으로 RPC 클라이언트가 자동으로 만들어진다.

어떻게 동작하는지 부품 단위로 분해해보자.

```typescript
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

// 라우트 정의 — 이 시점에서 타입 정보가 캡처됨
const routes = app
    .get('/users/:id', async (c) => {
        const id = c.req.param('id')  // string으로 추론됨
        const user = await findUser(id)
        return c.json({ id: user.id, name: user.name })
        //      ↑ 반환 타입이 자동 추론됨
    })
    .post('/users',
        zValidator('json', z.object({
            name: z.string(),
            email: z.string().email(),
        })),
        async (c) => {
            const body = c.req.valid('json')
            // body의 타입이 { name: string, email: string }으로 추론됨
            const user = await createUser(body)
            return c.json(user, 201)
        }
    )

export type AppType = typeof routes
// AppType에 모든 라우트의 입력·출력 타입이 인코딩되어 있음
```

이 `AppType`이 핵심이다. 각 라우트의 URL 패턴, HTTP 메서드, 요청 바디 타입, 응답 타입이 모두 타입 레벨에서 인코딩된다. 5장에서 본 매핑 타입과 조건부 타입이 내부적으로 이 정보를 추출한다.

### RPC 클라이언트 자동 생성

`AppType`을 클라이언트 코드로 가져오면 타입 안전한 HTTP 클라이언트가 자동으로 생성된다.

```typescript
// 클라이언트 코드 (프론트엔드 또는 다른 서비스)
import { hc } from 'hono/client'
import type { AppType } from './server'  // 타입만 가져옴 — 런타임 코드 없음

const client = hc<AppType>('http://localhost:3000')

// 이 시점에서 타입 추론이 완전히 동작함
const response = await client.users[':id'].$get({
    param: { id: '123' },
})

const data = await response.json()
// data의 타입: { id: string, name: string }
// ↑ 서버의 c.json({ id, name }) 반환 타입에서 자동 유도됨

// 존재하지 않는 라우트를 쓰면 컴파일 에러
const wrong = await client.posts.$get()  // ← 에러: 'posts' 라우트 없음
```

이게 왜 새로운가? 기존의 REST API 연동 방식을 생각해보자. 서버에서 API 스펙을 OpenAPI로 뽑고, 클라이언트에서 그 스펙을 바탕으로 SDK를 생성하거나 직접 타입을 작성한다. 서버가 응답 타입을 바꾸면 클라이언트도 직접 수정해야 한다. 그 간극에서 버그가 난다.

Hono의 RPC 모델은 그 간극을 없앤다. 서버와 클라이언트가 같은 타입 정보를 공유하기 때문에, 서버에서 응답 타입이 바뀌면 클라이언트에서 즉시 컴파일 에러가 난다. 타입이 계약이 되는 순간이다.

---

📚 **Java/Kotlin 시선 ⑤ — Spring WebFlux ↔ Hono async**

```java
// Spring WebFlux — Reactor 기반 비동기
@RestController
@RequestMapping("/users")
public class UserController {

    @GetMapping("/{id}")
    public Mono<UserDto> getUser(@PathVariable String id) {
        return userService.findById(id)
            .map(user -> new UserDto(user.getId(), user.getName()));
    }
}
```

```typescript
// Hono — async/await 기반, Web Standards Fetch API
app.get('/users/:id', async (c) => {
    const id = c.req.param('id')
    const user = await userService.findById(id)
    return c.json({ id: user.id, name: user.name })
})

// c.req, c.res가 Web Standards의 Request, Response를 따름
// Spring의 ServerRequest/ServerResponse와 개념은 비슷하지만
// Web Standards이므로 Cloudflare Workers, Deno, Bun에서도 동일하게 동작함
```

Spring WebFlux는 Reactor(`Mono`/`Flux`) 위에서, Hono는 표준 Promise 위에서 비동기를 처리한다. 두 모델 모두 비동기 요청을 블로킹 없이 처리하지만, 표현 방식이 다르다. Hono의 `async/await`는 Kotlin coroutine의 `suspend`와 표면적으로 가깝다 — 동기 코드처럼 읽힌다.

핵심 차이는 **Web Standards 기반**이다. Hono의 `c.req`는 Web Standards `Request` 객체, `c.res`는 `Response` 객체다. 이 표준은 브라우저·Node.js·Bun·Deno·Cloudflare Workers에서 동일하다. 코드 한 벌을 여러 런타임에 배포할 수 있다는 뜻이다.

---

### 전 런타임 동작 — Adapter 모델

Hono가 "Web Standards 기반"을 강조하는 이유가 여기 있다. Node.js의 `http` 모듈 API, Bun의 내장 서버 API, Cloudflare Workers의 실행 환경은 각각 다르다. 하지만 모두 Web Standards의 `Request`/`Response`를 지원한다. Hono는 이 공통 분모 위에 서 있기 때문에 런타임마다 어댑터 한 줄만 바꾸면 된다.

```typescript
// Node.js
import { serve } from '@hono/node-server'
serve({ fetch: app.fetch, port: 3000 })

// Bun
export default app  // Bun이 fetch 핸들러를 자동 인식

// Cloudflare Workers
export default app  // Workers 환경에서 동일하게 동작

// Deno
Deno.serve(app.fetch)
```

서버 코드 자체(`app.get(...)` 부분)는 바뀌지 않는다. 이 패턴은 Spring Boot가 내장 톰캣·제티·언더토우를 바꾸는 방식과 비슷하게 느껴지지만, 실제로는 더 가볍다 — 프레임워크가 플랫폼 추상화 계층 없이 표준 API 위에 바로 서 있기 때문이다.

### tRPC와의 차이점

Hono RPC와 tRPC를 비교하는 질문이 자주 나온다. 두 가지 모두 타입 안전한 API를 만드는 도구지만 철학이 다르다.

| | Hono RPC | tRPC |
|---|---|---|
| 전송 방식 | 표준 HTTP (GET, POST, DELETE...) | HTTP POST 기반 (또는 WebSocket) |
| REST 호환 | 완전 호환 — OpenAPI 스펙 자동 생성 가능 | REST가 아님 — tRPC 클라이언트 필요 |
| 적합한 상황 | 외부 공개 API, 모바일 클라이언트 있는 경우 | 동일 타입 코드베이스 내 웹 풀스택 |
| 런타임 | Web Standards 기반 전 런타임 | Node.js 중심 |
| 학습 곡선 | 낮음 (일반 라우터와 비슷) | 중간 (procedure, router 개념 필요) |

외부에 API를 열어야 하거나 모바일 클라이언트가 있다면 Hono RPC가 낫다 — REST 호환이기 때문이다. 단일 Next.js 풀스택 앱에서 프론트엔드와 백엔드만 연결한다면 tRPC가 더 자연스럽다. T3 스택이 tRPC를 기본 선택으로 두는 이유다.

---

## Express + Fastify — 여전히 현장의 표준

### Express: 왜 여전히 1위인가

JetBrains Developer Ecosystem 2024 기준으로 Node.js 백엔드 프레임워크 점유에서 Express가 여전히 1위다. 2010년에 나온 프레임워크가 2025년에도 1위라는 것이 어떤 의미인가.

답은 관성이 아니라 신뢰다. Express는 수천만 개의 npm 패키지가 "Express 미들웨어"로 만들어져 있다. 새 인증 라이브러리, 새 파일 업로드 라이브러리, 새 로깅 솔루션 — 대부분이 Express 미들웨어를 먼저 만든다. 이 생태계 규모는 단기간에 따라잡기 어렵다.

Express 자체는 매우 미니멀하다. 라우팅, 미들웨어 체인, 요청/응답 객체. 그 이상은 직접 선택한다.

```typescript
import express from 'express'
import { Request, Response, NextFunction } from 'express'

const app = express()
app.use(express.json())

// 기본 라우트 — 타입 추론이 제한적
app.get('/users/:id', async (req: Request, res: Response) => {
    const id = req.params.id  // string
    // req.params, req.query, req.body 모두 타입이 느슨하다
    // 이 느슨함이 Express TS 사용의 찜찜한 자리
    const user = await findUser(id)
    res.json(user)
})

// 미들웨어 패턴
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
    console.error(err.stack)
    res.status(500).json({ message: err.message })
})

app.listen(3000)
```

Express의 TS 지원에서 찜찜한 부분이 있다. `req.body`는 기본적으로 `any`다. `req.params`는 `string` 딕셔너리지만, 라우트 URL에 정의한 파라미터 이름과 연결되지 않는다. 이 느슨함을 보완하려면 제네릭을 명시하거나, zod로 검증하거나, 별도의 미들웨어 레이어를 만들어야 한다.

```typescript
// 타입을 조금 더 안전하게 쓰는 패턴
import { z } from 'zod'

const userParamSchema = z.object({ id: z.string() })
const createUserSchema = z.object({
    name: z.string(),
    email: z.string().email(),
})

app.post('/users', async (req: Request, res: Response) => {
    const body = createUserSchema.parse(req.body)
    // 이제 body가 { name: string, email: string }으로 좁혀짐
    const user = await createUser(body)
    res.status(201).json(user)
})
```

Express 4.x는 오랫동안 유지보수 중이었고, 2024년에 Express 5.x가 정식 릴리즈됐다. Promise 기반 라우터, 비동기 에러 핸들러 자동 처리 등이 개선됐지만, 큰 아키텍처 변화는 없다.

### Fastify: Express의 후계자 지위

Fastify는 Express의 느슨한 타입과 성능 문제를 직접 겨냥하며 설계됐다. Node.js 코어 팀원인 Matteo Collina가 주도하며 만든 이 프레임워크는 두 가지 방향에서 Express보다 강하다.

**첫째, JSON Schema 기반 검증과 직렬화.** Fastify는 라우트 스키마를 JSON Schema로 정의하면 요청 검증과 응답 직렬화를 동시에 처리한다. 응답 직렬화를 스키마 기반으로 하기 때문에 JSON 생성 성능이 크게 좋다.

```typescript
import Fastify from 'fastify'
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'
import { Type } from '@sinclair/typebox'

const fastify = Fastify().withTypeProvider<TypeBoxTypeProvider>()

fastify.get('/users/:id', {
    schema: {
        params: Type.Object({ id: Type.String() }),
        response: {
            200: Type.Object({
                id: Type.String(),
                name: Type.String(),
                email: Type.String(),
            }),
        },
    },
}, async (request, reply) => {
    const { id } = request.params
    // id가 string으로 정확히 추론됨 — TypeBox 스키마에서 유도
    const user = await findUser(id)
    return user  // 응답 스키마에 맞게 직렬화됨
})
```

TypeBox를 쓰면 JSON Schema와 TS 타입을 동시에 정의할 수 있다. 검증·직렬화·타입 추론이 단일 소스에서 나온다. 이 패턴은 zod + Hono의 방향과 비슷하지만, Fastify는 표준 JSON Schema를 기반으로 해서 OpenAPI 스펙 자동 생성이 더 자연스럽다.

**둘째, 플러그인 시스템.** Fastify의 플러그인은 캡슐화된 스코프를 가진다. Express의 `app.use()`가 전역 미들웨어를 쌓는 방식과 달리, Fastify 플러그인은 자신의 스코프에서만 동작하는 데코레이터·훅·플러그인을 등록할 수 있다. NestJS의 모듈과 비슷한 캡슐화 개념이다.

두 프레임워크를 어떻게 고르는가. 기존 Express 생태계(미들웨어, 레거시 코드)와의 호환이 최우선이라면 Express를 유지하는 편이 낫다. 새 프로젝트이고 타입 안전과 성능이 중요하다면 Fastify가 더 나은 선택이다. NestJS는 Fastify를 HTTP 어댑터로 쓸 수 있다 — `@nestjs/platform-fastify`로 바꾸면 NestJS의 DI·모듈 체계를 유지하면서 Fastify의 성능을 얻는다.

---

📚 **Java/Kotlin 시선 ④ — Bean Validation `@Valid` ↔ zod**

```java
// Spring — 클래스 필드에 어노테이션으로 검증 규칙 선언
public class CreateUserRequest {
    @NotBlank
    @Size(max = 100)
    private String name;

    @Email
    @NotNull
    private String email;

    @Min(0) @Max(150)
    private int age;
}

@PostMapping("/users")
public ResponseEntity<UserDto> createUser(
    @RequestBody @Valid CreateUserRequest req,
    BindingResult result
) {
    if (result.hasErrors()) {
        throw new ValidationException(result.getAllErrors());
    }
    ...
}
```

```typescript
// TS — zod 스키마가 타입 정의와 검증 규칙을 동시에 표현
import { z } from 'zod'

const createUserSchema = z.object({
    name: z.string().min(1).max(100),
    email: z.string().email(),
    age: z.number().int().min(0).max(150),
})

type CreateUserRequest = z.infer<typeof createUserSchema>
// { name: string, email: string, age: number }

// Express에서 직접 검증
app.post('/users', async (req, res) => {
    const result = createUserSchema.safeParse(req.body)
    if (!result.success) {
        return res.status(400).json({ errors: result.error.flatten() })
    }
    const user = await createUser(result.data)
    res.status(201).json(user)
})
```

Bean Validation은 클래스에 검증 어노테이션을 달고 Spring이 런타임에 실행한다 — 런타임 메타데이터 의존이다. zod는 스키마 객체를 직접 호출하는 방식이다. `z.infer<typeof schema>`가 타입을 유도하는 것이 5장의 조건부 타입이 현실에서 쓰이는 핵심 사례다. NestJS에서는 `class-validator`와 `class-transformer`로 Spring과 더 비슷한 패턴을 쓸 수 있지만, 커뮤니티의 방향은 zod 쪽으로 기울고 있다.

---

## 풀스택 메타프레임워크 — 철학의 지형도

### Next.js와 RSC — 서버가 돌아온다

Next.js App Router와 React Server Components(RSC)의 등장은 "프론트엔드와 백엔드의 경계"라는 오래된 구분을 다시 흔들고 있다. 어떻게?

기존 SPA 모델을 생각해보자. 프론트엔드는 정적 파일로 배포하고, 백엔드 API를 호출해 데이터를 가져온다. BFF(Backend for Frontend) 패턴이 필요해지면 별도 서버를 두거나 API Gateway를 끼워 넣는다.

Next.js App Router에서는 컴포넌트 자체가 서버에서 실행될 수 있다.

```typescript
// app/users/[id]/page.tsx — 서버 컴포넌트 (기본)
// 이 파일은 서버에서 실행됨 — DB 직접 호출 가능
async function UserPage({ params }: { params: { id: string } }) {
    // DB를 직접 호출한다 — API 레이어 없음
    const user = await db.user.findUnique({
        where: { id: params.id },
    })

    if (!user) notFound()

    return (
        <div>
            <h1>{user.name}</h1>
            <p>{user.email}</p>
        </div>
    )
}
```

```typescript
// app/users/[id]/actions.ts — Server Action
'use server'  // 이 지시어가 있으면 서버에서만 실행됨

export async function updateUser(id: string, data: UpdateUserData) {
    // 폼 제출 → 서버 함수 직접 호출 — fetch 없음
    await db.user.update({ where: { id }, data })
    revalidatePath(`/users/${id}`)
}

// 클라이언트 컴포넌트에서 사용
'use client'
import { updateUser } from './actions'

function EditUserForm({ userId }: { userId: string }) {
    return (
        <form action={updateUser.bind(null, userId)}>
            {/* 폼이 서버 함수를 직접 호출 */}
        </form>
    )
}
```

Server Actions는 PHP의 `<form action="process.php">`와 비슷하게 느껴지기도 한다. 실제로 Dan Abramov는 "서버 우선 개발의 부활"이라고 표현했다. 이 방식이 BFF를 사라지게 만드는가?

단일 웹 클라이언트만 있는 서비스라면 Next.js 풀스택으로 BFF를 대체할 수 있다. 그러나 모바일 앱이 있거나, 파트너 API를 열어야 하거나, 여러 클라이언트가 같은 API를 써야 한다면 여전히 별도 API 서버가 필요하다. 풀스택 메타프레임워크는 "웹 한정"의 해법이다 — 이 제약을 인지하고 선택하는 편이 낫다.

### React Router 7 (구 Remix) — Web Standards의 길

React Router 7은 Remix가 React Router와 통합되면서 나온 메타프레임워크다. Next.js와 다른 철학을 가진다.

| | Next.js App Router | React Router 7 |
|---|---|---|
| 데이터 패턴 | Server Components + Server Actions | loader/action 패턴 |
| 표준 준수 | React 전용 (RSC) | Web Standards (FormData, Response) |
| 서버 렌더링 | RSC 우선 | SSR/SSG 선택 |
| 데이터 뮤테이션 | Server Actions | `action` 함수 |
| 캐싱 전략 | 복잡 (세 종류) | 단순 |

React Router 7의 loader/action 패턴은 Web Standards(`Request`, `Response`, `FormData`)를 직접 다루기 때문에, 브라우저 폼의 동작 방식에 충실하다. Spring MVC의 controller 메서드가 `HttpServletRequest`를 직접 다루는 방식과 닮았다.

```typescript
// React Router 7 — route loader
export async function loader({ params }: LoaderFunctionArgs) {
    const user = await db.user.findUnique({
        where: { id: params.id },
    })
    if (!user) throw new Response('Not Found', { status: 404 })
    return { user }
}

// route action — 폼 제출 처리
export async function action({ request, params }: ActionFunctionArgs) {
    const formData = await request.formData()
    const name = formData.get('name') as string
    await db.user.update({
        where: { id: params.id },
        data: { name },
    })
    return redirect(`/users/${params.id}`)
}
```

### SvelteKit · Solid Start — 다른 reactivity의 풀스택

SvelteKit은 Svelte의 컴파일 타임 reactivity 위에 서버 렌더링·파일 기반 라우팅·폼 액션을 얹는다. 코드가 간결하고 번들이 작다는 것이 강점이다. Solid Start는 fine-grained reactivity(signal 기반) 위의 풀스택이다. 한국 시장에서 두 프레임워크의 비중은 아직 높지 않다 — 업무에서 만날 확률이 낮다. 하지만 기술적 방향의 다양성을 파악하는 차원에서 인지하는 것이 낫다.

### Astro — 콘텐츠 사이트 풀스택의 자리

Astro는 12장에서 잠깐 언급되었지만, 여기 13장이 더 자연스러운 자리다. Astro의 핵심 개념인 Islands Architecture는 reactivity 모델이 아니라 **콘텐츠 사이트 풀스택 hydration 전략**이기 때문이다.

아이디어는 단순하다. 콘텐츠 중심 사이트(블로그, 문서, 마케팅 페이지)의 대부분은 정적 HTML로 충분하다. 인터랙티브한 부분은 극히 일부 — 검색 바, 댓글 폼, 슬라이더. Islands Architecture는 이 "극히 일부"에만 JS를 hydrate하고, 나머지는 정적 HTML로 낸다.

```astro
---
// Astro 컴포넌트 — 서버에서만 실행되는 부분
import { getPost } from '../lib/posts'
const post = await getPost(Astro.params.slug)
---

<html>
<body>
    <!-- 정적 콘텐츠 — JS 없음 -->
    <h1>{post.title}</h1>
    <article>{post.content}</article>

    <!-- 인터랙티브 섬(Island) — React 컴포넌트를 hydrate -->
    <CommentForm client:load postId={post.id} />
    {/*         ↑ client:load로 이 컴포넌트만 JS를 실행 */}
</body>
</html>
```

Astro는 React, Vue, Svelte, Solid 컴포넌트를 동시에 섞어 쓸 수 있다. 다양한 라이브러리의 컴포넌트를 하나의 페이지에서 쓸 수 있는 "프레임워크 불가지론자"다.

어떤 상황에서 Astro를 쓰는가. 콘텐츠가 주인공이고 인터랙션이 보조인 사이트 — 기술 문서, 블로그, 마케팅 사이트, 전자상거래 상품 페이지. Next.js나 React Router는 SPA를 서버에서 렌더링하는 방향이라면, Astro는 "기본이 정적"인 방향이다. 성격이 다른 도구를 비교하는 것은 큰 의미가 없다.

---

### T3 스택 — 타입 안전 모노레포의 사실상 표준

T3 스택은 공식 프레임워크가 아니라, Theo Browne이 정착시킨 실전 조합이다. Next.js + tRPC + Prisma + Tailwind + zod. 이 다섯 도구가 함께 쓰일 때 어떻게 타입이 흐르는지를 보면 13장 전체 주제와 연결된다.

```
[데이터베이스] → Prisma 스키마
    → Prisma Client 타입 자동 생성
    → tRPC router에서 사용
    → tRPC client에서 자동 추론
    → React 컴포넌트에서 타입 안전하게 사용
    → zod로 입력 검증
    → Tailwind로 스타일
```

각 레이어의 타입이 다음 레이어로 자동으로 흐른다. 어느 레이어에서도 타입을 손으로 다시 정의하지 않는다. 이것이 T3 스택의 핵심 가치다.

```bash
# create-t3-app으로 프로젝트 생성
npm create t3-app@latest

# 생성되는 구조
├── src/
│   ├── server/
│   │   ├── api/
│   │   │   └── routers/
│   │   │       └── user.ts    # tRPC router
│   │   └── db.ts              # Prisma client
│   ├── app/
│   │   └── ...                # Next.js App Router
│   └── trpc/
│       ├── client.tsx         # tRPC client (자동 타입 추론)
│       └── server.ts          # tRPC server
```

```typescript
// server/api/routers/user.ts — tRPC router
export const userRouter = createTRPCRouter({
    getById: publicProcedure
        .input(z.object({ id: z.string() }))
        .query(async ({ input, ctx }) => {
            return ctx.db.user.findUnique({
                where: { id: input.id },
            })
        }),
    create: protectedProcedure
        .input(z.object({
            name: z.string().min(1),
            email: z.string().email(),
        }))
        .mutation(async ({ input, ctx }) => {
            return ctx.db.user.create({ data: input })
        }),
})

// 클라이언트 컴포넌트에서 — 타입이 자동 추론됨
const { data: user } = api.user.getById.useQuery({ id: '123' })
// user: Prisma의 User 타입 | null | undefined — 자동 추론
```

한국의 신생 스타트업과 핀테크 팀 사이에서 T3 스택 채택 사례가 늘고 있다. 빠른 개발 속도와 타입 안전성을 동시에 챙기고 싶은 팀에게 합리적인 시작점이다.

---

## ORM — 데이터베이스와 타입의 경계

### Prisma, Drizzle, TypeORM의 세 길

ORM을 선택하는 것은 데이터베이스를 TS와 어떻게 연결할지의 철학을 선택하는 것이다.

---

📚 **Java/Kotlin 시선 ③ — JPA `@Entity` ↔ Prisma schema**

```java
// JPA — 클래스와 어노테이션으로 엔티티 정의
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(unique = true, nullable = false)
    private String email;

    @OneToMany(mappedBy = "user", fetch = FetchType.LAZY)
    private List<Post> posts;
}
```

```prisma
// Prisma — 스키마 파일에서 모델 정의
model User {
    id    String  @id @default(cuid())
    name  String  @db.VarChar(100)
    email String  @unique

    posts Post[]

    createdAt DateTime @default(now())
    updatedAt DateTime @updatedAt
}
```

```typescript
// 스키마에서 자동 생성되는 Prisma Client 사용
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// 쿼리 — 반환 타입이 자동 추론됨
const user = await prisma.user.findUnique({
    where: { id: userId },
    include: { posts: true },
})
// user: (User & { posts: Post[] }) | null — 자동 추론

// 생성
const newUser = await prisma.user.create({
    data: { name: '홍길동', email: 'hong@example.com' },
})
```

JPA는 Java 클래스가 엔티티 정의이자 ORM 매핑이다. Prisma는 별도 스키마 파일(`schema.prisma`)이 소스이고, 거기서 TS 타입과 DB 마이그레이션 파일이 자동 생성된다. "스키마가 단일 진실의 원천"이라는 원칙이 있다. JPA의 `@Column(nullable = false)` ↔ Prisma의 `name  String` (nullable이면 `String?`). JPA의 `@OneToMany` ↔ Prisma의 `posts Post[]`.

---

**Drizzle — 타입-퍼스트 ORM**

Drizzle은 Prisma와 다른 방향에서 설계됐다. 스키마를 TypeScript 코드로 정의한다 — 별도 스키마 파일이 없다.

```typescript
// Drizzle — 스키마를 TS 코드로 정의
import { pgTable, serial, varchar, text, timestamp } from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
    id: serial('id').primaryKey(),
    name: varchar('name', { length: 100 }).notNull(),
    email: text('email').notNull().unique(),
    createdAt: timestamp('created_at').defaultNow(),
})

// 쿼리 — SQL에 가까운 문법
const result = await db
    .select({
        id: users.id,
        name: users.name,
    })
    .from(users)
    .where(eq(users.email, 'hong@example.com'))
    .limit(1)

// result: { id: number, name: string }[] — 선택한 필드만 추론
```

Drizzle의 강점은 타입 추론이 선택한 컬럼에만 정확히 적용된다는 것이다. `select({ id: users.id, name: users.name })`이면 반환 타입에 `email`이 없다. Prisma에서 `select`를 명시하면 비슷한 결과를 얻지만, 문법이 덜 직관적이다.

또 다른 강점: SQL과 가까운 문법이다. Spring Data JPA의 JPQL보다 원시 SQL에 더 가깝다. ORM의 추상화 레이어를 얇게 유지하고 싶거나, 복잡한 쿼리를 TS로 표현하고 싶을 때 Drizzle이 낫다.

**TypeORM — 자바스러운, 그러나 레거시의 그늘**

TypeORM은 Java의 JPA에 가장 가깝다. 클래스에 `@Entity`, `@Column`, `@ManyToOne`을 달고, 리포지토리 패턴으로 쿼리한다.

```typescript
// TypeORM — JPA와 구조가 비슷
@Entity('users')
export class User {
    @PrimaryGeneratedColumn('uuid')
    id: string

    @Column({ length: 100 })
    name: string

    @Column({ unique: true })
    email: string

    @OneToMany(() => Post, post => post.user)
    posts: Post[]
}

// 리포지토리 패턴
const userRepository = dataSource.getRepository(User)
const user = await userRepository.findOne({
    where: { id: userId },
    relations: ['posts'],
})
```

Spring 경험자에게 TypeORM이 가장 친숙하다. 그러나 TypeORM은 NestJS와 마찬가지로 legacy 데코레이터에 의존한다. 그리고 활발한 개발이 예전만 못하다는 커뮤니티의 평이 있다 — 이슈가 오래 방치되거나 PR이 느리게 머지되는 경우가 많다. 새 프로젝트라면 Prisma나 Drizzle을 먼저 고려하는 편이 낫다. 기존 TypeORM 코드베이스가 있다면 유지하는 것이 합리적이다.

---

## 두 철학의 비교 — 어떤 팀에 어떤 선택인가

이 챕터를 마무리하기 전에, 두 가지 근본적으로 다른 철학을 한 단락으로 정리해두자.

**데코레이터 메타데이터 진영** (NestJS, TypeORM, class-validator, InversifyJS): 클래스와 데코레이터로 의도를 선언하고, 런타임에 메타데이터를 읽어 동작한다. Spring에서 온 사람에게 자연스럽다. 엔터프라이즈 패턴(DI, AOP, Exception 계층)이 표준으로 제공된다. 단점은 legacy 데코레이터 의존과 `reflect-metadata`, 그리고 무거운 추상화 레이어다.

**Web Standards 진영** (Hono, Fastify, Remix, zod, Drizzle): 표준 API(`Request`, `Response`, `FormData`)와 타입 추론에 기댄다. 런타임 메타데이터가 없고, 타입이 컴파일타임에만 살아있다. TS의 본성과 정합하고, 여러 런타임에서 동작한다. 단점은 엔터프라이즈 패턴을 스스로 조립해야 한다는 것이다.

어떤 팀에 어떤 선택이 맞는가. 몇 가지 질문으로 좁혀보자.

- **팀원 대부분이 Spring 경험자고 빠른 온보딩이 우선인가?** → NestJS. 학습 곡선이 가장 짧다.
- **외부 공개 API, 모바일 클라이언트, 다중 클라이언트가 있는가?** → Express/Fastify/Hono + 분리된 API. Next.js 풀스택은 적합하지 않다.
- **단일 웹 앱, 빠른 MVP, 타입 안전 모노레포가 필요한가?** → T3 스택(Next + tRPC + Prisma). 타입이 DB에서 UI까지 흐른다.
- **Cloudflare Workers, Deno, Bun 같은 Edge 환경을 고려하는가?** → Hono. 전 런타임에서 동작한다.
- **마이크로서비스, 이벤트 기반, 큰 엔터프라이즈 아키텍처인가?** → NestJS가 가장 성숙한 생태계를 제공한다.

---

💡 **작가의 한 마디 — 풀스택은 답이 아니라 선택지다**

Next.js App Router와 Server Actions의 등장 이후 "풀스택이 답"이라는 분위기가 생겼다. 하지만 모바일 앱이 있는 회사, 파트너 API를 열어야 하는 서비스, 여러 팀이 각자의 클라이언트를 만드는 조직에서는 여전히 백엔드와 프론트엔드의 분리가 정답이다.

풀스택 메타프레임워크는 "웹 한정"의 해법이다. 그 제약을 인지하고 선택하는 것과, 유행에 따라 선택하는 것 사이에는 큰 차이가 있다. 지금 팀이 만드는 제품이 웹만 있는가, 아니면 앞으로 모바일이 들어올 가능성이 있는가 — 이 질문 하나만 제대로 해도 아키텍처 선택이 훨씬 명확해진다.

---

## 데이터 검증 경계 — 짧게

zod와 valibot에 대해서는 5장과 12장에서 이미 깊게 다뤘다. 여기서는 백엔드 맥락에서 한 줄만 짚는다.

외부에서 들어오는 모든 데이터 — API 요청 바디, URL 쿼리 파라미터, 환경 변수, 외부 API 응답 — 는 런타임 검증이 필요하다. 내부 코드끼리의 타입 신뢰는 `as`나 타입 단언 없이도 가능하지만, 외부 경계를 넘어오는 데이터는 TS 컴파일러가 보장할 수 없다. 이것이 논쟁 D(타입 단언 vs zod)의 사실상 합의다 — "외부 경계만 검증한다."

valibot은 zod와 비슷한 스키마 API를 갖지만 번들 크기가 훨씬 작다(트리 쉐이킹 친화). Edge 환경이나 번들 크기가 민감한 Cloudflare Workers에서는 valibot이 낫다.

---

## 마무리

Spring 베테랑이 이 챕터를 읽고 가져갈 것이 두 가지 있다.

하나는 NestJS에 대한 자신감이다. 모양이 비슷하다는 것은 진짜다. 그리고 다른 자리들 — 모듈 명시 등록, module re-export, Provider 스코프, Guard/Pipe/Filter의 분리 — 도 이제 예상 가능한 자리가 됐다. 헷갈릴 때 이 챕터의 다섯 가지 함정으로 돌아오자.

다른 하나는 Hono와 Web Standards 진영의 방향이다. 타입이 라우트 정의에서 클라이언트까지 자동으로 흐르는 것이 어떻게 가능한지 — 5장에서 배운 타입 마법이 현실 코드에서 어떻게 살아나는지 — 를 눈으로 봤다. 이 방향이 앞으로 Node.js 백엔드 생태계에서 더 넓어질 가능성이 높다.

프레임워크는 많고 선택은 어렵다. 하지만 선택의 기준 — 팀의 배경, 클라이언트의 다양성, 런타임 환경 — 이 명확하면 선택이 명확해진다. 도구를 고르는 사람이 도구에 휘둘리지 않는다.

---

📖 **더 깊이 가려면**

- **NestJS 공식 문서** (docs.nestjs.com): 모듈 체계와 DI, Guard/Pipe/Filter 상세 설명. "Fundamentals" 섹션은 Spring 경험자에게 가장 유용하다.
- **Hono 공식 문서** (hono.dev): RPC 섹션과 `hc` 클라이언트 사용법. Cloudflare Workers 배포 가이드.
- **Total TypeScript** (Matt Pocock): Hono의 타입 추론 내부 작동 방식을 파헤치는 글들. Hono 소스를 따라가며 5장의 타입 도구들이 어떻게 조합되는지 볼 수 있다.
- **Prisma 공식 문서** (prisma.io): 스키마 정의, 마이그레이션, 타입 추론 패턴.
- **T3 Stack 문서** (create.t3.gg): T3 스택의 각 컴포넌트 선택 이유와 통합 패턴.
- **이동욱(향로) 기술블로그** (jojoldu.tistory.com): NestJS와 Spring의 차이를 한국어로 가장 잘 정리한 자료 중 하나.
- **라인·쿠팡 NestJS 도입 사례** (각사 기술블로그): Spring 조직이 NestJS를 도입할 때의 실제 결정 과정과 함정.

→ **14장에서는 NestJS·Hono·tRPC의 *타입 수준 계약 테스트*와 *Playwright E2E*를 자세히 다룬다.** 이 챕터에서 만든 라우터와 서비스 코드가 어떻게 Vitest로 검증되는지, RPC 클라이언트의 타입이 E2E 시나리오와 어떻게 연결되는지 — 테스트와 타입이 만나는 자리다.
