# 12장. 그리고 그 다음 — 운영 기능과 다음 세계

긴 길을 함께 걸어왔다. 1장 회의실 풍경에서 출발해, 라운드트립과 트랜잭션이라는 두 단어로 모든 비용을 풀어보자고 약속했다. 그 약속이 2장 커넥션, 3장 엔티티, 4장 N+1, 5장 Projection을 거쳐 7장 캐시와 8장 락, 10장 페이지네이션까지 한 줄로 이어졌다. 11장에서는 그 모든 비용을 *보이게* 만드는 도구 한 세트와 함께, 36개 체크리스트를 한 표로 펼쳐봤다.

자, 그렇다면 이제 무엇이 남았을까? 두 가지가 남았다.

하나는 *오늘 당장* 우리 서비스에 보탤 수 있는 운영 기능이다. 감사 로그, 소프트 삭제, 멀티 테넌시, 스토어드 프로시저 같은 것들. 책 전체에서 한 번씩 스치긴 했지만, 정면으로 다뤄 한 자리에 모아두지는 않았다. 자기 도메인에 막 손이 가던 자리들이다. 다른 하나는 *이 책 다음에 펼칠 자료의 지도*다. Hibernate 6의 신기능, JPA + jOOQ의 분업, Jakarta Data, Reactive — 이 책의 영역 바깥에 있지만 지금 우리 손이 닿을 만한 곳에 놓인 도구들. 책 한 권으로 모든 것을 다룰 수는 없으니, 그 자리에서 한 발 더 나갈 때 어디로 가야 하는지를 가리켜둬야 한다.

이 마지막 장은 그 두 가지를 한 챕터로 묶는다. 12.1에서는 오늘 쓸 수 있는 운영 도구 네 가지를, 12.2에서는 다음 세계의 여섯 가지 자리를 걷는다. 그리고 12.3에서 책을 닫는다. 닫으면서 1장의 북극성을 다시 한 번 가리키고, 11장의 체크리스트를 *오늘 코드 한 줄부터*의 약속으로 회수한다.

가볍게 가자. 깊은 디테일은 각 도구의 공식 문서와 책 마지막 부록에 미뤄두고, 이 장에서는 *어떤 자리에 어떤 도구가 있는지*를 함께 그려두자.

## 12.1 운영 기능 — 오늘 쓸 수 있는 도구

자기 서비스에 어느 정도 트래픽이 쌓이고, 도메인이 일정 크기를 넘기면 반드시 마주치는 운영 요구가 있다. *"이 데이터가 언제 누구에 의해 어떻게 바뀌었는지 추적해야 한다"*는 감사 요구, *"이 사용자가 탈퇴했는데, 그가 남긴 주문 데이터는 어떻게 처리하지?"* 같은 소프트 삭제 요구, *"이 SaaS를 여러 회사가 같이 쓰는데, 데이터를 어떻게 격리하지?"*라는 멀티 테넌시 요구, *"이 분석 쿼리는 너무 무거우니 DB 함수로 캡슐화하자"*는 스토어드 프로시저 요구. 네 가지 모두 JPA 표준이 정면으로 답을 주지는 않는다. Hibernate에는 그러나 *손이 닿는 자리*에 도구가 마련돼 있다. 한 번에 정리하고 가자.

### Audit — Envers의 자리와 한계

먼저 감사 로그부터 시작하자. *"이 게시글이 언제 누구에 의해 수정됐는지를 보고 싶다"*는 요구는 비즈니스 도메인 어디에나 들어온다. 회계, 의료, 보험은 *법적으로* 요구한다. 그 외에도 보안 사고가 났을 때 *누가 무엇을 만진 마지막 사람인가*를 추적해야 하는 자리가 늘 있다.

가장 단순한 답은 *모든 도메인 객체에 `updatedAt`, `updatedBy` 같은 컬럼을 박는 것*이다. JPA에 `@PreUpdate` 리스너를 걸어두면 자동으로 채워진다. 이 방법은 가볍지만 한계가 있다. *변경 시점만* 알 수 있고 *변경 전의 값*은 모른다. 어떤 컬럼이 바뀌었는지, 이전 값은 무엇이었는지를 알려면 별도 테이블이 필요하다.

여기에 답으로 자주 등장하는 도구가 **Hibernate Envers**다. 엔티티 클래스에 `@Audited` 한 줄만 붙이면 Hibernate가 자동으로 `_AUD` 미러 테이블을 만들어준다. 그 엔티티에 INSERT/UPDATE/DELETE가 일어날 때마다 미러 테이블에 *revision 번호*와 함께 이력을 한 줄 박는다.

```java
@Entity
@Audited
public class Post {
    @Id @GeneratedValue
    private Long id;

    private String title;

    @ManyToOne(fetch = FetchType.LAZY)
    private User author;
}
```

이 한 줄을 붙이고 나면 `post_aud`라는 미러 테이블이 자동으로 만들어진다. 거기에는 `id`, `title`, `author_id` 같은 원본 컬럼에 더해, `rev`라는 revision 번호와 `revtype`(0=INSERT, 1=UPDATE, 2=DELETE)이 함께 박힌다. 별도로 `revinfo` 테이블이 만들어져 각 revision의 타임스탬프와 (커스터마이즈하면) 작성자 정보를 담는다. 이력 조회는 `AuditReader`로 한다.

```java
AuditReader reader = AuditReaderFactory.get(em);
Post oldVersion = reader.find(Post.class, postId, revisionNumber);
List<Number> revisions = reader.getRevisions(Post.class, postId);
```

손에 잡힌 듯 편하다. 그런데 운영을 좀 해보면 Envers의 *한계*가 보이기 시작한다.

첫째, *_AUD 테이블이 빠르게 폭발한다*. 게시글 한 줄의 모든 변경마다 `post_aud`에 한 줄이 박힌다. 댓글 수 카운트, 좋아요 카운트, 마지막 활동 시각 같은 *자주 바뀌는 컬럼*이 끼어 있으면 미러 테이블이 원본보다 100배 커지는 일이 흔하다. 한 게시판 사이트의 운영자가 *post 테이블 2GB, post_aud 테이블 200GB*가 됐다는 이야기가 종종 나온다. 정말 끔찍한 일이다.

둘째, *모든 변경마다 INSERT가 한 번 더 일어난다*. 쓰기 트래픽이 두 배가 되는 셈이다. 평시에는 별 문제가 안 되지만, 쓰기 부하가 높은 시스템에선 Envers를 켜는 순간 throughput이 절반으로 떨어질 수 있다. 또한 미러 테이블 INSERT가 같은 트랜잭션 안에서 일어나므로, 트랜잭션이 그만큼 길어진다. 트랜잭션이 길어진다는 게 무엇을 뜻하는지는 6장에서 보았다 — 커넥션 점유 시간이 늘고, 락이 길어지고, 시스템 전체 throughput이 떨어진다.

셋째, *스키마 변경에 약하다*. 컬럼 하나를 추가하면 `_AUD` 테이블에도 같은 컬럼을 추가해야 한다. 컬럼 타입을 바꾸면 이력의 *이전 값*을 어떻게 해석할지 정해야 한다. 운영하다 보면 마이그레이션 스크립트가 두 배로 늘어난다. 번거롭다.

그렇다면 어떻게 해야 할까? 답은 *Envers를 자기 자리에 정확히 쓰는 것*이다. Envers가 빛나는 자리는 *변경 빈도가 낮고 추적이 필수인 도메인*이다. 회원의 약관 동의 이력, 보험 계약 변경, 의료 처방 이력, 회계 분개 — 이런 자리는 변경 자체가 자주 일어나지 않고, *모든 변경을 빠짐없이 보존해야 한다*. Envers의 비용을 정당화할 수 있다.

