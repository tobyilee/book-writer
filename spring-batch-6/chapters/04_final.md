# 4장. ItemReader/Processor/Writer 계약 — 그리고 Tasklet의 1할

OKKY를 한참 뒤지다 보면 이런 질문이 정기적으로 등장한다.

> "60만 건 처리하는데 OOM이 납니다. ItemReader가 다 들고 있는 것 같아요. heap을 봐도 row 데이터가 가득 차 있고, GC도 못 돌고, 결국 컨테이너가 죽습니다. 어떻게 해야 할까요?"

질문을 자세히 읽어보면 패턴이 보인다. 대부분의 OOM 케이스는 결국 이 장에서 다루는 내용 중 하나에 걸려 있다. Reader가 한 번에 다 들고 있거나, chunk size·page size·fetch size를 헷갈렸거나, Cursor와 Paging을 잘못 골랐거나, JpaItemWriter Dirty Checking이 메모리를 잡고 있거나. 한 번 알면 안 걸리는 함정인데, 모르면 새벽에 한 시간씩 추적하다가 끝난다.

3장에서 첫 잡을 띄우고 `@StepScope` 함정도 통과했다. 이제 모델의 안쪽을 더 깊이 들여다보자. **ItemReader/Processor/Writer 계약은 정확히 어떻게 되어 있고, 어떤 결정 트리로 골라야 하는가?** 그리고 청크 모델이 어색해지는 일은 어떻게 다루는가? 이 두 질문에 답하는 것이 이 장의 목표다.

## 한 번 더 — 청크 = 트랜잭션

본격적으로 들어가기 전에 한 줄을 박아두자. 이 장 전체를 관통하는 핵심 규칙이다.

**청크는 트랜잭션이다. 그리고 트랜잭션은 청크다.**

이 한 줄이 모든 것의 출발이다. Reader 결정도, Writer 결정도, chunk size 튜닝도, 멱등성 설계도, fault tolerance도 — 모두 "청크 = 트랜잭션"에서 파생된다. 잊지 말자.

## read() / process() / write() — 계약 한 줄씩 풀기

세 메서드의 시그니처와 의미를 다시 한 줄씩 적어보자. 비슷해 보이지만 미묘하게 다른 점이 있다.

```java
// ItemReader
T read() throws Exception;

// ItemProcessor
O process(I item) throws Exception;

// ItemWriter
void write(Chunk<? extends T> chunk) throws Exception;
```

각각의 계약을 풀어 쓰면 이렇다.

- **`read()`의 `null` 반환은 입력 종료를 뜻한다.** Spring Batch는 `read()`가 `null`을 리턴하는 순간 "더 읽을 게 없다"고 판단하고 Step을 종료한다. 그러니 비어 있는 결과를 `null`로 표시하면 안 된다. 그건 다른 의미가 된다. Reader는 stateful해도 된다 — 어디까지 읽었는지 자기 안에 들고 있다가 다음 호출에서 그 다음 항목을 내준다.
- **`process(item)`의 `null` 반환은 필터링을 뜻한다.** 즉 "이 항목은 Writer로 보내지 않는다"는 의미다. skip이 아니다. skip은 "예외가 났는데 그 항목을 건너뛴다"는 뜻이고, 필터링은 "정상 흐름인데 이 항목은 처리 대상이 아니다"라는 뜻이다. 이 둘을 헷갈리면 메트릭이 이상해진다 — `read_count`와 `write_count`의 차이가 필터링 건수다.
- **`write(chunk)`는 한 청크 전체를 한 번에 받는다.** 그리고 이 호출은 트랜잭션 1건당 한 번이다. 청크 사이즈 100이면 Writer는 100건짜리 리스트를 한 번에 받고, 그 한 번의 호출 안에서 일괄 처리해야 한다. Writer 안에서 한 건씩 루프 돌리면서 INSERT를 N번 호출하면 청크의 의미가 사라진다.

이 세 계약을 정확히 알면 OOM의 절반은 안 만난다. 예를 들어 직접 작성한 Reader가 `read()` 안에서 List를 통째로 들고 한 건씩 내주면, 그 List가 메모리에 그대로 잡혀 있다. 60만 건이면 60만 건이 다 메모리에 있다. 이게 전형적인 OOM 패턴이다. 한 건씩 페이지·커서로 가져오면서 처리할 때만 메모리가 작게 유지된다.

## chunk size, page size, fetch size — 셋이 다른 개념이다

이름이 비슷해서 가장 자주 헷갈리는 셋이다. 한 번에 그림으로 정리해 두자.

