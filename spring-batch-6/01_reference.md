# Spring Batch 6 완전 정복 — 레퍼런스 문서

> 책 저술을 위해 수집한 1차 리서치. 출처별이 아니라 주제별로 재조직되어 있다. 각 항목 끝의 `[웹]` `[논문]` `[커뮤니티]` 표기는 어느 스트림에서 나온 정보인지를 가리키며, 같은 주장이 여러 소스에 있으면 한 곳만 대표 인용한다. 본문 챕터를 쓸 때 이 문서를 1차 자료로 삼는다.

> **대상 독자 환기:** Spring/Spring Boot 익숙, 직접 배치 코드도 짜본 경험은 있지만 Spring Batch는 처음. 따라서 "왜 굳이 프레임워크냐"는 의문에 답하는 비중을 크게 두고, JCL/메인프레임 시대의 배치 역사 같은 너무 먼 배경은 비중을 줄였다.

---

## 1. 개념과 정의

### 1.1 배치 처리란 무엇인가
배치 처리는 사용자 인터랙션 없이, 정해진 양의 데이터를 정해진 시간 창에서 일괄 처리하는 일이다. 일반적으로 `대량 + 비동기 + 시간 창` 세 조건이 결합된다. 결제 정산, 일말 마감, 데이터 마이그레이션, 통계 집계, 파일 ETL이 대표 사례다. 대량 작업을 웹 요청 처리 자원과 같은 풀에서 돌리면 사용자 응답성이 망가지므로, 운영상 별도 서버·별도 프로세스로 격리하는 것이 정석이다. [커뮤니티: velog 다수, OKKY]

배치 vs 실시간 처리의 분리는 시스템 설계의 영구적인 트레이드오프다. 학술 문헌은 이를 `Lambda 아키텍처`(배치 레이어 + 스트리밍 레이어 병행)와 `Kappa 아키텍처`(스트리밍 단일화) 등으로 형식화하며, 배치는 **글로벌 일관성과 정확성**을 책임지는 layer로 남는 경향이 명확하다. [논문: arxiv 2511.03393, Databricks blog]

### 1.2 Spring Batch란
Spring Batch는 Spring 진영에서 배치 애플리케이션을 작성하기 위한 표준 프레임워크다. JCL/COBOL 같은 메인프레임 배치 운용 노하우를 Java/Spring 모델로 옮긴 것이 출발점이며, 다음을 표준화한다.

- **모델:** `Job` → `Step` (1:N) → `Step` 안의 `ItemReader` → `ItemProcessor` → `ItemWriter` (chunk-oriented)
- **메타데이터:** 모든 실행 이력을 `JobRepository`에 저장 — `JobInstance`, `JobExecution`, `StepExecution`, `ExecutionContext`
- **재시작·트랜잭션·예외 처리:** Skip / Retry / Restart / Rollback이 프레임워크 차원에서 제공
- **확장:** Multi-thread Step, Partitioning, Remote Chunking, Remote Step

대상 독자(이미 배치 코드를 직접 작성해본 백엔드 개발자)에게 Spring Batch를 한 줄로 요약하면 다음과 같다: **"`재실행 안전성 + 메타데이터 + 청크 트랜잭션 경계`를 직접 짜지 않게 해주는 프레임워크."** 직접 배치 짜본 사람이 결국 다시 만들게 되는 인프라가 이미 들어 있다는 점이 핵심 포지션이다. [웹: Spring Batch Reference Architecture]

### 1.3 chunk-oriented vs tasklet
Spring Batch의 Step은 두 모델을 가진다.
- **chunk-oriented:** Reader가 한 건씩 읽고, Processor가 변환하고, 누적된 청크가 commit-interval에 닿으면 Writer가 한 번에 쓰고 트랜잭션 커밋. 대량 항목 반복 처리에 표준.
- **tasklet:** "한 덩어리의 단발성 작업"용. 파일 압축, 디렉터리 정리, 외부 명령 실행처럼 항목 단위 반복이 어색한 일에 쓴다. [웹: Baeldung "Tasklets vs Chunks", Spring Batch Reference]

이 책에서는 **9 대 1 비중으로 chunk-oriented가 본류**임을 분명히 하고, tasklet은 보조 도구로 자리매김한다.

---

## 2. 핵심 아키텍처

### 2.1 레이어 구조
공식 레퍼런스가 말하는 3 레이어는 이렇다.
- **Application:** 개발자가 작성하는 Job/Step 정의와 비즈니스 로직.
- **Batch Core:** Job, Step, JobLauncher/JobOperator 등 런타임 핵심.
- **Batch Infrastructure:** Reader/Writer 구현체, Repository, Retry/Skip 정책 등.

이 3-layer 분리는 "내 도메인 로직(Application)이 프레임워크 변경(Core)에 끌려가지 않도록"이라는 분명한 의도가 있다. [웹: Spring Batch Reference "Architecture"]

### 2.2 Job, Step, JobInstance, JobExecution 의 관계
- **Job:** 추상 정의. "결제 정산 잡"처럼 이름과 흐름만 있는 청사진.
- **JobInstance:** 같은 Job이라도 실행되는 비즈니스 단위(ex. `2026-05-08 정산`). JobParameters로 식별.
- **JobExecution:** JobInstance의 실제 실행 시도. 같은 인스턴스가 실패해서 다시 돌면 JobInstance 1 + JobExecution N.
- **Step / StepExecution:** 같은 식의 1:N 관계가 Step에서도 성립.
- **ExecutionContext:** Job/Step 단위로 따로 관리되는 key-value 상태. 재시작 시 reader의 마지막 위치 등을 저장하는 데 쓰인다.

이 관계는 **재시작이 가능한 이유**다. JobInstance가 동일하면 이전 JobExecution 상태를 가져와 실패한 곳부터 다시 돈다. [웹: Spring Batch Reference, OKKY 답변]

### 2.3 ItemReader / Processor / Writer 계약
- `read()`은 `null`로 입력 종료를 알린다. stateful해도 됨.
- `process(item)`은 `null` 반환 시 해당 항목을 필터링(skip이 아님).
- `write(List<? extends T> chunk)`는 청크 단위 쓰기. 트랜잭션 1건당 1회 호출이 원칙.

