# 10장. K8s에서 운영하기 — CronJob, Graceful Shutdown, JobRepository 정리

이런 일이 한 번쯤 있었다고 해보자. 야간 정산 잡이 잘 돌고 있다가 어느 새벽 Pod이 OOM으로 강제 종료됐다. 다음 날 출근해보니 메타 테이블의 JobExecution은 STARTED로 박제돼 있고, 그날 스케줄에서 다시 돌아야 할 잡은 "이미 실행 중인 인스턴스가 있다"며 거부당한 상태다. 결국 운영자가 손으로 `BATCH_JOB_EXECUTION` 테이블을 UPDATE 쳐서 상태를 FAILED로 돌려놨고, 그 사이에 자동 알람도 한 차례 울었다. 누군가는 이걸 "운영"이라고 부른다.

조금 단호하게 말하자면, **사람이 매번 DB를 손봐야 하는 일은 운영이 아니다.** 그건 임시방편이고, 그 임시방편이 운영 패턴으로 굳어지는 순간 시스템은 사람의 새벽잠에 의존하는 인프라가 된다. K8s 위에서 Spring Batch를 production-ready로 돌린다는 건, 이런 사고가 났을 때 시스템 스스로 일어나도록 만들어 두는 일이다.

다행히 Spring Batch 6은 K8s 운영의 가장 아픈 두 자리에 표준 답을 들고 왔다. 하나는 graceful shutdown이고, 다른 하나는 `JobOperator#recover()`다. 거기에 K8s CronJob 패턴, JobRepository 정리, CommandLineJobOperator를 얹으면, "사람 없이 일어나는 잡"의 모양이 비로소 갖춰진다. 그 모양을 한 번에 그려보자.

## 10.1 K8s CronJob — Pod 하나 = 잡 하나

K8s에서 Spring Batch 잡을 스케줄링하는 표준 방식은 `CronJob` 리소스다. cron 표현으로 시각을 정해두면, 그 시각마다 K8s가 새 Pod을 띄우고, Pod 안에서 Spring Boot 애플리케이션이 부팅하면서 잡 한 개를 돌리고, 잡이 끝나면 Pod이 종료된다. 단순한 모양이지만, 이 단순함을 지키는 것이 cloud-native에서의 좋은 운영이다.

원칙 하나를 미리 박아두자 — **단일 Pod = 단일 Job**. 한 Pod 안에 여러 잡을 돌리거나, 한 Pod이 영구 데몬처럼 살면서 안에서 스케줄러를 돌리는 모양은 권장되지 않는다. K8s가 잘 다루지 못하는 패턴이다. 매 잡마다 새 Pod, 끝나면 종료, 다음 잡은 다음 Pod. 이 단순함이 graceful shutdown, recover, 자원 격리, 모니터링 모두에 결정적으로 유리하다.

### 10.1.1 가장 단순한 CronJob 매니페스트

야간 정산 잡을 매일 새벽 2시에 돌린다고 해보자. 가장 작은 CronJob이 다음과 같다.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: settlement-batch
  namespace: batch
spec:
  schedule: "0 2 * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 5
  startingDeadlineSeconds: 600
  jobTemplate:
    spec:
      backoffLimit: 0
      activeDeadlineSeconds: 7200
      template:
        spec:
          restartPolicy: Never
          terminationGracePeriodSeconds: 60
          containers:
            - name: settlement
              image: registry.example.com/settlement-batch:1.4.2
              args:
                - "--spring.batch.job.name=settlementJob"
                - "--targetDate=$(TARGET_DATE)"
              env:
                - name: TARGET_DATE
                  value: "$(date -d 'yesterday' +%Y-%m-%d)"
              resources:
                requests:
                  cpu: "1"
                  memory: "2Gi"
                limits:
                  memory: "4Gi"
