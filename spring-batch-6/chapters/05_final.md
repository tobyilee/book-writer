# 5장. Spring Batch 6의 변경점 — 무엇이, 왜 달라졌는가

5에서 잘 돌던 코드를 6으로 올린 첫날을 떠올려보자. 의존성을 바꾸고 빌드를 돌리면 IDE의 절반이 빨갛다. `ChunkOrientedTasklet`은 deprecated라고 한다. `JobLauncher`를 주입하던 자리에 `JobOperator`를 쓰라는 권고가 붙는다. `JobParameters`에 String을 꺼내 쓰던 코드가 컴파일은 되는데 어쩐지 모양이 달라졌다. 왜 멀쩡하던 걸 바꿨을까? 마이그레이션이 끝나기는 할까?

Spring Batch 6 GA(2025-11-19)에 도달하기까지의 변경점을 한 묶음으로 풀어보자. 단순히 "API 표"를 외우자는 것이 아니다. 변경의 **동기**를 이해해두면, 마이그레이션의 우선순위가 보이고, 무엇이 자기 코드에 영향을 줄지 빠르게 판별할 수 있다. 운영 중인 시스템을 옮기는 실전 시나리오는 11장에서 다룬다. 여기서는 그 전에 "왜"부터 짚어두자.

## 출시 타임라인과 baseline

먼저 시간 축을 짚어두자. 6.0이 어느 날 갑자기 발표된 게 아니다.

- 2025-07-23: 6.0.0-M1 — 첫 마일스톤. 새 ChunkOrientedStepBuilder의 골격이 공개됐다.
- 2025-08-20: 6.0.0-M2 — `JobOperator#recover()` 도입. K8s 운영자가 가장 기다리던 그 메서드.
- 2025-09-17: 6.0.0-M3, 그리고 5.2.3 동시 출시 — 5.x 사용자에게 "이쪽 라인은 이게 마지막 의미 있는 백포트"라는 신호.
- 2025-10-09: 6.0.0-M4 — 도메인 모델 record화의 윤곽이 거의 다 드러난 시점.
- **2025-11-19: 6.0.0 GA** — 우리가 기준으로 삼는 그 버전.
- 2025-12-17: 6.0.1 maintenance — 첫 패치.

타임라인을 굳이 적어둔 이유가 있다. 마이그레이션을 검토할 때 "지금 6.0을 쓸 거냐, 6.0.1까지 기다릴 거냐, 더 늦게 갈 거냐"의 결정에서 패치 출시 간격이 중요한 신호가 된다. 6.0 GA에서 한 달 만에 6.0.1이 나왔다는 것은, 초기 도입자가 마주칠 만한 코너 케이스가 빠르게 정리되고 있다는 뜻이다. 운영에 올린다면 6.0.1 이후를 기준으로 가는 편이 낫다.

그리고 의존성 baseline. 이건 마이그레이션을 마음먹기 전에 먼저 확인할 줄 한 줄이다.

| 항목 | 5.x | 6.0 |
|------|-----|-----|
| Java | 17+ | 17+ |
| Spring Framework | 6.x | **7.0** |
| Spring Boot | 3.x | **4.0** |
| Spring Data | 3.x | **4.0** |
| Spring Integration | 6.x | **7.0** |
| Spring AMQP / Kafka | 3.x | **4.0** |
| Micrometer | 1.13~ | **1.16** |
| Jackson | 2.x | **3.x** (2.x deprecated) |

Java 17은 5.x와 같다. 그래서 "Java 21을 강제하지 않는다"는 점이 다행이다. 하지만 Spring Framework 7과 Spring Boot 4가 함께 올라간다는 것은, Spring Batch 6 마이그레이션이 단독 결정이 아니라 **Spring 진영 전체의 메이저 라인을 옮기는 결정**과 묶여 있다는 뜻이다. Boot 4를 미루고 싶다면 Batch 6도 미루자. 반대로 Boot 4로 가야 하는 이유가 있다면 Batch 6도 같이 가는 게 자연스럽다.

Jackson 3 전환도 작지 않다. ExecutionContext에 도메인 객체를 넣어두고 Jackson으로 직렬화·역직렬화하던 코드는 이번 기회에 한 번 점검해두는 편이 낫다. v5에서 v6로 직렬화 포맷이 호환되지 않는다는 점은 뒤에서 자세히 다룬다.

## 가장 큰 변화: chunk-oriented 모델의 재설계

Spring Batch 6에서 가장 중요한 변경 하나만 꼽으라면 이것이다. **chunk-oriented step의 골격이 바뀌었다.** 이전 모델의 핵심이었던 `ChunkOrientedTasklet`과 `TaskletStep` 조합이 deprecated되고, `ChunkOrientedStep` + `ChunkOrientedStepBuilder`라는 새 구조가 표준이 됐다.

먼저 코드부터 보자. 가장 작은 청크 step을 6 스타일로 짜면 이렇다.

```java
@Bean
public Step settlementStep(JobRepository jobRepository,
                           ItemReader<Settlement> reader,
                           ItemWriter<Settlement> writer) {
    return new ChunkOrientedStepBuilder<Settlement, Settlement>(
            "settlementStep", jobRepository, /* chunkSize */ 500)
        .reader(reader)
        .writer(writer)
        .build();
}
```

5에서 `StepBuilder.chunk(500, transactionManager)` 식으로 짜던 그 자리다. 같은 일을 한다. 그런데 왜 갈아엎었을까?

