# 3장. 활용 패턴의 지형 — REST·GraphQL·CLI·워커·WebSocket·서버리스

손에 새 환경이 갖춰졌다고 해 보자. TypeScript로 타입을 짜고, pnpm으로 의존성을 묶고, lockfile로 결정론을 잡았다. 이제 그 환경 위에 진짜 백엔드를 올려야 한다. 그런데 막상 빈 폴더 앞에 앉으면, 한 가지 질문이 가만히 떠오른다 — Spring에서 늘 쓰던 도구들의 자리에 Node에선 무엇을 두어야 하는가? Spring MVC가 차지하던 자리, Spring Batch가 차지하던 자리, WebFlux + STOMP의 자리, Spring Cloud Function의 자리. 그 각각을 누가 메우고 있고, 어디서 모양이 갈라지는가. 이번 장에서 우리가 그릴 것은 Node 백엔드의 활용 패턴 지형이다. 도구를 나열하는 카탈로그가 아니라, "어디서 강점을 보이는가"의 관점에서 본 지도다.

## LinkedIn이 보여준 것 — Node가 잘하는 자리

지도 그리기를 시작하기 전에, 한 가지 사례를 떠올려 보자. 2011년 LinkedIn이 모바일 백엔드를 Ruby on Rails에서 Node.js로 옮겼던 이야기다. 출발점은 평범했다 — Mongrel 인스턴스가 메모리 누수로 한 프로세스당 300MB까지 부풀고, JSON 직렬화가 느렸다. 익숙한 통증이다. 그런데 결과는 평범하지 않았다. **서버 30대가 3대로 줄었고, 동시에 10배 부하 헤드룸이 생겼다.** 처리량은 약 20배 빨라졌고, 코드는 6만 라인에서 2천 라인으로 줄었다. 그저 빠른 런타임으로 갈아탄 게 아니다. 일감 자체가 Node의 본성과 잘 맞은 것이다.

LinkedIn 팀이 그 회고에서 짚은 한 줄이 핵심이다 — "Node의 강점은 다른 서비스와 대화하기였다." 모바일 앱이 들어와서, 백엔드 플랫폼 API 여러 곳에 동시에 요청을 보내고, 응답을 합쳐서 모바일에 알맞은 모양으로 돌려주는 일. 이걸 우리는 BFF(Backend for Frontend)라 부른다. 이 일감은 거의 100% I/O다. 네트워크 호출을 동시에 여러 개 띄워 두고, 먼저 끝난 응답부터 차곡차곡 쌓는다. 단일 스레드 + 이벤트 루프 모델이 가장 빛나는 자리이고, JVM이 무겁게 느껴지는 자리이기도 하다. 같은 시기에 Netflix가 UI 서버 시작 시간을 40분에서 1분 미만으로 줄이고, 응답 시간을 약 70% 깎았다고 보고한 것도 같은 자리에서다 — 백엔드 마이크로서비스(Java/Groovy)는 그대로 두고, 그 앞에 Node BFF만 새로 깔았다. 이 그림을 잘 기억해 두자. 8장 마이그레이션 전략에서 같은 그림이 다시 등장한다.

여기서 한 가지 메시지를 받자. **Node를 도구로 고를 때, 가장 먼저 물어야 할 것은 일감의 모양이다.** I/O가 본체인가, CPU가 본체인가. 사용자 응답이 짧아야 하는가, 백그라운드에서 길게 돌아도 되는가. 트래픽이 평탄한가, 들쭉날쭉한가. 한 인스턴스가 한 시간에 열 번만 호출되는가, 분당 1,500번 호출되는가. 이 질문들이 곧 이 장의 절을 가른다. 그러니 활용 패턴을 살펴볼 때마다, "이 일감은 Node가 잘하는 자리인가"를 같이 점검해 보자. 잘 맞으면 LinkedIn처럼 30대가 3대로 줄고, 잘 안 맞으면 Uber처럼 신규 권장 스택에서 빠진다. 도구는 자리에 맞춰 고르는 거다.

## Spring 진영의 풀 스택 매트릭스를 Node에 겹쳐 보자

먼저 큰 지도부터 그리자. Spring 진영은 한 단체 사진을 갖고 있다 — Spring MVC가 동기 REST를 맡고, Spring Batch가 야간 일괄 처리를 맡고, Spring WebFlux가 리액티브와 SSE·WebSocket을 맡고, Spring Cloud Function이 서버리스 함수를 맡는다. 거기에 picocli가 CLI를, Spring Integration이 메시지 라우팅을 맡는 식이다. 자리마다 한 도구가 박혀 있다.

Node 진영은 같은 자리에 다른 도구들을 둔다. 짝을 지어 한 표로 모아 보자.

| Spring 진영의 자리 | Node 진영의 짝 | 본질적 차이의 한 줄 |
|---|---|---|
| Spring MVC | Express / Fastify / NestJS | NestJS가 가장 닮았고, Fastify가 가장 빠르고, Express가 가장 보편 |
| JAX-RS | Express raw 라우터 | 어노테이션 대신 함수 등록 |
| Spring Batch | BullMQ + 워커 프로세스 | 잡 단위 + 분산 큐, "스텝" 추상은 없음 |
| Spring Scheduler / Quartz | BullMQ repeatable job, `node-cron` | 단일 인스턴스 cron은 거의 안 씀, Redis 기반이 표준 |
| Spring WebFlux + STOMP | Socket.IO / `ws` | 메시지 브로커가 한 단계 분리 |
| Spring Cloud Function | AWS Lambda / Vercel / Cloudflare Workers | 콜드 스타트 격차가 본질 |
| picocli | commander / yargs / oclif | 데코레이터까지 모양이 비슷 |
| Spring Integration | RabbitMQ/Kafka 클라이언트 + 직접 라우팅 | "통합 DSL"의 자리는 비어 있다 |
| Spring Data JPA | Prisma / Drizzle / TypeORM | 5장에서 정면으로 다룬다 |

이 표가 이번 장의 목차다. 자리마다 한 절씩 들러서, "원래 Spring 출신이 알던 그 일감이 Node에선 어떤 모양으로 풀리는가"를 살피자. 표만 보고 끝낼 수도 있겠지만, 그러면 막상 코드를 짤 때 손이 멈춘다. 모양이 비슷한 자리(NestJS ↔ Spring MVC)는 빠르게, 모양이 갈라지는 자리(BullMQ ↔ Spring Batch, Lambda ↔ Cloud Function)는 천천히 살펴보자.

한 가지 약속을 해 두자. 이 장은 NestJS의 모듈·DI·인터셉터를 깊게 들어가지 않는다. 거기는 4장에서 정면으로 비교한다. 여기서는 "NestJS가 어디에 자리 잡고 있는가"까지만 본다. 그래야 4장의 깊은 비교가 어색해지지 않는다.

또 한 가지, 이 표를 읽을 때 빠지기 쉬운 함정을 짚어 두자. **"자리가 일대일로 매핑된다고 해서 사고방식이 같다는 뜻은 아니다."** Spring Batch와 BullMQ는 자리는 같지만 사고 모델이 갈라지고, Spring WebFlux + STOMP와 Socket.IO도 자리는 같지만 메시지 라우팅 사상이 다르다. 자리 매핑은 출발점일 뿐이다 — 같은 자리에서 어떻게 모양이 다른가가 진짜 본문이다. 그래서 다음 절들은 도구를 소개한다기보다, "Spring 진영의 사고방식이 Node 진영에서 어떻게 비틀려 들어오는가"를 짚는 모양으로 흘러갈 것이다.

## REST — Express, Fastify, NestJS의 삼각 구도