```

여기서 신경 써야 할 필드 몇 가지를 짚어보자.

**`concurrencyPolicy: Forbid`.** 이전 잡이 아직 안 끝났는데 다음 스케줄이 도래하면 새 잡을 띄우지 않는다는 뜻이다. 정산처럼 같은 도메인 데이터를 두 잡이 동시에 만지면 안 되는 경우, 이 옵션이 안전 장치다. `Allow`(병행 실행)이나 `Replace`(이전 것 죽이고 새로 띄움)는 잡의 성격에 따라 골라야 하는데, 잡 하나의 신뢰성을 보장하는 입장에서는 `Forbid`가 기본값으로 적당하다.

**`backoffLimit: 0`.** K8s 입장에서의 재시도 횟수다. 0으로 두는 이유는, **K8s의 backoff와 Spring Batch의 restart는 의미가 완전히 다르기 때문**이다. K8s가 Pod을 죽였다 다시 띄우면 새 JobExecution이 생기는데, 그게 Spring Batch의 의도된 재시작과 어긋난다. 재시작은 Spring Batch가 자기 메타로 처리해야지, K8s가 단순 재실행으로 풀면 데이터가 망가질 수 있다. `backoffLimit: 0`이 그 경계를 명시한다.

**`restartPolicy: Never`.** 같은 맥락이다. Pod이 안에서 죽었을 때 K8s가 컨테이너만 재시작하지 못하도록 막는다. Pod이 죽으면 Pod 자체가 끝나고, 다음 스케줄에서 깨끗한 새 Pod이 올라오는 게 정석이다.

**`terminationGracePeriodSeconds: 60`.** Pod 종료 신호(SIGTERM)부터 SIGKILL까지의 유예 시간이다. 잡이 진행 중이라면 이 60초 안에 graceful shutdown이 진행돼야 한다. 잡 길이에 따라 늘려야 할 수도 있는데, 그 얘기는 다음 절에서.

**`activeDeadlineSeconds: 7200`.** 잡이 2시간 안에 끝나야 한다는 절대 데드라인. 정상 처리 시간이 50분이라면 2배 정도가 적당한 출발점이다. 데이터가 점점 늘면 이 값도 같이 키워야 하니, 알람과 함께 운영 항목으로 끼워두자.

### 10.1.2 ConfigMap / Secret으로 JobParameters 관리

JobParameters를 매니페스트 안에 하드코딩하면 잡마다 매니페스트를 복사해야 한다. ConfigMap이나 Secret에 모아두고 envFrom으로 주입하는 편이 깔끔하다.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: settlement-batch-config
data:
  CHUNK_SIZE: "500"
  PAGE_SIZE: "500"
  RETRY_LIMIT: "3"
```

```yaml
spec:
  containers:
    - name: settlement
      envFrom:
        - configMapRef:
            name: settlement-batch-config
        - secretRef:
            name: settlement-batch-secret
      args:
        - "--spring.batch.job.name=settlementJob"
        - "--chunkSize=$(CHUNK_SIZE)"
```

Helm 차트로 묶으면 환경별(stage, prod) 차이를 values.yaml로 관리할 수 있다. 운영이 익으면 자연스럽게 가게 되는 모양이다.

## 10.2 Graceful Shutdown — 60초의 운영 의미

Pod이 종료될 때 무슨 일이 벌어지는지를 한 번 따라가보자. K8s가 Pod에 SIGTERM을 보낸다. 컨테이너 안의 JVM은 SIGTERM을 받고 shutdown hook을 실행하기 시작한다. `terminationGracePeriodSeconds`가 정한 시간 안에 shutdown hook이 끝나면 정상 종료, 그 시간을 넘기면 SIGKILL이 와서 강제 종료다.

5.x까지 Spring Batch는 이 자리에 표준 답이 약했다. JVM이 종료되면 잡 스레드도 그냥 죽고, 진행 중이던 청크는 트랜잭션 롤백 정도만 처리되고, JobExecution은 STARTED인 채로 메타에 남았다. 그래서 노드 재부팅이나 Pod 재배포 한 번이면 운영자가 새벽에 호출되는 패턴이 굳었다.

6.0은 이 자리에 graceful shutdown hook을 정식으로 박았다. JVM 종료 신호가 오면 실행 중인 Job/Step에 인터럽트를 전달하고, 진행 중인 청크의 트랜잭션을 안전하게 마감하고, JobRepository에 일관된 상태를 기록한 뒤 종료한다. **K8s 환경에서 가장 큰 운영 차이를 만드는 변경 한 가지를 고르라면 이것이다.**

### 10.2.1 Spring Batch 6의 셧다운 훅 활용