Spring Batch 측이 공식적으로 든 이유가 세 가지다. 하나, **`maxItemCount`가 멀티스레드 step에서 지켜지지 않는 버그가 있었다.** 상한 1만 건을 걸어둔 잡이 멀티스레드를 켜는 순간 그 상한을 약간씩 초과하는 일이 보고됐다. 이전 모델은 항목 카운트를 reader 쪽에서 세고 있었는데, 멀티스레드 환경에서 카운트와 read 호출 사이에 race가 났다. 둘, **롤백 시 상태가 어긋나서 optimistic locking 이슈를 일으켰다.** 청크가 롤백된 뒤 다음 청크로 진입할 때, 이전 시도의 상태가 깨끗이 정리되지 않은 채 남아 두 번째 시도가 버전 충돌을 보는 식이었다. 셋, **throttle 동작이 부정확했다.** 동시 실행 수를 제한하려고 해도 실측 throughput이 설정값과 어긋나는 케이스가 있었다.

이 셋을 한 번에 풀려고 동시성 모델 자체를 갈아엎었다. 6.0의 멀티스레드 step은 이제 **producer-consumer + bounded queue** 구조다. producer 한 개가 reader에서 읽어 큐에 푸시하고, consumer N개가 큐에서 꺼내 process → write를 진행한다. 청크가 차서 write가 도는 동안에는 producer가 잠깐 멈춘다. 큐가 bounded라서 메모리 폭주를 자체 차단한다. 이전의 "parallel iteration"보다 코드와 상태 동기화가 단순해지고, 위 세 이슈가 한 번에 풀렸다는 것이 변경 동기다.

여기서 한 가지 짚어두자. 모델이 바뀌었다고 해서 우리가 짜는 application 코드가 크게 바뀌는 건 아니다. Reader/Processor/Writer 계약은 그대로다. 빌더 진입점 한 줄과 import 몇 개가 바뀐다고 보면 된다. 하지만 직접 청크 처리 흐름을 커스터마이즈하던 코드 — 예를 들어 `ChunkOrientedTasklet`을 상속해서 chunk 처리에 hook을 끼워넣었던 코드 — 가 있다면, 그건 거의 다시 써야 한다. 다행히 한국 커뮤니티에 그런 코드는 많지 않다. 대부분의 운영 잡은 빌더만 쓴다.

## 동시성 모델: producer-consumer + bounded queue

producer-consumer 모델을 한 번 더 풀어보자. 멀티스레드 step을 안 쓸 거라면 이 절은 가볍게 보고 넘어가도 좋다. 8장에서 더 자세히 다룬다. 다만 "왜 6에서 모델을 바꿨는지"를 한 번은 머릿속에 그려두자.

이전 모델은 N개의 스레드가 각자 reader.read() → process() → write() 사이클을 돌았다. 모든 스레드가 reader를 공유했고, 각자 자기 청크 크기만큼 누적해서 write로 보냈다. 문제는 reader 호출이 N개 스레드 사이에서 race가 난다는 것이고, 멈추지 않고 read를 계속하다 보니 producer 측의 항목 카운트가 어긋날 여지가 컸다.

6의 모델은 이렇다.

```
[reader] → producer 1 → [bounded queue, 크기 K] → consumer N → [process → write]
```

producer가 한 명이라 reader 호출은 thread-safe하지 않아도 된다. 큐가 bounded라서 consumer가 느리면 producer가 자연스럽게 backpressure를 받는다. consumer N개는 자기 청크를 모아 write로 진행하고, write 사이엔 트랜잭션 경계가 자연스럽게 잡힌다.

이 모델의 부수효과로 **stateful Reader 사용이 멀티스레드에서 한결 안전해졌다.** 단 "안전해졌다"가 "안전하다"는 아니다. 8장에서 보겠지만, 멀티스레드 step에서 stateful Reader를 쓰는 건 여전히 권장 패턴이 아니다. restartability가 약화되기 때문이다. 데이터를 정말 분할 처리하고 싶다면, 멀티스레드 step보다 partitioning을 보는 편이 낫다.

## `JobOperator`로의 통합 — `JobLauncher`와 `JobExplorer`를 흡수

다음으로 큰 변화는 인터페이스 통합이다. 5에서는 다음 셋을 따로 다뤘다.

- **JobLauncher** — 잡을 시작.
- **JobExplorer** — 잡 메타데이터를 조회.
- **JobOperator** — 외부에서 잡을 컨트롤(stop, restart 등).

이 셋이 6에서 하나로 합쳐졌다. **`JobOperator`가 launch + explore + control을 다 한다.** 그리고 `JobRepository`가 `JobExplorer`의 인터페이스를 흡수한다. 즉 6에서는 `JobLauncher`/`JobExplorer` 빈을 따로 등록할 필요가 없다.

5에서 이렇게 짠 코드가 있다고 해보자.

```java
// 5.x 스타일
@Service
public class SettlementService {
    private final JobLauncher jobLauncher;
    private final JobExplorer jobExplorer;
    private final Job settlementJob;

    public void runSettlement(LocalDate date) throws Exception {
        JobParameters params = new JobParametersBuilder()
            .addString("date", date.toString())
            .toJobParameters();
        jobLauncher.run(settlementJob, params);
    }

    public List<JobExecution> recentRuns() {
        return jobExplorer.findJobExecutions(...);
    }
}
```

6에서는 이렇게 단순해진다.

