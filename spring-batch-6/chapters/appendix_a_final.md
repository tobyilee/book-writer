# 부록 A. 유스케이스 패턴 카탈로그

6장이 카카오페이 정산 사례를 backbone으로 한 호흡에 풀었다면, 본문에 녹이지 못한 다른 유스케이스 4가지를 부록으로 묶어두자. 본문의 밀도를 지키면서, 자기 도메인에 가장 가까운 패턴을 빠르게 찾아갈 수 있는 카탈로그가 목적이다.

각 패턴은 같은 구조로 정리한다 — **언제 이 패턴인가 / Reader·Writer 결정 / 핵심 코드 / 주의할 함정**. 책을 다 읽은 뒤 1년 운영하면서 가장 자주 다시 펼쳐볼 자리가 이 부록이다.

## A.1 대용량 데이터 일괄 처리

### 언제 이 패턴인가

수천만~수억 행짜리 RDB 테이블 또는 멀티 GB 플랫 파일을 도메인 변환·검증·외부 시스템 적재로 한 번에 처리하는 잡. 가장 흔한 패턴이고, Spring Batch가 가장 잘 푸는 자리다.

대표 예: 사용자 활동 로그 → 데이터 웨어하우스 적재, 신용평가 데이터 일괄 갱신, 캠페인 대상자 한 번에 추출.

### Reader / Writer 결정

- **Reader:** `JdbcPagingItemReader` (단순 SQL) 또는 `QuerydslNoOffsetPagingItemReader` (jojoldu, 복잡 SQL + keyset 페이징). OFFSET 기반은 N이 커지면 비용이 폭증하므로 keyset(no-offset) 페이징이 사실상 표준.
- **Writer:** `JdbcBatchItemWriter` 1순위. 청크 단위 batch insert가 native query로 한 번에 나간다. JpaItemWriter는 Dirty Checking 비용으로 권장하지 않는다.
- **확장:** 입력을 N등분할 수 있으면 Partitioning. restartability를 유지한 채 수평 확장이 가능한 가장 일반적인 옵션.

### 핵심 코드 — 사용자 활동 로그 1억 건 적재

```java
@Configuration
@RequiredArgsConstructor
public class ActivityIngestJobConfig {

    private final JobRepository jobRepository;
    private final PlatformTransactionManager txm;
    private final DataSource sourceDataSource;
    private final DataSource targetDataSource;

    @Bean
    public Job activityIngestJob(Step ingestStep) {
        return new JobBuilder("activityIngestJob", jobRepository)
            .start(ingestStep)
            .build();
    }

    @Bean
    @StepScope
    public JdbcPagingItemReader<Activity> activityReader(
            @Value("#{jobParameters['targetDate']}") String targetDate) {

        SqlPagingQueryProviderFactoryBean queryProvider =
            new SqlPagingQueryProviderFactoryBean();
        queryProvider.setDataSource(sourceDataSource);
        queryProvider.setSelectClause("SELECT id, user_id, event_type, occurred_at");
        queryProvider.setFromClause("FROM raw_activity");
        queryProvider.setWhereClause("WHERE DATE(occurred_at) = :targetDate");
        queryProvider.setSortKey("id");

        return new JdbcPagingItemReaderBuilder<Activity>()
            .name("activityReader")
            .dataSource(sourceDataSource)
            .queryProvider(queryProvider.getObject())
            .parameterValues(Map.of("targetDate", targetDate))
            .pageSize(1000)
            .fetchSize(1000)
            .rowMapper(new ActivityRowMapper())
            .build();
    }

    @Bean
    public JdbcBatchItemWriter<Activity> activityWriter() {
        return new JdbcBatchItemWriterBuilder<Activity>()
            .dataSource(targetDataSource)
            .sql("""
                INSERT INTO activity_warehouse(id, user_id, event_type, occurred_at)
                VALUES (:id, :userId, :eventType, :occurredAt)
                ON CONFLICT (id) DO NOTHING
                """)
            .beanMapped()
            .build();
    }

    @Bean
    public Step ingestStep(JdbcPagingItemReader<Activity> reader,
                           JdbcBatchItemWriter<Activity> writer) {
        return new ChunkOrientedStepBuilder<Activity, Activity>(
                "ingestStep", jobRepository, 1000)
            .reader(reader)
            .writer(writer)
            .build();
    }
}
```