Spring Boot 4 + Spring Batch 6 환경에서는 별도 코드를 쓰지 않아도 graceful shutdown이 동작한다. 다만 두 가지를 정렬해두자.

**첫째, `terminationGracePeriodSeconds`를 청크 길이에 맞춘다.** 청크 1개가 30초 걸리는 잡인데 grace period가 10초라면, graceful shutdown이 청크 마감을 기다리다가 SIGKILL을 맞는다. 결국 STARTED 박제다. 청크 1개의 평균 + 여유를 잡아 60~120초 정도로 두는 편이 안전하다.

**둘째, Spring Boot의 graceful shutdown 옵션을 켠다.** Web 서버용 옵션이지만, 잡 종료 흐름과 결을 같이 한다.

```yaml
server:
  shutdown: graceful
spring:
  lifecycle:
    timeout-per-shutdown-phase: 60s
```

이 둘이 맞물리면 SIGTERM → Spring 컨텍스트 close → JobOperator stop signal → 진행 중 청크 마감 → 메타 정합 기록 → JVM 종료의 흐름이 한 번에 도는 모양이 된다.

### 10.2.2 StoppableStep — 외부 stop 신호에 응답한다

6.0의 또 한 가지 정돈은 `StoppableStep` 인터페이스다. 이전엔 Tasklet 기반 Step만 `JobOperator#stop`에 응답할 수 있었다. 6에서는 chunk-oriented Step을 비롯한 어떤 종류의 Step이든 `StoppableStep`을 구현하면 외부 stop 신호를 받는다. graceful shutdown이 내부적으로 이걸 호출한다.

직접 구현할 일은 드물지만, 흐름을 한 번 보자.

```java
public class CleanupStep implements StoppableStep {

    private volatile boolean stopRequested = false;

    @Override
    public void stop() {
        this.stopRequested = true;
    }

    @Override
    public void execute(StepExecution stepExecution) {
        while (hasMoreWork() && !stopRequested) {
            doNextChunk();
        }
        if (stopRequested) {
            stepExecution.setStatus(BatchStatus.STOPPED);
        }
    }
}
```

핵심은 `stopRequested` 플래그가 매 청크 사이에 체크된다는 점이다. 청크 1개 안에서는 끊어내지 않는다 — 청크 = 트랜잭션이라는 핵심 규칙을 유지한다. 즉 **graceful shutdown은 청크의 끝에서만 중단한다.** 그래서 청크 길이가 grace period를 결정하는 1차 변수가 된다.

### 10.2.3 PreStop hook — 마지막 안전 장치

K8s에는 SIGTERM 직전에 실행되는 `preStop` lifecycle hook이 있다. 여기에 짧은 sleep을 넣어 트래픽 종료를 기다리게 만드는 패턴이 있는데, 배치 Pod에서는 다른 용도로 쓸 수 있다 — 외부에 "이제 종료한다"고 알리는 용도.

```yaml
spec:
  containers:
    - name: settlement
      lifecycle:
        preStop:
          exec:
            command: ["/bin/sh", "-c", "curl -X POST http://alerting/notify-shutdown && sleep 5"]
```

알림을 받는 운영자가 "이번 종료는 의도된 것"임을 미리 안다는 점에서, 알람 피로를 줄이는 작은 장치다. 큰 차이는 아니지만 운영 1년차에 누적되는 운영 디테일은 이런 작은 장치들의 묶음이다.

## 10.3 JobOperator#recover() — 박제된 STARTED를 자동으로 푼다

graceful shutdown이 모든 종료를 안전하게 만들면 좋겠지만, 현실은 그렇지 않다. SIGKILL은 항상 가능하다 — OOM Killer, 노드 강제 재부팅, kubelet 이슈, terminationGracePeriodSeconds 초과. 이런 비정상 종료의 결과는 늘 같다 — JobExecution이 STARTED로 박제되고, 다음 스케줄에서 "이미 실행 중"이라며 거부당한다.

5.x에서는 이걸 사람이 풀어야 했다. `BATCH_JOB_EXECUTION` 테이블을 SELECT로 들여다보고, 박제된 행의 status를 FAILED로 UPDATE하고, end_time을 채워넣고, 그 위에 다시 잡을 launch한다. 운영자가 새벽에 깨어나서 손으로 하던 일이다.

