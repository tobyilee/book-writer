# 11장. Spring Batch 5에서 6으로 — 마이그레이션 실전

팀에 이런 소식이 들어왔다고 해보자. "6.0 GA가 나왔다더라. graceful shutdown이 들어왔고, recover()도 정식 API로 박혔대." 솔깃하다. K8s 운영을 1년쯤 해본 입장에서는 그 두 가지가 어떤 의미인지 신체적으로 안다. 그런데 흥분과 동시에 부담이 따라온다 — **우리는 5.x로 운영 중이다.** 새 기능은 끌리는데, 마이그레이션 비용을 모르겠다. 진행 중인 잡들은 어떻게 옮겨야 하나? 메타 테이블은? 직렬화는? 코드 변경 면적은?

그 질문에 정직하게 답하는 일이 이번 장의 목적이다. "그냥 의존성만 올리면 된다"는 거짓말 대신, 어떤 변화가 있고, 어디가 무겁고, 어디는 가벼운지를 코드 diff로 풀어보자. 한 잡을 골라 5.x → 6.0 마이그레이션을 4~5단계 시나리오로 따라가본 뒤, 메타 정합성 검증 SQL과 단계 실패 시의 롤백 시나리오까지 한 호흡에 짚는다.

미리 한 줄로 압축하면 이렇다. **마이그레이션의 90%는 패키지 import 정리와 JobLauncher → JobOperator 전환이고, 나머지 10%가 진짜 함정이다.** 그 10%가 직렬화 호환성과 도메인 모델 record화에 숨어 있다. 큰 것부터 짚어가자.

## 11.1 마이그레이션 전 체크리스트 — 이것부터 맞추자

마이그레이션을 시작하기 전에 환경 baseline 4개를 먼저 맞춰야 한다. 이게 안 맞으면 의존성 해결 단계에서 빨간불이 줄줄이 켜진다.

| 항목 | 5.x baseline | 6.0 baseline |
|---|---|---|
| Java | 17+ | 17+ (변동 없음) |
| Spring Framework | 6.x | **7.0** |
| Spring Boot | 3.x | **4.0** |
| Spring Data | 3.x | **4.0** |
| Spring Integration | 6.x | **7.0** |
| Micrometer | 1.12+ | **1.16** |
| Jackson | 2.x | **3.x** (2.x deprecated) |

**Java 버전은 변동이 없다.** 이게 다행이다 — 5에서 이미 17을 쓰고 있었다면 추가 부담이 없다. 진짜 부담은 Spring Framework 7과 Spring Boot 4, 그리고 **Jackson 3**이다.

Jackson 3은 2.x와 패키지가 완전히 분리된다(`com.fasterxml.jackson` → `tools.jackson`). 직접 작성한 ObjectMapper 설정, 커스텀 (De)Serializer, Module 등록 코드가 영향을 받는다. 다행히 Spring Boot 4가 자동 구성을 잘 해주니 평균적인 사용처에서는 영향이 작은데, 직접 ObjectMapper를 빈으로 주입해 쓰던 코드가 있으면 한 번 훑어보자.

Spring Boot 4는 GA가 비교적 최근이라 production 사용기가 아직 두텁지 않다. 운영 안정성이 걱정된다면 Spring Boot 4의 첫 메이너 패치(4.0.x) 한 두 번을 기다리는 것도 합리적인 판단이다. 하네스 자체의 CVE/패치 수명도 있으니, "최신을 무조건 따라가야 한다"는 부담을 잠시 내려두는 편이 낫다.

### 11.1.1 진행 중인 JobInstance를 비우고 올린다

여기가 첫 번째 진짜 함정이다. 5.x 메타에 STARTED 상태로 남아있는 JobInstance, 또는 5.x에서 실패한 채 재시작 대기 중인 JobInstance가 있으면 — **그건 6에서 재시작 불가능하다.**

이유는 5장에서 짚은 그 변경에서 온다. JobParameters가 record로 재설계되고, ExecutionContext의 직렬화 포맷이 바뀌었다. 5에서 직렬화된 ExecutionContext byte를 6에서 읽으면 deserialize가 깨진다. 즉, **5에서 진행 중이던 잡은 5에서 끝낸 다음 6으로 올리는 게 정석**이다.

마이그레이션 직전에 이 검증을 SQL로 한 번 돌려보자.

```sql
-- 진행 중 또는 미완 JobExecution 확인
SELECT
    JOB_EXECUTION_ID,
    JOB_INSTANCE_ID,
    STATUS,
    EXIT_CODE,
    START_TIME,
    END_TIME,
    LAST_UPDATED
FROM BATCH_JOB_EXECUTION
WHERE STATUS IN ('STARTED', 'STARTING', 'STOPPING')
   OR (STATUS = 'FAILED' AND END_TIME IS NULL);
```

이 쿼리에 결과가 나오면 마이그레이션 대상에 포함된다. 다음 중 하나를 선택해야 한다.

- **A안 — 5에서 자연 종료를 기다린다.** 잡이 짧으면 가장 깔끔하다.
- **B안 — 5에서 recover 또는 abandon 처리한다.** `JobOperator#abandon`(5.x에 이미 있다)으로 STARTED를 ABANDONED로 마킹.
- **C안 — 6 메타를 fresh DB로 시작한다.** 메타를 비우고 운영 이력을 한 번 끊는 강한 선택. 이력 손실이 있다.