Spring MVC의 자리부터 보자. 컨트롤러에 `@RestController`를 붙이고, 메서드에 `@GetMapping("/users/{id}")`을 붙이고, 매개변수에 `@PathVariable`을 붙이는 그 패턴. Node에서 같은 자리를 차지하는 도구가 셋 있다. 하나로 좁혀지지 않고 셋이 동시에 살아 있다는 점부터가 Spring 진영과 다르다. Spring 진영은 거의 단일 표준이지만(Spring MVC가 압도적), Node 진영은 셋이 각자의 강점을 갖고 공존한다. 이 다양성이 처음엔 난감하게 느껴질 수 있는데, 사실은 자리값을 한다 — 작은 BFF엔 가벼운 도구, 큰 도메인엔 구조 도구, 성능 민감 자리엔 빠른 도구. 한 줄짜리 답이 없다는 게 솔직히 말하면 Node 진영의 솔직함이다.

**Express**는 가장 보편적이다. 2010년부터 살아 있고, 미들웨어 생태계는 npm에서 가장 두껍다. 코드 모양은 함수 등록형이다 — `app.get('/users/:id', handler)`. 데코레이터도, 모듈 그래프도, 의존성 주입도 없다. 좋게 말하면 가볍고, 나쁘게 말하면 강제성이 없다. 큰 팀에서 컨트롤러 모양이 사람마다 달라져 버리는 일이 흔히 생긴다. 한 사람은 `try-catch`로 에러를 잡고, 다른 사람은 `next(err)`에 넘기고, 또 다른 사람은 미들웨어 체인 어딘가에 모듈 단위 catch를 둔다. 처음엔 자유롭게 보이지만 코드가 100파일을 넘어가는 순간, 누가 어디서 응답을 잘랐는지 추적이 어려워지기 시작한다. PayPal이 사내에 Kraken.js라는 컨벤션 레이어를 직접 만들어 얹은 이유가 그것이고, 인프랩이 Express + 함수형 라이브러리에서 NestJS Monorepo로 옮긴 이유의 첫 번째도 그것이다. JAX-RS가 어노테이션으로 강제하던 모양이 Express에는 없다는 점, 한 줄로 정리하면 그것이다.

**Fastify**는 성능이 본체다. 2017년에 출발했고, 핵심 설계는 두 가지다. 첫째, 경로별로 JSON Schema를 등록하면 그 스키마로 직렬화 코드를 빌드 타임에 생성한다. `JSON.stringify`가 느린 자리에서 두 배까지 빠르다. 둘째, 요청·응답 라이프사이클을 hook 단계로 명시했다. Express의 미들웨어 체인보다 모양이 명확하다. 헬로월드 벤치 기준으로 Express의 RPS가 약 38,000 근처라면 Fastify는 약 76,000 근처에 닿고, p99 레이턴시도 절반 가까이 줄어든다는 보고가 있다. 다만 헬로월드는 헬로월드일 뿐이다. 실제 DB·외부 호출이 들어가면 그 격차가 줄어든다는 건 잊지 말자. 그래도 한 가지 진짜 가치가 남는다 — **JSON Schema가 검증과 직렬화와 OpenAPI 문서까지 한 source of truth로 묶인다는 점.** Spring 진영에서 `@Valid`, Bean Validation, springdoc-openapi가 따로 자리 잡던 곳을 Fastify는 한 도구로 묶는다. 이 자리값이 의외로 크다.

**NestJS**는 구조가 본체다. 컨트롤러·서비스·모듈을 데코레이터로 묶고, DI 컨테이너가 주입을 처리하고, 인터셉터·가드·파이프가 AOP의 자리를 메운다. Spring Boot 출신이라면 처음 본 순간 "어, 어디서 본 모양인데?"라는 감각이 든다. 직방의 김동영이 회고에서 정리한 1:1 매핑이 그걸 그대로 보여준다 — `@Controller` ↔ `@Controller`, `@Bean` ↔ `@Injectable`, IoC Container ↔ NestJS Module, `@Interceptor` ↔ NestInterceptor, Exception Handler ↔ Exception Filter, Argument Resolver / Validator ↔ Pipe, Spring Security ↔ Guard. 모양은 거의 그대로 들고 갈 수 있다. 다만 NestJS는 내부적으로 Express 또는 Fastify 위에서 돌아간다. 즉 "NestJS vs Express"는 정확한 대립이 아니다. NestJS를 Fastify 어댑터로 띄우면 구조와 성능을 같이 가져갈 수도 있다.

그렇다면 어느 도구를 첫날 도구로 골라야 할까. 한 가지 가이드를 산문으로 풀어 보자. 팀이 두세 명이고, 마이크로서비스가 한두 개고, 수명이 짧다면 — Fastify 위에 가볍게 시작하는 편이 낫다. 보일러플레이트 부담이 적고, 사고 모델이 작다. 반대로 팀이 다섯 이상이고, 도메인이 여럿이고, 수명이 길게 잡힌다면 — NestJS의 모듈 그래프가 짐을 덜어 준다. 4장에서 자세히 다루겠지만, 이 결정의 본질은 "구조의 강제가 짐인가, 안전망인가"의 판단이다. Express는 기존 프로젝트가 이미 그 위에 서 있을 때 그대로 가는 선택지로 두자. 새 프로젝트의 디폴트 추천은 아니다.

### 시그니처 페이지 — 같은 엔드포인트, 세 모양

말로만 보면 닿지 않는다. 가장 평범한 엔드포인트 하나, `GET /users/:id`를 세 모양으로 나란히 두고 보자. 먼저 Spring Boot 컨트롤러부터.

```java
// Spring Boot — UserController.java
@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserDto> findOne(@PathVariable Long id) {
        UserDto user = userService.findById(id);
        return ResponseEntity.ok(user);
    }
}
```

이번엔 NestJS다.

```ts
// NestJS — users.controller.ts
import { Controller, Get, Param, ParseIntPipe } from '@nestjs/common';
import { UsersService } from './users.service';
import { UserDto } from './dto/user.dto';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get(':id')
  async findOne(@Param('id', ParseIntPipe) id: number): Promise<UserDto> {
    return this.usersService.findById(id);
  }
}
```

두 코드가 거의 거울처럼 닮았다. `@RestController` ↔ `@Controller`, `@RequestMapping("/users")` ↔ `@Controller('users')`, `@GetMapping("/{id}")` ↔ `@Get(':id')`, `@PathVariable` ↔ `@Param`, 생성자 주입까지 그대로다. `ParseIntPipe`가 Spring의 컨버터·바인딩 자리에 박혀 있다는 정도가 차이다. Spring 출신이 NestJS 코드를 읽을 때 "이미 알던 코드처럼 읽힌다"는 회고가 흔한 이유가 여기에 있다. 한 가지 미묘한 차이가 더 있다 — Spring은 `ResponseEntity<UserDto>`로 응답 코드를 명시적으로 제어하는 모양이 흔한데, NestJS는 기본적으로 반환값을 200 OK로 직렬화하고, 다른 코드를 주려면 `@HttpCode(204)` 데코레이터나 `Response` 객체를 직접 받는다. 이 차이는 작아 보이지만, REST 응답을 정밀하게 제어해야 하는 자리에서 첫날 한 번씩 부딪힌다. 잊지 말자.

이제 같은 엔드포인트를 Express raw로 짠 모양도 잠깐 보자.

```ts
// Express — server.ts
import express from 'express';
import { findUserById } from './users.service';

const app = express();

app.get('/users/:id', async (req, res, next) => {
  try {
    const id = Number(req.params.id);
    if (Number.isNaN(id)) return res.status(400).json({ message: 'invalid id' });
    const user = await findUserById(id);
    if (!user) return res.status(404).json({ message: 'not found' });
    res.json(user);
  } catch (err) {
    next(err);
  }
});

app.listen(3000);
```

