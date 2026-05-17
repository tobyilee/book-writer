# 3장. 엔티티를 잘 빚는다는 것 — 식별자, equals, 그리고 bytecode enhancement

같은 도메인을 둘이 짰는데 결과가 다르다고 해보자. 한쪽은 `saveAll(1만 건)`을 호출하면 INSERT 한 묶음에 25건씩 깔끔하게 묶여 나간다. 다른 한쪽은 같은 코드, 같은 라이브러리, 같은 데이터베이스인데 1만 건이 한 줄씩 1만 번 나간다. `batch_size=25`도 설정파일에 떡하니 적혀 있다. 그런데도 묶이지 않는다. 어느 쪽이 더 답답할까. 아마 두 번째 쪽일 것이다. *분명히 켰는데 안 켜진* 상황이기 때문이다.

비슷한 일은 또 일어난다. `fetch = FetchType.LAZY`를 모든 연관관계에 꼼꼼히 박았다. 그런데 SQL 로그를 켜 보면 `@ManyToOne` 마다 추가 SELECT가 따라 나간다. *분명히 LAZY로 적었는데 LAZY가 아니다*. 이쯤 되면 누구나 한 번쯤 화면 앞에서 멍해진다.

왜 이런 일이 벌어질까. 답은 엔티티를 빚어내는 *첫 단계*에 있다. 엔티티 클래스에 어떤 어노테이션을 붙였는지, `equals`와 `hashCode`를 어떻게 짰는지, 컬렉션을 어떤 타입으로 선언했는지 — 이 작은 결정 하나하나가 Hibernate가 만들어내는 SQL과 메모리 사용 패턴을 직접 결정한다. 코드 리뷰에서는 한 줄짜리 변경처럼 보이는 것이 운영에서는 한 자릿수의 throughput 차이로 돌아온다.

그러니 이번 장에서는 엔티티를 *잘 빚는* 일에 집중해보자. 식별자 전략부터 equals/hashCode, 컬렉션 매핑, 상속 매핑, 그리고 마지막으로 bytecode enhancement까지. 다섯 가지 결정이 운영의 SQL을 어떻게 바꾸는지를 하나씩 따라가 본다.

---

## 식별자가 모든 것을 결정한다 — IDENTITY는 왜 배치를 죽이는가

엔티티를 처음 만들 때 가장 먼저 손이 가는 자리는 `@Id`이다. 그런데 그 옆에 무심코 적어 두는 `@GeneratedValue(strategy = ...)` 한 줄이, 사실은 운영의 batch INSERT 성능을 결정짓는 가장 큰 분기점이다.

상황을 가정해보자. 신규 회원 가입 이벤트가 몰리는 시점이다. 한 트랜잭션 안에서 `Member`, `Profile`, `AuthLog`, `WelcomeCoupon` 네 개의 엔티티를 함께 저장한다. `hibernate.jdbc.batch_size=25` 도 켜두었고, `order_inserts=true`도 켰다. 그런데 SQL 로그를 보면 INSERT가 한 줄씩 나간다. 묶이지 않는다.

왜 그럴까. 모든 엔티티가 `@GeneratedValue(strategy = GenerationType.IDENTITY)`로 선언돼 있기 때문이다.

### IDENTITY가 batch를 죽이는 메커니즘

이 동작을 한 문장으로 줄이면 이렇다. **`IDENTITY` 전략은 INSERT가 실행돼야 PK가 정해지기 때문에, Hibernate가 write-behind를 포기한다.** 풀어 쓰면 이렇다.

JPA의 핵심은 *flush를 미루는 것*이다. `persist()`를 호출한다고 즉시 INSERT가 나가지 않는다. 트랜잭션이 커밋되거나, JPQL을 실행하기 직전, 또는 `flush()`를 명시적으로 부를 때 일괄로 INSERT가 모인다. 이것이 write-behind이다. 한 번에 25개씩 묶어 INSERT를 날리려면, 적어도 `persist()` 시점에 *모든 엔티티의 상태가 완결*돼야 한다. PK까지 포함해서 말이다.

그런데 `IDENTITY`는 어떤가. PK가 데이터베이스의 auto-increment에 의해 *INSERT 직후에* 정해진다. 그러니까 Hibernate는 `entityManager.persist(post)`가 호출된 순간, 그 자리에서 즉시 INSERT를 발행해야 한다. PK를 받아와야 영속 컨텍스트에 등록할 수 있기 때문이다. 결과적으로 5건을 `persist`하면 5번 INSERT가 나간다. 묶일 자리가 없다.

Vlad Mihalcea는 이 동작을 자신의 블로그에서 단호하게 정리해두었다. *"IDENTITY와 batch INSERT는 함께 갈 수 없다. 5건을 persist하면 5번의 round trip이 발생한다."* 운영을 해 본 사람은 이 한 줄의 무게를 안다. round trip 5번과 1번은 평균 응답시간 차이는 적어 보여도, 동시 트랜잭션 수가 늘어나면 누적 지연이 폭발적으로 벌어진다.

이 결론은 9장의 정식 배치 처리 단원에서 다시 깊이 회수한다. 지금 단계에서 기억해 둘 것은 이 한 줄이다. **IDENTITY는 배치를 죽인다.** 도메인 모델을 처음 빚을 때부터 이 사실을 깔고 가자.

### SEQUENCE — 정석은 pooled-lo

그렇다면 어떻게 해야 할까. PostgreSQL, Oracle, H2, SQL Server 2012 이상, MariaDB 10.3 이상을 쓰고 있다면 답은 분명하다. **`GenerationType.SEQUENCE` + pooled-lo optimizer**이다.

```java
@Id
@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "post_seq")
@SequenceGenerator(
    name = "post_seq",
    sequenceName = "post_sequence",
    allocationSize = 50    // pooled-lo의 핵심
)
private Long id;
```

SEQUENCE 전략이 좋은 이유는 두 가지다.

첫째, PK를 INSERT 전에 미리 받아올 수 있다. Hibernate는 `persist()` 시점에 sequence에서 ID를 한 개 뽑아 엔티티에 박는다. 그러면 batch INSERT가 그대로 가능해진다. 25건이 묶여 한 round trip에 나간다.

