# 5장. 가져오는 형태도 다시 본다 — Projection과 query 선택

글 목록 API 하나를 떠올려 보자. 화면에는 글 제목, 작성자 이름, 작성 시각, 그리고 댓글 수 — 네 가지 정보만 보이면 충분하다. 그런데 코드를 들춰 보면 `postRepository.findAll(pageable)`이 떡 하니 박혀 있다. SQL 한 줄이 나간다. 이 한 줄이 끌고 오는 컬럼은 몇 개일까? `Post`에 24개, `JOIN FETCH author`로 묶여 `Author`에서 18개, 그리고 `created_on`, `updated_on`, `deleted`, `version`까지 자동으로 끌려 나오는 잡다한 컬럼들. 결국 네 개를 보여주기 위해 마흔 개가 넘는 컬럼이 네트워크를 타고 넘어온다. SQL 한 줄로는 단정하고 빠른 코드처럼 보이지만, *한 row의 무게*는 우리가 본 적도 없다.

여기에 무게가 또 한 겹 얹힌다. 끌고 온 `Post`와 `Author`는 모두 PersistenceContext에 등록된다. Hibernate는 이들의 LoadedState 스냅샷을 메모리에 잡아 두고, 트랜잭션 끝에 dirty checking을 돌려 *수정된 게 있는지* 일일이 비교한다. 우리가 "글 목록 한 페이지를 보여 줘"라고 한 줄을 짠 것뿐인데, 시스템은 *우리가 이 글들을 수정할지도 모른다*고 가정하고, 그에 대비한 모든 비용을 미리 치른다. 끔찍한 일이다. 보여주기만 할 데이터를 가져오면서 수정 가능성을 위한 메모리와 CPU를 함께 사 오는 셈이다.

지난 4장에서 우리는 N+1을 잡았다. SQL 카운트를 줄였다. 박수받을 만한 진전이다. 그런데 SQL 카운트가 1로 줄었다고 해도 *그 한 줄이 끌고 오는 것의 무게*는 그대로다. fetch를 줄였으면, 이제 가져오는 형태를 다시 봐야 한다. 이 챕터는 그 이야기다.

먼저 슬로건 한 줄을 못 박고 시작하자. Vlad Mihalcea의 14가지 고성능 팁 중 열 번째 항목이다.

> **수정 안 할 read는 모두 DTO.**

이 한 줄이 우리의 나침반이다. 엔티티 fetch는 *modification 의도가 있을 때만* 사용한다. 화면에 보여주고, JSON으로 응답하고, 통계 페이지에 띄울 데이터는 — 엔티티가 아니라 DTO로 가져온다. 이 원칙 하나를 받아들이는 순간, 우리는 매우 많은 비용을 *치르지 않을 권리*를 얻는다.

이 권리가 구체적으로 무엇이며, 어떻게 행사하는지, 그리고 도구가 한두 가지가 아니라 일곱 가지나 되는 이유는 무엇인지를 함께 살펴보자.

## 엔티티로 가져오는 것이 왜 비싼가

DTO 이야기를 시작하기 전에, *왜 그렇게까지 해야 하는가*를 먼저 정리하자. 엔티티 fetch가 정확히 무엇을 비싸게 만드는지를 잡아 두지 않으면, "그냥 깔끔해 보이니까 엔티티 그대로 쓰자"는 유혹이 한 줄 한 줄 코드를 다시 무겁게 만든다.

엔티티 한 건을 가져온다고 해 보자. 어떤 일이 일어나는가?

첫째, SELECT 절에 *엔티티의 모든 매핑 컬럼*이 들어간다. `@Column`이 28개 박혀 있으면 SELECT 컬럼이 28개다. 화면에 네 개만 쓸 거라고 해서 자동으로 좁혀 주지 않는다. 한 row의 폭이 4KB든 16KB든 그대로 네트워크를 탄다.

둘째, 가져온 ResultSet은 *엔티티 객체로 hydrate*된다. 즉 Hibernate가 `new Post()`를 만들고 28개 컬럼을 setter나 reflection으로 채워 넣는다. 이 hydration 비용은 컬럼 수에 비례한다.

셋째, hydrate된 엔티티는 *PersistenceContext에 등록*된다. Hibernate는 그 엔티티의 LoadedState — 처음 가져왔을 때의 컬럼 값들 — 를 별도의 배열로 떠 둔다. 트랜잭션 끝에 dirty checking을 돌릴 때 *현재 값과 LoadedState를 비교*하기 위해서다. 컬럼이 28개면 비교도 28번이다. 이 비교는 *읽기만 한 엔티티에도 어김없이 일어난다*. Hibernate는 우리가 어떤 의도였는지 모르기 때문이다.

넷째, lazy 연관관계마다 proxy를 씌운다. `@ManyToOne(fetch = LAZY)`인 `author`에는 `Author$HibernateProxy$abc123`이 들어간다. 이 proxy는 그것대로 메모리를 먹는다.

다섯째, 엔티티가 살아있는 동안 *변경이 일어나면 트랜잭션 끝에 자동으로 UPDATE가 나간다*. 우리가 의도하지 않은 컬럼까지 변경이 감지되어 UPDATE에 실린다면? 끔찍한 일이다. 실제로 이런 식의 *유령 UPDATE*가 production에서 발견되는 경우가 적지 않다.

이 다섯 가지가 모두 *읽기 한 번*의 그림자다. 보여주기만 할 데이터에 이 그림자를 함께 사 와야 할 이유는 어디에도 없다.