반면 *쓰기 부하가 높은 일반 도메인*에서는 다른 접근으로 가야 한다. 게시판, 채팅, 활동 로그, 캐시성 카운트가 끼어 있는 도메인은 Envers의 *INSERT 두 배* 비용을 감당하기 어렵다.

이 자리에 등장하는 대안이 **CDC + Debezium**이다. Change Data Capture, 우리말로는 변경 데이터 캡처다. 핵심 아이디어는 단순하다. *DB의 트랜잭션 로그(MySQL의 binlog, PostgreSQL의 WAL)를 읽어서 변경 이벤트를 외부로 흘려보낸다*는 발상이다. 애플리케이션이 INSERT/UPDATE/DELETE를 *모를 필요가 없다*. 트랜잭션이 커밋되면 DB가 알아서 로그에 변경을 쓰고, Debezium이 그 로그를 읽어 Kafka 같은 메시지 브로커로 흘려보낸다. 다운스트림에서는 그 이벤트를 *감사 로그 저장소*, *데이터 웨어하우스*, *검색 인덱스* 등 자기가 원하는 자리로 옮길 수 있다.

Envers와 비교하면 어떨까? CDC + Debezium의 *큰 이점*은 셋이다. 첫째, *애플리케이션의 트랜잭션이 길어지지 않는다*. 미러 INSERT가 같은 트랜잭션에 끼어들지 않으므로, 운영 부하가 거의 0이다. 둘째, *모든 테이블에 일괄 적용된다*. 새 테이블을 만들 때마다 `@Audited`를 붙이는 일을 잊지 않아도 된다. 셋째, *감사 데이터의 저장소를 분리할 수 있다*. 본 DB는 가볍게 유지하고, 감사 로그는 *값싼 저장소*(예: S3, BigQuery)에 옮긴다. 디스크 비용이 십분의 일로 떨어진다.

물론 Debezium에도 단점이 있다. *별도 인프라*(Kafka Connect)가 필요하고, *DB의 binlog/WAL 형식과 강하게 결합*되며, *DDL 변경을 따라가는 운영이 만만치 않다*. 작은 팀이 도입하기에는 무겁다. 다만 한 가지는 분명하다. *쓰기 부하가 있고 감사 요구가 있는 시스템이라면, Envers 한 가지에 모든 걸 맡기는 시대는 지나갔다*. 자리에 따라 Envers와 Debezium을 *섞어 쓰는 것이 합리적*이다.

그렇다면 자기 도메인에서 무엇을 골라야 할까? 단순한 결정 트리 하나를 들고 가보자. *그 엔티티의 변경 빈도가 일 100건 이하인가? 그리고 모든 변경의 *이전 값*까지 빠짐없이 보존해야 하는가?* 둘 다 그렇다면 Envers가 가벼운 답이다. *변경 빈도가 일 1만 건 이상인가? 그리고 외부 분석 시스템과의 연계가 필요한가?* 둘 다 그렇다면 Debezium 쪽으로 기우는 편이 낫다. 그 사이는 *자기 팀의 운영 역량과 인프라*가 가르는 회색 지대다.

### Soft Delete — `@SoftDelete` 어노테이션의 시대

다음으로 소프트 삭제로 옮겨가자. 사용자가 *삭제* 버튼을 누르긴 했지만, 실제로는 DELETE를 치지 않고 *삭제 표시*만 해두는 흔한 패턴이다. *"실수로 지웠다고 복구 요청이 오면 어떡하지?"*, *"감사 대비 데이터는 보존해야 한다"*, *"외래키로 묶인 다른 테이블이 깨질까 무섭다"* 같은 이유에서 도입된다.

Hibernate 6.4 이전 시대의 표준 패턴은 두 어노테이션을 조합하는 것이었다.

```java
// 구식 패턴 — 6.4 이전
@Entity
@SQLDelete(sql = "UPDATE post SET deleted = true WHERE id = ?")
@Where(clause = "deleted = false")
public class Post {
    @Id @GeneratedValue
    private Long id;
    private String title;
    private boolean deleted;
}
```

`@SQLDelete`로 *DELETE SQL을 UPDATE로 갈아끼우고*, `@Where`로 *모든 조회에 WHERE 조건을 자동으로 박는다*. 작동은 한다. 그런데 손맛이 좀 그렇다.

첫째, `@Where`는 *원시 SQL 조각*이다. 컴파일러가 검증해주지 않는다. 컬럼 이름을 잘못 적으면 런타임에 SQL 오류가 난다. 둘째, JPQL의 `WHERE` 절과 `@Where`가 *어떻게 합쳐지는지*가 직관에 어긋난다. `findByTitle("hello")`를 부르면 실제 SQL은 `WHERE title = 'hello' AND deleted = false`가 나간다. 두 조건이 자동으로 AND로 묶이는데, 이게 *복잡한 OR 조건*과 어떻게 결합되는지가 흐릿하다. 셋째, *연관관계 fetch*에서 `@Where`가 어떻게 적용되는지가 미묘하다. `Post -> Comment`를 fetch join하면 *댓글의 `deleted` 컬럼*도 함께 필터링되는데, 정확히 어떤 조건이 어디 붙는지를 추적하기가 번거롭다.

이 모든 손맛을 한 번에 정리하는 답이 **Hibernate 6.4에서 도입된 `@SoftDelete` 어노테이션**이다. 한 줄로 끝난다.

```java
// 새 패턴 — Hibernate 6.4+
@Entity
@SoftDelete
public class Post {
    @Id @GeneratedValue
    private Long id;
    private String title;
}
```

`@SoftDelete` 한 줄을 붙이면 Hibernate가 *자동으로* `deleted` 컬럼을 추가하고(또는 기존 컬럼을 활용하고), DELETE SQL을 UPDATE로 갈아끼우고, 모든 조회에 WHERE 조건을 박는다. 컬럼 이름과 타입을 바꾸고 싶다면 `@SoftDelete(columnName = "is_active", converter = ReversedBooleanConverter.class)` 같은 옵션으로 조정할 수 있다.

Vlad의 표현을 빌리면 이렇다 — *"much easier to just use the native Hibernate mechanism."* 직역하면 *"그냥 Hibernate의 네이티브 메커니즘을 쓰는 편이 훨씬 쉽다"*는 말이다. 정말 그렇다. 어노테이션 한 줄이 패턴 두 줄을 대체하고, 검증·결합·연관관계 처리가 *Hibernate 내부에서* 일관성 있게 일어난다.

만약 자기 코드베이스에 *구식 `@SQLDelete` + `@Where` 조합이 깔려 있고* Hibernate 6.4+를 쓰고 있다면, 시간 날 때 한 번 마이그레이션을 검토해볼 만하다. 코드도 줄어들고, 미묘한 결합 동작에 대한 불안도 줄어든다. 다만 옮길 때 한 가지는 주의해야 한다 — `@SoftDelete`는 *Hibernate가 컬럼 이름을 디폴트로 `deleted`*로 가정한다. 기존 컬럼 이름이 `is_deleted`, `del_yn`, `deleted_at` 같이 다르다면 `columnName` 옵션으로 정확히 매핑해주자. 디폴트만 믿고 두면 새 컬럼이 추가되고 기존 컬럼이 같이 살아남는 *끔찍한 상황*이 벌어진다.

그리고 한 가지 더 짚어두자. 소프트 삭제 자체에 대한 *함정*이 있다. Vlad가 자주 이야기하는 지점이다.

