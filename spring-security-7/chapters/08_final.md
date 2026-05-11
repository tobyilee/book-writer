# 8장. 권한은 어디에 사는가 — 인가의 5층 구조

**선행 필요:** 2장(필터 체인), 3장(`AuthorizationManager`), 4~7장(권한·SCOPE·Authority의 생산자)

---

운영 중인 주문 시스템에 새 기능을 붙인다고 해보자. "관리자는 모든 주문을 취소할 수 있어야 한다. 매니저는 자기 부서의 주문만 취소할 수 있다. 일반 사용자는 본인이 만든 주문만 취소할 수 있다." 요구사항을 받아들고 IDE를 켠 순간, 가장 먼저 떠오르는 질문은 이것이다. 이 규칙들은 도대체 코드 어디에 살아야 하는가?

`SecurityFilterChain`의 `authorizeHttpRequests`에 한 줄 더 추가하면 될까? 컨트롤러 메서드 위에 `@PreAuthorize`를 붙이면 될까? 아니면 서비스 안에서 `if` 문으로 직접 비교해야 할까? 그것도 아니면 도메인 객체 자체에 권한 정보를 매달아야 할까?

어느 답이든 코드는 작동한다. 그러나 어디에 두느냐에 따라 6개월 뒤 운영의 모습이 완전히 달라진다. URL에만 의존하면 API 한 곳이 깨질 때마다 보안 규칙을 다시 짜야 한다. 서비스 안에 `if` 문을 흩뿌리면 보안 규칙이 비즈니스 로직 사이에 숨어 감사가 불가능해진다. 도메인 객체에 권한을 박으면 객체 모델이 점점 무거워진다.

Spring Security가 이 모든 층위를 한꺼번에 제공하는 데에는 이유가 있다. 모든 권한 검사를 한 층에 몰아넣으려는 시도는 거의 예외 없이 실패한다. 그렇다면 함께 사고 모델을 정돈해보자. 우리가 다룰 인가의 층은 다섯 개다.

## 8.1 권한이 사는 다섯 개의 층

OWASP가 2017판에서 5위였던 "Broken Access Control"을 2021판에서 **1위**로 올린 것은 우연이 아니다. 평균 발견율 3.81%. 열에 가까운 애플리케이션에 권한 결함이 살아 있다는 뜻이다. 그리고 결함의 대부분은 "권한 규칙을 어디에 둘지" 모호하게 흩뿌린 코드에서 자란다.

다섯 개의 층을 한눈에 보자. 위로 갈수록 거칠고(coarse-grained) 아래로 갈수록 미세하다(fine-grained).

```
┌─────────────────────────────────────────────────────┐
│ 1층. URL 패턴       authorizeHttpRequests            │   거칠다
│   ──────────────────────────────────────────────    │
│ 2층. HTTP Method    requestMatchers(POST, "/...")   │
│   ──────────────────────────────────────────────    │
│ 3층. 메서드 경계    @PreAuthorize / @PostAuthorize  │
│   ──────────────────────────────────────────────    │
│ 4층. 메타 어노테이션  @AdminOnly, @CanEditPost       │
│   ──────────────────────────────────────────────    │
│ 5층. 도메인 객체    #post.author == auth.name / ACL  │   미세하다
└─────────────────────────────────────────────────────┘
```

이 그림이 8장의 척추다. 다섯 층은 경쟁 관계가 아니라 **분담 관계**다. URL 한 줄로 막을 수 있는 건 1층에서 막아 비즈니스 코드를 깨끗하게 유지하고, 비즈니스 의미가 강하게 묶이는 규칙은 아래층으로 내려 보낸다. 그러면 코드 본문은 자기 책임에만 집중하고, 보안 규칙은 한곳에 모여 감사 가능한 형태로 남는다.

층 사이의 결정 기준을 한 문장으로 요약하면 이렇다. **"누가 호출했는가"만으로 결정되면 위층, "무엇을 향해 호출했는가"가 함께 필요하면 아래층이다.** `/admin/**`에 매니저 권한을 막는 건 위층의 일이다. "본인이 작성한 글만 수정 가능"이라는 규칙은 도메인 객체를 봐야 결론이 나니 아래층의 일이다.

이제 한 층씩 내려가 보자.

## 8.2 1층 — URL 기반 인가

가장 거친 층은 URL이다. `SecurityFilterChain` 안에서 `authorizeHttpRequests` 한 블록으로 끝난다. 7.0에서 가장 눈에 띄는 변화는 매처가 `PathPatternRequestMatcher`로 통일됐다는 점이다. Spring MVC가 라우팅에 쓰는 바로 그 패턴 파서를 보안 매칭에도 동일하게 쓴다. 6.x 시절 `mvcMatchers`/`antMatchers`/`AntPathRequestMatcher` 사이를 오가며 `/api`와 `/api/`가 같은지 다른지 헷갈리던 시간은 이제 끝난다. 좋은 일이다.

기본 형태부터 보자.