둘째, `allocationSize`를 늘리면 *sequence 호출 자체*가 줄어든다. `allocationSize=50`이면 Hibernate는 sequence를 한 번 호출해 50개의 PK를 application 메모리에서 분배한다. INSERT 50건마다 sequence call 한 번이다. 호출 비용도 round trip도 모두 줄어든다.

이 `allocationSize` 동작을 지원하는 알고리즘이 *pooled-lo optimizer*이다. Hibernate는 sequence의 *현재값*과 *그다음 값*의 사이를 application이 채워서 쓴다. 동시에 여러 인스턴스가 떠 있어도 sequence의 트랜잭션 안전성 덕분에 겹침이 없다. 운영 관점에서는 *번호가 듬성듬성 비어 있어도 괜찮다는 합의* 하나만 있으면 된다. PK가 1, 2, 3, ...이 아니라 51, 52, ..., 101, 102, ...로 점프하는 일이 생긴다. 이는 *정상*이다.

DB가 SEQUENCE를 지원하면, 식별자 전략의 디폴트는 이것으로 잡자. 그게 정석이다.

### TABLE — SELECT FOR UPDATE로 비싸다

세 번째 선택지는 `GenerationType.TABLE`이다. 이름 그대로 *별도 테이블에 ID 카운터를 저장*하고, 새 ID가 필요할 때마다 그 행에 `SELECT … FOR UPDATE`로 잠금을 걸어 카운터를 증가시킨다.

여기서 멈칫해야 한다. `SELECT FOR UPDATE`라는 단어가 들어가는 순간, 이 전략은 *row-level lock*을 매번 잡는다는 뜻이다. 동시 INSERT가 늘어나면 어떤 일이 벌어질까. 모든 인스턴스가 같은 행 위에서 잠금 경쟁을 한다. lock 대기열이 길어진다.

Vlad는 이렇게 적었다. *"the row-level locking is definitely less efficient than using a native IDENTITY or SEQUENCE."* TABLE 전략은 DB가 sequence도, identity도 지원하지 않는 *역사적 호환성*을 위해 남아 있는 자리이다. 새 프로젝트에서 굳이 고를 이유는 거의 없다.

### AUTO — DB별 지뢰

마지막은 `GenerationType.AUTO`이다. 가장 무난해 보이는 이름이지만, 실은 가장 위험하다. *DB에 따라 다른 전략으로 떨어지기* 때문이다.

- PostgreSQL이면 SEQUENCE
- MySQL pre-10.3이면 *TABLE*로 떨어진다
- Oracle이면 SEQUENCE
- H2면 SEQUENCE

MySQL을 쓰는데 `AUTO`를 적었다고 해보자. 어느 날 운영에서 INSERT가 느려지기 시작한다. 들여다보니 ID 발급용 별도 테이블에 `SELECT FOR UPDATE`가 계속 걸리고 있다. 누가 시켰는가. 아무도. AUTO가 골라준 것이다. *지뢰*라는 표현이 결코 과장이 아니다.

도메인 모델을 짤 때는 `AUTO`를 피하고 *전략을 명시적으로 적어두는 편이 낫다*. 의도가 코드에 박혀 있어야 6개월 뒤에 다른 사람이 봤을 때도 흔들리지 않는다.

### 식별자 전략 비교 — 한 장으로

위 내용을 표 한 장에 모아 보자.

| 전략 | JDBC batch INSERT | 권장 자리 |
|------|-------------------|-----------|
| `IDENTITY` | **불가능** — INSERT 직후 PK 발급 | MySQL을 쓰며 batch 부담이 없는 도메인. 어쩔 수 없는 곳에서만 |
| `SEQUENCE` + pooled-lo | 가능 — INSERT 전에 PK 확보, sequence 호출도 분할상환 | DB가 sequence를 지원하면 *정석* |
| `TABLE` | 가능하지만 비싸다 — `SELECT … FOR UPDATE`로 행 잠금 | 거의 쓰지 말자 |
| `AUTO` | DB에 따라 다름 — MySQL pre-10.3은 TABLE로 떨어짐 | 절대 명시적으로 고르지 말자 |

### MySQL이라는 현실 — SEQUENCE가 없을 때

여기서 한 가지 난감한 현실이 등장한다. **MySQL에는 SEQUENCE가 없다.** 8.x 기준으로 여전히 없다. MariaDB는 10.3부터 sequence 객체를 정식 지원하지만, MySQL 본가는 그렇지 않다.

그럼 MySQL 위에서 batch INSERT를 어떻게 묶을까. 두 가지 우회로가 있다.

첫째, **수동 ID 할당**이다. Hibernate에 PK 발급을 위임하지 않고, application이 직접 ID를 만들어 박는다. UUID v7 같은 시간 기반 UUID를 쓰거나, Twitter snowflake 같은 분산 ID 발급기를 쓴다. Hibernate가 보기에는 PK가 이미 박혀 있으니 `IDENTITY`처럼 INSERT 후 PK를 받아올 필요가 없다. batch가 그대로 묶인다.

둘째, **`StatelessSession`** 우회이다. Hibernate가 제공하는 *영속 컨텍스트 없는 세션*이다. dirty checking도, 1차 캐시도, cascade도 없는 *얇은 세션*. 6.3 이후로는 batch INSERT와 UPSERT까지 지원해 진정한 high-volume ingest 도구로 부활했다. ID 발급은 우회로지만, 그 위에서 직접 batch INSERT를 묶는 패턴이 익숙해지면 운영에서 잘 통한다.

이 두 가지는 9장의 정식 batch 단원에서 코드까지 풀어 본다. 지금은 *MySQL 환경에서는 디폴트 IDENTITY로 가다가 batch 부담이 생기면 우회로가 있다*는 사실만 머리에 박아두자.

### 첫 번째 체크리스트

여기까지 왔으면, 자기 코드의 핵심 엔티티 다섯 개를 떠올려 보자.

- 그 다섯 개의 `@Id` 전략이 무엇인가.
- 그게 *의도된 선택*인가, 아니면 IDE 자동완성으로 채워진 결과인가.
- batch INSERT가 묶일 자리가 있는 도메인에 `IDENTITY`를 박아두지 않았는가.
- MySQL을 쓰는데 `AUTO`를 적어 두지 않았는가.

이 네 줄이 명확하지 않은 엔티티가 있다면, 그 엔티티는 *다시 빚어야 할* 후보이다.