```java
// 6.0 스타일
@Service
public class SettlementService {
    private final JobOperator jobOperator;
    private final Job settlementJob;

    public long runSettlement(LocalDate date) throws Exception {
        JobParameters params = new JobParametersBuilder()
            .addString("date", date.toString())
            .toJobParameters();
        return jobOperator.start(settlementJob, params);
    }

    public Collection<JobExecution> recentRuns() {
        return jobOperator.getJobExecutions(...);
    }
}
```

빈 두 개가 한 개로 줄었다. 그리고 `start`/`stop`/`restart`/`abandon`/`recover`가 한 인터페이스에 모인다. 외부 API에서 잡을 제어하는 컨트롤러를 짜본 사람이라면 이 통합이 얼마나 자연스러운지 알 것이다.

마이그레이션 측면에서 보면, 5.x 코드의 `JobLauncher` 주입을 `JobOperator`로 바꾸는 일은 거의 기계적이다. `run(...)`이 `start(...)`로 이름이 바뀌었다. 메서드 시그니처와 반환 타입이 약간 다르므로 IDE의 inspection을 따라가면 된다. 11장의 마이그레이션 코드 diff에서 다시 본다.

## `JobOperator#recover()` — STARTED 박제 문제의 표준 해결

이 한 줄짜리 메서드가 6.0의 가장 사랑받는 변화 중 하나다. 운영을 해본 사람만 그 가치를 안다.

상황을 그려보자. 새벽 3시에 정산 잡이 돌고 있다. 컨테이너가 OOM으로 SIGKILL을 받는다. JVM이 graceful shutdown 훅도 못 돌리고 즉사한다. 다음날 아침 출근해서 잡 상태를 확인하면 — `BATCH_JOB_EXECUTION` 테이블에 `STARTED` 상태가 박제되어 있다. 잡을 재시작하려고 하면 "이미 동일 인스턴스가 실행 중"이라고 거부당한다.

5.x에서는 이걸 어떻게 풀었나? 두 가지 길이 있었다.

```sql
-- 길 1: DB를 직접 손댄다
UPDATE BATCH_JOB_EXECUTION
SET STATUS = 'FAILED', END_TIME = NOW(), VERSION = VERSION + 1
WHERE JOB_EXECUTION_ID = ?;
```

운영 DB에 들어가 UPDATE를 친다. 박력 있다. 그런데 새벽 3시에 졸린 눈으로 이걸 짜는 게 정답일 리 없다. 자칫 WHERE를 빼면 박제 정리가 아니라 **모든 STARTED를 한꺼번에 FAILED로 만드는 사고**다. 한 번이라도 그 직전까지 가본 사람은 안다 — 이 길은 찜찜하다.

길 2는 직접 유틸리티를 짜는 것이었다. 회사마다 비슷한 코드가 굴러다닌다. "특정 조건의 STARTED를 FAILED로 마킹하는 어드민 API." 이게 표준이 아니라 직접 짠 코드라는 게 문제다. 직접 짜고 돌려놓은 회사가 한국에 몇 군데인지 헤아릴 수가 없다.

6.0에서는 이렇게 끝난다.

```java
jobOperator.recover(executionId);
```

한 줄이다. `SimpleJobOperator`도 구현하고 `CommandLineJobOperator`도 구현한다. K8s에서는 더 흥미로운 패턴이 가능해진다 — Pod이 시작될 때 자기와 묶인 잡 인스턴스 중 STARTED 박제를 자동으로 recover하는 init 절차. 매번 사람이 DB를 손보는 운영은 정말 운영이 아니라는 점을, 6.0은 한 메서드로 인정한 셈이다.

이 메서드의 자세한 운영 패턴은 10장에서 K8s와 함께 다룬다. 여기서는 "있다는 사실"과 "왜 들어왔는지"만 기억해두자.

## Graceful Shutdown — K8s 운영자에게 가장 중요한 한 줄

`recover()`와 짝을 이루는 또 하나의 변화가 graceful shutdown이다. JVM이 종료 신호(SIGTERM)를 받으면 6.0의 Spring Batch는 다음과 같이 동작한다.

1. 실행 중인 Job/Step에 중단 신호를 전달.
2. 현재 처리 중인 청크는 끝낸다 (트랜잭션은 커밋한다).
3. JobRepository에 일관된 상태(`STOPPED`)를 기록.
4. JVM 종료.

그러니까, **종료 신호 → 진행 중 청크 안전 종료 → 메타 일관성 보장 → exit**라는 한 호흡이 표준화됐다. 이전엔 이게 잡마다 별도 코드였고, 잘못 짜면 메타가 어긋나서 다음 실행이 거부됐다. 6.0이 정식 셧다운 훅을 제공한 것은 K8s 운영자에게 가장 큰 선물이다.

`StoppableStep`이라는 인터페이스도 함께 들어왔다. 이전엔 Tasklet 기반 step만 `JobOperator#stop`에 응답할 수 있었다. 청크 step은 reader/processor/writer 사이클이 자체적으로 돌아서, 외부 stop 신호를 받아주는 표준 구멍이 없었다. 6에서는 `StoppableStep`을 구현하면 어떤 종류의 step이든 외부 stop에 응답한다. 청크 사이클의 적절한 지점에서 stop 플래그를 체크해 안전하게 종료한다.

이게 왜 중요한가? K8s가 Pod을 종료할 때 보내는 SIGTERM의 의미를 그대로 받아주기 때문이다. terminationGracePeriodSeconds 동안 잡은 자기 청크를 끝내고 메타를 정리한 뒤 정상 종료한다. 시간이 모자라 SIGKILL을 받을 때만 STARTED 박제가 생기고, 그건 다음 Pod에서 `recover()`로 푼다. 이 흐름이 매끄러워진 것이 6.0의 운영 가치다. 자세한 K8s 매니페스트는 10장에서 다룬다.