```
┌──────────────────────────────────────────────────────────┐
│  청크 (트랜잭션 1건)                                       │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐         │
│  │ 1  │ │ 2  │ │ 3  │ │... │ │ 99 │ │100 │  ← chunk size  │
│  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘                │
│         100건이 모이면 Writer 1번 호출 + COMMIT            │
└──────────────────────────────────────────────────────────┘

Reader가 데이터베이스에서 읽는 방식:

  Paging Reader 기준:
    한 페이지에 page size만큼 (예: 100건)
    Reader가 한 페이지를 다 소진하면 다음 페이지 SELECT
    
  JDBC fetch size:
    SELECT 결과를 클라이언트로 가져올 때
    한 번의 네트워크 라운드트립에 fetch size만큼 (예: 1,000건)
    드라이버 버퍼에 쌓아두고 ResultSet에서 한 건씩 꺼냄
```

세 개념이 어떻게 다른지 한 줄씩 다시 적자.

- **chunk size:** Spring Batch의 트랜잭션 1건당 처리할 항목 수. **Step의 결정**이다.
- **page size:** Paging Reader가 한 페이지에 가져올 행 수. **Reader의 결정**이다.
- **fetch size:** JDBC 드라이버가 네트워크 라운드트립 1회당 가져올 행 수. **JDBC의 결정**이다.

세 개념이 작동하는 레이어가 다른 게 핵심이다. chunk size는 Spring Batch가 다루고, page size는 Reader 안에서 다루고, fetch size는 JDBC 드라이버가 다룬다.

권장 시작값을 적자면 이렇다.

- `chunk size = page size`로 맞추는 것이 표준이다. 다르게 두면 페이지를 걸친 청크가 생기면서 페이지 fetch 횟수가 늘어 비효율이 된다.
- `fetch size ≥ chunk size`로 두는 것이 좋다. 가능하면 더 크게(예: chunk 500이면 fetch 1,000). 라운드트립을 줄여준다.
- 시작값으로는 chunk = page = 500~1,000, fetch = 1,000이 흔하다. 단, **production 데이터로 반드시 측정**한다. 무엇이 가장 빠른지는 데이터 분포와 DB 상황에 따라 다르다.

청크 사이즈를 무작정 키우는 것이 답이 아니라는 것도 짚자. 청크가 커지면 한 트랜잭션이 길어지고, 트랜잭션 로그가 커지고, 실패 시 롤백 비용이 커진다. 그리고 한 청크가 다 끝날 때까지 메모리에 청크 전체를 쥐고 있어야 한다. 청크 크기는 **트랜잭션 길이 + 메모리 + 실패 비용**의 트레이드오프다. 이 감각은 12장에서 다시 회고로 돌아온다.

## Cursor vs Paging — 두 가지 Reader 패러다임

RDB에서 데이터를 읽는 Reader는 두 가지 패러다임이 있다. 둘의 차이를 모르면 OOM이나 락 타임아웃을 만든다.

### Cursor Reader

`JdbcCursorItemReader`가 대표다. 한 번 SELECT를 실행하고, **DB 커서를 열어둔 채로** 결과를 한 건씩 fetch해서 내준다. 트랜잭션 하나 안에서 끝까지 읽는 모델이다.

```java
@Bean
@StepScope
public JdbcCursorItemReader<Payment> cursorReader(
        @Value("#{jobParameters['date']}") String date,
        DataSource dataSource) {
    return new JdbcCursorItemReaderBuilder<Payment>()
            .name("paymentCursorReader")
            .dataSource(dataSource)
            .sql("SELECT id, amount, status FROM payments WHERE created_date = ?")
            .preparedStatementSetter((ps, ctx) -> ps.setString(1, date))
            .rowMapper(new BeanPropertyRowMapper<>(Payment.class))
            .fetchSize(1000)
            .build();
}
```

**장점:** 메모리 효율이 좋다. 드라이버가 fetch size만큼만 버퍼에 두고 한 건씩 흘려 보낸다. 일관성도 강하다 — 한 트랜잭션 안에서 다 읽으므로 다른 세션의 변경이 끼어들지 않는다.

**단점:** 트랜잭션이 길게 유지된다. 100만 건을 한 시간 동안 처리한다면 그 한 시간 내내 DB 커서가 열려 있다. 커넥션 풀이 그만큼 점유된다. 일부 DB 벤더(특히 DB2)는 장시간 커서에 락 이슈를 일으킨다. 그리고 **재시작 친화도가 떨어진다.** 잡이 중간에 죽었다가 다시 시작하면 커서를 어디까지 진행했는지 복원하기가 까다롭다.

### Paging Reader

`JdbcPagingItemReader`가 대표다. 페이지 단위로 SELECT를 반복한다. 한 페이지를 다 읽으면 트랜잭션을 끊고, 다음 페이지를 새 트랜잭션으로 SELECT한다.