대부분의 운영 환경에선 A나 B를 쓴다. C를 고른 적이 있다면, 메타 보존 기간을 마이그레이션 전에 일부러 한 번 더 짧게 잡아 누적된 메타 양을 줄여둔 뒤 가는 게 보통이다.

## 11.2 패키지 이동 정리 — 가장 면적이 큰 변경

마이그레이션 작업 시간의 가장 큰 비중을 차지하는 건, 의외로 단순 노동에 가까운 패키지 import 정리다. 6.0은 패키지 구조를 한 차례 정리했다. 대표적인 이동을 표로 보자.

| 5.x 위치 | 6.0 위치 |
|---|---|
| `org.springframework.batch.*` (인프라류) | `org.springframework.batch.infrastructure.*` |
| `org.springframework.batch.core.explore.*` | `org.springframework.batch.core.repository.explore.*` |
| `org.springframework.batch.core.partition.support.*` | `org.springframework.batch.core.partition.*` |
| `JobRepositoryFactoryBean` | `JdbcJobRepositoryFactoryBean` |
| `JobExplorerFactoryBean` | `JdbcJobExplorerFactoryBean` |
| `ChunkHandler` | `ChunkRequestHandler` |

다행히 IDE의 "Optimize Imports" + 컴파일 오류 따라가기로 80%는 자동 해결된다. 패키지 변경만 하면 클래스명과 시그니처가 같은 경우가 많다. IntelliJ에서는 Find/Replace에 정규식을 쓰면 더 빠르다.

```
# Find:
org\.springframework\.batch\.item\.(\w+)\.

# Replace:
org.springframework.batch.infrastructure.item.$1.
```

다만 자동 변환이 안 되는 자리가 몇 개 있다. 다음을 짚어두자.

**`JobStep.setJobLauncher` → `setJobOperator`.** Step 내부에서 다른 잡을 호출하는 JobStep을 쓴 코드가 있다면, setter 이름이 바뀌었다.

**시퀀스 이름 변경.** DB 스키마 영향이라 코드 변경만으론 안 된다. 11.5에서 따로 다룬다.

**`@EnableBatchProcessing(modular = true)` deprecated.** 단순 import 변경이 아니라 구조 재설계라 11.4에서 따로 다룬다.

이 셋만 따로 의식하고, 나머지는 IDE에 맡기자. 컴파일이 통과하기 시작하면 1차 작업이 끝난 셈이다.

## 11.3 JobLauncher / JobExplorer 주입을 JobOperator로 전환

Spring Batch 6은 인터페이스를 통합했다. `JobLauncher`/`JobExplorer` 빈을 따로 등록할 필요가 없다 — `JobOperator` 하나가 launch + explore + control + recover를 다 한다.

운영 코드에서 가장 자주 보이는 패턴은 다음이다.

```java
// 5.x — Before
@Service
@RequiredArgsConstructor
public class SettlementJobLauncher {

    private final JobLauncher jobLauncher;
    private final JobExplorer jobExplorer;
    private final Job settlementJob;

    public void launch(LocalDate targetDate) throws Exception {
        JobParameters params = new JobParametersBuilder()
            .addString("targetDate", targetDate.toString())
            .toJobParameters();

        Set<JobExecution> running = jobExplorer.findRunningJobExecutions("settlementJob");
        if (!running.isEmpty()) {
            throw new IllegalStateException("Already running");
        }

        jobLauncher.run(settlementJob, params);
    }
}
```

```java
// 6.0 — After
@Service
@RequiredArgsConstructor
public class SettlementJobLauncher {

    private final JobOperator jobOperator;
    private final Job settlementJob;

    public void launch(LocalDate targetDate) throws Exception {
        JobParameters params = new JobParametersBuilder()
            .addString("targetDate", targetDate.toString())
            .toJobParameters();

        Set<Long> running = jobOperator.getRunningExecutions("settlementJob");
        if (!running.isEmpty()) {
            throw new IllegalStateException("Already running");
        }

        jobOperator.start(settlementJob, params);
    }
}
```

차이점 정리.

- `JobLauncher` + `JobExplorer` → `JobOperator` 하나
- `jobLauncher.run(job, params)` → `jobOperator.start(job, params)`
- `jobExplorer.findRunningJobExecutions(name)` → `jobOperator.getRunningExecutions(name)` (반환 타입은 `Set<Long>`)

반환 타입이 `Set<JobExecution>`에서 `Set<Long>`로 바뀐 건 작은 차이지만, JobExecution 객체가 필요한 곳에서는 `jobRepository.getJobExecution(id)`로 한 번 더 조회해야 한다. 이걸 놓치면 NPE가 떠서 알아채게 된다.

10장의 recover 워크플로우도 자연스럽게 같은 빈으로 풀린다. 같은 `JobOperator` 한 개에서 `start` / `stop` / `restart` / `recover` / `getRunningExecutions`가 다 나온다. 빈 의존성이 줄어든다는 단순한 사실이 운영 코드의 가독성을 꽤 높인다.

## 11.4 `@EnableBatchProcessing` 분리 — 공통 + Store-specific

5.x까지 `@EnableBatchProcessing` 한 개가 모든 인프라를 들고 있었다. 6에서는 두 갈래로 갈라진다.

