# 7장. Fault Tolerance와 테스트 — Skip/Retry/Restart와 멱등성

지난주에 컨테이너가 죽었다. 그 시점에 돌고 있던 정산 잡 인스턴스가 `STARTED`로 박제됐다. 다시 돌리려고 했더니 "이미 실행 중인 인스턴스가 있다"고 거부당했다. 결국 운영 DB에 들어가 `BATCH_JOB_EXECUTION`을 직접 UPDATE했다. 그 SQL을 치는 손이 떨렸다. WHERE 절을 한 번 더 확인하고, 트랜잭션을 시작하고, 결과를 본 뒤 커밋했다. 이게 정말 정답일까?

또 다른 새벽. 송금 잡이 retry 정책에 걸려 같은 청크를 두 번 처리했다. 첫 시도는 마지막 항목에서 외부 API 타임아웃으로 실패했고, retry가 같은 청크를 다시 돌렸다. 그런데 — 첫 시도에서 송금이 이미 나간 항목이 있었다. 두 번 돌면서 같은 사람에게 같은 금액이 두 번 송금됐다. 정산 시스템이 보고하는 매칭 결과는 깨끗한데, 외부 시스템에는 불일치가 남았다.

이 두 일화가 이 장의 출발점이다. **잡은 언젠가 실패한다.** 그게 인프라 문제든, 데이터 결함이든, 외부 API의 일시적 오류든. Spring Batch는 그 실패에 어떻게 대응하고, 우리 코드는 어떤 조건을 갖춰야 안전한가? 그리고 — 이 안전성을 어떻게 테스트로 증명할 것인가?

이 장에서 다룰 것은 다음 다섯 가지다. Skip/Retry/Restart의 의미와 적용 순서. 청크 재처리 모드(잘 알려지지 않은 동작). Restart 안전성을 위한 멱등성 3 조건. 외부 부수효과를 위한 outbox/멱등 키/dedupe 패턴. 그리고 `spring-batch-test`로 잡을 테스트하는 법.

## Skip / Retry / Restart의 의미 차이

먼저 세 단어의 의미부터 분리하자. 이게 헷갈리면 정책을 잘못 짠다.

**Skip** — 특정 예외에 대해 그 *항목*을 건너뛰고 잡은 계속 진행한다. 예를 들어 CSV 파싱 중 한 라인이 형식이 깨졌다면, 그 한 라인을 건너뛰고 다음 라인부터 계속 처리한다. `skipLimit`까지 누적되면 잡이 실패한다. 데이터 결함을 감내하면서 잡 전체를 살리는 도구다.

**Retry** — 일시적 오류에 대해 같은 항목을 N회 재시도한다. 외부 API 호출이 네트워크 일시 장애로 실패했다면, 잠깐 기다렸다가 다시 호출한다. 백오프 정책으로 간격을 늘릴 수 있다. **데이터 결함이 아니라 외부 환경 문제에 쓰는 도구**다.

**Restart** — 잡 자체가 실패했을 때, 동일 JobInstance를 다시 호출하면 마지막 커밋된 청크 다음부터 재실행한다. 1만 건 처리 중 5,001번째에서 실패했다면, 재시작 시 5,001번째부터 다시 시작한다. 이건 잡 단위의 회복이다.

이 셋은 적용 순서가 중요하다. **retry → skip → restart**.

먼저 retry. 일시 오류로 짐작되는 예외(`TransientException`, `SocketTimeoutException` 등)는 retryPolicy에 따라 N회 재시도된다. 모든 retry가 실패하면 다음 단계로 간다.

그 다음 skip. retry로 안 풀린 예외 중 skipPolicy에 등록된 것은 그 항목을 skip하고 잡을 계속 진행한다. skipLimit을 넘으면 잡 실패.

마지막이 restart. 잡 단위 실패로 나간 인스턴스를 다음 호출에서 동일 JobInstance로 재시작하면, 마지막 청크 다음부터 다시 시작한다.

이 순서를 모르고 정책을 짜면 어떤 일이 벌어질까? 가령 데이터 결함을 retry로 처리하려 들면 — 같은 결함을 N번 반복해서 만나고, retry가 모두 실패한 뒤에야 skip이 작동한다. 그동안 시간만 잡아먹는다. 반대로 외부 API 일시 오류를 skip으로 처리하면 — 운영자가 매일 아침 unmatched 테이블에서 수십 건씩 정상 거래를 손으로 다시 처리하게 된다. 정책의 의미를 알고 적용 자리를 가르는 게 출발이다.

## fault-tolerant step 빌드 — 6.0 스타일

5장에서 한번 짚었지만 한 번 더 코드로 풀어보자. 6.0의 fault-tolerant step은 이렇게 짠다.

