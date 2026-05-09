# 6장. 실전 유스케이스 — 카카오페이 정산 사례 해부

정산 잡이 5만 건을 넘기면서 1시간을 넘긴다. PM이 묻는다, 왜 이렇게 느리냐고. 우리는 답한다 — "쿼리 튜닝하면 됩니다." 그런데 EXPLAIN을 떠보니 인덱스도 잘 타고, slow query도 안 잡힌다. 어디가 느린 건지 손으로 짚을 수가 없다. 그러는 사이 데이터는 자라고, 다음 분기에는 7만 건, 그 다음엔 10만 건이 된다. 어디서부터 손을 대야 할까?

카카오페이 정산팀이 공개한 실 개선 사례를 한 호흡에 풀어보자. 단순 인용이 아니라, 그 단계 하나하나를 우리 시각으로 다시 분석하면서 — **production 정산 시스템이 어떤 결정을 어떤 순서로 내려야 약 10배가 빨라지는지**를 추적한다. 이 backbone 하나를 머릿속에 박아두면, 자기 도메인의 정산·집계·변환 잡을 어디서부터 손볼지 결정할 수 있다.

미리 한 가지를 짚어두자. 이건 "튜닝 챕터"가 아니다. 튜닝의 한 가지 결정 트리(chunk size·page size·fetch size)는 8장에서 본격적으로 다룬다. 6장은 그 결정 트리를 꺼내기 전에 — **구조 자체를 먼저 점검**하는 사례다. 카카오페이의 결론이 그것이다: "처음부터 병렬 처리보다, 현재 구조에서 I/O를 묶는 것이 효율적이다."

## 정산이라는 도메인의 특수성

본 사례를 뜯기 전에, 정산이라는 일이 왜 특별한지부터 짚어두자. 사례를 머릿속에 두면서 본 사례를 분석해야 단계별 결정의 의미가 살아난다.

정산(settlement)은 결제(payment)와 다르다. 결제는 사용자가 카드를 긁는 그 순간의 거래다. 정산은 그 거래가 발생한 뒤, **여러 채널의 데이터를 모아서 누구에게 얼마를 줘야 하는지를 확정하는 일**이다. 가맹점 정산이면 가맹점에게 얼마를 송금할지, 파트너 정산이면 파트너사에 얼마를 분배할지를 매일·주간·월간 단위로 산출한다.

이 도메인의 특수성을 세 가지로 정리해두자.

**하나, 다중 소스 ingest.** 정산의 입력은 한 군데가 아니다. 카드사 청구 파일, PG사 거래 내역, 자체 거래 로그, 환불 데이터, 수수료 정책 — 각기 다른 시스템에서 온다. 어떤 건 파일로 오고, 어떤 건 API로 오고, 어떤 건 자체 DB에 있다. 잡의 첫 단계는 이 여러 소스를 모으는 일이다.

**둘, intelligent matching.** 모은 데이터를 서로 짝지어야 한다. 카드사가 보내준 청구 1건이 자체 거래 로그의 어떤 거래와 짝인지를 ID·금액·시각의 조합으로 매칭한다. 1대1 매칭이 안 되는 건이 항상 생긴다 — 이건 reconciliation 패턴의 영역이다.

**셋, mismatch 처리.** 매칭이 안 된 건들을 어떻게 격리할지. 일부는 자동으로 보정 가능하고, 일부는 사람이 보고 판단해야 한다. 정산 시스템의 신뢰성은 결국 이 mismatch 처리가 얼마나 견고한지에 달려 있다.

이 셋이 한 잡 안에서 한 호흡에 흐른다. 그래서 정산 잡은 단순한 "데이터 변환"이 아니라, 도메인 지식이 코드에 두껍게 녹아드는 잡이다. Spring Batch의 모델이 이 일에 잘 맞는 이유가 여기 있다 — chunk-oriented가 ingest와 변환을, ExecutionContext가 단계 간 상태 전달을, fault-tolerance가 mismatch 격리를 책임진다.

## 출발점 — 50,000건 1시간+, 그리고 잘못된 가설

