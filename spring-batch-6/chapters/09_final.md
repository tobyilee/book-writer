# 9장. 모니터링과 옵저버빌리티 — Micrometer, JFR, 알람 설계

지난주 새벽에 이런 일이 있었다고 해보자. 야간 정산 잡이 평소엔 50분이면 끝나던 것이, 어느 날 갑자기 2시간을 넘기더니 결국 다음 잡과 시간 창이 겹쳐 알림이 울렸다. 노트북을 켜고 로그를 뒤진다. ERROR는 없다. 처리 건수도 평소와 비슷하다. 그런데 왜 두 배가 걸렸을까?

이런 순간이 운영 1년차에 가장 자주 마주치는 종류의 통증이다. **잡이 죽지는 않았는데 느려졌다.** 죽었으면 차라리 단서가 명확하다. 스택트레이스, 마지막 SQL, 메타 테이블의 FAILED 행. 하지만 "느려졌다"는 신호는 모니터링 체계가 없으면 단서를 남기지 않는다. 그래서 어딘가가 탑승했는지 — 외부 API의 latency가 늘었는지, DB의 인덱스 통계가 어긋났는지, 청크 1개의 commit 시간이 길어졌는지 — 손으로 짚어가며 추적해야 한다.

옵저버빌리티는 이 추적을 사후가 아니라 **상시 가시화**로 만드는 일이다. 잡이 평소에 어떤 모양으로 도는지를 평시에 기록해두면, 어느 날 모양이 변했을 때 변화를 본다. Spring Batch는 6.0 들어 옵저버빌리티 측면에서 한 단계 더 정돈됐다 — Micrometer 메트릭의 등록 방식이 깔끔해졌고, JFR 이벤트가 1급 시민으로 들어왔다. 그 정돈된 모양을 한 번 살펴보고, 거기에 알람 임계값 설계까지 얹어보자.

## 9.1 Spring Boot Actuator + Micrometer — 측정의 기본 골격

먼저 측정의 기본기부터 다지자. Spring Batch는 4.2부터 Micrometer 기반 메트릭을 기본 제공한다. 5.x에서는 트레이싱(Job=trace, Step=span)도 표준이 됐다. 6.0은 이 둘을 그대로 이어받되, 등록 방식 하나를 바꿨다 — 그 한 줄짜리 변경이 의외로 중요하니 잠시 후에 짚는다.

먼저 의존성부터 보자. Spring Boot Starter를 쓰면 Actuator와 Micrometer가 자연스럽게 묶여 들어온다.

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-batch")
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("io.micrometer:micrometer-registry-prometheus")
}
```

`application.yml`에서 actuator endpoint를 노출한다. production에서는 `/actuator/prometheus`만 열어두고 나머지는 닫는 편이 안전하다.

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health, info, prometheus
  endpoint:
    health:
      show-details: when_authorized
  metrics:
    distribution:
      percentiles-histogram:
        spring.batch.job: true
        spring.batch.step: true
        spring.batch.item.read: true
        spring.batch.item.process: true
        spring.batch.chunk.write: true
```

`percentiles-histogram: true`는 처리 시간을 단순 평균이 아니라 히스토그램으로 모은다는 뜻이다. p50/p95/p99를 PromQL로 뽑아낼 수 있는 형태가 되니, 알람 임계값을 잡을 때 결정적으로 유리해진다. 이 한 줄을 빼먹은 채 평균만 보다가는, 평균이 멀쩡한 동안에도 꼬리(tail)가 늘어지는 현상을 놓친다.

### 9.1.1 6.0의 변경: ObservationRegistry를 빈으로 등록해야 한다

여기서 Spring Batch 6에서 의식해야 할 변경 한 가지를 짚자. 5.x까지는 Micrometer의 전역 정적 레지스트리(`Metrics.globalRegistry`)에 자동으로 메트릭이 발행됐다. 그래서 별다른 설정 없이도 메트릭이 뽑혀 나왔다. 6.0은 이 전역 레지스트리 의존을 폐기했다. 대신 **`ObservationRegistry` 빈을 컨텍스트에 등록**해야 메트릭이 수집된다.

