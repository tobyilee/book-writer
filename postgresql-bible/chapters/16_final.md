# 16장. API 백엔드 — DB가 백엔드다

새 서비스를 하나 만든다고 해보자. 화면을 그리고, 테이블을 설계하고, 그 사이를 잇는 API 서버를 또 하나 짓는다. `GET /users`, `POST /users`, `GET /users/:id`, `PATCH /users/:id`, `DELETE /users/:id`. 그리고 같은 일을 `orders`에 대해 반복한다. `products`에 대해서도 반복한다. 컨트롤러, 서비스, 리포지토리. 세 겹의 클래스가 테이블 수만큼 늘어난다. 일이 끝나갈 무렵 뒤를 돌아보면, 자기가 쓴 코드의 절반이 "테이블의 열을 JSON으로 옮기고, JSON의 키를 다시 테이블의 열로 옮기는" 단순 매핑이라는 사실을 발견한다. 그러면 자연스레 한 가지 질문이 든다.

"이거, DB가 직접 해주면 안 되나?"

물론 안 될 이유는 많다. 비즈니스 로직이 있어야 하고, 권한 분기가 있어야 하고, 트랜잭션 경계가 있어야 한다. 그런데 그 "안 될 이유"들을 하나하나 꺼내놓고 보면, 의외로 PostgreSQL이 이미 가진 기능들로 상당 부분 풀린다. 권한은 role과 GRANT가 있고, 정책은 RLS가 있고, 트랜잭션은 어차피 DB의 것이다. 그렇다면 그 위에 얇은 변환 레이어 하나만 얹으면, "DB가 백엔드"라는 말이 농담이 아니라 실제 아키텍처가 된다.

PostgREST, pg_graphql, Hasura, Supabase가 그 농담을 진지하게 만든 도구들이다. 이번 장에서 같이 따라가 볼 것은 두 가지다. 하나는 "이게 어디서 빛나는가" — 빠른 출시, 작은 팀, BaaS형 SaaS, 내부 도구. 다른 하나는 "어디서 위험한가" — 복잡한 도메인 로직, 통합 테스트의 깊이, lock-in의 비용. 두 가지를 같이 보지 않으면 결국 한쪽으로 휘청거리게 된다.

## 16.1 PostgREST — 스키마가 곧 REST API다

PostgREST는 한 줄로 설명할 수 있다. "PostgreSQL 스키마를 읽어서, 그대로 REST API로 노출한다." 그게 전부다. 테이블이 `users`라면 `GET /users`가 생기고, 컬럼이 `email`이라면 `?email=eq.foo@bar.com`이 필터가 된다. 뷰가 `vw_active_users`라면 `GET /vw_active_users`가 생기고, 함수가 `fn_search_orders(p_query text)`라면 `POST /rpc/fn_search_orders`로 호출된다. 별도의 코드 없이.

처음 들으면 두 가지 반응이 갈린다. 한쪽은 "그게 진짜 쓸 만한가?"이고, 다른 한쪽은 "그러면 백엔드 개발자가 필요 없는 거 아닌가?"이다. 둘 다 절반만 맞다. 진짜 쓸 만한 영역은 분명히 있고, 그 영역 밖에서는 여전히 백엔드 코드가 필요하다. 어디까지 쓸 만한지 먼저 살펴보자.

### 가장 단순한 시나리오

테이블 하나로 시작해보자.

```sql
CREATE TABLE posts (
  id BIGSERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  author_id UUID NOT NULL,
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

PostgREST를 띄우고 이 DB를 가리키면, 다음과 같은 요청들이 즉시 동작한다.

```http
GET /posts                              # 전체 목록
GET /posts?id=eq.42                     # id가 42인 row
GET /posts?published_at=not.is.null     # 발행된 글만
GET /posts?title=ilike.*postgres*       # 제목에 'postgres' 포함 (대소문자 무시)
GET /posts?select=id,title&order=created_at.desc&limit=10
POST /posts                             # 새 글 등록
PATCH /posts?id=eq.42                   # 부분 수정
DELETE /posts?id=eq.42                  # 삭제
```

코드는 한 줄도 쓰지 않았다. 마이그레이션으로 `CREATE TABLE` 한 번 한 게 전부다. 새 컬럼을 추가하면? 다음 요청부터 그 컬럼이 자동으로 응답에 포함된다. 외래키를 걸면? `GET /posts?select=*,authors(*)`로 조인 결과를 한 번에 받을 수 있다. 마치 GraphQL의 nested query를 REST 문법으로 흉내 낸 듯한 표현력이다.

여기까지 보면 한 가지 의문이 든다. "이렇게 다 열어두면 보안은 어떻게 하지?" 좋은 질문이다. PostgREST의 진짜 정체성은 여기서 드러난다.

### 핵심 메커니즘 — JWT와 role switch

PostgREST는 자기가 권한을 갖지 않는다. 권한은 전부 PostgreSQL의 role에 위임한다. 정확히 말하면, 요청이 들어올 때마다 PostgREST가 `SET LOCAL ROLE <누구>`로 PG role을 바꾸고, 그 role의 권한으로 쿼리를 실행한다. 익명 사용자는 `anon` role, 로그인한 사용자는 JWT에 담긴 role(예: `authenticated`)로 들어간다.

```sql
-- 익명 role: 발행된 글만 SELECT 가능
GRANT USAGE ON SCHEMA api TO anon;
GRANT SELECT ON api.posts TO anon;

CREATE POLICY posts_anon_select ON api.posts
  FOR SELECT TO anon
  USING (published_at IS NOT NULL);

-- 인증된 사용자: 자기 글에 한해 모든 권한
GRANT ALL ON api.posts TO authenticated;

CREATE POLICY posts_owner_all ON api.posts
  FOR ALL TO authenticated
  USING (author_id = auth.uid())
  WITH CHECK (author_id = auth.uid());
```

여기서 `auth.uid()`는 JWT의 `sub` claim을 꺼내주는 함수다(보통 `current_setting('request.jwt.claims', true)::json->>'sub'`을 감싼 헬퍼). 흐름은 단순하다.

1. 사용자가 어딘가에서 로그인하고, JWT를 받는다(Supabase Auth든, 자체 인증 서버든).
2. 사용자가 `Authorization: Bearer <JWT>`로 PostgREST에 요청한다.
3. PostgREST가 JWT의 `role` claim을 보고 `SET LOCAL ROLE authenticated` 실행, `sub` claim을 `request.jwt.claims`에 박는다.
4. 쿼리가 RLS를 거치면서 `auth.uid()`가 작동, 자기 row만 보인다.

코드 없이 권한 분기가 끝난다. 그것도 DB 안에서. 애플리케이션 레이어에서 `if user.id != post.author_id throw new ForbiddenException()`을 천 번 쓰던 시절을 생각하면, 묘하게 후련하다.

### 함수로 비즈니스 로직을 노출한다

"권한은 알겠는데, 비즈니스 로직은 어떻게 하지?"라는 다음 의문이 자연스럽다. PostgREST는 함수도 노출한다. `POST /rpc/{함수명}`이 그 입구다.

```sql
CREATE OR REPLACE FUNCTION api.publish_post(p_post_id BIGINT)
RETURNS api.posts
LANGUAGE plpgsql
SECURITY INVOKER
AS $$
DECLARE
  v_post api.posts;