카카오페이 정산팀이 공개한 그 시점의 상황은 이렇다. **5만 건 이상 처리할 때 잡이 1시간을 넘긴다.** 데이터가 자라면서 야간 배치 창이 점점 빠듯해진다. 가장 자연스럽게 떠오르는 가설은 두 개다.

가설 A — "쿼리가 느린 거다, 인덱스를 추가하거나 SQL을 튜닝하자."
가설 B — "병렬 처리하자, 멀티스레드를 켜거나 partitioning하면 빨라진다."

이 두 가설이 운영 회의에서 가장 먼저 나온다. 그런데 둘 다 이 사례에서는 부분 정답이거나, 잘못된 첫걸음이었다. 왜일까?

EXPLAIN을 떠봤다. SELECT는 빠르다. 인덱스도 잘 탄다. slow query log도 깨끗하다. 그렇다면 쿼리는 1차 원인이 아니다. 가설 A는 빠진다.

병렬 처리는 어떨까? 멀티스레드로 4배 빠르게 한다고 해보자. 그래서 1시간이 15분이 되면 좋겠다. 그런데 — **같은 구조를 4개로 복제했을 뿐, 병목 자체는 그대로다.** 한 스레드에서 일어나던 비효율이 4개 스레드 각각에서 4배로 일어난다. CPU와 DB 커넥션만 더 쓴다. 그리고 더 큰 문제 — 병렬 처리는 코드 복잡도를 키운다. restartability가 약화되고, race condition이 새 함정을 만든다. **병렬 처리는 마지막 카드여야지, 첫 카드가 아니다.**

이게 이 사례의 가장 큰 교훈이다. 카카오페이팀의 결론을 한 번 더 인용해두자.

> "처음부터 병렬 처리보다 현재 구조에서 I/O 작업을 묶어서 처리하는 것이 효율적이다."

병렬 처리 대신, 그들은 **구조를 점검**했다. 한 스레드 안에서 일어나는 일을 한 단계씩 들여다봤다. 그러자 비효율의 위치가 분명해졌다. 그것이 다음 4단계의 출발이다.

## 개선 1단계 — Processor 단건 외부 API 호출 → Writer 일괄 처리

처음 발견한 비효율의 위치는 ItemProcessor였다.

기존 구조는 이랬다.

```java
// (개선 전) Processor가 항목마다 외부 API 호출
public class SettlementProcessor implements ItemProcessor<RawTransaction, EnrichedTransaction> {
    private final ExternalApiClient apiClient;

    @Override
    public EnrichedTransaction process(RawTransaction tx) {
        // 항목마다 외부 API 호출 — 약 150ms
        ExternalInfo info = apiClient.fetch(tx.getExternalId());
        return new EnrichedTransaction(tx, info);
    }
}
```

이 코드의 문제는 무엇일까? 청크 사이즈를 1,000으로 잡았다고 해보자. 한 청크를 처리하는 동안, Processor가 1,000번 외부 API를 호출한다. 한 호출이 150ms라면 청크 1개 처리에만 — 외부 API에서만 — 150초가 든다. 5만 건이면 7,500초, 약 2시간이다.

그리고 더 큰 문제가 있다. 이 호출들은 **순차적**이다. read 1 → process 1 → read 2 → process 2 → … 이렇게 흐른다. 외부 API는 batch 호출도 받을 수 있는데, 그 능력을 안 쓴다. 네트워크 라운드트립이 1번이면 끝날 수 있는 일을 1,000번 한다.

개선 방향이 분명하다. **외부 API 호출을 Processor에서 떼어내, Writer가 청크 단위로 일괄 호출하게 한다.**

