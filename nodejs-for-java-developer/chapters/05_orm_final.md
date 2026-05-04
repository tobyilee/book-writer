# 5장. ORM과 데이터베이스 — Hibernate의 마법이 사라진 자리

Spring 출신 개발자가 Node.js로 와서 가장 오래 그리워하는 게 무엇이냐고 물으면, 답은 거의 한 단어로 모인다. Hibernate. 정확히는 Hibernate가 우리 모르게 해주던 일들이다. `entityManager.find()`로 가져온 엔티티의 자식 컬렉션을 그냥 `for`로 돌면 알아서 SQL이 한 번 더 나가던 마법, 트랜잭션이 끝날 때 변경된 필드를 자동으로 추적해 `UPDATE`를 만들어 주던 dirty checking, `@Transactional` 한 줄이면 메서드 진입과 종료 시점에 트랜잭션이 시작되고 커밋되던 AOP의 손길.

처음 Prisma 코드를 들여다보면 이 손길이 모두 사라져 있다. `prisma.user.findUnique({ where: { id: 1 } })`로 사용자를 가져온 다음 `user.posts`를 출력하면 `undefined`가 찍힌다. 트랜잭션은 `prisma.$transaction([...])`이라는 명시적 호출로 묶어야 시작된다. 엔티티의 필드를 바꿔놓고 가만히 두면 아무 SQL도 나가지 않는다. 데이터 계층 전체가 한 단계 더 손으로 내려와 있다.

처음에는 허전하다. 그리고 조금 난감하다. "이걸 다 손으로 적어야 한다고?"라는 질문이 입에서 먼저 나온다. 그런데 그 허전함을 며칠 안고 가다 보면 다른 감각이 같이 따라온다. 이 코드가 어떤 SQL을 만드는지가 코드 표면에서 거의 그대로 보인다는 감각, 그리고 트랜잭션의 경계가 콜백의 괄호 안과 밖으로 정확히 갈린다는 감각. Hibernate는 마법으로 우리 손을 덜어주었지만, 그 마법은 동시에 SQL 한 줄을 두 단계 깊은 프록시 너머로 밀어 넣고 있었다.

이 장에서 우리가 같이 들여다볼 풍경은 그래서 두 겹이다. 한 겹은 "사라진 마법이 정확히 뭐였는지" 하나씩 짚어 보는 일이고, 다른 한 겹은 "그 사라짐을 우리가 어떤 설계로 메우는지" 따라가 보는 일이다. JPA 시절에 우리가 쓰던 직관 — 엔티티, 연관관계, lazy 로딩, 트랜잭션 — 이 Node 진영에서 어떤 모양으로 다시 등장하는지, 그리고 어떤 모양으로는 영영 등장하지 않는지를 같이 보자. 우리가 잃은 건 도구일 뿐이다. 우리가 풀던 문제는 그대로다.

## Prisma, Drizzle, TypeORM — 세 가지 길

Node.js 진영에서 ORM이라는 단어를 입에 담으면 거의 세 이름이 같이 따라 나온다. Prisma, Drizzle, TypeORM. 이 셋은 같은 자리에서 같은 일을 하지만, 자라난 배경이 다르고 사상이 다르다. JPA·Hibernate라는 한 줄로 정리되는 Java 진영과 다른 점이 바로 여기다.

가장 익숙한 모양부터 보자. TypeORM이다. 클래스 위에 `@Entity`를 얹고 필드 위에 `@Column`을 다는 모양이 거의 JPA 그대로다. Active Record 패턴(엔티티 자신이 `save()`를 가지는 형태)과 Data Mapper 패턴(별도의 리포지토리를 두는 형태) 둘 다 지원하고, 마이그레이션 CLI도 갖춰져 있다. Spring + Hibernate 출신이 Node로 와서 처음 손이 가는 도구가 거의 TypeORM이다. 그런데 신규 프로젝트에서 점점 비추천되는 흐름이 분명히 있다. 데코레이터 기반 타입 추론이 약해서 IDE 자동완성이 어긋나는 자리가 있고, 마이그레이션 신뢰성에 대한 후기가 좋지 않으며, 성능 이슈도 꾸준히 보고된다. 익숙함을 사는 대신 다른 비용을 치르는 구도다.

다음이 Prisma다. Prisma는 사상이 다르다. 스키마를 `.prisma`라는 별도 DSL 파일에 적고, `prisma generate` 명령이 그 파일을 읽어 타입스크립트 클라이언트를 코드 생성해 준다. 우리가 직접 작성하는 게 아니라 도구가 만들어준 클라이언트를 import해서 쓰는 구조다. 이게 무슨 차이를 만드느냐 하면, 타입 안전성이 추론이 아니라 생성에서 나온다는 차이를 만든다. `findMany({ select: { id: true, posts: { select: { title: true } } } })`라고 쓰면 결과 타입이 정확히 `{ id: number, posts: { title: string }[] }[]`로 좁혀진다. JPA 시절 DTO 클래스를 손으로 만들어가며 프로젝션을 적던 일이 한 줄의 객체 리터럴로 끝난다. 마이그레이션 도구도 강력하고, DX가 좋다는 후기는 거의 정설처럼 자리잡았다. 콜드 스타트가 무겁다는 단점이 오래 따라다녔지만, Prisma 7에서 쿼리 엔진을 Rust 바이너리에서 TypeScript로 옮기는 작업이 진행되며 이 부담은 빠르게 줄어드는 중이다.

마지막이 Drizzle이다. 이쪽은 결이 또 다르다. JOOQ나 Querydsl을 좋아했던 사람이라면 첫 줄을 보자마자 표정이 풀린다. 타입스크립트로 직접 스키마를 적고, 쿼리는 SQL에 거의 일대일로 대응되는 빌더로 적는다. `db.select().from(users).leftJoin(posts, eq(users.id, posts.userId)).where(eq(users.id, 1))` 같은 식이다. 결과 타입은 추론으로 정확히 떨어지고, 번들 크기가 7KB 수준이라 Edge·Lambda 환경에 가볍게 들어간다. ORM이라기보다 타입 안전한 SQL 빌더에 가깝고, 쓰는 사람의 감각도 그렇다. SQL 한 줄이 무엇이 될지 코드에서 그대로 읽힌다.

이 셋의 차이를 한 번에 보고 싶으면 다음 표가 도움이 될 것이다. 본문 흐름을 자르지 않으려고 절 끝에 둔다.