DTO로 가져오면 어떻게 달라지는가? 첫째, SELECT 절은 *DTO 생성자에 필요한 컬럼만* 들어간다. 컬럼 수가 줄어든다. 둘째, ResultSet은 *DTO 객체로 직접 매핑*된다. Hibernate가 `new PostListItemDto(...)`를 호출할 뿐, 엔티티 hydration 경로를 타지 않는다. 셋째, DTO는 *PersistenceContext에 등록되지 않는다*. LoadedState도 없고, dirty checking 대상도 아니다. 넷째, proxy도 없다. DTO에 `Author`가 필요하면 `String authorName` 컬럼 하나로 끝낸다. 다섯째, 유령 UPDATE의 가능성이 0이 된다. DTO는 *변경되어도 DB에 반영되지 않는다*. 시스템이 보장한다.

이 차이가 얼마나 큰가? JPAB.org가 운영하는 표준 ORM 벤치마크에는 다양한 JPA provider — Hibernate, EclipseLink, OpenJPA, DataNucleus — 가 분석성 데이터 처리 시 보이는 throughput이 정리되어 있고, 같은 데이터를 *엔티티로 가져왔을 때와 projection으로 가져왔을 때*의 차이가 분명히 드러난다. ORM Battle 2025의 결과도 같은 방향을 가리킨다. 단순 read에서 JDBC > jOOQ > Hibernate(엔티티) 순으로 빠르고, 그 차이는 종종 10~30%에 이른다. *엔티티 fetch의 추가 비용이 그만큼*이라는 뜻이다. 즉 Hibernate 자체가 느려서가 아니라, *엔티티로 가져오기 때문에 생기는 그림자*가 그만큼인 것이다. DTO projection을 쓰면 그 그림자의 상당 부분이 사라진다.

그렇다면 어떻게 DTO로 가져올까? 도구가 한두 가지가 아니다. 하나씩 살펴보자.

## Projection 도구 상자 일곱 가지

JPA와 Hibernate, 그리고 Spring Data가 우리에게 건네는 projection 도구는 일곱 가지쯤 된다. 처음에는 너무 많아 보이지만, 각각이 *쓸 자리*와 *피할 자리*가 분명하다. 표 하나로 먼저 펼쳐 놓고, 하나씩 풀어 보자.

| 옵션 | 형태 | 권장 시나리오 |
|------|------|---------------|
| JPQL constructor expression | `select new com.acme.PostDto(p.id, p.title) from Post p` | DTO 클래스가 있고 JPQL을 쓸 때의 기본 |
| Tuple | `select p.id as id, p.title as title ...` → `tuple.get("title")` | 일회성, DTO 클래스 만들기가 과한 자리 |
| `@SqlResultSetMapping` + `@ConstructorResult` | Native SQL의 결과를 DTO로 매핑하는 JPA 표준 | Native SQL을 표준 방식으로 DTO에 매핑할 때 |
| `TupleTransformer` (Hibernate 6+) | Hibernate-specific 변환기 | 동적 매핑, 타입 변환 자유도가 필요한 자리 |
| Spring Data Interface Projection | `interface PostSummary { Long getId(); String getTitle(); }` | Spring Data 환경의 간단한 read-only |
| Java Records + JPQL constructor expression | `select new acme.PostDto(p.id, p.title) ...`의 Record | Java 16+, 가장 깔끔한 immutable DTO |
| `@Subselect` | 가상 read-only 엔티티 — 임의 SQL/뷰 위에 매핑 | 복잡한 분석 쿼리를 도메인 객체로 들고 올 때 |

일곱 줄짜리 표를 던져 놓고 끝낼 일이 아니다. 각각이 어떤 모양이고, 언제 빛나고, 언제 피해야 하는지를 함께 짚어 보자.

### JPQL constructor expression — 가장 익숙한 출발점

가장 오래되고 가장 익숙한 도구다. JPQL의 `select` 절에서 `new` 키워드와 함께 DTO 클래스의 *완전한 경로*를 적어 주면 된다.

```java
public record PostListItemDto(Long id, String title, String authorName, Instant createdOn) {}

@Query("""
    select new com.acme.dto.PostListItemDto(p.id, p.title, a.name, p.createdOn)
    from Post p join p.author a
    where p.status = 'PUBLISHED'
    order by p.createdOn desc
    """)
List<PostListItemDto> findRecentPosts(Pageable pageable);
```

이 DTO는 엔티티가 아니다. PersistenceContext에 등록되지 않는다. dirty checking 대상도 아니다. SELECT 절에는 정확히 네 개의 컬럼만 들어간다. 우리가 원하던 그림이다.

쓸 자리는 분명하다. *DTO 클래스를 정식으로 정의해 두고 정적으로 자주 호출되는 read API*. 거의 모든 list/조회 API의 기본형이다.

피할 자리는? *일회성 쿼리*. 보고서 한 번 뽑으려고 DTO 클래스를 만드는 것은 과하다. 또 *동적으로 SELECT 절이 달라지는 쿼리*. constructor expression은 시그니처가 고정된 생성자에 묶이기 때문에, 컬럼이 들쭉날쭉한 경우엔 안 맞는다.

Hibernate 6부터는 한 가지 자잘한 행복이 더해진다. *완전한 경로 없이 DTO 클래스명만 적어도 된다*. 즉 `select new PostListItemDto(...)`만 써도 된다. 그리고 `select PostListItemDto(...)` — `new` 키워드 없이도 가능해졌다. 작은 변화이지만, JPQL이 SQL에 한 걸음 더 가까워졌다.

여기에 *Java Records*를 얹으면 형태가 거의 완성에 가까워진다.

```java
public record PostListItemDto(Long id, String title, String authorName, Instant createdOn) {}
```

Record는 immutable이고, `equals`/`hashCode`/`toString`까지 컴파일러가 만들어 준다. DTO에 setter가 있을 이유가 없고, 매번 보일러플레이트로 채우던 코드가 한 줄로 줄어든다. Java 16 이상을 쓸 수 있다면 — *DTO는 Record로 한다*가 거의 무조건의 권장이라고 봐도 무방하다.

