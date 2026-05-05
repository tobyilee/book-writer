# 6장. Workers 본격 사용법 — Spring 멘탈을 Hono로 다시 그리자

처음 Worker를 띄운 다음 날 아침을 떠올려 보자. 3장에서 `wrangler deploy` 한 번에 글로벌 PoP에 코드가 깔리는 순간을 손끝으로 느꼈고, 5장에서 자기 시스템 컴포넌트 8개를 결정 워크시트에 채워 "이건 Move now"라고 표시했다. 그래서 다음 한 시간 안에 그 첫 컴포넌트를 옮기려고 IDE를 연다. 그런데 빈 화면 앞에 앉으면 이상한 일이 생긴다. *분명 익숙한 자리인데 손이 어디로 가야 할지 모르겠다.*

`@RestController`는 어디에 적나. `@Component`로 주입하던 `UserService`는 어디에 둬야 하나. `SecurityFilterChain`을 매개로 인증·인가를 한 줄에 그리던 그 익숙한 빈 등록은 누가 대신 해주나. 5축 결정 트리는 손에 쥐었는데, 정작 한 라우트에 인증·로깅·에러 처리·DB 조회를 어떻게 늘어놓을지 빈 `index.ts` 한 장이 답을 안 해준다.

이 장에서 손에 쥐고 가야 할 건 그 빈 화면을 채우는 다섯 도구다. 라우팅, 미들웨어, 의존성 주입, 시크릿·환경 분리, 테스트. Spring 개발자가 이미 갖고 있는 다섯 도구를 Workers + Hono 환경에서 *어떤 모양으로 다시 그릴지* 한 번에 풀어 보자. 단, 한 가지 약속을 먼저 하자 — Spring을 잊으라고 하지 않는다. *익숙한 자리에 다른 도구를 끼워 맞춰 보는 것뿐*이다. JPA의 `@Transactional`이 KV·D1·DO에서 어떻게 다시 짜이는지는 7장으로 미루고, 여기서는 한 Worker 안의 골격을 끝까지 깔아 보자.

자, 첫 도구부터 살펴보자.

## fetch(request, env, ctx) — Workers의 본질 진입점

Workers 코드의 진짜 출발점은 한 함수다. `export default { fetch(request, env, ctx) { ... } }`. 이게 전부다. `request`는 표준 Web `Request`, `env`는 `wrangler.toml`이 주입한 바인딩 객체, `ctx`는 `ctx.waitUntil()`로 응답 후 작업을 등록할 수 있는 컨텍스트다. Spring Boot가 `DispatcherServlet`을 띄우고 그 위에 `@RestController`를 얹는 것과 비교하면, *Workers는 컨테이너 자체가 없다*. 컨테이너 없이 한 함수가 요청을 받아 응답을 만든다. 이게 5ms 콜드스타트의 비밀이다. 띄울 게 없으니 띄우는 시간도 없다.

이 본질을 잊지 말자. 이 책 내내 Hono를 쓸 텐데, Hono는 `fetch(request, env, ctx)` 위에 라우팅·미들웨어 한 겹을 얹은 *얇은 라이브러리*일 뿐이다. Spring처럼 풀스택 프레임워크가 아니다. 모든 게 결국 `fetch` 한 함수로 수렴한다는 사실을 기억해두자. 이상한 동작을 디버깅할 때 이 본질로 한 번 내려가 보면 보통 답이 나온다.

```ts
// 가장 본질적인 형태
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return new Response("hello edge");
  },
};
```

이 위에 라우팅을 얹으면 우리가 손에 익은 모양이 나타난다. 그게 Hono다.

## Hono — Express에 가까운 라우팅 DSL

Hono는 일본 개발자 Yusuke Wada가 만든 작은 웹 프레임워크다. Cloudflare Workers·Bun·Deno·Node 어디서든 도는데, 출발점이 Workers였던 만큼 V8 isolate 환경에서 가장 자연스럽다. Express를 써본 사람이라면 30초 만에 손에 붙는다. 5장 결정 워크시트의 2번 항목 *상품 검색 API* 를 한번 옮겨보자.

```ts
// apps/api/src/index.ts
import { Hono } from "hono";

type Bindings = {
  CACHE: KVNamespace;
  DB: D1Database;
  JWT_SECRET: string;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get("/", (c) => c.text("toby-shop API"));

app.get("/products/:id", async (c) => {
  const id = c.req.param("id");
  // 캐시 먼저
  const cached = await c.env.CACHE.get(`product:${id}`, "json");
  if (cached) return c.json(cached);

  // 캐시 미스 → D1
  const row = await c.env.DB
    .prepare("SELECT * FROM products WHERE id = ?")
    .bind(id)
    .first();
  if (!row) return c.notFound();

  c.executionCtx.waitUntil(
    c.env.CACHE.put(`product:${id}`, JSON.stringify(row), { expirationTtl: 300 })
  );
  return c.json(row);
});

export default app;
```