| 항목 | Prisma | Drizzle | TypeORM |
|---|---|---|---|
| 스키마 정의 | `.prisma` DSL → 코드 생성 | TypeScript 직접 | TypeScript 데코레이터 |
| 타입 안전 | 생성된 클라이언트 기반, 정확 | 추론 기반, 정확 | 데코레이터 기반, 약점 있음 |
| 마이그레이션 | `prisma migrate` (강력) | `drizzle-kit` (수동 검토 필요) | TypeORM CLI (신뢰성 후기 약함) |
| 번들 크기 | 무거움 (쿼리 엔진 바이너리) | ~7KB gzipped | 중간 |
| 콜드 스타트 | 무거움 (Prisma 7에서 개선 중) | 거의 영향 없음 — Edge·Lambda 강점 | 중간 |
| Hibernate 비교 | "Hibernate-like 마법은 적지만 타입 안전이 강함" | "JOOQ에 가까움" | "Hibernate에 가장 비슷한 모양" |

표를 한 줄로 옮기면 이렇다. **Hibernate가 그리우면 Prisma, JOOQ가 그리우면 Drizzle, 익숙한 데코레이터 모양을 사고 싶으면 TypeORM이지만 그 익숙함의 대가가 만만치 않다.** 이 책은 비교의 절반 이상을 Prisma에 할애한다. 가장 많이 쓰이고 있고, JPA 출신이 처음 부딪히는 충격이 가장 정직하게 드러나는 도구이기 때문이다. Drizzle은 "다른 길"의 대표 사례로, Mongoose와 ioredis는 관계형 DB 너머의 자리에서 한 번씩 등장한다.

## include와 select — lazy proxy 없이 관계를 다룬다는 것

JPA에서 가장 익숙한 코드 한 줄을 떠올려 보자.

```java
@Entity
public class User {
    @Id
    private Long id;

    @OneToMany(mappedBy = "author", fetch = FetchType.LAZY)
    private List<Post> posts;
    // ...
}

// 호출부
User user = userRepository.findById(1L).orElseThrow();
for (Post post : user.getPosts()) {  // 여기서 SQL 한 번 더
    System.out.println(post.getTitle());
}
```

`getPosts()`를 호출하는 그 순간, Hibernate는 프록시 안에 숨어 있던 SQL을 자동으로 던진다. 이게 lazy proxy의 마법이다. 우리는 자식 컬렉션이 비어 있는지 차 있는지 신경 쓰지 않고 그냥 객체 그래프를 따라 내려가면 됐다. 트랜잭션 안에서만 동작한다는 단서가 붙긴 했지만, 안에서는 거의 모든 게 알아서 굴러갔다.

Prisma에는 이 마법이 없다. 정확히 말하면, 같은 모양으로는 없다. 같은 코드를 Prisma로 옮기면 이렇다.

```ts
// 1번 시도 — JPA 출신이 가장 먼저 적는 코드
const user = await prisma.user.findUnique({ where: { id: 1 } });
console.log(user?.posts);  // undefined
```

찍어보면 `undefined`다. 에러가 나는 게 아니라, 그냥 그 자리에 아무것도 없다. 처음 보면 "타입스크립트 컴파일러가 막아줄 줄 알았는데?"라는 생각이 든다. 실제로 막아준다 — Prisma 클라이언트가 생성한 `User` 타입에는 `posts` 필드가 아예 없기 때문이다. 그러니 `user.posts`라고 적는 순간 IDE가 빨간 줄을 그어준다. 컴파일러가 못 막는 건 우리가 `(user as any).posts`라고 쓰거나 JSON.stringify로 펼쳐서 클라이언트에 던진 다음 클라이언트에서 `undefined`를 만나는 경로뿐이다.

원하는 코드는 이렇게 적어야 한다.

```ts
// 2번 시도 — 관계를 명시적으로 가져온다
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: { posts: true },
});

if (user) {
  for (const post of user.posts) {
    console.log(post.title);
  }
}
```

`include: { posts: true }`라고 적는 순간 Prisma 클라이언트의 반환 타입에 `posts: Post[]`가 추가된다. SQL은 한 번에 join으로 나가거나(혹은 두 번 나누어 나가거나 — Prisma의 전략에 따라) 관계가 채워진 객체가 돌아온다. 자식만 가져오고 싶으면 `select`를 쓴다.

```ts
const user = await prisma.user.findUnique({
  where: { id: 1 },
  select: {
    id: true,
    email: true,
    posts: {
      select: { id: true, title: true },
    },
  },
});
// user의 타입: { id: number, email: string, posts: { id: number, title: string }[] } | null
```

이 코드를 보면 JPA 시절의 한 가지 경험이 떠오른다. `@Query`에 JPQL을 적고 `new com.example.UserDto(u.id, u.email)` 같은 생성자 표현으로 프로젝션을 손으로 짜던 일. 매핑 DTO를 클래스로 따로 만들어 놓고, 필드가 늘 때마다 그 DTO도 같이 고치고, 컴파일러가 그 둘이 어긋나면 알려주길 빌던 일. Prisma의 `select`는 그 일을 단번에 끝낸다. 어떤 필드를 가져올지 적으면 결과 타입이 그 모양으로 좁혀진다. 이 한 가지만으로도 Prisma의 DX가 왜 호평받는지가 설명된다.

마법이 사라진 자리에 무엇이 들어왔는지 정리해 보자. **lazy proxy가 사라진 대신, 어떤 데이터를 가져올지가 코드 표면에 드러난다.** 이 차이는 양면이다. 한쪽 면은 코드가 길어진다는 사실이고, 다른 쪽 면은 코드를 읽는 사람이 SQL 윤곽을 짐작할 수 있다는 사실이다. JPA 시절 우리는 엔티티 한 마리를 가져왔는데 뒷단에서 SQL 다섯 줄이 나가는 광경을 자주 만났다. Prisma는 그 광경이 일어나려면 우리가 다섯 번을 적거나 한 번에 다섯을 묶어 적어야 한다.

## LazyInitializationException 대신 등장하는 것

Hibernate를 실무에서 쓰면 거의 통과 의례처럼 만나는 에러가 하나 있다.

```
org.hibernate.LazyInitializationException:
  could not initialize proxy - no Session
```

트랜잭션이 끝난 뒤에 `user.getPosts()`를 호출하면 터지는 그 에러다. 컨트롤러에서 서비스가 반환한 엔티티를 받아 뷰로 넘기는 순간, 또는 `@RestController`가 JSON 직렬화를 시도하는 순간 터진다. open-session-in-view 설정으로 임시 봉합한 적도 있고, 서비스 안에서 미리 컬렉션을 다 풀어놓고 반환한 적도 있다. 이 에러를 한 번이라도 운영에서 만났던 사람은 그 트라우마가 길게 간다.