```java
http.authorizeHttpRequests(a -> a
    .requestMatchers(HttpMethod.GET, "/health").permitAll()
    .requestMatchers("/admin/**").hasRole("ADMIN")
    .requestMatchers("/orders/**").hasAuthority("SCOPE_orders.read")
    .anyRequest().authenticated()
);
```

코드를 위에서 아래로 읽으면 그대로 의미가 잡힌다. `/health`는 누구나 통과. `/admin/**`은 `ADMIN` 역할만. `/orders/**`는 `SCOPE_orders.read` 권한을 가진 자만. 그 외 모든 요청은 인증된 사용자여야 한다.

여기서 한 가지 짚고 가자. **순서가 의미를 만든다.** Spring Security는 위에서 아래로 매칭을 시도하고, 첫 매치에서 결정을 확정한다. `anyRequest()`를 가장 먼저 두면 그 아래 규칙들은 영원히 도달하지 않는다. 처음 이 사실을 모르고 `anyRequest().permitAll()`을 맨 위에 둔 코드는 그야말로 끔찍한 일이다. 모든 URL이 무방비로 열린다.

7.0의 통일 매처는 path variable 매칭도 일관되게 처리한다.

```java
var p = PathPatternRequestMatcher.withDefaults();
http.authorizeHttpRequests(a -> a
    .requestMatchers(p.matcher("/products/{id}")).hasRole("USER")
    .requestMatchers(p.matcher("/products/{id}/edit")).hasRole("ADMIN")
    .anyRequest().authenticated());
```

같은 path variable을 컨트롤러와 보안 규칙이 똑같이 해석한다는 점은 마음의 평화에 큰 도움이 된다. 6.x에서 trailing slash 하나로 403과 200이 갈렸던 함정이 사라진 셈이다.

## 8.3 2층 — HTTP Method까지 보는 인가

URL이 같아도 `GET`과 `POST`는 의미가 다르다. 같은 `/posts/{id}`라도 조회는 누구나 가능하지만 수정은 작성자만 가능해야 하는 경우가 그렇다. 이때 2층으로 내려간다.

```java
http.authorizeHttpRequests(a -> a
    .requestMatchers(HttpMethod.GET,  "/posts/**").permitAll()
    .requestMatchers(HttpMethod.POST, "/posts/**").hasRole("USER")
    .requestMatchers(HttpMethod.PUT,  "/posts/**").hasRole("USER")
    .requestMatchers(HttpMethod.DELETE, "/posts/**").hasRole("ADMIN")
    .anyRequest().authenticated()
);
```

HTTP 메서드를 첫 인자로 추가하기만 하면 끝이다. 코드를 읽어보면 머릿속에 자연스럽게 "조회는 열고, 작성·수정은 사용자, 삭제는 관리자"라는 문장이 그려진다. 의미가 코드에 그대로 박힌다. 이게 1·2층 인가가 주는 가장 큰 가치다. **권한 규칙이 비즈니스 코드 바깥에 명문화되어 한곳에 모인다.**

여기서 `hasRole`과 `hasAuthority`, `hasAnyRole`이 어떻게 다른지 한 번 정리하고 가는 편이 낫다. 이 셋의 차이를 모호하게 두면 두고두고 디버깅의 원흉이 된다.

### `hasRole` vs `hasAuthority` vs `hasAnyRole`

Spring Security 내부에서 권한은 모두 `GrantedAuthority`라는 한 가지 타입이다. `ROLE_ADMIN`, `SCOPE_orders.read`, `factor.password` 같은 문자열이 모두 같은 통 안에 들어 있다. 그렇다면 왜 `hasRole`과 `hasAuthority`가 따로 있을까?

답은 `ROLE_` 접두사다.

- `hasRole("ADMIN")` — 내부에서 자동으로 `"ROLE_"`을 붙여 `ROLE_ADMIN`을 찾는다. 인자에는 절대 `ROLE_`을 붙이지 말자.
- `hasAuthority("ROLE_ADMIN")` — 접두사를 붙이지 않는다. 문자열 그대로 매칭한다.
- `hasAuthority("SCOPE_orders.read")` — OAuth2 스코프처럼 `ROLE_`이 붙지 않는 권한을 검사할 때 쓴다.
- `hasAnyRole("ADMIN", "STAFF")` — `hasRole`의 OR 버전. 역시 `ROLE_`이 자동으로 붙는다.
- `hasAnyAuthority(...)` — `hasAuthority`의 OR 버전. 접두사 처리 안 함.

규칙을 한 줄로 요약하면, **"`ROLE_`을 자동으로 붙여주는 게 `hasRole`, 안 붙이는 게 `hasAuthority`"**다. 두 함수를 같은 코드에서 섞어 쓸 때 가장 자주 사고가 난다. 예를 들어 `hasRole("ROLE_ADMIN")`이라고 쓰면 내부에서 `ROLE_ROLE_ADMIN`을 찾아 헤매다 실패한다. 이런 코드가 운영 환경에 올라가서 며칠 동안 "왜 관리자가 들어가지지 않는다는 컴플레인이 들어오지?"로 헤매면 정말로 난감해진다. 기억해두자.

