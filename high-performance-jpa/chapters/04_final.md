# 4장. 쿼리 한 줄이 백 번 나가는 이유 — N+1을 다시 본다

상황을 하나 떠올려보자. 어느 월요일 아침, 새로 합류한 후배가 자랑스럽게 게시판 목록 API를 보여준다. 코드는 깔끔하다. `postRepository.findAll(pageable)` 한 줄로 페이지 처리도 되고, 응답으로는 작성자 이름과 댓글 수까지 친절하게 내려간다. 로컬 환경에서 동작은 잘 된다. 평균 응답시간은 30밀리초. 후배는 만족스러운 얼굴이다.

그 코드는 운영에 올라가자마자 무너졌다. CPU 그래프는 평온한데 DB 커넥션 풀은 매분 가득 찬다. 응답시간은 어떤 요청은 50밀리초, 어떤 요청은 4초. 슬로우 쿼리 로그를 켜고 살펴봐도 잡히는 쿼리가 없다. 모든 쿼리가 1밀리초 안에 끝나고 있기 때문이다. 그런데 한 요청당 SQL이 두 자리 수, 세 자리 수로 나가고 있었다. 익숙한 풍경이다. 우리는 이걸 N+1이라고 부른다.

여기까지 읽고 "아, N+1. 그건 안다"라고 생각했다면 한 번 더 묻고 싶다. 안다는 그 말은 무엇을 안다는 뜻일까. 정의를 안다는 뜻일까, 잡는 방법을 안다는 뜻일까, 아니면 우리 코드에는 없다는 뜻일까. 솔직히 말해서, 마지막 명제는 거의 거짓이다. N+1은 누구나 알지만, 우리 코드에는 여전히 있다. 그 모순을 풀어보는 것이 이 장의 일이다.

## N+1이라는 이름의 함정

N+1은 데이터 접근 프레임워크가 "한 번의 주 쿼리로 가져올 수 있었던 같은 데이터를, N개의 추가 SQL로 다시 가져오는 현상"이다. Vlad Mihalcea가 즐겨 인용하는 정의다. 단순하게 보면 "쿼리를 1번에 묶을 수 있는데 N+1번 나간다"는 이야기인데, 이 정의의 진짜 무서움은 따로 있다.

생각해보자. 추가로 나가는 N개의 쿼리는 *어떤 쿼리*일까. 대체로 `select * from author where id = ?` 같은 단순 PK 조회다. 인덱스를 정확히 타고, 캐시 히트도 잘 일어나고, 1밀리초도 안 걸린다. 슬로우 쿼리 로그의 임계값을 100밀리초로 잡아 두었다면 단 한 줄도 잡히지 않는다. 그러니까 N+1은 "느린 쿼리 한 개"가 아니라 "빠른 쿼리 수십, 수백 개"의 문제다. 그래서 잡기 어렵다.

비유를 하나 들어 보자. 회사에서 멀리 떨어진 자료실에 자료가 있다고 해보자. 한 번 가서 한 더미를 들고 오면 일이 끝난다. 그런데 우리는 자료실에 한 번 가서 종이 한 장을 들고 오고, 다시 자료실에 가서 한 장을 들고 오고, 또 한 번 다녀온다. 한 번 다녀오는 데 30초밖에 안 걸리지만, 100번 다녀오면 50분이다. 같은 이야기다. 라운드트립이 비싸지, 한 번의 fetch가 비싼 게 아니다.

DB도 마찬가지다. 한 쿼리의 실행 시간이 1밀리초라도, 거기에 네트워크 왕복과 트랜잭션·커넥션 점유가 곱해진다. 100개의 N+1 쿼리는 100번의 왕복이고, 그 시간 동안 커넥션은 다른 요청에게 양보되지 않는다. 그래서 평소엔 멀쩡하다가, 동시 요청이 늘어나는 순간 풀이 차오르고 응답시간이 무너진다. 이 부분이 1장에서 본 *라운드트립이 진짜 비용이다*라는 명제의 가장 직관적인 사례다.

여기서 잠깐 멈추자. 이 정의를 받아들이고 나면 자기 코드를 보는 눈이 바뀐다. *우리 코드의 가장 큰 list API는 한 요청에 SQL이 몇 개나 나가는가.* 모른다면, 모르고 있다는 사실 자체가 출발점이다. 슬로우 쿼리 로그가 깨끗하다는 것은 위안이 되지 않는다. 깨끗할수록 더 의심해야 한다.

## 어디서 N+1이 자라는가

그래서 정확히 어디서 발생할까. 두 가지 자리만 외워두면 거의 다 잡는다.

### 첫 번째 자리: `@ManyToOne`과 `@OneToOne`의 기본값

JPA 명세를 한 줄 읽어 보자. `@ManyToOne`의 기본 `fetch` 속성은 `FetchType.EAGER`다. `@OneToOne`도 마찬가지다. 즉 아무것도 안 쓰면 EAGER다. 그런데 `@ManyToOne`을 안 쓰는 엔티티가 흔할까? 거의 없다. 작성자가 있는 글, 부서가 있는 직원, 상품 카테고리가 있는 상품 — 도메인 모델은 ToOne 관계로 가득하다.