Prisma로 넘어오면 이 에러는 영영 나오지 않는다. 트랜잭션이라는 개념 자체가 명시적 함수 호출 안에만 있고, 객체가 함수 바깥으로 나간 순간 그것은 그냥 plain JavaScript object다. 프록시가 아니다. 따라서 "세션이 닫혔는데 프록시를 건드려서 터지는" 일은 구조적으로 일어날 수 없다.

그런데 그 자리에 다른 질문이 들어온다.

```ts
// 컨트롤러
const user = await userService.findById(1);
return { posts: user.posts ?? [] };  // user.posts는 왜 undefined?
```

트랜잭션이 닫혀서 터지는 게 아니라, "왜 `user.posts`가 `undefined`냐"가 디버깅의 새 출발점이 된다. 답은 거의 항상 같다. 서비스 어디선가 `findUnique`를 부를 때 `include: { posts: true }`를 적지 않았기 때문이다. 그러니 컴파일러가 그 자리를 막는다 — 정확히 말하면, 막아주는 게 정상이다. `user.posts`라고 적는 순간 `Property 'posts' does not exist on type 'User'`라는 에러가 떠야 맞다. 안 뜨고 있다면 어디선가 `any`로 풀어놓았거나, 서비스 반환 타입을 직접 손으로 적어놓고 그 타입이 실제 쿼리와 어긋나 있다.

타입을 어떻게 적느냐가 이 새 질문의 답을 만든다. Prisma의 한 가지 좋은 점은 쿼리에서 결과 타입을 추출할 수 있다는 점이다.

```ts
import { Prisma } from '@prisma/client';

// 쿼리 모양을 따로 선언해두고
const userWithPosts = Prisma.validator<Prisma.UserDefaultArgs>()({
  include: { posts: true },
});

// 결과 타입을 그 모양에서 뽑아낸다
type UserWithPosts = Prisma.UserGetPayload<typeof userWithPosts>;

// 서비스
async function findById(id: number): Promise<UserWithPosts | null> {
  return prisma.user.findUnique({
    where: { id },
    ...userWithPosts,
  });
}
```

이렇게 두면 서비스의 반환 타입과 실제 쿼리 모양이 한 자리에 묶인다. 둘 중 하나만 바뀌어도 컴파일러가 알려준다. JPA 시절 DTO 클래스를 따로 두던 그 패턴이, 도구 안쪽으로 들어와서 한 번 더 풀려 나오는 모양이다. 처음 보면 장황해 보이지만, 운영 며칠 가면 이 명시성에 고마워하게 된다.

LazyInitializationException이 사라진 자리에 들어선 새 질문 — "왜 `undefined`냐" — 는 사실 같은 질문의 다른 모양이다. 둘 다 "관계를 어디서 가져오기로 했는가"를 묻고 있다. Hibernate는 그 질문을 트랜잭션 경계와 fetch 전략으로 답하라고 했고, Prisma는 함수 호출 시점의 `include`/`select`로 답하라고 한다. 답하는 위치가 한 단계 더 가까워졌을 뿐이다.

## Unit of Work는 어디로 갔나

Hibernate에서 가장 신비롭게 느껴지는 동작이 dirty checking이다.

```java
@Transactional
public void rename(Long id, String newName) {
    User user = userRepository.findById(id).orElseThrow();
    user.setName(newName);
    // 메서드 끝나면 알아서 UPDATE가 나간다
}
```

`save()`도 부르지 않았는데 SQL이 나간다. 이게 Hibernate의 1차 캐시가 하는 일이고, 더 넓게 보면 Unit of Work 패턴이 하는 일이다. 세션이 살아 있는 동안 영속 컨텍스트에 들어온 엔티티의 상태를 추적하고, 트랜잭션이 끝나는 시점에 변경된 필드만 모아 SQL을 생성한다. 변경 추적이 자동이고, 같은 ID로 두 번 조회하면 1차 캐시에서 같은 인스턴스가 돌아온다. JPA를 써본 사람은 이 동작에 길들어 있어서, 어떤 트랜잭션 안에서는 객체를 일급 시민처럼 다루고 SQL은 도구가 알아서 만든다는 감각이 몸에 박혀 있다.

Prisma에는 이 동작이 없다. Prisma 이슈 트래커에는 #4991이라는 오래된 항목이 하나 있다. "Unit of Work 지원을 추가해 달라"는 요청이고, 별이 꽤 붙은 채로 오래 떠 있다. Prisma 팀의 답은 일관된다. "명시적 메서드 호출이 곧 SQL이라는 게 우리 사상이다." `prisma.user.update({ where: { id }, data: { name } })`이라고 적은 순간 그 줄에서 SQL이 나가고, 그게 전부다. 객체를 조회해 와서 필드를 바꿔놓고 가만히 두면 데이터베이스에는 아무 일도 일어나지 않는다.

이게 좋은가 나쁜가는 입장이 갈린다. 한쪽에서는 "JPA의 dirty checking은 마법이 아니라 부채다"라고 본다. 변경이 자동으로 나가는 건 편하지만, 어느 시점에 어떤 SQL이 나갈지가 코드 흐름에서 보이지 않는다. flush 타이밍이 의도와 어긋나서 외부 시스템과의 동기화가 깨지는 경우, 영속 컨텍스트가 부풀어 메모리를 먹는 경우, 같은 트랜잭션 안에서 변경 순서를 잡기가 까다로운 경우 — 운영 가다 보면 이런 자리들이 누적된다. 다른 쪽에서는 "그래도 그 마법이 도메인 코드를 깨끗하게 해줬다"고 본다. 도메인 객체에 비즈니스 로직만 적고 영속화는 알아서 되니까, 도메인 모델과 영속화 모델을 나란히 짤 수 있었다.

Prisma의 사상은 전자에 가깝다. 모든 SQL은 메서드 호출에서 시작되고, 메서드 이름과 인자에 그 SQL의 모양이 거의 다 들어 있다. 코드를 위에서 아래로 읽기만 해도 어떤 쿼리들이 어떤 순서로 나가는지 짐작이 된다. JPA 출신이 처음 만나면 답답하다. 익숙한 손이 가는 자리에 손이 갈 곳이 없기 때문이다. 그런데 운영을 같이 가다 보면 이 답답함의 절반은 다른 감각으로 바뀐다. SQL이 안 보이는 것보다 보이는 게 차라리 낫다는 감각이다.