### Tuple — DTO 클래스 만들기가 과한 자리

DTO 클래스를 만들 가치가 없는 일회성 조회에는 `Tuple`을 쓰는 선택지가 있다. JPA 2.0부터 표준이다.

```java
List<Tuple> rows = em.createQuery("""
    select p.id as id, p.title as title, p.createdOn as createdOn
    from Post p where p.status = :status
    """, Tuple.class)
    .setParameter("status", Status.PUBLISHED)
    .getResultList();

for (Tuple t : rows) {
    Long id = t.get("id", Long.class);
    String title = t.get("title", String.class);
    // ...
}
```

장점은 분명하다. *DTO 클래스를 만들 필요가 없다*. 별칭으로 접근하니 가독성도 나쁘지 않다. SELECT 절은 우리가 명시한 컬럼만 들어간다.

단점도 분명하다. *컴파일 타임 타입 안전성이 없다*. `t.get("title", String.class)`는 별칭이 틀리거나 타입이 어긋나면 런타임에서야 터진다. 그리고 *API 경계로 내보낼 자료형이 아니다*. JPA의 `Tuple` 자체를 컨트롤러 응답으로 그대로 내보내면 묘한 의존성이 생긴다.

쓸 자리는 *내부 어드민 페이지의 일회성 쿼리, 데이터 마이그레이션 스크립트, 통계 뽑기*처럼 짧게 살고 끝나는 코드. 피할 자리는 *공개 API의 응답*. 거기엔 정식 DTO를 만드는 편이 낫다.

### `@SqlResultSetMapping` + `@ConstructorResult` — Native SQL과 DTO를 잇는 표준 다리

Native SQL을 써야 하는 자리가 있다. window function, CTE, PIVOT, JSON 함수 — JPQL이 가리지 못하는 영역이다. 그런데 native SQL의 ResultSet을 어떻게 DTO에 채울까? JDBC ResultSet을 손으로 풀면 *우리가 ORM을 쓰는 의미가 흐려진다*.

JPA 표준이 마련해 둔 다리가 `@SqlResultSetMapping`과 `@ConstructorResult`다.

```java
@SqlResultSetMapping(
    name = "PostListItemMapping",
    classes = @ConstructorResult(
        targetClass = PostListItemDto.class,
        columns = {
            @ColumnResult(name = "id", type = Long.class),
            @ColumnResult(name = "title", type = String.class),
            @ColumnResult(name = "author_name", type = String.class),
            @ColumnResult(name = "created_on", type = Instant.class)
        }
    )
)
@NamedNativeQuery(
    name = "Post.findRecentNative",
    query = """
        select p.id, p.title, a.name as author_name, p.created_on
        from post p join author a on a.id = p.author_id
        where p.status = 'PUBLISHED'
        order by p.created_on desc
        """,
    resultSetMapping = "PostListItemMapping"
)
@Entity
public class Post { ... }
```

선언적이고 표준적이다. 한 번 정의해 두면 native SQL의 결과가 자동으로 DTO 생성자에 흘러 들어간다.

대신 길다. 매핑 선언이 쿼리만큼 길어지는 경우도 많다. 그리고 *컴파일 타임 검증이 약하다* — 컬럼 이름과 타입이 SQL의 실제 결과와 맞는지는 런타임에서야 확인된다.

쓸 자리는 *반복적으로 호출되는 native SQL을 표준 JPA 방식으로 정리하고 싶을 때*. 회사 컨벤션이 "Hibernate-specific 코드를 가능하면 피한다"인 자리. 피할 자리는 *일회성 native SQL* — 그 자리엔 다음에 볼 `TupleTransformer`가 간결하다.

### `TupleTransformer` — Hibernate 6의 신무기

Hibernate 6부터는 `TupleTransformer<T>`라는 함수형 인터페이스가 도입됐다. 한 줄짜리 람다로 ResultSet의 한 row를 DTO로 변환한다.

```java
List<PostListItemDto> rows = em.createQuery("""
    select p.id, p.title, a.name, p.createdOn
    from Post p join p.author a
    where p.status = :status
    """)
    .setParameter("status", Status.PUBLISHED)
    .unwrap(org.hibernate.query.Query.class)
    .setTupleTransformer((tuple, aliases) ->
        new PostListItemDto(
            (Long) tuple[0],
            (String) tuple[1],
            (String) tuple[2],
            (Instant) tuple[3]
        ))
    .getResultList();
```

Hibernate 5 시절의 `ResultTransformer`가 deprecated되고, 그 자리를 `TupleTransformer`와 `ResultListTransformer` 두 인터페이스가 나눠 받았다. row 단위 변환은 전자, 결과 리스트 전체에 대한 변환(grouping, distinct 등)은 후자다.

쓸 자리는 *동적인 매핑*. 컬럼 타입을 강제 변환해야 하거나 — `BigInteger`를 `Long`으로 — DTO를 만들기 전 약간의 가공이 필요할 때. 그리고 *부모-자식 그룹화*. 잠시 뒤에 보자.

피할 자리는 *컴파일 타임 타입 안전성이 중요한 자리*. `tuple[0]`을 `(Long)`으로 캐스팅하는 코드는 보기에 좋지 않다. 정적 read에는 JPQL constructor expression + Record가 더 깔끔하다.

### Spring Data Interface Projection — 가장 손이 덜 가는 길

Spring Data를 쓰는 자리에서는 *인터페이스만 정의하면* 끝나는 길이 있다.

```java
public interface PostSummary {
    Long getId();
    String getTitle();
    String getAuthorName();
    Instant getCreatedOn();
}

interface PostRepository extends JpaRepository<Post, Long> {
    List<PostSummary> findByStatus(Status status);
}
```