- `@EnableBatchProcessing` → **공통** 인프라 속성만 (taskExecutor 등)
- `@EnableJdbcJobRepository(dataSourceRef=…, transactionManagerRef=…)` → JDBC 저장소
- `@EnableMongoJobRepository(...)` → MongoDB 저장소

마이그레이션 코드 diff가 이렇다.

```java
// 5.x — Before
@Configuration
@EnableBatchProcessing
public class BatchConfig {
    // ...
}
```

```java
// 6.0 — After
@Configuration
@EnableBatchProcessing
@EnableJdbcJobRepository(
    dataSourceRef = "batchDataSource",
    transactionManagerRef = "batchTransactionManager"
)
public class BatchConfig {
    // ...
}
```

저장소 어노테이션이 한 줄 추가된다. **Spring Boot 4 자동 구성을 쓰는 평균 사용처에서는 이 어노테이션조차 필요 없다.** Boot가 기본 DataSource로 자동으로 JDBC JobRepository를 구성해준다. 직접 데이터소스를 두 개 이상 쓰거나, 메타용 데이터소스를 비즈니스용과 분리하는 환경에서만 명시한다.

### 11.4.1 modular=true의 deprecation

`@EnableBatchProcessing(modular = true)`는 deprecated다. 잡마다 별도 ApplicationContext를 두는 패턴이었는데, 6에서는 Spring 컨텍스트 계층 + `GroupAwareJob`을 쓰라는 권고로 바뀌었다.

이 옵션을 안 쓰고 있었다면 무시해도 된다. 만약 쓰고 있었다면, 6 마이그레이션 시점에 컨텍스트 계층 구조로 옮기는 작업을 별도로 잡아야 한다. 단순 어노테이션 변경이 아니라 설계 변경이라, 시간이 걸린다.

```java
// modular=true 패턴 (deprecated)
@Configuration
@EnableBatchProcessing(modular = true)
public class ParentBatchConfig {
    @Bean
    public ApplicationContextFactory jobAContext() {
        return new GenericApplicationContextFactory(JobAConfig.class);
    }
}
```

```java
// 6.0 권고 — 컨텍스트 계층 + GroupAwareJob
@Configuration
@EnableBatchProcessing
public class ParentBatchConfig {
    @Bean
    public Job jobA(JobRepository jobRepository, ...) {
        return new GroupAwareJob("groupA",
            new JobBuilder("jobA", jobRepository).start(...).build());
    }
}
```

이 deprecation은 운영 면에서는 큰 영향이 없는 자리지만, 5.x에서 modular 패턴을 적극적으로 썼다면 마이그레이션 일정에 별도 라인 한 개를 두는 편이 안전하다.

## 11.5 DB 스키마 변경 — 시퀀스 이름

6.0은 메타 스키마의 시퀀스 이름을 변경했다. 영향 범위가 크진 않지만, **DB 스키마를 자동 마이그레이션하는 도구(Flyway, Liquibase)에 신경 써야 하는 자리**다.

| 5.x 시퀀스 | 6.0 시퀀스 |
|---|---|
| `BATCH_JOB_SEQ` | `BATCH_JOB_INSTANCE_SEQ` |
| `BATCH_JOB_EXECUTION_SEQ` | `BATCH_JOB_EXECUTION_SEQ` (변동 없음) |
| `BATCH_STEP_EXECUTION_SEQ` | `BATCH_STEP_EXECUTION_SEQ` (변동 없음) |

`BATCH_JOB_SEQ` 하나만 이름이 바뀌었다. 이 시퀀스의 현재 값을 새 시퀀스로 옮긴 뒤 옛 시퀀스를 드롭하는 작업이 필요하다.

### 11.5.1 PostgreSQL Flyway 마이그레이션 SQL

```sql
-- V20260509__rename_batch_job_seq.sql

-- 1. 현재 값 가져오기
DO $$
DECLARE
    current_value BIGINT;
BEGIN
    SELECT last_value INTO current_value FROM BATCH_JOB_SEQ;

    -- 2. 새 시퀀스 생성 (현재 값 + 1부터 시작)
    EXECUTE format(
        'CREATE SEQUENCE IF NOT EXISTS BATCH_JOB_INSTANCE_SEQ START WITH %s INCREMENT BY 1',
        current_value + 1
    );

    -- 3. 옛 시퀀스 드롭
    DROP SEQUENCE IF EXISTS BATCH_JOB_SEQ;
END $$;
```

### 11.5.2 검증 SQL

마이그레이션 직후 다음 검증을 돌린다.

```sql
-- 새 시퀀스가 존재하는지
SELECT sequence_name, last_value
FROM information_schema.sequences
WHERE sequence_name = 'batch_job_instance_seq';

-- 옛 시퀀스가 사라졌는지
SELECT sequence_name
FROM information_schema.sequences
WHERE sequence_name = 'batch_job_seq';
-- (결과가 0행이어야 함)
```

MySQL이나 다른 DB는 시퀀스 자체가 없거나 표현이 다르다. 자동 증가 컬럼 또는 `BATCH_JOB_SEQ` 같은 단일 행 테이블로 구현돼 있을 수 있으니, 환경에 맞춰 조정해야 한다. Spring Batch 공식 스키마 SQL이 `org/springframework/batch/core/schema-{db}.sql` 형태로 들어 있으니, 6.0 jar 안의 그 파일을 5.x 버전과 diff 떠보면 정확한 변경 면적이 보인다.