---

## 상속을 매핑하는 네 가지 길

식별자 다음으로 자주 만나는 결정은 *상속을 어떻게 풀 것인가*이다. JPA는 네 가지 길을 열어두었다. `SINGLE_TABLE`, `JOINED`, `TABLE_PER_CLASS`, 그리고 `@MappedSuperclass`. 이름은 비슷하지만 만들어내는 SQL의 모양은 전혀 다르다.

상황을 가정해보자. `Payment`라는 추상 엔티티가 있고 `CardPayment`, `BankTransfer`, `MobilePayment` 세 하위 클래스가 있다. 가장 자주 부르는 query는 *어떤 사용자의 최근 결제 10건*이다. 폴리모픽하게 모든 결제 유형을 한 번에 가져온다. 이 도메인에 어떤 전략이 어울릴까.

### SINGLE_TABLE — 디폴트, 가장 빠르다

`@Inheritance(strategy = InheritanceType.SINGLE_TABLE)`은 모든 하위 클래스를 *한 테이블에* 담는다. 자식별 컬럼이 모두 한 테이블에 펼쳐지고, `dtype` 같은 *discriminator 컬럼*이 한 줄의 정체를 알려준다.

장점은 *읽기·쓰기 모두 가장 빠르다*는 점이다. JOIN이 없다. 폴리모픽 query는 그저 `SELECT * FROM payment WHERE user_id = ? ORDER BY created_at DESC LIMIT 10` 한 줄이다. 인덱스도 한 테이블에만 걸면 된다.

단점이 있다. 자식 필드에 `NOT NULL` 제약을 걸기 어렵다. 한 테이블에 모든 자식의 컬럼이 펼쳐져 있으니, *카드 결제용 컬럼*은 *계좌 이체 row*에서는 비어 있어야 한다. DB 차원의 무결성을 강제하려면 `CHECK` 제약을 별도로 만들거나 application-level 검증에 맡겨야 한다.

운영의 관점에서 보면, 이 단점은 *대부분 감내할 수 있는 비용*이다. throughput이 우선이라면 `SINGLE_TABLE`을 디폴트로 잡자. 권고 #8도 이를 명시한다 — *상속은 `SINGLE_TABLE`을 디폴트로, 무결성이 결정적으로 중요한 경우에만 `JOINED`*.

### JOINED — 무결성용

`JOINED`는 부모 테이블과 자식 테이블을 각각 두고, 자식 row를 fetch할 때마다 JOIN으로 묶는다. 자식 테이블에 자식 전용 컬럼을 두니 `NOT NULL` 제약이 자연스럽다. DB 차원에서 무결성이 강하다.

비용은 분명하다. 자식 하나를 가져올 때마다 JOIN 한 번이 든다. 폴리모픽 query는 부모와 *모든 자식 테이블*을 outer join한다. 데이터가 많고 폴리모픽 query가 잦은 도메인이라면 비용이 무시할 수준이 아니다.

언제 쓸 만한가. DB 무결성이 결정적이고, 폴리모픽 query 빈도가 낮으며, 자식 row의 수명이 길어 자주 update가 되는 도메인. 결제·계좌처럼 *법적으로 누락이 안 되는* 자리에 어울린다.

### TABLE_PER_CLASS — UNION ALL 폭발

`TABLE_PER_CLASS`는 부모 없이 자식별로 독립 테이블을 만든다. 자식 한 종류만 query할 때는 빠르다. 단일 테이블이니 join도 없다.

문제는 *폴리모픽 query*이다. `SELECT p FROM Payment p WHERE p.userId = ?`를 부르면 Hibernate가 `UNION ALL`로 모든 자식 테이블을 묶어 한 query로 만든다. 자식 종류가 늘어날수록 SQL이 비대해진다. plan cache도 잘 못 탄다.

Vlad는 이렇게 평했다. *"can generate statements that are way too complex."* 어지간한 도메인에서는 피하는 편이 낫다. 다만 *자식 종류가 셋 이하이고 폴리모픽 query가 거의 없는* 도메인에서는 무난히 통한다.

### @MappedSuperclass — 자바 상속만, DB는 모름

마지막 선택지는 가장 가볍다. `@MappedSuperclass`는 *자바 코드의 상속만 표현*한다. DB에는 부모 테이블이 없다. 부모의 필드(예: `createdAt`, `updatedAt`, `createdBy`)는 자식 테이블 각각에 컬럼으로 복제된다.

이 선택은 *폴리모픽 query가 필요 없을 때* 가장 깔끔하다. `AuditableEntity`를 부모로 두고 모든 도메인 엔티티가 그것을 상속해 `createdAt`, `updatedAt`을 공통으로 가져가는 패턴이 대표적이다. DB는 그저 컬럼 네 개가 더 있는 일반 테이블로 본다. JOIN도 UNION도 없다.

기억해두자. **상속 매핑을 고를 때, 가장 먼저 던질 질문은 "폴리모픽 query가 정말 필요한가"이다.** 필요 없으면 `@MappedSuperclass`로 충분하다. 필요하면 `SINGLE_TABLE`을 디폴트로. 무결성이 양보할 수 없는 자리에만 `JOINED`. `TABLE_PER_CLASS`는 *알고서* 골라야 한다.

---

## equals/hashCode — 가장 작은 메서드가 가장 큰 사고를 낸다

엔티티 클래스를 잘 다듬고 나면, IDE가 자동으로 만들어 주는 메서드 두 개가 있다. `equals`와 `hashCode`이다. 길이는 열 줄 남짓. 누구도 진지하게 읽지 않는다. 그런데 이 두 메서드가 운영에서 *가장 음흉한 버그*의 원천이 된다.

상황을 풀어 보자.

### Set 슬립 — 그 어이없는 사례

`Post`라는 엔티티가 있고, `Comment`를 자식으로 가진다. `Post`는 자식들을 `Set<Comment>`로 들고 있다.

```java
@OneToMany(mappedBy = "post", cascade = CascadeType.ALL, orphanRemoval = true)
private Set<Comment> comments = new HashSet<>();

public void addComment(Comment c) {
    comments.add(c);
    c.setPost(this);
}
```