```java
// (개선 후) Processor는 단순 변환만, Writer가 일괄 처리
public class SettlementProcessor implements ItemProcessor<RawTransaction, RawTransaction> {
    @Override
    public RawTransaction process(RawTransaction tx) {
        // 외부 API 호출 제거, 단순 변환만
        return tx;
    }
}

public class SettlementWriter implements ItemWriter<RawTransaction> {
    private final ExternalApiClient apiClient;
    private final SettlementRepository repository;

    @Override
    public void write(Chunk<? extends RawTransaction> chunk) throws Exception {
        // 청크 안의 외부 ID를 한 번에 모아서 batch 호출
        List<String> externalIds = chunk.getItems().stream()
            .map(RawTransaction::getExternalId)
            .toList();

        // 1번 호출로 1,000건 분 외부 정보를 가져온다
        Map<String, ExternalInfo> infoMap = apiClient.fetchBatch(externalIds);

        // 변환 후 일괄 저장
        List<EnrichedTransaction> enriched = chunk.getItems().stream()
            .map(tx -> new EnrichedTransaction(tx, infoMap.get(tx.getExternalId())))
            .toList();

        repository.saveAll(enriched);
    }
}
```

이 변경 하나로 청크 1개 처리 시 외부 API 호출 횟수가 1,000번 → 1번이 된다. 네트워크 라운드트립이 1,000배로 줄어드는 셈이다. 외부 API가 batch 호출을 지원하지 않는다 해도 — 적어도 같은 청크 안에서 비동기 호출로 묶거나, 동일 키 호출을 dedupe하는 자리가 Writer에 생긴다.

여기서 짚을 점이 두 가지다.

**첫째, 트랜잭션 경계가 깨끗해진다.** 이전 구조는 외부 API 호출이 청크 트랜잭션 안에 들어와 있었다. 외부 호출이 느려지면 DB 트랜잭션이 길게 잡혀 락 경합을 일으켰다. Writer로 옮기면서 외부 API와 DB 쓰기의 순서가 명확해진다. (외부 API가 멱등하지 않으면 7장의 outbox 패턴을 함께 봐야 한다. 여기서는 외부 정보 조회가 멱등이라고 가정한다.)

**둘째, Processor의 자리가 다시 명확해진다.** Spring Batch의 모델에서 Processor는 **"변환과 필터링"** 자리지, "외부 호출" 자리가 아니다. 외부 호출을 Processor에 넣으면 항목 단위 호출이 되고, 항목 단위 호출은 거의 항상 비효율이다. 외부 의존이 들어와야 한다면 Writer로 모아 청크 단위로 묶자.

이 한 단계만으로 정산 잡이 얼마나 빨라졌을까? 카카오페이팀의 보고는 이 지점부터 다음 단계와 합쳐 약 10배 향상이라고 묶어 적었지만, 이 한 단계만 따로 보면 외부 API I/O 비중이 큰 잡일수록 효과가 크다. 5만 건의 외부 API 호출을 50번으로 줄였다면(청크 1,000), 그 자체로 수십 분 단축이 가능하다.

## 개선 2단계 — JpaItemWriter Dirty Checking → JdbcBatchItemWriter

다음 비효율의 위치는 Writer였다. 처음 코드는 JPA 기반이었다.

```java
// (개선 전) JpaItemWriter — Dirty Checking에 의존
public class SettlementWriter implements ItemWriter<EnrichedTransaction> {
    private final EntityManager em;

    @Override
    public void write(Chunk<? extends EnrichedTransaction> chunk) {
        for (EnrichedTransaction tx : chunk.getItems()) {
            Settlement settlement = em.find(Settlement.class, tx.getSettlementId());
            settlement.update(tx);  // 도메인 메서드로 필드 변경
            // flush 시점에 Dirty Checking으로 UPDATE
        }
    }
}
```

이 코드의 모양은 깔끔하다. JPA의 도메인 객체 그대로, 도메인 메서드로 상태를 바꾸고, flush 시점에 알아서 UPDATE가 나간다. JPA 책의 모범 사례 같다.

그런데 정산 잡 같은 대량 처리에서는 이 패턴이 위험하다. 왜일까?

Dirty Checking은 영속성 컨텍스트가 관리하는 모든 엔티티를 감시하면서, flush 직전에 변경된 필드를 찾아내 UPDATE SQL을 만든다. 청크 1,000건이면 1,000번의 변경 감지가 일어나고, **1,000개의 개별 UPDATE 문**이 만들어진다. 한 트랜잭션 안에서 1,000번의 UPDATE를 RDB에 쏘는 셈이다.