> "Soft deletes can barely guarantee consistent behavior when related entities reference the deleted row." — Vlad Mihalcea의 표현 요약

소프트 삭제는 *연관된 엔티티가 삭제된 row를 가리킬 때 일관된 동작을 보장하기 어렵다*는 뜻이다. `Post`가 *소프트 삭제*됐다. 그런데 `Comment.post` 외래키가 그 `Post`를 가리키고 있다. *댓글을 조회하면 어떻게 될까?* 부모 `Post`는 *논리적으로는 삭제됐지만 물리적으로는 살아 있다*. 조회는 되는데 비즈니스 의미상으로는 안 된다. `comment.getPost()`를 부르면 *논리적으로 삭제된 Post*가 돌아온다. 이 자리에서 NullPointerException을 기대하던 코드라면 깨진다. 반대로 *조회되지 않기를 기대하던 자리*라면 또 다른 모양으로 깨진다.

그래서 소프트 삭제는 *도메인에 대한 의식적 결정*이 필요하다. *진짜 삭제가 정답인가? 아니면 상태 컬럼이 정답인가?* 후자라면 차라리 *명시적 상태 머신*(`status = 'ACTIVE' | 'ARCHIVED' | 'DELETED'`)으로 모델링하는 편이 낫다. 상태가 의미를 가지면 코드도 그 의미를 따라간다. *그냥 데이터를 안 지우고 숨기고 싶어서* 소프트 삭제를 고른 거라면, 그 결정을 한 번 더 의심해볼 만하다.

### Multi-tenancy — 세 가지 전략의 선택

이번엔 멀티 테넌시로 옮겨가자. 한 시스템을 여러 *테넌트*(통상 회사, 조직, 워크스페이스 같은 단위)가 공유할 때, 그들 사이의 데이터를 *어떻게 격리할 것인가*라는 질문이다.

크게 세 가지 전략이 있다. *Database-per-tenant*, *Schema-per-tenant*, *Discriminator 컬럼*. 각각의 자리와 비용을 정리해보자.

**첫째, Database-per-tenant.** 테넌트마다 *완전히 별도의 DB*를 둔다. 격리는 가장 강하다. 한 테넌트의 데이터가 다른 테넌트로 누설될 가능성이 *물리적으로* 차단된다. 백업·복원·암호화·물리 위치 같은 *컴플라이언스 요구*가 강한 도메인(의료, 금융, 정부)에서 자주 선택된다. 비용은 무엇일까? *운영 비용*이 가장 크다. 100개의 테넌트는 100개의 DB 인스턴스(또는 적어도 100개의 connection pool, 100개의 백업 스케줄, 100개의 모니터링 대시보드)를 뜻한다. 마이그레이션을 한 번 돌리려면 100번을 돌려야 한다. *DDL 변경의 운영*이 정말 번거롭다.

**둘째, Schema-per-tenant.** 같은 DB 인스턴스 안에 *테넌트마다 별도의 스키마*를 둔다. PostgreSQL의 `SET search_path` 또는 MySQL의 database(스키마와 동치)로 구현한다. 격리는 중간 수준이다. 같은 DB 프로세스를 공유하지만, 테이블 자체는 분리되어 있어 *실수로 다른 테넌트의 데이터를 읽을* 위험이 줄어든다. 운영은 *Database-per-tenant보다 가볍다* — 같은 DB의 같은 커넥션 풀을 공유할 수 있다. Hibernate에서는 `MultiTenantConnectionProvider`로 *요청별로 search_path를 바꿔서* 구현한다. 다만 마이그레이션은 여전히 *스키마마다 돌려야 한다*. PostgreSQL이라면 스키마가 1,000개를 넘어가면 `pg_class` 같은 카탈로그가 커져 *카탈로그 자체의 쿼리가 느려지는* 자리가 생긴다.

**셋째, Discriminator 컬럼.** 모든 테이블에 *`tenant_id` 컬럼*을 박고, 모든 쿼리에 *`WHERE tenant_id = :current`* 조건을 자동으로 더한다. 격리는 가장 약하다 — 한 줄의 코드 실수가 다른 테넌트 데이터로 가는 길을 연다. 그래서 *애플리케이션 레이어에서 강제*하는 것이 핵심이다. 운영 비용은 가장 가볍다 — DB 인스턴스 하나, 스키마 하나, 테이블 하나. 새 테넌트 추가는 *INSERT 한 줄*이다. SaaS의 빠른 성장기에 가장 자주 선택된다.

Discriminator를 고르면 한 가지 *기술적 도전*이 생긴다. *모든 SQL에 `WHERE tenant_id = :current`를 빠짐없이 박는 것*이다. 비즈니스 코드 한 줄이라도 빠뜨리면 다른 테넌트의 데이터를 *실수로 읽는다*. 끔찍한 일이다.

그렇다면 어떻게 강제할 수 있을까? 두 가지 답이 있다. Hibernate 6의 *`@TenantId` 어노테이션*과, 2장에서 등장했던 *`StatementInspector`*다.

`@TenantId`는 가장 깔끔한 답이다. 엔티티에 *현재 테넌트 컬럼*을 표시해두면 Hibernate가 자동으로 모든 쿼리에 WHERE 조건을 더하고, INSERT에 값을 채워준다.

```java
@Entity
public class Post {
    @Id @GeneratedValue
    private Long id;

    @TenantId
    private String tenantId;

    private String title;
}
```

이 한 줄을 붙이고 나면 Hibernate가 `CurrentTenantIdentifierResolver`를 호출해 *현재 요청의 tenant ID*를 가져와, 모든 SELECT/UPDATE/DELETE의 WHERE에 박는다. 좋다.

그런데 *모든* SQL이 다 거기를 지나가는 게 아니다. 예를 들어 *native query*(`em.createNativeQuery(...)`)나 *JdbcTemplate 직접 호출*, 또는 *jOOQ나 MyBatis 같은 외부 ORM과의 공존* 코드가 끼어 있다면 `@TenantId`로는 막을 수 없다. 그런 자리에서는 *모든 SQL을 가로채는 외피*가 필요하다. 그 자리에 `StatementInspector`가 등장한다.

2장에서 우리는 `StatementInspector`를 *SQL 가시화* 도구로 만났다. Hibernate가 JDBC에 SQL을 던지기 직전에 모든 SQL을 통과시키는 *얇은 후크*다. 이 후크는 *SQL을 보기*만 하는 게 아니라 *고칠 수도 있다*. WHERE 절에 `tenant_id` 조건을 *없으면 추가*하는 식의 방어선을 여기서 칠 수 있다.

```java
public class TenantInspector implements StatementInspector {
    @Override
    public String inspect(String sql) {
        if (!isTenantSafe(sql)) {
            throw new IllegalStateException(
                "Tenant filter missing in SQL: " + sql);
        }
        return sql;
    }
}
```

가장 단순한 형태는 *조건이 없는 SQL을 거부*하는 방어선이다. 더 적극적으로는 *조건을 자동으로 주입*할 수도 있지만, SQL 파서가 필요한 작업이라 일반적으로는 거부 모드로 두는 편이 안전하다. CI 단계에서 *모든 native query에 tenant_id 조건이 박혀 있는지*를 검증하는 정적 분석을 더하면 한 층의 안전판이 더 생긴다.