```java
@Bean
@StepScope
public JdbcPagingItemReader<Payment> pagingReader(
        @Value("#{jobParameters['date']}") String date,
        DataSource dataSource) {

    Map<String, Order> sortKeys = Map.of("id", Order.ASCENDING);

    MySqlPagingQueryProvider qp = new MySqlPagingQueryProvider();
    qp.setSelectClause("id, amount, status");
    qp.setFromClause("FROM payments");
    qp.setWhereClause("WHERE created_date = :date");
    qp.setSortKeys(sortKeys);

    return new JdbcPagingItemReaderBuilder<Payment>()
            .name("paymentPagingReader")
            .dataSource(dataSource)
            .queryProvider(qp)
            .parameterValues(Map.of("date", date))
            .pageSize(500)
            .rowMapper(new BeanPropertyRowMapper<>(Payment.class))
            .build();
}
```

**장점:** 장시간 트랜잭션이 없다. 페이지마다 트랜잭션이 끊기므로 DB 락이 짧다. 재시작 친화도가 좋다 — 어느 페이지까지 처리했는지가 ExecutionContext에 자동 저장되고, 다시 시작하면 그 다음 페이지부터 읽는다.

**단점:** 페이지 사이에 데이터가 변경되면 일관성이 흐트러질 수 있다. 그리고 **OFFSET/LIMIT 페이징의 비용 폭증** 문제가 있다 — 페이지가 깊어질수록 OFFSET이 커지면서 DB가 그 앞의 N건을 다 스캔해서 버려야 한다. 100만 건 째 페이지를 가져오려면 100만 건을 스캔하고 1,000건만 돌려준다. 이건 끔찍한 일이다.

### 결정 트리

| 상황 | 권장 |
|---|---|
| 작은 데이터(수만~수십만 건), 한 트랜잭션 안에 끝남, 일관성 강력히 필요 | Cursor |
| 큰 데이터(수백만~수억 건), 장시간 트랜잭션 회피, 재시작 가능성 | Paging (단 keyset 권장) |
| 컨테이너 환경(K8s)에서 운영, Pod 재시작 시 이어가야 함 | Paging |
| DB 락 민감, 다른 세션의 변경이 잦은 테이블 | Paging |

**큰 데이터를 다룰 때는 Paging이 사실상 표준이다.** 그리고 OFFSET 비용 폭증을 피하기 위해 **keyset(no-offset) pagination**을 쓰는 것이 권장된다. keyset은 마지막으로 읽은 PK를 기억해두고 다음 페이지를 `WHERE id > :lastId ORDER BY id LIMIT 500`으로 가져오는 방식이다. 페이지가 깊어져도 비용이 일정하다.

한국 커뮤니티에서는 jojoldu(이동욱)의 **`QuerydslNoOffsetPagingItemReader`**가 사실상 표준 라이브러리다. Querydsl과 keyset 페이징을 합친 구현으로, 우아한형제들 기술블로그 "Spring Batch와 Querydsl"에서 시작해 한국 실무 코드에 널리 쓰인다. JPA + Querydsl 환경이라면 이걸 먼저 검토해보는 것이 합리적이다.

## 내장 Reader 라인업

Spring Batch가 기본 제공하는 Reader들을 한 번 정리해두자. 자주 쓰는 순서다.

| Reader | 입력 | 특징 |
|---|---|---|
| `FlatFileItemReader` | 텍스트 파일 (CSV, TSV, 고정폭) | 기본 중의 기본. 라인 단위 매핑 |
| `JdbcPagingItemReader` | RDB | 페이징, 가장 널리 쓰임 |
| `JdbcCursorItemReader` | RDB | 커서, 작은 데이터에 |
| `JpaPagingItemReader` | JPA Entity | JPA 엔티티 매핑이 필요할 때 |
| `MongoItemReader` | MongoDB | NoSQL |
| `JsonItemReader` | JSON 파일 | 한 라인 한 객체 형식 |
| `StaxEventItemReader` | XML 파일 | XML 스트리밍 파싱 |

이 중 RDB Reader가 압도적으로 많이 쓰인다. 실무 잡 10개 중 7~8개는 `JdbcPagingItemReader`나 그 변종(`QuerydslNoOffsetPagingItemReader`)이라고 봐도 무방하다.

## Writer 결정 트리 — JdbcBatchItemWriter는 좋고, JpaItemWriter는 위험하다

Reader 못지않게 Writer도 결정이 중요하다. 그리고 한국 커뮤니티에서 가장 많이 부딪히는 운영 함정이 Writer 쪽에 있다. 카카오페이 정산팀의 성능 개선 사례에서도 가장 큰 변화 중 하나가 Writer 교체였다.

### JdbcBatchItemWriter

JDBC batch update를 사용하는 Writer다. 청크 한 번에 INSERT/UPDATE를 batched로 묶어 보낸다. **RDB Writer의 사실상 표준이다.**