내장 Reader 라인업: `FlatFileItemReader`, `JdbcCursorItemReader`, `JdbcPagingItemReader`, `JpaPagingItemReader`, `MongoItemReader`, `JsonItemReader`, `StaxEventItemReader` 등. 한국 커뮤니티에서 가장 많이 언급되는 것은 `JdbcPagingItemReader`(메모리 효율), 그리고 jojoldu(이동욱)의 `QuerydslPagingItemReader`/`QuerydslNoOffsetPagingItemReader` (커서 기반 페이징, Querydsl 친화). [웹+커뮤니티: jojoldu/spring-batch-querydsl, 우아한형제들 기술블로그 "Spring Batch와 Querydsl"]

### 2.4 트랜잭션 경계와 청크
**핵심 규칙: chunk = transaction.** 청크 안에서 한 항목이 실패하면 청크 전체가 롤백된다. 이게 idempotency 설계의 출발점이다. 즉 "내 Writer는 같은 청크를 두 번 받아도 결과가 같아야 한다"가 기본 가정이 되어야 한다. 이 점이 직접 배치 짜본 개발자가 가장 흔히 놓치는 부분이며, OKKY/StackOverflow에서 반복 등장하는 질문이기도 하다. [웹: Spring Batch Reference "Chunk-oriented Processing", Baeldung; 커뮤니티: OKKY 다수]

추가로 알아둘 것: `chunk size` ≠ `page size` ≠ `fetch size`. 셋은 다른 개념이며 혼동이 매우 흔하다. 챕터에서 명시적으로 쪼개야 한다. [웹: Stack Overflow 정리, dev.to "chunk and fetchSize"]

---

## 3. Spring Batch 6 변경점 (이 책의 차별화 포인트)

### 3.1 출시 타임라인 (2025)
- **2025-07-23:** 6.0.0-M1
- **2025-08-20:** 6.0.0-M2 — `JobOperator#recover` 도입
- **2025-09-17:** 6.0.0-M3 (5.2.3 동시 출시)
- **2025-10-09:** 6.0.0-M4
- **2025-11-19:** **6.0.0 GA** ← 책의 기준
- **2025-12-17:** 6.0.1 maintenance

[웹: spring.io/blog 시리즈, github releases]

### 3.2 의존성·플랫폼 baseline
- Java 17+ (5.x와 동일, 변동 없음)
- Spring Framework **7.0**
- Spring Data **4.0**, Spring Integration **7.0**, Spring AMQP/Kafka **4.0**
- Micrometer **1.16**
- Spring Boot **4.0**으로 출하
- Jackson **3.x** 기본 (2.x deprecated)

[웹: docs.spring.io/spring-batch/reference/whatsnew.html, GA blog]

### 3.3 chunk-oriented 모델의 근본 재설계
이번 메이저의 가장 큰 변화. `ChunkOrientedTasklet`/`TaskletStep` 조합이 deprecated 되고, 안정 버전 `ChunkOrientedStep` + `ChunkOrientedStepBuilder` 가 등장한다.

```java
@Bean
Step step(JobRepository jobRepository, ItemReader<Person> r, ItemWriter<Person> w) {
    return new ChunkOrientedStepBuilder<Person, Person>("step", jobRepository, 100)
        .reader(r)
        .writer(w)
        .build();
}
```

