# 10장. 깊은 페이지도 첫 페이지처럼 — 페이지네이션

긴 글 목록이 있는 서비스를 하나 떠올려 보자. 게시판이든, 상품 카탈로그든, 알림 피드든. 첫 페이지는 시원하게 떨어진다. 50ms. 누구도 불평하지 않는다. 두 번째 페이지도 비슷하다. 열 번째 페이지도 그럭저럭. 그런데 어느 날 누군가가 *500페이지*를 누른다. 응답이 3초가 걸린다. 천 페이지를 누르면 6초. 만 페이지에서는 타임아웃이 떨어진다. *어디에서 무엇이 무너졌을까?* SQL은 그대로다. 인덱스도 그대로다. 데이터가 늘었을 뿐인데, 왜 깊은 페이지가 더 느릴까?

이게 OFFSET 페이지네이션의 정체다. 우리가 무심코 짠 `LIMIT 20 OFFSET 10000`이라는 한 줄에 비밀이 숨어 있다. 그리고 그 비밀을 알고 나면, 무한 스크롤이 *깊이와 무관하게* 늘 일정한 속도로 떨어지는 이유도 함께 보인다. 이번 장에서는 한국 서비스 곳곳에 깔린 OFFSET을 keyset으로 옮기는 절차, 그리고 Spring Data 3.x와 Hibernate 6가 이 작업을 어떻게 *한 줄로* 만들어 줬는지를 함께 살펴본다.

## OFFSET이 무너지는 이유 — "앞을 다 읽고 버린다"

먼저 한 가지를 확실히 해두자. *OFFSET이 느린 이유는 인덱스가 없어서가 아니다*. 인덱스가 있어도 OFFSET은 깊은 페이지에서 무너진다. 이유는 단순하다. 데이터베이스는 *OFFSET 개의 row를 다 읽은 다음에 버린다*. 우리가 11페이지를 보고 싶다고 해서 DB가 곧장 11페이지로 점프하지는 못한다. 첫 페이지부터 차례대로 *세면서* 와야 한다.

SQL 한 줄로 보자.

```sql
SELECT id, title, created_at
FROM post
ORDER BY created_at DESC
LIMIT 20 OFFSET 10000;
```

OFFSET=10000일 때, DB는 10000개의 row를 *읽고 버린다*. 그리고 그다음 20개만 우리에게 준다. 인덱스가 created_at에 잘 잡혀 있어도, 인덱스 스캔을 통해 10020개 entry를 훑어야 한다. 페이지가 깊어질수록 비례해서 비용이 늘어난다. 페이지 1000에 가면 인덱스 entry 20020개를 훑는다. 페이지 5000에 가면 100020개. 인덱스 스캔이 *원래는 O(log n)*이라는 직관이 깨지는 자리다. 인덱스로 *찾는 비용*은 여전히 빠르다. 깨지는 건 *훑고 버리는* 비용 쪽이다.

여기에 한 가지가 더 붙는다. *정렬 안정성 문제*다. `ORDER BY created_at DESC` 한 줄로 정렬하면, created_at이 동일한 row가 둘 이상일 때 그들 간의 순서는 *DB에 맡겨진다*. 같은 초에 INSERT된 글이 두 개라면, 그 두 글의 순서가 페이지마다 바뀔 수 있다. 어느 페이지에서는 A가 먼저, 다른 페이지에서는 B가 먼저. 사용자가 새로 고침을 누를 때마다 글이 *위치를 바꾸는* 풍경이 보인다. 첫 페이지에서 봤던 글이 두 번째 페이지에도 보이거나, 보였던 글이 사라지기도 한다. 사용자 입장에서는 *데이터가 새는* 듯한 감각을 준다. 난감한 상황이다.

이 정렬 불안정성은 OFFSET이 깊을수록 두드러진다. 페이지 1에서 누락된 한 줄이 페이지 500에서 갑자기 보이는 일도 가능하다. 그리고 그 사이에 새 글이 추가되면 페이지 경계가 통째로 흔들린다. 누군가 *글을 작성하는 순간*과 *누군가 페이지를 넘기는 순간*이 겹치면, 같은 글을 두 번 보거나 한 번도 못 보는 일이 생긴다. 이걸 두고 사용자가 "데이터가 이상해요"라고 문의를 보낸다. 우리는 *원인을 추적할 수도 없다*. 그저 OFFSET 페이지네이션의 본성이다.

그렇다면 OFFSET은 도대체 언제 쓸 만한 것인가? 짧은 결론은 이렇다. *데이터가 얕고, 사용자가 깊은 페이지로 갈 일이 없을 때*. 관리자 대시보드의 작은 목록, 한 페이지에 다 들어가는 카탈로그, 페이지가 다섯 개를 넘어가지 않는 화면. 이런 자리에서는 OFFSET이 멀쩡히 동작한다. 함정은, *처음에는 그렇게 보이던 화면*이 시간이 지나며 데이터가 쌓이면서 어느새 깊은 페이지를 요구받는 자리로 바뀐다는 점이다. 우리 코드의 OFFSET이 *3년 후의 데이터양*에서도 멀쩡할지를 한 번 의심해 보는 편이 낫다. 그렇지 않으면 어느 새벽 알람이 운영자를 깨운다.