EAGER가 무슨 짓을 하는지 한 번 그려보자. JPQL을 던지면 Hibernate는 본 쿼리를 만든 뒤, EAGER 관계마다 *별도의* secondary select를 발사한다. JOIN을 자동으로 깔아주지도 않는다. 그 결과 글 100개를 fetch하면 작성자 조회 SQL이 100번 추가로 나간다. 잡으려 든다고 잡히는 것도 아니다 — 글 목록 SQL은 정상이고, 작성자 SQL 한 건도 정상이다. 다만 한 페이지 요청에 SQL이 101번 나간다는 사실만이 문제다.

그런데도 우리는 왜 EAGER를 못 떼어낼까. 답은 단순하다. *기본값이라서*. 어노테이션에 `fetch = LAZY`를 굳이 안 쓴 코드가 너무 많다. 입사 첫 주에 짠 엔티티에는 모두 `@ManyToOne` 한 줄로만 끝나 있다. 그 한 줄이 묵묵히 EAGER로 동작하고 있는 것이다. 끔찍한 일이다.

Vlad는 이걸 "code smell"이라고 부른다. 그의 말 한 줄을 그대로 옮겨 두자. *"EAGER 페치는 거의 항상 코드 스멜이다. 한 번 EAGER로 정해 두면 모든 use case가 그 비용을 같이 치른다. LAZY는 query 시점에 끌어올릴 수 있지만, EAGER는 query에서 다시 LAZY로 내릴 수 없다."* 이 비대칭이 핵심이다. 전역 fetch plan에 묶이는 비용은 전 use case가 분담한다. 어떤 use case는 작성자 정보가 필요하고, 어떤 use case는 필요 없는데, 일단 EAGER이면 모두에게 부담을 떠넘긴다.

### 두 번째 자리: LAZY 컬렉션을 view·stream에서 이터레이트

좋다, 그래서 `fetch = LAZY`를 명시적으로 붙였다고 하자. 이제 안전한가? 안타깝게도, 새로운 함정이 기다린다. 컬렉션을 LAZY로 두면 fetch 시점이 *그 컬렉션에 접근하는 순간*으로 미뤄진다. 서비스에서 글 목록을 가져온 뒤 컨트롤러에서 각 글의 댓글을 순회하면 어떤 일이 벌어질까. 글마다 한 번씩 `select * from comment where post_id = ?`가 발사된다. 영락없는 N+1이다.

특히 OSIV(open-in-view)가 켜져 있는 환경이면, 트랜잭션 경계가 컨트롤러까지 늘어진다. 그래서 *view에서 lazy를 호출해도 에러가 안 난다*. 동작은 한다. 그런데 잡힐 듯 잡히지 않는 N+1이 계속 자란다. velog의 `@gwanghyeonkim`, `@sdsd0908` 같은 한국 개발자들이 잇따라 정리한 게시판 장애 사례를 보면, 거의 모두 같은 줄기를 따른다. 페이지네이션 + ToMany + OSIV 조합으로 시작해, 메모리가 부풀고, 최종적으로 DB가 먼저 OOM을 내고 죽는다. 한 번이라도 운영에서 그 풍경을 본 적이 있다면, OSIV가 왜 "있어서는 안 되는 문제의 해결책"인지 단번에 이해된다. (이 비판은 6장에서 본격적으로 다룬다.)

이 두 자리만 머릿속에 박아두자. *기본값 EAGER로 묶인 `@ManyToOne`/`@OneToOne`*, 그리고 *컨트롤러나 stream에서 이터레이트되는 LAZY 컬렉션*. 우리 코드의 N+1은 거의 항상 이 둘 중 하나, 혹은 둘 다에서 나온다.

## 권장 순서가 있다 — 그냥 JOIN FETCH가 답이 아니다

N+1을 잡는 방법은 여러 가지다. 그런데 한국 개발자 커뮤니티에서 가장 흔히 보는 답이 한 가지로 굳어져 있다. "JOIN FETCH 써라." 틀린 말은 아니다. 그러나 *언제* 써야 하고, *언제* 다른 도구로 가야 하는지의 지도 없이 망치만 든 채 모든 못을 두드리면 새로운 사고가 난다. 그래서 권장 순서를 한 번 정리해두자. Vlad가 자기 책과 블로그에서 일관되게 권하는 순서가 다음 네 가지다.

### ① JOIN FETCH (JPQL / Criteria)

가장 단순하다. 가장 직접적이다.

```java
List<Post> posts = em.createQuery("""
    select distinct p
    from Post p
    left join fetch p.author
    where p.status = :status
    """, Post.class)
    .setParameter("status", "PUBLISHED")
    .getResultList();
```

`join fetch`는 SQL의 INNER/LEFT JOIN으로 풀리되, 부모 row와 자식 row를 한 result set으로 끌어와 영속성 컨텍스트에 같이 등록한다. ToOne 관계라면 거의 이대로 두면 된다. 한 번의 쿼리로 끝난다. 단순하고 명료하다.

그런데 *컬렉션*(ToMany)에 fetch join을 걸 때부터 이야기가 달라진다. 한 부모에 자식이 5개 있으면 result set의 row가 5배로 뻥튀기된다. 자식이 100개면 100배. 그리고 거기에 페이지네이션을 더하면 — 이 조합이 바로 책의 본 챕터에서 가장 길게 다룰 자리인 HHH000104의 세계다. 그 이야기는 곧 한 절을 따로 떼어 풀어보자.