```java
@Bean
public JdbcBatchItemWriter<Payment> paymentWriter(DataSource dataSource) {
    return new JdbcBatchItemWriterBuilder<Payment>()
            .dataSource(dataSource)
            .sql("UPDATE payments SET status = :status, processed_at = NOW() " +
                 "WHERE id = :id")
            .beanMapped()
            .assertUpdates(true)
            .build();
}
```

`beanMapped()`는 객체 프로퍼티를 named parameter에 매핑한다. `assertUpdates(true)`는 한 INSERT/UPDATE가 1건도 변경하지 못하면 예외를 던진다 — 이게 멱등성 검증의 한 축이 된다.

JdbcBatchItemWriter가 빠른 이유는 단순하다. 100건짜리 청크라면 JDBC `addBatch()`로 100번 더하고, 마지막에 `executeBatch()`로 한 번에 보낸다. 네트워크 라운드트립이 100번이 아니라 1번이다. 그래서 같은 100건이라도 처리 시간이 10배 이상 차이 난다.

### JpaItemWriter — Dirty Checking의 함정

JPA 환경에서 자연스럽게 손이 가는 Writer다. `JpaItemWriter`는 청크 안의 엔티티들을 `EntityManager`에 merge한다. 그러면 트랜잭션 커밋 시점에 JPA가 알아서 변경된 필드를 UPDATE 한다. 이게 **Dirty Checking**이다.

코드는 깔끔해 보인다.

```java
@Bean
public JpaItemWriter<Payment> jpaWriter(EntityManagerFactory emf) {
    return new JpaItemWriterBuilder<Payment>()
            .entityManagerFactory(emf)
            .build();
}
```

그런데 위험하다. 왜?

JPA의 Dirty Checking은 **엔티티 한 개당 UPDATE 한 번**을 만든다. 100건짜리 청크라면 100개의 UPDATE가 트랜잭션 커밋 시점에 차례로 날아간다. JdbcBatchItemWriter처럼 한 번에 묶이지 않는다(엄밀히 말하면 hibernate batch insert/update 설정으로 일부 묶을 수 있지만 기본 구성에서는 안 묶인다).

게다가 영속성 컨텍스트(1차 캐시)에 청크의 모든 엔티티가 누적된다. 60만 건 잡이라면 영속성 컨텍스트에 60만 개의 엔티티가 쌓이려고 한다. 메모리 폭발이다. 이걸 막으려면 청크마다 `EntityManager.clear()`를 호출하는 패턴이 필요하다.

카카오페이 정산팀이 공개한 사례에서 가장 큰 단일 개선 중 하나가 **JpaItemWriter Dirty Checking을 JdbcBatchItemWriter로 교체**하는 것이었다. 50,000건 정산 잡에서 이 한 가지 변경이 큰 비중의 시간 단축을 만들었다. 이 사례는 6장에서 backbone으로 다시 다룬다.

### Writer 결정 트리

| 출력 대상 | 권장 | 비고 |
|---|---|---|
| RDB INSERT/UPDATE | `JdbcBatchItemWriter` | 표준 |
| 외부 API 호출 | 커스텀 Writer (멱등 키 + 에러 격리) | 7장에서 다룸 |
| 파일 출력 | `FlatFileItemWriter` / `JsonFileItemWriter` | |
| Kafka 발행 | `KafkaItemWriter` | 트랜잭션 동기화 주의 |
| MongoDB | `MongoItemWriter` | |
| JPA가 진짜 필요한 경우 | `JpaItemWriter` + `EntityManager.clear()` 패턴 | 신중히 |

**원칙:** RDB라면 JdbcBatchItemWriter를 기본으로, JPA Dirty Checking은 정말 그게 필요한 자리에서만. 정산·통계·마이그레이션 같은 대량 처리에는 거의 항상 JdbcBatchItemWriter가 답이다.

## ItemProcessor — 변환과 필터링

Reader와 Writer 사이에 끼는 Processor는 두 가지 일을 한다.

- **변환:** 입력 타입 I를 출력 타입 O로 바꾼다. 예를 들어 `Payment` 엔티티를 `SettlementResult` DTO로 바꾼다.
- **필터링:** `null`을 반환해서 그 항목이 Writer로 가지 않게 한다.

```java
@Bean
@StepScope
public ItemProcessor<Payment, SettlementResult> settlementProcessor(
        @Value("#{jobParameters['minAmount']}") Long minAmount) {
    return payment -> {
        if (payment.getAmount() < minAmount) {
            return null;  // 최소 금액 미만은 필터링
        }
        return SettlementResult.from(payment);
    };
}
```

Processor를 안 쓸 수도 있다. Reader와 Writer만으로 잡이 완결된다면 Processor를 생략해도 된다. `StepBuilder`에 reader와 writer만 등록하면 된다.

