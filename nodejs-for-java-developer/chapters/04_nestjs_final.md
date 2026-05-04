# 4장. NestJS와 Spring Boot — 가장 닮은 두 프레임워크의 정면 비교

> **모듈, DI, 데코레이터, 인터셉터·가드, 그리고 테스트 — Spring Boot 출신의 통념이 흔들리는 자리**

PayPal의 한 엔지니어가 사내 회고에 적은 한 문장이 오래도록 머릿속을 맴돈다. "Express는 너무 자유로워서 큰 팀에서는 자유가 곧 혼돈이 되었다." 처음에는 가벼움이 매력이었다. 미들웨어 한 줄과 라우트 한 줄이면 서버가 떴다. 그러나 팀이 커지고, 서비스가 늘고, 새로 들어오는 엔지니어가 매주 한두 명씩 추가되기 시작하자, 같은 폴더 구조라는 게 자연스럽게 합의되지 않는다는 사실이 드러났다. 누구는 라우트를 컨트롤러에 두고, 누구는 미들웨어 안에 썼다. 누구는 비즈니스 로직을 서비스로 빼고, 누구는 라우트 안에 그대로 박았다. 결국 PayPal은 사내에서 `Kraken.js`라는 컨벤션 강제 프레임워크를 따로 만들었다. Express가 가진 비강제성(non-prescriptive)을 자기 팀의 일관성으로 메운 것이다. 자유의 대가가 만만치 않았다는 정직한 회고다.

같은 시기, 지구 반대편의 어느 1인 개발자는 이런 글을 적었다. "Spring Boot 한 인스턴스가 t2.micro에서 무부하 상태로 27~29% CPU를 먹는다. NestJS로 옮긴 뒤 6~7%로 떨어졌고, 같은 인스턴스에서 작은 앱 4~5개를 동시에 띄울 수 있게 됐다." 큰 회사 이야기가 아니라 작은 사이드 프로젝트 이야기다. JVM의 따뜻한 워밍업과 두꺼운 클래스로더가 가져다주는 안정감이, 작은 인스턴스 위에서는 그 자체로 비용이라는 것. 같은 도메인을 NestJS로 옮기자 메모리 풋프린트와 부팅 시간이 한꺼번에 줄어드는 그림. 둘은 다른 종류의 회고지만, 한 가지 공통점이 있다. **Spring 출신이 Node 진영에서 처음 자연스러움을 느끼는 자리는 거의 항상 NestJS다.**

그래서 이 장은 두 프레임워크를 정면으로 마주 세운다. PayPal이 Express에서 느꼈던 "구조 강제의 필요성"과, t2.micro 후기가 보여준 "가벼움의 약속"을 한 도입에서 같이 들고 간다. NestJS는 그 둘을 한꺼번에 내미는 도구다. Spring과 거의 같은 모양의 모듈·DI·데코레이터·인터셉터·가드를 들고 있어 일관성 강제에는 강하고, JVM 부팅 비용 없이 가볍게 뜨므로 컨테이너 운영에는 산뜻하다. 그렇다면 진짜 차이는 어디에 있을까? 어디서 Spring이 그리워지고, 어디서 NestJS가 더 가뿐할까? 이 장에서 우리가 풀어볼 질문은 단순하다. **Spring Boot 출신이 NestJS를 처음 쓸 때 가장 자주 데이는 지점은 어디인가? 그리고 어디서 두 프레임워크가 정직하게 갈라지는가?**

8장에서 다시 만나는 PayPal의 마이그레이션 수치(2배 RPS, 35% 응답 감소, 33% 적은 코드)는 이 장의 결정과는 별개의 차원이다. 4장에서 우리가 짚을 것은 그 결정의 도구 — NestJS 그 자체다. 코드 한 페이지 한 페이지에서 Spring과 어떻게 닮았고 어디서 갈라지는지를 손에 익히는 일이 이 장의 일이다.

## 공통 DNA — 모듈, 컨트롤러, 서비스

처음 NestJS의 코드를 열어 본 Spring 출신은 거의 예외 없이 같은 반응을 보인다. "어디서 본 그림이다." 모듈이 있고, 컨트롤러가 있고, 서비스가 있다. 컨트롤러에는 `@Controller`가 붙고, 서비스에는 `@Injectable`이 붙고, 라우트에는 `@Get`, `@Post`가 붙는다. Spring의 `@Service`, `@Repository`, `@RestController`, `@GetMapping`, `@PostMapping`을 그대로 옮겨다 놓은 것 같은 풍경이다.

직방의 한 엔지니어가 적은 1:1 매핑표는 이 인상을 그대로 보여 준다. `@Controller`는 그대로 `@Controller`로 옮겨오고, `@Bean`은 `@Injectable`로 옮겨오며, IoC Container는 NestJS의 Module로 옮겨온다. `@Interceptor`는 `NestInterceptor`, Exception Handler는 Exception Filter, Argument Resolver와 Validator는 Pipe, Spring Security의 권한 처리는 Guard로 매핑된다. 데코레이터의 이름과 자리만 살짝 다를 뿐, 한 칸에 한 칸을 그대로 끼워 넣을 수 있다. Spring으로 5년을 굴려 온 손이 NestJS 코드 베이스에 들어와 일주일 안에 익숙해진다는 회고가 우연이 아니다.

깊은 자리에서 보면 닮음은 더 분명해진다. 두 프레임워크 모두 **DI 컨테이너**가 핵심이다. 부팅 시점에 의존성 그래프를 빌드하고, 런타임에는 `new`를 직접 호출하지 않는다. 두 프레임워크 모두 **데코레이터(또는 어노테이션) 기반의 메타데이터 모델**을 쓴다. 라우팅·검증·인터셉트·권한 같은 횡단 관심사가 코드 위에 메타데이터로 박히고, 프레임워크가 그것을 읽어 동작한다. 두 프레임워크 모두 **AOP스러운 횡단 관심사 분리**를 자기 식으로 들고 있다. Spring의 `@Aspect`·`HandlerInterceptor`·`Filter`·`@Valid`가 가진 자리에, NestJS는 인터셉터·가드·파이프·예외 필터를 둔다. 이름이 달라도 푸는 문제는 같다 — 비즈니스 코드 안에 인증·검증·로깅·트랜잭션 같은 코드를 쏟아 내지 않고, 데코레이터 한 줄로 분리하기.

이 닮음을 정직하게 인정하고 넘어가자. Spring/Kotlin으로 20년을 굴려 온 어느 시니어가 NestJS로 옮긴 뒤 적은 글에 이런 문장이 있다. "Express만 쓰면 Spring DI가 그립지만 NestJS는 익숙한 모양을 그대로 준다." 이 한 줄이 NestJS의 정체성이다. **Express의 가벼움 위에, Spring의 구조를 얹은 도구.** 그래서 Spring 출신에게 학습 곡선이 가장 부드러운 Node 프레임워크이고, 그래서 또한 한국에서 토스·당근마켓·인프랩·직방 같은 회사들이 차례로 NestJS를 본격 운영하게 된 배경이다.

라우트 한 줄이 어떻게 닮았는지 짧은 코드로 비교해 보자. 같은 GET 핸들러를 양쪽 프레임워크로 짜면 거의 거울처럼 보인다.

```kotlin
// Spring (Kotlin) — RestController 한 줄
@RestController
@RequestMapping("/orders")
class OrderController(private val service: OrderService) {

    @GetMapping("/{id}")
    fun get(@PathVariable id: Long): OrderDto =
        service.findById(id) ?: throw NotFoundException()
}
```

```typescript
// NestJS — 거의 거울 모양
@Controller('orders')
export class OrderController {
  constructor(private readonly service: OrderService) {}

  @Get(':id')
  async get(@Param('id', ParseIntPipe) id: number): Promise<OrderDto> {
    const found = await this.service.findById(id);
    if (!found) throw new NotFoundException();
    return found;
  }
}
```

`@RestController` ↔ `@Controller`, `@RequestMapping("/orders")` ↔ `@Controller('orders')`, `@GetMapping("/{id}")` ↔ `@Get(':id')`, `@PathVariable id: Long` ↔ `@Param('id', ParseIntPipe) id: number`. 매핑이 거의 한 칸씩 비낀 채로 그대로 통한다. `ParseIntPipe`가 NestJS 쪽에서 약간 더 명시적이긴 한데(Spring에서는 `Long`으로 자동 변환되지만 NestJS는 number로의 변환을 파이프로 명시한다), 한 번 손에 익으면 자연스럽다. 생성자 주입의 모양도, 예외를 throw해 프레임워크가 잡아 주는 모양도, 모두 같은 자리에 있다.

