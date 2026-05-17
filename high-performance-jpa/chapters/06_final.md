# 6장. 트랜잭션 경계를 설계한다 — @Transactional과 OSIV

신입 시절 다들 한 번쯤 들어본 조언이 있다. *"DB 작업이 있는 메서드에는 `@Transactional`을 꼭 붙여라."* 듣고 보면 맞는 말이다. 그래서 우리는 그 말대로 했다. 서비스 메서드 위에 `@Transactional` 한 줄을 박았고, 어딘가에서 `LazyInitializationException`이 터졌다는 동료의 SOS를 받으면 그 메서드에도 `@Transactional`을 추가했다. 그렇게 우리 코드베이스에는 `@Transactional`이 점점 많아졌다.

그런데 어느 날, 한 번도 의심하지 않았던 풍경 하나가 눈에 들어온다. 컨트롤러에서 엔티티의 lazy 컬렉션을 호출했는데, 아무 일도 없이 *그냥 동작한다*. SQL이 한 줄 더 나가는 게 로그에 보이긴 한다. 하지만 예외는 없다. 트랜잭션은 분명 서비스에서 끝났을 텐데, 어떻게 컨트롤러에서 lazy 호출이 통할까? 잠시 멈춰 생각해보자. *이 환경은 정상인가?*

이 장에서 다룰 모든 이야기가 이 한 질문에서 출발한다. 트랜잭션을 *코드 한 줄로* 보는 시각과, 트랜잭션을 *시스템 경계로* 보는 시각의 차이. 그리고 그 경계를 흐리는 두 가지 큰 함정 — OSIV와 `enable_lazy_load_no_trans`. 어느 쪽도 그냥 두고 넘어갈 수 없는 친구들이다.

## `@Transactional`은 정말 한 줄이면 끝일까

먼저 `@Transactional`이라는 어노테이션 자체부터 다시 보자. 메서드 위에 한 줄 박는 그 어노테이션이 실제로 무엇을 결정하는지, 우리는 정말 알고 있을까?

Spring의 `@Transactional`은 속성이 여럿 달려 있다. 대부분의 코드는 `@Transactional` 한 줄만 쓰고 끝낸다. 즉 *모든 속성이 디폴트*다. 그런데 그 디폴트가 어떤 의미인지를 모르고 쓰면, 어느 새벽에 부메랑처럼 돌아온다. 하나씩 짚어보자.

### propagation — 트랜잭션은 어떻게 합쳐지고 갈라지는가

`propagation`의 기본값은 `REQUIRED`다. 의미는 단순하다. *이미 시작된 트랜잭션이 있으면 거기에 합류하고, 없으면 새로 시작한다.* 99%의 경우 이게 맞는 답이다. 두 번 의심할 일이 없다.

그런데 가끔 `REQUIRES_NEW`를 쓰고 싶은 순간이 온다. *바깥 트랜잭션이 롤백돼도, 이 안의 작업은 따로 커밋되길 바란다*는 요구다. 감사 로그를 남길 때, 또는 외부 시스템에 알림을 발송한 기록을 남길 때 자주 등장한다. `REQUIRES_NEW`를 선언하면 Spring은 바깥 트랜잭션을 *잠시 미뤄두고*(suspend) 새 물리 트랜잭션을 시작한다.

여기까지는 좋다. 그런데 한 가지 사실을 잊지 말자. *새 물리 트랜잭션은 새 커넥션을 필요로 한다*. 즉 같은 요청이 동시에 두 개의 커넥션을 점유한다. 1, 2장에서 우리가 줄이려고 그렇게 애썼던 그 커넥션 말이다. `REQUIRES_NEW`를 무심코 여기저기에 박아 두면, 풀 사이즈가 10인 환경에서 동시 5개 요청이 풀을 비울 수 있다. 끔찍한 일이다. 풀을 비우면 그 뒤로 도착하는 요청은 timeout으로 죽는다. *필요한 자리에만, 의식적으로* 쓰는 편이 낫다.

`NESTED`라는 옵션도 있다. 이건 진짜 새 트랜잭션이 아니라 *savepoint*다. 안쪽 작업이 실패하면 savepoint까지만 롤백하고 바깥 트랜잭션은 계속 간다. 한 가지 주의할 점은 NESTED는 JDBC 기반 트랜잭션 매니저에서만 동작한다는 것이다. JTA에서는 사용할 수 없다. 일반적인 Spring Boot + 단일 DB 환경이라면 쓸 수 있지만, *실무에서 정말 NESTED가 필요한 자리가 얼마나 자주 있는지*는 한 번 의심해볼 만하다. 대부분은 도메인 모델로 풀어내는 편이 낫다.

### isolation — 의식적으로 올리는 자리

`isolation`의 기본값은 DB 디폴트다. PostgreSQL이면 READ COMMITTED, Oracle도 READ COMMITTED, MySQL InnoDB는 REPEATABLE READ. 즉 *DB의 기본을 따라간다*. 이게 합리적인 디폴트다. 비즈니스 요구로 격리 수준을 *올려야 할 때*에만 의식적으로 명시하자.

그런데 한 가지 함정이 있다. 어떤 사람들은 *어디서 본 코드*를 따라 모든 트랜잭션에 `isolation = SERIALIZABLE`을 박아 둔다. 이러면 성능이 폭락한다. 동시성 문제는 isolation 한 줄로 풀 일이 아니다. 락과 isolation의 실전 이야기는 8장에서 따로 다룰 테니, 여기서는 한 가지만 기억하자. *isolation은 디폴트 두는 편이 낫다. 올릴 때는 이유가 있어야 한다.*