OAuth2 스코프는 거의 항상 `hasAuthority`로 검사한다. 5장에서 본 것처럼 JWT의 `scope` 클레임은 기본적으로 `SCOPE_` 접두사가 붙은 `GrantedAuthority`로 매핑된다. `SCOPE_`는 `ROLE_`이 아니므로 `hasRole`로는 잡을 수 없다.

## 8.4 3층 — 메서드 경계의 인가

URL이 막지 못하는 상황을 생각해보자. 같은 컨트롤러의 같은 엔드포인트로 들어오는 요청인데, 내부의 어떤 서비스 메서드를 호출하느냐에 따라 권한이 갈려야 한다면 어떻게 할까? 또는 컨트롤러를 거치지 않고 스케줄러·메시지 컨슈머가 비즈니스 메서드를 직접 부를 때 동일한 권한 규칙을 적용하고 싶다면?

이때 3층이 필요하다. 메서드에 직접 인가를 거는 Method Security다.

```java
@Configuration
@EnableMethodSecurity   // ← 7.0의 표준
class SecConfig {}

@Service
class OrderService {

    @PreAuthorize("hasRole('ADMIN')")
    public void cancelAll() { ... }

    @PreAuthorize("hasAnyRole('ADMIN', 'MANAGER')")
    public Order findById(Long id) { ... }
}
```

`@PreAuthorize`는 메서드 진입 직전에 SpEL 식을 평가해 통과 여부를 결정한다. 통과하지 못하면 `AccessDeniedException`이 던져지고, 8.10절에서 다룰 `ExceptionTranslationFilter`가 이를 403 응답으로 번역한다. `@PostAuthorize`는 메서드가 반환한 뒤 반환값을 보고 결정한다. `@Secured`는 역할만 보는 단순한 형태다. `@PreAuthorize`가 가장 표현력이 좋고, 실무에서 압도적으로 많이 쓰인다.

여기서 가장 중요한 함정을 한 절 통째로 할애해 짚어야 한다.

### 함정 — `@EnableGlobalMethodSecurity` 잔존 시 `@PreAuthorize`가 소리 없이 무력화된다

6.2.7 issue #17487에 이런 질문이 올라온 적이 있다.

> "왜 내 `@PreAuthorize`가 동작 안 하는지 모르겠다. 코드는 컴파일되고, 앱은 정상 기동되고, 에러도 안 난다. 그런데 관리자 권한이 없는 사용자도 `cancelAll()`을 호출할 수 있다."

원인은 단 한 줄이었다. 설정 클래스에 옛날 어노테이션 `@EnableGlobalMethodSecurity`가 그대로 남아 있던 것. Spring Security 6.x 어느 시점부터 이 어노테이션은 deprecated가 되었고, 6.2.7에서는 **메서드 보안 빈(`MethodSecurityInterceptor`)을 등록하지 않는다.** 경고 로그도, 예외도 없다. `@PreAuthorize`가 그냥 평범한 어노테이션 한 줄이 되어 컴파일러를 통과한다.

> "If you only supply `@EnableGlobalMethodSecurity`, no method-security beans are registered, and no warning or error is logged. As a result, annotations like `@PreAuthorize` silently have no effect." — Spring Security issue #17487

소리 없이 깨지는 건 가장 끔찍한 종류의 버그다. 빨간 줄이 뜨지 않고, 테스트가 잘 짜여 있지 않으면 운영에 올라가서야 발견된다. 그것도 누군가 권한 검사를 우회한 흔적이 로그에 찍히고 나서.

7.0으로 올릴 때, 또는 6.x에서 이미 작업 중이라면 반드시 한 번은 전체 모듈을 grep해두자.

```bash
grep -rn "@EnableGlobalMethodSecurity" src/
```

한 줄이라도 잡히면 즉시 `@EnableMethodSecurity`로 교체한다. `@EnableMethodSecurity`는 `@PreAuthorize`/`@PostAuthorize`/`@Secured`/`@PreFilter`/`@PostFilter`를 모두 기본 활성화한다. 옵션(`prePostEnabled`, `securedEnabled` 등)을 굳이 명시할 필요도 없다. 모르고 옛 어노테이션을 쓰는 것보다, 명확하게 새 어노테이션 한 줄을 두고 두 발 뻗고 자는 편이 낫다.

### SpEL의 매력과 위험

`@PreAuthorize`의 진짜 힘은 SpEL에서 나온다.

```java
@PreAuthorize("hasRole('ADMIN') and #user.id == authentication.principal.id")
public void updateProfile(User user) { ... }
```

이 식은 두 가지를 동시에 검사한다. 호출자가 `ADMIN` 역할을 가졌고, **메서드 인자로 들어온 `user` 객체의 `id`가 인증된 주체의 `id`와 같은가**. SpEL 안에서 메서드 인자(`#user`), 인증 객체(`authentication`), 주체(`principal`)를 모두 참조할 수 있다. 이게 매력이다. 비즈니스 의미를 어노테이션 한 줄에 담을 수 있다.