```java
@Bean
public Step settlementStep(JobRepository jobRepository,
                           ItemReader<RawTransaction> reader,
                           ItemWriter<RawTransaction> writer) {
    // retry 정책: 일시 오류만 3회까지
    RetryPolicy retryPolicy = RetryPolicy.builder()
        .maxRetries(3)
        .includes(Set.of(
            SocketTimeoutException.class,
            TransientDataAccessException.class
        ))
        .build();

    // skip 정책: 데이터 결함은 50건까지 허용
    SkipPolicy skipPolicy = new LimitCheckingExceptionHierarchySkipPolicy(
        Set.of(
            FlatFileParseException.class,
            ValidationException.class
        ),
        50  // skipLimit
    );

    return new ChunkOrientedStepBuilder<RawTransaction, RawTransaction>(
            "settlementStep", jobRepository, 1000)
        .reader(reader)
        .writer(writer)
        .faultTolerant()
            .retryPolicy(retryPolicy)
            .skipPolicy(skipPolicy)
        .build();
}
```

여기서 짚어야 할 디테일 두 가지.

**하나, retry와 skip의 예외 집합이 겹치면 안 된다.** `SocketTimeoutException`을 retry에도 넣고 skip에도 넣으면, retry로 N번 재시도한 뒤 skip이 작동해서 항목을 건너뛴다. 이게 의도면 좋지만, 보통은 의도가 아니다. 일시 오류는 재시도하고, 데이터 결함은 건너뛰는 게 분리된 의도다.

**둘, `.faultTolerant()`가 트리거다.** 이 호출이 빠지면 retryPolicy/skipPolicy 설정이 적용되지 않는다. fault-tolerant step의 동작 모드는 일반 청크 step과 다르다. 한 항목이 실패할 때 청크 전체를 롤백하고 항목 단위 재처리 모드로 들어가는 등, 약간 더 무거운 동작을 한다. 그래서 명시적으로 켜야 한다.

## Skip 발생 시 청크 재처리 모드

이게 Spring Batch에서 잘 알려지지 않은 중요한 동작이다. 한 번 짚어두자.

청크 사이즈를 1,000으로 잡고 fault-tolerant step에서 돌리고 있다고 하자. 어느 청크에서 423번째 항목이 `ValidationException`을 던졌다. skipPolicy에 등록된 예외라 skip 대상이다. 그러면 어떻게 동작할까?

**1차 시도:** 청크의 1~423번째까지 process가 진행된다. 423번째에서 예외 발생. 청크 트랜잭션이 **롤백**된다. 1~422번째까지 변경된 모든 것이 되돌아간다.

**2차 시도 (자동 전환):** 같은 청크를 **chunk size = 1로 항목 단위 단건 모드**로 다시 처리한다. 이제 1번째 항목부터 한 건씩 process하고 한 건씩 트랜잭션을 커밋한다. 423번째 항목이 다시 예외를 던지면, 그 한 건만 skip하고 다음(424번째)으로 진행한다. 나머지 577건은 한 건씩 처리되고, 청크 처리가 끝난다.

이 동작을 알면 두 가지 함정을 피할 수 있다.

**함정 1 — 성능 영향.** skip이 많이 일어나는 잡은 청크 단위 처리가 항목 단위 처리로 자주 전환된다. 1,000건짜리 청크가 trim되어 1,000번의 트랜잭션이 일어나면, 그 청크 처리는 일반 청크의 수십 배 시간이 걸린다. skip이 정상 운영의 일부라면, skipLimit을 잘 잡아서 잡을 빨리 실패시키든가, 데이터 정제를 reader 앞단으로 옮기든가 해야 한다.

**함정 2 — 멀티스레드 step과의 상호작용.** skip이 발생한 청크가 항목 단위 모드로 전환될 때, 멀티스레드 step의 reader 일관성이 어긋날 수 있다. 6.0의 producer-consumer 모델은 이 부분을 일부 완화했지만, **skip이 일상적인 잡에서는 멀티스레드 대신 partitioning**을 권장한다. 8장에서 다시 본다.

## Restart 안전성 — Idempotency 3 조건

restart가 안전하게 동작하려면 잡이 다음 세 조건을 만족해야 한다. 이게 Spring Batch에서 가장 중요한 자기진단 체크리스트다.

**조건 1: ItemWriter는 같은 청크를 두 번 받아도 동일 결과여야 한다 (멱등).**

청크가 1,001~2,000번째 항목으로 채워졌다. write가 진행되다가 마지막에 트랜잭션 커밋이 실패했다(예: DB 커넥션 끊김). retry 정책에 의해 같은 청크가 다시 시도된다. 같은 1,000건이 두 번 write로 들어온다.

이 두 번이 동일 결과여야 한다. 첫 시도에서 일부가 INSERT됐다면, 두 번째 시도에서 같은 INSERT를 시도하면 PK 중복 에러가 난다. 그래서 INSERT 대신 UPSERT(`INSERT ... ON DUPLICATE KEY UPDATE`, `MERGE`, JPA의 `saveAll` with managed entity 등)를 쓰거나, 처리 완료 ID를 별도 dedupe 테이블에 기록하고 write 전에 SELECT로 거르는 패턴을 쓴다.