Processor에서 절대 하지 말아야 할 일이 한 가지 있다. **Processor 안에서 외부 API를 단건 호출하는 것이다.** 청크가 100건이면 외부 API가 100번 호출되고, 각 호출이 100ms면 청크 처리에 10초가 걸린다. 그동안 청크 트랜잭션은 열려 있고, DB 커넥션은 점유돼 있다. 끔찍한 일이다.

외부 API 호출이 필요하다면 Writer 단계에서 청크 단위로 일괄 호출하거나, 별도 Step으로 분리하는 것이 정석이다. 카카오페이 정산팀의 첫 번째 개선이 정확히 이거였다 — Processor에서 외부 API 단건 호출을 제거하고, Writer에서 일괄 처리로 옮긴 것. 이 패턴이 6장에서 backbone으로 자세히 다뤄진다.

## @StepScope 실전 매개화 — JobParameters를 받는 Reader/Writer

3장에서 `@StepScope`가 왜 필요한지를 짚었다. 빈 생성 시점이 컨테이너 부팅이 아니라 Step 시작 시점으로 미뤄지는 이유 — 그래야 JobParameters가 주입될 수 있다.

이번 장에서는 그걸 실전 패턴으로 묶어보자. **Reader와 Writer를 JobParameters로 매개화하는 것**은 운영 잡의 거의 모든 자리에서 등장한다. 매일 도는 정산 잡이 그날 날짜를 받아야 하고, 마이그레이션 잡이 시작 ID와 끝 ID를 받아야 하고, 통계 잡이 집계 기간을 받아야 한다.

다음은 정산 Reader/Writer를 매개화한 예시다.

```java
@Configuration
public class SettlementJobConfig {

    @Bean
    public Job settlementJob(JobRepository jobRepository, Step settleStep) {
        return new JobBuilder("settlementJob", jobRepository)
                .start(settleStep)
                .build();
    }

    @Bean
    public Step settleStep(JobRepository jobRepository,
                           PlatformTransactionManager txManager,
                           ItemReader<Payment> paymentReader,
                           ItemProcessor<Payment, SettlementResult> processor,
                           ItemWriter<SettlementResult> writer) {
        return new StepBuilder("settleStep", jobRepository)
                .<Payment, SettlementResult>chunk(500, txManager)
                .reader(paymentReader)
                .processor(processor)
                .writer(writer)
                .build();
    }

    @Bean
    @StepScope
    public JdbcPagingItemReader<Payment> paymentReader(
            @Value("#{jobParameters['date']}") String date,
            DataSource dataSource) throws Exception {

        MySqlPagingQueryProvider qp = new MySqlPagingQueryProvider();
        qp.setSelectClause("id, amount, status");
        qp.setFromClause("FROM payments");
        qp.setWhereClause("WHERE settle_date = :date AND status = 'PENDING'");
        qp.setSortKeys(Map.of("id", Order.ASCENDING));

        return new JdbcPagingItemReaderBuilder<Payment>()
                .name("paymentReader")
                .dataSource(dataSource)
                .queryProvider(qp)
                .parameterValues(Map.of("date", date))
                .pageSize(500)
                .rowMapper(new BeanPropertyRowMapper<>(Payment.class))
                .build();
    }

    @Bean
    @StepScope
    public ItemProcessor<Payment, SettlementResult> settlementProcessor(
            @Value("#{jobParameters['minAmount']}") Long minAmount) {
        long threshold = (minAmount != null) ? minAmount : 0L;
        return payment -> {
            if (payment.getAmount() < threshold) return null;
            return SettlementResult.from(payment);
        };
    }

    @Bean
    public JdbcBatchItemWriter<SettlementResult> settlementWriter(DataSource dataSource) {
        return new JdbcBatchItemWriterBuilder<SettlementResult>()
                .dataSource(dataSource)
                .sql("INSERT INTO settlements (payment_id, amount, settled_at) " +
                     "VALUES (:paymentId, :amount, NOW())")
                .beanMapped()
                .build();
    }
}
```

이 코드에서 주목할 점이 몇 가지 있다.

- **Reader와 Processor에만 `@StepScope`가 붙어 있다.** Writer는 JobParameters를 받지 않으므로 싱글턴으로 둔다. 불필요한 자리에 `@StepScope`를 붙이지 않는 것이 원칙이다.
- **Reader가 keyset 페이징을 쓰지 않는 점은 의도된 단순화다.** 본격적인 keyset이 필요하면 Querydsl no-offset reader를 쓴다.
- **chunk size 500을 일단 기본값으로 두고, production에서 측정해서 조정한다.** 이게 8장 튜닝의 출발점이다.