### rollbackFor — 가장 흔히 밟히는 지뢰

이 자리는 한 번도 본 적 없다면 거의 100% 한 번은 밟는 지뢰다. 잠시 멈춰서 보자.

Spring `@Transactional`의 기본 롤백 정책은 이렇다. **`RuntimeException`과 `Error`에서만 롤백한다. checked exception에서는 롤백하지 않는다.** 다시 한번 읽어보자. *checked exception에서는 롤백하지 않는다.*

```java
@Transactional
public void registerUser(UserRequest req) throws DuplicateEmailException {
    User user = new User(req);
    userRepository.save(user);
    if (emailService.isDuplicated(req.email())) {
        throw new DuplicateEmailException(req.email());
    }
}
```

이 코드를 무심코 보면 *예외가 터지면 롤백되겠지*라고 생각한다. 그런데 `DuplicateEmailException`이 `Exception`을 상속한 checked exception이라면, 이 메서드는 *예외를 던지면서도 커밋한다*. `save()`가 끝난 user는 DB에 남는다. 사용자가 화면에서 "중복 이메일입니다"라는 에러를 보고도, DB에는 회원이 한 명 추가돼 있다. 정말 찜찜한 일이다.

이 함정을 피하는 방법은 두 가지다. 첫째, *도메인 예외를 `RuntimeException` 기반으로 설계한다*. 사실 현대 Java/Spring 진영의 합의는 이쪽으로 거의 기울었다. 비즈니스 예외는 `RuntimeException`을 상속하는 편이 낫다. 둘째, 만약 checked exception을 쓸 수밖에 없다면 *`rollbackFor`에 명시*한다.

```java
@Transactional(rollbackFor = DuplicateEmailException.class)
public void registerUser(UserRequest req) throws DuplicateEmailException {
    // ...
}
```

가능하면 첫 번째 길로 가자. 매번 `rollbackFor`를 기억해서 쓰는 건 사람의 몫이고, 사람은 잊는다. 잊을 만한 일은 *기억할 필요 없게 설계*하는 편이 낫다.

여기까지가 `@Transactional`의 속성들이다. *한 줄로 끝이 아니다*는 사실은 어느 정도 다가왔으리라 본다. 자, 그렇다면 이제 정말 흥미로운 속성 하나를 따로 다뤄볼 차례다. `readOnly`다.

## `readOnly = true`는 단순한 힌트가 아니다

`@Transactional(readOnly = true)`. 이 한 단어가 정말 많은 일을 한다. 그런데 그 효과를 다 알고 쓰는 사람은 의외로 드물다. 같이 한번 풀어보자.

먼저 흔한 오해부터 짚자. *"readOnly = true는 그냥 힌트일 뿐이고, SELECT만 한다는 자기 선언 같은 거다"*라는 말. 절반은 맞고 절반은 틀리다. 트랜잭션 매니저는 이 플래그를 단순한 힌트로 흘려보내지 않는다. Hibernate를 쓰는 Spring 환경에서는 이 한 줄이 *두 가지 구체적 최적화*를 발동시킨다.

### 효과 1 — FlushMode가 MANUAL이 된다

기본 상태의 Hibernate Session은 `FlushMode.AUTO`다. 즉 트랜잭션 커밋 직전, 그리고 어떤 종류의 쿼리 실행 직전에 *자동으로* dirty checking을 돌고 변경 사항을 flush한다. 이 과정은 결코 공짜가 아니다. PersistenceContext에 엔티티가 1000개 들어있다면, 1000번의 dirty checking이 매 flush마다 일어난다.

읽기만 하는 트랜잭션에서는 dirty checking이 *원천적으로* 필요 없다. 변경하지 않을 거니까. 그런데도 디폴트는 매 쿼리 직전, 그리고 커밋 직전에 검사를 돈다. 정말 번거로운 낭비다.

`readOnly = true`를 박으면 Hibernate는 `FlushMode.MANUAL`로 동작한다. 자동 flush가 발생하지 않는다. dirty checking이 사실상 무효화된다. *읽기 트랜잭션에 변경이 안 새는*, 가장 직접적인 안전망이다.

### 효과 2 — LoadedState 스냅샷을 만들지 않는다

이게 사실 더 큰 이야기다. Spring 5.1+ 부터 `readOnly` 플래그가 Hibernate Session까지 끝까지 전파된다. 그 결과로 Hibernate는 *조회된 엔티티의 LoadedState 스냅샷*을 만들지 않는다.

3장에서 dirty checking을 다룰 때 LoadedState 이야기가 살짝 나왔을 것이다. Hibernate는 엔티티를 조회할 때 *현재 상태*뿐 아니라 *조회 시점의 원본 상태*도 함께 메모리에 보관한다. 나중에 dirty checking이 두 상태를 비교해야 하기 때문이다. 즉 엔티티 하나를 가져오면 메모리는 *두 배*를 쓴다.