아주 짧지만 이 안에 6개의 작은 결정이 들어 있다. `Hono<{ Bindings }>`로 타입 파라미터를 넘기면 `c.env.CACHE` 같은 접근에 자동완성이 붙는다. `c.req.param("id")`는 path param. `c.env.CACHE.get(...)`은 KV 호출. `c.executionCtx.waitUntil(...)`은 응답을 보낸 뒤 백그라운드로 캐시 쓰기를 마무리하라는 약속 — Lambda의 `context.callbackWaitsForEmptyEventLoop = false`와 비슷한 의도다. 이 한 화면이 *Hono의 거의 전부*다.

Spring MVC와 한 화면씩 마주 놓아 보자.

```java
// Spring Boot — 같은 기능
@RestController
@RequestMapping("/products")
class ProductController {
    private final ProductRepository repo;
    private final CacheManager cache;

    ProductController(ProductRepository repo, CacheManager cache) {
        this.repo = repo;
        this.cache = cache;
    }

    @GetMapping("/{id}")
    @Cacheable(value = "products", key = "#id")
    public Product get(@PathVariable Long id) {
        return repo.findById(id).orElseThrow();
    }
}
```

같은 일을 Spring은 두 어노테이션(`@GetMapping`, `@Cacheable`)으로, Hono는 미들웨어 체인이나 명시적 KV 호출로 표현한다. 문법의 우열은 아니다. 다만 Hono 쪽은 *마법이 적다.* `@Cacheable`이 어떻게 동작하는지 디버깅하려면 Spring AOP·CGLIB·Caffeine을 쪼개야 하지만, Hono의 `c.env.CACHE.get`은 호출 한 줄이라 추적할 게 없다. Spring 개발자에겐 이게 처음엔 *허전하게* 느껴지고, 한 달쯤 지나면 *솔직하게* 느껴진다. 마법이 줄어든 만큼 책임이 늘어난 것 — 그 트레이드오프를 이 장 끝까지 같이 받아들이자.

### 타입 안전한 path / query / body

Hono의 좋은 자리 하나는 validator다. `@hono/zod-validator`를 얹으면 query·body가 컴파일 타임에 잡힌다.

```ts
import { z } from "zod";
import { zValidator } from "@hono/zod-validator";

app.post(
  "/products",
  zValidator("json", z.object({
    name: z.string().min(1),
    price: z.number().int().nonnegative(),
  })),
  async (c) => {
    const body = c.req.valid("json"); // 타입이 좁혀진 채로
    const result = await c.env.DB
      .prepare("INSERT INTO products (name, price) VALUES (?, ?)")
      .bind(body.name, body.price)
      .run();
    return c.json({ id: result.meta.last_row_id }, 201);
  },
);
```

Spring의 `@RequestBody @Valid CreateProductDto dto` + `@NotBlank` 어노테이션 묶음과 같은 자리다. Hono의 zValidator 쪽이 *코드로 명시적*인 게 다르다. 어떤 검증이 어떤 라우트에 어떻게 붙었는지 그 자리에 다 적혀 있다. Spring처럼 어노테이션이 자동으로 해석되는 마법은 없지만, 그 자리에 적혀 있다는 명시성이 운영에서 의외로 큰 장점이 된다. *어디서 무엇이 검증되는지 한 화면에서 보인다.*

## 미들웨어 체인 — SecurityFilterChain을 다시 그리자

Spring Boot에서 인증·로깅·CORS·rate limit을 어떻게 묶는가. `SecurityFilterChain` 빈 한 개에 `HttpSecurity` 빌더로 필터를 줄 세우고, `HandlerInterceptor`로 횡단 관심사를 끼워 넣고, `@RestControllerAdvice`로 예외를 한 자리에 모은다. 세 도구가 세 자리에 흩어져 있다. 한 신참이 들어오면 *이게 어디서 어떻게 호출되는지* 추적하는 데 며칠이 걸린다.

Hono의 미들웨어는 한 자리에 줄 세운다. `app.use()` 한 줄로 끝이다. Express를 써본 사람이라면 정확히 그 모양이고, 안 써본 사람이라도 *함수가 함수를 호출한다*는 가장 단순한 흐름이라 한 화면에 다 보인다.