코드가 짧긴 한데, 한눈에 봐도 모양이 다르다. 컨트롤러도 모듈도 없고, 함수 하나에 라우팅·검증·예외 처리·응답 코드가 다 들어가 있다. 이 모양으로 30~40개의 엔드포인트가 쌓이면 어떻게 될지 상상해 보자. 한 사람이 짠 모양과 다른 사람이 짠 모양이 미묘하게 어긋나기 시작한다. PayPal이 Kraken.js를 만들게 된 그 자리다. 이 모양이 무조건 나쁘다는 게 아니다. 작은 BFF·짧은 수명·소규모 팀이라면 이 가벼움이 강점이다. 다만 규모가 커지는 순간, 같은 가벼움이 부담으로 바뀐다.

세 코드를 같이 놓고 보면, 한 가지 직관이 들어온다. **NestJS는 Spring Boot 코드의 모양 자체를 가장 적게 바꾼다.** 어노테이션이 데코레이터로, Java 타입이 TypeScript 타입으로 바뀌는 정도다. Express는 그 반대편 — 컨트롤러라는 추상 자체가 사라지고, 함수가 직접 라우팅 테이블에 등록된다. Fastify는 Express와 NestJS의 중간 어디쯤이다. 이 직관이 "어느 도구가 우리 팀에 자연스러운가"를 결정한다. Spring 출신이 일찌감치 NestJS를 만나 본 한국 회사들 — 직방, 인프랩, 토스, 당근 — 의 회고가 모두 같은 자리를 짚는다 — "구조가 매우 유사해 적응이 빨랐다." 그 익숙함이 도구 결정에 큰 무게를 준다. 다만 4장에서 다시 보겠지만, 이 익숙함이 만능은 아니다. NestJS는 Spring Boot의 두툼한 ecosystem(트랜잭션, 캐시, 배치, 시큐리티)이 빠진 자리에 직접 도구를 끼워야 하고, "이건 NestJS의 진짜 DI인가"라는 비판도 있다. 거기까진 다음 장에서 정직하게 다루자.

## GraphQL — Apollo, Mercurius, 그리고 NestJS DI가 풀어 주는 것

REST의 자리를 봤으니 GraphQL의 자리도 보자. Spring 진영이라면 graphql-java + Spring for GraphQL이 익숙할 테고, DataLoader로 N+1을 푸는 패턴도 익숙할 것이다. 한 가지 직관 — GraphQL은 본래 페이스북이 모바일 앱의 BFF 문제를 풀기 위해 만든 기술이다. 클라이언트마다 필요한 필드가 다르고, 한 화면에 여러 자원이 동시에 등장하는 자리. 이 자리가 LinkedIn·Netflix가 Node BFF로 풀던 자리와 거의 정확히 겹친다. 그래서 Node 진영에서 GraphQL이 깊이 자리 잡았다. Node 진영도 같은 도구의 자리에 두 도구가 있다 — **Apollo Server**와 **Mercurius**. Apollo는 GraphQL 쪽의 표준에 가깝고, Mercurius는 Fastify 위에서 돌도록 설계된 빠른 대안이다.

여기서 흥미로운 자리가 NestJS다. NestJS는 `@nestjs/graphql` 모듈에서 Apollo와 Mercurius를 둘 다 어댑터로 지원한다. 그리고 NestJS의 진짜 무기가 등장한다 — **request scope DI**. GraphQL의 N+1을 푸는 가장 표준적인 방법이 DataLoader인데, DataLoader는 요청 단위로 새 인스턴스가 만들어져야 한다(요청 간 캐시가 섞이면 안 되니까). Spring에서 `@RequestScope` Bean을 만드는 자리와 같은 사고방식이다. NestJS에서는 `@Injectable({ scope: Scope.REQUEST })`로 그 자리를 채운다.

말이 길었으니 짧은 코드로 풀어 보자. 사용자와 사용자가 쓴 글의 관계가 있는 스키마에서 N+1을 막는 모양이다.

```ts
// posts.loader.ts
import DataLoader from 'dataloader';
import { Injectable, Scope } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import type { Post } from '@prisma/client';

@Injectable({ scope: Scope.REQUEST })
export class PostsLoader {
  constructor(private readonly prisma: PrismaService) {}

  // 여러 userId를 모았다가 한 번의 쿼리로 가져온다
  readonly byUser = new DataLoader<number, Post[]>(async (userIds) => {
    const rows = await this.prisma.post.findMany({
      where: { authorId: { in: [...userIds] } },
    });

    // 입력 순서를 그대로 유지해 돌려주는 게 DataLoader 규약
    const grouped = new Map<number, Post[]>();
    for (const id of userIds) grouped.set(id, []);
    for (const row of rows) grouped.get(row.authorId)?.push(row);
    return [...userIds].map((id) => grouped.get(id) ?? []);
  });
}

// users.resolver.ts
import { Resolver, ResolveField, Parent, Query, Args } from '@nestjs/graphql';
import { UsersService } from './users.service';
import { PostsLoader } from '../posts/posts.loader';

@Resolver('User')
export class UsersResolver {
  constructor(
    private readonly usersService: UsersService,
    private readonly postsLoader: PostsLoader,
  ) {}

  @Query(() => [User])
  users() {
    return this.usersService.findAll();
  }

  @ResolveField('posts')
  posts(@Parent() user: User) {
    // N개의 user에 대해 호출돼도 결국 단일 SELECT로 묶인다
    return this.postsLoader.byUser.load(user.id);
  }
}
```

짚어 둘 자리가 두 군데다. 첫째, `@Injectable({ scope: Scope.REQUEST })`가 없다면 같은 NestJS 인스턴스가 여러 요청에서 DataLoader 캐시를 공유해 버린다. 어제 본 사용자의 글이 오늘 다른 요청에 섞여 들어가는 끔찍한 일이 생긴다. 잊지 말자. 둘째, DataLoader의 핵심 규약은 "입력 순서를 그대로 유지해 돌려준다"는 점이다. graphql-java의 BatchLoader도 같은 규약을 쓴다. 모양이 거의 똑같다.

여기서 Spring 출신이 마주치는 작은 충격이 하나 있다. Spring for GraphQL은 `@SchemaMapping`, `@BatchMapping` 같은 어노테이션으로 DataLoader 등록을 거의 자동화한다. NestJS는 좀 더 명시적이다 — DataLoader 인스턴스를 직접 만들고, `load()`를 직접 호출한다. "마법이 적은 대신 설계가 보인다"는 표현이 어울리는 자리다. 5장에서 Prisma를 다룰 때 비슷한 감각이 또 한 번 등장한다. Hibernate의 자동 dirty checking이 사라진 자리에서, 우리가 직접 트랜잭션과 select를 적어야 하는 그 감각이다.

Apollo와 Mercurius 중 어느 것을 디폴트로 둘지도 짧게 짚어 두자. **Apollo Server**는 GraphQL 진영의 표준에 가깝고, 사가(saga)·페더레이션·스튜디오 같은 부가 도구가 많다. 학습 자료가 가장 두껍고, 외부 인력이 들어와도 익숙하다. **Mercurius**는 Fastify 위에서 돌도록 설계됐고, JIT 쿼리 컴파일 같은 성능 트릭이 박혀 있다. 같은 헬로월드 GraphQL에서 Mercurius가 Apollo보다 두 배 가까이 빠르다는 보고가 흔하다. 결정의 본질은 단순하다 — 이미 NestJS + Express 위에 있다면 Apollo가 자연스럽고, NestJS + Fastify 또는 raw Fastify 위에서 시작한다면 Mercurius를 고려하자. NestJS는 둘 다 어댑터로 지원하니까 갈아끼울 수도 있다. 다만 갈아끼우는 데 비용이 든다는 점은 잊지 말자 — 데코레이터 일부, 컨텍스트 모양, 페더레이션 도구가 미묘하게 다르다.