### ② `@EntityGraph` (fetchgraph vs loadgraph)

`JOIN FETCH`는 JPQL을 직접 쓰니까 강력하지만, Spring Data Repository의 그 깔끔한 메서드 이름과 잘 안 어울린다. 그래서 등장한 게 `@EntityGraph`다.

```java
public interface PostRepository extends JpaRepository<Post, Long> {

    @EntityGraph(attributePaths = {"author", "category"})
    List<Post> findByStatus(String status);
}
```

선언적으로 "이 쿼리에서는 author와 category까지 즉시 가져온다"라고 표시한다. 코드가 깔끔하다. 그리고 한 가지 더, 알아두면 좋은 디테일이 있다.

`@EntityGraph`에는 두 가지 *모드*가 있다.

- `javax.persistence.fetchgraph` — 그래프에 명시한 노드만 EAGER, 나머지는 명시한 fetch type을 무시하고 *강제로 LAZY*.
- `javax.persistence.loadgraph` — 그래프에 명시한 노드는 EAGER, 그래프 *밖*은 매핑된 기본 동작 유지(즉 EAGER이면 EAGER).

차이가 무엇을 뜻하는가. 만약 코드에 잔여 EAGER가 남아 있고 그 비용을 일시적으로라도 끊고 싶다면 `fetchgraph`가 칼처럼 잘 작동한다. 한 쿼리만은 *이 그래프에 있는 것 빼고 전부 LAZY*로 동작한다. Vlad가 *"Overriding FetchType.EAGER with fetchgraph"* 글에서 강조하는 활용법이다. 반대로 *기본값을 살리고 추가만 가져오고 싶다*면 `loadgraph`. 한국어 자료에는 두 모드를 같은 것으로 설명하는 경우가 적지 않은데, 차이가 분명히 존재하니 기억해두자.

```java
@EntityGraph(attributePaths = {"author"}, type = EntityGraphType.FETCH)
List<Post> findAllProjectedBy();
```

기본 모드는 보통 `LOAD`다. EAGER 잔재를 한 query에서 끊고 싶을 때 `FETCH`를 명시적으로 쓰자.

### ③ `@BatchSize` + `hibernate.default_batch_fetch_size`

자, 이제 한국 실무에서 가장 자주 마주치는 무기다. 사실상 한국 백엔드 개발자들이 가장 사랑하는 N+1 해법이라고 해도 과언이 아니다.

`@BatchSize`는 LAZY를 *유지하면서* N+1을 막는다. 어떻게? LAZY 트리거가 발생할 때, 즉시 N번의 select를 발사하는 대신 *해당 영속성 컨텍스트에 등록된 같은 타입의 프록시를 모아서 IN 절 한 방으로 묶는다*. 글 100개의 작성자를 lazy load하면 작성자 조회가 100번 나가는 것이 아니라, `select * from author where id in (?, ?, ?, ...)` 한 번으로 끝난다.

설정은 두 방향이 있다.

```java
@OneToMany(mappedBy = "post", fetch = FetchType.LAZY)
@BatchSize(size = 200)
private List<Comment> comments;
```

또는 글로벌 옵션 한 줄.

```properties
hibernate.default_batch_fetch_size=200
```

권장값은 어느 정도일까. velog의 `@joonghyun` 같은 한국 글에서 "100~1000 사이"라는 가이드를 만나게 된다. Vlad 본인은 "default_batch_fetch_size를 켜면 거의 모든 곳에서 안전한 디폴트가 된다"고 말한다. 한 가지 주의할 것은, MS SQL Server나 Oracle의 일부 버전은 IN 절 파라미터 개수에 1000 같은 상한이 있다는 점이다. 그 한계를 넘는 batch size를 잡으면 오히려 쿼리가 분할되거나 에러가 난다. 우리 DB가 무엇인지에 따라 *상한선 안에서 가능한 크게*가 정답이다.

이 옵션이 한국 실무에서 사실상 합의로 굳어진 데에는 이유가 있다. 첫째, *전역 설정 한 줄로 어디서든 작동*한다. 코드를 일일이 손대지 않아도 효과가 난다. 둘째, *LAZY 의미를 유지*한다 — 진짜로 필요한 곳에서만 fetch가 일어난다. 셋째, *컬렉션 페이지네이션과도 충돌이 없다*. 다음 절의 HHH000104 함정을 자연스럽게 피해 간다. 결국 한국 백엔드 진영에서 다음 슬로건이 굳었다:

> **ToOne만 fetch join, ToMany는 batch_size 100~1000.**

이 한 줄을 외워두자. velog의 `@hyojhand`, GitHub Pages의 `cheese10yun.github.io` 등 여러 자료가 동일한 결론에 수렴한다. 우리 코드에 이 디폴트가 없다면, 지금 `application.yml`에 한 줄 더 넣는 것만으로 운영의 풍경이 바뀐다.

### ④ `@Fetch(FetchMode.SUBSELECT)`

마지막 카드다. 컬렉션 fetch를 *자식 select 단 한 방*으로 묶는다.

```java
@OneToMany(mappedBy = "post", fetch = FetchType.LAZY)
@Fetch(FetchMode.SUBSELECT)
private List<Comment> comments;
```