6.0의 `JobOperator#recover(executionId)` 한 줄이 이걸 표준화했다. 메서드 한 방으로 STARTED를 FAILED로 마킹하고, 메타 정합을 맞춘다. **K8s 운영 워크플로우의 가장 아픈 자리를 정확히 푼 변경**이다.

### 10.3.1 자동 recover 워크플로우

이 메서드를 어디에서 호출할 것인가가 운영 패턴을 결정한다. 두 가지 모양이 흔하다.

**모양 1 — 잡 시작 직전에 recover 호출.** 잡이 부팅하면서, 같은 이름의 잡이 STARTED 상태로 남아있는지 확인하고, 있으면 recover 후 본 잡을 launch한다.

```java
@Component
@RequiredArgsConstructor
public class StartupRecoveryRunner implements ApplicationRunner {

    private final JobOperator jobOperator;
    private final JobRepository jobRepository;

    @Value("${spring.batch.job.name}")
    private String jobName;

    @Override
    public void run(ApplicationArguments args) {
        Set<Long> running = jobOperator.getRunningExecutions(jobName);
        for (Long executionId : running) {
            JobExecution execution = jobRepository.getJobExecution(executionId);
            if (execution != null && isStale(execution)) {
                log.warn("Recovering stale execution: {}", executionId);
                jobOperator.recover(executionId);
            }
        }
    }

    private boolean isStale(JobExecution execution) {
        // 마지막 heartbeat 또는 lastUpdated가 N분 이상 지났는지 확인
        return execution.getLastUpdated() != null
            && execution.getLastUpdated().plusMinutes(10).isBefore(LocalDateTime.now());
    }
}
```

`isStale` 판단이 핵심이다. 단순히 STARTED라는 이유로 무조건 recover하면, 정말 다른 노드에서 도는 잡까지 죽인다. **"마지막 업데이트가 N분 이상 정지"** 같은 stale 판단을 함께 두는 편이 안전하다.

**모양 2 — K8s init container에서 recover 호출.** 잡 컨테이너가 뜨기 전에, init container가 recover 작업만 한 번 돌고 끝난다. 잡 컨테이너 코드를 깨끗하게 유지할 수 있다는 장점.

```yaml
spec:
  template:
    spec:
      initContainers:
        - name: recover
          image: registry.example.com/settlement-batch:1.4.2
          args:
            - "--spring.batch.job.name=settlementJob"
            - "--mode=recover-only"
      containers:
        - name: settlement
          # ...
```

어느 모양이든 핵심은 **사람이 손으로 안 들어가게** 만드는 것이다. recover는 빈 메서드 호출이 아니라 운영 워크플로우의 1단계로 박혀야 한다.

## 10.4 CommandLineJobOperator — K8s CronJob 진입점

5장에서 잠깐 이름만 언급했던 `CommandLineJobOperator`를 여기서 본격적으로 쓴다. 이전의 `CommandLineJobRunner`를 대체하는 모던 CLI 진입점이고, K8s CronJob의 `args:` 와 가장 잘 맞는 형태다.

### 10.4.1 CLI 옵션 모양

가장 단순한 사용법은 잡 이름과 파라미터를 args로 넘기는 것이다.

```bash
java -jar settlement-batch.jar \
  --spring.batch.job.name=settlementJob \
  --targetDate=2026-05-08 \
  --runId=20260508-0200
```

Spring Boot 4 + Spring Batch 6의 자동 구성이 이 args를 받아 `CommandLineJobOperator`에게 전달한다. 잡이 정의되어 있고, JobParameters 식별자가 잘 설계돼 있으면, 이 한 줄로 잡이 돈다.

start/stop/restart 표준 옵션도 들어왔다.

```bash
# 시작
java -jar batch.jar --spring.batch.operation=start --spring.batch.job.name=settlementJob

# 중지 (외부 신호)
java -jar batch.jar --spring.batch.operation=stop --spring.batch.execution.id=12345

# 재시작
java -jar batch.jar --spring.batch.operation=restart --spring.batch.execution.id=12345

# 복구
java -jar batch.jar --spring.batch.operation=recover --spring.batch.execution.id=12345
```