이 패턴이 1장의 *"라운드트립과 트랜잭션 동작"*과 2장의 *`StatementInspector`*가 만나는 자리다. *모든 SQL이 통과하는 한 자리*가 있다는 사실 — 그것이 가시화에도, 강제 주입에도, 멀티 테넌시 방어에도 쓰인다. 한 도구가 여러 역할을 한다는 사실 자체가 *Hibernate 설계의 우아한 지점*이다.

자기 시스템이 어느 전략으로 가야 하느냐는 *컴플라이언스 요구*, *테넌트 수와 성장 속도*, *팀의 운영 역량* 세 변수가 가른다. 컴플라이언스가 까다롭고 테넌트가 적다면 Database-per-tenant. 그 외 SaaS의 일반적인 자리는 *Discriminator + `@TenantId` + `StatementInspector` 방어선* 조합이 가장 균형이 좋다. Schema-per-tenant는 *그 둘 사이의 어중간한 자리에 종종 머무는* 선택이다 — 정말 그게 우리 자리에 답인지 한 번 더 의심해보자.

### Stored Procedure와 `FunctionContributor` — DB 함수를 도메인으로

운영 기능 네 번째, 스토어드 프로시저로 가자. *DB 안에 정의된 함수나 프로시저*를 JPA에서 호출하는 패턴이다.

스토어드 프로시저는 한국 SI에서 한때 *표준*이었고, 마이크로서비스의 시대에 한 발 물러섰다가, *분석 쿼리*와 *복잡한 데이터 변환*의 자리에서 다시 손이 가는 도구다. 비즈니스 로직을 DB로 끌어내리는 일반적 권고와는 거리가 있지만, *순수한 데이터 가공*에는 여전히 강하다. 거대한 GROUP BY와 윈도우 함수가 끼어 있는 분석 쿼리를 한 번 보자. 같은 쿼리를 JPQL이나 jOOQ로 풀어내는 것보다 *DB에 함수로 박아두고 호출하는 편*이 더 명료한 경우가 있다. 특히 *여러 클라이언트가 같은 분석 쿼리를 부르는* 자리라면, DB 함수가 *단일 소스*가 된다.

JPA에서 스토어드 프로시저를 부르는 표준 방법은 `@NamedStoredProcedureQuery`다.

```java
@NamedStoredProcedureQuery(
    name = "Post.popularInLastWeek",
    procedureName = "popular_posts_last_week",
    parameters = {
        @StoredProcedureParameter(
            name = "min_views", type = Integer.class,
            mode = ParameterMode.IN),
        @StoredProcedureParameter(
            name = "result", type = void.class,
            mode = ParameterMode.REF_CURSOR)
    }
)
@Entity
public class Post { /* ... */ }
```

호출은 `EntityManager`로 한다.

```java
StoredProcedureQuery query = em.createNamedStoredProcedureQuery(
    "Post.popularInLastWeek");
query.setParameter("min_views", 100);
List<Post> posts = query.getResultList();
```

`IN`, `OUT`, `INOUT` 파라미터와 `REF_CURSOR`까지 표준이 지원한다. 다만 *DB 벤더마다 동작이 미묘하게 다른* 자리가 있어, 운영에서는 *벤더별 통합 테스트*가 필수다.

스토어드 프로시저까지 가지 않더라도, *DB 함수를 JPQL에 노출*하는 가벼운 패턴이 있다. **`FunctionContributor` SPI**가 그 자리다. Hibernate 6에서 도입된 인터페이스로, *DB의 native 함수를 JPQL에서 호출할 수 있게 등록*한다.

예를 들어 PostgreSQL의 `jsonb_extract_path_text` 함수를 JPQL에서 부르고 싶다고 해보자.

```java
public class PostgresFunctionContributor implements FunctionContributor {
    @Override
    public void contributeFunctions(FunctionContributions contributions) {
        contributions.getFunctionRegistry()
            .registerNamed("jsonb_extract_path_text",
                StandardBasicTypes.STRING);
    }
}
```

`META-INF/services/org.hibernate.boot.model.FunctionContributor`에 클래스를 등록하면 Hibernate가 부팅 시 자동으로 읽어들인다. 이제 JPQL에서 함수를 부를 수 있다.

```java
em.createQuery(
    "select function('jsonb_extract_path_text', " +
    "p.metadata, 'category') from Post p where p.id = :id",
    String.class)
  .setParameter("id", postId)
  .getSingleResult();
```

JPA 표준 밖이지만, Hibernate를 쓰는 한 *DB의 특수 함수를 손에 잡힌 듯 가깝게* 부를 수 있다. 5장에서 다룬 *`@Subselect`*와 짝이 되는 자리다. `@Subselect`가 *복잡한 SELECT 결과를 엔티티처럼 매핑*해주는 도구라면, `FunctionContributor`는 *DB의 함수를 JPQL에서 호출 가능한 일등 시민으로* 만들어준다. 분석 쿼리를 *도메인 코드로 끌어올리는* 두 갈래의 길이다.

이 도구들이 빛나는 자리는 분명하다 — *DB 벤더의 풍부한 기능을 활용하고 싶지만, 코드는 자바 도메인 안에 두고 싶을 때*. JPA의 추상화를 살리면서도 *벤더의 강점*을 손에 쥘 수 있다. 다만 한 가지는 기억해두자. *벤더의 특수 함수에 의존하는 코드*는 *벤더 이전 비용*을 키운다. *어디까지 의존할 것인가*를 의식적으로 결정하는 편이 낫다. *읽기 분석은 의존해도 좋다, 쓰기 핵심 로직은 의존하지 않는다*는 식의 경계가 한 가지 가이드다.

### 네 도구를 한 줄로 정리

여기까지가 12.1이다. 네 가지 운영 기능을 한 표로 정리하고 다음 절로 넘어가자.

| 도구 | 자리 | 좋은 자리 | 의심할 자리 |
|------|------|-----------|-------------|
| Hibernate Envers | 감사 로그 | 변경 빈도 낮고 추적 필수인 도메인 | 쓰기 부하 높은 도메인 — CDC로 |
| `@SoftDelete` (H6.4+) | 소프트 삭제 | 명확한 *논리적 삭제* 요구 | 상태 머신이 더 정확한 자리 |
| `@TenantId` + `StatementInspector` | 멀티 테넌시 Discriminator | 빠른 성장기 SaaS | 컴플라이언스 강한 도메인 — DB 분리로 |
| `@NamedStoredProcedureQuery` + `FunctionContributor` | DB 함수의 도메인화 | 분석·복잡 데이터 가공 | 핵심 비즈니스 로직 — 자바에 |

네 도구가 공통으로 가리키는 한 가지가 있다. *Hibernate는 ORM이지만, ORM 위에 운영 기능을 얹는 도구이기도 하다*는 사실이다. 우리는 종종 Hibernate를 *엔티티를 SQL로 바꾸는 매핑 도구* 정도로만 생각한다. 그런데 그 추상화를 잘 쓰면 *감사·삭제·격리·함수 호출* 같은 *횡단 관심사*까지 한 자리에 모을 수 있다. 이 시각 자체가 책 전체를 통해 자라는 무언가다.

## 12.2 다음 세계 — 한 발 더 나갈 자리

자, 이제 *다음 세계*로 옮겨가자. 이 절의 톤은 12.1과 다르다. 12.1은 *오늘 당장 손에 잡히는 도구*였다면, 12.2는 *책이 다 다루지 못한 영역에 대한 지도*다. 깊은 디테일을 풀어내기보다는, *어떤 자리에 무엇이 있고 왜 그것이 우리 다음 학습의 후보인가*를 가리킨다.

### Hibernate 6의 SQM — 윈도우, CTE, 멀티셋