부모를 select한 *그 쿼리*를 subquery로 다시 써서, 그 PK 집합 전체를 한 번에 IN 절로 풀어 자식을 들고 온다. 효과는 강력하다. N+1이 1+1이 된다. 그런데 권장 순서의 마지막에 둔 데에는 이유가 있다.

`SUBSELECT`는 *해당 컬렉션을 사용하는 모든 use case에 영향을 미친다*. 어떤 시나리오에선 자식이 5개씩만 필요하고, 어떤 시나리오에선 부모만 100건 골라 자식엔 손도 안 대고 싶은데, 한 번 SUBSELECT로 매핑해 두면 모든 use case가 그 자식 전체를 끌어 올 위험을 떠안는다. 그래서 *마지막 카드*다. 다른 도구로 안 풀릴 때, 그리고 그 컬렉션의 사용 패턴이 항상 *부모 결과 전체에 대한 자식 전체*라는 확신이 있을 때만 꺼내자.

### 결정 트리, 한 번에 정리

권장 순서를 짧은 결정 트리로 정리해두자.

| 관계 | 페이지네이션? | 1순위 | 비고 |
|------|---------------|-------|------|
| ToOne (`@ManyToOne`, `@OneToOne`) | 무관 | `JOIN FETCH` 또는 `@EntityGraph` | EAGER는 코드 스멜, 명시적 LAZY + per-query fetch |
| ToMany 컬렉션 | 아니오 | `JOIN FETCH(distinct)` 또는 `@EntityGraph` | 결과 row 뻥튀기는 `distinct`로 흡수 |
| ToMany 컬렉션 | 예 | `@BatchSize` / `default_batch_fetch_size` | 다음 절의 HHH000104 회피 |
| ToMany 컬렉션 (use case 전부에서 전체 사용) | 무관 | `@Fetch(FetchMode.SUBSELECT)` | 마지막 카드 |

이 표 한 장을 머릿속에 두면, *N+1을 잡자*는 막연한 결심이 *어디서 어떤 도구를 꺼낸다*는 구체적인 손동작이 된다.

## HHH000104 — 컬렉션 fetch와 페이지네이션이 만나면

여기가 N+1 챕터에서 가장 진하게 풀어야 할 자리다. 한국 백엔드 개발자가 운영 장애로 이 함정을 한 번씩 다 겪고 지나간다 해도 과언이 아니기 때문이다.

상황을 가정해보자. 게시판이 있다. 글 목록 페이지에서는 한 번에 글 10개를 보여주고, 각 글에 달린 댓글 수를 함께 노출한다. 글 한 개에 보통 댓글이 5~50개쯤 달린다. 페이지 번호도 있다. 직관적으로 짠 JPQL은 대체로 이렇게 생긴다.

```java
List<Post> posts = em.createQuery("""
    select distinct p
    from Post p
    left join fetch p.comments
    order by p.createdOn desc
    """, Post.class)
    .setFirstResult(0)
    .setMaxResults(10)
    .getResultList();
```

`fetch join`으로 댓글까지 한 방에. `setMaxResults(10)`으로 10개씩. 깔끔해 보인다. 그런데 로그에 한 줄이 떠 있다.

```
WARN o.h.h.internal.ast.QueryTranslatorImpl :
HHH000104: firstResult/maxResults specified with collection fetch; applying in memory!
```

이 한 줄을 보고 등에 식은땀이 흘러야 한다. *applying in memory*. Hibernate가 SQL의 LIMIT/OFFSET을 *적용하지 못하고* 전 결과를 메모리로 끌고 와 거기서 페이지를 자른다는 뜻이다. 왜 그럴까?

생각해보자. `Post`와 `Comment`를 LEFT JOIN하면 row가 어떻게 부풀어 오를까. 글 한 개에 댓글이 5개라면, JOIN 결과는 5개의 row다. 글 10개에 댓글이 평균 20개씩이면 200개의 row. 그 상태로 `LIMIT 10`을 SQL에 박으면 무엇이 잘릴까. 글 단위가 아니라 *row 단위*로 10개가 잘린다. 운이 나쁘면 글 1개의 댓글 10개만 들고 끝난다. 글 10개가 안 온다.

Hibernate는 이걸 알고 있다. SQL에 안전하게 LIMIT을 박을 수가 없으니, *전 결과를 메모리로 가져온 뒤* 그 위에서 부모 PK 기준으로 페이지를 자른다. 동작은 한다. 그런데 동작만 한다. 글 1000개의 댓글이 평균 50개씩 달려 있는 게시판이라면, 한 페이지 요청 한 번에 5만 row를 메모리에 들고 온다. 평소엔 잘 동작한다. 트래픽이 늘어나는 어느 순간, 힙이 차오르고, GC가 멈추지 않다가, OOM이 난다. 끔찍한 일이다.

velog의 `@gwanghyeonkim`이 정리한 사례, `@sdsd0908`의 글, OKKY의 여러 질문 스레드, `cheese10yun.github.io`의 가이드 — 한국 커뮤니티의 이 문제 사례는 거의 같은 패턴을 따른다. 처음엔 fetch join + 페이지네이션으로 시작한다. 운영에 올라간다. 평온하게 며칠 돈다. 어느 날 OOM. 로그를 보면 HHH000104 경고가 줄지어 있었다. *그 경고를 봤어야 했다*는 후회만 남는다.