그리고 `Comment` 클래스에는 IDE가 만들어 준 `equals`/`hashCode`가 PK 기반으로 들어가 있다.

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Comment c)) return false;
    return Objects.equals(id, c.id);
}

@Override
public int hashCode() {
    return Objects.hash(id);
}
```

언뜻 보면 정상이다. PK가 같으면 같은 코멘트로 본다. 깔끔하다.

이제 다음 코드를 실행한다고 해보자.

```java
Post post = new Post("새 글");
Comment c1 = new Comment("첫 댓글");
Comment c2 = new Comment("둘째 댓글");

post.addComment(c1);
post.addComment(c2);

entityManager.persist(post);   // PK 발급, 자식 두 개도 함께
```

자, 무슨 일이 벌어질까. 짐작이 가는가.

`c1`과 `c2`는 transient 상태일 때, 즉 `persist()` 호출 전에 `Set`에 들어갔다. 그때 두 객체의 `id`는 모두 `null`이었다. `hashCode()`는 `Objects.hash(null)` — 같은 값이 나온다. `equals()`도 `null == null` — 둘 다 같다고 본다. 즉 *둘은 같은 코멘트*로 인식된다. `Set`에는 첫 댓글이 들어간 뒤 둘째 댓글이 들어가려는 순간 중복으로 판단돼 *조용히 무시된다*.

심지어 더 음흉한 일이 그다음에 벌어진다. `persist()`가 실행되며 둘 다에게 PK가 할당된다. `c1.id = 100`, `c2.id = 101`. 그러면 두 객체의 `hashCode()`가 *달라진다*. `Set`은 hash bucket 위에서 객체를 찾는데, bucket 위치가 바뀐 객체는 `Set`이 더 이상 찾지 못한다. 분명 안에 들어 있는데 `contains(c1)`이 `false`를 돌려준다. 객체가 *Set 안에서 슬립한다*. 이름하여 **Set 슬립**.

이게 얼마나 끔찍한 일인가. 코드는 정상으로 보인다. 테스트도 통과한다. 다만 *특정 시점*에 *특정 객체가* 컬렉션 안에서 보이지 않을 뿐이다. 운영 모니터링에서는 "왜 자식이 누락되지?"라는 의문만 남는다. 추적할 단서가 없다.

이 한 사례가 PK 기반 `equals`/`hashCode`의 정체를 보여 준다. PK가 *DB에 의해 발급*되고, 객체의 생애주기 중 *transient 상태와 persisted 상태*가 모두 존재하는 한, 단순한 `Objects.hash(id)`는 시한폭탄이다.

### 정석 1 — 비즈니스 키가 있다면 그것을 쓰자

Vlad가 제시하는 첫 번째 정석은 단순하다. **자연 키, 즉 비즈니스 키가 있다면 그것으로 `equals`/`hashCode`를 만들자.**

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Book book)) return false;
    return Objects.equals(getIsbn(), book.getIsbn());
}

@Override
public int hashCode() {
    return Objects.hash(getIsbn());
}
```

`Book`은 ISBN이라는 자연 키를 가진다. ISBN은 객체 생성 시점에 결정되고, 영속화 이후에도 변하지 않는다. transient든 persisted든 같은 책이라면 같은 ISBN이다. `equals`/`hashCode`가 일관적이다. `Set`이 안전하다.

비즈니스 키가 분명히 있는 도메인이라면 이 방식이 가장 안전하다. *사람이 이미 식별자로 인식하는 무언가*가 있다면 그것을 쓰자.

### 정석 2 — DB 생성 PK밖에 없을 때

도메인이 그렇게 친절하지 않은 경우가 더 많다. 사용자, 게시글, 댓글 — 자연 키랄 게 없고 DB가 발급하는 PK밖에 없다. 이때의 정석은 두 가지 약속이다.

첫째, `equals`는 *id가 null이 아닐 때만 비교*한다. id가 null이면 서로 다른 객체로 본다 (같은 참조가 아닌 한). 이렇게 하면 transient 상태에서 두 객체가 우연히 "같다"고 판정되는 일이 없다.

둘째, `hashCode`는 *id가 아니라 `getClass().hashCode()`*를 돌려준다. 즉 *클래스 단위로 상수*이다. 객체의 생애주기 동안 `hashCode`가 절대 바뀌지 않는다. `Set` bucket에서 객체가 슬립하지 않는다.

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Post other)) return false;
    return id != null && id.equals(other.getId());
}

@Override
public int hashCode() {
    return getClass().hashCode();   // 상수
}
```

처음 보면 어이가 없다. `hashCode`가 상수라니, 그러면 모든 `Post`가 같은 hash bucket에 몰리는 거 아닌가? 맞다. 하지만 이 비효율은 *대부분의 도메인 코드에서 무시할 수준*이다. 우리가 엔티티를 `HashSet` 안에 *수십만 개* 담을 일은 거의 없다. 부모-자식 컬렉션 안의 수십 개 자식, 또는 영속 컨텍스트 안의 관리 엔티티 정도이다. 그 정도 규모에서 hash collision은 무의미하다.

반면 *생애주기에 걸쳐 hashCode가 변하지 않는다*는 보장은 무엇과도 바꾸기 어려운 가치이다. Vlad의 문장이 이를 가장 간결하게 정리한다. *"Always return `getClass().hashCode()` for generated IDs — ensures consistency across entity state transitions."* 상태 전이를 가로질러 일관성이 유지된다. 그것이 핵심이다.

### 그렇다면 무엇을 골라야 하는가

비즈니스 키가 분명한 도메인이라면 *비즈니스 키 방식*을. 그렇지 않다면 *PK + 상수 hashCode 방식*을. 이 두 가지 중 하나가 아니라면, 자기 엔티티의 `equals`/`hashCode`를 *지금 당장* 다시 보자. IDE 자동완성이 만들어 준 그 익숙한 패턴이, 운영에서는 가장 음흉한 슬립을 만들고 있을지도 모른다.

### 두 번째 체크리스트

핵심 엔티티 다섯 개의 `equals`/`hashCode`를 펼쳐 두고 자문해보자.

- PK 기반인가, 비즈니스 키 기반인가.
- PK 기반이라면 `id != null && id.equals(...)` 가드가 들어 있는가.
- `hashCode`가 상수(getClass)인가, 아니면 `Objects.hash(id)`인가.
- 이 엔티티가 transient 상태에서 `Set` 또는 `Map`의 키로 들어갈 자리가 있는가.

이 네 줄에 한 군데라도 자신이 없다면, 그 엔티티는 *Set 슬립의 후보*다.

---

## 컬렉션 매핑 — 작은 선언이 큰 SQL을 만든다

엔티티 안에 컬렉션을 선언하는 자리는 두 개의 결정이 한꺼번에 일어나는 자리이다. *방향*(단방향/양방향)과 *타입*(`List`/`Set`/`Map`). 이 두 결정의 조합이 Hibernate가 만들어내는 SQL의 모양을 결정한다.

### 단방향 `@OneToMany` — 숨겨진 join table

가장 자주 보는 안티패턴 하나가 *단방향 `@OneToMany`* 이다.

```java
@Entity
public class Post {
    @Id @GeneratedValue
    private Long id;