dirty checking이 그리우면 이렇게 메우는 편이 낫다. 도메인 서비스 안에서 "조회 → 변경 → 저장"의 사이클을 한 함수에 묶어 두는 패턴이다. JPA 시절에는 트랜잭션 경계 안에서만 끝나면 됐던 일이, Prisma에서는 명시적인 `update` 호출까지 한 함수에 모이도록 적는다.

```ts
async function renameUser(id: number, newName: string) {
  const user = await prisma.user.findUnique({ where: { id } });
  if (!user) throw new NotFoundError();
  // 비즈니스 검증
  if (newName.length < 2) throw new ValidationError();
  // 명시적 저장
  return prisma.user.update({
    where: { id },
    data: { name: newName },
  });
}
```

코드가 살짝 길어진다. 그러나 "이 함수가 어떤 SQL을 두 번 부르는지"가 표면에 그대로 있다. JPA 출신이 가장 자주 빠지는 함정 — 도메인 객체를 들고 다니다 어디선가 이상한 시점에 flush가 도는 — 가 구조적으로 사라진다.

## 트랜잭션 — `@Transactional`의 자리에 들어선 것

Spring 시절 트랜잭션 한 줄을 떠올려 보자.

```java
@Service
public class TransferService {
    @Transactional
    public void transfer(Long fromId, Long toId, BigDecimal amount) {
        Account from = accountRepository.findById(fromId).orElseThrow();
        Account to = accountRepository.findById(toId).orElseThrow();
        from.withdraw(amount);
        to.deposit(amount);
    }
}
```

`@Transactional` 한 줄이 메서드 진입 시점에 트랜잭션을 열고, 정상 종료에 커밋하며, 런타임 예외에 롤백한다. 자바 출신이 가장 사랑하는 어노테이션 중 하나다. 그런데 이 마법이 어떻게 동작하는지를 정확히 아는 사람은 의외로 적다. Spring AOP가 프록시 객체를 만들어 메서드를 가로채고, 그 프록시 안에서 트랜잭션 매니저가 트랜잭션을 시작하고 끝낸다. 우리가 직접 `getConnection()`이나 `setAutoCommit(false)`나 `commit()`을 부른 적은 한 번도 없다.

Prisma의 트랜잭션은 다르다. 두 가지 모양이 있고, 둘 다 호출이 명시적이다. 첫 번째는 배열 모양이다.

```ts
await prisma.$transaction([
  prisma.account.update({
    where: { id: fromId },
    data: { balance: { decrement: amount } },
  }),
  prisma.account.update({
    where: { id: toId },
    data: { balance: { increment: amount } },
  }),
]);
```

여러 쿼리를 배열로 묶어 던지면 Prisma가 하나의 트랜잭션 안에서 차례로 실행하고, 하나라도 실패하면 모두 롤백한다. 단순한 경우에 깔끔하다. 그러나 중간에 조건 분기가 있거나, 한 쿼리의 결과를 보고 다음 쿼리 모양을 정해야 한다면 이 모양은 부족하다. 그때 두 번째 모양이 나온다. 콜백 모양이다.

```ts
await prisma.$transaction(async (tx) => {
  const from = await tx.account.findUnique({ where: { id: fromId } });
  if (!from) throw new NotFoundError();
  if (from.balance.lt(amount)) throw new InsufficientFundsError();

  await tx.account.update({
    where: { id: fromId },
    data: { balance: { decrement: amount } },
  });
  await tx.account.update({
    where: { id: toId },
    data: { balance: { increment: amount } },
  });
});
```

콜백 안의 `tx`는 트랜잭션이 묶인 클라이언트다. 콜백이 정상 종료하면 커밋, 예외가 던져지면 롤백. 안에서 일반 `prisma`(`tx` 말고)를 호출하면 그 호출은 트랜잭션 바깥으로 새어 나간다 — 이게 처음 운영에서 만나는 함정 중 하나다. `@Transactional` AOP는 우리가 같은 메서드 안에서 호출한 모든 리포지토리 호출을 알아서 같은 트랜잭션에 묶어 줬지만, Prisma는 우리가 `tx`를 정확히 들고 다녀야 한다.

이게 바로 명시성의 비용이다. 그리고 명시성의 미덕이기도 하다. 어떤 쿼리가 트랜잭션 안에 있고 어떤 쿼리가 밖에 있는지가 코드의 변수 이름으로 드러난다. Spring 시절에 만났던 함정 — `@Transactional` 메서드 안에서 외부 메서드를 호출했는데 같은 클래스 메서드라 프록시를 거치지 않아 새 트랜잭션이 안 열리는 — 같은 일은 Prisma에서는 일어나지 않는다. 대신 우리가 `tx`를 깜빡 잊고 `prisma`로 적으면 그 호출이 자동 커밋으로 새어 나간다. 함정의 모양이 바뀌었을 뿐, 함정 자체는 여전히 있다.

분산 트랜잭션과 Saga는 또 다른 이야기다. 두 서비스가 자기 DB를 가지고 있고 그 사이를 트랜잭션으로 묶어야 한다면, JPA의 `@Transactional`도 답이 아니다. JTA가 있긴 했지만 운영에서 거의 쓰이지 않았고, MSA 시대 들어 보상 트랜잭션·이벤트 소싱·Saga 패턴이 자리를 차지했다. Node.js에서도 답은 같다. Prisma `$transaction`은 단일 DB 안에서만 동작한다. 두 서비스를 묶고 싶으면 Outbox 패턴 + Kafka, 또는 Saga orchestrator(Temporal·Conductor 같은) 같은 별도의 도구가 들어온다. 이 책의 8장에서 마이그레이션 전략을 다룰 때 이 자리가 다시 등장한다.

여기서 한 가지 권할 만한 패턴이 있다. NestJS를 쓰는 프로젝트라면 `tx`를 서비스 메서드의 첫 인자로 받는 컨벤션을 정해두는 편이 낫다.

```ts
@Injectable()
export class AccountService {
  constructor(private prisma: PrismaService) {}

  async withdraw(tx: Prisma.TransactionClient, accountId: number, amount: Decimal) {
    const account = await tx.account.findUnique({ where: { id: accountId } });
    if (!account) throw new NotFoundException();
    if (account.balance.lt(amount)) throw new BadRequestException('insufficient funds');
    await tx.account.update({
      where: { id: accountId },
      data: { balance: { decrement: amount } },
    });
  }

  async deposit(tx: Prisma.TransactionClient, accountId: number, amount: Decimal) {
    await tx.account.update({
      where: { id: accountId },
      data: { balance: { increment: amount } },
    });
  }
}

@Injectable()
export class TransferService {
  constructor(
    private prisma: PrismaService,
    private accounts: AccountService,
  ) {}

  async transfer(fromId: number, toId: number, amount: Decimal) {
    return this.prisma.$transaction(async (tx) => {
      await this.accounts.withdraw(tx, fromId, amount);
      await this.accounts.deposit(tx, toId, amount);
    });
  }
}
```

