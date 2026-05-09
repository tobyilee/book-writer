# 3장. 첫 번째 잡 만들기 — 그리고 @StepScope 함정

OKKY를 배회하다 보면 Spring Batch 입문자들의 질문이 두 묶음으로 모여 있는 게 보인다. 한 묶음은 이런 식이다.

> "스프링 배치 시작했는데 매번 부팅할 때마다 잡이 한 번 더 돌아요. 코드에선 한 번만 호출하고 있는데 이상하네요."

다른 한 묶음은 이렇다.

> "@StepScope 안 붙였더니 NPE가 떠요. 분명 jobParameters['date']로 주입한다고 적어놨는데 BeanCreationException이 뜨면서 안 됩니다."

이 두 가지가 한국 Spring Batch 입문자가 1번으로 부딪히는 함정이다. 첫 번째는 Spring Boot 자동 실행과 수동 트리거가 충돌하는 문제고, 두 번째는 `@StepScope`/`@JobScope`의 늦은 빈 생성을 모르고 쓰는 문제다. 이 둘 다 코드는 멀쩡해 보이는데 동작이 이상해서 한 시간씩 디버깅하다가 결국 검색해서야 답을 찾는 종류다.

이번 장에서는 첫 번째 잡을 손으로 짜보면서 이 두 함정을 정면으로 통과한다. 코드가 한 번에 잘 돌게 만드는 게 목적이 아니다. **함정에 한 번 빠져보고, 왜 그렇게 동작하는지 이해하고, 그 다음에 표준 방식으로 다시 짜본다.** 그래야 나중에 다른 잡을 만들 때 같은 함정에 두 번 빠지지 않는다.

## 프로젝트 만들기 — Spring Initializr부터

가장 작은 프로젝트부터 시작하자. Spring Initializr(start.spring.io)에서 다음과 같이 골라본다.

- **Project:** Maven
- **Language:** Java
- **Spring Boot:** 3.5.x 또는 4.0.x (Spring Batch 6은 Boot 4와 가장 정합이 좋지만, 본문 시점에 Boot 4가 GA된 직후라면 3.5도 충분히 동작한다)
- **Java:** 17 이상 (Spring Batch 6의 baseline)
- **Dependencies:** Spring Batch, JDBC API, H2 Database, Lombok (선택)

H2를 쓰는 이유는 명확하다. JobRepository가 메타데이터를 쓸 곳이 필요한데, 첫 실험에서 production DB를 붙이는 건 무겁다. H2 인메모리 또는 파일 모드로 시작하자. 어차피 메타데이터 스키마는 똑같다.

`pom.xml`에 들어간 핵심 의존성은 이 정도다.

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-batch</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-jdbc</artifactId>
    </dependency>
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>runtime</scope>
    </dependency>
</dependencies>
```

Spring Boot가 알아서 Spring Batch starter를 끌어오므로 버전을 직접 명시하지 않아도 된다. Spring Boot 4.0이면 Spring Batch 6.0이 자동으로 묶여 들어온다.

## application.yml — JobRepository를 위한 자리

`src/main/resources/application.yml`에 다음을 적어보자.

```yaml
spring:
  datasource:
    url: jdbc:h2:file:./build/h2/batch
    username: sa
    password:
    driver-class-name: org.h2.Driver
  batch:
    jdbc:
      initialize-schema: always
    job:
      enabled: false
```

세 줄이 핵심이다.

`spring.datasource.url`은 H2 파일 모드를 쓰는 설정이다. 인메모리(`mem:`)를 써도 되지만 파일 모드면 잡 실행 후에 H2 콘솔로 BATCH_ 테이블을 직접 들여다볼 수 있어서 학습용으로 좋다.

`spring.batch.jdbc.initialize-schema: always`는 Spring Batch 메타데이터 테이블(BATCH_JOB_INSTANCE 등)을 자동으로 생성한다. production이라면 `never`로 두고 Flyway/Liquibase로 관리하는 게 정석이지만, 첫 실험엔 `always`가 편하다.

그리고 마지막 줄, **`spring.batch.job.enabled: false`**. 이게 중요하다. 이 한 줄이 한국 입문자 1번 함정의 절반을 막는다. 왜 그런지를 다음 절에서 짚자.

## 함정 1 — 잡이 두 번 도는 현상

먼저 가장 작은 잡 하나를 짜보자. "1부터 100까지 숫자를 콘솔에 출력"하는 잡이다.

```java
@Configuration
public class HelloJobConfig {