```ts
import { Hono } from "hono";
import { logger } from "hono/logger";
import { cors } from "hono/cors";
import { jwt } from "hono/jwt";
import type { Context, Next } from "hono";

type Bindings = {
  CACHE: KVNamespace;
  DB: D1Database;
  JWT_SECRET: string;
  RATE_LIMIT: KVNamespace;
};
type Variables = { userId: string };

const app = new Hono<{ Bindings: Bindings; Variables: Variables }>();

// 1. 전역: 로깅 + CORS
app.use("*", logger());
app.use("*", cors({ origin: ["https://toby-shop.com"], credentials: true }));

// 2. /api/* 에만: rate limit
app.use("/api/*", async (c, next) => {
  const ip = c.req.header("CF-Connecting-IP") ?? "unknown";
  const key = `rl:${ip}`;
  const count = parseInt((await c.env.RATE_LIMIT.get(key)) ?? "0", 10);
  if (count > 100) return c.json({ error: "rate limited" }, 429);
  c.executionCtx.waitUntil(
    c.env.RATE_LIMIT.put(key, String(count + 1), { expirationTtl: 60 }),
  );
  await next();
});

// 3. /api/admin/* 에만: JWT 검증
app.use("/api/admin/*", async (c, next) => {
  const middleware = jwt({ secret: c.env.JWT_SECRET });
  return middleware(c, next);
});

// 4. /api/admin/* 에만: 인가 (관리자 권한)
app.use("/api/admin/*", async (c, next) => {
  const payload = c.get("jwtPayload") as { role?: string };
  if (payload.role !== "admin") return c.json({ error: "forbidden" }, 403);
  c.set("userId", (payload as { sub: string }).sub);
  await next();
});

// 5. 라우트
app.get("/api/admin/orders", async (c) => {
  const userId = c.get("userId");
  // ... D1 쿼리
  return c.json({ ok: true, by: userId });
});

// 6. 에러 핸들러 — @RestControllerAdvice 자리
app.onError((err, c) => {
  console.error(err);
  return c.json({ error: "internal" }, 500);
});

app.notFound((c) => c.json({ error: "not found" }, 404));

export default app;
```

이 한 파일이 Spring의 `SecurityFilterChain` + `HandlerInterceptor` + `@RestControllerAdvice` + `Filter` 네 자리에 흩어져 있던 모든 횡단 관심사를 *한 자리에 줄 세운 것*이다. 위에서 아래로 읽으면 라이프사이클이 그대로 흐른다. 매칭된 미들웨어들이 순서대로 실행되고, `next()` 호출 후 코드는 응답이 만들어진 뒤에 실행된다 (Express의 onion 모델 그대로). 이게 처음엔 어색하지만, 사흘이면 손에 붙는다.

Spring `HandlerInterceptor`와 짧게 마주 놓아 보자.

```java
// Spring — 인증 인터셉터
@Component
class AuthInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
        String token = req.getHeader("Authorization");
        if (!isValid(token)) {
            res.setStatus(401);
            return false;
        }
        req.setAttribute("userId", parseUser(token));
        return true;
    }
}

// 등록은 별도 자리
@Configuration
class WebConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new AuthInterceptor()).addPathPatterns("/api/admin/**");
    }
}
```

기능은 정확히 같다. 다만 Spring 쪽은 *인터셉터 클래스 한 개 + 등록 클래스 한 개* 두 자리에 흩어진다. Hono는 한 자리. 어느 쪽이 더 좋다 나쁘다가 아니다 — 큰 팀, 다층 권한, 메서드 단위 보안이 필요한 시스템에는 Spring 모델이 더 안전하다. 작은 API, 빠른 추적, 단일 파일 가독성을 원하는 시스템에는 Hono 모델이 더 *솔직하다*. 5장의 결정 프레임을 한 번 더 떠올리자 — 모든 워크로드가 Workers로 옮겨가는 게 아니다. Spring의 `SecurityFilterChain`이 빛나는 어드민·금융 도메인은 Spring에 두고, edge에서 가벼운 게이트웨이만 Workers + Hono로 까는 *하이브리드*가 흔한 답이다.

### 미들웨어 우선순위 — 위에서 아래로 읽힌다

기억해두자. Hono는 `app.use(path, handler)`를 *등록 순서대로* 실행한다. 그래서 글로벌 로깅·CORS는 가장 위에, 경로별 인증은 그 아래, 라우트 핸들러는 맨 아래에 두는 게 자연스럽다. Spring의 `Filter` order 어노테이션처럼 숫자를 넣어 우선순위를 비틀지 말자. *위에서 아래로 읽히는 코드*가 가장 디버깅하기 쉽다는 사실은 Workers에서도 변함이 없다.

## DI를 다시 그리자 — c.set/c.get과 Bindings, 그리고 정직한 권유

Spring 개발자가 Workers에서 가장 허전해하는 한 자리. *DI 컨테이너가 없다.* `@Component`도, `@Autowired`도, `ApplicationContext`도 없다. 그렇다면 어떻게 의존성을 주입할까. 답은 세 갈래다. *솔직하게 무엇이 권유할 만한지*부터 짚어 보자.

### 갈래 1. Bindings — 런타임이 주입해주는 의존성

가장 먼저, 그리고 *가장 권유할 만한* 자리. `wrangler.toml`에 적은 KV·D1·R2·Queue·Service binding은 사실상 런타임 DI다. 코드에서 `c.env.DB.prepare(...)`로 쓰는 그 `DB`는 `wrangler.toml`이 주입한 D1 핸들이다. Spring의 `@Autowired DataSource`와 *기능적으로 같은 자리*다.

```toml
# wrangler.toml
[[d1_databases]]
binding = "DB"
database_name = "toby-shop"
database_id = "xxxx"

[[kv_namespaces]]
binding = "CACHE"
id = "yyyy"
```