    @OneToMany(cascade = CascadeType.ALL)
    private List<Comment> comments = new ArrayList<>();
}

@Entity
public class Comment {
    @Id @GeneratedValue
    private Long id;
    // Post 참조 없음 — Comment는 자기가 어느 Post에 속하는지 모른다
}
```

깔끔해 보인다. `Post`만 `Comment`를 알고, 자식은 부모를 모른다. 도메인 그림이 단순해진다.

그런데 Hibernate는 이 매핑을 어떻게 풀까. 자식이 부모를 가리키는 *외래 키 컬럼*이 없다. 그러면 둘 사이의 관계를 어디에 적나. 답은 *별도의 join table*이다. `post_comments`라는 중간 테이블을 만들어 `post_id`, `comment_id` 두 컬럼을 둔다. 모든 fetch가 join 한 번 더 늘어난다.

심지어 어떤 자식 하나를 제거하면 어떤 일이 벌어질까. Hibernate는 join table에서 *그 자식과 연결된 모든 row를 지운 뒤*, 남은 자식들의 row를 *다시 insert*하는 동작을 한다. *delete-all-and-reinsert*이다. 100개의 자식 중 1개를 빼는데 99번의 INSERT가 부가로 발생한다. 끔찍한 일이다.

정석은 이렇다. **`@OneToMany`는 양방향으로 만들고, `mappedBy`로 자식이 외래 키 주인임을 알려준다.** 그리고 부모에는 자식을 더해 주는 helper method를 두자.

```java
@Entity
public class Post {
    @OneToMany(mappedBy = "post", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Comment> comments = new ArrayList<>();

    public void addComment(Comment c) {
        comments.add(c);
        c.setPost(this);
    }
    public void removeComment(Comment c) {
        comments.remove(c);
        c.setPost(null);
    }
}

@Entity
public class Comment {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "post_id")
    private Post post;
}
```

이제 join table은 없다. 외래 키는 `comment.post_id` 하나. 자식 하나를 제거해도 영향받는 row는 단 한 줄이다. 정상이다.

권고 #7이 못 박는다. *"관계는 `@OneToMany` 단방향 금지, 양방향 또는 join entity로."* 잊지 말자.

### `@ManyToMany` + `List` — delete-all-and-reinsert의 함정

`@ManyToMany`에서도 비슷한 함정이 있다. 만약 컬렉션을 `List`로 선언하면, 같은 row가 중복으로 들어갈 수 있다. 그러면 Hibernate는 *전체 컬렉션을 비우고 다시 채우는 방식*으로 삭제를 처리한다. 즉 한 줄을 빼고 싶었는데 *모든 자식 row를 delete하고 나머지를 re-insert*한다.

정석은 단순하다. **`@ManyToMany`에는 `Set`을 쓰자.** `Set`은 중복이 없으니 Hibernate가 자식 하나만 정확히 지우는 SQL을 만든다.

```java
@ManyToMany
@JoinTable(
    name = "post_tag",
    joinColumns = @JoinColumn(name = "post_id"),
    inverseJoinColumns = @JoinColumn(name = "tag_id"))