게다가 영속성 컨텍스트는 1,000개의 엔티티를 메모리에 들고 있어야 한다. 청크 트랜잭션이 커밋되기 전까지 — 즉 모든 변경이 flush될 때까지 — 메모리 점유가 유지된다. OOM의 출발점이 여기다.

대안은 `JdbcBatchItemWriter`다. JDBC batch insert/update 기능을 그대로 쓴다.

```java
// (개선 후) JdbcBatchItemWriter — JDBC batch UPDATE
@Bean
public JdbcBatchItemWriter<EnrichedTransaction> settlementWriter(DataSource dataSource) {
    return new JdbcBatchItemWriterBuilder<EnrichedTransaction>()
        .dataSource(dataSource)
        .sql("""
            UPDATE settlement
               SET amount = :amount,
                   external_id = :externalId,
                   updated_at = :updatedAt
             WHERE id = :id
            """)
        .beanMapped()
        .build();
}
```

이 한 번의 변경으로 무엇이 달라질까?

**하나, JDBC batch.** 1,000건의 UPDATE가 개별 round-trip 1,000번이 아니라, JDBC batch로 한 번에 전송된다. 드라이버가 일괄로 처리하고, 결과만 한 번에 받는다. 네트워크 라운드트립이 1번 또는 batch size 단위로 줄어든다.

**둘, 메모리 점유 감소.** Dirty Checking이 빠지면 영속성 컨텍스트가 필요 없다. 청크가 끝나면 객체가 해제 가능 상태가 된다. 메모리 압박이 한층 가벼워진다.

**셋, SQL이 명시적이다.** Dirty Checking은 자기가 어떤 SQL을 만들지 코드만 봐서는 알 수 없다. JdbcBatchItemWriter는 SQL이 코드에 적혀 있다. 운영자가 EXPLAIN을 떠보고 인덱스를 점검할 수 있다. SQL의 모양을 코드에서 읽을 수 있다는 건, 디버깅·튜닝 측면에서 큰 가치다.

JpaItemWriter가 무조건 나쁘다는 얘기가 아니다. 작은 잡, 트랜잭션 안에서 도메인 메서드의 흐름이 중요한 잡에서는 JpaItemWriter도 충분하다. **다만 대량 처리에서 Dirty Checking은 함정이 되기 쉽다.** 청크 사이즈가 커지고 데이터가 자라면 비례해서 비용이 부풀어 오른다. 그런 자리에서는 JdbcBatchItemWriter로 옮겨두는 편이 낫다.

## 개선 3단계 — 동일 값 UPDATE의 IN 절 그룹화

여기서부터 흥미로워진다. 카카오페이팀이 본 다음 비효율은 **"같은 값으로 UPDATE되는 행이 많다"**는 점이었다.

상황을 그려보자. 정산 잡에서 가맹점 1,000개의 정산 상태를 `COMPLETED`로 마킹해야 한다고 하자. 단순하게 짜면 이렇다.

```sql
-- 1,000번의 UPDATE — JDBC batch로 묶여도 1,000개의 행 변경
UPDATE settlement SET status = 'COMPLETED' WHERE id = ?;
UPDATE settlement SET status = 'COMPLETED' WHERE id = ?;
... (1,000번 반복)
```

JDBC batch로 묶었으니 네트워크 라운드트립은 1번이지만 — RDB는 여전히 **1,000번의 행 단위 UPDATE 작업**을 한다. 인덱스를 1,000번 갱신하고, 1,000번의 row lock을 잡고 푼다.

그런데 자세히 보면 — 모두 같은 값(`'COMPLETED'`)으로 바꾸는 일이다. SQL에는 이걸 한 번에 처리하는 표준 도구가 있다 — IN 절이다.

```sql
-- 1번의 UPDATE — 1,000개 행을 한 번에
UPDATE settlement SET status = 'COMPLETED' WHERE id IN (?, ?, ?, ...);
```

