# 4장. `java.time`과 종종 잊히는 Java 8의 보석들

결제 정산 시스템이 새벽에 깨졌다고 해보자. 한국 시간 자정에 마감되는 일일 정산 배치가 미국 동부의 결제 게이트웨이에서 받은 거래 시각을 잘못 해석한 탓이었다. 거래 시각은 `2026-05-04T22:30:00`이라는 *시간대 정보 없는 문자열*로 넘어왔고, 우리 코드는 그걸 한국 시간으로 가정해 처리했다. 실제로는 미국 동부 시간 — UTC-4 — 의 22:30이었으니, UTC로는 다음 날 02:30, 한국 시간으로는 같은 날 11:30이었다. 정산일이 하루씩 어긋났고, 그 차이만큼의 거래가 *어제와 오늘의 경계*에서 사라졌다.

이런 버그를 겪고 새벽에 깨본 사람이라면 안다. 시간대 처리는 *틀리면 조용히 틀린다*. 컴파일도 되고 단위 테스트도 통과하는데, 한 달 뒤 정산 보고서에서 5만 원짜리 거래 한 건이 두 번 잡혀 있거나 아예 빠져 있는 식이다. 끔찍한 일이다.

그래서 묻자. 우리는 정말 `java.util.Date`와 `Calendar`에서 벗어났을까? Java 8이 `java.time`을 들고 온 지 11년이 됐는데, 사내 코드베이스 어디엔가는 여전히 `new Date()`와 `Calendar.getInstance()`가 살아 있지 않을까. 그리고 더 중요하게, *벗어났다고 믿고 있는 우리*가 `java.time`을 정말 제대로 쓰고 있을까. 한번 들여다보자.

## `Date`와 `Calendar`의 *끔찍했던* 결함들

먼저 우리가 어디에서 출발했는지를 기억하자. Java 1.0의 `java.util.Date`는 *디자인의 거의 모든 차원에서* 실패한 클래스다. 그 결함을 하나씩 짚어두자.

**첫째, 의미의 혼란.** `Date`라는 이름이 무색하게도, 이 클래스는 *날짜*가 아니다. UTC 기준 epoch 밀리초를 담는 *시각(instant)*이다. "오늘이 며칠인가"를 표현하고 싶으면 다른 도구가 필요한데, JDK는 그걸 주지 않았다.

**둘째, mutable.** `Date`의 `setTime()`, `setYear()`, `setMonth()` 같은 메서드가 객체 내부 상태를 바꾼다. 한 `Date` 인스턴스를 여러 곳에서 공유하는 코드는 *어디에서 변형이 일어났는지* 추적하기가 사실상 불가능했다. 그래서 모든 getter가 *방어적 복사*를 해야 했고, 그 비용과 보일러플레이트는 11년 내내 자바 개발자의 *지긋지긋한* 동반자였다.

**셋째, thread-unsafe.** `SimpleDateFormat`이 가장 악명 높았다. 멀티스레드 환경에서 같은 포매터 인스턴스를 공유하면 *조용히 잘못된 문자열*을 뱉었다. 첫 번째 호출은 멀쩡한데 두 번째에서 갑자기 깨지는 식이라, 재현이 어렵고 디버깅이 끔찍했다.

**넷째, 0-based month.** `Calendar.set(2026, 4, 4)`가 5월 4일을 만든다. 4월이 아니다. C 언어의 `tm` 구조체에서 가져온 이 *유물*이 자바 1.0에 그대로 박혀 들어왔고, 11년 동안 수많은 off-by-one 버그를 양산했다.

**다섯째, `Calendar`의 거대함.** `Calendar`는 *모든 달력 시스템을 추상화*한다는 야심으로 만들어졌는데, 실제로는 그레고리력만 제대로 동작했고, API는 거대한 비밀번호 자판 같았다 — `add()`, `roll()`, `set()`, `get()` 사이의 차이를 직관으로 짐작할 수 없었다.

**여섯째, `TimeZone`과의 어색한 결합.** 시간대는 `Date`에 묶이지 않고 별도 `TimeZone` 객체를 통해 *간접적으로* 표현됐다. 같은 epoch 값을 가진 두 `Date`가 같은 시각인지 다른 시각인지는 코드 작성자만 알았다.