이 사례를 좀 더 진하게 그려보자. 어떤 팀이 게시판을 만든다. 글 한 개당 댓글이 평균 30개, 인기 글에는 300개. 글 1만 개를 운영한다. QA에서는 글 50개로 테스트했고, 한 페이지에 글 10개씩 무리 없이 잘 나왔다. 응답시간도 80밀리초. 합격. 운영에 올라간다. 첫째 주는 평온하다. 둘째 주, 인기글 게시판이 메인 노출되면서 트래픽이 들이친다. 한 페이지 요청 한 번이 메모리에 평균 30 × 1000 = 3만 row를 끌고 온다. 동시 요청 50개면 150만 row. 힙이 차오른다. GC가 풀가동된다. 응답시간이 80밀리초에서 4초로 늘어난다. 알람이 울린다. 새벽 3시. 누가 봐도 N+1과는 다른 풍경이다 — *느린 쿼리가 잡힌다*. 그런데 쿼리 자체는 빠르다. 메모리에서 페이지를 자르는 단계가 느릴 뿐이다. 진짜 원인을 찾는 데 한나절이 걸린다. 알고 보니 HHH000104. *경고는 첫날부터 뜨고 있었다*. 그저 누구도 안 봤다. 끔찍한 일이다.

그래서 어떻게 해야 할까. Vlad의 정석은 *2-query 패턴*이다. 한 쿼리로 풀려고 하지 말자. 두 쿼리로 풀자.

```java
// 1) 부모 PK만 페이지로 뽑는다 — 컬렉션 join 없이 깨끗하게.
List<Long> postIds = em.createQuery("""
    select p.id
    from Post p
    where p.status = :status
    order by p.createdOn desc
    """, Long.class)
    .setParameter("status", "PUBLISHED")
    .setFirstResult(0)
    .setMaxResults(10)
    .getResultList();

// 2) 그 PK를 IN 절로 한 번에 join fetch.
List<Post> posts = em.createQuery("""
    select distinct p
    from Post p
    left join fetch p.comments
    where p.id in :ids
    order by p.createdOn desc
    """, Post.class)
    .setParameter("ids", postIds)
    .getResultList();
```

첫 쿼리는 *부모만, PK만* 뽑는다. JOIN이 없으니 row 뻥튀기가 없다. SQL의 LIMIT/OFFSET이 정확히 글 10개에 적용된다. 두 번째 쿼리는 그 PK 10개를 IN 절로 받아 자식까지 한 번에 끌고 온다. `distinct`로 부모 row의 중복도 흡수한다. 결과는 정확히 글 10개 + 그 각각의 댓글들. 메모리에 5만 row가 올라오지 않는다.

이게 *공식 정석*이다. 그리고 한국 커뮤니티가 이 정석을 한 번 더 단순화한 패턴이 위에서 외워둔 슬로건이다.

> **ToOne만 fetch join, ToMany는 `default_batch_fetch_size`로 풀자.**

이 패턴이 한국에서 사실상 *컬렉션 페이지네이션의 합의된 해법*이 된 데에는 명료한 이유가 있다. 첫째, 코드가 단순하다. 한 쿼리로 끝난다. 둘째, 2-query 패턴의 모든 이점을 다 누린다 — fetch join은 부모만 LIMIT 안전하게 쓸 수 있는 ToOne에만 걸고, ToMany는 batch_size로 lazy 트리거 시점에 IN 절로 묶는다. 셋째, 잊어버려도 글로벌 옵션이 잡아준다.

코드로 하나만 더 보자.

```java
// 글로벌 옵션
// application.yml
//   hibernate:
//     default_batch_fetch_size: 200

// JPQL — ToMany엔 fetch join 안 건다.
List<Post> posts = em.createQuery("""
    select p
    from Post p
    left join fetch p.author
    left join fetch p.category
    where p.status = :status
    order by p.createdOn desc
    """, Post.class)
    .setParameter("status", "PUBLISHED")
    .setFirstResult(0)
    .setMaxResults(10)
    .getResultList();

// 컨트롤러나 서비스에서 댓글에 처음 접근하는 순간,
// Hibernate가 글 10개의 댓글을 batch_size=200 IN 절로 한 번에 풀어 온다.
for (Post p : posts) {
    int commentCount = p.getComments().size();
    // ...
}
```

깔끔하다. 그리고 HHH000104 경고는 더 이상 안 뜬다. 글 목록 한 페이지의 SQL은 본 쿼리 1번 + 댓글 IN 절 fetch 1번. 총 2번. 100명이 동시에 들어와도 200번이지, 100×N번이 아니다. 운영의 풍경이 바뀐다.

여기서 한 가지를 더 짚어두고 싶다. 이 패턴을 머리로 알고 있어도, *기존에 동작하던 코드를 고칠 때* 흔히 빠지는 함정이 있다. fetch join을 그냥 떼어 내고 batch_size만 거는 것으로는 모자라다. 코드 어딘가에서 컬렉션을 stream으로 처리하면서 *부모 외부에서 자식을 호출*하는 흐름이 있다면, 그 호출이 트랜잭션 안에서 일어나는지부터 확인하자. 트랜잭션이 끝난 뒤 컨트롤러에서 lazy를 호출하는 패턴은 OSIV 의존이다. 6장에서 자세히 보겠지만, 그 의존이 또 다른 문제의 시작이다.