그렇다면 이렇게 닮았다는 건 어디서 끝나는가. 정직한 차이의 자리부터 들여다보자.

## 차이 1 — 클래스패스 컴포넌트 스캔과 명시적 모듈 그래프

Spring과 NestJS가 결정적으로 갈라지는 첫 자리는 **의존성 그래프를 어떻게 구성하는가**다. Spring은 우리가 익숙한 그림으로 일을 한다 — 클래스패스를 훑어 `@Component`, `@Service`, `@Repository`, `@RestController`가 붙은 클래스들을 자동으로 빈으로 등록한다. `@SpringBootApplication`이 자동으로 `@ComponentScan`을 깔아 주고, 패키지 트리 안의 모든 후보를 자동으로 발견한다. 새 서비스를 추가할 때 우리가 하는 일은 `@Service` 한 줄을 다는 것이다. 부모 어딘가의 빈 정의 파일에 새 항목을 추가할 일이 거의 없다. 마법 같다고 느끼는 사람도 있고, 예측할 수 없다고 불평하는 사람도 있다. 어쨌든 모양은 그렇다.

NestJS는 다른 길을 택했다. **`@Module` 데코레이터 안에 `imports`/`providers`/`controllers`/`exports`를 직접 적는 명시적 그래프**를 강제한다. 컴포넌트 스캔은 없다. 새 서비스를 만들면 `@Injectable`을 붙이는 것만으로는 부족하다. 그 서비스를 어느 모듈의 `providers` 배열에 등록할지를 직접 적어야 한다. 다른 모듈이 그것을 쓰려면, 정의한 모듈의 `exports`에 추가하고, 사용하는 모듈의 `imports`에 그 모듈을 등록해야 한다.

같은 도메인을 두 프레임워크로 짜 보면 차이가 한눈에 들어온다. 사용자 등록 도메인을 단순화한 코드다.

```java
// Spring Boot — UserService
package com.example.users;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;

@Service
public class UserService {
    private final UserRepository repository;
    private final EmailService emailService;

    public UserService(UserRepository repository, EmailService emailService) {
        this.repository = repository;
        this.emailService = emailService;
    }

    public User register(String email, String name) {
        User user = repository.save(new User(email, name));
        emailService.sendWelcome(user);
        return user;
    }
}

// UserController
@RestController
@RequestMapping("/users")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping
    public User create(@RequestBody RegisterRequest req) {
        return userService.register(req.email(), req.name());
    }
}
```

같은 코드를 NestJS로 옮겨 보자.

```typescript
// users.service.ts
import { Injectable } from '@nestjs/common';
import { UserRepository } from './user.repository';
import { EmailService } from '../email/email.service';

@Injectable()
export class UserService {
  constructor(
    private readonly repository: UserRepository,
    private readonly emailService: EmailService,
  ) {}

  async register(email: string, name: string) {
    const user = await this.repository.save({ email, name });
    await this.emailService.sendWelcome(user);
    return user;
  }
}

// users.controller.ts
import { Body, Controller, Post } from '@nestjs/common';
import { UserService } from './users.service';

@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post()
  create(@Body() dto: { email: string; name: string }) {
    return this.userService.register(dto.email, dto.name);
  }
}

// users.module.ts — 여기가 핵심이다
import { Module } from '@nestjs/common';
import { UserController } from './users.controller';
import { UserService } from './users.service';
import { UserRepository } from './user.repository';
import { EmailModule } from '../email/email.module';

@Module({
  imports: [EmailModule],
  controllers: [UserController],
  providers: [UserService, UserRepository],
  exports: [UserService],
})
export class UsersModule {}
```

코드 양만 보면 NestJS 쪽이 약간 길다. `users.module.ts` 파일 한 개를 새로 적어 줘야 하기 때문이다. Spring에서는 `@Service`와 `@RestController` 어노테이션 두 줄로 끝났을 일이, NestJS에서는 모듈 파일에 `controllers: [UserController], providers: [UserService, UserRepository]`를 적어 주는 보일러플레이트가 추가된다. `EmailModule`이라는 외부 모듈을 쓰려면 `imports`에 등록하고, 자기 서비스를 다른 모듈에 노출하려면 `exports`에 등록한다.

처음에는 이 보일러플레이트가 살짝 번거롭게 느껴진다. "어차피 클래스패스 다 훑어주면 되지 왜 매번 적게 하지?" 같은 의문이 자연스럽게 든다. 직방의 회고에서도 정확히 이 표현이 나온다. "명시성은 높지만 보일러플레이트는 더 많다." 그러나 이 명시성에는 정직한 보상이 따른다. **첫째, 의존성 그래프가 코드 위에 보인다.** 어느 모듈이 어느 모듈을 쓰는지가 `imports` 배열을 보면 바로 읽힌다. Spring에서 컴포넌트 스캔 결과를 IDE의 Bean 그래프 도구로 떠봐야 알던 것이, NestJS에서는 모듈 파일 한 개에 박혀 있다. **둘째, 패키지 안에 들어 있다고 자동으로 등록되지 않는다.** 같은 폴더에 빈처럼 보이는 클래스를 둬도, 모듈에 등록하지 않으면 컨테이너 입장에서는 존재하지 않는 것이다. 의도하지 않은 빈이 자동 등록되는 일이 없다. **셋째, 순환 의존이 코드 위에 드러난다.** A 모듈이 B 모듈을, B 모듈이 다시 A 모듈을 `imports`로 부르면 NestJS는 부팅 시점에 그 사실을 알려 주고, `forwardRef`를 쓰라고 지시한다. Spring에서도 순환 의존이 일어나지만, 코드 위에 가시화되지 않은 채 런타임 BeanCurrentlyInCreationException으로 새벽 두 시에 만나기도 한다.

명시성과 자동성, 어느 쪽이 더 좋은가는 단정하기 어렵다. 작은 서비스에서는 자동 스캔이 가벼워서 좋고, 큰 모듈 그래프에서는 명시적 등록이 깔끔해서 좋다. 다만 한 가지는 분명하다 — **NestJS의 `@Module`은 의존성 그래프를 코드 위에 박아 두기로 한 설계다.** 이 사상을 받아들이고 모듈 파일 한 개를 더 적는 데 익숙해지는 게, NestJS의 첫 학습 단계다.

여기서 잠깐, "그래도 매번 모듈 파일을 적는 게 번거로운데" 싶다면 NestJS CLI를 쓰자. `nest g module users`, `nest g controller users`, `nest g service users` 한 줄씩이면 빈 파일이 자동 생성되고, 부모 모듈에 자동 등록까지 된다. Spring Initializr가 프로젝트 스켈레톤을 만들어 주는 것과 비슷한 자리에서, 이 CLI는 모듈 단위 스켈레톤을 만들어 준다. 명시성을 받아들이되, 손은 가볍게 둘 수 있다.

## 차이 2 — 자바 어노테이션과 TS 데코레이터, 그리고 reflect-metadata의 자리

두 프레임워크가 메타데이터 모델 위에 서 있다는 점은 닮았지만, 그 메타데이터를 어떻게 보존하는지는 갈라진다. Java의 어노테이션은 컴파일된 바이트코드의 표준 위에 박힌다. `@Service`라고 적으면 컴파일된 `.class` 파일의 attribute로 들어가, 런타임에 리플렉션으로 읽을 수 있다. JVM 표준이 받쳐 주는 탄탄한 모델이다.

TypeScript의 데코레이터는 사정이 다르다. JavaScript 표준 자체가 데코레이터를 정식 사양으로 받은 게 비교적 최근의 일이고(stage 3을 오래 끌었다), TypeScript는 `experimentalDecorators` 플래그를 켜야 데코레이터를 켤 수 있다. 그리고 거기서 끝이 아니다. 컴파일된 JS 코드는 `@Injectable()` 같은 데코레이터를 단순히 함수 호출로 변환할 뿐, "이 클래스의 생성자가 어떤 타입의 인자를 받는다"는 정보를 자동으로 보존하지 않는다. NestJS의 DI 컨테이너가 동작하려면 그 정보가 반드시 있어야 한다. `UserService`의 생성자가 `UserRepository`와 `EmailService`를 받는다는 사실을, 컴파일된 JS는 어디에 적어 둘까?