먼저 Hibernate 6의 *SQM(Semantic Query Model)* 이야기로 들어가자. Hibernate 5와 6의 가장 큰 내부 변화 중 하나가 *쿼리 파서의 교체*다. 5의 ANTLR 기반 HQL 파서가 6의 SQM으로 갈아끼워졌다. 사용자 입장에서 즉시 보이는 차이는 두 가지다 — *컴파일이 빨라졌고*, *JPQL이 표현할 수 있는 SQL의 폭이 넓어졌다*.

뭐가 넓어졌을까? 네 가지를 꼽을 수 있다.

**첫째, 윈도우 함수.** 10장에서 페이지네이션의 표준 도구로 잠깐 등장한 그 윈도우 함수다. JPA 표준 JPQL은 윈도우 함수를 정의하지 않는다. Hibernate 6의 JPQL은 그것을 *문법 차원에서 받는다*. 키셋 페이지네이션의 *경계 계산*, 매출 분석의 *누적합*, *순위 매기기* 같은 자리에 사용자는 native SQL을 쓰지 않고도 손이 닿는다.

```java
List<RankedPost> ranked = em.createQuery(
    "select new com.acme.dto.RankedPost(" +
    "  p.id, p.title, " +
    "  row_number() over (partition by p.category order by p.views desc)) " +
    "from Post p", RankedPost.class)
  .getResultList();
```

5장에서 본 *DTO Projection*과 결합하면, *분석 쿼리를 DTO로 깔끔하게 가져오는* 길이 열린다.

**둘째, CTE(Common Table Expression).** WITH 절로 *중간 계산을 한 번 정의*하고 그것을 이름으로 부르는 패턴이다. 복잡한 쿼리의 *가독성*과 *재사용성*을 끌어올린다. Hibernate 6의 JPQL은 CTE를 받는다.

**셋째, derived table.** FROM 절 안에 *서브쿼리를 테이블처럼* 쓰는 패턴이다. 5장에서 다룬 *Projection 전략*의 변형으로 종종 등장한다.

**넷째, multiset.** *N+1을 단일 SQL로 푸는 새로운 방식*이다. 부모와 자식을 fetch join으로 묶지 않고, *각 부모의 자식들을 JSON 배열로 묶어 한 row에 담아 오는* 모양이다.

```java
List<PostWithComments> result = em.createQuery(
    "select new map(p as post, " +
    "  multiset(select c from Comment c where c.post = p) as comments) " +
    "from Post p where p.category = :cat", PostWithComments.class)
  .setParameter("cat", category)
  .getResultList();
```

이 한 줄이 *부모 + 자식들의 컬렉션*을 한 번의 라운드트립으로 가져온다. 4장에서 다룬 N+1, 5장의 Projection 전략, 10장의 페이지네이션 — 세 장의 도구가 *한 자리에서 합쳐지는* 모양이다. JPA 표준은 아니지만, Hibernate를 쓰는 한 *손에 잡힌 듯 가까운 도구*다.

이 네 가지는 책의 본문에서 자주 *예고*만 하고 정면으로 다루지 않았다. 5장과 10장에서 한 번씩 *"Hibernate 6의 새 도구로 더 우아하게 풀 수 있다"*고 짚어두기만 했다. 그 자리에 발을 디뎌 더 깊이 가고 싶다면, *Vlad의 Hibernate JPQL window functions 글*과 *Hibernate 사용자 가이드의 SQM 챕터*가 좋은 출발점이다.

### `@JdbcTypeCode` — JSON과 ARRAY를 native하게

다음 자리는 *JSON과 ARRAY 매핑*이다. PostgreSQL을 쓰는 팀이라면 한 번쯤 마주친다 — *`jsonb` 컬럼을 자바 객체로 매핑하고 싶다*, *`text[]` 컬럼을 `List<String>`으로 받고 싶다*는 요구다.

오래 전부터 답은 *Hypersistence Utils*(이전 이름 `hibernate-types`)였다. Vlad가 만든 외부 라이브러리를 의존성에 추가하고, `@Type` 어노테이션으로 명시하는 방식이다. 잘 작동했지만 *외부 라이브러리에 대한 의존*은 늘 한 줄의 부담이었다.

Hibernate 6에서 이 패턴이 *Hibernate 본체로 내부화*됐다. `@JdbcTypeCode`라는 새 어노테이션 한 줄이면 끝난다.

```java
@Entity
public class Post {
    @Id @GeneratedValue
    private Long id;

    @JdbcTypeCode(SqlTypes.JSON)
    private Map<String, Object> metadata;

    @JdbcTypeCode(SqlTypes.ARRAY)
    @Column(columnDefinition = "text[]")
    private List<String> tags;
}
```

이 한 줄로 PostgreSQL의 `jsonb`와 `text[]`가 *자바의 Map과 List로* 매핑된다. MySQL의 `JSON` 컬럼이나 Oracle의 SODA도 같은 어노테이션으로 받는다. 벤더에 따라 *내부 직렬화·역직렬화 전략*이 다르지만, 사용자 코드는 동일하다.

이 도구의 진가는 *Hypersistence Utils를 추가로 안 깔아도 된다*는 사실 자체에 있다. 의존성이 한 줄 줄어든다. 외부 라이브러리의 *버전 호환성 추적*이 사라진다. 작은 변화지만, 운영 시점에 부담을 한 줄 덜어주는 변화다.

다만 한 가지는 짚어두자. *JSON 컬럼에 무엇을 담을 것인가*는 *모델링 결정*이다. *자주 검색되는 필드*를 JSON에 묻어두면 검색 인덱스가 잘 작동하지 않는다. *항상 함께 다니는 보조 정보*는 JSON이 가볍지만, *비즈니스 핵심 속성*은 컬럼으로 분리하는 편이 낫다. *컬럼 vs JSON*의 경계는 *그 필드에 인덱스가 필요한가, 그 필드로 GROUP BY를 거는가, 그 필드의 변경이 다른 시스템에 이벤트로 흘러가야 하는가*의 세 질문으로 가른다.

### JPA + jOOQ — 경쟁이 아니라 분업

이번 자리가 12.2의 가장 큰 자리다. *JPA와 jOOQ의 관계*에 대해 한 번 정리하고 가자.

지금까지 인터넷의 글들은 두 도구를 *경쟁자*로 그려왔다. *"JPA vs jOOQ — 무엇이 더 빠른가?"*, *"JPA는 죽었다 — jOOQ로 옮겨라"* 같은 톤이다. 그런 글에 자극을 받으면 우리는 둘 중 하나를 *선택해야 한다*는 잘못된 압박을 느낀다. 그게 1장의 그 회의실에서 누군가가 *jOOQ로 갈아타자*는 글을 슬랙에 올린 풍경이다.

진짜 답은 다른 자리에 있다. *경쟁이 아니라 분업이다.*

먼저 두 도구의 *서로 다른 강점*을 정리하자.

**JPA(Hibernate)의 강점:**
- 엔티티의 *라이프사이클 관리*. INSERT/UPDATE/DELETE의 적절한 시점, dirty checking, write-behind, cascade.
- *PersistenceContext의 일관성*. 한 트랜잭션 안에서 같은 row를 두 번 보면 같은 인스턴스. 7장의 토대.
- *연관관계 그래프*. fetch plan, lazy/eager, 2차 캐시.
- *낙관락의 자연스러운 통합*. `@Version` 한 줄.