이 결함들 때문에 자바 개발자들은 *오랫동안 외부 라이브러리*에 의존했다. 그 이름이 **Joda-Time**이다.

## Joda-Time과 Stephen Colebourne의 유산

Joda-Time은 2002년부터 Stephen Colebourne이 만들고 발전시킨 시간 라이브러리다. 자바 1.0이 못한 일들을 하나씩 풀어냈다 — immutable 객체, 명확한 의미 분리(`LocalDate` vs `LocalDateTime` vs `DateTime`), thread-safe 포매터, 1-based month. 2010년대 초중반의 거의 모든 자바 프로젝트가 Joda-Time을 의존성에 추가했다.

흥미로운 점은 JDK가 결국 *Joda-Time의 저자에게 직접 표준 시간 API를 그려달라고 의뢰*했다는 사실이다. JSR-310은 Stephen Colebourne이 주도한 JEP이고, Java 8의 `java.time`은 사실상 *Joda-Time의 교훈을 흡수한 차세대*다. 단지 베끼지 않았다. Colebourne 본인도 Joda-Time에서 잘못 설계했다고 판단한 부분들 — 예를 들어 `DateTime`이라는 단일 클래스로 너무 많은 의미를 묶었던 점 — 을 새 API에서 *분리*했다. 그래서 `java.time`은 클래스가 많아 보이지만, 그 많음이 *의미의 명확함*에서 나온다.

기억해두자. `java.time`을 깊이 이해하려면 그것이 *Joda-Time의 후예*라는 사실을 알고 시작하는 편이 낫다. 두 라이브러리는 메서드명이 비슷한데 *의미가 다른 자리*가 꽤 있기 때문이다 — `getMonthOfYear()` vs `getMonthValue()`, `plusDays()` 동작의 미묘한 차이 같은 것들 말이다.

## 일곱 가지 시간 — `java.time`의 어휘

`java.time`이 처음에 거대해 보이는 이유는 시간을 *일곱 가지 다른 의미*로 나눠 표현하기 때문이다. 일단 이름을 외우고, 의미를 한 줄씩 붙여보자.

| 클래스 | 의미 | 시간대 정보 |
|--------|------|------------|
| `LocalDate` | "2026년 5월 4일" — 날짜만 | 없음 |
| `LocalTime` | "오후 11시 30분" — 시각만 | 없음 |
| `LocalDateTime` | "2026년 5월 4일 오후 11시 30분" | 없음 |
| `ZonedDateTime` | 위 + "Asia/Seoul" 시간대 | 있음 (지역) |
| `OffsetDateTime` | 위 + "+09:00" 오프셋 | 있음 (오프셋만) |
| `Instant` | UTC 기준 epoch 시각 | 항상 UTC |
| `Year`, `YearMonth`, `MonthDay` | 부분 정보 | 없음 |

이 표를 외우는 일은 *시간대 버그를 줄이는 첫걸음*이다. 각 클래스가 무엇을 표현하는지 *그리고 무엇을 표현하지 않는지*를 알면, "이 값에 시간대를 붙여야 하나 말아야 하나"가 코드 작성 시점에 결정된다.

가장 중요한 구분이 `LocalDateTime`과 `ZonedDateTime`의 차이다. `LocalDateTime`은 *시간대 정보가 없다*. "2026-05-04T23:30:00"이라는 정보만 있고, 이게 한국 시간인지 미국 시간인지 알 수 없다. 머리말의 정산 버그가 정확히 이 자리에서 터졌다. 외부 시스템에서 시각 정보를 받을 때, 그것이 `LocalDateTime`으로 표현되어 있다면 *시간대를 누가 어디서 결정하는지*를 반드시 짚어야 한다.

`Instant`는 정반대다. 시간대 따위가 없고, 그냥 *epoch 이후 몇 나노초가 지났는가*만 담는다. 기계 친화적이고, 데이터베이스 저장과 로그 기록과 분산 시스템 메시지에 적합하다. *기계가 읽는 시각은 `Instant`로, 사람이 읽는 시각은 `ZonedDateTime`으로* — 이 원칙을 한 줄로 외워두면 절반은 안전하다.