```ts
// 코드는 그냥 c.env.DB / c.env.CACHE 를 쓰면 된다
app.get("/users/:id", async (c) => {
  const row = await c.env.DB.prepare("SELECT * FROM users WHERE id = ?").bind(c.req.param("id")).first();
  return row ? c.json(row) : c.notFound();
});
```

이 자리는 *권유할 필요도 없다.* Workers에서는 이게 기본이고, `wrangler types`가 자동 생성한 `Env` 인터페이스 덕분에 타입까지 안전하다. 처음엔 이걸 DI로 부르기 어색하지만, 한 번 익숙해지면 Spring의 IoC 컨테이너보다 *오히려 더 명확한 의존성 표현*이라는 의견에 동의하는 자신을 발견하게 된다. 무엇이 어디에 주입되는지 `wrangler.toml` 한 파일에 다 적혀 있다.

### 갈래 2. c.set / c.get — 요청 단위 컨텍스트 주입

미들웨어 체인 예제에서 이미 본 패턴이다. 인증 미들웨어가 `c.set("userId", ...)`로 값을 꽂으면, 라우트 핸들러가 `c.get("userId")`로 꺼낸다. Spring의 `RequestContextHolder`나 ThreadLocal과 비슷한 자리다. *요청 단위 의존성*을 표현하는 깔끔한 방법이고, Hono의 타입 시스템(`Variables` 제네릭)이 자동완성까지 받쳐준다.

이 자리도 *권유할 만하다.* 다만 한 함정이 있다. `c.set`에 비즈니스 로직을 너무 많이 꽂으면 라우트 핸들러가 어디서 무엇이 들어왔는지 추적하기 어려워진다. Spring의 ThreadLocal 남용과 똑같은 함정이다. *userId·tenantId·tracerId처럼 진짜 횡단적인 값*만 꽂고, 비즈니스 객체는 함수 인자로 명시적으로 넘기는 편이 낫다.

### 갈래 3. 함수형 DI — 가장 솔직하고 가장 가벼운 패턴

서비스 클래스를 함수로 풀어 헤치고, 의존성을 첫 번째 인자로 명시적으로 받는다. 이게 사실상 *Workers에서 가장 권유할 만한 패턴*이다.

```ts
// packages/shared/src/users.ts
import type { D1Database } from "@cloudflare/workers-types";

export async function getUser(db: D1Database, id: string) {
  return db.prepare("SELECT * FROM users WHERE id = ?").bind(id).first();
}

export async function createUser(db: D1Database, input: { name: string; email: string }) {
  const result = await db
    .prepare("INSERT INTO users (name, email) VALUES (?, ?)")
    .bind(input.name, input.email)
    .run();
  return result.meta.last_row_id;
}
```

```ts
// apps/api/src/routes/users.ts
import { Hono } from "hono";
import { getUser, createUser } from "@toby-shop/shared/users";

const users = new Hono<{ Bindings: Bindings }>();

users.get("/:id", async (c) => {
  const row = await getUser(c.env.DB, c.req.param("id"));
  return row ? c.json(row) : c.notFound();
});

export default users;
```

`UserService` 클래스도, `@Component`도 없다. 그냥 함수 + 명시적 의존성. 테스트 시에는 `getUser(mockDb, "1")`처럼 mock을 그대로 넘기면 된다. Spring 개발자에겐 *너무 단순해 보이는 게 함정*이다. 큰 시스템에서도 정말 이걸로 충분한가 묻고 싶어진다. 솔직히 답하자면, *Workers 한 개에 들어가는 정도의 도메인이라면 충분하다.* Workers는 코드 크기 한도(Free 3MiB / Paid 10MiB)가 있어서 한 Worker에 너무 많은 도메인을 묶을 수 없고, 그래서 *Spring Boot 모놀리스급 복잡도가 한 Worker에 들어올 일 자체가 드물다.* 도메인이 정말 커지면 Worker를 쪼개고 Service Bindings로 잇는다 (다음 챕터들에서 다룬다).

### 갈래 4. awilix·tsyringe 같은 가벼운 컨테이너 — 권유하지 않는다

awilix, tsyringe, InversifyJS 같은 TypeScript DI 컨테이너를 Workers에 얹으면 어떨까. 가능은 하다. 다만 *권유하지 않는다.* 이유 셋.

첫째, Workers는 한 isolate가 여러 요청을 처리한다. 컨테이너가 글로벌 싱글톤이 되면 한 요청의 의존성 상태가 다음 요청에 새는 함정이 생긴다. Spring처럼 RequestScope·SessionScope·SingletonScope를 분리해주는 인프라가 컨테이너 안에 없다. 직접 깔아야 한다.

둘째, Workers의 코드 크기 한도. awilix만 해도 10~30KB 수준이지만 reflect-metadata + tsyringe 조합은 더 무겁다. 큰 의존성에 비해 얻는 게 함수형 DI보다 분명하지 않다.

셋째, *팀 신참이 입사 첫 주에 코드를 읽을 때*. 함수형 DI는 import 한 줄만 따라가면 끝이지만, 컨테이너 등록은 별도 파일·별도 토큰을 추적해야 한다. Spring에서 이미 익숙하지만, Workers의 작은 도메인에 굳이 그 복잡도를 끌어올 이유가 빈약하다.

