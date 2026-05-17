# 13장. 통합 사례 — 결제 시스템 한 건을 끝까지 분해해 보자

"이론은 알겠는데, 실제로는 어떻게 짜야 하죠?"

책을 읽으면서 이 질문을 한 번쯤 했을 것이다. 인덱스 설계는 4장에서 배웠고, 락 패턴은 10장에서, 복제는 11장에서, 관측과 백업은 12장에서. 그런데 이 조각들이 실제 서비스에서 어떻게 맞물려 돌아가는지는 다른 이야기다.

이 장에서는 가상의 결제 시스템을 처음부터 끝까지 분해한다. 도메인 모델링, 스키마, 인덱스, 트랜잭션 경계, 동시성 처리, 슬로우 쿼리 대응, PITR 복구까지 — 앞 챕터들의 도구들이 한 줄로 연결되는 감각을 느껴보자.

---

## 결제 도메인 — 4개 애그리거트

결제 시스템은 크게 네 개의 애그리거트로 나눌 수 있다.

- **주문(Order)**: 사용자가 무엇을 얼마에 구매하는지
- **결제(Payment)**: 실제 금액 이동, PG와의 인터페이스
- **정산(Settlement)**: 판매자에게 얼마를 언제 정산할지
- **포인트(Point)**: 사용자 포인트 적립/사용

각 애그리거트는 자신의 트랜잭션 경계를 가진다. "주문 하나에 결제·정산·포인트를 한 트랜잭션에서 처리해야 하나요?" — 이 질문을 처음 받으면 당황스럽다. 정답은 없지만 기준은 있다.

DDD 원칙에서 애그리거트 간 트랜잭션은 결과적 일관성(eventual consistency)으로 가는 편이 낫다. 한 트랜잭션이 길어질수록 락이 오래 유지되고, 실패 시 롤백 범위가 커진다.

---

## 도메인 모델링에서 스키마까지

### 스키마 설계

