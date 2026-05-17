# 2장. 커넥션은 적을수록 빠르다 — JDBC, 풀, 그리고 statement caching

상황 하나를 떠올려보자. 운영팀에서 다급한 메시지가 날아온다. "응답 시간이 튄다", "DB가 또 죽을 것 같다". 모니터링 대시보드를 켜보면 TPS는 평소와 다를 게 없는데, p99 응답 시간이 갑자기 두 배가 되어 있다. 어딘가에서 누군가가 한마디 던진다. "커넥션 풀이 작아서 그래요. `maximumPoolSize`를 30에서 100으로 올려봅시다."

이 한 줄은 너무 자주 들린다. 그리고 들을 때마다 어딘지 찜찜하다. 왜냐하면 1장에서 우리가 이미 한 번 본 그 수치 — 64 트랜잭션 워크로드에서 HikariCP 기본 10개로는 149ms, 64개로 늘리면 272ms, FlexyPool이 발견한 4개에서는 128ms — 이 수치는 정확히 그 직관과 반대 방향을 가리키고 있었기 때문이다. 풀을 키울수록 빨라진다는 가정이 시원하게 깨지는 순간을, 우리는 이미 한 번 봤다.

그렇다면 이 2장에서 던질 질문은 이렇다. 트랜잭션은 정확히 *언제* 커넥션을 잡을까? 풀을 어느 정도 크기로 두는 게 합리적일까? 그리고 같은 PreparedStatement를 천 번 던지면 정말 그 SQL이 한 번만 컴파일되고 있는 걸까? 이 세 질문에 답하는 동안 우리는 커넥션 풀에서 statement cache까지, 한 트랜잭션이 시작해서 끝나는 그 짧은 구간에 무슨 일이 벌어지는지를 한 번 더 깊게 들여다보게 된다.

이 챕터를 다 읽고 나면, 자기 프로젝트의 JDBC URL 한 줄을 다시 열어보고 싶어질 것이다. 거기에 무엇이 빠져 있는지, 무엇이 잘못 들어가 있는지 30초 만에 확인할 수 있게 된다.

## 풀을 키우면 왜 더 느려지는가

1장에서 마주한 충격적인 수치를 다시 천천히 풀어보자. Vlad Mihalcea가 *High-Performance Java Persistence* 본문과 블로그 시리즈에서 반복해서 제시하는 그 실험이다. 64개의 동시 송금 트랜잭션을 같은 PostgreSQL 인스턴스에 던졌을 때, HikariCP의 풀 크기를 어떻게 잡느냐에 따라 처리 시간이 이렇게 달라졌다.

| 풀 크기 | 평균 트랜잭션 처리 시간 |
|---------|------------------------|
| 10 (HikariCP 기본) | 149 ms |
| 64 (동시 트랜잭션 수와 동일) | 272 ms |
| **4 (FlexyPool이 찾아낸 적정값)** | **128 ms** |

64개의 트랜잭션이 동시에 들어오니까 커넥션도 64개 있으면 되겠지? 직관적으로는 가장 합리적인 답이다. 그런데 결과는 정반대다. 풀을 늘렸더니 거의 두 배 가까이 느려졌다. 더 놀라운 건 4개라는 숫자다. 64개의 트랜잭션을 단 4개의 커넥션으로 처리할 때 가장 빨랐다. 처음 보면 "이게 가능한가?" 싶다.

여기서 우리가 마주하는 건 Universal Scalability Law라는 오래된 직관이다. Neil Gunther가 제시한 이 모델은 한 시스템에 동시 작업자를 늘리면 처음에는 처리량이 선형으로 증가하지만, 어느 임계점을 지나면 *경쟁 비용*(contention)과 *일관성 유지 비용*(coherency)이 누적되면서 오히려 처리량이 떨어진다는 이야기다. 데이터베이스도 예외가 아니다. 아니, 데이터베이스야말로 이 법칙이 가장 잔혹하게 적용되는 무대다.

커넥션 하나가 늘어난다는 건 단순히 소켓 하나가 더 생긴다는 의미가 아니다. 그 뒤에는 백엔드 프로세스(PostgreSQL의 경우)나 스레드(MySQL의 경우)가 따라붙는다. 각각이 CPU 시간을 다투고, 공유 메모리 영역의 라치(latch)를 다투고, lock manager의 슬롯을 다투고, 디스크 I/O 큐를 다툰다. 64개의 백엔드가 동시에 같은 인덱스 페이지에 락을 걸려고 한다고 상상해보자. 누군가는 반드시 기다려야 한다. 한 명이 기다리는 시간이 두 명이 기다리는 시간보다 짧다는 건 너무 당연하다. 문제는 그 기다림의 합이 *전체 처리 시간*이 된다는 점이다.

Vlad는 한 문장으로 이렇게 정리한다. "the maximum throughput of a database system is achieved for a limited number of database connections." 데이터베이스 시스템의 최대 throughput은 *제한된 수*의 커넥션에서 나온다. 무제한 풀은 절대 답이 아니다.

그렇다면 적정값은 어떻게 구할까? 인터넷을 뒤지면 PostgreSQL 위키에 적힌 유명한 공식이 나온다.

```
connections = (core_count * 2) + effective_spindle_count
```

8코어 머신에 SSD를 쓰고 있다면 `(8 * 2) + 1 = 17`쯤이 출발점이다. 이 숫자가 마법의 답은 아니다. 그저 *너무 크게 잡지 말라*는 안전 가이드다. 진짜 적정값은 워크로드마다 다르다. 짧은 OLTP 트랜잭션이 폭주하는 서비스와, 분석성 쿼리가 섞인 서비스의 적정값은 같지 않다. 캐시 적중률, 인덱스 분포, 동시 락 경합 정도가 모두 변수다.