**jOOQ의 강점:**
- *type-safe SQL DSL*. 컴파일 타임에 모든 SQL을 검증.
- *DB 스키마에서 자동 생성된 코드*. 컬럼 이름, 타입, 외래키가 자바 코드로 노출.
- *복잡한 SELECT의 표현력*. window function, CTE, lateral join, recursive — DB의 모든 기능에 *손이 닿는 가까움*.
- *결과 매핑의 유연함*. 엔티티에 묶이지 않고 *Record, Map, POJO, DTO* 어느 모양으로도.

두 도구를 *경쟁자로* 두면 어느 한쪽이 다른 쪽을 압도해야 한다. 그런데 정직하게 보면 두 도구는 *완전히 다른 자리에서 빛난다*. JPA는 *write 라이프사이클*에서, jOOQ는 *복잡한 read*에서. 이것을 솔직히 받아들이면 *두 도구를 함께 쓰는* 길이 열린다.

벤치 수치를 한 번 보자. **ORM Battle 2025**라는 벤치마크가 있다. *Hibernate, jOOQ, Plain JDBC*를 다양한 시나리오로 비교한 결과다.

| 시나리오 | JDBC | jOOQ | Hibernate(엔티티) |
|----------|------|------|-------------------|
| 단순 SELECT (1만 row) | 100% (기준) | 90~95% | 70~80% |
| 복잡 SELECT (조인+필터) | 100% | 90~95% | 60~75% |
| 매핑+dirty checking 있는 UPDATE | — | 90% | 95%+ |
| 대량 INSERT (배치) | 100% | 95% | 90~95% (StatelessSession 시 거의 동등) |

이 표가 가리키는 한 가지가 있다. *단순 read에서 JDBC > jOOQ > Hibernate(엔티티)*의 차이는 분명히 있다. 다만 그 차이는 *종종 10~30%*다. *3배 차이* 같은 극단적인 수치가 아니라, 같은 자릿수 안의 차이다. 그리고 *write*에서는 *Hibernate가 jOOQ + 수동 dirty 추적과 거의 비등*하다. Hibernate의 dirty checking이 *공짜로* 해주는 일을 jOOQ에서 수동으로 구현해야 하는 비용이 있기 때문이다.

이 결과를 받아들이면 *합리적인 배치*가 보인다. **write는 Hibernate, read는 jOOQ.** 엔티티 라이프사이클 관리가 *공짜로* 일어나는 자리는 그대로 두고, *복잡한 read 쿼리*만 jOOQ로 옮긴다. 한 프로젝트 안에 *두 도구가 공존*한다. 점진적으로 도입할 수 있다 — *오늘 가장 무거운 read 한 자리*만 jOOQ로 옮겨도 가치를 본다.

Vlad의 표현을 빌리면 이렇다.

> "Use Hibernate for write transactions and entity lifecycle, use jOOQ for complex reporting and analytical queries. They complement each other." — Vlad Mihalcea의 입장

*보완 관계*라는 단어가 핵심이다. 한 도구를 *버리고* 다른 도구로 *옮기는* 사고를 *함께 쓴다*는 사고로 바꿔보자. 1장의 회의실에서 누군가 슬랙에 올렸던 *jOOQ로 갈아타자*는 글이, *jOOQ로 부분 도입하자*는 글로 바뀐다면, 우리 시스템은 어떻게 달라질까?

여기에 *Blaze-Persistence*라는 또 하나의 도구가 자리를 잡고 있다. Blaze-Persistence는 *Hibernate 위에 올라가는 쿼리 빌더*다. JPA Criteria의 한계를 넘어 *CTE, LATERAL JOIN, window function*까지 *type-safe하게* 표현하게 해준다. *jOOQ만큼 강하지는 않지만 Hibernate와 한 자리에서 자연스럽게 결합한다*는 자리에 선다. 4.7절의 *동적 쿼리 선택지*에서 등장한 그 자리다.

세 도구의 자리를 한 줄로 정리하면 이렇다.

| 도구 | 자리 |
|------|------|
| Spring Data Specification | 가벼운 동적 조건. 표준 Criteria의 wrapping. 복잡해지면 약하다. |
| Blaze-Persistence | JPA 안에 머물면서 *window·CTE·LATERAL*까지. *Hibernate와 동거*. |
| jOOQ | 완전한 *type-safe SQL DSL*. *codegen* 필요. *Hibernate와 동거*. |

*무엇이 우리 자리에 맞는가*는 *쿼리의 복잡도*와 *팀의 학습 비용*이 가른다. *복잡도가 점진적*이라면 Spring Data Specification → Blaze-Persistence → jOOQ 순으로 *점점 더 강한 도구로 옮겨가는* 흐름이 자연스럽다.

### Jakarta Data — Spring Data 표준화의 흐름

다음 자리는 *Jakarta Data*다. Jakarta EE의 새로운 스펙으로, *Spring Data의 인터페이스 기반 repository 패턴을 표준화*하려는 움직임이다.

지금까지 *인터페이스에 메서드 시그니처만 선언하면 구현체가 자동 생성*되는 패턴은 Spring Data의 전유물이었다.

```java
public interface PostRepository extends JpaRepository<Post, Long> {
    List<Post> findByCategoryOrderByCreatedAtDesc(String category);
    Optional<Post> findFirstByAuthorOrderByCreatedAtDesc(User author);
}
```

이 우아한 패턴이 표준이 아니어서, Quarkus의 Panache나 Micronaut Data는 *각자의 방식*으로 비슷한 기능을 제공했다. Jakarta Data는 이것을 *플랫폼 중립적인 표준*으로 만든다.

```java
@Repository
public interface PostRepository {
    @Find
    List<Post> byCategory(String category, Order<Post> sortBy);

    @Find
    Optional<Post> firstByAuthor(User author);
}
```

Hibernate 6.6부터 Jakarta Data 어노테이션의 *부분 지원*이 들어왔다. 완전한 시점은 Hibernate 7과 Jakarta EE 11 이후가 될 가능성이 높다.

이 흐름이 *왜 중요한가*. 두 가지 이유다.

**첫째, 플랫폼 이동의 비용이 줄어든다.** 지금까지 Spring에서 Quarkus나 Micronaut로 *옮기려고 했을 때* 큰 비용 중 하나가 *repository 코드의 재작성*이었다. Spring Data의 시그니처 컨벤션이 다른 프레임워크에선 통하지 않았기 때문이다. Jakarta Data가 자리잡으면 *같은 인터페이스가 여러 프레임워크에서 동작*한다. 의존성을 바꿔도 비즈니스 로직은 그대로다.

**둘째, *간결한 코드 스타일*이 표준이 된다는 신호다.** Spring Data의 한 줄짜리 시그니처는 *너무 많은 마법*이라는 비판을 받았지만, 결국 *생산성으로 사람들을 끌어당겼다*. 그 흐름이 표준으로 굳어지면, 새 자바 백엔드 코드의 *디폴트 모양*이 한 단계 가벼워진다.

Spring을 쓰는 한국 팀에게는 *당분간 직접적인 변화는 거의 없다*. Spring Data가 이미 충분한 자리에 있기 때문이다. 다만 *Quarkus와 Micronaut에 관심이 있는 팀*, 또는 *서버리스·GraalVM 네이티브 이미지의 흐름*을 따라가는 팀에게는 *주시할 만한 자리*다. *다음 분기 학습 계획에 한 줄을 비워두자*.

### Reactive(R2DBC) — 별개 패러다임이라는 솔직한 안내

이제 *Reactive*로 옮겨가자. *R2DBC*, *Spring Data R2DBC*, *Hibernate Reactive* — 비동기·반응형 DB 액세스의 도구들이다. *높은 동시성 환경에서 스레드를 적게 쓰면서도 throughput을 끌어올린다*는 약속을 한다. WebFlux의 시대 이후 자주 회자된다.