Spring Boot Actuator를 쓰고 있다면 이 빈은 자동으로 만들어진다. 그러니 starter를 정상적으로 의존성에 넣고 actuator를 켰다면 따로 코드를 쓸 필요는 없다. 다만 actuator를 안 쓰고 Micrometer만 직접 깔아쓰는 환경, 또는 5.x에서 6.0으로 올리고 나서 "왜 메트릭이 안 보이지?" 하고 의아해할 때 — 그 답은 거의 늘 이 빈 등록이다.

수동으로 등록하려면 이렇게 한다.

```java
@Configuration
public class ObservabilityConfig {

    @Bean
    ObservationRegistry observationRegistry(MeterRegistry meterRegistry) {
        ObservationRegistry registry = ObservationRegistry.create();
        registry.observationConfig()
            .observationHandler(new DefaultMeterObservationHandler(meterRegistry));
        return registry;
    }
}
```

5에서 6으로 마이그레이션을 한 직후, **메트릭이 갑자기 비어 보이면 가장 먼저 의심할 자리가 여기**다. 11장에서 다시 한 번 짚을 자리이기도 하다.

### 9.1.2 어떤 메트릭이 기본으로 나오는가

Spring Batch가 기본 발행하는 메트릭의 prefix는 `spring.batch.`다. 한눈에 보자.

| 메트릭 이름 | 종류 | 의미 |
|---|---|---|
| `spring.batch.job` | timer | 잡 1회 실행 시간 |
| `spring.batch.job.active` | gauge | 현재 실행 중인 잡 수 |
| `spring.batch.step` | timer | 스텝 1회 실행 시간 |
| `spring.batch.step.active` | gauge | 현재 실행 중인 스텝 수 |
| `spring.batch.item.read` | timer | item 읽기 1건 소요 시간 |
| `spring.batch.item.process` | timer | item 변환 1건 소요 시간 |
| `spring.batch.chunk.write` | timer | 청크 1개 쓰기 시간 |

태그(label)는 잡 이름, 스텝 이름, 상태(`COMPLETED`/`FAILED`)로 붙는다. 그래서 PromQL에서 `spring_batch_job_seconds_count{name="settlementJob",status="COMPLETED"}` 같은 식으로 잡별 성공·실패를 분리해 본다.

여기서 잠깐. timer 메트릭은 Prometheus로 노출될 때 `_count` / `_sum` / `_bucket` 세 시리즈로 나뉜다. `_count`는 발생 횟수, `_sum`은 누적 시간, `_bucket`은 히스토그램 버킷이다. PromQL `rate(spring_batch_chunk_write_seconds_count[5m])`는 "최근 5분간 청크 쓰기 처리율(초당 건수)"이다. 이 패턴 하나만 익혀두면 알람 임계값의 절반은 풀린다.

### 9.1.3 트레이싱 모델 — Job=trace, Step=span

Micrometer의 트레이싱 면에서 Spring Batch는 **잡 = trace, 스텝 = span**이라는 단순한 매핑을 따른다. 잡 하나가 시작부터 끝까지 trace 하나로 묶이고, 그 안의 각 스텝이 자식 span으로 잡힌다. Zipkin이나 Jaeger, Tempo 같은 trace 백엔드에 보내면 잡 하나의 라이프사이클이 시각적으로 한 줄에 늘어선다.

이 모델이 빛을 발하는 자리는 "어느 스텝이 느렸는가"를 한눈에 볼 때다. 정산 잡이 read → enrich → settle → notify 4 스텝으로 구성돼 있고, 어느 날 어느 스텝이 길어졌는지 궁금하다고 해보자. trace 한 줄을 펼치면 각 span의 길이가 시각적으로 비교된다. 메트릭의 평균 그래프로는 보이지 않던 "특정 잡 인스턴스에서만 enrich가 길어진다" 같은 패턴이 잡힌다.

