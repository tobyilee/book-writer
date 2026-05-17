# 11장. 보이지 않는 비용을 본다 — 관찰과 진단

새벽 두 시, 결제 API의 p95 응답시간이 1.4초를 찍고 있다는 알람이 울린다. 같은 API의 평소 p95는 180ms. 어제도, 그제도 코드는 한 줄도 안 바뀌었다. 사용량이 평소의 1.4배쯤 늘었을 뿐이다. 일어나서 모니터링 대시보드를 켠다. CPU는 30%, 메모리도 60%로 평온하다. DB 쪽 슬로우 쿼리 로그를 본다 — *비어 있다*. 가장 느린 쿼리도 80ms를 안 넘는다. 그런데 응답시간은 1.4초다.

이 자리에서 우리는 가장 난감한 종류의 질문 앞에 서게 된다. *어디가 느린지 보이지 않는다*. 코드는 그대로다. 모든 메트릭은 정상이다. 그런데 시스템은 *느리다*. 들여다볼 자리가 없는 게 아니라, 들여다볼 도구가 없다. 이 챕터의 출발선이 바로 거기다.

1장에서 우리는 한 가지 북극성을 받아두었다. *ORM 성능 문제의 99%는 라운드트립과 트랜잭션 동작에 있다*. 99%라는 숫자가 그저 수사가 아니라는 것을 이제 우리는 안다. 2장에서 풀과 statement caching을 깔았고, 3장에서 엔티티를 빚었고, 4장에서 N+1을 발견하는 눈을 갖췄다. 5장에서 가져오는 형태를 바꿨고, 6장에서 OSIV를 껐다. 7장에서 캐시의 자리를, 8장에서 락을, 9장에서 배치를, 10장에서 깊은 페이지를 정리했다. 열 개의 장에서 우리는 *코드를 바꾸는 법*을 차곡차곡 익혔다.

그런데 코드를 바꾸려면 *무엇이 잘못됐는지를 봐야 한다*. 새벽 두 시의 알람 앞에서 — 또는 평일 오후의 슬로우 클레임 앞에서 — 우리가 가져야 할 것은 *보는 도구*다. 이 챕터에서 모은다.

그리고 한 가지 더. 책 전체에서 우리는 매 챕터 끝에 "내 코드 체크리스트 3개"를 받아두었다. 36개의 체크리스트가 쌓였다. 이 챕터의 마지막 절에서 그 36개를 한 표로 모은다. 책을 덮고 IDE를 여는 자리다.

## SQL을 본다 — 첫 번째 도구

가장 먼저 정착시켜야 할 도구는 단순하다. *SQL을 본다*. Vlad의 14 tips 중 첫 번째가 이 한 줄이다. "SQL을 항상 본다." 다른 모든 도구는 이 한 줄 위에 얹힌다.

문제는 *어떻게* 보느냐다. JPA를 쓰면 우리가 짠 코드와 실제로 나가는 SQL 사이에 한 겹이 있다. 그 한 겹 때문에 *어떤 SQL이 언제 어떻게 나가는지*를 우리는 직관적으로 알 수 없다. 다섯 줄의 자바 코드가 한 줄의 INSERT를 만들기도 하고, 한 줄의 `findAll()`이 백 줄의 SELECT를 만들기도 한다. 그 사이가 보이지 않으면 우리는 짐작에 의지하게 되고, 짐작은 거의 항상 틀린다.

### `org.hibernate.SQL` + `orm.jdbc.bind`

가장 가벼운 방법부터 살펴보자. Hibernate가 그대로 제공하는 두 줄의 로깅 설정이다.

```yaml
logging:
  level:
    org.hibernate.SQL: DEBUG
    org.hibernate.orm.jdbc.bind: TRACE
```

`org.hibernate.SQL`은 Hibernate가 만들어내는 SQL을 그대로 콘솔에 찍는다. `org.hibernate.orm.jdbc.bind`(Hibernate 6 이전엔 `org.hibernate.type.descriptor.sql.BasicBinder`)는 그 SQL에 *바인딩되는 파라미터*를 찍는다. 두 줄을 함께 켜야 한다. 한 줄만 켜면 `where id = ?` 같은 SQL만 보일 뿐, *어떤 id가 들어갔는지*는 모른다. ID를 모르면 *어떤 사용자의 어떤 게시글이 만든 쿼리인지*를 추적할 수 없다.

이 두 줄은 개발 환경의 디폴트로 두자. `application-local.yml`이나 `application-dev.yml`에 박아 두는 편이 낫다. 콘솔이 SQL로 도배되는 게 처음엔 정신없지만, 일주일 쓰다 보면 *코드 한 줄이 어떤 SQL을 만드는지*가 머릿속에 그려진다. 4장의 N+1을 *직관으로* 발견하는 능력이 이 한 단계에서 자란다.

다만 production에서는 이 한 쌍을 절대 켜지 않는다. 로그가 폭주하고 디스크 I/O가 응답시간을 잡아먹는다. 운영에서 SQL을 봐야 한다면 *다른 도구*가 필요하다. 거기서 등장하는 것이 datasource-proxy다.

### datasource-proxy — production에서도 켤 수 있는 SQL 가시화