## EAGER이 코드 스멜인 이유, 한 번 더

위에서 잠깐 언급했지만, 이 자리에서 좀 더 진하게 풀어두고 싶다. *왜 EAGER이 그 자체로 코드 스멜인가.* "성능 문제"라는 짧은 답으로는 부족하다. 본질을 한 번 더 들여다보자.

EAGER는 *전역적 결정*이다. 엔티티 정의 한 줄에 EAGER이 박히면, 그 관계는 *어떤 쿼리에서든* EAGER로 동작한다. 어떤 use case는 작성자가 정말 필요하다 — list API. 어떤 use case는 작성자 따위 안 본다 — 글 삭제 API, 글 상태만 바꾸는 API, 글 검색 결과 카운트 API. 그런데 EAGER이면 *모두*가 작성자를 들고 온다. 비용은 누구에게 부과되는가? 안 쓰는 곳을 포함한 모두에게 부과된다.

이걸 LAZY로 바꾸면 그림이 뒤집힌다. 기본은 *안 가져온다*. 그리고 필요할 때, 즉 list API에서 `JOIN FETCH`나 `@EntityGraph`로 *그 쿼리에서만* 끌어올린다. 비용은 *그 쿼리만* 치른다. *전역 LAZY, 쿼리별 EAGER*. Vlad의 슬로건 한 줄로 정리하면 다음과 같다.

> **LAZY globally, JOIN FETCH per query.**

이 슬로건의 의미는 단지 fetch type 디폴트의 문제가 아니다. *결정을 어디서 내릴 것인가*의 문제다. fetch plan을 매핑 단계에서 결정하면, 그 결정은 모든 use case에 강제된다. fetch plan을 쿼리 단계에서 결정하면, use case마다 자기 결정을 내릴 수 있다. 같은 엔티티에 다섯 가지 사용 시나리오가 있다면, 다섯 가지 fetch 계획이 가능하다. 매핑에 EAGER을 박는 순간 그 자유를 잃는다.

여기에 한 가지 비대칭이 더 얹힌다. LAZY는 query에서 끌어올릴 수 있다. EAGER는 query에서 다시 LAZY로 내릴 수 없다. 즉 *전역 LAZY + 쿼리별 fetch*는 항상 가능한 조합이지만, *전역 EAGER + 쿼리별 lazy*는 가능하지 않다. 비대칭이 비교를 끝낸다.

EAGER이 빚는 사고를 한 토막 더 그려보자. 어떤 팀의 `Order` 엔티티에는 `@ManyToOne` 관계가 다섯 개 박혀 있다 — `Customer`, `ShippingAddress`, `BillingAddress`, `PaymentMethod`, `Coupon`. 모두 기본값. 즉 모두 EAGER. 주문 한 건을 조회하는 API는 잘 동작한다. 그런데 *주문 통계* API가 추가된다. 지난 한 달의 주문을 1000건씩 페이지로 보여주는 화면. JPQL을 직관적으로 짜면 `select o from Order o where o.createdAt > :from`. 동작은 한다. 그런데 한 페이지 요청에 SQL이 6번이 아니라 5001번 나간다 — 본 쿼리 1번 + 다섯 관계 × 1000건. 통계 화면에는 고객 이름만 한 번 보여주면 되는데, 우리는 결제수단과 쿠폰까지 한 줄씩 끌고 왔다. 다섯 관계 모두에게 사례가 분담된 셈이다. EAGER을 한 곳에서 떼어내려면 매핑을 바꿔야 한다. 그런데 매핑을 바꾸면 *주문 한 건 조회* API의 풍경도 같이 바뀐다 — 그쪽엔 의도된 fetch가 있었으니까. 이런 상황을 보면 EAGER이 왜 *코드 스멜*인지 단번에 이해된다. 한 곳의 결정이 모든 곳을 인질로 잡는다.

자, 그럼 우리가 해야 할 일은 한 가지다. *모든 `@ManyToOne`과 `@OneToOne`에 `fetch = LAZY`를 명시적으로 박자*. 기본값이라서 안 쓴 게 아니라, 명시적으로 쓰자. 명시는 의도를 드러낸다. 명시는 코드 리뷰에서 잡힌다. 명시는 미래의 후배가 "왜 LAZY가 안 붙어 있지?" 묻기 전에 답이 된다.

```java
@Entity
public class Post {

    @Id @GeneratedValue(strategy = SEQUENCE)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)   // 명시
    @JoinColumn(name = "author_id")
    private Author author;

    @ManyToOne(fetch = FetchType.LAZY)   // 명시
    @JoinColumn(name = "category_id")
    private Category category;

    // ...
}
```

이 한 줄을 빠뜨리지 않는 코드 컨벤션을 두는 편이 낫다. 신규 프로젝트라면 더 그렇다. 그리고 한 가지 더 — bytecode enhancement를 켜 두면, ToOne LAZY가 *진짜로* lazy로 동작한다. 3장에서 다룬 옵션이다. 기본 ToOne LAZY는 사실 Hibernate가 reflection만으로는 부분적 lazy를 만들 수 없어서 일부 시나리오에서 EAGER처럼 동작하는 함정이 있다. bytecode enhancement의 `enableLazyInitialization`이 그 함정을 막아준다. 3장의 결론을 여기서 다시 회수하자.