서비스 메서드가 트랜잭션 클라이언트를 받게 통일하면 "이 함수가 트랜잭션 안에서만 부를 수 있다"는 약속이 시그니처로 드러난다. Spring의 `@Transactional`이 어노테이션으로 표현하던 약속이, 인자 타입으로 옮겨 왔을 뿐이다. 우리가 잃은 건 어노테이션 한 줄의 우아함이고, 얻은 건 호출 그래프 위에 트랜잭션 경계가 그대로 보이는 가독성이다.

## N+1 — `@BatchSize`의 자리, DataLoader의 자리

ORM을 쓰는 한 N+1은 영원한 동반자다. JPA 시절 우리가 N+1을 만났을 때 손이 가던 도구는 두 갈래였다. 첫 번째는 JPQL의 `fetch join`이다. 컬렉션을 한 번에 같이 가져오라고 명시하는 방식.

```java
@Query("SELECT u FROM User u JOIN FETCH u.posts WHERE u.id IN :ids")
List<User> findAllWithPosts(@Param("ids") List<Long> ids);
```

두 번째는 `@BatchSize`다. lazy 컬렉션이 풀릴 때 N개 row마다 한 번씩 SQL이 나가던 걸, 배치 사이즈만큼 IN 절로 묶어서 한 번에 풀어낸다.

```java
@OneToMany(mappedBy = "author", fetch = FetchType.LAZY)
@BatchSize(size = 100)
private List<Post> posts;
```

Prisma에서 N+1을 만나는 경로는 거의 정해져 있다. `findMany`로 부모 목록을 가져온 뒤, 그 결과를 `for`로 돌면서 자식을 따로 부르는 모양이다.

```ts
// 안 좋은 패턴 — N+1
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { authorId: user.id } });
  // ...
}
```

이 코드가 100명의 사용자를 가져왔다면 SQL은 101번 나간다. 첫 줄에 한 번, `for` 안에서 100번. JPA 시절의 N+1과 정확히 같은 모양이다. Prisma는 `include`로 한 번에 묶을 수 있다.

```ts
const users = await prisma.user.findMany({
  include: { posts: true },
});
```

이게 가장 흔하고 가장 효과적인 답이다. JPQL fetch join의 자리에 정확히 들어선다. Prisma가 내부에서 두 번의 SQL을 던지는지(하나는 사용자, 하나는 IN 절로 모든 게시물) 한 번의 join을 던지는지는 버전과 옵션에 따라 다르지만, 어쨌든 N+1은 아니다.

N+1이 생기는 더 까다로운 자리는 GraphQL 같은 환경이다. 부모 한 마리를 받은 뒤 리졸버가 자식을 따로 가져오는 구조. 이때 자식 리졸버가 100번 호출되면 100번의 쿼리가 나간다. 부모 측에서 미리 `include`로 묶어둘 수가 없는 구조다. 이 자리에 들어서는 도구가 DataLoader다. Facebook에서 만든 작은 라이브러리고, 사고 방식은 단순하다. "한 이벤트 루프 틱 안에서 모인 ID들을 묶어 한 번의 쿼리로 처리한다."

```ts
import DataLoader from 'dataloader';

const postsByAuthorLoader = new DataLoader<number, Post[]>(async (authorIds) => {
  // authorIds: readonly number[]  — 한 틱 안에 모인 모든 ID
  const posts = await prisma.post.findMany({
    where: { authorId: { in: [...authorIds] } },
  });
  // 입력 순서대로 결과를 정렬해 반환해야 한다
  const grouped = new Map<number, Post[]>();
  for (const post of posts) {
    const list = grouped.get(post.authorId) ?? [];
    list.push(post);
    grouped.set(post.authorId, list);
  }
  return authorIds.map((id) => grouped.get(id) ?? []);
});

// 리졸버에서
async function userPosts(parent: User) {
  return postsByAuthorLoader.load(parent.id);
}
```

이 코드가 하는 일이 `@BatchSize`가 하는 일과 거의 같다. 100번의 `load()` 호출이 한 틱 안에 모이면 batch 함수가 한 번 호출되고, IN 절로 묶인 한 번의 SQL이 나간다. 도구의 이름이 다르고 모양이 다르지만, "여러 번의 단건 조회를 한 번의 IN 절로 합친다"는 사고 방식은 그대로다.

DataLoader는 GraphQL 진영에서 자주 보이지만, REST에서도 쓸 자리가 있다. 한 요청 안에서 여러 서비스 함수가 같은 리소스를 반복 조회한다면, 요청 단위로 DataLoader 인스턴스를 만들어 캐시 + 배치 효과를 얻는다. NestJS에서는 request-scoped 프로바이더로 이 패턴을 얹는다. 핵심은 한 가지다. 인스턴스는 요청마다 새로 만들어야 한다 — 안 그러면 다른 요청의 결과가 섞인다.

N+1을 잡는 가장 빠른 방법은 도구를 추가하는 게 아니라 SQL 로그를 켜는 일이다. Prisma에서는 `new PrismaClient({ log: ['query'] })`로 모든 쿼리를 로그로 떨어뜨릴 수 있다. 개발 중에 이걸 켜놓고 화면 한 번 갱신할 때 콘솔에 SQL이 몇 줄 떨어지는지를 본다. 100줄이 떨어지면 무언가 잘못된 것이다. JPA 시절 `show_sql=true` + `format_sql=true`를 켜놓고 봤던 그 풍경과 똑같다.

## Drizzle — JOOQ가 그리운 사람의 자리

JPA가 모두에게 맞았던 건 아니다. Java 진영에는 늘 JOOQ나 Querydsl을 사랑하는 사람들이 있었다. SQL을 SQL답게 적되, 컴파일 타임에 컬럼 이름과 타입을 잡아주는 도구를 원하는 사람들. 객체 그래프를 따라 내려가는 손맛보다, SELECT/FROM/JOIN/WHERE의 구조가 코드에 그대로 있는 손맛을 좋아하는 사람들이다. 이 손맛이 그리운 사람에게 Drizzle이 정확히 답이다.

Drizzle의 스키마는 타입스크립트 파일이다.

```ts
import { pgTable, serial, text, integer, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  authorId: integer('author_id').notNull().references(() => users.id),
  title: text('title').notNull(),
  body: text('body').notNull(),
  publishedAt: timestamp('published_at'),
});
```