핵심은 이거다. 풀 크기는 *실측을 통해 발견하는 값*이지, *어림짐작으로 키우는 값*이 아니다. 그리고 보통 "그 정도면 충분하다"라고 직감적으로 떠올린 숫자보다 *작다*. 한국의 많은 서비스가 `maximumPoolSize=50` 이상으로 두고 운영하고 있는데, 거기서 30이나 20으로 줄였을 때 응답 시간이 *더 빨라지는* 경험을 한 번이라도 해본 사람이라면 이 말이 무슨 뜻인지 안다.

## 실측 도구로서의 FlexyPool

"실측으로 발견하라"는 말은 듣기에 좋은데, 정작 어떻게 실측하느냐는 또 다른 문제다. 운영 중인 서비스의 풀 크기를 하루는 100, 다음 날은 50, 그다음 날은 20으로 바꿔가며 비교하는 건 사실상 가능하지 않다. 그렇다고 부하 테스트 환경에서 매번 새 값을 손으로 넣어보는 것도 번거롭다.

이 지점에서 Vlad가 직접 만든 오픈소스 도구인 FlexyPool이 등장한다. FlexyPool은 HikariCP, C3P0, DBCP2, Tomcat JDBC, Vibur 같은 기존 풀을 *감싸서* 두 가지를 추가해준다. 하나는 메트릭이고, 다른 하나는 동적 리사이즈다.

메트릭부터 살펴보자. FlexyPool은 다음 같은 값을 히스토그램으로 노출한다.

- **connection acquire time** — `getConnection()`을 호출해서 실제 커넥션을 받기까지 걸린 시간
- **retry count** — acquire 타임아웃이 나서 재시도한 횟수
- **concurrent connections** — 어떤 순간 동시에 얼마나 많은 커넥션이 사용 중이었는지의 분포
- **overflow pool size** — 기본 풀 위에 임시로 더 만들어진 커넥션 수

이 메트릭들 중에서도 가장 결정적인 건 *connection acquire time*이다. 우리가 평소 모니터링하는 "DB 응답 시간"은 사실 DB가 쿼리를 처리한 시간이지, 커넥션을 잡기까지 기다린 시간이 아니다. 그런데 풀이 부족할 때 응답 시간이 튀는 진짜 원인은 후자다. acquire에서 200ms를 기다린 뒤 SQL 실행은 5ms에 끝나도, 사용자가 체감하는 시간은 205ms다. 이 200ms를 *DB 응답 시간*에서 찾으려고 하면 영원히 안 보인다. acquire histogram에서만 보인다.

다음은 동적 리사이즈다. FlexyPool의 핵심 전략 중 하나가 `IncrementPoolOnTimeoutConnectionAcquisitionStrategy`라는 길고 거창한 이름을 가진 녀석이다. 동작은 단순하다. 풀에서 커넥션을 못 받고 타임아웃이 발생할 때마다, 기본 max-size 위에 *임시 buffer*만큼 풀을 키운다. 그 안에서 시스템이 실제로 얼마까지 늘어났는지를 메트릭으로 기록한다.

부하 테스트를 한 번 돌리면 FlexyPool이 알려주는 그래프에서 "아, 이 워크로드는 동시 커넥션 4개에서 처리량이 정점이고, 6개를 넘어서면 더 빨라지지 않는구나"라는 사실이 *눈에 보인다*. 1장의 4개라는 숫자는 누군가의 추측이 아니라, 바로 이 도구가 발견해낸 실측값이었다.

그렇다면 우리가 당장 해야 할 일은 명확하다. 부하 테스트 환경에 FlexyPool을 한 번 끼워보자. HikariCP 위에 얇은 래퍼로 들어가니까 코드 변경은 거의 없다. 한 번만 돌려보면, 우리 서비스의 현재 풀 크기가 *과하게* 잡혀 있는지 아닌지가 보인다. 운영 환경에서도 메트릭만 켜두면 acquire 분포가 계속 쌓인다. p99 acquire time이 10ms를 넘기 시작한다면 풀이 부족하다는 신호고, 평균 acquire time이 거의 0인데 동시 사용 커넥션이 늘 max의 절반에도 못 미친다면 풀이 과하다는 신호다.

FlexyPool 없이도 HikariCP 자체 메트릭(`HikariPool-1.pool.Wait`, `HikariPool-1.pool.Usage`)을 Micrometer로 노출하면 비슷한 분석이 가능하다. 도구 자체가 핵심은 아니다. 핵심은 *acquire time을 지표로 보고 있느냐*다. 보고 있지 않다면, 풀에 관한 우리의 결정은 모두 직감에 기댄 것이다.

## 트랜잭션은 언제 커넥션을 잡는가

풀을 작게 운영하려면 한 가지 전제가 필요하다. 커넥션이 *짧게* 점유되어야 한다는 것이다. 트랜잭션 하나가 1초 동안 커넥션을 들고 있다면, 풀 크기 4로는 초당 4개의 트랜잭션밖에 처리할 수 없다. 트랜잭션 하나가 50ms 만에 커넥션을 놓아준다면, 같은 풀로 초당 80개를 처리할 수 있다. 풀 크기 자체보다 *커넥션 lease time*이 더 중요하다는 사실은 직관에 잘 안 들어오지만, 실제로 그렇다.