트레이싱 백엔드 연동은 `micrometer-tracing-bridge-otel` + OpenTelemetry exporter 조합이 가장 무난하다. 다만 trace 양이 많으면 sampling 정책을 명확히 해야 한다 — 모든 잡을 100% 샘플링하면 백엔드가 비명을 지른다. 운영에서는 5~10% 샘플링 + 실패 잡은 100% 샘플링이 흔한 출발점이다.

## 9.2 Prometheus + Grafana — 한 화면에 잡의 health를 본다

메트릭이 발행되더라도 그것을 사람의 눈이 한 화면에서 알아볼 수 있게 만들지 않으면 무의미하다. Prometheus + Grafana 조합이 사실상 표준이다. 다른 백엔드가 더 나은 자리도 있지만, Spring Boot 생태계와 가장 마찰이 적고 자료가 풍부한 조합은 이 둘이다.

### 9.2.1 Prometheus 스크레이프 설정

Spring Boot 앱이 `/actuator/prometheus`로 메트릭을 노출하면 Prometheus는 그것을 주기적으로 긁어간다(scrape). K8s에서는 `ServiceMonitor`(prometheus-operator) 또는 Pod annotation 패턴을 쓴다. 단발성으로 도는 배치 잡이라면 한 가지 함정이 있다 — **잡이 끝나서 Pod이 사라지면 메트릭이 누락된다**. Prometheus 스크레이프 주기보다 잡 수명이 짧으면 당연히 그렇다.

이 문제를 푸는 표준 방식은 **Pushgateway**다. 잡이 끝나기 직전에 누적된 메트릭을 Pushgateway로 push하고, Prometheus는 Pushgateway를 스크레이프한다. Spring Boot Actuator는 `micrometer-registry-prometheus`에 simpleclient pushgateway를 곁들이면 된다.

```java
@Configuration
public class PushgatewayConfig {

    @Bean
    PrometheusPushGatewayManager pushGatewayManager(
            PrometheusMeterRegistry registry,
            @Value("${prometheus.pushgateway.url}") String url,
            @Value("${spring.application.name}") String jobName) {
        PushGateway pushGateway = new PushGateway(url);
        return new PrometheusPushGatewayManager(
            pushGateway,
            registry.getPrometheusRegistry(),
            jobName,
            Map.of("instance", InetAddress.getLocalHost().getHostName()),
            Duration.ofSeconds(10),
            ShutdownOperation.PUSH
        );
    }
}
```

`ShutdownOperation.PUSH`가 핵심이다. JVM 종료 직전에 한 번 더 push해 마지막 메트릭이 누락되지 않게 만든다. 10장의 graceful shutdown과 결을 같이 하는 설정이다.

### 9.2.2 Grafana 대시보드 — 5개 패널이면 충분하다

Grafana 대시보드는 화려하게 만들 수도 있고, 핵심만 추릴 수도 있다. 운영 1년차에는 화려한 대시보드보다 **5개 패널짜리 간결한 대시보드가 훨씬 자주 쓰인다**. 다음을 권한다.

1. **잡별 처리 시간(p50/p95/p99)** — 평소 모양을 본다
2. **잡별 성공률 (최근 24시간)** — 단순한 비율, 알람의 1차 출처
3. **스텝별 chunk write 처리율** — 어느 스텝이 병목인지
4. **skip / retry 누적 카운터** — 추세선
5. **현재 실행 중인 잡 (gauge)** — 동시에 도는지, 박제됐는지

각 패널의 PromQL을 하나씩 짚어보자.

**잡 처리 시간 p95:**
```promql
histogram_quantile(0.95,
  sum by (le, name) (
    rate(spring_batch_job_seconds_bucket{status="COMPLETED"}[5m])
  )
)
```