이 모양이 JOOQ의 코드 생성 결과와 거의 같은 자리에 있다. 다른 점은 손으로 적는다는 것이다. 편하지는 않다. 그러나 한 번 적어두면 그 다음부터는 컴파일러가 모든 컬럼과 모든 타입을 알아본다. 쿼리는 이렇게 적는다.

```ts
import { db } from './db';
import { users, posts } from './schema';
import { eq, and, desc, isNotNull } from 'drizzle-orm';

const recent = await db
  .select({
    id: users.id,
    email: users.email,
    postTitle: posts.title,
    publishedAt: posts.publishedAt,
  })
  .from(users)
  .leftJoin(posts, eq(posts.authorId, users.id))
  .where(and(eq(users.id, 1), isNotNull(posts.publishedAt)))
  .orderBy(desc(posts.publishedAt))
  .limit(10);
```

JOOQ를 써본 사람은 몸에 익은 모양이다. SELECT, FROM, JOIN, WHERE, ORDER BY, LIMIT이 그대로 메서드 체인이 되고, 컬럼은 객체 속성으로 참조된다. `eq(posts.authorId, users.id)` 같은 헬퍼는 `org.jooq.impl.DSL.eq()`와 사고 방식이 같다. 결과 타입은 추론으로 정확히 떨어진다 — `select` 객체에 적은 키와 그 컬럼 타입이 합쳐져 한 줄로 좁혀진다.

Drizzle의 가장 큰 강점은 가벼움이다. 7KB 정도의 작은 라이브러리고, 쿼리 엔진 같은 별도 바이너리가 없다. Cloudflare Workers·AWS Lambda·Vercel Edge Functions 같은 콜드 스타트 민감 환경에서 진가가 나온다. Prisma가 자랑하는 마이그레이션 도구 같은 건 약한 편이다 — `drizzle-kit generate`가 SQL 스크립트를 만들어 주지만, 그 SQL을 사람이 한 번 더 보고 검토해야 한다는 후기가 많다. 자동화된 신뢰성은 Prisma 쪽이 더 강하다.

선택의 기준은 한두 줄로 정리된다. 마이그레이션 도구의 안전성과 자동 생성된 클라이언트의 DX가 최우선이면 Prisma. 번들 크기와 콜드 스타트와 SQL에 가까운 손맛이 최우선이면 Drizzle. 둘 사이에서 고민하다 보면 결국 "지금 만드는 시스템이 서버리스에 얼마나 깊이 들어가 있는가"가 갈림길의 한 축이 된다.

## Mongoose — Spring Data MongoDB의 자리

관계형 DB가 모든 답은 아니다. MongoDB를 쓰는 자리에서는 Spring Data MongoDB가 차지하던 위치를 Node 진영에서는 Mongoose가 가져간다. 사실상 표준이고, 거의 모든 Express/NestJS 프로젝트에서 만난다.

Mongoose의 사상은 분명하다. MongoDB는 스키마리스지만, 우리가 쓰는 컬렉션에는 결국 모양이 있다. 그 모양을 코드에 적자는 게 Mongoose의 출발이다.

```ts
import mongoose, { Schema, model, InferSchemaType } from 'mongoose';

const userSchema = new Schema({
  email: { type: String, required: true, unique: true },
  name: { type: String, required: true },
  posts: [{ type: Schema.Types.ObjectId, ref: 'Post' }],
  createdAt: { type: Date, default: Date.now },
});

type User = InferSchemaType<typeof userSchema>;

export const UserModel = model<User>('User', userSchema);
```

Spring Data MongoDB 출신이라면 `@Document` + `@Field`로 적던 모양이 비슷한 자리에 있다고 느낀다. populate(관계 채우기)는 Hibernate의 lazy join과 가장 닮은 자리다.

```ts
const user = await UserModel.findById(id).populate('posts');
```

이 코드가 두 번의 쿼리를 부르는 건 SQL ORM의 join과 다르고, 정확히 Spring Data MongoDB의 `@DBRef`나 lookup 단계의 사고 방식과 같다. 결과 타입을 정확히 좁히려면 `.populate<{ posts: Post[] }>('posts')` 식으로 명시해 줘야 한다는 디테일이 있고, 이 자리가 Prisma의 `include`만큼 매끈하지는 않다.

Mongoose의 트랜잭션은 MongoDB 4.0+의 Replica Set/Sharded 환경에서만 의미가 있다. 단일 서버 dev 환경에서는 트랜잭션이 silent하게 작동하지 않는 경우가 있고, 운영에서는 세션을 명시적으로 시작해 호출에 넘긴다.

```ts
const session = await mongoose.startSession();
session.startTransaction();
try {
  await UserModel.create([{ email, name }], { session });
  await PostModel.create([{ authorId, title }], { session });
  await session.commitTransaction();
} catch (err) {
  await session.abortTransaction();
  throw err;
} finally {
  session.endSession();
}
```

Spring 시절 `@Transactional` 한 줄로 끝났던 일이 try/catch/finally로 풀려 있다. Prisma의 `$transaction` 콜백 모양과 비교해도 더 길다. 분명한 단점이지만, 어떤 시점에 어떤 일이 일어나는지가 코드 표면에 그대로 드러난다는 면에서 Prisma의 명시성과 같은 결에 있다.

Spring 출신이 Mongoose에서 가장 자주 헷갈리는 자리는 두 가지다. 첫 번째는 `_id`가 ObjectId라는 점이다. JSON으로 직렬화할 때 문자열로 바뀌고 입력으로 받을 때 문자열에서 ObjectId로 다시 변환해야 한다. 두 번째는 populate가 자동이 아니라는 점이다. Hibernate의 lazy proxy 같은 동작은 없다. 부르지 않으면 그 자리에 ObjectId만 있다 — Prisma의 `include`와 정확히 같은 사상이다.

## Redis — Spring Data Redis가 ioredis로

Spring Boot 시절 우리가 Redis를 쓰던 모양은 거의 정형화되어 있었다. Spring Data Redis로 `RedisTemplate`을 주입받고, `@Cacheable`로 메서드 결과를 캐시하고, Pub/Sub은 `@RedisListener`로 받고, 분산 잠금은 Redisson 같은 라이브러리로 추상화했다. Node 진영에서 그 자리에 들어서는 라이브러리는 두 갈래다. `node-redis`(공식 클라이언트)와 `ioredis`(커뮤니티 표준에 가까움). 운영에서는 `ioredis`가 자주 보인다 — Cluster·Sentinel 지원이 안정적이고, Pipeline·Lua 호출 API가 깔끔하고, 자동 재연결이 견고하다는 평이다.