```java
// 1. 사람이 입력한 시각 — 시간대 명시
ZonedDateTime userTime = ZonedDateTime.of(2026, 5, 4, 23, 30, 0, 0, ZoneId.of("Asia/Seoul"));

// 2. UTC로 변환해 저장
Instant utc = userTime.toInstant();

// 3. 다시 사람에게 보여줄 때 — 다른 시간대로 표시
ZonedDateTime forUS = utc.atZone(ZoneId.of("America/New_York"));
```

이 세 단계를 *어디에서나 같은 패턴으로* 적용하면, 정산 버그의 절반은 사라진다.

## `Duration`과 `Period` — 시간의 두 가지 *기간*

자주 헷갈리는 두 클래스가 있다. `Duration`과 `Period`다. 둘 다 *기간*을 표현하는데, 의미가 다르다.

`Duration`은 *기계적 시간*이다. "5초", "3시간 27분"처럼 *정확한 양*을 담는다. 내부적으로 초와 나노초로 표현된다.

`Period`는 *달력 시간*이다. "1개월", "2년 3개월"처럼 *달력 단위*를 담는다. 1개월은 28일일 수도, 31일일 수도 있다.

이 차이가 왜 중요한가. *서머타임이 있는 자리*에서 둘이 다르게 동작하기 때문이다. 미국 동부에서 3월 둘째 주 일요일에 서머타임이 시작되면, 그날의 *달력상 24시간*은 *실제로는 23시간*이다. `Period.ofDays(1)`을 더하면 같은 시각이 되고, `Duration.ofHours(24)`를 더하면 한 시간 어긋난 시각이 된다.

```java
ZonedDateTime before = ZonedDateTime.of(2026, 3, 7, 12, 0, 0, 0, ZoneId.of("America/New_York"));
ZonedDateTime byPeriod = before.plus(Period.ofDays(1));        // 2026-03-08T12:00 (정상)
ZonedDateTime byDuration = before.plus(Duration.ofHours(24));  // 2026-03-08T13:00 (한 시간 어긋남)
```

기억해두자. *달력 의미가 중요한 곳*에는 `Period`, *기계적 시간 간격이 중요한 곳*에는 `Duration`. 멱등성 토큰의 만료, 캐시 TTL, 락 보유 시간 같은 자리는 `Duration`이다. 청구서 발행 주기, 구독 만료일 같은 자리는 `Period`다.

## `ChronoUnit`과 `TemporalAdjusters`

`ChronoUnit`은 시간 단위의 열거형이다. `ChronoUnit.DAYS`, `ChronoUnit.MINUTES`, `ChronoUnit.HALF_DAYS` 같은 식이다. 두 시각 사이의 거리를 계산할 때 유용하다.

```java
long days = ChronoUnit.DAYS.between(start, end);
long minutes = ChronoUnit.MINUTES.between(start, end);
```

`TemporalAdjusters`는 *시각을 어떤 규칙에 맞춰 옮기는* 도구다. "이번 달의 마지막 영업일", "다음 월요일", "이번 분기의 첫 날" 같은 도메인 규칙을 *함수형으로* 표현한다.

```java
LocalDate lastDayOfMonth = LocalDate.now().with(TemporalAdjusters.lastDayOfMonth());
LocalDate nextMonday = LocalDate.now().with(TemporalAdjusters.next(DayOfWeek.MONDAY));
```

3장에서 다룬 함수형 인터페이스의 자취가 여기서도 보인다 — `TemporalAdjuster` 자체가 `@FunctionalInterface`다. 사용자 정의 조정자도 람다로 짤 수 있다.

```java
TemporalAdjuster nextWorkday = temporal -> {
    DayOfWeek day = DayOfWeek.of(temporal.get(ChronoField.DAY_OF_WEEK));
    int daysToAdd = switch (day) {
        case FRIDAY -> 3;
        case SATURDAY -> 2;
        default -> 1;
    };
    return temporal.plus(daysToAdd, ChronoUnit.DAYS);
};

LocalDate nextBusinessDay = LocalDate.now().with(nextWorkday);
```

## 시간대 — `ZoneId`와 DST

`ZoneId`는 "Asia/Seoul", "America/New_York" 같은 *지역 식별자*를 담는다. 단순 오프셋(`+09:00`)이 아니라 *DST 규칙을 포함한 지역의 시간 운영 정책 전체*를 가리킨다. 한국은 DST가 없어서 항상 UTC+9지만, 미국은 봄·가을마다 한 시간씩 움직인다.