    @Bean
    public Job helloJob(JobRepository jobRepository, Step printStep) {
        return new JobBuilder("helloJob", jobRepository)
                .start(printStep)
                .build();
    }

    @Bean
    public Step printStep(JobRepository jobRepository,
                          PlatformTransactionManager txManager,
                          ItemReader<Integer> reader,
                          ItemWriter<Integer> writer) {
        return new StepBuilder("printStep", jobRepository)
                .<Integer, Integer>chunk(10, txManager)
                .reader(reader)
                .writer(writer)
                .build();
    }

    @Bean
    public ItemReader<Integer> numberReader() {
        return new ListItemReader<>(IntStream.rangeClosed(1, 100).boxed().toList());
    }

    @Bean
    public ItemWriter<Integer> consoleWriter() {
        return chunk -> chunk.forEach(n -> System.out.println("number = " + n));
    }
}
```

`ListItemReader`는 Spring Batch가 제공하는 가장 단순한 Reader다. 메모리에 있는 List를 그대로 한 건씩 내보낸다. 학습용으로 적당하다.

이 잡을 그냥 실행하면 어떻게 될까? 한번 직접 돌려보자. `spring.batch.job.enabled` 설정을 빼고, 즉 `application.yml`에서 그 줄을 지우고 돌려본다.

실행하면 콘솔에 1부터 100까지가 한 번 찍힌다. 자, 이제 다시 실행해보자.

같은 결과가 다시 한 번 찍히는가? 아닐 것이다. 이런 메시지가 뜬다.

```
A job instance already exists and is complete for parameters={...}.
If you want to run this job again, change the parameters.
```

같은 JobInstance가 이미 끝났다는 거부 메시지다. 2장에서 짚었던 JobInstance 동일성 검사가 여기서 작동한다.

그런데 여기서 더 큰 문제가 있다. 우리가 명시적으로 잡을 시작하는 코드를 어디에도 안 짰는데, 잡이 알아서 한 번 돌았다. 누가 시작시켰는가?

**Spring Boot가 시작시켰다.** Spring Boot의 `BatchAutoConfiguration`이 컨텍스트에 등록된 Job 빈을 감지하면, 부팅 시점에 자동으로 한 번 실행한다. `JobLauncherApplicationRunner`라는 컴포넌트가 그 일을 한다.

이게 처음엔 편해 보인다. 잡을 따로 트리거할 필요가 없으니까. 그런데 운영 환경에 가면 골치가 된다. CronJob이 시간 맞춰 트리거하려고 하는데, 컨테이너가 부팅하면서 자동으로 한 번 돌아버리면 같은 잡이 두 번 돌게 된다. 또는 CronJob 트리거를 받기 위해 Pod이 idle 상태로 떠 있어야 하는데, 부팅 시 잡이 자동으로 돌아 끝나면 Pod이 종료된다.

해결책은 두 갈래다.

- **자동 실행을 끈다:** `spring.batch.job.enabled: false`로 두고, 잡 시작은 명시적으로 트리거한다. CronJob 패턴에 어울린다.
- **자동 실행을 쓰되 한 잡만 지정한다:** `spring.batch.job.name=helloJob`처럼 이름을 박아두면 그 잡만 자동 실행한다. 컨텍스트에 잡이 여러 개 있을 때 실수를 막는 안전장치다.

학습 단계에서는 `spring.batch.job.enabled: false`로 두는 게 깔끔하다. 그리고 잡을 명시적으로 시작하려면 다음과 같은 `CommandLineRunner`를 쓴다.

```java
@Component
@RequiredArgsConstructor
public class HelloJobLauncher implements CommandLineRunner {

    private final JobOperator jobOperator;
    private final Job helloJob;