여기서 자연스럽게 다음 질문이 나온다. 트랜잭션은 정확히 *언제* 커넥션을 잡을까?

Spring과 Hibernate가 RESOURCE_LOCAL 트랜잭션을 다루는 기본 동작을 따라가보자. `@Transactional`이 붙은 메서드가 시작되는 순간, Spring의 트랜잭션 매니저(`JpaTransactionManager` 또는 `DataSourceTransactionManager`)는 다음 일을 한다.

1. 풀에서 커넥션을 하나 빌린다.
2. 그 커넥션에 `Connection.setAutoCommit(false)`를 호출한다.
3. Hibernate Session(또는 EntityManager)을 그 커넥션에 묶는다.

여기까지가 메서드의 첫 줄이 실행되기 *전*에 일어나는 일이다. 그리고 메서드가 끝날 때까지 이 커넥션을 들고 있는다. 메서드 본문이 외부 HTTP API를 호출하든, 복잡한 자바 계산을 하든, 한참 동안 SQL을 하나도 안 던지든 상관없이, 커넥션은 처음부터 끝까지 자리에 있다.

이게 왜 문제인가. `@Transactional` 메서드 안에서 SQL을 던지기 *전에* 외부 결제사 API를 한 번 호출한다고 해보자. 그 API가 평소 50ms에 답을 주는데 가끔 500ms가 걸린다. 그 500ms 동안 커넥션은 풀에서 빠져나와 *놀고 있다*. 그동안 다른 트랜잭션은 풀이 빌 때까지 기다린다. 풀 크기가 작을수록 이 영향은 즉시 처리량 감소로 나타난다. 외부 호출 한 번이 풀 전체의 acquire 시간을 끌어올리는 그림이라니, 난감한 일이다.

그렇다면 어떻게 해야 할까? 답은 "트랜잭션 메서드 안에서 외부 호출을 하지 말자"는 일반 원칙이기도 하지만, 더 근본적인 답이 있다. *커넥션을 정말 필요한 순간까지 잡지 않는 것*이다. 즉, 트랜잭션이 *논리적으로* 시작되더라도, 실제로 첫 SQL이 나갈 때까지는 커넥션을 빌리지 않게 만드는 것이다.

이 동작을 켜주는 옵션이 바로 `hibernate.connection.provider_disables_autocommit=true`다. 이름이 한참 길지만, 의미는 짧다. "커넥션 provider(=HikariCP)에서 이미 autoCommit을 false로 만들어주니까, Hibernate는 그 작업을 위해 일찍 커넥션을 잡지 않아도 된다." 그리고 풀 쪽에서도 `autoCommit=false`로 설정해야 짝이 맞는다.

Spring Boot 환경에서 설정 예시를 보자.

```yaml
spring:
  datasource:
    hikari:
      auto-commit: false           # 풀에서 빌려주는 커넥션은 이미 autoCommit=false
  jpa:
    properties:
      hibernate:
        connection:
          provider_disables_autocommit: true   # Hibernate는 일찍 잡지 않는다
```

이 두 줄이 같이 켜져 있어야 한다. 하나만 켜져 있으면 동작이 어긋난다. 두 줄이 모두 켜져 있을 때, 트랜잭션 메서드가 시작되어도 Hibernate는 *느긋하게* 기다린다. 첫 SQL이 나갈 때, 그제서야 커넥션을 빌린다. 그 전에 외부 API가 500ms를 잡아먹어도 풀에는 영향이 없다.

수치로 보면 어떨까. 풀 크기 4, 트랜잭션 평균 100ms, 그중 SQL 실행은 30ms이고 나머지 70ms는 자바 로직과 외부 호출이라고 해보자. autoCommit 지연이 *없으면* 한 트랜잭션이 100ms 동안 커넥션을 잡으니까, 풀 4개로는 초당 40 트랜잭션이 한계다. autoCommit 지연이 *있으면* 30ms만 잡으므로 같은 풀로 초당 133 트랜잭션이 가능하다. 같은 하드웨어, 같은 풀 크기, 같은 코드. 단지 설정 두 줄을 켰을 뿐이다.

게다가 이 옵션은 6장에서 다룰 read-write/read-only 라우팅의 필수 전제이기도 하다. `AbstractRoutingDataSource`로 read 트랜잭션을 replica로, write를 primary로 보내는 패턴을 쓰려면, 커넥션이 *너무 일찍* 잡혀버려서는 안 된다. 트랜잭션 시작 시점에는 read-only 플래그가 라우팅에 반영되어야 하기 때문이다. 그런데 autoCommit을 끄려고 *진짜* 커넥션을 일찍 잡아버리면, 라우팅 결정이 이미 끝난 뒤다.

기억해두자. `provider_disables_autocommit=true`는 단순한 미세 튜닝이 아니다. 풀을 작게 운영하기 위한 토대이고, 라우팅 같은 더 큰 설계를 가능하게 하는 전제다. Spring Boot 2.x 이후 새 프로젝트라면 첫 줄부터 켜두는 편이 낫다.

## 같은 SQL을 천 번 던지면 컴파일도 천 번 될까

이제 두 번째 큰 주제로 넘어가보자. 트랜잭션의 lease time을 줄이는 또 다른 축이다. 바로 statement caching이다.

상황 하나를 가정해보자. 게시판 상세 페이지가 있다. 트래픽이 평소 초당 200, 피크에 초당 1,000을 친다. 이 API가 던지는 SQL은 단순하다. `SELECT * FROM post WHERE id = ?`. 파라미터 하나만 바뀐다. 같은 SQL이 하루에 수백만 번 실행된다.