K8s CronJob에서는 `start`만 쓰는 게 보통이지만, 별도 Job 리소스를 띄워 `recover`나 `restart`만 도는 패턴도 가능하다. 운영 도구를 전부 같은 이미지로 묶을 수 있다는 게 장점이다.

### 10.4.2 Helm 차트로 추상화

같은 이미지로 여러 잡을 돌리려면 Helm 차트가 답이다. 차트 한 개에 잡 정의 N개를 values로 관리한다.

```yaml
# values.yaml
jobs:
  settlement:
    schedule: "0 2 * * *"
    jobName: settlementJob
    chunkSize: 500
    activeDeadlineSeconds: 7200
  reconciliation:
    schedule: "0 4 * * *"
    jobName: reconciliationJob
    chunkSize: 1000
    activeDeadlineSeconds: 3600

image:
  repository: registry.example.com/batch
  tag: 1.4.2
```

```yaml
# templates/cronjob.yaml
{{- range $name, $job := .Values.jobs }}
apiVersion: batch/v1
kind: CronJob
metadata:
  name: {{ $name }}-batch
spec:
  schedule: {{ $job.schedule | quote }}
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      backoffLimit: 0
      activeDeadlineSeconds: {{ $job.activeDeadlineSeconds }}
      template:
        spec:
          restartPolicy: Never
          terminationGracePeriodSeconds: 60
          containers:
            - name: batch
              image: "{{ $.Values.image.repository }}:{{ $.Values.image.tag }}"
              args:
                - "--spring.batch.operation=start"
                - "--spring.batch.job.name={{ $job.jobName }}"
                - "--chunkSize={{ $job.chunkSize }}"
---
{{- end }}
```

새 잡을 추가하려면 values.yaml에 항목 한 개만 추가하면 된다. 이 모양에서 한 발 더 나가면 12장 다음 학습 주제인 Spring Cloud Data Flow다.

## 10.5 JobRepository 정리 잡 — 정리 잡을 Spring Batch로 짜는 흥미로운 사례

잡을 운영하다 보면 메타데이터 테이블이 빠르게 자란다. `BATCH_JOB_INSTANCE`, `BATCH_JOB_EXECUTION`, `BATCH_STEP_EXECUTION`, `BATCH_JOB_EXECUTION_PARAMS`, `BATCH_JOB_EXECUTION_CONTEXT`, `BATCH_STEP_EXECUTION_CONTEXT`. 잡 1회 실행에 청크 1,000개가 돌면, 그 자체로는 행이 많지 않지만 매일 도는 잡 10개가 1년이면 수백만 행이 된다. 거기에 ExecutionContext의 byte 컬럼까지 합쳐지면 디스크 사용량도 빠르게 커진다.

이 자리에 정기 정리 잡이 필요하다. 보존 기간을 정하고(예: 90일), 그보다 오래된 메타를 삭제하는 잡. 흥미로운 건 — **이 정리 잡 자체를 Spring Batch로 짜면 자연스럽다.** 메타 → 메타를 다루는 자기 참조적인 케이스인데, 청크 단위 처리, 트랜잭션, ExecutionContext 같은 Spring Batch의 모든 장점이 그대로 살아난다.

### 10.5.1 정리 잡의 기본 구조

대상 메타 행을 찾아 청크 단위로 삭제한다. `JdbcCursorItemReader`로 보존 기간 초과 ID를 읽고, `JdbcBatchItemWriter`로 묶어 삭제한다. 외래 키 순서를 지키는 게 핵심이다.