## Keyset — "방금 본 자리"부터 다음 페이지

OFFSET이 *세고 버리는* 방식이라면, keyset(또는 seek method라고도 부른다)은 *방금 본 자리부터 잇는* 방식이다. 직관은 간단하다. 우리가 친구에게 책을 읽다 멈춘 자리를 알려주려면, "30페이지 다음을 읽어"라고 말하지 *"앞에서 30장을 세고 그다음을 읽어"*라고 말하지는 않는다. 책갈피를 꽂아두는 셈이다. SQL로도 그렇게 한다.

```sql
SELECT id, title, created_at
FROM post
WHERE (created_at, id) < (?, ?)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

여기서 `?, ?`에는 *직전 페이지의 마지막 row의 (created_at, id)* 값을 넣는다. 그러면 DB는 *그 자리 다음부터* 인덱스를 forward iterate하면서 20개를 가져온다. *훑고 버리는 row가 없다*. OFFSET이 페이지 깊이에 비례해 느려졌던 그 비용이 0이 된다. 페이지 1에서도, 페이지 1000에서도, 페이지 50000에서도 같은 응답시간이 나온다. *깊이 무관*(depth-independent) 페이지네이션이라고 부르는 까닭이다.

여기서 한 가지를 강조해 두자. `WHERE (created_at, id) < (?, ?)`라는 *튜플 비교* 한 줄이 keyset의 진짜 핵심이다. created_at 하나만 쓰면 어떨까? `WHERE created_at < ?`. 잘 동작하는 듯 보이지만, 같은 초에 INSERT된 글이 두 개라면 *그중 하나가 페이지 경계에 걸쳤을 때* 한 행이 사라지거나 두 번 보일 수 있다. 페이지 첫째 줄에 보인 글이 다음 페이지에도 보인다. 끔찍한 일이다. 그래서 *정렬 키가 unique하지 않다면, 반드시 PK 같은 tie-breaker를 함께 넣는다*. created_at으로 일차 정렬, id로 이차 정렬. 튜플 비교는 이 둘을 *사전식 순서로* 비교한다. created_at이 같다면 id로 가른다. 이게 keyset이 OFFSET이 못 가졌던 *정렬 안정성*까지 함께 챙기는 메커니즘이다.

JPA로 옮기면 이렇게 된다.

```java
public List<Post> findNextPage(LocalDateTime lastCreatedAt, Long lastId, int size) {
    return em.createQuery("""
        select p from Post p
        where p.createdAt < :lastCreatedAt
           or (p.createdAt = :lastCreatedAt and p.id < :lastId)
        order by p.createdAt desc, p.id desc
        """, Post.class)
        .setParameter("lastCreatedAt", lastCreatedAt)
        .setParameter("lastId", lastId)
        .setMaxResults(size)
        .getResultList();
}
```

JPQL은 표준에서 row constructor 비교(`(a, b) < (?, ?)`)를 보장하지 않는다. 그래서 위처럼 *동등 + 부등* 조합을 OR로 풀어 쓰는 편이 안전하다. Hibernate가 DB에 따라 row constructor를 지원하기도 하지만, 호환을 보장하려면 이 형태가 정석이다. 인덱스로 `(created_at desc, id desc)` 복합 인덱스를 함께 만들어 두면, 옵티마이저가 이 비교를 인덱스 forward scan으로 풀어낸다.

물론 이 패턴에는 신경 써 줘야 할 자리들이 있다. 살펴보자.

### tie-breaker는 PK가 정석이다

정렬 키에 tie가 생길 수 있는 컬럼만 있다면, 반드시 두 번째 정렬 키로 PK를 함께 넣는다. created_at처럼 timestamp 컬럼은 같은 ms에 두 row가 들어올 가능성이 항상 있다. 가끔은 같은 *초*에도 들어온다. score, priority, popularity 같은 숫자 컬럼은 더 자주 tie를 만든다. 정렬 키만으로 페이지를 짜고 한참 운영하다 *드물게 한 글이 사라진다*는 제보를 받으면, 그 자리가 거의 항상 tie-breaker가 빠진 자리다. 어떤 정렬을 쓰든 마지막에 *unique한 무엇*(보통 PK)을 한 줄 더 붙여두는 편이 낫다. *마지막에 PK 한 줄*은 keyset의 안전벨트다.

### NULL은 어떻게 처리할까

정렬 컬럼이 nullable이라면 이야기가 까다로워진다. SQL은 NULL과의 비교 결과가 *늘 unknown*이다. `NULL < anything`도, `anything < NULL`도, 둘 다 false에 가깝게 동작한다. NULL이 섞인 컬럼으로 keyset을 짜면 페이지 경계에서 row가 *통째로 누락*되거나 *겹쳐서* 나올 수 있다. DB는 또 `NULLS FIRST`/`NULLS LAST` 정책이 제각각이다. PostgreSQL은 default가 `NULLS LAST`(DESC 정렬일 때는 `NULLS FIRST`), MySQL은 NULL을 작은 값으로 본다. 그대로 두면 사고가 난다.

처리 방법은 두 가지다. *NULL이 안 들어오는 컬럼*만 keyset 키로 쓰거나, 정렬 시 NULL을 명시적으로 다루는 것. created_at처럼 *생성 시점에 늘 채워지는* 컬럼은 안전하다. 반면 deleted_at, modified_at, completed_at 같은 *선택적 timestamp*는 NULL이 섞이므로 keyset 키로는 부적합하다. 그래도 굳이 써야 한다면, `ORDER BY completed_at DESC NULLS LAST, id DESC`처럼 명시적 NULL 처리 절을 붙이고, WHERE 절에서도 `(completed_at IS NULL AND ...) OR (completed_at < :last ...)`처럼 분기를 짜야 한다. 코드가 단번에 지저분해진다. 그래서 *keyset 키는 NOT NULL 컬럼만 쓰는* 편이 깔끔하다. 우리 엔티티의 정렬 기준 컬럼들에 nullable이 섞여 있다면, 한 번 더 들여다보는 편이 낫다.

### descending과 ascending이 섞일 때

`ORDER BY priority ASC, created_at DESC` 같은 정렬을 keyset으로 풀어야 할 때가 있다. 부호가 섞이면 튜플 비교가 깔끔하게 안 된다. 이때는 분기를 명시적으로 풀어 써야 한다.

```sql
WHERE p.priority > :lastPriority
   OR (p.priority = :lastPriority AND p.createdAt < :lastCreatedAt)
   OR (p.priority = :lastPriority AND p.createdAt = :lastCreatedAt AND p.id < :lastId)