BEGIN
  -- 자기 글인지 확인은 RLS가 알아서 한다 (UPDATE의 USING 정책)
  UPDATE api.posts
     SET published_at = now()
   WHERE id = p_post_id
   RETURNING * INTO v_post;

  IF v_post.id IS NULL THEN
    RAISE EXCEPTION 'post not found or not yours'
      USING ERRCODE = '42501';
  END IF;

  -- 발행 이벤트를 outbox에 적재 (13장 패턴)
  INSERT INTO api.outbox (event_type, payload)
       VALUES ('post.published', row_to_json(v_post));

  RETURN v_post;
END;
$$;
```

호출은 이렇게 된다.

```http
POST /rpc/publish_post
Content-Type: application/json
Authorization: Bearer eyJ...

{ "p_post_id": 42 }
```

PL/pgSQL이 못마땅하면 SQL 함수, 더 무거우면 PL/Python, PL/V8까지 갈 수 있다. 어떤 언어를 택하든, 그 로직은 DB 안에서 트랜잭션의 일부로 실행된다. 애플리케이션 레이어가 트랜잭션 경계를 잘못 잡아서 "1만큼 빠진 상태가 잠깐 보이는" 버그를 만들 일이 없다. 그 자체는 마음 편한 일이다.

물론 모든 로직을 PL/pgSQL로 쓰는 일이 즐겁지는 않다. 디버깅 도구도 부족하고, 테스트 프레임워크의 두께도 백엔드 언어에 비할 바 못 된다. 그래서 PostgREST를 진지하게 쓰는 팀의 공식은 대체로 이렇다 — **데이터 조작과 권한은 DB 안, 외부 통신·복잡한 도메인 로직은 별도의 작은 서비스**. 둘을 합쳐 "lean한 backend-for-frontend" 같은 구조를 만든다. PostgREST가 100%의 백엔드를 대체한다는 환상은 빨리 버리는 편이 낫다.

### 빛나는 곳, 위험한 곳

PostgREST가 어디서 빛나는지 정리해보자.

- **내부 도구·관리자 화면.** CRUD가 거의 전부이고 사용자는 직원 50명. 백엔드 한 사람이 두 달 걸리던 일이, 마이그레이션과 RLS 정책 며칠로 끝난다.
- **MVP·프로토타입.** "이 도메인이 진짜로 먹히는지" 검증해야 하는 단계. 도메인이 굳어진 뒤에 백엔드를 따로 떼어내도 늦지 않다. 그동안 손이 가는 곳이 너무 많지 않다는 것 자체가 자산이다.
- **얇은 SaaS의 데이터 API.** 모바일 앱이나 SPA가 직접 PostgREST를 두드린다. 인증과 RLS만 잘 짜두면, 백엔드를 따로 운영할 이유가 점점 옅어진다.
- **사이드 프로젝트.** 혼자 만드는 도구에 풀스택 보일러플레이트를 또 까는 일은 솔직히 번거롭다. PostgREST 하나 띄워두면 끝이다.

반대로 어디서 위험한가.

- **복잡한 도메인 로직이 많은 곳.** 결제, 회계, 보험 같이 비즈니스 규칙이 수백 개 얽힌 도메인을 PL/pgSQL로 옮기는 일은 끔찍한 일이다. 코드 베이스의 가독성, 테스트 가능성, 디버깅 도구 어느 면에서도 일반 백엔드 언어에 미치지 못한다.
- **여러 외부 서비스를 호출해야 하는 곳.** 결제 PG, 이메일, 푸시, 외부 API를 동기 호출하는 로직이 흔하다면, 그건 백엔드가 할 일이지 DB가 할 일이 아니다. DB 안에서 HTTP 호출을 하는 익스텐션이 없는 건 아니지만, 그쪽으로 깊이 들어갈수록 운영의 무게가 빠르게 커진다.
- **응답 모양을 자유자재로 빚어야 하는 곳.** 화면 한 곳마다 응답 구조가 달라야 한다면, REST의 자원 중심 모델로 대응하기 답답하다. 그럴 땐 GraphQL이 자연스러운데, 그 얘기는 다음 절에서 하자.
- **레거시 백엔드와 공존해야 하는 곳.** 이미 인증·인가·도메인 서비스가 잘 갖춰진 백엔드가 있고, 데이터 일부만 PostgREST로 노출하고 싶다면 가능은 하다. 그런데 권한 모델이 둘로 갈리는 순간(애플리케이션 권한 + DB 권한), 누가 진실의 원천인지 헷갈리기 시작한다. 조심해서 다뤄야 한다.

여기까지가 REST의 세계다. 그러면 GraphQL은 어떨까.

## 16.2 pg_graphql — 스키마에서 GraphQL이 자란다

PostgREST를 따라가다 보면 한 가지 답답함을 만난다. "한 화면을 그리려고 다섯 번의 GET을 날린다." `GET /posts`로 글 목록을 받고, 각 글의 작성자를 보려고 `GET /authors?id=in.(1,2,3,...)`을 하고, 댓글 수를 세려고 또 한 번, 좋아요 수를 세려고 또 한 번. REST의 자원 중심 모델이 그렇다. PostgREST의 `select=*,authors(*)` 같은 임베딩이 이걸 어느 정도 해결해주지만, 화면이 복잡해질수록 클라이언트가 원하는 모양과 자원의 경계가 어긋난다.

이럴 때 GraphQL이 자연스럽다. 클라이언트가 "이 글의 제목, 작성자의 이름, 댓글 3개의 작성자 아바타"를 한 쿼리로 묻고, 서버는 그 모양 그대로 응답한다. 그런데 GraphQL을 직접 짜는 일도 만만치 않다. 스키마 정의, resolver 작성, N+1 문제, DataLoader 배치, 권한 분기 — 한쪽 짐을 덜었더니 다른 쪽 짐이 늘어난 느낌이다.

pg_graphql은 그 짐을 다시 DB로 옮긴다. PostgreSQL 익스텐션 하나로, 스키마를 reflect해서 GraphQL endpoint를 자동으로 만들어준다. Supabase가 작성하고 자기 BaaS에 기본 탑재한 익스텐션이다.

### 작동 방식 — 스키마 reflection

```sql
CREATE EXTENSION pg_graphql;

