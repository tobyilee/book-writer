# 8장. 성능과 확장 — 파티셔닝, 멀티스레드, Remote Step

잡이 느려서 멀티스레드를 켰다. 그런데 결과가 이상해졌다. 어떤 항목은 두 번 처리되고, 어떤 항목은 누락됐다. 멀티스레드로 4배가 빨라지긴 했는데 — 데이터가 신뢰할 수 없게 됐다. 이게 정말 정답일까? 어디서부터 잘못된 걸까?

또 다른 시나리오. 잡이 1시간에서 2시간으로 늘었다. 데이터가 늘어서인지, 어딘가가 느려져서인지 — 어디서부터 손을 대야 할지 모르겠다. 멀티스레드를 켜야 하나? partitioning을 해야 하나? Remote Chunking인가? 이름은 들어봤는데 무엇을 언제 써야 하는지가 안 보인다.

잡이 느릴 때의 결정 트리를 한 번 만들어보자. 무엇부터 측정하고, 어떤 옵션을 어느 순서로 시도할지. 6장의 카카오페이 사례가 끝낸 4단계 — Processor I/O 묶기, Writer 변경, IN 절 그룹화, chunk·page·fetch 정렬 — 그 다음에 꺼낼 카드들이다. 카카오페이의 결론을 다시 한번 환기하자: "처음부터 병렬 처리보다 현재 구조에서 I/O를 묶는 것이 효율적이다." 여기에 등장하는 카드는 그 말 다음에 꺼내야 할 카드다.

## 튜닝의 첫 단계 — chunk size · page size · fetch size 정렬

병렬화에 들어가기 전에, 단일 스레드 안에서의 정렬부터 다시 짚자. 6장에서 한 번 언급했지만, 여기서는 **측정**과 **결정 트리**까지 본격적으로 풀어낸다.

세 개념을 한 번 더.

- **chunk size** — 트랜잭션 1건당 처리할 항목 수.
- **page size** — Paging Reader가 한 페이지에 가져올 행 수.
- **fetch size** — JDBC 드라이버가 한 라운드트립에 가져올 행 수.

권장 시작값.

```yaml
# 측정 전 시작값
chunk size = page size = 1,000
fetch size = chunk size 이상 (1,000 또는 2,000)
```

시작값은 1,000 근처가 안전한 베이스라인이다. 너무 작으면 트랜잭션 커밋 빈도가 높아 처리량이 떨어진다. 너무 크면 트랜잭션 길이가 길어져 락 점유와 실패 비용이 커진다. 1,000은 그 중간의 안전한 자리다.

그 다음 — **production 데이터로 측정한다.** 측정 없는 튜닝은 거의 항상 잘못된 값에 도달한다.

### 청크 사이즈를 키우는 것이 항상 좋은가

자연스러운 직관은 "청크가 클수록 처리량이 좋다"이다. 한 트랜잭션에 더 많은 항목을 묶으면 트랜잭션 시작·종료 오버헤드가 분산되니까. 그런데 이건 어느 지점까지만 맞다.

청크 사이즈를 키울 때의 트레이드오프 셋이다.

**하나, 트랜잭션 길이.** 청크가 5,000건이면 트랜잭션이 5,000건을 처리하는 동안 열려 있다. 그 시간만큼 DB 락을 잡고, 트랜잭션 로그가 쌓이고, 다른 세션의 read를 방해한다. RDB의 동시성 측면에서 트랜잭션이 길어지는 건 거의 항상 비용이다.

**둘, 메모리 점유.** 청크 안의 항목들은 트랜잭션 커밋 전까지 메모리에 들고 있어야 한다. 청크 사이즈 5,000과 항목 평균 1KB라면 청크당 5MB. 한 잡에 동시에 몇 개의 청크가 메모리에 있을 수 있는지 고려하면, 청크가 너무 크면 OOM 위험이 커진다.

**셋, 실패 비용.** 청크가 5,000건일 때 마지막 1건에서 실패하면 4,999건이 통째로 롤백된다. 5,000건을 다시 처리해야 한다. 청크가 100건이라면 99건만 다시 처리하면 된다. **청크 사이즈 = 실패 시 재처리 단위**다.