`@StepScope`가 빈 생성을 잡 시작 이후로 미루는 효과 덕에, JobParameters의 `date`와 `minAmount`가 자연스럽게 주입된다. 이 패턴이 운영 잡의 90%에서 그대로 쓰인다. 자주 마주칠 형태이니 손에 익혀두자.

## 직접 짠 코드 vs Spring Batch 6 — Reader/Writer 매핑

이쯤에서 1·2·3장에서 시작한 매핑을 이어가자. Reader/Writer 영역에서 우리가 직접 짤 때 했던 일이 어디로 옮겨지는가?

| 직접 짤 때 | Spring Batch 6 |
|---|---|
| `SELECT ... LIMIT N OFFSET M` 페이징 SQL을 직접 작성 | `JdbcPagingItemReader`가 자동 |
| 페이지 인덱스를 멤버 변수에 들고 다님 | Reader가 ExecutionContext에 자동 저장 |
| 재시작 시 마지막 페이지 인덱스를 별도 테이블에서 복원 | ExecutionContext에서 자동 복원 |
| `for (Item i : chunk) jdbc.update(...)` 100번 호출 | `JdbcBatchItemWriter`의 batch update 1번 |
| try-commit-rollback을 N건마다 직접 작성 | `.chunk(N, txManager)` 한 줄 |
| JPA로 짤 때 `entityManager.clear()` 매 청크마다 직접 호출 | (JdbcBatchItemWriter면 아예 불필요) |
| 단건 처리 안 되는 일을 어떻게 할지 매번 고민 | tasklet으로 명확히 분리 |

매번 짜던 페이징 SQL과 트랜잭션 관리 코드가 표준 자리로 옮겨진 모습이다. 그리고 새로 추가된 게 한 가지 있다 — **재시작 시 자동 복원**이다. 직접 짤 때는 진행 위치를 별도 테이블에 INSERT하고 재시작 시 SELECT 하는 인프라를 따로 만들어야 했는데, Spring Batch에서는 Reader가 알아서 ExecutionContext에 저장하고 알아서 읽어온다. 이게 1장에서 우리가 가장 골치 아파했던 부분이고, 그게 이렇게 표준화돼 있다.

## Tasklet의 1할 자리

이제 청크 모델이 어색해지는 자리로 넘어가자. 2장에서 잠깐 언급한 tasklet이다.

청크 모델은 항목 단위 반복에 잘 맞는다. "수십만 건의 어떤 데이터를 한 건씩 변환해서 쓴다"는 식이다. 그런데 모든 일이 그런 모양은 아니다. 한번 상황을 가정해보자.

- 어제 떨어진 압축 파일을 풀어야 한다.
- 30일 지난 임시 디렉터리를 비워야 한다.
- 잡 시작 전에 외부 셸 스크립트로 환경 점검을 한다.
- 잡 끝난 뒤 결과 파일을 S3에 업로드한다.
- FTP에서 오늘 떨어질 파일을 받아온다.

이 일들은 청크 모델로 풀면 어색해진다. "압축 파일 한 개를 한 건으로 보고 read해서 변환해서 write한다"는 식으로 짜면 작위적이다. 한 덩어리의 일이지 항목 반복이 아니다. 이런 일을 위해 Spring Batch는 **tasklet** 모델을 따로 둔다.

### Tasklet의 모양

`Tasklet` 인터페이스는 메서드 하나다.

```java
public interface Tasklet {
    RepeatStatus execute(StepContribution contribution, ChunkContext chunkContext)
            throws Exception;
}
```

`execute()`가 한 번 호출되어 일을 다 하면 `RepeatStatus.FINISHED`를 반환하고 끝난다. 한 번에 다 못 끝나면 `RepeatStatus.CONTINUABLE`을 반환해서 다시 호출되도록 할 수도 있다. 단발성 작업은 보통 FINISHED 한 번이면 끝이다.

가장 단순한 예시. 디렉터리 정리 tasklet.

```java
@Bean
public Tasklet cleanupTasklet() {
    return (contribution, chunkContext) -> {
        Path tempDir = Path.of("/var/batch/tmp");
        Instant cutoff = Instant.now().minus(Duration.ofDays(30));

        try (Stream<Path> files = Files.walk(tempDir)) {
            files.filter(p -> {
                try {
                    return Files.getLastModifiedTime(p).toInstant().isBefore(cutoff);
                } catch (IOException e) {
                    return false;
                }
            }).forEach(p -> {
                try { Files.deleteIfExists(p); } catch (IOException ignored) {}
            });
        }
        return RepeatStatus.FINISHED;
    };
}

@Bean
public Step cleanupStep(JobRepository jobRepository,
                        PlatformTransactionManager txManager,
                        Tasklet cleanupTasklet) {
    return new StepBuilder("cleanupStep", jobRepository)
            .tasklet(cleanupTasklet, txManager)
            .build();
}
```