인터페이스의 getter 시그니처를 보고 Spring Data가 *프록시*를 만들어 채워 준다. DTO 클래스를 따로 만들 필요도 없고, JPQL을 적을 필요도 없다. 가장 손이 덜 간다.

여기에는 *Closed projection*과 *Open projection*이 있다. 위의 예제처럼 *엔티티 필드명과 그대로 매핑되는* 게 closed projection이다. Spring Data가 영리하게 SELECT 절을 좁혀서 *필요한 컬럼만* 가져온다.

문제는 open projection이다. SpEL을 쓰는 형태다.

```java
public interface PostSummary {
    @Value("#{target.title + ' (' + target.author.name + ')'}")
    String getDisplay();
}
```

`#{target...}` 안에서 SpEL로 엔티티 필드를 자유롭게 조합할 수 있다는 점에서 매력적으로 보인다. 하지만 *함정이 있다*. Spring Data는 SpEL이 어떤 필드를 참조하는지 분석하지 못한다. 그래서 *안전한 쪽으로 가서 엔티티 전체를 SELECT 한다*. 즉 SELECT *이 되어 버린다. 우리가 *컬럼 네 개만 가져오려고* projection을 도입했는데, open projection을 쓰는 순간 그 효과가 사라진다.

쓸 자리는 *closed projection*만이다. 인터페이스 getter가 엔티티 필드명과 1:1로 매핑되는 단순 read-only 응답. 피할 자리는 *open projection*. 손이 가더라도 JPQL constructor expression + DTO로 가는 편이 낫다. 그리고 한 가지 더, *우리 코드에 open projection이 있는지 한 번 grep해 보자*. `@Value("#{target.`을 찾으면 된다. 있다면 datasource-proxy로 SQL을 한 번 찍어 보자. SELECT 절이 의외로 길게 늘어져 있을 가능성이 높다. 찜찜한 실험이지만, 한 번은 해 봐야 할 검증이다.

### `@Subselect` — 분석 쿼리를 도메인 객체로

마지막으로 가장 흥미로운 도구다. `@Subselect`는 *임의의 SQL을 가상의 read-only 엔티티로 매핑*하는 Hibernate-specific 기능이다.

분석성 화면을 상상해 보자. *각 작성자별 글 수, 최근 글 시각, 평균 댓글 수*를 한 번에 뽑아야 한다. 이 쿼리는 단순 read도 아니고, 어느 엔티티의 자연스러운 view도 아니다. CTE와 window function이 섞여 있다. 매번 JPQL이나 Tuple로 풀자니 *도메인 코드 어디에도 안 어울리는 임시 코드*가 자꾸 늘어난다. 난감하다.

```java
@Entity
@Immutable
@Subselect("""
    select a.id as id,
           a.name as name,
           count(p.id) as post_count,
           max(p.created_on) as last_post_at,
           avg(p.comment_count) as avg_comments
    from author a
    left join post p on p.author_id = a.id
    where p.status = 'PUBLISHED'
    group by a.id, a.name
    """)
@Synchronize({"author", "post"})
public class AuthorStats {
    @Id private Long id;
    private String name;
    private Long postCount;
    private Instant lastPostAt;
    private Double avgComments;
    // getters only
}
```

`AuthorStats`는 가상의 read-only 엔티티다. `@Immutable`이 박혀 있어 *수정해도 DB에 반영되지 않는다*. PersistenceContext에 들어가긴 하지만, dirty checking은 작동하지 않는다. `@Synchronize`는 *이 view가 어떤 테이블의 변경에 영향을 받는지*를 Hibernate에 알려 줘 캐시 무효화에 활용된다.

쓰는 입장에서는 그냥 엔티티다.

```java
List<AuthorStats> top10 = em.createQuery(
    "select a from AuthorStats a order by a.postCount desc", AuthorStats.class)
    .setMaxResults(10)
    .getResultList();
```

자연스럽다. 도메인 코드 안에서 분석 쿼리를 *엔티티처럼* 다룬다. 그러면서도 *수정 가능성은 차단된다*. 그리고 DB의 진짜 view를 만들지 않아도 된다 — DBA와 협업 없이도 애플리케이션 코드만으로 끝낼 수 있다.

쓸 자리는 *반복 호출되는 분석성 쿼리*. 대시보드, 통계 화면, 리포팅용 화면. 피할 자리는 *진짜 view로 만드는 편이 나은 자리*. 여러 서비스가 함께 쓰고, DB 인덱스나 머티리얼라이즈드 뷰의 도움을 받아야 하는 분석은 DB view 또는 materialized view 위에 정식 엔티티를 얹는 편이 맞는다.

도구를 일곱 가지 늘어놓았다. *결국 어느 것을 쓰란 말인가*? 결정 트리를 한 장으로 정리해 보자.

## 어떤 projection을 언제 쓸까 — 결정 트리

복잡해 보이지만, 실은 질문 세 개로 정리된다.

**질문 1: 이 read는 DTO 클래스를 정식으로 정의할 가치가 있는가?**

여러 곳에서 호출된다거나, API 응답의 정식 형태로 굳어질 데이터라면 답은 *그렇다*이다. 일회성 어드민 페이지의 임시 조회라면 *아니다*다.

- **그렇다 → DTO 클래스(가능하면 Record)를 만들자.**
- **아니다 → `Tuple`로 간다.**

**질문 2: SQL은 JPQL로 충분히 표현되는가, 아니면 native SQL이 필요한가?**

window function, CTE, PIVOT, JSON 함수, DB-specific 문법이 필요한가? Hibernate 6의 JPQL은 의외로 많이 커버한다(곧 다시 본다). 그래도 안 되는 자리가 있다.

- **JPQL로 충분 → JPQL constructor expression**, Record DTO. *가장 깔끔한 길*이다.
- **Native가 필요 → `@SqlResultSetMapping` + `@ConstructorResult`** 또는 **`TupleTransformer`**. 회사 컨벤션이 표준 지향이면 전자, Hibernate에 의존해도 무방하면 후자.