UPDATE 작업도 멱등이라야 한다. "이 행의 status를 'COMPLETED'로 바꾼다"는 본질적으로 멱등이지만, "이 행의 count를 1 증가시킨다" 같은 누적 연산은 비멱등이다. 누적 연산을 청크 안에서 하는 잡은 retry/restart에서 특히 위험하다 — 같은 청크가 두 번 돌면 카운트가 2 증가한다.

**조건 2: ItemReader는 ExecutionContext에 진행 위치를 저장해야 한다.**

restart 시 reader가 어디부터 다시 읽어야 할지 알아야 한다. Spring Batch의 내장 Reader는 대부분 이걸 자동으로 한다. `JdbcCursorItemReader`, `JdbcPagingItemReader`, `FlatFileItemReader` 모두 마지막 처리 위치를 ExecutionContext에 저장한다. 잡이 5,001번째에서 실패했다면, restart 시 5,001번째부터 다시 읽는다.

직접 작성한 Reader라면 이 부분을 직접 짜야 한다. `ItemStream` 인터페이스를 구현하면 된다.

```java
public class CustomReader implements ItemReader<MyItem>, ItemStream {
    private long lastProcessedId;
    private static final String LAST_ID_KEY = "lastProcessedId";

    @Override
    public void open(ExecutionContext executionContext) {
        // restart 시 마지막 위치 복원
        if (executionContext.containsKey(LAST_ID_KEY)) {
            lastProcessedId = executionContext.getLong(LAST_ID_KEY);
        }
    }

    @Override
    public void update(ExecutionContext executionContext) {
        // 청크 커밋 시점에 호출 — 진행 위치 저장
        executionContext.putLong(LAST_ID_KEY, lastProcessedId);
    }

    @Override
    public void close() { /* 자원 정리 */ }

    @Override
    public MyItem read() { /* 다음 항목 반환, 없으면 null */ }
}
```

`update()`가 청크 커밋 직전에 호출된다는 점이 핵심이다. 청크 트랜잭션이 커밋되면 ExecutionContext도 함께 영속된다. 트랜잭션이 롤백되면 ExecutionContext도 롤백된다. 즉 **reader의 진행 위치 저장과 청크 트랜잭션이 한 트랜잭션**으로 묶인다 — Spring Batch의 우아한 설계 중 하나다.

**조건 3: 외부 부수효과는 단순 멱등으로 부족하다.**

송금, 이메일, 푸시, 외부 API 변경 호출 — 이런 부수효과는 우리 시스템 밖에서 일어난다. 청크 트랜잭션이 롤백되어도 이미 나간 송금은 되돌아오지 않는다. 이메일은 받는 사람이 이미 봤다.

이 자리에서는 단순한 Writer 멱등성으로 부족하다. 추가 장치가 필요하다. 그게 다음 절의 outbox 패턴, 멱등 키, dedupe 저장소다.

## STARTED 박제 문제 — 6.0의 `recover()` 한 줄

조건 1~3을 만족해도, 회복 불가능해 보이는 상태가 하나 있다. **STARTED 박제.**

상황을 그려보자. 잡이 정상적으로 시작됐다. JobRepository에 JobExecution 레코드가 STATUS = `STARTED`로 INSERT된다. 잡이 한참 도는 도중 컨테이너가 SIGKILL(예: K8s OOMKilled)을 받는다. JVM이 graceful shutdown 훅을 돌릴 시간조차 없이 즉사한다. JobExecution은 `STARTED`인 채로 DB에 남는다.

다음 스케줄에서 같은 잡을 호출한다. Spring Batch는 메타를 본다 — "STARTED 인스턴스가 이미 있다." 새 시도는 거부된다. 운영자가 손을 봐야 한다.

5.x에서는 이 자리를 두 가지 방법으로 풀었다.

```sql
-- 직접 손으로 SQL
UPDATE BATCH_JOB_EXECUTION
SET STATUS = 'FAILED',
    EXIT_CODE = 'FAILED',
    END_TIME = NOW(),
    VERSION = VERSION + 1
WHERE JOB_EXECUTION_ID = ?;
```

이걸 새벽 3시에 졸린 눈으로 짠다. WHERE 절을 빠뜨리는 사고가 한 번이라도 있으면 모든 STARTED가 한 번에 FAILED로 마킹된다. 끔찍한 일이다.

또는 회사마다 직접 짠 admin 유틸이 있다. 비슷한 코드가 한국 회사 어디에나 굴러다닌다. 표준이 아니라 직접 짠 코드라는 게 문제다 — 새 멤버가 들어오면 또 그 유틸의 사용법을 가르쳐야 한다.

6.0에서는 한 줄이다.

```java
jobOperator.recover(executionId);
```

이 메서드는 다음을 한다.

1. 해당 JobExecution을 찾는다.
2. 상태가 STARTED인지 확인 (다른 상태면 예외).
3. 상태를 FAILED로, EXIT_CODE를 FAILED로 마킹.
4. 그 안의 모든 STARTED StepExecution도 함께 FAILED로 마킹.
5. END_TIME을 현재 시각으로.