## `JobRepository` ⊃ `JobExplorer` 통합

`JobOperator`가 `JobLauncher`/`JobExplorer`를 흡수한 것과 짝지어, 저장소 인터페이스도 정리됐다. 6에서는 **`JobRepository`가 `JobExplorer`의 메서드를 함께 노출한다.** 별도 `JobExplorer` 빈을 등록할 필요가 없다.

이게 의미가 작지 않다. 5에서는 `JobRepository`(쓰기 + 일부 조회)와 `JobExplorer`(읽기)가 따로 있어서, "이 메서드는 어디 있더라"를 매번 헷갈렸다. 잡 실행 이력을 조회하려고 `JobRepository`를 봤다가 메서드가 없어서 `JobExplorer`로 옮겨가는 일이 흔했다. 6에서는 그 모호함이 사라진다. 메타데이터에 관한 모든 건 `JobRepository`다.

`JobRepositoryFactoryBean`도 이름이 바뀌었다. JDBC 백엔드를 쓴다면 `JdbcJobRepositoryFactoryBean`이고, MongoDB를 쓴다면 다른 팩토리 빈이다. 즉 백엔드별로 명시적으로 갈렸다. 이게 다음 변경과 짝지어 의미가 살아난다.

## `@EnableJdbcJobRepository` / `@EnableMongoJobRepository` — 어노테이션 분리

5까지는 `@EnableBatchProcessing` 하나가 거의 모든 일을 했다. JobRepository, JobLauncher, transactionManager 빈을 자동으로 깔아주고, 거기에 dataSource를 물려서 잡 인프라를 완성했다.

6에서는 이게 두 갈래로 갈라진다.

- `@EnableBatchProcessing` — 공통 인프라(taskExecutor 등)만 담당.
- `@EnableJdbcJobRepository(dataSourceRef=..., transactionManagerRef=...)` — JDBC 백엔드 전용.
- `@EnableMongoJobRepository(...)` — MongoDB 백엔드 전용.

코드로는 이런 모양이다.

```java
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

왜 갈라졌을까? 5.2에서 MongoDB JobRepository가 정식 지원되면서, 한 어노테이션이 두 백엔드를 동시에 알고 있는 구조가 어색해졌다. 어떤 dataSource를 쓸지, 어떤 transactionManager를 쓸지, 백엔드 종류에 따라 달라야 하는데, 한 어노테이션 안에 그걸 다 욱여넣으려니 옵션이 부풀었다. 6에서는 백엔드 종류 자체를 어노테이션 이름에 박아버렸다.

이게 한국 운영 환경에 미치는 영향은 크지 않다. 대부분 RDB 기반이고 JDBC 백엔드를 쓴다. 마이그레이션 시 `@EnableBatchProcessing` 옆에 `@EnableJdbcJobRepository`를 한 줄 더 붙이면 끝이다.

다만 한 가지, **`@EnableBatchProcessing(modular = true)`는 deprecated됐다.** modular 모드는 여러 잡 컨텍스트를 격리하기 위한 옵션이었는데, 6에서는 Spring 컨텍스트 계층 + `GroupAwareJob`을 쓰라는 권고로 바뀌었다. modular를 쓰던 코드가 있다면 11장 마이그레이션 절을 참조하자. 흔한 패턴은 아니다.

그리고 한국 입문자가 자주 묻는 질문 하나 — **Spring Boot 3 이상에서는 `@EnableBatchProcessing`을 직접 붙이는 것이 discouraged**다. `BatchAutoConfiguration`이 자동 구성하는데, 직접 붙이면 자동 구성을 끄게 되기 때문이다. 6에서도 이 권고는 그대로다. Boot 환경이라면 어노테이션 두 개(`@EnableBatchProcessing` + `@EnableJdbcJobRepository`)를 모두 떼고, application.yml의 `spring.batch.*` 속성으로만 설정하는 편이 낫다. 그게 Boot의 기본 가정이다.

## MongoDB JobRepository — 정식 지원

5.2에서 도입돼 6.0에서 자리를 잡은 변화. 그동안 Spring Batch는 메타데이터 저장소로 RDB를 가정했다. NoSQL만 쓰는 시스템은 별도 RDB를 띄워서 메타만 저장하는 구조를 짜야 했고, 그게 운영 부담이었다.

6에서는 다음 세 가지가 갖춰지면 MongoDB JobRepository를 1급 시민으로 쓸 수 있다.

```java
@Configuration
@EnableBatchProcessing
@EnableMongoJobRepository(mongoOperationsRef = "mongoTemplate")
public class MongoBatchConfig {
    @Bean
    public MongoTemplate mongoTemplate(MongoClient client) { ... }

    @Bean
    public MongoTransactionManager mongoTransactionManager(MongoClient client) { ... }
}
```

조건은 MongoDB 4 이상(트랜잭션 지원). 한국 production 후기는 아직 많지 않다 — 5.2부터 도입된 기능이라 시간이 더 필요하다. 도입을 검토 중이라면, 이 책의 다음 판본까지는 영문 자료와 GitHub Discussion 위주로 follow-up하는 편이 낫다. 정직하게 말해서, 6.0 시점의 한국 production 사례는 아직 누적 중이다.

## 도메인 모델·`JobParameters` 재설계 — record화와 primitive long 전환

이 절은 6.0에서 가장 의미 변화가 큰 부분이고, **마이그레이션의 1차 위험 지점**이다. 자기 코드에 영향을 줄지 안 줄지를 가르는 대목이라 자세히 짚어두자.

### 엔티티 ID: `Long` → `long`

5에서는 `JobInstance#getId()`, `JobExecution#getId()`, `StepExecution#getId()`가 모두 `Long`(wrapper)을 반환했다. 6에서는 모두 **primitive `long`**으로 바뀌었다. 의미상 의도는 분명하다 — null을 허용하지 않겠다는 것이다. 박제된 잡 인스턴스의 ID가 null인 케이스가 있어선 안 된다는 합의가 6에 와서 신호로 박혔다.