**질문 3: Spring Data 환경이고, getter 시그니처가 엔티티 필드와 1:1로 매핑되는가?**

- **그렇다 → Closed Interface Projection**. 가장 손이 덜 간다.
- **SpEL이 끼는 open projection으로 가려고 했다 → 멈추자**. 그 자리는 JPQL constructor expression + DTO로 다시 짜는 편이 낫다.

그리고 결정 트리 밖에 따로 서 있는 한 가지가 `@Subselect`다. *반복 호출되는 분석 쿼리를 도메인 객체로 들고 오고 싶을 때*. 결정 트리의 어떤 분기에서도 답이 나오지 않을 때 — 그러면서 매번 같은 임시 코드를 반복해 짜고 있을 때 — `@Subselect`가 정답일 가능성이 높다.

이 세 질문이 우리의 일상 결정 95%를 처리한다. 나머지 5%는 *동적 SELECT 절이 필요한 자리*인데, 그 자리는 잠시 뒤 Query 선택 절에서 따로 다룬다.

## One-to-Many DTO projection — 부모와 자식을 한 번에

여기까지가 *부모만 가져오는* projection 이야기였다. 그런데 실무에는 부모와 자식 컬렉션을 함께 가져와야 하는 자리가 많다. 글 한 건과 그 글의 댓글 다섯 개를 한 번에 보여주는 상세 페이지 같은 자리다. 이 자리에서 *DTO projection은 어떻게 해야 하는가*?

순진하게 다음과 같이 시도하는 경우가 있다.

```java
@Query("""
    select new com.acme.dto.PostDetailDto(p.id, p.title, c.id, c.content)
    from Post p left join p.comments c
    where p.id = :id
    """)
List<PostDetailDto> findDetail(@Param("id") Long id);
```

이 쿼리의 결과는 *댓글 수만큼 row가 늘어난다*. 댓글이 다섯 개면 같은 글 정보가 다섯 번 반복된다. 그리고 DTO 리스트도 다섯 개로 부풀어 있다. 컨트롤러 응답이 엉뚱해진다. 난감하다.

여기서 우리에게 도구가 셋 있다.

**첫 번째 — `ResultTransformer.distinct()` 또는 그 후속.** Hibernate 5 시절의 `Transformers.distinctRootEntity()`나 `DistinctResultTransformer`로 *부모를 기준으로 distinct* 해 주는 변환기다. 하지만 이건 *엔티티 fetch* 경로에서 동작하는 도구다. DTO projection에서는 부분적으로만 도움이 된다.

**두 번째 — `TupleTransformer.LIST` 패턴 + 메모리 그룹화.** Hibernate 6에서 `TupleTransformer`가 row 단위 변환을 책임지고, 결과 리스트는 메모리에서 직접 그룹화한다.

```java
List<Object[]> rows = em.createQuery("""
    select p.id, p.title, c.id, c.content
    from Post p left join p.comments c
    where p.id = :id
    """, Object[].class)
    .setParameter("id", id)
    .getResultList();

Map<Long, PostDetailDto> grouped = new LinkedHashMap<>();
for (Object[] row : rows) {
    Long postId = (Long) row[0];
    String postTitle = (String) row[1];
    Long commentId = (Long) row[2];
    String commentContent = (String) row[3];

    PostDetailDto dto = grouped.computeIfAbsent(postId,
        k -> new PostDetailDto(k, postTitle, new ArrayList<>()));
    if (commentId != null) {
        dto.comments().add(new CommentDto(commentId, commentContent));
    }
}
return new ArrayList<>(grouped.values());
```

장점은 *한 번의 SQL로 부모-자식을 모두 끌어왔다*는 점이다. N+1이 발생하지 않는다. 단점은 *코드가 길다*. 그리고 row가 댓글 수 × 다른 컬렉션 수만큼 카르테시안 곱으로 부풀 위험이 여전히 있다. *둘 이상의 ToMany 컬렉션*을 한 번에 가져오면 안 된다 — 이건 fetch join에서 본 함정과 같다.

**세 번째 — Hibernate 6.3 이상이라면 `multiset`.** Hibernate가 *JPQL에 multiset을 도입*했다.

```java
@Query("""
    select new com.acme.dto.PostDetailDto(
        p.id,
        p.title,
        multiset(
            select new com.acme.dto.CommentDto(c.id, c.content)
            from p.comments c
        )
    )
    from Post p
    where p.id = :id
    """)
PostDetailDto findDetail(@Param("id") Long id);
```

여기서 `multiset`은 *서브쿼리의 결과를 하나의 컬렉션 값으로 묶어 부모 row에 붙여 준다*. 즉 *카르테시안 곱이 발생하지 않는다*. SQL은 보통 한 번 나가거나, 효율적인 형태로 두 번 나간다. PostgreSQL이라면 `json_agg` 같은 형태로 컴파일된다. 도메인 코드는 깔끔한 JPQL 한 줄, DTO는 정상적인 nested 구조. 가장 이상적인 그림이다.

쓸 자리는 *Hibernate 6.3 이상*이고, *부모 한 건과 자식 컬렉션을 함께 가져오는 read-only 화면*. Blaze-Persistence를 쓰고 있다면 동일한 효과의 `MULTISET`을 더 일찍부터 누릴 수 있다. 회사 환경이 거기까지 못 미친다면 — 두 번째 옵션, 즉 `TupleTransformer.LIST` + 메모리 그룹화로 가는 편이 낫다.

기억해두자. *부모-자식 DTO projection은 카르테시안 곱과의 싸움이다*. 도구는 우리 손에 있고, 어떤 도구를 고를지는 *우리의 Hibernate 버전과 회사의 도구 채택 정책*이 결정한다.