이게 얼마나 빠른지 측정한 결과가 있다. 카카오페이팀의 보고에 따르면, 동일 값 UPDATE 1,000건을 IN 절로 묶었을 때 — **5,000건 이상 규모에서 90%+ 성능 향상**. 1,000건의 IN 절 UPDATE를 다시 쪼개도 최대 3건의 IN 절 UPDATE면 끝난다. 두 자릿수 배수의 차이다.

```java
// 동일 값으로 UPDATE되는 행을 그룹화
public class GroupedSettlementWriter implements ItemWriter<EnrichedTransaction> {
    private final NamedParameterJdbcTemplate jdbc;
    private static final int IN_CLAUSE_BATCH = 500;  // IN 절 1개당 최대 ID 수

    @Override
    public void write(Chunk<? extends EnrichedTransaction> chunk) {
        // 상태별로 그룹화: COMPLETED 그룹, PENDING 그룹, FAILED 그룹 ...
        Map<SettlementStatus, List<Long>> groups = chunk.getItems().stream()
            .collect(Collectors.groupingBy(
                EnrichedTransaction::getNewStatus,
                Collectors.mapping(EnrichedTransaction::getSettlementId, Collectors.toList())
            ));

        // 그룹별로 IN 절 UPDATE
        groups.forEach((status, ids) -> {
            // IN 절이 너무 길면 RDB 성능이 도리어 떨어지므로 적절히 분할
            for (int i = 0; i < ids.size(); i += IN_CLAUSE_BATCH) {
                List<Long> chunk2 = ids.subList(i, Math.min(i + IN_CLAUSE_BATCH, ids.size()));
                jdbc.update(
                    "UPDATE settlement SET status = :status WHERE id IN (:ids)",
                    Map.of("status", status.name(), "ids", chunk2)
                );
            }
        });
    }
}
```

여기서 두 가지 디테일을 짚어두자.

**하나, IN 절의 크기는 무한정 키울 수 없다.** Oracle은 IN 절에 1,000개 한도가 있다. PostgreSQL/MySQL은 한도가 더 크지만, IN 절이 너무 길면 옵티마이저가 다른 플랜으로 바꿔 도리어 느려질 수 있다. 보통 500~1,000을 한 IN 절의 안정 한도로 잡는다. 청크 사이즈가 그보다 크면 위 코드처럼 분할한다.

**둘, 멱등성 검토가 필요하다.** IN 절 UPDATE는 한 번에 여러 행을 바꾼다. 만약 중간에 실패해서 트랜잭션이 롤백되면 모든 행이 같이 롤백된다 — 이건 청크 트랜잭션의 정상 동작이다. 그러나 같은 청크가 retry로 재처리될 때, 첫 시도에서 일부가 다른 트랜잭션에 의해 이미 `COMPLETED`로 바뀌었다면? 그래도 동일 값을 다시 쓰는 UPDATE라 결과는 같다. **동일 값 UPDATE는 본질적으로 멱등**이다. 그래서 이 그룹화 패턴은 retry/restart에 안전하다.

이 패턴이 카카오페이 사례의 가장 인상적인 발견이다. SQL 한 줄을 어떻게 쓰느냐가 두 자릿수 성능 차이를 만든다는 것을 — 그것도 인덱스나 쿼리 튜닝이 아니라 "여러 UPDATE를 묶을 수 있는가"라는 단순한 시각의 차이가 만든다는 것을.

## 개선 4단계 — chunk size·page size·fetch size 정렬

마지막 단계는 셋의 정렬이다. 본격적인 튜닝 결정 트리는 8장에서 풀어내지만, 이 사례의 핵심만 여기서 한 번 짚어두자.

세 개념을 다시 분리하자.

- **chunk size** — 트랜잭션 1건당 처리할 항목 수. Spring Batch가 관리한다.
- **page size** — Paging Reader가 한 페이지에 가져올 행 수. JdbcPagingItemReader 등의 설정.
- **fetch size** — JDBC 드라이버가 한 라운드트립에 가져올 행 수. SQL 드라이버 레벨.

이 셋이 어긋나면 어떤 일이 벌어질까?