운영에서 가장 자주 데이는 자리가 *서버 기본 시간대 가정*이다. 같은 코드가 개발자 노트북에서는 잘 돌다가 UTC로 설정된 운영 컨테이너에서 다른 결과를 낸다. 그래서 권장은 단순하다.

**서버는 UTC, 입출력에서만 변환한다.**

```java
// 컨테이너 시작 시
TZ=UTC

// 사용자에게 보일 때만 변환
ZonedDateTime displayTime = instant.atZone(userZoneId);
```

이 한 줄짜리 운영 규칙이 *시간대 버그의 60%를 막아준다*고 봐도 좋다.

## 포매팅 — `DateTimeFormatter`

`SimpleDateFormat`이 thread-unsafe였던 *그 끔찍한 시절*은 끝났다. `DateTimeFormatter`는 *immutable이고 thread-safe*다. 마음껏 static 필드로 공유해도 된다.

```java
public class TimeFormats {
    public static final DateTimeFormatter ISO = DateTimeFormatter.ISO_OFFSET_DATE_TIME;
    public static final DateTimeFormatter KOREAN = DateTimeFormatter.ofPattern("yyyy년 M월 d일 HH시 mm분");
    public static final DateTimeFormatter LOG_TS = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSSXXX");
}
```

ISO-8601 표준 포맷은 *직접 만들지 말고* `DateTimeFormatter.ISO_*` 상수들을 쓰는 편이 낫다. `ISO_INSTANT`, `ISO_LOCAL_DATE`, `ISO_OFFSET_DATE_TIME` 등이 미리 정의되어 있다.

파싱할 때 한 가지 주의점. `LocalDateTime.parse()`는 *입력 문자열에 시간대 정보가 있어도 버린다*. 시간대를 살리고 싶으면 `ZonedDateTime.parse()`나 `OffsetDateTime.parse()`를 써야 한다. 머리말의 정산 버그가 사실 이 자리와도 관련이 있다.

## JSON·JPA 직렬화 — 라이브러리와의 만남

`java.time`을 도입할 때 가장 자주 막히는 자리가 직렬화다. Jackson과 JPA 둘 다 *기본 설정에서는* `java.time`을 곱게 다뤄주지 않는다. 짚어두자.

**Jackson + java.time.** `jackson-datatype-jsr310` 모듈이 필요하다. Spring Boot 2 이후로는 자동 설정되지만, 두 가지 옵션을 명시하는 편이 낫다.

```java
ObjectMapper mapper = new ObjectMapper();
mapper.registerModule(new JavaTimeModule());
mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);  // ISO 문자열로
mapper.setTimeZone(TimeZone.getTimeZone("UTC"));
```

`WRITE_DATES_AS_TIMESTAMPS`를 끄지 않으면 `Instant`가 *epoch 초의 숫자*로 직렬화된다. API 응답에서는 거의 항상 ISO-8601 문자열이 낫다.

**JPA + java.time.** Hibernate 6부터는 `LocalDate`, `LocalDateTime`, `Instant`, `ZonedDateTime`을 *기본 지원*한다. 이전 버전에서는 `AttributeConverter`를 직접 짜야 했다.

```java
@Converter(autoApply = true)
public class InstantConverter implements AttributeConverter<Instant, Timestamp> {
    @Override public Timestamp convertToDatabaseColumn(Instant attribute) {
        return attribute == null ? null : Timestamp.from(attribute);
    }
    @Override public Instant convertToEntityAttribute(Timestamp dbData) {
        return dbData == null ? null : dbData.toInstant();
    }
}
```

`autoApply = true`로 두면 해당 타입을 가진 모든 Entity 필드에 자동 적용된다.

운영에서 한 가지 권장. *Entity의 시각 필드는 가급적 `Instant`로 통일*하는 편이 낫다. `LocalDateTime`을 Entity에 두면 시간대 책임이 *코드 어딘가에 분산*된다. `Instant`로 통일하면 DB에는 UTC, 응답 직렬화 시점에 사용자 시간대로 변환 — 흐름이 단순해진다.