`StepBuilder.tasklet(...)`이 청크 모델 `.chunk(...)`의 자리를 대신한다. 이 Step은 한 번 실행되면 디렉터리를 정리하고 끝난다.

### SystemCommandTasklet

외부 셸 명령을 실행해야 할 때를 위해 Spring Batch는 `SystemCommandTasklet`을 미리 제공한다.

```java
@Bean
public Tasklet unzipTasklet() {
    SystemCommandTasklet tasklet = new SystemCommandTasklet();
    tasklet.setCommand("unzip", "/data/incoming/today.zip", "-d", "/data/work");
    tasklet.setTimeout(60_000);  // 60초 타임아웃
    tasklet.setWorkingDirectory("/data");
    return tasklet;
}
```

이걸 직접 짜려면 `ProcessBuilder`로 프로세스를 띄우고, stdout/stderr를 읽고, exit code를 확인하고, 타임아웃을 걸고, 인터럽트 처리를 하고… 한참이다. SystemCommandTasklet이 그걸 다 표준 방식으로 해준다.

### MethodInvokingTaskletAdapter

이미 있는 빈의 메서드를 tasklet으로 쓰고 싶을 때 어댑터다.

```java
@Bean
public MethodInvokingTaskletAdapter notifyTasklet(NotificationService service) {
    MethodInvokingTaskletAdapter adapter = new MethodInvokingTaskletAdapter();
    adapter.setTargetObject(service);
    adapter.setTargetMethod("sendCompletionAlert");
    return adapter;
}
```

`NotificationService.sendCompletionAlert()` 메서드가 호출되고, void 반환이면 자동으로 FINISHED가 된다.

### Tasklet vs Chunk-oriented — 비교 표

| 항목 | Tasklet | Chunk-oriented |
|---|---|---|
| 적합한 일 | 단발성 작업, 한 덩어리의 일 | 항목 단위 반복 처리 |
| 트랜잭션 | tasklet 전체가 한 트랜잭션 | 청크 단위 트랜잭션 |
| 재시작 | tasklet 단위 재실행 (보통 처음부터) | 마지막 커밋된 청크 다음부터 |
| 메트릭 | step 단위 (item 단위 메트릭은 약함) | item read/write 카운트 자동 |
| 사용 빈도 | 1할 | 9할 |
| 대표 예시 | 파일 압축, 디렉터리 정리, 외부 명령 | 데이터 처리 모든 종류 |

이 표를 머릿속에 두고 가자. **새 잡을 만들 때 첫 질문은 "이게 항목 반복인가, 한 덩어리 일인가?"** 항목 반복이면 chunk, 한 덩어리면 tasklet. 그 외에는 chunk가 기본이라고 생각하면 거의 틀리지 않는다.

### Tasklet과 Chunk-oriented Step을 한 잡에 섞기

실제 잡은 종종 둘을 섞는다. 흔한 패턴은 이렇다.

```
Job
├── Step 1: tasklet (파일 다운로드)
├── Step 2: chunk-oriented (파일 파싱 + DB 적재)
├── Step 3: chunk-oriented (적재된 데이터 검증 + 정산 계산)
└── Step 4: tasklet (결과 파일 S3 업로드)
```

앞뒤 단발성 작업은 tasklet, 가운데 데이터 처리는 chunk. 이렇게 섞이면 각 단계의 책임이 명확해지고, Step 단위 재시작도 깔끔해진다. 한 Step에 모든 것을 우겨 넣지 않는 게 운영 감각이다.

## 청크 안에서 한 건이 실패하면 — 미리 보는 fault tolerance

이 장의 마지막 주제로, 청크 안에서 한 건이 실패하면 어떻게 되는지를 한 번 짚자. 자세한 내용은 7장에서 다루지만, 이 장에서 청크 모델을 깊이 봤으니 미리 그림을 그려두자.

기본 동작은 이렇다.

- 청크 안의 한 건이 예외를 던지면 **청크 전체 트랜잭션이 롤백된다.**
- 그러면 Step 자체가 FAILED 상태가 된다.

이게 우리가 원하는 동작인 경우도 있고 아닌 경우도 있다. **일시적 외부 의존 실패**(네트워크 깜빡임, DB 락 타임아웃)는 잠깐 기다렸다가 같은 청크를 다시 시도하면 되는 일이다. 이걸 retry라고 한다. **데이터 결함 실패**(특정 항목의 형식이 깨져 있음)는 그 항목만 건너뛰고 잡은 계속 가는 게 합리적이다. 이걸 skip이라고 한다.

`StepBuilder`에 `.faultTolerant()`를 호출하고 retry/skip 정책을 붙이면 이 동작이 활성화된다.