가령 chunk size = 1,000, page size = 100, fetch size = 10이라고 하자. 청크 하나를 채우려면 reader가 10번 page를 가져와야 하고, 각 page를 가져올 때 JDBC는 10번의 라운드트립을 한다 — 청크 하나 채우는 데 100번의 네트워크 호출. 이건 명백히 비효율이다.

권장하는 정렬은 이렇다.

```yaml
# 시작값 (production 데이터로 측정 후 조정)
chunk size = page size = 1,000
fetch size = chunk size 이상 (1,000 또는 2,000)
```

`chunk size = page size`로 맞추면 청크 하나를 채우는 데 reader가 page를 정확히 1번 호출한다. `fetch size ≥ chunk size`로 맞추면 그 page 호출이 1번의 JDBC 라운드트립으로 끝난다. 청크 하나 채우는 데 네트워크 호출 1번 — 가장 깔끔한 그림이다.

```java
@Bean
public JdbcPagingItemReader<RawTransaction> reader(DataSource dataSource) {
    return new JdbcPagingItemReaderBuilder<RawTransaction>()
        .name("settlementReader")
        .dataSource(dataSource)
        .pageSize(1000)              // chunk size와 일치
        .fetchSize(1000)             // page size 이상
        .selectClause("SELECT *")
        .fromClause("FROM raw_transaction")
        .whereClause("WHERE settlement_date = :date")
        .parameterValues(Map.of("date", "2026-05-08"))
        .sortKeys(Map.of("id", Order.ASCENDING))
        .rowMapper(new RawTransactionRowMapper())
        .build();
}
```

청크 사이즈를 더 키우면 좋을까? 항상 그렇진 않다. 청크 사이즈는 **트랜잭션 길이**다. 트랜잭션 길이는 **실패 비용**이다. 청크가 5,000건일 때 마지막 1건에서 실패하면 4,999건이 통째로 롤백된다. 그 5,000건을 처음부터 다시 처리해야 한다. 청크가 너무 크면 retry/restart의 비용이 커진다. 동시에 메모리 점유도 커진다.

그래서 시작값은 1,000 근처로 잡고, **production 데이터로 측정해서 늘리거나 줄인다.** 측정 없이 추측으로 정하는 chunk size는 거의 항상 잘못된 값이다. 8장에서 측정 방법과 결정 트리를 자세히 풀어낸다. 여기서는 "셋이 어긋나 있지 않은가"부터 점검하자는 점이 핵심이다.

## 약 10배 향상의 분배 — 어디가 얼마나 기여했나

위 4단계가 합쳐져 정산 잡이 약 10배 빨라졌다. 카카오페이팀의 보고는 단계별 정확한 기여도를 모두 적지는 않았지만, 일반적인 정산 잡의 특성을 감안해 기여도를 추정해보면 이렇다.

| 단계 | 변경 | 추정 기여 |
|------|-----|----------|
| 1단계 | Processor 단건 외부 API → Writer 일괄 | 약 3~5배 (외부 API I/O 비중에 비례) |
| 2단계 | JpaItemWriter Dirty Checking → JdbcBatchItemWriter | 약 1.5~2배 (행 수와 트랜잭션 패턴에 비례) |
| 3단계 | 동일 값 UPDATE → IN 절 그룹화 | 약 1.5~2배 (그룹화 가능 비율에 비례) |
| 4단계 | chunk·page·fetch size 정렬 | 약 1.2~1.5배 (이전 미스매치 정도에 비례) |

곱하면 대략 8~30배 사이가 나온다. 카카오페이의 약 10배는 이 분포의 중간쯤이다. 잡의 특성에 따라 단계별 기여도는 다르다 — 외부 API가 없는 잡은 1단계의 효과가 작고, 동일 값 UPDATE가 적은 잡은 3단계의 효과가 작다.

여기서 중요한 점은, **이 4단계 모두 "구조 변경"이지 "병렬화"가 아니라는 점이다.** 멀티스레드도, partitioning도, Remote Step도 켜지 않았다. 단일 스레드 안에서, 단일 JVM 안에서, 한 청크 한 청크 흐르는 모습 그대로 — 그저 **각 청크가 외부 시스템과 어떻게 통신하느냐**를 다듬었다. 한 자리에서 1,000번 호출하던 걸 1번 호출로 묶고, 1,000번 UPDATE하던 걸 IN 절 1번으로 묶고, 메모리에 1,000건을 들고 있던 걸 들고 있지 않게 만들었다.