이 책은 *의도적으로* reactive를 정면으로 다루지 않았다. 그 이유를 솔직히 짚어두자.

**첫째, reactive는 별개 패러다임이다.** 동기 JPA의 *PersistenceContext, dirty checking, write-behind, 2차 캐시, lazy loading* 같은 개념의 *대부분이 reactive 세계에서는 다른 모양으로 존재하거나 아예 사라진다*. Hibernate Reactive조차도 *동기 Hibernate의 직접 포팅이 아니라 별도 엔진*이다. *책 한 권이 다 다루기 어려운 별도의 영역*이다.

**둘째, JPA를 잘 쓰는 것이 reactive보다 먼저다.** 많은 팀이 *JPA가 느리니까 reactive로 가자*는 결정을 한다. 그런데 책 11장까지 함께 걸어온 우리는 이제 안다 — *JPA가 느린 이유의 99%는 reactive로 갈 이유가 아니다*. 라운드트립이 많아서, 트랜잭션이 길어서, 인덱스가 없어서, 너무 많이 가져와서, 캐시를 잘못 켜서다. 이 모든 자리를 *손에 잡힌 도구로* 풀고 나면, *그래도 더 필요한가*를 물어볼 수 있는 자리에 선다. 거기서 *답이 그래도 reactive*라면, 그때 옮겨가는 편이 합리적이다.

**셋째, reactive의 비용은 *코드의 모양 전체*다.** `Mono`와 `Flux`가 비즈니스 로직의 모든 자리에 침투한다. *디버깅의 어려움*, *에러 처리의 변형*, *기존 라이브러리와의 비호환*이 함께 온다. 그 비용을 *충분히 정당화하는 자리*는 의외로 좁다. *수만 동시 연결을 한 인스턴스에서 처리해야 하는 게이트웨이*, *외부 API 호출의 fan-out이 큰 시스템* 같은 특수한 자리다. *일반적인 비즈니스 백엔드*는 거기 들어가지 않는다.

그래서 이 책은 *동기 JPA를 잘 쓰는 것이 reactive보다 먼저*라는 입장을 분명히 한다. 우리 시스템이 *JPA의 도구를 모두 쓴 뒤에도 부족한 자리에 있다*면, 그때 reactive를 *별개 영역의 책*에서 만나자. R2DBC와 Spring Data R2DBC가 가장 자연스러운 출발점이다.

### Hibernate 7 전망 — release note를 따라가는 습관

마지막으로 *Hibernate 7*에 대해 한 줄 짚어두자. 이 책의 베이스라인은 *Hibernate 6.x*다. 집필 시점에 6.6이 안정판이고 6.7이 마일스톤 단계다. Hibernate 7은 그 다음에 온다.

Hibernate 7의 주요 변화로 *예고된 자리*는 몇 가지다. *instance creation 모델의 변화*(엔티티 생성자 호출 시점이 더 명확해진다), *embeddable의 다형성 강화*, *Jakarta Data의 정식 지원 확대*, *StatelessSession의 추가 기능* 등. 다만 *release note는 살아 움직이는 문서*다. 책에 쓰인 어느 시점의 예고가 정식 릴리스에서 *조금 다른 모양*으로 나올 가능성은 늘 있다.

이 자리에서 *우리가 들고 갈 습관 하나*를 짚어두자. *Hibernate의 release note를 분기에 한 번씩 훑어보자*. 새 버전의 *changelog*를 본다. *deprecation 목록*을 본다. *새 어노테이션, 새 SPI, 새 함수*가 어떤 자리에 들어왔는지 본다. 한 번에 깊이 보지 않아도 좋다. *어떤 변화가 생겼는지에 대한 흐릿한 지도*만 머리에 두면, 나중에 그 도구가 필요해진 자리에서 *"아, 이걸 새로 받아주는 게 있었지"*를 떠올릴 수 있다. 이 작은 습관이 *몇 분기 뒤*의 자기 코드를 한 줄씩 가볍게 만든다.

### 여섯 자리를 한 줄로

12.2를 정리하고 12.3으로 넘어가자.

| 자리 | 의미 | 다음 학습의 후보 |
|------|------|------------------|
| Hibernate 6 SQM | JPQL이 표현하는 SQL의 폭 확장 | window function, CTE, multiset |
| `@JdbcTypeCode` | JSON·ARRAY를 native 매핑 | Hypersistence Utils 의존성 정리 |
| JPA + jOOQ | 경쟁이 아닌 분업 | 가장 무거운 read 한 자리에 jOOQ 부분 도입 |
| Jakarta Data | 인터페이스 repository의 표준화 | Hibernate 6.6+ 부분 지원 확인 |
| Reactive(R2DBC) | 별개 패러다임 — JPA 다음 자리 | 정말 필요한 자리만, 늦게 |
| Hibernate 7 | release note의 흐름 | 분기에 한 번 changelog 훑기 |

여섯 자리 모두 *책의 다음에 펼칠 지도*다. 한 자리에 한 분기씩 손을 가져가도 이 책의 *3배 깊이*에 도달할 수 있다. 다만 *모든 자리를 한 번에 다 가지는 않아도 된다*. 자기 시스템의 *지금 가장 가까운 한 자리*만 골라 한 발 더 가는 편이 합리적이다.

## 12.3 책의 닫음 — 라운드트립과 트랜잭션, 그 한 줄로

여기까지가 12장이다. 그리고 *이 책 전체의 끝*이다. 한 호흡 쉬고, 책을 닫는 자리로 가자.

### 북극성 다시 가리키기

1장의 회의실 풍경을 다시 떠올려보자. DB 응답시간은 10밀리초인데 API는 1.5초가 튀는 그 자리. 누군가가 *"JPA가 원래 좀 느려요"*라고 말하고, 또 누군가가 *jOOQ로 갈아타자*는 글을 슬랙에 올린 그 자리.

그 자리에서 우리는 한 가지 시각을 약속했다. **느린 JPA에는 이유가 있고, 그 이유는 거의 항상 *라운드트립과 트랜잭션 동작*에 있다**는 시각.

그 한 줄이 책 전체의 북극성이었다. 모든 챕터의 모든 도구가 결국 *같은 한 줄로 환원된다*. 다시 한 번 차례를 펼쳐보자.

**2장은 라운드트립의 가장 비싼 한 단계 — 커넥션 획득 — 를 본다.** 풀 사이즈를 키울수록 빨라진다는 직관을 의심한다. PreparedStatement 캐시, statement caching, JDBC batch의 default를 잡는다.

**3장은 엔티티의 모양을 만든다.** ID 전략(`IDENTITY` vs `SEQUENCE`)이 *그 자체로 라운드트립의 모양을 결정*한다는 사실을 본다. bytecode enhancement로 dirty checking과 lazy loading의 비용을 깎는다.

**4장은 가장 흔한 라운드트립 폭발 — N+1 — 의 정체를 풀어낸다.** join fetch, batch fetch, entity graph 셋의 자리를 가른다.

**5장은 *너무 많이 가져오는* 비용을 다른 각도에서 깎는다.** Projection의 시각이다. 엔티티 fetch는 *수정 의도가 있을 때만*. 그 외에는 DTO·Tuple·`@Subselect`로.

**6장은 트랜잭션의 자리를 정한다.** `@Transactional`의 디폴트 동작, OSIV를 끄는 결정, `readOnly=true`의 의미. 트랜잭션이 *언제 열리고 언제 닫히는가*가 라운드트립의 *맥락*이라는 시각.