그러나 매력은 위험과 짝을 이룬다. 식이 길어지면 어떤 일이 벌어지는지 보자.

```java
@PreAuthorize(
  "hasRole('ADMIN') or " +
  "(hasRole('MANAGER') and #order.department == authentication.principal.department) or " +
  "(hasRole('USER') and #order.userId == authentication.principal.id and " +
  "  #order.status == T(com.example.OrderStatus).DRAFT)"
)
public void cancelOrder(Order order) { ... }
```

코드 본문보다 어노테이션이 길다. SpEL이라 컴파일 타임 타입 체크가 약하고, 리팩토링 때 IDE가 따라가지 못한다. 단위 테스트를 짜려면 `MethodSecurityExpressionHandler` 컨텍스트가 필요해서 순수 자바 테스트로는 검증되지 않는다.

**보안 규칙이 코드 본문을 가린다면, 결국 보안이 비즈니스의 적이 된다.** 어떤 시점이 오면 SpEL을 줄이고 비즈니스 메서드 안에서 명시적으로 `AuthorizationManager`를 부르는 편이 낫다. SpEL은 "한 문장으로 자연스럽게 읽힐 때까지"가 사용 한계라고 마음에 두자.

### 커스텀 SpEL 함수 — `MethodSecurityExpressionHandler`

SpEL 식이 반복된다면 함수로 추출하는 편이 깔끔하다. `MethodSecurityExpressionRoot`를 확장하거나, 별도 빈을 등록해 `@bean.method()` 형태로 호출할 수 있다.

```java
@Component("perm")
class PermissionChecker {
    public boolean canEditOrder(Long orderId) {
        // 복잡한 권한 로직을 자바로 표현
        return orderRepository.findById(orderId)
            .map(o -> o.belongsToCurrentUser())
            .orElse(false);
    }
}

@Service
class OrderService {
    @PreAuthorize("@perm.canEditOrder(#orderId)")
    public void edit(Long orderId, EditCommand cmd) { ... }
}
```

SpEL 식은 짧게 유지하고 복잡한 판단은 자바 코드에 둔다. 테스트도 `PermissionChecker`만 단위 테스트로 검증할 수 있다. **SpEL은 가능한 한 호출 한 줄에 가깝게 유지하는 편이 바람직하다.**

`MethodSecurityExpressionHandler`를 직접 커스터마이즈해야 하는 경우는 흔하지 않다. 다만 모든 메서드 보안 식에 공통 변수를 주입하거나, 평가 환경을 통째로 바꿔야 할 때는 빈으로 노출해 교체할 수 있다.

```java
@Bean
static MethodSecurityExpressionHandler expressionHandler(RoleHierarchy roleHierarchy) {
    var handler = new DefaultMethodSecurityExpressionHandler();
    handler.setRoleHierarchy(roleHierarchy);
    return handler;
}
```

여기에 8.7절에서 다룰 `RoleHierarchy`를 주입하면, `@PreAuthorize("hasRole('STAFF')")`라고 써도 `ADMIN`이 자동 통과한다.

## 8.5 4층 — 메타 어노테이션으로 의미를 묶기

`@PreAuthorize("hasRole('ADMIN')")`가 코드베이스 곳곳에 반복된다고 상상해보자. 50개 메서드에 같은 식이 박혀 있다면, 정책이 바뀌어 `ADMIN`을 `SUPER_ADMIN`으로 바꿔야 할 때 50번 수정해야 한다. 한 줄이라도 빠뜨리면 그 메서드는 다음 빌드까지 잠재적 보안 구멍으로 남는다. 찜찜한 일이다.

해법은 의미를 묶는 것이다. Spring Security 6.3부터 메타 어노테이션 패턴이 1급으로 지원된다.

```java
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@PreAuthorize("hasRole('ADMIN')")
public @interface AdminOnly {}

@Service
class OrderService {
    @AdminOnly
    public void cancelAll() { ... }

    @AdminOnly
    public void purgeOldOrders() { ... }
}
```

`@AdminOnly`라는 이름이 코드에 박힌다. 의미가 즉시 읽힌다. 그리고 정책이 바뀌면 `@AdminOnly` 어노테이션 정의 한 곳만 수정하면 된다. 50개 메서드는 그대로다.

좀 더 흥미로운 예를 보자.

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@PreAuthorize("hasRole('USER') and #post.author == authentication.name")
public @interface CanEditOwnPost {}