## 11.6 fault-tolerance 코드 재작성 — Spring Retry → Spring Framework 7 retry

5.x에서는 fault tolerance를 위해 별도의 Spring Retry 라이브러리(`org.springframework.retry`)에 의존했다. 6.0은 이 의존을 떼고, **Spring Framework 7의 retry 기능 위로** 이전했다. 의존성 한 개가 줄고, API가 살짝 바뀐다.

```java
// 5.x — Before
@Bean
public Step step(JobRepository jobRepository, PlatformTransactionManager txm,
                 ItemReader<Order> reader, ItemWriter<Order> writer) {
    return new StepBuilder("settleStep", jobRepository)
        .<Order, Order>chunk(500, txm)
        .reader(reader)
        .writer(writer)
        .faultTolerant()
        .retryLimit(3)
        .retry(TransientApiException.class)
        .skipLimit(50)
        .skip(FlatFileParseException.class)
        .build();
}
```

```java
// 6.0 — After
@Bean
public Step step(JobRepository jobRepository, PlatformTransactionManager txm,
                 ItemReader<Order> reader, ItemWriter<Order> writer) {

    RetryPolicy retryPolicy = RetryPolicy.builder()
        .maxRetries(3)
        .includes(Set.of(TransientApiException.class))
        .build();

    SkipPolicy skipPolicy = new LimitCheckingExceptionHierarchySkipPolicy(
        Set.of(FlatFileParseException.class), 50);

    return new ChunkOrientedStepBuilder<Order, Order>("settleStep", jobRepository, 500)
        .reader(reader)
        .writer(writer)
        .faultTolerant()
        .retryPolicy(retryPolicy)
        .skipPolicy(skipPolicy)
        .build();
}
```

차이점.

- `StepBuilder` → `ChunkOrientedStepBuilder` (이게 5장에서 짚은 메이저 변경의 운영 자리다)
- `chunk(500, txm)` 대신 빌더 생성자 인자에 chunk size, txm은 빌더 파라미터로 자동 주입
- `.retryLimit(N).retry(Exception.class)` → `RetryPolicy.builder()`로 명시적 객체 구성
- `.skipLimit(N).skip(Exception.class)` → `SkipPolicy` 객체 명시적 구성

빌더 호출의 면적은 비슷하지만, retry/skip 정책이 별개의 객체로 분리되니 **테스트 코드에서 정책 단독 검증이 가능**하다는 부수 효과가 있다. 정책의 단위 테스트를 따로 짤 수 있게 된 셈이다.

### 11.6.1 ChunkOrientedTasklet의 deprecation

5.x의 `ChunkOrientedTasklet` + `TaskletStep` 조합은 6에서 deprecated다. 직접 그 클래스를 import해 쓰던 코드가 있다면 `ChunkOrientedStep` + `ChunkOrientedStepBuilder`로 옮긴다. 일반 사용자는 거의 만지지 않는 자리지만, 커스텀 Step을 직접 짠 코드라면 영향이 크다.

```java
// 5.x — Before (이제 deprecated)
ChunkOrientedTasklet<Order> tasklet = new ChunkOrientedTasklet<>(chunkProvider, chunkProcessor);
TaskletStep step = new TaskletStep("step");
step.setTasklet(tasklet);
// ...
```

```java
// 6.0 — After
ChunkOrientedStep<Order, Order> step = new ChunkOrientedStepBuilder<Order, Order>(
    "step", jobRepository, 500)
    .reader(reader)
    .processor(processor)
    .writer(writer)
    .build();
```

이 변경이 5장에서 본 "왜 갈아엎었나"의 운영 귀결이다. 6의 producer-consumer + bounded queue 모델은 이전 모델의 maxItemCount/throttle/optimistic locking 이슈를 푼 자리이고, 그 모델 변경이 빌더 API에도 반영됐다.

## 11.7 도메인 모델 영향 — primitive long과 record화

여기가 마이그레이션의 두 번째 진짜 함정이다. 5장에서 짚은 도메인 모델 변경 — JobInstance/JobExecution의 ID가 `Long`에서 `long`으로, JobParameter가 record로 — 이 변경이 일반 비즈니스 코드에는 영향이 적은데, **커스텀 Listener나 ExecutionContext에 도메인 객체를 직접 저장한 코드**에는 영향이 크다.

### 11.7.1 ID 박싱 NPE 위험

```java
// 5.x — Before
@Component
public class AuditListener implements JobExecutionListener {

    @Override
    public void afterJob(JobExecution jobExecution) {
        Long jobInstanceId = jobExecution.getJobInstance().getId();
        if (jobInstanceId != null) {
            auditRepository.save(new Audit(jobInstanceId, jobExecution.getStatus()));
        }
    }
}
```

```java
// 6.0 — After
@Component
public class AuditListener implements JobExecutionListener {

    @Override
    public void afterJob(JobExecution jobExecution) {
        long jobInstanceId = jobExecution.getJobInstance().getId();
        // null 체크 의미가 사라짐. 0이 "미할당" 표시
        if (jobInstanceId != 0) {
            auditRepository.save(new Audit(jobInstanceId, jobExecution.getStatus()));
        }
    }
}
```

`getId()` 반환이 `Long` → `long`으로 바뀌었다. 박싱 NPE가 사라지지만, **null 체크 로직이 0 비교로 바뀐다.** 코드 의미는 비슷하지만 수정이 필요하다. IDE가 컴파일 오류로 알려주는 자리는 아니라(unboxing은 자동), 정적 분석 도구로 한 번 훑어보는 편이 안전하다.