그 후 같은 JobInstance를 `start()` 또는 `restart()`로 호출하면, restart로 동작해서 마지막 커밋된 청크 다음부터 다시 시작한다.

K8s 운영에서 이 메서드를 쓰는 표준 패턴은 다음 두 가지다.

**패턴 1 — Pod 시작 시 자동 recover.** 잡 Pod이 시작될 때 init 단계에서 자기 잡 이름의 STARTED 박제를 모두 recover한다.

```java
@Component
public class StartedJobRecoveryRunner implements ApplicationRunner {
    private final JobOperator jobOperator;
    private final JobRepository jobRepository;

    @Override
    public void run(ApplicationArguments args) {
        String jobName = args.getOptionValues("spring.batch.job.name").get(0);
        // 해당 잡의 STARTED 인스턴스를 모두 찾아 recover
        Set<JobExecution> stale = jobRepository.findRunningJobExecutions(jobName);
        for (JobExecution execution : stale) {
            jobOperator.recover(execution.getId());
        }
    }
}
```

**패턴 2 — 운영 admin API.** 운영자가 호출할 수 있는 단일 엔드포인트로 recover를 노출한다.

```java
@RestController
@RequestMapping("/admin/batch")
public class BatchAdminController {
    private final JobOperator jobOperator;

    @PostMapping("/recover/{executionId}")
    public ResponseEntity<Void> recover(@PathVariable long executionId) {
        jobOperator.recover(executionId);
        return ResponseEntity.ok().build();
    }
}
```

운영 시점에는 패턴 1이 자동화 측면에서 이상적이다. 사람이 매번 손을 대지 않게 만든다는 게 6.0의 약속이다. 자세한 K8s 매니페스트 패턴은 10장에서 다룬다.

## SkipListener / JobExecutionListener 패턴

skip된 항목을 그냥 흘려보내면 안 된다. 운영자가 알아야 한다. SkipListener가 그 자리다.

```java
public class SettlementSkipListener implements SkipListener<RawTransaction, RawTransaction> {
    private final FailedItemRepository failedItems;
    private final SlackNotifier slack;

    @Override
    public void onSkipInRead(Throwable t) {
        // read 중 skip — 파일 한 줄 깨짐 등
        slack.warn("Read skip: " + t.getMessage());
    }

    @Override
    public void onSkipInProcess(RawTransaction item, Throwable t) {
        // process 중 skip — validation 실패 등
        failedItems.save(new FailedItem(item, t.getMessage(), Stage.PROCESS));
    }

    @Override
    public void onSkipInWrite(RawTransaction item, Throwable t) {
        // write 중 skip — 외부 API 영구 실패 등
        failedItems.save(new FailedItem(item, t.getMessage(), Stage.WRITE));
        slack.alert("Write skip — 데이터 정합성 검토 필요: " + item.getId());
    }
}
```

핵심은 **skip된 항목을 별도 테이블에 격리**한다는 점이다. 그러면 다음 날 운영자가 그 테이블만 보고 처리하면 된다. 그 항목들의 원인이 일시 외부 API 장애였다면 — 운영자가 일괄 재처리할 수 있다. 데이터 결함이었다면 — 원본 시스템에 보고해서 정정 요청을 한다.

JobExecutionListener는 잡 시작/종료 시점의 hook이다.

```java
public class SettlementJobListener implements JobExecutionListener {
    private final JobMetricsCollector metrics;
    private final SlackNotifier slack;

    @Override
    public void beforeJob(JobExecution jobExecution) {
        slack.info("정산 잡 시작: " + jobExecution.getJobInstance().getJobName());
    }

    @Override
    public void afterJob(JobExecution jobExecution) {
        long durationMs = jobExecution.getEndTime().toEpochMilli()
            - jobExecution.getStartTime().toEpochMilli();
        metrics.record(jobExecution, durationMs);

        if (jobExecution.getStatus() == BatchStatus.FAILED) {
            slack.alert("정산 잡 실패: " + jobExecution.getAllFailureExceptions());
        }
    }
}
```

skip이 누적되면 운영자에게 알람을 보내고, 잡 실패는 즉시 콜라보레이션 채널에 푸시한다. 모니터링 인프라가 갖춰지기 전까지의 가장 단단한 운영 장치다. 본격적인 메트릭과 알람 임계값 설계는 9장에서 다룬다.

## 외부 부수효과 보호 — Outbox / 멱등 키 / Dedupe

이 절이 fault tolerance의 가장 어려운 자리다. 송금, 이메일, 푸시처럼 외부 시스템에 부수효과를 일으키는 잡은 — 단순한 Writer 멱등성으로 충분하지 않다. 세 가지 패턴을 비교해보자.

### 패턴 1 — Outbox

도메인 트랜잭션과 같은 트랜잭션에 outbox 행을 INSERT하고, 별도 워커가 그 outbox를 읽어 외부 시스템에 발행한다.