    @Override
    public void run(String... args) throws Exception {
        JobParameters params = new JobParametersBuilder()
                .addLocalDateTime("startedAt", LocalDateTime.now())
                .toJobParameters();
        jobOperator.start(helloJob, params);
    }
}
```

여기서 두 가지가 한꺼번에 등장한다. 첫째, 2장에서 본 **`JobOperator`가 잡을 시작하는 진입점**으로 등장한다. Spring Batch 6에서는 이 한 줄이 잡 시작의 표준이다. 둘째, **JobParameters에 `startedAt` 시각을 박아 둔다.** 매 실행마다 다른 시각이 들어가니, 매 실행이 다른 JobInstance가 된다. "이미 끝났다"는 거부 메시지를 안 받게 된다.

이걸 빼먹고 파라미터 없이 매번 돌리면 두 번째 실행부터 거부당한다. JobInstance 동일성을 만들어주는 식별 파라미터가 필요한 것이다.

## @EnableBatchProcessing을 붙이지 말자

여기서 또 하나 짚자. 한국 자료들을 보면 메인 클래스나 설정 클래스에 `@EnableBatchProcessing`을 붙이는 예제가 흔하다. 5.x 이전 자료들이 그렇다. **Spring Boot 3 이상에서는 이걸 직접 붙이는 것이 권장되지 않는다.** Spring Boot의 `BatchAutoConfiguration`이 자동으로 구성하는데, 우리가 `@EnableBatchProcessing`을 붙이면 자동 구성이 꺼져버린다. 직접 모든 빈을 등록해야 하는 상황이 된다.

Spring Batch 6에서는 한 발 더 나아가 `@EnableBatchProcessing`이 두 갈래로 갈라졌다. JDBC 저장소가 필요하면 `@EnableJdbcJobRepository`, MongoDB 저장소가 필요하면 `@EnableMongoJobRepository`를 쓴다. 그리고 Spring Boot가 알아서 둘 중 하나를 골라 자동 구성한다. 우리가 직접 붙일 일은 거의 없다.

기억해두자. **Spring Boot 환경에서는 `@EnableBatchProcessing`을 그냥 쓰지 마라.** 자동 구성에 맡기는 게 정답이다.

## 메타데이터 테이블 들여다보기

잡을 한 번 돌리고 나면, 우리가 2장에서 그림으로 봤던 메타데이터 테이블들이 실제로 어떤 모양인지 직접 확인해볼 수 있다. H2 콘솔(`http://localhost:8080/h2-console`)을 열어 들어가 보자. URL을 `jdbc:h2:file:./build/h2/batch`로 맞추고, 사용자명 `sa`, 비밀번호 빈 칸으로 접속한다.

들어가면 BATCH_로 시작하는 테이블이 여러 개 보인다. 우리가 자주 들여다볼 것은 다음 셋이다.

- `BATCH_JOB_INSTANCE`: 잡 인스턴스. 잡 이름과 식별 파라미터의 해시.
- `BATCH_JOB_EXECUTION`: 잡 실행. 시작·종료 시각, 상태(COMPLETED/FAILED/STARTED).
- `BATCH_STEP_EXECUTION`: 스텝 실행. 우리가 가장 자주 보게 될 표.

`BATCH_STEP_EXECUTION`을 SELECT 해보면 흥미롭다.

```sql
SELECT step_name, status, commit_count, read_count, write_count, rollback_count
FROM BATCH_STEP_EXECUTION;
```

```
STEP_NAME   | STATUS    | COMMIT_COUNT | READ_COUNT | WRITE_COUNT | ROLLBACK_COUNT
printStep   | COMPLETED |           11 |        100 |         100 |              0
```

`commit_count`가 11이다. 청크 사이즈 10으로 100건을 처리했으니, 청크 10개 + 마지막 비어 있는 청크 1개 = 11번의 커밋이다. 이 한 줄이 우리가 1장에서 직접 짤 때 `step_log` 테이블에 기록하려고 했던 그 정보다. 그게 표준 자리에 자동으로 들어와 있다.

운영 환경에서는 이 표가 잡의 health를 들여다보는 1번 자료가 된다. `commit_count`/`rollback_count` 비율, `read_count`/`write_count` 차이(필터링된 항목 수), `skip_count` 추세 — 이런 게 잡이 정상인지를 말해준다. 12장에서 다시 다룰 운영 감각의 시작점이다.

## JobParameters 더 깊게 — 식별 vs 비식별

JobParameters에는 한 가지 미묘한 구분이 있다. **identifying** 플래그다. 같은 잡이라도 어떤 파라미터는 인스턴스를 식별하는 데 쓰이고, 어떤 파라미터는 그냥 정보로만 쓰인다.