-- 권한을 주면 GraphQL이 그 자원을 본다
GRANT USAGE ON SCHEMA api TO anon, authenticated;
GRANT SELECT ON api.posts TO anon;
GRANT ALL ON api.posts TO authenticated;
```

이렇게 하면 `posts` 테이블이 GraphQL 타입으로 노출된다. 외래키가 있으면 관계 필드가 자동으로 생긴다. PostgREST의 sibling이라는 말이 적절하다 — 같은 DB 스키마를 다른 입구(REST vs GraphQL)로 비춘다.

쿼리는 보통의 GraphQL과 같은 모양이다.

```graphql
{
  postsCollection(
    filter: { publishedAt: { is: NOT_NULL } }
    orderBy: [{ createdAt: DescNullsLast }]
    first: 10
  ) {
    edges {
      node {
        id
        title
        author { id displayName avatarUrl }
        commentsCollection(first: 3) {
          edges { node { id body createdAt } }
        }
      }
    }
  }
}
```

응답은 정확히 이 모양 그대로 돌아온다. 내부적으로 pg_graphql은 이 GraphQL 쿼리 하나를 단일 SQL 쿼리로 컴파일한다. N+1이 발생할 여지가 거의 없다. resolver마다 따로 쿼리가 나가는 일반 GraphQL 서버와 가장 큰 차이가 여기서 난다.

권한 분기는 PostgREST와 같다. JWT에서 role과 claims를 꺼내 PG role로 switch하고, RLS가 행을 거른다. GraphQL의 권한 처리는 보통 resolver마다 if문을 박아야 하는 번거로움이 있는데, RLS로 처리하면 한 번 쓴 정책이 모든 쿼리에 자동 적용된다.

### Mutation도 같은 구조다

```graphql
mutation {
  insertIntoPostsCollection(
    objects: [{ title: "Hello PG", body: "..." }]
  ) {
    records { id title createdAt }
  }
}
```

`INSERT`, `UPDATE`, `DELETE`가 mutation으로 노출된다. RLS의 `WITH CHECK`가 그대로 작동하므로, "남의 글을 자기 글로 둔갑시키는" 시도는 DB가 차단한다.

복잡한 로직은? PostgREST와 마찬가지로 함수를 노출한다. pg_graphql은 SECURITY DEFINER가 아닌 일반 함수를 GraphQL의 mutation으로 보여준다(설정에 따라 다르다).

### 어디서 빛나고 어디서 답답한가

pg_graphql의 강점은 분명하다.

- **클라이언트가 응답 모양을 결정한다.** 모바일과 웹이 같은 endpoint를 다른 모양으로 소비할 수 있다. 백엔드가 화면 변화마다 새 endpoint를 추가하지 않아도 된다.
- **N+1이 사라진다.** 일반 GraphQL 서버에서 가장 자주 겪는 두통이 한 번에 사라진다. 쿼리 하나로 컴파일된다는 성질의 자연스러운 귀결이다.
- **권한이 RLS로 일원화된다.** REST에서 본 그 모델이 GraphQL에서도 그대로 작동한다. 두 입구를 동시에 운영해도 정책을 한 번만 쓰면 된다.

답답한 지점도 있다.

- **표현력에 한계가 있다.** Federation, custom scalar, directives 같이 복잡한 GraphQL 기능은 pg_graphql의 자동 노출과 결이 맞지 않는다. 깊이 들어갈수록 직접 짠 GraphQL 서버의 유연성이 그리워질 수 있다.
- **스키마가 그대로 노출된다는 부담.** GraphQL 타입 이름이 곧 테이블 이름이다. 컬럼 이름을 함부로 바꾸면 클라이언트가 깨진다. 스키마 진화 정책을 처음부터 잘 세워둬야 한다. snake_case와 camelCase의 자동 변환 같은 사소한 결정도 한번 정한 뒤에 바꾸기 어렵다.
- **subscriptions가 약하다.** 실시간이 필요하면 Supabase Realtime이나 pg_notify 기반 별도 채널을 붙여야 한다. 한 입구에서 모든 게 해결되는 그림은 아니다.

PostgREST와 pg_graphql 둘 중 무엇을 고를지 묻는다면, 답은 "클라이언트의 모양이 얼마나 다양한가"에 달려 있다. 자원 단위 CRUD가 거의 전부면 PostgREST가 가볍다. 화면마다 응답 구조가 천차만별이면 pg_graphql이 편하다. 두 입구를 동시에 운영해도 부담은 거의 없다 — DB 한 벌에 RLS 한 벌이면 끝이다.

그렇다면 Hasura는 어디 있는가.

## 16.3 Hasura — 한 GraphQL 입구가 여러 DB를 묶는다

PostgREST와 pg_graphql이 "PostgreSQL 한 벌"에 묶인 도구라면, Hasura는 그 경계를 벗어난다. PostgreSQL, MySQL, BigQuery, Snowflake, MS SQL, REST endpoint, 다른 GraphQL endpoint까지 하나의 GraphQL 입구 아래에 묶는다. 그래서 Hasura의 정체성은 "DB 위에 얹는 자동 API"라기보다 "여러 데이터 소스 위에 얹는 통합 게이트웨이"에 가깝다.

이게 왜 중요한가? 회사가 자라면 데이터가 한 DB에 모이지 않는다. 사용자 데이터는 PostgreSQL에, 이벤트는 Kafka에, 분석은 BigQuery에, 결제 이력은 외부 SaaS의 REST API에 있다. 화면 하나를 그리려고 각 소스를 따로 호출하는 백엔드 코드를 짜는 일은 번거롭다. Hasura는 이런 환경에서 한 결로 입구를 잡아준다.

### Hasura의 모델

Hasura는 메타데이터에 "어떤 테이블을 어떤 GraphQL 타입으로 노출할지, 어떤 권한이 누구에게 있는지, 어떤 관계가 있는지"를 선언한다. 메타데이터는 JSON 또는 YAML로 git에 커밋된다. 마이그레이션과 함께 버전 관리된다.

권한 모델이 pg_graphql과 다르다. Hasura는 자기 안에 RBAC을 갖는다. role별로 어떤 컬럼을 볼 수 있고, 어떤 필터를 강제할지를 메타데이터에 적는다.

```yaml
- role: authenticated
  permission:
    columns: [id, title, body, author_id, published_at]
    filter:
      _or:
        - { published_at: { _is_null: false } }
        - { author_id: { _eq: X-Hasura-User-Id } }