```java
@Service
@Transactional
public class TransferService {
    private final TransferRepository transfers;
    private final OutboxRepository outbox;

    public void process(Transfer transfer) {
        // 1. 도메인 변경
        transfer.markAsCompleted();
        transfers.save(transfer);

        // 2. 같은 트랜잭션에 outbox 행 INSERT
        outbox.save(new OutboxEntry(
            transfer.getId(),
            "TRANSFER_COMPLETED",
            transfer.toJson()
        ));
        // 트랜잭션 커밋 시 둘 다 영속, 롤백 시 둘 다 사라짐
    }
}

// 별도 워커가 outbox를 읽어 외부 발행
@Component
public class OutboxPublisher {
    @Scheduled(fixedDelay = 5000)
    public void publish() {
        List<OutboxEntry> pending = outbox.findUnpublished();
        for (OutboxEntry entry : pending) {
            externalSystem.send(entry);  // 외부 호출
            outbox.markPublished(entry.getId());
        }
    }
}
```

이 패턴의 장점은 **도메인 변경과 외부 발행이 결코 어긋나지 않는다**는 점이다. 도메인 트랜잭션이 커밋됐다면 outbox에도 행이 있고, 결국 발행된다. 도메인 트랜잭션이 롤백됐다면 outbox에 행이 없고, 발행도 안 된다. 잡이 retry/restart로 같은 청크를 두 번 받아도, 도메인 트랜잭션이 멱등이면 outbox도 결과적으로 멱등이다.

단점은 — **워커가 추가로 필요**하다. 외부 발행이 즉시가 아니다(지연 발생). outbox 테이블이 자라므로 정리 잡도 필요하다. 그러나 정확성 측면에서 가장 단단한 패턴이다.

### 패턴 2 — 멱등 키

외부 호출에 idempotency-key 헤더를 붙인다. 동일 키로 같은 호출이 들어오면 외부 시스템이 자기 쪽에서 중복을 검출해 첫 결과를 그대로 반환한다.

```java
public class TransferWriter implements ItemWriter<Transfer> {
    private final ExternalTransferApi api;

    @Override
    public void write(Chunk<? extends Transfer> chunk) {
        for (Transfer transfer : chunk.getItems()) {
            String idempotencyKey = "transfer-" + transfer.getId();
            api.send(idempotencyKey, transfer);
        }
    }
}
```

장점은 **단순**하다는 것. 외부 시스템이 idempotency-key를 지원한다면 추가 인프라 없이 안전성이 확보된다. Stripe, Toss Payments 같은 결제 API가 표준으로 제공한다.

단점은 — 외부 시스템이 멱등 키를 지원해야만 가능하다. 자체 구축 외부 시스템은 보통 지원하지 않는다. 그리고 멱등 키의 보존 기간이 짧으면, 잡이 24시간 뒤에 재시작될 때 같은 키로 호출해도 외부가 새 호출로 인식할 수 있다. 키 정책을 외부와 합의해야 한다.

### 패턴 3 — Dedupe 저장소

처리 완료한 항목 ID를 별도 dedupe 테이블에 기록하고, write 전에 SELECT해서 이미 처리된 항목은 거른다.

```java
public class TransferWriter implements ItemWriter<Transfer> {
    private final ExternalTransferApi api;
    private final DedupeRepository dedupe;

    @Override
    @Transactional
    public void write(Chunk<? extends Transfer> chunk) {
        Set<Long> alreadyProcessed = dedupe.findExistingIds(
            chunk.getItems().stream().map(Transfer::getId).toList()
        );

        for (Transfer transfer : chunk.getItems()) {
            if (alreadyProcessed.contains(transfer.getId())) {
                continue;  // 이미 처리됨, skip
            }
            api.send(transfer);
            dedupe.markProcessed(transfer.getId());
        }
    }
}
```

장점은 — **외부 시스템에 의존하지 않는다**. 우리 쪽에서 모든 책임을 진다. 외부 호출 직후 dedupe 마킹이 같은 트랜잭션이라면, 외부 호출 성공 시에만 마킹된다.

단점은 — 외부 호출과 dedupe 마킹 사이에 race가 있다. 외부 호출이 성공한 직후 컨테이너가 죽으면 마킹이 안 되고, 재시작 시 같은 호출이 다시 나간다. 이 race를 완전히 닫으려면 결국 outbox 패턴이거나 멱등 키가 필요하다.

### 세 패턴 비교

| 항목 | Outbox | 멱등 키 | Dedupe 저장소 |
|------|--------|---------|---------------|
| 정확성 | 매우 높음 (트랜잭션 보장) | 높음 (외부 의존) | 중간 (race 존재) |
| 구현 복잡도 | 높음 (워커 필요) | 낮음 (헤더 하나) | 중간 (테이블 하나) |
| 외부 시스템 의존 | 없음 | 멱등 키 지원 필요 | 없음 |
| 즉시 발행 | 아니오 (지연) | 예 | 예 |
| 재시도 친화 | 매우 친화 | 친화 | 부분 친화 |