이 셋의 균형점이 자기 잡의 최적 청크 사이즈다. 그 균형점은 도메인마다 다르다 — 항목이 작고 처리가 단순하면 청크를 크게, 항목이 크고 처리가 복잡하거나 외부 시스템 의존이 있으면 청크를 작게.

### 측정 — 무엇을 어떻게 보는가

production 데이터로 측정할 때 무엇을 보아야 할까.

**처리량 (items per second).** 가장 직관적인 지표. 청크 사이즈를 100, 500, 1000, 2000, 5000으로 바꿔가며 같은 데이터를 처리해 처리량을 비교한다. 보통 어느 지점까지는 처리량이 오르다가, 그 너머에서는 평평해지거나 도리어 떨어진다. 평평해지는 직전이 권장 값이다.

**P95 청크 처리 시간.** 청크 하나를 처리하는 데 걸리는 시간의 95백분위. 평균이 아니라 95백분위인 이유는 — 평균은 outlier를 가린다. 일부 청크가 매우 오래 걸린다면(예: 외부 API 타임아웃) 평균은 멀쩡해도 운영에선 문제가 된다. P95가 안정적이어야 production-ready.

**메모리 사용량.** JVM의 heap 사용 그래프. 청크 사이즈를 키울수록 heap 사용량이 어떻게 변하는지 본다. -Xmx의 70%를 안정적으로 넘기지 않는 청크 사이즈가 안전 한도다.

측정의 표준 도구는 9장에서 다룰 Micrometer + Prometheus + Grafana다. 여기서는 "측정 후에 결정한다"는 원칙만 강조해두자.

## JDBC Batch와 Connection Timeout 회피

청크 사이즈가 정렬됐다고 해서 자동으로 JDBC batch가 켜지는 건 아니다. 한 가지 더 점검할 곳이 있다.

`JdbcBatchItemWriter`는 청크 안의 항목들을 JDBC batch로 묶어 한 번에 전송한다. 그러나 청크 사이즈가 매우 클 때 — 예를 들어 5,000건 — DB로의 한 번의 batch 전송이 connection timeout에 걸릴 수 있다. 특히 클라우드 환경에서 connection idle timeout이 30초~60초로 설정된 경우.

해결은 batch 크기를 분할하는 것이다.

```java
public class ChunkedJdbcWriter implements ItemWriter<EnrichedTransaction> {
    private final NamedParameterJdbcTemplate jdbc;
    private static final int BATCH_PARTITION = 1000;  // batch 1회당 최대 항목

    @Override
    public void write(Chunk<? extends EnrichedTransaction> chunk) {
        List<? extends EnrichedTransaction> items = chunk.getItems();
        for (int i = 0; i < items.size(); i += BATCH_PARTITION) {
            List<? extends EnrichedTransaction> partition =
                items.subList(i, Math.min(i + BATCH_PARTITION, items.size()));
            jdbc.batchUpdate(SQL, toParams(partition));
        }
    }
}
```

청크 사이즈가 5,000이라도 JDBC batch는 1,000 단위로 5번 나눠 보낸다. 한 번의 batch 전송이 30초를 넘지 않게 보장한다. 카카오페이 사례에서도 이 패턴이 등장한다 — 1,000건 단위로 분할해 connection timeout을 회피.

## 멀티스레드 Step — 가장 단순한 병렬화

여기서부터 병렬화 카드들을 본다. 첫 번째 카드는 멀티스레드 step이다.

기본 아이디어는 단순하다 — **하나의 step을 여러 스레드가 동시에 처리한다.** Spring Batch가 taskExecutor를 받아 chunk 처리를 N개 스레드에 분배한다.

```java
@Bean
public TaskExecutor batchTaskExecutor() {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(4);
    executor.setMaxPoolSize(4);
    executor.setQueueCapacity(0);  // unbounded queue 회피
    executor.setThreadNamePrefix("batch-");
    executor.initialize();
    return executor;
}

@Bean
public Step multithreadedStep(JobRepository jobRepository,
                               ItemReader<RawTransaction> reader,
                               ItemWriter<RawTransaction> writer,
                               TaskExecutor batchTaskExecutor) {
    return new ChunkOrientedStepBuilder<RawTransaction, RawTransaction>(
            "multithreadedStep", jobRepository, 1000)
        .reader(reader)
        .writer(writer)
        .taskExecutor(batchTaskExecutor)
        .build();
}
```