Spring for GraphQL과 비교해 두 가지 미묘한 차이가 더 있다. 첫째, 스키마 정의 방식이다. Spring for GraphQL은 SDL(Schema Definition Language) 파일을 별도로 두고 Java 메서드와 매핑하는 방식이 표준이다. NestJS는 두 갈래가 있다 — SDL 우선(schema-first)과 코드 우선(code-first). 코드 우선으로 가면 데코레이터로 타입을 적고 SDL이 자동 생성된다. 코드와 스키마가 한 파일에 있다는 매끄러움이 강점이지만, 큰 팀에서 스키마 리뷰를 별도로 돌리고 싶다면 schema-first가 더 적합하다. 둘째, 페더레이션이다. Apollo Federation으로 여러 서비스의 GraphQL을 한 게이트웨이 뒤로 묶는 패턴이 마이크로서비스 시대에 자리값을 한다. NestJS도 `@nestjs/graphql`에서 Federation v2를 지원한다. Spring for GraphQL은 페더레이션 쪽이 조금 더 보수적이다. 운영 규모가 커지는 자리에서는 이 차이가 의외로 무게를 가진다.

GraphQL을 도입할지 자체를 결정하는 자리도 한 번 짚어 두는 편이 낫다. **REST 컨트롤러 두세 개로 끝나는 일감에 GraphQL을 들이는 건 끔찍한 일이다.** 스키마, 리졸버, DataLoader, 코드 생성, 타입 동기화 — 이 모든 인프라를 짓는 비용을 회수하려면, 클라이언트가 여러 자원을 한 번에 조합해야 하는 자리, 또는 클라이언트마다 필요한 필드가 다른 자리(웹/iOS/Android의 BFF)여야 한다. LinkedIn·Netflix·페이스북이 GraphQL을 본격 도입한 이유가 그 자리에 정확히 있다. 우리 도메인이 그 자리에 있는지 먼저 묻고, 그 다음에 도구를 고르자.

## CLI — picocli의 자리에 commander, yargs, oclif

활용 패턴 지도에서 종종 잊히는 자리가 CLI다. 그런데 실무에서 CLI 도구의 비중은 의외로 크다. 데이터 백필, 운영 스크립트, 사내 마이그레이션 도구, 신규 프로젝트 스캐폴더. Spring 출신이라면 **picocli**나 Spring Shell이 익숙할 것이다. Node 진영에는 같은 자리에 셋이 있다.

**commander**는 가장 보편적이다. API가 작고, 학습 곡선이 거의 없다. 한 파일에 `program.command('build').option('--watch')` 스타일로 커맨드를 등록한다. **yargs**는 commander와 비슷한 자리에 있는 대안이고, 자동 도움말 생성이 강하다. **oclif**는 picocli에 가장 모양이 닮았다. 클래스 단위로 커맨드를 정의하고, 데코레이터·플러그인 시스템을 갖췄으며, Heroku CLI가 oclif로 만들어져 있다. CLI 자체가 큰 도구로 자랄 가능성이 있다면 oclif가 자리값을 한다.

짧은 commander 예시를 보자. 가장 익숙한 모양이다.

```ts
// scripts/migrate.ts — 운영용 마이그레이션 CLI
import { Command } from 'commander';
import { runMigration } from '../src/jobs/migrate-users';

const program = new Command();

program
  .name('migrate-users')
  .description('레거시 DB에서 새 스키마로 사용자 데이터를 옮긴다')
  .version('1.2.0');

program
  .command('run')
  .option('-b, --batch <size>', '한 번에 옮길 행 수', '500')
  .option('--dry', '실제 쓰지 않고 시뮬레이션만')
  .action(async (opts) => {
    await runMigration({
      batchSize: Number(opts.batch),
      dryRun: Boolean(opts.dry),
    });
  });

program.parseAsync(process.argv);
```

이걸 어떻게 배포하느냐가 한 가지 더 풀어야 할 자리다. Java라면 fat jar로 묶고 `java -jar`로 돌렸을 텐데, Node는 사정이 다르다. 사용자가 `node` 런타임을 갖고 있어야 하고, `node_modules`도 있어야 한다. 이 부담을 줄이는 방법이 두 갈래다. 사내 도구라면 `npm publish`(혹은 사내 레지스트리)로 패키지로 배포하고 `npx`로 실행하는 편이 가장 매끄럽다. 외부에 단일 실행 파일을 주고 싶다면, **esbuild**나 **Vite**로 모든 의존성을 한 파일로 번들링한 뒤, Node 22+의 `--experimental-sea-config`(Single Executable Applications) 또는 `pkg`/`nexe` 같은 도구로 Node 런타임까지 한 바이너리로 묶을 수 있다. picocli + GraalVM Native Image로 한 바이너리를 만드는 그 자리다. 다만 SEA는 아직 실험 단계라는 점을 잊지 말자. 사내 표준 도구라면 npx 배포가 안전하다.

CLI 자리에서 한 가지 더 짚어 두자 — **운영 스크립트의 위치**다. 운영팀이 가끔 한 번씩 돌리는 잡(예: 특정 사용자 데이터 정정, 캐시 무효화, 백필)을 어디에 둘 것인가? Spring Boot라면 종종 `CommandLineRunner`나 `ApplicationRunner` Bean으로 같은 jar 안에 둬서, 같은 빈 그래프와 트랜잭션 매니저를 그대로 쓸 수 있었다. Node에선 한 가지 좋은 모양이 있다 — 모노레포 안에 `apps/cli`라는 워크스페이스를 두고, API 서버와 같은 도메인 모듈(`packages/domain`)을 그대로 import해 쓴다. 같은 Prisma 클라이언트, 같은 서비스 함수, 같은 도메인 타입이 그대로 들어온다. 2장 monorepo 자리에서 본 workspaces 사고가 여기서 자리값을 한다. CLI는 별도 프로젝트가 아니라, 같은 도메인의 다른 진입점일 뿐이다.

## 백그라운드 워커 — BullMQ가 차지한 자리

자리 매트릭스에서 가장 모양이 갈라지는 곳이 여기다. Spring Batch는 "스텝(step)" 추상을 중심으로 짠다 — 입력 reader, 변환 processor, 출력 writer를 한 스텝으로 묶고, 스텝들을 잡(job)으로 엮는다. 청크 단위 트랜잭션, 스킵·재시도 정책, JobRepository를 통한 이력 관리가 한 통으로 들어 있다. Quartz Scheduler를 함께 쓰면 cron 스케줄까지 같은 우산 아래 들어온다. 한 마디로 **잡과 스텝이 일급 시민이고, 트랜잭션이 그 안에 박혀 있다.**

Node 진영은 사고 모델이 다르다. **분산 큐 + 워커 풀**이 본체다. 사실상의 표준이 **BullMQ**다(이름 그대로 Redis 위에서 동작하는 잡 큐다). 모양은 이렇게 그릴 수 있다 — 한쪽에는 잡을 만들어 큐에 던지는 producer가 있다(보통 API 서버). 다른 쪽에는 큐에서 잡을 꺼내 처리하는 worker 프로세스가 있다(보통 별도 컨테이너). 그 사이에 Redis가 있다. 잡은 우선순위·재시도 횟수·백오프 전략·딜레이·repeatable cron을 메타로 가지며, 처리 결과는 큐에 다시 적힌다. Spring Batch처럼 "스텝 안의 트랜잭션 청크" 같은 추상은 없다. 하나의 잡이 한 번 돌고, 실패하면 재시도된다. 이 모양은 Sidekiq(Ruby), Celery(Python), RabbitMQ + Spring AMQP 컨슈머와 사고 모델이 더 가깝다. Spring 출신이 처음 BullMQ를 만났을 때 "어, 이건 배치라기보다 메시지 큐 컨슈머에 가깝네"라는 감각을 받는 이유가 그것이다.