## 발견의 윤곽 — 우리 N+1을 보이게 만들자

여기까지 읽고 든 생각이 있을 것이다. *우리 코드에 N+1이 있는지 어떻게 알지?* 합리적인 질문이다. 가장 정직한 답은 한 줄이다 — *SQL 카운트를 세어보자*.

자세한 도구 사용법은 11장에서 본격적으로 다룬다. 여기서는 발견의 윤곽만 잡아 두자. 두 가지 도구가 사실상 표준이다.

첫째, *로깅으로 일단 본다*. `org.hibernate.SQL` 로그 레벨을 DEBUG로 켜고, `org.hibernate.orm.jdbc.bind`까지 켜면 한 요청에 어떤 SQL이 몇 번 나가는지 줄줄이 콘솔에 찍힌다. 처음 N+1을 마주하는 개발자는 이 로그를 한 번 띄워 보기만 해도 자기 코드에 어떤 일이 일어나는지 보인다. 다만 운영에서 이걸 켜 두는 건 추천하지 않는다. 너무 시끄럽다. 개발·테스트 단계에서.

둘째, *테스트에서 SQL 카운트를 검증한다*. Vlad가 직접 만든 `hypersistence-utils`의 `SQLStatementCountValidator`가 사실상 표준이다.

```java
@Test
void postList_executesSingleQuery() {
    SQLStatementCountValidator.reset();

    List<PostListItem> posts = postService.listPublished(0, 10);

    SQLStatementCountValidator.assertSelectCount(1);
}
```

`assertSelectCount(1)`. 이 한 줄이 무엇을 보장하는가. 우리 list API는 *정확히 한 번*의 SELECT만 발사한다. 누가 코드를 잘못 손대서 N+1이 다시 자라면, 이 테스트가 빨갛게 떨어진다. *N+1이 회귀하기 전에* 잡힌다는 뜻이다. CI에 박아두면 영구적인 안전망이 된다.

여기서 한 가지를 강하게 권하고 싶다. *가장 큰 list API 세 개에 대해서는 SQL 카운트 단위 테스트를 박아두자*. 두 줄짜리 테스트가 운영의 1초짜리 응답 무너짐을 사전에 막는다. 그 가성비를 한 번 맛본 팀은 다시는 안 켜고 못 살게 된다. 자세한 사용법, 그리고 datasource-proxy의 query count listener를 활용하는 변형까지는 11장의 진단·관찰 챕터에서 한 번 더 정리한다.

여기까지 정리하고 나면, N+1은 *발견하는 눈*과 *고치는 손* 두 가지로 정리된다. 발견의 눈은 SQL 로깅과 카운트 단위 테스트, 고치는 손은 위의 네 가지 권장 순서. 두 가지를 모두 가져야 비로소 N+1이 *재발하지 않는다*.

## 한 번 더 짚어두는 함정들

본격적인 절들은 끝났지만, N+1 이야기를 닫기 전에 흔히 빠지는 함정 몇 가지를 짚어두자. 우리 코드에 익숙한 풍경이라면 한 번씩 다시 봐주자.

첫째, *`distinct`를 빼먹는다*. fetch join 컬렉션에 distinct가 없으면 결과 row의 부모가 자식 수만큼 중복으로 나온다. 글 10개를 기대했는데 50개가 나오는 풍경. Hibernate 6에서는 `hibernate.query.passDistinctThrough=false`로 자식 row의 distinct는 메모리에서만 수행하는 패턴이 권장된다 — SQL에까지 DISTINCT가 박혀 DB가 불필요한 정렬을 하지 않도록.

둘째, *Spring Data의 `Page<T>`와 fetch join을 같이 쓴다*. `Page`는 내부적으로 count 쿼리를 한 번 더 던지고, 본 쿼리에 LIMIT/OFFSET을 박는다. 컬렉션 fetch join이 있는 JPQL을 `Page`로 반환하려고 하면, HHH000104의 본진에 들어선다. *컬렉션은 fetch join 안 하기*가 답이다.

셋째, *`@OneToMany`만 LAZY로 두고 `@ManyToOne`은 기본값으로 둔다*. 가장 흔한 풍경 중 하나다. 컬렉션은 LAZY인 줄 알지만, ToOne의 기본값이 EAGER이라는 사실이 머릿속에서 빠져 있다. 우리 엔티티의 `@ManyToOne` 자리에 `fetch = LAZY`가 빠진 곳이 있다면, 거기가 N+1의 가장 큰 입구다.

넷째, *EntityGraph를 걸었는데 다른 EAGER 잔재가 살아 있다*. 이때 `EntityGraphType.FETCH`(fetchgraph)를 쓰면 그래프 밖의 EAGER을 *한 쿼리만* 끌 수 있다. 기본 `LOAD`만 쓰다 보면 잔재가 그대로 살아 있다. 한 번 더 짚어두자.