`org.hibernate.SQL` 한 쌍이 *개발 환경의 콘솔용*이라면, datasource-proxy는 *production의 메트릭/감사용*이다. Hibernate가 만든 SQL이 아니라 *JDBC 드라이버 앞에서 가로채는* 방식이라, Hibernate가 아닌 raw JDBC 호출까지 잡힌다. 그리고 배치 SQL을 *그룹으로 묶어 보여준다*. 한 트랜잭션 안에서 백 개의 INSERT가 묶여 나갔다는 사실이 한 줄로 정리된다.

```java
@Bean
public DataSource dataSource(@Qualifier("realDataSource") DataSource realDataSource) {
    return ProxyDataSourceBuilder
        .create(realDataSource)
        .name("DS-Proxy")
        .countQuery()
        .logQueryBySlf4j(SLF4JLogLevel.INFO)
        .multiline()
        .build();
}
```

이 한 묶음이 datasource-proxy의 입구다. `.countQuery()`는 트랜잭션 단위로 *쿼리 개수를 센다*. `.multiline()`은 SQL을 여러 줄로 나눠 가독성을 올린다. `.logQueryBySlf4j(...)`로 SLF4J 어디로 던질지 정한다. production에서는 ERROR 레벨로 두고 *N+1 detection listener*만 따로 붙여 두는 패턴이 정석이다. 평소엔 잠잠하다가 *조건에 걸리는 자리에서만* 알려준다.

p6spy와 자주 비교된다. 둘은 비슷한 일을 하지만 결이 다르다.

| 항목 | datasource-proxy | p6spy |
|------|------------------|-------|
| 설정 방식 | Java programmatic — Spring 친화 | declarative `spy.properties` — Java EE 친화 |
| 배치 가시화 | 묶어서 한 묶음으로 | row 단위로 한 줄씩 |
| Custom listener (N+1 detect) | 강력 | 가능 |
| JDBC 드라이버 프록시 | DataSource 레벨 | 드라이버·DataSource 둘 다 |
| 의존성 | Spring Boot starter 잘 정리됨 | 드라이버 클래스 이름 변경 필요 |

p6spy는 *드라이버 자체를 갈아 끼우는* 방식이라, 동작하는 환경의 폭이 넓다. Java EE 레거시나 비-Spring 환경에서는 p6spy가 자리를 잡기 좋다. 다만 Spring Boot 환경에서는 datasource-proxy가 *깔끔하다*. Java 코드 한 묶음으로 빌드되고, 메트릭 listener를 붙이기 좋고, 무엇보다 *배치 SQL을 한 묶음으로 보여준다*. 9장에서 `batch_size=25`를 켰는데 정말 묶이는지가 *눈에 보인다*. 한 줄씩 찍히는 로그를 세는 것과 *25개씩 묶인 로그를 보는 것*은 디버깅 난이도가 다르다.

Vlad가 production에서 datasource-proxy를 권하는 이유가 여기다. p6spy의 declarative 방식은 *환경 설정 파일에 따라* 동작이 달라진다. production에서 누군가가 `spy.properties`를 한 줄 바꾸면 시스템이 흔들린다. datasource-proxy는 *코드*로 묶여 있어, PR과 리뷰의 통제 안에 들어간다. 운영 자산을 운영 도구로 다루는 자리에 알맞다.

여기서 잊지 말자. SQL 가시화 도구를 켜는 일은 *비용을 보겠다는 결심*이다. 도구만 켜두고 보지 않으면 그것은 책상 위의 청진기와 같다. 도구가 켜졌다면 다음 절차는 *언제 보는지를 정하는 것*이다. CI에서 단위 테스트마다 본다. 운영에서 알람이 떴을 때 본다. 평소엔 메트릭 한 줄로 *느린 자리를 가리키게* 한다. 그 절차가 정해져야 도구가 일을 한다.

## 테스트에서 N+1을 잡는다 — 영구히

4장에서 우리는 N+1의 정의를 다시 봤다. *슬로우 쿼리 로그에 안 잡힌다*. *각 쿼리는 충분히 빠르다*. 그래서 production에서 N+1은 *없는 듯 보이다가 사용량이 늘면 시스템을 꺾는다*. 이 비대칭이 N+1의 무서움이다.

그렇다면 어떻게 영구히 잡을 수 있을까? 정답은 단순하다. *단위 테스트에 박는다*. 한 자리 잡았다고 끝이 아니라, *다시 만들어지지 않게 회귀 테스트로 막는다*. 코드 리뷰에 의지하지 않는다. 사람의 눈은 N+1을 놓친다 — 이미 우리 코드에 그것이 있다는 사실이 그 증거다.

### Hypersistence Utils의 `SQLStatementCountValidator`

Vlad가 만든 Hypersistence Utils 라이브러리에 그 도구가 들어 있다. 이름은 길지만 쓰는 법은 짧다.