@Service
class PostService {
    @CanEditOwnPost
    public void edit(Post post, EditCommand cmd) { ... }
}
```

"자신이 작성한 게시물만 수정 가능"이라는 정책이 어노테이션 이름으로 코드에 박힌다. 본문은 그저 `edit(...)` 한 줄이다. **코드와 정책이 한 줄 안에 자연스럽게 동거한다.** 이 정도가 메서드 보안의 이상적인 모습이다.

7장에서 본 `@EnableMultiFactorAuthentication`도 사실은 메타 어노테이션 묶음의 한 형태다. MFA 정책을 `factor.password`와 `factor.ott` 같은 권한으로 표현하고, 메타 어노테이션으로 의미를 묶는 흐름이 7.0의 권장 방향이다.

## 8.6 5층 — 도메인 객체 단위 인가

가장 미세한 층이다. "본인이 작성한 게시물만 수정 가능"이라는 규칙은 4층 메타 어노테이션의 SpEL로 표현했지만, 그것이 가능했던 건 `#post`라는 메서드 인자에서 작성자 정보를 꺼낼 수 있었기 때문이다. 인자만으로 결정되지 않고 더 복잡한 객체 단위 권한이 필요하다면 어떻게 할까?

대부분의 경우, SpEL과 `AuthorizationManager`만으로 충분히 풀린다.

```java
@PreAuthorize("#post.author == authentication.name")
public void deletePost(Post post) { ... }
```

```java
@PreAuthorize("@postPermissionService.canEdit(#postId, authentication.name)")
public void editPost(Long postId) { ... }
```

이 두 패턴이 5층의 90%를 차지한다. SpEL이 객체 속성과 인증 주체를 직접 비교하거나, 별도 권한 빈에 위임해서 자바 코드로 판단을 위임하는 것. 권한 결정이 객체의 상태에 따라 달라지더라도 결국 한 번의 함수 호출로 답이 나온다면 이 두 패턴으로 끝난다.

> ### 박스 — 도메인 객체 ACL이 필요해지는 순간
>
> 그런데 가끔, 정말 가끔, 객체 인스턴스 단위 권한이 시스템 전체에 걸쳐 영속화되어야 하는 경우가 있다. "특정 게시물 ID에 대해 사용자 A는 읽기, B는 읽기·쓰기, C는 권한 없음"이 데이터로 관리되는 위키 시스템이나 협업 도구가 그렇다. 이때 `spring-security-acl` 모듈이 등장한다.
>
> ACL은 별도 테이블(`acl_object_identity`, `acl_entry` 등)에 객체별 권한을 저장하고, `@PreAuthorize("hasPermission(#post, 'WRITE')")` 같은 표현식으로 검사한다. 강력하지만 **무겁다.** 별도 스키마, 별도 캐시, 별도 운영. 작은 시스템에서 도입하면 배보다 배꼽이 더 커진다.
>
> 그러니 ACL은 마지막 선택지로 두는 편이 낫다. 객체 ID별 권한 저장이 시스템의 핵심 기능이라면 도입하고, 그게 아니라면 SpEL과 `AuthorizationManager` 빈으로 충분하다. "ACL이 필요한 것 같다"고 느낄 때, 한 번 더 "이 정책을 권한 빈 하나로 표현할 수 없는가?"를 물어보자.

도메인 객체 인가의 핵심은 결국 **"코드 본문은 비즈니스만, 권한은 메타 어노테이션이나 SpEL로 모아두기"**다. 객체 안에 권한 메서드(`isOwnedBy(user)` 같은)를 두는 건 자연스럽지만, 그것을 호출하는 책임은 도메인 객체 자신이 아니라 메서드 보안 층에 두는 편이 깔끔하다.

## 8.7 Role Hierarchy — 권한을 계층으로 묶기

요구사항이 이렇게 바뀌었다고 해보자. "관리자는 매니저가 할 수 있는 일을 모두 할 수 있어야 한다. 매니저는 일반 사용자가 할 수 있는 일을 모두 할 수 있어야 한다." 가장 둔한 방법은 모든 메서드에 `hasAnyRole('ADMIN', 'MANAGER')`라고 죽 늘어놓는 것이다. 또는 `MANAGER` 권한을 검사하는 곳마다 `ADMIN`도 함께 포함시키는 것이다. 컴파일은 되지만, 관리·매니저·사용자 권한 사이의 의미 관계가 코드 전체에 흩어져 보이지 않게 된다.

Spring Security는 이 문제를 `RoleHierarchy`로 깔끔하게 해결한다.

```java
@Bean
static RoleHierarchy roleHierarchy() {
    return RoleHierarchyImpl.withDefaultRolePrefix()
        .role("ADMIN").implies("MANAGER")
        .role("MANAGER").implies("USER")
        .build();
}

@Bean
static GrantedAuthorityDefaults authorityDefaults() {
    return new GrantedAuthorityDefaults("ROLE_");
}
```

한 번 빈으로 등록해두면 `ADMIN`으로 인증된 사용자는 `MANAGER`와 `USER` 권한도 자동으로 가진 것처럼 동작한다. 코드의 모든 `hasRole`, `hasAuthority` 검사에 이 계층이 일관되게 적용된다. 권한 사이의 관계가 한곳에 명문화되어 보이고, 메서드 단위 규칙은 가장 적합한 최소 권한만 적시하면 된다. 깔끔하다.