**7장은 캐시의 자리에 의심을 던진다.** 1차 캐시는 *공짜로 강하다*. 2차 캐시는 *충분히 정당화될 때만*. 쿼리 캐시는 *드물게*. PersistenceContext가 *application-level snapshot*이라는 사실 자체가 캐시의 첫 번째 자리.

**8장은 동시성의 두 도구 — 낙관락과 비관락 — 의 합의를 본다.** *낙관이 디폴트, 비관은 정당화 필요*. MVCC와 PersistenceContext의 두 층 일관성을 한 번 더.

**9장은 대량 write의 모양을 다시 그린다.** `batch_size=25`, `order_inserts=true`, `StatelessSession`. 30분짜리 INSERT을 1분으로 줄이는 *한 줄짜리 설정*들.

**10장은 페이지네이션의 무너짐을 본다.** OFFSET이 비싼 이유, 키셋 페이지네이션의 안전성. 페이지를 *DB의 인덱스 시각*으로 다시 보기.

**11장은 모든 비용을 *보이게* 만든다.** datasource-proxy, `SQLStatementCountValidator`, Hibernate Statistics, FlexyPool metrics, Hypersistence Optimizer. *코드만 봐서는 모를 비용*을 *보이는 비용*으로 옮기는 도구 한 세트. 마지막에 12개 챕터의 36개 체크리스트 표.

**12장은 운영 기능 네 가지와 다음 세계 여섯 자리**를 본다. *책의 다음에 펼칠 지도*.

이 모든 챕터가 결국 한 줄을 가리킨다. *우리 시스템이 *얼마나 자주, 언제, 왜* DB와 왕복하는가*. 그리고 *그 왕복을 둘러싼 트랜잭션이 *언제 열리고 언제 닫히는가*. 두 질문에 정확히 답할 수 있는 시각이 곧 *Vlad의 시각*이고, 이 책이 함께 자라기를 바라는 그 시각이다.

### 36개 체크리스트 — 오늘 코드 한 줄부터

11장에서 우리는 36개 체크리스트를 한 표로 모아봤다. 매 챕터 끝에 *내 코드 점검 세 가지*가 있었고, 12개 챕터가 합쳐져 36개가 됐다.

그 표를 다시 펼치자는 게 이 자리의 약속이다. 다만 *한꺼번에 다 보지 말자*. 36개는 *오늘 모두 점검하기에는* 너무 많다. 한꺼번에 다 보려고 하면 한 자리도 깊이 못 본다. *책을 덮고 자기 코드로 돌아가는 자리*에서 우리에게 필요한 건 다른 약속이다.

**오늘 한 줄.** 36개 중 하나만 골라, *오늘 자기 IDE에서 30초 안에 확인*해보자. `grep -r "@Transactional" src/main/java/`를 친다. `application.yml`에서 `spring.jpa.open-in-view`를 찾는다. `entityManagerFactory`의 `hibernate.jdbc.batch_size`를 본다. 한 자리만. 30초.

**이번 주 다섯 줄.** 36개 중 자기 시스템에 *가장 의심스러운 다섯 자리*를 골라, 한 주에 한 자리씩 본다. 의심이 풀리든, 새 PR이 올라가든, 한 자리에 한 발이 닿는다.

**이번 분기 모두.** 36개를 분기 단위로 한 바퀴 돈다. 한 분기에 한 번씩 *우리 시스템의 JPA 건강 검진*을 한다. 점검 자체가 *습관이 되면* 시스템이 천천히 자라기 시작한다.

이 세 단위의 약속이 *책 한 권을 읽고 끝내지 않는* 한 가지 길이다. *읽고 자기 코드로 돌아가는* 사람을 만드는 길이다.

자, 이 마지막 챕터의 *내 코드 점검 세 가지*도 정리해두자.

**하나, 지금 소프트 삭제를 쓰고 있다면, `@SoftDelete`(Hibernate 6.4+)로 옮길 만한 자리인가.** 코드베이스에서 `@SQLDelete`와 `@Where`를 한 번 grep해보자.

```bash
grep -r "@SQLDelete\|@Where" src/main/java/
```

리스트가 나오면 한 번 살펴보자. Hibernate 6.4+를 쓰고 있고, 컬럼 이름이 표준에 가깝다면 *마이그레이션을 한 PR로 정리*할 만하다. 코드도 줄고 미묘한 결합 동작에 대한 불안도 줄어든다. 다만 컬럼 이름이 `is_deleted`, `del_yn`, `deleted_at` 등으로 다르다면 *columnName 옵션을 정확히 매핑*해두자. 깜빡 잊고 디폴트로 두면 새 컬럼이 추가되는 끔찍한 상황이 벌어진다.

**둘, 우리 시스템의 read 쿼리 중 *가장 무거운 한 자리*에 jOOQ를 *부분 도입*할 만한 자리가 있는가.** 일주일 동안 가장 느렸던 read API를 한 번 꼽아보자. 분석 대시보드의 *통계 쿼리*, 백오피스의 *복잡한 필터 검색*, 외부 리포트의 *집계 쿼리* 같은 자리가 후보다. 거기에 *복잡한 window function이나 CTE가 끼어 있다*면, JPQL로 풀어내는 게 코드를 무겁게 만들고 있을 가능성이 높다. *그 한 자리만* jOOQ로 옮기는 PR을 한 번 검토해보자. 전체를 옮기지 않아도 좋다. *경쟁이 아니라 분업*이라는 시각을 한 자리에서 손에 잡아보는 것이 목표다.

**셋, 다음 분기 학습 계획에 *Hibernate 6.6 / Jakarta Data 한 줄*이 포함돼 있는가.** 자기 학습 노트나 팀의 *기술 부채 백로그*를 한 번 펼쳐보자. *Hibernate의 release note*가 한 번도 검토된 적이 없는가? 그렇다면 한 줄을 비워두자. *분기에 한 번 release note 훑기*, *반기에 한 번 핵심 신기능 한 가지 시도해보기* 같은 가벼운 항목이면 충분하다. 도구의 흐름을 따라가는 *습관*이 결국 자기 시스템을 천천히 가볍게 만든다.

### 마지막 한 문장

긴 길이었다. 1장의 회의실에서 12장의 마지막까지, *라운드트립과 트랜잭션*이라는 두 단어로 모든 비용을 한 줄로 환원하는 시각을 함께 자라보자고 약속했다. 그 약속이 어디까지 닿았는지는 *이 책을 덮은 뒤 자기 코드 앞에 앉을 때* 비로소 드러난다.

마지막으로 한 가지를 짚어두자. *완벽한 JPA 시스템은 없다*. 어느 시스템에도 *의심스러운 자리*는 있고, *바꾸지 못한 자리*는 있다. *이 책에서 다루지 못한 자리*도 있고, *책이 권하지 않은 자리에 정당한 예외*도 있다. 그 모든 자리를 *한 번에 다 풀려고 하지 말자*. 책 한 권이 약속할 수 있는 건 *한 가지 시각*이다. 그 시각으로 *오늘 한 자리, 이번 주 다섯 자리, 이번 분기 한 바퀴*를 도는 습관이 결국 시스템을 자라게 한다.

그리고 그 시각의 한 줄은 책의 처음부터 끝까지 동일했다.

> **느린 JPA에는 이유가 있다. 그리고 그 이유는 거의 항상 들여다보면 보인다.**

이 한 문장을 손에 쥐고, 자기 코드 앞에 앉아보자. 거기서부터 시작이다.

긴 길을 함께 걸어와주어서 고맙다.