병렬화는 그 다음 카드다. 8장에서 멀티스레드와 partitioning을 풀어내는데, 그것을 첫 번째 카드로 꺼내지 말자. 구조부터 점검하자. 카카오페이의 결론이 다시 한번 — "처음부터 병렬 처리보다 현재 구조에서 I/O 작업을 묶어서 처리하는 것이 효율적이다."

## reconciliation 패턴 — 다중 소스 매칭과 mismatch 격리

위 4단계는 "정산 잡이 빠르게 도는 법"의 사례다. 그런데 정산 도메인에는 또 하나의 결정 트리가 있다. **다중 소스 매칭과 mismatch 처리** — reconciliation이라고 부른다.

상황을 그려보자. 카드사 A의 청구 파일에 거래 1,000건이 있고, 자체 거래 로그에 같은 시점의 거래가 1,005건 있다. 5건이 차이난다. 이 5건이 무엇인지 — 카드사가 늦게 보고한 건인지, 자체 로그에 잘못 들어간 건인지, 환불 처리가 어긋난 건인지 — 매칭으로 가려야 한다.

reconciliation 시스템은 보통 3 단계로 흐른다.

**1단계: 다중 소스 ingest.** 카드사 청구 파일을 읽고, 자체 거래 로그를 읽고, 환불 데이터를 읽는다. 각각이 별도 Step이거나, 하나의 잡 안의 별도 Reader다. 입력 형식이 제각각(파일/DB/API)이라 Reader도 제각각.

**2단계: intelligent matching.** 모은 데이터를 짝지어 `matched` 테이블과 `unmatched` 테이블에 분리한다. 매칭 키는 거래 ID + 금액 + 시각의 조합. 1대1 매칭이 안 되는 건은 unmatched로 격리.

**3단계: mismatch 처리.** unmatched 항목을 분류한다. 자동 보정 가능한 건 — 카드사가 1초 늦게 보고한 식의 — 자동 보정. 사람 판단이 필요한 건 — 금액이 다른 식의 — 운영자 큐로 보낸다.

코드로 본 매칭 단계의 한 모양은 이렇다.

```java
// 매칭 Step의 Writer
public class ReconciliationWriter implements ItemWriter<TransactionPair> {
    private final MatchedRepository matched;
    private final UnmatchedRepository unmatched;

    @Override
    public void write(Chunk<? extends TransactionPair> chunk) {
        List<TransactionPair> matchedPairs = new ArrayList<>();
        List<TransactionPair> unmatchedPairs = new ArrayList<>();

        for (TransactionPair pair : chunk.getItems()) {
            if (pair.matches()) {
                matchedPairs.add(pair);
            } else {
                unmatchedPairs.add(pair);
            }
        }

        matched.saveAll(matchedPairs);
        unmatched.saveAll(unmatchedPairs);
    }
}
```

이 패턴의 가치는 **mismatch가 잡 자체를 실패시키지 않는다**는 점이다. 5건의 불일치가 있다고 잡 전체가 멈추면, 운영자가 매번 손으로 정리해야 한다. unmatched 테이블에 격리하면 잡은 정상 종료하고, 운영자는 그 테이블만 열어 처리한다. SkipListener를 써서 Slack/이메일로 알림을 보낼 수도 있다.

학술/산업 자료는 이 패턴이 이벤트 소싱과 결합되면 reconciliation 시간을 약 60% 줄인다고 보고한다. 이벤트 소싱이라는 추가 설계까지 가지 않더라도, **단순한 matched/unmatched 분리만으로도 정산 잡의 신뢰성은 한 단계 올라간다.** 카카오페이의 4단계 개선과 짝지어 보면, 정산 시스템의 두 축이 보인다. 하나는 한 번 도는 잡을 빠르게 만드는 일, 다른 하나는 그 잡이 mismatch를 견디며 매일 정상 종료하게 만드는 일.