### 11.7.2 JobParameter record화

JobParameter가 record로 바뀌면서 직접 빌드하던 코드가 영향을 받는다.

```java
// 5.x — Before
JobParameter param = new JobParameter("2026-05-08", String.class, true);
```

```java
// 6.0 — After
JobParameter<String> param = new JobParameter<>("2026-05-08", String.class, true);
```

표면은 거의 같지만 제네릭이 추가됐다. record 시그니처가 `record JobParameter<T>(T value, Class<T> type, boolean identifying)`로 바뀐 결과다. 대부분의 사용자는 `JobParametersBuilder`를 거쳐 쓰니 직접 만들 일이 적은데, 직접 만들던 곳이 있다면 제네릭 추가가 필요하다.

JobParameters 자체는 `Map<String, JobParameter>`에서 `Set<JobParameter>` 기반으로 바뀌었지만, 외부 API(`getString`, `getLong` 등)는 거의 동일해서 일반 사용자는 거의 영향 없다.

### 11.7.3 ExecutionContext 직렬화 호환성 검증

5에서 6으로 올린 직후 ExecutionContext가 멀쩡한지 검증하는 절차가 필요하다. 11.1.1에서 짚은 "진행 중 잡을 비우고 올린다"가 첫 번째 안전 장치고, 그 다음에 신규 잡으로 ExecutionContext를 한 번 끝까지 도는 시나리오를 확인하는 게 두 번째 안전 장치다.

검증 SQL.

```sql
-- ExecutionContext byte 컬럼이 비어있지 않고 정상 deserialize 되는지
-- (코드에서 한 번 읽어보는 게 가장 확실. SQL은 비정상 byte만 1차 검출)
SELECT
    JOB_EXECUTION_ID,
    LENGTH(SERIALIZED_CONTEXT) AS context_bytes,
    LENGTH(SHORT_CONTEXT) AS short_bytes
FROM BATCH_JOB_EXECUTION_CONTEXT
WHERE SERIALIZED_CONTEXT IS NOT NULL
ORDER BY JOB_EXECUTION_ID DESC
LIMIT 20;
```

여기서 `LENGTH`가 너무 크면(예: 수 MB) 5.x에서 누가 ExecutionContext에 큰 객체를 부주의하게 박았을 가능성이 있다. 이게 6.0의 새 직렬화 포맷에서 deserialize 깨질 위험 자리다. 마이그레이션 직전에 한 번 훑어두는 편이 낫다.

## 11.8 잡 한 개의 실제 마이그레이션 시나리오 — 4단계 코드 diff

여기까지 카탈로그를 펼쳤으니, 이제 실제 잡 한 개를 골라 단계별로 마이그레이션하는 시나리오를 풀어보자. 가상의 정산 잡 `settlementJob` 한 개를 고르고, 4단계로 옮긴다. 각 단계마다 메타 정합성 검증과 롤백 시나리오가 따라간다.

### 11.8.1 Stage 0 — 마이그레이션 전 상태

5.x로 운영 중인 잡의 코드와 환경.

```java
// 5.x
@Configuration
@EnableBatchProcessing
@RequiredArgsConstructor
public class SettlementJobConfig {

    private final JobRepository jobRepository;
    private final PlatformTransactionManager txm;

    @Bean
    public Job settlementJob(Step settlementStep) {
        return new JobBuilder("settlementJob", jobRepository)
            .start(settlementStep)
            .build();
    }

    @Bean
    public Step settlementStep(ItemReader<Order> orderReader,
                               ItemProcessor<Order, Settlement> processor,
                               ItemWriter<Settlement> writer) {
        return new StepBuilder("settlementStep", jobRepository)
            .<Order, Settlement>chunk(500, txm)
            .reader(orderReader)
            .processor(processor)
            .writer(writer)
            .faultTolerant()
            .retryLimit(3)
            .retry(TransientApiException.class)
            .skipLimit(50)
            .skip(FlatFileParseException.class)
            .build();
    }
}

@Service
@RequiredArgsConstructor
public class SettlementLauncher {
    private final JobLauncher jobLauncher;
    private final JobExplorer jobExplorer;
    private final Job settlementJob;
    // ...
}
```

### 11.8.2 Stage 1 — Baseline 의존성 업그레이드

`build.gradle.kts`를 6.0으로 올린다.

```kotlin
plugins {
    id("org.springframework.boot") version "4.0.0"
    id("io.spring.dependency-management") version "1.1.7"
    java
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-batch")
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    // ...
}
```

**메타 정합성 검증.**

```sql
-- 5에서 진행 중 잡이 없는지
SELECT COUNT(*) AS in_progress
FROM BATCH_JOB_EXECUTION
WHERE STATUS IN ('STARTED', 'STARTING', 'STOPPING');
-- 0이어야 함
```

**롤백.** Gradle 버전을 5.x baseline으로 되돌린다. 코드 변경은 아직 없으므로 롤백 비용이 가장 낮다.

### 11.8.3 Stage 2 — 패키지 import 정리 + 컴파일 통과

IDE에 맡겨 모든 import를 6.0 위치로 옮긴다. 컴파일 오류를 따라가며 한 줄씩 수정한다. 이 단계에서는 동작 의미는 바꾸지 않는다 — **단순 패키지 이동만**.