## 그렇다면 query 언어는 무엇으로 짤까

여기까지가 *결과를 어떤 형태로 가져올 것인가*의 이야기였다. 함께 짚어야 할 다른 축이 있다. *그 쿼리를 무엇으로 짤 것인가*. JPQL, HQL, Criteria, Native, jOOQ, Blaze-Persistence — 여기도 도구가 한두 가지가 아니다.

Vlad가 한 줄로 정리한 입장이 있다. 그대로 옮긴다.

> "When it comes to reading data, nothing can beat native SQL because the most commonly-used RDBMS have implemented non-standard data access techniques (window functions, CTE, PIVOT) and the SQL-92 JPA abstraction layer can only focus on common functionalities."

*읽기에 한해서는 native SQL을 이길 것이 없다*. 표준 JPA의 추상화 레이어는 SQL-92 공통 기능에 묶여 있고, 우리가 실제로 쓰는 DB의 강력한 기능 — window function, CTE, PIVOT, JSON 함수, MERGE — 은 비표준이다. 표준의 그물을 빠져 나가는 자리에 진짜 성능이 있다.

그렇다면 무조건 native만 쓸 것인가? 아니다. 도구에는 *쓸 자리*가 있다. 결정 트리를 한 번 더 그리자.

| 도구 | 어디에 | 왜 |
|------|--------|----|
| **JPQL** | 80%의 정적 read/write | 엔티티 graph를 그대로 따라가는 자연스러운 자리. 가장 익숙하고 가장 짧다. |
| **HQL** | JPQL이 못 가는 자리(window function, CTE 등)인데 Hibernate에 묶여도 무방 | JPQL의 superset. Hibernate 6에서는 JPQL과 HQL의 경계가 매우 흐려졌다. |
| **Criteria API** | 동적 쿼리 — Specification 패턴, 검색 필터 다섯 개가 옵션인 자리 | 컴파일 타임 type safety. 단점은 verbose + plan cache miss 위험. |
| **Native SQL** | DB-specific 기능이 필요한 read — window, CTE, PIVOT, JSON, MERGE | 표준이 가린 DB 능력을 직접 부른다. 가장 빠른 read 경로. |
| **jOOQ** | 복잡한 분석/리포트 쿼리, type-safe SQL builder가 필요한 자리 | SQL을 일급으로, 그러나 type-safe로. JPA write + jOOQ read 조합이 강력. |
| **Blaze-Persistence** | Criteria의 진화형이 필요한 동적 쿼리 — LATERAL JOIN, CTE까지 동적으로 | type-safe하면서도 Criteria의 한계를 넘는다. |

이 표를 어떻게 *결정 트리*로 풀어 쓸까? 질문 두 개면 된다.

**질문 1: 이 쿼리는 정적인가, 동적인가?**

- 정적(SELECT/WHERE 절이 코드 작성 시점에 정해진다) → JPQL이 기본, native가 필요한 자리는 native.
- 동적(런타임에 검색 필터의 조합이 바뀐다) → Criteria가 기본. 더 강력한 게 필요하면 Blaze-Persistence나 jOOQ.

**질문 2: 이 쿼리는 단순 entity navigation인가, 복잡한 분석인가?**

- 단순 entity navigation(join이 두세 개, WHERE/ORDER BY 정도) → JPQL.
- 복잡한 분석(window function, CTE, derived table, multi-step aggregation) → Hibernate 6 JPQL의 새 기능으로 풀리는지 먼저 본다. 안 되면 native. 자주 호출되는 분석이면 jOOQ로 정식 채택.

*"동적 쿼리는 Criteria, 정적 read는 JPQL, 복잡 분석은 jOOQ 또는 Native"* — 한 줄짜리 슬로건으로 외워 두자.

그리고 한 가지 더, *조합*이 가능하다는 점을 잊지 말자. JPA를 버리고 jOOQ로 갈아탈 필요 없다. *write와 도메인 모델은 JPA, read 중 복잡한 분석 경로는 jOOQ*로 분리하는 게 Vlad의 일관된 권고다. 두 도구는 같은 데이터소스를 공유하고, 같은 트랜잭션 안에서 함께 쓸 수 있다. 우리가 jOOQ에 매여 *코드 두 벌을 짜는* 문제가 아니라, *적재적소에 도구를 배치하는* 문제다.

ORM Battle 2025의 결론도 같은 방향이다. 단순 read는 JDBC > jOOQ > Hibernate(엔티티), 10~30% 차이. 매핑과 dirty checking이 필요한 write는 Hibernate가 jOOQ + 수동 dirty 추적과 거의 비등. *read는 jOOQ/Native, write는 Hibernate* — 두 줄의 합의다.

## Hibernate 6의 SQM이 가능하게 한 것들

여기서 한 가지를 더 짚자. 위의 결정 트리에서 *"Hibernate 6 JPQL의 새 기능으로 풀리는지 먼저 본다"*는 줄이 있었다. 무엇이 새로 가능해진 것일까?

Hibernate 6의 큰 변화 중 하나가 *Semantic Query Model(SQM)*이라는 새 query parser다. Hibernate 5까지의 query parser는 JPQL을 텍스트 변환에 가깝게 SQL로 옮겼고, 그 과정에서 *정확하지 않은 타입 추론과 SQL 표현의 한계*가 자주 발목을 잡았다. SQM은 그 자리를 다시 짠다. JPQL을 먼저 *의미적 트리*로 컴파일하고, 그 트리에서 SQL을 생성한다. 효과가 여럿이다.

첫째, *JPQL window function*. `row_number()`, `rank()`, `lag()`, `lead()`를 JPQL에서 직접 쓸 수 있다.

```java
@Query("""
    select p.id, p.title,
           row_number() over (partition by p.author.id order by p.createdOn desc) as rn
    from Post p
    """)
List<Object[]> findWithRowNumber();
```