예를 들어 정산 잡이 있다고 해보자. `date=2026-05-08`은 인스턴스를 식별한다(이건 5월 8일 정산이다). 그런데 `dryRun=true`라는 파라미터는 인스턴스 식별과 무관하다(같은 5월 8일 정산을 dry run으로 한 번, 실제로 한 번 돌리고 싶은 경우).

```java
JobParameters params = new JobParametersBuilder()
        .addString("date", "2026-05-08", true)        // 식별
        .addString("dryRun", "true", false)           // 비식별
        .toJobParameters();
```

세 번째 인자가 `identifying` 플래그다. `true`면 인스턴스 식별에 쓰인다. 기본값은 `true`이므로, 명시하지 않은 파라미터는 다 식별 파라미터다.

Spring Batch 6에서는 `JobParameter`가 record 타입으로 바뀌었고, `JobParameters`도 `Set<JobParameter>` 기반으로 재설계됐다. 사용자 입장에서 큰 차이는 없다 — `JobParametersBuilder`로 빌드하면 내부에서 알아서 처리해준다. 다만 5.x에서 ExecutionContext에 `JobParameters` 객체를 직접 직렬화해서 저장한 코드가 있다면, 6에서 그 직렬화가 깨질 수 있다. 마이그레이션 시 주의할 점이다 — 11장에서 자세히 짚는다.

## 함정 2 — @StepScope의 늦은 빈 생성

이제 진짜 까다로운 함정으로 들어가자. `@StepScope`의 늦은 빈 생성 문제는 한국 입문자가 가장 자주 막히는 지점이고, 한 번에 이해되기도 어렵다. 천천히 풀어보자.

상황 가정. 우리가 정산 잡을 짠다. 매일 다른 날짜에 대해 도는 잡이다. 그래서 JobParameters에 `date=2026-05-08`을 넣어 시작한다. Reader가 그 날짜의 데이터만 읽어야 한다. 즉 Reader는 JobParameters의 `date` 값을 알아야 한다.

자연스럽게 이렇게 짜본다.

```java
@Bean
public ItemReader<Settlement> settlementReader(
        @Value("#{jobParameters['date']}") String date,
        DataSource dataSource) {
    return new JdbcCursorItemReaderBuilder<Settlement>()
            .name("settlementReader")
            .dataSource(dataSource)
            .sql("SELECT * FROM payments WHERE settle_date = ?")
            .preparedStatementSetter((ps, ctx) -> ps.setString(1, date))
            .rowMapper(...)
            .build();
}
```

`@Value("#{jobParameters['date']}")` SpEL 표현식으로 JobParameters에서 `date` 값을 꺼내려는 의도다. 그럴듯해 보인다. 그런데 실행하면 BeanCreationException이 뜬다. 이렇게 시작하는 메시지가 뜬다.

```
Cannot resolve reference to bean 'jobParameters' while setting bean property
...
Field or property 'jobParameters' cannot be found on object of type
'org.springframework.beans.factory.config.BeanExpressionContext'
```

왜 이럴까? **빈이 만들어지는 시점에 `jobParameters`가 없기 때문이다.**

Spring 컨테이너는 부팅할 때 모든 싱글턴 빈을 한꺼번에 만든다. 그 시점에 `jobParameters`가 어디 있는가? 없다. 잡은 아직 시작되지도 않았다. JobParameters는 잡을 시작할 때(`jobOperator.start(job, params)`) 비로소 생긴다. 그러니 컨테이너가 부팅할 때 `@Value("#{jobParameters['date']}")`를 평가하려고 하면, 그 시점에 `jobParameters`라는 객체가 컨텍스트에 없어서 실패하는 것이다.

이걸 어떻게 해결하는가? **빈 생성을 잡 시작 이후로 미뤄야 한다.** 정확히 그 일을 하는 게 `@StepScope`다.

```java
@Bean
@StepScope
public ItemReader<Settlement> settlementReader(
        @Value("#{jobParameters['date']}") String date,
        DataSource dataSource) {
    // ...
}
```

`@StepScope`를 붙이면 이 빈은 **Step이 시작되는 시점에 비로소 생성**된다. Step이 시작되는 시점에는 JobParameters가 이미 존재하므로, `@Value("#{jobParameters['date']}")`가 정상적으로 평가된다.