`ON CONFLICT (id) DO NOTHING`(PostgreSQL) 또는 `ON DUPLICATE KEY UPDATE`(MySQL)가 멱등성을 만들어준다. 같은 청크가 두 번 들어와도 같은 결과가 보장된다.

### 함정

- **chunk size = page size = (fetch size ≥ chunk size).** 셋이 어긋나면 N+1 SQL이 나거나 메모리가 폭증한다. 시작값은 1,000.
- **OFFSET 페이징.** 페이지 N이 100,000을 넘으면 DB가 앞 99,999 페이지를 매번 스캔한다. keyset 페이징(WHERE id > :lastId ORDER BY id LIMIT N)으로 옮기는 편이 낫다.

## A.2 ETL / 데이터 마이그레이션

### 언제 이 패턴인가

시스템 A → 시스템 B로 데이터를 옮기되, 변환·정합성 검증·실패 항목 격리가 필요한 일회성 또는 주기적 잡. 시스템 통합, 레거시 마이그레이션, 데이터 모델 재구성.

대용량 일괄 처리(A.1)와 비슷해 보이지만 결정적 차이가 둘 있다. 첫째, **데이터 정합성 검증이 1급 시민**이다. 둘째, **실패 항목을 끝에 격리**해야 한다 — 그냥 넘기면 안 되고, 누군가 후처리해야 한다.

대표 예: 신규 결제 시스템으로 이관, 회원 정보 통합, 주소 체계 표준화.

### Reader / Writer 결정

- **Reader:** A.1과 동일. 페이징 기반.
- **Processor:** 변환 + 검증 책임. 검증 실패 시 `null` 반환으로 필터링하지 말고, **별도 예외 throw + SkipListener로 격리**가 권장. null 필터링은 메트릭에 안 잡혀 사후 추적이 어렵다.
- **Writer:** UPSERT 패턴 또는 outbox + 별도 발행 잡 조합.
- **fault-tolerance:** retry는 일시 외부 의존만, skip은 데이터 결함만. 둘을 혼동하지 않기.

### 핵심 코드 — 회원 데이터 마이그레이션

```java
@Bean
public Step memberMigrationStep(JpaPagingItemReader<LegacyMember> reader,
                                MemberMigrationProcessor processor,
                                JdbcBatchItemWriter<NewMember> writer) {

    RetryPolicy retryPolicy = RetryPolicy.builder()
        .maxRetries(3)
        .includes(Set.of(TransientApiException.class))
        .build();

    SkipPolicy skipPolicy = new LimitCheckingExceptionHierarchySkipPolicy(
        Set.of(MemberValidationException.class), 1000);

    return new ChunkOrientedStepBuilder<LegacyMember, NewMember>(
            "memberMigrationStep", jobRepository, 500)
        .reader(reader)
        .processor(processor)
        .writer(writer)
        .faultTolerant()
        .retryPolicy(retryPolicy)
        .skipPolicy(skipPolicy)
        .listener(new MigrationFailureListener(failureRepository))
        .build();
}

@Component
public class MemberMigrationProcessor implements ItemProcessor<LegacyMember, NewMember> {

    @Override
    public NewMember process(LegacyMember legacy) {
        if (!isValidEmail(legacy.getEmail())) {
            throw new MemberValidationException(
                "Invalid email: " + legacy.getId());
        }
        if (!isValidPhone(legacy.getPhone())) {
            throw new MemberValidationException(
                "Invalid phone: " + legacy.getId());
        }
        return NewMember.builder()
            .legacyId(legacy.getId())
            .email(legacy.getEmail())
            .phone(normalizePhone(legacy.getPhone()))
            .migratedAt(LocalDateTime.now())
            .build();
    }
}

@Component
@RequiredArgsConstructor
public class MigrationFailureListener implements SkipListener<LegacyMember, NewMember> {

    private final MigrationFailureRepository failureRepository;

    @Override
    public void onSkipInProcess(LegacyMember item, Throwable t) {
        failureRepository.save(MigrationFailure.builder()
            .legacyId(item.getId())
            .reason(t.getMessage())
            .skippedAt(LocalDateTime.now())
            .build());
    }
}
```