읽기만 하는 트랜잭션에서는 이 LoadedState가 필요 없다. 비교할 일이 없으니까. `readOnly = true`는 이 스냅샷을 *아예 만들지 말라*는 신호다. 결과적으로 **읽기 트랜잭션의 메모리 사용량이 절반에 가깝게 줄어든다.** 한 번에 1000개의 글을 끌어오는 list API에서 이 차이는 보이지 않게 누적된다. GC 압박이 줄고, 페이지네이션이 한 번 더 가능해지고, OOM이 한 번 덜 터진다.

### 그래서 어떻게 써야 할까

Vlad의 실무 권고는 단순하다. **서비스 클래스에 디폴트 `@Transactional(readOnly = true)`을 박고, write 메서드에만 `@Transactional`로 오버라이드한다.** 코드로 보면 이렇다.

```java
@Service
@Transactional(readOnly = true)   // 디폴트는 readOnly
public class OrderService {

    public Order findById(Long id) {
        return orderRepository.findById(id).orElseThrow();
    }

    public List<OrderSummary> findRecent(int limit) {
        return orderRepository.findTopNByOrderByCreatedAtDesc(limit);
    }

    @Transactional                  // write만 오버라이드
    public Order place(OrderRequest req) {
        Order order = new Order(req);
        return orderRepository.save(order);
    }

    @Transactional
    public void cancel(Long id) {
        Order order = orderRepository.findById(id).orElseThrow();
        order.cancel();
    }
}
```

이 패턴의 좋은 점이 여럿 있다. 첫째, *디폴트가 안전한 쪽이다*. 깜빡 잊고 `@Transactional`을 안 붙인 read 메서드도 readOnly 디폴트의 보호를 받는다. 둘째, *쓰는 메서드를 한눈에 식별*할 수 있다. 클래스 안에서 `@Transactional`이 박혀 있는 메서드 = write 메서드라는 일관성. 셋째, *읽기 메서드의 메모리·flush 비용이 자동으로 절감*된다. 한 줄로 두 가지를 얻는 셈이다.

그리고 한 가지 더, *조금 뒤에 다룰 read-replica 라우팅까지 이 패턴이 그대로 풀어준다*. 이게 진짜 매력이다. 잊지 말고 이어서 보자.

### 의외의 발자국 — Repository에는 `@Transactional`을 박지 말자

여기서 잠시 한 가지 함정도 짚고 가자. 사람들이 가끔 `Repository` 인터페이스나 구현체에 직접 `@Transactional`을 박는다. 결론부터 말하면 *바람직하지 않다*. Spring Data JPA의 기본 Repository는 이미 메서드 단위로 트랜잭션을 처리한다. 거기에 우리가 또 `@Transactional`을 박으면, *서비스 계층에서 묶고 싶은 단일 트랜잭션*이 Repository 호출마다 쪼개진다. 한 서비스 메서드 안에서 `findX → updateY`를 호출했는데, *서로 다른 트랜잭션*에서 일어나면 atomicity가 깨진다.

트랜잭션 경계는 *비즈니스 단위*에 두는 편이 낫다. 그 단위는 거의 항상 *서비스 계층*이다. Repository는 트랜잭션의 *주체가 아니라 도구*다. 이 위치 감각을 한 번 굳혀 두자.

## 같은 readOnly가 라우팅까지 풀어준다

자, 이제 정말 흥미로운 자리로 들어가자. 위에서 약속한 *read-replica 라우팅*이다.

대부분의 운영 시스템은 어느 단계에 가면 read replica를 추가한다. 쓰기는 primary 한 대로 가야 하니 scaling이 막혀 있지만, 읽기는 여러 replica로 분산하면 처리량이 늘어난다. 문제는 *어떻게 분산하느냐*다. 코드의 어디에선가 *이 쿼리는 read니까 replica로 가라*는 결정을 해야 한다.

이 결정을 *서비스 계층의 어노테이션 한 줄*로 끝낼 수 있다면 어떨까. 정확히 이 일을 해주는 도구가 Spring의 `AbstractRoutingDataSource`다.

### `AbstractRoutingDataSource`로 라우팅하기

`AbstractRoutingDataSource`는 *런타임에* 어떤 DataSource를 쓸지 결정하는 추상 클래스다. `determineCurrentLookupKey()`라는 메서드 하나만 우리가 채워주면 된다. 그 안에서 *현재 트랜잭션이 readOnly인지*를 물어보고, 그 결과로 primary냐 replica냐를 고른다.

```java
public enum DataSourceType { READ_WRITE, READ_ONLY }

public class TransactionRoutingDataSource extends AbstractRoutingDataSource {

    @Override
    protected Object determineCurrentLookupKey() {
        return TransactionSynchronizationManager.isCurrentTransactionReadOnly()
            ? DataSourceType.READ_ONLY
            : DataSourceType.READ_WRITE;
    }
}
```

이게 전부다. Spring이 `@Transactional(readOnly = true)`인 트랜잭션을 시작할 때 `TransactionSynchronizationManager`에 그 플래그를 등록해 둔다. 우리의 `TransactionRoutingDataSource`는 그 플래그를 읽어서 라우팅 키를 정한다. 그 결과로 *우리가 위에서 한 작업 — 서비스 디폴트 readOnly, write만 오버라이드 — 이 그대로 read-replica 라우팅으로 풀린다*. 같은 한 줄이 메모리도 절감하고, flush도 끄고, 트래픽도 분산한다. 한 자리에서 셋이 따라오는 셈이다.

### 그런데 한 가지 *필수* 조건이 있다