다섯째, *N+1을 잡으려고 한 곳에서 JOIN FETCH를 욱여넣다가 카르테시안 곱을 만든다*. 한 쿼리에 두 개의 컬렉션을 동시에 fetch join하면, 두 컬렉션의 곱만큼 row가 폭발한다. 글 100개에 댓글 평균 20, 좋아요 평균 50을 동시에 fetch join하면 row가 10만 개로 부푼다. 한 쿼리에 컬렉션 fetch는 한 번만. 다른 컬렉션은 `@BatchSize` 또는 별도 쿼리로.

이 다섯 가지는 운영 사고로 직결되는 함정들이라 외워두는 편이 낫다. 살짝 찜찜한 코드를 발견했다면 그 자리에서 한 번 더 의심하자. 의심하지 않고 넘어간 코드가 어느 새벽 알람을 깨운다.

## 가져오는 형태는 다음 장으로

여기까지 N+1을 다뤘다. 우리 코드의 SQL 카운트를 줄였다. 한 페이지 요청에 100번 나가던 SQL이 2번으로 줄었다. 박수받을 일이다.

그런데 한 가지 의문이 슬며시 떠오른다. *우리는 정말 이 데이터를 다 가져와야 했던가?* 글 목록 화면에 작성자 *이름과 프로필 사진 URL*만 보여줘도 되는데, 우리는 `Author` 엔티티 전체를 끌고 왔다. 안 쓰는 컬럼이 열 개쯤 더 있다. 그리고 `Author`는 또 `Department`와 `Role`을 EAGER로 들고 올 수도 있다 — 우리가 매핑을 그렇게 짰다면. 결국 *fetch 수*는 줄였는데, *한 row의 무게*는 그대로다.

여기서 N+1 이야기와 자연스럽게 만나는 다른 축이 한 줄로 모습을 드러낸다. *fetch를 줄였으면, 가져오는 형태도 다시 봐야 한다*. 엔티티를 그대로 가져올 것이냐, DTO로 사영(projection)할 것이냐, JPQL constructor expression을 쓸 것이냐, Spring Data Interface Projection을 쓸 것이냐, 아니면 `@Subselect`로 가상 엔티티를 만들 것이냐. 그리고 native query는 언제, jOOQ는 언제? 한 챕터를 따로 떼어 다뤄야 할 이야기다.

다음 5장의 슬로건 한 줄을 미리 던져두자. *"수정 안 할 read는 모두 DTO."* Vlad의 14 tips 중 한 줄이다. 이 슬로건이 무엇을 뜻하는지, 그리고 우리에게 어떤 도구 상자가 있는지를 다음 장에서 함께 살펴보자.

## 마무리 — 잊지 말자

이 장은 한 가지 단순한 사실에서 시작했다. *N+1은 누구나 안다고 한다. 그런데 우리 코드에는 여전히 있다.* 그 모순의 정체를 한 줄로 정리하면 이렇다. *N+1은 슬로우 쿼리 로그에 안 잡힌다. 각 쿼리가 빠르기 때문이다. 그래서 모르고 지나간다.*

우리가 가진 무기는 정리됐다. 권장 순서는 ① `JOIN FETCH` / `@EntityGraph` ② `@BatchSize` + `default_batch_fetch_size` ③ `@Fetch(FetchMode.SUBSELECT)`. 한국 실무의 합의된 한 줄 슬로건은 *ToOne만 fetch join, ToMany는 batch_size 100~1000*. 컬렉션 fetch join + 페이지네이션은 HHH000104의 함정. 정석은 2-query 패턴이지만, batch_size를 켜 두면 한 줄에 끝난다.

전역 fetch plan을 매핑에서 결정하는 EAGER는 코드 스멜이다. *LAZY globally, JOIN FETCH per query*. 모든 `@ManyToOne`과 `@OneToOne`에 `fetch = LAZY`를 명시적으로 박는 코드 컨벤션을 두는 편이 낫다. bytecode enhancement를 켜 두면 그 LAZY가 진짜로 작동한다.

발견의 눈도 함께 가져가자. SQL 로깅을 켜 한 번 살펴보고, 가장 큰 list API에는 `SQLStatementCountValidator.assertSelectCount(...)`로 회귀 테스트를 박아 두자. 자세한 도구는 11장에서 다시 만난다.

마지막으로, 한 가지를 마음에 새겨 두자. *우리 코드의 N+1은 우리만 안다*. Vlad의 책에도, 이 챕터에도, 우리 회사의 N+1이 어디에 있는지는 적혀 있지 않다. 책을 덮고 우리 IDE를 열어, `@ManyToOne`이 박힌 줄을 한 번 grep해 보는 30초만이 우리 코드의 N+1을 찾는 유일한 길이다. 30초의 grep이 다음 새벽의 알람을 막는다.

### 내 코드 체크리스트 3개

- 우리 코드의 모든 `@ManyToOne`과 `@OneToOne`에 `fetch = LAZY`가 *명시적으로* 붙어 있는지.
- 컬렉션 fetch join과 페이지네이션이 같은 쿼리에 함께 걸린 곳이 있는지(있다면 HHH000104 경고가 로그에 떠 있을 가능성이 높다).
- 가장 큰 list API 한두 개의 SQL 카운트를 단위 테스트로 검증하고 있는지(예: `SQLStatementCountValidator.assertSelectCount(1)`).

다음 장에서는 *가져오는 형태*로 들어간다. fetch 수를 줄였으니, 이제 row 하나의 무게를 줄일 차례다.