여기서 잠깐 생각해보자. 같은 SQL이 백만 번 실행될 때, 데이터베이스는 그 SQL을 *몇 번 컴파일*하고 있을까?

언뜻 보면 답은 명확하다. PreparedStatement를 쓰니까 한 번만 컴파일되고 나머지 999,999번은 캐시된 plan을 쓰는 거 아닌가? 표준 자바 교과서가 그렇게 가르친다. 그런데 *실제로는* 그렇지 않을 수 있다. 드라이버와 설정에 따라, 그 SQL이 매번 다시 파싱되고, 매번 다시 plan이 만들어지고 있을 수 있다. 그것도 모른 채.

이 사실을 처음 마주하면 정말 찜찜하다. 우리가 당연하다고 믿었던 "PreparedStatement = 한 번 컴파일"이라는 등식이, 사실은 *드라이버 설정에 따라 달라지는 약속*이었다는 걸 알게 된다. 한 줄로 표현하면 이렇다. **PreparedStatement는 자동으로 캐시되지 않는다. 캐시되도록 *시켜야* 한다.**

각 데이터베이스 드라이버가 statement caching을 어떻게 처리하는지 하나씩 살펴보자. PostgreSQL, MySQL, Oracle 순으로 다른데, 셋의 동작 방식이 충분히 다르므로 자기 환경에 맞는 설정을 따로 챙겨야 한다.

### PostgreSQL — pgjdbc의 prepareThreshold

PostgreSQL JDBC 드라이버(pgjdbc)는 흥미로운 절충안을 채택했다. 같은 PreparedStatement가 같은 커넥션에서 *몇 번 실행되어야* 비로소 서버사이드 prepare로 승격할지를 결정하는 임계값이 있다. 그 이름이 `prepareThreshold`이고, 기본값은 5다.

무슨 뜻이냐. `connection.prepareStatement("SELECT * FROM post WHERE id = ?")`를 호출하고, 같은 SQL을 4번까지 execute하는 동안에는 드라이버가 매번 *simple query*로 처리한다. SQL을 그대로 파라미터와 함께 서버에 보내고, 서버는 매번 파싱하고 plan을 만든다. 5번째 실행 때부터 비로소 드라이버가 서버에 "이 SQL을 이름 붙여 prepare해줘"라고 요청한다. 그 뒤로는 prepared name + 파라미터만 보내면 되니까 round-trip 한 번이 줄어들고, 서버는 plan을 재사용한다.

기본값 5가 합리적인 절충안인 것 같지만, 잘 생각해보면 좀 아쉽다. 우리 서비스의 핵심 API가 1초 동안 똑같은 SQL을 100번 던지는데, 그중 첫 4번이 매번 simple query라는 건, 4번의 불필요한 파싱이 일어난다는 뜻이다. 더 결정적으로, 커넥션 풀에서 커넥션을 빌려 쓰는 모델에서는 같은 커넥션이 항상 같은 워크로드를 처리한다는 보장이 없다. 한 트랜잭션이 끝나면 커넥션은 풀로 돌아가고, 다음 트랜잭션이 그 커넥션을 받는다. 같은 SQL이 같은 커넥션에서 5번 실행되기 *전에* 풀에 반납되면, 다음에 받는 트랜잭션은 다시 1번부터 시작한다. 결국 *영원히* server-side prepare로 못 올라가는 경우가 생긴다.

Vlad의 권장은 단순하다. `prepareThreshold=1`로 두자. 처음 한 번 실행되는 순간 바로 server-side prepare로 승격하라는 의미다. round-trip 절약 효과를 처음부터 누리고, plan은 즉시 재사용 대상이 된다.

```
jdbc:postgresql://localhost:5432/mydb?prepareThreshold=1
```

다음은 캐시 크기다. PostgreSQL 드라이버는 커넥션마다 PreparedStatement 핸들을 캐시한다. 너무 작으면 LRU로 밀려나서 자주 쓰는 SQL도 매번 새로 prepare된다. 두 옵션이 있다.

- `preparedStatementCacheQueries` — 캐시할 PreparedStatement 개수. 기본 256.
- `preparedStatementCacheSizeMiB` — 캐시 총 메모리 한도. 기본 5MiB.

기본 256개라는 숫자는 보통은 충분하지만, JPA처럼 한 엔티티에 대해 SELECT/INSERT/UPDATE/DELETE가 다 만들어지고, 거기에 fetch graph 변형까지 더해지는 환경에서는 의외로 빠르게 찬다. 동적 IN 절을 쓰는 쿼리가 파라미터 개수마다 다른 SQL로 풀리는 경우도 마찬가지다. 운영 중 캐시 미스가 잦다면 `preparedStatementCacheQueries=512` 정도로 키워볼 만하다. 메모리 한도도 함께 키워야 한다.

```
jdbc:postgresql://localhost:5432/mydb?prepareThreshold=1&preparedStatementCacheQueries=512&preparedStatementCacheSizeMiB=10
```

PostgreSQL wire protocol에 익숙하지 않은 독자를 위해 한 문장만 덧붙이자. PostgreSQL은 V3 protocol에서 *extended query*를 지원한다. extended query는 Parse-Bind-Execute의 3-phase로 구성되는데, Parse가 서버에 이름 붙은 prepare를 만드는 단계다. 이름이 한 번 만들어지면 그 커넥션에서 살아 있는 동안 Bind-Execute만으로 재실행이 가능하다. simple query는 이 분리가 없는 한 줄 발화다. `prepareThreshold`가 가르는 건 바로 simple query와 extended query 사이의 경계다.