5장에서 본 것처럼 6.0의 멀티스레드 step은 **producer-consumer + bounded queue** 모델이다. producer 한 명이 reader에서 읽어 큐에 푸시하고, consumer N명이 큐에서 꺼내 process → write 한다. 큐가 bounded라서 메모리 폭주를 자체 차단한다.

### 멀티스레드 step의 함정

코드는 간단해 보이는데 함정이 한 둘이 아니다. 가장 중요한 셋만 짚자.

**함정 1 — Stateful Reader는 Thread-Safe 해야 한다.**

`JdbcCursorItemReader`처럼 cursor 상태를 들고 있는 Reader는 thread-safe하지 않다. 멀티스레드에서 같은 cursor를 여러 스레드가 동시에 호출하면 데이터가 중복되거나 누락된다. 직접 thread-safe하게 짠다고 해도 락 경합으로 처리량이 도리어 떨어질 수 있다.

`JdbcPagingItemReader`는 페이지 단위로 새 쿼리를 던져 stateless에 가깝지만 — 그래도 멀티스레드 환경에서 페이지 사이의 데이터가 일관되지 않을 수 있다(다른 스레드가 같은 페이지를 다시 읽거나, 페이지 사이의 데이터가 바뀐 경우).

6.0의 producer-consumer 모델은 **producer가 한 명**이라 reader를 단일 스레드가 호출한다 — 이전 모델보다 안전해졌다. 그러나 reader 자체가 stateful이라면 여전히 주의가 필요하다.

**함정 2 — Restartability가 약화된다.**

멀티스레드 step에서 N개 스레드가 청크를 동시에 처리한다. 잡이 도중에 실패하면 — 어떤 청크가 커밋됐고 어떤 청크가 실패했는지의 순서가 단순하지 않다. ExecutionContext에 저장되는 reader의 위치가 어느 스레드 기준인지가 모호해진다.

restart했을 때 마지막 커밋 다음부터 다시 시작하는 의미가 멀티스레드에서는 깔끔하게 정의되지 않는다. 이게 멀티스레드 step의 가장 큰 단점이다 — **restartability가 약화된다.**

데이터를 다시 처리해도 안전한 잡(완전 멱등 Writer + dedupe)이라면 멀티스레드도 무방하다. 그러나 restart 시 정확히 빠진 자리부터 다시 처리되어야 하는 잡이라면 — 멀티스레드 대신 partitioning을 본다.

**함정 3 — 트랜잭션 격리 이슈.**

여러 스레드가 동시에 같은 테이블을 UPDATE하면 deadlock 위험이 생긴다. 인덱스 락 순서가 스레드마다 다르게 잡혀 데드락이 자주 보고된다. 처리하는 데이터가 충분히 분리되어 있어야 안전하다.

### 멀티스레드 step을 언제 쓰는가

위 함정을 감안하면, 멀티스레드 step이 잘 맞는 자리는 좁다.

- **Read는 단순한 페이징, Process가 무겁고 CPU bound, Write는 멱등.** 이 조합이면 멀티스레드의 효과가 크다.
- **잡이 일회성이거나 재시작이 의미 없는 잡.** restartability 약화가 문제 안 됨.
- **데이터가 자연스럽게 분리되어 deadlock 위험이 없는 잡.**

이 조건을 만족하지 못하면 — 다음 카드, partitioning을 본다.

## Partitioning — 실무에서 가장 많이 쓰는 수평 확장

partitioning은 다른 모델이다. **입력을 N등분한 다음, 각 등분을 독립된 step instance가 처리한다.** 멀티스레드 step이 한 step을 N개 스레드가 공유한다면, partitioning은 N개의 독립된 step이 각자 자기 데이터만 본다.

이 차이가 뭘 의미할까? 각 step은 자기만의 reader/writer/ExecutionContext를 가진다. 즉 — **각 step은 독립적으로 restartable하다.** 데이터가 분리되어 있으니 deadlock 위험도 작다. stateful reader 문제도 사라진다(각 reader가 자기 데이터만).

partitioning의 구조는 master + worker다.