private Set<Tag> tags = new HashSet<>();
```

더 일반적으로는, `@ManyToMany`가 정말 *순수한* 다대다인지 다시 보자. 보통은 *연결 엔티티*(`PostTag`처럼 join을 위한 엔티티)를 만들어 *두 개의 `@ManyToOne`*으로 푸는 편이 코드와 SQL 모두 깔끔해진다. join 엔티티에 *연결 시점*, *연결자*, *연결 메타데이터*를 더할 수도 있다.

### 양방향 `@OneToMany`에서 `Set`을 피하라

여기서 함정 하나가 더 있다. 위에서는 "@ManyToMany는 Set"을 권했다. 그런데 *양방향 `@OneToMany`*에서는 반대로, **`Set`을 피하는 편이 낫다**.

이유는 이렇다. 양방향 `@OneToMany`에서 컬렉션을 `Set`으로 두면, Hibernate가 컬렉션을 *평가*할 때 자식들의 `equals`/`hashCode`를 호출한다. 자식이 백 개면 백 번의 `equals`/`hashCode`이다. 그 자체로 부담이기도 하지만, 그 안에서 PK를 비교하느라 *lazy proxy 초기화*가 일어나면 N+1로 폭발한다.

Vlad는 직설적으로 정리한다. *"Avoid using Set for bidirectional JPA OneToMany collections."* 그 자리에는 `List`가 어울린다. 자식이 부모를 알고 있으니 외래 키 컬럼 하나로 관계가 일대일로 묶이고, `List`라고 해서 추가 비용이 생기지 않는다.

정리하면 이렇다.

| 컬렉션 자리 | 권장 타입 | 사유 |
|-------------|-----------|------|
| 양방향 `@OneToMany` | `List` | `Set`은 자식의 equals/hashCode 폭발 |
| 단방향 `@ManyToMany` | `Set` | `List`는 delete-all-and-reinsert 위험 |
| 차라리 join 엔티티 | `@ManyToOne` 두 개 | 다대다는 일대다 + 일대다로 분해 |

작은 결정이지만 SQL의 모양을 통째로 바꾼다는 사실을 기억해두자.

---

## `@Immutable` — dirty checking 비용 차단의 첫 다리

위 컬렉션 단원에서 우리는 *Hibernate가 매 flush마다 무언가를 비교한다*는 사실을 살짝 봤다. 이 비교가 바로 **dirty checking**이다. PersistenceContext 안에 있는 모든 엔티티에 대해, Hibernate는 load 시점의 *스냅샷*을 메모리에 저장해두고 flush 시점에 *현재값*과 *스냅샷*을 reflection으로 비교한다. 다른 필드가 있으면 UPDATE를 만든다.

이 동작은 *편의의 핵심*이지만 동시에 *비용의 근원*이다. 같은 엔티티가 메모리에 *두 벌* 존재한다. N개 엔티티 × P개 속성의 reflection 비교가 매 flush마다 일어난다. PersistenceContext가 커지면 dirty checking 비용도 같이 커진다.

여기서 떠올려보자. 변하지 않는 데이터가 있다. `Country`, `Currency`, `Category` — 마스터 데이터, 카탈로그 데이터. 한 번 들어오면 운영 동안 *변경되지 않는다*. 그런데도 Hibernate는 이 엔티티들에 대해 매 flush마다 스냅샷을 비교한다. 비용은 발생하는데 효과는 없다.

이 자리를 막아주는 어노테이션이 `@Immutable`이다.

```java
@Entity
@Immutable
public class Country {
    @Id
    private Long id;
    private String code;
    private String name;
}
```

`@Immutable`이 붙은 엔티티는 dirty checking 대상에서 빠진다. 스냅샷을 저장하지 않고, flush 시 비교도 하지 않는다. 메모리도 절약되고 CPU도 절약된다. update를 시도하면 무시되거나(설정에 따라) 예외가 난다 — *읽기 전용*이라는 의미가 정직하게 강제된다.

여기서 한 번에 둘이 풀린다. 첫째, 운영의 dirty checking 부담이 줄어든다. 둘째, *7장에서 다룰 2차 캐시와 자연스럽게 짝을 이룬다*. `@Immutable` + `@Cache(strategy = READ_ONLY)`는 마스터 데이터를 위한 가장 깔끔한 묶음이다. *변경되지 않는다*는 사실이 두 장치 모두를 가능하게 한다. 7장에서 이 다리를 다시 건넌다.

이 절은 chapter 9의 본격적인 batch·dirty 단원으로 가는 두 번째 다리이기도 하다. *PersistenceContext에 무엇이 얼마나 쌓이는가*가 dirty checking 비용을 결정한다는 사실, 그리고 *그 비용을 어떻게 줄일 수 있는가*가 여러 자리에서 반복해 등장한다.

---

## Bytecode enhancement — 빌드 한 단계가 운영을 바꾼다

이제 가장 흥미로운 자리로 들어간다. 처음 머리말에서 던졌던 두 번째 질문을 다시 떠올려 보자. *"LAZY를 켰는데 왜 컬렉션 fetch가 줄지 않을까?"*. 더 정확히 풀어보면 *"`@ManyToOne(fetch = FetchType.LAZY)`를 적었는데 왜 SQL 로그에 추가 SELECT가 나갈까?"* 라는 질문이다. 이 자리가 **bytecode enhancement**가 빛을 발하는 자리이다.

### 기본 LAZY의 한계 — `@ManyToOne`이 *진짜* LAZY가 아닌 이유

먼저 기본 동작부터 이해해야 한다. JPA에서 `@ManyToOne`의 기본값은 `FetchType.EAGER`이다. 그래서 모두 *명시적으로* `fetch = FetchType.LAZY`를 박는다. 그런데 그렇게 적어도 *진정한 LAZY*가 되지 않는 경우가 흔하다. 왜 그럴까.

`@ManyToOne` LAZY의 구현 원리를 들여다보자. Hibernate는 LAZY 연관관계를 *proxy*로 채워둔다. 부모 객체를 가져오면 자식 자리에는 *실제 자식이 아닌 proxy*가 들어가 있고, 자식의 메서드가 호출되는 순간 proxy가 *실제 SELECT*를 발동시킨다. 이 동작이 `@OneToMany` 컬렉션에서는 잘 작동한다. 컬렉션 자체가 proxy(`PersistentBag`, `PersistentSet`)이기 때문이다.

문제는 `@ManyToOne`이다. proxy를 만들려면 자식의 클래스를 *상속*해 가짜 자식 객체를 만들어야 한다. 그런데 final 클래스라거나, no-arg constructor가 없거나, 자식의 PK 외에 다른 필드를 미리 채워야 하는 경우, proxy를 만들 수 없거나 만들어도 *PK 비교*를 위해 lazy로 두기 어렵다. 결국 Hibernate는 *그 자리에서 자식을 즉시 SELECT*해 채워 넣는다. LAZY라고 적었지만 *실제로는 EAGER*.

심지어 자식 클래스에 `equals`/`hashCode`가 *PK 기반*으로 되어 있다면 더 큰 문제가 생긴다. 자식 객체가 proxy에서 unwrap 되어야 비교가 가능하니, 부모의 컬렉션 안에 들어 있던 자식들이 *모두 즉시 SELECT*된다. 다시 *N+1*이다.

이쯤 되면 답답하다. LAZY를 적어도 LAZY가 안 된다니. 그 답이 bytecode enhancement이다.

### Bytecode enhancement란 무엇인가

Hibernate는 빌드 시점에 *엔티티 클래스의 bytecode를 살짝 수정*하는 도구를 제공한다. Maven에는 `hibernate-enhance-maven-plugin`, Gradle에는 동일한 기능의 Gradle plugin이 있다. 빌드 단계에 한 줄이 추가되고, 그것만으로 모든 엔티티의 setter/getter에 *Hibernate가 알아챌 수 있는 작은 hook*이 박힌다.

이 hook이 세 가지를 가능하게 한다. 옵션별로 살펴보자.

```xml
<plugin>
    <groupId>org.hibernate.orm.tooling</groupId>
    <artifactId>hibernate-enhance-maven-plugin</artifactId>
    <version>${hibernate.version}</version>
    <executions>
        <execution>
            <configuration>
                <enableLazyInitialization>true</enableLazyInitialization>
                <enableDirtyTracking>true</enableDirtyTracking>
                <enableAssociationManagement>true</enableAssociationManagement>
            </configuration>
            <goals>
                <goal>enhance</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

Gradle도 동일한 옵션 이름을 그대로 쓴다. 세 옵션을 하나씩 풀어 보자.