window function이 JPQL에 들어왔다는 것은 — *그동안 native로 내려가야 했던 자리의 상당수가 JPQL로 돌아온다*는 뜻이다.

둘째, *CTE*. JPQL의 `with` 절이 지원된다. 재귀 CTE까지도 가능한 영역으로 들어왔다.

셋째, *derived table*. FROM 절에 서브쿼리를 둘 수 있게 됐다. 그동안 *Criteria도 native도 아니면 풀리지 않던* 형태가 JPQL로 표현 가능해졌다.

넷째, *multiset*. 앞서 One-to-Many DTO projection에서 본 그 도구다. 부모-자식을 카르테시안 곱 없이 한 번에 뽑아 준다.

이 네 가지가 의미하는 바를 한 줄로 정리하면, *"native로 도망쳐야 했던 자리의 상당수가 JPQL로 복귀했다"*는 것이다. 결정 트리의 "JPQL로 가능한가?" 질문의 *대답 범위가 넓어졌다*. 분석 쿼리를 JPQL로 풀어 볼 여유가 생겼고, 그래도 부족하면 native 또는 jOOQ로 넘어간다.

12장에서 이 새 기능들을 더 깊이 살펴본다. 지금 자리에서 기억해두면 좋은 한 줄은 이거다. *Hibernate 5 시절의 "안 되니까 native"가 6에서는 한 번 더 의심해 봐야 할 가정이 됐다*. 우리의 결정 트리를 한 번씩 다시 그려 보자.

## projection은 dirty checking 비용 자체를 차단한다

여기서 한 번 챕터 초입의 이야기로 돌아가자. *엔티티 fetch는 PersistenceContext에 등록되고, 그 등록 자체가 비용이다*. dirty checking, LoadedState 스냅샷, 트랜잭션 끝의 변경 감지, 그리고 유령 UPDATE의 가능성까지. 이 모든 비용이 *읽기 한 번의 그림자*로 따라붙는다.

projection을 쓴다는 것은 무엇인가? *그 그림자를 *원천에서* 차단한다*는 뜻이다. DTO는 엔티티가 아니다. Hibernate가 *PersistenceContext에 등록할 대상으로 보지 않는다*. LoadedState도 만들지 않는다. dirty checking 대상에 끼지 않는다. 트랜잭션 끝에 변경 감지 루프를 도는 객체 목록에서 *애초에 빠져 있다*.

이게 어떤 차이를 만드는가? 트랜잭션 안에서 한 번의 read API가 1,000건의 데이터를 가져온다고 상상해 보자. 엔티티로 가져오면 — 1,000개의 엔티티가 PersistenceContext에 등록되고, 1,000개의 LoadedState 스냅샷이 메모리에 자리잡고, 트랜잭션 끝에 1,000번의 dirty checking이 돈다. DTO로 가져오면 — 1,000개의 DTO 리스트가 메모리에 잠시 자리잡고, 컨트롤러가 응답으로 내보낸 뒤 GC된다. *PersistenceContext는 비어 있다*. 메모리도, CPU도, 시간도 다르다.

그리고 한 가지 더. 엔티티가 PersistenceContext에 1,000개 쌓이면 — 같은 트랜잭션 안의 *다른 작업*도 느려진다. PersistenceContext가 커질수록 *모든 dirty check이 그만큼 느려지기 때문*이다. *1차 캐시는 작아야 한다*는 권고가 여기에 닿는다. 9장에서 배치 처리를 다룰 때 다시 만난다.

기억해두자. *projection은 단순히 컬럼 수를 줄이는 게 아니다. dirty checking 비용 자체를 차단하는 도구다.*

## 그래서 우리는 무엇을 봐야 하는가 — 체크리스트

도구가 많았다. 결정 트리도 두 개나 그렸다. 그런데 우리 코드로 돌아가 *지금 무엇을 봐야 하는가*를 한 번 정리하자.

**체크리스트 ①: 가장 자주 호출되는 read API 5개를 꼽아 보자. 엔티티를 반환하고 있는가, DTO를 반환하고 있는가?**

이건 가장 단순하면서도 효과가 큰 점검이다. 회사 시스템의 traffic 모니터링이나 APM에서 *호출 빈도 top 5*를 뽑아 보자. 그중 GET 메서드, 즉 read API에 해당하는 것들. 거기서 우리 컨트롤러 코드를 따라가 보자. 반환 타입이 무엇인가? `Post` 엔티티인가, `PostListItemDto`인가? `List<Post>`인가, `Page<PostSummary>`인가?

엔티티를 그대로 반환하고 있다면 — 그건 *우리 시스템이 가장 자주 사 오는 그림자*다. 호출 빈도가 높을수록 그림자도 무겁다. *수정 안 할 read는 모두 DTO* 슬로건이 이 한 줄에 정확히 닿는다. top 5 중 단 한 개라도 DTO로 옮기는 작업이, 시스템 전체 비용에 의미 있는 차이를 만든다.

**체크리스트 ②: Open Interface Projection을 쓰는 곳이 있다면, 그것이 SELECT *을 유발하는지 검증했는가?**

코드를 한 번 grep해 보자. `@Value("#{target.`을 찾으면 된다. 매치가 나오면 — 그 자리의 실제 SQL을 datasource-proxy 또는 `org.hibernate.SQL` 로그로 한 번 찍어 보자. SELECT 절이 *우리가 의도한 컬럼만* 들어가 있는지, 아니면 *엔티티 전체*가 들어가 있는지.

찜찜한 실험일 가능성이 높다. 많은 경우 SELECT 절은 엔티티 전체로 늘어져 있다. SpEL이 어떤 필드를 참조하는지 Spring Data가 분석하지 못해서, *안전한 쪽으로 SELECT \**을 택한 결과다. 발견하면 JPQL constructor expression + DTO로 다시 짜는 편이 낫다.