`plan_cache_mode`라는 서버 측 설정도 함께 알아두면 좋다. PostgreSQL은 prepared plan을 두 가지 모드로 운영한다. generic plan(파라미터에 무관한 일반 plan)과 custom plan(파라미터를 보고 다시 짠 plan)이다. 기본은 5번까지는 custom plan을 쓰다가 6번째부터 generic으로 고정한다. 그런데 데이터 분포가 편향된 컬럼에서 이 generic plan이 *나쁜 plan*으로 굳어버리는 사고가 종종 일어난다. 그럴 때 `plan_cache_mode=force_custom_plan`으로 두면 매번 custom plan을 강제할 수 있다. 파싱 비용은 더 들지만 plan 품질이 안정된다. 동적 SQL이 많고 데이터 편향이 심한 분석성 워크로드에서 한 번씩 만나는 옵션이다.

### MySQL — connector-j의 두 갈래 캐시

MySQL은 PostgreSQL과 출발점부터 다르다. MySQL의 mysql-connector-j는 기본적으로 *client-side prepare*를 한다. 무슨 뜻이냐. `connection.prepareStatement(sql)`를 부르면, 드라이버가 그 SQL을 클라이언트 쪽에서 파싱하고, 실제 execute 시점에는 파라미터를 inlining한 *완전한 SQL*을 서버에 한 번에 보낸다. round-trip이 하나뿐이다. 서버 쪽에는 prepare라는 개념이 안 도착한다.

처음 들으면 이상하다. PreparedStatement를 쓰는 이유가 서버 쪽 plan 재사용 아니었나? 그런데 MySQL의 plan optimizer는 historically *상대적으로 가볍다*. 단순 OLTP 쿼리에서 파싱 비용이 큰 plan을 재사용하는 이득보다, round-trip을 하나로 줄이고 서버에 상태(prepare 핸들)를 안 남기는 이득이 더 크다는 게 mysql-connector-j의 기본 입장이다.

그래서 MySQL의 statement caching은 두 갈래로 갈린다.

첫째, **client-side cache**다. 드라이버가 같은 SQL의 ParseInfo(파싱 결과 + 파라미터 위치 정보)를 캐시한다. 같은 SQL이 다시 들어오면 파싱을 건너뛰고 캐시된 ParseInfo로 파라미터만 채워 서버에 보낸다. 이걸 켜는 옵션이 `cachePrepStmts=true`이고, 기본은 `false`다. 즉, 켜지 않으면 같은 SQL을 백만 번 던져도 *드라이버 쪽에서* 매번 파싱한다. 켜야 한다.

두 번째, **server-side prepare**다. 옵션 `useServerPrepStmts=true`로 켜면 동작 모드가 바뀐다. 드라이버가 서버에 prepare를 보내고, execute는 별도로 보낸다. PostgreSQL의 extended query와 비슷한 모델이 된다. round-trip은 두 번이 되지만, 서버 plan 재사용 + 바이너리 protocol(파라미터 직렬화가 더 작다)의 이득이 있다.

Vlad가 권장하는 조합은 의외다. **`useServerPrepStmts=false`로 두고, `cachePrepStmts=true`만 켠다.** 즉 client-side 캐시는 켜되, server-side prepare는 켜지 않는다. 이유는 단순하다. MySQL 8.0.22 기준 Vlad의 벤치에서, throughput과 p99 모두 client-side가 server-side를 앞섰기 때문이다. round-trip 두 번의 비용이 plan 재사용의 이득을 넘어선다는 결론이다.

게다가 client-side 캐시는 크기 설정이 매우 중요하다. 두 옵션이 있다.

- `prepStmtCacheSize` — 캐시할 prepared statement 개수. 기본 **25**.
- `prepStmtCacheSqlLimit` — 캐시할 SQL의 최대 길이(글자 수). 기본 **256**.

기본 25는 정말 작다. 어떤 서비스도 PreparedStatement 25개로는 부족하다. 기본 256자도 작다. JPA가 만드는 SELECT 쿼리는 컬럼 수가 많아지면 금세 1,000자를 넘긴다. 256자 제한에 걸리면 그 SQL은 *영원히* 캐시되지 않는다.

Vlad의 권장값에 살을 붙이면 이 정도가 적정선이다.

```
jdbc:mysql://localhost:3306/mydb?useServerPrepStmts=false&cachePrepStmts=true&prepStmtCacheSize=500&prepStmtCacheSqlLimit=2048
```

500개, 2048자. 메모리 부담은 무시할 만한 수준이지만, 캐시 적중률은 비교할 수 없을 정도로 올라간다. JPA를 쓰는 서비스에서는 250 정도로 두는 합의가 한국 커뮤니티에서도 자주 보이는데, 적어도 500까지는 키워두는 편이 낫다. 안 켜진 채로 운영하다가 어느 날 acquire time이 튀는 패턴이 보이기 시작하면, 그제서야 이 설정을 찾아 헤매게 된다. 그 시점에는 이미 늦었다.

한 가지 더. MySQL 환경에서 자주 함께 보는 옵션이 `rewriteBatchedStatements=true`다. 이건 statement caching 자체와는 다른 주제로, 9장의 배치 INSERT 단원에서 자세히 다룬다. 다만 statement 캐시 옵션을 손볼 때 함께 챙기는 자리라고 기억해두자.

### Oracle — defaultRowPrefetch와 statement cache

Oracle JDBC 드라이버(ojdbc)는 또 다른 양상이다. Oracle은 plan 재사용에 가장 적극적인 DB이고, ojdbc도 거기에 맞춰 *기본적으로* statement cache를 켤 수 있게 되어 있다. 다만 추가로 챙겨야 할 옵션이 두 가지 있다.