### `enableLazyInitialization` — `@ManyToOne` LAZY가 *진짜* LAZY가 된다

이 옵션이 켜지면, Hibernate는 *필드 단위로* lazy proxy를 만들 수 있게 된다. proxy 객체를 만드는 게 아니라 *bytecode 안에 lazy 접근 지점*을 박는다. 부모 엔티티의 자식 참조 자리가, 실제 객체 대신 *"필요할 때 fetch한다"* 라는 흔적을 갖게 된다.

그 결과 `@ManyToOne(fetch = FetchType.LAZY)`이 비로소 진짜 LAZY가 된다. 부모를 fetch해도 자식 SELECT가 따라가지 않는다. `parent.getChild().getName()`을 호출하는 *바로 그 시점*에 SELECT가 나간다.

LAZY를 곳곳에 적어두고도 N+1이 나는 코드 베이스라면, 이 옵션 하나로 *상당량의 부담이 사라진다*. 도입 비용은 빌드 단계에 한 줄. 운영 이득은 fetch plan이 의도대로 동작하는 것. 트레이드오프가 매우 명확하다.

### `enableDirtyTracking` — 스냅샷 비교를 인터셉터로

두 번째 옵션은 `enableDirtyTracking`이다. 위 `@Immutable` 단원에서 봤듯, Hibernate의 기본 dirty checking은 *스냅샷 vs 현재값 비교*이다. 메모리 두 배, reflection 비교 비용.

이 옵션이 켜지면, Hibernate가 setter 호출 자체에 *dirty 플래그*를 박는다. 어떤 필드가 변경됐다면 그 필드가 "더러워졌다"고 *그 자리에서* 표시된다. flush 시점에는 *스냅샷 비교 없이*, 더러워진 필드만 모아 UPDATE를 만든다.

효과가 큰 자리는 두 가지다. 첫째, *스냅샷을 만들지 않으니 메모리가 절반*이다. 큰 PersistenceContext일수록 메모리 이득이 커진다. 둘째, *어떤 필드가 변경됐는지 정확히 안다*. 그래서 UPDATE에 *변경된 컬럼만* 담을 수 있다(`@DynamicUpdate`와 결합 시). 인덱스가 많은 테이블에서 모든 컬럼을 UPDATE 절에 담으면 인덱스를 모두 건드리지만, 변경된 컬럼만 담으면 인덱스 비용이 줄어든다.

운영의 관점에서, *큰 엔티티가 많고 flush가 잦은* 시스템에서 이 옵션은 throughput에 직접 영향을 준다. dirty checking 자체가 hot path가 되는 시스템이라면 *반드시 검토할* 옵션이다.

### `enableAssociationManagement` — 양방향 자동 동기화

세 번째 옵션은 `enableAssociationManagement`이다. 양방향 연관관계의 *동기화*를 빌드 단계에 자동으로 박는다.

위에서 우리는 양방향 `@OneToMany`에 `addComment(Comment c)`라는 helper method를 만들어 *부모 컬렉션과 자식 참조를 함께 설정*하는 패턴을 봤다. 이 helper method를 깜빡하고 한쪽만 설정하면 어떤 일이 벌어질까. 영속 컨텍스트에서는 자식이 부모를 모르고, 부모는 자식을 안다. flush 시점에 외래 키가 어디로 박힐지 *예측이 어렵다*. 운영의 음흉한 버그 자리이다.

`enableAssociationManagement`가 켜지면, `setPost(p)`를 호출하는 *순간* 자동으로 `p.getComments().add(this)`가 일어난다. 반대 방향도 마찬가지다. helper method를 깜빡해도, 양방향 무결성이 *자동으로* 유지된다.

이 옵션은 *얼마나 helper method 규율이 잡혀 있느냐*에 따라 가치가 갈린다. 코드 베이스가 크고 협업이 활발하다면, 자동화는 큰 안전망이 된다. helper method 패턴이 이미 정착해 있다면 굳이 안 켜도 된다.

### 도입 비용 vs 운영 이득

세 옵션을 모아 다시 한 번 정리해보자.

| 옵션 | 무엇이 가능해지나 | 운영 이득 |
|------|-------------------|-----------|
| `enableLazyInitialization` | `@ManyToOne`/`@OneToOne`의 *진짜* LAZY | 의도하지 않은 secondary select 차단 |
| `enableDirtyTracking` | 스냅샷 → 인터셉터 기반 추적 | 메모리 절반, dirty checking CPU 절감, `@DynamicUpdate` 효과 극대화 |
| `enableAssociationManagement` | 양방향 자동 동기화 | helper method 누락에도 무결성 유지 |

도입 비용은 무엇인가. 빌드 단계에 plugin 한 줄. 빌드 시간이 약간 늘어난다. 그것이 전부이다. *런타임 비용은 없다* — 이미 빌드 시점에 bytecode가 다듬어져 있기 때문이다.

이 정도 비용이라면 *왜 안 켜는가*가 오히려 더 어려운 질문이다. 다만 *왜 켰는지*를 팀 전체가 설명할 수 있어야 한다. 운영 중에 lazy 동작이 갑자기 바뀌면 *왜 그런지*를 빠르게 추적해야 하기 때문이다. plugin 설정 한 줄이 운영에 영향을 미친다는 사실이 모든 동료에게 인지돼 있어야 한다.

### 세 번째 체크리스트

여기까지 왔으면 자기 프로젝트의 빌드 설정을 한 번 들여다 보자.

- bytecode enhancement plugin이 켜져 있는가, 꺼져 있는가.
- 켜져 있다면, 세 옵션 중 어느 옵션이 켜져 있는가.
- 그 옵션을 *왜 켰는지* 팀 안에서 한 줄로 설명할 수 있는가.
- `@ManyToOne(fetch = LAZY)`을 적어두고도 SQL 로그에 *해당 자식 SELECT*가 따라 나가는 자리가 있는가.

네 번째 질문에 "있다"라고 답이 나오는 자리가 있다면, 그 자리가 `enableLazyInitialization`이 *진짜* 도움이 되는 자리이다.

---

## 컬럼 타입을 인색하게 — 권고 #6 회수