```sql
-- 주문 애그리거트
CREATE TABLE orders (
    id              BIGINT          NOT NULL AUTO_INCREMENT,
    user_id         BIGINT          NOT NULL,
    status          VARCHAR(20)     NOT NULL DEFAULT 'PENDING',
    total_amount    DECIMAL(10, 2)  NOT NULL,
    created_at      DATETIME(6)     NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at      DATETIME(6)     NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
                                    ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    INDEX idx_user_status (user_id, status),        -- 사용자별 주문 목록
    INDEX idx_created_at (created_at)               -- 날짜 범위 조회
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 주문 상품 (주문 애그리거트 내부)
CREATE TABLE order_items (
    id          BIGINT          NOT NULL AUTO_INCREMENT,
    order_id    BIGINT          NOT NULL,
    product_id  BIGINT          NOT NULL,
    quantity    INT             NOT NULL,
    unit_price  DECIMAL(10, 2)  NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_order_id (order_id),              -- 주문별 상품 조회
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id) REFERENCES orders(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 결제 애그리거트
CREATE TABLE payments (
    id              BIGINT          NOT NULL AUTO_INCREMENT,
    order_id        BIGINT          NOT NULL,
    pg_transaction_id VARCHAR(100)  NULL,           -- PG사 트랜잭션 ID
    status          VARCHAR(20)     NOT NULL DEFAULT 'PENDING',
    amount          DECIMAL(10, 2)  NOT NULL,
    method          VARCHAR(20)     NOT NULL,        -- CARD, TRANSFER, POINT
    paid_at         DATETIME(6)     NULL,
    created_at      DATETIME(6)     NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE INDEX idx_pg_transaction_id (pg_transaction_id),  -- PG 트랜잭션 중복 방지
    INDEX idx_order_id (order_id),
    INDEX idx_status_created (status, created_at)   -- 상태별 정산 대상 조회
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 정산 애그리거트
CREATE TABLE settlements (
    id              BIGINT          NOT NULL AUTO_INCREMENT,
    seller_id       BIGINT          NOT NULL,
    payment_id      BIGINT          NOT NULL,
    amount          DECIMAL(10, 2)  NOT NULL,
    status          VARCHAR(20)     NOT NULL DEFAULT 'PENDING',
    settled_at      DATE            NULL,
    created_at      DATETIME(6)     NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    INDEX idx_seller_status (seller_id, status, settled_at),
    INDEX idx_payment_id (payment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 포인트 원장
CREATE TABLE point_ledger (
    id          BIGINT          NOT NULL AUTO_INCREMENT,
    user_id     BIGINT          NOT NULL,
    amount      DECIMAL(10, 2)  NOT NULL,            -- 양수: 적립, 음수: 사용
    type        VARCHAR(20)     NOT NULL,             -- EARN, USE, EXPIRE
    ref_id      BIGINT          NOT NULL,             -- 참조 ID (order_id 등)
    ref_type    VARCHAR(20)     NOT NULL,             -- 참조 유형
    created_at  DATETIME(6)     NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    INDEX idx_user_created (user_id, created_at)     -- 사용자 포인트 이력
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

포인트 잔액을 별도 `user_points` 테이블에 두고 싶은 충동이 생긴다. 빠르게 현재 잔액을 알 수 있으니. 하지만 원장(ledger) 패턴이 더 안전하다. 각 거래를 append-only로 기록하고, 잔액은 sum으로 계산한다. 원장이 있으면 어느 시점의 잔액이든 재계산할 수 있고, 감사 추적도 된다.

> **다른 도메인으로 옮긴다면** — 이커머스 재고 도메인에서는 `stock_ledger`로 같은 패턴을 쓸 수 있다. 입고(+), 출고(-), 취소(+) 이벤트를 append-only로 쌓으면 재고 이력 추적과 시점별 재고 계산이 모두 된다. 단, 재고 조회 빈도가 매우 높다면 materialized view나 별도 `current_stock` 테이블로 최신 값을 캐싱하는 것을 고려해야 한다.

---

## 동시성 시나리오 — 같은 상품 결제 폭주

인기 상품 한정 판매 이벤트를 상상해보자. 1,000명이 동시에 같은 상품을 결제하려 한다. 재고는 100개. 이 상황에서 어떤 락 전략을 써야 할까?

충돌이 매우 빈번하다. 낙관적 락이라면 `@Retryable`과 결합하더라도 900건이 실패를 경험하고 재시도한다. 이 와중에 DB에 불필요한 부하가 집중된다.

비관적 락이 맞는 선택이다. 하지만 단순히 `@Lock(PESSIMISTIC_WRITE)`로 상품을 잠그면, 1,000개의 커넥션이 그 락을 기다리며 커넥션 풀을 잡는다. 그 상황이 얼마나 번거로운지 상상해보자.

Named lock이 적절하다. 락을 비즈니스 커넥션 풀과 분리하고, 락을 얻은 요청만 처리하도록 설계한다.

```java
// 결제 처리 서비스: named lock으로 상품별 직렬화
@Service
@RequiredArgsConstructor
public class PaymentProcessingService {

    private final MysqlNamedLockManager lockManager;
    private final ProductRepository productRepository;
    private final OrderRepository orderRepository;
    private final PaymentRepository paymentRepository;

    public PaymentResult processPayment(PaymentCommand command) {
        String lockName = "payment:product:" + command.getProductId();

        return lockManager.executeWithLock(lockName, 5, () -> {
            // 락 안에서: 재고 확인 → 차감 → 주문 생성 → 결제 생성
            return doProcessPayment(command);
        });
    }