이 라우팅이 의도대로 동작하려면, 한 가지 설정이 반드시 켜져 있어야 한다.

```properties
spring.jpa.properties.hibernate.connection.provider_disables_autocommit=true
```

이 설정의 의미는 2장에서 자세히 다뤘다. 짧게 회수하자면 *Hibernate가 트랜잭션이 진짜로 SQL을 던지기 직전까지 커넥션을 잡지 않게* 만드는 플래그다. 디폴트 상태의 Hibernate는 트랜잭션이 시작되자마자 커넥션을 풀에서 빼오고, 그 위에서 `setAutoCommit(false)`를 호출한다. *트랜잭션이 시작되는 순간*에 커넥션을 받아온다는 뜻이다.

이게 라우팅과 충돌한다. 왜 그럴까? `@Transactional(readOnly = true)` 메서드가 시작되면 Spring이 트랜잭션 매니저를 통해 *커넥션을 미리 받아온다*. 그런데 이 시점에 우리의 `determineCurrentLookupKey()`가 호출되어 라우팅 키가 결정된다. 여기까지는 좋다. 그런데 만약 이 시점에 어떤 이유로 라우팅 정보가 아직 등록되지 않았다거나, autocommit을 끄려고 잡은 커넥션이 *primary로 잡혔다가 replica로 바꿔야 하는* 상황이 생기면 라우팅이 비틀린다.

`provider_disables_autocommit=true`로 켜 두면 Hibernate는 *진짜 SQL이 나가는 시점*까지 커넥션 획득을 미룬다. 그 시점이면 Spring의 트랜잭션 플래그는 이미 안정적으로 등록돼 있고, 라우팅이 깨끗하게 결정된다. 그리고 한 가지 부수적인 효과도 있다 — *트랜잭션 시작 시점부터 첫 SQL이 나가기까지의 시간 동안 커넥션을 점유하지 않는다*. 커넥션 lease time이 줄어든다. 2장의 핵심 주제였던 *커넥션을 짧게 쓰기*가 다시 풀린다.

설정 파일에는 풀 자체에서도 짝을 맞춰주는 편이 낫다. HikariCP라면 이렇게.

```properties
spring.datasource.hikari.auto-commit=false
spring.jpa.properties.hibernate.connection.provider_disables_autocommit=true
```

이 두 줄이 짝을 이뤄야 라우팅이 의도대로 돌아간다. 잊지 말고 같이 켜자.

이렇게 *서비스 디폴트 readOnly + 라우팅 + provider_disables_autocommit*, 이 세 가지가 한 묶음이다. 이 묶음을 굳혀 두면, 읽기 트래픽은 자동으로 replica로 흘러가고, 쓰기만 primary로 모인다. 화려한 코드 변경 없이도 우리 시스템의 read scaling이 한 단계 올라간다. 그리고 우리는 그저 *서비스 계층의 트랜잭션 경계를 깔끔하게 그려둔 것*뿐이다.

자, 트랜잭션 경계를 시스템 설계로 보는 시각이 한 번 풀렸다. 그렇다면 이제 *그 경계를 흐리는 가장 큰 함정*과 마주할 시간이다. OSIV다.

## OSIV — 정말 한 번도 의심하지 않았던 환경

처음에 던졌던 질문을 다시 꺼내보자. *컨트롤러에서 lazy를 호출했는데 동작하는 이 환경은 정상인가?* 답을 한 줄로 말하면 이렇다. *정상이 아니다. 단지 익숙해서 정상처럼 보이는 것뿐이다.*

이 환경의 이름이 OSIV — Open Session in View — 다. 의미는 글자 그대로다. *View가 렌더링되는 동안에도 Session(=PersistenceContext)을 열어둔다*. Spring Boot의 디폴트는 *켜져 있음*이다. 그래서 우리는 한 번도 의심하지 않고 lazy 호출이 통하는 환경에 익숙해졌다.

OSIV는 표면적으로는 정말 편리하다. 서비스가 엔티티를 반환하고 컨트롤러가 그 엔티티의 lazy 컬렉션을 자유롭게 호출해도, 어떤 예외도 나지 않는다. View 템플릿에서 `${order.items}`를 펼치면 그 자리에서 SQL이 나가고 컬렉션이 채워진다. *DTO 매핑 보일러플레이트가 사라진다*. 처음 보면 매력적이다.

그런데 우리는 이미 한참 더 멀리 와 있다. *그게 왜 안티패턴인지*를, 그것도 *다섯 가지나*. 하나씩 천천히 보자.

### 첫째, 커넥션 lease time이 폭발한다

OSIV가 켜진 상태에서 한 요청의 라이프사이클을 따라가보자.

1. 컨트롤러에 요청이 들어온다.
2. Spring이 PersistenceContext를 연다.
3. *DB 커넥션이 풀에서 빠진다*.
4. 서비스가 호출되고 SQL이 나간다.
5. 서비스 트랜잭션이 끝난다.
6. **그런데 PersistenceContext는 안 닫힌다. 커넥션도 풀로 돌아가지 않는다.**
7. 컨트롤러가 결과를 받아 View에 넘긴다.
8. View가 렌더링되면서 lazy 컬렉션을 호출한다.
9. 그 자리에서 SQL이 또 나간다.
10. View 렌더링이 다 끝난다.
11. 그제야 PersistenceContext가 닫히고 커넥션이 풀로 돌아간다.