```java
// 변경 후
import org.springframework.batch.core.Job;
import org.springframework.batch.core.Step;
import org.springframework.batch.infrastructure.item.ItemReader;
import org.springframework.batch.infrastructure.item.ItemProcessor;
import org.springframework.batch.infrastructure.item.ItemWriter;
import org.springframework.batch.core.job.builder.JobBuilder;
import org.springframework.batch.core.step.builder.StepBuilder;
import org.springframework.batch.core.repository.JobRepository;
// ...
```

**메타 정합성 검증.** 의미 변경이 없으니 잡을 한 번 돌려본다.

```sql
-- 새 JobExecution이 정상 COMPLETED인지
SELECT JOB_EXECUTION_ID, STATUS, EXIT_CODE
FROM BATCH_JOB_EXECUTION
WHERE JOB_INSTANCE_ID = (
    SELECT MAX(JOB_INSTANCE_ID) FROM BATCH_JOB_INSTANCE
    WHERE JOB_NAME = 'settlementJob'
);
-- STATUS = 'COMPLETED', EXIT_CODE = 'COMPLETED'
```

**롤백.** Git revert로 되돌린다. 코드 변경은 패키지 이동에 한정돼 있어 충돌이 거의 없다.

### 11.8.4 Stage 3 — JobLauncher → JobOperator 전환

운영 코드의 JobLauncher 주입을 JobOperator로 바꾼다.

```java
// 변경 전
@Service
@RequiredArgsConstructor
public class SettlementLauncher {
    private final JobLauncher jobLauncher;
    private final JobExplorer jobExplorer;
    private final Job settlementJob;

    public void launch(LocalDate targetDate) throws Exception {
        if (!jobExplorer.findRunningJobExecutions("settlementJob").isEmpty()) {
            throw new IllegalStateException("Already running");
        }
        jobLauncher.run(settlementJob, buildParams(targetDate));
    }
}
```

```java
// 변경 후
@Service
@RequiredArgsConstructor
public class SettlementLauncher {
    private final JobOperator jobOperator;
    private final Job settlementJob;

    public void launch(LocalDate targetDate) throws Exception {
        if (!jobOperator.getRunningExecutions("settlementJob").isEmpty()) {
            throw new IllegalStateException("Already running");
        }
        jobOperator.start(settlementJob, buildParams(targetDate));
    }
}
```

빈 의존성이 셋에서 둘로 줄었다.

**메타 정합성 검증.** 잡을 launch해 정상 시작/종료 확인.

```sql
SELECT
    JE.JOB_EXECUTION_ID,
    JE.STATUS,
    JE.START_TIME,
    JE.END_TIME,
    COUNT(SE.STEP_EXECUTION_ID) AS step_count
FROM BATCH_JOB_EXECUTION JE
LEFT JOIN BATCH_STEP_EXECUTION SE ON JE.JOB_EXECUTION_ID = SE.JOB_EXECUTION_ID
WHERE JE.JOB_INSTANCE_ID = (
    SELECT MAX(JOB_INSTANCE_ID) FROM BATCH_JOB_INSTANCE WHERE JOB_NAME = 'settlementJob'
)
GROUP BY JE.JOB_EXECUTION_ID, JE.STATUS, JE.START_TIME, JE.END_TIME;
```

**롤백.** Git revert. 빈 주입 변경뿐이라 코드 면적이 작다.

### 11.8.5 Stage 4 — fault-tolerance 빌더 재작성

`StepBuilder`의 fault-tolerance API를 `ChunkOrientedStepBuilder` + `RetryPolicy` / `SkipPolicy` 객체로 옮긴다.

```java
// 변경 후
@Bean
public Step settlementStep(ItemReader<Order> orderReader,
                           ItemProcessor<Order, Settlement> processor,
                           ItemWriter<Settlement> writer) {

    RetryPolicy retryPolicy = RetryPolicy.builder()
        .maxRetries(3)
        .includes(Set.of(TransientApiException.class))
        .build();

    SkipPolicy skipPolicy = new LimitCheckingExceptionHierarchySkipPolicy(
        Set.of(FlatFileParseException.class), 50);

    return new ChunkOrientedStepBuilder<Order, Settlement>("settlementStep", jobRepository, 500)
        .reader(orderReader)
        .processor(processor)
        .writer(writer)
        .faultTolerant()
        .retryPolicy(retryPolicy)
        .skipPolicy(skipPolicy)
        .build();
}
```

**메타 정합성 검증 — retry/skip 정책 동작 확인.**

```sql
-- 청크 단위 read/write/skip count
SELECT
    SE.STEP_NAME,
    SE.READ_COUNT,
    SE.WRITE_COUNT,
    SE.READ_SKIP_COUNT,
    SE.PROCESS_SKIP_COUNT,
    SE.WRITE_SKIP_COUNT,
    SE.COMMIT_COUNT,
    SE.ROLLBACK_COUNT
FROM BATCH_STEP_EXECUTION SE
WHERE SE.JOB_EXECUTION_ID = ?
ORDER BY SE.STEP_EXECUTION_ID;
```