```java
// 5.x
Long executionId = jobExecution.getId();  // null 가능성 있었음

// 6.0
long executionId = jobExecution.getId();  // primitive, null 불가
```

코드 영향은 작아 보이지만, 박싱/언박싱 경계에 있는 코드는 한 번 점검할 필요가 있다.

```java
// 5에서 멀쩡히 돌던 코드
Map<Long, String> executionToStatus = new HashMap<>();
executionToStatus.put(jobExecution.getId(), "ok");

// 6에서도 컴파일은 되지만, 자동 박싱이 일어난다
// 의미는 같지만, IDE 경고가 뜰 수 있다
```

더 위험한 건 ID를 null과 비교하던 코드다.

```java
// 5에서는 의미 있었던 코드
if (jobExecution.getId() != null) { ... }

// 6에서는 항상 true다 — 컴파일러가 경고를 띄운다
```

또 하나, **ID 재할당 불가**. 도메인 객체에 ID를 setter로 다시 박는 코드가 있었다면 6에서는 작동하지 않는다. 부모 없는 orphan 엔티티 생성도 막혔다 — 즉 JobInstance 없는 JobExecution을 코드로 만들어내려는 시도는 컴파일/런타임에서 차단된다. 정상적인 운영 코드에서는 만날 일이 없지만, 테스트 픽스처에서 도메인 객체를 손으로 만들던 코드가 있다면 7장의 `MetaDataInstanceFactory`를 참조해 픽스처를 짜자.

### `JobParameter` — record화

이게 가장 흥미로운 변경이다. 5에서 `JobParameter`는 클래스였다.

```java
// 5.x
public class JobParameter {
    private final Object value;
    private final ParameterType type;
    private final boolean identifying;
    // getters, equals, hashCode, ...
}
```

6에서는 record로 갈아엎었다.

```java
// 6.0
public record JobParameter<T>(T value, Class<T> type, boolean identifying) { }
```

타입 파라미터가 들어온 게 큰 변화다. `JobParameter<String>`, `JobParameter<Long>`, `JobParameter<LocalDate>` 식으로 컴파일 시점에 타입이 박힌다. 5에서는 `Object value`였고 꺼낼 때 캐스팅을 했는데, 6에서는 그게 필요 없다.

`JobParameters`도 같이 바뀌었다. 5에서는 `Map<String, JobParameter>`였다. 6에서는 **`Set<JobParameter>` 기반**이고, 파라미터의 이름(name)은 JobParameter 자체가 가진다. 즉 이름·값·타입·identifying 여부가 한 record에 다 모인다.

이게 왜 record로 바뀌었는지 의도를 정리하자면 네 가지다.

1. **불변성** — record는 본질적으로 불변. 잡이 시작된 뒤 파라미터가 바뀌는 일은 절대 일어나선 안 되는 일이다. 타입 시스템에서 그걸 보장하게 만들었다.
2. **null safety** — JSpecify와의 정합. 6.0은 null 안정성을 한층 강화했다(곧 다룬다). record는 그 흐름과 자연스럽게 맞물린다.
3. **Jackson 3 직렬화 표준화** — record는 Jackson 3에서 직렬화·역직렬화가 깔끔하다. ExecutionContext에 JobParameters를 저장할 때 포맷이 일관된다.
4. **타입 파라미터** — 캐스팅 없는 값 접근이 가능해졌다.

그런데 4번이 곧 다음 문제로 이어진다.

### v5 직렬화 비호환 — 마이그레이션의 1차 위험 지점

`JobParameter`가 record로 바뀌면서 직렬화 포맷도 바뀌었다. 결과는 분명하다.

> **v5에서 실패한 JobInstance는 v6에서 재시작 불가.**

운영 측면에서 이게 의미하는 바는 뼈아프다. 5.x로 돌리던 잡을 6으로 올리고 싶은데, BATCH_JOB_EXECUTION에 `FAILED`로 남아있는 옛 인스턴스는 재시작할 수 없다. 6의 코드가 5에서 직렬화한 JobParameters를 역직렬화할 수 없기 때문이다. ExecutionContext에 v5 포맷으로 저장된 도메인 객체도 마찬가지다.

마이그레이션을 결정한 시점에 해야 할 운영적 합의 한 줄이 이것이다.

> "6으로 올리기 전에, **5에서 실패한 잡은 5에서 끝낸다.**"

말이 쉽지, 실제로는 다음 단계를 밟는 일이다. (자세한 시나리오는 11장에서 코드 diff와 검증 SQL과 함께 풀어낸다. 여기서는 신호만.)

1. 마이그레이션 사전에 모든 STARTED 박제를 정리한다 — 5.x의 운영 유틸로 FAILED 마킹.
2. FAILED 인스턴스 중 재시작이 필요한 건 5.x에서 모두 재시작해 SUCCESS로 마무리한다.
3. 더 이상 재시작이 의미 없는 FAILED는 운영 합의로 그대로 둔다(메타로만 남김).
4. 그 시점에 6으로 올린다.