첫째, **statement cache** 자체다. ojdbc의 implicit statement cache를 켜려면 데이터소스 쪽 옵션으로 `OracleDataSource.setImplicitCachingEnabled(true)`를 호출하고, 캐시 크기를 `setStatementCacheSize(int)`로 잡는다. 기본은 켜져 있지 않다. 켜지 않으면 PreparedStatement를 닫을 때 실제로 닫혀버려서 다음 호출에서 또 prepare해야 한다.

```java
OracleDataSource ds = new OracleDataSource();
ds.setURL("jdbc:oracle:thin:@//host:1521/orcl");
ds.setImplicitCachingEnabled(true);
ds.setStatementCacheSize(500);
```

HikariCP를 쓴다면 `dataSourceProperties`로 같은 설정을 전달할 수 있다.

```yaml
spring:
  datasource:
    hikari:
      data-source-properties:
        oracle.jdbc.implicitStatementCacheSize: 500
```

둘째, **defaultRowPrefetch**다. Oracle 드라이버는 ResultSet을 읽을 때 *몇 줄씩 미리 가져올지*를 결정하는 prefetch 크기를 가진다. 기본값은 **10**이다. 의미는 단순하다. SELECT 결과가 1,000 row인 쿼리를 실행했을 때, 드라이버는 처음에 10 row만 가져온다. 그 10 row를 다 소비하면 다음 10 row를 가져오기 위해 *서버에 또 다녀온다*. 1,000 row를 다 가져오려면 round-trip이 100번이다.

이 기본값은 *작아도 너무 작다*. JDBC가 만들어진 시점에는 메모리가 부족한 클라이언트가 흔했기 때문에 안전하게 잡았지만, 지금 환경에 맞지 않는다. 단순히 키우기만 해도 큰 ResultSet 쿼리의 응답 시간이 극적으로 줄어든다.

키우는 방법은 두 가지다. JDBC 레벨에서는 `OracleStatement.setRowPrefetch(int)`로 statement마다 잡을 수 있고, 드라이버 레벨에서는 `oracle.jdbc.defaultRowPrefetch` 시스템 프로퍼티로 잡을 수 있다. Hibernate를 쓰는 환경에서는 더 간단하다. 다음 한 줄을 application.yml에 추가하면 된다.

```yaml
spring:
  jpa:
    properties:
      hibernate:
        jdbc:
          fetch_size: 100
```

Hibernate는 모든 PreparedStatement의 fetch size를 이 값으로 잡는다. Oracle만이 아니라 어느 DB든 적용된다. 권장값은 워크로드에 따라 100~500이다. 너무 크게 잡으면 한 번에 너무 많은 메모리를 잡으므로 균형이 필요하다. 분석성 쿼리가 많은 환경이라면 500까지, OLTP 위주라면 100쯤이 보통의 출발점이다.

### 세 DB를 한 그림으로

세 드라이버를 표로 정리해보자.

| DB / 드라이버 | 핵심 옵션 | 권장값 | 의미 |
|---------------|-----------|--------|------|
| PostgreSQL / pgjdbc | `prepareThreshold` | 1 | 첫 실행부터 server-side prepare |
| | `preparedStatementCacheQueries` | 512 | 캐시 슬롯 수 (기본 256) |
| | `preparedStatementCacheSizeMiB` | 10 | 캐시 메모리 (기본 5) |
| MySQL / connector-j | `useServerPrepStmts` | false | client-side prepare 유지 |
| | `cachePrepStmts` | true | ParseInfo 캐시 켬 |
| | `prepStmtCacheSize` | 500 | 캐시 슬롯 수 (기본 25) |
| | `prepStmtCacheSqlLimit` | 2048 | SQL 길이 한도 (기본 256) |
| Oracle / ojdbc | `implicitStatementCacheSize` | 500 | implicit cache 크기 |
| | `defaultRowPrefetch` (또는 `hibernate.jdbc.fetch_size`) | 100~500 | ResultSet fetch 단위 |

이 표를 보고도 이상한 점이 있다. 왜 세 DB의 권장값이 이렇게 제각각인가. PostgreSQL은 server-side prepare를 켜라고 하고, MySQL은 *끄라*고 한다. 두 DB에서 같은 모델을 쓰면 좋지 않을까?

그렇다면 한 가지를 기억해두자. JDBC는 표준 *인터페이스*지만, 그 뒤의 드라이버는 *벤더 구현*이다. 표준 인터페이스의 같은 메서드 호출이 드라이버마다 다른 wire protocol로 풀린다. PostgreSQL의 server-side prepare는 round-trip 절약 + 서버 plan 재사용이 한 묶음이지만, MySQL의 server-side prepare는 round-trip 두 번 + 바이너리 protocol이라는 다른 묶음이다. 비용-이득 균형이 다르므로 답도 다르다.

여기서 우리는 한 가지 더 큰 교훈을 얻는다. *"JDBC 옵션"은 데이터베이스마다 따로 챙겨야 한다.* 하나의 application.yml에 PostgreSQL과 MySQL을 동시에 지원한다면, JDBC URL을 환경마다 분리해야 한다. 그 분리를 안 해두면, 한쪽 환경에서 켜둔 옵션이 다른 환경에서 무시되거나 잘못된 동작을 한다.

## 측정하지 않은 캐시는 켜진 것이 아니다