그래서 권유: *Bindings + c.set/get + 함수형 DI 셋이면 충분하다.* 이 셋으로 안 풀리는 자리가 생기면 그 자리는 보통 "이 도메인은 한 Worker에 너무 많이 들어왔다"는 신호다. Worker를 쪼개라는 신호로 받아들이자. *DI 컨테이너의 부재가 처음엔 결핍 같다가, 나중엔 안내판처럼 보인다.*

## 환경변수와 시크릿 — `.dev.vars`, `wrangler secret put`, `c.env`

다음으로 Spring의 `application-{profile}.yml` + Spring Cloud Config + AWS Secrets Manager 자리. Workers에서는 세 레이어가 한결 단순해진다.

**로컬 개발용은 `.dev.vars`** — gitignore 필수. `.env`와 동시에 쓰지 말자. `.dev.vars`가 있으면 `wrangler dev`가 그걸 읽고 `.env`는 무시한다.

```bash
# .dev.vars (gitignore 됨)
JWT_SECRET=local-only-do-not-deploy
DATABASE_URL=postgresql://localhost/toby_shop_dev
```

**배포 환경의 시크릿은 `wrangler secret put`** — 대시보드에서 값은 다시 안 보인다.

```bash
$ wrangler secret put JWT_SECRET
? Enter a secret value: ********
✨ Success! Uploaded secret JWT_SECRET

$ wrangler secret put JWT_SECRET --env production
```

**일반 환경변수는 `wrangler.toml`의 `vars`** — 코드 저장소에 그대로 들어가도 안전한 값. 로그 레벨, feature flag, 외부 API URL 같은 비기밀 값.

```toml
[env.production]
vars = { LOG_LEVEL = "info", IMAGE_CDN = "https://images.toby-shop.com" }

[env.staging]
vars = { LOG_LEVEL = "debug", IMAGE_CDN = "https://staging-images.toby-shop.com" }
```

코드에서는 모두 `c.env`로 동일하게 접근한다. 시크릿이든 vars든 `wrangler types`가 만들어 준 `Env` 타입으로 오타가 잡힌다.

```ts
app.get("/protected", (c) => {
  const secret = c.env.JWT_SECRET;       // wrangler secret으로 등록
  const logLevel = c.env.LOG_LEVEL;      // [env.*].vars 로 등록
  // ...
});
```

기억해두자. *`.dev.vars`를 절대 git에 올리지 말자.* 한 번 올라가면 history에서 지우는 데 며칠을 쓴다. `.gitignore`에 `.dev.vars`를 처음 프로젝트 만들 때 적어두는 습관을 들이자.

여러 Worker에서 같은 시크릿을 공유해야 한다면 2025년에 발표된 **Cloudflare Secrets Store**(account-level 중앙 관리)를 쓸 수 있다. 다만 새 프로젝트에서는 우선 `wrangler secret put`으로 시작하고, 시크릿 공유가 정말 늘어나는 시점에 Secrets Store로 옮기자. *지금 당장 권유하기엔 아직 새로운 자리*다.

## wrangler.toml의 `[env.*]` — `application-{profile}.yml`을 다시 그리자

Spring 개발자가 환경 분리에 쓰는 `application-prod.yml` / `application-staging.yml` 자리. Workers에서는 `wrangler.toml`의 `[env.production]` / `[env.staging]` 블록이 그 역할이다.

```toml
name = "toby-shop-api"
main = "src/index.ts"
compatibility_date = "2025-04-01"
compatibility_flags = ["nodejs_compat"]

# 기본(개발) 환경 바인딩
[[kv_namespaces]]
binding = "CACHE"
id = "dev-kv-id"

[[d1_databases]]
binding = "DB"
database_name = "toby-shop-dev"
database_id = "dev-db-id"

# Staging
[env.staging]
name = "toby-shop-api-staging"
vars = { LOG_LEVEL = "debug" }

[[env.staging.kv_namespaces]]
binding = "CACHE"
id = "staging-kv-id"

[[env.staging.d1_databases]]
binding = "DB"
database_name = "toby-shop-staging"
database_id = "staging-db-id"

# Production
[env.production]
name = "toby-shop-api"
vars = { LOG_LEVEL = "info" }

[[env.production.kv_namespaces]]
binding = "CACHE"
id = "prod-kv-id"

[[env.production.d1_databases]]
binding = "DB"
database_name = "toby-shop-prod"
database_id = "prod-db-id"
```

배포는 환경별로 한 명령씩.

```bash
$ wrangler deploy --env staging
$ wrangler deploy --env production

$ wrangler secret put JWT_SECRET --env staging
$ wrangler secret put JWT_SECRET --env production

$ wrangler tail --env production    # 라이브 로그
```