만약 진행 중인 5.x 잡을 그대로 둔 채 6으로 올렸다면? 그 잡들은 6에서 영영 재시작되지 않는다. 메타데이터 청소나 폐기가 유일한 길이다. 운영 중인 시스템이라면, 이 사실을 마이그레이션 계획서 첫 줄에 적어두자.

이 부분이 6의 모든 변경 중 가장 먼저 점검해야 하는 항목이다. 직렬화 비호환은 코드 변경이 아니라 **운영 절차의 변경**을 강제한다. 도메인 모델 record화는 멋진 설계지만, 그 멋이 운영자에겐 실재하는 부담으로 도착한다.

### 영향 범위 — 어디를 살펴봐야 하나

자기 코드에서 다음을 점검해두자.

- **커스텀 Listener** — `JobExecutionListener`, `StepExecutionListener` 안에서 `getId()`를 `Long`으로 받아 처리하는 코드. 박싱/언박싱 경계 NPE 위험.
- **ExecutionContext에 도메인 객체 저장** — `executionContext.put("jobInstance", jobInstance)` 같은 코드가 있다면, 직렬화 포맷이 바뀌었으니 5에서 저장한 컨텍스트는 6에서 못 읽는다.
- **JobParameters 직접 빌드** — 테스트 코드에서 `new JobParameter(...)`를 직접 호출하는 자리. record 시그니처에 맞춰 다시 짠다.
- **JobParameters를 캐스팅으로 꺼내던 코드** — 5에서 `(String) jobParameters.getString("date")` 식의 코드. 6에서는 타입이 박혀 캐스팅이 필요 없거나 시그니처가 달라진다.

11장 마이그레이션 표에서 이 영향 범위를 코드 diff로 다시 정리한다.

## fault-tolerance 재구성 — Spring Retry에서 Spring Framework 7 retry로

5까지 Spring Batch의 retry는 외부 라이브러리인 **Spring Retry**에 의존했다. 별도 GroupId(`org.springframework.retry`)였고, Spring Batch가 그걸 쓰는 구조였다.

6에서는 이게 갈라섰다. Spring Framework 7에 retry 기능이 들어가면서, Spring Batch는 외부 Spring Retry 의존을 떼고 Framework 7의 retry 위로 옮겨갔다. 빌더 API도 새 모양이다.

```java
// 5.x — Spring Retry 기반
@Bean
public Step step(...) {
    return stepBuilder.<Item, Item>chunk(100, txManager)
        .reader(reader).writer(writer)
        .faultTolerant()
        .retry(TransientException.class).retryLimit(3)
        .skip(FlatFileParseException.class).skipLimit(50)
        .build();
}

// 6.0 — Spring Framework 7 retry
@Bean
public Step step(JobRepository jobRepository,
                 ItemReader<Item> reader,
                 ItemWriter<Item> writer) {
    RetryPolicy retryPolicy = RetryPolicy.builder()
        .maxRetries(3)
        .includes(Set.of(TransientException.class))
        .build();

    SkipPolicy skipPolicy = new LimitCheckingExceptionHierarchySkipPolicy(
        Set.of(FlatFileParseException.class),
        50
    );

    return new ChunkOrientedStepBuilder<Item, Item>("step", jobRepository, 100)
        .reader(reader).writer(writer)
        .faultTolerant()
            .retryPolicy(retryPolicy)
            .skipPolicy(skipPolicy)
        .build();
}
```

핵심은 `RetryPolicy.builder()`로 정책 객체를 먼저 만들고, 빌더의 `.retryPolicy(...)`로 꽂는다는 점이다. 5에서 `.retry(...).retryLimit(...)` 체인을 한 줄에 흐르게 적던 스타일과 모양이 다르다. 정책이 분리된 객체가 됐다는 게 의미가 있다 — 정책을 재사용하기도, 테스트하기도 더 쉽다.

skip도 비슷한 구조다. `SkipPolicy` 인터페이스 하나로 통합됐고, `LimitCheckingExceptionHierarchySkipPolicy` 같은 표준 구현이 있다. 직접 구현한 SkipPolicy가 있다면 시그니처를 점검하자.

이 변경은 Skip/Retry/Restart의 동작 자체를 바꾸지는 않는다. 정책을 표현하는 방식만 바뀐다. 그 동작 의미는 7장에서 본격적으로 다룬다.

## JFR 옵저버빌리티 — 6.0의 새 카드

Java Flight Recorder를 활용한 새 옵저버빌리티 채널이 들어왔다. Micrometer 메트릭은 그대로 있고, 그 위에 JFR 이벤트를 추가로 발행한다.

JFR 이벤트로 잡힌다는 건 다음을 의미한다.

- Job 시작/종료 이벤트.
- Step 시작/종료 이벤트.
- Item read/write 이벤트.
- **트랜잭션 경계 이벤트** — 청크가 시작될 때, 커밋될 때, 롤백될 때.

이게 왜 신선한가? Micrometer는 메트릭(카운트, 게이지, 히스토그램)을 모은다. 그래서 "잡이 1시간 걸렸다"는 알지만 "그 1시간 안에 어느 청크에서 어느 트랜잭션이 어떻게 흘렀는지"를 추적하려면 별도 로그 인프라가 필요했다. JFR은 그 저수준 흐름을 시간 축에 박아서 남긴다. JDK Mission Control이나 JProfiler 같은 도구로 .jfr 파일을 열면 트랜잭션 경계가 그대로 보인다.