문제가 보이는가? *비즈니스 로직이 끝난 5번 시점*에 커넥션이 풀로 돌아가야 마땅하다. 그런데 OSIV 때문에 *View 렌더링이 끝나는 11번까지* 커넥션을 점유한다. View 렌더링은 길다. 템플릿 엔진을 쓰면 더 길고, 외부 API 호출이 섞이면 끔찍하게 길어진다. 그 시간 동안 커넥션 하나가 *놀면서 점유*된다.

2장에서 우리가 그렇게 강조했던 한 가지를 떠올려보자. *동시 요청 수 = 풀 사이즈가 아니라, 평균 커넥션 점유 시간이 진짜 병목이다.* OSIV는 그 점유 시간을 *비즈니스 로직 시간 + View 시간*으로 늘려놓는다. 같은 트래픽을 받는데 풀이 두 배, 세 배 빨리 소진된다. 신규 서비스 초기에는 안 보이지만, 트래픽이 임계점을 넘는 순간 풀이 비고 모든 요청이 timeout으로 죽기 시작한다. 이게 한국 커뮤니티 사례에서도 반복되는 패턴이다.

### 둘째, 트랜잭션 경계가 깨진다

여기가 더 미묘한 문제다. 서비스에서 트랜잭션이 끝났는데, OSIV는 컨트롤러까지 *PersistenceContext만* 들고 간다. 트랜잭션은 끝나 있다는 점에 주목하자.

그 상태에서 컨트롤러에서 lazy 호출이 일어나면 그 SQL은 어떻게 실행될까? 답은 *auto-commit으로 한 statement씩*이다. 즉 그 SQL 하나만 자기 자신의 트랜잭션으로 처리된다. statement 하나에 트랜잭션 하나. 정말 찜찜하다.

이게 왜 문제일까? 가장 간단한 시나리오 하나만 봐도 충분하다. 서비스 트랜잭션 안에서 `Order` 한 건을 조회했고, 그 안에 `Items` 컬렉션이 LAZY로 매달려 있다. 트랜잭션이 끝난 뒤 컨트롤러에서 `Items`를 펼친다. 이 시점에 다른 트랜잭션이 그 사이에 `Items`를 *수정해 커밋*했다면? 컨트롤러가 보는 `Items`는 *서비스가 조회한 Order의 시점*과 일관되지 않은 *나중 상태*다. 같은 화면에 표시되는 한 페이지가 두 개의 다른 트랜잭션에서 본 데이터로 짜인다. 일관성이 깨졌다는 사실을 *눈에 보이게* 알 수 있는 방법조차 없다.

대부분의 상황에서는 이게 큰 사고로 번지지 않는다. 그래서 사람들은 OSIV를 *안전한 편의 기능*으로 인식하고 산다. 그러다 어느 날, 결제·재고·정산 같은 영역에 이 패턴이 그대로 들어가는 순간, 디버깅 불가능한 데이터 일관성 사고가 터진다. *원인 추적조차 어려운 사고*다. 끔찍한 일이다.

### 셋째, 계층 책임이 누설된다

OSIV가 켜져 있으면 컨트롤러에서 `entity.getItems()` 한 줄을 호출하는 게 *그저 메서드 호출*처럼 보인다. 그런데 그 한 줄이 *SQL을 발생시킨다*. UI를 짜는 개발자가 UI 코드를 쓰면서, *자기도 모르게 DB 쿼리를 추가하고 있는* 셈이다. 

계층 경계를 그려둔 의미가 사라진다. Repository는 DB 호출, 서비스는 비즈니스 로직, 컨트롤러는 변환 — 이 분리가 코드 컨벤션 차원에서는 살아 있어도, *실제 실행 모델*에서는 컨트롤러와 View가 자유롭게 Repository 일을 한다. 코드 리뷰에서 어떤 SQL이 어디서 나가는지 *읽을 수가 없다*. 한 번 익숙해지면 이게 얼마나 이상한 일인지조차 잊는다.

### 넷째, N+1이 자유롭게 발생한다

이건 4장 N+1 이야기와 그대로 이어진다. OSIV가 컨트롤러까지 lazy를 허용하는 환경이면, *컨트롤러를 짜는 개발자는 ORM의 비용을 의식하지 않는다*. 화면이 필요로 하는 데이터를 그저 *엔티티 그래프를 타고* 가져오면 된다고 믿는다. 그 결과 한 화면을 그리는 데 SQL이 100번 나가도 *그 100번의 발생 위치가 보이지 않는다*.

서비스에서 fetch plan을 세우는 의식 자체가 약해진다. 4장에서 `JOIN FETCH`니 `@EntityGraph`니 `default_batch_fetch_size`니 그렇게 정리한 도구들이 *쓰일 동기*를 잃는다. 왜냐하면 *fetch 안 해도 컨트롤러에서 알아서 가져와지니까*. OSIV는 N+1의 토양이다. N+1을 만들기 정말 쉽다.

### 다섯째, 테스트가 어렵다

마지막은 좀 미묘하지만 누적되면 큰 문제다. lazy 호출이 컨트롤러나 View에서 일어난다는 건, *그 호출의 동작을 단위 테스트로 검증할 수 없다*는 뜻이다. 서비스만 떼서 테스트하면 그 부분의 SQL이 일어나지 않는다. 통합 테스트, MockMvc, 풀 스택 부트 테스트가 동원돼야 비로소 *실제 어떤 SQL이 나가는지*를 본다. 테스트 비용이 비싸진다. 그리고 비싼 테스트는 잘 안 짜진다.