이 모양이 의외로 단단하다. 한국 사례 하나 — 당근마켓의 푸시알림 서비스가 이 자리에 있다. 채팅, 키워드 알림, 금주의 인기글 같은 푸시 트래픽이 한 곳에 몰려 모놀리식 Rails가 한계에 닿자, 푸시만 떼어 NestJS + BullMQ 마이크로서비스로 옮겼다. 회고에 적힌 수치가 인상적이다 — **초당 1,500 RPS의 푸시 잡을 누락 없이 처리**, 그것도 별도 인프라 추가 없이 단일 마이크로서비스로 흡수했다. "트래픽 폭주 + I/O 바운드"라는 모양이 Node + 큐 모델과 정확히 맞물린 자리다.

코드로 보자. 가장 흔한 시나리오 — 회원가입 시 이메일을 보내야 하는데, 응답을 막기 싫어 큐로 던지는 모양이다.

```ts
// queues/email.queue.ts — producer
import { Queue } from 'bullmq';
import IORedis from 'ioredis';

const connection = new IORedis(process.env.REDIS_URL!, {
  maxRetriesPerRequest: null,
});

export const emailQueue = new Queue<EmailJobData>('email', { connection });

export type EmailJobData = {
  to: string;
  templateId: 'welcome' | 'reset-password';
  payload: Record<string, unknown>;
};

// 사용 — 회원가입 컨트롤러 어딘가
await emailQueue.add(
  'welcome',
  { to: user.email, templateId: 'welcome', payload: { name: user.name } },
  {
    attempts: 5,                    // 최대 5번까지 재시도
    backoff: { type: 'exponential', delay: 1000 }, // 1s, 2s, 4s, 8s, 16s
    removeOnComplete: { age: 3600 },// 성공한 잡은 1시간 보관
    removeOnFail: { age: 86400 },   // 실패한 잡은 하루 보관(분석용)
  },
);
```

이제 잡을 처리하는 워커 프로세스다. 이 코드는 API 서버와는 **별도의 프로세스**로 띄운다. 컨테이너로 본다면 별도 컨테이너다.

```ts
// workers/email.worker.ts — consumer
import { Worker } from 'bullmq';
import IORedis from 'ioredis';
import { sendEmail } from '../infra/email-client';
import type { EmailJobData } from '../queues/email.queue';

const connection = new IORedis(process.env.REDIS_URL!, {
  maxRetriesPerRequest: null,
});

const worker = new Worker<EmailJobData>(
  'email',
  async (job) => {
    // 잡 하나의 본문. 실패하면 위에서 정한 backoff로 자동 재시도된다
    await sendEmail({
      to: job.data.to,
      templateId: job.data.templateId,
      payload: job.data.payload,
    });
  },
  {
    connection,
    concurrency: 50,                  // 한 워커가 동시에 50개까지 처리
    limiter: { max: 100, duration: 1000 }, // 외부 API rate limit 보호
  },
);

worker.on('failed', (job, err) => {
  console.error('email job failed', { id: job?.id, attempts: job?.attemptsMade, err });
});

worker.on('completed', (job) => {
  // 메트릭으로 보내거나 그냥 두거나
});

// graceful shutdown — K8s SIGTERM 받았을 때
process.on('SIGTERM', async () => {
  await worker.close(); // 진행 중 잡은 마저 끝낸 뒤 종료
  await connection.quit();
});
```

이 코드 한 통이 풀고 있는 일들을 정리해 보자. **재시도 정책**이 producer 쪽에 박혀 있다 — Spring Batch의 `RetryPolicy`가 잡 정의에 박혀 있는 자리다. **백오프**가 지수형으로 적힌다. **동시성**이 워커당 50으로 잡혔다 — 이건 Spring Batch의 `taskExecutor` 자리다. **rate limiter**가 외부 API를 보호한다. **graceful shutdown**으로 K8s가 SIGTERM을 보내도 진행 중인 잡을 마저 끝낸다. 이 모든 것이 BullMQ가 사실상 표준으로 자리 잡은 이유다. Sidekiq(Ruby)이나 Celery(Python)에 비해 동시성을 기본으로 잘 풀어낸다는 평가도 같이 따라다닌다.

여기서 BullMQ가 풀지 못하는 자리도 짚어 두자. **Spring Batch의 청크 트랜잭션** — "1000개를 reader로 읽어 1000개를 writer로 쓰고, 그 1000개가 한 트랜잭션 안에서 커밋되거나 전부 롤백된다"는 의미론은 BullMQ에 없다. 내가 직접 잡 안에서 트랜잭션을 열고, 청크 사이즈를 결정하고, 실패 시 어떻게 부분 커밋을 다룰지를 정해야 한다. 이건 빠진 게 아니라 모양이 다른 거다. 큰 야간 ETL을 매일 한 번 도는 일감이라면 Spring Batch 쪽 사고 모델이 더 적합할 수도 있다. 그래서 Node 진영에서도 무거운 ETL은 종종 별도 도구(예: Airflow, dbt)에 위임하고, BullMQ는 사용자 트랜잭션 직후의 비동기 후처리(이메일·푸시·웹훅·인덱싱 갱신)에 더 자주 쓴다.

또 한 가지 짚을 자리가 **잡 결과의 멱등성(idempotency)**이다. BullMQ는 잡이 실패하면 정해진 횟수만큼 재시도하는데, 외부 API 호출이 도중에 끊긴 경우 — "보냈는지 안 보냈는지" 모호한 상태가 종종 생긴다. 이걸 그냥 두면 같은 사용자에게 환영 메일이 두 번, 세 번 가는 끔찍한 일이 벌어진다. 처음 잡을 설계할 때부터 멱등 키(`jobId` 또는 비즈니스 키)를 같이 박아 두는 편이 낫다. BullMQ의 `add(name, data, { jobId: 'welcome:' + userId })`로 같은 키의 잡은 중복으로 들어오지 않게 막을 수도 있다. Spring Batch의 `JobRepository`가 같은 잡 인스턴스 중복을 막아 주던 자리에 우리가 직접 한 줄 적어 둔다고 보면 된다.

repeatable job으로 cron의 자리도 메운다 — `emailQueue.add('digest', ..., { repeat: { pattern: '0 9 * * *' } })`로 매일 오전 9시 잡을 박아 두면, 워커가 살아 있는 동안 알아서 발화한다. Spring의 `@Scheduled`나 Quartz가 차지하던 자리다. 다만 한 가지 함정이 있다 — **single-instance cron은 Node 진영에서 거의 안 쓴다.** `node-cron` 같은 라이브러리로 단일 프로세스 안에서 cron을 돌리는 모양은, 컨테이너가 두 개 이상 뜨는 순간 한 잡이 두 번 발화한다. 회원 한 명에게 알림이 두 번 가고, 같은 인보이스가 두 번 발행되는 일이 생긴다. Redis 기반 distributed lock이나 BullMQ의 repeatable job처럼 "한 잡은 한 워커만 잡는다"는 보장이 박힌 도구를 쓰자. 잊지 말자.