어떤 패턴을 고를까? 결정 트리를 그려보자.

1. **외부 시스템이 멱등 키를 지원하는가?** → 멱등 키. 가장 단순하고 표준이다.
2. **지원하지 않는다면, 정확성이 매우 중요한가(송금·결제)?** → Outbox. 도메인 트랜잭션과 외부 발행을 묶어 절대 어긋나지 않게.
3. **그보다는 즉시성이 중요하고 race를 감수할 수 있는가(이메일·푸시)?** → Dedupe 저장소. 90% 정확성을 단순하게.

송금 잡을 예로 들면, 외부 송금 API가 멱등 키를 지원한다면 패턴 2로 끝난다. 자체 송금 시스템이라 멱등 키 지원이 없다면, 도메인 트랜잭션 안에 outbox를 넣고 별도 워커로 외부 발행을 분리한다. 이메일 잡 같은 자리는 dedupe 저장소로도 충분하다 — 한 번 더 보내질 위험이 있어도 운영상 받아들일 수 있는 수준이다.

## 안티패턴 — 비멱등 Writer + Retry 조합

이 조합이 가장 위험하다. 한 번 더 강조하자.

```java
// (위험) 비멱등 Writer
public class CounterWriter implements ItemWriter<Event> {
    private final CounterRepository counters;

    @Override
    public void write(Chunk<? extends Event> chunk) {
        for (Event event : chunk.getItems()) {
            // count를 1 증가 — 비멱등
            counters.incrementBy(event.getCounterId(), 1);
        }
    }
}
```

이 Writer가 retry 정책에 묶여 있으면, 일시 오류로 같은 청크가 두 번 처리될 때 카운트가 두 번 증가한다. 운영자는 통계가 왜 이상한지 한참을 헤매다 결국 추적 로그를 보고 알게 된다. 가장 어두운 종류의 버그다.

해결은 두 가지다.

```java
// 해결 1: Writer를 멱등으로 만든다
public class IdempotentCounterWriter implements ItemWriter<Event> {
    @Override
    public void write(Chunk<? extends Event> chunk) {
        for (Event event : chunk.getItems()) {
            // 이미 처리된 이벤트인지 확인 후 증가
            if (!processedEvents.exists(event.getId())) {
                counters.incrementBy(event.getCounterId(), 1);
                processedEvents.mark(event.getId());
            }
        }
    }
}

// 해결 2: 절대값 UPDATE로 바꾼다 (멱등)
public class IdempotentCounterWriter implements ItemWriter<DailyCounter> {
    @Override
    public void write(Chunk<? extends DailyCounter> chunk) {
        for (DailyCounter dc : chunk.getItems()) {
            // SET count = N — 두 번 돌려도 결과 동일
            counters.setCount(dc.getCounterId(), dc.getValue());
        }
    }
}
```

증분 연산이 본질적으로 비멱등이라는 점을 기억해두자. 청크 안에서 외부 카운터를 증가시키거나, 잔액을 차감하거나, 재고를 줄이는 작업은 모두 위험 신호다. 이런 자리에서는 dedupe로 막거나, 절대값 SET으로 바꾸거나, outbox로 분리하자.

## 잡을 어떻게 테스트할 것인가 — `spring-batch-test`

여기까지가 안전성의 이론이다. 그러면 — 이 안전성을 어떻게 자동화 테스트로 증명할까? 한국 자료에 가장 빈약한 영역이다. 한 절을 충분히 할애해 풀어보자.

먼저 의존성. 6.0에서 `spring-batch-test`는 JUnit 5만 지원한다(JUnit 4 deprecated).

```xml
<dependency>
    <groupId>org.springframework.batch</groupId>
    <artifactId>spring-batch-test</artifactId>
    <scope>test</scope>
</dependency>
```

핵심 도구가 두 개다. **`JobLauncherTestUtils`**와 **`MetaDataInstanceFactory`**.

### JobLauncherTestUtils로 잡/스텝 실행

`JobLauncherTestUtils`는 테스트에서 잡 또는 단일 스텝을 실행할 수 있게 해준다.

```java
@SpringBatchTest
@SpringBootTest(classes = {SettlementJobConfig.class, BatchTestConfig.class})
class SettlementJobIntegrationTest {

    @Autowired
    private JobLauncherTestUtils jobLauncherTestUtils;

    @Autowired
    private JobRepository jobRepository;

    @BeforeEach
    void setUp() {
        // 매 테스트마다 깨끗한 메타 — 인메모리 DB라면 자동
    }

    @Test
    @DisplayName("정산 잡이 1,000건 입력에 대해 SUCCESS로 종료한다")
    void settlementJob_succeeds_for_1000_items() throws Exception {
        // given: 1,000건의 raw_transaction 데이터 준비
        seedRawTransactions(1000);

        JobParameters params = new JobParametersBuilder()
            .addString("date", "2026-05-08")
            .addLong("run.id", System.currentTimeMillis())
            .toJobParameters();

        // when
        JobExecution execution = jobLauncherTestUtils.launchJob(params);

        // then
        assertThat(execution.getStatus()).isEqualTo(BatchStatus.COMPLETED);
        assertThat(execution.getStepExecutions())
            .extracting(StepExecution::getWriteCount)
            .containsExactly(1000L);
    }

    @Test
    @DisplayName("settlementStep만 단독 실행이 가능하다")
    void launch_step_in_isolation() throws Exception {
        seedRawTransactions(100);

        JobExecution execution = jobLauncherTestUtils.launchStep(
            "settlementStep",
            new JobParametersBuilder()
                .addString("date", "2026-05-08")
                .addLong("run.id", System.currentTimeMillis())
                .toJobParameters()
        );

        assertThat(execution.getStatus()).isEqualTo(BatchStatus.COMPLETED);
    }
}
```