```java
import io.hypersistence.utils.jdbc.validator.SQLStatementCountValidator;
import static io.hypersistence.utils.jdbc.validator.SQLStatementCountValidator.*;

@DataJpaTest
class PostListApiSqlCountTest {

    @Autowired PostRepository postRepository;

    @Test
    void 게시판_목록_API는_SQL_한_번에_끝난다() {
        reset();

        Page<PostListDto> page = postRepository.findListWithAuthor(
            PageRequest.of(0, 20));

        assertSelectCount(1);    // SELECT는 1번만 나간다
        assertInsertCount(0);    // INSERT는 0번
        assertUpdateCount(0);    // UPDATE는 0번
        assertDeleteCount(0);    // DELETE는 0번
    }
}
```

`reset()`이 한 번 호출되면, 그 뒤로 발생한 모든 SQL을 카운팅한다. `assertSelectCount(1)`이 한 줄로 *SELECT는 정확히 한 번만 나가야 한다*고 못 박는다. 만약 누군가가 한 달 뒤 이 코드에 `.getAuthor().getName()`을 추가해서 LAZY association을 깨운다면, *이 테스트가 빨갛게 변한다*. 누구의 눈에 띄기 전에, 빌드가 막힌다. N+1이 main 브랜치에 들어오지 못한다.

이 한 줄이 강력한 이유는 *불일치를 즉시 드러내기 때문*이다. SQL 카운트라는 *간접 지표*가 코드의 의도를 *직접 검증해준다*. 우리가 *list API는 SELECT 한 번에 끝나야 한다*고 머릿속으로 결정했다면, 그 결정은 테스트 한 줄에 박혀야 한다. 결정이 코드 옆에 같이 살아 있어야 결정이 지켜진다.

### CI에 회귀 테스트로 박는 패턴

한 자리에서 멈추지 말자. 우리 시스템의 *list API 전부*에 이 패턴을 박을 만하다. 작은 패턴 하나를 두자.

```java
abstract class SqlCountRegressionTest {

    @BeforeEach
    void resetCounter() {
        SQLStatementCountValidator.reset();
    }

    protected void assertSqlCount(int select, int insert, int update, int delete) {
        assertSelectCount(select);
        assertInsertCount(insert);
        assertUpdateCount(update);
        assertDeleteCount(delete);
    }
}
```

list API마다 이 추상 클래스를 상속받고 *기대값*을 한 줄로 적는다. 새로운 list API가 추가될 때 이 테스트가 함께 만들어지면, 한 달이 지나도 N+1은 다시 만들어지지 않는다. 코드 리뷰는 *사람이 가진 N+1 감지 능력*에 의존한다. 회귀 테스트는 *기계가 매번 짚는 자리*에 의존한다. 후자가 더 안정적이다.

물론 *모든 API*에 이 테스트를 박을 필요는 없다. 우리 시스템의 핵심 list API 다섯 개, 가장 큰 응답을 만드는 자리 세 개, 가장 자주 호출되는 자리 두 개. 그 정도면 충분하다. 자기 시스템의 *위험 표면*을 알아두자. 위험 표면 위에만 그물을 치는 게 정석이다.

여기서 4장에서 받았던 한 줄을 회수하자. *우리 코드의 N+1은 우리만 안다*. 책에는 없다. 그리고 *우리 코드의 N+1을 영구히 막는 회귀 테스트도 우리만 짠다*. CI 파이프라인에 SQL count 검증이 박혀 있는지가 그래서 11장의 첫 번째 체크리스트가 된다. 박혀 있지 않다면, 이 한 절을 다 읽었다는 의미는 *영구히 잡지 않았다*는 뜻이다.

## Hibernate Statistics — 안에서 새는 비용을 본다

datasource-proxy가 *밖에서 보는 도구*라면, Hibernate Statistics는 *안에서 보는 도구*다. PersistenceContext가 몇 개의 엔티티를 들고 있는지, 2차 캐시 hit ratio가 얼마인지, slowest query가 무엇인지, optimistic lock failure가 몇 번 났는지. Hibernate 내부에서만 알 수 있는 지표들이다.

켜는 방법은 한 줄이다.

```yaml
spring:
  jpa:
    properties:
      hibernate:
        generate_statistics: true
```

켜고 나면 `SessionFactory#getStatistics()`로 그 안의 모든 카운터에 접근할 수 있다. Micrometer로 export하면 Grafana 대시보드에 바로 띄울 수 있다.

```java
@Component
@RequiredArgsConstructor
public class HibernateMetricsBinder {

    private final EntityManagerFactory entityManagerFactory;
    private final MeterRegistry meterRegistry;

    @PostConstruct
    void bind() {
        SessionFactory sessionFactory = entityManagerFactory.unwrap(SessionFactory.class);
        Statistics statistics = sessionFactory.getStatistics();

        Gauge.builder("hibernate.cache.hit.ratio", statistics, s -> {
            long hits = s.getSecondLevelCacheHitCount();
            long total = hits + s.getSecondLevelCacheMissCount();
            return total == 0 ? 0.0 : (double) hits / total;
        }).register(meterRegistry);

        Gauge.builder("hibernate.session.open.count",
            statistics, Statistics::getSessionOpenCount).register(meterRegistry);

        Gauge.builder("hibernate.optimistic.failure.count",
            statistics, Statistics::getOptimisticFailureCount).register(meterRegistry);
    }
}
```