운영 자리에서 한 가지 더 — BullMQ에는 **bull-board**라는 대시보드가 있다. 큐 상태, 진행 중인 잡, 실패한 잡, 재시도 이력을 한 화면에서 본다. Spring Batch Admin이 차지하던 자리에 가깝다. 운영팀이 들여다볼 수 있는 화면이 있다는 게 의외로 큰 차이를 낸다 — 새벽에 잡이 막혔을 때, 콘솔이 아니라 웹 화면에서 한 번 클릭으로 retry를 눌러 보고, 안 되면 dead letter로 밀어 둔다. 잡 큐를 운영하기로 마음먹은 첫날에 같이 띄워 두는 편이 낫다.

## WebSocket — Socket.IO와 `ws`, 그리고 STOMP의 자리

실시간 양방향 통신 자리도 보자. Spring 진영은 보통 두 가지 그림을 그린다. 하나는 raw WebSocket으로 직접 핸들러를 적는 모양이고, 다른 하나는 STOMP를 얹어 메시지 브로커(RabbitMQ, ActiveMQ)와 연결한 뒤 pub/sub 토픽을 다루는 모양이다. WebFlux + STOMP 조합이 후자의 대표다.

Node 진영도 두 갈래가 있다.

**Socket.IO**는 가장 보편적이다. 그런데 엄밀히 말하면 Socket.IO는 raw WebSocket이 아니다 — 자체 프레이밍과 룸(room), 네임스페이스, 자동 재연결, 폴리필(WebSocket이 안 되는 환경에서 long-polling으로 자동 폴백)까지 모두 들어 있다. 클라이언트 SDK도 `socket.io-client`라는 한 짝이 따로 있다. 좋게 말하면 박스 외 모든 게 다 들어 있고, 나쁘게 말하면 wire protocol이 표준 WebSocket이 아니라 자체 사양이다.

**`ws`**는 그 반대편이다. 최소한의 raw WebSocket 구현이다. 가볍고, 표준만 다루고, 직접 메시지 형식과 라우팅을 짜야 한다. Express의 자리에 가까운 도구다.

여기서 한 가지 자리가 비어 보인다 — Spring의 STOMP + RabbitMQ 통합처럼, 메시지 브로커와 WebSocket을 한 우산 아래 묶어 주는 표준 도구가 Node 진영에는 사실상 없다. 비슷하게 짜려면 직접 조립한다 — RabbitMQ 클라이언트(`amqplib`)나 Redis pub/sub을 한쪽에 두고, Socket.IO 어댑터(`@socket.io/redis-adapter`, `@socket.io/amqp-adapter`)로 인스턴스 간 메시지를 분배한다. 다중 인스턴스에서 같은 사용자에게 가는 메시지가 어느 컨테이너에 잡혀 있는지 모르는 문제(이른바 sticky session 문제)를 이 어댑터가 풀어 준다.

이 자리에서 한 가지 결정이 흔히 갈린다. 단순히 서버에서 클라이언트로 이벤트를 흘려보내기만 하는 일감이라면, WebSocket까지 안 가도 된다. **Server-Sent Events**(SSE)가 더 단순하다. HTTP 위에서 동작하고, 단방향이고, 자동 재연결도 표준에 박혀 있다. Spring WebFlux의 `Flux<ServerSentEvent>`가 차지하던 자리에, Node에서는 Express나 Fastify에서 응답 스트림을 그대로 쓰면 된다. 알림 한 방향 전송이라면 SSE가 충분하고, 그 위에 양방향이 진짜 필요해지는 자리에 Socket.IO를 들이는 편이 낫다.

Socket.IO를 운영하면서 가장 자주 마주치는 자리가 **메시지 라우팅과 인스턴스 간 분배**다. 사용자 A가 인스턴스 #1에 붙어 있고, 사용자 A에게 보낼 메시지를 인스턴스 #2가 만들어 냈다고 해 보자. 인스턴스 #2는 사용자 A가 어디 붙어 있는지 모른다. 이걸 풀어 주는 게 Redis adapter다 — Redis pub/sub을 통해 모든 인스턴스가 메시지를 듣고, 자기 쪽에 붙은 사용자만 골라 내려보낸다. Spring 진영의 RabbitMQ relay와 비슷한 자리에 Redis pub/sub이 박힌 모양이다. 그 차이가 운영 부담에 영향을 준다 — 메시지 영속성이 필요하면 RabbitMQ 쪽이 좀 더 두툼하고, 가벼운 fan-out이 필요하면 Redis 쪽이 단순하다.

WebSocket을 도입할 때 잊지 말 한 가지가 더 있다. **단일 스레드 + 이벤트 루프 모델은 장기 커넥션과 잘 맞는다.** Java가 스레드 1만 개를 띄우려면 메모리가 부담이지만, Node는 커넥션 1만 개를 같은 프로세스 안에서 거뜬히 든다. 이 자리는 가상 스레드(Project Loom)가 들어오기 전 Java가 끙끙거리던 자리이고, Node가 처음부터 잘하던 자리다. 다만 **메시지 처리 자체가 CPU 바운드라면 다시 단일 스레드가 발목을 잡는다** — 이때는 WebSocket 게이트웨이만 Node로 두고, 무거운 처리는 큐로 던진 뒤 별도 워커(또는 Java 마이크로서비스)에서 처리하는 모양이 자연스럽다.

## 서버리스 — Lambda, Vercel, Cloudflare Workers, 그리고 콜드 스타트의 본질

Spring Cloud Function의 자리다. 그런데 이 자리에서 Node와 Spring의 격차가 가장 크게 벌어진다. 말 그대로다.

기본 그림부터 그리자. 함수 하나를 클라우드에 올려 두고, 트래픽이 들어오면 그때 인스턴스가 깨어나 처리하고, 트래픽이 없으면 인스턴스가 사라진다. AWS Lambda, Vercel Functions, Cloudflare Workers가 모두 이 모양이다. 이때 핵심 지표가 **콜드 스타트** — 인스턴스가 막 깨어나서 첫 응답을 줄 때까지 걸리는 시간이다. 사용자가 "어 왜 느리지" 하고 느끼는 그 자리.

수치를 비교해 보자. **Spring Boot Lambda는 콜드 스타트가 보통 3~10초 걸린다.** SnapStart라는 기능을 켜면 약 1.5초까지 줄고, 잘 튜닝한 케이스는 180ms 근처까지 보고된다. 반면 **Node Lambda는 보통 200ms 미만이다.** 단순 함수라면 100ms도 흔하다. 이 격차가 본질적인 이유는 무엇일까. 한 줄로 말하면, **JVM은 클래스 로딩과 JIT 워밍업에 시간이 들고, Node는 그 단계가 거의 없기 때문이다.** Spring Boot가 들어가면 컴포넌트 스캔, Bean 생성, Spring AOT 처리까지 포함해 더 늘어난다. SnapStart는 메모리 스냅샷을 미리 떠 두는 트릭으로 그 시간을 줄이는 도구지, JVM의 본질을 바꾸지는 못한다.

이 격차가 왜 결정적이냐. 동기 사용자 응답 — 즉, 사람이 화면 앞에서 기다리는 자리에서는, 첫 응답이 3초 늦으면 그게 그대로 사용자 경험 손실이다. 들쭉날쭉한 트래픽(밤에 거의 0, 낮에 잠깐 폭주)을 가진 BFF에서는 늘 콜드 스타트가 발생한다. 이 모양에 Node가 강하다. 반대로 트래픽이 종일 평탄해서 인스턴스가 거의 늘 깨어 있는 모양이라면, 콜드 스타트는 거의 일어나지 않고 두 진영의 차이가 작아진다. 그 자리에는 컨테이너가 더 단순하다.