레퍼런스 문서에서 직접 언급한 이전 모델의 한계: **"`maxItemCount`가 멀티스레드 스텝에서 지켜지지 않거나, 롤백 시 상태가 어긋나 optimistic locking 이슈가 나거나, throttle 동작이 부정확하고 성능도 좋지 않았다."** 6에서는 producer-consumer + bounded queue 모델로 갈아엎었다. [웹: whatsnew.html, github issue #3950]

### 3.4 동시성 모델: producer-consumer + bounded queue
6.0의 멀티스레드 step은 producer 1 + consumer N의 단방향 큐 구조다.
- producer는 reader에서 읽은 항목을 큐에 푸시
- consumer 스레드 N이 큐에서 꺼내 process → write
- 청크가 차서 write가 진행되는 동안 producer는 일시 정지
이전 "parallel iteration" 모델보다 코드/상태 동기화가 단순해지고 처리량이 향상되었다는 것이 변경 동기. [웹: whatsnew.html]

### 3.5 신규 어노테이션: `@EnableJdbcJobRepository`, `@EnableMongoJobRepository`
`@EnableBatchProcessing`이 두 갈래로 갈라졌다.
- `@EnableBatchProcessing` → **공통** 인프라 속성만 (taskExecutor 등)
- `@EnableJdbcJobRepository(dataSourceRef=…, transactionManagerRef=…)` → JDBC 저장소 전용
- `@EnableMongoJobRepository(...)` → MongoDB 저장소 전용

**`@EnableBatchProcessing(modular = true)`는 deprecated.** 대신 Spring 컨텍스트 계층 + `GroupAwareJob`을 쓰라는 권고. [웹: 6.0 Migration Guide]

### 3.6 MongoDB JobRepository 정식 지원
RDB 없이 NoSQL만 쓰는 시스템도 메타데이터 저장소를 1급 시민으로 가질 수 있다. `MongoTemplate`, `MongoTransactionManager` 빈 + `@EnableMongoJobRepository`. MongoDB 4 이상 필요. 5.2에서 도입돼 6.0에서 정착됐다. [웹: medium "Spring Batch Now Supports NoSQL", 5.2 release blog]

### 3.7 `JobRepository` ⊃ `JobExplorer` / `JobOperator` ⊃ `JobLauncher`
인터페이스 통합. **`JobLauncher`/`JobExplorer` 빈을 따로 등록할 필요가 없다.** `JobOperator` 하나가 launch + explore + control을 다 한다. 마이그레이션 시 `JobLauncher` 주입은 `JobOperator`로 바꾼다. [웹: 6.0 Migration Guide]

### 3.8 `JobOperator#recover()` — 복구 API
컨테이너가 갑자기 죽어 `STARTED` 상태로 박제된 JobExecution을 안전하게 `FAILED`로 마킹해 재시작 가능 상태로 만드는 표준 API. 이전엔 DB를 직접 손대거나 별도 유틸이 필요했는데, 이게 메서드 한 방으로 해결된다.

```java
jobOperator.recover(executionId);
```

`SimpleJobOperator`, `CommandLineJobOperator` 모두 구현체 제공. [웹: 6.0 API doc, M2 blog]

### 3.9 Graceful Shutdown
JVM 종료 신호를 받으면 실행 중인 Job/Step에 인터럽트를 전달하고, JobRepository에 일관된 상태를 기록한 뒤 종료한다. **K8s 환경에서 이 기능 부재가 매우 큰 운영 리스크였는데, 6.0이 정식 셧다운 훅을 제공한다.** [웹: whatsnew, Kubernetes 운영 글들]

### 3.10 `StoppableStep` 인터페이스
이전엔 Tasklet 기반 Step만 `JobOperator#stop`에 응답할 수 있었다. 6에서는 `StoppableStep`을 구현하면 어떤 Step이든 외부 stop 신호를 받을 수 있다. [웹: whatsnew]

### 3.11 JFR(Java Flight Recorder) 옵저버빌리티
Micrometer 메트릭 외에 JFR 이벤트를 발행한다. job/step/item read·write/transaction 경계를 JFR 이벤트로 잡을 수 있어, profiler/디버깅 도구 친화. 오버헤드는 명시적으로 "minimal". [웹: whatsnew, GA blog]

### 3.12 JSpecify null 안정성
모든 public API에 JSpecify(`@Nullable`, `@NonNull` 등) 어노테이션이 붙는다. IntelliJ/Errorprone 통합 시 컴파일 시점에 null 위반을 잡을 수 있다. [웹: GA blog]

### 3.13 Spring Boot의 `@EnableBatchProcessing` 권고 변화
> Spring Boot 3 이상에서는 `@EnableBatchProcessing`을 직접 붙이는 것이 **discouraged**. `BatchAutoConfiguration`이 자동 구성하기 때문에 직접 붙이면 자동 구성을 끄게 된다.

이건 5에서 시작된 흐름이지만 6에서도 그대로 유효. [웹: docs.spring.io/spring-boot reference; Baeldung]

### 3.14 패키지 이동·이름 변경 (대량)
6 마이그레이션 가이드의 핵심 부담. 대표 사례:
- `org.springframework.batch.*` → `org.springframework.batch.infrastructure.*`
- `org.springframework.batch.core.explore` → `org.springframework.batch.core.repository.explore`
- `org.springframework.batch.core.partition.support` → `org.springframework.batch.core.partition`
- `org.springframework.batch.core.listener.*` 신규 정리
- `JobRepositoryFactoryBean` → `JdbcJobRepositoryFactoryBean`
- `JobExplorerFactoryBean` → `JdbcJobExplorerFactoryBean`
- `ChunkHandler` → `ChunkRequestHandler`
- `JobStep.setJobLauncher(JobLauncher)` → `setJobOperator(JobOperator)`
- 시퀀스 이름 변경: `BATCH_JOB_SEQ` → `BATCH_JOB_INSTANCE_SEQ`

[웹: 6.0 Migration Guide]

### 3.15 도메인 모델 불변성·`JobParameters` 재설계
- `Entity` ID는 wrapper `Long`에서 primitive `long`으로 바뀜.
- ID 재할당 불가. 부모 없는 orphan 엔티티 생성 불가.
- `JobParameter`는 **record** 타입으로, 파라미터 이름까지 자체 보유.
- `JobParameters`는 `Set<JobParameter>` 기반 (이전 `Map<String, JobParameter>`).
- **중요한 호환성 경고:** v5에서 실패한 Job Instance를 v6로 재시작하는 것은 **직렬화 포맷 차이로 불가능**. 마이그레이션 시 진행 중인 잡은 5에서 끝낸 뒤 올려야 한다.

[웹: 6.0 Migration Guide]

### 3.16 fault-tolerance 재구성
- Retry는 Spring Retry 라이브러리 의존을 떼고 **Spring Framework 7의 retry 기능** 위로 이전.
- Skip은 `SkipPolicy` 인터페이스 하나로 통합.
- 새 빌더 사용:
  ```java
  RetryPolicy retryPolicy = RetryPolicy.builder()
      .maxRetries(10).includes(Set.of(TransientException.class)).build();
  SkipPolicy skipPolicy = new LimitCheckingExceptionHierarchySkipPolicy(
      Set.of(FlatFileParseException.class), 50);
  return new ChunkOrientedStepBuilder<>(...)
      .reader(r).writer(w)
      .faultTolerant().retryPolicy(retryPolicy).skipPolicy(skipPolicy)
      .build();
  ```
[웹: whatsnew]

### 3.17 신규 `CommandLineJobOperator`
`CommandLineJobRunner`(이전 산물)를 대체하는 모던 CLI 진입점. start/stop/restart 표준 옵션 제공. Spring Boot CLI 컨벤션과 정합. [웹: API doc, Migration Guide]

### 3.18 람다 스타일 빌더
빌더 코드를 더 간결하게 쓸 수 있는 컨텍스추얼 람다.
```java
new FlatFileItemReaderBuilder()
    .resource(...)
    .delimited(c -> c.delimiter(',').quoteCharacter('"'))
    .build();
```
[웹: whatsnew]

### 3.19 Local Chunking + Remote Step + SEDA via Spring Integration
- **Local chunking:** 같은 JVM 내 다중 스레드 청크 처리.
- **Remote Step:** 스텝 단위로 원격 노드에서 실행.
- **SEDA:** Spring Integration 메시지 채널을 활용한 스테이지 간 비동기 분리. 5.2의 local SEDA가 이번에 메시징 기반으로 확장.

대규모 병렬화 옵션의 정리. [웹: whatsnew, GA blog]

### 3.20 deprecation 정리 (한눈에)
이전 deprecated API 일괄 제거. 새로 deprecated 된 것:
- `@EnableBatchProcessing(modular=true)`
- `batch:` / `batch-integration:` XML 네임스페이스 (v7에서 제거 예정)
- JUnit 4 지원 (`spring-batch-test`)
- Jackson 2.x

[웹: 6.0 Migration Guide]

---

## 4. 실전 유스케이스

### 4.1 대용량 데이터 일괄 처리 (대표 패턴)
- 입력: 수천만~수억 행의 RDB 테이블 또는 멀티 GB 플랫 파일.
- 처리: 도메인 변환 + 검증 + 외부 시스템 호출 (선택).
- 출력: 다른 RDB 테이블 / S3 / Kafka / 다른 시스템 API.
- 핵심 구성: `JdbcPagingItemReader` 또는 jojoldu의 `QuerydslNoOffsetPagingItemReader` + chunk size 500–2000 + JDBC batch insert + 파티셔닝(필요 시). [웹+커뮤니티]

### 4.2 ETL / 데이터 마이그레이션
시스템 A → 시스템 B로 데이터를 옮기되, 변환·정합성 검증·실패 항목 격리가 필요한 경우. Spring Batch는 chunking + retry/skip + restart 모델 덕에 ETL 파이프라인의 신뢰성 layer로 기능한다. 학술 문헌은 ETL/ELT/ETLT 패턴을 형식화하며 batch는 글로벌 일관성 검증 layer로 자리잡았다고 보고한다. [논문: arxiv 2511.03393 "Formalizing ETLT and ELTL"; 웹: skyvia/inexture 블로그]

### 4.3 정산 (Settlement) — 카카오페이 사례
카카오페이 정산팀이 공개한 실 개선 사례는 이 책의 가장 강력한 한국 레퍼런스다. 요점:
- **증상:** 50,000건 이상 처리 시 1시간+ 소요.
- **원인 1:** Processor에서 외부 API를 단건 호출(150ms × N) → 네트워크 I/O가 직렬로 누적.
- **원인 2:** `JpaItemWriter` Dirty Checking으로 청크 안에서 개별 UPDATE.
- **개선 1:** Processor 제거, Writer에서 일괄 처리하도록 구조 변경.
- **개선 2:** RX Kotlin + `Schedulers.io()`로 10 레일 병렬 — **약 10배 향상**.
- **개선 3:** 동일 값 UPDATE는 그룹화 후 IN 절로 — 1,000건 개별 UPDATE → 최대 3건 IN UPDATE → **5,000건 이상에서 90%+ 향상**.
- **개선 4:** 개별 값 UPDATE는 JDBC Batch (Exposed의 `BatchUpdateStatement`) 활용, 1,000건 단위 분할로 connection timeout 회피.
- **결론 인용:** **"처음부터 병렬 처리보다 현재 구조에서 I/O 작업을 묶어서 처리하는 것이 효율적이다."**

이 케이스 스터디는 책의 정산 챕터의 backbone으로 쓸 수 있다. [커뮤니티: tech.kakaopay.com "Spring Batch 애플리케이션 성능 향상을 위한 주요 팁"]

### 4.4 통계·집계
일말/시간 단위 거래량 집계, 사용자 활동 로그 집계 등. Spring Batch의 step 흐름과 ExecutionContext가 자연스럽게 맞다. velog 다수 글이 "특정 날짜 기준 합산" 잡을 입문 예제로 다룸. [커뮤니티: velog]

### 4.5 파일 ETL
플랫 파일·CSV·JSON·XML 입력 → 검증 → DB/S3/Kafka 출력. `FlatFileItemReader`/`JsonItemReader`/`StaxEventItemReader`. 우아한형제들의 "주소 DB 구축" 사례가 대표적. [커뮤니티: woowabros 블로그 "주소검색서버 개발기"]

### 4.6 금융 정산·재무 보고
금융권에서 Spring Batch는 일말 reconciliation 엔진으로 자주 쓰인다. 학술/산업 자료는 reconciliation 시스템의 3 요소를 강조한다: (1) 다중 소스 ingest, (2) intelligent matching, (3) mismatch 처리. 이벤트 소싱과 결합 시 reconciliation 시간을 약 60% 줄인다는 보고도 있다. [논문/웹: Databricks "Design Patterns for Batch Processing in Financial Services", Cognizant]

---

## 5. 성능·확장 (운영 관점)

### 5.1 chunk size / page size / fetch size
- **chunk size:** 트랜잭션 1건당 처리할 항목 수.
- **page size (Paging Reader):** Reader가 한 페이지에 가져올 행 수.
- **fetch size (JDBC):** JDBC 드라이버가 네트워크 라운드트립 1회당 가져올 행 수.

권장: **chunk size = page size**, fetch size는 chunk size 이상으로 설정해 라운드트립을 줄인다. 시작값으로는 chunk = page = 500–1,000, fetch = 1,000이 흔한 출발점. 단 production 데이터로 반드시 측정. [웹: dev.to "chunk size and fetchSize"; medium "Cursor vs Paging"]

### 5.2 Cursor vs Paging Reader
- **Cursor (`JdbcCursorItemReader`):** DB 커서로 한 트랜잭션 안에서 끝까지 읽음. 메모리 효율 좋고 일관성 강함. 그러나 **장시간 트랜잭션** + DB 커서 핸들 점유 위험. 매우 큰 데이터에서 일부 DB 벤더(특히 DB2)가 lock 문제를 일으킨다.
- **Paging (`JdbcPagingItemReader`):** OFFSET/LIMIT 또는 keyset으로 페이지 단위 읽기. 장시간 트랜잭션 회피, 재시작 친화. 단 OFFSET은 N이 커지면 비용 폭증 → **keyset(no-offset) pagination** 권장.

수억 행 규모에서는 Paging + keyset이 사실상 표준. [웹: medium "Cursor vs Paging"; jojoldu의 `QuerydslNoOffsetPagingItemReader`]

### 5.3 멀티스레드 step
가장 단순한 병렬화. `taskExecutor` 지정 + `throttleLimit` 으로 동시 처리 수 제어. 6.0에서 producer-consumer 모델로 재설계되어 이전 모델의 상태 동기화·throttle 이슈가 해소됨. **트레이드오프:** Reader/Writer 상태가 thread-safe해야 하고, restartability가 약화됨(공유 reader 상태가 재시작 시 일관되지 않음). [웹: Spring Batch Reference Scalability]

### 5.4 Partitioning
입력을 N 등분해서 N개의 워커 step에 분배. 마스터 step이 `Partitioner`로 분할 → `PartitionHandler`가 워커 step을 지휘.
- **로컬 파티셔닝:** `TaskExecutorPartitionHandler`로 같은 JVM 내 스레드에서 분할 실행.
- **원격 파티셔닝:** Spring Integration 메시지 채널로 다른 노드의 워커 호출.

장점: 멀티스레드 step과 달리 각 워커가 자기 데이터만 보므로 **restartability 유지**. 가장 많이 쓰이는 수평 확장 옵션. [웹: Spring Batch Reference, howtodoinjava]

### 5.5 Remote Chunking
Reader/Process는 master에서 동작, Writer만 워커로 분산. master가 병목이 아닌 경우, 즉 **process 비용이 read 비용보다 훨씬 큰 경우**에만 의미가 있음. 메시지 큐(Spring Integration) 필수. [웹: Spring Batch Reference Scalability]

### 5.6 Remote Step (6.0 신규)
파티셔닝의 외삽: Step 자체를 다른 노드에서 통째로 실행. 분산 환경에서 더 자유로운 분배가 가능. [웹: whatsnew]

### 5.7 K8s에서의 운영
실무에서 Spring Batch + K8s는 다음 패턴이 정착:
- **K8s `CronJob`** 으로 스케줄링 (Pod-당-Job 1개)
- **Pod 그레이스 풀 셧다운**: K8s가 Pod 종료 시 graceful shutdown을 보장하지 않으므로 `restartPolicy`/`backoffLimit`/Spring Batch 6.0의 graceful shutdown hook을 모두 활용.
- **JobRepository 정리:** Job/Step Execution 메타가 빠르게 누적되므로 정기적인 정리 잡 필요.
- **단일 Pod = 단일 Job:** "한 Pod에 여러 Job 컨테이너"는 cloud-native 관점에서 권장되지 않음.

[웹: spring.io/blog "Spring Batch on Kubernetes", BootLabs Tech]

### 5.8 옵저버빌리티 (Spring Batch + Spring Boot Actuator + Micrometer)
- Spring Batch 4.2부터 Micrometer 기반 메트릭 제공. 5.x부터는 트레이싱(Job=trace, Step=span)도.
- 6.0에서는 **`ObservationRegistry` 빈을 컨텍스트에 등록해야** 메트릭이 수집된다 (전역 정적 레지스트리 폐기).
- 메트릭 prefix: `spring.batch.`
- Spring Boot Actuator + `micrometer-registry-prometheus` → `/actuator/prometheus` → Grafana 대시보드.
- 6.0의 JFR 이벤트는 이와 별개로, 더 저수준의 흐름(트랜잭션 경계 등)을 잡고 싶을 때.

[웹: docs.spring.io/spring-batch reference observability, dataflow.spring.io]

---

## 6. 에러 처리·재실행 (책의 한 챕터 전체 분량)

### 6.1 Skip / Retry / Restart 의 의미
- **Skip:** 특정 예외가 났을 때 그 *항목*을 건너뛰고 잡은 계속 진행. `skipLimit`까지 누적되면 잡 실패.
- **Retry:** 일시적 오류(네트워크/DB 락)에 대해 같은 항목을 N회 재시도. 백오프 정책 가능.
- **Restart:** 잡 자체가 실패했을 때, 동일 JobInstance를 다시 호출하면 마지막 커밋된 청크 다음부터 재실행.

순서 중요: **retry → skip.** 재시도가 모두 실패한 다음에야 skip 정책을 본다. [웹: Baeldung "Configuring Retry/Skip", Spring Batch Reference]

### 6.2 fault-tolerant step 빌드 (6.0)
3.16 절 참고. 핵심:
- `RetryPolicy.builder().maxRetries(N).includes(...)`
- `SkipPolicy` 구현 또는 `LimitCheckingExceptionHierarchySkipPolicy`
- `.faultTolerant()` 호출이 트리거.

### 6.3 Skip 발생 시 청크 동작
하나의 항목이 skip 되더라도 청크 트랜잭션이 롤백되는 경우, **재처리는 chunk size = 1로 항목 단위 단건 모드로 자동 전환**된다. 이건 의외로 놓치는 동작이며, 멀티스레드 step에서 reader 일관성 문제를 일으킬 여지가 있다. [웹: Baeldung "Configuring Skip", terasoluna 가이드]

### 6.4 Restart 안전성 — idempotency
restartable한 잡을 만들려면 다음을 만족해야 한다.
1. **ItemWriter는 같은 청크를 두 번 받아도 동일 결과**여야 한다 (멱등).
2. **ItemReader는 ExecutionContext에 진행 위치를 저장**해야 한다. 내장 Reader는 대체로 자동.
3. **외부 부수효과(이메일 발송, 송금)** 가 있다면 단순 멱등으로는 부족 — outbox 테이블, 멱등 키, dedupe 저장소 같은 추가 장치 필요.

[웹: Spring Batch Reference Transaction Appendix, Baeldung]

### 6.5 STARTED 상태 박제 문제
컨테이너가 SIGKILL 등으로 갑자기 죽으면 JobExecution이 `STARTED`로 박제되어 "이미 실행 중인 인스턴스가 있다"고 거부당한다. **6.0 이전:** DB를 직접 손대 상태를 `FAILED`로 바꿔야 했다. **6.0 이후:** `JobOperator.recover(executionId)` 한 줄. K8s 운영에서 매우 큰 차이를 만든다. [웹: github discussion #4532, 6.0 API]

### 6.6 SkipListener/JobExecutionListener 패턴
스킵된 항목을 별도 테이블/파일/Slack으로 보내 사람이 후처리할 수 있게 만드는 게 흔한 운영 패턴. `JobExecutionListener`로 시작/종료 시점에 로그·알림·메트릭. [웹: Java Code Geeks "Robust Error Handling"]

---

## 7. 커뮤니티 인사이트 — 실제 개발자가 부딪히는 지점

이 섹션은 책의 **챕터 도입부 통증 묘사**(pain point 훅)와 **함정 챕터**의 1차 자료다.

### 7.1 가장 자주 보고되는 문제들 (Reddit/StackOverflow/OKKY 종합)
- **트랜잭션 경계 오해:** 청크 = 트랜잭션이라는 점을 모르고 쓰다가 부분 처리/이중 처리에 당함. [커뮤니티: dev.to, javanexus, OKKY]
- **OOM (Out of Memory):** 60만 건 단위 ItemStream에서 메모리 폭발. 원인은 페이징/커서 미적용 또는 Reader가 모든 항목을 메모리에 로드. [커뮤니티: OKKY 1489911]
- **`@StepScope` 사용법 함정:** 잘못 쓰면 빈이 늦게 생성되어 NPE/주입 실패. [커뮤니티: OKKY 380648]
- **재시작 안 되는 잡:** "한 번 실패하면 어떤 식으로 재시작해야 하는지 모르겠다." JobInstance 동일성을 만들어주는 JobParameters 설계가 빠진 경우가 대부분. [커뮤니티: OKKY 다수]
- **잡이 두 번 도는 현상:** Spring Boot 자동 실행 + 수동 트리거가 겹친 경우. `spring.batch.job.enabled=false` 모르는 케이스. [커뮤니티: OKKY 268704]
- **chunk size vs page size 혼동:** 가장 흔한 입문자 질문. [커뮤니티: StackOverflow 다수]

### 7.2 비판·논쟁점
- **"Spring Batch는 design이 verbose하고 reuse가 어렵다"** 는 강한 비판이 dev.to "Why is SpringBatch a poor design?"과 일부 Quora 답변에 존재. 객체 생성·설정·라이프사이클이 무거워 작은 잡에는 과한 도구라는 주장.
- **반론:** 작은 잡엔 Spring scheduler + 평범한 코드면 되고, Spring Batch는 **재시작·메트릭·운영 표준화**가 필요한 규모에서 진가가 나온다는 것이 다수 의견. 우아한형제들·카카오페이의 실 사례가 후자 입장의 강력한 근거.
- **Airflow와의 비교:** "여러 잡 의존성 + DAG + 시각화" 가 필요하면 Airflow가 더 어울린다. Spring Batch는 **잡 하나의 내부 신뢰성**에 강점, Airflow는 **잡들 사이의 오케스트레이션**에 강점. 둘은 보완적. [웹: SaaSHub 비교, hevodata]

### 7.3 한국 커뮤니티 토픽 분포 (체감)
- **velog/tistory 글의 70% 정도가 입문 → JobBuilder/StepBuilder 예제, 정산 잡, 일말 통계.**
- **OKKY의 질문은 운영 단계 이슈에 집중:** OOM, `@StepScope`, 재시작, 잡 중복 실행, 트랜잭션 분리.
- **기업 블로그(우아한형제들·카카오페이):** 성능 튜닝 중심.

이 분포는 책의 챕터 비중 결정에 그대로 활용 가능: 입문 챕터(빠르게) → 운영 챕터(가장 두껍게) → 성능 튜닝 챕터(실 사례 포함).

---

## 8. 안티패턴·주의사항

### 8.1 트랜잭션 미설계
청크 트랜잭션 경계, transactionManager 미지정, JpaItemWriter Dirty Checking으로 인한 N건 개별 UPDATE — 이 셋이 "성능이 안 나오면 90%는 여기"의 정확한 위치. [커뮤니티: kakao pay 사례]

### 8.2 Reader가 모든 데이터를 한 번에 메모리로
List를 통째로 들고 있는 직접 작성 Reader는 OOM의 지름길. PagingReader/CursorReader/Querydsl no-offset reader 중 하나로 강제할 것. [커뮤니티: OKKY OOM 사례]

### 8.3 Writer 비멱등성
같은 청크를 두 번 받았을 때 결과가 달라지면 retry/restart가 모두 위험해진다. UPSERT/dedupe key/outbox 패턴 중 하나는 거의 필수. [웹: Spring Batch Reference]

### 8.4 한 트랜잭션에 reader cursor 점유 + 외부 API 호출
cursor가 열린 채로 외부 API를 동기 호출하면 DB 락이 길게 잡힌다. Paging Reader 또는 reader/processor 분리(SEDA 패턴) 고려. [웹: Spring Batch Reference batch-processing-strategies]

### 8.5 멀티스레드 step + stateful Reader
공유 Reader가 thread-safe하지 않으면 데이터 손실/중복. 6.0의 producer-consumer 모델이 일부 완화하지만, **restartability를 원하면 Partitioning으로 가는 게 정석**. [웹: hevodata, Spring Batch Reference]

### 8.6 JobParameters 설계 미스
JobInstance를 매일 새로 만들고 싶은데 파라미터가 항상 같으면 "이미 동일 인스턴스가 있다"고 거부당한다. 일자/run.id 등 식별자 파라미터 필수. [커뮤니티: OKKY 다수]

### 8.7 Spring Boot 자동 실행과 명시적 launch 충돌
`spring.batch.job.enabled=false`로 자동 실행을 끄거나, `spring.batch.job.name`으로 1개만 지정. 모르고 쓰면 같은 잡이 부팅마다 자동으로 한 번 더 돈다. [커뮤니티: OKKY 268704]

### 8.8 K8s graceful shutdown 미설계
`terminationGracePeriodSeconds` 짧고 graceful shutdown 훅 없음 + recover API 모름 → 매번 DB를 직접 고치게 된다. 6.0에서는 graceful shutdown + `recover()`로 해결. [웹: spring.io blog "Spring Batch on Kubernetes"]

### 8.9 메타데이터 테이블 무한 누적
정기 정리 잡 없이 운영하면 `BATCH_JOB_EXECUTION`/`BATCH_STEP_EXECUTION`이 수천만 행으로 자라 잡 시작이 느려짐. 정리 잡(보존 기간 N일)은 필수. [웹: spring.io blog]

---

## 9. 실무 적용 팁 (체크리스트)

1. **잡 설계 단계:** 입력 출처, chunk size 후보, JobParameters 식별자, 재시작 정책을 먼저 종이에 그린다.
2. **Reader 결정 트리:** 파일 → Flat/JSON/Stax. RDB 큰 데이터 → Paging(가능하면 keyset/no-offset). RDB 작은 데이터 → Cursor.
3. **Writer 결정 트리:** RDB → JdbcBatchItemWriter (JPA Dirty Checking은 피한다). 외부 API → 멱등 키 + dedupe + 비동기/병렬화.
4. **chunk = page = (fetch ≥ chunk).** production 데이터로 반드시 측정.
5. **fault tolerance:** 일시 오류는 retry, 데이터 결함은 skip + listener로 격리, 영구 실패는 jobExecution 단위 fail.
6. **모니터링:** Micrometer + Prometheus + Grafana 기본. 6.0은 JFR도 추가.
7. **K8s:** CronJob 1잡, graceful shutdown 활성화, JobRepository 정리 잡 등록, recover API로 STARTED 박제 자동 정리.
8. **마이그레이션 (5 → 6):** 진행 중 JobInstance를 비우고 올린다. 자동 import 정리(패키지 이동), `JobLauncher`→`JobOperator`, `@EnableBatchProcessing`을 store-specific 어노테이션과 분리.

---

## 10. 참고문헌

### 공식 (Spring 진영)
- Spring Batch Reference, "What's new in Spring Batch 6", https://docs.spring.io/spring-batch/reference/whatsnew.html
- Spring Batch Reference, "Spring Batch Architecture", https://docs.spring.io/spring-batch/reference/spring-batch-architecture.html
- Spring Batch Reference, "Chunk-oriented Processing", https://docs.spring.io/spring-batch/reference/step/chunk-oriented-processing.html
- Spring Batch Reference, "Configuring Retry Logic", https://docs.spring.io/spring-batch/reference/step/chunk-oriented-processing/retry-logic.html
- Spring Batch Reference, "Scaling and Parallel Processing", https://docs.spring.io/spring-batch/reference/scalability.html
- Spring Batch Reference, "Configuring a JobRepository", https://docs.spring.io/spring-batch/reference/job/configuring-repository.html
- Spring Batch Reference, "Common Batch Patterns", https://docs.spring.io/spring-batch/reference/common-patterns.html
- Spring Batch Reference, "Micrometer support / Observability", https://docs.spring.io/spring-batch/reference/spring-batch-observability/micrometer.html
- Spring Batch 6.0 Migration Guide (GitHub Wiki), https://github.com/spring-projects/spring-batch/wiki/Spring-Batch-6.0-Migration-Guide
- Spring Batch GitHub Releases, https://github.com/spring-projects/spring-batch/releases
- spring.io blog, "Spring Batch 6.0.0-M1 is out!" (2025-07-23), https://spring.io/blog/2025/07/23/spring-batch-6/
- spring.io blog, "Spring Batch 6.0.0-M2 available now" (2025-08-20), https://spring.io/blog/2025/08/20/spring-batch-6/
- spring.io blog, "Spring Batch 6.0.0-M3 / 5.2.3" (2025-09-17), https://spring.io/blog/2025/09/17/spring-batch-6-0-0-m3-5-2-3-released/
- spring.io blog, "Spring Batch 6.0.0-M4 released" (2025-10-09), https://spring.io/blog/2025/10/09/spring-batch-6-0-0-m4-released/
- spring.io blog, "Spring Batch 6.0.0 GA is out!" (2025-11-19), https://spring.io/blog/2025/11/19/spring-batch-6-0-0-ga/
- spring.io blog, "Spring Batch 6.0.1 available now" (2025-12-17), https://spring.io/blog/2025/12/17/spring-batch-6-0-1-available-now/
- spring.io blog, "Spring Batch on Kubernetes" (2021-01-27), https://spring.io/blog/2021/01/27/spring-batch-on-kubernetes-efficient-batch-processing-at-scale/
- Spring Boot Reference, "Spring Batch", https://docs.spring.io/spring-boot/reference/io/spring-batch.html
- Spring Boot API doc, BatchAutoConfiguration, https://docs.spring.io/spring-boot/api/java/org/springframework/boot/autoconfigure/batch/BatchAutoConfiguration.html
- Spring Cloud Data Flow, "Task and Batch Monitoring with Prometheus and InfluxDB", https://dataflow.spring.io/docs/feature-guides/batch/monitoring/

### 웹 — 영문 블로그·튜토리얼
- Baeldung, "Introduction to Spring Batch", https://www.baeldung.com/introduction-to-spring-batch
- Baeldung, "Spring Boot With Spring Batch", https://www.baeldung.com/spring-boot-spring-batch
- Baeldung, "Spring Batch — Tasklets vs Chunks", https://www.baeldung.com/spring-batch-tasklet-chunk
- Baeldung, "Configuring Retry Logic in Spring Batch", https://www.baeldung.com/spring-batch-retry-logic
- Baeldung, "Configuring Skip Logic in Spring Batch", https://www.baeldung.com/spring-batch-skip-logic
- Baeldung, "Restart a Job on Failure and Continue in Spring Batch", https://www.baeldung.com/spring-batch-restart-job-failure-continue
- HowToDoInJava, "Spring Batch Example with Spring Boot", https://howtodoinjava.com/spring-batch/spring-boot-batch-tutorial-example/
- HowToDoInJava, "Spring Batch Partitioning into Multiple Steps", https://howtodoinjava.com/spring-batch/spring-batch-step-partitioning/
- Java Code Geeks, "Robust Error Handling in Spring Batch" (2025-02), https://www.javacodegeeks.com/2025/02/robust-error-handling-in-spring-batch.html
- Java Tech Blog (javanexus), "Common Spring Batch Pitfalls and How to Avoid Them", https://javanexus.com/blog/common-spring-batch-pitfalls
- DEV.to, "Why is SpringBatch a poor design?", https://dev.to/canonical/why-is-springbatch-a-poor-design-2bc
- DEV.to, "Understanding the Relationship Between chunk() Size and fetchSize in Spring Batch", https://dev.to/shaogat_alam_1e055e90254d/understanding-the-relationship-between-chunk-size-and-fetchsize-in-spring-batch-28n3
- Medium (Bayonne Sensei), "Spring Batch Now Supports NoSQL (MongoDB) as JobRepository", https://medium.com/@eddybayonne1/spring-batch-now-supports-nosql-mongodb-as-jobrepository-1278d459facd
- Medium (Nemal Perera), "Spring Batch Database ItemReaders: Cursor vs Paging", https://medium.com/@nemalperera3/spring-batch-database-itemreaders-cursor-vs-paging-622180d5c42b
- Medium (Vatsal Gupta), "Spring Batch on Steroids: Faster, Smarter, Scalable", https://medium.com/@vatsuvaksi/spring-batch-on-steroids-faster-smarter-scalable-d157bec3eaf5
- Medium (Youness Boutkhourst), "Increase Spring Batch Performance through multithreading", https://medium.com/@YounessBout/increase-spring-batch-performance-through-multithreading-b513ca90aeb5
- BootLabs Tech, "Spring Batch on Kubernetes — Jobs and CronJobs" (2024-07-15), https://blog.boottechsolutions.com/2024/07/15/lab7-spring-boot-k8s-spring-batch-on-kubernetes-jobs-and-cronjobs/
- DZone, "Chunk Oriented Processing in Spring Batch", https://dzone.com/articles/chunk-oriented-processing
- Databricks, "Design Patterns for Batch Processing in Financial Services", https://www.databricks.com/blog/design-patterns-batch-processing-financial-services

### 한국 커뮤니티·기업 블로그
- 카카오페이 기술블로그, "Spring Batch 애플리케이션 성능 향상을 위한 주요 팁", https://tech.kakaopay.com/post/spring-batch-performance/
- 우아한형제들 기술블로그, "Spring Batch와 Querydsl", https://techblog.woowahan.com/2662/ (mirror: https://woowabros.github.io/experience/2020/02/05/springbatch-querydsl.html)
- 우아한형제들 기술블로그, "주소검색서버(woowahan-juso) 개발기", https://woowabros.github.io/experience/2018/05/26/woowahan-juso.html
- 우아한형제들 기술블로그, "파일럿 프로젝트를 통한 배치경험기", https://woowabros.github.io/experience/2019/03/31/pilot-batch.html
- jojoldu (이동욱), "spring-batch-querydsl", https://github.com/jojoldu/spring-batch-querydsl
- 마이리얼트립 기술블로그(Medium), 정휘준, "Spring Batch, 처음부터 시작하기", https://medium.com/myrealtrip-product/spring-batch-%EC%B2%98%EC%9D%8C%EB%B6%80%ED%84%B0-%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0-3c6a5db0646d
- SK devocean, "[SpringBatch 연재 02] SpringBatch 코드 설명 및 아키텍처 알아보기", https://devocean.sk.com/blog/techBoardDetail.do?ID=166690&boardType=techBlog
- velog 다수: "Spring Batch", "스프링 배치란?", "Spring Batch 5.x ~ 사용해보기", "Spring Batch 삽질기" 시리즈 (개별 URL은 본문 인용처 참고)
- OKKY Q&A, 스프링 배치 질문 모음:
  - "스프링 배치(Spring Batch) 에 대한 질문 드립니다", https://okky.kr/questions/684140
  - "spring batch OOM 관련 질문", https://okky.kr/questions/1489911
  - "Spring Batch 사용시 @StepScope 주의사항", https://okky.kr/articles/380648
  - "spring batch에 대하여 질문이있습니다", https://okky.kr/questions/1491943
  - "스프링 배치 관련하여 질문드립니다", https://okky.kr/article/850501
  - "SPRING BATCH 2번 돌때;;", https://okky.kr/questions/268704
- 토리맘의 한글라이즈 프로젝트(Spring Batch 한글 가이드), https://godekdls.github.io/Spring%20Batch/configuringastep/

### 학술·논문류
- arxiv 2511.03393, "Formalizing ETLT and ELTL Design Patterns and Proposing Enhanced Variants" (2025), https://arxiv.org/html/2511.03393v1
- arxiv 2503.16079, "Efficient Data Ingestion in Cloud-based architecture: a Data Engineering Design Pattern Proposal" (2025), https://arxiv.org/html/2503.16079v1
- arxiv 2505.04717, "Big Data Architecture for Large Organizations" (2025), https://arxiv.org/html/2505.04717v1
- ResearchGate, "Real-Time Data Processing Versus Batch Processing in Modern Cloud ETL" (2025), https://www.researchgate.net/publication/399084943
- ResearchGate, "Batch to Real-Time: Leveraging AI for Streaming ETL Pipelines" (2025), https://www.researchgate.net/publication/392770477
- Springer, Journal of Cloud Computing, "An efficient hybrid optimization of ETL process in data warehouse of cloud architecture" (2023), https://link.springer.com/article/10.1186/s13677-023-00571-y
- WJAETS 2025-0199, "Optimizing event-driven architectures for real-time financial systems", https://wjaets.com/sites/default/files/fulltext_pdf/WJAETS-2025-0199.pdf
- IJCSP 2022 1305, "Distributed ETL Architecture for Processing", https://rjpn.org/ijcspub/papers/IJCSP22C1305.pdf

### 비교·생태계
- SaaSHub, "Apache Airflow VS Spring Batch", https://www.saashub.com/compare-airflow-vs-spring-batch
- StackShare, "50 Alternatives to Spring Batch", https://stackshare.io/spring-batch/alternatives
- Hevo, "Top 11 Airflow Alternatives", https://hevodata.com/learn/airflow-alternatives/

---

## 11. 리서치 한계 (커버하지 못한 영역)

이 책을 쓰면서 추가 보완이 필요할 수 있는 영역들. 정직하게 적어둔다.

1. **Spring Batch Admin / 운영 UI:** 공식 Spring Batch Admin은 더 이상 활발히 유지되지 않으며, 후속으로 Spring Cloud Data Flow가 위치를 이어받았다. 책에서 "운영 UI" 챕터를 쓸 때 SCDF 또는 자체 만든 대시보드(Actuator + Prometheus + Grafana)의 비중을 어떻게 둘지에 대한 1차 자료가 얕다. 추가 리서치 필요: SCDF의 batch monitoring 화면, 사례.
2. **Reddit r/java / r/SpringBoot의 1차 스레드:** 메타 검색만 했고 개별 스레드 본문까지 들어가지는 못했다. 챕터 도입부 "현장의 목소리" 인용을 더 살리려면 개별 스레드 직인용 1–2개씩이 더 있으면 좋다.
3. **GitHub Discussions:** spring-projects/spring-batch의 discussion #4664(파티셔닝 grid size), #4532(STARTED 박제 복구) 정도만 표면 확인. 마이그레이션 직후의 실 사용자 후기(2026 상반기 제보)는 시간상 더 모일 여지가 있다.
4. **arxiv·DOI 1차 인용 깊이:** ETL/배치 관련 논문 4–5편은 abstract/요약 수준만 확인. "이 책의 어느 챕터에서 정확히 어떤 주장의 출처로 쓸지"가 정해지면 본문 1차 정독이 추가로 필요.
5. **Spring Batch 6 + Boot 4 통합 사례:** Boot 4가 GA된 직후라 실 production 사용기는 아직 적다. 책 출간 시점까지 누적되는 사례를 follow up해야 한다.
6. **JFR 이벤트 운영 사례:** 6.0 신기능이라 실 운영 활용 글이 거의 없다. 6.0.x 마이너가 더 나오면 보완 필요.
7. **MongoDB JobRepository 운영 후기:** 5.2부터 도입되었으나, 한국·영문 모두 production 후기가 드물다. 학습용 예제 위주.
8. **vs Quartz / Spring Cloud Task의 결정 트리:** 가볍게만 다룸. 책의 "다른 도구 비교" 박스에서는 표 형식으로 정돈하는 게 좋겠다.