여기서 등장하는 게 **`reflect-metadata`** 라이브러리다. `tsconfig.json`에 `"emitDecoratorMetadata": true`를 켜면, TypeScript 컴파일러가 데코레이터가 붙은 클래스에 한해 `design:paramtypes`라는 메타데이터를 함께 내보낸다. 이 메타데이터는 `Reflect.metadata` API를 통해 런타임에 읽을 수 있고, NestJS는 이 정보를 보고 "아, 이 클래스의 생성자에 이 두 타입을 주입해야 하는구나"를 결정한다. NestJS의 DI는 표면적으로 Spring과 똑같은 모양이지만, 그 밑단에는 TypeScript 컴파일러와 `reflect-metadata`가 받쳐 주는 약간 더 위태로운 토대가 있다.

이 위태로움이 가끔 표면으로 올라오기도 한다. 인터페이스 타입을 생성자 인자로 적었을 때다. TS의 인터페이스는 컴파일 후 사라진다. `paramtypes`에는 `Object` 정도로만 남는다. NestJS는 이 경우 어떤 구현체를 주입해야 할지 알 수 없다. Spring에서는 인터페이스 타입으로 빈을 주입받는 게 자연스러운 일이지만, NestJS에서는 인터페이스가 아니라 클래스 또는 별도의 토큰(`Symbol` 또는 string)을 사용한다. 처음 만나면 살짝 난감하지만, 한 번 정리하면 두 번째부터는 의식하지 않게 된다.

토스의 한 엔지니어가 데코레이터를 깊게 다룬 글에는 이 메타데이터 모델을 응용하는 사례가 잘 정리돼 있다. NestJS의 `DiscoveryModule`을 통해 모든 등록된 프로바이더를 순회하고, 그중에서 자신이 정의한 커스텀 데코레이터(예: `@Cron`)가 박힌 메서드를 찾아내, 별도의 스케줄러에 등록하는 패턴이다. Spring AOP에서 `@Pointcut`으로 어드바이스를 거는 그림과 거의 같은 일을 — 다만 데코레이터 메타데이터 + DiscoveryModule + 프로토타입 순회의 조합으로 — 한다. Spring이 가진 AOP의 표현력은, NestJS에서도 이 조합을 이해하면 충분히 재현 가능하다는 사실은 정직하게 받아들여 둘 만하다.

다만 짚어 두자. **NestJS의 데코레이터는 Java 어노테이션만큼 표준화돼 있지 않다.** 데코레이터 사양이 표준 JS로 안착해 가는 도중이라, 라이브러리에 따라 데코레이터를 호출하는 시점이나 인자 모양이 살짝씩 달라질 수 있다. `tsconfig.json`의 `experimentalDecorators`와 `useDefineForClassFields` 같은 플래그들이 의외의 방식으로 부딪치기도 한다. Spring에서는 거의 신경 쓸 일이 없던 빌드 설정이, NestJS에서는 한 번씩 관심을 요구한다. 이게 이 도구의 가장 위태로운 토대 중 하나라는 걸 잊지 말자.

## 차이 3 — 생태계 두께, 그리고 시작 시간과 메모리의 역전

세 번째 차이는 두 프레임워크가 들고 있는 **생태계의 두께**다. Spring은 20년 가까이 자라 온 거대한 생태계를 가진다. `@Transactional` AOP, Spring Cache, Spring Batch, Spring Security, Spring Data, Spring Cloud, Spring Integration… 거의 모든 엔터프라이즈 관심사에 대해 잘 다듬어진 모듈이 자리잡고 있다. 새 요구가 들어와도 검색 한 번이면 표준화된 풀이 방식이 나온다. 그 자리에 있는 안정감은, 한 번 익숙해지면 다른 도구로 옮길 때 강하게 그리워진다.

NestJS는 그 자리에 한참 못 미친다. 트랜잭션은 ORM(Prisma·TypeORM·Drizzle) 쪽에 위임하고, 캐시는 `@nestjs/cache-manager`라는 얇은 래퍼를 통해 Redis나 in-memory를 붙인다. 배치는 사실상 NestJS 표준이 없고, BullMQ 같은 큐 라이브러리를 직접 가져다 쓴다. 시큐리티는 Passport.js와 `@nestjs/passport`로 상당 부분을 풀지만, Spring Security의 method-level 권한 처리만큼 잘 정리된 도구는 아니다. Spring 진영에서 익숙했던 한 줄짜리 어노테이션이, NestJS에서는 가드 + 커스텀 데코레이터 + 메타데이터의 조합으로 직접 짜야 하는 자리가 종종 나온다.

이 격차를 단점으로만 받아들일지, 아니면 다른 식으로 풀지는 사용자의 자세에 달렸다. 어느 Spring/Kotlin 시니어는 NestJS로 옮기면서 적은 글에서 이렇게 말했다 — "Spring/Kotlin의 견고함을 그리워하는 순간이 분명히 있다. 다만 그 그리움은 도구 자체보다는 사용자가 가진 운영 경험의 누적에 대한 것이다." 정직한 표현이다. NestJS의 가벼운 생태계는 한편으로 자유를 준다. 트랜잭션 모델을 ORM 단위로 자기에게 맞게 짜고, 캐시 정책을 명시적으로 컨트롤하고, 시큐리티를 도메인에 딱 맞춰 작성하는 일이 가능해진다. Spring이 깔아 둔 표준이 어떤 자리에서는 과한 추상이었다는 걸, NestJS의 가벼움 위에서 다시 보게 되기도 한다.

그리고 이 가벼움은 운영에서 정직하게 보상을 준다. 앞서 도입에서 인용한 t2.micro 후기 — 무부하 27~29% CPU가 6~7%로 떨어졌고, 같은 인스턴스에서 4~5개 앱을 동시 운영할 수 있게 됐다는 — 가 그 보상의 한 가지 모양이다. 네이버파이낸셜이 페이 플랫폼을 옮긴 회고에서도 같은 그림이 나온다. **유휴 인스턴스 메모리 비교: Java Spring ≈ 400MB vs Node.js ≈ 25MB.** K8s 위에서 컨테이너 단위로 가로 확장하는 시대에, 한 컨테이너의 메모리 풋프린트는 곧 비용이다. 16배 차이는 작은 차이가 아니다. 람다 콜드 스타트도 마찬가지다 — Spring Boot가 3~10초(SnapStart로 1.5초까지) 걸리는 자리에서 Node.js는 200ms 미만이다. 동기 사용자 응답 경로에 람다를 쓰는 순간, 이 차이는 결정적인 차원이 된다.

요약하면 이렇다. **Spring은 생태계 두께가 낫고, NestJS는 시작 시간과 메모리에서 우위다.** 어느 쪽이 결정적인지는 우리가 풀고 있는 문제에 따라 다르다. 큰 모놀리스에 트랜잭션·배치·시큐리티·통합이 모두 필요한 자리라면 Spring 생태계의 깊이가 짐을 덜어 준다. BFF, 마이크로서비스, 람다 함수, 컨테이너 가로 확장이 본진인 자리라면 NestJS의 가벼움이 운영 비용을 덜어 준다. 두 도구가 같은 자리를 두고 다투기보다, 자기에게 맞는 자리에서 강하다.

## 인터셉터·가드·파이프 — Spring의 횡단 관심사를 옮겨심기

NestJS가 Spring 출신에게 가장 자연스럽게 다가오는 자리가 바로 **횡단 관심사 처리**다. Spring에서 우리가 익숙했던 도구들 — `HandlerInterceptor`, `Filter`, `MethodSecurity`의 `@PreAuthorize`, `@Valid` + `Validator` — 가 NestJS에서는 인터셉터·가드·파이프의 세 갈래로 다시 정리된다. 이름이 다르지만 사고 회로는 거의 같다.

매핑을 정직하게 정리하면 이렇다.

- Spring `HandlerInterceptor` ↔ NestJS `Interceptor` — 요청 전후의 횡단 처리, 응답 변환, 캐싱.
- Spring Servlet `Filter` ↔ NestJS `Middleware` — Express 미들웨어 그대로의 자리, 요청 raw 단계의 처리.
- Spring `@PreAuthorize`, `@Secured` ↔ NestJS `Guard` — 권한 결정, 인증 체크.
- Spring `@Valid` + `Validator` ↔ NestJS `Pipe` (특히 `ValidationPipe`) — 입력 검증과 변환.
- Spring `@ControllerAdvice` + `@ExceptionHandler` ↔ NestJS `Exception Filter` — 예외를 일관된 응답으로 변환.