엔티티를 빚는 마지막 결정 자리가 있다. *각 필드를 어떤 컬럼 타입으로 매핑할 것인가*. 권고 #6은 이를 한 줄로 정리한다. **컬럼 타입을 인색하게.** `BIGINT`보다 `INT`를, `varchar`는 길이를 명확히, `@Lob`은 주의해 쓰자.

### `@Column(length = ...)`을 박자

JPA 표준에서 `String` 필드의 디폴트 길이는 255이다. `@Column` 없이 그냥 `String name`을 적으면 `VARCHAR(255)`로 컬럼이 생성된다. *대부분의 자리에서 이는 너무 길거나 너무 짧다*.

너무 길면 무엇이 문제인가. DB에 따라 다르지만, varchar 길이가 인덱스 키 길이 산정에 들어간다. *복합 인덱스*에 varchar 컬럼이 들어가면 인덱스 페이지의 fill ratio가 떨어진다. 캐시 효율도 함께 떨어진다.

너무 짧으면 무엇이 문제인가. 운영 한 달 만에 *길이 초과 예외*가 나기 시작한다. 사용자 이름이 256자인 사람이 있을 리 없지만, *비고 필드*에 사용자가 무엇을 적어 넣을지는 모른다.

권고는 단순하다. **모든 `String` 필드에 `@Column(length = ...)`을 명시적으로 박자.** 의도를 박는 것이다.

```java
@Column(length = 50, nullable = false)
private String name;

@Column(length = 4000)
private String description;
```

50인지 4000인지가 중요한 게 아니라, *얼만큼이라고 정했는지가 명시적으로 코드에 박혔는지*가 중요하다. 6개월 뒤 누군가가 이 컬럼을 인덱스에 넣을지 고민할 때, 그 길이가 *의도된 결정*이었음을 알 수 있어야 한다.

### `@Lob`의 함정

큰 텍스트나 바이너리 데이터를 저장하려고 `@Lob`을 쓰는 경우가 있다. `@Lob`은 DB의 `CLOB`/`BLOB` 컬럼으로 매핑된다.

여기에 함정 하나가 있다. `@Lob`이 붙은 필드는 *모든 SELECT에 비용을 더한다*. CLOB/BLOB은 row 본체와 별도 페이지에 저장되는 경우가 많아 read마다 추가 IO가 발생한다. 그 자체로도 비용이지만, *그 컬럼을 안 쓰는 SELECT*에서도 비용이 따라온다 — Hibernate가 디폴트로 엔티티 전체를 가져오기 때문이다.

대안은 두 가지이다. 첫째, 정말 큰 데이터가 아니라면 *그냥 `varchar(N)` 또는 `text`*로 두자. PostgreSQL의 `text`는 사실상 무제한이고, 부담은 `@Lob`보다 훨씬 적다. 둘째, 큰 데이터가 *진짜 큰 데이터*라면 별도 엔티티로 분리하고 LAZY로 연결하자. 그러면 평소 SELECT에는 그 컬럼이 따라오지 않는다.

### JSON 컬럼은 잠시 미뤄두자

요즘은 도메인의 일부를 JSON 컬럼에 담는 패턴이 자주 보인다. PostgreSQL의 `jsonb`, MySQL의 `JSON` 컬럼이 대표적이다. Hibernate 6은 `@JdbcTypeCode(SqlTypes.JSON)` 어노테이션으로 이를 자연스럽게 지원한다.

JSON 컬럼은 강력하지만, 그 자체로 별도의 세계이다. *어떻게 query하는가*가 일반 컬럼과 전혀 다르다. 인덱싱 전략도 다르다. 이 주제는 5장의 Projection과 12장의 Hibernate 6 신기능에서 본격적으로 회수한다. 지금 단계에서는 *JSON 컬럼은 깊은 주제이고, 도메인 모델을 처음 빚을 때부터 함부로 넣지 말자*라는 정도로 머리에 박아두자.

---

## 마무리 — 엔티티 한 줄이 SQL 한 줄을 결정한다

지금까지 살펴 본 결정들을 한 번에 모아 보자.

- **식별자**: `IDENTITY`는 배치를 죽인다. SEQUENCE + pooled-lo가 정석. `AUTO`는 지뢰. MySQL은 우회로.
- **상속**: `SINGLE_TABLE`이 디폴트. 무결성이 결정적이면 `JOINED`. 폴리모픽이 없으면 `@MappedSuperclass`. `TABLE_PER_CLASS`는 알고서.
- **equals/hashCode**: 비즈니스 키 vs PK + `getClass().hashCode()`. *Set 슬립*은 가장 음흉한 버그다.
- **컬렉션**: 단방향 `@OneToMany` 금지. `@ManyToMany List` 금지. 양방향 `@OneToMany`에는 `List`. 컬렉션 자리마다 SQL의 모양이 다르다.
- **`@Immutable`**: dirty checking 비용 차단의 첫 다리. 7장의 2차 캐시와 연결된다.
- **Bytecode enhancement**: 빌드 단계 한 줄이 LAZY를 *진짜* LAZY로, dirty checking을 *절반* 비용으로 바꾼다.
- **컬럼 타입**: 인색하게. 길이를 박자. `@Lob`은 의도해 쓰자.

이 결정들은 모두 *엔티티 클래스의 한두 줄*에서 정해진다. 그러나 그 한두 줄이 Hibernate가 만들어내는 SQL의 모양, 그리고 운영의 throughput을 직접 결정한다. *엔티티를 잘 빚는다*는 말의 무게가 여기에 있다.

자기 프로젝트로 한 번 돌아가 보자. 핵심 엔티티 다섯 개를 펼쳐 두고 세 가지를 자문하자.

- `@Id` 전략이 *의도된* 것인가.
- `equals`/`hashCode`가 transient 시점에 안전한가.
- bytecode enhancement를 *왜* 켰는지(또는 안 켰는지) 한 줄로 설명할 수 있는가.

이 세 줄이 명료해지면, 우리 프로젝트의 엔티티 토대는 단단하다. 그 위에 다음 장의 fetch 전략이 자연스럽게 올라간다.

다음 장에서는 *그 엔티티들이 query 시점에 어떻게 뽑혀 나오는가*를 본다. 모두가 안다고 말하지만 모두가 한 번씩은 다시 만나는 그 이름 — N+1. *왜 우리 코드에는 여전히 N+1이 있을까*. 이 질문을 함께 살펴보자.