이 메커니즘을 SpEL late binding이라고 부른다. **빈의 정의는 컨테이너 부팅 시 등록되지만, 빈의 생성은 잡 실행 시점으로 미뤄진다**는 뜻이다. 빈 정의에 박힌 `@Value` 표현식도 그때 비로소 evaluate된다.

`@JobScope`도 비슷하다. `@StepScope`는 매 Step마다 다시 생성되고, `@JobScope`는 매 Job마다 다시 생성된다. JobParameters는 잡 단위로 정해지므로 Job 안에서는 `@StepScope`나 `@JobScope`나 둘 다 작동한다. 일반적으로는 더 짧은 생명주기인 `@StepScope`를 쓰는 것이 권장된다.

## @StepScope의 또 다른 함정 — 클래스 프록시

`@StepScope`를 쓸 때 생기는 두 번째 함정이 있다. 이건 더 미묘하다.

`@StepScope`의 동작 방식은 사실 **프록시**다. 컨테이너 시작 시점에는 진짜 빈이 아니라 프록시 객체가 등록되고, 그 프록시가 Step 시작 시점에 진짜 빈을 만들어 호출을 위임한다. 이 프록시가 어떻게 만들어지냐가 문제가 된다.

Spring은 프록시를 두 가지 방식으로 만들 수 있다.

- **JDK 동적 프록시 (인터페이스 기반):** 빈이 인터페이스를 구현하면 그 인터페이스에 대한 프록시를 만든다.
- **CGLIB 프록시 (클래스 기반):** 인터페이스가 없으면 클래스 자체를 상속받는 프록시를 만든다.

`@StepScope`는 기본적으로 CGLIB 프록시를 쓴다. 이게 왜 함정이냐면, 우리의 빈 메서드 반환 타입이 인터페이스인 경우에 미묘한 충돌이 생길 수 있기 때문이다.

예를 들어 위의 `settlementReader`는 반환 타입이 `ItemReader<Settlement>`라는 **인터페이스**다. 그런데 실제 구현체는 `JdbcCursorItemReader`라는 클래스다. 이 경우 `@StepScope`가 만드는 프록시가 인터페이스 기반인지 클래스 기반인지에 따라 동작이 달라질 수 있다.

대부분의 경우는 자동으로 잘 동작한다. 그런데 특정 라이브러리나 특수한 패턴을 쓸 때 "프록시가 클래스를 상속받지 못해서 빈 등록이 실패"하거나 "인터페이스 메서드는 보이는데 구체 클래스 메서드는 안 보이는" 문제가 생길 수 있다. 이런 증상이 나타나면 다음 두 가지를 의심한다.

- 반환 타입을 더 구체적인 클래스로 바꾼다 (`ItemReader<Settlement>` → `JdbcCursorItemReader<Settlement>`).
- `@StepScope` 옵션을 명시적으로 조정한다 (`@StepScope(proxyMode = ScopedProxyMode.TARGET_CLASS)`).

이 함정은 실무에서 가끔 마주친다. 미리 알아두면 한 시간을 아낄 수 있다. 잊지 말자.

## 첫 잡에 @StepScope 적용해보기

이제 함정을 알았으니, 첫 잡을 JobParameters와 `@StepScope`를 써서 다시 짜보자. "1부터 N까지 출력"이라는 잡으로 만들되, N을 JobParameters에서 받는다.

```java
@Configuration
public class ParamHelloJobConfig {

    @Bean
    public Job paramHelloJob(JobRepository jobRepository, Step paramPrintStep) {
        return new JobBuilder("paramHelloJob", jobRepository)
                .start(paramPrintStep)
                .build();
    }

    @Bean
    public Step paramPrintStep(JobRepository jobRepository,
                               PlatformTransactionManager txManager,
                               ItemReader<Integer> rangeReader,
                               ItemWriter<Integer> consoleWriter) {
        return new StepBuilder("paramPrintStep", jobRepository)
                .<Integer, Integer>chunk(10, txManager)
                .reader(rangeReader)
                .writer(consoleWriter)
                .build();
    }

    @Bean
    @StepScope
    public ItemReader<Integer> rangeReader(
            @Value("#{jobParameters['endNumber']}") Long endNumber) {
        long end = (endNumber != null) ? endNumber : 10L;
        return new ListItemReader<>(
                LongStream.rangeClosed(1, end).boxed()
                        .map(Long::intValue)
                        .toList());
    }

    @Bean
    public ItemWriter<Integer> consoleWriter() {
        return chunk -> chunk.forEach(n -> System.out.println("n = " + n));
    }
}
```