```java
@Configuration
public class BatchMetaCleanupJobConfig {

    @Bean
    public Job batchMetaCleanupJob(JobRepository jobRepository,
                                    Step deleteStepExecutionContextStep,
                                    Step deleteStepExecutionStep,
                                    Step deleteJobExecutionContextStep,
                                    Step deleteJobExecutionParamsStep,
                                    Step deleteJobExecutionStep,
                                    Step deleteJobInstanceStep) {
        return new JobBuilder("batchMetaCleanupJob", jobRepository)
            .start(deleteStepExecutionContextStep)
            .next(deleteStepExecutionStep)
            .next(deleteJobExecutionContextStep)
            .next(deleteJobExecutionParamsStep)
            .next(deleteJobExecutionStep)
            .next(deleteJobInstanceStep)
            .build();
    }

    @Bean
    @StepScope
    public JdbcCursorItemReader<Long> staleJobExecutionIdReader(
            DataSource dataSource,
            @Value("#{jobParameters['retentionDays']}") Long retentionDays) {
        return new JdbcCursorItemReaderBuilder<Long>()
            .name("staleJobExecutionIdReader")
            .dataSource(dataSource)
            .sql("""
                SELECT JOB_EXECUTION_ID
                FROM BATCH_JOB_EXECUTION
                WHERE END_TIME < ?
                  AND STATUS IN ('COMPLETED', 'FAILED', 'STOPPED')
                ORDER BY JOB_EXECUTION_ID
                """)
            .preparedStatementSetter((ps) ->
                ps.setTimestamp(1, Timestamp.valueOf(
                    LocalDateTime.now().minusDays(retentionDays))))
            .rowMapper((rs, n) -> rs.getLong(1))
            .fetchSize(1000)
            .build();
    }

    @Bean
    @StepScope
    public JdbcBatchItemWriter<Long> jobExecutionDeleteWriter(DataSource dataSource) {
        return new JdbcBatchItemWriterBuilder<Long>()
            .dataSource(dataSource)
            .sql("DELETE FROM BATCH_JOB_EXECUTION WHERE JOB_EXECUTION_ID = ?")
            .itemPreparedStatementSetter((id, ps) -> ps.setLong(1, id))
            .build();
    }

    @Bean
    public Step deleteJobExecutionStep(JobRepository jobRepository,
                                        PlatformTransactionManager txm,
                                        JdbcCursorItemReader<Long> staleJobExecutionIdReader,
                                        JdbcBatchItemWriter<Long> jobExecutionDeleteWriter) {
        return new StepBuilder("deleteJobExecutionStep", jobRepository)
            .<Long, Long>chunk(500, txm)
            .reader(staleJobExecutionIdReader)
            .writer(jobExecutionDeleteWriter)
            .build();
    }

    // 다른 Step (StepExecutionContext, StepExecution, JobExecutionContext, ...)도 동일 패턴
}
```

### 10.5.2 외래 키 순서가 결정적이다

핵심은 삭제 순서다. Spring Batch 메타 스키마의 외래 키 관계는 다음 모양이다.

```
BATCH_JOB_INSTANCE
  └─ BATCH_JOB_EXECUTION
       ├─ BATCH_JOB_EXECUTION_PARAMS
       ├─ BATCH_JOB_EXECUTION_CONTEXT
       └─ BATCH_STEP_EXECUTION
            └─ BATCH_STEP_EXECUTION_CONTEXT
```

자식부터 지운다. 순서가 다음과 같아야 한다.

1. `BATCH_STEP_EXECUTION_CONTEXT`
2. `BATCH_STEP_EXECUTION`
3. `BATCH_JOB_EXECUTION_CONTEXT`
4. `BATCH_JOB_EXECUTION_PARAMS`
5. `BATCH_JOB_EXECUTION`
6. `BATCH_JOB_INSTANCE` (자식 JobExecution이 모두 사라진 후)

부모를 먼저 지우면 외래 키 위반으로 트랜잭션이 롤백된다. 6 스텝짜리 잡이 깔끔하게 떨어지는 자리다.

### 10.5.3 트랜잭션 길이를 짧게 — chunk size를 작게

여기서 흔한 함정 한 가지. DELETE를 한 트랜잭션에 1만 건 묶어 처리하면 트랜잭션 길이가 길어지고, 그 사이에 들어오는 다른 잡(또는 운영 작업)과 lock 경합이 일어난다. **chunk size를 작게 (200~500) 잡고 트랜잭션 길이를 짧게 유지하는 편이 운영에 안전하다.**

이 정리 잡은 일주일에 한 번, 또는 매일 새벽 비번 시간대에 도는 게 보통이다. CronJob 한 개를 추가로 띄워두자.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: batch-meta-cleanup
spec:
  schedule: "0 5 * * 0"  # 매주 일요일 새벽 5시
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Never
          containers:
            - name: cleanup
              image: registry.example.com/batch:1.4.2
              args:
                - "--spring.batch.job.name=batchMetaCleanupJob"
                - "--retentionDays=90"