이 다섯 자리가 거의 1:1로 매핑된다. Spring 출신이 NestJS의 횡단 관심사 코드에 빠르게 적응하는 이유다.

다만 한 가지 차원에서는 맛이 다르다. Spring의 횡단 관심사는 AOP 위에 서 있다. `@Aspect`와 `@Around`는 그 자체로 메서드 호출을 가로채는 강력한 도구이고, `@Transactional` 같은 표준 어노테이션도 결국 AOP 프록시의 산물이다. 클래스 레벨에서 메서드 호출을 가로채 트랜잭션을 시작하고, 예외 시 롤백하고, 끝나면 커밋한다. 이 그림이 너무 자연스러워서, 우리는 종종 이게 마법인지 인지하지 못한다.

NestJS에는 이런 일반화된 AOP는 없다. 인터셉터·가드·파이프는 모두 컨트롤러 메서드의 진입·진출 경로에 박히는 도구이고, 클래스 안의 임의 메서드 호출을 가로채는 기능은 표준에 없다. 그래서 Spring의 `@Transactional`처럼 서비스 메서드에 한 줄 어노테이션만 박으면 트랜잭션이 자동으로 동작하는 그림은, NestJS에서는 자연스럽지 않다(5장에서 본격적으로 마주한다). 트랜잭션은 ORM의 명시적 호출(`prisma.$transaction([...])`)로 굴리고, 메서드 단위 권한 체크는 가드 + 커스텀 데코레이터의 조합으로 표현하는 게 NestJS의 자연스러움이다.

매핑을 한 줄짜리 코드로 한 번 더 살펴보자. Spring Security의 `@PreAuthorize`와 NestJS의 가드 + 커스텀 데코레이터는 이렇게 거울이 된다.

```java
// Spring Security — 메서드 레벨 권한
@RestController
@RequestMapping("/admin")
public class AdminController {

    @PreAuthorize("hasRole('ADMIN')")
    @GetMapping("/users")
    public List<User> list() { return userService.findAll(); }
}
```

```typescript
// NestJS — 커스텀 @Roles 데코레이터 + RolesGuard
@Controller('admin')
@UseGuards(JwtAuthGuard, RolesGuard)
export class AdminController {
  constructor(private readonly userService: UserService) {}

  @Roles('ADMIN')
  @Get('users')
  list() {
    return this.userService.findAll();
  }
}
```

NestJS 쪽이 약간 손이 더 간다. `@Roles('ADMIN')`이라는 메타데이터를 붙이고, 그것을 읽어 권한을 결정하는 `RolesGuard`를 직접(또는 라이브러리로) 만들어 둬야 한다. Spring Security가 SpEL로 `hasRole('ADMIN')`을 한 줄에 표현하던 그 자리에 NestJS는 가드 + 데코레이터 + `Reflector`의 조합이 들어선다. 작은 보일러플레이트지만, 한 번 만들어 두면 그다음부터는 한 줄로 끝난다. 표현력은 동등하고, 다만 표준 도구의 두께가 다르다.

자, 이제 코드로 들어가 보자. 사용자 등록 API에 (1) JWT 인증 가드, (2) 요청·응답 로깅 인터셉터, (3) DTO 검증 파이프를 한 모듈에 묶는 그림이다.

```typescript
// jwt-auth.guard.ts — Spring의 SecurityFilter + @PreAuthorize 자리
import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { Request } from 'express';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(private readonly jwt: JwtService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const req = context.switchToHttp().getRequest<Request>();
    const auth = req.headers.authorization;
    if (!auth?.startsWith('Bearer ')) {
      throw new UnauthorizedException('missing bearer token');
    }
    try {
      const payload = await this.jwt.verifyAsync(auth.slice(7));
      (req as any).user = payload;
      return true;
    } catch {
      throw new UnauthorizedException('invalid token');
    }
  }
}

// logging.interceptor.ts — Spring의 HandlerInterceptor 자리
import {
  CallHandler,
  ExecutionContext,
  Injectable,
  Logger,
  NestInterceptor,
} from '@nestjs/common';
import { Observable, tap } from 'rxjs';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  private readonly logger = new Logger(LoggingInterceptor.name);

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const req = context.switchToHttp().getRequest();
    const start = Date.now();
    return next.handle().pipe(
      tap(() => {
        const ms = Date.now() - start;
        this.logger.log(`${req.method} ${req.url} ${ms}ms`);
      }),
    );
  }
}

// register.dto.ts — Spring의 @Valid + JSR-303 자리
import { IsEmail, IsString, MaxLength, MinLength } from 'class-validator';

export class RegisterDto {
  @IsEmail()
  email!: string;

  @IsString()
  @MinLength(2)
  @MaxLength(50)
  name!: string;
}

// users.controller.ts — 한 컨트롤러에 셋을 묶는다
import {
  Body,
  Controller,
  Post,
  UseGuards,
  UseInterceptors,
  UsePipes,
  ValidationPipe,
} from '@nestjs/common';
import { JwtAuthGuard } from './jwt-auth.guard';
import { LoggingInterceptor } from './logging.interceptor';
import { RegisterDto } from './register.dto';
import { UserService } from './users.service';

@Controller('users')
@UseInterceptors(LoggingInterceptor)
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post('register')
  @UseGuards(JwtAuthGuard)
  @UsePipes(new ValidationPipe({ whitelist: true, transform: true }))
  register(@Body() dto: RegisterDto) {
    return this.userService.register(dto.email, dto.name);
  }
}
```

이 코드를 처음 보는 Spring 출신은 거의 자동으로 머릿속에서 매핑이 된다. `@UseGuards`는 `@PreAuthorize`의 자리, `@UseInterceptors`는 `HandlerInterceptor` 등록의 자리, `@UsePipes(new ValidationPipe(...))`는 `@Valid` + JSR-303 검증의 자리다. `class-validator`라는 라이브러리는 Hibernate Validator(Bean Validation)와 거의 같은 데코레이터 어휘를 갖는다 — `@IsEmail`, `@MinLength`, `@MaxLength`, `@IsNotEmpty`. Spring 출신이 보면 거의 이질감이 없다.

그렇다고 차이가 없는 건 아니다. 첫째, **NestJS의 Pipe는 Spring의 Validator보다 일을 하나 더 한다.** `transform: true` 옵션을 켜면, 요청 body를 단순한 plain object가 아니라 `RegisterDto` 클래스 인스턴스로 변환한다. 컨트롤러 메서드 안에서 `dto.email`이 그냥 string이 아니라, 데코레이터 메타데이터를 들고 있는 클래스 인스턴스가 된다. 이게 의외로 강력하다 — 검증과 변환이 한 도구에 묶인다. 둘째, **NestJS의 Interceptor는 RxJS Observable 위에 서 있다.** Spring 출신에게는 약간 낯선 모양이다. 응답 변환이 `pipe(tap(...))` 형태로 나오고, 비동기 합성도 RxJS 연산자로 푼다. WebFlux의 Project Reactor와 닮았지만, NestJS 진영에서 RxJS는 기본 도구다. 처음에는 살짝 어색해도 익숙해지면 응답 변환·캐싱·재시도 같은 패턴이 깔끔하게 정리된다.

여기서 짚어 둘 것 하나. Spring의 `@Transactional`처럼 서비스 메서드에 한 줄 박으면 자동으로 트랜잭션이 도는 그림은, NestJS에서 따라 하지 않는 편이 낫다. 흉내 내려고 인터셉터로 트랜잭션을 관리하다 보면, 컨트롤러 진입 시점에 트랜잭션을 시작하고 컨트롤러 진출 시점에 커밋하는 식의 어색한 디자인으로 흐른다. NestJS의 자연스러움은 **트랜잭션을 서비스 안에서 명시적으로 관리하는 것**이다. `prisma.$transaction(async (tx) => { ... })` 같은 호출로 묶고, 트랜잭션 경계를 코드로 보이게 둔다. 5장에서 이 사고를 본격적으로 마주한다.

## forwardRef와 순환 의존 — 등장 자체가 신호다

명시적 모듈 그래프의 정직한 부작용이 한 가지 있다. **순환 의존이 코드 위에 그대로 드러난다는 것.** A 모듈이 B 모듈을 `imports`하고, B 모듈이 A 모듈을 `imports`하면, NestJS는 부팅 시점에 그 사실을 알려 주고 `forwardRef`를 쓰라고 지시한다.