여기서 `rangeReader`만 `@StepScope`다. `consoleWriter`는 JobParameters를 받지 않으니 굳이 `@StepScope`를 붙일 필요가 없다. 싱글턴으로 두면 된다. **`@StepScope`는 필요한 자리에만 붙인다**가 원칙이다. 다 붙이면 매번 새 인스턴스가 만들어져서 불필요한 비용이 생긴다.

이 잡을 시작할 때 `endNumber=50`을 넣어주면 1부터 50까지가 찍힌다. `endNumber=200`을 넣어주면 1부터 200까지가 찍힌다. 같은 Job 정의가 다른 JobInstance로 다르게 동작하는 모습이다.

```java
JobParameters params = new JobParametersBuilder()
        .addLong("endNumber", 50L)
        .addLocalDateTime("startedAt", LocalDateTime.now())
        .toJobParameters();
jobOperator.start(paramHelloJob, params);
```

`startedAt`을 같이 넣은 이유는 매번 다른 JobInstance를 만들기 위해서다. `endNumber=50` 한 가지 파라미터만 넣으면, 같은 50으로 두 번 돌릴 때 두 번째가 거부당한다.

## 빈 생성 시점의 그림

이쯤에서 시간 축으로 정리해보자. `@StepScope`가 어떻게 동작하는지를 시간 순으로 그려보면 머릿속에 박힌다.

```
T0  Spring Boot 부팅
     │
     │  컨테이너에 모든 빈 등록
     │  - paramHelloJob 빈 등록 (Job)
     │  - paramPrintStep 빈 등록 (Step)
     │  - consoleWriter 빈 등록 (Writer, 싱글턴 인스턴스 생성)
     │  - rangeReader 빈 등록 (Reader, 프록시 객체만 생성, 진짜 인스턴스 X)
     │
T1  CommandLineRunner 실행
     │
     │  jobOperator.start(paramHelloJob, params) 호출
     │  - JobParameters를 컨텍스트에 등록
     │
T2  Job 시작
     │
     │  paramPrintStep 시작
     │  - StepContext 생성, JobParameters 접근 가능
     │  - rangeReader 프록시가 호출되면서 진짜 인스턴스 생성
     │  - @Value("#{jobParameters['endNumber']}") 평가 → 50 주입 성공
     │
T3  Step 종료
     │
     │  rangeReader 인스턴스 폐기
     │
T4  Job 종료
```

T0의 시점에 `@Value("#{jobParameters['endNumber']}")`를 평가하려고 하면 `jobParameters`가 컨텍스트에 없어서 실패한다 — 그게 함정 2의 근원이다. `@StepScope`를 붙이면 이 평가 시점이 T2로 미뤄진다. 그러면 잡은 무사히 돈다.

이 시간 축이 머릿속에 들어오면 `@StepScope` 함정은 더 이상 함정이 아니다. 그냥 "빈이 언제 만들어지는가"라는 자연스러운 질문이 된다.

## 자기 손으로 함정에 빠져보기 (실험)

이 책을 읽다 보면 "함정에 한 번 빠져보라"는 말이 종종 등장할 것이다. 이게 학습에서 가장 효과적인 방법이라고 믿기 때문이다. 책을 읽고 머리로만 안 함정은 6개월 뒤에 실제로 마주치면 못 알아본다. 한 번 빠져본 함정은 평생 알아본다.

여기서도 권하자. 위의 `rangeReader`에서 `@StepScope`를 일부러 빼고 돌려보라. 그러면 컨테이너 부팅 시점에 BeanCreationException이 뜨면서 시작 자체가 실패한다. 에러 메시지를 자세히 읽어보자. "jobParameters를 찾을 수 없다"는 메시지가 어디에 있는지, 어떤 빈에서 그 에러가 났는지를 확인한다.

그 다음에 `@StepScope`를 다시 붙이고 잘 도는 걸 확인한다. 이 실험을 한 번 해보면, 6개월 뒤에 비슷한 에러를 만났을 때 5초 만에 원인을 알아낸다. 시간 투자 대비 효과가 가장 좋은 학습이다.

## 직접 짠 코드 vs Spring Batch 매핑 — 첫 잡 편