- **Master step:** 입력을 N등분한다(`Partitioner` 인터페이스).
- **Worker step:** 각 partition을 독립적으로 처리.
- **PartitionHandler:** master가 worker step을 어떻게 호출할지(로컬 스레드 또는 원격 노드).

코드로 보자.

```java
@Configuration
public class PartitionedSettlementJobConfig {

    @Bean
    public Partitioner settlementPartitioner(DataSource dataSource) {
        return new Partitioner() {
            @Override
            public Map<String, ExecutionContext> partition(int gridSize) {
                // ID 범위를 gridSize 등분
                long minId = jdbc.queryForObject("SELECT MIN(id) FROM raw_transaction", Long.class);
                long maxId = jdbc.queryForObject("SELECT MAX(id) FROM raw_transaction", Long.class);
                long range = (maxId - minId + 1) / gridSize;

                Map<String, ExecutionContext> partitions = new HashMap<>();
                for (int i = 0; i < gridSize; i++) {
                    ExecutionContext ctx = new ExecutionContext();
                    ctx.putLong("minId", minId + i * range);
                    ctx.putLong("maxId", (i == gridSize - 1) ? maxId : minId + (i + 1) * range - 1);
                    partitions.put("partition-" + i, ctx);
                }
                return partitions;
            }
        };
    }

    @Bean
    @StepScope
    public JdbcPagingItemReader<RawTransaction> partitionedReader(
            DataSource dataSource,
            @Value("#{stepExecutionContext['minId']}") Long minId,
            @Value("#{stepExecutionContext['maxId']}") Long maxId) {
        return new JdbcPagingItemReaderBuilder<RawTransaction>()
            .name("partitionedReader")
            .dataSource(dataSource)
            .pageSize(1000)
            .fetchSize(1000)
            .selectClause("SELECT *")
            .fromClause("FROM raw_transaction")
            .whereClause("WHERE id BETWEEN :minId AND :maxId")
            .parameterValues(Map.of("minId", minId, "maxId", maxId))
            .sortKeys(Map.of("id", Order.ASCENDING))
            .rowMapper(new RawTransactionRowMapper())
            .build();
    }

    @Bean
    public Step workerStep(JobRepository jobRepository,
                            JdbcPagingItemReader<RawTransaction> partitionedReader,
                            ItemWriter<RawTransaction> writer) {
        return new ChunkOrientedStepBuilder<RawTransaction, RawTransaction>(
                "workerStep", jobRepository, 1000)
            .reader(partitionedReader)
            .writer(writer)
            .build();
    }

    @Bean
    public Step partitionedMasterStep(JobRepository jobRepository,
                                       Partitioner settlementPartitioner,
                                       Step workerStep,
                                       TaskExecutor batchTaskExecutor) {
        return new PartitionStepBuilder("partitionedMasterStep", jobRepository)
            .partitioner("workerStep", settlementPartitioner)
            .step(workerStep)
            .gridSize(4)
            .taskExecutor(batchTaskExecutor)
            .build();
    }
}
```

핵심 포인트.

**Partitioner가 데이터를 등분한다.** 위 코드에서는 ID 범위를 gridSize(4)로 나눠 각 partition에 minId/maxId를 ExecutionContext로 넘긴다. 등분 기준은 도메인마다 다르다 — ID 범위, 날짜, 가맹점 ID 등.

**`@StepScope` Reader가 partition별 파라미터를 주입받는다.** 여기서 3장에서 본 `@StepScope` 패턴이 진가를 발휘한다. 각 worker step instance마다 별도 Reader 빈이 생성되고, 자기 partition의 minId/maxId를 받는다.

**gridSize는 partition 수.** 보통 CPU 코어 수의 1~2배. 4코어 환경이면 4~8.

**TaskExecutor가 worker를 어떻게 실행할지 결정.** 위 코드는 `TaskExecutorPartitionHandler`가 같은 JVM 내 스레드 풀에서 worker를 실행한다(로컬 partitioning).

### Partitioning의 장점

**Restartability 유지.** 각 worker step은 독립적인 ExecutionContext를 가진다. 일부 worker가 실패해도 그 worker의 위치만 기록된다. restart 시 실패한 worker만 그 위치부터 다시 시작한다 — 정확히, 깔끔하게.