```typescript
// users.module.ts — 순환 의존을 표면으로 끌어올린다
import { Module, forwardRef } from '@nestjs/common';
import { OrdersModule } from '../orders/orders.module';

@Module({
  imports: [forwardRef(() => OrdersModule)],
  providers: [UserService],
  exports: [UserService],
})
export class UsersModule {}

// orders.module.ts
@Module({
  imports: [forwardRef(() => UsersModule)],
  providers: [OrderService],
  exports: [OrderService],
})
export class OrdersModule {}
```

`forwardRef`는 "이 모듈은 지금 정의 중이지만, 부팅 시점에는 결국 해결될 것"이라는 약속을 NestJS의 DI 컨테이너에 보내는 신호다. 이 한 줄 없이 두 모듈이 서로를 직접 `imports`하면, 둘 다 정의되기 전에 다른 쪽을 참조하니 컨테이너가 부팅을 못 한다.

이 도구를 처음 만난 Spring 출신은 살짝 의아해질 수 있다. Spring에서도 순환 의존은 일어나지만, 컴포넌트 스캔의 자동성에 묻혀 잘 안 보였다. `BeanCurrentlyInCreationException`이 새벽 두 시에 운영을 덮치고 나서야 "아 그동안 순환 의존이 있었구나"를 깨닫는 식이었다. NestJS의 명시성은 이걸 코드 위에 미리 끌어올린다. 보일러플레이트가 약간 더 늘어나는 대신, 함정이 새벽이 아니라 낮에 발견된다.

여기서 짚어 둘 더 중요한 사실이 있다. **`forwardRef`가 등장하는 자리는 거의 예외 없이 설계 점검 신호다.** A가 B를 부르고 B가 A를 부른다는 건, 두 모듈이 한 번 더 분해돼야 한다는 뜻이다. 보통은 이렇다 — A와 B가 공통으로 쓰는 도메인 개념을 C 모듈로 빼낸다. A → C ← B의 모양으로 정리된다. 순환은 사라지고, 두 모듈은 서로를 직접 모르는 채로 도메인을 공유한다. 또는 도메인 이벤트를 던지는 식으로 결합을 비동기화한다 — A가 B를 직접 부르지 않고 이벤트를 발행하면, B는 그 이벤트를 받아 자기 일을 한다. `EventEmitter`나 `@nestjs/event-emitter`가 이 자리를 받쳐 준다.

이건 사실 Spring에서도 같은 신호다. `@Lazy`나 setter 주입으로 순환을 우회하는 패턴이 나오면, 우리는 거의 자동으로 "도메인 분해가 늦었구나"를 떠올렸다. 신호의 모양은 다르지만 신호의 의미는 같다 — **순환 의존은 도구로 우회하기보다, 모델로 풀어 가는 편이 낫다.** NestJS의 `forwardRef`도 같은 자리를 차지하는 도구다. 우회가 가능하지만, 자주 등장하면 모델을 다시 들여다보는 게 자연스럽다.

## "DI인가, 그냥 hardwiring인가" — 정직하게 마주하기

NestJS의 DI 모델을 두고 Hacker News에 흥미로운 비판이 한 번 올라온 적이 있다. 누군가가 이렇게 적었다. "Nest의 모듈은 dependency를 선언하는 게 아니라 hardwiring하는 형태라 진짜 DI가 아니다." Spring 출신에게 이 비판은 자연스럽게 와 닿는다. Spring의 `@Bean`이나 `@Component`는 정말로 빈 정의의 선언이다. 클래스패스에 자동으로 등록되고, 같은 인터페이스를 구현하는 여러 빈이 있을 때 `@Qualifier`나 `@Primary`로 결정한다. 빈의 발견과 결정이 컨테이너의 책임이다.

NestJS는 다르다. `@Module`의 `providers` 배열에 직접 클래스를 적어 넣는다. 이게 정말 "선언"인가, 아니면 "직접 와이어링"인가? `providers: [UserService, UserRepository]`라는 배열은 Spring의 `@Bean` 정의보다 자바 컨피그(`@Configuration` 클래스 안의 `@Bean` 메서드)에 더 가깝다. 그리고 자바 컨피그도 여전히 DI라고 부른다. 그러니 "진짜 DI가 아니다"라는 표현은 약간 과하다. 다만 비판의 핵심은 정직하게 받아들일 만하다.

Spring의 `@Component`는 클래스 자체에 "나는 컨테이너 관리 빈입니다"라는 선언을 박는다. 어디서 쓰일지를 그 클래스가 알 필요는 없다. 컨테이너가 발견하고 등록한다. NestJS의 `@Injectable`은 그것만으로는 부족하다. 어느 모듈의 `providers`에 등록될지를 누군가가 적어야 한다. 그 누군가는 보통 모듈 정의 파일이고, 그래서 모듈 정의 파일은 의존성 그래프의 명시적 지도가 된다. **자동 발견이 아니라 명시적 등록.** 이 차이가 비판의 본질이다.

이 차이를 어떻게 받아들일 것인가. 두 가지 시각이 다 가능하다.

첫 번째 시각은 비판자의 시각이다 — "DI의 본질은 의존성 결정을 컨테이너에 위임하는 것인데, NestJS의 모듈은 결국 사용자가 직접 결정한다. 그 정도라면 단순한 팩토리 패턴과 차이가 작다." 이 시각은 자바 진영의 DI 전통에서 보면 일리가 있다. Spring은 자동 스캔과 자동 와이어링으로 사용자가 의존성 결정을 거의 신경 쓰지 않게 만들었다. NestJS는 그 한 발을 사용자에게 다시 돌려 줬다.

두 번째 시각은 옹호자의 시각이다 — "DI의 본질은 의존성을 직접 `new`하지 않고 외부에서 받는 것이다. NestJS의 컨트롤러와 서비스는 자기 의존성을 직접 만들지 않고 생성자 주입으로 받는다. 이건 DI다. 모듈이 명시적이라는 건 다른 차원의 문제다." 이 시각도 일리가 있다. 그리고 명시성이 가져다주는 보상 — 그래프 가시성, 의도하지 않은 빈의 차단, 순환 의존의 표면화 — 은 가볍지 않다.

이 책은 어느 쪽으로도 단정하지 않는다. 다만 한 가지는 정직하게 인정한다 — **NestJS의 DI는 Spring의 자동 와이어링만큼 자동이지는 않다.** 사용자가 모듈 정의 파일에 더 적어야 하고, 의존성 그래프를 머리로 들고 있어야 한다. 작은 모듈에서는 이 부담이 거의 없지만, 큰 모듈 그래프에서는 정직하게 무게가 있다. 그 무게를 받아들이는 대신, 그래프가 코드에 박혀 있다는 안전감을 받는다. 둘은 다른 트레이드오프이고, 어느 쪽이 절대적으로 옳다고 말하기 어렵다.

자바 컨피그(`@Configuration` 클래스에서 `@Bean` 메서드로 빈을 직접 정의하는 방식)를 썼던 사람이라면, NestJS의 모듈이 거의 같은 자리에 있다는 인상을 받을 수 있다. 그 사람에게는 NestJS의 모델이 어색하지 않다. 컴포넌트 스캔만 써 온 사람에게는 첫 학습 비용이 약간 있다. 어느 쪽이든 한 번 정리하면 다음부터는 의식하지 않게 된다.

## 호불호의 양면 — 어느 쪽도 외면하지 말자

NestJS를 둘러싼 평가는 갈린다. 정직하게 양쪽을 보자.

옹호 쪽 회고부터. Spring/Kotlin으로 20년을 굴려 온 어느 시니어는 NestJS로 옮긴 뒤 이렇게 적었다. "Express만 쓰면 Spring DI가 그립지만 NestJS는 익숙한 모양을 그대로 준다. 같은 모듈/컨트롤러/서비스 구조, 같은 데코레이터 기반 라우팅, 같은 인터셉터·가드·파이프. 일주일이면 적응됐다. 다만 Spring/Kotlin의 견고함을 그리워하는 순간이 분명히 있다. 트랜잭션 처리, ORM의 마법, 시큐리티 표준화 — 이런 자리에서는 NestJS가 한 발 가벼운 만큼 한 손이 더 가게 된다." 양면을 다 인정하는 회고다. 익숙함의 보상과 깊이의 부재를 같이 받아들이는 자세다.