## 박스: 직접 짰을 때 vs Spring Batch 6 — 정산 잡 매핑

이 사례를 직접 짠 코드와 매핑해보면, "Spring Batch가 어디까지 해주는가"가 분명해진다.

| 직접 짤 때 우리가 직접 만들던 것 | Spring Batch 6에서 |
|--------------------------------|--------------------|
| 어디까지 처리됐는지 추적 (offset/last_id 컬럼) | `ExecutionContext`가 자동 저장 |
| 배치 1건 = 트랜잭션 1건 (commit/rollback 직접 짬) | 청크 = 트랜잭션 (자동) |
| 외부 API batch 호출 묶기 | `ItemWriter`의 자연스러운 자리 |
| 실패한 배치 재시작 (수동 SQL 또는 admin API) | `JobOperator.start()`로 동일 JobInstance 재시작 |
| 어제 못 끝낸 거 처리 (직접 만든 cleanup 잡) | restart로 마지막 청크 다음부터 자동 |
| 메타 테이블 (직접 설계한 jobs/runs/items) | `BATCH_JOB_INSTANCE`/`BATCH_JOB_EXECUTION`/`BATCH_STEP_EXECUTION` 표준 |
| 멀티스레드 처리 (수동 ExecutorService) | `taskExecutor` 한 줄 + producer-consumer 모델 |
| Skip된 항목 별도 테이블에 격리 | `SkipListener`로 표준 패턴 |
| STARTED 박제 정리 | `JobOperator#recover()` 한 줄 (6.0 신규) |

직접 짠 정산 시스템의 코드 80%는 위 표의 왼쪽 칸에 들어 있다. 도메인 로직은 20% 정도다. Spring Batch가 약속하는 건 **그 80%를 다시 만들지 않게 해주겠다**는 것이고, 카카오페이 사례는 그 20%의 도메인 로직조차 어떤 구조로 짜야 production-ready인지를 보여준다.

## 정리 — 자기 도메인에 적용할 결정 트리

이 사례를 자기 정산·집계·변환 잡에 적용하려면 다음 순서로 점검해보자.

1. **외부 API 호출이 Processor에 있는가?** 있다면 Writer로 옮길 수 없는지 검토. 청크 단위 batch 호출로 묶을 수 있다면 거의 반드시 묶는다.
2. **Writer가 JpaItemWriter + Dirty Checking인가?** 대량 처리라면 JdbcBatchItemWriter로 바꿀 수 있는지 검토. 도메인 메서드의 흐름이 꼭 필요한 자리만 JPA로 남기고, 나머지는 명시적 SQL로.
3. **동일 값으로 UPDATE되는 행이 많은가?** 그룹화해서 IN 절로 묶을 수 있는지 검토. 멱등성 확인 후 적용.
4. **chunk size = page size, fetch size ≥ chunk size인가?** 어긋나 있다면 정렬. 그 다음 production 데이터로 측정해서 청크 사이즈를 조정.
5. **여기까지 했는데도 느린가?** 이제 멀티스레드/partitioning을 검토. 8장 결정 트리를 따라간다.
6. **정산 도메인이라면 reconciliation 단계가 있는가?** mismatch를 잡 실패가 아니라 별도 테이블로 격리하는 구조를 점검.

이 순서가 중요하다. 1번부터 4번을 건너뛰고 5번으로 가면, 비효율을 4배 빠르게 처리하게 될 뿐이다. 1번부터 4번이 끝난 뒤에야 멀티스레드가 진짜 의미를 가진다.

다음으로 넘어가, 이 잡들이 실패할 때를 보자. 청크가 롤백되면 어떻게 되는가, retry는 언제 의미 있는가, restart 안전성은 어떻게 자기진단하는가, 그리고 — 이 잡을 어떻게 테스트로 증명할 것인가. 정산 잡이 빠르게 도는 것만큼 중요한 건, 그 잡이 어떤 실패에서도 안전하게 다시 시작할 수 있다는 약속이다.