**잡 성공률 (최근 1시간):**
```promql
sum by (name) (rate(spring_batch_job_seconds_count{status="COMPLETED"}[1h]))
/
sum by (name) (rate(spring_batch_job_seconds_count[1h]))
```

**chunk write 처리율 (스텝별):**
```promql
sum by (job_name, step_name) (
  rate(spring_batch_chunk_write_seconds_count[5m])
)
```

이 세 개의 PromQL이면 `5개 패널` 대시보드의 절반이 그려진다. 나머지는 단순 카운터 누적과 gauge라서 표현이 더 간단하다. 처음부터 모든 메트릭을 패널화하려 하지 말자 — 운영이 익으면서 진짜로 필요한 것만 천천히 늘려가는 편이 낫다.

## 9.3 JFR — 트랜잭션 경계까지 잡히는 저수준 가시성

Micrometer 메트릭이 "잡의 모양"을 보여준다면, JFR(Java Flight Recorder)은 "잡의 살결"을 보여준다. 6.0에서 Spring Batch는 자체 JFR 이벤트를 발행한다. job/step/item read·write/transaction 경계가 모두 이벤트로 남는다.

JFR의 이점은 두 가지다. 첫째, 오버헤드가 매우 낮다 — 공식 문서가 "minimal"이라 표현할 정도다. production에서 항상 켜둘 수 있다는 뜻이다. 둘째, JDK가 기본으로 내장하니 추가 의존성 없이 쓸 수 있다. JFR 파일을 받아서 JDK Mission Control이나 IntelliJ Profiler 같은 도구로 열면, 잡 1회 실행이 시간 축에 모두 펼쳐진다.

### 9.3.1 JFR 켜는 법

JVM 옵션 한 줄이면 된다. K8s CronJob의 `args:`에도 그대로 들어간다.

```bash
java \
  -XX:StartFlightRecording=duration=30m,filename=/var/log/batch.jfr,settings=profile \
  -jar settlement-batch.jar
```

`duration=30m`는 30분간 기록하겠다는 뜻이고, `settings=profile`은 default보다 조금 더 촘촘한 샘플링이다. 잡이 30분 안에 끝난다면 `duration` 없이 `dumponexit=true`로 두면 잡이 끝날 때 자동으로 파일로 떨어진다.

운영에서는 보통 두 가지 방식을 섞어 쓴다.

- **상시 기록(continuous):** 일정 크기 ring buffer로 항상 켜둔다. 문제 생기면 그 시점의 JFR을 dump.
- **on-demand 기록:** 특정 잡, 특정 시점에만 켜서 분석.

상시 기록은 다음과 같다.

```bash
java \
  -XX:StartFlightRecording=settings=default,maxsize=200m,disk=true,filename=/var/log/batch.jfr,dumponexit=true \
  -jar settlement-batch.jar
```

### 9.3.2 무엇을 보는가

JFR 파일을 열면 Spring Batch가 발행하는 이벤트가 시간 축에 표시된다. 가장 자주 보게 되는 이벤트는 다음이다.

- `org.springframework.batch.JobExecutionEvent` — 잡 시작/종료
- `org.springframework.batch.StepExecutionEvent` — 스텝 시작/종료
- `org.springframework.batch.ChunkExecutionEvent` — 청크 단위
- `org.springframework.batch.ItemReadEvent` / `ItemWriteEvent` — 항목 단위
- (JDK 자체 이벤트) `jdk.JavaMonitorWait`, `jdk.GCPhasePause`, `jdk.JdbcStatementExecute`

마지막 줄이 사실상 JFR의 진가다. **Spring Batch 이벤트와 JDK 자체 이벤트가 같은 시간 축에 겹쳐 보인다.** "청크 5번째에서 chunk write가 길어졌는데, 같은 시각에 GC pause가 800ms 걸렸다" 같은 인과관계를 찾는 데 결정적이다.