Spring의 `--spring.profiles.active=production` 자리에 `--env production`이 들어선다. 한 가지 다른 점이 있다 — Spring은 한 jar가 profile만 바꿔 여러 환경에 도는데, Workers는 환경별로 *별도 Worker가 배포된다.* `[env.production]` 블록은 사실상 새 Worker(`toby-shop-api-staging`)를 만든다. 같은 코드, 다른 바인딩·다른 시크릿·다른 이름. 처음엔 *이게 환경 분리가 맞나* 싶지만, 환경 사이 간섭이 원천적으로 막힌다는 점에서 *오히려 더 안전한 분리*다.

흔한 함정 하나. preview 환경을 만들고 싶을 때다. PR마다 임시 URL을 띄우려면 `wrangler versions upload --env preview` 같은 패턴을 쓰는데, 이건 14장에서 마이그레이션 시 다시 다룬다. 일단 6장에서는 `staging` / `production` 둘이면 충분하다.

## 테스트 — vitest + miniflare로 단위·통합

Spring의 `@SpringBootTest`는 컨텍스트 전체를 띄워 통합 테스트를 한다. 비싸고 느리지만, 진짜 빈을 그대로 검증할 수 있다는 안정감이 크다. Workers에서는 어떻게 그 안정감을 손에 쥐어야 할까.

답은 두 갈래. *단위 테스트는 vitest 그대로*, *통합 테스트는 `@cloudflare/vitest-pool-workers` 위에서 miniflare가 띄운 가짜 Workers 환경*. miniflare는 workerd(production과 같은 V8 isolate 런타임)를 로컬에서 그대로 실행한다. 즉 production과 같은 환경에서 KV·D1·R2까지 SQLite 시뮬레이션으로 돌릴 수 있다.

설치는 한 번에.

```bash
$ pnpm add -D vitest @cloudflare/vitest-pool-workers
```

```ts
// vitest.config.ts
import { defineWorkersConfig } from "@cloudflare/vitest-pool-workers/config";

export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: "./wrangler.toml" },
      },
    },
  },
});
```

이 위에 통합 테스트 한 토막을 써보자. 5장 워크시트의 2번 항목 *상품 검색 API* 를 검증한다.

```ts
// apps/api/test/products.test.ts
import { env, createExecutionContext, waitOnExecutionContext } from "cloudflare:test";
import { describe, it, expect, beforeEach } from "vitest";
import app from "../src/index";

describe("GET /products/:id", () => {
  beforeEach(async () => {
    // D1 스키마 시드
    await env.DB.exec(`
      CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price INTEGER NOT NULL
      );
    `);
    await env.DB.prepare("DELETE FROM products").run();
    await env.DB.prepare("INSERT INTO products (id, name, price) VALUES (1, 'edge book', 25000)").run();
  });

  it("D1에서 가져온 상품을 반환한다", async () => {
    const ctx = createExecutionContext();
    const res = await app.fetch(new Request("http://x/products/1"), env, ctx);
    await waitOnExecutionContext(ctx);
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ id: 1, name: "edge book", price: 25000 });
  });

  it("두 번째 요청은 KV 캐시에서 응답한다", async () => {
    const ctx = createExecutionContext();
    await app.fetch(new Request("http://x/products/1"), env, ctx);
    await waitOnExecutionContext(ctx); // 캐시 쓰기 완료 대기

    // 캐시 hit 확인
    const cached = await env.CACHE.get("product:1", "json");
    expect(cached).toMatchObject({ id: 1, name: "edge book" });
  });

  it("없는 상품은 404", async () => {
    const ctx = createExecutionContext();
    const res = await app.fetch(new Request("http://x/products/999"), env, ctx);
    await waitOnExecutionContext(ctx);
    expect(res.status).toBe(404);
  });
});
```

이 테스트가 도는 모습은 Spring의 `@SpringBootTest`와 다르고도 같다. *다른 점*은 컨텍스트를 띄우는 비용이 거의 없다는 것 — miniflare가 in-memory로 D1·KV를 돌리니까 한 테스트가 수십 ms 안에 끝난다. *같은 점*은 production과 같은 런타임에서 같은 바인딩으로 돌린다는 것. workerd가 production V8 isolate를 그대로 재현하므로, "테스트는 통과했는데 production에서 깨지는" 흔한 함정이 크게 줄어든다.

순수 함수 테스트는 vitest 기본 모드로 돌리자. miniflare를 띄울 필요가 없다.

```ts
// packages/shared/test/users.test.ts (Workers pool 안 씀)
import { describe, it, expect } from "vitest";
import { getUser } from "../src/users";

describe("getUser", () => {
  it("D1 mock으로 단위 테스트", async () => {
    const mockDb = {
      prepare: () => ({
        bind: () => ({
          first: async () => ({ id: 1, name: "alice" }),
        }),
      }),
    } as unknown as D1Database;

    const user = await getUser(mockDb, "1");
    expect(user).toEqual({ id: 1, name: "alice" });
  });
});
```

함수형 DI 패턴이 여기서 빛난다. mock을 그대로 인자로 넘기면 끝. Spring의 `@MockBean`이 자동으로 빈을 갈아 끼워주는 마법은 없지만, *어떤 mock이 어디 들어갔는지가 한 화면에 보이는 명시성*이 그 자리에 들어선다.

