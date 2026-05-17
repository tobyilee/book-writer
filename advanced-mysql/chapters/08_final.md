# 8장. 도메인 모델링과 스키마 설계의 만남

도메인 주도 설계(DDD) 책을 읽고 애그리거트를 잘 정의했다. Order, OrderItem, Customer가 있고 Order 안에 OrderItem들이 들어있는 구조다. 그런데 막상 테이블을 만들려고 하면 질문들이 쌓인다. Order와 OrderItem은 다른 테이블인데, PK는 어떻게 잡아야 할까? 삭제된 주문은 테이블에서 지워야 하나, 아니면 `deleted_at` 컬럼을 두어야 하나? 외래 키 제약은 어디까지 걸어야 하나? UUID를 써도 성능이 괜찮을까?

이런 질문은 도메인 모델링과 InnoDB 물리 구조가 만나는 접점에서 나온다. 둘을 따로 보면 각각은 명확한데, 함께 놓으면 트레이드오프가 생긴다. 그 트레이드오프를 같이 살펴보자.

## 애그리거트와 InnoDB 클러스터링 인덱스를 같은 그림에서 보기

DDD에서 애그리거트(Aggregate)는 하나의 일관성 경계다. Order 애그리거트 안에 OrderItem들이 있고, 이 경계 안의 데이터는 항상 일관성 있게 유지된다. 외부에서는 Order라는 루트를 통해서만 내부를 변경할 수 있다.

InnoDB에서는 PK가 클러스터링 인덱스다. 즉, 테이블의 데이터 자체가 PK 순서로 B+Tree에 저장된다. 같은 PK 범위에 있는 행들은 물리적으로 가까운 디스크 페이지에 있다.

이 두 가지를 연결하면 흥미로운 인사이트가 나온다. 애그리거트의 하위 항목들이 물리적으로 가까이 있으면 한 번의 디스크 IO로 많이 읽어올 수 있다.