```

90일이라는 보존 기간은 출발점이다. 운영하면서 "그래도 한 달은 보고 싶다", "180일은 봐야 분기 분석이 가능하다" 같은 요구가 생기면 그에 맞춰 조정하자. 다만 보존 기간이 너무 길면 메타 테이블이 다시 무거워지니, 90~180일이 흔한 운영 범위다.

## 10.6 K8s 환경에서만 의미 있는 모니터링 결정

9장이 일반 모니터링을 다뤘다면, 10장에서 짚어야 할 K8s 특화 결정이 몇 개 더 있다. Pod이라는 단위, K8s Event라는 별도 신호 채널, 컨테이너와 JVM의 OOM 구분 — 이 셋이 K8s 환경에서만 의미 있는 항목들이다.

### 10.6.1 컨테이너 OOMKilled vs JVM OOM — 구분이 진단을 가른다

배치 잡이 메모리 문제로 죽었다는 신호가 들어왔다고 해보자. 두 가지 가능성이 있다.

**가능성 1 — 컨테이너 OOMKilled.** Pod 메모리 limit을 컨테이너 전체가 초과한 것. K8s의 cgroup이 컨테이너를 SIGKILL로 죽인다. JVM 입장에서는 갑자기 죽은 거라 스택트레이스가 안 남는다. K8s Event에 `Reason: OOMKilled`가 찍힌다.

**가능성 2 — JVM OOM.** JVM heap이 max heap을 초과한 것. `OutOfMemoryError`가 throw되고 스택트레이스가 로그에 남는다. JVM이 자체 종료하니 K8s Event에는 OOMKilled가 안 찍힌다.

진단 경로가 완전히 다르다. 컨테이너 OOMKilled면 Pod 메모리 limit을 키우거나, native heap 사용처(Direct ByteBuffer, JNI 등)를 의심한다. JVM OOM이면 heap dump를 받아 누가 메모리를 잡고 있는지 본다.

K8s 환경의 모니터링은 이 둘을 구분해서 알람을 띄워야 한다.

```promql
# 컨테이너 OOMKilled (kube-state-metrics 메트릭)
kube_pod_container_status_last_terminated_reason{reason="OOMKilled",namespace="batch"} > 0
```

JVM OOM은 별도로 잡는다. heap dump on OOM을 자동화해 두면, 사후 분석 자료가 쌓인다.

```yaml
spec:
  containers:
    - name: settlement
      args:
        - "-XX:+HeapDumpOnOutOfMemoryError"
        - "-XX:HeapDumpPath=/var/heap-dumps"
      volumeMounts:
        - name: heap-dump-volume
          mountPath: /var/heap-dumps
  volumes:
    - name: heap-dump-volume
      persistentVolumeClaim:
        claimName: heap-dump-pvc
```

heap dump 파일이 PVC로 떨어지니, Pod이 종료된 뒤에도 분석 가능하다. 디스크 비용은 들지만, OOM 한 번 잡았을 때의 가치는 그 비용을 초과한다.

### 10.6.2 K8s Event과 JobExecution 상태 매칭

JobExecution은 메타 테이블에 있고, Pod의 운명은 K8s Event에 있다. 둘이 매칭되지 않으면 진단이 어긋난다. 예를 들어 JobExecution이 STARTED인 채 메타에 박제됐는데, K8s Event에는 Pod이 OOMKilled로 종료됐다고 찍혀 있다 — 그 시점이 정확히 일치하면, "OOMKilled로 죽어서 박제된" 정황 인과가 분명해진다.

이걸 자동화하는 표준 답은 없지만, 운영 표준으로 권할 수 있는 패턴은 다음이다.

- 알람 메시지에 **JobExecution ID와 Pod 이름을 함께 적는다**
- Loki/ELK 같은 로그 백엔드에 **JobExecution ID 라벨을 자동 부착한다**
- Grafana에 **"JobExecution별 Pod 이력"** 패널을 둔다

특별히 화려한 도구가 필요한 건 아니다. JobExecutionListener에서 시작/종료 시점에 Pod 이름을 ExecutionContext에 적어두기만 해도 절반은 된다.

```java
@Component
public class PodAwareListener implements JobExecutionListener {