종합하면 — OSIV는 다섯 가지 모서리에서 우리를 찌른다. *커넥션 lease가 늘어나고, 트랜잭션 경계가 깨지고, 계층 책임이 누설되고, N+1이 자유로워지고, 테스트가 어려워진다*. 어느 한쪽만 봐도 만만치 않은데, OSIV 하나가 다섯 가지 모서리를 동시에 만든다.

이 자리에서 한 줄, Vlad의 표현을 그대로 인용해두자.

> "Open Session in View is a solution to a problem that should not exist in the first place. The most likely root cause is relying exclusively on entity fetching."

번역하자면 *애초에 존재해서는 안 될 문제에 대한 해결책*. 그리고 *그 문제의 가장 흔한 뿌리는 엔티티 fetch에만 의존하는 것*. 한 문장 안에 우리가 5장까지 다뤄온 모든 이야기가 압축돼 있다. *수정 안 할 read는 모두 DTO*. *fetch plan은 쿼리별로*. 이 두 가지를 굳혀두면 OSIV가 제공한다는 *편의*는 사실 필요 없다. 우리에게는 더 나은 도구가 이미 있다.

### Spring Boot의 디폴트와, 새 프로젝트의 첫 줄

Spring Boot 2.0부터는 OSIV가 켜져 있으면 부트 시 경고 로그를 찍는다. 디폴트 값은 여전히 *true*다 (호환성 이유다). 그러나 *경고는 분명하게* 띄운다. 우리는 그 경고를 읽고 끄는 편이 낫다.

새 프로젝트를 시작할 때 `application.properties`의 첫 줄을 이렇게 두자.

```properties
spring.jpa.open-in-view=false
```

말 그대로 *첫 줄*이다. 이 한 줄이 우리 시스템의 트랜잭션 경계를 깨끗하게 그려둔다. 코드를 한 줄도 더 쓰기 전에 박아두자. 그러면 처음부터 lazy 호출을 *서비스 안*에서 끝내는 코드 컨벤션이 자연스럽게 자리잡는다. 처음 잘 그려둔 경계는 시간이 갈수록 값을 한다.

### 그런데, OSIV를 켜고 싶다는 사람들의 이야기도 들어보자

여기서 한 가지 솔직한 이야기를 같이 해야겠다. OSIV를 옹호하는 입장도 분명히 존재한다. 작은 팀이거나 사내 도구를 빠르게 짜는 자리, 또는 CRUD 위주의 단순한 시스템에서는 *컨트롤러까지 lazy navigation을 허용해야 DTO 매핑 보일러플레이트를 줄일 수 있다*는 주장이다. Stack Overflow의 많은 답변, 그리고 Spring 1.x 시절의 표준 설명도 이 입장에 가까웠다. 일리가 없는 주장은 아니다.

이 입장에 대한 답을 한 줄로 하면 이렇다. *DTO 보일러플레이트를 줄이는 도구는 OSIV 말고도 충분히 많다*. 5장에서 이미 다뤘다. Spring Data Interface Projection은 매핑 코드를 거의 안 쓴다. JPQL constructor expression은 줄 수가 적다. `@EntityGraph`는 한 줄로 fetch plan을 깔끔하게 정한다. MapStruct 같은 매퍼는 매핑 코드를 컴파일 타임에 만들어준다.

즉 OSIV가 주는 *유일한 편익 — 매핑 보일러플레이트 절감 — 은 다른 도구로 더 안전하게 풀린다*. 그리고 그 도구들은 OSIV의 다섯 가지 부작용을 *주지 않는다*. 타협안으로 정리하면 한 줄이다. **OSIV를 끄는 대신, 5장의 Projection과 4장의 EntityGraph로 보강하자.**

이 한 줄을 굳혀두면, OSIV 옹호 입장에 대한 우리 팀의 답이 분명해진다. *우리는 OSIV의 편익을 다른 도구로 더 좋게 얻는다*. 새 프로젝트의 첫 줄이 `spring.jpa.open-in-view=false`인 이유가 여기 있다.

## 더 큰 함정 — `hibernate.enable_lazy_load_no_trans=true`

OSIV에 대해 길게 이야기했다. 그런데 사실 *더 큰 함정* 하나가 따로 있다. 이 자리에서 정말 분명하게 짚고 가야 한다.

`hibernate.enable_lazy_load_no_trans=true`라는 설정이 있다. 이름이 길지만 의미는 짧다. *트랜잭션 없이도 lazy 로딩을 허용한다*. 즉 PersistenceContext 밖에서, 트랜잭션 밖에서, lazy 컬렉션을 호출해도 `LazyInitializationException`이 나지 않게 만든다.

언뜻 보면 OSIV와 닮았다. *컨트롤러에서 lazy 호출이 통하게 만든다*는 점에서 결과가 비슷하다. 그래서 어떤 사람들은 "OSIV가 안티패턴이라니, 그럼 `enable_lazy_load_no_trans`를 켜면 되겠네"라고 생각한다.

여기서 분명히 말해두자. **`enable_lazy_load_no_trans=true`는 OSIV보다 *더* 큰 함정이다. 어떤 상황에서도 켜지 않는다.**