오버헤드는 명시적으로 "minimal"이라고 적혀 있다. JFR 자체가 JVM 내부에서 매우 가볍게 돌도록 설계됐다. production에서 상시 켜둘 수 있는 수준이다.

다만 **운영 사례가 아직 거의 없다.** 6.0이 GA된 직후라 한국에서도 영문권에서도 production 후기가 부족하다. 도입을 검토한다면 9장의 옵저버빌리티 절을 참조하고, 6.0.x 마이너가 더 누적된 뒤에 follow-up하는 편이 낫다. 이 책은 "신기능이 있다"는 사실을 정확히 전달하되, "어떻게 운영에 녹였더라"의 한국 사례는 다음 판본을 기약한다.

## JSpecify null 안정성

6.0에서 모든 public API에 **JSpecify** 어노테이션이 붙는다. `@Nullable`, `@NonNull` 같은 표준화된 null annotation이다.

```java
// 6.0 API doc 예시 (개념적)
@Nullable
JobInstance getLastJobInstance(String jobName);

@NonNull
JobExecution start(@NonNull Job job, @NonNull JobParameters parameters);
```

코드 동작이 바뀌지는 않는다. 그러나 IntelliJ나 Errorprone과 같은 도구가 컴파일 시점에 null 위반을 잡아준다. 다음 같은 코드가 IDE에서 빨갛게 표시된다.

```java
JobInstance last = jobOperator.getLastJobInstance("settlementJob");
String name = last.getJobName();  // last가 @Nullable인데 null 체크 없이 호출 — IDE 경고
```

운영하다 보면 NPE는 결국 아무도 막지 못한 어둠 속 길에서 만난다. 정적 분석이 한 자리라도 더 켜진다는 건 그만큼 어둠이 줄어든다는 뜻이다. record화와 함께, 6.0의 도메인 모델은 한층 단단해졌다.

## 람다 스타일 빌더

작은 변화지만 코드 가독성에 도움이 된다. 빌더 코드를 컨텍스추얼 람다로 더 간결하게 쓸 수 있다.

```java
// 5.x 스타일
FlatFileItemReader<Customer> reader = new FlatFileItemReaderBuilder<Customer>()
    .name("customerReader")
    .resource(new ClassPathResource("customers.csv"))
    .delimited()
        .delimiter(",")
        .quoteCharacter('"')
        .names("id", "name", "email")
    .targetType(Customer.class)
    .build();

// 6.0 스타일 — 람다로 분리된 영역이 명시적
FlatFileItemReader<Customer> reader = new FlatFileItemReaderBuilder<Customer>()
    .name("customerReader")
    .resource(new ClassPathResource("customers.csv"))
    .delimited(c -> c
        .delimiter(",")
        .quoteCharacter('"')
        .names("id", "name", "email"))
    .targetType(Customer.class)
    .build();
```

`delimited(...)` 같은 빌더 진입점이 람다를 받아 그 안에서 sub-builder를 구성한다. 들여쓰기 한 단계 안에 관련된 설정이 묶여 보인다. 의무 사항은 아니다 — 5.x 스타일도 6에서 그대로 동작한다. 다만 새 코드를 짠다면 람다 스타일이 가독성에서 한 발 앞선다.

## 신규 `CommandLineJobOperator`

CLI에서 잡을 띄우는 진입점이 새로 들어왔다. 이전 산물인 `CommandLineJobRunner`를 대체한다.

```bash
java -jar settlement-batch.jar \
    --spring.batch.job.name=settlementJob \
    settlement.date=2026-05-08
```

start, stop, restart 표준 옵션을 제공한다. Spring Boot CLI 컨벤션과 정합한다.

이 도구가 단독으로 의미 있는 자리는 K8s `CronJob`의 `command:` 필드다. K8s가 스케줄링하면서 Pod을 띄울 때, `CommandLineJobOperator`가 잡 진입점이 된다. JobParameters는 ConfigMap이나 환경 변수로 주입한다. 자세한 매니페스트 패턴은 10장에서 풀어낸다. 여기서는 "표준 CLI 진입점이 들어왔다"는 사실만 짚어두자.

## Remote Step (6.0 신규) — 분산 실행의 한 카드 더

5까지 Spring Batch의 분산 실행 옵션은 Multi-thread step / Partitioning / Remote Chunking 셋이었다. 6에서 **Remote Step**이 추가됐다. Step 자체를 다른 노드에서 통째로 실행한다. Partitioning이 한 step을 N개의 워커 step으로 분할 실행한다면, Remote Step은 **step 단위로 분산**한다.

이 카드가 어디에 쓸모가 있을까? 잡 안의 어떤 step은 GPU 노드에서, 어떤 step은 메모리 큰 노드에서 돌리고 싶을 때. 또는 step별로 처리량 특성이 매우 달라서 노드를 분리하고 싶을 때. 분산 환경에서 더 자유로운 분배가 가능해진다.

Local Chunking, Remote Step, SEDA via Spring Integration까지를 묶어 6.0의 분산 실행 카드는 한층 풍성해졌다. 어떤 카드를 언제 꺼낼지에 대한 결정 트리는 8장에서 자세히 본다. 여기서는 "Remote Step이라는 새 카드가 들어왔다"는 신호만 받아두자.

## 패키지 이동 — 마이그레이션의 잔잔한 부담

가장 사소해 보이지만 실제 마이그레이션에서 가장 많은 시간을 잡아먹는 부분이 패키지 이동이다. 대표 사례를 묶어보자.