가장 단순한 사용은 GET/SET이다.

```ts
import Redis from 'ioredis';

const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: 6379,
});
// Cluster 사용 시:
// const redis = new Redis.Cluster([{ host, port }, ...]);

await redis.set('user:1:name', 'toby', 'EX', 60);
const name = await redis.get('user:1:name');
```

Spring `RedisTemplate.opsForValue().set()` 자리에 그대로 들어선다. Pub/Sub도 사고 방식이 같다. 구독 클라이언트와 발행 클라이언트를 따로 만드는 패턴 — 한 클라이언트가 구독 모드에 들어가면 다른 명령을 못 받는다는 Redis의 제약 때문 — 까지 그대로다.

분산 잠금은 운영에서 가장 자주 마주치는 자리다. Spring 진영에서는 Redisson의 `RLock`이 사실상 표준이었다. Node에서는 `ioredis` 위에 직접 `SET key value NX PX 30000` 패턴을 적거나, `redlock`이라는 라이브러리를 쓴다. 가장 단순한 패턴 한 가지를 적어 보자.

```ts
import Redis from 'ioredis';
import { randomUUID } from 'crypto';

const redis = new Redis();

async function withLock<T>(
  key: string,
  ttlMs: number,
  fn: () => Promise<T>,
): Promise<T> {
  const token = randomUUID();
  const lockKey = `lock:${key}`;

  const acquired = await redis.set(lockKey, token, 'PX', ttlMs, 'NX');
  if (acquired !== 'OK') {
    throw new Error(`could not acquire lock: ${key}`);
  }

  try {
    return await fn();
  } finally {
    // 자기 토큰일 때만 푼다 — Lua로 원자성 확보
    const unlock = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;
    await redis.eval(unlock, 1, lockKey, token);
  }
}

// 사용
await withLock('user:1:rebuild-cache', 5000, async () => {
  const data = await rebuildCache(1);
  await redis.set('cache:user:1', JSON.stringify(data), 'EX', 300);
});
```

세 가지가 핵심이다. 첫 번째, 잠금을 걸 때 NX(없을 때만 SET) + PX(만료 시간)로 원자성을 만든다. 두 번째, 토큰을 박아 두고 풀 때 자기 토큰인지 확인한다 — TTL이 만료된 뒤 다른 작업자가 걸었던 잠금을 우리가 잘못 풀어버리는 사태를 막는다. 세 번째, "확인 후 삭제"는 Lua 스크립트로 원자화한다. 이 셋이 다 갖춰져야 분산 잠금이라고 부를 수 있고, Redisson이 우리 모르게 해주던 일이 바로 이 세 가지다. 도구가 사라진 자리에 사고 방식이 그대로 드러난다.

운영 가다 보면 추가로 챙겨야 할 자리가 더 있다. Cluster 환경에서는 Redlock 알고리즘이 단일 마스터의 분산 잠금보다 안전하다. 한 노드의 장애와 동시에 다른 노드에 쓰기가 일어나는 경계 케이스에서 단일 마스터 잠금은 깨질 수 있고, Redlock은 다수의 노드에 동시에 락을 걸어 안전성을 높인다. 이 자리는 별도의 라이브러리(`redlock`)를 쓰는 편이 낫다.

캐시 패턴도 사고 방식이 같다. Spring `@Cacheable`이 하던 "메서드 결과를 키로 캐시하고 만료시키기"를 NestJS에서는 인터셉터로 적는다. `@nestjs/cache-manager` + `cache-manager-ioredis-yet` 조합이 가장 자주 쓰이고, 데코레이터로 `@CacheKey`를 붙이면 메서드 결과가 자동으로 캐시된다. Spring AOP가 하던 일이 인터셉터로 옮겨 와 있을 뿐이다.

## 마이그레이션 — Flyway·Liquibase의 자리

스키마 마이그레이션은 ORM의 가장 보수적인 영역이다. Spring 진영에는 두 가지 표준이 있다. Flyway는 SQL 파일을 버전 순으로 적용하는 단순한 모양이고, Liquibase는 changeset을 XML/YAML로 적되 다양한 DB로 추상화하는 모양이다. 둘 다 "한 번 적용된 마이그레이션은 다시 안 돌린다"는 원칙이 핵심이다. Node 진영에서 그 자리에 가장 강하게 들어선 도구가 Prisma Migrate다.

Prisma Migrate의 흐름은 이렇다. `.prisma` 스키마 파일을 고치고, `npx prisma migrate dev --name add-user-bio` 같은 명령을 친다. Prisma가 현재 DB 스키마와 새 `.prisma` 스키마를 비교해 SQL diff를 만들고, `migrations/20260504_add_user_bio/migration.sql` 같은 파일을 생성한 다음 그 SQL을 dev DB에 적용한다. 적용 이력은 `_prisma_migrations` 테이블에 기록된다 — Flyway의 `flyway_schema_history`와 같은 자리다.

운영 흐름은 다르다. dev에서는 `prisma migrate dev`가 SQL을 만들고 적용을 동시에 하지만, 프로덕션에서는 `prisma migrate deploy`만 쓴다. 이 명령은 새 SQL을 만들지 않는다. 이미 만들어 커밋된 SQL 파일들을 순서대로 적용할 뿐이다. 이게 운영에서 중요한 분리다 — 프로덕션 배포 시점에 도구가 SQL을 새로 만들면 큰 사고가 난다. Flyway/Liquibase에서도 같은 원칙이다.

```bash
# 개발 환경
npx prisma migrate dev --name add-user-bio
# → migrations/ 폴더에 SQL 생성, dev DB에 적용

# 운영 환경 (CI/CD 파이프라인 안에서)
npx prisma migrate deploy
# → 이미 커밋된 SQL을 운영 DB에 순서대로 적용
```

Drizzle의 `drizzle-kit generate`는 SQL 파일까지 만들어 주는 점에서 비슷하지만, 사람이 한 번 더 검토해야 한다는 후기가 많다. 컬럼 타입 변경 같은 자리에서 의도와 다른 SQL이 나올 수 있고, 자동화된 신뢰성에서 Prisma만큼 단단하지 않다. 신규 프로젝트에서 마이그레이션 안정성이 최우선이라면 Prisma가 가장 안전한 선택이다. 이 한 가지 사실이 Prisma 채택의 절반쯤을 설명한다.