### 왜 더 큰 함정인가

OSIV는 한 요청 내내 같은 PersistenceContext, 같은 커넥션을 *유지*했다. 그게 다섯 가지 문제를 만들었다. 그런데 적어도 *같은 트랜잭션*은 아니어도 *같은 PersistenceContext*는 유지됐다. lazy 호출은 그 컨텍스트 안에서 처리됐다.

`enable_lazy_load_no_trans`는 다르다. *PersistenceContext가 닫힌 뒤*의 lazy 호출에도 동작한다. 어떻게? Hibernate가 *그 자리에서* 임시 Session을 새로 열고, *새 트랜잭션을 시작*하고, SQL을 한 번 던지고, 트랜잭션을 닫는다. *lazy 호출 한 번 = 새 트랜잭션 하나 = 새 커넥션 하나*.

상상해보자. 한 화면에 글 100개가 있고, 각각 `Author` 컬렉션이 LAZY다. View 렌더링 중 100개의 `Author`를 펼친다. *100번의 lazy 호출 = 100번의 새 트랜잭션 = 100번의 커넥션 획득/반환*. 정말 아찔하다.

OSIV가 커넥션 한 개를 길게 점유했다면, `enable_lazy_load_no_trans`는 커넥션을 *발작적으로* 잡았다 놨다 한다. 풀의 lease 시간은 짧을지언정, *풀 사용 빈도가 폭증한다*. 풀 contention이 끔찍해진다. 약간의 트래픽만 들어와도 풀이 깨진다. 그리고 더 심각한 문제는 *각 lazy 호출이 별개의 트랜잭션*이라는 사실이다.

### 일관성이 완전히 무너진다

이 부분이 가장 무서운 자리다.

OSIV에서는 적어도 *하나의 PersistenceContext가 1차 캐시 역할*을 하면서 같은 엔티티의 동일성을 어느 정도 지켰다. `enable_lazy_load_no_trans`는 그런 안전망조차 없다. lazy 호출 100번이 100개의 *독립된 트랜잭션*이라면, 그 100번이 각각 *서로 다른 시점*의 데이터를 본다. 그 사이에 누군가 데이터를 수정해 커밋했다면, 한 화면에 *100개의 다른 트랜잭션이 본 데이터*가 섞여 표시된다.

대시보드 한 페이지를 그렸는데, 1번 글의 작성자는 *수정 전* 이름이고, 50번 글의 작성자는 *수정 후* 이름이다. 디버깅하는 사람 입장에서 이게 어떻게 보일까? *재현이 안 된다*. *원인을 찾을 수가 없다*. 코드 어디에도 *그런 일이 일어나라*고 쓰여 있지 않으니까. 설정 한 줄이 그 일을 한 거다.

### 이름이 주는 함정

이 설정의 이름이 함정을 한 번 더 만든다. `enable_lazy_load_no_trans`. *트랜잭션 없이도 lazy를 허용한다*는 뜻으로 읽힌다. 어떤 신입 개발자가 한 번도 본 적 없는 `LazyInitializationException`을 만나, "구글링했더니 이 옵션을 켜면 된다더라"는 답을 찾는다. 그래서 켠다. 예외가 사라진다. 끝.

그 한 줄이 풀어버린 *연쇄적 결과*는 아무도 보지 못한다. 트래픽이 적은 dev/스테이지 환경에서는 멀쩡하다. 운영에 올라가서 *어느 정도 트래픽이 모이는 순간*, 풀 contention과 데이터 일관성 깨짐이 동시에 폭발한다. 그제야 누군가 그 설정을 추적해 찾아낸다. 끔찍한 일이다.

### 우리 코드에서 켜져 있다면

만약 우리 코드에 이 설정이 켜져 있다면 — *지금 당장* 끄자.

```properties
# 이 줄이 있다면 즉시 지운다
# spring.jpa.properties.hibernate.enable_lazy_load_no_trans=true
```

설정 파일을 grep해보자. `hibernate.properties`, `application.yml`, `persistence.xml` 어디에든 박혀 있을 수 있다. 어디에서도 *그것의 효과*를 정확히 모른 채 *예외를 막기 위해* 켜놓은 경우가 대부분이다.

끄면 어떤 일이 일어날까? *전에 안 보이던 `LazyInitializationException`이 다시 보인다*. 좋은 일이다. 그 예외가 나는 자리가 우리 코드가 *트랜잭션 경계를 잘못 그린 자리*다. 예외를 *증상*이 아니라 *진단 신호*로 받아들이자. 그 자리를 하나씩 고친다.

고치는 방법은 우리가 이미 안다.
- 해당 응답에 필요한 lazy 컬렉션을 *서비스 안에서* `JOIN FETCH` 또는 `@EntityGraph`로 미리 가져온다 (4장).
- 또는 응답 형태를 *DTO Projection*으로 바꿔서 lazy 자체가 필요 없게 만든다 (5장).
- 그것도 어렵다면 그 응답 전체에 대한 트랜잭션 경계를 다시 그린다 — 하지만 OSIV로 돌아가지는 않는다.

이 절차를 거치면 우리 시스템은 *훨씬 더 정직한 트랜잭션 경계*를 갖게 된다. 한 번 거쳐갈 만한 통과의례다. 시간 들이는 만큼 갚는다.