| 5.x | 6.0 |
|-----|-----|
| `org.springframework.batch.*` | `org.springframework.batch.infrastructure.*` |
| `org.springframework.batch.core.explore` | `org.springframework.batch.core.repository.explore` |
| `org.springframework.batch.core.partition.support` | `org.springframework.batch.core.partition` |
| `JobRepositoryFactoryBean` | `JdbcJobRepositoryFactoryBean` |
| `JobExplorerFactoryBean` | `JdbcJobExplorerFactoryBean` |
| `ChunkHandler` | `ChunkRequestHandler` |
| `JobStep.setJobLauncher(JobLauncher)` | `JobStep.setJobOperator(JobOperator)` |

DB 시퀀스 이름도 바뀌었다.

| 5.x 시퀀스 | 6.0 시퀀스 |
|-----------|-----------|
| `BATCH_JOB_SEQ` | `BATCH_JOB_INSTANCE_SEQ` |
| `BATCH_JOB_EXECUTION_SEQ` | `BATCH_JOB_EXECUTION_SEQ` (그대로) |
| `BATCH_STEP_EXECUTION_SEQ` | `BATCH_STEP_EXECUTION_SEQ` (그대로) |

운영 DB에 Flyway/Liquibase로 시퀀스 리네임 SQL을 넣어줘야 한다. 이걸 잊으면 잡 시작 시 `BATCH_JOB_SEQ`를 못 찾아 즉시 실패한다. 11장 마이그레이션 절에 SQL 예시를 둔다.

다행히 import 정리는 IDE의 자동 import 정리 기능으로 거의 다 해결된다. 한 번 빌드를 돌려서 컴파일 에러를 모은 뒤, IntelliJ의 "Auto Import" 또는 Ctrl+Alt+O로 일괄 처리하면 90%는 처리된다. 남는 10%가 손으로 봐야 하는 자리다.

## deprecation 한눈에

6.0에서 새로 deprecated된 항목을 모아두자.

- `@EnableBatchProcessing(modular=true)` — 컨텍스트 계층 + GroupAwareJob으로 대체.
- `batch:` / `batch-integration:` XML 네임스페이스 — v7에서 제거 예정. 자바 설정 또는 어노테이션 설정으로 옮기자.
- JUnit 4 지원 (`spring-batch-test`) — JUnit 5로.
- Jackson 2.x — Jackson 3.x로.
- `ChunkOrientedTasklet` — `ChunkOrientedStep` + `ChunkOrientedStepBuilder`로.
- `JobLauncher`, `JobExplorer` — `JobOperator` + `JobRepository`로.

deprecated가 곧 제거는 아니다. 6.x 기간 동안은 동작한다. 다만 다음 메이저(v7)에서는 사라질 예정이라는 신호다. 마이그레이션을 한 번에 깨끗이 하고 싶다면 deprecated된 자리를 모두 정리해두는 편이 낫다.

## 정리: 6의 변경을 한 줄씩

이 장에서 다룬 것을 한 페이지에 모아두자. 마이그레이션을 검토할 때 체크리스트로 쓸 수 있다.

**구조 변화**

- chunk-oriented 모델 재설계 — `ChunkOrientedStep` + `ChunkOrientedStepBuilder`.
- 동시성 모델 — producer-consumer + bounded queue.
- `JobOperator`로의 통합 — `JobLauncher`/`JobExplorer` 흡수.
- `JobRepository` ⊃ `JobExplorer`.
- `@EnableJdbcJobRepository` / `@EnableMongoJobRepository` 분리.
- MongoDB JobRepository 정식 지원.

**도메인 모델**

- 엔티티 ID `Long` → `long` (primitive).
- `JobParameter` record화, `JobParameters`는 `Set<JobParameter>` 기반.
- v5 직렬화 비호환 — 마이그레이션 1차 위험 지점.

**운영**

- `JobOperator#recover()` — STARTED 박제 자동 정리.
- Graceful shutdown — SIGTERM 안전 종료.
- `StoppableStep` — 어떤 step이든 외부 stop 응답.
- 신규 `CommandLineJobOperator` — K8s CronJob 친화 CLI.

**옵저버빌리티**

- JFR 이벤트 — 트랜잭션 경계까지 추적 가능.
- JSpecify null 안정성.

**fault-tolerance**

- Spring Retry 의존 제거, Spring Framework 7 retry로.
- `RetryPolicy.builder()` + `SkipPolicy` 표준화.

**기타**

- 람다 스타일 빌더.
- Remote Step 추가.
- 패키지 이동, 시퀀스 이름 변경 (`BATCH_JOB_SEQ` → `BATCH_JOB_INSTANCE_SEQ`).
- `@EnableBatchProcessing(modular=true)`, XML 네임스페이스, JUnit 4, Jackson 2 deprecation.

여기까지가 6의 큰 그림이다. 이 변경들이 머릿속에 들어왔다면, 다음 장으로 넘어갈 준비가 됐다. 카카오페이 정산 사례를 backbone으로 — production 시스템이 50,000건 1시간 처리에서 어떻게 한 호흡에 10배가 빨라졌는지를 단계별로 풀어내자. 6의 변경점이 어떻게 실전에서 쓰이는지가 그 사례의 모든 단계에 녹아 있다.

마이그레이션 자체의 코드 diff와 검증 SQL은 11장에서 다룬다. 5장은 "왜"를, 11장은 "어떻게"를 책임진다. 둘은 짝이다.