마이그레이션의 가장 어려운 자리는 도구가 아니라 운영 패턴이다. 다운타임 없는 배포에서는 "코드 v1과 v2가 같은 시간에 같은 DB를 본다"는 상황을 인정하고 마이그레이션을 작성해야 한다. 컬럼을 `NOT NULL`로 바꾸고 싶다면, 한 번에 바꾸는 게 아니라 (1) nullable인 채로 새 컬럼 추가, (2) 두 코드 버전이 새 컬럼에 쓰는 동안 백필, (3) 모든 row가 채워진 뒤 `NOT NULL` 제약 추가 — 세 단계로 쪼개야 한다. 이 자리는 Prisma냐 Flyway냐의 차이가 거의 없다. 도구가 아니라 사고 방식의 문제다.

## 어떤 길을 갈 것인가 — Prisma·Drizzle·TypeORM 중에서

여기까지 따라온 사람이라면 어렴풋이 그림이 잡힌다. 그림을 산문으로 정리해 보자.

JPA·Hibernate에서 자라온 사람이 Node로 와서 가장 적은 학습 비용으로 생산성을 회복하고 싶다면, 답은 Prisma다. 마이그레이션이 안정적이고, DX가 일관되고, 타입 안전이 도구가 보장하는 수준에서 가장 강하다. lazy proxy와 dirty checking이라는 두 가지 마법은 못 가져오지만, 그 자리에 명시적 `include`/`select`와 `update` 호출이 들어선다. Spring 시절의 직관 — 도메인 서비스, 트랜잭션 경계, 리포지토리 — 이 거의 같은 모양으로 옮겨 온다. NestJS와 같이 쓰면 그림이 더 매끈해진다. 마이그레이션은 Prisma Migrate, 트랜잭션은 `prisma.$transaction` 콜백, 캐시는 `@nestjs/cache-manager`. 같은 손이 그대로 옮겨 가는 그림이다.

JOOQ나 Querydsl을 사랑했던 사람, SQL을 SQL답게 적되 컴파일러가 컬럼을 잡아주길 바라는 사람, 그리고 Cloudflare Workers나 Lambda Edge에 배포할 일이 잦은 사람이라면 Drizzle이 답이다. ORM의 추상화 한 겹을 걷어내고, 쿼리 빌더로서의 정직함을 즐길 수 있다. 마이그레이션 도구가 Prisma만큼 안전하지는 않다는 점, 그리고 스키마를 손으로 적어야 한다는 부담은 비용으로 받아들여야 한다.

TypeORM은 권장하기 어려워졌다. 데코레이터의 익숙함만 보고 신규 프로젝트에 도입하면 마이그레이션 신뢰성과 타입 안전성에서 약점을 만난다. 이미 TypeORM으로 가는 코드베이스가 있다면 무리해서 갈아엎을 필요는 없지만, 새 프로젝트의 첫 선택지로는 Prisma나 Drizzle이 낫다.

MongoDB를 쓰는 자리는 거의 자동으로 Mongoose다. 다른 답이 강하게 자리잡은 적이 없다. Redis는 거의 자동으로 ioredis다. 둘 다 사실상 표준이고, 새 프로젝트에서 다른 선택을 할 이유가 잘 없다.

이 모든 결정의 바닥에 한 줄의 사실이 있다. **JPA처럼 마법 같은 ORM은 Node에 없다.** Prisma가 가장 가까이 가 있지만, 자동 dirty checking과 lazy proxy는 안 한다. 처음 만나면 충격이고, 며칠 지나면 그 충격의 절반은 다른 감각으로 바뀐다. 어떤 SQL이 언제 나가는지가 코드 표면에서 보인다는 감각, 트랜잭션 경계가 함수의 괄호로 그려진다는 감각, 컬럼과 타입이 데코레이터가 아니라 코드 생성으로 묶여 있다는 감각. 잃은 게 분명히 있고, 얻은 것도 분명히 있다. 어느 쪽이 더 큰지는 며칠 운영해보면 자기 손에 잡힌다.

## 마무리

이 장에서 우리가 본 풍경은 한 줄로 정리하면 단순하다. **도구가 마법으로 가려놓던 자리가 코드 표면으로 올라왔다.** lazy proxy의 자리에 `include`가, dirty checking의 자리에 `update` 호출이, `@Transactional` AOP의 자리에 `$transaction` 콜백이, `@BatchSize`의 자리에 DataLoader가, Flyway의 자리에 Prisma Migrate가 들어선다. 도구의 모양은 다르지만 우리가 풀던 문제는 같다. "어떤 SQL을 어떤 트랜잭션 경계 안에서 어떤 순서로 던질 것인가."

처음에는 허전하다. JPA가 우리 손을 덜어주던 그 마법이 사라진 자리가 그립다. 그런데 그 그리움을 며칠 안고 가다 보면 코드가 다르게 읽히기 시작한다. 함수를 위에서 아래로 읽기만 해도 어떤 쿼리가 어떤 순서로 나가는지가 짐작이 되고, 트랜잭션 경계가 인자 타입으로 표현되고, 결과 타입이 쿼리 모양에서 자동으로 따라온다. 이 명시성에 한 번 익숙해진 사람은 다시 자동 마법으로 돌아가는 일을 망설이게 된다.

물론 명시성은 비용이다. 코드가 길어지고, `tx`를 들고 다녀야 하고, `include`를 깜빡 잊으면 `undefined`를 만난다. 그래서 NestJS 같은 프레임워크에서 컨벤션을 정해두는 일이 중요하다. 서비스 메서드는 `Prisma.TransactionClient`를 첫 인자로 받는다, 쿼리 모양은 `Prisma.validator`로 한 자리에 모은다, 결과 타입은 `Prisma.UserGetPayload`로 추출한다 — 이런 작은 약속들이 명시성의 비용을 깎아낸다. Spring 시절 `@Transactional` 한 줄로 끝나던 일이 우리 손으로 풀려 나오지만, 풀려 나오는 자리들이 어디인지가 일관되면 인지 부담이 줄어든다.

다음 장에서 우리는 또 한 번 도구의 자리가 옮겨 가는 풍경을 본다. JVM 시절에 손에 익었던 jstack·jmap·VisualVM·JFR 같은 도구들이 Node 진영에서 어떤 이름으로 다시 등장하는지를 따라간다. 이 ORM 장에서 본 사고 방식 — 도구는 바뀌지만 우리가 풀던 문제는 같다 — 이 디버깅·프로파일링·메모리 분석에서도 똑같이 적용된다. 운영 중인 컨테이너에 붙어 스레드 덤프를 뜨고, 힙 스냅샷을 받아 retainer chain을 읽고, flame graph로 핫스팟을 찾는 손이 어떻게 옮겨가는지 같이 가 보자.