## 트랜잭션 경계는 코드 한 줄이 아니라 시스템 설계다

여기까지 길게 왔다. 마무리에 가깝다. 그 전에 한 가지를 정리해두자. 이 장을 관통한 한 가지 시각의 변화는 이렇다.

처음에 우리는 `@Transactional`을 *코드 한 줄*로 봤다. 메서드 위에 박는 어노테이션. 까먹지 말자, 빠뜨리지 말자, 그게 전부였다.

지금 우리는 같은 어노테이션을 *시스템 경계의 선언*으로 본다. 한 줄이 결정하는 것들의 목록이 길다.

- propagation은 트랜잭션의 *합류와 분기*를 결정한다.
- isolation은 *동시성 anomaly의 허용 수준*을 결정한다.
- rollbackFor는 *예외 정책*을 결정한다.
- readOnly는 *flush 모드, 메모리 사용량, 라우팅*까지 결정한다.

그리고 *어디까지* 트랜잭션을 끌고 가느냐 — 이것이 OSIV와 `enable_lazy_load_no_trans`가 던지는 질문이었다. 둘 다 *컨트롤러까지* 끌고 가는 옵션이지만, 그 결과는 다섯 가지 안티패턴이고 운영 사고다. 우리가 그린 경계는 *서비스 계층까지*. 서비스 안에서 fetch plan을 완성하고, 닫힌 엔티티 또는 DTO로 컨트롤러에 넘긴다. 컨트롤러는 *DB 호출하지 않는다*. View는 *DB 호출하지 않는다*. 이 한 가지 원칙이 우리 시스템의 절반을 정직하게 만든다.

같은 한 줄(`@Transactional(readOnly = true)`)이 *flush를 끄고, 메모리를 절반으로 줄이고, replica 라우팅까지 풀어준다*. 한 줄이 셋을 한다. 그 한 줄이 깔끔하게 동작하려면 *Repository에는 트랜잭션을 박지 않고*, *provider_disables_autocommit을 켜고*, *서비스 디폴트 readOnly + write 오버라이드 패턴*을 굳혀두면 된다.

OSIV는 끈다. 새 프로젝트의 첫 줄이 `spring.jpa.open-in-view=false`다. *DTO 보일러플레이트라는 명분*은 5장의 Projection으로 더 좋게 푼다.

`enable_lazy_load_no_trans`는 어떤 경우에도 켜지 않는다. 켜져 있다면 *지금 즉시* 끈다. 그 자리에서 드러나는 예외들이 우리 코드의 *진짜 경계 누락*이다. 하나씩 고친다.

이 시각을 한 줄로 압축하면 이렇다. *트랜잭션은 코드 한 줄이 아니라 시스템의 일관성 경계다*. 그 경계가 *서비스 계층에서 깔끔하게 닫혀 있어야* 컨트롤러도, View도, replica 라우팅도, 풀 사이즈도 정상적으로 일한다. 그렇지 않으면 한 자리의 누설이 다섯 자리의 부작용으로 번진다.

## 내 코드 체크리스트 3개

이 장이 우리에게 시킨 일을 한 줄씩 점검할 수 있게 추려두자.

- **`spring.jpa.open-in-view`가 `false`로 설정돼 있는가?** 새 프로젝트라면 첫 줄로, 기존 프로젝트라면 끄고 나오는 예외들을 *진단 신호*로 받아 하나씩 고친다. 끄지 않은 채로는 트랜잭션 경계 이야기를 시작할 수 없다.

- **서비스 클래스에 디폴트 `@Transactional(readOnly = true)`이 박혀 있고, write 메서드에만 `@Transactional`이 오버라이드돼 있는가?** 이 패턴 한 줄이 flush·메모리·라우팅 셋을 한 번에 풀어준다. 그리고 Repository에는 `@Transactional`을 박지 않는다 — 트랜잭션 경계는 *비즈니스 단위*에 둔다.

- **`hibernate.enable_lazy_load_no_trans`가 *꺼져* 있는가?** 켜져 있다면 그 자체가 사고의 위치다. 즉시 끄고 드러나는 예외들을 4장·5장의 도구(JOIN FETCH, EntityGraph, DTO Projection)로 정직하게 해결한다. 임시방편으로 다시 켜지 않는다.

## 다음 장 — 그래서, 캐시는 답일까

트랜잭션 경계를 깔끔하게 그렸다. lazy 자유 발생을 막았고, readOnly로 메모리를 줄였고, replica 라우팅까지 풀었다. 우리 시스템의 *DB 호출 모양*이 정직해졌다.

그런데 한 가지 의문이 자연스럽게 떠오른다. *그래도 read replica로 풀리지 않는, 같은 SQL이 너무 자주 나가는 자리*는 어떻게 할까? 캐시는 답일까? Hibernate의 1차 캐시, 2차 캐시, 쿼리 캐시. 이름은 익숙하지만 *언제 켤 만한 것이고, 언제는 켜면 안 되는지*를 정직하게 다뤄볼 자리다.

다음 7장의 슬로건을 한 줄 미리 던져두자. *"캐시는 정당한 이유 있을 때만. 켜기 전에 DB·replica·application cache를 먼저."* Vlad의 14 tips 중 한 줄이다. 이 슬로건을 어떻게 풀어야 우리가 캐시를 *방패가 아니라 도구로* 쓸 수 있는지, 다음 장에서 함께 살펴보자.