    @Transactional
    protected PaymentResult doProcessPayment(PaymentCommand command) {
        // 재고 확인 및 차감 (락 안에서 안전)
        Product product = productRepository.findByIdWithLock(command.getProductId())
            .orElseThrow();

        if (product.getStockQuantity() < command.getQuantity()) {
            throw new InsufficientStockException("재고가 부족합니다.");
        }
        product.decreaseStock(command.getQuantity());

        // 주문 생성
        Order order = Order.create(command.getUserId(), product, command.getQuantity());
        orderRepository.save(order);

        // 결제 레코드 생성 (PG 호출은 트랜잭션 밖에서)
        Payment payment = Payment.pending(order, command);
        paymentRepository.save(payment);

        return PaymentResult.of(order, payment);
    }
}
```

named lock 안에서 `@Transactional` 메서드를 호출한다. 락이 있으니 같은 상품에 대한 동시 결제 요청은 직렬화된다. 각 요청은 재고를 정확히 확인하고 차감한다.

PG API 호출은 이 코드에 없다. 결제 레코드는 `PENDING` 상태로 만들고, 실제 PG 호출은 별도의 단계에서 트랜잭션 밖에서 처리한다. 10장에서 배운 외부 IO를 트랜잭션 밖으로 패턴이다.

> **다른 도메인으로 옮긴다면** — SaaS 멀티테넌시에서 테넌트별 리소스 한도 초과를 막아야 할 때도 같은 패턴이 쓰인다. `"quota:tenant:{tenantId}"` named lock으로 동시 요청을 직렬화하고, 현재 사용량을 확인한 뒤 한도 내에서만 처리한다. 테넌트 수가 많을수록 락 이름이 세분화되어 락 경합이 줄어든다.

---

## 보고서 — 일별 정산 쿼리

매일 밤 정산 배치가 돌아간다. 판매자별로 당일 결제된 금액을 집계하고, 수수료를 계산해 정산 레코드를 만든다.

```sql
-- 일별 판매자 정산 집계 (윈도우 함수 + CTE)
WITH daily_payments AS (
    -- 오늘 완료된 결제
    SELECT
        s.seller_id,
        p.id AS payment_id,
        p.amount,
        p.paid_at
    FROM payments p
    JOIN settlements s ON s.payment_id = p.id
    WHERE p.status = 'COMPLETED'
      AND DATE(p.paid_at) = CURDATE()
),
seller_daily_summary AS (
    -- 판매자별 일별 집계
    SELECT
        seller_id,
        SUM(amount)                        AS total_amount,
        COUNT(*)                           AS payment_count,
        SUM(amount) * 0.032                AS commission,    -- 수수료 3.2%
        SUM(amount) * (1 - 0.032)          AS net_amount
    FROM daily_payments
    GROUP BY seller_id
),
seller_cumulative AS (
    -- 이번 달 누적 (윈도우 함수)
    SELECT
        s2.seller_id,
        s2.net_amount AS today_net,
        SUM(s2.net_amount) OVER (
            PARTITION BY s2.seller_id
            ORDER BY DATE(s2.created_at)
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS monthly_cumulative
    FROM settlements s2
    WHERE MONTH(s2.created_at) = MONTH(CURDATE())
      AND s2.status = 'COMPLETED'
)
SELECT
    ds.seller_id,
    ds.total_amount,
    ds.payment_count,
    ds.commission,
    ds.net_amount,
    sc.monthly_cumulative
FROM seller_daily_summary ds
LEFT JOIN seller_cumulative sc ON sc.seller_id = ds.seller_id
ORDER BY ds.net_amount DESC;
```

이 쿼리가 EXPLAIN ANALYZE에서 어떻게 실행되는지 확인해보자. `settlements.seller_id + status + created_at` 복합 인덱스가 없다면 `seller_cumulative` CTE의 집계가 풀스캔을 한다. 6장의 윈도우 함수 패턴과 5장의 EXPLAIN ANALYZE를 함께 적용하는 순간이다.

```sql
-- 정산 집계 쿼리의 실행 계획 확인
EXPLAIN ANALYZE
WITH daily_payments AS (
    SELECT s.seller_id, p.amount
    FROM payments p
    JOIN settlements s ON s.payment_id = p.id
    WHERE p.status = 'COMPLETED'
      AND DATE(p.paid_at) = CURDATE()
)
SELECT seller_id, SUM(amount)
FROM daily_payments
GROUP BY seller_id;
-- actual rows와 estimated rows 괴리가 크면 ANALYZE TABLE 재실행
```

> **다른 도메인으로 옮긴다면** — B2B 대용량 배치에서는 이런 집계를 야간 배치로 처리한다. Spring Batch의 `JdbcCursorItemReader`로 대량 데이터를 청크 단위로 읽고, `JdbcBatchItemWriter`로 집계 결과를 쓰는 구조다. 청크 사이즈(예: 500~1,000)와 커밋 간격을 조율해 메모리 사용량과 락 유지 시간을 균형 있게 설정한다.

---

## 운영 시나리오 — 슬로우 쿼리 알람에서 인덱스 추가까지

월요일 아침 9시. 슬로우 쿼리 알람이 뜬다. 정산 조회 API의 p99 응답시간이 12초다.

`pt-query-digest`를 돌려보니 문제 쿼리가 잡힌다.

```sql
-- 문제 쿼리: 판매자 정산 목록 조회
SELECT s.*, p.amount, p.paid_at
FROM settlements s
JOIN payments p ON p.id = s.payment_id
WHERE s.seller_id = 1234
  AND s.status = 'PENDING'
ORDER BY s.created_at DESC
LIMIT 20;
```

`EXPLAIN ANALYZE`로 확인해보자.

```sql
EXPLAIN ANALYZE
SELECT s.*, p.amount, p.paid_at
FROM settlements s
JOIN payments p ON p.id = s.payment_id
WHERE s.seller_id = 1234
  AND s.status = 'PENDING'
ORDER BY s.created_at DESC
LIMIT 20;

-- 출력 예시:
-- -> Limit: 20 row(s)  (actual time=8234.5..8234.5 rows=20 loops=1)
--   -> Sort: settlements.created_at DESC  (actual rows=45000 loops=1)
--     -> Filter: (s.status = 'PENDING')  (actual rows=45000 loops=1)
--       -> Index scan on settlements using idx_seller_id
--                 (actual rows=89000 loops=1)
```

안쪽 노드부터 읽어보자. `idx_seller_id`를 써서 seller_id=1234인 행 89,000개를 읽고, status='PENDING'으로 필터링해 45,000개가 남고, 전부 정렬한 다음 20개를 돌려준다. 8초가 걸린 이유가 보인다.

복합 인덱스 `(seller_id, status, created_at)`을 추가하면 세 조건이 모두 인덱스에서 처리된다.

```sql
-- Invisible index로 먼저 테스트 (운영 영향 없이)
ALTER TABLE settlements
ADD INDEX idx_seller_status_created (seller_id, status, created_at) INVISIBLE;

-- 세션에서 invisible index 강제 사용
SET SESSION optimizer_switch = 'use_invisible_indexes=on';

EXPLAIN ANALYZE
SELECT s.*, p.amount, p.paid_at
FROM settlements s
JOIN payments p ON p.id = s.payment_id
WHERE s.seller_id = 1234
  AND s.status = 'PENDING'
ORDER BY s.created_at DESC
LIMIT 20;
-- 실행 시간이 얼마나 줄었는지 확인

-- 효과 확인 후 visible로 전환
ALTER TABLE settlements
ALTER INDEX idx_seller_status_created VISIBLE;
```

Invisible index로 실제 운영 쿼리에 영향 없이 새 인덱스의 효과를 확인하고, 그 다음 visible로 전환하는 4장의 패턴이 여기서 빛난다.

그런데 한 가지 더 확인할 게 있다. 새 인덱스를 추가하면 기존 `idx_seller_id` 단순 인덱스가 필요 없어질 수 있다. 사용되지 않는 인덱스는 INSERT/UPDATE 부하만 늘린다.

```sql
-- 인덱스 사용 통계 확인
SELECT INDEX_NAME, COUNT_READ, COUNT_WRITE
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE OBJECT_SCHEMA = 'mydb' AND OBJECT_NAME = 'settlements'
ORDER BY COUNT_READ DESC;
-- COUNT_READ가 0이거나 매우 낮은 인덱스는 Invisible로 비활성화 후 제거 검토
```

> **다른 도메인으로 옮긴다면** — 이커머스 재고 도메인에서 창고별·카테고리별 재고 조회가 느릴 때도 같은 절차를 따른다. EXPLAIN ANALYZE로 병목 노드를 찾고, 복합 인덱스 설계로 해결하고, Invisible index로 검증 후 적용한다.

---

## 월요일 새벽 백업 검증 실패 → PITR 리허설

밤새 자동으로 돌아야 할 PITR 리허설 배치가 슬랙에 실패 알림을 남겼다. "스냅샷 복원 완료됐는데 binlog 적용 중 오류."

실제 장애가 아니라 다행이지만, 이 신호를 무시하면 진짜 장애 때 망연자실하게 된다.

```bash
# 원인 파악: binlog 연속성 확인
mysqlbinlog --verbose /var/lib/mysql/binlog.000789 | head -50
# ERROR: Could not read entry at offset 4:
#   Error in log format or read error.
# -> binlog 파일 손상

# Aurora RDS라면: binlog 연속성을 AWS가 관리
# 자체 관리 MySQL이라면: binlog 보존 정책 확인
SHOW VARIABLES LIKE 'binlog_expire_logs_seconds';
-- binlog_expire_logs_seconds: 86400 (1일)
-- 너무 짧으면 PITR 윈도우가 1일로 제한됨

-- 더 긴 보존 기간으로 변경
SET GLOBAL binlog_expire_logs_seconds = 604800; -- 7일
```

이 경우 binlog 만료 기간이 너무 짧아 연속성이 끊겼다. 리허설에서 발견했으니 다행이다. 다음 분기 리허설 전에 만료 기간을 7일로 늘리고 binlog가 정상적으로 누적되는지 재확인한다.

Aurora RDS라면 자동 백업 보존 기간이 7~35일 범위에서 설정된다. "1일로 설정돼 있는데 아무도 몰랐다"는 일이 생각보다 흔하다. 설정을 한 번은 직접 확인해보자.

```bash
# AWS CLI로 자동 백업 보존 기간 확인
aws rds describe-db-instances \
  --db-instance-identifier mydb-prod \
  --query 'DBInstances[0].BackupRetentionPeriod'
# 1 이면 너무 짧다

# 7일로 변경
aws rds modify-db-instance \
  --db-instance-identifier mydb-prod \
  --backup-retention-period 7 \
  --apply-immediately
```

> **다른 도메인으로 옮긴다면** — SaaS 멀티테넌시에서는 테넌트별 데이터 복구 요청이 올 수 있다. "3시간 전 상태로 돌려주세요"가 특정 테넌트의 데이터만 의미할 때, 전체 PITR이 아니라 테넌트 파티션만 복구하는 방법이 필요하다. 이때 논리 파티셔닝(테넌트 ID 기반 테이블 분리)이나 binlog 이벤트를 테넌트 기준으로 필터링하는 도구를 검토해야 한다.

---

## 인프라 — Aurora 클러스터 설계

결제 시스템의 인프라 구성을 한 줄씩 따져보자.

**Aurora 클러스터 선택**. 결제 서비스는 페일오버 RTO에 민감하다. 수십 초 장애도 결제 실패로 이어질 수 있다. Aurora의 15~30초 페일오버가 RDS의 60~120초보다 낫다. 읽기 트래픽도 높으니 리플리카를 적극 활용할 수 있는 Aurora가 맞는 선택이다.

**읽기 리플리카 분산**. Writer는 주문 생성·결제 처리·포인트 차감 등 쓰기 중심으로, Reader는 판매자 정산 조회·사용자 주문 이력 조회로 분산한다.

```java
// Spring Boot에서 읽기/쓰기 DB 라우팅
@Configuration
public class DataSourceConfig {

    @Primary
    @Bean("writerDataSource")
    @ConfigurationProperties(prefix = "spring.datasource.writer")
    public DataSource writerDataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean("readerDataSource")
    @ConfigurationProperties(prefix = "spring.datasource.reader")
    public DataSource readerDataSource() {
        return DataSourceBuilder.create().build();
    }
}

// 읽기 전용 트랜잭션은 리플리카로
@Service
public class SettlementQueryService {

    @Transactional(readOnly = true)  // readOnly=true → Reader 라우팅
    public List<SettlementDto> findBySellerAndDate(Long sellerId, LocalDate date) {
        // ...
    }
}
```

**파티셔닝 정책**. `payments` 테이블은 날짜 기반 RANGE 파티셔닝을 검토해볼 수 있다. 정산은 주로 최근 7~30일 데이터를 조회하므로 오래된 파티션을 아카이빙하거나 읽기 전용으로 전환하는 것이 가능하다.

```sql
-- payments 테이블 RANGE 파티셔닝 (연도 기반)
ALTER TABLE payments
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- 오래된 파티션을 별도 테이블로 분리해 아카이빙
ALTER TABLE payments EXCHANGE PARTITION p2022
WITH TABLE payments_archive_2022;
```

**페일오버 RTO 측정**. Aurora의 페일오버를 실제로 테스트해보는 것이 좋다. AWS는 "장애 주입 테스트" 기능을 제공한다.

```bash
# AWS Fault Injection Simulator로 Aurora 페일오버 테스트
aws fis start-experiment \
  --experiment-template-id <template_id>

# 또는 Aurora 콘솔에서 "Failover" 버튼 클릭
# 페일오버 시작 시간 → 연결 재수립 시간 측정
```

실측한 RTO를 운영팀과 공유하고, SLA에 명시된 목표치와 비교해보자.

---

## 카카오 MRTE식 트래픽 미러링 — 변경 검증

인덱스를 추가하거나 쿼리를 수정하기 전에 실제 운영 트래픽으로 검증하고 싶다면 어떻게 할까?

카카오의 MRTE(MySQL Realtime Traffic Emulator)는 운영 트래픽을 새 환경에 미러링해 실제 동작을 미리 본다. MySQL 업그레이드나 대형 튜닝 전에 "미러 환경에서 운영 트래픽을 한 주 돌려보고 판단"하는 방식이다.

동일한 원칙을 스테이징 환경에서 부분적으로 구현할 수 있다. 프록시 레이어(HAProxy, ProxySQL)에서 읽기 쿼리의 일부를 스테이징 DB로 복제해 실행 계획 차이를 비교한다.

결제 도메인처럼 데이터 정합성이 중요한 시스템에서는 쓰기 트래픽을 미러링하기 어렵지만, 읽기 쿼리 미러링만으로도 인덱스 변경의 효과를 사전 검증하는 데 충분하다.

---

## 마무리 — 도구함을 하나로 연결하는 감각

이 장에서 결제 시스템을 분해하면서 앞 챕터들의 도구들이 어떻게 연결되는지 봤다.

도메인 모델링(8장)이 스키마를 만들고, 인덱스 설계(4장)가 조회 성능을 결정한다. 동시성 처리는 낙관적 락과 named lock(10장)을 워크로드에 맞게 선택하는 문제다. 슬로우 쿼리가 뜨면 EXPLAIN ANALYZE(5장)로 분해하고 Invisible index(4장)로 안전하게 테스트한다.

정산 보고서는 윈도우 함수와 CTE(6장)로 SQL 안에서 처리하는 편이 애플리케이션 코드보다 깔끔하다. 백업 검증 실패 신호는 무시하지 않고, PITR 리허설(12장)로 대응 능력을 유지한다.

각 절의 "다른 도메인으로 옮긴다면" 단락에서 강조하고 싶었던 것은 이것이다. 결제가 아니더라도 같은 원칙이 적용된다. 도메인이 다르면 구체적인 구현은 달라지지만, 애그리거트 경계 → 스키마 → 인덱스 → 동시성 → 운영이라는 사고의 순서는 변하지 않는다.

다음 장에서는 메이저 업그레이드를 다룬다. MySQL 8.0에서 8.4로 넘어갈 때 무엇부터 점검해야 하는지, 다운그레이드 불가의 무게를 어떻게 준비하는지 함께 살펴보자.

---

## 참고 자료

- 우아한형제들 — MySQL을 이용한 분산락: https://techblog.woowahan.com/2631/
- 카카오 — MRTE (MySQL Realtime Traffic Emulator): https://tech.kakao.com/posts/311
- Baeldung — DDD aggregates and @DomainEvents: https://www.baeldung.com/spring-data-ddd
- 토스 SLASH 21 — MYSQL HA & DR Topology: https://toss.im/slash-21/sessions/2-3
- MySQL — Invisible Indexes: https://dev.mysql.com/doc/refman/8.0/en/invisible-indexes.html
- Vlad Mihalcea — Keyset Pagination with JPA and Hibernate: https://vladmihalcea.com/keyset-pagination-jpa-hibernate/