이 한 묶음이 들어가면 7장의 *2차 캐시 hit ratio*가 운영 대시보드에 뜨고, 8장의 *optimistic lock failure*가 시간대별로 보인다. 1차 캐시가 OOM을 만들고 있는지도 `getSessionOpenCount()`와 `getEntityLoadCount()`의 비율로 짐작할 수 있다. 9장에서 우리가 짠 *배치 코드의 flush+clear가 정말 PersistenceContext를 비우는지*도 이 대시보드에서 보인다.

### Production에서 켜는 비용 — 그리고 샘플링

Hibernate Statistics를 켜는 데에는 *공짜가 아니다*. Vlad는 production에서 통상 끄는 편을 권한다. 카운터 자체가 lock-free atomic 연산이라 한 호출당 비용은 작지만, *모든 SQL 호출마다 누적되는* 자리라 트래픽이 큰 시스템에서는 무시할 수 없는 부담이 된다. 트러블슈팅 때만 토글로 켜는 패턴이 안전하다.

그렇다고 production에서 *완전히 보지 못해야 하는가*. 그렇지는 않다. 두 가지 패턴이 있다.

첫째, **샘플링**이다. 운영 인스턴스가 여러 대라면, 그중 한두 대에서만 Statistics를 켠다. 전체 부하의 5~10%만 본다. 평소엔 그 대시보드를 흘끗 보는 정도로 충분하고, 알람이 떴을 때 그 인스턴스로 트래픽을 집중시켜 *집중 진단*을 한다.

둘째, **시간 기반 토글**이다. JMX endpoint나 Actuator endpoint로 *런타임에 켜고 끌 수 있게* 둔다. 알람이 떴을 때 인스턴스 단위로 5분만 켰다가 끄는 패턴이다. 5분이면 Statistics는 충분한 데이터를 모은다.

```java
@RestController
@RequestMapping("/admin/hibernate")
@RequiredArgsConstructor
public class HibernateStatisticsController {

    private final EntityManagerFactory entityManagerFactory;

    @PostMapping("/statistics/{enabled}")
    public void toggle(@PathVariable boolean enabled) {
        SessionFactory sessionFactory = entityManagerFactory.unwrap(SessionFactory.class);
        sessionFactory.getStatistics().setStatisticsEnabled(enabled);
    }
}
```

이 endpoint는 *관리자 권한* 뒤에 숨겨야 한다. 운영 보안의 일부다. 그 위에서, *알람이 떴을 때 한 번 켜고 5분 뒤에 끈다*는 절차가 운영 매뉴얼에 적혀 있어야 한다. 절차가 적혀 있어야 새벽 두 시에도 망설임 없이 켜진다.

여기서 한 가지 더. Hibernate Statistics를 켜고 가장 먼저 봐야 할 지표가 무엇인가? 우선순위가 있다.

- `getSlowQueryThreshold()` 이상의 slowest queries — *눈에 보이는 자리*. 가장 먼저 잡힌다.
- 2차 캐시 hit ratio — 7장의 *캐시를 켰다면 효과가 있는가*의 답.
- optimistic lock failure count — 8장의 *충돌 retry가 어디서 일어나는가*의 답.
- entity load count vs session open count — *세션당 평균 엔티티 수*. 1차 캐시 OOM의 사전 경고.

이 네 가지면 우리 시스템의 *내부 비용*이 한 화면에 잡힌다. Statistics가 다른 것 다 빼고 이 네 줄만 봐도 충분하다.

## FlexyPool — 풀의 안쪽을 본다

2장에서 우리는 풀 사이징의 직관을 받았다. *풀은 작게 시작한다*. 그러나 *얼마나 작게*는 시스템마다 다르다. Vlad의 64-트랜잭션 실험에서 정답은 4였다. 우리 시스템의 정답은 우리만 알 수 있다.

그 정답을 *측정으로 찾아주는* 도구가 FlexyPool이다. 2장에서 우리는 이 도구의 존재를 받았다. 11장에서는 그 메트릭을 본다.

```java
@Bean
public DataSource dataSource() {
    HikariDataSource hikariDataSource = new HikariDataSource(hikariConfig());

    Configuration<HikariDataSource> configuration =
        new Configuration.Builder<>(
            "FlexyHikari",
            hikariDataSource,
            HikariCPPoolAdapter.FACTORY)
        .setMetricsFactory(MicrometerMetrics.FACTORY)
        .setConnectionAcquisitionTimeThreshold(50)  // 50ms 초과시 알람
        .build();

    return new FlexyPoolDataSource<>(configuration,
        new IncrementPoolOnTimeoutConnectionAcquisitionStrategy.Factory<>(5, 5));
}
```

이 묶음이 두 가지 일을 한다. 첫째, *connection acquisition time을 histogram으로 측정*한다. p50, p95, p99 — 어느 구간에서 풀이 비어 있어 기다리고 있는지 보인다. 둘째, *acquisition timeout*이 나면 풀을 *임시로 5개씩 늘린다*. 운영 중에 트래픽 스파이크가 와도 시스템이 안 죽는다.

FlexyPool이 제공하는 메트릭 중에서 운영 대시보드에 꼭 둘 만한 것이 두 가지다.