인프랩의 회고도 비슷한 결이다. 처음에 JS + Express + 함수형 라이브러리(FxJS, FxSQL) 조합으로 빠르게 키워 온 백엔드 8명 팀이, 연 50~300% 성장하는 플랫폼을 책임지는 단계에서 한계를 느꼈다. 신규 입사자의 학습 곡선, IDE 자동완성·리팩터링 부족, 타입 안정성 부재, 함수형 JS 인력 풀의 좁음, 서드파티 호환성 문제, 커뮤니티 자료의 부족. 여섯 가지 페인 포인트를 정리한 뒤 신규 스택을 짰다 — NestJS Monorepo + TypeORM/MikroORM + Jest/SuperTest + 도메인 주도 설계. **"처음엔 익숙한 방식으로 빠르게, 규모가 커지면 구조에 투자한다."** 이 한 문장이 그 회고의 정수다. NestJS의 보일러플레이트는 작은 팀에는 부담이지만, 큰 팀에는 일관성을 강제하는 도구가 된다.

반대 쪽 회고도 외면하지 말자. Hacker News의 한 댓글은 이렇게 적는다. "Express나 Fastify로 충분한 작은 서비스에 NestJS는 과한 보일러플레이트다. 모듈 파일, 컨트롤러 파일, 서비스 파일, 그 사이의 imports/providers/exports — 단순한 CRUD API 한 개 뽑는 데 파일이 너무 많다. 같은 일을 Express로는 30줄로 끝낸다." 이 비판도 일리가 있다. 마이크로서비스 3~5개 이하의 작은 시스템에서는, NestJS의 구조가 자기 일감보다 더 무겁게 느껴질 수 있다. 모듈 그래프가 한 모듈 안에 다 들어가는 작은 서비스에 모듈 시스템 자체가 과한 도구가 된다.

여기에 또 한 가지 시각이 있다. RxJS 의존이다. NestJS의 인터셉터는 Observable을 반환하고, 비동기 합성을 RxJS 연산자로 푼다. Promise/async-await에 익숙한 사람에게는 한 단계 학습이 더 들어간다. WebFlux를 잘 안 쓰던 Spring 팀이라면, 이 자리에서 약간 어색함을 느낀다. NestJS는 인터셉터 안에서 Promise를 반환할 수도 있게 만들었지만, 깊은 패턴은 여전히 RxJS 위에 서 있다.

정리하면 이렇다. **NestJS는 만능 도구가 아니다.** 작은 서비스에는 과한 도구이고, 큰 시스템에는 깔끔한 도구다. 함수형 코드 위주의 팀에는 어색한 도구이고, OOP·DI에 익숙한 팀에는 익숙한 도구다. Spring의 깊은 생태계가 필요한 자리에는 부족한 도구이고, 가벼운 컨테이너 풋프린트가 필요한 자리에는 자연스러운 도구다. 어느 쪽도 절대적이지 않다. 우리가 풀고 있는 문제와 팀의 모양에 비춰 결정하는 일이다.

## 직방 — Spring 개발자 1인칭 적응기

한국 사례 한 가지를 1인칭 시점으로 들여다보자. 직방의 한 엔지니어가 적은 적응기는 Spring 출신의 NestJS 적응 과정을 정직하게 기록한다. 처음에 그가 NestJS를 받아 들었을 때 떠올린 것은 두 가지였다. "이 코드는 어디서 본 그림이다"와 "그런데 어디가 다르지?"

매핑은 일주일 안에 끝났다. 그가 정리한 1:1 표는 이렇다.

- `@Controller` ↔ `@Controller`
- `@Bean` ↔ `@Injectable`
- IoC Container ↔ NestJS Module
- `@Interceptor`(Spring HandlerInterceptor) ↔ NestInterceptor
- Exception Handler ↔ Exception Filter
- Argument Resolver / Validator ↔ Pipe
- Spring Security ↔ Guard

"구조가 매우 유사해 적응이 빨랐다"가 그의 결론이었다. TypeScript 코드 작성 속도가 Java보다 빠르다는 인상까지 받았다고 한다. 어노테이션과 데코레이터의 모양이 같고, 생성자 주입 방식이 같고, 라우트 정의 방식이 같으니, 손이 자연스럽게 움직였다.

다만 한 자리에서 정직한 차이가 있었다. **Spring의 컴포넌트 스캔 기반 자동 등록 vs NestJS의 모듈 명시적 선언.** 그가 적은 표현 그대로다 — "명시성은 높지만 보일러플레이트는 더 많다." 새 서비스를 만들 때마다 모듈 파일에 등록해야 하는 보일러플레이트가, 처음에는 살짝 번거로웠다. 시간이 지나면서 그 번거로움이 안전감으로 바뀌었다고 그는 적는다 — 의존성 그래프가 코드에 박혀 있다는 사실이, 큰 코드 베이스에서 의외로 든든했다는 것.

이 회고의 한 줄이 책 전체의 메시지와 만난다. **도구의 모양은 거의 같다. 다만 한두 자리의 사고 회로를 새로 정리해야 한다.** 직방의 사례는 그 새로 정리해야 할 자리가 무엇인지를 한국어로 명료하게 보여 준다. 모듈 명시성, 데코레이터의 메타데이터 모델, 트랜잭션의 자리(여기는 직방 회고의 표면에는 안 나오지만 5장에서 마주할 자리), RxJS의 등장 — 이 네 자리만 정리되면 NestJS는 Spring 출신의 두 번째 손에 가까운 도구가 된다.

## 어느 쪽을 고를까 — 산문으로 풀기

자, 그렇다면 NestJS와 다른 Node 프레임워크(Express, Fastify) 사이에서 어떻게 결정해야 할까. 산문으로 풀어 보자.

팀 규모가 5명 이하이고, 마이크로서비스가 3개 이하이고, 도메인이 단순하다면 — Fastify가 더 가볍다. NestJS의 모듈 그래프, 데코레이터 메타데이터, 인터셉터 시스템 같은 도구들이 자기 일감보다 무겁게 느껴지는 자리다. Fastify의 스키마 기반 검증과 직렬화는 OpenAPI/JSON Schema에 자연스럽게 녹아들고, 헬로월드 벤치 기준이긴 하지만 Express보다 두 배 빠르다. NestJS는 사실 Fastify를 어댑터로 끼워 쓸 수도 있어, 두 도구는 완전히 별개도 아니다. 그래도 깔끔한 자리는 분명히 다르다 — 작고 가벼운 서비스에는 Fastify, 일관성과 구조가 필요한 큰 서비스에는 NestJS.

팀이 그 위로 올라가기 시작하면 — 8명 이상, 마이크로서비스 5개 이상, 도메인이 깊고 신규 입사자가 자주 들어오는 자리 — NestJS의 모듈 그래프가 짐을 덜어 준다. 새 엔지니어가 코드 베이스를 처음 열 때, `@Module` 한 줄에서 의존성 그래프를 읽을 수 있다는 사실은 큰 안전감이다. PayPal이 Express의 비강제성 위에 Kraken.js라는 컨벤션 강제 도구를 따로 만들었던 그 자리에, NestJS는 처음부터 강제력을 가진 도구로 들어선다. 인프랩이 Express + 함수형 → NestJS Monorepo로 옮긴 그 결정도 같은 그림이다. **익숙한 방식으로 빠르게 시작하고, 규모가 커지면 구조에 투자한다.**

Spring 진영에서 옮겨오는 경우라면, 첫 NestJS 프로젝트는 익숙함이 무기가 된다. 모듈·컨트롤러·서비스·DI·데코레이터의 자리가 그대로 있고, 인터셉터·가드·파이프의 매핑도 1:1이다. 직방의 회고가 보여 준 일주일의 적응 곡선이 우리에게도 적용된다. 다만 한 가지를 잊지 말자 — **NestJS는 Spring을 그대로 옮긴 도구가 아니다.** 모듈 명시성, 트랜잭션 모델, RxJS, 데코레이터의 위태로운 토대 같은 자리에서 사고 회로를 한 번씩 새로 짜야 한다. 익숙함을 무기로 시작하되, 그 익숙함에 속아 차이를 외면하지는 말자.