5.x에서 평소 기록되던 `COMMIT_COUNT` / `ROLLBACK_COUNT` 패턴과 6.0에서 같은 데이터로 돌렸을 때의 패턴을 비교한다. 거의 같아야 한다 — **동작 의미는 바뀌지 않는다.** 만약 `ROLLBACK_COUNT`가 갑자기 늘었다면, retry/skip 정책 매핑이 어긋났을 가능성이 있다.

**롤백.** 이 단계가 가장 코드 면적이 큰데, 롤백 시 운영 영향이 있을 수 있다. **Stage 4는 별도 PR + 별도 배포로 분리**하는 편이 안전하다. Stage 1~3까지 한 번 배포해 안정화한 뒤, Stage 4를 며칠 뒤 별도 배포로 올린다.

## 11.9 단계적 마이그레이션 전략 — 잡 하나씩, 트래픽 분리

11.8의 시나리오는 잡 한 개의 4단계 마이그레이션이다. 실제 운영에서는 잡이 여러 개일 텐데, 이걸 한꺼번에 올릴 것이냐 하나씩 올릴 것이냐의 결정이 남는다.

권하는 방식은 **잡을 하나씩, 메타 정합성을 검증하며**다. 다음 순서가 안전하다.

1. **잡 우선순위 표.** 비즈니스 중요도(상)·코드 복잡도(상)를 두 축으로 4분면을 그린다. 우선순위는 "중요도 낮음 + 복잡도 낮음" → "중요도 낮음 + 복잡도 높음" → "중요도 높음 + 복잡도 낮음" → "중요도 높음 + 복잡도 높음" 순.
2. **첫 잡으로 마이그레이션 패턴을 검증.** 가장 간단한 잡 한 개를 골라 4단계 시나리오를 다 돌고, 메타 정합성을 1주일 정도 관찰.
3. **패턴이 굳으면 다음 잡들에 같은 패턴 적용.** 한 잡당 1~2일이면 끝난다.
4. **마지막 잡(가장 중요한 것)은 마지막에.** 정산·결제 잡 같은 것은 마지막에 옮겨, 그 전까지 6에서 충분히 안정화된 패턴을 적용한다.

이 단계적 접근이 운영자의 새벽잠을 지킨다. 한 번에 모든 잡을 올렸다가 한 자리에서 어긋나면, 어디가 어긋났는지 추적이 어렵다. 한 잡씩 올리면 어긋남 자리가 명확하다.

### 11.9.1 메타 DB는 같이 옮긴다 — 분리 운영 불가

한 가지 짚어둘 것 — 같은 `BATCH_JOB_*` 메타 테이블에 5.x 잡과 6.0 잡이 동시에 쓰려고 하는 자리는 위험하다. **같은 메타 DB를 5.x 앱과 6.0 앱이 공유하면, 직렬화 포맷 차이로 메타 깨짐이 발생할 수 있다.**

그래서 마이그레이션 도중에는 두 가지 중 하나를 선택해야 한다.

- **A안 — 한 번에 모든 잡을 6.0으로.** 같은 메타 DB를 일관되게 6.0이 쓴다.
- **B안 — 메타 DB를 두 개로 분리.** 5.x용 하나, 6.0용 하나. 잡을 하나씩 옮길 때마다 그 잡의 메타 위치를 6.0 DB로 바꾼다.

운영 1년차에는 A안이 깔끔하다. 잡 수가 많아 한꺼번에 못 옮긴다면 B안이 안전한 차선책이다. 어느 쪽이든 핵심은 "같은 메타 DB 공유는 피한다"는 원칙이다.

## 11.10 롤백 시나리오 — 어느 단계에서 어디로

마이그레이션이 매끄럽지 않으면 어디로 되돌릴 것인가를 단계별로 정리해두자.

| 단계 | 실패 증상 | 롤백 위치 | 운영 영향 |
|---|---|---|---|
| Stage 1 (의존성) | Boot 4 호환성 오류 | Stage 0 | 없음 (코드 변경 전) |
| Stage 2 (import) | 컴파일 오류 잔존 | Stage 1 | 없음 |
| Stage 3 (JobOperator 전환) | launch 동작 이상 | Stage 2 | 잡 하나 launch 실패 |
| Stage 4 (fault-tolerance) | retry/skip 동작 이상 | Stage 3 | 잡 하나 동작 이상, 메타 누적 |
| (전체) DB 시퀀스 변경 | 시퀀스 오류로 잡 시작 실패 | 시퀀스 SQL 역실행 | 모든 잡 영향 |

DB 시퀀스 변경은 코드 롤백만으로는 해결이 안 된다. **시퀀스 마이그레이션 SQL을 짤 때 반드시 역실행 SQL을 같이 만들어두자.**

```sql
-- 역실행 (긴급 시)
DO $$
DECLARE
    current_value BIGINT;
BEGIN
    SELECT last_value INTO current_value FROM BATCH_JOB_INSTANCE_SEQ;

    EXECUTE format(
        'CREATE SEQUENCE IF NOT EXISTS BATCH_JOB_SEQ START WITH %s INCREMENT BY 1',
        current_value + 1
    );

    DROP SEQUENCE IF EXISTS BATCH_JOB_INSTANCE_SEQ;
END $$;
```

Flyway라면 V 마이그레이션과 짝이 되는 U(undo) 마이그레이션을 같이 두는 편이 안전하다. 운영 환경에 들어가는 모든 DB 변경에 짝 롤백 SQL이 있어야 새벽 사고에 손을 댈 수 있다.

## 11.11 마이그레이션 후 첫 1주일 — 무엇을 봐야 하는가