statement cache를 켰다고 끝일까? 아니다. 켰는데 *실제로 동작하고 있는지*를 확인할 줄 알아야 한다. 옵션을 application.yml에 적었는데, JDBC URL에 안 박혀 있어서 정작 드라이버에는 안 닿고 있는 경우를 너무 자주 본다. 이런 상황은 정말 끔찍하다. 우리는 켰다고 믿고 그 위에서 다른 결정을 쌓아 가는데, 실제로는 켜진 적이 없다.

PostgreSQL에서 가장 간단한 확인 방법은 서버 로그를 켜는 것이다. `log_statement = 'all'`로 두면, simple query인지 extended query인지가 그대로 보인다. extended query는 `LOG: execute <unnamed>: SELECT ...` 형태로 prepared name이 함께 찍힌다. 이 로그가 보이면 server-side prepare가 도는 중이다. 안 보이면 안 도는 중이다.

또 다른 방법은 `pg_prepared_statements` 뷰를 조회하는 것이다. 한 커넥션에 어떤 prepared statement가 살아 있는지 보여준다.

```sql
SELECT name, statement, prepare_time FROM pg_prepared_statements;
```

이게 비어 있다면 그 커넥션에서 server-side prepare가 한 번도 일어나지 않은 것이다.

MySQL에서는 `SHOW SESSION STATUS LIKE 'Com_stmt_%'`로 prepare 카운터를 볼 수 있다. server-side prepare를 켰다면 `Com_stmt_prepare`가 올라간다. 끈 상태에서는 0이다. client-side 캐시 적중 여부는 직접 카운터로 나오지는 않지만, MySQL의 *general log*를 켜서 같은 SQL이 매번 다시 들어오는지를 확인할 수 있다.

이 확인 절차를 처음 한 번이라도 해본 사람과 그렇지 않은 사람의 차이는 크다. *"옵션을 켰다"*와 *"옵션이 실제로 동작 중인 걸 확인했다"*는 다르다. 측정 없이 켜놓기만 한 캐시는 켜진 것이 아니다.

## StatementInspector — 모든 SQL을 가로채는 자리

Hibernate는 statement cache 자체에 대해서는 드라이버에 위임한다. 다만 *모든 SQL을 가로챌 수 있는 후크*를 하나 제공한다. `StatementInspector`다. 옵션 한 줄로 켠다.

```yaml
spring:
  jpa:
    properties:
      hibernate:
        session_factory:
          statement_inspector: com.example.MyStatementInspector
```

`StatementInspector`는 단순한 인터페이스다.

```java
public interface StatementInspector {
    String inspect(String sql);
}
```

Hibernate가 SQL을 만들어 JDBC에 보내기 *직전에* 이 `inspect()` 메서드를 부른다. 반환값이 *최종 SQL*이 된다. 즉 여기서 SQL을 *수정*할 수 있다. 한 줄 추가하기, 주석 박기, 힌트 넣기 같은 일이 가능하다.

활용은 크게 세 갈래다.

첫째, **로깅과 감사**다. 모든 SQL을 별도 스토리지에 적재하거나, 특정 패턴의 SQL이 나갈 때 경고를 띄울 수 있다. 일반 SQL 로깅은 너무 양이 많아서 운영에서 켜기 어려운데, StatementInspector로 *선별적*으로 잡으면 부담이 적다.

```java
public class AuditingStatementInspector implements StatementInspector {
    @Override
    public String inspect(String sql) {
        if (sql.contains("DELETE FROM payment")) {
            auditLogger.warn("Payment delete: {}", sql);
        }
        return sql;
    }
}
```

둘째, **강제 hint 삽입**이다. Oracle이나 PostgreSQL에서 특정 쿼리에 인덱스 힌트나 plan 힌트를 *전역적으로* 박아야 할 때 쓴다. 코드 한 줄 한 줄 native query로 풀어내지 않고, inspector가 패턴 매칭으로 주입한다.

셋째, 가장 강력한 용법인 **멀티테넌시 강제 주입**이다. 멀티테넌트 SaaS에서 모든 SQL에 `tenant_id = ?` 조건을 *반드시* 넣어야 한다고 해보자. 개발자가 깜빡하면 보안 사고가 나는 종류의 요구다. StatementInspector로 SQL을 가로채서 WHERE 절을 검사하고, 누락된 경우 강제로 주입하거나 예외를 던질 수 있다. 자세한 패턴은 12장의 multi-tenancy 단원에서 다시 풀어내자.

지금 단계에서 기억해둘 건 하나다. *Hibernate가 만들어내는 모든 SQL을 한 자리에서 가로챌 수 있다.* 이 자리는 audit, hint, tenancy, 디버깅 어디에든 쓸 수 있는 다용도 후크다. 알아두면 손에 든 도구 하나가 늘어난다.

## 다 더하면 무엇이 보이는가

이 챕터에서 다룬 것들을 *한 트랜잭션의 일생*이라는 그림에 다시 얹어보자.

서비스 메서드가 호출된다. `@Transactional`이 트랜잭션을 연다. 여기서 `provider_disables_autocommit=true`가 켜져 있다면, 아직 커넥션은 안 잡힌다. 메서드가 자바 로직을 돌리고, 외부 API를 한 번 호출한다. 그동안 풀의 커넥션은 다른 트랜잭션이 쓰고 있다.

비로소 첫 SQL이 나간다. 이제 풀에서 커넥션을 빌린다. HikariCP는 풀에 여유가 있다면 즉시(보통 마이크로초 단위) 커넥션을 돌려준다. FlexyPool 메트릭이 켜져 있다면 이 acquire 시간이 히스토그램에 한 줄로 기록된다.