마지막으로 짚어 둘 자리가 하나 있다. **NestJS와 Express는 서로 배제되지 않는다.** NestJS는 내부적으로 Express(또는 Fastify)를 HTTP 서버로 쓴다. NestJS 안에서도 직접 Express 미들웨어를 등록할 수 있고, 라우트 단위로 Express 핸들러를 끼울 수도 있다. 두 도구는 같은 자리를 두고 다투기보다, 한 시스템 안에서 공존할 수 있다. 큰 NestJS 모놀리스 안에 가벼운 Express 미들웨어가 끼어 있는 그림은 흔하다. 도구의 선택을 양자택일로 생각하지 않는 편이 자연스럽다.

비교 정리표는 이 절 끝에 붙여 두자.

| 항목 | Express | Fastify | NestJS |
|---|---|---|---|
| 강제성 | 거의 없음 | 약함 | 강함 |
| 학습 곡선 | 가장 낮음 | 낮음 | 중간 |
| 보일러플레이트 | 적음 | 적음 | 중간~많음 |
| 검증·직렬화 | 미들웨어로 직접 | 스키마 빌트인 | `class-validator` + Pipe |
| DI | 없음 | 없음 | 빌트인 |
| 모듈 시스템 | 없음 | 없음 | `@Module` |
| 권장 자리 | 작은 서비스, MVP | 작은 서비스, p99 민감 | 큰 시스템, 일관성 강제 |
| Spring 출신 익숙도 | 낮음 | 낮음 | 높음 |

표는 표일 뿐이다. 실제 결정은 산문 위의 팀 모양에 비춰 내린다.

## NestJS 테스트 — Spring @SpringBootTest의 자리

이제 마지막 절이다. Spring 출신이 NestJS로 옮길 때 가장 정직하게 보상을 받는 자리가 바로 **테스트**다. Spring에서 우리가 잘 다듬어 온 도구들 — `@SpringBootTest`, `@MockBean`, `MockMvc`, `@DataJpaTest`, `@Transactional` 테스트 — 의 거의 모든 자리를 NestJS가 익숙한 모양으로 가져온다. 이름이 살짝 바뀌고, 도구가 살짝 다르고, 트랜잭션 처리가 약간 다를 뿐이다. 사고 회로는 거의 그대로다.

핵심 도구는 `@nestjs/testing` 패키지의 `Test.createTestingModule()`이다. Spring의 `@SpringBootTest`가 ApplicationContext를 떠올려 부팅하는 그 자리에 있다. 모듈 정의를 받아 테스트 전용 컨테이너를 만들고, 일부 프로바이더를 mock으로 갈아끼울 수 있게 해 준다. `@MockBean`이 Spring 빈을 mock으로 교체하던 그 자리를, NestJS에서는 `.overrideProvider(...).useValue(...)` 또는 `.useClass(...)`로 같은 일을 한다.

```typescript
// users.service.spec.ts — 단위 테스트, 의존성을 mock
import { Test } from '@nestjs/testing';
import { UserService } from './users.service';
import { UserRepository } from './user.repository';
import { EmailService } from '../email/email.service';

describe('UserService', () => {
  let service: UserService;
  let repository: jest.Mocked<UserRepository>;
  let emailService: jest.Mocked<EmailService>;

  beforeEach(async () => {
    const moduleRef = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: UserRepository,
          useValue: { save: jest.fn() },
        },
        {
          provide: EmailService,
          useValue: { sendWelcome: jest.fn() },
        },
      ],
    }).compile();

    service = moduleRef.get(UserService);
    repository = moduleRef.get(UserRepository);
    emailService = moduleRef.get(EmailService);
  });

  it('새 사용자를 저장하고 환영 이메일을 보낸다', async () => {
    repository.save.mockResolvedValue({ id: 1, email: 'a@b.c', name: 'A' });

    const user = await service.register('a@b.c', 'A');

    expect(repository.save).toHaveBeenCalledWith({ email: 'a@b.c', name: 'A' });
    expect(emailService.sendWelcome).toHaveBeenCalledWith(user);
    expect(user.id).toBe(1);
  });
});
```

이 코드를 처음 보는 Spring 출신은 거의 자동으로 `@MockBean`과 매핑한다. `useValue: { save: jest.fn() }`이 Spring의 `@MockBean private UserRepository repository;`와 같은 자리에 있다. 차이는 두 가지다. 첫째, **mock 라이브러리가 Mockito가 아니라 Jest의 내장 mock**이다. `jest.fn()`은 단순한 Mockito stub과 비슷하지만, `mockResolvedValue`, `mockRejectedValue` 같은 비동기 헬퍼가 자연스럽게 들어 있다. async/await 코드를 테스트할 때 손에 잘 맞는다. 둘째, **타입 시스템이 mock과 정직하게 만난다.** `jest.Mocked<UserRepository>`라는 타입을 쓰면, mock 객체가 원본 인터페이스를 그대로 구현한 형태가 된다. 메서드 이름을 잘못 적으면 컴파일러가 잡아 준다. Mockito도 강한 도구지만, 타입 시스템과의 만남에서는 Jest mock이 살짝 더 매끄럽다.

여기까지가 단위 테스트다. 다음은 통합 테스트다. Spring의 `MockMvc`가 컨트롤러 + 인터셉터 + 필터를 함께 묶어 HTTP 요청을 시뮬레이션하는 그 자리에, NestJS는 **Supertest**를 쓴다. Supertest는 Express와 함께 자라 온 라이브러리로, 실제 HTTP 서버를 띄우거나 메모리에서 직접 핸들러를 호출하는 두 가지 모드를 지원한다.

```typescript
// users.e2e-spec.ts — 통합 테스트, Supertest로 HTTP 검증
import { Test } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../src/app.module';
import { PrismaService } from '../src/prisma.service';

describe('Users (e2e)', () => {
  let app: INestApplication;
  let prisma: PrismaService;

  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleRef.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
    await app.init();
    prisma = app.get(PrismaService);
  });

  afterAll(async () => {
    await app.close();
  });

  describe('POST /users/register', () => {
    it('유효한 입력은 201과 사용자 객체를 반환한다', async () => {
      const res = await request(app.getHttpServer())
        .post('/users/register')
        .set('Authorization', 'Bearer ' + validTestToken())
        .send({ email: 'a@b.c', name: 'Alice' })
        .expect(201);

      expect(res.body).toMatchObject({ email: 'a@b.c', name: 'Alice' });
      expect(res.body.id).toBeGreaterThan(0);
    });

    it('잘못된 이메일은 400을 반환한다', () =>
      request(app.getHttpServer())
        .post('/users/register')
        .set('Authorization', 'Bearer ' + validTestToken())
        .send({ email: 'not-an-email', name: 'Alice' })
        .expect(400));

    it('인증 헤더가 없으면 401을 반환한다', () =>
      request(app.getHttpServer())
        .post('/users/register')
        .send({ email: 'a@b.c', name: 'Alice' })
        .expect(401));
  });
});
```

이 테스트는 Spring의 `MockMvc`로 짜는 컨트롤러 통합 테스트와 거의 같은 그림이다. `request(app.getHttpServer()).post(...)`가 `mockMvc.perform(post(...))`의 자리에 있고, `.expect(201)`이 `.andExpect(status().isCreated())`의 자리에 있다. 검증 파이프, 가드, 인터셉터까지 한 번에 통과하는 통합 테스트이고, 데이터베이스(여기서는 Prisma)에도 실제로 INSERT가 일어난다.

여기서 자연스럽게 따라오는 질문이 있다. **테스트 격리는 어떻게 보장하지?** Spring 진영에서는 `@Transactional`이 테스트 메서드를 감싸 자동으로 롤백해 주는 그림이 익숙하다. 한 테스트가 INSERT한 데이터가 다음 테스트로 새지 않는다. 새벽에 운영을 망가뜨리지 않는 안전감의 한 자락이 거기서 나온다. NestJS에는 그런 자동 마법이 없다. 트랜잭션은 ORM 단위로 명시적으로 관리되고, 테스트도 같은 모델을 따른다. **테스트마다 트랜잭션을 열고, 마지막에 강제로 롤백하는 패턴**이 자연스러운 자리에 있다.