```

JWT의 claim을 `X-Hasura-User-Id` 같은 세션 변수로 매핑해서 필터에 쓴다. RLS와 비슷한 결과를 만들지만, 정책이 DB 안이 아니라 Hasura 안에 있다는 차이가 있다. 이 차이는 작아 보이지만 결정적이다. 다음과 같은 트레이드오프가 따른다.

- **장점:** PG 외 DB(MySQL, BigQuery 등)에서도 같은 권한 모델이 작동한다. 한 GraphQL 입구에 권한 모델을 일원화한다.
- **단점:** DB에 직접 붙는 다른 도구(BI, 분석 쿼리, 운영 콘솔)는 Hasura의 권한을 모른다. RLS처럼 DB 자체의 정책이 아니므로, 입구가 둘이 되는 순간 누수가 생긴다.

이 트레이드오프를 어떻게 다룰지가 Hasura 도입의 가장 큰 결정이다. "Hasura를 통하지 않고는 데이터에 접근하지 않는다"는 약속을 조직 차원에서 받쳐줄 수 있는가? 그렇다면 Hasura의 RBAC이 편하다. 그렇지 않다면, 권한은 DB(RLS)에 두고 Hasura는 얇은 게이트웨이로만 쓰는 구조를 고민하는 편이 낫다.

### Actions, Events, Remote Schemas

Hasura가 단순한 자동 GraphQL 도구를 넘는 지점이 있다. Action, Event, Remote Schema라는 세 개념이다.

- **Action:** GraphQL mutation을 HTTP webhook으로 라우팅한다. "복잡한 도메인 로직은 별도 서비스로 빼고, GraphQL 입구만 통일하고 싶다"는 요구에 답한다. Hasura가 라우터 역할, 실제 로직은 Node/Go/Python 서비스가 처리.
- **Event:** DB 이벤트(INSERT/UPDATE/DELETE)를 webhook으로 발사한다. logical replication의 단순한 사촌이다. 14장의 Debezium보다 가볍지만 정밀도가 낮다.
- **Remote Schema:** 다른 GraphQL endpoint를 자기 스키마에 합친다. 외부 SaaS의 GraphQL을 자기 도메인의 일부처럼 노출한다.

이 셋을 잘 쓰면 Hasura가 진짜로 "데이터 게이트웨이"가 된다. CRUD는 자동, 도메인 로직은 Action, 비동기 처리는 Event, 외부 시스템은 Remote Schema — 그림이 깔끔하다.

### 빛나는 곳, 위험한 곳

빛나는 곳은 명확하다.

- **여러 데이터 소스가 섞인 환경.** 한 GraphQL 입구로 묶어야 화면이 깔끔해지는 회사.
- **GraphQL을 진지하게 쓰는 팀.** Federation까지 가지 않아도 되는 규모이고, 자동 스키마 + Action 조합으로 충분하다고 판단되는 곳.
- **권한 모델을 한 곳에 모으고 싶은 팀.** DB가 여러 개라 RLS가 일관성을 못 주는 상황에서, Hasura 메타데이터를 진실의 원천으로 삼는 선택.

위험한 곳도 있다.

- **DB가 PostgreSQL 하나뿐인 곳.** 그러면 pg_graphql + RLS가 더 가볍고, lock-in도 덜하다. Hasura의 추가 운영 비용이 정당화되기 어렵다.
- **모든 데이터 접근을 Hasura로 강제할 수 없는 곳.** RBAC이 Hasura 안에만 있으면 누수가 생긴다. BI 도구, 직접 SQL 콘솔, 다른 마이크로서비스가 DB에 붙는 한 권한 일관성은 무너진다.
- **라이선스에 민감한 곳.** Hasura는 오픈 소스 버전과 Enterprise/Cloud 버전이 갈린다. 진지한 운영 기능(쿼리 캐시 일부, 모니터링 일부)이 유료 라인에 묶인다. 도입 전에 가격표를 한 번 살피는 편이 낫다.

PostgREST가 "가벼움", pg_graphql이 "PG 내장 GraphQL", Hasura가 "여러 DB 위 통합 게이트웨이" — 이렇게 세 점을 머릿속에 박아두면 도구 선택이 헷갈리지 않는다. 그러면 이 셋을 다 모아놓은 풀스택 패키지는 무엇인가? Supabase로 가보자.

## 16.4 Supabase — 풀스택을 한 묶음으로

Supabase의 자기 소개는 "Firebase의 오픈 소스 대안"이다. Firebase가 Realtime DB·Firestore·Auth·Storage·Functions를 한 묶음으로 제공하는 BaaS인 것처럼, Supabase는 그 자리에 PostgreSQL을 앉히고, 그 위에 PostgREST(데이터 API), pg_graphql(GraphQL API), GoTrue(Auth), Realtime, Storage, Edge Functions를 얹는다. 한 줄 요약은 "PostgreSQL 풀스택 BaaS"다.

처음 보면 묘하다. 우리가 앞 절들에서 본 도구들이 이미 다 들어 있다. 거기에 인증, 파일 저장, 실시간 구독, 서버리스 함수가 따라온다. 무료 티어가 500MB DB + 50K MAU. 사이드 프로젝트와 MVP에는 거의 무료처럼 느껴지는 한도다.

### Supabase의 풀스택 구성

각 컴포넌트가 PostgreSQL에 어떻게 얹히는지 살펴보자.

- **Auth (GoTrue):** 사용자를 `auth.users` 테이블에 저장하고, JWT를 발급한다. JWT의 `sub` claim이 `auth.uid()`로 RLS에서 그대로 쓰인다. 이메일·OAuth·매직 링크·SAML까지 다 지원한다. 비밀번호 해싱과 토큰 회전은 직접 짜지 않아도 된다.
- **Data API (PostgREST + pg_graphql):** 16.1과 16.2에서 본 그대로. 스키마와 RLS만 잘 짜두면 REST와 GraphQL이 동시에 나온다.
- **Realtime:** logical replication을 구독해서 WebSocket으로 클라이언트에 흘려준다. `posts` 테이블에 INSERT가 일어나면, 그걸 구독 중인 클라이언트가 즉시 받는다. 채팅, 협업 도구, 실시간 대시보드에 잘 맞는다.
- **Storage:** 객체 저장소. 권한은 RLS와 같은 방식으로 정책을 쓴다. 파일 메타데이터가 DB의 테이블이라, "내 파일만 보기"가 한 줄 정책으로 끝난다.
- **Edge Functions:** Deno 기반 서버리스 함수. 외부 API 호출, 결제 webhook 처리, 무거운 로직을 여기에 둔다.

이 다섯이 PostgreSQL 한 벌을 진실의 원천으로 공유한다. 사용자도 DB의 row, 파일 메타데이터도 DB의 row, 실시간 이벤트도 DB의 WAL에서 나온다. 그래서 권한을 한 곳(RLS)에만 잘 짜두면, 다섯 입구 전부에서 같은 정책이 작동한다. 이 일관성이 Supabase의 진짜 매력이다.

### 작은 예제 — 채팅 한 채널

```sql
-- 1. 메시지 테이블
CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  channel_id UUID NOT NULL,
  sender_id UUID NOT NULL REFERENCES auth.users(id),
  body TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- 2. 채널 멤버 테이블
CREATE TABLE channel_members (
  channel_id UUID NOT NULL,
  user_id UUID NOT NULL REFERENCES auth.users(id),
  PRIMARY KEY (channel_id, user_id)
);

ALTER TABLE channel_members ENABLE ROW LEVEL SECURITY;

-- 3. 정책: 채널 멤버만 메시지를 본다
CREATE POLICY messages_select_member ON messages
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM channel_members
       WHERE channel_id = messages.channel_id
         AND user_id    = auth.uid()
    )
  );

-- 4. 정책: 자기 이름으로만 메시지를 쓴다
CREATE POLICY messages_insert_self ON messages
  FOR INSERT TO authenticated
  WITH CHECK (
    sender_id = auth.uid()
    AND EXISTS (
      SELECT 1 FROM channel_members
       WHERE channel_id = messages.channel_id
         AND user_id    = auth.uid()
    )
  );

-- 5. Realtime publication에 추가
ALTER PUBLICATION supabase_realtime ADD TABLE messages;
```

클라이언트는 이제 SDK 한 줄로 끝낸다.

```ts
// 메시지 보내기
await supabase.from('messages').insert({
  channel_id: 'abc-...',
  sender_id: user.id,
  body: 'Hello'
});