여기서 한 단계 더 나간 자리가 **Cloudflare Workers**다. Workers는 Lambda와도 모양이 다르다 — V8 isolate 단위로 함수가 격리되고, Node 런타임 전체를 띄우지 않는다. 콜드 스타트가 거의 0(수 ms)이고, 글로벌 엣지에서 동작한다. 다만 이 가벼움의 대가가 있다 — 일부 Node API와 무거운 라이브러리(예: Prisma의 일부 엔진)가 그대로 안 돌아간다. 이 부분은 5장 ORM 자리에서 다시 본다. **Drizzle**이 Workers·Edge에 가장 잘 맞는다는 평이 그래서 자리값을 한다.

서버리스가 Node와 자연스레 맞는 또 한 가지 이유가 있다. **이벤트 드리븐 모델**이다. SQS 메시지 도착, S3 객체 업로드, EventBridge 이벤트, Cron 트리거 — 이 모든 게 함수 한 번 실행을 트리거한다. Node의 함수가 곧 단위라는 모양이 그 사상에 맞는다. Spring Cloud Function이 같은 추상을 자바에서 풀려 했지만, 콜드 스타트가 발목을 잡는다. 사용자 응답이 없는 백그라운드 트리거라면 SnapStart로 충분히 가볍지만, 사용자가 기다리는 API라면 여전히 어렵다.

한 가지 더 짚어 둘 자리가 **DB 커넥션의 함정**이다. Lambda는 호출마다 새 인스턴스가 깨어날 수 있는데, 인스턴스마다 DB 커넥션을 만들면 — 트래픽이 폭주하는 순간 DB 커넥션 풀이 터진다. 이 자리를 풀려면 RDS Proxy나 PgBouncer 같은 connection pooler를 한 단계 끼우거나, 서버리스 친화적 DB(Neon, PlanetScale, Cloudflare D1)를 쓴다. Spring Boot에서는 HikariCP가 기본으로 깔려서 신경 쓰지 않던 자리가, 서버리스에서는 첫날부터 등장한다. 잊지 말자.

여기서 잊지 말 한 가지가 더 있다. **모든 서버리스가 답은 아니다.** 장기 커넥션(WebSocket의 그 자리), 메모리 캐시, 무거운 ORM(Prisma 같은), 분당 수만 RPS의 안정 트래픽 — 이런 자리는 컨테이너가 더 적합하다. 서버리스는 가격 모델이 호출당 + 실행 시간이라, 트래픽이 평탄해서 인스턴스가 늘 떠 있는 모양이라면 컨테이너 대비 더 비싸진다. 한 회고에서 "월 트래픽이 안정 RPS로 들어오기 시작하자, Lambda 청구서가 컨테이너 두 대보다 비싸졌다"는 패턴은 흔하게 보고된다. "들쭉날쭉한 트래픽 + 짧은 응답 + 이벤트 드리븐"이 서버리스의 강점 자리다. 그 자리에 Node가 자연스레 맞는다.

여기까지 보면 한 가지 그림이 그려진다. **Spring Cloud Function의 자리 자체는 Node가 더 잘 맞는다.** SnapStart로 1.5초까지 줄여도, Node 200ms와는 한 자릿수 차이가 그대로 남는다. 이 격차는 도구 튜닝의 문제가 아니라 런타임의 본성 문제다. Spring 출신이 처음 Lambda를 진지하게 도입할 때 "여긴 정직하게 Node로 가자"는 결론을 내는 경우가 흔한 이유다. 모놀리스 코어는 그대로 Spring으로 두고, Lambda는 Node로 다는 폴리글랏 절충 — 8장에서 다시 본다.

이 자리에서 한 가지 더 짚을 게 있다 — **번들 크기와 콜드 스타트의 관계**. Lambda의 콜드 스타트는 패키지 다운로드 + 런타임 부트 + 함수 초기화로 갈라지는데, 패키지가 두꺼우면 그 첫 단계가 늘어난다. 그래서 Node Lambda를 진지하게 운영할 때 esbuild로 트리 셰이킹을 거친 단일 번들로 묶는 모양이 흔하다. 같은 함수가 50MB로 부풀던 게 2MB로 줄면, 콜드 스타트가 또 한 단계 짧아진다. 이건 도구 자체의 트릭이 아니라 빌드 파이프라인의 결정인데, 이 결정이 의외로 운영 차이를 크게 만든다. Spring Boot Lambda에서는 jar가 본래 두툼하니 같은 트릭을 쓰기 어렵다는 점도 함께 짚자.

## 패턴은 어떻게 골라야 할까 — 산문으로 풀어 보자

여기까지 보면, 한 가지 질문이 가만히 떠오른다. 이 모든 자리 중에 우리는 어디를 디폴트로 두어야 할까. 결정 트리나 점수표로 풀고 싶지만, 실제로 그 모양이 잘 안 맞는다. 자리 선택은 트래픽 모양·팀 크기·운영 부담이라는 세 축이 함께 결정한다. 산문으로 풀어 보자.

먼저 트래픽 모양부터 보자. **트래픽이 종일 평탄하면 컨테이너가 자연스럽다.** Kubernetes나 Fly.io나 ECS에 컨테이너 두세 개 띄워 두고, 그 위에 Express 또는 Fastify를 얹는다. 콜드 스타트는 첫 배포 때만 한 번 일어나고, 그 뒤로는 늘 따끈한 인스턴스가 응답한다. 가격도 예측 가능하다. 반대로 **트래픽이 들쭉날쭉하면 서버리스가 자연스럽다.** 깊은 새벽엔 한 시간에 열 번 호출되고, 낮 한 시간엔 1만 번 호출되는 BFF — 컨테이너로 운영하면 평소엔 노는 인스턴스 비용이 들고, 폭주 때엔 오토스케일이 따라가지 못한다. Lambda나 Workers에 던져 두면 그 두 극단이 모두 자연스레 풀린다.

다음은 팀 크기다. **팀이 다섯 이하 + 마이크로서비스가 한두 개라면 Fastify 위에 가볍게 시작하는 편이 낫다.** NestJS의 모듈 그래프가 주는 안전망보다, Fastify의 가벼움이 주는 속도가 더 큰 자리다. 보일러플레이트가 적고, 새 사람이 들어와서 코드를 읽기 시작할 때 진입 장벽이 낮다. 인프랩이 8명 백엔드 팀에서 NestJS Monorepo로 옮긴 회고를 보면, 그 결정이 무거워지는 분기점이 어디쯤인지 보인다 — 입사자 학습 곡선, IDE 자동완성, 타입 안전, 인력 풀, 서드파티 호환성, 커뮤니티 자료. 이 여섯 가지가 부담으로 느껴지기 시작했다는 게 핵심이다. **팀이 다섯을 넘기고 도메인이 여러 개로 갈라지는 시점에 NestJS의 구조 강제가 짐을 덜어 준다.** 4장에서 정면으로 비교한다.

운영 부담도 함께 고려하자. **트래픽이 비교적 단순하고, 사용자 트랜잭션 직후의 후처리(이메일·푸시·웹훅·인덱싱)가 본체라면 BullMQ + 워커 컨테이너 한두 개로 충분하다.** 무거운 ETL이나 청크 트랜잭션이 본체라면 Spring Batch 쪽 사고 모델이 여전히 적합하다 — Node 진영의 자리값을 솔직히 인정하자. Airflow나 dbt 같은 별도 도구에 위임하는 모양도 흔하다. 실시간 양방향이 필요하면 Socket.IO가 디폴트, 단순 알림 한 방향이라면 SSE가 더 단순하고, raw WebSocket으로 가벼움이 우선이라면 `ws`다.