    private final String podName = System.getenv("HOSTNAME");

    @Override
    public void beforeJob(JobExecution jobExecution) {
        jobExecution.getExecutionContext().putString("podName", podName);
    }
}
```

`HOSTNAME`은 K8s가 컨테이너에 자동으로 주입하는 환경변수로, Pod 이름과 같다. 이 한 줄이 박제 사고 진단의 결정적 단서가 되는 자리가 종종 있다.

### 10.6.3 Pod 재기동 시 recover 자동 트리거

10.3에서 본 recover 워크플로우를 K8s에 자연스럽게 끼워넣는 방식이 init container다. 잡 컨테이너 직전에 recover 전용 컨테이너 한 개가 돌고 끝나도록.

```yaml
spec:
  template:
    spec:
      initContainers:
        - name: recover-stale
          image: registry.example.com/batch:1.4.2
          args:
            - "--spring.batch.operation=recover"
            - "--spring.batch.job.name=settlementJob"
            - "--mode=stale-only"
      containers:
        - name: settlement
          # ...
```

이 init container는 STARTED인 기존 execution을 찾아 stale 판단 후 recover한다. 본 잡 컨테이너는 깨끗한 상태에서 시작한다. **운영자의 수동 개입이 사라지는 자리**다.

## 10.7 실 운영 체크리스트

이 장에서 다룬 것을 한 번에 모아보자. K8s에서 Spring Batch 6을 production-ready로 돌리는 데 갖춰야 할 항목 9가지다.

1. **CronJob `concurrencyPolicy: Forbid`, `backoffLimit: 0`, `restartPolicy: Never`** — K8s와 Spring Batch의 의미 충돌 차단
2. **`terminationGracePeriodSeconds`를 청크 길이에 맞춤** — graceful shutdown이 청크 마감을 기다릴 시간
3. **Spring Boot graceful shutdown 옵션 활성화** — `server.shutdown: graceful`
4. **`JobOperator#recover()` 자동 호출 워크플로우** — init container 또는 startup runner
5. **CommandLineJobOperator + Helm 차트** — 새 잡 추가가 values.yaml 한 줄
6. **JobRepository 정리 잡 등록** — 보존 기간 90~180일, chunk size 200~500
7. **Heap dump on OOM, PVC 마운트** — JVM OOM 사후 분석 가능하게
8. **Pod 이름을 JobExecution 메타에 기록** — K8s Event과 메타 매칭
9. **컨테이너 OOMKilled vs JVM OOM 분리 알람** — 진단 경로가 다르다

이 9가지가 다 갖춰지면 — **운영자가 새벽에 호출되는 빈도가 한 자릿수에서 한 자릿수의 한 자릿수로 떨어진다.** 정확한 수치는 잡의 성격에 따라 다르지만, 이 차이는 1년쯤 운영해보면 신체적으로 안다. 박제된 메타를 손으로 푸는 일이 사라지고, recover가 자동으로 도는 모양을 처음 봤을 때의 안도감 — 그게 production-ready의 실감이다.

## 마무리

K8s 운영을 정리하면서 한 가지 분명해진 것이 있다. **6의 graceful shutdown과 recover() 한 쌍은 5에서 6으로 넘어갈 가장 강한 동기 한 가지를 제공한다.** 5에서 K8s 운영을 해본 사람이라면, 이 두 가지가 표준화된 것의 의미를 안다. 사람이 새벽에 깨어나서 DB를 손봐야 했던 패턴이, 시스템이 스스로 일어나는 패턴으로 대체된다.

그러면 자연스러운 다음 질문이 생긴다 — **5에서 6으로 어떻게 옮기는가?** 진행 중인 잡이 있고, 5의 직렬화 포맷으로 메타가 쌓여 있고, 패키지 import는 거의 다 빨갛다. 다음 장은 정확히 이 마이그레이션을 다룬다. 잡 한 개를 골라 코드 diff 4~5단계로 풀어보고, 메타 정합성을 SQL로 검증하고, 단계 실패 시의 롤백 시나리오까지 한 호흡에 본다.