ORDER BY p.priority ASC, p.createdAt DESC, p.id DESC
LIMIT 20
```

priority가 더 *큰* row, priority가 같다면 createdAt이 더 *작은* row(역순이니까), 둘 다 같다면 id가 더 작은 row. 사전식 비교를 손으로 푸는 셈이다. 정렬 키가 두세 개를 넘어 네 개, 다섯 개가 되면 이 분기가 손으로 짜기 매우 번거롭다. 이쯤 되면 직접 짜기보다 도구의 힘을 빌리는 편이 낫다. 그 도구가 다음 절의 주인공인 Blaze-Persistence와 Spring Data의 `ScrollPosition`이다.

## Blaze-Persistence — `withKeysetExtraction(true)` 한 줄

Blaze-Persistence는 JPA Criteria를 *진짜 production 도구*로 진화시킨 라이브러리다. 4장과 5장에서 한 번씩 이름이 나왔었다. 페이지네이션에서도 그 매력이 두드러진다. Vlad가 *keyset pagination을 쓰려거든 Blaze-Persistence를 쓰라*고 강하게 권하는 이유가 있다. *위에서 손으로 짠 분기를 한 줄로 자동 생성해주기 때문이다*.

```java
PagedList<Post> page = cbf.create(em, Post.class)
    .orderByDesc("createdAt")
    .orderByDesc("id")
    .page(0, 20)
    .withKeysetExtraction(true)
    .getResultList();

// 다음 페이지를 받을 때는 직전 페이지의 keyset을 그대로 넘긴다
PagedList<Post> next = cbf.create(em, Post.class)
    .orderByDesc("createdAt")
    .orderByDesc("id")
    .pageAndNavigate(page.getKeysetPage(), 20)
    .getResultList();
```

`withKeysetExtraction(true)` 한 줄로 Blaze-Persistence가 *마지막 row의 정렬 키*를 자동으로 추출해 다음 페이지의 cursor로 쓸 수 있게 한다. 정렬 키가 ASC/DESC로 섞여 있어도, NULL 처리도, 분기 작성도 라이브러리가 알아서 풀어준다. 우리가 신경 쓸 것은 *어떤 컬럼들로 정렬할 것인가*뿐이다. 손으로 짠 OR 분기가 사라진다.

추가로 Blaze-Persistence는 *count 쿼리 생략*까지 챙겨준다. OFFSET 페이지네이션이 보통 `count(*)` 쿼리를 한 번 더 던지는 것과 달리(이 count 쿼리도 깊은 데이터에서 충분히 비싸다), keyset은 *다음 페이지가 있는지*만 알면 된다. limit+1로 한 row 더 읽어, 마지막 row가 있으면 "다음 페이지 있음" 표시를 켜는 식. 이 *count 회피*가 keyset의 또 다른 비용 절감 포인트다. 깊은 데이터에서 count 한 번이 페이지 read 본체보다 비싼 경우도 흔하다.

물론 Blaze-Persistence를 도입하는 데에는 한 가지 비용이 따른다. *학습 곡선*. Criteria 위에 새 DSL이 한 겹 더 있고, JPA 환경 설정에 추가가 필요하다. 그래도 한 번 도입하고 나면 keyset뿐만 아니라 LATERAL JOIN, CTE, window function까지 type-safe API로 쓸 수 있어서, 진지한 페이지네이션과 분석 쿼리가 많은 서비스라면 도입 가성비가 크다. *진짜 큰 list API*가 서너 개 있는 서비스라면 검토해 볼 만하다.

## Spring Data 3.x — `KeysetScrollPosition` 한 줄

Blaze-Persistence가 부담스럽다면, Spring Data JPA 3.x가 *keyset을 1급 시민*으로 끌어 올린 새 API가 있다. `ScrollPosition`이다. 이 API의 등장은 Spring Data 진영이 *keyset이 페이지네이션의 정석*이라고 공식 선언한 순간이다. 무한 스크롤이 흔한 모바일 시대에 맞춰 진작 자리잡았어야 할 도구가 늦었지만 도착했다.

기본 사용법은 이렇게 단순하다.

```java
public interface PostRepository extends Repository<Post, Long> {
    Window<Post> findFirst20ByOrderByCreatedAtDescIdDesc(ScrollPosition position);
}