**테스트 권유 지점**: 단위 테스트는 빠른 피드백용으로 매번 돌리고, miniflare 통합 테스트는 PR 단위 CI에서 돌리자. Spring의 `@SpringBootTest`는 한 번 띄울 때 5~30초가 걸려 PR마다 돌리기 부담스럽지만, *miniflare는 cold start가 1초 안*이라 PR마다 마음 편히 돌릴 수 있다. 이게 Workers의 작은 자랑이다.

## 짧은 KV 세션 실습 — 다음 장으로 넘어가기 전에

여기까지 라우팅·미들웨어·DI·시크릿·테스트까지 5도구를 깔았다. 마지막 한 토막으로 KV에 세션을 저장해보고 7장으로 넘기자. 5장 워크시트의 3번 항목 *사용자 세션* 이다.

```ts
// apps/api/src/routes/auth.ts
import { Hono } from "hono";
import { setCookie, getCookie, deleteCookie } from "hono/cookie";

type Bindings = { SESSIONS: KVNamespace; JWT_SECRET: string };
type Variables = { userId: string };

const auth = new Hono<{ Bindings: Bindings; Variables: Variables }>();

auth.post("/login", async (c) => {
  const { email, password } = await c.req.json<{ email: string; password: string }>();
  // 인증 로직 (실제로는 D1 + bcrypt)
  if (email !== "demo@toby-shop.com" || password !== "demo") {
    return c.json({ error: "invalid" }, 401);
  }

  const sessionId = crypto.randomUUID();
  const userId = "user-1";

  // 1시간짜리 세션 — KV의 sweet spot
  await c.env.SESSIONS.put(
    `session:${sessionId}`,
    JSON.stringify({ userId, createdAt: Date.now() }),
    { expirationTtl: 3600 },
  );

  setCookie(c, "session", sessionId, {
    httpOnly: true,
    secure: true,
    sameSite: "Lax",
    maxAge: 3600,
  });

  return c.json({ ok: true });
});

// 인증 미들웨어 — KV에서 세션 조회
auth.use("/me", async (c, next) => {
  const sessionId = getCookie(c, "session");
  if (!sessionId) return c.json({ error: "unauthenticated" }, 401);

  const raw = await c.env.SESSIONS.get(`session:${sessionId}`);
  if (!raw) return c.json({ error: "expired" }, 401);

  const session = JSON.parse(raw) as { userId: string };
  c.set("userId", session.userId);
  await next();
});

auth.get("/me", (c) => c.json({ userId: c.get("userId") }));

auth.post("/logout", async (c) => {
  const sessionId = getCookie(c, "session");
  if (sessionId) await c.env.SESSIONS.delete(`session:${sessionId}`);
  deleteCookie(c, "session");
  return c.json({ ok: true });
});

export default auth;
```

이게 Spring Security의 `HttpSessionRepository` + `SessionAuthenticationFilter`가 차지하던 자리다. KV는 이런 *eventually consistent + read-heavy + 짧은 TTL* 워크로드의 sweet spot이다. 60초 정도의 전파 지연이 세션에는 문제가 안 된다 — 사용자가 로그인하자마자 다른 PoP로 옮겨가서 세션이 보이지 않을 확률이 그렇게 높지 않고, 보였다 안 보였다 하는 건 1분 안에 수렴한다.

*다만* — 세션 같은 데이터가 *strong consistency*를 요구하는 시스템이라면 KV는 답이 아니다. 여기서 한 박자 멈추자. 다음 장 7장에서 KV의 *무너지는 자리*와 D1의 자리를 본격적으로 다룬다. 일단 6장의 KV 세션은 "워밍업"이라고 이해하자.

## 코드 품질 도구 — 짧게 한 자리

마무리 전에 코드 품질 한 단락. Workers + Hono 프로젝트에 권유할 만한 셋.

- **`wrangler types`** — `worker-configuration.d.ts`를 자동 생성. `Env` 타입과 compat date 기반 runtime types가 들어와서 IDE 자동완성이 산다. `package.json`의 prebuild 스크립트에 `wrangler types`를 걸어두자.
- **Biome 또는 ESLint + Prettier** — Biome이 더 빠르고 설정이 한 파일이지만, 팀에 이미 ESLint config가 있으면 굳이 갈아엎지 말자.
- **TypeScript strict 모드** — `tsconfig.json`에 `"strict": true`. `c.env.DB`의 타입이 strict일 때 더 정확히 좁혀진다.

모노레포 구조는 reference §4.7 그대로 권유한다.

```
apps/
  api/             # Workers + Hono (이번 장의 결과물)
  web/             # Next.js (9장에서 추가)
  worker-jobs/     # Cron + Workflows (12장에서 추가)
packages/
  shared/          # 도메인 함수 (오늘의 함수형 DI 베이스)
  db/              # Drizzle 스키마 (다음 장에서 추가)
```