- **connection acquisition time histogram** — *풀 사이즈가 적절한가*의 답. p99가 10ms 미만이면 충분히 큰 풀이다. 100ms를 넘기는 자리가 있다면 풀이 부족하거나 *트랜잭션이 길게 잡고 있다*는 신호다. 후자라면 6장으로 돌아가 *언제 커넥션을 잡는지*를 다시 본다.
- **overflow 사용량** — IncrementPool 전략이 실제로 *얼마나 자주 늘리는가*. 평소에 0이라면 풀 사이즈가 충분하다. 자주 5씩 늘리고 있다면 *디폴트 풀이 부족하다*는 신호. 평소 사이즈를 올리자.

이 두 줄이 *우리 풀의 진실*을 말해준다. 통념이 아니라 측정이다. 1장에서 Vlad가 켠 USL 그래프가 우리 운영 대시보드 위에서 *다시 그려진다*. 그 모양이 어떤가를 보는 일이 *우리 시스템의 풀 사이즈를 정할 권리*다. 보지 않고 정하는 사람은 결국 직감에 기댄다. 직감은 어느 한 자리에서 틀린다.

2장에서 받았던 한 줄을 회수하자. *connection acquire time을 지표로 보고 있는가*. 보고 있지 않다면, 우리 풀 사이즈에 대한 모든 결정은 *추측*이다. 추측을 측정으로 바꾸는 자리가 여기다. FlexyPool이 마음에 들지 않으면 HikariCP 자체 Micrometer 메트릭(`hikaricp.connections.acquire`)을 봐도 좋다. 도구는 둘째 문제다. *보고 있는가*가 첫째 문제다.

## Hypersistence Optimizer — 정적 분석으로 잡는 안티패턴

지금까지 본 도구들은 *런타임에 보는 도구*다. SQL이 나가고, 카운트가 쌓이고, 풀이 늘어나는 자리를 본다. 그런데 한 가지 도구가 더 있다. *런타임 이전에* 안티패턴을 잡는 도구. Vlad가 만든 Hypersistence Optimizer다.

이 도구는 application 시작 시점에 *엔티티 매핑·설정·관계 정의*를 한 번 훑어보고, 잘 알려진 안티패턴 50여 가지를 자동으로 검출한다. 우리가 책 전체에서 다룬 안티패턴 대부분이 이 한 묶음 안에 있다.

```java
@Configuration
@Profile("dev")
public class HypersistenceOptimizerConfig {

    @Bean
    public HypersistenceOptimizer hypersistenceOptimizer(EntityManagerFactory emf) {
        return new HypersistenceOptimizer(new JpaConfig(emf));
    }
}
```

이 한 묶음이 application 시작 시 콘솔에 안티패턴 경고를 출력한다. 예를 들면 이런 식이다.

```
WARN: EagerFetchingEvent - The [post.tags] association is using EAGER fetching.
   Consider switching to LAZY and using fetch joins per query.
WARN: ConnectionProviderEvent - The hibernate.connection.provider_disables_autocommit is not set.
   This causes JDBC connections to be acquired earlier than necessary.
WARN: IdentityGeneratorEvent - The [order] entity uses IDENTITY which disables JDBC batch inserts.
   Consider using SEQUENCE generator instead.
```

이 한 줄 한 줄이 우리가 책 전체에서 다룬 자리들이다. EAGER, provider_disables_autocommit, IDENTITY + batch. 이미 우리는 *왜* 안 좋은지를 안다. Hypersistence Optimizer는 *어디에 있는지*를 가리켜준다. 둘이 합쳐지면 즉시 PR이 된다.

도구가 상용이라는 점은 짚어두자. 무료가 아니다. 다만 한 번이라도 돌려보면 *우리 코드에 안티패턴이 얼마나 있는지*를 일주일 안에 알 수 있다. 14일 평가판이라도 한 번 돌려본 적이 있는가가 11장의 세 번째 체크리스트다. 돌려본 적이 없다면, 우리는 우리 코드에 어떤 함정이 있는지를 *정확히는 모른다*. 사람의 눈으로 보는 안티패턴과 정적 분석이 잡는 안티패턴은 *겹치되 같지 않다*.

상용이 부담스러우면 무료 대안도 있다. IntelliJ IDEA의 JPA inspections, SpotBugs의 jpa-plugin, jpa-buddy 플러그인. 모두 *부분적*이긴 하지만 어느 정도는 잡는다. 완벽한 도구를 기다리지 말고 *무엇이든 켜자*. 안 켜는 것보다는 한 가지를 켜는 게 압도적으로 낫다.

## 안티패턴 카탈로그 회수 — 내가 이 책을 시작할 때 했던 실수들

여기서 잠시 멈춰 서 보자. 책을 처음 폈을 때, 우리 코드를 떠올리며 *"이 정도면 무난하다"*고 생각했던 자리가 분명히 있었을 것이다. 이제 그 자리들을 한 표로 모아본다. 책 전체에서 다룬 *안티패턴 12개*다. 정직하게 자기 코드에 대입해보자.