// 실시간 구독
supabase
  .channel('messages-room-abc')
  .on('postgres_changes',
      { event: 'INSERT', schema: 'public', table: 'messages',
        filter: `channel_id=eq.abc-...` },
      (payload) => render(payload.new))
  .subscribe();
```

채팅 한 채널이 끝났다. 백엔드 코드는 한 줄도 없다. 권한도 인증도 실시간도 다 DB의 한 정의에서 나온다. 처음 이 그림을 그려보면 묘한 기분이 든다. "내가 지난 1년간 짜온 코드의 절반이 뭐였지?" 하는.

### 여기서 멈추는 자리

물론 모든 게 이렇게 깔끔하지는 않다. Supabase로 풀스택을 짜다 보면 어느 순간 "여기서부터는 백엔드가 있어야겠다" 싶은 경계를 만난다.

- **외부 API와의 무거운 통합.** 결제 PG 호출, 외부 SaaS 연동, 복잡한 webhook 처리. Edge Function으로 어느 정도 풀리지만, 로직이 무거워지면 별도 서비스가 더 편하다.
- **비동기 잡 처리.** 큰 이메일 발송, 배치 작업, 외부 데이터 동기화. Edge Function의 타임아웃과 메모리 한계에 부딪힌다.
- **이벤트 소싱·CQRS 같은 깊은 패턴.** PG의 기본 RLS·trigger·function으로는 표현이 답답해진다.
- **사용자 인터페이스가 아닌 비즈니스 도메인이 두꺼운 시스템.** 보험 청구, 회계 마감, 공급망 같은 도메인은 코드의 두께가 데이터의 두께보다 큰 시스템이다. 그쪽은 BaaS의 결과 맞지 않는다.

그래서 Supabase의 진짜 자리는 "사용자가 데이터를 만들고 보는 시스템"이다. 채팅, 문서 협업, 노트, 작은 SaaS, 대시보드, 콘텐츠 플랫폼 — 데이터 모델이 곧 도메인의 80%인 시스템에서 빛난다. 그 밖에서는 일부 컴포넌트(Auth만, Storage만)를 골라 쓰는 방식으로 절충하는 편이 낫다.

## 16.5 RLS 멀티테넌트 패턴 — tenant_id, current_setting, USING 정책

이쯤에서 RLS 이야기를 좀 더 깊이 해보자. 위에서 본 도구들이 다 RLS를 권한 모델의 토대로 삼는다. 그런데 SaaS를 만든다면, 인증된 사용자별 권한보다 한 층 더 큰 경계가 있다 — **테넌트(고객사) 경계**다.

상상해보자. 같은 데이터베이스 한 벌에 100개 회사의 데이터가 들어 있다. A 회사의 사용자가 B 회사의 데이터를 한 row라도 보면, 그건 단순한 버그가 아니라 신뢰의 끝이다. 회사가 무너지는 종류의 사고다. 이런 격리를 어떻게 보장할 것인가? 세 가지 큰 갈래가 있다.

1. **DB 분리.** 회사마다 DB 한 벌. 가장 강한 격리이지만, 운영 비용이 회사 수에 비례해 폭발한다.
2. **스키마 분리.** 한 DB에 회사별 스키마. 중간 정도의 격리. PG에서는 search_path와 권한으로 다룬다.
3. **공유 테이블 + tenant_id.** 한 테이블에 모든 회사 데이터, `tenant_id` 컬럼으로 구분. 운영은 가장 가볍지만, 격리는 가장 약하다. 애플리케이션의 한 줄 실수로도 누수가 일어날 수 있다.

세 번째가 가장 위험해 보이지만, 동시에 가장 흔하다. 운영 단순성이 압도적이기 때문이다. 그렇다면 그 위험을 어떻게 막을 것인가? RLS가 그 답이다.

### 표준 패턴

AWS Database Blog가 정리한 multi-tenant SaaS 표준 패턴이 있다. 대략 이렇다.

```sql
-- 1. 모든 도메인 테이블에 tenant_id 1급 컬럼
CREATE TABLE orders (
  id        BIGSERIAL PRIMARY KEY,
  tenant_id UUID NOT NULL,
  customer  TEXT NOT NULL,
  amount    NUMERIC(12,2) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX orders_tenant_id_idx ON orders (tenant_id);

ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- 2. 정책: 세션의 현재 tenant만 보인다
CREATE POLICY orders_tenant_isolation ON orders
  FOR ALL TO app_user
  USING      (tenant_id = current_setting('app.current_tenant')::UUID)
  WITH CHECK (tenant_id = current_setting('app.current_tenant')::UUID);
```

이게 핵심 골격이다. 풀어보자.

- 모든 도메인 테이블에 `tenant_id`를 1급 컬럼으로 둔다. 외래키처럼 부수적인 게 아니라, 1순위 의미를 갖는 컬럼이다.
- 세션 변수 `app.current_tenant`에 "지금 이 세션이 누구의 데이터에 접근하는지"를 박는다. PG는 `SET LOCAL` 또는 `SET`으로 세션 변수를 쓸 수 있고, `current_setting()`으로 읽는다.
- RLS의 USING은 SELECT/UPDATE/DELETE에서 어떤 행이 보일지, WITH CHECK은 INSERT/UPDATE 후에 어떤 행이 허용될지를 결정한다. 둘을 같이 둔다.

이렇게 짜두면, 애플리케이션이 어떤 쿼리를 던지든 — `SELECT * FROM orders`처럼 WHERE 절을 깜빡한 코드라도 — 다른 테넌트의 데이터가 절대로 나가지 않는다. DB가 강제로 거른다. 애플리케이션 코드의 실수가 데이터 누수로 이어지지 않는다.

### 세션 변수를 어디서 박는가

핵심은 "`app.current_tenant`를 누가 언제 박는가"이다. 잘못 박으면 정책이 무력화된다. 대표적인 패턴 두 가지를 보자.

**패턴 1: 풀러 후 첫 쿼리에서 박는다.**

```sql
-- 트랜잭션 시작 직후
SET LOCAL app.current_tenant = '11111111-1111-1111-1111-111111111111';

-- 이후 모든 쿼리는 이 테넌트에 한정
SELECT * FROM orders;
UPDATE orders SET amount = 100 WHERE id = 42;
```

`SET LOCAL`을 쓰는 게 중요하다. `SET`은 세션 끝까지 유지되는데, PgBouncer transaction pooling을 쓰면 그 세션이 다른 사용자에게 재사용된다(21장 참고). 재사용된 세션에 이전 사용자의 tenant 값이 남아 있으면? 끔찍한 일이다. `SET LOCAL`은 트랜잭션 끝나면 자동으로 사라진다. 풀러 호환성을 위한 사실상 필수 선택이다.

**패턴 2: 함수 안에서 박는다.**

```sql
CREATE OR REPLACE FUNCTION api.with_tenant(p_tenant UUID, p_sql TEXT)
RETURNS SETOF JSON
LANGUAGE plpgsql
AS $$
BEGIN
  PERFORM set_config('app.current_tenant', p_tenant::TEXT, true);
  RETURN QUERY EXECUTE p_sql;
END;
$$;
```

이 방식은 PostgREST/Hasura/Supabase에서는 보통 쓰지 않는다. 그쪽은 JWT의 claim을 자동으로 PG 세션에 박는 메커니즘이 따로 있기 때문이다.

**패턴 3 (Supabase식): JWT claim에서 직접 꺼낸다.**

Supabase는 JWT의 claim을 `request.jwt.claims`에 박는다. 그 안에 `tenant_id`가 있다면 정책에서 직접 꺼낼 수 있다.

```sql
CREATE POLICY orders_tenant_isolation ON orders
  FOR ALL TO authenticated
  USING (
    tenant_id = (
      current_setting('request.jwt.claims', true)::JSON
        ->>'tenant_id'
    )::UUID
  );
```

JWT가 진실의 원천이 된다. 사용자가 어떤 tenant에 속해 있는지는 인증 시점에 결정되고, JWT에 박혀서 매 요청마다 검증된다. 세션 변수를 따로 박지 않아도 된다.

### 다중 테넌트 사용자의 어려움

여기서 한 가지 까다로운 경우가 있다. **한 사용자가 여러 테넌트에 속할 수 있는 시스템.** 컨설턴트가 5개 회사를 관리하거나, 본사 직원이 여러 자회사 데이터를 본다거나. 이때 JWT에 `tenant_id` 하나를 박으면 표현이 안 된다.

해결책은 보통 둘 중 하나다.

- **요청마다 어떤 테넌트인지 명시.** HTTP 헤더(`X-Tenant-Id`) 또는 URL path로. 그걸 받아서 `SET LOCAL app.current_tenant`로 박는다. 그 사용자가 그 테넌트에 정말 속하는지는 별도 검증 함수에서 확인.
- **세션 단위 테넌트 스위치.** 사용자가 "테넌트 전환" UI에서 선택하면, 그때 토큰을 새로 발급해 그 안에 `tenant_id`를 박는다.

두 방식 다 일장일단이 있다. 첫 번째는 유연하지만 헤더 누락 시 동작이 애매하다. 두 번째는 명확하지만 UX가 무겁다. 시스템의 사용 패턴에 따라 골라야 한다.

### 한 단계 더 — role 기반 권한과 결합

테넌트 격리만 RLS로 풀면 절반이다. 같은 테넌트 안에서도 "관리자만 보는 데이터", "본인만 보는 데이터", "팀 단위로 공유하는 데이터"가 있다. 두 층의 정책을 같이 쓴다.

```sql
CREATE POLICY orders_tenant_and_role ON orders
  FOR SELECT TO app_user
  USING (
    tenant_id = current_setting('app.current_tenant')::UUID
    AND (
      -- 관리자는 전부 본다
      current_setting('app.current_role') = 'admin'
      -- 일반 사용자는 자기가 만든 것만
      OR created_by = current_setting('app.current_user_id')::UUID
    )
  );
```

정책은 여러 개를 동시에 둘 수 있다. PG는 같은 명령(SELECT/INSERT 등)에 대해 여러 정책이 있으면 **OR로 결합한다**(PERMISSIVE 정책일 때). 이건 직관과 어긋날 수 있는 지점이다 — "더 엄격한 정책을 추가하면 더 엄격해질 것"이라고 생각했다가, OR 결합 때문에 오히려 더 열리는 결과가 나오기도 한다.

엄격한 결합이 필요하면 `AS RESTRICTIVE` 정책을 쓴다.

```sql
CREATE POLICY orders_tenant_required ON orders
  AS RESTRICTIVE
  FOR ALL TO app_user
  USING (tenant_id = current_setting('app.current_tenant')::UUID);

CREATE POLICY orders_owner ON orders
  AS PERMISSIVE
  FOR ALL TO app_user
  USING (created_by = current_setting('app.current_user_id')::UUID);
```

RESTRICTIVE는 모든 RESTRICTIVE 정책을 AND로 묶어 통과해야 한다. PERMISSIVE는 그중 하나라도 통과하면 된다. 둘을 합치면 "테넌트는 무조건 일치 + (관리자 or 본인 작성)" 같은 표현이 가능하다.

RLS의 권한 결합 규칙은 처음 보면 헷갈리니, 정책을 도입하기 전에 작은 테스트 테이블로 한 번 직접 동작을 확인해보는 편이 낫다. "이거 막힐 줄 알았는데 안 막히네"가 운영에 들어간 뒤에 발견되면 끔찍하다.

## 16.6 RLS 운영 주의 — EXPLAIN에 보이는 술어, admin bypass

RLS가 "코드 없이 격리"라는 매력으로 다가오지만, 운영에 들어가면 두 가지 함정이 기다린다. 하나는 **성능**, 다른 하나는 **감사 가능성**이다. 이 두 함정은 본격적으로 22장(보안과 감사)에서 다루지만, 16장에서 멀티테넌트 패턴을 권한 모델로 채택한다면 최소한 알아둬야 할 결을 짚어두자.

### 정책 술어는 plan에 들어간다

RLS 정책의 USING 절은 단순한 권한 검사가 아니다. 그게 옵티마이저가 실행할 쿼리의 일부가 된다. 정책 술어가 추가 WHERE처럼 plan에 박힌다.

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer = 'foo';
```

```
Seq Scan on orders
  Filter: ((customer = 'foo'::text)
           AND (tenant_id = (current_setting('app.current_tenant'::text))::uuid))
```

세 가지를 보자.

- 정책 술어가 Filter에 보인다. 이게 안 보이면 RLS가 작동하지 않는 거다 — 켜졌는지 확인.
- `tenant_id` 인덱스가 사용되는지 확인. 인덱스가 있어야 한다. `(tenant_id)` 단독 인덱스, 또는 자주 쓰는 컬럼과의 복합 인덱스 `(tenant_id, customer)`.
- 정책 안의 함수 호출이 STABLE인지 IMMUTABLE인지 VOLATILE인지에 따라 plan 캐싱이 달라진다. `current_setting()`은 STABLE이다. 트랜잭션 내에서 같은 값을 돌려준다는 약속.

정책이 복잡해질수록 plan이 무거워진다. 서브쿼리가 들어가면(예: 위의 `EXISTS (SELECT 1 FROM channel_members ...)`), 그 서브쿼리가 매 row마다 평가될 수 있다. 자주 보는 정책 패턴은 인덱스를 받쳐줘야 한다.

흔히 빠지는 함정 하나 — **정책이 인덱스를 무력화한다.** 예를 들어 정책이 `USING (lower(email) = current_setting('app.email'))`이면, `email` 컬럼의 일반 인덱스는 작동하지 않는다. `lower(email)` 표현식 인덱스를 따로 만들어야 한다. 정책 술어에 함수가 감싸여 있으면, 그 표현식이 인덱스의 표현과 정확히 일치해야 한다. 이 디테일을 놓치면 SELECT가 수십 배 느려진다.

### admin bypass — privilege보다 policy로

운영하다 보면 "관리자 계정으로 모든 데이터를 봐야 하는" 순간이 온다. 데이터 패치, 통계 산출, 고객 문의 응대. 이때 가장 흔히 떠올리는 방법이 두 가지다.

1. **role에 BYPASSRLS 속성을 준다.** PG는 `ALTER ROLE admin_role BYPASSRLS`로 RLS를 완전히 비켜가게 만들 수 있다.
2. **superuser로 접속한다.** superuser는 RLS 정책을 무조건 무시한다.

두 방법 다 단순하지만, 감사 관점에서 위험하다. "왜 이 row를 봤는가"의 흔적이 정책에 남지 않기 때문이다. 권한 시스템이 우회되면 — 흔적 없이 우회되면 — 사후 감사가 거의 불가능해진다.

권장되는 방법은 **policy 안에서 명시적으로 허용**하는 것이다.

```sql
CREATE POLICY orders_tenant_or_admin ON orders
  FOR SELECT TO app_user
  USING (
    tenant_id = current_setting('app.current_tenant', true)::UUID
    OR current_setting('app.current_role', true) = 'platform_admin'
  );
```

이렇게 두면 "admin이 봤다"는 사실 자체가 정책의 한 가지를 작동시킨 결과로 남는다. pgaudit를 켜두면(22장), admin이 봤다는 사실이 audit log에 명시적으로 기록된다. 흔적이 살아 있다.

`FORCE ROW LEVEL SECURITY`도 알아두는 편이 낫다. 기본적으로 RLS는 테이블 소유자에게는 적용되지 않는다 — 마이그레이션과 운영의 편의를 위해서. 그런데 멀티테넌트 시스템이라면, 테이블 소유자도 정책을 따르도록 강제해야 한다.

```sql
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
```

이 한 줄을 잊으면, 마이그레이션 계정으로 접속한 누군가가 모든 테넌트의 데이터를 보게 된다. 운영의 침묵 속에서.

### 감사를 위한 한 줄 — 누가 봤는가

RLS는 "누가 무엇을 봤는가"를 자동으로 기록해주지 않는다. 정책이 통과되면 그냥 데이터가 나가는 것뿐이다. 감사 추적이 필요하면 pgaudit(또는 자체 trigger 기반 audit table)를 별도로 켜야 한다. 이 부분은 22장에서 본격적으로 다룬다. 16장에서는 단지 "RLS가 격리는 해주지만 감사는 별개"라는 것만 기억해두자.

요약하면 이렇다 — RLS의 운영 주의 셋.

1. **EXPLAIN으로 정책 술어가 plan에 들어왔는지 매번 확인.** 안 들어왔으면 정책이 꺼졌거나, 적용 role을 잘못 잡았다.
2. **admin bypass는 privilege(BYPASSRLS, superuser)가 아닌 policy로.** 흔적이 남는 길을 택하자.
3. **테이블 소유자도 정책 적용 — `FORCE ROW LEVEL SECURITY` 한 줄을 잊지 말자.**

이 셋을 항상 함께 끌고 다니면 RLS가 진짜 격리 도구로 작동한다. 그렇지 않으면 그저 "켜놓긴 했다"는 위안만 남는다.

## 16.7 lock-in 트레이드오프 — 자유와 속도 사이

여기까지 본 도구들의 매력은 분명하다. 짧은 시간에 풀스택 시스템 한 벌을 띄우고, 권한·실시간·인증까지 한 결로 묶는다. 사이드 프로젝트나 MVP라면 거절할 이유가 거의 없다. 그런데 진지하게 운영할 시스템을 두고 도입을 고민한다면, 한 가지 묵직한 질문이 따라온다.

"빠져나올 수 있는가?"

이걸 한번에 답하는 일은 어렵다. 결의 결을 갈라야 한다. PostgREST·pg_graphql·Hasura·Supabase는 lock-in의 두께가 다 다르다. 한 묶음으로 "BaaS는 위험하다"고 말하는 건 게으른 결론이다. 하나씩 짚어보자.

### lock-in의 결을 갈라본다

**PostgREST.** lock-in이 가장 옅다. 모든 게 표준 PostgreSQL 안에 있다. 테이블, 뷰, 함수, RLS — 전부 표준 SQL과 PG 기능이다. 어느 날 PostgREST를 빼고 직접 짠 백엔드로 옮겨도, DB 스키마는 그대로 살아남는다. 옮기는 게 일이긴 하지만, 데이터 자체는 인질이 아니다.

**pg_graphql.** 역시 옅다. 익스텐션 하나가 PG 안에 들어가지만, 데이터는 모두 표준 테이블에 있다. pg_graphql을 끄면 GraphQL endpoint가 사라질 뿐 데이터는 그대로다. 클라이언트 코드가 GraphQL 쿼리에 묶여 있는 만큼이 마이그레이션 비용이다. 새 GraphQL 서버를 세워서 같은 스키마를 따라가게 만드는 일은 어려운 과제가 아니다.

**Hasura.** 중간이다. DB 스키마는 그대로지만, **권한 모델이 Hasura 메타데이터에 묶인다**. Actions, Events, Remote Schemas도 Hasura 고유의 추상이다. 빠져나오려면 이걸 다 다른 방식으로 재구성해야 한다. RBAC 메타데이터를 RLS로 옮기는 일은 가능하지만 만만치 않다. Hasura의 가치는 인정하되, "이 메타데이터가 진실의 원천이 된 순간 빠져나오는 비용이 두꺼워진다"는 사실을 받아들이고 도입하는 편이 낫다.

**Supabase.** 가장 두껍다. 그런데 두께가 균일하지 않다.

- **Data API (PostgREST + pg_graphql):** 위에서 본 대로 옅다. 셀프호스트하거나 RDS로 옮겨도 같은 스키마를 그대로 살린다.
- **DB 자체 (PostgreSQL):** 당연히 옅다. `pg_dump`로 받아서 다른 매니지드 PG로 옮기면 끝.
- **Auth (GoTrue):** 중간. GoTrue가 오픈 소스이므로 셀프호스트는 가능하다. 사용자 테이블이 표준 PG 안에 있어서 데이터는 살린다. 다만 JWT 발급 메커니즘과 클라이언트 SDK 호환성을 어떻게 유지할지 고민이 따른다.
- **Storage:** 중간. 오픈 소스이고 S3 호환 객체 저장소를 백엔드로 쓴다. 옮기려면 메타데이터와 파일을 동시에 이관해야 한다.
- **Realtime:** 중간. logical replication 기반이라 원리는 표준 PG의 것이다. 같은 패턴을 자체 서비스로 재구현할 수 있다.
- **Edge Functions:** 가장 두껍다. Deno 런타임에 묶인 코드, Supabase 고유의 컨텍스트. 빠져나오려면 다른 서버리스 플랫폼(Cloudflare Workers, Vercel)에 다시 짜야 한다.

**전체 그림.** Supabase 풀스택을 한 묶음으로 쓰면, 빠져나오는 일은 분명 어렵다. 하지만 그 두께가 균일하지 않다는 사실은 중요하다. **데이터와 권한은 표준 PG 안에 있고, 두꺼운 lock-in은 주변부(Edge Functions, 특정 SDK)에 모인다.** 그래서 진지하게 운영하는 팀이 자주 택하는 절충안이 있다 — 시작은 Supabase로 빠르게, 도메인 핵심 로직만 외부 백엔드 서비스로 분리해서 의존성을 분산. 그러면 어느 날 Supabase에서 자체 인프라로 옮겨야 할 때, 핵심 자산이 그대로 살아남는다.

### lock-in이 정말 문제인가

여기서 멈춰서 한 번 더 생각해보자. lock-in이 항상 나쁜가?

당장 한 사람 또는 작은 팀이 6개월 안에 시장 검증을 끝내야 한다고 해보자. 그 6개월 동안 자체 인프라 구축에 쓰는 시간은 비용이다. lock-in이 없는 "완전 자유"라는 환상에 매달리면, 정작 검증해야 할 가설은 검증되지 못한다. 그 사이 경쟁자가 시장을 가져간다. 자유는 시간이 있는 사람의 사치다.

반대로, 도메인이 굳고 트래픽이 진지해진 시점에서는 lock-in의 비용이 점점 무거워진다. 벤더의 가격 인상, 기능 우선순위 변경, 운영 정책 변경에 휘둘릴 가능성이 커진다. 그때는 "어디까지 자체 인프라로 옮길 것인가"를 진지하게 평가할 시점이다.

그래서 lock-in의 결정은 "예/아니오"가 아니라 "지금 우리 단계에서 적절한 수준은 어디인가"의 문제다. 다음과 같이 가지를 친다.

| 단계 | 적절한 결 |
|------|-----------|
| **개념 검증 (1~3개월)** | Supabase 풀스택. 자유보다 속도. |
| **MVP (3~9개월)** | Supabase + 핵심 로직 분리(별도 backend). 도메인 자산을 외부에 둔다. |
| **성장기 (9~24개월)** | PostgREST/pg_graphql + 자체 운영 PG + 자체 Auth로 단계적 이행 검토. |
| **성숙기 (24개월+)** | 도메인 두께에 따라 정통 백엔드로 옮길지, PostgREST/Hasura를 데이터 layer로 유지할지 결정. |

물론 단계가 칼로 자르듯 나뉘지는 않는다. 작은 SaaS는 성숙기까지도 Supabase 그대로 가는 게 가장 합리적일 수 있다. 큰 엔터프라이즈는 처음부터 PostgREST + 자체 운영을 택하는 게 맞다. 자기 시스템의 도메인 두께, 팀 규모, 검증 단계를 정직하게 보고 결정하는 편이 낫다.

### "DB가 백엔드"라는 말의 진짜 의미

이번 장을 다시 한 번 멀리서 보자. PostgREST, pg_graphql, Hasura, Supabase가 가능하게 만든 패턴이 무엇인가? "DB가 백엔드"라는 표어가 강한 인상을 주지만, 진짜 의미는 따로 있다.

이 도구들이 한 일은 **"백엔드 코드 중에서 정형화 가능한 부분을 DB의 선언으로 옮긴 것"**이다. CRUD는 자동화되고, 권한은 정책으로 선언되고, 실시간 구독은 WAL로 흐른다. 그러면 사람이 짜야 할 코드는 무엇이 남는가? **정형화되지 않는 부분, 즉 도메인 로직, 외부 통합, 깊은 알고리즘.** 그 영역은 여전히 사람이 짜야 한다. 그리고 그게 진짜로 가치 있는 코드다.

그래서 "DB가 백엔드"는 백엔드 개발자가 필요 없다는 말이 아니다. "백엔드 개발자가 진짜 가치 있는 일에 시간을 쓸 수 있게 됐다"는 말이다. CRUD 매핑 코드를 천 번 쓰는 대신, 도메인 로직과 시스템 통합에 시간을 쓰자는 것. 이 관점에서 보면, 16장의 도구들은 백엔드 개발자를 대체하는 게 아니라 해방한다.

물론 모든 시스템이 이 길을 따라야 한다는 결론은 아니다. 도메인이 두꺼운 시스템, 외부 통합이 많은 시스템, 정형화되지 않는 흐름이 대부분인 시스템은 여전히 정통 백엔드가 답이다. 16장에서 본 도구들이 빛나는 자리는 분명히 있고, 그 자리 밖에서는 다른 답이 더 낫다. 둘을 정직하게 가르자.

## 마무리

이번 장을 정리해보자. 네 가지를 기억해두자.

**첫째, "DB가 백엔드"는 CRUD 자동화의 다른 이름이다.** PostgREST는 스키마를 REST로, pg_graphql은 GraphQL로, Hasura는 여러 DB 위 통합 게이트웨이로, Supabase는 그 위에 인증·실시간·저장소까지 묶은 풀스택 BaaS다. 작은 팀과 빠른 검증, 그리고 데이터 모델이 곧 도메인의 80%인 시스템에서 빛난다.

**둘째, 권한은 RLS로 일원화하는 편이 낫다.** 어떤 도구를 쓰든 PostgreSQL의 RLS가 권한 모델의 토대다. 멀티테넌트 SaaS라면 `tenant_id` + `current_setting` + USING/WITH CHECK 패턴이 표준이다. `SET LOCAL`로 박고, `FORCE ROW LEVEL SECURITY`를 빼먹지 말고, admin bypass는 privilege가 아닌 policy로 표현하자. 흔적이 남는 길로 가자는 것이다.

**셋째, EXPLAIN을 늘 같이 봐야 한다.** RLS 정책의 술어는 plan에 들어간다. 정책이 인덱스를 무력화하는 흔한 함정을 피하려면, 정책 도입 후 주요 쿼리의 EXPLAIN을 한 번씩 확인하는 습관이 필요하다. "정책 켜놓고 인덱스 안 만든 채로 운영 들어가서 SELECT가 수십 배 느려졌다"는 야간 호출은 끔찍한 일이다.

**넷째, lock-in의 결을 정직하게 보자.** PostgREST·pg_graphql은 거의 옅고, Hasura는 메타데이터 단위로 중간, Supabase는 부분별로 두께가 다르다. 데이터와 권한은 표준 PG 안에 있다는 사실을 잊지 말자. 단계에 맞는 결을 택하면, 자유와 속도 사이에서 좋은 균형을 찾을 수 있다.

이 장에서 본 RLS는 "어떻게 설계하는가"의 응용 패턴이었다. 같은 RLS를 운영의 관점에서 — 정책이 실제로 잘 작동하는지 어떻게 감사하고 검증하는가 — 본격적으로 다루는 자리는 22장(보안과 감사)이다. pgaudit으로 정책 통과 흔적을 어떻게 남길지, CVE를 어떻게 추적할지, scram-sha-256과 SSL/TLS는 어떻게 강제할지. RLS가 진짜 격리 도구로 자리잡으려면 22장의 도구들과 손을 잡아야 한다.

다음 장(17장)에서는 잠깐 시선을 옮긴다. 지금까지 우리는 PostgreSQL을 활용하는 9가지 시나리오를 따라왔다. Part 4의 첫 자리에서, 그동안 미뤄왔던 한 가지 질문을 정면으로 다룬다 — "MySQL/Oracle을 쓰는 우리 시스템을 PostgreSQL로 진짜 옮길 수 있는가?" 4억 row를 6개월에 걸쳐 옮긴 사람들의 이야기로, 마이그레이션 실전을 같이 따라가 보자.