`withDefaultRolePrefix()`는 `ROLE_` 접두사를 자동으로 붙여주는 빌더다. `role("ADMIN")`이라고만 써도 내부에서는 `ROLE_ADMIN`을 다루고, `implies("MANAGER")`도 같은 방식이다. 만약 `ROLE_` 외의 접두사를 쓰거나 접두사 없이 권한을 다룬다면 `withRolePrefix("")`나 다른 빌더 옵션을 쓸 수 있지만, 표준 관행을 그대로 따르는 편이 협업에서 혼란을 줄인다.

주의할 점이 하나 있다. **Role Hierarchy는 `MethodSecurityExpressionHandler`와 `AuthorizationManager` 양쪽 모두에 주입되어야 일관되게 동작한다.** Spring Boot의 자동 설정이 대부분 해주지만, 커스텀 `MethodSecurityExpressionHandler`를 등록하면서 `setRoleHierarchy(...)`를 빼먹으면 메서드 보안에서만 계층이 동작 안 하는 묘한 상황이 벌어진다. 그러면 URL에서는 계층이 통하는데 메서드에서는 안 통하는, 정말 찜찜한 디버깅 시간을 보내게 된다. 잊지 말자.

## 8.8 `AuthorizationManagerFactory` — 권한 빌더의 중앙 집중

7장에서 MFA를 다룰 때 슬쩍 언급한 `AuthorizationManagerFactory`가 본격적으로 무대에 오를 차례다. 7장에서는 "선택적 MFA를 표현할 때 `AuthorizationManagerFactory.allAuthorities(...)`로 두 factor를 AND로 묶는다"라는 미리보기로 끝났다. 그 빌더가 어디서 왔는지 이제 그림이 잡힌다.

`AuthorizationManagerFactory`는 7.0에서 도입된 팩토리 추상화다. `permitAll()`, `hasRole(...)`, `hasAnyRole(...)`, `hasAuthority(...)`, `allAuthorities(...)`, `anyAuthority(...)` 같은 빌더를 한 곳에서 만들어내고, 그 기본값(접두사, `RoleHierarchy`, `AuthenticationTrustResolver`)을 한 곳에서 커스터마이즈할 수 있다.

```java
@Bean
AuthorizationManagerFactory<Object> authorizationManagerFactory(
        RoleHierarchy roleHierarchy) {
    return AuthorizationManagerFactories.<Object>multiFactor()
        .roleHierarchy(roleHierarchy)
        .build();
}
```

그리고 7장의 MFA 패턴이 자연스럽게 이어진다.

```java
AuthorizationManager<RequestAuthorizationContext> requireMfa =
    authzFactory.allAuthorities("factor.password", "factor.ott");

http.authorizeHttpRequests(a -> a
    .requestMatchers("/sensitive/**").access(requireMfa)
    .anyRequest().authenticated());
```

`allAuthorities`는 7.0 신규 `AllAuthoritiesAuthorizationManager`를 만들어 두 권한을 **AND**로 요구한다. 이게 `hasAnyAuthority`(OR)와 짝을 이루는 새 구현체다. 비밀번호로 인증했고 OTT까지 거친 사용자만 `/sensitive/**`에 접근할 수 있다. 7장의 MFA가 결국 인가의 한 모양이라는 것이 이제 명확해진다.

`AuthorizationManagerFactory`의 진짜 가치는 **모든 권한 검사의 기본 동작을 한 곳에서 통제할 수 있다는 점**이다. 접두사를 `ROLE_` 대신 `AUTH_`로 바꾸고 싶다면? `roleHierarchy`를 빌더에 통합하고 싶다면? 익명 사용자도 일부 권한 검사를 통과시키고 싶다면? 모두 이 팩토리 한 곳에서 끝난다.

## 8.9 거부를 어떻게 표현할 것인가 — `AuthenticationEntryPoint`와 `AccessDeniedHandler`

권한 결정의 절반은 통과시키는 것이고, 나머지 절반은 거부하는 것이다. 그리고 거부하는 방식이 일관되지 않으면 클라이언트는 매우 혼란스러워진다. 어떤 API는 401을 주고, 어떤 API는 302를 주고, 또 어떤 API는 500을 주고 JSON 안에 한국어 에러 메시지가 들어 있는 식이라면, 프론트엔드 개발자는 분기 처리에 점점 화가 난다. 그것도 정말로 화가 난다.

Spring Security가 이 거부를 어떻게 다루는지는 2장에서 한 번 살펴봤다. 여기서 다시 짚고, 8장에서 이를 어떻게 커스터마이즈할지 본다.

### 두 핸들러의 분기점 — `ExceptionTranslationFilter`

`ExceptionTranslationFilter`는 필터 체인의 거의 끝에 자리잡고, 자신보다 뒤쪽 필터에서 던져진 보안 예외를 잡아 일관된 HTTP 응답으로 번역한다. 핵심은 두 가지 예외를 두 가지 핸들러로 보낸다는 점이다.