**데이터 분리로 lock 경합 회피.** ID 범위로 등분하면 각 worker가 다른 행을 처리한다. UPDATE도 다른 행이라 lock 경합이 거의 없다.

**확장성.** 데이터가 두 배가 되면 gridSize를 두 배로 늘린다. 또는 노드를 추가해 원격 partitioning으로.

이런 이유로 **실무에서 가장 많이 쓰이는 수평 확장 옵션**이다.

### 로컬 vs 원격 Partitioning

`PartitionHandler`를 갈아끼우면 같은 partitioner 코드로 로컬 또는 원격 실행이 가능하다.

- **로컬 Partitioning** (`TaskExecutorPartitionHandler`): 같은 JVM 내 스레드 풀.
- **원격 Partitioning**: Spring Integration 메시지 채널로 다른 노드의 worker를 호출.

원격 partitioning은 master가 message를 보내고 worker 노드가 수신해 step을 실행한다. 큰 데이터를 여러 노드로 분산하고 싶을 때. 다만 메시지 큐 인프라(RabbitMQ, Kafka 등)가 필요하고, 운영 복잡도가 한 단계 올라간다.

**먼저 로컬 partitioning부터.** 단일 JVM의 CPU·메모리·DB 연결 한도를 모두 쓴 다음에야 원격 partitioning을 검토하자. 대부분의 한국 운영 환경은 로컬 partitioning만으로 충분하다.

### Grid Size 결정

gridSize를 얼마로 잡을지가 흔한 질문이다. 가이드라인.

- **CPU bound 잡**: CPU 코어 수와 같거나 약간 더(코어의 1배~1.5배).
- **I/O bound 잡 (DB·외부 API)**: CPU 코어 수의 2배 또는 더. CPU가 대기 중일 때 다른 worker가 일하므로.
- **DB 연결 한도**: gridSize × chunk 처리에 필요한 connection ≤ 풀 크기. 풀이 작으면 worker가 connection을 못 받아 대기.

측정 후 조정한다. 너무 작으면 처리량 미달, 너무 크면 컨텍스트 스위칭 비용이 처리량을 깎는다.

## Remote Chunking — Process가 매우 무거운 자리

다음 카드 — Remote Chunking. 이건 어디에 쓸까?

상황을 그려보자. 잡의 reader는 빠르다(DB에서 페이징으로 읽어옴). writer도 빠르다(JDBC batch). 그런데 **processor가 매우 무겁다** — 머신러닝 추론이라거나, 외부 시스템에 복잡한 호출을 하거나, CPU intensive한 변환이라거나. 단일 노드의 CPU가 100%가 되는데 처리량이 안 나온다.

partitioning이라면 — 데이터를 등분해 N개 노드에 나눈다. 그런데 reader도 N개 노드에서 각자 동작하므로, DB가 N개의 동시 read 요청을 받는다. DB가 병목이 될 수 있다.

Remote Chunking은 이 자리에 맞다. **Reader/Process는 master에서, Writer만 워커로 분산.**

```
[master 노드]
   reader → process(가벼운 사전 처리) → 메시지 큐로 청크 전송
                                              ↓
[worker 노드 N개]
   메시지 큐에서 청크 수신 → process(무거운 핵심 처리) → write
```

(메시징 인프라가 필요하다는 점이 partitioning과 같다.)

이게 의미가 있는 자리는 매우 좁다 — process 비용이 read 비용보다 훨씬 큰 경우. 일반적인 ETL이나 정산 잡에서는 process가 그리 무겁지 않다. 머신러닝 추론을 청크별로 돌리는 잡 같은 매우 특수한 자리에서 이 카드를 본다.

대부분의 운영 환경에서는 **partitioning이 충분하다.** Remote Chunking은 partitioning으로 안 풀리는 명확한 이유가 있을 때만 검토하자.

## Remote Step — 6.0의 새 카드

5장에서 신호로 적은 그 카드. 6.0에서 새로 들어왔다. **Step 자체를 다른 노드에서 통째로 실행한다.**

Partitioning이 한 step을 N개의 worker step instance로 나눈다면, Remote Step은 step 자체를 분산한다. 한 잡 안에 step A, step B, step C가 있고 — step A는 GPU 노드에서, step B는 메모리 큰 노드에서, step C는 일반 노드에서 돌리고 싶을 때.