코드와 DB 마이그레이션이 끝난 뒤, 첫 1주일은 평소보다 조금 촘촘히 들여다보는 게 좋다. 다음 메트릭과 SQL을 daily로 본다.

**1. JobExecution 분포의 변화.**
```sql
SELECT
    DATE(START_TIME) AS run_date,
    JOB_NAME,
    STATUS,
    COUNT(*) AS cnt,
    AVG(EXTRACT(EPOCH FROM (END_TIME - START_TIME))) AS avg_seconds
FROM BATCH_JOB_EXECUTION JE
JOIN BATCH_JOB_INSTANCE JI ON JE.JOB_INSTANCE_ID = JI.JOB_INSTANCE_ID
WHERE START_TIME >= NOW() - INTERVAL '7 days'
GROUP BY DATE(START_TIME), JOB_NAME, STATUS
ORDER BY run_date DESC, JOB_NAME, STATUS;
```

5.x 마지막 1주일과 6.0 첫 1주일의 평균 처리 시간, FAILED 비율을 비교한다. 차이가 ±10% 이내면 정상.

**2. ROLLBACK_COUNT 변화.**
```sql
SELECT
    JOB_NAME,
    SUM(SE.ROLLBACK_COUNT) AS total_rollback,
    SUM(SE.COMMIT_COUNT) AS total_commit
FROM BATCH_STEP_EXECUTION SE
JOIN BATCH_JOB_EXECUTION JE ON SE.JOB_EXECUTION_ID = JE.JOB_EXECUTION_ID
JOIN BATCH_JOB_INSTANCE JI ON JE.JOB_INSTANCE_ID = JI.JOB_INSTANCE_ID
WHERE JE.START_TIME >= NOW() - INTERVAL '7 days'
GROUP BY JOB_NAME;
```

ROLLBACK_COUNT가 갑자기 늘었다면 retry/skip 정책 매핑이 어긋났을 가능성이 있다. 11.6에서 작성한 `RetryPolicy`/`SkipPolicy`가 정확히 5.x와 같은 예외를 잡고 있는지 다시 확인.

**3. ExecutionContext 크기 분포.**
```sql
SELECT
    JOB_NAME,
    AVG(LENGTH(SERIALIZED_CONTEXT)) AS avg_context_bytes,
    MAX(LENGTH(SERIALIZED_CONTEXT)) AS max_context_bytes
FROM BATCH_JOB_EXECUTION_CONTEXT BJEC
JOIN BATCH_JOB_EXECUTION JE ON BJEC.JOB_EXECUTION_ID = JE.JOB_EXECUTION_ID
JOIN BATCH_JOB_INSTANCE JI ON JE.JOB_INSTANCE_ID = JI.JOB_INSTANCE_ID
WHERE JE.START_TIME >= NOW() - INTERVAL '7 days'
GROUP BY JOB_NAME;
```

직렬화 포맷이 바뀌었으니 byte 크기가 약간 달라질 수 있다. 평균이 5.x 대비 ±20% 이내면 정상. ±50%를 넘으면 ExecutionContext 사용처를 다시 확인할 자리.

**4. recover() 자동 호출 횟수.** 10장에서 깐 자동 recover 워크플로우가 6.0 환경에서 처음 도는 자리다. recover가 무리 없이 도는지, init container가 stale execution을 잘 정리하는지를 본다.

이 4가지가 1주일간 평온하면 마이그레이션은 안정 단계로 들어간 것이다. 그 시점에 비로소 graceful shutdown과 recover의 운영 효과를 신체적으로 확인하는 자리도 온다 — 새벽에 박제된 메타를 손으로 풀던 일이 한 번도 없는 한 주.

## 마무리

마이그레이션 시나리오를 4단계로 풀어놓고 보면, 실제 변경 면적이 생각보다 작다는 사실에 놀라게 된다. 패키지 import는 IDE가 80%를 자동 처리하고, JobLauncher → JobOperator 전환은 운영 코드 한 군데가 보통이고, fault-tolerance 빌더는 객체로 분리된 형태가 오히려 깔끔하다. 무거워 보였던 6.0 변경이, 실제 마이그레이션 작업으로 풀어보면 **잡 한 개당 1~2일 작업**이 상한선이다.

다만 두 가지는 가볍게 보지 말자. **첫째, 진행 중인 JobInstance를 5에서 비우고 올리는 단계**. 직렬화 포맷 차이를 가볍게 보면 박제와 복구 불가가 동시에 온다. **둘째, 한 잡씩 옮기는 단계적 전략**. 한꺼번에 올리면 어긋남 자리 추적이 어렵다.

그리고 잊지 말 것 — 마이그레이션의 진짜 보상은 graceful shutdown과 recover()다. 1년쯤 운영해 본 사람에게 이 두 가지의 표준화는 **기능 추가**가 아니라 **수면의 질 개선**이다. 그 한 가지만으로도 6으로 올라갈 가치가 있다.

이로써 5에서 6으로의 마이그레이션이 끝났다. 마지막으로 이 책 전체를 한 발 떨어져서 보자 — 첫 잡을 만들고, 운영하고, 마이그레이션까지 마친 사람의 시야는 어떻게 바뀌는가? 5번째 잡을 만들 때 처음 잡과 무엇이 다른가? 운영 1년차의 회고로 책을 마무리하자.