## Kafka·로그 — 메시지 타임스탬프의 자리

Kafka의 `ProducerRecord`에는 `timestamp` 필드가 있다. 이 값은 *epoch 밀리초의 `long`*이다. `Instant.toEpochMilli()`로 채우는 편이 일관성 있다. Kafka Streams의 `WindowedBy` 윈도잉도 `Duration`을 받는다.

```java
KStream<String, Event> stream = ...;
stream.groupByKey()
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
    .aggregate(...)
```

로그 타임스탬프는 *반드시 ISO-8601 with offset*으로 적는 편이 낫다. `2026-05-04T14:30:00.123+09:00` 같은 형식이다. Logback의 `%date{ISO8601}` 패턴이 이 형식을 지원한다. 시간대 정보 없는 타임스탬프는 *멀티 리전 운영에서 추적을 끔찍하게 만든다*.

## Spring 맥락 — `@DateTimeFormat`과 친구들

Spring MVC는 `@DateTimeFormat`으로 *컨트롤러 파라미터의 파싱 형식*을 지정한다.

```java
@GetMapping("/orders")
public List<Order> orders(
    @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate from,
    @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate to
) { ... }
```

`?from=2026-05-01&to=2026-05-31` 같은 쿼리 파라미터가 자동으로 `LocalDate`로 바인딩된다. 만약 시각까지 받고 싶으면 `ISO.DATE_TIME`을 쓴다.

Spring Boot의 properties에서도 `Duration`이 자연스럽다.

```yaml
app:
  cache-ttl: 30m
  request-timeout: 5s
  retention-period: 7d
```

```java
@ConfigurationProperties("app")
public record AppProperties(Duration cacheTtl, Duration requestTimeout, Duration retentionPeriod) {}
```

문자열 `"30m"`이 자동으로 `Duration.ofMinutes(30)`으로 파싱된다. `30s`, `1h`, `7d` 등이 모두 지원된다. Boot 2.3 이후로는 `Period`도 같은 방식으로 받는다 — `1y`, `3M`, `14d` 같은 식이다.

## 마이그레이션 — `Date`/`Calendar`에서 옮겨오기

레거시 코드를 *살려 둔 채로* 점진 마이그레이션하는 패턴을 정리해두자.

**1단계 — 경계에서 변환.** 외부 라이브러리(JDBC, 오래된 SDK)가 `Date`를 반환하면, *받자마자* `Instant`로 변환한다.

```java
Date legacy = stmt.executeQuery().getDate(1);
Instant modern = legacy.toInstant();
```

반대로 외부에 `Date`를 줘야 하면, *나갈 때만* 변환한다.

```java
Date toLegacy = Date.from(instant);
```

**2단계 — 도메인 클래스의 시각 필드 교체.** Entity·DTO·Value Object의 `Date`/`Calendar` 필드를 차례로 `Instant`/`LocalDate`로 바꾼다. JPA `AttributeConverter`로 DB 컬럼은 그대로 둘 수 있어서 *마이그레이션을 점진적으로* 끌고 갈 수 있다.

**3단계 — `SimpleDateFormat` 추방.** 코드베이스 전체에서 `SimpleDateFormat`을 grep으로 찾아 `DateTimeFormatter`로 옮긴다. 단위 테스트가 *멀티스레드에서 잘 도는지*를 함께 확인하는 편이 낫다.

**4단계 — `Calendar` 산수 추방.** `cal.add(Calendar.DAY_OF_MONTH, 7)` 같은 코드를 `date.plusDays(7)`로 바꾼다. 가독성이 즉시 좋아진다.

**5단계 — 시간대 가정 점검.** 마지막 단계가 가장 어렵다. 코드베이스 전체에서 *시간대를 어디서 어떻게 가정*하고 있는지를 한 번 훑는다. 머리말의 정산 버그가 여기서 잡힌다.

## 한국 시간대 운영의 미세한 함정들

한국은 *DST가 없어서* 시간대 운영이 비교적 단순하다. 그래도 몇 가지는 짚어둘 만하다.