```
try {
    chain.doFilter(req, res);
} catch (AuthenticationException ae) {
    // "당신이 누군지 모릅니다" 또는 "당신의 인증이 만료됐습니다"
    authenticationEntryPoint.commence(req, res, ae);
} catch (AccessDeniedException ade) {
    if (anonymous(authentication)) {
        // 익명인데 권한 자원에 접근 → 일단 로그인부터
        authenticationEntryPoint.commence(req, res, ade);
    } else {
        // 인증은 됐는데 권한이 없음
        accessDeniedHandler.handle(req, res, ade);
    }
}
```

요약하면 이렇다.

- `AuthenticationEntryPoint` — **인증되지 않은 사용자가 보호된 자원에 접근**할 때 호출된다. 401 응답을 주거나, 로그인 페이지로 리다이렉트한다.
- `AccessDeniedHandler` — **인증된 사용자가 권한이 부족한 자원에 접근**할 때 호출된다. 403 응답을 준다.

두 핸들러는 한 쌍이다. 한쪽만 커스터마이즈하고 다른 쪽을 기본값으로 두면 응답 형태가 들쭉날쭉해진다. 짝지어 함께 다루자.

### REST API를 위한 ProblemDetail 응답

전통적인 폼 로그인 앱이라면 기본 동작이 알맞다. 인증이 필요하면 로그인 페이지로 리다이렉트, 권한이 부족하면 403 페이지를 보여준다. 그러나 REST API라면 사정이 다르다. 클라이언트는 사람이 아니라 SPA의 JavaScript 코드다. HTML 페이지를 받으면 무엇을 해야 할지 모른다.

RFC 7807이 정의한 `ProblemDetail` 표준 형태로 응답하는 편이 깔끔하다.

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .exceptionHandling(e -> e
            .authenticationEntryPoint(restAuthenticationEntryPoint())
            .accessDeniedHandler(restAccessDeniedHandler()))
        .build();
}

private AuthenticationEntryPoint restAuthenticationEntryPoint() {
    return (req, res, ex) -> {
        var problem = ProblemDetail.forStatus(HttpStatus.UNAUTHORIZED);
        problem.setTitle("Authentication required");
        problem.setDetail("이 자원에 접근하려면 인증이 필요합니다.");
        problem.setType(URI.create("https://api.example.com/errors/unauthorized"));
        writeProblem(res, problem);
    };
}

private AccessDeniedHandler restAccessDeniedHandler() {
    return (req, res, ex) -> {
        var problem = ProblemDetail.forStatus(HttpStatus.FORBIDDEN);
        problem.setTitle("Access denied");
        problem.setDetail("이 자원에 접근할 권한이 없습니다.");
        problem.setType(URI.create("https://api.example.com/errors/forbidden"));
        writeProblem(res, problem);
    };
}

private void writeProblem(HttpServletResponse res, ProblemDetail problem) throws IOException {
    res.setStatus(problem.getStatus());
    res.setContentType(MediaType.APPLICATION_PROBLEM_JSON_VALUE);
    new ObjectMapper().writeValue(res.getWriter(), problem);
}
```

응답이 일관된 모양을 갖는다. 클라이언트는 `application/problem+json` 한 가지만 알면 된다. 401과 403의 차이도 명확히 구분된다. 9장에서 다룰 보안 헤더와 짝을 이뤄, "거부 응답이 어떤 메타데이터를 함께 가져야 하는가"라는 더 큰 질문에 답할 수 있다.

### Method Security의 거부 응답 — `MethodAuthorizationDeniedHandler`

3층 메서드 보안이 거부될 때, 즉 `@PreAuthorize`가 실패할 때도 같은 모양의 응답을 주고 싶다면 `MethodAuthorizationDeniedHandler`를 활용한다. 6.3+에서 추가된 기능이다.

```java
@PreAuthorize("hasRole('ADMIN')")
@HandleAuthorizationDenied(handlerClass = AdminOnlyDeniedHandler.class)
public void cancelAll() { ... }
```

`AdminOnlyDeniedHandler`는 `MethodAuthorizationDeniedHandler` 구현체로, 거부됐을 때의 응답이나 대체 반환값을 정의한다. URL 인가의 `AccessDeniedHandler`와 의미적으로 같은 짝이지만, 메서드 단위로 동작한다. `@ControllerAdvice`로 `AccessDeniedException`을 잡는 방법도 있지만, 메서드 보안의 의미를 어노테이션 안에 응축하고 싶다면 `@HandleAuthorizationDenied`가 더 자연스럽다.

`@ControllerAdvice`로 `AccessDeniedException`/`AuthenticationException`을 잡아 통합 처리하는 패턴도 흔히 쓰인다. 그러나 주의해야 한다. **`ExceptionTranslationFilter`가 컨트롤러보다 뒤쪽(바깥쪽)에 있다는 사실을 기억하자.** 컨트롤러에서 던져진 보안 예외는 `@ControllerAdvice`로 잡힐 수 있지만, 컨트롤러까지 도달하지 못한 인가 거부(`AuthorizationFilter`에서 막힌 것)는 `ExceptionTranslationFilter`만 잡을 수 있다. 두 경로를 통합하려면 양쪽 모두 같은 응답 포맷을 쓰도록 맞춰야 한다.

## 8.10 인가와 OWASP A01 — 한눈에 매핑

OWASP Top 10 2021에서 "Broken Access Control"이 1위로 올라왔다는 사실을 처음에 언급했다. 평균 발견율 3.81%. 이제 5층 모델 위에서 이 통계를 다시 읽어보자.

| OWASP A01 결함 유형 | 5층 구조에서의 대응 |
|---------------------|---------------------|
| URL 접근 제어 누락 | 1·2층 — `authorizeHttpRequests` + `anyRequest().authenticated()` |
| HTTP 메서드 우회(`GET`은 막았는데 `POST`는 통과) | 2층 — `requestMatchers(HttpMethod, ...)` |
| 비즈니스 로직 권한 누락 | 3·4층 — `@PreAuthorize`, 메타 어노테이션 |
| IDOR(Insecure Direct Object Reference) | 5층 — `#post.author == authentication.name` 또는 권한 빈 |
| Role 상승 / Vertical privilege escalation | Role Hierarchy + 메타 어노테이션 일관성 |
| 거부 응답 누설 / 누락 | 8.9절 `AccessDeniedHandler` + ProblemDetail |