// 첫 호출
Window<Post> first = repo.findFirst20ByOrderByCreatedAtDescIdDesc(
    ScrollPosition.keyset()
);

// 다음 페이지
Window<Post> next = repo.findFirst20ByOrderByCreatedAtDescIdDesc(
    first.positionAt(first.size() - 1)
);

// 끝까지 순회하고 싶다면
WindowIterator<Post> it = WindowIterator.of(
    pos -> repo.findFirst20ByOrderByCreatedAtDescIdDesc(pos)
).startingAt(ScrollPosition.keyset());

it.forEachRemaining(post -> { /* ... */ });
```

`ScrollPosition.keyset()`이 첫 호출의 *비어 있는 cursor*다. 첫 페이지가 떨어지면 `Window<Post>`가 반환되고, 거기에 `positionAt(index)`로 *그 row의 keyset 위치*를 뽑을 수 있다. 다음 페이지 호출에 그걸 그대로 넘기면 끝. 손으로 짤 OR 분기도, 마지막 row의 (created_at, id)를 따로 들고 다닐 컨트롤러 변수도 필요 없다. *Spring Data가 알아서 한다*.

여기에 한 가지 더 매력적인 점이 있다. `WindowIterator`다. 무한 스크롤 형태의 API를 서버에서 *순회*하면서 처리해야 할 때, 그러니까 *전체 데이터를 keyset 방식으로 한 번 훑고 싶을 때* `WindowIterator`가 cursor를 자동으로 이어 준다. 백오피스 export, 데이터 마이그레이션, 대량 알림 발송 같은 자리에서 *OOM 없이*(1차 캐시는 잘게 끊어내야 한다 — 9장의 `flush() + clear()` 패턴과 합쳐서 쓰자) 전체를 훑을 수 있다.

`ScrollPosition`에는 두 가지 변종이 있다는 점을 짚어두자. `KeysetScrollPosition`과 `OffsetScrollPosition`. 이름 그대로다. 후자는 *Spring Data가 OFFSET을 흉내내 주는* 길이다. 점진적으로 keyset으로 옮기고 싶다면 `OffsetScrollPosition`으로 시작해 인터페이스를 통일한 뒤, 핫한 API만 골라 `KeysetScrollPosition`으로 옮기는 마이그레이션 경로도 가능하다. *인터페이스가 같다*는 점이 이 API의 진짜 가치다. 컨트롤러와 서비스 코드는 그대로 두고, repository 호출 한 줄만 바꿀 수 있다.

물론 `findBy...` 시그니처에는 *정렬 키가 메서드 이름에 박혀 있어야* keyset 컬럼이 결정된다. 동적 정렬이 필요한 자리에는 `@Query` JPQL과 함께 `Sort`/`Pageable` 대신 `ScrollPosition`을 인자로 받아 풀어내는 형태가 있다. 자세한 사용법은 Vlad의 *Spring Data WindowIterator* 글에 코드와 함께 잘 정리돼 있다. 우리 서비스의 가장 큰 list API를 한 번 골라 시범 적용해 보면, 첫 마이그레이션의 어느 자리가 까다로운지가 30분 안에 손에 잡힌다. 해 보는 편이 낫다.

## Hibernate 6의 한 방 — JPQL window function

여기까지가 *cursor 기반*의 페이지네이션이었다. 그런데 어떤 자리에서는 우리가 *전체 row 수*와 *현재 페이지가 몇 번째인지*를 함께 알아야 한다. 페이지 번호가 보이는 클래식한 게시판 UI다. 1, 2, 3, ..., 10, 다음. 이 화면을 짜자면 보통 두 가지 쿼리를 한 트랜잭션에 던진다. 본 쿼리에 `LIMIT/OFFSET`을, 별도로 `count(*)`. count 쿼리가 깊은 데이터에서 충분히 비싸다는 점은 앞서도 짚었다.

Hibernate 6의 *JPQL window function*이 이 자리에서 한 방 카드를 꺼낸다. SQM(Semantic Query Model)이라는 새 query parser가 들어오면서, JPQL이 SQL의 window function을 표준 문법으로 지원하기 시작했다. `ROW_NUMBER() OVER (...)`, `COUNT(*) OVER ()`, `RANK() OVER (...)`. 이전에는 native SQL로 내려가야만 쓸 수 있던 도구들이 *JPQL 안에서* 동작한다.

페이지네이션에 적용해 보자. 페이지 메타와 본 쿼리를 한 번에 가져오는 식이다.

```java
List<Tuple> rows = em.createQuery("""
    select p.id, p.title, p.createdAt,
           count(*) over () as total,
           row_number() over (order by p.createdAt desc, p.id desc) as rn
    from Post p
    where p.status = :status
    order by p.createdAt desc, p.id desc
    """, Tuple.class)
    .setParameter("status", Status.PUBLISHED)
    .setFirstResult(offset)
    .setMaxResults(20)
    .getResultList();