각 앱마다 `wrangler.toml` 분리, 공통 binding은 같은 namespace 공유. *지금 6장 단계에서는 `apps/api` 한 개와 `packages/shared` 한 개로 시작*하면 충분하다. 다음 장에서 `packages/db`가 들어온다.

## 이 기술이 무너지는 자리

이 장의 마지막은 정직한 한계로 닫자. Hono + Workers가 빛나는 자리가 분명하지만, *무너지는 자리*도 정직하게 적어야 6장이 광고가 아닌 게 된다.

- **거대한 npm 생태계 대비 작은 미들웨어 풀.** Spring Boot의 starter 생태계가 수천 개라면, Hono의 공식·인기 미들웨어는 수십 개 수준이다. JWT·CORS·logger·basic auth·timing·secure-headers 같은 기본은 다 있지만, *Spring Cloud Gateway 같은 깊이 있는 게이트웨이 미들웨어, Resilience4j 수준의 circuit breaker·bulkhead 라이브러리는 부재*하다. 이런 기능이 핵심이면 직접 짜거나 외부 SaaS(예: AI Gateway는 LLM 트래픽 한정)에 맡겨야 한다.
- **AOP 부재.** Spring의 `@Cacheable`·`@Transactional`·`@Retry` 같은 메서드 단위 cross-cutting concern을 미들웨어 레이어로 풀어 놓으면 라우트 단위까지는 깔끔하지만, *서비스 함수 안의 한 메서드만 캐시*하고 싶을 때는 Hono로 표현이 안 된다. 함수 호출 자리에 명시적으로 `withCache(fn)` 같은 wrapper를 끼워야 한다. 처음엔 번거롭지만 한 달 지나면 *명시성이 살아 있는 코드*에 정이 든다.
- **DI 컨테이너의 안전망 부재.** awilix·tsyringe로 풀 수 있지만 위에서 권유하지 않은 이유가 그대로. 의존성 그래프가 100개를 넘는 도메인은 컨테이너의 lifecycle·scope 관리 없이는 직접 짜기 어렵다. 그런 도메인은 *Workers 한 개에 넣지 말자.* 5장 결정 프레임을 다시 펼쳐 — 이 도메인은 Spring 모놀리스에 두는 게 맞을 가능성이 높다.
- **테스트의 상한.** miniflare가 production V8 isolate를 그대로 재현하지만, Cloudflare Network 측 동작(예: 일부 Zone 기능, AI Gateway 일부 동작)은 시뮬레이션 안 된다. `wrangler dev --remote`로 production edge에 띄워 통합 테스트를 한 번 더 돌려야 하는 자리가 있다.
- **에러 추적의 공백.** `app.onError`로 한 자리에 모을 수는 있지만, Spring Boot Actuator + Sentry + Micrometer가 한 묶음으로 주는 metric·trace·log 통합은 아직 부재하다. Sentry는 됐지만 metric·tracing은 외부 APM(Datadog·Baselime)을 직접 붙여야 한다. 13장에서 다시 다룬다.

이 다섯 자리에서 무너진다는 사실을 손에 쥔 채로 6장의 도구들을 쓰자. 모든 워크로드를 Workers + Hono로 밀어넣지 말고, 5장 워크시트가 *Move now*로 표시한 자리부터 차분히 옮기자. *지금 잘 돌고 있는 Spring Boot를 부수러 가는 게 아니다.*

## 마무리 — 7장 KV·D1로 가기 전에

빈 화면 앞에 앉았던 한 시간 전을 떠올려 보자. `@RestController`도 없고 `@Component`도 없고 `application-prod.yml`도 없는데 어디서부터 시작해야 할지 막막했던 그 자리. 지금은 손에 다섯 도구가 있다. `fetch(req, env, ctx)`라는 본질, Hono의 라우팅·미들웨어 체인, Bindings + c.set/get + 함수형 DI 셋, `.dev.vars`·`wrangler secret put`·`[env.*]`의 시크릿·환경 분리, vitest + miniflare의 테스트.

5장 워크시트로 결정한 *Move now* 항목 중 가장 risk-low한 한 개를 골라, 이 6장의 골격 위에 사흘쯤 깔아 보자. 사용자 검색 API든, 정적 자산 게이트웨이든, 인증 미들웨어든 좋다. 한 번 깔아 본 코드 위에 다음 장의 데이터 레이어가 얹힌다.

7장 *데이터 1 — KV와 D1, 워크로드 패턴으로 골라 쓰기*에서는 오늘 잠깐 만난 KV를 *어디까지 믿어도 되는지*, eventually consistent의 60초 전파가 무엇을 허용하고 무엇을 금지하는지, 그리고 SQL이 필요한 자리에 D1 + Drizzle을 어떻게 끼워 넣는지를 본격적으로 다룬다. 6장이 *골격*이었다면 7장은 그 골격에 *데이터의 살을 붙이는 장*이다. 사용자 CRUD에 D1을 추가하고, 세션은 KV로 분리하고, `drizzle-kit migrate`로 스키마를 첫 번째로 돌려보자.

자, 다음 장을 펴자.