```java
RetryPolicy retryPolicy = RetryPolicy.builder()
        .maxRetries(3)
        .includes(Set.of(TransientException.class))
        .build();

SkipPolicy skipPolicy = new LimitCheckingExceptionHierarchySkipPolicy(
        Map.of(FlatFileParseException.class, true), 50);

return new StepBuilder("step", jobRepository)
        .<In, Out>chunk(500, txManager)
        .reader(reader)
        .writer(writer)
        .faultTolerant()
        .retryPolicy(retryPolicy)
        .skipPolicy(skipPolicy)
        .build();
```

여기서 한 가지를 미리 짚어두자. **Skip이 발생하면 청크가 chunk size = 1로 자동 단건 모드로 전환된다.** 이건 Spring Batch의 내부 메커니즘이다. 청크 안에서 어느 항목이 실패했는지 정확히 식별하려면 한 건씩 다시 처리할 수밖에 없기 때문이다. 즉, skip을 켜면 정상 시 chunk size 500으로 잘 돌다가, skip 발생 청크에서만 잠시 단건 모드가 된다. 이게 멀티스레드 step에서 reader 일관성과 미묘하게 충돌할 수 있다 — 자세한 내용은 8장 멀티스레드 함정에서 다룬다.

지금은 한 줄만 기억하자. **chunk = 트랜잭션. 청크 안 한 건 실패는 청크 롤백. retry/skip을 켜면 동작이 달라진다.**

## 자기 손으로 OOM 만들어보기 (실험)

3장에서 `@StepScope` 함정에 일부러 빠져보라고 권한 것처럼, 이 장에서도 한 가지 실험을 권한다. **OOM을 의도적으로 만들어 보자.**

`JdbcPagingItemReader` 대신, "쿼리 결과를 다 List에 담은 다음 한 건씩 내보내는" 직접 작성 Reader를 만들어보자.

```java
@Bean
@StepScope
public ItemReader<Payment> dangerousReader(JdbcTemplate jdbc) {
    List<Payment> all = jdbc.query(
            "SELECT * FROM payments",
            new BeanPropertyRowMapper<>(Payment.class));
    Iterator<Payment> it = all.iterator();
    return () -> it.hasNext() ? it.next() : null;
}
```

이 Reader로 100만 건짜리 테이블을 처리해보자. 힙 사이즈를 작게 잡고 돌리면(`-Xmx256m`) OOM이 난다. 어디서 메모리가 잡혀 있는지 heap dump로 확인해보자. `Payment` 객체 100만 개가 List에 잡혀 있다.

이 실험을 한 번 해보면, "Reader는 한 건씩 흘려보내야지 다 들고 있으면 안 된다"는 감각이 신체적으로 박힌다. 그리고 OKKY OOM 질문을 보면 5초 만에 원인이 보인다.

## 마무리

ItemReader/Processor/Writer의 계약을 한 줄씩 풀고, chunk·page·fetch size가 다른 레이어의 개념임을 그림으로 정리하고, Cursor와 Paging의 결정 트리를 만들었다. JdbcBatchItemWriter가 표준이고 JpaItemWriter Dirty Checking이 위험하다는 운영 감각도 짚었다. `@StepScope` 실전 매개화 패턴은 운영 잡의 90%에서 그대로 쓰인다.

청크 모델이 어색한 자리에는 tasklet을 꺼낸다. 9 대 1 비중에서 1할이 tasklet의 자리다. SystemCommandTasklet, MethodInvokingTaskletAdapter 같은 표준 어댑터가 그 자리에 있다. 한 잡 안에 tasklet과 chunk-oriented Step을 섞는 게 흔한 패턴이다.

여기까지가 1막의 마무리다. 우리는 배치라는 문제를 다시 정의했고(1장), Spring Batch의 모델을 한 그림으로 정리했고(2장), 첫 잡을 손으로 띄우면서 두 가지 함정을 통과했고(3장), 청크 모델의 안쪽을 깊이 들여다봤다(4장). 이제 독자는 Spring Batch가 자기 문제를 어떻게 해결하는지를 신체적으로 안다.

다음 장부터는 2막이다. **Spring Batch 6에서 무엇이 갈아엎어졌는지**를 본격적으로 다룬다. 4장에서 청크 모델을 봤으니, 5장에서 그 모델이 6에서 어떻게 재설계됐는지가 자연스럽게 이어진다. `ChunkOrientedTasklet`이 deprecated된 이유, producer-consumer + bounded queue 동시성 모델, JobOperator로의 통합, recover API, graceful shutdown, 그리고 도메인 모델 record화·primitive long 전환·v5 직렬화 비호환까지. 모델을 알아야 변경의 의도가 보인다 — 그래서 4장 다음에 5장이다.