```sql
-- OrderItem의 PK를 order_id를 포함한 복합 키로 잡으면
-- 같은 주문의 아이템들이 order_id 범위 안에 모인다
CREATE TABLE order_items (
    order_id    BIGINT UNSIGNED NOT NULL,
    item_seq    INT UNSIGNED NOT NULL,   -- 주문 안에서의 순번
    product_id  BIGINT UNSIGNED NOT NULL,
    quantity    INT NOT NULL,
    unit_price  DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (order_id, item_seq),    -- 복합 PK
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

이렇게 하면 `WHERE order_id = ?`로 특정 주문의 아이템을 조회할 때 클러스터링 인덱스 범위 스캔이 일어나고, 관련 행들이 같은 페이지나 인접 페이지에 있으므로 IO가 효율적이다.

반면 auto_increment PK를 단독으로 쓰면 아이템들이 삽입 순서대로 흩어진다. 주문 A의 아이템 1이 page 100에, 주문 B의 아이템 2가 page 101에, 주문 A의 아이템 2가 page 200에 있을 수 있다. `JOIN`으로 주문과 아이템을 같이 조회할 때 여러 페이지를 오가게 된다.

애그리거트 패턴과 InnoDB 클러스터링을 맞추는 것이 항상 가능하지는 않다. 하지만 "하위 엔티티의 PK에 상위 ID를 포함할 수 있는가"를 한 번 검토해보는 것은 가치 있다.

## PK 전략 — auto_increment, UUID, Snowflake

PK 선택은 생각보다 영향이 넓다. 클러스터링 인덱스이기 때문에 삽입 패턴, 조회 패턴, 심지어 배치 처리(10장에서 다룬다)에도 영향을 준다.

### auto_increment — 단순하고 효율적이지만 노출이 찜찜하다

가장 단순한 선택이다. 순차적으로 증가하므로 클러스터링 인덱스의 페이지 분할이 최소화되고, 삽입이 효율적이다.

```sql
CREATE TABLE orders (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    status VARCHAR(20) NOT NULL,
    total_amount DECIMAL(14,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

단점은 두 가지다. 첫째, 숫자가 외부에 노출되면 총 주문 수를 추정할 수 있고, 순차적인 ID로 크롤링이 쉬워진다. `/api/orders/1`, `/api/orders/2` 패턴은 인증이 없으면 바로 취약점이 된다. 둘째, 분산 환경(샤딩)에서 여러 인스턴스가 중복 없는 ID를 생성하려면 별도 조율이 필요하다.

### UUID v4 — 분산에는 좋지만 클러스터링이 나빠진다

UUID는 전역적으로 유일하고 외부 예측이 불가능하다.

```sql
CREATE TABLE orders (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    -- 또는 BINARY(16)으로 저장하면 크기를 절반으로 줄임
    ...
);
```

문제는 무작위 값이 PK 클러스터링 인덱스에 들어갈 때다. 새 행이 B+Tree의 임의 위치에 삽입되면서 페이지 분할이 자주 일어난다. 기존 페이지를 반으로 쪼개고 데이터를 재분배하는 과정이 삽입마다 반복될 수 있다. 삽입이 많은 테이블에서는 이 비용이 눈에 띈다. 또한 UUID 문자열이 36바이트라서 세컨더리 인덱스마다 36바이트짜리 포인터가 달린다.

UUID를 써야 한다면 `BINARY(16)`으로 저장해 크기를 줄이는 것과, MySQL 8.0이 지원하는 UUID v1(시간 기반, 단조 증가 성질이 있어 순차 삽입에 가깝다)을 고려해보자. `UUID_TO_BIN(UUID(), 1)` — 두 번째 인수 `1`은 타임스탬프 바이트를 앞으로 이동시켜 순차 삽입 최적화를 한다.

```sql
CREATE TABLE orders (
    id BINARY(16) NOT NULL DEFAULT (UUID_TO_BIN(UUID(), 1)),
    PRIMARY KEY (id)
);

-- 조회 시 UUID 문자열로 변환
SELECT BIN_TO_UUID(id, 1) AS id_str, * FROM orders WHERE id = UUID_TO_BIN('...', 1);
```

### Snowflake 스타일 — 순차 + 분산

트위터가 만든 Snowflake ID는 타임스탬프 + 워커 ID + 시퀀스를 조합한 64비트 정수다. 시간 순으로 증가하므로 클러스터링 인덱스에 유리하고, 워커 ID로 여러 노드가 충돌 없이 ID를 생성할 수 있다. 분산 환경에서 auto_increment의 한계를 넘으면서도 B+Tree 효율을 유지하는 방법이다.

Java 생태계에서는 Twitter Snowflake와 호환되는 라이브러리가 여럿 있고, Spring Boot 프로젝트에서 ID 생성기로 쓸 수 있다.

```java
// Snowflake ID 생성 예시 (개념 코드)
@Component
public class SnowflakeIdGenerator {
    private final long workerId;
    private long sequence = 0;
    private long lastTimestamp = -1;

    // 41비트 타임스탬프 + 10비트 워커 ID + 12비트 시퀀스
    // 실제 구현은 라이브러리를 활용하는 편이 낫다
}
```

**PK 선택 기준 요약:**
- 단일 DB, 노출 무방 → auto_increment BIGINT
- 외부 노출 금지, 단일 DB → auto_increment + 외부 식별자 별도 (UUID or opaque token)
- 분산 DB, 클러스터링 효율 필요 → Snowflake
- 진정한 글로벌 분산 + 충돌 불가 → UUID v4 (클러스터링 비용 감수)

## Soft Delete 논쟁 — brandur vs Brent Ozar

주문이 취소됐다. 데이터를 어떻게 처리해야 할까? 행을 그냥 DELETE하면 간단하지만 이력이 사라진다. 그래서 많은 팀이 `deleted_at DATETIME NULL` 컬럼을 두고, 삭제할 때 실제로 지우지 않고 `deleted_at = NOW()`로 표시하는 방식을 택한다. 이것이 소프트 딜리트(soft delete)다.

개념은 명쾌한데 구현이 번거롭다. brandur.org는 소프트 딜리트가 "거의 가치 없다"고 단호하게 주장한다. 이유는 명확하다.

첫째, `WHERE deleted_at IS NULL`을 모든 쿼리에 끼워야 한다. 하나라도 빠지면 삭제된 데이터가 조회에 노출된다. 10개 테이블이 있으면 10개 테이블의 모든 쿼리에 이 조건이 들어가야 한다. JPA에서는 `@Where(clause = "deleted_at IS NULL")` 애노테이션으로 자동 적용할 수 있지만, native SQL이나 보고서 쿼리에는 직접 붙여야 한다.

둘째, UNIQUE 제약이 망가진다. MySQL에는 partial unique index가 없다. `email` 컬럼에 UNIQUE 제약을 걸었는데 같은 이메일이 soft delete 됐다가 다시 가입하면 중복 오류가 난다.

```sql
-- 이것은 MySQL에서 지원 안 됨 (partial unique index)
CREATE UNIQUE INDEX idx_email_active
ON users (email) WHERE deleted_at IS NULL;

-- 우회책: 함수 기반 인덱스 (MySQL 8.0.13+)
-- deleted_at이 NULL이면 email, NULL이 아니면 NULL을 인덱싱
CREATE UNIQUE INDEX idx_email_not_deleted
ON users ((CASE WHEN deleted_at IS NULL THEN email ELSE NULL END));
```

셋째, FK 관계가 복잡해진다. orders가 user를 참조하는데 user가 soft delete됐다면, orders는 존재하지 않는 user를 가리킨다. FK 제약은 통과하지만 논리적으로 이상한 상태다.

반면 Brent Ozar는 "감사(audit)나 복원이 필요한 도메인에서는 소프트 딜리트가 유효하다"는 입장이다. 금융 거래, 의료 기록 같은 데이터는 법적으로 보관 의무가 있고, 실수로 삭제한 데이터를 복원해야 하는 경우도 있다.

**절충점은 이렇다.** 소프트 딜리트의 이유가 "이력 보관"이라면, 차라리 이력 테이블을 별도로 두는 편이 낫다.

```sql
-- 실제 삭제 + 이력 테이블 패턴
CREATE TABLE orders_history (
    id              BIGINT UNSIGNED NOT NULL,
    user_id         BIGINT UNSIGNED,
    status          VARCHAR(20),
    total_amount    DECIMAL(14,2),
    created_at      DATETIME,
    deleted_at      DATETIME NOT NULL,
    deleted_by      BIGINT UNSIGNED,       -- 누가 삭제했는지
    deletion_reason VARCHAR(500),
    PRIMARY KEY (id, deleted_at)
);

-- 삭제 전 이력으로 복사 후 실제 삭제하는 트리거 또는 서비스 레이어
```

이렇게 하면 `orders` 테이블의 모든 쿼리는 `WHERE deleted_at IS NULL` 없이 작성할 수 있고, UNIQUE 제약도 온전히 작동한다. 이력이 필요하면 `orders_history`를 보면 된다.

소프트 딜리트를 유지해야 한다면, 테이블 전체를 소프트 딜리트로 다루기보다 "활성 상태"를 별도 뷰나 파티션으로 분리해 일반 쿼리가 소프트 딜리트 레코드를 자동으로 보지 않게 하는 방법도 고려해볼 만하다.

## 이력 테이블과 audit log

소프트 딜리트 이야기에서 자연스럽게 이어진다. 도메인 이벤트를 어디에, 어떻게 저장할 것인가.

이력 테이블 패턴은 변경이 일어날 때마다 이전 상태를 별도 테이블에 복사해두는 방식이다. 위의 `orders_history` 같은 것이다.

audit log는 더 일반적인 형태로, 엔티티, 변경 유형(INSERT/UPDATE/DELETE), 변경 전/후 값, 변경자, 시각을 기록한다. JPA의 `@EntityListeners(AuditingEntityListener.class)`로 간단한 audit log를 구현할 수 있다.

```java
@Entity
@EntityListeners(AuditingEntityListener.class)
public class Order {
    @Id
    private Long id;

    @CreatedDate
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;

    @CreatedBy
    private Long createdBy;

    @LastModifiedBy
    private Long updatedBy;
}
```

더 세밀한 필드 수준의 변경 이력이 필요하다면 Envers(Hibernate Audit)를 쓰면 된다. Envers는 엔티티 변경마다 자동으로 revision 테이블에 이전 상태를 기록한다.

DDD 관점에서는 도메인 이벤트를 이벤트 소싱 패턴으로 저장하는 방법도 있다. `OrderCreated`, `OrderCancelled` 같은 이벤트를 직렬화해 이벤트 저장소에 쌓는 것이다. 이 방향은 이 책의 범위를 벗어나지만, 이력 보관이 핵심 요구사항이라면 탐색해볼 만하다.

## 캐릭터셋과 콜레이션 — utf8mb4_0900_ai_ci와 NO PAD

작은 것처럼 보이지만 나중에 큰 문제가 되는 부분이다. MySQL 5.7에서 8.0으로 마이그레이션할 때 특히 주의하자.

MySQL의 `utf8`은 실제로 최대 3바이트 UTF-8이었다. 이모지 같은 4바이트 문자(보충 문자, supplementary characters)를 저장하지 못한다. `utf8mb4`가 진짜 UTF-8이고, 이 차이 때문에 이모지를 저장하려다 `Incorrect string value` 오류를 본 팀이 많다. 8.0 이후 신규 테이블은 `utf8mb4`를 쓰는 편이 낫다.

콜레이션(collation)은 문자열 비교와 정렬 방식을 결정한다. 8.0의 기본 콜레이션은 `utf8mb4_0900_ai_ci`다. `ai`는 Accent-Insensitive(악센트 무시), `ci`는 Case-Insensitive(대소문자 무시)를 의미한다. `café`와 `cafe`가 같은 값으로 비교된다.

5.7에서 마이그레이션할 때 한 가지 짚고 가자. 8.0의 `utf8mb4_0900_ai_ci`는 NO PAD 동작을 한다. 5.7의 `utf8mb4_unicode_ci`는 PAD SPACE 동작이다. 이 차이는 문자열 끝의 공백 처리에서 나타난다.

```sql
-- PAD SPACE 방식 (5.7 기본): 'a' = 'a ' → TRUE (공백 채워서 같다고 봄)
-- NO PAD 방식 (8.0 기본): 'a' = 'a ' → FALSE (공백도 의미 있음)

-- 5.7에서 이 쿼리는 아무것도 반환하지 않았는데
-- 8.0에서는 반환할 수 있다 (또는 반대)
SELECT * FROM users WHERE username = 'admin ';  -- 끝에 공백 있음
```

마이그레이션 시 `SHOW CREATE TABLE`로 각 테이블의 캐릭터셋과 콜레이션을 확인하고, 의도치 않은 동작 변화가 없는지 주요 쿼리를 검토해두는 편이 낫다. 5.7 호환성이 필요한 컬럼은 명시적으로 `CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`로 지정해두면 된다.

```sql
-- 8.0에서 5.7 콜레이션을 명시적으로 쓰는 경우
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50)
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_unicode_ci  -- PAD SPACE 방식, 5.7 호환
        NOT NULL,
    email VARCHAR(200)
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_0900_ai_ci  -- NO PAD 방식, 8.0 기본
        NOT NULL
);
```

## FK를 어디까지 둘 것인가 — 8.4 변화의 무게

외래 키(Foreign Key, FK) 제약은 데이터 정합성을 DB 레벨에서 강제한다. `orders.user_id`가 존재하지 않는 user를 가리키는 상황을 막아준다.

그렇다면 항상 FK를 걸어야 할까? 팀마다 입장이 갈린다.

**FK를 적극 사용하는 입장:**
- DB 레벨에서 정합성 보장 — 애플리케이션 버그로 고립된(orphan) 데이터가 생기지 않는다
- 관계를 명시해 스키마 자체가 문서 역할을 한다
- ON DELETE CASCADE, ON UPDATE CASCADE로 연쇄 처리를 자동화할 수 있다

**FK를 줄이거나 없애는 입장:**
- 마이크로서비스 환경에서 다른 서비스의 테이블을 참조하는 FK는 만들 수 없다
- 대용량 데이터 마이그레이션이나 배치 INSERT에서 FK 체크가 성능 부담이 된다
- 샤딩 환경에서는 다른 샤드의 데이터를 참조하는 FK가 불가능하다

MySQL 8.4에서 FK 관련 동작이 더 엄격해졌다. 8.4에서는 FK 제약이 부모 테이블의 정확히 일치하는 UNIQUE KEY를 요구한다. 이전에는 UNIQUE INDEX면 됐는데 이제는 UNIQUE KEY 제약이어야 한다. Skeema가 "Five Surprises"에서 이 변화를 강조한 이유다.

```sql
-- 8.4에서 이런 상황은 FK 생성 실패
CREATE TABLE categories (
    id INT,
    name VARCHAR(100)
);
CREATE UNIQUE INDEX idx_id ON categories (id);  -- UNIQUE INDEX, KEY 제약 아님

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories (id)  -- 8.4에서 오류 가능
);

-- 대신 UNIQUE KEY 제약으로 명시
ALTER TABLE categories ADD UNIQUE KEY uq_id (id);
-- 또는 PK를 명시
ALTER TABLE categories ADD PRIMARY KEY (id);
```

실무적인 접근법은 이렇다. 같은 DB, 같은 스키마 안의 테이블 관계에는 FK를 둔다. 정합성이 중요하고 성능 비용이 수용 가능한 범위다. 마이크로서비스 경계를 넘는 참조나 샤딩된 데이터 사이의 참조에는 FK를 두지 않고 애플리케이션 레이어에서 정합성을 관리하자.

FK를 안 두기로 했다면, 적어도 외래 키 역할을 하는 컬럼에는 인덱스를 명시적으로 만들어두는 편이 낫다. FK가 있으면 MySQL이 자동으로 인덱스를 만들어주지만, FK가 없으면 만들어주지 않는다. `orders.user_id`에 인덱스가 없으면 user를 삭제할 때 (또는 `WHERE user_id = ?` 조건 쿼리에서) 풀스캔이 일어난다.

## 마무리

도메인 모델과 스키마는 서로를 압박한다. 애그리거트 경계를 테이블로 표현하면서 InnoDB의 클러스터링 특성을 활용하면 조회 성능을 얻을 수 있다. PK 전략은 삽입 패턴, 외부 노출 여부, 분산 환경 여부를 고려해 선택한다. Soft delete는 편리해 보이지만 전체 쿼리에 미치는 부담을 따져봐야 하고, 이력 보관이 목적이라면 이력 테이블이 더 명료한 선택일 때가 많다. 캐릭터셋과 콜레이션은 마이그레이션 시 조용히 문제를 일으키므로 변경 사항을 꼭 확인하자.

9장에서는 JPA와 MySQL이 실제로 맞붙는 지점을 본다. N+1 문제, 페이지네이션 함정, 영속성 컨텍스트의 메모리 문제 — JPA가 만들어주는 편안함 뒤에 있는 MySQL과의 간극을 함께 들여다보자.

## 참고 자료

- Baeldung — DDD aggregates and @DomainEvents — https://www.baeldung.com/spring-data-ddd
- brandur.org — Soft Deletion Probably Isn't Worth It — https://brandur.org/soft-deletion
- Brent Ozar — What Are Soft Deletes — https://www.brentozar.com/archive/2020/02/what-are-soft-deletes-and-how-are-they-implemented/
- Cultured Systems — Avoiding the soft delete anti-pattern — https://www.cultured.systems/2024/04/24/Soft-delete/
- Skeema — Five Surprises in MySQL 8.4 LTS — https://www.skeema.io/blog/2024/05/14/mysql84-surprises/
- CodeRed — Guide to MySQL Charsets & Collations — https://www.coderedcorp.com/blog/guide-to-mysql-charsets-collations/
- MySQL :: Migrating from older collations — https://dev.mysql.com/blog-archive/mysql-8-0-collations-migrating-from-older-collations/