| 안티패턴 | 어디서 다뤘나 | 증상 | 정답 |
|----------|----------------|------|------|
| `FetchType.EAGER`을 디폴트로 둠 | 4장 | 모든 query에 join 또는 secondary select가 따라 나간다 | 모든 association을 LAZY로 명시. fetch는 *per-query* JOIN FETCH/EntityGraph로 |
| `spring.jpa.open-in-view=true` | 6장 | 커넥션 lease 증가, View에서 lazy N+1 발생 | `open-in-view=false` + DTO/JOIN FETCH로 *서비스에서 끝내고* 반환 |
| `hibernate.enable_lazy_load_no_trans=true` | 6장 | LazyInitializationException은 안 나지만 매 lazy마다 새 트랜잭션, 커넥션 폭주 | *어떤 상황에서도 켜지 않는다.* 정상 fetch 또는 DTO로 해결 |
| `IDENTITY` + 배치 INSERT 기대 | 3장, 9장 | INSERT가 한 줄씩 나간다, `batch_size`는 무시된다 | SEQUENCE(pooled-lo). MySQL이면 수동 ID 또는 StatelessSession |
| OFFSET으로 깊은 페이지 처리 | 10장 | 페이지 깊이에 따라 응답시간이 무너진다 | keyset(seek) pagination. `WHERE (created_at, id) < (?, ?)` 패턴 |
| 컬렉션 fetch join + 페이지네이션 | 4장, 10장 | HHH000104 경고 + 메모리 OOM | 2-query 패턴. ID 한 번 + 본문 한 번 |
| 쿼리 캐시 단독 사용 | 7장 | PK 목록만 캐시되어 엔티티 조회에서 N+1 재발 | 엔티티 2차 캐시와 *함께* 켜기. 안 되면 끄는 편이 낫다 |
| Open Interface Projection의 SELECT * | 5장 | 4개 컬럼만 필요한데 SELECT *이 나간다 | JPQL constructor expression + Records, 또는 닫힌 interface projection |
| One-to-Many DTO projection에서 `ResultTransformer` 누락 | 5장 | 부모-자식 join 결과가 카르테시안 곱으로 풀린다 | `ResultTransformer.distinct()` 또는 Hibernate 6 `TupleTransformer.LIST` |
| 2차 캐시 무효화 우회(직접 UPDATE 발행) | 7장 | DB와 캐시의 일관성 깨짐 | bulk UPDATE 후 명시적 `evict`, 또는 `@SQLInsert/@SQLUpdate`로 우회 자체 회피 |
| `default_batch_fetch_size=0` 디폴트 방치 | 4장 | LAZY 컬렉션을 깨우면 N+1 | 100~1000 사이 값. ToMany는 batch_size, ToOne은 fetch join |
| equals/hashCode를 IDE 자동완성으로 둠 | 3장 | transient 상태에서 Set에 넣었다가 PK 발급 후 *같은 entity*를 못 찾는다 | PK + `getClass().hashCode()` 패턴 또는 비즈니스 키 |

이 표를 보고 있으면 한 가지 감각이 자연스럽게 든다. *내가 이 책을 시작할 때, 이 중 몇 가지에 해당하는 코드를 짜고 있었나*. 솔직하게 답해보자. 두 가지? 다섯 가지? 모두? 그 답이 무엇이든 — *이제 우리는 안다*. 안다는 것이 가장 큰 변화다.

물론 안다고 모두 *오늘 당장* 고칠 수는 없다. 운영 중인 시스템에 EAGER를 한꺼번에 LAZY로 바꾸는 일은 한 달짜리 PR이다. OSIV를 끄는 결단은 *예외가 쏟아질* 가능성을 안고 가는 일이다. IDENTITY를 SEQUENCE로 바꾸는 일은 마이그레이션 스크립트와 함께 와야 한다.

다만 한 가지는 다르다. *새로 짜는 코드*에 이 안티패턴 12개는 들어가지 않는다. 그것이 11장이 우리에게 시킨 일의 핵심이다. 기존 코드는 점진적으로 고친다. 새 코드는 처음부터 다르게 짠다. 이 두 줄로 책 한 권의 가치가 실현된다.

## 36개 체크리스트 — 책을 덮고 자기 코드로 돌아간다

이제 마지막 자리에 다다랐다. 책을 처음 폈을 때 우리는 한 가지 약속을 받았다. *매 챕터 끝에 "내 코드 체크리스트 3개"가 있다. 12개 챕터를 다 읽으면 36개의 체크리스트가 쌓인다. 11장에서 한 표로 회수한다.* 그 약속을 지킨다.

여기서 가장 중요한 것은 — 표를 *읽는 것이 아니라 풀어내는 것*이다. 한 줄씩, 자기 IDE를 열고, `application.yml`을 펴고, 핵심 엔티티를 열어, 30초씩 답해본다. 표는 한 번 본다고 끝이 아니다. 분기마다 한 번씩 다시 본다. 그게 *읽고 자기 코드로 돌아가는 책*의 정석이다.