**Asia/Seoul vs +09:00.** 둘 다 *현재로서는* 같은 결과를 낸다. 그러나 `ZoneId.of("Asia/Seoul")`은 *지역 시간대 데이터베이스*를 가리킨다 — 만약 한국이 DST를 도입하기로 결정하면(역사적으로 1948년, 1949년, 1987~88년에 짧게 시행한 적이 있다) `Asia/Seoul`은 자동으로 적응한다. `+09:00`은 고정 오프셋이라 그렇지 않다. *지역 운영* 관점에서는 `ZoneId.of("Asia/Seoul")`을 쓰는 편이 미래 대비에 낫다.

**`tzdata` 업데이트.** JDK는 IANA의 `tzdata`를 내장하고 있다. 이 데이터는 *세계 어디선가* 시간대 규칙이 바뀔 때마다 갱신된다. JDK 마이너 버전 업데이트에서 `tzdata`가 함께 갱신되니, 운영 환경의 JDK를 *너무 오래 안 올리면* 외국 거래 처리에서 미세한 어긋남이 발생할 수 있다.

**Excel·CSV 시간대.** 한국 사용자가 익숙한 Excel은 시간대 개념이 없다. CSV로 시각을 주고받을 때, *어떤 시간대 기준의 시각인지*를 컬럼 이름이나 별도 컬럼으로 명시하자. 그냥 `"2026-05-04 14:30"`이라고만 적으면 받는 쪽이 *알아서 추측*하게 된다 — 추측은 틀린다.

## 종종 잊히는 Java 8의 보석들

`java.time`만큼 화려하진 않지만 *조용히 도움 되는* Java 8 추가 기능들을 잠깐 살펴보자. Map에 추가된 네 가지 메서드가 그중 백미다.

```java
// getOrDefault — null 체크 없이 기본값
String name = userIdToName.getOrDefault(userId, "anonymous");

// computeIfAbsent — 캐시 패턴의 정석
Map<String, List<Product>> byCategory = new HashMap<>();
products.forEach(p -> byCategory.computeIfAbsent(p.category(), k -> new ArrayList<>()).add(p));

// merge — 카운터·합계 누적
Map<String, Integer> counts = new HashMap<>();
words.forEach(w -> counts.merge(w, 1, Integer::sum));

// replaceAll — 전체 값 변환
prices.replaceAll((k, v) -> v.multiply(new BigDecimal("1.1")));
```

특히 `computeIfAbsent`는 *그동안 우리가 적어왔던* 6줄짜리 *putIfAbsent + get* 패턴을 한 줄로 줄여준다. `merge`는 카운팅·합계 누적 코드의 보일러플레이트를 거의 없앤다. 한번 써보면 `containsKey` 검사로 분기하던 옛 코드가 새삼 *번거롭게* 느껴진다.

`Optional`도 Java 8의 보석이지만, 그건 7장에서 따로 다룬다. 여기서는 한 가지만 짚자 — `Map.get()`의 결과를 *`Optional.ofNullable`로 감싸는 습관*은 좋은 출발이지만, 그게 정말 어디까지 가야 하는지는 7장에서 깊이 보자.

## 마무리

`java.time`은 Java 8의 *가장 조용하지만 가장 깊은* 변화다. 람다나 Stream만큼 화려하지 않아서 적게 언급되지만, 이 라이브러리가 11년 동안 막아낸 *시간대 버그의 양*은 측정하기 어려울 만큼 많다. 그리고 동시에, 우리가 *제대로 쓰지 못해 여전히 만들고 있는 시간대 버그*도 적지 않다.

정리하자면 시각의 의미를 일곱 가지로 *분리해서* 외우자. 기계 시각은 `Instant`, 사람 시각은 `ZonedDateTime`. 기간은 달력이면 `Period`, 기계면 `Duration`. 서버는 UTC로 돌리고 입출력에서만 변환하자. `SimpleDateFormat`은 다시 보지 말자. JPA Entity의 시각 필드는 `Instant`로 통일하는 편이 낫고, Hibernate 6 이후로는 변환자도 필요 없다.

다음 5장에서는 람다와 함수형 인터페이스가 *컬렉션 처리*와 만나서 생긴 변화 — Stream API — 를 들여다보자. 동료가 무심코 던진 `stream.parallel()` 한 줄이 운영을 어떻게 흔들 수 있는지, 그리고 그걸 막으려면 무엇을 알아야 하는지를 함께 살펴보자.