이건 **잡 안의 step별로 자원 특성이 매우 다른 경우**의 카드다. 일반 ETL 잡에는 거의 등장하지 않는다. 다만 6.0의 분산 실행 옵션 카탈로그에 새 항목이 들어왔다는 점은 알아두자. 한국 production 후기는 아직 누적 중이다.

## SEDA via Spring Integration

마지막으로 SEDA(Staged Event-Driven Architecture). Spring Integration의 메시지 채널을 활용해 step 간 비동기 분리를 하는 패턴이다.

```
[step A: ingest] → 메시지 채널 → [step B: process] → 메시지 채널 → [step C: write]
```

각 step이 메시지 채널로 분리되어 있으므로, 한 step의 처리량이 다른 step에 직접 영향을 주지 않는다. step A가 빨라지거나 느려져도 step B는 자기 페이스로 처리한다. 채널 큐가 backpressure 역할을 한다.

이게 잘 맞는 자리는 — step별 처리 속도가 매우 다르고, 큐로 흘러가는 모델이 자연스러운 도메인. ETL의 ingest/transform/load가 명확히 분리되는 잡 같은 자리.

운영 복잡도가 한 단계 올라간다. 메시지 채널 인프라, persistent queue, 실패 처리, 재처리 — 모두 추가 고려사항이 된다. SEDA는 잡이 아니라 "잡들 사이의 오케스트레이션"에 가까운 패턴이라, Airflow 같은 도구가 더 자연스러운 자리이기도 하다. Spring Batch 안에서 SEDA를 짜기 전에, "이게 정말 한 잡 안에서 풀어야 할 문제인가?"부터 점검하자.

## 결정 트리 — 무엇부터 시도할까

여기까지 다섯 카드를 봤다. 정리하면 — 멀티스레드 step, partitioning, Remote Chunking, Remote Step, SEDA. 어떤 카드를 언제 꺼낼지 결정 트리를 그리자.

```
[잡이 느리다]
    ↓
[1단계] 측정 — 어디가 병목인가?
    - reader, processor, writer 중 어디가 시간을 잡아먹는가?
    - DB·외부 API·CPU·메모리 중 어느 자원이 한계에 가까운가?
    ↓
[2단계] 단일 스레드 구조 점검 (6장 4단계)
    - Processor의 외부 호출을 Writer로 묶었는가?
    - JdbcBatchItemWriter를 쓰고 있는가?
    - 동일 값 UPDATE를 IN 절로 묶을 수 있는가?
    - chunk·page·fetch size가 정렬되어 있는가?
    ↓ (여기까지 했는데도 느리면)
[3단계] 병렬화 카드 선택
    ↓
    데이터를 ID 범위·날짜·가맹점 등으로 깔끔히 분할 가능한가?
        ├─ 예 → Partitioning (실무 1순위)
        │       └─ 단일 JVM이면 로컬, 분산이 필요하면 원격
        │
        └─ 아니오 → Process가 매우 무거운가?
                    ├─ 예 → Remote Chunking 검토
                    │       (메시징 인프라 필요)
                    │
                    └─ 아니오 → 멀티스레드 step
                              (restartability 약화 감수)
    ↓
[4단계] Step 단위로 자원 특성이 매우 다른가?
    └─ 예 → Remote Step (6.0 신규)

[5단계] Step 간 비동기 분리가 자연스러운 도메인인가?
    └─ 예 → SEDA via Spring Integration
            (운영 복잡도 한 단계 추가)
```

이 결정 트리의 핵심 메시지는 두 가지다.

**하나, 측정이 모든 결정의 출발이다.** 어디가 병목인지 모르고 카드를 꺼내면 잘못된 카드를 꺼낸다. processor가 빠른데 멀티스레드를 켜는 건 의미가 없다. DB가 병목인데 partitioning을 키우면 DB가 더 빨리 무너진다.

**둘, 6장 4단계가 끝난 다음의 카드다.** 단일 스레드의 비효율을 안고 병렬화하면 그 비효율이 N배로 증폭된다. 구조 점검 → 병렬화 순서를 지키자.

## Partitioning이 1순위인 이유