JDBC가 SQL을 받는다. PostgreSQL이라면 `prepareThreshold=1`이 켜져 있으니 즉시 server-side prepare로 풀려 round-trip 한 번이 줄어든다. 같은 SQL이 같은 커넥션에서 이전에 한 번이라도 prepare된 적이 있다면, 캐시 적중으로 그마저도 생략된다. MySQL이라면 `cachePrepStmts=true` 덕분에 client-side ParseInfo가 캐시에서 꺼내져 파싱이 생략된다. Oracle이라면 implicit statement cache가 적중하면서 prepared handle이 재사용된다.

서버가 결과를 돌려준다. Oracle에서는 `defaultRowPrefetch` 또는 `hibernate.jdbc.fetch_size`가 키워져 있어 한 번에 100 row가 도착한다. 작은 ResultSet이라면 한 번의 round-trip으로 끝난다.

Hibernate가 그 결과를 ResultSet에서 읽어 PersistenceContext에 채운다. StatementInspector가 켜져 있다면 SQL은 발송 전에 이미 inspect를 거쳤다 — audit 로그가 어딘가에 쌓이고, 멀티테넌시 강제 조건이 들어가 있다.

트랜잭션이 commit된다. 커넥션이 풀로 돌아간다. 전체 lease time은 30ms. 풀 크기 4로도 초당 백 개 단위의 트랜잭션을 받아낼 수 있는 구성이다.

이 그림에서 가장 중요한 건, *위 한 줄 한 줄이 모두 우리 설정 한 줄에 달려 있다*는 점이다. `provider_disables_autocommit=true`가 빠지면 첫 줄부터 무너진다. JDBC URL에 prepareThreshold나 cachePrepStmts가 안 박혀 있으면 두 번째 줄이 무너진다. fetch_size를 키우지 않으면 Oracle의 큰 ResultSet 한 줄이 무너진다. 설정 한 줄이 *그날 밤 운영 알람의 빈도*를 좌우한다.

## 이 챕터는 끝내지 않는다 — 다음 장으로

여기까지 오면서 우리는 한 트랜잭션이 시작부터 끝까지 어떻게 흘러가는지의 *토대*를 다 봤다. 풀에서 커넥션을 빌리는 시점, autoCommit 처리, statement cache 적중, StatementInspector를 통한 SQL 가로채기. 이 토대 위에서 다음 장부터는 *엔티티가 그 SQL을 어떻게 만들어내는지*를 본다.

3장에서 우리는 식별자 전략과 equals/hashCode 같은 엔티티 설계 결정이 *어떻게 SQL을 바꾸는가*를 다룬다. 같은 도메인을 표현하는 두 엔티티가 있는데 한쪽은 배치가 묶이고 다른 쪽은 한 줄씩 INSERT가 나가는 사례를 풀어낸다. 거기서 또 한 번 우리는 "ORM이 자동으로 해주는 줄 알았는데 실은 우리가 안 시키면 안 해주더라"는 경험을 마주하게 된다.

statement cache는 이 챕터의 끝이 아니다. 이 챕터에서 시작된 *"라운드트립을 줄인다"*는 흐름은 4장(N+1)에서 fetch 시점으로, 9장(배치)에서 write 시점으로, 10장(페이지네이션)에서 read 시점으로 차례로 풀려나간다. 1장에서 던진 북극성 — *라운드트립과 트랜잭션 동작* — 의 첫 번째 큰 가지가 이제 막 자라기 시작한 셈이다.

기억해두자. 풀은 *작게* 가는 편이 낫다. 작게 가려면 lease time이 *짧아야* 한다. lease time이 짧으려면 커넥션을 *늦게* 잡고, statement cache가 *적중*해야 한다. 이 세 가지가 한 묶음이다. 한 줄이 빠지면 나머지도 흔들린다. 운영 환경의 응답 시간 그래프가 어느 날 갑자기 튀기 시작한다면, 가장 먼저 들춰볼 곳은 이 세 줄이다.

## 내 코드 체크리스트 3개

이제 자기 IDE를 열고 30초 만에 확인할 수 있는 세 가지를 두자.

1. **우리 PostgreSQL/MySQL JDBC URL에 statement cache 옵션이 명시되어 있는가?**
   PostgreSQL이라면 `prepareThreshold=1`과 `preparedStatementCacheQueries` 둘 다 박혀 있는지, MySQL이라면 `cachePrepStmts=true`와 `prepStmtCacheSize=500` 이상이 박혀 있는지. URL에 없다면 켜져 있지 않다.

2. **`hibernate.connection.provider_disables_autocommit=true`가 켜져 있는가? 그리고 HikariCP의 `auto-commit: false`도 함께 켜져 있는가?**
   하나만 켜져 있으면 의미가 없다. 두 줄이 함께 있어야 트랜잭션이 첫 SQL이 나갈 때 커넥션을 잡는다.

3. **connection acquire time을 지표로 보고 있는가?**
   FlexyPool의 histogram이든, HikariCP 자체 Micrometer 메트릭(`hikaricp.connections.acquire`)이든, p99 acquire time이 대시보드 한 자리를 차지하고 있는지. 안 보고 있다면, 풀 크기에 대한 우리의 모든 결정은 직감에 기댄 것이다.

세 줄이 모두 통과한다면, 적어도 JDBC 토대에서는 더 들여다볼 거리가 많지 않다. 한 줄이라도 막힌다면, 거기서부터 시작해보자. 다음 장에서 만나는 *엔티티 설계*는 이 토대 위에서만 의미가 있다.