여기서 1장과 2장에서 시작한 매핑을 잠시 이어가자. 지금까지 만든 첫 잡에서 우리가 직접 짤 때 어떤 코드를 짰을지를 비교해 보면 이렇다.

| 직접 짤 때 | Spring Batch에서 |
|---|---|
| 잡 시작/종료 시각을 `job_log`에 INSERT | BATCH_JOB_EXECUTION에 자동 기록 |
| 잡 식별을 위한 별도 락 테이블 또는 파일 | JobInstance + JobParameters 식별로 자동 |
| 청크 단위 try-commit 직접 짜기 | StepBuilder의 `.chunk(10, txManager)` 한 줄 |
| 자동 실행 막기 위한 별도 플래그 | `spring.batch.job.enabled: false` |
| 매번 다른 파라미터로 도는 것을 추적 | JobParameters identifying 플래그로 자동 |

100건짜리 작은 잡인데도 직접 짤 때 우리가 신경 써야 했던 부분이 5개나 줄어들었다. 잡이 많아질수록 이 차이는 누적된다. 직접 짠 코드 vs Spring Batch의 진짜 차이는 한 잡이 아니라 10개·100개의 잡을 운영할 때 드러난다.

## 첫 잡을 만들고 나서 — 운영자 시각의 작은 점검

학습용 잡 하나를 만들어 봤으니, 끝내기 전에 운영자 시각으로 작은 점검을 해보자. "이 잡을 진짜 운영에 올리려면 무엇이 더 필요한가?"라는 질문이다.

- **DataSource:** H2가 아니라 production DB로. JobRepository와 비즈니스 데이터를 다른 DB로 분리할지 같은 DB로 둘지 결정이 필요하다 (보통 같은 DB가 트랜잭션 일관성에 유리).
- **스키마 관리:** `initialize-schema: always`가 아니라 Flyway/Liquibase로 명시 관리.
- **트리거:** CommandLineRunner가 아니라 K8s CronJob. 매니페스트에서 JobParameters를 어떻게 넘길지 결정 (10장에서 다룬다).
- **재시작 정책:** 잡이 실패했을 때 그 JobInstance를 어떻게 다시 돌릴지 결정. 6의 `JobOperator#recover()`가 주된 도구가 된다 (7장과 10장에서 다룬다).
- **모니터링:** Micrometer 메트릭을 Prometheus로 publish하고, 알람 임계값을 설계 (9장에서 다룬다).

이 다섯 가지가 production 잡의 표준 체크리스트다. 첫 잡에서는 다 갖추지 않아도 된다. 하지만 머릿속에 "이 다섯이 운영에서 필요하다"는 그림은 두자. 지금부터 만드는 잡들이 결국 다 이 길로 간다.

## 마무리

첫 잡을 만들면서 두 가지 함정을 정면으로 통과했다. 잡이 두 번 도는 현상은 Spring Boot 자동 실행과 명시적 트리거의 충돌이고, `spring.batch.job.enabled: false` + 명시적 `JobOperator.start()`로 해결된다. `@StepScope` NPE는 빈 생성 시점이 컨테이너 부팅 시점이라 JobParameters가 아직 없는 게 원인이고, `@StepScope`를 붙여 빈 생성을 Step 시작 이후로 미루면 해결된다.

이 두 가지를 신체적으로 익혀두면, 앞으로 만들 잡에서 같은 함정에 다시 빠지지 않는다. 시간 축 그림 — "T0 컨테이너 부팅 → T1 잡 시작 → T2 빈 실제 생성" — 이 머릿속에 박혀 있으면, NPE를 만났을 때 5초 만에 `@StepScope`가 빠진 자리를 찾는다.

한 가지가 더 남았다. 청크 모델을 더 깊게 들여다보는 일이다. ItemReader/Processor/Writer 계약을 한 줄씩 쪼개고, chunk size·page size·fetch size의 차이를 그림으로 풀어내고, Cursor vs Paging의 결정 트리를 만들어보자. 그리고 `@StepScope`를 실제 Reader/Writer 매개화에 어떻게 쓰는지 — "왜 붙어야 하는가"는 여기서 알았으니, "어떻게 매개화하는가"를 다음 장에서 직접 손으로 짜본다. 청크가 안 맞는 일에는 tasklet을 어떻게 꺼내드는지도 같이 보자.