다만 6.0이 갓 GA된 단계라 JFR 운영 사례가 한국·영문 양쪽 모두 아직 풍부하지 않다. 1차 자료에 정직하게 표시한 한계다. 그래서 이 절은 "지금부터 자기 잡으로 사례를 만들어 가자"는 톤으로 받아들이는 편이 낫다. 운영하다 의심 가는 잡 하나에 JFR을 켜보고, JDK Mission Control로 펼쳐보는 경험 한 번이면 — 그 다음부터는 자기 패턴북에 추가된다.

## 9.4 알람 임계값 설계 — 가장 어려운 일

여기까지가 "측정"이다. 측정이 끝나면 다음 질문이 자연스럽게 이어진다 — **무엇을 어떤 임계값으로 알람으로 걸어야 하는가?**

이 질문이 가장 어렵다. 임계값을 너무 빡빡하게 잡으면 알람 피로(alert fatigue)가 쌓인다. 새벽 3시에 울리는 알람이 매번 "그냥 일시적이었다"로 끝나기 시작하면, 사람들은 알람 자체를 무시하기 시작한다. 반대로 너무 느슨하게 잡으면 진짜 문제가 났을 때 발견이 늦는다. 그 중간을 어떻게 잡을 것인가.

운영 1년차에는 "처음에 잘 잡았다"는 답이 없다. 잡아본 임계값을 운영하면서 조정해 가는 게 정직한 답이다. 다만 **출발점으로 삼을 만한 3축 분리**가 있다. 알람을 한 종류로 묶지 말고, 성격이 다른 세 축으로 나눠서 설계해보자.

### 9.4.1 3축 분리 — 정상 범위 / 추세 / 파편적 실패

**축 1 — 정상 범위 알람(absolute threshold).** 절대값 기준으로 정상 범위를 벗어났는지 본다. 잡 실패율이 5%를 넘으면 알람, 잡 처리 시간 p95가 10분을 넘으면 알람, 같은 식.

장점은 명확하다 — 임계값이 직관적이고 PromQL이 짧다. 단점은 "정상 범위"가 시간에 따라 변한다는 점을 못 따라간다. 데이터가 점점 늘면서 잡 시간도 자연스럽게 늘어나면, 절대 임계값은 매번 손으로 올려줘야 한다.

**축 2 — 추세 알람(trend deviation).** 7일 또는 14일 이동평균(moving average)을 기준선으로 두고, 거기서 ±N% 이상 벗어나면 알람. 절대값이 아니라 "평소와 비교"가 기준.

장점은 데이터 증가를 자동으로 반영한다는 점이다. 단점은 임계값이 복잡해져서 PromQL이 길어진다는 점이다. 그리고 "평소가 이미 비정상"인 상황에는 둔감하다. 그래서 축 1과 짝지어 쓴다.

**축 3 — 파편적 실패 알람(rare-event spike).** 평소에 거의 0인 메트릭이 갑자기 늘었는지를 본다. skip 카운터, retry 카운터, OOM 발생, recover() 호출 횟수 같은 것들. 추세도 아니고 절대값도 아닌, "0이 아니면 의심"이라는 결.

장점은 가장 뼈아픈 신호를 빠르게 잡는다는 점이다. 운영 사고 직전 가장 먼저 어긋나는 메트릭이 대개 이쪽이다. 단점은 알람이 너무 시끄러워지기 쉽다 — 그래서 minimum count(예: 1시간에 10회 이상)와 결합해 쓰는 편이 낫다.

세 축은 보완적이다. **정상 범위만 보면 시간 흐름을 못 따라가고, 추세만 보면 평시 비정상에 둔감하고, 파편적 실패만 보면 만성 문제는 못 잡는다.** 그래서 셋을 함께 깔아둔다.

### 9.4.2 잡 실패율 알람 — 절대값 + 이동평균

잡 실패율은 가장 1차적인 알람이다. 절대값과 이동평균을 함께 쓴 PromQL을 보자.