핵심은 SkipListener다. **검증 실패 항목이 별도 테이블에 모이니까, 잡 종료 후 그 테이블을 SELECT해서 사람이 후처리할 수 있다.** 그냥 null 반환으로 필터링하면 어디로 사라졌는지 추적이 안 된다.

### 함정

- **마이그레이션 잡의 멱등성.** 한 번 실패해서 재실행할 때, 이미 옮긴 회원이 다시 옮겨지면 곤란하다. UPSERT 또는 `legacy_id` UNIQUE 제약 + ON CONFLICT.
- **외래 키 순서.** 회원 → 회원_주소 → 회원_결제수단 처럼 의존이 있을 때, 잡을 분리해 순서대로. 한 잡에 모든 걸 넣으면 트랜잭션이 길어져 lock 위험.

## A.3 통계·집계

### 언제 이 패턴인가

일말/시간 단위 거래량 집계, 사용자 활동 로그 일별 요약, 매출 통계 산출. **원본 데이터 → 집계 데이터** 흐름이 핵심.

Spring Batch의 Step 흐름과 ExecutionContext가 자연스럽게 어울리는 자리다. 단계가 명확하다 — (1) 원본 읽고 (2) 그룹별로 집계 (3) 집계 결과 INSERT.

대표 예: 일별 매출 통계, 시간당 사용자 활동 합계, 월말 통계 마감.

### Reader / Writer 결정

집계는 두 가지 모양으로 풀린다.

**모양 1 — DB에서 GROUP BY로 집계, 결과만 INSERT.** 데이터가 많고 집계 로직이 SQL로 표현 가능하면 이쪽이 압도적으로 빠르다.

```sql
INSERT INTO daily_sales(target_date, product_id, total_amount, order_count)
SELECT DATE(ordered_at) AS target_date, product_id,
       SUM(amount) AS total_amount, COUNT(*) AS order_count
FROM orders
WHERE DATE(ordered_at) = :targetDate
GROUP BY DATE(ordered_at), product_id;
```

이 자리에는 Spring Batch가 별 의미가 없다 — Tasklet 한 개로 SQL 한 방이면 된다.

**모양 2 — 코드에서 그룹별 누적, 청크 단위 flush.** 집계 로직이 복잡하거나 외부 데이터를 함께 봐야 하면 코드 집계가 필요하다. 이때 Spring Batch 모델이 자연스럽게 어울린다.

### 핵심 코드 — 사용자별 활동 점수 집계

```java
@Configuration
@RequiredArgsConstructor
public class ActivityScoreJobConfig {

    private final JobRepository jobRepository;
    private final PlatformTransactionManager txm;

    @Bean
    public Job activityScoreJob(Step scoreStep) {
        return new JobBuilder("activityScoreJob", jobRepository)
            .start(scoreStep)
            .build();
    }

    @Bean
    @StepScope
    public JdbcPagingItemReader<Activity> activityReader(
            @Value("#{jobParameters['targetDate']}") String targetDate,
            DataSource dataSource) {
        // ... A.1 패턴과 동일
    }

    @Bean
    public ItemProcessor<Activity, UserScoreDelta> scoreProcessor(
            ScoreCalculator calculator) {
        return activity -> calculator.delta(activity);
    }

    @Bean
    public ItemWriter<UserScoreDelta> scoreAccumulatingWriter(
            JdbcTemplate jdbcTemplate) {
        return chunk -> {
            // 청크 안에서 user_id로 그룹화 후, IN 절로 한 번에 누적 UPDATE
            Map<Long, Long> aggregated = chunk.getItems().stream()
                .collect(Collectors.groupingBy(
                    UserScoreDelta::userId,
                    Collectors.summingLong(UserScoreDelta::delta)));

            for (Map.Entry<Long, Long> entry : aggregated.entrySet()) {
                jdbcTemplate.update("""
                    INSERT INTO user_score(user_id, score)
                    VALUES (?, ?)
                    ON CONFLICT (user_id) DO UPDATE SET score = user_score.score + ?
                    """,
                    entry.getKey(), entry.getValue(), entry.getValue());
            }
        };
    }

    @Bean
    public Step scoreStep(JdbcPagingItemReader<Activity> reader,
                          ItemProcessor<Activity, UserScoreDelta> processor,
                          ItemWriter<UserScoreDelta> writer) {
        return new ChunkOrientedStepBuilder<Activity, UserScoreDelta>(
                "scoreStep", jobRepository, 1000)
            .reader(reader)
            .processor(processor)
            .writer(writer)
            .build();
    }
}
```