**체크리스트 ③: 분석/리포트성 쿼리에 Native나 jOOQ를 검토해 본 적이 있는가?**

대시보드 화면, 통계 페이지, 월말 리포트 — 이런 자리에 어떤 도구가 들어가 있는지 한 번 따라가 보자. JPQL로 짜려다가 *너무 복잡해져서 결국 메모리에서 가공*하는 코드가 끼어 있는가? Java 스트림으로 group by와 average를 손으로 돌리는 자리가 있는가? 그건 *DB가 1초에 풀 일을 자바가 10초에 푸는* 자리일 가능성이 높다.

window function이나 CTE가 필요한 자리라면 — Hibernate 6 JPQL로 풀리는지 한 번 보고, 안 되면 native, 자주 호출되면 jOOQ로 정식 채택해 보자. `@Subselect`로 read-only 가상 엔티티를 만드는 것도 강력한 카드다. 분석 쿼리를 *임시 코드에 잠그지 말고 도메인 객체로* 들고 오자.

이 세 가지 체크가 끝나면, 우리는 한 가지를 깨닫게 된다. *우리 시스템에서 fetch를 줄여 얻을 수 있는 이득의 상당 부분은 사실 projection을 통해 얻는 이득이었다*. N+1을 해결하는 챕터를 한 권 통째로 썼지만, *그 옆 챕터의 projection 도입 한 번이 더 큰 효과를 낼 수도 있다*. 두 축이 따로 노는 게 아니라 함께 묶인다는 점을, 우리 코드의 30초 grep으로 다시 확인해 보자.

## 마무리 — 잊지 말자

이 장의 출발점은 단순한 관찰 하나였다. *네 개의 컬럼을 보여주려고 마흔 개를 가져왔다*. fetch 수를 줄이는 데까지만 신경 쓰면, *한 row의 무게*는 그대로 남는다. SQL 카운트가 1로 줄어든 우리의 코드가 여전히 느릴 수 있는 이유다.

슬로건 한 줄로 다시 못 박는다. *수정 안 할 read는 모두 DTO.* 이 한 줄을 받아들이는 순간, 우리는 dirty checking 비용을 차단하는 권리를 갖는다. PersistenceContext에 들어가지 않는 데이터는 LoadedState 스냅샷도, 변경 감지 루프도, 유령 UPDATE의 위험도 가져오지 않는다. *읽기 한 번의 그림자가 사라진다*.

도구는 일곱 가지였다. JPQL constructor expression(가능하면 Record와 함께)이 가장 깔끔한 기본형. `Tuple`은 일회성 자리. `@SqlResultSetMapping` + `@ConstructorResult`는 native SQL과 DTO를 잇는 표준 다리. `TupleTransformer`는 Hibernate 6의 신무기 — 동적 매핑과 부모-자식 그룹화에 강하다. Spring Data Interface Projection은 closed projection만 쓰자, open projection은 SELECT *의 함정. `@Subselect`는 분석 쿼리를 도메인으로 들고 오는 길.

부모-자식을 한 번에 가져오는 자리는 카르테시안 곱과의 싸움이다. Hibernate 6.3 이상이라면 JPQL `multiset`, Blaze-Persistence라면 `MULTISET`, 아니면 `TupleTransformer.LIST` + 메모리 그룹화로 풀자. 둘 이상의 ToMany 컬렉션을 한 번에 끌고 오는 자리는 — 4장의 fetch join 함정과 같은 함정이다. 잊지 말자.

쿼리 언어 선택은 슬로건 한 줄로 정리됐다. *동적 쿼리는 Criteria, 정적 read는 JPQL, 복잡 분석은 jOOQ 또는 Native.* Hibernate 6의 SQM 덕분에 JPQL이 풀 수 있는 영역이 넓어졌다 — window function, CTE, derived table, multiset. 결정 트리의 "JPQL로 가능한가?" 질문의 답이 5년 전과 다르다. 한 번씩 다시 그려 보자. 그래도 부족하면 native, 자주 호출되면 jOOQ로 정식 분리. JPA를 버릴 필요는 없다. *write는 JPA, read 중 복잡한 분석은 jOOQ*가 합의된 그림이다.

마지막으로 우리 코드로 돌아가는 30초의 작업을 적어 둔다. 그 30초가 책 한 권보다 우리 시스템을 더 잘 안다.

### 내 코드 체크리스트 3개

- 가장 자주 호출되는 read API 5개를 꼽아 보자. 그중 엔티티를 반환하는 것이 몇 개인가? 그 자리들이 *수정 안 할 read*라면, DTO로 옮길 후보다.
- 코드에 `@Value("#{target.`을 grep해 보자. Open Interface Projection이 있다면 datasource-proxy로 SELECT 절을 한 번 찍어, *우리가 의도한 컬럼만* 들어가는지 검증하자. 안 그렇다면 JPQL constructor expression + DTO로 다시 짜는 편이 낫다.
- 대시보드·통계·리포트 화면의 쿼리를 한 번 따라가 보자. 메모리에서 group by와 average를 손으로 돌리는 자리가 있는가? 그렇다면 Hibernate 6 JPQL의 window function/CTE로 풀리는지 먼저 보고, 안 되면 native, 자주 호출되면 jOOQ나 `@Subselect`로 정식 채택을 검토해 보자.

다음 6장에서는 *트랜잭션 경계*로 들어간다. `@Transactional`을 붙이면 끝일까? 그리고 컨트롤러에서 lazy를 호출했는데 동작하는 이 환경은 정말 정상인가? — 이 챕터의 DTO projection이 그 다음 장 OSIV의 타협안에서 어떻게 다시 등장하는지, 함께 살펴보자.