long total = ((Number) rows.get(0).get("total")).longValue();
```

`count(*) over ()`가 한 쿼리 안에서 *전체 row 수*를 함께 계산해 준다. 별도 count 쿼리가 사라진다. DB가 한 번의 scan으로 본 데이터와 메타 데이터를 동시에 만들어낸다. 깊은 페이지에서도 count의 부담이 본 쿼리에 흡수돼 추가 비용이 거의 없다(같은 인덱스 scan을 두 번 하지 않는다). *클래식한 페이지 번호 UI를 keyset 없이 유지해야 하는 자리*에서 이만큼 깔끔한 도구가 없다.

물론 window function도 page 깊이 자체의 비용은 그대로 안고 간다. OFFSET이 깊어지면 본 쿼리의 스캔 비용은 여전히 늘어난다. 즉 window function은 *count 부담을 줄이는* 도구지, *깊이 무관* 도구는 아니다. 깊이 무관이 필요하면 keyset으로 가야 한다. 두 도구의 자리가 다르다.

`ROW_NUMBER()`를 활용하면 또 다른 한 가지가 풀린다. *카테고리별 N개씩*이라는 화면이다. 부서별로 최근 5개의 글씩 뽑아 한 화면에 보여주고 싶다면, 부서마다 별도 쿼리를 보내는 게 자연스러워 보인다. N+1의 친구다. window function으로 한 방에 풀 수 있다.

```sql
SELECT *
FROM (
    SELECT id, title, dept_id,
           ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY created_at DESC) AS rn
    FROM post
) ranked
WHERE rn <= 5;
```

JPQL로도 그대로 표현된다. *부서마다 N개*가 한 쿼리에 떨어진다. 이런 자리는 OFFSET이든 keyset이든 단일 페이지네이션으로는 풀리지 않는다. *카테고리 차원이 추가된* 페이지네이션이라고 부를 만하다. Hibernate 6의 SQM이 가능하게 한 새 도구가 우리에게 새 풍경을 보여주는 자리다. JPA가 *DB 능력을 가린다고 못 쓰는 게 아니다*. 한 번 더 강조해 두자.

## 컬렉션 fetch와 페이지네이션 — HHH000104의 재방문

4장에서 다뤘던 HHH000104 경고를 기억하는가? 짧게 복습하자. *컬렉션 fetch join + 페이지네이션*은 함께 쓰면 안 된다. Hibernate가 부모 row가 자식 수만큼 부풀려진 결과를 *DB-level OFFSET이 아닌 메모리 내에서* 잘라낸다. 글 100개를 페이지로 잘라야 하는데 댓글 fetch join이 들어가면 부풀려진 row를 전부 메모리로 들고 와서 자른다. 깊은 페이지에서 *OOM의 단골 자리*다.

4장의 결론은 2-query 패턴이었다. 부모 PK만 페이지로 뽑은 뒤, 그 PK 목록을 IN 절로 던져 자식과 함께 한 번에 가져오는 형태. 이걸 keyset으로 옮기면 어떻게 될까?

```java
// 1) 부모 PK를 keyset 페이지로 뽑는다
List<Object[]> idAndKey = em.createQuery("""
    select p.id, p.createdAt
    from Post p
    where p.createdAt < :lastCreatedAt
       or (p.createdAt = :lastCreatedAt and p.id < :lastId)
    order by p.createdAt desc, p.id desc
    """, Object[].class)
    .setParameter("lastCreatedAt", lastCreatedAt)
    .setParameter("lastId", lastId)
    .setMaxResults(20)
    .getResultList();

List<Long> postIds = idAndKey.stream()
    .map(arr -> (Long) arr[0])
    .toList();

// 2) 그 PK들을 IN 절로 fetch join
List<Post> posts = em.createQuery("""
    select distinct p from Post p
    left join fetch p.comments
    where p.id in :ids
    order by p.createdAt desc, p.id desc
    """, Post.class)
    .setParameter("ids", postIds)
    .getResultList();
```

이 2-query 패턴은 OFFSET일 때도 OFFSET을 *부모 PK 쿼리*로만 보내기 때문에 부풀림 문제를 피했다. keyset으로 옮기면 거기에 *깊이 무관* 속성이 함께 따라온다. 깊은 페이지의 게시판에 댓글 미리보기까지 같이 보여주고 싶은 화면에서 정석 형태다. 한국 커뮤니티의 게시판 사례에서 가장 자주 만나는 자리이기도 하다.

추가로, ToMany 컬렉션이 fetch join 대신 `@BatchSize`로 묶이도록 매핑돼 있다면 *한 쿼리*로도 끝난다. 부모 페이지를 keyset으로 뽑으면 Hibernate가 그 부모들의 ToMany 컬렉션을 `WHERE parent_id IN (?, ?, ?, ...)` 한 쿼리로 채워준다. 4장의 *ToOne만 fetch join, ToMany는 batch_size 100~1000* 슬로건이 페이지네이션 자리에서도 그대로 살아 있는 셈이다. 우리 매핑이 그렇게 돼 있다면 손가락 하나 안 움직여도 깊이 무관 페이지가 떨어진다. 한 번 더 강조하자면, *매핑이 곧 SQL이다*. 3장과 4장에서 본 풍경이 10장에서도 동일하다.

## Projection과 함께 — list API의 정석 형태

여기서 한 가지 의문이 슬며시 떠오른다. *우리는 정말 엔티티를 통째로 가져와야 하는가?* 5장에서 다뤘던 projection 이야기를 다시 꺼낼 자리다. 글 목록 화면에 글 제목, 작성자 이름, 댓글 수 정도만 보이면 된다면, `Post` 엔티티 전체를 메모리에 올릴 이유가 없다. *수정 안 할 read는 모두 DTO*. Vlad의 슬로건이 페이지네이션 자리에서도 그대로 적용된다.

keyset과 projection을 합치면 list API의 *정석 형태*가 나온다.

```java
public record PostSummary(
    Long id,
    String title,
    LocalDateTime createdAt,
    String authorName,
    long commentCount
) {}