**청크 안에서 그룹화 후 IN UPDATE**가 핵심이다. 1,000건의 INSERT/UPDATE가 청크당 사용자 수(보통 수백 명)로 줄어든다. 6장에서 본 카카오페이의 "동일 값 UPDATE 그룹화"와 같은 결의 패턴이다.

### 함정

- **재실행 시 누적 중복.** 잡을 두 번 돌리면 score가 두 번 더해진다. JobInstance 식별자(`targetDate`) + UNIQUE 제약 + 멱등 처리가 필요. 또는 잡 시작 시 해당 날짜의 누적을 먼저 0으로 리셋하는 prerequisite step 추가.
- **메모리 폭주.** 청크 안에서 그룹화하지 않고 잡 전체에서 그룹화하려는 시도가 흔한 함정. 1억 건을 다 들고 있으면 OOM. **청크 단위 그룹화 + DB UPSERT 누적**이 정석.

## A.4 파일 ETL — 우아한형제들 주소 DB 패턴

### 언제 이 패턴인가

플랫 파일·CSV·JSON·XML 입력 → 검증 → DB/S3/Kafka 출력. 외부 시스템에서 받은 파일을 자기 시스템으로 가져오거나, 자기 시스템 데이터를 외부로 내보낼 때.

우아한형제들의 "주소 DB 구축" 사례가 한국 자료의 대표다 — 행정안전부에서 받는 주소 텍스트 파일을 정기적으로 자기 DB에 반영하는 패턴.

대표 예: 행정구역 주소 갱신, 외부 카탈로그 일괄 가져오기, 정산 결과 외부 시스템으로 내보내기.

### Reader / Writer 결정

- **CSV/TSV:** `FlatFileItemReader` + `DelimitedLineTokenizer`. 한국 자료에서 인코딩(EUC-KR)이 자주 함정.
- **JSON 라인(NDJSON):** `JsonItemReader`.
- **XML:** `StaxEventItemReader`. 큰 XML 파일을 streaming으로 읽는다.
- **Writer:** DB라면 `JdbcBatchItemWriter`. 파일 출력은 `FlatFileItemWriter` / `JsonFileItemWriter`.
- **압축 파일:** `Tasklet`으로 먼저 풀고, chunk-oriented step에서 처리. 4장에서 본 tasklet의 1할 자리.

### 핵심 코드 — 행정구역 주소 파일 적재