| # | 챕터 | 체크리스트 |
|---|------|-------------|
| 1 | 1장 | 우리 서비스의 현재 HikariCP `maximumPoolSize`가 몇인지, 그 숫자의 *근거*가 무엇인지 안다 |
| 2 | 1장 | 가장 자주 호출되는 read API의 평균 응답시간 중 *DB 응답시간 비중*을 안다 |
| 3 | 1장 | `application.yml`의 `spring.jpa.open-in-view` 값을 안다 |
| 4 | 2장 | JDBC URL에 statement cache 옵션(PG `prepareThreshold`, MySQL `cachePrepStmts`)이 명시되어 있다 |
| 5 | 2장 | `hibernate.connection.provider_disables_autocommit=true`와 HikariCP `auto-commit: false`가 *함께* 켜져 있다 |
| 6 | 2장 | connection acquire time(p99)을 지표로 보고 있다 |
| 7 | 3장 | 핵심 엔티티 5개의 `@Id` 전략이 의도된 선택이다(MySQL인데 `AUTO`가 박혀 있지 않다) |
| 8 | 3장 | equals/hashCode가 PK 기반이라면 `id != null && id.equals(...)` 가드와 상수 `hashCode`가 들어 있다 |
| 9 | 3장 | bytecode enhancement plugin을 켰는지/꺼두었는지를 알고, 켰다면 어떤 옵션을 *왜* 켰는지 한 줄로 설명할 수 있다 |
| 10 | 4장 | 모든 `@ManyToOne`/`@OneToOne`에 `fetch = LAZY`가 *명시적으로* 붙어 있다 |
| 11 | 4장 | 컬렉션 fetch join + 페이지네이션이 함께 걸린 자리가 없다(있다면 HHH000104가 로그에 보일 것이다) |
| 12 | 4장 | 가장 큰 list API의 SQL 카운트를 단위 테스트로 검증하고 있다 |
| 13 | 5장 | 가장 자주 호출되는 read API 5개 중 엔티티를 반환하는 것이 몇 개인지, 그것이 *수정 의도*가 있는 자리인지 확인했다 |
| 14 | 5장 | Open Interface Projection을 쓰는 곳이 있다면 datasource-proxy로 *SELECT 절*을 검증했다 |
| 15 | 5장 | 분석/리포트성 쿼리에 Native나 jOOQ, 또는 H6 JPQL window function을 검토해 본 적이 있다 |
| 16 | 6장 | `spring.jpa.open-in-view=false`가 박혀 있다 |
| 17 | 6장 | 서비스 계층에 디폴트 `@Transactional(readOnly = true)`이, write 메서드에만 오버라이드가 박혀 있다. Repository에는 트랜잭션이 없다 |
| 18 | 6장 | `hibernate.enable_lazy_load_no_trans`가 *꺼져* 있다(켜져 있다면 그 자체가 사고의 위치다) |
| 19 | 7장 | 2차 캐시를 쓴다면 어떤 엔티티에 어떤 concurrency strategy로 걸려 있는지 한 표로 적을 수 있다 |
| 20 | 7장 | 쿼리 캐시가 켜져 있다면 그 쿼리가 가리키는 엔티티에 2차 캐시도 함께 켜져 있다 |
| 21 | 7장 | `hibernate.query.in_clause_parameter_padding=true`가 켜져 있다 |
| 22 | 8장 | 동시 수정 가능성이 있는 엔티티에 `@Version`이 붙어 있다 |
| 23 | 8장 | MySQL이라면 핵심 트랜잭션의 isolation을 *의식적으로* 정한 적이 있다 |
| 24 | 8장 | `SELECT ... FOR UPDATE`를 쓰는 자리의 *잠기는 범위*(gap lock 포함)를 EXPLAIN으로 확인한 적이 있다 |
| 25 | 9장 | `hibernate.jdbc.batch_size` + `order_inserts=true` + `order_updates=true`가 *함께* 켜져 있다 |
| 26 | 9장 | 대량 INSERT 코드에 `flush() + clear()` 루프가 있다(또는 StatelessSession을 쓴다) |
| 27 | 9장 | 대량 ingest 경로에 PostgreSQL `reWriteBatchedInserts=true`(또는 MySQL `rewriteBatchedStatements=true`)가 켜져 있다 |
| 28 | 10장 | 가장 큰 list API가 keyset 기반이다(아니라면 OFFSET인 이유가 명시적이다) |
| 29 | 10장 | 정렬 컬럼이 tie를 만들 때 두 번째 정렬 키(보통 PK)가 함께 들어가 있다 |
| 30 | 10장 | 깊은 페이지(500페이지 정도)와 첫 페이지의 응답시간 차이를 측정해본 적이 있다 |
| 31 | 11장 | CI 파이프라인에 SQL count 회귀 테스트가 박혀 있다(최소 핵심 list API 다섯 개) |
| 32 | 11장 | Production에서 Hibernate Statistics의 일부 지표(slowest query, cache hit ratio, optimistic failure)를 메트릭으로 보고 있다 |
| 33 | 11장 | Hypersistence Optimizer(또는 IDE inspection)를 *한 번이라도* 돌려본 적이 있다 |
| 34 | 12장 | 운영 중인 Audit/Soft Delete가 있다면 Envers·`@SoftDelete`로의 이전이나 CDC 분리 검토를 해본 적이 있다 |
| 35 | 12장 | 분석성 쿼리에 jOOQ를 *부분 도입*할 만한 자리가 있는지 한 번이라도 따져봤다 |
| 36 | 12장 | 다음 분기 학습 계획에 Hibernate 6.6+/Jakarta Data 한 줄이라도 들어가 있다 |