`@SpringBatchTest`가 핵심이다. 이 어노테이션이 `JobLauncherTestUtils`와 관련 빈을 자동 등록한다. 그 다음 `launchJob` 또는 `launchStep`으로 실행한다. 잡 단위 통합 테스트는 `launchJob`을, step 단위로 격리해서 디버깅하고 싶다면 `launchStep`을 쓴다.

### MetaDataInstanceFactory로 픽스처 생성

JobParameters나 StepExecution을 손으로 만들어야 하는 자리가 있다. 예를 들어 listener를 단위 테스트하거나, custom Reader/Writer가 ExecutionContext를 어떻게 다루는지 검증하고 싶을 때.

```java
class SettlementSkipListenerTest {

    private SettlementSkipListener listener;
    private FailedItemRepository failedItems;
    private SlackNotifier slack;

    @BeforeEach
    void setUp() {
        failedItems = mock(FailedItemRepository.class);
        slack = mock(SlackNotifier.class);
        listener = new SettlementSkipListener(failedItems, slack);
    }

    @Test
    @DisplayName("process skip 시 failedItems에 격리된다")
    void onSkipInProcess_persists_failed_item() {
        RawTransaction item = new RawTransaction(1L, "ext-1", BigDecimal.TEN);
        ValidationException ex = new ValidationException("amount mismatch");

        listener.onSkipInProcess(item, ex);

        ArgumentCaptor<FailedItem> captor = ArgumentCaptor.forClass(FailedItem.class);
        verify(failedItems).save(captor.capture());
        assertThat(captor.getValue().getReason()).contains("amount mismatch");
    }
}
```

위는 listener를 직접 단위 테스트하는 모양이다. JobExecution 같은 도메인 객체를 픽스처로 만들고 싶다면 `MetaDataInstanceFactory`를 쓴다.

```java
@Test
@DisplayName("afterJob 콜백이 메트릭을 기록한다")
void afterJob_records_metrics() {
    JobExecution execution = MetaDataInstanceFactory.createJobExecution(
        "settlementJob", 1L, 1L,
        new JobParametersBuilder()
            .addString("date", "2026-05-08")
            .toJobParameters()
    );
    execution.setStatus(BatchStatus.COMPLETED);
    execution.setStartTime(LocalDateTime.now().minusMinutes(10).toInstant(ZoneOffset.UTC));
    execution.setEndTime(Instant.now());

    listener.afterJob(execution);

    verify(metrics).record(eq(execution), longThat(d -> d > 0));
}
```

JobExecution을 손으로 new하지 않는다. `MetaDataInstanceFactory`가 도메인 모델의 invariant(JobInstance와 JobExecution의 부모-자식 관계 등)를 지키면서 픽스처를 만들어준다. 6의 record화 이후에는 더더욱 이 팩토리를 쓰는 게 안전하다.

### Chunk-level vs End-to-end 테스트의 분리

테스트 전략에서 중요한 결정이 이것이다. 모든 테스트를 `launchJob`으로 짜면 — 한 테스트가 무겁다. DB 컨테이너를 띄우고, 잡 전체를 돌리고, 결과를 검증한다. 수십 개가 넘으면 CI가 느려진다.

권장 분리는 다음과 같다.

**Chunk-level (단위/협력 테스트)** — Reader/Processor/Writer를 따로 또는 묶어서 테스트.
- Reader가 ExecutionContext에 진행 위치를 저장하는가?
- Processor가 null을 반환하면 필터링되는가?
- Writer가 같은 청크를 두 번 받았을 때 멱등인가? (중요)
- SkipListener가 실패 항목을 격리하는가?

이 자리는 빠르고, mock과 in-memory를 자유롭게 쓴다.

**End-to-end (통합 테스트)** — 전체 잡을 `launchJob`으로 실행.
- 1,000건 입력 → COMPLETED → 결과 데이터 검증
- 일부러 실패 데이터를 섞고 → skipLimit까지 skip되며 COMPLETED
- 잡 실행 도중 강제 중단 → 메타 상태 검증
- 같은 JobParameters로 두 번 실행 → 두 번째는 거부