그 모든 결정 위에 한 가지 큰 원칙이 깔린다. **Node를 도구로 고를 때, 그 도구가 잘 맞는 자리에 일감을 둔다.** I/O가 본체이고, 외부 서비스 호출이 많고, 응답이 짧고, 트래픽이 변동성 있는 자리. LinkedIn이 BFF에서 30대를 3대로 줄였던 그 자리. 당근이 푸시알림에서 1,500 RPS를 단일 마이크로서비스로 흡수했던 그 자리. 이 자리들은 Node + 큐 모델 + 컨테이너의 조합이 거의 그대로 잘 맞는다.

반대로 CPU 바운드(이미지 변환, PDF 생성, 큰 정규식, 무거운 암호화), 청크 트랜잭션 ETL, 분당 수만 건의 안정적 동기 트래픽 — 이 자리는 Node의 강점 자리가 아니다. CPU 바운드는 worker_threads로 옮기거나 별도 마이크로서비스(다른 언어도 가능)로 분리하자. 청크 트랜잭션 ETL은 Airflow + dbt에 위임하거나 Spring Batch를 따로 두는 모양이 솔직하다. 큰 안정 트래픽은 Java/Spring 진영이 여전히 강하다. 한 진영이 모든 자리를 다 잘하는 게 아니라, 자리에 맞는 도구를 고르는 것뿐이다.

여기서 한국 회사들이 실제로 그 결정을 어떻게 풀어냈는지 짧게 환기해 보자. 당근마켓은 Ruby, Java, Python, Go, TypeScript 다섯 언어를 동시에 굴리던 시기를 겪고, 결국 두 축으로 정리했다 — 정형적 비즈니스 로직(채팅·피드·이미지·인프라)은 Go, 사용자 대면 서비스(광고·커머스·동네 프로모션)는 TypeScript. 결제·금융 영역은 Java를 그대로 유지하는 폴리글랏 절충이다. 네이버파이낸셜은 페이 플랫폼 직속팀에서 신규 DB 마이그레이션 프로젝트를 Node.js MSA로 풀고 — "Node.js로도 대규모 CPU 연산 검증 가능"이라는 결론을 내면서도 — 결제·신뢰성 도메인의 본진은 Spring을 그대로 두는 모양을 잡았다. 이 회사들이 보여 주는 결정의 본질은 같다. **언어를 하나로 통일하는 게 목표가 아니다. 자리에 맞는 도구를 두고, 운영 가능한 수(2~3개)로 줄이는 것이다.** 우리도 그 사고방식을 그대로 들고 가자.

마지막 자리 정리 표 하나로 이 절을 닫자. 본문에서 풀어낸 권고를 압축한 것이다.

| 일감 모양 | Node 진영의 디폴트 | 반대 자리(주의) |
|---|---|---|
| 동기 REST, 큰 도메인, 큰 팀 | NestJS (필요 시 Fastify 어댑터) | 작은 팀엔 과한 보일러플레이트 |
| 동기 REST, 짧은 수명, 작은 팀 | Fastify (또는 Express) | 큰 팀에선 일관성 부담 |
| GraphQL + N+1 위험 | NestJS + DataLoader (request scope) | 단일 화면 BFF엔 REST가 단순 |
| 사용자 후처리(이메일·푸시·웹훅·인덱싱) | BullMQ + 워커 컨테이너 | 무거운 ETL은 Airflow에 |
| 청크 트랜잭션 ETL | (그대로 Spring Batch 또는 Airflow) | Node에 강제로 옮길 자리 아님 |
| cron 스케줄 | BullMQ repeatable job | 단일 인스턴스 cron 금지 |
| 실시간 양방향 | Socket.IO + Redis adapter | 단방향이면 SSE로 충분 |
| 들쭉날쭉 BFF | Lambda / Workers | 평탄 트래픽엔 컨테이너 |
| 글로벌 엣지 | Cloudflare Workers + Drizzle | Node API 의존 라이브러리 호환성 확인 |
| 사내 CLI / 운영 도구 | commander + npm 배포 | 큰 CLI 도구는 oclif |

한 가지 더 — 사용자 응답이 끝난 뒤에 BullMQ 잡을 던지면, 그 잡이 처리되는 사이에 응답이 사용자에게 먼저 가 있다는 점도 잊지 말자. 만약 잡이 실패해도 사용자는 이미 "성공" 응답을 받은 상태다. 그래서 잡 안에서 발생하는 에러는 별도 채널(슬랙 알림, Sentry, 운영 대시보드)로 흘려보내는 모양이 거의 의무에 가깝다. 이 자리값을 이른 단계에 잡아 두지 않으면, 나중에 "메일이 안 갔다"는 사용자 문의를 추적하다가 한 번씩 끔찍한 시간을 보내게 된다.

## 마무리 — NestJS의 자리 앞에서

이 장에서 우리가 그린 지도에는 자리마다 도구가 있고, 그 자리값을 한 사례도 함께 두었다. Spring 출신이 Node로 넘어올 때 자주 겪는 첫 혼란이 "도구가 너무 많다"인데, 사실 자리는 그리 많지 않다. **REST·GraphQL·CLI·워커·WebSocket·서버리스** — 여섯 자리고, 각 자리에 둘셋의 후보가 있을 뿐이다. 자리부터 보면 길을 잃지 않는다. 어떤 도구를 쓸까가 아니라, 어느 자리에 어떤 일감을 둘까로 사고하자.

다시 돌아보면, 이 장에서 우리가 만난 메시지는 한 줄로 줄어든다 — **Node는 I/O 친화적인 일감에 본성이 맞고, 그 자리에서는 Spring보다 가볍고 빠르며, 그 자리 밖에서는 솔직하게 다른 도구에 자리를 내주는 게 낫다.** LinkedIn이 BFF에서 30대를 3대로 줄였던 자리, 당근이 푸시알림 1,500 RPS를 단일 마이크로서비스로 흡수한 자리, Lambda 콜드 스타트 200ms와 3초의 격차가 결정적이었던 자리 — 이 세 그림이 같은 메시지를 가리킨다. 도구는 자리에 맞춰 고른다. 도구만 바뀐다고 우리가 백엔드 개발자가 아닌 다른 무엇이 되는 건 아니다. 같은 사고방식으로, 다른 모양의 도구를 쓰는 것뿐이다.

이 지도 위에서 한 자리만은 정면으로 더 들여다볼 가치가 있다. **NestJS다.** 이 장에서 우리는 NestJS가 REST의 한 도구이고, GraphQL에서 DI로 N+1을 푸는 도구이며, 모듈·인터셉터·가드의 모양이 Spring과 닮아 있다는 점까지만 봤다. 그러나 진짜 정면 비교는 아직 시작도 하지 않았다. 모듈 그래프는 어떻게 그려야 하고, `forwardRef`는 언제 등장하고, 인터셉터·가드·파이프는 Spring의 `HandlerInterceptor`·`Filter`·`@Valid`와 어디까지 같고 어디서 갈라지는가. "Nest의 DI는 진짜 DI인가" 같은 정직한 질문도 회피하지 않고 다뤄야 한다. PayPal이 Express의 자유로움을 Kraken.js로 강제했던 자리에서, NestJS는 처음부터 그 강제를 박아 두었다 — 그 강제가 짐인지 안전망인지를 가름하는 자리에 다음 장이 놓인다. 거기에 NestJS 테스트의 자리(`@nestjs/testing` ↔ `@SpringBootTest`)까지 더해야 비로소 그림이 완성된다. 다음 장에서 가장 닮은 두 프레임워크를 정면으로 마주 세워 보자.