```java
@Configuration
@RequiredArgsConstructor
public class AddressIngestJobConfig {

    private final JobRepository jobRepository;
    private final PlatformTransactionManager txm;
    private final DataSource dataSource;

    @Bean
    public Job addressIngestJob(Step unzipStep, Step ingestStep) {
        return new JobBuilder("addressIngestJob", jobRepository)
            .start(unzipStep)
            .next(ingestStep)
            .build();
    }

    // Step 1 — 압축 해제 (tasklet)
    @Bean
    public Step unzipStep() {
        return new StepBuilder("unzipStep", jobRepository)
            .tasklet((contribution, chunkContext) -> {
                String zipPath = (String) chunkContext.getStepContext()
                    .getJobParameters().get("zipPath");
                String extractDir = (String) chunkContext.getStepContext()
                    .getJobParameters().get("extractDir");
                ZipUtils.unzip(zipPath, extractDir);
                return RepeatStatus.FINISHED;
            }, txm)
            .build();
    }

    // Step 2 — 청크로 파일 적재
    @Bean
    @StepScope
    public FlatFileItemReader<AddressLine> addressReader(
            @Value("#{jobParameters['extractDir']}") String extractDir) {

        return new FlatFileItemReaderBuilder<AddressLine>()
            .name("addressReader")
            .resource(new FileSystemResource(extractDir + "/address.txt"))
            .encoding("EUC-KR")
            .delimited(c -> c.delimiter("|").quoteCharacter('"'))
            .names("zipCode", "sido", "sigungu", "roadName", "buildingNumber", "addressName")
            .targetType(AddressLine.class)
            .linesToSkip(1)
            .build();
    }

    @Bean
    public JdbcBatchItemWriter<AddressLine> addressWriter() {
        return new JdbcBatchItemWriterBuilder<AddressLine>()
            .dataSource(dataSource)
            .sql("""
                INSERT INTO address(zip_code, sido, sigungu, road_name,
                                    building_number, address_name)
                VALUES (:zipCode, :sido, :sigungu, :roadName,
                        :buildingNumber, :addressName)
                ON CONFLICT (zip_code, road_name, building_number) DO UPDATE SET
                    sido = EXCLUDED.sido,
                    sigungu = EXCLUDED.sigungu,
                    address_name = EXCLUDED.address_name
                """)
            .beanMapped()
            .build();
    }

    @Bean
    public Step ingestStep(FlatFileItemReader<AddressLine> reader,
                           JdbcBatchItemWriter<AddressLine> writer) {
        return new ChunkOrientedStepBuilder<AddressLine, AddressLine>(
                "ingestStep", jobRepository, 1000)
            .reader(reader)
            .writer(writer)
            .faultTolerant()
            .skipPolicy(new LimitCheckingExceptionHierarchySkipPolicy(
                Set.of(FlatFileParseException.class), 100))
            .build();
    }
}
```

두 가지 패턴이 한 잡에 들어 있다. **첫 스텝은 tasklet(파일 압축 해제), 둘째 스텝은 chunk-oriented(라인 단위 적재).** 4장에서 본 tasklet과 chunk-oriented의 짝짓기 패턴이 자연스럽게 풀린다.

### 함정

- **인코딩.** 한국 정부·공공기관 파일은 거의 EUC-KR. UTF-8로 가정하면 한글이 깨진다. `encoding("EUC-KR")` 명시 필수.
- **헤더 라인.** `linesToSkip(1)` 빼먹으면 헤더가 데이터로 들어가서 첫 청크가 통째로 skip된다.
- **파일 부분 적재 후 실패.** 청크 트랜잭션이 보장하지만, **중복 처리 방지는 UPSERT가 책임**. ON CONFLICT가 없으면 재실행 시 PK 충돌로 잡이 안 돈다.

## A.5 알림 발송

### 언제 이 패턴인가

푸시 알림, 이메일, SMS를 대량으로 발송하는 잡. 정해진 시각에 캠페인 푸시, 결제 완료 이메일 일괄 발송, 일일 알림 묶음 발송.

이 패턴이 까다로운 이유는 단 하나다. **외부 시스템에 부수효과가 있다.** 잡이 한 번 실패해서 재실행하면 같은 사용자에게 같은 알림이 두 번 갈 수 있다. 7장에서 다룬 outbox / 멱등 키 / dedupe 저장소가 진가를 발휘하는 자리다.

### Reader / Writer 결정

- **Reader:** A.1 패턴 (대상자 페이징).
- **Writer:** **외부 API를 직접 호출하지 말고**, outbox 테이블에 INSERT한다. 도메인 트랜잭션과 같은 트랜잭션에 outbox 행을 박는다. 별도 발행 워커가 outbox를 폴링해 외부에 발송.
- **멱등 키:** outbox 테이블의 `idempotency_key` 컬럼에 (대상자 ID, 알림 종류, 캠페인 ID) 같은 식별자를 박는다. UNIQUE 제약. 같은 키가 두 번 들어오면 INSERT가 실패하므로 자연스럽게 dedup.

### 핵심 코드 — 캠페인 푸시 outbox