이 자리는 무겁지만, 진짜 안전성을 보증한다. 핵심 잡 1~2개에 대해 충실히 짜자.

### In-memory JobRepository(H2) vs Testcontainers

테스트 메타 저장소도 결정 사항이다.

```java
// 옵션 1: H2 in-memory
@SpringBootTest
@TestPropertySource(properties = {
    "spring.datasource.url=jdbc:h2:mem:batch_test;MODE=MySQL",
    "spring.batch.jdbc.initialize-schema=always"
})
class InMemoryBatchTest { ... }

// 옵션 2: Testcontainers — production DB와 같은 종
@Testcontainers
@SpringBootTest
class IntegrationBatchTest {
    @Container
    static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.0");

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", mysql::getJdbcUrl);
        registry.add("spring.datasource.username", mysql::getUsername);
        registry.add("spring.datasource.password", mysql::getPassword);
    }
    // ...
}
```

H2 in-memory는 빠르다. CI에서 수십 개의 테스트를 1분 안에 돌릴 수 있다. 그러나 production이 PostgreSQL이나 MySQL이라면, **DB 종 차이로 인한 미묘한 동작 차이**가 있다. 시퀀스 동작, JSON 컬럼 처리, lock 동작이 다르다.

권장 분리는 — chunk-level 테스트는 H2로, end-to-end 테스트는 Testcontainers로 production과 같은 DB를 띄운다. 핵심 잡 1~2개에 대해서는 production DB와 같은 환경에서 검증하는 게 안전성의 마지막 보증이다.

### 멱등성 테스트 — 가장 중요한 한 가지

이 책에서 강조하고 싶은 테스트 한 가지를 꼽으라면, Writer 멱등성 테스트다. 이걸 빠뜨리면 retry/restart가 운영에서 사고를 만든다.

```java
@Test
@DisplayName("Writer가 같은 청크를 두 번 받아도 결과가 동일하다 (멱등)")
void writer_is_idempotent_on_double_invocation() {
    // given
    Chunk<EnrichedTransaction> chunk = new Chunk<>(List.of(
        new EnrichedTransaction(1L, BigDecimal.valueOf(100)),
        new EnrichedTransaction(2L, BigDecimal.valueOf(200))
    ));

    // when: 같은 청크를 두 번 write
    writer.write(chunk);
    State afterFirst = captureState();
    writer.write(chunk);
    State afterSecond = captureState();

    // then: 두 상태가 동일
    assertThat(afterSecond).isEqualTo(afterFirst);
}
```

이 테스트가 통과하면 retry/restart로 같은 청크가 두 번 들어와도 안전하다는 보증이 생긴다. 모든 Writer에 이 테스트가 짝지어 있어야 한다 — 외부 부수효과가 있는 Writer는 dedupe/outbox/멱등 키 검증을 함께.

## 자기진단 체크리스트

이 장을 마무리하면서, 자기 잡이 production-ready인지 점검할 한 페이지 체크리스트를 묶어두자.

**Skip / Retry 정책**
- [ ] retry 예외 집합과 skip 예외 집합이 분리되어 있는가? (일시 오류 vs 데이터 결함)
- [ ] skipLimit이 운영 합의된 값인가? (너무 크면 잡이 무한 살아남고, 너무 작으면 일상 결함에 즉시 실패)
- [ ] `.faultTolerant()`가 호출됐는가?

**Restart 안전성 (Idempotency 3 조건)**
- [ ] Writer가 같은 청크를 두 번 받아도 동일 결과인가? (테스트로 증명)
- [ ] Reader가 ExecutionContext에 진행 위치를 저장하는가? (내장 Reader는 자동, 커스텀이면 ItemStream 구현)
- [ ] 외부 부수효과가 있다면 outbox/멱등 키/dedupe 중 하나가 적용됐는가?

**STARTED 박제 대비**
- [ ] `JobOperator#recover()`가 운영 워크플로우에 통합됐는가? (Pod 시작 시 자동, 또는 admin API)

**모니터링 hook**
- [ ] SkipListener가 등록되어 skip 항목이 별도 테이블에 격리되는가?
- [ ] JobExecutionListener가 잡 실패를 운영 채널에 알리는가?

**테스트**
- [ ] Writer 멱등성 테스트가 있는가?
- [ ] 핵심 잡에 대한 end-to-end 테스트가 있는가?
- [ ] skip이 발생하는 시나리오 테스트가 있는가?

이 체크리스트를 한 잡에 적용해 모두 체크 표시가 되면, 그 잡은 운영에서 실패해도 안전하게 회복한다. 모든 체크가 처음부터 만족되지는 않는다 — 하나씩 채워가는 일이 운영 시스템을 만드는 일이다.

잡이 안전한 상태를 가정하고, 다음 장에서는 **빨라지는 길**을 보자. chunk size 튜닝, 멀티스레드, partitioning, Remote Step의 결정 트리. 6장의 카카오페이 사례에서 4단계로 끝낸 그 자리, 그 다음 카드들이다.