public List<PostSummary> findNextSummaries(
    LocalDateTime lastCreatedAt, Long lastId, int size
) {
    return em.createQuery("""
        select new com.acme.PostSummary(
            p.id, p.title, p.createdAt,
            p.author.name,
            (select count(c) from Comment c where c.post = p)
        )
        from Post p
        where p.createdAt < :lastCreatedAt
           or (p.createdAt = :lastCreatedAt and p.id < :lastId)
        order by p.createdAt desc, p.id desc
        """, PostSummary.class)
        .setParameter("lastCreatedAt", lastCreatedAt)
        .setParameter("lastId", lastId)
        .setMaxResults(size)
        .getResultList();
}
```

세 가지 미덕이 한 자리에 모인다. *깊이 무관*(keyset) + *가벼운 row*(projection) + *PersistenceContext 비용 없음*(엔티티가 아니라 record라서 1차 캐시에 등록되지 않는다). 이 셋이 합쳐지면 list API의 응답시간이 *데이터 양에 무관하게 일정*해진다. 글이 100개일 때나 1000만 개일 때나, 한 페이지의 read 비용이 같다. 그리고 같은 트랜잭션 안에서 다른 entity를 잡고 있어도 *깨끗하게 빠져나간다*. 안 빠지면 6장의 OSIV 안티패턴과 만나니까. 운영 사고의 진원지가 하나씩 사라지는 풍경이다.

list API가 자주 호출되는 API일수록 이 정석 형태가 *몇 배의 운영 안정성*을 가져온다. 핫한 list API 세 개에 대해서만 이 패턴으로 옮겨도 운영 메트릭이 바뀐다. 한 번 시범 적용해 보면 응답시간 분포의 long tail이 *눈에 띄게* 줄어든다. 깊은 페이지를 누르는 일부 사용자만 겪던 3초가 사라지고, 평균과 p99가 거의 붙는 자리로 옮겨간다. 작은 투자로 큰 효과를 보는 자리. 손을 안 댈 이유가 없다.

## OFFSET을 keyset으로 옮기는 절차

여기까지 도구를 모두 살펴봤다. 그렇다면 *지금 OFFSET을 쓰고 있는 우리 코드*는 어떻게 옮겨야 할까? 한 번에 다 옮기려고 하면 부담스럽다. 코드 양도 양이지만, UI의 페이지네이션 형태가 바뀌면 사용자 경험도 함께 바뀐다. 단계적으로 가는 편이 낫다. 권하고 싶은 절차는 이렇다.

먼저, *측정한다*. 우리 서비스의 가장 큰 list API 세 개를 고른다. p99 응답시간을 페이지 깊이별로 측정한다. 페이지 1과 페이지 100, 페이지 500의 응답시간 차이를 본다. 차이가 5배 이상 나는 API가 *옮길 1순위 후보*다. 차이가 미미하다면 이미 데이터가 충분히 작거나, 인덱스 hit ratio가 좋아 OFFSET이 멀쩡히 동작 중인 자리다. 옮길 우선순위가 낮다.

두 번째로, *UI 형태를 결정한다*. 페이지 번호가 보이는 클래식 UI인지, 무한 스크롤인지. 무한 스크롤이면 keyset이 자연스럽다. 페이지 번호 UI라면 두 가지 길이 있다. (a) UI를 무한 스크롤로 바꾸는 길, (b) UI는 두고 Hibernate 6 window function으로 count를 한 쿼리로 흡수하는 길. 사용자 경험 변경이 허용된다면 (a)가 가장 깔끔하고 깊이 무관까지 챙긴다. UI를 못 바꾸겠다면 (b)로 일단 count 부담만 줄이고, 깊이 무관은 인덱스 튜닝으로 어느 정도 풀어두는 절충안이 가능하다.

세 번째로, *cursor를 노출한다*. keyset으로 옮기면 클라이언트가 *cursor*를 들고 다녀야 한다. 페이지 번호 대신 *"방금 본 마지막 row의 정렬 키"*를 다음 요청에 넣어 보낸다. API 응답에 `nextCursor` 같은 필드를 추가하고, 클라이언트가 그걸 그대로 다음 요청에 보내도록 인터페이스를 짠다. cursor는 보통 base64 인코딩한 JSON으로 노출하는 편이 안전하다 — 정렬 키 컬럼명을 노출하지 않고, 서버 측에서 변경 여지를 남긴다. Spring Data 3.x의 `ScrollPosition`이 이 작업의 상당 부분을 자동으로 해 준다.

네 번째로, *인덱스를 점검한다*. keyset의 핵심은 *정렬 키 컬럼들로 구성된 복합 인덱스*가 forward iterate에 쓰이는 것이다. `(created_at desc, id desc)` 같은 복합 인덱스가 없다면 keyset의 효과가 절반쯤 사라진다. EXPLAIN을 보면서 인덱스가 잘 쓰이는지를 한 번 확인하자. PostgreSQL이라면 `EXPLAIN ANALYZE`로 실제 row 수와 cost를 본다. MySQL이라면 `EXPLAIN FORMAT=JSON`. 깊은 페이지에서 *Index Scan*이 나와야 정상이다. *Seq Scan*이나 *Sort*가 보이면 인덱스가 의도대로 안 잡힌 것이다.

다섯 번째로, *전환 후에도 모니터링한다*. keyset이 들어간 뒤 응답시간 분포가 어떻게 변했는지를 본다. p99의 long tail이 줄어들어야 한다. 평균은 비슷할 수도 있다. keyset의 진짜 가치는 *최악 케이스를 평탄화*하는 데 있다. 그래서 평균만 보면 변화가 작아 보일 수도 있는데, p99/p999가 *수직 낙하*하는 모습이 보인다면 옮긴 보람이 있다. Hibernate Statistics나 datasource-proxy로 SQL 자체의 패턴이 의도대로 바뀌었는지도 한 번 확인하자. 자세한 도구는 11장에서 다시 만난다.

이 다섯 걸음을 한 번 거치고 나면, OFFSET을 keyset으로 옮기는 일이 *코드 한 줄 바꾸는 일이 아니라 시스템 설계 한 자락 다시 짜는 일*임이 손에 잡힌다. 그리고 그 가성비가 *얼마나 큰지*도 함께 보인다. 운영 사고를 미리 막는 가성비. 사용자에게 *깊은 페이지도 첫 페이지처럼* 보이게 하는 가성비. 충분히 손을 댈 만한 자리다.

## 한 번 더 짚어두는 함정들

본격적인 절들은 끝났지만, 페이지네이션을 닫기 전에 흔히 빠지는 함정 몇 가지를 짚어두자. 한 번씩 우리 코드에 보이는 풍경이라면 다시 봐주자.

첫째, *정렬 키에 PK가 없다*. 가장 흔한 사고 자리다. `ORDER BY created_at DESC`만 있고 id가 빠진 keyset. 같은 초에 두 글이 들어오는 자리에서 한 행이 사라지거나 두 번 보인다. 사용자가 *"글이 가끔 사라져요"*라고 문의를 보내면, 거의 항상 이 자리다. 모든 정렬에 PK를 마지막에 한 줄 더 붙이자. *마지막에 PK 한 줄*. 안전벨트다.

둘째, *cursor를 페이지 번호처럼 쓴다*. 클라이언트가 cursor를 받아 *저장*해 두고 며칠 뒤에 다시 보낸다. 그 사이에 정렬 키 컬럼이 변경되거나 row가 삭제되면 cursor가 가리키는 자리가 흐려진다. cursor는 *세션 내에서만* 유효한 것으로 인터페이스를 짜는 편이 낫다. 며칠 뒤에 같은 위치로 돌아가려면 *별도의 북마크 기능*이 필요하다. 그 둘은 다른 문제다.

셋째, *깊은 페이지 UI를 그대로 두고 keyset만 적용한다*. 페이지 번호 UI에 keyset을 끼워 넣으려고 하면 *5페이지로 점프* 같은 클릭이 동작하지 않는다. keyset은 *순차 이동*만 자연스럽다. UI를 무한 스크롤로 바꾸거나, 점프는 OFFSET이나 window function의 ROW_NUMBER로 별도 처리하는 분기가 필요하다. UI 결정 없이 백엔드만 바꾸면 *기능 회귀*가 생긴다. 사용자가 이상하다고 문의를 보낸다. 난감하다.

넷째, *count 쿼리를 그대로 둔다*. keyset으로 옮겼는데 count(*) 쿼리는 여전히 매 요청마다 던진다. 깊은 데이터에서 count의 비용이 본 쿼리만큼 비싸다. *전체 row 수가 정말 필요한가*를 다시 묻자. 무한 스크롤이라면 필요 없다. 페이지 번호 UI라도 *"총 1,234,567개의 글"*을 정확히 보여줄 필요가 정말 있는지를 다시 보자. *"수만 개"* 정도의 어림으로 충분하다면 통계 테이블에서 가져오거나 캐시해 두는 길도 있다. count는 페이지네이션과 분리해서 다루는 편이 깔끔하다.

다섯째, *Spring Data `Page<T>`와 keyset을 섞어 쓴다*. `Page<T>`는 *OFFSET 페이지네이션을 전제로 설계*된 추상이다. `getTotalElements()`, `getTotalPages()`, `getNumber()` 같은 메서드가 페이지 번호 UI를 가정한다. keyset으로 옮기면 `Window<T>`나 직접 만든 cursor DTO를 쓰는 편이 인터페이스 결이 맞다. `Page<T>`를 그대로 두고 cursor를 *추가로* 노출하는 어색한 형태가 자주 보이는데, 깔끔히 한쪽으로 정리하는 편이 낫다.

이 다섯 가지는 keyset 마이그레이션의 단골 함정이다. 외워두자. 살짝 찜찜한 자리를 발견했다면 그 자리에서 한 번 더 의심하는 편이 낫다. 의심하지 않고 넘어간 코드가 어느 새벽 알람을 깨운다.

## 다음 장과 이어지는 자리

이 장에서 OFFSET을 keyset으로 옮기는 도구 상자를 모두 꺼냈다. *왜 OFFSET이 무너지는가*에서 시작해 *튜플 비교* 패턴, *Blaze-Persistence*의 자동 생성, *Spring Data 3.x*의 `ScrollPosition`, *Hibernate 6*의 JPQL window function까지. 그리고 4장의 HHH000104와 5장의 projection이 keyset과 합쳐지면 *list API의 정석 형태*가 손에 잡힌다는 점도 확인했다.

여기서 한 가지가 자연스럽게 떠오른다. *이 모든 도구가 잘 동작하는지를 어떻게 확인할 것인가?* 우리 코드의 list API에 keyset이 들어갔다고 해서, *그게 의도대로 동작*하는지를 운영에서 어떻게 보증할 것인가? 응답시간 분포는 어떻게 측정하고, SQL 패턴은 어떻게 모니터링하고, depth-independent 속성을 *영구히* 보증할 회귀 테스트는 어떻게 짜야 할까? *코드만 봐서는 모를 비용을 어떻게 보이게 만들* 것인가?

이 질문이 다음 11장의 주인공이다. SQL 로깅, datasource-proxy, Hibernate Statistics, FlexyPool metrics, Hypersistence Optimizer. 책 전체에서 다뤄온 도구들을 한 챕터에 모은다. 그리고 11장 마지막에서는 1장부터 11장까지의 *36개 체크리스트*를 한 표에 회수한다. 책을 덮고 우리 코드로 돌아가는 자리다.

## 마무리 — 잊지 말자

이 장은 한 가지 질문에서 시작했다. *OFFSET 10,000을 넘기는 순간 왜 응답시간이 무너지는가?* 답은 한 줄이다. *OFFSET은 앞을 다 읽고 버린다*. 깊이가 깊을수록 비례해서 비용이 늘어난다. 인덱스가 있어도 그 *훑고 버리는* 비용은 사라지지 않는다.

그래서 우리는 keyset(seek method)으로 옮긴다. *방금 본 자리부터 잇는다*. `WHERE (created_at, id) < (?, ?) ORDER BY created_at DESC, id DESC LIMIT 20`. 튜플 비교 한 줄이 핵심이다. tie-breaker로 PK를 마지막에 한 줄 더. NULL 컬럼은 가능하면 keyset 키로 쓰지 않는다. 부호가 섞이면 분기를 손으로 풀어 쓴다.

직접 짜기가 번거롭다면 도구의 힘을 빌리자. *Blaze-Persistence*는 `withKeysetExtraction(true)` 한 줄로 분기를 자동 생성한다. *Spring Data 3.x*는 `ScrollPosition.keyset()`으로 keyset을 1급 시민으로 만들었다. `WindowIterator`로 전체 순회까지. *Hibernate 6*는 JPQL window function으로 count 쿼리를 본 쿼리에 흡수한다. SQM이 가능하게 한 새 풍경이다.

4장의 HHH000104(컬렉션 fetch + 페이지네이션)는 keyset과 만나도 그대로 살아 있다. 2-query 패턴에 keyset을 끼우거나, ToMany는 `@BatchSize`로 묶어 한 쿼리에 끝내자. 5장의 projection과 결합하면 list API의 *정석 형태*가 떨어진다. *깊이 무관 + 가벼운 row + PersistenceContext 비용 없음*. 핫한 list API에 이 정석 형태를 시범 적용해 보자. p99의 long tail이 *눈에 띄게* 줄어든다.

마지막으로, 한 가지를 마음에 새겨 두자. *우리 list API의 깊은 페이지가 얼마나 느린지는 우리만 안다*. Vlad의 책에도, 이 챕터에도, 우리 서비스의 페이지 500 응답시간이 적혀 있지 않다. 측정해 보지 않으면 모른다. 책을 덮고 우리 모니터링 대시보드를 열어 list API 한두 개의 페이지 깊이별 응답시간을 *지금* 한 번 들여다보는 30분이 우리 코드의 OFFSET 함정을 찾는 유일한 길이다. 30분의 측정이 다음 새벽의 알람을 막는다.

### 내 코드 체크리스트 3개

- 우리 서비스의 가장 큰 list API가 OFFSET 기반인지, keyset 기반인지(application 코드와 SQL을 한 번씩 확인하자).
- 정렬 컬럼이 tie를 만들 수 있을 때 두 번째 정렬 키(보통 PK)가 ORDER BY에 함께 들어가 있는지.
- 깊은 페이지(예: 500페이지 또는 cursor 깊이 10,000) 응답시간을 첫 페이지와 비교 측정해 본 적이 있는지.

다음 장에서는 *보이지 않는 비용을 보이게* 만드는 도구 상자를 연다. SQL 로깅, datasource-proxy, Hibernate Statistics, FlexyPool, Hypersistence Optimizer. 그리고 책 전체의 36개 체크리스트를 한 표에 모은다.