5층 중 어느 한 층이라도 비어 있으면 그 자리가 곧 A01의 결함이 된다. 1층만으로 막으려 들면 IDOR이 새고, 5층만 짜놓고 1층을 비워두면 URL 통째로 노출된다. **다섯 층은 함께 묶일 때 완전해진다.** OWASP가 보여주는 발견율 3.81%는 그 어느 한 층의 결함이 아니라, 층들 사이의 연결이 끊어진 자리에서 자라난 결과다.

## 8.11 정리 — 권한이 사는 자리를 결정하는 법

다섯 층을 한 그림으로 묶어 다시 보면, 결국 결정은 두 축으로 내려진다. **하나는 결정에 필요한 정보의 위치(URL인가, 메서드 인자인가, 객체 상태인가), 다른 하나는 그 규칙이 얼마나 자주 바뀌는가(인프라처럼 안정적인가, 비즈니스처럼 변하는가)**다.

URL과 HTTP 메서드만으로 결론이 나는 규칙은 위로 올린다. 결정에 객체의 상태가 필요하면 아래로 내린다. 자주 바뀌는 비즈니스 규칙은 자바 코드(권한 빈)로 두어 IDE의 도움을 받는다. 안정적이고 광범위한 규칙은 URL 매처나 메타 어노테이션으로 명문화한다.

기억할 다섯 가지만 추리자.

1. **`@EnableGlobalMethodSecurity`는 즉시 grep해 `@EnableMethodSecurity`로 교체한다.** 소리 없이 깨지는 보안만큼 끔찍한 건 없다.
2. **`hasRole`은 `ROLE_`을 자동으로 붙이고, `hasAuthority`는 안 붙인다.** OAuth2 스코프는 `hasAuthority("SCOPE_...")`로 검사한다.
3. **SpEL이 코드 본문을 가리면 권한 빈으로 추출한다.** `@PreAuthorize("@perm.canEdit(#id)")`가 긴 SpEL보다 낫다.
4. **Role Hierarchy는 한 곳에 명문화하고, `MethodSecurityExpressionHandler`에도 같이 주입한다.** URL과 메서드의 계층이 어긋나면 디버깅이 끔찍해진다.
5. **`AuthenticationEntryPoint`와 `AccessDeniedHandler`는 짝으로 커스터마이즈한다.** API는 ProblemDetail로, 401과 403을 명확히 구분해서.

8장에서 우리는 인증된 사용자에게 "무엇을 허용할지" 결정하는 다섯 층을 둘러봤다. 다음 9장에서는 다른 종류의 문제를 다룬다. **인증·인가가 다 통과한 정상 요청처럼 보이는데, 사실은 다른 사이트에서 위조해 보낸 요청이라면?** CSRF가 던지는 질문이다. 그리고 그것과 한 묶음으로 헷갈리는 CORS, 그리고 헤더 한 줄이 막아주는 위협들까지 — 가장 헷갈리는 셋을 한 챕터에서 풀어보자.

---

## 판권 / 콜로폰 참조

- 본 챕터 인용: OWASP Top 10 2021 — A01 Broken Access Control (avg. incidence 3.81%)
- Spring Security 공식 문서 — `authorizeHttpRequests`, `@EnableMethodSecurity`, `AuthorizationManager`
- Spring Security issue #17487 — `@EnableGlobalMethodSecurity` 잔존 시 `@PreAuthorize` 무력화
- RFC 7807 — Problem Details for HTTP APIs