```promql
# 절대값: 최근 1시간 실패율 5% 초과
(
  sum by (name) (rate(spring_batch_job_seconds_count{status="FAILED"}[1h]))
  /
  sum by (name) (rate(spring_batch_job_seconds_count[1h]))
) > 0.05
```

```promql
# 추세: 최근 1시간 실패율이 7일 이동평균보다 +10%p 초과
(
  sum by (name) (rate(spring_batch_job_seconds_count{status="FAILED"}[1h]))
  /
  sum by (name) (rate(spring_batch_job_seconds_count[1h]))
)
-
(
  sum by (name) (rate(spring_batch_job_seconds_count{status="FAILED"}[7d]))
  /
  sum by (name) (rate(spring_batch_job_seconds_count[7d]))
) > 0.10
```

두 알람을 OR로 묶는다. 둘 중 하나만 터져도 의심한다. 알람 메시지에는 "어떤 축에서 터졌는가"를 적어두면 디버깅 1단계가 짧아진다.

### 9.4.3 처리 시간 알람 — 데이터 크기 정규화

잡 처리 시간을 그대로 임계값에 걸면 데이터 증가에 끌려간다. 그래서 "건당 처리 시간"으로 정규화하는 편이 낫다.

```promql
# 건당 처리 시간 = 잡 총 시간 / 처리 항목 수
sum by (name) (rate(spring_batch_job_seconds_sum[1h]))
/
sum by (name) (rate(spring_batch_chunk_write_seconds_count[1h]))
```

이 값이 7일 이동평균 대비 +30% 넘으면 알람. 데이터가 늘었든 줄었든 건당 시간 자체가 변했는지를 본다.

```promql
(
  sum by (name) (rate(spring_batch_job_seconds_sum[1h]))
  /
  sum by (name) (rate(spring_batch_chunk_write_seconds_count[1h]))
)
> 1.3 *
(
  sum by (name) (rate(spring_batch_job_seconds_sum[7d]))
  /
  sum by (name) (rate(spring_batch_chunk_write_seconds_count[7d]))
)
```

도입부의 "1시간 → 2시간이 됐다"는 통증이 이 알람이 잡으려는 자리다. 데이터가 두 배가 됐으면 시간도 두 배가 자연스럽다. 그러나 데이터가 그대로인데 시간만 두 배라면 — 그게 정확히 이 알람이 우는 순간이다.

### 9.4.4 Skip/Retry 누적 알람 — 일별 추세 + 비율

skip과 retry는 평시 0에 가까워야 정상이지만, 완전히 0인 잡은 드물다. 그래서 "갑자기 늘었는지"를 본다.

```promql
# skip 1시간 누적
sum by (name) (increase(spring_batch_step_seconds_count{status="COMPLETED"}[1h]))
```

이건 단순 카운터 추출이라, 실제로는 SkipListener에서 별도 메트릭을 등록해 추적하는 패턴이 더 흔하다. SkipListener가 발생할 때마다 `Counter`를 증가시키는 코드 한 줄을 넣어두면 PromQL이 깔끔해진다.

```java
@Component
public class SkipMetricListener implements SkipListener<Object, Object> {

    private final Counter skipCounter;

    public SkipMetricListener(MeterRegistry registry) {
        this.skipCounter = Counter.builder("batch.skip.count")
            .description("Number of skipped items")
            .register(registry);
    }

    @Override
    public void onSkipInRead(Throwable t) { skipCounter.increment(); }

    @Override
    public void onSkipInProcess(Object item, Throwable t) { skipCounter.increment(); }

    @Override
    public void onSkipInWrite(Object item, Throwable t) { skipCounter.increment(); }
}
```

이렇게 만든 `batch_skip_count_total`을 쓰면 PromQL이 자연스러워진다.

```promql
# 시간당 skip 누적이 평소(7일 평균)의 3배 초과
increase(batch_skip_count_total[1h])
>
3 * (increase(batch_skip_count_total[7d]) / 24 / 7)
```

축 3(파편적 실패)에 어울리는 모양이다. 평소 시간당 1~2건이던 게 갑자기 30건이 되는 순간을 잡는다.