```java
@Bean
public Step pushOutboxStep(JdbcPagingItemReader<TargetUser> reader,
                           PushPayloadProcessor processor,
                           JdbcBatchItemWriter<PushOutbox> writer) {
    return new ChunkOrientedStepBuilder<TargetUser, PushOutbox>(
            "pushOutboxStep", jobRepository, 500)
        .reader(reader)
        .processor(processor)
        .writer(writer)
        .build();
}

@Component
@RequiredArgsConstructor
@StepScope
public class PushPayloadProcessor implements ItemProcessor<TargetUser, PushOutbox> {

    @Value("#{jobParameters['campaignId']}")
    private String campaignId;

    @Override
    public PushOutbox process(TargetUser user) {
        return PushOutbox.builder()
            .idempotencyKey(campaignId + ":" + user.getId())
            .userId(user.getId())
            .deviceToken(user.getDeviceToken())
            .title(buildTitle(campaignId))
            .body(buildBody(campaignId, user))
            .createdAt(LocalDateTime.now())
            .status(PushStatus.PENDING)
            .build();
    }
}

@Bean
public JdbcBatchItemWriter<PushOutbox> pushOutboxWriter(DataSource dataSource) {
    return new JdbcBatchItemWriterBuilder<PushOutbox>()
        .dataSource(dataSource)
        .sql("""
            INSERT INTO push_outbox(idempotency_key, user_id, device_token,
                                    title, body, status, created_at)
            VALUES (:idempotencyKey, :userId, :deviceToken,
                    :title, :body, :status, :createdAt)
            ON CONFLICT (idempotency_key) DO NOTHING
            """)
        .beanMapped()
        .build();
}
```

이 잡이 끝나면 outbox 테이블에 PENDING 상태 푸시가 쌓인다. 별도 워커(또는 잡)가 outbox를 폴링해 FCM/APNs로 보내고, 성공하면 SENT로 마킹. 실패하면 backoff 후 재시도.

**왜 outbox로 분리하는가?** 잡이 청크 트랜잭션 안에서 외부 API를 직접 호출하면, 청크가 롤백될 때 외부 호출을 되돌릴 수 없다. outbox로 분리하면 도메인 트랜잭션은 안전하게 롤백되고, 외부 발송은 별도 워커가 멱등 키로 dedup하면서 책임진다.

### 함정

- **outbox 테이블 누적.** SENT 상태 행이 영구 누적되면 테이블이 무거워진다. 보존 기간 정리 잡 필요(10장).
- **outbox 워커가 사라지면 알림이 안 간다.** outbox는 잡과 워커의 짝이 맞아야 의미 있다. 워커 monitoring을 함께.
- **idempotency_key 설계.** 캠페인 ID만으로는 부족하다 — 같은 캠페인을 두 디바이스에 보내야 할 수 있다. (campaign_id, user_id) 또는 (campaign_id, device_token) 같은 복합 키.

## 마무리

5개 패턴을 한 카탈로그로 묶어보면, 결국 같은 모양이 반복된다는 사실이 보인다. 페이징 Reader + JdbcBatchItemWriter + UPSERT 멱등 + 청크 단위 트랜잭션 + 검증 실패는 SkipListener로 격리. **이 묶음이 production-ready 잡의 골격이다.** 자기 도메인이 어디에 가까운지를 골라, 그 자리에서 출발하면 된다.

| 유스케이스 | Reader | Writer | 핵심 패턴 |
|---|---|---|---|
| A.1 대용량 일괄 처리 | JdbcPaging / Querydsl | JdbcBatch | UPSERT + 파티셔닝 |
| A.2 ETL / 마이그레이션 | JdbcPaging / JpaPaging | JdbcBatch + UPSERT | SkipListener로 실패 격리 |
| A.3 통계·집계 | JdbcPaging | 청크 그룹화 후 IN UPDATE | 멱등 + 누적 리셋 prerequisite |
| A.4 파일 ETL | FlatFile / Json / Stax | JdbcBatch | tasklet(압축 해제) + 청크 step |
| A.5 알림 발송 | JdbcPaging | outbox 테이블 INSERT | 멱등 키 + 별도 워커 |

이 표를 책상에 붙여두자. 새 잡 설계의 1단계가 30초로 줄어든다.