```typescript
// 트랜잭셔널 롤백 패턴 — Prisma $transaction 안에서 테스트하고 throw로 롤백
import { Test } from '@nestjs/testing';
import { PrismaService } from '../src/prisma.service';
import { UserService } from '../src/users/users.service';

describe('UserService (트랜잭셔널 롤백)', () => {
  let prisma: PrismaService;
  let service: UserService;

  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [/* AppModule */],
    }).compile();
    prisma = moduleRef.get(PrismaService);
    service = moduleRef.get(UserService);
  });

  it('register는 user를 저장한다 (테스트 후 롤백)', async () => {
    class Rollback extends Error {}

    await expect(
      prisma.$transaction(async (tx) => {
        const txService = service.withTransaction(tx);
        const user = await txService.register('a@b.c', 'Alice');

        const found = await tx.user.findUnique({ where: { id: user.id } });
        expect(found?.email).toBe('a@b.c');

        throw new Rollback();  // 롤백 강제
      }),
    ).rejects.toBeInstanceOf(Rollback);

    // 트랜잭션 밖에서는 데이터가 없어야 한다
    const after = await prisma.user.findFirst({ where: { email: 'a@b.c' } });
    expect(after).toBeNull();
  });
});
```

`prisma.$transaction(async (tx) => { ... })` 콜백 안에서 모든 작업을 `tx` 객체로 한다. 콜백 안에서 throw하면 트랜잭션이 롤백되고, 데이터가 사라진다. `Rollback`이라는 별도 에러 타입을 만들어 의도적으로 throw하면, 테스트 마지막에 데이터가 깨끗하게 정리된다. Spring의 `@Transactional` + `@Rollback(true)`이 자동으로 해 주던 일을, NestJS에서는 명시적인 코드로 구현한다.

이 패턴이 처음에는 살짝 번거로워 보인다. Spring의 마법이 그립다는 감각이 정직하게 나타나는 자리다. 그러나 한 번 손에 익으면 정직한 보상이 돌아온다 — **트랜잭션 경계가 코드에 보인다.** 어느 자리에서 트랜잭션이 시작하고 어디서 롤백되는지가 명시적이다. Spring의 `@Transactional`이 가끔 일으키는 미스테리(가령 `private` 메서드에서 자기 호출 시 트랜잭션이 안 도는 그 함정)가 NestJS에서는 일어나지 않는다. 테스트에 명시성을 들이는 대신 마법의 함정을 빼는 트레이드오프다.

테스트 도구 한 가지를 더 짚자. **Jest와 Vitest의 차이.** Jest는 NestJS의 디폴트 테스트 러너로, Facebook이 만들어 React 진영에서 자라 온 도구다. 안정적이고, mock·spy·snapshot 같은 도구가 한 패키지에 묶여 있고, NestJS CLI가 `jest.config.json`을 자동으로 만들어 준다. Vitest는 Vite 생태계에서 자라 온 신생 러너로, ESM 친화적이고, Vite의 transform 파이프라인을 그대로 쓰므로 빠른 시작 시간이 강점이다. NestJS도 Vitest를 받아들여 가는 추세이지만, 2026년 시점에 디폴트는 여전히 Jest다. 새 프로젝트에서 NestJS CLI를 그대로 쓰면 Jest가 자동으로 들어온다. 굳이 갈아탈 이유가 없다면 Jest를 그대로 쓰는 편이 자연스럽다. Vitest는 ESM 마이그레이션이 절실한 자리, 또는 Vite를 이미 쓰고 있는 모노레포에서 한 도구로 통일하고 싶을 때 들이는 카드다.

마지막으로 운영 차원의 직관 한 가지. **테스트 컨테이너(Testcontainers)** 같은 도구는 Java 진영의 표준이지만, Node 진영에서도 `testcontainers` npm 패키지로 같은 패턴이 가능하다. 테스트 시작 시 PostgreSQL이나 Redis 컨테이너를 자동으로 띄우고, 테스트가 끝나면 정리한다. CI에서 H2 같은 인메모리 DB를 쓰지 않고 실제 DB에 가까운 환경을 쓰고 싶을 때 자연스러운 도구다. Spring 출신이라면 거의 그대로 옮겨와도 손에 잘 맞는다.

테스트 절을 닫으며 한 가지 짚어 두자. **NestJS의 테스트는 Spring 테스트보다 가볍다.** `@SpringBootTest`가 ApplicationContext를 통째로 부팅하는 데 몇 초가 걸리는 자리에서, `Test.createTestingModule`은 보통 백 밀리초 단위에서 끝난다. JVM 부팅 비용이 빠지고, 테스트 모듈을 작게 잘라 쓰는 게 NestJS의 자연스러움이다. 큰 통합 테스트도 NestJS 쪽이 유의미하게 빠르다. CI에서 테스트 묶음을 통째로 도는 데 걸리는 시간이, Spring 시절 대비 몇 배 줄어드는 경험을 NestJS 첫 프로젝트에서 정직하게 만난다. 이 가벼움은 단순한 운영 비용 절감이 아니라, 테스트를 자주 돌리는 문화로도 이어진다. 가벼운 테스트는 자주 돌리고, 자주 돌리는 테스트는 일찍 깨진다. Java 시절의 두꺼운 테스트 인프라가 가져다준 신뢰감과는 또 다른 안전감이다.

8장에서 우리가 다시 만나는 마이그레이션 사례 — PayPal이 Java JUnit 자산을 어떻게 처리했는가, 인프랩이 NestJS Monorepo로 옮기면서 Jest/SuperTest 기반 테스트 자산을 어떻게 짰는가, 줌인터넷이 모바일 줌을 옮기면서 SSR 테스트 커버리지를 어떻게 유지했는가 — 의 한 단락은 모두 이 절의 도구들을 다시 부른다. 4장에서 우리가 손에 익힌 `Test.createTestingModule`, Supertest, 트랜잭셔널 롤백, Jest mock의 모양이 그 회고들의 토대다. **테스트 도구는 이름만 바뀌었을 뿐, 우리가 풀고 있는 테스트 문제는 같다.** Spring 출신의 테스트 직관 — 단위·통합·E2E의 세 층, mock vs 진짜 의존성의 트레이드오프, 트랜잭션 격리 — 이 거의 그대로 통한다. 4장의 마지막 절이 책에서 보상이 가장 큰 자리가 되는 이유다.

## 마무리 — 닮음과 갈라짐, 그리고 다음 장

이 장은 두 프레임워크의 정면 비교였다. 닮음이 7할이고, 갈라짐이 3할이다. 닮음 쪽을 정리하면 — 모듈·컨트롤러·서비스의 레이어 구조, 데코레이터(어노테이션) 기반 라우팅, 생성자 주입 DI, 인터셉터·가드·파이프의 횡단 관심사 처리, 그리고 테스트 인프라의 거의 모든 자리. Spring으로 다져 온 손이 NestJS의 첫 코드 베이스에 들어와 일주일 안에 적응하는 이유가 여기에 있다.

갈라짐 쪽을 정리하면 — 모듈 그래프의 명시성(클래스패스 컴포넌트 스캔이 없다), 데코레이터의 메타데이터 모델(`reflect-metadata`라는 위태로운 토대), 생태계의 두께(트랜잭션·시큐리티·배치는 직접 짜는 일이 늘어난다), 트랜잭션의 자리(AOP 마법 대신 명시적 호출), RxJS 의존도(인터셉터의 깊은 패턴은 Observable 위에 있다). 이 다섯 자리가 Spring 출신이 NestJS에서 정직하게 새로 정리해야 할 사고 회로다. 그중에서도 트랜잭션과 ORM의 자리는 한 장의 무게가 더 필요하다. 5장이 그 자리를 받아 든다.

호불호의 양면도 외면하지 말자. 옹호 쪽 — 익숙한 모양, 일관성 강제, 가벼운 풋프린트, 빠른 콜드 스타트. 반대 쪽 — 작은 서비스에 과한 보일러플레이트, 일반화된 AOP 부재, 표준화된 시큐리티 스택의 얕음, RxJS의 학습 비용. 어느 쪽도 절대적이지 않다. 우리가 풀고 있는 문제와 팀의 모양에 비춰 결정하는 일이다.

도구의 결정 다음은, 데이터다. NestJS의 모듈·DI·인터셉터를 다 받아 들였다고 해도, 데이터베이스 위에서 코드를 짜기 시작하는 순간 다시 한 번 정직한 충격이 온다. **Hibernate의 마법이 사라진 자리.** lazy loading이 자동으로 안 되고, dirty checking이 없고, `@Transactional` AOP가 없는 그 자리에서 우리는 어떤 직관을 새로 짜야 할까. JPA로 자라 온 손이 Prisma를 처음 만났을 때 어떤 감각이 사라졌다고 느끼고, 그 사라짐을 어떻게 설계로 메우는지를 다음 장에서 정면으로 들여다보자.