이 36줄을 한 번에 다 통과하는 시스템은 거의 없을 것이다. 그래도 괜찮다. *한 줄씩 통과시켜 가는 일*이 이 책이 우리에게 시킨 일이다. 일주일에 한 줄씩이면 1년이면 다 통과한다. 1년 뒤의 우리 시스템은 *지금과 다른 시스템*이다.

표를 한 번 더 보자. 어떤 줄에서 *모르겠다*고 답해야 했는가? 그 자리가 우리 시스템의 가장 큰 *위험 표면*이다. 답을 모른다는 것은 코드가 그 자리에서 *어떻게 동작하는지를 모른다*는 뜻이다. 모르는 자리는 *측정하지 않은 자리*이고, 측정하지 않은 자리는 *문제가 와도 알아채지 못하는 자리*다. 11장이 우리에게 시킨 일은 — 그 자리들을 *보이게 만드는 것*이다.

## 본 챕터의 체크리스트 3개

11장도 다른 챕터와 똑같이 끝맺자. 세 가지 자리, 30초씩.

**하나, CI 파이프라인에 SQL count 회귀 테스트가 박혀 있는가?**

핵심 list API 다섯 개에 `SQLStatementCountValidator.assertSelectCount(...)`가 박혀 있는지. 박혀 있지 않다면, N+1은 *영구히 잡히지 않았다*. 한 자리에서 잡았다고 끝이 아니다. 회귀 테스트가 없으면 한 달 뒤에 다시 만들어진다. 가장 큰 list API 하나만이라도 오늘 박는 편이 낫다. 시작은 한 줄이다.

**둘, Production에서 Hibernate Statistics의 일부라도 메트릭으로 보고 있는가?**

cache hit ratio든, optimistic failure count든, slowest query 한 줄이든. *무엇이든 한 가지*를 운영 대시보드에 두자. 보지 않으면 우리는 *문제가 일어난 뒤*에야 안다. 한 줄이라도 보고 있으면 *문제가 자라는 동안* 안다. 그 차이가 알람을 *예방으로* 바꾼다.

**셋, 정적 분석(Hypersistence Optimizer 또는 IDE inspection)을 한 번이라도 돌려본 적이 있는가?**

상용이 부담스러우면 14일 평가판으로 한 번이라도. 그게 안 되면 IntelliJ JPA inspections라도 한 번 깔끔하게 통과시켜보자. 알람이 뜨지 않는 코드와 *알람을 한 번도 켜본 적이 없는 코드*는 다르다. 한 번 켜본 적이 있어야 *우리 코드가 깨끗한지*를 안다. 한 번도 안 켜봤다면 *깨끗하지 않을 가능성이 매우 높다*. 책 전체에서 다룬 안티패턴 12개 중 몇 가지는 거의 분명히 우리 코드에 있을 것이기 때문이다.

이 세 줄이 11장의 체크리스트다. 36개 표의 31, 32, 33번 줄이기도 하다. 회수가 자기 자리에 맞게 들어왔다.

## 다음 장 — 그리고 그 다음

여기까지 왔으면 책이 거의 끝나간다. 11장이 *책 전체의 회수*였다면, 12장은 *책 다음의 지도*다. 운영 기능 네 가지(Audit, Soft Delete, Multi-tenancy, Stored Procedure)가 한 묶음으로 정리되고, 그 다음 *책 다음에 가야 할 자리*가 한 묶음으로 정리된다. Hibernate 6의 신기능, JPA + jOOQ 조합, Jakarta Data, Reactive에 대한 입장. 그리고 마지막에 1장의 북극성 — *라운드트립과 트랜잭션 동작* — 을 다시 한 번 가리킨다.

그 전에 한 가지를 적어 두자. 11장에서 다룬 도구들 — datasource-proxy, `SQLStatementCountValidator`, Hibernate Statistics, FlexyPool metrics, Hypersistence Optimizer — 다섯 가지는 *오늘 당장 켤 수 있는 다섯 가지*다. 켜는 데 코드 한 묶음과 의존성 한 줄이면 된다. 켜고 나서 한 주만 보면 우리 시스템이 어디서 새는지가 보이기 시작한다. 한 주의 측정이 한 달의 추측을 이긴다.

그리고 보이기 시작하면 — 1장에서 약속한 *"내가 만든 ORM 성능 문제는 어디서 봐야 하는가"*에 우리는 이제 답할 수 있다. 보이는 곳에서 본다. 11장이 그 보이는 곳을 만들어주는 자리다. 책의 첫 페이지가 던진 질문에 마지막 한 장 직전에 답이 닿는다.

이제 12장으로 넘어가자. 11장이 *책 전체를 모아 묶은 자리*였다면, 12장은 *모아 묶은 짐을 들고 어디로 갈지를 정하는 자리*다. 책의 마지막 페이지가 가까워졌다. 한 챕터만 더 함께 가자.