위 결정 트리에서 partitioning을 실무 1순위로 적었다. 왜 그런지 정리해두자.

| 항목 | 멀티스레드 Step | Partitioning |
|------|----------------|--------------|
| 구현 난도 | 매우 낮음 (taskExecutor 한 줄) | 중간 (Partitioner 작성 필요) |
| Restartability | 약화됨 | 유지 |
| Stateful Reader 안전성 | 위험 | 안전 (partition별 reader) |
| Lock 경합 | 데이터에 따라 위험 | 데이터 분리로 회피 |
| 확장 가능성 | 단일 JVM | 로컬 + 원격 모두 |

partitioning은 구현이 약간 더 손이 가지만, 운영 안전성이 한 단계 위다. 한 번 짜두면 데이터가 두 배로 자라도 gridSize만 늘리면 된다. 그래서 한국 production 환경에서 가장 많이 쓰이는 카드다. 멀티스레드 step은 "임시방편" 또는 "특수 자리"에 가깝고, partitioning이 표준이다.

## 한국 커뮤니티에서 자주 보는 함정

이 장을 마무리하기 전에, 한국 커뮤니티에서 반복 보고되는 병렬화 관련 함정 셋을 짚자.

**함정 1 — 멀티스레드를 켰는데 데이터가 중복/누락된다.**

원인: stateful Reader를 멀티스레드 step에 그대로 썼다. 6.0의 producer-consumer 모델로 일부 완화됐지만, **데이터 정확성이 중요하면 멀티스레드 대신 partitioning**을 써야 한다. 이 함정을 만나면 멀티스레드 step을 partitioning으로 옮기는 작업이 답이다.

**함정 2 — Partition gridSize를 너무 키웠더니 DB가 죽었다.**

원인: gridSize × 청크당 DB 연결 수가 DB 풀 한도를 넘었다. worker들이 connection을 받지 못해 대기하거나, DB 자체가 동시 연결 한도에 도달했다. **gridSize는 DB 연결 한도의 50% 이내**로 잡는 게 안전하다.

**함정 3 — Connection timeout이 자주 난다.**

원인: 청크 사이즈가 너무 커서 한 트랜잭션이 30초를 넘어선다. JDBC connection idle timeout이 30초인 클라우드 환경에서 자주 보고됨. 해결 — 청크 사이즈를 줄이거나, JDBC batch를 1,000 단위로 분할(앞서 본 패턴), 또는 connection idle timeout을 늘림.

이 셋이 한국 OKKY와 GitHub Discussion에서 반복 보고되는 자리다. partitioning을 쓰고, 청크와 batch 크기를 측정으로 정렬하면 대부분 피할 수 있다.

## 정리 — 자기 잡에 적용할 순서

이 장의 결정 트리를 자기 잡에 적용하는 단계.

1. **측정한다.** 처리량, P95 청크 처리 시간, 메모리 사용량. 어디가 병목인가?
2. **단일 스레드 구조 점검** (6장 4단계). Processor I/O 묶기, JdbcBatchItemWriter, IN 절 그룹화, chunk·page·fetch 정렬.
3. **여전히 느리다면 partitioning을 1순위로 검토.** 데이터가 깔끔히 분할 가능한가? gridSize는 DB 연결 한도의 50% 이내.
4. **Process가 매우 무겁다면** Remote Chunking 검토 (메시징 인프라 추가 비용).
5. **멀티스레드 step은 마지막 수단.** restartability 약화 감수, stateful reader 회피, deadlock 위험 점검.
6. **6.0 신규 Remote Step**은 step별 자원 특성이 매우 다를 때만.

이 순서를 지키면, 잡이 느려질 때마다 다음 카드가 자연스럽게 보인다. 그리고 **카드를 잘못 꺼내서 데이터가 깨지는 일이 없다.** 그게 production-ready 잡의 핵심이다 — 빠른 게 다가 아니라, 빨라지면서도 정확한 잡.

다음 장으로 넘어가, 이 잡들이 운영 환경에서 어떻게 보이는지를 보자. Micrometer 메트릭, Prometheus, Grafana 대시보드, JFR, 그리고 — 가장 어려운 일인 알람 임계값 설계까지. "잡이 1시간 걸리던 게 어느 날 2시간이 됐다"의 답이 거기에 있다.