### 9.4.5 알람 라우팅 — 채널을 셋으로 나눈다

알람의 임계값만큼 중요한 게 **어디로 어떻게 보낼 것인가**다. 운영해본 결과로 권하는 라우팅은 채널 셋이다.

- **#batch-critical (호출):** 즉시 사람을 깨워야 하는 것. 잡 자체 실패, recover() 자동 호출 실패, 금융 정합성 의심 알람.
- **#batch-warning (확인):** 모니터링 시간에 보면 되는 것. 처리 시간 ±30%, skip 추세 이상, p99 latency 증가.
- **#batch-info (로그):** 알람이라기보다 기록. 잡 시작/종료, recover() 자동 성공, retry 누적.

처음에는 모든 알람을 critical로 묶기 쉽다. 그러면 한 달 안에 알람 피로가 온다. 셋으로 나누고 각 채널의 SLO를 다르게 잡는 편이 낫다 — critical은 5분 안에 응답, warning은 다음 영업일 안에, info는 주간 회고에서 본다.

## 9.5 운영 UI — 자체 대시보드냐, Spring Cloud Data Flow냐

운영자가 잡의 모양을 보는 UI를 어디에 둘 것인가. 이 질문에 답이 둘 있다.

**선택 1 — 자체 Actuator + Grafana 대시보드.** 지금까지 다룬 것. 가볍고 자유롭다. 잡이 10개 이내, 단일 클러스터에서 운영하는 규모에서는 이 조합이 거의 늘 정답이다.

**선택 2 — Spring Cloud Data Flow(SCDF).** Spring Batch + Spring Cloud Task를 한꺼번에 묶어주는 운영 UI. 잡 의존성 그래프, 잡 launch UI, 잡 이력 검색이 화면으로 제공된다. 잡이 수십 개 이상으로 늘고, 잡 간 의존성 관리(잡 A 끝나면 잡 B 시작)가 필요해지는 규모에서 의미가 생긴다.

이 책은 SCDF를 깊게 다루지 않는다. 그 자체로 한 권의 분량이고, 한국 운영 사례도 아직 두텁지 않은 영역이라 정직하게 12장의 다음 학습 주제로 안내하는 편이 낫다고 판단했다. **운영 1년차에는 자체 Grafana로 충분하다.** 5번째 잡, 10번째 잡을 만들 즈음 SCDF로 옮겨갈 시점이 자연스럽게 온다. 그 시점에 이 책 너머로 한 발 더 나가면 된다.

## 마무리

이 장에서 한 일을 정리해보자. Micrometer + Actuator로 메트릭의 골격을 깔고, Prometheus + Grafana로 한 화면에 모았다. JFR로 트랜잭션 경계까지 들여다볼 수 있는 저수준 가시성을 추가했다. 그 위에 알람 임계값을 정상 범위 / 추세 / 파편적 실패 3축으로 나눠 설계했다.

핵심을 한 줄로 줄이면 이렇다 — **평시의 모양을 기록해두면, 어느 날 모양이 변할 때 본다.** 평시 기록 없이는 사후 추적이 추적이 아니라 추측이 된다. 잡이 죽었을 때보다 잡이 느려졌을 때 더 빨리 발견하는 운영을 만드는 일, 그것이 옵저버빌리티다.

그런데 여기까지의 설계가 의미 있으려면 한 가지 전제가 필요하다 — 잡이 죽었을 때 안전하게 다시 일어나야 한다. graceful shutdown이 동작하지 않거나, JobRepository가 무한 누적되거나, K8s가 Pod을 강제 종료하는 순간 메타가 박제되는 환경에서는, 아무리 정교한 모니터링도 결국 사람을 새벽에 호출하는 데 그친다. 다음 장은 그 운영 환경 자체를 다룬다 — K8s에서 Spring Batch 6을 production-ready로 돌리려면 무엇을 갖춰야 하는가.
